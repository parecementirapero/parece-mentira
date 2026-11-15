"""Ilustraciones SVG del vídeo 01 (Zanzíbar) — v4: dibujo detallado con degradados, luz, sombras y textura.
Genera los SVG en ./svg/. Estilo: ilustración plana con volumen (luz de contra, sombras proyectadas,
texturas suaves con feTurbulence), paleta cálida para historia.
"""
import math, os, random

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "svg")
os.makedirs(OUT, exist_ok=True)
R = random.Random(7)

W, H = 1080, 1920


def guardar(nombre, cuerpo, w=W, h=H, defs=""):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
           f'<defs>{TEXTURA}{defs}</defs>{cuerpo}</svg>')
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


def palacio(x, y, s=1.0, ruinas=False):
    """Palacio del sultán frente al mar: cuerpo con arcadas, galería, torre del reloj. (x, y) = base centro."""
    piedra_l, piedra_s = ("#fff4dc", "#d9b98a") if not ruinas else ("#9b9284", "#5d564c")
    ventana = "#5a3a22" if not ruinas else "#1f1b18"
    g = [f'<g transform="translate({x} {y}) scale({s})">']
    # sombra proyectada
    g.append('<ellipse cx="40" cy="6" rx="470" ry="40" fill="#000" opacity="0.35" filter="url(#blur20)"/>')
    # cuerpo principal (cara iluminada + cara en sombra)
    g.append(f'<rect x="-400" y="-420" width="800" height="420" fill="{piedra_l}"/>')
    g.append(f'<polygon points="400,-420 470,-380 470,0 400,0" fill="{piedra_s}"/>')
    # cornisa
    g.append(f'<rect x="-420" y="-440" width="840" height="26" fill="{piedra_s}"/>')
    g.append(f'<rect x="-420" y="-446" width="840" height="8" fill="#fffaf0" opacity="0.8"/>')
    # galerías con arcos (2 pisos)
    for fila, yy in enumerate((-380, -190)):
        for i in range(8):
            cx = -350 + i * 100
            g.append(f'<path d="M{cx-34} {yy+150} L{cx-34} {yy+40} A34 34 0 0 1 {cx+34} {yy+40} L{cx+34} {yy+150} Z" fill="{ventana}"/>')
            g.append(f'<path d="M{cx-34} {yy+40} A34 34 0 0 1 {cx+34} {yy+40}" stroke="#ffffff" stroke-opacity="0.6" stroke-width="4" fill="none"/>')
            if not ruinas:
                g.append(f'<rect x="{cx-30}" y="{yy+110}" width="60" height="6" fill="#c9a36b"/>')
        g.append(f'<rect x="-400" y="{yy+150}" width="800" height="14" fill="{piedra_s}" opacity="0.9"/>')
    # torre del reloj
    tx = 0
    g.append(f'<rect x="{tx-70}" y="-760" width="140" height="340" fill="{piedra_l}"/>')
    g.append(f'<rect x="{tx+40}" y="-760" width="30" height="340" fill="{piedra_s}" opacity="0.8"/>')
    g.append(f'<polygon points="{tx-90},-760 {tx+90},-760 {tx},-880" fill="{"#b23a2a" if not ruinas else "#4a4038"}"/>')
    g.append(f'<polygon points="{tx},-880 {tx+90},-760 {tx+40},-760" fill="#000" opacity="0.25"/>')
    if not ruinas:
        g.append(f'<circle cx="{tx}" cy="-660" r="46" fill="#fffaf0" stroke="#7a5a2e" stroke-width="8"/>')
        g.append(f'<line x1="{tx}" y1="-660" x2="{tx}" y2="-692" stroke="#2a2a33" stroke-width="6"/>')
        g.append(f'<line x1="{tx}" y1="-660" x2="{tx+22}" y2="-660" stroke="#2a2a33" stroke-width="6"/>')
    else:
        # boquetes, grietas, cascotes
        for bx, by, r in ((-220, -300, 90), (160, -120, 110), (-40, -560, 70), (300, -360, 70)):
            pts = " ".join(f"{bx+math.cos(a)*r*(0.6+R.random()*0.5):.0f},{by+math.sin(a)*r*(0.6+R.random()*0.5):.0f}"
                           for a in [i * math.pi / 5 for i in range(10)])
            g.append(f'<polygon points="{pts}" fill="#120f0d"/>')
        for i in range(26):
            cx, cy = R.uniform(-460, 480), R.uniform(-30, 10)
            r = R.uniform(14, 46)
            g.append(f'<polygon points="{cx-r},{cy} {cx-r*0.3},{cy-r*0.9} {cx+r*0.6},{cy-r*0.6} {cx+r},{cy}" fill="{R.choice(["#6e665b","#857c6f","#4c463f"])}"/>')
        g.append('<rect x="-400" y="-420" width="800" height="420" fill="#2b2620" opacity="0.25"/>')
    g.append('</g>')
    return "".join(g)


def barco_guerra(nombre="crucero", s=1.0):
    """Crucero de finales del XIX visto de lado, mirando a la izquierda. Lienzo 900x420, línea de flotación y=320."""
    d = lg("casco", (0, "#4a515e"), (1, "#1c2027")) + lg("sup", (0, "#f4f1e6"), (1, "#b9b5a6")) + \
        lg("chim", (0, "#e0b45a"), (1, "#8a6224"))
    b = ['<ellipse cx="450" cy="330" rx="430" ry="26" fill="#000" opacity="0.3" filter="url(#blur8)"/>']
    b.append('<path d="M40 250 L860 250 L820 330 L110 330 Z" fill="url(#casco)"/>')
    b.append('<path d="M110 318 L820 318 L812 330 L116 330 Z" fill="#8e2a22"/>')
    b.append('<path d="M40 250 L860 250 L856 258 L44 258 Z" fill="#c9c4b4"/>')
    for i in range(14):
        b.append(f'<circle cx="{150+i*48}" cy="285" r="6" fill="#ffd77a" opacity="0.8"/>')
    b.append('<rect x="240" y="190" width="420" height="62" fill="url(#sup)"/>')
    b.append('<rect x="320" y="150" width="200" height="44" fill="url(#sup)"/>')
    for cx in (360, 470):
        b.append(f'<rect x="{cx}" y="40" width="54" height="130" rx="6" fill="url(#chim)"/>')
        b.append(f'<rect x="{cx}" y="40" width="54" height="14" fill="#2a2a2a"/>')
    b.append('<line x1="250" y1="190" x2="250" y2="10" stroke="#2c2f36" stroke-width="8"/>')
    b.append('<line x1="640" y1="190" x2="640" y2="30" stroke="#2c2f36" stroke-width="8"/>')
    b.append('<line x1="250" y1="20" x2="640" y2="40" stroke="#2c2f36" stroke-width="2"/>')
    b.append('<rect x="70" y="232" width="110" height="20" rx="8" fill="#3a3f48"/>')
    b.append('<rect x="-30" y="236" width="120" height="12" rx="6" fill="#2a2e35"/>')
    b.append('<rect x="700" y="232" width="110" height="20" rx="8" fill="#3a3f48"/>')
    # bandera británica de popa (esquemática)
    b.append('<g transform="translate(830 180)"><rect width="60" height="38" fill="#c8102e"/>'
             '<rect width="26" height="18" fill="#012169"/><path d="M0 0 L26 18 M26 0 L0 18" stroke="#fff" stroke-width="3"/></g>')
    b.append('<line x1="830" y1="180" x2="830" y2="250" stroke="#2c2f36" stroke-width="4"/>')
    guardar(nombre, "".join(b), 900, 420, d)


def yate():
    d = lg("yh", (0, "#ffffff"), (1, "#c8cbd2")) + lg("yc", (0, "#e7c070"), (1, "#9a6c22"))
    b = ['<ellipse cx="360" cy="300" rx="330" ry="22" fill="#000" opacity="0.3" filter="url(#blur8)"/>',
         '<path d="M20 230 Q60 300 160 300 L620 300 Q690 270 700 230 Z" fill="url(#yh)"/>',
         '<path d="M40 268 L680 268" stroke="#b23a2a" stroke-width="8"/>',
         '<rect x="200" y="170" width="300" height="62" rx="10" fill="url(#yh)"/>',
         '<rect x="320" y="70" width="46" height="110" rx="6" fill="url(#yc)"/>',
         '<line x1="160" y1="230" x2="160" y2="20" stroke="#5b4a3a" stroke-width="7"/>',
         '<line x1="560" y1="230" x2="560" y2="50" stroke="#5b4a3a" stroke-width="7"/>',
         '<g transform="translate(560 50)"><path d="M0 0 L70 14 L0 30 Z" fill="#c0392b"/></g>']
    for i in range(8):
        b.append(f'<rect x="{220+i*36}" y="190" width="20" height="18" rx="3" fill="#2a4a6a"/>')
    guardar("yate", "".join(b), 720, 330, d)


def silueta(nombre, sombrero="turbante", luz="#ffb45a", ancho=300, alto=760, arma=False):
    """Personaje en contraluz (silueta con borde iluminado)."""
    cab = {"turbante": '<ellipse cx="150" cy="110" rx="62" ry="46" fill="#1a1412"/><circle cx="150" cy="150" r="52" fill="#1a1412"/>',
           "salacot": '<ellipse cx="150" cy="104" rx="96" ry="22" fill="#1a1412"/><ellipse cx="150" cy="92" rx="62" ry="44" fill="#1a1412"/><circle cx="150" cy="150" r="48" fill="#1a1412"/>',
           "corona": '<circle cx="150" cy="150" r="52" fill="#1a1412"/><ellipse cx="150" cy="104" rx="64" ry="44" fill="#1a1412"/>'}[sombrero]
    cuerpo = ('<path d="M70 230 Q150 190 230 230 L262 700 Q150 730 38 700 Z" fill="#1a1412"/>'
              '<rect x="120" y="190" width="60" height="50" fill="#1a1412"/>')
    brazos = ('<path d="M74 240 L30 470 L58 478 L104 260 Z" fill="#1a1412"/>'
              '<path d="M226 240 L270 470 L242 478 L196 260 Z" fill="#1a1412"/>')
    extra = ""
    if arma:
        extra = '<rect x="250" y="250" width="12" height="380" rx="5" fill="#1a1412" transform="rotate(12 256 440)"/>'
    if sombrero == "corona":
        extra += ('<path d="M100 96 L118 54 L136 84 L150 44 L164 84 L182 54 L200 96 Z" fill="#f1c24f"/>'
                  '<path d="M100 96 L200 96 L200 110 L100 110 Z" fill="#d49b16"/>')
    borde = (f'<path d="M262 700 L230 230 Q190 205 160 200" stroke="{luz}" stroke-width="7" fill="none" opacity="0.9"/>'
             f'<path d="M202 120 Q214 150 196 190" stroke="{luz}" stroke-width="6" fill="none" opacity="0.9"/>'
             f'<path d="M270 470 L226 240" stroke="{luz}" stroke-width="5" fill="none" opacity="0.8"/>')
    guardar(nombre, cab + cuerpo + brazos + extra + borde, ancho, alto)


# ------------------------------------------------------------------ fondos completos
def bg_estadio():
    d = (lg("cie", (0, "#05070f"), (0.6, "#121a33"), (1, "#24345e")) +
         lg("cesped", (0, "#2f7d3c"), (1, "#123d1c")) +
         rg("foco", (0, "#fffbe0", 1), (0.25, "#fff2b0", 0.55), (1, "#fff2b0", 0)))
    b = ['<rect width="1080" height="1920" fill="url(#cie)"/>']
    # gradas con público (puntos)
    b.append('<path d="M0 620 L1080 620 L1080 1000 L0 1000 Z" fill="#0d1224"/>')
    for fila in range(16):
        y = 640 + fila * 22
        for i in range(70):
            x = i * 16 + (fila % 2) * 8 + R.uniform(-3, 3)
            c = R.choice(["#2a3561", "#3b4a80", "#5d6aa8", "#c94b4b", "#e8e0d0", "#1e2747"])
            b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{5+fila*0.15:.1f}" fill="{c}" opacity="{0.55+fila*0.02:.2f}"/>')
    # torres de focos
    for fx in (120, 960):
        b.append(f'<rect x="{fx-6}" y="250" width="12" height="400" fill="#0a0d18"/>')
        b.append(f'<rect x="{fx-70}" y="220" width="140" height="70" rx="8" fill="#151b2e"/>')
        for i in range(4):
            b.append(f'<circle cx="{fx-48+i*32}" cy="255" r="12" fill="#fff8d8"/>')
        b.append(f'<circle cx="{fx}" cy="255" r="380" fill="url(#foco)"/>')
    # césped en perspectiva con franjas
    b.append('<polygon points="-300,1920 1380,1920 900,980 180,980" fill="url(#cesped)"/>')
    for i in range(9):
        y0 = 980 + (i / 9) ** 1.6 * 940
        y1 = 980 + ((i + 1) / 9) ** 1.6 * 940
        if i % 2:
            def xl(y): return 180 - (y - 980) / 940 * 480
            def xr(y): return 900 + (y - 980) / 940 * 480
            b.append(f'<polygon points="{xl(y0):.0f},{y0:.0f} {xr(y0):.0f},{y0:.0f} {xr(y1):.0f},{y1:.0f} {xl(y1):.0f},{y1:.0f}" fill="#ffffff" opacity="0.06"/>')
    b.append('<polygon points="200,1000 880,1000 1240,1880 -160,1880" fill="none" stroke="#ffffff" stroke-opacity="0.85" stroke-width="6"/>')
    b.append('<line x1="540" y1="1000" x2="540" y2="1880" stroke="#fff" stroke-opacity="0" />')
    b.append('<line x1="20" y1="1300" x2="1060" y2="1300" stroke="#ffffff" stroke-opacity="0.85" stroke-width="6"/>')
    b.append('<ellipse cx="540" cy="1300" rx="190" ry="70" fill="none" stroke="#ffffff" stroke-opacity="0.85" stroke-width="6"/>')
    # neblina de luz sobre el campo
    b.append('<rect y="900" width="1080" height="260" fill="#cfe0ff" opacity="0.10" filter="url(#blur40)"/>')
    b.append(grano())
    guardar("bg_estadio", "".join(b), defs=d)


def marcador():
    d = lg("mk", (0, "#1b2236"), (1, "#0b0f1c"))
    b = ['<rect x="10" y="10" width="880" height="380" rx="36" fill="url(#mk)" stroke="#3a4670" stroke-width="6" filter="url(#sombra)"/>',
         '<rect x="40" y="40" width="820" height="60" rx="14" fill="#0a0e19"/>',
         '<text x="450" y="84" font-family="DejaVu Sans" font-weight="bold" font-size="36" fill="#9fb3e6" text-anchor="middle" letter-spacing="6">DURACIÓN</text>',
         '<text x="60" y="190" font-family="DejaVu Sans" font-weight="bold" font-size="40" fill="#e8ecf7">PARTIDO</text>',
         '<text x="60" y="320" font-family="DejaVu Sans" font-weight="bold" font-size="40" fill="#ff8a7a">GUERRA</text>']
    guardar("marcador", "".join(b), 900, 400, d)


def bg_mapa():
    d = rg("quemado", (0.55, "#000", 0), (1, "#3a1d05", 0.75)) + lg("pap", (0, "#f3e2b8"), (1, "#d9bf85"))
    b = ['<rect width="1080" height="1920" fill="url(#pap)"/>', '<rect width="1080" height="1920" filter="url(#papel)"/>']
    # retícula
    for i in range(0, 1080, 120):
        b.append(f'<line x1="{i}" y1="0" x2="{i}" y2="1920" stroke="#8a6a3a" stroke-opacity="0.25" stroke-width="2"/>')
    for j in range(0, 1920, 120):
        b.append(f'<line x1="0" y1="{j}" x2="1080" y2="{j}" stroke="#8a6a3a" stroke-opacity="0.25" stroke-width="2"/>')
    # costa de África oriental (izquierda) con sombreado de mar
    costa = "M0 0 L380 0 C360 200 420 330 400 520 C380 700 300 820 330 1000 C360 1200 290 1350 310 1560 C330 1720 260 1840 270 1920 L0 1920 Z"
    b.append(f'<path d="{costa}" fill="#cfae6c" stroke="#6b4a22" stroke-width="5"/>')
    for k in range(1, 7):
        b.append(f'<path d="{costa}" fill="none" stroke="#6b8aa0" stroke-opacity="{0.28-k*0.035:.2f}" stroke-width="3" transform="translate({k*16} 0)"/>')
    # isla de Zanzíbar
    isla = "M640 820 C700 760 760 800 770 880 C790 980 760 1080 720 1150 C690 1210 640 1200 630 1130 C610 1030 600 900 640 820 Z"
    for k in range(1, 6):
        b.append(f'<path d="{isla}" fill="none" stroke="#6b8aa0" stroke-opacity="{0.3-k*0.05:.2f}" stroke-width="3" transform="translate(690 1000) scale({1+k*0.06}) translate(-690 -1000)"/>')
    b.append(f'<path d="{isla}" fill="#d9b874" stroke="#6b4a22" stroke-width="5"/>')
    b.append('<text x="820" y="1000" font-family="DejaVu Serif" font-style="italic" font-size="44" fill="#4a2f12">Zanzíbar</text>')
    b.append('<text x="60" y="760" font-family="DejaVu Serif" font-style="italic" font-size="40" fill="#4a2f12" transform="rotate(-80 120 760)">ÁFRICA ORIENTAL</text>')
    b.append('<text x="700" y="1500" font-family="DejaVu Serif" font-style="italic" font-size="38" fill="#3c5b70">Océano Índico</text>')
    # rosa de los vientos
    cx, cy = 870, 1720
    b.append(f'<circle cx="{cx}" cy="{cy}" r="110" fill="none" stroke="#6b4a22" stroke-width="4"/>')
    for a in range(0, 360, 45):
        L = 120 if a % 90 == 0 else 70
        x2, y2 = cx + math.sin(math.radians(a)) * L, cy - math.cos(math.radians(a)) * L
        xl, yl = cx + math.sin(math.radians(a + 90)) * 16, cy - math.cos(math.radians(a + 90)) * 16
        b.append(f'<polygon points="{cx},{cy} {xl:.0f},{yl:.0f} {x2:.0f},{y2:.0f}" fill="#6b4a22"/>')
    b.append(f'<text x="{cx}" y="{cy-130}" font-family="DejaVu Serif" font-size="36" fill="#4a2f12" text-anchor="middle">N</text>')
    b.append('<rect width="1080" height="1920" fill="url(#quemado)"/>')
    b.append(grano())
    guardar("bg_mapa", "".join(b), defs=d)


def chincheta():
    d = rg("cb", (0, "#ff8a7a", 1), (0.6, "#d62f22", 1), (1, "#8a1a12", 1), cx=0.35, cy=0.35)
    b = ['<ellipse cx="60" cy="188" rx="22" ry="8" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<line x1="60" y1="90" x2="60" y2="186" stroke="#7b7f88" stroke-width="7" stroke-linecap="round"/>',
         '<circle cx="60" cy="62" r="52" fill="url(#cb)"/>', '<circle cx="44" cy="44" r="14" fill="#fff" opacity="0.7"/>']
    guardar("chincheta", "".join(b), 120, 200, d)


def bg_palacio(nombre="bg_palacio", hora="tarde", ruinas=False):
    if hora == "tarde":
        cielo = lg("c", (0, "#2c3a6b"), (0.45, "#e98a5a"), (0.7, "#ffc97a"), (1, "#ffe2a8"))
        mar = lg("m", (0, "#f4a865"), (0.2, "#2a6e8f"), (1, "#0f3550"))
        sol = rg("s", (0, "#fff6d2", 1), (0.2, "#ffd27a", 0.8), (1, "#ffb05a", 0))
    elif hora == "manana":
        cielo = lg("c", (0, "#6aa6d9"), (0.6, "#bfe0f0"), (1, "#fbe6c0"))
        mar = lg("m", (0, "#7fc0d8"), (0.3, "#2a7aa0"), (1, "#0f3a5a"))
        sol = rg("s", (0, "#ffffff", 0.9), (0.3, "#fff1c4", 0.5), (1, "#fff1c4", 0))
    else:  # ruinas: cielo gris con humo
        cielo = lg("c", (0, "#3b3d45"), (0.6, "#7d7468"), (1, "#c9a27a"))
        mar = lg("m", (0, "#8a7d6d"), (0.25, "#3d4d58"), (1, "#18242d"))
        sol = rg("s", (0, "#ffcf9a", 0.6), (1, "#ffcf9a", 0))
    d = cielo + mar + sol + lg("arena", (0, "#e8c890"), (1, "#b58a52"))
    b = ['<rect width="1080" height="1920" fill="url(#c)"/>',
         '<circle cx="760" cy="520" r="520" fill="url(#s)"/>']
    # nubes alargadas
    for i in range(6):
        y = R.uniform(150, 700)
        x = R.uniform(-100, 900)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{R.uniform(140,300):.0f}" ry="{R.uniform(16,34):.0f}" fill="#fff4e0" opacity="0.35" filter="url(#blur8)"/>')
    # costa lejana y ciudad de piedra
    b.append('<path d="M0 1010 L1080 990 L1080 1060 L0 1070 Z" fill="#6d6a7a" opacity="0.6"/>')
    for i in range(22):
        x = i * 52 + R.uniform(-10, 10)
        h = R.uniform(30, 90)
        b.append(f'<rect x="{x:.0f}" y="{1030-h:.0f}" width="{R.uniform(36,56):.0f}" height="{h:.0f}" fill="#8d8798" opacity="0.7"/>')
    b.append(palacio(540, 1180, 0.9, ruinas))
    if ruinas:
        for i in range(5):
            x = R.uniform(250, 830)
            b.append(f'<path d="M{x:.0f} 900 C{x-80:.0f} 700 {x+90:.0f} 500 {x:.0f} 200" stroke="#2c2a2a" stroke-width="{R.uniform(80,150):.0f}" opacity="0.35" fill="none" filter="url(#blur40)"/>')
    # paseo marítimo y mar
    b.append('<rect y="1180" width="1080" height="70" fill="#c9b08a"/>')
    b.append('<rect y="1180" width="1080" height="10" fill="#fff1d0" opacity="0.7"/>')
    b.append('<rect y="1250" width="1080" height="670" fill="url(#m)"/>')
    for i in range(60):
        y = 1270 + (i / 60) ** 1.4 * 640
        x = R.uniform(0, 1080)
        w = 20 + (y - 1250) * 0.12
        b.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{2+(y-1250)*0.008:.1f}" rx="2" fill="#fff6dc" opacity="{R.uniform(0.15,0.4):.2f}"/>')
    b.append(palmera(70, 1190, 0.9))
    b.append(palmera(1010, 1190, 0.8))
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def bandera():
    b = '<path d="M0 0 C60 -10 120 20 200 0 L200 110 C120 130 60 100 0 110 Z" fill="#c62828"/>' \
        '<path d="M0 0 C60 -10 120 20 200 0 L200 20 C120 40 60 10 0 20 Z" fill="#ffffff" opacity="0.25"/>'
    guardar("bandera_roja", '<g transform="translate(10 20)">' + b + '</g><rect x="0" y="0" width="10" height="400" fill="#3a2a1a"/>', 220, 400)


def carta():
    d = lg("cp", (0, "#f7ebcd"), (1, "#dcc690")) + rg("lacre", (0, "#e0473a", 1), (1, "#7a1610", 1), cx=0.4, cy=0.4)
    b = ['<g filter="url(#sombra)"><path d="M40 40 L700 20 L720 960 L30 980 Z" fill="url(#cp)"/></g>',
         '<path d="M40 40 L700 20 L720 960 L30 980 Z" filter="url(#papel)"/>',
         '<text x="380" y="190" font-family="DejaVu Serif" font-weight="bold" font-size="72" fill="#3a2410" text-anchor="middle" letter-spacing="6">ULTIMÁTUM</text>',
         '<line x1="120" y1="230" x2="640" y2="226" stroke="#3a2410" stroke-width="3"/>']
    for i in range(10):
        w = R.uniform(380, 520)
        b.append(f'<path d="M120 {300+i*52} q{w/4} -10 {w/2} 0 t{w/2} 0" stroke="#4a3018" stroke-width="5" fill="none" opacity="0.75"/>')
    b.append('<circle cx="560" cy="860" r="70" fill="url(#lacre)"/>')
    b.append('<circle cx="560" cy="860" r="44" fill="none" stroke="#5a0f0a" stroke-width="5"/>')
    b.append('<text x="560" y="878" font-family="DejaVu Serif" font-weight="bold" font-size="48" fill="#5a0f0a" text-anchor="middle">GB</text>')
    guardar("carta", "".join(b), 760, 1020, d)


def defensores():
    b = []
    for i in range(30):
        x = 20 + i * 34 + R.uniform(-6, 6)
        y = 110 + R.uniform(-10, 10)
        b.append(f'<circle cx="{x:.0f}" cy="{y-58:.0f}" r="16" fill="#1a1412"/>'
                 f'<rect x="{x-16:.0f}" y="{y-44:.0f}" width="32" height="70" rx="10" fill="#1a1412"/>')
        if i % 3 == 0:
            b.append(f'<line x1="{x+10:.0f}" y1="{y-30:.0f}" x2="{x+30:.0f}" y2="{y-110:.0f}" stroke="#1a1412" stroke-width="5"/>')
    # muro de sacos
    for fila in range(3):
        for i in range(16):
            x = i * 70 + (fila % 2) * 35 - 20
            y = 150 + fila * 44
            b.append(f'<ellipse cx="{x}" cy="{y}" rx="40" ry="24" fill="#b89a6a" stroke="#6e5634" stroke-width="3"/>'
                     f'<ellipse cx="{x-8}" cy="{y-8}" rx="22" ry="8" fill="#e3c99a" opacity="0.6"/>')
    guardar("defensores", "".join(b), 1100, 280)


def reloj_bolsillo():
    d = rg("oro", (0, "#fff1b0", 1), (0.5, "#e2b13c", 1), (1, "#8a5c12", 1), cx=0.35, cy=0.3) + \
        rg("esf", (0, "#fffdf4", 1), (1, "#e9dcc0", 1))
    b = ['<circle cx="300" cy="330" r="270" fill="#000" opacity="0.4" filter="url(#blur20)"/>',
         '<rect x="270" y="10" width="60" height="70" rx="20" fill="url(#oro)"/>',
         '<circle cx="300" cy="30" r="34" fill="none" stroke="url(#oro)" stroke-width="14"/>',
         '<circle cx="300" cy="320" r="260" fill="url(#oro)"/>',
         '<circle cx="300" cy="320" r="226" fill="url(#esf)"/>',
         '<circle cx="300" cy="320" r="226" fill="none" stroke="#7a5a1e" stroke-width="4"/>']
    for i in range(60):
        a = math.radians(i * 6)
        r1 = 206 if i % 5 else 186
        b.append(f'<line x1="{300+math.sin(a)*r1:.1f}" y1="{320-math.cos(a)*r1:.1f}" x2="{300+math.sin(a)*216:.1f}" y2="{320-math.cos(a)*216:.1f}" stroke="#2a2a33" stroke-width="{6 if i % 5 == 0 else 2}"/>')
    rom = ["XII", "I", "II", "III", "IIII", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
    for i, t in enumerate(rom):
        a = math.radians(i * 30)
        b.append(f'<text x="{300+math.sin(a)*152:.0f}" y="{334-math.cos(a)*152:.0f}" font-family="DejaVu Serif" font-size="34" fill="#2a2a33" text-anchor="middle">{t}</text>')
    b.append('<ellipse cx="230" cy="220" rx="120" ry="60" fill="#ffffff" opacity="0.25" transform="rotate(-30 230 220)"/>')
    guardar("reloj_bolsillo", "".join(b), 600, 600, d)
    # agujas centradas en su lienzo (el centro del SVG = eje)
    guardar("aguja_min", '<path d="M93 100 L100 8 L107 100 Z" fill="#1b1b22"/><circle cx="100" cy="100" r="10" fill="#1b1b22"/>', 200, 200)
    guardar("aguja_hora", '<path d="M92 100 L100 36 L108 100 Z" fill="#1b1b22"/><circle cx="100" cy="100" r="12" fill="#c0392b"/>', 200, 200)


def balanza():
    d = lg("br", (0, "#ffe7a0"), (0.5, "#d4a23a"), (1, "#7a5212"), x2=1, y2=0)
    base = ['<ellipse cx="400" cy="1000" rx="300" ry="40" fill="#000" opacity="0.4" filter="url(#blur20)"/>',
            '<path d="M260 990 L540 990 L500 940 L300 940 Z" fill="url(#br)"/>',
            '<rect x="384" y="200" width="32" height="750" fill="url(#br)"/>',
            '<circle cx="400" cy="190" r="34" fill="url(#br)"/>']
    guardar("balanza_base", "".join(base), 800, 1040, d)
    # viga con la barra en el centro exacto del lienzo (800x900, eje en y=450) para que gire sobre el pivote
    viga = ['<rect x="20" y="438" width="760" height="24" rx="12" fill="url(#br)"/>', '<circle cx="400" cy="450" r="22" fill="url(#br)"/>']
    for side in (60, 740):
        viga.append(f'<line x1="{side}" y1="450" x2="{side-110}" y2="770" stroke="#8a6a2a" stroke-width="4"/>'
                    f'<line x1="{side}" y1="450" x2="{side+110}" y2="770" stroke="#8a6a2a" stroke-width="4"/>'
                    f'<path d="M{side-150} 770 Q{side} 830 {side+150} 770 Z" fill="url(#br)"/>')
    for i in range(160):
        x = 60 + R.uniform(-120, 120)
        y = 760 - abs(R.gauss(0, 30)) - (120 - abs(x - 60)) * 0.35
        viga.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{R.choice(["#c0392b","#e74c3c","#a93226"])}"/>')
    viga.append('<circle cx="740" cy="754" r="12" fill="#3b82f6" stroke="#fff" stroke-width="3"/>')
    guardar("balanza_viga", "".join(viga), 800, 900, d)


def todo():
    bg_estadio(); marcador(); bg_mapa(); chincheta()
    bg_palacio("bg_palacio", "tarde"); bg_palacio("bg_puerto_manana", "manana"); bg_palacio("bg_ruinas", "ruinas", True)
    bandera(); carta(); defensores(); reloj_bolsillo(); balanza(); yate()
    barco_guerra("crucero")
    silueta("jalid", "turbante", "#ffb45a"); silueta("oficial", "salacot", "#ffd59a")
    silueta("sultan_nuevo", "corona", "#ffd27a"); silueta("guardia", "turbante", "#ffb45a", arma=True)


if __name__ == "__main__":
    todo()
    print(sorted(os.listdir(OUT)))
