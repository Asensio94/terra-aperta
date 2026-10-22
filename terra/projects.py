"""The sibling projects: what each one answers, how, where, and which live figure it shows.

Everything a reader sees about a project is written here, in Spanish and French. The bot
only adds what changes by itself: the figure (from the project's signals.json), when it was
last updated, its status (from its README) and whether a French page exists.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .i18n import day, n

BASE = "https://asensio94.github.io"
# Where a French page may live; the first one that answers in French wins.
FR_PATHS = ("fr/", "index.fr.html", "france.html")


@dataclass(frozen=True)
class Figure:
    """One live figure: a number and the sentence that says what it counts."""
    country: str | None
    value: float
    es: str
    fr: str


@dataclass(frozen=True)
class Page:
    """One page of a project's site, as the menu lists it."""
    es: str
    fr: str
    path: str = ""                 # relative to the project's url
    lang: str = "es"               # the language the page is written in
    only: str | None = None        # shown only to readers of this language (when both versions exist)

    def href(self, project_url: str) -> str:
        return project_url + self.path


@dataclass(frozen=True)
class Project:
    slug: str                      # repo name, also the path on github.io
    name: dict[str, str]
    question: dict[str, str]       # the question it answers, in plain words
    how: dict[str, str]            # how, in one or two sentences
    countries: tuple[str, ...]     # covered on its main branch today (the bot may add FR)
    figure: Callable[[list[dict]], list[Figure]] | None = None
    max_age_days: int = 3          # older than this = shown as not updated
    has_web: bool = True
    note: dict[str, str] = field(default_factory=dict)
    pages: tuple[Page, ...] = ()   # what the menu lists for it, in this order

    @property
    def url(self) -> str:
        return f"{BASE}/{self.slug}/"

    @property
    def repo(self) -> str:
        return f"https://github.com/Asensio94/{self.slug}"




def _since(signals: list[dict]) -> tuple[str, str]:
    d = min(s["date"] for s in signals)
    return day(d, "es"), day(d, "fr")


def _by_country(signals: list[dict]) -> dict[str | None, list[dict]]:
    out: dict[str | None, list[dict]] = {}
    for s in signals:
        out.setdefault(s.get("country"), []).append(s)
    order = {"ES": 0, "FR": 1}
    return dict(sorted(out.items(), key=lambda kv: order.get(kv[0], 2)))


def fig_observatorio(sig: list[dict]) -> list[Figure]:
    notices = [s for s in sig if s.get("kind") == "notice"]
    res = [s for s in sig if s.get("kind") == "resolution"]
    out = []
    if notices:
        es, fr = _since(notices)
        out.append(Figure("ES", len(notices),
                          f"anuncios del BOE y del Boletín de Cantabria con trámite ambiental desde el {es}",
                          f"avis du Journal officiel espagnol (BOE) et du Bulletin de Cantabrie avec procédure environnementale depuis le {fr}"))
    if res:
        out.append(Figure("ES", len(res), "resoluciones finales leídas, con sus condiciones",
                          "décisions finales lues, avec leurs prescriptions"))
    return out


def fig_vigia(sig: list[dict]) -> list[Figure]:
    out = []
    for c, ss in _by_country(sig).items():
        ss = [s for s in ss if s.get("kind") == "fire"]
        if not ss:
            continue
        es, fr = _since(ss)
        natura = sum(bool(s.get("sites")) for s in ss)
        out.append(Figure(c, natura, f"incendios que tocan la Red Natura 2000, de {n(len(ss), 'es')} con focos desde el {es}",
                          f"incendies qui touchent Natura 2000, sur {n(len(ss), 'fr')} avec foyers depuis le {fr}"))
    return out


_PILOT = {"ES": (" de Cantabria", " de Cantabrie"), "FR": (" de los Pirineos Atlánticos", " des Pyrénées-Atlantiques")}


def fig_centinela(sig: list[dict]) -> list[Figure]:
    out = []
    for c, ss in _by_country(sig).items():
        ok = [s for s in ss if s.get("status") == "confirmada"]
        if ss:
            es, fr = _since(ss)
            area_es, area_fr = _PILOT.get(c, ("", ""))
            out.append(Figure(c, len(ok), f"cambios confirmados dentro de espacios Natura 2000{area_es} desde el {es}",
                              f"changements confirmés à l'intérieur de sites Natura 2000{area_fr} depuis le {fr}"))
    return out


def fig_humedales(sig: list[dict]) -> list[Figure]:
    cur = [s for s in sig if s.get("status") == "vigente"]
    return [Figure("ES", len(cur), f"de {n(len(sig), 'es')} humedales españoles con lectura de agua reciente",
                   f"zones humides espagnoles sur {n(len(sig), 'fr')} avec une mesure d'eau récente")] if sig else []


def fig_caudal(sig: list[dict]) -> list[Figure]:
    below = sum(bool((s.get("details") or {}).get("below_now")) for s in sig)
    return [Figure("ES", below, f"puntos de aforo por debajo del mínimo hoy, de {n(len(sig), 'es')} que lo estuvieron algún día de los últimos 30 (datos provisionales)",
                   f"stations sous le minimum aujourd'hui, sur {n(len(sig), 'fr')} qui l'ont été un jour des 30 derniers (données provisoires)")] if sig else []


def fig_depuracion(sig: list[dict]) -> list[Figure]:
    out = []
    for c, ss in _by_country(sig).items():
        ww = sum(s.get("kind") == "wastewater" for s in ss)
        bw = sum(s.get("kind") == "bathing_water" for s in ss)
        if c == "FR":
            out.append(Figure(c, ww, "aglomeraciones no conformes según el veredicto oficial francés",
                              "agglomérations non conformes selon le verdict officiel"))
        else:
            out.append(Figure(c, ww, "aglomeraciones con indicios de no depurar como pide la directiva",
                              "agglomérations avec des indices d'épuration non conforme à la directive"))
        out.append(Figure(c, bw, "zonas de baño con calidad insuficiente en la última temporada",
                          "zones de baignade de qualité insuffisante la dernière saison"))
    return out


def fig_zona(sig: list[dict]) -> list[Figure]:
    total = sum((s.get("value") or {}).get("amount") or 0 for s in sig)
    return [Figure("ES", total, f"edificios fechados en 2017 o después dentro de zonas inundables, en {n(len(sig), 'es')} municipios de la Comunitat Valenciana",
                   f"bâtiments datés de 2017 ou après dans des zones inondables, dans {n(len(sig), 'fr')} communes de la Communauté valencienne")] if sig else []


def fig_tendidos(sig: list[dict]) -> list[Figure]:
    out = []
    for c, ss in _by_country(sig).items():
        total = sum((s.get("value") or {}).get("amount") or 0 for s in ss)
        out.append(Figure(c, total, f"apoyos y tramos de línea de riesgo alto dentro de {n(len(ss), 'es')} espacios Natura 2000",
                          f"pylônes et tronçons de ligne à risque élevé dans {n(len(ss), 'fr')} sites Natura 2000"))
    return out


def fig_subnocte(sig: list[dict]) -> list[Figure]:
    hi = sum(s.get("status") in ("high", "very high") for s in sig)
    return [Figure(None, hi, f"de {n(len(sig), 'es')} ciudades españolas con previsión de migración alta o muy alta esta noche",
                   f"villes espagnoles sur {n(len(sig), 'fr')} avec une migration forte ou très forte prévue cette nuit")] if sig else []



# The pages of each site, as listed under its menu item. Labels are in the reader's language;
# `lang` is the page's own, so the menu can say when a link leads to another language.
PAGES: dict[str, tuple[Page, ...]] = {
    "sub-nocte": (
        Page("Esta noche", "Cette nuit", ""),
        Page("Rutas", "Routes", "rutas.html"),
        Page("Parques eólicos", "Parcs éoliens", "parques.html"),
        Page("Método", "Méthode", "metodo.html"),
    ),
    "vigia-incendios": (
        Page("España: mapa en directo", "Espagne : carte en direct", ""),
        Page("España: mayores incendios", "Espagne : grands incendies", "incendio/"),
        Page("Francia: mapa en directo", "France : carte en direct", "fr/", "fr"),
        Page("Francia: mayores incendios", "France : grands incendies", "fr/incendio/", "fr"),
    ),
    "centinela-natura": (
        Page("España (Cantabria)", "Espagne (Cantabrie)", ""),
        Page("Francia (Pirineos Atlánticos)", "France (Pyrénées-Atlantiques)", "fr/", "fr"),
    ),
    "estado-iba": (
        Page("España", "Espagne", ""),
        Page("Francia", "France", "fr/", "fr"),
    ),
    "riesgo-tendidos-aves": (
        Page("Por regiones", "Par région", "regions.es.html", only="es"),
        Page("Por regiones", "Par région", "regions.fr.html", "fr", only="fr"),
        Page("El proyecto", "Le projet", "index.html", only="es"),
        Page("El proyecto", "Le projet", "index.fr.html", "fr", only="fr"),
    ),
    "observatorio-alegaciones": (
        Page("Alegaciones abiertas", "Consultations ouvertes", "index.html"),
        Page("Después del sí", "Après l'autorisation", "condicionado.html"),
        Page("Seguimiento", "Suivi", "seguimiento.html"),
        Page("Litoral", "Littoral", "litoral.html"),
        Page("Histórico", "Historique", "historico.html"),
    ),
    "grafo-promotores": (Page("Grafo de promotores", "Graphe des porteurs de projet", ""),),
    "vigilancia-humedales": (
        Page("España", "Espagne", ""),
        Page("Francia", "France", "france.html", "fr"),
    ),
    "caudal-ecologico": (Page("Caudal ecológico", "Débit écologique", ""),),
    "acuiferos-francia": (
        Page("Acuíferos de Francia", "Nappes de France", "", only="es"),
        Page("Acuíferos de Francia", "Nappes de France", "fr/", "fr", only="fr"),
    ),
    "depuracion-y-bano": (
        Page("España", "Espagne", ""),
        Page("Francia", "France", "fr/", "fr"),
    ),
    "zona-inundable": (Page("Construir en zona inundable", "Construire en zone inondable", ""),),
}

# The top bar, in this order. An item with more than one page opens a menu.
MENU: tuple[tuple[str, dict[str, str], tuple[str, ...]], ...] = (
    ("noche", {"es": "Sub Nocte", "fr": "Sub Nocte"}, ("sub-nocte",)),
    ("fuego", {"es": "Incendios", "fr": "Incendies"}, ("vigia-incendios",)),
    ("suelo", {"es": "Centinela", "fr": "Centinela"}, ("centinela-natura",)),
    ("iba", {"es": "IBA", "fr": "IBA"}, ("estado-iba",)),
    ("tendidos", {"es": "Tendidos", "fr": "Lignes"}, ("riesgo-tendidos-aves",)),
    ("alegaciones", {"es": "Alegaciones", "fr": "Consultations"}, ("observatorio-alegaciones", "grafo-promotores")),
    ("agua", {"es": "Agua", "fr": "Eau"}, ("vigilancia-humedales", "caudal-ecologico", "acuiferos-francia",
                                          "depuracion-y-bano", "zona-inundable")),
)

PROJECTS: list[Project] = [
    Project("sub-nocte", {"es": "Sub Nocte", "fr": "Sub Nocte"},
            {"es": "¿Cuántas aves migrarán esta noche sobre cada ciudad, y cuándo conviene apagar las luces?",
             "fr": "Combien d'oiseaux migreront cette nuit au-dessus de chaque ville, et quand faut-il éteindre les lumières ?"},
            {"es": "Previsión a partir de los perfiles abiertos de los radares meteorológicos europeos (Aloft) y de la meteorología. Ciudades de España, Francia y Portugal.",
             "fr": "Prévision à partir des profils ouverts des radars météorologiques européens (Aloft) et de la météo. Villes d'Espagne, de France et du Portugal."},
            ("ES", "FR"), fig_subnocte,
            pages=PAGES["sub-nocte"]),
    Project("vigia-incendios", {"es": "Vigía de incendios", "fr": "Vigie des incendies"},
            {"es": "¿Qué está ardiendo ahora, y toca un espacio protegido?",
             "fr": "Qu'est-ce qui brûle en ce moment, et cela touche-t-il un site protégé ?"},
            {"es": "Agrupa en incendios, varias veces al día, los focos de calor de los satélites VIIRS (NASA FIRMS) y los cruza con la Red Natura 2000. Después mide la superficie quemada con Sentinel-2.",
             "fr": "Regroupe en incendies, plusieurs fois par jour, les foyers de chaleur des satellites VIIRS (NASA FIRMS) et les croise avec Natura 2000. Mesure ensuite la surface brûlée avec Sentinel-2."},
            ("ES", "FR"), fig_vigia,
            pages=PAGES["vigia-incendios"]),
    Project("centinela-natura", {"es": "Centinela Natura", "fr": "Centinela Natura"},
            {"es": "¿Qué cambia físicamente dentro de los espacios Natura 2000: desbroces, movimientos de tierra, explanaciones?",
             "fr": "Qu'est-ce qui change physiquement dans les sites Natura 2000 : défrichements, terrassements, aplanissements ?"},
            {"es": "Compara imágenes Sentinel-2 cada pocos días con reglas espectrales fijas y señala la parcela catastral afectada. Piloto en Cantabria y en los Pirineos Atlánticos. Un cambio menor que unos píxeles, como una casa aislada, no se ve.",
             "fr": "Compare des images Sentinel-2 tous les quelques jours avec des règles spectrales fixes et indique la parcelle cadastrale concernée. Pilotes : Cantabrie et Pyrénées-Atlantiques. Un changement plus petit que quelques pixels, comme une maison isolée, n'est pas vu."},
            ("ES", "FR"), fig_centinela,
            pages=PAGES["centinela-natura"]),
    Project("estado-iba", {"es": "Estado de las IBA", "fr": "État des IBA"},
            {"es": "¿Qué saben todos estos proyectos de cada espacio importante para las aves y de cada municipio?",
             "fr": "Que savent tous ces projets de chaque site important pour les oiseaux et de chaque commune ?"},
            {"es": "Reúne en una ficha por espacio y por municipio lo que publican los demás proyectos: proyectos, fuego, suelo, agua, ríos y tendidos. Sin índices. De momento trabaja sobre las ZEPA, la figura legal que protege esas áreas.",
             "fr": "Réunit dans une fiche par site et par commune ce que publient les autres projets : projets, feu, sol, eau, rivières et lignes. Sans indice. Pour l'instant, il travaille sur les ZPS, le statut légal qui protège ces zones."},
            ("ES", "FR"),
            pages=PAGES["estado-iba"]),
    Project("riesgo-tendidos-aves", {"es": "Riesgo de tendidos para aves", "fr": "Risque des lignes pour les oiseaux"},
            {"es": "¿Qué aerogeneradores, apoyos eléctricos y tramos de línea ponen en más riesgo a las aves?",
             "fr": "Quelles éoliennes, quels pylônes et quels tronçons de ligne mettent le plus les oiseaux en danger ?"},
            {"es": "Cruza las líneas de OpenStreetMap y de las eléctricas con la presencia de aves (eBird, GBIF, Movebank) y el relieve, y ordena los elementos por riesgo de colisión y electrocución. Se actualiza cada mes.",
             "fr": "Croise les lignes d'OpenStreetMap et des gestionnaires de réseau avec la présence des oiseaux (eBird, GBIF, Movebank) et le relief, et classe les éléments par risque de collision et d'électrocution. Mis à jour chaque mois."},
            ("ES", "FR"), fig_tendidos, max_age_days=40,
            pages=PAGES["riesgo-tendidos-aves"]),
    Project("observatorio-alegaciones", {"es": "Observatorio de alegaciones", "fr": "Observatoire des consultations"},
            {"es": "¿Qué proyectos con impacto ambiental salen a información pública, cerca de qué espacios protegidos, y qué se les exigió al aprobarlos?",
             "fr": "Quels projets à impact environnemental sont soumis à consultation, près de quels sites protégés, et que leur a-t-on imposé en les autorisant ?"},
            {"es": "Lee cada mañana el BOE y el Boletín de Cantabria, cruza cada proyecto con la Red Natura 2000 y las especies amenazadas, y guarda la resolución final con sus condiciones, para poder alegar a tiempo.",
             "fr": "Lit chaque matin le Journal officiel espagnol (BOE) et le Bulletin de Cantabrie, croise chaque projet avec Natura 2000 et les espèces menacées, et garde la décision finale avec ses prescriptions, pour pouvoir réagir à temps."},
            ("ES",), fig_observatorio,
            pages=PAGES["observatorio-alegaciones"]),
    Project("grafo-promotores", {"es": "Grafo de promotores", "fr": "Graphe des porteurs de projet"},
            {"es": "¿Qué grupos empresariales están detrás de los proyectos energéticos, y cuáles parecen trocear uno grande en varios pequeños?",
             "fr": "Quels groupes sont derrière les projets énergétiques, et lesquels semblent découper un grand projet en plusieurs petits ?"},
            {"es": "Une los titulares de las instalaciones energéticas del BOE por el Registro Mercantil (BORME) y señala los conjuntos de un mismo grupo que se quedan por debajo de 50 MW, el umbral a partir del cual autoriza el Estado y no la comunidad autónoma. Indicios, no pruebas. Las personas físicas no aparecen.",
             "fr": "Relie les titulaires des installations énergétiques du BOE par le registre du commerce espagnol (BORME) et signale les ensembles d'un même groupe qui restent sous 50 MW, le seuil à partir duquel c'est l'État, et non la région, qui autorise. Des indices, pas des preuves. Les personnes physiques n'y figurent pas."},
            ("ES",),
            pages=PAGES["grafo-promotores"]),
    Project("vigilancia-humedales", {"es": "Vigilancia de humedales", "fr": "Veille des zones humides"},
            {"es": "¿Cuánta agua tienen los grandes humedales protegidos, y está turbia o eutrofizada?",
             "fr": "Combien d'eau ont les grandes zones humides protégées, et est-elle trouble ou eutrophisée ?"},
            {"es": "Superficie de agua, turbidez y clorofila (índices NDTI y NDCI) con Sentinel-2 cada pocos días, frente a la serie de cada humedal desde 2017. Doce humedales: seis en España y seis en Francia.",
             "fr": "Surface en eau, turbidité et chlorophylle (indices NDTI et NDCI) avec Sentinel-2 tous les quelques jours, face à la série de chaque zone humide depuis 2017. Douze sites : six en Espagne et six en France."},
            ("ES", "FR"), fig_humedales,
            pages=PAGES["vigilancia-humedales"]),
    Project("caudal-ecologico", {"es": "Caudal ecológico", "fr": "Débit écologique"},
            {"es": "¿Llevan los ríos el agua mínima que fija el plan hidrológico?",
             "fr": "Les rivières ont-elles le débit minimal fixé par le plan de bassin ?"},
            {"es": "Caudal diario de las estaciones de aforo frente al caudal ecológico de cada tramo. Ríos de cuatro cuencas. Los datos de aforo son provisionales, así que dice «por debajo del mínimo», nunca «incumple».",
             "fr": "Débit journalier des stations hydrométriques face au débit écologique de chaque tronçon. Rivières de quatre bassins. Les données sont provisoires : on écrit « sous le minimum », jamais « en infraction »."},
            ("ES",), fig_caudal,
            pages=PAGES["caudal-ecologico"]),
    Project("acuiferos-francia", {"es": "Acuíferos de Francia", "fr": "Nappes de France"},
            {"es": "¿Cómo están los acuíferos franceses frente a las restricciones de agua por sequía?",
             "fr": "Où en sont les nappes phréatiques françaises face aux restrictions d'eau ?"},
            {"es": "Nivel del agua en los pozos de control (piezómetros) de Hub'Eau frente a los decretos de sequía de VigiEau.",
             "fr": "Niveaux piézométriques de Hub'Eau face aux arrêtés sécheresse de VigiEau."},
            ("FR",),
            pages=PAGES["acuiferos-francia"]),
    Project("depuracion-y-bano", {"es": "Depuración y baño", "fr": "Épuration et baignade"},
            {"es": "¿Qué ciudades no depuran sus aguas como pide la directiva europea, y qué zonas de baño quedan aguas abajo?",
             "fr": "Quelles villes n'épurent pas leurs eaux comme l'exige la directive européenne, et quelles baignades se trouvent en aval ?"},
            {"es": "Informes de cada país a la Agencia Europea de Medio Ambiente sobre la directiva de aguas residuales (91/271), con la clasificación oficial de las zonas de baño. En España, los indicios salen de reglas propias sobre esos informes; en Francia se da el veredicto oficial del Estado.",
             "fr": "Rapports de chaque pays à l'Agence européenne pour l'environnement sur la directive eaux résiduaires urbaines (91/271), avec le classement officiel des baignades. En Espagne, les indices viennent de règles propres appliquées à ces rapports ; en France, c'est le verdict officiel de l'État."},
            ("ES", "FR"), fig_depuracion, max_age_days=40,
            pages=PAGES["depuracion-y-bano"]),
    Project("zona-inundable", {"es": "Construir en zona inundable", "fr": "Construire en zone inondable"},
            {"es": "¿Se sigue construyendo en zonas que se inundan?",
             "fr": "Construit-on encore dans des zones qui sont inondées ?"},
            {"es": "Edificios del Catastro por año de construcción dentro de las zonas inundables oficiales (SNCZI), antes y después del RD 638/2016. Piloto en la Comunitat Valenciana. El año puede ser el de una reforma.",
             "fr": "Les bâtiments du cadastre espagnol par année de construction dans les zones inondables officielles (SNCZI), avant et après la réforme de 2016. Pilote : Communauté valencienne. L'année peut être celle d'une rénovation."},
            ("ES",), fig_zona, max_age_days=40,
            pages=PAGES["zona-inundable"]),
]
