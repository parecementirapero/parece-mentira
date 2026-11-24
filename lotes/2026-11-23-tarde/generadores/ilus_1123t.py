"""Ilustraciones del lote 2026-11-23-tarde (Jorge, con el agente): 01 no ves tus ojos moverse, 02 el Sol es blanco, 03 di el color (Stroop).
Uso: python3 ilus_1123t.py DIR_SVG. Reutiliza el lote 2026-11-22-tarde entero (muñecos cartoon, cerebro, ojo…) y piezas del 20-11 tarde.
Estilo cartoon con contorno grueso (el que pidió Jorge el 23-11). Todo dibujado aquí, sin logos ni personas reales."""
import importlib.util, math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano  # noqa: E402

OL = "#1b1b2b"


def _mod(rel, nombre):
    s = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, rel))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


# ---------------------------------------------------------------- 01 · ojos
def espejo(nombre="espejo"):
    """Espejo de pared con marco de madera y reflejo (el interior se deja medio transparente para ver el muñeco detrás)."""
    w, h = 640, 900
    d = lg("es_m", (0, "#c88a4a"), (1, "#7a4a20")) + lg("es_v", (0, "#d8eef8"), (1, "#8ab0c8"))
    b = [f'<rect x="20" y="20" width="600" height="860" rx="60" fill="url(#es_m)" stroke="{OL}" stroke-width="10"/>',
         f'<rect x="70" y="70" width="500" height="760" rx="30" fill="url(#es_v)" opacity="0.35" stroke="{OL}" stroke-width="8"/>',
         '<path d="M120 200 L240 110 M120 300 L340 130" stroke="#ffffff" stroke-width="14" opacity="0.55" stroke-linecap="round"/>']
    guardar(nombre, "".join(b), w, h, d)


def ojo_cartoon(nombre="ojo_cartoon"):
    """Ojo grande de dibujo con contorno (sin pupila: la pupila va aparte para moverla)."""
    w, h = 700, 460
    b = [f'<path d="M30 230 C190 20 510 20 670 230 C510 440 190 440 30 230 Z" fill="#ffffff" stroke="{OL}" stroke-width="14"/>',
         f'<path d="M60 120 Q350 -40 640 120" stroke="{OL}" stroke-width="16" fill="none" stroke-linecap="round"/>']
    guardar(nombre, "".join(b), w, h)


def pupila_cartoon(nombre="pupila_cartoon"):
    w = h = 260
    b = ['<circle cx="130" cy="130" r="110" fill="#3a8a6a" stroke="#1b1b2b" stroke-width="10"/>', '<circle cx="130" cy="130" r="56" fill="#1b1b2b"/>',
         '<circle cx="104" cy="100" r="20" fill="#ffffff"/>']
    guardar(nombre, "".join(b), w, h)


def flash_salto(nombre="salto"):
    """Arco discontinuo de «salto» para enseñar el movimiento sacádico."""
    w, h = 700, 300
    b = [f'<path d="M80 220 Q350 -40 620 220" stroke="#ffd23f" stroke-width="16" fill="none" stroke-dasharray="40 26" stroke-linecap="round"/>',
         '<path d="M590 170 L630 230 L560 225 Z" fill="#ffd23f"/>']
    guardar(nombre, "".join(b), w, h)


def reloj_pared(nombre="reloj_cartoon"):
    w = h = 620
    b = [f'<circle cx="310" cy="310" r="280" fill="#fff6e8" stroke="{OL}" stroke-width="16"/>']
    for k in range(12):
        a = math.radians(k * 30)
        b.append(f'<path d="M{310 + 230 * math.sin(a):.0f} {310 - 230 * math.cos(a):.0f} L{310 + 255 * math.sin(a):.0f} {310 - 255 * math.cos(a):.0f}" stroke="{OL}" stroke-width="12" stroke-linecap="round"/>')
    b += [f'<path d="M310 310 L310 160" stroke="{OL}" stroke-width="18" stroke-linecap="round"/>', f'<path d="M310 310 L420 360" stroke="{OL}" stroke-width="22" stroke-linecap="round"/>']
    guardar(nombre, "".join(b), w, h)


def segundero(nombre="segundero"):
    w = h = 620
    guardar(nombre, '<path d="M310 360 L310 70" stroke="#e8402a" stroke-width="8" stroke-linecap="round"/><circle cx="310" cy="310" r="18" fill="#e8402a"/>', w, h)


# ---------------------------------------------------------------- 02 · el Sol
def bg_cielo_dia(nombre="bg_cielo_dia"):
    r = random.Random(4)
    d = lg(f"{nombre}_c", (0, "#2a6ad8"), (0.6, "#7ab8f0"), (1, "#d8ecff"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>']
    for _ in range(6):
        x, y = r.uniform(80, 1000), r.uniform(900, 1500)
        b.append(f'<g opacity="0.9"><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="120" ry="44" fill="#ffffff" stroke="{OL}" stroke-width="6"/>'
                 f'<circle cx="{x - 40:.0f}" cy="{y - 30:.0f}" r="50" fill="#ffffff"/><circle cx="{x + 40:.0f}" cy="{y - 40:.0f}" r="60" fill="#ffffff"/></g>')
    b.append('<path d="M-20 1640 Q300 1560 600 1620 T1100 1600 L1100 1940 L-20 1940 Z" fill="#5ab04a" stroke="#1b1b2b" stroke-width="8"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def sol_blanco(nombre="sol_blanco", c1="#ffffff", c2="#fff8e8", halo="#ffffff"):
    w = h = 700
    d = rg(f"{nombre}_g", (0, c1, 1), (0.8, c2, 1), (1, c2, 1))
    b = [f'<circle cx="350" cy="350" r="330" fill="{halo}" opacity="0.18"/>', f'<circle cx="350" cy="350" r="270" fill="{halo}" opacity="0.25"/>',
         f'<circle cx="350" cy="350" r="210" fill="url(#{nombre}_g)" stroke="{OL}" stroke-width="10"/>']
    guardar(nombre, "".join(b), w, h, d)


def sol_dibujo(nombre="sol_dibujo"):
    """El Sol amarillo de los dibujos, con rayos y cara sonriente."""
    w = h = 700
    b = []
    for k in range(12):
        a = math.radians(k * 30)
        b.append(f'<path d="M{350 + 220 * math.sin(a):.0f} {350 - 220 * math.cos(a):.0f} L{350 + 320 * math.sin(a):.0f} {350 - 320 * math.cos(a):.0f}" stroke="#ffc800" stroke-width="30" stroke-linecap="round"/>')
    b += [f'<circle cx="350" cy="350" r="190" fill="#ffd23f" stroke="{OL}" stroke-width="12"/>',
          f'<circle cx="290" cy="320" r="18" fill="{OL}"/><circle cx="410" cy="320" r="18" fill="{OL}"/>',
          f'<path d="M270 400 Q350 470 430 400" stroke="{OL}" stroke-width="14" fill="none" stroke-linecap="round"/>',
          '<ellipse cx="250" cy="380" rx="26" ry="14" fill="#ff8a6a" opacity="0.6"/><ellipse cx="450" cy="380" rx="26" ry="14" fill="#ff8a6a" opacity="0.6"/>']
    guardar(nombre, "".join(b), w, h)


def espectro(nombre="espectro"):
    """Los colores de la luz en barras, con contorno (del violeta al rojo)."""
    w, h = 900, 520
    cols = ["#8a3ad8", "#3a5ae8", "#2ab0e8", "#3ac84a", "#ffe02a", "#ff9a2a", "#ff3a2a"]
    b = []
    for k, c in enumerate(cols):
        b.append(f'<rect x="{40 + k * 120}" y="60" width="100" height="400" rx="20" fill="{c}" stroke="{OL}" stroke-width="8"/>')
    guardar(nombre, "".join(b), w, h)


def rayo_luz(nombre, color, dash=False):
    """Rayo de luz ondulado (para la luz que viaja)."""
    w, h = 900, 160
    pts = " ".join(f"L{x} {80 + 40 * math.sin(x / 40):.0f}" for x in range(20, 880, 10))
    b = [f'<path d="M10 80 {pts}" stroke="{color}" stroke-width="16" fill="none" stroke-linecap="round"' + (' stroke-dasharray="30 20"' if dash else '') + '/>']
    guardar(nombre, "".join(b), w, h)


def molecula(nombre="molecula_aire"):
    w = h = 160
    guardar(nombre, f'<circle cx="60" cy="80" r="40" fill="#d8ecff" stroke="{OL}" stroke-width="8"/><circle cx="110" cy="80" r="40" fill="#d8ecff" stroke="{OL}" stroke-width="8"/>', w, h)


# ---------------------------------------------------------------- 03 · Stroop
def bg_pizarra(nombre="bg_pizarra"):
    d = lg(f"{nombre}_c", (0, "#1a1a2e"), (1, "#0e0e1a"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>', '<rect x="60" y="560" width="960" height="900" rx="40" fill="#f6f2ea" stroke="#1b1b2b" stroke-width="12"/>',
         '<rect x="60" y="560" width="960" height="900" rx="40" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.4"/>', grano()]
    guardar(nombre, "".join(b), defs=d)


def generar(dirsvg):
    m = _mod("lotes/2026-11-22-tarde/generadores/ilus_1122t.py", "_ilus_1122t_23")
    m.generar(dirsvg)
    t20 = _mod("lotes/2026-11-20-tarde/generadores/ilus_1120t.py", "_ilus_1120t_23"); ilus.OUT = dirsvg
    t20.tierra_arco(); t20.bg_amanecer_orbital()
    ilus.OUT = dirsvg
    espejo(); ojo_cartoon(); pupila_cartoon(); flash_salto(); reloj_pared(); segundero()
    bg_cielo_dia(); sol_blanco(); sol_blanco("sol_amarillento", "#fffbe0", "#ffe27a", "#fff0a0"); sol_blanco("sol_rojo", "#ffb070", "#ff5a2a", "#ff8a4a")
    sol_dibujo(); espectro(); rayo_luz("rayo_blanco", "#ffffff"); rayo_luz("rayo_azul", "#3a7aff"); rayo_luz("rayo_verde", "#3ac84a"); molecula()
    bg_pizarra()
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
