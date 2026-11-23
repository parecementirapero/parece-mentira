"""Ilustraciones del lote 2026-11-22-tarde (Jorge, con el agente): 01 el punto ciego, 02 el cerebro enamorado, 03 test de atención (el astronauta).
Uso: python3 ilus_1122t.py DIR_SVG. Reutiliza el lote 2026-11-22-manana entero (ojo en corte, cerebro, cara, gimnasio, jugadores…) y el escáner del 17-11.
Todo dibujado aquí: sin logos, marcas ni personas reales reconocibles. El test del 03 es una escena propia (no copia ningún vídeo)."""
import importlib.util, math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano, _estrellas_ricas  # noqa: E402


def _mod(rel, nombre):
    s = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, rel))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


# ====================================================================== 01 · PUNTO CIEGO
def tarjeta_test(nombre="tarjeta_test"):
    """La prueba del punto ciego: fondo claro, cruz a la izquierda y punto negro a la derecha, a la misma altura."""
    b = ['<rect width="1080" height="1920" fill="#f4f1ea"/>',
         '<path d="M180 960 H300 M240 900 V1020" stroke="#141414" stroke-width="22" stroke-linecap="round"/>',
         '<circle cx="880" cy="960" r="52" fill="#141414"/>']
    guardar(nombre, "".join(b))


def mancha_negra(nombre="mancha_negra"):
    w = h = 600
    d = rg("mn_g", (0, "#000000", 1), (0.6, "#000000", 0.95), (1, "#000000", 0))
    guardar(nombre, '<circle cx="300" cy="300" r="290" fill="url(#mn_g)"/>', w, h, d)


def celula(nombre="celula_luz", col="#7df9ff"):
    """Célula de la retina que detecta la luz (bastón estilizado con brillo en la punta)."""
    w, h = 220, 620
    d = lg(f"{nombre}_g", (0, col), (1, "#2a3a6a"))
    b = [f'<rect x="80" y="40" width="60" height="320" rx="30" fill="url(#{nombre}_g)"/>', '<ellipse cx="110" cy="420" rx="56" ry="70" fill="#c8a0d8"/>',
         '<circle cx="110" cy="420" r="22" fill="#6a3a8a"/>', '<path d="M110 490 L110 600" stroke="#c8a0d8" stroke-width="16" stroke-linecap="round"/>',
         f'<circle cx="110" cy="60" r="60" fill="{col}" opacity="0.35" filter="url(#blur20)"/>']
    guardar(nombre, "".join(b), w, h, d)


def retina_fila(nombre="retina_fila"):
    """Fila de células de la retina con un hueco en medio por donde salen los cables del nervio."""
    w, h = 1080, 700
    b = ['<rect width="1080" height="700" fill="#2a0a1a"/>', '<rect y="0" width="1080" height="120" fill="#6a1a2a"/>']
    for k in range(18):
        x = 30 + k * 60
        if 420 < x < 660:
            continue
        b.append(f'<rect x="{x}" y="160" width="34" height="260" rx="17" fill="#7df9ff"/><ellipse cx="{x + 17}" cy="460" rx="26" ry="32" fill="#c8a0d8"/>')
    for k in range(9):  # fibras que convergen al hueco y bajan
        x0 = 60 + k * 120
        b.append(f'<path d="M{x0} 520 Q{(x0 + 540) / 2:.0f} 560 540 600 L540 700" stroke="#f4d8a8" stroke-width="10" fill="none" opacity="0.8"/>')
    b.append('<rect x="470" y="140" width="140" height="460" rx="40" fill="#f4d8a8" opacity="0.25"/>')
    guardar(nombre, "".join(b), w, h)


def bg_corte(nombre="bg_corte"):
    """Gran salón de palacio del siglo XVII genérico: espejos, lámparas de araña, suelo de damero."""
    r = random.Random(5)
    d = lg(f"{nombre}_p", (0, "#5a3a1a"), (1, "#2a1a0a")) + lg(f"{nombre}_o", (0, "#ffe8a0"), (1, "#c8902a"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_p)"/>']
    for k in range(4):  # arcos con espejos
        x = 40 + k * 260
        b.append(f'<path d="M{x} 1250 V560 Q{x + 100} 420 {x + 200} 560 V1250 Z" fill="#8ab0c8" opacity="0.55" stroke="url(#{nombre}_o)" stroke-width="12"/>')
        b.append(f'<path d="M{x + 30} 1200 V600 Q{x + 60} 520 {x + 100} 500" stroke="#ffffff" stroke-width="10" opacity="0.35" fill="none"/>')
    for x in (270, 810):  # lámparas
        b.append(f'<path d="M{x} 0 V220" stroke="#c8902a" stroke-width="6"/><ellipse cx="{x}" cy="260" rx="120" ry="40" fill="url(#{nombre}_o)"/>')
        b += [f'<circle cx="{x + dx}" cy="230" r="10" fill="#fff6c8"/>' for dx in (-100, -50, 0, 50, 100)]
        b.append(f'<circle cx="{x}" cy="240" r="200" fill="#ffe8a0" opacity="0.25" filter="url(#blur40)"/>')
    b.append('<rect y="1250" width="1080" height="670" fill="#e8dcc0"/>')
    for i in range(12):
        for j in range(8):
            if (i + j) % 2:
                b.append(f'<path d="M{i * 100 - 60 + j * 30} {1250 + j * 84} l100 0 l30 84 l-100 0 Z" fill="#3a2a1a" opacity="0.8"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def noble(nombre="noble", col="#6a2a5a", luz="#ffd88a"):
    """Silueta de noble del siglo XVII (peluca larga, casaca, encajes), sin cara reconocible."""
    w, h = 420, 900
    b = ['<ellipse cx="210" cy="880" rx="140" ry="16" fill="#000" opacity="0.3" filter="url(#blur8)"/>',
         '<path d="M160 620 L150 870 L195 870 L210 660 L225 870 L270 870 L260 620 Z" fill="#2a1a2a"/>',
         f'<path d="M110 280 Q210 240 310 280 L340 640 Q210 680 80 640 Z" fill="{col}"/>',
         '<path d="M170 300 L210 360 L250 300 Z" fill="#f4f0e8"/>',
         '<circle cx="210" cy="190" r="70" fill="#e8c8a8"/>',
         '<path d="M130 170 Q120 80 210 80 Q300 80 290 170 L310 330 Q280 300 270 220 L150 220 Q140 300 110 330 Z" fill="#3a2a1a"/>',
         f'<path d="M110 280 Q100 400 120 520" stroke="{luz}" stroke-width="6" fill="none" opacity="0.7"/>']
    guardar(nombre, "".join(b), w, h)


def moneda(nombre="moneda_antigua"):
    w = h = 520
    d = rg("mo_g", (0, "#fff0a0", 1), (0.6, "#e8b830", 1), (1, "#8a6010", 1), cx=0.35, cy=0.35)
    b = ['<circle cx="260" cy="260" r="240" fill="url(#mo_g)" stroke="#6a4a08" stroke-width="10"/>',
         '<circle cx="260" cy="260" r="200" fill="none" stroke="#8a6010" stroke-width="6" stroke-dasharray="8 10"/>',
         '<path d="M200 330 Q180 220 260 170 Q340 220 320 330 Z" fill="#c8902a" opacity="0.8"/>',
         '<path d="M170 150 Q230 100 300 120" stroke="#ffffff" stroke-width="14" opacity="0.5" fill="none" stroke-linecap="round"/>']
    guardar(nombre, "".join(b), w, h, d)


def mano_tapa(nombre="mano_tapa"):
    """Mano abierta de perfil (para taparse un ojo)."""
    w, h = 500, 700
    c = "#e8b890"
    b = [f'<rect x="140" y="320" width="220" height="380" rx="80" fill="{c}"/>']
    for k, (x, l) in enumerate([(150, 260), (205, 300), (260, 310), (315, 270)]):
        b.append(f'<rect x="{x}" y="{360 - l}" width="50" height="{l}" rx="25" fill="{c}"/>')
    b.append(f'<rect x="20" y="420" width="190" height="56" rx="28" fill="{c}" transform="rotate(-35 200 450)"/>')
    b.append('<path d="M170 380 V200 M225 380 V160" stroke="#c8906a" stroke-width="4" opacity="0.6"/>')
    guardar(nombre, "".join(b), w, h)


# ====================================================================== 02 · AMOR
def corazon(nombre="corazon", c1="#ff4a6a", c2="#a0102a"):
    w, h = 700, 640
    d = rg(f"{nombre}_g", (0, c1, 1), (0.7, c2, 1), (1, "#4a0612", 1), cx=0.35, cy=0.3)
    b = [f'<path d="M350 600 C120 440 20 320 40 190 C60 70 200 20 290 90 C320 112 340 140 350 160 C360 140 380 112 410 90 C500 20 640 70 660 190 C680 320 580 440 350 600 Z" fill="url(#{nombre}_g)"/>',
         '<path d="M140 150 C170 100 230 90 270 120" stroke="#ffffff" stroke-width="22" stroke-linecap="round" opacity="0.45" fill="none"/>']
    guardar(nombre, "".join(b), w, h, d)


def foto(nombre, cara="#e8b890", pelo="#3a2a1a", fondo="#ffd0d8", marco="#c8902a", corazones=True):
    """Foto en un marco: retrato genérico (sin rasgos de nadie real)."""
    w, h = 600, 760
    b = [f'<rect x="10" y="10" width="580" height="740" rx="18" fill="{marco}"/>', f'<rect x="50" y="50" width="500" height="580" fill="{fondo}"/>',
         f'<path d="M150 630 Q300 470 450 630 Z" fill="#4a6aa8"/>', f'<circle cx="300" cy="330" r="110" fill="{cara}"/>',
         f'<path d="M190 330 Q180 190 300 190 Q420 190 410 330 Q380 250 300 250 Q220 250 190 330 Z" fill="{pelo}"/>',
         '<circle cx="262" cy="335" r="10" fill="#2a1a1a"/><circle cx="338" cy="335" r="10" fill="#2a1a1a"/>',
         '<path d="M270 385 Q300 405 330 385" stroke="#8a3a3a" stroke-width="6" fill="none" stroke-linecap="round"/>',
         '<rect x="50" y="650" width="500" height="80" fill="#f4ece0"/>']
    if corazones:
        for x, y, s in ((110, 110, 1.0), (480, 150, 0.8), (460, 560, 0.7)):
            b.append(f'<path transform="translate({x} {y}) scale({s})" d="M0 30 C-40 0 -40 -30 -18 -34 C-6 -36 0 -26 0 -20 C0 -26 6 -36 18 -34 C40 -30 40 0 0 30 Z" fill="#ff4a6a"/>')
    guardar(nombre, "".join(b), w, h)


def cerebro_corte(nombre="cerebro_corte"):
    """Cerebro de perfil en corte, con el tronco y una zona profunda marcada (área tegmental ventral)."""
    w, h = 1000, 820
    d = rg("cc_g", (0, "#ffc8d0", 1), (1, "#d87a90", 1), cx=0.4, cy=0.4)
    b = ['<path d="M120 420 C90 220 260 70 480 70 C720 70 900 200 880 400 C870 520 780 580 660 590 L560 600 C540 660 520 720 500 800 L430 800 C440 720 450 660 440 600 C300 600 140 560 120 420 Z" fill="url(#cc_g)" stroke="#8a3a5a" stroke-width="8"/>',
         '<path d="M200 300 C280 220 380 280 460 220 C540 160 640 240 720 200 M180 420 C280 360 380 420 480 360 C580 300 700 380 820 330 M300 520 C380 480 460 520 540 480" stroke="#b05a78" stroke-width="10" fill="none" opacity="0.7"/>',
         '<path d="M440 600 C480 520 560 500 600 560" stroke="#8a3a5a" stroke-width="8" fill="none"/>']
    guardar(nombre, "".join(b), w, h, d)


def dopamina(nombre="dopamina"):
    """Molécula esquemática (anillo hexagonal con cadena), con brillo."""
    w, h = 700, 500
    cx, cy, r = 220, 250, 110
    pts = [(cx + r * math.cos(math.radians(30 + 60 * k)), cy + r * math.sin(math.radians(30 + 60 * k))) for k in range(6)]
    b = ['<path d="' + "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + ' Z" fill="none" stroke="#ffd23f" stroke-width="14"/>',
         f'<path d="M{pts[0][0]:.0f} {pts[0][1]:.0f} L420 300 L520 240 L640 300" stroke="#ffd23f" stroke-width="14" fill="none"/>',
         f'<path d="M{pts[3][0]:.0f} {pts[3][1]:.0f} L40 200 M{pts[4][0]:.0f} {pts[4][1]:.0f} L160 60" stroke="#ff6aa0" stroke-width="14"/>']
    for x, y, c in [(40, 200, "#ff6aa0"), (160, 60, "#ff6aa0"), (640, 300, "#7df9ff")] + [(x, y, "#ffd23f") for x, y in pts]:
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="26" fill="{c}"/>')
    b.append('<circle cx="320" cy="250" r="160" fill="#ffd23f" opacity="0.10" filter="url(#blur20)"/>')
    guardar(nombre, "".join(b), w, h)


def chocolate(nombre="chocolate"):
    w, h = 520, 760
    b = ['<rect x="40" y="380" width="440" height="360" rx="20" fill="#c8302a"/>', '<rect x="40" y="380" width="440" height="60" fill="#e8b830"/>',
         '<path d="M40 380 L80 300 L120 360 L160 290 L200 360 L240 300 L280 370 L320 300 L360 360 L400 290 L440 360 L480 300 L480 380 Z" fill="#d8d8e0"/>',
         '<rect x="60" y="40" width="400" height="320" rx="14" fill="#5a2a12"/>']
    for i in range(3):
        for j in range(3):
            b.append(f'<rect x="{80 + i * 128}" y="{60 + j * 100}" width="110" height="84" rx="8" fill="#6a3418" stroke="#3a1a08" stroke-width="5"/>')
    guardar(nombre, "".join(b), w, h)


def anzuelo(nombre="anzuelo"):
    w, h = 400, 800
    b = ['<path d="M200 0 V80" stroke="#c8c8d0" stroke-width="6"/>', '<circle cx="200" cy="100" r="22" fill="none" stroke="#a8b0c0" stroke-width="14"/>',
         '<path d="M200 120 V560 C200 720 360 720 360 600 L330 640" stroke="#a8b0c0" stroke-width="22" fill="none" stroke-linecap="round"/>',
         '<path d="M360 600 L380 660 L330 640 Z" fill="#a8b0c0"/>', '<path d="M190 140 V540" stroke="#ffffff" stroke-width="6" opacity="0.6"/>']
    guardar(nombre, "".join(b), w, h)


def tubo_sangre(nombre="tubo_sangre"):
    w, h = 260, 900
    b = ['<rect x="80" y="60" width="100" height="780" rx="50" fill="#ffffff" opacity="0.25" stroke="#d8e8f0" stroke-width="8"/>',
         '<rect x="88" y="380" width="84" height="452" rx="42" fill="#b0101e"/>', '<rect x="60" y="20" width="140" height="70" rx="12" fill="#7a3aa8"/>',
         '<rect x="100" y="400" width="14" height="380" rx="7" fill="#ff8a8a" opacity="0.6"/>']
    guardar(nombre, "".join(b), w, h)


def bucle_pensamiento(nombre="bucle"):
    """Flecha circular que da vueltas (pensamiento que se repite)."""
    w = h = 700
    b = ['<path d="M350 90 A260 260 0 1 1 120 220" stroke="#ff6aa0" stroke-width="30" fill="none" stroke-linecap="round"/>',
         '<path d="M70 150 L140 260 L180 160 Z" fill="#ff6aa0"/>']
    guardar(nombre, "".join(b), w, h)


def pareja(nombre="pareja"):
    """Dos siluetas de espaldas dadas de la mano al atardecer (genéricas)."""
    w, h = 700, 900
    c = "#1a1020"
    b = ['<ellipse cx="350" cy="880" rx="300" ry="16" fill="#000" opacity="0.3" filter="url(#blur8)"/>',
         f'<circle cx="220" cy="180" r="70" fill="{c}"/>', f'<path d="M150 270 Q220 240 290 270 L300 600 L270 870 L230 870 L220 640 L210 870 L170 870 L140 600 Z" fill="{c}"/>',
         f'<circle cx="480" cy="210" r="62" fill="{c}"/>', f'<path d="M420 290 Q480 265 540 290 L570 620 Q480 650 400 620 Z" fill="{c}"/><path d="M440 620 L440 870 L470 870 L480 640 L490 870 L520 870 L520 620 Z" fill="{c}"/>',
         f'<path d="M295 400 Q350 470 420 400" stroke="{c}" stroke-width="30" fill="none" stroke-linecap="round"/>',
         '<path d="M150 270 Q140 400 145 560 M420 290 Q410 420 405 600" stroke="#ffb070" stroke-width="6" fill="none" opacity="0.7"/>']
    guardar(nombre, "".join(b), w, h)


def bg_atardecer(nombre="bg_atardecer"):
    r = random.Random(3)
    d = lg(f"{nombre}_c", (0, "#2a1a4a"), (0.45, "#c0507a"), (0.75, "#ffb070"), (1, "#ffe0a0"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>', '<circle cx="540" cy="1260" r="160" fill="#fff0c0"/>',
         '<circle cx="540" cy="1260" r="420" fill="#ffd0a0" opacity="0.35" filter="url(#blur40)"/>',
         '<path d="M-20 1380 Q300 1330 540 1370 T1100 1360 L1100 1920 L-20 1920 Z" fill="#3a1a3a"/>']
    for _ in range(18):
        x, y = r.uniform(0, 1080), r.uniform(200, 900)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(60, 180):.0f}" ry="{r.uniform(10, 24):.0f}" fill="#ffd0e0" opacity="0.25" filter="url(#blur8)"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


# ====================================================================== 03 · TEST DE ATENCIÓN
def bg_escena(nombre, c1, c2, c3):
    """Escenario del test: pared lisa con luz cenital y suelo oscuro (el color cambia entre la versión azul y la naranja)."""
    d = lg(f"{nombre}_p", (0, c1), (1, c2)) + lg(f"{nombre}_s", (0, c3), (1, "#0a0a14"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_p)"/>', '<ellipse cx="540" cy="600" rx="600" ry="420" fill="#ffffff" opacity="0.12" filter="url(#blur40)"/>',
         f'<rect y="1380" width="1080" height="540" fill="url(#{nombre}_s)"/>', '<rect y="1378" width="1080" height="6" fill="#ffffff" opacity="0.25"/>',
         '<ellipse cx="540" cy="1500" rx="520" ry="60" fill="#ffffff" opacity="0.06"/>', grano()]
    guardar(nombre, "".join(b), defs=d)


def pelota(nombre, c1, c2):
    w = h = 200
    d = rg(f"{nombre}_g", (0, c1, 1), (1, c2, 1), cx=0.35, cy=0.3)
    guardar(nombre, f'<circle cx="100" cy="100" r="92" fill="url(#{nombre}_g)"/><path d="M40 70 Q70 30 110 30" stroke="#ffffff" stroke-width="12" opacity="0.5" fill="none" stroke-linecap="round"/>', w, h, d)


def gorila(nombre="gorila", golpe=False):
    """Persona disfrazada de gorila (silueta peluda genérica), de pie; con golpe=True, los puños en el pecho."""
    w, h = 600, 900
    c, c2 = "#2a2420", "#4a3e36"
    b = ['<ellipse cx="300" cy="880" rx="220" ry="18" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         f'<path d="M190 560 L170 860 L260 860 L290 640 L320 860 L410 860 L400 560 Z" fill="{c}"/>',
         f'<path d="M150 260 Q300 180 450 260 L470 580 Q300 640 130 580 Z" fill="{c}"/>', f'<ellipse cx="300" cy="400" rx="100" ry="120" fill="{c2}"/>',
         f'<circle cx="300" cy="170" r="100" fill="{c}"/>', f'<ellipse cx="300" cy="200" rx="64" ry="52" fill="{c2}"/>',
         '<circle cx="268" cy="160" r="10" fill="#e8e0d0"/><circle cx="332" cy="160" r="10" fill="#e8e0d0"/>']
    if golpe:
        b += [f'<path d="M160 290 Q190 420 250 380" stroke="{c}" stroke-width="70" fill="none" stroke-linecap="round"/>',
              f'<path d="M440 290 Q410 420 350 380" stroke="{c}" stroke-width="70" fill="none" stroke-linecap="round"/>']
    else:
        b += [f'<path d="M160 290 Q100 450 110 640" stroke="{c}" stroke-width="70" fill="none" stroke-linecap="round"/>',
              f'<path d="M440 290 Q500 450 490 640" stroke="{c}" stroke-width="70" fill="none" stroke-linecap="round"/>']
    r = random.Random(2)
    for _ in range(60):
        x, y = r.uniform(140, 460), r.uniform(220, 600)
        b.append(f'<path d="M{x:.0f} {y:.0f} l{r.uniform(-8, 8):.0f} 16" stroke="#5a4e46" stroke-width="3"/>')
    guardar(nombre, "".join(b), w, h)


def tac_pulmon(nombre="tac_pulmon", con_gorila=True):
    """Corte de TAC de pulmón (vista axial) en grises, con un gorila diminuto arriba a la derecha."""
    r = random.Random(9)
    d = rg(f"{nombre}_p", (0, "#3a3a3a", 1), (1, "#0a0a0a", 1))
    b = ['<rect width="1080" height="1920" fill="#000"/>', '<ellipse cx="540" cy="1000" rx="470" ry="380" fill="#8a8a8a"/>',
         '<ellipse cx="540" cy="1000" rx="430" ry="340" fill="#5a5a5a"/>',
         f'<path d="M190 1000 C190 760 330 700 470 760 C500 900 500 1150 450 1260 C300 1300 190 1200 190 1000 Z" fill="url(#{nombre}_p)"/>',
         f'<path d="M890 1000 C890 760 750 700 610 760 C580 900 580 1150 630 1260 C780 1300 890 1200 890 1000 Z" fill="url(#{nombre}_p)"/>',
         '<ellipse cx="540" cy="1250" rx="60" ry="50" fill="#d8d8d8"/>', '<ellipse cx="540" cy="830" rx="50" ry="40" fill="#b8b8b8"/>']
    for _ in range(70):  # vasos y nódulos
        x = r.choice([r.uniform(230, 460), r.uniform(620, 850)]); y = r.uniform(800, 1220)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(2, 7):.1f}" fill="#9a9a9a"/>')
    if con_gorila:
        b.append('<g transform="translate(700 840) scale(0.11)" opacity="0.55">'
                 '<path d="M150 260 Q300 180 450 260 L470 580 Q300 640 130 580 Z" fill="#c8c8c8"/><circle cx="300" cy="170" r="100" fill="#c8c8c8"/>'
                 '<path d="M190 560 L170 860 L260 860 L290 640 L320 860 L410 860 L400 560 Z" fill="#c8c8c8"/>'
                 '<path d="M160 290 Q100 450 110 640" stroke="#c8c8c8" stroke-width="70" fill="none"/><path d="M440 290 Q500 450 490 640" stroke="#c8c8c8" stroke-width="70" fill="none"/></g>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def caja_cerillas(nombre="caja_cerillas"):
    w, h = 600, 400
    b = ['<rect x="40" y="80" width="520" height="280" rx="14" fill="#c8302a"/>', '<rect x="40" y="80" width="40" height="280" fill="#6a3a2a"/>',
         '<rect x="120" y="130" width="380" height="180" rx="10" fill="#f4e8c8"/>', '<circle cx="310" cy="220" r="50" fill="#e8b830"/>',
         '<path d="M310 170 Q330 200 310 260 Q290 200 310 170 Z" fill="#ff7a2a"/>']
    guardar(nombre, "".join(b), w, h)


def ojo_mira(nombre="ojo_mira"):
    """Ojo con la trayectoria de la mirada (puntos del seguimiento ocular)."""
    w, h = 900, 500
    b = ['<path d="M40 250 C220 40 680 40 860 250 C680 460 220 460 40 250 Z" fill="#f4ece6" stroke="#2a1410" stroke-width="12"/>',
         '<circle cx="450" cy="250" r="140" fill="#3a6a8a"/><circle cx="450" cy="250" r="70" fill="#0a0a0a"/><circle cx="410" cy="210" r="26" fill="#ffffff"/>']
    guardar(nombre, "".join(b), w, h)


def bocadillo_num(nombre="bocadillo"):
    """Bocadillo de comentario vacío (para la cifra que escribe la gente)."""
    w, h = 700, 500
    b = ['<path d="M60 60 H640 Q680 60 680 100 V340 Q680 380 640 380 H260 L160 470 L180 380 H60 Q20 380 20 340 V100 Q20 60 60 60 Z" fill="#ffffff" stroke="#141414" stroke-width="10"/>',
         *[f'<circle cx="{250 + k * 100}" cy="220" r="20" fill="#141414"/>' for k in range(3)]]
    guardar(nombre, "".join(b), w, h)


# ====================================================================== GENERAR
def generar(dirsvg):
    m22 = _mod("lotes/2026-11-22-manana/generadores/ilus_1122m.py", "_ilus_1122m_t")
    m22.generar(dirsvg)
    a = _mod("lotes/2026-11-17-manana/generadores/ilus_lote.py", "_ilus_1117m_t"); ilus.OUT = dirsvg
    a.escaner(); a.bg_lab()
    m18 = _mod("lotes/2026-11-18-manana/generadores/ilus_02.py", "_ilus_1118m_02_t"); ilus.OUT = dirsvg
    m18.ojo_simple()
    t20 = _mod("lotes/2026-11-20-tarde/generadores/ilus_1120t.py", "_ilus_1120t_t"); ilus.OUT = dirsvg
    m20 = _mod("lotes/2026-11-20-manana/generadores/ilus_1120m.py", "_ilus_1120m_t"); ilus.OUT = dirsvg
    m20.bg_estudio()
    t20.persona_pie("persona_pie_clara", "#e8e4dc"); t20.persona_pie("persona_pie_ambar", "#ffb02e")
    ilus.OUT = dirsvg
    # 01
    tarjeta_test(); mancha_negra(); celula(); retina_fila(); bg_corte(); noble(); noble("noble2", "#2a4a7a"); moneda(); mano_tapa()
    # 02
    corazon(); corazon("corazon_rosa", "#ff9ab8", "#d0507a"); foto("foto_pareja"); foto("foto_conocido", "#d8a880", "#6a5a4a", "#d8dce4", "#8a8a8a", False)
    cerebro_corte(); dopamina(); chocolate(); anzuelo(); tubo_sangre(); bucle_pensamiento(); pareja(); bg_atardecer()
    # 03
    bg_escena("bg_escena_azul", "#2a4a9a", "#14204a", "#1a1a3a"); bg_escena("bg_escena_naranja", "#d0702a", "#6a2a10", "#2a1a14")
    pelota("pelota_amarilla", "#fff27a", "#e8b800"); pelota("pelota_blanca", "#ffffff", "#b8b8c8")
    gorila(); gorila("gorila_golpe", True); tac_pulmon(); tac_pulmon("tac_sin", False); caja_cerillas(); ojo_mira(); bocadillo_num()
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
