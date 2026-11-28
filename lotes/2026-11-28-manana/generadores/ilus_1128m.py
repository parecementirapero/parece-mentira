"""Ilustraciones del lote 2026-11-28-manana (Agente 08:00 (Nico)), con el ESTILO DEL VÍDEO LARGO de la cueva
(DECISIONS 2026-11-26). Reutiliza todo el arte anterior (`ilus_1127t.generar`, que encadena los lotes 25/26/27-tarde
y el vídeo largo) y añade solo las piezas nuevas con los mismos ayudantes (Lz, mat, sombra_suelo, Lienzo):
01 en enero estamos más cerca del Sol · 02 la nevada de Ciudad de México de 1967 · 03 el vidrio no se escurre.
Uso: python3 ilus_1128m.py DIR_SVG"""
import importlib.util, math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
LARGO = os.path.join(RAIZ, "lotes", "largo-cueva-500-dias", "generadores")
sys.path.insert(0, RAIZ)
sys.path.insert(0, LARGO)
from motor.biblioteca import ilus  # noqa: E402
import ilus_escenarios as IE  # noqa: E402
from ilus_personajes import Lz, busto, _pj, mat, F, sombra_suelo, PIEL2, PIEL3, PIEL4  # noqa: E402

_spec = importlib.util.spec_from_file_location("ilus_1127t", os.path.join(RAIZ, "lotes", "2026-11-27-tarde", "generadores", "ilus_1127t.py"))
T27 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(T27)
T25 = T27.T25

SALA = dict(luz=(-0.6, -0.8), rim="#fff1d8")
FRIO = dict(luz=(-0.6, -0.8), rim="#bfe4ff")
FUEGO = dict(luz=(0.7, -0.6), rim="#ffb060")

ABUELA = _pj(nombre="abuela", fem=True, peinado="melena", pelo="#d8d4ce", top=mat("#7a3a4a", "#a8606e", "#3e1c24"), prenda="chaqueta",
             pant=mat("#3a3440"), calzado="zapato", bota=mat("#2a2020"), edad=74, piel=PIEL2)
NINO67 = _pj(nombre="nino67", peinado="corto", pelo="#1e140c", top=mat("#c0392b", "#e86a5a", "#6a1a12"), prenda="polar",
             pant=mat("#3a4a6a"), calzado="zapato", bota=mat("#3a2a1e"), edad=10, piel=PIEL3)
NINA67 = _pj(nombre="nina67", fem=True, peinado="coleta", pelo="#2a1a10", top=mat("#2a7f9e", "#5fb3cf", "#174a5e"), prenda="chaqueta",
             pant=mat("#4a3a5a"), calzado="zapato", bota=mat("#2a2a2e"), edad=9, piel=PIEL4)
CRISTALERO = _pj(nombre="cristalero", peinado="corto", pelo="#3a2618", top=mat("#8a6a4a", "#b8946e", "#4a3420"), prenda="camiseta", manga="larga",
                 pant=mat("#4a3a2a"), calzado="zapato", bota=mat("#3a2a1e"), edad=45, piel=PIEL3)

NOMBRES = []


def _a(n):
    NOMBRES.append(n)
    return n


def _rnd(sem):
    return random.Random(sem)


# =========================================================================== comunes
def termometro(n, nivel=0.2, frio=True):
    """Termómetro grande de cristal: `nivel` 0..1 de la columna; azul helado o rojo."""
    w, h = 220, 900
    z = Lz(n, w, h, **(FRIO if frio else FUEGO))
    cx = w / 2
    c0, c1 = ("#2a8aff", "#9ad8ff") if frio else ("#e0301a", "#ff8a5a")
    z(f'<rect x="{cx - 52}" y="40" width="104" height="700" rx="52" fill="{z.lin((cx - 52, 0), (cx + 52, 0), [(0, "#c8d8e8", 0.5), (0.3, "#ffffff", 0.85), (1, "#8aa0b8", 0.55)])}" stroke="#ffffff" stroke-opacity="0.7" stroke-width="4"/>',
      f'<circle cx="{cx}" cy="790" r="95" fill="{z.lin((cx - 95, 0), (cx + 95, 0), [(0, "#c8d8e8", 0.6), (0.35, "#ffffff", 0.9), (1, "#8aa0b8", 0.6)])}" stroke="#ffffff" stroke-opacity="0.7" stroke-width="4"/>')
    top = 700 - 640 * nivel + 40
    z(f'<rect x="{cx - 22}" y="{F(top)}" width="44" height="{F(760 - top)}" rx="22" fill="{z.lin((cx - 22, 0), (cx + 22, 0), [(0, c0), (0.4, c1), (1, c0)])}"/>',
      f'<circle cx="{cx}" cy="790" r="70" fill="{z.rad((cx - 20, 770), 80, [(0, c1), (0.6, c0), (1, c0)])}"/>',
      f'<ellipse cx="{cx - 25}" cy="765" rx="18" ry="26" fill="#ffffff" opacity="0.55"/>')
    for k in range(13):
        y = 90 + k * 50
        z(f'<rect x="{cx + 52 - (28 if k % 2 == 0 else 16)}" y="{y}" width="{28 if k % 2 == 0 else 16}" height="5" fill="#3a4658" opacity="0.8"/>')
    z(f'<rect x="{cx - 34}" y="60" width="14" height="640" rx="7" fill="#ffffff" opacity="0.45"/>')
    z.guardar(textura=False)
    return _a(n)


def muneco_nieve(n="muneco_nieve"):
    """Muñeco de nieve con bufanda roja, botones de carbón y nariz de zanahoria."""
    w, h = 520, 760
    z = Lz(n, w, h, **FRIO)
    sombra_suelo(z, w / 2, h - 30, 210)
    nieve = lambda cx, cy, r: z(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{z.rad((cx - r * 0.35, cy - r * 0.4), r * 1.3, [(0, "#ffffff"), (0.55, "#eef4fb"), (0.85, "#b8cbe0"), (1, "#8aa4c4")])}"/>')
    nieve(260, 560, 180)
    nieve(260, 330, 125)
    nieve(260, 160, 88)
    for y in (300, 350, 400):
        z(f'<circle cx="260" cy="{y}" r="11" fill="#1a1a20"/>')
    for x in (228, 292):
        z(f'<circle cx="{x}" cy="145" r="10" fill="#14141a"/><circle cx="{x - 3}" cy="141" r="3" fill="#ffffff" opacity="0.8"/>')
    z(f'<path d="M258 168 L340 182 L258 186 Z" fill="{z.lin((258, 0), (340, 0), [(0, "#e8701a"), (1, "#ffa040")])}"/>')
    for k, x in enumerate((222, 240, 260, 280, 298)):
        z(f'<circle cx="{x}" cy="{205 + (k - 2) ** 2 * 3}" r="5" fill="#1a1a20"/>')
    z(f'<path d="M168 230 Q260 270 352 230 L356 262 Q260 300 164 262 Z" fill="{z.lin((0, 230), (0, 290), [(0, "#e04040"), (1, "#8a1a1a")])}"/>',
      f'<path d="M300 262 L330 380 L292 384 L276 268 Z" fill="{z.lin((280, 0), (330, 0), [(0, "#c02a2a"), (1, "#7a1616")])}"/>')
    # brazos de rama
    z('<path d="M150 330 L40 250 M85 282 L60 230 M370 330 L480 260 M440 285 L470 236" stroke="#5a3a20" stroke-width="12" stroke-linecap="round" fill="none"/>')
    z.guardar()
    return _a(n)


def bola_nieve(n="bola_nieve"):
    w = h = 200
    z = Lz(n, w, h, **FRIO)
    z(f'<circle cx="100" cy="100" r="80" fill="{z.rad((75, 70), 110, [(0, "#ffffff"), (0.6, "#e6eef8"), (1, "#9ab4d0")])}"/>')
    r = _rnd(4)
    for _ in range(14):
        z(f'<circle cx="{r.uniform(45, 155):.0f}" cy="{r.uniform(45, 155):.0f}" r="{r.uniform(4, 10):.0f}" fill="#c8d8ea" opacity="0.6"/>')
    z.guardar(textura=False)
    return _a(n)


def nieve_suelo(n="nieve_suelo", w=1200, h=520):
    """Franja de nieve en primer término (montones suaves con brillos), transparente arriba."""
    z = Lz(n, w, h, **FRIO)
    r = _rnd(9)
    d = f"M0 {h} L0 120"
    x = 0
    while x < w:
        nx = x + r.uniform(120, 240)
        d += f" Q{(x + nx) / 2:.0f} {r.uniform(40, 110):.0f} {nx:.0f} {r.uniform(100, 140):.0f}"
        x = nx
    d += f" L{w} {h} Z"
    z(f'<path d="{d}" fill="{z.lin((0, 40), (0, h), [(0, "#ffffff"), (0.35, "#e4edf8"), (1, "#9ab0cc")])}"/>')
    for _ in range(60):
        z(f'<circle cx="{r.uniform(0, w):.0f}" cy="{r.uniform(140, h):.0f}" r="{r.uniform(1.5, 4):.1f}" fill="#ffffff" opacity="{r.uniform(0.5, 1):.2f}"/>')
    z.guardar()
    return _a(n)


# =========================================================================== 01 · cerca del Sol en enero
def haz(n, oblicuo=False):
    """Linterna/rayo de sol sobre un trozo de suelo: vertical = mancha pequeña e intensa; oblicuo = mancha larga y floja."""
    w, h = 1000, 900
    z = Lz(n, w, h, **FUEGO)
    # suelo en perspectiva
    z(f'<path d="M0 640 L1000 640 L1000 900 L0 900 Z" fill="{z.lin((0, 640), (0, 900), [(0, "#6a8a4a"), (1, "#2a3a1e")])}"/>')
    z('<path d="M0 640 L1000 640" stroke="#a8c878" stroke-width="4" opacity="0.6"/>')
    if not oblicuo:
        z(f'<path d="M420 40 L580 40 L580 700 L420 700 Z" fill="{z.lin((0, 40), (0, 700), [(0, "#fff2a0", 0.95), (1, "#ffd040", 0.75)])}"/>',
          f'<ellipse cx="500" cy="700" rx="110" ry="34" fill="{z.rad((500, 700), 120, [(0, "#ffffff"), (0.5, "#fff2a0"), (1, "#ffd040", 0.2)])}"/>')
    else:
        z(f'<path d="M40 60 L180 40 L940 700 L380 720 Z" fill="{z.lin((0, 0), (900, 700), [(0, "#fff2a0", 0.75), (1, "#ffd040", 0.3)])}"/>',
          f'<ellipse cx="660" cy="705" rx="300" ry="40" fill="{z.rad((660, 705), 300, [(0, "#fff2a0", 0.55), (0.7, "#ffd040", 0.35), (1, "#ffd040", 0)])}"/>')
    z.guardar(textura=False)
    return _a(n)


def eje_tierra(n="eje_tierra"):
    """Varilla del eje de giro con flechita de rotación (se coloca encima de `tierra_hd`, girada 23°)."""
    w, h = 120, 1000
    z = Lz(n, w, h)
    z(f'<rect x="54" y="20" width="12" height="960" rx="6" fill="{z.lin((54, 0), (66, 0), [(0, "#ffffff"), (1, "#9ad8ff")])}"/>',
      '<circle cx="60" cy="20" r="14" fill="#ff4a6a"/><circle cx="60" cy="980" r="14" fill="#2ff3ff"/>',
      '<path d="M10 120 Q60 150 110 120" stroke="#ffffff" stroke-width="7" fill="none"/><path d="M110 120 l-22 -4 l8 18 Z" fill="#ffffff"/>')
    z.guardar(textura=False)
    return _a(n)


def bg_espacio_orbita(L, sem=611):
    w, h = L.w, L.h
    L.add(L.rect(L.lg((0, "#02030a"), (0.5, "#0a1030"), (1, "#120a26"))))
    L.add(L.luz(w * 0.5, h * 0.55, w * 0.9, 700, "#3a2a8a", 0.35))
    L.add(L.polvo(140, 0, 0, w, h, "#ffffff", 2.0, 0.85, sem=sem))
    return {}


# =========================================================================== 02 · nevada de 1967
def columna_angel(n="columna_angel"):
    """Columna conmemorativa alta con figura dorada alada arriba (monumento de avenida, silueta de noche)."""
    w, h = 420, 1700
    z = Lz(n, w, h, **FRIO)
    cx = w / 2
    # basamento
    z(f'<path d="M30 1690 L390 1690 L370 1560 L50 1560 Z" fill="{z.lin((30, 0), (390, 0), [(0, "#3a3a46"), (0.4, "#8a8a98"), (1, "#2a2a34")])}"/>',
      f'<rect x="80" y="1460" width="260" height="110" fill="{z.lin((80, 0), (340, 0), [(0, "#4a4a56"), (0.4, "#a0a0ae"), (1, "#34343e")])}"/>')
    # fuste
    z(f'<path d="M{cx - 46} 1460 L{cx - 34} 330 L{cx + 34} 330 L{cx + 46} 1460 Z" fill="{z.lin((cx - 46, 0), (cx + 46, 0), [(0, "#4a4a56"), (0.35, "#c8c8d4"), (0.6, "#9a9aa8"), (1, "#3a3a46")])}"/>')
    for y in range(400, 1460, 150):
        z(f'<rect x="{cx - 50}" y="{y}" width="100" height="16" fill="#d8d8e2" opacity="0.6"/>')
    z(f'<rect x="{cx - 60}" y="300" width="120" height="40" fill="{z.lin((cx - 60, 0), (cx + 60, 0), [(0, "#5a5a66"), (0.4, "#d8d8e2"), (1, "#4a4a56")])}"/>')
    # figura dorada alada
    oro = z.lin((cx - 120, 0), (cx + 120, 0), [(0, "#8a5a10"), (0.4, "#ffe08a"), (0.6, "#e0a830"), (1, "#7a4a0c")])
    z(f'<path d="M{cx} 300 L{cx - 28} 180 Q{cx - 20} 120 {cx} 110 Q{cx + 22} 120 {cx + 26} 180 Z" fill="{oro}"/>',
      f'<circle cx="{cx}" cy="92" r="22" fill="{oro}"/>',
      f'<path d="M{cx - 18} 150 Q{cx - 150} 60 {cx - 170} 190 Q{cx - 90} 150 {cx - 20} 190 Z" fill="{oro}"/>',
      f'<path d="M{cx + 18} 150 Q{cx + 150} 60 {cx + 170} 190 Q{cx + 90} 150 {cx + 20} 190 Z" fill="{oro}"/>',
      f'<path d="M{cx + 20} 120 L{cx + 60} 40" stroke="#ffe08a" stroke-width="8" stroke-linecap="round"/>')
    # nieve en las cornisas
    for y, a in ((300, 64), (1460, 134), (1560, 164)):
        z(f'<path d="M{cx - a} {y} Q{cx} {y - 22} {cx + a} {y} Z" fill="#ffffff" opacity="0.95"/>')
    z.guardar()
    return _a(n)


def nieve_capota(n="nieve_capota"):
    """Capa de nieve para ponerla sobre `coche_crema` (mismo ancho)."""
    w, h = 900, 220
    z = Lz(n, w, h, **FRIO)
    z(f'<path d="M80 200 Q120 150 230 140 Q300 60 420 50 Q560 40 640 120 Q760 120 830 170 Q860 200 840 210 L90 212 Z" '
      f'fill="{z.lin((0, 40), (0, 212), [(0, "#ffffff"), (1, "#c8d8ea")])}"/>')
    z.guardar(textura=False)
    return _a(n)


def foto_1967(n="foto_1967"):
    """Foto antigua en blanco y negro con borde blanco: calle nevada con una columna y gente."""
    w, h = 700, 820
    z = Lz(n, w, h, **SALA)
    z(f'<rect x="10" y="10" width="680" height="800" rx="8" fill="#f4efe2"/>')
    z(f'<rect x="40" y="40" width="620" height="620" fill="{z.lin((0, 40), (0, 660), [(0, "#8a8a86"), (0.55, "#c8c8c0"), (1, "#f0f0ea")])}"/>')
    z('<rect x="330" y="120" width="26" height="420" fill="#3a3a38"/><path d="M343 80 l-40 40 l80 0 Z" fill="#2a2a28"/>')
    r = _rnd(67)
    for _ in range(8):
        x = r.uniform(70, 620)
        hh = r.uniform(60, 90)
        z(f'<rect x="{x:.0f}" y="{560 - hh:.0f}" width="16" height="{hh:.0f}" rx="7" fill="#2a2a28"/><circle cx="{x + 8:.0f}" cy="{552 - hh:.0f}" r="11" fill="#2a2a28"/>')
    z(f'<path d="M40 560 Q330 520 660 560 L660 660 L40 660 Z" fill="#f6f6f2"/>')
    for _ in range(120):
        z(f'<circle cx="{r.uniform(45, 655):.0f}" cy="{r.uniform(45, 650):.0f}" r="{r.uniform(1.5, 3.5):.1f}" fill="#ffffff" opacity="0.85"/>')
    z(f'<rect x="40" y="40" width="620" height="620" fill="#8a6a3a" opacity="0.18"/>')
    z(f'<text x="350" y="750" font-family="DejaVu Serif" font-size="58" text-anchor="middle" fill="#3a3028" font-style="italic">enero de 1967</text>')
    z.guardar()
    return _a(n)


def bg_reforma_nieve(L, sem=621):
    """Avenida ancha de noche, todo nevado, farolas con halo y nieve cayendo (sin coches modernos)."""
    w, h = L.w, L.h
    L.add(L.rect(L.lg((0, "#0a0e22"), (0.45, "#1e2848"), (0.7, "#3a4868"), (1, "#c8d4e6"))))
    L.add(L.luz(w * 0.5, h * 0.62, w, 380, "#ffd8a0", 0.25))
    r = L.r
    # edificios a los lados, años 60 (bloques con ventanas)
    for lado in (0, 1):
        x = -20 if lado == 0 else w * 0.62
        while (x < w * 0.38) if lado == 0 else (x < w + 20):
            bw, bh = r.uniform(90, 170), r.uniform(380, 760)
            yb = h * 0.66
            L.add(f'<rect x="{x:.0f}" y="{yb - bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="#1a2034"/>')
            for yy in range(int(yb - bh + 20), int(yb - 30), 34):
                for xx in range(int(x + 12), int(x + bw - 16), 26):
                    if r.random() < 0.45:
                        L.add(f'<rect x="{xx}" y="{yy}" width="12" height="16" fill="#ffd28a" opacity="{r.uniform(0.5, 0.95):.2f}"/>')
            L.add(f'<path d="M{x:.0f} {yb - bh:.0f} q{bw / 2:.0f} -14 {bw:.0f} 0 Z" fill="#ffffff" opacity="0.9"/>')
            x += bw + r.uniform(4, 20)
    # avenida nevada en perspectiva
    L.add(f'<path d="M0 {h * 0.66:.0f} L{w} {h * 0.66:.0f} L{w} {h} L0 {h} Z" fill="{L.lg((0, "#dfe8f4"), (1, "#a8bcd6"))}"/>')
    L.add(f'<path d="M{w * 0.45:.0f} {h * 0.66:.0f} L{w * 0.1:.0f} {h} M{w * 0.55:.0f} {h * 0.66:.0f} L{w * 0.9:.0f} {h}" stroke="#8aa0bc" stroke-width="6" opacity="0.5"/>')
    for k in range(6):
        y = h * (0.7 + 0.05 * k)
        L.add(f'<ellipse cx="{w * 0.5:.0f}" cy="{y:.0f}" rx="{120 + k * 60}" ry="6" fill="#ffffff" opacity="0.4"/>')
    L.add(L.polvo(220, 0, 0, w, h, "#ffffff", 4.5, 0.9, sem=sem))
    return {}


# =========================================================================== 03 · el vidrio no se escurre
def _arco(x0, y0, x1, y1):
    cx = (x0 + x1) / 2
    return f"M{x0} {y1} L{x0} {y0 + (x1 - x0) * 0.5} Q{x0} {y0} {cx} {y0} Q{x1} {y0} {x1} {y0 + (x1 - x0) * 0.5} L{x1} {y1} Z"


def vidriera(n="vidriera", gotea=False):
    """Ventana gótica de vidriera de colores, con marco de piedra. `gotea`: el cristal parece escurrirse hacia abajo."""
    w, h = 700, 1520 if gotea else 1300
    z = Lz(n, w, h, **SALA)
    z(f'<path d="{_arco(20, 20, 680, 1280)}" fill="{z.lin((20, 0), (680, 0), [(0, "#4a4038"), (0.4, "#a89a88"), (1, "#3a322c")])}"/>')
    clip = z.clip(_arco(80, 80, 620, 1220))
    r = _rnd(31)
    cols = ["#c0392b", "#2a6ad8", "#f0b030", "#2aa86a", "#8a3ab8", "#e8702a", "#2ac0d8"]
    piezas = []
    for row in range(14):
        for col in range(6):
            x = 80 + col * 90 + r.uniform(-10, 10)
            y = 80 + row * 85 + r.uniform(-8, 8)
            piezas.append(f'<path d="M{x:.0f} {y:.0f} l{90 + r.uniform(-8, 8):.0f} {r.uniform(-10, 10):.0f} l{r.uniform(-8, 8):.0f} {85 + r.uniform(-6, 6):.0f} l{-90 + r.uniform(-8, 8):.0f} {r.uniform(-8, 8):.0f} Z" '
                          f'fill="{r.choice(cols)}" opacity="{r.uniform(0.75, 0.95):.2f}" stroke="#1a1410" stroke-width="7"/>')
    z(f'<g clip-path="{clip}"><rect x="80" y="80" width="540" height="1140" fill="#1a1410"/>{"".join(piezas)}'
      f'<rect x="80" y="80" width="540" height="1140" fill="{z.lin((0, 80), (0, 1220), [(0, "#ffffff", 0.25), (0.5, "#ffffff", 0), (1, "#000000", 0.25)])}"/></g>')
    z(f'<path d="M350 80 L350 1220 M80 650 L620 650" stroke="#2a221c" stroke-width="16"/>')
    if gotea:
        for k, x in enumerate((130, 215, 300, 395, 480, 565)):
            L_ = 130 + (k * 53) % 140
            c = cols[k % len(cols)]
            z(f'<path d="M{x - 34} 1170 C{x - 30} {1250 + L_ * 0.4} {x - 16} {1260 + L_} {x} {1270 + L_} C{x + 16} {1260 + L_} {x + 30} {1250 + L_ * 0.4} {x + 34} 1170 Z" '
              f'fill="{z.lin((0, 1170), (0, 1290 + L_), [(0, c), (0.7, c, 0.85), (1, "#ffffff", 0.7)])}"/>',
              f'<ellipse cx="{x - 10}" cy="{1250 + L_ * 0.5}" rx="6" ry="{20 + L_ * 0.15}" fill="#ffffff" opacity="0.45"/>')
    z.guardar()
    return _a(n)


def corte_cristal(n="corte_cristal"):
    """Corte de un cristal antiguo: más fino arriba, más grueso abajo (cuña de vidrio verdoso)."""
    w, h = 500, 1100
    z = Lz(n, w, h, **SALA)
    z(f'<path d="M220 40 L280 40 L330 1060 L170 1060 Z" fill="{z.lin((170, 0), (330, 0), [(0, "#4a8a7a", 0.85), (0.4, "#c8f0e0", 0.95), (1, "#2a6a5a", 0.85)])}" stroke="#e8fff6" stroke-width="4"/>',
      f'<path d="M232 60 L240 60 L250 1040 L222 1040 Z" fill="#ffffff" opacity="0.5"/>')
    r = _rnd(5)
    for _ in range(18):
        y = r.uniform(80, 1020)
        z(f'<circle cx="{250 + r.uniform(-20, 20):.0f}" cy="{y:.0f}" r="{r.uniform(2, 5):.1f}" fill="#ffffff" opacity="0.6"/>')
    z.guardar(textura=False)
    return _a(n)


def bola_vidrio(n="bola_vidrio"):
    """Bola de vidrio al rojo en la punta de la caña de soplar."""
    w, h = 1000, 600
    z = Lz(n, w, h, **FUEGO)
    z(f'<rect x="0" y="282" width="560" height="36" rx="18" fill="{z.lin((0, 282), (0, 318), [(0, "#c8c8d0"), (0.4, "#ffffff"), (1, "#5a5a66")])}"/>')
    z(f'<circle cx="740" cy="300" r="250" fill="{z.rad((740, 300), 300, [(0, "#ffb040", 0.5), (1, "#ff6a10", 0)])}"/>',
      f'<circle cx="740" cy="300" r="190" fill="{z.rad((690, 240), 230, [(0, "#fffbe0"), (0.35, "#ffd060"), (0.75, "#ff8a20"), (1, "#c03a08")])}"/>',
      f'<path d="M560 270 Q600 260 620 230 L620 370 Q600 340 560 330 Z" fill="#ffb040"/>',
      f'<ellipse cx="680" cy="220" rx="50" ry="30" fill="#ffffff" opacity="0.6"/>')
    z.guardar(textura=False)
    return _a(n)


def disco_vidrio(n="disco_vidrio"):
    """Disco de vidrio aplanado y girado (corona): grueso en el centro, anillos desiguales."""
    w = h = 900
    z = Lz(n, w, h, **SALA)
    z(f'<circle cx="450" cy="450" r="420" fill="{z.rad((450, 450), 420, [(0, "#2a7a68", 0.95), (0.3, "#7ac8b0", 0.7), (1, "#d8fff0", 0.45)])}" stroke="#e8fff6" stroke-width="6"/>')
    for k, r_ in enumerate((60, 120, 190, 260, 330, 390)):
        z(f'<circle cx="450" cy="450" r="{r_}" fill="none" stroke="#ffffff" stroke-width="{6 - k * 0.7:.1f}" opacity="{0.5 - k * 0.05:.2f}"/>')
    z('<circle cx="450" cy="450" r="45" fill="#1a4a40"/><path d="M220 230 Q300 160 420 150" stroke="#ffffff" stroke-width="16" opacity="0.5" fill="none" stroke-linecap="round"/>')
    z.guardar(textura=False)
    return _a(n)


def cilindro_vidrio(n="cilindro_vidrio"):
    w, h = 600, 1000
    z = Lz(n, w, h, **SALA)
    z(f'<rect x="100" y="120" width="400" height="760" fill="{z.lin((100, 0), (500, 0), [(0, "#3a8a74", 0.8), (0.35, "#d8fff0", 0.75), (0.7, "#7ac8b0", 0.6), (1, "#2a6a5a", 0.85)])}" stroke="#e8fff6" stroke-width="5"/>',
      f'<ellipse cx="300" cy="120" rx="200" ry="50" fill="#bff0e0" opacity="0.6" stroke="#e8fff6" stroke-width="5"/>',
      f'<ellipse cx="300" cy="880" rx="200" ry="50" fill="#4a9a84" opacity="0.7" stroke="#e8fff6" stroke-width="5"/>',
      f'<path d="M300 70 L300 930" stroke="#ff5a3a" stroke-width="8" stroke-dasharray="26 16"/>')
    z.guardar(textura=False)
    return _a(n)


def panel_vidrio(n="panel_vidrio"):
    """Cristal suelto (para que lo sostenga el cristalero): verdoso, con ondas."""
    w, h = 360, 520
    z = Lz(n, w, h, **SALA)
    z(f'<rect x="20" y="20" width="320" height="480" rx="6" fill="{z.lin((20, 0), (340, 520), [(0, "#d8fff0", 0.75), (0.5, "#7ac8b0", 0.55), (1, "#3a8a74", 0.8)])}" stroke="#e8fff6" stroke-width="6"/>')
    for k in range(5):
        y = 90 + k * 90
        z(f'<path d="M40 {y} Q180 {y - 25} 320 {y}" stroke="#ffffff" stroke-width="4" opacity="0.4" fill="none"/>')
    z(f'<rect x="20" y="420" width="320" height="80" fill="#2a6a5a" opacity="0.45"/>')
    z.guardar(textura=False)
    return _a(n)


def abadia(n="abadia"):
    """Fachada gótica con dos torres (abadía medieval), piedra clara al atardecer."""
    w, h = 1000, 1200
    z = Lz(n, w, h, **FUEGO)
    piedra = z.lin((0, 0), (1000, 0), [(0, "#6a5a48"), (0.45, "#e8d8b8"), (0.6, "#c8b490"), (1, "#5a4a3a")])
    for x0 in (60, 700):
        z(f'<rect x="{x0}" y="200" width="240" height="1000" fill="{piedra}"/>',
          f'<path d="M{x0 - 10} 200 L{x0 + 120} 40 L{x0 + 250} 200 Z" fill="#5a4a3a"/>')
        for y in (300, 520, 740):
            z(f'<path d="{_arco(x0 + 80, y, x0 + 160, y + 160)}" fill="#1a1420"/>')
        for k in range(6):
            z(f'<rect x="{x0 + k * 40}" y="180" width="22" height="30" fill="{piedra}"/>')
    z(f'<rect x="300" y="420" width="400" height="780" fill="{piedra}"/>',
      f'<path d="M290 420 L500 260 L710 420 Z" fill="#6a5a48"/>',
      f'<circle cx="500" cy="560" r="110" fill="{z.rad((500, 560), 110, [(0, "#f0b030"), (0.5, "#c0392b"), (1, "#2a6ad8")])}" stroke="#3a2c20" stroke-width="12"/>',
      f'<path d="{_arco(400, 760, 600, 1200)}" fill="#1a1420"/>')
    for k in range(12):
        z(f'<path d="M500 560 L{500 + 110 * math.cos(k * math.pi / 6):.0f} {560 + 110 * math.sin(k * math.pi / 6):.0f}" stroke="#3a2c20" stroke-width="6"/>')
    z.guardar()
    return _a(n)


def virus(n="virus"):
    w = h = 500
    z = Lz(n, w, h, **SALA)
    for k in range(16):
        a = k * math.pi / 8
        x1, y1 = 250 + 150 * math.cos(a), 250 + 150 * math.sin(a)
        x2, y2 = 250 + 220 * math.cos(a), 250 + 220 * math.sin(a)
        z(f'<path d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}" stroke="#ff5a8a" stroke-width="12"/><circle cx="{x2:.0f}" cy="{y2:.0f}" r="16" fill="#ff8ab0"/>')
    z(f'<circle cx="250" cy="250" r="160" fill="{z.rad((210, 200), 200, [(0, "#ffd0e0"), (0.5, "#e0507a"), (1, "#7a1a3a")])}"/>')
    z.guardar(textura=False)
    return _a(n)


def atomos(n, orden=True):
    """Átomos en red ordenada (cristal) o desordenada (vidrio)."""
    w = h = 900
    z = Lz(n, w, h, **SALA)
    r = _rnd(12)
    pts = []
    for i in range(7):
        for j in range(7):
            x, y = 120 + i * 110, 120 + j * 110
            if not orden:
                x += r.uniform(-40, 40)
                y += r.uniform(-40, 40)
            pts.append((x, y))
    for (x, y) in pts:
        for (x2, y2) in pts:
            if 0 < math.hypot(x2 - x, y2 - y) < 135 and (x, y) < (x2, y2):
                z(f'<path d="M{x:.0f} {y:.0f} L{x2:.0f} {y2:.0f}" stroke="#7df9ff" stroke-width="5" opacity="0.5"/>')
    for (x, y) in pts:
        z(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="30" fill="{z.rad((x - 10, y - 10), 40, [(0, "#ffffff"), (0.5, "#2ff3ff"), (1, "#0a4a8a")])}"/>')
    z.guardar(textura=False)
    return _a(n)


def bg_catedral(L, sem=631):
    """Interior de catedral en penumbra con haces de luz de colores entrando en diagonal."""
    w, h = L.w, L.h
    L.add(L.rect(L.lg((0, "#0e0c14"), (0.6, "#1e1a24"), (1, "#2a2420"))))
    for k, x in enumerate((140, 940)):
        L.add(f'<rect x="{x - 70}" y="0" width="140" height="{h}" fill="{L.lg((0, "#2a2430"), (0.5, "#4a4048"), (1, "#1a161e"), x1=0, y1=0, x2=1, y2=0)}"/>')
    for k in range(5):
        y = 200 + k * 260
        L.add(f'<path d="M140 {y} Q540 {y - 200} 940 {y}" stroke="#3a3238" stroke-width="18" fill="none"/>')
    for k, c in enumerate(("#c0392b", "#2a6ad8", "#f0b030")):
        x = 200 + k * 260
        L.add(f'<path d="M{x} 0 L{x + 120} 0 L{x + 520} {h} L{x + 260} {h} Z" fill="{c}" opacity="0.13"/>')
    L.add(f'<rect x="0" y="{h * 0.8:.0f}" width="{w}" height="{h * 0.2:.0f}" fill="{L.lg((0, "#3a3028"), (1, "#14100c"))}"/>')
    L.add(L.polvo(70, 0, 0, w, h, "#ffe6c0", 2.2, 0.6, sem=sem))
    return {}


def bg_taller_vidrio(L, sem=641):
    """Taller de vidriero: horno con la boca al rojo al fondo, penumbra cálida."""
    w, h = L.w, L.h
    L.add(L.rect(L.lg((0, "#140a06"), (0.6, "#2a160c"), (1, "#1a0e08"))))
    L.add(f'<path d="M240 700 Q540 420 840 700 L840 1300 L240 1300 Z" fill="#3a2a22"/>')
    L.add(f'<ellipse cx="540" cy="1000" rx="170" ry="150" fill="{L.rgu(540, 1000, 170, 150, (0, "#fff2a0", 1), (0.5, "#ff8a20", 1), (1, "#a02a08", 1))}"/>')
    L.add(L.luz(540, 1000, 600, 500, "#ff7a20", 0.55))
    L.add(f'<rect x="0" y="1300" width="{w}" height="{h - 1300}" fill="#120a06"/>')
    L.add(L.polvo(60, 200, 600, 880, 1300, "#ffb060", 3.0, 0.8, sem=sem))
    return {}


def generar(dirsvg):
    T27.generar(dirsvg)
    ilus.OUT = dirsvg
    # comunes
    termometro("termo_frio", 0.12, True); termometro("termo_calor", 0.85, False)
    muneco_nieve(); bola_nieve(); nieve_suelo()
    # 01
    haz("haz_vertical"); haz("haz_oblicuo", oblicuo=True); eje_tierra()
    # 02
    columna_angel(); nieve_capota(); foto_1967()
    T25.p_de_pie("nino67", NINO67, 3, "sonrisa", 0, luz=FRIO)
    T25.p_de_pie("nina67", NINA67, 1, "sonrisa", 2, luz=FRIO)
    _a(busto("cara_abuela", ABUELA, "sonrisa", ang=3, luz=SALA))
    _a(busto("cara_nino67", NINO67, "sorpresa", ang=-3, luz=FRIO))
    # 03
    vidriera("vidriera"); vidriera("vidriera_gotea", gotea=True); corte_cristal(); bola_vidrio(); disco_vidrio(); cilindro_vidrio()
    panel_vidrio(); abadia(); virus(); atomos("atomos_orden", True); atomos("atomos_desorden", False)
    T25.p_de_pie("cristalero", CRISTALERO, 1, "neutra", 0, luz=FUEGO)
    for i, f in enumerate((bg_espacio_orbita, bg_reforma_nieve, bg_catedral, bg_taller_vidrio)):
        L = IE.Lienzo(f.__name__, 1080, 1920, 6100 + i * 13)
        f(L)
        L.guardar(dirsvg, f.__name__)
        NOMBRES.append(f.__name__)
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
