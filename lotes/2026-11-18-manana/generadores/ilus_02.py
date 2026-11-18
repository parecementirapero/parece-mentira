"""Ilustraciones del vídeo 02 del lote 2026-11-18-manana («Esta muralla no se ve»: la Gran Muralla desde el espacio).
Uso: python3 ilus_02.py DIR_SVG   (semillas fijas). Ladrillos de motor/biblioteca/ilus.py. Agente 08:00 (Nico)."""
import math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano, _neb, _mascara, _estrellas_ricas  # noqa: E402,F401


def _cresta(r, y0, amp, pasos=14, w=1080):
    """Línea de cresta de montaña (lista de puntos) con picos irregulares."""
    pts, x = [], -40
    paso = (w + 80) / pasos
    for i in range(pasos + 1):
        pts.append((x + i * paso + r.uniform(-0.2, 0.2) * paso, y0 - (r.uniform(0.55, 1.0) if i % 2 else r.uniform(0.0, 0.3)) * amp))
    return pts


def _poli_cresta(pts, fondo=1920):
    d = f"M{pts[0][0]:.0f} {fondo} " + " ".join(f"L{x:.0f} {y:.0f}" for x, y in pts) + f" L{pts[-1][0]:.0f} {fondo} Z"
    return d


def _camino(pts):
    d = f"M{pts[0][0]:.0f} {pts[0][1]:.0f}"
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        d += f" Q{x0:.0f} {y0:.0f} {(x0 + x1) / 2:.0f} {(y0 + y1) / 2:.0f}"
    d += f" T{pts[-1][0]:.0f} {pts[-1][1]:.0f}"
    return d


# Camino de la muralla por las crestas (de abajo a la izquierda hasta el fondo a la derecha)
CAMINO = [(-60, 1560), (160, 1430), (330, 1470), (470, 1300), (600, 1250), (720, 1120), (640, 1000), (760, 900),
          (880, 860), (980, 760), (1140, 720)]


def bg_montanas(nombre="bg_montanas", cielo=("#f6c48a", "#e88a5a", "#4a3a6a"), sem=3):
    """Montañas por capas con bruma (amanecer cálido). La muralla va en una capa aparte."""
    r = random.Random(sem)
    d = lg(f"{nombre}_c", (0, cielo[2]), (0.45, cielo[1]), (0.75, cielo[0]), (1, "#fff0d0"))
    tonos = ["#8a6a8a", "#6a5a7a", "#4f4a62", "#3a3a4a", "#262a30"]
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>',
         '<circle cx="760" cy="560" r="120" fill="#fff3d0" opacity="0.9"/>',
         '<circle cx="760" cy="560" r="260" fill="#ffd8a0" opacity="0.35" filter="url(#blur40)"/>']
    for k, t in enumerate(tonos):
        y0 = 720 + k * 210
        pts = _cresta(r, y0, 260 - k * 25, 7 + k * 2)
        b.append(f'<path d="{_poli_cresta(pts)}" fill="{t}"/>')
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):  # cara en sombra de cada pico
            if yb > ya: b.append(f'<path d="M{xa:.0f} {ya:.0f} L{xb:.0f} {yb:.0f} L{xa + (xb - xa) * 0.3:.0f} {yb + 260:.0f} Z" fill="#000" opacity="0.12"/>')
        # luz de borde en la cresta y bruma entre capas
        b.append(f'<path d="{_camino(pts)}" stroke="#ffd8a8" stroke-width="3" fill="none" opacity="{0.35 - k * 0.05:.2f}"/>')
        b.append(f'<rect x="0" y="{y0 + 30}" width="1080" height="120" fill="#ffe6c8" opacity="{0.22 - k * 0.03:.2f}" filter="url(#blur40)"/>')
        for _ in range(18 + k * 6):  # árboles / matorrales oscuros
            x = r.uniform(0, 1080); yy = y0 + r.uniform(60, 240)
            b.append(f'<ellipse cx="{x:.0f}" cy="{yy:.0f}" rx="{r.uniform(8, 20) + k * 3:.0f}" ry="{r.uniform(6, 14) + k * 2:.0f}" fill="#1a2018" opacity="{0.25 + k * 0.1:.2f}"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def muralla(nombre="muralla", color="#c8a070", sombra="#6a4a30", luz="#ffe0b0", grosor=34):
    """La muralla serpenteando por las crestas, con almenas y torres de vigilancia (capa transparente 1080×1920)."""
    pts = CAMINO
    cam = _camino(pts)
    b = [f'<path d="{cam}" stroke="#000" stroke-width="{grosor + 26}" fill="none" opacity="0.35" filter="url(#blur8)" transform="translate(10 18)"/>',
         f'<path d="{cam}" stroke="{sombra}" stroke-width="{grosor + 10}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
         f'<path d="{cam}" stroke="{color}" stroke-width="{grosor}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
         f'<path d="{cam}" stroke="{luz}" stroke-width="6" fill="none" opacity="0.7" transform="translate(-3 -10)"/>',
         f'<path d="{cam}" stroke="{sombra}" stroke-width="{grosor * 0.5:.0f}" fill="none" stroke-dasharray="7 9" transform="translate(0 -{grosor * 0.55:.0f})"/>',
         f'<path d="{cam}" stroke="{color}" stroke-width="{grosor * 0.36:.0f}" fill="none" stroke-dasharray="7 9" transform="translate(0 -{grosor * 0.62:.0f})"/>']
    # torres en algunos puntos del camino (más grandes en primer plano)
    for i, (x, y) in enumerate(pts[1:-1]):
        s = 1.6 - i * 0.12
        tw, th = 56 * s, 70 * s
        b.append(f'<g transform="translate({x:.0f} {y - th * 0.55:.0f})">'
                 f'<rect x="{-tw / 2:.0f}" y="{-th / 2:.0f}" width="{tw:.0f}" height="{th:.0f}" fill="{color}" stroke="{sombra}" stroke-width="3"/>'
                 f'<rect x="{-tw / 2:.0f}" y="{-th / 2:.0f}" width="{tw * 0.3:.0f}" height="{th:.0f}" fill="{sombra}" opacity="0.45"/>'
                 f'<rect x="{-tw * 0.12:.0f}" y="{-th * 0.12:.0f}" width="{tw * 0.24:.0f}" height="{th * 0.3:.0f}" rx="{tw * 0.1:.0f}" fill="#2a1a10"/>'
                 + "".join(f'<rect x="{-tw / 2 + j * tw / 4:.0f}" y="{-th / 2 - 10 * s:.0f}" width="{tw / 8:.0f}" height="{10 * s:.0f}" fill="{color}" stroke="{sombra}" stroke-width="2"/>' for j in range(4))
                 + f'<rect x="{-tw / 2:.0f}" y="{-th / 2:.0f}" width="{tw:.0f}" height="4" fill="{luz}" opacity="0.6"/></g>')
    guardar(nombre, "".join(b))


def torre_detalle():
    """Primer plano de una torre de vigilancia de piedra, con ladrillos y almenas."""
    w, h = 900, 1100
    r = random.Random(12)
    d = lg("td_p", (0, "#e0b880"), (1, "#9a7048"), x2=1, y2=0)
    b = ['<ellipse cx="450" cy="1060" rx="420" ry="30" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         '<rect x="140" y="260" width="620" height="800" fill="url(#td_p)"/>',
         '<rect x="140" y="260" width="200" height="800" fill="#5a3a20" opacity="0.35"/>']
    for fila in range(26):  # ladrillos
        y = 270 + fila * 30
        off = 0 if fila % 2 else 40
        for c in range(9):
            x = 140 + off + c * 80
            if x + 76 > 762: continue
            b.append(f'<rect x="{x:.0f}" y="{y}" width="76" height="26" fill="none" stroke="#6a4a2a" stroke-width="2" opacity="{r.uniform(0.3, 0.7):.2f}"/>')
    b += [*[f'<rect x="{140 + j * 135}" y="190" width="80" height="80" fill="#c8a070" stroke="#6a4a2a" stroke-width="3"/>' for j in range(5)],
          '<path d="M390 1060 L390 820 Q450 760 510 820 L510 1060 Z" fill="#1e140c"/>',
          '<rect x="260" y="480" width="70" height="110" rx="35" fill="#1e140c"/><rect x="570" y="480" width="70" height="110" rx="35" fill="#1e140c"/>',
          '<rect x="140" y="262" width="620" height="8" fill="#ffe8c0" opacity="0.7"/>',
          '<rect width="900" height="1100" fill="#888" filter="url(#grano)" opacity="0.5"/>']
    guardar("torre", "".join(b), w, h, d)


def carta_1754():
    """Carta antigua con renglones de tinta, una Luna dibujada a pluma y lacre (sin texto legible)."""
    w, h = 820, 1040
    r = random.Random(17)
    d = rg("c54_p", (0, "#f6e6c0", 1), (0.7, "#e6cc98", 1), (1, "#b8945a", 1))
    b = ['<rect x="30" y="40" width="760" height="980" fill="#000" opacity="0.35" filter="url(#blur8)" transform="translate(12 14)"/>',
         '<path d="M30 40 L790 52 L782 1020 L38 1008 Z" fill="url(#c54_p)"/>',
         '<path d="M30 40 L790 52 L782 1020 L38 1008 Z" fill="#7a5a2a" filter="url(#papel)" opacity="0.6"/>']
    for k in range(14):  # renglones manuscritos (garabatos)
        y = 130 + k * 44
        x0, x1 = 90, 720 - (r.uniform(0, 260) if k % 5 == 4 else r.uniform(0, 60))
        pts = []
        x = x0
        while x < x1:
            pts.append(f"{x:.0f},{y + r.uniform(-7, 7):.0f}")
            x += r.uniform(9, 16)
        b.append(f'<polyline points="{" ".join(pts)}" stroke="#2a1a10" stroke-width="3.2" fill="none" stroke-linejoin="round" opacity="0.8"/>')
    # Luna a pluma y una línea de puntos hacia ella
    b += ['<circle cx="560" cy="830" r="95" fill="none" stroke="#2a1a10" stroke-width="5"/>',
          '<path d="M520 790 a18 18 0 1 0 1 0 M600 860 a12 12 0 1 0 1 0 M560 880 a9 9 0 1 0 1 0" stroke="#2a1a10" stroke-width="3" fill="none"/>',
          '<path d="M150 920 Q300 760 460 820" stroke="#2a1a10" stroke-width="3" fill="none" stroke-dasharray="8 10"/>',
          '<circle cx="180" cy="960" r="44" fill="#9a1a1a"/><circle cx="180" cy="960" r="30" fill="none" stroke="#5a0a0a" stroke-width="4"/>',
          '<path d="M600 140 l130 0" stroke="#2a1a10" stroke-width="4"/>']
    guardar("carta_1754", "".join(b), w, h, d)


def pluma():
    w, h = 300, 900
    d = lg("pl_g", (0, "#ffffff"), (1, "#c8c0b0"), x2=1, y2=0)
    b = ['<path d="M150 60 C260 200 250 520 160 760 C70 520 40 200 150 60 Z" fill="url(#pl_g)"/>',
         *[f'<path d="M152 {120 + k * 34} L{240 - k * 3} {80 + k * 34}" stroke="#a8a090" stroke-width="2"/>' for k in range(18)],
         *[f'<path d="M150 {120 + k * 34} L{60 + k * 3} {80 + k * 34}" stroke="#a8a090" stroke-width="2"/>' for k in range(18)],
         '<path d="M152 70 L156 860" stroke="#8a8070" stroke-width="5"/>',
         '<path d="M150 820 L160 900 L166 820 Z" fill="#1a1010"/>']
    guardar("pluma", "".join(b), w, h, d)


def muralla_cenital():
    """Tramo de muralla visto desde arriba (para comparar el ancho con una carretera)."""
    w, h = 1400, 360
    r = random.Random(5)
    d = lg("mc_g", (0, "#d8b07a"), (1, "#a07a4a"))
    b = ['<rect x="0" y="80" width="1400" height="200" fill="#000" opacity="0.35" filter="url(#blur8)" transform="translate(0 16)"/>',
         '<rect x="0" y="90" width="1400" height="180" fill="url(#mc_g)"/>',
         '<rect x="0" y="90" width="1400" height="26" fill="#7a5a34"/><rect x="0" y="244" width="1400" height="26" fill="#7a5a34"/>',
         *[f'<rect x="{x}" y="72" width="34" height="26" fill="#c89a62" stroke="#6a4a2a" stroke-width="2"/>' for x in range(0, 1400, 62)],
         *[f'<rect x="{x}" y="262" width="34" height="26" fill="#c89a62" stroke="#6a4a2a" stroke-width="2"/>' for x in range(30, 1400, 62)]]
    for _ in range(140):  # losas del paseo
        x, y = r.uniform(0, 1400), r.uniform(120, 240)
        b.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{r.uniform(30, 60):.0f}" height="{r.uniform(16, 26):.0f}" fill="none" stroke="#8a6a40" stroke-width="2" opacity="0.5"/>')
    guardar("muralla_cenital", "".join(b), w, h, d)


def carretera():
    w, h = 1400, 360
    b = ['<rect x="0" y="90" width="1400" height="180" fill="#3a3c42"/>',
         '<rect x="0" y="96" width="1400" height="8" fill="#e8e8e8"/><rect x="0" y="256" width="1400" height="8" fill="#e8e8e8"/>',
         *[f'<rect x="{x}" y="174" width="70" height="10" fill="#ffd23f"/>' for x in range(20, 1400, 140)],
         '<rect width="1400" height="360" fill="#888" filter="url(#grano)" opacity="0.4"/>']
    guardar("carretera", "".join(b), w, h)


def coche():
    """Coche visto desde arriba."""
    w, h = 300, 160
    d = lg("co_g", (0, "#ff5a4a"), (1, "#b8241a"))
    b = ['<rect x="16" y="22" width="270" height="124" rx="40" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<rect x="10" y="14" width="270" height="124" rx="40" fill="url(#co_g)"/>',
         '<rect x="150" y="30" width="80" height="92" rx="16" fill="#1e2a3a"/>', '<rect x="60" y="34" width="60" height="84" rx="14" fill="#2a3a4e"/>',
         '<rect x="160" y="36" width="20" height="80" fill="#5a7aa0" opacity="0.5"/>',
         '<rect x="262" y="26" width="16" height="22" rx="5" fill="#fff6c0"/><rect x="262" y="104" width="16" height="22" rx="5" fill="#fff6c0"/>']
    guardar("coche", "".join(b), w, h, d)


def bg_terreno(nombre="bg_terreno", base="#b08a5a", sem=8):
    """Suelo ocre visto desde muy alto: manchas, arrugas del relieve, ríos secos. La muralla se pierde en él."""
    r = random.Random(sem)
    d = _neb(f"{nombre}_n", "#6a4a2a", sem, freq=0.004, contraste=2.0, corte=1.0)
    b = [f'<rect width="1080" height="1920" fill="{base}"/>', f'<rect width="1080" height="1920" filter="url(#{nombre}_n)" opacity="0.6"/>']
    for _ in range(60):  # arrugas del relieve
        x, y = r.uniform(0, 1080), r.uniform(0, 1920)
        L = r.uniform(80, 260); a = r.uniform(0, math.pi)
        b.append(f'<path d="M{x:.0f} {y:.0f} q{L * math.cos(a) / 2:.0f} {L * math.sin(a) / 2 + r.uniform(-30, 30):.0f} {L * math.cos(a):.0f} {L * math.sin(a):.0f}" '
                 f'stroke="#5a3c22" stroke-width="{r.uniform(2, 6):.1f}" fill="none" opacity="0.35"/>')
    for _ in range(40):
        b.append(f'<ellipse cx="{r.uniform(0, 1080):.0f}" cy="{r.uniform(0, 1920):.0f}" rx="{r.uniform(20, 80):.0f}" ry="{r.uniform(10, 40):.0f}" fill="#4a6a3a" opacity="0.25"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def franja(nombre="franja", color="#a8845a", grosor=6):
    """La muralla vista desde muy arriba: una línea finísima del mismo color que el suelo."""
    pts = [(-40, 1700), (200, 1480), (360, 1520), (520, 1260), (700, 1180), (640, 900), (820, 760), (960, 500), (1120, 380)]
    b = [f'<path d="{_camino(pts)}" stroke="#6a4a2a" stroke-width="{grosor + 3}" fill="none" opacity="0.6"/>',
         f'<path d="{_camino(pts)}" stroke="{color}" stroke-width="{grosor}" fill="none"/>']
    guardar(nombre, "".join(b))


def iss():
    """Estación espacial genérica: viga central, módulos y alas de paneles solares (sin banderas ni logotipos)."""
    w, h = 1200, 700
    d = lg("is_p", (0, "#2a4a8a"), (0.5, "#4a7ad0"), (1, "#1a2a5a"), x2=1, y2=1) + lg("is_m", (0, "#f0f0f0"), (1, "#9aa0a8"))
    b = ['<rect x="80" y="335" width="1040" height="22" fill="#b8bcc4"/>',
         *[f'<path d="M{80 + k * 40} 335 l20 22 l20 -22" stroke="#7a808a" stroke-width="3" fill="none"/>' for k in range(26)]]
    for cx in (170, 330, 870, 1030):  # alas de paneles
        for sgn in (-1, 1):
            y = 346 + sgn * 170
            b.append(f'<rect x="{cx - 60}" y="{y - 140 if sgn < 0 else y - 30:.0f}" width="120" height="170" fill="url(#is_p)" stroke="#c8d0e0" stroke-width="3"/>')
            b += [f'<path d="M{cx - 60} {(y - 140 if sgn < 0 else y - 30) + k * 21:.0f} h120" stroke="#9ab8f0" stroke-width="1.5" opacity="0.6"/>' for k in range(1, 8)]
    b += ['<rect x="480" y="300" width="240" height="92" rx="40" fill="url(#is_m)" stroke="#6a707a" stroke-width="3"/>',
          '<rect x="560" y="250" width="80" height="190" rx="30" fill="url(#is_m)" stroke="#6a707a" stroke-width="3"/>',
          '<rect x="420" y="320" width="70" height="52" rx="20" fill="url(#is_m)" stroke="#6a707a" stroke-width="3"/>',
          '<rect x="710" y="320" width="90" height="52" rx="20" fill="url(#is_m)" stroke="#6a707a" stroke-width="3"/>',
          '<rect x="520" y="306" width="180" height="10" fill="#ffffff" opacity="0.7"/>',
          '<rect x="640" y="160" width="40" height="110" fill="#e8e0d0" stroke="#8a8070" stroke-width="2"/>']
    guardar("iss", "".join(b), w, h, d)


def bg_orbita(nombre="bg_orbita"):
    """La Tierra vista desde la órbita baja: horizonte curvo, atmósfera azul, nubes y tierra parda abajo."""
    r = random.Random(23)
    d = (lg(f"{nombre}_t", (0, "#6a8a5a"), (0.5, "#a8865a"), (1, "#7a5a3a")) + rg(f"{nombre}_a", (0, "#7ad0ff", 0.0), (0.93, "#7ad0ff", 0.0), (0.965, "#9ae0ff", 0.9), (1, "#1a3a8a", 0), cx=0.5, cy=1.4, r=1.0)
         + _neb(f"{nombre}_n", "#ffffff", 4, freq=0.006, contraste=2.6, corte=1.1))
    b = ['<rect width="1080" height="1920" fill="#02030a"/>', _estrellas_ricas(31, n_peq=200, n_med=20, n_bri=4),
         '<circle cx="540" cy="3400" r="2800" fill="url(#bg_orbita_t)"/>',
         f'<circle cx="540" cy="3400" r="2800" filter="url(#{nombre}_n)" opacity="0.55"/>',
         '<circle cx="540" cy="3400" r="2830" fill="none" stroke="#7ad0ff" stroke-width="40" opacity="0.5" filter="url(#blur20)"/>',
         '<circle cx="540" cy="3400" r="2806" fill="none" stroke="#c8f0ff" stroke-width="8" opacity="0.8"/>']
    for _ in range(30):
        b.append(f'<ellipse cx="{r.uniform(0, 1080):.0f}" cy="{r.uniform(700, 1920):.0f}" rx="{r.uniform(40, 160):.0f}" ry="{r.uniform(14, 40):.0f}" fill="#ffffff" opacity="0.35" filter="url(#blur8)"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def capsula():
    """Cápsula tripulada genérica (módulo de descenso en campana, módulo orbital y paneles), sin insignias."""
    w, h = 900, 500
    d = lg("ca_m", (0, "#f2f2ee"), (1, "#8a8e96")) + lg("ca_p", (0, "#1a2a6a"), (1, "#3a6ac8"), x2=1, y2=0)
    b = ['<rect x="20" y="200" width="250" height="100" fill="url(#ca_p)" stroke="#c8d0e0" stroke-width="3"/>',
         '<rect x="630" y="200" width="250" height="100" fill="url(#ca_p)" stroke="#c8d0e0" stroke-width="3"/>',
         *[f'<path d="M{20 + k * 31} 200 v100" stroke="#9ab8f0" stroke-width="1.5" opacity="0.6"/>' for k in range(1, 8)],
         *[f'<path d="M{630 + k * 31} 200 v100" stroke="#9ab8f0" stroke-width="1.5" opacity="0.6"/>' for k in range(1, 8)],
         '<rect x="270" y="236" width="360" height="28" fill="#8a8e96"/>',
         '<path d="M300 170 L470 170 L520 250 L470 330 L300 330 Z" fill="url(#ca_m)" stroke="#5a5e66" stroke-width="3"/>',
         '<ellipse cx="560" cy="250" rx="80" ry="70" fill="url(#ca_m)" stroke="#5a5e66" stroke-width="3"/>',
         '<path d="M330 186 L460 186" stroke="#ffffff" stroke-width="6" opacity="0.7"/>',
         '<circle cx="380" cy="250" r="18" fill="#1a2a3a" stroke="#c8d0e0" stroke-width="3"/>',
         '<path d="M240 250 L190 250" stroke="#ff9a3a" stroke-width="10" opacity="0.0"/>']
    guardar("capsula", "".join(b), w, h, d)


def casco():
    """Casco de astronauta de frente con el visor dorado reflejando la Tierra (sin cara visible)."""
    w, h = 900, 1000
    d = (rg("cs_v", (0, "#ffd88a", 1), (0.6, "#c8902a", 1), (1, "#5a3a10", 1), cx=0.4, cy=0.35) + lg("cs_c", (0, "#ffffff"), (1, "#a8acb4"))
         + rg("cs_t", (0, "#7ad0ff", 1), (0.6, "#2a6ac8", 1), (1, "#0a2a5a", 1), cx=0.4, cy=0.4))
    b = ['<ellipse cx="450" cy="940" rx="380" ry="40" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         '<path d="M120 820 C120 900 780 900 780 820 L760 700 L140 700 Z" fill="url(#cs_c)" stroke="#6a6e76" stroke-width="4"/>',
         '<circle cx="450" cy="470" r="380" fill="url(#cs_c)" stroke="#6a6e76" stroke-width="5"/>',
         '<path d="M190 440 C190 250 710 250 710 440 C710 640 600 720 450 720 C300 720 190 640 190 440 Z" fill="url(#cs_v)" stroke="#3a2a10" stroke-width="8"/>',
         # reflejo de la Tierra en el visor
         '<clipPath id="cs_clip"><path d="M190 440 C190 250 710 250 710 440 C710 640 600 720 450 720 C300 720 190 640 190 440 Z"/></clipPath>',
         '<g clip-path="url(#cs_clip)" opacity="0.8"><circle cx="520" cy="560" r="170" fill="url(#cs_t)"/>'
         '<path d="M440 470 q40 -20 80 10 q30 40 -10 70 q-50 10 -70 -30 Z" fill="#c8a060" opacity="0.8"/>'
         '<path d="M380 560 q120 -30 260 10" stroke="#ffffff" stroke-width="10" opacity="0.6" fill="none"/></g>',
         '<path d="M250 360 C300 300 400 280 470 290" stroke="#ffffff" stroke-width="22" stroke-linecap="round" opacity="0.55" fill="none"/>',
         '<rect x="130" y="420" width="50" height="120" rx="20" fill="#8a8e96"/><rect x="720" y="420" width="50" height="120" rx="20" fill="#8a8e96"/>']
    guardar("casco", "".join(b), w, h, d)


def camara_tele():
    """Cámara de fotos con un teleobjetivo muy largo."""
    w, h = 1200, 520
    d = lg("ct_b", (0, "#3a3e46"), (1, "#14161a")) + lg("ct_l", (0, "#e8e8e8"), (0.5, "#c8c8c8"), (1, "#8a8a8a"))
    b = ['<ellipse cx="600" cy="480" rx="520" ry="26" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<rect x="60" y="150" width="300" height="230" rx="30" fill="url(#ct_b)"/>', '<rect x="120" y="100" width="140" height="70" rx="14" fill="url(#ct_b)"/>',
         '<rect x="340" y="190" width="620" height="160" rx="20" fill="url(#ct_l)" stroke="#6a6a6a" stroke-width="3"/>',
         '<rect x="560" y="186" width="40" height="168" fill="#c0261a"/>',
         '<rect x="940" y="170" width="200" height="200" rx="24" fill="url(#ct_l)" stroke="#6a6a6a" stroke-width="3"/>',
         '<ellipse cx="1140" cy="270" rx="26" ry="96" fill="#1a2a4a"/><ellipse cx="1136" cy="250" rx="10" ry="40" fill="#7ad0ff" opacity="0.6"/>',
         '<rect x="380" y="200" width="560" height="12" fill="#ffffff" opacity="0.6"/>']
    guardar("camara_tele", "".join(b), w, h, d)


def bg_noche_ciudades(nombre="bg_noche"):
    """La Tierra de noche desde la órbita: horizonte curvo y manchas de luz de ciudades unidas por carreteras."""
    r = random.Random(44)
    d = rg(f"{nombre}_t", (0, "#0a1020", 1), (1, "#04060c", 1), cx=0.5, cy=0.2)
    b = ['<rect width="1080" height="1920" fill="#01020a"/>', _estrellas_ricas(41, n_peq=240, n_med=20, n_bri=4),
         '<circle cx="540" cy="3300" r="2700" fill="url(#bg_noche_t)"/>',
         '<circle cx="540" cy="3300" r="2712" fill="none" stroke="#3a8aff" stroke-width="14" opacity="0.6" filter="url(#blur8)"/>']
    ciudades = [(r.uniform(60, 1020), r.uniform(800, 1880), r.uniform(0.5, 1.6)) for _ in range(26)]
    for (x0, y0, _), (x1, y1, _) in zip(ciudades, ciudades[1:]):
        if abs(x0 - x1) + abs(y0 - y1) < 600:
            b.append(f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#ffb84a" stroke-width="2" opacity="0.5"/>')
    for x, y, s in ciudades:
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{60 * s:.0f}" fill="#ffb84a" opacity="0.25" filter="url(#blur20)"/>')
        for _ in range(int(14 * s)):
            b.append(f'<circle cx="{x + r.gauss(0, 22 * s):.0f}" cy="{y + r.gauss(0, 16 * s):.0f}" r="{r.uniform(1.5, 4):.1f}" fill="#ffe8a8"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def ojo_simple():
    """Ojo humano estilizado (sin cara) para «a simple vista»."""
    w, h = 900, 500
    d = rg("os_i", (0, "#0a0a0a", 1), (0.38, "#0a0a0a", 1), (0.42, "#6a4a2a", 1), (0.95, "#2a1a0a", 1), (1, "#0a0a0a", 1))
    b = ['<path d="M40 250 C220 40 680 40 860 250 C680 460 220 460 40 250 Z" fill="#f4ece6" stroke="#6a3a2a" stroke-width="10"/>',
         '<circle cx="450" cy="250" r="150" fill="url(#os_i)"/>', '<circle cx="400" cy="200" r="34" fill="#ffffff" opacity="0.9"/>',
         '<path d="M40 250 C220 40 680 40 860 250" stroke="#2a1410" stroke-width="18" fill="none"/>']
    guardar("ojo_simple", "".join(b), w, h, d)


def descenso():
    """Paracaídas con gajos y módulo de descenso en campana (chamuscado por la reentrada), sin insignias."""
    w, h = 800, 1100
    d = lg("de_m", (0, "#d8d0c0"), (0.6, "#8a7a6a"), (1, "#3a3028"), x2=1, y2=0)
    b = ['<path d="M60 360 C60 60 740 60 740 360 Z" fill="#ff7a2a"/>']
    for k in range(6):  # gajos alternos
        x0 = 60 + k * 680 / 6
        if k % 2: b.append(f'<path d="M{x0:.0f} 360 Q{x0 + 56:.0f} 60 400 70 Q{x0 + 70:.0f} 120 {x0 + 113:.0f} 360 Z" fill="#ffffff" opacity="0.9"/>')
    b += ['<path d="M60 360 C60 60 740 60 740 360" stroke="#c84a10" stroke-width="6" fill="none"/>',
          '<path d="M60 360 Q230 330 400 360 Q570 330 740 360" stroke="#c84a10" stroke-width="5" fill="#000" fill-opacity="0.08"/>',
          *[f'<path d="M{60 + k * 680 / 6:.0f} 360 L400 820" stroke="#f4f0e8" stroke-width="3"/>' for k in range(7)],
          '<path d="M300 840 L500 840 L560 1040 L240 1040 Z" fill="url(#de_m)" stroke="#2a2018" stroke-width="4"/>',
          '<ellipse cx="400" cy="840" rx="100" ry="20" fill="#e8e0d0"/>',
          '<path d="M250 1010 L550 1010 L560 1040 L240 1040 Z" fill="#2a1a10" opacity="0.8"/>',
          '<circle cx="360" cy="930" r="20" fill="#1a2a3a" stroke="#c8d0e0" stroke-width="3"/>']
    guardar("descenso", "".join(b), w, h, d)


def generar(dirsvg):
    ilus.generar(dirsvg)
    ilus.OUT = dirsvg
    bg_montanas(); bg_montanas("bg_montanas_dia", ("#cfe6ff", "#8ab8e8", "#4a7ab8"), 9)
    muralla(); muralla("muralla_dia", "#d8b888", "#7a5a3a", "#fff4d8")
    torre_detalle(); carta_1754(); pluma(); muralla_cenital(); carretera(); coche()
    bg_terreno(); franja(); franja("franja_marcada", "#ffd23f", 10)
    iss(); bg_orbita(); capsula(); casco(); camara_tele(); bg_noche_ciudades(); ojo_simple(); descenso()
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
