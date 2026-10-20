"""Read every sibling project and write docs/index.html, docs/fr/index.html and docs/estado.json."""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

from .collect import collect
from .web import render

DOCS = Path(__file__).resolve().parent.parent / "docs"
# If most projects cannot be read, the problem is the network, not the projects: keep the
# page that is already published instead of publishing a page full of failures.
MAX_FAILED_SHARE = 0.5


def write(state: dict, docs: Path = DOCS) -> None:
    (docs / "fr").mkdir(parents=True, exist_ok=True)
    (docs / "index.html").write_text(render(state, "es"), encoding="utf-8")
    (docs / "fr" / "index.html").write_text(render(state, "fr"), encoding="utf-8")
    (docs / "estado.json").write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    (docs / ".nojekyll").write_text("", encoding="utf-8")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    state = collect()
    failed = [s["slug"] for s in state["projects"] if "readme" in s["errors"] and "repo" in s["errors"]]
    if len(failed) > MAX_FAILED_SHARE * len(state["projects"]):
        logging.error("Could not read %d projects (%s); page left as it was.", len(failed), ", ".join(failed))
        sys.exit(1)
    for s in state["projects"]:
        logging.info("%-26s status=%s fr=%s figures=%d errors=%s", s["slug"], s["status"], bool(s["fr_url"]),
                     len(s["figures"]), ",".join(s["errors"]) or "-")
    write(state)


if __name__ == "__main__":
    main()
