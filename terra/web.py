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
from .projects import MENU, PROJECTS, Page, Project

COMMON_CSS = (Path(__file__).with_name("common.css")).read_text(encoding="utf-8")
ACCENT, ACCENT_DARK = "#a8432a", "#f08d6e"
REPO = "https://github.com/Asensio94/naturaleza"
FONTS = ("https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700"
         "&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=IBM+Plex+Mono:wght@400;500&display=swap")

T = {
    "es": {
        "title": "Terra Aperta: datos abiertos sobre naturaleza en España y Francia",
        "meta": ("Datos abiertos sobre la naturaleza de España y Francia: la migración de esta noche, lo que arde, "
                 "lo que cambia en los espacios protegidos, lo que se tramita y el agua."),
        "h1": "Terra <span>Aperta</span>",
        "lede": "Datos públicos sobre la naturaleza de España y Francia, leídos cada mañana.",
        "figures_at": "Cifras del {t}.",
        "nav_aria": "Proyectos",
        "menu_method": "Método",
        "method_page": "metodo.html",
        "method_title": "Cómo se lee y cómo se hace Terra Aperta",
        "method_cta": "Qué cuenta cada cifra, de dónde sale y qué no es esto: <a href=\"metodo.html\">método y glosario</a>.",
        "projects_h": "Qué hace cada proyecto",
        "latin": "<i lang=\"la\">Terra aperta</i> es latín: «tierra abierta», a la vista de todos.",
        "switch": "Français",
        "read_h": "Cómo leer esta página",
        "read": [
            "El <b>menú</b> de arriba lleva a cada web y a cada una de sus páginas. Si una página está en otro idioma, "
            "lo indica con <small class=\"lg\">ES</small> o <small class=\"lg\">FR</small>.",
            "Cada ficha es un proyecto independiente: la <b>pregunta</b> que responde, su <b>cifra de hoy</b> y la frase "
            "que dice exactamente qué cuenta. Un robot la lee cada mañana del fichero de señales que publica el proyecto "
            "(<a href=\"#glosario\">glosario</a>). Las cifras no se suman entre proyectos: cada uno cuenta una cosa "
            "distinta.",
            "La <b>fecha</b> es la de su última actualización. Si lleva más tiempo del normal sin actualizarse, la ficha "
            "lo marca en vez de esconderlo.",
            "Todos se actualizan solos. Los que dicen <span class=\"st st-mantenimiento\">mantenimiento</span> se "
            "corrigen, pero por ahora no crecen.",
        ],
        "status": {"activo": "activo", "mantenimiento": "mantenimiento", "aparcado": "aparcado"},
        "updated": "Actualizado el {t}",
        "updated_repo": "Última actividad del repositorio: {t}",
        "stale": "Lleva más de {d} días sin actualizarse",
        "failed": "Hoy no se ha podido leer su fichero de señales.",
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
    },
    "fr": {
        "title": "Terra Aperta : données ouvertes sur la nature en Espagne et en France",
        "meta": ("Données ouvertes sur la nature en Espagne et en France : la migration de cette nuit, ce qui brûle, "
                 "ce qui change dans les sites protégés, ce qui s'autorise et l'eau."),
        "h1": "Terra <span>Aperta</span>",
        "lede": "Des données publiques sur la nature en Espagne et en France, relues chaque matin.",
        "figures_at": "Chiffres du {t}.",
        "nav_aria": "Projets",
        "menu_method": "Méthode",
        "method_page": "methode.html",
        "method_title": "Comment lire et comment se fait Terra Aperta",
        "method_cta": "Ce que compte chaque chiffre, d'où il vient et ce que ce n'est pas : <a href=\"methode.html\">méthode et glossaire</a>.",
        "projects_h": "Ce que fait chaque projet",
        "latin": "<i lang=\"la\">Terra aperta</i> est du latin : « terre ouverte », à la vue de tous.",
        "switch": "Español",
        "read_h": "Comment lire cette page",
        "read": [
            "Le <b>menu</b> du haut mène à chaque site et à chacune de ses pages. Si une page est dans une autre langue, "
            "il l'indique par <small class=\"lg\">ES</small> ou <small class=\"lg\">FR</small>.",
            "Chaque fiche est un projet indépendant : la <b>question</b> à laquelle il répond, son <b>chiffre du jour</b> "
            "et la phrase qui dit exactement ce qu'il compte. Un robot le lit chaque matin dans le fichier de signaux que "
            "publie le projet (<a href=\"#glossaire\">glossaire</a>). On n'additionne pas les chiffres d'un projet à "
            "l'autre : chacun compte autre chose.",
            "La <b>date</b> est celle de sa dernière mise à jour. S'il reste plus longtemps que d'habitude sans mise à "
            "jour, la fiche le signale au lieu de le cacher.",
            "Tous se mettent à jour seuls. Ceux marqués <span class=\"st st-mantenimiento\">maintenance</span> sont "
            "corrigés, mais n'évoluent pas pour l'instant.",
        ],
        "status": {"activo": "actif", "mantenimiento": "maintenance", "aparcado": "en pause"},
        "updated": "Mis à jour le {t}",
        "updated_repo": "Dernière activité du dépôt : {t}",
        "stale": "Plus de {d} jours sans mise à jour",
        "failed": "Son fichier de signaux n'a pas pu être lu aujourd'hui.",
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
    },
}


BAR = {"bg": "#221d1a", "panel": "#2c2521", "line": "#41362f", "ink": "#efe7df", "dim": "#cbbfb5", "muted": "#a2958b"}

CSS = """
.tn{position:sticky;top:0;z-index:30;background:%(bg)s;color:%(ink)s;border-bottom:1px solid %(line)s;
  font:600 15px/1 var(--font-title);text-transform:uppercase;letter-spacing:.06em}
.tn .in{max-width:1180px;margin:0 auto;padding:0 16px;display:flex;align-items:center;gap:0 12px}
.tn a{color:inherit;text-decoration:none}
.tn .brand{display:flex;align-items:center;gap:6px;padding:10px 0;white-space:nowrap;font-weight:700}
.tn .brand span{color:%(accent)s}
.tn .logo{width:20px;height:20px;margin:0;color:%(ink)s}
.tn .logo .logo-breast{fill:%(accent)s}
.tn ul{display:flex;flex-wrap:wrap;margin:0;padding:0;list-style:none;flex:1}
.tn li{position:relative}
.tn .top,.tn summary{display:block;padding:13px 10px 11px;white-space:nowrap;border-bottom:3px solid transparent;color:%(dim)s;cursor:pointer;list-style:none}
.tn summary::-webkit-details-marker{display:none}
.tn summary::after{content:"";display:inline-block;margin-left:6px;border:4px solid transparent;border-top-color:currentColor;border-bottom:0;vertical-align:2px}
.tn .top:hover,.tn summary:hover,.tn details[open] summary{color:#fff}
.tn details[open] summary,.tn .top[aria-current=page]{color:#fff;border-bottom-color:%(accent)s}
.tn .dd{position:absolute;left:0;top:100%%;min-width:260px;background:%(panel)s;border:1px solid %(line)s;
  box-shadow:0 12px 28px rgba(0,0,0,.35);padding:6px 0;display:grid;text-transform:none;letter-spacing:0;font:500 16px/1.25 var(--font-text)}
.tn li:nth-last-child(-n+3) .dd{left:auto;right:0}
.tn .dd a{padding:8px 14px;color:%(ink)s}
.tn .dd a:hover,.tn .dd a:focus-visible{background:%(line)s}
.tn .dd-h{margin:10px 14px 2px;font:600 12px/1 var(--font-title);text-transform:uppercase;letter-spacing:.09em;color:%(muted)s}
.tn .dd-h:first-child{margin-top:6px}
.tn .lang{padding:6px 9px 5px;border:1.5px solid %(line)s;font-size:13px;white-space:nowrap;color:%(dim)s}
.tn .lang:hover{border-color:%(accent)s;color:#fff}
.tn a:focus-visible,.tn summary:focus-visible{outline:2px solid %(accent)s;outline-offset:-2px}
.lg{display:inline-block;font:600 10.5px/1 var(--font-title);letter-spacing:.06em;padding:2px 4px 1px;border:1px solid currentColor;margin-left:6px;opacity:.7;vertical-align:1px}
@media (max-width:820px){
  .tn{position:relative}.tn .in{flex-wrap:wrap}.tn .brand{order:1}.tn .lang{order:2;margin-left:auto}
  .tn ul{order:3;flex-basis:100%%;margin:0 -10px}
  .tn li{position:static}.tn .dd,.tn li:nth-last-child(-n+3) .dd{left:8px;right:8px;min-width:0}
}
.site-header{padding-bottom:6px}
.site-header .latin{margin:0;color:var(--muted);font-size:15px}
main{max-width:1180px;margin:0 auto;padding:0 16px 8px}
main h2{margin:30px 0 10px;font:700 26px/1 var(--font-title);text-transform:uppercase;letter-spacing:.03em}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%%,330px),1fr));gap:14px;margin-top:14px}
.card{display:grid;gap:10px;align-content:start;border-top:4px solid var(--p);padding:14px 16px 16px}
.card h3{margin:0;font:700 23px/1.05 var(--font-title);text-transform:uppercase;letter-spacing:.02em}
.card h3 a{text-decoration:none}
.card h3 a:hover{text-decoration:underline;text-decoration-color:var(--p)}
.card .q{margin:0}
.card.lead{margin-top:18px;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:12px 28px;padding:20px 22px}
.card.lead h3{font-size:34px}
.card.lead .q{font-size:19px}
.card.lead .figs{grid-row:1/span 4;grid-column:2;border-top:0;padding:0;align-content:center}
.card.lead .figs b{font-size:46px}
.card.lead .go{display:flex;flex-wrap:wrap;gap:8px}
.card.lead .go a{font:600 14px/1 var(--font-title);text-transform:uppercase;letter-spacing:.07em;padding:8px 11px 7px;border:1.5px solid var(--p);text-decoration:none}
.card.lead .go a:hover{background:var(--p);color:#fff}
@media (max-width:700px){.card.lead{grid-template-columns:1fr}.card.lead .figs{grid-row:auto;grid-column:auto}}
.figs{margin:0;padding:10px 0 0;border-top:1px solid var(--line);display:grid;gap:8px}
.figs div{display:grid;grid-template-columns:auto 1fr;gap:2px 10px;align-items:baseline}
.figs b{font:600 22px/1 var(--font-data);font-variant-numeric:tabular-nums;color:var(--accent)}
.figs span{font-size:14.5px}
.figs small{grid-column:2;font:600 11.5px/1 var(--font-title);text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
.when{color:var(--muted);font-size:13.5px;margin:0}
.warn{color:var(--ink);font-weight:600}
.warn::before{content:"⚠ ";color:var(--accent)}
.st{display:inline-block;font:600 12px/1 var(--font-title);text-transform:uppercase;letter-spacing:.09em;padding:4px 7px 3px;border:1.5px solid currentColor;vertical-align:4px;margin-left:8px}
.st-mantenimiento{color:var(--muted)}
.st-aparcado{color:var(--accent)}
.cta{margin:30px 0 0;font-size:16px}
.prose{max-width:900px}
.prose ul,.prose ol{padding-left:22px;display:grid;gap:6px}
dl.gloss{display:grid;grid-template-columns:minmax(140px,max-content) 1fr;gap:8px 18px;max-width:900px}
dl.gloss dt{font:600 15px/1.35 var(--font-title);text-transform:uppercase;letter-spacing:.05em}
dl.gloss dd{margin:0}
@media (max-width:640px){dl.gloss{grid-template-columns:1fr}dl.gloss dd{margin-bottom:6px}}
""" % {**BAR, "accent": ACCENT_DARK}

# Closes the open menu on a click elsewhere or on Escape, so only one is open at a time.
JS = """<script>
(function(){var all=function(){return document.querySelectorAll('.tn details[open]')};
document.addEventListener('click',function(e){all().forEach(function(d){if(!d.contains(e.target))d.removeAttribute('open')})});
document.addEventListener('keydown',function(e){if(e.key==='Escape')all().forEach(function(d){d.removeAttribute('open');d.querySelector('summary').focus()})});
})();</script>"""

# Each project's own accent (estilo-comun/GUIA.md) marks its card, so it reads as the same
# colour the reader will find on its site.
ACCENTS = {
    "observatorio-alegaciones": "#9f1d35", "vigia-incendios": "#c2410c", "centinela-natura": "#2f7a55",
    "vigilancia-humedales": "#1d6a96", "sub-nocte": "#4a4fb5", "riesgo-tendidos-aves": "#8a5a00",
    "grafo-promotores": "#6b3fa0", "caudal-ecologico": "#007c91", "estado-iba": "#a3336e",
    "depuracion-y-bano": "#2b59a6", "zona-inundable": "#4a5d75", "acuiferos-francia": "#7f3b8c",
}
BY_SLUG = {p.slug: p for p in PROJECTS}


def _pages(p: Project, lang: str) -> list[Page]:
    return [pg for pg in p.pages if pg.only in (None, lang)]


def _tag(pg: Page, lang: str) -> str:
    return f'<small class="lg" lang="{pg.lang}">{pg.lang.upper()}</small>' if pg.lang != lang else ""


def _link(p: Project, pg: Page, lang: str) -> str:
    return f'<a href="{pg.href(p.url)}" hreflang="{pg.lang}">{escape(getattr(pg, lang))}{_tag(pg, lang)}</a>'


def _main_page(p: Project, lang: str) -> Page:
    pages = _pages(p, lang)
    return next((pg for pg in pages if pg.lang == lang), pages[0])


def nav(lang: str, here: str) -> str:
    """The top bar. `here` is "home" or "method"."""
    L = T[lang]
    items = []
    for _key, label, slugs in MENU:
        ps = [BY_SLUG[s] for s in slugs]
        links = [(p, pg) for p in ps for pg in _pages(p, lang)]
        if len(links) == 1:
            p, pg = links[0]
            items.append(f'<li><a class="top" href="{pg.href(p.url)}">{escape(label[lang])}{_tag(pg, lang)}</a></li>')
            continue
        body = []
        for p in ps:
            pages = _pages(p, lang)
            if len(ps) > 1 and len(pages) > 1:
                body.append(f'<p class="dd-h">{escape(p.name[lang])}</p>')
            body += [_link(p, pg, lang) for pg in pages]
        items.append(f'<li><details><summary>{escape(label[lang])}</summary><div class="dd">{"".join(body)}</div>'
                     "</details></li>")
    cur = ' aria-current="page"' if here == "method" else ""
    items.append(f'<li><a class="top" href="{L["method_page"]}"{cur}>{escape(L["menu_method"])}</a></li>')
    other = "fr" if lang == "es" else "es"
    switch = {("es", "home"): "fr/", ("es", "method"): "fr/methode.html",
              ("fr", "home"): "../", ("fr", "method"): "../metodo.html"}[(lang, here)]
    return (f'<nav class="tn" aria-label="{escape(L["nav_aria"])}"><div class="in">'
            f'<a class="brand" href="./">{LOGO_SVG}Terra <span>Aperta</span></a>'
            f'<ul>{"".join(items)}</ul>'
            f'<a class="lang" href="{switch}" hreflang="{other}" lang="{other}">{L["switch"]}</a>'
            "</div></nav>")


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


def _figs(st: dict, p: Project, lang: str) -> str:
    L = T[lang]
    if not p.figure:
        return ""
    if "signals" in st["errors"]:
        return f'<p class="when warn">{L["failed"]}</p>'
    rows = []
    many = len({f["country"] for f in st["figures"]}) > 1
    for f in st["figures"]:
        lab = f'<small>{L["country"][f["country"]]}</small>' if many and f["country"] else ""
        rows.append(f'<div><b>{n(f["value"], lang)}</b><span>{escape(f[lang])}</span>{lab}</div>')
    return f'<div class="figs">{"".join(rows)}</div>' if rows else ""


def card(p: Project, st: dict, lang: str, lead: bool = False) -> str:
    L = T[lang]
    status = st.get("status")
    badge = f'<span class="st st-{status}">{L["status"][status]}</span>' if status in ("mantenimiento", "aparcado") else ""
    main = _main_page(p, lang)
    go = f'<div class="go">{"".join(_link(p, pg, lang) for pg in _pages(p, lang))}</div>' if lead else ""
    return (
        f'<article class="card{" lead" if lead else ""}" id="{p.slug}" style="--p:{ACCENTS.get(p.slug, "var(--accent)")}">'
        f'<h3><a href="{main.href(p.url)}" hreflang="{main.lang}">{escape(p.name[lang])}</a>{badge}</h3>'
        f'<p class="q">{escape(p.question[lang])}</p>'
        f'{_figs(st, p, lang)}{go}{_when(st, p, lang)}'
        "</article>"
    )


def _page(lang: str, here: str, title: str, body: str) -> str:
    L = T[lang]
    other = "fr" if lang == "es" else "es"
    alt = ("fr/" if lang == "es" else "../") + ("" if here == "home" else T[other]["method_page"])
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(L["meta"])}">
<link rel="alternate" hreflang="{other}" href="{alt}">
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
{nav(lang, here)}
{body}
<footer class="site-footer">
  <p class="principle">{escape(L["principle"])}</p>
  <p>{L["footer"].format(repo=REPO)}</p>
</footer>
{JS}
</body>
</html>
"""


def render(state: dict, lang: str) -> str:
    """The home page: the bar, one line of introduction and one card per project, in menu order."""
    L = T[lang]
    by_slug = {s["slug"]: s for s in state["projects"]}
    built = moment(datetime.fromisoformat(state["generated"].replace("Z", "+00:00")), lang)
    parts, loose = [], []
    for i, (key, label, slugs) in enumerate(MENU):
        cards = [card(BY_SLUG[s], by_slug[s], lang, lead=i == 0) for s in slugs]
        if i == 0:
            parts.append(cards[0])
        elif len(slugs) == 1:
            loose.append(cards[0])  # single projects share one grid
        else:
            if loose:
                parts.append(f'<div class="grid">{"".join(loose)}</div>')
                loose = []
            parts.append(f'<section id="{key}"><h2>{escape(label[lang])}</h2>'
                         f'<div class="grid">{"".join(cards)}</div></section>')
    if loose:
        parts.append(f'<div class="grid">{"".join(loose)}</div>')
    body = f"""<header class="site-header">
  <h1>{LOGO_SVG}{L["h1"]}</h1>
  <p class="lede">{escape(L["lede"])}</p>
  <p class="latin">{L["latin"]} {escape(L["figures_at"].format(t=built))}</p>
</header>
<main>
{"".join(parts)}
<p class="cta">{L["method_cta"]}</p>
</main>"""
    return _page(lang, "home", L["title"], body)


def render_method(state: dict, lang: str) -> str:
    """Everything that explains the page: how to read it, what each project does, what this is not, glossary."""
    L = T[lang]
    gid = "glosario" if lang == "es" else "glossaire"
    projects = "".join(
        f'<dt><a href="{_main_page(p, lang).href(p.url)}">{escape(p.name[lang])}</a></dt><dd>{escape(p.how[lang])}</dd>'
        for p in PROJECTS)
    body = f"""<header class="site-header">
  <h1>{escape(L["method_title"])}</h1>
</header>
<main class="prose">
<section><h2>{escape(L["read_h"])}</h2><ol>{"".join(f"<li>{x}</li>" for x in L["read"])}</ol></section>
<section><h2>{escape(L["projects_h"])}</h2><dl class="gloss">{projects}</dl></section>
<section><h2>{escape(L["is_h"])}</h2><ul>{"".join(f"<li>{x}</li>" for x in L["is"])}</ul></section>
<section><h2>{escape(L["method_h"])}</h2><ol>{"".join(f"<li>{x}</li>" for x in L["method"])}</ol></section>
<section><h2 id="{gid}">{escape(L["gloss_h"])}</h2>
<dl class="gloss">{"".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in L["gloss"])}</dl></section>
</main>"""
    return _page(lang, "method", f'{L["method_title"]} · Terra Aperta', body)
