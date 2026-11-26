"""Fondos del vídeo largo «El que copiaba en el colegio» (estilo del vídeo largo de la cueva). Ver ../ARTE.md.

Uso:  python3 lotes/largo-el-que-copiaba/generadores/ilus_fondos.py DIR_SVG [nombre ...]
      from ilus_fondos import generar; generar(DIR_SVG) → lista de nombres
Cada fondo sale en `nombre.svg` (1080×1920) y `nombre_h.svg` (1920×1080), recompuestos (no recortados).
Sin personas, sin letras ni logos. Semillas fijas: sale igual cada vez.
`INFO[nombre]` guarda la y del suelo (donde pisan los pies) y el centro de interés de cada formato.

Cómo está hecho:
- Se apoya en `ilus_escenarios.Lienzo` (degradados, luz, bruma, relieve, grano) y en sus ayudantes (`suave`, `_nube`, `mezcla`).
- Los interiores usan un suelo en perspectiva de un punto (`_suelo`: tarima o damero) que arranca en la línea pared/suelo `yb`
  con el horizonte (altura de los ojos) en `yh`; la luz de las ventanas se proyecta en el suelo con `_luz_ventana`.
- Rendimiento: como mucho 2 `feTurbulence` grandes por escena (relieve de pared y de suelo) más el grano.
"""
import math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
LARGO = os.path.join(RAIZ, "lotes", "largo-cueva-500-dias", "generadores")
sys.path.insert(0, RAIZ)
sys.path.insert(0, LARGO)
from motor.biblioteca import ilus  # noqa: E402,F401
import ilus_escenarios as IE  # noqa: E402
from ilus_escenarios import suave, mezcla, linea_ruido, _nube  # noqa: E402

INFO = {}


# ============================================================================ utilidades
def _ap(lst, *a):
    lst.extend(a)


def _hull(pts):
    pts = sorted(set((round(x, 1), round(y, 1)) for x, y in pts))
    if len(pts) < 3:
        return pts

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def _poly(pts, extra=""):
    return '<path d="M' + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + f' Z" {extra}/>'


def _rect(x, y, w, h, fill, op=None, extra=""):
    o = f' opacity="{op}"' if op is not None else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{o} {extra}/>'


def _suelo(L, yb, yh, cx, tipo, piezas, base, sem, a=70, junta="#2a160c", Dw=None, op_pieza=0.6):
    """Suelo en perspectiva de un punto desde la línea pared/suelo `yb` hasta abajo. tipo: 'tarima' | 'damero'.
    piezas: colores de tablas/baldosas; base: (color arriba, color abajo)."""
    w, h = L.w, L.h
    r = random.Random(sem)
    Dw = Dw or h * 0.9

    def P(X, Z):
        return (cx + X * Dw / Z, yh + (yb - yh) * Dw / Z)
    Zmin = (yb - yh) * Dw / (h + 30 - yh)
    out = [_rect(-10, yb, w + 20, h - yb + 10, L.lg((0, base[0]), (1, base[1])))]
    nX = int((w / 2 + abs(cx - w / 2)) / a) + 2
    if tipo == "tarima":
        for j in range(-nX, nX + 1):
            Z = Dw * (1 + r.uniform(0, 0.4) * a / Dw * 4)
            Z = Dw
            first = True
            while Z > Zmin:
                ln = r.uniform(4, 9) * a * (0.5 if first else 1)
                first = False
                Z2 = max(Zmin * 0.95, Z - ln)
                q = [P(j * a, Z), P((j + 1) * a, Z), P((j + 1) * a, Z2), P(j * a, Z2)]
                _ap(out, _poly(q, f'fill="{r.choice(piezas)}" opacity="{r.uniform(op_pieza * 0.6, op_pieza):.2f}"'))
                p0, p1 = P(j * a, Z2), P((j + 1) * a, Z2)
                _ap(out, f'<path d="M{p0[0]:.1f} {p0[1]:.1f} L{p1[0]:.1f} {p1[1]:.1f}" stroke="{junta}" stroke-width="{1 + (p0[1] - yb) / 300:.1f}" opacity="0.55"/>')
                Z = Z2
            p0, p1 = P(j * a, Dw), P(j * a, Zmin * 0.95)
            _ap(out, f'<path d="M{p0[0]:.1f} {p0[1]:.1f} L{p1[0]:.1f} {p1[1]:.1f}" stroke="{junta}" stroke-width="2" opacity="0.6"/>')
            q0, q1 = P(j * a + 3, Dw), P(j * a + 3, Zmin * 0.95)
            _ap(out, f'<path d="M{q0[0]:.1f} {q0[1]:.1f} L{q1[0]:.1f} {q1[1]:.1f}" stroke="#fff2dc" stroke-width="1" opacity="0.18"/>')
    else:
        Z, k = Dw, 0
        while Z > Zmin:
            Z2 = max(Zmin * 0.95, Z - a)
            for j in range(-nX, nX + 1):
                q = [P(j * a, Z), P((j + 1) * a, Z), P((j + 1) * a, Z2), P(j * a, Z2)]
                c = piezas[(j + k) % 2] if len(piezas) == 2 else r.choice(piezas)
                _ap(out, _poly(q, f'fill="{c}" opacity="{op_pieza:.2f}"'))
            p0, p1 = P(-nX * a, Z2), P((nX + 1) * a, Z2)
            _ap(out, f'<path d="M{p0[0]:.1f} {p0[1]:.1f} L{p1[0]:.1f} {p1[1]:.1f}" stroke="{junta}" stroke-width="{1 + (p0[1] - yb) / 400:.1f}" opacity="0.5"/>')
            Z, k = Z2, k + 1
        for j in range(-nX, nX + 2):
            p0, p1 = P(j * a, Dw), P(j * a, Zmin * 0.95)
            _ap(out, f'<path d="M{p0[0]:.1f} {p0[1]:.1f} L{p1[0]:.1f} {p1[1]:.1f}" stroke="{junta}" stroke-width="1.5" opacity="0.5"/>')
    # oclusión junto a la pared y reflejo suave
    _ap(out, _rect(-10, yb, w + 20, 60, L.lg((0, "#000000", 0.35), (1, "#000000", 0))))
    return "".join(out), P


def _luz_ventana(L, ven, nx, ny, fy0, fy1, shift, cx, yh, yb, color="#fff0c8", op=0.45, haz=0.16, polvo=0, sem=0):
    """Luz que entra por una ventana (x0,y0,x1,y1) con nx×ny cristales: haz diagonal y manchas en el suelo con la sombra
    del marco. La parte alta de la ventana cae más cerca del espectador (fy1) y desplazada `shift` en x."""
    x0, y0, x1, y1 = ven
    def proy(x, y):
        t = (y1 - y) / (y1 - y0)
        yy = fy0 + t * (fy1 - fy0)
        xx = x + shift * t
        sc = (yy - yh) / (yb - yh)
        return (cx + (xx - cx) * sc, yy)
    manchas, todos = [], []
    m = 0.06
    for i in range(nx):
        for j in range(ny):
            px0 = x0 + (x1 - x0) * (i + m) / nx
            px1 = x0 + (x1 - x0) * (i + 1 - m) / nx
            py0 = y0 + (y1 - y0) * (j + m) / ny
            py1 = y0 + (y1 - y0) * (j + 1 - m) / ny
            q = [proy(px0, py0), proy(px1, py0), proy(px1, py1), proy(px0, py1)]
            todos += q
            manchas.append(_poly(q, f'fill="{color}" opacity="{op}"'))
    hz = _hull([(x0, y0), (x1, y0), (x0, y1), (x1, y1)] + todos)
    g = L.lg((0, color, haz), (1, color, haz * 0.3), x1=0, y1=0, x2=0.6, y2=1)
    out = [f'<g filter="url(#blur20)">' + _poly(hz, f'fill="{g}"') + "</g>",
           f'<g filter="url(#blur8)" style="mix-blend-mode:screen">' + "".join(manchas) + "</g>"]
    if polvo:
        c = L.clip(" ".join(f"M{p[0]:.0f} {p[1]:.0f}" if k == 0 else f"L{p[0]:.0f} {p[1]:.0f}" for k, p in enumerate(hz)) + " Z")
        _ap(out, f'<g clip-path="{c}">' + L.polvo(polvo, min(p[0] for p in hz), min(p[1] for p in hz), max(p[0] for p in hz),
                                                    max(p[1] for p in hz), "#fff6e0", 2.4, 0.7, sem=sem) + "</g>")
    return "".join(out)


def _vista_fuera(L, x0, y0, x1, y1, r, hora="dia"):
    """Lo que se ve por una ventana: cielo, sol, copa de árbol y tejado lejano (sin detalles que distraigan)."""
    c = L.clip(f"M{x0} {y0} L{x1} {y0} L{x1} {y1} L{x0} {y1} Z")
    ww, hh = x1 - x0, y1 - y0
    if hora == "dia":
        cielo = L.lg((0, "#7cbbe8"), (0.6, "#b9dcf2"), (1, "#f4ead0"))
        hojas, hl, edif = ("#4f7a3a", "#7aa64e", "#b8d47a"), "#cfe6a0", "#c8b8a0"
    elif hora == "tarde":
        cielo = L.lg((0, "#5a4a8a"), (0.35, "#c8607a"), (0.65, "#f49a5a"), (1, "#ffd08a"))
        hojas, hl, edif = ("#2a1e2e", "#3a2634", "#4a2e3a"), "#7a4a48", "#4a3044"
    else:
        cielo = L.lg((0, "#0a1230"), (1, "#24345a"))
        hojas, hl, edif = ("#0c1420", "#142030", "#1c2a40"), "#3a5070", "#101828"
    s = [_rect(x0, y0, ww, hh, cielo)]
    if hora == "dia":
        s.append(_nube(L, x0 + ww * 0.6, y0 + hh * 0.22, ww / 520, r, op=0.8))
    elif hora == "tarde":
        sx_, sy_ = x0 + ww * 0.42, y0 + hh * 0.42
        s.append(L.brillo(sx_, sy_, ww * 0.6, ww * 0.6, "#ffe0a0", 0.9))
        s.append(f'<circle cx="{sx_:.0f}" cy="{sy_:.0f}" r="{ww * 0.11:.0f}" fill="#fff4d0"/>')
        for k in range(3):
            yy = y0 + hh * (0.2 + k * 0.12)
            s.append(f'<path d="M{x0 + ww * r.uniform(-0.1, 0.4):.0f} {yy:.0f} l{ww * 0.6:.0f} 0" stroke="#e07a8a" stroke-width="{hh * 0.025:.0f}" stroke-linecap="round" opacity="0.6"/>')
    yt = y0 + hh * 0.72
    for k in range(4):
        bx = x0 + ww * (k * 0.3 - 0.05) + r.uniform(-10, 10)
        bw, bh = ww * r.uniform(0.25, 0.35), hh * r.uniform(0.12, 0.3)
        s.append(_rect(bx, yt - bh, bw, hh, edif))
        s.append(_rect(bx, yt - bh, bw, 4, "#ffffff", 0.3))
        if hora != "dia":
            for q in range(3):
                if r.random() < 0.6:
                    s.append(_rect(bx + 8 + q * bw / 3, yt - bh + 10, bw / 6, bh / 5, "#ffc870", 0.8))
    # copa de árbol cercana en un lado
    tx = x0 + ww * (0.15 if r.random() < 0.5 else 0.85)
    for k in range(26 if hora != "tarde" else 0):
        bx, by = tx + r.gauss(0, ww * 0.18), y0 + hh * 0.55 + r.gauss(0, hh * 0.18)
        rr = r.uniform(0.06, 0.12) * ww
        s.append(f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="{rr:.0f}" ry="{rr * 0.8:.0f}" fill="{hojas[k % 3]}"/>')
    for k in range(10 if hora != "tarde" else 0):
        bx, by = tx - ww * 0.05 + r.gauss(0, ww * 0.12), y0 + hh * 0.45 + r.gauss(0, hh * 0.12)
        s.append(f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="{ww * 0.04:.0f}" ry="{ww * 0.025:.0f}" fill="{hl}" opacity="0.6"/>')
    s.append(L.brillo(x0 + ww * 0.2, y0 + hh * 0.1, ww * 0.8, hh * 0.5, "#fff8e0" if hora == "dia" else "#ffd0a0", 0.5))
    return f'<g clip-path="{c}">' + "".join(s) + "</g>"


def _marco_ventana(x0, y0, x1, y1, nx, ny, g_marco, grosor=14, alfeizar="#e8e0d0", sombra=True):
    out = []
    if sombra:
        _ap(out, _rect(x0 - grosor - 4, y0 - grosor - 4, x1 - x0 + 2 * grosor + 16, y1 - y0 + 2 * grosor + 16, "#000", 0.12))
    for i in range(nx + 1):
        x = x0 + (x1 - x0) * i / nx
        gg = grosor if i in (0, nx) else grosor * 0.6
        _ap(out, _rect(x - gg / 2, y0 - grosor / 2, gg, y1 - y0 + grosor, g_marco))
    for j in range(ny + 1):
        y = y0 + (y1 - y0) * j / ny
        gg = grosor if j in (0, ny) else grosor * 0.6
        _ap(out, _rect(x0 - grosor / 2, y - gg / 2, x1 - x0 + grosor, gg, g_marco))
    # alféizar
    _ap(out, _rect(x0 - grosor * 2, y1 + grosor / 2, x1 - x0 + grosor * 4, grosor * 0.9, alfeizar))
    _ap(out, _rect(x0 - grosor * 2, y1 + grosor * 1.4, x1 - x0 + grosor * 4, 5, "#000", 0.25))
    return "".join(out)


def _reloj(L, x, y, R, r, marco=("#c89a4a", "#7a5420"), cara="#f6ecd4", forma="redondo", oscuro=0.0):
    """Reloj de pared sin números: marco con volumen, marcas, agujas, cristal con brillo y sombra en la pared."""
    out = [f'<ellipse cx="{x + R * 0.12:.0f}" cy="{y + R * 0.16:.0f}" rx="{R * 1.08:.0f}" ry="{R * 1.08:.0f}" fill="#000" opacity="0.28"/>']
    gm = L.lg((0, marco[0]), (1, marco[1]), x1=0.2, y1=0, x2=0.8, y2=1)
    if forma == "cuadrado":
        _ap(out, f'<rect x="{x - R * 1.08:.0f}" y="{y - R * 1.08:.0f}" width="{R * 2.16:.0f}" height="{R * 2.16:.0f}" rx="{R * 0.18:.0f}" fill="{gm}"/>')
    elif forma == "sol":
        for k in range(16):
            a = k * math.pi / 8
            _ap(out, f'<path d="M{x + math.cos(a) * R:.0f} {y + math.sin(a) * R:.0f} L{x + math.cos(a) * R * 1.45:.0f} {y + math.sin(a) * R * 1.45:.0f}" stroke="{gm}" stroke-width="{R * 0.12:.1f}" stroke-linecap="round"/>')
        _ap(out, f'<circle cx="{x}" cy="{y}" r="{R * 1.1:.0f}" fill="{gm}"/>')
    elif forma == "pendulo":
        _ap(out, f'<path d="M{x - R * 0.9:.0f} {y - R * 0.6:.0f} Q{x - R * 0.9:.0f} {y - R * 1.3:.0f} {x:.0f} {y - R * 1.3:.0f} Q{x + R * 0.9:.0f} {y - R * 1.3:.0f} {x + R * 0.9:.0f} {y - R * 0.6:.0f} L{x + R * 0.8:.0f} {y + R * 2.6:.0f} L{x - R * 0.8:.0f} {y + R * 2.6:.0f} Z" fill="{gm}"/>')
        _ap(out, _rect(x - R * 0.55, y + R * 1.2, R * 1.1, R * 1.25, "#2a1a10", 0.8))
        _ap(out, f'<path d="M{x:.0f} {y + R * 1.2:.0f} L{x + R * 0.15:.0f} {y + R * 2.1:.0f}" stroke="#d8b060" stroke-width="{R * 0.05:.1f}"/>'
                   f'<circle cx="{x + R * 0.15:.0f}" cy="{y + R * 2.15:.0f}" r="{R * 0.2:.0f}" fill="#e0b85a"/>')
        _ap(out, f'<circle cx="{x}" cy="{y}" r="{R * 0.98:.0f}" fill="{gm}"/>')
    else:
        _ap(out, f'<circle cx="{x}" cy="{y}" r="{R * 1.1:.0f}" fill="{gm}"/>')
    _ap(out, f'<circle cx="{x}" cy="{y}" r="{R:.0f}" fill="{L.rgu(x - R * 0.3, y - R * 0.3, R * 1.5, R * 1.5, (0, mezcla(cara, "#ffffff", 0.4), 1), (1, mezcla(cara, "#806040", 0.25), 1))}"/>')
    _ap(out, f'<circle cx="{x}" cy="{y}" r="{R:.0f}" fill="none" stroke="#000" stroke-width="{max(1, R * 0.05):.1f}" opacity="0.25"/>')
    for k in range(12):
        a = k * math.pi / 6
        l0 = 0.78 if k % 3 == 0 else 0.86
        _ap(out, f'<path d="M{x + math.cos(a) * R * l0:.1f} {y + math.sin(a) * R * l0:.1f} L{x + math.cos(a) * R * 0.93:.1f} {y + math.sin(a) * R * 0.93:.1f}" '
                   f'stroke="#2a2018" stroke-width="{R * (0.07 if k % 3 == 0 else 0.035):.1f}" stroke-linecap="round"/>')
    ah, am = r.uniform(0, 2 * math.pi), r.uniform(0, 2 * math.pi)
    _ap(out, f'<path d="M{x:.1f} {y:.1f} L{x + math.sin(ah) * R * 0.5:.1f} {y - math.cos(ah) * R * 0.5:.1f}" stroke="#1a1410" stroke-width="{R * 0.08:.1f}" stroke-linecap="round"/>'
               f'<path d="M{x:.1f} {y:.1f} L{x + math.sin(am) * R * 0.75:.1f} {y - math.cos(am) * R * 0.75:.1f}" stroke="#1a1410" stroke-width="{R * 0.05:.1f}" stroke-linecap="round"/>'
               f'<circle cx="{x}" cy="{y}" r="{R * 0.07:.1f}" fill="#b03a2a"/>')
    _ap(out, f'<path d="M{x - R * 0.7:.1f} {y - R * 0.35:.1f} A{R * 0.8:.1f} {R * 0.8:.1f} 0 0 1 {x + R * 0.1:.1f} {y - R * 0.8:.1f}" stroke="#ffffff" stroke-width="{R * 0.08:.1f}" opacity="0.5" fill="none" stroke-linecap="round"/>')
    if oscuro:
        _ap(out, f'<circle cx="{x}" cy="{y}" r="{R * 1.12:.0f}" fill="#0a0e1a" opacity="{oscuro}"/>')
    return "".join(out)


def _arbol(L, x, yb, s, r, hojas=("#3f6a30", "#5f8f40", "#9cc260"), tronco=("#5a4030", "#8a6a4a"), luz=-1, sombra=True, alto=1.0):
    """Árbol de copa redonda (plátano de sombra/morera): tronco con ramas y masa de hojas en tres tonos, luz del lado `luz`."""
    out = []
    if sombra:
        _ap(out, f'<ellipse cx="{x - luz * 40 * s:.0f}" cy="{yb + 4 * s:.0f}" rx="{110 * s:.0f}" ry="{14 * s:.0f}" fill="#1a2010" opacity="0.3"/>')
    th = 230 * s * alto
    gt = L.lg((0, tronco[1] if luz < 0 else tronco[0]), (1, tronco[0] if luz < 0 else tronco[1]), x2=1, y2=0)
    _ap(out, f'<path d="M{x - 16 * s:.0f} {yb:.0f} C{x - 10 * s:.0f} {yb - th * 0.5:.0f} {x - 14 * s:.0f} {yb - th * 0.7:.0f} {x - 40 * s:.0f} {yb - th:.0f} '
               f'L{x - 26 * s:.0f} {yb - th - 6 * s:.0f} C{x - 2 * s:.0f} {yb - th * 0.75:.0f} {x + 2 * s:.0f} {yb - th * 0.75:.0f} {x + 30 * s:.0f} {yb - th - 10 * s:.0f} '
               f'L{x + 40 * s:.0f} {yb - th:.0f} C{x + 14 * s:.0f} {yb - th * 0.7:.0f} {x + 10 * s:.0f} {yb - th * 0.5:.0f} {x + 16 * s:.0f} {yb:.0f} Z" fill="{gt}"/>')
    cy = yb - th - 90 * s
    for capa, (col, n, rr0, dy) in enumerate(((hojas[0], 22, 52, 20), (hojas[1], 20, 44, -6), (hojas[2], 12, 30, -26))):
        for k in range(n):
            a = r.uniform(0, 2 * math.pi)
            d = r.uniform(0, 1) ** 0.6
            bx = x + math.cos(a) * d * 150 * s + (luz * 20 * s if capa == 2 else 0)
            by = cy + math.sin(a) * d * 100 * s + dy * s
            if capa == 2 and (bx - x) * luz < 0:
                bx = x + (x - bx) * 0.6
            rr = r.uniform(0.7, 1.2) * rr0 * s
            _ap(out, f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="{rr:.0f}" ry="{rr * 0.82:.0f}" fill="{col}" opacity="{0.95 if capa < 2 else 0.8}"/>')
    # huecos de cielo y ramitas que asoman
    for k in range(4):
        bx, by = x + r.uniform(-110, 110) * s, cy + r.uniform(-40, 60) * s
        _ap(out, f'<path d="M{bx:.0f} {by:.0f} l{r.uniform(-20, 20) * s:.0f} {r.uniform(-30, -10) * s:.0f}" stroke="{tronco[0]}" stroke-width="{4 * s:.1f}" opacity="0.7"/>')
    return "".join(out)


def _farola(x, yb, H, s=1.0, encendida=False):
    """Farola clásica de hierro (fuste con basa y farol de cuatro cristales)."""
    out = [f'<ellipse cx="{x + 30 * s:.0f}" cy="{yb + 3 * s:.0f}" rx="{40 * s:.0f}" ry="{6 * s:.0f}" fill="#000" opacity="0.25"/>',
           f'<path d="M{x - 14 * s:.0f} {yb:.0f} L{x - 9 * s:.0f} {yb - 40 * s:.0f} L{x - 4 * s:.0f} {yb - H:.0f} L{x + 4 * s:.0f} {yb - H:.0f} L{x + 9 * s:.0f} {yb - 40 * s:.0f} L{x + 14 * s:.0f} {yb:.0f} Z" fill="#1e2228"/>',
           f'<path d="M{x - 2 * s:.0f} {yb - 40 * s:.0f} L{x - 1 * s:.0f} {yb - H:.0f}" stroke="#7a8494" stroke-width="{2 * s:.1f}" opacity="0.6"/>',
           f'<rect x="{x - 16 * s:.0f}" y="{yb - 46 * s:.0f}" width="{32 * s:.0f}" height="{8 * s:.0f}" fill="#2a2e36"/>']
    ft = yb - H
    _ap(out, f'<path d="M{x - 14 * s:.0f} {ft:.0f} L{x - 20 * s:.0f} {ft - 50 * s:.0f} L{x + 20 * s:.0f} {ft - 50 * s:.0f} L{x + 14 * s:.0f} {ft:.0f} Z" '
               f'fill="{"#ffe8b0" if encendida else "#d8e2e8"}" opacity="0.85"/>')
    _ap(out, f'<path d="M{x - 20 * s:.0f} {ft - 50 * s:.0f} L{x:.0f} {ft - 68 * s:.0f} L{x + 20 * s:.0f} {ft - 50 * s:.0f} Z" fill="#1e2228"/>'
               f'<path d="M{x - 14 * s:.0f} {ft:.0f} L{x + 14 * s:.0f} {ft:.0f} M{x:.0f} {ft:.0f} L{x:.0f} {ft - 50 * s:.0f}" stroke="#1e2228" stroke-width="{3 * s:.1f}"/>'
               f'<circle cx="{x:.0f}" cy="{ft - 72 * s:.0f}" r="{4 * s:.0f}" fill="#1e2228"/>')
    _ap(out, f'<path d="M{x - 17 * s:.0f} {ft - 46 * s:.0f} L{x - 13 * s:.0f} {ft - 4 * s:.0f}" stroke="#ffffff" stroke-width="{2 * s:.1f}" opacity="0.6"/>')
    return "".join(out)


def _coche(x, yb, s, col, r, mira=1):
    """Coche utilitario genérico de perfil (sin marca): carrocería con brillo, cristales, ruedas y sombra."""
    c1, c2 = mezcla(col, "#ffffff", 0.35), mezcla(col, "#000000", 0.4)
    g = f'<linearGradient id="co{abs(hash((x, yb))) % 99999}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="0.45" stop-color="{col}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'
    gid = f"co{abs(hash((x, yb))) % 99999}"
    body = ("M-120 -22 C-122 -40 -116 -52 -100 -56 L-62 -60 L-38 -92 C-34 -97 -28 -99 -20 -99 L44 -99 C54 -99 60 -96 66 -90 L92 -62 "
            "L112 -56 C122 -52 124 -40 122 -22 Z")
    out = [f'<defs>{g}</defs><g transform="translate({x:.0f} {yb:.0f}) scale({s * mira:.3f} {s:.3f})">',
           '<ellipse cx="0" cy="2" rx="130" ry="9" fill="#000" opacity="0.35"/>',
           f'<path d="{body}" fill="url(#{gid})"/>',
           '<path d="M-56 -60 L-34 -88 C-31 -92 -27 -93 -22 -93 L8 -93 L8 -60 Z" fill="#a8c8dc"/>',
           '<path d="M14 -93 L42 -93 C50 -93 55 -90 60 -85 L80 -60 L14 -60 Z" fill="#a8c8dc"/>',
           '<path d="M-50 -64 L-30 -88 L-20 -88 L-40 -64 Z M22 -88 L32 -88 L20 -64 L12 -64 Z" fill="#ffffff" opacity="0.5"/>',
           f'<path d="M-118 -40 L120 -40" stroke="{c2}" stroke-width="2" opacity="0.6"/>',
           f'<path d="M10 -58 L10 -24" stroke="{c2}" stroke-width="2" opacity="0.7"/>',
           f'<path d="M-100 -54 L100 -56" stroke="{c1}" stroke-width="3" opacity="0.7"/>',
           '<rect x="112" y="-50" width="10" height="9" rx="3" fill="#fff4c0"/><rect x="-122" y="-50" width="8" height="9" rx="3" fill="#c0302a"/>',
           '<rect x="-124" y="-26" width="248" height="8" rx="4" fill="#2a2a2e"/>']
    for wx in (-74, 74):
        _ap(out, f'<circle cx="{wx}" cy="-18" r="24" fill="#18181c"/><circle cx="{wx}" cy="-18" r="12" fill="#a8acb4"/><circle cx="{wx - 3}" cy="-21" r="5" fill="#e8eaf0"/>')
    _ap(out, "</g>")
    return "".join(out)


def _maceta_colgante(L, x, ytecho, ycuelga, s, r, hojas=("#2f5a2a", "#4f8a3a", "#8cc060"), maceta=("#c87a4a", "#7a3e20")):
    """Planta colgante: tres cuerdas, maceta con volumen y tallos que caen con hojas."""
    out = []
    for dx in (-26, 0, 26):
        _ap(out, f'<path d="M{x:.0f} {ytecho:.0f} L{x + dx * s:.0f} {ycuelga:.0f}" stroke="#d8c8a0" stroke-width="{1.6 * s:.1f}" opacity="0.8"/>')
    gm = L.lg((0, maceta[0]), (1, maceta[1]), x2=1, y2=0)
    _ap(out, f'<path d="M{x - 34 * s:.0f} {ycuelga:.0f} L{x + 34 * s:.0f} {ycuelga:.0f} L{x + 26 * s:.0f} {ycuelga + 44 * s:.0f} L{x - 26 * s:.0f} {ycuelga + 44 * s:.0f} Z" fill="{gm}"/>'
               f'<rect x="{x - 36 * s:.0f}" y="{ycuelga - 4 * s:.0f}" width="{72 * s:.0f}" height="{10 * s:.0f}" rx="{3 * s:.0f}" fill="{maceta[0]}"/>')
    for k in range(7):
        x0 = x + r.uniform(-30, 30) * s
        L_ = r.uniform(140, 380) * s
        dx = r.uniform(-60, 60) * s
        pts = [(x0, ycuelga), (x0 + dx * 0.4, ycuelga + L_ * 0.4), (x0 + dx, ycuelga + L_)]
        _ap(out, f'<path d="M{pts[0][0]:.0f} {pts[0][1]:.0f} Q{pts[1][0]:.0f} {pts[1][1]:.0f} {pts[2][0]:.0f} {pts[2][1]:.0f}" stroke="{hojas[0]}" stroke-width="{2 * s:.1f}" fill="none"/>')
        for j in range(int(L_ / (18 * s))):
            t = j / max(1, int(L_ / (18 * s)))
            hx = (1 - t) ** 2 * pts[0][0] + 2 * (1 - t) * t * pts[1][0] + t * t * pts[2][0]
            hy = (1 - t) ** 2 * pts[0][1] + 2 * (1 - t) * t * pts[1][1] + t * t * pts[2][1]
            lado = 1 if j % 2 else -1
            c = hojas[1] if r.random() < 0.6 else hojas[2]
            _ap(out, f'<ellipse cx="{hx + lado * 9 * s:.0f}" cy="{hy:.0f}" rx="{10 * s:.0f}" ry="{6 * s:.0f}" transform="rotate({lado * 35} {hx + lado * 9 * s:.0f} {hy:.0f})" fill="{c}"/>')
    for k in range(10):
        _ap(out, f'<ellipse cx="{x + r.uniform(-34, 34) * s:.0f}" cy="{ycuelga - r.uniform(0, 18) * s:.0f}" rx="{14 * s:.0f}" ry="{9 * s:.0f}" '
                   f'transform="rotate({r.uniform(-40, 40):.0f} {x:.0f} {ycuelga:.0f})" fill="{hojas[k % 3]}"/>')
    return "".join(out)


# ============================================================================ 1. aula
def _tiza(r, x0, y0, x1, y1):
    """Garabatos de tiza: formas, ondas, espirales, flechas y renglones ilegibles (sin letras)."""
    out = []
    ww, hh = x1 - x0, y1 - y0
    col = "#f4f2e8"
    # borrones de borrador (manchas claras desenfocadas)
    bor = "".join(f'<ellipse cx="{r.uniform(x0, x1):.0f}" cy="{r.uniform(y0, y1):.0f}" rx="{r.uniform(40, 120):.0f}" ry="{r.uniform(14, 30):.0f}" fill="#e8f0e8" opacity="{r.uniform(0.06, 0.14):.2f}"/>' for _ in range(10))
    _ap(out, f'<g filter="url(#blur8)">{bor}</g>')
    celdas = [(i, j) for i in range(4) for j in range(2)]
    r.shuffle(celdas)
    tipos = ["espiral", "onda", "circulos", "flecha", "triangulo", "sol", "estrella", "renglones"]
    for (i, j), t in zip(celdas, tipos):
        cx = x0 + ww * (i + 0.5) / 4 + r.uniform(-12, 12)
        cy = y0 + hh * (j + 0.5) / 2 + r.uniform(-10, 10)
        s = min(ww / 4, hh / 2) * 0.36
        sw = max(2.2, s * 0.06)
        st = f'stroke="{col}" stroke-width="{sw:.1f}" fill="none" stroke-linecap="round" opacity="{r.uniform(0.7, 0.9):.2f}"'
        if t == "espiral":
            pts = [(cx + math.cos(a / 4) * s * a / 30, cy + math.sin(a / 4) * s * a / 30 * 0.8) for a in range(1, 30)]
            _ap(out, f'<path d="{suave(pts, cerrado=False)}" {st}/>')
        elif t == "onda":
            pts = [(cx - s * 1.3 + k * s * 0.2, cy + math.sin(k * 0.9) * s * 0.35) for k in range(14)]
            _ap(out, f'<path d="{suave(pts, cerrado=False)}" {st}/>')
            _ap(out, f'<path d="{suave([(px, py + s * 0.5) for px, py in pts], cerrado=False)}" {st}/>')
        elif t == "circulos":
            for k in range(3):
                _ap(out, f'<ellipse cx="{cx + (k - 1) * s * 0.7:.0f}" cy="{cy + r.uniform(-6, 6):.0f}" rx="{s * 0.4:.0f}" ry="{s * 0.36:.0f}" {st}/>')
        elif t == "flecha":
            _ap(out, f'<path d="M{cx - s:.0f} {cy + s * 0.4:.0f} Q{cx:.0f} {cy - s * 0.8:.0f} {cx + s:.0f} {cy:.0f} M{cx + s * 0.6:.0f} {cy - s * 0.3:.0f} L{cx + s:.0f} {cy:.0f} L{cx + s * 0.55:.0f} {cy + s * 0.25:.0f}" {st}/>')
        elif t == "triangulo":
            _ap(out, f'<path d="M{cx - s:.0f} {cy + s * 0.6:.0f} L{cx + s:.0f} {cy + s * 0.6:.0f} L{cx - s * 0.2:.0f} {cy - s * 0.7:.0f} Z M{cx - s * 0.2:.0f} {cy - s * 0.7:.0f} L{cx - s * 0.2:.0f} {cy + s * 0.6:.0f}" {st}/>')
            _ap(out, f'<path d="M{cx - s * 0.2:.0f} {cy + s * 0.45:.0f} L{cx - s * 0.05:.0f} {cy + s * 0.45:.0f} L{cx - s * 0.05:.0f} {cy + s * 0.6:.0f}" {st}/>')
        elif t == "sol":
            _ap(out, f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{s * 0.38:.0f}" {st}/>')
            for k in range(9):
                a = k * 2 * math.pi / 9
                _ap(out, f'<path d="M{cx + math.cos(a) * s * 0.55:.0f} {cy + math.sin(a) * s * 0.55:.0f} L{cx + math.cos(a) * s * 0.85:.0f} {cy + math.sin(a) * s * 0.85:.0f}" {st}/>')
        elif t == "estrella":
            pts = []
            for k in range(10):
                a = -math.pi / 2 + k * math.pi / 5
                rr = s * (0.8 if k % 2 == 0 else 0.35)
                pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
            _ap(out, _poly(pts, st))
        else:  # renglones de garabato ilegible (bucles continuos)
            for k in range(3):
                yy = cy - s * 0.5 + k * s * 0.5
                pts = []
                xx = cx - s * 1.3
                while xx < cx + s * (1.3 - k * 0.3):
                    pts.append((xx, yy + r.uniform(-3, 3)))
                    pts.append((xx + s * 0.06, yy - s * 0.22))
                    xx += s * r.uniform(0.12, 0.2)
                _ap(out, f'<path d="{suave(pts, cerrado=False, t=0.8)}" stroke="{col}" stroke-width="{sw * 0.7:.1f}" fill="none" opacity="0.65"/>')
    return "".join(out)


def _dibujo_nino(L, x, y, ww, hh, tipo, r, rot):
    """Papel con un dibujo infantil a cera (formas simples, sin letras) y su chincheta."""
    papel = r.choice(["#fffdf4", "#fff6c8", "#e8f4ff", "#ffe8ec"])
    out = [f'<g transform="rotate({rot:.1f} {x + ww / 2:.0f} {y + hh / 2:.0f})">',
           _rect(x + 4, y + 6, ww, hh, "#000", 0.22), _rect(x, y, ww, hh, papel),
           _rect(x, y + hh * 0.85, ww, hh * 0.15, "#000", 0.04)]
    cx, cy = x + ww / 2, y + hh / 2
    s = min(ww, hh) / 2
    sw = max(2, s * 0.08)
    def tr(c, w_=sw):
        return f'stroke="{c}" stroke-width="{w_:.1f}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    if tipo == "casa":
        _ap(out, f'<path d="M{cx - s * 0.5:.0f} {cy + s * 0.6:.0f} L{cx - s * 0.5:.0f} {cy - s * 0.05:.0f} L{cx + s * 0.5:.0f} {cy - s * 0.05:.0f} L{cx + s * 0.5:.0f} {cy + s * 0.6:.0f} Z" fill="#f0a060" opacity="0.6"/>'
                   f'<path d="M{cx - s * 0.65:.0f} {cy:.0f} L{cx:.0f} {cy - s * 0.55:.0f} L{cx + s * 0.65:.0f} {cy:.0f} Z" fill="#d83a2a" opacity="0.8"/>'
                   f'<rect x="{cx - s * 0.12:.0f}" y="{cy + s * 0.2:.0f}" width="{s * 0.24:.0f}" height="{s * 0.4:.0f}" fill="#7a4a2a"/>'
                   f'<circle cx="{x + ww * 0.82:.0f}" cy="{y + hh * 0.18:.0f}" r="{s * 0.18:.0f}" fill="#f8c830"/>'
                   f'<path d="M{x + ww * 0.05:.0f} {cy + s * 0.62:.0f} L{x + ww * 0.95:.0f} {cy + s * 0.62:.0f}" {tr("#3aa04a", sw * 1.4)}/>')
    elif tipo == "arbol":
        _ap(out, f'<rect x="{cx - s * 0.1:.0f}" y="{cy:.0f}" width="{s * 0.2:.0f}" height="{s * 0.65:.0f}" fill="#8a5a2a"/>'
                   f'<circle cx="{cx:.0f}" cy="{cy - s * 0.15:.0f}" r="{s * 0.45:.0f}" fill="#3aa04a" opacity="0.85"/>'
                   f'<circle cx="{cx - s * 0.15:.0f}" cy="{cy - s * 0.2:.0f}" r="{s * 0.07:.0f}" fill="#e83a3a"/><circle cx="{cx + s * 0.18:.0f}" cy="{cy - s * 0.05:.0f}" r="{s * 0.07:.0f}" fill="#e83a3a"/>')
    elif tipo == "flor":
        _ap(out, f'<path d="M{cx:.0f} {cy + s * 0.75:.0f} L{cx:.0f} {cy:.0f}" {tr("#3aa04a")}/>'
                   f'<ellipse cx="{cx + s * 0.18:.0f}" cy="{cy + s * 0.4:.0f}" rx="{s * 0.16:.0f}" ry="{s * 0.07:.0f}" fill="#3aa04a"/>')
        for k in range(6):
            a = k * math.pi / 3
            _ap(out, f'<circle cx="{cx + math.cos(a) * s * 0.25:.0f}" cy="{cy - s * 0.2 + math.sin(a) * s * 0.25:.0f}" r="{s * 0.17:.0f}" fill="#e84a9a" opacity="0.85"/>')
        _ap(out, f'<circle cx="{cx:.0f}" cy="{cy - s * 0.2:.0f}" r="{s * 0.13:.0f}" fill="#f8c830"/>')
    elif tipo == "arcoiris":
        for k, c in enumerate(["#e83a3a", "#f8a030", "#f8d830", "#3aa04a", "#3a7ae8"]):
            rr = s * (0.8 - k * 0.12)
            _ap(out, f'<path d="M{cx - rr:.0f} {cy + s * 0.4:.0f} A{rr:.0f} {rr:.0f} 0 0 1 {cx + rr:.0f} {cy + s * 0.4:.0f}" {tr(c, sw * 1.2)}/>')
    elif tipo == "pez":
        _ap(out, f'<path d="M{cx - s * 0.55:.0f} {cy:.0f} Q{cx:.0f} {cy - s * 0.45:.0f} {cx + s * 0.4:.0f} {cy:.0f} Q{cx:.0f} {cy + s * 0.45:.0f} {cx - s * 0.55:.0f} {cy:.0f} Z" fill="#f8902a" opacity="0.85"/>'
                   f'<path d="M{cx + s * 0.35:.0f} {cy:.0f} L{cx + s * 0.75:.0f} {cy - s * 0.3:.0f} L{cx + s * 0.75:.0f} {cy + s * 0.3:.0f} Z" fill="#f8902a"/>'
                   f'<circle cx="{cx - s * 0.3:.0f}" cy="{cy - s * 0.06:.0f}" r="{s * 0.06:.0f}" fill="#1a1a1a"/>')
        for k in range(3):
            _ap(out, f'<circle cx="{cx - s * 0.6 - k * s * 0.08:.0f}" cy="{cy - s * 0.3 - k * s * 0.22:.0f}" r="{s * (0.05 + k * 0.02):.0f}" {tr("#3a7ae8", sw * 0.6)}/>')
    else:  # sol con cara sonriente simple
        _ap(out, f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{s * 0.38:.0f}" fill="#f8c830"/>')
        for k in range(10):
            a = k * math.pi / 5
            _ap(out, f'<path d="M{cx + math.cos(a) * s * 0.5:.0f} {cy + math.sin(a) * s * 0.5:.0f} L{cx + math.cos(a) * s * 0.75:.0f} {cy + math.sin(a) * s * 0.75:.0f}" {tr("#f8a030")}/>')
        _ap(out, f'<path d="M{cx - s * 0.18:.0f} {cy + s * 0.08:.0f} Q{cx:.0f} {cy + s * 0.25:.0f} {cx + s * 0.18:.0f} {cy + s * 0.08:.0f}" {tr("#8a4a10", sw * 0.7)}/>'
                   f'<circle cx="{cx - s * 0.13:.0f}" cy="{cy - s * 0.08:.0f}" r="{s * 0.04:.0f}" fill="#8a4a10"/><circle cx="{cx + s * 0.13:.0f}" cy="{cy - s * 0.08:.0f}" r="{s * 0.04:.0f}" fill="#8a4a10"/>')
    pc = r.choice(["#e83a3a", "#3a7ae8", "#3aa04a", "#f8c830"])
    _ap(out, f'<circle cx="{cx + 2:.0f}" cy="{y + 10:.0f}" r="7" fill="#000" opacity="0.3"/><circle cx="{cx:.0f}" cy="{y + 8:.0f}" r="6" fill="{pc}"/><circle cx="{cx - 2:.0f}" cy="{y + 6:.0f}" r="2" fill="#fff" opacity="0.7"/>')
    _ap(out, "</g>")
    return "".join(out)


def _corcho(L, x0, y0, x1, y1, r):
    out = [_rect(x0 + 8, y0 + 10, x1 - x0, y1 - y0, "#000", 0.2),
           _rect(x0 - 10, y0 - 10, x1 - x0 + 20, y1 - y0 + 20, L.lg((0, "#c89a64"), (1, "#7a5430"))),
           _rect(x0, y0, x1 - x0, y1 - y0, L.lg((0, "#d4a26a"), (1, "#b07a44"), x2=1, y2=1))]
    pts = "".join(f'<circle cx="{r.uniform(x0, x1):.0f}" cy="{r.uniform(y0, y1):.0f}" r="{r.uniform(1, 2.6):.1f}" fill="{r.choice(["#7a4a20", "#e8c08a"])}" opacity="0.5"/>'
                  for _ in range(int((x1 - x0) * (y1 - y0) / 400)))
    _ap(out, pts)
    tipos = ["casa", "sol", "flor", "arcoiris", "arbol", "pez"]
    r.shuffle(tipos)
    n = max(3, int((x1 - x0) / 120))
    filas = 1 if (y1 - y0) < 200 else 2
    k = 0
    for f in range(filas):
        for i in range(n):
            pw = (x1 - x0) / n * 0.8
            ph = (y1 - y0) / filas * 0.78
            px = x0 + (x1 - x0) * i / n + (x1 - x0) / n * 0.1 + r.uniform(-4, 4)
            py = y0 + (y1 - y0) * f / filas + (y1 - y0) / filas * 0.12 + r.uniform(-4, 4)
            _ap(out, _dibujo_nino(L, px, py, pw, ph, tipos[k % len(tipos)], r, r.uniform(-6, 6)))
            k += 1
    return "".join(out)


def _radiador(x0, y0, x1, y1):
    out = [_rect(x0 + 6, y0 + 8, x1 - x0, y1 - y0, "#000", 0.18), _rect(x0, y0, x1 - x0, y1 - y0, "#ece8e0")]
    n = int((x1 - x0) / 16)
    for k in range(n):
        x = x0 + 4 + k * (x1 - x0 - 8) / n
        _ap(out, _rect(x, y0 + 4, 4, y1 - y0 - 8, "#b8b2a6", 0.7))
        _ap(out, _rect(x + 5, y0 + 4, 2, y1 - y0 - 8, "#ffffff", 0.7))
    _ap(out, _rect(x0, y0, x1 - x0, 5, "#ffffff", 0.8))
    return "".join(out)


def _estanteria(L, x0, y0, x1, y1, r, baldas=3, madera=("#a8784a", "#5a3a20")):
    out = [_rect(x0 + 8, y0 + 8, x1 - x0, y1 - y0, "#000", 0.2), _rect(x0, y0, x1 - x0, y1 - y0, madera[1]),
           _rect(x0 + 10, y0 + 10, x1 - x0 - 20, y1 - y0 - 20, mezcla(madera[1], "#000000", 0.35))]
    cols = ["#c0392b", "#2f6fb0", "#3a8a5e", "#e0a92e", "#6a3a7a", "#e07a3a", "#2a7f9e", "#d8d0c0"]
    for b in range(baldas):
        yb_ = y0 + 10 + (y1 - y0 - 20) * (b + 1) / baldas
        ytop = y0 + 10 + (y1 - y0 - 20) * b / baldas
        x = x0 + 14
        while x < x1 - 30:
            bw = r.uniform(10, 22)
            bh = (yb_ - ytop - 12) * r.uniform(0.65, 0.95)
            c = r.choice(cols)
            if r.random() < 0.08:
                x += 20
                continue
            inc = 0 if r.random() < 0.85 else r.uniform(-12, 12)
            _ap(out, f'<g transform="rotate({inc:.0f} {x + bw / 2:.0f} {yb_:.0f})">' + _rect(x, yb_ - bh, bw, bh, c) +
                       _rect(x + 2, yb_ - bh + 4, 2, bh - 8, "#ffffff", 0.3) + _rect(x, yb_ - bh * 0.8, bw, 3, mezcla(c, "#000000", 0.4)) + "</g>")
            x += bw + 1
        _ap(out, _rect(x0 + 10, yb_, x1 - x0 - 20, 8, madera[0]))
        _ap(out, _rect(x0 + 10, yb_ + 8, x1 - x0 - 20, 3, "#000", 0.3))
    _ap(out, _rect(x0, y0, x1 - x0, 6, madera[0]))
    return "".join(out)


def bg_aula(L, sem=501):
    """Aula de colegio de día: pizarra verde con garabatos, ventanas con luz cálida en diagonal, corcho con dibujos, reloj."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    S = lambda a, b: a if V else b  # noqa: E731
    yb = S(1180, 720)            # línea pared/suelo
    yh = S(650, 420)             # altura de los ojos
    ytecho = S(140, 44)
    yz = yb - S(220, 150)        # zócalo
    cx = w * 0.5
    # pared y techo
    L.add(L.rect(L.lg((0, "#f6e8c6"), (0.55, "#ecd8ae"), (1, "#d8bd8c"), x2=1, y2=0.25), h=yb + 2))
    L.add(L.relieve(sem + 1, freq="0.006 0.004", escala=2.2, az=225, elev=60, op=0.35, oct=3, modo="soft-light", caja=(0, 0, w, yb)))
    L.add(_rect(0, 0, w, ytecho, L.lg((0, "#cfc8b8"), (1, "#e8e0cc"))))
    L.add(_rect(0, ytecho - 4, w, 12, "#c8b48e"), _rect(0, ytecho + 8, w, 6, "#000", 0.08))
    for x in S([w * 0.28, w * 0.72], [w * 0.22, w * 0.5, w * 0.78]):
        L.add(_rect(x - S(110, 120), S(40, 6), S(220, 240), S(26, 16), "#f4f6f2"), _rect(x - S(110, 120), S(64, 20), S(220, 240), 4, "#a8a49a"))
    if V:   # guirnalda de recortes de papel (estrellas y círculos de colores) bajo el techo
        pts = [(20 + k * 1040 / 10, 230 + 40 * math.sin(k * math.pi / 5) ** 2) for k in range(11)]
        L.add(f'<path d="{suave(pts, cerrado=False)}" stroke="#6a5a4a" stroke-width="2" fill="none"/>')
        for k in range(15):
            t = (k + 0.5) / 15
            x = 20 + 1040 * t
            y = 230 + 40 * math.sin(t * 10 * math.pi / 5) ** 2 + 4
            c = ["#e84a3a", "#f8c830", "#3a8ae8", "#3aa04a", "#e86aa8"][k % 5]
            if k % 2:
                pe = [(x + math.cos(-math.pi / 2 + j * math.pi / 5) * (26 if j % 2 == 0 else 11), y + 28 + math.sin(-math.pi / 2 + j * math.pi / 5) * (26 if j % 2 == 0 else 11)) for j in range(10)]
                L.add(_poly([(px + 4, py + 6) for px, py in pe], 'fill="#000" opacity="0.15"'), _poly(pe, f'fill="{c}"'))
            else:
                L.add(f'<circle cx="{x + 4:.0f}" cy="{y + 30:.0f}" r="20" fill="#000" opacity="0.15"/><circle cx="{x:.0f}" cy="{y + 26:.0f}" r="20" fill="{c}"/>'
                      f'<circle cx="{x - 6:.0f}" cy="{y + 20:.0f}" r="6" fill="#ffffff" opacity="0.35"/>')
    # zócalo pintado
    L.add(_rect(0, yz, w, yb - yz, L.lg((0, "#9ab49a"), (1, "#6f8c72"))), _rect(0, yz - 6, w, 12, "#5e7a62"), _rect(0, yz - 6, w, 3, "#c8dcc4"))
    # ventanas
    vens = [(40, 400, 300, 980)] if V else [(70, 120, 340, 540), (420, 120, 690, 540)]
    for (x0, y0, x1, y1) in vens:
        L.add(_rect(x0 - 26, y0 - 26, x1 - x0 + 52, y1 - y0 + 52, "#000", 0.1))
        L.add(_vista_fuera(L, x0, y0, x1, y1, r, "dia"))
        L.add(_marco_ventana(x0, y0, x1, y1, 2, 3, L.lg((0, "#ffffff"), (1, "#d8d4cc"), x2=1, y2=0), 16, "#f0ece4"))
        L.add(L.brillo((x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) * 0.9, (y1 - y0) * 0.7, "#fff4d0", 0.35))
        # radiador bajo la ventana
        L.add(_radiador(x0 + 10, y1 + S(50, 46), x1 - 10, y1 + S(150, 120)))
    # pizarra
    px0, py0, px1, py1 = (340, 640, 1040, 940) if V else (770, 240, 1440, 540)
    L.add(_rect(px0 + 10, py0 + 14, px1 - px0, py1 - py0, "#000", 0.25))
    L.add(_rect(px0 - 16, py0 - 16, px1 - px0 + 32, py1 - py0 + 32, L.lg((0, "#c8a070"), (1, "#7a5430"))))
    L.add(_rect(px0, py0, px1 - px0, py1 - py0, L.lg((0, "#3a6a54"), (0.6, "#2c5644"), (1, "#22463a"), x2=1, y2=1)))
    L.add(_tiza(r, px0 + 20, py0 + 20, px1 - 20, py1 - 20))
    L.add(L.brillo(px0 + (px1 - px0) * 0.25, py0 + 40, (px1 - px0) * 0.4, 60, "#ffffff", 0.12))
    L.add(_rect(px0 - 24, py1 + 14, px1 - px0 + 48, 14, L.lg((0, "#a07a50"), (1, "#5a3a20"))))
    for k in range(4):   # tizas y borrador en la repisa
        L.add(_rect(px0 + 60 + k * 34, py1 + 6, 24, 8, ["#ffffff", "#f8e070", "#ffffff", "#f0a0b0"][k], extra='rx="3"'))
    L.add(_rect(px1 - 170, py1 + 2, 90, 14, "#3a3030", extra='rx="3"'), _rect(px1 - 170, py1 + 12, 90, 5, "#d8d0c0"))
    # corcho con dibujos y reloj
    if V:
        L.add(_corcho(L, 360, 430, 790, 590, r))
        L.add(_reloj(L, 925, 515, 62, r, marco=("#e8e8e8", "#8a8a8a"), cara="#fbf8ee"))
    else:
        L.add(_corcho(L, 1520, 180, 1860, 470, r))
        L.add(_reloj(L, 1105, 138, 50, r, marco=("#e8e8e8", "#8a8a8a"), cara="#fbf8ee"))
        L.add(_estanteria(L, 1530, 540, 1860, yb - 4, r, baldas=1))
    # suelo de tarima y luz de las ventanas
    suelo, P = _suelo(L, yb, yh, cx, "tarima", ["#b8834e", "#a87244", "#c8925a", "#9a6a3e"], ("#a8744a", "#6a4228"), sem + 2, a=S(78, 74))
    L.add(suelo)
    L.add(L.relieve(sem + 3, freq="0.004 0.05", escala=2, az=180, elev=60, op=0.3, oct=3, modo="soft-light", caja=(0, yb, w, h - yb)))
    for (x0, y0, x1, y1) in vens:
        L.add(_luz_ventana(L, (x0, y0, x1, y1), 2, 3, yb + S(30, 20), yb + S(520, 300), S(380, 420), cx, yh, yb,
                           color="#ffe2a8", op=0.4, haz=0.2, polvo=S(60, 50), sem=sem + 4))
    L.add(L.luz(S(170, 380), S(700, 330), S(700, 900), S(700, 500), "#ffcf8a", 0.35))
    L.add(L.oscuridad(w * 0.5, yb - S(250, 150), w * 0.95, h * 0.75, color="#2a1808", op=0.45, medio=0.12))
    return {"suelo": S(1420, 870), "centro": (round(cx), S(1300, 800)),
            "nota": f"pared/suelo y={yb}; pizarra ({px0},{py0})–({px1},{py1}); suelo de tarima despejado en el centro"}


# ============================================================================ 2. colegio por fuera
def _ventana_fach(L, x, y, ww, hh, r, marco="#f4efe6", persiana=None, reflejo=("#8ec4ea", "#e6f2fa"), balcon=None, luz=-1, sombra=0.25):
    out = [_rect(x - 8, y - 8, ww + 16, hh + 16, "#000", 0.18)]
    _ap(out, _rect(x, y, ww, hh, L.lg((0, reflejo[0]), (1, reflejo[1]), x1=0, y1=0, x2=0.4, y2=1)))
    _ap(out, _rect(x, y + hh * 0.55, ww, hh * 0.45, "#203040", 0.35))
    _ap(out, _poly([(x + ww * 0.15, y), (x + ww * 0.45, y), (x + ww * 0.05, y + hh), (x, y + hh), (x, y + hh * 0.6)], 'fill="#ffffff" opacity="0.28"'))
    if persiana:
        ph = hh * persiana
        _ap(out, _rect(x, y, ww, ph, "#e0d8c4"))
        for k in range(int(ph / 7)):
            _ap(out, _rect(x, y + k * 7 + 5, ww, 1.5, "#8a8070", 0.6))
        _ap(out, _rect(x, y + ph - 4, ww, 5, "#7a7060"))
    _ap(out, _rect(x, y, ww, 6, "#000", 0.25))
    g = 6 if ww > 60 else 4
    for xx in (x - g / 2, x + ww / 2 - g / 2, x + ww - g / 2):
        _ap(out, _rect(xx, y - g / 2, g, hh + g, marco))
    for yy in (y - g / 2, y + hh * 0.38, y + hh - g / 2):
        _ap(out, _rect(x - g / 2, yy, ww + g, g, marco))
    _ap(out, _rect(x - 10, y + hh, ww + 20, 9, mezcla(marco, "#000000", 0.08)), _rect(x - 10, y + hh + 9, ww + 20, 6, "#000", 0.2))
    if balcon:
        by = y + hh + 4
        _ap(out, _poly([(x - 22, by + 14), (x + ww + 22, by + 14), (x + ww + 22 + 30 * -luz, by + 14 + 60), (x - 22 + 30 * -luz, by + 14 + 60)], f'fill="#000" opacity="{sombra}"'))
        _ap(out, _rect(x - 24, by, ww + 48, 14, mezcla(balcon, "#ffffff", 0.2)), _rect(x - 24, by + 14, ww + 48, 5, "#000", 0.3))
        bh = hh * 0.42
        _ap(out, _rect(x - 22, by - bh, ww + 44, 4, "#1e2228"))
        for k in range(int((ww + 44) / 9) + 1):
            _ap(out, _rect(x - 22 + k * 9, by - bh, 2.2, bh, "#1e2228"))
        _ap(out, _poly([(x - 22, by - bh), (x + ww + 22, by - bh), (x + ww + 22 + 24 * -luz, by - bh + 70), (x - 22 + 24 * -luz, by - bh + 70)], 'fill="#000" opacity="0.06"'))
        if r.random() < 0.6:   # macetas con flores
            for k in range(r.randint(1, 3)):
                mx = x - 10 + r.uniform(0, ww + 20)
                fc = r.choice(["#e84a5a", "#f8a8c0", "#f8d040", "#ffffff"])
                _ap(out, f'<path d="M{mx - 12:.0f} {by - 22:.0f} L{mx + 12:.0f} {by - 22:.0f} L{mx + 9:.0f} {by:.0f} L{mx - 9:.0f} {by:.0f} Z" fill="#c0663a"/>')
                for j in range(7):
                    _ap(out, f'<circle cx="{mx + r.uniform(-16, 16):.0f}" cy="{by - 26 - r.uniform(0, 16):.0f}" r="{r.uniform(4, 7):.0f}" fill="{"#3f7a34" if j < 4 else fc}"/>')
    return "".join(out)


def _verja(L, x0, x1, yb, alto, hueco=None, col="#2e6a4a", luz="#7ab890"):
    """Verja de barrotes con punta de lanza, dos travesaños y pilares; `hueco`=(xa,xb) puerta abierta hacia dentro."""
    out = []
    paso = 22
    x = x0
    while x < x1:
        if hueco and hueco[0] < x < hueco[1]:
            x += paso
            continue
        _ap(out, _rect(x, yb - alto, 5, alto, col), _rect(x, yb - alto, 1.6, alto, luz, 0.6))
        _ap(out, f'<path d="M{x - 3:.1f} {yb - alto:.1f} L{x + 2.5:.1f} {yb - alto - 16:.1f} L{x + 8:.1f} {yb - alto:.1f} Z" fill="{col}"/>')
        x += paso
    segs = [(x0, x1)] if not hueco else [(x0, hueco[0]), (hueco[1], x1)]
    for a, b in segs:
        for yy in (yb - alto + 18, yb - 26):
            _ap(out, _rect(a, yy, b - a, 8, col), _rect(a, yy, b - a, 2, luz, 0.6))
    if hueco:
        for xp in hueco:
            _ap(out, _rect(xp - 14, yb - alto - 30, 28, alto + 30, L.lg((0, luz), (0.4, col), (1, mezcla(col, "#000000", 0.4)), x2=1, y2=0)))
            _ap(out, _rect(xp - 20, yb - alto - 40, 40, 12, mezcla(col, "#000000", 0.2)), f'<circle cx="{xp}" cy="{yb - alto - 48}" r="10" fill="{col}"/>')
        # hojas de la puerta abiertas hacia dentro (escorzadas)
        for xp, lado in ((hueco[0], 1), (hueco[1], -1)):
            ancho = (hueco[1] - hueco[0]) * 0.22
            xf = xp + lado * ancho
            top0, top1 = yb - alto, yb - alto - 22
            bot1 = yb - 34
            _ap(out, _poly([(xp, top0 + 10), (xf, top1 + 10), (xf, bot1), (xp, yb - 6)], f'fill="none" stroke="{col}" stroke-width="7"'))
            for k in range(1, 6):
                t = k / 6
                xx = xp + lado * ancho * t
                _ap(out, f'<path d="M{xx:.0f} {top0 + 10 + (top1 - top0) * t:.0f} L{xx:.0f} {yb - 6 + (bot1 - yb + 6) * t:.0f}" stroke="{col}" stroke-width="{4 - t * 1.5:.1f}"/>')
    return "".join(out)


def _campana(L, x, y, s):
    """Timbre/campana de colegio: campana de bronce sobre soporte de hierro anclado a la fachada."""
    out = [_rect(x - 30 * s, y - 6 * s, 60 * s, 12 * s, "#2a2e36"),
           f'<path d="M{x:.0f} {y:.0f} L{x:.0f} {y + 26 * s:.0f}" stroke="#2a2e36" stroke-width="{6 * s:.1f}"/>',
           f'<ellipse cx="{x + 14 * s:.0f}" cy="{y + 96 * s:.0f}" rx="{58 * s:.0f}" ry="{12 * s:.0f}" fill="#000" opacity="0.15"/>',
           f'<path d="M{x - 40 * s:.0f} {y + 86 * s:.0f} C{x - 40 * s:.0f} {y + 50 * s:.0f} {x - 30 * s:.0f} {y + 24 * s:.0f} {x:.0f} {y + 24 * s:.0f} '
           f'C{x + 30 * s:.0f} {y + 24 * s:.0f} {x + 40 * s:.0f} {y + 50 * s:.0f} {x + 40 * s:.0f} {y + 86 * s:.0f} Z" '
           f'fill="{L.lg((0, "#f4d48a"), (0.35, "#d0a040"), (1, "#6a4a14"), x2=1, y2=0)}"/>',
           f'<ellipse cx="{x:.0f}" cy="{y + 86 * s:.0f}" rx="{42 * s:.0f}" ry="{8 * s:.0f}" fill="#4a3410"/>',
           f'<ellipse cx="{x:.0f}" cy="{y + 84 * s:.0f}" rx="{42 * s:.0f}" ry="{6 * s:.0f}" fill="none" stroke="#f8e0a0" stroke-width="{2 * s:.1f}" opacity="0.6"/>',
           f'<circle cx="{x:.0f}" cy="{y + 92 * s:.0f}" r="{7 * s:.0f}" fill="#3a2a10"/>',
           f'<path d="M{x - 22 * s:.0f} {y + 76 * s:.0f} C{x - 24 * s:.0f} {y + 52 * s:.0f} {x - 18 * s:.0f} {y + 36 * s:.0f} {x - 8 * s:.0f} {y + 32 * s:.0f}" stroke="#fff4d0" stroke-width="{4 * s:.1f}" opacity="0.6" fill="none" stroke-linecap="round"/>',
           f'<path d="M{x - 40 * s:.0f} {y + 60 * s:.0f} L{x + 40 * s:.0f} {y + 60 * s:.0f}" stroke="#8a6420" stroke-width="{2 * s:.1f}" opacity="0.5"/>']
    return "".join(out)


def bg_colegio_fuera(L, sem=511):
    """Fachada de colegio de día: dos plantas, campana sobre la puerta, espadaña, patio, verja abierta, árboles y cielo con nubes."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    S = lambda a, b: a if V else b  # noqa: E731
    yed = S(1050, 590)       # base del edificio
    yv = S(1250, 740)        # base de la verja / borde de la acera
    yh = S(900, 520)
    cx = w * 0.5
    # cielo y nubes
    L.add(L.rect(L.lg((0, "#3f8fd8"), (0.55, "#7cbcec"), (1, "#d6ecf8")), h=yed + 10))
    L.add(L.luz(-w * 0.1, -h * 0.05, w * 0.9, h * 0.5, "#fff4d0", 0.5))
    for k in range(S(4, 6)):
        L.add(_nube(L, r.uniform(0, w), r.uniform(S(140, 60), S(460, 230)), r.uniform(0.6, 1.1) * S(1, 0.9), r, op=0.92))
    # árboles y tejados lejanos a los lados
    for k in range(S(5, 9)):
        x = r.uniform(-40, w + 40)
        hx = r.uniform(80, 140)
        L.add(_rect(x - hx, yed - S(110, 80), hx * 2, S(110, 80), "#b8a898"),
              _poly([(x - hx - 10, yed - S(110, 80)), (x, yed - S(150, 110)), (x + hx + 10, yed - S(110, 80))], 'fill="#b07a62"'))
    for k in range(S(10, 16)):
        x = r.uniform(-40, w + 40)
        L.add(_arbol(L, x, yed, r.uniform(0.35, 0.5), r, hojas=("#7a9a7a", "#8aac84", "#a8c49a"), tronco=("#8a8478", "#9a948a"), sombra=False))
    L.add(L.bruma(yed - S(40, 30), S(100, 70), "#d6ecf8", 0.6))
    # edificio
    bx0, bx1 = (-30, w + 30) if V else (260, 1660)
    pl = S(220, 140)                 # altura de planta
    ytop = yed - 2 * pl - S(40, 30)
    tx0, tx1 = cx - S(190, 170), cx + S(190, 170)   # cuerpo central
    ttop = ytop - S(90, 60)
    gf = L.lg((0, "#f6e2b4"), (0.5, "#ecd29c"), (1, "#c8a670"), x2=1, y2=0)
    L.add(_rect(bx0 + 14, ytop + 10, bx1 - bx0, yed - ytop, "#000", 0.12))
    L.add(_rect(bx0, ytop, bx1 - bx0, yed - ytop, gf))
    L.add(_rect(tx0, ttop, tx1 - tx0, yed - ttop, L.lg((0, "#fae8c0"), (1, "#d8b880"), x2=1, y2=0)))
    L.add(_rect(tx1, ttop, 14, yed - ttop, "#000", 0.12))
    # espadaña con campana pequeña
    ex, ey = cx, ttop
    L.add(f'<path d="M{ex - 70:.0f} {ey:.0f} L{ex - 70:.0f} {ey - 90:.0f} Q{ex:.0f} {ey - 150:.0f} {ex + 70:.0f} {ey - 90:.0f} L{ex + 70:.0f} {ey:.0f} Z" fill="{L.lg((0, "#fae8c0"), (1, "#d0ae78"), x2=1, y2=0)}"/>'
          f'<path d="M{ex - 34:.0f} {ey - 6:.0f} L{ex - 34:.0f} {ey - 80:.0f} Q{ex:.0f} {ey - 112:.0f} {ex + 34:.0f} {ey - 80:.0f} L{ex + 34:.0f} {ey - 6:.0f} Z" fill="#5a7ea0" opacity="0.55"/>')
    L.add(_campana(L, ex, ey - 96, 0.55))
    L.add(f'<path d="M{ex - 76:.0f} {ey - 88:.0f} Q{ex:.0f} {ey - 158:.0f} {ex + 76:.0f} {ey - 88:.0f}" stroke="#b08850" stroke-width="8" fill="none"/>')
    # cornisas y zócalo de ladrillo
    for (a, b, y) in ((bx0, bx1, ytop), (tx0 - 10, tx1 + 10, ttop)):
        L.add(_rect(a - 10, y - 14, b - a + 20, 18, "#e8d4a8"), _rect(a - 10, y + 4, b - a + 20, 8, "#000", 0.18))
    L.add(_rect(bx0, yed - pl - 10, bx1 - bx0, 10, "#d8be8a"))
    zh = S(60, 42)
    L.add(_rect(bx0, yed - zh, bx1 - bx0, zh, L.lg((0, "#b8643e"), (1, "#7a3a22"))))
    for j in range(int(zh / 12)):
        for i in range(int((bx1 - bx0) / 40) + 1):
            L.add(_rect(bx0 + i * 40 + (20 if j % 2 else 0), yed - zh + j * 12, 38, 10, "#c8744a", 0.5))
    # ventanas (dos plantas), ninguna en el cuerpo central salvo la de arriba
    vw, vh = S(110, 80), S(140, 92)
    for planta in range(2):
        yv0 = yed - (planta + 1) * pl + S(40, 26)
        xs = []
        x = bx0 + S(50, 40)
        while x + vw < bx1 - 30:
            if not (tx0 - 20 < x + vw and x < tx1 + 20):
                xs.append(x)
            x += vw + S(60, 46)
        for x in xs:
            L.add(_ventana_fach(L, x, yv0, vw, vh, r, persiana=r.choice([None, 0.3, 0.5]) if r.random() < 0.5 else None))
    oy, orr = yed - 2 * pl + S(70, 46), S(50, 34)
    L.add(f'<circle cx="{cx:.0f}" cy="{oy:.0f}" r="{orr + 14:.0f}" fill="#e8d0a0"/><circle cx="{cx + 4:.0f}" cy="{oy + 4:.0f}" r="{orr:.0f}" fill="#000" opacity="0.2"/>'
          f'<circle cx="{cx:.0f}" cy="{oy:.0f}" r="{orr:.0f}" fill="{L.lg((0, "#8ec4ea"), (1, "#e6f2fa"))}"/>'
          f'<path d="M{cx - orr:.0f} {oy:.0f} L{cx + orr:.0f} {oy:.0f} M{cx:.0f} {oy - orr:.0f} L{cx:.0f} {oy + orr:.0f}" stroke="#f4efe6" stroke-width="6"/>'
          f'<circle cx="{cx:.0f}" cy="{oy:.0f}" r="{orr:.0f}" fill="none" stroke="#f4efe6" stroke-width="7"/>'
          f'<path d="M{cx - orr * 0.6:.0f} {oy - orr * 0.3:.0f} L{cx - orr * 0.2:.0f} {oy - orr * 0.7:.0f}" stroke="#ffffff" stroke-width="6" opacity="0.5"/>')
    # puerta central con marquesina y campana (timbre)
    dw, dh = S(220, 170), S(170, 118)
    dx0, dy0 = cx - dw / 2, yed - dh
    L.add(_rect(dx0 - 16, dy0 - 16, dw + 32, dh + 16, "#d8bc88"))
    L.add(_rect(dx0, dy0, dw, dh, L.lg((0, "#3a6a50"), (1, "#24463a"))))
    for k in (0, 1):
        L.add(_rect(dx0 + 12 + k * dw / 2, dy0 + 12, dw / 2 - 24, dh * 0.45, "#9ac8e0", 0.85), _rect(dx0 + 12 + k * dw / 2, dy0 + dh * 0.62, dw / 2 - 24, dh * 0.3, "#000", 0.12))
    L.add(_rect(cx - 2, dy0, 4, dh, "#1a2a22"), _rect(cx - 16, dy0 + dh * 0.55, 8, 20, "#d0b070"), _rect(cx + 8, dy0 + dh * 0.55, 8, 20, "#d0b070"))
    L.add(_poly([(dx0 - 50, dy0 - 30), (dx0 + dw + 50, dy0 - 30), (dx0 + dw + 70, dy0 - 6), (dx0 - 70, dy0 - 6)], 'fill="#9a3a2a"'),
          _rect(dx0 - 70, dy0 - 6, dw + 140, 8, "#6a2418"), _poly([(dx0 - 70, dy0 + 2), (dx0 + dw + 70, dy0 + 2), (dx0 + dw + 90, dy0 + 40), (dx0 - 40, dy0 + 40)], 'fill="#000" opacity="0.15"'))
    L.add(_campana(L, cx, dy0 - S(120, 92), S(1.0, 0.75)))
    # escalones
    for k in range(2):
        L.add(_rect(dx0 - 30 - k * 20, yed + k * 10, dw + 60 + k * 40, 10, ["#d8d0c0", "#c8c0b0"][k]), _rect(dx0 - 30 - k * 20, yed + k * 10 + 8, dw + 60 + k * 40, 3, "#000", 0.2))
    # patio: hormigón claro con rayuela pintada
    L.add(_rect(-10, yed, w + 20, yv - yed + 10, L.lg((0, "#d8ccb4"), (1, "#c4b496"))))
    L.add(_rect(-10, yed, w + 20, 14, "#000", 0.12))
    for k in range(4):
        x0 = S(150, 520) + k * S(46, 40)
        L.add(_poly([(x0, yv - S(50, 30)), (x0 + S(40, 36), yv - S(50, 30)), (x0 + S(36, 32), yv - S(90, 56)), (x0 - 4, yv - S(90, 56))], 'fill="none" stroke="#f4f4f0" stroke-width="3" opacity="0.8"'))
    # árboles del patio a los lados (no tapan la puerta)
    for (x, s) in (((60, 1.05), (1010, 1.0)) if V else ((110, 0.95), (1820, 1.0), (330, 0.7), (1600, 0.72))):
        L.add(_arbol(L, x, yed + S(70, 50), s * S(1.15, 0.95), r, luz=-1))
    # verja abierta
    gx0, gx1 = cx - S(170, 150), cx + S(170, 150)
    L.add(_verja(L, -20, w + 20, yv, S(150, 100), hueco=(gx0, gx1)))
    # acera delante (baldosa gris) con sombra de la verja
    suelo, P = _suelo(L, yv, yh, cx, "damero", ["#c8c4bc", "#bcb8b0"], ("#c4c0b8", "#8a8680"), sem + 3, a=S(90, 80), junta="#7a766e", op_pieza=0.7)
    L.add(suelo)
    L.add(_rect(-10, yv, w + 20, 16, "#e8e4dc"), _rect(-10, yv + 16, w + 20, 6, "#000", 0.2))
    L.add(L.relieve(sem + 4, freq="0.02 0.04", escala=2, az=225, elev=55, op=0.2, oct=3, modo="soft-light", caja=(0, yv, w, h - yv)))
    sh = "".join(f'<ellipse cx="{r.uniform(-100, w + 100):.0f}" cy="{r.uniform(yv + S(260, 150), h + 40):.0f}" rx="{r.uniform(40, 120):.0f}" ry="{r.uniform(14, 36):.0f}" fill="#4a5058" opacity="{r.uniform(0.05, 0.11):.2f}"/>' for _ in range(S(26, 34)))
    L.add(f'<g filter="url(#blur8)">{sh}</g>')
    for _ in range(S(14, 18)):   # hojas caídas
        x, y = r.uniform(0, w), r.uniform(yv + 40, h)
        L.add(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(6, 10):.0f}" ry="{r.uniform(3, 5):.0f}" transform="rotate({r.uniform(0, 180):.0f} {x:.0f} {y:.0f})" fill="{r.choice(["#c89a3a", "#a8702a", "#8aa040"])}" opacity="0.85"/>')
    L.add(L.luz(w * 0.3, yv + S(200, 120), w * 0.8, S(300, 200), "#fff0c8", 0.3))
    L.add(L.oscuridad(cx, S(900, 520), w * 0.95, h * 0.8, color="#1a2a3a", op=0.35, medio=0.1))
    return {"suelo": S(1430, 880), "centro": (round(cx), S(900, 520)), "nota": f"verja y={yv}, puerta abierta x {gx0:.0f}–{gx1:.0f}; campana sobre la puerta"}


# ============================================================================ 3. calle de día
def bg_calle_dia(L, sem=521):
    """Calle de barrio por la mañana: edificios bajos con balcones, árboles, farolas, coches aparcados al fondo, acera ancha."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    S = lambda a, b: a if V else b  # noqa: E731
    yfa = S(1080, 600)       # acera de enfrente (base de los edificios)
    yca = S(1110, 620)       # bordillo de enfrente
    ycn = S(1260, 730)       # bordillo de este lado
    yh = S(880, 470)
    cx = w * 0.5
    L.add(L.rect(L.lg((0, "#4a9ad8"), (0.5, "#8cc4ec"), (1, "#f4e4c4")), h=yfa))
    L.add(L.luz(-w * 0.05, S(200, 60), w * 0.9, S(800, 500), "#ffe4b0", 0.55))
    for k in range(S(3, 5)):
        L.add(_nube(L, r.uniform(0, w), r.uniform(S(120, 50), S(300, 150)), r.uniform(0.5, 0.9), r, op=0.85))
    # fondo lejano: bloques pálidos
    L.add(IE._edificios(L, r, yfa - S(300, 200), 70, 140, 80, 220, "#b8c4d4", ["#d8e2ec"], "#a8b4c4", 0.05, 1.0))
    L.add(L.bruma(yfa - S(320, 220), S(160, 110), "#e8eef4", 0.6))
    # fachadas de enfrente
    paleta = [("#e8b480", "#b07a48"), ("#f0d8b0", "#c0a070"), ("#d88a6a", "#9a5a40"), ("#f2e6d0", "#c4b494"), ("#e8c8c0", "#b08a80"), ("#c8d0a8", "#8a9470")]
    x = -r.uniform(20, 80)
    pl = S(150, 92)
    while x < w + 20:
        bw = r.uniform(S(300, 260), S(420, 380))
        np_ = r.randint(3, 4) if V else r.randint(2, 4)
        bh = S(170, 120) + np_ * pl
        yt = yfa - bh
        c, cs = r.choice(paleta)
        L.add(_rect(x, yt, bw + 2, bh, L.lg((0, mezcla(c, "#fff4e0", 0.25)), (1, cs), x2=1, y2=0.3)))
        L.add(_rect(x - 8, yt - 16, bw + 18, 18, mezcla(c, "#ffffff", 0.3)), _rect(x - 8, yt + 2, bw + 18, 8, "#000", 0.2))
        L.add(_rect(x + bw - 6, yt, 8, bh, "#000", 0.12))
        # bajo: local con persiana o escaparate y toldo
        gb = S(170, 120)
        lx0, lx1 = x + 30, x + bw - 30
        if r.random() < 0.5:
            L.add(_rect(lx0, yfa - gb + 30, lx1 - lx0, gb - 30, "#a8acb0"))
            for k in range(int((gb - 30) / 8)):
                L.add(_rect(lx0, yfa - gb + 30 + k * 8, lx1 - lx0, 2, "#6a6e74", 0.6))
        else:
            L.add(_rect(lx0, yfa - gb + 30, lx1 - lx0, gb - 30, L.lg((0, "#5a6a78"), (1, "#2a3440"))))
            L.add(_poly([(lx0 + 20, yfa - gb + 30), (lx0 + 70, yfa - gb + 30), (lx0 + 20, yfa)], 'fill="#ffffff" opacity="0.18"'))
            tc = r.choice(["#c0392b", "#2a7f5e", "#2f5fa0", "#d08a2a"])
            ty = yfa - gb + 24
            L.add(_poly([(lx0 - 10, ty), (lx1 + 10, ty), (lx1 + 24, ty + 40), (lx0 - 24, ty + 40)], f'fill="{tc}"'))
            for k in range(int((lx1 - lx0) / 30) + 1):
                L.add(_poly([(lx0 - 10 + k * 30, ty), (lx0 + 5 + k * 30, ty), (lx0 + 2 + k * 31.5, ty + 40), (lx0 - 14 + k * 31.5, ty + 40)], 'fill="#ffffff" opacity="0.35"'))
            L.add(_poly([(lx0 - 24, ty + 40), (lx1 + 24, ty + 40), (lx1 + 50, ty + 80), (lx0, ty + 80)], 'fill="#000" opacity="0.14"'))
        # portal
        px = x + bw / 2 - 30 if r.random() < 0.5 else lx1 - 70
        # plantas con ventanas y balcones
        nv = max(2, int(bw / S(120, 110)))
        vw, vh = S(56, 44), S(92, 66)
        for p in range(np_):
            yy = yfa - gb - (p + 1) * pl + S(30, 22)
            for i in range(nv):
                vx = x + (bw / nv) * (i + 0.5) - vw / 2
                L.add(_ventana_fach(L, vx, yy, vw, vh, r, marco="#f4efe6", persiana=r.choice([None, 0.3, 0.55, 0.8]),
                                    reflejo=("#7aaed8", "#e0ecf4"), balcon=c if r.random() < 0.7 else None, luz=-1))
        # sombra arrojada por el edificio de al lado (luz desde la izquierda)
        L.add(_poly([(x + bw, yt), (x + bw + 60, yt + 60), (x + bw + 60, yfa), (x + bw, yfa)], 'fill="#3a2a40" opacity="0.12"'))
        x += bw
    # acera de enfrente
    L.add(_rect(-10, yfa, w + 20, yca - yfa, L.lg((0, "#cfc6b8"), (1, "#b4aa9a"))), _rect(-10, yfa, w + 20, 6, "#000", 0.2))
    # calzada
    L.add(_rect(-10, yca, w + 20, ycn - yca, L.lg((0, "#5a5a60"), (1, "#3e3e44"))))
    L.add(_rect(-10, yca, w + 20, 8, "#d8d4cc"), _rect(-10, yca + 8, w + 20, 4, "#000", 0.3))
    ym = (yca + ycn) / 2 + S(16, 10)
    for k in range(-1, int(w / 140) + 1):
        L.add(_poly([(k * 140, ym - 3), (k * 140 + 70, ym - 3), (k * 140 + 72, ym + 4), (k * 140 - 2, ym + 4)], 'fill="#f0ece0" opacity="0.8"'))
    # árboles, farolas y coches en la acera de enfrente
    xs_arb = [w * f for f in (S([0.1, 0.55, 0.98], [0.06, 0.32, 0.6, 0.88]))]
    for xa in xs_arb:
        L.add(_arbol(L, xa, yfa + S(16, 10), S(1.0, 0.78), r, luz=-1, alto=S(1.25, 1.1)))
    for xf in [w * f for f in (S([0.33, 0.8], [0.19, 0.46, 0.74]))]:
        L.add(_farola(xf, yfa + S(18, 12), S(330, 230), S(1.0, 0.75)))
    cols = ["#c0392b", "#e8e4dc", "#2f5fa0", "#3a3e44", "#d0a030", "#5a8a6a"]
    xs_co = S([w * 0.2, w * 0.68, w * 1.02], [w * 0.1, w * 0.4, w * 0.55, w * 0.82])
    for xc in xs_co:
        L.add(_coche(xc + r.uniform(-20, 20), yca + S(34, 24), S(0.9, 0.66), r.choice(cols), r, mira=r.choice([1, -1])))
    # acera de este lado: bordillo y baldosa de tacos
    L.add(_rect(-10, ycn - 10, w + 20, 12, "#e4e0d8"), _rect(-10, ycn + 2, w + 20, 10, "#8a867e"))
    suelo, P = _suelo(L, ycn + 12, yh, cx, "damero", ["#d4cec4", "#c6c0b6"], ("#d0cac0", "#9a948a"), sem + 3, a=S(100, 90), junta="#8a847a", op_pieza=0.6)
    L.add(suelo)
    L.add(L.relieve(sem + 4, freq="0.05 0.05", escala=2.5, az=225, elev=55, op=0.18, oct=2, modo="soft-light", caja=(0, ycn, w, h - ycn)))
    # sombras de los árboles de este lado (fuera de cuadro) sobre la acera y luz cálida
    sh = "".join(f'<ellipse cx="{r.uniform(-100, w + 100):.0f}" cy="{r.uniform(ycn + S(300, 180), h + 40):.0f}" rx="{r.uniform(120, 240):.0f}" ry="{r.uniform(30, 60):.0f}" fill="#3a3040" opacity="0.08"/>' for _ in range(S(6, 8)))
    L.add(f'<g filter="url(#blur20)">{sh}</g>')
    sh2 = "".join(f'<ellipse cx="{r.uniform(-60, w + 60):.0f}" cy="{r.uniform(ycn + S(380, 220), h + 20):.0f}" rx="{r.uniform(30, 90):.0f}" ry="{r.uniform(10, 26):.0f}" fill="#4a4050" opacity="{r.uniform(0.04, 0.09):.2f}"/>' for _ in range(S(30, 40)))
    L.add(f'<g filter="url(#blur8)">{sh2}</g>')
    for _ in range(S(12, 16)):
        x, y = r.uniform(0, w), r.uniform(ycn + 40, h)
        L.add(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(6, 10):.0f}" ry="{r.uniform(3, 5):.0f}" transform="rotate({r.uniform(0, 180):.0f} {x:.0f} {y:.0f})" fill="{r.choice(["#c89a3a", "#a8702a", "#8aa040"])}" opacity="0.85"/>')
    L.add(_rect(w * S(0.7, 0.62), ycn + 2, S(90, 80), 10, "#3a3a40"), _rect(w * S(0.7, 0.62) + 4, ycn + 4, S(82, 72), 3, "#1a1a1e"))
    L.add(L.luz(w * 0.2, yfa - S(400, 250), w * 1.1, S(800, 500), "#ffd8a0", 0.3))
    L.add(L.luz(w * 0.1, ycn + S(250, 150), w * 1.1, S(500, 300), "#ffe0b0", 0.3))
    L.add(L.oscuridad(cx, S(1000, 560), w * 0.95, h * 0.8, color="#2a1a20", op=0.3, medio=0.08))
    return {"suelo": S(1440, 880), "centro": (round(cx), S(1260, 760)), "nota": f"bordillo de este lado y={ycn}; acera despejada debajo"}


# ============================================================================ 4–5. cafetería
def _mesa(L, x, yp, s, madera=("#c08a52", "#6a4224")):
    """Mesa redonda de madera con pie central. yp = suelo bajo la mesa."""
    R = 100 * s
    yt = yp - 190 * s
    g = L.lg((0, madera[0]), (1, madera[1]), x2=1, y2=0.3)
    return (f'<ellipse cx="{x:.0f}" cy="{yp:.0f}" rx="{R * 1.0:.0f}" ry="{R * 0.16:.0f}" fill="#000" opacity="0.3"/>'
            f'<path d="M{x - 8 * s:.0f} {yt:.0f} L{x + 8 * s:.0f} {yt:.0f} L{x + 10 * s:.0f} {yp - 14 * s:.0f} L{x - 10 * s:.0f} {yp - 14 * s:.0f} Z" fill="{madera[1]}"/>'
            f'<path d="M{x - 50 * s:.0f} {yp:.0f} Q{x:.0f} {yp - 26 * s:.0f} {x + 50 * s:.0f} {yp:.0f} Z" fill="{mezcla(madera[1], "#000000", 0.3)}"/>'
            f'<ellipse cx="{x:.0f}" cy="{yt + 8 * s:.0f}" rx="{R:.0f}" ry="{R * 0.24:.0f}" fill="{mezcla(madera[1], "#000000", 0.2)}"/>'
            f'<ellipse cx="{x:.0f}" cy="{yt:.0f}" rx="{R:.0f}" ry="{R * 0.24:.0f}" fill="{g}"/>'
            f'<ellipse cx="{x - R * 0.25:.0f}" cy="{yt - R * 0.06:.0f}" rx="{R * 0.5:.0f}" ry="{R * 0.08:.0f}" fill="#ffffff" opacity="0.18"/>'), yt


def _silla(L, x, y, s, col=("#8a5a34", "#4a2a16"), invertida=False):
    """Silla de café de madera curvada, de frente. Normal: y = suelo. Invertida: y = tablero donde apoya el asiento."""
    g = L.lg((0, col[0]), (1, col[1]), x2=1, y2=0)
    # coords locales: asiento en y=0, patas hasta +110, respaldo hasta -150
    p = [f'<path d="M-34 0 L-38 110 M34 0 L38 110 M-24 4 L-22 104 M24 4 L22 104" stroke="{col[1]}" stroke-width="7" stroke-linecap="round"/>',
         f'<path d="M-30 4 L-34 110 M30 4 L34 110" stroke="{col[0]}" stroke-width="3" opacity="0.6"/>',
         '<ellipse cx="0" cy="70" rx="34" ry="5" fill="none" stroke="#3a2010" stroke-width="4"/>',
         f'<path d="M-30 -2 C-34 -60 -40 -130 0 -150 C40 -130 34 -60 30 -2" stroke="{g}" stroke-width="9" fill="none"/>',
         f'<path d="M-22 -10 C-26 -60 -26 -110 0 -124 C26 -110 26 -60 22 -10" stroke="{col[1]}" stroke-width="5" fill="none"/>',
         f'<ellipse cx="0" cy="4" rx="44" ry="12" fill="{col[1]}"/><ellipse cx="0" cy="0" rx="44" ry="12" fill="{g}"/>',
         '<ellipse cx="-10" cy="-3" rx="22" ry="4" fill="#ffffff" opacity="0.2"/>']
    if invertida:
        return f'<g transform="translate({x:.0f} {y - 4 * s:.0f}) scale({s:.3f} {-s:.3f})">' + "".join(p) + "</g>"
    return (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{50 * s:.0f}" ry="{8 * s:.0f}" fill="#000" opacity="0.28"/>'
            f'<g transform="translate({x:.0f} {y - 110 * s:.0f}) scale({s:.3f})">' + "".join(p) + "</g>")


def _lampara(L, x, ycuelga, s, encendida=True, ytecho=0):
    g = L.lg((0, "#e8c070"), (0.4, "#b08030"), (1, "#5a3a10"), x2=1, y2=0) if encendida else L.lg((0, "#6a5630"), (0.4, "#4a3818"), (1, "#20160a"), x2=1, y2=0)
    out = [f'<path d="M{x:.0f} {ytecho:.0f} L{x:.0f} {ycuelga:.0f}" stroke="#1a1410" stroke-width="{2.5 * s:.1f}"/>',
           f'<path d="M{x - 60 * s:.0f} {ycuelga + 60 * s:.0f} C{x - 56 * s:.0f} {ycuelga + 10 * s:.0f} {x - 26 * s:.0f} {ycuelga:.0f} {x:.0f} {ycuelga:.0f} '
           f'C{x + 26 * s:.0f} {ycuelga:.0f} {x + 56 * s:.0f} {ycuelga + 10 * s:.0f} {x + 60 * s:.0f} {ycuelga + 60 * s:.0f} Z" fill="{g}"/>',
           f'<rect x="{x - 8 * s:.0f}" y="{ycuelga - 10 * s:.0f}" width="{16 * s:.0f}" height="{14 * s:.0f}" fill="#3a2a14"/>']
    if encendida:
        _ap(out, f'<ellipse cx="{x:.0f}" cy="{ycuelga + 60 * s:.0f}" rx="{58 * s:.0f}" ry="{10 * s:.0f}" fill="#fff4d0"/>')
        _ap(out, L.brillo(x, ycuelga + 64 * s, 120 * s, 60 * s, "#ffd890", 0.9))
    else:
        _ap(out, f'<ellipse cx="{x:.0f}" cy="{ycuelga + 60 * s:.0f}" rx="{58 * s:.0f}" ry="{10 * s:.0f}" fill="#2a2a30"/>')
    _ap(out, f'<path d="M{x - 40 * s:.0f} {ycuelga + 40 * s:.0f} C{x - 36 * s:.0f} {ycuelga + 16 * s:.0f} {x - 20 * s:.0f} {ycuelga + 8 * s:.0f} {x - 6 * s:.0f} {ycuelga + 6 * s:.0f}" stroke="#fff0c0" stroke-width="{3 * s:.1f}" opacity="0.6" fill="none"/>')
    return "".join(out)


def _cafetera(L, x0, yb_, ww, hh):
    g = L.lg((0, "#f0f2f4"), (0.3, "#a8acb4"), (0.6, "#e0e4ea"), (1, "#6a6e76"), x2=1, y2=0)
    out = [_rect(x0, yb_ - hh, ww, hh, g, extra='rx="8"'), _rect(x0, yb_ - hh, ww, hh * 0.18, "#2a2a30", extra='rx="6"'),
           _rect(x0 + ww * 0.08, yb_ - hh * 0.75, ww * 0.84, hh * 0.08, "#3a3a40")]
    for k in range(2):
        gx = x0 + ww * (0.3 + k * 0.4)
        _ap(out, _rect(gx - 10, yb_ - hh * 0.62, 20, 16, "#2a2a30"), _rect(gx - 4, yb_ - hh * 0.5, 8, 14, "#4a4a50"))
        _ap(out, f'<path d="M{gx - 14:.0f} {yb_ - 30:.0f} L{gx + 14:.0f} {yb_ - 30:.0f} L{gx + 11:.0f} {yb_ - 8:.0f} L{gx - 11:.0f} {yb_ - 8:.0f} Z" fill="#f8f4ec"/>')
    _ap(out, f'<circle cx="{x0 + ww * 0.85:.0f}" cy="{yb_ - hh * 0.9:.0f}" r="5" fill="#ff8a3a"/>')
    for k in range(3):   # tazas encima
        _ap(out, _rect(x0 + 10 + k * (ww - 20) / 3, yb_ - hh - 20, (ww - 20) / 3 - 6, 20, "#f8f4ec", extra='rx="3"'))
    return "".join(out)


def _cafe(L, triste, sem):
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    S = lambda a, b: a if V else b  # noqa: E731
    yb = S(1200, 740)
    yh = S(660, 420)
    ytecho = S(150, 56)
    cx = w * 0.5
    # pared verde azulada con papel de rombos y zócalo de madera
    L.add(L.rect(L.lg((0, "#2e5e56"), (0.6, "#2a5049"), (1, "#1e3a36"), x2=1, y2=0.2), h=yb + 2))
    pid = L.p + "romb"
    L.defs.append(f'<pattern id="{pid}" width="44" height="60" patternUnits="userSpaceOnUse"><path d="M22 6 L34 30 L22 54 L10 30 Z" fill="none" stroke="#e8d8a8" stroke-width="1.2" opacity="0.16"/>'
                  f'<circle cx="0" cy="0" r="2" fill="#e8d8a8" opacity="0.25"/><circle cx="44" cy="0" r="2" fill="#e8d8a8" opacity="0.25"/></pattern>')
    L.add(L.rect(f"url(#{pid})", h=yb))
    L.add(L.relieve(sem + 1, freq="0.006 0.005", escala=2, az=225, elev=60, op=0.3, oct=3, modo="soft-light", caja=(0, 0, w, yb)))
    yz = yb - S(200, 140)
    L.add(_rect(0, yz, w, yb - yz, L.lg((0, "#7a4a2a"), (1, "#4a2a16"))), _rect(0, yz - 8, w, 12, "#a87444"))
    for k in range(int(w / 90) + 1):
        L.add(_rect(k * 90 + 12, yz + 16, 66, yb - yz - 32, "none", extra='stroke="#2a160a" stroke-width="3" opacity="0.4"'))
    # techo con vigas
    L.add(_rect(0, 0, w, ytecho, L.lg((0, "#2a1a10"), (1, "#4a3020"))))
    for k in range(int(w / 160) + 1):
        L.add(_rect(k * 160 + 20, 0, 40, ytecho, "#1a1008", 0.6))
    L.add(_rect(0, ytecho - 16, w, 16, "#5a3a22"), _rect(0, ytecho, w, 8, "#000", 0.3))
    # ventanas (solo horizontal): arcos a los lados
    if not V:
        for (x0, x1) in ((60, 360), (1560, 1860)):
            y0, y1 = 140, 620
            d = f"M{x0} {y1} L{x0} {y0 + 150} A{(x1 - x0) / 2} {(x1 - x0) / 2} 0 0 1 {x1} {y0 + 150} L{x1} {y1} Z"
            L.add(f'<path d="{d}" fill="#000" opacity="0.2" transform="translate(10 12)"/>')
            if triste:
                L.add(f'<path d="{d}" fill="#0c1424"/>')
                c = L.clip(d)
                lam = "".join(_rect(x0, y0 + k * 16, x1 - x0, 12, "#3a4050") + _rect(x0, y0 + k * 16 + 12, x1 - x0, 4, "#9ab4d8", 0.35) for k in range(int((y1 - y0) / 16) + 1))
                L.add(f'<g clip-path="{c}">{lam}</g>')
            else:
                c = L.clip(d)
                L.add(f'<g clip-path="{c}">' + _vista_fuera(L, x0, y0, x1, y1, r, "dia") + _rect(x0, y0, x1 - x0, y1 - y0, "#fff4e0", 0.15) + "</g>")
            L.add(f'<path d="{d}" fill="none" stroke="#2a1a10" stroke-width="16"/>',
                  f'<path d="M{(x0 + x1) / 2} {y0} L{(x0 + x1) / 2} {y1} M{x0} {y0 + 320} L{x1} {y0 + 320}" stroke="#2a1a10" stroke-width="10"/>',
                  _rect(x0 - 24, y1, x1 - x0 + 48, 16, "#a87444"))
    # relojes (muchos) en la pared, sin pisar ventanas ni estantes
    ytop = yb - S(220, 150)
    zona = (30, ytecho + 40, w - 30, ytop - S(290, 200))
    hechos = []
    intentos = 0
    formas = ["redondo", "redondo", "cuadrado", "sol", "redondo", "pendulo"]
    marcos = [("#e0b860", "#7a5420"), ("#d8d8d8", "#6a6a6a"), ("#c06a3a", "#6a2a14"), ("#2a2a2a", "#0a0a0a"), ("#e8e0c8", "#a89a7a"), ("#b03a2a", "#5a1a10")]
    caras = ["#f6ecd4", "#fbf8ee", "#efe4c8", "#f4f0e4"]
    while len(hechos) < S(15, 24) and intentos < 4000:
        intentos += 1
        R = r.uniform(S(34, 26), S(70, 56))
        x, y = r.uniform(zona[0] + R, zona[2] - R), r.uniform(zona[1] + R * 1.4, zona[3] - R * 1.4)
        f = r.choice(formas)
        if f == "pendulo":
            y = min(y, zona[3] - R * 2.8)
        if any(math.hypot(x - a, y - b) < (R + c) * 1.5 + 8 for a, b, c in hechos):
            continue
        if not V and (x - R * 1.5 < 400 or x + R * 1.5 > 1520):
            continue
        hechos.append((x, y, R))
        L.add(_reloj(L, x, y, R, r, marco=r.choice(marcos), cara=r.choice(caras), forma=f, oscuro=0.45 if triste else 0))
    # barra al fondo con estantes
    bx0, bx1 = S(130, 520), S(950, 1400)
    ytop = yb - S(220, 150)
    sh_y = [ytop - S(260, 180), ytop - S(140, 96)]
    for k, y in enumerate(sh_y):
        L.add(_rect(bx0 + 20, y, bx1 - bx0 - 40, 12, "#a87444"), _rect(bx0 + 20, y + 12, bx1 - bx0 - 40, 6, "#000", 0.35))
        x = bx0 + 40
        while x < bx1 - 60:
            t = r.random()
            if t < 0.45:   # taza
                L.add(_rect(x, y - 24, 26, 24, "#f8f4ec", extra='rx="3"'), f'<path d="M{x + 26} {y - 18} q10 2 0 12" stroke="#f8f4ec" stroke-width="3" fill="none"/>',
                      _rect(x + 3, y - 22, 4, 18, "#ffffff", 0.6))
                x += 40
            elif t < 0.75:   # tarro
                hh = r.uniform(40, 60)
                cc = r.choice(["#6a3a1a", "#c8a060", "#3a2010", "#e8d8b0"])
                L.add(_rect(x, y - hh, 34, hh, "#d8e8ec", 0.5), _rect(x + 2, y - hh * 0.75, 30, hh * 0.75, cc, 0.9), _rect(x - 2, y - hh - 8, 38, 9, "#8a6a40"),
                      _rect(x + 4, y - hh + 4, 4, hh - 8, "#ffffff", 0.5))
                x += 50
            else:   # plantita
                L.add(f'<path d="M{x} {y - 26} L{x + 30} {y - 26} L{x + 26} {y} L{x + 4} {y} Z" fill="#d07a4a"/>')
                for j in range(6):
                    L.add(f'<ellipse cx="{x + 15 + r.uniform(-14, 14):.0f}" cy="{y - 30 - r.uniform(0, 22):.0f}" rx="9" ry="5" transform="rotate({r.uniform(-50, 50):.0f} {x + 15} {y - 34})" fill="{r.choice(["#3f7a34", "#5f9a48"])}"/>')
                x += 50
    # mostrador
    L.add(_rect(bx0 + 10, ytop + 10, bx1 - bx0, yb - ytop, "#000", 0.25))
    L.add(_rect(bx0, ytop, bx1 - bx0, yb - ytop, L.lg((0, "#8a5430"), (1, "#4a2a14"))))
    for k in range(int((bx1 - bx0) / 30)):
        L.add(_rect(bx0 + 6 + k * 30, ytop + 24, 3, yb - ytop - 30, "#2a160a", 0.5), _rect(bx0 + 10 + k * 30, ytop + 24, 2, yb - ytop - 30, "#c88a5a", 0.3))
    L.add(_rect(bx0 - 16, ytop - 12, bx1 - bx0 + 32, 22, L.lg((0, "#f4ece0"), (1, "#c8bca8"))), _rect(bx0 - 16, ytop + 10, bx1 - bx0 + 32, 6, "#000", 0.35))
    L.add(_rect(bx0, yb - S(46, 32), bx1 - bx0, 6, "#d8b060"))
    L.add(_cafetera(L, bx0 + S(50, 60), ytop - 12, S(170, 150), S(130, 110)))
    # campana de tartas
    kx = bx1 - S(130, 140)
    L.add(f'<ellipse cx="{kx}" cy="{ytop - 14}" rx="60" ry="8" fill="#e8e0d0"/><path d="M{kx - 40} {ytop - 16} L{kx + 40} {ytop - 16} L{kx + 40} {ytop - 46} L{kx - 40} {ytop - 46} Z" fill="#e0a070"/>'
          f'<path d="M{kx - 40} {ytop - 46} L{kx + 40} {ytop - 46}" stroke="#fff4e8" stroke-width="6"/>'
          f'<path d="M{kx - 52} {ytop - 14} C{kx - 54} {ytop - 90} {kx + 54} {ytop - 90} {kx + 52} {ytop - 14}" fill="#e8f4f8" opacity="0.25" stroke="#ffffff" stroke-width="2"/>'
          f'<path d="M{kx - 36} {ytop - 30} C{kx - 38} {ytop - 70} {kx - 10} {ytop - 76} {kx} {ytop - 76}" stroke="#ffffff" stroke-width="4" opacity="0.5" fill="none"/>')
    # plantas colgantes
    for x in S([80, 1000], [440, 1480]):
        L.add(_maceta_colgante(L, x, ytecho, ytecho + S(80, 50), S(1.1, 0.9), r))
    # suelo de madera
    suelo, P = _suelo(L, yb, yh, cx, "tarima", ["#9a6438", "#8a5630", "#a86e40", "#7a4a28"], ("#8a5630", "#3a2010"), sem + 2, a=S(70, 66))
    L.add(suelo)
    L.add(L.relieve(sem + 3, freq="0.004 0.05", escala=2, az=180, elev=60, op=0.3, oct=3, modo="soft-light", caja=(0, yb, w, h - yb)))
    # mesas y sillas a los lados
    mesas = [(S(110, 250), S(1400, 900), S(1.05, 0.85)), (S(975, 1680), S(1410, 900), S(1.05, 0.85))]
    if not V:
        mesas += [(560, 820, 0.62), (1360, 820, 0.62)]
    mesas.sort(key=lambda m: m[1])
    for (mx, my, ms) in mesas:
        if not triste:
            L.add(_silla(L, mx - 110 * ms, my - 26 * ms, ms * 0.95), _silla(L, mx + 110 * ms, my - 26 * ms, ms * 0.95))
        m, yt = _mesa(L, mx, my, ms)
        L.add(m)
        if triste:
            L.add(_silla(L, mx - 40 * ms, yt, ms * 0.9, invertida=True), _silla(L, mx + 44 * ms, yt + 2, ms * 0.9, invertida=True))
        else:
            L.add(f'<ellipse cx="{mx:.0f}" cy="{yt - 4 * ms:.0f}" rx="{14 * ms:.0f}" ry="{4 * ms:.0f}" fill="#f8f4ec"/>'
                  f'<rect x="{mx - 4 * ms:.0f}" y="{yt - 30 * ms:.0f}" width="{8 * ms:.0f}" height="{26 * ms:.0f}" fill="#d8e8f0" opacity="0.7"/>'
                  f'<circle cx="{mx:.0f}" cy="{yt - 34 * ms:.0f}" r="{7 * ms:.0f}" fill="#e84a5a"/>')
    # lámparas colgantes y su luz
    lamps = S([(250, 420), (540, 470), (830, 420)], [(700, 270), (960, 300), (1220, 270)])
    for i, (x, y) in enumerate(lamps):
        on = (not triste) or i == 2
        if triste and on:
            L.add(L.rect("#06091a", 0.55, extra='style="mix-blend-mode:multiply"'))
            L.add(L.luz(S(-100, 200), S(800, 380), w * 0.7, S(700, 450), "#4a6aa8", 0.22))
        if on:
            sp = S(1.1, 0.9)
            ycono = y + 64 * sp
            cono = [(x - 56 * sp, ycono), (x + 56 * sp, ycono), (x + S(300, 240), yb + S(200, 120)), (x - S(300, 240), yb + S(200, 120))]
            g = L.lg((0, "#ffe0a0", 0.35 if triste else 0.18), (1, "#ffe0a0", 0))
            L.add('<g filter="url(#blur20)">' + _poly(cono, f'fill="{g}"') + "</g>")
            L.add(L.luz(x, ytop - 10, S(320, 260), S(140, 100), "#ffc070", 0.5 if triste else 0.35))
            L.add(L.luz(x, yb + S(160, 100), S(380, 320), S(120, 80), "#ffc070", 0.4 if triste else 0.25))
            if triste:
                c = L.clip("M" + " L".join(f"{a:.0f} {b:.0f}" for a, b in cono) + " Z")
                L.add(f'<g clip-path="{c}">' + L.polvo(S(220, 180), x - 320, ycono, x + 320, yb + 200, "#fff0c8", 2.4, 0.8, sem=sem + 9) + "</g>")
                big = "".join(f'<circle cx="{r.uniform(x - 200, x + 200):.0f}" cy="{r.uniform(ycono + 60, yb):.0f}" r="{r.uniform(3, 7):.1f}" fill="#fff0c8" opacity="{r.uniform(0.2, 0.5):.2f}"/>' for _ in range(16))
                L.add(f'<g filter="url(#blur8)">{big}</g>')
        L.add(_lampara(L, x, y, S(1.1, 0.9), encendida=on))
    if triste:
        L.add(L.polvo(S(120, 160), 0, ytecho, w, h, "#c8d4f0", 1.6, 0.35, sem=sem + 11))
        L.add(L.oscuridad(lamps[2][0], S(900, 560), w * 0.8, h * 0.6, color="#03050c", op=0.85, medio=0.35))
    else:
        L.add(L.luz(cx, S(700, 380), w * 0.9, S(800, 500), "#ffb860", 0.25))
        L.add(L.oscuridad(cx, S(900, 520), w * 0.95, h * 0.75, color="#0e0806", op=0.55, medio=0.12))
    return {"suelo": S(1430, 880), "centro": (round(lamps[2][0]) if triste else round(cx), S(1000, 560)),
            "nota": f"barra x {bx0}–{bx1}, mostrador desde y={ytop}; mesas a los lados, centro del suelo despejado"}


def bg_cafe_dentro(L, sem=531):
    """Cafetería original y bonita, vacía: muchos relojes en la pared, plantas colgantes, lámparas cálidas, barra al fondo."""
    return _cafe(L, False, sem)


def bg_cafe_dentro_triste(L, sem=531):
    """La misma cafetería de noche, cerrada: una sola lámpara, sillas subidas a las mesas, polvo en el aire."""
    return _cafe(L, True, sem)


# ============================================================================ 6. cocina
def _olla(L, x, yb_, ww, hh, col=("#e8eaee", "#8a8e96"), tapa=True, mango=False):
    g = L.lg((0, col[1]), (0.25, col[0]), (0.5, mezcla(col[0], col[1], 0.4)), (1, col[1]), x2=1, y2=0)
    out = [_rect(x - ww / 2, yb_ - hh, ww, hh, g, extra=f'rx="{ww * 0.06:.0f}"'),
           f'<ellipse cx="{x:.0f}" cy="{yb_ - hh:.0f}" rx="{ww / 2:.0f}" ry="{ww * 0.1:.0f}" fill="{mezcla(col[1], "#000000", 0.3)}"/>']
    if tapa:
        _ap(out, f'<ellipse cx="{x:.0f}" cy="{yb_ - hh - 2:.0f}" rx="{ww / 2 + 3:.0f}" ry="{ww * 0.11:.0f}" fill="{g}"/>'
                   f'<path d="M{x - ww * 0.45:.0f} {yb_ - hh - 2:.0f} Q{x:.0f} {yb_ - hh - ww * 0.3:.0f} {x + ww * 0.45:.0f} {yb_ - hh - 2:.0f}" fill="{g}"/>'
                   f'<rect x="{x - 10:.0f}" y="{yb_ - hh - ww * 0.22 - 6:.0f}" width="20" height="9" rx="4" fill="#2a2a2e"/>')
    if mango:
        _ap(out, _rect(x + ww / 2, yb_ - hh * 0.8, ww * 0.9, 9, "#2a2a2e", extra='rx="4"'))
    else:
        for s in (-1, 1):
            _ap(out, _rect(x + s * ww / 2 - (12 if s > 0 else -2) + (0 if s > 0 else -10), yb_ - hh * 0.8, 12, 8, "#2a2a2e", extra='rx="3"'))
    _ap(out, _rect(x - ww * 0.32, yb_ - hh + 6, 6, hh - 12, "#ffffff", 0.55))
    return "".join(out)


def bg_cocina(L, sem=541):
    """Cocina de casa cálida: azulejos, encimera, fogones con ollas, especiero, utensilios colgados y ventana con luz."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    S = lambda a, b: a if V else b  # noqa: E731
    yb = S(1230, 760)
    yh = S(660, 420)
    yen = yb - S(330, 210)      # encimera
    yaz = S(430, 120)           # hasta donde llega el alicatado
    cx = w * 0.5
    L.add(L.rect(L.lg((0, "#f0dcb8"), (1, "#d8b88a"), x2=1, y2=0.2), h=yb + 2))
    L.add(L.relieve(sem + 1, freq="0.006 0.005", escala=2, az=225, elev=60, op=0.3, oct=3, modo="soft-light", caja=(0, 0, w, yaz)))
    # alicatado tipo metro
    pid = L.p + "azul"
    L.defs.append(f'<pattern id="{pid}" width="64" height="36" patternUnits="userSpaceOnUse">'
                  f'<rect width="64" height="36" fill="#f4f0e6"/><rect x="0" y="0" width="64" height="2" fill="#c8bca4"/><rect x="0" y="18" width="64" height="2" fill="#c8bca4"/>'
                  f'<rect x="0" y="2" width="2" height="16" fill="#c8bca4"/><rect x="32" y="20" width="2" height="16" fill="#c8bca4"/>'
                  f'<rect x="4" y="4" width="26" height="3" fill="#ffffff" opacity="0.8"/><rect x="36" y="22" width="26" height="3" fill="#ffffff" opacity="0.8"/></pattern>')
    L.add(_rect(0, yaz, w, yen - yaz, f"url(#{pid})"))
    L.add(_rect(0, yaz, w, yen - yaz, L.lg((0, "#f0d8a8", 0.1), (1, "#a88a5a", 0.3))))
    L.add(_rect(0, yaz - 8, w, 10, "#c8a878"))
    if V:   # balda alta con platos y cazos de cobre colgados
        ys_ = 230
        L.add(_rect(40, ys_, 480, 14, "#a87444"), _rect(40, ys_ + 14, 480, 6, "#000", 0.3))
        for k in range(5):
            px = 80 + k * 52
            L.add(f'<ellipse cx="{px + 3}" cy="{ys_ - 40}" rx="8" ry="42" fill="#000" opacity="0.15"/>'
                  f'<ellipse cx="{px}" cy="{ys_ - 44}" rx="9" ry="44" fill="{["#f4f0e6", "#3a7ab8", "#f4f0e6", "#e8b040", "#f4f0e6"][k]}"/>'
                  f'<ellipse cx="{px - 2}" cy="{ys_ - 50}" rx="3" ry="30" fill="#ffffff" opacity="0.5"/>')
        for k in range(3):
            jx = 380 + k * 46
            L.add(_rect(jx, ys_ - 56, 36, 56, "#d8eaf0", 0.5), _rect(jx + 2, ys_ - 44, 32, 44, ["#e8d8b0", "#8a5a2a", "#f4f0e6"][k]), _rect(jx - 1, ys_ - 64, 38, 10, "#a87444"))
        L.add(_rect(60, ys_ + 70, 440, 6, "#6a6e76"))
        for k in range(4):
            px = 110 + k * 110
            rr = 36 - k * 4
            L.add(f'<path d="M{px} {ys_ + 76} L{px} {ys_ + 96}" stroke="#4a4a50" stroke-width="3"/>',
                  _rect(px - 4, ys_ + 92, 8, 46, "#4a2a14"),
                  f'<circle cx="{px + 4}" cy="{ys_ + 140 + rr + 4}" r="{rr}" fill="#000" opacity="0.18"/>'
                  f'<circle cx="{px}" cy="{ys_ + 138 + rr}" r="{rr}" fill="{L.lg((0, "#f0a070"), (0.5, "#c0602a"), (1, "#6a2a10"), x2=1, y2=1)}"/>'
                  f'<circle cx="{px}" cy="{ys_ + 138 + rr}" r="{rr * 0.7:.0f}" fill="#8a3a18" opacity="0.5"/>'
                  f'<path d="M{px - rr * 0.6:.0f} {ys_ + 138 + rr * 0.6:.0f} A{rr} {rr} 0 0 1 {px:.0f} {ys_ + 138:.0f}" stroke="#ffd0a0" stroke-width="4" fill="none" opacity="0.7"/>')
    # ventana sobre el fregadero
    vx0, vy0, vx1, vy1 = (70, 460, 400, 790) if V else (120, 150, 520, 460)
    L.add(_rect(vx0 - 24, vy0 - 24, vx1 - vx0 + 48, vy1 - vy0 + 48, "#000", 0.1))
    L.add(_vista_fuera(L, vx0, vy0, vx1, vy1, r, "dia"))
    L.add(_marco_ventana(vx0, vy0, vx1, vy1, 2, 2, L.lg((0, "#ffffff"), (1, "#d8d4cc"), x2=1, y2=0), 14, "#e8e2d4"))
    L.add(L.brillo((vx0 + vx1) / 2, (vy0 + vy1) / 2, vx1 - vx0, vy1 - vy0, "#fff4d0", 0.3))
    # macetita y botella en el alféizar
    L.add(f'<path d="M{vx0 + 30} {vy1 + 8} L{vx0 + 70} {vy1 + 8} L{vx0 + 64} {vy1 - 26} L{vx0 + 36} {vy1 - 26} Z" fill="#c8703a" transform="translate(0 0)"/>')
    for j in range(8):
        L.add(f'<ellipse cx="{vx0 + 50 + r.uniform(-20, 20):.0f}" cy="{vy1 - 34 - r.uniform(0, 30):.0f}" rx="10" ry="6" transform="rotate({r.uniform(-60, 60):.0f} {vx0 + 50} {vy1 - 40})" fill="{r.choice(["#3f7a34", "#6aa848"])}"/>')
    # campana extractora sobre los fogones
    fx0, fx1 = (590, 870) if V else (880, 1180)
    hy0, hy1 = S(380, 110), S(640, 330)
    L.add(_rect((fx0 + fx1) / 2 - 50, 0, 100, hy0, L.lg((0, "#c8ccd2"), (0.5, "#f0f2f4"), (1, "#9a9ea6"), x2=1, y2=0)))
    L.add(_poly([((fx0 + fx1) / 2 - 60, hy0), ((fx0 + fx1) / 2 + 60, hy0), (fx1 + 20, hy1), (fx0 - 20, hy1)], f'fill="{L.lg((0, "#d8dce2"), (0.5, "#f4f6f8"), (1, "#a0a4ac"), x2=1, y2=0)}"'))
    L.add(_rect(fx0 - 24, hy1, fx1 - fx0 + 48, 14, "#8a8e96"), _rect(fx0 - 24, hy1 + 14, fx1 - fx0 + 48, 6, "#000", 0.2))
    L.add(L.luz((fx0 + fx1) / 2, hy1 + 40, (fx1 - fx0) * 0.6, 60, "#ffe8b0", 0.4))
    # barra de utensilios entre ventana y campana
    ux0, ux1 = (vx1 + 40, fx0 - 40)
    uy = S(560, 220)
    L.add(_rect(ux0, uy, ux1 - ux0, 6, "#9a9ea6"), f'<circle cx="{ux0}" cy="{uy + 3}" r="6" fill="#6a6e76"/><circle cx="{ux1}" cy="{uy + 3}" r="6" fill="#6a6e76"/>')
    n_ut = max(3, int((ux1 - ux0) / 42))
    for k in range(n_ut):
        x = ux0 + (ux1 - ux0) * (k + 0.5) / n_ut
        tipo = k % 4
        L.add(f'<path d="M{x:.0f} {uy + 6} L{x:.0f} {uy + 18}" stroke="#6a6e76" stroke-width="2"/>')
        if tipo == 0:     # cucharón
            L.add(_rect(x - 3, uy + 18, 6, S(110, 80), "#8a5a34"), f'<ellipse cx="{x:.0f}" cy="{uy + 18 + S(122, 92):.0f}" rx="18" ry="14" fill="#c8ccd2"/>')
        elif tipo == 1:   # espátula
            L.add(_rect(x - 3, uy + 18, 6, S(90, 66), "#2a2a2e"), _rect(x - 16, uy + 18 + S(90, 66), 32, 40, "#4a4a50", extra='rx="4"'))
        elif tipo == 2:   # varillas
            for dx in (-10, -4, 4, 10):
                L.add(f'<path d="M{x:.0f} {uy + 18 + S(50, 36)} Q{x + dx * 2:.0f} {uy + 18 + S(110, 86)} {x:.0f} {uy + 18 + S(140, 106)}" stroke="#c8ccd2" stroke-width="2" fill="none"/>')
            L.add(_rect(x - 4, uy + 18, 8, S(50, 36), "#c8ccd2"))
        else:             # cuchara de madera
            L.add(_rect(x - 3, uy + 18, 6, S(110, 80), "#c8925a"), f'<ellipse cx="{x:.0f}" cy="{uy + 18 + S(122, 92):.0f}" rx="13" ry="18" fill="#c8925a"/>')
    # especiero a la derecha de la campana (y armario alto)
    ex0, ex1 = (fx1 + 40, w - 20) if V else (1230, 1640)
    for k, y in enumerate(S([560, 690], [250, 350])):
        L.add(_rect(ex0, y, ex1 - ex0, 12, "#a87444"), _rect(ex0, y + 12, ex1 - ex0, 5, "#000", 0.3))
        x = ex0 + 10
        while x < ex1 - 36:
            hh = r.uniform(44, 64)
            cc = r.choice(["#c0392b", "#e0a92e", "#6a8a3a", "#8a4a2a", "#e8d8b0", "#d0602a", "#3a2a1a"])
            L.add(_rect(x, y - hh, 30, hh, "#d8eaf0", 0.45), _rect(x + 2, y - hh * 0.8, 26, hh * 0.8, cc), _rect(x - 1, y - hh - 10, 32, 11, "#2a2a2e"),
                  _rect(x + 4, y - hh + 2, 4, hh - 6, "#ffffff", 0.5))
            x += 38
    ac0 = S(220, 40)
    L.add(_rect(ex0 - 6, ac0, ex1 - ex0 + 12, S(240, 160), L.lg((0, "#e8d4b0"), (1, "#b89a6a"))), _rect(ex0 - 6, ac0 + S(240, 160), ex1 - ex0 + 12, 8, "#000", 0.25))
    for k in range(2):
        xd = ex0 + (ex1 - ex0) * k / 2
        L.add(_rect(xd + 10, ac0 + 12, (ex1 - ex0) / 2 - 20, S(216, 136), "none", extra='stroke="#9a7a4a" stroke-width="3"'),
              _rect(xd + (ex1 - ex0) / 2 - 26 if k == 0 else xd + 18, ac0 + S(180, 110), 8, 30, "#5a4a3a", extra='rx="4"'))
    # nevera (solo horizontal)
    if not V:
        nx0, nx1 = 1690, 1900
        L.add(_rect(nx0 + 10, 100, nx1 - nx0, yb - 100, "#000", 0.2),
              _rect(nx0, 90, nx1 - nx0, yb - 90, L.lg((0, "#f4f6f8"), (0.6, "#dde2e6"), (1, "#a8aeb4"), x2=1, y2=0), extra='rx="10"'),
              _rect(nx0, 340, nx1 - nx0, 5, "#8a9096"), _rect(nx0 + 20, 220, 8, 90, "#9aa0a6", extra='rx="4"'), _rect(nx0 + 20, 380, 8, 140, "#9aa0a6", extra='rx="4"'))
        for k, c in enumerate(["#e84a5a", "#3a7ae8", "#f8c830"]):
            L.add(f'<circle cx="{nx0 + 90 + k * 36}" cy="{170 + k * 14}" r="10" fill="{c}"/>')
        L.add(_dibujo_nino(L, nx0 + 70, 200, 90, 110, "casa", r, -4))
    # muebles bajos y encimera
    mx1 = S(w, 1680)
    L.add(_rect(0, yen, mx1, yb - yen, L.lg((0, "#e8d0a4"), (1, "#b8946a"))))
    nm = int(mx1 / S(180, 200))
    for k in range(nm):
        xd = k * mx1 / nm
        L.add(_rect(xd + 8, yen + 30, mx1 / nm - 16, yb - yen - 70, "none", extra='stroke="#9a7a4a" stroke-width="3"'),
              _rect(xd + mx1 / nm / 2 - 20, yen + 46, 40, 7, "#5a4a3a", extra='rx="3"'))
    L.add(_rect(0, yb - 34, mx1, 34, "#3a2a1a"))
    # horno bajo los fogones
    L.add(_rect(fx0 - 10, yen + 26, fx1 - fx0 + 20, yb - yen - 64, L.lg((0, "#3a3a40"), (1, "#1a1a1e"))),
          _rect(fx0 + 20, yen + 80, fx1 - fx0 - 40, yb - yen - 150, "#0e0e12"), _rect(fx0 + 30, yen + 88, (fx1 - fx0) * 0.3, yb - yen - 166, "#ffffff", 0.08),
          _rect(fx0 + 10, yen + 50, fx1 - fx0 - 20, 10, "#c8ccd2", extra='rx="5"'))
    # encimera
    L.add(_poly([(0, yen - S(34, 24)), (mx1, yen - S(34, 24)), (mx1, yen), (0, yen)], f'fill="{L.lg((0, "#7a5a3e"), (1, "#a87a52"))}"'))
    L.add(_rect(0, yen, mx1, 16, L.lg((0, "#c8946a"), (1, "#6a4428"))), _rect(0, yen + 16, mx1, 6, "#000", 0.3))
    # fogones (vitro de gas) y ollas
    L.add(_poly([(fx0, yen - S(30, 22)), (fx1, yen - S(30, 22)), (fx1 + 6, yen - 2), (fx0 - 6, yen - 2)], 'fill="#1e1e22"'))
    for k, (fx, ff) in enumerate((((fx0 + fx1) / 2 - (fx1 - fx0) * 0.25, 0.3), ((fx0 + fx1) / 2 + (fx1 - fx0) * 0.25, 0.7))):
        L.add(f'<ellipse cx="{fx:.0f}" cy="{yen - S(16, 12):.0f}" rx="{(fx1 - fx0) * 0.16:.0f}" ry="{S(9, 6)}" fill="none" stroke="#5a5a60" stroke-width="3"/>')
    L.add(_olla(L, (fx0 + fx1) / 2 - (fx1 - fx0) * 0.24, yen - S(14, 10), S(130, 110), S(100, 80)))
    L.add(_olla(L, (fx0 + fx1) / 2 + (fx1 - fx0) * 0.2, yen - S(14, 10), S(90, 76), S(50, 40), col=("#e0703a", "#7a2a10"), tapa=False, mango=True))
    vap = "".join(f'<path d="M{(fx0 + fx1) / 2 - (fx1 - fx0) * 0.24 + r.uniform(-30, 30):.0f} {yen - S(150, 120):.0f} q{r.uniform(-30, 30):.0f} -{S(60, 40)} 0 -{S(120, 80)} t0 -{S(100, 70)}" stroke="#ffffff" stroke-width="{r.uniform(10, 18):.0f}" fill="none" opacity="0.18"/>' for _ in range(4))
    L.add(f'<g filter="url(#blur8)">{vap}</g>')
    # fregadero bajo la ventana
    sx0, sx1 = vx0 + 30, vx1 - 30
    L.add(_poly([(sx0, yen - S(30, 22)), (sx1, yen - S(30, 22)), (sx1 - 10, yen - 6), (sx0 + 10, yen - 6)], 'fill="#9aa0a8"'),
          _poly([(sx0 + 16, yen - S(26, 19)), (sx1 - 16, yen - S(26, 19)), (sx1 - 22, yen - 10), (sx0 + 22, yen - 10)], 'fill="#5a6068"'))
    gx = (sx0 + sx1) / 2
    L.add(f'<path d="M{gx - 6:.0f} {yen - S(30, 22):.0f} L{gx - 6:.0f} {yen - S(110, 80):.0f} Q{gx - 6:.0f} {yen - S(130, 96):.0f} {gx + 20:.0f} {yen - S(130, 96):.0f} L{gx + 40:.0f} {yen - S(126, 92):.0f} L{gx + 40:.0f} {yen - S(108, 78):.0f}" stroke="#c8ccd2" stroke-width="9" fill="none" stroke-linecap="round"/>'
          f'<path d="M{gx - 9:.0f} {yen - S(30, 22):.0f} L{gx - 9:.0f} {yen - S(110, 80):.0f}" stroke="#ffffff" stroke-width="2" opacity="0.7"/>')
    # tabla con tomates y frutero
    tx = (ux0 + ux1) / 2
    L.add(_poly([(tx - 80, yen - S(26, 20)), (tx + 80, yen - S(26, 20)), (tx + 86, yen - 6), (tx - 86, yen - 6)], 'fill="#d8a46a"'), _rect(tx - 86, yen - 6, 172, 6, "#8a5a30"))
    for k in range(3):
        L.add(f'<circle cx="{tx - 40 + k * 34:.0f}" cy="{yen - S(30, 24):.0f}" r="16" fill="#d8322a"/><circle cx="{tx - 45 + k * 34:.0f}" cy="{yen - S(35, 29):.0f}" r="5" fill="#ff9a8a" opacity="0.7"/>'
              f'<path d="M{tx - 46 + k * 34:.0f} {yen - S(46, 40):.0f} l6 4 l6 -4" stroke="#3a7a2a" stroke-width="3" fill="none"/>')
    fx_ = S(ex0 + 80, 1500)
    L.add(f'<path d="M{fx_ - 70} {yen - S(60, 50)} Q{fx_} {yen - S(4, 4)} {fx_ + 70} {yen - S(60, 50)} Z" fill="#2f6fb0"/>')
    for k in range(5):
        L.add(f'<circle cx="{fx_ - 44 + k * 22:.0f}" cy="{yen - S(66, 56) - (8 if k % 2 else 0):.0f}" r="{18 if k != 2 else 20}" fill="{["#f0a030", "#e84a3a", "#f8d030", "#7ab040", "#f0a030"][k]}"/>')
    # suelo de baldosa en damero
    suelo, P = _suelo(L, yb, yh, cx, "damero", ["#b8765a", "#e4d6bc"], ("#c8a07a", "#6a3e28"), sem + 2, a=S(110, 100), junta="#5a3a28", op_pieza=0.7)
    L.add(suelo)
    L.add(L.relieve(sem + 3, freq="0.03 0.03", escala=1.5, az=225, elev=60, op=0.25, oct=2, modo="soft-light", caja=(0, yb, w, h - yb)))
    L.add(_luz_ventana(L, (vx0, vy0, vx1, vy1), 2, 2, yb + S(30, 20), yb + S(420, 260), S(340, 360), cx, yh, yb, color="#ffe2a8", op=0.35, haz=0.18, polvo=S(40, 40), sem=sem + 5))
    L.add(L.luz(vx0 + 100, vy0 + 120, w * 0.8, S(800, 500), "#ffd090", 0.3))
    L.add(L.oscuridad(cx, S(950, 520), w * 0.95, h * 0.75, color="#2a1408", op=0.45, medio=0.1))
    return {"suelo": S(1440, 880), "centro": (round(cx), S(900, 480)), "nota": f"encimera y={yen}; fogones x {fx0}–{fx1}; suelo de damero despejado"}


# ============================================================================ 7. habitación
def _poster(L, x, y, ww, hh, tipo, r, rot=0):
    out = [f'<g transform="rotate({rot:.1f} {x + ww / 2:.0f} {y + hh / 2:.0f})">', _rect(x + 6, y + 8, ww, hh, "#000", 0.3)]
    c = L.clip(f"M{x} {y} L{x + ww} {y} L{x + ww} {y + hh} L{x} {y + hh} Z")
    if tipo == "montana":
        cont = [_rect(x, y, ww, hh, L.lg((0, "#2a2a5a"), (0.5, "#c8507a"), (1, "#f8b060"))),
                f'<circle cx="{x + ww * 0.62:.0f}" cy="{y + hh * 0.55:.0f}" r="{ww * 0.2:.0f}" fill="#ffe0a0"/>',
                _poly([(x, y + hh * 0.8), (x + ww * 0.35, y + hh * 0.4), (x + ww * 0.6, y + hh * 0.7), (x + ww * 0.8, y + hh * 0.5), (x + ww, y + hh * 0.75), (x + ww, y + hh), (x, y + hh)], 'fill="#1a1430"'),
                _poly([(x + ww * 0.35, y + hh * 0.4), (x + ww * 0.42, y + hh * 0.5), (x + ww * 0.3, y + hh * 0.48)], 'fill="#f0e0f0"')]
    elif tipo == "planeta":
        cont = [_rect(x, y, ww, hh, "#0e1230"), L.polvo(30, x, y, x + ww, y + hh, "#ffffff", 1.8, 0.9, sem=r.randint(0, 999)),
                f'<circle cx="{x + ww / 2:.0f}" cy="{y + hh * 0.5:.0f}" r="{ww * 0.28:.0f}" fill="{L.lg((0, "#f8c070"), (1, "#c0502a"), x2=1, y2=1)}"/>',
                f'<ellipse cx="{x + ww / 2:.0f}" cy="{y + hh * 0.5:.0f}" rx="{ww * 0.46:.0f}" ry="{ww * 0.1:.0f}" fill="none" stroke="#f8e8c0" stroke-width="{ww * 0.04:.1f}" transform="rotate(-18 {x + ww / 2:.0f} {y + hh * 0.5:.0f})"/>']
    elif tipo == "guitarra":
        gx, gy = x + ww / 2, y + hh * 0.62
        cont = [_rect(x, y, ww, hh, L.lg((0, "#f8d040"), (1, "#f08a30"))),
                f'<g transform="rotate(-25 {gx:.0f} {gy:.0f})"><ellipse cx="{gx:.0f}" cy="{gy:.0f}" rx="{ww * 0.24:.0f}" ry="{hh * 0.16:.0f}" fill="#1a1a1a"/>'
                f'<ellipse cx="{gx:.0f}" cy="{gy - hh * 0.16:.0f}" rx="{ww * 0.18:.0f}" ry="{hh * 0.12:.0f}" fill="#1a1a1a"/><circle cx="{gx:.0f}" cy="{gy - hh * 0.08:.0f}" r="{ww * 0.06:.0f}" fill="#f8d040"/>'
                f'<rect x="{gx - ww * 0.03:.0f}" y="{y + hh * 0.05:.0f}" width="{ww * 0.06:.0f}" height="{hh * 0.4:.0f}" fill="#1a1a1a"/></g>']
    else:   # geométrico
        cont = [_rect(x, y, ww, hh, "#f4ece0")]
        for k in range(6):
            cc = r.choice(["#e84a3a", "#2f6fb0", "#f8c830", "#2a2a2a", "#3aa07a"])
            if k % 2:
                cont.append(f'<circle cx="{x + r.uniform(0.2, 0.8) * ww:.0f}" cy="{y + r.uniform(0.2, 0.8) * hh:.0f}" r="{r.uniform(0.1, 0.22) * ww:.0f}" fill="{cc}" opacity="0.9"/>')
            else:
                cont.append(_rect(x + r.uniform(0, 0.6) * ww, y + r.uniform(0, 0.7) * hh, r.uniform(0.2, 0.4) * ww, r.uniform(0.1, 0.3) * hh, cc, 0.9))
    _ap(out, f'<g clip-path="{c}">' + "".join(cont) + "</g>")
    _ap(out, _rect(x, y, ww, hh, "none", extra='stroke="#ffffff" stroke-width="4" opacity="0.6"'))
    for (a, b) in ((x, y), (x + ww, y), (x, y + hh), (x + ww, y + hh)):
        _ap(out, f'<rect x="{a - 12:.0f}" y="{b - 6:.0f}" width="24" height="12" fill="#f4f0d8" opacity="0.75" transform="rotate({r.uniform(-30, 30):.0f} {a:.0f} {b:.0f})"/>')
    _ap(out, "</g>")
    return "".join(out)


def bg_habitacion(L, sem=551):
    """Habitación de adolescente al atardecer: cama, pósters, luces de guirnalda, estantería, ventana naranja y alfombra."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    S = lambda a, b: a if V else b  # noqa: E731
    yb = S(1240, 760)
    yh = S(680, 430)
    cx = w * 0.5
    L.add(L.rect(L.lg((0, "#4a6a8c"), (0.6, "#3e5a7a"), (1, "#2a3e58"), x2=1, y2=0.2), h=yb + 2))
    if V:   # techo y lámpara de papel
        L.add(_rect(0, 0, w, 130, L.lg((0, "#5a6a80"), (1, "#7a8aa0"))), _rect(0, 124, w, 12, "#e8e0d4"), _rect(0, 136, w, 6, "#000", 0.2))
        L.add(f'<path d="M420 0 L420 270" stroke="#e8e0d4" stroke-width="2"/>',
              f'<circle cx="420" cy="340" r="78" fill="{L.lg((0, "#fff4e0"), (1, "#d8c8b0"), x2=1, y2=1)}"/>')
        for k in range(1, 6):
            L.add(f'<ellipse cx="420" cy="{262 + k * 26}" rx="{(78 ** 2 - (78 - k * 26) ** 2) ** 0.5:.0f}" ry="6" fill="none" stroke="#c8b8a0" stroke-width="2" opacity="0.6"/>')
    L.add(L.relieve(sem + 1, freq="0.006 0.005", escala=2, az=225, elev=60, op=0.3, oct=3, modo="soft-light", caja=(0, 0, w, yb)))
    # ventana a la derecha con atardecer
    vx0, vy0, vx1, vy1 = (650, 470, 1010, 900) if V else (1240, 120, 1600, 520)
    L.add(_vista_fuera(L, vx0, vy0, vx1, vy1, r, "tarde"))
    L.add(L.brillo((vx0 + vx1) / 2, vy0 + (vy1 - vy0) * 0.7, (vx1 - vx0) * 0.5, 100, "#ffd890", 0.7))
    L.add(_marco_ventana(vx0, vy0, vx1, vy1, 2, 2, L.lg((0, "#f4ece0"), (1, "#b8a890"), x2=1, y2=0), 14, "#d8ccb4"))
    # luz naranja proyectada en la pared (hacia la izquierda, cayendo)
    dxp = S(-560, -620)
    proy = [(vx0 + dxp, vy0 + S(120, 80)), (vx1 + dxp * 0.95, vy0 + S(160, 100)), (vx1 + dxp * 0.95, vy1 + S(200, 120)), (vx0 + dxp, vy1 + S(160, 100))]
    pr = []
    for i in range(2):
        for j in range(2):
            def pt(u, v):
                a = (proy[0][0] + (proy[1][0] - proy[0][0]) * u, proy[0][1] + (proy[1][1] - proy[0][1]) * u)
                b = (proy[3][0] + (proy[2][0] - proy[3][0]) * u, proy[3][1] + (proy[2][1] - proy[3][1]) * u)
                return (a[0] + (b[0] - a[0]) * v, a[1] + (b[1] - a[1]) * v)
            m = 0.05
            pr.append(_poly([pt(i / 2 + m, j / 2 + m), pt((i + 1) / 2 - m, j / 2 + m), pt((i + 1) / 2 - m, (j + 1) / 2 - m), pt(i / 2 + m, (j + 1) / 2 - m)], 'fill="#ffa860" opacity="0.5"'))
    L.add('<g filter="url(#blur8)" style="mix-blend-mode:screen">' + "".join(pr) + "</g>")
    # cortinas
    for xin, lado in ((vx0 - 20, -1), (vx1 + 20, 1)):
        xo = xin + lado * S(70, 90)
        d = f"M{xin} {vy0 - 50} C{xin + lado * 10} {vy0 + 200} {xin - lado * 20} {vy1} {xin + lado * 10} {vy1 + 120} L{xo} {vy1 + 130} L{xo} {vy0 - 50} Z"
        L.add(f'<path d="{d}" fill="{L.lg((0, "#e8c860"), (1, "#a08030"), x2=1, y2=0)}"/>')
        for k in range(1, 4):
            L.add(f'<path d="M{xin + lado * k * 18} {vy0 - 50} L{xin + lado * k * 18} {vy1 + 125}" stroke="#7a5a20" stroke-width="4" opacity="0.35"/>')
    L.add(_rect(vx0 - 120, vy0 - 64, vx1 - vx0 + 240, 10, "#2a2a2e", extra='rx="5"'))
    # pósters y guirnalda de luces
    if V:
        pos = [(60, 520, 220, 300, "montana", -2), (320, 560, 200, 250, "planeta", 3), (120, 870, 150, 190, "geometrico", 4)]
        gx0, gx1, gy = 30, 620, 470
    else:
        pos = [(110, 140, 220, 300, "montana", -2), (380, 170, 190, 240, "planeta", 3), (640, 130, 200, 280, "guitarra", -1), (900, 190, 170, 210, "geometrico", 2)]
        gx0, gx1, gy = 60, 1160, 90
    for p in pos:
        L.add(_poster(L, *p[:4], p[4], r, p[5]))
    pts = [(gx0 + (gx1 - gx0) * k / 12, gy + 30 * math.sin(k * math.pi / 3) ** 2) for k in range(13)]
    L.add(f'<path d="{suave(pts, cerrado=False)}" stroke="#1a1a1e" stroke-width="2" fill="none"/>')
    for k in range(25):
        t = k / 24
        x = gx0 + (gx1 - gx0) * t
        y = gy + 30 * math.sin(t * 12 * math.pi / 3) ** 2 + 6
        L.add(L.brillo(x, y + 6, 26, 26, "#ffd890", 0.7), f'<ellipse cx="{x:.0f}" cy="{y + 6:.0f}" rx="4" ry="6" fill="#fff4c0"/>')
    # estantería pequeña con libros
    if V:
        L.add(_estanteria(L, 400, 860, 600, 1010, r, baldas=1, madera=("#e8e0d4", "#b8aea0")))
    else:
        L.add(_estanteria(L, 940, 440, 1180, 560, r, baldas=1, madera=("#e8e0d4", "#b8aea0")))
    # suelo de tarima
    suelo, P = _suelo(L, yb, yh, cx, "tarima", ["#c8986a", "#b8885a", "#d4a676", "#a87a4e"], ("#b8885a", "#5a3a22"), sem + 2, a=S(76, 72))
    L.add(suelo)
    L.add(L.relieve(sem + 3, freq="0.004 0.05", escala=2, az=180, elev=60, op=0.3, oct=3, modo="soft-light", caja=(0, yb, w, h - yb)))
    L.add(_rect(0, yb - 26, w, 26, "#e8e0d4"), _rect(0, yb - 4, w, 6, "#000", 0.25))
    # alfombra (ovalada, con rayas)
    ry0 = S(1420, 870)
    arx, ary = S(380, 420), S(140, 90)
    L.add(f'<ellipse cx="{cx + 6:.0f}" cy="{ry0 + 8:.0f}" rx="{arx:.0f}" ry="{ary:.0f}" fill="#000" opacity="0.25"/>')
    for k, c in enumerate(["#d8604a", "#f0c878", "#3a7a8a", "#f4ecd8", "#d8604a"]):
        L.add(f'<ellipse cx="{cx:.0f}" cy="{ry0:.0f}" rx="{arx * (1 - k * 0.17):.0f}" ry="{ary * (1 - k * 0.17):.0f}" fill="{c}"/>')
    # cama a la izquierda (cabecero contra la pared, colcha que viene hacia nosotros)
    if V:
        hb0, hb1, hy0 = -20, 360, 1010
        fy = 1450
    else:
        hb0, hb1, hy0 = 40, 620, 560
        fy = 960
    L.add(_rect(hb0, hy0, hb1 - hb0, yb - hy0 + 10, L.lg((0, "#8a5a3a"), (1, "#5a3a22"))))
    L.add(_rect(hb0 + 14, hy0 + 14, hb1 - hb0 - 28, yb - hy0 - 20, "none", extra='stroke="#3a2214" stroke-width="3" opacity="0.5"'))
    my0 = yb - S(110, 70)
    bed = [(hb0 + 10, my0), (hb1 - 10, my0), (hb1 + S(80, 90), fy - S(90, 60)), (hb0 - S(120, 60), fy - S(90, 60))]
    L.add(_poly([(hb0 - S(120, 60), fy - S(90, 60)), (hb1 + S(80, 90), fy - S(90, 60)), (hb1 + S(80, 90), fy), (hb0 - S(120, 60), fy)], 'fill="#5a3a22"'))
    L.add(_poly(bed, f'fill="{L.lg((0, "#3a6aa0"), (1, "#2a4a78"))}"'))
    L.add(_poly([(bed[3][0], bed[3][1]), (bed[2][0], bed[2][1]), (bed[2][0], bed[2][1] + S(70, 46)), (bed[3][0], bed[3][1] + S(70, 46))], 'fill="#22406a"'))
    for k in range(6):   # pliegues de la colcha
        t = (k + 1) / 7
        xa = bed[0][0] + (bed[1][0] - bed[0][0]) * t
        xb = bed[3][0] + (bed[2][0] - bed[3][0]) * t
        L.add(f'<path d="M{xa:.0f} {my0 + 30:.0f} Q{(xa + xb) / 2 + r.uniform(-20, 20):.0f} {(my0 + bed[2][1]) / 2:.0f} {xb:.0f} {bed[2][1] + S(60, 40):.0f}" stroke="#1a3050" stroke-width="5" opacity="0.4" fill="none"/>'
              f'<path d="M{xa + 6:.0f} {my0 + 30:.0f} Q{(xa + xb) / 2 + 6:.0f} {(my0 + bed[2][1]) / 2:.0f} {xb + 6:.0f} {bed[2][1] + S(60, 40):.0f}" stroke="#7aa8d8" stroke-width="2" opacity="0.35" fill="none"/>')
    # almohada y cojín
    L.add(f'<path d="M{hb0 + 40} {my0 + 20} C{hb0 + 40} {my0 - 50} {hb1 - 40} {my0 - 50} {hb1 - 40} {my0 + 20} C{hb1 - 60} {my0 + 50} {hb0 + 60} {my0 + 50} {hb0 + 40} {my0 + 20} Z" fill="{L.lg((0, "#ffffff"), (1, "#c8ccd8"))}"/>')
    L.add(f'<rect x="{hb1 - S(170, 220)}" y="{my0 - 24}" width="{S(100, 120)}" height="{S(80, 90)}" rx="18" fill="#f0a030" transform="rotate(-8 {hb1 - 120} {my0})"/>')
    # luz de atardecer en el suelo y la cama
    L.add(_luz_ventana(L, (vx0, vy0, vx1, vy1), 2, 2, yb + S(40, 20), yb + S(380, 240), S(-420, -480), cx, yh, yb, color="#ffa860", op=0.35, haz=0.16, polvo=S(50, 50), sem=sem + 4))
    L.add(L.luz(vx0, vy1, w * 0.9, S(800, 560), "#ff9a50", 0.5))
    L.add(L.rect("#ff8a40", 0.07))
    L.add(L.oscuridad(w * 0.6, S(900, 500), w * 0.95, h * 0.75, color="#120a1a", op=0.55, medio=0.15))
    return {"suelo": S(1440, 880), "centro": (round(cx + S(60, 80)), S(1250, 760)), "nota": f"alfombra centrada en y={ry0}; cama a la izquierda; ventana x {vx0}–{vx1}"}


# ============================================================================ 8. campo de fútbol de barrio
def bg_campo_barrio(L, sem=561):
    """Campo de fútbol de barrio al atardecer: portería, valla metálica, bloques de pisos y cielo naranja."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    S = lambda a, b: a if V else b  # noqa: E731
    yfb = S(1000, 590)      # base de la valla del fondo
    yh = yfb - S(260, 160)
    gyb = yfb + S(80, 60)
    cx = w * 0.5
    L.add(L.rect(L.lg((0, "#2a2a5e"), (0.3, "#6a3a7a"), (0.6, "#e0604a"), (0.82, "#f8a050"), (1, "#ffd890")), h=yfb + 10))
    sx, sy = w * S(0.68, 0.7), yfb - S(260, 170)
    L.add(L.luz(sx, sy, w * 0.9, S(700, 450), "#ffd890", 0.6), L.brillo(sx, sy, 140, 140, "#fff4c0", 0.95), f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{S(56, 44)}" fill="#fff8e0"/>')
    for k in range(S(4, 6)):
        L.add(_nube(L, r.uniform(0, w), r.uniform(S(160, 70), S(520, 260)), r.uniform(0.5, 0.9), r, c_luz="#ffc8a0", c_sombra="#9a5a8a", op=0.85))
    # bloques de pisos a contraluz con ventanas encendidas
    L.add(IE._edificios(L, r, yfb - S(80, 50), 120, 220, 200, S(380, 240), "#5a3a5a", ["#ffd890", "#ffc070"], "#4a2a4a", 0.06, 1.2, top_luz="#ffb070"))
    L.add(L.bruma(yfb - S(80, 50), 120, "#f09060", 0.4))
    L.add(IE._edificios(L, r, yfb, 160, 280, 160, S(290, 190), "#2e1e34", ["#ffd38a", "#ffb060", "#fff0c0"], "#22162a", 0.12, 1.6, top_luz="#ff9a60"))
    # árboles oscuros tras la valla
    for k in range(S(4, 7)):
        x = r.uniform(0, w)
        L.add(_arbol(L, x, yfb + 5, S(0.7, 0.55), r, hojas=("#1e1a24", "#2a2230", "#4a2e38"), tronco=("#1a141e", "#2a2028"), luz=1, sombra=False))
    # suelo del campo (césped artificial con franjas)
    L.add(_rect(-10, yfb, w + 20, h - yfb + 10, L.lg((0, "#5a8a3a"), (1, "#2e5a24"))))
    Dw = h * 0.9

    def P(X, Z):
        return (cx + X * Dw / Z, yh + (gyb - yh) * Dw / Z)
    Zmin = (gyb - yh) * Dw / (h + 30 - yh)
    Z, k = Dw, 0
    while Z > Zmin:
        Z2 = max(Zmin * 0.95, Z - 140)
        q = [P(-4000, Z), P(4000, Z), P(4000, Z2), P(-4000, Z2)]
        L.add(_poly(q, f'fill="{"#6a9a44" if k % 2 else "#4a7a32"}" opacity="0.6"'))
        Z, k = Z2, k + 1
    # líneas del campo: área grande y área pequeña, frente a la portería
    def linea(pts, wd=4):
        return f'<path d="M' + " L".join(f"{P(X, Z)[0]:.0f} {P(X, Z)[1]:.0f}" for X, Z in pts) + f'" stroke="#f4f4ec" stroke-width="{wd}" fill="none" opacity="0.8"/>'
    L.add(linea([(-4000, Dw), (4000, Dw)], 3))
    L.add(linea([(-760, Dw), (-760, Dw - 420), (760, Dw - 420), (760, Dw)], 4))
    L.add(linea([(-420, Dw), (-420, Dw - 160), (420, Dw - 160), (420, Dw)], 4))
    pm = P(0, Dw - 300)
    L.add(f'<ellipse cx="{pm[0]:.0f}" cy="{pm[1]:.0f}" rx="7" ry="4" fill="#f4f4ec"/>')
    # valla metálica de simple torsión del fondo
    vh = S(250, 170)
    pid = L.p + "malla"
    L.defs.append(f'<pattern id="{pid}" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M0 9 L9 0 L18 9 L9 18 Z" fill="none" stroke="#c8ccd4" stroke-width="1.2" opacity="0.55"/></pattern>')
    L.add(_rect(-10, yfb - vh, w + 20, vh, f"url(#{pid})"))
    for k in range(int(w / S(180, 200)) + 2):
        x = k * S(180, 200) - 10
        L.add(_rect(x - 4, yfb - vh - 10, 8, vh + 14, "#5a5e66"), _rect(x - 4, yfb - vh - 10, 3, vh + 14, "#e8b080", 0.6))
    L.add(_rect(-10, yfb - vh - 10, w + 20, 6, "#5a5e66"), _rect(-10, yfb - 6, w + 20, 6, "#3a3e46"))
    # focos del campo (apagados) a los lados
    for x in S([40, 1040], [80, 1840]):
        L.add(_rect(x - 7, yfb - S(560, 380), 14, S(560, 380) + 10, "#3a3a44"), _rect(x - 40, yfb - S(590, 405), 80, 34, "#2a2a32", extra='rx="4"'),
              _rect(x - 34, yfb - S(584, 399), 68, 10, "#d8d4c8", 0.6))
    # portería con red
    gw, gh = S(560, 560), S(190, 190)
    gx0, gx1 = cx - gw / 2, cx + gw / 2
    prof = S(80, 80)
    red = L.p + "red"
    L.defs.append(f'<pattern id="{red}" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M0 0 L12 0 M0 0 L0 12" stroke="#ffffff" stroke-width="1.5" opacity="0.75"/></pattern>')
    L.add(f'<ellipse cx="{cx - 60:.0f}" cy="{gyb + 6:.0f}" rx="{gw * 0.6:.0f}" ry="14" fill="#1a2a10" opacity="0.35"/>')
    back = [(gx0 + 20, gyb - prof * 0.6), (gx1 - 20, gyb - prof * 0.6), (gx1 - 30, gyb - gh + 10), (gx0 + 30, gyb - gh + 10)]
    L.add(_poly(back, f'fill="url(#{red})"'), _poly([(gx0, gyb - gh), (gx0 + 30, gyb - gh + 10), (gx0 + 20, gyb - prof * 0.6), (gx0, gyb)], f'fill="url(#{red})"'),
          _poly([(gx1, gyb - gh), (gx1 - 30, gyb - gh + 10), (gx1 - 20, gyb - prof * 0.6), (gx1, gyb)], f'fill="url(#{red})"'),
          _poly([(gx0, gyb - gh), (gx1, gyb - gh), (gx1 - 30, gyb - gh + 10), (gx0 + 30, gyb - gh + 10)], f'fill="url(#{red})"'))
    gp = L.lg((0, "#ffffff"), (0.6, "#e8e4dc"), (1, "#a8a49c"), x2=1, y2=0)
    L.add(_rect(gx0 - 6, gyb - gh - 6, 12, gh + 6, gp), _rect(gx1 - 6, gyb - gh - 6, 12, gh + 6, gp), _rect(gx0 - 6, gyb - gh - 6, gw + 12, 12, gp))
    L.add(_rect(gx1 - 2, gyb - gh - 6, 6, gh + 6, "#ffb070", 0.5), _rect(gx0 - 6, gyb - gh - 6, gw + 12, 3, "#ffd0a0", 0.7))
    # tierra gastada delante de la portería y suelo cercano
    L.add(f'<g filter="url(#blur20)"><ellipse cx="{cx:.0f}" cy="{gyb + 20:.0f}" rx="{gw * 0.4:.0f}" ry="{S(40, 30)}" fill="#a8845a" opacity="0.5"/>'
          f'<ellipse cx="{cx:.0f}" cy="{h - S(300, 150):.0f}" rx="{w * 0.3:.0f}" ry="{S(120, 60)}" fill="#a8845a" opacity="0.3"/></g>')
    L.add(L.relieve(sem + 3, freq="0.12 0.3", escala=1.5, az=225, elev=55, op=0.2, oct=2, modo="soft-light", caja=(0, yfb, w, h - yfb)))
    # luz rasante de atardecer y sombras largas de la valla
    L.add(L.luz(sx, yfb + S(100, 60), w * 1.1, S(300, 180), "#ffa860", 0.35))
    L.add(L.polvo(S(60, 70), 0, yfb - 300, w, h, "#ffe0b0", 2, 0.5, sem=sem + 5))
    L.add(L.oscuridad(sx, yfb, w * 1.1, h * 0.8, color="#140a1a", op=0.5, medio=0.12))
    return {"suelo": S(1440, 880), "centro": (round(cx), gyb - gh // 2), "nota": f"portería x {gx0:.0f}–{gx1:.0f}, base y={gyb}; césped despejado delante"}


# ============================================================================ 9. estudio oscuro
def bg_estudio_oscuro(L, sem=571):
    """Escenario neutro muy oscuro: pared con textura, suelo apenas marcado, bruma y un charco de luz suave."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    S = lambda a, b: a if V else b  # noqa: E731
    yb = S(1300, 760)
    cx = w * 0.5
    L.add(L.rect(L.lg((0, "#0c0d12"), (0.75, "#161820"), (1, "#1a1c26")), h=yb + 2))
    L.add(L.textura([f"M0 0 L{w} 0 L{w} {yb} L0 {yb} Z"], sem, oscuro="#000000", claro="#3a3e50", freq=0.004, fuerza=0.6, oct=4))
    # paneles verticales muy sutiles (fondo de escenario)
    for k in range(int(w / S(180, 200)) + 1):
        x = k * S(180, 200)
        L.add(_rect(x, 0, 2, yb, "#000000", 0.35), _rect(x + 2, 0, 1, yb, "#2a2e3c", 0.4))
    # suelo
    L.add(_rect(-10, yb, w + 20, h - yb + 10, L.lg((0, "#1a1c26"), (0.4, "#12141c"), (1, "#0a0b10"))))
    L.add(f'<path d="M0 {yb} L{w} {yb}" stroke="#3a3e52" stroke-width="2" opacity="0.6"/>')
    for k in range(-12, 13):
        L.add(f'<path d="M{cx + k * 90:.0f} {yb} L{cx + k * S(420, 340):.0f} {h}" stroke="#2a2e3e" stroke-width="1.2" opacity="0.25"/>')
    for k in range(6):
        y = yb + (h - yb) * ((k + 1) / 7) ** 1.6
        L.add(f'<path d="M0 {y:.0f} L{w} {y:.0f}" stroke="#2a2e3e" stroke-width="1" opacity="0.2"/>')
    L.add(L.relieve(sem + 2, freq="0.01 0.04", escala=1.5, az=270, elev=60, op=0.25, oct=3, modo="soft-light", caja=(0, yb, w, h - yb)))
    # luz cenital suave y su reflejo en el suelo
    L.add(L.luz(cx, yb - S(300, 200), w * 0.6, S(700, 450), "#4a5068", 0.28))
    L.add(L.luz(cx, yb + S(160, 100), w * 0.45, S(140, 80), "#5a6078", 0.35))
    L.add(L.bruma(yb - S(40, 30), S(220, 140), "#2a2e40", 0.55), L.bruma(yb - S(400, 260), S(300, 200), "#20232f", 0.35))
    bru = "".join(f'<ellipse cx="{r.uniform(0, w):.0f}" cy="{r.uniform(yb - S(600, 380), yb + 40):.0f}" rx="{r.uniform(160, 380):.0f}" ry="{r.uniform(30, 70):.0f}" fill="#3a3e54" opacity="{r.uniform(0.08, 0.18):.2f}"/>' for _ in range(S(10, 12)))
    L.add(f'<g filter="url(#blur40)">{bru}</g>')
    L.add(L.polvo(S(90, 110), 0, S(300, 100), w, yb + 100, "#8a90b0", 1.6, 0.35, sem=sem + 3))
    L.add(L.oscuridad(cx, yb - S(100, 80), w * 0.85, h * 0.7, color="#050608", op=0.85, medio=0.3))
    return {"suelo": S(1400, 860), "centro": (round(cx), S(1000, 560)), "nota": f"horizonte del suelo y={yb}; charco de luz en el centro"}


FONDOS = [bg_aula, bg_colegio_fuera, bg_calle_dia, bg_cafe_dentro, bg_cafe_dentro_triste, bg_cocina, bg_habitacion, bg_campo_barrio, bg_estudio_oscuro]


def generar(dirsvg, solo=None):
    os.makedirs(dirsvg, exist_ok=True)
    nombres = []
    for i, f in enumerate(FONDOS):
        nom = f.__name__
        if solo and nom not in solo:
            continue
        for w, h, suf in ((1080, 1920, ""), (1920, 1080, "_h")):
            L = IE.Lienzo(nom + suf, w, h, 5000 + i * 37)
            INFO[nom + suf] = f(L) or {}
            L.guardar(dirsvg, nom + suf)
            nombres.append(nom + suf)
    return nombres


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg", sys.argv[2:] or None))
    for k, v in INFO.items():
        print(k, v)
