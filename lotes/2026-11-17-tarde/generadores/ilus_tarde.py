"""Ilustraciones del lote 2026-11-17-tarde (rayo más caliente que el Sol, luz del Sol con retraso, cebolla).
Uso: python3 ilus_tarde.py DIR_SVG   (semillas fijas). Ladrillos de motor/biblioteca/ilus.py.
Reutiliza también las del lote 2026-11-17-manana (casa, edificio, cocina, laboratorio, átomo, nube de gas…)."""
import math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "lotes", "2026-11-17-manana", "generadores"))
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano, _hoja, _neb, _mascara, _estrellas_ricas, _animal, _pata  # noqa: E402,F401
import ilus_lote  # noqa: E402


# ====================================================================== 01 · rayo
def _zigzag(r, x0, y0, y1, amp, pasos):
    pts = [(x0, y0)]
    for k in range(1, pasos + 1):
        y = y0 + (y1 - y0) * k / pasos
        pts.append((x0 + r.uniform(-amp, amp) + (k * 6 if k % 3 == 0 else 0), y))
    return pts


def rayo(nombre="rayo", sem=3, w=700, h=1600, ramas=4):
    r = random.Random(sem)
    tronco = _zigzag(r, w / 2, 0, h, 90, 16)
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in tronco)
    rs = []
    for _ in range(ramas):
        i = r.randint(2, 11)
        x, y = tronco[i]
        lado = r.choice([-1, 1])
        pts = [(x, y)]
        for k in range(r.randint(3, 6)):
            x += lado * r.uniform(30, 80); y += r.uniform(40, 90)
            pts.append((x, y))
        rs.append("M" + " L".join(f"{a:.0f} {b:.0f}" for a, b in pts))
    b = [f'<path d="{d}" stroke="#7ad8ff" stroke-width="70" fill="none" opacity="0.35" filter="url(#blur40)"/>',
         f'<path d="{d}" stroke="#bfe9ff" stroke-width="30" fill="none" opacity="0.7" filter="url(#blur8)"/>',
         *[f'<path d="{p}" stroke="#9fe0ff" stroke-width="14" fill="none" opacity="0.6" filter="url(#blur8)"/>' for p in rs],
         *[f'<path d="{p}" stroke="#ffffff" stroke-width="5" fill="none" stroke-linejoin="round"/>' for p in rs],
         f'<path d="{d}" stroke="#ffffff" stroke-width="12" fill="none" stroke-linejoin="round"/>']
    guardar(nombre, "".join(b), w, h)


def nube_tormenta(nombre="nube", sem=2, w=1200, h=600, tono="#2a2a44"):
    r = random.Random(sem)
    d = lg(f"{nombre}_g", (0, "#6a6a90"), (0.5, tono), (1, "#0e0e1e")) + rg(f"{nombre}_l", (0, "#bfe9ff", 0.7), (1, "#bfe9ff", 0))
    b = []
    for k in range(26):
        x, y = r.uniform(120, w - 120), r.uniform(150, h - 160)
        rr = r.uniform(90, 190)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.0f}" fill="url(#{nombre}_g)"/>')
    b.append(f'<rect y="{h-170}" width="{w}" height="170" fill="#0e0e1e" opacity="0.6" filter="url(#blur20)"/>')
    b.append(f'<ellipse cx="{w/2}" cy="{h*0.65}" rx="{w*0.25}" ry="{h*0.2}" fill="url(#{nombre}_l)" opacity="0.6"/>')
    b.append(f'<rect width="{w}" height="{h}" fill="#888" filter="url(#grano)" opacity="0.6"/>')
    guardar(nombre, f'<g filter="url(#blur8)">{"".join(b[:-3])}</g>' + "".join(b[-3:]), w, h, d)


def bg_tormenta():
    r = random.Random(14)
    d = (lg("tor_c", (0, "#0a0a1e"), (0.5, "#1e1a40"), (0.8, "#3a2a5a"), (1, "#0a0a14")) +
         rg("tor_l", (0, "#9fd8ff", 0.5), (1, "#9fd8ff", 0)) + lg("tor_s", (0, "#14142a"), (1, "#05050c")) + _neb("tn1", "#5a4a9a", 3, 0.003, 2.2, 0.9))
    b = ['<rect width="1080" height="1920" fill="url(#tor_c)"/>',
         '<rect width="1080" height="1920" filter="url(#tn1)" opacity="0.5"/>',
         '<ellipse cx="540" cy="700" rx="700" ry="500" fill="url(#tor_l)" opacity="0.5"/>']
    # colinas y ciudad lejana
    b.append('<path d="M0 1450 C200 1380 380 1420 560 1390 C760 1360 900 1410 1080 1380 L1080 1920 L0 1920 Z" fill="#1a1630"/>')
    x = 0
    while x < 1080:
        bw, bh = r.uniform(40, 90), r.uniform(60, 220)
        b.append(f'<rect x="{x:.0f}" y="{1440-bh:.0f}" width="{bw:.0f}" height="{bh+40:.0f}" fill="#120f22"/>')
        for _ in range(r.randint(1, 5)):
            b.append(f'<rect x="{x+r.uniform(5,bw-12):.0f}" y="{1440-bh+r.uniform(10,bh-10):.0f}" width="7" height="9" fill="#ffd27a" opacity="{r.uniform(0.4,0.9):.2f}"/>')
        x += bw + r.uniform(2, 14)
    b.append('<path d="M0 1560 C260 1520 520 1580 760 1540 C900 1520 1000 1550 1080 1540 L1080 1920 L0 1920 Z" fill="url(#tor_s)"/>')
    for _ in range(140):  # lluvia
        x0, y0 = r.uniform(0, 1180), r.uniform(0, 1800)
        b.append(f'<path d="M{x0:.0f} {y0:.0f} l-14 46" stroke="#9fb8ff" stroke-width="2" opacity="{r.uniform(0.15,0.4):.2f}"/>')
    b.append(grano())
    guardar("bg_tormenta", "".join(b), defs=d)


def termometro(nombre="termometro", nivel=0.3, color="#ff3d3d"):
    w, h = 300, 1000
    d = lg(f"{nombre}_v", (0, "#ffffff55"), (0.5, "#ffffff22"), (1, "#ffffff55"), x2=1, y2=0)
    alto = 700 * nivel
    b = ['<ellipse cx="150" cy="985" rx="110" ry="12" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         '<rect x="105" y="60" width="90" height="780" rx="45" fill="#1a1f2e"/>',
         f'<circle cx="150" cy="870" r="95" fill="#1a1f2e"/><circle cx="150" cy="870" r="78" fill="{color}"/>',
         f'<rect x="125" y="{840-alto:.0f}" width="50" height="{alto+40:.0f}" rx="25" fill="{color}"/>',
         '<circle cx="125" cy="845" r="22" fill="#ffffff" opacity="0.5"/>',
         *[f'<path d="M200 {y} l{30 if (k % 2 == 0) else 18} 0" stroke="#ffffff" stroke-width="5"/>' for k, y in enumerate(range(140, 820, 70))],
         '<rect x="105" y="60" width="90" height="780" rx="45" fill="url(#' + nombre + '_v)"/>',
         '<rect x="105" y="60" width="90" height="780" rx="45" fill="none" stroke="#dfe8ff" stroke-width="6"/>']
    guardar(nombre, "".join(b), w, h, d)


def onda(nombre="onda", color="#bfe9ff"):
    w = h = 800
    b = [f'<circle cx="400" cy="400" r="{r}" fill="none" stroke="{color}" stroke-width="{s}" opacity="{o}"/>'
         for r, s, o in [(380, 10, 0.25), (330, 16, 0.45), (280, 24, 0.8), (240, 10, 0.4)]]
    guardar(nombre, '<g filter="url(#blur8)">' + "".join(b) + '</g>' + "".join(b), w, h)


def oreja():
    w, h = 600, 800
    d = lg("or_p", (0, "#f2c09a"), (0.6, "#d8936a"), (1, "#a8623e")) + lg("or_s", (0, "#7a3a20"), (1, "#5a2410"))
    b = ['<path d="M300 60 C470 60 560 200 540 360 C525 470 450 520 430 600 C410 700 330 760 250 740 C180 720 170 650 210 620 '
         'C260 580 250 520 220 470 C150 380 120 300 140 200 C160 110 220 60 300 60 Z" fill="url(#or_p)"/>',
         '<path d="M300 140 C410 140 470 230 455 340 C445 410 395 440 380 500 C368 550 330 580 300 560" stroke="url(#or_s)" stroke-width="34" fill="none" stroke-linecap="round"/>',
         '<path d="M300 260 C360 260 380 320 360 380 C345 420 300 420 290 390" stroke="#8a4628" stroke-width="22" fill="none" stroke-linecap="round"/>',
         '<ellipse cx="300" cy="380" rx="45" ry="60" fill="#3a1408"/>',
         '<path d="M300 60 C470 60 560 200 540 360" stroke="#ffe0c8" stroke-width="10" fill="none" opacity="0.6"/>', grano(w, h)]
    guardar("oreja", "".join(b), w, h, d)


def campo_noche():
    """Paisaje abierto de noche con un camino y postes (para contar kilómetros)."""
    r = random.Random(5)
    d = lg("cn_c", (0, "#0b0b22"), (0.55, "#2a2450"), (1, "#151228")) + lg("cn_t", (0, "#1f2a24"), (1, "#0a120e"))
    b = ['<rect width="1080" height="1920" fill="url(#cn_c)"/>', *[f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,900):.0f}" r="{r.uniform(1,2.4):.1f}" fill="#fff" opacity="{r.uniform(0.2,0.8):.2f}"/>' for _ in range(90)],
         '<path d="M0 1150 C300 1110 700 1160 1080 1120 L1080 1920 L0 1920 Z" fill="url(#cn_t)"/>',
         '<path d="M480 1150 L600 1150 L1000 1920 L80 1920 Z" fill="#2a2a30"/>',
         *[f'<path d="M{540-4+(k*k*0.9):.0f} {1150+k*k*9:.0f} l{6+k:.0f} 0 l{4+k:.0f} {20+k*4:.0f} l-{10+2*k:.0f} 0 Z" fill="#ffd23f" opacity="0.8"/>' for k in range(1, 14)],
         *[f'<rect x="{x}" y="{y}" width="{wd}" height="{hh}" fill="#0c0c14"/>' for x, y, wd, hh in [(380, 1080, 8, 90), (300, 1060, 10, 140), (180, 1020, 14, 220), (20, 960, 20, 360)]],
         grano()]
    guardar("campo_noche", "".join(b), defs=d)


def refugio():
    """Casa con ventanas encendidas bajo la lluvia (refugio cerrado)."""
    w, h = 800, 700
    d = lg("rf_m", (0, "#c8b8a0"), (1, "#7a6a58")) + lg("rf_t", (0, "#8a2a1a"), (1, "#4a1408")) + rg("rf_v", (0, "#ffe9a8", 1), (1, "#ffb84a", 1))
    b = ['<ellipse cx="400" cy="680" rx="380" ry="20" fill="#000" opacity="0.5" filter="url(#blur8)"/>',
         '<rect x="120" y="300" width="560" height="380" fill="url(#rf_m)"/>', '<path d="M80 320 L400 80 L720 320 Z" fill="url(#rf_t)"/>',
         '<rect x="190" y="390" width="140" height="130" fill="url(#rf_v)"/><rect x="470" y="390" width="140" height="130" fill="url(#rf_v)"/>',
         '<path d="M260 390 L260 520 M190 455 L330 455 M540 390 L540 520 M470 455 L610 455" stroke="#5a4030" stroke-width="10"/>',
         '<rect x="350" y="540" width="100" height="140" fill="#4a2a18"/><circle cx="430" cy="610" r="7" fill="#ffd27a"/>',
         '<rect x="560" y="120" width="60" height="140" fill="#5a3a2a"/>', grano(w, h)]
    guardar("refugio", "".join(b), w, h, d)


def persona_cuenta():
    """Silueta a contraluz mirando la tormenta con la mano alzada (contando con los dedos). Sin rasgos."""
    w, h = 500, 1000
    b = ['<ellipse cx="250" cy="985" rx="160" ry="14" fill="#000" opacity="0.5" filter="url(#blur8)"/>',
         '<circle cx="250" cy="170" r="80" fill="#0b0b16"/>',
         '<path d="M150 300 C170 260 330 260 350 300 L380 600 L330 610 L320 960 L265 960 L250 680 L235 960 L180 960 L170 610 L120 600 Z" fill="#0b0b16"/>',
         '<path d="M345 310 L440 200 L455 120" stroke="#0b0b16" stroke-width="48" stroke-linecap="round" fill="none"/>',
         *[f'<path d="M455 120 l{dx} -60" stroke="#0b0b16" stroke-width="14" stroke-linecap="round"/>' for dx in (-24, -6, 12)],
         '<path d="M330 120 C350 140 352 210 330 240" stroke="#9fd8ff" stroke-width="6" fill="none" opacity="0.7"/>',
         '<path d="M345 310 L440 200 L455 120" stroke="#9fd8ff" stroke-width="5" fill="none" opacity="0.4"/>']
    guardar("persona_cuenta", "".join(b), w, h)


# ---------------------------------------------------------------- v2 del 01: más tipos de rayo (petición de cambios, 2026-11-17)
def _trazo(r, p0, p1, pasos, amp):
    (x0, y0), (x1, y1) = p0, p1
    pts = [(x0, y0)]
    for k in range(1, pasos):
        u = k / pasos
        nx, ny = -(y1 - y0), (x1 - x0)
        L = math.hypot(nx, ny) or 1
        o = r.uniform(-amp, amp)
        pts.append((x0 + (x1 - x0) * u + nx / L * o, y0 + (y1 - y0) * u + ny / L * o))
    pts.append((x1, y1))
    return pts


def _dibuja_rayo(caminos, color="#bfe9ff", nucleo="#ffffff", g=12):
    b = []
    for pts, peso in caminos:
        d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
        b.append(f'<path d="{d}" stroke="{color}" stroke-width="{g*5*peso:.0f}" fill="none" opacity="0.3" filter="url(#blur40)"/>')
        b.append(f'<path d="{d}" stroke="{color}" stroke-width="{g*2.2*peso:.0f}" fill="none" opacity="0.65" filter="url(#blur8)"/>')
    for pts, peso in caminos:
        d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
        b.append(f'<path d="{d}" stroke="{nucleo}" stroke-width="{max(2, g*peso):.1f}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
    return "".join(b)


def rayo_horizontal(nombre="rayo_horizontal", sem=31, w=1600, h=700, color="#d8b8ff"):
    """Rayo entre nubes (intranube): avanza de lado con muchas ramas finas."""
    r = random.Random(sem)
    tronco = _trazo(r, (0, h * 0.45), (w, h * 0.5), 26, 70)
    cam = [(tronco, 1.0)]
    for _ in range(9):
        i = r.randint(2, 22); x, y = tronco[i]
        fin = (x + r.uniform(80, 260), y + r.choice([-1, 1]) * r.uniform(100, 280))
        cam.append((_trazo(r, (x, y), fin, 7, 30), 0.4))
    guardar(nombre, _dibuja_rayo(cam, color, g=9), w, h)


def rayo_ramificado(nombre="rayo_ramificado", sem=44, w=1080, h=1600, color="#ffb8f0"):
    """Rayo en árbol: varias ramas grandes que bajan abiertas en abanico (tono violeta)."""
    r = random.Random(sem)
    tronco = _trazo(r, (w * 0.45, 0), (w * 0.55, h), 20, 80)
    cam = [(tronco, 1.0)]
    for _ in range(7):
        i = r.randint(3, 13); x, y = tronco[i]
        lado = r.choice([-1, 1])
        fin = (x + lado * r.uniform(200, 420), y + r.uniform(250, 600))
        rama = _trazo(r, (x, y), fin, 10, 40)
        cam.append((rama, 0.55))
        j = r.randint(2, 7); xx, yy = rama[j]
        cam.append((_trazo(r, (xx, yy), (xx + lado * r.uniform(60, 180), yy + r.uniform(80, 200)), 5, 20), 0.3))
    guardar(nombre, _dibuja_rayo(cam, color, "#fff6ff", 11), w, h)


def rayo_doble(nombre="rayo_doble", sem=52, w=1080, h=1600):
    """Dos descargas a la vez que bajan separadas (una ámbar y otra blanca)."""
    r = random.Random(sem)
    a = _trazo(r, (260, 0), (330, h), 18, 60)
    b = _trazo(r, (800, 120), (720, h), 16, 55)
    cuerpo = _dibuja_rayo([(a, 0.9)], "#ffd27a", "#fffbe8", 10) + _dibuja_rayo([(b, 0.8)], "#bfe9ff", "#ffffff", 10)
    guardar(nombre, cuerpo, w, h)


def canal_plasma():
    """Primer plano del canal del rayo: tubo de aire incandescente de pocos centímetros, con capas de calor."""
    w, h = 1080, 1920
    r = random.Random(61)
    pts = _trazo(r, (540, 0), (550, 1920), 14, 60)
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
    b = [f'<path d="{d}" stroke="#ff5a1a" stroke-width="320" fill="none" opacity="0.25" filter="url(#blur40)"/>',
         f'<path d="{d}" stroke="#ffb02e" stroke-width="160" fill="none" opacity="0.45" filter="url(#blur20)"/>',
         f'<path d="{d}" stroke="#fff3c0" stroke-width="70" fill="none" opacity="0.9" filter="url(#blur8)"/>',
         f'<path d="{d}" stroke="#ffffff" stroke-width="30" fill="none"/>']
    guardar("canal_plasma", "".join(b), w, h)


def arbol_tormenta(nombre="arbol", quemado=False):
    """Árbol solitario en silueta (el rayo le cae encima)."""
    w, h = 800, 1000
    r = random.Random(71)
    col = "#1a120c" if not quemado else "#2a1206"
    b = ['<ellipse cx="400" cy="985" rx="300" ry="16" fill="#000" opacity="0.5" filter="url(#blur8)"/>',
         f'<path d="M370 990 C380 800 360 650 390 520 L410 520 C440 650 420 800 430 990 Z" fill="{col}"/>']
    def rama(x, y, ang, L, g, n):
        if n == 0 or L < 20: return
        x2, y2 = x + L * math.cos(ang), y + L * math.sin(ang)
        b.append(f'<path d="M{x:.0f} {y:.0f} L{x2:.0f} {y2:.0f}" stroke="{col}" stroke-width="{g:.0f}" stroke-linecap="round"/>')
        for da in (-0.45, 0.4):
            rama(x2, y2, ang + da + r.uniform(-0.15, 0.15), L * 0.72, g * 0.65, n - 1)
    rama(400, 540, -math.pi / 2, 170, 30, 6)
    if quemado:
        b.append('<path d="M400 520 L405 990" stroke="#ff8a1a" stroke-width="10" opacity="0.9"/>')
        b.append('<ellipse cx="400" cy="400" rx="260" ry="200" fill="#ff8a1a" opacity="0.25" filter="url(#blur40)"/>')
    guardar(nombre, "".join(b), w, h)


def bg_mar_tormenta():
    """Mar de noche bajo tormenta, con olas y reflejos."""
    r = random.Random(81)
    d = lg("mt_c", (0, "#05060f"), (0.45, "#22183c"), (0.62, "#3a2a5a"), (1, "#05060f")) + lg("mt_m", (0, "#1a2240"), (1, "#03050c")) + _neb("mt_n", "#4a3a8a", 6, 0.0035, 2.2, 0.9)
    b = ['<rect width="1080" height="1920" fill="url(#mt_c)"/>', '<rect width="1080" height="1200" filter="url(#mt_n)" opacity="0.6"/>',
         '<rect y="1180" width="1080" height="740" fill="url(#mt_m)"/>']
    for k in range(60):
        y = 1190 + (k ** 1.35) * 2.2
        if y > 1920: break
        x = r.uniform(-100, 1080)
        b.append(f'<path d="M{x:.0f} {y:.0f} q{40+k:.0f} -{6+k*0.2:.0f} {80+k*2:.0f} 0" stroke="#8aa0d8" stroke-width="{2+k*0.08:.1f}" fill="none" opacity="{r.uniform(0.15,0.4):.2f}"/>')
    b.append('<path d="M0 1180 L1080 1180" stroke="#9fb8ff" stroke-width="3" opacity="0.4"/>')
    b.append('<path d="M760 1180 l20 0 l40 600 l-100 0 Z" fill="#bfe9ff" opacity="0.12" filter="url(#blur20)"/>')  # reflejo del rayo
    b.append(grano())
    guardar("bg_mar_tormenta", "".join(b), defs=d)


def yunque():
    """Nube de tormenta en yunque (cumulonimbo) vista de lejos: el rayo puede salir por un lado, a cielo despejado."""
    w, h = 1080, 900
    r = random.Random(91)
    d = lg("yu_g", (0, "#d8d0f0"), (0.5, "#7a6aa0"), (1, "#2a2244"))
    b = ['<path d="M80 260 C200 160 420 130 540 140 C700 120 900 170 1040 250 C960 290 760 300 640 310 L620 760 L420 760 L420 310 C300 300 180 300 80 260 Z" fill="url(#yu_g)"/>']
    for _ in range(30):
        b.append(f'<circle cx="{r.uniform(430,620):.0f}" cy="{r.uniform(320,760):.0f}" r="{r.uniform(50,110):.0f}" fill="url(#yu_g)" opacity="0.9"/>')
    b.append('<rect x="380" y="760" width="300" height="140" fill="#1a1630" opacity="0.6" filter="url(#blur20)"/>')
    guardar("yunque", '<g filter="url(#blur8)">' + "".join(b) + '</g>', w, h, d)


def bg_cielo_despejado():
    r = random.Random(95)
    d = lg("cd_c", (0, "#0a0f2a"), (0.6, "#24305a"), (1, "#0a0c18"))
    b = ['<rect width="1080" height="1920" fill="url(#cd_c)"/>',
         *[f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1300):.0f}" r="{r.uniform(1,2.6):.1f}" fill="#fff" opacity="{r.uniform(0.3,0.9):.2f}"/>' for _ in range(160)],
         '<path d="M0 1500 C300 1460 700 1520 1080 1480 L1080 1920 L0 1920 Z" fill="#0c1410"/>', grano()]
    guardar("bg_cielo_despejado", "".join(b), defs=d)


# ====================================================================== 02 · Sol
def sol_corte():
    """Sol cortado: núcleo, zona radiativa (donde la luz rebota) y zona convectiva."""
    w = h = 1000
    r = random.Random(4)
    d = (rg("sc_conv", (0, "#ff8a1a", 1), (0.8, "#ff5a0a", 1), (1, "#b82a00", 1)) + rg("sc_rad", (0, "#ffd84a", 1), (1, "#ff9a1a", 1)) +
         rg("sc_nuc", (0, "#ffffff", 1), (0.5, "#fff6b0", 1), (1, "#ffd23f", 1)) + rg("sc_hal", (0, "#ffb02e", 0.6), (1, "#ffb02e", 0)))
    b = ['<circle cx="500" cy="500" r="500" fill="url(#sc_hal)"/>',
         '<circle cx="500" cy="500" r="430" fill="url(#sc_conv)"/>']
    for k in range(40):  # granulación de la zona convectiva
        a = r.uniform(0, 2 * math.pi); rr = r.uniform(330, 420)
        b.append(f'<circle cx="{500+rr*math.cos(a):.0f}" cy="{500+rr*math.sin(a):.0f}" r="{r.uniform(10,26):.0f}" fill="#ffd27a" opacity="0.35"/>')
    b += ['<circle cx="500" cy="500" r="310" fill="url(#sc_rad)"/>',
          '<circle cx="500" cy="500" r="310" fill="none" stroke="#fff3c0" stroke-width="4" stroke-dasharray="14 10" opacity="0.7"/>',
          '<circle cx="500" cy="500" r="120" fill="url(#sc_nuc)"/>',
          '<circle cx="500" cy="500" r="120" fill="none" stroke="#ffffff" stroke-width="6" opacity="0.8" filter="url(#blur8)"/>',
          '<rect width="1000" height="1000" fill="#888" filter="url(#grano)" opacity="0.4"/>']
    guardar("sol_corte", "".join(b), w, h, d)


def foton():
    w = h = 200
    d = rg("fo_g", (0, "#ffffff", 1), (0.3, "#fff3a0", 1), (1, "#ffd23f", 0))
    guardar("foton", '<circle cx="100" cy="100" r="96" fill="url(#fo_g)"/><circle cx="100" cy="100" r="22" fill="#ffffff"/>', w, h, d)


def ojo(nombre="ojo", iris="#3a8a5a", lloroso=False):
    w, h = 900, 520
    d = (rg(f"{nombre}_i", (0, "#0a0a0a", 1), (0.35, "#0a0a0a", 1), (0.4, iris, 1), (0.95, "#0f2a1a", 1), (1, "#0a0a0a", 1)) +
         rg(f"{nombre}_b", (0, "#ffffff", 1), (0.8, "#f2e2dc", 1), (1, "#d8a8a0", 1)) + lg(f"{nombre}_p", (0, "#e8b090"), (1, "#b8724e")))
    b = ['<rect width="900" height="520" fill="url(#' + nombre + '_p)"/>',
         '<path d="M60 270 C230 60 670 60 840 270 C670 470 230 470 60 270 Z" fill="url(#' + nombre + '_b)"/>',
         '<clipPath id="' + nombre + '_k"><path d="M60 270 C230 60 670 60 840 270 C670 470 230 470 60 270 Z"/></clipPath>',
         f'<g clip-path="url(#{nombre}_k)"><circle cx="450" cy="270" r="165" fill="url(#{nombre}_i)"/>',
         *[f'<path d="M450 270 L{450+160*math.cos(math.radians(a)):.0f} {270+160*math.sin(math.radians(a)):.0f}" stroke="#9adab0" stroke-width="2" opacity="0.35"/>' for a in range(0, 360, 12)],
         '<circle cx="450" cy="270" r="62" fill="#050505"/><circle cx="395" cy="215" r="30" fill="#fff" opacity="0.9"/>',
         '<path d="M60 270 C230 60 670 60 840 270" stroke="#000" stroke-width="40" fill="none" opacity="0.25" filter="url(#blur8)"/></g>',
         '<path d="M60 270 C230 60 670 60 840 270" stroke="#3a1a10" stroke-width="16" fill="none"/>',
         *[f'<path d="M{x} {y} l{dx} -50" stroke="#2a120a" stroke-width="7" stroke-linecap="round"/>' for x, y, dx in [(200, 150, -20), (290, 105, -10), (380, 85, 0), (470, 82, 6), (560, 90, 14), (650, 115, 22), (730, 160, 30)]],
         '<path d="M60 270 C230 470 670 470 840 270" stroke="#8a4a3a" stroke-width="8" fill="none" opacity="0.6"/>']
    if lloroso:
        b += ['<path d="M60 270 C230 470 670 470 840 270" stroke="#bfe9ff" stroke-width="14" fill="none" opacity="0.7"/>',
              '<path d="M640 420 C620 470 630 500 650 510 C672 500 680 470 640 420 Z" fill="#bfe9ff" opacity="0.9"/>',
              '<path d="M60 270 C230 60 670 60 840 270 C670 470 230 470 60 270 Z" fill="#ff5a5a" opacity="0.12"/>']
    b.append(grano(w, h))
    guardar(nombre, "".join(b), w, h, d)


def cara_sol():
    """Perfil de una cara (silueta cálida) con los ojos cerrados y luz dorada."""
    w, h = 700, 900
    d = lg("cs_p", (0, "#f2b88a"), (1, "#a8623e"), x2=1, y2=0)
    b = ['<path d="M520 60 C380 40 250 120 230 260 C220 330 160 380 170 420 C180 450 230 440 220 480 C210 520 250 520 240 560 '
         'C230 600 270 620 300 640 C330 700 320 780 340 900 L700 900 L700 60 Z" fill="url(#cs_p)"/>',
         '<path d="M240 320 C270 330 300 330 320 320" stroke="#5a2a18" stroke-width="8" fill="none" stroke-linecap="round"/>',
         '<path d="M520 60 C380 40 250 120 230 260 C220 330 160 380 170 420" stroke="#ffe6b0" stroke-width="12" fill="none" opacity="0.8" filter="url(#blur8)"/>',
         grano(w, h)]
    guardar("cara_sol", "".join(b), w, h, d)


def cara_perfil():
    """v2 del 02 (petición de cambios): perfil de una cara mirando a la izquierda, ojos cerrados al sol,
    con pelo, oreja, ceja, pestañas, labios, mejilla y luz dorada de borde."""
    w, h = 900, 1300
    d = (lg("cp_piel", (0, "#f6c49a"), (0.45, "#e2a074"), (1, "#9a5a38"), x2=1, y2=0.2) +
         lg("cp_pelo", (0, "#5a3420"), (0.5, "#3a2014"), (1, "#1a0c06"), x2=1, y2=0.4) +
         rg("cp_mej", (0, "#ff8a7a", 0.55), (1, "#ff8a7a", 0)) + rg("cp_luz", (0, "#fff0b0", 0.9), (1, "#fff0b0", 0)))
    perfil = ("M470 150 C360 150 290 230 275 330 C268 380 262 420 250 450 C230 495 190 540 205 575 C215 600 250 600 262 612 "
              "C250 640 252 660 268 672 C255 690 258 712 278 722 C270 760 285 800 330 812 C380 826 410 840 420 900 "
              "L430 1300 L900 1300 L900 760 C880 420 780 150 470 150 Z")
    b = [f'<path d="{perfil}" fill="url(#cp_piel)"/>',
         # pelo: masa redonda desde la frente por la coronilla hasta la nuca
         '<path d="M290 360 C285 200 420 95 580 95 C770 95 890 250 885 470 C880 640 830 760 790 860 L700 860 C735 760 745 640 720 560 C690 470 600 400 480 370 C400 352 330 360 290 360 Z" fill="url(#cp_pelo)"/>',
         *[f'<path d="M{x} {y} C{x+80} {y-50} {x+200} {y-20} {x+270} {y+60}" stroke="#8a5a34" stroke-width="5" fill="none" opacity="0.45"/>' for x, y in [(340, 260), (400, 200), (480, 160), (560, 150), (640, 180)]],
         '<path d="M320 300 C380 200 480 150 580 140" stroke="#fff0b0" stroke-width="8" fill="none" opacity="0.6" filter="url(#blur8)"/>',
         # oreja
         '<path d="M640 470 C700 440 750 480 745 550 C740 620 700 660 660 650 C640 645 635 620 650 600" fill="#d8946a"/>',
         '<path d="M662 500 C700 490 722 520 718 560 C714 600 690 615 672 605" stroke="#9a5a38" stroke-width="10" fill="none"/>',
         # ceja, ojo cerrado y pestañas
         '<path d="M300 405 C330 385 375 385 405 400" stroke="#4a2a18" stroke-width="12" fill="none" stroke-linecap="round"/>',
         '<path d="M310 455 C335 470 365 472 390 460" stroke="#3a1a10" stroke-width="7" fill="none" stroke-linecap="round"/>',
         *[f'<path d="M{x} {y} l{dx} 16" stroke="#2a120a" stroke-width="4" stroke-linecap="round"/>' for x, y, dx in [(318, 462, -8), (334, 468, -6), (350, 471, -4), (366, 470, -2), (380, 466, 0)]],
         # nariz, labios
         '<path d="M262 470 C246 520 212 560 214 578 C220 594 246 596 262 592" stroke="#b06a44" stroke-width="5" fill="none" opacity="0.6"/>',
         '<path d="M262 612 C280 618 300 622 315 616 C300 640 280 650 262 640" fill="#c9604e"/>',
         '<path d="M268 672 C285 664 305 666 318 672 C305 690 285 696 268 690" fill="#b8503e"/>',
         # mejilla rosada y luz de sol
         '<ellipse cx="380" cy="560" rx="90" ry="60" fill="url(#cp_mej)"/>',
         '<ellipse cx="300" cy="460" rx="260" ry="320" fill="url(#cp_luz)" opacity="0.55"/>',
         f'<path d="{perfil}" fill="none" stroke="#fff3b0" stroke-width="10" opacity="0.85" filter="url(#blur8)"/>',
         f'<path d="{perfil}" fill="none" stroke="#fff8d8" stroke-width="3" opacity="0.9"/>',
         # cuello y hombro
         '<path d="M430 900 C520 960 700 980 900 1000 L900 1300 L430 1300 Z" fill="#c07a50" opacity="0.5"/>',
         '<path d="M380 1120 C480 1060 700 1050 900 1080 L900 1300 L340 1300 Z" fill="#2a4a7a"/>',
         ]
    guardar("cara_perfil", "".join(b), w, h, d)


def interruptor(nombre, encendido):
    w, h = 400, 600
    d = lg("in_c", (0, "#f2f2f2"), (1, "#b8b8b8"))
    pal = ('<rect x="140" y="140" width="120" height="160" rx="18" fill="#ffffff" stroke="#888" stroke-width="4"/>' if encendido else
           '<rect x="140" y="300" width="120" height="160" rx="18" fill="#dcdcdc" stroke="#888" stroke-width="4"/>')
    b = ['<rect x="60" y="40" width="280" height="520" rx="30" fill="url(#in_c)" filter="url(#sombra)"/>',
         '<rect x="120" y="120" width="160" height="360" rx="20" fill="#8a8a8a"/>', pal]
    guardar(nombre, "".join(b), w, h, d)


def neandertal():
    """Silueta de cazador del Paleolítico (sin rasgos) con lanza, junto a una hoguera."""
    w, h = 700, 1000
    d = rg("ne_f", (0, "#fff3a0", 1), (0.4, "#ff8a1a", 1), (1, "#b82a00", 0))
    b = ['<ellipse cx="350" cy="980" rx="300" ry="20" fill="#000" opacity="0.5" filter="url(#blur8)"/>',
         '<ellipse cx="300" cy="200" rx="78" ry="88" fill="#140c08"/>',
         '<path d="M190 330 C200 280 400 280 420 330 L450 620 L400 640 L380 960 L320 960 L300 700 L280 960 L220 960 L210 640 L160 620 Z" fill="#140c08"/>',
         '<path d="M200 330 C230 360 380 360 410 330 L420 420 C380 440 230 440 190 420 Z" fill="#3a2414"/>',
         '<path d="M520 960 L560 40" stroke="#2a1a10" stroke-width="16"/>', '<path d="M548 40 L560 -20 L578 44 Z" fill="#6a6a6a"/>',
         '<path d="M420 360 L520 470" stroke="#140c08" stroke-width="42" stroke-linecap="round"/>',
         '<path d="M380 140 C400 170 402 240 380 270" stroke="#ff9a3a" stroke-width="7" fill="none" opacity="0.7"/>',
         '<path d="M420 330 L450 620" stroke="#ff9a3a" stroke-width="6" fill="none" opacity="0.5"/>']
    guardar("neandertal", "".join(b), w, h, d)


def hoguera():
    w, h = 400, 400
    d = rg("ho_f", (0, "#fff6c0", 1), (0.4, "#ffb02e", 1), (1, "#ff3d1a", 0))
    b = ['<ellipse cx="200" cy="200" rx="200" ry="200" fill="url(#ho_f)" opacity="0.5"/>',
         '<path d="M200 60 C240 150 300 200 260 300 C240 340 160 340 140 300 C100 220 180 160 200 60 Z" fill="#ff7a1a"/>',
         '<path d="M200 150 C220 210 250 240 230 300 C215 320 185 320 170 300 C155 260 190 220 200 150 Z" fill="#ffe08a"/>',
         '<path d="M90 340 L310 310 M110 310 L300 350" stroke="#3a2010" stroke-width="22" stroke-linecap="round"/>']
    guardar("hoguera", "".join(b), w, h, d)


def bg_cueva():
    r = random.Random(8)
    d = lg("cu_c", (0, "#0a0604"), (0.5, "#2a1a10"), (1, "#0a0604")) + rg("cu_l", (0, "#ff9a3a", 0.7), (1, "#ff9a3a", 0))
    b = ['<rect width="1080" height="1920" fill="url(#cu_c)"/>', '<ellipse cx="540" cy="1400" rx="800" ry="700" fill="url(#cu_l)" opacity="0.6"/>',
         '<path d="M0 0 L1080 0 L1080 500 C900 400 800 560 640 480 C480 400 380 560 200 460 C120 420 60 480 0 440 Z" fill="#050302"/>',
         '<path d="M0 1700 C300 1640 700 1700 1080 1650 L1080 1920 L0 1920 Z" fill="#140c06"/>']
    for _ in range(30):
        b.append(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(600,1600):.0f}" r="{r.uniform(20,80):.0f}" fill="#000" opacity="{r.uniform(0.05,0.18):.2f}"/>')
    b.append(grano())
    guardar("bg_cueva", "".join(b), defs=d)


def gente_estadio():
    """Multitud desde arriba: muchas cabezas de colores (para el «estadio lleno»)."""
    w, h = 1080, 1920
    r = random.Random(12)
    b = ['<rect width="1080" height="1920" fill="#1a1a24"/>']
    for k in range(900):
        x, y = r.uniform(-20, 1100), r.uniform(-20, 1940)
        c = r.choice(["#e05a3a", "#3a8ae0", "#f2c230", "#5ac46a", "#e8e8e8", "#c03a8a", "#3a3a4a", "#ff8a3a"])
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="26" fill="{c}"/><circle cx="{x-6:.0f}" cy="{y-6:.0f}" r="20" fill="#2a1a10"/>')
    b.append(grano())
    guardar("gente_estadio", "".join(b), w, h)


# ====================================================================== 03 · cebolla
def cebolla(nombre="cebolla", piel="#c87a2a", carne="#f2e6c8"):
    w, h = 700, 820
    d = (rg(f"{nombre}_p", (0, "#f2b860", 1), (0.6, piel, 1), (1, "#6a3410", 1), cx=0.4, cy=0.45) +
         lg(f"{nombre}_r", (0, "#e8d0a0"), (1, "#a87a40")))
    cuerpo = "M350 140 C520 160 650 330 640 520 C630 700 500 790 350 790 C200 790 70 700 60 520 C50 330 180 160 350 140 Z"
    b = ['<ellipse cx="350" cy="800" rx="260" ry="20" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         f'<path d="{cuerpo}" fill="url(#{nombre}_p)"/>',
         *[f'<path d="M350 150 C{350+dx} 300 {350+dx*1.2} 600 350 785" stroke="#7a3a10" stroke-width="5" fill="none" opacity="0.45"/>' for dx in (-260, -170, -80, 80, 170, 260)],
         '<path d="M330 145 C320 90 300 50 280 20 M350 140 C350 80 360 40 380 10 M370 145 C390 100 420 70 450 50" stroke="#a87a40" stroke-width="10" stroke-linecap="round" fill="none"/>',
         '<path d="M300 785 l-20 30 M350 790 l0 32 M400 785 l20 30" stroke="#d8c0a0" stroke-width="5"/>',
         '<path d="M180 300 C220 230 280 200 330 195" stroke="#ffe0a0" stroke-width="18" fill="none" opacity="0.5" stroke-linecap="round"/>',
         f'<clipPath id="{nombre}_k"><path d="{cuerpo}"/></clipPath><g clip-path="url(#{nombre}_k)">{grano(w, h)}</g>']
    guardar(nombre, "".join(b), w, h, d)


def cebolla_mitad():
    """Media cebolla vista por el corte: anillos concéntricos húmedos."""
    w, h = 800, 700
    d = rg("cm_c", (0, "#fffbe8", 1), (1, "#f2e2b8", 1))
    b = ['<ellipse cx="400" cy="680" rx="330" ry="18" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         '<ellipse cx="400" cy="380" rx="340" ry="300" fill="#c87a2a"/>',
         '<ellipse cx="400" cy="380" rx="322" ry="284" fill="url(#cm_c)"/>']
    for k in range(1, 9):
        b.append(f'<ellipse cx="400" cy="{380+k*4}" rx="{322-k*36}" ry="{284-k*32}" fill="none" stroke="#d8c08a" stroke-width="7" opacity="0.8"/>')
        b.append(f'<ellipse cx="{390}" cy="{372+k*4}" rx="{322-k*36}" ry="{284-k*32}" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.6"/>')
    b += ['<ellipse cx="400" cy="410" rx="30" ry="24" fill="#e8d6a0"/>', '<ellipse cx="300" cy="250" rx="90" ry="30" fill="#fff" opacity="0.35" transform="rotate(-25 300 250)"/>',
          grano(w, h)]
    guardar("cebolla_mitad", "".join(b), w, h, d)


def cuchillo(nombre="cuchillo", filo=True):
    w, h = 1200, 300
    d = lg(f"{nombre}_h", (0, "#f4f8fc"), (0.5, "#b8c4d0"), (1, "#6a7684")) + lg(f"{nombre}_m", (0, "#4a2a18"), (1, "#1a0c06"))
    borde = '<path d="M60 230 L700 230" stroke="#ffffff" stroke-width="5" opacity="0.95"/>' if filo else \
            '<path d="M60 230 L700 230" stroke="#6a6a6a" stroke-width="14" opacity="0.9"/>' + \
            "".join(f'<path d="M{x} 222 l8 14" stroke="#4a4a4a" stroke-width="4"/>' for x in range(90, 700, 40))
    b = ['<path d="M40 232 C120 120 300 70 700 70 L700 232 Z" fill="url(#' + nombre + '_h)"/>', borde,
         '<path d="M140 150 C260 110 450 100 690 100" stroke="#ffffff" stroke-width="6" opacity="0.5" fill="none"/>',
         '<rect x="700" y="60" width="40" height="180" rx="8" fill="#8a96a4"/>',
         '<rect x="740" y="80" width="420" height="140" rx="60" fill="url(#' + nombre + '_m)"/>',
         *[f'<circle cx="{x}" cy="150" r="14" fill="#c8ccd2"/>' for x in (830, 950, 1070)]]
    guardar(nombre, "".join(b), w, h, d)


def tabla():
    w, h = 1080, 500
    d = lg("ta_m", (0, "#d8a868"), (0.5, "#b8864a"), (1, "#8a5a2a"))
    r = random.Random(3)
    b = ['<ellipse cx="540" cy="470" rx="520" ry="26" fill="#000" opacity="0.45" filter="url(#blur8)"/>',
         '<rect x="30" y="80" width="1020" height="360" rx="40" fill="url(#ta_m)"/>',
         *[f'<path d="M60 {y:.0f} C300 {y+r.uniform(-14,14):.0f} 700 {y+r.uniform(-14,14):.0f} 1020 {y:.0f}" stroke="#7a4a1a" stroke-width="3" fill="none" opacity="0.35"/>' for y in range(110, 430, 26)],
         '<rect x="30" y="80" width="1020" height="20" rx="10" fill="#f2c890" opacity="0.6"/>', grano(w, h)]
    guardar("tabla", "".join(b), w, h, d)


def gotitas(nombre="gotitas", sem=6, n=60, color="#d8f2ff"):
    """Chorro de gotitas que salen hacia arriba en abanico (desde abajo al centro)."""
    w, h = 800, 1000
    r = random.Random(sem)
    b = []
    for _ in range(n):
        a = math.radians(r.gauss(-90, 18)); dist = r.uniform(80, 900)
        x, y = 400 + dist * math.cos(a), 980 + dist * math.sin(a)
        rr = r.uniform(4, 16) * (1.2 - dist / 1100)
        b.append(f'<path d="M{x:.0f} {y:.0f} l{-math.cos(a)*rr*3:.0f} {-math.sin(a)*rr*3:.0f}" stroke="{color}" stroke-width="{rr*0.8:.1f}" opacity="0.35" stroke-linecap="round"/>')
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.1f}" fill="{color}"/><circle cx="{x-rr*0.3:.0f}" cy="{y-rr*0.3:.0f}" r="{rr*0.35:.1f}" fill="#fff"/>')
    guardar(nombre, "".join(b), w, h)


def gas_nube():
    w, h = 900, 900
    r = random.Random(9)
    d = rg("gn_g", (0, "#d8ff9a", 0.55), (1, "#d8ff9a", 0))
    b = [f'<circle cx="{r.uniform(200,700):.0f}" cy="{r.uniform(200,700):.0f}" r="{r.uniform(120,260):.0f}" fill="url(#gn_g)"/>' for _ in range(10)]
    guardar("gas", '<g filter="url(#blur20)">' + "".join(b) + "</g>", w, h, d)


def celulas():
    """Primer plano de las células de la cebolla (rectángulos alargados), unas rotas."""
    w, h = 1080, 1920
    r = random.Random(2)
    b = ['<rect width="1080" height="1920" fill="#f2ecd2"/>']
    y = -20
    fila = 0
    while y < 1940:
        x = -r.uniform(0, 120)
        while x < 1080:
            cw, ch = r.uniform(180, 300), r.uniform(90, 120)
            rota = r.random() < 0.18
            b.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{cw-8:.0f}" height="{ch-8:.0f}" rx="16" fill="{"#e8f2c0" if not rota else "#f8e8a0"}" '
                     f'stroke="#b8a870" stroke-width="5"{" stroke-dasharray=\"30 18\"" if rota else ""}/>')
            b.append(f'<ellipse cx="{x+cw*0.5:.0f}" cy="{y+ch*0.45:.0f}" rx="16" ry="12" fill="#c8a85a" opacity="0.7"/>')
            x += cw
        y += r.uniform(95, 120); fila += 1
    b.append(grano())
    guardar("celulas", "".join(b))


def enzima():
    w = h = 400
    d = rg("en_g", (0, "#ff9ad8", 1), (1, "#b82a8a", 1), cx=0.35, cy=0.35)
    b = ['<path d="M200 30 C320 30 380 120 380 200 C380 300 300 370 200 370 C100 370 30 300 30 200 C30 140 60 100 90 80 L200 200 L170 40 Z" fill="url(#en_g)"/>',
         '<circle cx="150" cy="120" r="30" fill="#fff" opacity="0.35"/>', '<path d="M60 220 C80 300 160 350 230 345" stroke="#ffd0ee" stroke-width="8" fill="none" opacity="0.5"/>']
    guardar("enzima", "".join(b), w, h, d)


def molecula_azufre():
    w = h = 400
    d = rg("ma_s", (0, "#fff6a0", 1), (1, "#d8a800", 1), cx=0.35, cy=0.35) + rg("ma_c", (0, "#8a8a8a", 1), (1, "#2a2a2a", 1), cx=0.35, cy=0.35)
    b = ['<path d="M200 200 L90 110 M200 200 L320 120 M200 200 L200 340" stroke="#dcdcdc" stroke-width="18"/>',
         '<circle cx="90" cy="110" r="55" fill="url(#ma_c)"/><circle cx="320" cy="120" r="50" fill="url(#ma_c)"/><circle cx="200" cy="340" r="40" fill="#e8e8f8"/>',
         '<circle cx="200" cy="200" r="85" fill="url(#ma_s)"/><text x="200" y="228" font-family="DejaVu Sans" font-weight="bold" font-size="80" text-anchor="middle" fill="#5a4a00">S</text>']
    guardar("molecula_s", "".join(b), w, h, d)


def camara_rapida():
    w, h = 900, 600
    d = lg("cr_c", (0, "#4a5260"), (1, "#1a1e26")) + rg("cr_l", (0, "#5ad8ff", 1), (0.5, "#1a3a5a", 1), (1, "#05080c", 1))
    b = ['<ellipse cx="450" cy="580" rx="380" ry="18" fill="#000" opacity="0.45" filter="url(#blur8)"/>',
         '<rect x="80" y="140" width="520" height="340" rx="30" fill="url(#cr_c)"/>', '<rect x="80" y="140" width="520" height="340" rx="30" fill="none" stroke="#8a96a4" stroke-width="4"/>',
         '<rect x="600" y="200" width="200" height="220" rx="20" fill="#2a2e36"/>', '<circle cx="800" cy="310" r="130" fill="#1a1e26"/>',
         '<circle cx="800" cy="310" r="100" fill="url(#cr_l)"/>', '<circle cx="770" cy="280" r="26" fill="#fff" opacity="0.5"/>',
         '<rect x="130" y="190" width="200" height="110" rx="10" fill="#0a1a20"/><text x="230" y="262" font-family="DejaVu Sans" font-weight="bold" font-size="46" text-anchor="middle" fill="#ff3d3d">● REC</text>',
         '<rect x="380" y="100" width="120" height="50" rx="10" fill="#3a4250"/>', grano(w, h)]
    guardar("camara", "".join(b), w, h, d)


def guepardo():
    """Guepardo corriendo, con manchas (ladrillo `_animal`)."""
    cuerpo = ("M120 300 C160 230 300 210 430 220 C540 228 620 200 690 210 C740 190 790 200 800 230 C805 260 780 270 760 268 "
              "C720 300 680 330 600 340 C480 352 330 350 220 340 C160 334 110 330 120 300 Z")
    lejos = [_pata(260, 330, 470, 26, 1.3, 40), _pata(620, 330, 460, 24, 1.3, -50)]
    cerca = [_pata(330, 330, 480, 30, 1.3, -70), _pata(560, 330, 470, 28, 1.3, 70)]
    extra = [('<path d="M130 300 C60 280 30 220 10 180" stroke="#c8902a" stroke-width="22" fill="none" stroke-linecap="round"/>'
             '<path d="M10 180 l-6 -20" stroke="#1a1208" stroke-width="22" stroke-linecap="round"/>'
             '<path d="M760 215 C770 230 770 250 760 262" stroke="#1a1208" stroke-width="6" fill="none"/>'
             '<path d="M720 212 l10 -40 l18 36 Z" fill="#c8902a"/>')]
    _animal("guepardo", 840, 520, cuerpo, lejos, cerca, extra, "#d8a040", "#f2dcb0", manchas=60, sem=4, ojo=(745, 225, 9), sombra=(420, 490, 330, 16))


def gafas():
    """Gafas de protección cerradas (tipo laboratorio): montura de goma, cristales transparentes que dejan ver los ojos, cinta."""
    w, h = 900, 400
    izq = "M100 180 C100 130 150 115 230 115 L370 115 C410 115 420 160 410 200 C400 250 380 285 330 285 L230 285 C150 285 100 250 100 180 Z"
    der = "M800 180 C800 130 750 115 670 115 L530 115 C490 115 480 160 490 200 C500 250 520 285 570 285 L670 285 C750 285 800 250 800 180 Z"
    b = ['<path d="M60 175 L0 165 M840 175 L900 165" stroke="#1a2a3a" stroke-width="34" stroke-linecap="round"/>',
         f'<path d="{izq}" fill="#bfe9ff" fill-opacity="0.18" stroke="#1a2a3a" stroke-width="34" stroke-linejoin="round"/>',
         f'<path d="{der}" fill="#bfe9ff" fill-opacity="0.18" stroke="#1a2a3a" stroke-width="34" stroke-linejoin="round"/>',
         f'<path d="{izq}" fill="none" stroke="#4a6a8a" stroke-width="8"/>', f'<path d="{der}" fill="none" stroke="#4a6a8a" stroke-width="8"/>',
         '<path d="M410 170 C435 150 465 150 490 170" stroke="#1a2a3a" stroke-width="30" fill="none" stroke-linecap="round"/>',
         '<path d="M140 150 L260 140 M560 140 L680 150" stroke="#ffffff" stroke-width="10" opacity="0.55" stroke-linecap="round"/>']
    guardar("gafas", "".join(b), w, h)

def piedra_afilar():
    w, h = 900, 260
    d = lg("pa_g", (0, "#8a9aa8"), (1, "#3a4652"))
    b = ['<ellipse cx="450" cy="240" rx="420" ry="16" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         '<rect x="60" y="80" width="780" height="140" rx="16" fill="#5a3a20"/>', '<rect x="80" y="40" width="740" height="110" rx="12" fill="url(#pa_g)"/>',
         '<rect x="80" y="40" width="740" height="110" rx="12" fill="#888" filter="url(#grano)"/>']
    guardar("piedra", "".join(b), w, h, d)


# ---------------------------------------------------------------- v2 del 03 (petición de cambios): cebolla que se parte y enzima más clara
def cebolla_partida(lado):
    """Media cebolla vista de frente tras el corte vertical: piel por fuera y capas a la vista en la cara del corte."""
    w, h = 400, 820
    izq = lado == "izq"
    d = (rg(f"cpt_{lado}_p", (0, "#f2b860", 1), (0.6, "#c87a2a", 1), (1, "#6a3410", 1), cx=0.6 if izq else 0.4, cy=0.45) +
         lg(f"cpt_{lado}_c", (0, "#fffbe8"), (1, "#efe0b8"), x2=1, y2=0))
    if izq:
        cuerpo = "M380 140 C230 160 70 330 60 520 C50 700 200 790 380 790 Z"
        cara = "M380 140 L400 140 L400 790 L380 790 Z"
        capas = "".join(f'<path d="M398 {200+k*28} C{398-(300-k*36)} {260+k*24} {398-(300-k*36)} {720-k*24} 398 {760-k*28}" stroke="#d8c08a" stroke-width="6" fill="none"/>' for k in range(8))
    else:
        cuerpo = "M20 140 C170 160 330 330 340 520 C350 700 200 790 20 790 Z"
        cara = "M0 140 L20 140 L20 790 L0 790 Z"
        capas = "".join(f'<path d="M2 {200+k*28} C{2+(300-k*36)} {260+k*24} {2+(300-k*36)} {720-k*24} 2 {760-k*28}" stroke="#d8c08a" stroke-width="6" fill="none"/>' for k in range(8))
    corte = (f'<path d="M{400 if izq else 0} 140 C{400 - 330 if izq else 330} 300 {400 - 330 if izq else 330} 700 {400 if izq else 0} 790 Z" fill="url(#cpt_{lado}_c)"/>')
    b = ['<ellipse cx="200" cy="805" rx="170" ry="14" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         f'<path d="{cuerpo}" fill="url(#cpt_{lado}_p)"/>', corte, capas,
         f'<path d="{cara}" fill="#ffffff" opacity="0.6"/>',
         f'<ellipse cx="{360 if izq else 40}" cy="460" rx="18" ry="200" fill="#ffffff" opacity="0.35"/>']
    guardar(f"cebolla_{lado}", "".join(b), w, h, d)


def enzima_v2():
    """Enzima (aliinasa) como proteína: ovillo de hélices con un hueco activo que brilla."""
    w, h = 700, 700
    r = random.Random(33)
    d = rg("ez_c", (0, "#ffb8e8", 1), (0.6, "#d84aa8", 1), (1, "#7a1a5a", 1), cx=0.4, cy=0.35) + rg("ez_h", (0, "#7df9ff", 1), (1, "#7df9ff", 0))
    b = ['<ellipse cx="350" cy="360" rx="300" ry="280" fill="#ff3df2" opacity="0.18" filter="url(#blur40)"/>',
         '<path d="M350 70 C520 70 640 180 640 340 C640 520 520 640 350 640 C190 640 70 530 70 360 C70 260 110 190 170 140 L300 300 L250 90 C280 76 314 70 350 70 Z" fill="url(#ez_c)"/>']
    for k in range(9):  # hélices (cintas en espiral) por encima
        x, y = r.uniform(170, 560), r.uniform(330, 580)
        L = r.uniform(80, 150); a = r.uniform(-0.6, 0.6)
        pts = " ".join(f"{x + t*L*math.cos(a) + 14*math.sin(t*12):.0f},{y + t*L*math.sin(a) + 14*math.cos(t*12):.0f}" for t in [i / 24 for i in range(25)])
        b.append(f'<polyline points="{pts}" stroke="#ffe0f6" stroke-width="9" fill="none" stroke-linecap="round" opacity="0.8"/>')
        b.append(f'<polyline points="{pts}" stroke="#a0207a" stroke-width="3" fill="none" opacity="0.6"/>')
    b += ['<circle cx="255" cy="215" r="70" fill="url(#ez_h)" opacity="0.8"/>',  # hueco activo
          '<path d="M120 380 C140 500 230 590 340 600" stroke="#ffe0f6" stroke-width="10" fill="none" opacity="0.5"/>']
    guardar("enzima_v2", "".join(b), w, h, d)


def generar(dirsvg):
    ilus_lote.generar(dirsvg)          # piezas del lote de la mañana (cocina, laboratorio, casa, edificio, átomo…)
    ilus.OUT = dirsvg
    rayo(); rayo("rayo_b", 9, ramas=6); rayo("rayo_c", 17, 500, 1200, 3)
    nube_tormenta(); nube_tormenta("nube_b", 7, tono="#1e1e36"); bg_tormenta(); campo_noche()
    rayo_horizontal(); rayo_horizontal("rayo_horizontal_b", 37, color="#bfe9ff"); rayo_ramificado(); rayo_doble(); canal_plasma(); arbol_tormenta(); arbol_tormenta("arbol_quemado", True); bg_mar_tormenta(); yunque(); bg_cielo_despejado()
    termometro("termo_sol", 0.32, "#ffb02e"); termometro("termo_rayo", 1.0, "#ff2d55"); onda(); oreja(); refugio(); persona_cuenta()
    sol_corte(); foton(); ojo(); ojo("ojo_lloroso", "#5a3a1a", True); cara_sol(); cara_perfil(); interruptor("interruptor_on", True); interruptor("interruptor_off", False)
    neandertal(); hoguera(); bg_cueva(); gente_estadio()
    cebolla(); cebolla("cebolla_roja", "#8a2a5a"); cebolla_mitad(); cuchillo(); cuchillo("cuchillo_romo", False); tabla(); gotitas(); gotitas("gotitas_b", 8, 160)
    gas_nube(); celulas(); enzima(); enzima_v2(); cebolla_partida("izq"); cebolla_partida("der"); molecula_azufre(); camara_rapida(); guepardo(); gafas(); piedra_afilar()
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
