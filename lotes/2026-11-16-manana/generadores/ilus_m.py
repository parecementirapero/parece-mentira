"""Ilustraciones SVG del lote 2026-11-16-manana (estilo v4: degradados, luz, sombras, textura).
Reutiliza las piezas de lotes/2026-11-15-tarde/generadores/v4/ilus.py. Escribe en ./svg/.
Uso: python3 ilus_m.py
"""
import math, os, random, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.join(AQUI, "..", "..", "2026-11-15-tarde", "generadores", "v4")
sys.path.insert(0, V4)
import ilus  # noqa: E402
from ilus import lg, rg, grano  # noqa: E402

OUT = os.path.join(AQUI, "svg")
os.makedirs(OUT, exist_ok=True)
ilus.OUT = OUT
R = random.Random(16)


def guardar(nombre, cuerpo, w=1080, h=1920, defs=""):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
           f'<defs>{ilus.TEXTURA}{defs}</defs>{cuerpo}</svg>')
    open(os.path.join(OUT, nombre + ".svg"), "w").write(svg)


def estrellas(n=260, w=1080, h=1920):
    b = []
    for _ in range(n):
        x, y = R.uniform(0, w), R.uniform(0, h)
        r = R.choice([0.8, 1.0, 1.3, 1.7, 2.3, 3.0])
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{R.choice(["#ffffff","#dfe8ff","#fff1d6"])}" opacity="{R.uniform(0.35,1):.2f}"/>')
    return "".join(b)


# ============================================================ 01 · PLANETAS
def planeta(nombre, tam, base, luz, sombra, bandas=None, manchas=None, anillo=False, atm=None, mancha_roja=False, crateres=0):
    """Planeta redondo con volumen (luz arriba-izquierda), bandas opcionales y halo."""
    W = int(tam * (2.3 if anillo else 1.0))
    H = tam
    cx, cy, r = W / 2, H / 2, tam * 0.46
    pid = nombre
    d = rg(f"v{pid}", (0, luz, 1), (0.55, base, 1), (1, sombra, 1), cx=0.35, cy=0.32, r=0.75) + \
        rg(f"s{pid}", (0.5, "#000", 0), (1, "#000", 0.75), cx=0.28, cy=0.25, r=0.95) + \
        f'<clipPath id="c{pid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
    b = []
    if atm:
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r*1.08}" fill="{atm}" opacity="0.35" filter="url(#blur8)"/>')
    if anillo:  # mitad trasera del anillo
        b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r*2.35}" ry="{r*0.55}" fill="none" stroke="#d8c08c" stroke-width="{r*0.32}" opacity="0.55" transform="rotate(-14 {cx} {cy})"/>')
        b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r*1.95}" ry="{r*0.44}" fill="none" stroke="#efe0b8" stroke-width="{r*0.12}" opacity="0.6" transform="rotate(-14 {cx} {cy})"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#v{pid})"/>')
    b.append(f'<g clip-path="url(#c{pid})">')
    if bandas:
        y = cy - r
        rr = random.Random(len(nombre))
        while y < cy + r:
            h = rr.uniform(0.05, 0.13) * r * 2
            c = rr.choice(bandas)
            b.append(f'<path d="M{cx-r-20} {y:.1f} Q{cx} {y+rr.uniform(-8,8)*tam/400:.1f} {cx+r+20} {y:.1f} L{cx+r+20} {y+h:.1f} Q{cx} {y+h+rr.uniform(-8,8)*tam/400:.1f} {cx-r-20} {y+h:.1f} Z" fill="{c}" opacity="{rr.uniform(0.35,0.75):.2f}"/>')
            y += h
        b.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#888" filter="url(#grano)" opacity="0.6"/>')
    if mancha_roja:
        b.append(f'<ellipse cx="{cx+r*0.3}" cy="{cy+r*0.32}" rx="{r*0.22}" ry="{r*0.12}" fill="#c4583a"/>'
                 f'<ellipse cx="{cx+r*0.3}" cy="{cy+r*0.32}" rx="{r*0.14}" ry="{r*0.07}" fill="#e07a52"/>')
    if manchas:
        rr = random.Random(len(nombre) * 3)
        for _ in range(manchas[1]):
            x, y = cx + rr.uniform(-r, r), cy + rr.uniform(-r, r)
            b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr.uniform(0.08,0.25)*r:.0f}" ry="{rr.uniform(0.05,0.15)*r:.0f}" fill="{manchas[0]}" opacity="{rr.uniform(0.3,0.6):.2f}" transform="rotate({rr.uniform(-30,30):.0f} {x:.0f} {y:.0f})"/>')
    rr = random.Random(len(nombre) * 7)
    for _ in range(crateres):
        x, y, cr = cx + rr.uniform(-r, r) * 0.8, cy + rr.uniform(-r, r) * 0.8, rr.uniform(0.04, 0.11) * r
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{cr:.1f}" fill="{sombra}" opacity="0.45"/><circle cx="{x-cr*0.2:.0f}" cy="{y-cr*0.2:.0f}" r="{cr*0.75:.1f}" fill="{luz}" opacity="0.25"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#s{pid})"/></g>')
    b.append(f'<ellipse cx="{cx-r*0.35}" cy="{cy-r*0.42}" rx="{r*0.32}" ry="{r*0.16}" fill="#fff" opacity="0.16" transform="rotate(-30 {cx-r*0.35} {cy-r*0.42})"/>')
    if anillo:  # mitad delantera del anillo (por delante del planeta)
        b.append(f'<clipPath id="f{pid}"><rect x="0" y="{cy}" width="{W}" height="{H}"/></clipPath>')
        b.append(f'<g clip-path="url(#f{pid})" transform="rotate(-14 {cx} {cy})">'
                 f'<ellipse cx="{cx}" cy="{cy}" rx="{r*2.35}" ry="{r*0.55}" fill="none" stroke="#e6cf98" stroke-width="{r*0.32}" opacity="0.9"/>'
                 f'<ellipse cx="{cx}" cy="{cy}" rx="{r*1.95}" ry="{r*0.44}" fill="none" stroke="#fff3d0" stroke-width="{r*0.12}" opacity="0.9"/>'
                 f'<ellipse cx="{cx}" cy="{cy}" rx="{r*2.12}" ry="{r*0.5}" fill="none" stroke="#7a6440" stroke-width="{r*0.03}" opacity="0.8"/></g>')
    guardar(nombre, "".join(b), W, H, d)


def planetas():
    planeta("mercurio", 400, "#9a948c", "#d9d3c8", "#4a4640", crateres=26)
    planeta("venus", 400, "#e0b46a", "#fbe7b4", "#8a5a24", bandas=["#f2d28e", "#d6a457", "#e8c27a"], atm="#ffd98a")
    planeta("marte", 400, "#c2552c", "#f08a52", "#5a1d0c", manchas=("#7a2c14", 10), crateres=8)
    planeta("jupiter", 800, "#d2a77a", "#f6e2c4", "#5e3a1e", bandas=["#f3dfc0", "#c88e5a", "#e8c79c", "#a7704a", "#fbeedc"], mancha_roja=True)
    planeta("saturno", 700, "#e3c88e", "#fbf0cf", "#7a5c2c", bandas=["#f2deac", "#d9b878", "#efd9a2"], anillo=True)
    planeta("urano", 400, "#8fdbe2", "#d8f7f7", "#2f7a86", bandas=["#a6e6ea", "#9ad9df"], atm="#b6f3ff")
    planeta("neptuno", 400, "#3a63d8", "#8fb0ff", "#0f1f66", bandas=["#4a74e4", "#3456c4", "#5a86f0"], manchas=("#1b2f8a", 2), atm="#6f9bff")
    planeta("pluton", 300, "#c9a98a", "#f2e2cc", "#5a4636", manchas=("#f5ece0", 3), crateres=6)


def bg_noche():
    """Noche en el campo con una silueta mirando la Luna (sin la Luna: va aparte)."""
    d = lg("cn", (0, "#050817"), (0.55, "#15204a"), (1, "#3a3d6a")) + \
        rg("hal", (0, "#cfe0ff", 0.35), (1, "#cfe0ff", 0), cx=0.72, cy=0.22, r=0.5)
    b = ['<rect width="1080" height="1920" fill="url(#cn)"/>', estrellas(220, 1080, 1300),
         '<ellipse cx="780" cy="420" rx="700" ry="600" fill="url(#hal)"/>',
         '<path d="M-50 1420 C200 1330 420 1360 600 1300 C780 1240 950 1280 1130 1250 L1130 1920 L-50 1920 Z" fill="#141a33"/>',
         '<path d="M-50 1560 C250 1470 520 1520 760 1470 C900 1440 1000 1460 1130 1430 L1130 1920 L-50 1920 Z" fill="#0b0f22"/>',
         ]
    # silueta: persona de pie mirando arriba a la derecha
    x, y = 360, 1500
    b.append(f'<g transform="translate({x} {y})" fill="#05070f">'
             '<ellipse cx="0" cy="-330" rx="34" ry="40" transform="rotate(18 0 -330)"/>'
             '<path d="M-38 -285 C-60 -200 -58 -120 -48 -40 L-30 60 L-8 60 L0 -60 L10 60 L32 60 L44 -40 C54 -120 58 -210 36 -285 Z"/>'
             '<path d="M30 -270 C70 -230 90 -190 96 -150 L80 -146 C70 -180 50 -215 24 -240 Z"/>'
             '<path d="M-34 -270 C-60 -220 -66 -170 -62 -120 L-46 -120 C-46 -170 -40 -210 -22 -250 Z"/>'
             '</g>')
    # luz de borde en la silueta
    b.append(f'<path d="M{x+30} {y-290} C{x+50} {y-220} {x+48} {y-120} {x+42} {y-40}" stroke="#bcd0ff" stroke-width="3" opacity="0.5" fill="none"/>')
    for _ in range(26):  # hierbas
        gx = R.uniform(0, 1080)
        gy = 1600 + R.uniform(0, 300)
        b.append(f'<path d="M{gx:.0f} {gy:.0f} q{R.uniform(-10,10):.0f} -{R.uniform(30,70):.0f} {R.uniform(-20,20):.0f} -{R.uniform(60,110):.0f}" stroke="#1d2547" stroke-width="4" fill="none"/>')
    b.append(grano())
    guardar("bg_noche", "".join(b), defs=d)


# ============================================================ 02 · PULPO
def bg_mar():
    d = lg("mar", (0, "#1f7fa8"), (0.45, "#0d4a72"), (1, "#041a33")) + \
        rg("sol", (0, "#bff4ff", 0.55), (1, "#bff4ff", 0), cx=0.5, cy=0.0, r=0.6)
    b = ['<rect width="1080" height="1920" fill="url(#mar)"/>', '<ellipse cx="540" cy="0" rx="900" ry="700" fill="url(#sol)"/>']
    for i in range(7):  # rayos de luz
        x = 120 + i * 140 + R.uniform(-40, 40)
        b.append(f'<path d="M{x} -20 L{x+70} -20 L{x+260} 1500 L{x+120} 1500 Z" fill="#d6fbff" opacity="{R.uniform(0.04,0.09):.2f}" filter="url(#blur20)"/>')
    for _ in range(40):
        x, y = R.uniform(0, 1080), R.uniform(0, 1500)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{R.uniform(1.5,4):.1f}" fill="#e0fbff" opacity="{R.uniform(0.15,0.4):.2f}"/>')
    # fondo marino: arena, rocas y algas
    b.append('<path d="M-40 1560 C200 1500 420 1540 640 1500 C840 1470 980 1500 1120 1480 L1120 1960 L-40 1960 Z" fill="#c8a873"/>')
    b.append('<path d="M-40 1640 C260 1600 520 1640 760 1610 C900 1590 1000 1610 1120 1600 L1120 1960 L-40 1960 Z" fill="#a68752"/>')
    for x, w, h in ((120, 220, 150), (860, 280, 190), (520, 160, 90)):
        b.append(f'<path d="M{x-w/2} 1600 C{x-w/2} {1600-h} {x+w/2} {1600-h*1.1} {x+w/2} 1600 Z" fill="#4a4a56"/>'
                 f'<path d="M{x-w/2+20} {1600-h*0.5} C{x-w/4} {1600-h} {x+w/6} {1600-h} {x+w/3} {1600-h*0.8}" stroke="#7a7a8a" stroke-width="10" fill="none" opacity="0.6"/>')
    for x in (60, 300, 700, 1000):
        for k in range(3):
            b.append(f'<path d="M{x+k*18} 1620 C{x+k*18-40} 1480 {x+k*18+40} 1380 {x+k*18} 1240" stroke="#2f8a5a" stroke-width="14" fill="none" stroke-linecap="round" opacity="0.85"/>')
    b.append(grano())
    guardar("bg_mar", "".join(b), defs=d)


def _brazo(x0, y0, ang, largo, grosor, curva, color, ventosas=True):
    """Brazo de pulpo como trazo grueso que se afina, con ventosas en un lado."""
    pts = []
    for i in range(13):
        t = i / 12
        a = math.radians(ang + curva * t * t * 90)
        x = x0 + math.cos(math.radians(ang)) * largo * t + math.cos(a) * largo * 0.15 * t
        y = y0 + math.sin(math.radians(ang)) * largo * t + math.sin(a) * largo * 0.15 * t
        pts.append((x, y))
    b = []
    for i in range(len(pts) - 1):
        g = grosor * (1 - i / 13) + 4
        b.append(f'<line x1="{pts[i][0]:.0f}" y1="{pts[i][1]:.0f}" x2="{pts[i+1][0]:.0f}" y2="{pts[i+1][1]:.0f}" stroke="{color}" stroke-width="{g:.0f}" stroke-linecap="round"/>')
    if ventosas:
        for i in range(1, 11):
            x, y = pts[i]
            g = grosor * (1 - i / 13) * 0.22 + 2
            b.append(f'<circle cx="{x+4:.0f}" cy="{y+g*1.2:.0f}" r="{g:.1f}" fill="#f6c6b0" stroke="#b5583e" stroke-width="2"/>')
    return "".join(b), pts


def pulpo(nombre="pulpo", nadando=False):
    """Pulpo rojizo de frente. Coordenadas: cabeza (manto) centrada en (500, 420) de un lienzo 1000x1100."""
    d = rg("piel", (0, "#ff9a7a", 1), (0.6, "#d4573c", 1), (1, "#7a2418", 1), cx=0.38, cy=0.3, r=0.75) + \
        lg("brz", (0, "#d4573c"), (1, "#9a3524"))
    b = []
    col = "#c44c33"
    if nadando:  # brazos juntos hacia atrás (abajo), manto alargado
        for k, ang in enumerate((80, 85, 90, 95, 100, 88, 92, 84)):
            s, _ = _brazo(500 + (k - 3.5) * 16, 640, ang, 420, 46, 0.15 * (k - 3.5), col if k % 2 else "#b84530", ventosas=k in (0, 7))
            b.append(s)
        b.append('<ellipse cx="500" cy="420" rx="170" ry="260" fill="url(#piel)"/>')
    else:
        angs = (160, 135, 112, 96, 84, 68, 45, 20)
        for k, ang in enumerate(angs):
            s, _ = _brazo(500 + (k - 3.5) * 22, 620, ang, 360 + (k % 3) * 40, 58, (1 if k > 3 else -1) * 0.5, col if k % 2 else "#b84530")
            b.append(s)
        b.append('<ellipse cx="500" cy="590" rx="200" ry="90" fill="#b84530"/>')
        b.append('<path d="M330 560 C300 360 360 160 500 150 C640 160 700 360 670 560 Z" fill="url(#piel)"/>')
    # manchas y textura
    rr = random.Random(5)
    for _ in range(26):
        x, y = 500 + rr.uniform(-130, 130), 420 + rr.uniform(-200, 120)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr.uniform(4,12):.0f}" fill="#7a2418" opacity="0.35"/>')
    b.append('<ellipse cx="440" cy="260" rx="60" ry="30" fill="#fff" opacity="0.22" transform="rotate(-30 440 260)"/>')
    # ojos
    for ex in (420, 580):
        ey = 520 if not nadando else 560
        b.append(f'<ellipse cx="{ex}" cy="{ey}" rx="42" ry="34" fill="#f6e6c8" stroke="#7a2418" stroke-width="5"/>'
                 f'<rect x="{ex-24}" y="{ey-8}" width="48" height="16" rx="8" fill="#141414"/>'
                 f'<circle cx="{ex-12}" cy="{ey-12}" r="7" fill="#fff"/>')
    guardar(nombre, "".join(b), 1000, 1100, d)


def corazon(nombre, color="#3d7bff", tam=200):
    c = tam / 2
    d = rg(f"h{nombre}", (0, "#bcd4ff", 1), (0.5, color, 1), (1, "#0c1f6a", 1), cx=0.35, cy=0.3, r=0.8)
    s = tam / 200
    path = (f'M{c} {170*s} C{40*s} {120*s} {10*s} {80*s} {20*s} {50*s} C{30*s} {15*s} {80*s} {10*s} {c} {50*s} '
            f'C{120*s} {10*s} {170*s} {15*s} {180*s} {50*s} C{190*s} {80*s} {160*s} {120*s} {c} {170*s} Z')
    b = [f'<path d="{path}" fill="{color}" opacity="0.35" filter="url(#blur8)" transform="translate(0 4) scale(1.05)"/>',
         f'<path d="{path}" fill="url(#h{nombre})" stroke="#e6f0ff" stroke-width="{3*s}"/>',
         f'<ellipse cx="{60*s}" cy="{55*s}" rx="{22*s}" ry="{12*s}" fill="#fff" opacity="0.45" transform="rotate(-35 {60*s} {55*s})"/>']
    guardar(nombre, "".join(b), tam, tam, d)


def casa_bombas():
    """Casa en sección con tuberías y tres bombas: dos pequeñas (izq./der.) y una grande (centro)."""
    d = lg("par", (0, "#f3e6cf"), (1, "#d9c4a0")) + lg("tej", (0, "#b5513a"), (1, "#7a2c1e")) + \
        rg("bom", (0, "#ffffff", 1), (0.4, "#8fa6c2", 1), (1, "#3a4a66", 1), cx=0.35, cy=0.3)
    b = ['<rect width="1080" height="1920" fill="#203048"/>',
         '<path d="M140 760 L540 420 L940 760 Z" fill="url(#tej)"/>',
         '<rect x="180" y="760" width="720" height="760" fill="url(#par)"/>',
         '<rect x="180" y="760" width="720" height="760" fill="#000" opacity="0.05" filter="url(#grano)"/>',
         '<line x1="180" y1="1140" x2="900" y2="1140" stroke="#b39b74" stroke-width="10"/>',
         '<rect x="120" y="1510" width="840" height="40" fill="#5a4a36"/>']
    # tuberías
    tub = 'stroke="#8a95a8" stroke-width="26" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    b.append(f'<path d="M300 1400 L300 900 L780 900 L780 1400" {tub}/><path d="M300 1400 L780 1400" {tub}/>'
             f'<path d="M540 1400 L540 1000" {tub}/>')
    b.append('<path d="M300 1400 L300 900 L780 900 L780 1400 L300 1400" stroke="#c9d3e2" stroke-width="6" fill="none" opacity="0.6"/>')
    # bombas
    for x, y, r in ((300, 1000, 70), (780, 1000, 70), (540, 1260, 120)):
        b.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#bom)" stroke="#20283a" stroke-width="6"/>'
                 f'<circle cx="{x}" cy="{y}" r="{r*0.35}" fill="#20283a"/>'
                 f'<rect x="{x-r*0.12}" y="{y-r*0.85}" width="{r*0.24}" height="{r*0.5}" fill="#20283a"/>')
    # ventanas
    for x in (230, 790):
        b.append(f'<rect x="{x}" y="800" width="60" height="70" fill="#ffe7a6" stroke="#7a5a3a" stroke-width="6"/>')
    b.append(grano())
    guardar("casa_bombas", "".join(b), defs=d)


def gota(nombre, color, claro, osc):
    d = rg(f"g{nombre}", (0, claro, 1), (0.55, color, 1), (1, osc, 1), cx=0.35, cy=0.55, r=0.75)
    p = 'M150 20 C150 20 40 170 40 250 C40 320 90 370 150 370 C210 370 260 320 260 250 C260 170 150 20 150 20 Z'
    b = [f'<path d="{p}" fill="{color}" opacity="0.4" filter="url(#blur8)"/>', f'<path d="{p}" fill="url(#g{nombre})"/>',
         '<ellipse cx="105" cy="230" rx="22" ry="40" fill="#fff" opacity="0.45" transform="rotate(20 105 230)"/>']
    guardar(nombre, "".join(b), 300, 400, d)


# ============================================================ 03 · VIKINGOS
def drakkar(nombre="drakkar"):
    """Barco vikingo de perfil (proa a la derecha), vela a rayas. Lienzo 900x700, línea de flotación y=560."""
    d = lg("cas", (0, "#8a5a32"), (1, "#3e2412")) + lg("vel", (0, "#f2e6d0"), (1, "#c9b48c"))
    b = ['<path d="M60 520 C140 600 760 600 840 520 L870 420 C860 470 820 500 780 505 L120 505 C90 500 60 470 50 430 Z" fill="url(#cas)"/>']
    for k in range(4):  # tablas
        y = 520 + k * 14
        b.append(f'<path d="M{80+k*10} {y} C200 {y+50-k*8} 700 {y+50-k*8} {820-k*10} {y}" stroke="#2a180a" stroke-width="3" fill="none" opacity="0.6"/>')
    # proa y popa en espiral
    b.append('<path d="M840 520 C900 470 900 360 860 330 C830 310 800 340 820 365 C835 380 850 365 845 355" stroke="#3e2412" stroke-width="22" fill="none" stroke-linecap="round"/>')
    b.append('<path d="M60 520 C10 470 10 380 50 350 C75 335 95 360 80 380" stroke="#3e2412" stroke-width="22" fill="none" stroke-linecap="round"/>')
    # escudos
    for i in range(9):
        x = 170 + i * 66
        c = ["#c0392b", "#f1c40f", "#2e86c1"][i % 3]
        b.append(f'<circle cx="{x}" cy="510" r="26" fill="{c}" stroke="#2a180a" stroke-width="4"/><circle cx="{x}" cy="510" r="7" fill="#d0d0d0"/>')
    # mástil y vela a rayas
    b.append('<rect x="440" y="80" width="16" height="430" fill="#4a2c14"/>')
    b.append('<path d="M250 120 L650 120 C670 260 660 360 640 420 L260 420 C240 360 230 260 250 120 Z" fill="url(#vel)"/>')
    for i in range(5):
        if i % 2 == 0:
            x0 = 250 + i * 80
            b.append(f'<path d="M{x0} 120 L{x0+80} 120 C{x0+92} 260 {x0+88} 360 {x0+78} 420 L{x0+4} 420 C{x0-6} 360 {x0-10} 260 {x0} 120 Z" fill="#b8352a" opacity="0.85"/>')
    b.append('<rect x="235" y="110" width="430" height="14" rx="7" fill="#4a2c14"/>')
    b.append('<path d="M260 420 C240 360 230 260 250 120" stroke="#000" stroke-width="2" opacity="0.2" fill="none"/>')
    # remos
    for i in range(8):
        x = 190 + i * 70
        b.append(f'<line x1="{x}" y1="530" x2="{x-50}" y2="640" stroke="#5a3a1e" stroke-width="7"/>')
    guardar(nombre, "".join(b), 900, 700, d)


def carabela(nombre="carabela"):
    """Carabela de 1492 de perfil (proa a la izquierda). Lienzo 900x800, flotación y=640."""
    d = lg("cc", (0, "#9a6a3a"), (1, "#4a2c14")) + lg("vb", (0, "#fbf6ea"), (1, "#d9cdb0"))
    b = ['<path d="M80 560 L820 560 L800 520 L860 470 L860 560 C820 660 200 670 120 620 Z" fill="url(#cc)"/>',
         '<path d="M640 470 L860 470 L860 560 L640 560 Z" fill="#6a4020"/>',
         '<line x1="80" y1="560" x2="10" y2="500" stroke="#4a2c14" stroke-width="10"/>']
    for x, top, w in ((260, 120, 200), (470, 60, 260), (700, 200, 150)):
        b.append(f'<rect x="{x-7}" y="{top}" width="14" height="{560-top}" fill="#4a2c14"/>')
        b.append(f'<path d="M{x-w/2} {top+30} C{x-w/2-20} {top+150} {x-w/2-10} {top+240} {x-w/2} {top+260} L{x+w/2} {top+260} C{x+w/2+10} {top+240} {x+w/2+20} {top+150} {x+w/2} {top+30} Z" fill="url(#vb)"/>')
        b.append(f'<path d="M{x-10} {top+90} h20 v60 h40 v20 h-40 v60 h-20 v-60 h-40 v-20 h40 Z" fill="#b8352a" opacity="0.9"/>')
    for i in range(6):
        b.append(f'<rect x="{200+i*80}" y="580" width="22" height="16" fill="#2a180a"/>')
    guardar(nombre, "".join(b), 900, 800, d)


def bg_mar_norte(nombre="bg_mar_norte", amanecer=False):
    cielo = ("#1d2b44", "#6a8bb0", "#f2c48a") if amanecer else ("#22324c", "#5a7898", "#a9bccd")
    d = lg("cmn", (0, cielo[0]), (0.6, cielo[1]), (1, cielo[2])) + lg("agn", (0, "#3a5a78"), (1, "#0c1a2a"))
    b = ['<rect width="1080" height="1920" fill="url(#cmn)"/>']
    for _ in range(8):
        x, y = R.uniform(-100, 1100), R.uniform(150, 900)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{R.uniform(180,360):.0f}" ry="{R.uniform(40,80):.0f}" fill="#e6eef6" opacity="{R.uniform(0.18,0.4):.2f}" filter="url(#blur20)"/>')
    # costa lejana con colinas (Terranova)
    b.append('<path d="M-40 1080 C150 1020 320 1050 480 1000 C620 960 760 1010 900 980 C980 965 1060 990 1120 980 L1120 1110 L-40 1110 Z" fill="#3c5048"/>')
    b.append('<path d="M-40 1100 C200 1070 420 1090 640 1060 C820 1040 960 1070 1120 1050 L1120 1120 L-40 1120 Z" fill="#2c3e38"/>')
    b.append('<rect x="-40" y="1100" width="1160" height="860" fill="url(#agn)"/>')
    for i in range(40):
        y = 1120 + i * 20 + R.uniform(-5, 5)
        x = R.uniform(-100, 1000)
        b.append(f'<path d="M{x:.0f} {y:.0f} q40 -10 80 0 t80 0" stroke="#bcd6ea" stroke-width="{2+i*0.12:.1f}" fill="none" opacity="{0.15+i*0.01:.2f}"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def bg_terranova():
    """Costa de hierba de L'Anse aux Meadows con casas de turba (techos de hierba) y el mar al fondo."""
    d = lg("ct", (0, "#5f86b0"), (0.7, "#c9d9e2"), (1, "#e9e6d6")) + lg("hb", (0, "#7a9a4a"), (1, "#3d5a26")) + \
        lg("tb", (0, "#8aa856"), (1, "#5a6e30"))
    b = ['<rect width="1080" height="1920" fill="url(#ct)"/>']
    for _ in range(6):
        x, y = R.uniform(-100, 1100), R.uniform(200, 800)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{R.uniform(200,380):.0f}" ry="{R.uniform(40,70):.0f}" fill="#ffffff" opacity="0.45" filter="url(#blur20)"/>')
    b.append('<rect x="-40" y="980" width="1160" height="140" fill="#4a6e8e"/>')
    for i in range(12):
        b.append(f'<path d="M{R.uniform(-50,1000):.0f} {990+i*10} q50 -6 100 0" stroke="#d6e6f0" stroke-width="2" opacity="0.4" fill="none"/>')
    b.append('<path d="M-40 1110 C200 1060 480 1100 700 1070 C880 1050 1000 1080 1120 1070 L1120 1960 L-40 1960 Z" fill="url(#hb)"/>')
    # casas de turba alargadas
    for x, y, w, h in ((300, 1260, 420, 150), (790, 1180, 300, 110)):
        b.append(f'<ellipse cx="{x+30}" cy="{y+10}" rx="{w/2+20}" ry="24" fill="#000" opacity="0.3" filter="url(#blur8)"/>')
        b.append(f'<path d="M{x-w/2} {y} L{x-w/2} {y-h*0.45} C{x-w/2+30} {y-h} {x+w/2-30} {y-h} {x+w/2} {y-h*0.45} L{x+w/2} {y} Z" fill="url(#tb)"/>')
        b.append(f'<path d="M{x-w/2} {y-h*0.45} L{x+w/2} {y-h*0.45}" stroke="#4a5a28" stroke-width="5" opacity="0.6"/>')
        for k in range(6):
            yy = y - k * h * 0.08
            b.append(f'<line x1="{x-w/2}" y1="{yy:.0f}" x2="{x+w/2}" y2="{yy:.0f}" stroke="#5a4a2a" stroke-width="3" opacity="0.4"/>')
        b.append(f'<rect x="{x-24}" y="{y-80}" width="48" height="80" fill="#2a1e12"/>')
        b.append(f'<path d="M{x+w/2-60} {y-h*0.95} q8 -40 -4 -80 q-8 -30 6 -60" stroke="#d8d8d8" stroke-width="16" fill="none" opacity="0.35" filter="url(#blur8)"/>')
    for _ in range(140):
        gx, gy = R.uniform(0, 1080), R.uniform(1150, 1920)
        b.append(f'<path d="M{gx:.0f} {gy:.0f} q{R.uniform(-8,8):.0f} -{R.uniform(20,40):.0f} {R.uniform(-14,14):.0f} -{R.uniform(30,60):.0f}" stroke="{R.choice(["#9ab85a","#5a7a2e","#b8c86a"])}" stroke-width="3" fill="none"/>')
    b.append(grano())
    guardar("bg_terranova", "".join(b), defs=d)


def _costa(pts, sem, amp=14, pasos=6):
    """Polígono cerrado con borde irregular a partir de puntos de control."""
    rr = random.Random(sem)
    out = []
    for i in range(len(pts)):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
        for k in range(pasos):
            t = k / pasos
            out.append((x0 + (x1 - x0) * t + rr.uniform(-amp, amp), y0 + (y1 - y0) * t + rr.uniform(-amp, amp)))
    return " ".join(f"{x:.0f},{y:.0f}" for x, y in out)


def mapa():
    """Atlántico norte (papel antiguo): Escandinavia, Islandia, Groenlandia, Terranova, Norteamérica, Europa."""
    d = lg("pap", (0, "#efe0bd"), (1, "#d6bf8f")) + lg("mr", (0, "#8fb3b0"), (1, "#5f8c8f"))
    b = ['<rect width="1080" height="1920" fill="url(#mr)"/>', '<rect width="1080" height="1920" fill="#000" filter="url(#papel)" opacity="0.35"/>']
    tierra = 'fill="#ead9ad" stroke="#5a4428" stroke-width="5"'
    zonas = {
        "escandinavia": [(760, 360), (860, 330), (930, 420), (960, 560), (920, 700), (870, 820), (820, 760), (790, 640), (760, 500)],
        "islandia": [(540, 520), (610, 495), (670, 520), (660, 580), (590, 600), (545, 575)],
        "groenlandia": [(240, 280), (380, 240), (490, 300), (480, 450), (430, 620), (360, 760), (300, 700), (240, 560), (220, 400)],
        "terranova": [(90, 900), (170, 870), (220, 930), (210, 1020), (150, 1060), (95, 1020)],
        "america": [(-60, 700), (40, 760), (70, 860), (40, 980), (60, 1120), (20, 1300), (-60, 1320)],
        "europa": [(760, 890), (880, 860), (1000, 880), (1140, 900), (1140, 1400), (1000, 1410), (920, 1360), (860, 1300), (800, 1190), (770, 1040)],
    }
    for i, (nombre, pts) in enumerate(zonas.items()):
        b.append(f'<polygon points="{_costa(pts, i)}" {tierra}/>')
        b.append(f'<polygon points="{_costa(pts, i)}" fill="none" stroke="#5a4428" stroke-width="2" opacity="0.35" transform="translate(0 10)"/>')
    for _ in range(40):  # olas del papel
        x, y = R.uniform(240, 740), R.uniform(820, 1650)
        b.append(f'<path d="M{x:.0f} {y:.0f} q12 -8 24 0 t24 0" stroke="#3e6466" stroke-width="3" fill="none" opacity="0.6"/>')
    b.append('<g transform="translate(520 1560)"><circle r="80" fill="none" stroke="#3e3020" stroke-width="4"/>'
             '<path d="M0 -100 L16 0 L0 100 L-16 0 Z" fill="#3e3020"/><path d="M-100 0 L0 16 L100 0 L0 -16 Z" fill="#6a5434"/></g>')
    b.append(grano())
    guardar("mapa_atlantico", "".join(b), defs=d)


def tronco(nombre="tronco", marcas=True):
    """Tronco de abeto talado, de lado, con corteza y corte limpio de hacha de metal. Lienzo 1000x420."""
    d = lg("crt", (0, "#7a5a3a"), (0.5, "#5a3e24"), (1, "#3a2614")) + rg("cor", (0, "#f0d6a0", 1), (0.7, "#d2a868", 1), (1, "#8a6236", 1))
    b = ['<ellipse cx="520" cy="380" rx="460" ry="26" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<rect x="120" y="90" width="760" height="260" rx="40" fill="url(#crt)"/>']
    for i in range(18):
        y = 100 + i * 14
        b.append(f'<path d="M140 {y} C300 {y+R.uniform(-6,6):.0f} 600 {y+R.uniform(-6,6):.0f} 870 {y}" stroke="#2a180a" stroke-width="3" opacity="0.35" fill="none"/>')
    # cara cortada con anillos
    b.append('<ellipse cx="880" cy="220" rx="80" ry="130" fill="url(#cor)" stroke="#3a2614" stroke-width="8"/>')
    for k in range(1, 9):
        b.append(f'<ellipse cx="880" cy="220" rx="{80-k*9}" ry="{130-k*14.5}" fill="none" stroke="#9a7040" stroke-width="2" opacity="0.7"/>')
    if marcas:  # cortes de hacha de metal
        for x in (300, 360, 600):
            b.append(f'<path d="M{x} 90 L{x+40} 170 L{x+70} 90 Z" fill="#e8c890" stroke="#6a4a2a" stroke-width="3"/>')
    guardar(nombre, "".join(b), 1000, 420, d)


def hacha(nombre="hacha"):
    d = lg("met", (0, "#f4f7fb"), (0.5, "#9aa6b6"), (1, "#4a5464"))
    b = ['<rect x="230" y="40" width="34" height="520" rx="14" fill="#6a4426"/>',
         '<path d="M240 70 C150 40 60 60 30 120 C20 190 70 250 150 240 C190 230 220 200 250 180 Z" fill="url(#met)" stroke="#2a3040" stroke-width="5"/>',
         '<path d="M40 130 C50 90 110 70 160 80" stroke="#fff" stroke-width="6" opacity="0.6" fill="none"/>']
    guardar(nombre, "".join(b), 300, 600, d)


def anillos(nombre="anillos", n=34, marca=8):
    """Corte del tronco visto de frente con anillos; el anillo `marca` (contado desde el centro) va en ámbar."""
    d = rg("mad", (0, "#f6dfb0", 1), (0.8, "#d8ae6c", 1), (1, "#a77a42", 1))
    c, rmax = 500, 440
    b = [f'<circle cx="{c}" cy="{c}" r="{rmax+40}" fill="#4a2e18"/>', f'<circle cx="{c}" cy="{c}" r="{rmax+40}" fill="#000" filter="url(#grano)" opacity="0.5"/>',
         f'<circle cx="{c}" cy="{c}" r="{rmax}" fill="url(#mad)"/>']
    rr = random.Random(11)
    radios = []
    acc = 30
    for i in range(n):
        acc += (rmax - 30) / n * rr.uniform(0.7, 1.3)
        radios.append(min(acc, rmax - 4))
    for i, r in enumerate(radios):
        pts = " ".join(f"{c+math.cos(a)*(r+rr.uniform(-3,3)):.0f},{c+math.sin(a)*(r+rr.uniform(-3,3)):.0f}" for a in [k * math.pi / 24 for k in range(48)])
        col, w, op = ("#ff9a1f", 9, 1.0) if i == marca else ("#8a5a2a", 3, 0.7)
        b.append(f'<polygon points="{pts}" fill="none" stroke="{col}" stroke-width="{w}" opacity="{op}"/>')
    b.append(f'<circle cx="{c}" cy="{c}" r="10" fill="#6a4020"/>')
    for k in range(5):  # grietas radiales
        a = rr.uniform(0, 6.28)
        b.append(f'<line x1="{c+math.cos(a)*40:.0f}" y1="{c+math.sin(a)*40:.0f}" x2="{c+math.cos(a)*rr.uniform(150,300):.0f}" y2="{c+math.sin(a)*rr.uniform(150,300):.0f}" stroke="#5a3a1a" stroke-width="3" opacity="0.5"/>')
    guardar(nombre, "".join(b), 1000, 1000, d)
    return radios


def sol_tormenta():
    d = rg("sl", (0, "#fffbe0", 1), (0.5, "#ffc93a", 1), (0.85, "#ff7a1a", 1), (1, "#c43a0a", 1))
    c = 450
    b = [f'<circle cx="{c}" cy="{c}" r="440" fill="#ff9a2a" opacity="0.35" filter="url(#blur40)"/>', f'<circle cx="{c}" cy="{c}" r="300" fill="url(#sl)"/>']
    rr = random.Random(3)
    for _ in range(40):
        x, y = c + rr.uniform(-220, 220), c + rr.uniform(-220, 220)
        if (x - c) ** 2 + (y - c) ** 2 < 260 ** 2:
            b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr.uniform(6,20):.0f}" fill="#ffe680" opacity="0.5"/>')
    # eyección (llamarada) hacia la derecha
    b.append(f'<path d="M{c+250} {c-120} C{c+420} {c-260} {c+470} {c+80} {c+270} {c+90}" stroke="#ff8a1a" stroke-width="46" fill="none" stroke-linecap="round" opacity="0.85" filter="url(#blur8)"/>')
    b.append(f'<path d="M{c+250} {c-120} C{c+420} {c-260} {c+470} {c+80} {c+270} {c+90}" stroke="#ffe27a" stroke-width="16" fill="none" stroke-linecap="round"/>')
    guardar("sol_tormenta", "".join(b), 900, 900, d)


def arbol(nombre="arbol"):
    """Abeto con volumen. Lienzo 500x900."""
    d = lg("ab", (0, "#3f7a4a"), (1, "#1d3e24"))
    b = ['<ellipse cx="250" cy="880" rx="160" ry="20" fill="#000" opacity="0.3" filter="url(#blur8)"/>', '<rect x="232" y="700" width="36" height="180" fill="#5a3a1e"/>']
    for k in range(6):
        y = 120 + k * 110
        w = 70 + k * 30
        b.append(f'<path d="M250 {y-60} L{250+w} {y+120} L{250-w} {y+120} Z" fill="url(#ab)"/>')
        b.append(f'<path d="M250 {y-60} L{250-w} {y+120} L{250-w*0.5} {y+120} Z" fill="#7ab86a" opacity="0.25"/>')
    guardar(nombre, "".join(b), 500, 900, d)


if __name__ == "__main__":
    planetas(); bg_noche()
    bg_mar(); pulpo(); pulpo("pulpo_nada", nadando=True)
    corazon("corazon_azul"); corazon("corazon_rojo", color="#e0392b"); casa_bombas()
    gota("gota_roja", "#d22b2b", "#ff9a8a", "#6a0a0a"); gota("gota_azul", "#2b6ad2", "#a8c8ff", "#0a1e6a")
    drakkar(); carabela(); bg_mar_norte(); bg_terranova(); mapa(); tronco(); hacha(); anillos(); sol_tormenta(); arbol()
    for n in ("tierra_hd", "luna_hd", "bg_espacio", "lupa"):
        shutil.copy(os.path.join(V4, "svg", n + ".svg"), os.path.join(OUT, n + ".svg"))
    print(sorted(os.listdir(OUT)))
