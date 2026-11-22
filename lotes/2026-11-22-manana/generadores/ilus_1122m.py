"""Ilustraciones del lote 2026-11-22-manana (Agente 08:00, Nico): 01 el baloncesto empezó con cestas de melocotones,
02 tu sangre viene de estrellas, 03 tus ojos ven al revés (Stratton, 1896).
Uso: python3 ilus_1122m.py DIR_SVG. Ladrillos de motor/biblioteca/ilus.py; reutiliza piezas de lotes anteriores
(ojo, cara de perfil, cerebro, esqueleto, fémur, átomo, estrella de neutrones, martillo) cargándolas por ruta.
Sin logos, marcas, escudos ni personas reales reconocibles: las personas son siluetas a contraluz."""
import importlib.util, math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano, _estrellas_ricas  # noqa: E402


def _mod(rel, nombre):
    s = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, rel))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _p(pts, cerrar=True):
    return "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + (" Z" if cerrar else "")


# ====================================================================== 01 · BALONCESTO 1891
def bg_gimnasio(nombre="bg_gimnasio", lampara=1.0):
    """Gimnasio de 1891: pared de ladrillo, ventanales altos con nieve, galería con barandilla de madera a media altura,
    suelo de tablas en perspectiva y luz cálida de lámparas."""
    r = random.Random(3)
    d = (lg(f"{nombre}_p", (0, "#5a3326"), (1, "#3a1f18")) + lg(f"{nombre}_s", (0, "#a8743e"), (1, "#5e3a1c"))
         + lg(f"{nombre}_v", (0, "#cfe0f4"), (1, "#8aa6c8")) + lg(f"{nombre}_g", (0, "#8a5a2e"), (1, "#5a3818"))
         + rg(f"{nombre}_l", (0, "#ffd88a", 0.55 * lampara), (1, "#ffd88a", 0)))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_p)"/>']
    for y in range(0, 1240, 34):  # ladrillos
        off = 0 if (y // 34) % 2 else 40
        for x in range(-80 + off, 1100, 80):
            b.append(f'<rect x="{x + 2}" y="{y + 2}" width="76" height="30" fill="#6a3a2a" opacity="{r.uniform(0.25, 0.6):.2f}"/>')
    for x in (120, 440, 760):  # ventanales con nieve
        b += [f'<rect x="{x}" y="120" width="200" height="420" rx="100" fill="#2a1a14"/>',
              f'<rect x="{x + 14}" y="134" width="172" height="392" rx="86" fill="url(#{nombre}_v)"/>',
              f'<path d="M{x + 100} 134 V526 M{x + 14} 330 H{x + 186}" stroke="#2a1a14" stroke-width="10"/>',
              f'<path d="M{x + 14} 500 q40 -24 86 -8 q44 -18 86 6 V526 H{x + 14} Z" fill="#ffffff"/>']
    # galería (balcón) con barandilla: la barandilla inferior queda a «tres metros» del suelo
    b += [f'<rect y="560" width="1080" height="130" fill="url(#{nombre}_g)"/>',
          '<rect y="560" width="1080" height="16" fill="#c08a4a"/>', '<rect y="676" width="1080" height="22" fill="#3a2410"/>']
    for x in range(10, 1080, 46):
        b.append(f'<rect x="{x}" y="580" width="16" height="96" rx="6" fill="#b07a40"/><rect x="{x}" y="580" width="5" height="96" fill="#e0aa66" opacity="0.6"/>')
    b += ['<rect y="698" width="1080" height="560" fill="#2a1610" opacity="0.35"/>',
          f'<path d="M0 1250 H1080 V1920 H0 Z" fill="url(#{nombre}_s)"/>']
    for k in range(-14, 15):  # tablas del suelo en perspectiva
        b.append(f'<path d="M{540 + k * 40} 1250 L{540 + k * 150} 1920" stroke="#3a2410" stroke-width="3" opacity="0.6"/>')
    for k, y in enumerate([1290, 1350, 1440, 1560, 1720]):
        b.append(f'<path d="M0 {y} H1080" stroke="#3a2410" stroke-width="{2 + k}" opacity="0.35"/>')
    b += ['<path d="M0 1250 H1080" stroke="#1a0e08" stroke-width="10"/>',
          f'<ellipse cx="540" cy="420" rx="620" ry="520" fill="url(#{nombre}_l)"/>',
          *[f'<g><path d="M{x} 0 V60" stroke="#222" stroke-width="4"/><circle cx="{x}" cy="78" r="22" fill="#ffe8a8"/>'
            f'<circle cx="{x}" cy="78" r="70" fill="#ffd88a" opacity="{0.35 * lampara:.2f}" filter="url(#blur20)"/></g>' for x in (280, 800)],
          grano()]
    guardar(nombre, "".join(b), defs=d)


def bg_nieve_noche(nombre="bg_nieve_noche"):
    """Exterior de un edificio de ladrillo del siglo XIX en una noche de nieve, con las ventanas encendidas."""
    r = random.Random(11)
    d = lg(f"{nombre}_c", (0, "#0c1430"), (1, "#3a4a72")) + lg(f"{nombre}_e", (0, "#7a3a2a"), (1, "#4a2018"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>', _estrellas_ricas(19, n_peq=90, n_med=6, n_bri=1),
         '<path d="M0 760 L180 640 L360 760 L540 600 L760 760 L940 650 L1080 720 V1400 H0 Z" fill="#1a2240" opacity="0.8"/>',
         f'<rect x="140" y="700" width="800" height="760" fill="url(#{nombre}_e)"/>',
         '<path d="M110 700 L540 470 L970 700 Z" fill="#3a2a2a"/>', '<path d="M110 700 L540 470 L970 700" stroke="#ffffff" stroke-width="22" fill="none" opacity="0.9"/>',
         '<rect x="500" y="300" width="80" height="220" fill="#4a2018"/>', '<path d="M490 300 H590" stroke="#ffffff" stroke-width="18"/>']
    for fila in range(3):
        for col in range(5):
            x, y = 190 + col * 150, 760 + fila * 210
            if fila == 2 and col == 2:
                b.append(f'<rect x="{x - 10}" y="{y - 20}" width="120" height="250" rx="50" fill="#2a1408"/><rect x="{x + 4}" y="{y - 6}" width="92" height="236" rx="44" fill="#ffcf7a"/>')
                continue
            b += [f'<rect x="{x}" y="{y}" width="100" height="150" rx="40" fill="#ffd88a"/>',
                  f'<rect x="{x}" y="{y}" width="100" height="150" rx="40" fill="#ffb84a" opacity="{r.uniform(0.1, 0.5):.2f}"/>',
                  f'<path d="M{x + 50} {y} V{y + 150} M{x} {y + 75} H{x + 100}" stroke="#4a2018" stroke-width="6"/>',
                  f'<rect x="{x - 8}" y="{y + 146}" width="116" height="14" rx="6" fill="#ffffff"/>',
                  f'<ellipse cx="{x + 50}" cy="{y + 75}" rx="110" ry="120" fill="#ffd88a" opacity="0.10" filter="url(#blur20)"/>']
    b += ['<path d="M0 1400 Q300 1360 540 1390 T1080 1380 V1920 H0 Z" fill="#e8eef8"/>',
          '<path d="M0 1480 Q400 1440 1080 1500 V1920 H0 Z" fill="#cfd8ea"/>',
          *[f'<ellipse cx="{r.uniform(0, 1080):.0f}" cy="{r.uniform(1420, 1900):.0f}" rx="{r.uniform(40, 140):.0f}" ry="8" fill="#ffffff" opacity="0.6"/>' for _ in range(14)],
          '<ellipse cx="540" cy="1440" rx="300" ry="40" fill="#ffcf7a" opacity="0.25" filter="url(#blur20)"/>', grano()]
    guardar(nombre, "".join(b), defs=d)


def _mimbre(x0, y0, x1, y1, xb0, xb1, yb, filas=9, sem=1):
    """Tejido de mimbre entre la boca (x0..x1 en y0) y la base (xb0..xb1 en yb)."""
    r = random.Random(sem)
    out = []
    for i in range(filas + 1):
        u = i / filas
        y = y0 + (yb - y0) * u
        xa, xc = x0 + (xb0 - x0) * u, x1 + (xb1 - x1) * u
        col = "#e0a85a" if i % 2 else "#c88a40"
        out.append(f'<path d="M{xa:.0f} {y:.0f} Q{(xa + xc) / 2:.0f} {y + 26:.0f} {xc:.0f} {y:.0f}" stroke="{col}" stroke-width="{(yb - y0) / filas * 0.8:.0f}" fill="none" stroke-linecap="round"/>')
        out.append(f'<path d="M{xa:.0f} {y - 6:.0f} Q{(xa + xc) / 2:.0f} {y + 18:.0f} {xc:.0f} {y - 6:.0f}" stroke="#ffe2a8" stroke-width="3" fill="none" opacity="0.5"/>')
    for k in range(12):  # varillas verticales
        u = k / 11
        out.append(f'<path d="M{x0 + (x1 - x0) * u:.0f} {y0:.0f} L{xb0 + (xb1 - xb0) * u:.0f} {yb:.0f}" stroke="#8a5a24" stroke-width="5" opacity="{0.55 + r.uniform(0, 0.3):.2f}"/>')
    return out


def cesta(nombre="cesta", fondo=True):
    """Cesta de melocotones de mimbre vista de frente y un poco desde arriba (boca elíptica). Sin fondo: se ve el hueco."""
    w, h = 560, 520
    d = rg(f"{nombre}_i", (0, "#3a2410", 1), (1, "#1a0e06", 1)) + lg(f"{nombre}_b", (0, "#f0c070"), (1, "#a8722e"))
    b = ['<ellipse cx="280" cy="490" rx="190" ry="24" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<path d="M40 110 L110 470 Q280 500 450 470 L520 110 Z" fill="#b07a36"/>',
         *_mimbre(44, 120, 516, 120, 112, 448, 462, sem=2 if fondo else 3),
         '<path d="M40 110 L110 470 Q280 500 450 470 L520 110" stroke="#5a3814" stroke-width="6" fill="none" opacity="0.6"/>',
         '<ellipse cx="280" cy="110" rx="246" ry="70" fill="url(#%s_i)"/>' % nombre]
    if not fondo:  # se ve la luz por el hueco
        b.append('<ellipse cx="280" cy="140" rx="150" ry="36" fill="#ffe8b0" opacity="0.85"/>')
        b.append('<ellipse cx="280" cy="140" rx="150" ry="36" fill="none" stroke="#7a4a1a" stroke-width="10"/>')
    else:
        b.append('<ellipse cx="280" cy="150" rx="160" ry="34" fill="#6a4218" opacity="0.8"/>')
    b += [f'<ellipse cx="280" cy="110" rx="250" ry="72" fill="none" stroke="url(#{nombre}_b)" stroke-width="20"/>',
          '<path d="M60 100 Q280 30 500 100" stroke="#fff2c8" stroke-width="5" fill="none" opacity="0.6"/>']
    guardar(nombre, "".join(b), w, h, d)


def cesta_frente(nombre="cesta_frente"):
    """La boca de la cesta (solo el aro delantero) para poner por ENCIMA del balón: así el balón queda «dentro»."""
    w, h = 560, 520
    d = lg(f"{nombre}_b", (0, "#f0c070"), (1, "#a8722e"))
    b = ['<path d="M40 110 L110 470 Q280 500 450 470 L520 110 Q280 190 40 110 Z" fill="#b07a36"/>',
         *_mimbre(44, 150, 516, 150, 112, 448, 462, sem=2),
         f'<path d="M30 110 Q280 192 530 110" stroke="url(#{nombre}_b)" stroke-width="20" fill="none" stroke-linecap="round"/>']
    guardar(nombre, "".join(b), w, h, d)


def fondo_cesta(nombre="fondo_cesta"):
    """El fondo redondo de mimbre suelto (se cae al quitarlo)."""
    w, h = 360, 140
    b = ['<ellipse cx="180" cy="70" rx="170" ry="56" fill="#a8722e"/>',
         *[f'<ellipse cx="180" cy="70" rx="{170 - k * 22}" ry="{56 - k * 7}" fill="none" stroke="{"#e0a85a" if k % 2 else "#8a5a24"}" stroke-width="9"/>' for k in range(7)],
         '<path d="M20 60 Q180 0 340 60" stroke="#ffe2a8" stroke-width="4" fill="none" opacity="0.6"/>']
    guardar(nombre, "".join(b), w, h)


def balon_cuero(nombre="balon_cuero"):
    """Balón de fútbol antiguo de cuero marrón con cordones (como el de 1891)."""
    w = h = 400
    d = rg(f"{nombre}_g", (0, "#e8a868", 1), (0.55, "#a8622e", 1), (1, "#4a2410", 1), cx=0.38, cy=0.32, r=0.7)
    b = ['<circle cx="200" cy="200" r="190" fill="url(#%s_g)"/>' % nombre,
         '<path d="M30 160 Q200 120 370 160 M40 260 Q200 300 360 260 M200 10 Q150 200 200 390" stroke="#3a1a08" stroke-width="6" fill="none" opacity="0.7"/>',
         '<path d="M200 70 V170" stroke="#f4e2c0" stroke-width="10"/>',
         *[f'<path d="M184 {y} H216" stroke="#f4e2c0" stroke-width="7" stroke-linecap="round"/>' for y in range(80, 170, 16)],
         '<ellipse cx="130" cy="110" rx="60" ry="34" fill="#ffffff" opacity="0.25" transform="rotate(-30 130 110)"/>',
         '<circle cx="200" cy="200" r="190" fill="none" stroke="#2a1206" stroke-width="6"/>']
    guardar(nombre, "".join(b), w, h, d)


def balon_moderno(nombre="balon_moderno"):
    """Balón de baloncesto actual, naranja con costuras negras (genérico, sin marca)."""
    w = h = 400
    d = rg(f"{nombre}_g", (0, "#ffb060", 1), (0.6, "#e8661e", 1), (1, "#8a3206", 1), cx=0.38, cy=0.32, r=0.7)
    b = ['<circle cx="200" cy="200" r="190" fill="url(#%s_g)"/>' % nombre,
         '<path d="M10 200 H390 M200 10 V390 M60 64 Q200 200 60 336 M340 64 Q200 200 340 336" stroke="#1a0a04" stroke-width="7" fill="none"/>',
         '<ellipse cx="130" cy="110" rx="60" ry="34" fill="#ffffff" opacity="0.22" transform="rotate(-30 130 110)"/>']
    guardar(nombre, "".join(b), w, h, d)


def canasta_moderna(nombre="canasta_moderna"):
    """Canasta de hoy: tablero blanco con cuadro, aro naranja y red."""
    w, h = 640, 760
    b = ['<rect x="300" y="380" width="40" height="380" fill="#5a6270"/>',
         '<rect x="40" y="20" width="560" height="380" rx="10" fill="#f4f6f8" stroke="#2a3038" stroke-width="10"/>',
         '<rect x="210" y="180" width="220" height="170" fill="none" stroke="#e8461e" stroke-width="10"/>',
         '<rect x="60" y="40" width="200" height="340" fill="#ffffff" opacity="0.5"/>',
         '<path d="M190 420 L240 640 H400 L450 420" stroke="#ffffff" stroke-width="5" fill="none"/>',
         *[f'<path d="M{190 + k * 26} 420 L{240 + k * 16} 640" stroke="#ffffff" stroke-width="4" opacity="0.85"/>' for k in range(11)],
         *[f'<path d="M{190 + k * 26} 420 L{450 - (10 - k) * 26 + 0} 640" stroke="#ffffff" stroke-width="3" opacity="0.5"/>' for k in range(11)],
         '<ellipse cx="320" cy="420" rx="134" ry="26" fill="none" stroke="#ff6a1e" stroke-width="14"/>']
    guardar(nombre, "".join(b), w, h)


def escalera(nombre="escalera"):
    w, h = 300, 1100
    d = lg(f"{nombre}_m", (0, "#d8a060"), (1, "#8a5a24"), x2=1, y2=0)
    b = [f'<rect x="20" y="0" width="34" height="1100" rx="10" fill="url(#{nombre}_m)"/>', f'<rect x="246" y="0" width="34" height="1100" rx="10" fill="url(#{nombre}_m)"/>',
         *[f'<rect x="40" y="{60 + k * 110}" width="220" height="26" rx="8" fill="#b07a40"/><rect x="40" y="{60 + k * 110}" width="220" height="7" fill="#f0c888" opacity="0.7"/>' for k in range(10)]]
    guardar(nombre, "".join(b), w, h, d)


def palo(nombre="palo"):
    w, h = 120, 1300
    b = ['<rect x="44" y="60" width="28" height="1240" rx="12" fill="#a87a40"/>', '<rect x="48" y="60" width="8" height="1240" fill="#e8c088" opacity="0.6"/>',
         '<path d="M58 70 Q58 10 100 14" stroke="#6a6a72" stroke-width="12" fill="none" stroke-linecap="round"/>']
    guardar(nombre, "".join(b), w, h)


def hoja_reglas(nombre="hoja_reglas"):
    """Dos hojas clavadas en la pared con trece reglas numeradas (líneas, sin texto real)."""
    w, h = 620, 820
    d = lg(f"{nombre}_p", (0, "#fbf3dc"), (1, "#e2d0a4"))
    b = ['<rect x="30" y="30" width="560" height="760" fill="#000" opacity="0.3" filter="url(#blur8)"/>',
         f'<rect x="20" y="16" width="560" height="760" fill="url(#{nombre}_p)" stroke="#a88a5a" stroke-width="3"/>',
         '<rect x="140" y="50" width="320" height="26" rx="6" fill="#3a2a1a"/>']
    r = random.Random(4)
    for k in range(13):
        y = 120 + k * 50
        b.append(f'<circle cx="70" cy="{y + 6}" r="13" fill="#7a2a1a"/>')
        b.append(f'<rect x="100" y="{y}" width="{r.uniform(260, 440):.0f}" height="12" rx="6" fill="#4a3a2a" opacity="0.75"/>')
    b.append('<circle cx="300" cy="28" r="12" fill="#6a6a72"/>')
    guardar(nombre, "".join(b), w, h, d)


def _silueta_hombre_1890(x, y, s=1.0, col="#1a1410", luz="#ffcf7a", bigote=True, perfil=1):
    """Hombre de traje de 1890 a contraluz (de pie, de perfil), con luz de borde. Sin rasgos reconocibles."""
    f = perfil
    def P(px, py): return f"{x + px * s * f:.0f} {y + py * s:.0f}"
    cuerpo = (f"M{P(-70, 0)} L{P(-80, -360)} Q{P(-90, -560)} {P(-40, -600)} L{P(40, -600)} Q{P(95, -560)} {P(80, -360)} L{P(70, 0)} Z")
    cabeza = f"M{P(-50, -640)} Q{P(-56, -760)} {P(4, -770)} Q{P(70, -760)} {P(66, -690)} L{P(84, -660)} L{P(62, -650)} Q{P(56, -600)} {P(10, -604)} L{P(-30, -600)} Z"
    out = [f'<path d="{cuerpo}" fill="{col}"/>', f'<path d="{cabeza}" fill="{col}"/>',
           f'<path d="M{P(80, -360)} Q{P(95, -560)} {P(40, -600)}" stroke="{luz}" stroke-width="{5 * s:.1f}" fill="none" opacity="0.9"/>',
           f'<path d="M{P(66, -690)} L{P(84, -660)} L{P(62, -650)}" stroke="{luz}" stroke-width="{4 * s:.1f}" fill="none" opacity="0.9"/>',
           f'<path d="M{P(4, -770)} Q{P(70, -760)} {P(66, -690)}" stroke="{luz}" stroke-width="{5 * s:.1f}" fill="none" opacity="0.9"/>',
           f'<path d="M{P(-20, -600)} L{P(10, -540)} L{P(40, -600)}" fill="#e8e0d0" opacity="0.85"/>']
    if bigote:
        out.append(f'<path d="M{P(60, -648)} Q{P(80, -640)} {P(88, -628)}" stroke="{col}" stroke-width="{12 * s:.1f}" stroke-linecap="round" fill="none"/>')
    return out


def profesor(nombre="profesor"):
    """El profesor de 1891 a contraluz junto a la ventana (silueta genérica, sin cara)."""
    w, h = 420, 820
    b = ['<ellipse cx="210" cy="800" rx="150" ry="18" fill="#000" opacity="0.45" filter="url(#blur8)"/>', *_silueta_hombre_1890(200, 800, 1.0)]
    guardar(nombre, "".join(b), w, h)


def jugador(nombre, camisa, luz="#ffd88a", pose=0):
    """Jugador de 1891 (camisa de manga larga y pantalón largo), silueta con volumen y luz de borde. pose 0 = salta con brazos arriba."""
    w, h = 320, 640
    sh = {0: (-40, -20), 1: (30, 60)}[pose]
    b = ['<ellipse cx="160" cy="626" rx="90" ry="12" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         f'<path d="M120 380 L96 620 H134 L160 430 L186 620 H224 L200 380 Z" fill="#2a2420"/>',
         f'<path d="M106 200 Q160 180 214 200 L224 390 H96 Z" fill="{camisa}"/>',
         f'<path d="M214 200 L224 390" stroke="{luz}" stroke-width="5" opacity="0.8"/>',
         f'<path d="M110 210 L{70 + sh[0]} {110 + sh[1]}" stroke="{camisa}" stroke-width="34" stroke-linecap="round"/>',
         f'<path d="M210 210 L{250 - sh[0]} {110 + sh[1]}" stroke="{camisa}" stroke-width="34" stroke-linecap="round"/>',
         f'<circle cx="{70 + sh[0]}" cy="{100 + sh[1]}" r="18" fill="#d8a07a"/><circle cx="{250 - sh[0]}" cy="{100 + sh[1]}" r="18" fill="#d8a07a"/>',
         '<circle cx="160" cy="150" r="46" fill="#d8a07a"/>', '<path d="M114 140 Q160 90 206 140 Q190 112 160 110 Q130 112 114 140 Z" fill="#3a2a1a"/>',
         f'<path d="M200 130 Q212 160 196 186" stroke="{luz}" stroke-width="4" fill="none" opacity="0.8"/>']
    guardar(nombre, "".join(b), w, h)


def pizarra(nombre="pizarra"):
    w, h = 700, 460
    b = ['<rect x="10" y="10" width="680" height="440" rx="12" fill="#6a4220"/>', '<rect x="34" y="34" width="632" height="392" fill="#1e3a2e"/>',
         '<rect x="34" y="34" width="632" height="392" fill="#ffffff" opacity="0.05" filter="url(#grano)"/>',
         '<path d="M80 380 Q200 360 300 390 M420 380 Q520 370 620 392" stroke="#ffffff" stroke-width="4" opacity="0.15" fill="none"/>']
    guardar(nombre, "".join(b), w, h)


def copo(nombre="copo"):
    w = h = 400
    b = []
    for k in range(6):
        a = k * 60
        b.append(f'<g transform="rotate({a} 200 200)"><path d="M200 200 V30 M200 90 L160 60 M200 90 L240 60 M200 140 L170 115 M200 140 L230 115" '
                 f'stroke="#e8f6ff" stroke-width="14" stroke-linecap="round" fill="none"/></g>')
    b.append('<circle cx="200" cy="200" r="24" fill="#ffffff"/>')
    guardar(nombre, '<g filter="url(#sombra)">' + "".join(b) + "</g>", w, h)


def clavo(nombre="clavo"):
    w, h = 120, 300
    b = ['<rect x="52" y="40" width="16" height="250" fill="#8a8e96"/>', '<path d="M52 290 L60 300 L68 290 Z" fill="#8a8e96"/>',
         '<ellipse cx="60" cy="40" rx="40" ry="14" fill="#a8acb4"/>', '<rect x="54" y="40" width="5" height="250" fill="#e0e4ea" opacity="0.6"/>']
    guardar(nombre, "".join(b), w, h)


def melocoton(nombre="melocoton"):
    """Melocotón con su piel de dos tonos, surco y una hoja."""
    w, h = 300, 300
    d = rg(f"{nombre}_g", (0, "#ffd08a", 1), (0.55, "#ff8a4a", 1), (1, "#c8402a", 1), cx=0.38, cy=0.36, r=0.68)
    b = [f'<circle cx="150" cy="160" r="128" fill="url(#{nombre}_g)"/>',
         '<path d="M150 40 Q120 160 150 286" stroke="#b8402a" stroke-width="6" fill="none" opacity="0.5"/>',
         '<ellipse cx="100" cy="110" rx="36" ry="22" fill="#ffffff" opacity="0.3" transform="rotate(-30 100 110)"/>',
         '<path d="M150 40 Q190 0 240 20 Q200 60 150 40 Z" fill="#4a9a3a"/>', '<path d="M150 40 V20" stroke="#5a3a1a" stroke-width="6"/>']
    guardar(nombre, "".join(b), w, h, d)


# ====================================================================== 02 · POLVO DE ESTRELLAS
def supernova(nombre="supernova", c1="#ffffff", c2="#ffd27a", c3="#ff5a3a", c4="#7a3aff", sem=7):
    """Explosión: núcleo blanco, rayos, onda de choque en anillo y jirones de gas de colores."""
    r = random.Random(sem)
    w = h = 1000
    d = rg(f"{nombre}_n", (0, c1, 1), (0.18, c2, 1), (0.45, c3, 0.7), (1, c4, 0))
    b = [f'<circle cx="500" cy="500" r="490" fill="url(#{nombre}_n)"/>']
    for _ in range(46):
        a = r.uniform(0, 2 * math.pi); L = r.uniform(220, 480); g = r.uniform(4, 14)
        b.append(f'<path d="M{500 + 40 * math.cos(a):.0f} {500 + 40 * math.sin(a):.0f} L{500 + L * math.cos(a):.0f} {500 + L * math.sin(a):.0f}" '
                 f'stroke="{r.choice([c1, c2, c2, c3])}" stroke-width="{g:.0f}" stroke-linecap="round" opacity="{r.uniform(0.35, 0.9):.2f}"/>')
    for _ in range(26):
        a = r.uniform(0, 2 * math.pi); rr = r.uniform(300, 430)
        b.append(f'<ellipse cx="{500 + rr * math.cos(a):.0f}" cy="{500 + rr * math.sin(a):.0f}" rx="{r.uniform(30, 80):.0f}" ry="{r.uniform(14, 34):.0f}" '
                 f'fill="{r.choice([c3, c4, c2])}" opacity="0.5" transform="rotate({math.degrees(a):.0f} {500 + rr * math.cos(a):.0f} {500 + rr * math.sin(a):.0f})" filter="url(#blur8)"/>')
    b += [f'<circle cx="500" cy="500" r="380" fill="none" stroke="{c2}" stroke-width="18" opacity="0.6" filter="url(#blur8)"/>',
          f'<circle cx="500" cy="500" r="110" fill="{c1}" filter="url(#blur20)"/>', f'<circle cx="500" cy="500" r="60" fill="#ffffff"/>']
    guardar(nombre, "".join(b), w, h, d)


def estrella_capas(nombre="estrella_capas"):
    """Estrella gigante cortada como una cebolla: hidrógeno fuera, luego helio, carbono-oxígeno, silicio y hierro en el centro."""
    w = h = 900
    capas = [(430, "#ffd27a", "#ff8a3a"), (340, "#ff9a5a", "#e8462a"), (260, "#ff5a8a", "#b8306a"), (180, "#b07aff", "#6a3ac8"), (100, "#7a8a9a", "#3a4450")]
    d = "".join(rg(f"{nombre}_{k}", (0, a, 1), (1, c, 1), cx=0.4, cy=0.4) for k, (_, a, c) in enumerate(capas))
    b = ['<circle cx="450" cy="450" r="448" fill="#ffb84a" opacity="0.25" filter="url(#blur20)"/>']
    for k, (rr, _, _) in enumerate(capas):
        b.append(f'<circle cx="450" cy="450" r="{rr}" fill="url(#{nombre}_{k})"/>')
        b.append(f'<circle cx="450" cy="450" r="{rr}" fill="none" stroke="#ffffff" stroke-width="3" opacity="0.35"/>')
    r = random.Random(2)
    for _ in range(80):
        a = r.uniform(0, 2 * math.pi); rr = r.uniform(110, 420)
        b.append(f'<circle cx="{450 + rr * math.cos(a):.0f}" cy="{450 + rr * math.sin(a):.0f}" r="{r.uniform(2, 6):.0f}" fill="#ffffff" opacity="0.35"/>')
    # el corte: un cuarto "abierto" iluminado
    b.append('<path d="M450 450 L450 20 A430 430 0 0 1 880 450 Z" fill="#ffffff" opacity="0.06"/>')
    guardar(nombre, "".join(b), w, h, d)


def globulo(nombre="globulo"):
    """Glóbulo rojo (disco con el centro hundido)."""
    w, h = 400, 300
    d = rg(f"{nombre}_g", (0, "#8a0a14", 1), (0.5, "#c8202a", 1), (0.85, "#ff5a5a", 1), (1, "#a8101a", 1))
    b = ['<ellipse cx="200" cy="150" rx="190" ry="130" fill="url(#%s_g)"/>' % nombre,
         '<ellipse cx="200" cy="155" rx="90" ry="56" fill="#7a0a10" opacity="0.6" filter="url(#blur8)"/>',
         '<path d="M60 100 Q200 20 340 100" stroke="#ffb0a8" stroke-width="10" fill="none" opacity="0.5" stroke-linecap="round"/>']
    guardar(nombre, "".join(b), w, h, d)


def gota_sangre(nombre="gota_sangre"):
    w, h = 400, 560
    d = rg(f"{nombre}_g", (0, "#ff5a5a", 1), (0.6, "#c0101e", 1), (1, "#5a0008", 1), cx=0.35, cy=0.55, r=0.7)
    b = ['<path d="M200 20 C200 20 40 260 40 380 A160 160 0 0 0 360 380 C360 260 200 20 200 20 Z" fill="url(#%s_g)"/>' % nombre,
         '<ellipse cx="130" cy="390" rx="34" ry="70" fill="#ffffff" opacity="0.35" transform="rotate(-15 130 390)"/>',
         '<circle cx="250" cy="300" r="12" fill="#ffffff" opacity="0.5"/>']
    guardar(nombre, "".join(b), w, h, d)


def disco_proto(nombre="disco_proto"):
    """Nube de gas y polvo girando alrededor de un Sol que nace (disco visto de lado)."""
    w, h = 1000, 700
    r = random.Random(9)
    d = rg(f"{nombre}_s", (0, "#ffffff", 1), (0.2, "#fff0a0", 1), (1, "#ff9a3a", 0))
    b = []
    for k in range(9, 0, -1):
        b.append(f'<ellipse cx="500" cy="350" rx="{55 * k}" ry="{15 * k}" fill="none" stroke="{["#ff9a5a", "#c87aff", "#7ad0ff"][k % 3]}" stroke-width="{18 - k}" opacity="0.35" filter="url(#blur8)"/>')
    for _ in range(260):
        a = r.uniform(0, 2 * math.pi); rr = r.uniform(80, 480)
        b.append(f'<circle cx="{500 + rr * math.cos(a):.0f}" cy="{350 + rr * 0.27 * math.sin(a):.0f}" r="{r.uniform(1, 4):.1f}" fill="{r.choice(["#ffe0b0", "#ffffff", "#c8b0ff"])}" opacity="{r.uniform(0.3, 0.9):.2f}"/>')
    for (rr, a, s) in [(220, 0.6, 16), (340, 3.6, 22), (430, 2.2, 12)]:  # planetas que se forman
        b.append(f'<circle cx="{500 + rr * math.cos(a):.0f}" cy="{350 + rr * 0.27 * math.sin(a):.0f}" r="{s}" fill="#8a7a6a"/>')
    b += [f'<circle cx="500" cy="350" r="150" fill="url(#{nombre}_s)"/>', '<circle cx="500" cy="350" r="40" fill="#ffffff"/>']
    guardar(nombre, "".join(b), w, h, d)


def cuerpo_estrellas(nombre="cuerpo_estrellas"):
    """Silueta humana de pie rellena de estrellas y nebulosa (eres polvo de estrellas)."""
    w, h = 560, 1300
    r = random.Random(13)
    sil = ("M280 40 Q340 40 348 110 Q352 170 316 200 L330 230 Q430 250 450 320 L500 640 Q506 680 470 680 L440 660 L400 380 L392 700 L400 1240 "
           "Q400 1280 360 1280 L330 1280 L300 760 H260 L230 1280 H200 Q160 1280 160 1240 L168 700 L160 380 L120 660 L90 680 Q54 680 60 640 L110 320 "
           "Q130 250 230 230 L244 200 Q208 170 212 110 Q220 40 280 40 Z")
    d = (f'<clipPath id="{nombre}_c"><path d="{sil}"/></clipPath>'
         + lg(f"{nombre}_f", (0, "#1a0a3a"), (0.5, "#3a1a6a"), (1, "#0a1a3a"))
         + rg(f"{nombre}_n1", (0, "#ff4aa8", 0.7), (1, "#ff4aa8", 0)) + rg(f"{nombre}_n2", (0, "#3ac8ff", 0.6), (1, "#3ac8ff", 0)))
    b = [f'<path d="{sil}" fill="#9ad8ff" opacity="0.5" filter="url(#blur20)"/>', f'<g clip-path="url(#{nombre}_c)">',
         f'<rect width="{w}" height="{h}" fill="url(#{nombre}_f)"/>',
         f'<ellipse cx="300" cy="420" rx="260" ry="320" fill="url(#{nombre}_n1)"/>', f'<ellipse cx="260" cy="900" rx="240" ry="380" fill="url(#{nombre}_n2)"/>']
    for _ in range(420):
        b.append(f'<circle cx="{r.uniform(0, w):.0f}" cy="{r.uniform(0, h):.0f}" r="{r.choice([1, 1, 1.5, 2, 3]):.1f}" fill="#ffffff" opacity="{r.uniform(0.4, 1):.2f}"/>')
    b += ['</g>', f'<path d="{sil}" fill="none" stroke="#c8f0ff" stroke-width="4" opacity="0.9"/>']
    guardar(nombre, "".join(b), w, h, d)


def vaso_agua(nombre="vaso_agua"):
    w, h = 420, 620
    d = lg(f"{nombre}_a", (0, "#8ad8ff"), (1, "#2a8ad8"))
    b = ['<ellipse cx="210" cy="600" rx="150" ry="16" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<path d="M50 40 L90 590 H330 L370 40 Z" fill="#ffffff" opacity="0.18" stroke="#e8f6ff" stroke-width="6"/>',
         f'<path d="M66 200 L90 590 H330 L354 200 Z" fill="url(#{nombre}_a)" opacity="0.85"/>',
         '<ellipse cx="210" cy="200" rx="144" ry="18" fill="#c8f0ff"/>',
         '<path d="M80 80 L110 560" stroke="#ffffff" stroke-width="14" opacity="0.4" stroke-linecap="round"/>',
         *[f'<circle cx="{c[0]}" cy="{c[1]}" r="{c[2]}" fill="#ffffff" opacity="0.6"/>' for c in [(180, 420, 8), (240, 360, 6), (210, 500, 5), (270, 460, 7)]]]
    guardar(nombre, "".join(b), w, h, d)


def anillo_oro(nombre="anillo_oro"):
    w, h = 520, 420
    d = lg(f"{nombre}_o", (0, "#fff2a8"), (0.4, "#f0b832"), (0.7, "#a8701a"), (1, "#ffe07a"), x2=1, y2=1)
    b = ['<ellipse cx="260" cy="230" rx="230" ry="150" fill="none" stroke="#5a3a08" stroke-width="64" opacity="0.4" filter="url(#blur8)"/>',
         f'<ellipse cx="260" cy="210" rx="220" ry="140" fill="none" stroke="url(#{nombre}_o)" stroke-width="56"/>',
         '<path d="M80 150 Q260 50 440 150" stroke="#ffffff" stroke-width="10" fill="none" opacity="0.7" stroke-linecap="round"/>',
         '<path d="M90 280 Q260 350 430 280" stroke="#7a4a08" stroke-width="10" fill="none" opacity="0.6"/>']
    guardar(nombre, "".join(b), w, h, d)


def estrella_roja(nombre="estrella_roja"):
    """Estrella supergigante roja con manchas de convección y corona brillante."""
    w = h = 900
    r = random.Random(17)
    d = rg(f"{nombre}_g", (0, "#ffd08a", 1), (0.5, "#ff6a2a", 1), (0.85, "#c8201a", 1), (1, "#6a0a0a", 1), cx=0.42, cy=0.4, r=0.6)
    b = ['<circle cx="450" cy="450" r="448" fill="#ff5a2a" opacity="0.35" filter="url(#blur40)"/>',
         f'<circle cx="450" cy="450" r="380" fill="url(#{nombre}_g)"/>']
    for _ in range(60):
        a = r.uniform(0, 2 * math.pi); rr = r.uniform(0, 330)
        b.append(f'<circle cx="{450 + rr * math.cos(a):.0f}" cy="{450 + rr * math.sin(a):.0f}" r="{r.uniform(14, 46):.0f}" fill="{r.choice(["#ffb04a", "#a81a10"])}" opacity="0.35" filter="url(#blur8)"/>')
    guardar(nombre, "".join(b), w, h, d)


# ====================================================================== 03 · OJOS AL REVÉS
def ojo_corte(nombre="ojo_corte"):
    """Ojo cortado de lado: córnea a la izquierda, iris, cristalino, humor vítreo, retina rosada al fondo y nervio óptico."""
    w, h = 1000, 800
    d = (rg(f"{nombre}_b", (0, "#ffffff", 1), (0.8, "#f0e6e0", 1), (1, "#d8b8b0", 1), cx=0.45, cy=0.45)
         + rg(f"{nombre}_v", (0, "#1a2438", 1), (1, "#0a0e18", 1)) + lg(f"{nombre}_c", (0, "#e0f4ff"), (1, "#7ab8e0"), x2=1, y2=0))
    b = ['<path d="M840 400 Q920 400 1000 360 L1000 470 Q920 430 840 440 Z" fill="#f0c8a0" stroke="#b08060" stroke-width="4"/>',  # nervio óptico
         f'<circle cx="520" cy="400" r="340" fill="url(#{nombre}_b)"/>',
         f'<circle cx="520" cy="400" r="300" fill="url(#{nombre}_v)"/>',
         # retina (fondo rosado)
         '<path d="M720 160 A300 300 0 0 1 720 640" stroke="#ff7a8a" stroke-width="22" fill="none"/>',
         '<path d="M720 160 A300 300 0 0 1 720 640" stroke="#ffb0b8" stroke-width="6" fill="none"/>',
         *[f'<path d="M{820 - 8 * k} {400 + s * (20 + 40 * k)} Q{760 - 10 * k} {400 + s * (60 + 50 * k)} {700 - 6 * k} {400 + s * (150 + 30 * k)}" stroke="#c8304a" stroke-width="4" fill="none" opacity="0.6"/>'
           for k in range(3) for s in (-1, 1)],
         # córnea y cámara anterior
         f'<path d="M210 260 Q110 400 210 540" stroke="url(#{nombre}_c)" stroke-width="16" fill="none"/>',
         '<path d="M200 270 Q130 400 200 530 L230 530 L230 270 Z" fill="#bfe6ff" opacity="0.35"/>',
         # iris (arriba y abajo) y cristalino
         '<path d="M236 230 L236 330" stroke="#3a7a5a" stroke-width="22" stroke-linecap="round"/>', '<path d="M236 470 L236 570" stroke="#3a7a5a" stroke-width="22" stroke-linecap="round"/>',
         '<ellipse cx="290" cy="400" rx="52" ry="110" fill="#e8f6ff" opacity="0.9" stroke="#9ad0f0" stroke-width="5"/>',
         '<ellipse cx="276" cy="360" rx="14" ry="40" fill="#ffffff" opacity="0.8"/>',
         '<path d="M220 120 Q520 40 820 140" stroke="#ffffff" stroke-width="10" fill="none" opacity="0.35" stroke-linecap="round"/>']
    guardar(nombre, "".join(b), w, h, d)


def arbol_verde(nombre="arbol_verde"):
    """Árbol pequeño con copa verde y tronco (para ver cómo se da la vuelta)."""
    w, h = 400, 560
    d = rg(f"{nombre}_c", (0, "#9ae05a", 1), (0.6, "#3a9a3a", 1), (1, "#1a5a24", 1), cx=0.4, cy=0.35)
    b = ['<ellipse cx="200" cy="544" rx="120" ry="12" fill="#000" opacity="0.3"/>',
         '<path d="M180 540 L186 330 Q200 300 214 330 L220 540 Z" fill="#6a3a1a"/>', '<path d="M200 380 L150 300 M200 360 L250 290" stroke="#6a3a1a" stroke-width="14"/>',
         f'<circle cx="200" cy="210" r="170" fill="url(#{nombre}_c)"/>',
         *[f'<circle cx="{c[0]}" cy="{c[1]}" r="{c[2]}" fill="#b8f070" opacity="0.4"/>' for c in [(140, 140, 40), (230, 110, 30), (110, 230, 30)]],
         *[f'<circle cx="{c[0]}" cy="{c[1]}" r="14" fill="#e8302a"/>' for c in [(260, 200), (160, 270), (230, 300), (120, 180)]]]
    guardar(nombre, "".join(b), w, h, d)


def camara_fuelle(nombre="camara_fuelle"):
    """Cámara antigua de fuelle vista de lado: objetivo a la izquierda, fuelle, y el cristal de enfoque detrás (donde la imagen sale al revés)."""
    w, h = 1000, 640
    d = lg(f"{nombre}_m", (0, "#c88a4a"), (1, "#7a4a1a")) + lg(f"{nombre}_f", (0, "#3a2a2a"), (1, "#1a1010"))
    b = ['<rect x="120" y="560" width="760" height="30" rx="6" fill="url(#%s_m)"/>' % nombre,
         '<path d="M440 600 L380 640 M560 600 L620 640" stroke="#4a3020" stroke-width="12"/>',
         f'<rect x="100" y="180" width="160" height="380" rx="10" fill="url(#{nombre}_m)" stroke="#4a2a10" stroke-width="6"/>',
         '<rect x="10" y="300" width="100" height="140" rx="8" fill="#2a2a30"/>', '<ellipse cx="14" cy="370" rx="18" ry="62" fill="#6aa8d8" opacity="0.8"/>',
         '<path d="M260 210 L700 120 V620 L260 530 Z" fill="url(#%s_f)"/>' % nombre]
    for k in range(1, 9):
        x = 260 + k * 55
        y0, y1 = 210 - k * 11.25, 530 + k * 11.25
        b.append(f'<path d="M{x} {y0:.0f} V{y1:.0f}" stroke="#5a4040" stroke-width="6"/>')
    b += [f'<rect x="700" y="100" width="200" height="540" rx="10" fill="url(#{nombre}_m)" stroke="#4a2a10" stroke-width="6"/>',
          '<rect x="890" y="140" width="30" height="460" fill="#e8f0f8" opacity="0.85"/>']
    guardar(nombre, "".join(b), w, h, d)


def bg_paisaje(nombre="bg_paisaje"):
    """Paisaje de día: cielo con nubes, colinas, una casa y un camino (para darle la vuelta)."""
    r = random.Random(23)
    d = lg(f"{nombre}_c", (0, "#3a8ae0"), (0.6, "#9ad0ff"), (1, "#d8f0ff")) + lg(f"{nombre}_h", (0, "#7ac85a"), (1, "#3a7a2a"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>',
         '<circle cx="820" cy="300" r="90" fill="#fff6c0"/>', '<circle cx="820" cy="300" r="170" fill="#fff6c0" opacity="0.3" filter="url(#blur20)"/>']
    for _ in range(6):
        x, y = r.uniform(50, 1000), r.uniform(200, 700)
        b.append(f'<g opacity="0.95"><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="120" ry="40" fill="#ffffff"/><ellipse cx="{x - 50:.0f}" cy="{y - 24:.0f}" rx="60" ry="44" fill="#ffffff"/>'
                 f'<ellipse cx="{x + 40:.0f}" cy="{y - 30:.0f}" rx="70" ry="50" fill="#ffffff"/></g>')
    b += ['<path d="M0 1100 Q300 980 600 1080 T1080 1040 V1920 H0 Z" fill="#5aa848"/>',
          f'<path d="M0 1250 Q400 1120 1080 1240 V1920 H0 Z" fill="url(#{nombre}_h)"/>',
          '<path d="M480 1920 Q520 1500 560 1250 Q600 1500 760 1920 Z" fill="#d8b878"/>',
          '<rect x="180" y="1060" width="240" height="200" fill="#f4e8d0"/>', '<path d="M160 1070 L300 960 L440 1070 Z" fill="#c8402a"/>',
          '<rect x="270" y="1160" width="60" height="100" fill="#6a3a1a"/>', '<rect x="200" y="1100" width="50" height="50" fill="#7ab8e8"/>',
          '<rect x="350" y="1100" width="50" height="50" fill="#7ab8e8"/>', grano()]
    guardar(nombre, "".join(b), defs=d)


def stratton(nombre="stratton"):
    """Psicólogo de 1896 a contraluz con un tubo de lentes en un ojo y el otro tapado (silueta genérica, sin cara)."""
    w, h = 700, 900
    col, luz = "#1a1622", "#7df9ff"
    b = ['<path d="M140 900 L170 640 Q200 560 330 540 L430 540 Q560 560 590 640 L620 900 Z" fill="%s"/>' % col,
         '<path d="M300 560 L360 640 L420 560 Z" fill="#e8e0d0"/>',
         '<path d="M250 300 Q250 120 400 120 Q520 130 520 260 L540 300 L524 320 Q530 420 470 470 L440 560 H310 Q260 480 250 300 Z" fill="%s"/>' % col,
         f'<path d="M400 120 Q520 130 520 260 L540 300 L524 320" stroke="{luz}" stroke-width="6" fill="none" opacity="0.9"/>',
         # tubo con lentes delante del ojo (de perfil)
         '<rect x="470" y="232" width="200" height="64" rx="10" fill="#4a4a54" stroke="#9a9aa8" stroke-width="4"/>',
         '<ellipse cx="670" cy="264" rx="14" ry="34" fill="#7ad0ff" opacity="0.9"/>',
         '<path d="M480 240 H660" stroke="#c8c8d8" stroke-width="5" opacity="0.6"/>',
         '<path d="M300 250 Q400 230 470 248" stroke="#6a6a74" stroke-width="10" fill="none"/>']
    guardar(nombre, "".join(b), w, h)


def tubo_lentes(nombre="tubo_lentes"):
    w, h = 700, 260
    d = lg(f"{nombre}_m", (0, "#9a9aa8"), (0.5, "#4a4a54"), (1, "#2a2a30"))
    b = [f'<rect x="60" y="60" width="580" height="140" rx="20" fill="url(#{nombre}_m)"/>',
         '<ellipse cx="60" cy="130" rx="30" ry="70" fill="#7ad0ff" opacity="0.9" stroke="#c8c8d8" stroke-width="6"/>',
         '<ellipse cx="640" cy="130" rx="30" ry="70" fill="#7ad0ff" opacity="0.9" stroke="#c8c8d8" stroke-width="6"/>',
         '<ellipse cx="350" cy="130" rx="22" ry="62" fill="#bfe6ff" opacity="0.7"/>',
         '<path d="M90 80 H610" stroke="#ffffff" stroke-width="10" opacity="0.4" stroke-linecap="round"/>']
    guardar(nombre, "".join(b), w, h, d)


def bg_salon_1896(nombre="bg_salon_1896"):
    """Salón de 1896: papel pintado, ventana, mesa con lámpara y una taza (para ver el mundo «patas arriba»)."""
    r = random.Random(29)
    d = lg(f"{nombre}_p", (0, "#6a5a3a"), (1, "#3a3020")) + lg(f"{nombre}_s", (0, "#7a4a2a"), (1, "#3a2010"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_p)"/>']
    for x in range(0, 1080, 90):
        b.append(f'<path d="M{x + 45} 0 V1300" stroke="#8a7a4a" stroke-width="18" opacity="0.25"/>')
        for y in range(40, 1300, 120):
            b.append(f'<circle cx="{x + 45}" cy="{y}" r="10" fill="#c8a85a" opacity="0.35"/>')
    b += ['<rect x="560" y="260" width="380" height="520" fill="#2a2010"/>', '<rect x="580" y="280" width="340" height="480" fill="#9ad0ff"/>',
          '<path d="M750 280 V760 M580 520 H920" stroke="#2a2010" stroke-width="14"/>',
          '<path d="M540 240 Q600 500 560 800 L520 800 Q560 500 520 240 Z" fill="#8a2a2a"/>',
          f'<rect y="1300" width="1080" height="620" fill="url(#{nombre}_s)"/>',
          '<rect x="140" y="1080" width="520" height="40" rx="8" fill="#5a3014"/>', '<path d="M180 1120 V1420 M620 1120 V1420" stroke="#4a2810" stroke-width="26"/>',
          '<path d="M260 1080 L300 900 H380 L420 1080 Z" fill="#e8d8a0"/>', '<rect x="330" y="820" width="20" height="80" fill="#5a4a2a"/>',
          '<path d="M260 820 L300 720 H380 L420 820 Z" fill="#f0c86a"/>', '<ellipse cx="340" cy="800" rx="160" ry="90" fill="#ffd88a" opacity="0.3" filter="url(#blur20)"/>',
          '<path d="M480 1000 H580 L570 1080 H490 Z" fill="#ffffff"/>', '<path d="M580 1020 Q620 1030 576 1060" stroke="#ffffff" stroke-width="10" fill="none"/>', grano()]
    guardar(nombre, "".join(b), defs=d)


def generar(dirsvg):
    ilus.generar(dirsvg)
    t17 = _mod("lotes/2026-11-17-tarde/generadores/ilus_tarde.py", "_ilus_1117t_b"); ilus.OUT = dirsvg
    t17.ojo(); t17.cara_perfil()
    m183 = _mod("lotes/2026-11-18-manana/generadores/ilus_03.py", "_ilus_1118m_03_b"); ilus.OUT = dirsvg
    m183.cerebro()
    m181 = _mod("lotes/2026-11-18-manana/generadores/ilus_01.py", "_ilus_1118m_01_b"); ilus.OUT = dirsvg
    m181.martillo()
    t18 = _mod("lotes/2026-11-18-tarde/generadores/ilus_tarde.py", "_ilus_1118t_b"); ilus.OUT = dirsvg
    t18.atomo(); t18.bola_neutrones()
    t18.hoja_calendario("cal_1891", "1891"); t18.hoja_calendario("cal_1896", "1896")
    t19 = _mod("lotes/2026-11-19-tarde/generadores/ilus_1119t.py", "_ilus_1119t_b"); ilus.OUT = dirsvg
    t19.esqueleto(); t19.femur()
    t20 = _mod("lotes/2026-11-20-tarde/generadores/ilus_1120t.py", "_ilus_1120t_b"); ilus.OUT = dirsvg
    t20.persona_pie()
    ilus.OUT = dirsvg
    ilus.bg_espacio_rico("bg_esp_violeta", "violeta", 31); ilus.bg_espacio_rico("bg_esp_ambar", "ambar", 43); ilus.bg_espacio_rico("bg_esp_petroleo", "petroleo", 57)
    # 01
    bg_gimnasio(); bg_gimnasio("bg_gimnasio_luz", 1.6); bg_nieve_noche(); cesta(); cesta("cesta_sin_fondo", fondo=False); cesta_frente(); fondo_cesta()
    balon_cuero(); balon_moderno(); canasta_moderna(); escalera(); palo(); hoja_reglas(); melocoton(); profesor(); pizarra(); copo(); clavo()
    jugador("jugador_a", "#c8302a"); jugador("jugador_b", "#e8e0c8", pose=1); jugador("jugador_a2", "#c8302a", pose=1); jugador("jugador_b2", "#e8e0c8")
    # 02
    supernova(); supernova("bigbang", "#ffffff", "#fff6e0", "#ffd0a0", "#a0c8ff", sem=3); supernova("choque", "#ffffff", "#fff0a0", "#ffb020", "#3ac8ff", sem=11)
    estrella_capas(); globulo(); gota_sangre(); disco_proto(); cuerpo_estrellas(); vaso_agua(); anillo_oro(); estrella_roja()
    # 03
    ojo_corte(); arbol_verde(); camara_fuelle(); bg_paisaje(); stratton(); tubo_lentes(); bg_salon_1896()
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
