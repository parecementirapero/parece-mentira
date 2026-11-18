"""Ilustraciones del vídeo 01 del lote 2026-11-18-manana («Un día duraba dieciocho horas»).
Uso: python3 ilus_01.py DIR_SVG   (semillas fijas). Ladrillos de motor/biblioteca/ilus.py. Agente 08:00 (Nico)."""
import math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano, _estrellas_ricas  # noqa: E402,F401


def _onda(r, x0, x1, y, amp, pasos=14):
    pts = []
    for i in range(pasos + 1):
        x = x0 + (x1 - x0) * i / pasos
        pts.append((x, y + r.uniform(-amp, amp)))
    return pts


def _banda(r, y0, y1, color, amp=10, op=1.0):
    a = _onda(r, -40, 1120, y0, amp)
    b = _onda(r, -40, 1120, y1, amp)[::-1]
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in a + b) + " Z"
    return f'<path d="{d}" fill="{color}" opacity="{op}"/>'


# ------------------------------------------------------------------ Tierra primitiva (hace 1.400 millones de años)
def bg_tierra_antigua():
    r = random.Random(11)
    d = (lg("ta_cielo", (0, "#1a0f2e"), (0.35, "#5a2448"), (0.62, "#d8643a"), (0.72, "#ffb25a"), (1, "#3a1a10")) +
         rg("ta_sol", (0, "#fff2c0", 1), (0.3, "#ffb25a", 0.6), (1, "#ff6a2a", 0)) +
         lg("ta_mar", (0, "#ff9a5a"), (0.15, "#7a3a40"), (1, "#1a1424")) + lg("ta_roca", (0, "#4a2a22"), (1, "#140a08")) +
         rg("ta_lava", (0, "#ffd06a", 1), (1, "#ff3a1a", 0)))
    b = ['<rect width="1080" height="1920" fill="url(#ta_cielo)"/>', _estrellas_ricas(4, 120, 12, 3, banda=None).replace("<g", "<g opacity=\"0.5\"", 1),
         '<ellipse cx="540" cy="1230" rx="900" ry="380" fill="url(#ta_sol)"/>']
    # volcanes lejanos con humo y brillo de lava
    for cx, h, w in [(160, 330, 420), (560, 240, 360), (930, 380, 460)]:
        b.append(f'<path d="M{cx-w/2:.0f} 1300 L{cx-40:.0f} {1300-h:.0f} L{cx+40:.0f} {1300-h:.0f} L{cx+w/2:.0f} 1300 Z" fill="#3a1e2a" opacity="0.85"/>')
        b.append(f'<ellipse cx="{cx}" cy="{1300-h}" rx="60" ry="26" fill="url(#ta_lava)" opacity="0.8"/>')
        for k in range(5):
            b.append(f'<ellipse cx="{cx + r.uniform(-60,80):.0f}" cy="{1300-h-60-k*70:.0f}" rx="{70+k*30}" ry="{40+k*15}" fill="#5a3a44" opacity="{0.35-k*0.05:.2f}" filter="url(#blur20)"/>')
    b.append('<rect x="0" y="1290" width="1080" height="640" fill="url(#ta_mar)"/>')
    for k in range(40):  # brillos en el agua
        y = r.uniform(1300, 1600); w = r.uniform(30, 160)
        b.append(f'<rect x="{r.uniform(0,1080):.0f}" y="{y:.0f}" width="{w:.0f}" height="4" fill="#ffd8a0" opacity="{r.uniform(0.15,0.5):.2f}"/>')
    # estromatolitos (montículos de microbios con capas): lo único vivo
    for cx, cy, s in [(180, 1560, 1.0), (420, 1600, 0.7), (760, 1580, 1.2), (980, 1620, 0.8), (600, 1660, 0.6)]:
        rx, ry = 110 * s, 70 * s
        b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx:.0f}" ry="{ry:.0f}" fill="#6a4a3a"/>')
        for j in range(4):
            b.append(f'<path d="M{cx-rx*(0.9-j*0.18):.0f} {cy+ry*0.2:.0f} Q{cx} {cy-ry*(0.9-j*0.2):.0f} {cx+rx*(0.9-j*0.18):.0f} {cy+ry*0.2:.0f}" stroke="#a87a5a" stroke-width="4" fill="none" opacity="0.6"/>')
        b.append(f'<ellipse cx="{cx-rx*0.3:.0f}" cy="{cy-ry*0.5:.0f}" rx="{rx*0.4:.0f}" ry="{ry*0.2:.0f}" fill="#ffc890" opacity="0.35"/>')
    # rocas en primer plano
    b.append('<path d="M0 1720 L120 1680 L260 1710 L380 1690 L520 1740 L700 1700 L860 1730 L1080 1690 L1080 1920 L0 1920 Z" fill="url(#ta_roca)"/>')
    for k in range(25):
        x = r.uniform(0, 1080); y = r.uniform(1730, 1900)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(15,50):.0f}" ry="{r.uniform(8,20):.0f}" fill="#2a1612"/><ellipse cx="{x-6:.0f}" cy="{y-6:.0f}" rx="{r.uniform(8,20):.0f}" ry="4" fill="#ff9a5a" opacity="0.3"/>')
    b.append(grano())
    guardar("bg_tierra_antigua", "".join(b), defs=d)


# ------------------------------------------------------------------ rocas con capas (norte de China)
CAPAS = ["#d9b98a", "#8a6a52", "#c99a6a", "#5a4a42", "#e6cfa0", "#7a5a48", "#b88a5a", "#4a3a36"]


def acantilado():
    r = random.Random(5)
    d = lg("ac_cielo", (0, "#7ab8e8"), (1, "#f2dcb0")) + lg("ac_sombra", (0, "#00000000"), (1, "#00000088"))
    b = ['<rect width="1080" height="1920" fill="url(#ac_cielo)"/>',
         '<path d="M0 520 L200 470 L420 500 L600 440 L820 480 L1080 430 L1080 700 L0 700 Z" fill="#9aa8b8" opacity="0.6"/>']
    y = 560
    k = 0
    while y < 1700:
        # ritmo: grupos de capas finas y una gruesa (como los ciclos del clima)
        gruesa = (k % 5 == 4)
        h = r.uniform(46, 70) if gruesa else r.uniform(14, 30)
        b.append(_banda(r, y, y + h + 4, CAPAS[k % len(CAPAS)], amp=6))
        y += h; k += 1
    b.append('<rect x="0" y="560" width="1080" height="1140" fill="url(#ac_sombra)" opacity="0.5"/>')
    for _ in range(18):  # grietas
        x = r.uniform(40, 1040); y0 = r.uniform(600, 1500)
        b.append(f'<path d="M{x:.0f} {y0:.0f} l{r.uniform(-20,20):.0f} {r.uniform(40,120):.0f} l{r.uniform(-20,20):.0f} {r.uniform(30,90):.0f}" stroke="#2a1c14" stroke-width="3" fill="none" opacity="0.5"/>')
    b.append('<path d="M0 1690 Q300 1650 540 1700 T1080 1680 L1080 1920 L0 1920 Z" fill="#6a5040"/>')
    for _ in range(40):
        x = r.uniform(0, 1080); y = r.uniform(1700, 1900)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(10,40):.0f}" ry="{r.uniform(6,16):.0f}" fill="#4a3628"/>')
    b.append(grano())
    guardar("acantilado", "".join(b), defs=d)


def capas_cerca():
    r = random.Random(8)
    b = []
    y = -40; k = 0
    while y < 1960:
        gruesa = (k % 5 == 4)
        h = r.uniform(110, 150) if gruesa else r.uniform(34, 60)
        b.append(_banda(r, y, y + h + 6, CAPAS[k % len(CAPAS)], amp=14))
        for _ in range(int(h / 6)):  # granos
            b.append(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(y, y+h):.0f}" r="{r.uniform(1.5,4):.1f}" fill="#000" opacity="0.15"/>')
        y += h; k += 1
    b.append(grano())
    guardar("capas_cerca", "".join(b))


def tronco():
    w = h = 900
    r = random.Random(3)
    d = rg("tr_c", (0, "#f2d29a", 1), (1, "#c8945a", 1))
    b = ['<ellipse cx="460" cy="470" rx="440" ry="430" fill="#000" opacity="0.35" filter="url(#blur20)"/>',
         '<circle cx="450" cy="450" r="430" fill="#5a3a22"/>',
         *[f'<path d="M{450+430*math.cos(a):.0f} {450+430*math.sin(a):.0f} L{450+405*math.cos(a+0.05):.0f} {450+405*math.sin(a+0.05):.0f}" stroke="#2a1a0e" stroke-width="10"/>' for a in [i * 0.21 for i in range(30)]],
         '<circle cx="450" cy="450" r="395" fill="url(#tr_c)"/>']
    rr = 380
    while rr > 20:
        b.append(f'<circle cx="{450+r.uniform(-4,4):.0f}" cy="{450+r.uniform(-4,4):.0f}" r="{rr:.0f}" fill="none" stroke="#a8743e" stroke-width="{r.uniform(2,5):.1f}" opacity="0.8"/>')
        rr -= r.uniform(16, 30)
    b.append('<path d="M450 450 L700 160" stroke="#6a4424" stroke-width="5" opacity="0.6"/>')
    guardar("tronco", "".join(b), w, h, d)


def martillo():
    w, h = 700, 300
    d = lg("ma_m", (0, "#d8dde6"), (1, "#5a6272")) + lg("ma_p", (0, "#c8784a"), (1, "#6a3418"))
    b = ['<rect x="80" y="130" width="560" height="44" rx="18" fill="url(#ma_p)"/>',
         '<path d="M20 60 L200 60 L220 90 L220 200 L200 230 L60 230 L20 200 Z" fill="url(#ma_m)"/>',
         '<path d="M30 70 L190 70" stroke="#ffffff" stroke-width="6" opacity="0.6"/>']
    guardar("martillo", "".join(b), w, h, d)


def _silueta(trazos, extra, w, h, nombre, borde="#ffb46a"):
    """Figura a contraluz: miembros como trazos redondeados (sin cara) y halo cálido detrás."""
    cuerpo = "".join(f'<path d="{d}" stroke-width="{g}" stroke-linecap="round" stroke-linejoin="round" fill="none"/>' for d, g in trazos) + extra
    b = [f'<g stroke="{borde}" fill="{borde}" transform="translate(-10 -6)" opacity="0.9" filter="url(#blur8)">{cuerpo}</g>',
         f'<g stroke="#0e0a14" fill="#0e0a14">{cuerpo}</g>',
         f'<ellipse cx="{w/2:.0f}" cy="{h-20}" rx="{w*0.35:.0f}" ry="18" fill="#000" opacity="0.35" filter="url(#blur8)"/>']
    guardar(nombre, "".join(b), w, h)


def geologo_lupa():
    """Silueta agachada (rodilla en el suelo) mirando la roca con una lupa."""
    w, h = 700, 900
    tr = [("M300 360 Q330 470 360 560", 120),            # torso inclinado
          ("M360 560 L250 650 L250 840", 62),             # pierna con rodilla en el suelo
          ("M370 570 L470 690 L440 850", 62),
          ("M330 400 L450 480 L560 470", 46)]              # brazo hacia la roca
    extra = ('<circle cx="285" cy="270" r="78"/><path d="M190 255 Q285 160 380 255 L410 272 L170 272 Z"/>'
             '<circle cx="600" cy="460" r="52" fill="none" stroke-width="14"/><path d="M560 470 L520 480" stroke-width="16"/>')
    _silueta(tr, extra, w, h, "geologo_lupa")


def geologo_libreta():
    w, h = 600, 1100
    tr = [("M300 280 L300 600", 140), ("M275 640 L250 1040", 66), ("M325 640 L360 1040", 66),
          ("M350 330 L430 450 L470 400", 44), ("M250 330 L200 500", 44)]
    extra = ('<circle cx="300" cy="175" r="78"/><path d="M205 160 Q300 70 395 160 L425 178 L175 178 Z"/>'
             '<rect x="440" y="340" width="130" height="100" rx="8" transform="rotate(-15 505 390)"/>')
    _silueta(tr, extra, w, h, "geologo_libreta")


# ------------------------------------------------------------------ mar antiguo y corales
def bg_mar_antiguo():
    r = random.Random(9)
    d = lg("ma_agua", (0, "#4ac8d8"), (0.4, "#167a96"), (1, "#062236")) + lg("ma_rayo", (0, "#ffffff88"), (1, "#ffffff00"))
    b = ['<rect width="1080" height="1920" fill="url(#ma_agua)"/>']
    for _ in range(7):
        x = r.uniform(0, 1080)
        b.append(f'<path d="M{x:.0f} -20 L{x+90:.0f} -20 L{x+260:.0f} 1500 L{x+120:.0f} 1500 Z" fill="url(#ma_rayo)" opacity="0.25"/>')
    b.append('<path d="M0 1560 Q270 1500 540 1560 T1080 1540 L1080 1920 L0 1920 Z" fill="#c8b07a"/>')
    b.append('<path d="M0 1600 Q270 1560 540 1610 T1080 1600" stroke="#e8d4a0" stroke-width="8" fill="none" opacity="0.5"/>')
    for _ in range(60):
        b.append(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(1580,1910):.0f}" r="{r.uniform(2,6):.0f}" fill="#8a7448"/>')
    for x in (90, 250, 880, 1010):  # crinoideos (lirios de mar) en silueta
        hh = r.uniform(300, 480)
        b.append(f'<path d="M{x} 1560 Q{x+30} {1560-hh/2:.0f} {x+10} {1560-hh:.0f}" stroke="#0e3a4a" stroke-width="10" fill="none"/>')
        for a in range(-60, 61, 20):
            ra = math.radians(a - 90)
            b.append(f'<path d="M{x+10} {1560-hh:.0f} q{60*math.cos(ra):.0f} {60*math.sin(ra):.0f} {40*math.cos(ra+0.6):.0f} {90*math.sin(ra+0.3):.0f}" stroke="#0e3a4a" stroke-width="7" fill="none"/>')
    for _ in range(50):
        b.append(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1500):.0f}" r="{r.uniform(1.5,4):.1f}" fill="#d8ffff" opacity="{r.uniform(0.2,0.6):.2f}"/>')
    b.append(grano())
    guardar("bg_mar_antiguo", "".join(b), defs=d)


def coral_vivo():
    """Coral rugoso (en forma de cuerno) vivo, con su pólipo abierto arriba."""
    w, h = 600, 900
    r = random.Random(4)
    d = lg("cv_c", (0, "#ff9a7a"), (1, "#8a3a3a"), x2=1, y2=0)
    b = ['<ellipse cx="300" cy="860" rx="160" ry="24" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<path d="M290 860 Q170 700 180 420 L420 420 Q430 700 310 860 Z" fill="url(#cv_c)"/>']
    for k in range(9):
        y = 450 + k * 45
        b.append(f'<path d="M{185+k*5} {y} Q300 {y+18} {415-k*5} {y}" stroke="#5a2020" stroke-width="3" fill="none" opacity="0.5"/>')
    b.append('<ellipse cx="300" cy="420" rx="122" ry="34" fill="#5a1e2a"/>')
    for a in range(0, 360, 20):
        ra = math.radians(a)
        x0, y0 = 300 + 100 * math.cos(ra), 420 + 26 * math.sin(ra)
        L = r.uniform(120, 200)
        b.append(f'<path d="M{x0:.0f} {y0:.0f} q{40*math.cos(ra):.0f} {-L*0.6:.0f} {70*math.cos(ra):.0f} {-L:.0f}" stroke="#ffd0e0" stroke-width="12" stroke-linecap="round" fill="none" opacity="0.9"/>')
        b.append(f'<circle cx="{x0+70*math.cos(ra):.0f}" cy="{y0-L:.0f}" r="9" fill="#ffffff"/>')
    b.append('<path d="M200 460 Q210 700 290 840" stroke="#ffd0b0" stroke-width="10" fill="none" opacity="0.4"/>')
    guardar("coral_vivo", "".join(b), w, h, d)


def coral_fosil():
    w, h = 800, 800
    d = lg("cf_c", (0, "#e6d2a8"), (1, "#8a744e"), x2=1, y2=1) + lg("cf_r", (0, "#6a6a72"), (1, "#3a3a42"))
    b = ['<path d="M40 620 Q200 520 400 560 T760 600 L780 800 L20 800 Z" fill="url(#cf_r)"/>',
         '<path d="M150 640 Q120 330 330 150 L520 240 Q330 400 330 640 Z" fill="url(#cf_c)"/>',
         '<ellipse cx="425" cy="195" rx="105" ry="45" transform="rotate(25 425 195)" fill="#bfa478"/>',
         '<ellipse cx="425" cy="195" rx="70" ry="26" transform="rotate(25 425 195)" fill="#8a6a44"/>']
    for k in range(22):  # crestas de crecimiento
        f = k / 22
        x0 = 150 + (330 - 150) * f * 0.2 + 175 * f
        b.append(f'<path d="M{150+150*f:.0f} {640-470*f:.0f} Q{240+60*f:.0f} {600-430*f:.0f} {330+150*f:.0f} {640-420*f:.0f}" stroke="#6a5434" stroke-width="{4 if k % 4 == 0 else 2}" fill="none" opacity="0.7"/>')
    b.append('<path d="M170 600 Q160 380 320 190" stroke="#fff4d8" stroke-width="10" fill="none" opacity="0.4"/>')
    guardar("coral_fosil", "".join(b), w, h, d)


def coral_superficie():
    """Primer plano de la pared del coral fósil: crestas anchas (años); las rayas diarias se dibujan encima en el vídeo."""
    r = random.Random(12)
    d = lg("cs_f", (0, "#d8c49a"), (1, "#a08458"), x2=1, y2=0)
    b = ['<rect width="1080" height="1920" fill="url(#cs_f)"/>']
    for k in range(5):
        y = 200 + k * 380
        b.append(f'<path d="M-20 {y} Q540 {y+40} 1100 {y}" stroke="#5a4428" stroke-width="18" fill="none" opacity="0.55"/>')
        b.append(f'<path d="M-20 {y+12} Q540 {y+52} 1100 {y+12}" stroke="#fff0d0" stroke-width="5" fill="none" opacity="0.35"/>')
    for _ in range(500):
        b.append(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,1920):.0f}" r="{r.uniform(1.5,4):.1f}" fill="#4a3820" opacity="{r.uniform(0.1,0.3):.2f}"/>')
    b.append(grano())
    guardar("coral_superficie", "".join(b), defs=d)


# ------------------------------------------------------------------ freno, marea
def disco_freno():
    w = h = 900
    d = rg("df_c", (0, "#e8ecf2", 1), (0.7, "#9aa2b0", 1), (1, "#4a5260", 1))
    b = ['<circle cx="450" cy="450" r="420" fill="url(#df_c)"/>', '<circle cx="450" cy="450" r="160" fill="#3a404c"/>',
         *[f'<circle cx="{450+300*math.cos(math.radians(a)):.0f}" cy="{450+300*math.sin(math.radians(a)):.0f}" r="22" fill="#2a2e38"/>' for a in range(0, 360, 30)],
         *[f'<circle cx="{450+90*math.cos(math.radians(a)):.0f}" cy="{450+90*math.sin(math.radians(a)):.0f}" r="20" fill="#c8ccd6"/>' for a in range(0, 360, 72)],
         '<path d="M120 300 A360 360 0 0 1 300 120" stroke="#ffffff" stroke-width="14" fill="none" opacity="0.5"/>']
    guardar("disco_freno", "".join(b), w, h, d)
    w2, h2 = 340, 520
    d2 = lg("pz_c", (0, "#ff4a3a"), (1, "#8a1a12"), x2=1, y2=0)
    guardar("pinza_freno", '<rect x="20" y="20" width="300" height="480" rx="60" fill="url(#pz_c)"/><rect x="60" y="80" width="40" height="360" rx="12" fill="#2a2a2a"/>'
            '<path d="M60 60 Q170 30 280 60" stroke="#ffb0a0" stroke-width="10" fill="none" opacity="0.6"/>', w2, h2, d2)


def playa():
    r = random.Random(14)
    d = lg("pl_cielo", (0, "#2a4a8a"), (0.7, "#e8a070"), (1, "#f4c890")) + lg("pl_arena", (0, "#e8c890"), (1, "#a8804a"))
    b = ['<rect width="1080" height="1920" fill="url(#pl_cielo)"/>',
         '<path d="M0 1100 L1080 1100 L1080 1920 L0 1920 Z" fill="url(#pl_arena)"/>',
         *[f'<ellipse cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(1150,1900):.0f}" rx="{r.uniform(10,30):.0f}" ry="4" fill="#8a6a3a" opacity="0.4"/>' for _ in range(60)],
         '<path d="M700 1300 L760 1180 L800 1300 Z" fill="#5a4030"/><path d="M180 1500 L240 1420 L300 1500 Z" fill="#5a4030"/>',
         grano()]
    guardar("playa", "".join(b), defs=d)
    d2 = lg("mf_a", (0, "#4ab8e0"), (0.1, "#1a6aa8"), (1, "#0a2a4a"))
    guardar("mar_frente", '<rect y="40" width="1080" height="1300" fill="url(#mf_a)"/>'
            '<path d="M0 50 C120 10 240 90 360 50 C480 10 600 90 720 50 C840 10 960 90 1080 50 L1080 90 L0 90 Z" fill="#ffffff" opacity="0.8"/>'
            + "".join(f'<rect x="{r.uniform(0,1000):.0f}" y="{r.uniform(150,1200):.0f}" width="{r.uniform(40,140):.0f}" height="5" fill="#bfe9ff" opacity="0.35"/>' for _ in range(40)),
            1080, 1340, d2)


# ------------------------------------------------------------------ Babilonia
def bg_babilonia():
    r = random.Random(17)
    d = lg("bb_cielo", (0, "#06081a"), (0.6, "#1a1a40"), (1, "#5a3a3a")) + lg("bb_suelo", (0, "#5a3a24"), (1, "#1a0e08"))
    b = ['<rect width="1080" height="1920" fill="url(#bb_cielo)"/>', _estrellas_ricas(21, 300, 30, 8),
         '<path d="M0 1450 L1080 1450 L1080 1920 L0 1920 Z" fill="url(#bb_suelo)"/>']
    # zigurat escalonado
    for k, (wz, hz) in enumerate([(760, 120), (580, 110), (420, 100), (260, 90)]):
        y = 1450 - sum(h for _, h in [(760, 120), (580, 110), (420, 100), (260, 90)][:k + 1])
        b.append(f'<rect x="{540-wz/2:.0f}" y="{y}" width="{wz}" height="{hz+2}" fill="#2a1a18"/>')
        b.append(f'<rect x="{540-wz/2:.0f}" y="{y}" width="{wz}" height="6" fill="#c8845a" opacity="0.5"/>')
    b.append('<path d="M500 1450 L520 1090 L560 1090 L580 1450 Z" fill="#3a2420"/>')
    for x in (90, 180, 930, 1010):  # palmeras
        b.append(f'<path d="M{x} 1460 Q{x+10} 1300 {x-5} 1200" stroke="#120a08" stroke-width="14" fill="none"/>')
        for a in range(0, 360, 45):
            ra = math.radians(a)
            b.append(f'<path d="M{x-5} 1200 q{60*math.cos(ra):.0f} {-30+40*math.sin(ra):.0f} {110*math.cos(ra):.0f} {30+60*abs(math.sin(ra)):.0f}" stroke="#120a08" stroke-width="10" fill="none"/>')
    b.append(grano())
    guardar("bg_babilonia", "".join(b), defs=d)


def tablilla():
    w, h = 700, 900
    r = random.Random(23)
    d = lg("tb_c", (0, "#d8a878"), (1, "#8a5a36"), x2=1, y2=1)
    b = ['<rect x="60" y="70" width="580" height="780" rx="70" fill="#000" opacity="0.4" filter="url(#blur20)"/>',
         '<rect x="40" y="40" width="580" height="780" rx="70" fill="url(#tb_c)"/>',
         '<path d="M90 80 Q330 50 580 80" stroke="#ffe0b8" stroke-width="10" fill="none" opacity="0.5"/>']
    for fila in range(11):
        y = 120 + fila * 62
        b.append(f'<path d="M80 {y+40} L580 {y+40}" stroke="#6a4224" stroke-width="2" opacity="0.4"/>')
        x = 100
        while x < 560:
            s = r.uniform(0.7, 1.2)
            if r.random() < 0.6:
                b.append(f'<path d="M{x} {y} l{14*s:.0f} {8*s:.0f} l{-14*s:.0f} {8*s:.0f} Z M{x+14*s:.0f} {y+8*s:.0f} l{18*s:.0f} 0" stroke="#4a2a16" stroke-width="4" fill="#5a341a"/>')
            else:
                b.append(f'<path d="M{x} {y} l{8*s:.0f} {28*s:.0f} l{8*s:.0f} {-28*s:.0f} Z" fill="#4a2a16"/>')
            x += r.uniform(30, 52)
    b.append('<circle cx="500" cy="210" r="46" fill="none" stroke="#4a2a16" stroke-width="7"/><path d="M470 210 A30 30 0 0 0 530 210" fill="#4a2a16"/>')
    guardar("tablilla", "".join(b), w, h, d)
    guardar("estilete", '<path d="M10 40 L560 20 L600 40 L560 60 Z" fill="#c8a060"/><path d="M10 40 L560 20" stroke="#fff0c0" stroke-width="4" opacity="0.6"/>', 620, 80)


def chispa():
    w = h = 300
    d = rg("ch_g", (0, "#ffffff", 1), (0.25, "#ffd27a", 1), (1, "#ff7a2a", 0))
    b = ['<circle cx="150" cy="150" r="140" fill="url(#ch_g)"/>'] + \
        [f'<path d="M150 150 L{150+140*math.cos(math.radians(a)):.0f} {150+140*math.sin(math.radians(a)):.0f}" stroke="#fff4d0" stroke-width="{5 if a % 90 == 0 else 2}"/>' for a in range(0, 360, 45)]
    guardar("chispa", "".join(b), w, h, d)


def generar(dirsvg):
    ilus.OUT = dirsvg
    os.makedirs(dirsvg, exist_ok=True)
    bg_tierra_antigua(); acantilado(); capas_cerca(); tronco(); martillo(); geologo_lupa(); geologo_libreta()
    bg_mar_antiguo(); coral_vivo(); coral_fosil(); coral_superficie(); disco_freno(); playa(); bg_babilonia(); tablilla(); chispa()
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
