"""Objetos del mundo de arriba, del cerebro y de los recuerdos — vídeo largo «500 días en una cueva».

Uso:  from lotes... import ilus_objetos_mundo; ilus_objetos_mundo.generar(DIR_SVG)  → lista de nombres
      python3 lotes/largo-cueva-500-dias/generadores/ilus_objetos_mundo.py DIR_SVG

Todas las piezas: fondo transparente, lienzo ajustado, luz principal arriba a la izquierda, luz de borde
del lado contrario, grano sutil y sombra de contacto opcional (parámetro `sombra`, global SOMBRA).
Prefijo de ids propio: «om».
"""
import math, os, random, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano  # noqa: E402

SOMBRA = True  # sombra de contacto en las piezas que se posan en el suelo
NOMBRES = []


def _g(nombre, cuerpo, w, h, defs=""):
    guardar(nombre, cuerpo, w, h, defs)
    NOMBRES.append(nombre)


# ------------------------------------------------------------------ ayudantes
def _sc(cx, cy, rx, ry, op=0.4, sombra=None):
    """Sombra de contacto suave."""
    if sombra is None:
        sombra = SOMBRA
    if not sombra:
        return ""
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#000" opacity="{op}" filter="url(#blur8)"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*0.55:.0f}" ry="{ry*0.5:.0f}" fill="#000" opacity="{op*0.6:.2f}"/>')


def _gr(clip, w, h, op=1.0):
    """Grano recortado a un clipPath."""
    return f'<g clip-path="url(#{clip})" opacity="{op}"><rect width="{w}" height="{h}" fill="#888" filter="url(#grano)"/></g>'


def _clip(id_, *paths):
    return f'<clipPath id="{id_}">' + "".join(p if p.startswith("<") else f'<path d="{p}"/>' for p in paths) + '</clipPath>'


def _lgu(id_, x1, y1, x2, y2, *stops):
    """Degradado lineal en coordenadas de usuario; stops: (offset, color) o (offset, color, alfa)."""
    s = "".join(f'<stop offset="{st[0]}" stop-color="{st[1]}" stop-opacity="{st[2] if len(st) > 2 else 1}"/>' for st in stops)
    return f'<linearGradient id="{id_}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def _rgu(id_, cx, cy, r, *stops, fx=None, fy=None):
    s = "".join(f'<stop offset="{st[0]}" stop-color="{st[1]}" stop-opacity="{st[2] if len(st) > 2 else 1}"/>' for st in stops)
    f = f' fx="{fx}" fy="{fy}"' if fx is not None else ""
    return f'<radialGradient id="{id_}" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" r="{r}"{f}>{s}</radialGradient>'


def _suave(pts, cerrado=False):
    """Curva suave (cuadráticas por puntos medios) a partir de puntos."""
    if len(pts) < 3:
        return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    if cerrado:
        pts = pts + pts[:2]
        m = ((pts[0][0] + pts[1][0]) / 2, (pts[0][1] + pts[1][1]) / 2)
        d = f"M{m[0]:.1f} {m[1]:.1f}"
        for i in range(1, len(pts) - 1):
            m2 = ((pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2)
            d += f" Q{pts[i][0]:.1f} {pts[i][1]:.1f} {m2[0]:.1f} {m2[1]:.1f}"
        return d + " Z"
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(1, len(pts) - 1):
        m2 = ((pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2)
        d += f" Q{pts[i][0]:.1f} {pts[i][1]:.1f} {m2[0]:.1f} {m2[1]:.1f}"
    return d + f" L{pts[-1][0]:.1f} {pts[-1][1]:.1f}"


def _vetas(r, x0, y0, x1, y1, n, col, op=0.25, ondas=3, sw=1.6):
    """Vetas de madera horizontales."""
    out = []
    for i in range(n):
        y = y0 + (y1 - y0) * (i + r.random()) / n
        pts = [(x0 + (x1 - x0) * k / 8, y + math.sin(k * ondas / 8 * math.pi + r.uniform(0, 6)) * r.uniform(1, 5)) for k in range(9)]
        out.append(f'<path d="{_suave(pts)}" stroke="{col}" stroke-width="{r.uniform(sw*0.5, sw*1.4):.1f}" opacity="{r.uniform(op*0.5, op):.2f}" fill="none"/>')
    return "".join(out)


def _estrella(cx, cy, R, r_, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        a = math.radians(rot + i * 180 / n)
        rr = R if i % 2 == 0 else r_
        pts.append(f"{cx + math.cos(a)*rr:.1f},{cy + math.sin(a)*rr:.1f}")
    return " ".join(pts)


def _destello_peq(x, y, L, col="#ffffff", op=0.9):
    return (f'<circle cx="{x}" cy="{y}" r="{L*0.5:.1f}" fill="{col}" opacity="{op*0.25:.2f}"/>'
            f'<path d="M{x-L} {y} Q{x} {y} {x} {y-L} Q{x} {y} {x+L} {y} Q{x} {y} {x} {y+L} Q{x} {y} {x-L} {y} Z" fill="{col}" opacity="{op}"/>')


# ================================================================== CEREBRO
_CER = ("M140 330 C92 282 100 180 188 118 C270 60 410 44 522 68 C624 90 702 160 714 250 C722 312 702 360 662 386 "
        "C632 402 602 400 576 396 C540 412 500 426 450 432 C390 438 330 432 290 412 C256 396 236 372 230 346 "
        "C212 354 182 354 162 346 C152 342 145 337 140 330 Z")
_CBL = ("M488 400 C530 366 620 352 676 372 C706 386 712 430 684 456 C640 490 560 492 516 470 C486 454 476 424 488 400 Z")
_TRONCO = "M410 404 C452 418 486 440 494 476 C500 504 492 530 486 552 L440 552 C446 522 444 498 432 476 C420 456 400 440 384 426 Z"


def _cerebro(nombre, brillo=False):
    w, h = 800, 560
    r = random.Random(101)
    d = (_rgu("omcb_c", 300, 150, 560, ("0", "#ffe1e8"), ("0.35", "#f4a3b8"), ("0.75", "#d0688a"), ("1", "#8e3a5c")) +
         _rgu("omcb_cb", 570, 400, 160, ("0", "#f0a0b6"), ("0.6", "#c85a7e"), ("1", "#7a2c4c")) +
         _lgu("omcb_tr", 440, 0, 500, 0, ("0", "#8e3a5c"), ("0.5", "#d77d98"), ("1", "#6a2440")) +
         _lgu("omcb_rim", 360, 120, 720, 470, ("0", "#2ff3ff", 0), ("0.6", "#2ff3ff", 0.15), ("1", "#2ff3ff", 1)) +
         _lgu("omcb_sh", 0, 60, 0, 440, ("0", "#000", 0), ("0.6", "#3a0a24", 0.0), ("1", "#3a0a24", 0.55)) +
         _clip("omcb_clip", _CER) + _clip("omcb_clipb", _CBL) +
         '<filter id="omcb_gy" filterUnits="userSpaceOnUse" x="90" y="30" width="640" height="420" color-interpolation-filters="sRGB">'
         '<feTurbulence type="fractalNoise" baseFrequency="0.0105 0.013" numOctaves="2" seed="8" result="n"/>'
         '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1.25 0 0 0 -0.12" result="a"/>'
         '<feComponentTransfer in="a" result="h0"><feFuncA type="table" tableValues="0 1 0 1 0 1 0 1 0 1 0"/></feComponentTransfer>'
         '<feComponentTransfer in="h0" result="h1"><feFuncA type="gamma" amplitude="1" exponent="0.55" offset="0"/></feComponentTransfer>'
         '<feGaussianBlur in="h1" stdDeviation="1.6" result="h"/>'
         '<feDiffuseLighting in="h" surfaceScale="5" diffuseConstant="1.3" lighting-color="#ff9cba" result="dif">'
         '<feDistantLight azimuth="225" elevation="48"/></feDiffuseLighting>'
         '<feSpecularLighting in="h" surfaceScale="5" specularConstant="0.45" specularExponent="18" lighting-color="#fff2f6" result="esp">'
         '<feDistantLight azimuth="225" elevation="48"/></feSpecularLighting>'
         '<feComposite in="esp" in2="dif" operator="arithmetic" k1="0" k2="1" k3="1" k4="0"/></filter>')
    b = []
    if brillo:
        b.append('<ellipse cx="410" cy="260" rx="340" ry="230" fill="#ff3df2" opacity="0.22" filter="url(#blur40)"/>')
    b.append(f'<path d="{_TRONCO}" fill="url(#omcb_tr)"/>')
    b.append(f'<path d="M470 470 C480 480 486 500 486 520" stroke="#5a1a34" stroke-width="3" opacity="0.4" fill="none"/>')
    # cerebelo con láminas finas
    b.append(f'<path d="{_CBL}" fill="url(#omcb_cb)"/><g clip-path="url(#omcb_clipb)">')
    for i in range(18):
        yy = 372 + i * 6.5
        b.append(f'<path d="M470 {yy+14:.0f} C540 {yy-6:.0f} 640 {yy-10:.0f} 716 {yy+8:.0f}" stroke="#7a2848" stroke-width="2.4" opacity="0.6" fill="none"/>'
                 f'<path d="M470 {yy+12:.0f} C540 {yy-8:.0f} 640 {yy-12:.0f} 716 {yy+6:.0f}" stroke="#ffd0dc" stroke-width="1.3" opacity="0.4" fill="none"/>')
    b.append(_gr("omcb_clipb", w, h) + '</g>')
    b.append(f'<path d="{_CBL}" fill="none" stroke="#2ff3ff" stroke-width="3" opacity="0.55" stroke-dasharray="0 150 300 999"/>')
    # cerebro
    b.append(f'<path d="{_CER}" fill="url(#omcb_c)"/><g clip-path="url(#omcb_clip)">')
    # surcos: caminos aleatorios suaves
    surcos, luces = [], []
    xs = list(range(100, 730, 44))
    ys = list(range(50, 440, 40))
    hondo = []
    for gx in xs:
        for gy in ys:
            x, y = gx + r.uniform(-16, 16), gy + r.uniform(-14, 14)
            # orientación general: rodeando el centro del cerebro (como los giros reales)
            hd = math.atan2(y - 250, x - 420) + math.pi / 2 + r.uniform(-0.7, 0.7)
            tr = 0
            pts = [(x, y)]
            for _ in range(r.randint(4, 7)):
                tr = tr * 0.6 + r.uniform(-0.55, 0.55)
                hd += tr
                x += math.cos(hd) * 14
                y += math.sin(hd) * 14
                pts.append((x, y))
                if r.random() < 0.18:  # rama corta
                    a2 = hd + r.choice((-1, 1)) * r.uniform(1.0, 1.6)
                    q = [(x, y), (x + math.cos(a2) * 14, y + math.sin(a2) * 14), (x + math.cos(a2 + 0.3) * 24, y + math.sin(a2 + 0.3) * 24)]
                    pb = _suave(q)
                    hondo.append(f'<path d="{pb}" stroke="#7a2a4c" stroke-width="10" stroke-linecap="round" fill="none" opacity="0.16"/>')
                    surcos.append(f'<path d="{pb}" stroke="#8a2e56" stroke-width="3" stroke-linecap="round" fill="none" opacity="0.85"/>')
                    luces.append(f'<path d="{pb}" transform="translate(-4 -4)" stroke="#ffe8ef" stroke-width="4" stroke-linecap="round" fill="none" opacity="0.35"/>')
            p = _suave(pts)
            hondo.append(f'<path d="{p}" stroke="#7a2a4c" stroke-width="12" stroke-linecap="round" fill="none" opacity="0.16"/>')
            surcos.append(f'<path d="{p}" stroke="#8a2e56" stroke-width="{r.uniform(3, 4.2):.1f}" stroke-linecap="round" fill="none" opacity="0.9"/>')
            luces.append(f'<path d="{p}" transform="translate(-5 -5)" stroke="#ffe8ef" stroke-width="5" stroke-linecap="round" fill="none" opacity="0.35"/>')
    b.append(f'<rect x="90" y="30" width="640" height="420" filter="url(#omcb_gy)" opacity="0.82"/>')
    b.append(f'<rect width="{w}" height="{h}" fill="#ff6f9a" opacity="0.16"/>')
    # cisuras grandes: lateral (Silvio) y central (Rolando)
    for p, sw in (("M236 334 C300 300 384 290 470 272 C504 264 524 250 540 232", 11),
                  ("M444 52 C426 108 448 150 422 192 C404 224 416 252 400 282", 8),
                  ("M610 106 C600 150 630 190 612 240", 6)):
        b.append(f'<path d="{p}" transform="translate(-4 -4)" stroke="#ffe4ec" stroke-width="{sw*0.5}" opacity="0.45" fill="none" stroke-linecap="round"/>'
                 f'<path d="{p}" stroke="#6e2244" stroke-width="{sw}" fill="none" stroke-linecap="round"/>')
    b.append(f'<rect width="{w}" height="{h}" fill="url(#omcb_sh)"/>')
    b.append(f'<path d="{_CER}" fill="none" stroke="#5a1634" stroke-width="26" opacity="0.28" filter="url(#blur8)"/>')
    b.append(_gr("omcb_clip", w, h))
    b.append(f'<rect width="{w}" height="{h}" fill="url(#omcb_rim)" opacity="0.28"/>')
    if brillo:
        rr = random.Random(5)
        pts = []
        while len(pts) < 46:
            x, y = rr.uniform(150, 700), rr.uniform(80, 420)
            # dentro aproximado (elipse del cerebro)
            if ((x - 420) / 300) ** 2 + ((y - 245) / 185) ** 2 < 1:
                pts.append((x, y))
        d += (rg("omcb_hc", (0, "#ffffff", 1), (0.25, "#9ffcff", 0.9), (1, "#2ff3ff", 0)) +
              rg("omcb_hm", (0, "#ffffff", 1), (0.25, "#ffb0f8", 0.9), (1, "#ff3df2", 0)))
        for (cx, cy, rad, c) in ((260, 200, 110, "#2ff3ff"), (520, 170, 100, "#ff3df2"), (420, 330, 80, "#2ff3ff"), (640, 300, 70, "#ff3df2")):
            b.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="{c}" opacity="0.24" filter="url(#blur20)"/>')
        for i, (x, y) in enumerate(pts):
            for (x2, y2) in pts[i + 1:]:
                dd = math.hypot(x2 - x, y2 - y)
                if dd < 85:
                    mx, my = (x + x2) / 2 + rr.uniform(-12, 12), (y + y2) / 2 + rr.uniform(-12, 12)
                    b.append(f'<path d="M{x:.0f} {y:.0f} Q{mx:.0f} {my:.0f} {x2:.0f} {y2:.0f}" stroke="#bffcff" stroke-width="1.6" opacity="0.6" fill="none"/>')
        for i, (x, y) in enumerate(pts):
            hal = "omcb_hc" if i % 3 else "omcb_hm"
            s = rr.uniform(14, 30)
            b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s:.0f}" fill="url(#{hal})"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{s*0.16:.1f}" fill="#ffffff"/>')
    b.append('</g>')
    # luz de borde cian en la nuca y abajo
    b.append(f'<path d="M560 70 C640 96 706 160 714 250 C722 312 702 360 662 386" stroke="#2ff3ff" stroke-width="7" opacity="0.55" fill="none" filter="url(#blur8)"/>'
             f'<path d="M580 78 C648 106 706 166 714 250 C722 312 702 360 662 386" stroke="#bffcff" stroke-width="2.5" opacity="0.8" fill="none"/>'
             f'<path d="M290 412 C330 432 390 438 450 432" stroke="#2ff3ff" stroke-width="3" opacity="0.5" fill="none"/>')
    if brillo:
        for k in range(10):
            x, y = r.uniform(140, 720), r.uniform(40, 460)
            b.append(_destello_peq(round(x), round(y), r.uniform(6, 12), "#e8feff", 0.8))
    _g(nombre, "".join(b), w, h, d)


# ================================================================== RECUERDOS (fotos instantáneas)
PW, PH = 600, 700
PX, PY, PS = 58, 50, 484  # foto: esquina y lado


def _polaroid(nombre, escena, defs_esc="", gris=False):
    d = (lg("ompf", (0, "#fdfbf6"), (0.6, "#f4efe4"), (1, "#e6dfcf"), x2=1, y2=1) +
         lg("ompg", (0, "#ffffff"), (0.45, "#ffffff00"), x2=1, y2=1) +
         rg("ompv", (0, "#000", 0), (0.6, "#000", 0), (1, "#000", 0.28), r=0.72) +
         f'<clipPath id="ompc"><rect width="{PS}" height="{PS}"/></clipPath>' +
         '<clipPath id="ompm"><rect x="30" y="22" width="540" height="640" rx="6"/></clipPath>' + defs_esc)
    b = ['<g filter="url(#sombra)"><rect x="30" y="22" width="540" height="640" rx="6" fill="url(#ompf)"/></g>',
         '<g clip-path="url(#ompm)"><rect width="600" height="700" fill="#fff" filter="url(#papel)" opacity="0.18"/>',
         _gr("ompm", 600, 700, 0.6), '</g>',
         '<path d="M32 660 L568 660" stroke="#c9bfa8" stroke-width="2" opacity="0.6"/>',
         '<path d="M32 24 L568 24" stroke="#ffffff" stroke-width="2" opacity="0.9"/>',
         f'<g transform="translate({PX} {PY})"><g clip-path="url(#ompc)">', escena]
    if gris:
        b.append(f'<rect width="{PS}" height="{PS}" fill="#8a8c90" opacity="0.10"/>')
    else:
        b.append(f'<rect width="{PS}" height="{PS}" fill="#ffb060" opacity="0.08"/>')
    b += [f'<rect width="{PS}" height="{PS}" fill="url(#ompv)"/>',
          f'<rect width="{PS}" height="{PS}" fill="#888" filter="url(#grano)"/>',
          f'<rect width="{PS}" height="{PS}" fill="url(#ompg)" opacity="0.16"/>',
          '</g>',
          f'<rect width="{PS}" height="{PS}" fill="none" stroke="#000" stroke-opacity="0.18" stroke-width="2"/></g>']
    _g(nombre, "".join(b), PW, PH, d)


def _nubes(r, n, y0, y1, s=1.0, col="#ffffff", op=0.9):
    out = []
    for _ in range(n):
        x, y = r.uniform(-20, PS + 20), r.uniform(y0, y1)
        k = r.uniform(0.7, 1.3) * s
        out.append(f'<g opacity="{op}"><ellipse cx="{x:.0f}" cy="{y+6*k:.0f}" rx="{60*k:.0f}" ry="{12*k:.0f}" fill="{col}"/>'
                   f'<circle cx="{x-24*k:.0f}" cy="{y:.0f}" r="{16*k:.0f}" fill="{col}"/><circle cx="{x+4*k:.0f}" cy="{y-8*k:.0f}" r="{22*k:.0f}" fill="{col}"/>'
                   f'<circle cx="{x+30*k:.0f}" cy="{y+2*k:.0f}" r="{14*k:.0f}" fill="{col}"/>'
                   f'<ellipse cx="{x:.0f}" cy="{y+12*k:.0f}" rx="{56*k:.0f}" ry="{6*k:.0f}" fill="#9fb8d0" opacity="0.35"/></g>')
    return "".join(out)


def _esc_playa():
    r = random.Random(1)
    d = (lg("om1s", (0, "#4fb0e8"), (1, "#c8ecfa")) + lg("om1m", (0, "#2a9fd0"), (1, "#5fd0e0")) +
         lg("om1a", (0, "#f6dfa8"), (1, "#e0b46e")) + rg("om1h", (0, "#fff6c8", 1), (1, "#fff6c8", 0)))
    b = [f'<rect width="{PS}" height="250" fill="url(#om1s)"/>',
         '<circle cx="390" cy="72" r="90" fill="url(#om1h)"/><circle cx="390" cy="72" r="30" fill="#fff8d8"/>',
         _nubes(r, 3, 40, 150, 0.9),
         f'<rect y="228" width="{PS}" height="110" fill="url(#om1m)"/>',
         '<path d="M0 230 L484 230" stroke="#e8fbff" stroke-width="2" opacity="0.7"/>']
    for i in range(16):
        y = r.uniform(240, 320)
        x = r.uniform(-20, 470)
        b.append(f'<path d="M{x:.0f} {y:.0f} q{12:.0f} -4 {24} 0 q12 4 24 0" stroke="#ffffff" stroke-width="2" opacity="0.5" fill="none"/>')
    b += ['<path d="M0 330 C60 316 120 340 200 324 C280 310 360 336 484 318 L484 484 L0 484 Z" fill="url(#om1a)"/>',
          '<path d="M0 330 C60 316 120 340 200 324 C280 310 360 336 484 318" stroke="#ffffff" stroke-width="7" opacity="0.85" fill="none"/>',
          '<path d="M0 340 C70 328 130 348 210 334 C290 322 370 344 484 330" stroke="#c8a060" stroke-width="3" opacity="0.4" fill="none"/>']
    for _ in range(60):
        b.append(f'<circle cx="{r.uniform(0,484):.0f}" cy="{r.uniform(345,484):.0f}" r="{r.uniform(0.8,2):.1f}" fill="#a5793e" opacity="0.4"/>')
    # sombra de la sombrilla y toalla
    b += ['<ellipse cx="250" cy="430" rx="150" ry="26" fill="#a5743a" opacity="0.35"/>',
          '<path d="M190 400 L330 392 L360 452 L210 462 Z" fill="#3a8fd8"/>',
          '<path d="M200 418 L338 409 L346 426 L206 436 Z" fill="#ffd34a"/><path d="M206 440 L350 431 L355 442 L210 452 Z" fill="#ffffff" opacity="0.85"/>',
          '<path d="M190 400 L330 392" stroke="#ffffff" stroke-width="2" opacity="0.5"/>',
          # palo
          '<path d="M228 440 L258 196" stroke="#f2f2f2" stroke-width="7" stroke-linecap="round"/>',
          '<path d="M226 440 L256 196" stroke="#8a8a8a" stroke-width="2" opacity="0.5"/>']
    # lona de la sombrilla: cúpula en gajos (vista algo por debajo)
    cx, cy = 258, 190
    ax, ay = cx, cy - 56
    gajos = 8
    edge = [(cx + math.cos(math.pi - math.pi * k / gajos) * 168, cy + 18 + math.sin(math.pi - math.pi * k / gajos) * 30) for k in range(gajos + 1)]
    def ctrl(x, y):
        return (ax + x) / 2 + (x - ax) * 0.28, (ay + y) / 2 - 22 + abs(x - ax) * 0.02
    for i in range(gajos):
        (x0, y0), (x1, y1) = edge[i], edge[i + 1]
        c0, c1 = ctrl(x0, y0), ctrl(x1, y1)
        col = "#e8483b" if i % 2 == 0 else "#fff4e6"
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + 12
        b.append(f'<path d="M{ax} {ay} Q{c0[0]:.0f} {c0[1]:.0f} {x0:.0f} {y0:.0f} Q{mx:.0f} {my:.0f} {x1:.0f} {y1:.0f} Q{c1[0]:.0f} {c1[1]:.0f} {ax} {ay} Z" fill="{col}"/>')
    b.append(f'<path d="M{ax} {ay} Q{cx+60} {ay+20} {cx+168} {cy+18} Q{cx+120} {cy+60} {cx+60} {cy+46} Q{cx+40} {ay+40} {ax} {ay} Z" fill="#000" opacity="0.13"/>')
    b += [f'<path d="M{ax} {ay} Q{cx-110} {ay+4} {cx-166} {cy+16}" stroke="#ffffff" stroke-width="3" opacity="0.6" fill="none"/>',
          f'<circle cx="{ax}" cy="{ay-2}" r="6" fill="#f4f4f4"/>',
          # cubo y balón
          '<path d="M380 410 L410 410 L405 446 L385 446 Z" fill="#ff8a2a"/><path d="M380 410 Q395 392 410 410" stroke="#ff8a2a" stroke-width="3" fill="none"/>',
          '<circle cx="130" cy="430" r="22" fill="#ffffff"/><path d="M108 430 A22 22 0 0 1 130 408 L130 430 Z" fill="#e8483b"/><path d="M130 452 A22 22 0 0 1 108 430 L130 430 Z" fill="#3a8fd8"/>'
          '<path d="M152 430 A22 22 0 0 1 130 452 L130 430 Z" fill="#ffd34a"/><circle cx="122" cy="420" r="6" fill="#ffffff" opacity="0.7"/>',
          '<ellipse cx="134" cy="455" rx="20" ry="4" fill="#8a5a2a" opacity="0.35"/>']
    return "".join(b), d


def _esc_tarta():
    r = random.Random(2)
    d = (lg("om2s", (0, "#4a1e3a"), (1, "#b2544a")) + lg("om2t", (0, "#f8e8d0"), (1, "#d8bfa0")) +
         lg("om2c", (0, "#f7a7c0"), (0.5, "#fbc2d4"), (1, "#d26f92"), x2=1, y2=0) +
         lg("om2k", (0, "#f9d2a8"), (0.5, "#fde6c8"), (1, "#c99668"), x2=1, y2=0) +
         rg("om2b", (0, "#ffd890", 0.9), (1, "#ffd890", 0)) + rg("om2f", (0, "#fffbe0", 1), (0.3, "#ffd24a", 0.9), (1, "#ff8a1a", 0)))
    b = [f'<rect width="{PS}" height="{PS}" fill="url(#om2s)"/>']
    for _ in range(18):
        b.append(f'<circle cx="{r.uniform(0,484):.0f}" cy="{r.uniform(0,300):.0f}" r="{r.uniform(10,34):.0f}" fill="{r.choice(["#ffd890","#ff9ac8","#9ad8ff","#fff0b0"])}" opacity="{r.uniform(0.15,0.4):.2f}"/>')
    # banderines
    b.append('<path d="M-10 40 Q242 110 494 40" stroke="#f4e0c0" stroke-width="2" fill="none"/>')
    for i in range(10):
        t = (i + 0.5) / 10
        x = -10 + 504 * t
        y = 40 + 4 * 70 * t * (1 - t) * 0.98
        col = ["#ff5a5a", "#ffd34a", "#4ac0ff", "#7ad86a", "#ff8ad8"][i % 5]
        b.append(f'<path d="M{x-18:.0f} {y-2:.0f} L{x+18:.0f} {y+2:.0f} L{x:.0f} {y+40:.0f} Z" fill="{col}"/>')
    b += ['<rect y="350" width="484" height="134" fill="url(#om2t)"/>', '<path d="M0 350 L484 350" stroke="#fff" stroke-width="3" opacity="0.6"/>',
          '<ellipse cx="242" cy="392" rx="190" ry="34" fill="#000" opacity="0.18"/>',
          '<ellipse cx="242" cy="384" rx="176" ry="30" fill="#ffffff"/><ellipse cx="242" cy="380" rx="160" ry="24" fill="#eef0f4"/>',
          # piso inferior
          '<path d="M100 290 L100 372 A142 22 0 0 0 384 372 L384 290 Z" fill="url(#om2c)"/>',
          '<path d="M100 334 A142 22 0 0 0 384 334" stroke="#fff3f6" stroke-width="6" fill="none"/>',
          '<path d="M100 340 A142 22 0 0 0 384 340" stroke="#c84a74" stroke-width="2" fill="none" opacity="0.5"/>',
          '<ellipse cx="242" cy="290" rx="142" ry="22" fill="#fff4f8"/>']
    # goterones de nata
    for i in range(13):
        x = 106 + i * 21.5
        L = r.uniform(8, 26)
        yb = 290 + 22 * math.sin(math.acos(max(-1, min(1, (x - 242) / 142)))) - 2
        b.append(f'<path d="M{x-8:.0f} {yb-6:.0f} L{x-6:.0f} {yb+L:.0f} Q{x:.0f} {yb+L+8:.0f} {x+6:.0f} {yb+L:.0f} L{x+8:.0f} {yb-6:.0f} Z" fill="#fff4f8"/>')
    b += ['<path d="M150 228 L150 294 A92 15 0 0 0 334 294 L334 228 Z" fill="url(#om2k)"/>',
          '<ellipse cx="242" cy="228" rx="92" ry="15" fill="#fff8ee"/>',
          '<path d="M150 262 A92 15 0 0 0 334 262" stroke="#e8483b" stroke-width="5" fill="none" opacity="0.8"/>']
    for x in (170, 205, 242, 279, 314):  # fresas en el borde
        b.append(f'<path d="M{x-8} 296 Q{x} 284 {x+8} 296 Q{x} 314 {x-8} 296 Z" fill="#e8283b"/><circle cx="{x-2}" cy="294" r="1.5" fill="#ffe08a"/>')
    # velas
    for i, x in enumerate((186, 214, 242, 270, 298)):
        y = 224 - abs(x - 242) * 0.05
        col = ["#4ac0ff", "#ffd34a", "#ff5a8a", "#7ad86a", "#b48aff"][i]
        b += [f'<rect x="{x-5}" y="{y-56:.0f}" width="10" height="56" rx="3" fill="{col}"/>',
              f'<path d="M{x-5} {y-46:.0f} L{x+5} {y-52:.0f} M{x-5} {y-30:.0f} L{x+5} {y-36:.0f} M{x-5} {y-14:.0f} L{x+5} {y-20:.0f}" stroke="#ffffff" stroke-width="2.5" opacity="0.8"/>',
              f'<rect x="{x-5}" y="{y-56:.0f}" width="3" height="56" fill="#ffffff" opacity="0.35"/>',
              f'<circle cx="{x}" cy="{y-74:.0f}" r="26" fill="url(#om2b)"/>',
              f'<path d="M{x} {y-92:.0f} Q{x+8} {y-72:.0f} {x} {y-62:.0f} Q{x-8} {y-72:.0f} {x} {y-92:.0f} Z" fill="url(#om2f)"/>',
              f'<path d="M{x} {y-80:.0f} Q{x+3} {y-70:.0f} {x} {y-64:.0f} Q{x-3} {y-70:.0f} {x} {y-80:.0f} Z" fill="#ffffff"/>']
    for _ in range(26):  # confeti en la mesa
        x, y = r.uniform(10, 474), r.uniform(400, 480)
        b.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="7" height="4" fill="{r.choice(["#ff5a5a","#ffd34a","#4ac0ff","#7ad86a"])}" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>')
    return "".join(b), d


def _rueda(cx, cy, R, col_cubierta="#2a2a2e", llanta="#c9ccd2", radios=16, sw=7):
    out = [f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{col_cubierta}" stroke-width="{sw}"/>',
           f'<circle cx="{cx}" cy="{cy}" r="{R-sw*0.7:.1f}" fill="none" stroke="{llanta}" stroke-width="{sw*0.35:.1f}"/>']
    for k in range(radios):
        a = k * math.pi / radios * 2
        out.append(f'<path d="M{cx} {cy} L{cx+math.cos(a)*(R-sw*0.8):.1f} {cy+math.sin(a)*(R-sw*0.8):.1f}" stroke="{llanta}" stroke-width="1" opacity="0.8"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{sw*0.6:.1f}" fill="{llanta}"/>')
    out.append(f'<path d="M{cx-R*0.7:.1f} {cy-R*0.7:.1f} A{R} {R} 0 0 1 {cx+R*0.2:.1f} {cy-R:.1f}" stroke="#ffffff" stroke-width="2" opacity="0.4" fill="none"/>')
    return "".join(out)


def _esc_bici():
    r = random.Random(3)
    d = (lg("om3s", (0, "#7cc4ee"), (0.7, "#cdeaf6"), (1, "#fde2b0")) + lg("om3c", (0, "#e8c890"), (1, "#c49a62")) +
         lg("om3g", (0, "#8cc860"), (1, "#4f8a3a")))
    b = [f'<rect width="{PS}" height="230" fill="url(#om3s)"/>', _nubes(r, 3, 30, 120, 0.8),
         '<path d="M0 200 C80 170 160 190 240 172 C330 152 410 186 484 170 L484 240 L0 240 Z" fill="#8fb0c8" opacity="0.8"/>',
         '<path d="M0 220 C100 196 200 216 300 200 C380 188 440 206 484 200 L484 260 L0 260 Z" fill="#7ea862"/>',
         f'<rect y="225" width="{PS}" height="260" fill="url(#om3g)"/>']
    for x in range(10, 480, 34):  # álamos al fondo
        hh = r.uniform(30, 52)
        b.append(f'<ellipse cx="{x}" cy="{222-hh/2:.0f}" rx="9" ry="{hh/2:.0f}" fill="#4e7a3a"/><ellipse cx="{x-3}" cy="{220-hh/2:.0f}" rx="4" ry="{hh/2.4:.0f}" fill="#8ab860" opacity="0.6"/>')
    b += ['<path d="M228 228 C220 280 150 330 60 484 L330 484 C300 380 250 300 240 228 Z" fill="url(#om3c)"/>',
          '<path d="M228 228 C220 280 150 330 60 484" stroke="#a8804a" stroke-width="3" opacity="0.5" fill="none"/>']
    for _ in range(70):
        x, y = r.uniform(0, 484), r.uniform(260, 484)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.5,3.5):.1f}" fill="{r.choice(["#ffe85a","#ffffff","#ff8ab0","#c890ff"])}" opacity="0.9"/>')
    for _ in range(40):
        x, y = r.uniform(0, 484), r.uniform(300, 484)
        b.append(f'<path d="M{x:.0f} {y:.0f} l-3 -12 M{x:.0f} {y:.0f} l3 -10" stroke="#3a6a2a" stroke-width="1.5" opacity="0.7"/>')
    # bicicleta
    b.append('<ellipse cx="248" cy="430" rx="140" ry="10" fill="#4a3a20" opacity="0.4"/>')
    b.append(_rueda(170, 380, 52) + _rueda(330, 380, 52))
    col = "#1fa3a0"
    b += [f'<path d="M170 380 L230 380 L312 304 L210 304 Z" stroke="{col}" stroke-width="7" fill="none" stroke-linejoin="round"/>',
          f'<path d="M230 380 L198 290" stroke="{col}" stroke-width="7" stroke-linecap="round"/>',
          f'<path d="M312 304 L330 380 M312 304 L304 274" stroke="{col}" stroke-width="7" stroke-linecap="round"/>',
          f'<path d="M171 378 L229 378 L310 302" stroke="#9af0ec" stroke-width="2" opacity="0.6" fill="none"/>',
          '<path d="M184 288 L214 286 Q218 280 208 278 L186 280 Z" fill="#3a2a22"/>',
          '<path d="M296 274 L318 270 Q328 270 330 280" stroke="#2a2a2e" stroke-width="5" fill="none" stroke-linecap="round"/>',
          '<circle cx="230" cy="380" r="9" fill="#c9ccd2"/><path d="M230 380 L244 392" stroke="#2a2a2e" stroke-width="5" stroke-linecap="round"/>',
          '<path d="M300 300 Q322 296 334 312 L328 330 Q312 320 296 322 Z" fill="#d8a86a"/>',  # cesta
          *[f'<path d="M{300+k*7} 302 L{298+k*7} 322" stroke="#a8784a" stroke-width="1.5"/>' for k in range(5)],
          '<circle cx="306" cy="300" r="6" fill="#ff5a8a"/><circle cx="318" cy="298" r="5" fill="#ffd34a"/>']
    return "".join(b), d


def _esc_perro():
    r = random.Random(4)
    d = (lg("om4s", (0, "#5ab4ee"), (1, "#d2eefa")) + lg("om4g", (0, "#9ad86a"), (1, "#4c9a3a")) +
         lg("om4p", (0, "#f0b864"), (0.6, "#d8903e"), (1, "#b06a28")))
    b = [f'<rect width="{PS}" height="260" fill="url(#om4s)"/>', _nubes(r, 4, 30, 140),
         '<path d="M0 220 C60 190 120 200 170 180 C230 160 280 190 340 176 C400 164 450 190 484 182 L484 270 L0 270 Z" fill="#5f9a4a"/>']
    for x in (40, 110, 380, 450):  # árboles redondos
        b.append(f'<path d="M{x} 230 L{x} 196" stroke="#5a3a22" stroke-width="7"/><circle cx="{x}" cy="180" r="30" fill="#3f7a34"/>'
                 f'<circle cx="{x-10}" cy="170" r="16" fill="#6aa850" opacity="0.7"/>')
    b.append(f'<path d="M0 240 C120 226 300 250 484 232 L484 484 L0 484 Z" fill="url(#om4g)"/>')
    for _ in range(90):
        x, y = r.uniform(0, 484), r.uniform(250, 484)
        b.append(f'<path d="M{x:.0f} {y:.0f} q-2 -8 -1 -14 M{x:.0f} {y:.0f} q3 -6 4 -11" stroke="#3a7a2a" stroke-width="1.6" opacity="0.6" fill="none"/>')
    for _ in range(14):
        b.append(f'<circle cx="{r.uniform(0,484):.0f}" cy="{r.uniform(300,484):.0f}" r="3" fill="{r.choice(["#ffffff","#ffe85a"])}"/>')
    # perro corriendo hacia la derecha (galope extendido)
    b += ['<ellipse cx="240" cy="420" rx="120" ry="12" fill="#2a4a1a" opacity="0.35"/>',
          # patas lejanas
          '<path d="M178 330 C150 350 120 372 96 380" stroke="#a8682a" stroke-width="15" stroke-linecap="round" fill="none"/>',
          '<path d="M300 330 C330 344 360 360 384 356" stroke="#a8682a" stroke-width="14" stroke-linecap="round" fill="none"/>',
          # cola
          '<path d="M160 304 C130 292 116 270 108 252 C124 266 144 282 170 290 Z" fill="#d8903e"/>',
          '<path d="M108 252 C120 266 140 280 166 290" stroke="#f8d090" stroke-width="2" opacity="0.6" fill="none"/>',
          # cuerpo
          '<path d="M156 300 C170 272 250 262 300 276 C330 284 344 300 340 322 C334 344 300 352 260 350 C214 348 170 346 158 330 C150 320 150 310 156 300 Z" fill="url(#om4p)"/>',
          '<path d="M170 286 C220 268 280 270 318 284" stroke="#ffe0a8" stroke-width="4" opacity="0.6" fill="none"/>',
          '<path d="M200 344 C240 352 290 350 326 336" stroke="#8a5220" stroke-width="3" opacity="0.4" fill="none"/>',
          # patas cercanas
          '<path d="M190 334 C164 360 140 384 112 394" stroke="#d8903e" stroke-width="17" stroke-linecap="round" fill="none"/>',
          '<path d="M310 330 C340 352 366 372 398 372" stroke="#d8903e" stroke-width="16" stroke-linecap="round" fill="none"/>',
          '<ellipse cx="108" cy="396" rx="12" ry="7" fill="#c88038"/><ellipse cx="402" cy="372" rx="12" ry="7" fill="#c88038"/>',
          # cuello y cabeza
          '<path d="M300 290 C320 266 336 244 352 238 C372 232 392 246 392 262 C390 280 372 296 344 310 Z" fill="url(#om4p)"/>',
          '<path d="M350 236 C366 220 394 222 404 236 C414 250 428 254 440 260 C446 266 440 276 428 278 C410 280 392 278 376 274 C356 270 344 254 350 236 Z" fill="#e0a050"/>',
          '<path d="M354 230 C372 222 392 224 402 234" stroke="#ffe0a8" stroke-width="3" opacity="0.7" fill="none"/>',
          '<ellipse cx="440" cy="262" rx="7" ry="5" fill="#2a1a12"/><circle cx="438" cy="260" r="2" fill="#ffffff" opacity="0.7"/>',
          '<path d="M420 276 C424 288 432 294 438 292 C440 286 436 280 430 276 Z" fill="#ff7a8a"/>',
          '<path d="M376 240 C366 246 360 262 364 280 C356 276 350 260 356 244 Z" fill="#a8682a"/>',  # oreja
          '<circle cx="398" cy="246" r="4.5" fill="#2a1a12"/><circle cx="399.5" cy="244.5" r="1.6" fill="#ffffff"/>',
          '<path d="M318 270 C326 300 330 304 336 306" stroke="#e8483b" stroke-width="5" fill="none" opacity="0.9"/>',  # collar
          # pelota volando
          '<circle cx="452" cy="200" r="15" fill="#ff4a3a"/><path d="M440 192 Q452 204 464 196" stroke="#ffffff" stroke-width="2" fill="none"/>'
          '<circle cx="447" cy="195" r="4" fill="#ffffff" opacity="0.6"/>',
          '<path d="M60 300 L96 300 M50 320 L92 320 M70 340 L100 340" stroke="#ffffff" stroke-width="3" opacity="0.6" stroke-linecap="round"/>']
    return "".join(b), d


def _esc_nieve():
    r = random.Random(5)
    d = (lg("om5s", (0, "#8fb4dc"), (1, "#e4effa")) + lg("om5n", (0, "#ffffff"), (1, "#cfdcec")) +
         _rgu("om5b1", 222, 380, 110, ("0", "#ffffff"), ("0.6", "#eaf2fb"), ("1", "#a9bfd8")) +
         _rgu("om5b2", 228, 270, 80, ("0", "#ffffff"), ("0.6", "#eaf2fb"), ("1", "#a9bfd8")) +
         _rgu("om5b3", 234, 190, 58, ("0", "#ffffff"), ("0.6", "#eaf2fb"), ("1", "#a9bfd8")))
    b = [f'<rect width="{PS}" height="{PS}" fill="url(#om5s)"/>',
         '<path d="M0 260 C80 230 160 250 240 236 C320 222 400 250 484 240 L484 330 L0 330 Z" fill="#dce8f4"/>']
    for x, s in ((30, 1.0), (80, 0.8), (380, 1.1), (440, 0.9), (420, 0.7)):
        y = 270
        b.append(f'<path d="M{x} {y-90*s:.0f} L{x+34*s:.0f} {y:.0f} L{x-34*s:.0f} {y:.0f} Z" fill="#2f5a4a"/>'
                 f'<path d="M{x} {y-90*s:.0f} L{x+14*s:.0f} {y-50*s:.0f} L{x} {y-56*s:.0f} L{x-14*s:.0f} {y-50*s:.0f} Z" fill="#ffffff"/>'
                 f'<path d="M{x-24*s:.0f} {y-26*s:.0f} Q{x} {y-34*s:.0f} {x+24*s:.0f} {y-26*s:.0f}" stroke="#ffffff" stroke-width="{5*s:.0f}" fill="none"/>')
    b += [f'<path d="M0 300 C120 286 300 310 484 290 L484 484 L0 484 Z" fill="url(#om5n)"/>',
          '<ellipse cx="236" cy="462" rx="130" ry="16" fill="#8aa4c4" opacity="0.5"/>',
          '<circle cx="222" cy="390" r="92" fill="url(#om5b1)"/>', '<circle cx="228" cy="276" r="66" fill="url(#om5b2)"/>',
          '<circle cx="234" cy="194" r="48" fill="url(#om5b3)"/>',
          # brazos
          '<path d="M170 270 L96 220 M120 236 L104 210 M118 236 L94 238" stroke="#5a3a22" stroke-width="6" stroke-linecap="round"/>',
          '<path d="M288 266 L366 214 M342 230 L352 204 M342 230 L370 232" stroke="#5a3a22" stroke-width="6" stroke-linecap="round"/>',
          # sombrero
          '<ellipse cx="236" cy="152" rx="56" ry="10" fill="#1e1e26"/><path d="M204 152 L208 96 L266 96 L270 152 Z" fill="#26262e"/>',
          '<rect x="206" y="132" width="62" height="10" fill="#c83a3a"/><path d="M212 100 L214 148" stroke="#5a5a6a" stroke-width="4" opacity="0.6"/>',
          # cara
          '<circle cx="220" cy="186" r="5" fill="#1a1a1a"/><circle cx="250" cy="186" r="5" fill="#1a1a1a"/>',
          '<path d="M236 198 L284 206 L236 208 Z" fill="#f08a2a"/>',
          *[f'<circle cx="{216+k*8}" cy="{220+abs(k-2)*-2+4:.0f}" r="2.5" fill="#1a1a1a"/>' for k in range(5)],
          # bufanda
          '<path d="M178 236 Q232 256 284 234 L288 250 Q232 274 176 252 Z" fill="#e8483b"/>',
          '<path d="M256 248 L270 310 L250 312 L240 254 Z" fill="#d23a30"/>',
          '<path d="M190 242 L190 256 M210 248 L208 262 M262 246 L264 258 M253 280 L266 278 M256 296 L268 294" stroke="#ffd34a" stroke-width="4"/>',
          *[f'<circle cx="228" cy="{300+k*30}" r="6" fill="#1a1a1a"/>' for k in range(3)]]
    for _ in range(80):
        b.append(f'<circle cx="{r.uniform(0,484):.0f}" cy="{r.uniform(0,484):.0f}" r="{r.uniform(1.2,4):.1f}" fill="#ffffff" opacity="{r.uniform(0.6,1):.2f}"/>')
    return "".join(b), d


def _esc_concierto():
    r = random.Random(6)
    d = (lg("om6s", (0, "#160a34"), (0.6, "#3a0f4a"), (1, "#1a0a20")) +
         "".join(lg(f"om6h{i}", (0, c), (1, c + "00")) for i, c in enumerate(["#ff3df2", "#2ff3ff", "#ffd34a", "#ff6a3a", "#7a6aff"])))
    b = [f'<rect width="{PS}" height="{PS}" fill="url(#om6s)"/>']
    for i, (x, ang) in enumerate([(60, 18), (150, -10), (242, 4), (334, 12), (424, -16), (200, 26), (290, -24)]):
        a = math.radians(ang)
        L = 520
        ex, ey = x + math.sin(a) * L, math.cos(a) * L
        b.append(f'<path d="M{x-4} 30 L{ex-70:.0f} {ey:.0f} L{ex+70:.0f} {ey:.0f} L{x+4} 30 Z" fill="url(#om6h{i % 5})" opacity="0.55"/>')
    b.append(f'<rect width="{PS}" height="{PS}" fill="#ff8ae0" opacity="0.06"/>')
    b.append('<rect x="0" y="18" width="484" height="16" fill="#0a0612"/>')
    for x in (60, 150, 242, 334, 424, 200, 290):
        b.append(f'<circle cx="{x}" cy="32" r="18" fill="#ffffff" opacity="0.25"/><circle cx="{x}" cy="32" r="7" fill="#ffffff"/>')
    b += ['<path d="M0 290 L484 290 L484 310 L0 310 Z" fill="#20102a"/>', '<path d="M0 290 L484 290" stroke="#ff8ae0" stroke-width="2" opacity="0.6"/>',
          '<rect x="60" y="250" width="40" height="40" fill="#120818"/><rect x="384" y="250" width="40" height="40" fill="#120818"/>']
    # público a contraluz con manos arriba
    for fila, (y0, s, col) in enumerate([(360, 0.8, "#1a0e26"), (420, 1.0, "#0e0816"), (480, 1.25, "#06040a")]):
        x = -20 + fila * 18
        while x < 510:
            hx = x + r.uniform(-6, 6)
            b.append(f'<circle cx="{hx:.0f}" cy="{y0-48*s:.0f}" r="{17*s:.0f}" fill="{col}"/>'
                     f'<path d="M{hx-34*s:.0f} {y0+40:.0f} C{hx-34*s:.0f} {y0-20*s:.0f} {hx-18*s:.0f} {y0-30*s:.0f} {hx:.0f} {y0-30*s:.0f} '
                     f'C{hx+18*s:.0f} {y0-30*s:.0f} {hx+34*s:.0f} {y0-20*s:.0f} {hx+34*s:.0f} {y0+40:.0f} Z" fill="{col}"/>'
                     f'<path d="M{hx-14*s:.0f} {y0-62*s:.0f} A{17*s:.0f} {17*s:.0f} 0 0 1 {hx+12*s:.0f} {y0-62*s:.0f}" stroke="{r.choice(["#ff3df2","#2ff3ff","#ffd34a"])}" stroke-width="2" opacity="0.7" fill="none"/>')
            if r.random() < 0.45:
                lado = r.choice((-1, 1))
                bx, by = hx + lado * 22 * s, y0 - 22 * s
                tx, ty = bx + lado * r.uniform(4, 20) * s, by - r.uniform(70, 95) * s
                b.append(f'<path d="M{bx:.0f} {by:.0f} L{tx:.0f} {ty:.0f}" stroke="{col}" stroke-width="{10*s:.0f}" stroke-linecap="round"/>'
                         f'<circle cx="{tx:.0f}" cy="{ty-4*s:.0f}" r="{7*s:.0f}" fill="{col}"/>')
            x += r.uniform(48, 64) * s
    for _ in range(40):
        x, y = r.uniform(0, 484), r.uniform(40, 330)
        b.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="6" height="3" fill="{r.choice(["#ff3df2","#2ff3ff","#ffd34a","#ffffff"])}" opacity="0.9" transform="rotate({r.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>')
    return "".join(b), d


def _esc_colegio():
    r = random.Random(7)
    d = (lg("om7w", (0, "#d47a52"), (1, "#a8553a")) + lg("om7d", (0, "#3a8a6a"), (1, "#22604a"), x2=1, y2=0) +
         lg("om7m", (0, "#ffcc3a"), (1, "#e89a1a"), x2=1, y2=1) + lg("om7s", (0, "#8acaf0"), (1, "#d6eefa")) +
         lg("om7l", (0, "#fff2c0"), (1, "#fff2c000"), x2=1, y2=1))
    b = [f'<rect width="{PS}" height="60" fill="url(#om7s)"/>', f'<rect y="40" width="{PS}" height="360" fill="url(#om7w)"/>']
    for fila in range(26):  # ladrillos
        y = 40 + fila * 14
        off = 0 if fila % 2 == 0 else 20
        for k in range(-1, 13):
            b.append(f'<rect x="{k*40+off+1}" y="{y+1}" width="38" height="12" fill="#000" opacity="{r.uniform(0.02,0.12):.2f}"/>')
        b.append(f'<path d="M0 {y} L484 {y}" stroke="#f0c0a0" stroke-width="1.5" opacity="0.35"/>')
    b += ['<rect x="0" y="40" width="484" height="12" fill="#e8d6c0"/>',
          # ventanas
          '<rect x="30" y="80" width="90" height="110" fill="#f4ead8"/><rect x="38" y="88" width="74" height="94" fill="#7ab8dc"/>',
          '<path d="M75 88 L75 182 M38 135 L112 135" stroke="#f4ead8" stroke-width="5"/><path d="M42 92 L70 92 L44 130 Z" fill="#ffffff" opacity="0.35"/>',
          '<rect x="364" y="80" width="90" height="110" fill="#f4ead8"/><rect x="372" y="88" width="74" height="94" fill="#7ab8dc"/>',
          '<path d="M409 88 L409 182 M372 135 L446 135" stroke="#f4ead8" stroke-width="5"/><path d="M376 92 L404 92 L378 130 Z" fill="#ffffff" opacity="0.35"/>',
          # dibujos infantiles en la ventana (formas)
          '<circle cx="392" cy="160" r="9" fill="#ffd34a"/><path d="M420 172 L432 150 L444 172 Z" fill="#ff5a5a"/>',
          # puerta doble
          '<path d="M150 120 Q242 60 334 120 L334 380 L150 380 Z" fill="#efe2cc"/>',
          '<path d="M162 126 Q242 74 322 126 L322 380 L162 380 Z" fill="url(#om7d)"/>',
          '<path d="M242 96 L242 380" stroke="#174a38" stroke-width="4"/>',
          '<rect x="174" y="150" width="56" height="90" rx="4" fill="#9fd0e8" opacity="0.8"/><rect x="254" y="150" width="56" height="90" rx="4" fill="#9fd0e8" opacity="0.8"/>',
          '<path d="M178 154 L206 154 L180 196 Z" fill="#fff" opacity="0.45"/><path d="M258 154 L286 154 L260 196 Z" fill="#fff" opacity="0.45"/>',
          '<rect x="174" y="260" width="56" height="100" rx="4" fill="#000" opacity="0.15"/><rect x="254" y="260" width="56" height="100" rx="4" fill="#000" opacity="0.15"/>',
          '<rect x="226" y="270" width="6" height="30" rx="3" fill="#e8c060"/><rect x="252" y="270" width="6" height="30" rx="3" fill="#e8c060"/>',
          # escalones
          '<rect x="120" y="380" width="244" height="22" fill="#c9bfae"/><rect x="100" y="400" width="284" height="24" fill="#b5ab9a"/>',
          '<rect x="0" y="420" width="484" height="64" fill="#9a9488"/><path d="M120 380 L364 380 M100 400 L384 400" stroke="#ffffff" stroke-width="2" opacity="0.5"/>',
          # macetas
          '<path d="M100 340 L132 340 L128 380 L104 380 Z" fill="#c8603a"/><circle cx="116" cy="326" r="22" fill="#4f8a3a"/><circle cx="108" cy="318" r="10" fill="#7ab85a"/>'
          '<circle cx="110" cy="312" r="4" fill="#ff8ab0"/><circle cx="124" cy="322" r="4" fill="#ffd34a"/>',
          # luz de la mañana en diagonal
          '<path d="M0 40 L180 40 L484 330 L484 484 L380 484 Z" fill="url(#om7l)" opacity="0.35"/>']
    # mochila en primer plano
    b += ['<ellipse cx="350" cy="470" rx="92" ry="12" fill="#2a2018" opacity="0.4"/>',
          '<path d="M290 360 C290 320 410 320 410 360 L414 462 C414 474 286 474 286 462 Z" fill="url(#om7m)"/>',
          '<path d="M318 330 C318 300 382 300 382 330" stroke="#c8781a" stroke-width="9" fill="none"/>',
          '<path d="M306 400 L394 400 L398 456 C398 462 302 462 302 456 Z" fill="#3a8fd8"/>',
          '<path d="M306 400 L394 400" stroke="#ffffff" stroke-width="2" opacity="0.6"/>',
          '<path d="M300 380 C330 370 370 370 400 380" stroke="#c8781a" stroke-width="3" fill="none"/>',
          '<rect x="340" y="404" width="20" height="8" rx="2" fill="#e8e8f0"/>',
          '<path d="M296 344 C300 330 316 324 330 324" stroke="#fff3c0" stroke-width="4" opacity="0.7" fill="none"/>',
          '<circle cx="380" cy="430" r="9" fill="#ff5a8a"/><path d="M376 426 l8 8 M384 426 l-8 8" stroke="#ffffff" stroke-width="2"/>']
    return "".join(b), d


def _esc_carretera():
    r = random.Random(8)
    d = (lg("om8s", (0, "#5aa8e6"), (0.6, "#b8def4"), (1, "#ffd8a8")) + lg("om8m1", (0, "#8a90c0"), (1, "#a8b4d4")) +
         lg("om8m2", (0, "#5a7a9a"), (1, "#6a8a8a")) + lg("om8g", (0, "#7ab05a"), (1, "#3f7a34")) +
         lg("om8r", (0, "#5a5a62"), (1, "#3a3a40")) + rg("om8sol", (0, "#fff6d0", 1), (1, "#fff6d0", 0)))
    b = [f'<rect width="{PS}" height="300" fill="url(#om8s)"/>',
         '<circle cx="120" cy="150" r="80" fill="url(#om8sol)"/><circle cx="120" cy="150" r="22" fill="#fff8e0"/>',
         _nubes(r, 2, 40, 90, 0.7),
         '<path d="M0 230 L70 150 L120 190 L190 110 L260 180 L320 130 L400 200 L450 160 L484 180 L484 260 L0 260 Z" fill="url(#om8m1)"/>',
         '<path d="M190 110 L212 132 L200 130 L190 140 L178 128 L168 132 Z" fill="#ffffff"/>',
         '<path d="M320 130 L338 148 L326 146 L318 154 L310 144 Z" fill="#ffffff"/><path d="M70 150 L84 166 L70 162 L60 168 Z" fill="#ffffff"/>',
         '<path d="M0 260 L90 200 L160 240 L240 196 L330 246 L420 206 L484 236 L484 300 L0 300 Z" fill="url(#om8m2)"/>',
         '<path d="M0 290 C100 260 200 280 300 266 C380 256 440 270 484 266 L484 484 L0 484 Z" fill="url(#om8g)"/>']
    for _ in range(28):  # arbolitos
        x, y = r.uniform(0, 484), r.uniform(280, 330)
        if 190 < x < 300:
            continue
        s = 0.5 + (y - 280) / 60
        b.append(f'<path d="M{x:.0f} {y-22*s:.0f} L{x+8*s:.0f} {y:.0f} L{x-8*s:.0f} {y:.0f} Z" fill="#2f5a2a"/>')
    b += ['<path d="M236 272 L250 272 L420 484 L60 484 Z" fill="url(#om8r)"/>',
          '<path d="M236 272 L60 484" stroke="#f4f4f4" stroke-width="4"/><path d="M250 272 L420 484" stroke="#f4f4f4" stroke-width="4"/>']
    for k in range(8):  # línea discontinua en perspectiva
        t0, t1 = (k / 8) ** 1.8, ((k + 0.5) / 8) ** 1.8
        y0, y1 = 272 + 212 * t0, 272 + 212 * t1
        x0, x1 = 243 - 3 * t0, 243 - 3 * t1
        b.append(f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#ffd34a" stroke-width="{1+5*t1:.1f}"/>')
    for k in range(6):  # postes
        t = (k + 1) / 7
        y = 272 + 212 * t ** 1.6
        x = 250 + 190 * t ** 1.6 + 12
        b.append(f'<path d="M{x:.0f} {y:.0f} L{x:.0f} {y-30*t-4:.0f}" stroke="#ffffff" stroke-width="{1.5+3*t:.1f}"/><rect x="{x-1:.0f}" y="{y-30*t-4:.0f}" width="{2+3*t:.1f}" height="{4+5*t:.1f}" fill="#e8483b"/>')
    # coche de espaldas
    b += ['<ellipse cx="246" cy="430" rx="76" ry="10" fill="#000" opacity="0.4"/>',
          '<path d="M184 340 Q190 314 212 310 L280 310 Q302 314 308 340 Z" fill="#c82a2a"/>',
          '<path d="M194 338 Q200 320 216 318 L276 318 Q292 320 298 338 Z" fill="#2a3a4a"/>',
          '<path d="M200 334 Q206 322 220 321 L240 321 L208 336 Z" fill="#9fd0f0" opacity="0.6"/>',
          '<rect x="172" y="336" width="148" height="70" rx="12" fill="#e03a34"/>',
          '<rect x="172" y="336" width="148" height="14" rx="6" fill="#ff7a6a" opacity="0.6"/>',
          '<rect x="180" y="360" width="26" height="12" rx="3" fill="#ffcf8a"/><rect x="286" y="360" width="26" height="12" rx="3" fill="#ffcf8a"/>',
          '<rect x="226" y="372" width="40" height="12" rx="2" fill="#f4f4f4"/>',
          '<rect x="176" y="398" width="140" height="10" fill="#2a2a2e"/>',
          '<rect x="178" y="404" width="22" height="24" rx="4" fill="#1a1a1e"/><rect x="292" y="404" width="22" height="24" rx="4" fill="#1a1a1e"/>',
          '<rect x="208" y="298" width="76" height="12" rx="3" fill="#3a2a22"/><rect x="214" y="290" width="30" height="10" rx="2" fill="#4ac0ff"/>'
          '<rect x="246" y="292" width="32" height="8" rx="2" fill="#ffd34a"/>']
    return "".join(b), d


def _esc_cueva():
    """Escena fija de cueva gris y apagada: siempre la misma roca y la misma luz."""
    r = random.Random(9)
    d = (lg("om9f", (0, "#2a2b2f"), (1, "#18191c")) + lg("om9p", (0, "#55565a"), (1, "#2c2d30")) +
         rg("om9l", (0, "#9a9a9c", 0.5), (1, "#9a9a9c", 0)))
    b = [f'<rect width="{PS}" height="{PS}" fill="url(#om9f)"/>',
         '<ellipse cx="250" cy="300" rx="200" ry="150" fill="url(#om9l)"/>',
         # fondo de la galería
         '<path d="M120 330 C140 250 200 200 250 200 C310 200 360 250 370 330 Z" fill="#3a3b3f"/>',
         '<path d="M170 330 C180 280 220 250 250 250 C290 250 320 280 330 330 Z" fill="#232427"/>',
         # paredes cercanas
         '<path d="M0 0 L150 0 C130 80 110 160 120 240 C100 300 90 380 110 484 L0 484 Z" fill="#3e3f43"/>',
         '<path d="M484 0 L330 0 C360 90 380 170 368 250 C390 320 400 400 380 484 L484 484 Z" fill="#46474b"/>',
         '<path d="M150 0 C130 80 110 160 120 240 C100 300 90 380 110 484" stroke="#7a7a7e" stroke-width="3" opacity="0.5" fill="none"/>',
         '<path d="M330 0 C360 90 380 170 368 250 C390 320 400 400 380 484" stroke="#6a6a6e" stroke-width="3" opacity="0.4" fill="none"/>',
         # techo con estalactitas
         '<path d="M140 0 L340 0 C320 30 300 50 250 56 C200 56 160 40 140 0 Z" fill="#35363a"/>']
    for x, L in ((180, 40), (205, 70), (232, 34), (262, 58), (290, 30), (312, 48)):
        b.append(f'<path d="M{x-8} 40 L{x} {40+L} L{x+8} 40 Z" fill="#4a4b4f"/><path d="M{x-2} 44 L{x} {38+L}" stroke="#8a8a8e" stroke-width="1.5" opacity="0.5"/>')
    b += ['<path d="M0 360 C100 340 180 352 250 346 C330 340 400 356 484 350 L484 484 L0 484 Z" fill="url(#om9p)"/>',
          '<path d="M0 360 C100 340 180 352 250 346 C330 340 400 356 484 350" stroke="#7a7a7e" stroke-width="2" opacity="0.4" fill="none"/>']
    for _ in range(14):  # piedras grises
        x, y, s = r.uniform(20, 464), r.uniform(370, 470), r.uniform(8, 22)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y+s*0.3:.0f}" rx="{s*1.3:.0f}" ry="{s*0.3:.0f}" fill="#111" opacity="0.4"/>'
                 f'<path d="M{x-s:.0f} {y+s*0.3:.0f} C{x-s:.0f} {y-s*0.6:.0f} {x+s:.0f} {y-s*0.7:.0f} {x+s:.0f} {y+s*0.3:.0f} Z" fill="#5a5b5f"/>'
                 f'<path d="M{x-s*0.6:.0f} {y-s*0.3:.0f} Q{x:.0f} {y-s*0.6:.0f} {x+s*0.5:.0f} {y-s*0.3:.0f}" stroke="#8a8a8e" stroke-width="1.5" opacity="0.5" fill="none"/>')
    for _ in range(30):  # vetas
        x, y = r.uniform(0, 484), r.uniform(0, 340)
        if 140 < x < 360 and y > 60:
            continue
        b.append(f'<path d="M{x:.0f} {y:.0f} q{r.uniform(-30,30):.0f} {r.uniform(10,30):.0f} {r.uniform(-20,20):.0f} {r.uniform(30,60):.0f}" stroke="#1e1f22" stroke-width="{r.uniform(1,3):.1f}" opacity="0.6" fill="none"/>')
    b.append(f'<rect width="{PS}" height="{PS}" fill="#7a7a7e" opacity="0.08"/>')
    return "".join(b), d


def recuerdos():
    for i, f in enumerate([_esc_playa, _esc_tarta, _esc_bici, _esc_perro, _esc_nieve, _esc_concierto, _esc_colegio, _esc_carretera], 1):
        esc, d = f()
        _polaroid(f"recuerdo_{i}", esc, d)
    esc, d = _esc_cueva()
    _polaroid("recuerdo_cueva", esc, d, gris=True)


# ================================================================== RELOJ INTERNO
def reloj_interno():
    w = h = 620
    c = 310
    r = random.Random(11)
    d = (_lgu("omrj_dia", 0, 50, 0, 310, ("0", "#6fb6e8"), ("1", "#d6eefa")) +
         _lgu("omrj_noc", 0, 310, 0, 570, ("0", "#1b1340"), ("1", "#0b0f24")) +
         _lgu("omrj_bis", 40, 40, 580, 580, ("0", "#f4f6fa"), ("0.3", "#9aa3b0"), ("0.55", "#e8ecf2"), ("0.8", "#5a6270"), ("1", "#c9ced8")) +
         _lgu("omrj_bis2", 580, 580, 40, 40, ("0", "#f4f6fa"), ("0.4", "#7a8290"), ("1", "#3a404a")) +
         rg("omrj_sol", (0, "#fff8d0", 1), (0.35, "#ffe07a", 1), (0.6, "#ffcf8a", 0.4), (1, "#ffcf8a", 0)) +
         rg("omrj_luna", (0, "#e8eeff", 0.6), (1, "#e8eeff", 0)) +
         _lgu("omrj_hz", 0, 290, 0, 330, ("0", "#ffb15e", 0), ("0.5", "#ffb15e", 0.85), ("1", "#7a4ab0", 0)) +
         _lgu("omrj_gl", 100, 60, 300, 300, ("0", "#ffffff", 0.5), ("1", "#ffffff", 0)) +
         f'<clipPath id="omrj_cl"><circle cx="{c}" cy="{c}" r="262"/></clipPath>')
    b = ['<g filter="url(#sombra)">',
         f'<circle cx="{c}" cy="{c}" r="298" fill="url(#omrj_bis)"/>', f'<circle cx="{c}" cy="{c}" r="280" fill="url(#omrj_bis2)"/>',
         f'<circle cx="{c}" cy="{c}" r="270" fill="#2a2f3a"/></g>',
         '<g clip-path="url(#omrj_cl)">',
         f'<rect x="0" y="0" width="{w}" height="{c}" fill="url(#omrj_dia)"/>',
         f'<rect x="0" y="{c}" width="{w}" height="{c}" fill="url(#omrj_noc)"/>',
         _nubes(r, 0, 0, 0)]
    # nubes del día
    for (x, y, k) in ((170, 230, 0.9), (440, 210, 0.7), (230, 120, 0.6)):
        b.append(f'<g opacity="0.95"><ellipse cx="{x}" cy="{y}" rx="{50*k:.0f}" ry="{12*k:.0f}" fill="#ffffff"/><circle cx="{x-16*k:.0f}" cy="{y-8*k:.0f}" r="{16*k:.0f}" fill="#ffffff"/>'
                 f'<circle cx="{x+10*k:.0f}" cy="{y-14*k:.0f}" r="{20*k:.0f}" fill="#ffffff"/><ellipse cx="{x}" cy="{y+6*k:.0f}" rx="{46*k:.0f}" ry="{5*k:.0f}" fill="#9fc0dc" opacity="0.5"/></g>')
    # sol
    b.append(f'<circle cx="{c}" cy="150" r="90" fill="url(#omrj_sol)"/>')
    for k in range(12):
        a = math.radians(k * 30)
        b.append(f'<path d="M{c+math.cos(a)*44:.1f} {150+math.sin(a)*44:.1f} L{c+math.cos(a+0.12)*62:.1f} {150+math.sin(a+0.12)*62:.1f} L{c+math.cos(a-0.12)*62:.1f} {150+math.sin(a-0.12)*62:.1f} Z" fill="#ffd24a" opacity="0.9"/>')
    b.append(f'<circle cx="{c}" cy="150" r="36" fill="#ffd860"/><circle cx="{c-10}" cy="140" r="16" fill="#fff6c8" opacity="0.7"/>')
    # noche: estrellas y luna
    for _ in range(70):
        x, y = r.uniform(40, 580), r.uniform(330, 580)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(0.8,2.2):.1f}" fill="#ffffff" opacity="{r.uniform(0.4,1):.2f}"/>')
    for (x, y) in ((190, 400), (450, 430), (230, 520), (400, 360)):
        b.append(_destello_peq(x, y, 9, "#e8f0ff", 0.9))
    b.append(f'<circle cx="{c}" cy="462" r="70" fill="url(#omrj_luna)"/>'
             f'<path d="M{c-8} 424 A40 40 0 1 0 {c+30} 494 A32 32 0 1 1 {c-8} 424 Z" fill="#f2f0dc"/>'
             f'<circle cx="{c-10}" cy="476" r="5" fill="#cfcab0" opacity="0.7"/><circle cx="{c+4}" cy="490" r="3" fill="#cfcab0" opacity="0.7"/>')
    # horizonte: amanecer/atardecer
    b.append(f'<rect x="0" y="292" width="{w}" height="36" fill="url(#omrj_hz)"/>')
    b.append(f'<path d="M0 {c} L{w} {c}" stroke="#fff3d0" stroke-width="2" opacity="0.7"/>')
    # marcas sin números
    for k in range(48):
        a = math.radians(k * 7.5)
        L = 22 if k % 12 == 0 else (14 if k % 2 == 0 else 7)
        sw = 5 if k % 12 == 0 else (3 if k % 2 == 0 else 1.6)
        r0 = 256
        x0, y0 = c + math.cos(a) * r0, c + math.sin(a) * r0
        x1, y1 = c + math.cos(a) * (r0 - L), c + math.sin(a) * (r0 - L)
        col = "#ffffff" if math.sin(a) > 0 else "#1e3a5a"
        b.append(f'<path d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" opacity="0.85"/>')
    b += [_gr("omrj_cl", w, h, 0.8),
          f'<circle cx="{c}" cy="{c}" r="262" fill="none" stroke="#000" stroke-width="18" opacity="0.35" filter="url(#blur8)"/>',
          f'<path d="M{c-230} {c-60} A240 240 0 0 1 {c+60} {c-232} A260 200 0 0 0 {c-230} {c-60} Z" fill="url(#omrj_gl)" opacity="0.6"/>',
          '</g>',
          f'<path d="M{c+180} {c+220} A290 290 0 0 0 {c+250} {c-150}" stroke="#2ff3ff" stroke-width="3" opacity="0.5" fill="none"/>']
    _g("reloj_interno", "".join(b), w, h, d)


def aguja_interna():
    """Aguja del reloj interno. Lienzo 60×520: el centro (30,260) es el eje de giro. Apunta hacia arriba."""
    w, h = 60, 520
    cx, cy = 30, 260
    d = (lg("omag", (0, "#fff2c8"), (0.45, "#ffcf8a"), (0.55, "#d98a2a"), (1, "#8a4a12"), x2=1, y2=0) +
         rg("omag_h", (0, "#fff8e0", 1), (0.5, "#e8a84a", 1), (1, "#7a4210", 1), cx=0.35, cy=0.35))
    b = ['<g filter="url(#sombra)">',
         f'<path d="M{cx} 30 L{cx+9} 70 L{cx+6} {cy} L{cx+8} {cy+52} L{cx} {cy+66} L{cx-8} {cy+52} L{cx-6} {cy} L{cx-9} 70 Z" fill="url(#omag)"/>',
         f'<path d="M{cx} 30 L{cx} {cy+60}" stroke="#fff8e0" stroke-width="1.2" opacity="0.8"/>',
         f'<circle cx="{cx}" cy="{cy}" r="20" fill="url(#omag_h)"/>',
         f'<circle cx="{cx}" cy="{cy}" r="7" fill="#5a2e0a"/><circle cx="{cx-2}" cy="{cy-2}" r="2.5" fill="#fff8e0"/></g>',
         f'<path d="M{cx} 26 L{cx+6} 46 L{cx} 52 L{cx-6} 46 Z" fill="#fffbe8"/>']
    _g("aguja_interna", "".join(b), w, h, d)


# ================================================================== OJO
def ojo():
    w, h = 780, 480
    cx, cy = 390, 288
    r = random.Random(13)
    alm = f"M180 {cy+6} C250 {cy-104} 480 {cy-118} 600 {cy-22} C510 {cy+80} 270 {cy+92} 180 {cy+6} Z"
    d = (rg("omoj_piel", (0, "#eab894", 1), (0.55, "#e2aa86", 0.95), (0.8, "#e2aa86", 0.55), (1, "#e2aa86", 0)) +
         _rgu("omoj_esc", cx - 20, cy - 10, 230, ("0", "#fdfaf6"), ("0.6", "#f2e8e2"), ("1", "#c9a8a0")) +
         _rgu("omoj_iris", cx, cy - 18, 92, ("0", "#e8b45a"), ("0.32", "#c08a3a"), ("0.55", "#6f8a3e"), ("0.85", "#3f5a2c"), ("1", "#1e2a16")) +
         _lgu("omoj_par", 0, cy - 110, 0, cy - 20, ("0", "#3a1a12", 0.75), ("1", "#3a1a12", 0)) +
         _rgu("omoj_som", cx + 40, cy - 140, 200, ("0", "#b97d5c", 0.0), ("1", "#b97d5c", 0.0)) +
         _clip("omoj_cl", alm))
    b = [f'<ellipse cx="{cx}" cy="{cy-50}" rx="388" ry="236" fill="url(#omoj_piel)"/>',
         # sombra de la cuenca y pliegue del párpado
         f'<path d="M150 {cy-10} C230 {cy-170} 500 {cy-190} 640 {cy-40} C520 {cy-120} 280 {cy-120} 150 {cy-10} Z" fill="#b97d5c" opacity="0.45" filter="url(#blur8)"/>',
         f'<path d="M196 {cy-30} C270 {cy-150} 480 {cy-160} 604 {cy-58}" stroke="#9a5e42" stroke-width="5" opacity="0.55" fill="none" stroke-linecap="round"/>',
         f'<path d="M206 {cy-40} C280 {cy-160} 480 {cy-170} 600 {cy-70}" stroke="#f6cfae" stroke-width="6" opacity="0.5" fill="none"/>',
         f'<path d="M230 {cy+70} C320 {cy+120} 470 {cy+110} 570 {cy+40}" stroke="#b97d5c" stroke-width="10" opacity="0.35" fill="none" filter="url(#blur8)"/>',
         f'<path d="M190 {cy+10} C280 {cy+100} 510 {cy+92} 600 {cy-16}" stroke="#d99a8a" stroke-width="8" opacity="0.8" fill="none"/>',
         # ceja
         f'<path d="M190 {cy-170} C280 {cy-236} 470 {cy-246} 620 {cy-176} C600 {cy-196} 460 {cy-218} 300 {cy-200} C250 {cy-194} 210 {cy-180} 190 {cy-170} Z" fill="#3b2618" opacity="0.75"/>']
    for k in range(220):
        t = k / 120
        x = 196 + t * 420 + r.uniform(-4, 4)
        y = cy - 176 - 60 * math.sin(math.pi * (t * 0.85 + 0.1)) + r.uniform(-6, 10)
        a = math.radians(-20 + t * 40 + r.uniform(-12, 12)) if t > 0.15 else math.radians(-70)
        L = r.uniform(18, 30)
        b.append(f'<path d="M{x:.0f} {y:.0f} q{math.cos(a)*L*0.5:.1f} {math.sin(a)*L*0.5-4:.1f} {math.cos(a)*L:.1f} {math.sin(a)*L:.1f}" stroke="{r.choice(["#3b2618","#2a1a10","#5a3a24"])}" stroke-width="{r.uniform(1.5,2.6):.1f}" fill="none" stroke-linecap="round" opacity="0.85"/>')
    b += [f'<path d="{alm}" fill="url(#omoj_esc)"/>', '<g clip-path="url(#omoj_cl)">',
          f'<path d="M180 {cy+6} C220 {cy+30} 240 {cy+40} 260 {cy+30}" stroke="#e88a8a" stroke-width="6" opacity="0.25" fill="none"/>']
    # venitas suaves
    for k in range(6):
        x0 = r.choice((210, 220, 570, 580))
        y0 = cy + r.uniform(-20, 20)
        b.append(f'<path d="M{x0} {y0:.0f} q{(cx-x0)*0.15:.0f} {r.uniform(-14,14):.0f} {(cx-x0)*0.3:.0f} {r.uniform(-10,10):.0f}" stroke="#d07070" stroke-width="1" opacity="0.35" fill="none"/>')
    b.append(f'<circle cx="{cx}" cy="{cy-18}" r="96" fill="#000" opacity="0.18" filter="url(#blur8)"/>')
    b.append(f'<circle cx="{cx}" cy="{cy-18}" r="90" fill="url(#omoj_iris)"/>')
    for k in range(140):  # fibras del iris
        a = k / 140 * 2 * math.pi + r.uniform(-0.02, 0.02)
        r0, r1 = 34 + r.uniform(0, 6), r.uniform(60, 88)
        col = r.choice(["#f6d48a", "#2e3f1e", "#8aa050", "#5a3a1a"])
        b.append(f'<path d="M{cx+math.cos(a)*r0:.1f} {cy-18+math.sin(a)*r0:.1f} L{cx+math.cos(a+0.05)*r1:.1f} {cy-18+math.sin(a+0.05)*r1:.1f}" stroke="{col}" stroke-width="{r.uniform(1,2.4):.1f}" opacity="{r.uniform(0.25,0.55):.2f}"/>')
    b += [f'<circle cx="{cx}" cy="{cy-18}" r="52" fill="none" stroke="#c8902a" stroke-width="9" opacity="0.45"/>',
          f'<circle cx="{cx}" cy="{cy-18}" r="87" fill="none" stroke="#141c0e" stroke-width="7" opacity="0.8"/>',
          f'<circle cx="{cx}" cy="{cy-18}" r="34" fill="#070504"/>',
          # sombra del párpado superior sobre el ojo
          f'<rect x="150" y="{cy-130}" width="480" height="110" fill="url(#omoj_par)"/>',
          f'<ellipse cx="{cx+34}" cy="{cy-50}" rx="20" ry="15" fill="#ffffff" opacity="0.95"/>',
          f'<ellipse cx="{cx-28}" cy="{cy+18}" rx="8" ry="6" fill="#ffffff" opacity="0.55"/>',
          f'<path d="M{cx-60} {cy+30} A72 72 0 0 0 {cx+50} {cy+40}" stroke="#ffe8a0" stroke-width="5" opacity="0.25" fill="none"/>',
          _gr("omoj_cl", w, h, 0.6), '</g>',
          # carúncula y borde del párpado
          f'<path d="M180 {cy+6} C188 {cy-6} 200 {cy-10} 210 {cy-2} C206 {cy+12} 194 {cy+16} 180 {cy+6} Z" fill="#e48a8a"/>',
          f'<path d="M180 {cy+6} C250 {cy-104} 480 {cy-118} 600 {cy-22}" stroke="#5a2a1e" stroke-width="7" fill="none" stroke-linecap="round"/>',
          f'<path d="M182 {cy+8} C270 {cy+90} 510 {cy+80} 600 {cy-20}" stroke="#f0b0a0" stroke-width="3" fill="none" opacity="0.9"/>']
    # pestañas superiores
    for k in range(46):
        t = 0.04 + k / 46 * 0.94
        # punto sobre la curva superior (Bezier cúbica)
        p0, p1, p2, p3 = (180, cy + 6), (250, cy - 104), (480, cy - 118), (600, cy - 22)
        x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]
        y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
        L = (16 + 34 * math.sin(math.pi * (t * 0.8 + 0.15))) * r.uniform(0.85, 1.1)
        a = math.radians(-100 + t * 70 + r.uniform(-6, 6))
        ex, ey = x + math.cos(a) * L, y + math.sin(a) * L
        cxp, cyp = x + math.cos(a - 0.5) * L * 0.5, y + math.sin(a - 0.5) * L * 0.5 - 6
        b.append(f'<path d="M{x:.1f} {y:.1f} Q{cxp:.1f} {cyp:.1f} {ex+L*0.25:.1f} {ey:.1f}" stroke="#1e140e" stroke-width="{r.uniform(2.2,3.4):.1f}" fill="none" stroke-linecap="round"/>')
    for k in range(20):  # pestañas inferiores
        t = 0.2 + k / 20 * 0.75
        p0, p1, p2, p3 = (182, cy + 8), (270, cy + 90), (510, cy + 80), (600, cy - 20)
        x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t**2*p2[0] + t**3*p3[0]
        y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t**2*p2[1] + t**3*p3[1]
        L = r.uniform(8, 15)
        a = math.radians(95 - t * 50)
        b.append(f'<path d="M{x:.1f} {y+2:.1f} q{math.cos(a)*L*0.5+3:.1f} {math.sin(a)*L*0.5:.1f} {math.cos(a)*L+4:.1f} {math.sin(a)*L:.1f}" stroke="#3a2618" stroke-width="1.4" fill="none" opacity="0.7"/>')
    _g("ojo", "".join(b), w, h, d)


def rayo_sol():
    """Haz que viaja hacia la DERECHA: entra ancho por la izquierda y llega estrecho al punto (1000,180)."""
    w, h = 1040, 360
    r = random.Random(17)
    d = (lg("omry1", (0, "#ffcf8a00"), (0.25, "#ffcf8a"), (0.85, "#fff0c0"), (1, "#ffffff"), x2=1, y2=0) +
         lg("omry2", (0, "#fff8e000"), (0.4, "#fff8e0"), (1, "#ffffff"), x2=1, y2=0) +
         rg("omry3", (0, "#ffffff", 1), (0.4, "#fff3c0", 0.7), (1, "#ffcf8a", 0)))
    b = [f'<path d="M0 10 L1000 165 L1000 195 L0 350 Z" fill="url(#omry1)" opacity="0.45" filter="url(#blur20)"/>',
         f'<path d="M0 60 L1000 170 L1000 190 L0 300 Z" fill="url(#omry1)" opacity="0.6"/>',
         f'<path d="M0 130 L1000 176 L1000 184 L0 230 Z" fill="url(#omry2)" opacity="0.8"/>']
    for k in range(7):
        y0 = 40 + k * 46 + r.uniform(-10, 10)
        b.append(f'<path d="M0 {y0:.0f} L1000 {180+(y0-180)*0.08:.0f}" stroke="#fff8e0" stroke-width="{r.uniform(2,6):.1f}" opacity="{r.uniform(0.1,0.3):.2f}"/>')
    for _ in range(70):
        x = r.uniform(80, 980)
        hw = 170 * (1 - x / 1000) + 12
        y = 180 + r.uniform(-hw, hw)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1,3.2):.1f}" fill="#fffbe8" opacity="{r.uniform(0.3,0.9):.2f}"/>')
    b.append('<circle cx="1000" cy="180" r="38" fill="url(#omry3)"/>')
    _g("rayo_sol", "".join(b), w, h, d)


# ================================================================== TROFEO, URNA, NOTAS
_ORO = (("0", "#6a3e0c"), ("0.18", "#d9a23a"), ("0.32", "#fff2b8"), ("0.42", "#f6cf6a"), ("0.65", "#b07a1e"), ("0.85", "#7a4a10"), ("1", "#e8b84a"))


def trofeo(sombra=None):
    w, h = 540, 700
    d = (_lgu("omtr_o", 120, 0, 420, 0, *_ORO) + _lgu("omtr_o2", 190, 0, 350, 0, *_ORO) +
         _lgu("omtr_b", 0, 560, 0, 680, ("0", "#3a2a22"), ("1", "#1a120e")) +
         _lgu("omtr_bf", 140, 0, 400, 0, ("0", "#2a1e18"), ("0.35", "#5a463a"), ("1", "#1a120e")) +
         _lgu("omtr_in", 0, 60, 0, 120, ("0", "#5a3608"), ("1", "#b07a1e")))
    cup = "M120 70 L420 70 C420 230 360 330 270 340 C180 330 120 230 120 70 Z"
    b = [_sc(270, 678, 200, 18, 0.45, sombra),
         # asas
         '<path d="M126 110 C40 100 40 250 190 290" stroke="url(#omtr_o)" stroke-width="20" fill="none" stroke-linecap="round"/>',
         '<path d="M414 110 C500 100 500 250 350 290" stroke="url(#omtr_o)" stroke-width="20" fill="none" stroke-linecap="round"/>',
         '<path d="M124 104 C52 100 50 236 186 282" stroke="#fff6c8" stroke-width="4" opacity="0.6" fill="none"/>',
         f'<path d="{cup}" fill="url(#omtr_o)"/>',
         '<ellipse cx="270" cy="70" rx="150" ry="22" fill="url(#omtr_o)"/><ellipse cx="270" cy="72" rx="136" ry="16" fill="url(#omtr_in)"/>',
         '<path d="M175 100 C180 200 210 280 250 320" stroke="#fffbe0" stroke-width="14" opacity="0.55" fill="none" stroke-linecap="round"/>',
         '<path d="M150 100 C152 140 158 170 168 200" stroke="#ffffff" stroke-width="5" opacity="0.7" fill="none" stroke-linecap="round"/>',
         '<path d="M370 110 C366 200 340 280 300 320" stroke="#5a3608" stroke-width="10" opacity="0.4" fill="none"/>',
         '<path d="M140 150 Q270 176 400 150" stroke="#7a4a10" stroke-width="3" opacity="0.5" fill="none"/>',
         '<path d="M140 156 Q270 182 400 156" stroke="#fff2b8" stroke-width="2" opacity="0.6" fill="none"/>',
         # tallo y nudo
         '<path d="M250 336 L290 336 L284 420 L256 420 Z" fill="url(#omtr_o2)"/>',
         '<ellipse cx="270" cy="400" rx="38" ry="18" fill="url(#omtr_o2)"/>',
         '<path d="M230 470 C240 440 256 424 258 416 L282 416 C284 424 300 440 310 470 Z" fill="url(#omtr_o2)"/>',
         '<ellipse cx="270" cy="474" rx="90" ry="18" fill="url(#omtr_o)"/>',
         '<rect x="180" y="474" width="180" height="40" fill="url(#omtr_o)"/><ellipse cx="270" cy="514" rx="90" ry="14" fill="#7a4a10"/>',
         # peana de madera oscura con placa lisa
         '<path d="M140 530 L400 530 L420 670 L120 670 Z" fill="url(#omtr_bf)"/>',
         '<path d="M140 530 L400 530 L404 548 L136 548 Z" fill="#6a5244"/>',
         '<rect x="200" y="580" width="140" height="50" rx="4" fill="url(#omtr_o2)"/>',
         '<rect x="206" y="586" width="128" height="38" rx="3" fill="none" stroke="#7a4a10" stroke-width="2" opacity="0.6"/>',
         '<path d="M400 530 L420 670" stroke="#2ff3ff" stroke-width="0" />']
    # brillos estrella
    b += [_destello_peq(168, 128, 14, "#ffffff", 0.95), _destello_peq(398, 470, 9, "#ffffff", 0.8)]
    _g("trofeo", "".join(b), w, h, d)


def urna_voto(sombra=None):
    w, h = 600, 640
    r = random.Random(19)
    d = (_lgu("omur_v", 80, 0, 520, 0, ("0", "#dff3ff", 0.35), ("0.3", "#ffffff", 0.12), ("0.7", "#bfe4ff", 0.1), ("1", "#9fd0f0", 0.3)) +
         lg("omur_t", (0, "#5a6e86"), (1, "#2e3a4c")) + lg("omur_s", (0, "#f6efe0"), (1, "#d8ccb4"), x2=1, y2=1))
    # caja: frente 100..460 x 230..600; lado derecho hasta 520 (perspectiva)
    sobres = []
    for i in range(14):
        x, y = r.uniform(120, 430), r.uniform(470, 580)
        ang = r.uniform(-35, 35)
        sobres.append((x, y, ang))
    b = [_sc(310, 608, 250, 20, 0.4, sombra),
         # cara trasera y lado (se ven a través)
         '<path d="M160 190 L520 190 L520 560 L460 600 L100 600 L100 230 Z" fill="#cfeaff" opacity="0.10"/>',
         '<path d="M160 190 L160 560 L100 600 M160 560 L520 560" stroke="#e8f6ff" stroke-width="2" opacity="0.35" fill="none"/>']
    for (x, y, ang) in sobres:
        b.append(f'<g transform="translate({x:.0f} {y:.0f}) rotate({ang:.0f})"><rect x="-44" y="-28" width="88" height="56" rx="3" fill="url(#omur_s)"/>'
                 f'<path d="M-44 -28 L0 6 L44 -28" stroke="#b8a888" stroke-width="2" fill="none"/>'
                 f'<rect x="-44" y="-28" width="88" height="56" rx="3" fill="none" stroke="#a89878" stroke-width="1" opacity="0.6"/></g>')
    b += [f'<path d="M100 230 L460 230 L460 600 L100 600 Z" fill="url(#omur_v)"/>',
          '<path d="M460 230 L520 190 L520 560 L460 600 Z" fill="#bfe4ff" opacity="0.22"/>',
          '<path d="M100 230 L460 230 L460 600 L100 600 Z" fill="none" stroke="#f0faff" stroke-width="4" opacity="0.8"/>',
          '<path d="M460 230 L520 190 L520 560 L460 600" fill="none" stroke="#d8f0ff" stroke-width="3" opacity="0.7"/>',
          '<path d="M140 250 L220 250 L120 470 L120 330 Z" fill="#ffffff" opacity="0.18"/>',
          '<path d="M250 250 L280 250 L140 580 L120 580 Z" fill="#ffffff" opacity="0.12"/>',
          # tapa
          '<path d="M90 222 L160 176 L532 176 L472 222 Z" fill="url(#omur_t)"/>',
          '<path d="M90 222 L472 222 L472 240 L90 240 Z" fill="#26303e"/>',
          '<path d="M472 222 L532 176 L532 194 L472 240 Z" fill="#1e2632"/>',
          '<path d="M90 222 L160 176 L532 176" stroke="#9ab0c8" stroke-width="2" opacity="0.7" fill="none"/>',
          '<path d="M250 196 L380 196 L366 206 L236 206 Z" fill="#0a0e14"/>',
          # sobre entrando por la ranura
          '<g transform="translate(308 150) rotate(-4)"><rect x="-60" y="-70" width="120" height="78" rx="3" fill="url(#omur_s)"/>'
          '<path d="M-60 -70 L0 -26 L60 -70" stroke="#b8a888" stroke-width="2.5" fill="none"/>'
          '<path d="M-58 -68 L-58 6" stroke="#ffffff" stroke-width="2" opacity="0.8"/>'
          '<rect x="-60" y="-70" width="120" height="78" rx="3" fill="none" stroke="#a89878" stroke-width="1.2"/></g>',
          '<path d="M252 199 L378 199" stroke="#000" stroke-width="4" opacity="0.6"/>']
    _g("urna_voto", "".join(b), w, h, d)


def _nota(nombre, doble, c1, c2, cg):
    w, h = (440, 460) if doble else (300, 460)
    d = (lg(f"{nombre}_g", (0, c1), (1, c2), x2=1, y2=1) + rg(f"{nombre}_h", (0, cg, 0.8), (1, cg, 0)))
    def cabeza(x, y):
        return (f'<ellipse cx="{x}" cy="{y}" rx="52" ry="38" transform="rotate(-22 {x} {y})" fill="url(#{nombre}_g)"/>'
                f'<ellipse cx="{x-14}" cy="{y-12}" rx="22" ry="10" transform="rotate(-22 {x-14} {y-12})" fill="#ffffff" opacity="0.55"/>'
                f'<path d="M{x-44} {y+14} A52 38 -22 0 0 {x+30} {y+30}" stroke="#ffffff" stroke-width="3" opacity="0.35" fill="none"/>')
    b = [f'<ellipse cx="{w/2}" cy="{h/2}" rx="{w/2-10}" ry="{h/2-10}" fill="url(#{nombre}_h)"/>']
    if doble:
        b += [cabeza(110, 380), cabeza(320, 340),
              f'<rect x="146" y="80" width="16" height="300" rx="4" fill="url(#{nombre}_g)"/>',
              f'<rect x="356" y="40" width="16" height="300" rx="4" fill="url(#{nombre}_g)"/>',
              f'<path d="M146 80 L372 40 L372 92 L146 132 Z" fill="url(#{nombre}_g)"/>',
              f'<path d="M150 84 L368 46" stroke="#ffffff" stroke-width="4" opacity="0.6"/>',
              f'<path d="M150 90 L150 370" stroke="#ffffff" stroke-width="3" opacity="0.5"/>']
    else:
        b += [cabeza(110, 380),
              f'<rect x="146" y="50" width="16" height="330" rx="4" fill="url(#{nombre}_g)"/>',
              f'<path d="M154 50 C170 110 250 130 250 210 C250 250 232 280 216 296 C236 250 236 200 162 168 Z" fill="url(#{nombre}_g)"/>',
              f'<path d="M160 60 C180 112 240 132 244 200" stroke="#ffffff" stroke-width="3" opacity="0.5" fill="none"/>',
              f'<path d="M150 60 L150 370" stroke="#ffffff" stroke-width="3" opacity="0.5"/>']
    b += [_destello_peq(60, 300, 12), _destello_peq(w - 50, 120, 10), _destello_peq(w - 80, 420, 7)]
    _g(nombre, "".join(b), w, h, d)


# ================================================================== MÓVILES
def _icono(x, y, s, c1, c2, glifo, k):
    gid = f"omic{k}"
    g = lg(gid, (0, c1), (1, c2), x2=1, y2=1)
    q = s * 0.5
    cx, cy = x + q, y + q
    gl = {0: f'<circle cx="{cx}" cy="{cy}" r="{s*0.22:.1f}" fill="none" stroke="#fff" stroke-width="{s*0.08:.1f}"/>',
          1: f'<rect x="{cx-s*0.2:.1f}" y="{cy-s*0.2:.1f}" width="{s*0.4:.1f}" height="{s*0.4:.1f}" rx="{s*0.08:.1f}" fill="#fff" opacity="0.9"/>',
          2: f'<path d="M{cx-s*0.2:.1f} {cy+s*0.18:.1f} L{cx:.1f} {cy-s*0.2:.1f} L{cx+s*0.2:.1f} {cy+s*0.18:.1f} Z" fill="#fff" opacity="0.9"/>',
          3: f'<path d="M{cx-s*0.25:.1f} {cy:.1f} q{s*0.125:.1f} {-s*0.2:.1f} {s*0.25:.1f} 0 t{s*0.25:.1f} 0" stroke="#fff" stroke-width="{s*0.08:.1f}" fill="none"/>',
          4: f'<circle cx="{cx-s*0.1:.1f}" cy="{cy:.1f}" r="{s*0.12:.1f}" fill="#fff"/><circle cx="{cx+s*0.14:.1f}" cy="{cy:.1f}" r="{s*0.08:.1f}" fill="#fff" opacity="0.7"/>',
          5: f'<path d="M{cx-s*0.18:.1f} {cy-s*0.16:.1f} L{cx+s*0.18:.1f} {cy-s*0.16:.1f} M{cx-s*0.18:.1f} {cy:.1f} L{cx+s*0.18:.1f} {cy:.1f} M{cx-s*0.18:.1f} {cy+s*0.16:.1f} L{cx+s*0.06:.1f} {cy+s*0.16:.1f}" stroke="#fff" stroke-width="{s*0.07:.1f}" stroke-linecap="round"/>'}[glifo % 6]
    return g, (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s*0.24:.1f}" fill="url(#{gid})"/>'
               f'<path d="M{x+s*0.15:.1f} {y+s*0.08:.1f} L{x+s*0.85:.1f} {y+s*0.08:.1f}" stroke="#fff" stroke-width="2" opacity="0.35" stroke-linecap="round"/>' + gl)


_COLS = [("#ff6a5a", "#d8304a"), ("#4ac0ff", "#2a6ad8"), ("#7ad86a", "#2a9a4a"), ("#ffd34a", "#f08a1a"), ("#b48aff", "#6a3ad8"),
         ("#ff8ad8", "#d83a9a"), ("#5ae0d0", "#1a9a9a"), ("#f4f4f8", "#b8bcc8"), ("#ff9a4a", "#d85a1a"), ("#6a8aff", "#3a4ad8")]


def telefono_movil():
    w, h = 380, 760
    r = random.Random(23)
    d = (_lgu("omtm_c", 20, 0, 360, 0, ("0", "#5a5e66"), ("0.08", "#1e2026"), ("0.9", "#16181c"), ("1", "#4a4e56")) +
         _lgu("omtm_p", 0, 30, 0, 730, ("0", "#3a1e6a"), ("0.45", "#a83a8a"), ("0.8", "#ff8a5a"), ("1", "#ffcf8a")) +
         lg("omtm_gl", (0, "#ffffff"), (0.4, "#ffffff00"), x2=1, y2=1) +
         '<clipPath id="omtm_cl"><rect x="36" y="26" width="308" height="708" rx="34"/></clipPath>')
    b = ['<g filter="url(#sombra)"><rect x="20" y="10" width="340" height="740" rx="50" fill="url(#omtm_c)"/></g>',
         '<rect x="16" y="150" width="6" height="60" rx="3" fill="#3a3e46"/><rect x="358" y="120" width="6" height="90" rx="3" fill="#3a3e46"/>',
         '<rect x="16" y="230" width="6" height="60" rx="3" fill="#3a3e46"/>',
         '<rect x="22" y="12" width="336" height="736" rx="48" fill="none" stroke="#8a8e96" stroke-width="2" opacity="0.6"/>',
         '<rect x="36" y="26" width="308" height="708" rx="34" fill="url(#omtm_p)"/>', '<g clip-path="url(#omtm_cl)">']
    for k in range(5):  # ondas del fondo de pantalla
        y = 300 + k * 90
        b.append(f'<path d="M0 {y} C100 {y-60} 200 {y+60} 400 {y-30} L400 760 L0 760 Z" fill="#ffffff" opacity="0.06"/>')
    b += ['<circle cx="300" cy="200" r="110" fill="#ff3df2" opacity="0.25" filter="url(#blur20)"/>',
          # barra de estado
          '<rect x="60" y="44" width="40" height="10" rx="5" fill="#ffffff" opacity="0.9"/>',
          '<rect x="280" y="44" width="30" height="12" rx="3" fill="none" stroke="#fff" stroke-width="2"/><rect x="283" y="47" width="20" height="6" fill="#fff"/>',
          '<path d="M256 56 L262 50 L262 56 Z M264 56 L270 44 L270 56 Z" fill="#fff"/>',
          '<circle cx="190" cy="52" r="10" fill="#050608"/><circle cx="187" cy="49" r="3" fill="#2a3a5a"/>',
          # widget grande
          '<rect x="58" y="90" width="264" height="120" rx="24" fill="#ffffff" opacity="0.18"/>',
          '<rect x="78" y="112" width="120" height="22" rx="6" fill="#ffffff" opacity="0.9"/><rect x="78" y="146" width="80" height="12" rx="6" fill="#ffffff" opacity="0.6"/>',
          '<rect x="78" y="168" width="100" height="12" rx="6" fill="#ffffff" opacity="0.45"/>',
          '<circle cx="270" cy="148" r="30" fill="#ffd34a"/><ellipse cx="282" cy="166" rx="30" ry="14" fill="#ffffff"/>']
    k = 0
    for fila in range(4):
        for col in range(4):
            c1, c2 = _COLS[(fila * 4 + col) % len(_COLS)]
            gd, ic = _icono(62 + col * 68, 236 + fila * 86, 52, c1, c2, fila * 4 + col, f"a{k}")
            d += gd
            b.append(ic)
            b.append(f'<rect x="{70+col*68}" y="{294+fila*86}" width="36" height="6" rx="3" fill="#ffffff" opacity="0.5"/>')
            k += 1
    b.append('<rect x="52" y="610" width="276" height="88" rx="30" fill="#ffffff" opacity="0.22"/>')
    for col in range(4):
        c1, c2 = _COLS[(col * 3 + 1) % len(_COLS)]
        gd, ic = _icono(66 + col * 66, 628, 52, c1, c2, col + 2, f"ad{col}")
        d += gd
        b.append(ic)
    b += ['<rect x="140" y="716" width="100" height="6" rx="3" fill="#ffffff" opacity="0.85"/>',
          '<rect width="380" height="760" fill="url(#omtm_gl)" opacity="0.18"/>',
          '<path d="M36 26 L200 26 L36 300 Z" fill="#ffffff" opacity="0.06"/>', '</g>']
    _g("telefono_movil", "".join(b), w, h, d)


def telefono_movil_b():
    w, h = 380, 780
    d = (_lgu("omtb_c", 20, 0, 360, 0, ("0", "#e8eef4"), ("0.06", "#9aa6b4"), ("0.5", "#c8d2dc"), ("0.94", "#8a96a4"), ("1", "#f4f8fc")) +
         _lgu("omtb_p", 0, 20, 0, 760, ("0", "#0a2a4a"), ("0.4", "#1a6aa8"), ("0.75", "#2fc8d8"), ("1", "#bff6f0")) +
         lg("omtb_gl", (0, "#ffffff"), (0.4, "#ffffff00"), x2=1, y2=1) +
         '<clipPath id="omtb_cl"><rect x="30" y="18" width="320" height="744" rx="44"/></clipPath>')
    b = ['<g filter="url(#sombra)"><rect x="20" y="8" width="340" height="764" rx="54" fill="url(#omtb_c)"/></g>',
         '<rect x="15" y="160" width="7" height="44" rx="3" fill="#a8b2be"/><rect x="15" y="220" width="7" height="70" rx="3" fill="#a8b2be"/>',
         '<rect x="358" y="200" width="7" height="100" rx="3" fill="#a8b2be"/>',
         '<rect x="26" y="14" width="328" height="752" rx="50" fill="#0a0c10"/>',
         '<rect x="30" y="18" width="320" height="744" rx="44" fill="url(#omtb_p)"/>', '<g clip-path="url(#omtb_cl)">',
         '<circle cx="80" cy="560" r="160" fill="#2ff3ff" opacity="0.25" filter="url(#blur40)"/>',
         '<circle cx="320" cy="260" r="140" fill="#7a6aff" opacity="0.35" filter="url(#blur40)"/>',
         '<path d="M0 520 C120 440 240 600 400 480 L400 800 L0 800 Z" fill="#ffffff" opacity="0.07"/>',
         # isla
         '<rect x="140" y="34" width="100" height="30" rx="15" fill="#050608"/><circle cx="222" cy="49" r="6" fill="#1a2438"/>',
         '<rect x="58" y="42" width="36" height="12" rx="6" fill="#fff" opacity="0.9"/>',
         '<rect x="286" y="42" width="34" height="14" rx="4" fill="none" stroke="#fff" stroke-width="2"/><rect x="289" y="45" width="26" height="8" fill="#7af0a0"/>',
         # reloj grande sin números
         '<circle cx="118" cy="160" r="66" fill="#ffffff" opacity="0.92"/>',
         *[f'<path d="M{118+math.cos(a)*56:.1f} {160+math.sin(a)*56:.1f} L{118+math.cos(a)*62:.1f} {160+math.sin(a)*62:.1f}" stroke="#2a3a4a" stroke-width="3"/>' for a in [k*math.pi/6 for k in range(12)]],
         '<path d="M118 160 L118 116 M118 160 L150 176" stroke="#1a2a3a" stroke-width="5" stroke-linecap="round"/><circle cx="118" cy="160" r="5" fill="#ff5a5a"/>',
         # widget del tiempo
         '<rect x="200" y="94" width="130" height="132" rx="26" fill="#ffffff" opacity="0.2"/>',
         '<circle cx="250" cy="146" r="24" fill="#ffd34a"/><ellipse cx="270" cy="164" rx="34" ry="16" fill="#ffffff"/><circle cx="258" cy="156" r="16" fill="#ffffff"/>',
         '<rect x="220" y="196" width="60" height="10" rx="5" fill="#fff" opacity="0.7"/>',
         # tarjeta de música / foto
         '<rect x="50" y="250" width="280" height="110" rx="26" fill="#ffffff" opacity="0.18"/>',
         '<rect x="66" y="266" width="78" height="78" rx="16" fill="#ff8a5a"/><circle cx="105" cy="305" r="22" fill="#ffd34a" opacity="0.8"/>',
         '<rect x="160" y="276" width="140" height="14" rx="7" fill="#fff" opacity="0.85"/><rect x="160" y="300" width="90" height="10" rx="5" fill="#fff" opacity="0.55"/>',
         '<rect x="160" y="326" width="150" height="6" rx="3" fill="#fff" opacity="0.3"/><rect x="160" y="326" width="70" height="6" rx="3" fill="#fff" opacity="0.9"/>']
    for fila in range(2):
        for col in range(4):
            c1, c2 = _COLS[(fila * 4 + col + 5) % len(_COLS)]
            gd, ic = _icono(56 + col * 70, 392 + fila * 92, 56, c1, c2, fila * 4 + col + 3, f"b{fila}{col}")
            d += gd
            b.append(ic)
            b.append(f'<rect x="{66+col*70}" y="{454+fila*92}" width="36" height="6" rx="3" fill="#ffffff" opacity="0.5"/>')
    b.append('<rect x="46" y="640" width="288" height="92" rx="34" fill="#ffffff" opacity="0.22"/>')
    for col in range(4):
        c1, c2 = _COLS[(col * 2 + 3) % len(_COLS)]
        gd, ic = _icono(62 + col * 68, 658, 56, c1, c2, col, f"bd{col}")
        d += gd
        b.append(ic)
    b += ['<rect x="140" y="744" width="100" height="6" rx="3" fill="#ffffff" opacity="0.85"/>',
          '<rect width="380" height="780" fill="url(#omtb_gl)" opacity="0.16"/>', '</g>']
    _g("telefono_movil_b", "".join(b), w, h, d)


# ================================================================== CUNA
def cuna(sombra=None):
    w, h = 760, 740
    d = (_lgu("omcu_m", 0, 0, 40, 0, ("0", "#f6d9a8"), ("0.5", "#e8bf84"), ("1", "#b88a52")) +
         lg("omcu_r", (0, "#f8dcae"), (1, "#c89a62")) +
         _rgu("omcu_os", 380, 250, 90, ("0", "#e8b880"), ("0.7", "#c88a52"), ("1", "#8a5a32")) +
         lg("omcu_mt", (0, "#eaf4fb"), (1, "#bcd4e6")) + lg("omcu_mn", (0, "#ffd6e0"), (1, "#f0a8bc")))
    poste = lambda x: (f'<rect x="{x-16}" y="250" width="32" height="440" rx="6" fill="url(#omcu_m)"/>'
                       f'<circle cx="{x}" cy="236" r="22" fill="url(#omcu_os)"/><circle cx="{x-6}" cy="230" r="7" fill="#fff3d8" opacity="0.6"/>')
    b = [_sc(380, 706, 330, 22, 0.4, sombra),
         # brazo del móvil
         '<path d="M660 250 L660 70 C660 40 620 30 520 40 L420 50" stroke="#e8ecf2" stroke-width="10" fill="none" stroke-linecap="round"/>',
         '<path d="M656 250 L656 72 C656 46 620 36 520 44" stroke="#ffffff" stroke-width="3" opacity="0.8" fill="none"/>',
         '<ellipse cx="400" cy="56" rx="38" ry="12" fill="#ffd34a"/><ellipse cx="400" cy="52" rx="30" ry="7" fill="#fff0a8"/>']
    cuelga = [(320, 140, "estrella", "#ffd34a"), (370, 170, "luna", "#fff3c0"), (430, 160, "nube", "#ffffff"), (480, 130, "bola", "#7ac8ff")]
    for (x, y, tipo, col) in cuelga:
        b.append(f'<path d="M400 60 Q{(x+400)/2:.0f} {60+20} {x} {y-20}" stroke="#c8ccd4" stroke-width="1.6" fill="none"/>')
        if tipo == "estrella":
            b.append(f'<polygon points="{_estrella(x, y, 22, 10)}" fill="{col}"/><polygon points="{_estrella(x-2, y-2, 10, 5)}" fill="#fff8d0" opacity="0.7"/>')
        elif tipo == "luna":
            b.append(f'<path d="M{x-6} {y-22} A22 22 0 1 0 {x+16} {y+14} A17 17 0 1 1 {x-6} {y-22} Z" fill="{col}"/>')
        elif tipo == "nube":
            b.append(f'<ellipse cx="{x}" cy="{y+6}" rx="28" ry="12" fill="{col}"/><circle cx="{x-8}" cy="{y-2}" r="13" fill="{col}"/><circle cx="{x+10}" cy="{y}" r="10" fill="{col}"/>'
                     f'<ellipse cx="{x}" cy="{y+12}" rx="24" ry="5" fill="#a8c0d8" opacity="0.5"/>')
        else:
            b.append(f'<circle cx="{x}" cy="{y}" r="16" fill="{col}"/><circle cx="{x-5}" cy="{y-5}" r="5" fill="#ffffff" opacity="0.7"/>')
    b += [# fondo de la cuna (cara trasera, más oscura)
          '<rect x="104" y="300" width="552" height="16" rx="5" fill="#a8784a"/>',
          *[f'<rect x="{126+i*46}" y="316" width="12" height="230" fill="#9a6a3e"/>' for i in range(12)],
          # colchón y manta
          '<path d="M104 470 L656 470 L656 560 L104 560 Z" fill="url(#omcu_mt)"/>',
          '<path d="M300 452 C380 440 520 446 640 470 L640 560 L290 560 Z" fill="url(#omcu_mn)"/>',
          *[f'<circle cx="{340+i*44}" cy="{500+(i%2)*26}" r="5" fill="#ffffff" opacity="0.8"/>' for i in range(7)],
          '<path d="M300 452 C380 440 520 446 640 470" stroke="#fff0f4" stroke-width="5" fill="none"/>',
          # osito sentado
          '<ellipse cx="200" cy="470" rx="56" ry="64" fill="url(#omcu_os)"/>',
          '<ellipse cx="200" cy="486" rx="32" ry="38" fill="#f0cfa0"/>',
          '<circle cx="200" cy="386" r="48" fill="url(#omcu_os)"/>',
          '<circle cx="160" cy="348" r="18" fill="#c88a52"/><circle cx="160" cy="348" r="9" fill="#f0cfa0"/>',
          '<circle cx="240" cy="348" r="18" fill="#c88a52"/><circle cx="240" cy="348" r="9" fill="#f0cfa0"/>',
          '<ellipse cx="200" cy="402" rx="20" ry="15" fill="#f0cfa0"/><ellipse cx="200" cy="396" rx="7" ry="5" fill="#3a2214"/>',
          '<path d="M200 401 L200 410 M192 412 Q200 418 208 412" stroke="#3a2214" stroke-width="2.5" fill="none" stroke-linecap="round"/>',
          '<circle cx="184" cy="378" r="5" fill="#1a1008"/><circle cx="216" cy="378" r="5" fill="#1a1008"/>',
          '<circle cx="185.5" cy="376.5" r="1.6" fill="#ffffff"/><circle cx="217.5" cy="376.5" r="1.6" fill="#ffffff"/>',
          '<path d="M176 428 L200 440 L224 428 L224 446 L200 436 L176 446 Z" fill="#7ac8ff"/>',
          '<ellipse cx="148" cy="470" rx="18" ry="30" transform="rotate(20 148 470)" fill="#c88a52"/>',
          '<ellipse cx="252" cy="470" rx="18" ry="30" transform="rotate(-20 252 470)" fill="#c88a52"/>',
          '<path d="M164 352 C176 340 196 336 214 340" stroke="#fff0d0" stroke-width="3" opacity="0.5" fill="none"/>',
          # barrote delantero y barandillas
          poste(100), poste(660),
          '<rect x="100" y="282" width="560" height="26" rx="10" fill="url(#omcu_r)"/>',
          '<path d="M110 286 L650 286" stroke="#fff3d8" stroke-width="4" opacity="0.7"/>',
          '<rect x="100" y="560" width="560" height="34" rx="8" fill="url(#omcu_r)"/>',
          '<path d="M110 566 L650 566" stroke="#fff3d8" stroke-width="3" opacity="0.6"/>',
          *[f'<rect x="{134+i*44}" y="308" width="14" height="252" rx="6" fill="url(#omcu_m)"/>' for i in range(12)],
          # patas
          '<rect x="88" y="594" width="24" height="96" rx="6" fill="#b88a52"/><rect x="648" y="594" width="24" height="96" rx="6" fill="#b88a52"/>',
          '<path d="M660 250 L660 300" stroke="#2ff3ff" stroke-width="0"/>']
    _g("cuna", "".join(b), w, h, d)


# ================================================================== FLOR BLANCA CON VELA
def flor_blanca(sombra=None):
    w, h = 560, 680
    r = random.Random(29)
    d = (lg("omfb_p", (0, "#ffffff"), (0.6, "#eef0f2"), (1, "#c8d0d8")) + lg("omfb_t", (0, "#6a8a4a"), (1, "#3a5a2a"), x2=1, y2=0) +
         lg("omfb_h", (0, "#7a9a5a"), (1, "#3a5a2a")) + lg("omfb_v", (0, "#fbf6ea"), (0.5, "#f2e8d4"), (1, "#c8b898"), x2=1, y2=0) +
         rg("omfb_fl", (0, "#fffbe0", 1), (0.3, "#ffd24a", 0.9), (1, "#ff8a1a", 0)) + rg("omfb_gl", (0, "#ffcf8a", 0.55), (1, "#ffcf8a", 0)))
    cx, cy = 230, 210
    b = [_sc(250, 652, 220, 16, 0.4, sombra),
         # tallo y hojas
         f'<path d="M{cx} {cy+30} C{cx+10} 360 {cx-20} 520 {cx-6} 650" stroke="url(#omfb_t)" stroke-width="10" fill="none" stroke-linecap="round"/>',
         f'<path d="M{cx-4} 520 C{cx-90} 470 {cx-150} 400 {cx-170} 330 C{cx-120} 380 {cx-60} 430 {cx-2} 470 Z" fill="url(#omfb_h)"/>',
         f'<path d="M{cx-4} 500 C{cx-80} 450 {cx-140} 390 {cx-170} 330" stroke="#bfe08a" stroke-width="2" opacity="0.5" fill="none"/>',
         f'<path d="M{cx} 440 C{cx+80} 400 {cx+120} 330 {cx+130} 270 C{cx+90} 330 {cx+50} 370 {cx+2} 400 Z" fill="url(#omfb_h)"/>',
         f'<path d="M{cx} 600 C{cx+60} 580 {cx+110} 540 {cx+130} 500 C{cx+90} 540 {cx+50} 560 {cx-2} 570 Z" fill="#4a6a34"/>',
         f'<circle cx="{cx}" cy="{cy}" r="150" fill="#ffffff" opacity="0.14" filter="url(#blur20)"/>']
    # 6 pétalos: 3 de atrás (más grises) y 3 delante
    def petalo(ang, L, Wp, fill, op=1):
        a = math.radians(ang)
        ex, ey = cx + math.cos(a) * L, cy + math.sin(a) * L
        nx, ny = -math.sin(a) * Wp, math.cos(a) * Wp
        tipx, tipy = ex + math.cos(a + 0.6) * 18, ey + math.sin(a + 0.6) * 18
        p = (f"M{cx:.0f} {cy:.0f} C{cx+math.cos(a)*L*0.4+nx:.0f} {cy+math.sin(a)*L*0.4+ny:.0f} {ex+nx*0.6:.0f} {ey+ny*0.6:.0f} {tipx:.0f} {tipy:.0f} "
             f"C{ex-nx*0.5:.0f} {ey-ny*0.5:.0f} {cx+math.cos(a)*L*0.4-nx:.0f} {cy+math.sin(a)*L*0.4-ny:.0f} {cx:.0f} {cy:.0f} Z")
        return (f'<path d="{p}" fill="{fill}" opacity="{op}"/>'
                f'<path d="M{cx:.0f} {cy:.0f} Q{cx+math.cos(a)*L*0.5+nx*0.15:.0f} {cy+math.sin(a)*L*0.5+ny*0.15:.0f} {ex:.0f} {ey:.0f}" stroke="#b8c4cc" stroke-width="2" opacity="0.6" fill="none"/>'
                f'<path d="M{cx+math.cos(a)*20:.0f} {cy+math.sin(a)*20:.0f} L{cx+math.cos(a)*L*0.35:.0f} {cy+math.sin(a)*L*0.35:.0f}" stroke="#c8e0a0" stroke-width="7" opacity="0.5" stroke-linecap="round"/>')
    for ang in (-150, -30, 90):
        b.append(petalo(ang, 140, 48, "#dfe4ea"))
    for ang in (-90, 30, 150):
        b.append(petalo(ang, 150, 52, "url(#omfb_p)"))
    for ang in (-90, 30, 150):
        a = math.radians(ang)
        b.append(f'<path d="M{cx+math.cos(a)*30:.0f} {cy+math.sin(a)*30:.0f} L{cx+math.cos(a)*120:.0f} {cy+math.sin(a)*120:.0f}" stroke="#ffffff" stroke-width="4" opacity="0.8" stroke-linecap="round"/>')
    # estambres
    for k in range(6):
        a = math.radians(-120 + k * 22)
        ex, ey = cx + math.cos(a) * 80, cy + math.sin(a) * 80 + 20
        b.append(f'<path d="M{cx} {cy} Q{cx+math.cos(a)*40:.0f} {cy+math.sin(a)*40-10:.0f} {ex:.0f} {ey:.0f}" stroke="#d8e8b0" stroke-width="2.5" fill="none"/>'
                 f'<ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="8" ry="4" transform="rotate({math.degrees(a)+90:.0f} {ex:.0f} {ey:.0f})" fill="#c8782a"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="10" fill="#b8d07a"/>')
    # vela
    vx = 440
    b += [f'<circle cx="{vx}" cy="470" r="110" fill="url(#omfb_gl)"/>',
          f'<path d="M{vx-38} 520 L{vx-38} 640 A38 10 0 0 0 {vx+38} 640 L{vx+38} 520 Z" fill="url(#omfb_v)"/>',
          f'<ellipse cx="{vx}" cy="520" rx="38" ry="10" fill="#fffaf0"/><ellipse cx="{vx}" cy="521" rx="30" ry="6" fill="#f0e2c4"/>',
          f'<path d="M{vx-20} 522 C{vx-22} 540 {vx-18} 552 {vx-22} 560" stroke="#fffaf0" stroke-width="6" stroke-linecap="round" fill="none"/>',
          f'<path d="M{vx} 520 L{vx} 506" stroke="#2a2018" stroke-width="2.5"/>',
          f'<path d="M{vx} 466 Q{vx+11} 492 {vx} 506 Q{vx-11} 492 {vx} 466 Z" fill="url(#omfb_fl)"/>',
          f'<path d="M{vx} 482 Q{vx+4} 496 {vx} 504 Q{vx-4} 496 {vx} 482 Z" fill="#ffffff"/>',
          f'<path d="M{vx-38} 530 L{vx-38} 640" stroke="#ffffff" stroke-width="3" opacity="0.6"/>']
    _g("flor_blanca", "".join(b), w, h, d)


# ================================================================== PERIÓDICO
def periodico(sombra=None):
    w, h = 720, 560
    r = random.Random(31)
    d = (lg("ompe_p", (0, "#f4f0e6"), (0.5, "#ebe6d8"), (1, "#d8d0bc"), x2=1, y2=1) + lg("ompe_f", (0, "#bdbdbd"), (0.5, "#8a8a8a"), (1, "#5a5a5a"), x2=1, y2=1) +
         _lgu("ompe_pl", 0, 250, 0, 300, ("0", "#000", 0), ("0.5", "#000", 0.16), ("1", "#000", 0)) +
         '<clipPath id="ompe_cl"><path d="M80 60 L640 40 L660 500 L96 520 Z"/></clipPath>')
    b = [_sc(370, 528, 300, 18, 0.35, sombra),
         '<g filter="url(#sombra)"><path d="M98 80 L660 56 L676 512 L110 534 Z" fill="#d8d0bc"/>',
         '<path d="M80 60 L640 40 L660 500 L96 520 Z" fill="url(#ompe_p)"/></g>', '<g clip-path="url(#ompe_cl)" transform="">',
         '<g transform="rotate(-2 370 280)">',
         '<rect x="110" y="72" width="500" height="44" fill="#2a2a2a"/>',
         '<path d="M110 126 L610 126 M110 131 L610 131" stroke="#4a4a4a" stroke-width="2"/>',
         '<rect x="110" y="146" width="420" height="26" fill="#6a6a6a"/><rect x="110" y="182" width="330" height="26" fill="#6a6a6a"/>',
         '<rect x="110" y="222" width="260" height="170" fill="url(#ompe_f)"/>',
         '<path d="M110 340 C160 300 200 320 240 290 C290 260 330 300 370 280 L370 392 L110 392 Z" fill="#4a4a4a"/>',
         '<circle cx="320" cy="260" r="20" fill="#dcdcdc"/>',
         '<rect x="110" y="222" width="260" height="170" fill="none" stroke="#3a3a3a" stroke-width="2"/>',
         '<rect x="110" y="398" width="200" height="6" fill="#9a9a9a"/>']
    for col, (x0, y0, y1, ancho) in enumerate([(390, 222, 500, 100), (510, 222, 500, 100), (110, 416, 500, 120), (250, 416, 500, 120)]):
        y = y0
        while y < y1:
            L = ancho if r.random() > 0.15 else ancho * r.uniform(0.4, 0.8)
            b.append(f'<rect x="{x0}" y="{y}" width="{L:.0f}" height="5" fill="#8a8a8a" opacity="0.7"/>')
            y += 11
            if r.random() < 0.08:
                b.append(f'<rect x="{x0}" y="{y+2}" width="{ancho*0.7:.0f}" height="9" fill="#5a5a5a"/>')
                y += 18
    b += ['<path d="M380 140 L380 500" stroke="#9a9a9a" stroke-width="1"/>', '</g>',
          '<rect x="0" y="0" width="720" height="560" fill="url(#ompe_pl)"/>',
          '<rect width="720" height="560" fill="#fff" filter="url(#papel)" opacity="0.25"/>', _gr("ompe_cl", w, h, 0.8), '</g>',
          '<path d="M80 60 L640 40" stroke="#ffffff" stroke-width="3" opacity="0.8"/>',
          '<path d="M88 276 L650 262" stroke="#ffffff" stroke-width="2" opacity="0.6"/>']
    _g("periodico", "".join(b), w, h, d)


# ================================================================== MASCARILLA
def mascarilla():
    w, h = 680, 400
    d = (lg("omma_c", (0, "#a8d8f6"), (0.5, "#7ec0ea"), (1, "#4f94c8")) +
         '<clipPath id="omma_cl"><path d="M150 90 C260 70 420 70 530 90 C548 160 548 250 530 310 C420 340 260 340 150 310 C132 250 132 160 150 90 Z"/></clipPath>')
    m = "M150 90 C260 70 420 70 530 90 C548 160 548 250 530 310 C420 340 260 340 150 310 C132 250 132 160 150 90 Z"
    b = ['<path d="M150 110 C40 60 10 200 40 270 C60 320 120 320 150 290" stroke="#f2f6fa" stroke-width="9" fill="none" stroke-linecap="round"/>',
         '<path d="M530 110 C640 60 670 200 640 270 C620 320 560 320 530 290" stroke="#f2f6fa" stroke-width="9" fill="none" stroke-linecap="round"/>',
         '<path d="M150 112 C46 66 18 200 44 266" stroke="#c8d4e0" stroke-width="3" fill="none" opacity="0.7"/>',
         f'<g filter="url(#sombra)"><path d="{m}" fill="url(#omma_c)"/></g>', '<g clip-path="url(#omma_cl)">']
    for k, y in enumerate((150, 205, 260)):  # pliegues
        b.append(f'<path d="M130 {y} C260 {y-14} 420 {y-14} 550 {y}" stroke="#2f6fa8" stroke-width="9" opacity="0.35" fill="none" filter="url(#blur8)"/>'
                 f'<path d="M130 {y} C260 {y-14} 420 {y-14} 550 {y}" stroke="#3a7ab0" stroke-width="3" opacity="0.7" fill="none"/>'
                 f'<path d="M130 {y-8} C260 {y-22} 420 {y-22} 550 {y-8}" stroke="#e8f6ff" stroke-width="4" opacity="0.55" fill="none"/>')
    b += ['<rect x="150" y="80" width="380" height="18" fill="#f2f6fa" opacity="0.85"/>',
          '<rect x="260" y="84" width="160" height="7" rx="3" fill="#ffffff"/>',
          '<path d="M140 310 C260 340 420 340 540 310 L540 330 L140 330 Z" fill="#f2f6fa" opacity="0.8"/>',
          '<rect x="138" y="80" width="18" height="260" fill="#f2f6fa" opacity="0.8"/><rect x="524" y="80" width="18" height="260" fill="#e2eaf2" opacity="0.8"/>',
          _gr("omma_cl", w, h, 0.9),
          '<rect width="680" height="400" fill="#fff" filter="url(#papel)" opacity="0.12"/>', '</g>',
          '<path d="M530 100 C546 170 546 240 530 300" stroke="#2ff3ff" stroke-width="2" opacity="0.4" fill="none"/>']
    _g("mascarilla", "".join(b), w, h, d)


# ================================================================== MICRÓFONOS, CÁMARA, DESTELLO
def _microfono(nombre, c1, c2, c3):
    w, h = 260, 800
    r = random.Random(37)
    d = (_rgu(f"{nombre}_e", 108, 76, 90, ("0", "#6a6e76"), ("0.6", "#2e3036"), ("1", "#0e0f12")) +
         _lgu(f"{nombre}_f", 64, 0, 196, 0, ("0", c3), ("0.3", c1), ("1", c2)) +
         _lgu(f"{nombre}_m", 96, 0, 164, 0, ("0", "#4a4e56"), ("0.3", "#1a1c20"), ("0.8", "#0a0b0d"), ("1", "#3a3e46")) +
         _lgu(f"{nombre}_p", 112, 0, 148, 0, ("0", "#e8ecf2"), ("0.4", "#9aa3ae"), ("1", "#4a525e")) +
         f'<clipPath id="{nombre}_cl"><circle cx="130" cy="96" r="78"/></clipPath>')
    b = [f'<rect x="114" y="440" width="32" height="350" rx="8" fill="url(#{nombre}_p)"/>',
         *[f'<rect x="110" y="{600+k*16}" width="40" height="8" rx="3" fill="#2a2e34"/>' for k in range(6)],
         f'<rect x="108" y="776" width="44" height="18" rx="6" fill="#1a1c20"/>',
         f'<path d="M98 250 L162 250 L150 470 L110 470 Z" fill="url(#{nombre}_m)"/>',
         f'<path d="M108 260 L114 460" stroke="#ffffff" stroke-width="3" opacity="0.25"/>',
         f'<circle cx="130" cy="96" r="78" fill="url(#{nombre}_e)"/>', f'<g clip-path="url(#{nombre}_cl)">']
    for yy in range(20, 180, 9):
        for xx in range(50, 212, 9):
            off = 4.5 if (yy // 9) % 2 else 0
            b.append(f'<circle cx="{xx+off}" cy="{yy}" r="1.6" fill="#000" opacity="0.45"/>')
    b += [f'<circle cx="104" cy="66" r="40" fill="#ffffff" opacity="0.12" filter="url(#blur8)"/>', _gr(f"{nombre}_cl", w, h), '</g>',
          '<path d="M200 70 A78 78 0 0 1 176 158" stroke="#2ff3ff" stroke-width="3" opacity="0.45" fill="none"/>',
          # cubo de color (sin logotipo)
          f'<path d="M64 168 L196 168 L196 258 L64 258 Z" fill="url(#{nombre}_f)"/>',
          f'<path d="M64 168 L84 150 L216 150 L196 168 Z" fill="{c3}"/>',
          f'<path d="M196 168 L216 150 L216 240 L196 258 Z" fill="{c2}" opacity="0.85"/><path d="M196 168 L216 150 L216 240 L196 258 Z" fill="#000" opacity="0.25"/>',
          '<path d="M66 170 L194 170" stroke="#ffffff" stroke-width="2.5" opacity="0.6"/>',
          '<rect x="84" y="190" width="92" height="46" rx="8" fill="#ffffff" opacity="0.14"/>']
    _g(nombre, "".join(b), w, h, d)


def camara_flash():
    w, h = 660, 660
    d = (_lgu("omcf_c", 0, 300, 0, 620, ("0", "#3a3c42"), ("0.15", "#1e2024"), ("1", "#0c0d10")) +
         _rgu("omcf_l", 300, 420, 140, ("0", "#3a4a8a"), ("0.4", "#1a2050"), ("0.75", "#0a0c1a"), ("1", "#000")) +
         _lgu("omcf_r", 180, 0, 480, 0, ("0", "#2a2c30"), ("0.3", "#5a5e66"), ("0.5", "#1a1c20"), ("1", "#3a3e46")) +
         lg("omcf_fl", (0, "#ffffff"), (1, "#d8e4f0")) + _lgu("omcf_fh", 0, 0, 0, 200, ("0", "#3a3c42"), ("1", "#141518")) +
         rg("omcf_gl", (0, "#e8f2ff", 0.7), (1, "#e8f2ff", 0)))
    b = ['<g filter="url(#sombra)">',
         # flash encima
         '<rect x="250" y="190" width="100" height="60" rx="8" fill="#1a1b1e"/>',
         '<rect x="220" y="30" width="160" height="160" rx="16" fill="url(#omcf_fh)"/>',
         '<rect x="232" y="44" width="136" height="90" rx="8" fill="url(#omcf_fl)"/>',
         *[f'<path d="M236 {52+k*12} L364 {52+k*12}" stroke="#b8c8d8" stroke-width="1.5" opacity="0.7"/>' for k in range(7)],
         '<rect x="240" y="150" width="60" height="16" rx="4" fill="#2a2c30"/><circle cx="350" cy="158" r="6" fill="#ff5a3a"/>',
         # cuerpo
         '<path d="M70 300 L230 300 L250 250 L370 250 L390 300 L590 300 C610 300 620 310 620 330 L620 600 C620 616 610 624 594 624 L86 624 C70 624 60 616 60 600 L60 316 C60 306 64 300 70 300 Z" fill="url(#omcf_c)"/>',
         '<path d="M520 300 L590 300 C610 300 620 310 620 330 L620 600 C620 616 610 624 594 624 L520 624 C540 520 540 400 520 300 Z" fill="#2a2c30"/>',
         *[f'<path d="M{532+k*6} 330 L{532+k*6} 600" stroke="#000" stroke-width="2" opacity="0.4"/>' for k in range(12)],
         '<path d="M70 304 L230 304 L250 254 L370 254 L390 304 L590 304" stroke="#8a8e96" stroke-width="2.5" opacity="0.7" fill="none"/>',
         '<rect x="90" y="270" width="70" height="30" rx="6" fill="#2a2c30"/><rect x="460" y="276" width="56" height="24" rx="12" fill="#2a2c30"/>',
         '<circle cx="488" cy="288" r="8" fill="#5a5e66"/>',
         # objetivo
         '<circle cx="300" cy="440" r="176" fill="url(#omcf_r)"/>',
         '<circle cx="300" cy="440" r="160" fill="#0e0f12"/>',
         *[f'<path d="M{300+math.cos(a)*150:.0f} {440+math.sin(a)*150:.0f} L{300+math.cos(a)*166:.0f} {440+math.sin(a)*166:.0f}" stroke="#3a3e46" stroke-width="3"/>' for a in [k*math.pi/30 for k in range(60)]],
         '<circle cx="300" cy="440" r="136" fill="#1a1c20" stroke="#4a4e56" stroke-width="3"/>',
         '<circle cx="300" cy="440" r="112" fill="url(#omcf_l)"/>',
         '<circle cx="300" cy="440" r="70" fill="none" stroke="#5a6aba" stroke-width="2" opacity="0.5"/>',
         '<circle cx="300" cy="440" r="40" fill="#05060a"/>',
         '<path d="M240 390 A80 80 0 0 1 320 360" stroke="#ffffff" stroke-width="10" opacity="0.5" fill="none" stroke-linecap="round"/>',
         '<circle cx="250" cy="400" r="12" fill="#ffffff" opacity="0.7"/><circle cx="350" cy="480" r="7" fill="#a8b8ff" opacity="0.5"/>',
         '<path d="M180 540 A160 160 0 0 0 440 540" stroke="#ff3df2" stroke-width="3" opacity="0.4" fill="none"/>',
         '</g>',
         '<rect x="60" y="360" width="10" height="40" rx="3" fill="#5a5e66"/><rect x="610" y="360" width="10" height="40" rx="3" fill="#5a5e66"/>']
    _g("camara_flash", "".join(b), w, h, d)


def destello():
    w = h = 560
    c = 280
    d = rg("omde_g", (0, "#ffffff", 1), (0.12, "#ffffff", 0.95), (0.35, "#e8f4ff", 0.45), (1, "#bfe0ff", 0)) + \
        rg("omde_w", (0, "#fff8e0", 0.6), (1, "#fff8e0", 0))
    b = [f'<circle cx="{c}" cy="{c}" r="270" fill="url(#omde_w)"/>', f'<circle cx="{c}" cy="{c}" r="200" fill="url(#omde_g)"/>']
    for k in range(8):
        a = math.radians(k * 45)
        L = 270 if k % 2 == 0 else 150
        wd = 18 if k % 2 == 0 else 11
        ex, ey = c + math.cos(a) * L, c + math.sin(a) * L
        nx, ny = -math.sin(a) * wd, math.cos(a) * wd
        b.append(f'<path d="M{c+nx:.0f} {c+ny:.0f} L{ex:.0f} {ey:.0f} L{c-nx:.0f} {c-ny:.0f} Z" fill="#ffffff" opacity="0.9"/>')
    for k in range(16):
        a = math.radians(k * 22.5 + 11)
        L = 120 + (k % 3) * 30
        b.append(f'<path d="M{c} {c} L{c+math.cos(a)*L:.0f} {c+math.sin(a)*L:.0f}" stroke="#e8f4ff" stroke-width="2" opacity="0.5"/>')
    b += [f'<circle cx="{c}" cy="{c}" r="48" fill="#ffffff"/>',
          f'<circle cx="{c+120}" cy="{c+90}" r="14" fill="#bfe0ff" opacity="0.5"/><circle cx="{c+170}" cy="{c+130}" r="8" fill="#ffe8bf" opacity="0.5"/>']
    _g("destello", "".join(b), w, h, d)


# ================================================================== DUCHA
def ducha():
    w, h = 640, 860
    r = random.Random(41)
    d = (_lgu("omdu_t", 0, 0, 0, 40, ("0", "#f4f6fa"), ("0.4", "#a8b0bc"), ("1", "#4a525e")) +
         _lgu("omdu_tv", 0, 0, 40, 0, ("0", "#f4f6fa"), ("0.4", "#a8b0bc"), ("1", "#4a525e")) +
         _rgu("omdu_c", 290, 230, 160, ("0", "#ffffff"), ("0.5", "#c8d0da"), ("1", "#5a6270")) +
         lg("omdu_ag", (0, "#e8f8ff"), (1, "#bfe8ff00")))
    b = ['<path d="M0 60 L300 60 C330 60 340 70 340 100 L340 150" stroke="url(#omdu_t)" stroke-width="26" fill="none"/>',
         '<path d="M0 54 L300 54 C324 54 334 64 334 92" stroke="#ffffff" stroke-width="4" opacity="0.7" fill="none"/>',
         '<rect x="316" y="140" width="48" height="40" rx="8" fill="url(#omdu_tv)"/>',
         # alcachofa vista desde abajo en ángulo
         '<path d="M220 176 L460 176 L480 246 L200 246 Z" fill="#8a929e"/>',
         '<ellipse cx="340" cy="180" rx="120" ry="20" fill="#dfe4ea"/>',
         '<ellipse cx="340" cy="246" rx="140" ry="32" fill="url(#omdu_c)"/>',
         '<path d="M206 236 C260 210 420 210 474 236" stroke="#ffffff" stroke-width="4" opacity="0.8" fill="none"/>']
    agujeros = []
    for ring in range(4):
        n = 6 + ring * 6
        for k in range(n):
            a = k / n * 2 * math.pi
            x, y = 340 + math.cos(a) * ring * 34, 246 + math.sin(a) * ring * 7.5
            agujeros.append((x, y))
            b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#3a4250"/>')
    # chorros
    for (x, y) in agujeros:
        sp = (x - 340) / 120
        L = r.uniform(440, 560)
        ex = x + sp * 140 + r.uniform(-10, 10)
        b.append(f'<path d="M{x:.0f} {y+4:.0f} Q{x+sp*40:.0f} {y+L*0.5:.0f} {ex:.0f} {y+L:.0f}" stroke="#d8f2ff" stroke-width="{r.uniform(1.6,3):.1f}" opacity="{r.uniform(0.45,0.85):.2f}" fill="none" stroke-dasharray="{r.uniform(30,80):.0f} {r.uniform(6,20):.0f}"/>')
    for _ in range(80):
        x = r.uniform(200, 480)
        y = r.uniform(300, 840)
        x += (x - 340) * (y - 250) / 900
        rr = r.uniform(2, 5)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rr*0.7:.1f}" ry="{rr:.1f}" fill="#e8f8ff" opacity="{r.uniform(0.5,0.95):.2f}"/>'
                 f'<circle cx="{x-rr*0.2:.1f}" cy="{y-rr*0.3:.1f}" r="{rr*0.3:.1f}" fill="#ffffff"/>')
    # vapor
    for (x, y, s) in ((140, 520, 120), (520, 460, 110), (120, 760, 130), (530, 720, 120), (330, 820, 110)):
        b.append(f'<circle cx="{x}" cy="{y}" r="{s}" fill="#ffffff" opacity="0.22" filter="url(#blur40)"/>')
    for k in range(6):
        x = 120 + k * 80
        b.append(f'<path d="M{x} 840 C{x-30} 760 {x+30} 700 {x} 620 C{x-20} 560 {x+20} 520 {x} 470" stroke="#ffffff" stroke-width="16" opacity="0.18" fill="none" filter="url(#blur8)"/>')
    _g("ducha", "".join(b), w, h, d)


# ================================================================== VENTANA (día / noche)
def _ventana(nombre, noche=False):
    w, h = 760, 900
    r = random.Random(43)
    if noche:
        cielo = (("0", "#0b0f24"), ("0.6", "#1b1340"), ("1", "#2a3a6a"))
        luz = "#9fb8ff"
    else:
        cielo = (("0", "#6fb6e8"), ("1", "#d6eefa"))
        luz = "#fff0c0"
    d = (_lgu(f"{nombre}_s", 0, 90, 0, 600, *cielo) +
         _lgu(f"{nombre}_m", 0, 0, 0, 40, ("0", "#c08a52"), ("0.5", "#8a5a32"), ("1", "#5a3a1e")) +
         _lgu(f"{nombre}_mv", 0, 0, 40, 0, ("0", "#c08a52"), ("0.5", "#8a5a32"), ("1", "#5a3a1e")) +
         _lgu(f"{nombre}_l", 0, 600, 0, 900, ("0", luz, 0.45 if not noche else 0.22), ("1", luz, 0)) +
         lg(f"{nombre}_v", (0, "#ffffff"), (0.5, "#ffffff00"), x2=1, y2=1) +
         f'<clipPath id="{nombre}_cl"><rect x="190" y="100" width="380" height="500"/></clipPath>')
    b = [f'<path d="M190 600 L570 600 L760 900 L0 900 Z" fill="url(#{nombre}_l)"/>',
         # marco exterior (jamba) con profundidad
         f'<rect x="160" y="70" width="440" height="560" fill="#6a4426"/>',
         f'<rect x="190" y="100" width="380" height="500" fill="url(#{nombre}_s)"/>', f'<g clip-path="url(#{nombre}_cl)">']
    if noche:
        for _ in range(90):
            b.append(f'<circle cx="{r.uniform(190,570):.0f}" cy="{r.uniform(100,500):.0f}" r="{r.uniform(0.7,2.2):.1f}" fill="#ffffff" opacity="{r.uniform(0.4,1):.2f}"/>')
        b += ['<circle cx="460" cy="200" r="70" fill="#dfe8ff" opacity="0.18" filter="url(#blur20)"/>',
              '<circle cx="460" cy="200" r="34" fill="#f2f0dc"/><circle cx="448" cy="192" r="6" fill="#cfcab0" opacity="0.6"/><circle cx="470" cy="214" r="4" fill="#cfcab0" opacity="0.6"/>',
              '<path d="M190 520 C260 490 330 510 400 486 C470 466 520 496 570 480 L570 600 L190 600 Z" fill="#141a30"/>',
              '<path d="M190 556 C280 540 380 556 570 536 L570 600 L190 600 Z" fill="#0a0e1c"/>',
              *[f'<rect x="{x}" y="{y}" width="6" height="8" fill="#ffcf8a" opacity="0.8"/>' for x, y in ((250, 540), (300, 548), (470, 520), (520, 530))]]
    else:
        b += ['<circle cx="480" cy="170" r="90" fill="#fff6d0" opacity="0.6" filter="url(#blur20)"/>',
              '<circle cx="480" cy="170" r="30" fill="#fffbe8"/>',
              _nubes(r, 0, 0, 0)]
        for (x, y, k) in ((260, 200, 1.0), (420, 290, 0.8), (540, 240, 0.6)):
            b.append(f'<g><ellipse cx="{x}" cy="{y}" rx="{56*k:.0f}" ry="{13*k:.0f}" fill="#ffffff"/><circle cx="{x-20*k:.0f}" cy="{y-8*k:.0f}" r="{17*k:.0f}" fill="#ffffff"/>'
                     f'<circle cx="{x+12*k:.0f}" cy="{y-16*k:.0f}" r="{22*k:.0f}" fill="#ffffff"/><ellipse cx="{x}" cy="{y+7*k:.0f}" rx="{50*k:.0f}" ry="{5*k:.0f}" fill="#a8c4dc" opacity="0.5"/></g>')
        b += ['<path d="M190 500 C260 470 330 490 400 466 C470 446 520 476 570 460 L570 600 L190 600 Z" fill="#a8c0a0"/>',
              '<path d="M190 540 C280 520 380 540 570 516 L570 600 L190 600 Z" fill="#c9a26b"/>']
        for k in range(9):
            x = 200 + k * 44 + r.uniform(-10, 10)
            y = 548 - (x - 190) * 0.05 + r.uniform(-6, 6)
            b.append(f'<path d="M{x:.0f} {y+14:.0f} L{x:.0f} {y:.0f}" stroke="#4a3a22" stroke-width="3"/><ellipse cx="{x:.0f}" cy="{y-4:.0f}" rx="14" ry="10" fill="#5b6b3a"/>'
                     f'<ellipse cx="{x-4:.0f}" cy="{y-7:.0f}" rx="6" ry="4" fill="#8a9a5a" opacity="0.7"/>')
    b += [f'<rect x="190" y="100" width="380" height="500" fill="#000" opacity="0.0"/>', '</g>',
          # sombra interior en la jamba (profundidad)
          '<path d="M190 100 L570 100 L548 122 L212 122 L212 600 L190 600 Z" fill="#000" opacity="0.28"/>',
          # hojas abiertas hacia dentro (en perspectiva)
          f'<path d="M190 100 L60 50 L60 690 L190 600 Z" fill="url(#{nombre}_mv)"/>',
          f'<path d="M84 90 L172 122 L172 580 L84 640 Z" fill="{"#1a2240" if noche else "#bfe0f4"}"/>',
          f'<path d="M128 106 L128 610 M84 360 L172 352" stroke="#7a4e2a" stroke-width="8"/>',
          f'<path d="M90 110 L120 120 L92 260 Z" fill="#ffffff" opacity="{0.15 if noche else 0.45}"/>',
          f'<path d="M570 100 L700 50 L700 690 L570 600 Z" fill="url(#{nombre}_mv)"/>',
          f'<path d="M676 90 L588 122 L588 580 L676 640 Z" fill="{"#1a2240" if noche else "#bfe0f4"}"/>',
          f'<path d="M632 106 L632 610 M676 360 L588 352" stroke="#7a4e2a" stroke-width="8"/>',
          f'<path d="M670 110 L640 120 L668 260 Z" fill="#ffffff" opacity="{0.15 if noche else 0.45}"/>',
          '<circle cx="168" cy="352" r="6" fill="#d8b860"/><circle cx="592" cy="352" r="6" fill="#d8b860"/>',
          # marco con vetas
          f'<rect x="150" y="60" width="460" height="40" fill="url(#{nombre}_m)"/>',
          f'<rect x="150" y="60" width="40" height="560" fill="url(#{nombre}_mv)"/><rect x="570" y="60" width="40" height="560" fill="url(#{nombre}_mv)"/>',
          _vetas(r, 150, 62, 610, 98, 5, "#3a2412", 0.4),
          '<path d="M150 60 L610 60" stroke="#e8b880" stroke-width="3" opacity="0.7"/>',
          # alféizar
          '<path d="M120 600 L640 600 L670 640 L90 640 Z" fill="#a8784a"/>',
          '<rect x="90" y="640" width="580" height="22" fill="#6a4426"/>',
          '<path d="M120 602 L640 602" stroke="#f0c890" stroke-width="3" opacity="0.8"/>',
          # maceta en el alféizar
          '<path d="M480 560 L540 560 L532 620 L488 620 Z" fill="#c8603a"/><rect x="474" y="552" width="72" height="14" rx="4" fill="#d8704a"/>',
          '<path d="M510 552 C500 520 480 500 470 480 M510 552 C514 516 530 496 546 486 M510 552 C510 520 506 500 510 470" stroke="#3f6a2a" stroke-width="4" fill="none"/>',
          *[f'<ellipse cx="{x}" cy="{y}" rx="12" ry="6" transform="rotate({a} {x} {y})" fill="#5b8a3a"/>' for x, y, a in ((474, 486, -40), (544, 490, 30), (510, 474, 90), (488, 516, -20), (528, 512, 20))]]
    # haz de luz entrando
    if noche:
        b.append(f'<path d="M212 122 L548 122 L700 900 L60 900 Z" fill="url(#{nombre}_l)" opacity="0.5"/>')
    else:
        b.append(f'<path d="M212 122 L548 122 L760 900 L40 900 Z" fill="url(#{nombre}_l)" opacity="0.0"/>')
        for k in range(5):
            x0 = 230 + k * 70
            b.append(f'<path d="M{x0} 130 L{x0+40} 130 L{x0+120} 900 L{x0+20} 900 Z" fill="#fff6d0" opacity="0.12"/>')
    b.append(f'<rect x="190" y="100" width="380" height="500" fill="url(#{nombre}_v)" opacity="0.12"/>')
    _g(nombre, "".join(b), w, h, d)


# ================================================================== CALENDARIOS
def _calendario_taco(nombre, solo_hoja=False):
    w, h = 460, 560
    d = (lg("omct_h", (0, "#ffffff"), (1, "#ece6d8")) + lg("omct_r", (0, "#e0473a"), (1, "#a82a20")) +
         lg("omct_b", (0, "#8a6a4a"), (1, "#5a4028")) + lg("omct_m", (0, "#f4f6fa"), (1, "#8a929e"), x2=1, y2=0) +
         '<clipPath id="omct_cl"><path d="M50 110 L410 110 L410 490 C330 486 300 500 260 496 L50 496 Z"/></clipPath>')
    hoja = ['<path d="M50 110 L410 110 L410 490 C330 486 300 500 260 496 L50 496 Z" fill="url(#omct_h)"/>',
            '<rect x="50" y="110" width="360" height="74" fill="url(#omct_r)"/>',
            '<path d="M50 112 L410 112" stroke="#ff8a7a" stroke-width="3" opacity="0.7"/>',
            *[f'<circle cx="{60+k*14}" cy="118" r="2.6" fill="#7a1a12" opacity="0.7"/>' for k in range(26)],
            '<rect x="130" y="230" width="200" height="170" rx="18" fill="#000" opacity="0.04"/>',
            '<path d="M260 496 C300 500 330 486 410 490 L410 470 C370 478 320 470 260 496 Z" fill="#d8d0bc"/>',
            '<path d="M410 470 C370 478 320 470 260 496" stroke="#b8ae98" stroke-width="1.5" fill="none"/>',
            _gr("omct_cl", w, h, 0.7), '<g clip-path="url(#omct_cl)"><rect width="460" height="560" fill="#fff" filter="url(#papel)" opacity="0.12"/></g>']
    if solo_hoja:
        b = ['<g filter="url(#sombra)">'] + hoja + ['</g>']
    else:
        b = [_sc(230, 540, 200, 14, 0.4),
             '<g filter="url(#sombra)"><rect x="30" y="80" width="400" height="450" rx="10" fill="url(#omct_b)"/></g>',
             *[f'<path d="M{50+k*0.5:.1f} {500+k*4} L{410-k*0.5:.1f} {500+k*4}" stroke="{"#ffffff" if k % 2 == 0 else "#d8d0bc"}" stroke-width="3"/>' for k in range(6)],
             *[f'<rect x="{50}" y="{110+k*0}" width="360" height="{392+k*3}" fill="#e8e2d2"/>' for k in range(1)]]
        b += hoja + ['<rect x="30" y="70" width="400" height="44" rx="8" fill="#3a2e24"/>',
                     '<path d="M34 74 L426 74" stroke="#8a7a6a" stroke-width="2" opacity="0.7"/>',
                     '<rect x="110" y="56" width="16" height="64" rx="8" fill="url(#omct_m)"/><rect x="334" y="56" width="16" height="64" rx="8" fill="url(#omct_m)"/>']
    _g(nombre, "".join(b), w, h, d)


def calendario_diciembre():
    w, h = 600, 780
    r = random.Random(47)
    d = (lg("omcd_p", (0, "#ffffff"), (1, "#ece6d8")) + lg("omcd_s", (0, "#1a2a5a"), (0.7, "#5a7ab8"), (1, "#a8c4e8")) +
         lg("omcd_n", (0, "#ffffff"), (1, "#c8d8ec")) + lg("omcd_m", (0, "#f4f6fa"), (1, "#7a828e"), x2=1, y2=0) +
         '<clipPath id="omcd_cl"><rect x="60" y="80" width="480" height="300"/></clipPath>' +
         '<clipPath id="omcd_pc"><rect x="40" y="60" width="520" height="700" rx="8"/></clipPath>')
    b = ['<path d="M300 12 L170 70 M300 12 L430 70" stroke="#5a4a3a" stroke-width="3"/><circle cx="300" cy="12" r="8" fill="#8a7a6a"/>',
         '<g filter="url(#sombra)"><rect x="40" y="60" width="520" height="700" rx="8" fill="url(#omcd_p)"/></g>',
         '<rect x="60" y="80" width="480" height="300" fill="url(#omcd_s)"/>', '<g clip-path="url(#omcd_cl)">',
         '<circle cx="440" cy="140" r="26" fill="#f2f0dc"/><circle cx="440" cy="140" r="60" fill="#f2f0dc" opacity="0.15"/>',
         '<path d="M60 300 C160 250 240 280 320 250 C400 224 470 260 540 240 L540 380 L60 380 Z" fill="#dfe8f4"/>',
         '<path d="M60 340 C180 310 300 340 540 300 L540 380 L60 380 Z" fill="url(#omcd_n)"/>']
    for x, s in ((110, 1.0), (150, 0.7), (470, 0.9), (510, 1.1), (90, 0.6)):
        y = 330 if x < 300 else 300
        b.append(f'<path d="M{x} {y-100*s:.0f} L{x+36*s:.0f} {y:.0f} L{x-36*s:.0f} {y:.0f} Z" fill="#244a3a"/>'
                 f'<path d="M{x} {y-100*s:.0f} L{x+14*s:.0f} {y-60*s:.0f} L{x-14*s:.0f} {y-60*s:.0f} Z" fill="#ffffff"/>'
                 f'<path d="M{x-26*s:.0f} {y-30*s:.0f} Q{x} {y-40*s:.0f} {x+26*s:.0f} {y-30*s:.0f}" stroke="#ffffff" stroke-width="{5*s:.1f}" fill="none"/>')
    b += ['<path d="M260 300 L260 262 L300 236 L340 262 L340 300 Z" fill="#8a5a3a"/><path d="M252 266 L300 228 L348 266 L340 270 L300 240 L260 270 Z" fill="#ffffff"/>',
          '<rect x="290" y="270" width="18" height="18" fill="#ffcf8a"/><rect x="290" y="270" width="18" height="18" fill="#ffcf8a" opacity="0.5" filter="url(#blur8)"/>',
          *[f'<circle cx="{r.uniform(60,540):.0f}" cy="{r.uniform(80,380):.0f}" r="{r.uniform(1.2,3.5):.1f}" fill="#ffffff" opacity="{r.uniform(0.6,1):.2f}"/>' for _ in range(70)],
          '</g>',
          '<rect x="60" y="398" width="160" height="18" rx="4" fill="#c83a30"/>',
          '<rect x="60" y="424" width="90" height="8" rx="4" fill="#c9bfa8"/>']
    for c in range(7):
        b.append(f'<rect x="{60+c*68.6:.1f}" y="446" width="60" height="10" rx="3" fill="#b8b0a0" opacity="0.6"/>')
    for f in range(5):
        for c in range(7):
            x, y = 60 + c * 68.6, 466 + f * 56
            fill = "#f2e4e0" if c >= 5 else "#ffffff"
            b.append(f'<rect x="{x:.1f}" y="{y}" width="64" height="52" fill="{fill}" stroke="#d8d0bc" stroke-width="1.5"/>')
    b += [_gr("omcd_pc", w, h, 0.6),
          '<rect x="40" y="60" width="520" height="30" fill="#000" opacity="0.0"/>']
    for k in range(13):  # espiral
        x = 70 + k * 38
        b.append(f'<path d="M{x} 52 C{x-6} 62 {x-6} 78 {x} 86" stroke="url(#omcd_m)" stroke-width="5" fill="none"/><circle cx="{x}" cy="86" r="4" fill="#3a3a3a"/>')
    _g("calendario_diciembre", "".join(b), w, h, d)


# ================================================================== SOL Y LUNA
def sol_dibujo():
    w = h = 600
    c = 300
    d = (rg("omso_h", (0, "#fff2b0", 0.9), (0.4, "#ffcf8a", 0.45), (1, "#ffb15e", 0)) +
         _rgu("omso_d", 270, 270, 120, ("0", "#fffbe0"), ("0.45", "#ffe07a"), ("0.85", "#ffb84a"), ("1", "#f08a2a")) +
         lg("omso_r", (0, "#ffe07a"), (1, "#ff9a3a")))
    b = [f'<circle cx="{c}" cy="{c}" r="296" fill="url(#omso_h)"/>']
    for k in range(16):
        a = math.radians(k * 22.5)
        L = 250 if k % 2 == 0 else 190
        wd = 0.15 if k % 2 == 0 else 0.11
        b.append(f'<path d="M{c+math.cos(a-wd)*130:.1f} {c+math.sin(a-wd)*130:.1f} Q{c+math.cos(a)*L*0.8+math.cos(a+1.57)*10:.1f} {c+math.sin(a)*L*0.8+math.sin(a+1.57)*10:.1f} {c+math.cos(a)*L:.1f} {c+math.sin(a)*L:.1f} '
                 f'Q{c+math.cos(a)*L*0.8-math.cos(a+1.57)*10:.1f} {c+math.sin(a)*L*0.8-math.sin(a+1.57)*10:.1f} {c+math.cos(a+wd)*130:.1f} {c+math.sin(a+wd)*130:.1f} Z" fill="url(#omso_r)" opacity="0.92"/>')
    b += [f'<circle cx="{c}" cy="{c}" r="140" fill="#ffcf6a" opacity="0.5" filter="url(#blur20)"/>',
          f'<circle cx="{c}" cy="{c}" r="130" fill="url(#omso_d)"/>',
          f'<path d="M{c-90} {c+20} C{c-60} {c-40} {c} {c-30} {c+40} {c-80}" stroke="#ffffff" stroke-width="5" opacity="0.25" fill="none"/>',
          f'<path d="M{c-60} {c+80} C{c} {c+40} {c+60} {c+60} {c+100} {c+20}" stroke="#e8782a" stroke-width="5" opacity="0.25" fill="none"/>',
          f'<circle cx="{c-50}" cy="{c-50}" r="34" fill="#ffffff" opacity="0.35" filter="url(#blur8)"/>',
          f'<path d="M{c+80} {c+100} A130 130 0 0 0 {c+125} {c-40}" stroke="#ff6a2a" stroke-width="6" opacity="0.5" fill="none"/>']
    _g("sol_dibujo", "".join(b), w, h, d)


def luna_creciente():
    w, h = 480, 520
    r = random.Random(53)
    luna = "M300 40 A220 220 0 1 0 420 420 A180 180 0 1 1 300 40 Z"
    d = (_rgu("omlu_d", 140, 200, 300, ("0", "#fffbe8"), ("0.6", "#f2ecc8"), ("1", "#b8b090")) +
         rg("omlu_g", (0, "#fff6d0", 0.4), (1, "#fff6d0", 0)) + _clip("omlu_cl", luna))
    b = ['<circle cx="220" cy="260" r="250" fill="url(#omlu_g)"/>', f'<path d="{luna}" fill="url(#omlu_d)"/>', '<g clip-path="url(#omlu_cl)">']
    for (x, y, s) in ((120, 200, 26), (90, 320, 16), (170, 390, 22), (200, 110, 14), (60, 250, 10), (140, 290, 9), (250, 450, 12)):
        b.append(f'<circle cx="{x}" cy="{y}" r="{s}" fill="#b8b090" opacity="0.5"/><path d="M{x-s} {y} A{s} {s} 0 0 0 {x+s} {y}" stroke="#ffffff" stroke-width="2" opacity="0.5" fill="none"/>')
    b += [_gr("omlu_cl", w, h), '</g>',
          f'<path d="M300 40 A220 220 0 0 0 100 330" stroke="#ffffff" stroke-width="4" opacity="0.6" fill="none"/>',
          _destello_peq(400, 140, 12, "#fffbe8"), _destello_peq(440, 260, 8, "#fffbe8")]
    _g("luna_creciente", "".join(b), w, h, d)


# ================================================================== VERANO: BICI, BALÓN, HELADO
def bici_nino(sombra=None):
    w, h = 660, 460
    col = "#d8302a"
    b = [_sc(330, 430, 270, 16, 0.4, sombra),
         _rueda(170, 330, 92, "#2a2a2e", "#d8dce2", 14, 16), _rueda(490, 330, 92, "#2a2a2e", "#d8dce2", 14, 16),
         '<circle cx="170" cy="330" r="78" fill="none" stroke="#f4f4f4" stroke-width="4" opacity="0.7"/>',
         '<circle cx="490" cy="330" r="78" fill="none" stroke="#f4f4f4" stroke-width="4" opacity="0.7"/>',
         # ruedines
         '<path d="M170 330 L120 400" stroke="#9aa0a8" stroke-width="6"/><circle cx="116" cy="404" r="22" fill="#e8e8ec" stroke="#3a3a3e" stroke-width="6"/>',
         # cuadro
         f'<path d="M170 330 L300 340 L400 190 L250 190 Z" stroke="{col}" stroke-width="16" fill="none" stroke-linejoin="round"/>',
         f'<path d="M300 340 L232 166" stroke="{col}" stroke-width="16" stroke-linecap="round"/>',
         f'<path d="M400 190 L490 330 M400 190 L384 120" stroke="{col}" stroke-width="16" stroke-linecap="round"/>',
         '<path d="M172 324 L298 334 L396 186" stroke="#ff9a8a" stroke-width="4" opacity="0.7" fill="none"/>',
         '<path d="M252 184 L396 184" stroke="#ff9a8a" stroke-width="4" opacity="0.6"/>',
         # guardabarros
         '<path d="M68 300 A104 104 0 0 1 250 240" stroke="#f4f4f4" stroke-width="10" fill="none"/>',
         '<path d="M420 250 A104 104 0 0 1 590 290" stroke="#f4f4f4" stroke-width="10" fill="none"/>',
         # sillín y manillar
         '<path d="M196 160 L262 154 Q276 150 266 140 L210 140 Q190 142 196 160 Z" fill="#2a2a2e"/>',
         '<path d="M374 120 L400 104 Q420 96 440 110 L452 124" stroke="#d8dce2" stroke-width="9" fill="none" stroke-linecap="round"/>',
         '<rect x="440" y="116" width="34" height="18" rx="9" fill="#2a2a2e"/>',
         '<path d="M452 124 L476 112" stroke="#ff8ad8" stroke-width="3"/><path d="M452 128 L478 132" stroke="#4ac0ff" stroke-width="3"/>',
         # plato, biela, pedal
         '<circle cx="300" cy="340" r="28" fill="#9aa0a8"/><circle cx="300" cy="340" r="12" fill="#5a5e66"/>',
         '<path d="M300 340 L330 380" stroke="#3a3a3e" stroke-width="8" stroke-linecap="round"/><rect x="318" y="376" width="30" height="10" rx="3" fill="#2a2a2e"/>',
         '<path d="M300 340 L170 330" stroke="#3a3a3e" stroke-width="3"/>',
         # timbre
         '<circle cx="420" cy="116" r="9" fill="#ffd34a"/>']
    _g("bici_nino", "".join(b), w, h)


def balon_playa(sombra=None):
    w, h = 440, 470
    c, R = 220, 190
    d = (_rgu("omba_s", 160, 140, 260, ("0", "#ffffff", 0.6), ("0.4", "#ffffff", 0), ("0.8", "#000", 0.1), ("1", "#000", 0.4)) +
         f'<clipPath id="omba_cl"><circle cx="{c}" cy="{c}" r="{R}"/></clipPath>')
    cols = ["#e8483b", "#ffffff", "#ffd34a", "#3a8fd8", "#ffffff", "#2ab07a"]
    b = [_sc(c, 448, 150, 14, 0.4, sombra), f'<circle cx="{c}" cy="{c}" r="{R}" fill="#ffffff"/>', '<g clip-path="url(#omba_cl)">']
    # gajos: elipses verticales en perspectiva desde el polo superior
    for k in range(6):
        a0, a1 = -90 + k * 30, -90 + (k + 1) * 30
        x0 = c + R * math.sin(math.radians(a0))
        x1 = c + R * math.sin(math.radians(a1))
        rx0, rx1 = abs(R * math.sin(math.radians(a0))), abs(R * math.sin(math.radians(a1)))
        b.append(f'<path d="M{c} {c-R} A{rx0:.1f} {R} 0 0 {1 if a0 >= 0 else 0} {c} {c+R} A{rx1:.1f} {R} 0 0 {0 if a1 >= 0 else 1} {c} {c-R} Z" fill="{cols[k]}"/>')
    b += ['</g>', f'<circle cx="{c}" cy="{c}" r="{R}" fill="url(#omba_s)"/>',
          f'<ellipse cx="{c}" cy="{c-R+16}" rx="34" ry="18" fill="#ffffff"/><ellipse cx="{c}" cy="{c-R+14}" rx="14" ry="7" fill="#d8dce2"/>',
          f'<ellipse cx="{c-70}" cy="{c-90}" rx="40" ry="22" transform="rotate(-35 {c-70} {c-90})" fill="#ffffff" opacity="0.55"/>',
          f'<path d="M{c+120} {c+130} A{R} {R} 0 0 0 {c+180} {c-30}" stroke="#2ff3ff" stroke-width="3" opacity="0.4" fill="none"/>']
    _g("balon_playa", "".join(b), w, h, d)


def helado():
    w, h = 320, 600
    d = (lg("omhe_c", (0, "#f2c072"), (0.5, "#e0a050"), (1, "#a8702a"), x2=1, y2=0) +
         _rgu("omhe_b1", 140, 270, 100, ("0", "#fff4f8"), ("0.5", "#ffb8cc"), ("1", "#e07a9a")) +
         _rgu("omhe_b2", 145, 140, 90, ("0", "#f4fff8"), ("0.5", "#b8f0d0"), ("1", "#6ac89a")) +
         _clip("omhe_cl", "M60 310 L260 310 L166 590 L154 590 Z"))
    b = ['<path d="M60 310 L260 310 L166 590 L154 590 Z" fill="url(#omhe_c)"/>', '<g clip-path="url(#omhe_cl)">']
    for k in range(-6, 12):
        b.append(f'<path d="M{k*30} 300 L{k*30+200} 600" stroke="#8a5a1e" stroke-width="3" opacity="0.6"/>'
                 f'<path d="M{k*30+200} 300 L{k*30} 600" stroke="#8a5a1e" stroke-width="3" opacity="0.6"/>')
    b += [_gr("omhe_cl", w, h), '</g>',
          # bola inferior (fresa) con goterones
          '<path d="M52 300 C40 230 100 190 160 190 C220 190 280 230 268 300 C264 320 248 316 240 328 C232 340 222 330 214 322 C200 340 190 350 180 330 C170 316 150 322 136 330 C120 356 108 350 106 330 C90 320 70 330 52 300 Z" fill="url(#omhe_b1)"/>',
          '<path d="M80 240 C100 214 130 204 160 204" stroke="#ffffff" stroke-width="6" opacity="0.6" fill="none" stroke-linecap="round"/>',
          # bola superior (menta)
          '<path d="M76 180 C66 120 110 76 160 76 C210 76 254 120 244 180 C238 200 220 196 210 206 C196 214 184 200 170 208 C150 218 136 204 120 208 C100 212 84 202 76 180 Z" fill="url(#omhe_b2)"/>',
          '<path d="M100 120 C116 96 136 88 160 88" stroke="#ffffff" stroke-width="6" opacity="0.7" fill="none" stroke-linecap="round"/>',
          *[f'<path d="M{x} {y} l6 -3" stroke="{c}" stroke-width="4" stroke-linecap="round"/>' for x, y, c in ((120, 140, "#3a2a1a"), (180, 120, "#3a2a1a"), (200, 160, "#3a2a1a"), (140, 170, "#3a2a1a"), (110, 260, "#e8483b"), (200, 270, "#ffd34a"), (160, 240, "#4ac0ff"))],
          # cereza
          '<path d="M164 76 C170 50 186 36 200 30" stroke="#4a6a2a" stroke-width="3" fill="none"/>',
          '<circle cx="160" cy="62" r="20" fill="#d8202a"/><circle cx="153" cy="55" r="6" fill="#ffffff" opacity="0.7"/>',
          '<path d="M244 180 C238 200 220 196 210 206" stroke="#2ff3ff" stroke-width="0" fill="none"/>']
    _g("helado", "".join(b), w, h, d)


# ================================================================== TAZA Y PANTALLA
def taza_cafe(sombra=None):
    w, h = 480, 560
    d = (_lgu("omta_c", 90, 0, 370, 0, ("0", "#e8f4f4"), ("0.25", "#ffffff"), ("0.6", "#d8e8e8"), ("1", "#7aa0a8")) +
         _rgu("omta_cf", 230, 250, 140, ("0", "#c8905a"), ("0.6", "#7a4a22"), ("1", "#3a2210")))
    b = [_sc(240, 530, 190, 18, 0.45, sombra),
         '<path d="M360 300 C450 300 450 440 350 450" stroke="#e0ecec" stroke-width="30" fill="none"/>',
         '<path d="M360 300 C450 300 450 440 350 450" stroke="#7aa0a8" stroke-width="30" fill="none" opacity="0.35" stroke-dasharray="0 60 300"/>',
         '<path d="M90 250 L370 250 L350 490 C350 520 110 520 110 490 Z" fill="url(#omta_c)"/>',
         '<path d="M110 300 L350 300 L344 380 L116 380 Z" fill="#2a8a9e" opacity="0.85"/>',
         '<path d="M116 380 L344 380" stroke="#ffffff" stroke-width="3" opacity="0.6"/>',
         '<ellipse cx="230" cy="250" rx="140" ry="28" fill="#f4fafa"/>', '<ellipse cx="230" cy="252" rx="124" ry="20" fill="url(#omta_cf)"/>',
         '<ellipse cx="210" cy="248" rx="40" ry="7" fill="#e8c090" opacity="0.6"/>',
         '<path d="M130 270 C140 360 140 440 150 500" stroke="#ffffff" stroke-width="12" opacity="0.6" fill="none" stroke-linecap="round"/>']
    for k, x in enumerate((180, 232, 284)):  # vapor
        b.append(f'<path d="M{x} 230 C{x-30} 190 {x+30} 150 {x} 110 C{x-24} 80 {x+16} 50 {x} 20" stroke="#ffffff" stroke-width="14" opacity="0.35" fill="none" stroke-linecap="round" filter="url(#blur8)"/>'
                 f'<path d="M{x} 230 C{x-30} 190 {x+30} 150 {x} 110 C{x-24} 80 {x+16} 50 {x} 20" stroke="#ffffff" stroke-width="4" opacity="0.55" fill="none" stroke-linecap="round"/>')
    _g("taza_cafe", "".join(b), w, h, d)


def pantalla_ordenador(sombra=None):
    w, h = 800, 660
    r = random.Random(59)
    d = (_lgu("ompo_c", 0, 20, 0, 500, ("0", "#3a3c42"), ("1", "#141518")) + lg("ompo_s", (0, "#f8fafc"), (1, "#e8eef4")) +
         _lgu("ompo_pie", 300, 0, 500, 0, ("0", "#8a929e"), ("0.4", "#e8ecf2"), ("1", "#5a626e")) +
         lg("ompo_gl", (0, "#ffffff"), (0.4, "#ffffff00"), x2=1, y2=1))
    b = [_sc(400, 640, 220, 14, 0.4, sombra),
         '<path d="M360 470 L440 470 L452 600 L348 600 Z" fill="url(#ompo_pie)"/>',
         '<path d="M250 600 L550 600 C570 600 580 612 580 624 L220 624 C220 612 230 600 250 600 Z" fill="url(#ompo_pie)"/>',
         '<g filter="url(#sombra)"><rect x="30" y="20" width="740" height="460" rx="18" fill="url(#ompo_c)"/></g>',
         '<rect x="52" y="40" width="696" height="404" rx="4" fill="url(#ompo_s)"/>',
         '<rect x="52" y="40" width="696" height="34" fill="#2a8a5a"/>',
         *[f'<rect x="{66+k*36}" y="50" width="24" height="14" rx="3" fill="#ffffff" opacity="0.6"/>' for k in range(6)],
         '<rect x="52" y="74" width="696" height="26" fill="#e8eef4"/>',
         '<rect x="60" y="80" width="200" height="14" rx="3" fill="#ffffff" stroke="#c8d0d8"/>']
    # cuadrícula
    x0, y0, cw, ch = 52, 100, 62, 22
    for f in range(16):
        y = y0 + f * ch
        b.append(f'<path d="M{x0} {y} L{x0+430} {y}" stroke="#d0d8e0" stroke-width="1"/>')
        if f == 0:
            b.append(f'<rect x="{x0}" y="{y}" width="430" height="{ch}" fill="#d8eede"/>')
        for c in range(7):
            x = x0 + c * cw
            if f > 0 and r.random() < 0.75:
                L = r.uniform(18, 50)
                b.append(f'<rect x="{x+6:.0f}" y="{y+8}" width="{L:.0f}" height="6" rx="2" fill="{"#5a6a7a" if c else "#3a4a5a"}" opacity="0.6"/>')
            elif f == 0:
                b.append(f'<rect x="{x+8}" y="{y+8}" width="40" height="6" rx="2" fill="#2a6a4a" opacity="0.8"/>')
    for c in range(8):
        b.append(f'<path d="M{x0+c*cw} {y0} L{x0+c*cw} {y0+344}" stroke="#d0d8e0" stroke-width="1"/>')
    b.append(f'<rect x="{x0+2*cw}" y="{y0+5*ch}" width="{cw}" height="{ch}" fill="none" stroke="#2a8a5a" stroke-width="3"/>')
    # gráficos
    b += ['<rect x="500" y="110" width="232" height="150" rx="6" fill="#ffffff" stroke="#d0d8e0"/>']
    for k, v in enumerate((60, 90, 70, 110, 100, 126)):
        b.append(f'<rect x="{518+k*36}" y="{246-v}" width="22" height="{v}" fill="{["#2a8a5a","#4ac0ff","#ffb15e"][k%3]}"/>')
    b += ['<rect x="500" y="276" width="232" height="150" rx="6" fill="#ffffff" stroke="#d0d8e0"/>',
          '<path d="M516 400 L556 370 L596 384 L636 330 L676 346 L716 300" stroke="#ff3df2" stroke-width="4" fill="none" stroke-linejoin="round"/>',
          '<path d="M516 400 L556 370 L596 384 L636 330 L676 346 L716 300 L716 410 L516 410 Z" fill="#ff3df2" opacity="0.12"/>',
          '<path d="M516 410 L716 410" stroke="#c8d0d8" stroke-width="2"/>',
          '<rect x="52" y="40" width="696" height="404" fill="url(#ompo_gl)" opacity="0.18"/>',
          '<circle cx="400" cy="462" r="4" fill="#5a5e66"/>',
          '<path d="M32 40 L32 460" stroke="#6a6e76" stroke-width="2" opacity="0.6"/>']
    _g("pantalla_ordenador", "".join(b), w, h, d)


# ================================================================== RELOJ DE ARENA
def _reloj_arena(nombre, lleno_arriba):
    w, h = 380, 620
    vid = ("M110 70 L270 70 C270 170 220 250 198 300 C196 306 196 314 198 320 C220 370 270 450 270 550 L110 550 "
           "C110 450 160 370 182 320 C184 314 184 306 182 300 C160 250 110 170 110 70 Z")
    d = (_lgu("omra_m", 0, 0, 0, 40, ("0", "#c08a52"), ("0.5", "#8a5a32"), ("1", "#4a2e16")) +
         _lgu("omra_p", 0, 0, 22, 0, ("0", "#c08a52"), ("0.5", "#7a4a26"), ("1", "#3a2210")) +
         lg("omra_a", (0, "#f6d79a"), (1, "#d8a85a")) +
         _lgu("omra_v", 110, 0, 270, 0, ("0", "#ffffff", 0.35), ("0.3", "#ffffff", 0.08), ("0.8", "#bfe4ff", 0.1), ("1", "#ffffff", 0.3)) +
         _clip(f"{nombre}_cl", vid))
    b = [_sc(190, 604, 160, 12, 0.4), '<g clip-path="url(#%s_cl)">' % nombre]
    if lleno_arriba:
        b += ['<path d="M100 120 L280 120 L280 310 L100 310 Z" fill="url(#omra_a)"/>',
              '<path d="M100 120 Q190 136 280 120" stroke="#fff0c8" stroke-width="3" fill="none"/>',
              '<path d="M150 550 Q190 500 230 550 Z" fill="url(#omra_a)"/>',
              '<path d="M190 300 L190 520" stroke="#e8b86a" stroke-width="4"/>',
              '<path d="M190 120 L182 132 L198 132 Z" fill="#c8984a" opacity="0.6"/>']
    else:
        b += ['<path d="M100 400 Q190 360 280 400 L280 560 L100 560 Z" fill="url(#omra_a)"/>',
              '<path d="M120 400 Q190 362 260 400" stroke="#fff0c8" stroke-width="3" fill="none"/>',
              '<path d="M176 302 Q190 292 204 302 Z" fill="url(#omra_a)"/>']
    b += [f'<rect width="{w}" height="{h}" fill="url(#omra_v)"/>', _gr(f"{nombre}_cl", w, h, 0.5), '</g>',
          f'<path d="{vid}" fill="none" stroke="#e8f6ff" stroke-width="3" opacity="0.7"/>',
          '<path d="M128 90 C130 160 160 230 176 280" stroke="#ffffff" stroke-width="6" opacity="0.5" fill="none" stroke-linecap="round"/>',
          '<path d="M128 530 C130 470 150 410 170 360" stroke="#ffffff" stroke-width="6" opacity="0.4" fill="none" stroke-linecap="round"/>',
          # postes
          '<rect x="66" y="60" width="22" height="500" rx="8" fill="url(#omra_p)"/>', '<rect x="292" y="60" width="22" height="500" rx="8" fill="url(#omra_p)"/>',
          *[f'<ellipse cx="{x}" cy="{y}" rx="15" ry="8" fill="#a8703a"/>' for x in (77, 303) for y in (180, 310, 440)],
          # tapas
          '<rect x="40" y="30" width="300" height="40" rx="10" fill="url(#omra_m)"/>', '<rect x="40" y="550" width="300" height="40" rx="10" fill="url(#omra_m)"/>',
          '<path d="M50 34 L330 34" stroke="#f0c890" stroke-width="3" opacity="0.7"/><path d="M50 554 L330 554" stroke="#f0c890" stroke-width="3" opacity="0.7"/>',
          '<path d="M320 70 L330 550" stroke="#2ff3ff" stroke-width="0"/>']
    _g(nombre, "".join(b), w, h, d)


# ================================================================== ESTACIONES
def hoja_otono():
    w = h = 380
    d = (_lgu("omho_g", 80, 60, 300, 320, ("0", "#ffcf4a"), ("0.45", "#f08a2a"), ("1", "#c03a1a")) +
         _clip("omho_cl", "M190 30 L214 104 L262 70 L252 140 L330 120 L298 186 L350 210 L270 236 L286 290 L206 262 L198 330 L182 330 L174 262 L94 290 L110 236 L30 210 L82 186 L50 120 L128 140 L118 70 L166 104 Z"))
    leaf = "M190 30 L214 104 L262 70 L252 140 L330 120 L298 186 L350 210 L270 236 L286 290 L206 262 L198 330 L182 330 L174 262 L94 290 L110 236 L30 210 L82 186 L50 120 L128 140 L118 70 L166 104 Z"
    b = [f'<g filter="url(#sombra)"><path d="{leaf}" fill="url(#omho_g)" stroke="#a8301a" stroke-width="3" stroke-linejoin="round"/></g>',
         '<g clip-path="url(#omho_cl)">',
         '<path d="M190 330 L190 60 M190 250 L90 280 M190 250 L290 280 M190 200 L60 130 M190 200 L320 130 M190 160 L120 80 M190 160 L260 80" stroke="#fff0b0" stroke-width="3" opacity="0.7" fill="none"/>',
         '<circle cx="260" cy="200" r="18" fill="#8a2a12" opacity="0.3"/><circle cx="130" cy="240" r="10" fill="#8a2a12" opacity="0.25"/>',
         _gr("omho_cl", w, h), '</g>',
         '<path d="M190 330 L196 372" stroke="#8a4a1a" stroke-width="6" stroke-linecap="round"/>']
    _g("hoja_otono", "".join(b), w, h, d)


def copo_nieve():
    w = h = 380
    c = 190
    d = rg("omcn_g", (0, "#e8f6ff", 0.6), (1, "#a9d6f5", 0))
    b = [f'<circle cx="{c}" cy="{c}" r="180" fill="url(#omcn_g)"/>']
    brazo = []
    for k in range(6):
        a = math.radians(k * 60 - 90)
        ca, sa = math.cos(a), math.sin(a)
        ex, ey = c + ca * 160, c + sa * 160
        brazo.append(f'<path d="M{c} {c} L{ex:.1f} {ey:.1f}" />')
        for t, L in ((0.45, 46), (0.7, 32), (0.88, 18)):
            px, py = c + ca * 160 * t, c + sa * 160 * t
            for s in (-1, 1):
                b2 = a + s * math.radians(55)
                brazo.append(f'<path d="M{px:.1f} {py:.1f} L{px+math.cos(b2)*L:.1f} {py+math.sin(b2)*L:.1f}"/>')
    g = "".join(brazo)
    b += [f'<g stroke="#5f9fd1" stroke-width="16" stroke-linecap="round" opacity="0.4">{g}</g>',
          f'<g stroke="#e8f6ff" stroke-width="10" stroke-linecap="round">{g}</g>',
          f'<g stroke="#ffffff" stroke-width="3" stroke-linecap="round">{g}</g>',
          f'<polygon points="{_estrella(c, c, 34, 20, 6)}" fill="#a9d6f5"/><circle cx="{c}" cy="{c}" r="12" fill="#ffffff"/>']
    _g("copo_nieve", "".join(b), w, h, d)


def flor_primavera():
    w, h = 380, 420
    c, cy = 190, 170
    d = (_rgu("omfp_p", c, cy, 150, ("0", "#ffffff"), ("0.35", "#ffc8e0"), ("1", "#ff6aa8")) +
         _rgu("omfp_c", c - 8, cy - 8, 40, ("0", "#fff6a0"), ("0.6", "#ffd34a"), ("1", "#e89a1a")) +
         lg("omfp_h", (0, "#8ad86a"), (1, "#3a8a3a")))
    b = [f'<path d="M{c} {cy} C{c+6} 280 {c-10} 340 {c} 410" stroke="#4a9a3a" stroke-width="9" fill="none" stroke-linecap="round"/>',
         f'<path d="M{c-2} 330 C{c-80} 320 {c-120} 270 {c-120} 240 C{c-70} 250 {c-30} 280 {c-2} 320 Z" fill="url(#omfp_h)"/>',
         f'<path d="M{c+2} 360 C{c+80} 350 {c+120} 300 {c+124} 270 C{c+70} 280 {c+30} 310 {c+2} 350 Z" fill="url(#omfp_h)"/>',
         f'<path d="M{c-4} 326 C{c-60} 300 {c-100} 266 {c-116} 244" stroke="#c8f0a0" stroke-width="2" opacity="0.6" fill="none"/>']
    for k in range(5):
        a = k * 72 - 90
        b.append(f'<g transform="rotate({a} {c} {cy})"><ellipse cx="{c+78}" cy="{cy}" rx="78" ry="48" fill="url(#omfp_p)"/>'
                 f'<path d="M{c+20} {cy} L{c+140} {cy}" stroke="#ff4a90" stroke-width="2" opacity="0.4"/>'
                 f'<ellipse cx="{c+90}" cy="{cy-18}" rx="30" ry="10" fill="#ffffff" opacity="0.5"/></g>')
    b.append(f'<circle cx="{c}" cy="{cy}" r="38" fill="url(#omfp_c)"/>')
    r = random.Random(61)
    for _ in range(18):
        a, rr = r.uniform(0, 6.28), r.uniform(4, 30)
        b.append(f'<circle cx="{c+math.cos(a)*rr:.1f}" cy="{cy+math.sin(a)*rr:.1f}" r="2.6" fill="#c8701a" opacity="0.7"/>')
    b.append(_destello_peq(300, 60, 10))
    _g("flor_primavera", "".join(b), w, h, d)


def sol_verano():
    w = h = 380
    c, cy = 190, 170
    d = (_rgu("omsv_d", c - 20, cy - 20, 90, ("0", "#fffbe0"), ("0.5", "#ffd34a"), ("1", "#ff8a2a")) +
         rg("omsv_h", (0, "#ffcf8a", 0.6), (1, "#ffcf8a", 0)) + lg("omsv_m", (0, "#3ab0e0"), (1, "#1a6aa8")) +
         _clip("omsv_cl", f'<circle cx="{c}" cy="{c}" r="176"/>'))
    b = [f'<circle cx="{c}" cy="{cy}" r="176" fill="url(#omsv_h)"/>']
    for k in range(12):
        a = math.radians(k * 30)
        b.append(f'<path d="M{c+math.cos(a-0.13)*84:.1f} {cy+math.sin(a-0.13)*84:.1f} L{c+math.cos(a)*150:.1f} {cy+math.sin(a)*150:.1f} L{c+math.cos(a+0.13)*84:.1f} {cy+math.sin(a+0.13)*84:.1f} Z" fill="#ffb84a"/>')
    b += [f'<circle cx="{c}" cy="{cy}" r="80" fill="url(#omsv_d)"/>',
          f'<circle cx="{c-26}" cy="{cy-26}" r="22" fill="#ffffff" opacity="0.45" filter="url(#blur8)"/>',
          '<path d="M20 270 C70 250 110 290 160 270 C210 250 250 290 300 270 C330 258 350 266 360 270 L360 340 C300 370 80 370 20 340 Z" fill="url(#omsv_m)"/>',
          '<path d="M20 270 C70 250 110 290 160 270 C210 250 250 290 300 270 C330 258 350 266 360 270" stroke="#e8fbff" stroke-width="6" fill="none" stroke-linecap="round"/>',
          '<path d="M50 310 C90 296 120 320 160 306 C200 292 240 320 280 306 C310 296 330 302 340 306" stroke="#9ae0ff" stroke-width="4" fill="none" opacity="0.7" stroke-linecap="round"/>',
          '<path d="M120 286 L240 286 L220 296 L140 296 Z" fill="#ffd34a" opacity="0.5"/>']
    _g("sol_verano", "".join(b), w, h, d)


# ================================================================== PLACA PARA CIFRA
def cifra_marco():
    w, h = 840, 460
    r = random.Random(67)
    d = (_lgu("omcm_m", 0, 20, 0, 440, ("0", "#c89058"), ("0.5", "#9a6232"), ("1", "#6a3e1c")) +
         _lgu("omcm_i", 0, 90, 0, 370, ("0", "#5a3418"), ("1", "#7a4a26")) +
         '<clipPath id="omcm_cl"><rect x="20" y="20" width="800" height="420" rx="26"/></clipPath>' +
         '<clipPath id="omcm_ci"><rect x="90" y="90" width="660" height="280" rx="10"/></clipPath>' +
         rg("omcm_t", (0, "#f6d98a", 1), (0.6, "#b8862a", 1), (1, "#6a4a12", 1), cx=0.35, cy=0.35))
    b = [_sc(420, 448, 380, 14, 0.4),
         '<g filter="url(#sombra)"><rect x="20" y="20" width="800" height="420" rx="26" fill="url(#omcm_m)"/></g>',
         '<g clip-path="url(#omcm_cl)">', _vetas(r, 20, 20, 820, 440, 34, "#4a2810", 0.35, 4, 2.2),
         _gr("omcm_cl", w, h), '</g>',
         # bisel: luz arriba-izq, sombra abajo-der
         '<path d="M46 420 L46 46 Q46 40 52 40 L794 40" stroke="#f0c890" stroke-width="5" fill="none" opacity="0.7"/>',
         '<path d="M800 46 L800 414 Q800 420 794 420 L52 420" stroke="#3a1e0a" stroke-width="5" fill="none" opacity="0.6"/>',
         '<rect x="70" y="70" width="700" height="320" rx="14" fill="none" stroke="#3a1e0a" stroke-width="4" opacity="0.5"/>',
         '<rect x="90" y="90" width="660" height="280" rx="10" fill="url(#omcm_i)"/>',
         '<g clip-path="url(#omcm_ci)">', _vetas(r, 90, 90, 750, 370, 20, "#2a1408", 0.3, 3),
         '<path d="M90 90 L750 90 L750 110 L110 110 L110 370 L90 370 Z" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         _gr("omcm_ci", w, h), '</g>',
         '<path d="M92 368 L748 368 L748 92" stroke="#e8b070" stroke-width="3" opacity="0.6" fill="none"/>']
    for (x, y) in ((48, 48), (792, 48), (48, 412), (792, 412)):
        b.append(f'<circle cx="{x}" cy="{y}" r="10" fill="url(#omcm_t)"/><path d="M{x-6} {y} L{x+6} {y}" stroke="#5a3a0a" stroke-width="2"/>')
    _g("cifra_marco", "".join(b), w, h, d)


# ================================================================== GLOBO TERRÁQUEO
_TIERRAS = {
    "na": [(-165, 62), (-160, 70), (-140, 70), (-125, 70), (-110, 73), (-95, 72), (-85, 69), (-80, 63), (-95, 60), (-94, 57), (-85, 55),
           (-80, 52), (-78, 58), (-72, 62), (-65, 60), (-60, 55), (-56, 52), (-60, 47), (-66, 44), (-70, 42), (-74, 40), (-76, 37), (-76, 35),
           (-80, 32), (-81, 28), (-80, 25), (-82, 27), (-84, 30), (-89, 30), (-94, 29), (-97, 26), (-97, 22), (-95, 19), (-91, 19), (-87, 21),
           (-88, 16), (-84, 15), (-83, 10), (-79, 9), (-77, 8), (-80, 7), (-85, 10), (-87, 13), (-92, 15), (-96, 16), (-105, 20), (-106, 23),
           (-109, 26), (-112, 29), (-114, 31), (-113, 29), (-111, 25), (-110, 23), (-112, 25), (-115, 28), (-117, 32), (-120, 34), (-123, 38),
           (-124, 42), (-124, 47), (-123, 49), (-130, 54), (-135, 58), (-140, 60), (-148, 61), (-152, 59), (-158, 57), (-162, 55), (-160, 58), (-164, 60)],
    "sa": [(-77, 8), (-72, 12), (-64, 10), (-60, 8), (-52, 5), (-50, 0), (-44, -2), (-38, -4), (-35, -7), (-35, -10), (-39, -15), (-39, -20),
           (-42, -23), (-48, -26), (-49, -29), (-53, -34), (-58, -35), (-57, -38), (-62, -39), (-65, -42), (-65, -46), (-68, -50), (-69, -53),
           (-68, -55), (-72, -54), (-75, -50), (-74, -44), (-73, -38), (-71, -30), (-70, -20), (-75, -15), (-77, -12), (-80, -6), (-81, -2),
           (-80, 1), (-78, 4)],
    "gr": [(-73, 78), (-60, 82), (-35, 83), (-20, 80), (-18, 75), (-22, 70), (-30, 68), (-40, 65), (-43, 60), (-48, 61), (-52, 65), (-55, 70), (-60, 76), (-70, 77)],
    "is": [(-24, 65.5), (-22, 66.4), (-16, 66.5), (-13.5, 65), (-18, 63.4), (-22, 63.8)],
    "ea": [(28, 71), (18, 70), (13, 67), (5, 62), (6, 58), (11, 59), (11, 56), (8, 57), (8, 54), (4, 52), (2, 51), (-1.5, 49), (-4.5, 48.5),
           (-1.5, 46), (-1.5, 44), (-9, 43.5), (-9, 39), (-9, 37), (-6, 36.5), (-2, 37), (0, 39), (3, 42), (6, 43), (9, 44), (12, 42), (16, 38),
           (16, 40), (18, 40), (13, 44), (14, 45.5), (19, 42), (21, 39), (23, 37), (24, 40), (26, 41), (29, 41), (36, 41), (41, 41), (36, 37),
           (35, 33), (34, 31), (32, 31), (30, 31), (25, 32), (20, 31), (20, 32.5), (15, 32), (11, 34), (10, 37), (3, 37), (-2, 35), (-6, 36),
           (-10, 31), (-14, 26), (-17, 21), (-17, 15), (-15, 11), (-13, 8), (-8, 4.5), (-3, 5), (4, 6), (9, 4), (9, 1), (12, -5), (13, -12),
           (12, -17), (15, -27), (18, -34), (20, -35), (26, -34), (32, -29), (35, -24), (40, -15), (40, -10), (39, -5), (41, -1), (44, 2),
           (51, 11), (44, 12), (43, 13), (50, 15), (58, 20), (57, 25), (50, 30), (48, 30), (48, 40), (50, 45), (60, 45), (70, 50), (70, 70), (40, 68), (33, 70)],
    "gb": [(-5, 50), (1.5, 51), (1.7, 53), (0, 54), (-2, 56), (-2, 57.7), (-3, 58.6), (-5, 58.6), (-6, 57), (-5.5, 55), (-3, 54.5), (-3, 53.4),
           (-4.5, 52.8), (-5, 51.7), (-3, 51.4), (-5.7, 50)],
    "ie": [(-6, 52), (-6, 54), (-7.5, 55.3), (-10, 54), (-10, 51.6)],
    "md": [(44, -25), (47, -25), (50, -15), (49, -12), (44, -17)],
    "cu": [(-85, 22), (-82, 23), (-77, 21.5), (-74, 20), (-78, 20), (-82, 21.5)],
    "hi": [(-74, 19.8), (-72, 19.9), (-69, 19), (-68.5, 18.4), (-71, 18), (-74, 18.3)],
}


def foto_mundo():
    w = h = 740
    c, R = 370, 320
    lon0, lat0 = math.radians(-32), math.radians(26)

    def proy(lon, lat):
        lo, la = math.radians(lon), math.radians(lat)
        cosc = math.sin(lat0) * math.sin(la) + math.cos(lat0) * math.cos(la) * math.cos(lo - lon0)
        x = math.cos(la) * math.sin(lo - lon0)
        y = math.cos(lat0) * math.sin(la) - math.sin(lat0) * math.cos(la) * math.cos(lo - lon0)
        if cosc < 0:  # al otro lado: lo pegamos al borde
            n = math.hypot(x, y) or 1
            x, y = x / n, y / n
        return c + x * R, c - y * R

    def poli(pts, dens=4):
        out = []
        for i in range(len(pts)):
            a, b_ = pts[i], pts[(i + 1) % len(pts)]
            for k in range(dens):
                t = k / dens
                out.append(proy(a[0] + (b_[0] - a[0]) * t, a[1] + (b_[1] - a[1]) * t))
        return _suave(out, cerrado=True)

    tierras = {k: poli(v) for k, v in _TIERRAS.items()}
    d = (_rgu("omgl_o", c - 110, c - 120, 420, ("0", "#4ab0e0"), ("0.45", "#1f78b8"), ("0.85", "#0f3f78"), ("1", "#0a2a5a")) +
         _rgu("omgl_s", c - 140, c - 150, 470, ("0", "#000", 0), ("0.55", "#000", 0), ("0.85", "#0a1030", 0.45), ("1", "#050818", 0.8)) +
         _rgu("omgl_at", c, c, R + 36, ("0.86", "#6fd0ff", 0), ("0.9", "#6fd0ff", 0.55), ("1", "#6fd0ff", 0)) +
         _rgu("omgl_br", c - 130, c - 140, 160, ("0", "#ffffff", 0.45), ("1", "#ffffff", 0)) +
         f'<clipPath id="omgl_cl"><circle cx="{c}" cy="{c}" r="{R}"/></clipPath>' +
         '<clipPath id="omgl_tl">' + "".join(f'<path d="{p}"/>' for k, p in tierras.items() if k != "gr") + '</clipPath>' +
         ilus._neb("omgl_nb", "#ffffff", 77, freq=0.011, contraste=2.6, corte=1.25, oct=5) +
         ilus._neb("omgl_tx", "#2a3a12", 12, freq=0.03, contraste=2.0, corte=0.9, oct=3))
    b = [f'<circle cx="{c}" cy="{c}" r="{R+36}" fill="url(#omgl_at)"/>',
         f'<circle cx="{c}" cy="{c}" r="{R}" fill="url(#omgl_o)"/>', '<g clip-path="url(#omgl_cl)">']
    # tierra: verde con zonas secas y desierto
    b.append('<g clip-path="url(#omgl_tl)">')
    b.append(f'<rect width="{w}" height="{h}" fill="#4f8a3c"/>')
    for (lon, lat, rx, ry, col, op) in ((10, 23, 170, 70, "#e0c080", 0.95), (45, 24, 70, 50, "#d8b070", 0.9), (-110, 35, 50, 40, "#c8a060", 0.8),
                                       (-65, -25, 40, 50, "#a8a050", 0.6), (-60, -5, 70, 60, "#2f6a2a", 0.9), (20, 0, 60, 40, "#2f6a2a", 0.9),
                                       (-100, 58, 90, 40, "#3f7040", 0.7), (25, -25, 40, 30, "#b8a060", 0.7), (30, 60, 120, 40, "#5a7a40", 0.6)):
        x, y = proy(lon, lat)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx}" ry="{ry}" fill="{col}" opacity="{op}" filter="url(#blur20)"/>')
    b.append(f'<rect width="{w}" height="{h}" filter="url(#omgl_tx)" opacity="0.6"/>')
    b.append('</g>')
    for k, p in tierras.items():
        if k == "gr":
            b.append(f'<path d="{p}" fill="#eef4f8"/><path d="{p}" fill="none" stroke="#c8d8e4" stroke-width="2"/>')
        else:
            b.append(f'<path d="{p}" fill="none" stroke="#a8d890" stroke-width="1.6" opacity="0.6"/>')
    # hielo del ártico
    x, y = proy(-40, 88)
    b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="150" ry="40" fill="#ffffff" opacity="0.6" filter="url(#blur8)"/>')
    # nubes
    b.append(f'<rect width="{w}" height="{h}" filter="url(#omgl_nb)" opacity="0.85"/>')
    rr = random.Random(71)
    for _ in range(8):  # remolinos de nubes
        lon, lat = rr.uniform(-100, 20), rr.uniform(-45, 60)
        x, y = proy(lon, lat)
        s = rr.uniform(20, 40)
        b.append(f'<path d="M{x-s:.0f} {y:.0f} C{x-s:.0f} {y-s:.0f} {x+s:.0f} {y-s:.0f} {x+s*0.6:.0f} {y+s*0.2:.0f} C{x+s*0.2:.0f} {y+s*0.5:.0f} {x-s*0.3:.0f} {y+s*0.1:.0f} {x:.0f} {y-s*0.2:.0f}" '
                 f'stroke="#ffffff" stroke-width="{s*0.35:.0f}" opacity="0.55" fill="none" stroke-linecap="round" filter="url(#blur8)"/>')
    b += [f'<circle cx="{c}" cy="{c}" r="{R}" fill="url(#omgl_s)"/>',
          f'<circle cx="{c}" cy="{c}" r="{R}" fill="url(#omgl_br)"/>',
          _gr("omgl_cl", w, h, 0.6), '</g>',
          f'<circle cx="{c}" cy="{c}" r="{R}" fill="none" stroke="#bfefff" stroke-width="4" opacity="0.6"/>',
          f'<path d="M{c-R*0.86:.0f} {c-R*0.3:.0f} A{R} {R} 0 0 1 {c-R*0.1:.0f} {c-R*0.99:.0f}" stroke="#ffffff" stroke-width="6" opacity="0.5" fill="none" stroke-linecap="round"/>']
    _g("foto_mundo", "".join(b), w, h, d)


# ================================================================== GENERAR
def generar(dirsvg):
    global NOMBRES
    NOMBRES = []
    ilus.OUT = dirsvg
    os.makedirs(dirsvg, exist_ok=True)
    _cerebro("cerebro")
    _cerebro("cerebro_brillo", brillo=True)
    recuerdos()
    reloj_interno()
    aguja_interna()
    ojo()
    rayo_sol()
    trofeo()
    urna_voto()
    _nota("nota_musical_a", False, "#ff8ae8", "#8a2ad8", "#ff3df2")
    _nota("nota_musical_b", True, "#8af8ff", "#2a6ad8", "#2ff3ff")
    telefono_movil()
    telefono_movil_b()
    cuna()
    flor_blanca()
    periodico()
    mascarilla()
    _microfono("microfono_a", "#e0483a", "#9a1e18", "#ff8a7a")
    _microfono("microfono_b", "#3a7ae0", "#1a3a9a", "#8ab8ff")
    _microfono("microfono_c", "#f0b52a", "#b8780a", "#ffe08a")
    camara_flash()
    destello()
    ducha()
    _ventana("ventana")
    _ventana("ventana_noche", noche=True)
    _calendario_taco("calendario_taco")
    _calendario_taco("calendario_hoja", solo_hoja=True)
    calendario_diciembre()
    sol_dibujo()
    luna_creciente()
    bici_nino()
    balon_playa()
    helado()
    taza_cafe()
    pantalla_ordenador()
    _reloj_arena("reloj_arena_a", True)
    _reloj_arena("reloj_arena_b", False)
    hoja_otono()
    copo_nieve()
    flor_primavera()
    sol_verano()
    cifra_marco()
    foto_mundo()
    return list(NOMBRES)


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "/tmp/arte_objetos_mundo/svg"))
