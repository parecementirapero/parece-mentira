"""Ilustraciones de los vídeos 02 («El dólar no es americano») y 03 («Esta máquina engañó a Napoleón», el Turco).
Vídeos extra 2026-11-19 (Nico, chat). Uso: python3 ilus_extra2.py DIR_SVG. Ladrillos de motor/biblioteca/ilus.py.
Reutiliza: pluma (lote 2026-11-18-manana), hoguera (2026-11-17-tarde), hoja de calendario (2026-11-18-tarde) y las piezas de ilus_nino."""
import math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ); sys.path.insert(0, AQUI)
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano  # noqa: E402
import ilus_nino  # noqa: E402
from ilus_nino import _p, _mod  # noqa: E402

PLATA = lambda i: lg(i, (0, "#f4f6fa"), (0.35, "#c8ced8"), (0.6, "#8a92a0"), (1, "#dfe4ec"), x2=1, y2=1)  # noqa: E731
ORO = lambda i: lg(i, (0, "#fff2b0"), (0.4, "#f0c040"), (0.7, "#b8861e"), (1, "#ffe07a"), x2=1, y2=1)  # noqa: E731


def _texto(x, y, t, tam, color="#1a1a1a", peso=800, extra=""):
    fam = "" if "font-family" in extra else 'font-family="DejaVu Sans, Arial, sans-serif" '
    return f'<text x="{x}" y="{y}" {fam}font-size="{tam}" font-weight="{peso}" fill="{color}" text-anchor="middle" {extra}>{t}</text>'


# ====================================================================== 02 · EL DÓLAR
def billete():
    """Billete verde genérico (sin retrato ni diseño real): marco, óvalo vacío con «$» y cifras."""
    w, h = 1000, 460
    d = lg("bi_g", (0, "#d8ecc8"), (0.5, "#a8cf9a"), (1, "#7fae78"), x2=1, y2=1) + lg("bi_o", (0, "#2f6b3a"), (1, "#1c4526"))
    b = ['<rect x="20" y="34" width="960" height="410" rx="16" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<rect x="10" y="14" width="980" height="420" rx="14" fill="url(#bi_g)" stroke="#1c4526" stroke-width="8"/>',
         '<rect x="38" y="42" width="924" height="364" rx="8" fill="none" stroke="#2f6b3a" stroke-width="5"/>',
         '<rect x="52" y="56" width="896" height="336" rx="6" fill="none" stroke="#2f6b3a" stroke-width="2" stroke-dasharray="4 6"/>']
    for k in range(34):  # guilloché
        b.append(f'<ellipse cx="500" cy="224" rx="{150 + k*9}" ry="{120 + k*2.4:.0f}" fill="none" stroke="#2f6b3a" stroke-width="1.4" opacity="{0.28 - k*0.006:.2f}"/>')
    b.append('<ellipse cx="500" cy="224" rx="150" ry="150" fill="#eaf5dc" stroke="url(#bi_o)" stroke-width="10"/>')
    b.append(_texto(500, 298, "$", 220, "#1c4526", 900))
    for x, y in [(110, 130), (890, 130), (110, 360), (890, 360)]:
        b.append(f'<circle cx="{x}" cy="{y-30}" r="52" fill="#eaf5dc" stroke="#2f6b3a" stroke-width="5"/>' + _texto(x, y - 6, "1", 76, "#1c4526", 900))
    b.append('<rect x="10" y="14" width="980" height="420" rx="14" fill="#ffffff" opacity="0.08"/><path d="M10 14 L420 14 L260 434 L10 434 Z" fill="#ffffff" opacity="0.10"/>')
    guardar("billete", "".join(b), w, h, d)


def _moneda(nombre, dibujo, leyenda="", metal=PLATA, borde="#5a6270", w=700):
    r = random.Random(len(nombre))
    c = w / 2
    d = metal(f"{nombre}_m") + rg(f"{nombre}_b", (0, "#ffffff", 0.7), (0.5, "#ffffff", 0.0), (1, "#000000", 0.25), cx=0.32, cy=0.28, r=0.9)
    b = [f'<ellipse cx="{c}" cy="{w*0.96}" rx="{w*0.36}" ry="{w*0.03}" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         f'<circle cx="{c}" cy="{c}" r="{w*0.46}" fill="url(#{nombre}_m)" stroke="{borde}" stroke-width="{w*0.014:.0f}"/>']
    for k in range(64):  # canto estriado
        a = 2 * math.pi * k / 64
        b.append(f'<path d="M{c + w*0.43*math.cos(a):.0f} {c + w*0.43*math.sin(a):.0f} L{c + w*0.455*math.cos(a):.0f} {c + w*0.455*math.sin(a):.0f}" stroke="{borde}" stroke-width="4" opacity="0.6"/>')
    b.append(f'<circle cx="{c}" cy="{c}" r="{w*0.385}" fill="none" stroke="{borde}" stroke-width="5" opacity="0.8"/>')
    b.append(dibujo)
    if leyenda:
        b.append(f'<path id="{nombre}_arc" d="M{c - w*0.33} {c} A{w*0.33} {w*0.33} 0 0 1 {c + w*0.33} {c}" fill="none"/>'
                 f'<text font-family="DejaVu Serif, serif" font-size="{w*0.062:.0f}" font-weight="700" fill="{borde}" letter-spacing="6"><textPath href="#{nombre}_arc" startOffset="50%" text-anchor="middle">{leyenda}</textPath></text>')
    for k in range(14):  # desgaste
        x, y = c + r.uniform(-w*0.3, w*0.3), c + r.uniform(-w*0.3, w*0.3)
        b.append(f'<path d="M{x:.0f} {y:.0f} l{r.uniform(-30,30):.0f} {r.uniform(-12,12):.0f}" stroke="#ffffff" stroke-width="2" opacity="0.35"/>')
    b.append(f'<circle cx="{c}" cy="{c}" r="{w*0.46}" fill="url(#{nombre}_b)"/>')
    guardar(nombre, "".join(b), w, w, d)


def talero():
    """Tálero de 1520: león rampante muy simplificado (silueta heráldica) y la fecha."""
    leon = ('<g transform="translate(350 360)" fill="#5a6270">'
            '<path d="M-70 120 Q-90 20 -30 -40 Q-60 -90 -10 -120 Q40 -130 60 -90 Q110 -80 100 -40 L60 -30 Q90 10 70 70 L110 130 L70 140 L30 80 L10 140 L-30 140 L-20 70 Q-40 100 -40 140 L-80 140 Z"/>'
            '<path d="M-70 60 Q-150 40 -140 -40 Q-120 -90 -90 -60 Q-110 -30 -100 10 Q-90 40 -60 30 Z"/>'
            '<path d="M60 -90 l40 -50 l10 50 Z M10 -120 l-10 -50 l40 40 Z"/><circle cx="50" cy="-70" r="8" fill="#f4f6fa"/></g>')
    _moneda("talero", leon + _texto(350, 590, "1520", 70, "#5a6270", 800, 'font-family="DejaVu Serif, serif"'), "· TALER · BOHEMIA ·")


def real_de_a_ocho():
    """Real de a ocho: las dos columnas con sus cintas, olas y el «8»."""
    col = lambda x: (f'<rect x="{x-26}" y="210" width="52" height="240" fill="#5a6270"/><rect x="{x-40}" y="190" width="80" height="26" rx="6" fill="#5a6270"/>'  # noqa: E731
                     f'<rect x="{x-40}" y="446" width="80" height="24" rx="6" fill="#5a6270"/><path d="M{x-30} 176 l14 -30 l16 22 l16 -22 l14 30 Z" fill="#5a6270"/>'
                     f'<path d="M{x-56} 270 Q{x} 300 {x+56} 262 L{x+56} 296 Q{x} 336 {x-56} 304 Z" fill="#f4f6fa" stroke="#5a6270" stroke-width="5"/>')
    olas = "".join(f'<path d="M190 {490 + k*24} q40 -22 80 0 t80 0 t80 0 t80 0" stroke="#5a6270" stroke-width="7" fill="none"/>' for k in range(3))
    _moneda("real_de_a_ocho", col(250) + col(450) + olas + _texto(350, 400, "8", 150, "#5a6270", 900, 'font-family="DejaVu Serif, serif"'), "· HISPANIARUM · REX ·")


def moneda_oro():
    _moneda("moneda_oro", _texto(350, 440, "$", 330, "#7a5a10", 900), "", ORO, "#7a5a10")


def bg_valle():
    """Valle minero de Bohemia en 1520: montes con pinos, pueblo y bocamina."""
    r = random.Random(71)
    d = (lg("va_c", (0, "#2a3a5a"), (0.4, "#c88a6a"), (0.62, "#ffd8a0")) + lg("va_m1", (0, "#6a7a8a"), (1, "#3a4a5a")) +
         lg("va_m2", (0, "#3e5a48"), (1, "#1e3024")) + lg("va_m3", (0, "#2a4030"), (1, "#0c1810")) + rg("va_s", (0, "#fff6d0", 1), (0.3, "#ffd08a", 0.6), (1, "#ffb040", 0)))
    b = ['<rect width="1080" height="1920" fill="url(#va_c)"/>', '<circle cx="540" cy="1050" r="420" fill="url(#va_s)"/>']
    b.append('<path d="M-20 1150 L160 860 L300 1000 L460 780 L620 1010 L780 840 L940 1000 L1100 880 L1100 1400 L-20 1400 Z" fill="url(#va_m1)" opacity="0.85"/>')
    b.append('<path d="M460 780 l40 70 l-30 -10 l-20 40 l-30 -40 Z M160 860 l30 50 l-40 -6 Z M780 840 l34 60 l-50 -10 Z" fill="#f4f6fa" opacity="0.8"/>')
    b.append('<path d="M-20 1300 Q200 1120 420 1330 Q500 1400 540 1420 Q600 1400 680 1320 Q880 1130 1100 1280 L1100 1940 L-20 1940 Z" fill="url(#va_m2)"/>')
    for k in range(70):  # pinos en las laderas
        x = r.uniform(0, 1080); u = abs(x - 540) / 540
        y = 1420 - u * 170 + r.uniform(0, 250); s = r.uniform(0.6, 1.3) * (0.6 + (y - 1250) / 600)
        if abs(x - 540) < 120 and y < 1560: continue
        b.append(f'<path d="M{x:.0f} {y:.0f} l{-22*s:.0f} {60*s:.0f} l{14*s:.0f} 0 l{-18*s:.0f} {50*s:.0f} l{52*s:.0f} 0 l{-18*s:.0f} {-50*s:.0f} l{14*s:.0f} 0 Z" fill="#14281c" opacity="{0.6 + 0.4*(y-1250)/600:.2f}"/>')
    for x, y, s in [(430, 1500, 1.0), (520, 1520, 0.8), (620, 1505, 1.1), (700, 1540, 0.7)]:  # casas del pueblo
        b.append(f'<g transform="translate({x} {y}) scale({s})"><rect x="-34" y="0" width="68" height="56" fill="#d8c0a0"/><path d="M-44 4 L0 -44 L44 4 Z" fill="#7a3a2a"/><rect x="-8" y="22" width="16" height="34" fill="#3a2418"/><rect x="14" y="14" width="12" height="12" fill="#ffd27a"/></g>')
    b.append('<path d="M-20 1700 Q300 1600 620 1690 Q900 1760 1100 1680 L1100 1940 L-20 1940 Z" fill="url(#va_m3)"/>')
    # bocamina con vigas
    b.append('<g transform="translate(860 1640)"><path d="M-110 120 L-110 -20 Q0 -110 110 -20 L110 120 Z" fill="#05070a"/><path d="M-120 124 L-120 -30 M120 124 L120 -30 M-132 -30 L132 -30" stroke="#6a4a2a" stroke-width="22" stroke-linecap="round"/>'
             '<path d="M-60 124 L60 124 M-40 124 L-20 60 M40 124 L20 60" stroke="#8a8a8a" stroke-width="6"/><circle cx="0" cy="20" r="60" fill="#ffd27a" opacity="0.25" filter="url(#blur20)"/></g>')
    b.append(grano())
    guardar("bg_valle", "".join(b), defs=d)


def vagoneta():
    w, h = 800, 620
    r = random.Random(73)
    d = lg("vg_c", (0, "#8a6a4a"), (1, "#3a2818")) + PLATA("vg_p")
    b = ['<ellipse cx="400" cy="590" rx="330" ry="20" fill="#000" opacity="0.45" filter="url(#blur8)"/>']
    for k in range(22):  # mineral de plata
        x, y, s = 180 + r.uniform(0, 440), 190 + r.uniform(-90, 60), r.uniform(40, 90)
        pts = [(x + s * math.cos(a + r.uniform(-0.3, 0.3)) * r.uniform(0.7, 1), y + s * 0.8 * math.sin(a) * r.uniform(0.7, 1)) for a in [i * math.pi / 3 for i in range(6)]]
        b.append(f'<path d="{_p(pts)}" fill="url(#vg_p)" stroke="#5a6270" stroke-width="4"/><path d="M{x-s*0.3:.0f} {y-s*0.3:.0f} l{s*0.4:.0f} {-s*0.1:.0f}" stroke="#ffffff" stroke-width="5" opacity="0.8"/>')
    b.append('<path d="M110 230 L690 230 L630 480 L170 480 Z" fill="url(#vg_c)" stroke="#1e140c" stroke-width="8" stroke-linejoin="round"/>')
    for x in range(200, 640, 90):
        b.append(f'<path d="M{x} 236 l{(x-400)*-0.1:.0f} 240" stroke="#1e140c" stroke-width="5" opacity="0.6"/>')
    b.append('<path d="M110 250 L690 250 M150 420 L650 420" stroke="#4a4a4a" stroke-width="16"/>')
    for x in (250, 550):
        b.append(f'<circle cx="{x}" cy="520" r="62" fill="#2a2a2a" stroke="#8a8a8a" stroke-width="10"/><circle cx="{x}" cy="520" r="14" fill="#8a8a8a"/>'
                 + "".join(f'<path d="M{x} 520 l{50*math.cos(a):.0f} {50*math.sin(a):.0f}" stroke="#6a6a6a" stroke-width="7"/>' for a in [i * math.pi / 3 for i in range(6)]))
    b.append('<path d="M40 584 L760 584" stroke="#6a6a6a" stroke-width="10"/>')
    guardar("vagoneta", "".join(b), w, h, d)


def galeon():
    w, h = 1000, 1000
    d = (lg("ga_c", (0, "#8a5a32"), (1, "#3a2010")) + lg("ga_v", (0, "#fff8e8"), (1, "#d8c8a0")) + lg("ga_o", (0, "#ffd23f"), (1, "#b8861e")))
    b = ['<ellipse cx="500" cy="930" rx="420" ry="26" fill="#001020" opacity="0.45" filter="url(#blur8)"/>']
    for x, top, hh in [(300, 170, 620), (520, 90, 700), (720, 220, 560)]:  # mástiles y velas
        b.append(f'<rect x="{x-8}" y="{top}" width="16" height="{hh}" fill="#4a2e18"/>')
        for k, (y0, wv, hv) in enumerate([(top + 40, 220, 170), (top + 240, 280, 210)]):
            b.append(f'<path d="M{x - wv/2:.0f} {y0} Q{x} {y0 + 30} {x + wv/2:.0f} {y0} Q{x + wv/2 + 40:.0f} {y0 + hv/2:.0f} {x + wv/2:.0f} {y0 + hv} Q{x} {y0 + hv - 30} {x - wv/2:.0f} {y0 + hv} Q{x - wv/2 + 30:.0f} {y0 + hv/2:.0f} {x - wv/2:.0f} {y0} Z" fill="url(#ga_v)" stroke="#8a7a5a" stroke-width="4"/>')
            if x == 520 and k == 1:  # cruz roja sencilla en la vela mayor
                b.append(f'<path d="M{x} {y0 + 40} L{x} {y0 + hv - 40} M{x - 60} {y0 + hv/2:.0f} L{x + 60} {y0 + hv/2:.0f}" stroke="#c0392b" stroke-width="20"/>')
        b.append(f'<path d="M{x+8} {top+4} l70 18 l-70 20 Z" fill="#c0392b"/>')
    b.append('<path d="M520 100 L140 720 M520 100 L900 700 M300 180 L150 720 M720 230 L880 700" stroke="#2a1a0e" stroke-width="3" fill="none" opacity="0.8"/>')
    b.append('<path d="M100 700 L210 700 L240 740 L760 740 L780 660 L930 660 L900 820 Q500 900 190 850 Z" fill="url(#ga_c)" stroke="#1e1008" stroke-width="7" stroke-linejoin="round"/>')
    b.append('<path d="M780 660 L930 660 L922 700 L772 700 Z M100 700 L210 700 L226 730 L112 730 Z" fill="url(#ga_o)" opacity="0.9"/>')
    for x in range(290, 760, 70):
        b.append(f'<rect x="{x}" y="770" width="30" height="30" fill="#1e1008"/><rect x="{x}" y="770" width="30" height="8" fill="#ffd23f" opacity="0.5"/>')
    b.append('<path d="M196 800 Q500 850 896 780" stroke="#ffd23f" stroke-width="8" fill="none" opacity="0.8"/><path d="M100 700 L60 660" stroke="#4a2e18" stroke-width="12" stroke-linecap="round"/>')
    guardar("galeon", "".join(b), w, h, d)


def bg_puerto():
    """Puerto colonial al atardecer: muelle de madera, almacenes y mar."""
    r = random.Random(77)
    d = (lg("pu_c", (0, "#3a2a5a"), (0.35, "#d86a4a"), (0.55, "#ffc88a")) + lg("pu_m", (0, "#ff9a6a"), (0.25, "#8a5a6a"), (1, "#1a1430")) +
         lg("pu_w", (0, "#7a5232"), (1, "#2a1810")) + rg("pu_s", (0, "#fffbe0", 1), (0.3, "#ffd08a", 0.6), (1, "#ffb040", 0)))
    b = ['<rect width="1080" height="1920" fill="url(#pu_c)"/>', '<circle cx="320" cy="980" r="360" fill="url(#pu_s)"/>']
    for x, w_, h_ in [(620, 190, 260), (800, 150, 200), (930, 200, 320)]:  # almacenes
        b.append(f'<rect x="{x}" y="{1060-h_}" width="{w_}" height="{h_}" fill="#3a2430"/><path d="M{x-14} {1060-h_} L{x+w_/2:.0f} {1060-h_-70} L{x+w_+14} {1060-h_} Z" fill="#5a2a2a"/>')
        for k in range(3):
            b.append(f'<rect x="{x + 24 + k*50}" y="{1060-h_+50}" width="22" height="34" fill="#ffd27a" opacity="{r.uniform(0.4,0.95):.2f}"/>')
    b.append('<rect x="0" y="1050" width="1080" height="880" fill="url(#pu_m)"/>')
    for k in range(80):
        y = r.uniform(1060, 1900); u = (y - 1050) / 870; w_ = 20 + u * 140 * r.uniform(0.4, 1); x = r.uniform(-40, 1080)
        b.append(f'<path d="M{x:.0f} {y:.0f} q{w_/4:.0f} {-5-u*8:.0f} {w_/2:.0f} 0 t{w_/2:.0f} 0" stroke="#ffe0b0" stroke-width="{2+u*4:.1f}" fill="none" opacity="{r.uniform(0.15,0.5):.2f}" stroke-linecap="round"/>')
    b.append('<path d="M-20 1560 L700 1500 L760 1560 L760 1940 L-20 1940 Z" fill="url(#pu_w)"/>')
    for k in range(12):
        b.append(f'<path d="M{-20 + k*66} {1560 - k*5} L{-40 + k*70} 1940" stroke="#1a0e08" stroke-width="5" opacity="0.6"/>')
    for x in (120, 420, 700):
        b.append(f'<rect x="{x-18}" y="{1440 - (x*0.08):.0f}" width="36" height="150" rx="8" fill="#2a1810"/><ellipse cx="{x}" cy="{1440 - (x*0.08):.0f}" rx="22" ry="9" fill="#5a3a22"/>')
    b.append(grano())
    guardar("bg_puerto", "".join(b), defs=d)


def bg_escritorio():
    """Mesa de madera a la luz de una vela (para la pluma y las letras)."""
    r = random.Random(79)
    d = lg("es_m", (0, "#4a2e1a"), (1, "#1a0e06")) + rg("es_l", (0, "#ffd88a", 0.7), (0.5, "#ff9a3a", 0.25), (1, "#ff9a3a", 0))
    b = ['<rect width="1080" height="1920" fill="url(#es_m)"/>']
    for k in range(60):
        y = r.uniform(0, 1920)
        b.append(f'<path d="M-20 {y:.0f} Q540 {y + r.uniform(-40,40):.0f} 1100 {y + r.uniform(-20,20):.0f}" stroke="{r.choice(["#6a4226", "#2a180c", "#5a3820"])}" stroke-width="{r.uniform(2,7):.0f}" fill="none" opacity="{r.uniform(0.2,0.6):.2f}"/>')
    b.append('<ellipse cx="540" cy="900" rx="760" ry="900" fill="url(#es_l)"/>')
    b.append(grano())
    guardar("bg_escritorio", "".join(b), defs=d)


def pergamino(nombre="pergamino", lineas=True):
    w, h = 900, 1100
    r = random.Random(81)
    d = lg("pg_g", (0, "#f4e4b8"), (0.5, "#e8d09a"), (1, "#c8a868"), x2=1, y2=1)
    borde = [(40 + r.uniform(-10, 10), 40 + r.uniform(-8, 8))] + [(x, 40 + r.uniform(-10, 10)) for x in range(120, 860, 80)] + \
            [(860 + r.uniform(-10, 10), y) for y in range(60, 1060, 90)] + [(x, 1060 + r.uniform(-10, 10)) for x in range(860, 40, -80)] + [(40 + r.uniform(-10, 10), y) for y in range(1060, 60, -90)]
    b = [f'<path d="{_p(borde)}" fill="#000" opacity="0.4" transform="translate(14 20)" filter="url(#blur8)"/>', f'<path d="{_p(borde)}" fill="url(#pg_g)" stroke="#8a6a3a" stroke-width="4"/>']
    for k in range(30):
        b.append(f'<circle cx="{r.uniform(60,840):.0f}" cy="{r.uniform(60,1040):.0f}" r="{r.uniform(6,40):.0f}" fill="#a8824a" opacity="{r.uniform(0.04,0.12):.2f}"/>')
    if lineas:
        for k in range(9):
            y = 170 + k * 100
            pts = [(110 + i * 34, y + r.uniform(-9, 9)) for i in range(int(r.uniform(14, 21)))]
            b.append(f'<path d="{_p(pts, False)}" stroke="#3a2410" stroke-width="5" fill="none" opacity="0.55" stroke-linejoin="round"/>')
    guardar(nombre, "".join(b), w, h, d)


def letra(nombre, t, color="#2a1808", tam=560, cursiva=True):
    w = h = 640
    est = 'font-family="DejaVu Serif, serif" font-style="italic"' if cursiva else 'font-family="DejaVu Sans, Arial, sans-serif"'
    b = [_texto(320, 480, t, tam, "#000000", 700, est + ' opacity="0.25" filter="url(#blur8)" transform="translate(8 10)"'), _texto(320, 480, t, tam, color, 700, est)]
    guardar(nombre, "".join(b), w, h)


def tricornio():
    """Colono inglés de espaldas con tricornio y casaca (sin cara)."""
    w, h = 600, 900
    d = lg("tr_c", (0, "#3a5a8a"), (1, "#1a2a4a")) + lg("tr_s", (0, "#2a2a30"), (1, "#0a0a10"))
    b = ['<ellipse cx="300" cy="870" rx="220" ry="20" fill="#000" opacity="0.45" filter="url(#blur8)"/>',
         '<path d="M120 880 Q100 520 180 400 Q300 340 420 400 Q500 520 480 880 Z" fill="url(#tr_c)" stroke="#0e1830" stroke-width="6"/>',
         '<path d="M300 400 L300 880" stroke="#0e1830" stroke-width="5"/><path d="M180 400 Q300 470 420 400" stroke="#ffd23f" stroke-width="8" fill="none"/>',
         *[f'<circle cx="{x}" cy="{y}" r="9" fill="#ffd23f"/>' for x in (270, 330) for y in (520, 620, 720)],
         '<path d="M250 330 Q300 300 350 330 L360 410 Q300 440 240 410 Z" fill="#c89a78"/>',
         '<path d="M236 330 Q300 400 364 330 Q340 250 300 250 Q260 250 236 330 Z" fill="#e8e0d0"/><path d="M290 380 Q300 470 310 380 Z" fill="#e8e0d0"/><rect x="286" y="372" width="28" height="14" fill="#1a1a1a"/>',
         '<path d="M140 280 Q300 190 460 280 Q400 310 300 300 Q200 310 140 280 Z" fill="url(#tr_s)" stroke="#000" stroke-width="5"/><path d="M200 262 Q300 150 400 262 Q300 240 200 262 Z" fill="url(#tr_s)" stroke="#000" stroke-width="5"/>',
         '<path d="M150 282 Q300 214 450 282" stroke="#ffd23f" stroke-width="6" fill="none"/>']
    guardar("tricornio", "".join(b), w, h, d)


def bandera_eeuu():
    w, h = 900, 760
    b = ['<rect x="60" y="20" width="22" height="720" rx="8" fill="#8a8a8a"/><circle cx="71" cy="20" r="20" fill="#ffd23f"/>']
    onda = lambda y: f'M82 {y} Q290 {y-40} 480 {y} T860 {y}'  # noqa: E731
    for k in range(13):
        y = 60 + k * 36
        b.append(f'<path d="{onda(y)} L860 {y+36} Q670 {y+76} 480 {y+36} T82 {y+36} Z" fill="{"#c0392b" if k % 2 == 0 else "#f8f4ec"}"/>')
    b.append('<path d="M82 60 Q250 28 420 46 L420 298 Q250 280 82 312 Z" fill="#22386a"/>')
    for i in range(5):
        for j in range(4):
            x, y = 130 + i * 62, 96 + j * 54 - i * 3
            pts = [(x + (13 if k % 2 == 0 else 5.5) * math.cos(-math.pi / 2 + k * math.pi / 5), y + (13 if k % 2 == 0 else 5.5) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)]
            b.append('<path d="M' + " L".join(f"{a:.1f} {c:.1f}" for a, c in pts) + ' Z" fill="#ffffff"/>')
    b.append('<path d="M82 60 Q290 20 480 60 T860 60 L860 528 Q670 568 480 528 T82 528 Z" fill="#000" opacity="0.08"/>')
    guardar("bandera_eeuu", "".join(b), w, h)


def monton_monedas():
    w, h = 900, 600
    r = random.Random(83)
    d = PLATA("mm_p")
    b = ['<ellipse cx="450" cy="560" rx="400" ry="24" fill="#000" opacity="0.45" filter="url(#blur8)"/>']
    pilas = [(160, 5), (300, 9), (450, 13), (600, 8), (740, 4)]
    for x, n in pilas:
        for k in range(n):
            y = 540 - k * 30
            b.append(f'<ellipse cx="{x + r.uniform(-6,6):.0f}" cy="{y}" rx="80" ry="24" fill="url(#mm_p)" stroke="#5a6270" stroke-width="4"/><path d="M{x-74} {y} v16 a74 22 0 0 0 148 0 v-16" fill="#8a92a0" stroke="#5a6270" stroke-width="4"/>')
        b.append(f'<ellipse cx="{x}" cy="{540 - (n-1)*30 - 2}" rx="50" ry="14" fill="none" stroke="#5a6270" stroke-width="3"/>')
    guardar("monton_monedas", "".join(b), w, h, d)


# ====================================================================== 03 · EL TURCO
def bg_salon_velas():
    """Salón de palacio del siglo XVIII a la luz de las velas."""
    r = random.Random(91)
    d = (lg("sv_p", (0, "#2a1420"), (0.6, "#4a2030"), (1, "#1a0c14")) + lg("sv_s", (0, "#3a2418"), (1, "#0e0806")) + rg("sv_l", (0, "#ffd88a", 0.8), (0.4, "#ff9a3a", 0.3), (1, "#ff9a3a", 0)) +
         lg("sv_c", (0, "#7a1c2a"), (1, "#3a0c14")))
    b = ['<rect width="1080" height="1920" fill="url(#sv_p)"/>']
    for x in range(40, 1080, 200):  # paneles de la pared
        b.append(f'<rect x="{x}" y="330" width="160" height="820" rx="10" fill="none" stroke="#b8861e" stroke-width="5" opacity="0.45"/><rect x="{x+18}" y="350" width="124" height="780" rx="6" fill="#5a2838" opacity="0.5"/>')
    b.append('<path d="M-20 0 L300 0 Q260 300 120 620 Q60 900 -20 1100 Z" fill="url(#sv_c)"/><path d="M1100 0 L780 0 Q820 300 960 620 Q1020 900 1100 1100 Z" fill="url(#sv_c)"/>')
    for k in range(6):
        b.append(f'<path d="M{40 + k*45} 0 Q{20 + k*36} 400 {-20 + k*26} {900 + k*30}" stroke="#2a0810" stroke-width="5" fill="none" opacity="0.5"/><path d="M{1040 - k*45} 0 Q{1060 - k*36} 400 {1100 - k*26} {900 + k*30}" stroke="#2a0810" stroke-width="5" fill="none" opacity="0.5"/>')
    for x in (250, 830):  # candelabros de pared
        b.append(f'<circle cx="{x}" cy="640" r="260" fill="url(#sv_l)"/><path d="M{x-50} 700 Q{x} 760 {x+50} 700 M{x} 730 L{x} 800" stroke="#b8861e" stroke-width="8" fill="none"/>')
        for dx in (-50, 0, 50):
            b.append(f'<rect x="{x+dx-7}" y="{650 if dx else 630}" width="14" height="60" fill="#f4ecd8"/><path d="M{x+dx} {650 if dx else 630} q-12 -22 0 -46 q12 24 0 46 Z" fill="#ffd27a"/>')
    b.append('<rect x="0" y="1300" width="1080" height="640" fill="url(#sv_s)"/>')
    for k in range(9):  # tarima en perspectiva
        b.append(f'<path d="M{540 + (k-4)*70} 1300 L{540 + (k-4)*330} 1940" stroke="#000" stroke-width="4" opacity="0.4"/>')
    b.append('<ellipse cx="540" cy="1520" rx="520" ry="120" fill="#ffb060" opacity="0.10" filter="url(#blur40)"/>')
    b.append(grano())
    guardar("bg_salon_velas", "".join(b), defs=d)


def _engranaje(cx, cy, R, n, color, eje="#1a1208"):
    pts = []
    for k in range(n * 4):
        a = 2 * math.pi * k / (n * 4)
        rad = R if k % 4 in (0, 1) else R * 0.82
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    s = f'<path d="M' + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + f' Z" fill="{color}" stroke="#3a2a10" stroke-width="{max(2, R*0.03):.0f}"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{R*0.55:.0f}" fill="none" stroke="#3a2a10" stroke-width="{max(2, R*0.04):.0f}" opacity="0.6"/>'
    for k in range(5):
        a = 2 * math.pi * k / 5
        s += f'<path d="M{cx} {cy} L{cx + R*0.6*math.cos(a):.0f} {cy + R*0.6*math.sin(a):.0f}" stroke="#3a2a10" stroke-width="{max(3, R*0.07):.0f}" opacity="0.7"/>'
    return s + f'<circle cx="{cx}" cy="{cy}" r="{R*0.16:.0f}" fill="{eje}"/>'


def engranaje(nombre="engranaje", color="url(#en_g)", n=14):
    d = ORO("en_g") + lg("en_c", (0, "#e8a868"), (0.5, "#b86a3a"), (1, "#7a3a1a"), x2=1, y2=1)
    guardar(nombre, _engranaje(300, 300, 280, n, color), 600, 600, d)


def _turbante(cx, cy, s=1.0):
    g = [f'<g transform="translate({cx} {cy}) scale({s})">',
         '<path d="M-120 20 Q-150 -90 -60 -150 Q0 -190 70 -150 Q150 -90 120 20 Q0 60 -120 20 Z" fill="#f4ecd8" stroke="#8a7a5a" stroke-width="5"/>']
    for k in range(6):
        g.append(f'<path d="M{-112 + k*8} {10 - k*22} Q0 {-20 - k*30} {112 - k*8} {4 - k*20}" stroke="#b8a888" stroke-width="5" fill="none"/>')
    g.append('<ellipse cx="0" cy="-100" rx="22" ry="28" fill="#c0392b" stroke="#ffd23f" stroke-width="5"/><path d="M0 -128 Q-10 -200 20 -230 Q10 -190 0 -128 Z" fill="#f4ecd8" stroke="#8a7a5a" stroke-width="3"/></g>')
    return "".join(g)


def _mueble(abierto=False, rayos=False, ox=0, oy=0):
    """Mueble del autómata: 1100×520 con tablero encima. abierto: puertas abiertas con engranajes. rayos: corte con la persona dentro."""
    b = [f'<g transform="translate({ox} {oy})">', '<ellipse cx="550" cy="540" rx="560" ry="26" fill="#000" opacity="0.5" filter="url(#blur8)"/>',
         '<rect x="20" y="60" width="1060" height="460" rx="10" fill="url(#mu_m)" stroke="#1a0e06" stroke-width="8"/>',
         '<rect x="0" y="30" width="1100" height="44" rx="8" fill="#6a4226" stroke="#1a0e06" stroke-width="6"/>']
    if rayos:
        b.append('<rect x="44" y="92" width="1012" height="404" rx="6" fill="#0a0604"/>')
        b.append(_engranaje(170, 220, 90, 12, "url(#en_g)") + _engranaje(290, 330, 70, 10, "url(#en_c)") + _engranaje(150, 400, 60, 9, "url(#en_g)"))
        # persona encogida (silueta con luz de vela), sentada, brazo extendido hacia una palanca
        b.append('<circle cx="760" cy="300" r="260" fill="url(#mu_v)"/>')
        b.append('<g fill="#1e2c4a" stroke="#7df9ff" stroke-width="5" stroke-linejoin="round">'
                 '<path d="M560 480 L560 400 Q600 300 700 290 Q760 290 780 350 L800 440 L900 440 L900 480 Z"/>'
                 '<path d="M700 290 Q640 250 560 240 L470 250 L470 280 L560 284 Q620 300 660 340 Z"/>'
                 '<circle cx="735" cy="232" r="62"/></g>')
        b.append('<path d="M470 264 L400 180 L400 100" stroke="#b8861e" stroke-width="10" fill="none"/><circle cx="400" cy="180" r="12" fill="#ffd23f"/>')
        b.append('<rect x="930" y="330" width="22" height="90" fill="#f4ecd8"/><path d="M941 330 q-16 -30 0 -62 q16 32 0 62 Z" fill="#ffd27a"/><rect x="910" y="418" width="62" height="14" rx="4" fill="#b8861e"/>')
        b.append('<rect x="540" y="470" width="380" height="18" rx="6" fill="#6a4226"/><circle cx="600" cy="494" r="12" fill="#8a8a8a"/><circle cx="860" cy="494" r="12" fill="#8a8a8a"/>')
    else:
        for i, x in enumerate((60, 400, 740)):
            if abierto:
                b.append(f'<rect x="{x}" y="100" width="300" height="290" fill="#0a0604"/>')
                r_ = random.Random(i + 5)
                for k in range(4):
                    b.append(_engranaje(x + 70 + (k % 2) * 150 + r_.uniform(-10, 10), 170 + (k // 2) * 140, r_.uniform(50, 78), r_.choice([9, 10, 12]), r_.choice(["url(#en_g)", "url(#en_c)"])))
                b.append(f'<path d="M{x} 100 L{x-70} 80 L{x-70} 410 L{x} 390 Z" fill="#5a3820" stroke="#1a0e06" stroke-width="5"/>')
            else:
                b.append(f'<rect x="{x}" y="100" width="300" height="290" rx="6" fill="#5a3820" stroke="#1a0e06" stroke-width="5"/><rect x="{x+24}" y="124" width="252" height="242" rx="4" fill="none" stroke="#3a2010" stroke-width="5"/><circle cx="{x+270}" cy="245" r="10" fill="#ffd23f"/>')
        b.append('<rect x="60" y="410" width="980" height="86" rx="6" fill="#5a3820" stroke="#1a0e06" stroke-width="5"/><circle cx="350" cy="453" r="10" fill="#ffd23f"/><circle cx="750" cy="453" r="10" fill="#ffd23f"/>')
    # tablero en perspectiva sobre el mueble
    b.append('<path d="M330 30 L770 30 L810 -40 L290 -40 Z" fill="#2a180c" stroke="#1a0e06" stroke-width="5"/>')
    for i in range(8):
        for j in range(4):
            u0, u1 = i / 8, (i + 1) / 8; v0, v1 = j / 4, (j + 1) / 4
            xa = lambda u, v: 340 - 40 * v + (420 + 80 * v) * u  # noqa: E731
            ya = lambda v: 24 - 58 * v  # noqa: E731
            if (i + j) % 2 == 0:
                b.append(f'<path d="M{xa(u0,v0):.0f} {ya(v0):.0f} L{xa(u1,v0):.0f} {ya(v0):.0f} L{xa(u1,v1):.0f} {ya(v1):.0f} L{xa(u0,v1):.0f} {ya(v1):.0f} Z" fill="#f0e0b8"/>')
    for x, c in [(380, "#f4ecd8"), (470, "#1a1208"), (560, "#f4ecd8"), (650, "#1a1208"), (720, "#f4ecd8")]:
        b.append(f'<path d="M{x-12} 14 Q{x-16} -20 {x-6} -34 Q{x} -52 {x+6} -34 Q{x+16} -20 {x+12} 14 Z" fill="{c}" stroke="#3a2a10" stroke-width="3"/><circle cx="{x}" cy="-44" r="9" fill="{c}" stroke="#3a2a10" stroke-width="3"/>')
    b.append('</g>')
    return "".join(b)


MU_DEFS = (lg("mu_m", (0, "#7a4a28"), (0.5, "#5a3218"), (1, "#2a160a")) + ORO("en_g") + lg("en_c", (0, "#e8a868"), (0.5, "#b86a3a"), (1, "#7a3a1a"), x2=1, y2=1) +
           rg("mu_v", (0, "#ffd88a", 0.55), (0.5, "#ff9a3a", 0.2), (1, "#ff9a3a", 0)) + lg("tu_r", (0, "#2a6a5a"), (1, "#0e2a26")) + lg("tu_p", (0, "#d8b08a"), (1, "#a87a58")))


def _turco_cuerpo(ox, oy, brazo=True):
    """Muñeco de madera (busto con túnica, turbante, bigote) sentado tras el mueble. Cara de muñeco, simétrica y sencilla."""
    b = [f'<g transform="translate({ox} {oy})">',
         '<path d="M-230 330 Q-250 60 -120 0 Q0 -40 120 0 Q250 60 230 330 Z" fill="url(#tu_r)" stroke="#06181a" stroke-width="7"/>',
         '<path d="M-120 0 Q0 90 120 0 L96 -30 Q0 30 -96 -30 Z" fill="#ffd23f" stroke="#7a5a10" stroke-width="4"/>',
         '<path d="M0 60 L0 330" stroke="#ffd23f" stroke-width="10"/>' + "".join(f'<circle cx="0" cy="{y}" r="12" fill="#ffd23f" stroke="#7a5a10" stroke-width="3"/>' for y in (110, 180, 250)),
         '<path d="M-150 60 Q-60 120 -30 330 M150 60 Q60 120 30 330" stroke="#0e2a26" stroke-width="5" fill="none" opacity="0.7"/>',
         # cuello y cabeza
         '<rect x="-36" y="-60" width="72" height="60" fill="url(#tu_p)"/>',
         '<path d="M-92 -180 Q-100 -70 -40 -44 Q0 -30 40 -44 Q100 -70 92 -180 Q0 -230 -92 -180 Z" fill="url(#tu_p)" stroke="#6a4a30" stroke-width="5"/>',
         # ojos simétricos, cejas, nariz, bigote y barbilla
         '<ellipse cx="-38" cy="-140" rx="18" ry="11" fill="#fffaf0" stroke="#3a2410" stroke-width="3"/><ellipse cx="38" cy="-140" rx="18" ry="11" fill="#fffaf0" stroke="#3a2410" stroke-width="3"/>',
         '<circle cx="-38" cy="-140" r="8" fill="#1a1208"/><circle cx="38" cy="-140" r="8" fill="#1a1208"/><circle cx="-35" cy="-143" r="2.5" fill="#fff"/><circle cx="41" cy="-143" r="2.5" fill="#fff"/>',
         '<path d="M-62 -164 Q-38 -178 -16 -162 M16 -162 Q38 -178 62 -164" stroke="#1a1208" stroke-width="8" fill="none" stroke-linecap="round"/>',
         '<path d="M0 -136 Q-12 -104 -8 -96 Q0 -90 8 -96 Q12 -104 0 -136 Z" fill="#b88a64"/>',
         '<path d="M0 -86 Q-30 -96 -62 -72 Q-36 -70 -20 -76 Q-8 -72 0 -78 Q8 -72 20 -76 Q36 -70 62 -72 Q30 -96 0 -86 Z" fill="#1a1208"/>',
         '<path d="M-14 -62 Q0 -56 14 -62" stroke="#6a3a2a" stroke-width="5" fill="none" stroke-linecap="round"/>',
         _turbante(0, -190, 1.0)]
    if brazo:  # brazo izquierdo apoyado, con pipa larga
        b.append('<path d="M-210 150 Q-300 240 -250 330 L-180 330 Q-200 250 -150 190 Z" fill="url(#tu_r)" stroke="#06181a" stroke-width="6"/><ellipse cx="-216" cy="336" rx="40" ry="22" fill="url(#tu_p)" stroke="#6a4a30" stroke-width="4"/>')
        b.append('<path d="M-216 330 L-420 250" stroke="#3a2410" stroke-width="9" stroke-linecap="round"/><rect x="-446" y="226" width="34" height="34" rx="8" fill="#6a4226" stroke="#1a0e06" stroke-width="4"/>')
    b.append('</g>')
    return "".join(b)


def turco(nombre="turco", abierto=False):
    w, h = 1200, 1250
    cuerpo = _turco_cuerpo(600, 430) + _mueble(abierto, False, 50, 700)
    guardar(nombre, cuerpo, w, h, MU_DEFS)


def turco_rayos():
    w, h = 1200, 1250
    guardar("turco_rayos", '<g opacity="0.55">' + _turco_cuerpo(600, 430) + '</g>' + _mueble(False, True, 50, 700), w, h, MU_DEFS)


def brazo_turco():
    """Brazo derecho del muñeco con la mano en pinza (se anima girando sobre el hombro)."""
    w, h = 700, 420
    b = ['<path d="M40 60 Q60 20 120 30 L520 200 Q560 220 540 262 Q520 290 480 276 L80 150 Q30 120 40 60 Z" fill="url(#tu_r)" stroke="#06181a" stroke-width="7"/>',
         '<path d="M470 190 Q500 200 520 250" stroke="#ffd23f" stroke-width="10" fill="none"/>',
         '<path d="M520 214 Q600 230 640 280 Q650 300 630 306 L600 290 L610 330 Q600 346 584 334 L560 290 Q520 280 506 262 Z" fill="url(#tu_p)" stroke="#6a4a30" stroke-width="5"/>']
    guardar("brazo_turco", "".join(b), w, h, MU_DEFS)


def pieza(nombre="pieza_caballo", color="#f4ecd8", borde="#3a2a10"):
    """Caballo de ajedrez (pieza Staunton vista de lado)."""
    w, h = 400, 620
    b = ['<ellipse cx="200" cy="590" rx="150" ry="16" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         f'<path d="M110 480 Q120 380 170 300 Q120 300 96 250 Q120 190 180 130 L170 70 L220 110 Q300 130 320 240 Q330 360 300 480 Z" fill="{color}" stroke="{borde}" stroke-width="8" stroke-linejoin="round"/>',
         f'<path d="M96 250 Q120 262 150 244" stroke="{borde}" stroke-width="6" fill="none"/><circle cx="196" cy="190" r="12" fill="{borde}"/>',
         f'<path d="M230 140 Q290 200 290 300 Q290 400 270 470" stroke="{borde}" stroke-width="5" fill="none" opacity="0.5"/>',
         f'<path d="M80 480 L330 480 L350 540 L60 540 Z" fill="{color}" stroke="{borde}" stroke-width="8" stroke-linejoin="round"/><rect x="40" y="540" width="330" height="40" rx="12" fill="{color}" stroke="{borde}" stroke-width="8"/>',
         '<path d="M130 440 Q140 360 190 290" stroke="#ffffff" stroke-width="10" fill="none" opacity="0.5" stroke-linecap="round"/>']
    guardar(nombre, "".join(b), w, h)


def rey(nombre="pieza_rey", color="#1a1208", borde="#b8861e"):
    w, h = 400, 700
    b = ['<ellipse cx="200" cy="670" rx="150" ry="16" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         f'<path d="M188 30 h24 v40 h40 v24 h-40 v50 h-24 v-50 h-40 v-24 h40 Z" fill="{color}" stroke="{borde}" stroke-width="6"/>',
         f'<path d="M130 150 Q200 120 270 150 L250 250 Q200 270 150 250 Z" fill="{color}" stroke="{borde}" stroke-width="7"/>',
         f'<path d="M150 250 Q170 400 110 560 L290 560 Q230 400 250 250 Z" fill="{color}" stroke="{borde}" stroke-width="7"/>',
         f'<path d="M120 280 L280 280" stroke="{borde}" stroke-width="12"/>',
         f'<path d="M80 560 L320 560 L340 620 L60 620 Z" fill="{color}" stroke="{borde}" stroke-width="7"/><rect x="40" y="620" width="320" height="40" rx="12" fill="{color}" stroke="{borde}" stroke-width="7"/>',
         '<path d="M172 300 Q180 420 140 540" stroke="#ffffff" stroke-width="8" fill="none" opacity="0.25" stroke-linecap="round"/>']
    guardar(nombre, "".join(b), w, h)


def tablero():
    """Tablero visto desde arriba, con algunas piezas como discos."""
    w = h = 1000
    d = lg("tb_m", (0, "#6a4226"), (1, "#2a160a"), x2=1, y2=1)
    b = ['<rect x="20" y="30" width="960" height="960" rx="14" fill="#000" opacity="0.4" filter="url(#blur8)"/>', '<rect x="10" y="10" width="980" height="980" rx="14" fill="url(#tb_m)" stroke="#1a0e06" stroke-width="8"/>']
    for i in range(8):
        for j in range(8):
            b.append(f'<rect x="{60 + i*110}" y="{60 + j*110}" width="110" height="110" fill="{"#f0e0b8" if (i + j) % 2 == 0 else "#5a3820"}"/>')
    b.append('<rect x="60" y="60" width="880" height="880" fill="none" stroke="#b8861e" stroke-width="6"/>')
    for (i, j, c) in [(0, 0, 0), (2, 0, 0), (4, 0, 0), (7, 0, 0), (1, 1, 0), (3, 1, 0), (5, 2, 0), (6, 1, 0), (0, 7, 1), (3, 7, 1), (4, 7, 1), (7, 7, 1), (2, 6, 1), (5, 6, 1), (6, 6, 1), (1, 5, 1)]:
        x, y = 115 + i * 110, 115 + j * 110
        col, bor = ("#1a1208", "#b8861e") if c == 0 else ("#f4ecd8", "#3a2a10")
        b.append(f'<circle cx="{x+4}" cy="{y+6}" r="36" fill="#000" opacity="0.35"/><circle cx="{x}" cy="{y}" r="36" fill="{col}" stroke="{bor}" stroke-width="5"/><circle cx="{x}" cy="{y}" r="18" fill="none" stroke="{bor}" stroke-width="4"/>')
    guardar("tablero", "".join(b), w, h, d)


def iman():
    w, h = 500, 560
    b = ['<path d="M70 40 L190 40 L190 300 Q190 370 250 370 Q310 370 310 300 L310 40 L430 40 L430 300 Q430 500 250 500 Q70 500 70 300 Z" fill="#c0392b" stroke="#4a0e08" stroke-width="8" stroke-linejoin="round"/>',
         '<rect x="70" y="40" width="120" height="100" fill="#e8eef8" stroke="#4a0e08" stroke-width="8"/><rect x="310" y="40" width="120" height="100" fill="#e8eef8" stroke="#4a0e08" stroke-width="8"/>',
         '<path d="M110 180 L110 300 Q110 440 250 456" stroke="#ffffff" stroke-width="12" fill="none" opacity="0.35" stroke-linecap="round"/>']
    for k, x in enumerate((90, 200, 310, 410)):
        b.append(f'<path d="M{x} 0 q-20 -30 0 -0" stroke="#7df9ff" stroke-width="0"/>')
    guardar("iman", "".join(b), w, h)


def llave_cuerda():
    w, h = 500, 500
    d = ORO("lc_g")
    b = ['<rect x="226" y="200" width="48" height="280" rx="10" fill="url(#lc_g)" stroke="#7a5a10" stroke-width="6"/>',
         '<path d="M250 230 Q120 230 100 130 Q90 50 170 50 Q240 60 250 160 Q260 60 330 50 Q410 50 400 130 Q380 230 250 230 Z" fill="url(#lc_g)" stroke="#7a5a10" stroke-width="7"/>',
         '<ellipse cx="170" cy="130" rx="34" ry="44" fill="#1a0e06" opacity="0.85"/><ellipse cx="330" cy="130" rx="34" ry="44" fill="#1a0e06" opacity="0.85"/>']
    guardar("llave_cuerda", "".join(b), w, h, d)


def _figura(nombre, cabeza, cuerpo, w=600, h=1000, luz="#ffb46a"):
    """Silueta histórica (sin cara) con luz de borde."""
    b = [f'<ellipse cx="{w/2}" cy="{h-30}" rx="{w*0.36}" ry="20" fill="#000" opacity="0.5" filter="url(#blur8)"/>',
         f'<g fill="#141a2c" stroke="{luz}" stroke-width="6" stroke-linejoin="round">{cuerpo}{cabeza}</g>']
    guardar(nombre, "".join(b), w, h)


def sil_napoleon():
    """Silueta con bicornio y mano en el chaleco (lectura inmediata sin dibujar la cara)."""
    cuerpo = ('<path d="M150 980 Q130 600 190 440 Q300 380 410 440 Q470 600 450 980 Z"/>'
              '<path d="M190 440 L150 480 L160 700 L210 690 Z M410 440 L450 480 L440 700 L390 690 Z"/>')
    cabeza = ('<path d="M250 300 Q300 270 350 300 L356 400 Q300 430 244 400 Z"/>'
              '<path d="M110 270 Q300 110 490 270 Q400 250 300 256 Q200 250 110 270 Z"/><path d="M110 270 Q300 330 490 270 Q400 300 300 296 Q200 300 110 270 Z"/>')
    _figura("sil_napoleon", cabeza, cuerpo + '<path d="M260 620 Q330 600 350 660" stroke="#ffb46a" stroke-width="8" fill="none"/>'
            '<path d="M240 460 L300 520 L360 460" stroke="#ffd23f" stroke-width="8" fill="none"/>' + "".join(f'<circle cx="300" cy="{y}" r="9" fill="#ffd23f" stroke="none"/>' for y in (560, 720, 800)))


def sil_franklin():
    """Silueta con melena larga, frente despejada y gafas redondas (solo las gafas brillan)."""
    cuerpo = '<path d="M140 980 Q120 620 180 450 Q300 390 420 450 Q480 620 460 980 Z"/><path d="M240 450 L300 560 L360 450 Z" fill="#e8e0d0" stroke="#ffb46a"/>'
    cabeza = ('<path d="M214 200 Q300 130 386 200 Q410 300 380 380 Q300 440 220 380 Q190 300 214 200 Z"/>'
              '<path d="M214 210 Q170 300 190 440 L236 430 Q220 320 236 250 Z M386 210 Q430 300 410 440 L364 430 Q380 320 364 250 Z"/>')
    gafas = '<circle cx="262" cy="290" r="28" fill="#7df9ff" opacity="0.25" stroke="#7df9ff" stroke-width="6"/><circle cx="338" cy="290" r="28" fill="#7df9ff" opacity="0.25" stroke="#7df9ff" stroke-width="6"/><path d="M290 290 L310 290" stroke="#7df9ff" stroke-width="6"/>'
    _figura("sil_franklin", cabeza + gafas, cuerpo, luz="#7df9ff")


def sil_escritor():
    """Escritor de espaldas inclinado sobre la mesa (silueta con pelo oscuro), para Poe sin dibujar su cara."""
    cuerpo = '<path d="M100 980 Q80 640 170 500 Q300 440 430 500 Q520 640 500 980 Z"/><path d="M430 520 Q540 600 560 760 L500 780 Q480 660 410 600 Z"/>'
    cabeza = '<path d="M210 280 Q220 180 300 170 Q390 180 392 290 Q400 400 300 430 Q200 400 210 280 Z"/><path d="M204 300 Q180 200 260 160 Q340 130 400 190 Q420 250 396 310 Q380 220 300 210 Q230 220 204 300 Z"/>'
    _figura("sil_escritor", cabeza, cuerpo, luz="#c8a0ff")


def publico():
    """Fila de espectadores de espaldas con pelucas y sombreros del XVIII (siluetas)."""
    w, h = 1200, 520
    r = random.Random(95)
    b = []
    for k in range(9):
        x = 60 + k * 135 + r.uniform(-14, 14); s = r.uniform(0.9, 1.15)
        tipo = k % 3
        g = [f'<g transform="translate({x:.0f} 520) scale({s:.2f})" fill="#0e1220" stroke="#ffb46a" stroke-width="4" stroke-linejoin="round">',
             '<path d="M-90 0 Q-90 -190 0 -220 Q90 -190 90 0 Z"/><circle cx="0" cy="-270" r="52"/>']
        if tipo == 0: g.append('<path d="M-60 -290 Q0 -380 60 -290 Q70 -230 50 -210 Q0 -250 -50 -210 Q-70 -230 -60 -290 Z"/>')
        if tipo == 1: g.append('<path d="M-90 -300 Q0 -360 90 -300 Q40 -290 0 -292 Q-40 -290 -90 -300 Z"/><path d="M-50 -310 Q0 -390 50 -310 Z"/>')
        if tipo == 2: g.append('<path d="M-56 -300 Q-60 -420 0 -430 Q60 -420 56 -300 Z"/>')
        g.append('</g>')
        b.append("".join(g))
    guardar("publico", "".join(b), w, h)


def chip_ia():
    w = h = 700
    d = lg("ch_g", (0, "#2a3450"), (1, "#0e1424")) + rg("ch_l", (0, "#7df9ff", 0.9), (0.5, "#3fb8ff", 0.35), (1, "#3fb8ff", 0))
    b = ['<circle cx="350" cy="350" r="340" fill="url(#ch_l)" opacity="0.6"/>']
    for k in range(7):
        p = 170 + k * 60
        b += [f'<rect x="{p-9}" y="60" width="18" height="90" rx="6" fill="#b8c0d0"/><rect x="{p-9}" y="550" width="18" height="90" rx="6" fill="#b8c0d0"/>',
              f'<rect x="60" y="{p-9}" width="90" height="18" rx="6" fill="#b8c0d0"/><rect x="550" y="{p-9}" width="90" height="18" rx="6" fill="#b8c0d0"/>']
    b.append('<rect x="130" y="130" width="440" height="440" rx="36" fill="url(#ch_g)" stroke="#7df9ff" stroke-width="8"/><rect x="190" y="190" width="320" height="320" rx="20" fill="none" stroke="#3fb8ff" stroke-width="4" opacity="0.7"/>')
    b.append(_texto(350, 400, "IA", 170, "#7df9ff", 900))
    guardar("chip_ia", "".join(b), w, h, d)


def llamas():
    """Cortina de llamas (para el incendio), se anima subiendo."""
    w, h = 1200, 1000
    r = random.Random(97)
    d = lg("ll_1", (0, "#ffd23f"), (0.5, "#ff7a1e"), (1, "#c0392b")) + lg("ll_2", (0, "#fff6c0"), (1, "#ffb02e"))
    b = []
    for capa, (col, base, alto) in enumerate([("#8a1c10", 1000, 760), ("url(#ll_1)", 1000, 640), ("url(#ll_2)", 1000, 420)]):
        pts = [(-20, 1020)]
        for x in range(-20, 1240, 70):
            pts.append((x, base - alto * r.uniform(0.35, 1.0)))
            pts.append((x + 35, base - alto * r.uniform(0.1, 0.4)))
        pts.append((1220, 1020))
        dd = f"M{pts[0][0]} {pts[0][1]} " + " ".join(f"Q{pts[i][0]:.0f} {pts[i][1]:.0f} {pts[i+1][0]:.0f} {pts[i+1][1]:.0f}" for i in range(1, len(pts) - 1, 2)) + " Z"
        b.append(f'<path d="{dd}" fill="{col}" opacity="{0.9 if capa else 0.7}"/>')
    guardar("llamas", "".join(b), w, h, d)


def generar(dirsvg):
    ilus_nino.generar(dirsvg)   # mapa, Tierra, mares, nubes, termómetros, hoja de calendario base…
    t18 = _mod("ilus_tarde_1118b", os.path.join(RAIZ, "lotes", "2026-11-18-tarde", "generadores", "ilus_tarde.py"))
    m02 = _mod("ilus_02_1118", os.path.join(RAIZ, "lotes", "2026-11-18-manana", "generadores", "ilus_02.py"))
    ilus.OUT = dirsvg
    m02.pluma()
    for n, t, c in [("hoja_1520", "1520", "#8a6a3a"), ("hoja_1857", "1857", "#22386a"), ("hoja_1770", "1770", "#7a1c2a"), ("hoja_1854", "1854", "#c0392b")]:
        t18.hoja_calendario(n, t, c)
    # 02
    billete(); talero(); real_de_a_ocho(); moneda_oro(); bg_valle(); vagoneta(); galeon(); bg_puerto(); bg_escritorio(); pergamino(); pergamino("pergamino_vacio", False)
    letra("letra_p", "p"); letra("letra_s", "s"); letra("signo_peso", "$", "#ffd23f", 560, False); letra("signo_peso_tinta", "$", "#2a1808", 560, False)
    tricornio(); bandera_eeuu(); monton_monedas()
    # 03
    bg_salon_velas(); engranaje(); engranaje("engranaje_cobre", "url(#en_c)", 10); turco(); turco("turco_abierto", True); turco_rayos(); brazo_turco()
    pieza(); rey(); tablero(); iman(); llave_cuerda(); sil_napoleon(); sil_franklin(); sil_escritor(); publico(); chip_ia(); llamas()
    return dirsvg


if __name__ == "__main__":
    generar(sys.argv[1])
    print("SVG en", sys.argv[1])
