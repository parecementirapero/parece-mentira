"""Ilustraciones del lote 2026-11-24-tarde (Agente 20:00 (Jorge)): 01 tu gato ignora el dulce, 02 las lágrimas no caen
en el espacio, 03 los vikingos no llevaban cuernos. Estilo cartoon con contorno grueso (el del lote 2026-11-23-tarde).
Reutiliza el lote 2026-11-23-tarde entero (muñecos, astronauta, cielo, pizarra…). Todo dibujado aquí, sin logos ni personas reales.
Uso: python3 ilus_1124t.py DIR_SVG"""
import importlib.util, math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano  # noqa: E402

OL = "#1b1b2b"


def _mod(rel, nombre):
    s = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, rel))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def sombra(cx, cy, rx, ry=None, op=0.3):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry or rx * 0.12}" fill="#000" opacity="{op}"/>'


# ====================================================================== 01 · gato
def gato(nombre="gato", pelo=("#ffb35a", "#e0782a"), marca="#b8541a", patron="rayas", lengua=False, ojos="#7ac84a"):
    """Gato cartoon sentado de frente (lienzo 600x700). patron: rayas | manchas | tigre."""
    w, h = 600, 700
    d = lg(nombre + "_p", (0, pelo[0]), (1, pelo[1])) + lg(nombre + "_v", (0, "#fff4e4"), (1, "#f2d8b8"))
    b = [sombra(300, 680, 220, 22),
         # cola
         f'<path d="M430 640 C560 640 580 520 530 440" stroke="{OL}" stroke-width="64" fill="none" stroke-linecap="round"/>',
         f'<path d="M430 640 C560 640 580 520 530 440" stroke="{pelo[1]}" stroke-width="44" fill="none" stroke-linecap="round"/>',
         # cuerpo
         f'<path d="M160 660 C130 520 170 380 300 370 C430 380 470 520 440 660 Z" fill="url(#{nombre}_p)" stroke="{OL}" stroke-width="12"/>',
         f'<path d="M230 660 C220 560 240 450 300 440 C360 450 380 560 370 660 Z" fill="url(#{nombre}_v)"/>',
         # patas delanteras
         f'<rect x="215" y="560" width="70" height="110" rx="34" fill="url(#{nombre}_p)" stroke="{OL}" stroke-width="10"/>',
         f'<rect x="315" y="560" width="70" height="110" rx="34" fill="url(#{nombre}_p)" stroke="{OL}" stroke-width="10"/>',
         # orejas
         f'<path d="M140 210 L150 40 L270 130 Z" fill="url(#{nombre}_p)" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>',
         f'<path d="M460 210 L450 40 L330 130 Z" fill="url(#{nombre}_p)" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>',
         '<path d="M165 170 L170 85 L235 135 Z M435 170 L430 85 L365 135 Z" fill="#ff9aa8"/>',
         # cabeza
         f'<ellipse cx="300" cy="250" rx="190" ry="160" fill="url(#{nombre}_p)" stroke="{OL}" stroke-width="12"/>',
         f'<ellipse cx="300" cy="320" rx="110" ry="70" fill="url(#{nombre}_v)"/>']
    if patron in ("rayas", "tigre"):
        g = 16 if patron == "tigre" else 11
        b += [f'<path d="M300 92 L300 150 M250 98 L262 150 M350 98 L338 150" stroke="{marca}" stroke-width="{g}" stroke-linecap="round"/>',
              f'<path d="M115 230 L170 245 M112 275 L165 280 M485 230 L430 245 M488 275 L435 280" stroke="{marca}" stroke-width="{g}" stroke-linecap="round"/>',
              f'<path d="M175 450 Q215 470 210 500 M425 450 Q385 470 390 500 M168 540 Q205 555 205 585 M432 540 Q395 555 395 585" stroke="{marca}" stroke-width="{g}" fill="none" stroke-linecap="round"/>']
    if patron == "manchas":
        rr = random.Random(5)
        for _ in range(26):
            x, y = rr.choice([(rr.uniform(130, 470), rr.uniform(120, 220)), (rr.uniform(170, 430), rr.uniform(420, 640))])
            if 230 < x < 370 and y > 430:
                continue
            b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr.uniform(8, 14):.0f}" fill="{marca}"/>')
        b.append(f'<path d="M232 270 Q215 330 228 360 M368 270 Q385 330 372 360" stroke="{marca}" stroke-width="9" fill="none"/>')
    # ojos, nariz, boca, bigotes
    b += [f'<ellipse cx="225" cy="235" rx="44" ry="52" fill="{ojos}" stroke="{OL}" stroke-width="9"/>',
          f'<ellipse cx="375" cy="235" rx="44" ry="52" fill="{ojos}" stroke="{OL}" stroke-width="9"/>',
          f'<ellipse cx="225" cy="240" rx="14" ry="38" fill="{OL}"/><ellipse cx="375" cy="240" rx="14" ry="38" fill="{OL}"/>',
          '<circle cx="238" cy="218" r="11" fill="#fff"/><circle cx="388" cy="218" r="11" fill="#fff"/>',
          f'<path d="M280 300 L320 300 L300 325 Z" fill="#ff7a8a" stroke="{OL}" stroke-width="7" stroke-linejoin="round"/>',
          f'<path d="M300 325 Q300 350 270 352 M300 325 Q300 350 330 352" stroke="{OL}" stroke-width="7" fill="none" stroke-linecap="round"/>',
          f'<path d="M200 315 L90 300 M200 335 L95 345 M400 315 L510 300 M400 335 L505 345" stroke="{OL}" stroke-width="5" stroke-linecap="round" opacity="0.8"/>']
    if lengua:
        b.append(f'<path d="M282 350 Q282 420 300 425 Q318 420 318 350 Z" fill="#ff6a86" stroke="{OL}" stroke-width="7"/>')
    guardar(nombre, "".join(b), w, h, d)


def bg_cocina(nombre="bg_cocina"):
    d = lg("co_p", (0, "#ffe9c8"), (1, "#f6c98e")) + lg("co_m", (0, "#b8763e"), (1, "#7a4a22"))
    b = ['<rect width="1080" height="1920" fill="url(#co_p)"/>']
    for y in range(120, 1300, 120):
        for x in range(0 if (y // 120) % 2 else -60, 1080, 120):
            b.append(f'<rect x="{x + 6}" y="{y + 6}" width="108" height="108" rx="10" fill="#fff6e6" opacity="0.55"/>')
    b += ['<rect x="680" y="260" width="300" height="380" rx="20" fill="#9ad6ff" stroke="#7a4a22" stroke-width="22"/>',
          '<path d="M830 260 L830 640 M680 450 L980 450" stroke="#7a4a22" stroke-width="14"/>',
          '<rect x="0" y="1300" width="1080" height="80" fill="#e8e0d4" stroke="#1b1b2b" stroke-width="10"/>',
          '<rect x="0" y="1380" width="1080" height="540" fill="url(#co_m)"/>',
          '<path d="M60 1460 L500 1460 L500 1880 L60 1880 Z M580 1460 L1020 1460 L1020 1880 L580 1880 Z" fill="none" stroke="#5a3418" stroke-width="10"/>',
          '<circle cx="470" cy="1660" r="14" fill="#e8c070"/><circle cx="610" cy="1660" r="14" fill="#e8c070"/>']
    guardar(nombre, "".join(b), 1080, 1920, d)


def pastel(nombre="pastel"):
    w, h = 520, 440
    b = [sombra(260, 420, 220, 16),
         f'<path d="M40 210 L480 120 L480 380 L40 400 Z" fill="#f8d8a0" stroke="{OL}" stroke-width="10" stroke-linejoin="round"/>',
         '<path d="M40 290 L480 240 L480 270 L40 320 Z" fill="#ff6a9a"/>',
         f'<path d="M40 210 L480 120 Q500 90 470 80 L60 170 Q20 190 40 210 Z" fill="#fff4f8" stroke="{OL}" stroke-width="10"/>',
         f'<path d="M80 200 q10 40 20 0 M180 180 q10 50 20 0 M300 155 q10 40 20 0 M400 135 q10 45 20 0" fill="#fff4f8" stroke="{OL}" stroke-width="6"/>',
         f'<circle cx="420" cy="80" r="40" fill="#e0203a" stroke="{OL}" stroke-width="8"/><path d="M420 40 q10 -30 30 -30" stroke="#3a8a2a" stroke-width="8" fill="none"/>',
         '<circle cx="408" cy="68" r="9" fill="#fff" opacity="0.7"/>']
    guardar(nombre, "".join(b), w, h)


def caramelo(nombre="caramelo"):
    w, h = 520, 260
    b = [f'<path d="M150 130 L30 40 L60 130 L30 220 Z" fill="#ff5aa8" stroke="{OL}" stroke-width="9" stroke-linejoin="round"/>',
         f'<path d="M370 130 L490 40 L460 130 L490 220 Z" fill="#ff5aa8" stroke="{OL}" stroke-width="9" stroke-linejoin="round"/>',
         f'<ellipse cx="260" cy="130" rx="120" ry="90" fill="#ff8ac8" stroke="{OL}" stroke-width="10"/>',
         '<path d="M180 70 Q260 130 200 200 M260 45 Q330 130 270 215 M330 60 Q380 130 340 195" stroke="#fff" stroke-width="16" fill="none" opacity="0.8"/>',
         '<ellipse cx="210" cy="90" rx="30" ry="14" fill="#fff" opacity="0.6"/>']
    guardar(nombre, "".join(b), w, h)


def helado(nombre="helado"):
    w, h = 360, 620
    b = [f'<path d="M80 270 L180 600 L280 270 Z" fill="#e8a860" stroke="{OL}" stroke-width="10" stroke-linejoin="round"/>',
         '<path d="M110 300 L230 520 M160 290 L255 380 M250 300 L130 520 M200 290 L105 380" stroke="#b8763e" stroke-width="7"/>',
         f'<circle cx="130" cy="240" r="80" fill="#ffd8e8" stroke="{OL}" stroke-width="10"/>',
         f'<circle cx="230" cy="240" r="80" fill="#fff4d8" stroke="{OL}" stroke-width="10"/>',
         f'<circle cx="180" cy="150" r="90" fill="#8a5a3a" stroke="{OL}" stroke-width="10"/>',
         '<ellipse cx="150" cy="115" rx="30" ry="16" fill="#fff" opacity="0.45"/>',
         f'<path d="M100 300 q0 40 15 40 q10 0 10 -35" fill="#ffd8e8" stroke="{OL}" stroke-width="6"/>']
    guardar(nombre, "".join(b), w, h)


def filete(nombre="filete"):
    w, h = 560, 380
    b = [sombra(280, 360, 240, 16),
         f'<path d="M60 180 C60 70 200 40 300 60 C440 80 520 150 500 230 C480 320 340 340 220 330 C100 320 60 270 60 180 Z" fill="#d8404a" stroke="{OL}" stroke-width="12"/>',
         '<path d="M110 170 C160 120 260 110 330 140 M150 240 C230 210 330 220 420 200 M380 120 C430 150 450 180 440 210" stroke="#ffd0c8" stroke-width="14" fill="none" stroke-linecap="round"/>',
         f'<path d="M470 150 C530 190 520 260 480 280" stroke="#fff4e8" stroke-width="30" fill="none" stroke-linecap="round"/>',
         '<ellipse cx="200" cy="110" rx="50" ry="16" fill="#fff" opacity="0.35"/>']
    guardar(nombre, "".join(b), w, h)


def azucar(nombre="azucar"):
    w, h = 320, 320
    b = [f'<path d="M60 110 L170 60 L280 110 L280 240 L170 290 L60 240 Z" fill="#ffffff" stroke="{OL}" stroke-width="10" stroke-linejoin="round"/>',
         f'<path d="M60 110 L170 160 L280 110 M170 160 L170 290" stroke="{OL}" stroke-width="8" fill="none"/>',
         '<path d="M170 160 L280 110 L280 240 L170 290 Z" fill="#dde6f0"/>']
    rr = random.Random(3)
    for _ in range(40):
        b.append(f'<circle cx="{rr.uniform(80, 260):.0f}" cy="{rr.uniform(90, 270):.0f}" r="3" fill="#b8c4d8" opacity="0.8"/>')
    guardar(nombre, "".join(b), w, h)


def lengua(nombre="lengua"):
    """Lengua grande vista desde arriba con papilas (lienzo 640x820)."""
    w, h = 640, 820
    d = lg("le_g", (0, "#ff9aa8"), (1, "#e05a74"))
    b = [f'<path d="M60 60 L580 60 C620 380 560 760 320 790 C80 760 20 380 60 60 Z" fill="url(#le_g)" stroke="{OL}" stroke-width="14"/>',
         '<path d="M320 90 L320 600" stroke="#c03a5a" stroke-width="12" stroke-linecap="round"/>']
    rr = random.Random(9)
    for _ in range(70):
        x, y = rr.uniform(110, 530), rr.uniform(110, 700)
        if abs(x - 320) < 25:
            continue
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr.uniform(6, 12):.0f}" fill="#ffc0cc" opacity="0.85"/>')
    b.append('<ellipse cx="180" cy="180" rx="60" ry="26" fill="#fff" opacity="0.3"/>')
    guardar(nombre, "".join(b), w, h, d)


def pieza(nombre, color, lado="izq", rota=False):
    """Media pieza del receptor del dulce, como pieza de puzle (lienzo 360x520)."""
    w, h = 360, 520
    if lado == "izq":
        p = "M40 40 L300 40 L300 200 C360 200 360 300 300 300 L300 480 L40 480 Z"
    else:
        p = "M60 40 L320 40 L320 480 L60 480 L60 300 C120 300 120 200 60 200 Z"
    b = [f'<path d="{p}" fill="{color}" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>',
         f'<path d="M80 80 L80 420" stroke="#fff" stroke-width="18" opacity="0.35" stroke-linecap="round"/>']
    if rota:
        b.append(f'<path d="M60 150 L140 210 L90 260 L170 330 L120 380" stroke="{OL}" stroke-width="12" fill="none" stroke-linejoin="round"/>')
        b.append(f'<path d="M190 120 L240 160 M220 360 L260 400" stroke="{OL}" stroke-width="8"/>')
    guardar(nombre, "".join(b), w, h)


def adn(nombre="adn", hueco=False):
    """Tira de ADN en horizontal con «letras» de colores (lienzo 1000x360). hueco=True → falta un trozo en medio."""
    w, h = 1000, 360
    cols = ["#ff5a5a", "#3a8aff", "#ffd23f", "#3ac84a"]
    rr = random.Random(4)
    b = []
    n = 26
    for i in range(n):
        x = 40 + i * 36
        if hueco and 11 <= i <= 15:
            continue
        y1 = 180 - 110 * math.sin(i * 0.5)
        y2 = 180 + 110 * math.sin(i * 0.5)
        b.append(f'<path d="M{x} {y1:.0f} L{x} 180" stroke="{rr.choice(cols)}" stroke-width="14"/>')
        b.append(f'<path d="M{x} 180 L{x} {y2:.0f}" stroke="{rr.choice(cols)}" stroke-width="14"/>')
    for s in (1, -1):
        seg = []
        for tramo in ([range(0, 12), range(15, n)] if hueco else [range(0, n)]):
            pts = " ".join(f"{40 + i * 36} {180 - s * 110 * math.sin(i * 0.5):.0f}" for i in tramo)
            seg.append(f'<polyline points="{pts}" stroke="{OL}" stroke-width="22" fill="none" stroke-linecap="round"/>')
            seg.append(f'<polyline points="{pts}" stroke="{"#7df9ff" if s > 0 else "#ff9af2"}" stroke-width="10" fill="none" stroke-linecap="round"/>')
        b += seg
    if hueco:
        b.append(f'<path d="M455 60 L470 120 L450 180 L475 250 L455 300 M545 60 L530 120 L550 180 L525 250 L545 300" stroke="#ff3d3d" stroke-width="8" fill="none" stroke-dasharray="14 10"/>')
    guardar(nombre, "".join(b), w, h)


def microscopio(nombre="microscopio"):
    w, h = 420, 620
    b = [sombra(210, 600, 170, 16),
         f'<rect x="70" y="540" width="280" height="50" rx="18" fill="#3a4a6a" stroke="{OL}" stroke-width="10"/>',
         f'<path d="M260 540 C330 420 330 260 250 200" stroke="{OL}" stroke-width="56" fill="none"/>',
         f'<path d="M260 540 C330 420 330 260 250 200" stroke="#5a6a8a" stroke-width="36" fill="none"/>',
         f'<rect x="90" y="400" width="200" height="30" rx="10" fill="#8a9ab8" stroke="{OL}" stroke-width="8"/>',
         f'<rect x="130" y="70" width="80" height="300" rx="20" fill="#e8ecf4" stroke="{OL}" stroke-width="10" transform="rotate(-18 170 220)"/>',
         f'<rect x="120" y="30" width="100" height="50" rx="12" fill="#3a4a6a" stroke="{OL}" stroke-width="8" transform="rotate(-18 170 55)"/>',
         '<circle cx="200" cy="380" r="12" fill="#7df9ff"/>']
    guardar(nombre, "".join(b), w, h)


def cuenco(nombre="cuenco"):
    w, h = 480, 260
    b = [sombra(240, 245, 200, 14),
         f'<path d="M30 80 L450 80 C440 200 360 240 240 240 C120 240 40 200 30 80 Z" fill="#3a8aff" stroke="{OL}" stroke-width="12"/>',
         f'<ellipse cx="240" cy="80" rx="210" ry="34" fill="#c86a4a" stroke="{OL}" stroke-width="10"/>',
         '<path d="M150 70 q20 -20 40 0 q20 -20 40 0 q20 -20 40 0" stroke="#ffb0a0" stroke-width="10" fill="none"/>',
         '<text x="240" y="190" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="60" fill="#fff">MIAU</text>']
    guardar(nombre, "".join(b), w, h)


def bg_lab_claro(nombre="bg_lab_claro"):
    d = lg("lc_p", (0, "#dff4f4"), (1, "#a8d8dc"))
    b = ['<rect width="1080" height="1920" fill="url(#lc_p)"/>',
         '<rect x="0" y="0" width="1080" height="220" fill="#8ac8cc"/>']
    for x in (120, 420, 720):
        b.append(f'<rect x="{x}" y="300" width="240" height="520" rx="14" fill="#fff" stroke="#1b1b2b" stroke-width="10"/>')
        for k in range(3):
            b.append(f'<rect x="{x + 30 + k * 70}" y="{360 + k * 30}" width="40" height="{140 - k * 20}" rx="10" fill="{["#ff5a8a", "#3ac84a", "#ffd23f"][k]}" stroke="#1b1b2b" stroke-width="6"/>')
        b.append(f'<path d="M{x} 600 L{x + 240} 600" stroke="#1b1b2b" stroke-width="8"/>')
    b += ['<rect x="0" y="1320" width="1080" height="70" fill="#e8f0f4" stroke="#1b1b2b" stroke-width="10"/>',
          '<rect x="0" y="1390" width="1080" height="530" fill="#5a7a9a"/>']
    guardar(nombre, "".join(b), 1080, 1920, d)


# ====================================================================== 02 · lágrimas en el espacio
def cara_astro(nombre="cara_astro", hinchada=False, nariz_roja=False):
    """Cara cartoon de frente con gorro de comunicaciones del traje (lienzo 700x820). El ojo izquierdo (x≈250, y≈400)
    es donde va la bola de agua. hinchada=True → cara más redonda y ojos más pequeños."""
    w, h = 700, 820
    rx, ry = (300, 300) if hinchada else (240, 300)
    d = lg(nombre + "_piel", (0, "#ffd8b8"), (1, "#e8a882"))
    b = [f'<path d="M140 820 C150 700 230 660 350 660 C470 660 550 700 560 820 Z" fill="#2a5ae8" stroke="{OL}" stroke-width="12"/>',
         f'<ellipse cx="350" cy="420" rx="{rx}" ry="{ry}" fill="url(#{nombre}_piel)" stroke="{OL}" stroke-width="12"/>',
         f'<path d="M{350 - rx + 10} 330 C{350 - rx + 20} 80 {350 + rx - 20} 80 {350 + rx - 10} 330 C300 250 400 250 {350 - rx + 10} 330 Z" fill="#f4f4f8" stroke="{OL}" stroke-width="12"/>',
         f'<path d="M{350 - rx + 10} 330 C{350 - rx + 20} 80 {350 + rx - 20} 80 {350 + rx - 10} 330" fill="#ffffff" stroke="{OL}" stroke-width="12"/>',
         f'<ellipse cx="{350 - rx - 5}" cy="420" rx="40" ry="60" fill="#3a3a4a" stroke="{OL}" stroke-width="10"/>',
         f'<ellipse cx="{350 + rx + 5}" cy="420" rx="40" ry="60" fill="#3a3a4a" stroke="{OL}" stroke-width="10"/>']
    eo = 28 if hinchada else 36
    for x in (250, 450):
        b.append(f'<ellipse cx="{x}" cy="400" rx="{eo + 14}" ry="{eo + 8}" fill="#fff" stroke="{OL}" stroke-width="8"/>')
        b.append(f'<circle cx="{x}" cy="404" r="{eo - 10}" fill="#4a7ab8"/><circle cx="{x}" cy="404" r="{eo - 22}" fill="{OL}"/><circle cx="{x + 6}" cy="396" r="5" fill="#fff"/>')
        b.append(f'<path d="M{x - 50} 340 Q{x} 320 {x + 50} 340" stroke="#6a4a2a" stroke-width="14" fill="none" stroke-linecap="round"/>')
    b += [f'<path d="M350 430 Q330 500 350 510 Q370 512 380 500" stroke="{OL}" stroke-width="8" fill="{"#ff8a8a" if nariz_roja else "none"}" stroke-linecap="round"/>',
          f'<path d="M290 580 Q350 600 410 580" stroke="{OL}" stroke-width="10" fill="none" stroke-linecap="round"/>']
    if hinchada:
        b.append('<ellipse cx="190" cy="520" rx="50" ry="26" fill="#ff8a8a" opacity="0.5"/><ellipse cx="510" cy="520" rx="50" ry="26" fill="#ff8a8a" opacity="0.5"/>')
    guardar(nombre, "".join(b), w, h, d)


def bola_agua(nombre="bola_agua"):
    w = h = 400
    d = rg("ba_g", (0, "#e8fbff", 0.9), (0.6, "#7ad0ff", 0.75), (1, "#2a8ae8", 0.85), cx=0.38, cy=0.35)
    b = ['<circle cx="200" cy="200" r="180" fill="url(#ba_g)" stroke="#1b5aa8" stroke-width="8"/>',
         '<ellipse cx="140" cy="120" rx="54" ry="30" fill="#fff" opacity="0.85" transform="rotate(-30 140 120)"/>',
         '<circle cx="270" cy="280" r="16" fill="#fff" opacity="0.5"/>']
    guardar(nombre, "".join(b), w, h, d)


def lagrima(nombre="lagrima"):
    w, h = 200, 300
    d = rg("la_g", (0, "#e8fbff", 1), (1, "#3a9ae8", 1), cx=0.35, cy=0.6)
    b = [f'<path d="M100 20 C100 20 30 160 30 210 C30 255 62 285 100 285 C138 285 170 255 170 210 C170 160 100 20 100 20 Z" fill="url(#la_g)" stroke="{OL}" stroke-width="8"/>',
         '<ellipse cx="72" cy="200" rx="14" ry="30" fill="#fff" opacity="0.7"/>']
    guardar(nombre, "".join(b), w, h, d)


def estacion(nombre="estacion"):
    """Estación espacial cartoon (lienzo 1000x520): módulos blancos y paneles solares dorados."""
    w, h = 1000, 520
    b = []
    for x in (40, 760):
        for y in (40, 300):
            b.append(f'<rect x="{x}" y="{y}" width="200" height="180" rx="8" fill="#e0a830" stroke="{OL}" stroke-width="9"/>')
            b.append(f'<path d="M{x + 50} {y} L{x + 50} {y + 180} M{x + 100} {y} L{x + 100} {y + 180} M{x + 150} {y} L{x + 150} {y + 180} M{x} {y + 90} L{x + 200} {y + 90}" stroke="#9a6a10" stroke-width="5"/>')
    b += [f'<rect x="140" y="245" width="720" height="30" fill="#c8ccd8" stroke="{OL}" stroke-width="8"/>',
          f'<path d="M140 220 L140 300 M860 220 L860 300" stroke="{OL}" stroke-width="12"/>',
          f'<rect x="360" y="190" width="280" height="140" rx="50" fill="#f4f4f8" stroke="{OL}" stroke-width="10"/>',
          f'<rect x="440" y="120" width="120" height="290" rx="40" fill="#ffffff" stroke="{OL}" stroke-width="10"/>',
          '<circle cx="500" cy="170" r="16" fill="#7df9ff" stroke="#1b1b2b" stroke-width="5"/><circle cx="410" cy="260" r="12" fill="#7df9ff"/><circle cx="590" cy="260" r="12" fill="#7df9ff"/>',
          '<path d="M380 210 L620 210" stroke="#fff" stroke-width="10" opacity="0.6"/>']
    guardar(nombre, "".join(b), w, h)


def bg_modulo(nombre="bg_modulo"):
    """Interior de un módulo de la estación: paredes acolchadas, cables, pantallas y una ventana redonda con la Tierra."""
    d = lg("mo_p", (0, "#e8ecf4"), (1, "#b8c0d0")) + rg("mo_t", (0, "#8ad0ff", 1), (0.7, "#2a6ad8", 1), (1, "#0a2a6a", 1))
    b = ['<rect width="1080" height="1920" fill="url(#mo_p)"/>',
         '<path d="M0 0 L240 300 L240 1620 L0 1920 Z" fill="#d0d6e2"/><path d="M1080 0 L840 300 L840 1620 L1080 1920 Z" fill="#c4cad8"/>',
         '<rect x="240" y="300" width="600" height="1320" fill="#dfe4ee" stroke="#9aa2b4" stroke-width="8"/>']
    for y in range(340, 1600, 160):
        b.append(f'<rect x="270" y="{y}" width="250" height="130" rx="12" fill="#f4f6fa" stroke="#9aa2b4" stroke-width="6"/>')
        b.append(f'<rect x="560" y="{y}" width="250" height="130" rx="12" fill="#f4f6fa" stroke="#9aa2b4" stroke-width="6"/>')
    b += ['<circle cx="540" cy="760" r="150" fill="#5a6274" stroke="#1b1b2b" stroke-width="14"/>',
          '<circle cx="540" cy="760" r="120" fill="#02030a"/>',
          '<circle cx="570" cy="830" r="110" fill="url(#mo_t)"/>',
          '<path d="M480 800 q30 -30 60 -10 q20 20 50 0" stroke="#3ac84a" stroke-width="18" fill="none" opacity="0.8"/>',
          '<path d="M30 200 C200 400 60 700 200 1000 M1050 300 C900 600 1040 900 880 1300" stroke="#e0303a" stroke-width="10" fill="none"/>',
          '<path d="M60 260 C220 460 80 760 220 1060" stroke="#2a6ad8" stroke-width="10" fill="none"/>',
          '<rect x="880" y="900" width="160" height="110" rx="10" fill="#1b1b2b"/><rect x="895" y="915" width="130" height="80" fill="#3ac84a" opacity="0.7"/>']
    guardar(nombre, "".join(b), 1080, 1920, d)


def molecula_agua(nombre="molecula_agua"):
    w, h = 300, 240
    b = [f'<circle cx="150" cy="130" r="80" fill="#ff4a4a" stroke="{OL}" stroke-width="9"/>',
         f'<circle cx="60" cy="70" r="46" fill="#ffffff" stroke="{OL}" stroke-width="8"/>',
         f'<circle cx="240" cy="70" r="46" fill="#ffffff" stroke="{OL}" stroke-width="8"/>',
         '<ellipse cx="125" cy="100" rx="24" ry="12" fill="#fff" opacity="0.5"/>']
    guardar(nombre, "".join(b), w, h)


def toalla(nombre="toalla"):
    w, h = 460, 380
    b = [f'<path d="M40 60 Q230 20 420 60 L400 330 Q230 360 60 330 Z" fill="#ff8a3a" stroke="{OL}" stroke-width="11" stroke-linejoin="round"/>',
         '<path d="M55 270 Q230 300 405 270 M60 300 Q230 330 402 300" stroke="#fff" stroke-width="12" fill="none"/>',
         '<path d="M120 80 L110 320 M200 70 L195 330 M280 70 L285 330 M360 75 L370 320" stroke="#e06a20" stroke-width="5" opacity="0.6"/>']
    guardar(nombre, "".join(b), w, h)


def cuerpo_flujo(nombre="cuerpo_flujo", espacio=False):
    """Silueta de persona de frente (lienzo 420x1000). espacio=True → cabeza y cara grandes, piernas finas."""
    w, h = 420, 1000
    cab = 120 if espacio else 95
    pier = 28 if espacio else 48
    b = [f'<circle cx="210" cy="{30 + cab}" r="{cab}" fill="#ffd0b0" stroke="{OL}" stroke-width="11"/>',
         f'<path d="M110 300 L310 300 L330 600 L90 600 Z" fill="#2a5ae8" stroke="{OL}" stroke-width="11" stroke-linejoin="round"/>',
         f'<rect x="{150 - pier / 2}" y="590" width="{pier}" height="380" rx="{pier / 2}" fill="#2a3a6a" stroke="{OL}" stroke-width="10"/>',
         f'<rect x="{270 - pier / 2}" y="590" width="{pier}" height="380" rx="{pier / 2}" fill="#2a3a6a" stroke="{OL}" stroke-width="10"/>',
         f'<circle cx="{210 - cab * 0.35:.0f}" cy="{30 + cab}" r="10" fill="{OL}"/><circle cx="{210 + cab * 0.35:.0f}" cy="{30 + cab}" r="10" fill="{OL}"/>',
         f'<path d="M{210 - cab * 0.3:.0f} {30 + cab * 1.45:.0f} Q210 {30 + cab * 1.6:.0f} {210 + cab * 0.3:.0f} {30 + cab * 1.45:.0f}" stroke="{OL}" stroke-width="8" fill="none"/>']
    guardar(nombre, "".join(b), w, h)


def panuelo(nombre="panuelo"):
    w, h = 320, 300
    b = [f'<path d="M30 60 L290 40 L270 260 L50 280 Z" fill="#ffffff" stroke="{OL}" stroke-width="10" stroke-linejoin="round"/>',
         '<path d="M70 90 L250 75 M75 130 L255 115 M80 170 L250 158" stroke="#7ad0ff" stroke-width="8"/>']
    guardar(nombre, "".join(b), w, h)


def botella(nombre="botella"):
    w, h = 220, 480
    b = [f'<rect x="80" y="20" width="60" height="70" rx="10" fill="#3a3a4a" stroke="{OL}" stroke-width="8"/>',
         f'<path d="M40 110 Q40 80 110 80 Q180 80 180 110 L180 440 Q180 465 155 465 L65 465 Q40 465 40 440 Z" fill="#9ad8ff" stroke="{OL}" stroke-width="10"/>',
         '<rect x="40" y="220" width="140" height="120" fill="#ffffff" opacity="0.7"/><path d="M70 130 L70 420" stroke="#fff" stroke-width="12" opacity="0.6"/>']
    guardar(nombre, "".join(b), w, h)


# ====================================================================== 03 · vikingos
def casco_cuernos(nombre="casco_cuernos", alas=False, cuernos=True):
    """Casco «de vikingo de disfraz» (lienzo 900x620): cúpula metálica con remaches y dos cuernos (o alas)."""
    w, h = 900, 620
    d = lg(nombre + "_m", (0, "#d8dee8"), (1, "#7a8494")) + lg(nombre + "_c", (0, "#fff4d8"), (1, "#c8a870"))
    b = []
    if cuernos and not alas:
        b += [f'<path d="M270 330 C170 300 90 200 110 40 C160 160 230 220 300 240 Z" fill="url(#{nombre}_c)" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>',
              f'<path d="M630 330 C730 300 810 200 790 40 C740 160 670 220 600 240 Z" fill="url(#{nombre}_c)" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>',
              '<path d="M150 150 L230 200 M760 150 L680 200" stroke="#a88850" stroke-width="8"/>']
    if alas:
        for s in (1, -1):
            cx = 450 - s * 200
            for k in range(4):
                b.append(f'<path d="M{cx} {300 - k * 10} C{cx - s * (120 + k * 30)} {240 - k * 50} {cx - s * (160 + k * 40)} {120 - k * 30} {cx - s * (140 + k * 40)} {60 - k * 15} C{cx - s * (90 + k * 20)} {150 - k * 30} {cx - s * 40} {230 - k * 20} {cx} {300 - k * 10} Z" fill="#ffffff" stroke="{OL}" stroke-width="9"/>')
    b += [f'<path d="M210 450 C210 220 330 140 450 140 C570 140 690 220 690 450 Z" fill="url(#{nombre}_m)" stroke="{OL}" stroke-width="14"/>',
          f'<rect x="190" y="420" width="520" height="70" rx="20" fill="#9aa2b2" stroke="{OL}" stroke-width="12"/>',
          '<path d="M270 300 C290 230 340 190 400 175" stroke="#fff" stroke-width="20" fill="none" opacity="0.55" stroke-linecap="round"/>']
    for x in range(240, 700, 70):
        b.append(f'<circle cx="{x}" cy="455" r="10" fill="#e8ecf4" stroke="{OL}" stroke-width="4"/>')
    guardar(nombre, "".join(b), w, h, d)


def cuerno(nombre="cuerno", espejo=False):
    w, h = 300, 360
    d = lg("cu_c", (0, "#fff4d8"), (1, "#c8a870"))
    b = [f'<path d="M190 330 C90 300 10 200 30 30 C80 150 150 210 220 230 Z" fill="url(#cu_c)" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>']
    if espejo:
        b = ['<g transform="translate(300,0) scale(-1,1)">'] + b + ['</g>']
    guardar(nombre, "".join(b), w, h, d)


def casco_gjermundbu(nombre="casco_gjermundbu"):
    """Casco vikingo real: cúpula redonda de hierro con bandas en cruz y una «gafa» que protege ojos y nariz (lienzo 800x720)."""
    w, h = 800, 720
    d = lg("gj_m", (0, "#8a8a92"), (0.6, "#5a5a62"), (1, "#3a3a42"))
    b = [f'<path d="M150 470 C150 200 270 100 400 100 C530 100 650 200 650 470 Z" fill="url(#gj_m)" stroke="{OL}" stroke-width="14"/>',
         f'<path d="M400 100 L400 470 M150 330 C250 300 550 300 650 330" stroke="{OL}" stroke-width="10"/>',
         '<path d="M400 100 L400 470 M150 330 C250 300 550 300 650 330" stroke="#9a9aa2" stroke-width="22" opacity="0.6"/>',
         f'<circle cx="400" cy="88" r="22" fill="#6a6a72" stroke="{OL}" stroke-width="8"/>',
         # la «gafa»
         f'<path d="M190 460 L610 460 L600 520 C580 600 500 610 470 560 L430 520 L430 650 L370 650 L370 520 L330 560 C300 610 220 600 200 520 Z" fill="#4a4a52" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>',
         '<ellipse cx="275" cy="525" rx="62" ry="38" fill="#0a0a12"/><ellipse cx="525" cy="525" rx="62" ry="38" fill="#0a0a12"/>',
         '<path d="M230 200 C270 150 320 130 360 125" stroke="#fff" stroke-width="14" fill="none" opacity="0.35" stroke-linecap="round"/>']
    rr = random.Random(2)
    for _ in range(30):
        b.append(f'<circle cx="{rr.uniform(200, 600):.0f}" cy="{rr.uniform(160, 440):.0f}" r="{rr.uniform(4, 10):.0f}" fill="#8a4a2a" opacity="0.45"/>')
    guardar(nombre, "".join(b), w, h, d)


def vikingo(nombre="vikingo", casco="redondo"):
    """Guerrero vikingo cartoon de frente con escudo redondo (lienzo 560x1000). casco: redondo | cuernos | alas."""
    w, h = 560, 1000
    b = [sombra(280, 985, 200, 16),
         f'<rect x="200" y="700" width="70" height="270" rx="30" fill="#5a3a22" stroke="{OL}" stroke-width="10"/>',
         f'<rect x="290" y="700" width="70" height="270" rx="30" fill="#5a3a22" stroke="{OL}" stroke-width="10"/>',
         f'<path d="M150 420 C150 360 200 330 280 330 C360 330 410 360 410 420 L420 740 L140 740 Z" fill="#3a6a4a" stroke="{OL}" stroke-width="11"/>',
         f'<rect x="140" y="600" width="280" height="40" fill="#6a4a2a" stroke="{OL}" stroke-width="8"/>',
         f'<circle cx="280" cy="250" r="110" fill="#ffd0b0" stroke="{OL}" stroke-width="11"/>',
         f'<path d="M175 270 C170 420 240 470 280 470 C320 470 390 420 385 270 C350 330 210 330 175 270 Z" fill="#d8782a" stroke="{OL}" stroke-width="10"/>',
         f'<circle cx="240" cy="245" r="12" fill="{OL}"/><circle cx="320" cy="245" r="12" fill="{OL}"/>',
         f'<path d="M230 300 Q280 280 330 300" stroke="#b8541a" stroke-width="16" fill="none" stroke-linecap="round"/>']
    if casco == "cuernos":
        b += [f'<path d="M190 200 C120 190 70 120 80 30 C120 110 160 140 210 150 Z" fill="#fff0d0" stroke="{OL}" stroke-width="10"/>',
              f'<path d="M370 200 C440 190 490 120 480 30 C440 110 400 140 350 150 Z" fill="#fff0d0" stroke="{OL}" stroke-width="10"/>']
    if casco == "alas":
        for s in (1, -1):
            cx = 280 - s * 105
            for k in range(3):
                b.append(f'<path d="M{cx} {190 - k * 8} C{cx - s * (80 + k * 25)} {150 - k * 40} {cx - s * (110 + k * 30)} {70 - k * 25} {cx - s * (95 + k * 30)} {20 - k * 5} '
                         f'C{cx - s * (60 + k * 15)} {90 - k * 25} {cx - s * 30} {150 - k * 15} {cx} {190 - k * 8} Z" fill="#ffffff" stroke="{OL}" stroke-width="8"/>')
    color = "#5a5a62" if casco == "redondo" else "#b8c0cc"
    b += [f'<path d="M165 225 C165 100 230 60 280 60 C330 60 395 100 395 225 Z" fill="{color}" stroke="{OL}" stroke-width="11"/>',
          f'<path d="M280 60 L280 225" stroke="{OL}" stroke-width="7"/>']
    if casco == "redondo":
        b.append(f'<path d="M180 222 L380 222 L372 256 C360 290 310 290 300 262 L292 245 L292 320 L268 320 L268 245 L260 262 C250 290 200 290 188 256 Z" fill="#4a4a52" stroke="{OL}" stroke-width="8"/>')
        b.append('<ellipse cx="236" cy="252" rx="26" ry="16" fill="#0a0a12" opacity="0.6"/><ellipse cx="324" cy="252" rx="26" ry="16" fill="#0a0a12" opacity="0.6"/>')
    # escudo
    b += [f'<circle cx="420" cy="560" r="150" fill="#c83a3a" stroke="{OL}" stroke-width="12"/>',
          '<path d="M420 410 L420 710 M270 560 L570 560" stroke="#f4e0b0" stroke-width="26"/>',
          f'<circle cx="420" cy="560" r="40" fill="#b8c0cc" stroke="{OL}" stroke-width="9"/>']
    guardar(nombre, "".join(b), w, h)


def drakkar_c(nombre="drakkar_c"):
    """Barco vikingo cartoon de perfil (lienzo 1000x700)."""
    w, h = 1000, 700
    b = [f'<path d="M500 80 L500 470" stroke="{OL}" stroke-width="22"/><path d="M500 80 L500 470" stroke="#8a5a2a" stroke-width="12"/>',
         f'<path d="M300 110 L700 110 L680 420 L320 420 Z" fill="#f4e8d0" stroke="{OL}" stroke-width="11" stroke-linejoin="round"/>']
    for k in range(4):
        b.append(f'<path d="M{330 + k * 90} 112 L{340 + k * 85} 418" stroke="#d83a3a" stroke-width="44" opacity="0.85"/>')
    b += [f'<path d="M40 420 C60 560 200 620 500 620 C800 620 940 560 960 420 Z" fill="#8a5a2a" stroke="{OL}" stroke-width="12"/>',
          f'<path d="M40 420 C20 330 60 250 120 220 C100 290 110 360 150 420 Z" fill="#8a5a2a" stroke="{OL}" stroke-width="10"/>',
          f'<path d="M960 420 C990 330 950 260 900 240 C910 300 900 370 860 420 Z" fill="#8a5a2a" stroke="{OL}" stroke-width="10"/>',
          '<path d="M80 470 C200 520 800 520 920 470 M70 520 C220 575 780 575 930 520" stroke="#5a3418" stroke-width="8" fill="none"/>']
    for k in range(7):
        x = 180 + k * 105
        b.append(f'<circle cx="{x}" cy="440" r="40" fill="{["#e8c040", "#3a6ad8", "#c83a3a"][k % 3]}" stroke="{OL}" stroke-width="8"/>')
    guardar(nombre, "".join(b), w, h)


def bg_fiordo(nombre="bg_fiordo", noche=False):
    c = ("#0a1430", "#3a4a7a") if noche else ("#8ac8ff", "#e8f4ff")
    d = lg(nombre + "_c", (0, c[0]), (1, c[1])) + lg(nombre + "_a", (0, "#3a7ab8"), (1, "#0a2a5a"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>',
         '<path d="M0 900 L180 480 L320 700 L460 420 L620 760 L760 500 L900 720 L1080 460 L1080 1100 L0 1100 Z" fill="#5a6a8a"/>',
         '<path d="M180 480 L230 600 L140 580 Z M460 420 L520 540 L410 540 Z M760 500 L810 610 L720 600 Z M1080 460 L1080 560 L1010 560 Z" fill="#ffffff"/>',
         '<path d="M0 1050 L240 760 L400 980 L560 820 L760 1050 L900 860 L1080 1000 L1080 1200 L0 1200 Z" fill="#2a4a3a"/>',
         f'<rect x="0" y="1150" width="1080" height="770" fill="url(#{nombre}_a)"/>',
         '<path d="M0 1250 Q270 1230 540 1250 T1080 1250 M0 1400 Q270 1380 540 1400 T1080 1400 M0 1600 Q270 1580 540 1600 T1080 1600" stroke="#ffffff" stroke-width="6" opacity="0.3" fill="none"/>']
    if noche:
        rr = random.Random(8)
        b += [f'<circle cx="{rr.uniform(0, 1080):.0f}" cy="{rr.uniform(0, 450):.0f}" r="{rr.uniform(1.5, 4):.1f}" fill="#fff"/>' for _ in range(90)]
    guardar(nombre, "".join(b), 1080, 1920, d)


def bg_excavacion(nombre="bg_excavacion"):
    """Corte de tierra por capas con un hoyo de excavación y cuerdas de cuadrícula."""
    d = lg("ex_c", (0, "#a8d0f0"), (1, "#e8f4ff"))
    b = ['<rect width="1080" height="1920" fill="url(#ex_c)"/>',
         '<rect x="0" y="600" width="1080" height="80" fill="#5aa04a"/>']
    capas = ["#8a5a30", "#a8743e", "#7a4a26", "#b8885a", "#6a3e1e", "#9a6a3e"]
    for k, c in enumerate(capas):
        y = 680 + k * 210
        b.append(f'<path d="M0 {y} Q270 {y - 20} 540 {y} T1080 {y} L1080 1920 L0 1920 Z" fill="{c}"/>')
    rr = random.Random(6)
    for _ in range(60):
        b.append(f'<ellipse cx="{rr.uniform(0, 1080):.0f}" cy="{rr.uniform(700, 1900):.0f}" rx="{rr.uniform(8, 22):.0f}" ry="{rr.uniform(5, 12):.0f}" fill="#4a2a12" opacity="0.5"/>')
    b += ['<path d="M200 680 L200 1500 L880 1500 L880 680" fill="#3a2410" opacity="0.35"/>',
          '<path d="M200 680 L880 680 M200 900 L880 900 M200 1120 L880 1120 M430 680 L430 1500 M650 680 L650 1500" stroke="#f4f0e0" stroke-width="4" opacity="0.7"/>']
    guardar(nombre, "".join(b), 1080, 1920, d)


def pala(nombre="pala"):
    w, h = 240, 700
    b = [f'<rect x="105" y="20" width="30" height="460" rx="12" fill="#a8743e" stroke="{OL}" stroke-width="8"/>',
         f'<rect x="70" y="10" width="100" height="40" rx="18" fill="#3a3a4a" stroke="{OL}" stroke-width="8"/>',
         f'<path d="M50 470 L190 470 L180 640 Q120 690 60 640 Z" fill="#9aa2b2" stroke="{OL}" stroke-width="10" stroke-linejoin="round"/>']
    guardar(nombre, "".join(b), w, h)


def bg_teatro(nombre="bg_teatro"):
    """Escenario de ópera: telón rojo, candilejas, foco y suelo de madera."""
    d = lg("te_t", (0, "#e0303a"), (1, "#7a0a14")) + rg("te_f", (0, "#fff4c8", 0.9), (1, "#fff4c8", 0), cx=0.5, cy=0.5)
    b = ['<rect width="1080" height="1920" fill="#1a0a10"/>',
         '<rect x="140" y="300" width="800" height="1050" fill="#2a1a2a"/>',
         '<ellipse cx="540" cy="1200" rx="380" ry="420" fill="url(#te_f)"/>',
         '<path d="M0 0 L1080 0 L1080 260 Q810 330 540 260 Q270 330 0 260 Z" fill="url(#te_t)" stroke="#1b1b2b" stroke-width="10"/>',
         '<path d="M0 0 L240 0 C200 600 260 1100 180 1400 L0 1400 Z" fill="url(#te_t)" stroke="#1b1b2b" stroke-width="10"/>',
         '<path d="M1080 0 L840 0 C880 600 820 1100 900 1400 L1080 1400 Z" fill="url(#te_t)" stroke="#1b1b2b" stroke-width="10"/>',
         '<path d="M60 0 C40 500 90 1000 50 1400 M150 0 C120 500 170 1000 120 1400 M1020 0 C1040 500 990 1000 1030 1400 M930 0 C960 500 910 1000 960 1400" stroke="#7a0a14" stroke-width="12" fill="none"/>',
         '<rect x="0" y="1350" width="1080" height="570" fill="#6a3a1a"/>']
    for x in range(0, 1080, 90):
        b.append(f'<path d="M{x} 1350 L{x - 120} 1920" stroke="#4a2410" stroke-width="5"/>')
    b += ['<rect x="0" y="1340" width="1080" height="30" fill="#e8c040" stroke="#1b1b2b" stroke-width="8"/>']
    for x in range(80, 1080, 160):
        b.append(f'<ellipse cx="{x}" cy="1350" rx="34" ry="14" fill="#fff4b0"/>')
    guardar(nombre, "".join(b), 1080, 1920, d)


def boceto(nombre="boceto"):
    """Hoja de papel con el boceto a lápiz de un guerrero con casco de cuernos (lienzo 640x820)."""
    w, h = 640, 820
    b = [f'<path d="M40 40 L600 30 L610 780 L30 790 Z" fill="#fbf3e0" stroke="{OL}" stroke-width="10" stroke-linejoin="round"/>',
         '<path d="M320 210 C230 210 210 300 220 360 L420 360 C430 300 410 210 320 210 Z" fill="none" stroke="#4a4a5a" stroke-width="7"/>',
         '<path d="M230 300 C160 290 120 220 130 140 C160 210 200 240 240 250 M410 300 C480 290 520 220 510 140 C480 210 440 240 400 250" fill="none" stroke="#4a4a5a" stroke-width="7"/>',
         '<circle cx="320" cy="420" r="70" fill="none" stroke="#4a4a5a" stroke-width="6"/>',
         '<path d="M250 480 C240 560 260 680 230 740 M390 480 C400 560 380 680 410 740 M250 520 L390 520" fill="none" stroke="#4a4a5a" stroke-width="6"/>',
         '<path d="M140 150 L150 160 M500 140 L510 150 M300 200 L340 205" stroke="#8a8a9a" stroke-width="3"/>',
         '<path d="M80 100 L240 95" stroke="#8a8a9a" stroke-width="5"/>',
         '<text x="470" y="760" font-family="Georgia" font-style="italic" font-size="44" fill="#4a4a5a">1876</text>']
    guardar(nombre, "".join(b), w, h)


def lapiz(nombre="lapiz"):
    w, h = 600, 120
    b = [f'<path d="M40 60 L120 25 L540 25 L540 95 L120 95 Z" fill="#ffc83a" stroke="{OL}" stroke-width="9" stroke-linejoin="round"/>',
         f'<path d="M40 60 L120 25 L120 95 Z" fill="#f4d8b0" stroke="{OL}" stroke-width="8"/><path d="M40 60 L70 47 L70 73 Z" fill="{OL}"/>',
         f'<rect x="510" y="25" width="70" height="70" rx="10" fill="#ff8aa8" stroke="{OL}" stroke-width="8"/>']
    guardar(nombre, "".join(b), w, h)


def casco_vekso(nombre="casco_vekso"):
    """Casco de bronce de la Edad del Bronce, inspirado en los de Veksø: cúpula, cuernos curvos, ojos y pico (lienzo 900x700)."""
    w, h = 900, 700
    d = lg("vk_b", (0, "#e8b860"), (0.5, "#b8823a"), (1, "#6a4a1a"))
    b = [f'<path d="M280 360 C180 360 120 300 120 200 C120 120 180 90 230 110 C190 150 200 250 290 280 Z" fill="url(#vk_b)" stroke="{OL}" stroke-width="12"/>',
         f'<path d="M620 360 C720 360 780 300 780 200 C780 120 720 90 670 110 C710 150 700 250 610 280 Z" fill="url(#vk_b)" stroke="{OL}" stroke-width="12"/>',
         f'<path d="M230 520 C230 300 330 220 450 220 C570 220 670 300 670 520 Z" fill="url(#vk_b)" stroke="{OL}" stroke-width="14"/>',
         f'<path d="M450 220 L450 520" stroke="#6a4a1a" stroke-width="16"/>',
         f'<circle cx="370" cy="400" r="34" fill="#f4d890" stroke="{OL}" stroke-width="8"/><circle cx="530" cy="400" r="34" fill="#f4d890" stroke="{OL}" stroke-width="8"/>',
         f'<circle cx="370" cy="400" r="12" fill="{OL}"/><circle cx="530" cy="400" r="12" fill="{OL}"/>',
         f'<path d="M420 440 L480 440 L450 500 Z" fill="#f4d890" stroke="{OL}" stroke-width="8" stroke-linejoin="round"/>',
         f'<rect x="210" y="500" width="480" height="50" rx="18" fill="#9a6a2a" stroke="{OL}" stroke-width="12"/>',
         '<path d="M290 330 C320 270 370 250 420 240" stroke="#fff4c8" stroke-width="16" fill="none" opacity="0.5" stroke-linecap="round"/>']
    for x in range(250, 680, 50):
        b.append(f'<circle cx="{x}" cy="525" r="8" fill="#f4d890"/>')
    rr = random.Random(11)
    for _ in range(25):
        b.append(f'<circle cx="{rr.uniform(260, 640):.0f}" cy="{rr.uniform(260, 500):.0f}" r="{rr.uniform(5, 12):.0f}" fill="#3a8a6a" opacity="0.45"/>')
    guardar(nombre, "".join(b), w, h, d)


def bg_turbera(nombre="bg_turbera"):
    d = lg("tu_c", (0, "#c8d8c0"), (1, "#f0f0e0")) + lg("tu_a", (0, "#3a3a1a"), (1, "#1a1a0a"))
    b = ['<rect width="1080" height="1920" fill="url(#tu_c)"/>',
         '<path d="M0 900 Q300 820 600 880 T1080 860 L1080 1100 L0 1100 Z" fill="#7a8a4a"/>',
         '<rect x="0" y="1050" width="1080" height="870" fill="#5a4a2a"/>',
         '<ellipse cx="540" cy="1350" rx="460" ry="140" fill="url(#tu_a)"/>',
         '<path d="M160 1340 Q540 1300 920 1340" stroke="#8a9a6a" stroke-width="6" fill="none" opacity="0.6"/>']
    rr = random.Random(12)
    for _ in range(40):
        x = rr.uniform(0, 1080)
        b.append(f'<path d="M{x:.0f} 1060 l{rr.uniform(-20, 20):.0f} -{rr.uniform(40, 110):.0f}" stroke="#a8b870" stroke-width="6" stroke-linecap="round"/>')
    guardar(nombre, "".join(b), 1080, 1920, d)


def bg_papel(nombre="bg_papel"):
    d = lg("pa_c", (0, "#f8eed8"), (1, "#e8d4b0"))
    b = ['<rect width="1080" height="1920" fill="url(#pa_c)"/>']
    rr = random.Random(13)
    for _ in range(80):
        b.append(f'<circle cx="{rr.uniform(0, 1080):.0f}" cy="{rr.uniform(0, 1920):.0f}" r="{rr.uniform(10, 40):.0f}" fill="#c8a878" opacity="0.08"/>')
    guardar(nombre, "".join(b), 1080, 1920, d)


def banda_sub(nombre="banda_sub"):
    """Franja oscura difuminada detrás del subtítulo karaoke, para fondos claros (cocina, laboratorio, módulo, papel)."""
    d = lg("bs_g", (0, "#0a0f24" + "00"), (0.3, "#0a0f24"), (0.7, "#0a0f24"), (1, "#0a0f24" + "00"))
    d = ('<linearGradient id="bs_g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a0f24" stop-opacity="0"/>'
         '<stop offset="0.3" stop-color="#0a0f24" stop-opacity="0.62"/><stop offset="0.7" stop-color="#0a0f24" stop-opacity="0.62"/>'
         '<stop offset="1" stop-color="#0a0f24" stop-opacity="0"/></linearGradient>')
    guardar(nombre, '<rect width="1080" height="440" fill="url(#bs_g)"/>', 1080, 440, d)


# ====================================================================== GENERAR
def generar(dirsvg):
    m = _mod("lotes/2026-11-23-tarde/generadores/ilus_1123t.py", "_ilus_1123t_24")
    m.generar(dirsvg)
    ilus.OUT = dirsvg
    banda_sub()
    # 01
    gato(); gato("gato_lengua", lengua=True)
    gato("tigre", ("#ff9a2a", "#d8641a"), "#1b1b2b", "tigre", ojos="#ffd23f")
    gato("guepardo", ("#ffd27a", "#e0a848"), "#2a1a0a", "manchas", ojos="#e0a020")
    gato("gato_gris", ("#b8c0d0", "#7a849a"), "#4a5468", "rayas", ojos="#ffd23f")
    bg_cocina(); pastel(); caramelo(); helado(); filete(); azucar(); lengua(); microscopio(); cuenco(); bg_lab_claro()
    pieza("pieza_a", "#3a8aff", "izq"); pieza("pieza_b", "#ff5aa8", "der"); pieza("pieza_b_rota", "#ff5aa8", "der", rota=True)
    adn(); adn("adn_roto", hueco=True)
    # 02
    cara_astro(); cara_astro("cara_hinchada", hinchada=True, nariz_roja=True); bola_agua(); lagrima(); estacion(); bg_modulo()
    molecula_agua(); toalla(); cuerpo_flujo(); cuerpo_flujo("cuerpo_espacio", espacio=True); panuelo(); botella()
    # 03
    casco_cuernos(); casco_cuernos("casco_alas", alas=True); casco_cuernos("casco_sin", cuernos=False); cuerno(); cuerno("cuerno_d", espejo=True)
    casco_gjermundbu(); vikingo(); vikingo("vikingo_cuernos", "cuernos"); vikingo("cantante_alas", "alas"); drakkar_c()
    bg_fiordo(); bg_fiordo("bg_fiordo_noche", noche=True); bg_excavacion(); pala(); bg_teatro(); boceto(); lapiz(); casco_vekso(); bg_turbera(); bg_papel()
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
