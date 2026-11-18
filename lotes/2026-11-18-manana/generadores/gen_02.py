"""02 · Esta muralla no se ve (la Gran Muralla desde el espacio) — método denso. Lote 2026-11-18-manana, Agente 08:00 (Nico).
Experimento del lote: gancho de negación. Se omite «Nadie había subido nunca.» (palabras 42–45) para no pasar de 60 s.
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_02  # noqa: E402

SVG = ilus_02.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG, omitir=[(42, 46)])

PAPEL = ["#3a2a1a", "#1a120a"]
OCRE = ["#b08a5a", "#6a4a2a"]
ROJO = "#ff2d55"


def tachon(x, y, t0, tam=520, color=ROJO, z=0.8):
    """Aspa roja que se dibuja en dos trazos (sin glifos)."""
    h = tam / 2
    return [flecha([[x - h, y - h], [x + h, y + h]], t0, t0 + 0.18, color, 26, punta=False, z=z),
            flecha([[x + h, y - h], [x - h, y + h]], t0 + 0.14, t0 + 0.32, color, 26, punta=False, z=z)]


def iss_fondo(d, i0=80, i1=104):
    """La Estación Espacial cruza el fondo de todos los planos de ese tramo (detalle que dura)."""
    return IMG("iss", ancho=300, z=0.15, keys=recorrido(v.w(i0), v.w(i1), (1250, 300), (-200, 520), d))


def nubes(d, sem=1, y=520):
    r = random.Random(sem)
    return [{"tipo": "forma", "forma": "elipse", "ancho": r.uniform(260, 420), "alto": r.uniform(50, 80), "relleno": "#fff4e6", "z": 0.12, "op": 0.35,
             "keys": recorrido(v.w(0) - 4 + k * 3, v.w(66) + 6, (r.uniform(-300, 200), y + k * 70), (r.uniform(1200, 1500), y + k * 70), d)} for k in range(3)]


# ================================================================== PLANOS
@v.plano(0, "gancho: la muralla serpentea por las montañas y la tacha un aspa roja")
def _(d):
    return P(["#4a3a6a", "#262a30"], [BG("bg_montanas"), *nubes(d, 1),
             IMG("muralla", ancho=1300, x=540, y=960, z=0.4, keys=arranque(540, 960, d, "abajo", 220, 30)),
             polvo("#fff1c8", 30, (0, 500, 1080, 1500), 2),
             *tachon(540, 1150, 0.9, 560)],
             cam(1.25, 1.02, (520, 1150), (540, 1000)), vineta=0.6,
             sfx=[(0.0, "whoosh", -14, {"dur": 0.5}), (0.9, "golpe", -12), (1.05, "zap", -18)])


@v.plano(5, "es la Gran Muralla China (torre de vigilancia)")
def _(d):
    return P(["#4a7ab8", "#cfe6ff"], [BG("bg_montanas_dia"), *nubes(d, 2, 600),
             IMG("muralla_dia", ancho=1400, x=600, y=1020, z=0.3),
             IMG("torre", ancho=640, x=540, y=1180, z=0.55, keys=aparece(0.0, 0.45) + [{"t": d, "y": 1150}])],
             cam(1.0, 1.08, (540, 1100), (540, 1060)), "desenfoque",
             hud=[contexto(0.05, d - 0.05, "GRAN MURALLA CHINA")], sfx=[(0.05, "golpe", -18)])


@v.plano(10, "desde el espacio (la Tierra se aleja)")
def _(d):
    return P(ESPACIO, [BG("bg_esp_violeta"), tierra(540, 1050, 900, keys=[{"t": 0, "escala": 1.6}, {"t": d, "escala": 1.0, "ease": "salida"}]),
             IMG("satelite", ancho=200, z=0.6, keys=[{"t": 0, "x": 100, "y": 500}, {"t": d, "x": 300, "y": 470}])],
             cam(1.0, 1.04), "zoom", sfx=[(0.02, "whoosh", -16, {"dur": 0.5})])


@v.plano(13, "a simple vista: el ojo")
def _(d):
    return P(["#1a1a2a", "#0a0a12"], [brillo(540, 1000, 600, "#ffd8a8", 0.2),
             IMG("ojo_simple", ancho=900, x=540, y=1000, z=0.5, keys=[{"t": 0, "ey": 0.1}, {"t": 0.25, "ey": 1.0, "ease": "salida"}, {"t": d, "escala": 1.06}])],
             cam(1.0, 1.06), "corte", hud=[amarillo(0.02, d - 0.02, "SIMPLE VISTA", y=560, color=CIAN, tam=84)], sfx=[(0.1, "pop", -18)])


@v.plano(16, "no se distingue: la lupa busca y no encuentra")
def _(d):
    return P(OCRE, [BG("bg_terreno"), IMG("franja", ancho=1180, x=540, y=960, z=0.1),
             IMG("lupa", ancho=380, z=0.6, keys=[{"t": 0, "x": 300, "y": 1300}, {"t": d * 0.5, "x": 760, "y": 900, "ease": "suave"}, {"t": d, "x": 420, "y": 760, "ease": "suave"}]),
             rotulo(d * 0.55, d - 0.05, "?", tam=200, color="#ffffff", capsula="#c0392be6", y=560)],
             cam(1.0, 1.05), "desenfoque", sfx=[(0.1, "roce", -22), (d * 0.55, "pop", -18)])


@v.plano(19, "¿de dónde sale el mito? (la carta)")
def _(d):
    return P(PAPEL, [brillo(540, 1000, 600, "#ffd27a", 0.35), polvo("#ffe8b0", 25, (100, 400, 980, 1600), 3),
             IMG("carta_1754", ancho=720, x=540, y=1060, z=0.5, rot=-4, keys=[{"t": 0, "y": 1500, "rot": 10, "op": 0}, {"t": 0.4, "y": 1060, "rot": -4, "op": 1, "ease": "elastico"}])],
             cam(1.0, 1.06, (540, 1060), (540, 1040)), "desenfoque", hud=[amarillo(0.1, d - 0.05, "EL MITO", y=560, color=AMBAR)], sfx=[(0.05, "roce", -16)])


@v.plano(24, "en 1754")
def _(d):
    return P(PAPEL, [brillo(540, 1000, 500, "#ffd27a", 0.3), IMG("carta_1754", ancho=900, x=560, y=1200, z=0.4, rot=-4),
             IMG("pluma", ancho=200, x=760, y=1000, z=0.6, rot=25, anim={"balanceo": [4, 0.6]})],
             cam(1.05, 1.12, (540, 1100), (560, 1080)),
             hud=[contador(0.05, d - 0.05, 1700, 1754, d * 0.6, "", tam=150, y=560, borde=AMBAR, miles=False)], sfx=[(0.05, "subida", -18, {"dur": d * 0.6})])


@v.plano(30, "un inglés escribe en una carta (la pluma escribe)")
def _(d):
    ks = [{"t": 0, "x": 300, "y": 900}]
    for k in range(1, 9):
        ks.append({"t": d * k / 9, "x": 300 + 50 * k, "y": 900 + (16 if k % 2 else -16), "ease": "suave"})
    return P(PAPEL, [IMG("carta_1754", ancho=1500, x=640, y=1300, z=0.4, rot=-4),
             IMG("pluma", ancho=260, z=0.6, rot=28, keys=ks),
             flecha([[230, 1010], [300 + 50 * 8, 1010]], 0.0, d, "#2a1a10", 5, punta=False, z=0.5)],
             cam(1.0, 1.05, (540, 1000), (600, 1000)), "corte", hud=[contexto(0.05, d - 0.05, "INGLATERRA")], sfx=[(0.05, "roce", -20), (d * 0.5, "roce", -22)])


@v.plano(36, "que se veía desde la Luna")
def _(d):
    return P(ESPACIO, [BG("bg_esp_petroleo"), luna(740, 900, 420, keys=aparece(0.0, 0.4)), tierra(300, 1450, 480),
             flecha([[360, 1230], [520, 1080], [600, 1030]], 0.2, d * 0.8, AMBAR, 7, disc=[18, 14]),
             IMG("ojo_simple", ancho=260, x=740, y=900, z=0.6, keys=[{"t": d * 0.6, "op": 0, "escala": 0.5}, {"t": d * 0.75, "op": 1, "escala": 1, "ease": "elastico"}])],
             cam(1.0, 1.05), "desenfoque", hud=[amarillo(0.1, d - 0.05, "¿DESDE LA LUNA?", y=520, color=CIAN, tam=84)], sfx=[(0.1, "brillo", -20)])


@v.plano(46, "mide miles de kilómetros (la muralla larguísima)")
def _(d):
    return P(["#4a7ab8", "#cfe6ff"], [BG("bg_montanas_dia"), *nubes(d, 3, 580),
             IMG("muralla_dia", ancho=1900, x=540, y=1000, z=0.4, keys=[{"t": 0, "x": 760}, {"t": d, "x": 320, "ease": "suave"}]),
             flecha([[80, 1580], [1000, 720]], 0.2, d * 0.85, LIMA, 8)],
             cam(1.0, 1.06, (540, 1100), (540, 1040)), "barrido", hud=[rotulo(0.1, d - 0.05, "MILES DE KM", tam=104, color="#141414", capsula="#b6ff5ae6", y=560)],
             sfx=[(0.05, "whoosh", -16, {"dur": 0.6})])


@v.plano(51, "pero en muchos tramos (un tramo de cerca, de lado)")
def _(d):
    return P(["#4a7ab8", "#cfe6ff"], [BG("bg_montanas_dia"), IMG("muralla_dia", ancho=3600, x=900, y=300, z=0.4, keys=[{"t": 0, "x": 980}, {"t": d, "x": 860, "ease": "suave"}]),
             *nubes(d, 5, 520)],
             cam(1.0, 1.05), "zoom", sfx=[(0.02, "whoosh", -18, {"dur": 0.4})])


@v.plano(55, "cuatro o cinco metros de ancho (cota)")
def _(d):
    return P(OCRE, [BG("bg_terreno"), IMG("muralla_cenital", ancho=1700, x=540, y=1050, z=0.4),
             flecha([[200, 1050], [200, 800]], 0.15, 0.5, CIAN, 9), flecha([[200, 1050], [200, 1300]], 0.15, 0.5, CIAN, 9),
             flecha([[120, 830], [400, 830]], 0.1, 0.3, "#ffffff", 5, punta=False), flecha([[120, 1270], [400, 1270]], 0.1, 0.3, "#ffffff", 5, punta=False)],
             cam(1.0, 1.06, (540, 1050), (480, 1050)), hud=[rotulo(0.1, d - 0.05, "4–5 METROS", tam=110, color="#141414", capsula="#2ff3ffe6", y=560)],
             sfx=[(0.15, "trazo", -20)])


@v.plano(62, "como una carretera estrecha (pasa un coche)")
def _(d):
    return P(OCRE, [BG("bg_terreno"), IMG("muralla_cenital", ancho=1700, x=540, y=820, z=0.4), IMG("carretera", ancho=1700, x=540, y=1240, z=0.4),
             IMG("coche", ancho=300, y=1240, z=0.55, keys=[{"t": 0, "x": -150}, {"t": d, "x": 900, "ease": "lineal"}]),
             *lineas_vel(400, 1240, 4, "#ffffffaa")],
             cam(1.0, 1.04, (540, 1030), (560, 1030)), "barrido", hud=[rotulo(0.1, d - 0.05, "UN CARRIL", tam=104, color="#141414", capsula="#ffd23fe6", y=560)],
             sfx=[(0.05, "whoosh", -14, {"dur": 0.8})])


@v.plano(66, "de piedra y tierra (ladrillos de cerca)")
def _(d):
    return P(["#9a7048", "#5a3a20"], [IMG("torre", ancho=2200, x=600, y=1300, z=0.4, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.08, "ease": "suave"}]),
             polvo("#e8d0a8", 40, (100, 600, 980, 1700), 6),
             IMG("torre", ancho=360, x=860, y=1500, z=0.6, keys=aparece(d * 0.4, 0.35))],
             cam(1.0, 1.06, (540, 1100), (560, 1080)), "desenfoque", hud=[rotulo(0.1, d - 0.05, "PIEDRA Y TIERRA", tam=84, color="#ffffff", capsula="#3a2410e6", y=560)],
             sfx=[(0.05, "golpe", -20), (d * 0.4, "pop", -20)])


@v.plano(72, "del mismo color que el suelo: la franja amarilla se apaga y la muralla desaparece")
def _(d):
    return P(OCRE, [BG("bg_terreno"), IMG("franja", ancho=1180, x=540, y=960, z=0.1),
             IMG("franja_marcada", ancho=1180, x=540, y=960, z=0.12, keys=[{"t": 0, "op": 1}, {"t": d * 0.35, "op": 1}, {"t": d * 0.8, "op": 0, "ease": "suave"}]),
             {"tipo": "forma", "forma": "rect", "ancho": 140, "alto": 140, "relleno": "#b08a5a", "x": 300, "y": 1300, "z": 0.5, "rot": 12, "keys": aparece(0.1, 0.3)},
             {"tipo": "forma", "forma": "rect", "ancho": 140, "alto": 140, "relleno": "#a8845a", "x": 520, "y": 1300, "z": 0.5, "rot": -8, "keys": aparece(0.3, 0.3)},
             polvo("#fff1c8", 30, (0, 400, 1080, 1700), 11), IMG("lupa", ancho=300, z=0.7, keys=[{"t": 0, "x": 800, "y": 1500}, {"t": d, "x": 640, "y": 1000, "ease": "suave"}])],
             cam(1.0, 1.05), hud=[rotulo(0.1, d - 0.05, "MISMO COLOR", tam=104, color="#ffffff", capsula="#0d1330d8", borde=AMBAR, y=560)],
             sfx=[(0.1, "pop", -20), (0.3, "pop", -20), (d * 0.5, "brillo", -22)])


@v.plano(80, "¿desde dónde miran los astronautas? (la estación aparece)")
def _(d):
    return P(ESPACIO, [BG("bg_esp_violeta"), iss_fondo(d), tierra(540, 2000, 1900, giro=2),
             IMG("iss", ancho=900, x=540, y=1000, z=0.5, keys=arranque(540, 1000, d, "derecha", 300, 40)),
             fugaz(0.3, 900, 300, 600, 500)],
             cam(1.0, 1.06), "zoom", hud=[amarillo(0.1, d - 0.05, "¿DESDE DÓNDE?", y=560, color=MAGENTA)], sfx=[(0.05, "senal", -22)])


@v.plano(85, "la Estación Espacial vuela")
def _(d):
    return P(["#02030a", "#0a1a30"], [BG("bg_orbita"),
             IMG("iss", ancho=760, z=0.5, keys=[{"t": 0, "x": 900, "y": 700}, {"t": d, "x": 300, "y": 760, "ease": "lineal"}], anim={"balanceo": [2, 3]}),
             brillo(540, 1300, 500, "#7ad0ff", 0.15)],
             cam(1.0, 1.04), "desenfoque", hud=[contexto(0.05, d - 0.05, "ESTACIÓN")], sfx=[(0.05, "senal", -24)])


@v.plano(89, "a unos 400 km (regla de altura)")
def _(d):
    return P(["#02030a", "#0a1a30"], [BG("bg_orbita"), IMG("iss", ancho=420, x=700, y=640, z=0.5, anim={"balanceo": [2, 3]}),
             flecha([[300, 1700], [300, 700]], 0.1, d * 0.7, CIAN, 9, disc=[22, 16]),
             {"tipo": "forma", "forma": "rect", "ancho": 120, "alto": 8, "relleno": "#ffffff", "x": 300, "y": 1700, "z": 0.5}],
             cam(1.0, 1.05, (540, 1100), (540, 1000)),
             hud=[contador(0.05, d - 0.05, 0, 400, d * 0.7, "KM", tam=130, y=560, borde=CIAN)], sfx=[(0.05, "subida", -16, {"dur": d * 0.7})])


@v.plano(93, "desde ahí (mirando abajo desde la estación)")
def _(d):
    return P(["#02030a", "#0a1a30"], [BG("bg_orbita"), IMG("iss", ancho=1500, x=540, y=420, z=0.6, keys=[{"t": 0, "x": 640}, {"t": d, "x": 480, "ease": "lineal"}]),
             flecha([[540, 700], [540, 1450]], 0.05, d * 0.9, CIAN, 8, disc=[18, 14])],
             cam(1.1, 1.0), "zoom", sfx=[(0.02, "whoosh", -18, {"dur": 0.4})])


@v.plano(95, "una franja tan fina (se dibuja y se adelgaza)")
def _(d):
    return P(OCRE, [BG("bg_terreno"), IMG("franja", ancho=1180, x=540, y=960, z=0.1),
             IMG("franja_marcada", ancho=1180, x=540, y=960, z=0.12, keys=[{"t": 0, "op": 1}, {"t": d, "op": 0.15, "ease": "suave"}]),
             senala(700, 1180, 0.2, d - 0.05, 120, MAGENTA), *nubes(d, 7, 1300), polvo("#fff1c8", 25, (0, 500, 1080, 1700), 9),
             IMG("lupa", ancho=300, z=0.7, keys=[{"t": 0, "x": 950, "y": 1500}, {"t": d, "x": 760, "y": 1250, "ease": "suave"}])],
             cam(1.0, 1.08, (540, 1000), (640, 1100)), "corte", hud=[rotulo(0.1, d - 0.05, "TAN FINA", tam=110, color="#ffffff", capsula="#a0187ae6", y=560)], sfx=[(0.2, "pop", -20)])


@v.plano(99, "se pierde en el paisaje (zoom hacia fuera, nubes encima)")
def _(d):
    r = random.Random(9)
    nub = [{"tipo": "forma", "forma": "elipse", "ancho": r.uniform(300, 500), "alto": r.uniform(80, 140), "relleno": "#ffffff", "z": 0.6, "op": 0.55,
            "keys": [{"t": 0, "x": r.uniform(-100, 1100), "y": r.uniform(400, 1600)}, {"t": d, "x": r.uniform(-100, 1100), "y": r.uniform(400, 1600), "ease": "lineal"}]} for _ in range(5)]
    return P(OCRE, [BG("bg_terreno"), IMG("franja", ancho=1180, x=540, y=960, z=0.1), *nub,
             IMG("lupa", ancho=320, z=0.7, keys=[{"t": 0, "x": 760, "y": 1300}, {"t": d * 0.5, "x": 300, "y": 900, "ease": "suave"}, {"t": d, "x": 680, "y": 700, "ease": "suave"}])],
             cam(1.25, 1.0), "desenfoque", hud=[rotulo(0.1, d - 0.05, "SE PIERDE", tam=110, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.1, "roce", -22)])


@v.plano(104, "en 2003 (la cápsula despega)")
def _(d):
    return P(ESPACIO, [BG("bg_esp_ambar"), tierra(540, 1900, 1500, giro=2), iss_fondo(d),
             IMG("capsula", ancho=700, x=540, z=0.5, keys=[{"t": 0, "y": 1500, "escala": 0.6}, {"t": d, "y": 1000, "escala": 1.0, "ease": "salida"}]),
             brillo(540, 1250, 200, "#ffb84a", 0.6, 0.45, keys=[{"t": 0, "intensidad": 1}, {"t": d, "intensidad": 0.1}])],
             cam(1.0, 1.05), "corte", hud=[contador(0.05, d - 0.05, 2000, 2003, d * 0.6, "", tam=150, y=560, borde=AMBAR, miles=False)],
             sfx=[(0.05, "subida", -16, {"dur": d * 0.8})])


@v.plano(108, "el primer astronauta chino (casco, sin cara)")
def _(d):
    return P(["#0a1020", "#02030a"], [BG("bg_esp_petroleo"), IMG("casco", ancho=760, x=540, y=1100, z=0.5, keys=aparece(0.0, 0.45) + [{"t": d, "escala": 1.05}], anim={"balanceo": [2, 1.6]}),
             brillo(540, 1050, 420, "#ffd88a", 0.25), polvo("#ffffff", 30, (0, 300, 1080, 1700), 8, "estrellas"), fugaz(0.6, 950, 380, 650, 620),
             IMG("capsula", ancho=180, z=0.3, keys=[{"t": 0, "x": 1100, "y": 1650}, {"t": d, "x": 700, "y": 1550, "ease": "lineal"}])],
             cam(1.0, 1.06, (540, 1100), (540, 1060)), "desenfoque",
             hud=[rotulo(0.1, d - 0.05, "1.ER ASTRONAUTA CHINO", tam=74, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "brillo", -20)])


@v.plano(114, "dio 14 vueltas a la Tierra")
def _(d):
    import math
    ks = []
    for k in range(29):
        a = -math.pi / 2 + k * 2 * math.pi / 28 * 2
        ks.append({"t": d * k / 28, "x": 540 + 400 * math.cos(a), "y": 1050 + 400 * math.sin(a), "ease": "lineal"})
    return P(ESPACIO, [BG("bg_esp_violeta"), tierra(540, 1050, 600, giro=30),
             {"tipo": "forma", "forma": "elipse", "ancho": 800, "alto": 800, "relleno": "#ffffff", "op_relleno": 0, "grosor": 4, "borde": "#ffffff66", "x": 540, "y": 1050, "z": 0.45},
             IMG("capsula", ancho=200, z=0.6, keys=ks)],
             cam(1.0, 1.04), "zoom", hud=[contador(0.05, d - 0.05, 1, 14, d * 0.8, "VUELTAS", tam=120, y=560, borde=MAGENTA)],
             sfx=[(0.05, "subida", -18, {"dur": d * 0.8})])


@v.plano(120, "al volver (la cápsula baja con paracaídas; las nubes suben)")
def _(d):
    r = random.Random(12)
    nub = [{"tipo": "forma", "forma": "elipse", "ancho": r.uniform(300, 480), "alto": r.uniform(70, 110), "relleno": "#ffffff", "z": 0.3 + 0.4 * (k % 2), "op": 0.6,
            "keys": [{"t": 0, "x": r.uniform(0, 1080), "y": 1800 + k * 260}, {"t": d, "x": r.uniform(0, 1080), "y": 200 + k * 260, "ease": "lineal"}]} for k in range(4)]
    bal = [{"t": 0, "rot": -4}, {"t": d * 0.5, "rot": 4, "ease": "suave"}, {"t": d, "rot": -3, "ease": "suave"}]
    return P(["#4a7ab8", "#cfe6ff"], [
             IMG("descenso", ancho=700, x=540, y=1000, z=0.5, keys=bal), *nub],
             cam(1.0, 1.04), "corte", sfx=[(0.02, "whoosh", -18, {"dur": 0.6})])


@v.plano(125, "no vio la Muralla (el visor refleja la franja y el aspa)")
def _(d):
    return P(["#0a1020", "#02030a"], [BG("bg_esp_petroleo"), IMG("casco", ancho=1000, x=540, y=1050, z=0.5, keys=[{"t": 0, "escala": 1.1}, {"t": d, "escala": 1.0, "ease": "salida"}]),
             *tachon(540, 1000, 0.25, 420)],
             cam(1.0, 1.04), "corte", hud=[rotulo(0.1, d - 0.05, "NO LA VIO", tam=120, color="#ffffff", capsula="#c0392be6", y=560)],
             sfx=[(0.25, "golpe", -14), (0.4, "zap", -20)])


@v.plano(129, "al año siguiente: 2004")
def _(d):
    return P(ESPACIO, [BG("bg_esp_ambar"), iss_fondo(d), IMG("iss", ancho=700, x=540, y=1050, z=0.5, anim={"balanceo": [3, 2]}, keys=aparece(0.0, 0.35))],
             cam(1.0, 1.05), "corte", hud=[contador(0.05, d - 0.05, 2003, 2004, d * 0.5, "", tam=150, y=560, borde=CIAN, miles=False)], sfx=[(0.05, "tic", -18)])


@v.plano(132, "un astronauta de la NASA la fotografió (flash desde la estación)")
def _(d):
    return P(["#02030a", "#0a1a30"], [BG("bg_orbita"), IMG("iss", ancho=520, x=700, y=620, z=0.5, anim={"balanceo": [2, 3]}),
             flecha([[640, 700], [420, 1450]], 0.2, d * 0.6, LIMA, 7, disc=[18, 14]),
             brillo(640, 680, 260, "#ffffff", 0.0, 0.7, keys=[{"t": d * 0.55, "intensidad": 0}, {"t": d * 0.6, "intensidad": 1.2}, {"t": d * 0.8, "intensidad": 0}])],
             cam(1.0, 1.05), "desenfoque", hud=[amarillo(0.1, d - 0.05, "¡CLIC!", y=560, color=LIMA)], sfx=[(d * 0.58, "brillo", -14), (d * 0.6, "pop", -16)])


@v.plano(139, "pero con teleobjetivo (el objetivo se alarga)")
def _(d):
    return P(["#1a1e26", "#0a0c10"], [brillo(540, 1000, 600, "#7ad0ff", 0.15),
             IMG("camara_tele", ancho=1000, x=540, y=1050, z=0.5, keys=[{"t": 0, "ex": 0.6, "x": 380}, {"t": d * 0.5, "ex": 1.0, "x": 540, "ease": "elastico"}]),
             senala(950, 1050, d * 0.5, d - 0.05, 120, CIAN)],
             cam(1.0, 1.06), "corte", hud=[rotulo(0.1, d - 0.05, "TELEOBJETIVO", tam=100, color="#141414", capsula="#2ff3ffe6", y=560)],
             sfx=[(0.1, "roce", -18), (d * 0.5, "ding", -20)])


@v.plano(142, "micro: ¿qué sí? (el ojo late)")
def _(d):
    return P(["#1a1a2a", "#0a0a12"], [IMG("ojo_simple", ancho=1100, x=540, y=980, z=0.5, keys=late(0.05, 1, 0.08, 0.3))],
             cam(1.1, 1.2), "corte", sfx=[(0.02, "pop", -18)])


@v.plano(146, "las ciudades de noche")
def _(d):
    return P(["#01020a", "#04060c"], [BG("bg_noche"), brillo(400, 1300, 260, "#ffb84a", 0.5, 0.3, pulso=[0.2, 1.2]), brillo(760, 1000, 200, "#ffb84a", 0.4, 0.3, pulso=[0.2, 0.9]),
             IMG("iss", ancho=260, z=0.5, keys=[{"t": 0, "x": 1000, "y": 500}, {"t": d, "x": 700, "y": 560, "ease": "lineal"}])],
             cam(1.0, 1.08, (540, 1200), (540, 1150)), "desenfoque", hud=[amarillo(0.1, d - 0.05, "CIUDADES DE NOCHE", y=560, color=AMBAR, tam=80)],
             sfx=[(0.05, "brillo", -20)])


@v.plano(150, "¿y desde la Luna? (la Tierra pequeña sobre el horizonte)")
def _(d):
    return P(ESPACIO, [BG("bg_superficie"), tierra(760, 600, 260, keys=[{"t": 0, "y": 760}, {"t": d, "y": 600, "ease": "salida"}])],
             cam(1.0, 1.04, (540, 960), (600, 900)), "desenfoque", hud=[amarillo(0.1, d - 0.05, "¿DESDE LA LUNA?", y=520, color=CIAN, tam=84)],
             sfx=[(0.05, "senal", -22)])


@v.plano(154, "nada hecho por nosotros (la Tierra diminuta; bucle hacia la muralla)")
def _(d):
    return P(ESPACIO, [BG("bg_superficie"), tierra(600, 640, 160),
             senala(600, 640, 0.15, d * 0.7, 110, ROJO)],
             cam(1.3, 1.0, (600, 700), (560, 900)), "zoom", hud=[rotulo(0.1, d * 0.7, "NADA", tam=150, color="#ffffff", capsula="#c0392be6", y=1080)],
             sfx=[(0.1, "impacto", -12)], energia=0.4)


# ------------------------------------------------------------------ micro planos (golpes de 0,3–0,7 s)
@v.plano(50, "micro: sí (la muralla al atardecer, de punta a punta)")
def _(d):
    return P(["#4a3a6a", "#262a30"], [BG("bg_montanas"), IMG("muralla", ancho=1100, x=540, y=980, z=0.4, keys=[{"t": 0, "escala": 1.3}, {"t": d, "escala": 1.0, "ease": "salida"}])],
             cam(1.0, 1.03), "zoom", sfx=[(0.02, "golpe", -18)])


@v.plano(61, "micro: de ancho (la cota se cierra sobre el paseo)")
def _(d):
    return P(OCRE, [BG("bg_terreno"), IMG("muralla_cenital", ancho=3200, x=540, y=1000, z=0.4, rot=90),
             flecha([[260, 1000], [480, 1000]], 0.0, d * 0.6, MAGENTA, 10), flecha([[820, 1000], [600, 1000]], 0.0, d * 0.6, MAGENTA, 10)],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "trazo", -18)])


@v.plano(145, "micro: se ve (destello de luces de una ciudad)")
def _(d):
    return P(["#01020a", "#04060c"], [BG("bg_noche"), brillo(540, 1200, 420, "#ffb84a", 0.9, 0.3, keys=[{"t": 0, "intensidad": 0.2}, {"t": d * 0.5, "intensidad": 1.1}, {"t": d, "intensidad": 0.6}])],
             cam(1.6, 1.4, (540, 1300), (540, 1250)), "corte", sfx=[(0.02, "brillo", -18)])

v.construir("2026-11-18-manana-02-gran-muralla", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 41, "db": -13},
            claves=["muralla", "espacio", "vista", "mito", "Luna", "carretera", "color", "Estación", "cuatrocientos", "catorce", "teleobjetivo", "ciudades"])
