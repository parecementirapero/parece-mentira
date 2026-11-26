"""Ilustraciones del lote 2026-11-26-tarde (Agente 20:00 (Jorge)), con el ESTILO DEL VÍDEO LARGO de la cueva
(DECISIONS 2026-11-26, Jorge). Reutiliza todo el arte del vídeo largo y del lote 2026-11-25-tarde (`ilus_1125t.generar`)
y añade solo las piezas nuevas de estos temas, con los mismos ayudantes (Lz, figura, cabeza, mat, sombra_suelo):
01 posponer la alarma · 02 la cara oculta de la Luna · 03 el Black Friday lo bautizó la policía.
Uso: python3 ilus_1126t.py DIR_SVG"""
import importlib.util, math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
LARGO = os.path.join(RAIZ, "lotes", "largo-cueva-500-dias", "generadores")
sys.path.insert(0, RAIZ)
sys.path.insert(0, LARGO)
from motor.biblioteca import ilus  # noqa: E402
import ilus_personajes as IP  # noqa: E402
import ilus_escenarios as IE  # noqa: E402
from ilus_personajes import Lz, figura, busto, cabeza, _pj, mat, F, sombra_suelo, pie_suelo, PIEL2, PIEL3, PIEL4, mix  # noqa: E402

_spec = importlib.util.spec_from_file_location("ilus_1125t", os.path.join(RAIZ, "lotes", "2026-11-25-tarde", "generadores", "ilus_1125t.py"))
T25 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(T25)

NOCHE = dict(luz=(-0.4, -0.9), rim="#9fc4ff")
SALA = dict(luz=(-0.6, -0.8), rim="#fff1d8")
CALLE = dict(luz=(-0.6, -0.8), rim="#ffd9a0")

DORMILON = _pj(nombre="dorm", peinado="corto", pelo="#3a2618", top=mat("#4a6fa8", "#7a9fd8", "#26406a"), prenda="camiseta", manga="larga",
               pant=mat("#4a6fa8", "#7a9fd8", "#26406a"), calzado="zapato", bota=mat("#2a2a2e"), edad=30, piel=PIEL2)
POLI = _pj(nombre="poli", peinado="corto", pelo="#1e1612", top=mat("#1f2f5a", "#3f5a9a", "#0e1630"), prenda="abrigo",
           pant=mat("#1a2448", "#34447a", "#0c1226"), calzado="zapato", bota=mat("#141414", "#3a3a3a", "#0a0a0a"), edad=40, piel=PIEL3,
           casco=dict(b="#1a2448", l="#3a4a8a", s="#0a0f22"))
POLI2 = _pj(nombre="poli2", peinado="corto", pelo="#5a3a22", top=mat("#1f2f5a", "#3f5a9a", "#0e1630"), prenda="abrigo",
            pant=mat("#1a2448", "#34447a", "#0c1226"), calzado="zapato", bota=mat("#141414", "#3a3a3a", "#0a0a0a"), edad=33, piel=PIEL2,
            casco=dict(b="#1a2448", l="#3a4a8a", s="#0a0f22"), barba="#5a3a22")
COMPRADORA = _pj(nombre="compra", fem=True, peinado="melena", pelo="#6a3a1e", top=mat("#b0402a", "#e0705a", "#601e12"), prenda="abrigo",
                 pant=mat("#2e3440"), calzado="zapato", bota=mat("#3a2418"), edad=38, piel=PIEL4)

NOMBRES = []


def _a(n):
    NOMBRES.append(n)
    return n


# =========================================================================== 01 · alarma
def despertador(fot="a"):
    """Despertador de dos campanas, rojo, con martillo que golpea a un lado u otro (fotogramas a/b)."""
    n, w, h = f"despertador_{fot}", 760, 860
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#ffe2b0")
    cx, cy, R = 380, 470, 250
    sombra_suelo(z, cx, 835, 250, 26)
    roj = mat("#c8302a", "#f0685a", "#6a1210")
    met = mat("#c8ccd4", "#ffffff", "#6a7078")
    # patas
    for s in (-1, 1):
        z(f'<path d="M{cx + s * 120} {cy + 200} L{cx + s * 190} 820" stroke="{met["s"]}" stroke-width="26" stroke-linecap="round"/>',
          f'<path d="M{cx + s * 117} {cy + 200} L{cx + s * 186} 815" stroke="{met["b"]}" stroke-width="12" stroke-linecap="round"/>')
    # campanas
    for s in (-1, 1):
        bx, by = cx + s * 170, cy - 230
        g = z.rad((bx - 40, by - 50), 170, [(0, "#ffffff"), (0.35, met["l"]), (1, met["s"])])
        z(f'<path d="M{bx - 110} {by + 50} A110 110 0 0 1 {bx + 110} {by + 50} Z" fill="{g}" transform="rotate({s * 28} {bx} {by + 50})"/>',
          f'<path d="M{bx - 60} {by - 20} A70 70 0 0 1 {bx + 10} {by - 50}" stroke="#ffffff" stroke-width="10" opacity="0.7" fill="none" '
          f'stroke-linecap="round" transform="rotate({s * 28} {bx} {by + 50})"/>')
    # soporte de campanas y asa
    z(f'<path d="M{cx - 170} {cy - 190} Q{cx} {cy - 330} {cx + 170} {cy - 190}" stroke="{met["s"]}" stroke-width="14" fill="none"/>',
      f'<circle cx="{cx}" cy="{cy - 262}" r="16" fill="{met["b"]}"/>')
    # martillo
    lado = -1 if fot == "a" else 1
    hx = cx + lado * 95
    z(f'<path d="M{cx} {cy - 250} L{hx} {cy - 300}" stroke="{met["s"]}" stroke-width="10" stroke-linecap="round"/>',
      f'<circle cx="{hx}" cy="{cy - 300}" r="18" fill="{met["b"]}"/><circle cx="{hx - 5}" cy="{cy - 306}" r="6" fill="#fff" opacity="0.8"/>')
    # caja
    g = z.rad((cx - 90, cy - 110), R * 1.6, [(0, roj["l"]), (0.55, roj["b"]), (1, roj["s"])])
    z(f'<circle cx="{cx}" cy="{cy + 12}" r="{R}" fill="#000" opacity="0.25"/>', f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{g}"/>',
      f'<path d="M{cx - R + 40} {cy - 80} A{R - 20} {R - 20} 0 0 1 {cx - 40} {cy - R + 30}" stroke="#ffffff" stroke-width="18" opacity="0.4" fill="none" stroke-linecap="round"/>',
      f'<path d="M{cx + R - 30} {cy + 70} A{R - 10} {R - 10} 0 0 1 {cx + 70} {cy + R - 20}" stroke="{z.rim}" stroke-width="10" opacity="0.6" fill="none"/>')
    # esfera
    gf = z.rad((cx - 40, cy - 50), 220, [(0, "#fffdf6"), (0.7, "#f2ead8"), (1, "#c8bea6")])
    z(f'<circle cx="{cx}" cy="{cy}" r="{R - 46}" fill="{met["s"]}"/><circle cx="{cx}" cy="{cy}" r="{R - 56}" fill="{gf}"/>')
    for k in range(60):
        a = math.radians(k * 6)
        r0, r1 = (R - 72, R - 98) if k % 5 == 0 else (R - 72, R - 84)
        z(f'<path d="M{cx + r0 * math.sin(a):.1f} {cy - r0 * math.cos(a):.1f} L{cx + r1 * math.sin(a):.1f} {cy - r1 * math.cos(a):.1f}" '
          f'stroke="#2a2420" stroke-width="{7 if k % 5 == 0 else 3}" stroke-linecap="round"/>')
    # agujas: 6:59 casi
    for ang, L_, wd in ((-150, 95, 16), (354, 140, 10)):
        a = math.radians(ang)
        z(f'<path d="M{cx} {cy} L{cx + L_ * math.sin(a):.1f} {cy - L_ * math.cos(a):.1f}" stroke="#1e1a16" stroke-width="{wd}" stroke-linecap="round"/>')
    z(f'<path d="M{cx} {cy} L{cx + 120 * math.sin(math.radians(30)):.1f} {cy - 120 * math.cos(math.radians(30)):.1f}" stroke="#d8382a" stroke-width="5" stroke-linecap="round"/>',
      f'<circle cx="{cx}" cy="{cy}" r="14" fill="#1e1a16"/><circle cx="{cx}" cy="{cy}" r="5" fill="#d8382a"/>',
      f'<path d="M{cx - 120} {cy - 120} A170 170 0 0 1 {cx + 60} {cy - 170}" stroke="#ffffff" stroke-width="14" opacity="0.35" fill="none" stroke-linecap="round"/>')
    z.guardar()
    return _a(n)


def boton_posponer():
    """Botón grande de posponer (barra de metal encima del despertador, visto de cerca), sin letras."""
    n, w, h = "boton_posponer", 760, 420
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#ffe2b0")
    g = z.lin((0, 120), (0, 360), [(0, "#f4f6fa"), (0.5, "#b8bec8"), (1, "#5a6068")])
    z('<rect x="60" y="210" width="640" height="170" rx="40" fill="#000" opacity="0.3" transform="translate(0 16)"/>',
      f'<rect x="60" y="210" width="640" height="170" rx="40" fill="{g}"/>', '<rect x="90" y="226" width="580" height="26" rx="13" fill="#ffffff" opacity="0.7"/>')
    gz = z.rad((300, 140), 400, [(0, "#ff8a6a"), (0.6, "#d8382a"), (1, "#6a1210")])
    z(f'<rect x="160" y="80" width="440" height="170" rx="60" fill="{gz}"/>', '<rect x="190" y="96" width="380" height="34" rx="17" fill="#ffffff" opacity="0.45"/>',
      '<path d="M330 150 l40 0 l-40 50 l40 0" stroke="#fff4e8" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
      '<path d="M400 130 l26 0 l-26 32 l26 0" stroke="#fff4e8" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.8"/>')
    z.guardar()
    return _a(n)


def cama(n, ex="cerrados", brazo=False, w=1300, h=640):
    """Cama vista de lado con el durmiente: cabeza girada sobre la almohada y el edredón hasta el cuello."""
    u = 112
    z = IP._cuadro(n, w, h, NOCHE)
    sombra_suelo(z, 650, 620, 600, 40)
    mad = mat("#6a4428", "#9a6a40", "#3a2212")
    # cabecero y patas
    z(f'<rect x="40" y="120" width="60" height="500" rx="18" fill="{mad["s"]}"/><rect x="48" y="120" width="30" height="500" rx="12" fill="{mad["b"]}"/>',
      f'<rect x="1200" y="300" width="50" height="320" rx="16" fill="{mad["s"]}"/><rect x="1206" y="300" width="24" height="320" rx="10" fill="{mad["b"]}"/>')
    # colchón y sábana
    gs = z.lin((0, 380), (0, 520), [(0, "#f2f4fa"), (1, "#a8b0c8")])
    z(f'<rect x="90" y="390" width="1130" height="140" rx="30" fill="{gs}"/>', f'<rect x="90" y="510" width="1130" height="40" rx="12" fill="{mad["b"]}"/>')
    # almohada
    ga = z.rad((220, 300), 220, [(0, "#ffffff"), (0.7, "#e4e8f2"), (1, "#a8b0c8")])
    z(f'<path d="M110 390 C100 300 150 260 260 262 C360 264 400 300 400 360 C400 400 360 412 250 412 C160 412 116 410 110 390 Z" fill="{ga}"/>')
    # cabeza de lado (corona a la izquierda)
    cabeza(z, (265, 300), 125, -84, DORMILON, "frente", ex)
    # edredón ondulado
    gd = z.lin((300, 280), (300, 560), [(0, "#7a9ae0"), (0.5, "#4a6ab8"), (1, "#223a78")])
    z(f'<path d="M320 330 C420 290 560 270 720 300 C880 330 1040 320 1180 360 C1230 380 1240 470 1220 540 L330 540 C300 470 300 380 320 330 Z" fill="{gd}"/>',
      '<path d="M360 330 C520 290 760 300 1170 370" stroke="#a8c0ff" stroke-width="8" opacity="0.5" fill="none" stroke-linecap="round"/>')
    for x in (520, 760, 1000):
        z(f'<path d="M{x} 310 C{x - 30} 400 {x + 10} 470 {x - 10} 540" stroke="#1a2a5a" stroke-width="6" opacity="0.4" fill="none"/>')
    if brazo:
        z(f'<path d="M420 330 C470 250 520 190 560 150" stroke="{DORMILON["top"]["b"]}" stroke-width="60" stroke-linecap="round" fill="none"/>',
          f'<path d="M415 320 C462 245 512 188 552 150" stroke="{DORMILON["top"]["l"]}" stroke-width="16" stroke-linecap="round" fill="none" opacity="0.5"/>')
        IP.mano_lado(z, (570, 130), -40, u, PIEL2, c=0.5, pal=1)
    z.guardar()
    return _a(n)


def mesilla():
    n, w, h = "mesilla", 520, 520
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#9fc4ff")
    mad = mat("#6a4428", "#9a6a40", "#3a2212")
    sombra_suelo(z, 260, 500, 220, 22)
    g = z.lin((40, 0), (480, 0), [(0, mad["l"]), (1, mad["s"])])
    z(f'<rect x="40" y="90" width="440" height="400" rx="14" fill="{g}"/>', f'<rect x="30" y="70" width="460" height="40" rx="10" fill="{mad["b"]}"/>',
      f'<rect x="70" y="160" width="380" height="130" rx="8" fill="{mad["s"]}"/><circle cx="260" cy="225" r="12" fill="#e0c080"/>',
      f'<rect x="70" y="320" width="380" height="130" rx="8" fill="{mad["s"]}"/><circle cx="260" cy="385" r="12" fill="#e0c080"/>')
    z.guardar()
    return _a(n)


def zzz():
    n, w, h = "zzz", 420, 420
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#ffffff")
    for (x, y, s, op) in ((90, 330, 1.0, 1), (210, 210, 0.75, 0.85), (310, 110, 0.55, 0.7)):
        d = f"M{x - 50 * s} {y - 50 * s} L{x + 50 * s} {y - 50 * s} L{x - 50 * s} {y + 50 * s} L{x + 50 * s} {y + 50 * s}"
        z(f'<path d="{d}" stroke="#bfe6ff" stroke-width="{26 * s:.0f}" fill="none" stroke-linejoin="round" stroke-linecap="round" opacity="{op}"/>')
    z.guardar(textura=False)
    return _a(n)


def bg_dormitorio(L, sem=401):
    """Dormitorio a primera hora: pared azulada, ventana con el cielo clareando, luz fría que entra en diagonal."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    ys = 1500 if V else 860
    L.add(L.rect(L.lg((0, "#1a2240"), (0.6, "#2a3460"), (1, "#141a30")), h=ys + 20))
    for k in range(0, w + 60, 60):
        L.add(f'<rect x="{k}" y="0" width="2" height="{ys}" fill="#ffffff" opacity="0.03"/>')
    wx, wy, ww, wh = (w * 0.62, 260, 330, 520) if V else (w * 0.66, 120, 420, 420)
    L.add(f'<rect x="{wx - 14:.0f}" y="{wy - 14}" width="{ww + 28}" height="{wh + 28}" rx="8" fill="#0e1224"/>')
    L.add(f'<rect x="{wx:.0f}" y="{wy}" width="{ww}" height="{wh}" fill="{L.lg((0, "#2a3a7a"), (0.6, "#c87a6a"), (1, "#ffc890"))}"/>')
    for k in range(10):
        L.add(f'<circle cx="{wx + r.uniform(10, ww - 10):.0f}" cy="{wy + r.uniform(10, wh * 0.4):.0f}" r="{r.uniform(1, 2.2):.1f}" fill="#ffffff" opacity="0.7"/>')
    L.add(f'<path d="M{wx:.0f} {wy + wh * 0.8:.0f} L{wx + ww * 0.3:.0f} {wy + wh * 0.7:.0f} L{wx + ww * 0.55:.0f} {wy + wh * 0.78:.0f} L{wx + ww:.0f} {wy + wh * 0.68:.0f} L{wx + ww:.0f} {wy + wh} L{wx:.0f} {wy + wh} Z" fill="#1a1830"/>')
    L.add(f'<rect x="{wx + ww / 2 - 6:.0f}" y="{wy}" width="12" height="{wh}" fill="#0e1224"/><rect x="{wx:.0f}" y="{wy + wh / 2 - 6:.0f}" width="{ww}" height="12" fill="#0e1224"/>')
    L.add(f'<path d="M{wx - 60:.0f} {wy - 30} L{wx - 10:.0f} {wy - 30} L{wx - 20:.0f} {wy + wh + 60} L{wx - 80:.0f} {wy + wh + 60} Z" fill="#3a2a5a" opacity="0.9"/>')
    L.add(f'<path d="M{wx + ww + 10:.0f} {wy - 30} L{wx + ww + 60:.0f} {wy - 30} L{wx + ww + 80:.0f} {wy + wh + 60} L{wx + ww + 20:.0f} {wy + wh + 60} Z" fill="#3a2a5a" opacity="0.9"/>')
    L.add(f'<path d="M{wx:.0f} {wy + wh} L{wx + ww:.0f} {wy + wh} L{wx - w * 0.3:.0f} {ys + 200} L{wx - w * 0.8:.0f} {ys + 200} Z" fill="#ffd8b0" opacity="0.08"/>')
    L.add(f'<rect x="-20" y="{ys}" width="{w + 40}" height="{h - ys + 20}" fill="{L.lg((0, "#3a2a2a"), (1, "#120c10"))}"/>')
    for k in range(16):
        y = ys + (h - ys) * ((k + 1) / 16) ** 1.4
        L.add(f'<path d="M0 {y:.0f} L{w} {y:.0f}" stroke="#0a0608" stroke-width="2" opacity="0.5"/>')
    L.add(L.oscuridad(w / 2, ys - 300, w, h * 0.8, color="#06080e", op=0.5, medio=0.15))
    return {"suelo": ys + 60}


# =========================================================================== 02 · Luna
def _craters(z, cx, cy, R, r, n, cmin, cmax, oscuro="#8a8478", claro="#ffffff"):
    for _ in range(n):
        a, d = r.uniform(0, 2 * math.pi), R * math.sqrt(r.uniform(0, 0.92))
        x, y, s = cx + d * math.cos(a), cy + d * math.sin(a), r.uniform(cmin, cmax)
        z(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{s:.1f}" fill="{oscuro}" opacity="0.45"/>',
          f'<path d="M{x - s * 0.8:.0f} {y + s * 0.3:.0f} A{s:.1f} {s:.1f} 0 0 0 {x + s * 0.6:.0f} {y + s * 0.7:.0f}" stroke="{claro}" stroke-width="{max(1.5, s * 0.18):.1f}" opacity="0.5" fill="none"/>')


def luna(n, oculta=False, sem=7):
    """La Luna llena: cara visible (mares oscuros) o cara oculta (casi sin mares, llena de cráteres)."""
    w = h = 1000
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#cfe0ff")
    cx = cy = 500
    R = 460
    r = random.Random(sem)
    g = z.rad((cx - 150, cy - 170), R * 1.5, [(0, "#fbf8ee"), (0.45, "#d8d2c4"), (0.85, "#8a857a"), (1, "#4a4640")])
    z(f'<circle cx="{cx}" cy="{cy}" r="{R + 30}" fill="#cfe0ff" opacity="0.12"/>', f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{g}"/>')
    clip = z.clip(f"M{cx - R} {cy} A{R} {R} 0 1 0 {cx + R} {cy} A{R} {R} 0 1 0 {cx - R} {cy} Z")
    z(f'<g clip-path="{clip}">')
    if not oculta:
        mares = [(380, 330, 120, 90), (560, 300, 90, 70), (620, 420, 110, 80), (430, 480, 140, 100), (300, 450, 70, 110), (560, 560, 80, 60), (680, 300, 60, 50)]
        for (x, y, a, b) in mares:
            z(f'<ellipse cx="{x}" cy="{y}" rx="{a}" ry="{b}" fill="#6a6a70" opacity="0.55" transform="rotate({r.uniform(-30, 30):.0f} {x} {y})" filter="url(#blur8)"/>')
        _craters(z, cx, cy, R, r, 60, 4, 16)
        z(f'<circle cx="430" cy="760" r="26" fill="#ffffff" opacity="0.6"/>')
        for k in range(10):
            a = math.radians(r.uniform(0, 360))
            z(f'<path d="M430 760 L{430 + 300 * math.cos(a):.0f} {760 + 300 * math.sin(a):.0f}" stroke="#ffffff" stroke-width="4" opacity="0.18"/>')
    else:
        z(f'<ellipse cx="600" cy="640" rx="260" ry="200" fill="#7a7468" opacity="0.35" filter="url(#blur20)"/>',
          f'<ellipse cx="330" cy="300" rx="50" ry="40" fill="#6a6a70" opacity="0.5" filter="url(#blur8)"/>')
        _craters(z, cx, cy, R, r, 230, 5, 30)
        _craters(z, cx, cy, R, r, 14, 30, 62)
    # terminador suave
    gs = z.rad((cx - 200, cy - 220), R * 1.9, [(0, "#000", 0), (0.6, "#000", 0), (1, "#000", 0.55)])
    z(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{gs}"/></g>')
    z(f'<path d="M{cx - R + 40} {cy - 100} A{R - 10} {R - 10} 0 0 1 {cx + 60} {cy - R + 20}" stroke="#ffffff" stroke-width="12" opacity="0.35" fill="none" stroke-linecap="round"/>')
    z.guardar()
    return _a(n)


def sonda_luna3():
    """Sonda soviética de 1959: cuerpo cilíndrico con cúpula, paneles en franja y antenas (sin símbolos)."""
    n, w, h = "sonda_luna3", 760, 520
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#9fc4ff")
    g = z.lin((0, 160), (0, 380), [(0, "#f4f6fa"), (0.4, "#b8c0cc"), (1, "#4a5260")])
    z(f'<rect x="180" y="170" width="400" height="200" rx="40" fill="{g}"/>', f'<ellipse cx="180" cy="270" rx="60" ry="100" fill="#8a929e"/>',
      f'<ellipse cx="580" cy="270" rx="60" ry="100" fill="#d8dee6"/>', '<rect x="200" y="186" width="360" height="22" rx="11" fill="#ffffff" opacity="0.7"/>')
    for k in range(6):
        z(f'<rect x="{230 + k * 55}" y="300" width="40" height="40" fill="#1e3a7a" stroke="#6a9ae0" stroke-width="2"/>')
    for (x0, y0, x1, y1) in ((300, 170, 220, 30), (460, 170, 540, 30), (300, 370, 220, 500), (460, 370, 540, 500), (640, 270, 750, 270)):
        z(f'<path d="M{x0} {y0} L{x1} {y1}" stroke="#c8ccd4" stroke-width="6" stroke-linecap="round"/><circle cx="{x1}" cy="{y1}" r="8" fill="#e8ecf4"/>')
    z('<circle cx="120" cy="270" r="30" fill="#2a3a5a"/><circle cx="112" cy="262" r="10" fill="#9fd0ff"/>')
    z.guardar()
    return _a(n)


def capsula_apolo():
    """Nave de tres tripulantes: cápsula cónica + módulo de servicio cilíndrico con tobera (sin banderas ni letras)."""
    n, w, h = "capsula_apolo", 900, 460
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#9fc4ff")
    gc = z.lin((0, 80), (0, 380), [(0, "#fbfcff"), (0.45, "#c8ccd4"), (1, "#5a6068")])
    z(f'<path d="M80 230 L300 90 L300 370 Z" fill="{gc}"/>', '<path d="M90 226 L295 98" stroke="#ffffff" stroke-width="8" opacity="0.7"/>',
      '<rect x="170" y="190" width="40" height="30" rx="6" fill="#1a2a4a"/><rect x="176" y="194" width="14" height="10" fill="#9fd0ff" opacity="0.7"/>')
    gs = z.lin((0, 90), (0, 370), [(0, "#eef0f4"), (0.5, "#a8aeb8"), (1, "#3a4048")])
    z(f'<rect x="300" y="90" width="400" height="280" fill="{gs}"/>', '<rect x="300" y="100" width="400" height="18" fill="#ffffff" opacity="0.5"/>')
    for k in range(1, 5):
        z(f'<rect x="{300 + k * 80}" y="90" width="6" height="280" fill="#5a6068" opacity="0.6"/>')
    gt = z.lin((700, 0), (880, 0), [(0, "#5a5048"), (1, "#2a2420")])
    z(f'<path d="M700 160 L860 110 L860 350 L700 300 Z" fill="{gt}"/>')
    z.guardar()
    return _a(n)


def aterrizador():
    """Módulo de aterrizaje de cuatro patas con un pequeño vehículo de seis ruedas al lado (sin banderas)."""
    n, w, h = "aterrizador", 1000, 640
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#ffe2b0")
    sombra_suelo(z, 420, 600, 380, 34)
    oro = z.lin((0, 180), (0, 400), [(0, "#ffe8a0"), (0.5, "#d8a03a"), (1, "#6a4810")])
    for (x0, x1) in ((260, 140), (580, 700), (340, 300), (500, 540)):
        z(f'<path d="M{x0} 380 L{x1} 590" stroke="#8a8e96" stroke-width="14" stroke-linecap="round"/><ellipse cx="{x1}" cy="592" rx="34" ry="10" fill="#c8ccd4"/>')
    z(f'<path d="M230 200 L610 200 L640 400 L200 400 Z" fill="{oro}"/>', '<path d="M240 210 L600 210" stroke="#fff4c0" stroke-width="10" opacity="0.7"/>')
    for k in range(6):
        z(f'<path d="M{260 + k * 60} 210 L{250 + k * 64} 395" stroke="#8a6010" stroke-width="3" opacity="0.5"/>')
    z('<rect x="300" y="120" width="240" height="90" rx="10" fill="#d8dce4"/><rect x="320" y="70" width="200" height="60" rx="6" fill="#1e3a7a"/>',
      '<path d="M540 140 L640 60" stroke="#c8ccd4" stroke-width="6"/><circle cx="650" cy="52" r="30" fill="none" stroke="#e8ecf4" stroke-width="6"/>')
    # vehículo
    z('<rect x="760" y="470" width="190" height="70" rx="12" fill="#e8ecf4"/><rect x="770" y="440" width="170" height="30" fill="#1e3a7a"/>',
      '<path d="M840 470 L840 410 L880 400" stroke="#c8ccd4" stroke-width="6" fill="none"/>')
    for x in (780, 855, 930):
        z(f'<circle cx="{x}" cy="560" r="26" fill="#3a3e46"/><circle cx="{x}" cy="560" r="10" fill="#8a8e96"/>')
    z.guardar()
    return _a(n)


def foto_borrosa():
    """Foto antigua, en blanco y negro y con ruido, de la cara oculta (marco de papel, sin texto)."""
    n, w, h = "foto_borrosa", 760, 820
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#fff4dc")
    z('<rect x="50" y="50" width="660" height="720" rx="6" fill="#000" opacity="0.3" transform="translate(12 14)"/>',
      '<rect x="50" y="50" width="660" height="720" rx="6" fill="#efe8d8"/>', '<rect x="90" y="90" width="580" height="580" fill="#121212"/>')
    g = z.rad((330, 330), 330, [(0, "#d8d8d8"), (0.6, "#9a9a9a"), (1, "#3a3a3a")])
    z(f'<circle cx="420" cy="420" r="300" fill="{g}" filter="url(#blur8)"/>', '<ellipse cx="300" cy="300" rx="60" ry="40" fill="#4a4a4a" opacity="0.7" filter="url(#blur8)"/>')
    r = random.Random(11)
    for _ in range(900):
        x, y = r.uniform(90, 670), r.uniform(90, 670)
        z(f'<rect x="{x:.0f}" y="{y:.0f}" width="3" height="3" fill="{r.choice(["#ffffff", "#000000"])}" opacity="{r.uniform(0.1, 0.5):.2f}"/>')
    for k in range(12):
        y = 90 + k * 48
        z(f'<rect x="90" y="{y}" width="580" height="4" fill="#ffffff" opacity="0.12"/>')
    z.guardar(textura=False)
    return _a(n)


# =========================================================================== 03 · Black Friday
def p_poli(n, pj, pose):
    """Policía de pie con gorra (casco del vídeo largo en azul marino) y placa dorada."""
    w, h, u = 520, 940, 108
    z = IP._cuadro(n, w, h, CALLE)
    suelo = h - 25
    Pv = (w / 2, suelo - pie_suelo(u))
    sombra_suelo(z, w / 2, suelo - 6, 1.3 * u)
    if pose == 3:
        br = [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)),
              dict(lado="R", a1=150, a2=165, ah=170, mano=dict(t="plana", dorso=False, pulgar=1, abre=8, pul_ang=45))]
    else:
        br = [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)), dict(lado="R", a1=7, a2=3, mano=dict(t="lado", c=0.45, pal=-1))]
    figura(z, Pv, u, pj, "frente", cab=dict(ex="habla" if pose == 3 else "neutra", ang=2, casco=True), brazos=br,
           piernas=[dict(lado="L", a1=-3, a2=-1, pie=dict(vista="frente")), dict(lado="R", a1=4, a2=1, pie=dict(vista="frente"))])
    bx, by = Pv[0] - 0.42 * u, Pv[1] - 1.45 * u
    z(f'<path d="M{F(bx)} {F(by - 16)} l7 12 14 2 -10 10 3 14 -14 -7 -14 7 3 -14 -10 -10 14 -2 Z" fill="#f2c64a" stroke="#8a6010" stroke-width="2"/>')
    z.guardar()
    return _a(n)


def coche(n, c0, c1, c2):
    """Coche americano de los años sesenta visto de lado, con faros encendidos."""
    w, h = 1100, 440
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#ffd9a0")
    sombra_suelo(z, 550, 410, 500, 30)
    g = z.lin((0, 120), (0, 360), [(0, c0), (0.5, c1), (1, c2)])
    z(f'<path d="M60 300 C60 250 90 230 160 225 L300 215 C350 150 420 120 520 118 L700 118 C780 120 830 160 880 215 L990 230 C1040 238 1060 260 1060 300 L1060 340 L60 340 Z" fill="{g}"/>',
      '<path d="M90 250 L1040 260" stroke="#ffffff" stroke-width="6" opacity="0.45"/>',
      '<path d="M60 330 L1060 330" stroke="#e8ecf4" stroke-width="16"/>')
    gv = z.lin((0, 130), (0, 215), [(0, "#cfe6ff"), (1, "#3a5a8a")])
    z(f'<path d="M330 212 C370 160 430 138 510 136 L600 136 L600 212 Z" fill="{gv}"/><path d="M620 136 L700 136 C760 138 800 170 840 212 L620 212 Z" fill="{gv}"/>')
    z('<ellipse cx="1050" cy="270" rx="16" ry="22" fill="#fff8d0"/><ellipse cx="68" cy="275" rx="12" ry="18" fill="#ff4a3a"/>')
    gl = z.rad((1060, 270), 160, [(0, "#fff4c0", 0.7), (1, "#fff4c0", 0)])
    z(f'<circle cx="1060" cy="270" r="160" fill="{gl}"/>')
    for x in (250, 860):
        z(f'<circle cx="{x}" cy="340" r="66" fill="#141418"/><circle cx="{x}" cy="340" r="34" fill="#c8ccd4"/><circle cx="{x - 8}" cy="332" r="10" fill="#ffffff" opacity="0.7"/>')
    z.guardar()
    return _a(n)


def bolsas():
    """Tres bolsas de compras de papel de colores, con asas (sin marcas ni letras)."""
    n, w, h = "bolsas_compras", 820, 760
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#ffe2b0")
    sombra_suelo(z, 410, 735, 380, 26)
    for (x, y, ww, hh, c) in ((60, 260, 300, 470, ("#ff6a5a", "#d8382a", "#6a1210")), (470, 230, 300, 500, ("#5ad8ff", "#2a8ac8", "#123a6a")),
                              (260, 330, 320, 410, ("#ffd86a", "#e0a92e", "#7a5210"))):
        g = z.lin((x, 0), (x + ww, 0), [(0, c[0]), (0.6, c[1]), (1, c[2])])
        z(f'<path d="M{x + ww * 0.25} {y} C{x + ww * 0.25} {y - 130} {x + ww * 0.75} {y - 130} {x + ww * 0.75} {y}" stroke="{c[2]}" stroke-width="14" fill="none"/>',
          f'<rect x="{x}" y="{y}" width="{ww}" height="{hh}" rx="8" fill="{g}"/>', f'<rect x="{x}" y="{y}" width="{ww}" height="22" fill="#ffffff" opacity="0.35"/>',
          f'<path d="M{x + ww - 30} {y} L{x + ww - 30} {y + hh}" stroke="#000" stroke-width="3" opacity="0.15"/>')
    z.guardar()
    return _a(n)


def grafico_cae():
    """Pizarra de cotización: una línea dorada que sube y se desploma, con monedas cayendo."""
    n, w, h = "grafico_cae", 900, 700
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#ffe2b0")
    g = z.lin((0, 0), (0, 700), [(0, "#1e2a24"), (1, "#0c1410")])
    z('<rect x="30" y="30" width="840" height="560" rx="14" fill="#5a3a22"/>', f'<rect x="50" y="50" width="800" height="520" rx="8" fill="{g}"/>')
    for k in range(1, 6):
        z(f'<path d="M50 {50 + k * 87} L850 {50 + k * 87}" stroke="#ffffff" stroke-width="2" opacity="0.1"/>')
    pts = [(80, 420), (180, 380), (260, 300), (340, 260), (420, 170), (480, 120), (540, 160), (600, 420), (680, 500), (820, 520)]
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    z(f'<path d="{d}" stroke="#ffd86a" stroke-width="12" fill="none" stroke-linejoin="round" stroke-linecap="round"/>',
      '<path d="M540 160 L600 420 L680 500 L820 520" stroke="#ff4a3a" stroke-width="14" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')
    for (x, y) in ((620, 610), (700, 650), (560, 660)):
        z(f'<ellipse cx="{x}" cy="{y}" rx="40" ry="16" fill="#8a5a10"/><ellipse cx="{x}" cy="{y - 6}" rx="40" ry="16" fill="#e0a92e"/><ellipse cx="{x - 10}" cy="{y - 10}" rx="14" ry="5" fill="#fff4b0"/>')
    z.guardar()
    return _a(n)


def balon_americano():
    n, w, h = "balon_americano", 700, 440
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#ffe2b0")
    g = z.rad((280, 160), 380, [(0, "#c87a4a"), (0.5, "#8a4a22"), (1, "#3a1a0a")])
    z(f'<path d="M40 220 C120 60 580 60 660 220 C580 380 120 380 40 220 Z" fill="{g}"/>',
      '<path d="M120 130 C220 80 420 80 520 110" stroke="#ffffff" stroke-width="10" opacity="0.3" fill="none" stroke-linecap="round"/>',
      '<path d="M230 220 L470 220" stroke="#f4efe4" stroke-width="10"/>')
    for k in range(7):
        x = 260 + k * 30
        z(f'<path d="M{x} 200 L{x} 240" stroke="#f4efe4" stroke-width="8" stroke-linecap="round"/>')
    z.guardar()
    return _a(n)


def silbato():
    n, w, h = "silbato", 600, 360
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#ffffff")
    g = z.lin((0, 100), (0, 300), [(0, "#ffffff"), (0.5, "#b8bec8"), (1, "#4a5058")])
    z(f'<path d="M60 150 L330 150 C430 150 500 190 500 240 C500 300 430 330 360 320 C300 312 270 280 260 250 L60 250 Z" fill="{g}"/>',
      '<rect x="140" y="130" width="70" height="30" rx="6" fill="#4a5058"/>', '<circle cx="400" cy="240" r="40" fill="#2a2e34"/>',
      '<path d="M80 165 L320 165" stroke="#ffffff" stroke-width="8" opacity="0.7"/>')
    z.guardar()
    return _a(n)


def monedas_oro():
    """Montón de monedas de oro (sin grabados legibles)."""
    n, w, h = "monedas_oro", 760, 620
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#fff4c0")
    sombra_suelo(z, 380, 590, 330, 30)
    r = random.Random(5)
    pilas = [(230, 6), (380, 9), (530, 5)]
    for (x, k) in pilas:
        for i in range(k):
            y = 560 - i * 34
            z(f'<ellipse cx="{x}" cy="{y + 10}" rx="110" ry="34" fill="#7a5210"/>', f'<rect x="{x - 110}" y="{y - 6}" width="220" height="16" fill="#b8841e"/>',
              f'<ellipse cx="{x}" cy="{y - 6}" rx="110" ry="34" fill="#e0a92e"/>', f'<ellipse cx="{x}" cy="{y - 6}" rx="80" ry="22" fill="none" stroke="#fff0a0" stroke-width="4" opacity="0.6"/>')
        z(f'<ellipse cx="{x - 30}" cy="{560 - (k - 1) * 34 - 14}" rx="34" ry="9" fill="#fffbe0" opacity="0.8"/>')
    z.guardar()
    return _a(n)


def generar(dirsvg):
    T25.generar(dirsvg)
    ilus.OUT = dirsvg
    despertador("a"); despertador("b"); boton_posponer(); mesilla(); zzz()
    cama("cama_duerme", "cerrados"); cama("cama_despierta", "entrecierra", brazo=True)
    T25.p_de_pie("dormilon_pie", DORMILON, 3, "sonrisa", 0, luz=SALA)
    T25.p_de_pie("dormilon_sueno", DORMILON, 0, "cansado", 4, luz=SALA)
    _a(busto("cara_dormilon_sueno", DORMILON, "cansado", ang=5, luz=SALA))
    _a(busto("cara_dormilon_listo", DORMILON, "sonrisa", ang=-3, luz=SALA))
    luna("luna_llena"); luna("luna_oculta", oculta=True, sem=19)
    sonda_luna3(); capsula_apolo(); aterrizador(); foto_borrosa()
    p_poli("policia_para", POLI, 3); p_poli("policia_pie", POLI2, 0)
    _a(busto("cara_policia", POLI, "cansado", ang=3, casco=True, luz=CALLE))
    T25.p_de_pie("compradora", COMPRADORA, 1, "sonrisa", -3, luz=CALLE)
    coche("coche_rojo", "#ff7a6a", "#c8302a", "#5a1210"); coche("coche_azul", "#8ac0ff", "#2a6ab8", "#102a5a"); coche("coche_crema", "#fff4d8", "#e0caa0", "#7a6a48")
    bolsas(); grafico_cae(); monedas_oro(); balon_americano(); silbato()
    L = IE.Lienzo("bg_dormitorio", 1080, 1920, 4101)
    bg_dormitorio(L)
    L.guardar(dirsvg, "bg_dormitorio")
    NOMBRES.append("bg_dormitorio")
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
