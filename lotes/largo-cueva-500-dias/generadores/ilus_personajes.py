"""Personajes del vídeo largo «500 días en una cueva» (Beatriz, Siffre, equipos, voluntarios y gente de la superficie).

Uso:  python3 -m lotes.largo-cueva-500-dias.generadores.ilus_personajes DIR   (o importar y llamar a generar(DIR))

Sistema propio de figura:
- `Lz`: lienzo con degradados únicos (prefijo «pj») y una luz principal (arriba-izquierda, cálida) + luz de borde.
- `tubo`: segmento de miembro con volumen (degradado perpendicular: luz → base → sombra → borde).
- `cabeza`: cara reutilizable en vistas frente / tq (3/4 a la derecha) / perfil (derecha) / espalda, con expresiones.
- `mano_lado`, `mano_plana`, `bota`: manos con forma de mano y calzado.
- `figura`: esqueleto (pelvis, tronco, cuello, cabeza, brazos y piernas por ángulos absolutos) que dibuja el cuerpo vestido.
Ángulos absolutos: 0 = hacia abajo, 90 = hacia la derecha, 180 = hacia arriba, -90 = hacia la izquierda.
Unidad u = altura de la cabeza; una persona adulta mide unas 7,4 u.
"""
import math, os, random, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano  # noqa: E402,F401

SOMBRA_SUELO = True  # sombra de contacto en el suelo (se puede desactivar)


# =========================================================================== utilidades
def _hx(c):
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def mix(a, b, t):
    A, B = _hx(a), _hx(b)
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(A[i] + (B[i] - A[i]) * t))) for i in range(3))


LUZC, SOMC = "#ffdcae", "#141b29"


def mat(base, luz=None, sombra=None):
    return dict(b=base, l=luz or mix(base, LUZC, 0.36), s=sombra or mix(base, SOMC, 0.5))


def oscuro(m, k=0.22):
    return dict(b=mix(m["b"], SOMC, k), l=mix(m["l"], SOMC, k), s=mix(m["s"], SOMC, k * 0.6))


def D(a):
    r = math.radians(a)
    return (math.sin(r), math.cos(r))


def ad(p, v, k=1.0):
    return (p[0] + v[0] * k, p[1] + v[1] * k)


def F(v):
    return f"{v:.1f}"


def P(p):
    return f"{p[0]:.1f} {p[1]:.1f}"


def suave(pts, cerrado=True, t=0.5):
    """Curva Catmull-Rom por los puntos → path d."""
    n = len(pts)
    if n < 3:
        return "M" + " L".join(P(p) for p in pts)
    d = "M" + P(pts[0])
    rng = range(n) if cerrado else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (cerrado or i > 0) else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (cerrado or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += f" C{P(c1)} {P(c2)} {P(p2)}"
    return d + (" Z" if cerrado else "")


class Lz:
    """Lienzo de una pieza."""

    def __init__(s, nombre, w, h, luz=(-0.6, -0.8), rim="#ffcf8a", rimk=0.85):
        s.n, s.w, s.h = nombre, w, h
        s.defs, s.b, s.k = [], [], 0
        m = math.hypot(*luz)
        s.luz = (luz[0] / m, luz[1] / m)
        s.rim, s.rimk = rim, rimk

    def id(s):
        s.k += 1
        return f"pj{s.n.replace('_', '')}{s.k}"

    @staticmethod
    def _st(stops):
        out = []
        for st in stops:
            o, c, a = (st + (1,))[:3]
            out.append(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>')
        return "".join(out)

    def lin(s, p1, p2, stops):
        i = s.id()
        s.defs.append(f'<linearGradient id="{i}" gradientUnits="userSpaceOnUse" x1="{F(p1[0])}" y1="{F(p1[1])}" '
                      f'x2="{F(p2[0])}" y2="{F(p2[1])}">{s._st(stops)}</linearGradient>')
        return f"url(#{i})"

    def rad(s, c, r, stops, foco=None):
        i = s.id()
        fx = f' fx="{F(foco[0])}" fy="{F(foco[1])}"' if foco else ""
        s.defs.append(f'<radialGradient id="{i}" gradientUnits="userSpaceOnUse" cx="{F(c[0])}" cy="{F(c[1])}" r="{F(r)}"{fx}>'
                      f'{s._st(stops)}</radialGradient>')
        return f"url(#{i})"

    def clip(s, d):
        i = s.id()
        s.defs.append(f'<clipPath id="{i}"><path d="{d}"/></clipPath>')
        return f"url(#{i})"

    def __call__(s, *partes):
        s.b.extend(partes)

    def rimc(s, m, k=0.6):
        return mix(m["l"], s.rim, 0.45 * k * s.rimk)

    def guardar(s, textura=True):
        cuerpo = "".join(s.b)
        if textura:
            s.defs.append('<filter id="pjtex" x="0" y="0" width="100%" height="100%">'
                          '<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="5" result="n"/>'
                          '<feColorMatrix in="n" type="saturate" values="0" result="g"/>'
                          '<feComponentTransfer in="g" result="a"><feFuncA type="table" tableValues="0 0.13"/></feComponentTransfer>'
                          '<feComposite in="a" in2="SourceGraphic" operator="in" result="t"/>'
                          '<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="t"/></feMerge></filter>')
            cuerpo = f'<g filter="url(#pjtex)">{cuerpo}</g>'
        guardar(s.n, cuerpo, s.w, s.h, "".join(s.defs))


# =========================================================================== volúmenes
def tubo(z, A, B, r1, r2, m, bul=0.0, tb=0.5, borde=True, op=1.0):
    """Miembro: cápsula de A (radio r1) a B (r2) con abombamiento `bul` en la posición `tb`."""
    dx, dy = B[0] - A[0], B[1] - A[1]
    d = math.hypot(dx, dy) or 1e-6
    u = (dx / d, dy / d)
    n = (-u[1], u[0])
    ri = r1 + (r2 - r1) * tb
    rc = ri + 2 * bul * max(r1, r2)
    M = ad(A, u, d * tb)
    p1, p2, p3, p4 = ad(A, n, r1), ad(B, n, r2), ad(B, n, -r2), ad(A, n, -r1)
    c1, c2 = ad(M, n, rc), ad(M, n, -rc)
    path = (f"M{P(p1)} Q{P(c1)} {P(p2)} A{F(r2)} {F(r2)} 0 0 0 {P(p3)} "
            f"Q{P(c2)} {P(p4)} A{F(r1)} {F(r1)} 0 0 0 {P(p1)} Z")
    nl = n if (n[0] * z.luz[0] + n[1] * z.luz[1]) > 0 else (-n[0], -n[1])
    R = max(r1, r2, rc) * 1.02
    g = z.lin(ad(M, nl, R), ad(M, nl, -R), [(0, m["l"]), (0.34, m["b"]), (0.78, m["s"]), (0.9, m["s"]), (1, z.rimc(m))])
    st = f' stroke="{mix(m["s"], SOMC, 0.35)}" stroke-width="{F(max(0.8, r1 * 0.04))}" stroke-opacity="0.55"' if borde else ""
    z(f'<path d="{path}" fill="{g}"{st} opacity="{op}"/>')
    return path


def forma(z, d, m, eje1, eje2, borde=True, rim=True, extra=""):
    """Rellena un path con degradado de volumen entre eje1 (lado iluminado) y eje2 (lado en sombra)."""
    g = z.lin(eje1, eje2, [(0, m["l"]), (0.36, m["b"]), (0.82, m["s"]), (0.95, m["s"]), (1, z.rimc(m) if rim else m["s"])])
    st = f' stroke="{mix(m["s"], SOMC, 0.35)}" stroke-width="1" stroke-opacity="0.5"' if borde else ""
    z(f'<path d="{d}" fill="{g}"{st}{extra}/>')


def pliegue(z, d, m, w=2.0, op=0.55):
    """Pliegue de tela: surco oscuro con labio iluminado al lado."""
    z(f'<path d="{d}" fill="none" stroke="{m["s"]}" stroke-width="{F(w)}" stroke-linecap="round" opacity="{op}"/>'
      f'<path d="{d}" fill="none" stroke="{m["l"]}" stroke-width="{F(w * 0.55)}" stroke-linecap="round" opacity="{op * 0.6}" '
      f'transform="translate({F(-w * 0.6)} {F(-w * 0.6)})"/>')


def sombra_suelo(z, x, y, rx, ry=None, op=0.42):
    if not SOMBRA_SUELO:
        return
    ry = ry or rx * 0.16
    g = z.rad((x, y), rx, [(0, "#000", op), (0.6, "#000", op * 0.5), (1, "#000", 0)])
    z(f'<ellipse cx="{F(x)}" cy="{F(y)}" rx="{F(rx)}" ry="{F(ry)}" fill="{g}" transform="translate({F(x)} {F(y)}) scale(1 {F(ry / rx)}) translate({F(-x)} {F(-y)})"/>'
      if False else f'<g transform="translate({F(x)} {F(y)}) scale(1 {ry / rx:.3f})"><circle r="{F(rx)}" fill="{z.rad((0, 0), rx, [(0, "#000", op), (0.55, "#000", op * 0.55), (1, "#000", 0)])}"/></g>')


# =========================================================================== personajes (paletas)
PIEL_BEA = dict(b="#e8b48f", s="#b97d5c", l="#f6cfae")
BEA = dict(nombre="bea", piel=PIEL_BEA, pelo="#3b2618", peinado="coleta", iris="#5b3a22", labio="#b8655a", fem=True,
           top=dict(b="#2a7f9e", l="#5fb3cf", s="#174a5e"), pant=mat("#2e3440", "#525b6b", "#191d25"),
           bota=mat("#6b4426", "#9a6a40", "#3a2212"), casco=dict(b="#e0a92e", l="#f7cf6a", s="#9a6f17"), edad=48,
           prenda="polar")
SIFFRE = dict(nombre="siffre", piel=dict(b="#e6b593", s="#b47c5a", l="#f6d0b0"), pelo="#5a3a22", peinado="corto",
              barba="#5e3b22", iris="#4a5a6a", labio="#b36a5e", fem=False, gorro="#b33a2e",
              top=mat("#6b7a3f", "#98a660", "#39421f"), pant=mat("#4a3b2e", "#6e5a46", "#271e17"),
              bota=mat("#2f241c", "#5a4636", "#17110c"), edad=23, prenda="parka")


# =========================================================================== cara
EXP = {
    "neutra": dict(ojo=1.0, mira=(0, 0), ceja=(0, 0), boca="neutra"),
    "sonrisa": dict(ojo=0.82, mira=(0, 0), ceja=(-1.5, 0), boca="sonrisa", mejilla=1),
    "sonrisa_d": dict(ojo=0.78, mira=(0, 0), ceja=(-1.5, 0), boca="sonrisa_d", mejilla=1),
    "habla": dict(ojo=1.0, mira=(0, 0), ceja=(-2.5, -1), boca="habla"),
    "rie": dict(ojo="risa", mira=(0, 0), ceja=(-3, 0), boca="risa", mejilla=1.3),
    "sorpresa": dict(ojo=1.38, mira=(0, 0), ceja=(-7, -1), boca="o"),
    "miedo": dict(ojo=1.22, mira=(1.0, 0.1), ceja=(-3.5, -4.5), boca="tensa"),
    "cerrados": dict(ojo="cerrado", mira=(0, 0), ceja=(0.5, 0), boca="serena"),
    "parpadea": dict(ojo="cerrado", mira=(0, 0), ceja=(0, 0), boca="neutra"),
    "entrecierra": dict(ojo=0.32, mira=(0, 0), ceja=(3, 1.5), boca="mueca", mejilla=0.8),
    "cansado": dict(ojo=0.6, mira=(0.3, 0.5), ceja=(0, -2), boca="triste", ojeras=1),
    "pensativo": dict(ojo=0.88, mira=(0.7, -0.7), ceja=(-1, 0), ceja2=(-4, 0), boca="pensativo"),
    "agobio": dict(ojo="apretado", mira=(0, 0), ceja=(2, -4), boca="tensa"),
    "beber": dict(ojo=0.55, mira=(0.3, -0.6), ceja=(-1, 0), boca="beber"),
    "concentrada": dict(ojo=0.62, mira=(0.2, 0.9), ceja=(0.5, -0.5), boca="neutra"),
    "feliz_ojos": dict(ojo="risa", mira=(0, 0), ceja=(-2, 0), boca="sonrisa_d", mejilla=1.2),
}

# posiciones de rasgos por vista (coordenadas locales: cabeza de 100 de alto, centro en 0,0)
VISTA = {
    "frente": dict(ojos=[(-14.5, 3, 16.5, -1), (14.5, 3, 16.5, 1)], nariz=0, boca=(0, 31.5, 9.5, 9.5), oreja=[(-36, 1, -1), (36, 1, 1)]),
    "tq": dict(ojos=[(-1.5, 3, 15, -1), (23.5, 3, 10, 1)], nariz=15, boca=(15, 31.5, 9.5, 6), oreja=[(-22, 2, -1)]),
    "perfil": dict(ojos=[(25, 2.5, 9, 1)], nariz=None, boca=(31, 31.5, 0, 5), oreja=[(-5, 3, -1)]),
    "espalda": dict(ojos=[], nariz=None, boca=None, oreja=[(27, 3, 1)]),
}

CONTORNO = {
    "frente": "M0 -50 C23 -50 37.5 -35 37.5 -10 C37.5 6 35.5 18 30.5 28 C24.5 40 13 50.5 0 50.5 C-13 50.5 -24.5 40 -30.5 28 C-35.5 18 -37.5 6 -37.5 -10 C-37.5 -35 -23 -50 0 -50 Z",
    "tq": "M-3 -50 C21 -50 35.5 -37 36.5 -15 C37 -5 35.5 2 35.5 8 C35.5 19 32.5 29 26.5 38 C20.5 46.5 12 51 4 50.5 C-6 50 -13 45 -19 38 C-24 32 -27 26 -30 20 C-38 10 -42 -10 -39 -28 C-34 -44 -20 -50 -3 -50 Z",
    "perfil": "M-6 -50 C15 -50 30 -40 33 -22 C34 -14 33 -9 34.5 -4 C35.5 -1 35 2 36.5 6 L44 18 C45.2 20.5 43 22.5 38.5 22.5 C37.5 24.5 38.5 26.5 38.6 28.5 C39 30.3 37.6 31.2 36.6 32 C38.2 33.8 37.4 36.8 35.4 38.4 C34.2 40.2 34.4 42.4 35.2 45 C35.4 49 31 52 24 52 C15 52 8 48.5 2 44 C-2 40 -5 34 -7 28 C-20 26 -35 18 -41 3 C-46 -15 -40 -37 -26 -46 C-20 -49 -14 -50 -6 -50 Z",
    "espalda": "M2 -50 C24 -50 38 -36 38.5 -14 C39 2 36 14 30 22 C24 30 14 34 4 35 C-8 35 -20 32 -28 24 C-36 14 -40 2 -39.5 -12 C-39 -36 -22 -50 2 -50 Z",
}


def _ojo(z, ex, ey, w, lado, apertura, mira, iris, piel, fem, vista, escala_iris=1.0):
    """Un ojo completo. lado: -1 ojo de la izquierda de la pantalla, +1 derecha (esquina externa hacia ese lado)."""
    out = []
    a = w / 2
    osc = "#2a1810"
    if apertura == "cerrado":
        # párpado cerrado: curva hacia abajo con pestañas
        d = f"M{F(ex - a)} {F(ey)} Q{F(ex)} {F(ey + 3.6)} {F(ex + a)} {F(ey - 0.4)}"
        out.append(f'<path d="M{F(ex - a - 1)} {F(ey - 2)} Q{F(ex)} {F(ey - 5)} {F(ex + a + 1)} {F(ey - 2.4)}" fill="none" stroke="{piel["s"]}" stroke-width="0.9" opacity="0.6"/>')
        out.append(f'<path d="{d}" fill="none" stroke="{osc}" stroke-width="1.7" stroke-linecap="round"/>')
        for k in range(4 if fem else 2):
            t = 0.25 + k * 0.18
            px = ex - a + w * t
            py = ey + 3.6 * 2 * t * (1 - t) * 1.0 + (-0.4 * t * t)
            out.append(f'<path d="M{F(px)} {F(py + 0.4)} l{F(lado * 0.4 + (t - 0.5) * 1.2)} 1.8" stroke="{osc}" stroke-width="0.6" opacity="0.7"/>')
        return "".join(out)
    if apertura == "risa":
        d = f"M{F(ex - a)} {F(ey + 1.2)} Q{F(ex)} {F(ey - 4.2)} {F(ex + a)} {F(ey + 0.8)}"
        out.append(f'<path d="{d}" fill="none" stroke="{osc}" stroke-width="1.8" stroke-linecap="round"/>')
        out.append(f'<path d="M{F(ex - a * 0.8)} {F(ey + 3.8)} Q{F(ex)} {F(ey + 2)} {F(ex + a * 0.8)} {F(ey + 3.6)}" fill="none" stroke="{piel["s"]}" stroke-width="0.9" opacity="0.7"/>')
        out.append(f'<path d="M{F(ex + lado * (a + 0.5))} {F(ey + 0.6)} l{F(lado * 2.2)} 1.6 M{F(ex + lado * (a + 0.3))} {F(ey + 1.6)} l{F(lado * 2)} 2.4" stroke="{piel["s"]}" stroke-width="0.7" opacity="0.7"/>')
        return "".join(out)
    if apertura == "apretado":
        d = f"M{F(ex - a)} {F(ey)} Q{F(ex)} {F(ey + 1.6)} {F(ex + a)} {F(ey - 0.2)}"
        out.append(f'<path d="{d}" fill="none" stroke="{osc}" stroke-width="1.8" stroke-linecap="round"/>')
        for k in range(3):
            out.append(f'<path d="M{F(ex + lado * (a - 1))} {F(ey - 2 + k * 2)} l{F(lado * 3)} {F(-1 + k)}" stroke="{piel["s"]}" stroke-width="0.8" opacity="0.7"/>')
        out.append(f'<path d="M{F(ex - a)} {F(ey - 3)} Q{F(ex)} {F(ey - 5.5)} {F(ex + a)} {F(ey - 3.4)}" fill="none" stroke="{piel["s"]}" stroke-width="0.9" opacity="0.7"/>')
        return "".join(out)
    op = float(apertura)
    hu, hl = 4.3 * op, 2.7 * op
    tip = -0.7 * lado  # la esquina externa algo más alta
    xo, xi = ex + lado * a, ex - lado * a  # externa / interna
    yo, yi = ey + tip - 0.5, ey
    if vista == "perfil":
        # ojo de perfil: forma de punta de flecha abierta hacia delante (derecha)
        d = (f"M{F(ex - 4.5)} {F(ey - 0.4)} C{F(ex - 2)} {F(ey - hu * 1.05)} {F(ex + 3)} {F(ey - hu * 1.1)} {F(ex + 4.6)} {F(ey - 0.6)} "
             f"C{F(ex + 3.4)} {F(ey + hl * 0.9)} {F(ex - 1)} {F(ey + hl * 1.1)} {F(ex - 4.5)} {F(ey - 0.4)} Z")
        cid = z.clip(d)
        out.append(f'<path d="{d}" fill="#f4ebe4"/>')
        ix, iy = ex + 2.2 + mira[0] * 0.6, ey - 0.2 + mira[1] * 1.0
        out.append(f'<g clip-path="{cid}"><ellipse cx="{F(ix)}" cy="{F(iy)}" rx="{F(1.9 * escala_iris)}" ry="{F(3.7 * escala_iris)}" fill="{iris}"/>'
                   f'<ellipse cx="{F(ix + 0.5)}" cy="{F(iy)}" rx="0.9" ry="1.9" fill="#120a06"/>'
                   f'<rect x="{F(ex - 6)}" y="{F(ey - 6)}" width="13" height="{F(2.2 + (1 - op) * 3)}" fill="{piel["s"]}" opacity="0.45"/></g>'
                   f'<circle cx="{F(ix + 0.9)}" cy="{F(iy - 1.2)}" r="0.7" fill="#fff"/>')
        out.append(f'<path d="M{F(ex - 4.6)} {F(ey - 0.4)} C{F(ex - 2)} {F(ey - hu * 1.05)} {F(ex + 3)} {F(ey - hu * 1.1)} {F(ex + 4.8)} {F(ey - 0.6)}" '
                   f'fill="none" stroke="{osc}" stroke-width="1.6" stroke-linecap="round"/>')
        if fem:
            out.append(f'<path d="M{F(ex + 4.4)} {F(ey - 0.9)} l2.2 -1.6 M{F(ex + 3.6)} {F(ey - hu * 0.8)} l1.8 -2" stroke="{osc}" stroke-width="0.7"/>')
        out.append(f'<path d="M{F(ex - 4)} {F(ey - hu - 2.2)} Q{F(ex + 0.5)} {F(ey - hu - 3.8)} {F(ex + 4)} {F(ey - hu - 1.6)}" fill="none" stroke="{piel["s"]}" stroke-width="0.8" opacity="0.65"/>')
        return "".join(out)
    d = (f"M{F(xi)} {F(yi)} C{F(ex - lado * a * 0.35)} {F(ey - hu * 1.3)} {F(ex + lado * a * 0.55)} {F(ey - hu * 1.25 + tip)} {F(xo)} {F(yo)} "
         f"C{F(ex + lado * a * 0.5)} {F(ey + hl * 1.25)} {F(ex - lado * a * 0.45)} {F(ey + hl * 1.3)} {F(xi)} {F(yi)} Z")
    cid = z.clip(d)
    # cuenca: sombra suave alrededor
    out.append(f'<ellipse cx="{F(ex)}" cy="{F(ey - 1.5)}" rx="{F(a * 1.35)}" ry="{F(5.5 + hu * 0.4)}" fill="{piel["s"]}" opacity="0.18"/>')
    out.append(f'<path d="{d}" fill="#f3e9e1"/>')
    sx = w / 15.5
    rI = 3.9 * min(1.1, max(sx, 0.75)) * escala_iris
    ix = ex + mira[0] * a * 0.42 + (lado * 0.0)
    iy = ey + 0.3 + mira[1] * 1.6
    rx_i = rI * (sx if sx < 0.9 else 1)
    g_ir = z.rad((ix, iy + rI * 0.3), rI, [(0, mix(iris, "#e8c08a", 0.35)), (0.55, iris), (0.85, mix(iris, "#000", 0.35)), (1, mix(iris, "#000", 0.6))])
    out.append(f'<g clip-path="{cid}">'
               f'<ellipse cx="{F(ix)}" cy="{F(iy)}" rx="{F(rx_i)}" ry="{F(rI)}" fill="{g_ir}"/>'
               f'<ellipse cx="{F(ix)}" cy="{F(iy)}" rx="{F(rx_i * 0.47)}" ry="{F(rI * 0.47)}" fill="#120a06"/>'
               f'<path d="M{F(xi - 2)} {F(ey - 8)} L{F(xo + 2)} {F(ey - 8)} L{F(xo + 2)} {F(ey - hu * 0.55)} Q{F(ex)} {F(ey - hu * 0.75)} {F(xi - 2)} {F(ey - hu * 0.55)} Z" fill="{piel["s"]}" opacity="0.32"/>'
               f'</g>')
    out.append(f'<circle cx="{F(ix + rx_i * 0.38)}" cy="{F(iy - rI * 0.4)}" r="{F(rI * 0.27)}" fill="#ffffff"/>'
               f'<circle cx="{F(ix - rx_i * 0.4)}" cy="{F(iy + rI * 0.4)}" r="{F(rI * 0.12)}" fill="#ffffff" opacity="0.7"/>')
    # párpado superior (línea de pestañas) y pliegue
    top = f"M{F(xi - lado * 0.3)} {F(yi + 0.2)} C{F(ex - lado * a * 0.35)} {F(ey - hu * 1.3)} {F(ex + lado * a * 0.55)} {F(ey - hu * 1.25 + tip)} {F(xo + lado * 0.6)} {F(yo + 0.1)}"
    out.append(f'<path d="{top}" fill="none" stroke="{osc}" stroke-width="{1.9 if fem else 1.5}" stroke-linecap="round"/>')
    if fem:
        out.append(f'<path d="M{F(xo)} {F(yo)} q{F(lado * 1.6)} -0.6 {F(lado * 2.6)} -2.2 M{F(xo - lado * 1.6)} {F(yo - hu * 0.45)} q{F(lado * 1.2)} -1 {F(lado * 1.6)} -2.6" '
                   f'fill="none" stroke="{osc}" stroke-width="0.8" stroke-linecap="round"/>')
    out.append(f'<path d="M{F(xi + lado * 0.5)} {F(ey - hu - 1.6)} C{F(ex - lado * a * 0.3)} {F(ey - hu * 1.3 - 3.2)} {F(ex + lado * a * 0.6)} {F(ey - hu * 1.25 - 2.6)} {F(xo - lado * 0.4)} {F(yo - 2.2)}" '
               f'fill="none" stroke="{piel["s"]}" stroke-width="1.0" opacity="0.75"/>')
    out.append(f'<path d="M{F(xi + lado * 1)} {F(yi + 0.8)} C{F(ex - lado * a * 0.3)} {F(ey + hl * 1.35)} {F(ex + lado * a * 0.5)} {F(ey + hl * 1.3)} {F(xo - lado * 0.3)} {F(yo + 0.6)}" '
               f'fill="none" stroke="{piel["s"]}" stroke-width="0.7" opacity="0.6"/>')
    out.append(f'<circle cx="{F(xi + lado * 0.6)}" cy="{F(yi + 0.2)}" r="0.8" fill="#d99088" opacity="0.8"/>')
    return "".join(out)


def _ceja(cx, cy, w, lado, dy, din, color, grosor=1.0, fem=True):
    """Ceja en forma de hoja: gruesa en la parte interna. din: subida de la parte interna (negativo = arriba)."""
    a = w / 2
    xi, xo = cx - lado * a * 0.9, cx + lado * a * 1.05
    yi, yo = cy + dy + din, cy + dy + 1.2 + din * 0.15
    ym = cy + dy - 2.6 + din * 0.35
    g1, g2 = (2.2 if fem else 3.2) * grosor, 0.8 * grosor
    d = (f"M{F(xi)} {F(yi + g1 * 0.5)} Q{F(cx + lado * a * 0.2)} {F(ym + g1 * 0.4)} {F(xo)} {F(yo + g2 * 0.4)} "
         f"Q{F(cx + lado * a * 0.25)} {F(ym - g1 * 0.6)} {F(xi - lado * 0.4)} {F(yi - g1 * 0.5)} Z")
    return f'<path d="{d}" fill="{color}" opacity="0.92"/>'


def _boca(z, vista, bx, by, wl, wr, tipo, piel, labio, fem):
    """Boca con labio superior oscuro, inferior más claro y brillo."""
    out = []
    lab_s, lab_i = mix(labio, "#5a2620", 0.25), mix(labio, "#f0a090", 0.18)
    if not fem:
        lab_s, lab_i = mix(lab_s, piel["s"], 0.55), mix(lab_i, piel["b"], 0.5)
    linea = mix(labio, "#2a0e0a", 0.55)
    xl, xr = bx - wl, bx + wr
    if vista == "perfil":
        # perfil: comisura y separación de labios; los labios ya están en el contorno
        if tipo in ("habla", "risa", "o", "tensa", "sonrisa_d", "beber"):
            ab = {"habla": 3.2, "risa": 4.5, "o": 4, "tensa": 2.2, "sonrisa_d": 1.6, "beber": 1.2}[tipo]
            out.append(f'<path d="M{F(bx)} {F(by)} Q{F(bx + 3)} {F(by - 0.6)} {F(bx + 6.5)} {F(by - 0.5)} L{F(bx + 6.5)} {F(by + ab)} Q{F(bx + 3)} {F(by + ab)} {F(bx)} {F(by + 0.6)} Z" fill="#3a1410"/>')
            if tipo in ("risa", "sonrisa_d", "habla"):
                out.append(f'<path d="M{F(bx + 2)} {F(by - 0.3)} L{F(bx + 6.4)} {F(by - 0.4)} L{F(bx + 6.4)} {F(by + 1.0)} L{F(bx + 2)} {F(by + 0.6)} Z" fill="#f4efe8"/>')
        up = -2.0 if tipo in ("sonrisa", "sonrisa_d", "risa") else (0.8 if tipo in ("triste",) else 0)
        out.append(f'<path d="M{F(bx - 1)} {F(by + up)} Q{F(bx + 2.5)} {F(by + 0.2)} {F(bx + 6)} {F(by)}" fill="none" stroke="{linea}" stroke-width="1.1" stroke-linecap="round"/>')
        out.append(f'<path d="M{F(bx + 1)} {F(by - 3.6)} Q{F(bx + 4)} {F(by - 4.6)} {F(bx + 7.2)} {F(by - 3)} L{F(bx + 7.4)} {F(by)} Q{F(bx + 3.5)} {F(by - 0.8)} {F(bx + 1)} {F(by - 0.6)} Z" fill="{lab_s}" opacity="0.85"/>'
                   f'<path d="M{F(bx + 1)} {F(by + 0.8)} Q{F(bx + 4)} {F(by + 0.6)} {F(bx + 6.4)} {F(by + 1.2)} L{F(bx + 5.6)} {F(by + 4.6)} Q{F(bx + 3)} {F(by + 5)} {F(bx + 1)} {F(by + 3.6)} Z" fill="{lab_i}" opacity="0.85"/>')
        return "".join(out)
    sh = f'<ellipse cx="{F(bx + (wr - wl) * 0.3)}" cy="{F(by + 7.5)}" rx="{F((wl + wr) * 0.32)}" ry="2.2" fill="{piel["s"]}" opacity="0.32"/>'
    if tipo in ("neutra", "serena", "pensativo", "triste", "mueca"):
        up = {"neutra": 0, "serena": -0.8, "pensativo": 0.2, "triste": 1.2, "mueca": -0.4}[tipo]
        if tipo == "pensativo":
            xl, xr = bx - wl * 0.75, bx + wr * 0.75
        ylc, yrc = by + up, by + up + (0.8 if tipo == "mueca" else 0)
        sup = (f"M{F(xl)} {F(ylc)} C{F(bx - wl * 0.6)} {F(by - 1.6)} {F(bx - wl * 0.25)} {F(by - 3.1)} {F(bx)} {F(by - 2.2)} "
               f"C{F(bx + wr * 0.25)} {F(by - 3.1)} {F(bx + wr * 0.6)} {F(by - 1.6)} {F(xr)} {F(yrc)} "
               f"C{F(bx + wr * 0.5)} {F(by + 0.3)} {F(bx - wl * 0.5)} {F(by + 0.3)} {F(xl)} {F(ylc)} Z")
        inf = (f"M{F(xl + wl * 0.12)} {F(ylc + 0.3)} C{F(bx - wl * 0.5)} {F(by + 0.4)} {F(bx + wr * 0.5)} {F(by + 0.4)} {F(xr - wr * 0.12)} {F(yrc + 0.3)} "
               f"C{F(bx + wr * 0.6)} {F(by + 4.6)} {F(bx - wl * 0.6)} {F(by + 4.6)} {F(xl + wl * 0.12)} {F(ylc + 0.3)} Z")
        out += [sh, f'<path d="{inf}" fill="{lab_i}"/>', f'<path d="{sup}" fill="{lab_s}"/>',
                f'<path d="M{F(xl)} {F(ylc)} C{F(bx - wl * 0.5)} {F(by + 0.5)} {F(bx + wr * 0.5)} {F(by + 0.5)} {F(xr)} {F(yrc)}" fill="none" stroke="{linea}" stroke-width="0.9" stroke-linecap="round"/>',
                f'<ellipse cx="{F(bx - wl * 0.15)}" cy="{F(by + 2.4)}" rx="{F(wl * 0.3)}" ry="0.8" fill="#fff" opacity="0.28"/>']
        return "".join(out)
    if tipo in ("sonrisa", "sonrisa_d"):
        ylc, yrc = by - 2.6, by - 2.6
        xl, xr = bx - wl * 1.12, bx + wr * 1.12
        ab = 3.4 if tipo == "sonrisa_d" else 0.0
        out.append(sh)
        if ab:
            boca = (f"M{F(xl)} {F(ylc)} C{F(bx - wl * 0.5)} {F(by - 0.6)} {F(bx + wr * 0.5)} {F(by - 0.6)} {F(xr)} {F(yrc)} "
                    f"C{F(bx + wr * 0.6)} {F(by + ab + 1.2)} {F(bx - wl * 0.6)} {F(by + ab + 1.2)} {F(xl)} {F(ylc)} Z")
            cid = z.clip(boca)
            out.append(f'<path d="{boca}" fill="#3a1410"/><g clip-path="{cid}"><path d="M{F(xl)} {F(by - 3)} L{F(xr)} {F(by - 3)} L{F(xr)} {F(by + 0.9)} '
                       f'Q{F(bx)} {F(by + 2.2)} {F(xl)} {F(by + 0.9)} Z" fill="#f6f1ea"/>'
                       f'<path d="M{F(bx - wl * 0.35)} {F(by - 1)} v2.8 M{F(bx + wr * 0.35)} {F(by - 1)} v2.8 M{F(bx)} {F(by - 0.8)} v3" stroke="#d8cfc4" stroke-width="0.4"/></g>')
            inf = (f"M{F(xl + 0.8)} {F(ylc + 0.8)} C{F(bx - wl * 0.6)} {F(by + ab + 1.6)} {F(bx + wr * 0.6)} {F(by + ab + 1.6)} {F(xr - 0.8)} {F(yrc + 0.8)} "
                   f"C{F(bx + wr * 0.7)} {F(by + ab + 4.6)} {F(bx - wl * 0.7)} {F(by + ab + 4.6)} {F(xl + 0.8)} {F(ylc + 0.8)} Z")
            out.append(f'<path d="{inf}" fill="{lab_i}"/>')
            sup = (f"M{F(xl)} {F(ylc)} C{F(bx - wl * 0.6)} {F(by - 3.6)} {F(bx - wl * 0.25)} {F(by - 4.6)} {F(bx)} {F(by - 3.8)} "
                   f"C{F(bx + wr * 0.25)} {F(by - 4.6)} {F(bx + wr * 0.6)} {F(by - 3.6)} {F(xr)} {F(yrc)} "
                   f"C{F(bx + wr * 0.5)} {F(by - 0.8)} {F(bx - wl * 0.5)} {F(by - 0.8)} {F(xl)} {F(ylc)} Z")
            out.append(f'<path d="{sup}" fill="{lab_s}"/>')
        else:
            sup = (f"M{F(xl)} {F(ylc)} C{F(bx - wl * 0.6)} {F(by - 2.4)} {F(bx - wl * 0.25)} {F(by - 3.6)} {F(bx)} {F(by - 2.8)} "
                   f"C{F(bx + wr * 0.25)} {F(by - 3.6)} {F(bx + wr * 0.6)} {F(by - 2.4)} {F(xr)} {F(yrc)} "
                   f"C{F(bx + wr * 0.5)} {F(by + 0.4)} {F(bx - wl * 0.5)} {F(by + 0.4)} {F(xl)} {F(ylc)} Z")
            inf = (f"M{F(xl + 1)} {F(ylc + 0.6)} C{F(bx - wl * 0.5)} {F(by + 0.6)} {F(bx + wr * 0.5)} {F(by + 0.6)} {F(xr - 1)} {F(yrc + 0.6)} "
                   f"C{F(bx + wr * 0.6)} {F(by + 4.8)} {F(bx - wl * 0.6)} {F(by + 4.8)} {F(xl + 1)} {F(ylc + 0.6)} Z")
            out += [f'<path d="{inf}" fill="{lab_i}"/>', f'<path d="{sup}" fill="{lab_s}"/>',
                    f'<path d="M{F(xl)} {F(ylc)} C{F(bx - wl * 0.5)} {F(by + 0.8)} {F(bx + wr * 0.5)} {F(by + 0.8)} {F(xr)} {F(yrc)}" fill="none" stroke="{linea}" stroke-width="1" stroke-linecap="round"/>']
        out.append(f'<ellipse cx="{F(bx - wl * 0.1)}" cy="{F(by + ab + 2.6)}" rx="{F(wl * 0.3)}" ry="0.8" fill="#fff" opacity="0.28"/>')
        # hoyuelos / pliegues nasolabiales
        out.append(f'<path d="M{F(xl - 1.2)} {F(ylc - 3.5)} q-1.4 2.6 0.2 4.6 M{F(xr + 1.2)} {F(yrc - 3.5)} q1.4 2.6 -0.2 4.6" fill="none" stroke="{piel["s"]}" stroke-width="0.9" opacity="0.7"/>')
        return "".join(out)
    if tipo in ("habla", "risa", "o", "tensa", "beber"):
        if tipo == "habla":
            xl, xr, yt, yb, yc = bx - wl * 0.95, bx + wr * 0.95, by - 2.4, by + 5.2, by - 0.8
        elif tipo == "risa":
            xl, xr, yt, yb, yc = bx - wl * 1.2, bx + wr * 1.2, by - 3.4, by + 8.0, by - 3.2
        elif tipo == "o":
            xl, xr, yt, yb, yc = bx - wl * 0.5, bx + wr * 0.5, by - 2.6, by + 5.4, by + 0.8
        elif tipo == "beber":
            xl, xr, yt, yb, yc = bx - wl * 0.45, bx + wr * 0.45, by - 1.6, by + 2.2, by + 0.2
        else:
            xl, xr, yt, yb, yc = bx - wl * 1.05, bx + wr * 1.05, by - 1.4, by + 3.4, by + 0.9
        boca = (f"M{F(xl)} {F(yc)} C{F(xl + (bx - xl) * 0.3)} {F(yt)} {F(xr - (xr - bx) * 0.3)} {F(yt)} {F(xr)} {F(yc)} "
                f"C{F(xr - (xr - bx) * 0.15)} {F(yb)} {F(xl + (bx - xl) * 0.15)} {F(yb)} {F(xl)} {F(yc)} Z")
        cid = z.clip(boca)
        out.append(sh)
        out.append(f'<path d="{boca}" fill="#3b1411"/>')
        dient = ""
        if tipo in ("habla", "risa"):
            dient = (f'<path d="M{F(xl)} {F(yt - 2)} L{F(xr)} {F(yt - 2)} L{F(xr)} {F(yt + 1.9)} Q{F(bx)} {F(yt + 2.8)} {F(xl)} {F(yt + 1.9)} Z" fill="#f5f0e8"/>'
                     f'<ellipse cx="{F(bx + (wr - wl) * 0.2)}" cy="{F(yb + 0.5)}" rx="{F((xr - xl) * 0.33)}" ry="{F((yb - yt) * 0.32)}" fill="#b4504a"/>')
        if tipo == "tensa":
            dient = (f'<path d="M{F(xl)} {F(yb - 1.4)} L{F(xr)} {F(yb - 1.4)} L{F(xr)} {F(yb + 2)} L{F(xl)} {F(yb + 2)} Z" fill="#efe8de"/>'
                     f'<path d="M{F(xl)} {F(yt - 1)} L{F(xr)} {F(yt - 1)} L{F(xr)} {F(yt + 1.1)} L{F(xl)} {F(yt + 1.1)} Z" fill="#efe8de"/>')
        out.append(f'<g clip-path="{cid}">{dient}</g>')
        # labios alrededor
        out.append(f'<path d="M{F(xl)} {F(yc)} C{F(xl + (bx - xl) * 0.3)} {F(yt)} {F(xr - (xr - bx) * 0.3)} {F(yt)} {F(xr)} {F(yc)}" fill="none" stroke="{lab_s}" stroke-width="2.4" stroke-linecap="round"/>'
                   f'<path d="M{F(xl + 0.6)} {F(yc + 0.6)} C{F(xl + (bx - xl) * 0.15)} {F(yb + 0.8)} {F(xr - (xr - bx) * 0.15)} {F(yb + 0.8)} {F(xr - 0.6)} {F(yc + 0.6)}" fill="none" stroke="{lab_i}" stroke-width="2.8" stroke-linecap="round"/>'
                   f'<ellipse cx="{F(bx)}" cy="{F(yb + 1.6)}" rx="{F((xr - xl) * 0.16)}" ry="0.6" fill="#fff" opacity="0.3"/>')
        if tipo == "risa":
            out.append(f'<path d="M{F(xl - 1.5)} {F(yc - 3.5)} q-1.6 3 0.4 5.4 M{F(xr + 1.5)} {F(yc - 3.5)} q1.6 3 -0.4 5.4" fill="none" stroke="{piel["s"]}" stroke-width="1" opacity="0.7"/>')
        return "".join(out)
    return ""


def cabeza(z, C, u, ang, pj, vista="frente", ex="neutra", casco=False, frontal=None, extra_tras="", extra_del="",
           gafas=None, pelo_mojado=False, sin_cuello=False, rasgos=True):
    """Dibuja la cabeza (con pelo, casco, gafas) centrada en C, de alto u, girada `ang` grados (0 = recta).
    frontal: None (sin lámpara), 'on' (encendida) u 'off'."""
    e = dict(EXP[ex]) if isinstance(ex, str) else ex
    piel, fem = pj["piel"], pj.get("fem", True)
    k = u / 100.0
    z(f'<g transform="translate({F(C[0])} {F(C[1])}) rotate({F(ang)}) scale({k:.4f})">')
    lx = -1 if z.luz[0] < 0 else 1
    V = VISTA[vista]
    cont = CONTORNO[vista]
    # pelo de atrás (coleta, melena)
    z(_pelo(z, pj, vista, "tras", casco, pelo_mojado))
    z(extra_tras)
    if vista == "frente":
        for (ox, oy, ls) in V["oreja"]:
            z(_oreja(z, ox, oy, ls, piel, vista))
    # cara
    g = z.rad((lx * 14, -16), 78, [(0, piel["l"]), (0.45, piel["b"]), (0.85, mix(piel["b"], piel["s"], 0.6)), (1, piel["s"])])
    z(f'<path d="{cont}" fill="{g}"/>')
    cid = z.clip(cont)
    sombra_lado = z.lin((-lx * 6, 0), (-lx * 44, 0), [(0, piel["s"], 0), (0.7, piel["s"], 0.55), (1, z.rimc(piel, 0.8), 0.9)])
    z(f'<g clip-path="{cid}"><rect x="-60" y="-60" width="120" height="120" fill="{sombra_lado}"/>')
    # rubor y sombra bajo la mandíbula
    mj = e.get("mejilla", 0)
    if vista in ("frente", "tq"):
        for (exo, eyo, ew, ls) in V["ojos"]:
            z(f'<ellipse cx="{F(exo + ls * 3)}" cy="{F(eyo + 16 - mj * 2)}" rx="{F(ew * 0.55)}" ry="{F(5 + mj)}" fill="#e88a74" opacity="{0.16 + mj * 0.08:.2f}"/>')
            if mj:
                z(f'<ellipse cx="{F(exo + ls * 1.5)}" cy="{F(eyo + 12)}" rx="{F(ew * 0.38)}" ry="3" fill="{piel["l"]}" opacity="0.5"/>')
    if pj.get("barba"):
        z(_barba(z, pj, vista))
    if e.get("ojeras"):
        for (exo, eyo, ew, ls) in V["ojos"]:
            z(f'<path d="M{F(exo - ew * 0.45)} {F(eyo + 4)} Q{F(exo)} {F(eyo + 8)} {F(exo + ew * 0.45)} {F(eyo + 4)}" fill="none" stroke="#8a5a62" stroke-width="2" opacity="0.35"/>')
    if pj.get("edad", 30) > 44 and vista != "espalda":
        for (exo, eyo, ew, ls) in V["ojos"]:
            z(f'<path d="M{F(exo + ls * (ew * 0.55 + 1))} {F(eyo + 1)} l{F(ls * 2.5)} 1.2 M{F(exo + ls * (ew * 0.55 + 0.5))} {F(eyo + 3)} l{F(ls * 2.2)} 2.4" stroke="{piel["s"]}" stroke-width="0.6" opacity="0.6"/>')
        if vista == "frente":
            z(f'<path d="M-7 21 q-4 5 -4 10 M7 21 q4 5 4 10" fill="none" stroke="{piel["s"]}" stroke-width="0.8" opacity="0.4"/>')
    z("</g>")
    # borde de luz (rim) en el lado opuesto a la luz
    z(f'<path d="{cont}" fill="none" stroke="{mix(piel["s"], "#3a2010", 0.3)}" stroke-width="0.9" opacity="0.55"/>')
    if rasgos and vista != "espalda":
        _rasgos(z, pj, vista, e)
    z(_pelo(z, pj, vista, "del", casco, pelo_mojado))
    if vista != "frente" and not pj.get("gorro"):
        for (ox, oy, ls) in V["oreja"]:
            z(_oreja(z, ox, oy, ls, piel, vista))
    if gafas == "sol":
        z(_gafas_sol(z, vista))
    elif gafas == "vista":
        z(_gafas_vista(vista))
    if pj.get("gorro"):
        z(_gorro_lana(z, pj, vista, frontal))
    if casco:
        z(_casco(z, pj, vista, frontal, casco if isinstance(casco, dict) else None))
    z(extra_del)
    z("</g>")


def _rasgos(z, pj, vista, e):
    piel, fem = pj["piel"], pj.get("fem", True)
    V = VISTA[vista]
    lx = -1 if z.luz[0] < 0 else 1
    pelo = pj.get("ceja", mix(pj["pelo"], "#000", 0.15))
    ojo = e["ojo"]
    mira = e.get("mira", (0, 0))
    if vista == "tq":
        mira = (mira[0] + 0.55, mira[1])
    for i, (exo, eyo, ew, ls) in enumerate(V["ojos"]):
        z(_ojo(z, exo, eyo, ew, ls, ojo, mira, pj["iris"], piel, fem, vista))
        cj = e.get("ceja2", e["ceja"]) if (ls > 0 and "ceja2" in e) else e["ceja"]
        if vista == "perfil":
            z(f'<path d="M{F(exo - 6)} {F(eyo - 8.5 + cj[0])} Q{F(exo + 1)} {F(eyo - 12 + cj[0] + cj[1] * 0.3)} {F(exo + 6.5)} {F(eyo - 9.5 + cj[0] + cj[1])} '
              f'L{F(exo + 6.5)} {F(eyo - 7.5 + cj[0] + cj[1])} Q{F(exo + 1)} {F(eyo - 9.6 + cj[0])} {F(exo - 6)} {F(eyo - 7.4 + cj[0])} Z" fill="{pelo}" opacity="0.9"/>')
        else:
            z(_ceja(exo, eyo - 9.5, ew * 1.08, ls, cj[0], cj[1], pelo, 1.0 if fem else 1.25, fem))
    # nariz
    if vista == "frente":
        z(f'<path d="M{F(-lx * -3.5)} -6 C{F(-lx * -4.6)} 4 {F(-lx * -6)} 12 {F(-lx * -6.5)} 17 C{F(-lx * -4)} 19 {F(-lx * -2)} 17 {F(-lx * -1)} 14 C{F(-lx * -2)} 8 {F(-lx * -2)} 0 {F(-lx * -1)} -6 Z" fill="{piel["s"]}" opacity="0.35"/>')
        z(f'<path d="M{F(lx * 1.2)} -5 C{F(lx * 1.6)} 3 {F(lx * 1.8)} 9 {F(lx * 1.6)} 14" fill="none" stroke="{piel["l"]}" stroke-width="2.2" opacity="0.55" stroke-linecap="round"/>')
        z(f'<ellipse cx="0" cy="21.2" rx="6" ry="2.2" fill="{piel["s"]}" opacity="0.32"/>'
          f'<path d="M-6.8 18.2 Q-8.2 20.6 -5.6 21.6 M6.8 18.2 Q8.2 20.6 5.6 21.6" fill="none" stroke="{piel["s"]}" stroke-width="1.1" opacity="0.9"/>'
          f'<ellipse cx="-3.1" cy="20.9" rx="1.5" ry="0.7" fill="#7a3e2e" opacity="0.5"/><ellipse cx="3.1" cy="20.9" rx="1.5" ry="0.7" fill="#7a3e2e" opacity="0.5"/>'
          f'<ellipse cx="{F(lx * 1.3)}" cy="16.4" rx="2.6" ry="1.8" fill="{piel["l"]}" opacity="0.8"/>')
    elif vista == "tq":
        nx = V["nariz"]
        z(f'<path d="M{F(nx - 5)} -4 C{F(nx - 1)} 4 {F(nx + 4)} 12 {F(nx + 8)} 18 C{F(nx + 8.5)} 20.5 {F(nx + 6)} 22 {F(nx + 3.5)} 21.5 '
          f'C{F(nx + 1.5)} 23 {F(nx - 3)} 22.5 {F(nx - 5)} 20.5 C{F(nx - 6)} 19 {F(nx - 4)} 17.5 {F(nx - 2.5)} 17.5 C{F(nx - 3)} 10 {F(nx - 5)} 3 {F(nx - 7)} -4 Z" fill="{piel["s"]}" opacity="0.42"/>')
        z(f'<path d="M{F(nx - 3)} -3 C{F(nx)} 5 {F(nx + 3)} 11 {F(nx + 6)} 16.5" fill="none" stroke="{piel["l"]}" stroke-width="2" opacity="0.55" stroke-linecap="round"/>'
          f'<ellipse cx="{F(nx + 5.6)}" cy="17.2" rx="2.4" ry="1.7" fill="{piel["l"]}" opacity="0.85"/>'
          f'<path d="M{F(nx - 4.5)} 18.4 Q{F(nx - 6.5)} 21 {F(nx - 3)} 22" fill="none" stroke="{piel["s"]}" stroke-width="1.2"/>'
          f'<ellipse cx="{F(nx + 1)}" cy="21.2" rx="2.2" ry="1" fill="#6a3426" opacity="0.75"/>'
          f'<path d="M{F(nx + 8.6)} 18.6 C{F(nx + 9.6)} 21 {F(nx + 7.6)} 22.6 {F(nx + 4)} 22.2" fill="none" stroke="{mix(piel["s"], "#3a2010", 0.3)}" stroke-width="0.9" opacity="0.8"/>')
        # mejilla del lado lejano: el contorno pasa por delante
    elif vista == "perfil":
        z(f'<path d="M30 18 Q33 22 37 21.5" fill="none" stroke="{piel["s"]}" stroke-width="1.3"/>'
          f'<ellipse cx="35.5" cy="20.6" rx="2" ry="1" fill="#6a3426" opacity="0.7"/>'
          f'<path d="M35 -2 C37 4 40 10 42 16" fill="none" stroke="{piel["l"]}" stroke-width="1.6" opacity="0.6"/>')
    bx, by, wl, wr = V["boca"]
    z(_boca(z, vista, bx, by, wl, wr, e["boca"], piel, pj.get("labio", "#b8655a"), fem))
    # barbilla y mejilla con luz
    if vista == "frente":
        z(f'<ellipse cx="{F(lx * 2)}" cy="44" rx="7" ry="3" fill="{piel["l"]}" opacity="0.2"/>')
    elif vista == "tq":
        z(f'<ellipse cx="9" cy="44" rx="7" ry="3" fill="{piel["l"]}" opacity="0.2"/>')


def _oreja(z, ox, oy, ls, piel, vista):
    if vista == "perfil":
        d = (f"M{F(ox + 4)} {F(oy - 10)} C{F(ox - 3)} {F(oy - 13)} {F(ox - 9)} {F(oy - 9)} {F(ox - 9)} {F(oy - 1)} "
             f"C{F(ox - 9)} {F(oy + 7)} {F(ox - 5)} {F(oy + 14)} {F(ox + 1)} {F(oy + 14)} C{F(ox + 4)} {F(oy + 14)} {F(ox + 5)} {F(oy + 10)} {F(ox + 4)} {F(oy + 5)} Z")
        return (f'<path d="{d}" fill="{piel["b"]}" stroke="{piel["s"]}" stroke-width="0.8"/>'
                f'<path d="M{F(ox + 1)} {F(oy - 7)} C{F(ox - 5)} {F(oy - 8)} {F(ox - 6)} {F(oy)} {F(ox - 4)} {F(oy + 6)} C{F(ox - 3)} {F(oy + 9)} {F(ox)} {F(oy + 10)} {F(ox + 1)} {F(oy + 8)}" '
                f'fill="none" stroke="{piel["s"]}" stroke-width="1.6" opacity="0.8"/>'
                f'<ellipse cx="{F(ox - 0.5)}" cy="{F(oy + 2)}" rx="2.6" ry="3.6" fill="{piel["s"]}" opacity="0.7"/>')
    if vista == "tq":
        d = (f"M{F(ox + 3)} {F(oy - 9)} C{F(ox - 3)} {F(oy - 12)} {F(ox - 7)} {F(oy - 8)} {F(ox - 7)} {F(oy - 1)} "
             f"C{F(ox - 7)} {F(oy + 7)} {F(ox - 3)} {F(oy + 13)} {F(ox + 2)} {F(oy + 13)} Z")
        return (f'<path d="{d}" fill="{piel["b"]}" stroke="{piel["s"]}" stroke-width="0.8"/>'
                f'<path d="M{F(ox + 1)} {F(oy - 6)} C{F(ox - 4)} {F(oy - 7)} {F(ox - 5)} {F(oy)} {F(ox - 3)} {F(oy + 6)}" fill="none" stroke="{piel["s"]}" stroke-width="1.4" opacity="0.8"/>'
                f'<ellipse cx="{F(ox - 0.5)}" cy="{F(oy + 2)}" rx="2" ry="3" fill="{piel["s"]}" opacity="0.6"/>')
    # frente / espalda: oreja lateral
    d = (f"M{F(ox - ls * 1.5)} {F(oy - 9)} C{F(ox + ls * 5)} {F(oy - 13)} {F(ox + ls * 8)} {F(oy - 5)} {F(ox + ls * 7)} {F(oy + 3)} "
         f"C{F(ox + ls * 6)} {F(oy + 11)} {F(ox + ls * 3)} {F(oy + 16)} {F(ox - ls * 2)} {F(oy + 15)} Z")
    return (f'<path d="{d}" fill="{mix(piel["b"], piel["s"], 0.25)}" stroke="{piel["s"]}" stroke-width="0.8"/>'
            f'<path d="M{F(ox + ls * 0.5)} {F(oy - 6)} C{F(ox + ls * 5)} {F(oy - 7)} {F(ox + ls * 5)} {F(oy + 3)} {F(ox + ls * 2.5)} {F(oy + 8)}" fill="none" stroke="{piel["s"]}" stroke-width="1.5" opacity="0.8"/>')


def _barba(z, pj, vista):
    c = pj["barba"]
    r = random.Random(17)
    if vista == "frente":
        d = ("M-35 2 C-35 18 -30 30 -24 38 C-16 48 -8 52 0 52 C8 52 16 48 24 38 C30 30 35 18 35 2 "
             "C32 10 30 20 22 24 C16 22 10 22 6 24 C4 24 2 23 0 23 C-2 23 -4 24 -6 24 C-10 22 -16 22 -22 24 C-30 20 -32 10 -35 2 Z")
        bigote = "M-12 26 C-8 22.5 -3 22.5 0 24 C3 22.5 8 22.5 12 26 C8 25.4 4 25.6 0 26.4 C-4 25.6 -8 25.4 -12 26 Z"
        hueco = "M-8 30 C-4 33 4 33 8 30 C5 36 -5 36 -8 30 Z"
    elif vista == "tq":
        d = ("M-28 18 C-24 30 -14 46 0 50 C10 52 20 46 26 38 C31 30 34 20 35.5 8 C32 16 28 22 22 24 C16 22 10 22 6 23 "
             "C2 23 -2 22 -8 22 C-14 20 -18 14 -21 6 C-24 10 -26 14 -28 18 Z")
        bigote = "M4 26 C8 22.8 14 22.4 16 24 C19 22.8 23 23.6 25 26.4 C21 25.6 18 25.8 15.5 26.6 C12 25.8 8 25.6 4 26 Z"
        hueco = "M8 30 C11 33 19 33 22 30 C20 35.5 11 35.5 8 30 Z"
    elif vista == "perfil":
        d = ("M-4 24 C0 36 10 48 20 52 C28 54 34 50 35.5 45 C35 42 34 40 35 38.5 C33 36 32 34 33 32 C30 28 26 26 24 24 "
             "C18 24 12 18 8 10 C4 14 0 18 -4 24 Z")
        bigote = "M30 23 C33 22.4 36 23 38.4 25.4 C36.5 25.8 33 25.6 30 25.4 Z"
        hueco = None
    else:
        return ""
    out = [f'<path d="{d}" fill="{c}" opacity="0.88"/>', f'<path d="{bigote}" fill="{mix(c, "#000", 0.15)}"/>']
    if hueco:
        out.append(f'<path d="{hueco}" fill="{mix(c, pj["piel"]["s"], 0.3)}" opacity="0.6"/>')
    for _ in range(40):
        x, y = r.uniform(-30, 34), r.uniform(20, 50)
        out.append(f'<path d="M{F(x)} {F(y)} l{F(r.uniform(-1, 1))} 2.4" stroke="{mix(c, "#000", 0.3)}" stroke-width="0.6" opacity="0.5"/>')
    cid = z.clip(d)
    return f'<g>{"".join(out[:2])}{out[2] if hueco else ""}<g clip-path="{cid}">{"".join(out[3 if hueco else 2:])}</g></g>'


# --------------------------------------------------------------------------- pelo
def _hebras(z, color, curvas, w=1.0, op=0.5):
    return "".join(f'<path d="{c}" fill="none" stroke="{color}" stroke-width="{F(w)}" stroke-linecap="round" opacity="{op}"/>' for c in curvas)


def _pelo(z, pj, vista, capa, casco, mojado=False):
    est = pj.get("peinado", "corto")
    c = pj["pelo"]
    if mojado:
        c = mix(c, "#000", 0.25)
    cl, cs = mix(c, "#c9a07a", 0.38), mix(c, "#000", 0.45)
    lx = -1 if z.luz[0] < 0 else 1
    gp = z.rad((lx * 12, -40), 70, [(0, cl), (0.45, c), (1, cs)])
    if est == "coleta":
        return _pelo_coleta(z, vista, capa, casco, c, cl, cs, gp, mojado)
    if pj.get("gorro"):
        if capa == "del" and vista != "espalda":
            # patillas bajo el gorro
            if vista == "frente":
                return f'<path d="M-37 -14 L-31 -14 L-31 6 Q-34 4 -37 0 Z M37 -14 L31 -14 L31 6 Q34 4 37 0 Z" fill="{c}"/>'
            if vista == "tq":
                return f'<path d="M-16 -14 L-11 -14 L-12 8 Q-15 4 -17 0 Z M-38 -10 C-40 2 -36 14 -30 18 L-26 -10 Z" fill="{c}"/>'
            return f'<path d="M-2 -14 L4 -14 L3 8 Q0 4 -2 0 Z M-41 -6 C-42 6 -36 18 -28 24 L-18 -8 Z" fill="{c}"/>'
        return ""
    return _PELOS[est](z, vista, capa, c, cl, cs, gp)


def _pelo_coleta(z, vista, capa, casco, c, cl, cs, gp, mojado):
    out = []
    if capa == "tras":
        if mojado:
            # suelto y mojado sobre los hombros
            if vista == "frente":
                d = "M-40 -20 C-46 10 -46 40 -40 66 C-30 72 -22 66 -20 58 L20 58 C22 66 30 72 40 66 C46 40 46 10 40 -20 C30 -54 -30 -54 -40 -20 Z"
                return f'<path d="{d}" fill="{gp}"/>' + _hebras(z, cs, ["M-38 0 C-42 30 -40 50 -36 64", "M38 0 C42 30 40 50 36 64", "M-32 10 C-34 36 -32 52 -28 62"], 1.4, 0.7)
            return ""
        if vista == "frente":
            # la coleta asoma por un lado detrás del cuello
            return (f'<path d="M-27 22 C-35 30 -38 42 -37 54 C-36 60 -34 63 -32 65 C-31 56 -28 46 -22 38 Z" fill="{gp}"/>'
                    + _hebras(z, cl, ["M-30 30 C-36 42 -36 56 -33 70"], 1.2, 0.5))
        if vista in ("tq", "perfil", "espalda"):
            bx, by = {"tq": (-38, -14), "perfil": (-38, -14), "espalda": (-4, -4)}[vista]
            if vista == "espalda":
                d = (f"M{bx - 8} {by} C{bx - 14} {by + 20} {bx - 12} {by + 50} {bx - 4} {by + 80} C{bx} {by + 92} {bx + 6} {by + 96} {bx + 8} {by + 98} "
                     f"C{bx + 9} {by + 80} {bx + 14} {by + 50} {bx + 10} {by + 20} C{bx + 9} {by + 8} {bx + 6} {by} {bx} {by - 2} Z")
                hs = [f"M{bx - 4} {by + 6} C{bx - 8} {by + 30} {bx - 6} {by + 60} {bx} {by + 90}",
                      f"M{bx + 4} {by + 6} C{bx + 6} {by + 30} {bx + 6} {by + 60} {bx + 6} {by + 90}",
                      f"M{bx} {by + 4} C{bx - 1} {by + 40} {bx + 2} {by + 70} {bx + 4} {by + 94}"]
            else:
                d = (f"M{bx + 4} {by - 6} C{bx - 14} {by - 8} {bx - 26} {by + 6} {bx - 28} {by + 28} C{bx - 30} {by + 50} {bx - 24} {by + 72} {bx - 14} {by + 86} "
                     f"C{bx - 16} {by + 64} {bx - 14} {by + 44} {bx - 8} {by + 28} C{bx - 4} {by + 18} {bx + 2} {by + 10} {bx + 6} {by + 8} Z")
                hs = [f"M{bx - 2} {by - 2} C{bx - 18} {by + 6} {bx - 24} {by + 40} {bx - 18} {by + 80}",
                      f"M{bx} {by + 2} C{bx - 12} {by + 14} {bx - 16} {by + 40} {bx - 12} {by + 70}",
                      f"M{bx - 4} {by} C{bx - 22} {by + 10} {bx - 28} {by + 40} {bx - 22} {by + 76}"]
            g = z.lin((bx - 30, by), (bx + 6, by + 10), [(0, cl), (0.5, c), (1, cs)])
            out.append(f'<path d="{d}" fill="{g}"/>' + _hebras(z, cl, hs[:2], 1.3, 0.55) + _hebras(z, cs, hs[2:], 1.3, 0.7))
            # goma
            gx, gy = (bx - 1, by + 4) if vista != "espalda" else (bx, by + 4)
            out.append(f'<ellipse cx="{gx}" cy="{gy}" rx="{4 if vista != "espalda" else 7}" ry="{6 if vista != "espalda" else 3.5}" fill="#1c2430" transform="rotate({-30 if vista != "espalda" else 0} {gx} {gy})"/>')
        return "".join(out)
    # capa delantera: casquete de pelo
    if mojado:
        if vista == "frente":
            d = ("M-39 -4 C-42 -30 -30 -54 0 -55 C30 -54 42 -30 39 -4 C37 -14 34 -24 26 -32 C16 -38 6 -38 -4 -35 "
                 "C-10 -30 -16 -32 -24 -30 C-32 -24 -36 -14 -39 -4 Z")
            return (f'<path d="{d}" fill="{gp}"/>' + _hebras(z, cl, ["M-30 -40 C-20 -48 0 -50 16 -46", "M-34 -24 C-24 -36 -10 -40 4 -38", "M8 -40 C20 -40 30 -32 34 -20"], 1.6, 0.55)
                    + _hebras(z, cs, ["M-37 -10 C-38 6 -40 20 -40 36", "M37 -10 C38 6 40 20 40 36", "M-4 -35 C-6 -28 -10 -24 -14 -22"], 1.4, 0.8)
                    + f'<path d="M-37 -8 C-38 10 -41 26 -42 40 L-39 40 C-37 22 -35 8 -34 -4 Z M37 -8 C38 10 41 26 42 40 L39 40 C37 22 35 8 34 -4 Z" fill="{c}"/>')
        return ""
    if casco:
        # con casco: solo se ve el pelo de las sienes
        if vista == "frente":
            return f'<path d="M-38 -16 C-37 -8 -36 -2 -34 4 C-33 -2 -32 -8 -30 -16 Z M38 -16 C37 -8 36 -2 34 4 C33 -2 32 -8 30 -16 Z" fill="{c}"/>'
        if vista == "tq":
            return (f'<path d="M-14 -18 C-14 -10 -16 -2 -19 4 C-23 0 -28 6 -31 14 C-36 6 -40 -6 -40 -18 Z" fill="{gp}"/>'
                    + _hebras(z, cl, ["M-18 -14 C-22 -6 -26 0 -30 6"], 1, 0.5))
        if vista == "perfil":
            return (f'<path d="M3 -18 C2 -10 1 -4 -1 0 C-8 4 -12 10 -16 16 C-24 18 -30 12 -40 -2 L-42 -18 Z" fill="{gp}"/>'
                    + _hebras(z, cl, ["M-2 -12 C-8 -4 -16 4 -24 8", "M-10 -14 C-18 -8 -26 -2 -34 0"], 1.1, 0.5))
        if vista == "espalda":
            return (f'<path d="M-41 -18 C-41 4 -32 24 -18 33 C-8 38 4 37 14 32 C20 26 22 16 22 6 C26 2 30 4 32 8 C35 -2 37 -12 39 -18 Z" fill="{gp}"/>'
                    + _hebras(z, cl, ["M-26 -14 C-24 4 -14 18 -4 24", "M14 -14 C12 4 8 16 2 24", "M-6 -16 C-6 2 -4 14 -2 24"], 1.2, 0.5))
        return ""
    if vista == "frente":
        d = ("M-39 -4 C-42 -30 -30 -55 0 -56 C30 -55 42 -30 39 -4 C37 -14 34 -22 28 -29 C20 -36 10 -37 -1 -36 "
             "C-6 -33 -10 -36 -16 -35 C-26 -32 -34 -20 -36 -10 Z")
        hs_l = ["M-8 -36 C-14 -42 -24 -44 -32 -34", "M-4 -36 C-4 -46 -14 -52 -26 -48", "M0 -36 C8 -48 22 -48 32 -36", "M4 -37 C14 -42 26 -40 34 -28"]
        hs_s = ["M-35 -14 C-36 -24 -30 -34 -20 -36", "M30 -26 C34 -20 37 -12 38 -6", "M-2 -36 C-4 -42 -6 -48 -6 -54"]
        brillo = "M-30 -38 C-20 -50 4 -53 22 -46 C10 -48 -10 -46 -26 -34 Z"
        return (f'<path d="{d}" fill="{gp}"/>' + _hebras(z, cl, hs_l, 1.2, 0.55) + _hebras(z, cs, hs_s, 1.2, 0.7)
                + f'<path d="{brillo}" fill="{cl}" opacity="0.45"/>'
                + f'<path d="M-36 -10 C-37 -4 -37 0 -36 4 M36 -10 C37 -4 37 0 36 4" stroke="{c}" stroke-width="2.4" fill="none"/>')
    if vista == "tq":
        d = ("M31 -30 C22 -38 8 -40 -4 -36 C-10 -30 -13 -20 -14 -10 C-15 -4 -17 0 -19 3 C-24 -1 -29 5 -31 13 "
             "C-36 16 -40 10 -41 2 C-45 -16 -39 -40 -22 -50 C-6 -57 18 -55 30 -44 C35 -40 36 -35 31 -30 Z")
        hs_l = ["M28 -36 C16 -44 -2 -44 -16 -36", "M20 -34 C8 -40 -8 -36 -18 -28", "M-6 -50 C-20 -46 -32 -36 -36 -20"]
        hs_s = ["M-14 -22 C-22 -18 -28 -12 -32 -4", "M10 -36 C0 -36 -10 -30 -16 -18", "M-28 -44 C-36 -36 -40 -22 -40 -6"]
        brillo = "M24 -44 C10 -52 -12 -50 -26 -40 C-14 -46 8 -48 24 -44 Z"
        return (f'<path d="{d}" fill="{gp}"/>' + _hebras(z, cl, hs_l, 1.2, 0.55) + _hebras(z, cs, hs_s, 1.2, 0.7)
                + f'<path d="{brillo}" fill="{cl}" opacity="0.5"/>')
    if vista == "perfil":
        d = ("M29 -32 C20 -38 10 -38 6 -30 C6 -22 5 -12 3 -4 C0 0 -2 2 -4 4 C-10 4 -14 10 -16 16 C-24 22 -32 16 -40 4 "
             "C-46 -14 -40 -38 -24 -48 C-8 -56 16 -52 28 -42 C31 -39 32 -35 29 -32 Z")
        hs_l = ["M26 -38 C14 -44 -6 -42 -22 -32", "M6 -32 C-4 -36 -18 -32 -30 -20", "M-6 -50 C-22 -44 -34 -32 -38 -16"]
        hs_s = ["M4 -20 C-6 -16 -16 -8 -22 4", "M-12 -40 C-26 -32 -36 -16 -38 0"]
        brillo = "M22 -46 C8 -52 -12 -50 -26 -40 C-14 -46 6 -48 22 -46 Z"
        return (f'<path d="{d}" fill="{gp}"/>' + _hebras(z, cl, hs_l, 1.2, 0.55) + _hebras(z, cs, hs_s, 1.2, 0.7)
                + f'<path d="{brillo}" fill="{cl}" opacity="0.5"/>')
    if vista == "espalda":
        d = ("M2 -51 C26 -51 40 -36 39 -14 C38.5 -2 36 6 32 10 C30 4 26 0 22 2 C20 12 16 24 8 33 C-4 38 -18 36 -29 27 "
             "C-37 17 -41 2 -41 -12 C-41 -36 -22 -51 2 -51 Z")
        hs_l = ["M-30 -36 C-18 -24 -10 -12 -4 -4", "M30 -36 C20 -24 10 -12 2 -4", "M0 -50 C0 -32 -2 -18 -2 -4", "M-38 -10 C-28 -6 -16 -4 -6 -2"]
        hs_s = ["M-16 -46 C-10 -30 -6 -16 -3 -6", "M16 -46 C10 -30 6 -16 2 -6", "M34 -6 C24 -4 12 -2 4 -2"]
        brillo = "M-24 -42 C-10 -50 14 -50 26 -40 C14 -44 -10 -44 -24 -42 Z"
        return (f'<path d="{d}" fill="{gp}"/>' + _hebras(z, cl, hs_l, 1.3, 0.55) + _hebras(z, cs, hs_s, 1.3, 0.7)
                + f'<path d="{brillo}" fill="{cl}" opacity="0.5"/>')
    return ""


def _p_corto(z, vista, capa, c, cl, cs, gp):
    if capa == "tras":
        return ""
    if vista == "frente":
        d = ("M-39 -2 C-42 -34 -26 -56 0 -56 C26 -56 42 -34 39 -2 C38 -12 36 -22 33 -28 C24 -32 16 -34 6 -34 "
             "C-6 -32 -18 -34 -30 -30 C-35 -24 -37 -14 -39 -2 Z")
        hs = ["M-30 -32 C-24 -44 -10 -50 4 -50", "M6 -34 C14 -44 26 -46 34 -36", "M-20 -32 C-14 -40 -4 -44 8 -44", "M-36 -16 C-36 -26 -32 -32 -26 -36"]
    elif vista == "tq":
        d = ("M33 -28 C24 -34 10 -36 -4 -34 C-10 -28 -12 -18 -13 -8 L-17 -8 C-20 -6 -24 0 -28 8 C-34 10 -40 4 -41 -6 "
             "C-44 -26 -36 -46 -18 -53 C-2 -58 22 -54 32 -42 C36 -38 36 -32 33 -28 Z")
        hs = ["M28 -36 C16 -44 -2 -44 -16 -36", "M-4 -34 C-14 -36 -26 -30 -34 -18", "M-10 -50 C-24 -46 -36 -34 -38 -16", "M20 -46 C8 -52 -6 -52 -18 -48"]
    elif vista == "perfil":
        d = ("M30 -30 C20 -36 10 -36 4 -30 C3 -22 2 -14 1 -6 L-3 -6 C-8 -2 -12 4 -14 12 C-24 16 -34 10 -40 0 "
             "C-46 -18 -38 -40 -22 -49 C-6 -56 16 -52 28 -42 C31 -39 32 -34 30 -30 Z")
        hs = ["M26 -38 C14 -44 -6 -42 -22 -32", "M2 -30 C-8 -32 -20 -26 -30 -14", "M-8 -50 C-24 -44 -36 -30 -38 -12"]
    else:
        d = "M2 -52 C26 -52 41 -36 40 -14 C39 0 36 10 30 18 C16 24 -14 24 -30 16 C-37 6 -41 -6 -41 -16 C-41 -38 -22 -52 2 -52 Z"
        hs = ["M-30 -36 C-18 -24 -10 -12 -4 4", "M30 -36 C20 -24 10 -12 2 4", "M0 -50 C0 -32 -2 -18 -2 6"]
    return f'<path d="{d}" fill="{gp}"/>' + _hebras(z, cl, hs, 1.4, 0.5) + _hebras(z, cs, [h.replace("M", "M1 ", 0)[0:0] + h for h in hs[1:2]], 1.2, 0.0)


def _p_peinado60(z, vista, capa, c, cl, cs, gp):
    """Raya al lado y tupé corto, años 60."""
    if capa == "tras":
        return ""
    if vista == "frente":
        d = ("M-39 -2 C-43 -36 -26 -60 2 -59 C30 -58 43 -34 39 -2 C38 -14 36 -24 32 -30 C20 -40 0 -42 -12 -36 "
             "C-22 -36 -30 -32 -34 -24 C-36 -16 -38 -8 -39 -2 Z")
        hs = ["M-14 -38 C-6 -50 12 -54 28 -44", "M-10 -36 C0 -46 18 -48 34 -34", "M-16 -40 C-22 -48 -30 -46 -34 -34"]
        raya = "M-14 -38 C-16 -46 -18 -52 -20 -56"
    elif vista == "tq":
        d = ("M34 -28 C26 -40 10 -42 -2 -38 C-10 -32 -12 -20 -13 -8 L-17 -8 C-20 -6 -24 0 -28 8 C-34 10 -40 4 -41 -6 "
             "C-44 -28 -36 -48 -16 -56 C2 -62 24 -56 33 -44 C37 -40 37 -34 34 -28 Z")
        hs = ["M30 -40 C18 -50 0 -50 -14 -40", "M26 -34 C12 -44 -4 -42 -16 -32", "M-6 -52 C-22 -48 -34 -34 -38 -16"]
        raya = "M-12 -46 C-18 -50 -24 -50 -30 -46"
    else:
        d = ("M31 -32 C22 -42 10 -42 4 -32 C3 -22 2 -14 1 -6 L-3 -6 C-8 -2 -12 4 -14 12 C-24 16 -34 10 -40 0 "
             "C-46 -18 -38 -42 -20 -52 C-2 -60 18 -54 29 -44 C33 -40 33 -36 31 -32 Z")
        hs = ["M28 -40 C14 -50 -6 -46 -22 -34", "M4 -32 C-8 -34 -20 -28 -30 -14", "M-8 -52 C-24 -46 -36 -30 -38 -12"]
        raya = "M-4 -50 C-14 -48 -22 -44 -28 -38"
    return f'<path d="{d}" fill="{gp}"/>' + _hebras(z, cl, hs, 1.4, 0.55) + _hebras(z, cs, [raya], 1.2, 0.8)


def _p_melena(z, vista, capa, c, cl, cs, gp):
    """Melena por los hombros con raya al lado."""
    if capa == "tras":
        if vista == "frente":
            d = "M-40 -24 C-48 6 -50 40 -46 64 C-36 70 -26 66 -22 58 L22 58 C26 66 36 70 46 64 C50 40 48 6 40 -24 C30 -56 -30 -56 -40 -24 Z"
        elif vista == "tq":
            d = "M30 -34 C40 0 38 30 30 56 L-20 60 C-36 64 -50 58 -52 46 C-52 10 -50 -20 -40 -36 C-26 -56 20 -54 30 -34 Z"
        elif vista == "perfil":
            d = "M20 -40 C10 0 6 30 4 56 C-14 64 -36 62 -52 50 C-52 14 -50 -20 -40 -36 C-30 -54 10 -56 20 -40 Z"
        else:
            d = "M-42 -24 C-48 6 -48 40 -44 62 C-20 70 20 70 44 62 C48 40 48 6 42 -24 C30 -56 -30 -56 -42 -24 Z"
        return f'<path d="{d}" fill="{gp}"/>' + _hebras(z, cs, ["M-40 0 C-44 30 -42 50 -38 62", "M40 0 C44 30 42 50 38 62", "M-30 30 C-30 44 -28 54 -26 60"], 1.3, 0.6)
    if vista == "frente":
        d = ("M-40 10 C-46 -30 -30 -56 0 -56 C30 -56 46 -30 40 10 C38 -6 36 -20 30 -28 C18 -36 0 -40 -12 -36 "
             "C-16 -30 -24 -22 -30 -14 C-34 -6 -38 2 -40 10 Z")
        hs = ["M-12 -36 C-4 -46 12 -50 26 -42", "M-12 -36 C-22 -28 -30 -16 -36 0", "M-8 -38 C4 -42 20 -40 32 -26", "M-14 -40 C-24 -46 -34 -40 -38 -26"]
    elif vista == "tq":
        d = ("M33 -28 C24 -38 8 -40 -6 -36 C-12 -28 -14 -18 -15 -6 C-17 4 -20 14 -22 26 C-30 30 -40 22 -44 8 "
             "C-48 -20 -38 -46 -18 -54 C2 -60 24 -54 33 -42 C37 -38 37 -32 33 -28 Z")
        hs = ["M28 -38 C14 -46 -4 -44 -16 -34", "M-8 -36 C-18 -24 -22 -8 -24 14", "M-10 -50 C-26 -44 -38 -28 -42 -8"]
    elif vista == "perfil":
        d = ("M29 -32 C20 -40 10 -38 6 -30 C6 -20 5 -10 2 0 C-2 10 -6 20 -8 30 C-20 34 -34 26 -42 10 "
             "C-48 -14 -40 -40 -22 -50 C-6 -58 16 -52 28 -42 C31 -39 32 -35 29 -32 Z")
        hs = ["M26 -38 C14 -44 -6 -42 -22 -32", "M4 -28 C0 -10 -4 10 -8 26", "M-8 -50 C-24 -44 -36 -30 -40 -10"]
    else:
        d = "M2 -52 C28 -52 44 -34 44 -10 C44 20 42 44 40 60 C14 66 -14 66 -40 60 C-42 40 -44 20 -44 -10 C-44 -36 -24 -52 2 -52 Z"
        hs = ["M-30 -36 C-30 0 -28 30 -26 58", "M30 -36 C30 0 28 30 26 58", "M0 -50 C0 -10 0 30 0 60", "M-14 -46 C-14 -6 -12 30 -12 60"]
    return f'<path d="{d}" fill="{gp}"/>' + _hebras(z, cl, hs, 1.3, 0.5) + _hebras(z, cs, hs[1:2], 1.3, 0.6)


def _p_rizado(z, vista, capa, c, cl, cs, gp):
    """Pelo rizado corto-medio (volumen redondeado con bucles)."""
    r = random.Random(33)
    if capa == "tras":
        if vista in ("frente", "espalda"):
            pts = [(math.cos(t) * 50, math.sin(t) * 46 - 16) for t in [i * math.pi * 2 / 22 for i in range(22)]]
            pts = [p for p in pts]
            d = "M" + " ".join(f"{F(p[0])} {F(p[1])}" for p in pts) + " Z"
            out = [f'<path d="{suave(pts)}" fill="{gp}"/>']
            for i in range(22):
                t = i * math.pi * 2 / 22
                x, y = math.cos(t) * 48, math.sin(t) * 44 - 16
                if y < 30:
                    out.append(f'<circle cx="{F(x)}" cy="{F(y)}" r="{F(r.uniform(7, 10))}" fill="{c}"/><path d="M{F(x - 4)} {F(y)} a4 4 0 1 1 6 3" fill="none" stroke="{cl}" stroke-width="1.2" opacity="0.6"/>')
            return "".join(out)
        return ""
    if vista in ("frente", "tq"):
        sh = 8 if vista == "tq" else 0
        out = []
        for i in range(14):
            t = math.pi + i * math.pi / 13
            x, y = math.cos(t) * 40 + sh * (1 + math.cos(t)) * 0.3, math.sin(t) * 30 - 30
            rr = r.uniform(7, 11)
            out.append(f'<circle cx="{F(x)}" cy="{F(y)}" r="{F(rr)}" fill="{gp}"/>'
                       f'<path d="M{F(x - rr * 0.5)} {F(y + rr * 0.1)} a{F(rr * 0.5)} {F(rr * 0.5)} 0 1 1 {F(rr * 0.7)} {F(rr * 0.35)}" fill="none" stroke="{cl}" stroke-width="1.3" opacity="0.6"/>'
                       f'<path d="M{F(x - rr * 0.6)} {F(y + rr * 0.5)} a{F(rr * 0.6)} {F(rr * 0.4)} 0 0 0 {F(rr * 1.1)} 0" fill="none" stroke="{cs}" stroke-width="1.2" opacity="0.6"/>')
        return "".join(out)
    return _p_corto(z, vista, capa, c, cl, cs, gp)


def _p_mono(z, vista, capa, c, cl, cs, gp):
    """Pelo recogido en moño alto."""
    if capa == "tras":
        if vista == "frente":
            return f'<ellipse cx="4" cy="-58" rx="18" ry="14" fill="{gp}"/>' + _hebras(z, cl, ["M-8 -62 C0 -70 10 -68 16 -60", "M-10 -56 C0 -50 12 -52 18 -58"], 1.2, 0.6)
        if vista in ("tq", "perfil"):
            return f'<ellipse cx="-24" cy="-50" rx="16" ry="14" fill="{gp}"/>' + _hebras(z, cl, ["M-36 -52 C-30 -62 -16 -62 -12 -52"], 1.2, 0.6)
        return f'<ellipse cx="0" cy="-46" rx="17" ry="14" fill="{gp}"/>'
    return _pelo_coleta(z, vista, "del", False, c, cl, cs, gp, False)


def _p_calvo(z, vista, capa, c, cl, cs, gp):
    """Coronilla calva con pelo corto en los lados."""
    if capa == "tras":
        return ""
    if vista == "frente":
        d = "M-38 -24 C-40 -14 -39 -4 -37 6 L-33 6 C-34 -6 -34 -16 -32 -26 Z M38 -24 C40 -14 39 -4 37 6 L33 6 C34 -6 34 -16 32 -26 Z"
    elif vista == "tq":
        d = "M-14 -20 C-14 -10 -16 -2 -19 4 C-24 0 -28 6 -31 14 C-38 10 -42 -4 -41 -22 C-34 -26 -22 -24 -14 -20 Z"
    else:
        d = "M2 -22 C2 -14 1 -6 -2 0 C-8 4 -12 10 -14 14 C-26 16 -36 8 -41 -4 C-42 -12 -42 -18 -40 -24 C-26 -28 -10 -26 2 -22 Z"
    return f'<path d="{d}" fill="{gp}"/>' + f'<ellipse cx="-6" cy="-40" rx="14" ry="6" fill="#ffffff" opacity="0.14"/>'


def _p_nino(z, vista, capa, c, cl, cs, gp):
    if capa == "tras":
        return ""
    if vista == "frente":
        d = ("M-40 -4 C-44 -36 -26 -58 0 -58 C26 -58 44 -36 40 -4 C38 -14 35 -22 30 -26 L24 -22 L22 -30 L12 -24 L8 -32 L-2 -26 L-6 -34 "
             "L-14 -26 L-20 -32 L-26 -22 C-32 -20 -36 -12 -40 -4 Z")
        hs = ["M-26 -36 C-14 -48 4 -52 20 -44", "M-8 -30 C0 -42 12 -46 26 -38"]
    elif vista in ("tq", "perfil"):
        d = ("M34 -28 L28 -24 L28 -32 L18 -28 L16 -36 L6 -30 L2 -38 L-6 -30 C-10 -24 -12 -16 -13 -8 L-17 -8 C-22 -4 -26 2 -28 8 "
             "C-36 10 -42 2 -42 -8 C-44 -30 -34 -50 -14 -57 C4 -62 26 -54 34 -40 C36 -36 36 -32 34 -28 Z")
        hs = ["M26 -40 C12 -50 -6 -50 -20 -42", "M-4 -32 C-16 -32 -28 -24 -36 -10"]
    else:
        d = "M2 -54 C28 -54 42 -36 40 -14 C38 2 34 14 28 20 C14 26 -14 26 -30 18 C-38 8 -42 -6 -42 -16 C-42 -40 -22 -54 2 -54 Z"
        hs = ["M-30 -36 C-18 -24 -10 -12 -4 4"]
    return f'<path d="{d}" fill="{gp}"/>' + _hebras(z, cl, hs, 1.6, 0.55)


def _p_bebe(z, vista, capa, c, cl, cs, gp):
    if capa == "tras":
        return ""
    return (f'<path d="M-24 -42 C-14 -54 12 -56 24 -44 C14 -48 -12 -48 -24 -42 Z" fill="{c}" opacity="0.8"/>'
            f'<path d="M-2 -50 C2 -58 10 -60 12 -54 C8 -56 4 -54 2 -48" fill="{c}"/>')


_PELOS = {"corto": _p_corto, "peinado60": _p_peinado60, "melena": _p_melena, "rizado": _p_rizado, "mono": _p_mono,
          "calvo": _p_calvo, "nino": _p_nino, "bebe": _p_bebe}


# --------------------------------------------------------------------------- casco, gorro, gafas
def _lampara(cx, cy, w, h, on, z, vista):
    out = [f'<rect x="{F(cx - w / 2)}" y="{F(cy - h / 2)}" width="{F(w)}" height="{F(h)}" rx="{F(h * 0.3)}" fill="#22262d"/>',
           f'<rect x="{F(cx - w / 2)}" y="{F(cy - h / 2)}" width="{F(w)}" height="{F(h * 0.35)}" rx="{F(h * 0.2)}" fill="#4a505a" opacity="0.8"/>']
    lr = h * 0.36
    lxc = cx + (w * 0.28 if vista in ("tq", "perfil") else 0)
    if on:
        g = z.rad((lxc, cy), lr * 9, [(0, "#fffbe8", 0.85), (0.15, "#ffe7b0", 0.5), (0.5, "#ffcf8a", 0.15), (1, "#ffcf8a", 0)])
        out.append(f'<circle cx="{F(lxc)}" cy="{F(cy)}" r="{F(lr * 9)}" fill="{g}"/>')
        out.append(f'<circle cx="{F(lxc)}" cy="{F(cy)}" r="{F(lr)}" fill="#fffef6"/><circle cx="{F(lxc)}" cy="{F(cy)}" r="{F(lr * 1.25)}" fill="none" stroke="#c9ccd2" stroke-width="1"/>')
    else:
        g = z.rad((lxc - lr * 0.3, cy - lr * 0.3), lr, [(0, "#d9e4ee"), (0.6, "#8a96a4"), (1, "#3a414b")])
        out.append(f'<circle cx="{F(lxc)}" cy="{F(cy)}" r="{F(lr)}" fill="{g}"/><circle cx="{F(lxc)}" cy="{F(cy)}" r="{F(lr * 1.25)}" fill="none" stroke="#9aa2ad" stroke-width="1"/>')
    return "".join(out)


def _casco(z, pj, vista, frontal, colores=None):
    cc = colores or pj.get("casco", dict(b="#e0a92e", l="#f7cf6a", s="#9a6f17"))
    lx = -1 if z.luz[0] < 0 else 1
    g = z.rad((lx * 16, -58), 72, [(0, cc["l"]), (0.5, cc["b"]), (1, cc["s"])])
    on = frontal == "on"
    out = []
    if vista == "frente":
        sh = "M-46 -20 C-49 -50 -30 -70 0 -71 C30 -70 49 -50 46 -20 C44 -16 40 -15 36 -17 C20 -22 -20 -22 -36 -17 C-40 -15 -44 -16 -46 -20 Z"
        out += [f'<path d="M-40 -18 C-40 4 -36 26 -24 42 M40 -18 C40 4 36 26 24 42" fill="none" stroke="#1d2129" stroke-width="2.2"/>',
                f'<path d="{sh}" fill="{g}"/>',
                f'<path d="M-46 -20 C-44 -16 -40 -15 -36 -17 C-20 -22 20 -22 36 -17 C40 -15 44 -16 46 -20" fill="none" stroke="{cc["s"]}" stroke-width="3"/>',
                f'<path d="M-20 -66 C-14 -50 -12 -36 -12 -22 M20 -66 C14 -50 12 -36 12 -22" fill="none" stroke="{cc["s"]}" stroke-width="1.6" opacity="0.6"/>',
                f'<path d="M-30 -60 C-20 -68 0 -70 16 -66" fill="none" stroke="#fff6d8" stroke-width="3" opacity="0.5" stroke-linecap="round"/>',
                f'<path d="M-45 -30 C-30 -36 30 -36 45 -30" fill="none" stroke="#1d2129" stroke-width="4" opacity="0.9"/>',
                _lampara(0, -33, 20, 12, on, z, vista)]
    elif vista == "tq":
        sh = "M-46 -16 C-50 -48 -30 -70 -2 -71 C26 -71 44 -54 44 -22 C42 -17 37 -16 32 -18 C14 -23 -18 -23 -34 -16 C-40 -12 -44 -12 -46 -16 Z"
        out += [f'<path d="M-30 -16 C-28 6 -22 24 -12 40 Q-4 48 6 50" fill="none" stroke="#1d2129" stroke-width="2.2"/>',
                f'<path d="{sh}" fill="{g}"/>',
                f'<path d="M-46 -16 C-44 -12 -40 -12 -34 -16 C-18 -23 14 -23 32 -18 C37 -16 42 -17 44 -22" fill="none" stroke="{cc["s"]}" stroke-width="3"/>',
                f'<path d="M-6 -68 C2 -52 4 -38 4 -22 M-30 -62 C-28 -48 -26 -34 -26 -20" fill="none" stroke="{cc["s"]}" stroke-width="1.6" opacity="0.6"/>',
                f'<path d="M-30 -58 C-20 -68 -2 -71 14 -67" fill="none" stroke="#fff6d8" stroke-width="3" opacity="0.5" stroke-linecap="round"/>',
                f'<path d="M-46 -28 C-30 -34 20 -36 44 -30" fill="none" stroke="#1d2129" stroke-width="4" opacity="0.9"/>',
                _lampara(16, -33, 20, 12, on, z, vista)]
    elif vista == "perfil":
        sh = "M-48 -14 C-52 -46 -32 -70 -4 -71 C22 -71 40 -54 40 -26 C40 -20 36 -18 32 -20 C14 -24 -20 -22 -38 -14 C-42 -12 -46 -11 -48 -14 Z"
        out += [f'<path d="M-6 -18 C-6 4 -2 22 6 40 Q12 50 22 52" fill="none" stroke="#1d2129" stroke-width="2.2"/>',
                f'<path d="{sh}" fill="{g}"/>',
                f'<path d="M-48 -14 C-46 -11 -42 -12 -38 -14 C-20 -22 14 -24 32 -20 C36 -18 40 -20 40 -26" fill="none" stroke="{cc["s"]}" stroke-width="3"/>',
                f'<path d="M-16 -68 C-10 -52 -8 -38 -8 -22 M-36 -60 C-36 -46 -36 -32 -36 -18" fill="none" stroke="{cc["s"]}" stroke-width="1.6" opacity="0.6"/>',
                f'<path d="M-34 -58 C-24 -68 -6 -71 10 -67" fill="none" stroke="#fff6d8" stroke-width="3" opacity="0.5" stroke-linecap="round"/>',
                f'<path d="M-48 -26 C-30 -32 10 -34 40 -32" fill="none" stroke="#1d2129" stroke-width="4" opacity="0.9"/>',
                _lampara(36, -32, 16, 13, on, z, vista)]
    else:  # espalda (3/4 de espaldas mirando a la derecha)
        sh = "M-44 -18 C-46 -50 -26 -70 2 -71 C30 -70 48 -50 46 -18 C42 -14 36 -14 30 -16 C12 -20 -20 -20 -36 -16 C-40 -14 -42 -14 -44 -18 Z"
        out += [f'<path d="M36 -16 C36 6 32 24 24 38" fill="none" stroke="#1d2129" stroke-width="2.2"/>',
                f'<path d="{sh}" fill="{g}"/>',
                f'<path d="M-44 -18 C-42 -14 -36 -14 -30 -16 C-12 -20 12 -20 30 -16 C36 -14 42 -14 46 -18" fill="none" stroke="{cc["s"]}" stroke-width="3"/>',
                f'<path d="M-36 -26 C-20 -34 20 -34 46 -28" fill="none" stroke="#1d2129" stroke-width="4" opacity="0.9"/>',
                f'<rect x="-10" y="-34" width="18" height="8" rx="3" fill="#22262d"/>',
                f'<path d="M-24 -62 C-12 -70 8 -70 22 -64" fill="none" stroke="#fff6d8" stroke-width="3" opacity="0.5" stroke-linecap="round"/>']
        if on:
            gg = z.rad((50, -30), 22, [(0, "#fff3d0", 0.7), (1, "#ffcf8a", 0)])
            out.append(f'<circle cx="50" cy="-30" r="22" fill="{gg}"/>')
    return "".join(out)


def _gorro_lana(z, pj, vista, frontal):
    c = pj["gorro"]
    m = mat(c)
    lx = -1 if z.luz[0] < 0 else 1
    g = z.rad((lx * 14, -50), 70, [(0, m["l"]), (0.5, m["b"]), (1, m["s"])])
    out = []
    if vista == "frente":
        sh = "M-41 -12 C-44 -46 -26 -66 0 -66 C26 -66 44 -46 41 -12 Z"
        vu = "M-42 -24 C-20 -30 20 -30 42 -24 L42 -10 C20 -15 -20 -15 -42 -10 Z"
    elif vista == "tq":
        sh = "M-44 -8 C-48 -44 -28 -66 -2 -66 C24 -66 40 -48 38 -14 Z"
        vu = "M-45 -20 C-24 -28 16 -30 39 -26 L38 -12 C16 -16 -24 -14 -45 -6 Z"
    elif vista == "perfil":
        sh = "M-46 -6 C-50 -42 -30 -66 -4 -66 C22 -66 36 -48 34 -16 Z"
        vu = "M-47 -18 C-26 -26 12 -30 35 -28 L34 -14 C12 -16 -26 -12 -47 -4 Z"
    else:
        sh = "M-42 -10 C-44 -46 -24 -66 2 -66 C28 -66 46 -46 42 -10 Z"
        vu = "M-43 -22 C-20 -28 20 -28 43 -22 L42 -8 C20 -13 -20 -13 -43 -8 Z"
    out.append(f'<path d="{sh}" fill="{g}"/>')
    cid = z.clip(sh)
    out.append(f'<g clip-path="{cid}">' + "".join(
        f'<path d="M{x} -70 C{x + 2} -50 {x + 1} -30 {x} -10" fill="none" stroke="{m["s"]}" stroke-width="2.2" opacity="0.45"/>' for x in range(-44, 46, 7)) + "</g>")
    out.append(f'<path d="{vu}" fill="{m["b"]}"/><path d="{vu}" fill="none" stroke="{m["s"]}" stroke-width="1"/>')
    vid = z.clip(vu)
    out.append(f'<g clip-path="{vid}">' + "".join(f'<path d="M{x} -32 L{x} -4" stroke="{m["s"]}" stroke-width="1.8" opacity="0.6"/>' for x in range(-46, 46, 4)) + "</g>")
    if frontal:
        # frontal antiguo: cinta y foco redondo de latón
        if vista == "frente":
            fx, fy = 0, -40
        elif vista == "tq":
            fx, fy = 14, -40
        elif vista == "perfil":
            fx, fy = 32, -40
        else:
            fx, fy = None, None
        out.append(f'<path d="M-44 -40 C-20 -46 20 -46 44 -40" fill="none" stroke="#2b2622" stroke-width="5"/>')
        if fx is not None:
            gb = z.rad((fx - 3, fy - 3), 12, [(0, "#f2d38a"), (0.6, "#a8822e"), (1, "#5a4214")])
            out.append(f'<circle cx="{fx}" cy="{fy}" r="11" fill="{gb}"/>')
            if frontal == "on":
                gg = z.rad((fx + (5 if vista != "frente" else 0), fy), 80, [(0, "#fff4d0", 0.8), (0.2, "#ffd890", 0.35), (1, "#ffcf8a", 0)])
                out.append(f'<circle cx="{fx + (5 if vista != "frente" else 0)}" cy="{fy}" r="80" fill="{gg}"/><circle cx="{fx + (4 if vista != "frente" else 0)}" cy="{fy}" r="6.5" fill="#fffbea"/>')
            else:
                out.append(f'<circle cx="{fx}" cy="{fy}" r="6.5" fill="#c9d2da"/>')
    return "".join(out)


def _gafas_sol(z, vista):
    g = z.lin((0, -8), (0, 14), [(0, "#1d2a3a"), (0.6, "#0b0f16"), (1, "#3a2a1a")])
    if vista == "frente":
        lente = lambda x: (f'<path d="M{x - 11} -3 C{x - 11} -8 {x + 11} -8 {x + 11} -3 C{x + 11} 7 {x + 6} 11 {x} 11 C{x - 6} 11 {x - 11} 7 {x - 11} -3 Z" fill="{g}" stroke="#14171c" stroke-width="1.6"/>'
                           f'<path d="M{x - 7} -3 L{x - 2} 6" stroke="#fff" stroke-width="2" opacity="0.35"/>')
        return (lente(-15) + lente(15) + '<path d="M-4 -2 Q0 -5 4 -2" stroke="#14171c" stroke-width="2" fill="none"/>'
                '<path d="M-26 -4 L-37 -5 M26 -4 L37 -5" stroke="#14171c" stroke-width="2"/>')
    if vista == "tq":
        return (f'<path d="M-13 -3 C-13 -8 9 -8 9 -3 C9 7 4 11 -2 11 C-8 11 -13 7 -13 -3 Z" fill="{g}" stroke="#14171c" stroke-width="1.6"/>'
                f'<path d="M15 -3 C15 -7 30 -7 31 -3 C31 6 28 10 24 10 C19 10 15 6 15 -3 Z" fill="{g}" stroke="#14171c" stroke-width="1.6"/>'
                '<path d="M9 -2 Q12 -5 15 -2" stroke="#14171c" stroke-width="2" fill="none"/><path d="M-13 -4 L-22 -2" stroke="#14171c" stroke-width="2"/>'
                '<path d="M-9 -3 L-4 6" stroke="#fff" stroke-width="2" opacity="0.35"/>')
    return (f'<path d="M20 -4 L31 -4 C31 6 28 9 24 9 C21 9 20 4 20 -4 Z" fill="{g}"/><path d="M20 -3 L-6 0" stroke="#14171c" stroke-width="2"/>')


def _gafas_vista(vista):
    if vista == "frente":
        return ('<g fill="none" stroke="#2a2018" stroke-width="1.8"><rect x="-26" y="-4" width="22" height="15" rx="4"/><rect x="4" y="-4" width="22" height="15" rx="4"/>'
                '<path d="M-4 0 Q0 -3 4 0 M-26 0 L-37 -2 M26 0 L37 -2"/></g>'
                '<path d="M-22 -1 L-16 8 M8 -1 L14 8" stroke="#fff" stroke-width="1.6" opacity="0.4"/>')
    if vista == "tq":
        return ('<g fill="none" stroke="#2a2018" stroke-width="1.8"><rect x="-13" y="-4" width="21" height="15" rx="4"/><rect x="14" y="-4" width="16" height="14" rx="4"/>'
                '<path d="M8 0 Q11 -3 14 0 M-13 0 L-22 -1"/></g>')
    return '<g fill="none" stroke="#2a2018" stroke-width="1.8"><path d="M20 -4 L31 -4 L31 8 L21 8 Z M20 -2 L-6 0"/></g>'


# =========================================================================== manos y pies
def vara(pts, ws, punta=True):
    """Contorno suave de un dedo/miembro que pasa por pts con anchos ws (punta redondeada)."""
    n = len(pts)
    izq, der = [], []
    for i in range(n):
        if i == 0:
            dx, dy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
        elif i == n - 1:
            dx, dy = pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]
        else:
            dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        m = math.hypot(dx, dy) or 1e-6
        nx, ny = -dy / m, dx / m
        izq.append((pts[i][0] + nx * ws[i] / 2, pts[i][1] + ny * ws[i] / 2))
        der.append((pts[i][0] - nx * ws[i] / 2, pts[i][1] - ny * ws[i] / 2))
    dx, dy = pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]
    m = math.hypot(dx, dy) or 1e-6
    tip = (pts[-1][0] + dx / m * ws[-1] * 0.5, pts[-1][1] + dy / m * ws[-1] * 0.5)
    return suave(izq + ([tip] if punta else []) + der[::-1], t=0.45)


def _cadena(p0, a0, largos, angs):
    pts, a = [p0], a0
    for L, da in zip(largos, angs):
        a += da
        pts.append(ad(pts[-1], D(a), L))
    return pts


def mano_lado(z, W, ang, u, piel, c=0.3, pal=1, oscura=0.0, pulgar_c=None):
    """Mano vista de lado (desde el pulgar). W muñeca; ang dirección; c: 0 plana .. 1 puño; pal: lado de la palma (+1 = izquierda de la dirección)."""
    m = piel if not oscura else oscuro(piel, oscura)
    k = u
    linea = mix(m["s"], SOMC, 0.25)
    sw = F(0.009 * k)
    z(f'<g transform="translate({F(W[0])} {F(W[1])}) rotate({F(-ang)}) scale({F(pal)} 1)">')
    g = z.lin((-0.1 * k, 0), (0.12 * k, 0.1 * k), [(0, m["l"]), (0.45, m["b"]), (1, m["s"])])
    # dedos de atrás (corazón, anular): algo más curvados y oscuros
    for j, (dx, dy, extra, esc) in enumerate([(-0.035, -0.01, 12, 0.94), (-0.02, -0.005, 6, 0.98)]):
        pts = _cadena(((dx) * k, (0.34 + dy) * k), 8 + c * 6, [0.15 * k * esc, 0.105 * k * esc, 0.085 * k * esc],
                      [c * 70 + extra * c, c * 85, c * 60])
        d = vara(pts, [0.085 * k, 0.08 * k, 0.072 * k, 0.06 * k])
        z(f'<path d="{d}" fill="{mix(m["b"], m["s"], 0.55 - j * 0.2)}" stroke="{linea}" stroke-width="{sw}"/>')
    palma = suave([(-0.1 * k, -0.02 * k), (-0.105 * k, 0.16 * k), (-0.085 * k, 0.34 * k), (-0.02 * k, 0.4 * k), (0.05 * k, 0.385 * k),
                   (0.085 * k, 0.3 * k), (0.11 * k, 0.16 * k), (0.11 * k, 0.03 * k), (0.0, -0.04 * k)], t=0.5)
    z(f'<path d="{palma}" fill="{g}" stroke="{linea}" stroke-width="{sw}"/>')
    # índice
    pts = _cadena((0.0, 0.355 * k), 6 + c * 4, [0.16 * k, 0.11 * k, 0.09 * k], [c * 68, c * 85, c * 55])
    d = vara(pts, [0.088 * k, 0.082 * k, 0.074 * k, 0.062 * k])
    gi = z.lin(ad(pts[1], (-0.06 * k, 0)), ad(pts[1], (0.06 * k, 0.04 * k)), [(0, m["l"]), (0.5, m["b"]), (1, m["s"])])
    z(f'<path d="{d}" fill="{gi}" stroke="{linea}" stroke-width="{sw}"/>')
    for i in (1, 2):
        q, a_ = pts[i], math.degrees(math.atan2(pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]))
        n = D(a_ + 90)
        z(f'<path d="M{P(ad(q, n, 0.03 * k))} L{P(ad(q, n, 0.044 * k))}" stroke="{linea}" stroke-width="{F(0.007 * k)}" opacity="0.7"/>')
    # uña
    q = pts[3]
    a_ = math.degrees(math.atan2(pts[3][0] - pts[2][0], pts[3][1] - pts[2][1]))
    z(f'<ellipse cx="{F(ad(q, D(a_ - 90), 0.016 * k)[0])}" cy="{F(ad(q, D(a_ - 90), 0.016 * k)[1])}" rx="{F(0.02 * k)}" ry="{F(0.028 * k)}" '
      f'fill="{m["l"]}" opacity="0.8" transform="rotate({F(-a_)} {F(ad(q, D(a_ - 90), 0.016 * k)[0])} {F(ad(q, D(a_ - 90), 0.016 * k)[1])})"/>')
    # nudillo con luz
    z(f'<ellipse cx="{F(-0.03 * k)}" cy="{F(0.34 * k)}" rx="{F(0.035 * k)}" ry="{F(0.025 * k)}" fill="{m["l"]}" opacity="0.5"/>')
    # pulgar: nace junto a la muñeca, en el lado de la palma, por delante
    pc = c if pulgar_c is None else pulgar_c
    pts = _cadena((0.07 * k, 0.1 * k), 18 + pc * 16, [0.11 * k, 0.085 * k], [0, 14 + pc * 22])
    d = vara([(0.035 * k, 0.05 * k)] + pts, [0.105 * k, 0.095 * k, 0.075 * k, 0.062 * k])
    gp = z.lin((0.0, 0.1 * k), (0.2 * k, 0.2 * k), [(0, m["l"]), (0.5, m["b"]), (1, m["s"])])
    z(f'<path d="{d}" fill="{gp}" stroke="{linea}" stroke-width="{sw}"/>')
    q = pts[-1]
    a_ = 18 + pc * 16 + 14 + pc * 22
    z(f'<ellipse cx="{F(ad(q, D(a_ - 90), 0.014 * k)[0])}" cy="{F(ad(q, D(a_ - 90), 0.014 * k)[1])}" rx="{F(0.022 * k)}" ry="{F(0.03 * k)}" fill="{m["l"]}" opacity="0.75" '
      f'transform="rotate({F(-a_)} {F(ad(q, D(a_ - 90), 0.014 * k)[0])} {F(ad(q, D(a_ - 90), 0.014 * k)[1])})"/>')
    z(f'<path d="M{F(0.04 * k)} {F(0.2 * k)} Q{F(0.08 * k)} {F(0.17 * k)} {F(0.1 * k)} {F(0.2 * k)}" fill="none" stroke="{linea}" stroke-width="{F(0.007 * k)}" opacity="0.6"/>')
    z("</g>")


def mano_plana(z, W, ang, u, piel, dedos=(1, 1, 1, 1), pulgar=1, abre=6, pul_ang=35, dorso=True, oscura=0.0, curva=0.0, pul_ext=1.0):
    """Mano de frente (palma) o de dorso con los dedos en el plano. dedos: extensión índice..meñique (0 = doblado).
    pulgar: +1 pulgar a la izquierda de la dirección de la mano (visto en pantalla con la mano hacia abajo, a la derecha)."""
    m = piel if not oscura else oscuro(piel, oscura)
    k = u
    linea = mix(m["s"], SOMC, 0.25)
    sw = F(0.009 * k)
    z(f'<g transform="translate({F(W[0])} {F(W[1])}) rotate({F(-ang)}) scale({F(pulgar)} 1)">')
    g = z.lin((0.16 * k, 0.05 * k), (-0.16 * k, 0.4 * k), [(0, m["l"]), (0.5, m["b"]), (1, m["s"])])
    base = [(0.112, 0.345), (0.04, 0.365), (-0.034, 0.355), (-0.1, 0.32)]
    larg = [0.3, 0.335, 0.315, 0.245]
    anch = [0.078, 0.08, 0.076, 0.066]
    angs = [abre * 1.3, abre * 0.4, -abre * 0.4, -abre * 1.3]
    for i in range(4):
        e = dedos[i]
        p0 = (base[i][0] * k, base[i][1] * k)
        a0 = angs[i] + curva * 6 * (i - 1.5)
        L = larg[i] * k
        if e >= 0.5:
            pts = _cadena(p0, a0, [L * 0.42, L * 0.33, L * 0.25], [0, curva * 8, curva * 8])
        else:
            # doblado: solo se ve el nudillo y la primera falange recogida
            pts = _cadena(p0, a0, [L * 0.2, L * 0.1], [0, 0])
        ws = [anch[i] * k, anch[i] * k * 0.95, anch[i] * k * 0.88, anch[i] * k * 0.8][:len(pts)]
        d = vara(pts, ws)
        z(f'<path d="{d}" fill="{g}" stroke="{linea}" stroke-width="{sw}"/>')
        if e >= 0.5:
            for j in (1, 2):
                q = pts[j]
                n = D(a0 + 90)
                z(f'<path d="M{P(ad(q, n, ws[j] * 0.3))} L{P(ad(q, n, -ws[j] * 0.3))}" stroke="{linea}" stroke-width="{F(0.006 * k)}" opacity="0.6"/>')
            if dorso:
                q = ad(pts[-1], D(a0), -0.025 * k)
                z(f'<ellipse cx="{F(q[0])}" cy="{F(q[1])}" rx="{F(ws[-1] * 0.32)}" ry="{F(ws[-1] * 0.42)}" fill="{m["l"]}" opacity="0.8" transform="rotate({F(-a0)} {F(q[0])} {F(q[1])})"/>')
    palma = suave([(-0.105 * k, 0.0), (-0.13 * k, 0.17 * k), (-0.135 * k, 0.33 * k), (-0.06 * k, 0.385 * k), (0.04 * k, 0.4 * k),
                   (0.14 * k, 0.37 * k), (0.15 * k, 0.24 * k), (0.12 * k, 0.06 * k), (0.0, -0.03 * k)], t=0.5)
    z(f'<path d="{palma}" fill="{g}" stroke="{linea}" stroke-width="{sw}"/>')
    if dorso:
        for i in range(4):
            bx, by = base[i][0] * k, base[i][1] * k
            z(f'<path d="M{F(bx * 0.5)} {F(0.12 * k)} L{F(bx * 0.95)} {F(by - 0.05 * k)}" stroke="{m["s"]}" stroke-width="{F(0.008 * k)}" opacity="0.3"/>'
              f'<ellipse cx="{F(bx)}" cy="{F(by - 0.015 * k)}" rx="{F(0.024 * k)}" ry="{F(0.014 * k)}" fill="{m["l"]}" opacity="0.3"/>')
    else:
        z(f'<path d="M{F(-0.12 * k)} {F(0.27 * k)} Q{F(0.0)} {F(0.22 * k)} {F(0.11 * k)} {F(0.3 * k)} M{F(0.07 * k)} {F(0.08 * k)} Q{F(0.0)} {F(0.2 * k)} {F(-0.04 * k)} {F(0.33 * k)}" '
          f'fill="none" stroke="{m["s"]}" stroke-width="{F(0.008 * k)}" opacity="0.6"/>')
    # pulgar (nace en la base de la palma, por delante)
    a1 = pul_ang
    pts = _cadena((0.1 * k, 0.11 * k), a1, [0.13 * k * pul_ext, 0.1 * k * pul_ext], [0, -a1 * 0.3])
    d = vara([(0.06 * k, 0.07 * k)] + pts, [0.11 * k, 0.1 * k, 0.08 * k, 0.066 * k])
    z(f'<path d="{d}" fill="{g}" stroke="{linea}" stroke-width="{sw}"/>')
    if dorso:
        q = ad(pts[-1], D(a1 * 0.65), -0.025 * k)
        z(f'<ellipse cx="{F(q[0])}" cy="{F(q[1])}" rx="{F(0.022 * k)}" ry="{F(0.03 * k)}" fill="{m["l"]}" opacity="0.8" transform="rotate({F(-a1 * 0.65)} {F(q[0])} {F(q[1])})"/>')
    z("</g>")


def bota(z, A, u, m, dirx=1, vista="lado", ang=0, cana=0.3, suela="#1e1a17", tipo="bota", oscura=0.0):
    """Calzado con el tobillo en A. vista 'lado' (punta hacia dirx) o 'frente'. ang: inclinación (grados, + = punta arriba)."""
    m = m if not oscura else oscuro(m, oscura)
    k = u
    z(f'<g transform="translate({F(A[0])} {F(A[1])}) scale({dirx} 1) rotate({F(-ang)})">')
    if vista == "lado":
        if tipo == "bota":
            d = (f"M{F(-0.15 * k)} {F(-cana * k)} L{F(0.13 * k)} {F(-cana * k)} L{F(0.15 * k)} {F(0.02 * k)} "
                 f"C{F(0.3 * k)} {F(0.06 * k)} {F(0.62 * k)} {F(0.08 * k)} {F(0.76 * k)} {F(0.17 * k)} C{F(0.82 * k)} {F(0.21 * k)} {F(0.82 * k)} {F(0.27 * k)} {F(0.78 * k)} {F(0.29 * k)} "
                 f"L{F(-0.2 * k)} {F(0.29 * k)} C{F(-0.24 * k)} {F(0.2 * k)} {F(-0.2 * k)} {F(0.0)} {F(-0.15 * k)} {F(-cana * k)} Z")
        else:  # zapato / zapatilla
            d = (f"M{F(-0.14 * k)} {F(-0.04 * k)} L{F(0.12 * k)} {F(-0.06 * k)} L{F(0.16 * k)} {F(0.04 * k)} "
                 f"C{F(0.3 * k)} {F(0.07 * k)} {F(0.6 * k)} {F(0.1 * k)} {F(0.74 * k)} {F(0.18 * k)} C{F(0.8 * k)} {F(0.22 * k)} {F(0.8 * k)} {F(0.27 * k)} {F(0.76 * k)} {F(0.29 * k)} "
                 f"L{F(-0.2 * k)} {F(0.29 * k)} C{F(-0.24 * k)} {F(0.2 * k)} {F(-0.2 * k)} {F(0.02 * k)} {F(-0.14 * k)} {F(-0.04 * k)} Z")
        g = z.lin((0.2 * k, -0.2 * k), (0.3 * k, 0.3 * k), [(0, m["l"]), (0.45, m["b"]), (1, m["s"])])
        z(f'<path d="{d}" fill="{g}" stroke="{mix(m["s"], SOMC, 0.3)}" stroke-width="{F(0.01 * k)}"/>')
        z(f'<path d="M{F(-0.21 * k)} {F(0.235 * k)} L{F(0.8 * k)} {F(0.235 * k)} L{F(0.78 * k)} {F(0.3 * k)} L{F(-0.2 * k)} {F(0.3 * k)} Z" fill="{suela}"/>')
        z(f'<path d="M{F(0.36 * k)} {F(0.1 * k)} C{F(0.5 * k)} {F(0.11 * k)} {F(0.64 * k)} {F(0.14 * k)} {F(0.74 * k)} {F(0.2 * k)}" fill="none" stroke="{m["l"]}" stroke-width="{F(0.025 * k)}" opacity="0.55"/>')
        if tipo == "bota":
            for i in range(4):
                y = -cana * k + (0.06 + i * 0.075) * k
                z(f'<path d="M{F(0.02 * k + i * 0.04 * k)} {F(y)} l{F(0.08 * k)} {F(0.02 * k)}" stroke="#d8c8a8" stroke-width="{F(0.018 * k)}" stroke-linecap="round" opacity="0.8"/>')
            z(f'<path d="M{F(-0.15 * k)} {F(-cana * k + 0.05 * k)} L{F(0.13 * k)} {F(-cana * k + 0.05 * k)}" stroke="{m["s"]}" stroke-width="{F(0.02 * k)}"/>')
        else:
            z(f'<path d="M{F(-0.2 * k)} {F(0.2 * k)} L{F(0.78 * k)} {F(0.2 * k)}" stroke="#f0ece4" stroke-width="{F(0.04 * k)}" opacity="0.8"/>')
    else:
        d = (f"M{F(-0.13 * k)} {F(-cana * k)} L{F(0.13 * k)} {F(-cana * k)} L{F(0.15 * k)} {F(0.04 * k)} C{F(0.21 * k)} {F(0.1 * k)} {F(0.23 * k)} {F(0.2 * k)} {F(0.21 * k)} {F(0.29 * k)} "
             f"L{F(-0.21 * k)} {F(0.29 * k)} C{F(-0.23 * k)} {F(0.2 * k)} {F(-0.21 * k)} {F(0.1 * k)} {F(-0.15 * k)} {F(0.04 * k)} Z")
        if tipo != "bota":
            d = (f"M{F(-0.12 * k)} {F(-0.04 * k)} L{F(0.12 * k)} {F(-0.04 * k)} L{F(0.15 * k)} {F(0.06 * k)} C{F(0.2 * k)} {F(0.12 * k)} {F(0.22 * k)} {F(0.2 * k)} {F(0.2 * k)} {F(0.29 * k)} "
                 f"L{F(-0.2 * k)} {F(0.29 * k)} C{F(-0.22 * k)} {F(0.2 * k)} {F(-0.2 * k)} {F(0.12 * k)} {F(-0.15 * k)} {F(0.06 * k)} Z")
        g = z.lin((-0.2 * k, 0), (0.2 * k, 0.1 * k), [(0, m["l"]), (0.45, m["b"]), (1, m["s"])])
        z(f'<path d="{d}" fill="{g}" stroke="{mix(m["s"], SOMC, 0.3)}" stroke-width="{F(0.01 * k)}"/>')
        z(f'<path d="M{F(-0.22 * k)} {F(0.24 * k)} L{F(0.22 * k)} {F(0.24 * k)} L{F(0.21 * k)} {F(0.3 * k)} L{F(-0.21 * k)} {F(0.3 * k)} Z" fill="{suela}"/>')
        z(f'<ellipse cx="{F(-0.05 * k)}" cy="{F(0.15 * k)}" rx="{F(0.08 * k)}" ry="{F(0.04 * k)}" fill="{m["l"]}" opacity="0.4"/>')
        if tipo == "bota":
            for i in range(4):
                y = -cana * k + (0.06 + i * 0.075) * k
                z(f'<path d="M{F(-0.06 * k)} {F(y)} L{F(0.06 * k)} {F(y + 0.03 * k)} M{F(0.06 * k)} {F(y)} L{F(-0.06 * k)} {F(y + 0.03 * k)}" stroke="#d8c8a8" stroke-width="{F(0.014 * k)}" opacity="0.8"/>')
    z("</g>")


# =========================================================================== cuerpo
# contorno de la prenda de arriba: (altura sobre la cadera, desplazamiento lateral) en u; lado derecho de arriba abajo
_TOP = {
    "frente": ([(2.47, 0.2), (2.38, 0.52), (2.24, 0.82), (2.02, 0.86), (1.72, 0.76), (1.3, 0.66), (0.92, 0.6), (0.5, 0.68), (0.18, 0.72)], None),
    "tq": ([(2.47, 0.27), (2.38, 0.43), (2.2, 0.5), (1.85, 0.6), (1.5, 0.54), (1.0, 0.44), (0.55, 0.5), (0.18, 0.55)],
           [(0.18, -0.66), (0.55, -0.62), (1.0, -0.55), (1.4, -0.62), (1.8, -0.74), (2.05, -0.84), (2.24, -0.78), (2.38, -0.5), (2.47, -0.13)]),
    "perfil": ([(2.47, 0.2), (2.3, 0.27), (2.0, 0.38), (1.72, 0.5), (1.45, 0.47), (1.15, 0.37), (0.8, 0.34), (0.45, 0.4), (0.18, 0.44)],
               [(0.18, -0.48), (0.45, -0.44), (0.85, -0.34), (1.25, -0.38), (1.7, -0.47), (2.05, -0.47), (2.32, -0.36), (2.47, -0.12)]),
}
_TOP["espalda"] = _TOP["tq"]
_PANT = {
    "frente": ([(0.95, 0.6), (0.55, 0.68), (0.2, 0.7), (-0.1, 0.64)], [(-0.3, 0.12), (-0.36, 0.0), (-0.3, -0.12)]),
    "tq": ([(0.95, 0.44), (0.55, 0.5), (0.15, 0.52), (-0.15, 0.42)], [(-0.3, 0.12)], [(-0.15, -0.55), (0.15, -0.62), (0.55, -0.6), (0.95, -0.54)]),
    "perfil": ([(0.95, 0.32), (0.55, 0.36), (0.1, 0.36), (-0.2, 0.28)], [(-0.3, 0.0)], [(-0.2, -0.36), (0.1, -0.46), (0.55, -0.44), (0.95, -0.34)]),
}
_PANT["espalda"] = _PANT["tq"]
HOMBRO = {"frente": {"L": (2.12, -0.68), "R": (2.12, 0.68)},
          "tq": {"near": (2.12, -0.58), "far": (2.17, 0.36)},
          "perfil": {"near": (2.12, -0.05), "far": (2.17, 0.05)},
          "espalda": {"near": (2.16, 0.36), "far": (2.12, -0.58)}}
CADERA = {"frente": {"L": (0.0, -0.38), "R": (0.0, 0.38)},
          "tq": {"near": (0.0, -0.26), "far": (0.03, 0.24)},
          "perfil": {"near": (0.0, -0.04), "far": (0.02, 0.04)},
          "espalda": {"near": (0.03, 0.24), "far": (0.0, -0.26)}}
CUELLO = {"frente": (0.0, 0.0), "tq": (0.1, 0.08), "perfil": (0.06, 0.15), "espalda": (0.0, 0.04)}
L_BRAZO, L_ANTEB, L_MUSLO, L_PIERNA = 1.25, 1.1, 1.72, 1.6


def _pts(lista, base, up, perp, u, ancho=1.0, ajuste=None, alto=1.0):
    out = []
    for h, s in lista:
        if ajuste:
            s = ajuste(h, s)
        h = h * alto
        out.append((base[0] + up[0] * h * u + perp[0] * s * u * ancho, base[1] + up[1] * h * u + perp[1] * s * u * ancho))
    return out


def figura(z, Pv, u, pj, vista="frente", tronco=180, cadera=None, cab=None, brazos=(), piernas=(), capas=(), ancho=1.0,
           sin_cabeza=False, alto=1.0):
    """Persona vestida. Pv = articulación de la cadera (centro de la pelvis). Devuelve el diccionario de articulaciones."""
    cab = dict(cab or {})
    up = D(tronco)
    perp = (-up[1], up[0])
    upc = D(cadera if cadera is not None else tronco)
    perpc = (-upc[1], upc[0])
    fem = pj.get("fem", True)
    J = dict(P=Pv, up=up, perp=perp, u=u)

    def T(h, s, base=Pv, uu=up, pp=perp):
        h = h * alto
        return (base[0] + uu[0] * h * u + pp[0] * s * u * ancho, base[1] + uu[1] * h * u + pp[1] * s * u * ancho)
    J["T"] = T
    items = []  # (z, función)
    top, pant, piel = pj["top"], pj["pant"], pj["piel"]
    corto = pj.get("manga") == "corta"
    shorts = pj.get("pantalon") == "corto"
    # ---------------------------------------------------------------- piernas
    for pi in piernas:
        lado = pi["lado"]
        h0, s0 = CADERA[vista][lado]
        Hh = T(h0, s0, Pv, upc, perpc)
        if "obj" in pi:
            a1, a2 = ik(Hh, pi["obj"], L_MUSLO * u * pi.get("l1", 1), L_PIERNA * u * pi.get("l2", 1), pi.get("flex", -1))
            pi = dict(pi, a1=a1, a2=a2)
        K = ad(Hh, D(pi["a1"]), L_MUSLO * u * pi.get("l1", 1))
        A = ad(K, D(pi["a2"]), L_PIERNA * u * pi.get("l2", 1))
        J["pie_" + lado] = A
        J["rodilla_" + lado] = K
        J["cadera_" + lado] = Hh
        lejos = lado in ("far",) or pi.get("lejos")
        zz = pi.get("z", -20 if lejos else -10)

        def dib_pierna(Hh=Hh, K=K, A=A, pi=pi, lejos=lejos):
            mp = oscuro(pant, 0.2) if lejos else pant
            mb = pj["bota"]
            pie = pi.get("pie", {})
            ok = 0.2 if lejos else 0.0
            bota(z, A, u, mb, dirx=pie.get("dir", 1), vista=pie.get("vista", "lado"), ang=pie.get("ang", 0),
                 cana=pie.get("cana", 0.32 if pj.get("calzado", "bota") == "bota" else 0.05), tipo=pj.get("calzado", "bota"), oscura=ok,
                 suela=pj.get("suela", "#1e1a17"))
            rT = 0.33 if not fem else 0.32
            if shorts:
                mpiel = oscuro(piel, 0.2) if lejos else piel
                tubo(z, K, A, 0.13 * u, 0.085 * u, mpiel, bul=0.1, tb=0.3)
                tubo(z, Hh, K, rT * 0.8 * u, 0.13 * u, mpiel)
                Kc = ad(Hh, D(pi["a1"]), L_MUSLO * u * 0.55)
                tubo(z, Hh, Kc, rT * u * 1.05, 0.21 * u, mp)
                pliegue(z, f"M{P(ad(Kc, D(pi['a1'] + 90), 0.18 * u))} L{P(ad(Kc, D(pi['a1'] - 90), 0.18 * u))}", mp, 0.02 * u, 0.6)
            else:
                Ab = ad(A, D(pi["a2"]), 0.04 * u)
                tubo(z, K, Ab, 0.205 * u, 0.165 * u, mp, bul=0.04, tb=0.35)
                tubo(z, Hh, K, rT * u, 0.21 * u, mp, bul=0.02)
                # pliegues en la rodilla y en el bajo
                n1 = D(pi["a2"] + 90)
                pliegue(z, f"M{P(ad(K, n1, -0.13 * u))} Q{P(ad(ad(K, D(pi['a2']), 0.18 * u), n1, 0.0))} {P(ad(K, n1, 0.14 * u))}", mp, 0.022 * u, 0.5)
                q = ad(A, D(pi["a2"]), -0.28 * u)
                pliegue(z, f"M{P(ad(q, n1, -0.13 * u))} Q{P(ad(ad(q, D(pi['a2']), 0.06 * u), n1, 0))} {P(ad(q, n1, 0.12 * u))}", mp, 0.018 * u, 0.4)
                q = ad(Hh, D(pi["a1"]), 0.9 * u)
                n2 = D(pi["a1"] + 90)
                pliegue(z, f"M{P(ad(q, n2, -0.16 * u))} Q{P(ad(ad(q, D(pi['a1']), 0.1 * u), n2, -0.02 * u))} {P(ad(q, n2, 0.1 * u))}", mp, 0.018 * u, 0.35)
                if pj.get("vaquero"):
                    z(f'<path d="M{P(ad(Hh, n2, 0.2 * u))} L{P(ad(K, n2, 0.15 * u))} L{P(ad(Ab, n1, 0.12 * u))}" fill="none" stroke="{mp["l"]}" stroke-width="{F(0.012 * u)}" stroke-dasharray="{F(0.03 * u)} {F(0.02 * u)}" opacity="0.6"/>')
        items.append((zz, dib_pierna))
    # ---------------------------------------------------------------- pelvis (pantalón)
    def dib_pelvis():
        t = _PANT[vista]
        der = t[0]
        izq = t[2] if len(t) > 2 else [(h, -s) for h, s in reversed(der)]
        pts = _pts(der + t[1] + izq, Pv, upc, perpc, u, ancho, alto=alto)
        d = suave(pts)
        e1, e2 = _ejes(z, pts)
        forma(z, d, pant, e1, e2)
        # cinturón visible apenas bajo el polar; costura central
        if vista in ("frente", "tq"):
            c0 = 0 if vista == "frente" else 0.18
            z(f'<path d="M{P(T(0.6, c0, Pv, upc, perpc))} Q{P(T(0.0, c0 * 0.8, Pv, upc, perpc))} {P(T(-0.32, c0 * 0.5, Pv, upc, perpc))}" fill="none" stroke="{pant["s"]}" stroke-width="{F(0.018 * u)}" opacity="0.6"/>')
    items.append((pj.get("z_pelvis", 8), dib_pelvis))
    # ---------------------------------------------------------------- cuello
    hn, sn = 2.38, CUELLO[vista][0]
    N = T(hn, sn)
    upcab = D(tronco + cab.get("ang", 0))
    perpcab = (-upcab[1], upcab[0])
    fwd = CUELLO[vista][1]
    esc = cab.get("esc", 1.07)
    C = ad(ad(N, upcab, 0.76 * u * esc), perpcab, fwd * u * esc)
    C = ad(C, cab.get("off", (0, 0)), u)
    J["C"], J["N"] = C, N

    def dib_cuello():
        bajo = ad(ad(C, upcab, -0.3 * u * esc), perpcab, (0.04 if vista == "perfil" else 0.0) * u)
        tubo(z, N, bajo, 0.15 * u * esc, 0.14 * u * esc, piel, borde=False)
        z(f'<ellipse cx="{F(bajo[0])}" cy="{F(bajo[1] - 0.02 * u)}" rx="{F(0.16 * u)}" ry="{F(0.07 * u)}" fill="{piel["s"]}" opacity="0.55" transform="rotate({F(-(tronco + cab.get("ang", 0)) + 180)} {F(bajo[0])} {F(bajo[1])})"/>')
    items.append((0, dib_cuello))
    # ---------------------------------------------------------------- tronco (prenda)
    def dib_tronco():
        der, izq = _TOP[vista]
        largo = pj.get("largo", 0)
        if largo:
            der = der + [(0.18 - largo, der[-1][1] + 0.06)]
            izq = [(0.18 - largo, izq[0][1] - 0.06)] + (izq if izq else [])
        if izq is None or (largo and vista == "frente"):
            base = _TOP[vista][0] + ([(0.18 - largo, _TOP[vista][0][-1][1] + 0.06)] if largo else [])
            der = base
            izq = [(h, -s) for h, s in reversed(base)]
        k_h = 1.0 if fem else 1.08

        def aj(h, s):
            if not fem and 0.6 < h < 1.6:
                return s * 1.08
            if fem and 0.7 < h < 1.2:
                return s * 0.96
            return s * (k_h if h > 1.9 else 1.0)
        pts = _pts(der + izq, Pv, up, perp, u, ancho, aj, alto=alto)
        d = suave(pts)
        e1, e2 = _ejes(z, pts)
        forma(z, d, top, e1, e2)
        cid = z.clip(d)
        z(f'<g clip-path="{cid}">')
        _detalles_top(z, pj, vista, T, u, top, fem)
        z("</g>")
        _cuello_prenda(z, pj, vista, T, u, top)
    items.append((10, dib_tronco))
    # ---------------------------------------------------------------- cabeza
    if not sin_cabeza:
        def dib_cab():
            cabeza(z, C, u * esc, -(tronco + cab.get("ang", 0) - 180), pj, cab.get("vista", vista if vista != "espalda" else "espalda"),
                   cab.get("ex", "neutra"), casco=cab.get("casco", False), frontal=cab.get("frontal"), gafas=cab.get("gafas"),
                   pelo_mojado=cab.get("mojado", False), extra_del=cab.get("extra_del", ""), extra_tras=cab.get("extra_tras", ""))
        items.append((cab.get("z", 20), dib_cab))
    # ---------------------------------------------------------------- brazos
    for br in brazos:
        lado = br["lado"]
        h0, s0 = HOMBRO[vista][lado]
        S = T(h0, s0)
        if "obj" in br:
            a1, a2 = ik(S, br["obj"], L_BRAZO * u * br.get("l1", 1), L_ANTEB * u * br.get("l2", 1), br.get("flex", 1))
            br = dict(br, a1=a1, a2=a2)
        E = ad(S, D(br["a1"]), L_BRAZO * u * br.get("l1", 1))
        W = ad(E, D(br["a2"]), L_ANTEB * u * br.get("l2", 1))
        J["hombro_" + lado], J["codo_" + lado], J["mun_" + lado] = S, E, W
        ah = br.get("ah", br["a2"])
        J["mano_" + lado] = ad(W, D(ah), 0.3 * u)
        lejos = lado == "far" or br.get("lejos")
        zz = br.get("z", -30 if lejos else 30)
        items.append((zz, (lambda S=S, E=E, W=W, br=br, lejos=lejos, ah=ah: dib_brazo(z, pj, u, S, E, W, ah, br, lejos))))
    for zz, fn in capas:
        items.append((zz, (lambda fn=fn: fn(z, J))))
    for zz, fn in sorted(items, key=lambda t: t[0]):
        fn()
    return J


def ik(S, T, l1, l2, flex=1):
    """Ángulos absolutos (a1, a2) de una cadena de dos huesos que va de S a T; flex elige hacia qué lado se dobla."""
    dx, dy = T[0] - S[0], T[1] - S[1]
    d = max(1e-3, min(math.hypot(dx, dy), (l1 + l2) * 0.999))
    a = math.degrees(math.atan2(dx, dy))
    c = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    al = math.degrees(math.acos(max(-1, min(1, c))))
    a1 = a + flex * al
    E = ad(S, D(a1), l1)
    a2 = math.degrees(math.atan2(T[0] - E[0], T[1] - E[1]))
    return a1, a2


def dib_brazo(z, pj, u, S, E, W, ah, br, lejos=False):
    top, piel = pj["top"], pj["piel"]
    corto = pj.get("manga") == "corta"
    mt = oscuro(top, 0.2) if lejos else top
    mp = oscuro(piel, 0.15) if lejos else piel
    mn = br.get("mano", {"t": "lado", "c": 0.35, "pal": 1})
    guante = pj.get("guante")
    mh = (oscuro(guante, 0.15) if lejos else guante) if guante else mp
    a1 = math.degrees(math.atan2(E[0] - S[0], E[1] - S[1]))
    a2 = math.degrees(math.atan2(W[0] - E[0], W[1] - E[1]))

    def la_mano():
        if mn.get("t") == "plana":
            mano_plana(z, W, ah, u, mh, dedos=mn.get("dedos", (1, 1, 1, 1)), pulgar=mn.get("pulgar", 1), abre=mn.get("abre", 6),
                       pul_ang=mn.get("pul_ang", 35), dorso=mn.get("dorso", True), curva=mn.get("curva", 0), pul_ext=mn.get("pul_ext", 1))
        elif mn.get("t") != "nada":
            mano_lado(z, W, ah, u, mh, c=mn.get("c", 0.35), pal=mn.get("pal", 1), pulgar_c=mn.get("pc"))
        if mn.get("objeto"):
            mn["objeto"](z, W, ah)
    if br.get("mano_detras"):
        la_mano()
    if corto:
        Ec = ad(S, D(a1), L_BRAZO * u * 0.5)
        tubo(z, E, W, 0.125 * u, 0.09 * u, mp, bul=0.06, tb=0.3)
        tubo(z, S, E, 0.155 * u, 0.125 * u, mp)
        tubo(z, S, Ec, 0.215 * u, 0.19 * u, mt)
    else:
        Wc = ad(W, D(a2), 0.03 * u)
        tubo(z, E, Wc, 0.16 * u, 0.12 * u, mt, bul=0.04, tb=0.35)
        tubo(z, S, E, 0.21 * u, 0.165 * u, mt, bul=0.03)
        Wa = ad(W, D(a2), -0.09 * u)
        tubo(z, Wa, Wc, 0.125 * u, 0.122 * u, oscuro(mt, 0.18), borde=True)
        n = D(a2 + 90)
        for t, w_ in ((0.12, 0.022), (0.3, 0.016)):
            q = ad(E, D(a2), t * u)
            pliegue(z, f"M{P(ad(q, n, -0.11 * u))} Q{P(ad(ad(q, D(a2), -0.05 * u), n, 0))} {P(ad(q, n, 0.1 * u))}", mt, w_ * u, 0.55)
        q = ad(S, D(a1), 0.75 * u)
        n2 = D(a1 + 90)
        pliegue(z, f"M{P(ad(q, n2, -0.12 * u))} Q{P(ad(ad(q, D(a1), 0.07 * u), n2, 0))} {P(ad(q, n2, 0.1 * u))}", mt, 0.016 * u, 0.4)
    if not br.get("mano_detras"):
        la_mano()


def _ejes(z, pts):
    """Eje del degradado de volumen para un polígono: del lado iluminado al opuesto."""
    lx, ly = z.luz
    # dirección del degradado: sobre todo horizontal (volumen del cuerpo), algo inclinada hacia la luz
    dx, dy = lx, ly * 0.35
    m = math.hypot(dx, dy)
    dx, dy = dx / m, dy / m
    ts = [p[0] * dx + p[1] * dy for p in pts]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    tc = cx * dx + cy * dy
    return (cx + dx * (max(ts) - tc), cy + dy * (max(ts) - tc)), (cx + dx * (min(ts) - tc), cy + dy * (min(ts) - tc))


def _detalles_top(z, pj, vista, T, u, m, fem):
    pr = pj.get("prenda", "polar")
    cz = {"frente": 0.0, "tq": 0.24, "perfil": 0.38, "espalda": None}[vista]
    # pliegues comunes: de la axila a la cintura y en la cintura
    if vista == "frente":
        for sg in (-1, 1):
            pliegue(z, f"M{P(T(1.75, sg * 0.66))} Q{P(T(1.3, sg * 0.5))} {P(T(1.0, sg * 0.3))}", m, 0.024 * u, 0.5)
            pliegue(z, f"M{P(T(0.8, sg * 0.58))} Q{P(T(0.7, sg * 0.38))} {P(T(0.75, sg * 0.18))}", m, 0.02 * u, 0.45)
            pliegue(z, f"M{P(T(2.0, sg * 0.7))} Q{P(T(1.85, sg * 0.5))} {P(T(1.72, sg * 0.4))}", m, 0.018 * u, 0.4)
        if fem:
            for sg in (-1, 1):
                z(f'<path d="M{P(T(1.42, sg * 0.5))} Q{P(T(1.34, sg * 0.3))} {P(T(1.42, sg * 0.1))}" fill="none" stroke="{m["s"]}" stroke-width="{F(0.03 * u)}" opacity="0.45"/>')
    elif vista in ("tq", "espalda"):
        pliegue(z, f"M{P(T(1.8, -0.62))} Q{P(T(1.3, -0.4))} {P(T(1.0, -0.1))}", m, 0.024 * u, 0.5)
        pliegue(z, f"M{P(T(0.85, -0.5))} Q{P(T(0.72, -0.2))} {P(T(0.8, 0.1))}", m, 0.02 * u, 0.45)
        pliegue(z, f"M{P(T(1.75, 0.5))} Q{P(T(1.35, 0.42))} {P(T(1.05, 0.3))}", m, 0.02 * u, 0.4)
        if fem and vista == "tq":
            z(f'<path d="M{P(T(1.45, 0.58))} Q{P(T(1.36, 0.4))} {P(T(1.44, 0.2))}" fill="none" stroke="{m["s"]}" stroke-width="{F(0.03 * u)}" opacity="0.45"/>')
        if vista == "espalda":
            pliegue(z, f"M{P(T(2.1, -0.5))} Q{P(T(1.8, -0.1))} {P(T(2.0, 0.3))}", m, 0.022 * u, 0.45)
            z(f'<path d="M{P(T(2.3, -0.1))} L{P(T(0.3, -0.12))}" stroke="{m["s"]}" stroke-width="{F(0.02 * u)}" opacity="0.3"/>')
    else:
        pliegue(z, f"M{P(T(1.8, 0.0))} Q{P(T(1.3, 0.12))} {P(T(0.95, 0.25))}", m, 0.024 * u, 0.5)
        pliegue(z, f"M{P(T(0.85, -0.28))} Q{P(T(0.7, 0.0))} {P(T(0.8, 0.28))}", m, 0.02 * u, 0.45)
        if fem:
            z(f'<path d="M{P(T(1.45, 0.42))} Q{P(T(1.36, 0.3))} {P(T(1.44, 0.16))}" fill="none" stroke="{m["s"]}" stroke-width="{F(0.03 * u)}" opacity="0.45"/>')
    # dobladillo
    z(f'<path d="M{P(T(0.3, -1.2))} L{P(T(0.3, 1.2))}" stroke="{m["s"]}" stroke-width="{F(0.05 * u)}" opacity="0.55"/>'
      f'<path d="M{P(T(0.34, -1.2))} L{P(T(0.34, 1.2))}" stroke="{m["l"]}" stroke-width="{F(0.012 * u)}" opacity="0.35"/>')
    if pr in ("polar", "parka", "chaqueta") and cz is not None:
        cz2 = cz
        z(f'<path d="M{P(T(2.42, cz2 * 0.9))} L{P(T(0.18 - pj.get("largo", 0), cz2))}" stroke="{mix(m["s"], SOMC, 0.4)}" stroke-width="{F(0.025 * u)}"/>'
          f'<path d="M{P(T(2.42, cz2 * 0.9 + 0.015))} L{P(T(0.18 - pj.get("largo", 0), cz2 + 0.015))}" stroke="{m["l"]}" stroke-width="{F(0.008 * u)}" opacity="0.6"/>')
        tir = T(2.1, cz2 * 0.92 + 0.04)
        z(f'<rect x="{F(tir[0] - 0.02 * u)}" y="{F(tir[1])}" width="{F(0.04 * u)}" height="{F(0.12 * u)}" rx="{F(0.015 * u)}" fill="#c9ccd2"/>')
    if pr == "polar" and vista in ("frente", "tq"):
        # bolsillo de pecho con cremallera
        x0 = 0.28 if vista == "frente" else 0.42
        z(f'<path d="M{P(T(1.72, x0))} L{P(T(1.55, x0 + 0.08))}" stroke="{mix(m["s"], SOMC, 0.4)}" stroke-width="{F(0.02 * u)}"/>')
        # paneles laterales más oscuros (diseño del forro)
        if vista == "frente":
            for sg in (-1, 1):
                z(f'<path d="M{P(T(2.3, sg * 0.62))} Q{P(T(1.8, sg * 0.5))} {P(T(1.6, sg * 0.82))} L{P(T(2.4, sg * 0.95))} Z" fill="{m["s"]}" opacity="0.35"/>')
        else:
            z(f'<path d="M{P(T(2.3, -0.46))} Q{P(T(1.8, -0.4))} {P(T(1.6, -0.8))} L{P(T(2.4, -0.95))} Z" fill="{m["s"]}" opacity="0.35"/>')
    if pr == "parka":
        for sg in ((-1, 1) if vista == "frente" else ((1,) if vista in ("tq", "perfil") else ())):
            x = sg * 0.35 if vista == "frente" else (0.5 if vista == "tq" else 0.2)
            z(f'<rect x="{F(T(0.7, x)[0] - 0.17 * u)}" y="{F(T(0.7, x)[1])}" width="{F(0.34 * u)}" height="{F(0.38 * u)}" rx="{F(0.04 * u)}" fill="{m["s"]}" opacity="0.4"/>'
              f'<rect x="{F(T(0.7, x)[0] - 0.18 * u)}" y="{F(T(0.7, x)[1] - 0.02 * u)}" width="{F(0.36 * u)}" height="{F(0.1 * u)}" rx="{F(0.03 * u)}" fill="{m["b"]}" stroke="{m["s"]}" stroke-width="1"/>')
        for i in range(3):
            q = T(2.0 - i * 0.45, (cz or 0) + 0.1)
            z(f'<rect x="{F(q[0] - 0.03 * u)}" y="{F(q[1])}" width="{F(0.06 * u)}" height="{F(0.12 * u)}" rx="{F(0.02 * u)}" fill="#c8b48a"/>')
    if pr == "jersey":
        z(f'<path d="M{P(T(0.42, -1.2))} L{P(T(0.42, 1.2))}" stroke="{m["s"]}" stroke-width="{F(0.14 * u)}" opacity="0.25"/>')
        for i in range(-12, 13):
            z(f'<path d="M{P(T(0.5, i * 0.07))} L{P(T(0.32, i * 0.07))}" stroke="{m["s"]}" stroke-width="{F(0.012 * u)}" opacity="0.4"/>')
    if pr == "rescate":
        # bandas reflectantes
        for h in (1.25, 0.6):
            z(f'<path d="M{P(T(h, -1.2))} L{P(T(h, 1.2))}" stroke="#d9dcd6" stroke-width="{F(0.08 * u)}" opacity="0.85"/>'
              f'<path d="M{P(T(h, -1.2))} L{P(T(h, 1.2))}" stroke="#ffffff" stroke-width="{F(0.02 * u)}" opacity="0.6"/>')
    if pr == "camisa" and cz is not None:
        for i in range(4):
            q = T(2.15 - i * 0.45, cz)
            z(f'<circle cx="{F(q[0])}" cy="{F(q[1])}" r="{F(0.025 * u)}" fill="{m["l"]}"/>')
        z(f'<path d="M{P(T(2.42, cz))} L{P(T(0.18, cz))}" stroke="{m["s"]}" stroke-width="{F(0.015 * u)}" opacity="0.6"/>')
    if pr == "abrigo" and cz is not None:
        z(f'<path d="M{P(T(2.42, cz))} L{P(T(0.18 - pj.get("largo", 0), cz + 0.05))}" stroke="{m["s"]}" stroke-width="{F(0.03 * u)}"/>')
        for i in range(3):
            q = T(1.8 - i * 0.5, cz + 0.12)
            z(f'<circle cx="{F(q[0])}" cy="{F(q[1])}" r="{F(0.035 * u)}" fill="{m["s"]}"/>')
        q = T(0.8, cz + 0.42 if vista != "frente" else 0.4)
        z(f'<path d="M{P(q)} l{F(0.25 * u)} {F(0.02 * u)}" stroke="{m["s"]}" stroke-width="{F(0.03 * u)}"/>')


def _cuello_prenda(z, pj, vista, T, u, m):
    pr = pj.get("prenda", "polar")
    cz = {"frente": 0.0, "tq": 0.1, "perfil": 0.12, "espalda": 0.0}[vista]
    if pr in ("polar", "parka", "chaqueta", "rescate", "abrigo"):
        # cuello alto de la chaqueta alrededor de la base del cuello
        w = 0.26 if vista == "frente" else 0.22
        if vista == "espalda":
            d = f"M{P(T(2.36, cz - w))} L{P(T(2.62, cz - w * 0.9))} Q{P(T(2.66, cz))} {P(T(2.62, cz + w * 0.9))} L{P(T(2.36, cz + w))} Z"
        else:
            d = (f"M{P(T(2.34, cz - w))} L{P(T(2.6, cz - w * 0.95))} Q{P(T(2.5, cz))} {P(T(2.6, cz + w * 0.95))} L{P(T(2.34, cz + w))} "
                 f"Q{P(T(2.3, cz))} {P(T(2.34, cz - w))} Z")
        a, b = T(2.5, cz - w), T(2.5, cz + w)
        forma(z, d, oscuro(m, 0.08), a, b)
        if pr == "parka":
            # capucha recogida detrás
            hq = T(2.45, cz - (0.3 if vista != "frente" else 0))
            if vista != "frente":
                z(f'<path d="M{P(T(2.3, cz - 0.2))} Q{P(T(2.75, cz - 0.55))} {P(T(2.45, cz - 0.62))} Q{P(T(2.1, cz - 0.55))} {P(T(2.1, cz - 0.3))} Z" fill="{m["s"]}"/>')
    elif pr in ("jersey", "camiseta"):
        w = 0.24 if vista == "frente" else 0.2
        d = f"M{P(T(2.42, cz - w))} Q{P(T(2.22, cz))} {P(T(2.42, cz + w))}"
        z(f'<path d="{d}" fill="none" stroke="{m["s"]}" stroke-width="{F(0.07 * u)}" stroke-linecap="round"/>'
          f'<path d="{d}" fill="none" stroke="{m["l"]}" stroke-width="{F(0.02 * u)}" opacity="0.5" stroke-linecap="round"/>')
    elif pr == "camisa":
        w = 0.24 if vista == "frente" else 0.2
        for sg in (-1, 1):
            z(f'<path d="M{P(T(2.5, cz + sg * w * 0.8))} L{P(T(2.18, cz + sg * 0.04))} L{P(T(2.26, cz + sg * w * 1.2))} Z" fill="{m["l"]}" stroke="{m["s"]}" stroke-width="1"/>')


# =========================================================================== accesorios
def mochila_frente(z, J, u, color="#a8442e", tras=True):
    T = J["T"]
    m = mat(color)
    if tras:
        pts = [T(2.45, -0.62), T(2.5, 0.62), T(2.2, 0.98), T(0.5, 0.96), T(0.25, 0.8), T(0.25, -0.8), T(0.5, -0.96), T(2.2, -0.98)]
        d = suave(pts)
        forma(z, d, oscuro(m, 0.15), T(1.4, -1), T(1.4, 1))
        return
    for sg in (-1, 1):
        a, b, c = T(2.4, sg * 0.42), T(1.6, sg * 0.5), T(0.9, sg * 0.56)
        z(f'<path d="M{P(a)} Q{P(T(2.0, sg * 0.42))} {P(b)} L{P(c)}" fill="none" stroke="{mix(color, "#000", 0.45)}" stroke-width="{F(0.16 * u)}" stroke-linecap="round"/>'
          f'<path d="M{P(a)} Q{P(T(2.0, sg * 0.42))} {P(b)} L{P(c)}" fill="none" stroke="{mix(color, "#000", 0.2)}" stroke-width="{F(0.12 * u)}" stroke-linecap="round"/>'
          f'<path d="M{P(a)} Q{P(T(2.0, sg * 0.42))} {P(b)}" fill="none" stroke="{mix(color, "#fff", 0.35)}" stroke-width="{F(0.02 * u)}" opacity="0.6" transform="translate({F(-0.03 * u)} 0)"/>')
        q = T(1.1, sg * 0.54)
        z(f'<rect x="{F(q[0] - 0.08 * u)}" y="{F(q[1] - 0.05 * u)}" width="{F(0.16 * u)}" height="{F(0.1 * u)}" rx="{F(0.02 * u)}" fill="#2a2d33"/>')
    a, b = T(1.75, -0.48), T(1.75, 0.48)
    z(f'<path d="M{P(a)} L{P(b)}" stroke="#2a2d33" stroke-width="{F(0.06 * u)}"/><rect x="{F((a[0] + b[0]) / 2 - 0.07 * u)}" y="{F(a[1] - 0.05 * u)}" width="{F(0.14 * u)}" height="{F(0.1 * u)}" rx="{F(0.02 * u)}" fill="#14161a"/>')


def mochila_lado(z, J, u, color="#a8442e"):
    T = J["T"]
    m = mat(color)
    pts = [T(2.42, -0.36), T(2.35, -0.95), T(1.9, -1.08), T(0.55, -1.0), T(0.3, -0.8), T(0.35, -0.36), T(1.4, -0.4)]
    forma(z, suave(pts), m, T(1.5, -1.1), T(1.5, -0.3))
    z(f'<path d="M{P(T(1.6, -1.05))} Q{P(T(1.2, -1.12))} {P(T(0.7, -1.0))}" fill="none" stroke="{m["s"]}" stroke-width="{F(0.04 * u)}"/>'
      f'<rect x="{F(T(1.1, -0.98)[0] - 0.1 * u)}" y="{F(T(1.1, -0.98)[1])}" width="{F(0.2 * u)}" height="{F(0.36 * u)}" rx="{F(0.05 * u)}" fill="{m["s"]}" opacity="0.6"/>')


def haz(z, origen, ang, largo, ancho0, ancho1, op=0.5, color="#ffe2a8"):
    """Haz de luz de la lámpara, que se desvanece."""
    d0 = D(ang)
    n = (-d0[1], d0[0])
    fin = ad(origen, d0, largo)
    pts = [ad(origen, n, ancho0), ad(fin, n, ancho1), ad(fin, n, -ancho1), ad(origen, n, -ancho0)]
    g = z.lin(origen, fin, [(0, color, op), (0.4, color, op * 0.4), (1, color, 0)])
    z(f'<path d="M{P(pts[0])} L{P(pts[1])} L{P(pts[2])} L{P(pts[3])} Z" fill="{g}"/>')


def lampara_pos(J, u, vista="perfil", ang=0):
    loc = {"perfil": (36 + 4, -32), "tq": (16 + 5, -33), "frente": (0, -33)}[vista]
    a = math.radians(ang)
    x, y = loc[0] * u / 100, loc[1] * u / 100
    C = J["C"]
    return (C[0] + x * math.cos(a) - y * math.sin(a), C[1] + x * math.sin(a) + y * math.cos(a))


def pie_suelo(u):
    """Distancia de la cadera al suelo de pie (piernas rectas)."""
    return (L_MUSLO + L_PIERNA + 0.3) * u


def Tx(Pv, tronco, u, h, s):
    up = D(tronco)
    return (Pv[0] + up[0] * h * u - up[1] * s * u, Pv[1] + up[1] * h * u + up[0] * s * u)


def espejo(z, x0, fn):
    """Dibuja fn() reflejado respecto a la vertical x = x0 (la luz se refleja también para que siga viniendo del mismo lado)."""
    lx, ly = z.luz
    z.luz = (-lx, ly)
    z(f'<g transform="translate({F(2 * x0)} 0) scale(-1 1)">')
    r = fn()
    z("</g>")
    z.luz = (lx, ly)
    return r


# --------------------------------------------------------------------------- más personajes
def _pj(**k):
    base = dict(piel=dict(b="#e3b08c", s="#b07656", l="#f4cfae"), pelo="#2e2016", peinado="corto", iris="#4b3221",
                labio="#b46a5e", fem=False, top=mat("#555"), pant=mat("#3a3f4a"), bota=mat("#3a2a1e"), edad=35, prenda="chaqueta")
    base.update(k)
    return base


PIEL2 = dict(b="#c98d66", s="#94603f", l="#e5b48e")
PIEL3 = dict(b="#8d5a3b", s="#5e3a25", l="#b98262")
PIEL4 = dict(b="#f0c6a4", s="#c58f6c", l="#fbe0c8")
RESC1 = _pj(nombre="resc1", top=mat("#b8322a", "#e0604e", "#6a1712"), pant=mat("#5a6068", "#878e97", "#30343a"), prenda="rescate",
            casco=dict(b="#e9e7e1", l="#ffffff", s="#9d9b95"), guante=mat("#3a3d42", "#62666d", "#1d1f23"), bota=mat("#2a2a2a", "#4a4a4a", "#121212"))
RESC2 = _pj(nombre="resc2", fem=True, peinado="mono", pelo="#4a2e1c", top=mat("#b8322a", "#e0604e", "#6a1712"),
            pant=mat("#5a6068", "#878e97", "#30343a"), prenda="rescate", casco=dict(b="#c8392c", l="#ec6a58", s="#7a1c14"),
            guante=mat("#3a3d42", "#62666d", "#1d1f23"), bota=mat("#2a2a2a", "#4a4a4a", "#121212"), piel=PIEL2)
FAMILIAR = _pj(nombre="fam", pelo="#8e8a84", peinado="corto", edad=55, top=mat("#b99a6a", "#dcc195", "#6e5733"), prenda="abrigo",
               pant=mat("#3b5274", "#5f7aa0", "#1f2c42"), vaquero=True, calzado="zapato", bota=mat("#5a3a24"))
EQ62 = _pj(nombre="eq62", peinado="peinado60", pelo="#2a1d14", top=mat("#3d4f6a", "#6a7f9c", "#1f2a3a"), prenda="jersey",
           pant=mat("#5a4a38", "#7f6c55", "#2f261c"), calzado="zapato", bota=mat("#2a1d14"), edad=30)
ESPELEO = _pj(nombre="esp", top=mat("#3a2e26", "#5c4a3c", "#18120e"), pant=mat("#2a2622", "#423c36", "#120f0c"), prenda="chaqueta",
              casco=dict(b="#6a5a3a", l="#9a8458", s="#2a2418"), guante=mat("#2a2420"), bota=mat("#1e1a16"),
              piel=dict(b="#7a5a46", s="#3a2a20", l="#a07a60"))
VOLS = [
    _pj(nombre="v1", peinado="corto", pelo="#1e1612", barba="#2a1d14", top=mat("#c0392b"), pant=mat("#2e3440"), edad=32, piel=PIEL2),
    _pj(nombre="v2", fem=True, peinado="melena", pelo="#7a4a26", top=mat("#e0a92e"), pant=mat("#3b5274"), vaquero=True, edad=27, piel=PIEL4, iris="#3d6a5a"),
    _pj(nombre="v3", peinado="calvo", pelo="#9a948c", top=mat("#4f7a3a"), pant=mat("#5a5048"), edad=58, prenda="jersey"),
    _pj(nombre="v4", fem=True, peinado="rizado", pelo="#1a120c", top=mat("#7a3f8f"), pant=mat("#2e3440"), edad=30, piel=PIEL3, labio="#8a4a40"),
    _pj(nombre="v5", peinado="peinado60", pelo="#c9a26b", top=mat("#2f6fb0"), pant=mat("#4a4a4a"), edad=24, piel=PIEL4, iris="#4a6a8a", prenda="polar"),
    _pj(nombre="v6", fem=True, peinado="mono", pelo="#3a2418", top=mat("#d8682a"), pant=mat("#3a4a3a"), edad=42, piel=PIEL2, prenda="polar"),
]
NINO = _pj(nombre="nino", peinado="nino", pelo="#6a4426", piel=PIEL4, top=mat("#f2c230", "#ffe07a", "#a67a10"), prenda="camiseta",
           manga="corta", pantalon="corto", pant=mat("#3a76b8", "#6aa2dc", "#1d4272"), calzado="zapato", bota=mat("#e8e4dc", "#ffffff", "#9a968e"),
           suela="#c0392b", edad=8, iris="#5a3a22")
OFICINA = _pj(nombre="ofi", peinado="corto", pelo="#3a2a1e", top=mat("#9ab8d8", "#cfe0f2", "#4f6a88"), prenda="camisa",
              pant=mat("#4a4e58"), calzado="zapato", bota=mat("#2a1d14"), edad=40, barba=None)
PASEO = _pj(nombre="paseo", fem=True, peinado="melena", pelo="#2a1a10", top=mat("#8a5a3a", "#c08a5e", "#4a2e1a"), prenda="abrigo", largo=0.95,
            pant=mat("#2a2c34"), calzado="zapato", bota=mat("#1e1a16"), edad=38, piel=PIEL2)
BEBE = _pj(nombre="bebe", peinado="bebe", pelo="#8a6040", piel=PIEL4, top=mat("#8fd0c4", "#c4ece4", "#4a8a80"), prenda="camiseta",
           manga="corta", pantalon="corto", pant=mat("#8fd0c4", "#c4ece4", "#4a8a80"), calzado="zapato", bota=mat("#f0c6a4", "#fbe0c8", "#c58f6c"),
           suela="#e0b090", edad=1, iris="#3a2a1a")

CAVE = dict(luz=(-0.6, -0.8), rim="#ffcf8a")
DIA = dict(luz=(-0.5, -0.85), rim="#fff4dc")


# --------------------------------------------------------------------------- objetos
def libro_abierto(z, c, w, ang=0, pasa=False):
    """Libro abierto visto desde delante-arriba; pasa=True: una hoja levantada a medio pasar."""
    x, y = c
    h = w * 0.36
    z(f'<g transform="rotate({F(ang)} {F(x)} {F(y)})">')
    z(f'<path d="M{F(x - w * 0.52)} {F(y - h * 0.42)} L{F(x)} {F(y - h * 0.3)} L{F(x + w * 0.52)} {F(y - h * 0.42)} L{F(x + w * 0.52)} {F(y + h * 0.62)} L{F(x)} {F(y + h * 0.72)} L{F(x - w * 0.52)} {F(y + h * 0.62)} Z" fill="#7a2e26"/>')
    for sg in (-1, 1):
        for k in range(3):
            o = k * w * 0.008
            z(f'<path d="M{F(x)} {F(y - h * 0.32 + o)} C{F(x + sg * w * 0.15)} {F(y - h * 0.5 + o)} {F(x + sg * w * 0.35)} {F(y - h * 0.46 + o)} {F(x + sg * (w * 0.49 - o))} {F(y - h * 0.4 + o)} '
              f'L{F(x + sg * (w * 0.49 - o))} {F(y + h * 0.56 + o)} C{F(x + sg * w * 0.35)} {F(y + h * 0.5 + o)} {F(x + sg * w * 0.15)} {F(y + h * 0.52 + o)} {F(x)} {F(y + h * 0.66 + o)} Z" '
              f'fill="{["#e9dfc8", "#f1e8d4", "#f8f2e4"][k]}" stroke="#bfae8a" stroke-width="0.6"/>')
        for r_ in range(6):
            yy = y - h * 0.22 + r_ * h * 0.13
            z(f'<path d="M{F(x + sg * w * 0.06)} {F(yy)} Q{F(x + sg * w * 0.22)} {F(yy - h * 0.06)} {F(x + sg * w * 0.42)} {F(yy - h * 0.02)}" fill="none" stroke="#9a907c" stroke-width="{F(w * 0.012)}" opacity="0.45" stroke-dasharray="{F(w * 0.05)} {F(w * 0.015)}"/>')
    g = z.lin((x - w * 0.1, y), (x + w * 0.05, y), [(0, "#000", 0), (0.5, "#000", 0.25), (1, "#000", 0)])
    z(f'<rect x="{F(x - w * 0.1)}" y="{F(y - h * 0.4)}" width="{F(w * 0.15)}" height="{F(h * 1.1)}" fill="{g}"/>')
    if pasa:
        z(f'<path d="M{F(x)} {F(y - h * 0.32)} C{F(x + w * 0.08)} {F(y - h * 1.1)} {F(x + w * 0.3)} {F(y - h * 1.3)} {F(x + w * 0.36)} {F(y - h * 1.2)} '
          f'L{F(x + w * 0.36)} {F(y - h * 0.25)} C{F(x + w * 0.3)} {F(y - h * 0.3)} {F(x + w * 0.1)} {F(y - h * 0.1)} {F(x)} {F(y + h * 0.66)} Z" fill="#fbf6ea" stroke="#bfae8a" stroke-width="0.8"/>'
          f'<path d="M{F(x + w * 0.03)} {F(y - h * 0.2)} C{F(x + w * 0.1)} {F(y - h * 0.8)} {F(x + w * 0.25)} {F(y - h * 1.0)} {F(x + w * 0.33)} {F(y - h * 0.9)}" fill="none" stroke="#d8ccb0" stroke-width="{F(w * 0.02)}" opacity="0.7"/>')
    z("</g>")


def cuerda(z, pts, ancho=7, color="#d8452e"):
    d = suave(pts, cerrado=False, t=0.5)
    z(f'<path d="{d}" fill="none" stroke="{mix(color, "#000", 0.45)}" stroke-width="{F(ancho + 2)}" stroke-linecap="round"/>'
      f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{F(ancho)}" stroke-linecap="round"/>'
      f'<path d="{d}" fill="none" stroke="#f3d27a" stroke-width="{F(ancho * 0.5)}" stroke-dasharray="{F(ancho * 0.8)} {F(ancho * 1.1)}" opacity="0.8"/>'
      f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{F(ancho * 0.18)}" opacity="0.35" transform="translate(-1.5 0)"/>')


def tiza(z, W, ah, u):
    a = D(ah + 60)
    p0 = ad(ad(W, D(ah), 0.3 * u), D(ah + 90), 0.02 * u)
    p1 = ad(p0, a, 0.22 * u)
    z(f'<path d="M{P(p0)} L{P(p1)}" stroke="#d9d4c8" stroke-width="{F(0.07 * u)}" stroke-linecap="round"/>'
      f'<path d="M{P(p0)} L{P(p1)}" stroke="#ffffff" stroke-width="{F(0.025 * u)}" stroke-linecap="round" opacity="0.8"/>')


def botella(z, base, ang, u):
    """Botella de agua de aluminio azul; base = culo de la botella, ang = dirección hacia el tapón."""
    a = D(ang)
    n = (-a[1], a[0])
    L, r = 0.95 * u, 0.13 * u
    cu = ad(base, a, L)
    pts = [ad(base, n, r), ad(ad(base, a, L * 0.7), n, r), ad(ad(base, a, L * 0.85), n, r * 0.55), ad(cu, n, r * 0.5),
           ad(cu, n, -r * 0.5), ad(ad(base, a, L * 0.85), n, -r * 0.55), ad(ad(base, a, L * 0.7), n, -r), ad(base, n, -r)]
    d = "M" + " L".join(P(q) for q in pts) + " Z"
    g = z.lin(ad(base, n, r), ad(base, n, -r), [(0, "#9fd0f0"), (0.3, "#3a8ad0"), (0.8, "#1a4a80"), (1, "#5a8ab0")])
    z(f'<path d="{d}" fill="{g}" stroke="#123456" stroke-width="1" stroke-linejoin="round"/>')
    tp = ad(cu, a, 0.1 * u)
    z(f'<path d="M{P(ad(cu, n, r * 0.55))} L{P(ad(tp, n, r * 0.55))} L{P(ad(tp, n, -r * 0.55))} L{P(ad(cu, n, -r * 0.55))} Z" fill="#2a2d33"/>'
      f'<path d="M{P(ad(ad(base, a, L * 0.1), n, r * 0.5))} L{P(ad(ad(base, a, L * 0.65), n, r * 0.5))}" stroke="#fff" stroke-width="{F(0.03 * u)}" opacity="0.5" stroke-linecap="round"/>')


def saco_dormir(z, x0, y0, L, H):
    """Saco de dormir tipo momia, tumbado: cabeza a la izquierda en x0, pies a la derecha."""
    m = mat("#c0582a", "#ee8a50", "#6a2a10")
    pts = [(x0 + 0.02 * L, y0 - 0.35 * H), (x0 + 0.25 * L, y0 - 0.55 * H), (x0 + 0.55 * L, y0 - 0.45 * H), (x0 + 0.85 * L, y0 - 0.3 * H),
           (x0 + 1.0 * L, y0 + 0.05 * H), (x0 + 0.95 * L, y0 + 0.42 * H), (x0 + 0.5 * L, y0 + 0.5 * H), (x0 + 0.1 * L, y0 + 0.48 * H), (x0 - 0.04 * L, y0 + 0.1 * H)]
    d = suave(pts)
    forma(z, d, m, (x0 + 0.5 * L, y0 - 0.55 * H), (x0 + 0.5 * L, y0 + 0.5 * H))
    cid = z.clip(d)
    z(f'<g clip-path="{cid}">')
    for k in range(1, 9):
        x = x0 + k * L * 0.105
        pliegue(z, f"M{F(x)} {F(y0 - 0.6 * H)} Q{F(x - 0.03 * L)} {F(y0)} {F(x + 0.01 * L)} {F(y0 + 0.6 * H)}", m, H * 0.035, 0.55)
    z(f'<path d="M{F(x0)} {F(y0 - 0.05 * H)} C{F(x0 + 0.3 * L)} {F(y0 - 0.12 * H)} {F(x0 + 0.7 * L)} {F(y0 - 0.02 * H)} {F(x0 + L)} {F(y0 + 0.02 * H)}" stroke="#2a2d33" stroke-width="{F(H * 0.025)}" fill="none" opacity="0.6"/>')
    z("</g>")
    return d


def toalla(z, J, u):
    T = J["T"]
    m = mat("#f2ece0", "#ffffff", "#b3a890")
    for sg in (-1, 1):
        pts = [T(2.6, sg * 0.18), T(2.55, sg * 0.6), T(2.3, sg * 0.98), T(1.5, sg * 0.95), T(0.9, sg * 0.75), T(0.9, sg * 0.32),
               T(1.6, sg * 0.3), T(2.3, sg * 0.24)]
        d = suave(pts)
        forma(z, d, m, T(2.0, sg * 1.0), T(2.0, sg * 0.2))
        cid = z.clip(d)
        z(f'<g clip-path="{cid}">')
        for k in range(5):
            pliegue(z, f"M{P(T(2.5 - k * 0.05, sg * (0.3 + k * 0.14)))} Q{P(T(1.7, sg * (0.36 + k * 0.13)))} {P(T(0.9, sg * (0.36 + k * 0.1)))}", m, 0.03 * u, 0.45)
        z(f'<path d="M{P(T(1.15, -2))} L{P(T(1.15, 2))}" stroke="#5aa0c8" stroke-width="{F(0.07 * u)}" opacity="0.8"/>'
          f'<path d="M{P(T(1.03, -2))} L{P(T(1.03, 2))}" stroke="#5aa0c8" stroke-width="{F(0.03 * u)}" opacity="0.8"/>')
        z("</g>")
    z(f'<path d="M{P(T(2.62, -0.2))} Q{P(T(2.75, 0))} {P(T(2.62, 0.2))}" fill="none" stroke="{m["b"]}" stroke-width="{F(0.16 * u)}" stroke-linecap="round"/>')


# --------------------------------------------------------------------------- piezas de Beatriz
def _cuadro(nombre, w, h, luz=CAVE):
    return Lz(nombre, w, h, luz=luz["luz"], rim=luz["rim"])


def p_bea_baja_cuerda():
    n = "bea_baja_cuerda"
    w, h, u = 820, 1500, 112
    z = _cuadro(n, w, h)
    Pv = (380, 940)
    tr = 194
    desc = Tx(Pv, tr, u, 0.55, 0.62)
    rx = desc[0]
    mano_sup = (rx - 0.03 * u, Pv[1] - 3.4 * u)
    freno = Tx(Pv, tr, u, -0.35, -0.75)
    pared = 760

    def tras_cuerda(z, J):
        cuerda(z, [(rx + 2, 0), (rx + 1, mano_sup[1]), (rx, desc[1] - 0.6 * u), desc], 8)

    def arnes(z, J):
        T = J["T"]
        for hh in (0.72, 0.62):
            pass
        z(f'<path d="M{P(T(0.78, -0.62))} Q{P(T(0.68, 0.0))} {P(T(0.78, 0.55))}" fill="none" stroke="#1f2a44" stroke-width="{F(0.14 * u)}" stroke-linecap="round"/>'
          f'<path d="M{P(T(0.8, -0.6))} Q{P(T(0.7, 0.0))} {P(T(0.8, 0.53))}" fill="none" stroke="#3f5a8a" stroke-width="{F(0.05 * u)}" stroke-linecap="round"/>')
        for lado in ("near", "far"):
            hh = J["cadera_" + lado]
            kk = J["rodilla_" + lado]
            q = ad(hh, ((kk[0] - hh[0]) * 0.22, (kk[1] - hh[1]) * 0.22))
            a = math.degrees(math.atan2(kk[0] - hh[0], kk[1] - hh[1]))
            nn = D(a + 90)
            z(f'<path d="M{P(ad(q, nn, 0.34 * u))} Q{P(ad(ad(q, D(a), 0.08 * u), nn, 0))} {P(ad(q, nn, -0.34 * u))}" fill="none" stroke="#1f2a44" stroke-width="{F(0.1 * u)}" stroke-linecap="round"/>')
        # descensor (ocho) y mosquetón
        z(f'<ellipse cx="{F(desc[0])}" cy="{F(desc[1] - 0.12 * u)}" rx="{F(0.08 * u)}" ry="{F(0.15 * u)}" fill="none" stroke="#b8bec8" stroke-width="{F(0.04 * u)}"/>'
          f'<circle cx="{F(desc[0])}" cy="{F(desc[1] + 0.1 * u)}" r="{F(0.12 * u)}" fill="none" stroke="#d6dbe2" stroke-width="{F(0.05 * u)}"/>'
          f'<circle cx="{F(desc[0])}" cy="{F(desc[1] - 0.2 * u)}" r="{F(0.07 * u)}" fill="none" stroke="#d6dbe2" stroke-width="{F(0.04 * u)}"/>')
        cuerda(z, [desc, (desc[0] - 0.2 * u, desc[1] + 0.4 * u), J["mun_near"] if "mun_near" in J else freno], 8)

    def cuerda_baja(z, J):
        W = J["mun_near"]
        cuerda(z, [ad(W, (0, 0.2 * u)), (W[0] - 0.3 * u, W[1] + 1.4 * u), (W[0] - 0.1 * u, W[1] + 2.6 * u), (W[0] + 0.25 * u, h - 10)], 8)

    J = figura(z, Pv, u, BEA, "tq", tronco=tr, cab=dict(ex="concentrada", casco=True, frontal="on", ang=-26),
               brazos=[dict(lado="far", obj=mano_sup, flex=-1, ah=178, mano=dict(t="lado", c=0.75, pal=-1)),
                       dict(lado="near", obj=freno, flex=1, ah=10, mano=dict(t="lado", c=0.8, pal=1))],
               piernas=[dict(lado="near", obj=(pared - 0.3 * u, 1080), flex=1, pie=dict(ang=88)),
                        dict(lado="far", obj=(pared - 0.3 * u, 930), flex=1, pie=dict(ang=92))],
               capas=[(-40, tras_cuerda), (12, arnes), (31, cuerda_baja)])
    # la cuerda pasa por delante de la mano de arriba
    cuerda(z, [(rx + 2, mano_sup[1] - 0.6 * u), (rx + 1, mano_sup[1] + 0.25 * u)], 8)
    mano_lado(z, J["mun_far"], 178, u, oscuro(PIEL_BEA, 0.1), c=0.8, pal=-1)
    lp = lampara_pos(J, u * 1.07, "tq", 26 - 14)
    z.guardar()
    return n


def p_bea_despide():
    n = "bea_despide"
    w, h, u = 640, 1000, 112
    z = _cuadro(n, w, h, DIA)
    suelo = 970
    Pv = (320, suelo - pie_suelo(u))
    sombra_suelo(z, 320, suelo - 6, 1.4 * u)
    figura(z, Pv, u, BEA, "frente", cab=dict(ex="sonrisa_d", ang=-4),
           brazos=[dict(lado="L", a1=-8, a2=-3, mano=dict(t="lado", c=0.45, pal=1)),
                   dict(lado="R", a1=140, a2=170, ah=174, mano=dict(t="plana", dorso=False, pulgar=1, abre=9, pul_ang=45))],
           piernas=[dict(lado="L", a1=-4, a2=-1, pie=dict(vista="frente")), dict(lado="R", a1=4, a2=1, pie=dict(vista="frente"))],
           capas=[(-40, lambda z, J: mochila_frente(z, J, u)), (12, lambda z, J: mochila_frente(z, J, u, tras=False))])
    z.guardar()
    return n


def _camina(z, Pv, u, pj, fot, cab, mochila=None, suelo=None, tronco=182):
    if fot == "a":
        pn, pf, bn, bf = (24, 4, 10), (-18, -40, -22), (-22, -10), (22, 48)
    else:
        pn, pf, bn, bf = (-18, -40, -22), (24, 4, 10), (22, 48), (-22, -10)
    capas = [(-35, lambda z, J: mochila_lado(z, J, u, mochila))] if mochila else []
    return figura(z, Pv, u, pj, "perfil", tronco=tronco, cab=cab,
                  brazos=[dict(lado="near", a1=bn[0], a2=bn[1], mano=dict(t="lado", c=0.5, pal=1)),
                          dict(lado="far", a1=bf[0], a2=bf[1], mano=dict(t="lado", c=0.5, pal=1))],
                  piernas=[dict(lado="near", a1=pn[0], a2=pn[1], pie=dict(ang=pn[2])), dict(lado="far", a1=pf[0], a2=pf[1], pie=dict(ang=pf[2]))],
                  capas=capas)


def p_bea_camina(fot="a"):
    n = f"bea_camina_{fot}"
    w, h, u = 920, 960, 112
    z = _cuadro(n, w, h)
    suelo = 935
    Pv = (330, suelo - pie_suelo(u) + 0.07 * u)
    sombra_suelo(z, 340, suelo - 6, 1.6 * u)
    J = _camina(z, Pv, u, BEA, fot, dict(ex="neutra", casco=True, frontal="on", ang=4), mochila="#a8442e")
    haz(z, lampara_pos(J, u * 1.07, "perfil", -4), 98, 520, 0.08 * u, 1.3 * u, 0.42)
    z.guardar()
    return n


def _sentada_cruzada(Pv, u):
    return [dict(lado="L", a1=-66, a2=78, l1=0.86, l2=0.82, z=14, pie=dict(dir=1, ang=-15)),
            dict(lado="R", a1=66, a2=-78, l1=0.86, l2=0.82, z=13, pie=dict(dir=-1, ang=-15))]


def _suelo_sentada(z, Pv, u):
    sombra_suelo(z, Pv[0], Pv[1] + 0.55 * u, 2.2 * u, 0.3 * u)


def p_bea_lee(fot="a"):
    n = f"bea_lee_{fot}"
    w, h, u = 760, 820, 112
    z = _cuadro(n, w, h)
    Pv = (380, 700)
    _suelo_sentada(z, Pv, u)
    libro = (380, 505)

    def lib(z, J):
        libro_abierto(z, libro, 1.55 * u, -4, pasa=(fot == "b"))
    figura(z, Pv, u, BEA, "frente", tronco=180, cab=dict(ex="concentrada", ang=8),
           brazos=[dict(lado="L", obj=(libro[0] - 0.75 * u, libro[1] + 0.05 * u), flex=-1, ah=55, mano=dict(t="lado", c=0.55, pal=1)),
                   dict(lado="R", obj=(libro[0] + (0.75 if fot == "a" else 0.45) * u, libro[1] + (0.05 if fot == "a" else -0.45) * u), flex=1,
                        ah=-55 if fot == "a" else -150, mano=dict(t="lado", c=0.55 if fot == "a" else 0.3, pal=-1))],
           piernas=_sentada_cruzada(Pv, u), capas=[(25, lib)])
    z.guardar()
    return n


def p_bea_duerme():
    n = "bea_duerme"
    w, h, u = 1300, 520, 112
    z = _cuadro(n, w, h)
    sombra_suelo(z, 650, 470, 5.4 * u, 0.35 * u)
    # almohada (bolsa de ropa)
    m = mat("#5a6a7a", "#8a9aaa", "#2a3440")
    pts = [(70, 330), (110, 270), (260, 250), (360, 290), (380, 370), (330, 440), (150, 455), (75, 420)]
    forma(z, suave(pts), m, (200, 250), (200, 455))
    pliegue(z, "M120 300 Q220 330 340 310", m, 4, 0.5)
    # cabeza de lado sobre la almohada (corona hacia la izquierda)
    J = dict(C=(255, 300))
    cabeza(z, (255, 300), 125, -84, BEA, "frente", "cerrados")
    # saco (le tapa hasta la barbilla) y mano asomando
    saco_dormir(z, 300, 352, 950, 230)
    z(f'<path d="M300 300 C330 250 380 240 420 260 C400 300 360 330 310 340 Z" fill="{BEA["top"]["s"]}"/>')
    mano_lado(z, (395, 285), -70, 112, PIEL_BEA, c=0.45, pal=1)
    z.guardar()
    return n


def p_bea_marca(fot="a"):
    n = f"bea_marca_{fot}"
    w, h, u = 700, 1060, 112
    z = _cuadro(n, w, h)
    suelo = 1035
    Pv = (300, suelo - pie_suelo(u))
    sombra_suelo(z, 300, suelo - 6, 1.4 * u)
    obj = (560, 215) if fot == "a" else (565, 330)
    figura(z, Pv, u, BEA, "espalda", tronco=181, cab=dict(casco=True, frontal="on", ang=4),
           brazos=[dict(lado="near", obj=obj, flex=1, ah=150 if fot == "a" else 135, mano=dict(t="lado", c=0.7, pal=1, objeto=lambda z, W, ah: tiza(z, W, ah, u)), z=30),
                   dict(lado="far", a1=-6, a2=-2, mano=dict(t="lado", c=0.4, pal=-1))],
           piernas=[dict(lado="near", a1=3, a2=0, pie=dict(ang=0)), dict(lado="far", a1=-5, a2=-2, pie=dict(ang=0))])
    z.guardar()
    return n


def gorro_tejido(z, c, w, filas, m=None):
    m = m or mat("#c0392b", "#ea6a5a", "#6a1a12")
    x, y = c
    h = w * 0.55 * filas
    d = f"M{F(x - w / 2)} {F(y)} L{F(x + w / 2)} {F(y)} L{F(x + w * 0.48)} {F(y + h)} Q{F(x)} {F(y + h * 1.12)} {F(x - w * 0.48)} {F(y + h)} Z"
    forma(z, d, m, (x - w / 2, y), (x + w / 2, y))
    cid = z.clip(d)
    z(f'<g clip-path="{cid}">')
    for i in range(int(filas * 6) + 1):
        yy = y + i * w * 0.09
        for j in range(12):
            xx = x - w / 2 + j * w / 11
            z(f'<path d="M{F(xx - w * 0.03)} {F(yy)} l{F(w * 0.03)} {F(w * 0.06)} l{F(w * 0.03)} {F(-w * 0.06)}" fill="none" stroke="{m["s"]}" stroke-width="{F(w * 0.012)}" opacity="0.55"/>')
    z("</g>")


def agujas(z, J, u, fot):
    Wl, Wr = J["mun_L"], J["mun_R"]
    c = ((Wl[0] + Wr[0]) / 2, (Wl[1] + Wr[1]) / 2 + 0.1 * u)
    gorro_tejido(z, (c[0], c[1] + 0.12 * u), 0.85 * u, 0.9)
    for (Wp, a) in ((Wl, 60 if fot == "a" else 40), (Wr, -50 if fot == "a" else -70)):
        q = ad(Wp, D(a + (0 if a > 0 else 0)), 0.3 * u)
        p0, p1 = ad(q, D(a - 90 if a > 0 else a + 90), -0.5 * u), ad(q, D(a - 90 if a > 0 else a + 90), 0.55 * u)
        z(f'<path d="M{P(p0)} L{P(p1)}" stroke="#8a8f98" stroke-width="{F(0.035 * u)}" stroke-linecap="round"/>'
          f'<path d="M{P(p0)} L{P(p1)}" stroke="#e8ecf2" stroke-width="{F(0.012 * u)}" stroke-linecap="round"/>')
    # hilo hasta el ovillo
    z(f'<path d="M{F(c[0] + 0.3 * u)} {F(c[1] + 0.2 * u)} C{F(c[0] + 1.2 * u)} {F(c[1] + 0.6 * u)} {F(c[0] + 1.6 * u)} {F(c[1] + 1.6 * u)} {F(c[0] + 2.1 * u)} {F(c[1] + 2.05 * u)}" fill="none" stroke="#c0392b" stroke-width="{F(0.025 * u)}"/>')


def ovillo(z, c, r):
    m = mat("#c0392b", "#ea6a5a", "#6a1a12")
    g = z.rad((c[0] - r * 0.3, c[1] - r * 0.3), r * 1.2, [(0, m["l"]), (0.6, m["b"]), (1, m["s"])])
    z(f'<circle cx="{F(c[0])}" cy="{F(c[1])}" r="{F(r)}" fill="{g}"/>')
    for k in range(7):
        a = k * 26
        z(f'<ellipse cx="{F(c[0])}" cy="{F(c[1])}" rx="{F(r * 0.95)}" ry="{F(r * 0.35)}" fill="none" stroke="{m["s"]}" stroke-width="{F(r * 0.06)}" opacity="0.5" transform="rotate({a} {F(c[0])} {F(c[1])})"/>')


def p_bea_teje(fot="a"):
    n = f"bea_teje_{fot}"
    w, h, u = 860, 820, 112
    z = _cuadro(n, w, h)
    Pv = (380, 700)
    _suelo_sentada(z, Pv, u)
    ovillo(z, (380 + 2.2 * u, 755), 0.32 * u)
    dx = 0.08 * u if fot == "a" else -0.08 * u
    figura(z, Pv, u, BEA, "frente", cab=dict(ex="concentrada", ang=6),
           brazos=[dict(lado="L", obj=(380 - 0.45 * u + dx, 520), flex=-1, ah=60, mano=dict(t="lado", c=0.6, pal=1)),
                   dict(lado="R", obj=(380 + 0.45 * u + dx, 520 - (0.1 * u if fot == "b" else 0)), flex=1, ah=-60, mano=dict(t="lado", c=0.6, pal=-1))],
           piernas=_sentada_cruzada(Pv, u), capas=[(25, lambda z, J: agujas(z, J, u, fot))])
    z.guardar()
    return n


def pelvis_desde_pies(A, u, a1, a2):
    """Cadera tal que el tobillo cae en A con los ángulos dados."""
    K = ad(A, D(a2), -L_PIERNA * u)
    return ad(K, D(a1), -L_MUSLO * u)


def p_bea_ejercicio(fot="a"):
    n = f"bea_ejercicio_{fot}"
    w, h, u = 700, 980, 112
    z = _cuadro(n, w, h)
    suelo = 955
    A = (330, suelo - 0.29 * u)
    sombra_suelo(z, 380, suelo - 6, 1.5 * u)
    if fot == "a":
        Pv = (A[0] - 0.02 * u, A[1] - (L_MUSLO + L_PIERNA) * u)
        tr, cab_ang, br = 180, 0, dict(a1=60, a2=75)
        pn = dict(lado="near", obj=A, flex=1, pie=dict(ang=0))
    else:
        Pv = (A[0] - 0.95 * u, A[1] - 2.0 * u)
        tr, cab_ang, br = 148, 26, dict(a1=96, a2=92)
        pn = dict(lado="near", obj=A, flex=1, pie=dict(ang=0))
    pf = dict(pn, lado="far", obj=(A[0] + 0.2 * u, A[1]))
    figura(z, Pv, u, BEA, "perfil", tronco=tr, cab=dict(ex="concentrada" if fot == "b" else "neutra", ang=cab_ang),
           brazos=[dict(lado="near", ah=br["a2"], mano=dict(t="plana", dorso=True, pulgar=-1, abre=2, pul_ang=10), **br),
                   dict(lado="far", ah=br["a2"], mano=dict(t="plana", dorso=True, pulgar=-1, abre=2, pul_ang=10), a1=br["a1"] + 4, a2=br["a2"] + 3)],
           piernas=[pn, pf])
    z.guardar()
    return n


def p_bea_bebe():
    n = "bea_bebe"
    w, h, u = 700, 1000, 112
    z = _cuadro(n, w, h)
    suelo = 975
    Pv = (300, suelo - pie_suelo(u))
    sombra_suelo(z, 320, suelo - 6, 1.4 * u)
    tr, ang = 186, 30
    N = Tx(Pv, tr, u, 2.38, 0.06)
    up = D(tr + ang)
    perp = (-up[1], up[0])
    k = u * 1.07 / 100
    C = ad(ad(N, up, 0.76 * u * 1.07), perp, 0.15 * u * 1.07)
    rot = math.radians(-(tr + ang - 180))
    boca = (C[0] + (38 * math.cos(rot) - 31 * math.sin(rot)) * k, C[1] + (38 * math.sin(rot) + 31 * math.cos(rot)) * k)
    bang = -128
    base = ad(boca, D(bang), -1.02 * u)
    W = ad(ad(base, D(bang), 0.22 * u), D(bang + 90), 0.0)

    def bot(z, J):
        botella(z, base, bang, u)
    figura(z, Pv, u, BEA, "perfil", tronco=tr, cab=dict(ex="beber", ang=ang),
           brazos=[dict(lado="near", obj=ad(W, D(bang + 90), 0.16 * u), flex=-1, ah=bang - 100, mano=dict(t="lado", c=0.7, pal=-1), z=32),
                   dict(lado="far", a1=-4, a2=-2, mano=dict(t="lado", c=0.4, pal=1))],
           piernas=[dict(lado="near", a1=-3, a2=0, pie=dict(ang=0)), dict(lado="far", a1=5, a2=1, pie=dict(ang=0))],
           capas=[(31, bot)])
    z.guardar()
    return n


def cuaderno(z, c, w, ang, dibujo=True):
    x, y = c
    h = w * 0.72
    z(f'<g transform="rotate({F(ang)} {F(x)} {F(y)})">'
      f'<rect x="{F(x - w / 2 - 3)}" y="{F(y - h / 2 + 3)}" width="{F(w + 6)}" height="{F(h)}" rx="4" fill="#2a3a5a"/>'
      f'<rect x="{F(x - w / 2)}" y="{F(y - h / 2)}" width="{F(w)}" height="{F(h)}" rx="3" fill="#f4efe2" stroke="#c8bea6" stroke-width="1"/>')
    for i in range(9):
        z(f'<circle cx="{F(x - w / 2 + 8 + i * (w - 16) / 8)}" cy="{F(y - h / 2)}" r="3" fill="none" stroke="#6a6e76" stroke-width="2"/>')
    if dibujo:
        z(f'<path d="M{F(x - w * 0.3)} {F(y + h * 0.2)} L{F(x - w * 0.1)} {F(y - h * 0.15)} L{F(x + 0.02 * w)} {F(y + h * 0.05)} L{F(x + w * 0.15)} {F(y - h * 0.25)} L{F(x + w * 0.32)} {F(y + h * 0.2)}" '
          f'fill="none" stroke="#5a5a5a" stroke-width="{F(w * 0.012)}" stroke-linejoin="round"/>'
          f'<circle cx="{F(x + w * 0.24)}" cy="{F(y - h * 0.28)}" r="{F(w * 0.05)}" fill="none" stroke="#5a5a5a" stroke-width="{F(w * 0.01)}"/>')
    z("</g>")


def lapiz(z, W, ah, u):
    p0 = ad(ad(W, D(ah), 0.32 * u), D(ah + 90), 0.02 * u)
    a = D(ah + 140)
    p1 = ad(p0, a, -0.45 * u)
    p2 = ad(p0, a, 0.08 * u)
    z(f'<path d="M{P(p1)} L{P(p0)}" stroke="#e0a92e" stroke-width="{F(0.05 * u)}" stroke-linecap="butt"/>'
      f'<path d="M{P(p0)} L{P(p2)}" stroke="#e8c9a0" stroke-width="{F(0.04 * u)}"/>'
      f'<circle cx="{F(p2[0])}" cy="{F(p2[1])}" r="{F(0.012 * u)}" fill="#2a2a2a"/>')


def p_bea_dibuja():
    n = "bea_dibuja"
    w, h, u = 760, 860, 112
    z = _cuadro(n, w, h)
    suelo = 830
    Pv = (250, suelo - 0.45 * u)
    sombra_suelo(z, 380, suelo - 8, 2.2 * u, 0.3 * u)
    A1, A2 = (250 + 2.4 * u, suelo - 0.29 * u), (250 + 2.15 * u, suelo - 0.29 * u)
    rodilla = (250 + 1.55 * u, Pv[1] - 1.25 * u)
    cpos = (rodilla[0] - 0.1 * u, rodilla[1] - 0.35 * u)

    def cuad(z, J):
        cuaderno(z, cpos, 1.15 * u, -55)
    figura(z, Pv, u, BEA, "tq", tronco=166, cab=dict(ex="concentrada", ang=20),
           brazos=[dict(lado="far", obj=(cpos[0] - 0.1 * u, cpos[1] - 0.25 * u), flex=-1, ah=60, mano=dict(t="lado", c=0.5, pal=1)),
                   dict(lado="near", obj=(cpos[0] - 0.45 * u, cpos[1] + 0.1 * u), flex=1, ah=40, mano=dict(t="lado", c=0.7, pal=1, objeto=lambda z, W, ah: lapiz(z, W, ah, u)))],
           piernas=[dict(lado="far", obj=A1, flex=1, pie=dict(ang=0)), dict(lado="near", obj=A2, flex=1, pie=dict(ang=0), z=15)],
           capas=[(16, cuad)])
    z.guardar()
    return n


def p_bea_habla(fot="a"):
    n = f"bea_habla_{fot}"
    w, h, u = 760, 820, 112
    z = _cuadro(n, w, h)
    Pv = (380, 700)
    _suelo_sentada(z, Pv, u)
    if fot == "a":
        br = dict(lado="R", obj=(380 + 1.15 * u, 700 - 2.5 * u), flex=1, ah=160, mano=dict(t="plana", dorso=False, pulgar=1, abre=8, pul_ang=50, curva=0.3))
        ex = "habla"
    else:
        br = dict(lado="R", obj=(380 + 1.0 * u, 700 - 1.5 * u), flex=1, ah=140, mano=dict(t="plana", dorso=False, pulgar=1, abre=5, pul_ang=40, curva=0.6))
        ex = "rie"
    figura(z, Pv, u, BEA, "frente", cab=dict(ex=ex, ang=-5 if fot == "a" else 6),
           brazos=[dict(lado="L", obj=(380 - 1.25 * u, 700 - 0.55 * u), flex=-1, ah=-10, mano=dict(t="plana", dorso=True, pulgar=-1, abre=3, pul_ang=30)), br],
           piernas=_sentada_cruzada(Pv, u))
    z.guardar()
    return n


def p_bea_oye():
    n = "bea_oye"
    w, h, u = 640, 960, 112
    z = _cuadro(n, w, h)
    suelo = 935
    Pv = (320, suelo - pie_suelo(u) + 0.04 * u)
    sombra_suelo(z, 320, suelo - 6, 1.4 * u)
    J0 = Tx(Pv, 176, u, 2.38, 0)
    oreja = (J0[0] + 0.55 * u, J0[1] - 0.72 * u)
    figura(z, Pv, u, BEA, "frente", tronco=176, cab=dict(ex="miedo", ang=-14, casco=True, frontal="on"),
           brazos=[dict(lado="L", obj=(Pv[0] - 0.2 * u, Pv[1] - 0.9 * u), flex=-1, ah=60, mano=dict(t="lado", c=0.8, pal=1)),
                   dict(lado="R", obj=(oreja[0] + 0.25 * u, oreja[1] + 0.4 * u), flex=-1, ah=172, mano=dict(t="plana", dorso=False, pulgar=1, abre=1, pul_ang=25, curva=0.5))],
           piernas=[dict(lado="L", a1=3, a2=-5, pie=dict(vista="frente")), dict(lado="R", a1=-2, a2=4, pie=dict(vista="frente"))])
    z.guardar()
    return n


def p_bea_moscas():
    n = "bea_moscas"
    w, h, u = 640, 960, 112
    z = _cuadro(n, w, h)
    suelo = 935
    Pv = (320, suelo - pie_suelo(u) + 0.06 * u)
    sombra_suelo(z, 320, suelo - 6, 1.4 * u)
    N = Tx(Pv, 172, u, 2.38, 0)
    C = (N[0] + 0.12 * u, N[1] - 0.82 * u)
    figura(z, Pv, u, BEA, "frente", tronco=172, cab=dict(ex="agobio", ang=10, casco=True, frontal="off"),
           brazos=[dict(lado="L", obj=(C[0] - 0.2 * u, C[1] + 0.55 * u), flex=-1, ah=172, mano=dict(t="plana", dorso=True, pulgar=1, abre=2, pul_ang=15), z=31),
                   dict(lado="R", obj=(C[0] + 0.24 * u, C[1] + 0.5 * u), flex=1, ah=186, mano=dict(t="plana", dorso=True, pulgar=-1, abre=2, pul_ang=15), z=32)],
           piernas=[dict(lado="L", a1=8, a2=-6, pie=dict(vista="frente")), dict(lado="R", a1=-8, a2=6, pie=dict(vista="frente"))])
    z.guardar()
    return n


def p_bea_sujetada():
    n = "bea_sujetada"
    w, h, u = 1300, 1000, 108
    z = _cuadro(n, w, h, DIA)
    suelo = 975
    sombra_suelo(z, 650, suelo - 6, 4.6 * u, 0.32 * u)
    # rescatadores a los lados (3/4 mirando hacia ella)
    Pl = (330, suelo - pie_suelo(u))
    Pb = (650, suelo - pie_suelo(u) + 0.2 * u)
    Sb_L = Tx(Pb, 180, u, 2.12, -0.68)
    Sb_R = Tx(Pb, 180, u, 2.12, 0.68)

    def resc_izq():
        figura(z, Pl, u, RESC1, "tq", tronco=176, cab=dict(ex="concentrada", casco=True, frontal="on", ang=10),
               brazos=[dict(lado="far", obj=(Sb_L[0] - 0.05 * u, Sb_L[1] + 1.0 * u), flex=-1, ah=80, mano=dict(t="lado", c=0.7, pal=1)),
                       dict(lado="near", obj=(Pb[0] - 0.5 * u, Pb[1] - 0.2 * u), flex=1, ah=70, mano=dict(t="lado", c=0.6, pal=1), z=-31)],
               piernas=[dict(lado="near", a1=-6, a2=-2, pie=dict(ang=0)), dict(lado="far", a1=8, a2=2, pie=dict(ang=0))])
    resc_izq()
    Pr = (1300 - 330, Pl[1])
    espejo(z, 650, lambda: figura(z, (1300 - Pr[0], Pr[1]), u, RESC2, "tq", tronco=176, cab=dict(ex="neutra", casco=True, frontal="on", ang=8),
                                  brazos=[dict(lado="far", obj=(1300 - Sb_R[0] + 0.05 * u, Sb_R[1] + 1.0 * u), flex=-1, ah=80, mano=dict(t="lado", c=0.7, pal=1)),
                                          dict(lado="near", obj=(1300 - Pb[0] - 0.5 * u, Pb[1] - 0.2 * u), flex=1, ah=70, mano=dict(t="lado", c=0.6, pal=1), z=-31)],
                                  piernas=[dict(lado="near", a1=-6, a2=-2, pie=dict(ang=0)), dict(lado="far", a1=8, a2=2, pie=dict(ang=0))]))
    N = Tx(Pb, 180, u, 2.38, 0)
    C = (N[0], N[1] - 0.8 * u)
    figura(z, Pb, u, BEA, "frente", tronco=180, cab=dict(ex="entrecierra", ang=-6, casco=True, frontal="off"),
           brazos=[dict(lado="L", a1=-24, a2=-10, mano=dict(t="lado", c=0.5, pal=1)),
                   dict(lado="R", obj=(C[0] + 0.5 * u, C[1] - 0.22 * u), flex=-1, ah=-84, mano=dict(t="plana", dorso=True, pulgar=-1, abre=1, pul_ang=12), z=40)],
           piernas=[dict(lado="L", a1=6, a2=-10, pie=dict(vista="frente", ang=-8)), dict(lado="R", a1=-8, a2=6, pie=dict(vista="frente"))])
    # manos de los rescatadores por encima del brazo de Beatriz
    mano_lado(z, (Sb_L[0] - 0.05 * u, Sb_L[1] + 1.0 * u), 80, u, RESC1["guante"], c=0.75, pal=1)
    z.guardar()
    return n


def p_bea_abraza():
    n = "bea_abraza"
    w, h, u = 760, 1040, 112
    z = _cuadro(n, w, h, DIA)
    suelo = 1010
    sombra_suelo(z, 380, suelo - 6, 2.0 * u, 0.3 * u)
    Pb = (300, suelo - pie_suelo(u) + 0.05 * u)
    Pf = (445, suelo - pie_suelo(u * 1.04))
    Jb = figura(z, Pb, u, BEA, "frente", tronco=176, cab=dict(ex="feliz_ojos", ang=-14),
                piernas=[dict(lado="L", a1=-3, a2=-1, pie=dict(vista="frente")), dict(lado="R", a1=3, a2=1, pie=dict(vista="frente"))])
    uf = u * 1.04
    figura(z, Pf, uf, FAMILIAR, "frente", tronco=182, cab=dict(vista="espalda", ang=10),
           brazos=[dict(lado="L", a1=-14, a2=-25, l2=0.5, z=-45, mano=dict(t="nada")), dict(lado="R", a1=14, a2=25, l2=0.5, z=-45, mano=dict(t="nada"))],
           piernas=[dict(lado="L", a1=-3, a2=-1, pie=dict(vista="frente")), dict(lado="R", a1=3, a2=1, pie=dict(vista="frente"))])
    # brazos de Beatriz sobre la espalda del familiar: uno por encima del hombro y otro por debajo del brazo
    SL, SR = Jb["T"](2.12, -0.68), Jb["T"](2.12, 0.68)
    for S, obj, flex, ah, pul in ((SL, (Pf[0] - 0.05 * u, Pf[1] - 1.0 * u), 1, 70, -1),
                                  (SR, (Pf[0] - 0.05 * u, Pf[1] - 1.95 * u), -1, 115, -1)):
        a1, a2 = ik(S, obj, L_BRAZO * u, L_ANTEB * u, flex)
        E = ad(S, D(a1), L_BRAZO * u)
        W = ad(E, D(a2), L_ANTEB * u)
        dib_brazo(z, BEA, u, S, E, W, ah, dict(mano=dict(t="plana", dorso=True, pulgar=pul, abre=4, pul_ang=30)))
    z.guardar()
    return n


def p_bea_prensa():
    n = "bea_prensa"
    w, h, u = 640, 980, 112
    z = _cuadro(n, w, h, DIA)
    suelo = 955
    Pv = (320, suelo - pie_suelo(u))
    sombra_suelo(z, 320, suelo - 6, 1.4 * u)
    figura(z, Pv, u, BEA, "frente", cab=dict(ex="habla", gafas="sol", ang=-3),
           brazos=[dict(lado="L", a1=-6, a2=-2, mano=dict(t="lado", c=0.45, pal=1)),
                   dict(lado="R", obj=(Pv[0] + 0.85 * u, Pv[1] - 1.15 * u), flex=1, ah=150, mano=dict(t="plana", dorso=False, pulgar=1, abre=7, pul_ang=45, curva=0.25))],
           piernas=[dict(lado="L", a1=-3, a2=-1, pie=dict(vista="frente")), dict(lado="R", a1=4, a2=1, pie=dict(vista="frente"))])
    z.guardar()
    return n


def busto(nombre, pj, ex="neutra", vista="frente", casco=False, frontal=None, gafas=None, mojado=False, capas=(), ang=0,
          tronco=180, brazos=None, w=900, h=900, u=300, luz=CAVE):
    z = _cuadro(nombre, w, h, luz)
    N = (w / 2, 570)
    Pv = (N[0], N[1] + 2.38 * u)
    z.defs.append(f'<linearGradient id="pjfade{nombre}" x1="0" y1="0" x2="0" y2="1"><stop offset="0.8" stop-color="#fff"/><stop offset="0.99" stop-color="#000"/></linearGradient>'
                  f'<mask id="pjm{nombre}" maskUnits="userSpaceOnUse" x="0" y="0" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="url(#pjfade{nombre})"/></mask>')
    z(f'<g mask="url(#pjm{nombre})">')
    if brazos is None:
        if vista == "frente":
            brazos = [dict(lado="L", a1=-10, a2=-4, mano=dict(t="nada")), dict(lado="R", a1=10, a2=4, mano=dict(t="nada"))]
        else:
            brazos = [dict(lado="near", a1=-4, a2=0, mano=dict(t="nada")), dict(lado="far", a1=6, a2=4, mano=dict(t="nada"))]
    figura(z, Pv, u, pj, vista, tronco=tronco, cab=dict(ex=ex, casco=casco, frontal=frontal, gafas=gafas, mojado=mojado, ang=ang, esc=1.0),
           capas=capas, brazos=brazos)
    z("</g>")
    z.guardar()
    return nombre


def caras_bea():
    out = [busto("bea_cara_neutra", BEA, "neutra"),
           busto("bea_cara_sorpresa", BEA, "sorpresa", ang=-3),
           busto("bea_cara_ojos_cerrados", BEA, "cerrados", casco=True, frontal="off"),
           busto("bea_cara_rie", BEA, "rie", ang=4),
           busto("bea_cara_miedo", BEA, "miedo", ang=-6, casco=True, frontal="on"),
           busto("bea_cara_parpadea", BEA, "parpadea")]
    C = (450, 570 - 0.76 * 300)
    out.append(busto("bea_cara_luz", BEA, "entrecierra", luz=DIA, ang=-4,
                     brazos=[dict(lado="L", a1=-10, a2=-4, mano=dict(t="nada")),
                             dict(lado="R", obj=(C[0] + 0.42 * 300, C[1] - 0.2 * 300), flex=-1, ah=-80, mano=dict(t="lado", c=0.08, pal=-1, pc=0.0), z=40)]))
    out.append(busto("bea_cara_toalla", BEA, "sonrisa_d", mojado=True, luz=DIA, ang=3, capas=[(15, lambda z, J: toalla(z, J, 300))]))
    return out


# --------------------------------------------------------------------------- Siffre
def caja(z, x, y, w, h):
    m = mat("#8a6a42", "#b8955e", "#4a361e")
    forma(z, f"M{F(x)} {F(y)} L{F(x + w)} {F(y)} L{F(x + w)} {F(y + h)} L{F(x)} {F(y + h)} Z", m, (x, y), (x + w, y + h))
    for k in range(1, 4):
        z(f'<path d="M{F(x)} {F(y + k * h / 4)} L{F(x + w)} {F(y + k * h / 4)}" stroke="{m["s"]}" stroke-width="3" opacity="0.7"/>')
    z(f'<path d="M{F(x)} {F(y)} L{F(x + w)} {F(y)}" stroke="{m["l"]}" stroke-width="4"/>'
      f'<rect x="{F(x + w * 0.08)}" y="{F(y)}" width="{F(w * 0.08)}" height="{F(h)}" fill="{m["s"]}" opacity="0.4"/><rect x="{F(x + w * 0.84)}" y="{F(y)}" width="{F(w * 0.08)}" height="{F(h)}" fill="{m["s"]}" opacity="0.4"/>')


def telefono_campo(z, x, y, s):
    m = mat("#4a5a3a", "#6e8256", "#232c1a")
    forma(z, f"M{F(x)} {F(y)} L{F(x + 1.3 * s)} {F(y)} L{F(x + 1.3 * s)} {F(y + 0.9 * s)} L{F(x)} {F(y + 0.9 * s)} Z", m, (x, y), (x + 1.3 * s, y + 0.9 * s))
    z(f'<rect x="{F(x + 0.15 * s)}" y="{F(y + 0.2 * s)}" width="{F(0.5 * s)}" height="{F(0.3 * s)}" rx="4" fill="{m["s"]}"/>'
      f'<circle cx="{F(x + 1.0 * s)}" cy="{F(y + 0.45 * s)}" r="{F(0.14 * s)}" fill="#2a2a2a"/><path d="M{F(x + 1.0 * s)} {F(y + 0.45 * s)} l{F(0.25 * s)} {F(-0.05 * s)}" stroke="#c9b48a" stroke-width="{F(0.05 * s)}" stroke-linecap="round"/>'
      f'<path d="M{F(x + 1.3 * s)} {F(y + 0.3 * s)} l{F(0.12 * s)} 0" stroke="#c9b48a" stroke-width="{F(0.06 * s)}"/>')


def auricular(z, oreja, boca, u):
    a = math.degrees(math.atan2(boca[0] - oreja[0], boca[1] - oreja[1]))
    n = D(a + 90)
    g = z.lin(ad(oreja, n, 0.1 * u), ad(oreja, n, -0.1 * u), [(0, "#5a5e66"), (0.4, "#22252a"), (1, "#0e0f12")])
    z(f'<path d="M{P(ad(oreja, n, 0.06 * u))} L{P(ad(boca, n, 0.06 * u))} L{P(ad(boca, n, -0.06 * u))} L{P(ad(oreja, n, -0.06 * u))} Z" fill="{g}"/>'
      f'<ellipse cx="{F(oreja[0])}" cy="{F(oreja[1])}" rx="{F(0.15 * u)}" ry="{F(0.11 * u)}" fill="#1a1c20" transform="rotate({F(-a + 90)} {F(oreja[0])} {F(oreja[1])})"/>'
      f'<ellipse cx="{F(boca[0])}" cy="{F(boca[1])}" rx="{F(0.15 * u)}" ry="{F(0.11 * u)}" fill="#1a1c20" transform="rotate({F(-a + 90)} {F(boca[0])} {F(boca[1])})"/>')


def p_siffre_telefono():
    n = "siffre_telefono"
    w, h, u = 980, 940, 112
    z = _cuadro(n, w, h, dict(luz=(-0.6, -0.8), rim="#bfe2ff"))
    suelo = 915
    sombra_suelo(z, 480, suelo - 6, 2.6 * u, 0.3 * u)
    telefono_campo(z, 700, suelo - 0.95 * u, 1.0 * u)
    Pv = (330, suelo - 1.85 * u)
    caja(z, 200, Pv[1] + 0.15 * u, 2.4 * u, suelo - Pv[1] - 0.15 * u)
    tr, ang = 178, -4
    N = Tx(Pv, tr, u, 2.38, 0.1)
    C = (N[0] + 0.08 * u, N[1] - 0.8 * u)
    oreja = (C[0] - 0.2 * u, C[1] + 0.05 * u)
    bocat = (C[0] + 0.2 * u, C[1] + 0.48 * u)

    def tel(z, J):
        auricular(z, oreja, bocat, u)
        z(f'<path d="M{P(bocat)} C{F(bocat[0] + 0.5 * u)} {F(bocat[1] + 2 * u)} {F(650)} {F(suelo - 0.3 * u)} {F(705)} {F(suelo - 0.6 * u)}" fill="none" stroke="#1a1c20" stroke-width="4"/>')
    figura(z, Pv, u, SIFFRE, "tq", tronco=tr, cab=dict(ex="habla", ang=ang, frontal="off"),
           brazos=[dict(lado="near", obj=(oreja[0] + 0.05 * u, oreja[1] + 0.38 * u), flex=-1, ah=160, mano=dict(t="lado", c=0.75, pal=-1), z=33),
                   dict(lado="far", obj=(Pv[0] + 1.6 * u, Pv[1] - 0.3 * u), flex=-1, ah=40, mano=dict(t="lado", c=0.5, pal=1))],
           piernas=[dict(lado="far", obj=(Pv[0] + 1.9 * u, suelo - 0.29 * u), flex=1, pie=dict(ang=0)),
                    dict(lado="near", obj=(Pv[0] + 1.6 * u, suelo - 0.29 * u), flex=1, pie=dict(ang=0), z=15)],
           capas=[(32, tel)])
    z.guardar()
    return n


def p_siffre_cuenta(fot="a"):
    n = f"siffre_cuenta_{fot}"
    w, h, u = 640, 980, 112
    z = _cuadro(n, w, h, dict(luz=(-0.6, -0.8), rim="#bfe2ff"))
    suelo = 955
    Pv = (320, suelo - pie_suelo(u))
    sombra_suelo(z, 320, suelo - 6, 1.4 * u)
    arriba = dict(t="plana", dorso=True, abre=7, pul_ang=10, pul_ext=0.8)
    if fot == "a":
        bl = dict(lado="L", obj=(Pv[0] - 0.55 * u, Pv[1] - 1.5 * u), flex=-1, ah=175, mano=dict(arriba, dedos=(1, 1, 0, 0), pulgar=1))
        br = dict(lado="R", a1=8, a2=2, mano=dict(t="lado", c=0.45, pal=-1))
    else:
        bl = dict(lado="L", a1=-8, a2=-2, mano=dict(t="lado", c=0.45, pal=1))
        br = dict(lado="R", obj=(Pv[0] + 0.55 * u, Pv[1] - 1.5 * u), flex=1, ah=185, mano=dict(arriba, dedos=(1, 1, 1, 0), pulgar=-1))
    figura(z, Pv, u, SIFFRE, "frente", cab=dict(ex="cerrados", ang=-3, frontal="off"), brazos=[bl, br],
           piernas=[dict(lado="L", a1=-3, a2=-1, pie=dict(vista="frente")), dict(lado="R", a1=3, a2=1, pie=dict(vista="frente"))])
    z.guardar()
    return n


def p_siffre_camina():
    n = "siffre_camina"
    w, h, u = 920, 960, 112
    z = _cuadro(n, w, h, dict(luz=(-0.6, -0.8), rim="#bfe2ff"))
    suelo = 935
    Pv = (330, suelo - pie_suelo(u) + 0.07 * u)
    sombra_suelo(z, 340, suelo - 6, 1.6 * u)
    J = _camina(z, Pv, u, SIFFRE, "a", dict(ex="neutra", frontal="on", ang=4))
    C = J["C"]
    a = math.radians(-4)
    k = u * 1.07 / 100
    lp = (C[0] + (37 * math.cos(a) + 40 * math.sin(a)) * k, C[1] + (37 * math.sin(a) - 40 * math.cos(a)) * k)
    haz(z, lp, 98, 520, 0.08 * u, 1.3 * u, 0.42)
    z.guardar()
    return n


def p_siffre_cara():
    return busto("siffre_cara", SIFFRE, "pensativo", vista="tq", luz=dict(luz=(-0.6, -0.8), rim="#bfe2ff"), ang=-4)


# --------------------------------------------------------------------------- otros
def mesa_plegable(z, x, y, w, alto):
    z(f'<path d="M{F(x + 0.1 * w)} {F(y)} L{F(x + 0.85 * w)} {F(y + alto)} M{F(x + 0.9 * w)} {F(y)} L{F(x + 0.15 * w)} {F(y + alto)}" stroke="#5a5e66" stroke-width="6"/>')
    m = mat("#9a7a52", "#c8a878", "#5a4228")
    forma(z, f"M{F(x)} {F(y - 12)} L{F(x + w)} {F(y - 12)} L{F(x + w)} {F(y + 6)} L{F(x)} {F(y + 6)} Z", m, (x, y - 12), (x, y + 6))


def libreta(z, x, y, w):
    z(f'<path d="M{F(x)} {F(y)} L{F(x + w)} {F(y)} L{F(x + w * 0.92)} {F(y - w * 0.22)} L{F(x - w * 0.08)} {F(y - w * 0.22)} Z" fill="#f2ead6" stroke="#b8a888" stroke-width="1"/>')
    for i in range(4):
        yy = y - w * 0.05 - i * w * 0.04
        z(f'<path d="M{F(x + w * 0.05)} {F(yy)} L{F(x + w * 0.8)} {F(yy)}" stroke="#8a8270" stroke-width="1.2" opacity="0.5"/>')


def p_equipo_1962():
    n = "equipo_1962"
    w, h, u = 1000, 900, 112
    z = _cuadro(n, w, h, DIA)
    suelo = 875
    sombra_suelo(z, 500, suelo - 6, 3.2 * u, 0.3 * u)
    Pv = (300, suelo - 1.85 * u)
    # silla plegable
    z(f'<path d="M{F(Pv[0] - 0.6 * u)} {F(suelo)} L{F(Pv[0] + 0.5 * u)} {F(Pv[1] + 0.2 * u)} M{F(Pv[0] + 0.5 * u)} {F(suelo)} L{F(Pv[0] - 0.5 * u)} {F(Pv[1] + 0.2 * u)} '
      f'M{F(Pv[0] - 0.55 * u)} {F(Pv[1] + 0.2 * u)} L{F(Pv[0] - 0.75 * u)} {F(Pv[1] - 1.8 * u)}" stroke="#4a4e56" stroke-width="7" fill="none"/>')
    z(f'<rect x="{F(Pv[0] - 0.7 * u)}" y="{F(Pv[1] + 0.1 * u)}" width="{F(1.3 * u)}" height="{F(0.15 * u)}" fill="#2f5a3a"/>')
    mx = 560
    ytab = Pv[1] - 0.3 * u
    nota = (mx + 0.3 * u, ytab - 14)

    def mesa_y_libreta(z, J):
        pass
    mesa_plegable(z, mx - 0.4 * u, ytab, 3.3 * u, suelo - ytab)
    tr = 168
    N = Tx(Pv, tr, u, 2.38, 0.1)

    def auriculares(z, J):
        C = J["C"]
        k = u * 1.07 / 100
        a = math.radians(-(tr - 10 - 180))
        ox, oy = -22, 2
        o = (C[0] + (ox * math.cos(a) - oy * math.sin(a)) * k, C[1] + (ox * math.sin(a) + oy * math.cos(a)) * k)
        z(f'<path d="M{F(o[0] - 0.05 * u)} {F(o[1] - 0.05 * u)} C{F(o[0] - 0.1 * u)} {F(o[1] - 0.6 * u)} {F(o[0] + 0.3 * u)} {F(o[1] - 0.75 * u)} {F(o[0] + 0.45 * u)} {F(o[1] - 0.55 * u)}" fill="none" stroke="#2a2a2e" stroke-width="{F(0.05 * u)}"/>'
          f'<ellipse cx="{F(o[0])}" cy="{F(o[1])}" rx="{F(0.11 * u)}" ry="{F(0.15 * u)}" fill="#1e1f24"/><ellipse cx="{F(o[0] - 0.02 * u)}" cy="{F(o[1] - 0.03 * u)}" rx="{F(0.05 * u)}" ry="{F(0.07 * u)}" fill="#4a4e56"/>'
          f'<path d="M{F(o[0])} {F(o[1] + 0.15 * u)} C{F(o[0] - 0.2 * u)} {F(o[1] + 1.5 * u)} {F(mx + 2.2 * u)} {F(ytab + 0.2 * u)} {F(mx + 2.4 * u)} {F(ytab - 0.3 * u)}" fill="none" stroke="#1e1f24" stroke-width="3"/>')
    J = figura(z, Pv, u, EQ62, "tq", tronco=tr, cab=dict(ex="concentrada", ang=-10, gafas="vista", extra_del=""),
               brazos=[dict(lado="far", obj=(nota[0] + 0.9 * u, nota[1] - 0.05 * u), flex=-1, ah=95, mano=dict(t="plana", dorso=True, pulgar=-1, abre=2, pul_ang=15)),
                       dict(lado="near", obj=(nota[0] + 0.1 * u, nota[1] - 0.05 * u), flex=1, ah=80, mano=dict(t="lado", c=0.7, pal=1, objeto=lambda z, W, ah: lapiz(z, W, ah, u)), z=40)],
               piernas=[dict(lado="far", obj=(Pv[0] + 1.75 * u, suelo - 0.29 * u), flex=1, pie=dict(ang=0)),
                        dict(lado="near", obj=(Pv[0] + 1.45 * u, suelo - 0.29 * u), flex=1, pie=dict(ang=0))],
               capas=[(35, lambda z, J: libreta(z, nota[0] - 0.2 * u, nota[1] + 6, 1.4 * u)), (25, auriculares)])
    # aparato receptor sobre la mesa
    z(f'<rect x="{F(mx + 2.0 * u)}" y="{F(ytab - 0.75 * u)}" width="{F(1.0 * u)}" height="{F(0.65 * u)}" rx="6" fill="#4a5a3a"/>'
      f'<circle cx="{F(mx + 2.3 * u)}" cy="{F(ytab - 0.45 * u)}" r="{F(0.12 * u)}" fill="#1e1f24"/><circle cx="{F(mx + 2.7 * u)}" cy="{F(ytab - 0.45 * u)}" r="{F(0.12 * u)}" fill="#1e1f24"/>'
      f'<rect x="{F(mx + 2.0 * u)}" y="{F(ytab - 0.75 * u)}" width="{F(1.0 * u)}" height="{F(0.08 * u)}" fill="#7a8a62"/>')
    z.guardar()
    return n


def p_equipo_frontal(fot="a"):
    n = f"equipo_frontal_{fot}"
    w, h, u = 1200, 980, 108
    z = Lz(n, w, h, luz=(0.7, -0.6), rim="#ffcf8a", rimk=1.0)
    suelo = 955
    sombra_suelo(z, 600, suelo - 6, 4 * u, 0.3 * u)
    for i, (x, f2) in enumerate(((300, fot), (720, "b" if fot == "a" else "a"))):
        Pv = (x, suelo - pie_suelo(u) + 0.07 * u)
        J = _camina(z, Pv, u, ESPELEO, f2, dict(ex="neutra", casco=True, frontal="on", ang=4), mochila="#4a3a2a")
        haz(z, lampara_pos(J, u * 1.07, "perfil", -4), 98, 420 if i == 0 else 360, 0.08 * u, 1.1 * u, 0.4)
    z.guardar()
    return n


def p_voluntario(i):
    n = f"voluntario_{i + 1}"
    pj = VOLS[i]
    w, h, u = 520, 940, 108
    z = _cuadro(n, w, h)
    suelo = 915
    Pv = (260, suelo - pie_suelo(u))
    sombra_suelo(z, 260, suelo - 6, 1.3 * u)
    poses = [
        ([dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)), dict(lado="R", a1=7, a2=3, mano=dict(t="lado", c=0.45, pal=-1))], "sonrisa"),
        ([dict(lado="L", obj=(Pv[0] + 0.3 * u, Pv[1] - 1.0 * u), flex=-1, ah=80, mano=dict(t="lado", c=0.5, pal=1)),
          dict(lado="R", obj=(Pv[0] - 0.25 * u, Pv[1] - 1.1 * u), flex=1, ah=-80, mano=dict(t="lado", c=0.5, pal=-1), z=31)], "neutra"),
        ([dict(lado="L", a1=-5, a2=-2, mano=dict(t="lado", c=0.45, pal=1)), dict(lado="R", a1=10, a2=20, mano=dict(t="lado", c=0.5, pal=-1))], "sonrisa"),
        ([dict(lado="L", a1=-12, a2=30, ah=40, mano=dict(t="lado", c=0.6, pal=1)), dict(lado="R", a1=7, a2=3, mano=dict(t="lado", c=0.45, pal=-1))], "sonrisa_d"),
        ([dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)), dict(lado="R", a1=30, a2=150, ah=170, mano=dict(t="plana", dorso=False, pulgar=1, abre=8, pul_ang=45))], "sonrisa_d"),
        ([dict(lado="L", a1=-20, a2=12, mano=dict(t="lado", c=0.6, pal=1)), dict(lado="R", a1=20, a2=-12, mano=dict(t="lado", c=0.6, pal=-1))], "neutra"),
    ]
    br, ex = poses[i]
    figura(z, Pv, u, pj, "frente", cab=dict(ex=ex, ang=[-3, 4, -2, 5, -4, 2][i]), brazos=br,
           piernas=[dict(lado="L", a1=-3, a2=-1, pie=dict(vista="frente")), dict(lado="R", a1=3 + i % 3, a2=1, pie=dict(vista="frente"))],
           ancho=[1.0, 0.95, 1.08, 0.97, 1.0, 1.02][i])
    z.guardar()
    return n


def p_nino_corre():
    n = "nino_corre"
    w, h, u = 700, 760, 82
    z = _cuadro(n, w, h, DIA)
    suelo = 735
    Pv = (330, suelo - pie_suelo(u) * 0.8 - 0.35 * u)
    sombra_suelo(z, 340, suelo - 6, 1.6 * u)
    figura(z, Pv, u, NINO, "perfil", tronco=166, alto=0.82, cab=dict(ex="sonrisa_d", esc=1.45, ang=16),
           brazos=[dict(lado="near", a1=-40, a2=40, l1=0.82, l2=0.82, ah=60, mano=dict(t="lado", c=0.8, pal=1)),
                   dict(lado="far", a1=40, a2=130, l1=0.82, l2=0.82, ah=150, mano=dict(t="lado", c=0.8, pal=1))],
           piernas=[dict(lado="near", a1=60, a2=-5, l1=0.8, l2=0.8, pie=dict(ang=10)), dict(lado="far", a1=-28, a2=-80, l1=0.8, l2=0.8, pie=dict(ang=-60))])
    z.guardar()
    return n


def p_adulto_pantalla():
    n = "adulto_pantalla"
    w, h, u = 1100, 900, 108
    z = Lz(n, w, h, luz=(0.8, -0.35), rim="#ffcf8a")
    suelo = 875
    sombra_suelo(z, 550, suelo - 6, 3.4 * u, 0.3 * u)
    Pv = (330, suelo - 1.85 * u)
    # silla de oficina
    z(f'<path d="M{F(Pv[0] - 0.7 * u)} {F(suelo - 0.15 * u)} L{F(Pv[0] + 0.7 * u)} {F(suelo - 0.15 * u)} M{F(Pv[0])} {F(suelo - 0.15 * u)} L{F(Pv[0])} {F(Pv[1] + 0.4 * u)}" stroke="#2a2c32" stroke-width="10"/>'
      f'<circle cx="{F(Pv[0] - 0.7 * u)}" cy="{F(suelo - 0.07 * u)}" r="9" fill="#1a1b1f"/><circle cx="{F(Pv[0] + 0.7 * u)}" cy="{F(suelo - 0.07 * u)}" r="9" fill="#1a1b1f"/>'
      f'<rect x="{F(Pv[0] - 0.8 * u)}" y="{F(Pv[1] + 0.2 * u)}" width="{F(1.5 * u)}" height="{F(0.25 * u)}" rx="10" fill="#2f3138"/>'
      f'<path d="M{F(Pv[0] - 0.75 * u)} {F(Pv[1] + 0.25 * u)} L{F(Pv[0] - 0.95 * u)} {F(Pv[1] - 2.2 * u)}" stroke="#2f3138" stroke-width="{F(0.35 * u)}" stroke-linecap="round"/>')
    mx = 640
    ytab = Pv[1] - 0.15 * u
    # mesa
    m = mat("#6a5a4a", "#9a8670", "#3a2e22")
    forma(z, f"M{F(mx)} {F(ytab)} L{F(mx + 3.6 * u)} {F(ytab)} L{F(mx + 3.6 * u)} {F(ytab + 0.18 * u)} L{F(mx)} {F(ytab + 0.18 * u)} Z", m, (mx, ytab), (mx, ytab + 20))
    z(f'<rect x="{F(mx + 3.2 * u)}" y="{F(ytab + 0.18 * u)}" width="{F(0.2 * u)}" height="{F(suelo - ytab - 0.18 * u)}" fill="{m["s"]}"/>'
      f'<rect x="{F(mx + 0.2 * u)}" y="{F(ytab + 0.18 * u)}" width="{F(0.2 * u)}" height="{F(suelo - ytab - 0.18 * u)}" fill="{m["s"]}"/>')
    # monitor de perfil con resplandor
    sx = mx + 2.6 * u
    g = z.rad((sx - 0.2 * u, ytab - 1.4 * u), 2.4 * u, [(0, "#a8d8ff", 0.45), (1, "#a8d8ff", 0)])
    z(f'<circle cx="{F(sx - 0.2 * u)}" cy="{F(ytab - 1.4 * u)}" r="{F(2.4 * u)}" fill="{g}"/>')
    z(f'<path d="M{F(sx)} {F(ytab)} L{F(sx + 0.1 * u)} {F(ytab - 0.6 * u)}" stroke="#2a2c32" stroke-width="{F(0.12 * u)}"/>'
      f'<rect x="{F(sx - 0.25 * u)}" y="{F(ytab - 0.05 * u)}" width="{F(0.6 * u)}" height="{F(0.06 * u)}" fill="#2a2c32"/>'
      f'<path d="M{F(sx - 0.1 * u)} {F(ytab - 2.4 * u)} L{F(sx + 0.15 * u)} {F(ytab - 2.4 * u)} L{F(sx + 0.15 * u)} {F(ytab - 0.55 * u)} L{F(sx - 0.1 * u)} {F(ytab - 0.55 * u)} Z" fill="#1a1c22"/>'
      f'<path d="M{F(sx - 0.1 * u)} {F(ytab - 2.4 * u)} L{F(sx - 0.1 * u)} {F(ytab - 0.55 * u)}" stroke="#cfeaff" stroke-width="5"/>')
    tr = 166
    figura(z, Pv, u, OFICINA, "perfil", tronco=tr, cab=dict(ex="cansado", ang=10),
           brazos=[dict(lado="far", obj=(mx + 1.0 * u, ytab - 0.2 * u), flex=-1, ah=95, mano=dict(t="plana", dorso=True, pulgar=-1, abre=2, pul_ang=10)),
                   dict(lado="near", obj=(mx + 0.7 * u, ytab - 0.15 * u), flex=1, ah=90, mano=dict(t="lado", c=0.5, pal=1))],
           piernas=[dict(lado="far", obj=(Pv[0] + 1.75 * u, suelo - 0.29 * u), flex=1, pie=dict(ang=0)),
                    dict(lado="near", obj=(Pv[0] + 1.5 * u, suelo - 0.29 * u), flex=1, pie=dict(ang=0))],
           capas=[(35, lambda z, J: z(f'<ellipse cx="{F(mx + 1.15 * u)}" cy="{F(ytab - 0.06 * u)}" rx="{F(0.18 * u)}" ry="{F(0.07 * u)}" fill="#2a2c32"/>'))])
    z.guardar()
    return n


def movil(z, W, ah, u):
    c = ad(W, D(ah), 0.28 * u)
    a = -ah + 60
    z(f'<g transform="translate({F(c[0])} {F(c[1])}) rotate({F(a)})"><rect x="{F(-0.12 * u)}" y="{F(-0.22 * u)}" width="{F(0.24 * u)}" height="{F(0.44 * u)}" rx="{F(0.04 * u)}" fill="#15171b"/>'
      f'<rect x="{F(-0.1 * u)}" y="{F(-0.19 * u)}" width="{F(0.2 * u)}" height="{F(0.38 * u)}" rx="{F(0.02 * u)}" fill="#8fc8ff"/></g>')


def p_adulto_camina():
    n = "adulto_camina"
    w, h, u = 760, 960, 112
    z = _cuadro(n, w, h, DIA)
    suelo = 935
    Pv = (330, suelo - pie_suelo(u) + 0.07 * u)
    sombra_suelo(z, 340, suelo - 6, 1.6 * u)
    N = Tx(Pv, 182, u, 2.38, 0.15)
    tel = (N[0] + 0.7 * u, N[1] + 1.05 * u)
    figura(z, Pv, u, PASEO, "perfil", tronco=182, cab=dict(ex="cansado", ang=-20),
           brazos=[dict(lado="near", obj=tel, flex=-1, ah=130, mano=dict(t="lado", c=0.55, pal=1, objeto=lambda z, W, ah: movil(z, W, ah, u))),
                   dict(lado="far", a1=-18, a2=-8, mano=dict(t="lado", c=0.5, pal=1))],
           piernas=[dict(lado="near", a1=22, a2=4, pie=dict(ang=10)), dict(lado="far", a1=-16, a2=-38, pie=dict(ang=-22))])
    z.guardar()
    return n


def p_bebe():
    n = "bebe"
    w, h, u = 520, 560, 120
    z = _cuadro(n, w, h, DIA)
    suelo = 535
    Pv = (260, suelo - 0.55 * u)
    sombra_suelo(z, 260, suelo - 8, 1.7 * u, 0.3 * u)
    figura(z, Pv, u * 0.6, BEBE, "frente", alto=0.75, ancho=1.25, cab=dict(ex="sonrisa_d", esc=2.15, ang=-6),
           brazos=[dict(lado="L", a1=-30, a2=20, l1=0.7, l2=0.7, ah=40, mano=dict(t="lado", c=0.6, pal=1)),
                   dict(lado="R", a1=40, a2=-10, l1=0.7, l2=0.7, ah=-40, mano=dict(t="lado", c=0.6, pal=-1))],
           piernas=[dict(lado="L", a1=-60, a2=-20, l1=0.65, l2=0.6, z=12, pie=dict(vista="lado", dir=-1, ang=40)),
                    dict(lado="R", a1=60, a2=20, l1=0.65, l2=0.6, z=12, pie=dict(vista="lado", dir=1, ang=40))])
    z.guardar()
    return n


PIEZAS = {
    "bea_baja_cuerda": p_bea_baja_cuerda,
    "bea_despide": p_bea_despide,
    "bea_camina": lambda: [p_bea_camina("a"), p_bea_camina("b")],
    "bea_lee": lambda: [p_bea_lee("a"), p_bea_lee("b")],
    "bea_duerme": p_bea_duerme,
    "bea_marca": lambda: [p_bea_marca("a"), p_bea_marca("b")],
    "bea_teje": lambda: [p_bea_teje("a"), p_bea_teje("b")],
    "bea_ejercicio": lambda: [p_bea_ejercicio("a"), p_bea_ejercicio("b")],
    "bea_bebe": p_bea_bebe,
    "bea_dibuja": p_bea_dibuja,
    "bea_habla": lambda: [p_bea_habla("a"), p_bea_habla("b")],
    "bea_oye": p_bea_oye,
    "bea_moscas": p_bea_moscas,
    "bea_sujetada": p_bea_sujetada,
    "bea_abraza": p_bea_abraza,
    "bea_prensa": p_bea_prensa,
    "caras": caras_bea,
    "siffre_telefono": p_siffre_telefono,
    "siffre_cuenta": lambda: [p_siffre_cuenta("a"), p_siffre_cuenta("b")],
    "siffre_camina": p_siffre_camina,
    "siffre_cara": p_siffre_cara,
    "equipo_1962": p_equipo_1962,
    "equipo_frontal": lambda: [p_equipo_frontal("a"), p_equipo_frontal("b")],
    "voluntarios": lambda: [p_voluntario(i) for i in range(6)],
    "nino_corre": p_nino_corre,
    "adulto_pantalla": p_adulto_pantalla,
    "adulto_camina": p_adulto_camina,
    "bebe": p_bebe,
}


def generar(dirsvg):
    ilus.OUT = dirsvg
    nombres = []
    for k, fn in PIEZAS.items():
        r = fn()
        nombres += r if isinstance(r, list) else [r]
    return nombres


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "."))
