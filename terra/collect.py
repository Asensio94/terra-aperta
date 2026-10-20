"""What the bot reads every day from each sibling project, all of it public.

- docs/signals.json (contract in estado-iba/CONTRATO.md): the live figure and its date.
- The README status line («Estado: activo / mantenimiento / aparcado»).
- Whether a French page exists (fr/, index.fr.html or france.html, answering with lang="fr").
- For projects without signals.json, the last push to the repo (GitHub API), as a fallback date.

A source that fails is recorded as failed and shown as such; nothing is guessed.
"""
from __future__ import annotations

import json
import logging
import os
import re
import urllib.request
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Callable

from .projects import FR_PATHS, PROJECTS, Project

log = logging.getLogger(__name__)
UA = "terra-aperta (https://github.com/Asensio94/naturaleza)"
STATUS_RE = re.compile(r"\*\*Estado: (activo|mantenimiento|aparcado)([^*]*)\*\*")

Fetch = Callable[[str], "tuple[int, str]"]


def http_get(url: str) -> tuple[int, str]:
    headers = {"User-Agent": UA}
    if url.startswith("https://api.github.com/") and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        log.warning("%s: %s", url, e)
        return 0, ""


def _parse_time(s: str) -> datetime | None:
    for fmt in ("%Y-%m-%dT%H:%MZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"):
        try:
            t = datetime.strptime(s, fmt)
            return t if t.tzinfo else t.replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    return None


def project_state(p: Project, get: Fetch, now: datetime) -> dict:
    st: dict = {"slug": p.slug, "errors": []}

    code, body = get(f"https://raw.githubusercontent.com/Asensio94/{p.slug}/HEAD/README.md")
    m = STATUS_RE.search(body) if code == 200 else None
    st["status"] = m.group(1) if m else None
    st["status_note"] = m.group(2).strip(" .()") if m else ""
    if code != 200:
        st["errors"].append("readme")

    st["fr_url"] = None
    if p.has_web:
        for path in FR_PATHS:
            code, body = get(p.url + path)
            if code == 200 and re.search(r'<html[^>]*\blang="fr', body, re.I):
                st["fr_url"] = p.url + path
                break

    st["signals"] = None
    st["figures"] = []
    st["updated"] = None
    st["updated_from"] = None
    if p.figure:
        code, body = get(p.url + "signals.json")
        try:
            data = json.loads(body) if code == 200 else None
        except json.JSONDecodeError:
            data = None
        if data is None:
            st["errors"].append("signals")
        else:
            sig = data.get("signals") or []
            st["signals"] = len(sig)
            st["countries_v2"] = sorted({s["country"] for s in sig if s.get("country")})
            st["figures"] = [asdict(f) for f in p.figure(sig)]
            t = _parse_time(data.get("generated") or "")
            if t:
                st["updated"], st["updated_from"] = t.isoformat(), "signals"
    if st["updated"] is None:
        code, body = get(f"https://api.github.com/repos/Asensio94/{p.slug}")
        try:
            t = _parse_time(json.loads(body)["pushed_at"]) if code == 200 else None
        except (json.JSONDecodeError, KeyError, TypeError):
            t = None
        if t:
            st["updated"], st["updated_from"] = t.isoformat(), "repo"
        else:
            st["errors"].append("repo")

    countries = set(p.countries) | set(st.get("countries_v2") or [])
    if st["fr_url"]:
        countries.add("FR")
    st["countries"] = [c for c in ("ES", "FR") if c in countries]
    if st["updated"]:
        age = (now - datetime.fromisoformat(st["updated"])).total_seconds() / 86400
        st["stale"] = age > p.max_age_days
    else:
        st["stale"] = None
    return st


def collect(get: Fetch = http_get, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    states = [project_state(p, get, now) for p in PROJECTS]
    return {"generated": now.strftime("%Y-%m-%dT%H:%MZ"), "projects": states}
