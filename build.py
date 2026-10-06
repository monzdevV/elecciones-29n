#!/usr/bin/env python3
"""Genera el sitio estático Elecciones 29N en dist/.

Uso:  python build.py
Edita CONFIG antes de publicar (dominio, AdSense, datos del titular).
"""
import html
import json
import re
import shutil
import unicodedata
from datetime import date
from pathlib import Path

# ----------------------------------------------------------------------------
# CONFIG — rellena antes de publicar
# ----------------------------------------------------------------------------
CONFIG = {
    "site_url": "https://elecciones29n.es",       # sin barra final
    "site_name": "Elecciones 29N",
    "adsense_client": "",                          # p. ej. "ca-pub-1234567890123456" (vacío = sin anuncios)
    "owner_name": "[NOMBRE O RAZÓN SOCIAL DEL TITULAR]",
    "owner_nif": "[NIF]",
    "owner_address": "[DOMICILIO]",
    "contact_email": "[EMAIL DE CONTACTO]",
    # Votación simbólica (Supabase). La clave publicable es pública por diseño: solo permite votar y leer totales.
    "supabase_url": "https://gmzslroxejknsgcldmrx.supabase.co",
    "supabase_key": "sb_publishable_0Pwou436lxL-WPtxn1Hgnw_A2aZGahS",
}
ROOT = Path(__file__).parent
SRC, DATA, CONTENT, DIST = ROOT / "src", ROOT / "data", ROOT / "content", ROOT / "dist"
TODAY = date.today()
VER = TODAY.strftime("%Y%m%d")
MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
          "septiembre", "octubre", "noviembre", "diciembre"]
E = html.escape


def fdate(d):
    return f"{d.day} de {MONTHS[d.month - 1]} de {d.year}"


def fint(n):
    return f"{int(n):,}".replace(",", ".")


def fpct(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def url(path):
    return CONFIG["site_url"] + path


# ----------------------------------------------------------------------------
# Datos fijos verificados
# ----------------------------------------------------------------------------
TIMELINE = [
    ("2026-10-06", None, "martes 6 de octubre", "Se publica la convocatoria en el BOE y se abre la solicitud del voto por correo."),
    ("2026-10-12", "2026-10-19", "12–19 de octubre", "Consulta del censo electoral y plazo de reclamaciones."),
    ("2026-10-21", "2026-10-26", "21–26 de octubre", "Los partidos presentan sus candidaturas."),
    ("2026-10-31", "2026-11-04", "31 oct – 4 nov", "Los ayuntamientos sortean los miembros de las mesas electorales."),
    ("2026-11-02", None, "lunes 2 de noviembre", "Proclamación de las candidaturas."),
    ("2026-11-09", None, "lunes 9 de noviembre", "Correos empieza a entregar la documentación del voto por correo."),
    ("2026-11-13", None, "viernes 13 de noviembre", "Arranca la campaña electoral a las 00:00."),
    ("2026-11-19", None, "jueves 19 de noviembre", "Último día para solicitar el voto por correo."),
    ("2026-11-24", "2026-11-28", "24–28 de noviembre", "Prohibido publicar encuestas electorales (LOREG, art. 69)."),
    ("2026-11-25", None, "miércoles 25 de noviembre", "Último día para depositar el voto por correo en Correos."),
    ("2026-11-27", None, "viernes 27 de noviembre", "Termina la campaña a las 24:00."),
    ("2026-11-28", None, "sábado 28 de noviembre", "Jornada de reflexión."),
    ("2026-11-29", None, "domingo 29 de noviembre", "Votación de 9:00 a 20:00 y escrutinio en las mesas."),
    ("2026-12-04", None, "viernes 4 de diciembre", "Escrutinio general en las juntas electorales provinciales."),
]

# Posición en el cartograma (fila, columna), 1-based. Código = matrícula provincial histórica.
CARTO = {
    "a-coruna": (1, 1, "C"), "lugo": (1, 2, "LU"), "asturias": (1, 3, "O"), "cantabria": (1, 4, "S"),
    "vizcaya": (1, 5, "BI"), "guipuzcoa": (1, 6, "SS"),
    "pontevedra": (2, 1, "PO"), "ourense": (2, 2, "OR"), "leon": (2, 3, "LE"), "palencia": (2, 4, "P"),
    "burgos": (2, 5, "BU"), "alava": (2, 6, "VI"), "navarra": (2, 7, "NA"), "huesca": (2, 8, "HU"),
    "lleida": (2, 9, "L"), "girona": (2, 10, "GI"),
    "zamora": (3, 2, "ZA"), "valladolid": (3, 3, "VA"), "segovia": (3, 4, "SG"), "soria": (3, 5, "SO"),
    "la-rioja": (3, 6, "LO"), "zaragoza": (3, 7, "Z"), "tarragona": (3, 9, "T"), "barcelona": (3, 10, "B"),
    "salamanca": (4, 2, "SA"), "avila": (4, 3, "AV"), "madrid": (4, 4, "M"), "guadalajara": (4, 5, "GU"),
    "cuenca": (4, 6, "CU"), "teruel": (4, 7, "TE"), "castellon": (4, 8, "CS"), "baleares": (4, 10, "IB"),
    "caceres": (5, 2, "CC"), "toledo": (5, 3, "TO"), "ciudad-real": (5, 4, "CR"), "albacete": (5, 5, "AB"),
    "valencia": (5, 6, "V"),
    "badajoz": (6, 2, "BA"), "cordoba": (6, 3, "CO"), "jaen": (6, 4, "J"), "murcia": (6, 5, "MU"),
    "alicante": (6, 6, "A"),
    "huelva": (7, 1, "H"), "sevilla": (7, 2, "SE"), "malaga": (7, 3, "MA"), "granada": (7, 4, "GR"),
    "almeria": (7, 5, "AL"),
    "cadiz": (8, 2, "CA"), "santa-cruz-de-tenerife": (8, 8, "TF"), "las-palmas": (8, 9, "GC"),
    "ceuta": (9, 2, "CE"), "melilla": (9, 4, "ML"),
}
SLUG_ALIASES = {"illes-balears": "baleares", "islas-baleares": "baleares", "bizkaia": "vizcaya",
                "gipuzkoa": "guipuzcoa", "araba": "alava", "araba-alava": "alava", "lerida": "lleida",
                "gerona": "girona", "orense": "ourense", "la-coruna": "a-coruna", "castellon-de-la-plana": "castellon",
                "tenerife": "santa-cruz-de-tenerife", "gran-canaria": "las-palmas", "region-de-murcia": "murcia",
                "comunidad-de-madrid": "madrid", "principado-de-asturias": "asturias", "valencia-valencia": "valencia"}

SENADO = {
    "baleares": ("6 senadores: Mallorca 3, Menorca 1, Ibiza 1 y Formentera 1", 6),
    "las-palmas": ("5 senadores: Gran Canaria 3, Lanzarote 1 y Fuerteventura 1", 5),
    "santa-cruz-de-tenerife": ("6 senadores: Tenerife 3, La Palma 1, La Gomera 1 y El Hierro 1", 6),
    "ceuta": ("2 senadores", 2),
    "melilla": ("2 senadores", 2),
}

PARTY_SHORT = {"PP": "PP", "PSOE": "PSOE", "VOX": "Vox", "SUMAR": "Frente Amplio", "PODEMOS": "Podemos",
               "SALF": "SALF", "ERC": "ERC", "JUNTS": "Junts", "BILDU": "EH Bildu", "PNV": "PNV",
               "BNG": "BNG", "CC": "CC", "UPN": "UPN", "OTROS": "Otros"}
PARTY_2023_NAME = {"SUMAR": "Sumar"}
NEUTRAL_OTHERS = "#9aa1ab"
REGIONAL = {"ERC", "JUNTS", "BILDU", "PNV", "BNG", "CC", "UPN"}

# ----------------------------------------------------------------------------
# Carga de datos
# ----------------------------------------------------------------------------
def load_json(p):
    return json.loads(p.read_text(encoding="utf-8"))


PROV = load_json(DATA / "provincias.json")
TEST = load_json(DATA / "test.json") if (DATA / "test.json").exists() else None
PCOLORS = {k: v.get("color", NEUTRAL_OTHERS) for k, v in PROV["partidos"].items()}
PNAMES = {k: v.get("nombre", k) for k, v in PROV["partidos"].items()}
if TEST:
    for p in TEST["partidos"]:
        PCOLORS.setdefault(p["id"], p["color"])
        PNAMES.setdefault(p["id"], p["nombre"])
PCOLORS["OTROS"] = NEUTRAL_OTHERS

for p in PROV["provincias"]:
    s = SLUG_ALIASES.get(p["slug"], p["slug"])
    p["slug"] = s
    if s not in CARTO:
        raise SystemExit(f"Provincia sin posición en el cartograma: {s}")
    p["seats"] = p.get("escanos2026") or p["escanos2023"]
    p["res"] = sorted([r for r in p["resultados"] if r["partido"] != "OTROS"], key=lambda r: -r["votos"])
    p["otros_votos"] = sum(r["votos"] for r in p["resultados"] if r["partido"] == "OTROS")
PROVS = sorted(PROV["provincias"], key=lambda p: slugify(p["nombre"]))
BY_SLUG = {p["slug"]: p for p in PROVS}
assert len(PROVS) == 52, len(PROVS)
TOTAL_2026 = sum(p["seats"] for p in PROVS)
assert TOTAL_2026 == 350, TOTAL_2026


def short(pid):
    return PARTY_SHORT.get(pid, pid)


def color(pid):
    return PCOLORS.get(pid, NEUTRAL_OTHERS)


def seat_q(n):
    return 0 if n <= 2 else 1 if n == 3 else 2 if n == 4 else 3 if n <= 6 else 4 if n <= 11 else 5


def senators(slug):
    return SENADO.get(slug, ("4 senadores", 4))


def senate_marks(slug):
    if slug in ("ceuta", "melilla"):
        return "una cruz (de los 2 senadores)"
    if slug in ("baleares", "las-palmas", "santa-cruz-de-tenerife"):
        return "hasta 2 cruces en las islas que eligen 3 senadores y 1 en las que eligen uno"
    return "hasta 3 de las 4 plazas"


# ----------------------------------------------------------------------------
# D'Hondt (servidor) para contenido único por provincia
# ----------------------------------------------------------------------------
def dhondt_table(prov):
    valid = prov["validos"]
    elig = [r for r in prov["res"] if r["votos"] >= valid * 0.03]
    quots = []
    for r in elig:
        for d in range(1, prov["escanos2023"] + 2):
            quots.append((r["votos"] / d, r["partido"], d))
    quots.sort(key=lambda x: -x[0])
    n = prov["escanos2023"]
    won = quots[:n]
    last = won[-1] if won else None
    nxt = quots[n] if len(quots) > n else None
    return elig, won, last, nxt


# ----------------------------------------------------------------------------
# Plantilla
# ----------------------------------------------------------------------------
CUR = ' aria-current="page"'
VOTE_CLS = ' class="nav__vote"'
NAV = [("/mesa-electoral/", "Mesa electoral"), ("/voto-por-correo/", "Voto por correo"),
       ("/calendario-electoral/", "Calendario"), ("/simulador-escanos/", "Simulador"),
       ("/test-a-quien-voto/", "Test"), ("/provincias/", "Provincias"), ("/votacion/", "Vota")]

BRAND_SVG = """<svg class="brand__mark" viewBox="0 0 32 32" aria-hidden="true"><rect x="1.5" y="9.5" width="29" height="21" fill="none" stroke="currentColor" stroke-width="2"/><path d="M9 9.5h14" stroke="var(--paper)" stroke-width="3"/><path d="M8.5 9.5h15" stroke="currentColor" stroke-width="2" stroke-dasharray="0"/><rect x="10" y="2" width="12" height="12" fill="var(--sepia)" transform="rotate(-6 16 8)"/><path d="M6 23h20" stroke="currentColor" stroke-width="1"/></svg>"""


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"


def breadcrumbs(items):
    """items: [(nombre, path)] sin incluir Inicio."""
    full = [("Inicio", "/")] + items
    vis = "".join(
        f'<li><a href="{p}">{E(n)}</a></li>' if i < len(full) - 1 else f'<li aria-current="page">{E(n)}</li>'
        for i, (n, p) in enumerate(full))
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(full)]}
    return f'<nav class="crumbs wrap" aria-label="Migas de pan"><ol>{vis}</ol></nav>', ld


def ad(kind="", label="Publicidad"):
    cls = "ad" + (f" ad--{kind}" if kind else "")
    if CONFIG["adsense_client"]:
        return (f'<div class="{cls} is-live"><ins class="adsbygoogle" style="display:block" data-ad-client="{CONFIG["adsense_client"]}" '
                f'data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>')
    return f'<div class="{cls}" aria-hidden="true"><!-- PEGA AQUÍ TU BLOQUE DE ADSENSE -->{label}</div>'


EVENT_LD = {
    "@context": "https://schema.org", "@type": "Event",
    "name": "Elecciones generales de España 2026",
    "description": "Elecciones al Congreso de los Diputados (350 escaños) y al Senado convocadas por Real Decreto publicado en el BOE el 6 de octubre de 2026.",
    "startDate": "2026-11-29T09:00:00+01:00", "endDate": "2026-11-29T20:00:00+01:00",
    "eventStatus": "https://schema.org/EventScheduled",
    "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
    "location": {"@type": "Place", "name": "Colegios electorales de España", "address": {"@type": "PostalAddress", "addressCountry": "ES"}},
    "organizer": {"@type": "GovernmentOrganization", "name": "Junta Electoral Central", "url": "https://www.juntaelectoralcentral.es"},
}


def page(path, title, description, body, *, ld=None, active=None, og_type="article", extra_head="", scripts=()):
    canonical = url(path)
    lds = "".join(jsonld(x) for x in (ld or []))
    nav = "".join(
        f'<a href="{p}"{CUR if active == p else ""}{VOTE_CLS if p == "/votacion/" else ""}>{E(n)}</a>' for p, n in NAV)
    drawer = "".join(f'<li><a href="{p}">{E(n)}</a></li>' for p, n in NAV + [("/como-votar/", "Cómo votar"), ("/ley-dhondt/", "Ley D'Hondt"), ("/voto-extranjero/", "Voto exterior")])
    adsense = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={CONFIG["adsense_client"]}" crossorigin="anonymous"></script>'
               if CONFIG["adsense_client"] else "<!-- AdSense: rellena CONFIG['adsense_client'] en build.py. Activa el mensaje de consentimiento (CMP) de Google en AdSense > Privacidad y mensajes. -->")
    js = "".join(f'<script src="/assets/js/{s}?v={VER}" defer></script>' for s in ("site.js",) + tuple(scripts))
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{E(CONFIG['site_name'])}">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{url('/assets/og.png')}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1c2433">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="e29n-voto" content="{CONFIG['supabase_url']}|{CONFIG['supabase_key']}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=Source+Serif+4:opsz,wght@8..60,400..650&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v={VER}">
{adsense}
{extra_head}{lds}
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
<div class="folio"><div class="wrap"><span><b data-countdown>Domingo 29 de noviembre</b> · Elecciones generales · 9:00–20:00</span><span class="folio__right">Actualizado el {fdate(TODAY)}</span></div></div>
<header class="masthead">
  <div class="wrap">
    <a class="brand" href="/">{BRAND_SVG}<span class="brand__name">Elecciones <span>29N</span></span></a>
    <nav class="nav" aria-label="Principal">{nav}</nav>
    <button class="menu-btn" type="button" data-menu aria-expanded="false" aria-controls="drawer"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 4h12M2 8h12M2 12h12" stroke="currentColor" stroke-width="1.5"/></svg>Menú</button>
  </div>
  <div class="drawer" id="drawer" hidden><ul class="wrap">{drawer}</ul></div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <div>
      <p><strong>{E(CONFIG['site_name'])}</strong> es una guía ciudadana independiente sobre las elecciones generales del 29 de noviembre de 2026. No está vinculada a ningún partido ni a la Administración.</p>
      <p>Los datos oficiales proceden del BOE, la Junta Electoral Central, el Ministerio del Interior y el INE. Ante cualquier duda, prevalece la información oficial.</p>
      <p>Límites administrativos del mapa © Instituto Geográfico Nacional de España (CC BY 4.0).</p>
    </div>
    <div><h2>Guías</h2><ul><li><a href="/mesa-electoral/">Mesa electoral</a></li><li><a href="/voto-por-correo/">Voto por correo</a></li><li><a href="/como-votar/">Cómo votar</a></li><li><a href="/voto-extranjero/">Voto desde el extranjero</a></li><li><a href="/calendario-electoral/">Calendario electoral</a></li></ul></div>
    <div><h2>Herramientas</h2><ul><li><a href="/simulador-escanos/">Simulador de escaños</a></li><li><a href="/test-a-quien-voto/">Test: ¿a quién voto?</a></li><li><a href="/ley-dhondt/">Cómo funciona la ley D'Hondt</a></li><li><a href="/provincias/">Las 52 circunscripciones</a></li></ul></div>
    <div><h2>Legal</h2><ul><li><a href="/sobre-nosotros/">Quiénes somos</a></li><li><a href="/aviso-legal/">Aviso legal</a></li><li><a href="/privacidad/">Privacidad</a></li><li><a href="/cookies/">Cookies</a></li></ul></div>
  </div>
</footer>
{js}
</body>
</html>
"""


def write(path, content):
    out = DIST / path.lstrip("/")
    if path.endswith("/"):
        out = out / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(content.encode("utf-8").replace(b"\r\n", b"\n"))
    return out


SITEMAP = []


def add(path, html_, priority="0.7"):
    write(path, html_)
    SITEMAP.append((path, priority))


# ----------------------------------------------------------------------------
# Componentes
# ----------------------------------------------------------------------------
def cartogram(link=True):
    cells = []
    for p in PROVS:
        r, c, code = CARTO[p["slug"]]
        q = seat_q(p["seats"])
        label = f'{p["nombre"]}: {p["seats"]} diputados'
        cells.append(
            f'<a href="/provincias/{p["slug"]}/" style="grid-area:{r}/{c}" data-q="{q}" title="{E(label)}" aria-label="{E(label)}">'
            f'<span class="c">{code}</span><span class="n">{p["seats"]}</span></a>')
    legend = "".join(
        f'<span class="legend"><i style="background:var(--seq-{q})"></i>{lab}</span>'
        for q, lab in [(0, "1–2"), (1, "3"), (2, "4"), (3, "5–6"), (4, "7–11"), (5, "12+")])
    return f"""<figure class="plate" style="margin:0">
  <div class="plate__head"><span class="plate__title">Diputados que elige cada circunscripción</span><span class="plate__no">350 escaños · 52 circunscripciones</span></div>
  <div class="plate__body"><div class="carto" role="list" aria-label="Mapa de provincias">{''.join(cells)}<div aria-hidden="true" style="grid-area:8/8/9/10;border:1px dashed var(--rule-strong);margin:-3px;pointer-events:none"></div></div></div>
  <figcaption class="plate__foot"><span style="display:flex;flex-wrap:wrap;gap:.35rem .8rem">{legend}</span><span>Toca una provincia · Códigos de matrícula</span></figcaption>
</figure>"""


def faq_block(pairs, title="Preguntas frecuentes"):
    items = "".join(f"<details><summary>{E(q)}</summary><div>{a}</div></details>" for q, a in pairs)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a).strip()}}
        for q, a in pairs]}
    return f'<section class="faq" id="preguntas-frecuentes"><h2>{E(title)}</h2>{items}</section>', ld


def answer_box(text, extra=""):
    ex = f"<p>{extra}</p>" if extra else ""
    return f'<div class="answer"><span class="answer__label">Respuesta rápida</span><p>{text}</p>{ex}</div>'


def bars(rows, max_pct=None):
    mx = max_pct or max((r["pct"] for r in rows), default=1)
    out = []
    for r in rows:
        w = r["pct"] / mx * 100
        out.append(f'<div class="bar"><span class="p">{E(short(r["partido"]) if r["partido"] in PARTY_SHORT else r.get("nombre_lista", r["partido"]))}</span>'
                   f'<div class="bar__track"><div class="bar__fill" style="width:{w:.1f}%;background:{color(r["partido"])}"></div></div>'
                   f'<span class="v">{fpct(r["pct"])} %</span><span class="s">{r.get("escanos", 0)}</span></div>')
    return '<div class="bars">' + "".join(out) + "</div>"


def label_2023(pid):
    return PARTY_2023_NAME.get(pid, short(pid))


# ----------------------------------------------------------------------------
# Guías (contenido redactado en content/*.html)
# ----------------------------------------------------------------------------
GUIDES = [
    ("mesa-electoral", "Mesa electoral", "Cuánto se cobra, excusas válidas y qué pasa si no vas"),
    ("voto-por-correo", "Voto por correo", "Plazos, cómo pedirlo y dónde entregarlo"),
    ("calendario-electoral", "Calendario electoral", "Todas las fechas, del BOE al 29 de noviembre"),
    ("como-votar", "Cómo votar el 29N", "Documentos, horarios, papeletas y colegio electoral"),
    ("voto-extranjero", "Votar desde el extranjero", "CERA, ERTA, plazos y consulados"),
    ("ley-dhondt", "Cómo funciona la ley D'Hondt", "Por qué no todos los votos valen igual"),
]


def parse_fragment(text):
    meta = {}
    m = re.match(r"\s*<!--(.*?)-->", text, re.S)
    if m:
        for line in m.group(1).strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip().lower()] = v.strip()
        text = text[m.end():]
    return meta, text.strip()


def split_sections(body):
    """Devuelve (cuerpo, faq_pairs, fuentes_html)."""
    faq_pairs, sources = [], ""
    m = re.search(r"<h2[^>]*>\s*Fuentes(?: oficiales)?\s*</h2>(.*)$", body, re.S | re.I)
    if m:
        sources = m.group(1).strip()
        body = body[:m.start()]
    m = re.search(r"<h2[^>]*>\s*Preguntas frecuentes\s*</h2>(.*?)(?=<h2|$)", body, re.S | re.I)
    if m:
        chunk = m.group(1)
        for qm in re.finditer(r"<h3[^>]*>(.*?)</h3>(.*?)(?=<h3|$)", chunk, re.S):
            q = re.sub(r"<[^>]+>", "", qm.group(1)).strip()
            faq_pairs.append((html.unescape(q), qm.group(2).strip()))
        body = body[:m.start()] + body[m.end():]
    return body.strip(), faq_pairs, sources


def add_ids(body):
    toc = []
    used = set()

    def rep(m):
        txt = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        sid = slugify(html.unescape(txt))[:60] or "seccion"
        while sid in used:
            sid += "-2"
        used.add(sid)
        toc.append((sid, html.unescape(txt)))
        return f'<h2 id="{sid}"{m.group(1)}>{m.group(2)}</h2>'

    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", rep, body, flags=re.S)
    return body, toc


def inject_mid_ad(body):
    idx = [m.start() for m in re.finditer(r"<h2", body)]
    if len(idx) >= 3:
        return body[:idx[2]] + ad() + body[idx[2]:]
    return body


def guide_page(slug, name, sub):
    f = CONTENT / f"{slug}.html"
    if not f.exists():
        print(f"  ! falta content/{slug}.html — se omite")
        return None
    meta, body = parse_fragment(f.read_text(encoding="utf-8"))
    body, faq_pairs, sources = split_sections(body)
    body, toc = add_ids(body)
    body = inject_mid_ad(body)
    path = f"/{slug}/"
    crumbs, bc_ld = breadcrumbs([(name, path)])
    h1 = meta.get("h1", name)
    title = meta.get("title", f"{name} 2026")
    desc = meta.get("description", sub)
    answer = meta.get("answer", "")
    faq_html, faq_ld = faq_block(faq_pairs) if faq_pairs else ("", None)
    toc_html = "".join(f'<li><a href="#{i}">{E(t)}</a></li>' for i, t in toc)
    if faq_pairs:
        toc_html += '<li><a href="#preguntas-frecuentes">Preguntas frecuentes</a></li>'
    src_html = f'<aside class="sources" aria-label="Fuentes"><h2>Fuentes oficiales</h2>{sources}</aside>' if sources else ""
    related = "".join(f'<a href="/{s}/"><b>{E(n)}</b><span>{E(d)}</span></a>' for s, n, d in GUIDES if s != slug)
    article_ld = {"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc,
                  "inLanguage": "es-ES", "datePublished": "2026-10-05", "dateModified": TODAY.isoformat(),
                  "mainEntityOfPage": url(path), "author": {"@type": "Organization", "name": CONFIG["site_name"], "url": url("/")},
                  "publisher": {"@type": "Organization", "name": CONFIG["site_name"], "url": url("/")},
                  "about": {"@type": "Event", "name": "Elecciones generales de España 2026", "startDate": "2026-11-29"}}
    content = f"""{crumbs}
<div class="wrap">
  <header class="pagehead">
    <h1>{E(h1)}</h1>
    <p class="updated">Actualizado el <time datetime="{TODAY.isoformat()}">{fdate(TODAY)}</time> · Fuentes oficiales al final</p>
  </header>
  {answer_box(E(answer)) if answer else ""}
  {ad("wide")}
  <div class="layout">
    <div>
      <article class="prose">{body}</article>
      {faq_html}
      {src_html}
    </div>
    <aside class="rail"><div class="rail__sticky"><nav class="toc" aria-label="En esta página"><h2>En esta página</h2><ol>{toc_html}</ol></nav>{ad("rail")}</div></aside>
  </div>
</div>
<section class="section wrap"><h2>Sigue con estas guías</h2><div class="index">{related}</div></section>"""
    lds = [bc_ld, article_ld] + ([faq_ld] if faq_ld else []) + ([EVENT_LD] if slug == "calendario-electoral" else [])
    add(path, page(path, title, desc, content, ld=lds, active=path if path in dict(NAV) else None), "0.9")
    return {"slug": slug, "name": name, "title": title, "desc": desc, "answer": answer}


# ----------------------------------------------------------------------------
# Datos para el simulador
# ----------------------------------------------------------------------------
def national_2023():
    tot_valid = sum(p["validos"] for p in PROVS)
    tot_blank = sum(p["blanco"] for p in PROVS)
    votes, seats = {}, {}
    for p in PROVS:
        for r in p["resultados"]:
            votes[r["partido"]] = votes.get(r["partido"], 0) + r["votos"]
            seats[r["partido"]] = seats.get(r["partido"], 0) + r.get("escanos", 0)
    pct = {k: v / tot_valid * 100 for k, v in votes.items()}
    return pct, seats, tot_blank / tot_valid * 100


NAT_PCT, NAT_SEATS, NAT_BLANK = national_2023()


def sim_national_data():
    order = ["PP", "PSOE", "VOX", "SUMAR", "PODEMOS", "SALF", "ERC", "JUNTS", "BILDU", "PNV", "BNG", "CC", "UPN", "OTROS"]
    parties = []
    for pid in order:
        base = round(NAT_PCT.get(pid, 0.0), 1)
        if pid not in NAT_PCT and pid not in ("PODEMOS", "SALF"):
            continue
        name = {"SUMAR": "Sumar en 2023", "PODEMOS": "En 2023 iba dentro de Sumar", "SALF": "No se presentó en 2023",
                "OTROS": "Resto de candidaturas"}.get(pid, PNAMES.get(pid, pid))
        parties.append({"id": pid, "short": short(pid), "name": name, "color": color(pid), "base": base,
                        "regional": pid in REGIONAL, "ref": NAT_SEATS.get(pid) if pid not in ("OTROS",) else None,
                        "max": 50 if pid not in REGIONAL else 10})
    provs = []
    for p in PROVS:
        shares = {}
        for r in p["resultados"]:
            shares[r["partido"]] = round(r["votos"] / p["validos"] * 100, 3)
        provs.append({"slug": p["slug"], "seats": p["seats"], "blank": round(p["blanco"] / p["validos"] * 100, 3), "shares": shares})
    return {"mode": "national", "parties": parties, "provinces": provs, "blankNat": round(NAT_BLANK, 2)}


def sim_province_data(p):
    parties = []
    for r in p["res"]:
        pct = r["votos"] / p["validos"] * 100
        if pct < 0.5 and not r.get("escanos"):
            continue
        parties.append({"id": r["partido"], "short": short(r["partido"]) if r["partido"] in PARTY_SHORT else r.get("nombre_lista", r["partido"]),
                        "name": PARTY_2023_NAME.get(r["partido"], ""), "color": color(r["partido"]),
                        "base": round(pct, 1), "ref": r.get("escanos", 0), "max": 60})
    listed = {x["id"] for x in parties}
    rest = sum(r["votos"] for r in p["resultados"] if r["partido"] not in listed)
    parties.append({"id": "OTROS", "short": "Otros", "name": "Resto de candidaturas", "color": NEUTRAL_OTHERS,
                    "base": round(rest / p["validos"] * 100, 1), "ref": None, "max": 30})
    return {"mode": "province", "parties": parties, "seats": p["seats"], "blank": round(p["blanco"] / p["validos"] * 100, 2)}


def sim_widget(data, title, note):
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f"""<div class="tool" data-sim>
  <script type="application/json">{payload}</script>
  <div class="tool__bar"><strong>{E(title)}</strong><button class="btn btn--ghost" type="button" data-reset style="min-height:2.25rem;padding:.3rem .8rem">Volver a 2023</button></div>
  <div class="tool__body tool__body--split">
    <div>
      <div class="field-grid" data-inputs></div>
      <p class="sumline" data-sum><span>Suma de candidaturas</span><b>0 %</b></p>
      <p class="tool-note" style="margin-top:.5rem">{note}</p>
    </div>
    <div>
      <svg class="hemi" role="img" aria-label="Hemiciclo con el reparto de escaños"></svg>
      <ul class="seatlist" data-seatlist aria-live="polite"></ul>
      <p class="majority" data-majority></p>
    </div>
  </div>
</div>"""



# ----------------------------------------------------------------------------
# Mapa interactivo y votación simbólica (v2)
# ----------------------------------------------------------------------------
GEO = load_json(DATA / "mapa.json")
assert set(GEO["paths"]) == set(BY_SLUG), "mapa.json y provincias.json no coinciden"
VOTE_PARTIES = ["PP", "PSOE", "VOX", "SUMAR", "PODEMOS", "SALF", "ERC", "JUNTS", "BILDU", "PNV", "BNG", "CC", "UPN", "OTRO", "BLANCO"]
VOTE_NAMES = dict(PARTY_SHORT, OTRO="Otro partido", BLANCO="En blanco")
VOTE_COLORS = {k: color(k) for k in VOTE_PARTIES}
VOTE_COLORS.update({"OTRO": NEUTRAL_OTHERS, "BLANCO": "#e8e8e8"})


def mini_data():
    out = []
    for p in PROVS:
        top = [[r["partido"], round(r["pct"], 1), color(r["partido"])] for r in p["res"][:3]]
        out.append({"slug": p["slug"], "n": p["nombre"], "s": p["seats"], "r": top})
    names = {k: short(k) if k in PARTY_SHORT else k for k in PCOLORS}
    names.update(VOTE_NAMES)
    names["SUMAR"] = "Sumar"
    colors = dict(PCOLORS)
    colors.update(VOTE_COLORS)
    return {"p": out, "names": names, "colors": colors}


MINI = mini_data()


def map_svg():
    x, y, w, h = GEO["canarias_box"]
    parts = [f'<svg class="map__svg" viewBox="{GEO["viewBox"]}" role="img" aria-label="Mapa de las 52 circunscripciones de España">',
             f'<rect class="map__inset" x="{x}" y="{y}" width="{w}" height="{h}"/>']
    for slug, d in GEO["paths"].items():
        parts.append(f'<a href="/provincias/{slug}/" data-slug="{slug}"><path d="{d}"/></a>')
    parts.append("</svg>")
    return "".join(parts)


def map_widget(layer="ganador", inline=True, switcher=True, highlight=None, title="", extra_cls=""):
    seg = ""
    if switcher:
        btns = "".join(f'<button type="button" data-l="{k}" aria-pressed="{str(k == layer).lower()}">{E(v)}</button>'
                       for k, v in [("ganador", "Ganador 2023"), ("escanos", "Escaños 2026"), ("lectores", "Votación lectores")])
        seg = f'<div class="seg" role="group" aria-label="Qué muestra el mapa" data-layers>{btns}</div>'
    bar = f'<div class="map__bar"><strong>{E(title)}</strong>{seg}</div>' if (title or seg) else ""
    payload = ""
    svg = ""
    if inline:
        payload = '<script type="application/json">' + json.dumps(MINI, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"
        svg = map_svg()
    hl = f' data-highlight="{highlight}"' if highlight else ""
    legend = '<div class="map__legend" data-legend></div>' if layer != "locator" else ""
    return (f'<div class="map {extra_cls}" data-map data-layer="{layer}"{hl}>{payload}{bar}'
            f'<div class="map__canvas">{svg}<div class="map__tip" role="status"></div></div>{legend}</div>')


def vote_widget(province=None, autoload=False):
    chips = "".join(
        f'<label class="chip"><input type="radio" name="partido" value="{k}"><span><i style="background:{VOTE_COLORS[k]}"></i>{E(VOTE_NAMES[k])}</span></label>'
        for k in VOTE_PARTIES)
    opts = '<option value="">Elige tu provincia</option>' + "".join(
        f'<option value="{p["slug"]}">{E(p["nombre"])}</option>' for p in PROVS)
    payload = json.dumps({"names": VOTE_NAMES, "colors": VOTE_COLORS}, ensure_ascii=False, separators=(",", ":"))
    attrs = (f' data-province="{province}"' if province else "") + (" data-autoload" if autoload else "")
    return f"""<div class="voto" data-voto data-state="idle"{attrs}>
  <script type="application/json">{payload}</script>
  <div class="voto__head"><strong>Votación simbólica de los lectores</strong><span>No es una encuesta · un voto por dispositivo</span></div>
  <div class="voto__body">
    <form novalidate>
      <fieldset><legend>Si las elecciones fueran hoy, ¿a quién votarías?</legend><div class="chips">{chips}</div></fieldset>
      <div class="voto__row">
        <label>Tu provincia<select name="provincia">{opts}</select></label>
        <button class="btn" type="submit" data-submit>Votar</button>
      </div>
      <p class="voto__msg" data-msg aria-live="polite"></p>
      <p class="voto__mine" data-mine></p>
      <p class="voto__note">Solo se guarda el partido y la provincia, sin datos personales. Puedes cambiar tu voto cuando quieras.</p>
    </form>
    <div class="voto__res" data-results hidden aria-live="polite">
      <h3>Así va la votación</h3>
      <div class="vbars" data-bars></div>
      <p class="voto__total" data-total></p>
      <div class="share" data-share hidden><a href="#" data-net="wa" target="_blank" rel="noopener">Compartir en WhatsApp</a><a href="#" data-net="x" target="_blank" rel="noopener">Compartir en X</a><a href="#" data-net="copy">Copiar enlace</a></div>
    </div>
  </div>
</div>"""


def build_home2():
    faq_pairs = []
    fg = CONTENT / "faq-general.json"
    if fg.exists():
        faq_pairs = [(x["q"], E(x["a"])) for x in load_json(fg)]
    faq_html, faq_ld = faq_block(faq_pairs, "Lo que más se pregunta sobre el 29N") if faq_pairs else ("", None)
    guides = "".join(f'<a href="/{s}/"><b>{E(n)}</b><span>{E(d)}</span></a>' for s, n, d in GUIDES)
    tl = "".join(
        f'<li data-date="{d}"' + (f' data-end="{e}"' if e else "") + f'><time datetime="{d}">{E(lbl)}</time><span>{E(t)}</span></li>'
        for d, e, lbl, t in TIMELINE)
    by_cc = {}
    for p in PROVS:
        by_cc.setdefault(p["ccaa"], []).append(p)
    prov_list = "".join(
        f'<h3>{E(cc)}</h3>' + "".join(f'<a href="/provincias/{p["slug"]}/">{E(p["nombre"])} <span>{p["seats"]}</span></a>' for p in ps)
        for cc, ps in sorted(by_cc.items(), key=lambda x: slugify(x[0])))
    site_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": CONFIG["site_name"], "url": url("/"),
               "inLanguage": "es-ES", "description": "Guía ciudadana independiente de las elecciones generales del 29 de noviembre de 2026."}
    body = f"""<section class="night">
  <div class="wrap hero2">
    <div>
      <h1>Elecciones generales del <em>29 de noviembre</em></h1>
      <p class="dek">Mesa electoral, voto por correo, plazos y el reparto de escaños de cada provincia. Toca el mapa para ver la tuya.</p>
      <div class="cd" data-cd aria-label="Cuenta atrás hasta la apertura de los colegios">
        <div class="cd__u"><span class="cd__n" data-cd-d>--</span><span class="cd__l">días</span></div>
        <div class="cd__u"><span class="cd__n" data-cd-h>--</span><span class="cd__l">horas</span></div>
        <div class="cd__u"><span class="cd__n" data-cd-m>--</span><span class="cd__l">minutos</span></div>
      </div>
      <div class="hero-actions">
        <a class="btn" href="/votacion/">Vota en la votación simbólica</a>
        <a class="btn btn--ghost" href="/simulador-escanos/">Simular el reparto</a>
      </div>
    </div>
    <div>{map_widget("ganador", title="Las 52 circunscripciones")}<p class="map__credit">Límites © Instituto Geográfico Nacional · Resultados 2023: Ministerio del Interior</p></div>
  </div>
</section>
<div class="wrap">
  <dl class="keyfacts" style="margin-top:2rem;grid-template-columns:repeat(auto-fit,minmax(9rem,1fr))">
    <div><dt>Votación</dt><dd>Dom. 29 nov</dd></div>
    <div><dt>Colegios</dt><dd>9:00 – 20:00</dd></div>
    <div><dt>Congreso</dt><dd>350 escaños</dd></div>
    <div><dt>Mayoría absoluta</dt><dd>176</dd></div>
  </dl>
  {ad("wide")}
  <section class="vote-band"><h2>Y tú, ¿a quién votarías?</h2><p>Participa en la votación simbólica de los lectores. El resultado por partido se desvela la noche electoral, cuando cierren los colegios.</p>{vote_widget(autoload=True)}</section>
  <section class="section"><h2>Las dudas que más se buscan estos días</h2><div class="index">{guides}<a href="/test-a-quien-voto/"><b>Test: ¿a quién voto?</b><span>24 preguntas para ver tu afinidad con cada partido</span></a><a href="/simulador-escanos/"><b>Simulador de escaños</b><span>Prueba porcentajes y mira el hemiciclo resultante</span></a></div></section>
  <section class="section"><h2>Calendario: lo próximo que pasa</h2><ol class="timeline">{tl}</ol><p style="margin-top:1rem;font-family:var(--f-ui);font-size:.9rem"><a href="/calendario-electoral/">Ver el calendario completo</a></p></section>
  <section class="section"><h2>Tu provincia: escaños, resultados de 2023 y simulador</h2><div class="provgrid">{prov_list}</div></section>
  {faq_html}
  <div style="height:var(--s-8)"></div>
</div>"""
    title = "Elecciones generales 29 de noviembre de 2026: guía y simulador"
    desc = "Elecciones generales 29N 2026: mapa por provincias, mesa electoral, voto por correo, calendario, simulador D'Hondt, test y votación simbólica."
    lds = [site_ld, EVENT_LD] + ([faq_ld] if faq_ld else [])
    add("/", page("/", title, desc, body, ld=lds, og_type="website", scripts=("mapa.js", "voto.js")), "1.0")


def build_votacion():
    path = "/votacion/"
    crumbs, bc = breadcrumbs([("Votación simbólica", path)])
    pairs = [
        ("¿Es una encuesta?", "No. Es una votación simbólica abierta a quien visita la web, sin muestra representativa ni valor estadístico. Sirve para participar y comparar con el resultado real."),
        ("¿Cuándo se ven los resultados por partido?", "El domingo 29 de noviembre de 2026 a las 21:00 (hora peninsular), cuando cierran los últimos colegios en Canarias. Hasta entonces solo mostramos cuántas personas han votado en cada provincia."),
        ("¿Por qué no se enseñan antes?", "La Ley Orgánica del Régimen Electoral General (art. 69) regula la difusión de sondeos y la prohíbe los cinco días anteriores a la votación. La Junta Electoral Central considera sondeo cualquier estudio de intención de voto, se llame como se llame, así que no mostramos reparto por partido hasta que cierren las urnas."),
        ("¿Qué datos guardáis?", "Solo el partido, la provincia y la fecha. No guardamos tu IP ni datos personales. Tu navegador conserva un identificador aleatorio para que puedas cambiar tu voto sin duplicarlo."),
        ("¿Puedo cambiar mi voto?", "Sí, cuantas veces quieras desde el mismo dispositivo. Cuenta solo el último."),
    ]
    faq_html, faq_ld = faq_block(pairs)
    body = f"""{crumbs}
<div class="wrap">
  <header class="pagehead">
    <h1>Votación simbólica: ¿a quién votarías el 29N?</h1>
    <p class="dek">Vota en un clic y comparte. El resultado por partido de los lectores se desvela la noche electoral, a las 21:00.</p>
  </header>
  {vote_widget(autoload=True)}
  {ad("wide")}
  <div class="layout"><div>
    <section style="margin-bottom:2rem">{map_widget("lectores", inline=False, title="Participación por provincia")}</section>
    {faq_html}
  </div><aside class="rail"><div class="rail__sticky">{ad("rail")}</div></aside></div>
</div>"""
    add(path, page(path, "Votación simbólica elecciones 29N 2026: ¿a quién votarías?",
                   "Vota en la votación simbólica de las elecciones generales del 29 de noviembre de 2026 y descubre el resultado de los lectores la noche electoral.",
                   body, ld=[bc, faq_ld], active=path, scripts=("mapa.js", "voto.js")), "0.9")

# ----------------------------------------------------------------------------
# Páginas
# ----------------------------------------------------------------------------
def build_home(guides_meta):
    faq_pairs = []
    fg = CONTENT / "faq-general.json"
    if fg.exists():
        faq_pairs = [(x["q"], E(x["a"])) for x in load_json(fg)]
    faq_html, faq_ld = faq_block(faq_pairs, "Lo que más se pregunta sobre el 29N") if faq_pairs else ("", None)
    guides = "".join(f'<a href="/{s}/"><b>{E(n)}</b><span>{E(d)}</span></a>' for s, n, d in GUIDES)
    tl = "".join(
        f'<li data-date="{d}"{f" data-end={chr(34)}{e}{chr(34)}" if e else ""}><time datetime="{d}">{E(lbl)}</time><span>{E(t)}</span></li>'
        for d, e, lbl, t in TIMELINE)
    # Provincias por comunidad
    by_cc = {}
    for p in PROVS:
        by_cc.setdefault(p["ccaa"], []).append(p)
    prov_list = "".join(
        f'<h3>{E(cc)}</h3>' + "".join(f'<a href="/provincias/{p["slug"]}/">{E(p["nombre"])} <span>{p["seats"]}</span></a>' for p in ps)
        for cc, ps in sorted(by_cc.items(), key=lambda x: slugify(x[0])))
    site_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": CONFIG["site_name"], "url": url("/"),
               "inLanguage": "es-ES", "description": "Guía ciudadana independiente de las elecciones generales del 29 de noviembre de 2026."}
    body = f"""<div class="wrap">
  <section class="home-hero">
    <div>
      <h1>Elecciones generales del <em>29 de noviembre</em> de 2026</h1>
      <p class="dek">Todo lo práctico para votar, en un solo sitio: mesa electoral, voto por correo, plazos, el reparto de escaños de tu provincia y un simulador para hacer tus propias cuentas.</p>
      <dl class="keyfacts">
        <div><dt>Votación</dt><dd>Dom. 29 nov</dd></div>
        <div><dt>Colegios</dt><dd>9:00 – 20:00</dd></div>
        <div><dt>Congreso</dt><dd>350 escaños</dd></div>
        <div><dt>Mayoría absoluta</dt><dd>176</dd></div>
      </dl>
      <div class="hero-actions">
        <a class="btn" href="/simulador-escanos/">Simular el reparto</a>
        <a class="btn btn--ghost" href="/mesa-electoral/">Me ha tocado mesa</a>
      </div>
    </div>
    {cartogram()}
  </section>
  {ad("wide")}
  <section class="section"><h2>Las dudas que más se buscan estos días</h2><div class="index">{guides}<a href="/test-a-quien-voto/"><b>Test: ¿a quién voto?</b><span>24 preguntas para ver tu afinidad con cada partido</span></a><a href="/simulador-escanos/"><b>Simulador de escaños</b><span>Prueba porcentajes y mira el hemiciclo resultante</span></a></div></section>
  <section class="section"><h2>Calendario: lo próximo que pasa</h2><ol class="timeline">{tl}</ol><p style="margin-top:1rem;font-family:var(--f-ui);font-size:.9rem"><a href="/calendario-electoral/">Ver el calendario completo</a></p></section>
  <section class="section"><h2>Tu provincia: escaños, resultados de 2023 y simulador</h2><div class="provgrid">{prov_list}</div></section>
  {faq_html}
  <div style="height:var(--s-8)"></div>
</div>"""
    title = "Elecciones generales 29 de noviembre de 2026: guía y simulador"
    desc = "Elecciones generales 29N 2026: mesa electoral, voto por correo, calendario, escaños por provincia, simulador D'Hondt y test de afinidad."
    lds = [site_ld, EVENT_LD] + ([faq_ld] if faq_ld else [])
    add("/", page("/", title, desc, body, ld=lds, og_type="website"), "1.0")


def build_simulator():
    path = "/simulador-escanos/"
    crumbs, bc = breadcrumbs([("Simulador de escaños", path)])
    note = ("Parte de los resultados de 2023 en cada provincia y los escala según el porcentaje nacional que indiques; "
            "Podemos y SALF se reparten de forma uniforme porque no tienen resultado propio en 2023. "
            "Aplica la ley D'Hondt en las 52 circunscripciones con el umbral del 3 % y el reparto de escaños de 2026. "
            "Es una herramienta de cálculo, no una encuesta.")
    pairs = [
        ("¿Cómo calcula los escaños este simulador?", "Reparte los 350 diputados provincia a provincia con la ley D'Hondt, igual que el sistema real. Para cada partido parte de su porcentaje de 2023 en cada provincia y lo multiplica por la variación nacional que tú indicas."),
        ("¿Por qué el resultado no es una predicción?", "Porque los porcentajes los pones tú. El simulador solo hace las cuentas del reparto; no incluye encuestas ni estimaciones propias."),
        ("¿Qué es el umbral del 3 %?", "En cada provincia, las candidaturas que no superan el 3 % de los votos válidos (incluido el voto en blanco) no entran en el reparto de escaños (LOREG, art. 163)."),
        ("¿Cuántos escaños hacen falta para gobernar?", "La mayoría absoluta del Congreso es de 176 diputados. En la primera votación de investidura hace falta mayoría absoluta; en la segunda basta con más síes que noes."),
        ("¿Por qué un partido con más votos puede sacar menos escaños?", "Porque el reparto se hace por provincias. Los votos concentrados en provincias donde un partido supera el umbral rinden más que los dispersos por todo el país."),
    ]
    faq_html, faq_ld = faq_block(pairs)
    app_ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Simulador de escaños elecciones generales 2026",
              "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "inLanguage": "es-ES", "url": url(path),
              "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}}
    body = f"""{crumbs}
<div class="wrap">
  <header class="pagehead">
    <h1>Simulador de escaños para las elecciones generales de 2026</h1>
    <p class="dek">Cambia el porcentaje de voto de cada partido y mira cómo quedaría el Congreso. Empieza con los resultados de 2023.</p>
  </header>
  {sim_widget(sim_national_data(), "Porcentaje de voto en toda España", note)}
  {ad("wide")}
  <div class="layout"><div>
  <article class="prose">
    <h2 id="como-se-calcula">Cómo se calcula el reparto</h2>
    <p>El Congreso tiene 350 diputados repartidos en 52 circunscripciones: cada provincia tiene dos escaños garantizados (Ceuta y Melilla, uno) y el resto se reparte según la población. Dentro de cada provincia, los escaños se asignan con la <a href="/ley-dhondt/">ley D'Hondt</a> entre las candidaturas que superan el 3 % de los votos válidos.</p>
    <p>Por eso el porcentaje nacional no se traduce directamente en escaños. Un partido muy concentrado territorialmente, como los nacionalistas, puede obtener representación con poco voto nacional. Un partido con voto disperso necesita superar el umbral y la barrera natural de cada provincia; en las que eligen tres o cuatro diputados, esa barrera ronda el 15–20 %.</p>
    <h2 id="limitaciones">Lo que este simulador no hace</h2>
    <p>Supone que cada partido sube o baja en la misma proporción en todas las provincias, cosa que nunca pasa del todo. También da por fijo el voto en blanco de 2023. Si quieres afinar una provincia concreta, usa el simulador de su página: allí puedes escribir el porcentaje exacto de cada candidatura.</p>
  </article>
  {faq_html}
  </div><aside class="rail"><div class="rail__sticky">{ad("rail")}</div></aside></div>
</div>"""
    add(path, page(path, "Simulador de escaños elecciones generales 2026 (D'Hondt)",
                   "Calcula cuántos diputados sacaría cada partido el 29N. Simulador D'Hondt de las 52 provincias con el umbral del 3 % y el hemiciclo en vivo.",
                   body, ld=[bc, app_ld, faq_ld], active=path, scripts=("sim.js",)), "0.9")


def build_test():
    if not TEST:
        return
    path = "/test-a-quien-voto/"
    crumbs, bc = breadcrumbs([("Test: ¿a quién voto?", path)])
    parties = [dict(p, nombre_corto=short(p["id"])) for p in TEST["partidos"]]
    payload = json.dumps({"partidos": parties, "preguntas": [{"tema": q["tema"], "texto": q["texto"], "posiciones": q["posiciones"]} for q in TEST["preguntas"]]},
                         ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    n = len(TEST["preguntas"])
    rows = []
    for q in TEST["preguntas"]:
        cells = "".join(
            f'<td class="r">{"+" if q["posiciones"][p["id"]] > 0 else ""}{q["posiciones"][p["id"]]}{"*" if p["id"] in q.get("inciertos", []) else ""}</td>'
            for p in TEST["partidos"])
        src = " ".join(f'<a href="{E(u)}" rel="nofollow noopener" target="_blank">[{i + 1}]</a>' for i, u in enumerate(q.get("fuentes", [])))
        rows.append(f'<tr><td>{E(q["texto"])} <small>{src}</small></td>{cells}</tr>')
    head = "".join(f'<th class="r">{E(short(p["id"]))}</th>' for p in TEST["partidos"])
    pairs = [
        ("¿Qué partidos incluye el test?", "Los partidos de ámbito estatal con al menos un 2 % de media en las encuestas de septiembre de 2026: " + ", ".join(short(p['id']) for p in TEST['partidos']) + ". Los partidos que solo se presentan en una comunidad no aparecen porque sus programas no son comparables a escala nacional."),
        ("¿Cómo se asignan las posiciones de cada partido?", E(TEST["metodologia"])),
        ("¿Se guardan mis respuestas?", "No. El test funciona entero en tu navegador; no se envía ni se guarda ninguna respuesta."),
        ("¿Me dice a quién tengo que votar?", "No. Solo mide en cuántos temas coincides con cada partido. Hay asuntos que pesan más que otros para cada persona; léete los programas antes de decidir."),
    ]
    faq_html, faq_ld = faq_block(pairs)
    quiz_ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Test de afinidad política elecciones 2026",
               "applicationCategory": "EducationalApplication", "operatingSystem": "Web", "inLanguage": "es-ES", "url": url(path),
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}}
    body = f"""{crumbs}
<div class="wrap">
  <header class="pagehead">
    <h1>Test: ¿a quién voto en las elecciones generales de 2026?</h1>
    <p class="dek">{n} afirmaciones sobre vivienda, impuestos, inmigración, modelo territorial y otros temas. Al final verás cuánto coincides con cada partido.</p>
  </header>
  <div class="tool" data-quiz>
    <script type="application/json">{payload}</script>
    <div class="quiz__progress"><span data-progress></span></div>
    <div class="tool__body">
      <div class="quiz" data-stage>
        <p class="tool__bar" style="border:0;padding:0"><span class="quiz__topic" data-topic></span><span class="tool-note" data-count></span></p>
        <p class="quiz__q" data-q aria-live="polite"></p>
        <div class="scale" data-scale role="group" aria-label="Tu respuesta"></div>
        <div class="quiz__nav"><button class="btn btn--ghost" type="button" data-prev>Anterior</button><button class="btn btn--ghost" type="button" data-skip>Saltar pregunta</button></div>
      </div>
      <div data-result hidden tabindex="-1">
        <h2 style="font-size:1.5rem;margin-bottom:.4rem">Tu afinidad con cada partido</h2>
        <p class="tool-note" style="margin-bottom:1rem">Calculada sobre <span data-answered></span> respuestas. 100 % significa que coincides en todo.</p>
        <div class="result-list" data-reslist></div>
        <div class="quiz__nav" style="margin-top:1.25rem"><button class="btn" type="button" data-restart>Repetir el test</button><a class="btn btn--ghost" href="/simulador-escanos/">Ir al simulador de escaños</a></div>
      </div>
    </div>
  </div>
  <p class="tool-note" style="margin-top:.75rem">Tus respuestas no salen de tu dispositivo. Puedes responder con las teclas 1 a 5.</p>
  {ad("wide")}
  <div class="layout"><div>
    <article class="prose">
      <h2 id="metodologia">Metodología</h2>
      <p>{E(TEST["metodologia"])}</p>
      <p>Cada partido tiene una posición de −2 (muy en contra) a +2 (muy a favor) en cada afirmación. Tu afinidad es la distancia media entre tus respuestas y las suyas. Las marcadas con * son posiciones inciertas, a falta de programa electoral; se revisarán cuando se publiquen los programas de 2026.</p>
      <h2 id="posiciones">Posiciones de cada partido</h2>
      <div class="table-scroll"><table class="table"><thead><tr><th>Afirmación</th>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>
    </article>
    {faq_html}
  </div><aside class="rail"><div class="rail__sticky">{ad("rail")}</div></aside></div>
</div>"""
    add(path, page(path, "Test ¿a quién voto? Elecciones generales 2026",
                   f"Test de afinidad política para el 29N: {n} preguntas y tu porcentaje de coincidencia con PP, PSOE, Vox, Frente Amplio, Podemos y SALF.",
                   body, ld=[bc, quiz_ld, faq_ld], active=path, scripts=("test.js",)), "0.9")


def prov_en(p):
    return {"baleares": "en las Islas Baleares", "la-rioja": "en La Rioja", "las-palmas": "en Las Palmas"}.get(p["slug"], f"en {p['nombre']}")


def build_province(p, siblings):
    path = f"/provincias/{p['slug']}/"
    crumbs, bc = breadcrumbs([("Provincias", "/provincias/"), (p["nombre"], path)])
    en = prov_en(p)
    winner = p["res"][0]
    seat_parts = [r for r in p["res"] if r.get("escanos")]
    reparto = ", ".join(f'{label_2023(r["partido"])} {r["escanos"]}' for r in seat_parts)
    sen_txt, sen_n = senators(p["slug"])
    d26, d23 = p["seats"], p["escanos2023"]
    delta = d26 - d23
    delta_txt = ("los mismos que en 2023" if delta == 0 else
                 f"{'uno' if abs(delta) == 1 else abs(delta)} {'más' if delta > 0 else 'menos'} que en 2023, cuando eran {d23}, según el reparto por población de 2025 que debe confirmar el Real Decreto de convocatoria")
    dip = "diputado" if d26 == 1 else "diputados"
    answer = (f"{p['nombre']} elige <strong>{d26} {dip}</strong> al Congreso ({delta_txt}) y {sen_txt} al Senado "
              f"el domingo 29 de noviembre de 2026. En 2023 la candidatura más votada fue {E(label_2023(winner['partido']))} "
              f"con el {fpct(winner['pct'])} %, y el reparto quedó así: {E(reparto)}.")
    elig, won, last, nxt = dhondt_table(p)
    # Tabla de cocientes D'Hondt
    ncols = min(max(d23, 1), 8)
    qrows = []
    won_set = {(w[1], w[2]) for w in won}
    for r in elig:
        cells = []
        for d in range(1, ncols + 1):
            q = r["votos"] / d
            cls = ' style="font-weight:750;background:var(--sepia-wash)"' if (r["partido"], d) in won_set else ""
            cells.append(f'<td class="r"{cls}>{fint(round(q))}</td>')
        qrows.append(f'<tr><th scope="row">{E(label_2023(r["partido"]))}</th>{"".join(cells)}</tr>')
    qhead = "".join(f'<th class="r">÷{d}</th>' for d in range(1, ncols + 1))
    last_txt = ""
    if last and nxt:
        lp, np_ = last[1], nxt[1]
        need = int(last[0] * nxt[2] - next(r["votos"] for r in elig if r["partido"] == np_)) + 1
        last_txt = (f"<p>El último escaño de {E(p['nombre'])} fue para {E(label_2023(lp))}, con un cociente de {fint(round(last[0]))} votos. "
                    f"La siguiente candidatura en la cola era {E(label_2023(np_))}: le faltaron unos <strong>{fint(need)} votos</strong> para quitárselo.</p>")
    cost = last[0] / p["validos"] * 100 if last else 0
    hidden_more = "" if d23 <= 8 else f"<p class='tool-note'>La tabla muestra las ocho primeras divisiones; {E(p['nombre'])} reparte {d23} escaños.</p>"
    table_res = "".join(
        f'<tr><td>{E(r.get("nombre_lista") or label_2023(r["partido"]))}</td><td class="r">{fint(r["votos"])}</td><td class="r">{fpct(r["pct"])} %</td><td class="r">{r.get("escanos", 0)}</td></tr>'
        for r in p["res"])
    table_res += f'<tr><td>Votos en blanco</td><td class="r">{fint(p["blanco"])}</td><td class="r">{fpct(p["blanco"] / p["validos"] * 100)} %</td><td class="r">–</td></tr>'
    sib = "".join(f'<a href="/provincias/{s["slug"]}/">{E(s["nombre"])} <span>{s["seats"]}</span></a>' for s in siblings if s["slug"] != p["slug"])
    sib_html = f'<section class="section"><h2>Otras provincias de {E(p["ccaa"])}</h2><div class="provgrid">{sib}</div></section>' if sib else ""
    pairs = [
        (f"¿Cuántos diputados elige {p['nombre']} en 2026?",
         f"{p['nombre']} elige {d26} {dip} al Congreso en las elecciones generales del 29 de noviembre de 2026, {delta_txt}."),
        (f"¿Cuántos senadores elige {p['nombre']}?",
         f"Elige {sen_txt} por sufragio directo. En la papeleta del Senado se pueden marcar {senate_marks(p['slug'])}."),
        (f"¿Quién ganó las elecciones generales de 2023 {en}?",
         f"{label_2023(winner['partido'])} fue la candidatura más votada con {fint(winner['votos'])} votos ({fpct(winner['pct'])} %). Reparto de escaños: {reparto}."),
        (f"¿Cuántos votos cuesta un escaño {en}?",
         f"En 2023 el último escaño se asignó con un cociente de {fint(round(last[0]))} votos, un {fpct(cost)} % de los votos válidos. Además, hay que superar el 3 % de los votos válidos de la provincia." if last else "Depende del reparto D'Hondt de la provincia."),
        (f"¿Cuál fue la participación {en} en 2023?",
         f"Votó el {fpct(p['participacion'])} % del censo: {fint(p['votantes'])} de {fint(p['censo'])} electores."),
        ("¿Cuándo son las elecciones y en qué horario se vota?",
         "El domingo 29 de noviembre de 2026. Los colegios electorales abren de 9:00 a 20:00."),
    ]
    faq_html, faq_ld = faq_block(pairs)
    dataset_ld = {"@context": "https://schema.org", "@type": "Dataset",
                  "name": f"Resultados de las elecciones generales de 2023 {en} (Congreso)",
                  "description": f"Votos, porcentajes y escaños por candidatura {en} el 23 de julio de 2023, y escaños que elige en 2026.",
                  "spatialCoverage": {"@type": "Place", "name": f"{p['nombre']}, España"},
                  "temporalCoverage": "2023-07-23", "isAccessibleForFree": True, "inLanguage": "es-ES",
                  "creator": {"@type": "Organization", "name": CONFIG["site_name"]},
                  "isBasedOn": "https://infoelectoral.interior.gob.es", "license": "https://creativecommons.org/licenses/by/4.0/",
                  "url": url(path)}
    note = "Empieza con los resultados de 2023 en la provincia. Escribe tus porcentajes: se aplica D'Hondt con el umbral del 3 %. Es una herramienta de cálculo, no una encuesta."
    body = f"""{crumbs}
<div class="wrap">
  <div class="prov-head">
    <div>
      <header class="pagehead">
        <h1>Elecciones generales 2026 {E(en)}</h1>
        <p class="dek">Diputados que elige, resultados de 2023, cómo se repartieron los escaños y un simulador con los datos de la provincia.</p>
        <p class="updated">Actualizado el <time datetime="{TODAY.isoformat()}">{fdate(TODAY)}</time></p>
      </header>
      {answer_box(answer)}
    </div>
    <div class="locator" style="padding-top:1.5rem">{map_widget("locator", inline=False, switcher=False, highlight=p["slug"])}</div>
  </div>
  <dl class="factrow">
    <div><dt>Diputados 2026</dt><dd>{d26}{f"<small>{'+' if delta > 0 else ''}{delta}</small>" if delta else ""}</dd></div>
    <div><dt>Senadores</dt><dd>{sen_n}</dd></div>
    <div><dt>Censo 2023</dt><dd>{fint(p['censo'])}</dd></div>
    <div><dt>Participación 2023</dt><dd>{fpct(p['participacion'])} %</dd></div>
  </dl>
  {ad("wide")}
  <div class="layout"><div>
    <article class="prose">
      <h2 id="resultados-2023">Resultados de las elecciones generales de 2023 {E(en)}</h2>
      <p>El 23 de julio de 2023 votaron {fint(p['votantes'])} personas {E(en)}. Estas son las candidaturas por encima del 0,5 % de los votos válidos; la última cifra es el número de escaños.</p>
      {bars([r for r in p['res'] if r['pct'] >= 0.5][:9])}
      <div class="table-scroll"><table class="table"><thead><tr><th>Candidatura</th><th class="r">Votos</th><th class="r">%</th><th class="r">Escaños</th></tr></thead><tbody>{table_res}</tbody></table></div>
      <h2 id="reparto-dhondt">Cómo se repartieron los {d23} escaños</h2>
      <p>Con la ley D'Hondt, los votos de cada candidatura que supera el 3 % se dividen entre 1, 2, 3… y los escaños van a los cocientes más altos. Los resaltados son los que obtuvieron escaño en 2023.</p>
      <div class="table-scroll"><table class="table"><thead><tr><th>Candidatura</th>{qhead}</tr></thead><tbody>{''.join(qrows)}</tbody></table></div>
      {hidden_more}
      {last_txt}
      <h2 id="simulador">Simula el reparto {E(en)} en 2026</h2>
    </article>
    <div style="margin-top:1rem">{sim_widget(sim_province_data(p), f"{p['nombre']} · {d26} {dip}", note)}</div>
    <article class="prose">
      <h2 id="como-votar">Votar {E(en)} el 29 de noviembre</h2>
      <p>Los colegios abren de 9:00 a 20:00. Necesitas el DNI, el pasaporte o el carnet de conducir originales y en vigor. Puedes consultar tu colegio y tu mesa en la <a href="https://sede.ine.gob.es" rel="noopener">sede electrónica del INE</a>; consulta la <a href="/como-votar/">guía para votar</a> para el resto de detalles.</p>
      <p>En la papeleta blanca del Congreso eliges una lista cerrada. En la sepia del Senado puedes marcar {senate_marks(p['slug'])}.</p>
      <p>Si no vas a estar ese día, el plazo para pedir el <a href="/voto-por-correo/">voto por correo</a> termina el jueves 19 de noviembre. Si te ha tocado formar parte de una mesa, aquí tienes la <a href="/mesa-electoral/">guía de la mesa electoral</a>.</p>
    </article>
    <section style="margin-top:3rem"><h2 style="font-size:1.6rem;margin-bottom:1rem">¿A quién votarías {E(en)}?</h2>{vote_widget(province=p["slug"])}</section>
    {faq_html}
    <aside class="sources"><h2>Fuentes</h2><ul><li>Resultados 2023: <a href="https://infoelectoral.interior.gob.es" rel="noopener">Ministerio del Interior, Infoelectoral</a>.</li><li>Diputados por circunscripción: Real Decreto de convocatoria (BOE, 6 de octubre de 2026) y LOREG, arts. 161–163.</li></ul></aside>
  </div><aside class="rail"><div class="rail__sticky"><nav class="toc" aria-label="En esta página"><h2>En esta página</h2><ol><li><a href="#resultados-2023">Resultados 2023</a></li><li><a href="#reparto-dhondt">Reparto D'Hondt</a></li><li><a href="#simulador">Simulador</a></li><li><a href="#como-votar">Cómo votar</a></li><li><a href="#preguntas-frecuentes">Preguntas frecuentes</a></li></ol></nav>{ad("rail")}</div></aside></div>
  {sib_html}
</div>"""
    title = f"Elecciones generales 2026 {en}: escaños y resultados"
    if len(title) > 62:
        title = f"Elecciones 2026 {en}: escaños y resultados"
    desc = f"{p['nombre']} elige {d26} {dip} el 29N. Resultados de 2023, reparto D'Hondt, votos que costó el último escaño y simulador provincial."
    add(path, page(path, title, desc, body, ld=[bc, faq_ld, dataset_ld], active="/provincias/", scripts=("sim.js", "mapa.js", "voto.js")), "0.8")


def build_provinces_index():
    path = "/provincias/"
    crumbs, bc = breadcrumbs([("Provincias", path)])
    rows = "".join(
        f'<tr><td><a href="/provincias/{p["slug"]}/">{E(p["nombre"])}</a></td><td>{E(p["ccaa"])}</td><td class="r">{p["escanos2023"]}</td><td class="r"><strong>{p["seats"]}</strong></td><td class="r">{senators(p["slug"])[1]}</td></tr>'
        for p in sorted(PROVS, key=lambda x: (-x["seats"], slugify(x["nombre"]))))
    changes = [p for p in PROVS if p["seats"] != p["escanos2023"]]
    ch_txt = ("Respecto a 2023 cambian: " + "; ".join(f'{p["nombre"]} ({p["escanos2023"]} → {p["seats"]})' for p in changes) + "."
              if changes else "El reparto es el mismo que en 2023.")
    ch_txt += " Es el resultado de aplicar el artículo 162 de la LOREG a la población oficial de 2025; el reparto definitivo es el que fija el Real Decreto de convocatoria publicado en el BOE."
    body = f"""{crumbs}
<div class="wrap">
  <header class="pagehead"><h1>Escaños por provincia en las elecciones generales de 2026</h1>
  <p class="dek">Las 52 circunscripciones del Congreso, con los diputados que elige cada una, sus resultados de 2023 y un simulador propio.</p></header>
  {answer_box("El Congreso elige 350 diputados en 52 circunscripciones. Madrid es la que más elige y Ceuta y Melilla, las que menos (uno cada una). Cada provincia tiene dos escaños fijos y el resto se reparte según su población.", E(ch_txt))}
  <div style="margin-top:2rem;max-width:46rem">{map_widget("escanos", inline=False, title="Diputados por provincia")}</div>
  {ad("wide")}
  <section class="section" style="border-top:0;padding-top:0"><h2>Tabla de las 52 circunscripciones</h2>
  <div class="table-scroll"><table class="table"><thead><tr><th>Provincia</th><th>Comunidad</th><th class="r">Diputados 2023</th><th class="r">Diputados 2026</th><th class="r">Senadores</th></tr></thead><tbody>{rows}</tbody></table></div></section>
</div>"""
    item_ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Circunscripciones de las elecciones generales de 2026",
               "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": url(f'/provincias/{p["slug"]}/'), "name": p["nombre"]} for i, p in enumerate(PROVS)]}
    add(path, page(path, "Escaños por provincia: elecciones generales 2026",
                   "Cuántos diputados elige cada una de las 52 provincias el 29N de 2026, cambios respecto a 2023, senadores y resultados por circunscripción.",
                   body, ld=[bc, item_ld], active=path, scripts=("mapa.js",)), "0.9")


def simple_page(path, title, desc, h1, html_body, priority="0.3"):
    crumbs, bc = breadcrumbs([(h1, path)])
    body = f"""{crumbs}<div class="wrap"><header class="pagehead"><h1>{E(h1)}</h1></header><article class="prose" style="padding-bottom:4rem">{html_body}</article></div>"""
    add(path, page(path, title, desc, body, ld=[bc]), priority)


def build_legal():
    c = CONFIG
    simple_page("/sobre-nosotros/", f"Quiénes somos | {c['site_name']}", "Quién hace Elecciones 29N, cómo elaboramos los contenidos y cómo contactarnos.", "Quiénes somos", f"""
<p>{E(c['site_name'])} es una guía ciudadana independiente sobre las elecciones generales del 29 de noviembre de 2026. Nuestro objetivo es responder con claridad a las dudas prácticas del proceso electoral: la mesa electoral, el voto por correo, los plazos y el reparto de escaños.</p>
<h2>Independencia</h2><p>No pertenecemos a ningún partido, candidatura ni organismo público, ni recibimos financiación de ellos. La web se financia con publicidad. Los colores de los partidos solo se usan para representar datos.</p>
<h2>Cómo elaboramos los contenidos</h2><p>Cada dato procede de fuentes oficiales (BOE, Ley Orgánica del Régimen Electoral General, Junta Electoral Central, Ministerio del Interior, INE y Correos), que se citan al final de cada página. Las páginas indican la fecha de su última actualización. No publicamos encuestas propias.</p>
<h2>Contacto</h2><p>Para correcciones o sugerencias: {E(c['contact_email'])}.</p>""")
    simple_page("/aviso-legal/", f"Aviso legal | {c['site_name']}", "Aviso legal de Elecciones 29N.", "Aviso legal", f"""
<p>En cumplimiento de la Ley 34/2002, de servicios de la sociedad de la información y de comercio electrónico (LSSI-CE), se informa:</p>
<ul><li>Titular: {E(c['owner_name'])}</li><li>NIF: {E(c['owner_nif'])}</li><li>Domicilio: {E(c['owner_address'])}</li><li>Correo electrónico: {E(c['contact_email'])}</li></ul>
<h2>Objeto</h2><p>Este sitio ofrece información divulgativa sobre las elecciones generales de 2026. No es una web oficial. La información oficial está en el BOE, la Junta Electoral Central y el Ministerio del Interior, y prevalece sobre la de esta web.</p>
<h2>Responsabilidad</h2><p>Revisamos los contenidos con cuidado, pero no garantizamos que estén libres de errores. Las herramientas (simulador y test) son de cálculo y orientación; sus resultados no son encuestas ni predicciones.</p>
<h2>Propiedad intelectual</h2><p>Los textos y el diseño pertenecen al titular. Los datos electorales oficiales son de dominio público.</p>""")
    simple_page("/privacidad/", f"Política de privacidad | {c['site_name']}", "Política de privacidad de Elecciones 29N.", "Política de privacidad", f"""
<p>Responsable del tratamiento: {E(c['owner_name'])} ({E(c['contact_email'])}).</p>
<h2>Qué datos tratamos</h2><p>Esta web no tiene registro de usuarios ni formularios. El simulador y el test funcionan en tu navegador y no envían tus respuestas a ningún servidor.</p>
<p>Usamos Google AdSense para mostrar publicidad. Google y sus socios pueden usar cookies e identificadores para mostrar anuncios, personalizados o no según tu consentimiento. Más información en <a href="https://policies.google.com/technologies/ads" rel="noopener">Cómo utiliza Google las cookies en la publicidad</a>.</p>
<h2>Base legal y derechos</h2><p>La base legal es tu consentimiento, que puedes retirar en cualquier momento desde el aviso de cookies. Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a {E(c['contact_email'])}, y reclamar ante la Agencia Española de Protección de Datos (aepd.es).</p>""")
    simple_page("/cookies/", f"Política de cookies | {c['site_name']}", "Política de cookies de Elecciones 29N.", "Política de cookies", """
<p>Esta web no instala cookies propias. Las únicas cookies son las de Google AdSense y la plataforma de consentimiento de Google, que solo se activan si las aceptas en el aviso que aparece en la primera visita.</p>
<table><thead><tr><th>Proveedor</th><th>Finalidad</th><th>Más información</th></tr></thead><tbody>
<tr><td>Google (AdSense)</td><td>Mostrar y medir anuncios, personalizados o no</td><td><a href="https://policies.google.com/technologies/cookies" rel="noopener">policies.google.com</a></td></tr>
<tr><td>Google Fonts</td><td>Cargar las tipografías (no instala cookies)</td><td><a href="https://developers.google.com/fonts/faq/privacy" rel="noopener">developers.google.com</a></td></tr></tbody></table>
<p>Puedes cambiar tu elección en cualquier momento desde el enlace «Privacidad y cookies» del aviso de consentimiento, o borrar las cookies desde la configuración de tu navegador.</p>""")


def build_404():
    body = """<div class="wrap" style="padding:4rem 0 6rem"><h1 style="font-size:2.4rem">Esta página no existe</h1><p style="margin-top:1rem">Puede que la dirección haya cambiado. Prueba desde el <a href="/">inicio</a> o busca tu <a href="/provincias/">provincia</a>.</p></div>"""
    write("/404.html", page("/404.html", "Página no encontrada | Elecciones 29N", "Página no encontrada.", body))


def build_seo_files(guides_meta):
    sm = "".join(f"<url><loc>{url(p)}</loc><lastmod>{TODAY.isoformat()}</lastmod><priority>{pr}</priority></url>" for p, pr in SITEMAP)
    write("/sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    bots = ["Googlebot", "Bingbot", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "ClaudeBot", "Claude-SearchBot", "Google-Extended", "Applebot-Extended"]
    robots = "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"User-agent: *\nAllow: /\n\nSitemap: {url('/sitemap.xml')}\n"
    write("/robots.txt", robots)
    top = sorted(PROVS, key=lambda p: -p["seats"])
    lines = [f"# {CONFIG['site_name']}", "",
             "> Guía ciudadana independiente de las elecciones generales de España del 29 de noviembre de 2026: fechas, mesa electoral, voto por correo, reparto de escaños por provincia y herramientas de cálculo. Fuentes oficiales citadas en cada página.",
             "", "## Datos clave", "",
             "- Fecha: domingo 29 de noviembre de 2026; colegios de 9:00 a 20:00 (hora peninsular).",
             "- Convocatoria: Real Decreto publicado en el BOE el 6 de octubre de 2026.",
             "- Congreso: 350 diputados en 52 circunscripciones; mayoría absoluta 176; umbral del 3 % por provincia; ley D'Hondt.",
             "- Campaña: del 13 de noviembre (00:00) al 27 de noviembre (24:00). Jornada de reflexión: 28 de noviembre.",
             "- Voto por correo: solicitud hasta el 19 de noviembre; depósito en Correos hasta el 25 de noviembre.",
             "- Dieta por formar parte de una mesa electoral: 75 euros (titulares).",
             "- Diputados por provincia (2026): " + "; ".join(f"{p['nombre']} {p['seats']}" for p in top) + ".",
             "", "## Guías", ""]
    for g in guides_meta:
        if g:
            lines.append(f"- [{g['title']}]({url('/' + g['slug'] + '/')}): {g['answer'] or g['desc']}")
    lines += ["", "## Herramientas", "",
              f"- [Simulador de escaños]({url('/simulador-escanos/')}): reparto D'Hondt en las 52 circunscripciones a partir de porcentajes introducidos por el usuario.",
              f"- [Test de afinidad política]({url('/test-a-quien-voto/')}): 24 afirmaciones y posiciones documentadas de los partidos estatales.",
              f"- [Votación simbólica]({url('/votacion/')}): votación abierta de los lectores, sin valor estadístico; el resultado por partido se publica el 29 de noviembre a las 21:00.",
              "", "## Provincias", ""]
    lines += [f"- [{p['nombre']}]({url('/provincias/' + p['slug'] + '/')}): {p['seats']} diputados en 2026" for p in PROVS]
    write("/llms.txt", "\n".join(lines) + "\n")
    if CONFIG["adsense_client"]:
        pub = CONFIG["adsense_client"].replace("ca-", "")
        write("/ads.txt", f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n")


def main():
    DIST.mkdir(exist_ok=True)
    for child in DIST.iterdir():  # vaciar sin borrar la carpeta (puede estar en uso por el servidor local)
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    shutil.copytree(SRC / "assets", DIST / "assets")
    for extra in ("favicon.svg", ".htaccess"):
        if (SRC / extra).exists():
            shutil.copy(SRC / extra, DIST / extra)
    if (SRC / "og.png").exists():
        shutil.copy(SRC / "og.png", DIST / "assets" / "og.png")
    css = DIST / "assets" / "css" / "site.css"
    v2 = DIST / "assets" / "css" / "v2.css"
    css.write_bytes(css.read_bytes() + b"\n" + v2.read_bytes())
    v2.unlink()
    (DIST / "assets" / "data").mkdir(parents=True, exist_ok=True)
    (DIST / "assets" / "data" / "mapa.json").write_text(json.dumps(GEO, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (DIST / "assets" / "data" / "provincias-mini.json").write_text(json.dumps(MINI, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    guides_meta = [guide_page(*g) for g in GUIDES]
    build_home2()
    build_votacion()
    build_simulator()
    build_test()
    build_provinces_index()
    by_cc = {}
    for p in PROVS:
        by_cc.setdefault(p["ccaa"], []).append(p)
    for p in PROVS:
        build_province(p, by_cc[p["ccaa"]])
    build_legal()
    build_404()
    build_seo_files(guides_meta)
    print(f"OK · {len(SITEMAP)} páginas en {DIST}")


if __name__ == "__main__":
    main()
