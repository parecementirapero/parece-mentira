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
    w, h = 900, 400
    d = lg("ga_v", (0, "#bfe9ffaa"), (1, "#7ac8ff55"))
    b = ['<path d="M60 180 C60 100 140 80 230 80 L380 80 C420 80 440 110 450 140 C460 110 480 80 520 80 L670 80 C760 80 840 100 840 180 '
         'C840 280 760 320 670 320 L560 320 C500 320 470 270 450 240 C430 270 400 320 340 320 L230 320 C140 320 60 280 60 180 Z" fill="#1a2a3a"/>',
         '<path d="M100 180 C100 130 150 115 230 115 L370 115 C410 115 420 160 410 200 C400 250 380 285 330 285 L230 285 C150 285 100 250 100 180 Z" fill="url(#ga_v)"/>',
         '<path d="M800 180 C800 130 750 115 670 115 L530 115 C490 115 480 160 490 200 C500 250 520 285 570 285 L670 285 C750 285 800 250 800 180 Z" fill="url(#ga_v)"/>',
         '<path d="M140 150 L260 140 M560 140 L680 150" stroke="#ffffff" stroke-width="10" opacity="0.6" stroke-linecap="round"/>',
         '<path d="M60 180 L0 170 M840 180 L900 170" stroke="#1a2a3a" stroke-width="30"/>']
    guardar("gafas", "".join(b), w, h, d)


def piedra_afilar():
    w, h = 900, 260
    d = lg("pa_g", (0, "#8a9aa8"), (1, "#3a4652"))
    b = ['<ellipse cx="450" cy="240" rx="420" ry="16" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         '<rect x="60" y="80" width="780" height="140" rx="16" fill="#5a3a20"/>', '<rect x="80" y="40" width="740" height="110" rx="12" fill="url(#pa_g)"/>',
         '<rect x="80" y="40" width="740" height="110" rx="12" fill="#888" filter="url(#grano)"/>']
    guardar("piedra", "".join(b), w, h, d)


def generar(dirsvg):
    ilus_lote.generar(dirsvg)          # piezas del lote de la mañana (cocina, laboratorio, casa, edificio, átomo…)
    ilus.OUT = dirsvg
    rayo(); rayo("rayo_b", 9, ramas=6); rayo("rayo_c", 17, 500, 1200, 3)
    nube_tormenta(); nube_tormenta("nube_b", 7, tono="#1e1e36"); bg_tormenta(); campo_noche()
    termometro("termo_sol", 0.32, "#ffb02e"); termometro("termo_rayo", 1.0, "#ff2d55"); onda(); oreja(); refugio(); persona_cuenta()
    sol_corte(); foton(); ojo(); ojo("ojo_lloroso", "#5a3a1a", True); cara_sol(); interruptor("interruptor_on", True); interruptor("interruptor_off", False)
    neandertal(); hoguera(); bg_cueva(); gente_estadio()
    cebolla(); cebolla("cebolla_roja", "#8a2a5a"); cebolla_mitad(); cuchillo(); cuchillo("cuchillo_romo", False); tabla(); gotitas(); gotitas("gotitas_b", 8, 160)
    gas_nube(); celulas(); enzima(); molecula_azufre(); camara_rapida(); guepardo(); gafas(); piedra_afilar()
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
