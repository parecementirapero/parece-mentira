"""Personajes del vídeo largo «El que copiaba en el colegio» (estilo del vídeo largo de la cueva).

Marta, Lucas y la profesora con el diseño fijo de ARTE.md, más clientes, vida diaria y caras para primeros planos.
Todas las piezas: fondo transparente y lienzo ajustado (se dibujan en un lienzo amplio y luego se recorta la caja
al contenido real; los fotogramas _a/_b comparten la misma caja).
Uso: python3 ilus_gente.py DIR_SVG   (o importar y llamar a generar(DIR))"""
import math, os, re, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
LARGO = os.path.join(RAIZ, "lotes", "largo-cueva-500-dias", "generadores")
sys.path.insert(0, RAIZ)
sys.path.insert(0, LARGO)
from motor.biblioteca import ilus  # noqa: E402
import ilus_personajes as IP  # noqa: E402
from ilus_personajes import (Lz, figura, busto, _pj, mat, sombra_suelo, pie_suelo, forma, pliegue, suave, mix, oscuro,  # noqa: E402
                             ad, D, F, P, ik, PIEL2, PIEL3, PIEL4, DIA, L_MUSLO, L_PIERNA)

CLASE = dict(luz=(-0.6, -0.8), rim="#fff1d8")   # luz de aula / interior cálido
CALLE = dict(luz=(-0.5, -0.85), rim="#ffe2b0")

# =========================================================================== peinado de Marta: coleta alta
MARTA_PELO, MARTA_BRILLO = "#7a3a22", "#b5643a"


def _p_coleta_alta(z, vista, capa, c, cl, cs, gp):
    cl = MARTA_BRILLO if c == MARTA_PELO else cl
    lx = -1 if z.luz[0] < 0 else 1
    g = z.rad((lx * 12, -40), 70, [(0, cl), (0.45, c), (1, cs)])
    if capa == "del":
        return IP._pelo_coleta(z, vista, "del", False, c, cl, cs, g, False)
    gt = z.lin((0, -80), (60, 40), [(0, cl), (0.45, c), (1, cs)])
    if vista == "frente":
        # nace en la coronilla, asoma por arriba y cae por detrás del lado derecho de la pantalla
        d = ("M-6 -54 C-4 -70 14 -80 32 -72 C48 -64 54 -42 52 -16 C51 4 48 24 40 42 C38 30 38 14 38 0 "
             "C38 -20 36 -40 26 -52 C18 -60 6 -60 -6 -54 Z")
        hs = ["M2 -62 C16 -72 34 -66 44 -46", "M30 -66 C44 -54 48 -30 46 -4", "M36 -48 C42 -30 44 0 42 28"]
        return (f'<path d="{d}" fill="{gt}"/>' + IP._hebras(z, cl, hs[:2], 1.3, 0.55) + IP._hebras(z, cs, hs[2:], 1.3, 0.7)
                + '<ellipse cx="2" cy="-57" rx="9" ry="5" fill="#1c2430" transform="rotate(-18 2 -57)"/>')
    if vista in ("tq", "perfil"):
        d = ("M-22 -54 C-36 -66 -58 -62 -66 -44 C-74 -24 -70 6 -60 34 C-62 12 -60 -10 -54 -26 "
             "C-48 -40 -38 -46 -26 -44 Z")
        hs = ["M-28 -56 C-46 -62 -62 -50 -66 -30", "M-36 -50 C-52 -46 -62 -24 -62 6", "M-46 -48 C-58 -36 -64 -10 -62 22"]
        return (f'<path d="{d}" fill="{gt}"/>' + IP._hebras(z, cl, hs[:2], 1.3, 0.55) + IP._hebras(z, cs, hs[2:], 1.3, 0.7)
                + '<ellipse cx="-26" cy="-50" rx="5" ry="8" fill="#1c2430" transform="rotate(40 -26 -50)"/>')
    return ""


IP._PELOS["coleta_alta"] = _p_coleta_alta

# =========================================================================== personajes fijos
MOSTAZA = mat("#e0a92e", "#f4cc6a", "#8a6010")
VAQUERO = mat("#3b5274", "#5f7aa0", "#1f2c42")
BLANCAS = mat("#e8e4dc", "#ffffff", "#9a968e")
POLAR_AZUL = mat("#2f6fb0", "#5f9fe0", "#173a60")

MARTA = _pj(nombre="marta", fem=True, peinado="coleta_alta", pelo=MARTA_PELO, piel=PIEL4, iris="#3d6a5a", labio="#c0645a",
            top=MOSTAZA, prenda="chaqueta", pant=VAQUERO, vaquero=True, calzado="zapato", bota=BLANCAS, edad=30)
MARTA_NINA = _pj(nombre="martan", fem=True, peinado="coleta_alta", pelo=MARTA_PELO, piel=PIEL4, iris="#3d6a5a", labio="#c8706a",
                 top=MOSTAZA, prenda="jersey", pant=VAQUERO, vaquero=True, calzado="zapato", bota=BLANCAS, edad=11)
LUCAS = _pj(nombre="lucas", peinado="corto", pelo="#1e1612", top=POLAR_AZUL, prenda="polar",
            pant=mat("#2e3440"), calzado="zapato", bota=BLANCAS, edad=24, piel=PIEL4)
LUCAS_NINO = _pj(nombre="lucasn", peinado="nino", pelo="#1e1612", top=POLAR_AZUL, prenda="polar",
                 pant=mat("#2e3440"), calzado="zapato", bota=BLANCAS, edad=11, piel=PIEL4)
PROFE = _pj(nombre="profe", fem=True, peinado="corto", pelo="#8a8a90", piel=dict(b="#e6b593", s="#b47c5a", l="#f6d0b0"),
            iris="#4a5a6a", labio="#a85a58", top=mat("#7a2a3a", "#a8505e", "#3e1018"), prenda="abrigo",
            pant=mat("#4a4450", "#6a6270", "#2a2630"), calzado="zapato", bota=mat("#2a1d14"), edad=46)
FALDA = mat("#6a6a72", "#8e8e98", "#3a3a42")

# clientes y gente de la vida diaria (distintos de pelo, piel y ropa)
CONF1 = _pj(nombre="conf1", peinado="peinado60", pelo="#5a4a3a", barba="#5a4a3a", top=mat("#5a3a6a", "#8a64a0", "#2e1c38"),
            prenda="chaqueta", pant=mat("#2a2a34"), calzado="zapato", bota=mat("#2a1d14"), edad=50)
CONF2 = _pj(nombre="conf2", fem=True, peinado="mono", pelo="#1a120c", top=mat("#2a7f9e", "#5fb3cf", "#174a5e"), prenda="polar",
            pant=mat("#3a3f4a"), calzado="zapato", bota=mat("#1e1a16"), edad=38, piel=PIEL3, labio="#8a4a40")
SEVA = _pj(nombre="seva", peinado="corto", pelo="#3a2a1e", top=mat("#6a7a3f", "#98a660", "#39421f"), prenda="parka",
           pant=VAQUERO, vaquero=True, calzado="zapato", bota=mat("#4a3020"), edad=34, piel=PIEL2)
FELIZ = [
    _pj(nombre="fel1", fem=True, peinado="melena", pelo="#c9a26b", top=mat("#c0392b", "#e66a58", "#6a1712"), prenda="polar",
        pant=VAQUERO, vaquero=True, calzado="zapato", bota=BLANCAS, edad=26, piel=PIEL4, iris="#4a6a8a"),
    _pj(nombre="fel2", peinado="rizado", pelo="#1a120c", top=mat("#3a8a5e", "#6ab88c", "#1d4a32"), prenda="camiseta", manga="corta",
        pant=mat("#4a4038", "#6e6052", "#2a241e"), calzado="zapato", bota=mat("#e8e4dc"), edad=22, piel=PIEL3, labio="#8a4a40"),
    _pj(nombre="fel3", peinado="calvo", pelo="#9a948c", barba="#9a948c", top=mat("#d8682a", "#f09a5e", "#7a3410"), prenda="jersey",
        pant=mat("#3a4a3a"), calzado="zapato", bota=mat("#2a1d14"), edad=60, piel=PIEL2),
]
FUTBOL = _pj(nombre="futb", peinado="nino", pelo="#3a2414", piel=PIEL2, top=mat("#1f8a4c", "#4fc07a", "#0e4a26"), prenda="camiseta",
             manga="corta", pantalon="corto", pant=mat("#f2f2f0", "#ffffff", "#a8a8a6"), calzado="zapato", bota=mat("#2a2a2e", "#5a5a60", "#101012"),
             suela="#e0e0e0", edad=10, iris="#3a2a1a")
GUITAR = _pj(nombre="guit", peinado="rizado", pelo="#2a1a10", piel=PIEL3, labio="#8a4a40", top=mat("#5a5f8a", "#8a90c0", "#2a2e4a"),
             prenda="camiseta", manga="corta", pant=mat("#2e3440"), calzado="zapato", bota=BLANCAS, edad=16, iris="#2a1a10")
COCINERO = _pj(nombre="coci", peinado="corto", pelo="#2a1d14", barba="#2a1d14", piel=PIEL2, top=mat("#4a6a8a", "#7a9ab8", "#223448"),
               prenda="camisa", pant=mat("#2e3440"), calzado="zapato", bota=mat("#1e1a16"), edad=42)
PADRE = _pj(nombre="padre", peinado="corto", pelo="#3a2a1e", barba="#3a2a1e", top=mat("#3d4f6a", "#6a7f9c", "#1f2a3a"), prenda="jersey",
            pant=mat("#5a4a38", "#7f6c55", "#2f261c"), calzado="zapato", bota=mat("#2a1d14"), edad=36, piel=PIEL4)
MADRE = _pj(nombre="madre", fem=True, peinado="melena", pelo="#2a1a10", top=mat("#8fb0c4", "#c4dcec", "#4a6a80"), prenda="camisa",
            pant=VAQUERO, vaquero=True, calzado="zapato", bota=mat("#5a3a24"), edad=33, piel=PIEL4, iris="#3d6a5a")

# expresiones propias
EX = {
    "reojo": dict(ojo=0.62, mira=(1.0, 0.1), ceja=(0.5, 1.5), ceja2=(-3, 0), boca="mueca", mejilla=0.6),
    "culpable": dict(ojo=1.3, mira=(-0.3, 0), ceja=(-6, -4), boca="tensa"),
    "castigado": dict(ojo=0.55, mira=(0, 0.9), ceja=(-1, -4.5), boca="triste"),
    "triste": dict(ojo=0.7, mira=(0.1, 0.8), ceja=(-1, -4), boca="triste"),
    "enfadada": dict(ojo=0.8, mira=(0, 0), ceja=(2.5, 4.5), boca="tensa"),
    "entiende": dict(ojo=1.2, mira=(0, 0), ceja=(-5, -1.5), boca="o"),
    "confuso": dict(ojo=0.95, mira=(0.3, -0.3), ceja=(2, 2), ceja2=(-5, 0), boca="mueca"),
    "encoge": dict(ojo=1.05, mira=(0, 0), ceja=(-5, -3), boca="mueca"),
    "piensa": dict(ojo=0.88, mira=(0.6, -1.0), ceja=(-2, 0), ceja2=(-5, 0), boca="pensativo"),
    "lee": dict(ojo=0.6, mira=(-0.7, 0.7), ceja=(0, -0.5), boca="neutra"),
    "listo": dict(ojo=0.45, mira=(0.2, 0), ceja=(1.5, 1), ceja2=(-2, 0), boca="sonrisa", mejilla=0.8),
}

# =========================================================================== infraestructura
META = {}       # nombre -> dict(suelo=y, mesa=y opcional) en coordenadas del lienzo grande
GRUPOS = []     # listas de nombres que comparten caja


def _pieza(n, suelo, **extra):
    META[n] = dict(suelo=suelo, **extra)
    return n


def _recortar(dirsvg, margen=10):
    """Recorta cada SVG a su contenido (caja común en los grupos a/b) y devuelve {nombre: apoyo, mesa…} en fracciones."""
    cajas = {}
    with tempfile.TemporaryDirectory() as td:
        for n in META:
            png = os.path.join(td, n + ".png")
            subprocess.run(["rsvg-convert", os.path.join(dirsvg, n + ".svg"), "-o", png], check=True)
            from PIL import Image
            im = Image.open(png).convert("RGBA")
            a = im.split()[3].point(lambda v: 255 if v > 6 else 0)
            cajas[n] = a.getbbox()
    agrupado = {n: [n] for n in META}
    for g in GRUPOS:
        for n in g:
            agrupado[n] = g
    out = {}
    for n in META:
        bs = [cajas[m] for m in agrupado[n]]
        x0 = max(0, min(b[0] for b in bs) - margen)
        y0 = max(0, min(b[1] for b in bs) - margen)
        x1 = max(b[2] for b in bs) + margen
        y1 = max(b[3] for b in bs) + margen
        w, h = x1 - x0, y1 - y0
        ruta = os.path.join(dirsvg, n + ".svg")
        s = open(ruta).read()
        s = re.sub(r'viewBox="[^"]*" width="[^"]*" height="[^"]*"', f'viewBox="{x0} {y0} {w} {h}" width="{w}" height="{h}"', s, count=1)
        open(ruta, "w").write(s)
        m = META[n]
        info = dict(w=w, h=h, apoyo=min(1.0, round((m["suelo"] - y0) / h, 3)))
        if "mesa" in m:
            info["mesa"] = round((m["mesa"] - y0) / h, 3)
        if "balon" in m:
            info["balon"] = (round((m["balon"][0] - x0) / w, 3), round((m["balon"][1] - y0) / h, 3))
        out[n] = info
    return out


# =========================================================================== accesorios
def delantal(color, largo=1.55):
    """Capa de delantal (peto + falda hasta la rodilla) para vista de frente."""
    m = mat(color)

    def f(z, J):
        T, u = J["T"], J["u"]
        # tiras al cuello
        for sg in (-1, 1):
            z(f'<path d="M{P(T(2.0, sg * 0.36))} Q{P(T(2.3, sg * 0.3))} {P(T(2.42, sg * 0.18))}" fill="none" stroke="{m["s"]}" stroke-width="{F(0.07 * u)}" stroke-linecap="round"/>')
        d = suave([T(2.02, -0.38), T(2.02, 0.38), T(1.2, 0.46), T(0.95, 0.66), T(0.2, 0.74), T(-largo, 0.8), T(-largo - 0.04, 0.0),
                   T(-largo, -0.8), T(0.2, -0.74), T(0.95, -0.66), T(1.2, -0.46)], t=0.35)
        forma(z, d, m, T(1.0, -0.9), T(1.0, 0.9))
        # cintas de la cintura, bolsillo y pliegues
        z(f'<path d="M{P(T(0.95, -0.68))} L{P(T(0.95, 0.68))}" stroke="{m["s"]}" stroke-width="{F(0.05 * u)}" opacity="0.7"/>')
        z(f'<path d="M{P(T(0.25, -0.45))} L{P(T(0.25, 0.45))} L{P(T(-0.25, 0.45))} L{P(T(-0.25, -0.45))} Z" fill="{m["s"]}" opacity="0.35"/>'
          f'<path d="M{P(T(0.25, 0.0))} L{P(T(-0.25, 0.0))}" stroke="{m["s"]}" stroke-width="{F(0.02 * u)}" opacity="0.6"/>')
        for s in (-0.45, 0.3):
            pliegue(z, f"M{P(T(-0.4, s))} Q{P(T(-0.9, s + 0.05))} {P(T(-largo + 0.05, s + 0.1))}", m, 0.03 * u, 0.5)
        z(f'<path d="M{P(T(2.0, -0.36))} L{P(T(2.0, 0.36))}" stroke="{m["l"]}" stroke-width="{F(0.025 * u)}" opacity="0.6"/>')
    return f


def camiseta_blanca(z, J):
    """Camiseta blanca que asoma por la chaqueta abierta de Marta (vista de frente)."""
    T, u = J["T"], J["u"]
    m = mat("#f4f2ee", "#ffffff", "#b8b4ac")
    d = suave([T(2.42, -0.2), T(2.3, 0.0), T(2.42, 0.2), T(1.6, 0.17), T(0.35, 0.15), T(0.35, -0.15), T(1.6, -0.17)], t=0.3)
    forma(z, d, m, T(1.4, -0.3), T(1.4, 0.3))
    for sg in (-1, 1):
        z(f'<path d="M{P(T(2.4, sg * 0.21))} Q{P(T(1.6, sg * 0.2))} {P(T(0.35, sg * 0.17))}" fill="none" stroke="{MOSTAZA["s"]}" stroke-width="{F(0.05 * u)}"/>')


def falda(z, J):
    T, u = J["T"], J["u"]
    d = suave([T(0.85, -0.62), T(0.85, 0.62), T(-0.4, 0.8), T(-1.45, 0.9), T(-1.5, 0.0), T(-1.45, -0.9), T(-0.4, -0.8)], t=0.3)
    forma(z, d, FALDA, T(0, -1), T(0, 1))
    for s in (-0.4, 0.05, 0.45):
        pliegue(z, f"M{P(T(0.3, s))} Q{P(T(-0.6, s * 1.15))} {P(T(-1.42, s * 1.3))}", FALDA, 0.025 * u, 0.45)


def hoja(z, c, w, ang=0, dibujo=True):
    """Hoja de papel con un dibujo de lápiz (sin letras)."""
    x, y = c
    h = w * 1.3
    z(f'<g transform="rotate({F(ang)} {F(x)} {F(y)})"><rect x="{F(x - w / 2 + 3)}" y="{F(y - h / 2 + 4)}" width="{F(w)}" height="{F(h)}" fill="#000" opacity="0.18"/>'
      f'<rect x="{F(x - w / 2)}" y="{F(y - h / 2)}" width="{F(w)}" height="{F(h)}" fill="#fbf8f0" stroke="#c8c0b0" stroke-width="1.2"/>')
    if dibujo:
        k = w / 100
        z(f'<circle cx="{F(x + 24 * k)}" cy="{F(y - 38 * k)}" r="{F(12 * k)}" fill="#f2c230" opacity="0.9"/>'
          f'<path d="M{F(x - 34 * k)} {F(y + 30 * k)} L{F(x - 34 * k)} {F(y - 4 * k)} L{F(x - 10 * k)} {F(y - 26 * k)} L{F(x + 14 * k)} {F(y - 4 * k)} L{F(x + 14 * k)} {F(y + 30 * k)} Z" '
          f'fill="#e0603a" opacity="0.75" stroke="#7a2a1a" stroke-width="{F(2 * k)}"/>'
          f'<rect x="{F(x - 18 * k)}" y="{F(y + 8 * k)}" width="{F(14 * k)}" height="{F(22 * k)}" fill="#6a3a1a" opacity="0.8"/>'
          f'<path d="M{F(x - 44 * k)} {F(y + 32 * k)} Q{F(x)} {F(y + 26 * k)} {F(x + 44 * k)} {F(y + 34 * k)}" stroke="#4a9a4a" stroke-width="{F(4 * k)}" fill="none"/>'
          f'<path d="M{F(x + 26 * k)} {F(y + 30 * k)} L{F(x + 26 * k)} {F(y + 8 * k)}" stroke="#6a4a2a" stroke-width="{F(3 * k)}"/>'
          f'<circle cx="{F(x + 26 * k)}" cy="{F(y + 2 * k)}" r="{F(9 * k)}" fill="#4a9a4a" opacity="0.85"/>')
    else:
        for i in range(6):
            yy = y - h * 0.35 + i * h * 0.12
            z(f'<path d="M{F(x - w * 0.36)} {F(yy)} Q{F(x)} {F(yy - 2)} {F(x + w * (0.36 - 0.1 * (i % 2)))} {F(yy)}" stroke="#7a7a86" stroke-width="{F(w * 0.02)}" fill="none" opacity="0.6"/>')
    z("</g>")


def hoja_mesa(z, c, w):
    """Hoja apoyada en la mesa vista desde delante (trapecio aplastado) con renglones a lápiz."""
    x, y = c
    h = w * 0.32
    d = f"M{F(x - w * 0.42)} {F(y - h / 2)} L{F(x + w * 0.42)} {F(y - h / 2)} L{F(x + w * 0.5)} {F(y + h / 2)} L{F(x - w * 0.5)} {F(y + h / 2)} Z"
    z(f'<path d="{d}" fill="#fbf8f0" stroke="#c8c0b0" stroke-width="1.2"/>')
    for i in range(3):
        yy = y - h * 0.25 + i * h * 0.25
        z(f'<path d="M{F(x - w * 0.36)} {F(yy)} L{F(x + w * (0.1 + 0.1 * i))} {F(yy)}" stroke="#7a7a86" stroke-width="2" opacity="0.5"/>')


def lapiz(z, W, ah, u, largo=0.5):
    p0 = ad(ad(W, D(ah), 0.3 * u), D(ah + 90), 0.02 * u)
    a = D(ah + 150)
    p1, p2 = ad(p0, a, -largo * u), ad(p0, a, 0.1 * u)
    z(f'<path d="M{P(p1)} L{P(p0)}" stroke="#e0a92e" stroke-width="{F(0.065 * u)}"/>'
      f'<path d="M{P(p1)} L{P(ad(p1, a, 0.06 * u))}" stroke="#e88a9a" stroke-width="{F(0.065 * u)}"/>'
      f'<path d="M{P(p0)} L{P(p2)}" stroke="#e8c9a0" stroke-width="{F(0.05 * u)}"/>'
      f'<circle cx="{F(p2[0])}" cy="{F(p2[1])}" r="{F(0.014 * u)}" fill="#2a2a2a"/>')


def bolsa(z, top, u, k=1.0):
    """Bolsa de papel de la hamburguesería (sin logotipo) colgando de la mano; top = punto donde se agarra."""
    x, y = top
    w, h = 0.95 * u * k, 1.15 * u * k
    m = mat("#b8895a", "#dcb07e", "#6e4e2e")
    d = f"M{F(x - w / 2)} {F(y + 0.12 * u)} L{F(x + w / 2)} {F(y + 0.12 * u)} L{F(x + w / 2 + 4)} {F(y + h)} L{F(x - w / 2 - 4)} {F(y + h)} Z"
    forma(z, d, m, (x - w / 2, y), (x + w / 2, y))
    z(f'<path d="M{F(x - w / 2)} {F(y + 0.12 * u)} L{F(x - w / 2 + 6)} {F(y - 0.02 * u)} L{F(x + w / 2 - 6)} {F(y - 0.02 * u)} L{F(x + w / 2)} {F(y + 0.12 * u)} Z" fill="{m["l"]}"/>'
      f'<path d="M{F(x - w / 2)} {F(y + 0.2 * u)} L{F(x + w / 2)} {F(y + 0.2 * u)}" stroke="{m["s"]}" stroke-width="2" opacity="0.6"/>'
      f'<circle cx="{F(x)}" cy="{F(y + 0.55 * u * k)}" r="{F(0.2 * u * k)}" fill="#c8322a" opacity="0.85"/>'
      f'<path d="M{F(x - 0.1 * u * k)} {F(y + 0.53 * u * k)} Q{F(x)} {F(y + 0.42 * u * k)} {F(x + 0.1 * u * k)} {F(y + 0.53 * u * k)} Z" fill="#f2c230"/>'
      f'<path d="M{F(x - w / 2 - 4)} {F(y + h)} L{F(x + w / 2 + 4)} {F(y + h)}" stroke="{m["s"]}" stroke-width="3"/>')


def hamburguesa(z, c, s):
    x, y = c
    z(f'<path d="M{F(x - s)} {F(y)} Q{F(x - s)} {F(y - 0.85 * s)} {F(x)} {F(y - 0.88 * s)} Q{F(x + s)} {F(y - 0.85 * s)} {F(x + s)} {F(y)} Z" fill="#e8a040"/>'
      f'<path d="M{F(x - 0.7 * s)} {F(y - 0.3 * s)} Q{F(x - 0.55 * s)} {F(y - 0.7 * s)} {F(x - 0.1 * s)} {F(y - 0.75 * s)}" stroke="#ffd890" stroke-width="{F(0.1 * s)}" fill="none" stroke-linecap="round"/>'
      f'<path d="M{F(x - 1.08 * s)} {F(y + 0.05 * s)} Q{F(x - 0.8 * s)} {F(y - 0.12 * s)} {F(x - 0.5 * s)} {F(y + 0.08 * s)} Q{F(x - 0.2 * s)} {F(y - 0.12 * s)} {F(x + 0.1 * s)} {F(y + 0.08 * s)} '
      f'Q{F(x + 0.45 * s)} {F(y - 0.12 * s)} {F(x + 1.08 * s)} {F(y + 0.05 * s)} L{F(x + 1.05 * s)} {F(y + 0.18 * s)} L{F(x - 1.05 * s)} {F(y + 0.18 * s)} Z" fill="#6ab04a"/>'
      f'<rect x="{F(x - 1.02 * s)}" y="{F(y + 0.16 * s)}" width="{F(2.04 * s)}" height="{F(0.16 * s)}" rx="{F(0.06 * s)}" fill="#f0c020"/>'
      f'<rect x="{F(x - 1.0 * s)}" y="{F(y + 0.3 * s)}" width="{F(2.0 * s)}" height="{F(0.3 * s)}" rx="{F(0.14 * s)}" fill="#6a3418"/>'
      f'<path d="M{F(x - 0.98 * s)} {F(y + 0.6 * s)} L{F(x + 0.98 * s)} {F(y + 0.6 * s)} Q{F(x + 0.95 * s)} {F(y + 0.95 * s)} {F(x)} {F(y + 0.96 * s)} Q{F(x - 0.95 * s)} {F(y + 0.95 * s)} {F(x - 0.98 * s)} {F(y + 0.6 * s)} Z" fill="#d8903a"/>')
    for dx, dy in ((-0.4, -0.55), (0, -0.66), (0.4, -0.52), (-0.15, -0.38), (0.25, -0.34)):
        z(f'<ellipse cx="{F(x + dx * s)}" cy="{F(y + dy * s)}" rx="{F(0.07 * s)}" ry="{F(0.04 * s)}" fill="#fff4d0"/>')


def taza(z, c, u):
    """Taza con platillo y café (con vapor suave) apoyada en c (centro del platillo)."""
    x, y = c
    z(f'<ellipse cx="{F(x)}" cy="{F(y)}" rx="{F(0.42 * u)}" ry="{F(0.08 * u)}" fill="#e8e4dc" stroke="#a8a49c" stroke-width="1.5"/>')
    m = mat("#f4f2ee", "#ffffff", "#b0aca4")
    d = f"M{F(x - 0.26 * u)} {F(y - 0.42 * u)} L{F(x + 0.26 * u)} {F(y - 0.42 * u)} Q{F(x + 0.25 * u)} {F(y - 0.02 * u)} {F(x)} {F(y - 0.02 * u)} Q{F(x - 0.25 * u)} {F(y - 0.02 * u)} {F(x - 0.26 * u)} {F(y - 0.42 * u)} Z"
    z(f'<path d="M{F(x + 0.24 * u)} {F(y - 0.34 * u)} q{F(0.18 * u)} {F(0.02 * u)} {F(0.12 * u)} {F(0.16 * u)} q{F(-0.04 * u)} {F(0.06 * u)} {F(-0.14 * u)} {F(0.04 * u)}" fill="none" stroke="#d8d4cc" stroke-width="{F(0.05 * u)}"/>')
    forma(z, d, m, (x - 0.26 * u, y), (x + 0.26 * u, y))
    z(f'<ellipse cx="{F(x)}" cy="{F(y - 0.42 * u)}" rx="{F(0.26 * u)}" ry="{F(0.06 * u)}" fill="#5a3018"/>'
      f'<ellipse cx="{F(x - 0.05 * u)}" cy="{F(y - 0.43 * u)}" rx="{F(0.12 * u)}" ry="{F(0.025 * u)}" fill="#c8905a" opacity="0.7"/>')
    for dx in (-0.08, 0.08):
        z(f'<path d="M{F(x + dx * u)} {F(y - 0.52 * u)} q{F(-0.08 * u)} {F(-0.15 * u)} 0 {F(-0.3 * u)} q{F(0.08 * u)} {F(-0.15 * u)} 0 {F(-0.3 * u)}" fill="none" stroke="#ffffff" stroke-width="{F(0.035 * u)}" opacity="0.45" stroke-linecap="round"/>')


# =========================================================================== bases de pose
def _de_pie(n, pj, brazos, ex="neutra", ang=0, luz=CLASE, u=108, capas=(), piernas=None, off=(0, 0), tronco=180, ancho=1.0):
    w, h = 1000, 1150
    z = IP._cuadro(n, w, h, luz)
    suelo = 1100
    Pv = (w / 2, suelo - pie_suelo(u))
    sombra_suelo(z, w / 2, suelo - 6, 1.3 * u)
    br = brazos(Pv, u) if callable(brazos) else brazos
    figura(z, Pv, u, pj, "frente", tronco=tronco, cab=dict(ex=ex, ang=ang, off=off, gafas="vista" if pj is PROFE else None),
           brazos=br, ancho=ancho,
           piernas=piernas or [dict(lado="L", a1=-3, a2=-1, pie=dict(vista="frente")), dict(lado="R", a1=4, a2=1, pie=dict(vista="frente"))],
           capas=capas)
    z.guardar()
    return _pieza(n, suelo)


def _capas_pj(pj, extra=()):
    c = list(extra)
    if pj is MARTA:
        c.append((11, camiseta_blanca))
    if pj is PROFE:
        c.append((9, falda))
    return c


CAIDOS = [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)), dict(lado="R", a1=7, a2=3, mano=dict(t="lado", c=0.45, pal=-1))]
PLANA_ARR = dict(t="plana", dorso=False, abre=7, pul_ang=45)
INDICE = dict(t="plana", dorso=True, dedos=(1, 0, 0, 0), abre=2, pul_ang=12, pul_ext=0.8)


# --------------------------------------------------------------------------- niños sentados en la silla del pupitre
KU, KESC, KALTO, KL = 100, 1.45, 0.8, 0.76   # unidad del cuerpo, escala de cabeza, alto del tronco y largo de miembros


def silla(z, Pv, u, suelo):
    """Silla escolar de frente: respaldo de madera tras la espalda, asiento y patas de tubo."""
    madera = mat("#b07a45", "#d8a46a", "#6a4422")
    tubo_c = "#5a6068"
    xs = (Pv[0] - 1.05 * u, Pv[0] + 1.05 * u)
    for x in xs:
        z(f'<path d="M{F(x)} {F(Pv[1] - 2.0 * u)} L{F(x)} {F(suelo)}" stroke="{tubo_c}" stroke-width="{F(0.09 * u)}" stroke-linecap="round"/>'
          f'<path d="M{F(x - 0.02 * u)} {F(Pv[1] - 2.0 * u)} L{F(x - 0.02 * u)} {F(suelo)}" stroke="#9aa2ac" stroke-width="{F(0.025 * u)}" opacity="0.7"/>')
    d = f"M{F(xs[0] - 0.12 * u)} {F(Pv[1] - 2.15 * u)} L{F(xs[1] + 0.12 * u)} {F(Pv[1] - 2.15 * u)} L{F(xs[1] + 0.12 * u)} {F(Pv[1] - 1.45 * u)} L{F(xs[0] - 0.12 * u)} {F(Pv[1] - 1.45 * u)} Z"
    forma(z, d, madera, (xs[0], 0), (xs[1], 0))
    z(f'<path d="M{F(xs[0] - 0.1 * u)} {F(Pv[1] - 2.12 * u)} L{F(xs[1] + 0.1 * u)} {F(Pv[1] - 2.12 * u)}" stroke="{madera["l"]}" stroke-width="3" opacity="0.7"/>')
    d = f"M{F(xs[0] - 0.15 * u)} {F(Pv[1] + 0.12 * u)} L{F(xs[1] + 0.15 * u)} {F(Pv[1] + 0.12 * u)} L{F(xs[1] + 0.1 * u)} {F(Pv[1] + 0.3 * u)} L{F(xs[0] - 0.1 * u)} {F(Pv[1] + 0.3 * u)} Z"
    forma(z, d, madera, (xs[0], 0), (xs[1], 0))


def _nino_sentado(n, pj, ex, brazos, ang=0, off=(0, 0), capas=(), luz=CLASE):
    w, h = 900, 1100
    z = IP._cuadro(n, w, h, luz)
    u = KU
    Pv = (w / 2, 640)
    suelo = Pv[1] + 0.42 * L_MUSLO * u * 0.6 + L_PIERNA * u * KL + 0.29 * u
    sombra_suelo(z, Pv[0], suelo - 4, 1.6 * u, 0.22 * u)
    silla(z, Pv, u, suelo)
    mesa = Pv[1] - 1.0 * u
    br = brazos(Pv, u, mesa)
    for b in br:
        b.setdefault("l1", KL)
        b.setdefault("l2", KL)
    figura(z, Pv, u, pj, "frente", alto=KALTO, cab=dict(ex=ex, esc=KESC, ang=ang, off=off), brazos=br,
           piernas=[dict(lado="L", a1=-10, a2=-3, l1=0.42 * 0.6 / 0.72 * KL, l2=KL, pie=dict(vista="frente")),
                    dict(lado="R", a1=10, a2=3, l1=0.42 * 0.6 / 0.72 * KL, l2=KL, pie=dict(vista="frente"))],
           capas=capas)
    z.guardar()
    return _pieza(n, suelo, mesa=mesa)


def _mesa_br(lado, x, y, ah, mano, **k):
    flex = -1 if lado == "L" else 1
    return dict(lado=lado, obj=(x, y), flex=flex, ah=ah, mano=mano, l1=0.72, l2=0.6, **k)


def marta_nina_escribe(fot):
    def br(Pv, u, mesa):
        dx = 0.0 if fot == "a" else 0.22 * u
        dy = 0.0 if fot == "a" else -0.04 * u
        return [_mesa_br("L", Pv[0] - 0.8 * u, mesa + 0.05 * u, 60, dict(t="plana", dorso=True, pulgar=1, abre=3, pul_ang=25)),
                _mesa_br("R", Pv[0] + 0.3 * u + dx, mesa + dy, -40, dict(t="lado", c=0.65, pal=-1, objeto=lambda z, W, ah: lapiz(z, W, ah, u)), z=32)]

    def papel(z, J):
        hoja_mesa(z, (J["P"][0] + 0.05 * KU, J["P"][1] - 0.85 * KU), 1.5 * KU)
    return _nino_sentado(f"marta_nina_escribe_{fot}", MARTA_NINA, "concentrada", br, ang=-4 if fot == "a" else -2, off=(0, 0.05),
                         capas=[(25, papel)])


def marta_nina_orgullosa():
    def br(Pv, u, mesa):
        return [_mesa_br("L", Pv[0] - 0.45 * u, mesa + 0.05 * u, 80, dict(t="plana", dorso=True, pulgar=1, abre=3, pul_ang=25)),
                dict(lado="R", obj=(Pv[0] + 1.25 * u, Pv[1] - 2.05 * u), flex=-1, ah=175, mano=dict(t="lado", c=0.75, pal=-1), z=34)]

    def h(z, J):
        W = J["mun_R"]
        hoja(z, (W[0] + 0.05 * KU, W[1] - 0.95 * KU), 1.15 * KU, ang=6)
    return _nino_sentado("marta_nina_orgullosa", MARTA_NINA, "sonrisa_d", br, ang=-7, capas=[(29, h)])


def marta_nina_mano():
    def br(Pv, u, mesa):
        return [_mesa_br("L", Pv[0] - 0.4 * u, mesa + 0.05 * u, 80, dict(t="plana", dorso=True, pulgar=1, abre=3, pul_ang=25)),
                dict(lado="R", a1=168, a2=176, ah=178, mano=dict(PLANA_ARR, pulgar=1, abre=4))]
    return _nino_sentado("marta_nina_mano", MARTA_NINA, "sonrisa", br, ang=-5)


def lucas_nino_reojo():
    def br(Pv, u, mesa):
        return [_mesa_br("L", Pv[0] - 0.8 * u, mesa + 0.05 * u, 60, dict(t="plana", dorso=True, pulgar=1, abre=3, pul_ang=25)),
                _mesa_br("R", Pv[0] + 0.35 * u, mesa, -40, dict(t="lado", c=0.65, pal=-1, objeto=lambda z, W, ah: lapiz(z, W, ah, u)), z=32)]

    def papel(z, J):
        hoja_mesa(z, (J["P"][0], J["P"][1] - 0.85 * KU), 1.5 * KU)
    return _nino_sentado("lucas_nino_reojo", LUCAS_NINO, EX["reojo"], br, ang=6, off=(0.08, 0), capas=[(25, papel)])


def lucas_nino_pillado():
    def br(Pv, u, mesa):
        return [dict(lado="L", a1=-35, a2=-170, ah=-178, mano=dict(PLANA_ARR, pulgar=-1, abre=8)),
                dict(lado="R", a1=35, a2=170, ah=178, mano=dict(PLANA_ARR, pulgar=1, abre=8))]
    return _nino_sentado("lucas_nino_pillado", LUCAS_NINO, EX["culpable"], br, ang=-3)


def lucas_nino_triste():
    def br(Pv, u, mesa):
        return [_mesa_br("L", Pv[0] - 0.3 * u, mesa + 0.12 * u, 80, dict(t="lado", c=0.6, pal=1)),
                _mesa_br("R", Pv[0] + 0.3 * u, mesa + 0.12 * u, -80, dict(t="lado", c=0.6, pal=-1), z=32)]
    return _nino_sentado("lucas_nino_triste", LUCAS_NINO, EX["castigado"], br, ang=5, off=(0, 0.14))


# --------------------------------------------------------------------------- profesora
def profesora_senala():
    def br(Pv, u):
        return [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)),
                dict(lado="R", a1=98, a2=94, ah=92, mano=dict(INDICE, pulgar=-1))]
    return _de_pie("profesora_senala", PROFE, br, ex="habla", ang=-4, capas=_capas_pj(PROFE))


def profesora_enfadada():
    def br(Pv, u):
        return [dict(lado="L", a1=-42, a2=42, ah=70, mano=dict(t="lado", c=0.85, pal=1)),
                dict(lado="R", a1=42, a2=-42, ah=-70, mano=dict(t="lado", c=0.85, pal=-1))]
    return _de_pie("profesora_enfadada", PROFE, br, ex=EX["enfadada"], ang=3, capas=_capas_pj(PROFE))


def profesora_aplaude(fot="a"):
    sep = 0.0 if fot == "a" else 0.32

    def br(Pv, u):
        y = Pv[1] - 1.55 * u
        return [dict(lado="L", obj=(Pv[0] - 0.12 * u - sep * u, y), flex=-1, ah=150, mano=dict(t="plana", dorso=True, pulgar=1, abre=2, pul_ang=20), z=31),
                dict(lado="R", obj=(Pv[0] + 0.12 * u + sep * u, y), flex=1, ah=210, mano=dict(t="plana", dorso=True, pulgar=-1, abre=2, pul_ang=20), z=32)]
    n = "profesora_aplaude" if fot == "a" else "profesora_aplaude_b"
    return _de_pie(n, PROFE, br, ex="rie" if fot == "a" else "sonrisa_d", ang=-3, capas=_capas_pj(PROFE))


# --------------------------------------------------------------------------- Marta adulta
def marta_piensa():
    def br(Pv, u):
        return [dict(lado="L", obj=(Pv[0] + 0.3 * u, Pv[1] - 1.05 * u), flex=-1, ah=80, mano=dict(t="lado", c=0.5, pal=1), z=31),
                dict(lado="R", obj=(Pv[0] + 0.12 * u, Pv[1] - 2.3 * u), flex=1, ah=172, mano=dict(t="lado", c=0.8, pal=-1), z=32)]
    return _de_pie("marta_piensa", MARTA, br, ex=EX["piensa"], ang=-6, capas=_capas_pj(MARTA))


def marta_idea():
    def br(Pv, u):
        return [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)),
                dict(lado="R", obj=(Pv[0] + 0.95 * u, Pv[1] - 3.35 * u), flex=-1, ah=180, mano=dict(INDICE, pulgar=1))]
    return _de_pie("marta_idea", MARTA, br, ex="sonrisa_d", ang=-4, capas=_capas_pj(MARTA))


def marta_explica(fot):
    def br(Pv, u):
        if fot == "a":
            return [dict(lado="L", a1=-22, a2=-135, ah=-150, mano=dict(PLANA_ARR, pulgar=-1, abre=7, curva=0.3)),
                    dict(lado="R", a1=22, a2=135, ah=150, mano=dict(PLANA_ARR, pulgar=1, abre=7, curva=0.3))]
        return [dict(lado="L", a1=-16, a2=-160, ah=-172, mano=dict(PLANA_ARR, pulgar=-1, abre=9, curva=0.2)),
                dict(lado="R", a1=34, a2=112, ah=125, mano=dict(PLANA_ARR, pulgar=1, abre=6, curva=0.4))]
    return _de_pie(f"marta_explica_{fot}", MARTA, br, ex="habla" if fot == "a" else "sonrisa_d", ang=-3 if fot == "a" else 3, capas=_capas_pj(MARTA))


def marta_triste():
    br = [dict(lado="L", a1=-3, a2=-1, mano=dict(t="lado", c=0.35, pal=1)), dict(lado="R", a1=3, a2=1, mano=dict(t="lado", c=0.35, pal=-1))]
    return _de_pie("marta_triste", MARTA, br, ex=EX["triste"], ang=6, off=(0, 0.1), capas=_capas_pj(MARTA), ancho=0.94)


def marta_sonrie():
    br = [dict(lado="L", a1=-58, a2=-75, ah=-95, mano=dict(PLANA_ARR, pulgar=-1, abre=9)),
          dict(lado="R", a1=58, a2=75, ah=95, mano=dict(PLANA_ARR, pulgar=1, abre=9))]
    return _de_pie("marta_sonrie", MARTA, br, ex="rie", ang=-3, capas=_capas_pj(MARTA))


def marta_entiende():
    def br(Pv, u):
        return [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)),
                dict(lado="R", obj=(Pv[0] - 0.05 * u, Pv[1] - 1.95 * u), flex=1, ah=-120, mano=dict(t="plana", dorso=True, pulgar=-1, abre=3, pul_ang=20), z=32)]
    return _de_pie("marta_entiende", MARTA, br, ex=EX["entiende"], ang=-5, capas=_capas_pj(MARTA))


def marta_delantal():
    def br(Pv, u):
        W = (Pv[0] + 1.25 * u, Pv[1] - 1.2 * u)
        return [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)),
                dict(lado="R", obj=W, flex=-1, ah=95, mano=dict(t="plana", dorso=False, pulgar=-1, abre=2, pul_ang=20,
                                                                 objeto=lambda z, W_, ah: taza(z, (W_[0] + 0.12 * u, W_[1] - 0.12 * u), u)))]
    return _de_pie("marta_delantal", MARTA, br, ex="sonrisa_d", ang=-4, capas=_capas_pj(MARTA, [(12, delantal("#3a7a4a"))]))


def _camina_pie(n, pj, fot, cab, bolsillos=False, mirar_izq=False, luz=CALLE, u=108):
    w, h = 1000, 1150
    z = IP._cuadro(n, w, h, luz)
    suelo = 1100
    Pv = (w / 2 - 20, suelo - pie_suelo(u) + 0.07 * u)
    if fot == "a":
        pn, pf, bn, bf = (24, 4, 10), (-18, -40, -22), (-22, -10), (22, 48)
    else:
        pn, pf, bn, bf = (-18, -40, -22), (24, 4, 10), (22, 48), (-22, -10)

    def dib():
        sombra_suelo(z, Pv[0] + 10, suelo - 6, 1.6 * u)
        T = lambda hh, s: IP.Tx(Pv, 182, u, hh, s)  # noqa: E731
        if bolsillos:
            brazos = [dict(lado="near", obj=T(0.45, 0.26), flex=-1, ah=20, mano=dict(t="nada")),
                      dict(lado="far", obj=T(0.5, 0.2), flex=-1, ah=20, mano=dict(t="nada"))]
        else:
            brazos = [dict(lado="near", a1=bn[0], a2=bn[1], mano=dict(t="lado", c=0.5, pal=1)),
                      dict(lado="far", a1=bf[0], a2=bf[1], mano=dict(t="lado", c=0.5, pal=1))]
        figura(z, Pv, u, pj, "perfil", tronco=182, cab=cab, brazos=brazos,
               piernas=[dict(lado="near", a1=pn[0], a2=pn[1], pie=dict(ang=pn[2])), dict(lado="far", a1=pf[0], a2=pf[1], pie=dict(ang=pf[2]))])
    if mirar_izq:
        IP.espejo(z, w / 2 - 20, dib)
    else:
        dib()
    z.guardar()
    GRUPOS.append([n[:-1] + "a", n[:-1] + "b"]) if fot == "a" else None
    return _pieza(n, suelo)


# --------------------------------------------------------------------------- Lucas adulto
def lucas_senala():
    def br(Pv, u):
        return [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)),
                dict(lado="R", obj=(Pv[0] + 2.15 * u, Pv[1] - 2.0 * u), flex=-1, ah=100, mano=dict(INDICE, pulgar=-1))]
    return _de_pie("lucas_senala", LUCAS, br, ex="sonrisa_d", ang=-6, luz=CALLE)


def lucas_delantal():
    def br(Pv, u):
        return [dict(lado="L", obj=(Pv[0] + 0.42 * u, Pv[1] - 1.5 * u), flex=-1, ah=95, mano=dict(t="lado", c=0.6, pal=1), z=31),
                dict(lado="R", obj=(Pv[0] - 0.42 * u, Pv[1] - 1.62 * u), flex=1, ah=-95, mano=dict(t="lado", c=0.6, pal=-1), z=32)]
    return _de_pie("lucas_delantal", LUCAS, br, ex="sonrisa", ang=-4, capas=[(12, delantal("#c8322a"))])


def lucas_entrega():
    def br(Pv, u):
        return [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)),
                dict(lado="R", obj=(Pv[0] + 2.2 * u, Pv[1] - 1.55 * u), flex=-1, ah=95, mano=dict(t="lado", c=0.85, pal=-1,
                                                                                                    objeto=lambda z, W, ah: bolsa(z, (W[0] + 0.3 * u, W[1] + 0.05 * u), u)))]
    return _de_pie("lucas_entrega", LUCAS, br, ex="sonrisa_d", ang=-5, capas=[(12, delantal("#c8322a"))])


def lucas_contento():
    def br(Pv, u):
        return [dict(lado="L", obj=(Pv[0] - 0.3 * u, Pv[1] - 1.0 * u), flex=-1, ah=40, mano=dict(t="lado", c=0.9, pal=1)),
                dict(lado="R", a1=135, a2=178, ah=180, mano=dict(t="lado", c=1.0, pal=-1, pc=0.8))]
    return _de_pie("lucas_contento", LUCAS, br, ex="rie", ang=-5, luz=CALLE)


# --------------------------------------------------------------------------- clientes
def cliente_confuso_1():
    def br(Pv, u):
        return [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)),
                dict(lado="R", obj=(Pv[0] + 0.75 * u, Pv[1] - 3.25 * u), flex=-1, ah=205, mano=dict(t="plana", dorso=True, pulgar=-1, abre=3, pul_ang=20, curva=0.6))]
    return _de_pie("cliente_confuso_1", CONF1, br, ex=EX["confuso"], ang=8, luz=CALLE)


def cliente_confuso_2():
    br = [dict(lado="L", a1=-22, a2=-95, ah=-100, mano=dict(PLANA_ARR, pulgar=-1, abre=8)),
          dict(lado="R", a1=22, a2=95, ah=100, mano=dict(PLANA_ARR, pulgar=1, abre=8))]
    return _de_pie("cliente_confuso_2", CONF2, br, ex=EX["encoge"], ang=-8, luz=CALLE)


def cliente_feliz(i):
    pj = FELIZ[i]
    n = f"cliente_feliz_{i + 1}"
    if i == 1:
        def br(Pv, u):
            return [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)),
                    dict(lado="R", obj=(Pv[0] + 0.85 * u, Pv[1] - 1.75 * u), flex=-1, ah=170, mano=dict(t="lado", c=0.55, pal=-1),
                         z=31)]

        def burger(z, J):
            W = J["mun_R"]
            hamburguesa(z, (W[0] + 0.05 * J["u"], W[1] - 0.45 * J["u"]), 0.42 * J["u"])
        return _de_pie(n, pj, br, ex="sonrisa_d", ang=-4, luz=CALLE, capas=[(40, burger)])

    def br(Pv, u):
        lado_b = "R" if i == 0 else "L"
        otro = dict(lado="L" if lado_b == "R" else "R", a1=-7 if lado_b == "R" else 7, a2=-3 if lado_b == "R" else 3,
                    mano=dict(t="lado", c=0.45, pal=1 if lado_b == "R" else -1))
        sg = 1 if lado_b == "R" else -1
        con = dict(lado=lado_b, a1=sg * 14, a2=sg * 28, ah=sg * 20, mano=dict(t="lado", c=0.85, pal=-sg))
        return [otro, con]

    def bols(z, J):
        lado_b = "R" if i == 0 else "L"
        W = J["mun_" + lado_b]
        sg = 1 if lado_b == "R" else -1
        bolsa(z, (W[0] + sg * 0.12 * J["u"], W[1] + 0.25 * J["u"]), J["u"], 0.9)
    return _de_pie(n, pj, br, ex="sonrisa_d" if i == 0 else "rie", ang=4 if i == 0 else -3, luz=CALLE, capas=[(25, bols)])


# --------------------------------------------------------------------------- vida diaria
def nino_regate(fot):
    n = f"nino_regate_{fot}"
    w, h, u = 1000, 950, 92
    z = IP._cuadro(n, w, h, DIA)
    suelo = 900
    l = 0.76
    A = (440, suelo - 0.29 * u)
    if fot == "a":
        tr, sa1, sa2 = 176, -6, 0
        kick = dict(lado="near", a1=-38, a2=-95, l1=l, l2=l, pie=dict(ang=-70))
        bn, bf = (55, 80), (-55, -30)
    else:
        tr, sa1, sa2 = 172, -10, -2
        kick = dict(lado="near", a1=55, a2=40, l1=l, l2=l, pie=dict(ang=25))
        bn, bf = (-45, -20), (60, 95)
    K = ad(A, D(sa2), -L_PIERNA * u * l)
    Pv = ad(K, D(sa1), -L_MUSLO * u * l)
    sombra_suelo(z, A[0] + 40, suelo - 6, 1.7 * u)
    J = figura(z, Pv, u, FUTBOL, "perfil", tronco=tr, alto=0.8, ancho=1.08, cab=dict(ex="concentrada" if fot == "a" else "sonrisa_d", esc=1.45, ang=-10, off=(-0.05, 0.22)),
               brazos=[dict(lado="near", a1=bn[0], a2=bn[1], l1=0.74, l2=0.74, mano=dict(t="lado", c=0.6, pal=1)),
                       dict(lado="far", a1=bf[0], a2=bf[1], l1=0.74, l2=0.74, mano=dict(t="lado", c=0.6, pal=1))],
               piernas=[dict(lado="far", a1=sa1, a2=sa2, l1=l, l2=l, pie=dict(ang=0)), kick])
    z.guardar()
    if fot == "a":
        GRUPOS.append(["nino_regate_a", "nino_regate_b"])
    pie = J["pie_near"]
    return _pieza(n, suelo, balon=(pie[0] + 0.75 * u, suelo - 0.42 * u))


def balon_futbol():
    n, w, h = "balon_futbol", 300, 300
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#fff4dc")
    c, r = (150, 150), 100
    sombra_suelo(z, 150, 248, 90, 14)
    g = z.rad((c[0] - 35, c[1] - 40), r * 1.45, [(0, "#ffffff"), (0.55, "#ecebe6"), (1, "#8a8f98")])
    z(f'<circle cx="150" cy="150" r="{r}" fill="{g}"/>')
    cid = z.clip(f"M50 150 A100 100 0 1 0 250 150 A100 100 0 1 0 50 150 Z")
    z(f'<g clip-path="{cid}">')

    def pent(cx, cy, s, rot):
        pts = [(cx + s * math.sin(math.radians(rot + k * 72)), cy - s * math.cos(math.radians(rot + k * 72))) for k in range(5)]
        z(f'<path d="M{" L".join(P(p) for p in pts)} Z" fill="#23262c"/>')
        for p in pts:
            q = (cx + (p[0] - cx) * 2.1, cy + (p[1] - cy) * 2.1)
            z(f'<path d="M{P(p)} L{P(q)}" stroke="#3a3e46" stroke-width="2.4"/>')
    pent(150, 150, 30, 0)
    for k in range(5):
        a = math.radians(36 + k * 72)
        pent(150 + 92 * math.sin(a), 150 - 92 * math.cos(a), 26, 36 + k * 72 + 180)
    z("</g>")
    sh = z.rad((150, 150), r, [(0, "#000", 0), (0.7, "#000", 0), (1, "#0a1020", 0.35)])
    z(f'<circle cx="150" cy="150" r="{r}" fill="{sh}"/>'
      f'<ellipse cx="112" cy="105" rx="30" ry="18" fill="#ffffff" opacity="0.55" transform="rotate(-35 112 105)"/>')
    z.guardar()
    return _pieza(n, 250)


def guitarra(z, B, ang, u):
    """Guitarra acústica: B = centro de la caja; ang = dirección del mástil (grados en pantalla, 0 = derecha, negativo = sube)."""
    k = u / 100
    z(f'<g transform="translate({F(B[0])} {F(B[1])}) rotate({F(ang)}) scale({k:.4f})">')
    caja = ("M-120 0 C-120 -50 -95 -72 -62 -70 C-38 -68 -24 -50 0 -48 C24 -50 40 -62 62 -60 C92 -58 108 -34 108 0 "
            "C108 34 92 58 62 60 C40 62 24 50 0 48 C-24 50 -38 68 -62 70 C-95 72 -120 50 -120 0 Z")
    g = z.rad((-40, -40), 170, [(0, "#f0b868"), (0.5, "#c98a3e"), (1, "#7a4a1e")])
    z(f'<path d="{caja}" fill="{g}" stroke="#4a2a10" stroke-width="3"/>'
      f'<path d="{caja}" fill="none" stroke="#f6e2c0" stroke-width="2" opacity="0.6" transform="scale(0.96)"/>')
    # mástil y clavijero
    z('<rect x="100" y="-13" width="250" height="26" rx="3" fill="#5a3420"/><rect x="100" y="-13" width="250" height="6" fill="#8a5a3a" opacity="0.8"/>')
    for i in range(9):
        x = 112 + i * 26 - i * i * 0.6
        z(f'<path d="M{F(x)} -13 L{F(x)} 13" stroke="#d8d4cc" stroke-width="2"/>')
    z('<path d="M348 -16 L410 -20 Q418 0 410 20 L348 16 Z" fill="#3a2214"/>')
    for i in range(3):
        z(f'<circle cx="{362 + i * 16}" cy="-22" r="5" fill="#d8d4cc"/><circle cx="{362 + i * 16}" cy="22" r="5" fill="#d8d4cc"/>')
    # boca, puente y cuerdas
    z('<circle cx="22" cy="0" r="26" fill="#1e120a"/><circle cx="22" cy="0" r="31" fill="none" stroke="#5a3420" stroke-width="4"/>'
      '<rect x="-80" y="-24" width="14" height="48" rx="3" fill="#3a2214"/>')
    for j in range(6):
        y = -10 + j * 4
        z(f'<path d="M-74 {y} L405 {y * 0.9}" stroke="#eeeae0" stroke-width="{1.0 + j * 0.18:.2f}" opacity="0.85"/>')
    z("</g>")


def guitarrista(fot):
    n = "guitarrista" if fot == "a" else "guitarrista_b"
    w, h, u = 1100, 1100, 104
    z = IP._cuadro(n, w, h, CLASE)
    Pv = (520, 640)
    l = 0.95
    suelo = Pv[1] + 0.6 * L_MUSLO * u * 0.55 + L_PIERNA * u * l + 0.29 * u
    sombra_suelo(z, Pv[0], suelo - 4, 1.7 * u, 0.24 * u)
    # taburete
    madera = mat("#6a4a32", "#9a7050", "#3a2618")
    for dx in (-0.85, 0.85, 0.0):
        z(f'<path d="M{F(Pv[0] + dx * 0.7 * u)} {F(Pv[1] + 0.3 * u)} L{F(Pv[0] + dx * u)} {F(suelo)}" stroke="{madera["s"] if dx == 0 else madera["b"]}" stroke-width="{F(0.13 * u)}" stroke-linecap="round"/>')
    z(f'<path d="M{F(Pv[0] - 0.85 * u)} {F(suelo - 0.9 * u)} L{F(Pv[0] + 0.85 * u)} {F(suelo - 0.9 * u)}" stroke="{madera["s"]}" stroke-width="{F(0.08 * u)}"/>')
    forma(z, f"M{F(Pv[0] - 1.0 * u)} {F(Pv[1] + 0.12 * u)} L{F(Pv[0] + 1.0 * u)} {F(Pv[1] + 0.12 * u)} L{F(Pv[0] + 0.95 * u)} {F(Pv[1] + 0.34 * u)} L{F(Pv[0] - 0.95 * u)} {F(Pv[1] + 0.34 * u)} Z",
          madera, (Pv[0] - u, 0), (Pv[0] + u, 0))
    B = (Pv[0] - 0.35 * u, Pv[1] - 0.55 * u)
    ang = -22
    cuello = ad(B, (math.cos(math.radians(ang)), math.sin(math.radians(ang))), 2.55 * u)
    rasgueo = (B[0] + 0.15 * u, B[1] - 0.2 * u) if fot == "a" else (B[0] + 0.3 * u, B[1] + 0.25 * u)

    def guit(z, J):
        guitarra(z, B, ang, u)
    figura(z, Pv, u, GUITAR, "frente", alto=0.95, cab=dict(ex="concentrada" if fot == "a" else "sonrisa", esc=1.12, ang=8, off=(0, 0.05)),
           brazos=[dict(lado="L", obj=rasgueo, flex=-1, ah=40 if fot == "a" else 70, l1=0.95, l2=0.95, mano=dict(t="lado", c=0.55, pal=1)),
                   dict(lado="R", obj=(cuello[0] - 0.05 * u, cuello[1] + 0.12 * u), flex=-1, ah=200, l1=0.95, l2=0.95, mano=dict(t="lado", c=0.75, pal=-1))],
           piernas=[dict(lado="L", a1=-12, a2=-4, l1=0.55 * l, l2=l, pie=dict(vista="frente")),
                    dict(lado="R", a1=12, a2=4, l1=0.55 * l, l2=l, pie=dict(vista="frente"))],
           capas=[(25, guit)])
    z.guardar()
    if fot == "a":
        GRUPOS.append(["guitarrista", "guitarrista_b"])
    return _pieza(n, suelo)


def cocinero_receta():
    n = "cocinero_receta"
    w, h, u = 1100, 1150, 108
    z = IP._cuadro(n, w, h, CLASE)
    suelo = 1100
    Pv = (500, suelo - pie_suelo(u))
    top = Pv[1] - 0.45 * u
    olla = (Pv[0] + 1.05 * u, top)

    def libro(z, J):
        W = J["mun_L"]
        c = (W[0] + 0.05 * u, W[1] - 0.45 * u)
        IP.libro_abierto(z, c, 1.25 * u, 12)

    def cuchara(z, J):
        W = J["mun_R"]
        p0 = (W[0] + 0.05 * u, W[1] - 0.25 * u)
        p1 = (olla[0] - 0.05 * u, olla[1] - 0.15 * u)
        z(f'<path d="M{P(p0)} L{P(p1)}" stroke="#a8743e" stroke-width="{F(0.07 * u)}" stroke-linecap="round"/>'
          f'<path d="M{P(p0)} L{P(p1)}" stroke="#d8a46a" stroke-width="{F(0.02 * u)}" stroke-linecap="round" opacity="0.7"/>')
    figura(z, Pv, u, COCINERO, "frente", cab=dict(ex=EX["lee"], ang=-6),
           brazos=[dict(lado="L", obj=(Pv[0] - 0.75 * u, Pv[1] - 1.45 * u), flex=-1, ah=170, mano=dict(t="lado", c=0.55, pal=-1), z=31),
                   dict(lado="R", obj=(olla[0] - 0.05 * u, olla[1] - 0.75 * u), flex=-1, ah=150, mano=dict(t="lado", c=0.8, pal=-1), z=32)],
           piernas=[dict(lado="L", a1=-3, a2=-1, pie=dict(vista="frente")), dict(lado="R", a1=4, a2=1, pie=dict(vista="frente"))],
           capas=[(12, delantal("#ece6d8")), (31.5, cuchara), (33, libro)])
    # cazuela con vapor sobre la encimera (delante del cocinero)
    m = mat("#6a7078", "#a8b0ba", "#2a2e34")
    x, y = olla
    vap = z.rad((x, y - 0.6 * u), 0.6 * u, [(0, "#ffffff", 0.35), (1, "#ffffff", 0)])
    z(f'<ellipse cx="{F(x)}" cy="{F(y - 0.9 * u)}" rx="{F(0.5 * u)}" ry="{F(0.6 * u)}" fill="{vap}"/>')
    d = f"M{F(x - 0.6 * u)} {F(y - 0.55 * u)} L{F(x + 0.6 * u)} {F(y - 0.55 * u)} L{F(x + 0.56 * u)} {F(y - 0.02 * u)} L{F(x - 0.56 * u)} {F(y - 0.02 * u)} Z"
    forma(z, d, m, (x - 0.6 * u, y), (x + 0.6 * u, y))
    z(f'<ellipse cx="{F(x)}" cy="{F(y - 0.55 * u)}" rx="{F(0.6 * u)}" ry="{F(0.1 * u)}" fill="#c8602a"/>'
      f'<ellipse cx="{F(x - 0.1 * u)}" cy="{F(y - 0.56 * u)}" rx="{F(0.3 * u)}" ry="{F(0.04 * u)}" fill="#e89a5a" opacity="0.7"/>'
      f'<path d="M{F(x - 0.6 * u)} {F(y - 0.4 * u)} l{F(-0.18 * u)} 0 M{F(x + 0.6 * u)} {F(y - 0.4 * u)} l{F(0.18 * u)} 0" stroke="#2a2e34" stroke-width="{F(0.07 * u)}" stroke-linecap="round"/>')
    # encimera de cocina (tapa las piernas)
    enc = mat("#d8d2c4", "#f2eee4", "#8a8478")
    frente = mat("#4a6a5a", "#6e9282", "#24382e")
    x0, x1 = Pv[0] - 2.2 * u, Pv[0] + 2.4 * u
    forma(z, f"M{F(x0)} {F(top)} L{F(x1)} {F(top)} L{F(x1)} {F(top + 0.2 * u)} L{F(x0)} {F(top + 0.2 * u)} Z", enc, (x0, top), (x1, top))
    forma(z, f"M{F(x0 + 0.1 * u)} {F(top + 0.2 * u)} L{F(x1 - 0.1 * u)} {F(top + 0.2 * u)} L{F(x1 - 0.1 * u)} {F(suelo)} L{F(x0 + 0.1 * u)} {F(suelo)} Z",
          frente, (x0, top), (x1, top))
    xm = (x0 + x1) / 2
    z(f'<path d="M{F(xm)} {F(top + 0.3 * u)} L{F(xm)} {F(suelo - 0.1 * u)}" stroke="{frente["s"]}" stroke-width="4"/>'
      f'<rect x="{F(xm - 0.5 * u)}" y="{F(top + 0.6 * u)}" width="{F(0.3 * u)}" height="{F(0.06 * u)}" rx="4" fill="#c8ccd2"/>'
      f'<rect x="{F(xm + 0.2 * u)}" y="{F(top + 0.6 * u)}" width="{F(0.3 * u)}" height="{F(0.06 * u)}" rx="4" fill="#c8ccd2"/>')
    z.guardar()
    return _pieza(n, suelo)


def bebe_habla(fot):
    n = "bebe_habla" if fot == "a" else "bebe_habla_b"
    w, h, u = 700, 700, 120
    z = IP._cuadro(n, w, h, DIA)
    suelo = 640
    Pv = (350, suelo - 0.55 * u)
    sombra_suelo(z, 350, suelo - 8, 1.7 * u, 0.3 * u)
    mano_r = dict(lado="R", a1=120, a2=160, l1=0.7, l2=0.7, ah=170, mano=dict(t="plana", dorso=False, pulgar=1, abre=10, pul_ang=45)) if fot == "a" else \
        dict(lado="R", a1=60, a2=110, l1=0.7, l2=0.7, ah=130, mano=dict(t="plana", dorso=False, pulgar=1, abre=10, pul_ang=45))
    figura(z, Pv, u * 0.6, IP.BEBE, "frente", alto=0.75, ancho=1.25, cab=dict(ex="habla" if fot == "a" else "sonrisa_d", esc=2.15, ang=-6 if fot == "a" else 4),
           brazos=[dict(lado="L", a1=-30, a2=20, l1=0.7, l2=0.7, ah=40, mano=dict(t="lado", c=0.6, pal=1)), mano_r],
           piernas=[dict(lado="L", a1=-60, a2=-20, l1=0.65, l2=0.6, z=12, pie=dict(vista="lado", dir=-1, ang=40)),
                    dict(lado="R", a1=60, a2=20, l1=0.65, l2=0.6, z=12, pie=dict(vista="lado", dir=1, ang=40))])
    z.guardar()
    if fot == "a":
        GRUPOS.append(["bebe_habla", "bebe_habla_b"])
    return _pieza(n, suelo)


def padres_hablan():
    n = "padres_hablan"
    w, h, u = 1400, 1150, 108
    z = IP._cuadro(n, w, h, DIA)
    suelo = 1100
    sombra_suelo(z, 700, suelo - 6, 3.2 * u, 0.3 * u)
    Pm = (560, suelo - pie_suelo(u) + 0.05 * u)
    Pp = (860, suelo - pie_suelo(u * 1.05))
    figura(z, Pp, u * 1.05, PADRE, "frente", cab=dict(ex="sonrisa_d", ang=-7),
           brazos=[dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)),
                   dict(lado="R", a1=7, a2=3, mano=dict(t="lado", c=0.45, pal=-1))],
           piernas=[dict(lado="L", a1=-3, a2=-1, pie=dict(vista="frente")), dict(lado="R", a1=4, a2=1, pie=dict(vista="frente"))])
    figura(z, Pm, u, MADRE, "frente", cab=dict(ex="habla", ang=6),
           brazos=[dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)),
                   dict(lado="R", a1=18, a2=145, ah=160, mano=dict(PLANA_ARR, pulgar=1, abre=7, curva=0.3))],
           piernas=[dict(lado="L", a1=-4, a2=-1, pie=dict(vista="frente")), dict(lado="R", a1=3, a2=1, pie=dict(vista="frente"))])
    z.guardar()
    return _pieza(n, suelo)


# --------------------------------------------------------------------------- caras
def caras():
    out = []
    for n, pj, ex, ang, vista in (("cara_marta_feliz", MARTA, "sonrisa_d", -4, "frente"),
                                  ("cara_marta_triste", MARTA, EX["triste"], 5, "frente"),
                                  ("cara_marta_sorpresa", MARTA, "sorpresa", -3, "frente"),
                                  ("cara_lucas_listo", LUCAS, EX["listo"], -5, "tq"),
                                  ("cara_lucas_sonrie", LUCAS, "sonrisa_d", 3, "frente")):
        capas = [(11, camiseta_blanca)] if pj is MARTA and vista == "frente" else []
        busto(n, pj, ex, vista=vista, ang=ang, luz=CLASE, capas=capas)
        out.append(_pieza(n, 900))
    return out


# =========================================================================== generar
def generar(dirsvg):
    os.makedirs(dirsvg, exist_ok=True)
    ilus.OUT = dirsvg
    META.clear()
    GRUPOS.clear()
    marta_nina_escribe("a"); marta_nina_escribe("b")
    GRUPOS.append(["marta_nina_escribe_a", "marta_nina_escribe_b"])
    marta_nina_orgullosa(); marta_nina_mano()
    lucas_nino_reojo(); lucas_nino_pillado(); lucas_nino_triste()
    profesora_senala(); profesora_enfadada(); profesora_aplaude("a"); profesora_aplaude("b")
    GRUPOS.append(["profesora_aplaude", "profesora_aplaude_b"])
    marta_piensa(); marta_idea(); marta_explica("a"); marta_explica("b")
    GRUPOS.append(["marta_explica_a", "marta_explica_b"])
    marta_triste()
    _camina_pie("marta_camina_a", MARTA, "a", dict(ex="neutra", ang=2)); _camina_pie("marta_camina_b", MARTA, "b", dict(ex="neutra", ang=2))
    marta_sonrie(); marta_entiende(); marta_delantal()
    _camina_pie("lucas_camina_a", LUCAS, "a", dict(ex="neutra", ang=2), bolsillos=True)
    _camina_pie("lucas_camina_b", LUCAS, "b", dict(ex="neutra", ang=2), bolsillos=True)
    lucas_senala(); lucas_delantal(); lucas_entrega(); lucas_contento()
    cliente_confuso_1(); cliente_confuso_2()
    _camina_pie("cliente_se_va_a", SEVA, "a", dict(ex=EX["triste"], ang=-4), mirar_izq=True)
    _camina_pie("cliente_se_va_b", SEVA, "b", dict(ex=EX["triste"], ang=-4), mirar_izq=True)
    for i in range(3):
        cliente_feliz(i)
    nino_regate("a"); nino_regate("b"); balon_futbol()
    guitarrista("a"); guitarrista("b")
    cocinero_receta(); bebe_habla("a"); bebe_habla("b"); padres_hablan()
    caras()
    info = _recortar(dirsvg)
    return info


if __name__ == "__main__":
    import json
    print(json.dumps(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"), indent=1))
