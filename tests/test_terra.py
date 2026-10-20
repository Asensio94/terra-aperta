"""Offline tests: a fake fetch stands in for GitHub and the sibling projects."""
from __future__ import annotations

import json
import re
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from terra.build import write
from terra.collect import collect, project_state
from terra.i18n import day, moment, n
from terra.projects import MENU, PROJECTS, fig_caudal, fig_subnocte, fig_tendidos, fig_vigia
from terra.web import nav, render

NOW = datetime(2026, 10, 20, 10, 0, tzinfo=timezone.utc)
BY_SLUG = {p.slug: p for p in PROJECTS}


def fake_get(pages: dict[str, tuple[int, str]]):
    def get(url: str) -> tuple[int, str]:
        return pages.get(url, (404, ""))
    return get


def readme(status: str) -> str:
    return f"# X\n\n> **Estado: {status}.** Texto.\n"


class Formats(unittest.TestCase):
    def test_numbers(self):
        self.assertEqual(n(46709, "es"), "46.709")
        self.assertEqual(n(46709, "fr"), "46 709")

    def test_dates(self):
        self.assertEqual(day("2026-10-01", "es"), "1 de octubre de 2026")
        self.assertEqual(day("2026-10-01", "fr"), "1er octobre 2026")
        t = datetime(2026, 10, 20, 9, 31, tzinfo=timezone.utc)
        self.assertEqual(moment(t, "fr"), "20 octobre 2026, 9 h 31 UTC")


class Figures(unittest.TestCase):
    def test_vigia_counts_fires_touching_natura_per_country(self):
        sig = [
            {"kind": "fire", "country": "ES", "date": "2026-10-01", "sites": ["ES001"]},
            {"kind": "fire", "country": "ES", "date": "2026-10-02", "sites": []},
            {"kind": "fire", "country": "FR", "date": "2026-10-03", "sites": ["FR001"]},
        ]
        figs = {f.country: f for f in fig_vigia(sig)}
        self.assertEqual(figs["ES"].value, 1)
        self.assertIn("de 2 con focos desde el 1 de octubre de 2026", figs["ES"].es)
        self.assertEqual(figs["FR"].value, 1)

    def test_caudal_and_subnocte(self):
        caudal = [{"details": {"below_now": True}}, {"details": {"below_now": False}}, {}]
        self.assertEqual(fig_caudal(caudal)[0].value, 1)
        self.assertEqual(fig_caudal([]), [])
        night = [{"status": "very high"}, {"status": "high"}, {"status": "low"}]
        self.assertEqual(fig_subnocte(night)[0].value, 2)

    def test_tendidos_sums_elements(self):
        sig = [{"country": "ES", "value": {"amount": 3}}, {"country": "ES", "value": {"amount": 4}}]
        self.assertEqual(fig_tendidos(sig)[0].value, 7)


class Collect(unittest.TestCase):
    def test_signals_status_and_french_page(self):
        p = BY_SLUG["vigia-incendios"]
        data = {"generated": "2026-10-20T09:31Z", "signals": [
            {"kind": "fire", "country": "FR", "date": "2026-10-12", "sites": ["FR1"]}]}
        get = fake_get({
            f"https://raw.githubusercontent.com/Asensio94/{p.slug}/HEAD/README.md": (200, readme("activo")),
            p.url + "fr/": (200, '<html lang="fr"><body></body></html>'),
            p.url + "signals.json": (200, json.dumps(data)),
        })
        st = project_state(p, get, NOW)
        self.assertEqual(st["status"], "activo")
        self.assertEqual(st["fr_url"], p.url + "fr/")
        self.assertEqual(st["signals"], 1)
        self.assertEqual(st["updated_from"], "signals")
        self.assertFalse(st["stale"])
        self.assertIn("FR", st["countries"])
        self.assertEqual(st["errors"], [])

    def test_spanish_page_at_french_path_is_not_french(self):
        p = BY_SLUG["sub-nocte"]
        get = fake_get({p.url + "fr/": (200, '<html lang="es">')})
        self.assertIsNone(project_state(p, get, NOW)["fr_url"])

    def test_without_signals_uses_last_push_and_marks_stale(self):
        p = BY_SLUG["grafo-promotores"]
        get = fake_get({
            f"https://api.github.com/repos/Asensio94/{p.slug}": (200, json.dumps({"pushed_at": "2026-10-01T08:00:00Z"})),
        })
        st = project_state(p, get, NOW)
        self.assertEqual(st["updated_from"], "repo")
        self.assertTrue(st["stale"])
        self.assertEqual(st["errors"], ["readme"])

    def test_broken_signals_are_reported_not_guessed(self):
        p = BY_SLUG["caudal-ecologico"]
        get = fake_get({p.url + "signals.json": (200, "{not json")})
        st = project_state(p, get, NOW)
        self.assertIn("signals", st["errors"])
        self.assertEqual(st["figures"], [])


class Page(unittest.TestCase):
    def test_renders_both_languages_even_when_everything_failed(self):
        state = collect(get=fake_get({}), now=NOW)
        es, fr = render(state, "es"), render(state, "fr")
        self.assertIn('<html lang="es"', es)
        self.assertIn('<html lang="fr"', fr)
        for p in PROJECTS:
            self.assertIn(f'id="{p.slug}"', es)
            self.assertIn(p.name["fr"].replace("'", "&#x27;"), fr)
        with tempfile.TemporaryDirectory() as d:
            write(state, Path(d))
            for f in ("index.html", "metodo.html", "fr/index.html", "fr/methode.html"):
                self.assertTrue((Path(d) / f).exists(), f)
            self.assertEqual(len(json.loads((Path(d) / "estado.json").read_text("utf-8"))["projects"]), len(PROJECTS))


class Bar(unittest.TestCase):
    def test_every_project_is_in_the_menu_once(self):
        slugs = [s for _key, _label, ss in MENU for s in ss]
        self.assertEqual(sorted(slugs), sorted(p.slug for p in PROJECTS))
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_menu_lists_each_page_and_marks_other_languages(self):
        es, fr = nav("es", "home"), nav("fr", "home")
        tendidos = BY_SLUG["riesgo-tendidos-aves"].url
        self.assertIn(f'href="{tendidos}regions.es.html"', es)
        self.assertNotIn(f'href="{tendidos}regions.es.html"', fr)   # French readers get the French map
        self.assertIn(f'href="{BY_SLUG["sub-nocte"].url}rutas.html"', fr)
        self.assertIn('<small class="lg" lang="es">ES</small>', fr)
        self.assertIn('href="fr/"', es)
        self.assertIn('href="../metodo.html"', nav("fr", "method"))

    def test_external_links_open_in_a_new_tab_and_internal_ones_do_not(self):
        state = collect(get=fake_get({}), now=NOW)
        for lang in ("es", "fr"):
            html = render(state, lang)
            anchors = re.findall(r"<a [^>]*>", html)
            external = [a for a in anchors if 'href="http' in a]
            self.assertTrue(external)
            for a in external:
                self.assertIn('target="_blank" rel="noopener"', a)
            for a in anchors:
                if 'href="http' not in a:
                    self.assertNotIn("target=", a)


if __name__ == "__main__":
    unittest.main()
