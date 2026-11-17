"""Biblioteca de ilustraciones SVG del método denso (DECISIONS 2026-11-16). Sale de la prueba «La Luna se aleja».

Uso:  python3 -m motor.biblioteca.ilus DIR_SVG      → escribe ahí todas las ilustraciones generadas
      from motor.biblioteca import ilus; ilus.generar(DIR_SVG)
Las ilustraciones fijas del estilo v4 (Tierra, Luna, reloj, astronauta…) están ya hechas en `motor/biblioteca/svg/`.

Piezas para dibujar cosas NUEVAS con el mismo nivel (ver `motor/DENSO.md`):
- `guardar(nombre, cuerpo, w, h, defs)`, `lg`/`rg` (degradados), `grano()`, filtros `#blur8/#blur20/#blur40/#sombra/#grano`.
- `_animal(...)`: cualquier animal o figura con volumen (lomo→panza), manchas, textura de piel, luz de borde, ojo y sombra.
- `bg_espacio_rico(nombre, paleta, semilla)`: cielo con nebulosas en capas, polvo, Vía Láctea y estrellas de colores.
- `_neb`, `_mascara`, `_estrellas_ricas`, `_hoja`, `_pata`: ladrillos sueltos.
"""
import math, os, random

OUT = "."
R = random.Random(21)
_RP = random.Random(7)

W, H = 1080, 1920


def guardar(nombre, cuerpo, w=W, h=H, defs=""):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
           f'<defs>{TEXTURA}{defs}</defs>{cuerpo}</svg>')
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, nombre + ".svg"), "w").write(svg)


TEXTURA = """
<filter id="grano" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3" result="n"/>
  <feColorMatrix type="saturate" values="0"/>
  <feComponentTransfer><feFuncA type="table" tableValues="0 0.10"/></feComponentTransfer>
  <feComposite operator="in" in2="SourceGraphic"/>
</filter>
<filter id="papel" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="4" seed="9"/>
  <feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.30  0 0 0 0 0.12  0 0 0 0.55 0"/>
  <feComposite operator="in" in2="SourceGraphic"/>
</filter>
<filter id="blur8"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="blur20"><feGaussianBlur stdDeviation="20"/></filter>
<filter id="blur40"><feGaussianBlur stdDeviation="40"/></filter>
<filter id="sombra" x="-20%" y="-20%" width="140%" height="140%">
  <feDropShadow dx="10" dy="16" stdDeviation="12" flood-color="#000" flood-opacity="0.45"/>
</filter>
"""


def lg(id_, *stops, x2=0, y2=1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def rg(id_, *stops, cx=0.5, cy=0.5, r=0.5):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'


def grano(w=W, h=H):
    return f'<rect width="{w}" height="{h}" fill="#888" filter="url(#grano)"/>'


# ------------------------------------------------------------------ piezas reutilizables
def palmera(x, y, s=1.0, color="#1d2a1f", luz="#e9a35a"):
    tronco = (f'<path d="M{x} {y} C{x+10*s} {y-120*s} {x-6*s} {y-260*s} {x+24*s} {y-380*s}" '
              f'stroke="{color}" stroke-width="{18*s}" fill="none" stroke-linecap="round"/>'
              f'<path d="M{x+4*s} {y} C{x+14*s} {y-120*s} {x-2*s} {y-260*s} {x+28*s} {y-380*s}" '
              f'stroke="{luz}" stroke-opacity="0.35" stroke-width="{4*s}" fill="none"/>')
    hojas = ""
    cx, cy = x + 24 * s, y - 380 * s
    for ang in (-160, -125, -90, -55, -20, 15, 200):
        a = math.radians(ang)
        ex, ey = cx + math.cos(a) * 190 * s, cy + math.sin(a) * 120 * s + 60 * s
        mx, my = cx + math.cos(a) * 100 * s, cy + math.sin(a) * 90 * s - 30 * s
        hojas += (f'<path d="M{cx} {cy} Q{mx} {my} {ex} {ey} Q{mx+10*s} {my+30*s} {cx} {cy+8*s} Z" fill="{color}"/>')
    return tronco + hojas


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
         '</g>']
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
         '</g>']
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
         f'<circle cx="890" cy="92" r="6" fill="#ffd27a"/>']
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
    b += [f'<ellipse cx="{cx-120}" cy="{cy-420}" rx="110" ry="50" fill="#ffffff" opacity="0.18" transform="rotate(-25 {cx-120} {cy-420})"/></g></g>']
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
    b += ['</g>']
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


# ======================================================================= FONDOS RICOS (v4 densa)
def _neb(id_, color, sem, freq=0.0028, contraste=2.4, corte=0.95, oct=5):
    r, g, b = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return (f'<filter id="{id_}" x="0" y="0" width="100%" height="100%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="{oct}" seed="{sem}"/>'
            f'<feColorMatrix type="matrix" values="0 0 0 0 {r:.3f}  0 0 0 0 {g:.3f}  0 0 0 0 {b:.3f}  {contraste} 0 0 0 -{corte}"/></filter>')


def _mascara(id_, cx, cy, rx, ry, rot=0):
    return (f'<radialGradient id="{id_}g"><stop offset="0" stop-color="#fff"/><stop offset="0.55" stop-color="#fff" stop-opacity="0.7"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            f'<mask id="{id_}" maskUnits="userSpaceOnUse" x="0" y="0" width="1080" height="1920">'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" fill="url(#{id_}g)"/></mask>')


def _estrellas_ricas(sem, n_peq=650, n_med=70, n_bri=14, banda=None):
    r = random.Random(sem)
    cols = ["#ffffff", "#cfe0ff", "#a9c4ff", "#fff1c8", "#ffd2a0", "#ffb0a0"]
    out = []
    for _ in range(n_peq):
        x, y = r.uniform(0, 1080), r.uniform(0, 1920)
        if banda and r.random() < 0.55:  # más estrellas en la banda de la galaxia
            t = r.uniform(-0.2, 1.2); x = banda[0] + (banda[2] - banda[0]) * t + r.gauss(0, 110); y = banda[1] + (banda[3] - banda[1]) * t + r.gauss(0, 110)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(0.5, 1.4):.1f}" fill="{r.choice(cols)}" opacity="{r.uniform(0.35, 0.95):.2f}"/>')
    for _ in range(n_med):
        x, y, c = r.uniform(0, 1080), r.uniform(0, 1920), r.choice(cols)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.6, 2.6):.1f}" fill="{c}"/>'
                   f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{c}" opacity="0.18" filter="url(#blur8)"/>')
    for _ in range(n_bri):
        x, y, c, L = r.uniform(40, 1040), r.uniform(40, 1880), r.choice(cols[:4]), r.uniform(18, 40)
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="22" fill="{c}" opacity="0.28" filter="url(#blur8)"/>'
                   f'<path d="M{x-L:.0f} {y:.0f} L{x+L:.0f} {y:.0f} M{x:.0f} {y-L:.0f} L{x:.0f} {y+L:.0f}" stroke="{c}" stroke-width="1.4" opacity="0.7"/>'
                   f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.2" fill="#ffffff"/>')
    return "".join(out)


PALETAS = {"violeta": ("#03040c", "#0d0b2a", "#06081a", ["#7b3fe4", "#e0408a", "#2bb3c9"]),
           "petroleo": ("#020a10", "#06222e", "#030914", ["#1f8fb0", "#2fd1a6", "#6a3fb8"]),
           "ambar": ("#0a0508", "#22102a", "#0a0614", ["#ff8a3d", "#c2385a", "#4a5bd6"])}


def bg_espacio_rico(nombre, paleta, sem):
    c0, c1, c2, neb = PALETAS[paleta]
    r = random.Random(sem)
    d = lg(f"b{nombre}", (0, c0), (0.5, c1), (1, c2))
    capas = []
    for i, col in enumerate(neb):
        cx, cy = r.uniform(150, 930), r.uniform(250, 1700)
        d += _neb(f"n{nombre}{i}", col, sem * 10 + i, freq=r.uniform(0.0022, 0.0034)) + _mascara(f"m{nombre}{i}", cx, cy, r.uniform(420, 650), r.uniform(520, 900), r.uniform(-40, 40))
        capas.append(f'<rect width="1080" height="1920" filter="url(#n{nombre}{i})" mask="url(#m{nombre}{i})" opacity="0.75"/>')
    # polvo oscuro (filamentos) y banda de la galaxia en diagonal
    band = (r.uniform(-100, 200), r.uniform(1500, 1900), r.uniform(900, 1200), r.uniform(0, 400))
    d += _neb(f"p{nombre}", "#000000", sem + 77, freq=0.006, contraste=3.2, corte=1.35, oct=4)
    d += lg(f"via{nombre}", (0, "#ffffff00"), (0.5, "#dfe6ff"), (1, "#ffffff00"))
    ang = math.degrees(math.atan2(band[3] - band[1], band[2] - band[0]))
    mx, my = (band[0] + band[2]) / 2, (band[1] + band[3]) / 2
    b = [f'<rect width="1080" height="1920" fill="url(#b{nombre})"/>',
         f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="1400" ry="190" fill="#c9d4ff" opacity="0.10" transform="rotate({ang:.0f} {mx:.0f} {my:.0f})" filter="url(#blur40)"/>',
         f'<ellipse cx="{mx:.0f}" cy="{my:.0f}" rx="1300" ry="70" fill="#fff4e0" opacity="0.10" transform="rotate({ang:.0f} {mx:.0f} {my:.0f})" filter="url(#blur20)"/>',
         *capas,
         f'<rect width="1080" height="1920" filter="url(#p{nombre})" opacity="0.55"/>',
         "".join(f'<ellipse cx="{r.uniform(80,1000):.0f}" cy="{r.uniform(80,1840):.0f}" rx="{r.uniform(10,22):.0f}" ry="{r.uniform(3,7):.0f}" fill="#e8ddff" opacity="0.35" '
                 f'transform="rotate({r.uniform(0,180):.0f})" filter="url(#blur8)"/>' for _ in range(0)),
         _estrellas_ricas(sem, banda=band),
         *[f'<g transform="translate({r.uniform(80,1000):.0f} {r.uniform(80,1840):.0f}) rotate({r.uniform(0,180):.0f})">'
           f'<ellipse rx="26" ry="8" fill="#f0e6ff" opacity="0.35" filter="url(#blur8)"/><ellipse rx="6" ry="2.5" fill="#ffffff" opacity="0.8"/></g>' for _ in range(3)],
         grano()]
    guardar(nombre, "".join(b), defs=d)


def bg_superficie_rica():
    r = random.Random(41)
    d = (lg("cielo_l", (0, "#02030a"), (0.7, "#070a1c"), (1, "#0d1230")) +
         lg("suelo_l", (0, "#c9c2b6"), (0.25, "#a39d93"), (0.7, "#6f6b67"), (1, "#3b3a3e")) +
         lg("lejos_l", (0, "#8e8c94"), (1, "#5d5c66")) +
         _neb("tex_l", "#2a2620", 5, freq=0.02, contraste=2.0, corte=0.85, oct=4) +
         _neb("tex_l2", "#ffffff", 6, freq=0.008, contraste=1.6, corte=0.95, oct=3) +
         rg("crat", (0, "#3b3936", 0.9), (0.7, "#5a5753", 0.7), (1, "#5a5753", 0)) +
         '<clipPath id="cl_suelo"><path d="M0 1080 C200 1050 380 1090 560 1060 C760 1030 920 1075 1080 1050 L1080 1920 L0 1920 Z"/></clipPath>')
    b = ['<rect width="1080" height="1920" fill="url(#cielo_l)"/>',
         '<ellipse cx="600" cy="500" rx="1200" ry="130" fill="#cdd6ff" opacity="0.08" transform="rotate(-28 600 500)" filter="url(#blur40)"/>',
         _estrellas_ricas(42, 380, 40, 8, banda=(-100, 900, 1200, 100)),
         # cordillera lejana (más clara y azulada: perspectiva)
         '<path d="M0 1020 L120 960 L230 990 L340 930 L470 985 L600 950 L720 990 L860 940 L980 975 L1080 950 L1080 1100 L0 1100 Z" fill="url(#lejos_l)"/>',
         '<path d="M0 1020 L120 960 L230 990 L340 930 L470 985 L600 950 L720 990 L860 940 L980 975 L1080 950" stroke="#e8e4dc" stroke-width="3" opacity="0.6" fill="none"/>',
         # llanura
         '<g clip-path="url(#cl_suelo)"><rect width="1080" height="1920" fill="url(#suelo_l)"/>',
         '<rect width="1080" height="1920" filter="url(#tex_l)" opacity="0.8"/>',
         '<rect width="1080" height="1920" filter="url(#tex_l2)" opacity="0.15"/>']
    for _ in range(18):  # cráteres: cuenco oscuro + borde lejano iluminado (luz de la derecha), más grandes cuanto más cerca
        y = r.uniform(1110, 1860); k = (y - 1050) / 850
        rx = r.uniform(25, 70) * (0.4 + k * 1.8); ry = rx * (0.2 + k * 0.18); x = r.uniform(-30, 1110)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="url(#crat)"/>'
                 f'<path d="M{x-rx*0.2:.0f} {y+ry*0.95:.0f} A{rx:.0f} {ry:.0f} 0 0 0 {x+rx:.0f} {y:.0f}" stroke="#e9e2d6" stroke-width="{1.5+k*2.5:.1f}" opacity="0.45" fill="none"/>')
    for _ in range(34):  # piedras: cuerpo del color del suelo, cara iluminada a la derecha y sombra a la izquierda
        y = r.uniform(1120, 1900); k = (y - 1050) / 850; s = r.uniform(3, 10) * (0.5 + k * 2.2); x = r.uniform(0, 1080)
        b.append(f'<ellipse cx="{x-s*1.1:.0f}" cy="{y+s*0.35:.0f}" rx="{s*1.5:.0f}" ry="{s*0.3:.0f}" fill="#141418" opacity="0.45"/>'
                 f'<path d="M{x-s:.0f} {y+s*0.4:.0f} C{x-s:.0f} {y-s*0.6:.0f} {x+s:.0f} {y-s*0.7:.0f} {x+s:.0f} {y+s*0.4:.0f} Z" fill="#7b766f"/>'
                 f'<path d="M{x:.0f} {y-s*0.5:.0f} C{x+s*0.6:.0f} {y-s*0.5:.0f} {x+s:.0f} {y:.0f} {x+s:.0f} {y+s*0.4:.0f}" stroke="#d6d0c4" stroke-width="{max(1.5, s*0.25):.1f}" opacity="0.6" fill="none"/>')
    b += ['</g>',
          '<linearGradient id="prof" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b2140" stop-opacity="0"/><stop offset="1" stop-color="#1b2140" stop-opacity="0.45"/></linearGradient>',
          '<rect y="1100" width="1080" height="820" fill="url(#prof)"/>',
          '<path d="M-60 1920 C80 1760 260 1800 340 1920 Z" fill="#26252b" filter="url(#blur8)"/>',
          '<path d="M760 1920 C860 1740 1060 1770 1140 1920 Z" fill="#2a292f" filter="url(#blur8)"/>',
          grano()]
    guardar("bg_superficie_rica", "".join(b), defs=d)


def bg_eclipse_rico():
    d = (lg("ce2", (0, "#03040f"), (0.35, "#0b1238"), (0.62, "#2c2a66"), (0.74, "#8a3f6e"), (0.8, "#e0785a"), (0.84, "#f6b36a")) +
         lg("col1", (0, "#4a4a7a"), (1, "#2a2a4a")) + lg("col2", (0, "#24243e"), (1, "#14142a")))
    r = random.Random(51)
    b = ['<rect width="1080" height="1920" fill="url(#ce2)"/>',
         _estrellas_ricas(52, 260, 30, 6),
         '<rect y="1080" width="1080" height="840" fill="#03040f" opacity="0"/>',
         *[f'<ellipse cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(1300,1500):.0f}" rx="{r.uniform(200,420):.0f}" ry="{r.uniform(10,22):.0f}" fill="#ffb08a" opacity="{r.uniform(0.15,0.35):.2f}" filter="url(#blur8)"/>' for _ in range(6)],
         '<path d="M0 1520 C150 1470 300 1500 460 1460 C640 1420 820 1490 1080 1450 L1080 1920 L0 1920 Z" fill="url(#col1)"/>',
         '<path d="M0 1580 C220 1540 420 1590 640 1550 C820 1520 960 1570 1080 1550 L1080 1920 L0 1920 Z" fill="url(#col2)"/>',
         '<path d="M0 1650 C240 1620 500 1670 760 1630 C900 1610 1000 1640 1080 1630 L1080 1920 L0 1920 Z" fill="#05060b"/>',
         '<rect y="1440" width="1080" height="80" fill="#ffd0a0" opacity="0.12" filter="url(#blur20)"/>', grano()]
    guardar("bg_eclipse", "".join(b), defs=d)


# ======================================================================= DINOSAURIOS DETALLADOS
def _animal(nombre, w, h, cuerpo, lejos, cerca, extra, c_lomo, c_panza, luz="#ffc070", manchas=0, sem=1, ojo=None, sombra=None):
    """Silueta con volumen: degradado lomo→panza, manchas, textura de piel, luz de borde, ojo y sombra en el suelo.
    cuerpo: path principal; lejos/cerca: patas (lejos más oscuras); extra: detalles encima (placas, cuernos...)."""
    r = random.Random(sem)
    d = (lg(f"{nombre}_c", (0, c_lomo), (0.55, c_lomo), (1, c_panza)) +
         lg(f"{nombre}_l", (0, luz), (0.35, luz + "00")) +
         f'<clipPath id="{nombre}_clip"><path d="{cuerpo}"/>{"".join(f"<path d=\"{p}\"/>" for p in cerca)}</clipPath>')
    b = []
    if sombra:
        b.append(f'<ellipse cx="{sombra[0]}" cy="{sombra[1]}" rx="{sombra[2]}" ry="{sombra[3]}" fill="#000" opacity="0.4" filter="url(#blur8)"/>')
    b += [f'<path d="{p}" fill="{c_lomo}" opacity="1"/><path d="{p}" fill="#000" opacity="0.35"/>' for p in lejos]
    b += [f'<path d="{cuerpo}" fill="url(#{nombre}_c)"/>'] + [f'<path d="{p}" fill="url(#{nombre}_c)"/>' for p in cerca]
    b.append(f'<g clip-path="url(#{nombre}_clip)">')
    for _ in range(manchas):
        b.append(f'<ellipse cx="{r.uniform(0,w):.0f}" cy="{r.uniform(0,h*0.75):.0f}" rx="{r.uniform(10,34):.0f}" ry="{r.uniform(6,18):.0f}" fill="#000" opacity="{r.uniform(0.12,0.25):.2f}"/>')
    b.append(f'<rect width="{w}" height="{h}" fill="#888" filter="url(#grano)"/>')
    b.append(f'<rect width="{w}" height="{h}" fill="url(#{nombre}_l)" opacity="0.55"/></g>')
    b.append(f'<path d="{cuerpo}" fill="none" stroke="{luz}" stroke-width="3" opacity="0.45"/>')
    b += extra
    if ojo:
        b.append(f'<circle cx="{ojo[0]}" cy="{ojo[1]}" r="{ojo[2]}" fill="#1a1208"/><circle cx="{ojo[0]+ojo[2]*0.3:.1f}" cy="{ojo[1]-ojo[2]*0.3:.1f}" r="{ojo[2]*0.35:.1f}" fill="#fff6d8"/>')
    guardar(nombre, "".join(b), w, h, d)


def _pata(x, y0, y1, ancho, pie=1.25, dob=0):
    """Pata columnar con un pequeño codo/rodilla (dob px hacia delante) y pie ancho."""
    a = ancho / 2
    return (f"M{x-a} {y0} C{x-a+dob} {(y0+y1)/2} {x-a*0.9} {y1-30} {x-a*pie} {y1} L{x+a*pie} {y1} "
            f"C{x+a*0.9} {y1-30} {x+a+dob} {(y0+y1)/2} {x+a} {y0} Z")


def braquiosaurio():
    cuerpo = ("M150 470 C170 380 330 330 480 335 C560 338 620 360 660 390 C690 300 730 190 770 110 C785 80 810 55 845 52 "
              "C880 50 905 62 912 80 C918 96 900 104 880 104 C860 106 842 112 832 128 C806 210 782 300 760 400 "
              "C752 450 720 485 670 500 C560 525 380 525 280 505 C230 495 200 488 170 482 "
              "C120 480 60 495 10 530 C40 495 100 470 150 470 Z")
    lejos = [_pata(330, 470, 660, 54, dob=6), _pata(690, 460, 655, 58, dob=-6)]
    cerca = [_pata(280, 470, 668, 62, dob=8), _pata(640, 460, 664, 66, dob=-8)]
    extra = [f'<path d="M835 98 C850 90 868 92 880 98" stroke="#2a3a20" stroke-width="3" fill="none"/>',
             f'<path d="M700 300 C720 230 745 170 775 115" stroke="#000" stroke-width="10" opacity="0.12" fill="none"/>'] + \
            [f'<path d="M{760 - i*6} {160 + i*42} q14 -6 26 2" stroke="#000" stroke-width="3" opacity="0.18" fill="none"/>' for i in range(6)]
    _animal("dino_braquio", 960, 700, cuerpo, lejos, cerca, extra, "#5a6b3c", "#c8c08a", manchas=14, sem=3, ojo=(872, 76, 6), sombra=(470, 670, 360, 22))


def tiranosaurio():
    cuerpo = ("M30 300 C160 290 300 285 410 300 C470 240 550 210 630 215 C690 175 760 160 840 168 C900 172 945 195 958 232 "
              "L955 262 C915 266 880 266 850 272 C862 290 850 305 815 302 C780 322 740 360 700 382 C650 405 570 410 520 398 "
              "C470 388 440 368 418 352 C320 340 180 330 30 300 Z")
    lejos = ["M520 320 C600 300 660 350 650 430 C645 470 620 490 600 500 L620 615 L665 640 L560 645 L565 560 L545 500 C505 470 490 380 520 320 Z"]
    cerca = ["M440 320 C525 290 600 345 590 430 C585 470 560 492 540 502 L562 625 L612 652 L492 656 L500 560 L478 502 C436 470 418 390 440 320 Z"]
    dientes = "".join(f'<path d="M{870 + i*14} 262 l6 12 l6 -12 Z" fill="#fff8e0"/>' for i in range(6))
    extra = [dientes, '<path d="M850 272 C880 270 920 268 955 262" stroke="#2a1410" stroke-width="4" fill="none"/>',
             '<path d="M730 320 C745 335 760 345 775 340" stroke="#3a2a20" stroke-width="10" stroke-linecap="round" fill="none"/>',
             '<path d="M760 330 l12 10" stroke="#3a2a20" stroke-width="6" stroke-linecap="round"/>',
             '<path d="M800 200 C820 190 840 188 860 192" stroke="#2a1410" stroke-width="5" opacity="0.6" fill="none"/>']
    _animal("dino_trex", 980, 700, cuerpo, lejos, cerca, extra, "#6b4a30", "#d8b98a", manchas=16, sem=5, ojo=(845, 205, 7), sombra=(520, 660, 320, 20))


def triceratops():
    cuerpo = ("M110 430 C140 330 300 290 450 300 C560 305 640 330 680 370 C700 390 705 440 695 480 C600 510 300 512 200 492 "
              "C160 482 130 462 110 430 Z")
    cola = "M120 430 C80 425 40 440 5 470 C55 455 100 452 140 452 Z"
    lejos = [_pata(250, 470, 610, 70, 1.15), _pata(600, 470, 605, 70, 1.15)]
    cerca = [cola, _pata(210, 470, 620, 78, 1.15), _pata(560, 470, 615, 78, 1.15)]
    golilla = "M630 250 C680 160 820 150 860 240 C880 300 860 380 810 410 C760 420 700 400 660 370 Z"
    cara = "M690 340 C760 325 830 360 870 400 C892 420 884 452 850 458 L770 455 C725 445 695 405 690 340 Z"
    extra = [f'<path d="{golilla}" fill="#7a5a3a"/>', f'<path d="{golilla}" fill="none" stroke="#e8c08a" stroke-width="5" opacity="0.7"/>',
             *[f'<circle cx="{752 + 100 * math.cos(a):.0f}" cy="{292 + 112 * math.sin(a):.0f}" r="8" fill="#e8c08a" opacity="0.85"/>' for a in [k * 0.42 - 2.9 for k in range(7)]],
             f'<path d="{cara}" fill="#8a6a44"/>',
             '<path d="M780 345 C820 300 870 260 940 230 C890 280 850 320 815 360 Z" fill="#f1e4c4"/>',
             '<path d="M740 350 C770 310 810 270 870 245 C830 290 795 330 770 362 Z" fill="#e8d8b2"/>',
             '<path d="M850 395 C870 370 890 355 905 345 C895 370 880 390 865 405 Z" fill="#f1e4c4"/>',
             '<path d="M865 430 C885 440 892 455 880 462 L848 458 Z" fill="#3a2a1c"/>']
    _animal("dino_trice", 960, 660, cuerpo, lejos, cerca, extra, "#6e5a3a", "#d6c49a", manchas=12, sem=7, ojo=(790, 375, 7), sombra=(420, 625, 330, 20))


def estegosaurio():
    cuerpo = ("M60 470 C140 450 220 400 300 330 C380 270 480 255 560 290 C640 325 700 390 760 440 C800 470 840 480 880 480 "
              "C900 482 905 498 890 505 C840 510 780 505 730 495 C640 520 420 525 300 505 C200 495 120 490 60 470 Z")
    lejos = [_pata(330, 480, 640, 56, 1.2, 8), _pata(640, 480, 630, 48, 1.2)]
    cerca = [_pata(280, 480, 650, 64, 1.2, 10), _pata(600, 480, 642, 54, 1.2)]
    placas = []
    for i, (x, y, s) in enumerate([(190, 395, 50), (250, 345, 70), (320, 300, 90), (400, 275, 100), (480, 275, 95), (560, 300, 80), (630, 345, 60), (700, 395, 45)]):
        placas.append(f'<path d="M{x-s*0.45:.0f} {y+20} L{x:.0f} {y-s:.0f} L{x+s*0.45:.0f} {y+20} Z" fill="#b8553a"/>'
                      f'<path d="M{x-s*0.45:.0f} {y+20} L{x:.0f} {y-s:.0f}" stroke="#ffd08a" stroke-width="3" opacity="0.7"/>')
    puas = "".join(f'<path d="M{80+i*30} {465-i*6} L{40+i*30} {420-i*10} L{95+i*30} {455-i*6} Z" fill="#e8d8b2"/>' for i in range(2))
    _animal("dino_estego", 940, 690, cuerpo, lejos, cerca, placas + [puas], "#5e6a40", "#cfc39a", manchas=10, sem=9, ojo=(870, 470, 5), sombra=(470, 655, 360, 20))


def raptor():
    cuerpo = ("M20 250 C120 240 220 235 280 240 C320 200 380 180 430 185 C470 160 520 150 560 160 C600 170 615 190 612 205 "
              "C590 212 560 214 540 220 C530 240 505 255 470 262 C430 280 380 290 330 285 C290 282 260 272 240 266 C160 262 90 258 20 250 Z")
    lejos = ["M380 270 C410 320 400 360 380 390 L400 450 L430 455 L370 458 L360 395 C370 360 365 320 350 285 Z"]
    cerca = ["M320 260 C360 270 380 320 360 360 L330 400 L380 440 L410 445 L320 450 L300 400 C300 360 290 300 320 260 Z"]
    extra = ['<path d="M470 240 C490 260 510 270 530 262" stroke="#2a2018" stroke-width="7" stroke-linecap="round" fill="none"/>',
             *[f'<path d="M{300 + i*40} {240 - i*12} l10 -20 l8 18" fill="#c0392b" opacity="0.8"/>' for i in range(4)]]
    _animal("dino_raptor", 640, 470, cuerpo, lejos, cerca, extra, "#6a5a3a", "#d8c8a0", manchas=10, sem=11, ojo=(565, 180, 5), sombra=(330, 455, 160, 12))


def pterosaurio_detalle():
    w, h = 760, 400
    d = lg("ptw", (0, "#5a3a4a"), (1, "#2a1a24")) + lg("ptb", (0, "#6a4a3a"), (1, "#3a2a20"))
    ala = "M380 210 C320 160 220 110 30 110 C80 140 120 170 160 185 C220 200 300 215 360 230 Z"
    ala2 = "M380 210 C440 160 540 110 730 110 C680 140 640 170 600 185 C540 200 460 215 400 230 Z"
    b = [f'<path d="{ala}" fill="url(#ptw)"/>', f'<path d="{ala2}" fill="url(#ptw)"/>',
         *[f'<path d="M370 205 L{80 + i*70} {118 + i*12}" stroke="#1a0f14" stroke-width="2" opacity="0.5"/>' for i in range(4)],
         *[f'<path d="M390 205 L{680 - i*70} {118 + i*12}" stroke="#1a0f14" stroke-width="2" opacity="0.5"/>' for i in range(4)],
         '<path d="M30 110 C120 130 250 160 380 205" stroke="#ffb45a" stroke-width="3" opacity="0.6" fill="none"/>',
         '<path d="M340 215 C360 195 410 195 430 215 C440 225 470 222 520 228 L540 236 C490 242 450 246 420 246 C380 252 350 240 340 215 Z" fill="url(#ptb)"/>',
         '<path d="M440 205 C470 180 500 170 520 150 C510 175 495 195 470 210 Z" fill="#c0392b"/>',
         '<circle cx="455" cy="214" r="4" fill="#fff3c0"/>']
    guardar("pterosaurio", "".join(b), w, h, d)


def bg_jungla_rica():
    d = (lg("cj2", (0, "#1d1236"), (0.3, "#6a2a5a"), (0.5, "#d0543a"), (0.68, "#f2a65a"), (1, "#f6d08a")) +
         rg("solj2", (0, "#fff1c0", 1), (1, "#fff1c0", 0)) + lg("vol2", (0, "#6a3a3a"), (1, "#2b1a1e")) + lg("vol3", (0, "#a8604a"), (1, "#6a3a3a")))
    r = random.Random(61)
    b = ['<rect width="1080" height="1920" fill="url(#cj2)"/>',
         '<circle cx="720" cy="980" r="380" fill="url(#solj2)" opacity="0.85"/>', '<circle cx="720" cy="1000" r="105" fill="#fff4cf"/>',
         *[f'<path d="M720 1000 L{720 + 1400*math.cos(a):.0f} {1000 + 1400*math.sin(a):.0f}" stroke="#fff1c0" stroke-width="{r.uniform(30,80):.0f}" opacity="0.06"/>' for a in [k * 0.33 - 3.0 for k in range(9)]],
         '<path d="M480 1250 L800 880 L1120 1250 Z" fill="url(#vol3)" opacity="0.75"/>',
         '<rect y="1120" width="1080" height="140" fill="#f6c08a" opacity="0.35" filter="url(#blur40)"/>',
         '<path d="M-50 1280 L260 760 L330 740 L400 770 L760 1280 Z" fill="url(#vol2)"/>',
         '<path d="M300 745 L330 740 L360 755" stroke="#ff7a3a" stroke-width="10" opacity="0.8" filter="url(#blur8)" fill="none"/>',
         '<path d="M270 760 C250 640 330 560 290 460 C360 520 380 420 450 380 C470 300 420 260 480 200" stroke="#8a7070" stroke-width="80" opacity="0.3" filter="url(#blur20)" fill="none"/>',
         '<rect y="1230" width="1080" height="120" fill="#ffe0b0" opacity="0.3" filter="url(#blur20)"/>',
         '<rect y="1260" width="1080" height="660" fill="#1b2a14"/>',
         '<path d="M0 1270 C200 1230 400 1300 600 1260 C800 1225 950 1280 1080 1250 L1080 1340 L0 1340 Z" fill="#2e4520"/>']
    for x in range(-40, 1120, 80):
        y = 1310 + r.uniform(-20, 40)
        for k in range(7):
            a = -150 + k * 20 + r.uniform(-6, 6); L = r.uniform(90, 170)
            col = r.choice(["#2f4a22", "#3a5a28", "#26401c"])
            b.append(f'<path d="M{x} {y} Q{x+math.cos(math.radians(a))*L*0.6:.0f} {y+math.sin(math.radians(a))*L*0.9:.0f} '
                     f'{x+math.cos(math.radians(a))*L:.0f} {y+math.sin(math.radians(a))*L*0.6:.0f}" stroke="{col}" stroke-width="12" fill="none" stroke-linecap="round"/>')
    b += [palmera(120, 1440, 1.5, "#141f10", "#f2a65a"), palmera(960, 1480, 1.8, "#141f10", "#f2a65a"), palmera(600, 1340, 0.9, "#22341a", "#f2a65a"),
          palmera(420, 1320, 0.7, "#2a3e20", "#f2a65a"),
          '<rect y="1330" width="1080" height="90" fill="#f6d0a0" opacity="0.18" filter="url(#blur20)"/>',
          '<rect y="1520" width="1080" height="400" fill="#0f180c" opacity="0.55"/>', grano()]
    guardar("bg_jungla", "".join(b), defs=d)


# ======================================================================= METEORITO Y HOJAS (v5 densa)
def meteorito():
    """Meteorito detallado que viaja hacia la IZQUIERDA (la cola queda a la derecha): roca con cráteres y grietas
    incandescentes, frente al rojo blanco, cola de fuego en capas y chispas."""
    w, h = 1400, 520
    r = random.Random(71)
    cy = h / 2
    d = (lg("mt_c1", (0, "#fff6d0"), (0.12, "#ffd24a"), (0.4, "#ff7a1a"), (0.75, "#c2281a"), (1, "#c2281a00"), x2=1, y2=0) +
         lg("mt_c2", (0, "#ffffff"), (0.2, "#fff0a0"), (0.6, "#ffb030"), (1, "#ffb03000"), x2=1, y2=0) +
         lg("mt_h", (0, "#6a6a72"), (0.5, "#3a3a44"), (1, "#3a3a4400"), x2=1, y2=0) +
         rg("mt_r", (0, "#8a7462", 1), (0.6, "#4a3a32", 1), (1, "#1e1614", 1), cx=0.7, cy=0.35) +
         rg("mt_f", (0, "#ffffff", 1), (0.35, "#fff0a0", 0.9), (0.7, "#ff8a1a", 0.5), (1, "#ff8a1a", 0), cx=0.5, cy=0.5) +
         '<clipPath id="mt_cl"><path d="M150 260 C140 190 190 140 250 130 C310 118 370 150 385 205 C400 250 392 320 350 362 C300 400 220 398 180 360 C158 335 152 300 150 260 Z"/></clipPath>')
    roca = "M150 260 C140 190 190 140 250 130 C310 118 370 150 385 205 C400 250 392 320 350 362 C300 400 220 398 180 360 C158 335 152 300 150 260 Z"
    b = [  # humo exterior, llama exterior, llama interior
        f'<path d="M260 {cy-150} C600 {cy-190} 1000 {cy-120} 1390 {cy-20} C1000 {cy+60} 600 {cy+185} 260 {cy+150} Z" fill="url(#mt_h)" opacity="0.55" filter="url(#blur20)"/>',
        f'<path d="M230 {cy-135} C520 {cy-150} 900 {cy-80} 1300 {cy} C900 {cy+80} 520 {cy+150} 230 {cy+135} Z" fill="url(#mt_c1)" filter="url(#blur8)"/>',
        f'<path d="M240 {cy-85} C460 {cy-90} 720 {cy-40} 980 {cy} C720 {cy+40} 460 {cy+90} 240 {cy+85} Z" fill="url(#mt_c2)"/>']
    for _ in range(9):  # lenguas de fuego
        x0, y0, L = r.uniform(300, 700), cy + r.uniform(-110, 110), r.uniform(200, 520)
        b.append(f'<path d="M{x0:.0f} {y0-10:.0f} Q{x0+L*0.5:.0f} {y0+r.uniform(-30,30):.0f} {x0+L:.0f} {y0+(cy-y0)*0.5:.0f} Q{x0+L*0.5:.0f} {y0+14:.0f} {x0:.0f} {y0+10:.0f} Z" fill="#ffd24a" opacity="{r.uniform(0.35,0.7):.2f}"/>')
    for _ in range(40):  # chispas
        x0, y0 = r.uniform(380, 1350), cy + r.gauss(0, 70)
        b.append(f'<circle cx="{x0:.0f}" cy="{y0:.0f}" r="{r.uniform(2,6):.1f}" fill="{r.choice(["#fff6d0","#ffd24a","#ff8a1a"])}" opacity="{r.uniform(0.5,1):.2f}"/>')
    b += [f'<circle cx="250" cy="{cy}" r="230" fill="url(#mt_f)" opacity="0.9"/>',
          f'<path d="{roca}" fill="url(#mt_r)"/>', '<g clip-path="url(#mt_cl)">']
    for _ in range(9):  # cráteres de la roca
        x0, y0, rr = r.uniform(190, 360), r.uniform(160, 360), r.uniform(10, 26)
        b.append(f'<ellipse cx="{x0:.0f}" cy="{y0:.0f}" rx="{rr:.0f}" ry="{rr*0.8:.0f}" fill="#1e1614" opacity="0.55"/>'
                 f'<path d="M{x0-rr:.0f} {y0:.0f} A{rr:.0f} {rr*0.8:.0f} 0 0 0 {x0+rr:.0f} {y0:.0f}" stroke="#b89a80" stroke-width="2.5" opacity="0.6" fill="none"/>')
    for _ in range(7):  # grietas incandescentes
        x0, y0 = r.uniform(170, 300), r.uniform(170, 350)
        pts = " ".join(f"L{x0 + k*22 + r.uniform(-6,6):.0f} {y0 + r.uniform(-18,18):.0f}" for k in range(1, 5))
        b.append(f'<path d="M{x0:.0f} {y0:.0f} {pts}" stroke="#ffb030" stroke-width="5" opacity="0.9" fill="none" stroke-linejoin="round"/>'
                 f'<path d="M{x0:.0f} {y0:.0f} {pts}" stroke="#fff6d0" stroke-width="1.8" fill="none" stroke-linejoin="round"/>')
    b += [f'<rect width="{w}" height="{h}" fill="#888" filter="url(#grano)"/>', '</g>',
          # frente al rojo blanco (onda de choque) por delante de la roca
          f'<path d="M190 130 C110 190 100 330 190 392" stroke="#fff6d0" stroke-width="16" opacity="0.9" fill="none" stroke-linecap="round" filter="url(#blur8)"/>',
          f'<path d="M175 150 C112 205 108 318 175 372" stroke="#ffffff" stroke-width="6" fill="none" stroke-linecap="round"/>']
    guardar("meteorito", "".join(b), w, h, d)


def _hoja(x, y, L, ang, col, luz="#cfe58a"):
    return (f'<g transform="translate({x:.0f} {y:.0f}) rotate({ang:.0f})"><path d="M0 0 C{L*0.3:.0f} {-L*0.32:.0f} {L*0.8:.0f} {-L*0.25:.0f} {L:.0f} 0 '
            f'C{L*0.8:.0f} {L*0.25:.0f} {L*0.3:.0f} {L*0.32:.0f} 0 0 Z" fill="{col}"/>'
            f'<path d="M0 0 L{L:.0f} 0" stroke="{luz}" stroke-width="2" opacity="0.6"/>'
            + "".join(f'<path d="M{L*k:.0f} 0 l{L*0.12:.0f} {-L*0.12:.0f} M{L*k:.0f} 0 l{L*0.12:.0f} {L*0.12:.0f}" stroke="{luz}" stroke-width="1.2" opacity="0.45"/>' for k in (0.3, 0.5, 0.7)) + '</g>')


def rama(nombre, mordida=0):
    """Rama con hojas detalladas; `mordida` = número de bocados que le faltan (por la izquierda)."""
    w, h = 520, 360
    r = random.Random(81)
    b = ['<path d="M520 200 C400 190 280 175 120 185" stroke="#3a2a1a" stroke-width="16" stroke-linecap="round" fill="none"/>',
         '<path d="M520 196 C400 186 280 171 120 181" stroke="#8a6a44" stroke-width="4" opacity="0.6" stroke-linecap="round" fill="none"/>']
    for i in range(22):
        x = 110 + i * 18 + r.uniform(-6, 6); y = 184 + (x - 120) * 0.04
        for sgn in (-1, 1):
            b.append(_hoja(x, y, r.uniform(70, 120), sgn * r.uniform(40, 80) + 180 * (sgn < 0) * 0 + (0 if sgn > 0 else 0) - (0 if sgn > 0 else 0),
                           r.choice(["#3f7a2a", "#4f9a34", "#2f6a22", "#62a83c"])))
    cuerpo = "".join(b)
    if mordida:
        huecos = "".join(f'<circle cx="{95 + k*85}" cy="{150 + (k % 2)*70}" r="{70 - k*6}" fill="#000"/>' for k in range(mordida))
        cuerpo = (f'<mask id="mk{mordida}" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="#fff"/>{huecos}</mask>'
                  f'<g mask="url(#mk{mordida})">{cuerpo}</g>')
    guardar(nombre, cuerpo, w, h)


def arbusto():
    w, h = 460, 300
    r = random.Random(91)
    b = ['<ellipse cx="230" cy="285" rx="200" ry="14" fill="#000" opacity="0.35" filter="url(#blur8)"/>']
    for i in range(46):
        a = r.uniform(-170, -10)
        b.append(_hoja(230 + r.uniform(-90, 90), 280, r.uniform(90, 210), a, r.choice(["#2f6a22", "#3f7a2a", "#4f9a34", "#26521c"])))
    guardar("arbusto", "".join(b), w, h)


def todo_v4():
    bg_espacio_rico("bg_esp_violeta", "violeta", 3)
    bg_espacio_rico("bg_esp_petroleo", "petroleo", 5)
    bg_espacio_rico("bg_esp_ambar", "ambar", 8)
    bg_superficie_rica(); bg_eclipse_rico(); bg_jungla_rica()
    braquiosaurio(); tiranosaurio(); triceratops(); estegosaurio(); raptor(); pterosaurio_detalle()
    meteorito(); rama("rama_hojas"); rama("rama_mordida1", 1); rama("rama_mordida2", 2); arbusto()


# ------------------------------------------------------------------ personaje con expresiones (APRENDIZAJE.md, H6)
EXPRESIONES = ("neutral", "sorpresa", "feliz", "pensando", "susto", "senala")


def personaje(expr="neutral", piel=("#f2c9a0", "#d99a6c"), ropa=("#3d6fd6", "#24418f"), pelo="#3a2618", prefijo="pj"):
    """Personaje sencillo con volumen y cara expresiva, para que en el plano haya ALGUIEN que reaccione al dato
    (los Shorts ilustrados que mejor funcionan cuentan el dato a través de un personaje con emociones).
    Una ilustración por expresión: pj_neutral, pj_sorpresa, pj_feliz, pj_pensando, pj_susto, pj_senala (600×900).
    En el vídeo se cambia de una a otra con `denso.reaccion()`."""
    w, h, cx = 600, 900, 300
    defs = (lg("pj_piel", (0, piel[0]), (1, piel[1])) + lg("pj_ropa", (0, ropa[0]), (1, ropa[1]))
            + rg("pj_luz", (0, "#ffffff", 0.35), (1, "#ffffff", 0), cx=0.32, cy=0.28, r=0.6))
    b = [f'<ellipse cx="{cx}" cy="872" rx="190" ry="22" fill="#000" opacity="0.35" filter="url(#blur8)"/>']
    # brazos (detrás del cuerpo salvo el que señala)
    brazos = {
        "neutral": [(196, 560, 150, 700, 168, 760), (404, 560, 450, 700, 432, 760)],
        "feliz": [(196, 560, 120, 470, 96, 400), (404, 560, 480, 470, 504, 400)],
        "sorpresa": [(196, 560, 130, 520, 150, 430), (404, 560, 470, 520, 450, 430)],
        "susto": [(196, 560, 150, 470, 220, 410), (404, 560, 450, 470, 380, 410)],
        "pensando": [(196, 560, 150, 700, 168, 760), (404, 560, 440, 600, 350, 500)],
        "senala": [(196, 560, 150, 700, 168, 760), (404, 560, 500, 470, 560, 360)],
    }[expr]
    for x0, y0, x1, y1, x2, y2 in brazos:
        b.append(f'<path d="M{x0} {y0} Q{x1} {y1} {x2} {y2}" stroke="url(#pj_ropa)" stroke-width="58" stroke-linecap="round" fill="none"/>'
                 f'<circle cx="{x2}" cy="{y2}" r="34" fill="url(#pj_piel)"/>')
    # cuerpo y piernas
    b.append(f'<path d="M{cx-52} 800 L{cx-56} 868 M{cx+52} 800 L{cx+56} 868" stroke="#232a3d" stroke-width="56" stroke-linecap="round"/>')
    b.append(f'<path d="M{cx-120} 840 C{cx-150} 640 {cx-130} 520 {cx} 510 C{cx+130} 520 {cx+150} 640 {cx+120} 840 Z" fill="url(#pj_ropa)"/>'
             f'<path d="M{cx-120} 840 C{cx-150} 640 {cx-130} 520 {cx} 510" stroke="#ffffff" stroke-opacity="0.25" stroke-width="6" fill="none"/>'
             f'<path d="M{cx-34} 512 L{cx} 560 L{cx+34} 512" fill="{piel[1]}"/>')
    if expr in ("pensando",):   # la mano de pensar va por delante, en la barbilla
        b.append(f'<circle cx="350" cy="500" r="34" fill="url(#pj_piel)"/>')
    # cabeza
    b.append(f'<circle cx="{cx}" cy="330" r="190" fill="url(#pj_piel)"/><circle cx="{cx}" cy="330" r="190" fill="url(#pj_luz)"/>'
             f'<path d="M{cx-190} 320 C{cx-200} 150 {cx-80} 110 {cx+10} 120 C{cx+120} 110 {cx+200} 190 {cx+188} 300 C{cx+120} 220 {cx-40} 200 {cx-120} 250 C{cx-150} 270 {cx-170} 290 {cx-190} 320 Z" fill="{pelo}"/>'
             f'<ellipse cx="{cx-112}" cy="392" rx="30" ry="18" fill="#ff7a6a" opacity="0.35"/><ellipse cx="{cx+112}" cy="392" rx="30" ry="18" fill="#ff7a6a" opacity="0.35"/>')
    # ojos: (radio blanco, radio pupila, desplazamiento de la pupila)
    ojos = {"neutral": (34, 16, 0, 0), "feliz": (0, 0, 0, 0), "sorpresa": (46, 15, 0, -2), "susto": (48, 11, 0, 0),
            "pensando": (34, 16, 9, -9), "senala": (36, 16, 9, -8)}[expr]
    for sx in (-68, 68):
        ex, ey = cx + sx, 330
        if expr == "feliz":
            b.append(f'<path d="M{ex-30} {ey+6} Q{ex} {ey-30} {ex+30} {ey+6}" stroke="#20160f" stroke-width="12" stroke-linecap="round" fill="none"/>')
        else:
            rb, rp, dx, dy = ojos
            b.append(f'<ellipse cx="{ex}" cy="{ey}" rx="{rb}" ry="{rb * 1.08:.0f}" fill="#ffffff"/><circle cx="{ex+dx}" cy="{ey+dy}" r="{rp}" fill="#20160f"/>'
                     f'<circle cx="{ex+dx-5}" cy="{ey+dy-6}" r="{max(3, rp // 3)}" fill="#ffffff"/>')
    cejas = {"neutral": [(-100, 268, -36, 262), (36, 262, 100, 268)], "feliz": [(-100, 262, -36, 250), (36, 250, 100, 262)],
             "sorpresa": [(-104, 238, -36, 226), (36, 226, 104, 238)], "susto": [(-104, 232, -36, 250), (36, 250, 104, 232)],
             "pensando": [(-100, 262, -36, 270), (36, 236, 100, 248)], "senala": [(-100, 250, -36, 244), (36, 240, 100, 250)]}[expr]
    for x0, y0, x1, y1 in cejas:
        b.append(f'<path d="M{cx+x0} {y0} L{cx+x1} {y1}" stroke="{pelo}" stroke-width="14" stroke-linecap="round"/>')
    boca = {"neutral": f'<path d="M{cx-36} 430 Q{cx} 448 {cx+36} 430" stroke="#7a2e22" stroke-width="10" stroke-linecap="round" fill="none"/>',
            "feliz": f'<path d="M{cx-58} 418 Q{cx} 500 {cx+58} 418 Z" fill="#7a2e22"/><path d="M{cx-40} 426 Q{cx} 444 {cx+40} 426 L{cx+46} 420 L{cx-46} 420 Z" fill="#ffffff"/>',
            "sorpresa": f'<ellipse cx="{cx}" cy="444" rx="30" ry="40" fill="#5a1f18"/><ellipse cx="{cx}" cy="462" rx="18" ry="14" fill="#c2564a"/>',
            "susto": f'<path d="M{cx-52} 456 Q{cx-26} 416 {cx} 440 Q{cx+26} 416 {cx+52} 456 Q{cx} 486 {cx-52} 456 Z" fill="#5a1f18"/><rect x="{cx-34}" y="432" width="68" height="12" rx="4" fill="#ffffff"/>',
            "pensando": f'<path d="M{cx-30} 440 Q{cx+4} 432 {cx+38} 446" stroke="#7a2e22" stroke-width="10" stroke-linecap="round" fill="none"/>',
            "senala": f'<path d="M{cx-44} 424 Q{cx} 476 {cx+44} 424 Z" fill="#7a2e22"/>'}[expr]
    b.append(boca)
    if expr == "susto":   # gotas de sudor
        b.append(f'<path d="M{cx+170} 210 q16 26 0 40 q-16 -14 0 -40Z" fill="#9fdcff"/><path d="M{cx+205} 270 q11 18 0 28 q-11 -10 0 -28Z" fill="#9fdcff"/>')
    if expr == "senala":
        b.append(f'<path d="M548 372 L592 300" stroke="url(#pj_piel)" stroke-width="22" stroke-linecap="round"/>')
    guardar(f"{prefijo}_{expr}", "".join(b), w, h, defs)


def personajes():
    for e in EXPRESIONES:
        personaje(e)


def generar(directorio):
    """Escribe todas las ilustraciones generadas en `directorio` (siempre iguales: semillas fijas)."""
    global OUT, R, _RP
    OUT, R, _RP = directorio, random.Random(21), random.Random(7)
    for f in (pterosaurio, satelite, cohete, modulo_lunar, dinosaurio, bg_jungla, almeja_fosil, calendario, bg_eclipse, personas_mirando):
        f()
    dinosaurio("dino_peq", "#4a6a38")
    patinadora("patinadora_cerrada", "cerrados"); patinadora("patinadora_abierta", "abiertos"); bg_pista()
    todo_v4()
    personajes()
    return directorio


if __name__ == "__main__":
    import sys
    print("ok", generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
