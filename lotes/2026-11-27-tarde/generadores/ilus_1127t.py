"""Ilustraciones del lote 2026-11-27-tarde (Agente 20:00 (Jorge)), con el ESTILO DEL VÍDEO LARGO de la cueva
(DECISIONS 2026-11-26, Jorge). Reutiliza todo el arte del vídeo largo y de los lotes 2026-11-25/26-tarde
(`ilus_1126t.generar`) y añade solo las piezas nuevas, con los mismos ayudantes (Lz, mat, sombra_suelo, Lienzo):
01 anochece dos veces en el Burj Khalifa · 02 la capa de ozono mide tres milímetros · 03 la piel de gallina.
Uso: python3 ilus_1127t.py DIR_SVG"""
import importlib.util, math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
LARGO = os.path.join(RAIZ, "lotes", "largo-cueva-500-dias", "generadores")
sys.path.insert(0, RAIZ)
sys.path.insert(0, LARGO)
from motor.biblioteca import ilus  # noqa: E402
import ilus_personajes as IP  # noqa: E402
import ilus_escenarios as IE  # noqa: E402
from ilus_personajes import Lz, busto, _pj, mat, F, sombra_suelo, PIEL2, PIEL3, PIEL4, mix  # noqa: E402

_spec = importlib.util.spec_from_file_location("ilus_1126t", os.path.join(RAIZ, "lotes", "2026-11-26-tarde", "generadores", "ilus_1126t.py"))
T26 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(T26)
T25 = T26.T25

ATARDECER = dict(luz=(0.8, -0.5), rim="#ffb060")
SALA = dict(luz=(-0.6, -0.8), rim="#fff1d8")
FRIO = dict(luz=(-0.6, -0.8), rim="#bfe4ff")

MIRADOR = _pj(nombre="mirador", peinado="corto", pelo="#20160e", top=mat("#e8e2d6", "#ffffff", "#9a9284"), prenda="camiseta", manga="larga",
              pant=mat("#3a3f4a"), calzado="zapato", bota=mat("#3a2a1e"), edad=32, piel=PIEL3)
OYENTE = _pj(nombre="oyente", fem=True, peinado="melena", pelo="#2a1a10", top=mat("#2a8a7a", "#5ac0b0", "#124a40"), prenda="chaqueta",
             pant=mat("#2e3440"), calzado="zapato", bota=mat("#2a2a2e"), edad=27, piel=PIEL2)
INVESTIGADORA = _pj(nombre="invest", fem=True, peinado="coleta", pelo="#141010", top=mat("#f4f6fa", "#ffffff", "#a8b0bc"), prenda="bata",
                    pant=mat("#3a4a6a"), calzado="zapato", bota=mat("#2a2a2e"), edad=40, piel=PIEL4)

NOMBRES = []


def _a(n):
    NOMBRES.append(n)
    return n


def _rnd(sem):
    return random.Random(sem)


# =========================================================================== 01 · Burj Khalifa
def torre(n="torre", w=480, h=1900, noche=0.0):
    """Rascacielos-aguja de escalones en espiral (planta en Y), cristal azul plateado con la cara de poniente encendida.
    `noche` 0..1 oscurece la base (abajo ya ha anochecido, arriba sigue el sol)."""
    z = Lz(n, w, h, **ATARDECER)
    cx = w / 2
    base = h - 20
    alto = base - 40            # altura total hasta la punta de la aguja
    # perfil: ancho que se estrecha poco a poco; retranqueos escalonados que se alternan izquierda/derecha
    def ancho(y):               # semiancho del núcleo a una altura y (0 = suelo, 1 = punta)
        return 26 + 128 * (1 - y) ** 1.8
    g_sombra = z.lin((0, 0), (w, 0), [(0, "#1e2a46"), (0.4, "#4a6290"), (0.5, "#7a96c4"), (1, "#3a4a70")])
    g_luz = z.lin((0, 0), (w, 0), [(0, "#4a3a58"), (0.45, "#b88a86"), (0.56, "#ffd2a0"), (0.75, "#ffb070"), (1, "#e07a48")])
    Y = lambda f: base - f * alto
    # alas: (lado, fracción de altura donde acaba, desplazamiento extra hacia fuera)
    alas = [(-1, 0.09, 40), (1, 0.15, 36), (-1, 0.22, 32), (1, 0.29, 28), (-1, 0.36, 24), (1, 0.43, 20), (-1, 0.50, 16), (1, 0.57, 12), (-1, 0.63, 9), (1, 0.68, 6)]
    silu = []
    for lado, f_top, extra in alas:
        y_top = Y(f_top)
        a_out = ancho(f_top) + extra
        a_in = ancho(f_top) * 0.2
        xo = cx + lado * a_out
        xi = cx + lado * a_in
        # cara del ala: de la base al retranqueo, con el canto superior ligeramente inclinado
        silu.append(f"M{F(xi)} {F(base)} L{F(xo + lado * extra * 0.15)} {F(base)} L{F(xo)} {F(y_top + 10)} L{F(xi)} {F(y_top - 6)} Z")
        z(f'<path d="M{F(xi)} {F(base)} L{F(xo + lado * extra * 0.15)} {F(base)} L{F(xo)} {F(y_top + 10)} L{F(xi)} {F(y_top - 6)} Z" '
          f'fill="{g_luz if lado > 0 else g_sombra}" opacity="0.97"/>',
          f'<path d="M{F(xo)} {F(y_top + 10)} L{F(xi)} {F(y_top - 6)}" stroke="#fff0d8" stroke-width="3" opacity="0.7"/>')
    # núcleo central continuo hasta la base de la aguja
    f_n = 0.74
    pts_l = [(cx - ancho(f), Y(f)) for f in [k / 40 * f_n for k in range(41)]]
    pts_r = [(cx + ancho(f), Y(f)) for f in [k / 40 * f_n for k in range(40, -1, -1)]]
    d = "M" + " L".join(f"{F(x)} {F(y)}" for x, y in pts_l + pts_r) + " Z"
    silu.append(d)
    z(f'<path d="{d}" fill="{z.lin((0, 0), (w, 0), [(0, "#2a3656"), (0.42, "#8a9cc0"), (0.5, "#e8eef8"), (0.6, "#ffcf9a"), (1, "#c87a50")])}"/>')
    # líneas verticales del cristal (montantes), siguiendo el estrechamiento
    for k in range(-6, 7):
        t = k / 6
        x0, y0 = cx + t * ancho(0) * 0.92, base
        x1, y1 = cx + t * ancho(f_n) * 0.9, Y(f_n)
        z(f'<path d="M{F(x0)} {F(y0)} L{F(x1)} {F(y1)}" stroke="#ffffff" stroke-width="2" opacity="{0.10 + 0.12 * (1 - abs(t)):.2f}"/>')
    # reflejo largo del sol en la cara derecha
    z(f'<path d="M{F(cx + ancho(0) * 0.35)} {F(base)} L{F(cx + ancho(f_n) * 0.3)} {F(Y(f_n))}" stroke="#fff4dc" stroke-width="10" opacity="0.35"/>')
    # aguja
    ya = Y(f_n)
    z(f'<path d="M{F(cx - ancho(f_n) * 0.55)} {F(ya)} L{F(cx - 2)} {F(base - alto)} L{F(cx + 2)} {F(base - alto)} L{F(cx + ancho(f_n) * 0.55)} {F(ya)} Z" '
      f'fill="{z.lin((cx - 40, 0), (cx + 40, 0), [(0, "#6a7aa0"), (0.5, "#f4f6fa"), (1, "#ffb880")])}"/>',
      f'<circle cx="{F(cx)}" cy="{F(base - alto + 6)}" r="6" fill="#ff5a4a"/><circle cx="{F(cx)}" cy="{F(base - alto + 6)}" r="16" fill="#ff5a4a" opacity="0.3"/>')
    # podio en la base
    z(f'<path d="M{F(cx - 230)} {F(base)} L{F(cx - 200)} {F(base - 40)} L{F(cx + 200)} {F(base - 40)} L{F(cx + 230)} {F(base)} Z" fill="#2a2436"/>',
      f'<path d="M{F(cx - 200)} {F(base - 40)} L{F(cx + 200)} {F(base - 40)}" stroke="#ffd8a0" stroke-width="3" opacity="0.6"/>')
    if noche > 0:
        g = z.lin((0, h * 0.35), (0, h), [(0, "#0a0e22", 0), (0.5, "#0a0e22", noche * 0.55), (1, "#0a0e22", noche * 0.85)])
        for dd in silu:
            z(f'<path d="{dd}" fill="{g}"/>')
        # ventanas encendidas abajo
        r = _rnd(5)
        for _ in range(160):
            yy = r.uniform(h * 0.55, base - 10)
            frac = (base - yy) / (h * 0.45)
            half = 140 - frac * 90
            xx = cx + r.uniform(-half, half) * 0.95
            z(f'<rect x="{F(xx)}" y="{F(yy)}" width="5" height="3" fill="#ffd890" opacity="{r.uniform(0.4, 0.9) * noche:.2f}"/>')
    z.guardar()
    return _a(n)


def sol_poniente(n="sol_poniente"):
    """Disco de sol de atardecer con halo amplio."""
    w = h = 700
    z = Lz(n, w, h, **ATARDECER)
    c = (350, 350)
    z(f'<circle cx="350" cy="350" r="340" fill="{z.rad(c, 340, [(0, "#ffd080", 0.75), (0.35, "#ff9a40", 0.35), (1, "#ff6a20", 0)])}"/>',
      f'<circle cx="350" cy="350" r="150" fill="{z.rad((320, 320), 170, [(0, "#fffbe8"), (0.5, "#ffe08a"), (0.85, "#ffb040"), (1, "#ff8a20")])}"/>')
    z.guardar(textura=False)
    return _a(n)


def skyline(n="skyline_dubai", w=1080, h=760, noche=False):
    """Franja de primer término: ciudad baja y arena, transparente arriba (para que el sol se esconda detrás)."""
    z = Lz(n, w, h, **ATARDECER)
    r = _rnd(77)
    yb = 300
    # edificios lejanos
    x = -20
    while x < w + 20:
        bw = r.uniform(40, 110)
        bh = r.uniform(40, 200)
        c = "#2a1e30" if not noche else "#141628"
        z(f'<rect x="{F(x)}" y="{F(yb - bh)}" width="{F(bw)}" height="{F(bh + 10)}" fill="{c}"/>')
        for k in range(int(bh / 22)):
            if r.random() < (0.35 if not noche else 0.7):
                z(f'<rect x="{F(x + r.uniform(6, bw - 14))}" y="{F(yb - bh + 10 + k * 22)}" width="7" height="5" fill="#ffd28a" opacity="0.8"/>')
        x += bw + r.uniform(2, 20)
    # bruma cálida sobre la ciudad
    z(f'<rect x="0" y="{yb - 60}" width="{w}" height="90" fill="{z.lin((0, yb - 60), (0, yb + 30), [(0, "#ff9a50", 0), (0.6, "#ff9a50", 0.35 if not noche else 0.08), (1, "#ff9a50", 0)])}"/>')
    # arena / suelo
    z(f'<path d="M0 {yb} Q{w * 0.3} {yb - 18} {w * 0.6} {yb + 8} T{w} {yb - 4} L{w} {h} L0 {h} Z" fill="{z.lin((0, yb), (0, h), [(0, "#7a4a30" if not noche else "#2a2030"), (0.4, "#3a2420" if not noche else "#16121e"), (1, "#120c10")])}"/>')
    for k in range(5):
        yy = yb + 60 + k * 70
        z(f'<path d="M0 {yy} Q{w * 0.4} {yy - 20} {w} {yy + 10}" stroke="#000" stroke-width="3" opacity="0.15" fill="none"/>')
    z.guardar()
    return _a(n)


def bg_cielo_dubai(L, sem=511):
    """Cielo de atardecer del desierto: violeta arriba, naranja en el horizonte; sin suelo (lo pone `skyline_dubai`)."""
    w, h = L.w, L.h
    L.add(L.rect(L.lg((0, "#1c1838"), (0.35, "#5a3a6a"), (0.62, "#d0705a"), (0.78, "#ff9a50"), (1, "#ffc070"))))
    L.add(L.luz(w * 0.5, h * 0.75, w * 0.9, 500, "#ffb060", 0.5))
    L.add(L.polvo(25, 0, 0, w, h * 0.25, "#ffffff", 1.4, 0.5, sem=sem))
    for k in range(4):
        y = h * (0.42 + 0.07 * k)
        L.add(f'<path d="M{-50 + k * 90} {y:.0f} q{w * 0.3} -12 {w * 0.6} 0" stroke="#ffc0a0" stroke-width="{10 - k * 2}" opacity="0.25" stroke-linecap="round" fill="none"/>')
    return {}


def bg_cielo_noche_dubai(L, sem=512):
    w, h = L.w, L.h
    L.add(L.rect(L.lg((0, "#060818"), (0.6, "#16183a"), (0.85, "#3a2a4a"), (1, "#5a3a48"))))
    L.add(L.polvo(120, 0, 0, w, h * 0.7, "#ffffff", 2.0, 0.8, sem=sem))
    return {}


def ascensor(n="ascensor", fot="a"):
    """Cabina de ascensor de cristal con una persona dentro y luces de velocidad (sin rótulos)."""
    w, h = 520, 760
    z = Lz(n, w, h, **SALA)
    met = mat("#9aa4b4", "#e8eef8", "#4a5262")
    z(f'<rect x="40" y="40" width="440" height="680" rx="26" fill="{z.lin((40, 0), (480, 0), [(0, met["s"]), (0.5, met["l"]), (1, met["s"])])}"/>',
      f'<rect x="70" y="80" width="380" height="600" rx="12" fill="{z.lin((0, 80), (0, 680), [(0, "#2a3a5a"), (1, "#0e1426")])}"/>')
    # silueta de persona dentro, con luz cálida
    z(f'<circle cx="260" cy="250" r="56" fill="#2a1e1a"/>',
      f'<path d="M170 690 L180 380 Q260 320 340 380 L350 690 Z" fill="#3a3046"/>',
      f'<path d="M196 260 Q260 180 324 260" stroke="#ffb070" stroke-width="6" fill="none" opacity="0.6"/>')
    # reflejos del cristal
    z(f'<path d="M100 100 L170 100 L110 660 L80 660 Z" fill="#ffffff" opacity="0.10"/>',
      f'<path d="M380 100 L410 100 L360 660 L340 660 Z" fill="#ffffff" opacity="0.08"/>')
    # luz del techo
    z(f'<rect x="150" y="60" width="220" height="14" rx="6" fill="#fff6d8"/>',
      f'<path d="M150 74 L370 74 L430 300 L90 300 Z" fill="#fff6d8" opacity="0.10"/>')
    z.guardar()
    return _a(n)


def arco_tierra(n="arco_tierra"):
    """Gran arco de la Tierra visto de lado con atmósfera, mar y una franja de tierra: para enseñar la curvatura."""
    w, h = 1400, 700
    z = Lz(n, w, h, **ATARDECER)
    R = 950
    cx, cy = w / 2, 120 + R
    z(f'<circle cx="{cx}" cy="{cy}" r="{R + 46}" fill="{z.rad((cx, cy), R + 46, [(0.95, "#7ad0ff", 0), (0.975, "#7ad0ff", 0.55), (1, "#7ad0ff", 0)])}"/>',
      f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{z.rad((cx - 300, cy - R), R * 1.2, [(0, "#3a9ad8"), (0.5, "#1a5a9a"), (1, "#0a1e3a")])}"/>')
    z.guardar()
    return _a(n)


def datiles(n="datiles"):
    """Cuenco de dátiles y un vaso de agua: la comida al ponerse el sol."""
    w, h = 820, 560
    z = Lz(n, w, h, **ATARDECER)
    sombra_suelo(z, 330, 520, 300, 34)
    cer = mat("#2a6a9a", "#6ab0e0", "#123a5a")
    z(f'<path d="M80 330 Q330 560 580 330 Z" fill="{z.lin((80, 0), (580, 0), [(0, cer["s"]), (0.45, cer["l"]), (1, cer["s"])])}"/>',
      f'<ellipse cx="330" cy="330" rx="250" ry="44" fill="{cer["s"]}"/>',
      f'<path d="M110 360 Q330 470 550 360" stroke="#ffe0a0" stroke-width="10" fill="none" opacity="0.7"/>')
    r = _rnd(21)
    for i in range(16):
        x = 140 + (i % 6) * 72 + r.uniform(-10, 10)
        y = 300 - (i // 6) * 38 + r.uniform(-8, 8)
        a = r.uniform(-40, 40)
        g = z.rad((x - 10, y - 10), 60, [(0, "#c86a3a"), (0.5, "#6a2a12"), (1, "#2a0e06")])
        z(f'<ellipse cx="{F(x)}" cy="{F(y)}" rx="44" ry="24" fill="{g}" transform="rotate({F(a)} {F(x)} {F(y)})"/>',
          f'<ellipse cx="{F(x - 12)}" cy="{F(y - 8)}" rx="16" ry="5" fill="#ffd8a8" opacity="0.5" transform="rotate({F(a)} {F(x)} {F(y)})"/>')
    # vaso
    z(f'<path d="M640 180 L780 180 L760 500 L660 500 Z" fill="#dff4ff" opacity="0.35" stroke="#ffffff" stroke-width="4"/>',
      f'<path d="M645 250 L775 250 L760 500 L660 500 Z" fill="{z.lin((0, 250), (0, 500), [(0, "#9ad8ff", 0.7), (1, "#3a8ac8", 0.8)])}"/>',
      f'<path d="M660 200 L672 480" stroke="#ffffff" stroke-width="8" opacity="0.6"/>')
    z.guardar()
    return _a(n)


# =========================================================================== 02 · ozono
def aura_ozono(n="aura_ozono", hueco=False):
    """Anillo de la capa de ozono para poner encima de `foto_mundo` (mismo centro; la Tierra ocupa ≈ el 82 % del lienzo)."""
    w = h = 1000
    z = Lz(n, w, h)
    c = (500, 500)
    R = 410
    z(f'<circle cx="500" cy="500" r="{R + 60}" fill="{z.rad(c, R + 60, [(0.84, "#40e0ff", 0), (0.9, "#40e0ff", 0.55), (0.95, "#a0f4ff", 0.85), (1, "#40e0ff", 0)])}"/>')
    if hueco:
        z(f'<ellipse cx="500" cy="900" rx="170" ry="60" fill="#05030a" opacity="0.85"/>')
    z.guardar(textura=False)
    return _a(n)


def rayo_uv(n="rayo_uv"):
    """Rayo violeta en zigzag con halo (luz ultravioleta)."""
    w, h = 300, 900
    z = Lz(n, w, h)
    pts = "150,0 110,250 190,330 120,560 200,640 150,900"
    z(f'<polyline points="{pts}" stroke="#b06aff" stroke-width="46" opacity="0.25" fill="none" stroke-linejoin="round"/>',
      f'<polyline points="{pts}" stroke="#d29aff" stroke-width="20" opacity="0.8" fill="none" stroke-linejoin="round"/>',
      f'<polyline points="{pts}" stroke="#ffffff" stroke-width="6" fill="none" stroke-linejoin="round"/>')
    z.guardar(textura=False)
    return _a(n)


def dos_monedas(n="dos_monedas"):
    """Dos monedas apiladas vistas de lado, muy de cerca (sin grabados)."""
    w, h = 900, 520
    z = Lz(n, w, h, **SALA)
    sombra_suelo(z, 450, 470, 380, 40)
    m = mat("#d8a040", "#fff0b0", "#7a5010")
    for k, y in enumerate((380, 300)):
        z(f'<path d="M90 {y - 40} L90 {y + 20} A360 70 0 0 0 810 {y + 20} L810 {y - 40} Z" fill="{z.lin((90, 0), (810, 0), [(0, m["s"]), (0.35, m["l"]), (0.6, m["b"]), (1, m["s"])])}"/>')
        for x in range(110, 800, 18):
            z(f'<path d="M{x} {y - 30} L{x} {y + 20 + 60 * math.sin(math.pi * (x - 90) / 720) ** 0.5 * 0.2}" stroke="#7a5010" stroke-width="3" opacity="0.4"/>')
        z(f'<ellipse cx="450" cy="{y - 40}" rx="360" ry="70" fill="{z.rad((380, y - 70), 380, [(0, "#fff6c8"), (0.5, m["b"]), (1, m["s"])])}"/>',
          f'<ellipse cx="450" cy="{y - 40}" rx="300" ry="54" fill="none" stroke="#7a5010" stroke-width="4" opacity="0.5"/>')
    z.guardar()
    return _a(n)


def nevera(n="nevera"):
    """Nevera antigua de esquinas redondeadas, con tirador cromado."""
    w, h = 520, 980
    z = Lz(n, w, h, **SALA)
    sombra_suelo(z, 260, 955, 240, 30)
    c = mat("#e8f0e8", "#ffffff", "#9aa8a0")
    z(f'<rect x="40" y="40" width="440" height="900" rx="70" fill="{z.lin((40, 0), (480, 0), [(0, c["s"]), (0.4, c["l"]), (1, c["s"])])}"/>',
      f'<path d="M40 360 L480 360" stroke="#7a8a82" stroke-width="6"/>',
      f'<rect x="390" y="180" width="30" height="130" rx="12" fill="#c8ccd4" stroke="#6a7078" stroke-width="3"/>',
      f'<rect x="390" y="420" width="30" height="200" rx="12" fill="#c8ccd4" stroke="#6a7078" stroke-width="3"/>',
      f'<path d="M80 80 Q90 500 80 900" stroke="#ffffff" stroke-width="20" opacity="0.5"/>')
    z.guardar()
    return _a(n)


def spray(n="spray"):
    """Bote de espray con boquilla y nube de gotitas (sin marca)."""
    w, h = 520, 820
    z = Lz(n, w, h, **SALA)
    sombra_suelo(z, 200, 800, 130, 18)
    c = mat("#e04a4a", "#ff8a7a", "#7a1a1a")
    z(f'<rect x="100" y="240" width="200" height="560" rx="30" fill="{z.lin((100, 0), (300, 0), [(0, c["s"]), (0.35, c["l"]), (1, c["s"])])}"/>',
      f'<rect x="100" y="400" width="200" height="200" fill="#ffffff" opacity="0.85"/>',
      f'<path d="M120 200 Q200 150 280 200 L300 250 L100 250 Z" fill="#c8ccd4"/>',
      f'<rect x="175" y="130" width="50" height="50" rx="8" fill="#f4f4f4"/><rect x="225" y="148" width="22" height="12" fill="#888"/>')
    r = _rnd(4)
    for _ in range(70):
        d = r.uniform(20, 240)
        a = r.uniform(-0.45, 0.35)
        z(f'<circle cx="{F(250 + d * math.cos(a))}" cy="{F(154 + d * math.sin(a))}" r="{F(r.uniform(2, 7) * (1 - d / 300))}" fill="#e8f4ff" opacity="{r.uniform(0.3, 0.8):.2f}"/>')
    z.guardar()
    return _a(n)


def aire_acond(n="aire_acond"):
    """Aparato de aire acondicionado de pared con rejilla y aire frío."""
    w, h = 900, 420
    z = Lz(n, w, h, **SALA)
    c = mat("#f2f4f6", "#ffffff", "#a8b0b8")
    z(f'<rect x="40" y="40" width="820" height="230" rx="40" fill="{z.lin((0, 40), (0, 270), [(0, c["l"]), (0.6, c["b"]), (1, c["s"])])}"/>')
    for k in range(6):
        z(f'<path d="M110 {200 + k * 10} L790 {200 + k * 10}" stroke="#8a929a" stroke-width="3"/>')
    z(f'<circle cx="790" cy="90" r="8" fill="#5dff8a"/>')
    for k in range(4):
        x = 180 + k * 170
        z(f'<path d="M{x} 290 q-30 40 0 80 q30 40 0 60" stroke="#9ad8ff" stroke-width="10" fill="none" opacity="0.6" stroke-linecap="round"/>')
    z.guardar()
    return _a(n)


def _bola(z, x, y, r, c0, c1, c2, letra=None):
    z(f'<circle cx="{F(x)}" cy="{F(y)}" r="{F(r)}" fill="{z.rad((x - r * 0.35, y - r * 0.4), r * 1.3, [(0, c0), (0.5, c1), (1, c2)])}"/>',
      f'<ellipse cx="{F(x - r * 0.35)}" cy="{F(y - r * 0.45)}" rx="{F(r * 0.3)}" ry="{F(r * 0.18)}" fill="#ffffff" opacity="0.6"/>')


def molecula_ozono(n="molecula_ozono"):
    """O3: tres esferas azules unidas en V."""
    w, h = 600, 440
    z = Lz(n, w, h)
    for a, b in (((300, 150), (140, 300)), ((300, 150), (460, 300))):
        z(f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" stroke="#d8e8ff" stroke-width="34" stroke-linecap="round"/>')
    for x, y in ((140, 300), (460, 300), (300, 150)):
        _bola(z, x, y, 110, "#e8f8ff", "#3ab0ff", "#0a3a8a")
    z.guardar(textura=False)
    return _a(n)


def atomo_cloro(n="atomo_cloro"):
    w = h = 400
    z = Lz(n, w, h)
    z(f'<circle cx="200" cy="200" r="190" fill="{z.rad((200, 200), 190, [(0.5, "#7dff6a", 0.5), (1, "#7dff6a", 0)])}"/>')
    _bola(z, 200, 200, 120, "#f0ffe8", "#5ad83a", "#1a5a0a")
    z.guardar(textura=False)
    return _a(n)


def molecula_cfc(n="molecula_cfc"):
    """CFC: carbono gris en el centro con dos cloros verdes y dos flúores amarillos."""
    w = h = 640
    z = Lz(n, w, h)
    pos = [(320, 120, "cl"), (130, 380, "cl"), (510, 380, "f"), (320, 520, "f")]
    for x, y, _ in pos:
        z(f'<path d="M320 320 L{x} {y}" stroke="#e0e0e0" stroke-width="30" stroke-linecap="round"/>')
    _bola(z, 320, 320, 110, "#e8e8e8", "#7a7a7a", "#2a2a2a")
    for x, y, t in pos:
        if t == "cl":
            _bola(z, x, y, 95, "#f0ffe8", "#5ad83a", "#1a5a0a")
        else:
            _bola(z, x, y, 75, "#fffbe0", "#f0d040", "#7a5a00")
    z.guardar(textura=False)
    return _a(n)


def polo_sur(n="polo_sur"):
    """La Tierra vista desde abajo: la Antártida blanca en el centro rodeada de océano."""
    w = h = 1000
    z = Lz(n, w, h, luz=(-0.5, -0.8), rim="#bfe4ff")
    c = (500, 500)
    z(f'<circle cx="500" cy="500" r="470" fill="{z.rad((420, 400), 560, [(0, "#3a8ad0"), (0.6, "#174a8a"), (1, "#06142e")])}"/>')
    r = _rnd(31)
    pts = []
    for k in range(40):
        a = 2 * math.pi * k / 40
        rr = 230 + 40 * math.sin(3 * a) + r.uniform(-18, 18) + (90 if 2.2 < a < 2.9 else 0)
        pts.append(f"{F(500 + rr * math.cos(a))},{F(500 + rr * math.sin(a))}")
    z(f'<polygon points="{" ".join(pts)}" fill="{z.rad((460, 450), 320, [(0, "#ffffff"), (0.7, "#e4f0fa"), (1, "#a8c4dc")])}" stroke="#ffffff" stroke-width="6"/>')
    for _ in range(12):
        a = r.uniform(0, 6.28)
        d = r.uniform(300, 440)
        z(f'<ellipse cx="{F(500 + d * math.cos(a))}" cy="{F(500 + d * math.sin(a))}" rx="{F(r.uniform(40, 110))}" ry="{F(r.uniform(10, 22))}" '
          f'fill="#ffffff" opacity="0.4" transform="rotate({F(math.degrees(a) + 90)} {F(500 + d * math.cos(a))} {F(500 + d * math.sin(a))})"/>')
    z(f'<circle cx="500" cy="500" r="478" fill="none" stroke="#7ad0ff" stroke-width="12" opacity="0.5"/>')
    z.guardar()
    return _a(n)


def agujero(n="agujero_ozono"):
    """Mancha violeta translúcida con borde azul (el agujero, como en los mapas de la NASA)."""
    w = h = 800
    z = Lz(n, w, h)
    r = _rnd(8)
    pts = []
    for k in range(36):
        a = 2 * math.pi * k / 36
        rr = 300 + 30 * math.sin(2 * a + 0.5) + r.uniform(-14, 14)
        pts.append(f"{F(400 + rr * math.cos(a))},{F(400 + rr * math.sin(a) * 0.92)}")
    z(f'<polygon points="{" ".join(pts)}" fill="{z.rad((400, 400), 330, [(0, "#3a0a6a", 0.85), (0.7, "#7a2ad0", 0.65), (1, "#2a8aff", 0.35)])}" '
      f'stroke="#40c0ff" stroke-width="10" stroke-linejoin="round"/>')
    z.guardar(textura=False)
    return _a(n)


def vortice(n="vortice"):
    """Remolino de viento helado (vórtice polar)."""
    w = h = 900
    z = Lz(n, w, h)
    for k in range(5):
        a0 = k * 72
        d = []
        for i in range(60):
            t = i / 59
            a = math.radians(a0 + t * 300)
            rr = 60 + t * 360
            d.append(f"{'M' if i == 0 else 'L'}{F(450 + rr * math.cos(a))} {F(450 + rr * math.sin(a))}")
        z(f'<path d="{" ".join(d)}" stroke="#bfefff" stroke-width="{F(26 - k * 2)}" opacity="0.55" fill="none" stroke-linecap="round"/>')
    z.guardar(textura=False)
    return _a(n)


def bg_estratosfera(L, sem=531):
    """La Tierra desde muy alto: curva del horizonte abajo, franja azul de la atmósfera y cielo negro arriba."""
    w, h = L.w, L.h
    L.add(L.rect(L.lg((0, "#02030a"), (0.55, "#060a22"), (0.72, "#0e2a6a"), (0.8, "#3a8ae0"), (0.84, "#bfe8ff"), (0.86, "#2a6ab0"), (1, "#0a2a4a"))))
    L.add(L.polvo(90, 0, 0, w, h * 0.5, "#ffffff", 2.0, 0.7, sem=sem))
    L.add(f'<path d="M-200 {h * 0.86:.0f} Q{w / 2} {h * 0.78:.0f} {w + 200} {h * 0.86:.0f} L{w + 200} {h} L-200 {h} Z" fill="{L.lg((0, "#2a6aa0"), (0.3, "#1a4a7a"), (1, "#0a1a30"))}"/>')
    L.add(L.luz(w * 0.5, h * 0.8, w, 160, "#9ad8ff", 0.5))
    return {}


# =========================================================================== 03 · piel de gallina
PIEL_B = dict(b="#e3b08c", s="#b07656", l="#f6d2b2")


def brazo_piel(n, gallina=False):
    """Antebrazo de lado, muy grande, con vello: tumbado (liso) o de punta con bultitos (gallina)."""
    w, h = 1400, 700
    z = Lz(n, w, h, luz=(-0.5, -0.9), rim="#ffe8d0")
    top = 230
    d = f"M-40 {top + 20} Q400 {top - 20} 1000 {top + 50} L1000 560 Q500 640 -40 610 Z"
    # mano (dorso, dedos juntos hacia la derecha)
    gm = z.lin((0, top + 40), (0, 580), [(0, PIEL_B["l"]), (0.4, PIEL_B["b"]), (1, PIEL_B["s"])])
    z(f'<path d="M980 {top + 46} Q1080 {top + 30} 1180 {top + 70} L1300 {top + 90} Q1380 {top + 110} 1384 {top + 150} Q1380 {top + 186} 1300 {top + 184} '
      f'L1300 {top + 200} Q1370 {top + 214} 1366 {top + 250} Q1360 {top + 284} 1290 {top + 280} L1290 {top + 296} Q1350 {top + 312} 1342 {top + 344} '
      f'Q1334 {top + 372} 1270 {top + 364} Q1200 {top + 380} 1150 {top + 360} Q1080 {top + 350} 980 560 Z" fill="{gm}"/>',
      f'<path d="M1300 {top + 184} L1200 {top + 180} M1290 {top + 280} L1190 {top + 272} M1270 {top + 364} L1180 {top + 350}" stroke="{PIEL_B["s"]}" stroke-width="5" opacity="0.6" fill="none"/>',
      f'<path d="M1340 {top + 110} q20 18 14 40" stroke="#ffffff" stroke-width="6" opacity="0.5" fill="none"/>')
    z(f'<path d="{d}" fill="{z.lin((0, top), (0, 640), [(0, PIEL_B["l"]), (0.35, PIEL_B["b"]), (1, PIEL_B["s"])])}"/>',
      f'<path d="M-40 {top + 30} Q400 {top - 12} 960 {top + 44}" stroke="#fff2e0" stroke-width="10" opacity="0.5" fill="none"/>')
    r = _rnd(12)
    for _ in range(110):
        x = r.uniform(10, 960)
        yb = top + 10 + 40 * ((x - 700) / 700) ** 2 * 0.5
        y = r.uniform(yb + 15, yb + 300)
        if gallina:
            z(f'<circle cx="{F(x)}" cy="{F(y)}" r="7" fill="{PIEL_B["l"]}"/><circle cx="{F(x + 2)}" cy="{F(y + 3)}" r="7" fill="{PIEL_B["s"]}" opacity="0.35"/>')
            a = math.radians(-90 + r.uniform(-18, 18))
            L = r.uniform(34, 56)
        else:
            a = math.radians(r.uniform(-12, 8))
            L = r.uniform(40, 62)
        z(f'<path d="M{F(x)} {F(y)} q{F(L * 0.5 * math.cos(a) + 3)} {F(L * 0.5 * math.sin(a))} {F(L * math.cos(a))} {F(L * math.sin(a))}" '
          f'stroke="#3a2416" stroke-width="2.6" fill="none" opacity="0.85" stroke-linecap="round"/>')
    z.guardar()
    return _a(n)


def corte_piel(n, estado="liso"):
    """Corte de la piel: capas, un folículo con su pelo y el músculo diminuto (rojo). Estados: liso, gallina, nervio."""
    w, h = 1000, 1100
    z = Lz(n, w, h, luz=(-0.5, -0.9), rim="#ffe8d0")
    ys = 300
    bulto = 34 if estado != "liso" else 0
    z(f'<path d="M0 {ys} L380 {ys} Q450 {ys - bulto} 520 {ys} L1000 {ys} L1000 1100 L0 1100 Z" fill="{z.lin((0, ys), (0, 1100), [(0, "#f6d2b2"), (0.12, "#e8a890"), (0.4, "#d88a7a"), (1, "#f2dcb0")])}"/>',
      f'<path d="M0 {ys + 40} L1000 {ys + 40}" stroke="#c06a5a" stroke-width="4" opacity="0.4"/>',
      f'<rect x="0" y="760" width="1000" height="340" fill="#fff0c8" opacity="0.6"/>')
    for k in range(10):
        z(f'<circle cx="{60 + k * 100}" cy="{900 + (k % 2) * 60}" r="46" fill="#ffe8a8" stroke="#e8c880" stroke-width="3" opacity="0.8"/>')
    # folículo
    fx, fy = 450, 720
    z(f'<path d="M{fx - 40} {ys + 20} L{fx - 60} {fy} Q{fx} {fy + 70} {fx + 60} {fy} L{fx + 40} {ys + 20}" fill="#b85a4a" opacity="0.55"/>',
      f'<ellipse cx="{fx}" cy="{fy}" rx="58" ry="40" fill="#8a3a2a"/>')
    if estado == "nervio":
        for k in range(6):
            a = k * 1.05
            z(f'<circle cx="{F(fx - 30 + 22 * math.cos(a))}" cy="{F(fy - 80 + 30 * math.sin(a))}" r="16" fill="#7dff6a"/>'
              f'<circle cx="{F(fx - 30 + 22 * math.cos(a))}" cy="{F(fy - 80 + 30 * math.sin(a))}" r="34" fill="#7dff6a" opacity="0.25"/>')
    # pelo
    ang = -88 if estado != "liso" else -28
    a = math.radians(ang)
    L = 380
    z(f'<path d="M{fx} {fy} L{fx} {ys}" stroke="#3a2416" stroke-width="14" stroke-linecap="round"/>',
      f'<path d="M{fx} {ys} L{F(fx + L * math.cos(a))} {F(ys + L * math.sin(a))}" stroke="#3a2416" stroke-width="12" stroke-linecap="round"/>')
    if estado == "nervio":
        z(f'<path d="M{fx + 12} {ys} L{F(fx + 12 + 200 * math.cos(a))} {F(ys + 200 * math.sin(a))}" stroke="#7dff6a" stroke-width="8" stroke-linecap="round"/>')
    # músculo: del folículo hacia la superficie a la derecha
    mx0, my0 = fx + 20, fy - 160
    mx1, my1 = (fx + 250, ys + 50) if estado == "liso" else (fx + 190, ys + 70)
    grosor = 26 if estado == "liso" else 44
    z(f'<path d="M{mx0} {my0} Q{(mx0 + mx1) / 2 + 30} {(my0 + my1) / 2 + 40} {mx1} {my1}" stroke="#c8202a" stroke-width="{grosor}" stroke-linecap="round" fill="none"/>',
      f'<path d="M{mx0} {my0} Q{(mx0 + mx1) / 2 + 30} {(my0 + my1) / 2 + 40} {mx1} {my1}" stroke="#ff7a7a" stroke-width="{grosor * 0.3}" stroke-linecap="round" fill="none" opacity="0.6"/>')
    # nervio amarillo
    op = 1.0 if estado == "nervio" else 0.55
    z(f'<path d="M1000 700 Q800 640 {mx0 + 120} {my0 + 50}" stroke="#ffd23f" stroke-width="{16 if estado == "nervio" else 10}" fill="none" opacity="{op}"/>')
    if estado == "nervio":
        z(f'<path d="M1000 700 Q800 640 {mx0 + 120} {my0 + 50}" stroke="#ffd23f" stroke-width="40" fill="none" opacity="0.25"/>')
    z.guardar()
    return _a(n)


def gato(n, erizado=False):
    """Gato gris de perfil: tranquilo, o asustado con el lomo arqueado y el pelo erizado."""
    w, h = 1000, 800
    z = Lz(n, w, h, **SALA)
    sombra_suelo(z, 500, 760, 380, 40)
    pel = mat("#6a6e7a", "#a8acb8", "#2e3038")
    lomo = 330 if erizado else 430
    # cuerpo
    cuerpo = f"M250 560 Q240 {lomo} 500 {lomo - 20} Q760 {lomo} 760 560 Q500 610 250 560 Z"
    if erizado:
        r = _rnd(3)
        pts = []
        for k in range(46):
            t = k / 45
            x = 230 + t * 560
            y = 560 - (560 - (lomo - 30)) * math.sin(math.pi * t) ** 0.8
            pts.append(f"{F(x)},{F(y - (r.uniform(18, 40) if k % 2 else 0))}")
        z(f'<polygon points="230,580 {" ".join(pts)} 790,580" fill="{pel["s"]}"/>')
    z(f'<path d="{cuerpo}" fill="{z.lin((0, lomo), (0, 600), [(0, pel["l"]), (0.5, pel["b"]), (1, pel["s"])])}"/>')
    # patas
    for x in (300, 360, 660, 720):
        z(f'<path d="M{x} 540 L{x - 6} 740 Q{x + 14} 756 {x + 30} 740 L{x + 30} 540" fill="{pel["b"]}" stroke="{pel["s"]}" stroke-width="3"/>')
    # cola
    if erizado:
        z(f'<path d="M250 500 Q140 360 200 200" stroke="{pel["b"]}" stroke-width="70" stroke-linecap="round" fill="none"/>',
          f'<path d="M250 500 Q140 360 200 200" stroke="{pel["s"]}" stroke-width="86" stroke-dasharray="6 10" stroke-linecap="round" fill="none" opacity="0.6"/>')
    else:
        z(f'<path d="M250 520 Q120 560 150 400" stroke="{pel["b"]}" stroke-width="34" stroke-linecap="round" fill="none"/>')
    # cabeza
    hx, hy = 810, (430 if erizado else 400)
    z(f'<path d="M{hx - 70} {hy - 60} L{hx - 50} {hy - 150} L{hx - 10} {hy - 80} Z" fill="{pel["s"]}"/>',
      f'<path d="M{hx + 30} {hy - 80} L{hx + 70} {hy - 150} L{hx + 80} {hy - 50} Z" fill="{pel["s"]}"/>',
      f'<circle cx="{hx}" cy="{hy}" r="95" fill="{z.rad((hx - 30, hy - 30), 120, [(0, pel["l"]), (0.6, pel["b"]), (1, pel["s"])])}"/>')
    ojo_r = 20 if erizado else 15
    for dx in (-35, 35):
        z(f'<ellipse cx="{hx + dx}" cy="{hy - 15}" rx="{ojo_r}" ry="{ojo_r + 4}" fill="#e8d040"/>',
          f'<ellipse cx="{hx + dx}" cy="{hy - 15}" rx="{6 if erizado else 4}" ry="{ojo_r}" fill="#111"/>',
          f'<circle cx="{hx + dx - 5}" cy="{hy - 22}" r="4" fill="#fff"/>')
    z(f'<path d="M{hx - 10} {hy + 25} L{hx + 10} {hy + 25} L{hx} {hy + 36} Z" fill="#e88a9a"/>')
    if erizado:
        z(f'<path d="M{hx - 30} {hy + 50} Q{hx} {hy + 30} {hx + 30} {hy + 50} L{hx + 20} {hy + 70} L{hx - 20} {hy + 70} Z" fill="#3a1a1a"/>',
          f'<path d="M{hx - 18} {hy + 50} L{hx - 14} {hy + 64}" stroke="#fff" stroke-width="5"/><path d="M{hx + 18} {hy + 50} L{hx + 14} {hy + 64}" stroke="#fff" stroke-width="5"/>')
    for s in (-1, 1):
        for k in (-1, 0, 1):
            z(f'<path d="M{hx + s * 30} {hy + 30} l{s * 110} {k * 18}" stroke="#ffffff" stroke-width="2" opacity="0.6"/>')
    z.guardar()
    return _a(n)


def raton(n="raton"):
    """Ratón de laboratorio blanco, de perfil."""
    w, h = 800, 460
    z = Lz(n, w, h, **SALA)
    sombra_suelo(z, 380, 430, 260, 26)
    pel = mat("#f2f0ec", "#ffffff", "#b8b0a8")
    z(f'<path d="M120 380 Q100 230 330 200 Q520 180 590 300 Q620 380 560 400 L160 410 Z" fill="{z.lin((0, 190), (0, 410), [(0, pel["l"]), (0.6, pel["b"]), (1, pel["s"])])}"/>',
      f'<path d="M570 300 Q700 300 740 360 Q700 400 580 392 Z" fill="{pel["b"]}"/>',
      f'<circle cx="560" cy="230" r="54" fill="#f6c8c8" stroke="{pel["s"]}" stroke-width="4"/>',
      f'<circle cx="650" cy="335" r="10" fill="#c81a3a"/><circle cx="647" cy="331" r="3" fill="#fff"/>',
      f'<circle cx="742" cy="360" r="9" fill="#ff8aa0"/>',
      f'<path d="M120 370 Q30 340 20 260 Q10 200 60 160" stroke="#f0b0b0" stroke-width="10" fill="none" stroke-linecap="round"/>')
    for x in (220, 300, 470, 530):
        z(f'<ellipse cx="{x}" cy="414" rx="22" ry="10" fill="#f0b0b0"/>')
    z.guardar()
    return _a(n)


def celulas_madre(n="celulas_madre"):
    """Racimo de células que se encienden (verde neón)."""
    w = h = 700
    z = Lz(n, w, h)
    r = _rnd(44)
    for _ in range(14):
        x, y, rr = r.uniform(150, 550), r.uniform(150, 550), r.uniform(50, 90)
        z(f'<circle cx="{F(x)}" cy="{F(y)}" r="{F(rr * 1.6)}" fill="#7dff6a" opacity="0.12"/>',
          f'<circle cx="{F(x)}" cy="{F(y)}" r="{F(rr)}" fill="{z.rad((x - rr * 0.3, y - rr * 0.3), rr * 1.2, [(0, "#eaffe0"), (0.5, "#7ae860"), (1, "#1e6a1a")])}"/>',
          f'<circle cx="{F(x + 6)}" cy="{F(y + 4)}" r="{F(rr * 0.35)}" fill="#2a8a2a" opacity="0.7"/>')
    z.guardar(textura=False)
    return _a(n)


def auriculares(n="auriculares"):
    w, h = 600, 520
    z = Lz(n, w, h, **SALA)
    z(f'<path d="M110 360 Q110 70 300 70 Q490 70 490 360" stroke="#2a2a30" stroke-width="40" fill="none" stroke-linecap="round"/>')
    for x in (110, 490):
        z(f'<rect x="{x - 65}" y="300" width="130" height="190" rx="50" fill="{z.lin((x - 65, 0), (x + 65, 0), [(0, "#1a1a22"), (0.5, "#5a5a6a"), (1, "#1a1a22")])}"/>',
          f'<rect x="{x - 40}" y="330" width="80" height="130" rx="36" fill="#e04a6a"/>')
    z.guardar()
    return _a(n)


def generar(dirsvg):
    T26.generar(dirsvg)
    ilus.OUT = dirsvg
    # 01
    torre("torre"); torre("torre_noche", noche=1.0)
    sol_poniente(); skyline("skyline_dubai"); skyline("skyline_noche", noche=True)
    ascensor(); arco_tierra(); datiles()
    T25.p_mira_arriba("mira_sol", MIRADOR, ang=8) if hasattr(T25, "p_mira_arriba") else None
    NOMBRES.append("mira_sol")
    _a(busto("cara_mirador", MIRADOR, "sorpresa", ang=-4, luz=ATARDECER))
    # 02
    aura_ozono(); aura_ozono("aura_ozono_hueco", hueco=True); rayo_uv(); dos_monedas(); nevera(); spray(); aire_acond()
    molecula_ozono(); atomo_cloro(); molecula_cfc(); polo_sur(); agujero(); vortice()
    # 03
    brazo_piel("brazo_liso"); brazo_piel("brazo_gallina", gallina=True)
    corte_piel("piel_corte_a", "liso"); corte_piel("piel_corte_b", "gallina"); corte_piel("piel_corte_c", "nervio")
    gato("gato_calma"); gato("gato_erizado", erizado=True); raton(); celulas_madre(); auriculares()
    T25.p_de_pie("oyente", OYENTE, 3, "sonrisa", 0, luz=SALA)
    T25.p_de_pie("investigadora", INVESTIGADORA, 1, "neutra", 2, luz=SALA)
    _a(busto("cara_oyente", OYENTE, "sorpresa", ang=3, luz=SALA))
    for i, f in enumerate((bg_cielo_dubai, bg_cielo_noche_dubai, bg_estratosfera)):
        L = IE.Lienzo(f.__name__, 1080, 1920, 5100 + i * 13)
        f(L)
        L.guardar(dirsvg, f.__name__)
        NOMBRES.append(f.__name__)
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
