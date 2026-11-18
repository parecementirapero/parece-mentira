"""Ilustraciones del vídeo 03 del lote 2026-11-18-manana («Tu perro copia tus bostezos»).
Uso: python3 ilus_03.py DIR_SVG   (semillas fijas). Ladrillos de motor/biblioteca/ilus.py.
Reutiliza las de los lotes 2026-11-17 (cara de perfil, oreja, laboratorio, edificio, cámara…).

Perro que bosteza en 3 piezas con la bisagra de la mandíbula en el CENTRO del lienzo (450, 450 de 900×900), para que
al girarlas con `rot` giren alrededor de la bisagra: `perro_sup_*` (cráneo, oreja, ojo, hocico de arriba, cuello),
`perro_mand_*` (mandíbula con dientes y lengua) y `perro_boca_*` (interior de la boca: cuña que se abre con `ey`).
Las claves las calcula `bostezo()` en gen_03.py."""
import math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "lotes", "2026-11-17-tarde", "generadores"))
sys.path.insert(0, os.path.join(RAIZ, "lotes", "2026-11-17-manana", "generadores"))
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano, _neb, _mascara, _estrellas_ricas  # noqa: E402,F401
import ilus_tarde  # noqa: E402

RAZAS = {
    # nombre: (lomo, panza, hocico, oreja, luz, manchas)
    "dorado": ("#e0a352", "#9a5a22", "#f0c47a", "#b06a2a", "#ffe2a0", 0),
    "negro": ("#3a3430", "#141010", "#4a3a30", "#1e1a18", "#c8b8ff", 0),
    "dalmata": ("#f4f0ea", "#b8b0a6", "#fbf8f2", "#2a2624", "#ffffff", 26),
    "beagle": ("#b8742e", "#6a3a16", "#f6f0e6", "#5a3014", "#ffd9a0", 0),
}

ANG_MAX = 40  # apertura máxima de la boca (grados) que cubre la cuña del interior


# ====================================================================== perro que bosteza (3 piezas)
def _cabeza_sup(raza):
    lomo, panza, hocico, oreja, luz, manchas = RAZAS[raza]
    r = random.Random(len(raza))
    n = f"ps_{raza}"
    d = (lg(f"{n}_c", (0, lomo), (0.6, lomo), (1, panza)) + lg(f"{n}_h", (0, hocico), (1, lomo), x2=0, y2=1) +
         rg(f"{n}_l", (0, luz, 0.55), (1, luz, 0)) + lg(f"{n}_o", (0, oreja), (0.7, panza), (1, "#1a0e06"), x2=0.3, y2=1))
    forma = ("M120 270 C135 125 300 70 425 118 C482 146 505 228 545 290 C625 312 720 335 790 360 "
             "C832 376 852 400 846 426 C840 448 815 455 790 453 L470 453 C445 456 428 476 426 512 "
             "C436 610 476 730 570 900 L0 900 L0 540 C38 440 90 340 120 270 Z")
    hoc = "M500 300 C620 318 720 338 790 362 C832 376 852 400 846 426 C840 448 815 455 790 453 L500 453 C480 420 480 340 500 300 Z"
    b = [f'<clipPath id="{n}_clip"><path d="{forma}"/></clipPath>',
         f'<path d="{forma}" fill="url(#{n}_c)"/>',
         f'<path d="{hoc}" fill="url(#{n}_h)" opacity="0.85"/>',
         f'<g clip-path="url(#{n}_clip)">']
    for _ in range(manchas):
        b.append(f'<ellipse cx="{r.uniform(60, 800):.0f}" cy="{r.uniform(150, 880):.0f}" rx="{r.uniform(12, 26):.0f}" ry="{r.uniform(10, 20):.0f}" fill="#1a1614" opacity="0.92"/>')
    if raza == "beagle":  # franja blanca en la frente y pecho blanco
        b.append('<path d="M430 165 C470 192 500 255 540 298 L500 330 C470 290 440 230 400 180 Z" fill="#f6f0e6" opacity="0.9"/>')
        b.append('<path d="M412 498 C385 565 372 690 385 900 L250 900 C260 700 300 560 360 470 Z" fill="#f6f0e6" opacity="0.92"/>')
    # pelo: trazos cortos
    for _ in range(320):
        x, y = r.uniform(60, 840), r.uniform(130, 890)
        c = r.choice([luz, panza])
        b.append(f'<path d="M{x:.0f} {y:.0f} q{r.uniform(-8, 8):.0f} {r.uniform(6, 12):.0f} {r.uniform(-4, 4):.0f} {r.uniform(12, 22):.0f}" stroke="{c}" stroke-width="2.4" fill="none" opacity="0.35"/>')
    b.append(f'<rect width="900" height="900" fill="#888" filter="url(#grano)"/>')
    b.append(f'<ellipse cx="420" cy="230" rx="300" ry="220" fill="url(#{n}_l)"/>')
    b.append('</g>')
    b.append(f'<path d="{forma}" fill="none" stroke="{luz}" stroke-width="4" opacity="0.55"/>')
    # dientes de arriba (blancos, hacia abajo) y colmillo
    for x in range(560, 780, 26):
        b.append(f'<path d="M{x} 451 L{x+12} 466 L{x+24} 451 Z" fill="#fbf6ea"/>')
    b.append('<path d="M722 450 C726 470 732 486 738 494 C744 480 748 466 750 450 Z" fill="#fffaf0" stroke="#d8cfc0" stroke-width="2"/>')
    # belfo (labio de arriba) que cuelga un poco
    b.append(f'<path d="M520 448 C600 470 680 472 760 456 L760 450 L520 450 Z" fill="{panza}" opacity="0.9"/>')
    # nariz
    b.append('<ellipse cx="826" cy="398" rx="36" ry="30" fill="#141010"/><ellipse cx="814" cy="388" rx="12" ry="7" fill="#ffffff" opacity="0.35"/>'
             '<ellipse cx="843" cy="408" rx="7" ry="5" fill="#000"/>')
    # oreja caída
    b.append(f'<path d="M240 150 C170 180 110 300 118 430 C124 540 180 610 240 590 C300 560 322 460 318 350 C315 260 292 175 240 150 Z" fill="url(#{n}_o)"/>')
    b.append(f'<path d="M240 165 C190 230 160 330 168 450" stroke="{luz}" stroke-width="3" fill="none" opacity="0.35"/>')
    # ojo con ceja
    b.append('<ellipse cx="468" cy="300" rx="24" ry="20" fill="#1a1208"/><circle cx="476" cy="292" r="7" fill="#fff6d8"/>'
             f'<path d="M430 268 C455 252 490 254 510 270" stroke="{panza}" stroke-width="9" fill="none" stroke-linecap="round" opacity="0.8"/>')
    # bigotes
    for k in range(5):
        b.append(f'<path d="M{700+k*18} {420+k*4} q40 {-4+k*3} 90 {6+k*6}" stroke="#2a2018" stroke-width="2" fill="none" opacity="0.5"/>')
    guardar(f"perro_sup_{raza}", "".join(b), 900, 900, d)


def _cabeza_mand(raza):
    lomo, panza, hocico, oreja, luz, manchas = RAZAS[raza]
    n = f"pm_{raza}"
    d = lg(f"{n}_c", (0, lomo), (1, panza)) + lg(f"{n}_t", (0, "#ff8fa8"), (1, "#c84a6a"))
    mand = "M430 446 L790 450 C808 452 812 470 796 486 C762 518 690 528 600 522 C530 516 470 502 438 482 C420 470 420 455 430 446 Z"
    b = [f'<path d="{mand}" fill="url(#{n}_c)"/>',
         # lengua
         '<path d="M470 451 C560 424 690 420 765 436 C790 441 792 450 780 452 L470 452 Z" fill="url(#pm_' + raza + '_t)"/>',
         '<path d="M500 446 C580 436 680 434 760 442" stroke="#a83a58" stroke-width="4" fill="none" opacity="0.6"/>',
         '<path d="M520 432 C600 424 690 422 750 430" stroke="#ffd0dc" stroke-width="5" fill="none" opacity="0.6"/>']
    for x in range(560, 770, 26):
        b.append(f'<path d="M{x} 452 L{x+12} 438 L{x+24} 452 Z" fill="#fbf6ea"/>')
    b.append('<path d="M694 452 C698 432 704 418 708 412 C714 424 718 438 720 452 Z" fill="#fffaf0" stroke="#d8cfc0" stroke-width="2"/>')
    b.append(f'<path d="{mand}" fill="none" stroke="{luz}" stroke-width="3" opacity="0.5"/>')
    b.append(f'<path d="M500 512 C580 528 700 522 780 494" stroke="#000" stroke-width="10" fill="none" opacity="0.25" filter="url(#blur8)"/>')
    guardar(f"perro_mand_{raza}", "".join(b), 900, 900, d)


def _cabeza_boca(raza):
    a = math.radians(ANG_MAX)
    x2, y2 = 450 + 320 * math.cos(a), 450 + 320 * math.sin(a)
    d = rg("pb_g", (0, "#2a0408", 1), (0.6, "#5a0e18", 1), (1, "#8a2232", 1), cx=0.3, cy=0.2, r=0.9)
    b = [f'<path d="M440 446 L775 446 L{x2:.0f} {y2:.0f} Z" fill="url(#pb_g)"/>']
    for k in range(5):  # crestas del paladar
        t = 0.2 + k * 0.13
        b.append(f'<path d="M{450+280*t:.0f} 452 q-6 {20+k*6} -20 {40+k*10}" stroke="#a83444" stroke-width="5" fill="none" opacity="0.6"/>')
    guardar(f"perro_boca_{raza}", "".join(b), 900, 900, d)


def perro(raza):
    _cabeza_sup(raza); _cabeza_mand(raza); _cabeza_boca(raza)


# ====================================================================== perritos de la cuadrícula
def perrito(nombre, bosteza, col="#c8a070", luz="#ffe2a0"):
    """Perro sentado de perfil, pequeño (300×300), con boca cerrada o bostezando hacia arriba."""
    w, h = 300, 300
    d = lg(f"{nombre}_g", (0, col), (1, "#4a2e18"))
    osc = "#3a2414"
    cuerpo = "M70 290 C46 240 58 186 110 166 C140 150 162 132 178 112 L216 122 C216 172 210 230 214 290 L196 290 L194 244 L172 252 L160 290 Z"
    if bosteza:
        cab = ('<circle cx="194" cy="84" r="44" fill="url(#G)"/>'
               '<path d="M226 98 L282 94 C292 96 292 110 282 112 L226 114 Z" fill="url(#G)"/>'
               '<path d="M228 76 L270 36 L284 96 L226 100 Z" fill="#5a0e18"/>'
               '<path d="M232 98 C250 92 266 92 282 96" stroke="#ff8fa8" stroke-width="7" fill="none"/>'
               '<path d="M214 58 L262 22 C274 14 288 26 278 38 L234 80 Z" fill="url(#G)"/>'
               '<circle cx="280" cy="28" r="8" fill="#140c06"/>'
               '<path d="M202 70 q8 4 16 0" stroke="#140c06" stroke-width="4" fill="none"/>')
    else:
        cab = ('<circle cx="198" cy="86" r="44" fill="url(#G)"/>'
               '<path d="M222 70 L276 82 C290 86 292 104 278 108 L224 112 Z" fill="url(#G)"/>'
               '<circle cx="284" cy="88" r="8" fill="#140c06"/><circle cx="214" cy="74" r="5" fill="#140c06"/>'
               '<path d="M236 106 L270 104" stroke="#140c06" stroke-width="3" opacity="0.6"/>')
    cab = cab.replace("url(#G)", f"url(#{nombre}_g)")
    b = ['<ellipse cx="150" cy="292" rx="110" ry="10" fill="#000" opacity="0.35"/>',
         f'<path d="M78 262 C40 262 24 236 30 206" stroke="{col}" stroke-width="14" fill="none" stroke-linecap="round"/>',
         f'<path d="{cuerpo}" fill="url(#{nombre}_g)"/>', '<circle cx="110" cy="236" r="52" fill="#000" opacity="0.18"/>', cab,
         f'<path d="M176 56 C158 70 152 112 162 132 C176 126 188 100 190 66 Z" fill="{osc}"/>',
         f'<path d="{cuerpo}" fill="none" stroke="{luz}" stroke-width="3" opacity="0.5"/>']
    guardar(nombre, "".join(b), w, h, d)


# ====================================================================== personas en silueta (sin caras)
SIL_CERRADA = ("M250 120 C330 60 450 70 490 140 C510 175 505 200 515 230 L545 290 C550 300 540 305 525 305 L528 330 "
               "C520 340 515 350 522 360 C515 370 518 385 510 395 C505 420 480 440 450 445 L445 500 C520 520 600 560 620 700 "
               "L60 700 C80 560 150 520 200 500 C180 460 160 420 150 380 C120 300 160 170 250 120 Z")
SIL_ABIERTA = ("M236 132 C312 58 432 52 486 112 C512 142 514 170 526 198 L566 252 C572 264 562 270 546 272 L542 296 "
               "C530 302 516 310 500 318 L520 372 C526 392 520 420 504 434 C488 450 468 458 448 460 L445 505 "
               "C520 522 600 560 620 700 L60 700 C80 560 150 520 200 500 C178 456 156 410 146 366 C120 290 160 180 236 132 Z")


def silueta(nombre, abierta, col="#1a2238", luz="#7df9ff"):
    w, h = 680, 700
    p = SIL_ABIERTA if abierta else SIL_CERRADA
    d = lg(f"{nombre}_g", (0, col), (1, "#06080e"), x2=0.3, y2=1)
    b = [f'<path d="{p}" fill="url(#{nombre}_g)"/>',
         f'<path d="{p}" fill="none" stroke="{luz}" stroke-width="10" opacity="0.5" filter="url(#blur8)"/>',
         f'<path d="{p}" fill="none" stroke="{luz}" stroke-width="3" opacity="0.9"/>']
    guardar(nombre, "".join(b), w, h, d)


def bg_vagon():
    d = (lg("bv_c", (0, "#2a2438"), (1, "#141018")) + lg("bv_v", (0, "#0a1a3a"), (1, "#1a0a2a")) + lg("bv_a", (0, "#5a3a5a"), (1, "#2a1a2a")))
    r = random.Random(4)
    b = ['<rect width="1080" height="1920" fill="url(#bv_c)"/>']
    for x in (40, 560):
        b.append(f'<rect x="{x}" y="420" width="480" height="520" rx="40" fill="url(#bv_v)"/>')
        for _ in range(18):  # luces de ciudad desenfocadas que pasan
            b.append(f'<circle cx="{x + r.uniform(30, 450):.0f}" cy="{r.uniform(470, 900):.0f}" r="{r.uniform(10, 34):.0f}" '
                     f'fill="{r.choice(["#ffd27a", "#ff7ad8", "#7df9ff", "#ffffff"])}" opacity="{r.uniform(0.25, 0.6):.2f}" filter="url(#blur20)"/>')
        b.append(f'<rect x="{x}" y="420" width="480" height="520" rx="40" fill="none" stroke="#8a8aa8" stroke-width="12"/>')
    b.append('<rect x="0" y="220" width="1080" height="40" fill="#3a3448"/>')
    b += [f'<rect x="{x}" y="230" width="14" height="140" fill="#8a8aa8"/><circle cx="{x+7}" cy="400" r="34" fill="none" stroke="#c8c8d8" stroke-width="10"/>' for x in (180, 520, 860)]
    b.append('<rect x="0" y="1180" width="1080" height="740" fill="url(#bv_a)"/>')
    b.append('<rect x="0" y="1180" width="1080" height="30" fill="#8a5a8a" opacity="0.6"/>')
    b.append(grano())
    guardar("bg_vagon", "".join(b), defs=d)


# ====================================================================== objetos
def libro():
    w, h = 900, 600
    d = lg("lb_p", (0, "#fbf3e0"), (1, "#d8c8a8"), x2=1, y2=0) + lg("lb_q", (0, "#d8c8a8"), (1, "#fbf3e0"), x2=1, y2=0)
    b = ['<path d="M40 120 C200 60 350 70 450 130 L450 560 C350 500 200 500 40 550 Z" fill="url(#lb_p)"/>',
         '<path d="M860 120 C700 60 550 70 450 130 L450 560 C550 500 700 500 860 550 Z" fill="url(#lb_q)"/>',
         '<path d="M30 140 L30 570 C200 520 350 520 450 580 C550 520 700 520 870 570 L870 140" fill="none" stroke="#7a2a1a" stroke-width="16"/>']
    r = random.Random(3)
    for k in range(9):
        y = 170 + k * 38
        b.append(f'<path d="M90 {y+k*2} L{r.uniform(330, 400):.0f} {y-6+k*2}" stroke="#6a5a4a" stroke-width="7" opacity="0.5" stroke-linecap="round"/>')
        b.append(f'<path d="M500 {y-6+k*2} L{r.uniform(760, 810):.0f} {y+k*2}" stroke="#6a5a4a" stroke-width="7" opacity="0.5" stroke-linecap="round"/>')
    guardar("libro", "".join(b), w, h, d)


def bocadillo():
    w, h = 800, 600
    b = ['<g fill="#ffffff" opacity="0.95">',
         *[f'<circle cx="{x}" cy="{y}" r="{rr}"/>' for x, y, rr in [(260, 260, 150), (420, 210, 170), (570, 270, 150), (400, 360, 160), (230, 380, 110), (590, 390, 110)]],
         '<circle cx="190" cy="520" r="34"/><circle cx="120" cy="575" r="20"/></g>',
         '<g fill="none" stroke="#7df9ff" stroke-width="6" opacity="0.8">',
         *[f'<circle cx="{x}" cy="{y}" r="{rr}"/>' for x, y, rr in [(190, 520, 34), (120, 575, 20)]], '</g>']
    guardar("bocadillo", "".join(b), w, h)


def movil_mano():
    w, h = 700, 1100
    d = lg("mm_p", (0, "#e8b090"), (1, "#a8664a")) + lg("mm_t", (0, "#1a1a22"), (1, "#3a3a48"), x2=1, y2=1)
    b = ['<rect x="150" y="60" width="420" height="820" rx="56" fill="url(#mm_t)"/>',
         '<rect x="172" y="90" width="376" height="760" rx="40" fill="#0b1226"/>',
         '<rect x="300" y="100" width="120" height="22" rx="11" fill="#000"/>',
         '<path d="M90 1100 C80 900 110 760 160 700 C190 660 240 680 240 730 L240 860 C300 860 420 850 520 820 C600 800 650 860 620 930 C600 990 560 1040 540 1100 Z" fill="url(#mm_p)"/>',
         *[f'<path d="M560 {520+k*90} C620 {510+k*90} 660 {540+k*90} 640 {580+k*90} C620 {610+k*90} 580 {610+k*90} 560 {600+k*90} Z" fill="url(#mm_p)"/>' for k in range(3)],
         '<path d="M160 700 C130 600 150 520 190 500 C220 490 240 520 230 560 L210 700 Z" fill="url(#mm_p)"/>']
    guardar("movil_mano", "".join(b), w, h, d)


def cerebro():
    w, h = 900, 700
    d = lg("ce_g", (0, "#ffb0c8"), (1, "#c8607a")) + rg("ce_l", (0, "#ffe0ea", 0.8), (1, "#ffe0ea", 0))
    r = random.Random(5)
    forma = "M120 380 C80 260 170 120 320 110 C400 60 540 60 620 110 C760 110 860 230 830 370 C850 470 780 560 660 570 C600 620 470 630 400 590 C280 610 160 560 150 470 C120 450 110 420 120 380 Z"
    b = [f'<clipPath id="ce_c"><path d="{forma}"/></clipPath>', f'<path d="{forma}" fill="url(#ce_g)"/>', '<g clip-path="url(#ce_c)">']
    for _ in range(26):
        x, y = r.uniform(140, 800), r.uniform(120, 580)
        b.append(f'<path d="M{x:.0f} {y:.0f} c{r.uniform(20, 50):.0f} {r.uniform(-40, 40):.0f} {r.uniform(40, 80):.0f} {r.uniform(-30, 30):.0f} {r.uniform(60, 110):.0f} {r.uniform(-10, 30):.0f}" '
                 'stroke="#a03a58" stroke-width="9" fill="none" stroke-linecap="round" opacity="0.7"/>')
    b += ['<ellipse cx="380" cy="230" rx="300" ry="160" fill="url(#ce_l)"/>', '</g>',
          '<path d="M470 100 C450 240 490 420 460 600" stroke="#8a2a48" stroke-width="10" fill="none"/>',
          f'<path d="{forma}" fill="none" stroke="#ffe0ea" stroke-width="5" opacity="0.7"/>',
          '<path d="M560 580 C580 640 600 680 640 700 L700 700 C660 660 650 620 660 570 Z" fill="#c8607a"/>']
    guardar("cerebro", "".join(b), w, h, d)


def ventilador():
    w, h = 600, 600
    d = lg("ve_a", (0, "#bfe9ff"), (1, "#3a8ac8"))
    b = ['<circle cx="300" cy="300" r="280" fill="none" stroke="#7df9ff" stroke-width="12"/>',
         *[f'<line x1="300" y1="300" x2="{300+280*math.cos(math.radians(a)):.0f}" y2="{300+280*math.sin(math.radians(a)):.0f}" stroke="#7df9ff" stroke-width="4" opacity="0.5"/>' for a in range(0, 360, 20)],
         *[f'<path d="M300 300 C{300+100*math.cos(math.radians(a-20)):.0f} {300+100*math.sin(math.radians(a-20)):.0f} {300+250*math.cos(math.radians(a-8)):.0f} {300+250*math.sin(math.radians(a-8)):.0f} '
           f'{300+240*math.cos(math.radians(a+18)):.0f} {300+240*math.sin(math.radians(a+18)):.0f} Z" fill="url(#ve_a)" opacity="0.9"/>' for a in (0, 120, 240)],
         '<circle cx="300" cy="300" r="46" fill="#1a3a5a" stroke="#7df9ff" stroke-width="6"/>']
    guardar("ventilador", "".join(b), w, h, d)


def bolsa(nombre, c1, c2, hielo):
    w, h = 600, 420
    d = lg(f"{nombre}_g", (0, c1), (1, c2))
    b = [f'<path d="M60 120 C60 60 120 40 300 40 C480 40 540 60 540 120 L560 330 C560 390 480 400 300 400 C120 400 40 390 40 330 Z" fill="url(#{nombre}_g)"/>',
         '<path d="M90 110 C150 80 260 76 340 80" stroke="#ffffff" stroke-width="16" fill="none" opacity="0.5" stroke-linecap="round"/>',
         '<rect x="250" y="10" width="100" height="50" rx="14" fill="#ffffff" opacity="0.8"/>']
    if hielo:
        r = random.Random(2)
        for _ in range(7):
            x, y, s = r.uniform(120, 460), r.uniform(150, 320), r.uniform(50, 80)
            b.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{s:.0f}" height="{s:.0f}" rx="12" fill="#e8f8ff" opacity="0.75" transform="rotate({r.uniform(-30, 30):.0f} {x+s/2:.0f} {y+s/2:.0f})"/>')
    else:
        for k in range(3):
            b.append(f'<path d="M{200+k*90} 30 C{180+k*90} -10 {230+k*90} -40 {210+k*90} -80" stroke="#ffd27a" stroke-width="8" fill="none" opacity="0.6" stroke-linecap="round"/>')
    guardar(nombre, "".join(b), w, h, d)


def ecografia():
    """Imagen de ecografía (abanico gris con grano) y la silueta de perfil de un bebé con la boca abierta."""
    w, h = 1000, 1000
    d = (rg("ec_g", (0, "#6a6a6a", 1), (0.7, "#2a2a2a", 1), (1, "#0a0a0a", 1), cx=0.5, cy=0.1, r=0.95) +
         '<clipPath id="ec_c"><path d="M500 60 L940 760 C780 920 220 920 60 760 Z"/></clipPath>' +
         '<filter id="ec_n"><feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="3" seed="4"/><feColorMatrix type="saturate" values="0"/>'
         '<feComponentTransfer><feFuncA type="table" tableValues="0 0.55"/></feComponentTransfer></filter>')
    bebe = ("M330 470 C330 350 420 290 510 300 C600 310 650 380 650 450 C652 480 668 500 676 520 C680 532 670 540 660 540 "
            "L664 556 C656 566 646 572 636 578 L650 604 C652 626 636 642 612 646 C600 660 600 690 610 720 "
            "C700 740 760 800 740 860 C640 900 420 890 360 820 C310 760 320 650 360 600 C330 560 330 520 330 470 Z")
    b = ['<path d="M500 60 L940 760 C780 920 220 920 60 760 Z" fill="url(#ec_g)"/>',
         '<g clip-path="url(#ec_c)"><rect width="1000" height="1000" filter="url(#ec_n)"/>',
         '<ellipse cx="500" cy="600" rx="330" ry="300" fill="#000" opacity="0.55" filter="url(#blur20)"/>',
         f'<path d="{bebe}" fill="#d8d8d8" opacity="0.85" filter="url(#blur8)"/>',
         f'<path d="{bebe}" fill="none" stroke="#ffffff" stroke-width="6" opacity="0.9"/>',
         '<path d="M636 578 L668 544" stroke="#000" stroke-width="10" opacity="0.7"/>',
         '<rect width="1000" height="1000" filter="url(#ec_n)" opacity="0.6"/></g>',
         '<path d="M500 60 L940 760 C780 920 220 920 60 760 Z" fill="none" stroke="#7df9ff" stroke-width="5" opacity="0.6"/>']
    guardar("ecografia", "".join(b), w, h, d)


def bg_londres():
    d = (lg("bl_c", (0, "#1a1440"), (0.55, "#c8506a"), (1, "#ffb070")) + lg("bl_r", (0, "#3a2a50"), (1, "#0a0a1a")))
    b = ['<rect width="1080" height="1920" fill="url(#bl_c)"/>', _estrellas_ricas(11, 200, 20, 4, banda=None).replace("1920", "800") if False else "",
         '<circle cx="760" cy="980" r="120" fill="#ffd27a" opacity="0.8" filter="url(#blur20)"/>']
    sil = "#1a1028"
    # puente levadizo de dos torres (silueta) y edificios
    for x in (300, 780):
        b.append(f'<rect x="{x-60}" y="820" width="120" height="560" fill="{sil}"/><path d="M{x-70} 830 L{x} 700 L{x+70} 830 Z" fill="{sil}"/>'
                 + "".join(f'<path d="M{x+dx} 760 l0 -50" stroke="{sil}" stroke-width="10"/>' for dx in (-50, 50)))
    b.append(f'<rect x="360" y="880" width="360" height="40" fill="{sil}"/><rect x="0" y="1180" width="1080" height="50" fill="{sil}"/>')
    b.append(f'<path d="M0 1180 C120 1080 200 1060 240 1080 L240 1180 Z M840 1080 C900 1060 980 1080 1080 1160 L1080 1180 L840 1180 Z" fill="{sil}"/>')
    r = random.Random(8)
    for x in range(0, 1080, 60):
        hh = r.uniform(60, 220)
        b.append(f'<rect x="{x}" y="{1180-hh:.0f}" width="56" height="{hh:.0f}" fill="#24183a" opacity="0.8"/>')
    b.append('<rect x="0" y="1230" width="1080" height="690" fill="url(#bl_r)"/>')
    for _ in range(40):
        y = r.uniform(1240, 1700)
        b.append(f'<path d="M{r.uniform(0, 1000):.0f} {y:.0f} l{r.uniform(40, 120):.0f} 0" stroke="#ffb070" stroke-width="4" opacity="{r.uniform(0.2, 0.5):.2f}"/>')
    b.append(grano())
    guardar("bg_londres", "".join(b), defs=d)


def bg_salon():
    d = lg("bs_p", (0, "#3a2a3a"), (1, "#1a1220")) + lg("bs_s", (0, "#6a3a48"), (1, "#3a1a28")) + rg("bs_l", (0, "#ffd27a", 0.7), (1, "#ffd27a", 0))
    b = ['<rect width="1080" height="1920" fill="url(#bs_p)"/>',
         '<rect x="120" y="300" width="380" height="520" rx="10" fill="#0a1a3a"/><rect x="120" y="300" width="380" height="520" rx="10" fill="none" stroke="#5a4a5a" stroke-width="18"/>',
         '<path d="M310 300 L310 820 M120 560 L500 560" stroke="#5a4a5a" stroke-width="12"/>',
         '<circle cx="230" cy="400" r="24" fill="#fff8e0" opacity="0.8"/>',
         '<ellipse cx="860" cy="620" rx="380" ry="380" fill="url(#bs_l)"/>',
         '<path d="M800 520 L920 520 L960 640 L760 640 Z" fill="#e8b860"/><rect x="852" y="640" width="16" height="560" fill="#2a1a20"/>',
         '<rect x="0" y="1380" width="1080" height="540" fill="#2a1a20"/>',
         '<path d="M40 1100 C40 1040 90 1020 140 1020 L940 1020 C990 1020 1040 1040 1040 1100 L1040 1420 L40 1420 Z" fill="url(#bs_s)"/>',
         '<rect x="80" y="1180" width="920" height="200" rx="40" fill="#7a4a58"/>', grano()]
    guardar("bg_salon", "".join(b), defs=d)


def gotas_frio():
    w, h = 300, 300
    b = [f'<path d="M150 20 L150 280 M30 150 L270 150 M60 60 L240 240 M240 60 L60 240" stroke="#bfe9ff" stroke-width="12" stroke-linecap="round"/>',
         '<circle cx="150" cy="150" r="30" fill="#ffffff"/>']
    guardar("copo", "".join(b), w, h)


def generar(dirsvg):
    ilus_tarde.generar(dirsvg)     # también trae las del lote 2026-11-17-manana
    ilus.OUT = dirsvg
    for rz in RAZAS:
        perro(rz)
    perrito("perrito", False); perrito("perrito_b", True)
    perrito("perrito2", False, "#8a8a92", "#d8e8ff"); perrito("perrito2_b", True, "#8a8a92", "#d8e8ff")
    silueta("sil", False); silueta("sil_b", True)
    silueta("sil_m", False, "#3a1a38", "#ff7ad8"); silueta("sil_m_b", True, "#3a1a38", "#ff7ad8")
    silueta("sil_a", False, "#1a2a18", "#b6ff5a"); silueta("sil_a_b", True, "#1a2a18", "#b6ff5a")
    bg_vagon(); libro(); bocadillo(); movil_mano(); cerebro(); ventilador()
    bolsa("bolsa_hielo", "#7ac8ff", "#2a6ab0", True); bolsa("bolsa_templada", "#ffb070", "#c8502a", False)
    ecografia(); bg_londres(); bg_salon(); gotas_frio()
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
