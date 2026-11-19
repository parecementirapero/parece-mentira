"""Ilustraciones del lote 2026-11-19-manana (el espacio huele a filete · la canción pegada · la torre de Pisa).
Uso: python3 ilus_hoy.py DIR_SVG (semillas fijas). Ladrillos de motor/biblioteca/ilus.py. Agente 08:00 (Nico).
Reutiliza las piezas de los lotes 2026-11-18 (casco, ISS, cápsula, cerebro, cara de perfil, oreja, escáner, calendario…).
Nada de marcas, logotipos ni personajes: todo genérico y dibujado aquí."""
import importlib.util, math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano, _estrellas_ricas, _neb  # noqa: E402,F401


def _cargar(rel, nombre):
    p = os.path.join(RAIZ, rel)
    d = os.path.dirname(p)
    sys.path.insert(0, d)
    sp = importlib.util.spec_from_file_location(nombre, p)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    sys.path.remove(d)
    sys.modules.pop("ilus_tarde", None)
    return m


# ====================================================================== 01 · el espacio huele a filete
def filete():
    """Filete en una parrilla con marcas, grasa brillante y vapor."""
    w, h = 900, 620
    d = (rg("fl_c", (0, "#c0503a", 1), (0.7, "#7a2a1e", 1), (1, "#4a160e", 1)) + lg("fl_p", (0, "#3a3d44"), (1, "#121318"))
         + rg("fl_b", (0, "#ffffff", 0.5), (1, "#ffffff", 0)))
    b = ['<ellipse cx="450" cy="560" rx="400" ry="40" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         '<rect x="60" y="300" width="780" height="260" rx="30" fill="url(#fl_p)"/>']
    for k in range(9):
        b.append(f'<rect x="{90+k*84}" y="300" width="18" height="250" rx="6" fill="#55585f"/>')
    b += ['<g filter="url(#sombra)"><path d="M150 330 Q170 210 330 200 Q470 170 620 210 Q760 240 760 340 Q770 440 620 470 Q450 500 300 470 Q160 450 150 330 Z" fill="url(#fl_c)"/>',
          '<path d="M170 330 Q190 240 330 225" stroke="#f4e0c8" stroke-width="26" fill="none" stroke-linecap="round" opacity="0.9"/>']
    for k in range(5):
        x = 260 + k * 95
        b.append(f'<path d="M{x} 230 L{x+70} 460" stroke="#2a0a06" stroke-width="20" stroke-linecap="round" opacity="0.85"/>')
    b += ['<ellipse cx="420" cy="270" rx="160" ry="40" fill="url(#fl_b)"/>', '</g>']
    for k, x in enumerate((280, 450, 620)):
        b.append(f'<path d="M{x} 170 Q{x-40} 120 {x} 80 Q{x+40} 40 {x} 0" stroke="#ffffff" stroke-width="16" fill="none" opacity="0.45" stroke-linecap="round" filter="url(#blur8)"/>')
    guardar("filete", "".join(b), w, h, d)


def soldador():
    """Soplete de soldar con el arco encendido (máscara y mano fuera de plano)."""
    w, h = 900, 700
    d = lg("sd_c", (0, "#5a5f6a"), (1, "#1a1c22")) + rg("sd_l", (0, "#ffffff", 1), (0.2, "#b8f4ff", 0.9), (0.6, "#2ff3ff", 0.35), (1, "#2ff3ff", 0))
    b = ['<g filter="url(#sombra)">', '<rect x="380" y="120" width="460" height="110" rx="40" fill="url(#sd_c)" transform="rotate(30 600 170)"/>',
         '<rect x="250" y="320" width="220" height="44" rx="14" fill="#8a8f9a" transform="rotate(30 360 340)"/>',
         '<path d="M600 140 L860 40" stroke="#e05a2a" stroke-width="22" stroke-linecap="round"/>', '</g>',
         '<circle cx="230" cy="470" r="230" fill="url(#sd_l)"/>', '<circle cx="230" cy="470" r="34" fill="#ffffff"/>',
         '<rect x="0" y="560" width="900" height="140" fill="#2a2d34"/>', '<rect x="0" y="560" width="900" height="10" fill="#8a8f9a"/>']
    r = random.Random(5)
    for _ in range(26):
        a = r.uniform(-2.9, -0.2); L = r.uniform(60, 260)
        x1, y1 = 230 + math.cos(a) * 40, 480 + math.sin(a) * 40
        x2, y2 = 230 + math.cos(a) * L, 480 + math.sin(a) * L
        b.append(f'<path d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}" stroke="#ffd27a" stroke-width="{r.uniform(3,7):.1f}" stroke-linecap="round"/>')
    guardar("soldador", "".join(b), w, h, d)


def olor(nombre="olor", color="#ffb46a"):
    """Tres ondas de olor que suben (para colocar encima de un objeto)."""
    w, h = 600, 700
    b = []
    for k, x in enumerate((150, 300, 450)):
        b.append(f'<path d="M{x} 660 C{x-90} 560 {x+90} 470 {x} 370 C{x-90} 270 {x+90} 180 {x} 60" stroke="{color}" stroke-width="30" fill="none" stroke-linecap="round" opacity="0.85"/>')
        b.append(f'<path d="M{x} 660 C{x-90} 560 {x+90} 470 {x} 370 C{x-90} 270 {x+90} 180 {x} 60" stroke="{color}" stroke-width="70" fill="none" stroke-linecap="round" opacity="0.25" filter="url(#blur8)"/>')
    guardar(nombre, "".join(b), w, h)


def oxigeno():
    """Un átomo de oxígeno suelto: bola roja brillante con su «O»."""
    w, h = 300, 300
    d = rg("ox_c", (0, "#ff9a8a", 1), (0.55, "#e0342a", 1), (1, "#7a0a0a", 1), cx=0.38, cy=0.35) + rg("ox_h", (0, "#ff3d3d", 0.6), (1, "#ff3d3d", 0))
    b = ['<circle cx="150" cy="150" r="148" fill="url(#ox_h)"/>', '<circle cx="150" cy="150" r="95" fill="url(#ox_c)"/>',
         '<text x="150" y="182" font-family="DejaVu Sans" font-weight="bold" font-size="96" text-anchor="middle" fill="#ffffff">O</text>']
    guardar("oxigeno", "".join(b), w, h, d)


def matraz():
    """Matraz de laboratorio con líquido ámbar y burbujas."""
    w, h = 500, 700
    d = lg("mz_l", (0, "#ffd27a"), (1, "#c8781e")) + lg("mz_v", (0, "#ffffff"), (1, "#cfe8f4"))
    b = ['<ellipse cx="250" cy="670" rx="200" ry="22" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<path d="M190 60 L310 60 L310 260 L460 600 Q470 650 420 650 L80 650 Q30 650 40 600 L190 260 Z" fill="url(#mz_v)" opacity="0.35" stroke="#e8f6ff" stroke-width="10"/>',
         '<path d="M130 430 L370 430 L452 610 Q458 640 420 640 L80 640 Q42 640 48 610 Z" fill="url(#mz_l)" opacity="0.92"/>',
         '<rect x="170" y="40" width="160" height="34" rx="12" fill="#e8f6ff"/>',
         '<path d="M215 90 L215 250" stroke="#ffffff" stroke-width="12" opacity="0.6" stroke-linecap="round"/>']
    for x, y, r_ in [(200, 560, 18), (290, 520, 12), (250, 600, 10), (330, 590, 16), (180, 480, 9)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="{r_}" fill="#fff4c0" opacity="0.8"/>')
    guardar("matraz", "".join(b), w, h, d)


def perfume():
    """Frasco de perfume genérico (sin marca) con un planeta pintado."""
    w, h = 520, 720
    d = lg("pf_v", (0, "#3a2a7a"), (0.5, "#7a3ad8"), (1, "#1a0a3a"), x2=1, y2=1) + rg("pf_b", (0, "#ffffff", 0.6), (1, "#ffffff", 0))
    b = ['<ellipse cx="260" cy="690" rx="210" ry="22" fill="#000" opacity="0.4" filter="url(#blur8)"/>', '<g filter="url(#sombra)">',
         '<rect x="60" y="240" width="400" height="440" rx="60" fill="url(#pf_v)" stroke="#d8c8ff" stroke-width="8"/>',
         '<rect x="190" y="150" width="140" height="100" rx="16" fill="#c8b0ff"/>', '<rect x="160" y="40" width="200" height="120" rx="30" fill="#e8dcff"/>',
         '<circle cx="260" cy="460" r="110" fill="#ffb46a"/><ellipse cx="260" cy="470" rx="190" ry="34" fill="none" stroke="#ffe9a0" stroke-width="12"/>',
         '<ellipse cx="160" cy="330" rx="40" ry="110" fill="url(#pf_b)"/>', '</g>']
    for x, y in [(110, 300), (400, 330), (380, 600), (130, 610)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#ffffff"/>')
    guardar("perfume", "".join(b), w, h, d)


def polvo_lunar():
    """Nube de polvo gris oscuro con granos (el polvo de la Luna)."""
    w, h = 900, 700
    r = random.Random(12)
    b = []
    for _ in range(26):
        x, y, rr = r.uniform(150, 750), r.uniform(200, 560), r.uniform(70, 170)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.0f}" fill="#{r.choice(["8a8a90", "6a6a72", "a0a0a6", "55555c"])}" opacity="0.55" filter="url(#blur20)"/>')
    for _ in range(160):
        b.append(f'<circle cx="{r.uniform(80,820):.0f}" cy="{r.uniform(120,640):.0f}" r="{r.uniform(2,6):.1f}" fill="#d8d8de" opacity="{r.uniform(0.4,0.9):.2f}"/>')
    guardar("polvo_lunar", "".join(b), w, h)


def guante():
    """Guante de traje espacial con polvo gris en los dedos."""
    w, h = 600, 700
    d = lg("gt_c", (0, "#ffffff"), (1, "#c8ccd4"))
    b = ['<g filter="url(#sombra)">',
         '<path d="M150 690 L150 470 Q120 300 170 250 L190 120 Q200 80 235 90 Q260 100 255 140 L250 240 L280 90 Q290 50 325 60 Q355 70 348 115 L330 240 L380 110 Q395 75 425 90 Q450 105 438 145 L400 270 L460 200 Q490 170 515 195 Q535 220 510 255 L430 380 Q400 450 420 690 Z" fill="url(#gt_c)" stroke="#9aa0ac" stroke-width="8"/>',
         '<rect x="130" y="560" width="310" height="70" rx="16" fill="#e05a2a"/>', '</g>']
    r = random.Random(3)
    for _ in range(90):
        b.append(f'<circle cx="{r.uniform(180,500):.0f}" cy="{r.uniform(80,320):.0f}" r="{r.uniform(2,7):.1f}" fill="#55555c" opacity="{r.uniform(0.4,0.8):.2f}"/>')
    guardar("guante", "".join(b), w, h, d)


def frambuesa(nombre="frambuesa"):
    """Frambuesa con drupas brillantes y hojitas."""
    w, h = 600, 640
    d = rg("fb_d", (0, "#ff8aa8", 1), (0.6, "#d81e4a", 1), (1, "#7a0a24", 1), cx=0.35, cy=0.3)
    b = ['<ellipse cx="300" cy="610" rx="200" ry="20" fill="#000" opacity="0.35" filter="url(#blur8)"/>', '<g filter="url(#sombra)">']
    r = random.Random(4)
    pts = []
    for fila in range(7):
        y = 170 + fila * 58
        anch = 200 - abs(fila - 2.5) * 26
        n = int(anch / 44) + 3
        for k in range(n):
            x = 300 - anch + k * (2 * anch / max(1, n - 1))
            pts.append((x + r.uniform(-6, 6), y + r.uniform(-6, 6)))
    for x, y in pts:
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="38" fill="url(#fb_d)"/>')
        b.append(f'<circle cx="{x-12:.0f}" cy="{y-14:.0f}" r="8" fill="#ffffff" opacity="0.6"/>')
    for a in (-60, -20, 20, 60):
        b.append(f'<path d="M300 140 Q{300+a*2} {80} {300+a*3} {120}" stroke="#3a8a2a" stroke-width="26" fill="none" stroke-linecap="round"/>')
    b.append('</g>')
    guardar(nombre, "".join(b), w, h, d)


def radiotelescopio():
    """Antena parabólica de radiotelescopio sobre una montaña nevada, de noche."""
    w, h = 1080, 1100
    d = lg("rt_p", (0, "#ffffff"), (1, "#b8c0d0"), x2=1, y2=1) + lg("rt_m", (0, "#d8e4f4"), (0.4, "#5a6a8a"), (1, "#1a2238"))
    b = ['<path d="M0 1100 L0 820 L260 560 L420 700 L620 470 L1080 900 L1080 1100 Z" fill="url(#rt_m)"/>',
         '<path d="M620 470 L560 540 L600 530 L640 560 L690 520 Z" fill="#ffffff"/><path d="M260 560 L220 600 L270 595 L300 610 Z" fill="#ffffff"/>',
         '<rect x="560" y="560" width="120" height="200" fill="#c8ccd4"/><rect x="520" y="740" width="200" height="60" fill="#9aa0ac"/>',
         '<g filter="url(#sombra)"><path d="M300 180 Q620 520 940 180 Q620 420 300 180 Z" fill="url(#rt_p)" stroke="#e8eef8" stroke-width="10" transform="rotate(-18 620 330)"/></g>',
         '<path d="M620 420 L590 230 M620 420 L700 220" stroke="#e8eef8" stroke-width="10" transform="rotate(-18 620 330)"/>',
         '<circle cx="610" cy="215" r="20" fill="#e8eef8" transform="rotate(-18 620 330)"/>',
         '<rect x="590" y="400" width="60" height="180" fill="#b8c0d0"/>']
    guardar("radiotelescopio", "".join(b), w, h, d)


def molecula_fruta():
    """Molécula genérica (bolas y palos) en colores de fruta."""
    w, h = 800, 600
    at = [(170, 320, "#3a3d44", 60), (330, 230, "#3a3d44", 60), (490, 320, "#3a3d44", 60), (650, 230, "#ff3d3d", 56),
          (330, 90, "#ff3d3d", 56), (170, 470, "#e8eef8", 36), (490, 470, "#e8eef8", 36), (60, 260, "#e8eef8", 36), (720, 330, "#e8eef8", 36)]
    en = [(0, 1), (1, 2), (2, 3), (1, 4), (0, 5), (2, 6), (0, 7), (3, 8)]
    b = []
    for i, j in en:
        b.append(f'<line x1="{at[i][0]}" y1="{at[i][1]}" x2="{at[j][0]}" y2="{at[j][1]}" stroke="#d8dce4" stroke-width="18"/>')
    d = ""
    for k, (x, y, c, r_) in enumerate(at):
        d += rg(f"mf{k}", (0, "#ffffff", 1), (0.25, c, 1), (1, "#000000", 1), cx=0.35, cy=0.3)
        b.append(f'<circle cx="{x}" cy="{y}" r="{r_}" fill="url(#mf{k})"/>')
    guardar("molecula_fruta", "".join(b), w, h, d)


# ====================================================================== 02 · la canción pegada
def nota(nombre="nota", color="#ff3df2"):
    w, h = 300, 400
    b = [f'<ellipse cx="110" cy="320" rx="80" ry="58" fill="{color}" transform="rotate(-22 110 320)"/>',
         f'<rect x="168" y="40" width="24" height="290" fill="{color}"/>',
         f'<path d="M192 40 Q290 90 260 200 Q250 130 192 120 Z" fill="{color}"/>',
         f'<ellipse cx="110" cy="320" rx="120" ry="90" fill="{color}" opacity="0.25" filter="url(#blur20)"/>']
    guardar(nombre, "".join(b), w, h)


def auriculares():
    w, h = 800, 700
    d = lg("au_c", (0, "#3a3d44"), (1, "#0c0d10")) + lg("au_a", (0, "#ff5ad8"), (1, "#9a1a7a"))
    b = ['<g filter="url(#sombra)">', '<path d="M140 470 Q120 90 400 80 Q680 90 660 470" stroke="url(#au_c)" stroke-width="56" fill="none" stroke-linecap="round"/>',
         '<rect x="70" y="400" width="170" height="250" rx="70" fill="url(#au_a)"/><rect x="560" y="400" width="170" height="250" rx="70" fill="url(#au_a)"/>',
         '<rect x="110" y="440" width="40" height="170" rx="20" fill="#ffffff" opacity="0.25"/>', '</g>']
    guardar("auriculares", "".join(b), w, h, d)


def gusano():
    """Gusanito simpático con auriculares (el «gusano del oído»)."""
    w, h = 900, 700
    d = rg("gs_c", (0, "#ffd0e0", 1), (0.7, "#ff7aa8", 1), (1, "#c83a6a", 1), cx=0.4, cy=0.3)
    b = ['<ellipse cx="450" cy="640" rx="380" ry="28" fill="#000" opacity="0.35" filter="url(#blur8)"/>', '<g filter="url(#sombra)">']
    for k in range(7):
        x = 140 + k * 92
        y = 520 - math.sin(k * 0.9) * 60
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{78 - k*2}" fill="url(#gs_c)"/>')
        b.append(f'<path d="M{x-40:.0f} {y-40:.0f} Q{x:.0f} {y-70:.0f} {x+40:.0f} {y-40:.0f}" stroke="#c83a6a" stroke-width="5" fill="none" opacity="0.5"/>')
    hx, hy = 760, 300
    b += [f'<circle cx="{hx}" cy="{hy}" r="120" fill="url(#gs_c)"/>',
          f'<circle cx="{hx-40}" cy="{hy-20}" r="22" fill="#141414"/><circle cx="{hx+30}" cy="{hy-20}" r="22" fill="#141414"/>',
          f'<circle cx="{hx-34}" cy="{hy-28}" r="8" fill="#ffffff"/><circle cx="{hx+36}" cy="{hy-28}" r="8" fill="#ffffff"/>',
          f'<path d="M{hx-40} {hy+40} Q{hx} {hy+80} {hx+40} {hy+40}" stroke="#141414" stroke-width="10" fill="none" stroke-linecap="round"/>',
          f'<path d="M{hx-118} {hy+10} Q{hx-120} {hy-170} {hx} {hy-170} Q{hx+120} {hy-170} {hx+118} {hy+10}" stroke="#2a2d34" stroke-width="22" fill="none"/>',
          f'<rect x="{hx-150}" y="{hy-40}" width="60" height="110" rx="26" fill="#2ff3ff"/><rect x="{hx+90}" y="{hy-40}" width="60" height="110" rx="26" fill="#2ff3ff"/>',
          '</g>']
    guardar("gusano", "".join(b), w, h, d)


def chicle():
    """Paquete de chicles genérico con una pastilla fuera."""
    w, h = 800, 600
    d = lg("ch_p", (0, "#7df9ff"), (1, "#1a8ab0")) + lg("ch_c", (0, "#ffffff"), (1, "#ffc8e0"))
    b = ['<ellipse cx="400" cy="560" rx="330" ry="24" fill="#000" opacity="0.35" filter="url(#blur8)"/>', '<g filter="url(#sombra)">',
         '<rect x="80" y="200" width="520" height="300" rx="30" fill="url(#ch_p)"/>', '<rect x="80" y="300" width="520" height="80" fill="#ffffff" opacity="0.85"/>',
         '<path d="M140 340 Q200 300 260 340 T380 340 T500 340" stroke="#1a8ab0" stroke-width="14" fill="none"/>',
         '<rect x="440" y="90" width="300" height="130" rx="40" fill="url(#ch_c)" transform="rotate(-14 590 155)"/>', '</g>']
    guardar("chicle", "".join(b), w, h, d)


def globo_chicle():
    w, h = 600, 600
    d = rg("gb_c", (0, "#ffe0ee", 1), (0.6, "#ff7ab8", 1), (1, "#d83a8a", 1), cx=0.35, cy=0.3)
    b = ['<circle cx="300" cy="300" r="270" fill="url(#gb_c)"/>', '<ellipse cx="210" cy="190" rx="70" ry="40" fill="#ffffff" opacity="0.6" transform="rotate(-30 210 190)"/>']
    guardar("globo_chicle", "".join(b), w, h, d)


def mandibula():
    """Perfil de cara masticando: dos piezas, cara de arriba y mandíbula (gira en la bisagra 330,560 de 900×1100)."""
    w, h = 900, 1100
    d = lg("mb_p", (0, "#f2c4a0"), (1, "#c8845a"))
    sup = ['<path d="M300 1100 L300 820 Q160 700 180 480 Q200 200 470 140 Q700 110 760 330 Q780 420 740 470 L800 560 Q810 590 770 600 L560 600 L330 560 Z" fill="url(#mb_p)"/>',
           '<path d="M220 330 Q330 120 600 160 Q520 60 380 90 Q200 140 180 360 Z" fill="#3a2418"/>',
           '<ellipse cx="640" cy="360" rx="22" ry="14" fill="#2a1a12"/>', '<path d="M600 320 Q640 300 680 318" stroke="#2a1a12" stroke-width="8" fill="none"/>',
           '<path d="M330 380 Q300 300 360 300 Q400 320 380 420 Q350 450 330 380 Z" fill="#d89a70"/>']
    guardar("cara_sup", "".join(sup), w, h, d)
    inf = ['<path d="M330 560 L560 600 L770 600 Q790 640 760 700 Q700 790 560 800 Q420 810 330 760 Z" fill="url(#mb_p)"/>',
           '<path d="M700 640 Q730 660 760 640" stroke="#a04a3a" stroke-width="10" fill="none" stroke-linecap="round"/>']
    guardar("cara_inf", "".join(inf), w, h, d)


def bg_aula(nombre="bg_aula"):
    """Fondo de universidad: pared, pizarra con ondas y ventanas."""
    d = lg(f"{nombre}_p", (0, "#2a3048"), (1, "#141828")) + lg(f"{nombre}_s", (0, "#3a2a24"), (1, "#1a1210"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_p)"/>',
         '<rect x="90" y="380" width="900" height="560" rx="16" fill="#1a3a2a" stroke="#6a4a2a" stroke-width="22"/>',
         '<path d="M150 660 Q230 520 310 660 T470 660 T630 660 T790 660 T950 660" stroke="#e8f4e8" stroke-width="8" fill="none" opacity="0.7"/>',
         '<path d="M150 820 L950 820" stroke="#e8f4e8" stroke-width="4" opacity="0.4"/>',
         f'<rect x="0" y="1420" width="1080" height="500" fill="url(#{nombre}_s)"/>']
    for x in (120, 620):
        b.append(f'<rect x="{x}" y="1060" width="340" height="300" rx="10" fill="#4a6aa8" opacity="0.5"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


# ====================================================================== 03 · la torre de Pisa
def torre_pisa(nombre="torre_pisa", color="#f4ecdc", sombra="#c8b898", pisos=8, curva=0.0):
    """Torre de Pisa RECTA (la inclinación se pone con rot): 8 cuerpos con arcadas. Base en (300, 1580) de 600×1600."""
    w, h = 600, 1600
    d = lg(f"{nombre}_c", (0, sombra), (0.35, color), (0.6, "#ffffff"), (1, sombra), x2=1, y2=0)
    b = [f'<ellipse cx="300" cy="1585" rx="260" ry="20" fill="#000" opacity="0.35" filter="url(#blur8)"/>']
    x0, x1 = 120, 480
    alturas = [300, 160, 160, 160, 160, 160, 160, 170]
    y = 1580
    for k, hh in enumerate(alturas[:pisos]):
        top = y - hh
        dx = curva * max(0, k - 3) ** 1.3
        x0, x1 = 120 + dx, 480 + dx
        if k == 7:
            xa, xb = 175 + dx, 425 + dx
        else:
            xa, xb = x0, x1
        b.append(f'<rect x="{xa}" y="{top}" width="{xb-xa}" height="{hh}" fill="url(#{nombre}_c)"/>')
        b.append(f'<rect x="{xa-12}" y="{top-14}" width="{xb-xa+24}" height="18" fill="{color}" stroke="{sombra}" stroke-width="3"/>')
        n = 6 if k < 7 else 4
        aw = (xb - xa) / n
        for j in range(n):
            ax = xa + j * aw
            if k == 0:
                b.append(f'<path d="M{ax+10:.0f} {y} L{ax+10:.0f} {top+80} Q{ax+aw/2:.0f} {top+30} {ax+aw-10:.0f} {top+80} L{ax+aw-10:.0f} {y} Z" fill="{sombra}" opacity="0.75"/>')
            else:
                b.append(f'<path d="M{ax+8:.0f} {y-6} L{ax+8:.0f} {top+50} Q{ax+aw/2:.0f} {top+12} {ax+aw-8:.0f} {top+50} L{ax+aw-8:.0f} {y-6} Z" fill="#6a5a48" opacity="0.55"/>')
                b.append(f'<rect x="{ax+aw-6:.0f}" y="{top+10}" width="12" height="{hh-16}" fill="#ffffff" opacity="0.8"/>')
        y = top - 14
    guardar(nombre, "".join(b), w, h, d)


def bg_plaza(nombre="bg_plaza", tarde=False):
    """Cielo, catedral genérica a lo lejos y césped verde (plaza italiana)."""
    if tarde:
        cielo = lg(f"{nombre}_c", (0, "#3a2a6a"), (0.5, "#e88a6a"), (1, "#ffd8a0"))
    else:
        cielo = lg(f"{nombre}_c", (0, "#3a7ad8"), (0.6, "#9ad0ff"), (1, "#e8f4ff"))
    d = cielo + lg(f"{nombre}_h", (0, "#7ac84a"), (1, "#2a6a1e"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>']
    r = random.Random(7)
    for _ in range(6):
        x, y = r.uniform(0, 1080), r.uniform(150, 800)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(90,200):.0f}" ry="{r.uniform(26,50):.0f}" fill="#ffffff" opacity="0.7" filter="url(#blur8)"/>')
    # catedral genérica
    b += ['<rect x="-40" y="1180" width="560" height="260" fill="#e8dcc8"/>', '<path d="M-40 1180 L240 1060 L520 1180 Z" fill="#d8ccb8"/>',
          '<ellipse cx="240" cy="1060" rx="90" ry="70" fill="#c8b8a0"/>']
    for k in range(9):
        b.append(f'<path d="M{-20+k*60} 1440 L{-20+k*60} 1260 Q{k*60+5} 1225 {30+k*60} 1260 L{30+k*60} 1440 Z" fill="#b8a888" opacity="0.6"/>')
    b += ['<rect x="760" y="1250" width="380" height="190" fill="#e8dcc8"/>', '<ellipse cx="950" cy="1250" rx="190" ry="110" fill="#d8ccb8"/>',
          f'<rect x="0" y="1430" width="1080" height="490" fill="url(#{nombre}_h)"/>', '<path d="M0 1500 Q540 1470 1080 1500" stroke="#e8dcc8" stroke-width="40" fill="none"/>']
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def suelo_corte():
    """Corte del suelo: césped, arena y arcilla con agua."""
    w, h = 1080, 900
    d = lg("sc_a", (0, "#e8c88a"), (1, "#c8a060")) + lg("sc_b", (0, "#8a6a5a"), (1, "#5a4038"))
    r = random.Random(9)
    b = ['<rect x="0" y="0" width="1080" height="60" fill="#5aa83a"/>', '<rect x="0" y="60" width="1080" height="320" fill="url(#sc_a)"/>',
         '<path d="M0 380 Q270 340 540 390 T1080 370 L1080 900 L0 900 Z" fill="url(#sc_b)"/>']
    for _ in range(220):
        b.append(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(70,370):.0f}" r="{r.uniform(2,6):.1f}" fill="#a0784a" opacity="0.6"/>')
    for _ in range(30):
        y = r.uniform(430, 880)
        b.append(f'<path d="M{r.uniform(0,1000):.0f} {y:.0f} q40 -12 80 0" stroke="#3a2a24" stroke-width="5" fill="none" opacity="0.5"/>')
    for _ in range(14):
        b.append(f'<ellipse cx="{r.uniform(60,1020):.0f}" cy="{r.uniform(480,860):.0f}" rx="{r.uniform(20,50):.0f}" ry="10" fill="#4ac8e8" opacity="0.45"/>')
    guardar("suelo_corte", "".join(b), w, h, d)


def espadas():
    """Dos espadas medievales cruzadas sobre un escudo liso."""
    w, h = 800, 800
    d = lg("es_h", (0, "#ffffff"), (0.5, "#b8c0d0"), (1, "#6a7080"), x2=1, y2=0) + lg("es_e", (0, "#c0392b"), (1, "#7a1a12"))
    b = ['<g filter="url(#sombra)">', '<path d="M400 140 L620 220 Q620 520 400 680 Q180 520 180 220 Z" fill="url(#es_e)" stroke="#ffd27a" stroke-width="14"/>']
    for a in (-40, 40):
        b.append(f'<g transform="rotate({a} 400 420)"><rect x="380" y="20" width="40" height="560" fill="url(#es_h)"/><path d="M380 20 L400 -20 L420 20 Z" fill="#e8eef8"/>'
                 f'<rect x="300" y="580" width="200" height="30" rx="10" fill="#ffd27a"/><rect x="386" y="610" width="28" height="120" fill="#5a3a1a"/><circle cx="400" cy="745" r="24" fill="#ffd27a"/></g>')
    b.append('</g>')
    guardar("espadas", "".join(b), w, h, d)


def lingotes():
    """Pila de lingotes de plomo grises."""
    w, h = 800, 520
    d = lg("lg_c", (0, "#b8bcc8"), (0.5, "#7a7e8a"), (1, "#4a4e58"))
    b = ['<ellipse cx="400" cy="490" rx="360" ry="22" fill="#000" opacity="0.35" filter="url(#blur8)"/>']
    for fila, (n, y) in enumerate([(4, 380), (3, 280), (2, 180)]):
        x0 = 400 - n * 85
        for k in range(n):
            x = x0 + k * 170
            b.append(f'<path d="M{x+10} {y+90} L{x+30} {y} L{x+140} {y} L{x+160} {y+90} Z" fill="url(#lg_c)" stroke="#3a3d44" stroke-width="4"/>')
            b.append(f'<rect x="{x+40}" y="{y+8}" width="90" height="10" fill="#ffffff" opacity="0.4"/>')
            b.append(f'<text x="{x+85}" y="{y+70}" font-family="DejaVu Sans" font-weight="bold" font-size="40" text-anchor="middle" fill="#3a3d44">Pb</text>')
    guardar("lingotes", "".join(b), w, h, d)


def taladro():
    """Barrena de perforación inclinada (broca en espiral)."""
    w, h = 300, 1000
    d = lg("tl_c", (0, "#e8eef8"), (0.5, "#8a90a0"), (1, "#3a3d44"), x2=1, y2=0)
    b = ['<rect x="80" y="0" width="140" height="200" rx="20" fill="#ffb02e"/><rect x="80" y="60" width="140" height="20" fill="#3a3d44"/>',
         '<rect x="120" y="200" width="60" height="760" fill="url(#tl_c)"/>']
    for k in range(18):
        y = 220 + k * 42
        b.append(f'<path d="M110 {y} L190 {y+28}" stroke="#4a4e58" stroke-width="10" stroke-linecap="round"/>')
    b.append('<path d="M120 960 L150 1000 L180 960 Z" fill="#8a90a0"/>')
    guardar("taladro", "".join(b), w, h, d)


def bala_canon():
    w, h = 300, 300
    d = rg("bc_c", (0, "#8a8e98", 1), (0.6, "#3a3d44", 1), (1, "#0c0d10", 1), cx=0.35, cy=0.3)
    guardar("bala", '<circle cx="150" cy="150" r="120" fill="url(#bc_c)"/>', w, h, d)


def hoja(nombre, texto, color):
    """Hoja de calendario con el año (misma forma que la del lote 2026-11-18-tarde)."""
    w, h = 520, 600
    d = lg(f"{nombre}_p", (0, "#ffffff"), (1, "#ece6da"))
    tam = 150 if len(texto) <= 4 else 110
    b = ['<g filter="url(#sombra)">', f'<rect x="20" y="40" width="480" height="540" rx="22" fill="url(#{nombre}_p)"/>',
         f'<path d="M20 62 Q20 40 42 40 L478 40 Q500 40 500 62 L500 170 L20 170 Z" fill="{color}"/>',
         *[f'<circle cx="{80+i*90}" cy="40" r="14" fill="#3a3d44"/>' for i in range(5)],
         f'<text x="260" y="410" font-family="DejaVu Sans" font-weight="bold" font-size="{tam}" text-anchor="middle" fill="#2a2a2a">{texto}</text>', '</g>']
    guardar(nombre, "".join(b), w, h, d)


def generar(dirsvg):
    os.makedirs(dirsvg, exist_ok=True)
    _cargar("lotes/2026-11-18-manana/generadores/ilus_03.py", "i3").generar(dirsvg)
    _cargar("lotes/2026-11-18-manana/generadores/ilus_02.py", "i2").generar(dirsvg)
    _cargar("lotes/2026-11-18-tarde/generadores/ilus_tarde.py", "it").generar(dirsvg)
    ilus.OUT = dirsvg
    ilus.bg_espacio_rico("bg_galaxia", "ambar", 41) if hasattr(ilus, "bg_espacio_rico") else None
    filete(); soldador(); olor(); olor("olor_gris", "#c8c8d0"); olor("olor_rosa", "#ff7ab8"); oxigeno(); matraz(); perfume(); polvo_lunar(); guante()
    frambuesa(); radiotelescopio(); molecula_fruta()
    nota(); nota("nota_cian", "#2ff3ff"); nota("nota_lima", "#7dff3a"); nota("nota_ambar", "#ffb02e"); auriculares(); gusano(); chicle(); globo_chicle(); mandibula(); bg_aula()
    torre_pisa(); torre_pisa("torre_3", pisos=3); torre_pisa("torre_curva", curva=-14); bg_plaza(); bg_plaza("bg_plaza_tarde", True); suelo_corte(); espadas(); lingotes(); taladro(); bala_canon()
    hoja("hoja_1173", "1173", "#c0392b"); hoja("hoja_1990", "1990", "#2f7bff"); hoja("hoja_2001", "2001", "#27ae60"); hoja("hoja_2008", "2008", "#7a3ad8")
    hoja("hoja_2005", "2005", "#e05a2a"); hoja("hoja_2015", "2015", "#1a8ab0"); hoja("hoja_1372", "1372", "#8a5a2a")
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
