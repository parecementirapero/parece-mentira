"""Ilustraciones del lote 2026-11-20-tarde (Agente 20:00, Jorge): 01 dieciséis amaneceres (Estación Espacial),
02 desde el Mulhacén se ve África, 03 los flamencos nacen grises.
Uso: python3 ilus_1120t.py DIR_SVG. Ladrillos de motor/biblioteca/ilus.py. Reutiliza piezas de lotes anteriores
(Estación, órbita, casco, montaña, mar, cara, velocímetro…) cargándolas por ruta para no chocar de nombre.
Sin logos, banderas, marcas ni personas reales reconocibles: todo dibujado aquí."""
import importlib.util, math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano, _estrellas_ricas  # noqa: E402

W, H = 1080, 1920


def _mod(rel, nombre):
    s = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, rel))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _p(pts, cerrar=True):
    return "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + (" Z" if cerrar else "")


# ====================================================================== 01 · ESTACIÓN ESPACIAL
def bg_amanecer_orbital(nombre="bg_amanecer_orbital", fase=1.0):
    """La Tierra de noche desde la órbita con el Sol asomando por el borde: arco de luz naranja-azul y destello."""
    d = (rg(f"{nombre}_t", (0, "#10203a", 1), (1, "#03060e", 1), cx=0.5, cy=0.15)
         + rg(f"{nombre}_g", (0, "#fff6d8", 1), (0.15, "#ffc070", 0.9), (0.5, "#ff7a3a", 0.35), (1, "#ff7a3a", 0)))
    b = ['<rect width="1080" height="1920" fill="#01020a"/>', _estrellas_ricas(52, n_peq=260, n_med=24, n_bri=5),
         f'<circle cx="540" cy="3500" r="2800" fill="url(#{nombre}_t)"/>',
         # bandas de atmósfera iluminadas
         '<circle cx="540" cy="3500" r="2812" fill="none" stroke="#ff9a4a" stroke-width="18" opacity="0.75" filter="url(#blur8)"/>',
         '<circle cx="540" cy="3500" r="2826" fill="none" stroke="#7ad0ff" stroke-width="16" opacity="0.6" filter="url(#blur8)"/>',
         '<circle cx="540" cy="3500" r="2846" fill="none" stroke="#2a6aff" stroke-width="26" opacity="0.35" filter="url(#blur20)"/>',
         f'<ellipse cx="720" cy="700" rx="{520 * fase:.0f}" ry="{170 * fase:.0f}" fill="url(#{nombre}_g)"/>',
         f'<circle cx="720" cy="700" r="{60 * fase:.0f}" fill="#fffdf0"/>',
         f'<path d="M720 {700 - 260 * fase:.0f} L726 694 L720 {700 + 140 * fase:.0f} L714 694 Z" fill="#fff8e0" opacity="0.8"/>',
         f'<path d="M{720 - 420 * fase:.0f} 700 L714 694 L{720 + 420 * fase:.0f} 700 L714 706 Z" fill="#fff8e0" opacity="0.85"/>']
    r = random.Random(5)
    for _ in range(40):  # nubes con luz rasante
        x, y = r.uniform(0, 1080), r.uniform(760, 1100)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(30, 110):.0f}" ry="{r.uniform(6, 16):.0f}" fill="#ffb87a" opacity="{r.uniform(0.15, 0.4):.2f}" filter="url(#blur8)"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def ventanilla(nombre="ventanilla"):
    """Ventana redonda de la estación con la Tierra y el borde iluminado al otro lado."""
    w = h = 900
    d = (lg("vn_m", (0, "#e8eaee"), (1, "#7a808a")) + rg("vn_t", (0, "#5ab0f0", 1), (0.7, "#1a4a9a", 1), (1, "#0a1a3a", 1), cx=0.4, cy=0.9)
         + lg("vn_v", (0, "#ffffff", ), (1, "#ffffff")))
    b = ['<circle cx="450" cy="450" r="430" fill="url(#vn_m)" stroke="#4a4e56" stroke-width="8"/>',
         *[f'<circle cx="{450 + 395 * math.cos(a):.0f}" cy="{450 + 395 * math.sin(a):.0f}" r="14" fill="#5a5e66"/>' for a in [k * math.pi / 6 for k in range(12)]],
         '<clipPath id="vn_c"><circle cx="450" cy="450" r="340"/></clipPath>',
         '<g clip-path="url(#vn_c)"><rect width="900" height="900" fill="#02030a"/>',
         *[f'<circle cx="{random.Random(k).uniform(120, 780):.0f}" cy="{random.Random(k + 50).uniform(110, 420):.0f}" r="1.8" fill="#fff"/>' for k in range(40)],
         '<circle cx="450" cy="1500" r="1050" fill="url(#vn_t)"/>',
         '<circle cx="450" cy="1500" r="1058" fill="none" stroke="#9ae0ff" stroke-width="12" opacity="0.8" filter="url(#blur8)"/>',
         '<ellipse cx="330" cy="620" rx="120" ry="30" fill="#ffffff" opacity="0.45" filter="url(#blur8)"/>',
         '<ellipse cx="600" cy="700" rx="160" ry="34" fill="#ffffff" opacity="0.4" filter="url(#blur8)"/>',
         '<path d="M380 760 q60 -40 140 -10 q40 40 -20 70 q-90 10 -120 -60 Z" fill="#b89a60" opacity="0.7"/></g>',
         '<circle cx="450" cy="450" r="340" fill="none" stroke="#2a2e36" stroke-width="20"/>',
         '<path d="M220 300 Q300 200 420 170" stroke="#ffffff" stroke-width="18" stroke-linecap="round" opacity="0.35" fill="none"/>']
    guardar(nombre, "".join(b), w, h, d)


def campo_futbol(nombre="campo_futbol"):
    """Campo de fútbol americano visto desde arriba, en vertical (zonas de anotación arriba y abajo), sin logotipos."""
    w, h = 560, 1160
    d = lg("cf_h", (0, "#3a9a4a"), (1, "#2a7a3a"), x2=1, y2=0)
    b = ['<rect x="20" y="20" width="520" height="1120" fill="url(#cf_h)" stroke="#ffffff" stroke-width="8"/>',
         '<rect x="20" y="20" width="520" height="96" fill="#2a6a8a"/>', '<rect x="20" y="1044" width="520" height="96" fill="#8a2a3a"/>']
    for k in range(11):
        y = 116 + k * 92.8
        b.append(f'<path d="M20 {y:.0f} H540" stroke="#ffffff" stroke-width="{6 if k % 5 == 0 else 3}" opacity="0.9"/>')
    for k in range(10):
        for x in (170, 390):
            y = 116 + k * 92.8 + 46
            b.append(f'<path d="M{x - 12} {y:.0f} H{x + 12}" stroke="#ffffff" stroke-width="3"/>')
    for k in range(10):  # franjas de césped
        if k % 2: b.append(f'<rect x="20" y="{116 + k * 92.8:.0f}" width="520" height="92.8" fill="#ffffff" opacity="0.05"/>')
    b.append('<path d="M250 20 V-10 M310 20 V-10 M250 -10 H310" stroke="#ffd23f" stroke-width="8" fill="none"/>')
    guardar(nombre, "".join(b), w, h, d)


def torre_reloj(nombre="torre_reloj"):
    """Torre de reloj genérica de piedra clara al anochecer, con esfera iluminada (sin copiar ningún edificio)."""
    w, h = 520, 1400
    d = lg("tr_p", (0, "#e8d2a0"), (1, "#a8865a"), x2=1, y2=0) + rg("tr_e", (0, "#fffbe8", 1), (0.8, "#ffe8a8", 1), (1, "#c8a050", 1))
    b = ['<path d="M130 1400 V420 H390 V1400 Z" fill="url(#tr_p)" stroke="#6a5030" stroke-width="4"/>',
         *[f'<rect x="{150 + (k % 3) * 80}" y="{600 + (k // 3) * 140}" width="40" height="90" rx="18" fill="#3a3a5a" opacity="0.85"/>' for k in range(15)],
         '<path d="M110 420 H410 V250 H110 Z" fill="url(#tr_p)" stroke="#6a5030" stroke-width="4"/>',
         '<circle cx="260" cy="335" r="108" fill="#6a5030"/>', '<circle cx="260" cy="335" r="96" fill="url(#tr_e)"/>',
         '<circle cx="260" cy="335" r="150" fill="#ffe8a8" opacity="0.18" filter="url(#blur20)"/>',
         *[f'<path d="M{260 + 80 * math.cos(a):.0f} {335 + 80 * math.sin(a):.0f} L{260 + 92 * math.cos(a):.0f} {335 + 92 * math.sin(a):.0f}" stroke="#3a2a10" stroke-width="5"/>'
           for a in [k * math.pi / 6 for k in range(12)]],
         '<path d="M90 250 L260 40 L430 250 Z" fill="#4a5a6a" stroke="#2a3038" stroke-width="4"/>',
         '<path d="M260 40 V0" stroke="#c8a050" stroke-width="8"/>']
    guardar(nombre, "".join(b), w, h, d)


def manecillas(nombre="manecillas"):
    """Dos manecillas para poner encima de la esfera de la torre (giran con el motor)."""
    w, h = 220, 220
    b = ['<path d="M110 110 L110 34" stroke="#1a1408" stroke-width="9" stroke-linecap="round"/>',
         '<path d="M110 110 L160 138" stroke="#1a1408" stroke-width="11" stroke-linecap="round"/>', '<circle cx="110" cy="110" r="10" fill="#1a1408"/>']
    guardar(nombre, "".join(b), w, h)


def bg_londres_noche(nombre="bg_londres_noche"):
    """Ciudad junto a un río de noche, siluetas genéricas y luces en el agua."""
    r = random.Random(17)
    d = lg(f"{nombre}_c", (0, "#0a1030"), (0.6, "#2a2a5a"), (1, "#5a3a5a"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>', _estrellas_ricas(61, n_peq=120, n_med=10, n_bri=2)]
    x = -20
    while x < 1100:
        wd, hg = r.uniform(60, 150), r.uniform(200, 620)
        b.append(f'<rect x="{x:.0f}" y="{1300 - hg:.0f}" width="{wd:.0f}" height="{hg:.0f}" fill="#141830"/>')
        for _ in range(int(hg / 40)):
            b.append(f'<rect x="{x + r.uniform(8, wd - 16):.0f}" y="{1300 - r.uniform(20, hg - 20):.0f}" width="8" height="12" fill="#ffd88a" opacity="{r.uniform(0.4, 0.9):.2f}"/>')
        x += wd + r.uniform(0, 20)
    b += ['<rect y="1300" width="1080" height="620" fill="#0a1228"/>']
    for _ in range(70):
        b.append(f'<rect x="{r.uniform(0, 1080):.0f}" y="{r.uniform(1310, 1900):.0f}" width="{r.uniform(20, 80):.0f}" height="3" fill="#ffd88a" opacity="{r.uniform(0.1, 0.4):.2f}"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def orbita_luna(nombre="orbita_luna"):
    """Diagrama: trazo de ida y vuelta entre la Tierra (abajo) y la Luna (arriba) en línea discontinua."""
    w, h = 400, 1300
    b = ['<path d="M150 1200 C60 800 60 400 170 110" stroke="#7df9ff" stroke-width="8" fill="none" stroke-dasharray="26 18"/>',
         '<path d="M230 110 C340 400 340 800 250 1200" stroke="#ff3df2" stroke-width="8" fill="none" stroke-dasharray="26 18"/>',
         '<path d="M150 150 l20 -45 l25 40" stroke="#7df9ff" stroke-width="8" fill="none"/>',
         '<path d="M225 1160 l25 45 l25 -40" stroke="#ff3df2" stroke-width="8" fill="none"/>']
    guardar(nombre, "".join(b), w, h)


# ====================================================================== 02 · MULHACÉN
def bg_cumbre(nombre="bg_cumbre"):
    """Cima nevada de alta montaña con cielo azul intenso, rocas y un vértice de piedra en lo alto."""
    r = random.Random(31)
    d = (lg(f"{nombre}_c", (0, "#0a2a6a"), (0.5, "#2a6ac8"), (1, "#a8d4f8")) + lg(f"{nombre}_n", (0, "#ffffff"), (1, "#c8d8ec"))
         + lg(f"{nombre}_r", (0, "#5a5048"), (1, "#2a2420")))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>',
         '<path d="M-20 1300 L120 1180 L260 1250 L420 1120 L560 1210 L700 1150 L860 1240 L1100 1160 L1100 1920 L-20 1920 Z" fill="#8a9ab8" opacity="0.55"/>',
         # cresta principal
         '<path d="M-40 1920 L-40 1380 L180 1210 L330 1060 L470 900 L560 860 L640 900 L760 1040 L900 1150 L1120 1300 L1120 1920 Z" fill="url(#' + nombre + '_r)"/>',
         '<path d="M-40 1460 L180 1260 L330 1110 L470 950 L560 905 L640 945 L760 1080 L900 1200 L1120 1350 L1120 1920 L-40 1920 Z" fill="url(#' + nombre + '_n)"/>',
         '<path d="M560 905 L470 950 L380 1400 L520 1920 L620 1920 L600 1300 Z" fill="#a8bad4" opacity="0.6"/>']
    for _ in range(40):  # rocas que asoman de la nieve
        x = r.uniform(0, 1080); y = r.uniform(1150, 1900)
        s = r.uniform(18, 60)
        b.append(f'<path d="M{x - s:.0f} {y:.0f} L{x - s * 0.3:.0f} {y - s * 0.7:.0f} L{x + s * 0.5:.0f} {y - s * 0.5:.0f} L{x + s:.0f} {y:.0f} Z" fill="#4a4038" opacity="0.9"/>')
    b += ['<rect x="535" y="770" width="50" height="110" fill="#8a8478" stroke="#4a443c" stroke-width="4"/>',  # vértice geodésico
          '<rect x="528" y="760" width="64" height="18" fill="#6a645a"/>',
          '<circle cx="860" cy="330" r="80" fill="#fffbe8"/>', '<circle cx="860" cy="330" r="220" fill="#fff0b0" opacity="0.3" filter="url(#blur40)"/>']
    for _ in range(30):  # nieve que vuela
        b.append(f'<circle cx="{r.uniform(0, 1080):.0f}" cy="{r.uniform(600, 1500):.0f}" r="{r.uniform(1.5, 4):.1f}" fill="#ffffff" opacity="0.7"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def bg_vista_africa(nombre="bg_vista_africa", rif=1.0):
    """Vista al sur desde la cima: rocas nevadas delante, sierras pardas, el Mediterráneo y, al fondo, las montañas del Rif."""
    r = random.Random(32)
    d = (lg(f"{nombre}_c", (0, "#1a4a9a"), (0.55, "#7ab4e8"), (1, "#f0e0c8")) + lg(f"{nombre}_m", (0, "#3a6aa8"), (1, "#1a3a6a"))
         + lg(f"{nombre}_s", (0, "#a88a6a"), (1, "#5a4030")))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>',
         # Rif al fondo, sobre el mar
         f'<path d="M-20 1010 L80 975 L170 950 L250 905 L330 935 L420 870 L500 905 L590 850 L680 910 L760 875 L860 930 L960 900 L1100 950 L1100 1020 L-20 1020 Z" fill="#56689a" opacity="{0.9 * rif:.2f}"/>',
         f'<path d="M420 870 L440 890 L460 884 L500 905 M590 850 L612 872 L640 866 L680 910" stroke="#e8eef8" stroke-width="5" fill="none" opacity="{0.8 * rif:.2f}"/>',
         '<rect x="0" y="1012" width="1080" height="8" fill="#e8f0ff" opacity="0.4" filter="url(#blur8)"/>',
         f'<rect y="1018" width="1080" height="220" fill="url(#{nombre}_m)"/>']
    for _ in range(50):
        b.append(f'<rect x="{r.uniform(0, 1080):.0f}" y="{r.uniform(1030, 1230):.0f}" width="{r.uniform(20, 70):.0f}" height="2" fill="#ffffff" opacity="{r.uniform(0.1, 0.35):.2f}"/>')
    b += ['<path d="M-20 1240 L150 1180 L300 1220 L470 1150 L650 1210 L820 1160 L1100 1230 L1100 1920 L-20 1920 Z" fill="#8a6a50"/>',
          f'<path d="M-20 1360 L200 1280 L380 1340 L560 1270 L760 1330 L940 1290 L1100 1350 L1100 1920 L-20 1920 Z" fill="url(#{nombre}_s)"/>',
          '<path d="M-20 1560 L240 1480 L420 1540 L620 1460 L820 1530 L1100 1470 L1100 1920 L-20 1920 Z" fill="#4a3a30"/>',
          '<path d="M-40 1920 L-40 1650 L220 1600 L420 1680 L600 1620 L820 1700 L1120 1640 L1120 1920 Z" fill="#f4f8ff"/>',
          '<path d="M-40 1720 L260 1660 L480 1740 L1120 1700" stroke="#c8d6ea" stroke-width="10" fill="none"/>']
    for _ in range(14):
        x = r.uniform(0, 1080); y = r.uniform(1680, 1900); s = r.uniform(20, 55)
        b.append(f'<path d="M{x - s:.0f} {y:.0f} L{x:.0f} {y - s * 0.8:.0f} L{x + s:.0f} {y:.0f} Z" fill="#4a4038"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def tierra_arco(nombre="tierra_arco"):
    """Diagrama: casquete de la Tierra (mar azul) visto de lado, para enseñar la curva y el horizonte."""
    w, h = 1080, 900
    d = lg("ta_m", (0, "#4aa0e8"), (1, "#0a2a6a"))
    b = ['<path d="M-200 900 Q540 0 1280 900 Z" fill="url(#ta_m)"/>',
         '<path d="M-200 900 Q540 0 1280 900" stroke="#9ae0ff" stroke-width="10" fill="none"/>',
         '<path d="M-200 900 Q540 -30 1280 900" stroke="#7ad0ff" stroke-width="26" fill="none" opacity="0.3" filter="url(#blur8)"/>']
    guardar(nombre, "".join(b), w, h, d)


def persona_pie(nombre="persona_pie", col="#1a1a2a"):
    """Silueta pequeña de una persona de pie mirando a la derecha."""
    w, h = 160, 420
    b = [f'<circle cx="80" cy="50" r="34" fill="{col}"/>', f'<path d="M50 100 Q80 86 110 100 L120 250 L104 252 L100 410 L84 410 L80 270 L76 410 L60 410 L56 252 L40 250 Z" fill="{col}"/>',
         f'<path d="M110 110 L140 200" stroke="{col}" stroke-width="16" stroke-linecap="round"/>']
    guardar(nombre, "".join(b), w, h)


def excursionista(nombre="excursionista"):
    """Montañero de espaldas con mochila y bastón, mirando a lo lejos (silueta con luz de borde)."""
    w, h = 420, 760
    d = lg("ex_c", (0, "#3a4a6a"), (1, "#1a2030"))
    b = ['<ellipse cx="210" cy="740" rx="150" ry="16" fill="#000" opacity="0.3" filter="url(#blur8)"/>',
         '<path d="M150 380 L130 730 L180 730 L205 470 L230 730 L280 730 L262 380 Z" fill="#2a3040"/>',
         '<rect x="120" y="170" width="180" height="230" rx="40" fill="#c0392b"/>', '<rect x="140" y="200" width="140" height="60" rx="20" fill="#e0574a"/>',
         '<path d="M130 180 Q210 140 290 180 L300 400 L120 400 Z" fill="url(#ex_c)" opacity="0.35"/>',
         '<circle cx="210" cy="110" r="58" fill="#2a2420"/>', '<path d="M150 96 Q210 30 270 96 Z" fill="#e8b84a"/>',
         '<path d="M300 260 L370 730" stroke="#8a8a8a" stroke-width="10" stroke-linecap="round"/>',
         '<path d="M154 90 Q210 40 266 90" stroke="#ffe8a8" stroke-width="5" fill="none" opacity="0.8"/>']
    guardar(nombre, "".join(b), w, h, d)


def mapa_estrecho(nombre="mapa_estrecho"):
    """Mapa esquemático: costa del sur de la península arriba, el Mediterráneo y el norte de África abajo (sin textos)."""
    d = lg("me_m", (0, "#1a5a9a"), (1, "#0a2a5a")) + lg("me_t", (0, "#c8a874"), (1, "#a8845a"))
    b = ['<rect width="1080" height="1920" fill="url(#me_m)"/>',
         '<path d="M-20 0 H1100 V700 L980 690 L860 760 L760 740 L640 800 L520 790 L420 830 L300 840 L200 900 L120 960 L60 940 L-20 900 Z" fill="url(#me_t)"/>',
         '<path d="M-20 1300 L60 1250 L140 1230 L260 1260 L380 1240 L520 1290 L640 1270 L780 1310 L900 1290 L1100 1330 V1940 H-20 Z" fill="url(#me_t)"/>',
         # relieve
         '<path d="M520 520 l50 -70 l40 50 l60 -60 l50 70 Z" fill="#8a6a4a"/><path d="M560 450 l10 -14 l12 14 Z" fill="#ffffff"/>',
         '<path d="M180 1430 l60 -60 l50 40 l70 -80 l60 70 l60 -50 l70 80 Z" fill="#8a6a4a"/>',
         '<path d="M-20 900 L60 940 L120 960" stroke="#e8f4ff" stroke-width="6" fill="none" opacity="0.6"/>',
         '<path d="M-20 1300 L60 1250 L140 1230 L260 1260 L380 1240 L520 1290 L640 1270 L780 1310 L900 1290 L1100 1330" stroke="#e8f4ff" stroke-width="6" fill="none" opacity="0.6"/>',
         '<path d="M-20 900 L-20 0 H1100 V700 L980 690 L860 760 L760 740 L640 800 L520 790 L420 830 L300 840 L200 900" stroke="#e8f4ff" stroke-width="6" fill="none" opacity="0.6"/>']
    r = random.Random(4)
    for _ in range(40):
        b.append(f'<rect x="{r.uniform(0, 1080):.0f}" y="{r.uniform(900, 1250):.0f}" width="{r.uniform(30, 90):.0f}" height="3" fill="#ffffff" opacity="0.15"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def corona(nombre="corona"):
    """Corona dorada medieval con piedras."""
    w, h = 640, 440
    d = lg("co_o", (0, "#fff0a0"), (0.5, "#e8b830"), (1, "#8a6010"))
    b = ['<ellipse cx="320" cy="410" rx="260" ry="22" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<path d="M70 380 L50 120 L180 250 L320 60 L460 250 L590 120 L570 380 Z" fill="url(#co_o)" stroke="#6a4a08" stroke-width="6"/>',
         '<rect x="70" y="320" width="500" height="70" rx="10" fill="url(#co_o)" stroke="#6a4a08" stroke-width="6"/>',
         '<circle cx="320" cy="355" r="22" fill="#c0392b"/><circle cx="190" cy="355" r="16" fill="#2a6ac8"/><circle cx="450" cy="355" r="16" fill="#2a8a4a"/>',
         '<circle cx="50" cy="120" r="18" fill="#fff0a0"/><circle cx="320" cy="60" r="20" fill="#fff0a0"/><circle cx="590" cy="120" r="18" fill="#fff0a0"/>',
         '<path d="M110 300 L100 160" stroke="#fff8d0" stroke-width="8" opacity="0.6"/>']
    guardar(nombre, "".join(b), w, h, d)


def lapida_nieve(nombre="lapida_nieve"):
    """Montículo de piedras cubierto de nieve en una cima (sin cruces ni símbolos)."""
    w, h = 760, 520
    b = ['<ellipse cx="380" cy="490" rx="330" ry="26" fill="#000" opacity="0.3" filter="url(#blur8)"/>']
    r = random.Random(8)
    for k in range(22):
        x = 380 + r.uniform(-260, 260) * (1 - k / 30); y = 470 - k * 12 - r.uniform(0, 20)
        s = r.uniform(40, 80)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{s:.0f}" ry="{s * 0.6:.0f}" fill="#{r.choice(["5a524a", "6a6258", "4a443c"])}"/>')
    b += ['<path d="M90 330 Q200 170 380 140 Q560 170 670 330 Q560 280 380 270 Q200 280 90 330 Z" fill="#ffffff"/>',
          '<path d="M200 240 Q300 190 380 186" stroke="#c8d8ec" stroke-width="8" fill="none"/>']
    guardar(nombre, "".join(b), w, h)


def prismaticos(nombre="prismaticos"):
    """Prismáticos negros con reflejo azul en las lentes."""
    w, h = 760, 440
    d = lg("pr_c", (0, "#4a4e56"), (1, "#14161a"))
    b = ['<rect x="60" y="90" width="260" height="300" rx="70" fill="url(#pr_c)"/>', '<rect x="440" y="90" width="260" height="300" rx="70" fill="url(#pr_c)"/>',
         '<rect x="300" y="140" width="160" height="110" rx="20" fill="url(#pr_c)"/>',
         '<ellipse cx="190" cy="390" rx="110" ry="34" fill="#1a2a4a"/><ellipse cx="570" cy="390" rx="110" ry="34" fill="#1a2a4a"/>',
         '<ellipse cx="170" cy="384" rx="50" ry="12" fill="#7ad0ff" opacity="0.7"/><ellipse cx="550" cy="384" rx="50" ry="12" fill="#7ad0ff" opacity="0.7"/>',
         '<rect x="90" y="120" width="30" height="200" rx="14" fill="#ffffff" opacity="0.18"/><rect x="470" y="120" width="30" height="200" rx="14" fill="#ffffff" opacity="0.18"/>']
    guardar(nombre, "".join(b), w, h, d)



def bg_playa(nombre="bg_playa"):
    """Playa mirando al mar abierto: cielo claro, línea del horizonte recta, olas y arena delante."""
    r = random.Random(33)
    d = lg(f"{nombre}_c", (0, "#3a7ad0"), (0.7, "#a8d8f8"), (1, "#e8f4ff")) + lg(f"{nombre}_m", (0, "#2a6ab0"), (1, "#4ab0d8")) + lg(f"{nombre}_a", (0, "#f0d8a0"), (1, "#c8a870"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>', '<circle cx="250" cy="420" r="70" fill="#fffbe8"/>',
         '<circle cx="250" cy="420" r="200" fill="#fff6c8" opacity="0.3" filter="url(#blur40)"/>',
         f'<rect y="1000" width="1080" height="560" fill="url(#{nombre}_m)"/>', '<rect y="996" width="1080" height="6" fill="#e8f4ff" opacity="0.6"/>']
    for _ in range(70):
        y = r.uniform(1010, 1540)
        b.append(f'<rect x="{r.uniform(0, 1080):.0f}" y="{y:.0f}" width="{r.uniform(20, 140) * (y - 900) / 400:.0f}" height="{1 + (y - 1000) / 150:.0f}" fill="#ffffff" opacity="{r.uniform(0.15, 0.4):.2f}"/>')
    b += ['<path d="M-20 1540 Q270 1500 540 1540 T1100 1530 L1100 1600 L-20 1600 Z" fill="#ffffff" opacity="0.8"/>',
          f'<path d="M-20 1570 Q270 1540 540 1575 T1100 1565 L1100 1940 L-20 1940 Z" fill="url(#{nombre}_a)"/>']
    for _ in range(80):
        b.append(f'<circle cx="{r.uniform(0, 1080):.0f}" cy="{r.uniform(1600, 1920):.0f}" r="{r.uniform(1, 3):.1f}" fill="#8a6a40" opacity="0.4"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


# ====================================================================== 03 · FLAMENCOS
def bg_laguna(nombre="bg_laguna", hora="dia"):
    """Laguna salada poco profunda con cielo cálido, sierras lejanas y reflejos; bandada lejana."""
    r = random.Random(41)
    if hora == "dia":
        d = lg(f"{nombre}_c", (0, "#4a7ac8"), (0.6, "#f0c8a8"), (1, "#ffe8c8")) + lg(f"{nombre}_a", (0, "#d8b0a8"), (1, "#5a7a9a"))
    else:
        d = lg(f"{nombre}_c", (0, "#2a2a6a"), (0.5, "#d0607a"), (1, "#ffb070")) + lg(f"{nombre}_a", (0, "#e88a7a"), (1, "#3a3a6a"))
    b = [f'<rect width="1080" height="1920" fill="url(#{nombre}_c)"/>',
         '<circle cx="760" cy="760" r="90" fill="#fff4d8" opacity="0.9"/>', '<circle cx="760" cy="760" r="240" fill="#ffd8b0" opacity="0.3" filter="url(#blur40)"/>',
         '<path d="M-20 980 L140 900 L300 950 L470 870 L640 940 L820 880 L1100 960 L1100 1010 L-20 1010 Z" fill="#8a7a9a" opacity="0.7"/>',
         f'<rect y="1000" width="1080" height="920" fill="url(#{nombre}_a)"/>',
         '<ellipse cx="760" cy="1100" rx="60" ry="200" fill="#fff4d8" opacity="0.25" filter="url(#blur20)"/>']
    for _ in range(80):
        y = r.uniform(1010, 1900)
        b.append(f'<rect x="{r.uniform(0, 1080):.0f}" y="{y:.0f}" width="{r.uniform(20, 120) * (y / 1000):.0f}" height="{2 + (y - 1000) / 300:.0f}" fill="#ffffff" opacity="{r.uniform(0.08, 0.25):.2f}"/>')
    for _ in range(28):  # bandada lejana
        x, y = r.uniform(40, 1040), r.uniform(985, 1030)
        b.append(f'<path d="M{x:.0f} {y:.0f} v-22 q0 -10 6 -10" stroke="#e8708a" stroke-width="3" fill="none"/><ellipse cx="{x:.0f}" cy="{y - 24:.0f}" rx="7" ry="4" fill="#f08aa0"/>')
    b += ['<path d="M-20 1700 Q300 1650 600 1700 T1100 1690 L1100 1920 L-20 1920 Z" fill="#c8a890" opacity="0.55"/>']
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def _flamenco_partes(c1, c2, c3, comiendo=False, una_pata=True):
    """Devuelve el cuerpo del flamenco (lienzo 700×1100, mirando a la derecha). c1 claro, c2 medio, c3 oscuro (alas)."""
    b = ['<ellipse cx="320" cy="1080" rx="140" ry="14" fill="#000" opacity="0.25" filter="url(#blur8)"/>']
    # patas
    b.append(f'<path d="M318 560 L322 820 L318 1070" stroke="{c3}" stroke-width="12" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M318 1070 L270 1078 M318 1070 L372 1076" stroke="{c3}" stroke-width="10" stroke-linecap="round"/>')
    b.append(f'<circle cx="322" cy="820" r="11" fill="{c3}"/>')
    if una_pata:
        b.append(f'<path d="M350 560 L410 760 L330 720" stroke="{c3}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        b.append(f'<path d="M352 560 L372 820 L380 1070" stroke="{c3}" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M380 1070 L430 1076" stroke="{c3}" stroke-width="10" stroke-linecap="round"/>')
    # cuerpo
    b.append(f'<path d="M140 420 C150 330 300 300 420 340 C500 370 520 450 470 510 C420 570 300 590 220 560 C160 540 110 500 80 470 Z" fill="url(#fl_c)"/>')
    b.append(f'<path d="M150 420 C220 380 330 380 430 420 C380 470 260 500 160 470 Z" fill="{c2}" opacity="0.8"/>')
    b.append(f'<path d="M90 470 L40 500 L110 500 Z" fill="{c3}"/>')  # cola
    b.append('<path d="M170 360 C260 320 360 320 430 350" stroke="#ffffff" stroke-width="6" fill="none" opacity="0.35"/>')
    if comiendo:
        b.append(f'<path d="M440 380 C540 330 620 420 600 560 C590 660 560 760 560 840" stroke="{c1}" stroke-width="34" fill="none" stroke-linecap="round"/>')
        b.append(f'<circle cx="562" cy="860" r="36" fill="{c1}"/>')
        b.append('<path d="M560 880 C540 930 500 950 470 930 L480 900 C510 905 530 890 545 860 Z" fill="#f4e8d8"/>')
        b.append('<path d="M470 930 L480 900 L462 918 Z" fill="#1a1a1a"/>')
        b.append('<circle cx="575" cy="848" r="6" fill="#1a1a1a"/><circle cx="576" cy="846" r="2" fill="#fff"/>')
    else:
        b.append(f'<path d="M440 370 C520 330 520 240 470 200 C420 160 430 90 500 80" stroke="{c1}" stroke-width="34" fill="none" stroke-linecap="round"/>')
        b.append(f'<circle cx="510" cy="84" r="38" fill="{c1}"/>')
        b.append('<path d="M540 70 C600 70 630 100 630 140 C615 150 600 140 590 120 C575 110 555 108 540 104 Z" fill="#f4e8d8"/>')
        b.append('<path d="M630 140 C615 150 600 140 594 128 L612 122 C620 130 626 134 630 140 Z" fill="#1a1a1a"/>')
        b.append('<circle cx="520" cy="74" r="7" fill="#1a1a1a"/><circle cx="522" cy="72" r="2.5" fill="#fff"/>')
    return b


def flamenco(nombre, c1, c2, c3, comiendo=False, una_pata=True):
    d = lg("fl_c", (0, c1), (1, c2))
    guardar(nombre, "".join(_flamenco_partes(c1, c2, c3, comiendo, una_pata)), 700, 1100, d)


def pollito(nombre="pollito"):
    """Pollito de flamenco: bola de plumón gris con pico recto y patas gruesas."""
    w, h = 640, 700
    d = rg("po_c", (0, "#e8e8ea", 1), (0.7, "#a8a8b0", 1), (1, "#7a7a84", 1), cx=0.4, cy=0.35)
    r = random.Random(3)
    b = ['<ellipse cx="320" cy="680" rx="180" ry="16" fill="#000" opacity="0.3" filter="url(#blur8)"/>',
         '<path d="M270 540 L262 670 M370 540 L378 670" stroke="#6a6a72" stroke-width="26" stroke-linecap="round"/>',
         '<path d="M230 672 H300 M350 672 H420" stroke="#6a6a72" stroke-width="18" stroke-linecap="round"/>']
    for _ in range(120):  # borde de plumón
        a = r.uniform(0, 2 * math.pi)
        b.append(f'<circle cx="{320 + 200 * math.cos(a):.0f}" cy="{420 + 160 * math.sin(a):.0f}" r="{r.uniform(10, 22):.0f}" fill="#b8b8c0"/>')
    b += ['<ellipse cx="320" cy="420" rx="200" ry="160" fill="url(#po_c)"/>']
    for _ in range(70):
        a = r.uniform(0, 2 * math.pi)
        b.append(f'<circle cx="{440 + 100 * math.cos(a):.0f}" cy="{220 + 90 * math.sin(a):.0f}" r="{r.uniform(8, 16):.0f}" fill="#c0c0c8"/>')
    b += ['<ellipse cx="440" cy="220" rx="100" ry="90" fill="url(#po_c)"/>',
          '<path d="M520 200 L620 220 L522 246 Z" fill="#4a4a52"/>', '<path d="M520 222 L620 220" stroke="#2a2a30" stroke-width="3"/>',
          '<circle cx="470" cy="200" r="16" fill="#1a1a1a"/><circle cx="475" cy="194" r="5" fill="#fff"/>',
          '<path d="M180 380 Q260 330 360 350" stroke="#ffffff" stroke-width="8" fill="none" opacity="0.4"/>']
    guardar(nombre, "".join(b), w, h, d)


def gambita(nombre="gambita"):
    """Artemia / gamba diminuta vista al microscopio, curvada, rojo-anaranjada."""
    w, h = 700, 460
    d = lg("ga_c", (0, "#ffb070"), (1, "#e0502a"))
    b = ['<path d="M80 260 C120 120 380 80 560 160 C620 190 640 250 600 300 C500 360 300 380 160 330 Z" fill="url(#ga_c)" stroke="#a03018" stroke-width="5"/>']
    for k in range(7):
        x = 170 + k * 60
        b.append(f'<path d="M{x} {150 - k * 3} Q{x + 18} 240 {x} {340 - k * 4}" stroke="#a03018" stroke-width="4" fill="none" opacity="0.7"/>')
        b.append(f'<path d="M{x + 10} 330 L{x - 10} 410" stroke="#e0603a" stroke-width="6" stroke-linecap="round"/>')
    b += ['<path d="M560 170 L690 90 M570 180 L690 150" stroke="#e0603a" stroke-width="5" stroke-linecap="round"/>',
          '<circle cx="575" cy="200" r="14" fill="#1a1a1a"/>', '<path d="M80 260 L10 220 L30 300 Z" fill="#e0603a"/>',
          '<path d="M180 140 Q330 100 480 140" stroke="#ffffff" stroke-width="8" fill="none" opacity="0.4"/>']
    guardar(nombre, "".join(b), w, h, d)


def algas(nombre="algas"):
    """Células de alga microscópicas, rojas y anaranjadas, con brillo."""
    w, h = 800, 800
    r = random.Random(6)
    b = []
    for _ in range(26):
        x, y, s = r.uniform(80, 720), r.uniform(80, 720), r.uniform(30, 70)
        c = r.choice(["#ff6a4a", "#ff9a3a", "#e8403a", "#ffb84a"])
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{s:.0f}" ry="{s * 0.8:.0f}" fill="{c}" opacity="0.85" stroke="#8a2a1a" stroke-width="3"/>'
                 f'<circle cx="{x - s * 0.3:.0f}" cy="{y - s * 0.3:.0f}" r="{s * 0.25:.0f}" fill="#ffffff" opacity="0.5"/>')
    guardar(nombre, "".join(b), w, h)


def zanahoria(nombre="zanahoria"):
    w, h = 400, 900
    d = lg("za_c", (0, "#ffa040"), (1, "#e06010"), x2=1, y2=0)
    b = ['<path d="M200 880 C170 700 110 400 110 260 C110 200 290 200 290 260 C290 400 230 700 200 880 Z" fill="url(#za_c)"/>',
         *[f'<path d="M{130 + k * 5} {320 + k * 90} q40 10 70 0" stroke="#b04a08" stroke-width="5" fill="none" opacity="0.6"/>' for k in range(6)],
         '<path d="M200 230 C160 120 140 60 120 20 M200 230 C200 120 210 60 200 10 M200 230 C240 120 270 70 290 30" stroke="#3a9a3a" stroke-width="22" stroke-linecap="round" fill="none"/>',
         '<path d="M140 280 C140 420 170 560 190 700" stroke="#ffd8a0" stroke-width="10" fill="none" opacity="0.5"/>']
    guardar(nombre, "".join(b), w, h, d)


def pluma(nombre, c1, c2):
    w, h = 400, 1000
    d = lg(f"{nombre}_g", (0, c1), (1, c2))
    b = [f'<path d="M200 980 C200 700 200 300 200 40" stroke="#f4ece6" stroke-width="10" fill="none"/>',
         f'<path d="M200 60 C80 150 50 400 90 640 C120 760 180 820 200 840 C220 820 290 760 320 640 C360 400 320 150 200 60 Z" fill="url(#{nombre}_g)"/>']
    for k in range(18):
        y = 120 + k * 38
        b.append(f'<path d="M200 {y} q-90 30 -120 70 M200 {y} q90 30 120 70" stroke="#ffffff" stroke-width="2.5" fill="none" opacity="0.35"/>')
    b.append(f'<path d="M200 60 C200 300 200 600 200 840" stroke="#f4ece6" stroke-width="8"/>')
    guardar(nombre, "".join(b), w, h, d)


def colador(nombre="colador"):
    w, h = 900, 560
    d = lg("cl_c", (0, "#e8eaee"), (1, "#8a909a"))
    b = ['<path d="M110 160 C110 480 640 520 680 160 Z" fill="url(#cl_c)" stroke="#5a606a" stroke-width="6"/>',
         '<ellipse cx="395" cy="160" rx="290" ry="40" fill="#c8ccd4" stroke="#5a606a" stroke-width="6"/>',
         '<path d="M680 160 L880 110" stroke="#5a606a" stroke-width="26" stroke-linecap="round"/>']
    for k in range(60):
        x = 170 + (k % 12) * 40; y = 230 + (k // 12) * 45
        if (x - 395) ** 2 / 290 ** 2 + (y - 160) ** 2 / 300 ** 2 < 0.9:
            b.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#3a3e46"/>')
    guardar(nombre, "".join(b), w, h, d)


def nido(nombre="nido"):
    """Nido de barro en cono truncado, típico de los flamencos."""
    w, h = 800, 500
    d = lg("ni_c", (0, "#a8805a"), (1, "#5a4028"))
    b = ['<ellipse cx="400" cy="470" rx="360" ry="28" fill="#000" opacity="0.3" filter="url(#blur8)"/>',
         '<path d="M90 460 L220 140 L580 140 L710 460 Z" fill="url(#ni_c)"/>', '<ellipse cx="400" cy="140" rx="180" ry="36" fill="#6a4a30"/>',
         '<ellipse cx="400" cy="134" rx="150" ry="24" fill="#4a3220"/>',
         *[f'<path d="M{130 + k * 40} {400 - k * 6} q30 -10 60 0" stroke="#3a2818" stroke-width="4" fill="none" opacity="0.5"/>' for k in range(12)]]
    guardar(nombre, "".join(b), w, h, d)


def bg_microscopio(nombre="bg_micro"):
    """Fondo de campo de microscopio: círculo luminoso con viñeta negra."""
    d = rg(f"{nombre}_g", (0, "#d8f4e8", 1), (0.6, "#8ad0b8", 1), (0.95, "#2a5a4a", 1), (1, "#000000", 1))
    b = ['<rect width="1080" height="1920" fill="#000"/>', f'<circle cx="540" cy="1000" r="520" fill="url(#{nombre}_g)"/>']
    r = random.Random(9)
    for _ in range(50):
        b.append(f'<circle cx="{540 + r.uniform(-420, 420):.0f}" cy="{1000 + r.uniform(-420, 420):.0f}" r="{r.uniform(3, 9):.0f}" fill="#ffffff" opacity="0.3"/>')
    b.append(grano())
    guardar(nombre, "".join(b), defs=d)


def gota_leche(nombre="gota_leche"):
    w, h = 400, 560
    d = rg("gl_c", (0, "#ff8a8a", 1), (0.6, "#e0202a", 1), (1, "#8a0a14", 1), cx=0.35, cy=0.6)
    b = ['<path d="M200 20 C200 20 60 250 60 380 C60 470 130 540 200 540 C270 540 340 470 340 380 C340 250 200 20 200 20 Z" fill="url(#gl_c)"/>',
         '<ellipse cx="140" cy="380" rx="26" ry="60" fill="#ffffff" opacity="0.5"/>']
    guardar(nombre, "".join(b), w, h, d)


# ====================================================================== GENERAR
def generar(dirsvg):
    ilus.generar(dirsvg)
    # piezas de lotes anteriores (cada módulo se carga por ruta con un nombre único)
    m18 = _mod("lotes/2026-11-18-manana/generadores/ilus_02.py", "_ilus_1118m_02"); ilus.OUT = dirsvg
    m18.iss(); m18.bg_orbita(); m18.bg_noche_ciudades(); m18.casco(); m18.ojo_simple()
    m18.bg_montanas("bg_montanas_dia", ("#cfe6ff", "#8ab8e8", "#4a7ab8"), 9)
    t18 = _mod("lotes/2026-11-18-tarde/generadores/ilus_tarde.py", "_ilus_1118t"); ilus.OUT = dirsvg
    t18.montana(); t18.despertador()
    t17 = _mod("lotes/2026-11-17-tarde/generadores/ilus_tarde.py", "_ilus_1117t"); ilus.OUT = dirsvg
    t17.cara_perfil()
    m20 = _mod("lotes/2026-11-20-manana/generadores/ilus_1120m.py", "_ilus_1120m"); ilus.OUT = dirsvg
    m20.velocimetro(); m20.aguja_vel(); m20.bg_estudio()
    ilus.OUT = dirsvg
    # 01
    bg_amanecer_orbital(); bg_amanecer_orbital("bg_amanecer_orbital2", 1.4); ventanilla(); campo_futbol(); torre_reloj(); manecillas(); bg_londres_noche(); orbita_luna()
    # 02
    bg_cumbre(); bg_vista_africa(); bg_vista_africa("bg_vista_africa_sin", 0.0); tierra_arco(); persona_pie(); persona_pie("persona_pie_clara", "#f4f0e8")
    excursionista(); mapa_estrecho(); bg_playa(); corona(); lapida_nieve(); prismaticos()
    # 03
    bg_laguna(); bg_laguna("bg_laguna_tarde", "tarde"); pollito(); gambita(); algas(); zanahoria(); colador(); nido(); bg_microscopio(); gota_leche()
    pluma("pluma_rosa", "#ffb0c0", "#e8507a"); pluma("pluma_gris", "#d8d8dc", "#9a9aa2")
    flamenco("flamenco", "#ff8aa8", "#f05a82", "#e0607a")
    flamenco("flamenco_comiendo", "#ff8aa8", "#f05a82", "#e0607a", comiendo=True, una_pata=False)
    flamenco("flamenco_palido", "#f8eef0", "#e8d0d6", "#d8a0aa")
    flamenco("flamenco_joven", "#d8d0d4", "#b0a8ae", "#7a7078")
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
