"""The index page, in Spanish (docs/index.html) and French (docs/fr/index.html).

The page has to explain itself to someone who arrives knowing nothing: what each project
answers, what its figure counts, where the data come from and what none of this is.
"""
from __future__ import annotations

from datetime import datetime
from html import escape
from pathlib import Path

from .i18n import moment, n
from .logo import LOGO_SVG, favicon_link
from .projects import GROUP_INTRO, GROUPS, PROJECTS, Project

COMMON_CSS = (Path(__file__).with_name("common.css")).read_text(encoding="utf-8")
ACCENT, ACCENT_DARK = "#a8432a", "#f08d6e"
REPO = "https://github.com/Asensio94/naturaleza"
FONTS = ("https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700"
         "&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=IBM+Plex+Mono:wght@400;500&display=swap")

T = {
    "es": {
        "title": "Terra Aperta: datos abiertos sobre naturaleza en España y Francia",
        "meta": ("Índice de dieciséis proyectos de datos abiertos que vigilan la naturaleza en España y Francia: "
                 "qué se tramita, qué arde, qué cambia, cómo va el agua y dónde peligran las aves."),
        "h1": "Terra <span>Aperta</span>",
        "lede": ("Dieciséis proyectos que vigilan la naturaleza en España y Francia con datos públicos: qué se quiere "
                 "construir, qué arde, qué cambia en los espacios protegidos, cómo va el agua y dónde peligran las aves. "
                 "Cada uno se actualiza solo y explica sus reglas. Esta página es el índice: dice qué hace cada uno y "
                 "lleva a él."),
        "latin": "<i lang=\"la\">Terra aperta</i> es latín: «tierra abierta», a la vista de todos.",
        "switch": ("Version française", "fr/"),
        "fig_projects": "proyectos",
        "fig_fr": "también en Francia",
        "fig_signals": "señales publicadas ahora",
        "fig_built": "revisado",
        "read_h": "Cómo leer esta página",
        "read": [
            "Cada ficha es un proyecto independiente, con su propia web. Arriba está la <b>pregunta</b> que responde "
            "y debajo, en una o dos frases, <b>cómo</b> lo hace.",
            "Las <b>cifras</b> son de hoy: un robot las lee cada día del fichero de señales que publica cada proyecto "
            "(<a href=\"#glosario\">glosario</a>). La frase de al lado dice exactamente qué cuentan. No se suman entre "
            "proyectos porque cada uno cuenta una cosa distinta.",
            "<b>España / Francia</b> lleva a la web de cada país, en su idioma. Si un proyecto aún no tiene versión en "
            "francés, se dice.",
            "La <b>fecha</b> es la de su última actualización. Si lleva más tiempo del normal sin actualizarse, la ficha "
            "lo marca en vez de esconderlo.",
            "El <b>estado</b> viene del propio proyecto: <span class=\"st st-activo\">activo</span> se actualiza y se "
            "sigue mejorando; <span class=\"st st-mantenimiento\">mantenimiento</span> se actualiza y se corrige, pero "
            "no crece; <span class=\"st st-aparcado\">aparcado</span> está parado, con el motivo a la vista.",
        ],
        "status": {"activo": "activo", "mantenimiento": "mantenimiento", "aparcado": "aparcado"},
        "es_link": "España", "fr_link": "France", "web": "Web", "code": "Código y método",
        "fr_missing": "Aún sin versión en francés.",
        "es_only_fr": "Web en español.",
        "no_web": "Sin web publicada.",
        "updated": "Actualizado el {t}",
        "updated_repo": "Última actividad del repositorio: {t}",
        "stale": "Lleva más de {d} días sin actualizarse",
        "no_figure": "No publica cifras para otros proyectos.",
        "failed": "Hoy no se ha podido leer su fichero de señales.",
        "covers": "Cubre",
        "country": {"ES": "España", "FR": "Francia", None: ""},
        "is_h": "Qué es y qué no es",
        "is": [
            "<b>Es</b> un conjunto de herramientas cívicas hechas por un particular con datos que ya son públicos: "
            "boletines oficiales, satélites europeos y de la NASA, registros y agencias ambientales.",
            "<b>No es</b> una fuente oficial ni una ONG, y no sustituye a ninguna administración. Lo que muestra son "
            "<b>indicios, no veredictos</b>: un satélite puede confundir una sombra con agua o una quema agrícola con un "
            "incendio. Cada proyecto dice en su web cómo se ha comprobado y dónde falla.",
            "<b>No usa inteligencia artificial</b> para decidir nada. Todo son reglas fijas, escritas y publicadas, que "
            "cualquiera puede revisar.",
            "<b>No publica nombres de personas</b> (propietarios, administradores, particulares) ni la ubicación de "
            "especies sensibles. Solo empresas, administraciones y datos agregados.",
            "El código es libre (licencia MIT) y los datos propios se pueden reutilizar citando la fuente (CC BY 4.0).",
        ],
        "method_h": "Cómo se hace esta página",
        "method": [
            "Los textos de cada ficha (pregunta, método, países) se escriben a mano en <code>terra/projects.py</code>.",
            "Cada día, un robot de GitHub Actions lee de cada proyecto su fichero de señales (<code>signals.json</code>), "
            "la línea de estado de su README y si tiene página en francés.",
            "Con esas señales calcula la cifra de cada ficha, siempre con una regla escrita en el mismo fichero: por "
            "ejemplo, para el vigía de incendios, cuántos de los incendios publicados tocan algún espacio Natura 2000.",
            "Si un proyecto no publica señales, solo se muestra la fecha de la última actividad de su repositorio.",
            "Si un proyecto lleva más días de lo normal sin actualizarse (3 para los diarios, 40 para los mensuales), la "
            "ficha lo dice. Si una fuente falla, también.",
            "Lo leído se guarda tal cual en <a href=\"estado.json\">estado.json</a>, para que cualquiera pueda "
            "comprobar las cifras.",
        ],
        "gloss_h": "Glosario",
        "gloss": [
            ("Red Natura 2000", "La red europea de espacios protegidos: ZEPA (para las aves) y ZEC (para hábitats y "
             "otras especies). En Francia, ZPS y ZSC."),
            ("IBA", "Áreas importantes para las aves (<i lang=\"en\">Important Bird and Biodiversity Areas</i>), "
             "inventariadas por BirdLife International; en España por SEO/BirdLife y en Francia por la LPO."),
            ("Señales (<code>signals.json</code>)", "El fichero común en el que cada proyecto publica lo que ha "
             "encontrado (un incendio, un cambio de suelo, un río bajo mínimos), con fecha, lugar y enlace. Así los "
             "proyectos se leen entre sí. Las reglas están en el contrato de "
             "<a href=\"https://github.com/Asensio94/estado-iba/blob/main/CONTRATO.md\">estado-iba</a>."),
            ("Sentinel-2", "Satélites europeos del programa Copernicus que fotografían cada punto cada pocos días "
             "con píxeles de 10 a 20 m."),
            ("VIIRS / FIRMS", "Sensor de satélite que detecta puntos calientes, y el servicio de la NASA que los "
             "publica unas horas después de cada pasada."),
            ("BOE", "Boletín Oficial del Estado, donde se publican en España los proyectos sometidos a evaluación "
             "ambiental y sus resoluciones."),
            ("INE / INSEE", "Los institutos de estadística. Sus códigos identifican cada municipio (España) o "
             "commune (Francia)."),
        ],
        "principle": "Datos públicos, reglas a la vista y cada cifra enlazada a su fuente. Indicios, no veredictos.",
        "footer": ("Hecho con datos públicos por un particular. Código y método en "
                   "<a href=\"{repo}\">GitHub</a>; para avisar de un error, abre una incidencia allí."),
        "siblings_aria": "Proyectos",
    },
    "fr": {
        "title": "Terra Aperta : données ouvertes sur la nature en Espagne et en France",
        "meta": ("Index de seize projets de données ouvertes qui surveillent la nature en Espagne et en France : "
                 "ce qui s'autorise, ce qui brûle, ce qui change, l'état de l'eau et les dangers pour les oiseaux."),
        "h1": "Terra <span>Aperta</span>",
        "lede": ("Seize projets qui surveillent la nature en Espagne et en France avec des données publiques : ce qui "
                 "veut se construire, ce qui brûle, ce qui change dans les sites protégés, l'état de l'eau et les dangers "
                 "pour les oiseaux. Chacun se met à jour tout seul et explique ses règles. Cette page en est l'index : "
                 "elle dit ce que fait chacun et y mène."),
        "latin": "<i lang=\"la\">Terra aperta</i> est du latin : « terre ouverte », à la vue de tous.",
        "switch": ("Versión en español", "../"),
        "fig_projects": "projets",
        "fig_fr": "aussi en France",
        "fig_signals": "signaux publiés en ce moment",
        "fig_built": "vérifié",
        "read_h": "Comment lire cette page",
        "read": [
            "Chaque fiche est un projet indépendant, avec son propre site. En haut, la <b>question</b> à laquelle il "
            "répond ; en dessous, en une ou deux phrases, <b>comment</b>.",
            "Les <b>chiffres</b> sont ceux du jour : un robot les lit chaque jour dans le fichier de signaux que publie "
            "chaque projet (<a href=\"#glossaire\">glossaire</a>). La phrase à côté dit exactement ce qu'ils comptent. "
            "On ne les additionne pas d'un projet à l'autre : chacun compte autre chose.",
            "<b>España / France</b> mène au site de chaque pays, dans sa langue. Si un projet n'a pas encore de version "
            "française, c'est indiqué.",
            "La <b>date</b> est celle de sa dernière mise à jour. S'il reste plus longtemps que d'habitude sans mise à "
            "jour, la fiche le signale au lieu de le cacher.",
            "L'<b>état</b> vient du projet lui-même : <span class=\"st st-activo\">actif</span> se met à jour et "
            "s'améliore ; <span class=\"st st-mantenimiento\">maintenance</span> se met à jour et se corrige, sans "
            "nouvelles fonctions ; <span class=\"st st-aparcado\">en pause</span> est arrêté, raison à l'appui sur son "
            "dépôt.",
        ],
        "status": {"activo": "actif", "mantenimiento": "maintenance", "aparcado": "en pause"},
        "es_link": "España", "fr_link": "France", "web": "Site", "code": "Code et méthode",
        "fr_missing": "Pas encore de version française.",
        "es_only_fr": "Site en espagnol.",
        "no_web": "Pas de site publié.",
        "updated": "Mis à jour le {t}",
        "updated_repo": "Dernière activité du dépôt : {t}",
        "stale": "Plus de {d} jours sans mise à jour",
        "no_figure": "Ne publie pas de chiffres pour les autres projets.",
        "failed": "Son fichier de signaux n'a pas pu être lu aujourd'hui.",
        "covers": "Couvre",
        "country": {"ES": "Espagne", "FR": "France", None: ""},
        "is_h": "Ce que c'est, et ce que ce n'est pas",
        "is": [
            "<b>C'est</b> un ensemble d'outils citoyens faits par un particulier avec des données déjà publiques : "
            "journaux officiels, satellites européens et de la NASA, registres et agences environnementales.",
            "<b>Ce n'est pas</b> une source officielle ni une ONG, et cela ne remplace aucune administration. Ce qui est "
            "montré, ce sont des <b>indices, pas des verdicts</b> : un satellite peut confondre une ombre avec de l'eau "
            "ou un brûlage agricole avec un incendie. Chaque projet dit sur son site comment il a été vérifié et où il "
            "se trompe.",
            "<b>Aucune intelligence artificielle</b> ne décide de quoi que ce soit. Ce sont des règles fixes, écrites "
            "et publiées, que chacun peut relire.",
            "<b>Aucun nom de personne</b> (propriétaires, dirigeants, particuliers) ni la localisation d'espèces "
            "sensibles n'est publié. Seulement des entreprises, des administrations et des données agrégées.",
            "Le code est libre (licence MIT) et les données propres sont réutilisables en citant la source "
            "(CC BY 4.0).",
        ],
        "method_h": "Comment cette page est faite",
        "method": [
            "Les textes de chaque fiche (question, méthode, pays) sont écrits à la main dans "
            "<code>terra/projects.py</code>.",
            "Chaque jour, un robot GitHub Actions lit pour chaque projet son fichier de signaux "
            "(<code>signals.json</code>), la ligne d'état de son README et s'il a une page en français.",
            "À partir de ces signaux, il calcule le chiffre de chaque fiche, toujours avec une règle écrite dans le "
            "même fichier : par exemple, pour la vigie des incendies, combien des incendies publiés touchent un site "
            "Natura 2000.",
            "Si un projet ne publie pas de signaux, seule la date de la dernière activité de son dépôt est affichée.",
            "Si un projet reste plus de jours que d'habitude sans mise à jour (3 pour les quotidiens, 40 pour les "
            "mensuels), la fiche l'indique. Si une source est en panne, aussi.",
            "Ce qui a été lu est gardé tel quel dans <a href=\"../estado.json\">estado.json</a>, pour que chacun "
            "puisse vérifier les chiffres.",
        ],
        "gloss_h": "Glossaire",
        "gloss": [
            ("Natura 2000", "Le réseau européen de sites protégés : ZPS (pour les oiseaux) et ZSC (pour les habitats et "
             "les autres espèces). En Espagne, ZEPA et ZEC."),
            ("IBA", "Zones importantes pour la conservation des oiseaux (<i lang=\"en\">Important Bird and Biodiversity "
             "Areas</i>), inventoriées par BirdLife International ; en France par la LPO, en Espagne par "
             "SEO/BirdLife."),
            ("Signaux (<code>signals.json</code>)", "Le fichier commun où chaque projet publie ce qu'il a trouvé (un "
             "incendie, un changement d'usage du sol, une rivière sous le minimum), avec date, lieu et lien. Les "
             "projets se lisent ainsi entre eux. Les règles sont dans le contrat d'"
             "<a href=\"https://github.com/Asensio94/estado-iba/blob/main/CONTRATO.md\">estado-iba</a> (en espagnol)."),
            ("Sentinel-2", "Satellites européens du programme Copernicus qui photographient chaque point tous les "
             "quelques jours, avec des pixels de 10 à 20 m."),
            ("VIIRS / FIRMS", "Capteur satellite qui détecte les points chauds, et le service de la NASA qui les "
             "publie quelques heures après chaque passage."),
            ("BOE", "Le Journal officiel espagnol (<i lang=\"es\">Boletín Oficial del Estado</i>), où sont publiés "
             "les projets soumis à évaluation environnementale et leurs décisions."),
            ("INE / INSEE", "Les instituts de statistique espagnol et français. Leurs codes identifient chaque "
             "municipio ou commune."),
        ],
        "principle": "Données publiques, règles en clair et chaque chiffre relié à sa source. Des indices, pas des verdicts.",
        "footer": ("Fait avec des données publiques par un particulier. Code et méthode sur "
                   "<a href=\"{repo}\">GitHub</a> ; pour signaler une erreur, ouvrez-y un ticket."),
        "siblings_aria": "Projets",
    },
}

CSS = """
.switch{justify-self:start;font:600 14px/1 var(--font-title);text-transform:uppercase;letter-spacing:.08em}
.site-header .latin{margin:0;color:var(--muted);font-size:15px}
main{max-width:1440px;margin:0 auto;padding:0 16px}
.reading{max-width:900px}
.reading h2,.group h2,.prose h2{margin:28px 0 6px;font:700 28px/1 var(--font-title);text-transform:uppercase;letter-spacing:.03em}
.reading ol{margin:8px 0 0;padding-left:22px;display:grid;gap:6px}
.group > p{margin:0 0 12px;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr));gap:14px}
.card{display:grid;gap:10px;align-content:start;border-top:4px solid var(--p);padding:14px 16px 16px}
.card h3{margin:0;font:700 23px/1.05 var(--font-title);text-transform:uppercase;letter-spacing:.02em}
.card h3 a{text-decoration:none}
.card h3 a:hover{text-decoration:underline;text-decoration-color:var(--p)}
.card .q{margin:0;font-weight:600}
.card .how{margin:0;font-size:15.5px}
.card .meta{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;font-size:14px}
.card .links{display:flex;flex-wrap:wrap;gap:6px 14px;font:600 15px/1.2 var(--font-title);text-transform:uppercase;letter-spacing:.06em}
.card .links a{text-decoration-color:var(--p)}
.card .links .code{font-weight:500;color:var(--muted)}
.figs{margin:0;padding:10px 0 0;border-top:1px solid var(--line);display:grid;gap:6px}
.figs div{display:grid;grid-template-columns:auto 1fr;gap:2px 10px;align-items:baseline}
.figs b{font:600 22px/1 var(--font-data);font-variant-numeric:tabular-nums;color:var(--accent)}
.figs span{font-size:14.5px}
.figs small{grid-column:2;font:600 11.5px/1 var(--font-title);text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
.when{color:var(--muted);font-size:13.5px;margin:0}
.warn{color:var(--ink);font-weight:600}
.warn::before{content:"⚠ ";color:var(--accent)}
.st{display:inline-block;font:600 12px/1 var(--font-title);text-transform:uppercase;letter-spacing:.09em;padding:4px 7px 3px;border:1.5px solid currentColor}
.st-activo{color:var(--natura)}
.st-mantenimiento{color:var(--muted)}
.st-aparcado{color:var(--accent)}
.flags{font:500 13px/1 var(--font-data);color:var(--muted)}
.prose{max-width:900px}
.prose ul,.prose ol{padding-left:22px;display:grid;gap:6px}
dl.gloss{display:grid;grid-template-columns:minmax(120px,max-content) 1fr;gap:8px 18px;max-width:900px}
dl.gloss dt{font:600 15px/1.35 var(--font-title);text-transform:uppercase;letter-spacing:.05em}
dl.gloss dd{margin:0}
@media (max-width:640px){dl.gloss{grid-template-columns:1fr}dl.gloss dd{margin-bottom:6px}}
"""


def _when(st: dict, p: Project, lang: str) -> str:
    L = T[lang]
    if not st.get("updated"):
        return ""
    t = moment(datetime.fromisoformat(st["updated"]), lang)
    txt = (L["updated"] if st["updated_from"] == "signals" else L["updated_repo"]).format(t=t)
    out = f'<p class="when">{escape(txt)}'
    if st.get("stale"):
        out += f' · <span class="warn">{escape(L["stale"].format(d=p.max_age_days))}</span>'
    return out + "</p>"


def _links(st: dict, p: Project, lang: str) -> str:
    L = T[lang]
    parts = []
    if not p.has_web:
        note = f'<span class="note">{L["no_web"]}</span>'
    else:
        note = ""
        if "ES" in p.countries or not p.countries:
            parts.append(f'<a href="{p.url}" hreflang="es">{L["es_link"] if p.countries else L["web"]}</a>')
        if st.get("fr_url"):
            parts.append(f'<a href="{st["fr_url"]}" hreflang="fr">{L["fr_link"]}</a>')
        elif "FR" in st["countries"] and "ES" not in p.countries:
            parts.append(f'<a href="{p.url}" hreflang="es">{L["fr_link"]}</a>')
            note = f'<span class="note">{L["es_only_fr"]}</span>'
        elif "ES" in p.countries:
            note = f'<span class="note">{L["fr_missing"]}</span>'
    parts.append(f'<a class="code" href="{p.repo}">{L["code"]}</a>')
    return f'<div class="links">{"".join(parts)}</div>' + (f'<div class="meta">{note}</div>' if note else "")


def _figs(st: dict, p: Project, lang: str) -> str:
    L = T[lang]
    if not p.figure:
        return f'<p class="when">{L["no_figure"]}</p>'
    if "signals" in st["errors"]:
        return f'<p class="when warn">{L["failed"]}</p>'
    rows = []
    many = len({f["country"] for f in st["figures"]}) > 1
    for f in st["figures"]:
        lab = f'<small>{L["country"][f["country"]]}</small>' if many and f["country"] else ""
        rows.append(f'<div><b>{n(f["value"], lang)}</b><span>{escape(f[lang])}</span>{lab}</div>')
    return f'<div class="figs">{"".join(rows)}</div>' if rows else ""


def card(p: Project, st: dict, lang: str, colors: dict[str, str]) -> str:
    L = T[lang]
    status = st.get("status")
    badge = f'<span class="st st-{status}">{L["status"][status]}</span>' if status else ""
    flags = " · ".join(L["country"][c] for c in st["countries"])
    covers = f'<span class="flags">{L["covers"]}: {flags}</span>' if flags else ""
    name_href = st.get("fr_url") if lang == "fr" and st.get("fr_url") else (p.url if p.has_web else p.repo)
    return (
        f'<article class="card" id="{p.slug}" style="--p:{colors.get(p.slug, "var(--accent)")}">'
        f'<h3><a href="{name_href}">{escape(p.name[lang])}</a></h3>'
        f'<div class="meta">{badge}{covers}</div>'
        f'<p class="q">{escape(p.question[lang])}</p>'
        f'<p class="how">{escape(p.how[lang])}</p>'
        f'{_figs(st, p, lang)}{_when(st, p, lang)}{_links(st, p, lang)}'
        "</article>"
    )


# Each project's own accent (estilo-comun/GUIA.md) marks its card, so it reads as the same
# colour the reader will find on its site.
ACCENTS = {
    "observatorio-alegaciones": "#9f1d35", "vigia-incendios": "#c2410c", "centinela-natura": "#2f7a55",
    "vigilancia-humedales": "#1d6a96", "sub-nocte": "#4a4fb5", "riesgo-tendidos-aves": "#8a5a00",
    "grafo-promotores": "#6b3fa0", "cartera-cotizadas": "#0f6b6b", "cuaderno-campo": "#5d6b1f",
    "caudal-ecologico": "#007c91", "estado-iba": "#a3336e", "barbechos-esteparias": "#7c4a2d",
    "depuracion-y-bano": "#2b59a6", "zona-inundable": "#4a5d75", "quien-tiene-sombra": "#3f7d20",
    "acuiferos-francia": "#7f3b8c",
}


def render(state: dict, lang: str) -> str:
    L = T[lang]
    by_slug = {s["slug"]: s for s in state["projects"]}
    built = moment(datetime.fromisoformat(state["generated"].replace("Z", "+00:00")), lang)
    total_signals = sum(s.get("signals") or 0 for s in state["projects"])
    in_fr = sum("FR" in s["countries"] for s in state["projects"])

    groups = []
    for g, names in GROUPS.items():
        cards = "".join(card(p, by_slug[p.slug], lang, ACCENTS) for p in PROJECTS if p.group == g)
        groups.append(f'<section class="group" id="{g}"><h2>{escape(names[lang])}</h2>'
                      f'<p>{escape(GROUP_INTRO[g][lang])}</p><div class="grid">{cards}</div></section>')
    gid = "glosario" if lang == "es" else "glossaire"
    siblings = "".join(
        f'<li><a href="{(by_slug[p.slug].get("fr_url") if lang == "fr" else None) or (p.url if p.has_web else p.repo)}">'
        f'{escape(p.name[lang])}</a></li>' for p in PROJECTS)
    figures = [(n(len(PROJECTS), lang), L["fig_projects"]), (n(in_fr, lang), L["fig_fr"]),
               (n(total_signals, lang), L["fig_signals"])]
    alt = "fr" if lang == "es" else "es"
    alt_href = "fr/" if lang == "es" else "../"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(L["title"])}</title>
<meta name="description" content="{escape(L["meta"])}">
<link rel="alternate" hreflang="{alt}" href="{alt_href}">
{favicon_link(ACCENT, ACCENT_DARK)}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<style>
{COMMON_CSS}
:root{{--accent:{ACCENT};--accent-dark:{ACCENT_DARK}}}
{CSS}
</style>
</head>
<body>
<header class="site-header">
  <a class="switch" href="{L["switch"][1]}" hreflang="{alt}" lang="{alt}">{L["switch"][0]}</a>
  <h1>{LOGO_SVG}{L["h1"]}</h1>
  <p class="lede">{escape(L["lede"])}</p>
  <p class="latin">{L["latin"]}</p>
  <div class="figures">{"".join(f"<div><b>{a}</b><span>{escape(b)}</span></div>" for a, b in figures)}
    <div><b style="font-size:18px">{escape(built)}</b><span>{escape(L["fig_built"])}</span></div></div>
</header>
<main>
<section class="reading"><h2>{L["read_h"]}</h2><ol>{"".join(f"<li>{x}</li>" for x in L["read"])}</ol></section>
{"".join(groups)}
<section class="prose" id="{"que-es" if lang == "es" else "ce-que-c-est"}"><h2>{escape(L["is_h"])}</h2>
<ul>{"".join(f"<li>{x}</li>" for x in L["is"])}</ul></section>
</main>
<section class="method"><h2>{escape(L["method_h"])}</h2><ol>{"".join(f"<li>{x}</li>" for x in L["method"])}</ol>
<h2 id="{gid}" style="margin-top:28px">{escape(L["gloss_h"])}</h2>
<dl class="gloss">{"".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in L["gloss"])}</dl></section>
<footer class="site-footer">
  <p class="principle">{escape(L["principle"])}</p>
  <p>{L["footer"].format(repo=REPO)}</p>
  <nav aria-label="{L["siblings_aria"]}"><ul class="siblings">{siblings}</ul></nav>
</footer>
</body>
</html>
"""
