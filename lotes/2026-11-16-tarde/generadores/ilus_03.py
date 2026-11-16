"""Ilustraciones SVG del vídeo 03 (el móvil y el ordenador del Apolo 11) — estilo v4.
Reutiliza del lote 2026-11-15-tarde: bg_espacio, luna_hd, tierra_hd, bg_superficie."""
from base import guardar, lg, rg, grano, R, copiar_v4


def movil(nombre="movil", pantalla="galeria"):
    """Móvil genérico (sin marca), 420x860, con la pantalla encendida."""
    d = (lg("cuerpo", (0, "#3a3f4a"), (1, "#16181e"), x2=1, y2=0) + lg("pant", (0, "#1b2a5a"), (1, "#0a0f22")) +
         rg("brillo_p", (0, "#ffffff", 0.18), (1, "#ffffff", 0)))
    b = ['<rect x="20" y="20" width="380" height="820" rx="58" fill="#000" opacity="0.45" filter="url(#blur20)"/>',
         '<rect x="10" y="10" width="400" height="830" rx="60" fill="url(#cuerpo)"/>',
         '<rect x="30" y="30" width="360" height="790" rx="44" fill="url(#pant)"/>',
         '<rect x="170" y="48" width="80" height="22" rx="11" fill="#05070c"/>']
    if pantalla == "galeria":
        cols = ["#f2a85a", "#3fa0a8", "#e8829a", "#e8c46a", "#4a6a8a", "#8a4a3a", "#3ddc6e", "#c9824a", "#9aa6ff"]
        for i in range(15):
            x, y = 44 + (i % 3) * 112, 110 + (i // 3) * 132
            b.append(f'<rect x="{x}" y="{y}" width="104" height="124" rx="10" fill="{cols[i % len(cols)]}"/>'
                     f'<circle cx="{x+30}" cy="{y+36}" r="14" fill="#fff" opacity="0.6"/>'
                     f'<path d="M{x} {y+124} L{x+44} {y+70} L{x+70} {y+100} L{x+86} {y+84} L{x+104} {y+110} L{x+104} {y+124} Z" fill="#000" opacity="0.25"/>')
    elif pantalla == "video":
        b += ['<rect x="30" y="30" width="360" height="790" rx="44" fill="#03050c"/>',
              '<circle cx="210" cy="380" r="120" fill="#cfcfcf"/><circle cx="170" cy="340" r="22" fill="#9a9a9a"/><circle cx="250" cy="420" r="30" fill="#a8a8a8"/>',
              '<rect x="60" y="120" width="300" height="40" rx="10" fill="#ffffff" opacity="0.85"/>',
              '<rect x="60" y="760" width="300" height="8" rx="4" fill="#ffffff" opacity="0.3"/><rect x="60" y="760" width="190" height="8" rx="4" fill="#e8402f"/>',
              '<circle cx="350" cy="560" r="22" fill="#fff" opacity="0.8"/><circle cx="350" cy="630" r="22" fill="#fff" opacity="0.8"/>']
    b.append('<path d="M40 40 L260 40 L60 700 L40 700 Z" fill="url(#brillo_p)"/>')
    guardar(nombre, "".join(b), 420, 860, d)


def agc():
    """Ordenador de guiado del Apolo (caja metálica con conectores) + teclado DSKY. Lienzo 760x620."""
    d = (lg("caja", (0, "#c9ccd2"), (0.5, "#8d929b"), (1, "#5a5f68"), x2=1, y2=0) + lg("tapa", (0, "#e2e5ea"), (1, "#a9aeb6")) +
         lg("dsky", (0, "#6b6f78"), (1, "#3a3d44")))
    b = ['<ellipse cx="380" cy="600" rx="340" ry="22" fill="#000" opacity="0.45" filter="url(#blur8)"/>',
         # caja principal en perspectiva
         '<path d="M60 220 L520 220 L560 180 L100 180 Z" fill="url(#tapa)"/>',
         '<rect x="60" y="220" width="460" height="360" fill="url(#caja)"/>',
         '<path d="M520 220 L560 180 L560 540 L520 580 Z" fill="#4a4f58"/>']
    for i in range(9):
        b.append(f'<rect x="{84+i*48}" y="250" width="34" height="300" rx="4" fill="#7a8089" stroke="#4a4f58" stroke-width="3"/>')
        for j in range(6):
            b.append(f'<circle cx="{101+i*48}" cy="{275+j*48}" r="5" fill="#3a3d44"/>')
    b += ['<rect x="60" y="220" width="460" height="14" fill="#fff" opacity="0.3"/>',
          # DSKY delante
          '<rect x="430" y="300" width="300" height="290" rx="10" fill="url(#dsky)" stroke="#2a2c32" stroke-width="5"/>',
          '<rect x="450" y="318" width="260" height="100" rx="6" fill="#0b1a10"/>']
    for k, y in enumerate((338, 372)):
        for i in range(5):
            b.append(f'<rect x="{468+i*46}" y="{y}" width="36" height="26" rx="3" fill="#3dff6e" opacity="{0.9 if (i+k) % 2 else 0.6}"/>')
    for r in range(3):
        for c in range(6):
            b.append(f'<rect x="{450+c*44}" y="{438+r*48}" width="36" height="38" rx="6" fill="#d8d9dc" stroke="#9a9ca2" stroke-width="2"/>')
    guardar("agc", "".join(b), 760, 620, d)


def maletin():
    d = lg("cuero", (0, "#8a5a32"), (1, "#5a3818"))
    b = ['<ellipse cx="300" cy="440" rx="260" ry="18" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         '<path d="M220 110 Q220 50 300 50 Q380 50 380 110" stroke="#3a2410" stroke-width="22" fill="none"/>',
         '<rect x="40" y="110" width="520" height="320" rx="26" fill="url(#cuero)"/>',
         '<rect x="40" y="200" width="520" height="16" fill="#3a2410" opacity="0.5"/>',
         '<rect x="270" y="190" width="60" height="40" rx="6" fill="#e8c46a"/>',
         '<rect x="40" y="110" width="520" height="40" rx="20" fill="#fff" opacity="0.12"/>']
    guardar("maletin", "".join(b), 600, 470, d)


def modulo_lunar():
    """Módulo lunar genérico (lámina dorada, patas), 600x620."""
    d = lg("oro2", (0, "#ffe9a0"), (0.5, "#d8a838"), (1, "#8a6418"), x2=1, y2=0) + lg("gris", (0, "#e2e5ea"), (1, "#8d929b"), x2=1, y2=0)
    b = ['<path d="M190 120 L410 120 L450 230 L150 230 Z" fill="url(#gris)"/>',
         '<path d="M240 130 L290 130 L285 180 L240 180 Z" fill="#1a2030"/>',
         '<path d="M150 230 L450 230 L470 380 L130 380 Z" fill="url(#oro2)"/>']
    for i in range(10):
        b.append(f'<path d="M{150+i*32} 236 L{140+i*34} 376" stroke="#8a6418" stroke-width="3" opacity="0.6"/>')
    b += ['<path d="M150 360 L40 560 M450 360 L560 560 M220 380 L170 590 M380 380 L430 590" stroke="#c9ccd2" stroke-width="12"/>',
          '<ellipse cx="40" cy="570" rx="42" ry="12" fill="#c9ccd2"/><ellipse cx="560" cy="570" rx="42" ry="12" fill="#c9ccd2"/>',
          '<ellipse cx="170" cy="598" rx="36" ry="10" fill="#c9ccd2"/><ellipse cx="430" cy="598" rx="36" ry="10" fill="#c9ccd2"/>',
          '<path d="M270 380 L330 380 L350 450 L250 450 Z" fill="#5a5f68"/>',
          '<rect x="296" y="70" width="8" height="50" fill="#c9ccd2"/><circle cx="300" cy="64" r="14" fill="#e2e5ea"/>']
    guardar("modulo_lunar", "".join(b), 600, 620, d)


def nucleos():
    """Memoria de cuerda: rejilla de anillos de ferrita con hilos de cobre (lienzo completo)."""
    d = lg("pl", (0, "#1f3a2a"), (1, "#0c1a12")) + lg("cob", (0, "#ffcf8a"), (1, "#c87a32"))
    b = ['<rect width="1080" height="1920" fill="url(#pl)"/>']
    for r in range(9):
        for c in range(6):
            x, y = 140 + c * 160, 380 + r * 150
            b.append(f'<circle cx="{x}" cy="{y}" r="42" fill="none" stroke="#2a2a2e" stroke-width="22"/>'
                     f'<circle cx="{x}" cy="{y}" r="42" fill="none" stroke="#5a5a62" stroke-width="6" opacity="0.6"/>')
    for k in range(18):  # hilos que cruzan por dentro o por fuera
        y = 360 + k * 75
        b.append(f'<path d="M0 {y} C300 {y + R.uniform(-60, 60):.0f} 700 {y + R.uniform(-60, 60):.0f} 1080 {y}" stroke="url(#cob)" stroke-width="5" fill="none" opacity="0.85"/>')
    b.append(grano())
    guardar("bg_nucleos", "".join(b), defs=d)


def anillo(nombre="anillo"):
    """Un núcleo de ferrita grande (lienzo 600x600) visto en perspectiva."""
    d = lg("fer", (0, "#5a5a62"), (1, "#1a1a1e"))
    b = ['<ellipse cx="300" cy="330" rx="230" ry="140" fill="#000" opacity="0.4" filter="url(#blur20)"/>',
         '<ellipse cx="300" cy="300" rx="240" ry="150" fill="url(#fer)"/>',
         '<ellipse cx="300" cy="300" rx="120" ry="70" fill="#0c1a12"/>',
         '<ellipse cx="300" cy="280" rx="200" ry="110" fill="none" stroke="#9a9aa2" stroke-width="6" opacity="0.4"/>']
    guardar(nombre, "".join(b), 600, 600, d)


def manos_tejer():
    """Dos manos con una aguja e hilo de cobre (lienzo 900x700)."""
    d = lg("pt", (0, "#f2c29b"), (1, "#b9805c"), x2=1, y2=0) + lg("cob2", (0, "#ffcf8a"), (1, "#c87a32"))
    b = ['<path d="M0 520 Q140 420 260 430 Q330 440 360 400 Q390 360 350 340 Q300 330 240 360 Q160 330 0 380 Z" fill="url(#pt)"/>',
         '<path d="M240 360 Q300 300 360 300 Q392 302 380 330 Q350 350 300 370 Z" fill="url(#pt)"/>',
         '<path d="M900 540 Q760 440 640 450 Q570 460 540 420 Q510 380 550 360 Q600 350 660 380 Q740 350 900 400 Z" fill="url(#pt)"/>',
         '<path d="M370 330 L620 380" stroke="#d8d9dc" stroke-width="8" stroke-linecap="round"/>',
         '<path d="M620 380 C700 400 760 300 900 320" stroke="url(#cob2)" stroke-width="6" fill="none"/>',
         '<rect x="0" y="560" width="900" height="140" fill="#3a2410" opacity="0.0"/>']
    guardar("manos_tejer", "".join(b), 900, 700, d)


def todo():
    copiar_v4("bg_espacio", "luna_hd", "tierra_hd", "bg_superficie")
    movil("movil", "galeria"); movil("movil_video", "video"); agc(); maletin(); modulo_lunar(); nucleos(); anillo(); manos_tejer()


if __name__ == "__main__":
    todo()
    print("ok")
