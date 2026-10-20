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
class Project:
    slug: str                      # repo name, also the path on github.io
    name: dict[str, str]
    group: str
    question: dict[str, str]       # the question it answers, in plain words
    how: dict[str, str]            # how, in one or two sentences
    countries: tuple[str, ...]     # covered on its main branch today (the bot may add FR)
    figure: Callable[[list[dict]], list[Figure]] | None = None
    max_age_days: int = 3          # older than this = shown as not updated
    has_web: bool = True
    note: dict[str, str] = field(default_factory=dict)

    @property
    def url(self) -> str:
        return f"{BASE}/{self.slug}/"

    @property
    def repo(self) -> str:
        return f"https://github.com/Asensio94/{self.slug}"


GROUPS = {
    "permisos": {"es": "Lo que se quiere construir", "fr": "Ce qui veut se construire"},
    "suelo": {"es": "Fuego y suelo", "fr": "Feu et sol"},
    "agua": {"es": "Agua", "fr": "Eau"},
    "aves": {"es": "Aves", "fr": "Oiseaux"},
    "ciudad": {"es": "Ciudad", "fr": "Ville"},
    "campo": {"es": "En el campo", "fr": "Sur le terrain"},
}
GROUP_INTRO = {
    "permisos": {"es": "Quién quiere hacer qué, dónde, y qué le exigieron.",
                 "fr": "Qui veut faire quoi, où, et ce qu'on lui a imposé."},
    "suelo": {"es": "Lo que se quema, se desbroza o se ara.",
              "fr": "Ce qui brûle, se défriche ou se laboure."},
    "agua": {"es": "Humedales, ríos, acuíferos, vertidos e inundaciones.",
             "fr": "Zones humides, rivières, nappes, rejets et inondations."},
    "aves": {"es": "Los espacios de las aves, los tendidos que las matan y su migración.",
             "fr": "Les sites des oiseaux, les lignes qui les tuent et leur migration."},
    "ciudad": {"es": "La naturaleza que falta donde vive la gente.",
               "fr": "La nature qui manque là où vivent les gens."},
    "campo": {"es": "Una herramienta para quien sale a mirar.",
              "fr": "Un outil pour qui sort observer."},
}


def _since(signals: list[dict]) -> tuple[str, str]:
    d = min(s["date"] for s in signals)
    return day(d, "es"), day(d, "fr")


def _by_country(signals: list[dict]) -> dict[str | None, list[dict]]:
    out: dict[str | None, list[dict]] = {}
    for s in signals:
        out.setdefault(s.get("country"), []).append(s)
    return out


def fig_observatorio(sig: list[dict]) -> list[Figure]:
    notices = [s for s in sig if s.get("kind") == "notice"]
    res = [s for s in sig if s.get("kind") == "resolution"]
    out = []
    if notices:
        es, fr = _since(notices)
        out.append(Figure("ES", len(notices),
                          f"anuncios del BOE con trámite ambiental desde el {es}",
                          f"avis du Journal officiel espagnol (BOE) avec procédure environnementale depuis le {fr}"))
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


def fig_centinela(sig: list[dict]) -> list[Figure]:
    out = []
    for c, ss in _by_country(sig).items():
        ok = [s for s in ss if s.get("status") == "confirmada"]
        if ss:
            es, fr = _since(ss)
            out.append(Figure(c, len(ok), f"cambios confirmados dentro de espacios Natura 2000 desde el {es}",
                              f"changements confirmés à l'intérieur de sites Natura 2000 depuis le {fr}"))
    return out


def fig_humedales(sig: list[dict]) -> list[Figure]:
    cur = [s for s in sig if s.get("status") == "vigente"]
    return [Figure("ES", len(cur), "humedales españoles con lectura de agua reciente",
                   "zones humides espagnoles avec une mesure d'eau récente")] if sig else []


def fig_caudal(sig: list[dict]) -> list[Figure]:
    below = sum(bool((s.get("details") or {}).get("below_now")) for s in sig)
    return [Figure("ES", below, f"de {n(len(sig), 'es')} puntos de aforo, por debajo del mínimo según datos provisionales",
                   f"sur {n(len(sig), 'fr')} stations, sous le minimum d'après des données provisoires")] if sig else []


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
    return [Figure("ES", total, "edificios fechados en 2017 o después dentro de zonas inundables",
                   "bâtiments datés de 2017 ou après dans des zones inondables")] if sig else []


def fig_tendidos(sig: list[dict]) -> list[Figure]:
    out = []
    for c, ss in _by_country(sig).items():
        total = sum((s.get("value") or {}).get("amount") or 0 for s in ss)
        out.append(Figure(c, total, f"apoyos y tramos de línea de riesgo alto dentro de {n(len(ss), 'es')} espacios Natura 2000",
                          f"pylônes et tronçons de ligne à risque élevé dans {n(len(ss), 'fr')} sites Natura 2000"))
    return out


def fig_subnocte(sig: list[dict]) -> list[Figure]:
    hi = sum(s.get("status") in ("high", "very high") for s in sig)
    return [Figure(None, hi, f"de {n(len(sig), 'es')} ciudades con previsión de migración alta o muy alta esta noche",
                   f"villes sur {n(len(sig), 'fr')} avec une migration forte ou très forte prévue cette nuit")] if sig else []


PROJECTS: list[Project] = [
    Project("observatorio-alegaciones", {"es": "Observatorio de alegaciones", "fr": "Observatoire des consultations"},
            "permisos",
            {"es": "¿Qué proyectos con impacto ambiental salen a información pública, cerca de qué espacios protegidos, y qué se les exigió al aprobarlos?",
             "fr": "Quels projets à impact environnemental sont soumis à consultation, près de quels sites protégés, et que leur a-t-on imposé en les autorisant ?"},
            {"es": "Lee cada mañana el BOE, cruza cada proyecto con la Red Natura 2000 y las especies amenazadas, y guarda la resolución final con sus condiciones, para poder alegar a tiempo.",
             "fr": "Lit chaque matin le Journal officiel espagnol (BOE), croise chaque projet avec Natura 2000 et les espèces menacées, et garde la décision finale avec ses prescriptions, pour pouvoir réagir à temps."},
            ("ES",), fig_observatorio),
    Project("grafo-promotores", {"es": "Grafo de promotores", "fr": "Graphe des porteurs de projet"}, "permisos",
            {"es": "¿Qué empresas y grupos están detrás de los proyectos que se tramitan?",
             "fr": "Quelles entreprises et quels groupes sont derrière les projets en cours d'autorisation ?"},
            {"es": "Une cada promotor de los proyectos del observatorio con su grupo empresarial a partir de registros mercantiles públicos. Las personas físicas no aparecen.",
             "fr": "Relie chaque porteur de projet de l'observatoire à son groupe à partir des registres publics des sociétés. Les personnes physiques n'y figurent pas."},
            ("ES",)),
    Project("cartera-cotizadas", {"es": "Cartera de las cotizadas", "fr": "Portefeuille des sociétés cotées"}, "permisos",
            {"es": "¿Qué tramitan en España las renovables que cotizan en bolsa, qué les exigieron y qué dicen de la Red Natura 2000?",
             "fr": "Que font autoriser en Espagne les sociétés d'énergies renouvelables cotées en bourse, que leur a-t-on imposé, et que disent-elles de Natura 2000 ?"},
            {"es": "Cada dato lleva su prueba documental (BOE, declaraciones de impacto, informes a inversores). Sin puntuaciones.",
             "fr": "Chaque donnée a sa preuve documentaire (BOE, avis environnementaux, rapports aux investisseurs). Aucune note."},
            ("ES",), max_age_days=40),
    Project("vigia-incendios", {"es": "Vigía de incendios", "fr": "Vigie des incendies"}, "suelo",
            {"es": "¿Qué está ardiendo ahora, y toca un espacio protegido?",
             "fr": "Qu'est-ce qui brûle en ce moment, et cela touche-t-il un site protégé ?"},
            {"es": "Agrupa en incendios, varias veces al día, los focos de calor de los satélites VIIRS (NASA FIRMS) y los cruza con la Red Natura 2000. Después mide la superficie quemada con Sentinel-2.",
             "fr": "Regroupe en incendies, plusieurs fois par jour, les foyers de chaleur des satellites VIIRS (NASA FIRMS) et les croise avec Natura 2000. Mesure ensuite la surface brûlée avec Sentinel-2."},
            ("ES", "FR"), fig_vigia),
    Project("centinela-natura", {"es": "Centinela Natura", "fr": "Centinela Natura"}, "suelo",
            {"es": "¿Qué cambia físicamente dentro de los espacios Natura 2000: desbroces, movimientos de tierra, construcciones?",
             "fr": "Qu'est-ce qui change physiquement dans les sites Natura 2000 : défrichements, terrassements, constructions ?"},
            {"es": "Compara imágenes Sentinel-2 cada pocos días con reglas espectrales fijas y señala la parcela catastral afectada. Piloto en Cantabria y en los Pirineos Atlánticos.",
             "fr": "Compare des images Sentinel-2 tous les quelques jours avec des règles spectrales fixes et indique la parcelle cadastrale concernée. Pilotes : Cantabrie et Pyrénées-Atlantiques."},
            ("ES", "FR"), fig_centinela),
    Project("barbechos-esteparias", {"es": "Barbechos y esteparias", "fr": "Jachères et oiseaux steppiques"}, "suelo",
            {"es": "¿Cuánto barbecho queda en las comarcas de las aves esteparias?",
             "fr": "Combien de jachères reste-t-il là où vivent les oiseaux steppiques ?"},
            {"es": "Barbecho por comarca estimado con Sentinel-2 y contrastado con la PAC, frente a las ZEPA de aves esteparias.",
             "fr": "Les jachères par petite région, estimées avec Sentinel-2 et comparées à la PAC, face aux ZPS d'oiseaux steppiques."},
            ("ES",), has_web=False),
    Project("vigilancia-humedales", {"es": "Vigilancia de humedales", "fr": "Veille des zones humides"}, "agua",
            {"es": "¿Cuánta agua tienen los grandes humedales protegidos, y está turbia o eutrofizada?",
             "fr": "Combien d'eau ont les grandes zones humides protégées, et est-elle trouble ou eutrophisée ?"},
            {"es": "Superficie de agua, turbidez y clorofila con Sentinel-2 cada pocos días, frente a la serie de cada humedal desde 2017. Doce humedales: seis en España y seis en Francia.",
             "fr": "Surface en eau, turbidité et chlorophylle avec Sentinel-2 tous les quelques jours, face à la série de chaque zone humide depuis 2017. Douze sites : six en Espagne et six en France."},
            ("ES", "FR"), fig_humedales),
    Project("caudal-ecologico", {"es": "Caudal ecológico", "fr": "Débit écologique"}, "agua",
            {"es": "¿Llevan los ríos el agua mínima que fija el plan hidrológico?",
             "fr": "Les rivières ont-elles le débit minimal fixé par le plan de bassin ?"},
            {"es": "Caudal diario de las estaciones de aforo frente al caudal ecológico de cada tramo. Los datos de aforo son provisionales, así que dice «por debajo del mínimo», nunca «incumple».",
             "fr": "Débit journalier des stations hydrométriques face au débit écologique de chaque tronçon. Les données sont provisoires : on écrit « sous le minimum », jamais « en infraction »."},
            ("ES",), fig_caudal),
    Project("acuiferos-francia", {"es": "Acuíferos de Francia", "fr": "Nappes de France"}, "agua",
            {"es": "¿Cómo están los acuíferos franceses frente a las restricciones de agua por sequía?",
             "fr": "Où en sont les nappes phréatiques françaises face aux restrictions d'eau ?"},
            {"es": "Niveles piezométricos de Hub'Eau frente a los decretos de sequía de VigiEau.",
             "fr": "Niveaux piézométriques de Hub'Eau face aux arrêtés sécheresse de VigiEau."},
            ("FR",)),
    Project("depuracion-y-bano", {"es": "Depuración y baño", "fr": "Épuration et baignade"}, "agua",
            {"es": "¿Qué ciudades no depuran sus aguas como pide la directiva europea, y qué zonas de baño quedan aguas abajo?",
             "fr": "Quelles villes n'épurent pas leurs eaux comme l'exige la directive européenne, et quelles baignades se trouvent en aval ?"},
            {"es": "Informes de cada país a la Agencia Europea de Medio Ambiente sobre la directiva de aguas residuales (91/271), con la clasificación oficial de las zonas de baño.",
             "fr": "Rapports de chaque pays à l'Agence européenne pour l'environnement sur la directive eaux résiduaires urbaines (91/271), avec le classement officiel des baignades."},
            ("ES", "FR"), fig_depuracion, max_age_days=40),
    Project("zona-inundable", {"es": "Construir en zona inundable", "fr": "Construire en zone inondable"}, "agua",
            {"es": "¿Se sigue construyendo en zonas que se inundan?",
             "fr": "Construit-on encore dans des zones qui sont inondées ?"},
            {"es": "Edificios del Catastro por año de construcción dentro de las zonas inundables oficiales (SNCZI), antes y después del RD 638/2016. Piloto en la Comunitat Valenciana. El año puede ser el de una reforma.",
             "fr": "Les bâtiments du cadastre espagnol par année de construction dans les zones inondables officielles (SNCZI), avant et après la réforme de 2016. Pilote : Communauté valencienne. L'année peut être celle d'une rénovation."},
            ("ES",), fig_zona, max_age_days=40),
    Project("estado-iba", {"es": "Estado de las IBA", "fr": "État des IBA"}, "aves",
            {"es": "¿Qué saben todos estos proyectos de cada espacio importante para las aves y de cada municipio?",
             "fr": "Que savent tous ces projets de chaque site important pour les oiseaux et de chaque commune ?"},
            {"es": "Reúne en una ficha por espacio y por municipio lo que publican los demás proyectos: proyectos, fuego, suelo, agua, ríos y tendidos. Sin índices.",
             "fr": "Réunit dans une fiche par site et par commune ce que publient les autres projets : projets, feu, sol, eau, rivières et lignes. Sans indice."},
            ("ES", "FR")),
    Project("riesgo-tendidos-aves", {"es": "Riesgo de tendidos para aves", "fr": "Risque des lignes pour les oiseaux"}, "aves",
            {"es": "¿Qué aerogeneradores, apoyos eléctricos y tramos de línea ponen en más riesgo a las aves?",
             "fr": "Quelles éoliennes, quels pylônes et quels tronçons de ligne mettent le plus les oiseaux en danger ?"},
            {"es": "Cruza las líneas de OpenStreetMap y de las eléctricas con la presencia de aves (eBird, GBIF, Movebank) y el relieve, y ordena los elementos por riesgo de colisión y electrocución. Se actualiza cada mes.",
             "fr": "Croise les lignes d'OpenStreetMap et des gestionnaires de réseau avec la présence des oiseaux (eBird, GBIF, Movebank) et le relief, et classe les éléments par risque de collision et d'électrocution. Mis à jour chaque mois."},
            ("ES", "FR"), fig_tendidos, max_age_days=40),
    Project("sub-nocte", {"es": "Sub Nocte", "fr": "Sub Nocte"}, "aves",
            {"es": "¿Cuántas aves migrarán esta noche sobre cada ciudad, y cuándo conviene apagar las luces?",
             "fr": "Combien d'oiseaux migreront cette nuit au-dessus de chaque ville, et quand faut-il éteindre les lumières ?"},
            {"es": "Previsión a partir de los perfiles abiertos de los radares meteorológicos europeos (Aloft) y de la meteorología.",
             "fr": "Prévision à partir des profils ouverts des radars météorologiques européens (Aloft) et de la météo."},
            ("ES", "FR"), fig_subnocte),
    Project("quien-tiene-sombra", {"es": "¿Quién tiene sombra?", "fr": "Qui a de l'ombre ?"}, "ciudad",
            {"es": "¿Tienen los barrios con menos renta menos árboles y más calor?",
             "fr": "Les quartiers aux revenus modestes ont-ils moins d'arbres et plus de chaleur ?"},
            {"es": "Copa de los árboles y temperatura del suelo en verano (Landsat) por barrio, frente a la renta, en las grandes ciudades de España y Francia.",
             "fr": "Couvert arboré et température du sol en été (Landsat) par quartier, face au revenu, dans les grandes villes d'Espagne et de France."},
            ("ES", "FR"), max_age_days=400),
    Project("cuaderno-campo", {"es": "Cuaderno de campo", "fr": "Carnet de terrain"}, "campo",
            {"es": "Una libreta para apuntar observaciones en el campo, aunque no haya cobertura.",
             "fr": "Un carnet pour noter ses observations sur le terrain, même sans réseau."},
            {"es": "Aplicación web que funciona sin conexión. Es de uso personal y no publica ningún dato.",
             "fr": "Application web qui fonctionne hors ligne. Usage personnel ; elle ne publie aucune donnée."},
            (), max_age_days=400),
]
