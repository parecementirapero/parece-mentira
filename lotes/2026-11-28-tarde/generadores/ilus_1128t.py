"""Ilustraciones del lote 2026-11-28-tarde (Jorge con el agente, adelantado), con el ESTILO DEL VÍDEO LARGO
(DECISIONS 2026-11-26, Jorge). Reutiliza todo el arte anterior (`ilus_1127t.generar`, que a su vez trae el del vídeo
largo y los lotes 25/26/27-tarde) y añade solo las piezas nuevas:
01 el segundo intercalar · 02 por qué no hay estrellas en las fotos de la Luna · 03 la tostada cae del lado de la mantequilla.
Uso: python3 ilus_1128t.py DIR_SVG"""
import importlib.util, math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
LARGO = os.path.join(RAIZ, "lotes", "largo-cueva-500-dias", "generadores")
sys.path.insert(0, RAIZ)
sys.path.insert(0, LARGO)
from motor.biblioteca import ilus  # noqa: E402
import ilus_escenarios as IE  # noqa: E402
from ilus_personajes import Lz, busto, _pj, mat, F, sombra_suelo, PIEL2, PIEL3, mix  # noqa: E402

_spec = importlib.util.spec_from_file_location("ilus_1127t", os.path.join(RAIZ, "lotes", "2026-11-27-tarde", "generadores", "ilus_1127t.py"))
T27 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(T27)
T25 = T27.T25

SALA = dict(luz=(-0.6, -0.8), rim="#fff1d8")
LUNA = dict(luz=(-0.8, -0.6), rim="#ffffff")
NOMBRES = []
FUENTE = "font-family=\"DejaVu Sans Mono, Menlo, monospace\" font-weight=\"bold\""


def _a(n):
    NOMBRES.append(n)
    return n


# =========================================================================== 01 · segundo intercalar
def reloj_digital(n, texto, color="#5dff8a"):
    """Reloj digital grande de sobremesa con la hora en neón (dígitos dibujados como texto monoespaciado)."""
    w, h = 1000, 480
    z = Lz(n, w, h, **SALA)
    sombra_suelo(z, 500, 455, 430, 30)
    c = mat("#2a2e38", "#5a6070", "#0e1016")
    z(f'<rect x="40" y="60" width="920" height="360" rx="46" fill="{z.lin((0, 60), (0, 420), [(0, c["l"]), (0.3, c["b"]), (1, c["s"])])}"/>',
      f'<rect x="80" y="100" width="840" height="280" rx="24" fill="#05070a"/>',
      f'<rect x="80" y="100" width="840" height="280" rx="24" fill="{z.rad((500, 240), 500, [(0, color, 0.18), (1, color, 0)])}"/>',
      f'<text x="500" y="295" text-anchor="middle" font-size="170" {FUENTE} fill="{color}" opacity="0.18">88:88:88</text>',
      f'<text x="500" y="295" text-anchor="middle" font-size="170" {FUENTE} fill="{color}">{texto}</text>',
      f'<text x="500" y="295" text-anchor="middle" font-size="170" {FUENTE} fill="none" stroke="{color}" stroke-width="10" opacity="0.25">{texto}</text>',
      f'<path d="M110 120 Q300 108 520 118" stroke="#ffffff" stroke-width="10" opacity="0.18" fill="none" stroke-linecap="round"/>')
    z.guardar()
    return _a(n)


def reloj_atomico(n="reloj_atomico"):
    """Reloj atómico de laboratorio: armario de metal con una cámara de cristal y una nube de átomos brillante."""
    w, h = 700, 1000
    z = Lz(n, w, h, **SALA)
    sombra_suelo(z, 350, 975, 300, 30)
    c = mat("#c8ccd4", "#ffffff", "#6a7078")
    z(f'<rect x="80" y="120" width="540" height="850" rx="30" fill="{z.lin((80, 0), (620, 0), [(0, c["s"]), (0.35, c["l"]), (1, c["s"])])}"/>',
      f'<rect x="130" y="180" width="440" height="380" rx="20" fill="#0a1020"/>')
    r = random.Random(3)
    for _ in range(60):
        x, y = 350 + r.gauss(0, 50), 370 + r.gauss(0, 50)
        z(f'<circle cx="{F(x)}" cy="{F(y)}" r="{F(r.uniform(3, 8))}" fill="#7df9ff" opacity="{r.uniform(0.4, 1):.2f}"/>')
    z(f'<circle cx="350" cy="370" r="170" fill="{z.rad((350, 370), 170, [(0, "#7df9ff", 0.5), (1, "#7df9ff", 0)])}"/>',
      f'<path d="M140 190 L230 190 L150 550 L140 550 Z" fill="#ffffff" opacity="0.08"/>')
    for k in range(4):
        z(f'<circle cx="{180 + k * 110}" cy="640" r="22" fill="#1a1e26"/><circle cx="{180 + k * 110}" cy="640" r="9" fill="{["#5dff8a", "#ffd23f", "#5dff8a", "#ff5a4a"][k]}"/>')
    for k in range(5):
        z(f'<rect x="150" y="{720 + k * 44}" width="400" height="20" rx="6" fill="#8a929c" opacity="0.6"/>')
    z(f'<path d="M100 140 Q110 520 100 950" stroke="#ffffff" stroke-width="14" opacity="0.4"/>')
    z.guardar()
    return _a(n)


def servidor(n, fallo=False):
    """Armario de servidores con luces; con fallo, luces rojas y una chispa."""
    w, h = 600, 1000
    z = Lz(n, w, h, **SALA)
    sombra_suelo(z, 300, 975, 260, 26)
    c = mat("#1e222a", "#3a404c", "#0a0c10")
    z(f'<rect x="60" y="40" width="480" height="920" rx="18" fill="{z.lin((60, 0), (540, 0), [(0, c["s"]), (0.4, c["l"]), (1, c["s"])])}"/>')
    r = random.Random(7 if fallo else 8)
    for k in range(10):
        y = 80 + k * 86
        z(f'<rect x="90" y="{y}" width="420" height="66" rx="6" fill="#14171d" stroke="#4a505c" stroke-width="2"/>')
        for j in range(6):
            col = "#ff3d3d" if (fallo and r.random() < 0.6) else ("#5dff8a" if r.random() < 0.7 else "#2ff3ff")
            z(f'<circle cx="{120 + j * 26}" cy="{y + 33}" r="7" fill="{col}"/><circle cx="{120 + j * 26}" cy="{y + 33}" r="14" fill="{col}" opacity="0.25"/>')
        for j in range(8):
            z(f'<rect x="{300 + j * 24}" y="{y + 14}" width="14" height="38" rx="3" fill="#0a0c10"/>')
    if fallo:
        z(f'<path d="M420 300 L470 250 L455 300 L520 270 L470 340 L490 320" stroke="#ffd23f" stroke-width="8" fill="none" stroke-linejoin="round"/>',
          f'<circle cx="470" cy="300" r="80" fill="#ff5a3a" opacity="0.25"/>')
    z.guardar()
    return _a(n)


def bg_sala_votacion(L, sem=611):
    """Gran sala de reuniones antigua: paredes claras con columnas, luz cálida y filas de asientos (sin banderas ni logos)."""
    w, h = L.w, L.h
    ys = 1300
    L.add(L.rect(L.lg((0, "#e8dcc4"), (0.6, "#d4c4a4"), (1, "#a89272")), h=ys + 20))
    for k in range(5):
        x = 90 + k * 225
        L.add(f'<rect x="{x - 34}" y="160" width="68" height="{ys - 160}" fill="{L.lg((0, "#fff8e8"), (0.5, "#f0e4cc"), (1, "#c8b494"), x1=0, y1=0, x2=1, y2=0)}"/>',
              f'<rect x="{x - 50}" y="140" width="100" height="30" fill="#e8dcc4"/>')
    for k in range(3):
        x = 200 + k * 340
        L.add(f'<path d="M{x - 90} 1000 L{x - 90} 520 Q{x} 400 {x + 90} 520 L{x + 90} 1000 Z" fill="#9ab4d0" opacity="0.6"/>')
        L.add(L.luz(x, 700, 200, 400, "#fff4d8", 0.5))
    L.add(f'<rect x="-20" y="{ys}" width="{w + 40}" height="{h - ys + 20}" fill="{L.lg((0, "#7a3a2a"), (1, "#3a1810"))}"/>')
    for k in range(4):
        y = ys + 80 + k * 140
        L.add(f'<rect x="-20" y="{y}" width="{w + 40}" height="60" rx="10" fill="#5a2a1e"/><rect x="-20" y="{y}" width="{w + 40}" height="12" fill="#8a4a36"/>')
    L.add(L.oscuridad(w / 2, ys - 300, w, h * 0.8, color="#1a1008", op=0.5, medio=0.12))
    return {}


# =========================================================================== 02 · estrellas en la Luna
def astronauta(n, pose=0):
    """Astronauta con traje blanco, mochila y visera dorada, de pie en la Luna (pose 0: de pie; 1: sujeta una cámara al pecho)."""
    w, h = 560, 1000
    z = Lz(n, w, h, **LUNA)
    sombra_suelo(z, 280, 975, 200, 26)
    t = mat("#eeeeea", "#ffffff", "#9a9a94")
    cx = 280
    # mochila
    z(f'<rect x="{cx - 120}" y="270" width="240" height="300" rx="30" fill="{t["s"]}"/>')
    # piernas
    for s in (-1, 1):
        x = cx + s * 55
        z(f'<path d="M{x - 48} 600 L{x - 54} 900 Q{x} 930 {x + 50} 900 L{x + 48} 600 Z" fill="{z.lin((x - 50, 0), (x + 50, 0), [(0, t["s"]), (0.4, t["l"]), (1, t["b"])])}"/>',
          f'<path d="M{x - 64} 900 L{x + 62} 900 L{x + 70} 960 L{x - 70} 960 Z" fill="#6a6a70"/>',
          f'<path d="M{x - 50} 720 L{x + 50} 720" stroke="{t["s"]}" stroke-width="10"/>')
    # torso
    z(f'<path d="M{cx - 130} 330 Q{cx} 280 {cx + 130} 330 L{cx + 120} 630 Q{cx} 660 {cx - 120} 630 Z" fill="{z.lin((cx - 130, 0), (cx + 130, 0), [(0, t["s"]), (0.4, t["l"]), (1, t["b"])])}"/>',
      f'<rect x="{cx - 70}" y="420" width="140" height="90" rx="12" fill="#c8ccd4" stroke="#7a7e86" stroke-width="4"/>',
      f'<circle cx="{cx - 40}" cy="465" r="10" fill="#ff5a4a"/><circle cx="{cx}" cy="465" r="10" fill="#2a8aff"/><circle cx="{cx + 40}" cy="465" r="10" fill="#5dff8a"/>')
    # brazos
    for s in (-1, 1):
        x = cx + s * 150
        if pose == 1:
            z(f'<path d="M{x} 350 Q{x + s * 30} 480 {cx + s * 60} 540" stroke="{t["b"]}" stroke-width="80" stroke-linecap="round" fill="none"/>')
        else:
            z(f'<path d="M{x} 350 Q{x + s * 30} 480 {x + s * 10} 600" stroke="{t["b"]}" stroke-width="80" stroke-linecap="round" fill="none"/>',
              f'<circle cx="{x + s * 10}" cy="620" r="42" fill="#c8ccd4"/>')
    if pose == 1:
        z(f'<rect x="{cx - 80}" y="500" width="160" height="110" rx="12" fill="#2a2a2e"/><circle cx="{cx}" cy="555" r="38" fill="#0a0a0e" stroke="#8a8a90" stroke-width="8"/>')
    # casco
    z(f'<circle cx="{cx}" cy="220" r="125" fill="{z.rad((cx - 40, 180), 160, [(0, "#ffffff"), (0.7, t["b"]), (1, t["s"])])}"/>',
      f'<path d="M{cx - 95} 210 Q{cx} 120 {cx + 95} 210 Q{cx + 90} 300 {cx} 310 Q{cx - 90} 300 {cx - 95} 210 Z" fill="{z.lin((cx - 90, 140), (cx + 90, 300), [(0, "#ffe9a0"), (0.4, "#d8a030"), (1, "#6a4810")])}"/>',
      f'<path d="M{cx - 70} 190 Q{cx - 20} 150 {cx + 30} 160" stroke="#ffffff" stroke-width="12" opacity="0.7" fill="none" stroke-linecap="round"/>')
    z.guardar()
    return _a(n)


def bg_luna_superficie(L, sem=621, estrellas=False, quemado=False):
    """Suelo lunar gris con cráteres y horizonte cercano; cielo negro (con estrellas si `estrellas`); `quemado` = sobreexpuesto."""
    w, h = L.w, L.h
    yh = 1150
    r = random.Random(sem)
    L.add(L.rect("#000000"))
    if estrellas:
        L.add(L.polvo(260, 0, 0, w, yh, "#ffffff", 2.6, 1.0, sem=sem))
    sue = (("#ffffff", "#f4f4f0", "#e0e0d8") if quemado else ("#b8b6b0", "#8a8884", "#3a3936"))
    L.add(f'<path d="M-20 {yh} Q{w * 0.3} {yh - 30} {w * 0.6} {yh - 10} T{w + 20} {yh - 20} L{w + 20} {h} L-20 {h} Z" fill="{L.lg((0, sue[0]), (0.4, sue[1]), (1, sue[2]))}"/>')
    for _ in range(18):
        x = r.uniform(0, w)
        y = r.uniform(yh + 40, h - 40)
        rx = r.uniform(30, 120) * (0.4 + (y - yh) / (h - yh))
        L.add(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{rx * 0.28:.0f}" fill="#000" opacity="{0.06 if quemado else 0.25}"/>'
              f'<ellipse cx="{x:.0f}" cy="{y + rx * 0.06:.0f}" rx="{rx * 0.8:.0f}" ry="{rx * 0.2:.0f}" fill="#fff" opacity="{0.1 if quemado else 0.15}"/>')
    if quemado:
        L.add(L.rect("#ffffff", op=0.25))
    return {}


def foto_marco(n, estrellas=False):
    """Foto cuadrada con marco blanco: astronauta en la Luna con cielo negro (con o sin estrellas)."""
    w, h = 700, 760
    z = Lz(n, w, h, **SALA)
    z(f'<rect x="20" y="20" width="660" height="720" rx="8" fill="#f4f2ec"/>',
      f'<rect x="60" y="60" width="580" height="580" fill="#000"/>')
    if estrellas:
        r = random.Random(5)
        for _ in range(80):
            z(f'<circle cx="{F(r.uniform(70, 630))}" cy="{F(r.uniform(70, 420))}" r="{F(r.uniform(1, 3.4))}" fill="#fff" opacity="{r.uniform(0.5, 1):.2f}"/>')
    z(f'<path d="M60 460 Q300 430 640 450 L640 640 L60 640 Z" fill="{"#ffffff" if estrellas else z.lin((0, 440), (0, 640), [(0, "#c8c6c0"), (1, "#5a5854")])}"/>',
      f'<g opacity="{0.35 if estrellas else 1}"><circle cx="350" cy="360" r="40" fill="#eeeeea"/><path d="M315 360 Q350 330 385 360" fill="#d8a030"/>'
      f'<rect x="305" y="395" width="90" height="110" rx="20" fill="#eeeeea"/><rect x="315" y="500" width="28" height="70" fill="#eeeeea"/><rect x="357" y="500" width="28" height="70" fill="#eeeeea"/></g>')
    z.guardar()
    return _a(n)


def diafragma(n="diafragma"):
    """Objetivo de cámara visto de frente con el diafragma casi cerrado (poca luz)."""
    w = h = 700
    z = Lz(n, w, h, **SALA)
    z(f'<circle cx="350" cy="350" r="330" fill="{z.rad((300, 300), 380, [(0, "#4a4a50"), (1, "#0a0a0e")])}"/>',
      f'<circle cx="350" cy="350" r="260" fill="#14141a" stroke="#8a8a90" stroke-width="8"/>')
    for k in range(8):
        a = k * math.pi / 4
        x1, y1 = 350 + 250 * math.cos(a), 350 + 250 * math.sin(a)
        x2, y2 = 350 + 60 * math.cos(a + 0.9), 350 + 60 * math.sin(a + 0.9)
        x3, y3 = 350 + 250 * math.cos(a + 0.8), 350 + 250 * math.sin(a + 0.8)
        z(f'<path d="M{F(x1)} {F(y1)} L{F(x2)} {F(y2)} L{F(x3)} {F(y3)} Z" fill="{["#2a2a30", "#34343a"][k % 2]}" stroke="#0a0a0e" stroke-width="3"/>')
    z(f'<circle cx="350" cy="350" r="50" fill="#9ad8ff" opacity="0.5"/>',
      f'<path d="M150 180 Q240 110 330 100" stroke="#ffffff" stroke-width="14" opacity="0.3" fill="none" stroke-linecap="round"/>')
    z.guardar()
    return _a(n)


# =========================================================================== 03 · tostada
def tostada(n, mantequilla=True):
    """Rebanada de pan tostado vista de lado/en perspectiva con la capa de mantequilla amarilla arriba."""
    w, h = 700, 400
    z = Lz(n, w, h, **SALA)
    pan = mat("#d8964a", "#f4c27a", "#8a4e1a")
    z(f'<path d="M60 230 Q40 120 160 110 Q240 40 350 80 Q460 40 540 110 Q660 120 640 230 L630 300 Q350 330 70 300 Z" fill="#6a3a14"/>',
      f'<path d="M85 225 Q70 140 170 132 Q245 72 350 104 Q455 72 530 132 Q630 140 615 225 L605 285 Q350 310 95 285 Z" fill="{z.lin((0, 100), (0, 300), [(0, pan["l"]), (0.5, pan["b"]), (1, pan["s"])])}"/>')
    r = random.Random(2)
    for _ in range(40):
        z(f'<circle cx="{F(r.uniform(130, 570))}" cy="{F(r.uniform(150, 270))}" r="{F(r.uniform(2, 5))}" fill="#7a4418" opacity="0.5"/>')
    if mantequilla:
        z(f'<path d="M150 150 Q250 110 350 128 Q460 108 550 150 Q520 180 470 170 Q400 190 330 170 Q250 188 190 172 Q150 175 150 150 Z" fill="{z.lin((0, 110), (0, 190), [(0, "#fff6b0"), (1, "#f0c838")])}"/>',
          f'<path d="M210 140 Q300 120 380 132" stroke="#ffffff" stroke-width="8" opacity="0.7" fill="none" stroke-linecap="round"/>')
    z.guardar()
    return _a(n)


def mesa(n="mesa_cocina"):
    """Mesa de cocina de madera vista de lado (para posar la tostada en el borde)."""
    w, h = 1000, 800
    z = Lz(n, w, h, **SALA)
    sombra_suelo(z, 500, 780, 460, 30)
    m = mat("#a8683a", "#d8965a", "#5a3218")
    z(f'<rect x="40" y="60" width="920" height="60" rx="10" fill="{z.lin((0, 60), (0, 120), [(0, m["l"]), (1, m["s"])])}"/>',
      f'<path d="M40 70 L960 70" stroke="#ffe0b0" stroke-width="6" opacity="0.6"/>')
    for x in (100, 860):
        z(f'<rect x="{x}" y="120" width="50" height="660" fill="{z.lin((x, 0), (x + 50, 0), [(0, m["s"]), (0.5, m["b"]), (1, m["s"])])}"/>')
    z(f'<rect x="100" y="140" width="800" height="30" fill="{m["s"]}" opacity="0.8"/>')
    z.guardar()
    return _a(n)


def bg_cocina(L, sem=631):
    """Cocina luminosa por la mañana: azulejos claros, ventana con luz, encimera y suelo de baldosas."""
    w, h = L.w, L.h
    ys = 1480
    L.add(L.rect(L.lg((0, "#f6efe0"), (1, "#e4d8c0")), h=ys + 20))
    for x in range(0, w + 60, 60):
        L.add(f'<path d="M{x} 700 L{x} {ys}" stroke="#d8ccb4" stroke-width="2"/>')
    for y in range(700, ys, 60):
        L.add(f'<path d="M0 {y} L{w} {y}" stroke="#d8ccb4" stroke-width="2"/>')
    L.add(f'<rect x="300" y="160" width="480" height="420" rx="10" fill="#9ad0f0"/>',
          f'<path d="M540 160 L540 580 M300 370 L780 370" stroke="#ffffff" stroke-width="14"/>',
          f'<rect x="300" y="160" width="480" height="420" rx="10" fill="none" stroke="#ffffff" stroke-width="18"/>')
    L.add(L.luz(540, 400, 600, 500, "#fff6d8", 0.6))
    L.add(f'<rect x="-20" y="1000" width="{w + 40}" height="40" fill="#8a6a4a"/><rect x="-20" y="1040" width="{w + 40}" height="300" fill="#c8b090"/>')
    L.add(f'<rect x="-20" y="{ys}" width="{w + 40}" height="{h - ys + 20}" fill="{L.lg((0, "#d0c4b0"), (1, "#8a7e6a"))}"/>')
    for k in range(-6, 7):
        L.add(f'<path d="M{w / 2 + k * 90} {ys} L{w / 2 + k * 300} {h}" stroke="#7a6e5a" stroke-width="2" opacity="0.5"/>')
    L.add(L.oscuridad(w / 2, ys - 300, w, h * 0.8, color="#2a2010", op=0.35, medio=0.1))
    return {}


def televisor(n="televisor"):
    """Televisor antiguo de tubo con antena; pantalla con una mesa y una tostada en el aire."""
    w, h = 800, 700
    z = Lz(n, w, h, **SALA)
    sombra_suelo(z, 400, 680, 340, 28)
    c = mat("#7a4a2a", "#b07a4a", "#3a2010")
    z(f'<path d="M300 140 L200 20 M500 140 L600 30" stroke="#3a3a40" stroke-width="8"/>',
      f'<rect x="60" y="140" width="680" height="500" rx="40" fill="{z.lin((60, 0), (740, 0), [(0, c["s"]), (0.4, c["l"]), (1, c["s"])])}"/>',
      f'<rect x="110" y="190" width="460" height="400" rx="40" fill="{z.rad((340, 390), 300, [(0, "#9ad8c8"), (1, "#2a4a44")])}"/>',
      f'<rect x="170" y="440" width="220" height="16" fill="#2a3a36"/><path d="M200 456 L200 560 M360 456 L360 560" stroke="#2a3a36" stroke-width="10"/>',
      f'<path d="M420 330 l60 -20 l14 16 l-60 20 Z" fill="#c88a3a"/>',
      f'<circle cx="650" cy="270" r="30" fill="#2a1a10"/><circle cx="650" cy="360" r="30" fill="#2a1a10"/>',
      f'<path d="M130 210 Q200 200 260 205" stroke="#ffffff" stroke-width="10" opacity="0.3" fill="none" stroke-linecap="round"/>')
    z.guardar()
    return _a(n)


FISICO = _pj(nombre="fisico", peinado="corto", pelo="#8a7a6a", top=mat("#3a4a6a", "#6a7aa0", "#1a2440"), prenda="chaqueta",
             pant=mat("#3a3f4a"), calzado="zapato", bota=mat("#2a2a2e"), edad=45, piel=PIEL3, barba="#8a7a6a")


def generar(dirsvg):
    T27.generar(dirsvg)
    ilus.OUT = dirsvg
    reloj_digital("reloj_595959", "23:59:59"); reloj_digital("reloj_595960", "23:59:60", "#ff5a4a"); reloj_digital("reloj_000000", "00:00:00", "#2ff3ff")
    reloj_atomico(); servidor("servidor"); servidor("servidor_fallo", fallo=True)
    astronauta("astronauta"); astronauta("astronauta_camara", 1)
    foto_marco("foto_luna"); foto_marco("foto_luna_estrellas", True); diafragma()
    tostada("tostada"); tostada("tostada_sin", False); mesa(); televisor()
    T25.p_de_pie("fisico", FISICO, 1, "sonrisa", 2, luz=SALA)
    T25.p_de_pie("amigo_farola", T27.MIRADOR, 0, "sonrisa", -2, luz=SALA)
    _a(busto("cara_fisico", FISICO, "sonrisa", ang=3, luz=SALA))
    for i, (f, k) in enumerate(((bg_sala_votacion, {}), (bg_cocina, {}), (bg_luna_superficie, {}),
                                (bg_luna_superficie, {"estrellas": True, "quemado": True}), (bg_luna_superficie, {"estrellas": True}))):
        nombre = f.__name__ + ("_quemada" if k.get("quemado") else ("_estrellas" if k.get("estrellas") else ""))
        L = IE.Lienzo(nombre, 1080, 1920, 6100 + i * 13)
        f(L, **k)
        L.guardar(dirsvg, nombre)
        NOMBRES.append(nombre)
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
