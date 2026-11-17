"""Ilustraciones del lote 2026-11-17-manana (plátano radiactivo, Saturno flotaría, huellas de koala).
Uso: python3 ilus_lote.py DIR_SVG   (semillas fijas: siempre iguales). Ladrillos de motor/biblioteca/ilus.py."""
import math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano, _hoja, _neb, _mascara, _estrellas_ricas  # noqa: E402,F401


# ====================================================================== 01 · plátano
def platano(nombre="platano", manchas=9, sem=4):
    w, h = 700, 420
    r = random.Random(sem)
    cuerpo = ("M60 150 C40 120 50 95 75 100 C120 170 230 250 380 255 C500 258 590 210 640 140 "
              "C655 120 680 128 672 152 C640 270 520 360 370 360 C220 360 110 270 60 150 Z")
    d = (lg(f"{nombre}_c", (0, "#ffe46a"), (0.45, "#ffd23a"), (1, "#c98a12")) +
         lg(f"{nombre}_l", (0, "#fffbe0"), (0.3, "#fffbe000")) +
         f'<clipPath id="{nombre}_k"><path d="{cuerpo}"/></clipPath>')
    b = [f'<ellipse cx="370" cy="385" rx="270" ry="20" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         f'<path d="{cuerpo}" fill="url(#{nombre}_c)"/>', f'<g clip-path="url(#{nombre}_k)">',
         '<path d="M70 140 C150 240 260 300 380 300 C500 300 600 240 660 150" stroke="#b07a10" stroke-width="5" fill="none" opacity="0.45"/>',
         '<path d="M90 170 C170 255 270 320 380 322" stroke="#fff3a8" stroke-width="10" fill="none" opacity="0.35"/>']
    for _ in range(manchas):
        x, y = r.uniform(140, 600), r.uniform(220, 330)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(5,13):.0f}" ry="{r.uniform(3,8):.0f}" fill="#5a3a0a" opacity="{r.uniform(0.4,0.75):.2f}"/>')
    b += [f'<rect width="{w}" height="{h}" fill="#888" filter="url(#grano)"/>', f'<rect width="{w}" height="{h}" fill="url(#{nombre}_l)" opacity="0.5"/></g>',
          '<path d="M58 152 C40 122 48 96 74 101 L84 118 C70 118 66 132 74 150 Z" fill="#4a3a14"/>',   # rabito
          '<path d="M640 140 C655 120 680 128 672 152 L662 160 C664 145 655 138 640 150 Z" fill="#3a2a0a"/>',
          f'<path d="{cuerpo}" fill="none" stroke="#fff6c0" stroke-width="3" opacity="0.4"/>']
    guardar(nombre, "".join(b), w, h, d)


def racimo():
    w, h = 900, 700
    b = []
    for i, (dx, dy, rot) in enumerate([(-40, 60, -18), (0, 20, -6), (40, -20, 6), (80, -50, 18)]):
        b.append(f'<g transform="translate({120+dx} {150+dy}) rotate({rot} 350 210)"><use href="#pl"/></g>')
    # se resuelve dibujando varios plátanos completos (sin <use> externo): reutilizamos la geometría
    guardar_racimo = []
    cuerpo = ("M60 150 C40 120 50 95 75 100 C120 170 230 250 380 255 C500 258 590 210 640 140 "
              "C655 120 680 128 672 152 C640 270 520 360 370 360 C220 360 110 270 60 150 Z")
    d = lg("rc_c", (0, "#ffe46a"), (0.45, "#ffd23a"), (1, "#b67c10"))
    for i, (dx, dy, rot) in enumerate([(-30, 160, -24), (0, 90, -10), (30, 20, 4), (60, -50, 18)]):
        guardar_racimo.append(f'<g transform="translate({100+dx} {130+dy}) rotate({rot} 350 210)">'
                              f'<path d="{cuerpo}" fill="url(#rc_c)"/><path d="{cuerpo}" fill="none" stroke="#7a5208" stroke-width="4" opacity="0.5"/>'
                              f'<path d="M90 170 C170 255 270 320 380 322" stroke="#fff3a8" stroke-width="9" fill="none" opacity="0.35"/></g>')
    guardar_racimo.append('<path d="M80 250 C60 200 70 120 120 60 L150 70 C110 140 110 200 130 250 Z" fill="#5a4214"/>')
    guardar("racimo", '<ellipse cx="460" cy="660" rx="380" ry="26" fill="#000" opacity="0.35" filter="url(#blur8)"/>' + "".join(guardar_racimo), w, h, d)


def detector():
    """Contador Geiger de mano: caja con dial y aguja aparte (aguja_geiger), sonda con cable."""
    w, h = 620, 760
    d = (lg("dg_caja", (0, "#f2c230"), (0.5, "#e0a91a"), (1, "#9a6c08")) + lg("dg_dial", (0, "#fffbe8"), (1, "#e8dcb4")) +
         lg("dg_sonda", (0, "#cfd6de"), (0.5, "#8a96a4"), (1, "#4a5260")))
    b = ['<ellipse cx="300" cy="735" rx="250" ry="18" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         '<rect x="90" y="300" width="420" height="420" rx="40" fill="url(#dg_caja)"/>',
         '<rect x="90" y="300" width="420" height="420" rx="40" fill="none" stroke="#fff3b0" stroke-width="4" opacity="0.5"/>',
         '<path d="M190 300 C190 220 410 220 410 300" stroke="#2a2a2a" stroke-width="34" fill="none" stroke-linecap="round"/>',
         '<rect x="140" y="350" width="320" height="200" rx="18" fill="#2a2a2a"/>',
         '<rect x="155" y="365" width="290" height="170" rx="12" fill="url(#dg_dial)"/>',
         '<path d="M190 520 A115 115 0 0 1 410 520" stroke="#2a2a2a" stroke-width="4" fill="none"/>',
         '<path d="M330 448 A115 115 0 0 1 410 520" stroke="#e03a2a" stroke-width="10" fill="none"/>',
         *[f'<path d="M{300+115*math.cos(math.radians(a)):.0f} {520-115*math.sin(math.radians(a)):.0f} L{300+95*math.cos(math.radians(a)):.0f} {520-95*math.sin(math.radians(a)):.0f}" stroke="#2a2a2a" stroke-width="4"/>'
           for a in range(170, 9, -20)],
         '<text x="300" y="420" font-family="DejaVu Sans" font-weight="bold" font-size="26" text-anchor="middle" fill="#2a2a2a">µSv/h</text>',
         *[f'<circle cx="{x}" cy="630" r="26" fill="#3a3a3a"/><circle cx="{x}" cy="624" r="22" fill="{c}"/>' for x, c in [(190, "#4a4a4a"), (300, "#e03a2a"), (410, "#4a4a4a")]],
         '<path d="M510 600 C600 600 600 700 560 740" stroke="#1a1a1a" stroke-width="14" fill="none"/>',
         '<rect x="40" y="580" width="60" height="150" rx="14" fill="#555"/>',
         grano(w, h)]
    guardar("detector", "".join(b), w, h, d)
    # aguja (pivote en el centro del SVG: 300,520 → la dibujamos centrada)
    guardar("aguja_geiger", '<path d="M96 100 L100 4 L104 100 Z" fill="#c0261a"/><circle cx="100" cy="100" r="12" fill="#2a2a2a"/>', 200, 200)


def atomo(nombre="atomo", nucleo="#ff7a3a", e="#7df9ff"):
    w = h = 600
    r = random.Random(11)
    d = rg(f"{nombre}_g", (0, "#ffffff", 1), (0.3, nucleo, 1), (1, nucleo, 0)) + rg(f"{nombre}_p", (0, "#ffd0b0", 1), (1, "#c2381a", 1), cx=0.35, cy=0.35)
    b = [f'<circle cx="300" cy="300" r="170" fill="url(#{nombre}_g)" opacity="0.45" filter="url(#blur20)"/>']
    for i in range(16):
        a, rr = r.uniform(0, 6.28), r.uniform(0, 48)
        col = "#ff6a3a" if i % 2 else "#7aa8ff"
        b.append(f'<circle cx="{300+rr*math.cos(a):.0f}" cy="{300+rr*math.sin(a):.0f}" r="26" fill="{col}"/>'
                 f'<circle cx="{292+rr*math.cos(a):.0f}" cy="{292+rr*math.sin(a):.0f}" r="9" fill="#ffffff" opacity="0.45"/>')
    for ang in (0, 60, 120):
        b.append(f'<ellipse cx="300" cy="300" rx="270" ry="90" fill="none" stroke="{e}" stroke-width="4" opacity="0.7" transform="rotate({ang} 300 300)"/>')
    for ang, t in ((0, 0.2), (60, 2.1), (120, 4.0)):
        x, y = 270 * math.cos(t), 90 * math.sin(t)
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        b.append(f'<circle cx="{300+x*ca-y*sa:.0f}" cy="{300+x*sa+y*ca:.0f}" r="14" fill="{e}"/>')
    guardar(nombre, "".join(b), w, h, d)


def chispa():
    w = h = 300
    d = rg("ch_g", (0, "#ffffff", 1), (0.25, "#b6ff5a", 1), (1, "#7dff3a", 0))
    b = ['<circle cx="150" cy="150" r="140" fill="url(#ch_g)"/>'] + \
        [f'<path d="M150 150 L{150+140*math.cos(math.radians(a)):.0f} {150+140*math.sin(math.radians(a)):.0f}" stroke="#eaffc8" stroke-width="{5 if a % 90 == 0 else 2}"/>' for a in range(0, 360, 45)]
    guardar("chispa", "".join(b), w, h, d)


def bg_cocina():
    d = (lg("coc_pared", (0, "#2a1c14"), (0.6, "#5a3a22"), (1, "#3a2414")) + lg("coc_enc", (0, "#d8c6a8"), (1, "#8a7458")) +
         rg("coc_luz", (0, "#ffcf8a", 0.9), (1, "#ffcf8a", 0), cx=0.5, cy=0.3))
    b = ['<rect width="1080" height="1920" fill="url(#coc_pared)"/>',
         *[f'<rect x="{x}" y="{y}" width="176" height="96" fill="none" stroke="#000" stroke-opacity="0.18" stroke-width="3"/>' for x in range(-40, 1100, 180) for y in range(300, 1300, 100)],
         '<ellipse cx="540" cy="500" rx="700" ry="600" fill="url(#coc_luz)" opacity="0.5"/>',
         '<rect x="120" y="180" width="300" height="420" rx="10" fill="#1a3048"/><rect x="135" y="195" width="270" height="390" fill="#6aa0d0" opacity="0.5"/>',
         '<path d="M270 195 L270 585 M135 390 L405 390" stroke="#2a1c14" stroke-width="10"/>',
         '<rect x="0" y="1300" width="1080" height="80" fill="url(#coc_enc)"/>',
         '<rect x="0" y="1380" width="1080" height="540" fill="#3a2a1c"/>',
         *[f'<rect x="{x}" y="1420" width="250" height="460" rx="8" fill="#4a3624" stroke="#2a1c10" stroke-width="4"/><rect x="{x+105}" y="1460" width="40" height="10" rx="5" fill="#c8a878"/>' for x in (20, 290, 560, 830)],
         grano()]
    guardar("bg_cocina", "".join(b), defs=d)


def bg_lab():
    d = lg("lab_f", (0, "#06121a"), (0.6, "#0c2a38"), (1, "#041018")) + rg("lab_l", (0, "#2fd1a6", 0.6), (1, "#2fd1a6", 0))
    b = ['<rect width="1080" height="1920" fill="url(#lab_f)"/>',
         *[f'<path d="M{x} 0 L{x} 1920" stroke="#2ff3ff" stroke-opacity="0.05" stroke-width="2"/>' for x in range(0, 1080, 60)],
         *[f'<path d="M0 {y} L1080 {y}" stroke="#2ff3ff" stroke-opacity="0.05" stroke-width="2"/>' for y in range(0, 1920, 60)],
         '<ellipse cx="540" cy="960" rx="600" ry="700" fill="url(#lab_l)" opacity="0.35"/>',
         '<rect x="0" y="1380" width="1080" height="540" fill="#081820"/><rect x="0" y="1370" width="1080" height="14" fill="#2ff3ff" opacity="0.25"/>',
         grano()]
    guardar("bg_lab", "".join(b), defs=d)


def cuerpo_rayos():
    """Silueta humana translúcida con un esqueleto suave (para «dentro de tu cuerpo»)."""
    w, h = 700, 1500
    d = lg("cu_f", (0, "#3aa0ff"), (1, "#1a3a8a")) + rg("cu_g", (0, "#7df9ff", 0.7), (1, "#7df9ff", 0))
    sil = ("M350 40 C410 40 450 90 450 150 C450 215 410 260 350 260 C290 260 250 215 250 150 C250 90 290 40 350 40 Z "
           "M230 290 C280 270 420 270 470 290 C540 310 580 360 590 440 L630 820 C635 860 600 875 585 840 L530 470 "
           "L520 820 L540 1420 C542 1460 470 1465 465 1425 L370 900 L330 900 L235 1425 C230 1465 158 1460 160 1420 "
           "L180 820 L170 470 L115 840 C100 875 65 860 70 820 L110 440 C120 360 160 310 230 290 Z")
    b = [f'<path d="{sil}" fill="url(#cu_f)" opacity="0.55"/>', f'<path d="{sil}" fill="none" stroke="#7df9ff" stroke-width="5" opacity="0.8"/>',
         '<ellipse cx="350" cy="560" rx="200" ry="300" fill="url(#cu_g)" opacity="0.4"/>',
         '<path d="M350 270 L350 860" stroke="#dff6ff" stroke-width="16" opacity="0.35" stroke-dasharray="22 10"/>',
         *[f'<path d="M350 {380+i*45} C{280-i*4} {370+i*45} {240} {420+i*45} {250} {450+i*45} M350 {380+i*45} C{420+i*4} {370+i*45} 460 {420+i*45} 450 {450+i*45}" stroke="#dff6ff" stroke-width="7" fill="none" opacity="0.3"/>' for i in range(6)],
         '<path d="M270 880 C300 840 400 840 430 880 L420 930 L280 930 Z" fill="#dff6ff" opacity="0.25"/>']
    guardar("cuerpo_rayos", "".join(b), w, h, d)


def escaner():
    w, h = 1000, 800
    d = lg("es_c", (0, "#f4f6fa"), (1, "#b6bec8")) + lg("es_m", (0, "#d8dde4"), (1, "#8a929c"))
    b = ['<ellipse cx="500" cy="770" rx="460" ry="22" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<rect x="60" y="560" width="880" height="60" rx="20" fill="url(#es_m)"/><rect x="380" y="620" width="240" height="140" fill="#9aa2ac"/>',
         '<circle cx="640" cy="420" r="330" fill="url(#es_c)"/><circle cx="640" cy="420" r="330" fill="none" stroke="#ffffff" stroke-width="5" opacity="0.6"/>',
         '<circle cx="640" cy="420" r="175" fill="#1a2230"/><circle cx="640" cy="420" r="175" fill="none" stroke="#2ff3ff" stroke-width="8" opacity="0.8"/>',
         '<rect x="560" y="200" width="160" height="26" rx="13" fill="#2ff3ff" opacity="0.7"/>',
         '<rect x="40" y="520" width="700" height="44" rx="18" fill="#e8ecf2"/>', grano(w, h)]
    guardar("escaner", "".join(b), w, h, d)


def rinon_flecha():
    """Gota que sale (expulsar): un vaso de agua con flecha hacia fuera — simple y legible."""
    w, h = 400, 500
    d = lg("va_g", (0, "#bfe8ff"), (1, "#5ab0e8"))
    b = ['<path d="M80 60 L320 60 L290 460 L110 460 Z" fill="#ffffff" opacity="0.18" stroke="#dff6ff" stroke-width="5"/>',
         '<path d="M95 200 L305 200 L290 460 L110 460 Z" fill="url(#va_g)" opacity="0.75"/>',
         '<path d="M95 200 Q200 180 305 200" stroke="#ffffff" stroke-width="4" fill="none" opacity="0.7"/>']
    guardar("vaso_agua", "".join(b), w, h, d)


# ====================================================================== 02 · Saturno
def saturno(nombre="saturno", ancho=1000):
    w, h = 1000, 640
    cx, cy, R = 500, 320, 200
    d = (lg("sa_p", (0, "#f6e2b0"), (0.25, "#e8c88a"), (0.45, "#d9b070"), (0.6, "#f0d8a0"), (0.8, "#c89a5a"), (1, "#a87a44")) +
         rg("sa_s", (0, "#000", 0), (0.7, "#000", 0.15), (1, "#000", 0.65), cx=0.38, cy=0.35) +
         lg("sa_r", (0, "#c8b48a"), (0.3, "#efe0bc"), (0.5, "#a8946c"), (0.55, "#3a3020"), (0.6, "#d8c8a0"), (1, "#8a7a5a"), x2=1, y2=0) +
         f'<clipPath id="sa_top"><rect x="0" y="0" width="{w}" height="{cy}"/></clipPath>'
         f'<clipPath id="sa_bot"><rect x="0" y="{cy}" width="{w}" height="{h}"/></clipPath>')
    anillo = lambda: (f'<ellipse cx="{cx}" cy="{cy}" rx="470" ry="110" fill="none" stroke="url(#sa_r)" stroke-width="70" opacity="0.92" transform="rotate(-12 {cx} {cy})"/>'
                      f'<ellipse cx="{cx}" cy="{cy}" rx="400" ry="92" fill="none" stroke="#e6d6b0" stroke-width="40" opacity="0.7" transform="rotate(-12 {cx} {cy})"/>'
                      f'<ellipse cx="{cx}" cy="{cy}" rx="436" ry="101" fill="none" stroke="#1a140c" stroke-width="5" opacity="0.7" transform="rotate(-12 {cx} {cy})"/>')
    bandas = "".join(f'<ellipse cx="{cx}" cy="{cy - R + y}" rx="{R*1.02:.0f}" ry="{6 + (y % 23):.0f}" fill="{c}" opacity="0.35"/>'
                     for y, c in [(60, "#a87a44"), (110, "#fff0c8"), (150, "#b8884e"), (210, "#c89a5a"), (260, "#fff0c8"), (300, "#9a6a34"), (340, "#c89a5a")])
    planeta = (f'<clipPath id="sa_c"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath>'
               f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#sa_p)"/><g clip-path="url(#sa_c)" transform="rotate(-12 {cx} {cy})">{bandas}</g>'
               f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#sa_s)"/>'
               f'<path d="M{cx-R} {cy+20} Q{cx} {cy+60} {cx+R} {cy-20}" stroke="#000" stroke-width="26" opacity="0.25" fill="none" clip-path="url(#sa_c)"/>')
    b = [f'<g clip-path="url(#sa_top)">{anillo()}</g>', planeta, f'<g clip-path="url(#sa_bot)">{anillo()}</g>']
    guardar(nombre, "".join(b), w, h, d)


def banera():
    w, h = 1080, 760
    d = lg("ba_c", (0, "#ffffff"), (0.6, "#dfe6ee"), (1, "#9aa6b4")) + lg("ba_a", (0, "#7fd4ff"), (1, "#1a6aa8"))
    b = ['<ellipse cx="540" cy="735" rx="470" ry="22" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<path d="M70 230 L1010 230 C1010 520 900 640 760 660 L320 660 C180 640 70 520 70 230 Z" fill="url(#ba_c)"/>',
         '<path d="M70 230 L1010 230 L1010 262 L70 262 Z" fill="#ffffff"/>',
         '<path d="M90 262 L990 262 C985 300 980 330 970 350 L110 350 C100 330 95 300 90 262 Z" fill="url(#ba_a)" opacity="0.85"/>',
         '<path d="M90 262 L990 262" stroke="#dff6ff" stroke-width="6" opacity="0.8"/>',
         '<path d="M250 660 L230 740 M830 660 L850 740" stroke="#c8a24a" stroke-width="26" stroke-linecap="round"/>',
         '<path d="M140 140 C140 60 230 60 230 120 L230 230" stroke="#c0c8d2" stroke-width="22" fill="none" stroke-linecap="round"/>',
         '<path d="M140 240 C300 280 760 280 960 240" stroke="#ffffff" stroke-width="8" opacity="0.6" fill="none"/>']
    guardar("banera", "".join(b), w, h, d)
    guardar("agua_frente", '<path d="M0 60 C120 30 240 90 360 60 C480 30 600 90 720 60 C840 30 960 90 1080 60 L1080 400 L0 400 Z" fill="#2a8ad0" opacity="0.55"/>'
            '<path d="M0 60 C120 30 240 90 360 60 C480 30 600 90 720 60 C840 30 960 90 1080 60" stroke="#dff6ff" stroke-width="6" fill="none" opacity="0.9"/>', 1080, 400)


def cubo(nombre, cara, lado, arriba, etiqueta=""):
    w = h = 420
    b = [f'<ellipse cx="210" cy="395" rx="170" ry="14" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         f'<path d="M60 150 L260 150 L260 380 L60 380 Z" fill="{cara}"/>',
         f'<path d="M260 150 L360 80 L360 310 L260 380 Z" fill="{lado}"/>',
         f'<path d="M60 150 L160 80 L360 80 L260 150 Z" fill="{arriba}"/>',
         f'<path d="M60 150 L260 150 L360 80 M260 150 L260 380" stroke="#ffffff" stroke-width="3" opacity="0.5" fill="none"/>',
         f'<path d="M80 170 L130 170 L80 240 Z" fill="#ffffff" opacity="0.25"/>']
    guardar(nombre, "".join(b), w, h)


def casa():
    w, h = 420, 400
    b = ['<ellipse cx="210" cy="385" rx="180" ry="12" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<path d="M60 190 L210 70 L360 190 Z" fill="#c0392b"/><path d="M60 190 L210 70 L215 76 L70 196 Z" fill="#ff8a7a" opacity="0.5"/>',
         '<rect x="85" y="190" width="250" height="190" fill="#f2e2c4"/><rect x="185" y="270" width="60" height="110" fill="#6a4228"/>',
         '<rect x="110" y="220" width="55" height="50" fill="#7fc4ff"/><rect x="265" y="220" width="55" height="50" fill="#7fc4ff"/>',
         '<rect x="270" y="95" width="34" height="70" fill="#8a4a32"/>']
    guardar("casa", "".join(b), w, h)


def roca_hielo(nombre, sem):
    w = h = 400
    r = random.Random(sem)
    pts = []
    for i in range(11):
        a = i / 11 * 6.283; rr = r.uniform(120, 175)
        pts.append(f"{200+rr*math.cos(a):.0f} {200+rr*math.sin(a)*0.85:.0f}")
    d = lg(f"{nombre}_g", (0, "#f4fbff"), (0.5, "#bcd6ea"), (1, "#6a7c90"))
    b = [f'<path d="M{" L".join(pts)} Z" fill="url(#{nombre}_g)"/>',
         *[f'<circle cx="{r.uniform(110,290):.0f}" cy="{r.uniform(120,280):.0f}" r="{r.uniform(6,16):.0f}" fill="#5a6a80" opacity="0.45"/>' for _ in range(7)],
         f'<path d="M{" L".join(pts[:5])}" stroke="#ffffff" stroke-width="5" fill="none" opacity="0.6"/>', grano(w, h)]
    guardar(nombre, "".join(b), w, h, d)


def edificio():
    w, h = 300, 520
    b = ['<rect x="40" y="40" width="220" height="470" fill="#5a6474"/>', '<rect x="40" y="40" width="220" height="20" fill="#8a94a4"/>',
         *[f'<rect x="{x}" y="{y}" width="50" height="70" fill="#ffe08a" opacity="{0.9 if (x+y) % 3 else 0.4}"/>' for x in (65, 125, 185) for y in (90, 240, 390)]]
    guardar("edificio", "".join(b), w, h)


def gota_gas():
    w = h = 400
    d = rg("gg", (0, "#f0d8a0", 0.9), (0.6, "#d9b070", 0.4), (1, "#d9b070", 0))
    guardar("nube_gas", '<circle cx="200" cy="200" r="190" fill="url(#gg)" filter="url(#blur20)"/>', w, h, d)


# ====================================================================== 03 · koala
def huella(nombre="huella", color="#ffd23f", fondo=None, sem=5, w=600, h=760):
    """Huella dactilar: crestas en remolino (elipses concéntricas que se abren arriba) con cortes y bifurcaciones."""
    r = random.Random(sem)
    cx, cy = w / 2, h * 0.55
    b = []
    if fondo:
        b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{w*0.45}" ry="{h*0.47}" fill="{fondo}"/>')
    b.append(f'<clipPath id="{nombre}_k"><ellipse cx="{cx}" cy="{cy}" rx="{w*0.44}" ry="{h*0.46}"/></clipPath><g clip-path="url(#{nombre}_k)">')
    for i in range(1, 26):
        rx, ry = 12 + i * 12.5, 16 + i * 15.5
        a0 = r.uniform(-0.25, 0.25)
        # arco casi completo con un hueco (crestas que se cortan)
        g0 = r.uniform(0.2, 5.6); g1 = g0 + r.uniform(0.15, 0.45)
        def p(t): return f"{cx + rx*math.cos(t):.1f} {cy + ry*math.sin(t) - i*1.5:.1f}"
        b.append(f'<path d="M{p(g1)} A{rx} {ry} {a0:.2f} 1 1 {p(g0 + 6.283)}" stroke="{color}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    for i in range(10):   # crestas exteriores en arco (bucle de arriba)
        y = cy - h * 0.25 - i * 22
        b.append(f'<path d="M{cx - w*0.5:.0f} {y + 80:.0f} Q{cx:.0f} {y - 60:.0f} {cx + w*0.5:.0f} {y + 80:.0f}" stroke="{color}" stroke-width="7" fill="none"/>')
    b.append("</g>")
    guardar(nombre, "".join(b), w, h)


def koala(nombre="koala", sem=7):
    """Koala sentado agarrado a una rama (vertical): pelo gris con textura, orejas peludas, nariz grande."""
    w, h = 700, 900
    r = random.Random(sem)
    d = (lg("ko_c", (0, "#b8bcc4"), (0.6, "#8a8f98"), (1, "#5a5e66")) + rg("ko_o", (0, "#f4f0ea", 1), (1, "#b8bcc4", 1)) +
         lg("ko_n", (0, "#3a3a40"), (1, "#141418")) + lg("ko_t", (0, "#5a4a3a"), (1, "#2a2016"), x2=1, y2=0))
    pelo = "".join(f'<path d="M{x:.0f} {y:.0f} l{r.uniform(-6,6):.0f} {r.uniform(8,16):.0f}" stroke="{r.choice(["#d8dce2", "#6a6e76"])}" stroke-width="2" opacity="0.5"/>'
                   for x, y in [(r.uniform(170, 560), r.uniform(220, 800)) for _ in range(260)])
    b = ['<rect x="420" y="0" width="120" height="900" fill="url(#ko_t)"/>',
         '<path d="M440 0 L440 900" stroke="#8a7458" stroke-width="5" opacity="0.5"/>',
         # cuerpo
         '<ellipse cx="380" cy="600" rx="190" ry="230" fill="url(#ko_c)"/>',
         '<ellipse cx="350" cy="640" rx="110" ry="150" fill="#e8e4dc" opacity="0.75"/>',
         # brazo que abraza el tronco
         '<path d="M400 470 C470 440 540 450 560 500 C570 530 540 545 515 530 C480 515 450 520 420 540 Z" fill="#9a9ea8"/>',
         *[f'<path d="M{548+i*8} {500+i*6} l18 6" stroke="#1a1a1a" stroke-width="5" stroke-linecap="round"/>' for i in range(3)],
         '<path d="M330 760 C380 800 460 800 530 780 C545 800 520 830 480 830 C420 835 360 820 330 790 Z" fill="#8a8f98"/>',
         # cabeza
         '<circle cx="190" cy="250" r="95" fill="#8a8f98"/><circle cx="190" cy="250" r="62" fill="url(#ko_o)"/>',
         '<circle cx="540" cy="250" r="95" fill="#8a8f98"/><circle cx="540" cy="250" r="62" fill="url(#ko_o)"/>',
         '<ellipse cx="365" cy="320" rx="190" ry="165" fill="url(#ko_c)"/>',
         '<ellipse cx="365" cy="360" rx="58" ry="80" fill="url(#ko_n)"/><ellipse cx="350" cy="320" rx="16" ry="26" fill="#ffffff" opacity="0.25"/>',
         '<circle cx="280" cy="300" r="15" fill="#141418"/><circle cx="285" cy="295" r="5" fill="#fff"/>',
         '<circle cx="450" cy="300" r="15" fill="#141418"/><circle cx="455" cy="295" r="5" fill="#fff"/>',
         '<path d="M330 450 Q365 470 400 450" stroke="#2a2a2e" stroke-width="5" fill="none"/>',
         pelo, '<ellipse cx="365" cy="320" rx="190" ry="165" fill="none" stroke="#e8f0ff" stroke-width="4" opacity="0.4"/>']
    guardar(nombre, "".join(b), w, h, d)


def mano_koala():
    """Mano de koala (2 pulgares) agarrando una rama: dedos con yemas rosadas y crestas."""
    w, h = 800, 700
    d = lg("mk_p", (0, "#9a9ea8"), (1, "#5a5e66")) + lg("mk_y", (0, "#e8b4a8"), (1, "#a86a60")) + lg("mk_r", (0, "#6a5238"), (1, "#3a2a1a"))
    dedos = [(250, 300, -30), (330, 260, -10), (470, 260, 10), (550, 300, 30), (600, 420, 60)]
    b = ['<rect x="0" y="380" width="800" height="120" rx="60" fill="url(#mk_r)"/>',
         '<path d="M0 400 L800 400" stroke="#9a7a54" stroke-width="6" opacity="0.6"/>',
         '<path d="M220 700 C210 560 260 450 400 440 C540 450 590 560 580 700 Z" fill="url(#mk_p)"/>']
    for x, y, a in dedos:
        b.append(f'<g transform="rotate({a} {x} {y+140})"><rect x="{x-40}" y="{y}" width="80" height="190" rx="40" fill="url(#mk_p)"/>'
                 f'<ellipse cx="{x}" cy="{y+40}" rx="30" ry="34" fill="url(#mk_y)"/>'
                 + "".join(f'<path d="M{x-22+k*2} {y+30+k*6} q22 -10 44 0" stroke="#7a4a40" stroke-width="2" fill="none"/>' for k in range(4)) +
                 f'<path d="M{x} {y-6} l0 -26" stroke="#1a1a1a" stroke-width="10" stroke-linecap="round"/></g>')
    guardar("mano_koala", "".join(b), w, h, d)


def microscopio():
    w, h = 600, 900
    d = lg("mi_c", (0, "#f4f6fa"), (1, "#9aa4b0")) + lg("mi_n", (0, "#3a4250"), (1, "#141820"))
    b = ['<ellipse cx="300" cy="875" rx="230" ry="18" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         '<rect x="90" y="790" width="420" height="80" rx="24" fill="url(#mi_n)"/>',
         '<path d="M360 790 C460 700 470 450 380 330 L330 360 C400 460 400 680 310 790 Z" fill="url(#mi_c)"/>',
         '<rect x="140" y="600" width="300" height="34" rx="10" fill="url(#mi_n)"/>',
         '<g transform="rotate(-25 260 300)"><rect x="220" y="80" width="90" height="380" rx="18" fill="url(#mi_c)"/>'
         '<rect x="235" y="30" width="60" height="70" rx="10" fill="url(#mi_n)"/><rect x="230" y="450" width="70" height="90" rx="10" fill="url(#mi_n)"/></g>',
         '<circle cx="400" cy="400" r="40" fill="url(#mi_n)"/>', grano(w, h)]
    guardar("microscopio", "".join(b), w, h, d)


def detective():
    w, h = 600, 1000
    sil = ("M300 120 C350 120 380 160 380 210 C380 260 350 300 300 300 C250 300 220 260 220 210 C220 160 250 120 300 120 Z "
           "M180 330 C230 310 370 310 420 330 C480 350 500 420 505 500 L520 980 L360 980 L330 620 L270 620 L240 980 L80 980 L95 500 C100 420 120 350 180 330 Z")
    b = [f'<path d="{sil}" fill="#141820"/>', '<path d="M150 140 L450 140 L420 120 L390 40 L210 40 L180 120 Z" fill="#141820"/>',
         '<path d="M120 145 L480 145" stroke="#141820" stroke-width="22" stroke-linecap="round"/>',
         f'<path d="{sil}" fill="none" stroke="#ffcf8a" stroke-width="4" opacity="0.5"/>']
    guardar("detective", "".join(b), w, h)


def canguro():
    w, h = 700, 800
    c, l = "#9a5a32", "#ffcf8a"
    b = ['<ellipse cx="380" cy="770" rx="260" ry="16" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         f'<path d="M300 560 C220 640 120 700 30 760 C150 730 260 680 340 620 Z" fill="{c}"/>',                     # cola
         f'<ellipse cx="380" cy="480" rx="130" ry="200" fill="{c}" transform="rotate(20 380 480)"/>',                # cuerpo
         f'<ellipse cx="330" cy="600" rx="110" ry="140" fill="#8a4e2a"/>',                                         # muslo
         f'<path d="M300 700 L560 740 C590 745 590 770 560 770 L290 760 Z" fill="#7a4424"/>',                       # pie largo
         f'<ellipse cx="490" cy="280" rx="70" ry="55" fill="{c}" transform="rotate(-20 490 280)"/>',                 # cabeza
         f'<path d="M530 270 C580 270 610 290 600 310 C580 320 540 315 520 300 Z" fill="{c}"/>',                      # hocico
         f'<path d="M455 240 L440 150 L480 225 Z M490 232 L495 140 L515 228 Z" fill="#8a4e2a"/>',                   # orejas
         f'<path d="M470 420 C520 440 540 470 545 500" stroke="{c}" stroke-width="24" fill="none" stroke-linecap="round"/>',  # brazo
         '<circle cx="515" cy="268" r="9" fill="#1a1208"/><circle cx="600" cy="303" r="7" fill="#1a1208"/>',
         f'<ellipse cx="400" cy="500" rx="60" ry="110" fill="#e8b88a" opacity="0.45" transform="rotate(20 400 500)"/>',
         f'<ellipse cx="380" cy="480" rx="130" ry="200" fill="none" stroke="{l}" stroke-width="4" opacity="0.45" transform="rotate(20 380 480)"/>']
    guardar("canguro", "".join(b), w, h)


def wombat():
    w, h = 600, 380
    cuerpo = "M60 260 C40 160 140 80 300 80 C430 80 520 140 545 220 C560 270 540 320 500 330 L120 330 C80 320 64 300 60 260 Z"
    b = ['<ellipse cx="300" cy="345" rx="250" ry="16" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         f'<path d="{cuerpo}" fill="#7a6650"/>', '<path d="M120 330 l0 30 l40 0 l0 -30 M440 330 l0 30 l40 0 l0 -30" fill="#5a4a38"/>',
         '<circle cx="470" cy="180" r="9" fill="#1a1208"/><ellipse cx="530" cy="230" rx="22" ry="18" fill="#2a2018"/>',
         '<path d="M420 110 l10 -40 l25 35 Z" fill="#6a5640"/>',
         f'<path d="{cuerpo}" fill="none" stroke="#ffd8a0" stroke-width="3" opacity="0.5"/>']
    guardar("wombat", "".join(b), w, h)


def rama_eucalipto():
    w, h = 900, 520
    r = random.Random(33)
    b = ['<path d="M900 300 C700 280 450 250 60 270" stroke="#6a5642" stroke-width="22" stroke-linecap="round" fill="none"/>',
         '<path d="M900 294 C700 274 450 244 60 264" stroke="#c8b49a" stroke-width="5" opacity="0.6" fill="none"/>']
    for i in range(18):
        x = 90 + i * 44 + r.uniform(-10, 10); y = 270 + (900 - x) * 0.03
        for sgn in (-1, 1):
            b.append(_hoja(x, y, r.uniform(130, 190), 90 * sgn + r.uniform(-25, 25) + (0 if sgn > 0 else 0), r.choice(["#6a9a8a", "#7aaa96", "#5a8a7c", "#8ab8a2"]), luz="#d8f0e4"))
    guardar("rama_eucalipto", "".join(b), w, h)


def bg_bosque():
    d = lg("bo_f", (0, "#f2c88a"), (0.45, "#c88a5a"), (1, "#3a2a20")) + rg("bo_s", (0, "#fff2c8", 0.9), (1, "#fff2c8", 0), cx=0.6, cy=0.3)
    r = random.Random(44)
    b = ['<rect width="1080" height="1920" fill="url(#bo_f)"/>', '<ellipse cx="650" cy="560" rx="600" ry="500" fill="url(#bo_s)"/>']
    for capa, (col, y0, n) in enumerate([("#8a7a6a", 1100, 7), ("#5a5048", 1250, 6), ("#2e2a26", 1450, 5)]):
        for k in range(n):
            x = r.uniform(0, 1080); hh = r.uniform(700, 1100)
            b.append(f'<path d="M{x:.0f} 1920 C{x+10:.0f} {y0:.0f} {x-15:.0f} {y0-hh*0.5:.0f} {x+20:.0f} {y0-hh:.0f}" stroke="{col}" stroke-width="{14+capa*10}" fill="none"/>')
            b.append(f'<ellipse cx="{x+20:.0f}" cy="{y0-hh:.0f}" rx="{160+capa*40}" ry="{100+capa*20}" fill="{col}" opacity="0.85"/>')
    b.append('<rect x="0" y="1500" width="1080" height="420" fill="#2a2018"/>')
    b.append(grano())
    guardar("bg_bosque", "".join(b), defs=d)


def arbol_familia():
    """Dos ramas que se separan de un tronco común (antepasado) → koala / humano. Etiquetas en el montaje."""
    w, h = 900, 1000
    b = ['<path d="M450 980 L450 640" stroke="#ffd23f" stroke-width="16" stroke-linecap="round"/>',
         '<path d="M450 640 C450 520 250 460 200 200" stroke="#2ff3ff" stroke-width="14" fill="none" stroke-linecap="round"/>',
         '<path d="M450 640 C450 520 650 460 700 200" stroke="#ff3df2" stroke-width="14" fill="none" stroke-linecap="round"/>',
         '<circle cx="450" cy="640" r="34" fill="#ffd23f"/>', '<circle cx="200" cy="180" r="28" fill="#2ff3ff"/>', '<circle cx="700" cy="180" r="28" fill="#ff3df2"/>']
    guardar("arbol_familia", "".join(b), w, h)


def cinta_policia():
    w, h = 1400, 140
    b = ['<rect x="0" y="20" width="1400" height="100" fill="#ffd23f"/>',
         *[f'<path d="M{x} 20 l60 0 l-60 100 l-60 0 Z" fill="#141414" opacity="0.9"/>' for x in range(0, 1500, 260)],
         *[f'<text x="{x+150}" y="88" font-family="DejaVu Sans" font-weight="bold" font-size="46" fill="#141414">NO PASAR</text>' for x in range(0, 1400, 520)]]
    guardar("cinta", "".join(b), w, h)


def generar(dirsvg):
    ilus.OUT = dirsvg
    os.makedirs(dirsvg, exist_ok=True)
    platano(); platano("platano_b", 14, 9); racimo(); detector(); atomo(); atomo("atomo_h", "#7aa8ff", "#ff3df2"); chispa()
    bg_cocina(); bg_lab(); cuerpo_rayos(); escaner(); rinon_flecha()
    saturno(); banera(); cubo("cubo_agua", "#3a9ae0", "#1a6aa8", "#8ad4ff"); cubo("cubo_saturno", "#e8c88a", "#b8884e", "#f6e2b0")
    casa(); roca_hielo("hielo1", 1); roca_hielo("hielo2", 2); roca_hielo("hielo3", 3); edificio(); gota_gas()
    huella("huella", "#ffd23f"); huella("huella_koala", "#7df9ff", sem=9); huella("huella_tinta", "#1a1a22", "#f2ead8", sem=5)
    koala(); mano_koala(); microscopio(); detective(); canguro(); wombat(); rama_eucalipto(); bg_bosque(); arbol_familia(); cinta_policia()
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
