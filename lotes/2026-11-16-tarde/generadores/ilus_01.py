"""Ilustraciones SVG del vídeo 01 (crujirse los nudillos) — estilo v4."""
from base import guardar, lg, rg, grano, R

PIEL = lg("piel", (0, "#f2c29b"), (0.55, "#d99a72"), (1, "#a8694a"), x2=1, y2=0)
PIEL_D = lg("pield", (0, "#c98763"), (1, "#8c5236"))
# nudillos (centro de cada dedo, y del nudillo) en el lienzo 520x760 de la mano izquierda
DEDOS = [(150, 70, 300), (232, 40, 300), (314, 52, 300), (392, 110, 300)]  # (x, punta_y, nudillo_y)


def mano(nombre="mano_izq", espejo=False, roja=False):
    """Dorso de una mano izquierda (pulgar a la derecha), dedos hacia arriba. Lienzo 520x760."""
    b = ['<ellipse cx="270" cy="740" rx="200" ry="18" fill="#000" opacity="0.35" filter="url(#blur8)"/>']
    # antebrazo y puño de la camisa
    b.append('<path d="M150 560 L390 560 L400 760 L140 760 Z" fill="url(#pield)"/>')
    b.append('<path d="M128 640 L412 640 L420 760 L120 760 Z" fill="#e8eef5"/><path d="M128 640 L412 640 L414 660 L126 660 Z" fill="#b9c4d2"/>')
    # dedos
    for i, (x, top, kn) in enumerate(DEDOS):
        w = 70 if i < 3 else 58
        b.append(f'<rect x="{x-w/2}" y="{top}" width="{w}" height="{kn-top+60}" rx="{w/2}" fill="url(#piel)"/>')
        b.append(f'<rect x="{x-w/2}" y="{top}" width="{w*0.35:.0f}" height="{kn-top+40}" rx="{w/5}" fill="#fff" opacity="0.13"/>')
        for k in (0.36, 0.66):  # pliegues de las falanges
            y = top + (kn - top) * k
            b.append(f'<path d="M{x-w*0.3} {y:.0f} Q{x} {y+8:.0f} {x+w*0.3} {y:.0f}" stroke="#8c5236" stroke-width="4" fill="none" opacity="0.6"/>')
        b.append(f'<path d="M{x-16} {top+22} Q{x} {top+8} {x+16} {top+22} L{x+14} {top+44} Q{x} {top+50} {x-14} {top+44} Z" fill="#f7d9c4" opacity="0.8"/>')  # uña
    # palma (dorso)
    b.append('<path d="M108 300 Q100 470 150 580 L390 580 Q440 470 430 330 Q420 290 380 290 L130 290 Q108 290 108 300 Z" fill="url(#piel)"/>')
    b.append('<path d="M108 300 Q100 470 150 580 L200 580 Q160 470 170 300 Z" fill="#fff" opacity="0.10"/>')
    b.append('<path d="M330 300 Q420 300 430 330 Q440 470 390 580 L340 580 Q380 470 360 300 Z" fill="#000" opacity="0.12"/>')
    # pulgar
    b.append('<path d="M410 400 Q480 360 500 280 Q510 240 480 236 Q456 236 448 280 Q430 340 390 370 Z" fill="url(#piel)"/>')
    b.append('<path d="M470 246 Q486 238 494 252 L490 276 Q478 280 466 272 Z" fill="#f7d9c4" opacity="0.8"/>')
    # tendones y nudillos
    for x, top, kn in DEDOS:
        b.append(f'<path d="M{x} {kn+20} Q{x+6} {kn+140} {270} 560" stroke="#b97a56" stroke-width="5" fill="none" opacity="0.5"/>')
        col = "#d2543c" if roja else "#c98763"
        b.append(f'<ellipse cx="{x}" cy="{kn}" rx="24" ry="16" fill="{col}" opacity="{0.85 if roja else 0.7}"/>')
        b.append(f'<ellipse cx="{x-4}" cy="{kn-5}" rx="12" ry="6" fill="#fff" opacity="0.35"/>')
    cuerpo = "".join(b)
    if espejo:
        cuerpo = f'<g transform="translate(520 0) scale(-1 1)">{cuerpo}</g>'
    guardar(nombre, cuerpo, 520, 760, PIEL + PIEL_D)


def radiografia(nombre="rx_mano", espejo=False, artritis=False):
    """Radiografía de una mano (fondo transparente, huesos cian luminosos). Lienzo 520x760."""
    d = rg("hue", (0, "#eaffff", 1), (0.7, "#9fe6ff", 0.9), (1, "#5bc4ff", 0.6))
    b = ['<rect x="20" y="10" width="480" height="740" rx="30" fill="#061a2c" opacity="0.92"/>',
         '<rect x="20" y="10" width="480" height="740" rx="30" fill="none" stroke="#4aa8d8" stroke-width="4" opacity="0.6"/>',
         # silueta de partes blandas
         '<path d="M108 300 Q100 470 150 640 L390 640 Q440 470 430 330 L430 300 Z" fill="#2a6a90" opacity="0.35"/>']
    for i, (x, top, kn) in enumerate(DEDOS):
        w = 70 if i < 3 else 58
        b.append(f'<rect x="{x-w/2}" y="{top}" width="{w}" height="{kn-top+60}" rx="{w/2}" fill="#2a6a90" opacity="0.35"/>')
        # falanges
        segs = [top + 14, top + (kn - top) * 0.36, top + (kn - top) * 0.68, kn - 6]
        for a, z in zip(segs, segs[1:]):
            ww = w * 0.36
            b.append(f'<rect x="{x-ww/2:.0f}" y="{a+6:.0f}" width="{ww:.0f}" height="{z-a-12:.0f}" rx="{ww/2.4:.0f}" fill="url(#hue)" filter="url(#glow)"/>')
        # metacarpiano
        b.append(f'<path d="M{x-12} {kn+8} L{x+12} {kn+8} L{270+(x-270)*0.35+10:.0f} 560 L{270+(x-270)*0.35-10:.0f} 560 Z" fill="url(#hue)" filter="url(#glow)"/>')
        b.append(f'<ellipse cx="{x}" cy="{kn+6}" rx="18" ry="12" fill="url(#hue)"/>')
        if artritis:
            b.append(f'<circle cx="{x}" cy="{kn}" r="34" fill="#ff3b2f" opacity="0.55" filter="url(#blur8)"/>')
    # pulgar y carpo
    b.append('<path d="M392 470 L470 300 L486 306 L412 480 Z" fill="url(#hue)" filter="url(#glow)"/>')
    b.append('<rect x="460" y="246" width="24" height="56" rx="10" fill="url(#hue)" transform="rotate(16 472 274)"/>')
    for i in range(8):
        b.append(f'<ellipse cx="{200 + (i % 4) * 46}" cy="{580 + (i // 4) * 40}" rx="20" ry="16" fill="url(#hue)" opacity="0.85"/>')
    b.append('<rect x="190" y="660" width="40" height="90" rx="14" fill="url(#hue)" opacity="0.8"/><rect x="290" y="660" width="44" height="90" rx="14" fill="url(#hue)" opacity="0.8"/>')
    cuerpo = "".join(b)
    if espejo:
        cuerpo = f'<g transform="translate(520 0) scale(-1 1)">{cuerpo}</g>'
    guardar(nombre, cuerpo, 520, 760, d)


def bg_salon():
    """Salón de noche con lámpara de pie, sillón y ventana (luz cálida)."""
    d = (lg("pared", (0, "#3b2a24"), (1, "#5a3d2e")) + lg("suelo", (0, "#6b4630"), (1, "#2c1a10")) +
         rg("lamp", (0, "#ffe9b0", 0.9), (0.4, "#ffb860", 0.35), (1, "#ff9a40", 0)) + lg("sil", (0, "#7a2f2a"), (1, "#4a1a18")))
    b = ['<rect width="1080" height="1920" fill="url(#pared)"/>']
    for i in range(14):  # papel pintado de rayas
        b.append(f'<rect x="{i*80}" y="0" width="34" height="1300" fill="#000" opacity="0.06"/>')
    b += ['<rect x="620" y="300" width="360" height="520" fill="#0d1630"/>',
          '<circle cx="880" cy="400" r="40" fill="#f3f0dc" opacity="0.9"/>',
          '<rect x="620" y="300" width="360" height="520" fill="none" stroke="#2a1a12" stroke-width="22"/>',
          '<path d="M800 300 V820 M620 560 H980" stroke="#2a1a12" stroke-width="12"/>',
          '<path d="M600 280 Q560 600 600 860 L560 860 Q520 560 560 280 Z" fill="#7a2f2a"/>',
          '<rect y="1300" width="1080" height="620" fill="url(#suelo)"/>',
          '<rect y="1290" width="1080" height="24" fill="#2a1a12"/>']
    for i in range(10):
        b.append(f'<path d="M0 {1360+i*60} H1080" stroke="#000" stroke-width="3" opacity="0.18"/>')
    b += ['<ellipse cx="540" cy="1540" rx="440" ry="110" fill="#8c3a2a" opacity="0.7"/>',  # alfombra
          '<ellipse cx="540" cy="1540" rx="400" ry="90" fill="none" stroke="#e8b45a" stroke-width="8" opacity="0.5"/>',
          '<circle cx="190" cy="760" r="520" fill="url(#lamp)"/>',
          '<path d="M190 780 L190 1420" stroke="#2a1a12" stroke-width="12"/><ellipse cx="190" cy="1425" rx="80" ry="18" fill="#2a1a12"/>',
          '<path d="M120 650 L260 650 L230 790 L150 790 Z" fill="#ffd28a"/><path d="M120 650 L260 650 L250 690 L130 690 Z" fill="#fff3d0" opacity="0.6"/>',
          # sillón
          '<path d="M250 1080 Q250 920 420 920 L700 920 Q860 920 860 1080 L860 1360 L250 1360 Z" fill="url(#sil)"/>',
          '<rect x="200" y="1140" width="140" height="260" rx="50" fill="#5e2220"/><rect x="770" y="1140" width="140" height="260" rx="50" fill="#5e2220"/>',
          '<rect x="300" y="1220" width="510" height="120" rx="30" fill="#8c3a32"/>',
          '<path d="M300 940 Q420 900 560 930" stroke="#ffb07a" stroke-width="10" opacity="0.25" fill="none"/>',
          '<ellipse cx="560" cy="1420" rx="380" ry="30" fill="#000" opacity="0.35" filter="url(#blur20)"/>']
    b.append(grano())
    guardar("bg_salon", "".join(b), defs=d)


def medico(nombre="medico", viejo=False):
    """Médico sentado/de pie con bata, gafas y libreta (lienzo 420x900)."""
    pelo = "#e9e6e0" if viejo else "#4a3020"
    d = lg("bata", (0, "#ffffff"), (1, "#c9d3de"), x2=1, y2=0) + lg("pant", (0, "#3a4250"), (1, "#20252e"))
    b = ['<ellipse cx="210" cy="880" rx="150" ry="18" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<path d="M140 520 L130 860 L190 860 L210 560 L230 860 L290 860 L280 520 Z" fill="url(#pant)"/>',
         '<rect x="118" y="846" width="78" height="26" rx="10" fill="#1a1410"/><rect x="224" y="846" width="78" height="26" rx="10" fill="#1a1410"/>',
         '<path d="M120 260 Q210 220 300 260 L320 640 L100 640 Z" fill="url(#bata)"/>',
         '<path d="M190 250 L210 330 L230 250 Z" fill="#7a9cc6"/><path d="M204 270 L216 270 L222 400 L198 400 Z" fill="#2c4a7a"/>',
         '<path d="M190 250 L170 420 L210 330 Z M230 250 L250 420 L210 330 Z" fill="#e6ecf2"/>',
         '<rect x="236" y="430" width="50" height="60" rx="6" fill="#dfe6ee" stroke="#b5c0cc" stroke-width="3"/>',
         '<path d="M240 300 Q270 280 262 360" stroke="#3a3a44" stroke-width="5" fill="none"/>',  # fonendo
         '<rect x="190" y="200" width="40" height="40" fill="#d99a72"/>',
         '<ellipse cx="210" cy="150" rx="62" ry="72" fill="url(#piel2)"/>',
         f'<path d="M150 130 Q160 70 210 70 Q262 70 272 130 Q262 100 210 102 Q160 100 150 130 Z" fill="{pelo}"/>',
         '<circle cx="186" cy="152" r="17" fill="none" stroke="#2a2a30" stroke-width="5"/><circle cx="234" cy="152" r="17" fill="none" stroke="#2a2a30" stroke-width="5"/>',
         '<path d="M203 152 H217" stroke="#2a2a30" stroke-width="4"/>',
         '<circle cx="186" cy="154" r="4" fill="#2a1a12"/><circle cx="234" cy="154" r="4" fill="#2a1a12"/>',
         '<path d="M192 192 Q210 202 228 192" stroke="#7a3a2a" stroke-width="5" fill="none"/>',
         '<path d="M120 270 L70 470 L110 480 L150 320 Z" fill="url(#bata)"/>',
         '<path d="M300 270 L340 450 L250 470 L240 440 L300 410 L280 320 Z" fill="url(#bata)"/>',
         '<circle cx="88" cy="490" r="24" fill="#d99a72"/><circle cx="246" cy="456" r="24" fill="#d99a72"/>']
    if viejo:
        b.append('<path d="M168 196 Q210 236 252 196 Q246 226 210 232 Q174 226 168 196 Z" fill="#e9e6e0"/>')  # barba
    d += lg("piel2", (0, "#f2c29b"), (1, "#c98763"), x2=1, y2=0)
    guardar(nombre, "".join(b), 420, 900, d)


def cuaderno():
    """Libreta del experimento: dos columnas IZQ / DER con marcas (lienzo 760x900)."""
    d = lg("hoja", (0, "#fbf6e8"), (1, "#e9dfc4"))
    b = ['<rect x="40" y="40" width="680" height="820" rx="18" fill="#000" opacity="0.4" filter="url(#blur20)"/>',
         '<rect x="30" y="20" width="680" height="820" rx="18" fill="url(#hoja)"/>']
    for i in range(14):
        b.append(f'<path d="M60 {170+i*48} H690" stroke="#9fb6d6" stroke-width="2" opacity="0.7"/>')
    b += ['<path d="M370 120 V820" stroke="#d65a4a" stroke-width="4"/>',
          '<text x="200" y="120" font-family="DejaVu Sans" font-weight="bold" font-size="44" fill="#2a3a5a" text-anchor="middle">IZQ.</text>',
          '<text x="540" y="120" font-family="DejaVu Sans" font-weight="bold" font-size="44" fill="#2a3a5a" text-anchor="middle">DER.</text>']
    for i in range(12):
        y = 200 + i * 48
        b.append(f'<path d="M150 {y-6} l18 14 l34 -30" stroke="#1f7a3a" stroke-width="7" fill="none" stroke-linecap="round"/>')
        b.append(f'<path d="M230 {y-14} l26 24 M256 {y-14} l-26 24" stroke="#1f7a3a" stroke-width="0" fill="none"/>')
        b.append(f'<path d="M510 {y} H570" stroke="#b03a2e" stroke-width="7" stroke-linecap="round"/>')
    for i in range(10):
        b.append(f'<circle cx="30" cy="{70+i*80}" r="14" fill="#555" opacity="0.6"/>')
    guardar("cuaderno", "".join(b), 760, 900, d)


def negatoscopio():
    """Pantalla de luz de consulta con dos radiografías (fondo completo)."""
    d = lg("par", (0, "#1d2a36"), (1, "#0d141c")) + rg("luz", (0, "#ffffff", 0.95), (1, "#cfe8ff", 0.85))
    b = ['<rect width="1080" height="1920" fill="url(#par)"/>',
         '<rect x="70" y="560" width="940" height="820" rx="26" fill="#3a4654"/>',
         '<rect x="100" y="590" width="880" height="760" rx="14" fill="url(#luz)"/>',
         '<rect x="100" y="590" width="880" height="760" rx="14" fill="#bfe0ff" opacity="0.15" filter="url(#blur20)"/>',
         '<rect x="70" y="1380" width="940" height="40" rx="10" fill="#2a333e"/>',
         '<rect y="1500" width="1080" height="420" fill="#141b22"/>', grano()]
    guardar("bg_negatoscopio", "".join(b), defs=d)


def check(nombre="check", color="#3ddc6e"):
    guardar(nombre, f'<circle cx="100" cy="100" r="90" fill="{color}" opacity="0.95"/>'
            '<path d="M55 104 L88 136 L150 66" stroke="#fff" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/>', 200, 200)


def trofeo():
    d = lg("oro", (0, "#fff2a8"), (0.45, "#f2c040"), (1, "#a8741a"), x2=1, y2=0)
    b = ['<ellipse cx="200" cy="580" rx="150" ry="20" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         '<rect x="90" y="500" width="220" height="70" rx="8" fill="#2a1a12"/><rect x="90" y="500" width="220" height="12" fill="#5a3a22"/>',
         '<path d="M150 500 L170 400 L230 400 L250 500 Z" fill="url(#oro)"/>',
         '<rect x="180" y="330" width="40" height="80" fill="url(#oro)"/>',
         '<path d="M90 80 L310 80 Q310 300 200 340 Q90 300 90 80 Z" fill="url(#oro)"/>',
         '<path d="M90 110 Q20 110 30 180 Q40 250 120 260" stroke="url(#oro)" stroke-width="22" fill="none"/>',
         '<path d="M310 110 Q380 110 370 180 Q360 250 280 260" stroke="url(#oro)" stroke-width="22" fill="none"/>',
         '<path d="M120 90 Q130 230 190 300" stroke="#fff" stroke-width="12" opacity="0.5" fill="none"/>',
         '<ellipse cx="200" cy="82" rx="110" ry="16" fill="#a8741a"/>']
    guardar("trofeo", "".join(b), 400, 620, d)


def bg_escenario():
    d = lg("cor", (0, "#5a0f1a"), (1, "#2a060c")) + rg("foco", (0, "#fff6d8", 0.75), (1, "#fff6d8", 0))
    b = ['<rect width="1080" height="1920" fill="#120408"/>']
    for i in range(12):
        x = i * 95
        b.append(f'<path d="M{x} 0 Q{x+48} 900 {x} 1920 L{x+95} 1920 Q{x+48+10} 900 {x+95} 0 Z" fill="url(#cor)"/>'
                 f'<path d="M{x+20} 0 Q{x+60} 900 {x+20} 1920" stroke="#000" stroke-width="10" opacity="0.3" fill="none"/>')
    b += ['<path d="M440 0 L640 0 L900 1500 L180 1500 Z" fill="url(#foco)" opacity="0.6"/>',
          '<rect y="1420" width="1080" height="500" fill="#2a1a12"/><rect y="1420" width="1080" height="16" fill="#6a4a2a"/>',
          '<ellipse cx="540" cy="1480" rx="380" ry="60" fill="#fff6d8" opacity="0.25" filter="url(#blur20)"/>', grano()]
    guardar("bg_escenario", "".join(b), defs=d)


def resonancia():
    """Máquina de resonancia magnética (lienzo completo) con mesa y anillo."""
    d = (lg("sala", (0, "#cfe2ee"), (1, "#8fb0c4")) + lg("anillo", (0, "#ffffff"), (1, "#b9c8d6"), x2=1, y2=0) +
         rg("tunel", (0, "#2a4a6a", 1), (0.7, "#162a40", 1), (1, "#0a1828", 1)))
    b = ['<rect width="1080" height="1920" fill="url(#sala)"/>',
         '<rect y="1300" width="1080" height="620" fill="#7d97a8"/>']
    for i in range(9):
        b.append(f'<path d="M{i*130} 1300 L{i*200-260} 1920" stroke="#fff" stroke-width="3" opacity="0.25"/>')
    b += ['<ellipse cx="540" cy="1380" rx="460" ry="50" fill="#000" opacity="0.3" filter="url(#blur20)"/>',
          '<rect x="110" y="520" width="860" height="860" rx="140" fill="url(#anillo)"/>',
          '<rect x="110" y="520" width="860" height="80" rx="40" fill="#fff" opacity="0.5"/>',
          '<circle cx="540" cy="930" r="270" fill="url(#tunel)"/>',
          '<circle cx="540" cy="930" r="270" fill="none" stroke="#9fb4c6" stroke-width="18"/>',
          '<rect x="220" y="1130" width="80" height="20" rx="6" fill="#4fd2ff"/>',
          '<path d="M60 1080 L1020 1080 L1000 1140 L80 1140 Z" fill="#e9f0f5"/>',
          '<rect x="80" y="1140" width="920" height="40" fill="#b9c8d6"/>',
          '<rect x="440" y="1180" width="200" height="200" fill="#9fb0bf"/>', grano()]
    guardar("bg_resonancia", "".join(b), defs=d)


def pantalla_rm():
    """Monitor con la imagen de la resonancia (articulación del dedo en gris). 700x520."""
    b = ['<rect x="10" y="10" width="680" height="460" rx="20" fill="#1a1f26"/>',
         '<rect x="34" y="34" width="632" height="412" rx="8" fill="#03070c"/>',
         '<ellipse cx="350" cy="240" rx="120" ry="190" fill="#3a3a3a"/>',
         '<rect x="300" y="60" width="100" height="150" rx="40" fill="#cfcfcf"/>',
         '<rect x="300" y="250" width="100" height="170" rx="40" fill="#cfcfcf"/>',
         '<rect x="296" y="200" width="108" height="60" rx="10" fill="#5a5a5a"/>',
         '<text x="60" y="80" font-family="DejaVu Sans Mono" font-size="26" fill="#4fd2ff">MRI · 2015</text>',
         '<rect x="320" y="480" width="60" height="30" fill="#2a2f36"/><rect x="260" y="505" width="180" height="14" rx="6" fill="#2a2f36"/>']
    guardar("pantalla_rm", "".join(b), 700, 520)


def articulacion():
    """Sección de la articulación: fondo con cápsula y líquido; huesos por separado (para moverlos)."""
    d = (rg("fon", (0, "#3a1a22", 1), (1, "#12060a", 1)) + lg("liq", (0, "#6fd0ff"), (1, "#2a7ab8")) +
         lg("hue2", (0, "#fbf3e2"), (0.6, "#e7d6b4"), (1, "#bfa77e"), x2=1, y2=0) + lg("car", (0, "#cfe9ff"), (1, "#9cc8ea")))
    b = ['<rect width="1080" height="1920" fill="url(#fon)"/>']
    for i in range(40):  # tejido alrededor
        x, y = R.uniform(0, 1080), R.uniform(0, 1920)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{R.uniform(40,120):.0f}" ry="{R.uniform(20,60):.0f}" fill="#7a2a36" opacity="0.18"/>')
    b += ['<path d="M300 560 Q240 960 300 1360 L780 1360 Q840 960 780 560 Z" fill="#c76a7a" opacity="0.55"/>',  # cápsula
          '<path d="M330 600 Q280 960 330 1320 L750 1320 Q800 960 750 600 Z" fill="url(#liq)" opacity="0.85"/>',
          '<path d="M330 600 Q280 960 330 1320" stroke="#fff" stroke-width="8" opacity="0.25" fill="none"/>', grano()]
    guardar("bg_articulacion", "".join(b), defs=d)
    # hueso de arriba (metacarpiano) y de abajo (falange), lienzo 520x720
    sup = ('<path d="M150 0 L370 0 L370 380 Q420 480 380 600 Q260 690 140 600 Q100 480 150 380 Z" fill="url(#hue2)"/>'
           '<path d="M120 560 Q260 690 400 560 Q400 640 260 700 Q120 640 120 560 Z" fill="url(#car)"/>'
           '<path d="M170 0 L200 0 L200 380 Q160 480 170 580 Q140 480 170 380 Z" fill="#fff" opacity="0.4"/>')
    inf = ('<path d="M140 720 L380 720 L380 300 Q420 180 380 120 Q260 60 140 120 Q100 180 140 300 Z" fill="url(#hue2)"/>'
           '<path d="M120 150 Q260 40 400 150 Q400 110 260 70 Q120 110 120 150 Z" fill="url(#car)"/>'
           '<path d="M330 720 L380 720 L380 300 Q400 200 370 150 Q380 260 330 320 Z" fill="#000" opacity="0.12"/>')
    guardar("hueso_sup", sup, 520, 720, d)
    guardar("hueso_inf", inf, 520, 720, d)


def burbuja():
    d = rg("bur", (0, "#ffffff", 0.15), (0.75, "#dff6ff", 0.35), (1, "#ffffff", 0.95))
    guardar("burbuja", '<circle cx="150" cy="150" r="140" fill="url(#bur)"/>'
            '<ellipse cx="105" cy="95" rx="40" ry="24" fill="#fff" opacity="0.85" transform="rotate(-30 105 95)"/>'
            '<circle cx="150" cy="150" r="140" fill="none" stroke="#ffffff" stroke-width="5" opacity="0.8"/>', 300, 300, d)


def persona_sola():
    d = rg("halo", (0, "#ffe9b0", 0.6), (1, "#ffe9b0", 0))
    b = ['<circle cx="200" cy="300" r="200" fill="url(#halo)"/>',
         '<circle cx="200" cy="170" r="62" fill="#1c1a24"/>',
         '<path d="M110 260 Q200 230 290 260 L310 560 L90 560 Z" fill="#1c1a24"/>',
         '<rect x="120" y="550" width="60" height="200" fill="#1c1a24"/><rect x="220" y="550" width="60" height="200" fill="#1c1a24"/>']
    guardar("persona_sola", "".join(b), 400, 760, d)


def onda(nombre="ondas", color="#ffd23f"):
    b = "".join(f'<path d="M{60+i*50} {200-i*60} Q{150+i*70} 200 {60+i*50} {200+i*60}" stroke="{color}" stroke-width="14" fill="none" '
                f'stroke-linecap="round" opacity="{1-i*0.25}"/>' for i in range(3))
    guardar(nombre, b, 300, 400)


def todo():
    mano("mano_izq"); mano("mano_der", espejo=True); mano("mano_izq_roja", roja=True)
    radiografia("rx_izq"); radiografia("rx_der", espejo=True); radiografia("rx_artritis", artritis=True)
    bg_salon(); medico("medico"); medico("medico_viejo", viejo=True); cuaderno(); negatoscopio(); check()
    trofeo(); bg_escenario(); resonancia(); pantalla_rm(); articulacion(); burbuja(); persona_sola(); onda()


if __name__ == "__main__":
    todo()
    print("ok")
