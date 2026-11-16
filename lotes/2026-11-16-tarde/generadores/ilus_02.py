"""Ilustraciones SVG del vídeo 02 (las puertas te hacen olvidar) — estilo v4."""
from base import guardar, lg, rg, grano, R


def bg_pasillo(nombre="bg_pasillo", abierta=True):
    """Pasillo de casa en penumbra con una puerta al fondo que da a una habitación iluminada."""
    d = (lg("par", (0, "#2c3550"), (1, "#1a2036")) + lg("sue", (0, "#5a4030"), (1, "#20140c")) +
         lg("hab", (0, "#ffe2a8"), (1, "#f2a85a")) + rg("luzp", (0, "#ffd890", 0.75), (1, "#ffd890", 0)) +
         lg("hoja_p", (0, "#c08a5a"), (1, "#7a4e2c"), x2=1, y2=0))
    b = ['<rect width="1080" height="1920" fill="url(#par)"/>',
         # paredes laterales en perspectiva
         '<path d="M0 0 L250 380 L250 1380 L0 1920 Z" fill="#232b44"/>',
         '<path d="M1080 0 L830 380 L830 1380 L1080 1920 Z" fill="#1c2238"/>',
         '<path d="M0 1920 L250 1380 L830 1380 L1080 1920 Z" fill="url(#sue)"/>']
    for i in range(7):
        x = 250 + i * 97
        b.append(f'<path d="M{x} 1380 L{(x-540)*3.2+540:.0f} 1920" stroke="#000" stroke-width="3" opacity="0.25"/>')
    b += ['<rect x="250" y="380" width="580" height="1000" fill="#2a3352"/>',
          '<rect x="390" y="620" width="300" height="760" fill="url(#hab)"/>' if abierta else
          '<rect x="390" y="620" width="300" height="760" fill="url(#hoja_p)"/>',
          '<rect x="372" y="602" width="336" height="18" fill="#e8dcc8"/><rect x="372" y="602" width="18" height="778" fill="#e8dcc8"/>'
          '<rect x="690" y="602" width="18" height="778" fill="#d8ccb8"/>']
    if abierta:
        b += ['<path d="M390 620 L300 560 L300 1440 L390 1380 Z" fill="url(#hoja_p)"/>',  # hoja de la puerta abierta hacia dentro
              '<circle cx="320" cy="1010" r="10" fill="#e8c46a"/>',
              '<rect x="430" y="980" width="220" height="170" fill="#c9824a" opacity="0.5"/>',  # mueble del fondo
              '<rect x="560" y="760" width="90" height="120" fill="#7a4e2c" opacity="0.55"/>',
              '<path d="M390 1380 L690 1380 L900 1920 L180 1920 Z" fill="url(#luzp)" opacity="0.8"/>',
              '<circle cx="540" cy="900" r="420" fill="url(#luzp)" opacity="0.6"/>']
    else:
        b += ['<circle cx="660" cy="1010" r="12" fill="#e8c46a"/>',
              '<rect x="420" y="660" width="240" height="300" rx="8" fill="none" stroke="#5a3a20" stroke-width="8" opacity="0.6"/>',
              '<rect x="420" y="1010" width="240" height="330" rx="8" fill="none" stroke="#5a3a20" stroke-width="8" opacity="0.6"/>']
    b += ['<rect x="80" y="560" width="120" height="160" fill="#c9a46a" opacity="0.8"/><rect x="92" y="572" width="96" height="136" fill="#4a6a8a"/>',  # cuadro
          '<rect x="880" y="600" width="110" height="140" fill="#c9a46a" opacity="0.8"/><rect x="892" y="612" width="86" height="116" fill="#8a4a3a"/>',
          '<rect x="0" y="1880" width="1080" height="40" fill="#000" opacity="0.3"/>', grano()]
    guardar(nombre, "".join(b), defs=d)


def persona(nombre="persona_casa", lado=1):
    """Persona en casa (sudadera), ilustrada con volumen, de pie y algo de lado. Lienzo 420x980."""
    d = (lg("sud", (0, "#3fa0a8"), (1, "#1f5e66"), x2=1, y2=0) + lg("vaq", (0, "#3a5a8a"), (1, "#1f3050"), x2=1, y2=0) +
         lg("pp", (0, "#e9b48e"), (1, "#b9805c"), x2=1, y2=0))
    b = ['<ellipse cx="210" cy="960" rx="140" ry="18" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<path d="M140 560 L120 930 L190 930 L210 620 L230 930 L300 930 L280 560 Z" fill="url(#vaq)"/>',
         '<rect x="104" y="916" width="94" height="34" rx="14" fill="#f2f2f2"/><rect x="222" y="916" width="94" height="34" rx="14" fill="#f2f2f2"/>',
         '<path d="M120 300 Q210 250 300 300 L320 590 L100 590 Z" fill="url(#sud)"/>',
         '<path d="M170 290 Q210 330 250 290" stroke="#174a50" stroke-width="10" fill="none"/>',
         '<rect x="150" y="470" width="120" height="70" rx="20" fill="#000" opacity="0.15"/>',
         '<path d="M120 310 L80 560 L120 570 L150 360 Z" fill="url(#sud)"/><path d="M300 310 L340 560 L300 570 L270 360 Z" fill="url(#sud)"/>',
         '<circle cx="100" cy="580" r="26" fill="url(#pp)"/><circle cx="320" cy="580" r="26" fill="url(#pp)"/>',
         '<rect x="188" y="240" width="44" height="50" fill="#c98f68"/>',
         '<ellipse cx="210" cy="180" rx="68" ry="78" fill="url(#pp)"/>',
         '<path d="M140 170 Q140 90 210 92 Q284 92 282 170 Q272 128 210 126 Q160 128 140 170 Z" fill="#2a1a12"/>',
         '<ellipse cx="185" cy="185" rx="8" ry="11" fill="#1a1010"/><ellipse cx="237" cy="185" rx="8" ry="11" fill="#1a1010"/>',
         '<circle cx="188" cy="181" r="3" fill="#fff"/><circle cx="240" cy="181" r="3" fill="#fff"/>',
         '<path d="M168 158 Q185 148 200 160 M222 160 Q237 148 254 158" stroke="#2a1a12" stroke-width="6" fill="none"/>',  # cejas levantadas
         '<ellipse cx="211" cy="225" rx="14" ry="10" fill="#7a3a2a"/>']  # boca de «¿eh?»
    cuerpo = "".join(b)
    if lado < 0:
        cuerpo = f'<g transform="translate(420 0) scale(-1 1)">{cuerpo}</g>'
    guardar(nombre, cuerpo, 420, 980, d)


def bocadillo(nombre, contenido, w=360, h=300):
    b = (f'<ellipse cx="{w/2}" cy="{h*0.42}" rx="{w*0.47}" ry="{h*0.38}" fill="#ffffff"/>'
         f'<circle cx="{w*0.28}" cy="{h*0.86}" r="{w*0.05}" fill="#ffffff"/><circle cx="{w*0.18}" cy="{h*0.96}" r="{w*0.03}" fill="#ffffff"/>'
         f'<ellipse cx="{w/2}" cy="{h*0.42}" rx="{w*0.47}" ry="{h*0.38}" fill="none" stroke="#c8d4e0" stroke-width="5"/>{contenido}')
    guardar(nombre, b, w, h)


def llaves_svg():
    return ('<g transform="translate(110 50)"><circle cx="40" cy="50" r="34" fill="none" stroke="#e8b830" stroke-width="16"/>'
            '<rect x="66" y="42" width="90" height="16" fill="#e8b830"/><rect x="128" y="54" width="12" height="22" fill="#e8b830"/>'
            '<rect x="146" y="54" width="10" height="16" fill="#e8b830"/><circle cx="40" cy="50" r="12" fill="#fff"/>'
            '<circle cx="66" cy="110" r="22" fill="none" stroke="#9aa6b2" stroke-width="10"/></g>')


def bocadillos():
    bocadillo("bocadillo_llaves", llaves_svg())
    bocadillo("bocadillo_duda", '<text x="180" y="170" font-family="DejaVu Sans" font-weight="bold" font-size="150" fill="#2a3a5a" text-anchor="middle">?</text>')


def planta(nombre, con_puerta):
    """Plano visto desde arriba: dos mesas, con un tabique y una puerta (o sin tabique). Lienzo 900x1100."""
    d = lg("sue2", (0, "#f2e6cc"), (1, "#dccaa6"))
    b = ['<rect x="20" y="20" width="860" height="1060" rx="12" fill="#000" opacity="0.35" filter="url(#blur20)"/>',
         '<rect x="40" y="40" width="820" height="1020" fill="url(#sue2)"/>']
    for i in range(16):
        b.append(f'<path d="M40 {40+i*64} H860" stroke="#c9b48a" stroke-width="2" opacity="0.6"/>')
    b.append('<rect x="40" y="40" width="820" height="1020" fill="none" stroke="#3a3a44" stroke-width="22"/>')
    if con_puerta:
        b += ['<path d="M40 550 H350 M550 550 H860" stroke="#3a3a44" stroke-width="22"/>',
              '<path d="M350 550 A200 200 0 0 1 550 550" stroke="#3a3a44" stroke-width="5" fill="none" stroke-dasharray="12 10"/>',
              '<rect x="350" y="540" width="16" height="16" fill="#3a3a44"/>']
    for y in (210, 890):
        b.append(f'<rect x="330" y="{y-70}" width="240" height="140" rx="12" fill="#a0683a"/>'
                 f'<rect x="340" y="{y-62}" width="220" height="124" rx="8" fill="#c08a5a"/>')
    guardar(nombre, "".join(b), 900, 1100, d)


def bg_universidad():
    d = lg("cie", (0, "#2a4a8a"), (0.6, "#e8a070"), (1, "#ffd8a0")) + lg("pie2", (0, "#d8c8a8"), (1, "#a8946e"), x2=1, y2=0)
    b = ['<rect width="1080" height="1920" fill="url(#cie)"/>',
         '<path d="M0 1350 C300 1320 700 1360 1080 1330 L1080 1920 L0 1920 Z" fill="#3f6a3a"/>',
         '<rect x="140" y="900" width="800" height="460" fill="url(#pie2)"/>',
         '<path d="M120 900 L540 700 L960 900 Z" fill="#8a5a3a"/>',
         '<rect x="470" y="420" width="140" height="480" fill="url(#pie2)"/>',
         '<path d="M455 420 L540 250 L625 420 Z" fill="#c9a040"/><circle cx="540" cy="520" r="44" fill="#fff6d8" stroke="#8a6a3a" stroke-width="6"/>']
    for i in range(6):
        for j in range(2):
            b.append(f'<path d="M{190+i*125} {1060+j*170} v-60 a30 30 0 0 1 60 0 v60 Z" fill="#ffd27a" opacity="0.85"/>')
    for x in (60, 1010):
        b.append(f'<path d="M{x} 1340 v-200" stroke="#2a1a12" stroke-width="16"/><circle cx="{x}" cy="1110" r="110" fill="#2f5a2a"/>')
    b.append(grano())
    guardar("bg_universidad", "".join(b), defs=d)


def cerebro():
    d = rg("cer", (0, "#ffb8c8", 1), (0.7, "#e8829a", 1), (1, "#b85a72", 1))
    b = ['<ellipse cx="300" cy="230" rx="270" ry="200" fill="url(#cer)"/>']
    for i in range(14):
        x, y = R.uniform(90, 510), R.uniform(80, 380)
        b.append(f'<path d="M{x:.0f} {y:.0f} q30 -30 60 0 q30 30 60 0" stroke="#a84a64" stroke-width="7" fill="none" opacity="0.7"/>')
    b += ['<path d="M300 40 Q290 230 310 420" stroke="#a84a64" stroke-width="8" fill="none"/>',
          '<path d="M240 400 Q280 470 300 520 L340 520 Q330 460 360 410 Z" fill="#c86a84"/>',
          '<ellipse cx="200" cy="140" rx="90" ry="40" fill="#fff" opacity="0.25"/>']
    guardar("cerebro", "".join(b), 600, 540, d)


def pelicula():
    """Tira de película larga (2400x360) con fotogramas de la casa: cocina, pasillo, salón, dormitorio."""
    cols = ["#f2a85a", "#2a3352", "#c9824a", "#4a6a8a", "#e8c46a", "#8a4a3a", "#3fa0a8", "#f2a85a"]
    b = ['<rect width="2400" height="360" fill="#141414"/>']
    for i in range(48):
        b.append(f'<rect x="{12+i*50}" y="16" width="26" height="30" rx="5" fill="#e8e8e8"/><rect x="{12+i*50}" y="314" width="26" height="30" rx="5" fill="#e8e8e8"/>')
    for i, c in enumerate(cols):
        x = 30 + i * 296
        b.append(f'<rect x="{x}" y="64" width="270" height="232" fill="{c}"/>')
        b.append(f'<rect x="{x+90}" y="110" width="90" height="186" fill="#000" opacity="0.25"/>')  # puerta de cada fotograma
        b.append(f'<circle cx="{x+60}" cy="{120}" r="22" fill="#fff" opacity="0.5"/>')
    guardar("pelicula", "".join(b), 2400, 360)


def archivador():
    """Archivador metálico con un cajón abierto (lienzo 600x900)."""
    d = lg("met", (0, "#9aa6b2"), (0.5, "#6b7684"), (1, "#3f4854"), x2=1, y2=0)
    b = ['<ellipse cx="300" cy="880" rx="250" ry="20" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         '<rect x="80" y="120" width="440" height="760" rx="14" fill="url(#met)"/>']
    for k, y in enumerate((150, 400, 640)):
        b.append(f'<rect x="100" y="{y}" width="400" height="220" rx="10" fill="#5a6470" stroke="#3a424c" stroke-width="5"/>'
                 f'<rect x="250" y="{y+30}" width="100" height="26" rx="10" fill="#c9d1d9"/>'
                 f'<rect x="270" y="{y+70}" width="60" height="40" fill="#f2f2e8"/>')
    # cajón superior abierto con carpetas
    b += ['<path d="M100 150 L60 60 L540 60 L500 150 Z" fill="#7a8694"/>',
          '<path d="M60 60 L540 60 L540 20 L60 20 Z" fill="#4a535e"/>']
    for i, c in enumerate(("#e8c46a", "#f2a85a", "#3fa0a8", "#e8829a")):
        b.append(f'<rect x="{110+i*100}" y="-20" width="90" height="100" rx="6" fill="{c}" transform="rotate({(i-1.5)*4} {150+i*100} 40)"/>')
    guardar("archivador", "".join(b), 600, 900, d)


def carpeta(nombre="carpeta", texto="COCINA"):
    b = ('<path d="M10 40 L120 40 L150 10 L290 10 L290 220 L10 220 Z" fill="#f2a85a"/>'
         '<rect x="10" y="50" width="280" height="170" fill="#e8964a"/>'
         f'<text x="150" y="150" font-family="DejaVu Sans" font-weight="bold" font-size="40" fill="#5a2a10" text-anchor="middle">{texto}</text>')
    guardar(nombre, b, 300, 230)


def puerta_cerca(nombre="puerta_cerca"):
    """Puerta de madera de cerca, con marco (lienzo completo); la hoja va aparte."""
    d = lg("par3", (0, "#e8dcc8"), (1, "#b8a888")) + lg("hab3", (0, "#ffe2a8"), (1, "#f2a85a"))
    b = ['<rect width="1080" height="1920" fill="url(#par3)"/>',
         '<rect x="190" y="260" width="700" height="1560" fill="url(#hab3)"/>',
         '<circle cx="540" cy="700" r="400" fill="#fff6d8" opacity="0.35" filter="url(#blur40)"/>',
         '<rect x="150" y="220" width="780" height="40" fill="#f6f0e4"/><rect x="150" y="220" width="40" height="1700" fill="#f6f0e4"/>'
         '<rect x="890" y="220" width="40" height="1700" fill="#d8ccb8"/>',
         '<rect y="1820" width="1080" height="100" fill="#5a4030"/>', grano()]
    guardar(nombre, "".join(b), defs=d)
    d2 = lg("hj", (0, "#c08a5a"), (0.5, "#a06a3e"), (1, "#7a4e2c"), x2=1, y2=0)
    h = ['<rect x="0" y="0" width="700" height="1560" fill="url(#hj)"/>',
         '<rect x="70" y="80" width="560" height="600" rx="10" fill="none" stroke="#5a3a20" stroke-width="14" opacity="0.6"/>',
         '<rect x="70" y="820" width="560" height="640" rx="10" fill="none" stroke="#5a3a20" stroke-width="14" opacity="0.6"/>',
         '<circle cx="620" cy="760" r="26" fill="#e8c46a"/><rect x="560" y="750" width="70" height="18" rx="8" fill="#e8c46a"/>']
    guardar("hoja_puerta", "".join(h), 700, 1560, d2)


def todo():
    bg_pasillo("bg_pasillo", True); bg_pasillo("bg_pasillo_cerrada", False)
    persona("persona_casa", 1); persona("persona_casa_izq", -1); bocadillos()
    planta("planta_puerta", True); planta("planta_sin", False); bg_universidad(); cerebro(); pelicula(); archivador()
    carpeta("carpeta", "COCINA"); puerta_cerca()


if __name__ == "__main__":
    todo()
    print("ok")
