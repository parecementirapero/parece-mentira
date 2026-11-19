"""Ilustraciones de «Este niño cambia el clima» (El Niño), vídeo extra 2026-11-19 (Nico, chat).
Uso: python3 ilus_nino.py DIR_SVG   (semillas fijas). Ladrillos de motor/biblioteca/ilus.py.
Reutiliza piezas de lotes/2026-11-17-tarde (nubes, rayos, termómetro, gotas, canguro) y 2026-11-18-tarde (hoja de calendario)."""
import importlib.util, math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano  # noqa: E402


def _mod(alias, ruta):
    sys.path.insert(0, os.path.dirname(ruta))
    s = importlib.util.spec_from_file_location(alias, ruta)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _p(pts, cerrar=True):
    return "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + (" Z" if cerrar else "")


def _costa(r, pts, amp=14, sub=4):
    """Línea de costa irregular a partir de unos vértices."""
    out = []
    for i in range(len(pts)):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
        for k in range(sub):
            u = k / sub
            out.append((x0 + (x1 - x0) * u + r.uniform(-amp, amp), y0 + (y1 - y0) * u + r.uniform(-amp, amp)))
    return out


# ------------------------------------------------------------------ mapa del Pacífico (Asia y Australia a la izquierda, América a la derecha)
ASIA = [(-40, 250), (150, 240), (250, 330), (230, 470), (290, 560), (210, 640), (240, 760), (150, 800), (90, 720), (-40, 740)]
AUSTRALIA = [(60, 1180), (170, 1130), (290, 1160), (330, 1270), (270, 1380), (150, 1400), (50, 1340)]
NORTEAMERICA = [(1120, 220), (900, 240), (800, 330), (770, 470), (830, 600), (900, 690), (960, 760), (1000, 840), (1120, 860)]
SUDAMERICA = [(1120, 860), (1000, 850), (930, 900), (900, 1000), (930, 1110), (990, 1200), (1010, 1340), (1030, 1500), (1070, 1640), (1120, 1660)]
ISLAS = [(250, 900, 60, 22), (330, 960, 44, 18), (190, 980, 50, 16), (380, 1030, 30, 12), (300, 1060, 36, 12)]


def bg_pacifico():
    r = random.Random(5)
    d = (lg("pa_mar", (0, "#06142e"), (0.45, "#0c3a5e"), (0.55, "#0e4a6a"), (1, "#05122a")) +
         rg("pa_luz", (0, "#3fb8d8", 0.35), (1, "#3fb8d8", 0)) + lg("pa_tierra", (0, "#4a6a4a"), (1, "#2a3a2e")))
    b = ['<rect width="1080" height="1920" fill="url(#pa_mar)"/>', '<ellipse cx="540" cy="960" rx="620" ry="760" fill="url(#pa_luz)"/>']
    for y in range(160, 1900, 160):  # paralelos y meridianos tenues
        b.append(f'<path d="M0 {y} L1080 {y}" stroke="#8fd8ff" stroke-width="2" opacity="0.08"/>')
    for x in range(108, 1080, 108):
        b.append(f'<path d="M{x} 0 L{x} 1920" stroke="#8fd8ff" stroke-width="2" opacity="0.06"/>')
    for k in range(70):  # oleaje fino
        x, y, w = r.uniform(0, 1080), r.uniform(100, 1850), r.uniform(20, 70)
        b.append(f'<path d="M{x:.0f} {y:.0f} q{w/2:.0f} -8 {w:.0f} 0" stroke="#bfeaff" stroke-width="3" fill="none" opacity="{r.uniform(0.06,0.2):.2f}"/>')
    b.append('<path d="M0 960 L1080 960" stroke="#ffffff" stroke-width="4" stroke-dasharray="18 16" opacity="0.35"/>')
    for forma in (ASIA, AUSTRALIA, NORTEAMERICA, SUDAMERICA):
        c = _costa(r, forma, 12, 5)
        b.append(f'<path d="{_p(c)}" fill="#0a2030" opacity="0.6" transform="translate(10 16)"/>')
        b.append(f'<path d="{_p(c)}" fill="url(#pa_tierra)" stroke="#d8e8b0" stroke-width="5" stroke-linejoin="round"/>')
    for x, y, rx, ry in ISLAS:
        b.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#3a5a40" stroke="#d8e8b0" stroke-width="4"/>')
    for cx, cy in [(120, 480), (940, 420), (1020, 1180), (180, 1270)]:  # relieve
        for k in range(5):
            x, y = cx + r.uniform(-60, 60), cy + r.uniform(-80, 80)
            b.append(f'<path d="M{x-16:.0f} {y+10:.0f} L{x:.0f} {y-14:.0f} L{x+16:.0f} {y+10:.0f}" fill="#6a8a5a" opacity="0.7"/>')
    b.append(grano())
    guardar("bg_pacifico", "".join(b), defs=d)


def mancha(nombre, nucleo, medio, borde):
    """Mancha de agua (caliente o fría) alargada, con remolinos."""
    w, h = 1000, 460
    r = random.Random(len(nombre))
    d = rg(f"{nombre}_g", (0, nucleo, 0.95), (0.45, medio, 0.8), (1, borde, 0))
    b = [f'<ellipse cx="500" cy="230" rx="490" ry="220" fill="url(#{nombre}_g)"/>',
         f'<ellipse cx="500" cy="230" rx="300" ry="110" fill="{nucleo}" opacity="0.55" filter="url(#blur20)"/>']
    for k in range(9):
        x, y, s = r.uniform(180, 820), r.uniform(150, 310), r.uniform(26, 60)
        b.append(f'<path d="M{x-s:.0f} {y:.0f} q{s/2:.0f} {-s*0.5:.0f} {s:.0f} 0 t{s:.0f} 0" stroke="#ffffff" stroke-width="5" fill="none" opacity="0.35" stroke-linecap="round"/>')
    guardar(nombre, "".join(b), w, h, d)


# ------------------------------------------------------------------ la Tierra vista desde el Pacífico, con la franja caliente
def tierra_nino(nombre="tierra_nino", franja=True):
    w = h = 1000
    r = random.Random(9)
    d = (rg("tn_mar", (0, "#2a8ac8", 1), (0.7, "#0e4a8a", 1), (1, "#06203e", 1), cx=0.38, cy=0.34, r=0.75) +
         rg("tn_som", (0, "#000000", 0), (0.72, "#000000", 0), (1, "#000010", 0.75), cx=0.36, cy=0.32, r=0.8) +
         rg("tn_atm", (0.86, "#7fd0ff", 0), (0.95, "#7fd0ff", 0.55), (1, "#7fd0ff", 0)) +
         lg("tn_fr", (0, "#ffd23f"), (0.5, "#ff7a1e"), (1, "#e0302a"), x2=1, y2=0) +
         '<clipPath id="tn_c"><circle cx="500" cy="500" r="440"/></clipPath>')
    b = ['<circle cx="500" cy="500" r="490" fill="url(#tn_atm)"/>', '<circle cx="500" cy="500" r="440" fill="url(#tn_mar)"/>', '<g clip-path="url(#tn_c)">']
    esc = lambda pts, sx, sy, ox, oy: [(x * sx + ox, y * sy + oy) for x, y in pts]  # noqa: E731
    for forma, col in ((esc(ASIA, 0.62, 0.5, 20, 110), "#4f8a4a"), (esc(AUSTRALIA, 0.62, 0.5, 50, 150), "#b8935a"),
                       (esc(NORTEAMERICA, 0.62, 0.5, 250, 110), "#5a8a4a"), (esc(SUDAMERICA, 0.62, 0.5, 250, 110), "#4a8a44")):
        c = _costa(r, forma, 7, 5)
        b.append(f'<path d="{_p(c)}" fill="{col}" stroke="#dff0c0" stroke-width="3" opacity="0.95"/>')
    if franja:  # lengua de agua caliente pegada a América, sobre el ecuador
        b.append('<path d="M250 560 Q420 500 600 520 Q760 520 840 560 Q760 640 600 630 Q420 650 250 560 Z" fill="url(#tn_fr)" opacity="0.92" filter="url(#blur8)"/>')
        b.append('<path d="M330 566 Q480 530 620 545 Q740 548 800 566 Q740 606 620 600 Q480 612 330 566 Z" fill="#fff0a0" opacity="0.55" filter="url(#blur8)"/>')
    for k in range(16):  # nubes
        x, y = r.uniform(120, 880), r.uniform(120, 880)
        if franja and 480 < y < 660: y += 180
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(50,130):.0f}" ry="{r.uniform(14,34):.0f}" fill="#ffffff" opacity="{r.uniform(0.35,0.75):.2f}" filter="url(#blur8)" transform="rotate({r.uniform(-25,25):.0f} {x:.0f} {y:.0f})"/>')
    b.append('</g><circle cx="500" cy="500" r="440" fill="url(#tn_som)"/>')
    b.append('<ellipse cx="350" cy="300" rx="150" ry="90" fill="#ffffff" opacity="0.16" filter="url(#blur20)"/>')
    guardar(nombre, "".join(b), w, h, d)


# ------------------------------------------------------------------ mar del norte de Perú (frío / tibio) y fondo submarino
def bg_mar_peru(nombre, tibio=False):
    r = random.Random(13 + tibio)
    cielo = [(0, "#ffb070"), (0.3, "#ffd8a0"), (0.46, "#fff0d0")] if tibio else [(0, "#3a5a8a"), (0.3, "#8ab0d0"), (0.46, "#e8e0c8")]
    mar = [(0, "#ff9a6a"), (0.2, "#c8785a"), (0.6, "#7a5a6a"), (1, "#2a1c34")] if tibio else [(0, "#5ab0c8"), (0.2, "#2a7a9a"), (0.6, "#0e4a6e"), (1, "#041a30")]
    d = lg(f"{nombre}_c", *cielo) + lg(f"{nombre}_m", *mar) + rg(f"{nombre}_s", (0, "#fffbe0", 1), (0.25, "#ffe08a", 0.7), (1, "#ffb040", 0))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>',
         f'<circle cx="{760 if tibio else 300}" cy="{700 if tibio else 640}" r="{330 if tibio else 240}" fill="url(#{nombre}_s)"/>']
    for k in range(6):  # nubes altas
        x, y = r.uniform(0, 1080), r.uniform(200, 620)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(120,260):.0f}" ry="{r.uniform(18,40):.0f}" fill="#ffffff" opacity="{r.uniform(0.25,0.5):.2f}" filter="url(#blur8)"/>')
    # costa desértica lejana con cerros
    col_l, col_c = ("#c89a7a", "#8a5a4a") if tibio else ("#a8a0a0", "#5a5a6a")
    b.append(f'<path d="M560 900 L640 800 L720 850 L800 740 L900 820 L980 760 L1080 800 L1080 900 Z" fill="{col_l}" opacity="0.8"/>')
    b.append(f'<path d="M700 905 L780 850 L860 880 L960 830 L1080 870 L1080 905 Z" fill="{col_c}"/>')
    b.append(f'<rect x="0" y="895" width="1080" height="1030" fill="url(#{nombre}_m)"/>')
    for k in range(90):  # brillos y crestas
        y = r.uniform(905, 1900); u = (y - 900) / 1000
        w = 20 + u * 150 * r.uniform(0.4, 1); x = r.uniform(-40, 1080)
        b.append(f'<path d="M{x:.0f} {y:.0f} q{w/4:.0f} {-6-u*10:.0f} {w/2:.0f} 0 t{w/2:.0f} 0" stroke="{"#ffe8c0" if tibio else "#d8f4ff"}" stroke-width="{2+u*5:.1f}" fill="none" opacity="{r.uniform(0.15,0.5):.2f}" stroke-linecap="round"/>')
    b.append('<rect x="0" y="1500" width="1080" height="420" fill="#000814" opacity="0.35" filter="url(#blur40)"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def bg_submarino(nombre, tibio=False):
    r = random.Random(31 + tibio)
    agua = [(0, "#ffb86a"), (0.25, "#c87a6a"), (0.7, "#5a3a5a"), (1, "#1a1024")] if tibio else [(0, "#6ad8e8"), (0.25, "#1e8ab0"), (0.7, "#0a3a6a"), (1, "#020e22")]
    d = lg(f"{nombre}_a", *agua) + lg(f"{nombre}_r", (0, "#ffffff"), (1, "#ffffff00")) + lg(f"{nombre}_f", (0, "#3a4a5a" if not tibio else "#5a4050"), (1, "#0a0c14"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_a)"/>']
    for k in range(7):  # rayos de luz
        x = 80 + k * 150 + r.uniform(-30, 30)
        b.append(f'<path d="M{x:.0f} -20 L{x+90:.0f} -20 L{x+260+r.uniform(-40,40):.0f} 1500 L{x+60:.0f} 1500 Z" fill="url(#{nombre}_r)" opacity="{r.uniform(0.08,0.2):.2f}"/>')
    for k in range(3):  # relieve del fondo por capas
        y0 = 1480 + k * 130
        pts = [(-20, 1940)] + [(x, y0 + r.uniform(-50, 50)) for x in range(-20, 1120, 90)] + [(1100, 1940)]
        b.append(f'<path d="{_p(pts)}" fill="url(#{nombre}_f)" opacity="{0.5 + k*0.25:.2f}"/>')
    for k in range(14):  # algas
        x = r.uniform(20, 1060); hgt = r.uniform(120, 320)
        b.append(f'<path d="M{x:.0f} 1900 q{r.uniform(-50,50):.0f} {-hgt/2:.0f} 0 {-hgt:.0f}" stroke="{"#6a5a3a" if tibio else "#2a8a6a"}" stroke-width="{r.uniform(10,22):.0f}" fill="none" stroke-linecap="round" opacity="0.8"/>')
    for k in range(40):  # burbujas
        x, y, s = r.uniform(0, 1080), r.uniform(200, 1800), r.uniform(4, 16)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s:.0f}" fill="none" stroke="#ffffff" stroke-width="3" opacity="{r.uniform(0.15,0.45):.2f}"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


# ------------------------------------------------------------------ peces (anchoveta) y banco
def _pez(x, y, L, c_lomo="#2a5a8a", c_panza="#e8f0f4", rot=0, op=1.0, uid="p"):
    H2 = L * 0.2
    cuerpo = (f'M{-L/2:.0f} 0 Q{-L*0.25:.0f} {-H2:.0f} {L*0.15:.0f} {-H2*0.8:.0f} Q{L*0.4:.0f} {-H2*0.4:.0f} {L*0.42:.0f} 0 '
              f'Q{L*0.4:.0f} {H2*0.5:.0f} {L*0.15:.0f} {H2*0.9:.0f} Q{-L*0.25:.0f} {H2:.0f} {-L/2:.0f} 0 Z')
    cola = f'M{L*0.38:.0f} 0 L{L*0.56:.0f} {-H2*0.95:.0f} L{L*0.5:.0f} 0 L{L*0.56:.0f} {H2*0.95:.0f} Z'
    g = [f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot:.0f})" opacity="{op}">',
         f'<path d="{cola}" fill="{c_lomo}"/>', f'<path d="{cuerpo}" fill="url(#{uid}_g)"/>',
         f'<path d="M{-L*0.3:.0f} {-H2*0.72:.0f} Q0 {-H2*1.25:.0f} {L*0.12:.0f} {-H2*0.8:.0f}" fill="{c_lomo}"/>',
         f'<path d="M{-L*0.12:.0f} {H2*0.5:.0f} l{L*0.1:.0f} {H2*0.45:.0f} l{-L*0.02:.0f} {-H2*0.5:.0f}" fill="{c_lomo}" opacity="0.8"/>',
         f'<path d="M{-L*0.3:.0f} 0 Q0 {-H2*0.2:.0f} {L*0.36:.0f} 0" stroke="#ffffff" stroke-width="{max(1.5, L*0.012):.1f}" fill="none" opacity="0.6"/>',
         f'<path d="M{-L*0.33:.0f} {-H2*0.5:.0f} Q{-L*0.28:.0f} 0 {-L*0.33:.0f} {H2*0.5:.0f}" stroke="{c_lomo}" stroke-width="{max(1.5, L*0.012):.1f}" fill="none"/>',
         f'<circle cx="{-L*0.4:.0f}" cy="{-H2*0.15:.0f}" r="{L*0.035:.1f}" fill="#fff8d0"/><circle cx="{-L*0.4:.0f}" cy="{-H2*0.15:.0f}" r="{L*0.018:.1f}" fill="#0a0c14"/>',
         '</g>']
    return "".join(g)


def _pez_defs(uid="p", lomo="#2a5a8a", panza="#e8f0f4"):
    return lg(f"{uid}_g", (0, lomo), (0.42, "#9ac0d8"), (0.6, panza), (1, "#b8c8d0"))


def pez():
    b = ['<ellipse cx="320" cy="250" rx="230" ry="14" fill="#000" opacity="0.25" filter="url(#blur8)"/>', _pez(320, 140, 520)]
    for k in range(9):
        b.append(f'<path d="M{170+k*34} 118 q10 22 0 44" stroke="#5a8ab0" stroke-width="3" fill="none" opacity="0.5"/>')
    guardar("pez", "".join(b), 640, 280, _pez_defs())


def banco(nombre="banco", n=26, sem=4):
    r = random.Random(sem)
    b = []
    for k in range(n):
        u = k / n
        x, y = 120 + r.uniform(0, 860), 90 + r.uniform(0, 520)
        L = r.uniform(110, 200) * (0.7 + 0.5 * (y / 700))
        b.append((y, _pez(x, y, L, rot=r.uniform(-8, 8), op=round(0.55 + 0.45 * (y / 700), 2))))
    guardar(nombre, "".join(s for _, s in sorted(b)), 1100, 700, _pez_defs())


# ------------------------------------------------------------------ barca de pescadores del norte de Perú, red y viento
def barca(nombre="barca", red_llena=True):
    w, h = 1000, 900
    r = random.Random(3)
    d = (lg("ba_c", (0, "#e8e0d0"), (0.5, "#c8b8a0"), (1, "#7a6a5a")) + lg("ba_v", (0, "#f8f0dc"), (1, "#c8b890")) +
         lg("ba_f", (0, "#2a8ac8"), (1, "#14507a")) + _pez_defs("bp"))
    b = ['<ellipse cx="500" cy="840" rx="430" ry="26" fill="#001020" opacity="0.4" filter="url(#blur8)"/>']
    # mástil, vela recogida a medias y cabos
    b.append('<rect x="486" y="90" width="20" height="560" fill="#5a3a22"/><rect x="486" y="90" width="7" height="560" fill="#8a6a4a"/>')
    b.append('<path d="M506 120 L800 520 L506 560 Z" fill="url(#ba_v)" stroke="#8a7a5a" stroke-width="4"/>')
    for k in range(5):
        y = 200 + k * 70
        b.append(f'<path d="M506 {y} L{506 + (y-120)*0.66:.0f} {y+ (y-120)*0.09:.0f}" stroke="#a89878" stroke-width="3" opacity="0.6"/>')
    b.append('<path d="M496 100 L150 640 M496 100 L880 640" stroke="#3a2a1a" stroke-width="4" fill="none"/>')
    b.append('<path d="M506 92 l70 22 l-70 22 Z" fill="#e0302a"/>')
    # casco de madera con franjas de color
    casco = "M70 620 Q500 700 930 610 L850 800 Q500 850 150 800 Z"
    b.append(f'<path d="{casco}" fill="url(#ba_c)" stroke="#3a2a1a" stroke-width="6" stroke-linejoin="round"/>')
    b.append('<path d="M84 650 Q500 730 916 640 L900 680 Q500 765 100 690 Z" fill="url(#ba_f)"/>')
    b.append('<path d="M112 716 Q500 790 890 706 L882 728 Q500 810 122 738 Z" fill="#e0302a"/>')
    for x in range(180, 860, 62):
        b.append(f'<path d="M{x} {742 + abs(x-500)*-0.06:.0f} l-6 60" stroke="#5a4a3a" stroke-width="3" opacity="0.5"/>')
    b.append('<path d="M70 620 Q500 700 930 610" stroke="#fff8e0" stroke-width="5" fill="none" opacity="0.7"/>')
    # dos pescadores de espaldas (sin cara): sombrero, poncho, brazos tirando de la red
    for x, s, col in [(330, 1.0, "#b0463a"), (640, 0.92, "#3a6a8a")]:
        b.append(f'<g transform="translate({x} 640) scale({s})">'
                 f'<path d="M-52 0 Q-60 -110 0 -128 Q60 -110 52 0 Z" fill="{col}"/>'
                 f'<path d="M-30 -20 Q0 -40 30 -20 M-36 -60 Q0 -80 36 -60" stroke="#ffe0a0" stroke-width="5" fill="none" opacity="0.7"/>'
                 '<circle cx="0" cy="-150" r="30" fill="#8a5a3a"/>'
                 '<ellipse cx="0" cy="-170" rx="64" ry="16" fill="#e8d09a"/><path d="M-34 -172 Q0 -226 34 -172 Z" fill="#d8bc7a"/>'
                 '<path d="M-34 -176 Q0 -186 34 -176" stroke="#b0463a" stroke-width="6" fill="none"/>'
                 f'<path d="M40 -90 Q90 -70 110 -20" stroke="{col}" stroke-width="24" fill="none" stroke-linecap="round"/>'
                 '<circle cx="112" cy="-16" r="13" fill="#8a5a3a"/></g>')
    # red colgando por la borda
    red = ['<g transform="translate(470 630)">']
    for k in range(9):
        red.append(f'<path d="M{k*24} 0 Q{k*24-30} 90 {k*20+10} 170" stroke="#e8d8b0" stroke-width="3" fill="none" opacity="0.85"/>')
    for k in range(6):
        red.append(f'<path d="M{-6-k*5} {k*30} Q100 {k*30+18} {196-k*3} {k*30}" stroke="#e8d8b0" stroke-width="3" fill="none" opacity="0.85"/>')
    red.append('</g>')
    b.append("".join(red))
    if red_llena:
        for k in range(7):
            b.append(_pez(500 + r.uniform(0, 150), 690 + r.uniform(0, 90), r.uniform(70, 100), rot=r.uniform(40, 130), uid="bp"))
    guardar(nombre, "".join(b), w, h, d)


def viento(nombre="viento", color="#ffffff"):
    w, h = 900, 360
    b = []
    for k, (y, L, c) in enumerate([(70, 760, 70), (170, 640, 54), (280, 720, 62)]):
        x0 = 40 + k * 30
        cam = f'M{x0} {y} L{x0+L-c:.0f} {y} q{c} 0 {c} {-c*0.6:.0f} q0 {-c*0.5:.0f} {-c*0.55:.0f} {-c*0.5:.0f} q{-c*0.4:.0f} 0 {-c*0.4:.0f} {c*0.32:.0f}'
        b.append(f'<path d="{cam}" stroke="{color}" stroke-width="20" fill="none" stroke-linecap="round" opacity="0.25" filter="url(#blur8)"/>')
        b.append(f'<path d="{cam}" stroke="{color}" stroke-width="11" fill="none" stroke-linecap="round" opacity="0.92"/>')
    guardar(nombre, "".join(b), w, h)


# ------------------------------------------------------------------ Navidad: estrella y pesebre (sin figura: un fardo con luz)
def estrella_navidad():
    w, h = 700, 1000
    d = rg("en_g", (0, "#fffbe0", 1), (0.3, "#ffe08a", 0.6), (1, "#ffb040", 0)) + lg("en_c", (0, "#fff6c0"), (1, "#fff6c000"))
    b = ['<circle cx="350" cy="300" r="290" fill="url(#en_g)"/>', '<path d="M330 300 L370 300 L356 980 L344 980 Z" fill="url(#en_c)" opacity="0.8"/>']
    pts = []
    for k in range(16):
        a = math.pi * k / 8 - math.pi / 2
        rad = [250, 46, 110, 46][k % 4]
        pts.append((350 + rad * math.cos(a), 300 + rad * math.sin(a)))
    b.append(f'<path d="{_p(pts)}" fill="#fff2a8" stroke="#ffffff" stroke-width="5" stroke-linejoin="round"/>')
    b.append('<circle cx="350" cy="300" r="34" fill="#ffffff"/>')
    guardar("estrella_navidad", "".join(b), w, h, d)


def pesebre():
    w, h = 900, 760
    r = random.Random(8)
    d = (lg("pe_m", (0, "#a87a4a"), (1, "#4a2e1a")) + rg("pe_l", (0, "#fff6c8", 0.95), (0.5, "#ffd27a", 0.45), (1, "#ffb040", 0)) +
         lg("pe_t", (0, "#fffaf0"), (1, "#c8c0b0")))
    b = ['<ellipse cx="450" cy="700" rx="380" ry="28" fill="#000" opacity="0.45" filter="url(#blur8)"/>', '<circle cx="450" cy="330" r="330" fill="url(#pe_l)"/>']
    for x0, x1 in [(170, 300), (730, 600), (300, 170), (600, 730)]:
        b.append(f'<path d="M{x0} 700 L{x1} 430" stroke="url(#pe_m)" stroke-width="42" stroke-linecap="round"/>')
        b.append(f'<path d="M{x0-8} 700 L{x1-8} 430" stroke="#d8a870" stroke-width="8" stroke-linecap="round" opacity="0.6"/>')
    b.append('<path d="M150 440 L750 440 L690 580 L210 580 Z" fill="url(#pe_m)" stroke="#2a1a0e" stroke-width="6" stroke-linejoin="round"/>')
    for x in range(230, 700, 70):
        b.append(f'<path d="M{x} 450 l-10 122" stroke="#2a1a0e" stroke-width="4" opacity="0.5"/>')
    for k in range(80):  # paja
        x = r.uniform(150, 750); a = r.uniform(-1.2, 1.2); L = r.uniform(40, 110)
        b.append(f'<path d="M{x:.0f} 446 l{L*math.sin(a):.0f} {-L*abs(math.cos(a))*0.6:.0f}" stroke="{r.choice(["#ffe08a", "#e8c060", "#fff0b0", "#c8a040"])}" stroke-width="{r.uniform(3,6):.0f}" stroke-linecap="round"/>')
    # fardo de tela envuelto (no se dibuja ninguna cara)
    b.append('<path d="M250 420 Q300 300 450 290 Q610 300 650 420 Q450 470 250 420 Z" fill="url(#pe_t)" stroke="#a8a090" stroke-width="5"/>')
    for k in range(5):
        b.append(f'<path d="M{290+k*70} {400-k%2*10} Q{330+k*70} {330} {370+k*70} {410-k%2*8}" stroke="#b8b0a0" stroke-width="5" fill="none" opacity="0.8"/>')
    b.append('<ellipse cx="450" cy="250" rx="150" ry="34" fill="none" stroke="#fff2a8" stroke-width="10" opacity="0.9"/>')
    b.append('<ellipse cx="450" cy="250" rx="150" ry="34" fill="none" stroke="#fff2a8" stroke-width="26" opacity="0.3" filter="url(#blur8)"/>')
    guardar("pesebre", "".join(b), w, h, d)


# ------------------------------------------------------------------ desierto de Perú (seco) y lluvia; sequía en Australia
def bg_desierto():
    r = random.Random(17)
    d = (lg("de_c", (0, "#3a4a6a"), (0.4, "#8a8a9a"), (0.62, "#d8c0a0")) + lg("de_d1", (0, "#e8c890"), (1, "#a87a4a")) +
         lg("de_d2", (0, "#c89a5a"), (1, "#6a4426")) + lg("de_d3", (0, "#8a5e34"), (1, "#2a1a10")))
    b = ['<rect width="1080" height="1920" fill="url(#de_c)"/>']
    b.append('<path d="M0 1120 L140 1010 L300 1080 L460 960 L640 1070 L820 990 L1080 1090 L1080 1300 L0 1300 Z" fill="#9a8a8a" opacity="0.7"/>')
    b.append('<path d="M-20 1260 Q200 1120 480 1230 Q760 1330 1100 1180 L1100 1940 L-20 1940 Z" fill="url(#de_d1)"/>')
    b.append('<path d="M-20 1470 Q260 1330 560 1450 Q820 1550 1100 1420 L1100 1940 L-20 1940 Z" fill="url(#de_d2)"/>')
    b.append('<path d="M-20 1720 Q300 1600 640 1700 Q900 1780 1100 1690 L1100 1940 L-20 1940 Z" fill="url(#de_d3)"/>')
    for k in range(60):  # ondas del viento en la arena
        x, y = r.uniform(0, 1080), r.uniform(1280, 1900)
        b.append(f'<path d="M{x:.0f} {y:.0f} q30 -8 60 0" stroke="#fff0c8" stroke-width="3" fill="none" opacity="{r.uniform(0.1,0.3):.2f}"/>')
    for x, y, s in [(190, 1450, 1.0), (880, 1400, 0.8), (700, 1690, 1.3)]:  # algarrobos secos
        b.append(f'<g transform="translate({x} {y}) scale({s})"><path d="M0 0 L-4 -120 M-4 -70 L-50 -130 M-4 -90 L44 -150 M-4 -120 L-20 -180 M-4 -120 L20 -190" stroke="#3a2a1a" stroke-width="10" fill="none" stroke-linecap="round"/>'
                 '<ellipse cx="0" cy="6" rx="60" ry="10" fill="#000" opacity="0.3"/></g>')
    b.append(grano())
    guardar("bg_desierto", "".join(b), defs=d)


def lluvia(nombre="lluvia", sem=5, n=170):
    r = random.Random(sem)
    b = []
    for k in range(n):
        x, y, L = r.uniform(-100, 1180), r.uniform(-100, 2300), r.uniform(50, 130)
        b.append(f'<path d="M{x:.0f} {y:.0f} l{-L*0.22:.0f} {L:.0f}" stroke="#d8f0ff" stroke-width="{r.uniform(3,6):.0f}" stroke-linecap="round" opacity="{r.uniform(0.35,0.85):.2f}"/>')
    guardar(nombre, "".join(b), 1080, 2300)


def riada():
    """Agua marrón que sube (inundación) con crestas."""
    r = random.Random(23)
    d = lg("ri_g", (0, "#a8845a"), (0.3, "#7a5a3a"), (1, "#3a2a1c"))
    pts = [(-20, 1000)] + [(x, 70 + 30 * math.sin(x / 90) + r.uniform(-12, 12)) for x in range(-20, 1220, 40)] + [(1220, 1000)]
    b = [f'<path d="{_p(pts)}" fill="url(#ri_g)"/>']
    for k in range(50):
        x, y = r.uniform(0, 1200), r.uniform(80, 900)
        b.append(f'<path d="M{x:.0f} {y:.0f} q30 -12 60 0 t60 0" stroke="#e8d0a8" stroke-width="5" fill="none" opacity="{r.uniform(0.2,0.6):.2f}" stroke-linecap="round"/>')
    guardar("riada", "".join(b), 1200, 1000, d)


def bg_sequia():
    r = random.Random(29)
    d = (lg("se_c", (0, "#e0563a"), (0.35, "#ff9a4a"), (0.6, "#ffd88a")) + rg("se_s", (0, "#fffbe0", 1), (0.2, "#fff0a0", 0.9), (1, "#ffb040", 0)) +
         lg("se_t", (0, "#c87a4a"), (1, "#5a2a1a")))
    b = ['<rect width="1080" height="1920" fill="url(#se_c)"/>', '<circle cx="720" cy="620" r="420" fill="url(#se_s)"/>', '<circle cx="720" cy="620" r="120" fill="#fffbe8"/>']
    b.append('<path d="M0 1150 L200 1100 L420 1130 L700 1080 L1080 1120 L1080 1300 L0 1300 Z" fill="#a85a3a" opacity="0.8"/>')
    b.append('<rect x="0" y="1180" width="1080" height="760" fill="url(#se_t)"/>')
    # grietas: red de polígonos irregulares
    nod = {}
    for i in range(9):
        for j in range(8):
            u = j / 7
            nod[i, j] = (i * 150 - 60 + r.uniform(-45, 45) + (j % 2) * 70, 1200 + u ** 1.5 * 720 + r.uniform(-14, 14) * (1 + u * 3))
    for i in range(9):
        for j in range(8):
            for di, dj in ((1, 0), (0, 1)):
                if (i + di, j + dj) in nod and r.random() > 0.12:
                    (x0, y0), (x1, y1) = nod[i, j], nod[i + di, j + dj]
                    g = 3 + (j / 7) * 9
                    b.append(f'<path d="M{x0:.0f} {y0:.0f} L{(x0+x1)/2 + r.uniform(-14,14):.0f} {(y0+y1)/2 + r.uniform(-8,8):.0f} L{x1:.0f} {y1:.0f}" stroke="#2a120a" stroke-width="{g:.1f}" fill="none" stroke-linejoin="round"/>')
                    b.append(f'<path d="M{x0:.0f} {y0+g:.0f} L{x1:.0f} {y1+g:.0f}" stroke="#ffc890" stroke-width="2" fill="none" opacity="0.35"/>')
    # árbol seco
    b.append('<g transform="translate(250 1290)"><path d="M0 0 Q-10 -160 6 -300 M2 -150 Q-70 -210 -120 -330 M4 -210 Q80 -260 130 -380 M6 -300 Q-20 -380 -50 -450 M6 -300 Q50 -380 60 -470 M-80 -260 L-150 -280 M90 -310 L160 -300" stroke="#2a160e" stroke-width="20" fill="none" stroke-linecap="round"/><ellipse cx="60" cy="8" rx="170" ry="16" fill="#1a0a06" opacity="0.5"/></g>')
    b.append(grano())
    guardar("bg_sequia", "".join(b), defs=d)


# ------------------------------------------------------------------ La Niña (copo), y pantalla de los meteorólogos
def copo():
    w = h = 500
    b = ['<circle cx="250" cy="250" r="230" fill="#7fd8ff" opacity="0.18" filter="url(#blur20)"/>']
    for k in range(6):
        b.append(f'<g transform="rotate({k*60} 250 250)"><path d="M250 250 L250 40 M250 110 l-46 -46 M250 110 l46 -46 M250 170 l-34 -34 M250 170 l34 -34" stroke="#eaf8ff" stroke-width="16" stroke-linecap="round" fill="none"/></g>')
    b.append('<circle cx="250" cy="250" r="26" fill="#ffffff"/>')
    guardar("copo", "".join(b), w, h)


def monitor():
    w, h = 1000, 820
    r = random.Random(41)
    d = (lg("mo_p", (0, "#0a1e36"), (1, "#06101e")) + lg("mo_b", (0, "#3a4458"), (1, "#141a26")) + lg("mo_f", (0, "#ffd23f"), (0.5, "#ff7a1e"), (1, "#e0302a"), x2=1, y2=0))
    b = ['<ellipse cx="500" cy="790" rx="330" ry="20" fill="#000" opacity="0.5" filter="url(#blur8)"/>',
         '<path d="M430 640 L570 640 L600 770 L400 770 Z" fill="url(#mo_b)"/><rect x="330" y="760" width="340" height="26" rx="13" fill="#2a3244"/>',
         '<rect x="40" y="30" width="920" height="620" rx="34" fill="url(#mo_b)"/><rect x="70" y="60" width="860" height="560" rx="16" fill="url(#mo_p)"/>']
    for y in range(120, 600, 80):
        b.append(f'<path d="M70 {y} L930 {y}" stroke="#7fd8ff" stroke-width="2" opacity="0.12"/>')
    for x in range(150, 930, 110):
        b.append(f'<path d="M{x} 60 L{x} 620" stroke="#7fd8ff" stroke-width="2" opacity="0.1"/>')
    b.append('<path d="M70 120 L150 110 L190 190 L150 260 L70 250 Z M90 420 L170 400 L200 470 L140 520 L70 500 Z" fill="#3a6a4a" stroke="#d8e8b0" stroke-width="3"/>')
    b.append('<path d="M930 100 L820 120 L790 220 L850 300 L880 420 L900 560 L930 580 Z" fill="#3a6a4a" stroke="#d8e8b0" stroke-width="3"/>')
    b.append('<path d="M330 330 Q520 280 700 300 Q800 310 850 340 Q800 390 700 380 Q520 400 330 330 Z" fill="url(#mo_f)" filter="url(#blur8)"/>')
    b.append('<path d="M420 336 Q560 310 700 322 Q770 328 810 340 Q770 362 700 358 Q560 366 420 336 Z" fill="#fff0a0" opacity="0.7"/>')
    pts = [(110 + k * 52, 560 - (k ** 1.7) * 3.2 + r.uniform(-8, 8)) for k in range(15)]
    b.append(f'<path d="{_p(pts, False)}" stroke="#ff5a3a" stroke-width="8" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
    b.append(f'<circle cx="{pts[-1][0]:.0f}" cy="{pts[-1][1]:.0f}" r="14" fill="#ffd23f"/>')
    b.append('<rect x="70" y="60" width="860" height="560" rx="16" fill="#ffffff" opacity="0.04"/><path d="M70 60 L500 60 L260 620 L70 620 Z" fill="#ffffff" opacity="0.05"/>')
    guardar("monitor", "".join(b), w, h, d)


def boya():
    """Boya oceanográfica con antena (las que miden el Pacífico)."""
    w, h = 500, 800
    d = lg("bo_g", (0, "#ffd23f"), (1, "#c87a14"), x2=1, y2=0)
    b = ['<path d="M250 60 L250 330" stroke="#dfe8ff" stroke-width="10"/><circle cx="250" cy="50" r="22" fill="#ff3d3d"/><circle cx="250" cy="50" r="40" fill="#ff3d3d" opacity="0.3" filter="url(#blur8)"/>',
         '<path d="M180 330 L320 330 L360 520 L140 520 Z" fill="#e8eef8" stroke="#3a4458" stroke-width="6"/><rect x="200" y="370" width="100" height="70" fill="#1a3a5a"/>',
         '<path d="M70 520 L430 520 Q440 640 250 680 Q60 640 70 520 Z" fill="url(#bo_g)" stroke="#3a2a10" stroke-width="6"/>',
         '<path d="M90 560 Q250 600 410 560" stroke="#e0302a" stroke-width="22" fill="none"/>',
         '<path d="M250 680 L250 790" stroke="#3a4458" stroke-width="8" stroke-dasharray="14 10"/>']
    guardar("boya", "".join(b), w, h, d)


def generar(dirsvg):
    t17 = _mod("ilus_tarde_1117", os.path.join(RAIZ, "lotes", "2026-11-17-tarde", "generadores", "ilus_tarde.py"))
    t17.generar(dirsvg)                 # nubes, rayos, termómetro, gotas, canguro, bg_mar_tormenta, bg_cielo_despejado…
    t18 = _mod("ilus_tarde_1118", os.path.join(RAIZ, "lotes", "2026-11-18-tarde", "generadores", "ilus_tarde.py"))
    ilus.OUT = dirsvg
    t18.hoja_calendario("hoja_dic", "DIC", "#e0473a")
    t17.termometro("termo_frio", 0.22, "#3fb8ff"); t17.termometro("termo_tibio", 0.72, "#ff7a1e"); t17.termometro("termo_max", 1.0, "#ff2d55")
    bg_pacifico(); mancha("mancha_caliente", "#fff0a0", "#ff7a1e", "#e0302a"); mancha("mancha_fria", "#eaf8ff", "#3fb8ff", "#1e5ac8")
    tierra_nino(); tierra_nino("tierra_pacifico", False)
    bg_mar_peru("bg_mar_frio"); bg_mar_peru("bg_mar_tibio", True); bg_submarino("bg_sub_frio"); bg_submarino("bg_sub_tibio", True)
    pez(); banco(); banco("banco_b", 14, 9); barca(); barca("barca_vacia", False); viento(); viento("viento_cian", "#7df9ff")
    estrella_navidad(); pesebre(); bg_desierto(); lluvia(); riada(); bg_sequia(); copo(); monitor(); boya()
    return dirsvg


if __name__ == "__main__":
    generar(sys.argv[1])
    print("SVG en", sys.argv[1])
