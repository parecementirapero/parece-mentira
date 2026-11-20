"""Ilustraciones del lote 2026-11-19-tarde (Agente 20:00, Jorge): 01 atardecer azul en Marte, 02 huesos de bebé, 03 forma de las gotas.
Uso: python3 ilus_1119t.py DIR_SVG. Ladrillos de motor/biblioteca/ilus.py. Sin logos, personajes ni fotos: todo dibujado aquí."""
import math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano  # noqa: E402

W, H = 1080, 1920


def _p(pts, cerrar=True):
    return "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + (" Z" if cerrar else "")


def _cresta(r, y0, amp, n=14, x0=-40, x1=1120):
    pts = [(x0, 1920)]
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append((x, y0 - amp * (0.5 + 0.5 * math.sin(i * 1.3 + r.random() * 2)) - r.uniform(0, amp * 0.4)))
    pts.append((x1, 1920))
    return _p(pts)


def _rocas(r, n, y0, y1, col="#3a160c", luz="#c0603a"):
    b = []
    for _ in range(n):
        x, y = r.uniform(0, 1080), r.uniform(y0, y1)
        s = (y - y0) / max(1, y1 - y0) * 40 + 8
        b.append(f'<ellipse cx="{x:.0f}" cy="{y + s*0.3:.0f}" rx="{s*1.3:.0f}" ry="{s*0.35:.0f}" fill="#000" opacity="0.35"/>'
                 f'<path d="M{x-s:.0f} {y+s*0.3:.0f} Q{x-s*0.8:.0f} {y-s*0.6:.0f} {x:.0f} {y-s*0.7:.0f} Q{x+s:.0f} {y-s*0.4:.0f} {x+s*1.1:.0f} {y+s*0.3:.0f} Z" fill="{col}"/>'
                 f'<path d="M{x-s*0.6:.0f} {y-s*0.3:.0f} Q{x:.0f} {y-s*0.75:.0f} {x+s*0.6:.0f} {y-s*0.35:.0f}" stroke="{luz}" stroke-width="{max(2, s*0.12):.0f}" fill="none" opacity="0.7"/>')
    return "".join(b)


# ====================================================================== 01 · MARTE
def bg_marte(nombre, hora="dia"):
    """Paisaje marciano: cielo de óxido de día; al atardecer cielo oscuro ocre con halo azul alrededor del Sol junto a la cresta."""
    r = random.Random(41 if hora == "dia" else 43)
    if hora == "dia":
        d = (lg("ma_c", (0, "#b8784a"), (0.5, "#d8a070"), (0.72, "#e6b888")) + lg("ma_m1", (0, "#a85a34"), (1, "#7a3a20")) +
             lg("ma_m2", (0, "#8a3e1e"), (1, "#5a2410")) + lg("ma_s", (0, "#b8582c"), (1, "#3a140a")))
        halo = '<circle cx="760" cy="420" r="60" fill="#fff4e0" opacity="0.9"/><circle cx="760" cy="420" r="200" fill="#ffe0b0" opacity="0.18" filter="url(#blur40)"/>'
    else:
        d = (lg("ma_c", (0, "#1a1016"), (0.35, "#4a2a22"), (0.6, "#8a5a3a"), (0.74, "#a87048")) + lg("ma_m1", (0, "#3a1e18"), (1, "#24120c")) +
             lg("ma_m2", (0, "#2a140c"), (1, "#160804")) + lg("ma_s", (0, "#3a1a0c"), (1, "#0a0402")) +
             rg("ma_az", (0, "#e8f4ff", 1), (0.12, "#a8d4ff", 0.95), (0.4, "#5a9ad8", 0.6), (0.75, "#3a6aa8", 0.18), (1, "#3a6aa8", 0)))
        halo = ('<ellipse cx="540" cy="1110" rx="560" ry="460" fill="url(#ma_az)"/>'
                '<circle cx="540" cy="1110" r="34" fill="#ffe8ec"/><circle cx="540" cy="1110" r="46" fill="#ffd0dc" opacity="0.45" filter="url(#blur8)"/>')
    b = ['<rect width="1080" height="1920" fill="url(#ma_c)"/>', halo]
    for i in range(5):  # bandas de polvo en el cielo
        y = 300 + i * 150
        b.append(f'<path d="M-50 {y} Q300 {y-30} 600 {y+10} T1150 {y-20}" stroke="#ffd8b0" stroke-width="{30 + i*8}" opacity="0.05" fill="none" filter="url(#blur20)"/>')
    if hora != "dia":
        for _ in range(60):
            x, y = r.uniform(0, 1080), r.uniform(0, 520)
            b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(0.8, 2.2):.1f}" fill="#fff" opacity="{r.uniform(0.3, 0.8):.2f}"/>')
    b.append(f'<path d="{_cresta(r, 1170, 110, 9)}" fill="url(#ma_m1)"/>')
    b.append(f'<path d="{_cresta(r, 1320, 70, 12)}" fill="url(#ma_m2)"/>')
    b.append('<path d="M-40 1480 Q300 1420 600 1470 T1120 1440 L1120 1920 L-40 1920 Z" fill="url(#ma_s)"/>')
    for k in range(9):  # ondas de arena
        y = 1520 + k * 42
        b.append(f'<path d="M{-40 + (k%2)*60} {y} q90 -16 180 0 t180 0 t180 0 t180 0 t180 0 t180 0" stroke="#000" stroke-width="5" opacity="0.18" fill="none"/>')
    b.append(_rocas(r, 26, 1500, 1880, "#2a0e06" if hora != "dia" else "#5a2410", "#e08a50" if hora == "dia" else "#7aa8e8"))
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def bg_tierra_atardecer():
    """Atardecer naranja en la Tierra: mar, sol grande, nubes y cielo azul arriba."""
    d = (lg("ta_c", (0, "#2a3a7a"), (0.35, "#c05a6a"), (0.58, "#ff9a4a"), (0.68, "#ffd07a")) +
         lg("ta_m", (0, "#ff9a4a"), (0.2, "#a04a3a"), (1, "#1a1a3a")) + rg("ta_s", (0, "#fff8e0", 1), (0.25, "#ffd060", 0.9), (1, "#ff8030", 0)))
    b = ['<rect width="1080" height="1920" fill="url(#ta_c)"/>', '<circle cx="540" cy="1180" r="420" fill="url(#ta_s)"/>',
         '<circle cx="540" cy="1180" r="120" fill="#fff0c0"/>']
    for x, y, w in [(200, 600, 360), (800, 760, 300), (380, 920, 420)]:
        b.append(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{w*0.12:.0f}" fill="#7a3a5a" opacity="0.55"/><ellipse cx="{x}" cy="{y+12}" rx="{w*0.8:.0f}" ry="{w*0.05:.0f}" fill="#ffb070" opacity="0.6"/>')
    b.append('<rect x="0" y="1200" width="1080" height="720" fill="url(#ta_m)"/>')
    for k in range(18):
        y = 1220 + k * k * 2.2
        b.append(f'<rect x="{540 - 150 + k*4}" y="{y:.0f}" width="{300 - k*8}" height="5" fill="#ffe0a0" opacity="{0.8 - k*0.04:.2f}"/>')
    b.append('<path d="M-20 1700 Q200 1600 420 1690 Q300 1760 -20 1780 Z" fill="#0c0c1a"/><path d="M1100 1640 Q860 1590 700 1700 Q900 1740 1100 1730 Z" fill="#0c0c1a"/>')
    b.append(grano())
    guardar("bg_tierra_atardecer", "".join(b), defs=d)


def rover():
    """Rover genérico de seis ruedas con mástil y cámara (sin marcas)."""
    w, h = 900, 760
    d = lg("ro_c", (0, "#f2efe8"), (0.6, "#c8c2b6"), (1, "#8a8478")) + lg("ro_r", (0, "#4a4a50"), (1, "#1a1a1e")) + lg("ro_p", (0, "#3a4a6a"), (0.5, "#6a8ac8"), (1, "#2a3a5a"), x2=1, y2=0)
    b = ['<ellipse cx="450" cy="720" rx="400" ry="30" fill="#000" opacity="0.45" filter="url(#blur8)"/>']
    # suspensión
    b.append('<path d="M150 600 L280 470 L420 600 M420 600 L560 470 L700 600 L760 600" stroke="#6a665e" stroke-width="18" fill="none" stroke-linecap="round"/>')
    for x in (150, 420, 700):
        b.append(f'<circle cx="{x}" cy="620" r="82" fill="url(#ro_r)"/><circle cx="{x}" cy="620" r="48" fill="#8a8a90"/><circle cx="{x}" cy="620" r="16" fill="#2a2a2e"/>')
        for k in range(10):
            a = k * math.pi / 5
            b.append(f'<path d="M{x + 70*math.cos(a):.0f} {620 + 70*math.sin(a):.0f} L{x + 84*math.cos(a):.0f} {620 + 84*math.sin(a):.0f}" stroke="#0a0a0c" stroke-width="10"/>')
    # cuerpo
    b.append('<path d="M140 470 L760 470 L800 400 L180 380 Z" fill="url(#ro_c)" stroke="#5a564e" stroke-width="5"/>')
    b.append('<rect x="160" y="350" width="560" height="40" rx="8" fill="url(#ro_p)"/>')
    b.append('<rect x="230" y="410" width="160" height="40" rx="6" fill="#9a9488"/><rect x="420" y="410" width="200" height="40" rx="6" fill="#7a7468"/>')
    # brazo y antena
    b.append('<path d="M760 430 L860 400 L880 470" stroke="#6a665e" stroke-width="14" fill="none"/><circle cx="880" cy="480" r="18" fill="#4a4640"/>')
    b.append('<rect x="210" y="250" width="14" height="110" fill="#8a8478"/><circle cx="217" cy="248" r="34" fill="#d8d2c6" stroke="#5a564e" stroke-width="4"/>')
    # mástil con cámara
    b.append('<rect x="610" y="90" width="22" height="300" fill="url(#ro_c)" stroke="#5a564e" stroke-width="4"/>')
    b.append('<rect x="560" y="40" width="150" height="80" rx="10" fill="url(#ro_c)" stroke="#5a564e" stroke-width="5"/>')
    b.append('<circle cx="600" cy="80" r="20" fill="#1a1a2a"/><circle cx="660" cy="80" r="20" fill="#1a1a2a"/><circle cx="594" cy="74" r="6" fill="#7df9ff"/><circle cx="654" cy="74" r="6" fill="#7df9ff"/>')
    b.append('<path d="M140 470 L760 470 L800 400 L180 380 Z" fill="#ffd8a0" opacity="0.12"/>')
    guardar("rover", "".join(b), w, h, d)


def foto_marco(nombre, azul):
    """Foto «polaroid» de un atardecer en Marte (azul o de día)."""
    w, h = 520, 600
    d = (lg(f"{nombre}_c", (0, "#2a1810"), (0.55, "#7a5236"), (0.8, "#a8744a")) +
         rg(f"{nombre}_a", (0, "#e8f4ff", 1), (0.2, "#a8d4ff", 0.9), (1, "#3a6aa8", 0)))
    b = ['<rect x="14" y="20" width="500" height="580" rx="6" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<rect x="6" y="6" width="500" height="580" rx="6" fill="#f6f2ea"/>',
         f'<rect x="34" y="34" width="444" height="444" fill="url(#{nombre}_c)"/>']
    if azul:
        b.append(f'<ellipse cx="256" cy="380" rx="230" ry="190" fill="url(#{nombre}_a)"/><circle cx="256" cy="380" r="12" fill="#fff"/>')
    else:
        b.append('<circle cx="330" cy="200" r="16" fill="#fff4e0"/>')
    b.append('<path d="M34 400 Q140 360 256 395 Q380 360 478 390 L478 478 L34 478 Z" fill="#160804"/>')
    guardar(nombre, "".join(b), w, h, d)


def marte_planeta():
    w = 900
    d = rg("mp_b", (0, "#f0a070", 1), (0.5, "#c0582a", 1), (0.85, "#7a2a12", 1), (1, "#3a0e04", 1), cx=0.38, cy=0.35, r=0.7)
    r = random.Random(5)
    b = ['<circle cx="450" cy="450" r="440" fill="url(#mp_b)"/>']
    for _ in range(26):
        x, y, s = r.uniform(120, 780), r.uniform(120, 780), r.uniform(14, 70)
        if (x - 450) ** 2 + (y - 450) ** 2 < 380 ** 2:
            b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{s:.0f}" ry="{s*0.8:.0f}" fill="#5a1e0a" opacity="0.35"/><ellipse cx="{x-s*0.2:.0f}" cy="{y-s*0.2:.0f}" rx="{s*0.7:.0f}" ry="{s*0.5:.0f}" fill="#e88a5a" opacity="0.25"/>')
    b.append('<path d="M180 420 Q450 470 720 430" stroke="#4a1406" stroke-width="22" opacity="0.4" fill="none"/>')
    b.append('<ellipse cx="450" cy="40" rx="140" ry="40" fill="#fff4ec" opacity="0.85"/>')
    b.append('<circle cx="450" cy="450" r="440" fill="none" stroke="#ffb08a" stroke-width="10" opacity="0.4"/>')
    guardar("marte_planeta", "".join(b), w, w, d)


def grano_polvo():
    """Grano de polvo marciano visto muy de cerca: roca rojiza con facetas."""
    w = 500
    d = rg("gp_b", (0, "#f0a070", 1), (0.6, "#a8482a", 1), (1, "#4a1608", 1), cx=0.35, cy=0.3, r=0.8)
    b = ['<path d="M250 40 L400 110 L460 260 L390 420 L220 460 L80 380 L40 220 L120 90 Z" fill="url(#gp_b)" stroke="#3a1006" stroke-width="6"/>',
         '<path d="M250 40 L270 220 L460 260 M270 220 L220 460 M270 220 L80 380 M270 220 L120 90" stroke="#3a1006" stroke-width="3" opacity="0.4" fill="none"/>',
         '<path d="M120 90 L250 40 L270 220 Z" fill="#ffd0a0" opacity="0.3"/>']
    guardar("grano_polvo", "".join(b), w, w, d)


def luz_colores(nombre="rayo_luz"):
    """Haz de luz blanca que se abre en tres colores (azul, amarillo, rojo)."""
    w, h = 1000, 300
    b = ['<path d="M0 130 L420 130 L420 170 L0 170 Z" fill="#fffbe8" opacity="0.95"/><path d="M0 120 L420 120 L420 180 L0 180 Z" fill="#fff" opacity="0.3" filter="url(#blur8)"/>']
    for dy, c in [(-110, "#ffd23f"), (0, "#4aa8ff"), (110, "#ff5a3a")]:
        b.append(f'<path d="M420 140 L1000 {140+dy} L1000 {160+dy} L420 160 Z" fill="{c}" opacity="0.9"/>')
    guardar(nombre, "".join(b), w, h)


def tormenta_polvo():
    w, h = 1300, 900
    r = random.Random(9)
    b = []
    for _ in range(60):
        x, y, s = r.uniform(100, 1200), r.uniform(200, 800), r.uniform(80, 220)
        c = r.choice(["#c88a5a", "#a86a3a", "#e0a874", "#8a4a2a"])
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s:.0f}" fill="{c}" opacity="0.35" filter="url(#blur20)"/>')
    guardar("tormenta_polvo", "".join(b), w, h)


def barra_aire(nombre, lleno, color):
    """Bote de aire: cilindro de cristal con nivel."""
    w, h = 300, 700
    d = lg(f"{nombre}_v", (0, "#ffffff"), (0.3, "#c8e0f0"), (1, "#7a9ab0"), x2=1, y2=0)
    alto = 560 * lleno
    b = ['<ellipse cx="150" cy="680" rx="130" ry="18" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         '<rect x="30" y="80" width="240" height="590" rx="40" fill="#0a1424" opacity="0.6"/>',
         f'<rect x="40" y="{660 - alto:.0f}" width="220" height="{max(alto, 6):.0f}" rx="30" fill="{color}"/>',
         f'<rect x="40" y="{660 - alto:.0f}" width="220" height="14" rx="7" fill="#ffffff" opacity="0.5"/>',
         f'<rect x="30" y="80" width="240" height="590" rx="40" fill="url(#{nombre}_v)" opacity="0.3" stroke="#e8f4ff" stroke-width="6"/>',
         '<rect x="70" y="40" width="160" height="50" rx="10" fill="#7a8a9a"/>']
    guardar(nombre, "".join(b), w, h, d)


def sol_disco(nombre, color, r=220):
    w = 2 * r + 120
    c = w / 2
    d = rg(f"{nombre}_g", (0, "#ffffff", 1), (0.4, color, 1), (0.75, color, 0.4), (1, color, 0))
    guardar(nombre, f'<circle cx="{c}" cy="{c}" r="{c}" fill="url(#{nombre}_g)"/><circle cx="{c}" cy="{c}" r="{r*0.55:.0f}" fill="#fff8f4"/>', w, w, d)


# ====================================================================== 02 · HUESOS
HUESO = "#f2ead8"
HSOMBRA = "#b8a888"


def _hueso(x0, y0, x1, y1, g, cab=1.0, col=HUESO):
    """Hueso largo con dos cabezas redondeadas."""
    ang = math.atan2(y1 - y0, x1 - x0)
    nx, ny = -math.sin(ang), math.cos(ang)
    r = g * 0.9 * cab
    b = [f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="{HSOMBRA}" stroke-width="{g+6:.0f}" stroke-linecap="round"/>',
         f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="{col}" stroke-width="{g:.0f}" stroke-linecap="round"/>']
    for (x, y) in ((x0, y0), (x1, y1)):
        for s in (1, -1):
            b.append(f'<circle cx="{x + nx*s*g*0.45:.0f}" cy="{y + ny*s*g*0.45:.0f}" r="{r:.0f}" fill="{col}" stroke="{HSOMBRA}" stroke-width="3"/>')
    b.append(f'<path d="M{x0 + nx*g*0.25:.0f} {y0 + ny*g*0.25:.0f} L{x1 + nx*g*0.25:.0f} {y1 + ny*g*0.25:.0f}" stroke="#ffffff" stroke-width="{max(2, g*0.18):.0f}" opacity="0.6" stroke-linecap="round"/>')
    return "".join(b)


def bg_rayos_x(nombre="bg_rayos_x"):
    """Negatoscopio: fondo azul oscuro con cuadrícula y brillo."""
    d = lg("rx_c", (0, "#06142a"), (0.5, "#0c2a4a"), (1, "#041020")) + rg("rx_l", (0, "#5ab8ff", 0.35), (1, "#5ab8ff", 0))
    b = ['<rect width="1080" height="1920" fill="url(#rx_c)"/>', '<ellipse cx="540" cy="960" rx="700" ry="900" fill="url(#rx_l)"/>']
    for x in range(0, 1081, 90):
        b.append(f'<path d="M{x} 0 L{x} 1920" stroke="#5ab8ff" stroke-width="1.5" opacity="0.12"/>')
    for y in range(0, 1921, 90):
        b.append(f'<path d="M0 {y} L1080 {y}" stroke="#5ab8ff" stroke-width="1.5" opacity="0.12"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def _mano(x, y, s, rot=0, col=HUESO):
    """Huesos de la mano (27): carpo, 5 metacarpianos, falanges."""
    b = [f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">']
    for i in range(8):  # carpo
        b.append(f'<ellipse cx="{-60 + (i%4)*40}" cy="{40 + (i//4)*38}" rx="20" ry="17" fill="{col}" stroke="{HSOMBRA}" stroke-width="3"/>')
    dedos = [(-110, 20, -150, -60, 2), (-60, 0, -70, -200, 3), (-10, -5, -10, -230, 3), (40, 0, 50, -210, 3), (85, 15, 110, -170, 3)]
    for bx, by, tx, ty, n in dedos:
        seg = n + 1
        for k in range(seg):
            x0 = bx + (tx - bx) * k / seg
            y0 = by + (ty - by) * k / seg
            x1 = bx + (tx - bx) * (k + 0.82) / seg
            y1 = by + (ty - by) * (k + 0.82) / seg
            b.append(_hueso(x0, y0, x1, y1, 20 - k * 2.5, 0.75, col))
    b.append('<path d="M-70 120 L-60 260 M30 120 L40 260" stroke="' + col + '" stroke-width="34" stroke-linecap="round"/>')
    b.append("</g>")
    return "".join(b)


def mano_rx():
    w, h = 700, 900
    b = ['<rect x="0" y="0" width="700" height="900" rx="30" fill="#0a2240" opacity="0.0"/>', _mano(350, 560, 1.4)]
    guardar("mano_rx", "".join(b), w, h)


def pie_rx():
    w, h = 700, 900
    b = ['<g transform="translate(350 440)">']
    b.append(f'<ellipse cx="0" cy="300" rx="90" ry="70" fill="{HUESO}" stroke="{HSOMBRA}" stroke-width="4"/>')  # talón
    b.append(f'<ellipse cx="0" cy="190" rx="80" ry="60" fill="{HUESO}" stroke="{HSOMBRA}" stroke-width="4"/>')  # astrágalo
    for i in range(5):
        b.append(f'<ellipse cx="{-70 + i*35}" cy="90" rx="22" ry="30" fill="{HUESO}" stroke="{HSOMBRA}" stroke-width="3"/>')
    for i, (bx, tx) in enumerate([(-80, -120), (-40, -55), (0, 0), (40, 55), (75, 105)]):
        b.append(_hueso(bx, 50, (bx + tx) / 2, -110, 22 if i == 0 else 17, 0.8))
        n = 2 if i == 0 else 3
        for k in range(n):
            y0 = -140 - k * 50
            b.append(_hueso((bx + tx) / 2 + (tx - bx) * 0.1 * k, y0, (bx + tx) / 2 + (tx - bx) * 0.1 * (k + 1), y0 - 34, 16 - k * 2, 0.7))
    b.append("</g>")
    guardar("pie_rx", "".join(b), w, h)


def esqueleto(nombre="esqueleto", s=1.0, bebe=False, col=HUESO):
    """Esqueleto entero de frente, simplificado pero reconocible. bebé: cabeza grande y huesos separados por huecos de cartílago."""
    w, h = 700, 1950
    cab = 150 if bebe else 110
    b = [f'<g transform="translate(350 0)">']
    hy = 40 + cab
    # cráneo
    b.append(f'<ellipse cx="0" cy="{hy}" rx="{cab*0.85:.0f}" ry="{cab:.0f}" fill="{col}" stroke="{HSOMBRA}" stroke-width="5"/>')
    b.append(f'<ellipse cx="-{cab*0.35:.0f}" cy="{hy + cab*0.15:.0f}" rx="{cab*0.2:.0f}" ry="{cab*0.22:.0f}" fill="#1a2a3a"/><ellipse cx="{cab*0.35:.0f}" cy="{hy + cab*0.15:.0f}" rx="{cab*0.2:.0f}" ry="{cab*0.22:.0f}" fill="#1a2a3a"/>')
    b.append(f'<path d="M0 {hy + cab*0.4:.0f} l-12 26 l24 0 Z" fill="#1a2a3a"/>')
    if not bebe:
        b.append(f'<rect x="-{cab*0.45:.0f}" y="{hy + cab*0.72:.0f}" width="{cab*0.9:.0f}" height="{cab*0.3:.0f}" rx="10" fill="{col}" stroke="{HSOMBRA}" stroke-width="4"/>')
        for k in range(6):
            b.append(f'<path d="M{-cab*0.38 + k*cab*0.15:.0f} {hy + cab*0.72:.0f} l0 {cab*0.3:.0f}" stroke="{HSOMBRA}" stroke-width="2"/>')
    if bebe:  # fontanela
        b.append(f'<path d="M0 {hy - cab*0.95:.0f} l{cab*0.25:.0f} {cab*0.25:.0f} l-{cab*0.25:.0f} {cab*0.25:.0f} l-{cab*0.25:.0f} -{cab*0.25:.0f} Z" fill="#e8a0a8" opacity="0.8"/>')
    top = hy + cab + 20
    esc = 0.75 if bebe else 1.0
    gap = 14 if bebe else 4
    # columna
    for k in range(17):
        y = top + k * (34 * esc + gap * 0.3)
        b.append(f'<rect x="-18" y="{y:.0f}" width="36" height="{26*esc:.0f}" rx="8" fill="{col}" stroke="{HSOMBRA}" stroke-width="3"/>')
    # costillas
    for k in range(8):
        y = top + 60 * esc + k * 34 * esc
        L = (150 - abs(k - 3) * 10) * esc
        b.append(f'<path d="M-20 {y:.0f} Q-{L:.0f} {y + 10:.0f} -{L*0.7:.0f} {y + 60*esc:.0f}" stroke="{col}" stroke-width="{14*esc:.0f}" fill="none" stroke-linecap="round"/>')
        b.append(f'<path d="M20 {y:.0f} Q{L:.0f} {y + 10:.0f} {L*0.7:.0f} {y + 60*esc:.0f}" stroke="{col}" stroke-width="{14*esc:.0f}" fill="none" stroke-linecap="round"/>')
    # clavículas y brazos
    sy = top + 40 * esc
    b.append(_hueso(-30, sy, -170 * esc, sy + 10, 16 * esc, 0.8, col) + _hueso(30, sy, 170 * esc, sy + 10, 16 * esc, 0.8, col))
    for s in (-1, 1):
        x0 = s * (180 * esc)
        b.append(_hueso(x0, sy + 30, x0 + s * 30 * esc, sy + 300 * esc, 24 * esc, 1, col))
        b.append(_hueso(x0 + s * 34 * esc, sy + 300 * esc + gap, x0 + s * 50 * esc, sy + 540 * esc, 20 * esc, 1, col))
        b.append(_mano(x0 + s * 56 * esc, sy + 600 * esc + gap, 0.45 * esc, 180, col))
    # pelvis
    py = top + 17 * (34 * esc + gap * 0.3) + 10
    b.append(f'<path d="M-140 {py:.0f} Q-160 {py + 120*esc:.0f} -40 {py + 150*esc:.0f} L40 {py + 150*esc:.0f} Q160 {py + 120*esc:.0f} 140 {py:.0f} Q0 {py + 50:.0f} -140 {py:.0f} Z" fill="{col}" stroke="{HSOMBRA}" stroke-width="5"/>'
             .replace("-140", f"-{140*esc:.0f}").replace(" 140", f" {140*esc:.0f}"))
    # piernas
    for s in (-1, 1):
        x0 = s * 80 * esc
        fy = py + 140 * esc
        b.append(_hueso(x0, fy, x0 + s * 10, fy + 400 * esc, 30 * esc, 1, col))
        b.append(f'<circle cx="{x0 + s*10:.0f}" cy="{fy + 420*esc + gap:.0f}" r="{22*esc:.0f}" fill="{col}" stroke="{HSOMBRA}" stroke-width="3"/>')
        b.append(_hueso(x0 + s * 10, fy + 440 * esc + gap * 2, x0 + s * 16, fy + 790 * esc, 26 * esc, 1, col))
        b.append(f'<ellipse cx="{x0 + s*40:.0f}" cy="{fy + 830*esc + gap:.0f}" rx="{70*esc:.0f}" ry="{24*esc:.0f}" fill="{col}" stroke="{HSOMBRA}" stroke-width="4"/>')
    b.append("</g>")
    guardar(nombre, "".join(b), w, h)


def craneo_bebe(nombre="craneo_bebe", cerrado=0.0):
    """Cráneo de bebé visto desde arriba: placas con la fontanela en medio (rosada). cerrado 0..1."""
    w = 900
    d = rg("cb_b", (0, "#fff8ea", 1), (0.7, HUESO, 1), (1, HSOMBRA, 1), cx=0.4, cy=0.35, r=0.75)
    f = 1 - cerrado
    b = ['<ellipse cx="450" cy="470" rx="330" ry="410" fill="#000" opacity="0.4" filter="url(#blur20)"/>',
         '<ellipse cx="450" cy="450" rx="320" ry="400" fill="#e8a0a8"/>']
    sep = 12 * f + 2
    placas = [  # (path) frontal izq/der, parietal izq/der, occipital
        f"M{450-sep} {170 + 80*f} Q300 60 170 220 Q110 330 140 380 L{450-sep} {340 - 40*f} Z",
        f"M{450+sep} {170 + 80*f} Q600 60 730 220 Q790 330 760 380 L{450+sep} {340 - 40*f} Z",
        f"M{450-sep} {420 + 80*f} L135 {400+sep} Q120 600 260 760 L{450-sep} {700}",
        f"M{450+sep} {420 + 80*f} L765 {400+sep} Q780 600 640 760 L{450+sep} {700}",
        f"M{280} {790} Q450 880 620 790 L{450} {720 + sep} Z",
    ]
    for p in placas:
        b.append(f'<path d="{p}" fill="url(#cb_b)" stroke="{HSOMBRA}" stroke-width="5"/>')
    b.append('<ellipse cx="380" cy="280" rx="60" ry="30" fill="#ffffff" opacity="0.4" filter="url(#blur8)"/>')
    guardar(nombre, "".join(b), w, w, d)


def bebe():
    """Bebé tumbado con pijama, de perfil (silueta amable, ojos cerrados)."""
    w, h = 900, 520
    d = lg("bb_p", (0, "#8ad0f0"), (1, "#3a8ab8")) + rg("bb_c", (0, "#ffe2cc", 1), (0.8, "#f0b898", 1), (1, "#c8806a", 1), cx=0.4, cy=0.35, r=0.7)
    b = ['<ellipse cx="450" cy="490" rx="400" ry="24" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<path d="M300 300 Q320 200 520 210 Q760 220 820 330 Q840 440 760 460 L340 460 Q280 420 300 300 Z" fill="url(#bb_p)"/>',
         '<path d="M760 460 Q860 470 870 420 Q860 380 800 390" fill="url(#bb_p)"/>',
         '<circle cx="230" cy="320" r="150" fill="url(#bb_c)"/>',
         '<path d="M170 330 q22 14 44 0" stroke="#5a3a2a" stroke-width="7" fill="none" stroke-linecap="round"/>',
         '<path d="M110 360 q10 10 24 4" stroke="#c8705a" stroke-width="6" fill="none"/><circle cx="160" cy="370" r="26" fill="#ff8a8a" opacity="0.35"/>',
         '<path d="M260 180 q30 -20 60 6" stroke="#a87050" stroke-width="10" fill="none" stroke-linecap="round"/>',
         '<ellipse cx="420" cy="270" rx="70" ry="40" fill="url(#bb_c)"/>']
    for x in range(380, 800, 70):
        b.append(f'<circle cx="{x}" cy="{300 + (x%140)//2}" r="10" fill="#ffffff" opacity="0.6"/>')
    guardar("bebe", "".join(b), w, h, d)


def bg_cuarto_bebe():
    d = lg("cu_p", (0, "#f4d8c0"), (1, "#e0b898")) + lg("cu_s", (0, "#c88a6a"), (1, "#7a4a3a")) + rg("cu_l", (0, "#fff4d0", 0.8), (1, "#fff4d0", 0))
    b = ['<rect width="1080" height="1920" fill="url(#cu_p)"/>']
    for x in range(0, 1081, 120):
        b.append(f'<path d="M{x} 0 L{x} 1400" stroke="#e8c0a0" stroke-width="30" opacity="0.4"/>')
    b.append('<rect x="620" y="260" width="340" height="440" rx="10" fill="#bfe4ff" stroke="#ffffff" stroke-width="20"/><path d="M790 260 L790 700 M620 480 L960 480" stroke="#fff" stroke-width="14"/>')
    b.append('<ellipse cx="790" cy="480" rx="500" ry="600" fill="url(#cu_l)"/>')
    for k, (x, y, c) in enumerate([(160, 300, "#ffd23f"), (300, 220, "#7df9ff"), (420, 330, "#ff8ab8")]):  # móvil de estrellas
        b.append(f'<path d="M{x} 0 L{x} {y}" stroke="#8a6a5a" stroke-width="3"/><circle cx="{x}" cy="{y+30}" r="30" fill="{c}"/>')
    b.append('<rect x="0" y="1400" width="1080" height="520" fill="url(#cu_s)"/>')
    b.append('<rect x="80" y="1100" width="920" height="40" rx="10" fill="#ffffff"/>')
    for x in range(100, 1000, 70):
        b.append(f'<rect x="{x}" y="1140" width="22" height="420" rx="8" fill="#ffffff"/>')
    b.append('<rect x="80" y="1540" width="920" height="40" rx="10" fill="#ffffff"/>')
    b.append(grano())
    guardar("bg_cuarto_bebe", "".join(b), defs=d)


def femur():
    w, h = 400, 1100
    b = [_hueso(200, 120, 200, 980, 90, 1.1)]
    guardar("femur", "".join(b), w, h)


def estribo():
    """Estribo: el huesecillo con forma de estribo de montar."""
    w, h = 600, 700
    d = rg("es_b", (0, "#fff8ea", 1), (0.7, HUESO, 1), (1, HSOMBRA, 1), cx=0.4, cy=0.3, r=0.8)
    b = ['<ellipse cx="300" cy="660" rx="220" ry="24" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<path d="M300 60 Q340 60 340 110 L340 150 Q520 260 500 560 L100 560 Q80 260 260 150 L260 110 Q260 60 300 60 Z" fill="url(#es_b)" stroke="' + HSOMBRA + '" stroke-width="8"/>',
         '<path d="M300 160 Q470 260 455 540 L145 540 Q130 260 300 160 Z" fill="#14243a"/>',
         '<rect x="70" y="540" width="460" height="60" rx="24" fill="url(#es_b)" stroke="' + HSOMBRA + '" stroke-width="8"/>',
         '<path d="M140 556 L460 556" stroke="#ffffff" stroke-width="8" opacity="0.6"/>']
    guardar("estribo", "".join(b), w, h, d)


def grano_arroz():
    w, h = 400, 700
    d = rg("ar_b", (0, "#ffffff", 1), (0.7, "#f4efe0", 1), (1, "#cfc4a8", 1), cx=0.35, cy=0.3, r=0.8)
    b = ['<ellipse cx="200" cy="660" rx="120" ry="18" fill="#000" opacity="0.3" filter="url(#blur8)"/>',
         '<ellipse cx="200" cy="350" rx="130" ry="300" fill="url(#ar_b)" stroke="#bfb498" stroke-width="5"/>',
         '<path d="M200 80 Q170 350 200 620" stroke="#d8ceb4" stroke-width="5" fill="none"/>',
         '<ellipse cx="160" cy="250" rx="30" ry="90" fill="#fff" opacity="0.6"/>']
    guardar("grano_arroz", "".join(b), w, h, d)


def oreja_corte():
    """Oreja en corte: pabellón, conducto, tímpano y los tres huesecillos con el estribo resaltado."""
    w, h = 1000, 900
    d = rg("or_p", (0, "#ffd0b8", 1), (0.8, "#e8a088", 1), (1, "#a8604a", 1), cx=0.35, cy=0.4, r=0.8)
    b = ['<path d="M80 200 Q60 60 200 60 Q360 60 360 260 Q370 420 300 520 Q240 640 160 640 Q90 640 100 560 Q140 500 120 420 Q60 320 80 200 Z" fill="url(#or_p)" stroke="#a8604a" stroke-width="8"/>',
         '<path d="M150 200 Q160 120 230 130 Q300 150 290 260 Q280 360 230 420" stroke="#c8705a" stroke-width="16" fill="none"/>',
         '<path d="M300 380 L560 380 L560 440 L300 440 Z" fill="#7a3a2a"/>',
         '<ellipse cx="570" cy="410" rx="16" ry="70" fill="#ffd8c0" stroke="#a8604a" stroke-width="5"/>',
         f'<path d="M590 380 Q640 330 660 380 L640 430" stroke="{HUESO}" stroke-width="22" fill="none" stroke-linecap="round"/>',
         f'<path d="M660 380 Q700 360 720 400" stroke="{HUESO}" stroke-width="20" fill="none" stroke-linecap="round"/>',
         f'<path d="M720 400 L780 400 M730 380 Q760 360 780 380 L780 420 Q760 440 730 420" stroke="#ffd23f" stroke-width="12" fill="none" stroke-linecap="round"/>',
         '<path d="M800 300 Q900 260 940 360 Q960 460 880 500 Q800 520 800 440 Q860 440 860 380 Q840 330 800 360 Z" fill="#e8b0c0" stroke="#a8607a" stroke-width="6"/>']
    guardar("oreja_corte", "".join(b), w, h, d)


def pieza_cartilago():
    w, h = 400, 400
    d = rg("ca_b", (0, "#e8f4ff", 1), (0.7, "#a8c8e8", 1), (1, "#6a8ab0", 1), cx=0.35, cy=0.3, r=0.8)
    guardar("cartilago", '<ellipse cx="200" cy="200" rx="170" ry="140" fill="url(#ca_b)" stroke="#6a8ab0" stroke-width="6"/><ellipse cx="150" cy="150" rx="50" ry="26" fill="#fff" opacity="0.6"/>', w, h, d)


def lupa_simple():
    w, h = 500, 700
    b = ['<circle cx="220" cy="220" r="180" fill="#bfe4ff" opacity="0.25" stroke="#2a2a30" stroke-width="30"/>',
         '<path d="M350 350 L470 640" stroke="#3a2a1a" stroke-width="50" stroke-linecap="round"/>',
         '<path d="M120 140 Q170 90 240 90" stroke="#fff" stroke-width="14" opacity="0.7" fill="none" stroke-linecap="round"/>']
    guardar("lupa2", "".join(b), w, h)


# ====================================================================== 03 · GOTAS
AGUA = lambda i: rg(i, (0, "#ffffff", 1), (0.25, "#c8ecff", 0.95), (0.7, "#4ab0f0", 0.9), (1, "#1a5a9a", 0.95), cx=0.35, cy=0.3, r=0.8)  # noqa: E731


def gota_forma(nombre, forma):
    """Gota de agua con volumen: lagrima (la del dibujo), esfera, pan (hamburguesa), paracaidas (bolsa con aro)."""
    w = h = 700
    d = AGUA(f"{nombre}_a")
    sh = '<ellipse cx="350" cy="660" rx="200" ry="22" fill="#000" opacity="0.25" filter="url(#blur8)"/>'
    if forma == "lagrima":
        cuerpo = '<path d="M350 40 Q470 260 540 380 A200 200 0 1 1 160 380 Q230 260 350 40 Z"/>'
    elif forma == "esfera":
        cuerpo = '<circle cx="350" cy="380" r="230"/>'
    elif forma == "pan":
        cuerpo = '<path d="M110 470 Q100 200 350 180 Q600 200 590 470 Q470 430 350 440 Q230 430 110 470 Z"/>'
    else:  # paracaídas: bolsa hinchada hacia arriba con aro grueso abajo
        cuerpo = ('<path d="M120 470 Q90 100 350 90 Q610 100 580 470 Q350 360 120 470 Z" opacity="0.55"/>'
                  '<path d="M90 470 Q350 380 610 470 Q620 520 350 560 Q80 520 90 470 Z"/>')
    cuerpo = cuerpo.replace("/>", f' fill="url(#{nombre}_a)" stroke="#1a6ab0" stroke-width="6"/>')
    brillo = '<ellipse cx="270" cy="300" rx="50" ry="30" fill="#fff" opacity="0.8" transform="rotate(-30 270 300)"/>'
    if forma == "lagrima":
        brillo = '<ellipse cx="290" cy="360" rx="40" ry="70" fill="#fff" opacity="0.7" transform="rotate(20 290 360)"/>'
    if forma == "paracaidas":
        brillo = '<ellipse cx="260" cy="220" rx="60" ry="24" fill="#fff" opacity="0.6" transform="rotate(-20 260 220)"/>'
    guardar(nombre, sh + cuerpo + brillo, w, h, d)


def gotitas(nombre="gotitas", n=9, sem=3):
    r = random.Random(sem)
    w = h = 900
    d = AGUA("gt_a")
    b = []
    for _ in range(n):
        x, y, s = r.uniform(120, 780), r.uniform(120, 780), r.uniform(40, 90)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s:.0f}" fill="url(#gt_a)" stroke="#1a6ab0" stroke-width="4"/><circle cx="{x - s*0.3:.0f}" cy="{y - s*0.3:.0f}" r="{s*0.22:.0f}" fill="#fff" opacity="0.8"/>')
    guardar(nombre, "".join(b), w, h, d)


def pan_hamburguesa():
    w, h = 800, 500
    d = rg("pa_b", (0, "#ffd890", 1), (0.6, "#e09a40", 1), (1, "#9a5a1a", 1), cx=0.4, cy=0.3, r=0.8)
    r = random.Random(4)
    b = ['<ellipse cx="400" cy="460" rx="340" ry="24" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<path d="M70 400 Q60 110 400 90 Q740 110 730 400 Q560 370 400 375 Q240 370 70 400 Z" fill="url(#pa_b)" stroke="#8a4a10" stroke-width="6"/>',
         '<path d="M80 400 Q400 360 720 400 L716 430 Q400 400 84 430 Z" fill="#f4e0b0"/>']
    for _ in range(24):
        x, y = r.uniform(170, 630), r.uniform(150, 300)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="9" ry="5" fill="#fff6dc" transform="rotate({r.uniform(-40, 40):.0f} {x:.0f} {y:.0f})"/>')
    guardar("pan_hamburguesa", "".join(b), w, h, d)


def paracaidas():
    w, h = 700, 800
    d = lg("pc_t", (0, "#ff6a5a"), (1, "#c0392b"), x2=1, y2=0)
    b = ['<path d="M50 330 Q350 -60 650 330 Q570 290 500 330 Q430 290 350 330 Q270 290 200 330 Q130 290 50 330 Z" fill="url(#pc_t)" stroke="#7a1a10" stroke-width="6"/>',
         '<path d="M200 330 Q350 0 500 330" fill="#ffffff" opacity="0.35"/>']
    for x in (60, 200, 350, 500, 640):
        b.append(f'<path d="M{x} 330 L350 640" stroke="#3a2a2a" stroke-width="3"/>')
    b.append('<rect x="320" y="630" width="60" height="80" rx="10" fill="#4a4a5a"/>')
    guardar("paracaidas", "".join(b), w, h, d)


def lapiz():
    w, h = 900, 200
    b = ['<path d="M100 60 L760 60 L760 140 L100 140 Z" fill="#ffd23f" stroke="#a8861e" stroke-width="5"/>',
         '<path d="M100 60 L760 60 L760 85 L100 85 Z" fill="#fff" opacity="0.3"/>',
         '<path d="M760 60 L880 100 L760 140 Z" fill="#f0c890"/><path d="M845 88 L880 100 L845 112 Z" fill="#2a2a30"/>',
         '<rect x="40" y="60" width="70" height="80" fill="#c8c8d0"/><rect x="0" y="60" width="44" height="80" rx="16" fill="#ff8ab8"/>']
    guardar("lapiz", "".join(b), w, h)


def nube(nombre="nube", oscura=False):
    w, h = 1000, 520
    c1, c2 = ("#8a94a8", "#4a5468") if oscura else ("#ffffff", "#c8d4e4")
    d = lg(f"{nombre}_g", (0, c1), (1, c2))
    b = ['<g fill="url(#' + nombre + '_g)">']
    for x, y, r in [(220, 330, 150), (380, 250, 190), (580, 230, 200), (760, 300, 160), (500, 360, 170), (300, 380, 130), (720, 390, 120)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}"/>')
    b.append('</g><rect x="150" y="380" width="700" height="100" rx="50" fill="url(#' + nombre + '_g)"/>')
    guardar(nombre, "".join(b), w, h, d)


def bg_cielo_lluvia(nombre="bg_lluvia", noche=False):
    d = (lg("cl_c", (0, "#3a4458"), (0.6, "#6a7890"), (1, "#8a98ac")) if not noche else lg("cl_c", (0, "#0a1020"), (0.6, "#1a2a44"), (1, "#2a3a54"))) + lg("cl_s", (0, "#2a3440"), (1, "#141a22"))
    r = random.Random(12)
    b = ['<rect width="1080" height="1920" fill="url(#cl_c)"/>']
    for _ in range(14):
        x, y, s = r.uniform(-100, 1180), r.uniform(0, 600), r.uniform(160, 340)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{s:.0f}" ry="{s*0.45:.0f}" fill="#{"2a3244" if not noche else "0c1424"}" opacity="0.6" filter="url(#blur20)"/>')
    # ciudad lejana
    x = 0
    while x < 1080:
        bw, bh = r.uniform(60, 140), r.uniform(200, 520)
        b.append(f'<rect x="{x:.0f}" y="{1500 - bh:.0f}" width="{bw:.0f}" height="{bh + 40:.0f}" fill="#{"4a5466" if not noche else "1a2234"}"/>')
        for _ in range(int(bh / 50)):
            b.append(f'<rect x="{x + r.uniform(8, bw - 20):.0f}" y="{1500 - bh + r.uniform(20, bh - 20):.0f}" width="10" height="14" fill="#ffd27a" opacity="{r.uniform(0.2, 0.8):.2f}"/>')
        x += bw + r.uniform(4, 20)
    b.append('<rect x="0" y="1520" width="1080" height="400" fill="url(#cl_s)"/>')
    for _ in range(18):  # charcos con reflejo
        x, y = r.uniform(0, 1080), r.uniform(1560, 1900)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(60, 160):.0f}" ry="{r.uniform(8, 18):.0f}" fill="#8aa0c0" opacity="0.25"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def ondas_charco():
    w, h = 800, 300
    b = []
    for k, (rx, op) in enumerate([(380, 0.25), (280, 0.4), (180, 0.6), (90, 0.8)]):
        b.append(f'<ellipse cx="400" cy="150" rx="{rx}" ry="{rx*0.28:.0f}" fill="none" stroke="#c8ecff" stroke-width="6" opacity="{op}"/>')
    guardar("ondas_charco", "".join(b), w, h)


def velocimetro():
    """Marcador de velocidad genérico con aguja (36 km/h)."""
    w, h = 800, 520
    d = lg("ve_c", (0, "#2a3040"), (1, "#0a0e18"))
    b = ['<path d="M60 460 A340 340 0 0 1 740 460 Z" fill="url(#ve_c)" stroke="#7df9ff" stroke-width="8"/>']
    for k in range(13):
        a = math.pi + k * math.pi / 12
        x0, y0 = 400 + 300 * math.cos(a), 460 + 300 * math.sin(a)
        x1, y1 = 400 + 330 * math.cos(a), 460 + 330 * math.sin(a)
        b.append(f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#ffffff" stroke-width="{8 if k%3==0 else 4}"/>')
    b.append('<circle cx="400" cy="460" r="30" fill="#ff3d3d"/>')
    guardar("velocimetro", "".join(b), w, h, d)


def aguja_vel():
    w, h = 600, 60
    guardar("aguja_vel", '<path d="M300 22 L590 30 L300 38 Z" fill="#ff3d3d"/><circle cx="300" cy="30" r="22" fill="#ff3d3d"/>', w, h)


def montana_nube():
    """Perfil: suelo con montaña y una nube muy alta con la cota marcada."""
    d = lg("mn_c", (0, "#4a6a9a"), (1, "#a8c8e8")) + lg("mn_m", (0, "#5a6a5a"), (1, "#2a3a2a"))
    b = ['<rect width="1080" height="1920" fill="url(#mn_c)"/>',
         '<path d="M-40 1700 L300 1300 L460 1450 L700 1100 L1120 1700 L1120 1920 L-40 1920 Z" fill="url(#mn_m)"/>',
         '<path d="M700 1100 L640 1180 L680 1170 L720 1200 L760 1160 Z" fill="#f4f8ff"/>',
         '<rect x="-40" y="1700" width="1160" height="220" fill="#2a3a2a"/>']
    b.append(grano())
    guardar("bg_perfil_nube", "".join(b), defs=d)


def lluvia_lineas(nombre="lluvia_lineas", sem=8, n=160):
    r = random.Random(sem)
    b = []
    for _ in range(n):
        x, y, L = r.uniform(0, 1080), r.uniform(0, 2300), r.uniform(40, 110)
        b.append(f'<path d="M{x:.0f} {y:.0f} l-8 {L:.0f}" stroke="#c8e4ff" stroke-width="{r.uniform(2, 4):.1f}" opacity="{r.uniform(0.25, 0.6):.2f}" stroke-linecap="round"/>')
    guardar(nombre, "".join(b), 1080, 2300)


def generar(dirsvg):
    ilus.OUT = dirsvg
    # 01
    bg_marte("bg_marte_dia", "dia"); bg_marte("bg_marte_atardecer", "tarde"); bg_tierra_atardecer(); rover()
    foto_marco("foto_azul", True); foto_marco("foto_dia", False); marte_planeta(); grano_polvo(); luz_colores(); tormenta_polvo()
    barra_aire("aire_tierra", 1.0, "#5ab8ff"); barra_aire("aire_marte", 0.01, "#ff8a5a")
    sol_disco("sol_tierra", "#ffd060", 220); sol_disco("sol_marte", "#ffc0d0", 150)
    # 02
    bg_rayos_x(); mano_rx(); pie_rx(); esqueleto("esqueleto"); esqueleto("esqueleto_bebe", bebe=True); craneo_bebe("craneo_bebe", 0.0); craneo_bebe("craneo_cerrado", 1.0)
    bebe(); bg_cuarto_bebe(); femur(); estribo(); grano_arroz(); oreja_corte(); pieza_cartilago(); lupa_simple()
    # 03
    for f in ("lagrima", "esfera", "pan", "paracaidas"):
        gota_forma(f"gota_{f}", f)
    gotitas(); pan_hamburguesa(); paracaidas(); lapiz(); nube("nube"); nube("nube_oscura", True); bg_cielo_lluvia("bg_lluvia"); bg_cielo_lluvia("bg_lluvia_noche", True)
    ondas_charco(); velocimetro(); aguja_vel(); montana_nube(); lluvia_lineas()
    return dirsvg


if __name__ == "__main__":
    generar(sys.argv[1])
    print("SVG en", sys.argv[1])
