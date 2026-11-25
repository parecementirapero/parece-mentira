"""Ilustraciones del lote 2026-11-25-manana (Nico, con el agente): 01 el Hubble nació miope, 02 por qué se te arrugan
los dedos en el agua, 03 el olivo que conoció a Roma. Estilo cartoon con contorno grueso (el de los lotes 2026-11-23-tarde
y 2026-11-24-tarde, que se reutilizan enteros). Todo dibujado aquí, sin logos ni personas reales.
Uso: python3 ilus_1125m.py DIR_SVG"""
import importlib.util, math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg  # noqa: E402

OL = "#1b1b2b"


def _mod(rel, nombre):
    s = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, rel))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def sombra(cx, cy, rx, ry=None, op=0.3):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry or rx * 0.12}" fill="#000" opacity="{op}"/>'


# ====================================================================== 01 · Hubble
def _panel(x, y, w=150, h=330):
    b = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="url(#hb_pan)" stroke="{OL}" stroke-width="9"/>']
    for i in range(1, 6):
        b.append(f'<path d="M{x} {y + i * h / 6:.0f} L{x + w} {y + i * h / 6:.0f}" stroke="#0a1a4a" stroke-width="4"/>')
    b.append(f'<path d="M{x + w / 2} {y} L{x + w / 2} {y + h}" stroke="#0a1a4a" stroke-width="4"/>')
    b.append(f'<path d="M{x + 14} {y + 14} L{x + w * 0.45} {y + 14} L{x + 14} {y + h * 0.4} Z" fill="#fff" opacity="0.18"/>')
    return "".join(b)


def hubble(nombre="hubble"):
    """Telescopio espacial de dibujo, tubo en vertical con la boca arriba y la tapa abierta (lienzo 760x900)."""
    d = (lg("hb_tubo", (0, "#8e98ad"), (0.3, "#eef2fa"), (0.62, "#c3cbdb"), (1, "#6f7890"), x2=1, y2=0)
         + lg("hb_oro", (0, "#b98a2a"), (0.35, "#ffe08a"), (1, "#a8741a"), x2=1, y2=0)
         + lg("hb_pan", (0, "#3a6aff"), (1, "#16308a")) + lg("hb_boca", (0, "#05060f"), (1, "#27304f")))
    b = [  # brazos y paneles
        f'<rect x="150" y="470" width="460" height="22" rx="8" fill="#9aa3b8" stroke="{OL}" stroke-width="8"/>',
        _panel(20, 310), _panel(590, 310),
        # tapa abierta
        f'<path d="M258 150 L190 20 L250 6 L330 120 Z" fill="url(#hb_tubo)" stroke="{OL}" stroke-width="10" stroke-linejoin="round"/>',
        # tubo delantero
        f'<rect x="250" y="120" width="260" height="380" rx="18" fill="url(#hb_tubo)" stroke="{OL}" stroke-width="12"/>',
        f'<ellipse cx="380" cy="130" rx="130" ry="44" fill="url(#hb_boca)" stroke="{OL}" stroke-width="12"/>',
        '<ellipse cx="380" cy="140" rx="84" ry="22" fill="#5a78c8" opacity="0.55"/>',
        '<ellipse cx="350" cy="134" rx="26" ry="7" fill="#cfe0ff" opacity="0.8"/>',
        f'<path d="M250 250 L510 250 M250 330 L510 330" stroke="{OL}" stroke-width="7" opacity="0.55"/>',
        # cuerpo trasero dorado
        f'<rect x="218" y="490" width="324" height="330" rx="26" fill="url(#hb_oro)" stroke="{OL}" stroke-width="12"/>',
        f'<path d="M218 600 L542 600 M218 700 L542 700" stroke="{OL}" stroke-width="7" opacity="0.5"/>',
        f'<rect x="300" y="630" width="70" height="50" rx="8" fill="#fff3c0" stroke="{OL}" stroke-width="6"/>',
        f'<rect x="270" y="820" width="220" height="40" rx="12" fill="#8e98ad" stroke="{OL}" stroke-width="10"/>',
        # antena
        f'<path d="M542 560 L640 600" stroke="{OL}" stroke-width="10" stroke-linecap="round"/>',
        f'<circle cx="652" cy="606" r="26" fill="#eef2fa" stroke="{OL}" stroke-width="8"/>',
        '<rect x="262" y="140" width="34" height="340" rx="14" fill="#fff" opacity="0.4"/>']
    guardar(nombre, "".join(b), 760, 900, d)


def gafas(nombre="gafas"):
    d = lg("gf_c", (0, "#bfe6ff"), (1, "#6fb4f0"))
    b = [f'<circle cx="160" cy="150" r="118" fill="url(#gf_c)" fill-opacity="0.55" stroke="{OL}" stroke-width="26"/>',
         f'<circle cx="440" cy="150" r="118" fill="url(#gf_c)" fill-opacity="0.55" stroke="{OL}" stroke-width="26"/>',
         f'<path d="M270 130 Q300 96 330 130" stroke="{OL}" stroke-width="24" fill="none" stroke-linecap="round"/>',
         '<circle cx="160" cy="150" r="118" fill="none" stroke="#ff4d5e" stroke-width="12"/>',
         '<circle cx="440" cy="150" r="118" fill="none" stroke="#ff4d5e" stroke-width="12"/>',
         '<path d="M96 96 L150 70 M380 96 L434 70" stroke="#fff" stroke-width="16" stroke-linecap="round" opacity="0.85"/>']
    guardar(nombre, "".join(b), 600, 300, d)


def _galaxia(cx, cy, r, sem=4):
    rr = random.Random(sem)
    b = [f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * 0.62:.0f}" fill="url(#gx_h)"/>']
    for brazo in range(2):
        pts = []
        for i in range(60):
            a = i / 60 * 3.6 * math.pi / 2 + brazo * math.pi
            rad = r * (0.12 + 0.88 * i / 60)
            pts.append((cx + rad * math.cos(a), cy + rad * 0.62 * math.sin(a)))
        dd = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
        b.append(f'<path d="{dd}" stroke="#bcd0ff" stroke-width="{r * 0.16:.0f}" fill="none" stroke-linecap="round" opacity="0.5"/>')
        b.append(f'<path d="{dd}" stroke="#ffffff" stroke-width="{r * 0.05:.0f}" fill="none" stroke-linecap="round" opacity="0.85"/>')
        for x, y in pts[10::4]:
            b.append(f'<circle cx="{x + rr.uniform(-14, 14):.0f}" cy="{y + rr.uniform(-12, 12):.0f}" r="{rr.uniform(3, 7):.0f}" fill="{rr.choice(["#ff9ad8", "#9ad8ff", "#fff"])}"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 0.2:.0f}" fill="url(#gx_n)"/>')
    for _ in range(46):
        b.append(f'<circle cx="{rr.uniform(cx - r * 1.3, cx + r * 1.3):.0f}" cy="{rr.uniform(cy - r * 1.3, cy + r * 1.3):.0f}" r="{rr.uniform(1.5, 4):.1f}" fill="#fff" opacity="{rr.uniform(0.5, 1):.2f}"/>')
    return "".join(b)


def foto(nombre="foto_nitida", borrosa=False):
    """Foto enmarcada de una galaxia (lienzo 700x760). borrosa=True: la misma, desenfocada y con halo."""
    d = (rg("gx_h", (0, "#8aa8ff", 0.55), (1, "#8aa8ff", 0)) + rg("gx_n", (0, "#fff8d8", 1), (0.5, "#ffd88a", 0.9), (1, "#ffd88a", 0))
         + lg("gx_bg", (0, "#070a1e"), (1, "#141a3e")) + '<filter id="gx_b" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="26"/></filter>'
         + '<clipPath id="gx_c"><rect x="50" y="50" width="600" height="600" rx="10"/></clipPath>')
    g = _galaxia(350, 350, 230)
    if borrosa:
        g = (f'<g filter="url(#gx_b)">{g}{g}</g>'
             '<circle cx="350" cy="350" r="150" fill="none" stroke="#cfe0ff" stroke-width="26" opacity="0.22" filter="url(#blur20)"/>')
    b = [sombra(350, 740, 300, 16, 0.35),
         f'<rect x="20" y="20" width="660" height="700" rx="18" fill="#f6f1e6" stroke="{OL}" stroke-width="12"/>',
         '<rect x="50" y="50" width="600" height="600" rx="10" fill="url(#gx_bg)"/>',
         f'<g clip-path="url(#gx_c)">{g}</g>',
         f'<rect x="50" y="50" width="600" height="600" rx="10" fill="none" stroke="{OL}" stroke-width="8"/>',
         f'<rect x="250" y="670" width="200" height="22" rx="10" fill="{OL}" opacity="0.25"/>']
    guardar(nombre, "".join(b), 700, 760, d)


def estrella(nombre="estrella_nitida", borrosa=False):
    d = rg("es_h", (0, "#ffffff", 1), (0.25, "#cfe0ff", 0.7), (1, "#8aa8ff", 0))
    if borrosa:
        b = ['<circle cx="300" cy="300" r="270" fill="url(#es_h)" opacity="0.75"/>',
             '<circle cx="300" cy="300" r="170" fill="#dfe8ff" opacity="0.5" filter="url(#blur40)"/>',
             '<circle cx="300" cy="300" r="200" fill="none" stroke="#cfe0ff" stroke-width="22" opacity="0.3" filter="url(#blur20)"/>',
             '<circle cx="300" cy="300" r="90" fill="#fff" opacity="0.8" filter="url(#blur20)"/>']
    else:
        b = ['<circle cx="300" cy="300" r="120" fill="url(#es_h)"/>',
             '<path d="M300 20 L316 284 L580 300 L316 316 L300 580 L284 316 L20 300 L284 284 Z" fill="#fff"/>',
             '<path d="M300 150 L312 288 L450 300 L312 312 L300 450 L288 312 L150 300 L288 288 Z" fill="#fff" transform="rotate(45 300 300)" opacity="0.8"/>',
             '<circle cx="300" cy="300" r="34" fill="#fff"/>']
    guardar(nombre, "".join(b), 600, 600, d)


def espejo_hubble(nombre="espejo_hubble"):
    d = (rg("eh_c", (0, "#f4fbff", 1), (0.6, "#a8c8e8", 1), (1, "#5a7aa8", 1), cx=0.38, cy=0.34, r=0.75)
         + lg("eh_a", (0, "#d0d6e4"), (1, "#7a8298")))
    b = [sombra(350, 690, 280, 22, 0.35),
         f'<circle cx="350" cy="350" r="330" fill="url(#eh_a)" stroke="{OL}" stroke-width="14"/>',
         f'<circle cx="350" cy="350" r="296" fill="url(#eh_c)" stroke="{OL}" stroke-width="8"/>',
         '<path d="M140 260 A230 230 0 0 1 330 100" stroke="#fff" stroke-width="34" fill="none" stroke-linecap="round" opacity="0.75"/>',
         '<path d="M110 370 A250 250 0 0 1 124 300" stroke="#fff" stroke-width="22" fill="none" stroke-linecap="round" opacity="0.6"/>',
         f'<circle cx="350" cy="350" r="64" fill="#11162c" stroke="{OL}" stroke-width="10"/>',
         '<circle cx="350" cy="350" r="296" fill="none" stroke="#fff" stroke-width="6" opacity="0.35"/>']
    guardar(nombre, "".join(b), 700, 720, d)


def espejo_corte(nombre="espejo_corte"):
    """Sección del espejo: curva ideal (lima, discontinua) y curva real, más plana en los bordes (exagerado)."""
    d = lg("ec_v", (0, "#cfe6ff"), (1, "#6f93c8"))
    real = "M60 150 Q500 420 940 150 L940 420 L60 420 Z"
    b = [f'<path d="{real}" fill="url(#ec_v)" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>',
         '<path d="M60 96 Q500 440 940 96" fill="none" stroke="#7dff3a" stroke-width="12" stroke-dasharray="26 18" stroke-linecap="round"/>',
         '<path d="M80 180 Q500 420 920 180" fill="none" stroke="#fff" stroke-width="8" opacity="0.6"/>',
         '<path d="M60 96 L60 150 M940 96 L940 150" stroke="#ff3d3d" stroke-width="16" stroke-linecap="round"/>']
    guardar(nombre, "".join(b), 1000, 460, d)


def pelo(nombre="pelo"):
    d = lg("pl_g", (0, "#8a5a2e"), (0.3, "#d8a468"), (1, "#5a3414"))
    b = [f'<rect x="0" y="60" width="1000" height="240" rx="6" fill="url(#pl_g)" stroke="{OL}" stroke-width="12"/>']
    for x in range(-40, 1000, 110):
        b.append(f'<path d="M{x} 300 Q{x + 70} 180 {x + 150} 60" stroke="#4a2a10" stroke-width="7" fill="none" opacity="0.55"/>')
    b.append('<rect x="0" y="78" width="1000" height="34" fill="#fff" opacity="0.28"/>')
    guardar(nombre, "".join(b), 1000, 360, d)


def aparato_medir(nombre="aparato_medir", mal=False):
    """Aparato de comprobar el espejo: tubo con dos lentes; mal=True: una lente desplazada, en rojo."""
    d = lg("am_t", (0, "#5a6480"), (0.4, "#c8d0e4"), (1, "#4a5470"), x2=1, y2=0) + lg("am_l", (0, "#dff4ff"), (1, "#7ac0f0"))
    y2 = 470 if mal else 400
    b = [sombra(250, 780, 190, 18),
         f'<rect x="130" y="60" width="240" height="700" rx="26" fill="url(#am_t)" stroke="{OL}" stroke-width="12"/>',
         f'<rect x="160" y="100" width="180" height="620" rx="12" fill="#11162c"/>',
         f'<ellipse cx="250" cy="200" rx="84" ry="24" fill="url(#am_l)" stroke="{OL}" stroke-width="8"/>',
         f'<ellipse cx="250" cy="{y2}" rx="84" ry="24" fill="{"#ff8a8a" if mal else "url(#am_l)"}" stroke="{"#ff3d3d" if mal else OL}" stroke-width="{12 if mal else 8}"/>',
         f'<ellipse cx="250" cy="620" rx="84" ry="24" fill="url(#am_l)" stroke="{OL}" stroke-width="8"/>',
         '<path d="M250 100 L250 720" stroke="#7dff3a" stroke-width="5" stroke-dasharray="12 12" opacity="0.8"/>',
         '<rect x="146" y="80" width="26" height="660" rx="12" fill="#fff" opacity="0.3"/>']
    if mal:
        b.append('<path d="M110 400 L390 400" stroke="#ffffff" stroke-width="5" stroke-dasharray="10 10" opacity="0.8"/>')
    guardar(nombre, "".join(b), 500, 820, d)


def transbordador(nombre="transbordador"):
    d = (lg("tb_c", (0, "#b8c0d0"), (0.35, "#ffffff"), (1, "#a0a8bc"), x2=1, y2=0)
         + lg("tb_f", (0, "#fff6c0"), (0.4, "#ffb02a"), (1, "#ff4a1a")))
    b = [f'<path d="M210 760 Q250 1010 300 1040 Q350 1010 390 760 Z" fill="url(#tb_f)" opacity="0.95"/>',
         '<path d="M250 760 Q280 930 300 950 Q320 930 350 760 Z" fill="#fff8d8"/>',
         # alas
         f'<path d="M210 380 L40 700 L40 760 L210 760 Z M390 380 L560 700 L560 760 L390 760 Z" fill="#e6eaf2" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>',
         f'<path d="M40 730 L210 730 M390 730 L560 730" stroke="{OL}" stroke-width="20"/>',
         # fuselaje
         f'<path d="M300 20 Q400 120 400 320 L400 770 L200 770 L200 320 Q200 120 300 20 Z" fill="url(#tb_c)" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>',
         f'<path d="M300 20 Q352 76 372 150 L228 150 Q248 76 300 20 Z" fill="{OL}"/>',
         f'<path d="M244 196 L356 196 L344 246 L256 246 Z" fill="#24304e" stroke="{OL}" stroke-width="7"/>',
         '<path d="M252 204 L296 204 L290 238 L262 238 Z" fill="#7ac0f0" opacity="0.8"/>',
         f'<rect x="232" y="330" width="136" height="320" rx="14" fill="#d2d8e4" stroke="{OL}" stroke-width="7"/>',
         f'<path d="M300 330 L300 650" stroke="{OL}" stroke-width="5"/>',
         # cola
         f'<path d="M286 560 L300 440 L314 560 L314 770 L286 770 Z" fill="#e6eaf2" stroke="{OL}" stroke-width="9" stroke-linejoin="round"/>',
         f'<rect x="216" y="766" width="52" height="36" rx="8" fill="#5a6480" stroke="{OL}" stroke-width="8"/>',
         f'<rect x="332" y="766" width="52" height="36" rx="8" fill="#5a6480" stroke="{OL}" stroke-width="8"/>',
         '<rect x="214" y="250" width="26" height="500" rx="12" fill="#fff" opacity="0.5"/>']
    guardar(nombre, "".join(b), 600, 1060, d)


def espejito(nombre="espejito"):
    d = rg("ej_c", (0, "#ffffff", 1), (0.6, "#a8d4f4", 1), (1, "#5a8ac0", 1), cx=0.36, cy=0.32, r=0.8) + lg("ej_b", (0, "#c8d0e4"), (1, "#6a7490"))
    b = [f'<rect x="170" y="330" width="60" height="230" rx="16" fill="url(#ej_b)" stroke="{OL}" stroke-width="10"/>',
         f'<rect x="110" y="540" width="180" height="50" rx="14" fill="url(#ej_b)" stroke="{OL}" stroke-width="10"/>',
         f'<circle cx="200" cy="200" r="170" fill="#d8b040" stroke="{OL}" stroke-width="12"/>',
         f'<circle cx="200" cy="200" r="136" fill="url(#ej_c)" stroke="{OL}" stroke-width="8"/>',
         '<path d="M110 170 A100 100 0 0 1 190 96" stroke="#fff" stroke-width="22" fill="none" stroke-linecap="round" opacity="0.85"/>']
    guardar(nombre, "".join(b), 400, 620, d)


def billetes(nombre="billetes"):
    d = lg("bi_g", (0, "#9ae07a"), (1, "#4aa040"))
    b = [sombra(300, 400, 250, 20)]
    for i in range(6):
        y = 300 - i * 44
        b += [f'<rect x="{40 + (i % 2) * 14}" y="{y}" width="500" height="92" rx="12" fill="url(#bi_g)" stroke="{OL}" stroke-width="9"/>']
    y = 80
    b += [f'<rect x="72" y="{y + 16}" width="436" height="60" rx="8" fill="none" stroke="#2a6a2a" stroke-width="5"/>',
          f'<circle cx="290" cy="{y + 46}" r="30" fill="#d8f4c0" stroke="#2a6a2a" stroke-width="6"/>',
          f'<path d="M298 {y + 34} Q280 {y + 28} 280 {y + 40} Q280 {y + 48} 292 {y + 48} Q302 {y + 50} 300 {y + 58} Q296 {y + 66} 280 {y + 60} M290 {y + 24} L290 {y + 68}" stroke="#2a6a2a" stroke-width="5" fill="none" stroke-linecap="round"/>',
          f'<rect x="250" y="{y + 132}" width="90" height="268" fill="#f6f1e6" stroke="{OL}" stroke-width="7" opacity="0.9"/>']
    guardar(nombre, "".join(b), 600, 430, d)


# ====================================================================== 02 · dedos
PIEL = ("#ffd2ae", "#f0a882")


def _arrugas(cx, cy, w, h, n=5, col="#b86a4a", g=7):
    b = []
    for i in range(n):
        x = cx - w / 2 + w * (i + 0.5) / n
        b.append(f'<path d="M{x:.0f} {cy - h / 2:.0f} q{w / n * 0.35:.0f} {h * 0.25:.0f} 0 {h * 0.5:.0f} q{-w / n * 0.35:.0f} {h * 0.25:.0f} 0 {h * 0.5:.0f}" stroke="{col}" stroke-width="{g}" fill="none" stroke-linecap="round"/>')
    return "".join(b)


def mano(nombre="mano", arrugada=False, gotas=False, nervio=None):
    """Mano abierta de frente, palma hacia la cámara (lienzo 760x1000). nervio: None | "ok" | "cortado"."""
    d = lg("mn_p", (0, PIEL[0]), (1, PIEL[1]))
    dedos = [(120, 330, 92, 330, -14), (250, 190, 98, 440, -5), (385, 150, 100, 480, 0), (520, 200, 96, 430, 6)]
    b = [f'<path d="M560 640 Q700 560 720 440 Q726 380 680 384 Q640 390 620 470 Q600 540 520 600 Z" fill="url(#mn_p)" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>']
    for x, y, w, h, r in dedos:
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w / 2}" fill="url(#mn_p)" stroke="{OL}" stroke-width="12" transform="rotate({r} {x + w / 2} {y + h})"/>')
    b.append(f'<path d="M110 620 Q110 540 210 540 L560 540 Q640 560 630 700 Q620 900 520 960 L250 960 Q130 900 110 620 Z" fill="url(#mn_p)" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>')
    b.append('<path d="M150 600 L590 600" stroke="url(#mn_p)" stroke-width="130"/>')
    b.append('<path d="M200 690 Q330 640 470 700 M190 770 Q320 740 500 790 M300 860 Q360 780 330 690" stroke="#c88a6a" stroke-width="7" fill="none" stroke-linecap="round" opacity="0.8"/>')
    for x, y, w, h, r in dedos:
        tr = f'transform="rotate({r} {x + w / 2} {y + h})"'
        if arrugada:
            b.append(f'<g {tr}>{_arrugas(x + w / 2, y + 74, w - 26, 96, 4)}</g>')
        else:
            b.append(f'<g {tr}><path d="M{x + 22} {y + 150} Q{x + w / 2} {y + 164} {x + w - 22} {y + 150}" stroke="#c88a6a" stroke-width="6" fill="none"/>'
                     f'<ellipse cx="{x + w / 2}" cy="{y + 70}" rx="{w * 0.24:.0f}" ry="34" fill="#fff" opacity="0.28"/></g>')
    if arrugada:
        b.append(_arrugas(670, 440, 50, 80, 2))
    if nervio:
        b.append('<path d="M380 990 L380 760 Q380 640 300 520 L296 330 M380 760 Q400 640 435 520 L435 290 M380 780 Q470 660 566 540 L574 350 M380 800 Q260 680 180 560 L150 420" stroke="#ffd23f" stroke-width="13" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        b.append('<path d="M380 990 L380 760 Q380 640 300 520 L296 330 M380 760 Q400 640 435 520 L435 290" stroke="#fff6c0" stroke-width="4" fill="none" stroke-linecap="round"/>')
        if nervio == "cortado":
            b.append('<path d="M330 850 L430 910 M430 850 L330 910" stroke="#ff3d3d" stroke-width="20" stroke-linecap="round"/>')
            b.append('<path d="M380 990 L380 900" stroke="#ffd23f" stroke-width="13" stroke-linecap="round"/>')
    if gotas:
        for x, y, s in [(90, 300, 1.0), (640, 250, 0.8), (360, 60, 0.9), (700, 720, 0.7), (60, 760, 0.8)]:
            b.append(f'<path d="M{x} {y} q{-22 * s:.0f} {40 * s:.0f} 0 {56 * s:.0f} q{22 * s:.0f} {-16 * s:.0f} 0 {-56 * s:.0f} Z" fill="#7ad0ff" stroke="{OL}" stroke-width="6"/>')
    guardar(nombre, "".join(b), 760, 1000, d)


def yema(nombre="yema_lisa", arrugada=False):
    """Primer plano de la yema de un dedo (lienzo 560x820)."""
    d = lg("ym_p", (0, PIEL[0]), (1, PIEL[1]), x2=1, y2=0)
    b = [f'<path d="M80 820 L80 300 Q80 40 280 40 Q480 40 480 300 L480 820 Z" fill="url(#ym_p)" stroke="{OL}" stroke-width="14"/>']
    if arrugada:
        b.append(_arrugas(280, 300, 330, 380, 6, "#a85a3c", 11))
        b.append(_arrugas(292, 300, 330, 380, 6, "#ffe6d0", 5))
    else:
        for i in range(5):
            b.append(f'<ellipse cx="280" cy="300" rx="{40 + i * 34}" ry="{56 + i * 44}" fill="none" stroke="#d89a78" stroke-width="5" opacity="0.7"/>')
        b.append('<ellipse cx="200" cy="200" rx="50" ry="90" fill="#fff" opacity="0.3"/>')
    b.append('<path d="M120 640 Q280 670 440 640 M130 700 Q280 724 430 700" stroke="#c88a6a" stroke-width="7" fill="none"/>')
    guardar(nombre, "".join(b), 560, 820, d)


def yema_corte(nombre="yema_corte", estrecho=False):
    """Sección de la yema: piel, carne, vasos de sangre y nervio. estrecho=True: vasos finos, yema encogida y piel plegada."""
    d = lg("yc_c", (0, "#ffc2b0"), (1, "#f08a7a")) + lg("yc_p", (0, "#ffe2c8"), (1, "#f4b48e"))
    if estrecho:
        piel = "M100 800 L100 380 Q100 250 170 190 Q200 250 230 170 Q260 240 300 150 Q340 240 370 170 Q400 250 430 190 Q500 250 500 380 L500 800 Z"
        carne = "M150 800 L150 400 Q150 300 300 270 Q450 300 450 400 L450 800 Z"
        gv = 12
    else:
        piel = "M100 800 L100 360 Q100 110 300 110 Q500 110 500 360 L500 800 Z"
        carne = "M146 800 L146 370 Q146 160 300 160 Q454 160 454 370 L454 800 Z"
        gv = 34
    b = [f'<path d="{piel}" fill="url(#yc_p)" stroke="{OL}" stroke-width="14" stroke-linejoin="round"/>',
         f'<path d="{carne}" fill="url(#yc_c)"/>',
         f'<path d="M230 800 L230 520 Q230 400 190 340 M370 800 L370 520 Q370 400 410 340 M230 560 Q300 500 370 560 M230 680 Q300 630 370 680" stroke="#c0162a" stroke-width="{gv + 8}" fill="none" stroke-linecap="round"/>',
         f'<path d="M230 800 L230 520 Q230 400 190 340 M370 800 L370 520 Q370 400 410 340 M230 560 Q300 500 370 560 M230 680 Q300 630 370 680" stroke="#ff4d5e" stroke-width="{gv}" fill="none" stroke-linecap="round"/>',
         '<path d="M300 800 L300 430 M300 620 L262 560 M300 540 L340 480 M300 430 L270 380 M300 430 L330 380" stroke="#ffd23f" stroke-width="11" fill="none" stroke-linecap="round"/>',
         f'<path d="{piel}" fill="none" stroke="{OL}" stroke-width="14" stroke-linejoin="round"/>']
    guardar(nombre, "".join(b), 600, 820, d)


def pasa(nombre="pasa"):
    d = rg("ps_g", (0, "#8a4a6a", 1), (1, "#3a1630", 1), cx=0.4, cy=0.35, r=0.75)
    b = [sombra(210, 330, 150, 16),
         f'<path d="M60 190 Q40 90 150 60 Q250 20 330 90 Q400 160 350 250 Q290 320 170 310 Q80 290 60 190 Z" fill="url(#ps_g)" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>',
         '<path d="M110 120 Q160 170 130 240 M190 80 Q240 160 200 280 M270 80 Q310 170 280 270 M90 190 Q200 210 340 180" stroke="#24091e" stroke-width="9" fill="none" stroke-linecap="round"/>',
         '<path d="M130 100 Q170 80 210 90" stroke="#d89ac0" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.7"/>']
    guardar(nombre, "".join(b), 420, 360, d)


def bg_bano(nombre="bg_bano"):
    d = lg("bb_p", (0, "#cfeef4"), (1, "#8ccfe0")) + lg("bb_a", (0, "#7ad0ff"), (1, "#1a6ab8"))
    b = ['<rect width="1080" height="1920" fill="url(#bb_p)"/>']
    for y in range(0, 1300, 130):
        for x in range(0 if (y // 130) % 2 else -65, 1080, 130):
            b.append(f'<rect x="{x + 5}" y="{y + 5}" width="120" height="120" rx="10" fill="#f2fcff" opacity="0.5"/>')
    b += ['<rect x="0" y="1290" width="1080" height="70" rx="20" fill="#ffffff" stroke="#1b1b2b" stroke-width="10"/>',
          '<rect x="0" y="1350" width="1080" height="570" fill="url(#bb_a)"/>',
          '<path d="M0 1380 Q135 1350 270 1380 T540 1380 T810 1380 T1080 1380" stroke="#e8f8ff" stroke-width="12" fill="none" opacity="0.8"/>',
          '<path d="M0 1500 Q135 1470 270 1500 T540 1500 T810 1500 T1080 1500 M0 1660 Q135 1630 270 1660 T540 1660 T810 1660 T1080 1660" stroke="#bfe8ff" stroke-width="8" fill="none" opacity="0.4"/>']
    rr = random.Random(3)
    for _ in range(26):
        x, y, r = rr.uniform(30, 1050), rr.uniform(1150, 1340), rr.uniform(14, 44)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="#fff" opacity="0.75" stroke="#9adcf0" stroke-width="4"/>')
    guardar(nombre, "".join(b), 1080, 1920, d)


def bg_bajo_agua(nombre="bg_bajo_agua"):
    d = lg("ba_g", (0, "#5ad0f0"), (0.5, "#1a7ac0"), (1, "#0a2a66"))
    b = ['<rect width="1080" height="1920" fill="url(#ba_g)"/>']
    for x, w in [(120, 150), (430, 220), (760, 130), (940, 90)]:
        b.append(f'<path d="M{x} 0 L{x + w} 0 L{x + w + 260} 1920 L{x - 120} 1920 Z" fill="#fff" opacity="0.07"/>')
    rr = random.Random(8)
    for _ in range(46):
        x, y, r = rr.uniform(20, 1060), rr.uniform(60, 1900), rr.uniform(6, 26)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="none" stroke="#dff6ff" stroke-width="4" opacity="{rr.uniform(0.3, 0.8):.2f}"/>')
    b.append('<path d="M0 60 Q135 20 270 60 T540 60 T810 60 T1080 60 L1080 0 L0 0 Z" fill="#e8f8ff" opacity="0.6"/>')
    guardar(nombre, "".join(b), 1080, 1920, d)


def canica(nombre="canica", c=("#7dffb0", "#0a8a5a")):
    d = rg(nombre + "_g", (0, c[0], 1), (1, c[1], 1), cx=0.36, cy=0.32, r=0.8)
    b = [sombra(150, 286, 96, 12), f'<circle cx="150" cy="150" r="126" fill="url(#{nombre}_g)" stroke="{OL}" stroke-width="11"/>',
         '<path d="M70 190 Q150 90 232 150 Q160 150 110 236 Z" fill="#fff" opacity="0.4"/>',
         '<ellipse cx="104" cy="96" rx="30" ry="18" fill="#fff" opacity="0.9" transform="rotate(-35 104 96)"/>']
    guardar(nombre, "".join(b), 300, 300, d)


def cubeta(nombre="cubeta", agua=True):
    d = lg("cb_a", (0, "#8ad8ff"), (1, "#2a7ad0"))
    b = [sombra(250, 390, 200, 18),
         f'<path d="M40 80 L460 80 L410 380 L90 380 Z" fill="#eaf6ff" fill-opacity="0.55" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>']
    if agua:
        b += ['<path d="M56 170 L444 170 L412 370 L88 370 Z" fill="url(#cb_a)" opacity="0.9"/>',
              '<path d="M56 170 Q150 150 250 170 T444 170" stroke="#e8f8ff" stroke-width="9" fill="none"/>']
    b += [f'<path d="M30 80 L470 80" stroke="{OL}" stroke-width="22" stroke-linecap="round"/>',
          '<path d="M80 110 L104 330" stroke="#fff" stroke-width="14" stroke-linecap="round" opacity="0.6"/>']
    guardar(nombre, "".join(b), 500, 410, d)


def neumatico(nombre="neumatico"):
    d = rg("nm_l", (0, "#e6eaf2", 1), (1, "#7a8298", 1))
    b = [sombra(350, 690, 250, 20), f'<circle cx="350" cy="350" r="320" fill="#20222e" stroke="{OL}" stroke-width="14"/>']
    for i in range(24):
        a = i * 15
        b.append(f'<path d="M350 46 L372 100 L350 150 L328 100 Z" fill="#454a5e" transform="rotate({a} 350 350)"/>')
        b.append(f'<path d="M350 34 L350 160" stroke="#0c0d14" stroke-width="9" transform="rotate({a + 7.5} 350 350)"/>')
    b += [f'<circle cx="350" cy="350" r="196" fill="#11121a" stroke="{OL}" stroke-width="8"/>',
          f'<circle cx="350" cy="350" r="150" fill="url(#nm_l)" stroke="{OL}" stroke-width="10"/>']
    for i in range(5):
        b.append(f'<path d="M350 350 L350 222" stroke="{OL}" stroke-width="30" stroke-linecap="round" transform="rotate({i * 72} 350 350)"/>')
        b.append(f'<path d="M350 350 L350 226" stroke="#c8d0e4" stroke-width="18" stroke-linecap="round" transform="rotate({i * 72} 350 350)"/>')
    b.append(f'<circle cx="350" cy="350" r="40" fill="#e6eaf2" stroke="{OL}" stroke-width="9"/>')
    guardar(nombre, "".join(b), 700, 720, d)


def banda_rodadura(nombre="banda_rodadura"):
    """Dibujo de un neumático visto de frente, con el agua saliendo por los canales (lienzo 800x700)."""
    b = [f'<rect x="100" y="20" width="600" height="660" rx="40" fill="#20222e" stroke="{OL}" stroke-width="14"/>']
    for x in (250, 400, 550):
        b.append(f'<rect x="{x - 16}" y="28" width="32" height="644" fill="#0a0b12"/>')
        b.append(f'<rect x="{x - 9}" y="28" width="18" height="644" fill="#5ac8ff"/>')
    for y in range(70, 660, 90):
        b.append(f'<path d="M120 {y} L234 {y + 40} M266 {y + 40} L384 {y} M416 {y} L534 {y + 40} M566 {y + 40} L680 {y}" stroke="#0a0b12" stroke-width="18" stroke-linecap="round"/>')
        b.append(f'<path d="M120 {y} L234 {y + 40} M566 {y + 40} L680 {y}" stroke="#5ac8ff" stroke-width="8" stroke-linecap="round" opacity="0.9"/>')
    b.append('<rect x="120" y="36" width="40" height="628" rx="18" fill="#fff" opacity="0.1"/>')
    guardar(nombre, "".join(b), 800, 700, "")


def pie(nombre="pie"):
    d = lg("pi_p", (0, PIEL[0]), (1, PIEL[1]))
    b = [f'<path d="M150 300 Q110 520 170 700 Q210 800 300 800 Q400 800 420 700 Q470 500 450 320 Q440 230 300 220 Q170 220 150 300 Z" fill="url(#pi_p)" stroke="{OL}" stroke-width="12"/>']
    for x, y, r in [(170, 180, 62), (270, 120, 50), (350, 120, 44), (416, 150, 40), (466, 200, 34)]:
        b.append(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 1.15:.0f}" fill="url(#pi_p)" stroke="{OL}" stroke-width="11"/>')
        b.append(_arrugas(x, y, r * 1.2, r * 1.3, 3, "#b86a4a", 6))
    b.append(_arrugas(300, 420, 220, 220, 5, "#b86a4a", 8))
    b.append(_arrugas(300, 690, 160, 130, 4, "#b86a4a", 8))
    guardar(nombre, "".join(b), 600, 840, d)


# ====================================================================== 03 · olivo
def olivo(nombre="olivo", joven=False, hueco=False):
    """Olivo de tronco grueso y retorcido (lienzo 1000x1100). joven=True: arbolito recién plantado."""
    rr = random.Random(11)
    d = (lg("ol_t", (0, "#8a7458"), (0.35, "#c8b08a"), (1, "#5a4630"), x2=1, y2=0)
         + rg("ol_h", (0, "#b8cc9a", 1), (1, "#6a8a5a", 1), cx=0.4, cy=0.35, r=0.8))
    if joven:
        b = [sombra(250, 580, 120, 14),
             f'<path d="M240 580 Q236 420 250 300 Q262 420 262 580 Z" fill="url(#ol_t)" stroke="{OL}" stroke-width="9"/>']
        for x, y, r in [(250, 240, 90), (180, 300, 60), (320, 300, 62), (250, 160, 60)]:
            b.append(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 0.8:.0f}" fill="url(#ol_h)" stroke="{OL}" stroke-width="9"/>')
        b.append('<path d="M150 580 Q250 540 350 580 Z" fill="#7a5a34" stroke="#1b1b2b" stroke-width="8"/>')
        guardar(nombre, "".join(b), 500, 620, d)
        return
    b = [sombra(500, 1060, 420, 30, 0.35)]
    # copa (detrás)
    copas = [(500, 300, 330, 220), (240, 380, 220, 170), (770, 380, 220, 170), (380, 200, 200, 150), (640, 190, 210, 150), (500, 430, 300, 150)]
    for x, y, rx, ry in copas:
        b.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{OL}"/>')
    for x, y, rx, ry in copas:
        b.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx - 12}" ry="{ry - 12}" fill="url(#ol_h)"/>')
    for _ in range(90):
        x, y = rr.uniform(120, 880), rr.uniform(110, 500)
        a = rr.uniform(0, 180)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="26" ry="8" fill="{rr.choice(["#8aa870", "#d2e2b8", "#5a7a4a"])}" transform="rotate({a:.0f} {x:.0f} {y:.0f})" opacity="0.9"/>')
    for _ in range(22):
        x, y = rr.uniform(160, 840), rr.uniform(180, 500)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="11" ry="15" fill="#2a2a3a" stroke="#0c0c14" stroke-width="3"/><circle cx="{x - 3:.0f}" cy="{y - 5:.0f}" r="3" fill="#fff" opacity="0.7"/>')
    # tronco retorcido
    b += [f'<path d="M250 1060 Q300 960 290 860 Q250 740 330 640 Q360 560 320 470 L420 450 Q440 540 500 560 Q560 540 590 440 L690 470 Q650 570 690 650 Q770 750 720 860 Q710 960 770 1060 Z" fill="url(#ol_t)" stroke="{OL}" stroke-width="14" stroke-linejoin="round"/>',
          '<path d="M360 1040 Q390 900 350 780 Q340 700 400 620 M470 1050 Q450 900 500 760 Q520 680 490 600 M610 1040 Q640 900 610 780 Q600 700 640 630 M300 880 Q340 860 350 800 M700 900 Q660 860 650 800" stroke="#4a3822" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.8"/>',
          '<path d="M330 1000 Q350 880 320 780" stroke="#f0e0c0" stroke-width="12" fill="none" stroke-linecap="round" opacity="0.45"/>',
          f'<path d="M200 1060 Q260 1010 330 1050 M690 1050 Q760 1010 820 1060" stroke="{OL}" stroke-width="12" fill="none" stroke-linecap="round"/>']
    if hueco:
        b.append(f'<path d="M440 1050 Q420 880 470 760 Q500 700 530 760 Q580 880 560 1050 Z" fill="#1a120a" stroke="{OL}" stroke-width="10"/>')
        b.append('<path d="M470 1040 Q460 900 492 800" stroke="#4a3822" stroke-width="8" fill="none" opacity="0.8"/>')
    guardar(nombre, "".join(b), 1000, 1100, d)


def bg_olivar(nombre="bg_olivar", cielo=("#8ad0ff", "#e8f6ff"), tierra=("#e0b070", "#b87a3a"), sol="#fff6c0"):
    d = lg(nombre + "_c", (0, cielo[0]), (1, cielo[1])) + lg(nombre + "_t", (0, tierra[0]), (1, tierra[1]))
    rr = random.Random(5)
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>',
         f'<circle cx="850" cy="330" r="110" fill="{sol}" opacity="0.9"/><circle cx="850" cy="330" r="190" fill="{sol}" opacity="0.25"/>',
         '<path d="M0 1010 Q200 900 420 980 Q640 880 860 960 Q980 920 1080 970 L1080 1300 L0 1300 Z" fill="#9ab88a" opacity="0.75"/>',
         '<path d="M0 1100 Q260 1000 520 1080 Q800 1010 1080 1090 L1080 1400 L0 1400 Z" fill="#7aa06a"/>',
         f'<rect x="0" y="1220" width="1080" height="700" fill="url(#{nombre}_t)"/>']
    for fila, (y, s) in enumerate([(1190, 0.5), (1260, 0.7), (1360, 0.95)]):
        for x in range(-40 + fila * 60, 1120, int(210 * s + 40)):
            xx = x + rr.uniform(-16, 16)
            b.append(f'<ellipse cx="{xx:.0f}" cy="{y + 46 * s:.0f}" rx="{70 * s:.0f}" ry="{10 * s:.0f}" fill="#000" opacity="0.2"/>')
            b.append(f'<rect x="{xx - 9 * s:.0f}" y="{y - 20 * s:.0f}" width="{18 * s:.0f}" height="{64 * s:.0f}" rx="6" fill="#6a5438"/>')
            b.append(f'<ellipse cx="{xx:.0f}" cy="{y - 50 * s:.0f}" rx="{74 * s:.0f}" ry="{52 * s:.0f}" fill="#6a8a5a" stroke="#3a5a34" stroke-width="{5 * s:.0f}"/>')
            b.append(f'<ellipse cx="{xx - 18 * s:.0f}" cy="{y - 64 * s:.0f}" rx="{34 * s:.0f}" ry="{20 * s:.0f}" fill="#a8c494" opacity="0.8"/>')
    for i in range(7):
        y = 1480 + i * 62
        b.append(f'<path d="M0 {y} Q540 {y - 30} 1080 {y}" stroke="#8a5a2a" stroke-width="6" fill="none" opacity="0.3"/>')
    for x, y, w in [(140, 260, 200), (420, 180, 150), (560, 420, 180)]:
        b.append(f'<ellipse cx="{x}" cy="{y}" rx="{w * 0.5:.0f}" ry="34" fill="#fff" opacity="0.8"/><ellipse cx="{x + 50}" cy="{y - 24}" rx="{w * 0.3:.0f}" ry="30" fill="#fff" opacity="0.8"/>')
    guardar(nombre, "".join(b), 1080, 1920, d)


def bg_roma(nombre="bg_roma"):
    d = lg("br_c", (0, "#ffb86a"), (0.6, "#ffe2a8"), (1, "#f4c888")) + lg("br_m", (0, "#fff6e6"), (1, "#d8c4a0"), x2=1, y2=0)
    b = ['<rect width="1080" height="1920" fill="url(#br_c)"/>', '<circle cx="540" cy="760" r="260" fill="#fff6d0" opacity="0.55"/>',
         '<path d="M0 1180 Q300 1080 540 1150 Q800 1080 1080 1170 L1080 1920 L0 1920 Z" fill="#c89a5a"/>',
         f'<path d="M190 560 L540 380 L890 560 Z" fill="url(#br_m)" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>',
         f'<rect x="170" y="560" width="740" height="56" fill="url(#br_m)" stroke="{OL}" stroke-width="10"/>']
    for x in (210, 370, 530, 690, 850 - 30):
        b.append(f'<rect x="{x}" y="616" width="70" height="560" fill="url(#br_m)" stroke="{OL}" stroke-width="10"/>')
        b.append(f'<path d="M{x + 22} 630 L{x + 22} 1160 M{x + 48} 630 L{x + 48} 1160" stroke="#b8a480" stroke-width="5"/>')
        b.append(f'<rect x="{x - 14}" y="1160" width="98" height="34" fill="url(#br_m)" stroke="{OL}" stroke-width="9"/>')
    b.append(f'<rect x="130" y="1194" width="820" height="50" fill="url(#br_m)" stroke="{OL}" stroke-width="10"/>')
    b.append('<rect x="0" y="1244" width="1080" height="676" fill="#b8884a"/>')
    for i in range(8):
        b.append(f'<path d="M0 {1330 + i * 76} L1080 {1330 + i * 76}" stroke="#8a5a2a" stroke-width="5" opacity="0.3"/>')
    guardar(nombre, "".join(b), 1080, 1920, d)


def romano(nombre="romano"):
    """Campesino romano de dibujo, con túnica y una azada (lienzo 460x860). Figura genérica, no una persona real."""
    d = lg("ro_t", (0, "#fffaf0"), (1, "#d8ccb4")) + lg("ro_p", (0, "#f4c49a"), (1, "#d89a6a"))
    b = [sombra(230, 840, 150, 16),
         f'<rect x="150" y="640" width="54" height="180" rx="22" fill="url(#ro_p)" stroke="{OL}" stroke-width="9"/>',
         f'<rect x="256" y="640" width="54" height="180" rx="22" fill="url(#ro_p)" stroke="{OL}" stroke-width="9"/>',
         f'<path d="M136 808 L214 808 L214 838 L120 838 Z M246 808 L324 808 L340 838 L246 838 Z" fill="#8a5a2a" stroke="{OL}" stroke-width="8" stroke-linejoin="round"/>',
         f'<path d="M110 330 Q230 270 350 330 L372 680 L88 680 Z" fill="url(#ro_t)" stroke="{OL}" stroke-width="11" stroke-linejoin="round"/>',
         f'<path d="M110 330 Q230 430 330 680" stroke="#c0392b" stroke-width="30" fill="none"/>',
         f'<path d="M96 560 L366 560" stroke="#8a5a2a" stroke-width="18"/>',
         # brazos y azada
         f'<path d="M400 120 L400 760" stroke="{OL}" stroke-width="26" stroke-linecap="round"/><path d="M400 120 L400 760" stroke="#a87a4a" stroke-width="14" stroke-linecap="round"/>',
         f'<path d="M352 110 L448 110 L440 190 L360 190 Z" fill="#9aa3b8" stroke="{OL}" stroke-width="9" stroke-linejoin="round"/>',
         f'<path d="M340 360 Q420 400 400 470" stroke="{OL}" stroke-width="52" fill="none" stroke-linecap="round"/><path d="M340 360 Q420 400 400 470" stroke="#e8b088" stroke-width="34" fill="none" stroke-linecap="round"/>',
         f'<path d="M120 360 Q60 450 90 540" stroke="{OL}" stroke-width="52" fill="none" stroke-linecap="round"/><path d="M120 360 Q60 450 90 540" stroke="#e8b088" stroke-width="34" fill="none" stroke-linecap="round"/>',
         # cabeza
         f'<circle cx="230" cy="190" r="120" fill="url(#ro_p)" stroke="{OL}" stroke-width="11"/>',
         f'<path d="M116 160 Q130 60 230 62 Q330 60 344 160 Q300 110 230 112 Q160 110 116 160 Z" fill="#4a3020" stroke="{OL}" stroke-width="9" stroke-linejoin="round"/>',
         f'<circle cx="190" cy="200" r="15" fill="{OL}"/><circle cx="270" cy="200" r="15" fill="{OL}"/><circle cx="195" cy="194" r="5" fill="#fff"/><circle cx="275" cy="194" r="5" fill="#fff"/>',
         f'<path d="M196 248 Q230 276 264 248" stroke="{OL}" stroke-width="8" fill="none" stroke-linecap="round"/>',
         f'<path d="M172 172 L208 166 M252 166 L288 172" stroke="{OL}" stroke-width="7" stroke-linecap="round"/>']
    guardar(nombre, "".join(b), 460, 860, d)


def moneda_laurel(nombre="moneda_laurel"):
    d = rg("ml_g", (0, "#fff0a8", 1), (0.6, "#e0a830", 1), (1, "#8a5a10", 1), cx=0.36, cy=0.32, r=0.85)
    b = [sombra(300, 596, 220, 18), f'<circle cx="300" cy="300" r="280" fill="url(#ml_g)" stroke="{OL}" stroke-width="14"/>',
         '<circle cx="300" cy="300" r="236" fill="none" stroke="#8a5a10" stroke-width="7" stroke-dasharray="6 16"/>',
         # perfil genérico con corona de laurel
         '<path d="M250 470 Q240 400 262 370 Q212 350 212 280 Q210 170 310 160 Q400 160 404 250 Q406 276 426 300 L400 312 Q404 340 396 352 Q398 388 356 392 Q340 430 352 470 Z" fill="#9a6a16"/>']
    for i in range(7):
        a = -150 + i * 22
        x, y = 304 + 104 * math.cos(math.radians(a)), 252 + 100 * math.sin(math.radians(a))
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="30" ry="11" fill="#5a8a2a" stroke="#2a4a14" stroke-width="4" transform="rotate({a + 60:.0f} {x:.0f} {y:.0f})"/>')
    b.append('<path d="M110 220 A200 200 0 0 1 250 96" stroke="#fff" stroke-width="18" fill="none" stroke-linecap="round" opacity="0.7"/>')
    guardar(nombre, "".join(b), 600, 620, d)


def carabela(nombre="carabela"):
    d = lg("ca_m", (0, "#a8743a"), (1, "#5a3414")) + lg("ca_v", (0, "#fffaf0"), (1, "#e0d2b4"))
    b = [f'<path d="M400 60 L400 560 M210 180 L210 560 M600 200 L600 560" stroke="{OL}" stroke-width="18" stroke-linecap="round"/>',
         f'<path d="M270 100 Q420 180 270 430 Q420 380 560 430 Q440 250 560 100 Q420 140 270 100 Z" fill="url(#ca_v)" stroke="{OL}" stroke-width="11" stroke-linejoin="round"/>',
         f'<path d="M120 230 Q230 270 130 450 Q220 420 300 450 Q250 330 300 230 Q210 250 120 230 Z" fill="url(#ca_v)" stroke="{OL}" stroke-width="10" stroke-linejoin="round"/>',
         f'<path d="M580 250 L720 460 L580 460 Z" fill="url(#ca_v)" stroke="{OL}" stroke-width="10" stroke-linejoin="round"/>',
         f'<path d="M400 60 L480 40 L400 20 Z" fill="#c0392b" stroke="{OL}" stroke-width="7" stroke-linejoin="round"/>',
         f'<path d="M60 520 L760 500 Q740 640 620 690 L200 690 Q100 650 60 520 Z" fill="url(#ca_m)" stroke="{OL}" stroke-width="13" stroke-linejoin="round"/>',
         f'<path d="M84 566 L744 548 M110 620 L716 606" stroke="{OL}" stroke-width="6" opacity="0.5"/>',
         f'<rect x="610" y="440" width="140" height="70" fill="url(#ca_m)" stroke="{OL}" stroke-width="10"/>',
         '<path d="M0 690 Q100 650 200 690 T400 690 T600 690 T800 690 L800 780 L0 780 Z" fill="#2a7ad0" stroke="#1b1b2b" stroke-width="9"/>',
         '<path d="M0 730 Q100 700 200 730 T400 730 T600 730 T800 730" stroke="#bfe8ff" stroke-width="8" fill="none" opacity="0.7"/>']
    guardar(nombre, "".join(b), 800, 790, d)


def tronco_corte(nombre="tronco_anillos", hueco=False):
    d = rg("tc_g", (0, "#f4dca8", 1), (1, "#c89a5a", 1))
    b = [sombra(350, 690, 260, 20),
         f'<path d="M350 40 Q520 30 620 150 Q700 280 650 430 Q600 620 400 660 Q200 680 90 520 Q10 370 90 200 Q190 40 350 40 Z" fill="#6a5438" stroke="{OL}" stroke-width="14"/>',
         '<path d="M350 80 Q500 72 588 176 Q660 290 616 420 Q570 580 396 618 Q220 634 126 500 Q56 370 124 220 Q210 80 350 80 Z" fill="url(#tc_g)"/>']
    if hueco:
        b.append(f'<path d="M340 200 Q460 190 500 300 Q530 420 420 480 Q300 520 230 420 Q180 290 340 200 Z" fill="#150e08" stroke="{OL}" stroke-width="10"/>')
        b.append('<path d="M300 260 Q260 340 300 420" stroke="#3a2a18" stroke-width="10" fill="none" stroke-linecap="round"/>')
        for r in (0.86,):
            b.append('<path d="M350 130 Q470 124 546 210 Q600 300 566 404 Q526 530 392 562 Q250 574 174 470 Q118 368 172 250 Q240 130 350 130 Z" fill="none" stroke="#a87a44" stroke-width="6"/>')
    else:
        for i in range(1, 9):
            k = 1 - i * 0.105
            b.append(f'<path d="M350 80 Q500 72 588 176 Q660 290 616 420 Q570 580 396 618 Q220 634 126 500 Q56 370 124 220 Q210 80 350 80 Z" fill="none" stroke="#a87a44" stroke-width="6" transform="translate({350 * (1 - k):.0f} {350 * (1 - k):.0f}) scale({k:.3f})"/>')
        b.append('<circle cx="350" cy="350" r="12" fill="#6a4a24"/>')
    guardar(nombre, "".join(b), 700, 720, d)


def cinta_metrica(nombre="cinta_metrica"):
    b = [f'<rect x="6" y="20" width="1188" height="80" rx="8" fill="#ffd23f" stroke="{OL}" stroke-width="10"/>']
    for i in range(1, 48):
        x = 6 + i * 24.75
        h = 44 if i % 6 == 0 else 22
        b.append(f'<path d="M{x:.0f} 24 L{x:.0f} {24 + h}" stroke="{OL}" stroke-width="{6 if i % 6 == 0 else 4}"/>')
    guardar(nombre, "".join(b), 1200, 120, "")


def brote(nombre="brote"):
    d = lg("bt_t", (0, "#8a7458"), (0.4, "#c8b08a"), (1, "#5a4630"), x2=1, y2=0)
    b = [sombra(300, 560, 240, 20),
         f'<path d="M120 560 Q130 420 170 380 L210 330 L250 370 L300 320 L350 380 L400 340 L440 390 Q480 440 480 560 Z" fill="url(#bt_t)" stroke="{OL}" stroke-width="13" stroke-linejoin="round"/>',
         '<path d="M220 540 Q230 460 210 400 M330 540 Q320 460 340 400 M420 540 Q410 480 420 430" stroke="#4a3822" stroke-width="9" fill="none" stroke-linecap="round"/>']
    for x, h, a in [(190, 250, -12), (300, 300, 2), (410, 240, 14), (250, 180, -4), (360, 190, 8)]:
        b.append(f'<g transform="rotate({a} {x} 380)"><path d="M{x} 380 L{x} {380 - h}" stroke="{OL}" stroke-width="16" stroke-linecap="round"/><path d="M{x} 380 L{x} {380 - h}" stroke="#7ac84a" stroke-width="8" stroke-linecap="round"/>')
        for k in range(3):
            y = 380 - h + k * h * 0.28
            b.append(f'<ellipse cx="{x - 30}" cy="{y:.0f}" rx="32" ry="12" fill="#8ad85a" stroke="{OL}" stroke-width="6" transform="rotate(-28 {x - 30} {y:.0f})"/>'
                     f'<ellipse cx="{x + 30}" cy="{y + 14:.0f}" rx="32" ry="12" fill="#6ab84a" stroke="{OL}" stroke-width="6" transform="rotate(28 {x + 30} {y + 14:.0f})"/>')
        b.append('</g>')
    guardar(nombre, "".join(b), 600, 600, d)


def aceitunas(nombre="aceitunas", color=("#6a9a3a", "#3a5a1a")):
    d = rg(nombre + "_g", (0, color[0], 1), (1, color[1], 1), cx=0.38, cy=0.32, r=0.8)
    b = [f'<path d="M20 110 Q260 30 580 120" stroke="{OL}" stroke-width="22" fill="none" stroke-linecap="round"/>',
         '<path d="M20 110 Q260 30 580 120" stroke="#8a7458" stroke-width="10" fill="none" stroke-linecap="round"/>']
    for x, y, a in [(90, 60, -40), (190, 36, -20), (320, 30, 10), (450, 60, 30), (540, 150, 70), (140, 150, 130)]:
        b.append(f'<ellipse cx="{x}" cy="{y}" rx="62" ry="18" fill="#9ab87a" stroke="{OL}" stroke-width="7" transform="rotate({a} {x} {y})"/>')
    for x, y in [(170, 220), (300, 250), (420, 230), (240, 330), (360, 350)]:
        b.append(f'<path d="M{x} {y - 60} L{x} {y - 120 + abs(x - 300) * 0.2:.0f}" stroke="{OL}" stroke-width="6"/>')
        b.append(f'<ellipse cx="{x}" cy="{y}" rx="52" ry="66" fill="url(#{nombre}_g)" stroke="{OL}" stroke-width="10"/>')
        b.append(f'<ellipse cx="{x - 18}" cy="{y - 26}" rx="13" ry="20" fill="#fff" opacity="0.55"/>')
    guardar(nombre, "".join(b), 600, 440, d)


def botella_aceite(nombre="botella_aceite"):
    d = lg("bo_a", (0, "#f4e04a"), (1, "#a8a01a")) + lg("bo_v", (0, "#e8f6e0"), (1, "#a8c8a0"), x2=1, y2=0)
    b = [sombra(170, 770, 130, 16),
         f'<rect x="126" y="20" width="88" height="70" rx="12" fill="#8a5a2a" stroke="{OL}" stroke-width="10"/>',
         f'<path d="M132 90 L208 90 L208 220 Q300 280 300 380 L300 700 Q300 750 250 750 L90 750 Q40 750 40 700 L40 380 Q40 280 132 220 Z" fill="url(#bo_v)" fill-opacity="0.6" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>',
         '<path d="M60 400 Q60 330 130 290 L210 290 Q280 330 280 400 L280 700 Q280 730 250 730 L90 730 Q60 730 60 700 Z" fill="url(#bo_a)"/>',
         f'<rect x="76" y="470" width="188" height="150" rx="12" fill="#fffaf0" stroke="{OL}" stroke-width="7"/>',
         f'<ellipse cx="170" cy="545" rx="26" ry="36" fill="#6a9a3a" stroke="{OL}" stroke-width="7"/>',
         '<path d="M76 320 L96 680" stroke="#fff" stroke-width="16" stroke-linecap="round" opacity="0.6"/>']
    guardar(nombre, "".join(b), 340, 800, d)


def mapa_iberia(nombre="mapa_iberia"):
    """Silueta muy simplificada de la península ibérica con un punto en la costa mediterránea, al sur del Ebro."""
    d = lg("mi_t", (0, "#f4d898"), (1, "#d8a860"))
    b = ['<rect width="900" height="820" rx="30" fill="#2a7ad0"/>',
         '<path d="M0 200 Q200 160 450 220 T900 180 M0 640 Q250 600 500 660 T900 620" stroke="#bfe8ff" stroke-width="7" fill="none" opacity="0.35"/>',
         f'<path d="M120 150 L330 120 L520 140 L640 170 L760 200 L770 250 L690 330 L640 420 L600 500 L620 560 L540 620 L440 680 L330 690 L270 720 L200 660 L150 640 L130 540 L150 430 L110 330 L90 230 Z" fill="url(#mi_t)" stroke="{OL}" stroke-width="12" stroke-linejoin="round"/>',
         '<path d="M150 430 L130 540 L150 640 L200 660 L225 560 L215 440 Z" fill="#e8c888" stroke="#1b1b2b" stroke-width="6" stroke-linejoin="round" opacity="0.8"/>',
         '<path d="M330 190 Q500 230 668 362" stroke="#5ac8ff" stroke-width="9" fill="none" stroke-linecap="round"/>',
         f'<path d="M664 300 Q620 230 664 190 Q708 230 664 300 Z" fill="#ff3d3d" stroke="{OL}" stroke-width="8" transform="translate(-4 82)"/>',
         '<circle cx="660" cy="312" r="14" fill="#fff"/>']
    guardar(nombre, "".join(b), 900, 820, d)


# ====================================================================== GENERAR
def generar(dirsvg):
    m = _mod("lotes/2026-11-24-tarde/generadores/ilus_1124t.py", "_ilus_1124t_25")
    m.generar(dirsvg)
    ilus.OUT = dirsvg
    # 01
    hubble(); gafas(); foto(); foto("foto_borrosa", borrosa=True); estrella(); estrella("estrella_borrosa", borrosa=True)
    espejo_hubble(); espejo_corte(); pelo(); aparato_medir(); aparato_medir("aparato_mal", mal=True); transbordador(); espejito(); billetes()
    # 02
    mano(); mano("mano_arrugada", arrugada=True, gotas=True); mano("mano_nervio", nervio="ok"); mano("mano_nervio_cortado", nervio="cortado")
    yema(); yema("yema_arrugada", arrugada=True); yema_corte(); yema_corte("yema_corte_estrecho", estrecho=True); pasa()
    bg_bano(); bg_bajo_agua(); canica(); canica("canica_azul", ("#8ad0ff", "#1a4ab8")); canica("canica_roja", ("#ff9a9a", "#b81a2a"))
    cubeta(); cubeta("cubeta_seca", agua=False); neumatico(); banda_rodadura(); pie()
    # 03
    olivo(); olivo("olivo_joven", joven=True); olivo("olivo_hueco", hueco=True)
    bg_olivar(); bg_olivar("bg_olivar_tarde", ("#ff9a5a", "#ffe2a8"), ("#d89a5a", "#8a5a2a"), "#fff0b0"); bg_roma(); romano(); moneda_laurel()
    carabela(); tronco_corte(); tronco_corte("tronco_hueco", hueco=True); cinta_metrica(); brote()
    aceitunas(); aceitunas("aceitunas_negras", ("#5a4a6a", "#1a1420")); botella_aceite(); mapa_iberia()
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
