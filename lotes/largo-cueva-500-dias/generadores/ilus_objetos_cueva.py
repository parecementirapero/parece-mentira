"""Objetos de la vida en la cueva y de la naturaleza de la cueva («500 días en una cueva»).

Uso:  from ilus_objetos_cueva import generar; generar(DIR_SVG)          → lista de nombres
      python3 -m lotes.largo-cueva-500-dias... (o)  python3 ilus_objetos_cueva.py DIR_SVG [--sin-sombra]
Estilo v4 (ver ../ARTE.md): volumen con degradados, luz cálida desde arriba-izquierda, luz de borde fría
abajo-derecha, grano y sombra de contacto (se quita con generar(dir, sombra=False)).
Todos los ids llevan el prefijo «oc<nombre>_» para no chocar con otras piezas.
"""
import math, os, random, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar  # noqa: E402

LUZ, LUZ2, RIM = "#ffcf8a", "#ffb15e", "#8fb6e6"
SOMBRA = True
HECHAS = []


def F(v):
    return f"{v:.1f}"


def poly(ps):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in ps) + " Z"


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def dn(q, k):
    return (q[0], q[1] + k)


class P:
    """Acumula defs y cuerpo de una pieza; ids únicos con prefijo propio."""

    def __init__(s, n, w, h):
        s.n, s.w, s.h, s.d, s.b, s.i = n, w, h, [], [], 0

    def __call__(s, *xs):
        s.b.extend(xs)

    def nid(s, t="g"):
        s.i += 1
        return f"oc{s.n}_{t}{s.i}"

    def lin(s, *stops, x1=0, y1=0, x2=0, y2=1, us=False):
        i = s.nid("l")
        st = "".join(f'<stop offset="{o[0]}" stop-color="{o[1]}" stop-opacity="{o[2] if len(o) > 2 else 1}"/>' for o in stops)
        u = ' gradientUnits="userSpaceOnUse"' if us else ""
        s.d.append(f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{u}>{st}</linearGradient>')
        return f"url(#{i})"

    def rad(s, *stops, cx=0.5, cy=0.5, r=0.5, fx=None, fy=None, us=False):
        i = s.nid("r")
        st = "".join(f'<stop offset="{o[0]}" stop-color="{o[1]}" stop-opacity="{o[2] if len(o) > 2 else 1}"/>' for o in stops)
        u = ' gradientUnits="userSpaceOnUse"' if us else ""
        f = f' fx="{fx}" fy="{fy}"' if fx is not None else ""
        s.d.append(f'<radialGradient id="{i}" cx="{cx}" cy="{cy}" r="{r}"{f}{u}>{st}</radialGradient>')
        return f"url(#{i})"

    def clip(s, *ds):
        i = s.nid("c")
        s.d.append(f'<clipPath id="{i}">' + "".join(f'<path d="{d}"/>' for d in ds) + "</clipPath>")
        return f"url(#{i})"

    def filtro(s, cuerpo, x="-20%", y="-20%", w="140%", h="140%"):
        i = s.nid("f")
        s.d.append(f'<filter id="{i}" x="{x}" y="{y}" width="{w}" height="{h}">{cuerpo}</filter>')
        return f"url(#{i})"

    def grano(s, *ds, op=1.0):
        c = s.clip(*ds)
        s(f'<g clip-path="{c}" opacity="{op}"><rect width="{s.w}" height="{s.h}" fill="#888" filter="url(#grano)"/></g>')

    def vol(s, d, fill, k=6, luz=LUZ, lo=0.45, rim=RIM, ro=0.5, gr=True, extra=""):
        """Relleno + grano + media luna cálida arriba-izquierda + luz de borde fría abajo-derecha."""
        s(f'<path d="{d}" fill="{fill}" {extra}/>')
        if gr:
            s.grano(d)
        if lo:
            m = s.nid("m")
            s.d.append(f'<mask id="{m}"><path d="{d}" fill="#fff"/><path d="{d}" transform="translate({k} {k})" fill="#000"/></mask>')
            s(f'<path d="{d}" fill="{luz}" opacity="{lo}" mask="url(#{m})"/>')
        if ro:
            m = s.nid("m")
            kk = k * 0.7
            s.d.append(f'<mask id="{m}"><path d="{d}" fill="#fff"/><path d="{d}" transform="translate({-kk} {-kk})" fill="#000"/></mask>')
            s(f'<path d="{d}" fill="{rim}" opacity="{ro}" mask="url(#{m})"/>')

    def sombra(s, cx, cy, rx, ry, op=0.5):
        if SOMBRA:
            s(f'<ellipse cx="{F(cx)}" cy="{F(cy)}" rx="{F(rx)}" ry="{F(ry)}" fill="#05060a" opacity="{op}" filter="url(#blur8)"/>')

    def sombra_d(s, d, op=0.45, dx=6, dy=6):
        if SOMBRA:
            s(f'<path d="{d}" transform="translate({dx} {dy})" fill="#05060a" opacity="{op}" filter="url(#blur8)"/>')

    def fin(s):
        guardar(s.n, "".join(s.b), s.w, s.h, "".join(s.d))
        HECHAS.append(s.n)
        return s.n


def esfera(p, cx, cy, r, op=0.6, clip=None):
    """Sombreado de volumen esférico encima de lo que haya (oscurece abajo-derecha)."""
    g = p.rad((0, "#000", 0), (0.55, "#000", 0.08), (1, "#000", op), cx=0.38, cy=0.34, r=0.72)
    c = f' clip-path="{clip}"' if clip else ""
    p(f'<circle cx="{F(cx)}" cy="{F(cy)}" r="{F(r)}" fill="{g}"{c}/>')


# ============================================================== 1. LIBROS
def _libro(p, col, t, sem):
    base, claro, osc, deco = col
    r = random.Random(sem)
    dy = (176 - t) - 118
    P1, P2, P3, P4 = (24, 62 + dy), (352, 28 + dy), (496, 84 + dy), (168, 118 + dy)
    p.sombra_d(poly([dn(P1, t), dn(P2, t), dn(P3, t), dn(P4, t)]), op=0.5, dx=8, dy=5)
    # canto de páginas (cara izquierda)
    ux, uy = (P2[0] - P1[0]), (P2[1] - P1[1])
    L = math.hypot(ux, uy); ux, uy = ux / L * 5, uy / L * 5
    p(f'<path d="{poly([P1, P4, dn(P4, t), dn(P1, t)])}" fill="{osc}"/>')
    pag = [(P1[0] + ux, P1[1] + uy + 5), (P4[0] + ux, P4[1] + uy + 5), (P4[0] + ux, P4[1] + uy + t - 5), (P1[0] + ux, P1[1] + uy + t - 5)]
    p(f'<path d="{poly(pag)}" fill="{p.lin((0, "#fbf0d6"), (1, "#cdb88c"))}"/>')
    for k in range(8, t - 6, 3):
        a, b = (pag[0][0], P1[1] + uy + k), (pag[1][0], P4[1] + uy + k)
        p(f'<path d="M{F(a[0])} {F(a[1])} L{F(b[0])} {F(b[1])}" stroke="#8a7350" stroke-width="0.9" opacity="{r.uniform(0.2, 0.5):.2f}"/>')
    p(f'<path d="M{F(pag[0][0])} {F(pag[0][1] + 1)} L{F(pag[1][0])} {F(pag[1][1] + 1)}" stroke="#3a2a18" stroke-width="2.5" opacity="0.5"/>')
    p(f'<path d="{poly(pag)}" fill="{LUZ}" opacity="0.18"/>')
    # lomo (cara frontal), redondeado
    mx, my = (P4[0] + P3[0]) / 2, (P4[1] + P3[1]) / 2
    nx, ny = 0.103, 0.995
    g = p.lin((0, claro), (0.22, base), (0.75, osc), (1, "#0d0806"), x1=F(mx), y1=F(my), x2=F(mx + nx * t), y2=F(my + ny * t), us=True)
    lomo = (f"M{F(P4[0])} {F(P4[1])} L{F(P3[0])} {F(P3[1])} L{F(P3[0])} {F(P3[1] + t)} L{F(P4[0])} {F(P4[1] + t)} "
            f"Q{F(P4[0] - 9)} {F(P4[1] + t / 2)} {F(P4[0])} {F(P4[1])} Z")
    p.vol(lomo, g, k=4, lo=0.25, ro=0.55)
    for u in (0.1, 0.28, 0.72, 0.9):
        a, b = lerp(P4, P3, u - 0.018), lerp(P4, P3, u + 0.018)
        p(f'<path d="{poly([a, b, dn(b, t), dn(a, t)])}" fill="#000" opacity="0.18"/>'
          f'<path d="M{F(a[0] + 2)} {F(a[1] + 2)} L{F(a[0] + 2)} {F(a[1] + t - 2)}" stroke="{claro}" stroke-width="3" opacity="0.8" stroke-linecap="round"/>'
          f'<path d="M{F(b[0])} {F(b[1] + 2)} L{F(b[0])} {F(b[1] + t - 2)}" stroke="#0d0806" stroke-width="2" opacity="0.6"/>')
        for e in (-0.035, 0.035):
            c = lerp(P4, P3, u + e)
            p(f'<path d="M{F(c[0])} {F(c[1] + 3)} L{F(c[0])} {F(c[1] + t - 3)}" stroke="{deco}" stroke-width="1.3" opacity="0.75"/>')
    c1, c2 = lerp(P4, P3, 0.38), lerp(P4, P3, 0.62)  # cartela lisa sin letras
    p(f'<path d="{poly([dn(c1, t * 0.3), dn(c2, t * 0.3), dn(c2, t * 0.7), dn(c1, t * 0.7)])}" fill="none" stroke="{deco}" stroke-width="1.4" opacity="0.7"/>')
    # tapa (cara superior)
    tapa = poly([P1, P2, P3, P4])
    p.vol(tapa, p.lin((0, claro), (0.45, base), (1, osc), x2=1, y2=1), k=5, lo=0.35, ro=0.35)
    C = ((P1[0] + P2[0] + P3[0] + P4[0]) / 4, (P1[1] + P2[1] + P3[1] + P4[1]) / 4)
    inn = [lerp(C, q, 0.8) for q in (P1, P2, P3, P4)]
    p(f'<path d="{poly(inn)}" fill="none" stroke="#000" stroke-width="2.4" opacity="0.35"/>'
      f'<path d="{poly(inn)}" transform="translate(1.5 1.6)" fill="none" stroke="{claro}" stroke-width="1.4" opacity="0.5"/>')
    inn2 = [lerp(C, q, 0.42) for q in (P1, P2, P3, P4)]
    p(f'<path d="{poly(inn2)}" fill="none" stroke="{deco}" stroke-width="1.3" opacity="0.5"/>')
    for _ in range(14):  # desgaste
        q = lerp(lerp(P1, P2, r.random()), lerp(P4, P3, r.random()), r.random())
        p(f'<ellipse cx="{F(q[0])}" cy="{F(q[1])}" rx="{r.uniform(3, 12):.1f}" ry="{r.uniform(1, 3):.1f}" fill="{claro}" opacity="{r.uniform(0.08, 0.2):.2f}" transform="rotate(-6 {F(q[0])} {F(q[1])})"/>')
    p(f'<path d="M{F(P1[0])} {F(P1[1])} L{F(P4[0])} {F(P4[1])} L{F(P3[0])} {F(P3[1])}" fill="none" stroke="{claro}" stroke-width="2" opacity="0.7"/>'
      f'<path d="M{F(P2[0])} {F(P2[1])} L{F(P3[0])} {F(P3[1])} L{F(P3[0])} {F(P3[1] + t)}" fill="none" stroke="{RIM}" stroke-width="2.2" opacity="0.6"/>')


def libros():
    cols = {"libro_a": (("#8c2f22", "#c8603f", "#45140c", "#d9a94e"), 46, 1),
            "libro_b": (("#2f5a3a", "#64955f", "#122a18", "#cfae5c"), 36, 2),
            "libro_c": (("#2b3f6b", "#5d79b0", "#111b36", "#c9b26a"), 56, 3),
            "libro_d": (("#a8782a", "#ddae55", "#553a0f", "#6a2a18"), 40, 4)}
    for n, (col, t, sem) in cols.items():
        p = P(n, 520, 200)
        _libro(p, col, t, sem)
        p.fin()


def libro_abierto():
    p = P("libro_abierto", 720, 380)
    r = random.Random(12)
    p.sombra(360, 345, 330, 18, 0.55)
    for sg in (1, -1):
        X = (lambda x: x) if sg == 1 else (lambda x: 720 - x)
        cov = poly([(X(360), 102), (X(26), 80), (X(30), 322), (X(360), 340)])
        p.vol(cov, p.lin((0, "#9a3326"), (1, "#4a120c")), k=4, lo=0.3, ro=0.4 if sg == -1 else 0)
        for k in (3, 2, 1):
            d = (f"M{X(360)} {92 + 4 * k} C{X(330)} {48 + 4 * k} {X(200)} {38 + 4 * k} {X(40 - 3 * k)} {70 + 4 * k} "
                 f"L{X(46 - 3 * k)} {300 + 4 * k} C{X(200)} {270 + 4 * k} {X(330)} {280 + 4 * k} {X(360)} {318 + 4 * k} Z")
            p(f'<path d="{d}" fill="#d9c69c" stroke="#a8916a" stroke-width="1"/>')
    # páginas
    def curva(s, top, sg):
        if top:
            P0, C1, C2, P3_ = (360, 92), (330, 48), (200, 38), (40, 70)
        else:
            P0, C1, C2, P3_ = (360, 318), (330, 280), (200, 270), (46, 300)
        x = (1 - s) ** 3 * P0[0] + 3 * (1 - s) ** 2 * s * C1[0] + 3 * (1 - s) * s * s * C2[0] + s ** 3 * P3_[0]
        y = (1 - s) ** 3 * P0[1] + 3 * (1 - s) ** 2 * s * C1[1] + 3 * (1 - s) * s * s * C2[1] + s ** 3 * P3_[1]
        return (x if sg == 1 else 720 - x, y)
    for sg in (1, -1):
        X = (lambda x: x) if sg == 1 else (lambda x: 720 - x)
        d = (f"M{X(360)} 92 C{X(330)} 48 {X(200)} 38 {X(40)} 70 L{X(46)} 300 C{X(200)} 270 {X(330)} 280 {X(360)} 318 Z")
        if sg == 1:
            g = p.lin((0, "#efe1c0"), (0.72, "#f8efd9"), (0.9, "#dccaa2"), (1, "#a08a64"), x2=1, y2=0)
        else:
            g = p.lin((0, "#94805c"), (0.1, "#d2bf98"), (0.32, "#f1e5cb"), (1, "#e2d1ac"), x2=1, y2=0)
        p.vol(d, g, k=4, lo=0.25 if sg == 1 else 0, ro=0.4 if sg == -1 else 0)
        for i in range(17):
            if i in (6, 12) or r.random() < 0.04:
                continue
            v = 0.09 + 0.82 * i / 16
            fin = 0.9 if i not in (5, 11, 16) else r.uniform(0.35, 0.6)
            ss = [0.1 + (fin - 0.1) * j / 11 for j in range(12)]
            if sg == 1:
                ss = [0.92 - (0.92 - (1 - fin + 0.02)) * j / 11 for j in range(12)]
            pts = [lerp(curva(s, True, sg), curva(s, False, sg), v) for s in ss]
            dash = " ".join(f"{r.uniform(8, 38):.0f} {r.uniform(4, 7):.0f}" for _ in range(10))
            p(f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in pts)}" fill="none" stroke="#6e655a" stroke-width="2.3" '
              f'stroke-dasharray="{dash}" opacity="0.5"/>')
    p(f'<path d="M360 92 L360 318" stroke="#5a4630" stroke-width="2" opacity="0.6"/>'
      f'<path d="M356 316 C352 336 362 352 354 372 L364 368 L370 374 C374 352 364 336 366 318 Z" fill="#b8242a"/>')
    p.fin()


# ============================================================== 3. VELA
def _llama(p, cx, base, tip, an, glow=True, sx=0):
    tx, ty = tip
    if glow:
        p(f'<circle cx="{cx}" cy="{F((base + ty) / 2)}" r="{F((base - ty) * 0.95)}" fill="{p.rad((0, LUZ, 0.55), (0.35, LUZ2, 0.22), (1, LUZ2, 0))}"/>')
    h = base - ty
    out = (f"M{cx} {base} C{F(cx - an)} {base - 2} {F(cx - an * 1.1)} {F(base - h * 0.38)} {F(cx - an * 0.55 + sx * 0.3)} {F(base - h * 0.6)} "
           f"C{F(cx - an * 0.25 + sx * 0.6)} {F(base - h * 0.78)} {F(tx - 1)} {F(ty + h * 0.1)} {F(tx)} {F(ty)} "
           f"C{F(tx + 3)} {F(ty + h * 0.16)} {F(cx + an * 0.5 + sx * 0.6)} {F(base - h * 0.62)} {F(cx + an * 0.9 + sx * 0.2)} {F(base - h * 0.4)} "
           f"C{F(cx + an * 1.15)} {F(base - h * 0.2)} {F(cx + an)} {base - 2} {cx} {base} Z")
    p(f'<path d="{out}" fill="{p.lin((0, "#fff3c0"), (0.45, "#ffc24a"), (0.8, "#ff8a1a"), (1, "#e0541a"), x1=0, y1=1, x2=0, y2=0)}" opacity="0.95"/>')
    s = 0.55
    hi = base - h * 0.08
    inn = (f"M{cx} {hi} C{F(cx - an * s)} {hi - 2} {F(cx - an * s * 1.05)} {F(hi - h * s * 0.45)} {F((cx + tx) / 2)} {F(hi - h * s * 0.9)} "
           f"C{F(cx + an * s * 1.05)} {F(hi - h * s * 0.45)} {F(cx + an * s)} {hi - 2} {cx} {hi} Z")
    p(f'<path d="{inn}" fill="#fffbe8"/>')
    p(f'<ellipse cx="{cx}" cy="{F(base - 5)}" rx="{F(an * 0.5)}" ry="{F(h * 0.07)}" fill="#3d6dff" opacity="0.55"/>')


def _vela(n, alto, tip, an, sx):
    w, h = 200, 560
    p = P(n, w, h)
    r = random.Random(31)
    cx, rb, yb = 100, 38, 500
    top = yb - alto
    p.sombra(cx, 528, 92, 12, 0.55)
    # platillo
    p.vol("M18 512 C18 530 182 530 182 512 L176 520 C170 540 30 540 24 520 Z", p.lin((0, "#c99a52"), (1, "#5a3c18")), k=3, lo=0.2, ro=0.4)
    p(f'<ellipse cx="{cx}" cy="510" rx="82" ry="19" fill="{p.lin((0, "#f0c878"), (0.5, "#a87830"), (1, "#5c3c14"), x2=1, y2=0.3)}"/>'
      f'<ellipse cx="{cx}" cy="510" rx="68" ry="14" fill="#7a5420"/><ellipse cx="{cx}" cy="511" rx="64" ry="12" fill="{p.lin((0, "#c89850"), (1, "#8a6028"), x2=1, y2=0)}"/>')
    # charco de cera sobre el platillo
    charco = f"M{cx - 58} 508 C{cx - 62} 498 {cx - 40} 496 {cx - 30} 498 L{cx + 34} 497 C{cx + 52} 495 {cx + 62} 502 {cx + 50} 512 C{cx + 20} 520 {cx - 30} 520 {cx - 58} 508 Z"
    if alto < 150:
        charco = f"M{cx - 66} 508 C{cx - 72} 494 {cx - 46} 490 {cx - 30} 494 L{cx + 40} 492 C{cx + 64} 490 {cx + 70} 504 {cx + 58} 514 C{cx + 20} 524 {cx - 40} 522 {cx - 66} 508 Z"
    p.vol(charco, p.lin((0, "#fff4dc"), (1, "#d8b88a")), k=3, lo=0.4, ro=0.4, gr=False)
    # cuerpo
    cuerpo = f"M{cx - rb} {top} L{cx - rb} {yb} Q{cx} {yb + 10} {cx + rb} {yb} L{cx + rb} {top} Z"
    g = p.lin((0, "#fff6e2"), (0.3, "#f6dfb8"), (0.7, "#c8a072"), (1, "#7a5a3c"), x2=1, y2=0)
    p.vol(cuerpo, g, k=5, lo=0.3, ro=0.55)
    p(f'<rect x="{cx - rb}" y="{top}" width="{2 * rb}" height="70" fill="{p.lin((0, "#ffb060", 0.5), (1, "#ffb060", 0))}" clip-path="{p.clip(cuerpo)}"/>')
    # gotas de cera por el lateral
    for xg, lg_ in ((cx - 30, 0.45), (cx - 12, 0.25), (cx + 14, 0.6), (cx + 30, 0.35), (cx - 36, 0.8)):
        L = min(alto * lg_, alto - 8)
        d = (f"M{xg - 7} {top + 2} C{xg - 7} {top + L * 0.5} {xg - 5} {top + L * 0.8} {xg - 4} {top + L} "
             f"C{xg - 4} {top + L + 9} {xg + 5} {top + L + 9} {xg + 5} {top + L} C{xg + 6} {top + L * 0.7} {xg + 7} {top + L * 0.4} {xg + 7} {top + 2} Z")
        p(f'<path d="{d}" fill="{p.lin((0, "#fffaf0"), (1, "#e8cfa4"), x2=1, y2=0)}"/>'
          f'<path d="M{xg - 3} {top + 4} L{xg - 2} {top + L}" stroke="#fff" stroke-width="2" opacity="0.7" stroke-linecap="round"/>'
          f'<path d="M{xg + 6} {top + 4} L{xg + 4} {top + L}" stroke="#a07a50" stroke-width="1.4" opacity="0.5"/>')
    # borde irregular y pozo de cera fundida
    labio = (f"M{cx - rb - 2} {top + 2} " + " ".join(f"Q{cx - rb + i * 9 + 4} {top - r.uniform(6, 14):.1f} {cx - rb + i * 9 + 9} {top - r.uniform(0, 5):.1f}" for i in range(9))
             + f" L{cx + rb + 2} {top + 4} Q{cx} {top + 16} {cx - rb - 2} {top + 2} Z")
    p.vol(labio, p.lin((0, "#fffaf0"), (1, "#e6c896")), k=3, lo=0.3, ro=0.4, gr=False)
    p(f'<ellipse cx="{cx}" cy="{top}" rx="{rb - 8}" ry="7" fill="{p.rad((0, "#ffe2a8"), (0.6, "#ffc070"), (1, "#c89060"))}"/>'
      f'<ellipse cx="{cx - 8}" cy="{top - 2}" rx="12" ry="2" fill="#fff" opacity="0.6"/>')
    # mecha
    base = top - 10
    p(f'<path d="M{cx} {top} C{cx} {top - 6} {cx + 1} {top - 10} {cx + 2 + sx * 0.1} {top - 16}" stroke="#1a1208" stroke-width="3" fill="none" stroke-linecap="round"/>'
      f'<circle cx="{cx + 2 + sx * 0.1}" cy="{top - 16}" r="2.2" fill="#ff7a1a"/>')
    _llama(p, cx, base, (cx + tip[0], base - tip[1]), an, sx=sx)
    return p.fin()


def velas():
    _vela("vela_a", 250, (0, 118), 19, 0)
    _vela("vela_b", 250, (7, 104), 21, 5)
    _vela("vela_corta", 70, (2, 92), 16, 2)
    p = P("llama_vela", 120, 220)
    _llama(p, 60, 200, (60, 50), 20)
    p.fin()


# ============================================================== 4. MARCAS DE TIZA
def _tiza(p, a, b, sem, ancho=15):
    r = random.Random(sem)
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    nx, ny = -uy, ux
    n = int(L / 6)
    for capa in range(3):
        izq, der = [], []
        for i in range(n + 1):
            t = i / n
            ta = min(1, t * 8, (1 - t) * 6) ** 0.6
            wv = ancho * (0.55 + 0.45 * ta) * (1 - 0.18 * capa) / 2
            cx_, cy_ = a[0] + ux * L * t, a[1] + uy * L * t
            o = r.uniform(-1.5, 1.5)
            izq.append((cx_ + nx * (wv + r.uniform(-1.2, 0.8) + o * 0.4), cy_ + ny * (wv + r.uniform(-1.2, 0.8))))
            der.append((cx_ - nx * (wv + r.uniform(-1.2, 0.8) - o * 0.4), cy_ - ny * (wv + r.uniform(-1.2, 0.8))))
        p(f'<path d="{poly(izq + der[::-1])}" fill="#f6f3ea" opacity="{(0.55, 0.45, 0.6)[capa]}"/>')
    for _ in range(9):  # estrías donde la tiza no tocó la roca
        o = r.uniform(-ancho * 0.4, ancho * 0.4)
        t0, t1 = r.uniform(0, 0.8), r.uniform(0.1, 0.25)
        p(f'<path d="M{F(a[0] + ux * L * t0 + nx * o)} {F(a[1] + uy * L * t0 + ny * o)} l{F(ux * L * t1)} {F(uy * L * t1)}" '
          f'stroke="#3d2a1f" stroke-width="{r.uniform(0.8, 2):.1f}" opacity="0.5"/>')
    for _ in range(26):  # polvo
        t = r.random()
        o = r.gauss(0, ancho * 0.9)
        p(f'<circle cx="{F(a[0] + ux * L * t + nx * o)}" cy="{F(a[1] + uy * L * t + ny * o)}" r="{r.uniform(0.6, 1.8):.1f}" fill="#f6f3ea" opacity="{r.uniform(0.3, 0.8):.2f}"/>')


def _filtro_tiza(p):
    return p.filtro('<feTurbulence type="fractalNoise" baseFrequency="0.07" numOctaves="2" seed="4" result="t"/>'
                    '<feDisplacementMap in="SourceGraphic" in2="t" scale="3" xChannelSelector="R" yChannelSelector="G" result="d"/>'
                    '<feTurbulence type="fractalNoise" baseFrequency="0.55" numOctaves="2" seed="8" result="n"/>'
                    '<feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  -2.6 0 0 0 2.15" result="m"/>'
                    '<feComposite in="d" in2="m" operator="in"/>')


def marcas():
    p = P("marca_raya", 70, 320)
    f = _filtro_tiza(p)
    p(f'<g filter="{f}">')
    _tiza(p, (34, 16), (37, 304), 41, 16)
    p("</g>")
    p.fin()
    p = P("marca_grupo", 330, 340)
    f = _filtro_tiza(p)
    p(f'<g filter="{f}">')
    for i, x in enumerate((62, 122, 182, 240)):
        _tiza(p, (x + (i % 2) * 4 - 2, 30 + i * 3), (x + 4 - i, 312 - (i % 2) * 5), 50 + i)
    _tiza(p, (22, 262), (310, 82), 60, 12)
    p("</g>")
    p.fin()


# ============================================================== 5. LANA
def _punto(p, x, y, w, h, col, claro, osc, sx=13, sy=10, sem=1):
    r = random.Random(sem)
    p(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{osc}"/>')
    j = 0
    yy = y
    while yy < y + h + sy:
        xx = x + (sx / 2 if j % 2 else 0) * 0
        while xx < x + w + sx:
            for sg in (-1, 1):
                cx_ = xx + sg * sx * 0.24
                c = claro if (sg < 0 and r.random() < 0.12) else col
                p(f'<ellipse cx="{F(cx_)}" cy="{F(yy)}" rx="{F(sx * 0.27)}" ry="{F(sy * 0.62)}" fill="{c}" transform="rotate({-sg * 28} {F(cx_)} {F(yy)})"/>')
            p(f'<path d="M{F(xx - sx * 0.38)} {F(yy - sy * 0.4)} l{F(sx * 0.16)} {F(sy * 0.55)}" stroke="{claro}" stroke-width="1.3" opacity="0.6"/>')
            xx += sx
        yy += sy
        j += 1


def ovillo():
    p = P("ovillo_lana", 330, 300)
    r = random.Random(51)
    cx, cy, R = 150, 145, 112
    p.sombra(cx + 20, 262, 120, 18, 0.55)
    # hebra suelta
    hebra = f"M{cx + 80} {cy + 78} C{cx + 110} {cy + 112} {cx + 150} {cy + 96} {cx + 160} {cy + 120} C{cx + 168} {cy + 140} {cx + 120} {cy + 150} {cx + 90} {cy + 142}"
    p(f'<path d="{hebra}" stroke="#7a1016" stroke-width="7" fill="none" stroke-linecap="round"/>'
      f'<path d="{hebra}" stroke="#e0453e" stroke-width="3" fill="none" stroke-linecap="round" transform="translate(-1 -1.5)"/>')
    circ = f"M{cx - R} {cy} A{R} {R} 0 1 0 {cx + R} {cy} A{R} {R} 0 1 0 {cx - R} {cy} Z"
    p(f'<path d="{circ}" fill="{p.rad((0, "#ff8070"), (0.5, "#c4282a"), (1, "#5c0d12"), cx=0.38, cy=0.32, r=0.75)}"/>')
    cl = p.clip(circ)
    p(f'<g clip-path="{cl}">')
    for k in range(34):
        ang, ry = r.uniform(0, 180), R * r.uniform(0.12, 1)
        ox, oy = r.uniform(-8, 8), r.uniform(-8, 8)
        for j in range(r.choice((2, 3, 4))):
            p(f'<ellipse cx="{F(cx + ox)}" cy="{F(cy + oy)}" rx="{R}" ry="{F(ry + j * 4)}" fill="none" stroke="{r.choice(("#e0453e", "#9e1c22", "#ff8a7a", "#7a1016", "#c4282a"))}" '
              f'stroke-width="{r.uniform(2.5, 4.5):.1f}" opacity="0.85" transform="rotate({ang:.0f} {F(cx + ox)} {F(cy + oy)})"/>')
    for j in range(9):  # vuelta de encima, tensa
        p(f'<ellipse cx="{cx}" cy="{cy}" rx="{R}" ry="{F(R * 0.42 + j * 4.5)}" fill="none" stroke="{("#ff8a7a", "#d8383a", "#a51c22")[j % 3]}" stroke-width="4" '
          f'transform="rotate(-38 {cx} {cy})"/>')
    p(f'<rect width="330" height="300" fill="#888" filter="url(#grano)"/></g>')
    esfera(p, cx, cy, R, 0.65)
    p(f'<path d="{circ}" fill="none" stroke="{RIM}" stroke-width="5" opacity="0.4" clip-path="{p.clip(f"M{cx} {cy - 20} L330 {cy - 20} L330 300 L{cx} 300 Z")}"/>')
    p(f'<ellipse cx="{cx - 45}" cy="{cy - 55}" rx="34" ry="20" fill="{LUZ}" opacity="0.22" filter="url(#blur8)"/>')
    p.fin()


def agujas():
    p = P("agujas_tejer", 480, 250)
    def aguja(ang, x, y, L=400):
        p(f'<g transform="translate({x} {y}) rotate({ang})">')
        p(f'<rect x="0" y="-5" width="{L}" height="10" rx="4" fill="{p.lin((0, "#f2dcb0"), (0.4, "#c9a066"), (1, "#6a4a24"))}"/>'
          f'<path d="M{L} -5 L{L + 30} -0.5 Q{L + 33} 0 {L + 30} 0.5 L{L} 5 Z" fill="{p.lin((0, "#f2dcb0"), (1, "#7a5a30"))}"/>'
          f'<path d="M4 -3 L{L} -3" stroke="#fff6e0" stroke-width="1.6" opacity="0.7"/>'
          f'<path d="M4 4 L{L} 4" stroke="{RIM}" stroke-width="1.2" opacity="0.6"/>'
          f'<circle cx="-6" cy="0" r="12" fill="{p.rad((0, "#e06a4a"), (0.6, "#9a2a1a"), (1, "#4a0e08"), cx=0.35, cy=0.3)}"/>'
          f'<circle cx="-10" cy="-4" r="3.5" fill="#fff" opacity="0.55"/>')
        for k in range(10):
            p(f'<path d="M{30 + k * 37} -5 l3 10" stroke="#8a6438" stroke-width="0.8" opacity="0.4"/>')
        p("</g>")
    if SOMBRA:
        p('<g opacity="0.45" filter="url(#blur8)" transform="translate(6 14)"><path d="M40 190 L440 80 M50 70 L440 200" stroke="#000" stroke-width="12"/></g>')
    aguja(16, 42, 64)
    # labor colgando de la primera aguja
    sw = poly([(150, 118), (300, 155), (292, 222), (152, 200)])
    p.sombra_d(sw, 0.4, 4, 8)
    cl = p.clip(sw)
    p(f'<g clip-path="{cl}"><g transform="rotate(14 220 170)">')
    _punto(p, 120, 100, 210, 140, "#c4282a", "#ff8070", "#5c0d12", sem=5)
    p('</g>')
    esfera(p, 210, 150, 120, 0.4)
    p(f'<rect width="480" height="250" fill="#888" filter="url(#grano)"/></g>')
    p(f'<path d="M152 200 L292 222" stroke="#ff8070" stroke-width="2" opacity="0.5"/>')
    aguja(-15, 38, 188)
    for k in range(8):  # puntos montados en la aguja
        x = 158 + k * 18
        y = 64 + (x - 42) * math.tan(math.radians(16)) + 6
        p(f'<ellipse cx="{F(x)}" cy="{F(y)}" rx="7" ry="9" fill="none" stroke="#c4282a" stroke-width="4" transform="rotate(16 {F(x)} {F(y)})"/>'
          f'<path d="M{F(x - 5)} {F(y - 5)} q4 -4 8 0" stroke="#ff8a7a" stroke-width="1.5" fill="none"/>')
    p.fin()


def gorro(n, col, claro, osc, sem):
    p = P(n, 340, 350)
    p.sombra(170, 322, 140, 14, 0.5)
    domo = "M52 252 C46 130 104 78 170 76 C236 78 294 130 288 252 Z"
    cl = p.clip(domo)
    p(f'<g clip-path="{cl}">')
    _punto(p, 40, 60, 260, 200, col, claro, osc, sx=14, sy=11, sem=sem)
    p(f'<rect width="340" height="350" fill="#888" filter="url(#grano)"/></g>')
    esfera(p, 170, 175, 150, 0.7, cl)
    p(f'<path d="{domo}" fill="{LUZ}" opacity="0.15" clip-path="{p.clip("M0 0 L170 0 L120 300 L0 300 Z")}"/>')
    p(f'<path d="M290 252 C294 140 240 84 176 78" stroke="{RIM}" stroke-width="4" fill="none" opacity="0.45"/>')
    # vuelta acanalada
    vu = "M36 236 Q170 214 304 236 L302 302 Q170 324 38 302 Z"
    p(f'<path d="{vu}" fill="{osc}"/>')
    for i in range(34):
        t = i / 33
        x0, x1 = 36 + 268 * t, 38 + 264 * t
        y0 = 236 - 22 * 4 * t * (1 - t) * 1.0 + 0
        y1 = 302 + 22 * 4 * t * (1 - t)
        c = claro if i % 2 == 0 else col
        p(f'<path d="M{F(x0)} {F(y0 + 2)} L{F(x1)} {F(y1 - 2)}" stroke="{c}" stroke-width="5.5" stroke-linecap="round" opacity="0.95"/>')
    cl2 = p.clip(vu)
    p(f'<g clip-path="{cl2}"><rect width="340" height="350" fill="#888" filter="url(#grano)"/>'
      f'<rect x="30" y="210" width="280" height="120" fill="{p.lin((0, "#fff", 0.12), (0.5, "#000", 0), (1, "#000", 0.45))}"/>'
      f'<rect x="30" y="210" width="280" height="120" fill="{p.lin((0, "#000", 0), (0.7, "#000", 0), (1, "#000", 0.4), x2=1, y2=0)}"/></g>')
    p(f'<path d="M36 236 Q170 214 304 236" stroke="#000" stroke-width="3" opacity="0.35" fill="none"/>')
    # pompón
    r = random.Random(sem + 9)
    p(f'<circle cx="170" cy="62" r="40" fill="{p.rad((0, claro), (0.6, col), (1, osc), cx=0.38, cy=0.32)}"/>')
    for _ in range(170):
        a = r.uniform(0, 2 * math.pi); rr = r.uniform(10, 44)
        x, y = 170 + math.cos(a) * rr, 62 + math.sin(a) * rr
        L = r.uniform(6, 13)
        sh = 0.5 + 0.5 * math.cos(a + 2.3)
        c = claro if sh > 0.7 and r.random() < 0.7 else (osc if sh < 0.3 else col)
        p(f'<path d="M{F(x)} {F(y)} l{F(math.cos(a) * L)} {F(math.sin(a) * L)}" stroke="{c}" stroke-width="2.4" stroke-linecap="round" opacity="0.9"/>')
    p.fin()


def lana():
    ovillo(); agujas()
    gorro("gorro_lana_a", "#7a1e2c", "#b84a5c", "#3d0b14", 61)
    gorro("gorro_lana_b", "#c9962a", "#f0c860", "#6e4c0e", 62)
    gorro("gorro_lana_c", "#2a5c9a", "#5f94d4", "#13305a", 63)


# ============================================================== 6. AGUA
def garrafa():
    p = P("garrafa_agua", 380, 560)
    p.sombra(190, 536, 150, 14, 0.5)
    p(f'<ellipse cx="200" cy="534" rx="120" ry="10" fill="#9fd4ff" opacity="0.25" filter="url(#blur8)"/>')
    cuerpo = ("M58 196 Q58 150 100 140 L150 128 L150 96 L214 96 L214 128 L282 140 Q326 150 326 196 "
              "L326 500 Q326 528 296 528 L88 528 Q58 528 58 500 Z")
    asa = "M236 136 C238 82 312 74 318 150 L300 150 C296 104 258 102 256 138 Z"
    p(f'<path d="{asa}" fill="#dcefff" opacity="0.45" stroke="#bcdcf2" stroke-width="2"/>'
      f'<path d="M244 130 C248 92 304 86 310 146" stroke="#fff" stroke-width="2.5" fill="none" opacity="0.6"/>')
    cl = p.clip(cuerpo)
    p(f'<path d="{cuerpo}" fill="#e6f4ff" opacity="0.28"/>')
    p(f'<g clip-path="{cl}">'
      f'<rect x="50" y="206" width="290" height="330" fill="{p.lin((0, "#8fd0f4", 0.55), (0.6, "#4a9ad0", 0.6), (1, "#22609a", 0.75))}"/>'
      f'<rect x="50" y="206" width="290" height="330" fill="{p.lin((0, "#fff", 0.0), (0.75, "#000", 0.0), (1, "#0d1b2e", 0.35), x2=1, y2=0)}"/>'
      f'<ellipse cx="192" cy="208" rx="140" ry="9" fill="#d8f2ff" opacity="0.7"/>'
      f'<ellipse cx="192" cy="208" rx="140" ry="9" fill="none" stroke="#fff" stroke-width="2" opacity="0.8"/>'
      f'<ellipse cx="160" cy="470" rx="80" ry="22" fill="{LUZ}" opacity="0.28" filter="url(#blur8)"/>')
    for y in (300, 410):
        p(f'<path d="M50 {y} Q192 {y + 10} 340 {y}" stroke="#a9d6f5" stroke-width="5" fill="none" opacity="0.6"/>'
          f'<path d="M50 {y + 5} Q192 {y + 15} 340 {y + 5}" stroke="#fff" stroke-width="2" fill="none" opacity="0.7"/>')
    p('</g>')
    p(f'<path d="{cuerpo}" fill="none" stroke="#cfe8f8" stroke-width="3" opacity="0.8"/>'
      '<path d="M84 180 Q78 300 82 500" stroke="#fff" stroke-width="10" stroke-linecap="round" fill="none" opacity="0.65"/>'
      '<path d="M104 190 Q100 260 102 330" stroke="#fff" stroke-width="4" stroke-linecap="round" fill="none" opacity="0.5"/>'
      f'<path d="M316 200 Q320 350 314 500" stroke="{RIM}" stroke-width="6" stroke-linecap="round" fill="none" opacity="0.6"/>'
      f'<path d="M80 168 Q150 140 182 134" stroke="{LUZ}" stroke-width="4" fill="none" opacity="0.6"/>')
    # tapón
    tap = "M146 98 L146 60 Q146 52 154 52 L210 52 Q218 52 218 60 L218 98 Z"
    p.vol(tap, p.lin((0, "#6aa8ff"), (0.4, "#2a6fd0"), (1, "#123a7a"), x2=1, y2=0), k=4)
    for x in range(152, 216, 7):
        p(f'<path d="M{x} 56 L{x} 94" stroke="#0d2a5a" stroke-width="2" opacity="0.5"/>')
    p('<rect x="140" y="92" width="84" height="10" rx="3" fill="#1d4f9a"/>')
    p.fin()


def botella():
    p = P("botella_agua", 150, 450)
    p.sombra(75, 432, 56, 8, 0.5)
    cuerpo = "M44 120 Q44 92 60 80 L60 58 L90 58 L90 80 Q106 92 106 120 L108 250 Q102 264 108 278 L108 410 Q108 424 94 424 L56 424 Q42 424 42 410 L42 278 Q48 264 42 250 Z"
    cl = p.clip(cuerpo)
    p(f'<path d="{cuerpo}" fill="#e6f4ff" opacity="0.3"/>'
      f'<g clip-path="{cl}"><rect x="30" y="110" width="90" height="320" fill="{p.lin((0, "#9fd8f8", 0.5), (1, "#2a6aa8", 0.7))}"/>'
      f'<ellipse cx="75" cy="112" rx="34" ry="4" fill="#e8f8ff" opacity="0.8"/>'
      f'<rect x="30" y="180" width="90" height="60" fill="{p.lin((0, "#cfe8f6"), (0.5, "#8ec4e8"), (1, "#3d7aa8"), x2=1, y2=0)}" opacity="0.9"/>'
      f'<rect x="30" y="184" width="90" height="3" fill="#fff" opacity="0.6"/>')
    for y in range(290, 410, 22):
        p(f'<path d="M40 {y} Q75 {y + 6} 110 {y}" stroke="#fff" stroke-width="2" fill="none" opacity="0.5"/>')
    p('</g>')
    p(f'<path d="{cuerpo}" fill="none" stroke="#d6ecfa" stroke-width="2" opacity="0.8"/>'
      '<path d="M54 110 L52 416" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity="0.6"/>'
      f'<path d="M101 116 L102 414" stroke="{RIM}" stroke-width="4" stroke-linecap="round" opacity="0.6"/>')
    tap = "M56 60 L56 30 Q56 24 62 24 L88 24 Q94 24 94 30 L94 60 Z"
    p.vol(tap, p.lin((0, "#6aa8ff"), (1, "#123a7a"), x2=1, y2=0), k=3)
    for x in range(60, 92, 5):
        p(f'<path d="M{x} 28 L{x} 56" stroke="#0d2a5a" stroke-width="1.5" opacity="0.5"/>')
    p.fin()


# ============================================================== 7. COMIDA Y BASURA
def _lata(p, x, y, w, h, banda, sem):
    rx, ry = w / 2, w * 0.18
    cx = x + rx
    d = f"M{x} {y} L{x} {y + h} A{rx} {ry} 0 0 0 {x + w} {y + h} L{x + w} {y} Z"
    p(f'<path d="{d}" fill="{p.lin((0, "#f2f4f6"), (0.3, "#aab2ba"), (0.65, "#6a727a"), (1, "#2a3036"), x2=1, y2=0)}"/>')
    p(f'<rect x="{x}" y="{y + h * 0.18}" width="{w}" height="{h * 0.6}" fill="{p.lin((0, banda[0]), (0.35, banda[1]), (1, banda[2]), x2=1, y2=0)}"/>'
      f'<rect x="{x}" y="{y + h * 0.38}" width="{w}" height="{h * 0.08}" fill="#f2e6c8" opacity="0.8"/>'
      f'<rect x="{x + w * 0.18}" y="{y + 4}" width="{w * 0.1}" height="{h}" fill="#fff" opacity="0.35"/>'
      f'<rect x="{x + w * 0.86}" y="{y + 4}" width="{w * 0.06}" height="{h}" fill="{RIM}" opacity="0.5"/>')
    p(f'<ellipse cx="{cx}" cy="{y}" rx="{rx}" ry="{ry}" fill="{p.lin((0, "#ffffff"), (1, "#7a828a"), x2=1, y2=1)}"/>'
      f'<ellipse cx="{cx}" cy="{y}" rx="{rx - 4}" ry="{ry - 2}" fill="none" stroke="#5a626a" stroke-width="1.5"/>'
      f'<ellipse cx="{cx + 4}" cy="{y + 1}" rx="{rx * 0.35}" ry="{ry * 0.35}" fill="none" stroke="#4a5258" stroke-width="2"/>')


def caja_comida():
    p = P("caja_comida", 620, 450)
    r = random.Random(71)
    p.sombra(300, 418, 250, 18, 0.55)
    # tapa apoyada detrás
    tapa = "M118 176 L128 40 Q130 30 140 30 L540 30 Q550 30 552 40 L560 176 Z"
    p.vol(tapa, p.lin((0, "#7fb0d8"), (0.5, "#3c7ab0"), (1, "#1d4570"), x2=1, y2=1), k=5, lo=0.35)
    p('<path d="M136 48 L544 48 L548 164 L130 164 Z" fill="none" stroke="#1a3a5e" stroke-width="3" opacity="0.5"/>'
      f'<path d="M134 46 L546 46" stroke="#cfe6ff" stroke-width="2" opacity="0.7"/>')
    for x in range(160, 540, 40):
        p(f'<path d="M{x} 60 L{x + 2} 152" stroke="#9cc6ea" stroke-width="2" opacity="0.25"/>')
    # interior de la caja (pared trasera)
    p('<path d="M120 168 L540 168 L512 214 L72 214 Z" fill="#2a3a44"/>')
    p(f'<path d="M120 168 L540 168 L540 186 L120 186 Z" fill="{p.lin((0, "#000", 0.4), (1, "#000", 0))}"/>')
    # comida
    _lata(p, 150, 128, 64, 220, ("#e0503a", "#b8281a", "#5a0e08"), 1)
    _lata(p, 226, 150, 56, 200, ("#5fae5a", "#2f7a34", "#123a18"), 2)
    pan = "M292 172 C280 150 300 124 330 118 L440 98 C470 92 492 108 488 130 C484 150 466 160 440 166 L330 186 C310 190 298 184 292 172 Z"
    p.vol(pan, p.lin((0, "#f4c27a"), (0.5, "#c8833a"), (1, "#7a4214"), x2=0.3, y2=1), k=6, lo=0.4)
    for k in range(5):
        x = 330 + k * 30
        y = 128 - k * 5.5
        p(f'<path d="M{x} {y + 14} q10 -16 24 -18" stroke="#6a3410" stroke-width="5" fill="none" stroke-linecap="round"/>'
          f'<path d="M{x + 2} {y + 16} q10 -16 24 -18" stroke="#fff0c8" stroke-width="2" fill="none" opacity="0.7" stroke-linecap="round"/>')
    for _ in range(40):
        x, y = r.uniform(300, 480), r.uniform(110, 170)
        p(f'<circle cx="{F(x)}" cy="{F(y)}" r="0.9" fill="#fff2d0" opacity="0.6"/>')
    # naranja y manzana
    p(f'<circle cx="378" cy="196" r="32" fill="{p.rad((0, "#ffd080"), (0.5, "#f08a1a"), (1, "#8a3a06"), cx=0.36, cy=0.32)}"/>')
    for _ in range(60):
        a, rr = r.uniform(0, 6.28), r.uniform(0, 28)
        p(f'<circle cx="{F(378 + math.cos(a) * rr)}" cy="{F(196 + math.sin(a) * rr)}" r="1.1" fill="#8a3a06" opacity="0.35"/>')
    p(f'<circle cx="366" cy="182" r="7" fill="#fff" opacity="0.4" filter="url(#blur8)"/>')
    p(f'<path d="M462 160 C444 140 470 128 482 140 C494 128 520 140 502 160 C520 190 500 226 482 222 C464 226 444 190 462 160 Z" '
      f'fill="{p.rad((0, "#ff8a6a"), (0.5, "#c8202a"), (1, "#5a0810"), cx=0.36, cy=0.3)}"/>'
      '<path d="M482 142 C480 130 484 122 488 116" stroke="#4a2a10" stroke-width="3" fill="none"/>'
      '<path d="M488 124 C500 112 516 116 520 120 C510 130 496 130 488 124 Z" fill="#4f8a2a"/>'
      '<ellipse cx="468" cy="166" rx="6" ry="10" fill="#fff" opacity="0.45"/>')
    # paredes de plástico translúcido
    frente = "M72 214 L512 214 L500 404 Q500 412 492 412 L90 412 Q82 412 82 404 Z"
    lado = "M512 214 L540 168 L532 352 Q530 362 524 368 L500 404 Z"
    p(f'<path d="{lado}" fill="#b8cfdc" opacity="0.65"/>')
    p(f'<path d="{frente}" fill="{p.lin((0, "#e8f2f8"), (1, "#a8c2d2"))}" opacity="0.6"/>')
    p.grano(frente, lado)
    p(f'<path d="M86 240 L94 400" stroke="#fff" stroke-width="7" opacity="0.5" stroke-linecap="round"/>'
      f'<path d="M500 222 L490 400" stroke="{RIM}" stroke-width="4" opacity="0.6"/>'
      f'<path d="M96 380 L484 380" stroke="#fff" stroke-width="2" opacity="0.3"/>')
    p('<path d="M66 208 L514 208 L544 162 L538 160 L510 204 L70 204 Z" fill="#f2f8fc"/>'
      '<path d="M66 208 L514 208 L514 220 L68 220 Z" fill="#dbe8f0"/>'
      f'<path d="M68 220 L514 220" stroke="#7a95a8" stroke-width="2" opacity="0.7"/>'
      '<path d="M120 166 L540 166" stroke="#e8f2f8" stroke-width="3"/>')
    p.fin()


def bolsa_basura():
    p = P("bolsa_basura", 340, 430)
    r = random.Random(81)
    p.sombra(170, 404, 140, 14, 0.6)
    bolsa = ("M150 132 C120 140 70 170 52 230 C34 290 40 360 70 392 C110 412 236 414 276 392 C306 364 310 292 290 232 "
             "C272 176 224 140 190 132 Z")
    p.vol(bolsa, p.rad((0, "#4a4e58"), (0.5, "#1c1e24"), (1, "#07080b"), cx=0.35, cy=0.3, r=0.75), k=7, lo=0.18, ro=0.55)
    for k in range(9):  # pliegues que bajan del nudo
        x1 = 70 + k * 26 + r.uniform(-8, 8); y1 = r.uniform(250, 380)
        xm = 170 + (x1 - 170) * 0.45 + r.uniform(-10, 10)
        d = f"M{170 + (x1 - 170) * 0.12:.1f} 150 Q{xm:.1f} {(150 + y1) / 2:.1f} {x1:.1f} {y1:.1f}"
        p(f'<path d="{d}" stroke="#000" stroke-width="{r.uniform(4, 8):.1f}" fill="none" opacity="0.5" stroke-linecap="round"/>'
          f'<path d="{d}" transform="translate(-5 0)" stroke="#9aa0b0" stroke-width="{r.uniform(1.5, 3):.1f}" fill="none" opacity="{0.45 if x1 < 200 else 0.2}" stroke-linecap="round"/>')
    for _ in range(4):  # arrugas horizontales abajo
        y = r.uniform(330, 390); x = r.uniform(80, 200)
        p(f'<path d="M{x:.1f} {y:.1f} q30 {r.uniform(-8, 8):.1f} {r.uniform(50, 90):.1f} {r.uniform(-4, 6):.1f}" stroke="#000" stroke-width="4" fill="none" opacity="0.4" stroke-linecap="round"/>')
    p('<path d="M92 210 C76 250 72 300 84 350" stroke="#fff" stroke-width="5" fill="none" opacity="0.35" stroke-linecap="round"/>'
      '<path d="M120 170 C104 186 96 200 92 214" stroke="#ffe6c0" stroke-width="3" fill="none" opacity="0.5" stroke-linecap="round"/>'
      f'<path d="M286 250 C298 300 292 350 270 388" stroke="{RIM}" stroke-width="4" fill="none" opacity="0.5" stroke-linecap="round"/>')
    # cuello y nudo con orejas
    p.vol("M150 136 C156 118 158 104 156 92 L186 92 C184 104 186 118 192 136 Z", p.lin((0, "#3a3d46"), (1, "#0b0c10"), x2=1, y2=0), k=3, lo=0.2)
    p.vol("M156 96 C130 70 108 40 120 28 C134 18 150 50 166 88 Z", p.lin((0, "#4a4e58"), (1, "#0d0e12"), x2=1, y2=1), k=4, lo=0.3)
    p.vol("M178 92 C196 54 224 30 238 40 C248 52 216 78 186 98 Z", p.lin((0, "#40444e"), (1, "#0b0c10"), x2=1, y2=1), k=4, lo=0.25)
    p.vol("M150 90 C150 78 190 78 192 90 C192 104 150 104 150 90 Z", p.rad((0, "#4a4e58"), (1, "#0b0c10")), k=3, lo=0.3)
    p('<path d="M124 34 C134 52 146 70 160 86" stroke="#9aa0ae" stroke-width="2" fill="none" opacity="0.5"/>'
      '<path d="M230 44 C214 60 200 74 186 88" stroke="#9aa0ae" stroke-width="2" fill="none" opacity="0.4"/>')
    p.fin()


# ============================================================== 8. CÁMARA
def camara():
    p = P("camara_tripode", 330, 650)
    p.sombra(165, 626, 140, 12, 0.5)
    # patas del trípode
    for (x0, x1, c) in ((158, 40, "#2a2e34"), (172, 292, "#2a2e34"), (165, 175, "#1a1d22")):
        p(f'<path d="M{x0} 300 L{x1} 618" stroke="{c}" stroke-width="13" stroke-linecap="round"/>'
          f'<path d="M{x0 - 2} 302 L{x1 - 3} 612" stroke="#7a828c" stroke-width="2.5" opacity="0.6"/>'
          f'<path d="M{(x0 * 0.45 + x1 * 0.55):.0f} {300 + 318 * 0.55:.0f} L{x1} 618" stroke="#4a5058" stroke-width="9" stroke-linecap="round"/>'
          f'<rect x="{(x0 * 0.5 + x1 * 0.5) - 9:.0f}" y="{300 + 318 * 0.5 - 6:.0f}" width="18" height="12" rx="3" fill="#0d0f12"/>'
          f'<ellipse cx="{x1}" cy="620" rx="11" ry="5" fill="#0d0f12"/>')
    p('<path d="M110 430 L165 400 L220 430" stroke="#3a3f46" stroke-width="5" fill="none"/>')
    # columna y rótula
    p.vol("M156 238 L174 238 L174 410 L156 410 Z", p.lin((0, "#9aa2ac"), (0.4, "#4a5058"), (1, "#16181c"), x2=1, y2=0), k=3, gr=False)
    p.vol("M126 290 Q165 270 204 290 L198 312 Q165 324 132 312 Z", p.lin((0, "#5a616a"), (1, "#121418")), k=3)
    p.vol("M140 228 L190 228 L196 248 L134 248 Z", p.lin((0, "#6a727c"), (1, "#16181c")), k=3)
    p('<path d="M196 238 L246 262" stroke="#20242a" stroke-width="8" stroke-linecap="round"/><circle cx="248" cy="263" r="7" fill="#3a3f46"/>')
    # cuerpo de la cámara (objetivo a la izquierda)
    cu = "M92 132 Q92 118 106 118 L238 118 Q254 118 254 134 L254 214 Q254 228 240 228 L106 228 Q92 228 92 214 Z"
    p.vol(cu, p.lin((0, "#5a616c"), (0.35, "#2e333a"), (1, "#0f1114"), x2=0.6, y2=1), k=6, lo=0.3, ro=0.5)
    p('<path d="M110 196 L238 196" stroke="#000" stroke-width="2" opacity="0.5"/><path d="M110 198 L238 198" stroke="#8a929c" stroke-width="1" opacity="0.4"/>')
    for x in range(184, 240, 8):
        p(f'<rect x="{x}" y="204" width="4" height="16" rx="2" fill="#0a0b0d" opacity="0.8"/>')
    # visor trasero y pantalla plegada
    p.vol("M232 104 L268 104 Q276 104 276 112 L276 132 L232 132 Z", p.lin((0, "#3a4048"), (1, "#0d0f12")), k=3, gr=False)
    p.vol("M150 112 L224 112 L224 124 L150 124 Z", p.lin((0, "#4a515a"), (1, "#16181c")), k=2, gr=False)
    # objetivo
    p.vol("M34 140 L96 132 L96 214 L34 206 Z", p.lin((0, "#4a515a"), (0.5, "#1a1d22"), (1, "#08090b")), k=4, lo=0.3)
    for x in (46, 58, 70, 82):
        p(f'<path d="M{x} {140 - (x - 34) * 0.13:.1f} L{x} {206 + (x - 34) * 0.13:.1f}" stroke="#000" stroke-width="2.5" opacity="0.5"/>')
    p(f'<ellipse cx="34" cy="173" rx="14" ry="34" fill="#0a0b0e"/>'
      f'<ellipse cx="32" cy="173" rx="10" ry="27" fill="{p.rad((0, "#5a4aa8"), (0.45, "#1d2a5a"), (1, "#05060a"), cx=0.6, cy=0.4)}"/>'
      f'<ellipse cx="30" cy="160" rx="3" ry="8" fill="{LUZ}" opacity="0.8"/><ellipse cx="34" cy="188" rx="2" ry="5" fill="#9fd0ff" opacity="0.6"/>')
    # piloto rojo
    p(f'<circle cx="114" cy="130" r="14" fill="{p.rad((0, "#ff3a2a", 0.7), (1, "#ff3a2a", 0))}"/>'
      '<circle cx="114" cy="130" r="4.5" fill="#ff2a1a"/><circle cx="113" cy="128.5" r="1.6" fill="#fff"/>')
    p.fin()
    p = P("piloto_rojo", 60, 60)
    p(f'<circle cx="30" cy="30" r="29" fill="{p.rad((0, "#ff4a3a", 0.85), (0.3, "#ff2a1a", 0.45), (1, "#ff2a1a", 0))}"/>'
      '<circle cx="30" cy="30" r="7" fill="#ff2a1a"/><circle cx="30" cy="30" r="4" fill="#ffb0a0"/><circle cx="28" cy="28" r="1.8" fill="#fff"/>')
    p.fin()


# ============================================================== 9. LUCES
def _farol(p, cx, top, s=1.0, halo=True):
    """Farol de camping encendido; top = arriba del asa. Devuelve y de la base."""
    def X(v): return F(cx + v * s)
    def Y(v): return F(top + v * s)
    if halo:
        p(f'<circle cx="{X(0)}" cy="{Y(170)}" r="{F(175 * s)}" fill="{p.rad((0, "#fff4dc", 0.8), (0.25, LUZ, 0.45), (0.6, LUZ2, 0.14), (1, LUZ2, 0))}"/>')
    p(f'<path d="M{X(-52)} {Y(80)} C{X(-56)} {Y(-4)} {X(56)} {Y(-4)} {X(52)} {Y(80)}" stroke="#1d2026" stroke-width="{F(9 * s)}" fill="none" stroke-linecap="round"/>'
      f'<path d="M{X(-50)} {Y(74)} C{X(-52)} {Y(6)} {X(30)} {Y(-2)} {X(46)} {Y(40)}" stroke="#ffe0a8" stroke-width="{F(2.5 * s)}" fill="none" opacity="0.6"/>')
    tapa = f"M{X(-70)} {Y(110)} L{X(-58)} {Y(78)} L{X(58)} {Y(78)} L{X(70)} {Y(110)} Z"
    p.vol(tapa, p.lin((0, "#5a616a"), (0.5, "#2a2e34"), (1, "#0d0f12"), x2=1, y2=0), k=3 * s, lo=0.25, gr=False)
    dif = f"M{X(-60)} {Y(110)} L{X(60)} {Y(110)} L{X(60)} {Y(250)} L{X(-60)} {Y(250)} Z"
    p(f'<path d="{dif}" fill="{p.lin((0, "#ffd9a0"), (0.3, "#fffaf0"), (0.6, "#fff6e4"), (1, "#f0b870"), x2=1, y2=0)}"/>')
    for k in range(4):
        y = 128 + k * 34
        p(f'<ellipse cx="{X(-14)}" cy="{Y(y)}" rx="{F(5 * s)}" ry="{F(3 * s)}" fill="#ffffff"/><ellipse cx="{X(14)}" cy="{Y(y + 16)}" rx="{F(5 * s)}" ry="{F(3 * s)}" fill="#ffffff"/>')
    for v in (-40, 0, 40):
        p(f'<path d="M{X(v)} {Y(110)} L{X(v)} {Y(250)}" stroke="#2a2e34" stroke-width="{F(3 * s)}" opacity="0.55"/>')
    p(f'<path d="M{X(-60)} {Y(112)} L{X(60)} {Y(112)}" stroke="#fff" stroke-width="{F(2 * s)}" opacity="0.8"/>')
    base = f"M{X(-66)} {Y(250)} L{X(66)} {Y(250)} L{X(74)} {Y(318)} Q{X(0)} {Y(328)} {X(-74)} {Y(318)} Z"
    p.vol(base, p.lin((0, "#4a515a"), (0.5, "#20242a"), (1, "#0a0b0d"), x2=1, y2=0), k=4 * s, lo=0.2, gr=False)
    p(f'<path d="M{X(-66)} {Y(252)} L{X(66)} {Y(252)}" stroke="{LUZ}" stroke-width="{F(4 * s)}" opacity="0.8"/>')
    for v in range(-56, 60, 14):
        p(f'<path d="M{X(v)} {Y(264)} L{X(v * 1.08)} {Y(312)}" stroke="#000" stroke-width="{F(3 * s)}" opacity="0.4"/>')
    p(f'<circle cx="{X(0)}" cy="{Y(290)}" r="{F(8 * s)}" fill="#3a3f46" stroke="#7a828c" stroke-width="{F(1.5 * s)}"/>')
    return top + 324 * s


def lampara():
    p = P("lampara_led", 380, 500)
    p.sombra(190, 466, 110, 12, 0.55)
    p(f'<ellipse cx="190" cy="470" rx="170" ry="22" fill="{LUZ}" opacity="0.25" filter="url(#blur8)"/>')
    _farol(p, 190, 140)
    p.fin()


def haz():
    p = P("haz_frontal", 900, 420)
    r = random.Random(91)
    p(f'<g filter="url(#blur8)"><path d="M14 196 L900 18 L900 402 L14 224 Z" fill="{p.lin((0, "#fff3d6", 0.85), (0.12, LUZ, 0.5), (0.55, LUZ2, 0.16), (1, LUZ2, 0), x2=1, y2=0)}"/>'
      f'<path d="M14 203 L900 110 L900 310 L14 217 Z" fill="{p.lin((0, "#fffaf0", 0.9), (0.3, "#fff0c8", 0.35), (1, "#fff0c8", 0), x2=1, y2=0)}"/></g>')
    for _ in range(70):
        x = r.uniform(40, 820); sp = 14 + (x - 14) * 0.2
        y = 210 + r.uniform(-sp, sp)
        p(f'<circle cx="{F(x)}" cy="{F(y)}" r="{r.uniform(0.8, 2.2):.1f}" fill="#fff4dc" opacity="{max(0.05, 0.7 - x / 1100):.2f}"/>')
    p(f'<circle cx="14" cy="210" r="40" fill="{p.rad((0, "#ffffff", 1), (0.3, "#fff0c8", 0.7), (1, LUZ, 0))}"/>')
    p.fin()


# ============================================================== 10. COLCHÓN
def colchon():
    p = P("colchon", 920, 330)
    A, B, C, D = (40, 168), (790, 128), (872, 200), (118, 246)
    def M(u, v, z=0):
        q = lerp(lerp(A, B, u), lerp(D, C, u), v)
        return (q[0], q[1] - z)
    t = 22
    p.sombra_d(poly([dn(A, t), dn(B, t), dn(C, t), dn(D, t)]), 0.55, 8, 6)
    p.vol(poly([A, D, dn(D, t), dn(A, t)]), "#1d3a48", k=3, lo=0.2, ro=0)
    p.vol(poly([D, C, dn(C, t), dn(D, t)]), p.lin((0, "#3d7a92"), (1, "#16303c")), k=3, lo=0.3, ro=0.5)
    p.vol(poly([A, B, C, D]), p.lin((0, "#6fb0c8"), (0.5, "#3d7a92"), (1, "#1d4656"), x2=1, y2=1), k=4, lo=0.3)
    for k in range(1, 9):
        a, b = M(0, k / 9), M(1, k / 9)
        p(f'<path d="M{F(a[0])} {F(a[1])} L{F(b[0])} {F(b[1])}" stroke="#123040" stroke-width="2.5" opacity="0.6"/>'
          f'<path d="M{F(a[0])} {F(a[1] - 2.5)} L{F(b[0])} {F(b[1] - 2.5)}" stroke="#9fd4e8" stroke-width="1.2" opacity="0.4"/>')
    # almohada
    al = [M(0.03, 0.22, 4), M(0.09, 0.16, 26), M(0.17, 0.2, 6), M(0.19, 0.5, 30), M(0.18, 0.84, 4), M(0.1, 0.84, 22), M(0.02, 0.8, 4), M(0.0, 0.5, 26)]
    d = (f"M{F(al[0][0])} {F(al[0][1])} Q{F(al[1][0])} {F(al[1][1])} {F(al[2][0])} {F(al[2][1])} Q{F(al[3][0])} {F(al[3][1])} {F(al[4][0])} {F(al[4][1])} "
         f"Q{F(al[5][0])} {F(al[5][1])} {F(al[6][0])} {F(al[6][1])} Q{F(al[7][0])} {F(al[7][1])} {F(al[0][0])} {F(al[0][1])} Z")
    p.sombra_d(d, 0.4, 6, 6)
    p.vol(d, p.lin((0, "#f4ecdc"), (0.5, "#cfc4ae"), (1, "#7a7060"), x2=1, y2=1), k=7, lo=0.4)
    q1, q2 = M(0.06, 0.35, 20), M(0.14, 0.66, 18)
    p(f'<path d="M{F(q1[0])} {F(q1[1])} Q{F((q1[0] + q2[0]) / 2 + 12)} {F((q1[1] + q2[1]) / 2)} {F(q2[0])} {F(q2[1])}" stroke="#8a806c" stroke-width="3" fill="none" opacity="0.6"/>')
    # saco de dormir (vacío)
    us = [0.2 + 0.78 * i / 20 for i in range(21)]
    vb = lambda u: 0.14 + 0.12 * max(0, (u - 0.6) / 0.4)
    vf = lambda u: 0.88 - 0.14 * max(0, (u - 0.6) / 0.4)
    arriba = [M(u, vb(u) + 0.12, 34 - 10 * max(0, (u - 0.7) / 0.3)) for u in us]
    abajo = [M(u, vf(u), 4) for u in us[::-1]]
    sac = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in arriba) + f" Q{F(M(1.0, 0.5, 14)[0])} {F(M(1.0, 0.5, 14)[1])} " + \
          " L".join(f"{x:.1f} {y:.1f}" for x, y in abajo) + f" Q{F(M(0.17, 0.5, 30)[0])} {F(M(0.17, 0.5, 30)[1])} {F(arriba[0][0])} {F(arriba[0][1])} Z"
    p.sombra_d(sac, 0.45, 6, 8)
    p.vol(sac, p.lin((0, "#ff8a5a"), (0.4, "#d8461e"), (1, "#6a1a08"), x2=0.2, y2=1), k=7, lo=0.4, ro=0.5)
    cl = p.clip(sac)
    p(f'<g clip-path="{cl}">')
    for i in range(1, 15):
        u = 0.2 + 0.78 * i / 15
        a, m, b = M(u, vb(u) + 0.1, 36), M(u + 0.01, 0.55, 30), M(u, vf(u), 2)
        p(f'<path d="M{F(a[0])} {F(a[1])} Q{F(m[0])} {F(m[1])} {F(b[0])} {F(b[1])}" stroke="#4a1006" stroke-width="5" fill="none" opacity="0.55"/>'
          f'<path d="M{F(a[0] + 5)} {F(a[1])} Q{F(m[0] + 5)} {F(m[1])} {F(b[0] + 5)} {F(b[1])}" stroke="#ffb08a" stroke-width="2" fill="none" opacity="0.45"/>')
    # boca abierta con forro gris y esquina doblada
    o1, o2, o3 = M(0.2, 0.3, 30), M(0.36, 0.5, 28), M(0.22, 0.82, 6)
    p(f'<path d="M{F(o1[0])} {F(o1[1])} Q{F(o2[0])} {F(o2[1])} {F(o3[0])} {F(o3[1])} L{F(o3[0] - 30)} {F(o3[1])} L{F(o1[0] - 30)} {F(o1[1])} Z" fill="#1a1d22"/>')
    f1 = M(0.27, 0.62, 18)
    p(f'<path d="M{F(o2[0] - 6)} {F(o2[1])} L{F(f1[0] + 60)} {F(f1[1] + 6)} L{F(o3[0] + 6)} {F(o3[1])} Z" fill="{p.lin((0, "#c8ccd4"), (1, "#6a707a"))}"/>')
    z1, z2 = M(0.32, 0.86, 4), M(0.9, 0.78, 4)
    p(f'<path d="M{F(z1[0])} {F(z1[1] - 4)} L{F(z2[0])} {F(z2[1] - 4)}" stroke="#2a0a04" stroke-width="3" stroke-dasharray="3 2" opacity="0.8"/>')
    p("</g>")
    p.fin()


# ============================================================== 11. CUADERNO
def cuaderno():
    p = P("cuaderno_dibujo", 700, 460)
    r = random.Random(111)
    p.sombra_d("M22 52 L678 40 L682 430 L18 440 Z", 0.5, 8, 8)
    p.vol("M22 52 L678 40 L682 430 L18 440 Z", p.lin((0, "#3a2a20"), (1, "#140c08")), k=3, lo=0.3)
    pi_ = "M36 64 L340 58 L340 424 L32 428 Z"
    pd = "M360 58 L664 52 L668 418 L360 424 Z"
    for d in (pi_, pd):
        p.vol(d, p.lin((0, "#fbf6ea"), (0.6, "#f1e8d2"), (1, "#d8cba8"), x2=1, y2=1), k=3, lo=0.2, ro=0.3)
    p(f'<path d="M300 58 L340 58 L340 424 L300 426 Z" fill="{p.lin((0, "#000", 0), (1, "#000", 0.18), x2=1, y2=0)}"/>'
      f'<path d="M360 58 L400 57 L400 423 L360 424 Z" fill="{p.lin((0, "#000", 0.18), (1, "#000", 0), x2=1, y2=0)}"/>')
    # espiral
    for y in range(72, 414, 17):
        p(f'<ellipse cx="350" cy="{y}" rx="16" ry="6" fill="none" stroke="#2a2e34" stroke-width="4"/>'
          f'<path d="M336 {y - 2} Q344 {y - 7} 352 {y - 6}" stroke="#d8dee6" stroke-width="2" fill="none"/>'
          f'<circle cx="332" cy="{y + 1}" r="3" fill="#3a2a20"/><circle cx="368" cy="{y + 1}" r="3" fill="#3a2a20"/>')
    # dibujo a lápiz: paisaje con sol
    lap = "#4a4640"
    def tr(d, w=1.6, o=0.75):
        p(f'<path d="{d}" stroke="{lap}" stroke-width="{w}" fill="none" opacity="{o}" stroke-linecap="round" stroke-linejoin="round"/>')
    tr("M386 92 L640 88 L644 340 L388 344 Z", 1.2, 0.5)
    tr("M560 150 m-26 0 a26 26 0 1 0 52 0 a26 26 0 1 0 -52 0", 2)
    for k in range(12):
        a = k * math.pi / 6
        tr(f"M{560 + math.cos(a) * 34:.1f} {150 + math.sin(a) * 34:.1f} L{560 + math.cos(a) * 50:.1f} {150 + math.sin(a) * 50:.1f}", 1.6)
    tr("M388 262 L430 214 L456 236 L500 178 L540 226 L566 206 L610 250 L642 236", 2.2)
    for k in range(26):  # sombreado de las montañas
        x = 404 + k * 8
        tr(f"M{x} {270 - (k % 5) * 3} l10 -26", 1, 0.45)
    tr("M388 300 C440 280 500 296 560 284 C600 276 630 288 642 286", 2)
    tr("M450 340 C470 318 500 316 520 300", 1.4, 0.6)
    tr("M600 300 L600 262 M600 270 C580 250 586 232 600 226 C616 232 622 252 600 270", 1.8)
    for x0, y0 in ((430, 130), (452, 122), (480, 140)):
        tr(f"M{x0} {y0} q6 -6 12 0 q6 -6 12 0", 1.5)
    for _ in range(30):
        x, y = r.uniform(392, 636), r.uniform(306, 338)
        tr(f"M{x:.0f} {y:.0f} l{r.uniform(4, 12):.0f} 0", 0.9, 0.35)
    # página izquierda: bocetos tenues
    tr("M80 120 C120 100 160 130 200 110", 1.2, 0.3)
    tr("M90 300 C140 280 220 310 280 290", 1.2, 0.25)
    for k in range(6):
        tr(f"M{90 + k * 12} {200 + k * 2} l30 -40", 1, 0.2)
    p.grano("M36 64 L340 58 L340 424 L32 428 Z", "M360 58 L664 52 L668 418 L360 424 Z", op=0.6)
    # lápiz
    p(f'<g transform="translate(440 410) rotate(-28)">')
    if SOMBRA:
        p('<rect x="6" y="10" width="270" height="14" rx="4" fill="#000" opacity="0.35" filter="url(#blur8)"/>')
    p(f'<rect x="0" y="-8" width="220" height="16" fill="#e8b02a"/>'
      f'<rect x="0" y="-8" width="220" height="5" fill="#ffd866"/><rect x="0" y="3" width="220" height="5" fill="#a8740e"/>'
      f'<path d="M0 -3 L220 -3 M0 3 L220 3" stroke="#7a520a" stroke-width="0.8" opacity="0.6"/>'
      f'<path d="M220 -8 L256 -1 L256 1 L220 8 Z" fill="{p.lin((0, "#f2d4a4"), (1, "#b08050"))}"/>'
      f'<path d="M246 -2.6 L264 0 L246 2.6 Z" fill="#2a2a2e"/>'
      f'<path d="M220 -8 l5 3 l-2 3 l4 3 l-3 3 l3 4" stroke="#e8b02a" stroke-width="1.5" fill="none"/>'
      f'<rect x="-26" y="-9" width="28" height="18" fill="{p.lin((0, "#f0f2f4"), (0.4, "#b8bec6"), (1, "#5a6068"))}"/>'
      f'<path d="M-20 -9 L-20 9 M-14 -9 L-14 9 M-6 -9 L-6 9" stroke="#6a707a" stroke-width="1.2"/>'
      f'<rect x="-44" y="-8" width="18" height="16" rx="4" fill="{p.lin((0, "#ffb0b8"), (1, "#c05a6a"))}"/>'
      f'<path d="M-40 -5 L-28 -5" stroke="#fff" stroke-width="1.5" opacity="0.6"/></g>')
    p.fin()


# ============================================================== 12. ESTALACTITAS Y AGUA
def _gota_d(cx, cy, s):
    return (f"M{F(cx)} {F(cy - 14 * s)} C{F(cx + 3 * s)} {F(cy - 6 * s)} {F(cx + 8 * s)} {F(cy - 1 * s)} {F(cx + 8 * s)} {F(cy + 5 * s)} "
            f"A{F(8 * s)} {F(8 * s)} 0 0 1 {F(cx - 8 * s)} {F(cy + 5 * s)} C{F(cx - 8 * s)} {F(cy - 1 * s)} {F(cx - 3 * s)} {F(cy - 6 * s)} {F(cx)} {F(cy - 14 * s)} Z")


def _gota(p, cx, cy, s=1.0):
    d = _gota_d(cx, cy, s)
    p(f'<path d="{d}" fill="{p.lin((0, "#e8f6ff", 0.75), (0.6, "#7ab0d8", 0.6), (1, "#22405e", 0.85), x2=0.4, y2=1)}"/>'
      f'<path d="{d}" fill="none" stroke="#e8f6ff" stroke-width="{F(0.9 * s)}" opacity="0.6"/>'
      f'<ellipse cx="{F(cx - 3 * s)}" cy="{F(cy + 1 * s)}" rx="{F(2 * s)}" ry="{F(3.2 * s)}" fill="#fff"/>'
      f'<path d="M{F(cx + 5.5 * s)} {F(cy + 4 * s)} A{F(6 * s)} {F(6 * s)} 0 0 1 {F(cx + 1 * s)} {F(cy + 10 * s)}" stroke="{LUZ}" stroke-width="{F(0.9 * s)}" fill="none" opacity="0.45"/>')


def _espeleo(p, cx, y0, L, wb, sem, arriba=True, romo=0.0):
    """Estalactita (arriba=True: cuelga de y0 hacia abajo) o estalagmita (crece de y0 hacia arriba). Devuelve el path."""
    r = random.Random(sem)
    n = 26
    s = 1 if arriba else -1
    izq, der = [], []
    for i in range(n + 1):
        t = i / n
        w = wb / 2 * ((1 - t) ** (0.75 if arriba else 0.55)) * (1 + 0.08 * math.sin(t * 17 + sem)) + romo * wb * 0.5 * (t ** 3)
        w = max(w, 1.5 if t < 1 else 0.5)
        y = y0 + s * L * t
        o = math.sin(t * 5 + sem) * wb * 0.06
        izq.append((cx + o - w - r.uniform(0, 1.5), y)); der.append((cx + o + w + r.uniform(0, 1.5), y))
    if arriba:
        pts = izq + [(cx + math.sin(5 + sem) * wb * 0.06, y0 + L + 4)] + der[::-1]
    else:
        tipx = cx + math.sin(5 + sem) * wb * 0.06
        pts = izq[:-1] + [(tipx - romo * wb * 0.3, y0 - L - 2), (tipx + romo * wb * 0.3, y0 - L - 2)] + der[:-1][::-1]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    g = p.lin((0, "#8a6446"), (0.2, "#6b4a32"), (0.5, "#3d2a1f"), (0.8, "#1a120d"), (1, "#141b29"), x2=1, y2=0)
    p.vol(d, g, k=5, luz=LUZ, lo=0.5, ro=0.6)
    cl = p.clip(d)
    p(f'<g clip-path="{cl}">')
    for k in range(int(L / 26)):  # anillos de crecimiento: tramos cortos y sueltos
        y = y0 + s * r.uniform(10, L * 0.9)
        x0_ = cx + r.uniform(-0.6, 0.3) * wb
        p(f'<path d="M{F(x0_)} {F(y)} q{r.uniform(8, 20):.1f} {F(s * r.uniform(2, 5))} {r.uniform(18, 40):.1f} {r.uniform(-2, 3):.1f}" stroke="#1a120d" stroke-width="{r.uniform(1.2, 2.5):.1f}" fill="none" opacity="{r.uniform(0.15, 0.3):.2f}" stroke-linecap="round"/>'
          f'<path d="M{F(x0_)} {F(y - s * 2.5)} q{r.uniform(8, 20):.1f} {F(s * 3)} {r.uniform(14, 30):.1f} 0" stroke="#c89a70" stroke-width="1" fill="none" opacity="0.2" stroke-linecap="round"/>')
    for _ in range(int(L / 18)):  # manchas y vetas
        t = r.uniform(0, 0.9)
        p(f'<ellipse cx="{F(cx + r.uniform(-0.5, 0.5) * wb * (1 - t))}" cy="{F(y0 + s * L * t)}" rx="{r.uniform(3, 10):.1f}" ry="{r.uniform(6, 22):.1f}" fill="{r.choice(("#1a120d", "#6b4a32", "#141b29"))}" opacity="{r.uniform(0.15, 0.35):.2f}"/>')
    for k in range(2):  # película de agua: brillo que sigue la forma
        pts_ = []
        for i in range(12):
            t = 0.04 + 0.8 * i / 11
            w_ = wb / 2 * ((1 - t) ** (0.75 if arriba else 0.55)) * (1 + 0.08 * math.sin(t * 17 + sem))
            pts_.append((cx + math.sin(t * 5 + sem) * wb * 0.06 - w_ * (0.55 - k * 0.2), y0 + s * L * t))
        p(f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in pts_)}" stroke="#fff" stroke-width="{2.5 - k}" fill="none" opacity="{0.35 - k * 0.12:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')
    for _ in range(int(L / 10)):  # cuarzo húmedo
        t = r.uniform(0.05, 0.9)
        x = cx + r.uniform(-0.4, 0.3) * wb * (1 - t)
        p(f'<circle cx="{F(x)}" cy="{F(y0 + s * L * t)}" r="{r.uniform(0.8, 2):.1f}" fill="#fff" opacity="{r.uniform(0.4, 0.95):.2f}"/>')
    p("</g>")
    return d


def _techo(p, w, y, sem):
    r = random.Random(sem)
    pts = [(0, 0), (w, 0)] + [(w - i * w / 10, y + r.uniform(-10, 14)) for i in range(11)]
    d = poly(pts)
    p.vol(d, p.lin((0, "#3d2a1f"), (0.6, "#2a1c14"), (1, "#1a120d")), k=4, lo=0.3, ro=0.3)
    return d


def estalactitas():
    for n, w, h, parts, sem in (("estalactita_a", 180, 645, ((90, 600, 130),), 1),
                                ("estalactita_b", 160, 420, ((80, 400, 140),), 2),
                                ("estalactita_c", 260, 745, ((150, 690, 160), (66, 360, 80)), 3)):
        p = P(n, w, h)
        for i, (cx, L, wb) in enumerate(parts):
            _espeleo(p, cx, 6, L - 30 * (n == "estalactita_b"), wb, sem + i)
        _techo(p, w, 16, sem)
        cx, L, wb = parts[0]
        L2 = L - 30 * (n == "estalactita_b")
        _gota(p, cx + math.sin(5 + sem) * wb * 0.06, 6 + L2 + 16, 0.9)
        if len(parts) > 1:
            c2, l2_, _ = parts[1]
            _gota(p, c2 + math.sin(6 + sem) * 80 * 0.06, 6 + l2_ + 14, 0.7)
        p.fin()
    for n, w, h, parts, sem in (("estalagmita_a", 220, 520, ((110, 470, 170, 0.25),), 11),
                                ("estalagmita_b", 340, 400, ((140, 340, 190, 0.35), (250, 200, 140, 0.4)), 12)):
        p = P(n, w, h)
        yb = h - 22
        p.sombra(w / 2, yb + 4, w * 0.45, 12, 0.6)
        for i, (cx, L, wb, romo) in reversed(list(enumerate(parts))):
            _espeleo(p, cx, yb + 4, L, wb, sem + i, arriba=False, romo=romo)
        # colada a los pies, húmeda
        pie = f"M6 {yb + 6} C30 {yb - 22} {w - 30} {yb - 26} {w - 6} {yb + 6} Q{w / 2} {yb + 18} 6 {yb + 6} Z"
        p.vol(pie, p.lin((0, "#7a5a40"), (1, "#1a120d"), x2=1, y2=0), k=4, lo=0.4, ro=0.4)
        p(f'<ellipse cx="{F(w * 0.42)}" cy="{yb + 4}" rx="{F(w * 0.25)}" ry="5" fill="{LUZ}" opacity="0.35"/>')
        for cx, L, wb, romo in parts:
            tipx = cx + math.sin(5 + sem) * wb * 0.06
            p(f'<ellipse cx="{F(tipx - 3)}" cy="{F(yb + 4 - L + 4)}" rx="{F(wb * romo * 0.35 + 4)}" ry="3" fill="#fff" opacity="0.55"/>')
        p.fin()
    p = P("gota", 60, 96)
    _gota(p, 30, 58, 2.6)
    p.fin()
    p = P("salpicadura", 320, 230)
    r = random.Random(121)
    p(f'<ellipse cx="160" cy="180" rx="150" ry="40" fill="{p.rad((0, "#3a4658"), (0.7, "#141b29"), (1, "#07090f", 0.0))}"/>')
    for k, (rx, op) in enumerate(((140, 0.25), (110, 0.4), (78, 0.55))):
        p(f'<ellipse cx="160" cy="178" rx="{rx}" ry="{rx * 0.24:.1f}" fill="none" stroke="#a9d6f5" stroke-width="2" opacity="{op}"/>'
          f'<ellipse cx="160" cy="179.5" rx="{rx}" ry="{rx * 0.24:.1f}" fill="none" stroke="{LUZ}" stroke-width="1.2" opacity="{op * 0.7:.2f}" '
          f'clip-path="{p.clip("M0 0 L160 0 L160 180 L0 180 Z")}"/>')
    # corona
    cor = "M112 176 " + " ".join(f"L{112 + i * 8 + 4} {176 - r.uniform(22, 44):.0f} L{112 + i * 8 + 8} 176" for i in range(12)) + " Q160 188 112 176 Z"
    p(f'<path d="{cor}" fill="{p.lin((0, "#e8f6ff", 0.85), (1, "#5f9fd1", 0.5))}"/>'
      f'<ellipse cx="160" cy="176" rx="48" ry="9" fill="none" stroke="#e8f6ff" stroke-width="2.5" opacity="0.8"/>'
      f'<path d="M160 172 C158 150 162 120 160 98" stroke="#cfe8ff" stroke-width="6" stroke-linecap="round" opacity="0.7"/>')
    _gota(p, 160, 78, 0.8)
    for _ in range(14):
        a = r.uniform(math.pi * 1.05, math.pi * 1.95)
        rr = r.uniform(50, 95)
        x, y = 160 + math.cos(a) * rr, 160 + math.sin(a) * rr * 0.9
        p(f'<circle cx="{F(x)}" cy="{F(y)}" r="{r.uniform(1.5, 4):.1f}" fill="#e8f6ff" opacity="0.85"/>'
          f'<circle cx="{F(x - 0.8)}" cy="{F(y - 0.8)}" r="0.9" fill="#fff"/>')
    p.fin()


# ============================================================== 13. MURCIÉLAGO
def _ala(p, S, E, W, tips, tobillo, oscuro=False):
    pts = [S, E, W] + tips + [tobillo]
    d = f"M{F(S[0])} {F(S[1])} Q{F(E[0])} {F(E[1])} {F(W[0])} {F(W[1])} L{F(tips[0][0])} {F(tips[0][1])}"
    seq = tips + [tobillo]
    for a, b in zip(seq, seq[1:]):
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        c = lerp(m, W, 0.22)
        d += f" Q{F(c[0])} {F(c[1])} {F(b[0])} {F(b[1])}"
    d += f" L{F(S[0])} {F(S[1])} Z"
    if oscuro:
        p(f'<path d="{d}" fill="{p.lin((0, "#3a2a26"), (1, "#140c0c"), x2=1, y2=1)}"/>')
        p(f'<path d="{d}" fill="#000" opacity="0.3"/>')
    else:
        p.vol(d, p.rad((0, "#7a4a3a"), (0.5, "#4a2e28"), (1, "#20140f"), cx=0.3, cy=0.3, r=0.8), k=4, lo=0.35, ro=0.45)
    col = "#2a1a16" if oscuro else "#8a6052"
    p(f'<path d="M{F(S[0])} {F(S[1])} Q{F(E[0])} {F(E[1])} {F(W[0])} {F(W[1])}" stroke="{col}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    for tp in tips:
        mx, my = lerp(W, tp, 0.5)
        p(f'<path d="M{F(W[0])} {F(W[1])} Q{F(mx + 4)} {F(my + 4)} {F(tp[0])} {F(tp[1])}" stroke="{col}" stroke-width="2.2" fill="none"/>')
    if not oscuro:
        for tp in tips[1:]:
            q = lerp(W, tp, 0.45)
            p(f'<path d="M{F(q[0])} {F(q[1])} Q{F((q[0] + S[0]) / 2)} {F((q[1] + S[1]) / 2 + 10)} {F(lerp(S, tobillo, 0.5)[0])} {F(lerp(S, tobillo, 0.5)[1])}" stroke="#a06a58" stroke-width="0.8" fill="none" opacity="0.35"/>')
    p(f'<path d="M{F(W[0])} {F(W[1])} l-4 -9" stroke="#e8d6c8" stroke-width="2.5" stroke-linecap="round"/>')


def murcielago():
    for n, arriba in (("murcielago_a", True), ("murcielago_b", False)):
        p = P(n, 440, 320)
        r = random.Random(131)
        tob = (140, 186)
        if arriba:
            _ala(p, (234, 146), (248, 100), (214, 42), [(146, 8), (112, 46), (122, 96), (162, 138)], tob, oscuro=True)
        else:
            _ala(p, (232, 160), (252, 206), (226, 252), [(152, 294), (112, 264), (118, 224), (152, 196)], tob, oscuro=True)
        # cola y patas
        p(f'<path d="M168 170 L136 190 L120 176 Q140 172 168 160 Z" fill="#2a1a16"/>'
          f'<path d="M172 172 L138 190 M138 190 l-8 3 M138 190 l-7 -1 M138 190 l-8 7" stroke="#3a2420" stroke-width="3" stroke-linecap="round"/>')
        cuerpo = "M168 158 C170 136 200 128 230 132 C256 136 270 148 268 162 C266 178 240 186 212 184 C186 182 166 176 168 158 Z"
        p.vol(cuerpo, p.lin((0, "#8a6248"), (0.5, "#5a3e30"), (1, "#24160f")), k=5, lo=0.4, ro=0.5)
        cl = p.clip(cuerpo)
        p(f'<g clip-path="{cl}">')
        for _ in range(90):
            x, y = r.uniform(166, 270), r.uniform(130, 186)
            p(f'<path d="M{F(x)} {F(y)} l{r.uniform(-7, -3):.1f} {r.uniform(1, 3):.1f}" stroke="{r.choice(("#a07858", "#3a2620", "#6a4a38"))}" stroke-width="1.3" opacity="0.7"/>')
        p("</g>")
        # cabeza
        p.vol("M290 120 L284 92 L268 122 Z", p.lin((0, "#7a5444"), (1, "#2a1a14")), k=2, lo=0.3, gr=False)
        cab = "M254 150 C252 130 268 120 284 124 C298 128 306 140 312 148 L316 152 C312 158 300 162 290 164 C272 168 256 164 254 150 Z"
        p.vol(cab, p.lin((0, "#9a6e52"), (0.5, "#5e4032"), (1, "#24160f")), k=4, lo=0.45, ro=0.5)
        p.vol("M278 126 L272 88 L262 128 Z", p.lin((0, "#8a6050"), (1, "#3a2820")), k=2, lo=0.3, gr=False)
        p('<path d="M274 124 L271 98 L266 126 Z" fill="#c08070" opacity="0.7"/>'
          '<circle cx="292" cy="140" r="3.6" fill="#0a0606"/><circle cx="293" cy="139" r="1.2" fill="#fff"/>'
          '<path d="M312 150 l5 1" stroke="#1a0e0a" stroke-width="2"/><path d="M296 158 Q304 160 312 155" stroke="#1a0e0a" stroke-width="1.5" fill="none"/>'
          '<path d="M300 158 l1 4 l2 -3" fill="#f4ece0"/>')
        if arriba:
            _ala(p, (222, 150), (236, 104), (188, 46), [(92, 14), (54, 58), (72, 116), (124, 156)], tob)
        else:
            _ala(p, (220, 162), (238, 214), (198, 262), [(112, 306), (66, 272), (76, 226), (126, 194)], tob)
        p.fin()


# ============================================================== 14. MOSCA
def mosca():
    for n, ang in (("mosca_a", 22), ("mosca_b", 48)):
        p = P(n, 200, 220)
        r = random.Random(141)
        cx = 100
        # patas
        for sg in (-1, 1):
            for (x0, y0), (x1, y1), (x2, y2) in (((cx - 12, 82), (cx - 34, 66), (cx - 44, 34)),
                                                  ((cx - 16, 96), (cx - 46, 100), (cx - 68, 120)),
                                                  ((cx - 14, 108), (cx - 40, 138), (cx - 52, 180))):
                X = lambda v: cx + sg * (v - cx)
                p(f'<path d="M{F(X(x0))} {y0} L{F(X(x1))} {y1} L{F(X(x2))} {y2}" stroke="#141416" stroke-width="2.6" fill="none" stroke-linejoin="round"/>'
                  f'<path d="M{F(X(x1))} {y1} l{F(sg * -2)} -3 M{F((X(x1) + X(x2)) / 2)} {(y1 + y2) / 2:.0f} l{F(sg * -3)} -1" stroke="#141416" stroke-width="1"/>')
        # alas
        for sg in (-1, 1):
            p(f'<g transform="translate({cx + sg * 8} 90) rotate({sg * ang})">')
            wd = "M0 0 C-14 20 -16 60 -4 92 C2 100 12 96 14 84 C18 56 12 20 0 0 Z"
            if sg == 1:
                wd = "M0 0 C14 20 16 60 4 92 C-2 100 -12 96 -14 84 C-18 56 -12 20 0 0 Z"
            p(f'<path d="{wd}" fill="{p.lin((0, "#dff0ff", 0.55), (0.5, "#f0d8ff", 0.35), (1, "#cfe8ff", 0.45))}" stroke="#2a2a2e" stroke-width="0.9" opacity="0.95"/>')
            s = sg
            for v in (f"M0 4 C{-s * 6} 30 {-s * 6} 60 {-s * 2} 90", f"M0 6 C{s * 4} 30 {s * 8} 60 {s * 8} 86",
                      f"M0 10 C{-s * 10} 30 {-s * 12} 50 {-s * 11} 70", f"M{-s * 4} 50 L{s * 6} 54"):
                p(f'<path d="{v}" stroke="#2a2a2e" stroke-width="0.8" fill="none" opacity="0.7"/>')
            p(f'<path d="M{-s * 6} 20 C{-s * 8} 40 {-s * 8} 56 {-s * 6} 66" stroke="#fff" stroke-width="1.5" opacity="0.6" fill="none"/>')
            p("</g>")
        # abdomen, tórax, cabeza
        ab = f"M{cx} 104 C{cx + 26} 106 {cx + 28} 150 {cx + 18} 166 C{cx + 10} 178 {cx - 10} 178 {cx - 18} 166 C{cx - 28} 150 {cx - 26} 106 {cx} 104 Z"
        p.vol(ab, p.rad((0, "#8a8e96"), (0.6, "#3a3c42"), (1, "#121316"), cx=0.38, cy=0.3), k=3, lo=0.3, ro=0.5)
        cl = p.clip(ab)
        p(f'<g clip-path="{cl}">')
        for j, y in enumerate((116, 132, 148, 162)):
            for i in (-1, 1):
                p(f'<path d="M{cx + i * 2} {y} l{i * 22} -2 l0 10 l{-i * 22} 2 Z" fill="{"#0d0e10" if (i + j) % 2 else "#a0a4ac"}" opacity="0.6"/>')
        p(f'<rect width="200" height="220" fill="{p.lin((0, "#3fe0a0", 0.12), (0.5, "#c040ff", 0.08), (1, "#3fa0ff", 0.1), x2=1, y2=1)}"/></g>')
        p(f'<ellipse cx="{cx - 8}" cy="120" rx="4" ry="8" fill="#fff" opacity="0.5"/>')
        tor = f"M{cx} 68 C{cx + 22} 68 {cx + 26} 84 {cx + 24} 96 C{cx + 20} 110 {cx - 20} 110 {cx - 24} 96 C{cx - 26} 84 {cx - 22} 68 {cx} 68 Z"
        p.vol(tor, p.lin((0, "#7a7e86"), (1, "#1a1b1e"), x2=1, y2=1), k=3, lo=0.35, ro=0.5)
        for x in (-8, 0, 8):
            p(f'<path d="M{cx + x} 72 L{cx + x * 1.1} 104" stroke="#0d0e10" stroke-width="3" opacity="0.7"/>')
        for _ in range(26):
            x, y = r.uniform(cx - 20, cx + 20), r.uniform(72, 104)
            p(f'<path d="M{F(x)} {F(y)} l{r.uniform(-2, 2):.1f} {r.uniform(3, 5):.1f}" stroke="#000" stroke-width="0.9"/>')
        p.vol(f"M{cx - 14} 66 C{cx - 14} 54 {cx + 14} 54 {cx + 14} 66 C{cx + 10} 72 {cx - 10} 72 {cx - 14} 66 Z", "#3a3530", k=2, lo=0.3, gr=False)
        for sg in (-1, 1):
            ex = cx + sg * 13
            p(f'<ellipse cx="{ex}" cy="50" rx="15" ry="18" fill="{p.rad((0, "#e8603a"), (0.55, "#9a2814"), (1, "#3a0a04"), cx=0.35, cy=0.3)}" transform="rotate({sg * -14} {ex} 50)"/>')
            for k in range(-2, 3):
                p(f'<path d="M{ex - 12} {50 + k * 5} Q{ex} {50 + k * 5 + 3} {ex + 12} {50 + k * 5}" stroke="#3a0a04" stroke-width="0.5" fill="none" opacity="0.5"/>')
            p(f'<ellipse cx="{ex - 5}" cy="43" rx="4" ry="5" fill="#fff" opacity="0.55"/>')
        p(f'<path d="M{cx - 3} 34 L{cx + 3} 34 L{cx + 2} 62 L{cx - 2} 62 Z" fill="#6a6058"/>')
        p.fin()


# ============================================================== 15. CUERDA Y MOSQUETÓN
def cuerda():
    p = P("cuerda", 80, 1400)
    r = random.Random(151)
    cx, R = 40, 11
    fin = 1376
    p(f'<rect x="{cx - R}" y="0" width="{2 * R}" height="{fin}" fill="#1d3a70"/>')
    for row in range(int(fin / 4.6)):
        y = row * 4.6
        for c in range(4):
            x = cx - R + 2.8 + c * 5.5
            col = "#f08a1a" if (row // 2 + c) % 9 == 0 else ("#e8f0ff" if (row // 2 - c) % 13 == 0 else r.choice(("#2f62b8", "#3a74d0", "#244e98")))
            p(f'<ellipse cx="{F(x)}" cy="{F(y + (c % 2) * 2.3)}" rx="3.2" ry="1.9" fill="{col}" transform="rotate({35 if c % 2 else -35} {F(x)} {F(y + (c % 2) * 2.3)})"/>')
    p(f'<rect x="{cx - R}" y="0" width="{2 * R}" height="{fin}" fill="{p.lin((0, "#ffffff", 0.0), (0.18, "#ffe6c0", 0.35), (0.4, "#fff", 0.0), (0.7, "#000", 0.35), (0.92, "#000", 0.6), (1, RIM, 0.6), x2=1, y2=0)}"/>')
    p(f'<rect x="{cx - R}" y="{fin - 30}" width="{2 * R}" height="26" rx="2" fill="{p.lin((0, "#f4f4f4"), (0.6, "#b8b8b8"), (1, "#4a4a4a"), x2=1, y2=0)}"/>'
      f'<path d="M{cx - R} {fin - 24} L{cx + R} {fin - 22} M{cx - R} {fin - 14} L{cx + R} {fin - 12}" stroke="#8a8a8a" stroke-width="1"/>'
      f'<path d="M{cx - R + 1} {fin - 4} Q{cx} {fin + 8} {cx + R - 1} {fin - 4} Z" fill="#162e5a"/>')
    for k in range(7):
        p(f'<path d="M{cx - 8 + k * 2.6} {fin} l{r.uniform(-2, 2):.1f} {r.uniform(6, 12):.1f}" stroke="#3a74d0" stroke-width="1.2"/>')
    p.fin()
    p = P("mosqueton", 160, 260)
    D = "M126 210 C120 236 104 246 84 246 C60 246 42 230 42 204 L42 60 C42 32 62 14 90 14 C116 14 136 34 136 66"
    g = p.lin((0, "#ffc890"), (0.4, "#f07a2a"), (1, "#6a2406"), x1=30, y1=0, x2=150, y2=0, us=True)
    p(f'<path d="{D}" stroke="#000" stroke-width="18" fill="none" opacity="0.3" transform="translate(4 5)" filter="url(#blur8)"/>' if SOMBRA else "")
    p(f'<path d="{D}" stroke="{g}" stroke-width="17" fill="none" stroke-linecap="round"/>'
      f'<path d="{D}" stroke="#fff0dc" stroke-width="3" fill="none" opacity="0.7" transform="translate(-4 -2)"/>'
      f'<path d="{D}" stroke="{RIM}" stroke-width="2.5" fill="none" opacity="0.6" transform="translate(5 3)"/>')
    p('<path d="M136 66 L127 206" stroke="#5a6068" stroke-width="10" stroke-linecap="round"/>'
      '<path d="M135 68 L126 204" stroke="#e8eef4" stroke-width="4" stroke-linecap="round"/>'
      '<path d="M130 70 l12 -8 l-2 12 Z" fill="#a84a12"/>'
      '<circle cx="126" cy="208" r="6" fill="#c8ccd2" stroke="#4a4e56" stroke-width="2"/>')
    p.fin()


# ============================================================== 16-17. TIENDAS
def tienda_campana():
    p = P("tienda_campana", 760, 480)
    r = random.Random(161)
    p.sombra(380, 448, 330, 18, 0.6)
    p(f'<ellipse cx="420" cy="452" rx="150" ry="20" fill="{LUZ}" opacity="0.4" filter="url(#blur8)"/>')
    for x0, x1 in ((90, 18), (670, 744)):  # vientos
        p(f'<path d="M{x0 + (40 if x0 < 300 else -40)} 300 L{x1} 448" stroke="#d8d0c0" stroke-width="1.5" opacity="0.7"/>'
          f'<path d="M{x1 - 4} 440 L{x1 + 4} 456" stroke="#9aa0a8" stroke-width="3"/>')
    domo = "M80 440 C88 236 226 108 380 104 C534 108 672 236 680 440 Z"
    p.vol(domo, p.lin((0, "#ffc27a"), (0.35, "#f07a1e"), (0.8, "#a8400e"), (1, "#5a1e06"), x2=1, y2=1), k=10, lo=0.4, ro=0.55)
    cl = p.clip(domo)
    p(f'<g clip-path="{cl}">')
    p(f'<ellipse cx="410" cy="330" rx="220" ry="160" fill="{p.rad((0, "#ffd890", 0.5), (1, "#ffd890", 0))}"/>')
    for d in ("M120 446 C150 250 260 120 380 106 C470 110 560 200 620 446", "M140 446 C200 250 300 140 380 106 C500 120 640 260 650 446",
              "M84 330 C200 300 560 300 676 330"):
        p(f'<path d="{d}" stroke="#7a2a08" stroke-width="7" fill="none" opacity="0.55"/><path d="{d}" stroke="#ffd0a0" stroke-width="2" fill="none" opacity="0.5" transform="translate(-3 -3)"/>')
    for _ in range(18):  # arrugas de la tela
        x, y = r.uniform(120, 640), r.uniform(150, 400)
        p(f'<path d="M{F(x)} {F(y)} q{r.uniform(10, 30):.0f} {r.uniform(-8, 8):.0f} {r.uniform(30, 60):.0f} {r.uniform(-4, 14):.0f}" stroke="#7a2a08" stroke-width="2" fill="none" opacity="0.3"/>')
    p(f'<rect x="60" y="410" width="640" height="40" fill="{p.lin((0, "#3a3f46"), (1, "#16181c"))}"/>'
      f'<path d="M60 411 L700 411" stroke="#8a929c" stroke-width="2" opacity="0.6"/></g>')
    # puerta entreabierta con luz dentro
    hueco = "M380 432 L380 268 C400 236 450 236 470 268 L472 432 Z"
    p(f'<path d="{hueco}" fill="{p.rad((0, "#fff4d8"), (0.35, "#ffcf8a"), (0.75, "#e8842a"), (1, "#7a3010"), cx=0.5, cy=0.6, r=0.6)}"/>'
      f'<path d="M386 432 Q420 424 466 432 L470 412 Q420 404 384 412 Z" fill="#c86a2a" opacity="0.7"/>'
      f'<path d="M392 400 L400 360 L460 362 L466 404 Z" fill="#6a2a10" opacity="0.35"/>')
    hoja = "M300 434 L300 270 C310 226 360 216 380 228 C384 232 386 250 382 270 C376 330 388 390 382 434 Z"
    p.vol(hoja, p.lin((0, "#f08a3a"), (1, "#8a3410"), x2=1, y2=0), k=5, lo=0.3, ro=0.4)
    p('<path d="M372 236 C380 300 374 380 380 432" stroke="#2a2e34" stroke-width="3" fill="none"/>'
      '<path d="M372 236 C380 300 374 380 380 432" stroke="#8a929c" stroke-width="1" fill="none" stroke-dasharray="2 2"/>'
      f'<path d="M376 238 C378 300 374 380 378 432" stroke="{LUZ}" stroke-width="3" fill="none" opacity="0.8"/>'
      '<path d="M320 300 C340 320 330 360 348 400" stroke="#7a2a08" stroke-width="2" fill="none" opacity="0.4"/>')
    p.vol("M392 236 C420 222 462 232 474 260 C460 252 420 244 392 250 Z", p.lin((0, "#f08a3a"), (1, "#7a2a08")), k=3, lo=0.3, gr=False)
    p('<path d="M372 270 l8 -6 l2 10 Z" fill="#c8ccd2"/>')
    p.fin()


def tienda_1962():
    p = P("tienda_1962", 820, 500)
    r = random.Random(171)
    FR, FL, FA = (470, 452), (140, 446), (300, 120)
    RA, RR = (610, 96), (760, 418)
    FRIA, BORDE = "#e8f6ff", "#ffcf8a"
    p.sombra(450, 456, 360, 16, 0.55)
    # vientos y estacas
    for a, b in (((300, 120), (60, 470)), ((610, 96), (800, 300)), ((520, 300), (650, 478)), ((680, 260), (812, 440)), ((620, 180), (790, 360))):
        p(f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" stroke="#c8b890" stroke-width="1.8" opacity="0.8"/>'
          f'<rect x="{b[0] - 3}" y="{b[1] - 14}" width="6" height="16" fill="#6a4a28"/>')
    # techo lateral con caída de lona
    techo = f"M{FA[0]} {FA[1]} Q455 120 {RA[0]} {RA[1]} L{RR[0]} {RR[1]} Q615 440 {FR[0]} {FR[1]} Z"
    p.vol(techo, p.lin((0, "#b8b07a"), (0.5, "#8a8456"), (1, "#4f4a2c"), x2=1, y2=1), k=6, luz=FRIA, lo=0.35, ro=0.4, rim=BORDE)
    cl = p.clip(techo)
    p(f'<g clip-path="{cl}">')
    for k in range(1, 6):
        t = k / 6
        a, b = lerp(FA, RA, t), lerp(FR, RR, t)
        p(f'<path d="M{F(a[0])} {F(a[1] + 4)} Q{F((a[0] + b[0]) / 2 - 8)} {F((a[1] + b[1]) / 2)} {F(b[0])} {F(b[1])}" stroke="#3d3a20" stroke-width="2.5" fill="none" opacity="0.45"/>')
    for _ in range(10):
        x, y = r.uniform(380, 700), r.uniform(150, 400)
        p(f'<ellipse cx="{F(x)}" cy="{F(y)}" rx="{r.uniform(8, 26):.0f}" ry="{r.uniform(5, 14):.0f}" fill="#3d3a20" opacity="{r.uniform(0.1, 0.25):.2f}"/>')
    p('<path d="M480 380 L560 392 L556 420 L476 410 Z" fill="#9a9264" opacity="0.8"/><path d="M480 380 L560 392 L556 420 L476 410 Z" fill="none" stroke="#4f4a2c" stroke-width="1.5" stroke-dasharray="4 3"/>')
    p("</g>")
    # fachada (triángulo) con puerta atada
    fach = f"M{FA[0]} {FA[1]} L{FR[0]} {FR[1]} L{FL[0]} {FL[1]} Z"
    p.vol(fach, p.lin((0, "#c8c08a"), (0.6, "#9a9262"), (1, "#5a5432")), k=6, luz=FRIA, lo=0.4, ro=0.3, rim=BORDE)
    p(f'<path d="M300 150 L256 448 L352 450 Z" fill="{p.lin((0, "#2a2418"), (1, "#0d0b08"))}"/>'
      f'<path d="M300 150 L270 448 L340 450 Z" fill="{p.rad((0, "#ffcf8a", 0.5), (1, "#ffcf8a", 0))}"/>')
    for sg, X0 in ((-1, 256), (1, 352)):
        sol = f"M300 140 L{X0} 448 L{X0 + sg * 40} 446 Q{X0 + sg * 10} 330 {300 + sg * 30} 240 Z"
        p.vol(sol, p.lin((0, "#d8d09a"), (1, "#6a6440"), x2=1 if sg < 0 else 0, y2=1), k=4, luz=FRIA, lo=0.4, ro=0.3, gr=False)
        p(f'<path d="M{300 + sg * 30} 250 Q{X0 + sg * 6} 330 {X0 + sg * 20} 440" stroke="#4f4a2c" stroke-width="2" fill="none" opacity="0.5"/>')
        p(f'<path d="M{X0 + sg * 6} 330 l{sg * 26} 4" stroke="#6a4a28" stroke-width="3"/>')
    p(f'<path d="{fach}" fill="none" stroke="#3d3a20" stroke-width="2" opacity="0.6"/>')
    # mástiles con remate
    for x, y in (FA, RA):
        p(f'<rect x="{x - 4}" y="{y - 30}" width="8" height="34" fill="#6a4a28"/><circle cx="{x}" cy="{y - 32}" r="6" fill="#8a6438"/>')
    # escarcha y nieve al pie
    for k in range(40):
        t = k / 39
        q = lerp(FL, FR, t) if k < 20 else lerp(FR, RR, (k - 20) / 19)
        p(f'<ellipse cx="{F(q[0] + r.uniform(-6, 6))}" cy="{F(q[1] - 2)}" rx="{r.uniform(12, 24):.0f}" ry="{r.uniform(4, 9):.0f}" fill="{r.choice(("#e8f6ff", "#d0e8f8", "#a9d6f5"))}"/>')
    p.grano(fach, op=0.8)
    p.fin()


# ============================================================== 18. TELÉFONO DE CAMPO
def telefono():
    p = P("telefono_campo", 400, 420)
    r = random.Random(181)
    Fq = [(60, 150), (250, 162), (250, 380), (60, 370)]
    Sq = [(250, 162), (316, 128), (316, 336), (250, 380)]
    Tq = [(60, 150), (126, 118), (316, 128), (250, 162)]
    p.sombra_d(poly([(60, 370), (250, 380), (316, 336), (130, 330)]), 0.55, 8, 10)
    # cable de línea saliendo al suelo
    p('<path d="M300 320 C330 360 350 380 396 396" stroke="#1a1a1a" stroke-width="5" fill="none"/><path d="M300 318 C330 358 350 378 396 394" stroke="#6a6a6a" stroke-width="1.2" fill="none"/>')
    for q, g in ((Sq, p.lin((0, "#7a4a22"), (1, "#3a1e0a"))), (Fq, p.lin((0, "#b07a42"), (0.5, "#8a5a2e"), (1, "#4a2a12"), x2=1, y2=1)), (Tq, p.lin((0, "#d09a5a"), (1, "#8a5a2e"), x2=1, y2=0))):
        d = poly(q)
        p.vol(d, g, k=4, lo=0.35, ro=0.45)
        cl = p.clip(d)
        p(f'<g clip-path="{cl}">')
        for k in range(16):
            y = q[0][1] + 6 + k * 15 + r.uniform(-3, 3)
            p(f'<path d="M{q[0][0]} {F(y)} C{(q[0][0] + q[1][0]) / 2} {F(y + r.uniform(-6, 6))} {(q[0][0] + q[1][0]) / 2} {F(y + r.uniform(-6, 6))} {q[1][0]} {F(y + q[1][1] - q[0][1])}" stroke="#3a1e0a" stroke-width="{r.uniform(0.8, 1.8):.1f}" fill="none" opacity="0.35"/>')
        p("</g>")
    # tapa frontal con bisagras y esquinas metálicas
    p('<path d="M74 172 L236 180 L236 362 L74 354 Z" fill="none" stroke="#2a1404" stroke-width="2.5" opacity="0.6"/>'
      '<path d="M76 174 L238 182" stroke="#e8b878" stroke-width="1.5" opacity="0.6"/>')
    for x, y in ((60, 150), (250, 162), (60, 370), (250, 380)):
        p(f'<path d="M{x - 2} {y - 2} l14 1 l0 4 l-10 0 l0 10 l-4 0 Z" fill="#5a5048" transform="translate({0 if x < 100 else -10} {0 if y < 200 else -12})"/>')
    # campanillas y bornes
    for x in (120, 186):
        p(f'<ellipse cx="{x}" cy="215" rx="24" ry="20" fill="{p.rad((0, "#fff0c0"), (0.4, "#d8a840"), (1, "#5a3c0e"), cx=0.35, cy=0.3)}"/>'
          f'<ellipse cx="{x - 7}" cy="207" rx="6" ry="4" fill="#fff" opacity="0.6"/><circle cx="{x}" cy="215" r="3" fill="#3a2a10"/>')
    p('<path d="M153 240 l0 20" stroke="#3a3a3a" stroke-width="3"/><circle cx="153" cy="240" r="5" fill="#2a2a2a"/>')
    for x in (100, 210):
        p(f'<circle cx="{x}" cy="320" r="9" fill="{p.rad((0, "#ffe0a0"), (1, "#7a5418"), cx=0.35, cy=0.3)}"/><circle cx="{x}" cy="320" r="3" fill="#3a2a10"/>')
    # manivela en el lateral
    p.vol("M280 236 L290 230 L344 248 L338 258 Z", p.lin((0, "#c8ccd2"), (1, "#3a3e44")), k=2, lo=0.3, gr=False)
    p(f'<ellipse cx="284" cy="240" rx="12" ry="16" fill="{p.rad((0, "#d8dce2"), (1, "#3a3e44"), cx=0.35, cy=0.3)}"/>'
      f'<path d="M336 252 L338 292 Q342 300 348 292 L346 250 Z" fill="{p.lin((0, "#2a1a10"), (0.4, "#6a4020"), (1, "#1a0e06"), x2=1, y2=0)}"/>'
      '<path d="M339 256 L340 290" stroke="#c89060" stroke-width="1.5" opacity="0.6"/>')
    # auricular de baquelita sobre la caja + cordón
    p('<path d="M96 132 C70 160 40 200 46 250 C50 300 30 330 56 352" stroke="#1a1410" stroke-width="5" fill="none"/>'
      '<path d="M95 130 C69 158 39 198 45 248 C49 298 29 328 55 350" stroke="#7a6a5a" stroke-width="1.2" fill="none" opacity="0.6"/>')
    au = ("M92 118 C88 100 104 92 120 96 L128 98 C150 96 220 90 248 92 L262 92 C280 90 292 100 288 116 "
          "C284 128 268 130 258 124 L248 112 C220 110 150 116 132 118 L124 128 C112 136 96 132 92 118 Z")
    p.sombra_d(au, 0.5, 4, 8)
    p.vol(au, p.lin((0, "#4a4440"), (0.4, "#1a1614"), (1, "#050404")), k=4, lo=0.0, ro=0.6)
    p('<path d="M106 104 C120 98 200 94 260 96" stroke="#fff4e0" stroke-width="3" fill="none" opacity="0.6" stroke-linecap="round"/>'
      '<ellipse cx="106" cy="110" rx="8" ry="4" fill="#fff" opacity="0.35"/><ellipse cx="268" cy="104" rx="8" ry="4" fill="#fff" opacity="0.35"/>')
    p.fin()


# ============================================================== 19. MESA
def mesa():
    p = P("mesa_campamento", 680, 560)
    r = random.Random(191)
    A, B, C, D = (60, 262), (560, 240), (628, 300), (112, 326)
    t = 12
    p.sombra(350, 528, 300, 20, 0.55)
    def tubo(a, b, w=8, c="#8a929c"):
        p(f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" stroke="#2a2e34" stroke-width="{w}" stroke-linecap="round"/>'
          f'<path d="M{a[0] - 1.5} {a[1]} L{b[0] - 1.5} {b[1]}" stroke="{c}" stroke-width="{w * 0.35:.1f}" stroke-linecap="round" opacity="0.8"/>')
    tubo((80, 272), (150, 516)); tubo((150, 276), (70, 512)); tubo((540, 254), (620, 500)); tubo((610, 256), (530, 506))
    tubo((120, 340), (190, 536), 9, "#c8d0d8"); tubo((190, 336), (114, 532), 9, "#c8d0d8")
    tubo((590, 318), (650, 520), 9, "#c8d0d8"); tubo((650, 314), (580, 524), 9, "#c8d0d8")
    tubo((152, 430), (614, 410), 6)
    p.vol(poly([D, C, dn(C, t), dn(D, t)]), p.lin((0, "#c8d0d8"), (1, "#4a5058")), k=2, lo=0.3, gr=False)
    p.vol(poly([A, D, dn(D, t), dn(A, t)]), "#5a616a", k=2, lo=0.2, gr=False)
    p.vol(poly([A, B, C, D]), p.lin((0, "#f0f2f4"), (0.5, "#a8b0ba"), (1, "#5a626c"), x2=1, y2=1), k=4, lo=0.3)
    for k in range(1, 8):
        a, b = lerp(A, D, k / 8), lerp(B, C, k / 8)
        p(f'<path d="M{F(a[0])} {F(a[1])} L{F(b[0])} {F(b[1])}" stroke="#4a525c" stroke-width="1.5" opacity="0.6"/>'
          f'<path d="M{F(a[0])} {F(a[1] + 1.5)} L{F(b[0])} {F(b[1] + 1.5)}" stroke="#fff" stroke-width="1" opacity="0.5"/>')
    p(f'<ellipse cx="200" cy="286" rx="150" ry="30" fill="{LUZ}" opacity="0.35" filter="url(#blur8)"/>')
    # libros apilados
    p('<g transform="translate(250 196) scale(0.42)">')
    _libro(p, ("#2b3f6b", "#5d79b0", "#111b36", "#c9b26a"), 40, 7)
    p('</g><g transform="translate(262 178) scale(0.38)">')
    _libro(p, ("#8c2f22", "#c8603f", "#45140c", "#d9a94e"), 46, 8)
    p("</g>")
    # taza esmaltada
    tx, ty = 500, 280
    p(f'<ellipse cx="{tx}" cy="{ty}" rx="30" ry="7" fill="#000" opacity="0.4" filter="url(#blur8)"/>')
    p(f'<path d="M{tx + 26} {ty - 46} C{tx + 50} {ty - 46} {tx + 50} {ty - 14} {tx + 24} {ty - 16}" stroke="#e8ecf0" stroke-width="7" fill="none"/>'
      f'<path d="M{tx + 26} {ty - 46} C{tx + 50} {ty - 46} {tx + 50} {ty - 14} {tx + 24} {ty - 16}" stroke="#2a4a8a" stroke-width="1.5" fill="none" opacity="0.5" transform="translate(1 2)"/>')
    mug = f"M{tx - 28} {ty - 56} L{tx - 28} {ty - 4} Q{tx} {ty + 8} {tx + 28} {ty - 4} L{tx + 28} {ty - 56} Z"
    p.vol(mug, p.lin((0, "#ffffff"), (0.5, "#dfe4ea"), (1, "#7a8490"), x2=1, y2=0), k=4, lo=0.3, ro=0.5)
    p(f'<ellipse cx="{tx}" cy="{ty - 56}" rx="28" ry="7" fill="#2a4a8a"/><ellipse cx="{tx}" cy="{ty - 55}" rx="24" ry="5" fill="#3a2010"/>'
      f'<path d="M{tx - 28} {ty - 4} Q{tx} {ty + 8} {tx + 28} {ty - 4}" stroke="#2a4a8a" stroke-width="3" fill="none"/>'
      f'<circle cx="{tx + 14}" cy="{ty - 30}" r="3" fill="#2a3a5a" opacity="0.6"/>')
    for k in range(3):
        x = tx - 10 + k * 10
        p(f'<path d="M{x} {ty - 64} C{x - 10} {ty - 84} {x + 10} {ty - 96} {x} {ty - 120}" stroke="#fff" stroke-width="4" fill="none" opacity="0.25" stroke-linecap="round" filter="url(#blur8)"/>')
    # farolillo
    _farol(p, 160, 120, 0.5)
    p.fin()


# ============================================================== 20-22. SUELO
def huellas():
    p = P("huellas", 380, 320)
    r = random.Random(201)
    p(f'<ellipse cx="190" cy="165" rx="185" ry="150" fill="{p.rad((0, "#9a7a5a", 0.75), (0.6, "#8a6446", 0.45), (1, "#6b4a32", 0))}"/>')
    for _ in range(160):
        a, rr = r.uniform(0, 6.28), r.uniform(0, 150)
        p(f'<circle cx="{F(190 + math.cos(a) * rr * 1.2)}" cy="{F(165 + math.sin(a) * rr * 0.95)}" r="{r.uniform(0.6, 2):.1f}" fill="{r.choice(("#c8a682", "#4a3220"))}" opacity="{r.uniform(0.2, 0.6):.2f}"/>')
    suela = "M0 -70 C26 -70 34 -50 32 -26 C30 -6 22 6 20 20 C18 34 26 50 22 64 C18 80 -18 80 -22 64 C-26 50 -18 32 -20 18 C-24 4 -34 -8 -32 -30 C-30 -56 -20 -70 0 -70 Z"
    for (x, y, ang) in ((132, 210, -10), (240, 118, 8)):
        p(f'<g transform="translate({x} {y}) scale(1.15 0.78) rotate({ang})">')
        p(f'<path d="{suela}" fill="#e0c4a0" opacity="0.6" transform="scale(1.12)"/>')
        p(f'<path d="{suela}" fill="{p.lin((0, "#2a1a10"), (0.5, "#4a3220"), (1, "#6b4a32"), x2=1, y2=1)}"/>')
        for yy in range(-60, 66, 13):
            if -6 < yy < 12:
                continue
            ww = 22 if yy < 0 else 15
            for xx in (-ww / 2, ww / 2):
                p(f'<path d="M{xx - 6:.1f} {yy} l6 -5 l6 5 l0 5 l-6 -4 l-6 4 Z" fill="#7a5a40"/>'
                  f'<path d="M{xx - 6:.1f} {yy + 5} l6 -4 l6 4" stroke="#c8a682" stroke-width="1" fill="none" opacity="0.6"/>')
        p(f'<path d="{suela}" fill="none" stroke="#1a0e08" stroke-width="3" opacity="0.6" clip-path="{p.clip("M-60 -90 L60 -90 L-60 90 Z")}"/>'
          f'<path d="{suela}" fill="none" stroke="#f0d8b8" stroke-width="2.5" opacity="0.6" transform="translate(1.5 1.5)" clip-path="{p.clip("M60 -90 L60 90 L-60 90 Z")}"/>')
        p("</g>")
    p.fin()


def mochila():
    p = P("mochila", 400, 600)
    r = random.Random(211)
    p.sombra(200, 566, 150, 14, 0.6)
    cuerpo = "M96 150 C90 120 120 110 200 108 C280 110 310 120 304 150 L318 520 C318 552 290 560 200 560 C110 560 82 552 82 520 Z"
    p.vol(cuerpo, p.lin((0, "#d8564a"), (0.4, "#a3312a"), (1, "#4a1210"), x2=1, y2=1), k=9, lo=0.35, ro=0.5)
    cl = p.clip(cuerpo)
    p(f'<g clip-path="{cl}">')
    p(f'<path d="M70 430 C140 420 260 420 330 430 L330 570 L70 570 Z" fill="{p.lin((0, "#4a5260"), (1, "#16181e"))}"/>')
    for _ in range(14):
        x, y = r.uniform(100, 300), r.uniform(160, 420)
        p(f'<path d="M{F(x)} {F(y)} q{r.uniform(-10, 10):.0f} {r.uniform(10, 30):.0f} {r.uniform(-20, 20):.0f} {r.uniform(20, 50):.0f}" stroke="#3a0a08" stroke-width="2.5" fill="none" opacity="0.35"/>')
    p("</g>")
    # bolsillo frontal de malla
    bol = "M130 300 C130 288 270 288 270 300 L276 430 C276 446 124 446 124 430 Z"
    p.vol(bol, p.lin((0, "#3a404a"), (1, "#121418")), k=5, lo=0.3, ro=0.4, gr=False)
    clb = p.clip(bol)
    p(f'<g clip-path="{clb}" opacity="0.35">' + "".join(f'<path d="M{x} 280 L{x + 60} 450 M{x + 60} 280 L{x} 450" stroke="#9aa0aa" stroke-width="1"/>' for x in range(80, 300, 10)) + "</g>")
    p('<path d="M128 302 C160 294 240 294 272 302" stroke="#1a1d22" stroke-width="7" fill="none"/>')
    # tapa superior
    tapa = "M86 170 C70 100 120 60 200 58 C280 60 330 100 314 170 C290 188 110 188 86 170 Z"
    p.sombra_d(tapa, 0.4, 0, 10)
    p.vol(tapa, p.lin((0, "#e0685a"), (0.5, "#a3312a"), (1, "#4a1210"), x2=1, y2=1), k=8, lo=0.4, ro=0.5)
    p('<path d="M104 160 C150 150 250 150 296 160" stroke="#2a0a08" stroke-width="2" fill="none" stroke-dasharray="6 4" opacity="0.6"/>'
      '<path d="M150 116 C180 106 220 106 250 116" stroke="#1a1d22" stroke-width="5" fill="none"/><circle cx="252" cy="118" r="4" fill="#c8ccd2"/>'
      '<path d="M190 58 C190 40 210 40 210 58" stroke="#1a1d22" stroke-width="6" fill="none"/>')
    # correas
    for x in (150, 250):
        p(f'<path d="M{x} 176 L{x + (x - 200) * 0.08} 290" stroke="#16181c" stroke-width="12"/>'
          f'<path d="M{x - 3} 176 L{x - 3 + (x - 200) * 0.08} 290" stroke="#5a616a" stroke-width="2" opacity="0.6"/>'
          f'<rect x="{x - 10 + (x - 200) * 0.05:.0f}" y="230" width="20" height="16" rx="3" fill="#2a2e34" stroke="#7a828c" stroke-width="1.5"/>')
    for y in (250, 380):
        p(f'<path d="M84 {y} C140 {y + 8} 260 {y + 8} 316 {y}" stroke="#16181c" stroke-width="9" fill="none"/>'
          f'<path d="M84 {y - 3} C140 {y + 5} 260 {y + 5} 316 {y - 3}" stroke="#6a727c" stroke-width="1.5" fill="none" opacity="0.6"/>'
          f'<rect x="92" y="{y - 9}" width="18" height="18" rx="3" fill="#2a2e34" stroke="#8a929c" stroke-width="1.5"/>'
          f'<rect x="290" y="{y - 9}" width="18" height="18" rx="3" fill="#2a2e34" stroke="#8a929c" stroke-width="1.5"/>')
    # cinturón lumbar asomando
    for sg in (-1, 1):
        x = 200 + sg * 118
        p.vol(f"M{x} 470 C{x + sg * 30} 468 {x + sg * 38} 490 {x + sg * 34} 512 L{x} 520 Z", p.lin((0, "#4a5260"), (1, "#16181e")), k=3, lo=0.3, gr=False)
    p.fin()


def charco():
    p = P("charco", 620, 220)
    r = random.Random(221)
    borde = "M30 112 C40 60 160 40 300 44 C460 40 600 66 596 116 C592 162 470 186 310 182 C150 186 22 160 30 112 Z"
    p(f'<path d="{borde}" fill="#1a120d" opacity="0.7" transform="translate(310 112) scale(1.06 1.18) translate(-310 -112)" filter="url(#blur8)"/>')
    agua = "M48 112 C56 70 170 56 300 58 C450 56 580 76 576 114 C572 152 460 170 310 168 C160 170 42 150 48 112 Z"
    p(f'<path d="{agua}" fill="{p.lin((0, "#2a3446"), (0.5, "#0d1118"), (1, "#07090f"))}"/>')
    cl = p.clip(agua)
    p(f'<g clip-path="{cl}">')
    p(f'<ellipse cx="250" cy="110" rx="60" ry="48" fill="{p.rad((0, "#fff0c8", 0.9), (0.3, LUZ, 0.6), (1, LUZ2, 0))}"/>'
      f'<rect x="238" y="58" width="24" height="110" fill="{p.lin((0, LUZ, 0.0), (0.5, "#fff0c8", 0.55), (1, LUZ, 0.0))}"/>')
    for k in range(5):
        p(f'<ellipse cx="250" cy="110" rx="{80 + k * 50}" ry="{18 + k * 10}" fill="none" stroke="#a9b8cc" stroke-width="1" opacity="{0.25 - k * 0.04:.2f}"/>')
    for _ in range(8):
        x, y = r.uniform(80, 540), r.uniform(80, 150)
        p(f'<path d="M{F(x)} {F(y)} l{r.uniform(20, 60):.0f} 0" stroke="{LUZ}" stroke-width="1.5" opacity="0.3"/>')
    p("</g>")
    p(f'<path d="M60 96 C100 66 200 58 300 60" stroke="#fff" stroke-width="2" fill="none" opacity="0.4"/>'
      f'<path d="{agua}" fill="none" stroke="#3d2a1f" stroke-width="3" opacity="0.8"/>')
    p.fin()


# ============================================================== 23-24. ROCAS Y MOHO
def _roca(p, pts, sem, luz=0.5):
    r = random.Random(sem)
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    p.vol(d, p.lin((0, "#3d2a1f"), (0.35, "#22170f"), (1, "#07090f"), x2=0.6, y2=1), k=6, lo=luz, ro=0.35)
    cl = p.clip(d)
    xs = [x for x, _ in pts]; ys = [y for _, y in pts]
    p(f'<g clip-path="{cl}">')
    for _ in range(int((max(xs) - min(xs)) / 40)):  # facetas
        x, y = r.uniform(min(xs), max(xs)), r.uniform(min(ys), max(ys))
        s = r.uniform(30, 90)
        q = [(x + r.uniform(-s, s), y + r.uniform(-s, s)) for _ in range(3)]
        p(f'<path d="{poly(q)}" fill="{r.choice(("#000", "#6b4a32", "#141b29"))}" opacity="{r.uniform(0.12, 0.3):.2f}"/>')
    for _ in range(int((max(xs) - min(xs)) / 70)):  # grietas
        x, y = r.uniform(min(xs), max(xs)), r.uniform(min(ys), max(ys))
        seg = " ".join(f"l{r.uniform(-20, 20):.0f} {r.uniform(10, 30):.0f}" for _ in range(4))
        p(f'<path d="M{F(x)} {F(y)} {seg}" stroke="#05060a" stroke-width="{r.uniform(1.5, 3):.1f}" fill="none" opacity="0.8"/>'
          f'<path d="M{F(x + 2)} {F(y)} {seg}" stroke="#8a6446" stroke-width="0.8" fill="none" opacity="0.4"/>')
    for _ in range(int((max(xs) - min(xs)) / 12)):
        x, y = r.uniform(min(xs), max(xs)), r.uniform(min(ys), max(ys))
        p(f'<circle cx="{F(x)}" cy="{F(y)}" r="{r.uniform(0.6, 1.6):.1f}" fill="{r.choice(("#fff", "#8a6446"))}" opacity="{r.uniform(0.2, 0.7):.2f}"/>')
    p("</g>")
    arr = pts[1:-1]
    p(f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in arr)}" stroke="{LUZ2}" stroke-width="2.5" fill="none" opacity="{luz * 0.55:.2f}" stroke-linejoin="round" clip-path="{cl}"/>')
    return d


def _perfil(x0, x1, ybase, alturas, sem):
    r = random.Random(sem)
    n = len(alturas)
    pts = [(x0, ybase + 30)]
    for i, h in enumerate(alturas):
        x = x0 + (x1 - x0) * i / (n - 1)
        pts.append((x + r.uniform(-8, 8), ybase - h + r.uniform(-6, 6)))
    pts.append((x1, ybase + 30))
    return pts


def rocas():
    for n, conj, sem in (("rocas_primer_plano_a", (((-20, 520, 500, (60, 220, 330, 380, 360, 300, 240, 160, 90, 40)), 0.5),
                                                   ((880, 1420, 500, (40, 120, 220, 300, 350, 410, 440, 420, 400)), 0.5),
                                                   ((380, 1000, 500, (10, 50, 90, 110, 100, 120, 90, 60, 20)), 0.35)), 1),
                         ("rocas_primer_plano_b", (((900, 1420, 500, (60, 200, 330, 420, 460, 470, 440, 420, 400, 380)), 0.5),
                                                   ((-20, 560, 500, (180, 200, 170, 140, 150, 110, 90, 60, 30)), 0.45),
                                                   ((480, 1000, 500, (20, 60, 70, 100, 140, 120, 80, 40)), 0.35)), 2)):
        p = P(n, 1400, 500)
        for i, ((x0, x1, yb, alt), luz) in enumerate(conj):
            pts = _perfil(x0, x1, yb, alt, sem * 10 + i)
            _roca(p, pts, sem * 10 + i, luz)
        r = random.Random(sem)
        for _ in range(18):  # guijarros delante
            x, y, s = r.uniform(0, 1400), r.uniform(470, 500), r.uniform(10, 30)
            d = f"M{F(x - s)} {F(y)} Q{F(x - s * 0.8)} {F(y - s * 0.8)} {F(x)} {F(y - s * 0.7)} Q{F(x + s)} {F(y - s * 0.6)} {F(x + s)} {F(y)} Z"
            p(f'<path d="{d}" fill="{p.lin((0, "#4a3426"), (1, "#07090f"), x2=1, y2=1)}"/>'
              f'<path d="M{F(x - s * 0.7)} {F(y - s * 0.5)} Q{F(x - s * 0.2)} {F(y - s * 0.75)} {F(x + s * 0.4)} {F(y - s * 0.6)}" stroke="{LUZ}" stroke-width="1.5" fill="none" opacity="0.35"/>')
        p('<rect x="0" y="488" width="1400" height="12" fill="#07090f"/>')
        p.fin()


def moho():
    p = P("moho_pared", 600, 500)
    f = p.filtro('<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="4" seed="17" result="t"/>'
                 '<feColorMatrix in="t" type="matrix" values="0 0 0 0 0.16  0 0 0 0 0.2  0 0 0 0 0.1  2.8 0 0 0 -1.25" result="m"/>'
                 '<feComposite in="m" in2="SourceGraphic" operator="in"/>', "0", "0", "100%", "100%")
    i = p.nid("mk")
    p.d.append(f'<mask id="{i}"><ellipse cx="300" cy="230" rx="280" ry="220" fill="{p.rad((0, "#fff", 1), (0.6, "#fff", 0.7), (1, "#fff", 0))}"/></mask>')
    p(f'<g mask="url(#{i})"><rect width="600" height="500" fill="#000" filter="{f}" opacity="0.85"/>'
      f'<ellipse cx="300" cy="220" rx="200" ry="150" fill="#1e2410" opacity="0.25" filter="url(#blur20)"/></g>')
    r = random.Random(241)
    for _ in range(9):  # chorretones
        x = r.uniform(150, 450); y0 = r.uniform(200, 300); L = r.uniform(80, 180)
        p(f'<path d="M{F(x)} {F(y0)} q{r.uniform(-4, 4):.1f} {F(L / 2)} {r.uniform(-6, 6):.1f} {F(L)}" stroke="#1a1e12" stroke-width="{r.uniform(3, 8):.1f}" '
          f'opacity="0.3" stroke-linecap="round" fill="none" filter="url(#blur8)"/>')
    for _ in range(40):
        x, y = r.gauss(300, 90), r.gauss(220, 70)
        p(f'<circle cx="{F(x)}" cy="{F(y)}" r="{r.uniform(1, 4):.1f}" fill="{r.choice(("#3a4a1e", "#4a5a2a", "#1a1e10"))}" opacity="{r.uniform(0.2, 0.5):.2f}"/>')
    p.fin()


# ============================================================== registro
def generar(dirsvg, sombra=True):
    global SOMBRA
    SOMBRA = sombra
    ilus.OUT = dirsvg
    HECHAS.clear()
    for f in PIEZAS:
        f()
    return list(HECHAS)


PIEZAS = [libros, libro_abierto, velas, marcas, lana, garrafa, botella, caja_comida, bolsa_basura, camara, lampara, haz,
          colchon, cuaderno, estalactitas, murcielago, mosca, cuerda, tienda_campana, tienda_1962, telefono, mesa, huellas,
          mochila, charco, rocas, moho]

if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg", "--sin-sombra" not in sys.argv))
