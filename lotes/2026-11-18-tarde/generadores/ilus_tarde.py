"""Ilustraciones del lote 2026-11-18-tarde (GTA 6 · estrella de neutrones · mides menos por la noche).
Uso: python3 ilus_tarde.py DIR_SVG (semillas fijas). Ladrillos de motor/biblioteca/ilus.py. Agente 20:00 (Jorge).
Nada de logos, carátulas, personajes ni capturas de juegos: todo genérico y dibujado aquí."""
import math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano, palmera, _estrellas_ricas  # noqa: E402,F401


# ====================================================================== 01 · GTA 6
def bg_ciudad_tropical(nombre="bg_ciudad", noche=False, sem=4):
    """Ciudad costera genérica al atardecer (o de noche con neones), palmeras y mar."""
    r = random.Random(sem)
    if noche:
        cielo = lg(f"{nombre}_c", (0, "#0a0620"), (0.45, "#2a0f4a"), (0.7, "#b02a7a"), (0.8, "#ff7a5a"), (1, "#1a0a2a"))
    else:
        cielo = lg(f"{nombre}_c", (0, "#2a1a5a"), (0.35, "#c0407a"), (0.6, "#ff8a4a"), (0.72, "#ffd27a"), (1, "#3a1a3a"))
    d = cielo + rg(f"{nombre}_s", (0, "#fff4c0", 1), (0.35, "#ffb46a", 0.7), (1, "#ff6a6a", 0)) + lg(f"{nombre}_m", (0, "#ff9a7a"), (0.2, "#6a2a6a"), (1, "#120a24"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>']
    if noche:
        b.append(_estrellas_ricas(sem, 140, 14, 3, banda=None).replace("<g", '<g opacity="0.6"', 1))
    b.append(f'<ellipse cx="540" cy="1130" rx="520" ry="420" fill="url(#{nombre}_s)"/>')
    if not noche:
        b.append('<circle cx="540" cy="1120" r="150" fill="#ffe6a0" opacity="0.95"/>')
        for k in range(5):
            b.append(f'<rect x="380" y="{1060+k*26}" width="320" height="{6+k}" fill="#ff9a6a" opacity="0.55"/>')
    # rascacielos en dos capas
    for capa, (col, luz, y0, hmin, hmax) in enumerate([("#4a2350", "#ffd27a", 1250, 160, 420), ("#24102e", "#ffe9a0", 1290, 220, 640)]):
        x = -20
        while x < 1100:
            w = r.uniform(60, 130); h = r.uniform(hmin, hmax)
            b.append(f'<rect x="{x:.0f}" y="{y0-h:.0f}" width="{w:.0f}" height="{h+20:.0f}" fill="{col}"/>')
            if r.random() < 0.3:
                b.append(f'<path d="M{x+w/2:.0f} {y0-h-60:.0f} L{x+w/2+4:.0f} {y0-h:.0f} L{x+w/2-4:.0f} {y0-h:.0f} Z" fill="{col}"/>')
            for fy in range(int(y0 - h + 20), int(y0), 26):
                for fx in range(int(x + 10), int(x + w - 10), 20):
                    if r.random() < (0.55 if noche else 0.25):
                        b.append(f'<rect x="{fx}" y="{fy}" width="9" height="12" fill="{luz}" opacity="{r.uniform(0.35, 0.9):.2f}"/>')
            if noche and r.random() < 0.25:
                neon = r.choice(["#ff3df2", "#2ff3ff", "#7dff3a"])
                b.append(f'<rect x="{x+8:.0f}" y="{y0-h+30:.0f}" width="{w-16:.0f}" height="8" fill="{neon}" opacity="0.9"/>')
                b.append(f'<rect x="{x:.0f}" y="{y0-h+22:.0f}" width="{w:.0f}" height="24" fill="{neon}" opacity="0.25" filter="url(#blur8)"/>')
            x += w + r.uniform(4, 30)
    b.append(f'<rect x="0" y="1290" width="1080" height="640" fill="url(#{nombre}_m)"/>')
    for _ in range(50):
        y = r.uniform(1300, 1700)
        b.append(f'<rect x="{r.uniform(0,1080):.0f}" y="{y:.0f}" width="{r.uniform(30,180):.0f}" height="4" fill="#ffd8b0" opacity="{r.uniform(0.15,0.5):.2f}"/>')
    # paseo con palmeras en primer plano
    b.append('<path d="M0 1680 Q540 1640 1080 1680 L1080 1920 L0 1920 Z" fill="#140818"/>')
    for x, s in [(70, 1.25), (300, 0.9), (820, 1.1), (1010, 1.35)]:
        b.append(palmera(x, 1690, s, "#160a1e", "#ff9a6a"))
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def hoja_calendario(nombre, texto, color="#e0473a"):
    w, h = 520, 600
    d = lg(f"{nombre}_p", (0, "#ffffff"), (1, "#ece6da"))
    b = ['<g filter="url(#sombra)">', f'<rect x="20" y="40" width="480" height="540" rx="22" fill="url(#{nombre}_p)"/>',
         f'<path d="M20 62 Q20 40 42 40 L478 40 Q500 40 500 62 L500 170 L20 170 Z" fill="{color}"/>',
         *[f'<circle cx="{80+i*90}" cy="40" r="14" fill="#3a3d42"/>' for i in range(5)],
         f'<text x="260" y="410" font-family="DejaVu Sans" font-weight="bold" font-size="150" text-anchor="middle" fill="#2a2a2a">{texto}</text>',
         '</g>']
    guardar(nombre, "".join(b), w, h, d)


def mando():
    """Mando de consola genérico (sin marca)."""
    w, h = 760, 480
    d = lg("md_c", (0, "#4a4f5a"), (0.5, "#2a2d34"), (1, "#121418")) + rg("md_b", (0, "#ffffff", 0.45), (1, "#ffffff", 0))
    b = ['<g filter="url(#sombra)">',
         '<path d="M150 120 Q380 70 610 120 Q720 140 740 300 Q760 440 650 450 Q590 455 540 360 L220 360 Q170 455 110 450 Q0 440 20 300 Q40 140 150 120 Z" fill="url(#md_c)"/>',
         '<path d="M170 140 Q380 100 590 140" stroke="#8a90a0" stroke-width="6" fill="none" opacity="0.6"/>',
         '<ellipse cx="300" cy="150" rx="200" ry="40" fill="url(#md_b)"/>',
         # cruceta
         '<rect x="150" y="215" width="40" height="120" rx="8" fill="#16181d"/><rect x="110" y="255" width="120" height="40" rx="8" fill="#16181d"/>',
         # botones de colores genéricos
         '<circle cx="580" cy="220" r="26" fill="#2ff3ff"/><circle cx="630" cy="270" r="26" fill="#ff3d6a"/>',
         '<circle cx="530" cy="270" r="26" fill="#7dff3a"/><circle cx="580" cy="320" r="26" fill="#ffe93d"/>',
         # joysticks
         '<circle cx="290" cy="330" r="46" fill="#0c0d10"/><circle cx="290" cy="322" r="34" fill="#3a3e48"/>',
         '<circle cx="470" cy="330" r="46" fill="#0c0d10"/><circle cx="470" cy="322" r="34" fill="#3a3e48"/>',
         '<circle cx="380" cy="200" r="16" fill="#ffffff" opacity="0.8"/>', '</g>']
    guardar("mando", "".join(b), w, h, d)


def coche_policia():
    """Coche patrulla genérico de perfil, sin escudos ni marcas."""
    w, h = 900, 400
    d = lg("cp_c", (0, "#ffffff"), (0.55, "#dfe3ea"), (0.56, "#1a1d24"), (1, "#0a0b0e")) + lg("cp_v", (0, "#9ad8ff"), (1, "#2a4a6a"))
    b = ['<ellipse cx="450" cy="360" rx="420" ry="22" fill="#000" opacity="0.45" filter="url(#blur8)"/>',
         '<path d="M40 300 L60 210 Q80 180 160 170 L270 160 L360 90 Q380 80 420 80 L600 80 Q640 80 670 110 L740 170 L820 185 Q870 195 870 240 L870 310 Z" fill="url(#cp_c)"/>',
         '<path d="M290 165 L370 100 L500 100 L500 165 Z" fill="url(#cp_v)"/><path d="M520 100 L600 100 Q630 100 650 120 L700 165 L520 165 Z" fill="url(#cp_v)"/>',
         '<rect x="420" y="58" width="120" height="26" rx="8" fill="#ff2d55"/><rect x="480" y="58" width="60" height="26" rx="8" fill="#2f7bff"/>',
         '<rect x="60" y="245" width="810" height="10" fill="#2f7bff" opacity="0.7"/>',
         '<rect x="820" y="210" width="40" height="22" rx="6" fill="#ffe9a0"/><rect x="45" y="220" width="30" height="20" rx="5" fill="#ff4a3a"/>']
    for cx in (210, 700):
        b.append(f'<circle cx="{cx}" cy="310" r="72" fill="#0a0a0c"/><circle cx="{cx}" cy="310" r="40" fill="#8a8f9a"/><circle cx="{cx}" cy="310" r="14" fill="#2a2d34"/>')
    guardar("coche_policia", "".join(b), w, h, d)


def consola():
    """Consola de sobremesa genérica (caja negra con luz), sin forma de ninguna marca."""
    w, h = 420, 640
    d = lg("cs_c", (0, "#2a2d34"), (1, "#0c0d10"), x2=1, y2=0)
    b = ['<g filter="url(#sombra)">', '<rect x="80" y="40" width="260" height="560" rx="30" fill="url(#cs_c)"/>',
         '<rect x="100" y="60" width="16" height="520" rx="8" fill="#ffffff" opacity="0.12"/>',
         '<rect x="190" y="120" width="40" height="8" rx="4" fill="#2ff3ff"/><rect x="170" y="112" width="80" height="24" rx="10" fill="#2ff3ff" opacity="0.3" filter="url(#blur8)"/>',
         *[f'<rect x="{140+k*14}" y="480" width="6" height="80" rx="3" fill="#000" opacity="0.6"/>' for k in range(10)], '</g>']
    guardar("consola", "".join(b), w, h, d)


def tele_reproductor():
    """Pantalla con botón de reproducir (vídeo genérico) y barra de progreso."""
    w, h = 900, 600
    d = lg("tv_p", (0, "#1a2a5a"), (0.6, "#6a2a7a"), (1, "#ff7a5a"))
    b = ['<g filter="url(#sombra)">', '<rect x="20" y="20" width="860" height="500" rx="26" fill="#0c0d10"/>',
         '<rect x="44" y="44" width="812" height="452" rx="12" fill="url(#tv_p)"/>',
         # skyline genérico dentro de la pantalla
         *[f'<rect x="{60+k*70}" y="{300-((k*53)%140)}" width="58" height="{196+((k*53)%140)}" fill="#1a0a2a" opacity="0.8"/>' for k in range(11)],
         '<circle cx="450" cy="270" r="80" fill="#ffffff" opacity="0.25"/><path d="M425 230 L425 310 L495 270 Z" fill="#ffffff"/>',
         '<rect x="70" y="460" width="760" height="10" rx="5" fill="#ffffff" opacity="0.3"/><rect x="70" y="460" width="300" height="10" rx="5" fill="#2ff3ff"/>',
         '<rect x="380" y="520" width="140" height="50" fill="#16181d"/><rect x="300" y="560" width="300" height="20" rx="10" fill="#16181d"/>', '</g>']
    guardar("tele", "".join(b), w, h, d)


def rascacielos_deco():
    """Torre art déco genérica (inspirada en los rascacielos de los años treinta) con andamio."""
    w, h = 500, 1500
    d = lg("rd_c", (0, "#e8d8b8"), (0.5, "#b8a080"), (1, "#6a5a48"), x2=1, y2=0)
    b = []
    tramos = [(60, 440, 1500, 900), (110, 390, 900, 600), (150, 350, 600, 380), (190, 310, 380, 250), (220, 280, 250, 140)]
    for x0, x1, yb, yt in tramos:
        b.append(f'<rect x="{x0}" y="{yt}" width="{x1-x0}" height="{yb-yt}" fill="url(#rd_c)"/>')
        for fx in range(x0 + 14, x1 - 10, 22):
            b.append(f'<rect x="{fx}" y="{yt+10}" width="8" height="{yb-yt-20}" fill="#4a3a2a" opacity="0.35"/>')
    b.append('<rect x="244" y="20" width="12" height="130" fill="#b8a080"/><circle cx="250" cy="18" r="8" fill="#ffe9a0"/>')
    guardar("rascacielos", "".join(b), w, h, d)


def grua():
    w, h = 700, 900
    b = ['<g stroke="#ffb02a" stroke-width="8" fill="none">', '<path d="M120 900 L120 120 M170 900 L170 120"/>']
    for y in range(120, 900, 50):
        b.append(f'<path d="M120 {y} L170 {y+50} M170 {y} L120 {y+50}"/>')
    b += ['<path d="M40 120 L680 120 M40 160 L680 160"/>', *[f'<path d="M{x} 120 L{x+40} 160 M{x+40} 120 L{x} 160"/>' for x in range(40, 680, 40)],
          '<path d="M600 160 L600 500" stroke="#c8c8c8" stroke-width="4"/>', '</g>', '<rect x="560" y="500" width="80" height="60" fill="#6a5a48"/>',
          '<rect x="90" y="80" width="110" height="40" fill="#ffb02a"/>']
    guardar("grua", "".join(b), w, h)


def atril():
    """Atril de discurso con micrófonos (el discurso de 1961 sin dibujar a nadie)."""
    w, h = 600, 800
    d = lg("at_m", (0, "#7a4a2a"), (1, "#3a1e10"), x2=1, y2=0)
    b = ['<g filter="url(#sombra)">', '<rect x="60" y="740" width="480" height="50" rx="8" fill="#3a1e10"/>',
         '<path d="M170 330 L430 330 L400 740 L200 740 Z" fill="url(#at_m)"/>',
         '<path d="M40 330 L560 330 L520 250 L80 250 Z" fill="#8a5a3a"/>',
         '<circle cx="300" cy="500" r="56" fill="#d8c070" opacity="0.85"/><circle cx="300" cy="500" r="40" fill="none" stroke="#8a6a20" stroke-width="6"/>',
         *[f'<path d="M{240+k*40} 250 L{220+k*50} 120" stroke="#2a2a2a" stroke-width="8"/><rect x="{205+k*50}" y="80" width="34" height="60" rx="14" fill="#3a3a3a"/>' for k in range(3)],
         '<path d="M150 300 L450 300 L430 262 L170 262 Z" fill="#f4f0e4"/>', '</g>']
    guardar("atril", "".join(b), w, h, d)


def reloj_arena():
    w, h = 400, 640
    d = lg("ra_m", (0, "#a87a4a"), (1, "#5a3a1a")) + lg("ra_v", (0, "#cfefff"), (1, "#8ab8d8"))
    b = ['<g filter="url(#sombra)">', '<rect x="40" y="20" width="320" height="40" rx="10" fill="url(#ra_m)"/>', '<rect x="40" y="580" width="320" height="40" rx="10" fill="url(#ra_m)"/>',
         '<rect x="60" y="60" width="20" height="520" fill="url(#ra_m)"/><rect x="320" y="60" width="20" height="520" fill="url(#ra_m)"/>',
         '<path d="M100 60 L300 60 Q300 220 210 320 Q300 420 300 580 L100 580 Q100 420 190 320 Q100 220 100 60 Z" fill="url(#ra_v)" opacity="0.35" stroke="#e8f8ff" stroke-width="4"/>',
         '<path d="M140 190 L260 190 Q240 260 205 300 L195 300 Q160 260 140 190 Z" fill="#f2c060"/>',
         '<path d="M120 580 Q200 470 280 580 Z" fill="#f2c060"/><rect x="198" y="300" width="4" height="270" fill="#f2c060"/>', '</g>']
    guardar("reloj_arena", "".join(b), w, h, d)


def trofeo():
    w, h = 420, 560
    d = lg("tr_o", (0, "#fff2a0"), (0.4, "#ffc83a"), (1, "#b07a10"), x2=1, y2=0)
    b = ['<g filter="url(#sombra)">', '<path d="M90 60 L330 60 Q330 260 210 300 Q90 260 90 60 Z" fill="url(#tr_o)"/>',
         '<path d="M90 90 Q20 90 30 160 Q40 220 110 220" stroke="#ffc83a" stroke-width="18" fill="none"/>',
         '<path d="M330 90 Q400 90 390 160 Q380 220 310 220" stroke="#ffc83a" stroke-width="18" fill="none"/>',
         '<rect x="185" y="300" width="50" height="110" fill="url(#tr_o)"/><rect x="110" y="410" width="200" height="40" rx="8" fill="url(#tr_o)"/>',
         '<rect x="90" y="450" width="240" height="80" rx="10" fill="#3a2a1a"/>',
         '<path d="M160 90 Q170 200 200 260" stroke="#ffffff" stroke-width="10" opacity="0.5" fill="none"/>', '</g>']
    guardar("trofeo", "".join(b), w, h, d)


# ====================================================================== 02 · estrella de neutrones
def terron(nombre="terron", brillo_azul=True):
    """Terrón de azúcar con brillo azul por dentro (materia de estrella de neutrones)."""
    w = h = 420
    d = lg(f"{nombre}_t", (0, "#ffffff"), (1, "#d8dce8")) + lg(f"{nombre}_l", (0, "#eef0f8"), (1, "#a8b0c8")) + lg(f"{nombre}_f", (0, "#c8cee0"), (1, "#8a92b0"))
    d += rg(f"{nombre}_g", (0, "#bff6ff", 0.95), (0.5, "#2ff3ff", 0.5), (1, "#2ff3ff", 0))
    b = []
    if brillo_azul:
        b.append(f'<circle cx="210" cy="230" r="200" fill="url(#{nombre}_g)"/>')
    b += [f'<path d="M80 150 L240 100 L360 160 L200 210 Z" fill="url(#{nombre}_t)"/>',
          f'<path d="M80 150 L200 210 L200 360 L80 300 Z" fill="url(#{nombre}_l)"/>',
          f'<path d="M200 210 L360 160 L360 310 L200 360 Z" fill="url(#{nombre}_f)"/>']
    r = random.Random(5)
    for _ in range(90):  # cristalitos
        x, y = r.uniform(90, 350), r.uniform(110, 350)
        b.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="5" height="5" fill="#ffffff" opacity="{r.uniform(0.3,0.9):.2f}" transform="rotate({r.uniform(0,90):.0f} {x:.0f} {y:.0f})"/>')
    if brillo_azul:
        b.append('<path d="M200 210 L200 360" stroke="#7df9ff" stroke-width="4" opacity="0.8"/><path d="M80 150 L200 210 L360 160" stroke="#bff6ff" stroke-width="3" opacity="0.8" fill="none"/>')
    guardar(nombre, "".join(b), w, h, d)


def montana():
    w, h = 1080, 900
    d = lg("mo_r", (0, "#8a7aa8"), (0.6, "#4a3a6a"), (1, "#1a1430")) + lg("mo_n", (0, "#ffffff"), (1, "#c8d8ff"))
    b = ['<path d="M0 900 L260 380 L380 470 L560 90 L760 420 L860 330 L1080 900 Z" fill="url(#mo_r)"/>',
         '<path d="M560 90 L500 220 L540 200 L580 260 L620 210 L660 250 Z" fill="url(#mo_n)"/>',
         '<path d="M260 380 L225 450 L262 430 L290 460 L320 430 Z" fill="url(#mo_n)" opacity="0.9"/>',
         '<path d="M560 90 L760 420 L1080 900 L700 900 Z" fill="#000" opacity="0.25"/>']
    r = random.Random(9)
    for _ in range(40):
        x = r.uniform(100, 1000); y = r.uniform(500, 880)
        b.append(f'<path d="M{x:.0f} {y:.0f} l12 -40 l12 40 Z" fill="#1a2a20" opacity="0.8"/>')
    guardar("montana", "".join(b), w, h, d)


def bascula_rota():
    """Báscula de baño con el cristal roto (el terrón la revienta)."""
    w, h = 700, 300
    d = lg("bs_c", (0, "#f4f6fa"), (1, "#a8b0c0"))
    b = ['<ellipse cx="350" cy="270" rx="320" ry="24" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         '<rect x="40" y="80" width="620" height="180" rx="40" fill="url(#bs_c)"/>',
         '<rect x="250" y="120" width="200" height="70" rx="10" fill="#1a1d24"/>',
         '<text x="350" y="172" font-family="DejaVu Sans Mono" font-weight="bold" font-size="48" text-anchor="middle" fill="#ff3d3d">ERR</text>',
         '<path d="M150 90 L230 160 L200 220 M230 160 L320 140 M500 90 L460 170 L540 230 M460 170 L400 200" stroke="#3a3d48" stroke-width="5" fill="none"/>']
    guardar("bascula_rota", "".join(b), w, h, d)


def atomo():
    w = h = 600
    d = rg("at_n", (0, "#ffe9a0", 1), (1, "#ff7a2a", 1))
    b = [f'<ellipse cx="300" cy="300" rx="270" ry="90" fill="none" stroke="#2ff3ff" stroke-width="5" opacity="0.8" transform="rotate({a} 300 300)"/>' for a in (0, 60, 120)]
    r = random.Random(3)
    for k in range(9):
        x = 300 + r.uniform(-34, 34); y = 300 + r.uniform(-34, 34)
        col = "#ff5a3a" if k % 2 else "#9aa4b8"
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="24" fill="{col}"/><circle cx="{x-7:.0f}" cy="{y-7:.0f}" r="8" fill="#ffffff" opacity="0.5"/>')
    for a in (0, 120, 240):
        x = 300 + 270 * math.cos(math.radians(a)); y = 300 + 90 * math.sin(math.radians(a))
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="14" fill="#7df9ff"/>')
    guardar("atomo", "".join(b), w, h, d)


def bola_neutrones():
    """Bola de neutrones apretados (todos grises, pegados)."""
    w = h = 700
    d = rg("bn_g", (0, "#ffffff", 0.0), (0.7, "#2ff3ff", 0.15), (1, "#2ff3ff", 0))
    b = ['<circle cx="350" cy="350" r="340" fill="url(#bn_g)"/>']
    r = random.Random(12)
    pts = []
    for _ in range(4000):
        x, y = r.uniform(70, 630), r.uniform(70, 630)
        if (x - 350) ** 2 + (y - 350) ** 2 < 270 ** 2 and all((x - a) ** 2 + (y - c) ** 2 > 33 ** 2 for a, c in pts[-60:]):
            pts.append((x, y))
    for x, y in sorted(pts, key=lambda p: p[1]):
        sh = 0.55 + 0.45 * (1 - ((x - 300) ** 2 + (y - 300) ** 2) ** 0.5 / 380)
        c = int(120 + 110 * sh)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="20" fill="rgb({c},{c+8},{c+24})"/><circle cx="{x-6:.0f}" cy="{y-6:.0f}" r="6" fill="#ffffff" opacity="0.45"/>')
    guardar("bola_neutrones", "".join(b), w, h, d)


def mapa_ciudad():
    """Mancha de ciudad vista desde arriba (calles), para comparar con los ~20 km."""
    w = h = 900
    d = rg("mc_g", (0, "#ffd27a", 0.9), (0.6, "#ff9a3a", 0.5), (1, "#ff9a3a", 0))
    r = random.Random(17)
    b = ['<circle cx="450" cy="450" r="430" fill="url(#mc_g)" opacity="0.6"/>']
    for k in range(-400, 401, 34):
        b.append(f'<path d="M{450+k} 40 L{450+k+r.uniform(-30,30):.0f} 860" stroke="#ffe9a0" stroke-width="{3 if k%136 else 7}" opacity="0.55"/>')
        b.append(f'<path d="M40 {450+k} L860 {450+k+r.uniform(-30,30):.0f}" stroke="#ffe9a0" stroke-width="{3 if k%136 else 7}" opacity="0.55"/>')
    b.append('<path d="M60 600 Q300 520 450 560 Q650 610 860 480" stroke="#2ff3ff" stroke-width="22" fill="none" opacity="0.7"/>')
    guardar("mapa_ciudad", "".join(b), w, h, d)


def batidora():
    w, h = 420, 760
    d = lg("bt_v", (0, "#e8f8ff"), (1, "#9ac8e0"), x2=1, y2=0) + lg("bt_b", (0, "#5a6070"), (1, "#1a1d24"))
    b = ['<g filter="url(#sombra)">', '<path d="M90 60 L330 60 L300 480 L120 480 Z" fill="url(#bt_v)" opacity="0.45" stroke="#e8f8ff" stroke-width="6"/>',
         '<path d="M110 260 L310 260 L300 480 L120 480 Z" fill="#ff7aa8" opacity="0.8"/>',
         '<path d="M210 470 L210 380 M160 400 L260 400" stroke="#d8dce8" stroke-width="10"/>',
         '<rect x="80" y="40" width="260" height="30" rx="10" fill="#3a3d48"/>',
         '<path d="M90 480 L330 480 L360 720 L60 720 Z" fill="url(#bt_b)"/>', '<circle cx="210" cy="610" r="40" fill="#2a2d34" stroke="#7df9ff" stroke-width="5"/>', '</g>']
    guardar("batidora", "".join(b), w, h, d)


def malvavisco():
    w, h = 300, 260
    d = lg("mv_l", (0, "#ffffff"), (1, "#f0d8e8")) + lg("mv_t", (0, "#ffffff"), (1, "#fff4fa"))
    b = ['<rect x="40" y="70" width="220" height="160" rx="50" fill="url(#mv_l)"/>', '<ellipse cx="150" cy="80" rx="110" ry="40" fill="url(#mv_t)"/>',
         '<ellipse cx="110" cy="70" rx="40" ry="10" fill="#ffffff" opacity="0.9"/>', '<path d="M60 150 Q150 170 240 150" stroke="#e8c8d8" stroke-width="5" fill="none"/>']
    guardar("malvavisco", "".join(b), w, h, d)


def bomba_flash():
    """Hongo de luz estilizado, sin detalles (para «la energía de mil bombas»)."""
    w, h = 700, 800
    d = rg("bf_g", (0, "#ffffff", 1), (0.3, "#fff2a0", 1), (0.7, "#ff9a3a", 0.8), (1, "#ff3a1a", 0)) + lg("bf_t", (0, "#ffd27a"), (1, "#ff6a2a"))
    b = ['<ellipse cx="350" cy="260" rx="300" ry="200" fill="url(#bf_g)"/>', '<path d="M300 400 Q290 600 250 780 L450 780 Q410 600 400 400 Z" fill="url(#bf_t)" opacity="0.85"/>',
         '<ellipse cx="350" cy="780" rx="340" ry="40" fill="#ff9a3a" opacity="0.6" filter="url(#blur20)"/>']
    guardar("bomba_flash", "".join(b), w, h, d)


def antenas():
    """Campo de antenas de hilo sobre postes (radiotelescopio de 1967), al amanecer."""
    w, h = 1080, 1920
    d = lg("an_c", (0, "#1a2a4a"), (0.55, "#6a7aa8"), (0.75, "#ffc890"), (1, "#3a4a2a")) + lg("an_s", (0, "#4a6a3a"), (1, "#1a2a14"))
    r = random.Random(6)
    b = ['<rect width="1080" height="1920" fill="url(#an_c)"/>', '<rect y="1280" width="1080" height="640" fill="url(#an_s)"/>']
    for fila in range(6):
        y = 1300 + fila * 90; esc = 0.5 + fila * 0.22
        for k in range(-2, 14):
            x = k * 90 * esc + (fila % 2) * 30
            hgt = 140 * esc
            b.append(f'<path d="M{x:.0f} {y:.0f} L{x:.0f} {y-hgt:.0f}" stroke="#2a1e14" stroke-width="{3*esc:.1f}"/>')
            b.append(f'<path d="M{x:.0f} {y-hgt:.0f} L{x+90*esc:.0f} {y-hgt:.0f}" stroke="#d8d0c0" stroke-width="{1.5*esc:.1f}" opacity="0.8"/>')
            b.append(f'<path d="M{x:.0f} {y-hgt*0.5:.0f} L{x+90*esc:.0f} {y-hgt:.0f}" stroke="#d8d0c0" stroke-width="{1.2*esc:.1f}" opacity="0.6"/>')
    for _ in range(80):
        b.append(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(0,700):.0f}" r="{r.uniform(1,2.5):.1f}" fill="#ffffff" opacity="{r.uniform(0.3,0.9):.2f}"/>')
    b.append(grano())
    guardar("bg_antenas", "".join(b), defs=d)


def papel_registro():
    """Tira de papel de registrador con pulsos regulares."""
    w, h = 1000, 360
    b = ['<g filter="url(#sombra)">', '<rect x="20" y="40" width="960" height="280" fill="#f4ecd8"/>']
    for x in range(40, 980, 40):
        b.append(f'<path d="M{x} 40 L{x} 320" stroke="#e0b8a0" stroke-width="1.5"/>')
    for y in range(60, 320, 40):
        b.append(f'<path d="M20 {y} L980 {y}" stroke="#e0b8a0" stroke-width="1.5"/>')
    pts, x = [], 30
    r = random.Random(4)
    while x < 970:
        pico = (int(x) - 30) % 130 < 6
        pts.append(f"{x:.0f} {180 - (110 if pico else r.uniform(-8, 8)):.0f}")
        x += 3 if pico else 6
    b.append(f'<path d="M{" L".join(pts)}" stroke="#2a2a6a" stroke-width="4" fill="none"/>')
    b.append('</g>')
    guardar("papel_registro", "".join(b), w, h)


# ====================================================================== 03 · mides menos por la noche
def bg_dormitorio(nombre="bg_dormitorio", noche=True):
    r = random.Random(8)
    if noche:
        d = lg(f"{nombre}_p", (0, "#1a2040"), (1, "#0a0c1a")) + lg(f"{nombre}_v", (0, "#0a1030"), (1, "#2a3a7a"))
    else:
        d = lg(f"{nombre}_p", (0, "#f4dcb8"), (1, "#d8b890")) + lg(f"{nombre}_v", (0, "#8ad0ff"), (1, "#fff0c8"))
    d += lg(f"{nombre}_s", (0, "#6a4a3a"), (1, "#3a2418"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_p)"/>',
         f'<rect x="600" y="300" width="380" height="520" rx="10" fill="url(#{nombre}_v)"/>',
         '<path d="M790 300 L790 820 M600 560 L980 560" stroke="#2a1e18" stroke-width="16"/>',
         '<rect x="590" y="290" width="400" height="540" rx="12" fill="none" stroke="#2a1e18" stroke-width="20"/>']
    if noche:
        b.append('<circle cx="880" cy="420" r="60" fill="#fff4d0"/><circle cx="905" cy="405" r="52" fill="#0a1030"/>')
        b += [f'<circle cx="{r.uniform(620,970):.0f}" cy="{r.uniform(320,800):.0f}" r="2" fill="#fff" opacity="0.8"/>' for _ in range(25)]
        b.append('<path d="M600 820 L380 1500 L1080 1500 L1080 1100 L980 820 Z" fill="#8ab0ff" opacity="0.08"/>')
    else:
        b.append('<circle cx="700" cy="420" r="70" fill="#fff8d0"/>')
        b.append('<path d="M600 820 L380 1500 L1080 1500 L1080 1100 L980 820 Z" fill="#fff4c0" opacity="0.18"/>')
    b.append(f'<rect y="1450" width="1080" height="470" fill="url(#{nombre}_s)"/>')
    for x in range(-40, 1100, 120):
        b.append(f'<path d="M{x} 1450 L{x-60} 1920" stroke="#2a1810" stroke-width="4" opacity="0.5"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def cama():
    w, h = 1000, 520
    d = lg("cm_m", (0, "#8a5a3a"), (1, "#4a2a18")) + lg("cm_s", (0, "#e8eefc"), (1, "#a8b8e0")) + lg("cm_e", (0, "#4a6ad8"), (1, "#2a3a8a"))
    b = ['<ellipse cx="500" cy="500" rx="480" ry="24" fill="#000" opacity="0.45" filter="url(#blur8)"/>',
         '<rect x="30" y="120" width="60" height="380" rx="10" fill="url(#cm_m)"/>', '<rect x="910" y="260" width="60" height="240" rx="10" fill="url(#cm_m)"/>',
         '<rect x="60" y="300" width="900" height="120" rx="18" fill="url(#cm_s)"/>',
         '<ellipse cx="200" cy="290" rx="110" ry="50" fill="#ffffff"/>',
         '<path d="M300 250 Q600 200 940 270 L960 420 L300 420 Z" fill="url(#cm_e)"/>',
         '<path d="M330 300 Q600 260 930 310" stroke="#7a9aff" stroke-width="6" fill="none" opacity="0.6"/>']
    guardar("cama", "".join(b), w, h, d)


def despertador():
    w, h = 420, 460
    d = rg("dp_c", (0, "#ff8a7a", 1), (1, "#c02a2a", 1))
    b = ['<g filter="url(#sombra)">', '<path d="M90 120 L40 60 M330 120 L380 60" stroke="#3a3a3a" stroke-width="16"/>',
         '<circle cx="90" cy="80" r="50" fill="#d8d8d8"/><circle cx="330" cy="80" r="50" fill="#d8d8d8"/>',
         '<circle cx="210" cy="250" r="180" fill="url(#dp_c)"/><circle cx="210" cy="250" r="140" fill="#fff8ea"/>',
         *[f'<rect x="206" y="118" width="8" height="24" fill="#3a3a3a" transform="rotate({a} 210 250)"/>' for a in range(0, 360, 30)],
         '<path d="M210 250 L210 160" stroke="#1a1a1a" stroke-width="10" stroke-linecap="round"/><path d="M210 250 L270 270" stroke="#1a1a1a" stroke-width="8" stroke-linecap="round"/>',
         '<path d="M100 420 L80 450 M320 420 L340 450" stroke="#3a3a3a" stroke-width="16"/>', '</g>']
    guardar("despertador", "".join(b), w, h, d)


def cojin_agua():
    """Disco intervertebral de cerca: cojín translúcido con agua dentro."""
    w, h = 700, 420
    d = rg("cj_g", (0, "#bff6ff", 0.95), (0.6, "#4ac8e8", 0.8), (1, "#1a6aa8", 0.9)) + lg("cj_a", (0, "#e8fbff"), (1, "#4ac8e8"))
    b = ['<ellipse cx="350" cy="230" rx="320" ry="160" fill="url(#cj_g)"/>',
         '<ellipse cx="350" cy="230" rx="320" ry="160" fill="none" stroke="#e8d8c0" stroke-width="22" opacity="0.8"/>',
         '<ellipse cx="350" cy="230" rx="280" ry="130" fill="none" stroke="#e8d8c0" stroke-width="8" opacity="0.5"/>',
         '<ellipse cx="350" cy="230" rx="140" ry="70" fill="url(#cj_a)" opacity="0.8"/>',
         '<ellipse cx="270" cy="160" rx="90" ry="22" fill="#ffffff" opacity="0.6"/>']
    guardar("cojin", "".join(b), w, h, d)


def gota():
    w, h = 120, 170
    d = lg("gt_g", (0, "#e8fbff"), (1, "#2a9ad8"))
    guardar("gota", '<path d="M60 10 Q100 90 100 115 A40 40 0 0 1 20 115 Q20 90 60 10 Z" fill="url(#gt_g)"/><ellipse cx="45" cy="110" rx="10" ry="18" fill="#fff" opacity="0.7"/>', w, h, d)


def silueta_perfil(nombre="perfil", color="#1a1424", borde="#ffb46a"):
    """Persona de pie de perfil en silueta a contraluz, con borde de luz (sin rasgos: no es un personaje)."""
    w, h = 420, 1300
    cuerpo = ('M210 40 Q262 40 268 100 Q272 140 262 160 Q280 170 276 190 Q262 205 250 205 L246 235 Q300 250 310 320 L322 560 '
              'Q324 610 300 615 L292 680 L286 900 L300 1240 Q304 1270 330 1275 L330 1295 L220 1295 L226 1240 L214 900 L200 900 '
              'L196 1240 L204 1295 L120 1295 L124 1270 Q150 1262 152 1240 L160 900 L150 650 L120 600 L130 330 Q150 250 196 235 '
              'L190 200 Q150 190 150 120 Q156 40 210 40 Z')
    b = [f'<path d="{cuerpo}" fill="{color}"/>', f'<path d="{cuerpo}" fill="none" stroke="{borde}" stroke-width="6" opacity="0.8"/>']
    guardar(nombre, "".join(b), w, h)


def tallimetro():
    """Marcas de altura pintadas en un marco de puerta."""
    w, h = 300, 1500
    d = lg("tl_m", (0, "#f4e4c8"), (1, "#c8a880"), x2=1, y2=0)
    b = ['<rect x="60" y="0" width="180" height="1500" fill="url(#tl_m)"/>']
    for k, y in enumerate(range(40, 1500, 30)):
        larga = k % 5 == 0
        b.append(f'<path d="M60 {y} L{60 + (90 if larga else 45)} {y}" stroke="#4a3a2a" stroke-width="{5 if larga else 3}"/>')
    guardar("tallimetro", "".join(b), w, h, d)


def caballo():
    """Caballo de perfil al galope, ilustrado con volumen (cuerpo, crin, luz de borde)."""
    w, h = 1000, 760
    d = lg("cb_c", (0, "#9a5a2a"), (0.6, "#6a3a18"), (1, "#3a1e0c")) + lg("cb_crin", (0, "#2a160a"), (1, "#120804"))
    cuerpo = ('M230 300 Q300 220 470 230 Q620 236 700 220 Q760 160 790 90 Q800 60 830 66 Q880 70 930 120 Q960 150 940 175 Q920 190 880 170 '
              'Q860 200 840 240 Q800 300 790 360 Q780 410 740 420 L700 420 Q600 430 470 430 Q330 430 270 400 Q210 380 230 300 Z')
    b = ['<ellipse cx="500" cy="730" rx="380" ry="20" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         # patas al galope
         '<path d="M300 400 Q250 500 180 560 Q160 580 170 600" stroke="#4a2810" stroke-width="40" fill="none" stroke-linecap="round"/>',
         '<path d="M360 410 Q380 540 330 690" stroke="#5a3214" stroke-width="40" fill="none" stroke-linecap="round"/>',
         '<path d="M690 410 Q740 500 820 540 Q850 560 860 590" stroke="#4a2810" stroke-width="40" fill="none" stroke-linecap="round"/>',
         '<path d="M640 420 Q620 560 680 700" stroke="#5a3214" stroke-width="40" fill="none" stroke-linecap="round"/>',
         f'<path d="{cuerpo}" fill="url(#cb_c)"/>',
         '<path d="M240 300 Q300 236 470 244 Q620 250 700 234" stroke="#ffc890" stroke-width="7" fill="none" opacity="0.6"/>',
         # crin y cola
         '<path d="M790 92 Q740 140 700 220 Q720 180 760 170 Q730 210 720 250 Q770 180 820 120 Z" fill="url(#cb_crin)"/>',
         '<path d="M235 310 Q150 300 90 380 Q60 420 70 470 Q120 400 170 380 Q140 430 150 470 Q200 380 245 340 Z" fill="url(#cb_crin)"/>',
         '<circle cx="880" cy="118" r="9" fill="#120804"/><circle cx="883" cy="115" r="3" fill="#fff"/>',
         '<path d="M800 76 L790 30 L825 66 Z" fill="#5a3214"/>']
    guardar("caballo", "".join(b), w, h, d)


def parroco():
    """Silueta de un párroco del siglo XVIII con sombrero de tres picos y bastón de medir, a contraluz."""
    w, h = 420, 1200
    b = ['<path d="M120 170 L210 120 L300 170 L270 190 L150 190 Z" fill="#141018"/>',
         '<ellipse cx="210" cy="230" rx="60" ry="70" fill="#141018"/>',
         '<path d="M140 300 Q210 280 280 300 L330 1100 Q210 1140 90 1100 Z" fill="#141018"/>',
         '<rect x="198" y="300" width="24" height="40" fill="#e8e0d0"/>',
         '<path d="M340 380 L360 1160" stroke="#3a2a1a" stroke-width="14"/>',
         *[f'<path d="M352 {420+k*70} L372 {420+k*70}" stroke="#e8d8b0" stroke-width="5"/>' for k in range(11)],
         '<path d="M150 300 Q210 280 270 300 L330 1100" stroke="#ffb46a" stroke-width="5" fill="none" opacity="0.7"/>']
    guardar("parroco", "".join(b), w, h)


def bg_campo_1724():
    r = random.Random(14)
    d = lg("cp_c", (0, "#2a2050"), (0.5, "#c06a5a"), (0.7, "#ffc890"), (1, "#5a6a3a")) + lg("cp_s", (0, "#6a7a3a"), (1, "#2a3418"))
    b = ['<rect width="1080" height="1920" fill="url(#cp_c)"/>', '<circle cx="300" cy="1180" r="120" fill="#fff0c0" opacity="0.9"/>',
         '<path d="M0 1260 Q200 1200 420 1240 Q700 1290 1080 1220 L1080 1920 L0 1920 Z" fill="url(#cp_s)"/>',
         # iglesia lejana
         '<rect x="780" y="1080" width="120" height="170" fill="#2a2030"/><path d="M780 1080 L840 1020 L900 1080 Z" fill="#2a2030"/>',
         '<rect x="900" y="980" width="50" height="270" fill="#2a2030"/><path d="M895 980 L925 900 L955 980 Z" fill="#2a2030"/>']
    for _ in range(30):
        x = r.uniform(0, 1080); y = r.uniform(1300, 1900)
        b.append(f'<path d="M{x:.0f} {y:.0f} l6 -30 l6 30" stroke="#8a9a4a" stroke-width="3" fill="none" opacity="0.7"/>')
    b.append(grano())
    guardar("bg_campo", "".join(b), defs=d)


def plato_vacio(dirsvg):
    """Plato de la báscula de la biblioteca (plato_der) sin el punto azul."""
    src = os.path.join(AQUI, "..", "..", "..", "motor", "biblioteca", "svg", "plato_der.svg")
    t = open(src).read().replace('<circle cx="160" cy="318" r="13" fill="#3b82f6" stroke="#fff" stroke-width="3"/>', "")
    open(os.path.join(dirsvg, "plato_vacio.svg"), "w").write(t)


def generar(dirsvg):
    ilus.OUT = dirsvg
    os.makedirs(dirsvg, exist_ok=True)
    plato_vacio(dirsvg)
    bg_ciudad_tropical("bg_ciudad", False, 4); bg_ciudad_tropical("bg_ciudad_noche", True, 6)
    hoja_calendario("hoja_2013", "2013"); hoja_calendario("hoja_2026", "2026", "#2f7bff"); hoja_calendario("hoja_2022", "2022", "#7a3ad8")
    mando(); coche_policia(); consola(); tele_reproductor(); rascacielos_deco(); grua(); atril(); reloj_arena(); trofeo()
    terron("terron"); terron("terron_normal", False); montana(); bascula_rota(); atomo(); bola_neutrones(); mapa_ciudad(); batidora(); malvavisco()
    bomba_flash(); antenas(); papel_registro()
    bg_dormitorio("bg_dormitorio", True); bg_dormitorio("bg_dormitorio_dia", False); cama(); despertador(); cojin_agua(); gota()
    silueta_perfil("perfil"); silueta_perfil("perfil_azul", "#0a1030", "#7df9ff"); tallimetro(); caballo(); parroco(); bg_campo_1724()
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
