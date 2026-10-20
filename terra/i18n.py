"""Number and date formats, one per language (same pattern as humedales/i18n.py).

The Spanish page is written in Spanish and the French one in French; the data the bot
collects (docs/estado.json) stay language-independent.
"""
from __future__ import annotations

from datetime import datetime

LANGS = ("es", "fr")
_NNBSP = " "  # French: narrow no-break space for thousands and before «%»

MONTHS = {
    "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
           "octubre", "noviembre", "diciembre"],
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre",
           "octobre", "novembre", "décembre"],
}


def n(v: float, lang: str) -> str:
    """Integer with the thousands separator of the language: 46.709 / 46 709."""
    s = f"{v:,.0f}"
    return s.replace(",", "." if lang == "es" else _NNBSP)


def day(d: str, lang: str, year: bool = True) -> str:
    """'2026-10-20' -> «20 de octubre de 2026» / «20 octobre 2026»."""
    y, m, dd = int(d[:4]), int(d[5:7]), int(d[8:10])
    mes = MONTHS[lang][m - 1]
    if lang == "es":
        return f"{dd} de {mes}" + (f" de {y}" if year else "")
    return ("1er" if dd == 1 else str(dd)) + f" {mes}" + (f" {y}" if year else "")


def moment(t: datetime, lang: str) -> str:
    """A UTC instant: «20 de octubre de 2026, 09:31 UTC» / «20 octobre 2026, 9 h 31 UTC»."""
    d = day(t.strftime("%Y-%m-%d"), lang)
    if lang == "es":
        return f"{d}, {t:%H:%M} UTC"
    return f"{d}, {t.hour} h {t:%M} UTC"
