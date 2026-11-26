"""Objetos y locales del vídeo «El que copiaba en el colegio» (estilo del vídeo largo de la cueva).

Fachadas (900×820, misma escala y estructura que `frame_prueba.hamburgueseria`), colegio, comida y negocio,
móvil y apps genéricas (sin logos reales), iconos con volumen, vida diaria y focos de escenario.
Todas: fondo transparente, lienzo ajustado, luz principal arriba a la izquierda + luz de borde, degradados,
grano (filtro de `Lz.guardar`) y sombra de contacto en las que se posan. Sin letras, números ni logos.
Uso: python3 ilus_cosas.py DIR_SVG  → escribe los SVG y devuelve la lista de nombres.
"""
import math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
LARGO = os.path.join(RAIZ, "lotes", "largo-cueva-500-dias", "generadores")
sys.path.insert(0, RAIZ)
sys.path.insert(0, LARGO)
from motor.biblioteca import ilus  # noqa: E402
import ilus_personajes as IP  # noqa: E402
import ilus_objetos_mundo as IO  # noqa: E402
from ilus_personajes import Lz, F, mix, sombra_suelo, PIEL4  # noqa: E402

NOMBRES = []
LUZ = dict(luz=(-0.6, -0.8), rim="#fff1d8")

# posición de la pieza `persiana` sobre el lienzo de `cafeteria_marta` (900×820)
PERSIANA_XY = (110, 332)
PERSIANA_WH = (680, 478)


def _pz(n, w, h, rim="#fff1d8", luz=(-0.6, -0.8)):
    return Lz(n, w, h, luz=luz, rim=rim)


def _fin(z, textura=True):
    z.guardar(textura)
    NOMBRES.append(z.n)
    return z.n


def _lin(z, p1, p2, *cols):
    """Degradado lineal con paradas repartidas (o tuplas (offset, color[, alfa]))."""
    if cols and isinstance(cols[0], tuple):
        return z.lin(p1, p2, list(cols))
    n = len(cols) - 1
    return z.lin(p1, p2, [(round(i / n, 3), c) for i, c in enumerate(cols)])


def _extru(z, d, prof, col, dx=0.0, dy=1.0, pasos=10):
    """Extrusión barata: copias del contorno desplazadas hacia abajo-derecha (volumen de pieza)."""
    out = []
    for k in range(pasos, 0, -1):
        t = prof * k / pasos
        out.append(f'<path d="{d}" fill="{col}" transform="translate({F(dx * t)} {F(dy * t)})"/>')
    z("".join(out))


def _garabato(r, x0, x1, y, amp=3.0, paso=9.0):
    """Renglón garabateado (onda irregular, no son letras)."""
    pts = [f"M{F(x0)} {F(y)}"]
    x = x0
    while x < x1:
        x += paso
        pts.append(f"Q{F(x - paso / 2)} {F(y + r.uniform(-amp, amp) * 1.6)} {F(min(x, x1))} {F(y + r.uniform(-amp, amp) * 0.4)}")
    return "".join(pts)


# ============================================================================ FACHADAS
def _ladrillos(z, x0, y0, x1, y1, cols, seed, op=0.55):
    clip = z.clip(f"M{x0} {y0} L{x1} {y0} L{x1} {y1} L{x0} {y1} Z")
    r = random.Random(seed)
    b = [f'<g clip-path="{clip}">']
    for fila in range(int((y1 - y0) / 30) + 1):
        y = y0 + 4 + fila * 30
        off = 0 if fila % 2 else 30
        for c in range(int((x1 - x0) / 60) + 2):
            x = x0 - 30 + off + c * 60
            b.append(f'<rect x="{x}" y="{y}" width="56" height="26" rx="3" fill="{r.choice(cols)}" opacity="{op}"/>')
    b.append('</g>')
    z("".join(b))


def _burger_icono(z, tr=""):
    """La hamburguesa del cartel de `hamburgueseria` (coordenadas del cartel centrado en 450,130)."""
    z(f'<g transform="{tr}">',
      '<path d="M380 120 Q380 62 450 60 Q520 62 520 120 Z" fill="#e8a040"/>',
      '<path d="M392 108 Q400 74 440 68" stroke="#ffd890" stroke-width="7" fill="none" stroke-linecap="round"/>',
      '<path d="M372 124 Q390 112 410 126 Q430 112 450 126 Q470 112 490 126 Q510 112 528 124 L528 132 L372 132 Z" fill="#6ab04a"/>',
      '<rect x="374" y="132" width="152" height="20" rx="8" fill="#e0c020"/>',
      '<rect x="370" y="150" width="160" height="26" rx="12" fill="#6a3418"/>',
      '<path d="M380 178 L520 178 Q520 204 450 206 Q380 204 380 178 Z" fill="#d8903a"/>',
      *[f'<ellipse cx="{sx}" cy="{sy}" rx="5" ry="3" fill="#fff4d0"/>' for sx, sy in ((420, 84), (450, 76), (478, 86), (436, 98), (466, 98))],
      '</g>')


def _hamb(n, toldo=("#c8322a", "#f3e6cf", "#8a1e18", "#c8b89a"), muro=("#4a2e24", "#6a4232", "#3a241c"),
          ladr=("#7a4a36", "#6a3e2c", "#84523c", "#5e3628"), cocinero="normal", tenue=False, rayo=False):
    """Copia parametrizada de `frame_prueba.hamburgueseria` (mismo lienzo 900×820 y misma escala)."""
    w, h = 900, 820
    z = Lz(n, w, h, luz=(-0.5, -0.8), rim="#ffd9a0")
    k = 0.45 if tenue else 1.0
    gl = z.rad((450, 560), 520, [(0, "#ffcf8a", 0.45 * k * k), (0.6, "#ffb15e", 0.12 * k), (1, "#ffb15e", 0)])
    z(f'<ellipse cx="450" cy="600" rx="520" ry="300" fill="{gl}"/>')
    gm = z.lin((0, 0), (900, 0), [(0, muro[0]), (0.5, muro[1]), (1, muro[2])])
    z(f'<rect x="40" y="120" width="820" height="690" fill="{gm}"/>')
    _ladrillos(z, 40, 120, 860, 810, ladr, 7)
    if tenue:
        gi = z.lin((0, 330), (0, 760), [(0, "#c9a878"), (0.5, "#a8784a"), (1, "#6a4224")])
    else:
        gi = z.lin((0, 330), (0, 760), [(0, "#ffe2b0"), (0.5, "#ffc47a"), (1, "#e08a3a")])
    z(f'<rect x="110" y="330" width="420" height="430" rx="10" fill="{gi}"/>')
    z(f'<rect x="110" y="600" width="420" height="160" fill="{"#5a2a1a" if tenue else "#8a3a22"}"/>',
      f'<rect x="110" y="596" width="420" height="16" fill="{"#8a7258" if tenue else "#c8a07a"}"/>')
    for x in (200, 320, 440):
        z(f'<path d="M{x} 330 L{x} 380" stroke="#3a2a20" stroke-width="3"/>', f'<path d="M{x-26} 400 Q{x} 370 {x+26} 400 Z" fill="#2a1a14"/>',
          f'<ellipse cx="{x}" cy="404" rx="22" ry="8" fill="{"#d8c8a0" if tenue else "#fff4d0"}"/>')
        gb = z.rad((x, 430), 90, [(0, "#fff6d8", 0.7 * k * 0.6 if tenue else 0.7), (1, "#fff6d8", 0)])
        z(f'<circle cx="{x}" cy="440" r="90" fill="{gb}"/>')
    if cocinero == "normal":
        z('<circle cx="390" cy="505" r="30" fill="#5a2a18"/>', '<path d="M345 600 Q350 540 390 535 Q430 540 436 600 Z" fill="#f4efe6"/>',
          '<rect x="365" y="462" width="52" height="26" rx="10" fill="#ffffff"/>')
    elif cocinero == "lucas":   # Lucas de espaldas: pelo casi negro, polar azul y tirantes del delantal rojo
        z('<path d="M343 600 Q346 538 390 532 Q434 538 438 600 Z" fill="#2f6fb0"/>',
          '<path d="M352 600 Q356 548 390 542" stroke="#5f9fe0" stroke-width="5" fill="none" opacity="0.6"/>',
          '<path d="M372 538 L366 600 M408 538 L414 600" stroke="#c8322a" stroke-width="9"/>',
          '<path d="M358 574 L422 574" stroke="#c8322a" stroke-width="7"/>',
          '<rect x="380" y="520" width="20" height="16" fill="#e0b090"/>',
          '<circle cx="390" cy="502" r="29" fill="#1e1612"/>', '<path d="M368 492 Q384 474 406 484" stroke="#4a3a30" stroke-width="4" fill="none"/>',
          '<ellipse cx="361" cy="506" rx="5" ry="8" fill="#e8b898"/><ellipse cx="419" cy="506" rx="5" ry="8" fill="#e8b898"/>')
    if tenue:
        z('<rect x="110" y="330" width="420" height="430" rx="10" fill="#1a1a2a" opacity="0.18"/>')
    z(f'<path d="M140 340 L230 340 L150 750 L110 750 Z" fill="#ffffff" opacity="{0.07 if tenue else 0.12}"/>',
      '<path d="M260 340 L300 340 L220 750 L200 750 Z" fill="#ffffff" opacity="0.08"/>')
    z('<rect x="110" y="330" width="420" height="430" rx="10" fill="none" stroke="#1a1210" stroke-width="12"/>',
      '<path d="M320 330 L320 760" stroke="#1a1210" stroke-width="8"/>')
    gp = z.lin((0, 360), (0, 800), [(0, "#c8a070"), (1, "#8a5a30")] if tenue else [(0, "#ffd89a"), (1, "#f0a050")])
    z(f'<rect x="590" y="360" width="200" height="450" fill="{gp}"/>', '<path d="M590 360 L560 380 L560 800 L590 810 Z" fill="#2a1a14"/>',
      '<rect x="590" y="360" width="200" height="450" fill="none" stroke="#1a1210" stroke-width="12"/>')
    for i in range(10):
        x0 = 30 + i * 84
        col = toldo[0] if i % 2 == 0 else toldo[1]
        som = toldo[2] if i % 2 == 0 else toldo[3]
        z(f'<path d="M{x0} 250 L{x0+84} 250 L{x0+94} 315 L{x0+10} 315 Z" fill="{col}"/>',
          f'<path d="M{x0+10} 315 Q{x0+52} 345 {x0+94} 315 Z" fill="{col}"/>',
          f'<path d="M{x0+10} 315 L{x0+94} 315 L{x0+92} 322 L{x0+12} 322 Z" fill="{som}" opacity="0.6"/>')
    gt = z.lin((0, 250), (0, 322), [(0, "#ffffff", 0.18), (0.5, "#ffffff", 0), (1, "#000000", 0.15)])
    z(f'<path d="M30 250 L870 250 L874 322 L40 322 Z" fill="{gt}"/>')
    if tenue:
        z('<path d="M30 250 L870 250 L874 345 L40 345 Z" fill="#101020" opacity="0.15"/>')
    z('<rect x="22" y="236" width="856" height="18" rx="6" fill="#2a1a14"/>')
    gc = z.rad((450, 130), 120, [(0, "#3a2a20"), (1, "#1a1210")])
    z(f'<circle cx="450" cy="130" r="112" fill="{gc}"/>',
      f'<circle cx="450" cy="130" r="112" fill="none" stroke="{"#b89a5a" if tenue else "#ffcf6a"}" stroke-width="8"/>')
    gh = z.rad((450, 130), 170, [(0, "#ffd890", 0.18 if tenue else 0.55), (1, "#ffd890", 0)])
    z(f'<circle cx="450" cy="130" r="170" fill="{gh}"/>')
    if rayo:
        _burger_icono(z, "translate(428 130) scale(0.78) translate(-450 -130)")
        z('<path d="M520 58 L474 136 L506 136 L482 206 L548 112 L514 112 L536 58 Z" fill="#ffd23a" stroke="#c88a10" stroke-width="5" stroke-linejoin="round"/>',
          '<path d="M522 66 L486 128" stroke="#fff6c0" stroke-width="5" stroke-linecap="round"/>')
    else:
        _burger_icono(z)
    if tenue:
        z('<circle cx="450" cy="130" r="108" fill="#101020" opacity="0.25"/>')
    return _fin(z)


def hamburgueseria_lucas():
    return _hamb("hamburgueseria_lucas", toldo=("#2f8a4a", "#f4f1e6", "#1a5a2e", "#c8c4b4"),
                 muro=("#8a5a44", "#b07a5e", "#7a4c38"), ladr=("#c88a6a", "#b87a5c", "#d49a7a", "#a86e52"),
                 cocinero="lucas", rayo=True)


def hamburgueseria_vacia():
    return _hamb("hamburgueseria_vacia", cocinero=None, tenue=True)


def _persiana_dib(z, x, y, w, h, osc=0.0):
    """Persiana metálica de lamas con barra inferior y asa (en coordenadas x, y del lienzo)."""
    c = lambda col: mix(col, "#141b29", osc)  # noqa: E731
    g = _lin(z, (x, 0), (x + w, 0), c("#7c838a"), c("#b9bec3"), c("#a3a9ae"), c("#c9cdd1"), c("#6e757c"))
    z(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{g}"/>')
    paso = 22
    yy = y + 6
    b = []
    while yy < y + h - 30:
        b.append(f'<path d="M{x} {yy} L{x + w} {yy}" stroke="{c("#4a5056")}" stroke-width="3" opacity="0.8"/>'
                 f'<path d="M{x} {yy + 3} L{x + w} {yy + 3}" stroke="{c("#eef0f2")}" stroke-width="2" opacity="0.55"/>'
                 f'<path d="M{x} {yy + 12} L{x + w} {yy + 12}" stroke="{c("#5a6066")}" stroke-width="1" opacity="0.35"/>')
        yy += paso
    z("".join(b))
    # suciedad y manchas
    r = random.Random(31)
    for _ in range(14):
        xx = r.uniform(x + 10, x + w - 10)
        z(f'<path d="M{F(xx)} {F(r.uniform(y + 40, y + h * 0.6))} l{F(r.uniform(-3, 3))} {F(r.uniform(40, 120))}" '
          f'stroke="#3a3020" stroke-width="{F(r.uniform(6, 14))}" opacity="0.05" stroke-linecap="round"/>')
    gs = _lin(z, (0, y), (0, y + h), (0, "#000", 0.18), (0.25, "#000", 0), (0.8, "#000", 0), (1, "#000", 0.22))
    z(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{gs}"/>')
    # barra inferior y asa
    gb = _lin(z, (0, y + h - 30), (0, y + h), c("#d0d4d8"), c("#7a8086"), c("#4a5056"))
    z(f'<rect x="{x}" y="{y + h - 30}" width="{w}" height="30" fill="{gb}"/>',
      f'<path d="M{x} {y + h - 30} L{x + w} {y + h - 30}" stroke="{c("#f4f6f8")}" stroke-width="2"/>')
    cx = x + w / 2
    z(f'<path d="M{F(cx - 34)} {y + h - 26} L{F(cx - 34)} {y + h - 44} Q{F(cx - 34)} {y + h - 56} {F(cx - 22)} {y + h - 56} '
      f'L{F(cx + 22)} {y + h - 56} Q{F(cx + 34)} {y + h - 56} {F(cx + 34)} {y + h - 44} L{F(cx + 34)} {y + h - 26}" '
      f'stroke="{c("#3a3f44")}" stroke-width="9" fill="none" stroke-linecap="round"/>',
      f'<path d="M{F(cx - 30)} {y + h - 46} Q{F(cx - 30)} {y + h - 52} {F(cx - 20)} {y + h - 52} L{F(cx + 10)} {y + h - 52}" '
      f'stroke="#ffffff" stroke-width="2.5" fill="none" opacity="0.5"/>',
      f'<rect x="{F(x + 40)}" y="{y + h - 24}" width="26" height="16" rx="4" fill="{c("#3a3f44")}"/>',
      f'<circle cx="{F(x + 53)}" cy="{y + h - 16}" r="4" fill="{c("#9aa0a6")}"/>',
      f'<rect x="{F(x + w - 66)}" y="{y + h - 24}" width="26" height="16" rx="4" fill="{c("#3a3f44")}"/>',
      f'<circle cx="{F(x + w - 53)}" cy="{y + h - 16}" r="4" fill="{c("#9aa0a6")}"/>')
    z(f'<path d="M{x + 3} {y} L{x + 3} {y + h}" stroke="#ffffff" stroke-width="3" opacity="0.35"/>',
      f'<path d="M{x + w - 3} {y} L{x + w - 3} {y + h}" stroke="{z.rim}" stroke-width="4" opacity="0.4"/>')


def _planta(z, x, ybase, alto, seed, osc=0.0, maceta=True, ancho=1.0):
    """Maceta de barro con planta frondosa (hojas con luz y sombra)."""
    c = lambda col: mix(col, "#141b29", osc)  # noqa: E731
    r = random.Random(seed)
    hojas = []
    for _ in range(22):
        a = r.uniform(-75, 75)
        L = r.uniform(0.45, 1.0) * alto
        bx = x + r.uniform(-8, 8)
        by = ybase - 70
        tx = bx + math.sin(math.radians(a)) * L * 0.75 * ancho
        ty = by - math.cos(math.radians(a)) * L
        hojas.append((ty, bx, by, tx, ty, a))
    hojas.sort(key=lambda t: -t[0])
    for _, bx, by, tx, ty, a in hojas:
        mx, my = (bx + tx) / 2, (by + ty) / 2
        nx, ny = -(ty - by), (tx - bx)
        m = math.hypot(nx, ny) or 1
        nx, ny = nx / m * 22, ny / m * 22
        col = c(r.choice(["#3f7a3a", "#4f8a44", "#2f6a30", "#5a9a4a"]))
        z(f'<path d="M{F(bx)} {F(by)} Q{F(mx + nx)} {F(my + ny)} {F(tx)} {F(ty)} Q{F(mx - nx)} {F(my - ny)} {F(bx)} {F(by)} Z" fill="{col}"/>',
          f'<path d="M{F(bx)} {F(by)} Q{F(mx)} {F(my)} {F(tx)} {F(ty)}" stroke="{c("#a8d88a")}" stroke-width="2" opacity="0.5" fill="none"/>')
        if a < 0:
            z(f'<path d="M{F(bx)} {F(by)} Q{F(mx + nx * 0.6)} {F(my + ny * 0.6)} {F(tx)} {F(ty)}" stroke="{c("#c8f0a0")}" stroke-width="3" opacity="0.35" fill="none"/>')
    if maceta:
        g = _lin(z, (x - 34, 0), (x + 34, 0), c("#e09060"), c("#c06a3a"), c("#7a3a1a"))
        z(f'<path d="M{x - 36} {ybase - 74} L{x + 36} {ybase - 74} L{x + 28} {ybase} L{x - 28} {ybase} Z" fill="{g}"/>',
          f'<rect x="{x - 40}" y="{ybase - 80}" width="80" height="14" rx="4" fill="{c("#d0804e")}"/>',
          f'<path d="M{x - 38} {ybase - 79} L{x + 30} {ybase - 79}" stroke="{c("#ffc8a0")}" stroke-width="2" opacity="0.7"/>')


def _hiedra(z, x, y, largo, seed, osc=0.0, lado=1):
    c = lambda col: mix(col, "#141b29", osc)  # noqa: E731
    r = random.Random(seed)
    for t in range(3):
        x0 = x + t * 14 * lado
        pts = [(x0, y)]
        for k in range(1, 7):
            pts.append((x0 + r.uniform(-10, 10), y + largo * k / 6 * r.uniform(0.7, 1.0)))
        z(f'<path d="{IP.suave(pts, cerrado=False)}" stroke="{c("#2f5a2a")}" stroke-width="2.5" fill="none"/>')
        for (px, py) in pts[1:]:
            for s in (-1, 1):
                col = c(r.choice(["#4f8a44", "#3f7a3a", "#6aa858"]))
                z(f'<ellipse cx="{F(px + s * 8)}" cy="{F(py)}" rx="9" ry="6" fill="{col}" transform="rotate({s * 30} {F(px + s * 8)} {F(py)})"/>')


def _reloj_esfera(z, cx, cy, R, osc=0.0, marco="#6a4428"):
    """Esfera de reloj sin números (marcas), con marco de madera."""
    c = lambda col: mix(col, "#141b29", osc)  # noqa: E731
    gm = z.rad((cx - R * 0.4, cy - R * 0.4), R * 1.4, [(0, c(mix(marco, "#ffdcae", 0.4))), (0.6, c(marco)), (1, c(mix(marco, "#141b29", 0.5)))])
    ge = z.rad((cx - R * 0.3, cy - R * 0.3), R * 1.2, [(0, c("#fffaf0")), (0.7, c("#f4ead6")), (1, c("#d8c8a8"))])
    z(f'<circle cx="{F(cx + R * 0.06)}" cy="{F(cy + R * 0.08)}" r="{F(R)}" fill="#000" opacity="0.25"/>',
      f'<circle cx="{F(cx)}" cy="{F(cy)}" r="{F(R)}" fill="{gm}"/>', f'<circle cx="{F(cx)}" cy="{F(cy)}" r="{F(R * 0.84)}" fill="{ge}"/>')
    b = []
    for i in range(60):
        a = math.radians(i * 6)
        L = 0.14 if i % 5 == 0 else 0.05
        sw = R * (0.045 if i % 5 == 0 else 0.015)
        r1, r2 = R * 0.78, R * (0.78 - L)
        b.append(f'<path d="M{F(cx + math.sin(a) * r1)} {F(cy - math.cos(a) * r1)} L{F(cx + math.sin(a) * r2)} {F(cy - math.cos(a) * r2)}" '
                 f'stroke="{c("#2a2420")}" stroke-width="{F(sw)}" stroke-linecap="round"/>')
    z("".join(b))
    for ang, L, sw in ((305, 0.45, 0.07), (62, 0.66, 0.045)):
        a = math.radians(ang)
        z(f'<path d="M{F(cx - math.sin(a) * R * 0.1)} {F(cy + math.cos(a) * R * 0.1)} L{F(cx + math.sin(a) * R * L)} {F(cy - math.cos(a) * R * L)}" '
          f'stroke="{c("#1e1a18")}" stroke-width="{F(R * sw)}" stroke-linecap="round"/>')
    z(f'<path d="M{F(cx)} {F(cy + R * 0.12)} L{F(cx + R * 0.5)} {F(cy - R * 0.5)}" stroke="#c8322a" stroke-width="{F(R * 0.018)}"/>',
      f'<circle cx="{F(cx)}" cy="{F(cy)}" r="{F(R * 0.06)}" fill="{c("#b08a3a")}"/>',
      f'<path d="M{F(cx - R * 0.62)} {F(cy - R * 0.3)} A{F(R * 0.7)} {F(R * 0.7)} 0 0 1 {F(cx - R * 0.1)} {F(cy - R * 0.7)}" stroke="#ffffff" stroke-width="{F(R * 0.08)}" opacity="0.5" fill="none" stroke-linecap="round"/>',
      f'<path d="M{F(cx + R * 0.95)} {F(cy + R * 0.1)} A{F(R * 0.95)} {F(R * 0.95)} 0 0 1 {F(cx + R * 0.2)} {F(cy + R * 0.93)}" stroke="{z.rim}" stroke-width="{F(R * 0.05)}" opacity="0.45" fill="none"/>')


def _reloj_arena_mini(z, cx, cy, s, osc=0.0):
    c = lambda col: mix(col, "#141b29", osc)  # noqa: E731
    z(f'<g transform="translate({F(cx)} {F(cy)}) scale({s})">',
      f'<path d="M-40 -58 L40 -58 C40 -20 8 -6 6 0 C8 6 40 20 40 58 L-40 58 C-40 20 -8 6 -6 0 C-8 -6 -40 -20 -40 -58 Z" fill="{c("#dfeff6")}" opacity="0.35"/>',
      f'<path d="M-30 -40 L30 -40 C26 -18 8 -8 0 -2 C-8 -8 -26 -18 -30 -40 Z" fill="{c("#f2c46a")}"/>',
      f'<path d="M-30 56 Q0 28 30 56 Z" fill="{c("#f2c46a")}"/><path d="M0 0 L0 44" stroke="{c("#f2c46a")}" stroke-width="3"/>',
      f'<path d="M-40 -58 L40 -58 C40 -20 8 -6 6 0 C8 6 40 20 40 58 L-40 58 C-40 20 -8 6 -6 0 C-8 -6 -40 -20 -40 -58 Z" fill="none" stroke="{c("#fff8e8")}" stroke-width="4"/>',
      f'<rect x="-52" y="-72" width="104" height="16" rx="5" fill="{c("#b07a46")}"/><rect x="-52" y="56" width="104" height="16" rx="5" fill="{c("#b07a46")}"/>',
      f'<rect x="-50" y="-58" width="8" height="116" fill="{c("#8a5a32")}"/><rect x="42" y="-58" width="8" height="116" fill="{c("#8a5a32")}"/>',
      f'<path d="M-30 -50 C-28 -30 -16 -16 -8 -8" stroke="#ffffff" stroke-width="4" opacity="0.6" fill="none" stroke-linecap="round"/>',
      '</g>')


def _cafeteria_marta(n, cerrada=False):
    w, h = 900, 820
    z = Lz(n, w, h, luz=(-0.5, -0.8), rim="#ffd9a0" if not cerrada else "#9fb4d0")
    o = 0.32 if cerrada else 0.0
    c = lambda col: mix(col, "#141b29", o)  # noqa: E731
    if not cerrada:
        gl = z.rad((450, 560), 520, [(0, "#ffcf8a", 0.42), (0.6, "#ffb15e", 0.12), (1, "#ffb15e", 0)])
        z(f'<ellipse cx="450" cy="600" rx="520" ry="300" fill="{gl}"/>')
    # muro verde salvia con estuco
    gm = _lin(z, (40, 0), (860, 0), c("#5c7a66"), c("#7c9c86"), c("#6f8f7a"), c("#52705c"))
    z(f'<rect x="40" y="120" width="820" height="690" fill="{gm}"/>')
    r = random.Random(12)
    cl = z.clip("M40 120 L860 120 L860 810 L40 810 Z")
    b = [f'<g clip-path="{cl}">']
    for _ in range(40):
        b.append(f'<ellipse cx="{F(r.uniform(40, 860))}" cy="{F(r.uniform(130, 800))}" rx="{F(r.uniform(20, 70))}" ry="{F(r.uniform(8, 26))}" '
                 f'fill="{r.choice(["#ffffff", "#2a3a30"])}" opacity="{F(r.uniform(0.03, 0.07))}"/>')
    b.append('</g>')
    z("".join(b))
    # sombra de la cornisa y luz de borde
    z(f'<rect x="40" y="128" width="820" height="20" fill="#000" opacity="0.18"/>',
      f'<path d="M857 130 L857 810" stroke="{z.rim}" stroke-width="5" opacity="0.35"/>',
      f'<path d="M43 130 L43 810" stroke="#ffffff" stroke-width="3" opacity="0.2"/>')
    # cornisa de madera
    gw = _lin(z, (0, 104), (0, 132), c("#c89a68"), c("#8a5a32"), c("#4a2e16"))
    z(f'<rect x="26" y="104" width="848" height="28" rx="5" fill="{gw}"/>')
    # banda de madera (rótulo liso: el motor pone el nombre si hace falta)
    gf = _lin(z, (0, 250), (0, 310), c("#a87648"), c("#8a5a32"), c("#5a3a1e"))
    z(f'<rect x="60" y="250" width="780" height="58" rx="6" fill="{gf}"/>')
    r = random.Random(5)
    for k in range(9):
        y = 256 + k * 6 + r.uniform(-1, 1)
        z(f'<path d="M66 {F(y)} Q300 {F(y + r.uniform(-3, 3))} 520 {F(y)} T834 {F(y)}" stroke="{c("#5a3a1e")}" stroke-width="1.2" opacity="0.35" fill="none"/>')
    z(f'<path d="M62 252 L838 252" stroke="{c("#e8c090")}" stroke-width="3" opacity="0.7"/>',
      f'<rect x="80" y="262" width="740" height="34" rx="4" fill="none" stroke="{c("#4a2e16")}" stroke-width="2" opacity="0.5"/>')
    # lámparas de cuello de cisne sobre la banda
    for x in (180, 720):
        z(f'<path d="M{x} 248 L{x} 226 Q{x} 206 {x + 20} 206 L{x + 34} 206" stroke="{c("#2a2a26")}" stroke-width="6" fill="none"/>',
          f'<path d="M{x + 18} 200 L{x + 52} 200 L{x + 46} 216 L{x + 24} 216 Z" fill="{c("#2a2a26")}"/>')
        if not cerrada:
            gb = z.rad((x + 35, 230), 70, [(0, "#fff0c0", 0.7), (1, "#fff0c0", 0)])
            z(f'<path d="M{x + 24} 216 L{x + 46} 216 L{x + 90} 300 L{x - 20} 300 Z" fill="{gb}"/>',
              f'<ellipse cx="{x + 35}" cy="216" rx="11" ry="4" fill="#fff8e0"/>')
    # cajón de la persiana
    gk = _lin(z, (0, 312), (0, 334), c("#8a9096"), c("#5a6066"), c("#3a3f44"))
    z(f'<rect x="100" y="312" width="700" height="22" rx="3" fill="{gk}"/>',
      f'<path d="M100 313 L800 313" stroke="{c("#d0d4d8")}" stroke-width="2" opacity="0.7"/>')
    hx, hy, hw, hh = PERSIANA_XY + PERSIANA_WH
    if cerrada:
        _persiana_dib(z, hx, hy, hw, hh, osc=0.25)
        # papel pegado con cinta (sin letras: solo trazos y un dibujito de reloj de arena)
        z('<g transform="rotate(-4 520 520)">',
          '<rect x="452" y="452" width="150" height="196" fill="#000" opacity="0.25" transform="translate(6 8)"/>',
          f'<rect x="452" y="452" width="150" height="196" fill="{c("#fbf8f0")}"/>',
          f'<path d="M452 630 L602 630 L602 648 L470 648 Z" fill="{c("#e8e2d2")}"/>')
        rr = random.Random(8)
        for k, y in enumerate((540, 566, 592, 614)):
            z(f'<path d="{_garabato(rr, 474, 580 - (30 if k == 3 else 0), y, 2.0, 8)}" stroke="{c("#4a4a52")}" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.8"/>')
        _reloj_arena_mini(z, 527, 494, 0.36, osc=o)
        z(f'<rect x="500" y="440" width="54" height="20" fill="{c("#e8ddb0")}" opacity="0.85" transform="rotate(6 527 450)"/>',
          '</g>')
        # luz fría de la calle
        gn = z.rad((450, 300), 600, [(0, "#9fb4d0", 0.12), (1, "#9fb4d0", 0)])
        z(f'<rect x="40" y="120" width="820" height="690" fill="{gn}"/>')
    else:
        # marco de madera del hueco
        z(f'<rect x="{hx}" y="{hy}" width="{hw}" height="{hh}" fill="{c("#4a2e16")}"/>')
        # escaparate: interior cálido
        gi = _lin(z, (0, 342), (0, 700), "#ffe6b8", "#ffcf8a", "#e8a058")
        z(f'<rect x="124" y="344" width="392" height="350" fill="{gi}"/>')
        # pared del fondo con baldas y el gran reloj
        z('<rect x="124" y="344" width="392" height="60" fill="#e8b878" opacity="0.5"/>')
        gb = z.rad((320, 470), 220, [(0, "#fff6d8", 0.75), (1, "#fff6d8", 0)])
        z(f'<circle cx="320" cy="470" r="220" fill="{gb}"/>')
        _reloj_esfera(z, 320, 470, 98)
        for x in (180, 460):
            z(f'<path d="M{x} 344 L{x} 372" stroke="#3a2a20" stroke-width="3"/>', f'<path d="M{x - 22} 392 Q{x} 364 {x + 22} 392 Z" fill="#6f8f7a"/>',
              f'<ellipse cx="{x}" cy="394" rx="18" ry="6" fill="#fff4d0"/>')
        # mostrador con tazas y planta
        z('<rect x="124" y="610" width="392" height="84" fill="#7a4a2a"/>', '<rect x="124" y="604" width="392" height="12" fill="#d8b088"/>',
          '<path d="M124 640 L516 640" stroke="#5a3418" stroke-width="2" opacity="0.6"/>')
        for x in (170, 214, 400, 446):
            z(f'<path d="M{x - 15} 582 L{x + 15} 582 L{x + 12} 604 L{x - 12} 604 Z" fill="#fffaf0"/>',
              f'<path d="M{x + 14} 588 Q{x + 24} 590 {x + 13} 598" stroke="#fffaf0" stroke-width="3" fill="none"/>',
              f'<path d="M{x - 15} 582 L{x + 15} 582" stroke="#6f8f7a" stroke-width="3"/>')
        _tarta(z, 308, 590, 0.55, crema="#fff6e0", base="#c88a5a", fruta="#6f8f7a")
        # reflejos
        z('<path d="M150 344 L230 344 L150 694 L124 694 Z" fill="#ffffff" opacity="0.13"/>',
          '<path d="M262 344 L292 344 L212 694 L196 694 Z" fill="#ffffff" opacity="0.08"/>')
        # zócalo de madera bajo el escaparate
        gz = _lin(z, (0, 700), (0, 806), "#a87648", "#7a4a26", "#4a2e16")
        z(f'<rect x="120" y="700" width="400" height="106" fill="{gz}"/>',
          '<rect x="138" y="716" width="170" height="74" rx="3" fill="none" stroke="#4a2e16" stroke-width="4"/>',
          '<rect x="332" y="716" width="170" height="74" rx="3" fill="none" stroke="#4a2e16" stroke-width="4"/>',
          '<path d="M140 718 L306 718 M334 718 L500 718" stroke="#e8c090" stroke-width="2" opacity="0.6"/>',
          '<rect x="116" y="694" width="408" height="10" fill="#c89a68"/>')
        # columna y puerta de madera con cristal
        z('<rect x="520" y="338" width="40" height="472" fill="#6a4428"/>', '<path d="M523 340 L523 808" stroke="#c89a68" stroke-width="3" opacity="0.6"/>')
        gd = _lin(z, (566, 0), (786, 0), "#8a5a32", "#a87648", "#5a3a1e")
        z(f'<rect x="566" y="342" width="220" height="468" fill="{gd}"/>')
        gp = _lin(z, (0, 362), (0, 650), "#ffe6b8", "#ffc47a")
        z(f'<rect x="590" y="364" width="172" height="280" rx="4" fill="{gp}"/>',
          '<path d="M676 364 L676 400" stroke="#3a2a20" stroke-width="3"/><path d="M656 420 Q676 396 696 420 Z" fill="#6f8f7a"/>',
          '<ellipse cx="676" cy="422" rx="16" ry="5" fill="#fff4d0"/>',
          '<path d="M600 370 L650 370 L600 560 Z" fill="#ffffff" opacity="0.14"/>',
          '<rect x="590" y="364" width="172" height="280" rx="4" fill="none" stroke="#4a2e16" stroke-width="6"/>',
          '<rect x="592" y="672" width="168" height="114" rx="3" fill="none" stroke="#4a2e16" stroke-width="4"/>',
          '<path d="M594 674 L758 674" stroke="#e8c090" stroke-width="2" opacity="0.6"/>')
        gpo = _lin(z, (0, 560), (0, 600), "#fff0b0", "#c8962e", "#7a5410")
        z(f'<rect x="586" y="560" width="12" height="70" rx="6" fill="{gpo}"/>', '<circle cx="592" cy="594" r="9" fill="#d8a838"/>')
        z('<path d="M784 344 L784 808" stroke="#ffd9a0" stroke-width="3" opacity="0.5"/>')
    # cartel redondo con reloj de arena (madera y salvia)
    gc = z.rad((430, 110), 130, [(0, c("#8fb09a")), (0.7, c("#6f8f7a")), (1, c("#3f5a48"))])
    if not cerrada:
        gh = z.rad((450, 130), 170, [(0, "#ffe6b0", 0.45), (1, "#ffe6b0", 0)])
        z(f'<circle cx="450" cy="130" r="170" fill="{gh}"/>')
    z(f'<path d="M450 18 L450 2" stroke="{c("#3a2a20")}" stroke-width="0"/>',
      f'<circle cx="456" cy="138" r="112" fill="#000" opacity="0.22"/>',
      f'<circle cx="450" cy="130" r="112" fill="{c("#7a4a26")}"/>', f'<circle cx="450" cy="130" r="98" fill="{gc}"/>',
      f'<circle cx="450" cy="130" r="105" fill="none" stroke="{c("#c89a68")}" stroke-width="5"/>',
      f'<path d="M370 80 A96 96 0 0 1 470 34" stroke="#ffffff" stroke-width="8" opacity="0.3" fill="none" stroke-linecap="round"/>')
    _reloj_arena_mini(z, 450, 130, 1.05, osc=o)
    # plantas: macetas a los lados y hiedra colgando de la banda
    _planta(z, 72, 812, 230, 21, osc=o)
    _planta(z, 828, 812, 230, 22, osc=o)
    _hiedra(z, 64, 300, 140, 4, osc=o, lado=1)
    _hiedra(z, 836, 300, 140, 6, osc=o, lado=-1)
    return _fin(z)


def cafeteria_marta():
    return _cafeteria_marta("cafeteria_marta")


def cafeteria_marta_cerrada():
    return _cafeteria_marta("cafeteria_marta_cerrada", cerrada=True)


def persiana():
    w, h = PERSIANA_WH
    z = Lz("persiana", w, h, luz=(-0.5, -0.8), rim="#ffd9a0")
    _persiana_dib(z, 0, 0, w, h)
    return _fin(z)


def _tarta(z, x, y, s, crema="#fff4f0", base="#e8a0a8", fruta="#c8283a"):
    z(f'<g transform="translate({x} {y}) scale({s})">',
      '<path d="M-44 0 L44 0 L36 8 L-36 8 Z" fill="#f4f4f4"/><rect x="-4" y="8" width="8" height="24" fill="#e8e8e8"/>',
      '<ellipse cx="0" cy="34" rx="22" ry="5" fill="#e8e8e8"/>',
      f'<path d="M-38 0 L-38 -40 Q0 -50 38 -40 L38 0 Z" fill="{base}"/>',
      f'<path d="M-38 -22 Q0 -30 38 -22 L38 -16 Q0 -24 -38 -16 Z" fill="{crema}"/>',
      f'<path d="M-40 -40 Q0 -54 40 -40 Q30 -30 20 -38 Q10 -28 0 -38 Q-10 -28 -20 -38 Q-30 -30 -40 -40 Z" fill="{crema}"/>',
      *[f'<circle cx="{px}" cy="-48" r="5" fill="{fruta}"/><circle cx="{px - 1.5}" cy="-49.5" r="1.5" fill="#fff" opacity="0.7"/>' for px in (-20, 0, 20)],
      '<path d="M-34 -36 L-34 -4" stroke="#ffffff" stroke-width="4" opacity="0.35"/>',
      '</g>')


def cafeteria_nueva():
    """La cafetería final de Marta: normal y acogedora, toldo granate, con flores y una pizarra con un corazón de latte art."""
    w, h = 900, 820
    z = Lz("cafeteria_nueva", w, h, luz=(-0.5, -0.8), rim="#ffd9a0")
    gl = z.rad((450, 560), 520, [(0, "#ffcf8a", 0.45), (0.6, "#ffb15e", 0.12), (1, "#ffb15e", 0)])
    z(f'<ellipse cx="450" cy="600" rx="520" ry="300" fill="{gl}"/>')
    gm = _lin(z, (40, 0), (860, 0), "#d8c8ae", "#efe3cc", "#e4d6bc", "#c4b294")
    z(f'<rect x="40" y="120" width="820" height="690" fill="{gm}"/>')
    # zócalo de piedra
    _ladrillos(z, 40, 700, 860, 810, ("#8a7a6a", "#a08e7a", "#7a6a5a", "#958472"), 9, op=0.9)
    z('<rect x="40" y="696" width="820" height="8" fill="#6a5a4a"/>')
    r = random.Random(13)
    for _ in range(30):
        z(f'<ellipse cx="{F(r.uniform(60, 840))}" cy="{F(r.uniform(140, 680))}" rx="{F(r.uniform(20, 60))}" ry="{F(r.uniform(6, 20))}" '
          f'fill="{r.choice(["#ffffff", "#8a7a60"])}" opacity="0.07"/>')
    z('<rect x="40" y="128" width="820" height="20" fill="#000" opacity="0.15"/>', '<path d="M857 130 L857 810" stroke="#ffd9a0" stroke-width="5" opacity="0.4"/>')
    gw = _lin(z, (0, 104), (0, 132), "#9a4a54", "#7a2a3a", "#4a1420")
    z(f'<rect x="26" y="104" width="848" height="28" rx="5" fill="{gw}"/>')
    # escaparate (mismo hueco que la hamburguesería) con tartas y tazas
    gi = _lin(z, (0, 330), (0, 760), "#ffe8c0", "#ffcf8a", "#e8a058")
    z(f'<rect x="110" y="330" width="420" height="400" rx="10" fill="{gi}"/>')
    for x in (200, 320, 440):
        z(f'<path d="M{x} 330 L{x} 372" stroke="#3a2a20" stroke-width="3"/>', f'<circle cx="{x}" cy="386" r="16" fill="#fff8e0"/>')
        gb = z.rad((x, 400), 80, [(0, "#fff6d8", 0.7), (1, "#fff6d8", 0)])
        z(f'<circle cx="{x}" cy="410" r="80" fill="{gb}"/>')
    # balda con tazas
    z('<rect x="124" y="470" width="392" height="10" fill="#8a5a32"/>')
    cols = ["#7a2a3a", "#fffaf0", "#6f8f7a", "#fffaf0", "#e0a92e", "#fffaf0", "#7a2a3a"]
    for i, x in enumerate(range(150, 510, 54)):
        col = cols[i % len(cols)]
        z(f'<path d="M{x - 16} 444 L{x + 16} 444 L{x + 12} 470 L{x - 12} 470 Z" fill="{col}"/>',
          f'<path d="M{x + 15} 450 Q{x + 26} 452 {x + 14} 462" stroke="{col}" stroke-width="4" fill="none"/>',
          f'<path d="M{x - 12} 446 L{x - 10} 466" stroke="#ffffff" stroke-width="3" opacity="0.4"/>')
    # vitrina con tartas
    z('<rect x="124" y="610" width="392" height="120" fill="#6a2430"/>', '<rect x="124" y="602" width="392" height="12" fill="#d8b088"/>')
    _tarta(z, 180, 600, 1.0)
    _tarta(z, 290, 600, 1.15, crema="#fff6e0", base="#7a4a2a", fruta="#f0e0c0")
    _tarta(z, 405, 600, 1.0, crema="#fffaf0", base="#f4d06a", fruta="#e86a2a")
    z('<path d="M124 520 L516 520 L516 602 L124 602 Z" fill="#ffffff" opacity="0.08"/>', '<path d="M124 520 L516 520" stroke="#ffffff" stroke-width="2" opacity="0.5"/>')
    z('<path d="M140 340 L230 340 L150 720 L110 720 Z" fill="#ffffff" opacity="0.12"/>', '<path d="M260 340 L300 340 L220 720 L200 720 Z" fill="#ffffff" opacity="0.08"/>')
    z('<rect x="110" y="330" width="420" height="400" rx="10" fill="none" stroke="#3a1a20" stroke-width="12"/>')
    # jardinera con flores bajo el escaparate
    gj = _lin(z, (0, 728), (0, 770), "#8a5a32", "#5a3a1e")
    z(f'<rect x="96" y="730" width="448" height="40" rx="6" fill="{gj}"/>', '<path d="M100 732 L540 732" stroke="#e8c090" stroke-width="3" opacity="0.6"/>')
    r = random.Random(17)
    for _ in range(26):
        x = r.uniform(110, 530)
        y = r.uniform(700, 728)
        z(f'<ellipse cx="{F(x)}" cy="{F(y + 10)}" rx="12" ry="6" fill="{r.choice(["#3f7a3a", "#4f8a44"])}" transform="rotate({F(r.uniform(-40, 40))} {F(x)} {F(y + 10)})"/>')
    for _ in range(22):
        x = r.uniform(112, 528)
        y = r.uniform(690, 722)
        col = r.choice(["#f06a8a", "#fff4f0", "#ffd23a", "#c84a7a", "#ff9aa8"])
        z(*[f'<circle cx="{F(x + 6 * math.cos(a))}" cy="{F(y + 6 * math.sin(a))}" r="5" fill="{col}"/>' for a in (0, 1.26, 2.51, 3.77, 5.03)],
          f'<circle cx="{F(x)}" cy="{F(y)}" r="3.5" fill="#e8a020"/>')
    # puerta abierta con luz
    gp = _lin(z, (0, 360), (0, 800), "#ffd89a", "#f0a050")
    z(f'<rect x="590" y="360" width="200" height="450" fill="{gp}"/>', '<path d="M590 360 L560 380 L560 800 L590 810 Z" fill="#5a2a30"/>',
      '<rect x="590" y="360" width="200" height="450" fill="none" stroke="#3a1a20" stroke-width="12"/>')
    # flores trepando por el marco de la puerta
    pts = [(578, 800), (572, 700), (580, 600), (570, 500), (582, 400), (600, 346), (690, 340), (780, 346), (800, 420), (806, 520)]
    z(f'<path d="{IP.suave(pts, cerrado=False)}" stroke="#3f5a2a" stroke-width="4" fill="none"/>')
    r = random.Random(19)
    for i in range(len(pts) - 1):
        for t in (0.2, 0.6):
            x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t
            y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t
            z(f'<ellipse cx="{F(x + 10)}" cy="{F(y)}" rx="11" ry="6" fill="#4f8a44" transform="rotate(35 {F(x + 10)} {F(y)})"/>',
              f'<ellipse cx="{F(x - 10)}" cy="{F(y + 4)}" rx="11" ry="6" fill="#3f7a3a" transform="rotate(-35 {F(x - 10)} {F(y + 4)})"/>')
            if r.random() < 0.75:
                col = r.choice(["#f06a8a", "#ff9aa8", "#fff4f0", "#c84a7a"])
                z(*[f'<circle cx="{F(x + 7 * math.cos(a) + 4)}" cy="{F(y + 7 * math.sin(a) - 6)}" r="6" fill="{col}"/>' for a in (0, 1.26, 2.51, 3.77, 5.03)],
                  f'<circle cx="{F(x + 4)}" cy="{F(y - 6)}" r="4" fill="#f0b030"/>')
    # toldo granate a rayas
    for i in range(10):
        x0 = 30 + i * 84
        col = "#7a2a3a" if i % 2 == 0 else "#9a3e4e"
        som = "#4a1420" if i % 2 == 0 else "#6a2432"
        z(f'<path d="M{x0} 250 L{x0+84} 250 L{x0+94} 315 L{x0+10} 315 Z" fill="{col}"/>',
          f'<path d="M{x0+10} 315 Q{x0+52} 345 {x0+94} 315 Z" fill="{col}"/>',
          f'<path d="M{x0+10} 315 L{x0+94} 315 L{x0+92} 322 L{x0+12} 322 Z" fill="{som}" opacity="0.7"/>')
    gt = z.lin((0, 250), (0, 322), [(0, "#ffffff", 0.2), (0.5, "#ffffff", 0), (1, "#000000", 0.15)])
    z(f'<path d="M30 250 L870 250 L874 322 L40 322 Z" fill="{gt}"/>', '<rect x="22" y="236" width="856" height="18" rx="6" fill="#3a1a20"/>')
    z('<path d="M40 330 L860 330 L860 350 L40 350 Z" fill="#000" opacity="0.12"/>')
    # cartel redondo con taza y corazón
    gh = z.rad((450, 130), 170, [(0, "#ffd890", 0.5), (1, "#ffd890", 0)])
    gc = z.rad((430, 110), 130, [(0, "#9a3e4e"), (0.7, "#7a2a3a"), (1, "#4a1420")])
    z(f'<circle cx="450" cy="130" r="170" fill="{gh}"/>', f'<circle cx="456" cy="138" r="112" fill="#000" opacity="0.22"/>',
      f'<circle cx="450" cy="130" r="112" fill="{gc}"/>', '<circle cx="450" cy="130" r="104" fill="none" stroke="#f4d9a0" stroke-width="6"/>',
      '<path d="M392 100 L508 100 L496 180 Q450 196 404 180 Z" fill="#fffaf0"/>',
      '<path d="M506 112 Q540 114 530 140 Q522 160 498 160" stroke="#fffaf0" stroke-width="10" fill="none"/>',
      '<ellipse cx="450" cy="100" rx="58" ry="12" fill="#c8905a"/>',
      '<path d="M450 112 C438 98 422 104 432 92 C438 86 446 88 450 94 C454 88 462 86 468 92 C478 104 462 98 450 112 Z" fill="#fff4e0"/>',
      '<path d="M404 108 L414 176" stroke="#d8d0c0" stroke-width="5" opacity="0.6"/>',
      *[f'<path d="M{x} 82 C{x - 10} 66 {x + 10} 56 {x} 40" stroke="#fffaf0" stroke-width="5" opacity="0.6" fill="none" stroke-linecap="round"/>' for x in (432, 468)],
      '<path d="M370 80 A96 96 0 0 1 470 34" stroke="#ffffff" stroke-width="8" opacity="0.28" fill="none" stroke-linecap="round"/>')
    # pizarra de caballete con un corazón de latte art (tiza)
    sombra_suelo(z, 470, 812, 90, 10)
    z('<path d="M408 812 L438 586 M532 812 L502 586" stroke="#6a4428" stroke-width="12" stroke-linecap="round"/>',
      '<rect x="414" y="590" width="112" height="170" rx="6" fill="#6a4428"/>',
      '<rect x="424" y="600" width="92" height="150" rx="3" fill="#25302a"/>',
      '<rect x="424" y="600" width="92" height="150" rx="3" fill="#ffffff" opacity="0.05"/>',
      '<path d="M440 660 L500 660 L494 712 Q470 722 446 712 Z" fill="none" stroke="#f4f0e8" stroke-width="3.5"/>',
      '<path d="M499 668 Q514 670 510 684 Q506 696 494 696" stroke="#f4f0e8" stroke-width="3.5" fill="none"/>',
      '<path d="M470 676 C462 666 450 672 456 662 C460 656 467 658 470 663 C473 658 480 656 484 662 C490 672 478 666 470 676 Z" fill="#f4c8c8"/>',
      '<path d="M470 652 C464 638 476 630 470 618 M482 650 C478 640 488 634 484 624" stroke="#f4f0e8" stroke-width="3" fill="none" opacity="0.8"/>',
      '<path d="M436 730 L504 730" stroke="#f4f0e8" stroke-width="3" opacity="0.5" stroke-dasharray="6 6"/>',
      '<path d="M416 592 L416 758" stroke="#c89a68" stroke-width="3" opacity="0.6"/>')
    _planta(z, 828, 812, 220, 23)
    _planta(z, 72, 812, 220, 24)
    return _fin(z)


# ============================================================================ COLEGIO
_MAD = ("#d8a46a", "#b07a46", "#7a4a26", "#4a2e16")


def _pupitre(n, w):
    h = 480
    z = _pz(n, w, h)
    m = 26
    top_b, top_f = 40, round(0.35 * h)   # borde trasero y delantero del tablero (vista algo cenital)
    sombra_suelo(z, w / 2, h - 10, w * 0.46, 16)
    # patas metálicas traseras
    for x in (m + 70, w - m - 70):
        z(f'<rect x="{x - 8}" y="{top_f}" width="16" height="{h - 52 - top_f}" fill="#3a4048"/>')
    # cajón (caja bajo el tablero, abierta por delante: se ve el hueco)
    cy0, cy1 = top_f + 18, top_f + 128
    gcj = _lin(z, (0, cy0), (0, cy1), _MAD[1], _MAD[2])
    z(f'<rect x="{m + 30}" y="{cy0}" width="{w - 2 * m - 60}" height="{cy1 - cy0}" rx="4" fill="{gcj}"/>',
      f'<rect x="{m + 48}" y="{cy0 + 14}" width="{w - 2 * m - 96}" height="{cy1 - cy0 - 30}" rx="3" fill="#2a1a10"/>',
      f'<rect x="{m + 48}" y="{cy0 + 14}" width="{w - 2 * m - 96}" height="14" fill="#000" opacity="0.4"/>')
    # libros dentro del cajón
    r = random.Random(len(n))
    x = m + 60
    while x < w - m - 110:
        bw = r.uniform(26, 44)
        col = r.choice(["#c8322a", "#2f6fb0", "#e0a92e", "#3a8a5e", "#7a2a3a"])
        hb = r.uniform(44, 62)
        z(f'<rect x="{F(x)}" y="{F(cy1 - 16 - hb)}" width="{F(bw)}" height="{F(hb)}" fill="{col}"/>',
          f'<rect x="{F(x)}" y="{F(cy1 - 16 - hb)}" width="4" height="{F(hb)}" fill="#ffffff" opacity="0.3"/>')
        x += bw + r.uniform(4, 30)
    z(f'<rect x="{m + 48}" y="{cy1 - 16}" width="{w - 2 * m - 96}" height="10" fill="#000" opacity="0.3"/>',
      f'<path d="M{m + 31} {cy1 - 2} L{w - m - 31} {cy1 - 2}" stroke="{_MAD[3]}" stroke-width="4"/>',
      f'<path d="M{w - m - 32} {cy0} L{w - m - 32} {cy1}" stroke="{z.rim}" stroke-width="3" opacity="0.5"/>')
    # patas delanteras con travesaño y tacos
    gpm = _lin(z, (0, 0), (18, 0), "#8a929c", "#c8ced6", "#4a525c")
    for x in (m + 40, w - m - 40):
        z(f'<g transform="translate({x - 10} 0)"><rect x="0" y="{top_f}" width="20" height="{h - 30 - top_f}" fill="{gpm}"/></g>',
          f'<rect x="{x - 14}" y="{h - 34}" width="28" height="12" rx="5" fill="#2a2a2e"/>')
    z(f'<rect x="{m + 40}" y="{h - 150}" width="{w - 2 * m - 80}" height="10" fill="#5a626c"/>',
      f'<path d="M{m + 40} {h - 150} L{w - m - 40} {h - 150}" stroke="#d0d6de" stroke-width="2" opacity="0.6"/>')
    # tablero: cara superior (trapecio) y canto
    gt = _lin(z, (0, top_b), (0, top_f), _MAD[1], _MAD[0], "#e8b878")
    z(f'<path d="M{m + 60} {top_b} L{w - m - 60} {top_b} L{w - m} {top_f} L{m} {top_f} Z" fill="{gt}"/>')
    r = random.Random(3)
    for k in range(7):
        y = top_b + 8 + k * (top_f - top_b - 12) / 7
        z(f'<path d="M{m + 20} {F(y)} Q{w * 0.4:.0f} {F(y + r.uniform(-4, 4))} {w * 0.6:.0f} {F(y + r.uniform(-3, 3))} T{w - m - 20} {F(y)}" '
          f'stroke="{_MAD[2]}" stroke-width="1.2" opacity="0.3" fill="none"/>')
    z(f'<path d="M{m + 90} {top_b + 14} L{w * 0.45:.0f} {top_b + 14}" stroke="#ffffff" stroke-width="6" opacity="0.2" stroke-linecap="round"/>',
      f'<path d="M{m + 80} {top_b + 10} L{m + 160} {top_b + 10}" stroke="#7a4a26" stroke-width="7" opacity="0.5" stroke-linecap="round"/>',
      f'<path d="M{m + 60} {top_b} L{m} {top_f}" stroke="#ffffff" stroke-width="3" opacity="0.4"/>',
      f'<path d="M{w - m - 60} {top_b} L{w - m} {top_f}" stroke="{z.rim}" stroke-width="3" opacity="0.5"/>')
    gc = _lin(z, (0, top_f), (0, top_f + 22), _MAD[2], _MAD[3])
    z(f'<rect x="{m}" y="{top_f}" width="{w - 2 * m}" height="22" rx="4" fill="{gc}"/>',
      f'<path d="M{m + 2} {top_f + 1} L{w - m - 2} {top_f + 1}" stroke="#f4d0a0" stroke-width="3"/>',
      f'<path d="M{w - m - 2} {top_f + 2} L{w - m - 2} {top_f + 20}" stroke="{z.rim}" stroke-width="3" opacity="0.6"/>')
    return _fin(z)


def pupitre():
    return _pupitre("pupitre", 600)


def pupitre_doble():
    return _pupitre("pupitre_doble", 1100)


def _hoja(z, w, h, ang=0):
    """Hoja de papel con sombra, curvita en la esquina y grano."""
    x0, y0, x1, y1 = 30, 24, w - 34, h - 36
    d = f"M{x0} {y0} L{x1} {y0} L{x1} {y1 - 40} Q{x1 - 10} {y1 - 8} {x1 - 46} {y1} L{x0} {y1} Z"
    z(f'<g transform="rotate({ang} {w / 2} {h / 2})">')
    z(f'<path d="{d}" fill="#000" opacity="0.28" transform="translate(8 12)"/>')
    g = _lin(z, (x0, y0), (x1, y1), "#ffffff", "#f6f2e8", "#e6dfcf")
    z(f'<path d="{d}" fill="{g}"/>', f'<path d="M{x1} {y1 - 40} Q{x1 - 30} {y1 - 34} {x1 - 46} {y1} Q{x1 - 12} {y1 - 10} {x1} {y1 - 40} Z" fill="#d8d0bc"/>',
      f'<path d="M{x0} {y0} L{x1} {y0}" stroke="#ffffff" stroke-width="3"/>',
      f'<path d="M{x1} {y0} L{x1} {y1 - 40}" stroke="#c8c0ae" stroke-width="2"/>')
    return d, (x0, y0, x1, y1)


def _renglones(z, caja, desde, hasta, seed, col="#3a4a6a", azul=True):
    x0, y0, x1, y1 = caja
    r = random.Random(seed)
    y = desde
    while y < hasta:
        if azul:
            z(f'<path d="M{x0 + 10} {y + 8} L{x1 - 10} {y + 8}" stroke="#9ab8d8" stroke-width="1.5" opacity="0.6"/>')
        fin = x1 - 30 - r.uniform(0, 140)
        z(f'<path d="{_garabato(r, x0 + 40, fin, y, 2.2, 10)}" stroke="{col}" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.8"/>')
        y += 36


def examen():
    w, h = 560, 740
    z = _pz("examen", w, h)
    d, caja = _hoja(z, w, h, -2)
    x0, y0, x1, y1 = caja
    z(f'<path d="M{x0 + 28} {y0} L{x0 + 28} {y1}" stroke="#e08a8a" stroke-width="2" opacity="0.7"/>')
    z(f'<rect x="{x0 + 40}" y="{y0 + 26}" width="200" height="14" rx="7" fill="#3a4a6a" opacity="0.6"/>')
    _renglones(z, caja, y0 + 220, y1 - 30, 41)
    # tachones del alumno
    z(f'<path d="M{x0 + 60} {y0 + 400} l90 -6 M{x0 + 60} {y0 + 406} l90 -8" stroke="#3a4a6a" stroke-width="4" opacity="0.8"/>')
    # nota roja: círculo tachado
    cx, cy, R = x1 - 120, y0 + 110, 78
    z(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#d01e24" stroke-width="13" opacity="0.92" stroke-dasharray="{2 * math.pi * R - 30:.0f} 30" transform="rotate(-70 {cx} {cy})"/>',
      f'<path d="M{cx - 70} {cy + 66} L{cx + 66} {cy - 72}" stroke="#d01e24" stroke-width="14" stroke-linecap="round" opacity="0.92"/>',
      f'<path d="M{x0 + 50} {y0 + 300} q40 -10 70 4 M{x0 + 230} {y0 + 444} q50 10 80 -6" stroke="#d01e24" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.85"/>')
    z('</g>')
    return _fin(z)


def examen_bien():
    w, h = 560, 740
    z = _pz("examen_bien", w, h)
    d, caja = _hoja(z, w, h, 2)
    x0, y0, x1, y1 = caja
    z(f'<path d="M{x0 + 28} {y0} L{x0 + 28} {y1}" stroke="#e08a8a" stroke-width="2" opacity="0.7"/>')
    z(f'<rect x="{x0 + 40}" y="{y0 + 26}" width="200" height="14" rx="7" fill="#3a4a6a" opacity="0.6"/>')
    _renglones(z, caja, y0 + 220, y1 - 30, 43)
    cx, cy = x1 - 130, y0 + 110
    z(f'<path d="M{cx - 80} {cy} L{cx - 22} {cy + 62} L{cx + 92} {cy - 82}" stroke="#1f8a3a" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
      f'<path d="M{cx - 78} {cy - 4} L{cx - 24} {cy + 54}" stroke="#6ad07a" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.6"/>')
    for k in range(4):
        z(f'<path d="M{x1 - 60} {y0 + 236 + k * 72} l10 12 l20 -24" stroke="#1f8a3a" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    z('</g>')
    return _fin(z)


def hoja_dibujo():
    w, h = 740, 560
    z = _pz("hoja_dibujo", w, h)
    d, (x0, y0, x1, y1) = _hoja(z, w, h, 1.5)
    cer = 'stroke-linecap="round" stroke-linejoin="round" fill="none"'
    # sol con rayos (cera amarilla)
    z(f'<circle cx="{x0 + 100}" cy="{y0 + 90}" r="46" fill="#ffd23a" opacity="0.85"/>',
      f'<circle cx="{x0 + 100}" cy="{y0 + 90}" r="46" stroke="#f0a010" stroke-width="6" {cer}/>')
    for k in range(10):
        a = k * 36
        z(f'<path d="M{F(x0 + 100 + 60 * math.cos(math.radians(a)))} {F(y0 + 90 + 60 * math.sin(math.radians(a)))} '
          f'L{F(x0 + 100 + 88 * math.cos(math.radians(a)))} {F(y0 + 90 + 88 * math.sin(math.radians(a)))}" stroke="#f0a010" stroke-width="7" {cer}/>')
    z(f'<path d="M{x0 + 84} {y0 + 84} l2 0 M{x0 + 112} {y0 + 84} l2 0" stroke="#5a3a10" stroke-width="8" {cer}/>',
      f'<path d="M{x0 + 82} {y0 + 102} Q{x0 + 100} {y0 + 118} {x0 + 118} {y0 + 102}" stroke="#5a3a10" stroke-width="5" {cer}/>')
    # nube
    z(f'<path d="M{x0 + 430} {y0 + 90} q-10 -40 30 -40 q20 -30 60 -6 q40 -10 40 30 q20 20 -10 30 z" stroke="#5a9ad8" stroke-width="5" fill="#d8ecff" stroke-linejoin="round"/>')
    # hierba
    z(f'<path d="M{x0 + 10} {y1 - 70} Q{(x0 + x1) / 2} {y1 - 96} {x1 - 20} {y1 - 70} L{x1 - 30} {y1 - 10} L{x0 + 10} {y1 - 10} Z" fill="#7ad86a" opacity="0.7"/>')
    for k in range(26):
        x = x0 + 24 + k * 24
        z(f'<path d="M{x} {y1 - 70 - (8 if 4 < k < 20 else 0)} l6 -18 l6 18" stroke="#2a9a4a" stroke-width="4" {cer}/>')
    # casa
    hx, hy = x0 + 250, y0 + 220
    z(f'<path d="M{hx} {hy} L{hx + 220} {hy + 4} L{hx + 214} {hy + 200} L{hx + 4} {hy + 196} Z" fill="#ff9a6a" stroke="#c8322a" stroke-width="6" stroke-linejoin="round"/>',
      f'<path d="M{hx - 26} {hy + 6} L{hx + 108} {hy - 110} L{hx + 248} {hy + 8} Z" fill="#d84a3a" stroke="#8a1e18" stroke-width="6" stroke-linejoin="round"/>',
      f'<path d="M{hx + 160} {hy - 60} L{hx + 162} {hy - 100} L{hx + 192} {hy - 100} L{hx + 190} {hy - 34}" stroke="#5a3a2a" stroke-width="6" fill="#8a5a3a"/>',
      f'<path d="M{hx + 176} {hy - 108} q-12 -20 4 -34 q18 -14 6 -36" stroke="#9aa0a8" stroke-width="5" {cer}/>',
      f'<path d="M{hx + 84} {hy + 198} L{hx + 84} {hy + 110} L{hx + 140} {hy + 110} L{hx + 140} {hy + 198}" fill="#8a5a3a" stroke="#4a2e16" stroke-width="6"/>',
      f'<circle cx="{hx + 128}" cy="{hy + 156}" r="5" fill="#ffd23a"/>',
      f'<rect x="{hx + 22}" y="{hy + 40}" width="50" height="46" fill="#8acaff" stroke="#2a6ad8" stroke-width="5"/>',
      f'<path d="M{hx + 47} {hy + 40} L{hx + 47} {hy + 86} M{hx + 22} {hy + 63} L{hx + 72} {hy + 63}" stroke="#2a6ad8" stroke-width="4"/>',
      f'<rect x="{hx + 150}" y="{hy + 40}" width="50" height="46" fill="#8acaff" stroke="#2a6ad8" stroke-width="5"/>',
      f'<path d="M{hx + 175} {hy + 40} L{hx + 175} {hy + 86} M{hx + 150} {hy + 63} L{hx + 200} {hy + 63}" stroke="#2a6ad8" stroke-width="4"/>')
    # florecillas y un árbol
    tx = x1 - 110
    z(f'<path d="M{tx} {y1 - 70} L{tx + 4} {y1 - 170}" stroke="#7a4a26" stroke-width="16" {cer}/>',
      f'<circle cx="{tx}" cy="{y1 - 200}" r="56" fill="#3aa84a" opacity="0.85" stroke="#1f7a2e" stroke-width="5"/>',
      *[f'<circle cx="{tx + dx}" cy="{y1 - 200 + dy}" r="7" fill="#e83a3a"/>' for dx, dy in ((-20, -10), (18, -24), (10, 20), (-26, 22))])
    for fx in (x0 + 60, x0 + 120, x0 + 190):
        z(f'<path d="M{fx} {y1 - 30} l0 -34" stroke="#2a9a4a" stroke-width="4"/>', f'<circle cx="{fx}" cy="{y1 - 68}" r="11" fill="#ff6ab0"/>',
          f'<circle cx="{fx}" cy="{y1 - 68}" r="4" fill="#ffd23a"/>')
    z('</g>')
    return _fin(z)


def _timbre(n, vibra):
    w, h = 520, 520
    z = _pz(n, w, h)
    cx, cy = 260, 270
    sh = 6 if vibra else 0
    # placa de la pared
    gpl = _lin(z, (0, 60), (0, 140), "#8a929c", "#5a626c")
    z(f'<rect x="{cx - 50}" y="60" width="100" height="70" rx="12" fill="#000" opacity="0.25" transform="translate(5 7)"/>',
      f'<rect x="{cx - 50}" y="60" width="100" height="70" rx="12" fill="{gpl}"/>',
      f'<circle cx="{cx - 32}" cy="78" r="6" fill="#3a3f44"/><circle cx="{cx + 32}" cy="112" r="6" fill="#3a3f44"/>',
      f'<path d="M{cx - 46} 64 L{cx + 40} 64" stroke="#e0e6ec" stroke-width="3" opacity="0.7"/>',
      f'<rect x="{cx - 12}" y="126" width="24" height="40" fill="#4a525c"/>')
    # campana (cúpula metálica roja) con su sombra en la pared
    gb = z.rad((cx - 60 + sh, cy - 70), 220, [(0, "#ff8a7a"), (0.35, "#d8322a"), (0.8, "#8a1a14"), (1, "#5a0e0a")])
    z(f'<g transform="rotate({4 if vibra else 0} {cx} 160)">',
      f'<circle cx="{cx + 16}" cy="{cy + 22}" r="150" fill="#000" opacity="0.2"/>',
      f'<circle cx="{cx}" cy="{cy}" r="150" fill="{gb}"/>',
      f'<circle cx="{cx}" cy="{cy}" r="150" fill="none" stroke="#5a0e0a" stroke-width="4"/>',
      f'<circle cx="{cx}" cy="{cy}" r="118" fill="none" stroke="#ff9a8a" stroke-width="3" opacity="0.4"/>',
      f'<path d="M{cx - 120} {cy - 40} A130 130 0 0 1 {cx - 20} {cy - 128}" stroke="#ffffff" stroke-width="16" opacity="0.5" fill="none" stroke-linecap="round"/>',
      f'<path d="M{cx + 136} {cy + 30} A140 140 0 0 1 {cx + 40} {cy + 138}" stroke="{z.rim}" stroke-width="8" opacity="0.6" fill="none" stroke-linecap="round"/>',
      f'<circle cx="{cx}" cy="{cy}" r="22" fill="#c8ced6"/><circle cx="{cx - 6}" cy="{cy - 6}" r="8" fill="#ffffff" opacity="0.8"/>',
      '</g>')
    # martillo
    ang = -18 if vibra else 0
    z(f'<g transform="rotate({ang} {cx} {cy + 190})">',
      f'<rect x="{cx - 5}" y="{cy + 150}" width="10" height="50" fill="#5a626c"/>',
      f'<circle cx="{cx}" cy="{cy + 150}" r="16" fill="#3a3f44"/><circle cx="{cx - 5}" cy="{cy + 145}" r="5" fill="#c8ced6"/>',
      '</g>',
      f'<rect x="{cx - 30}" y="{cy + 192}" width="60" height="28" rx="6" fill="#4a525c"/>',
      f'<path d="M{cx - 26} {cy + 196} L{cx + 20} {cy + 196}" stroke="#c8ced6" stroke-width="2"/>')
    if vibra:
        for s in (-1, 1):
            for k, rr in enumerate((180, 215, 248)):
                a0, a1 = (200, 160) if s < 0 else (-20, 20)
                p0 = (cx + rr * math.cos(math.radians(a0)), cy + rr * math.sin(math.radians(a0)))
                p1 = (cx + rr * math.cos(math.radians(a1)), cy + rr * math.sin(math.radians(a1)))
                z(f'<path d="M{F(p0[0])} {F(p0[1])} A{rr} {rr} 0 0 {1 if s > 0 else 0} {F(p1[0])} {F(p1[1])}" stroke="#ffcf3a" stroke-width="{10 - 2 * k}" '
                  f'opacity="{0.95 - 0.2 * k}" fill="none" stroke-linecap="round"/>')
        z(f'<path d="M{cx - 150} {cy - 120} l-30 -30 M{cx + 150} {cy - 120} l30 -30" stroke="#ffcf3a" stroke-width="8" stroke-linecap="round"/>')
    return _fin(z)


def timbre_a():
    return _timbre("timbre_a", False)


def timbre_b():
    return _timbre("timbre_b", True)


def mochila_cole():
    w, h = 520, 640
    z = _pz("mochila_cole", w, h)
    sombra_suelo(z, 260, 616, 200, 18)
    # asa y tirantes detrás
    z('<path d="M210 70 Q260 20 310 70" stroke="#173a60" stroke-width="18" fill="none" stroke-linecap="round"/>',
      '<path d="M120 130 Q70 330 110 560" stroke="#173a60" stroke-width="30" fill="none"/>')
    body = "M110 140 Q110 70 260 66 Q410 70 410 140 L420 560 Q420 612 370 612 L150 612 Q100 612 100 560 Z"
    g = _lin(z, (100, 0), (420, 0), "#5f9fe0", "#2f6fb0", "#173a60")
    z(f'<path d="{body}" fill="{g}"/>',
      '<path d="M130 120 Q160 82 230 76" stroke="#9fd0ff" stroke-width="8" fill="none" opacity="0.6" stroke-linecap="round"/>',
      f'<path d="M410 150 L418 560" stroke="{z.rim}" stroke-width="6" opacity="0.5"/>')
    # cremallera de la tapa
    z('<path d="M120 210 Q260 170 400 210" stroke="#173a60" stroke-width="6" fill="none"/>',
      '<path d="M120 210 Q260 170 400 210" stroke="#c8ced6" stroke-width="2" stroke-dasharray="4 4" fill="none"/>',
      '<rect x="384" y="198" width="14" height="30" rx="5" fill="#e0a92e"/>')
    # bolsillo delantero
    gb = _lin(z, (0, 330), (0, 560), "#e0a92e", "#c88a10")
    z(f'<path d="M150 340 Q260 320 370 340 L376 540 Q376 572 344 572 L176 572 Q144 572 144 540 Z" fill="{gb}"/>',
      '<path d="M150 340 Q260 320 370 340" stroke="#fff0b0" stroke-width="4" fill="none" opacity="0.8"/>',
      '<path d="M156 390 Q260 372 364 390" stroke="#8a6010" stroke-width="5" fill="none"/>',
      '<path d="M156 390 Q260 372 364 390" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4 4" fill="none" opacity="0.7"/>',
      '<rect x="340" y="380" width="12" height="26" rx="4" fill="#173a60"/>',
      '<path d="M154 400 L160 540" stroke="#ffffff" stroke-width="6" opacity="0.25" stroke-linecap="round"/>')
    # estrella reflectante y llavero
    z('<path d="M260 440 L270 466 L298 466 L276 482 L284 508 L260 492 L236 508 L244 482 L222 466 L250 466 Z" fill="#fff6c8" opacity="0.9"/>',
      '<path d="M120 300 L104 330" stroke="#c8ced6" stroke-width="3"/><circle cx="100" cy="346" r="16" fill="#e83a6a"/><circle cx="95" cy="341" r="5" fill="#ffffff" opacity="0.6"/>')
    return _fin(z)


# ============================================================================ COMIDA Y NEGOCIO
def hamburguesa():
    w, h = 620, 520
    z = _pz("hamburguesa", w, h)
    sombra_suelo(z, 310, 494, 260, 22)
    gpan_b = _lin(z, (0, 400), (0, 480), "#e8a050", "#b8662a")
    z(f'<path d="M80 410 L540 410 Q544 476 470 484 L150 484 Q76 476 80 410 Z" fill="{gpan_b}"/>',
      '<path d="M96 420 L524 420" stroke="#f4c88a" stroke-width="4" opacity="0.6"/>')
    # carne
    gc = _lin(z, (0, 330), (0, 410), "#7a3a1a", "#4a200c", "#2a1206")
    z(f'<path d="M66 350 Q60 330 100 326 L520 326 Q560 330 554 350 L556 392 Q556 414 520 414 L100 414 Q64 414 64 392 Z" fill="{gc}"/>')
    r = random.Random(5)
    for _ in range(50):
        x, y = r.uniform(80, 540), r.uniform(334, 404)
        z(f'<circle cx="{F(x)}" cy="{F(y)}" r="{F(r.uniform(2, 5))}" fill="{r.choice(["#8a4a24", "#2a1206"])}" opacity="0.7"/>')
    z('<path d="M90 336 L530 336" stroke="#a8643a" stroke-width="4" opacity="0.5"/>')
    # queso fundido
    z('<path d="M70 318 L550 318 L556 336 L500 336 L486 380 L470 336 L330 336 L316 372 L300 336 L150 336 L130 392 L114 336 L64 336 Z" fill="#f4b81a"/>',
      '<path d="M76 320 L540 320" stroke="#ffe27a" stroke-width="4"/>')
    # tomate y lechuga
    z('<path d="M90 300 Q310 284 530 300 L536 322 L84 322 Z" fill="#e0402a"/>', '<path d="M100 304 Q300 292 520 304" stroke="#ff8a6a" stroke-width="3" fill="none"/>')
    let = "M62 300 " + " ".join(f"Q{70 + i * 40 + 20} {286 + (14 if i % 2 else -6)} {70 + (i + 1) * 40} 298" for i in range(12)) + " L560 312 L60 312 Z"
    z(f'<path d="{let}" fill="#6ab04a"/>', '<path d="M70 300 Q300 290 548 300" stroke="#a8e07a" stroke-width="3" fill="none" opacity="0.7"/>')
    # pan de arriba
    gpa = z.rad((230, 140), 360, [(0, "#ffd090"), (0.45, "#e8a050"), (1, "#a85a20")])
    z(f'<path d="M70 296 Q60 90 310 80 Q560 90 550 296 Q310 312 70 296 Z" fill="{gpa}"/>',
      '<path d="M130 210 Q150 130 250 108" stroke="#fff0c8" stroke-width="18" opacity="0.45" fill="none" stroke-linecap="round"/>',
      f'<path d="M530 200 Q520 260 490 290" stroke="{z.rim}" stroke-width="7" opacity="0.5" fill="none"/>')
    for _ in range(26):
        x, y = r.uniform(130, 500), r.uniform(120, 250)
        if ((x - 310) / 230) ** 2 + ((y - 290) / 200) ** 2 > 1:
            continue
        a = r.uniform(-40, 40)
        z(f'<ellipse cx="{F(x)}" cy="{F(y)}" rx="8" ry="4.5" fill="#fff4d8" transform="rotate({F(a)} {F(x)} {F(y)})"/>',
          f'<ellipse cx="{F(x + 1)}" cy="{F(y + 2)}" rx="7" ry="3" fill="#c88a40" opacity="0.5" transform="rotate({F(a)} {F(x)} {F(y)})"/>')
    return _fin(z)


def bolsa_comida():
    w, h = 460, 640
    z = _pz("bolsa_comida", w, h)
    sombra_suelo(z, 230, 618, 190, 16)
    g = _lin(z, (60, 0), (400, 0), "#e8c898", "#d4a870", "#a87a48")
    z('<path d="M330 150 L400 128 L404 600 L340 612 Z" fill="#8a6038"/>',
      f'<path d="M60 150 L340 150 L340 612 L56 606 Z" fill="{g}"/>',
      '<path d="M60 150 L340 150 L340 196 L60 200 Z" fill="#c89a62"/>',
      '<path d="M60 200 L340 196" stroke="#8a6038" stroke-width="3" opacity="0.6"/>',
      '<path d="M60 150 ' + ' '.join(f'L{70 + k * 20} {138 if k % 2 == 0 else 150}' for k in range(14)) + ' L340 150 Z" fill="#d4a870"/>',
      '<path d="M340 150 L400 128 L400 176 L340 196 Z" fill="#7a5230"/>',
      '<path d="M60 150 L340 150" stroke="#f4dcae" stroke-width="3"/>',
      '<path d="M120 150 L104 600 M200 150 L204 606" stroke="#a87a48" stroke-width="1.5" opacity="0.4"/>')
    # fuelle lateral y pliegue
    z('<path d="M340 150 L372 300 L340 612" stroke="#6a4424" stroke-width="2" fill="none" opacity="0.6"/>',
      f'<path d="M398 140 L402 590" stroke="{z.rim}" stroke-width="4" opacity="0.45"/>')
    # mancha de grasa y pegatina roja lisa con una hamburguesita
    z('<ellipse cx="270" cy="500" rx="30" ry="22" fill="#a87a48" opacity="0.35"/>',
      '<circle cx="200" cy="330" r="74" fill="#c8322a"/><circle cx="200" cy="330" r="66" fill="none" stroke="#f3e6cf" stroke-width="4"/>',
      '<path d="M160 330 Q160 288 200 286 Q240 288 240 330 Z" fill="#f0b050"/><rect x="156" y="332" width="88" height="10" rx="4" fill="#6ab04a"/>',
      '<rect x="156" y="344" width="88" height="14" rx="6" fill="#6a3418"/><path d="M160 360 L240 360 Q240 376 200 378 Q160 376 160 360 Z" fill="#f0b050"/>',
      '<path d="M150 300 Q160 270 190 262" stroke="#ffffff" stroke-width="5" opacity="0.4" fill="none" stroke-linecap="round"/>')
    return _fin(z)


def taza_cafe_latte():
    w, h = 560, 470
    z = _pz("taza_cafe_latte", w, h)
    sombra_suelo(z, 270, 420, 240, 34)
    # platillo
    gp = z.rad((240, 380), 260, [(0, "#ffffff"), (0.7, "#ece6dc"), (1, "#b8aea0")])
    z(f'<ellipse cx="270" cy="392" rx="240" ry="62" fill="{gp}"/>', '<ellipse cx="270" cy="384" rx="150" ry="36" fill="#d8d0c2"/>')
    # asa
    z('<path d="M430 210 C520 200 530 320 420 330" stroke="#e8e2d8" stroke-width="30" fill="none" stroke-linecap="round"/>',
      '<path d="M436 214 C508 208 514 300 428 318" stroke="#ffffff" stroke-width="7" opacity="0.6" fill="none"/>')
    # cuerpo
    gt = _lin(z, (110, 0), (440, 0), "#f4f0ea", "#ffffff", "#e0d8cc", "#a8a090")
    z(f'<path d="M100 180 L440 180 L414 330 Q400 392 270 394 Q140 392 126 330 Z" fill="{gt}"/>',
      '<path d="M132 210 Q140 300 170 360" stroke="#ffffff" stroke-width="14" opacity="0.7" fill="none" stroke-linecap="round"/>',
      f'<path d="M430 200 L408 330" stroke="{z.rim}" stroke-width="5" opacity="0.4"/>')
    # boca y café con corazón de espuma
    z('<ellipse cx="270" cy="180" rx="172" ry="60" fill="#f6f2ec"/>')
    gc = z.rad((250, 180), 160, [(0, "#c8905a"), (0.75, "#8a5428"), (1, "#4a2a12")])
    z(f'<ellipse cx="270" cy="184" rx="152" ry="50" fill="{gc}"/>',
      '<ellipse cx="270" cy="184" rx="152" ry="50" fill="none" stroke="#d8a878" stroke-width="5" opacity="0.6"/>')
    z('<path d="M270 222 C220 198 196 178 210 158 C222 142 252 146 266 168 C268 160 276 146 296 146 C330 146 340 172 322 192 C310 206 290 214 270 222 Z" fill="#fbf2e0"/>',
      '<path d="M270 208 C238 192 224 180 232 166 C240 156 256 160 266 176 M276 176 C284 160 304 156 312 168 C318 182 300 196 276 206" stroke="#e8c8a0" stroke-width="3" fill="none" opacity="0.8"/>',
      '<path d="M270 222 L270 236" stroke="#fbf2e0" stroke-width="4" stroke-linecap="round"/>',
      '<path d="M140 166 Q200 136 280 134" stroke="#ffffff" stroke-width="4" opacity="0.5" fill="none"/>')
    return _fin(z)


def reloj_pared():
    w, h = 520, 520
    z = _pz("reloj_pared", w, h)
    _reloj_esfera(z, 254, 252, 230, marco="#2a2a2e")
    return _fin(z)


def reloj_arena_grande():
    IO._reloj_arena("reloj_arena_grande", True)
    NOMBRES.append("reloj_arena_grande")
    return "reloj_arena_grande"


def _cerdito(z, roto=False):
    gp = z.rad((210, 210), 300, [(0, "#ffd0dc"), (0.5, "#f49ab0"), (1, "#c05a78")])
    if not roto:
        z('<rect x="160" y="400" width="44" height="60" rx="14" fill="#c86a88"/><rect x="380" y="400" width="44" height="60" rx="14" fill="#c86a88"/>')
        z('<rect x="120" y="390" width="48" height="74" rx="16" fill="#e889a2"/><rect x="340" y="390" width="48" height="74" rx="16" fill="#e889a2"/>',
          '<path d="M520 240 q40 -10 30 30 q-10 30 20 30" stroke="#e889a2" stroke-width="10" fill="none" stroke-linecap="round"/>')
        z(f'<ellipse cx="300" cy="280" rx="230" ry="170" fill="{gp}"/>',
          '<path d="M200 130 L220 70 L270 120 Z" fill="#e889a2"/><path d="M212 120 L224 84 L252 116 Z" fill="#c05a78"/>',
          '<path d="M360 118 L400 64 L420 128 Z" fill="#d87a96"/>',
          '<ellipse cx="96" cy="290" rx="46" ry="56" fill="#f4a8bc"/><ellipse cx="88" cy="290" rx="34" ry="44" fill="#e889a2"/>',
          '<ellipse cx="78" cy="276" rx="7" ry="12" fill="#8a3a52"/><ellipse cx="78" cy="306" rx="7" ry="12" fill="#8a3a52"/>',
          '<circle cx="170" cy="230" r="12" fill="#2a1a20"/><circle cx="166" cy="226" r="4" fill="#ffffff"/>',
          '<path d="M150 208 Q170 196 190 206" stroke="#8a3a52" stroke-width="4" fill="none" stroke-linecap="round"/>',
          '<ellipse cx="190" cy="290" rx="24" ry="12" fill="#ff7a9a" opacity="0.5"/>',
          '<rect x="270" y="120" width="90" height="14" rx="7" fill="#5a1a30"/><rect x="274" y="122" width="82" height="4" rx="2" fill="#2a0a14"/>',
          '<path d="M180 170 Q260 110 360 124" stroke="#ffffff" stroke-width="16" opacity="0.45" fill="none" stroke-linecap="round"/>',
          f'<path d="M520 250 Q520 380 420 430" stroke="{z.rim}" stroke-width="8" opacity="0.55" fill="none"/>')


def hucha():
    w, h = 600, 500
    z = _pz("hucha", w, h)
    sombra_suelo(z, 290, 466, 230, 20)
    _cerdito(z)
    return _fin(z)


def _moneda(z, x, y, r, ang=0, canto=0.35):
    """Moneda dorada en perspectiva (sin símbolos)."""
    ry = r * canto
    g = _lin(z, (x - r, 0), (x + r, 0), "#8a5a10", "#f6d27a", "#d8a030", "#7a4a08")
    z(f'<g transform="rotate({ang} {F(x)} {F(y)})">',
      f'<ellipse cx="{F(x)}" cy="{F(y + r * 0.16)}" rx="{F(r)}" ry="{F(ry)}" fill="#7a4a08"/>',
      f'<rect x="{F(x - r)}" y="{F(y)}" width="{F(2 * r)}" height="{F(r * 0.16)}" fill="{g}"/>',
      f'<ellipse cx="{F(x)}" cy="{F(y)}" rx="{F(r)}" ry="{F(ry)}" fill="#f0c04a"/>',
      f'<ellipse cx="{F(x)}" cy="{F(y)}" rx="{F(r * 0.78)}" ry="{F(ry * 0.78)}" fill="none" stroke="#b88214" stroke-width="{F(r * 0.06)}"/>',
      f'<ellipse cx="{F(x - r * 0.25)}" cy="{F(y - ry * 0.3)}" rx="{F(r * 0.4)}" ry="{F(ry * 0.25)}" fill="#fff4c0" opacity="0.6"/>',
      '</g>')


def hucha_rota():
    w, h = 760, 460
    z = _pz("hucha_rota", w, h)
    sombra_suelo(z, 380, 420, 330, 26)
    gp = z.rad((300, 250), 340, [(0, "#ffd0dc"), (0.5, "#f49ab0"), (1, "#c05a78")])
    gin = z.rad((360, 330), 200, [(0, "#5a1a30"), (1, "#a84a68")])
    # mitad trasera del cerdito: cáscara con el borde roto y el hueco oscuro dentro
    borde = "M210 300 L240 250 L268 282 L300 226 L334 270 L368 236 L398 284 L436 250 L470 300 L500 286"
    z(f'<path d="M200 300 Q190 410 330 418 Q470 418 520 360 Q540 320 500 286 Z" fill="{gp}"/>',
      f'<path d="{borde} Q440 300 350 312 Q260 318 210 300 Z" fill="{gin}"/>',
      f'<path d="{borde}" stroke="#fff0f4" stroke-width="6" fill="none" stroke-linejoin="round"/>',
      '<path d="M500 300 q40 -10 34 26 q-6 26 20 28" stroke="#e889a2" stroke-width="10" fill="none" stroke-linecap="round"/>',
      '<rect x="420" y="384" width="44" height="40" rx="12" fill="#c86a88"/><rect x="250" y="390" width="44" height="34" rx="12" fill="#e889a2"/>',
      '<path d="M222 340 Q240 392 300 404" stroke="#ffffff" stroke-width="10" opacity="0.35" fill="none" stroke-linecap="round"/>')
    # monedas saliendo del hueco
    for (x, y, rr, a) in ((320, 300, 30, -6), (380, 296, 28, 10)):
        _moneda(z, x, y, rr, a)
    # cabeza rota caída a la izquierda
    gc = z.rad((120, 250), 200, [(0, "#ffd0dc"), (0.55, "#f49ab0"), (1, "#c05a78")])
    z('<g transform="rotate(-18 130 320)">',
      f'<path d="M180 210 L160 250 L190 280 L166 320 L196 360 Q150 420 90 400 Q30 380 30 300 Q34 220 110 200 Z" fill="{gc}"/>',
      '<path d="M180 210 L160 250 L190 280 L166 320 L196 360" stroke="#fff0f4" stroke-width="5" fill="none" stroke-linejoin="round"/>',
      '<path d="M110 206 L120 150 L160 206 Z" fill="#e889a2"/><path d="M120 196 L126 166 L146 196 Z" fill="#c05a78"/>',
      '<ellipse cx="44" cy="310" rx="34" ry="42" fill="#f4a8bc"/><ellipse cx="38" cy="310" rx="24" ry="32" fill="#e889a2"/>',
      '<ellipse cx="32" cy="296" rx="5" ry="9" fill="#8a3a52"/><ellipse cx="32" cy="322" rx="5" ry="9" fill="#8a3a52"/>',
      '<path d="M96 266 q12 8 24 0" stroke="#2a1a20" stroke-width="5" fill="none" stroke-linecap="round"/>',
      '<path d="M92 252 q14 -8 30 -2" stroke="#8a3a52" stroke-width="4" fill="none" stroke-linecap="round" transform="rotate(10 108 250)"/>',
      '<ellipse cx="104" cy="330" rx="20" ry="10" fill="#ff7a9a" opacity="0.5"/>',
      '<path d="M60 236 Q80 214 110 210" stroke="#ffffff" stroke-width="8" opacity="0.4" fill="none" stroke-linecap="round"/>',
      '</g>')
    r = random.Random(9)
    for _ in range(10):
        x, y = r.uniform(520, 730), r.uniform(370, 420)
        s = r.uniform(14, 30)
        z(f'<path d="M{F(x)} {F(y)} l{F(s)} {F(-s * 0.4)} l{F(-s * 0.3)} {F(s * 0.7)} Z" fill="{r.choice(["#f49ab0", "#e889a2", "#ffd0dc"])}" '
          f'transform="rotate({F(r.uniform(0, 360))} {F(x)} {F(y)})"/>')
    for (x, y, rr, a) in ((560, 400, 32, -6), (640, 380, 26, 10), (230, 420, 28, 6), (600, 426, 24, 0), (690, 414, 22, -8)):
        _moneda(z, x, y, rr, a)
    return _fin(z)


def billete():
    w, h = 760, 400
    z = _pz("billete", w, h)
    d = "M30 50 Q200 30 380 46 Q560 62 730 44 L730 340 Q560 360 380 344 Q200 328 30 350 Z"
    z(f'<path d="{d}" fill="#000" opacity="0.25" transform="translate(8 12)"/>')
    g = _lin(z, (30, 50), (730, 350), "#b8dcae", "#7ab87a", "#5a9a62", "#8ac88a")
    z(f'<path d="{d}" fill="{g}"/>')
    cl = z.clip(d)
    z(f'<g clip-path="{cl}">',
      '<rect x="60" y="80" width="640" height="240" rx="18" fill="none" stroke="#2f6a3e" stroke-width="5" opacity="0.7"/>',
      '<rect x="74" y="94" width="612" height="212" rx="12" fill="none" stroke="#e8f8e0" stroke-width="2" opacity="0.6"/>')
    # guilloché (rosetas) y hoja central en lugar de cara
    for cx in (170, 590):
        for k in range(12):
            z(f'<ellipse cx="{cx}" cy="200" rx="62" ry="22" fill="none" stroke="#2f6a3e" stroke-width="1.6" opacity="0.6" transform="rotate({k * 15} {cx} 200)"/>')
        z(f'<circle cx="{cx}" cy="200" r="14" fill="#2f6a3e" opacity="0.6"/>')
    z('<ellipse cx="380" cy="200" rx="110" ry="80" fill="#e8f8e0" opacity="0.35"/>',
      '<path d="M380 270 C320 230 320 160 380 120 C440 160 440 230 380 270 Z" fill="#2f6a3e" opacity="0.55"/>',
      '<path d="M380 270 L380 130 M380 230 L352 200 M380 200 L408 172 M380 180 L356 158" stroke="#e8f8e0" stroke-width="3" opacity="0.7"/>')
    for k in range(18):
        y = 86 + k * 13
        z(f'<path d="M260 {y} Q300 {y - 6} 320 {y} M440 {y} Q460 {y + 6} 500 {y}" stroke="#2f6a3e" stroke-width="1.2" opacity="0.35" fill="none"/>')
    z('<path d="M30 50 Q200 30 380 46 L380 344 Q200 328 30 350 Z" fill="#ffffff" opacity="0.08"/>', '</g>',
      '<path d="M32 52 Q200 32 380 48" stroke="#ffffff" stroke-width="3" opacity="0.6" fill="none"/>',
      f'<path d="M728 50 L728 336" stroke="{z.rim}" stroke-width="3" opacity="0.5"/>')
    return _fin(z)


def monedas():
    w, h = 560, 310
    z = _pz("monedas", w, h)
    z('<g transform="translate(0 -110)">')
    sombra_suelo(z, 270, 384, 240, 26)
    for k in range(7):
        _moneda(z, 190, 340 - k * 22, 80, 0)
    for k in range(4):
        _moneda(z, 360, 350 - k * 22, 70, 0)
    _moneda(z, 470, 368, 50, 6)
    _moneda(z, 90, 376, 44, -8)
    _destello(z, 150, 180, 18)
    _destello(z, 400, 266, 12)
    z('</g>')
    return _fin(z)


def _destello(z, x, y, L, col="#ffffff", op=0.95):
    z(f'<path d="M{F(x)} {F(y - L)} Q{F(x + L * 0.14)} {F(y - L * 0.14)} {F(x + L)} {F(y)} Q{F(x + L * 0.14)} {F(y + L * 0.14)} {F(x)} {F(y + L)} '
      f'Q{F(x - L * 0.14)} {F(y + L * 0.14)} {F(x - L)} {F(y)} Q{F(x - L * 0.14)} {F(y - L * 0.14)} {F(x)} {F(y - L)} Z" fill="{col}" opacity="{op}"/>')


def saco_dinero():
    w, h = 560, 640
    z = _pz("saco_dinero", w, h)
    sombra_suelo(z, 280, 612, 230, 20)
    g = z.rad((220, 330), 320, [(0, "#e8d0a0"), (0.55, "#c8a468"), (1, "#7a5a30")])
    z(f'<path d="M210 190 Q80 260 70 430 Q66 600 280 604 Q494 600 490 430 Q480 260 350 190 Z" fill="{g}"/>',
      '<path d="M210 190 Q170 120 190 70 Q240 110 280 80 Q320 110 370 70 Q390 120 350 190 Z" fill="#c8a468"/>',
      '<path d="M200 80 Q240 120 280 92 Q320 120 360 80" stroke="#8a6a3a" stroke-width="3" fill="none"/>')
    r = random.Random(3)
    for _ in range(140):
        x, y = r.uniform(100, 460), r.uniform(230, 590)
        if ((x - 280) / 200) ** 2 + ((y - 430) / 180) ** 2 > 1:
            continue
        z(f'<path d="M{F(x)} {F(y)} l{F(r.uniform(4, 10))} {F(r.uniform(-2, 2))}" stroke="#7a5a30" stroke-width="1.4" opacity="0.35"/>')
    z('<path d="M120 330 Q130 260 200 226" stroke="#fff4d8" stroke-width="14" opacity="0.4" fill="none" stroke-linecap="round"/>',
      f'<path d="M480 420 Q470 560 360 596" stroke="{z.rim}" stroke-width="7" opacity="0.5" fill="none"/>')
    # cuerda atada
    z('<path d="M196 196 Q280 222 364 196" stroke="#6a3a1a" stroke-width="16" fill="none" stroke-linecap="round"/>',
      '<path d="M200 192 Q280 214 360 192" stroke="#a86a3a" stroke-width="5" fill="none"/>',
      '<path d="M300 206 Q330 250 314 290 M300 206 Q350 230 372 270" stroke="#6a3a1a" stroke-width="9" fill="none" stroke-linecap="round"/>')
    # emblema: moneda grande estampada en el saco (sin símbolos de divisa)
    z('<circle cx="280" cy="420" r="92" fill="#5a3a1a" opacity="0.25"/>')
    gm = z.rad((256, 396), 110, [(0, "#fff0a8"), (0.5, "#e8b030"), (1, "#8a5a10")])
    z(f'<circle cx="280" cy="416" r="84" fill="{gm}"/>', '<circle cx="280" cy="416" r="64" fill="none" stroke="#9a6a10" stroke-width="7"/>')
    _destello(z, 280, 416, 40, "#fff6d0", 0.95)
    # monedas que asoman
    _moneda(z, 250, 140, 34, -10)
    _moneda(z, 312, 128, 30, 12)
    _moneda(z, 450, 596, 40, 4)
    _moneda(z, 110, 600, 34, -6)
    return _fin(z)


def _bombilla(n, encendida):
    w, h = 460, 620
    z = _pz(n, w, h, rim="#fff4c0" if encendida else "#cfe0ff")
    cx = 230
    vid = "M230 90 C110 90 70 190 90 260 C104 310 160 340 170 420 L290 420 C300 340 356 310 370 260 C390 190 350 90 230 90 Z"
    if encendida:
        gh = z.rad((cx, 250), 230, [(0, "#fff4b0", 0.85), (0.5, "#ffd23a", 0.35), (1, "#ffd23a", 0)])
        z(f'<circle cx="{cx}" cy="250" r="230" fill="{gh}"/>')
        for k in range(12):
            a = math.radians(k * 30 + 15)
            if math.sin(a) > 0.55:
                continue
            z(f'<path d="M{F(cx + math.cos(a) * 180)} {F(250 + math.sin(a) * 180)} L{F(cx + math.cos(a) * 222)} {F(250 + math.sin(a) * 222)}" '
              f'stroke="#ffcf3a" stroke-width="12" stroke-linecap="round"/>')
        gv = z.rad((200, 210), 190, [(0, "#ffffff"), (0.4, "#fff6c0"), (1, "#ffc83a")])
    else:
        gv = z.rad((190, 190), 220, [(0, "#ffffff", 0.9), (0.5, "#dfe6ee", 0.75), (1, "#8a96a6", 0.8)])
    z(f'<path d="{vid}" fill="{gv}"/>')
    # filamento
    fil = "#fff8e0" if encendida else "#7a6a5a"
    z(f'<path d="M200 420 L196 300 M260 420 L264 300" stroke="{"#e8c060" if encendida else "#8a8a8a"}" stroke-width="4"/>',
      f'<path d="M196 300 Q206 270 216 300 Q226 330 236 300 Q246 270 256 300 L264 300" stroke="{fil}" stroke-width="{6 if encendida else 4}" fill="none"/>')
    z('<path d="M130 190 Q140 130 210 112" stroke="#ffffff" stroke-width="16" opacity="0.7" fill="none" stroke-linecap="round"/>',
      f'<path d="M360 240 Q350 300 300 350" stroke="{z.rim}" stroke-width="7" opacity="0.6" fill="none" stroke-linecap="round"/>',
      f'<path d="{vid}" fill="none" stroke="{"#e8a020" if encendida else "#6a7686"}" stroke-width="3" opacity="0.6"/>')
    # casquillo
    gc = _lin(z, (166, 0), (294, 0), "#7a828c", "#e8eef4", "#9aa2ac", "#4a525c")
    for k in range(4):
        z(f'<rect x="{166 + k * 2}" y="{420 + k * 26}" width="{128 - k * 4}" height="24" rx="10" fill="{gc}"/>')
    z('<path d="M196 524 L264 524 L248 560 L212 560 Z" fill="#3a3f44"/><ellipse cx="230" cy="562" rx="16" ry="7" fill="#c89a3a"/>')
    return _fin(z)


def bombilla_a():
    return _bombilla("bombilla_a", False)


def bombilla_b():
    return _bombilla("bombilla_b", True)


def _cartel(n, abierto):
    w, h = 560, 520
    z = _pz(n, w, h)
    c0, c1, c2 = ("#6ad07a", "#2f9a4a", "#1a5a2a") if abierto else ("#ff6a5a", "#c8322a", "#6a1410")
    # clavo y cordel
    z('<circle cx="280" cy="40" r="14" fill="#5a626c"/><circle cx="276" cy="36" r="5" fill="#e0e6ec"/>',
      '<path d="M280 40 L90 200 M280 40 L470 200" stroke="#a8844a" stroke-width="6" stroke-linecap="round"/>',
      '<path d="M280 40 L90 200" stroke="#e8c890" stroke-width="2" opacity="0.6"/>')
    d = "M60 190 Q60 170 80 170 L480 170 Q500 170 500 190 L500 470 Q500 490 480 490 L80 490 Q60 490 60 470 Z"
    z(f'<path d="{d}" fill="#000" opacity="0.3" transform="translate(8 12)"/>')
    _extru(z, d, 12, c2, 0.5, 1)
    g = _lin(z, (60, 170), (500, 490), c0, c1, c2)
    z(f'<path d="{d}" fill="{g}"/>',
      '<rect x="82" y="192" width="396" height="276" rx="12" fill="none" stroke="#ffffff" stroke-width="6" opacity="0.8"/>',
      '<circle cx="90" cy="200" r="9" fill="#d8dce0"/><circle cx="470" cy="200" r="9" fill="#d8dce0"/>',
      '<path d="M70 182 L300 182" stroke="#ffffff" stroke-width="4" opacity="0.45" stroke-linecap="round"/>',
      f'<path d="M497 200 L497 470" stroke="{z.rim}" stroke-width="4" opacity="0.5"/>')
    if abierto:   # puerta abierta con luz saliendo
        z('<rect x="200" y="230" width="140" height="220" rx="6" fill="#ffffff"/>',
          '<rect x="214" y="244" width="112" height="206" fill="#ffe8a0"/>',
          '<path d="M214 244 L282 266 L282 470 L214 450 Z" fill="#1a5a2a"/>', '<path d="M214 244 L282 266 L282 470 L214 450 Z" fill="none" stroke="#ffffff" stroke-width="4"/>',
          '<circle cx="270" cy="370" r="6" fill="#ffffff"/>',
          '<path d="M326 450 L400 470 L140 470 L214 450 Z" fill="#ffe8a0" opacity="0.6"/>')
    else:         # candado
        z('<path d="M230 300 L230 262 Q230 218 280 218 Q330 218 330 262 L330 300" stroke="#ffffff" stroke-width="22" fill="none"/>',
          '<path d="M230 300 L230 262 Q230 218 280 218 Q330 218 330 262 L330 300" stroke="#f0d0d0" stroke-width="6" fill="none" opacity="0.6"/>',
          '<rect x="196" y="296" width="168" height="140" rx="20" fill="#ffffff"/>',
          '<rect x="196" y="410" width="168" height="26" rx="12" fill="#e8d8d8"/>',
          '<circle cx="280" cy="352" r="18" fill="#c8322a"/><path d="M272 360 L288 360 L284 396 L276 396 Z" fill="#c8322a"/>')
    return _fin(z)


def cartel_abierto():
    return _cartel("cartel_abierto", True)


def cartel_cerrado():
    return _cartel("cartel_cerrado", False)


def contrato_prestamo():
    w, h = 560, 740
    z = _pz("contrato_prestamo", w, h)
    d, caja = _hoja(z, w, h, -1.5)
    x0, y0, x1, y1 = caja
    z(f'<rect x="{x0 + 120}" y="{y0 + 40}" width="{x1 - x0 - 240}" height="18" rx="9" fill="#2a2a34" opacity="0.75"/>',
      f'<rect x="{x0 + 160}" y="{y0 + 70}" width="{x1 - x0 - 320}" height="10" rx="5" fill="#2a2a34" opacity="0.4"/>')
    r = random.Random(77)
    y = y0 + 120
    while y < y1 - 200:
        largo = x1 - 40 - (r.uniform(40, 160) if r.random() < 0.25 else 0)
        z(f'<rect x="{x0 + 40}" y="{y}" width="{F(largo - x0 - 40)}" height="7" rx="3.5" fill="#4a4a54" opacity="0.45"/>')
        y += 22 if r.random() < 0.8 else 40
    # línea de firma y firma garabateada
    z(f'<path d="M{x0 + 40} {y1 - 90} L{x0 + 260} {y1 - 90}" stroke="#4a4a54" stroke-width="2"/>',
      f'<path d="M{x0 + 50} {y1 - 100} C{x0 + 70} {y1 - 160} {x0 + 90} {y1 - 150} {x0 + 84} {y1 - 110} C{x0 + 80} {y1 - 80} {x0 + 120} {y1 - 150} '
      f'{x0 + 140} {y1 - 120} C{x0 + 150} {y1 - 100} {x0 + 170} {y1 - 140} {x0 + 190} {y1 - 116} C{x0 + 204} {y1 - 100} {x0 + 230} {y1 - 120} {x0 + 250} {y1 - 112}" '
      'stroke="#1f3a8a" stroke-width="4" fill="none" stroke-linecap="round"/>')
    # sello rojo
    cx, cy = x1 - 110, y1 - 120
    z(f'<g transform="rotate(-14 {cx} {cy})" opacity="0.85">',
      f'<circle cx="{cx}" cy="{cy}" r="70" fill="none" stroke="#c8222a" stroke-width="8"/>',
      f'<circle cx="{cx}" cy="{cy}" r="54" fill="none" stroke="#c8222a" stroke-width="3"/>',
      *[f'<circle cx="{F(cx + 62 * math.cos(math.radians(a)))}" cy="{F(cy + 62 * math.sin(math.radians(a)))}" r="2.6" fill="#c8222a"/>' for a in range(0, 360, 15)],
      f'<path d="M{cx} {cy - 32} L{cx + 9} {cy - 10} L{cx + 32} {cy - 10} L{cx + 14} {cy + 4} L{cx + 20} {cy + 28} L{cx} {cy + 14} L{cx - 20} {cy + 28} '
      f'L{cx - 14} {cy + 4} L{cx - 32} {cy - 10} L{cx - 9} {cy - 10} Z" fill="#c8222a"/>',
      '</g>')
    z('</g>')
    return _fin(z)


# ============================================================================ MÓVIL Y APPS
def movil_mano():
    """Mano (izquierda) sujetando un móvil; pantalla en blanco luminosa (rect 144,54 → 416,626)."""
    w, h = 560, 940
    z = _pz("movil_mano", w, h)
    P = PIEL4
    gpiel = _lin(z, (110, 0), (460, 0), P["l"], P["b"], P["s"])
    # palma y muñeca (detrás del móvil; se ven por debajo)
    z(f'<path d="M120 560 Q100 700 180 790 L200 940 L390 940 L400 820 Q462 740 452 600 L440 520 Z" fill="{gpiel}"/>',
      f'<path d="M232 860 Q300 880 372 850" stroke="{P["s"]}" stroke-width="3" fill="none" opacity="0.45"/>',
      f'<path d="M452 600 Q462 740 400 820" stroke="{z.rim}" stroke-width="5" fill="none" opacity="0.5"/>')
    z('<path d="M176 880 L404 880 L412 940 L168 940 Z" fill="#2f6fb0"/>', '<path d="M178 882 L402 882" stroke="#5f9fe0" stroke-width="6"/>',
      '<path d="M176 880 L404 880 L404 892 L176 892 Z" fill="#173a60" opacity="0.4"/>')
    # dedos detrás: asoman por el canto derecho
    for k, y in enumerate((300, 384, 466, 546)):
        L = 60 - k * 5
        gd = _lin(z, (0, y - 26), (0, y + 26), P["l"], P["b"], P["s"])
        z(f'<path d="M{410 - L} {y - 27} Q458 {y - 32} 466 {y} Q460 {y + 32} {410 - L} {y + 27} Z" fill="{gd}"/>',
          f'<path d="M455 {y - 14} Q462 {y} 455 {y + 14}" stroke="#f8d8d0" stroke-width="5" fill="none" opacity="0.8"/>',
          f'<path d="M{424 - L} {y + 25} Q440 {y + 26} 460 {y + 10}" stroke="{P["s"]}" stroke-width="2.5" fill="none" opacity="0.6"/>')
    # móvil
    gc = _lin(z, (130, 0), (430, 0), "#5a5e66", "#1e2026", "#16181c", "#4a4e56")
    z('<rect x="130" y="40" width="300" height="600" rx="42" fill="#000" opacity="0.3" transform="translate(10 14)"/>',
      f'<rect x="130" y="40" width="300" height="600" rx="42" fill="{gc}"/>',
      '<rect x="132" y="42" width="296" height="596" rx="40" fill="none" stroke="#8a8e96" stroke-width="2" opacity="0.6"/>')
    gp = z.rad((240, 240), 460, [(0, "#ffffff"), (0.7, "#f6f9ff"), (1, "#e6ecf6")])
    z(f'<rect x="144" y="54" width="272" height="572" rx="30" fill="{gp}"/>',
      '<rect x="144" y="54" width="272" height="572" rx="30" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.8"/>',
      '<rect x="248" y="66" width="64" height="16" rx="8" fill="#0a0b0e"/>')
    gs = _lin(z, (144, 54), (416, 626), (0, "#ffffff", 0.0), (0.5, "#ffffff", 0.0), (1, "#c8d8ff", 0.25))
    z(f'<rect x="144" y="54" width="272" height="572" rx="30" fill="{gs}"/>')
    # pulgar por delante: sube por el canto izquierdo y apoya la yema sobre el borde
    gpu = _lin(z, (100, 0), (220, 0), P["l"], P["b"], P["s"])
    z(f'<path d="M112 720 Q92 620 112 540 Q124 470 150 420 Q168 392 194 400 Q214 410 208 444 Q198 500 196 560 Q196 640 236 720 Z" fill="#000" opacity="0.18" transform="translate(6 8)"/>',
      f'<path d="M112 720 Q92 620 112 540 Q124 470 150 420 Q168 392 194 400 Q214 410 208 444 Q198 500 196 560 Q196 640 236 720 Z" fill="{gpu}"/>',
      f'<path d="M158 418 Q172 400 192 406 Q204 416 200 440 Q182 440 168 432 Z" fill="#f8dcd4"/>',
      f'<path d="M158 418 Q172 400 192 406 Q204 416 200 440 Q182 440 168 432 Z" fill="none" stroke="{P["s"]}" stroke-width="2" opacity="0.55"/>',
      f'<path d="M150 520 Q170 528 196 520" stroke="{P["s"]}" stroke-width="3" fill="none" opacity="0.55"/>',
      f'<path d="M122 470 Q108 540 116 620" stroke="#ffffff" stroke-width="7" fill="none" opacity="0.35" stroke-linecap="round"/>',
      f'<path d="M198 600 Q214 670 252 720" stroke="{P["s"]}" stroke-width="3" fill="none" opacity="0.5"/>')
    return _fin(z)


def _app(n, c0, c1, c2, glifo, vieja=False, rad=None):
    """Icono de app con volumen: cuerpo extruido, brillo, luz de borde y un glifo."""
    w, h = 440, 440
    z = _pz(n, w, h)
    rr = rad if rad is not None else (30 if vieja else 96)
    d = f"M40 {40 + rr} Q40 40 {40 + rr} 40 L{360 - rr} 40 Q360 40 360 {40 + rr} L360 {360 - rr} Q360 360 {360 - rr} 360 L{40 + rr} 360 Q40 360 40 {360 - rr} Z"
    z(f'<path d="{d}" fill="#000" opacity="0.3" transform="translate(14 22)"/>')
    _extru(z, d, 18, c2, 0.4, 1)
    g = _lin(z, (40, 40), (360, 360), c0, c1, c2)
    z(f'<path d="{d}" fill="{g}"/>')
    if vieja:
        z(f'<path d="M44 44 L356 44" stroke="#ffffff" stroke-width="6" opacity="0.7"/><path d="M44 44 L44 356" stroke="#ffffff" stroke-width="6" opacity="0.5"/>',
          f'<path d="M356 46 L356 356 L46 356" stroke="#000" stroke-width="6" opacity="0.25" fill="none"/>')
    else:
        gb = _lin(z, (0, 40), (0, 220), (0, "#ffffff", 0.35), (1, "#ffffff", 0))
        z(f'<path d="M{40 + rr} 46 L{360 - rr} 46 Q354 46 354 {40 + rr} L354 200 Q200 240 46 200 L46 {40 + rr} Q46 46 {40 + rr} 46 Z" fill="{gb}"/>',
          f'<path d="{d}" fill="none" stroke="{z.rim}" stroke-width="4" opacity="0.35"/>')
    z(glifo)
    return _fin(z)


def _lupa(cx, cy, s, col="#ffffff", som="#000", op_s=0.25, lente="#ffffff", lente_op=0.2):
    return (f'<g transform="translate({cx} {cy}) scale({s})">'
            f'<path d="M30 30 L96 96" stroke="{som}" stroke-width="34" stroke-linecap="round" opacity="{op_s}" transform="translate(6 8)"/>'
            f'<circle cx="0" cy="0" r="62" fill="none" stroke="{som}" stroke-width="26" opacity="{op_s}" transform="translate(6 8)"/>'
            f'<circle cx="0" cy="0" r="62" fill="{lente}" opacity="{lente_op}"/>'
            f'<circle cx="0" cy="0" r="62" fill="none" stroke="{col}" stroke-width="26"/>'
            f'<path d="M44 44 L96 96" stroke="{col}" stroke-width="34" stroke-linecap="round"/>'
            f'<path d="M-34 -22 Q-28 -40 -10 -44" stroke="#ffffff" stroke-width="10" opacity="0.7" fill="none" stroke-linecap="round"/>'
            '</g>')


def app_buscador():
    return _app("app_buscador", "#5ae0c8", "#2a9ad8", "#3a2a9a", _lupa(180, 176, 1.05))


def app_buscador_viejo_1():
    gl = _lupa(190, 186, 0.95, col="#5a5e66", som="#000", op_s=0.15, lente="#cfe0f0", lente_op=0.8)
    gl += '<rect x="70" y="300" width="260" height="24" fill="#8a8e96"/><rect x="72" y="302" width="80" height="20" fill="#5a6a8a"/>'
    return _app("app_buscador_viejo_1", "#e4e4e0", "#b8b8b4", "#6a6a68", gl, vieja=True)


def app_buscador_viejo_2():
    globo = ('<circle cx="170" cy="170" r="96" fill="#9aa4ae"/><circle cx="170" cy="170" r="96" fill="none" stroke="#5a626c" stroke-width="6"/>'
             '<ellipse cx="170" cy="170" rx="40" ry="96" fill="none" stroke="#5a626c" stroke-width="5"/>'
             '<path d="M74 170 L266 170 M90 120 L250 120 M90 220 L250 220" stroke="#5a626c" stroke-width="5"/>')
    return _app("app_buscador_viejo_2", "#c8c4bc", "#9a968e", "#5a5852",
                globo + _lupa(250, 250, 0.72, col="#3a3a3e", op_s=0.2, lente="#e8eef4", lente_op=0.6), vieja=True, rad=50)


def _siluetas(col, som, op=0.25):
    def una(x, y, s):
        return (f'<g transform="translate({x} {y}) scale({s})">'
                f'<circle cx="0" cy="-60" r="44" fill="{col}"/>'
                f'<path d="M-84 70 Q-84 -4 0 -6 Q84 -4 84 70 Z" fill="{col}"/></g>')
    return (f'<g opacity="{op}" transform="translate(6 8)"><g fill="{som}">{una(250, 200, 0.85).replace(col, som)}{una(160, 220, 1.0).replace(col, som)}</g></g>'
            f'<g opacity="0.85">{una(250, 200, 0.85)}</g>{una(160, 220, 1.0)}'
            '<path d="M130 140 Q140 124 160 120" stroke="#ffffff" stroke-width="7" opacity="0.6" fill="none" stroke-linecap="round" transform="translate(-6 0)"/>')


def app_red():
    return _app("app_red", "#7ac8ff", "#3a6ae0", "#22308a", _siluetas("#ffffff", "#000"))


def app_red_vieja():
    return _app("app_red_vieja", "#d8d8dc", "#a4a6ac", "#5e6066", _siluetas("#6a6c74", "#000", 0.15), vieja=True)


def app_historias():
    w, h = 1100, 260
    z = _pz("app_historias", w, h)
    aros = [("#ffb03a", "#ff3a7a"), ("#3ae0c0", "#3a7aff"), ("#c8ff3a", "#1aa86a"), ("#ff7a3a", "#a83aff"), ("#ffe03a", "#ff5a3a")]
    fondos = ["#ffe0c8", "#d8e8ff", "#e0f4d8", "#f0dcff", "#fff0c8"]
    pieles = [PIEL4, IP.PIEL2, IP.PIEL3, PIEL4, IP.PIEL2]
    pelos = ["#7a3a22", "#1e1612", "#1a120c", "#c89a5a", "#3a2618"]
    ropa = ["#e0a92e", "#2f6fb0", "#3a8a5e", "#7a2a3a", "#c8322a"]
    for i in range(5):
        cx, cy = 120 + i * 215, 125
        g = _lin(z, (cx - 100, cy + 100), (cx + 100, cy - 100), aros[i][0], aros[i][1])
        z(f'<circle cx="{cx + 6}" cy="{cy + 10}" r="104" fill="#000" opacity="0.25"/>',
          f'<circle cx="{cx}" cy="{cy}" r="104" fill="{g}"/>', f'<circle cx="{cx}" cy="{cy}" r="90" fill="#ffffff"/>')
        cl = z.clip(f"M{cx - 82} {cy} A82 82 0 1 0 {cx + 82} {cy} A82 82 0 1 0 {cx - 82} {cy} Z")
        P = pieles[i]
        z(f'<g clip-path="{cl}">', f'<rect x="{cx - 90}" y="{cy - 90}" width="180" height="180" fill="{fondos[i]}"/>',
          f'<path d="M{cx - 70} {cy + 100} Q{cx - 66} {cy + 34} {cx} {cy + 30} Q{cx + 66} {cy + 34} {cx + 70} {cy + 100} Z" fill="{ropa[i]}"/>',
          f'<rect x="{cx - 12}" y="{cy + 8}" width="24" height="30" fill="{P["s"]}"/>')
        # pelo de atrás
        if i in (0, 3):
            z(f'<path d="M{cx - 40} {cy - 20} Q{cx - 48} {cy + 40} {cx - 30} {cy + 50} L{cx + 30} {cy + 50} Q{cx + 48} {cy + 40} {cx + 40} {cy - 20} Z" fill="{pelos[i]}"/>')
        gpi = z.rad((cx - 12, cy - 30), 60, [(0, P["l"]), (0.7, P["b"]), (1, P["s"])])
        z(f'<ellipse cx="{cx}" cy="{cy - 14}" rx="36" ry="42" fill="{gpi}"/>',
          f'<ellipse cx="{cx - 37}" cy="{cy - 10}" rx="6" ry="10" fill="{P["b"]}"/><ellipse cx="{cx + 37}" cy="{cy - 10}" rx="6" ry="10" fill="{P["b"]}"/>',
          f'<path d="M{cx - 38} {cy - 22} Q{cx - 40} {cy - 62} {cx} {cy - 60} Q{cx + 40} {cy - 62} {cx + 38} {cy - 22} Q{cx + 20} {cy - 44} {cx - 6} {cy - 40} Q{cx - 26} {cy - 38} {cx - 38} {cy - 22} Z" fill="{pelos[i]}"/>',
          f'<ellipse cx="{cx - 13}" cy="{cy - 14}" rx="5" ry="6" fill="#ffffff"/><ellipse cx="{cx + 13}" cy="{cy - 14}" rx="5" ry="6" fill="#ffffff"/>',
          f'<circle cx="{cx - 12}" cy="{cy - 13}" r="3.6" fill="#2a1a10"/><circle cx="{cx + 14}" cy="{cy - 13}" r="3.6" fill="#2a1a10"/>',
          f'<circle cx="{cx - 13}" cy="{cy - 15}" r="1.2" fill="#ffffff"/><circle cx="{cx + 13}" cy="{cy - 15}" r="1.2" fill="#ffffff"/>',
          f'<path d="M{cx - 20} {cy - 26} q7 -4 14 0 M{cx + 6} {cy - 26} q7 -4 14 0" stroke="{pelos[i]}" stroke-width="3" fill="none" stroke-linecap="round"/>',
          f'<path d="M{cx - 2} {cy - 8} q-4 10 2 12" stroke="{P["s"]}" stroke-width="2.5" fill="none" opacity="0.7"/>',
          f'<path d="M{cx - 12} {cy + 8} Q{cx} {cy + 18} {cx + 12} {cy + 8}" stroke="#a8403a" stroke-width="3.5" fill="none" stroke-linecap="round"/>',
          '</g>',
          f'<path d="M{cx - 70} {cy - 50} A86 86 0 0 1 {cx - 20} {cy - 86}" stroke="#ffffff" stroke-width="6" opacity="0.55" fill="none" stroke-linecap="round"/>')
    return _fin(z)


def app_fantasma_generico():
    cam = ('<g transform="translate(6 8)" opacity="0.2"><rect x="96" y="140" width="208" height="150" rx="26" fill="#000"/></g>'
           '<path d="M150 140 L168 112 L232 112 L250 140 Z" fill="#2a2a2e"/>'
           '<rect x="96" y="140" width="208" height="150" rx="26" fill="#2a2a2e"/>'
           '<circle cx="200" cy="215" r="52" fill="#ffffff"/><circle cx="200" cy="215" r="38" fill="#2a2a2e"/>'
           '<circle cx="200" cy="215" r="24" fill="#4a6a9a"/><circle cx="190" cy="205" r="8" fill="#ffffff" opacity="0.8"/>'
           '<rect x="262" y="156" width="24" height="14" rx="4" fill="#ffffff" opacity="0.8"/>'
           '<path d="M104 160 Q110 146 126 144" stroke="#ffffff" stroke-width="5" opacity="0.4" fill="none" stroke-linecap="round"/>')
    return _app("app_fantasma_generico", "#fff27a", "#ffd21a", "#d89a00", cam)


# ============================================================================ ICONOS «MEJORA UNA SOLA COSA»
def _icono(n, d, c0, c1, c2, extra="", w=440, h=440, prof=26):
    z = _pz(n, w + 50, h + 60)
    z('<g transform="translate(10 6)">')
    z(f'<path d="{d}" fill="#000" opacity="0.28" transform="translate({prof * 0.6 + 8} {prof + 14})"/>')
    _extru(z, d, prof, c2, 0.4, 1, pasos=14)
    g = _lin(z, (0, 0), (w, h), c0, c1, mix(c1, c2, 0.5))
    z(f'<path d="{d}" fill="{g}"/>', f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.45"/>')
    z(extra, '</g>')
    return _fin(z)


def icono_rapido():
    d = "M250 20 L90 250 L200 250 L150 410 L340 160 L228 160 L290 20 Z"
    return _icono("icono_rapido", d, "#fff6a0", "#ffcf1a", "#b87a00",
                  '<path d="M246 40 L120 230" stroke="#ffffff" stroke-width="10" opacity="0.6" stroke-linecap="round"/>')


def icono_barato():
    d = "M60 70 L230 70 L390 230 L230 390 L60 220 Z"
    ext = ('<circle cx="118" cy="128" r="22" fill="#7a1a20"/><circle cx="118" cy="128" r="22" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.4"/>'
           '<path d="M118 128 Q60 60 30 30" stroke="#c8a46a" stroke-width="5" fill="none"/>'
           '<path d="M70 80 L220 80" stroke="#ffffff" stroke-width="8" opacity="0.5" stroke-linecap="round"/>'
           # flecha hacia abajo
           '<g transform="translate(6 8)" opacity="0.25"><path d="M250 150 L250 270 M206 230 L250 280 L294 230" stroke="#000" stroke-width="30" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
           '<path d="M250 150 L250 270 M206 230 L250 280 L294 230" stroke="#ffffff" stroke-width="30" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    return _icono("icono_barato", d, "#ff9a8a", "#e83a3a", "#7a1a20", ext)


def icono_cerca():
    d = "M220 410 C190 340 90 260 90 160 C90 80 150 26 220 26 C290 26 350 80 350 160 C350 260 250 340 220 410 Z"
    ext = ('<circle cx="220" cy="160" r="56" fill="#7a1a30"/><circle cx="220" cy="160" r="46" fill="#ffffff"/>'
           '<path d="M130 120 Q150 60 210 50" stroke="#ffffff" stroke-width="12" opacity="0.55" fill="none" stroke-linecap="round"/>')
    return _icono("icono_cerca", d, "#ff8aa8", "#e8324a", "#7a1a30", ext)


def icono_bonito():
    pts = []
    for k in range(10):
        a = math.radians(-90 + k * 36)
        rr = 190 if k % 2 == 0 else 84
        pts.append(f"{F(215 + rr * math.cos(a))} {F(220 + rr * math.sin(a))}")
    d = "M" + " L".join(pts) + " Z"
    z = _pz("icono_bonito", 470, 480)
    gh = z.rad((215, 220), 200, [(0, "#fff6b0", 0.6), (0.6, "#fff6b0", 0.2), (1, "#fff6b0", 0)])
    z(f'<circle cx="215" cy="220" r="220" fill="{gh}"/>')
    z(f'<path d="{d}" fill="#000" opacity="0.25" transform="translate(22 36)"/>')
    _extru(z, d, 24, "#b87a00", 0.4, 1, pasos=14)
    g = _lin(z, (0, 0), (440, 440), "#fff6a0", "#ffcf1a", "#e8a010")
    z(f'<path d="{d}" fill="{g}"/>', f'<path d="{d}" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.5"/>',
      '<path d="M215 70 L240 170" stroke="#ffffff" stroke-width="10" opacity="0.6" stroke-linecap="round"/>')
    _destello(z, 340, 90, 34)
    _destello(z, 90, 340, 22)
    _destello(z, 380, 300, 16)
    return _fin(z)


def icono_mas():
    d = "M160 40 L280 40 L280 160 L400 160 L400 280 L280 280 L280 400 L160 400 L160 280 L40 280 L40 160 L160 160 Z"
    return _icono("icono_mas", d, "#8af0a0", "#2fb85a", "#145a2a",
                  '<path d="M170 52 L170 168 L52 168" stroke="#ffffff" stroke-width="8" opacity="0.55" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
                  w=460, h=460)


def icono_igual():
    d = "M40 110 L400 110 L400 200 L40 200 Z M40 250 L400 250 L400 340 L40 340 Z"
    return _icono("icono_igual", d, "#a8d8ff", "#3a8ae0", "#1a3a7a",
                  '<path d="M54 122 L380 122 M54 262 L380 262" stroke="#ffffff" stroke-width="8" opacity="0.55" stroke-linecap="round"/>',
                  w=460, h=420)


# ============================================================================ VIDA DIARIA
def balon_futbol():
    w, h = 480, 500
    z = _pz("balon_futbol", w, h)
    cx, cy, R = 236, 236, 210
    sombra_suelo(z, cx, 474, 170, 18)
    gb = z.rad((cx - 70, cy - 80), R * 1.5, [(0, "#ffffff"), (0.55, "#eef0f4"), (1, "#8a929e")])
    z(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{gb}"/>')
    cl = z.clip(f"M{cx - R} {cy} A{R} {R} 0 1 0 {cx + R} {cy} A{R} {R} 0 1 0 {cx - R} {cy} Z")

    def pent(px, py, s, rot):
        return "M" + " L".join(f"{F(px + s * math.cos(math.radians(rot + k * 72)))} {F(py + s * math.sin(math.radians(rot + k * 72)))}" for k in range(5)) + " Z"
    b = [f'<g clip-path="{cl}">']
    b.append(f'<path d="{pent(cx, cy, 62, -90)}" fill="#1e2026"/>')
    for k in range(5):
        a = math.radians(-90 + 36 + k * 72)
        px, py = cx + math.cos(a) * 172, cy + math.sin(a) * 172
        b.append(f'<path d="{pent(px, py, 54, math.degrees(a) + 180 + 36)}" fill="#1e2026" transform="translate({F(px)} {F(py)}) scale(0.8 1) translate({F(-px)} {F(-py)})"/>')
        a2 = math.radians(-90 + k * 72)
        b.append(f'<path d="M{F(cx + math.cos(a2) * 62)} {F(cy + math.sin(a2) * 62)} L{F(cx + math.cos(a2) * 128)} {F(cy + math.sin(a2) * 128)}" stroke="#3a3f48" stroke-width="3"/>')
        a3 = math.radians(-90 + 36 + k * 72)
        for s in (-1, 1):
            a4 = a3 + s * math.radians(22)
            b.append(f'<path d="M{F(cx + math.cos(a2 + s * 0) * 128)} {F(cy + math.sin(a2) * 128)} L{F(cx + math.cos(a4) * 140)} {F(cy + math.sin(a4) * 140)}" stroke="#3a3f48" stroke-width="3" opacity="0"/>')
    for k in range(5):
        a2 = math.radians(-90 + k * 72)
        b.append(f'<path d="M{F(cx + math.cos(a2) * 128)} {F(cy + math.sin(a2) * 128)} L{F(cx + math.cos(a2 - 0.38) * 150)} {F(cy + math.sin(a2 - 0.38) * 150)} '
                 f'M{F(cx + math.cos(a2) * 128)} {F(cy + math.sin(a2) * 128)} L{F(cx + math.cos(a2 + 0.38) * 150)} {F(cy + math.sin(a2 + 0.38) * 150)} '
                 f'M{F(cx + math.cos(a2) * 128)} {F(cy + math.sin(a2) * 128)} L{F(cx + math.cos(a2) * 220)} {F(cy + math.sin(a2) * 220)}" stroke="#3a3f48" stroke-width="3" fill="none"/>')
    gs = z.rad((cx - 70, cy - 80), R * 1.5, [(0, "#000", 0), (0.6, "#000", 0.05), (1, "#000", 0.35)])
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{gs}"/>')
    b.append('</g>')
    z("".join(b))
    z(f'<path d="M{cx - 150} {cy - 60} A170 170 0 0 1 {cx - 50} {cy - 166}" stroke="#ffffff" stroke-width="18" opacity="0.6" fill="none" stroke-linecap="round"/>',
      f'<path d="M{cx + 196} {cy + 40} A200 200 0 0 1 {cx + 60} {cy + 198}" stroke="{z.rim}" stroke-width="8" opacity="0.55" fill="none" stroke-linecap="round"/>')
    return _fin(z)


def guitarra():
    w, h = 460, 1060
    z = _pz("guitarra", w, h)
    cx = 230
    sombra_suelo(z, cx, 1040, 170, 14)
    cuerpo = ("M230 500 C160 500 104 520 100 600 C96 660 140 690 132 730 C122 780 34 800 34 900 C34 990 130 1032 230 1032 "
              "C330 1032 426 990 426 900 C426 800 338 780 328 730 C320 690 364 660 360 600 C356 520 300 500 230 500 Z")
    z(f'<path d="{cuerpo}" fill="#000" opacity="0.3" transform="translate(10 12)"/>',
      f'<path d="{cuerpo}" fill="#5a2e14"/>')
    g = z.rad((170, 760), 460, [(0, "#f4c27a"), (0.5, "#d0883a"), (0.85, "#8a4a1a"), (1, "#4a2008")])
    z(f'<path d="{cuerpo}" fill="{g}" transform="translate(230 766) scale(0.965 0.975) translate(-230 -766)"/>',
      f'<path d="{cuerpo}" fill="none" stroke="#f4e0b8" stroke-width="3" opacity="0.55" transform="translate(230 766) scale(0.955 0.965) translate(-230 -766)"/>')
    # boca, roseta, brillos y puente
    z('<circle cx="230" cy="700" r="66" fill="#e8d8b0" opacity="0.55"/><circle cx="230" cy="700" r="56" fill="#1a0e06"/>',
      '<circle cx="230" cy="700" r="62" fill="none" stroke="#4a2a14" stroke-width="5"/>',
      '<path d="M76 850 Q70 950 150 1000" stroke="#fff0c8" stroke-width="18" opacity="0.35" fill="none" stroke-linecap="round"/>',
      '<path d="M120 590 Q124 540 180 522" stroke="#fff0c8" stroke-width="10" opacity="0.4" fill="none" stroke-linecap="round"/>',
      f'<path d="M412 860 Q420 980 300 1020" stroke="{z.rim}" stroke-width="6" opacity="0.5" fill="none"/>',
      '<path d="M300 760 Q350 750 352 706 Q350 676 318 668 Q306 720 300 760 Z" fill="#3a1a0a" opacity="0.7"/>',
      '<path d="M150 896 L310 896 L302 924 L158 924 Z" fill="#2a160a"/><rect x="176" y="888" width="108" height="9" rx="3" fill="#f4ead6"/>')
    # mástil y clavijero
    gm = _lin(z, (206, 0), (254, 0), "#7a4a24", "#4a2a12", "#2a1608")
    z(f'<rect x="206" y="110" width="48" height="530" fill="{gm}"/>')
    y, paso = 132, 34
    k = 0
    while y < 600:
        z(f'<path d="M206 {F(y)} L254 {F(y)}" stroke="#d8d8d0" stroke-width="2.5"/>')
        if k in (2, 4, 6, 8):
            z(f'<circle cx="230" cy="{F(y + paso / 2 - 1)}" r="4" fill="#f4ead6"/>')
        y += paso
        paso *= 0.955
        k += 1
    z('<path d="M196 20 L264 20 L258 120 L202 120 Z" fill="#3a1a0a"/>', '<path d="M200 22 L260 22" stroke="#8a5a32" stroke-width="3"/>',
      '<rect x="204" y="108" width="52" height="8" fill="#f4ead6"/>')
    for k in range(3):
        y = 40 + k * 28
        z(f'<rect x="176" y="{y - 6}" width="26" height="14" rx="5" fill="#d8b040"/><rect x="258" y="{y - 6}" width="26" height="14" rx="5" fill="#d8b040"/>',
          f'<circle cx="218" cy="{y}" r="4" fill="#c8c8c0"/><circle cx="242" cy="{y}" r="4" fill="#c8c8c0"/>')
    for k in range(6):
        x = 214 + k * 6.4
        z(f'<path d="M{F(x)} 112 L{F(x - 10 + k * 4)} 892" stroke="#f0ece0" stroke-width="{1.2 + (5 - k) * 0.25:.2f}" opacity="0.9"/>')
    return _fin(z)


def libro_recetas():
    w, h = 900, 560
    z = _pz("libro_recetas", w, h)
    sombra_suelo(z, 450, 530, 400, 24)
    # tapas
    z('<path d="M40 110 Q240 70 450 120 Q660 70 860 110 L870 500 Q660 470 450 520 Q240 470 30 500 Z" fill="#7a2a3a"/>',
      '<path d="M30 500 Q240 470 450 520 Q660 470 870 500 L870 512 Q660 484 450 532 Q240 484 30 512 Z" fill="#4a1420"/>')
    # páginas (lomos)
    for k in range(5):
        z(f'<path d="M{56 + k * 2} {104 - k * 2} Q245 {64 - k * 2} 450 {114 - k * 2} L450 {506 - k * 2} Q245 {460 - k * 2} {50 + k * 2} {488 - k * 2} Z" fill="{"#ece4d0" if k % 2 else "#d8ceb6"}"/>',
          f'<path d="M{844 - k * 2} {104 - k * 2} Q655 {64 - k * 2} 450 {114 - k * 2} L450 {506 - k * 2} Q655 {460 - k * 2} {850 - k * 2} {488 - k * 2} Z" fill="{"#ece4d0" if k % 2 else "#d8ceb6"}"/>')
    gl = _lin(z, (60, 0), (450, 0), "#fffaf0", "#f6efe0", "#d8ceb6")
    gr = _lin(z, (450, 0), (840, 0), "#e0d6be", "#f6efe0", "#fffaf0")
    z(f'<path d="M66 96 Q250 56 450 104 L450 496 Q250 450 60 480 Z" fill="{gl}"/>',
      f'<path d="M834 96 Q650 56 450 104 L450 496 Q650 450 840 480 Z" fill="{gr}"/>',
      '<path d="M450 104 L450 496" stroke="#b8ae98" stroke-width="3"/>',
      '<path d="M420 104 Q440 110 450 104 L450 496 Q440 490 420 492 Z" fill="#000" opacity="0.08"/>',
      '<path d="M480 104 Q460 110 450 104 L450 496 Q460 490 480 492 Z" fill="#000" opacity="0.08"/>')
    # izquierda: ingredientes dibujados
    z('<circle cx="150" cy="190" r="40" fill="#e83a2a"/><path d="M134 156 l16 8 l16 -8 l-8 12 z" fill="#3a8a3a"/><circle cx="138" cy="178" r="10" fill="#ffffff" opacity="0.5"/>',
      '<path d="M250 150 L300 250 L240 170 Z" fill="#f08a1a"/><path d="M250 150 Q240 130 230 138 M252 150 Q262 128 270 138" stroke="#3a8a3a" stroke-width="5" fill="none"/>',
      '<path d="M256 170 l8 -4 M266 196 l8 -4 M276 220 l8 -4" stroke="#b85a10" stroke-width="3"/>',
      '<ellipse cx="350" cy="196" rx="34" ry="44" fill="#fff8ea" stroke="#d8c8a8" stroke-width="3"/><ellipse cx="340" cy="182" rx="10" ry="14" fill="#ffffff"/>',
      '<path d="M120 330 Q150 270 190 330 Q150 360 120 330 Z" fill="#c8a0d0" stroke="#7a4a8a" stroke-width="3"/><path d="M155 286 l0 -20" stroke="#3a8a3a" stroke-width="4"/>',
      '<path d="M240 300 Q290 270 340 300 L330 350 Q290 370 250 350 Z" fill="#f4d06a" stroke="#c89a2a" stroke-width="3"/>',
      '<path d="M256 318 Q290 304 324 318" stroke="#ffffff" stroke-width="4" opacity="0.6" fill="none"/>')
    r = random.Random(4)
    for k in range(3):
        y = 400 + k * 24
        z(f'<path d="{_garabato(r, 100, 380 - k * 40, y, 1.6, 9)}" stroke="#6a5a4a" stroke-width="3" fill="none" opacity="0.6" stroke-linecap="round"/>')
    # derecha: plato con olla dibujada y pasos (renglones)
    z('<ellipse cx="640" cy="200" rx="110" ry="44" fill="#ffffff" stroke="#c8beaa" stroke-width="3"/>',
      '<ellipse cx="640" cy="196" rx="76" ry="28" fill="#e8783a"/>',
      '<circle cx="616" cy="190" r="10" fill="#c83a2a"/><circle cx="650" cy="186" r="8" fill="#3a8a3a"/><circle cx="672" cy="200" r="9" fill="#f4d06a"/>',
      '<path d="M606 150 q-8 -20 4 -34 M640 146 q-8 -20 4 -34 M674 150 q-8 -20 4 -34" stroke="#b8ae98" stroke-width="4" fill="none" stroke-linecap="round"/>')
    for k in range(6):
        y = 290 + k * 30
        z(f'<circle cx="530" cy="{y}" r="7" fill="#7a2a3a" opacity="0.7"/>',
          f'<path d="{_garabato(r, 550, 790 - r.uniform(0, 100), y, 1.6, 9)}" stroke="#6a5a4a" stroke-width="3" fill="none" opacity="0.6" stroke-linecap="round"/>')
    # cinta marcapáginas
    z('<path d="M470 104 L490 104 L490 548 L480 536 L470 548 Z" fill="#e0a92e"/>')
    return _fin(z)


def olla():
    w, h = 640, 560
    z = _pz("olla", w, h)
    sombra_suelo(z, 320, 532, 250, 22)
    # asas
    z('<path d="M90 280 Q30 280 30 310 Q30 340 90 340" stroke="#2a2a2e" stroke-width="22" fill="none"/>',
      '<path d="M550 280 Q610 280 610 310 Q610 340 550 340" stroke="#2a2a2e" stroke-width="22" fill="none"/>')
    g = _lin(z, (90, 0), (550, 0), "#6a727c", "#e8eef4", "#b8c0c8", "#8a929c", "#3a424c")
    z(f'<path d="M90 240 L550 240 L540 480 Q540 520 320 524 Q100 520 100 480 Z" fill="{g}"/>',
      '<path d="M140 270 L150 470" stroke="#ffffff" stroke-width="14" opacity="0.55" stroke-linecap="round"/>',
      f'<path d="M538 260 L530 480" stroke="{z.rim}" stroke-width="6" opacity="0.5"/>',
      '<ellipse cx="320" cy="240" rx="230" ry="36" fill="#9aa2ac"/>')
    # tapa
    gt = z.rad((260, 180), 300, [(0, "#ffffff"), (0.4, "#d0d8e0"), (1, "#5a626c")])
    z(f'<path d="M100 236 Q120 150 320 140 Q520 150 540 236 Q320 262 100 236 Z" fill="{gt}"/>',
      '<path d="M150 210 Q190 168 290 158" stroke="#ffffff" stroke-width="8" opacity="0.7" fill="none" stroke-linecap="round"/>',
      '<path d="M280 130 Q280 104 320 104 Q360 104 360 130 Z" fill="#2a2a2e"/><rect x="300" y="126" width="40" height="18" fill="#2a2a2e"/>',
      '<path d="M290 122 Q296 110 316 108" stroke="#8a8e96" stroke-width="3" fill="none"/>')
    for x in (230, 320, 410):
        z(f'<path d="M{x} 96 C{x - 24} 70 {x + 24} 44 {x} 16" stroke="#ffffff" stroke-width="12" opacity="0.3" fill="none" stroke-linecap="round" filter="url(#blur8)"/>',
          f'<path d="M{x} 96 C{x - 24} 70 {x + 24} 44 {x} 16" stroke="#ffffff" stroke-width="4" opacity="0.5" fill="none" stroke-linecap="round"/>')
    return _fin(z)


# ============================================================================ FOCOS
def _foco(n, col, borde):
    """Cono de luz de escenario de arriba abajo (ancho 120 arriba, 700 abajo, alto 1500) con su mancha en el suelo."""
    w, h = 900, 1580
    z = Lz(n, w, h)
    z.defs.append('<filter id="fcblur" x="-30%" y="-5%" width="160%" height="110%"><feGaussianBlur stdDeviation="22"/></filter>'
                  '<filter id="fcblur2" x="-30%" y="-5%" width="160%" height="110%"><feGaussianBlur stdDeviation="10"/></filter>')
    cx, base = 450, 1500
    # mancha de luz en el suelo
    gs = z.rad((0, 0), 420, [(0, col, 0.95), (0.45, col, 0.6), (0.8, col, 0.2), (1, col, 0)])
    z(f'<g transform="translate({cx} {base}) scale(1 0.17)"><circle r="420" fill="{gs}"/></g>')
    gs2 = z.rad((0, 0), 300, [(0, "#ffffff", 0.7), (1, "#ffffff", 0)])
    z(f'<g transform="translate({cx} {base}) scale(1 0.15)"><circle r="300" fill="{gs2}"/></g>')
    # cono: degradado vertical que se desvanece, bordes suaves por desenfoque
    gv = _lin(z, (0, 0), (0, base), (0, col, 0.9), (0.3, col, 0.55), (0.75, col, 0.3), (1, col, 0.18))
    z(f'<path d="M{cx - 60} -40 L{cx + 60} -40 L{cx + 350} {base} Q{cx} {base + 50} {cx - 350} {base} Z" fill="{gv}" filter="url(#fcblur)"/>')
    gi = _lin(z, (0, 0), (0, base), (0, borde, 0.7), (0.5, borde, 0.25), (1, borde, 0.1))
    z(f'<path d="M{cx - 30} -20 L{cx + 30} -20 L{cx + 170} {base} L{cx - 170} {base} Z" fill="{gi}" filter="url(#fcblur2)" opacity="0.6"/>')
    r = random.Random(len(n))
    for _ in range(70):
        y = r.uniform(60, base - 40)
        half = 60 + (350 - 60) * y / base
        x = cx + r.uniform(-half * 0.8, half * 0.8)
        z(f'<circle cx="{F(x)}" cy="{F(y)}" r="{F(r.uniform(1, 3))}" fill="#ffffff" opacity="{F(r.uniform(0.15, 0.5))}"/>')
    gt = z.rad((0, 0), 120, [(0, "#ffffff", 0.9), (1, col, 0)])
    z(f'<g transform="translate({cx} 0) scale(1 0.5)"><circle r="120" fill="{gt}"/></g>')
    return _fin(z, textura=False)


def foco_luz():
    return _foco("foco_luz", "#fff0d2", "#ffffff")


def foco_luz_frio():
    return _foco("foco_luz_frio", "#dbe8ff", "#ffffff")


# ============================================================================
PIEZAS = [cafeteria_marta, cafeteria_marta_cerrada, persiana, hamburgueseria_lucas, hamburgueseria_vacia, cafeteria_nueva,
          pupitre, pupitre_doble, examen, examen_bien, hoja_dibujo, timbre_a, timbre_b, mochila_cole,
          hamburguesa, bolsa_comida, taza_cafe_latte, reloj_pared, reloj_arena_grande, hucha, hucha_rota, billete, monedas,
          saco_dinero, bombilla_a, bombilla_b, cartel_abierto, cartel_cerrado, contrato_prestamo,
          movil_mano, app_buscador, app_buscador_viejo_1, app_buscador_viejo_2, app_red, app_red_vieja, app_historias,
          app_fantasma_generico, icono_rapido, icono_barato, icono_cerca, icono_bonito, icono_mas, icono_igual,
          balon_futbol, guitarra, libro_recetas, olla, foco_luz, foco_luz_frio]


def generar(dirsvg):
    os.makedirs(dirsvg, exist_ok=True)
    ilus.OUT = dirsvg
    NOMBRES.clear()
    for f in PIEZAS:
        f()
    return list(NOMBRES)


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
