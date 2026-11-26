"""Ilustraciones del lote 2026-11-25-tarde (Jorge, con el agente), con el ESTILO DEL VÍDEO LARGO de la cueva
(petición de Jorge el 26-11: «me gusta el estilo de dibujo que usaste en el vídeo largo, usa ese estilo»).

Reutiliza todo el arte del vídeo largo (`lotes/largo-cueva-500-dias/generadores/ilus_*.py`: personas con volumen,
cerebro, ojo, móviles, ciudad, estadio, oficina, recuerdos…) y añade piezas nuevas hechas con SUS MISMOS ayudantes
(personas con `figura`/`busto`, objetos con luz principal, luz de borde, degradados y grano; fondos con `Lienzo`).
01 vibración fantasma · 02 medallas olímpicas de arte · 03 la Vía Láctea que ya no vemos.
Uso: python3 ilus_1125t.py DIR_SVG"""
import importlib, importlib.util, math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
LARGO = os.path.join(RAIZ, "lotes", "largo-cueva-500-dias", "generadores")
sys.path.insert(0, RAIZ)
sys.path.insert(0, LARGO)
from motor.biblioteca import ilus  # noqa: E402
import ilus_personajes as IP  # noqa: E402
import ilus_escenarios as IE  # noqa: E402
from ilus_personajes import Lz, figura, busto, _pj, mat, F, sombra_suelo, pie_suelo, DIA, CAVE, PIEL2, PIEL3, PIEL4, mix  # noqa: E402

NOCHE = dict(luz=(-0.4, -0.9), rim="#9fc4ff")
SALA = dict(luz=(-0.6, -0.8), rim="#fff1d8")

MEDICO = _pj(nombre="med1", peinado="corto", pelo="#2a1d14", top=mat("#eef2f5", "#ffffff", "#aab6c2"), prenda="abrigo",
             pant=mat("#3b4a5e"), calzado="zapato", bota=mat("#2a2a2e"), edad=44, piel=PIEL2, barba="#2a1d14")
MEDICA = _pj(nombre="med2", fem=True, peinado="mono", pelo="#5a3420", top=mat("#eef2f5", "#ffffff", "#aab6c2"), prenda="abrigo",
             pant=mat("#3a7a8a", "#5fa8b8", "#1f4650"), calzado="zapato", bota=mat("#e8e8ea"), edad=36, piel=PIEL4, iris="#3d6a5a")
ENFERMERO = _pj(nombre="enf", peinado="rizado", pelo="#1a120c", top=mat("#3a8a9e", "#6ab8cc", "#1d4a56"), prenda="camiseta", manga="corta",
                pant=mat("#3a8a9e", "#6ab8cc", "#1d4a56"), calzado="zapato", bota=mat("#e8e8ea"), edad=29, piel=PIEL3, labio="#8a4a40")
CHICA = _pj(nombre="chica", fem=True, peinado="melena", pelo="#2a1a10", top=mat("#c0392b", "#e66a58", "#6a1712"), prenda="polar",
            pant=mat("#3b5274", "#5f7aa0", "#1f2c42"), vaquero=True, calzado="zapato", bota=mat("#e8e4dc", "#ffffff", "#9a968e"), edad=24, piel=PIEL4,
            iris="#3d6a5a")
CHICO = _pj(nombre="chico", peinado="corto", pelo="#1e1612", top=mat("#2f6fb0", "#5f9fe0", "#173a60"), prenda="polar",
            pant=mat("#2e3440"), calzado="zapato", bota=mat("#2a2a2e"), edad=21, piel=PIEL2)
BARON = _pj(nombre="baron", peinado="peinado60", pelo="#5a4a3a", barba="#5a4a3a", top=mat("#2a2a34", "#4a4a5a", "#121218"), prenda="abrigo",
            pant=mat("#2a2a34", "#4a4a5a", "#121218"), calzado="zapato", bota=mat("#141414", "#3a3a3a", "#0a0a0a"), edad=50,
            piel=dict(b="#e6b593", s="#b47c5a", l="#f6d0b0"))
TIRADOR = _pj(nombre="tirador", peinado="peinado60", pelo="#3a2a1e", top=mat("#6a5a3a", "#9a8458", "#3a2e1a"), prenda="chaqueta",
              pant=mat("#4a4038", "#6e6052", "#2a241e"), calzado="zapato", bota=mat("#2a1d14"), edad=38, barba="#3a2a1e")
MIRADORA = _pj(nombre="mira", fem=True, peinado="coleta", pelo="#3b2618", top=mat("#2a7f9e", "#5fb3cf", "#174a5e"), prenda="polar",
               pant=mat("#2e3440", "#525b6b", "#191d25"), calzado="zapato", bota=mat("#6b4426", "#9a6a40", "#3a2212"), edad=34,
               piel=IP.PIEL_BEA)

NOMBRES = []


def _apunta(n):
    NOMBRES.append(n)
    return n


# =========================================================================== personas
def p_de_pie(n, pj, pose=0, ex="neutra", ang=0, luz=SALA, w=520, h=940, u=108, capas=()):
    """Persona de pie de frente (poses como los voluntarios del vídeo largo)."""
    z = IP._cuadro(n, w, h, luz)
    suelo = h - 25
    Pv = (w / 2, suelo - pie_suelo(u))
    sombra_suelo(z, w / 2, suelo - 6, 1.3 * u)
    poses = [
        [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)), dict(lado="R", a1=7, a2=3, mano=dict(t="lado", c=0.45, pal=-1))],
        [dict(lado="L", obj=(Pv[0] + 0.3 * u, Pv[1] - 1.0 * u), flex=-1, ah=80, mano=dict(t="lado", c=0.5, pal=1)),
         dict(lado="R", obj=(Pv[0] - 0.25 * u, Pv[1] - 1.1 * u), flex=1, ah=-80, mano=dict(t="lado", c=0.5, pal=-1), z=31)],
        # mano derecha al bolsillo del pantalón (nota algo)
        [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)),
         dict(lado="R", obj=(Pv[0] + 0.55 * u, Pv[1] + 0.25 * u), flex=-1, ah=10, mano=dict(t="plana", dorso=True, pulgar=1, abre=4, pul_ang=30), z=31)],
        # brazo derecho en alto (saluda o señala arriba)
        [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)),
         dict(lado="R", a1=150, a2=165, ah=170, mano=dict(t="plana", dorso=False, pulgar=1, abre=8, pul_ang=45))],
    ]
    figura(z, Pv, u, pj, "frente", cab=dict(ex=ex, ang=ang), brazos=poses[pose],
           piernas=[dict(lado="L", a1=-3, a2=-1, pie=dict(vista="frente")), dict(lado="R", a1=4, a2=1, pie=dict(vista="frente"))], capas=capas)
    z.guardar()
    return _apunta(n)


def p_mira_arriba(n, pj, u=112, ang=30, luz=NOCHE):
    """Persona de perfil mirando al cielo, con las manos en los bolsillos de la chaqueta."""
    w, h = 620, 980
    z = IP._cuadro(n, w, h, luz)
    suelo = h - 25
    Pv = (300, suelo - pie_suelo(u) + 0.07 * u)
    sombra_suelo(z, 300, suelo - 6, 1.5 * u)
    figura(z, Pv, u, pj, "perfil", tronco=184, cab=dict(ex="sorpresa", ang=ang),
           brazos=[dict(lado="near", a1=-8, a2=25, ah=40, mano=dict(t="lado", c=0.6, pal=1)),
                   dict(lado="far", a1=-12, a2=20, mano=dict(t="lado", c=0.6, pal=1))],
           piernas=[dict(lado="near", a1=6, a2=2, pie=dict(ang=0)), dict(lado="far", a1=-6, a2=-2, pie=dict(ang=0))])
    z.guardar()
    return _apunta(n)


def caras():
    out = [busto("cara_chica_sorpresa", CHICA, "sorpresa", ang=-3, luz=SALA),
           busto("cara_chica_pensativa", CHICA, "pensativo", ang=4, luz=SALA),
           busto("cara_chico_alerta", CHICO, "entrecierra", ang=-4, luz=SALA),
           busto("cara_mira_estrellas", MIRADORA, "sorpresa", ang=-14, luz=NOCHE),
           busto("cara_baron", BARON, "neutra", ang=3, luz=SALA)]
    for n in out:
        _apunta(n)


# =========================================================================== objetos (mismo método: luz arriba-izq, borde opuesto)
def medalla(n, c0, c1, c2, cinta=("#1f4fa8", "#3a78d8")):
    w, h = 520, 900
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#fff4dc")
    # cinta en V
    gL = z.lin((0, 0), (260, 0), [(0, cinta[0]), (1, cinta[1])])
    z(f'<path d="M110 0 L230 0 L300 470 L210 520 Z" fill="{gL}"/>', f'<path d="M410 0 L290 0 L220 470 L310 520 Z" fill="{cinta[0]}"/>',
      '<path d="M150 0 L170 0 L250 490 L236 494 Z" fill="#ffffff" opacity="0.5"/><path d="M370 0 L350 0 L270 490 L284 494 Z" fill="#ffffff" opacity="0.35"/>',
      '<path d="M110 0 L230 0 L300 470 L210 520 Z" fill="#000" opacity="0.08"/>')
    cx, cy, R = 260, 650, 205
    g = z.rad((cx - 70, cy - 90), R * 1.5, [(0, c0), (0.55, c1), (1, c2)])
    z(f'<circle cx="{cx}" cy="{cy + 10}" r="{R}" fill="#000" opacity="0.25"/>', f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{g}"/>',
      f'<circle cx="{cx}" cy="{cy}" r="{R - 26}" fill="none" stroke="{c2}" stroke-width="8" opacity="0.6"/>',
      f'<circle cx="{cx}" cy="{cy}" r="{R - 32}" fill="none" stroke="{c0}" stroke-width="3" opacity="0.7"/>')
    # relieve: corona de laurel y una figura (sin texto)
    for s in (-1, 1):
        for k in range(7):
            a = math.radians(115 + s * 0 + k * 18) if s < 0 else math.radians(65 - k * 18)
            x, y = cx + math.cos(a) * (R - 62), cy + math.sin(a) * (R - 62)
            z(f'<ellipse cx="{F(x)}" cy="{F(y)}" rx="16" ry="8" fill="{c2}" opacity="0.55" transform="rotate({F(math.degrees(a) + 90 * s)} {F(x)} {F(y)})"/>')
    z(f'<path d="M{cx - 40} {cy + 80} C{cx - 30} {cy + 20} {cx - 10} {cy - 10} {cx} {cy - 40} C{cx + 10} {cy - 10} {cx + 30} {cy + 20} {cx + 40} {cy + 80}" '
      f'fill="none" stroke="{c2}" stroke-width="14" stroke-linecap="round" opacity="0.6"/>',
      f'<circle cx="{cx}" cy="{cy - 70}" r="24" fill="{c2}" opacity="0.55"/>',
      f'<path d="M{cx - 120} {cy - 110} A{R - 40} {R - 40} 0 0 1 {cx + 30} {cy - R + 40}" stroke="#ffffff" stroke-width="16" opacity="0.45" fill="none" stroke-linecap="round"/>',
      f'<path d="M{cx + 150} {cy + 60} A{R - 20} {R - 20} 0 0 1 {cx + 40} {cy + R - 30}" stroke="{z.rim}" stroke-width="8" opacity="0.5" fill="none"/>')
    z(f'<rect x="{cx - 30}" y="{cy - R - 28}" width="60" height="44" rx="10" fill="{c1}"/>')
    z.guardar()
    return _apunta(n)


def caballete():
    """Caballete de madera con un lienzo: un corredor pintado al óleo (sin texto)."""
    n, w, h = "caballete", 620, 980
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#fff1d8")
    mad = mat("#8a5a32", "#c08a52", "#4a2e16")
    sombra_suelo(z, 310, 960, 230, 22)
    for (x0, x1) in ((150, 230), (470, 390), (310, 310)):
        z(f'<path d="M{x0} 955 L{x1} 60" stroke="{mad["s"]}" stroke-width="30" stroke-linecap="round"/>',
          f'<path d="M{x0 - 6} 955 L{x1 - 6} 60" stroke="{mad["b"]}" stroke-width="18" stroke-linecap="round"/>',
          f'<path d="M{x0 - 10} 950 L{x1 - 10} 70" stroke="{mad["l"]}" stroke-width="5" opacity="0.7"/>')
    z(f'<rect x="120" y="640" width="380" height="34" rx="6" fill="{mad["b"]}"/><rect x="120" y="640" width="380" height="8" fill="{mad["l"]}"/>')
    # lienzo
    gx = z.lin((0, 150), (0, 640), [(0, "#f4d9a8"), (0.55, "#e9a86a"), (1, "#6a8a4a")])
    z('<rect x="96" y="132" width="428" height="520" rx="6" fill="#3a2414"/>', f'<rect x="110" y="146" width="400" height="492" fill="{gx}"/>')
    # paisaje de óleo: sol, estadio, pista y corredor en silueta con pinceladas
    r = random.Random(4)
    z('<circle cx="400" cy="260" r="58" fill="#fff2c8" opacity="0.9"/>', '<path d="M110 500 Q310 450 510 500 L510 640 L110 640 Z" fill="#b8553a"/>',
      '<path d="M110 520 Q310 475 510 520" stroke="#f2e0c0" stroke-width="5" fill="none" opacity="0.8"/>')
    for _ in range(140):
        x, y = r.uniform(115, 505), r.uniform(150, 630)
        c = r.choice(["#f8e2b0", "#e3a160", "#c9774a", "#f4c58a", "#8aa060"])
        z(f'<path d="M{x:.0f} {y:.0f} l{r.uniform(8, 22):.0f} {r.uniform(-4, 4):.0f}" stroke="{c}" stroke-width="{r.uniform(3, 7):.1f}" opacity="0.35" stroke-linecap="round"/>')
    # corredor (pinceladas oscuras)
    z('<g stroke="#3a1e12" stroke-linecap="round" fill="none">'
      '<circle cx="270" cy="330" r="22" fill="#3a1e12"/><path d="M265 352 L250 440" stroke-width="26"/>'
      '<path d="M258 370 L300 410 L330 380" stroke-width="13"/><path d="M256 372 L215 400 L200 440" stroke-width="13"/>'
      '<path d="M250 440 L300 480 L310 540" stroke-width="15"/><path d="M250 440 L210 500 L160 505" stroke-width="15"/></g>')
    z('<rect x="110" y="146" width="400" height="492" fill="none" stroke="#000" stroke-width="4" opacity="0.25"/>')
    z.guardar()
    return _apunta(n)


def escultura_caballo():
    """Escultura de bronce: un caballo trotón tirando de un carro ligero, sobre peana de mármol."""
    n, w, h = "escultura_caballo", 900, 760
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#ffe2a8")
    br = mat("#8a5a2a", "#d8a058", "#3a2210")
    gb = z.lin((150, 150), (700, 600), [(0, br["l"]), (0.45, br["b"]), (1, br["s"])])
    sombra_suelo(z, 450, 745, 380, 26)
    gm = z.lin((0, 560), (0, 740), [(0, "#f0ece4"), (1, "#a8a29a")])
    z(f'<path d="M110 600 L790 600 L820 740 L80 740 Z" fill="{gm}"/>', '<path d="M110 600 L790 600 L800 620 L100 620 Z" fill="#ffffff" opacity="0.7"/>',
      '<path d="M200 650 Q300 640 360 690 M560 630 Q640 680 700 660" stroke="#b8b0a6" stroke-width="2" fill="none" opacity="0.7"/>')
    # carro y rueda (detrás)
    z(f'<circle cx="640" cy="500" r="92" fill="none" stroke="{br["s"]}" stroke-width="14"/>')
    for k in range(10):
        a = math.radians(k * 36)
        z(f'<path d="M640 500 L{640 + 88 * math.cos(a):.0f} {500 + 88 * math.sin(a):.0f}" stroke="{br["s"]}" stroke-width="4"/>')
    z(f'<path d="M520 470 L700 440 L720 470 L540 500 Z" fill="{gb}"/>', f'<path d="M300 430 L560 480" stroke="{br["b"]}" stroke-width="10"/>',
      f'<path d="M640 430 C640 380 670 370 690 380 L690 450" fill="{gb}"/>')
    # caballo trotando
    body = "M240 330 C300 290 420 290 470 320 C500 340 505 380 480 410 C440 440 330 445 270 425 C230 410 215 360 240 330 Z"
    neck = "M250 340 C220 300 200 250 185 215 L215 195 C245 230 280 270 300 315 Z"
    head = "M180 200 C165 175 140 160 120 175 C105 186 110 205 128 210 C150 216 165 228 180 240 C195 230 200 212 180 200 Z"
    for d_ in (neck, body, head):
        z(f'<path d="{d_}" fill="{gb}"/>')
    z(f'<path d="M205 205 C225 230 250 270 268 300" stroke="{br["l"]}" stroke-width="8" opacity="0.6" fill="none" stroke-linecap="round"/>',
      f'<path d="M260 320 C320 300 400 300 450 318" stroke="{br["l"]}" stroke-width="10" opacity="0.6" fill="none" stroke-linecap="round"/>',
      f'<path d="M470 330 C510 330 535 360 540 400" stroke="{br["s"]}" stroke-width="16" fill="none" stroke-linecap="round"/>',
      f'<path d="M190 205 L205 175 L215 205" fill="{br["s"]}"/><circle cx="140" cy="186" r="5" fill="#1a0e06"/>')
    patas = [((300, 420), (270, 500), (300, 590)), ((330, 425), (380, 495), (360, 590)), ((440, 420), (470, 500), (430, 590)), ((465, 410), (520, 470), (540, 560))]
    for a, b, c in patas:
        z(f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]} L{c[0]} {c[1]}" stroke="{br["s"]}" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
          f'<path d="M{a[0] - 3} {a[1]} L{b[0] - 3} {b[1]} L{c[0] - 3} {c[1]}" stroke="{br["b"]}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
          f'<ellipse cx="{c[0]}" cy="{c[1] + 6}" rx="16" ry="9" fill="#2a1608"/>')
    # jinete en el carro (silueta de bronce)
    z(f'<path d="M600 440 C590 400 600 370 625 365 C650 362 660 395 655 440 Z" fill="{gb}"/><circle cx="628" cy="345" r="22" fill="{gb}"/>',
      f'<path d="M610 395 L480 360" stroke="{br["b"]}" stroke-width="10" stroke-linecap="round"/>')
    z(f'<path d="M110 600 L80 740" stroke="#ffffff" stroke-width="4" opacity="0.5"/>')
    z.guardar()
    return _apunta(n)


def pergamino():
    """Hoja de poema con renglones (sin letras legibles) y una pluma de escribir."""
    n, w, h = "pergamino", 720, 860
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#fff4dc")
    gp = z.lin((0, 0), (720, 860), [(0, "#fbf1d8"), (0.6, "#efdcae"), (1, "#c9a96e")])
    z('<path d="M80 70 L620 50 C650 300 640 560 660 800 L110 820 C90 560 100 300 80 70 Z" fill="#000" opacity="0.2" transform="translate(12 14)"/>',
      f'<path d="M80 70 L620 50 C650 300 640 560 660 800 L110 820 C90 560 100 300 80 70 Z" fill="{gp}"/>')
    r = random.Random(7)
    y = 170
    for k in range(14):
        x0 = 150 + (40 if k % 4 == 0 else 0)
        x1 = x0 + r.uniform(260, 390)
        if k % 4 == 3:
            y += 30
            continue
        z(f'<path d="M{x0} {y} ' + " ".join(f"Q{x0 + (i + 0.5) * (x1 - x0) / 8:.0f} {y + r.uniform(-6, 6):.0f} {x0 + (i + 1) * (x1 - x0) / 8:.0f} {y}" for i in range(8)) +
          f'" stroke="#4a3220" stroke-width="5" fill="none" opacity="0.75" stroke-linecap="round"/>')
        y += 44
    z('<path d="M480 760 C520 740 560 745 600 760" stroke="#4a3220" stroke-width="5" fill="none" opacity="0.8"/>')
    # pluma
    g = z.lin((420, 600), (700, 200), [(0, "#e8e4dc"), (1, "#ffffff")])
    z(f'<path d="M440 640 C520 520 600 360 690 150 C650 300 600 440 470 650 Z" fill="{g}"/>',
      '<path d="M455 640 L690 150" stroke="#a8a29a" stroke-width="3"/>', '<path d="M440 640 L420 690 L455 650 Z" fill="#2a1e14"/>')
    z.guardar()
    return _apunta(n)


def planos():
    """Planos de arquitectura de un estadio: papel azul con líneas blancas."""
    n, w, h = "planos", 820, 600
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#dff0ff")
    g = z.lin((0, 0), (820, 600), [(0, "#2f6fb8"), (1, "#1a3a72")])
    z('<rect x="30" y="40" width="760" height="520" rx="8" fill="#000" opacity="0.25" transform="translate(10 12)"/>',
      f'<rect x="30" y="40" width="760" height="520" rx="8" fill="{g}"/>')
    for k in range(1, 16):
        z(f'<path d="M{30 + k * 48} 40 L{30 + k * 48} 560" stroke="#ffffff" stroke-width="1" opacity="0.12"/>')
    for k in range(1, 11):
        z(f'<path d="M30 {40 + k * 48} L790 {40 + k * 48}" stroke="#ffffff" stroke-width="1" opacity="0.12"/>')
    z('<g fill="none" stroke="#eaf4ff" stroke-width="5" opacity="0.9">'
      '<rect x="190" y="160" width="440" height="280" rx="140"/><rect x="240" y="200" width="340" height="200" rx="100"/>'
      '<path d="M410 200 L410 400 M240 300 L580 300"/><circle cx="410" cy="300" r="36"/></g>'
      '<g stroke="#eaf4ff" stroke-width="3" opacity="0.7"><path d="M170 470 L650 470 M170 460 L170 480 M650 460 L650 480"/>'
      '<path d="M120 150 L120 450 M110 150 L130 150 M110 450 L130 450"/></g>')
    z('<path d="M30 40 L790 40" stroke="#9fd0ff" stroke-width="4" opacity="0.6"/>')
    z.guardar()
    return _apunta(n)


def diana():
    n, w, h = "diana", 600, 760
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#fff4dc")
    mad = mat("#7a5230", "#a87a4a", "#3a2412")
    sombra_suelo(z, 300, 745, 200, 18)
    z(f'<path d="M210 520 L170 745 M390 520 L430 745" stroke="{mad["b"]}" stroke-width="22" stroke-linecap="round"/>')
    for i, c in enumerate(("#f4efe4", "#1e1e22", "#f4efe4", "#1e1e22", "#d8382a")):
        z(f'<circle cx="300" cy="320" r="{250 - i * 50}" fill="{c}"/>')
    z('<circle cx="300" cy="320" r="250" fill="none" stroke="#8a8478" stroke-width="6"/>',
      '<path d="M120 200 A230 230 0 0 1 300 92" stroke="#ffffff" stroke-width="16" opacity="0.35" fill="none" stroke-linecap="round"/>',
      '<circle cx="312" cy="312" r="10" fill="#120a06"/><circle cx="296" cy="334" r="9" fill="#120a06"/>')
    z.guardar()
    return _apunta(n)


def podio():
    n, w, h = "podio", 900, 520
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#fff4dc")
    sombra_suelo(z, 450, 505, 420, 22)
    for (x, y, ww, c) in ((300, 120, 300, "#f2f0ea"), (30, 230, 270, "#dcd8d0"), (600, 290, 270, "#d2cec6")):
        g = z.lin((x, y), (x + ww, 500), [(0, "#ffffff"), (1, c)])
        z(f'<rect x="{x}" y="{y}" width="{ww}" height="{500 - y}" fill="{g}"/>', f'<rect x="{x}" y="{y}" width="{ww}" height="14" fill="#ffffff"/>',
          f'<rect x="{x + ww - 10}" y="{y}" width="10" height="{500 - y}" fill="#000" opacity="0.08"/>')
    for (cx, cy, c) in ((450, 300, "#e0a92e"), (165, 365, "#b8bcc4"), (735, 395, "#b8743a")):
        z(f'<circle cx="{cx}" cy="{cy}" r="46" fill="{c}"/><circle cx="{cx - 12}" cy="{cy - 12}" r="16" fill="#ffffff" opacity="0.45"/>')
    z.guardar()
    return _apunta(n)


def bolsillo():
    """Primer plano de un bolsillo de vaquero con un teléfono dentro que brilla (vibración)."""
    n, w, h = "bolsillo", 900, 900
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#cfe6ff")
    g = z.lin((0, 0), (900, 900), [(0, "#5a7aa8"), (0.5, "#3b5884"), (1, "#1f3050")])
    z(f'<rect x="0" y="0" width="900" height="900" rx="60" fill="{g}"/>')
    r = random.Random(3)
    for _ in range(260):   # sarga del vaquero
        x, y = r.uniform(0, 900), r.uniform(0, 900)
        z(f'<path d="M{x:.0f} {y:.0f} l14 -14" stroke="{r.choice(["#7a9ac8", "#2a4068"])}" stroke-width="2" opacity="0.35"/>')
    # bolsillo
    gb = z.lin((150, 250), (750, 850), [(0, "#4e6e9c"), (1, "#2a4068")])
    z(f'<path d="M150 260 L750 260 L760 760 Q450 900 140 760 Z" fill="{gb}"/>',
      '<path d="M150 260 L750 260 L760 760 Q450 900 140 760 Z" fill="none" stroke="#e0a04a" stroke-width="6" stroke-dasharray="18 12"/>',
      '<path d="M176 290 L724 290 L732 744 Q450 868 166 744 Z" fill="none" stroke="#e0a04a" stroke-width="5" stroke-dasharray="18 12" opacity="0.8"/>')
    # teléfono marcado bajo la tela y su luz
    z('<rect x="300" y="190" width="300" height="520" rx="46" fill="#14202e" opacity="0.55"/>',
      '<rect x="318" y="205" width="264" height="490" rx="36" fill="#8fd0ff" opacity="0.18"/>')
    gl = z.rad((450, 450), 430, [(0, "#bfe6ff", 0.55), (0.5, "#8fd0ff", 0.15), (1, "#8fd0ff", 0)])
    z(f'<circle cx="450" cy="450" r="430" fill="{gl}"/>')
    z('<path d="M150 260 L750 260" stroke="#9ab8e0" stroke-width="5" opacity="0.6"/>', '<rect x="0" y="0" width="900" height="900" rx="60" fill="none" stroke="#000" stroke-width="10" opacity="0.2"/>')
    z.guardar()
    return _apunta(n)


def farola():
    n, w, h = "farola", 420, 1500
    z = Lz(n, w, h, luz=(0.2, 1.0), rim="#ffc070")
    gl = z.rad((260, 210), 260, [(0, "#ffd890", 0.75), (0.4, "#ffb050", 0.25), (1, "#ffb050", 0)])
    z(f'<circle cx="260" cy="210" r="260" fill="{gl}"/>')
    z('<path d="M120 1490 L120 200 Q120 120 200 120 L260 120" stroke="#1a1a22" stroke-width="26" fill="none" stroke-linecap="round"/>',
      '<path d="M112 1490 L112 205 Q112 130 190 128" stroke="#4a4a5a" stroke-width="6" fill="none" opacity="0.7"/>',
      '<path d="M200 130 L320 130 L300 190 L220 190 Z" fill="#20202a"/>', '<ellipse cx="260" cy="192" rx="44" ry="14" fill="#fff4d0"/>',
      '<path d="M90 1480 L150 1480 L160 1500 L80 1500 Z" fill="#14141a"/>')
    z.guardar()
    return _apunta(n)


def tierra_noche():
    """La Tierra de noche desde el espacio: continentes oscuros salpicados de luces de ciudades."""
    n, w, h = "tierra_noche", 900, 900
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#7ab8ff")
    cx, cy, R = 450, 450, 400
    go = z.rad((cx - 120, cy - 140), R * 1.4, [(0, "#1a2a4a"), (0.7, "#0a1428"), (1, "#03060e")])
    z(f'<circle cx="{cx}" cy="{cy}" r="{R + 22}" fill="#3a7aff" opacity="0.18"/>', f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{go}"/>')
    clip = z.clip(f"M{cx - R} {cy} A{R} {R} 0 1 0 {cx + R} {cy} A{R} {R} 0 1 0 {cx - R} {cy} Z")
    tierra = ("M180 250 C260 180 360 200 420 250 C470 300 440 360 380 380 C330 400 300 460 260 470 C210 480 170 420 160 360 C150 310 150 280 180 250 Z "
              "M470 200 C540 170 640 180 700 230 C760 290 740 360 680 380 C640 395 600 380 570 410 C540 450 560 520 520 560 C470 600 430 560 440 500 "
              "C450 440 420 400 440 340 C450 280 430 230 470 200 Z M300 560 C340 540 390 560 400 620 C410 690 360 760 320 750 C280 740 270 640 300 560 Z")
    z(f'<g clip-path="{clip}"><path d="{tierra}" fill="#131c2a"/>')
    r = random.Random(9)
    pts = []
    for _ in range(900):
        x, y = r.uniform(150, 760), r.uniform(170, 770)
        pts.append((x, y))
    import re as _re
    for (x, y) in pts:
        # solo sobre tierra aproximada: zonas densas en Europa/Norteamérica de este mapa
        dens = 0.0
        if 180 < x < 420 and 230 < y < 400: dens = 0.7
        if 480 < x < 700 and 210 < y < 380: dens = 0.8
        if 440 < x < 560 and 380 < y < 560: dens = 0.25
        if 290 < x < 400 and 560 < y < 740: dens = 0.3
        if r.random() < dens:
            c = r.choice(["#ffd890", "#ffb050", "#fff0c0"])
            z(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.2, 3.4):.1f}" fill="{c}" opacity="{r.uniform(0.5, 1):.2f}"/>')
    for (x, y, s) in ((300, 300, 60), (600, 280, 70), (560, 330, 50), (250, 340, 40)):
        z(f'<circle cx="{x}" cy="{y}" r="{s}" fill="#ffb050" opacity="0.18" filter="url(#blur20)"/>')
    z('</g>')
    z(f'<path d="M{cx - R + 30} {cy - 120} A{R} {R} 0 0 1 {cx + 120} {cy - R + 20}" stroke="#7ab8ff" stroke-width="10" opacity="0.5" fill="none"/>')
    z.guardar()
    return _apunta(n)


def satelite():
    n, w, h = "satelite_obs", 640, 360
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#9fc4ff")
    for x in (20, 420):
        g = z.lin((x, 120), (x + 200, 240), [(0, "#2a4a8a"), (1, "#0e1e44")])
        z(f'<rect x="{x}" y="120" width="200" height="120" rx="6" fill="{g}"/>')
        for k in range(1, 5):
            z(f'<path d="M{x + k * 40} 120 L{x + k * 40} 240" stroke="#6a9ae0" stroke-width="2" opacity="0.6"/>')
        z(f'<path d="M{x} 180 L{x + 200} 180" stroke="#6a9ae0" stroke-width="2" opacity="0.6"/>')
    gc = z.lin((250, 100), (390, 260), [(0, "#f4f0e4"), (0.5, "#d8c890"), (1, "#8a7a4a")])
    z('<path d="M220 180 L420 180" stroke="#9aa2b2" stroke-width="10"/>', f'<rect x="250" y="100" width="140" height="160" rx="16" fill="{gc}"/>',
      '<ellipse cx="320" cy="90" rx="50" ry="18" fill="#e8ecf4"/><path d="M320 90 L320 40" stroke="#c8ccd4" stroke-width="5"/>',
      '<circle cx="320" cy="180" r="18" fill="#2a3a5a"/><circle cx="314" cy="174" r="6" fill="#9fd0ff"/>')
    z.guardar()
    return _apunta(n)


def ondas():
    """Arcos de vibración (para poner a los lados del teléfono)."""
    n, w, h = "ondas_vibra", 900, 500
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#ffffff")
    for s in (-1, 1):
        for k in range(3):
            rr = 120 + k * 70
            x = 450 + s * 180
            z(f'<path d="M{x + s * 0} {250 - rr * 0.6} Q{x + s * rr * 0.45} 250 {x} {250 + rr * 0.6}" stroke="#7df9ff" stroke-width="{16 - k * 4}" '
              f'fill="none" stroke-linecap="round" opacity="{0.9 - k * 0.25}" transform="translate({s * k * 30} 0)"/>')
    z.guardar(textura=False)
    return _apunta(n)


# =========================================================================== fondos (método Lienzo del vídeo largo)
def bg_via_lactea(L, sem=301):
    """Campo oscuro sin luna con la Vía Láctea cruzando el cielo: núcleo dorado, polvo oscuro, millones de estrellas."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    yhz = 1300 if V else 760
    L.add(L.rect(L.lg((0, "#02030a"), (0.55, "#070c22"), (1, "#14204a")), h=yhz + 60))
    ang = -62 if V else -28
    cx, cy = w * 0.5, yhz * 0.5
    for (rx, ry, c, op, f) in ((w * 1.2, 260, "#3a4a8a", 0.35, "blur40"), (w * 1.1, 160, "#c9d4ff", 0.22, "blur40"), (w * 0.9, 120, "#ffe8c0", 0.22, "blur40"), (w * 1.3, 380, "#2a3a7a", 0.25, "blur40"),
                               (w * 0.35, 110, "#ffd090", 0.35, "blur40")):
        L.add(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry}" fill="{c}" opacity="{op}" transform="rotate({ang} {cx:.0f} {cy:.0f})" filter="url(#{f})"/>')
    # polvo oscuro que parte la banda
    for k in range(9):
        t = (k - 4) / 4
        x = cx + math.cos(math.radians(ang)) * t * w * 0.9
        y = cy + math.sin(math.radians(ang)) * t * w * 0.9
        L.add(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(140, 260):.0f}" ry="{r.uniform(10, 22):.0f}" fill="#04050e" opacity="0.22" '
              f'transform="rotate({ang + r.uniform(-12, 12):.0f} {x:.0f} {y:.0f})" filter="url(#blur20)"/>')
    cs = ["#ffffff", "#cfe0ff", "#fff1c8", "#ffd2a0", "#bcd0ff"]
    est = []
    for _ in range(int(2200 * w * yhz / (1080 * 1300))):
        if r.random() < 0.6:
            t = r.uniform(-0.75, 0.75)
            x = cx + math.cos(math.radians(ang)) * t * w * 1.5 + r.gauss(0, 70)
            y = cy + math.sin(math.radians(ang)) * t * w * 1.5 + r.gauss(0, 70)
        else:
            x, y = r.uniform(0, w), r.uniform(0, yhz)
        if y > yhz:
            continue
        est.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(0.5, 1.6):.1f}" fill="{r.choice(cs)}" opacity="{r.uniform(0.3, 1):.2f}"/>')
    L.add("".join(est))
    for _ in range(26):
        x, y = r.uniform(20, w - 20), r.uniform(20, yhz - 100)
        L.add(L.brillo(x, y, 16, 16, "#e8eeff", 0.6), f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.6" fill="#ffffff"/>')
    # sierra y campo
    sp = [(-20, yhz + 20)] + [(x, yhz - 30 - r.uniform(0, 110)) for x in range(0, w + 100, 80)] + [(w + 20, yhz + 20)]
    L.add(f'<path d="{IE.suave(sp, t=0.2)}" fill="#0a1024"/>', L.bruma(yhz, 70, "#2a3a6a", 0.45))
    L.add(f'<rect x="-20" y="{yhz}" width="{w + 40}" height="{h - yhz + 20}" fill="{L.lg((0, "#0c1226"), (1, "#05070e"))}"/>')
    for x in ((w * 0.12, w * 0.86) if V else (w * 0.08, w * 0.3, w * 0.9)):
        L.add(IE._olivo(L, x, yhz + 30, 1.0, r, c_hoja="#070a14", c_luz="#1e2a4a", c_tronco="#05070c"))
    for _ in range(int(w / 8)):
        x, y = r.uniform(0, w), r.uniform(yhz + 20, h)
        sz = r.uniform(1.5, 4) * (1 + (y - yhz) / 400)
        L.add(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{sz:.1f}" ry="{sz * 0.5:.1f}" fill="#020308" opacity="0.6"/>')
    L.add(L.luz(w * 0.5, yhz + 120, w * 0.6, 160, "#5a74b8", 0.15))
    return {"suelo": yhz + (150 if V else 90)}


def bg_cielo_naranja(L, sem=311):
    """La misma ciudad de noche vista de lejos: cúpula de luz anaranjada encima, sin estrellas."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    yb = 1250 if V else 720
    L.add(L.rect(L.lg((0, "#1a1428"), (0.35, "#4a2e3a"), (0.7, "#c0603a"), (0.9, "#f08a4a"), (1, "#ffb070")), h=yb + 40))
    L.add(L.luz(w * 0.5, yb - 80, w * 0.9, 600 if V else 360, "#ff9a50", 0.55))
    L.add(L.polvo(8, 0, 0, w, yb * 0.3, "#ffffff", 1.2, 0.35, sem=sem))   # apenas un par de estrellas
    L.add(IE._edificios(L, r, yb - 40, 60, 130, 120, 420 if V else 260, "#2a1e2e", ["#ffd9a0", "#ffe8b0"], "#201828", 0.1, 1.0, top_luz="#ff9a60"))
    L.add(L.bruma(yb - 60, 160, "#f0905a", 0.5))
    L.add(IE._edificios(L, r, yb + 10, 100, 220, 160, 600 if V else 380, "#120c16", ["#ffd38a", "#ffcf8a", "#fff0c0"], "#0a0810", 0.25, 1.6, top_luz="#ff8a50"))
    L.add(f'<rect x="-20" y="{yb}" width="{w + 40}" height="{h - yb + 20}" fill="{L.lg((0, "#1a1218"), (1, "#060408"))}"/>')
    for k in range(int(w / 180) + 1):
        x = k * 180 + 60
        L.add(L.luz(x, yb + 40, 120, 60, "#ffb060", 0.4))
    L.add(L.oscuridad(w / 2, yb - 300, w, h * 0.8, color="#0a0610", op=0.55, medio=0.12))
    return {"suelo": yb + (120 if V else 80)}


def bg_galeria(L, sem=321):
    """Sala de exposición de los años veinte: pared granate con molduras, focos cálidos y suelo de madera."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    ys = 1320 if V else 780
    L.add(L.rect(L.lg((0, "#3a1418"), (0.6, "#5a2228"), (1, "#2a0e12")), h=ys + 20))
    for k in range(0, w + 80, 80):
        L.add(f'<rect x="{k}" y="0" width="38" height="{ys}" fill="#000" opacity="0.06"/>')
    L.add(f'<rect x="0" y="{ys - 170 if V else ys - 110}" width="{w}" height="14" fill="#c9a26b" opacity="0.7"/>')
    L.add(f'<rect x="0" y="80" width="{w}" height="22" fill="#c9a26b" opacity="0.6"/>')
    for x in ([w * 0.2, w * 0.5, w * 0.8] if V else [w * 0.15, w * 0.38, w * 0.62, w * 0.85]):
        L.add(L.luz(x, 360 if V else 230, 260, 420 if V else 260, "#ffd8a0", 0.45))
        L.add(f'<path d="M{x - 30:.0f} 102 L{x + 30:.0f} 102 L{x + 14:.0f} 150 L{x - 14:.0f} 150 Z" fill="#2a1a10"/>')
    L.add(f'<rect x="-20" y="{ys}" width="{w + 40}" height="{h - ys + 20}" fill="{L.lg((0, "#7a4a28"), (1, "#2a160c"))}"/>')
    for k in range(18):
        y = ys + (h - ys) * ((k + 1) / 18) ** 1.4
        L.add(f'<path d="M0 {y:.0f} L{w} {y:.0f}" stroke="#2a160c" stroke-width="2" opacity="0.5"/>')
    for k in range(-8, 9):
        L.add(f'<path d="M{w / 2 + k * 70:.0f} {ys} L{w / 2 + k * 300:.0f} {h}" stroke="#2a160c" stroke-width="2" opacity="0.4"/>')
    L.add(L.luz(w / 2, ys + 80, w * 0.6, 120, "#ffc080", 0.3))
    L.add(L.oscuridad(w / 2, ys - 300, w * 0.9, h * 0.7, color="#0a0406", op=0.55, medio=0.15))
    return {"suelo": ys + (60 if V else 40)}


FONDOS = [bg_via_lactea, bg_cielo_naranja, bg_galeria]


def generar(dirsvg):
    os.makedirs(dirsvg, exist_ok=True)
    # 1) todo el arte del vídeo largo
    for m in ("ilus_personajes", "ilus_escenarios", "ilus_objetos_cueva", "ilus_objetos_mundo"):
        importlib.import_module(m).generar(dirsvg)
    ilus.OUT = dirsvg
    # 2) piezas nuevas con los mismos ayudantes
    p_de_pie("medico_1", MEDICO, 1, "neutra", 3)
    p_de_pie("medica_2", MEDICA, 0, "sonrisa", -3)
    p_de_pie("enfermero_3", ENFERMERO, 0, "neutra", 2)
    p_de_pie("chica_bolsillo", CHICA, 2, "sorpresa", -4)
    p_de_pie("chico_bolsillo", CHICO, 2, "entrecierra", 4)
    p_de_pie("baron", BARON, 0, "neutra", 2)
    p_de_pie("tirador", TIRADOR, 1, "sonrisa", -2)
    p_de_pie("chica_saluda", CHICA, 3, "sonrisa_d", 0)
    p_mira_arriba("mira_arriba", MIRADORA)
    p_mira_arriba("mira_arriba_b", CHICO, ang=26)
    caras()
    medalla("medalla_oro", "#fff4b0", "#e0a92e", "#8a5a10")
    medalla("medalla_plata", "#ffffff", "#c4c8d0", "#6a7078", cinta=("#a8282e", "#e04a50"))
    medalla("medalla_bronce", "#ffd8a8", "#c07a3a", "#6a3a14", cinta=("#2a7a3a", "#4ab05a"))
    caballete(); escultura_caballo(); pergamino(); planos(); diana(); podio()
    bolsillo(); farola(); tierra_noche(); satelite(); ondas()
    spec = importlib.util.spec_from_file_location("_ilus_1124t_b", os.path.join(RAIZ, "lotes", "2026-11-24-tarde", "generadores", "ilus_1124t.py"))
    m24 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m24)
    ilus.OUT = dirsvg
    m24.banda_sub()
    for i, f in enumerate(FONDOS):
        L = IE.Lienzo(f.__name__, 1080, 1920, 3000 + i * 17)
        f(L)
        L.guardar(dirsvg, f.__name__)
        NOMBRES.append(f.__name__)
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
