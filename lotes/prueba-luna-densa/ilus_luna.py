"""Ilustraciones nuevas para «La Luna se aleja» versión densa (estilo v4: degradados, luz, sombras, textura).
Reutiliza los ayudantes de lotes/2026-11-15-tarde/generadores/v4/ilus.py. Uso: python3 ilus_luna.py DIR_SVG"""
import math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "2026-11-15-tarde", "generadores", "v4"))
import ilus  # noqa: E402
from ilus import lg, rg, grano, palmera  # noqa: E402

ilus.OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "svg")
os.makedirs(ilus.OUT, exist_ok=True)
guardar = ilus.guardar
R = random.Random(21)


def cohete():
    w, h = 300, 1200
    d = lg("cu", (0, "#9aa3ad"), (0.35, "#ffffff"), (0.6, "#f1f3f5"), (1, "#7d8590"), x2=1, y2=0) + \
        lg("ne", (0, "#111"), (0.4, "#3a3d42"), (1, "#0a0a0a"), x2=1, y2=0)
    cx = w / 2
    b = [f'<g filter="url(#sombra)">',
         # escape de emergencia y punta
         f'<rect x="{cx-4}" y="20" width="8" height="90" fill="#d9dde2"/>',
         f'<path d="M{cx-26} 110 L{cx} 60 L{cx+26} 110 Z" fill="url(#cu)"/>',
         f'<path d="M{cx-40} 230 L{cx-26} 110 L{cx+26} 110 L{cx+40} 230 Z" fill="url(#cu)"/>',
         # tercera etapa
         f'<rect x="{cx-40}" y="230" width="80" height="170" fill="url(#cu)"/>',
         f'<path d="M{cx-40} 400 L{cx-62} 470 L{cx+62} 470 L{cx+40} 400 Z" fill="url(#cu)"/>',
         # segunda etapa
         f'<rect x="{cx-62}" y="470" width="124" height="230" fill="url(#cu)"/>',
         f'<rect x="{cx-62}" y="560" width="124" height="26" fill="url(#ne)"/>',
         # primera etapa
         f'<rect x="{cx-62}" y="700" width="124" height="400" fill="url(#cu)"/>',
         f'<rect x="{cx-62}" y="700" width="124" height="34" fill="url(#ne)"/>',
         ''.join(f'<rect x="{cx-62+i*31}" y="{760+ (i%2)*0}" width="15.5" height="80" fill="url(#ne)" opacity="{0.9 if i%2==0 else 0}"/>' for i in range(4)),
         f'<rect x="{cx-62}" y="1040" width="124" height="60" fill="url(#ne)"/>',
         # aletas
         f'<path d="M{cx-62} 1010 L{cx-110} 1130 L{cx-62} 1100 Z" fill="#2b2e33"/>',
         f'<path d="M{cx+62} 1010 L{cx+110} 1130 L{cx+62} 1100 Z" fill="#2b2e33"/>',
         # toberas
         ''.join(f'<path d="M{cx-48+i*24} 1100 L{cx-56+i*24} 1150 L{cx-34+i*24} 1150 L{cx-40+i*24} 1100 Z" fill="#3a3d42"/>' for i in range(5)),
         f'<text x="{cx}" y="660" font-family="Arial Black,Arial" font-weight="900" font-size="30" fill="#1b1d21" text-anchor="middle" '
         f'transform="rotate(-90 {cx} 660)" letter-spacing="6">USA</text>',
         '</g>', grano(w, h)]
    guardar("cohete", "".join(b), w, h, d)


def modulo_lunar():
    w, h = 700, 640
    d = lg("oro", (0, "#ffe08a"), (0.4, "#d9a23a"), (0.7, "#8a5a12"), (1, "#f0c35a"), x2=1, y2=1) + \
        lg("gris", (0, "#e8eaee"), (0.6, "#a9afb8"), (1, "#5d636c"), x2=1, y2=1)
    cx = w / 2
    pata = lambda s: (f'<path d="M{cx+s*120} 380 L{cx+s*270} 560" stroke="#c9ccd2" stroke-width="12" stroke-linecap="round"/>'
                      f'<path d="M{cx+s*140} 330 L{cx+s*260} 545" stroke="#9aa0a8" stroke-width="7"/>'
                      f'<ellipse cx="{cx+s*275}" cy="566" rx="46" ry="12" fill="#d6d9de"/>')
    b = ['<g filter="url(#sombra)">', pata(-1), pata(1),
         # etapa de descenso (octógono dorado)
         f'<polygon points="{cx-170},300 {cx-130},260 {cx+130},260 {cx+170},300 {cx+170},410 {cx+130},450 {cx-130},450 {cx-170},410" fill="url(#oro)"/>',
         ''.join(f'<path d="M{cx-160+i*40} 270 L{cx-150+i*40+R.uniform(-8,8):.0f} 445" stroke="#fff3c2" stroke-opacity="0.25" stroke-width="3"/>' for i in range(9)),
         f'<path d="M{cx-40} 450 L{cx-60} 500 L{cx+60} 500 L{cx+40} 450 Z" fill="#4a4e55"/>',
         # etapa de ascenso
         f'<path d="M{cx-150} 260 L{cx-130} 140 L{cx-60} 90 L{cx+90} 90 L{cx+150} 150 L{cx+150} 260 Z" fill="url(#gris)"/>',
         f'<path d="M{cx-120} 170 L{cx-70} 120 L{cx-20} 120 L{cx-20} 190 L{cx-110} 200 Z" fill="#1b2a3d"/>',
         f'<path d="M{cx-112} 168 L{cx-74} 128 L{cx-40} 128" stroke="#9fd0ff" stroke-width="5" opacity="0.6" fill="none"/>',
         f'<rect x="{cx+30}" y="130" width="90" height="100" fill="#3a3f47" opacity="0.5"/>',
         f'<line x1="{cx+60}" y1="90" x2="{cx+90}" y2="20" stroke="#c9ccd2" stroke-width="6"/>',
         f'<circle cx="{cx+92}" cy="16" r="16" fill="none" stroke="#c9ccd2" stroke-width="5"/>',
         f'<rect x="{cx-100}" y="300" width="40" height="70" fill="#f8f4e6" opacity="0.85"/>',
         '</g>', grano(w, h)]
    guardar("modulo_lunar", "".join(b), w, h, d)


def dinosaurio(nombre="dino", color="#3f5e2e", luz="#ffc070"):
    w, h = 1000, 700
    d = lg("dc", (0, color), (1, "#0f180c"))
    cuerpo = ("M120 520 C80 470 140 420 230 410 C300 330 470 300 600 330 C680 250 720 140 790 90 C830 60 900 60 920 95 "
              "C930 120 900 130 870 130 C820 150 790 250 760 350 C800 420 790 480 760 520 L740 640 L700 640 L700 540 "
              "C640 560 560 560 500 550 L480 650 L440 650 L440 540 C380 530 330 520 290 520 L280 640 L240 640 L240 520 "
              "C180 530 140 560 60 600 C40 610 20 600 40 590 Z")
    b = [f'<ellipse cx="480" cy="655" rx="380" ry="26" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         f'<path d="{cuerpo}" fill="url(#dc)"/>',
         f'<path d="{cuerpo}" fill="none" stroke="{luz}" stroke-width="7" opacity="0.8"/>',
         f'<circle cx="890" cy="92" r="6" fill="#ffd27a"/>',
         grano(w, h)]
    guardar(nombre, "".join(b), w, h, d)


def bg_jungla():
    d = lg("cj", (0, "#2b1b3a"), (0.35, "#c2543a"), (0.6, "#f2a65a"), (1, "#f6d08a")) + \
        rg("solj", (0, "#fff1c0", 1), (1, "#fff1c0", 0)) + lg("vol", (0, "#4a2a2a"), (1, "#1b1012"))
    b = ['<rect width="1080" height="1920" fill="url(#cj)"/>',
         '<circle cx="720" cy="980" r="320" fill="url(#solj)" opacity="0.8"/>',
         '<circle cx="720" cy="1000" r="110" fill="#fff4cf"/>',
         '<path d="M-50 1260 L260 760 L330 740 L400 770 L760 1260 Z" fill="url(#vol)"/>',
         '<path d="M270 760 C250 640 330 560 290 460 C360 520 380 420 450 380" stroke="#6b5a5a" stroke-width="70" opacity="0.35" filter="url(#blur20)" fill="none"/>',
         '<path d="M500 1300 L820 900 L1100 1300 Z" fill="#3a2226" opacity="0.8"/>',
         '<rect y="1250" width="1080" height="670" fill="#1b2a14"/>',
         '<path d="M0 1260 C200 1220 400 1290 600 1250 C800 1215 950 1270 1080 1240 L1080 1330 L0 1330 Z" fill="#26391b"/>']
    for x in range(-40, 1120, 90):  # helechos
        y = 1300 + R.uniform(-20, 40)
        for k in range(7):
            a = -150 + k * 20 + R.uniform(-6, 6)
            L = R.uniform(90, 170)
            b.append(f'<path d="M{x} {y} Q{x+math.cos(math.radians(a))*L*0.6:.0f} {y+math.sin(math.radians(a))*L*0.9:.0f} '
                     f'{x+math.cos(math.radians(a))*L:.0f} {y+math.sin(math.radians(a))*L*0.6:.0f}" stroke="#2f4a22" stroke-width="12" fill="none" stroke-linecap="round"/>')
    b += [palmera(120, 1420, 1.5, "#141f10", "#f2a65a"), palmera(960, 1460, 1.8, "#141f10", "#f2a65a"),
          palmera(600, 1330, 0.9, "#1b2a14", "#f2a65a"),
          '<rect y="1500" width="1080" height="420" fill="#0f180c" opacity="0.6"/>', grano()]
    guardar("bg_jungla", "".join(b), defs=d)


def almeja_fosil():
    w, h = 900, 800
    d = rg("pi", (0, "#efe3c8", 1), (0.7, "#c9b48a", 1), (1, "#8a7552", 1), cx=0.4, cy=0.35) + \
        lg("roca", (0, "#7d7466"), (1, "#3f3a33"))
    cx, cy = 450, 700
    conc = f"M{cx} {cy} C{cx-520} {cy-160} {cx-360} {cy-560} {cx} {cy-560} C{cx+360} {cy-560} {cx+520} {cy-160} {cx} {cy} Z"
    b = [f'<path d="M30 760 C120 640 260 600 450 610 C640 600 790 650 870 760 L870 800 L30 800 Z" fill="url(#roca)"/>',
         f'<clipPath id="conc"><path d="{conc}"/></clipPath>',
         f'<g filter="url(#sombra)"><path d="{conc}" fill="url(#pi)"/><g clip-path="url(#conc)">']
    for i in range(1, 46):  # anillos de crecimiento diarios
        s = i / 46
        b.append(f'<path d="M{cx-430*s:.0f} {cy-150*s:.0f} C{cx-330*s:.0f} {cy-560*s:.0f} {cx+330*s:.0f} {cy-560*s:.0f} {cx+430*s:.0f} {cy-150*s:.0f}" '
                 f'stroke="#6b5838" stroke-width="{2.6 if i % 7 == 0 else 1.2}" stroke-opacity="{0.75 if i % 7 == 0 else 0.4}" fill="none"/>')
    for k in range(11):  # costillas radiales desde la charnela
        a = math.radians(28 + k * 12.4)
        b.append(f'<path d="M{cx} {cy} L{cx+math.cos(a)*400:.0f} {cy-math.sin(a)*540:.0f}" stroke="#ffffff" stroke-opacity="0.13" stroke-width="12"/>')
    b += [f'<ellipse cx="{cx-120}" cy="{cy-420}" rx="110" ry="50" fill="#ffffff" opacity="0.18" transform="rotate(-25 {cx-120} {cy-420})"/></g></g>',
          grano(w, h)]
    guardar("almeja_fosil", "".join(b), w, h, d)


def calendario():
    w, h = 640, 720
    d = lg("cal", (0, "#ffffff"), (1, "#e9e4d8")) + lg("cab", (0, "#e0473a"), (1, "#a82a20"))
    b = ['<g filter="url(#sombra)">', f'<rect x="20" y="60" width="600" height="640" rx="28" fill="url(#cal)"/>',
         f'<path d="M20 88 Q20 60 48 60 L592 60 Q620 60 620 88 L620 200 L20 200 Z" fill="url(#cab)"/>']
    b += [f'<rect x="{90+i*110}" y="30" width="26" height="80" rx="13" fill="#3a3d42"/>' for i in range(5)]
    for f in range(4):
        for c in range(7):
            b.append(f'<rect x="{60+c*78}" y="{450+f*58}" width="56" height="40" rx="6" fill="#d9d3c4" opacity="0.7"/>')
    b += ['</g>', grano(w, h)]
    guardar("calendario", "".join(b), w, h, d)


def bg_eclipse():
    d = lg("ce", (0, "#020414"), (0.55, "#0d1638"), (0.8, "#3b3a6a"), (1, "#e08a4a"))
    b = ['<rect width="1080" height="1920" fill="url(#ce)"/>', ilus_estrellas(120, 1100),
         '<path d="M0 1560 C200 1500 360 1540 520 1500 C700 1460 880 1530 1080 1490 L1080 1920 L0 1920 Z" fill="#0b0d16"/>',
         '<path d="M0 1640 C240 1610 500 1660 760 1620 C900 1600 1000 1630 1080 1620 L1080 1920 L0 1920 Z" fill="#05060b"/>', grano()]
    guardar("bg_eclipse", "".join(b), defs=d)


def ilus_estrellas(n, hmax):
    return "".join(f'<circle cx="{R.uniform(0,1080):.0f}" cy="{R.uniform(0,hmax):.0f}" r="{R.uniform(0.8,2.4):.1f}" fill="#ffffff" opacity="{R.uniform(0.3,0.9):.2f}"/>' for _ in range(n))


def personas_mirando():
    w, h = 1080, 520
    b = []
    for x, s in [(200, 1.0), (330, 0.85), (760, 1.1), (880, 0.7)]:
        y = 520
        b.append(f'<g fill="#05060b"><circle cx="{x}" cy="{y-300*s:.0f}" r="{34*s:.0f}"/>'
                 f'<path d="M{x-60*s:.0f} {y} C{x-60*s:.0f} {y-180*s:.0f} {x-40*s:.0f} {y-250*s:.0f} {x} {y-262*s:.0f} '
                 f'C{x+40*s:.0f} {y-250*s:.0f} {x+60*s:.0f} {y-180*s:.0f} {x+60*s:.0f} {y} Z"/>'
                 f'<path d="M{x+30*s:.0f} {y-230*s:.0f} L{x+70*s:.0f} {y-330*s:.0f}" stroke="#05060b" stroke-width="{16*s:.0f}" stroke-linecap="round"/></g>'
                 f'<path d="M{x-34*s:.0f} {y-305*s:.0f} A{34*s:.0f} {34*s:.0f} 0 0 1 {x+30*s:.0f} {y-318*s:.0f}" stroke="#ffd9a0" stroke-width="3" opacity="0.7" fill="none"/>')
    guardar("personas_mirando", "".join(b), w, h)


def pterosaurio():
    w, h = 700, 360
    b = ['<path d="M350 190 C300 150 220 110 40 120 C140 150 220 180 300 210 Z" fill="#2a1d24"/>',
         '<path d="M350 190 C400 150 480 110 660 120 C560 150 480 180 400 210 Z" fill="#2a1d24"/>',
         '<path d="M300 205 C330 180 380 180 410 200 C430 205 470 200 520 215 C470 220 430 225 400 225 C360 235 320 230 300 205 Z" fill="#1f161b"/>',
         '<path d="M410 196 C430 170 450 160 470 150" stroke="#1f161b" stroke-width="10" stroke-linecap="round"/>',
         '<path d="M40 120 C140 150 220 180 300 210" stroke="#ffb45a" stroke-width="3" opacity="0.6" fill="none"/>']
    guardar("pterosaurio", "".join(b), w, h)


def satelite():
    w, h = 420, 200
    d = lg("pan", (0, "#2a4a8a"), (1, "#122244"))
    b = [f'<rect x="10" y="70" width="140" height="60" fill="url(#pan)" stroke="#9fb8e8" stroke-width="3"/>',
         f'<rect x="270" y="70" width="140" height="60" fill="url(#pan)" stroke="#9fb8e8" stroke-width="3"/>',
         ''.join(f'<line x1="{10+i*28}" y1="70" x2="{10+i*28}" y2="130" stroke="#9fb8e8" stroke-width="1.5"/>' for i in range(1, 5)),
         ''.join(f'<line x1="{270+i*28}" y1="70" x2="{270+i*28}" y2="130" stroke="#9fb8e8" stroke-width="1.5"/>' for i in range(1, 5)),
         '<line x1="150" y1="100" x2="270" y2="100" stroke="#c9ccd2" stroke-width="5"/>',
         '<rect x="175" y="55" width="70" height="90" rx="8" fill="#e2b13c"/>',
         '<circle cx="210" cy="40" r="22" fill="none" stroke="#e8eaee" stroke-width="5"/>']
    guardar("satelite", "".join(b), w, h, d)


def patinadora(nombre, brazos):
    """Silueta a contraluz; brazos: 'cerrados' (pegados al pecho) o 'abiertos' (en cruz)."""
    w, h = 700, 900
    d = lg("pt", (0, "#1a1030"), (1, "#0a0614"))
    cx = 350
    cuerpo = (f'<circle cx="{cx}" cy="150" r="52"/>'
              f'<path d="M{cx-14} 200 L{cx+14} 200 L{cx+40} 300 L{cx+52} 470 C{cx+110} 520 {cx+130} 560 {cx+40} 560 '
              f'L{cx+18} 560 L{cx+14} 800 L{cx+40} 830 L{cx-10} 830 L{cx-10} 560 L{cx-40} 560 C{cx-130} 560 {cx-110} 520 {cx-52} 470 L{cx-40} 300 Z"/>'
              f'<path d="M{cx+10} 560 L{cx+150} 690 L{cx+170} 680" stroke="#0a0614" stroke-width="30" stroke-linecap="round" fill="none"/>')
    if brazos == "abiertos":
        br = (f'<path d="M{cx-30} 270 L{cx-300} 250" stroke="#0a0614" stroke-width="26" stroke-linecap="round"/>'
              f'<path d="M{cx+30} 270 L{cx+300} 250" stroke="#0a0614" stroke-width="26" stroke-linecap="round"/>')
    else:
        br = (f'<path d="M{cx-34} 260 C{cx-90} 300 {cx-60} 340 {cx} 340" stroke="#0a0614" stroke-width="26" stroke-linecap="round" fill="none"/>'
              f'<path d="M{cx+34} 260 C{cx+90} 300 {cx+60} 340 {cx} 340" stroke="#0a0614" stroke-width="26" stroke-linecap="round" fill="none"/>')
    b = [f'<ellipse cx="{cx}" cy="840" rx="160" ry="22" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         f'<g fill="url(#pt)">{cuerpo}</g>', br,
         f'<g fill="none" stroke="#bfe6ff" stroke-width="5" opacity="0.8"><path d="M{cx+30} 120 A52 52 0 0 1 {cx+50} 170"/>'
         f'<path d="M{cx+40} 300 L{cx+52} 470"/><path d="M{cx+14} 600 L{cx+14} 790"/></g>',
         '<path d="M240 840 L470 840" stroke="#c9ccd2" stroke-width="6"/>']
    guardar(nombre, "".join(b), w, h, d)


def bg_pista():
    d = lg("pi1", (0, "#0b1430"), (0.55, "#24407a"), (1, "#9fd0ff")) + rg("foco", (0, "#ffffff", 0.7), (1, "#ffffff", 0))
    b = ['<rect width="1080" height="1920" fill="url(#pi1)"/>',
         '<ellipse cx="540" cy="700" rx="520" ry="900" fill="url(#foco)" opacity="0.5"/>',
         '<path d="M0 1350 L1080 1350 L1080 1920 L0 1920 Z" fill="#cfe8ff"/>',
         '<path d="M0 1350 L1080 1350" stroke="#ffffff" stroke-width="6" opacity="0.7"/>',
         ''.join(f'<path d="M{R.uniform(0,1080):.0f} {R.uniform(1380,1900):.0f} q{R.uniform(-200,200):.0f} {R.uniform(-30,30):.0f} {R.uniform(-300,300):.0f} 0" stroke="#ffffff" stroke-width="3" opacity="0.5" fill="none"/>' for _ in range(30)),
         '<ellipse cx="540" cy="1500" rx="420" ry="80" fill="#ffffff" opacity="0.35" filter="url(#blur20)"/>', grano()]
    guardar("bg_pista", "".join(b), defs=d)


if __name__ == "__main__":
    for f in (pterosaurio, satelite, cohete, modulo_lunar, dinosaurio, bg_jungla, almeja_fosil, calendario, bg_eclipse, personas_mirando):
        f()
    dinosaurio("dino_peq", "#4a6a38")
    patinadora("patinadora_cerrada", "cerrados"); patinadora("patinadora_abierta", "abiertos"); bg_pista()
    print("ok", ilus.OUT)
