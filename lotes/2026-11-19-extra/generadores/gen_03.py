"""03 · Esta máquina engañó a Napoleón (el Turco) — método denso. Vídeo extra 2026-11-19 (Nico, chat), tendencia: inteligencia artificial.
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]
La voz dura 62,8 s: se quitan «Y era el año mil setecientos setenta.» (9–15; el año sale en un rótulo) y «Tenía razón.» (131–132) para no pasar de 60 s."""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_extra2  # noqa: E402

SVG = ilus_extra2.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG, omitir=[(9, 16), (131, 133)] if len(VOZ) == 2 else ())

SALON = ["#2a1420", "#1a0c14"]
OSC = ["#0a0604", "#2a160a"]
NOCHE = ["#040818", "#101c3a"]
MADERA = ["#3a2212", "#120a04"]
ROJO = ["#3a0c08", "#7a2a14"]
MORADO = ["#1a0a24", "#3a1a48"]
TX, TY, TA = 540, 1120, 1000          # el Turco en su sitio habitual
CABEZA = (540, 800)
MUEBLE = (540, 1400)
DENTRO = (700, 1420)


def turco(n="turco", keys=None, ancho=TA, x=TX, y=TY, z=0.5, **k):
    return IMG(n, ancho=ancho, x=x, y=y, z=z, keys=keys or [], **k)


def velas(sem=3):
    return [brillo(250, 640, 260, "#ffb060", 0.5, 0.07, pulso=[0.2, 0.35 + sem * 0.03]), brillo(830, 640, 260, "#ffb060", 0.5, 0.07, pulso=[0.2, 0.45 + sem * 0.02]),
            polvo("#ffd27a", 26, (0, 400, 1080, 1700), sem)]


def gira(n, ancho, x, y, vel, z=0.5, **k):
    return IMG(n, ancho=ancho, x=x, y=y, z=z, anim={"girar": vel}, **k)


# ================================================================== PLANOS
@v.plano(0, "gancho: el Turco sube hacia cámara en el salón, a la luz de las velas")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(1), turco(keys=arranque(TX, TY, d, "abajo", 280, 40))],
             cam(1.0, 1.05, (540, 1050), (540, 980)), vineta=0.65, sfx=[(0.02, "whoosh", -12, {"dur": 0.6}), (0.45, "impacto", -15)])


@v.plano(3, "a Napoleón: la silueta con bicornio y el rey negro que cae")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(2), IMG("sil_napoleon", ancho=620, z=0.5, keys=arranque(400, 1250, d, "izquierda", 260, 30)),
             IMG("pieza_rey", ancho=260, z=0.6, keys=[{"t": 0.15, "x": 820, "y": 1300, "rot": 0}, {"t": 0.6, "x": 860, "y": 1420, "rot": 90, "ease": "rebote"}, {"t": d, "x": 870, "y": 1420, "rot": 90}])],
             cam(1.0, 1.06, (540, 1200)), "corte", hud=[contexto(0.05, d - 0.05, "NAPOLEÓN")], sfx=[(0.55, "golpe", -14)])


@v.plano(5, "jugaba sola al ajedrez: sobre el tablero, una pieza se mueve sin que nadie la toque")
def _(d):
    return P(MADERA, [BG("bg_escritorio"), IMG("tablero", ancho=980, x=540, y=1150, z=0.4, keys=[{"t": 0, "rot": -4, "escala": 0.96}, {"t": d, "rot": 0, "escala": 1.02, "ease": "suave"}]),
             IMG("pieza_caballo", ancho=150, z=0.6, keys=[{"t": 0.2, "x": 380, "y": 1420}, {"t": d * 0.7, "x": 600, "y": 1100, "ease": "suave"}, {"t": d, "x": 600, "y": 1100}]),
             flecha([[380, 1500], [380, 1260], [600, 1180]], 0.2, d * 0.7, CIAN, 10, z=0.55), polvo("#ffd27a", 30, (100, 600, 980, 1700), 5)],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[contexto(0.05, d - 0.05, "AÑO 1770")], sfx=[(0.25, "roce", -18), (d * 0.7, "golpe", -20)])


@v.plano(16, "¿cómo lo hacía? engranajes girando")
def _(d):
    return P(OSC, [brillo(540, 1050, 700, "#ffb060", 0.35, 0.08), gira("engranaje", 640, 420, 1000, 60), gira("engranaje_cobre", 420, 800, 1300, -90), gira("engranaje", 300, 800, 740, 110),
             polvo("#ffd27a", 30, (100, 500, 980, 1600), 7, "chispas")],
             cam(1.0, 1.08, (560, 1050)), "corte", hud=[amarillo(0.05, d - 0.03, "¿CÓMO?", y=580, tam=130, color=CIAN)], sfx=[(0.05, "tictac", -18, {"dur": 1.0, "ritmo": 0.12})])


@v.plano(19, "la llamaban el Turco: el autómata entero con su nombre")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(3), turco(keys=[{"t": 0, "escala": 0.9}, {"t": 0.35, "escala": 1.0, "ease": "rebote"}, {"t": d, "escala": 1.03}])],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[rotulo(0.1, d - 0.05, "EL TURCO", tam=110, color="#141414", capsula="#ffd23fe6", y=520)], sfx=[(0.1, "ding", -18)])


@v.plano(23, "un muñeco con turbante: la cabeza de cerca, el anillo marca el turbante")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(4), turco(keys=[{"t": 0, "rot": -1.5}, {"t": d, "rot": 1.5, "ease": "suave"}]), senala(540, 640, 0.2, d - 0.1, 150, AMBAR)],
             cam(1.7, 1.85, CABEZA, (540, 760)), "corte", sfx=[(0.2, "pop", -20)])


@v.plano(27, "sentado ante un mueble lleno de engranajes: las puertas abiertas y las ruedas girando")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(5), turco("turco_abierto"),
             gira("engranaje", 150, 250, 1330, 80, 0.6), gira("engranaje_cobre", 120, 540, 1400, -120, 0.6), gira("engranaje", 140, 840, 1340, 70, 0.6)],
             cam(1.0, 1.5, (540, 1100), MUEBLE), "corte",
             sfx=[(0.1, "tictac", -20, {"dur": 1.6, "ritmo": 0.14})])


@v.plano(34, "su inventor abría las puertas: el mueble cerrado se abre, el público mira")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(6), turco(keys=[{"t": 0, "op": 1}, {"t": d * 0.45, "op": 1}, {"t": d * 0.6, "op": 0}]),
             turco("turco_abierto", keys=[{"t": 0, "op": 0}, {"t": d * 0.45, "op": 0}, {"t": d * 0.6, "op": 1}], z=0.51),
             IMG("publico", ancho=1300, x=540, y=1800, z=0.8, keys=[{"t": 0, "y": 1840}, {"t": d, "y": 1790, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[contexto(0.05, d - 0.05, "KEMPELEN, SU INVENTOR")], sfx=[(d * 0.45, "golpe", -18), (d * 0.5, "roce", -18)])


@v.plano(39, "para enseñar que dentro no había nadie: una vela recorre el interior, solo hay ruedas")
def _(d):
    luz = brillo(0, 1380, 240, "#ffe08a", 0.9, 0.62, keys=[{"t": 0, "x": 250, "ease": "suave"}, {"t": d * 0.8, "x": 850}, {"t": d, "x": 860}])
    return P(SALON, [BG("bg_salon_velas"), turco("turco_abierto"), luz, IMG("publico", ancho=1300, x=540, y=1800, z=0.8),
             gira("engranaje", 150, 250, 1330, 60, 0.6), gira("engranaje", 140, 840, 1340, 60, 0.6)],
             cam(1.45, 1.5, (400, 1380), (680, 1380)), "corte", hud=[rotulo(d * 0.45, d - 0.05, "¿NADIE?", tam=110, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.1, "roce", -22), (d * 0.45, "pop", -18)])


@v.plano(46, "luego: la llave de cuerda aparece")
def _(d):
    return P(OSC, [brillo(540, 1050, 600, "#ffd23f", 0.4, 0.08), gira("engranaje", 520, 220, 1450, 40, 0.3), gira("engranaje_cobre", 420, 900, 620, -60, 0.3), polvo("#ffd27a", 40, (100, 400, 980, 1600), 41, "chispas"),
             IMG("llave_cuerda", ancho=760, x=540, y=1050, z=0.5, keys=[{"t": 0, "escala": 0.5, "rot": -40}, {"t": 0.3, "escala": 1.0, "rot": 0, "ease": "rebote"}, {"t": d, "rot": 20}])],
             cam(1.0, 1.08), "corte", sfx=[(0.05, "pop", -18)])


@v.plano(47, "micro: le daba cuerda, la llave gira", mas=0.03)
def _(d):
    return P(OSC, [brillo(540, 1050, 600, "#ffd23f", 0.4, 0.08), IMG("llave_cuerda", ancho=700, x=540, y=1050, z=0.5, keys=[{"t": 0, "rot": 20, "ease": "lineal"}, {"t": d, "rot": 380}]),
             gira("engranaje_cobre", 300, 880, 1500, -200, 0.4)],
             cam(1.05, 1.1), "corte", sfx=[(0.0, "tictac", -14, {"dur": 0.5, "ritmo": 0.07})])


@v.plano(49, "cuerda: el Turco gira la cabeza")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(7), turco(keys=[{"t": 0, "rot": 0}, {"t": d * 0.4, "rot": -3, "ease": "golpe"}, {"t": d * 0.8, "rot": 3, "ease": "golpe"}, {"t": d, "rot": 0}])],
             cam(1.6, 1.7, CABEZA), "corte", sfx=[(d * 0.4, "tic", -16), (d * 0.8, "tic", -16)])


@v.plano(50, "y el muñeco: el brazo se levanta sobre el tablero")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(8), turco(),
             IMG("brazo_turco", ancho=520, z=0.6, keys=[{"t": 0, "x": 760, "y": 1010, "rot": 30}, {"t": d, "x": 740, "y": 960, "rot": 8, "ease": "suave"}])],
             cam(1.3, 1.4, (560, 1050)), "corte", sfx=[(0.05, "tictac", -18, {"dur": 0.7, "ritmo": 0.1})])


@v.plano(53, "micro: movía, la mano coge la pieza", mas=0.03)
def _(d):
    return P(MADERA, [BG("bg_escritorio"), IMG("tablero", ancho=1500, x=540, y=1250, z=0.4), IMG("pieza_caballo", ancho=260, x=520, y=1180, z=0.55),
             IMG("brazo_turco", ancho=900, z=0.6, keys=[{"t": 0, "x": 240, "y": 760, "rot": 10}, {"t": d, "x": 300, "y": 880, "rot": 16, "ease": "salida"}])],
             cam(1.0, 1.08, (540, 1100)), "corte", sfx=[(0.05, "golpe", -20)])


@v.plano(54, "las piezas: la pieza cruza el tablero y se posa")
def _(d):
    return P(MADERA, [BG("bg_escritorio"), IMG("tablero", ancho=1100, x=540, y=1200, z=0.4),
             IMG("pieza_caballo", ancho=200, z=0.6, keys=[{"t": 0, "x": 330, "y": 1380, "escala": 1.1}, {"t": d * 0.6, "x": 700, "y": 1010, "escala": 1.2, "ease": "suave"}, {"t": d * 0.75, "escala": 1.0, "ease": "rebote"}, {"t": d, "x": 700, "y": 1010}]),
             flecha([[330, 1480], [520, 1300], [700, 1110]], 0.05, d * 0.6, CIAN, 10, z=0.5)],
             cam(1.0, 1.06, (540, 1150)), "corte", sfx=[(d * 0.7, "golpe", -18)])


@v.plano(56, "y casi siempre ganaba: el rey contrario se tumba")
def _(d):
    return P(MADERA, [BG("bg_escritorio"), IMG("tablero", ancho=1500, x=540, y=1300, z=0.3, op=0.8), brillo(540, 1100, 500, "#ffd23f", 0.4, 0.35, pulso=[0.2, 0.5]),
             IMG("pieza_caballo", ancho=360, x=330, y=1150, z=0.55, keys=late(0.2, 1, 0.08, 0.4)),
             IMG("pieza_rey", ancho=330, z=0.6, keys=[{"t": 0, "x": 740, "y": 1100, "rot": 0}, {"t": d * 0.3, "rot": 0}, {"t": d * 0.6, "x": 800, "y": 1320, "rot": 90, "ease": "rebote"}, {"t": d, "x": 810, "y": 1320, "rot": 90}])],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[rotulo(d * 0.38, d - 0.05, "JAQUE MATE", tam=100, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(d * 0.55, "golpe", -13)])


@v.plano(60, "¿contra quién? el público de espaldas")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(9), turco(ancho=620, y=1000, op=0.9), IMG("publico", ancho=1500, x=540, z=0.8, keys=[{"t": 0, "y": 1700}, {"t": d, "y": 1620, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1200)), "corte", hud=[amarillo(0.05, d - 0.03, "¿CONTRA QUIÉN?", y=580, tam=96, color=CIAN)], sfx=[(0.1, "rumor", -22, {"dur": 1.0})])


@v.plano(62, "recorrió Europa y América: la Tierra gira y el Turco viaja con su flecha")
def _(d):
    return P(NOCHE, [BG("bg_esp_violeta"), tierra(540, 1150, 900, 0.4, 8), flecha([[820, 880], [540, 760], [260, 900]], 0.1, d * 0.75, AMBAR, 12, z=0.6),
             IMG("turco", ancho=260, z=0.65, keys=lanza(0.1, d * 0.8, (840, 900), (250, 920)))],
             cam(1.0, 1.06, (540, 1050)), "desenfoque", hud=[amarillo(0.1, d - 0.03, "DE GIRA", y=580, tam=110, color=AMBAR)], sfx=[(0.1, "whoosh", -18, {"dur": 0.8})])


@v.plano(66, "durante ochenta: el contador de años sube")
def _(d):
    return P(NOCHE, [BG("bg_esp_petroleo"), tierra(540, 1750, 1300, 0.3, 6), turco(ancho=520, y=1180)],
             cam(1.0, 1.05), "corte", hud=[contador(0.05, d + 1.2, 0, 84, d + 0.3, " AÑOS", y=560, tam=130, color="#ffd23f")], sfx=[(0.05, "tictac", -20, {"dur": 0.8, "ritmo": 0.1})])


@v.plano(68, "micro: y cuatro años, las dos hojas del calendario", mas=0.03)
def _(d):
    return P(NOCHE, [BG("bg_esp_petroleo"), IMG("hoja_1770", ancho=440, x=300, y=1050, z=0.5, keys=[{"t": 0, "rot": -8, "escala": 0.9}, {"t": d, "rot": -5, "escala": 1.0}]),
             IMG("hoja_1854", ancho=440, x=780, y=1150, z=0.55, keys=[{"t": 0, "rot": 8, "escala": 0.9}, {"t": d, "rot": 5, "escala": 1.0}]), flecha([[470, 1090], [610, 1120]], 0.0, d * 0.7, AMBAR, 12, z=0.6)],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "pop", -16)])


@v.plano(70, "años: el Turco en penumbra, las velas siguen")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(10), turco(keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.05}])],
             cam(1.1, 1.2, (540, 1000)), "corte", hud=[rotulo(0.0, d - 0.03, "84 AÑOS", tam=120, color="#141414", capsula="#ffd23fe6", y=580, sin_pop=True)], sfx=[(0.05, "ding", -20)])


@v.plano(71, "venció a Benjamin Franklin: la silueta con gafas frente al tablero, su rey cae")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(11), IMG("sil_franklin", ancho=600, z=0.5, keys=[{"t": 0, "x": 330, "y": 1300, "escala": 0.94}, {"t": 0.3, "escala": 1.0, "ease": "rebote"}, {"t": d, "x": 340, "y": 1290}]),
             turco(ancho=520, x=820, y=1180, z=0.4),
             IMG("pieza_rey", ancho=200, z=0.6, keys=[{"t": 0, "x": 600, "y": 1520, "rot": 0}, {"t": d * 0.5, "rot": 0}, {"t": d * 0.75, "x": 560, "y": 1620, "rot": -90, "ease": "rebote"}, {"t": d, "x": 555, "y": 1620, "rot": -90}])],
             cam(1.0, 1.05, (540, 1250)), "corte", hud=[contexto(0.05, d - 0.05, "BENJAMIN FRANKLIN")], sfx=[(d * 0.72, "golpe", -15)])


@v.plano(75, "y a Napoleón: el bicornio entra por la derecha")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(12), turco(ancho=520, x=280, y=1180, z=0.4), IMG("sil_napoleon", ancho=640, z=0.5, keys=arranque(760, 1300, d, "derecha", 260, 30))],
             cam(1.0, 1.05, (560, 1250)), "corte", hud=[contexto(0.05, d - 0.05, "NAPOLEÓN")], sfx=[(0.02, "whoosh", -18, {"dur": 0.5})])


@v.plano(78, "que según cuentan intentó hacerle trampas: una pieza se mueve mal y el brazo la devuelve")
def _(d):
    return P(MADERA, [BG("bg_escritorio"), IMG("tablero", ancho=1100, x=540, y=1200, z=0.4),
             IMG("pieza_rey", ancho=180, z=0.6, keys=[{"t": 0.1, "x": 300, "y": 1420}, {"t": d * 0.3, "x": 760, "y": 980, "ease": "suave"}, {"t": d * 0.55, "x": 760, "y": 980}, {"t": d * 0.8, "x": 300, "y": 1420, "ease": "golpe"}, {"t": d, "x": 300, "y": 1420}]),
             flecha([[300, 1500], [500, 1380], [420, 1180], [760, 1080]], 0.1, d * 0.3, "#ff3d3d", 10, z=0.5),
             IMG("brazo_turco", ancho=620, z=0.65, keys=[{"t": d * 0.4, "x": 400, "y": 500, "rot": 20, "op": 0}, {"t": d * 0.5, "op": 1}, {"t": d * 0.58, "x": 560, "y": 800, "rot": 30, "ease": "golpe"}, {"t": d * 0.8, "x": 180, "y": 1200, "rot": 60, "ease": "golpe"}, {"t": d, "x": 120, "y": 1100, "rot": 50}])],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[rotulo(d * 0.3, d * 0.75, "¡TRAMPA!", tam=110, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.15, "roce", -18), (d * 0.3, "zap", -18), (d * 0.6, "golpe", -14)])


@v.plano(84, "¿el secreto? el anillo marca el mueble")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(13), turco(), senala(540, 1390, 0.1, d - 0.1, 300, MAGENTA)],
             cam(1.0, 1.3, (540, 1100), MUEBLE), "corte", hud=[rotulo(0.05, d - 0.05, "¿EL SECRETO?", tam=96, color="#ffffff", capsula="#c0392be6", y=580)], sfx=[(0.05, "subida", -16, {"dur": 1.0})])


@v.plano(86, "dentro sí había alguien: el mueble se vuelve transparente y aparece la persona")
def _(d):
    return P(OSC, [BG("bg_salon_velas"), turco(keys=[{"t": 0, "op": 1}, {"t": d * 0.3, "op": 0}]), turco("turco_rayos", keys=[{"t": 0, "op": 0}, {"t": d * 0.3, "op": 1}], z=0.51),
             brillo(DENTRO[0], DENTRO[1], 320, "#7df9ff", 0.6, 0.6, pulso=[0.3, 0.3], keys=[{"t": 0, "op": 0}, {"t": d * 0.3, "op": 1}]),
             fundido_blanco([{"t": d * 0.25, "op": 0}, {"t": d * 0.3, "op": 0.5}, {"t": d * 0.45, "op": 0}], "#dffaff")],
             cam(1.3, 1.45, MUEBLE, (620, 1400)), "corte", hud=[rotulo(d * 0.35, d - 0.05, "HABÍA ALGUIEN", tam=96, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(d * 0.28, "impacto", -12)])


@v.plano(90, "un maestro de ajedrez escondido: la persona dentro, muy de cerca")
def _(d):
    return P(OSC, [BG("bg_salon_velas"), turco("turco_rayos"), senala(DENTRO[0] + 40, DENTRO[1], 0.15, d - 0.1, 170, CIAN),
             IMG("pieza_caballo", ancho=90, z=0.7, keys=[{"t": 0.3, "x": 880, "y": 1360, "op": 0, "escala": 0.4}, {"t": 0.5, "op": 1, "escala": 1.0, "ease": "rebote"}, {"t": d, "y": 1350}])],
             cam(1.9, 2.1, (680, 1400), (720, 1400)), "corte", hud=[contexto(0.05, d - 0.05, "UN MAESTRO DE AJEDREZ")], sfx=[(0.3, "pop", -20)])


@v.plano(95, "en un asiento que se deslizaba: flechas a un lado y a otro, el asiento se mueve")
def _(d):
    return P(OSC, [BG("bg_salon_velas"), turco("turco_rayos", keys=[{"t": 0, "x": TX - 30, "ease": "suave"}, {"t": d * 0.5, "x": TX + 40}, {"t": d, "x": TX - 20}]),
             flecha([[520, 1560], [330, 1560]], 0.05, d * 0.4, AMBAR, 10, z=0.7), flecha([[720, 1560], [910, 1560]], d * 0.45, d * 0.85, AMBAR, 10, z=0.7)],
             cam(1.6, 1.6, (620, 1420)), "corte", hud=[amarillo(0.1, d - 0.03, "SE DESLIZABA", y=860, tam=84, color=AMBAR)], sfx=[(0.05, "roce", -16), (d * 0.45, "roce", -16)])


@v.plano(101, "para esquivar las miradas: el público mira las puertas abiertas y solo ve ruedas")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(14), turco("turco_abierto"), IMG("publico", ancho=1400, x=540, y=1780, z=0.8),
             IMG("lupa", ancho=320, z=0.7, keys=[{"t": 0, "x": 280, "y": 1300}, {"t": d, "x": 820, "y": 1380, "ease": "suave"}]),
             gira("engranaje", 150, 250, 1330, 60, 0.6), gira("engranaje", 140, 840, 1340, 60, 0.6)],
             cam(1.2, 1.3, (540, 1300)), "corte", sfx=[(0.1, "rumor", -22, {"dur": 1.2})])


@v.plano(105, "seguía la partida: el tablero desde arriba, una pieza avanza")
def _(d):
    return P(MADERA, [BG("bg_escritorio"), IMG("tablero", ancho=1000, x=540, y=1100, z=0.4), IMG("pieza_caballo", ancho=150, z=0.6, keys=[{"t": 0, "x": 320, "y": 1330, "ease": "suave"}, {"t": d, "x": 540, "y": 1000}])],
             cam(1.0, 1.05, (540, 1100)), "corte", sfx=[(0.1, "roce", -20)])


@v.plano(109, "micro: imanes, el imán de cerca", mas=0.03)
def _(d):
    return P(["#0a0c1a", "#1a2040"], [brillo(540, 1000, 500, "#7df9ff", 0.4, 0.1), IMG("iman", ancho=620, x=540, y=1050, z=0.5, keys=[{"t": 0, "escala": 0.7, "rot": -10}, {"t": 0.2, "escala": 1.05, "rot": 0, "ease": "rebote"}, {"t": d, "escala": 1.0}])],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "zap", -18)])


@v.plano(110, "bajo el tablero: el imán sigue a la pieza desde abajo")
def _(d):
    mov = [{"t": 0, "x": 380, "ease": "suave"}, {"t": d, "x": 700}]
    return P(OSC, [brillo(540, 1000, 700, "#7df9ff", 0.2, 0.05),
             {"tipo": "forma", "forma": "redondeado", "ancho": 980, "alto": 60, "relleno": "#6a4226", "x": 540, "y": 1000, "z": 0.45},
             IMG("pieza_caballo", ancho=240, y=800, z=0.5, keys=mov), IMG("iman", ancho=240, y=1230, z=0.5, keys=[{**k, "rot": 180} for k in mov]),
             flecha([[540, 1120], [540, 1040]], 0.1, d * 0.5, CIAN, 8, disc=[12, 10], z=0.6)],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[amarillo(0.05, d - 0.03, "IMANES", y=580, tam=124, color=CIAN)], sfx=[(0.1, "zap", -22)])


@v.plano(113, "y movía el: la palanca dentro del mueble sube")
def _(d):
    return P(OSC, [BG("bg_salon_velas"), turco("turco_rayos"), flecha([[470, 1440], [440, 1330], [440, 1180]], 0.05, d * 0.8, AMBAR, 10, z=0.7)],
             cam(1.7, 1.6, (560, 1380), (540, 1250)), "corte", sfx=[(0.05, "tic", -16)])


@v.plano(116, "micro: brazo, el brazo del muñeco a toda pantalla", mas=0.03)
def _(d):
    return P(SALON, [BG("bg_salon_velas"), IMG("brazo_turco", ancho=1100, z=0.5, keys=[{"t": 0, "x": 500, "y": 1000, "rot": -8}, {"t": d, "x": 560, "y": 1080, "rot": 6, "ease": "salida"}])],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "roce", -16)])


@v.plano(117, "del muñeco con palancas: el brazo baja sobre el tablero mientras gira la rueda")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(15), turco(), gira("engranaje_cobre", 200, 250, 1620, 140, 0.6),
             IMG("brazo_turco", ancho=520, z=0.6, keys=[{"t": 0, "x": 740, "y": 940, "rot": 0}, {"t": d * 0.5, "x": 700, "y": 1010, "rot": 22, "ease": "suave"}, {"t": d, "x": 740, "y": 950, "rot": 4, "ease": "suave"}])],
             cam(1.25, 1.35, (580, 1080)), "corte", hud=[amarillo(0.1, d - 0.03, "PALANCAS", y=1240, tam=110, color=AMBAR)], sfx=[(0.05, "tictac", -18, {"dur": 1.0, "ritmo": 0.12})])


@v.plano(121, "el escritor Edgar Allan: la silueta inclinada sobre el pergamino, la pluma escribe")
def _(d):
    return P(MORADO, [BG("bg_escritorio"), IMG("pergamino", ancho=620, x=700, y=1450, z=0.4, keys=[{"t": 0, "rot": 6}, {"t": d, "rot": 4}]),
             IMG("sil_escritor", ancho=640, x=360, y=1250, z=0.5, keys=[{"t": 0, "rot": -2}, {"t": d, "rot": 2, "ease": "suave"}]),
             IMG("pluma", ancho=150, z=0.6, keys=[{"t": 0, "x": 620, "y": 1260, "rot": 25, "ease": "lineal"}, {"t": d, "x": 800, "y": 1300, "rot": 32}]), polvo("#c8a0ff", 24, (100, 500, 980, 1600), 17)],
             cam(1.0, 1.05, (540, 1250)), "desenfoque", hud=[contexto(0.05, d - 0.05, "EDGAR ALLAN POE")], sfx=[(0.1, "trazo", -18), (0.5, "trazo", -18), (0.9, "trazo", -18)])


@v.plano(125, "micro: Poe, la pluma de cerca", mas=0.03)
def _(d):
    return P(MORADO, [BG("bg_escritorio"), IMG("pergamino", ancho=1300, x=540, y=1200, z=0.4), IMG("pluma", ancho=420, z=0.6, keys=[{"t": 0, "x": 420, "y": 900, "rot": 25}, {"t": d, "x": 660, "y": 960, "rot": 34, "ease": "salida"}])],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "trazo", -16)])


@v.plano(126, "sospechó que era un truco: la lupa pasa por el mueble")
def _(d):
    return P(SALON, [BG("bg_salon_velas"), *velas(16), turco(), IMG("lupa", ancho=460, z=0.7, keys=[{"t": 0, "x": 300, "y": 1250}, {"t": d, "x": 760, "y": 1420, "ease": "suave"}])],
             cam(1.2, 1.35, (540, 1300)), "corte", hud=[rotulo(0.15, d - 0.05, "¿UN TRUCO?", tam=100, color="#ffffff", capsula="#6a3ad8e6", y=720)], sfx=[(0.1, "roce", -20)])


@v.plano(133, "la máquina: el Turco, y el fuego empieza a subir por abajo")
def _(d):
    return P(ROJO, [BG("bg_salon_velas"), turco(), IMG("llamas", ancho=1500, x=540, z=0.7, keys=[{"t": 0, "y": 2300}, {"t": d, "y": 1900, "ease": "suave"}]),
             brillo(540, 1700, 700, "#ff7a1e", 0.6, 0.08, pulso=[0.3, 0.25])],
             cam(1.0, 1.05, (540, 1100)), "corte", sfx=[(0.05, "rumor", -16, {"dur": 0.8})])


@v.plano(135, "micro: ardió, llamas a pantalla completa", mas=0.03)
def _(d):
    return P(ROJO, [IMG("llamas", ancho=2000, x=540, z=0.5, keys=[{"t": 0, "y": 1150}, {"t": d, "y": 900, "ease": "salida"}]), polvo("#ffd27a", 60, (0, 300, 1080, 1700), 19, "chispas")],
             cam(1.0, 1.1, temblor=3), "corte", sfx=[(0.0, "meteoro", -14, {"dur": 0.5})])


@v.plano(136, "en un incendio: el Turco entre las llamas")
def _(d):
    return P(ROJO, [BG("bg_salon_velas"), brillo(540, 1200, 900, "#ff5a1e", 0.6, 0.08, pulso=[0.3, 0.2]), turco(keys=[{"t": 0, "op": 1}, {"t": d, "op": 0.75}]),
             IMG("llamas", ancho=1500, x=540, z=0.7, keys=[{"t": 0, "y": 1750}, {"t": d, "y": 1550, "ease": "suave"}], anim={"flotar": [18, 0.5]}),
             IMG("llamas", ancho=1300, x=400, z=0.3, ex=-1, keys=[{"t": 0, "y": 1500, "ex": -1}, {"t": d, "y": 1350, "ex": -1}]), polvo("#ffd27a", 60, (0, 300, 1080, 1700), 21, "chispas")],
             cam(1.0, 1.06, (540, 1100), temblor=1), "corte", sfx=[(0.05, "rumor", -14, {"dur": 1.0})])


@v.plano(139, "en mil ochocientos cincuenta y cuatro: la hoja del calendario cae sobre las brasas")
def _(d):
    return P(ROJO, [brillo(540, 1500, 900, "#ff5a1e", 0.5, 0.08, pulso=[0.2, 0.3]), IMG("llamas", ancho=1500, x=540, y=1800, z=0.3, anim={"flotar": [14, 0.6]}),
             IMG("hoja_1854", ancho=640, x=540, z=0.5, keys=cae(0.0, 0.45, 400, 1000)), polvo("#ffd27a", 50, (0, 300, 1080, 1700), 23, "chispas")],
             cam(1.0, 1.05), "corte", sfx=[(0.3, "golpe", -16)])


@v.plano(145, "la primera inteligencia artificial famosa: el chip de IA se enciende")
def _(d):
    return P(["#040818", "#0a1a3a"], [brillo(540, 1050, 700, "#3fb8ff", 0.45, 0.08, pulso=[0.2, 0.5]), IMG("chip_ia", ancho=760, x=540, y=1080, z=0.5, keys=[{"t": 0, "escala": 0.6, "op": 0.3}, {"t": 0.35, "escala": 1.05, "op": 1, "ease": "rebote"}, {"t": d, "escala": 1.0}]),
             polvo("#7df9ff", 50, (100, 500, 980, 1600), 25, "chispas")],
             cam(1.0, 1.06), "desenfoque", hud=[amarillo(0.15, d - 0.03, "¿LA PRIMERA IA?", y=580, tam=92, color=CIAN)], sfx=[(0.05, "subida", -18, {"dur": 0.8}), (0.35, "brillo", -18)])


@v.plano(150, "era una persona escondida: el Turco vuelve a subir, con el mueble transparente (bucle)")
def _(d):
    ks = [{"t": 0, "x": TX, "y": TY + 240, "escala": 0.94}, {"t": 0.45, "y": TY, "escala": 1.0, "ease": "rebote"}, {"t": d, "y": TY - 30, "escala": 1.03}]
    return P(SALON, [BG("bg_salon_velas"), *velas(1), turco("turco_rayos", keys=[{**k, "op": 1 if k["t"] < d else 0.0} for k in ks][:2] + [{"t": d * 0.75, "op": 1}, {"t": d, "y": TY - 30, "escala": 1.03, "op": 0}], z=0.51),
             turco(keys=ks, z=0.5)],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[rotulo(0.15, d - 0.45, "UNA PERSONA", tam=104, color="#141414", capsula="#ffd23fe6", y=580)], sfx=[(0.1, "impacto", -15), (d * 0.6, "ding", -22)])


v.construir("2026-11-19-extra-03-el-turco", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 29, "db": -13},
            claves=["máquina", "Napoleón", "ajedrez", "Turco", "muñeco", "turbante", "engranajes", "inventor", "nadie", "cuerda", "piezas", "ganaba", "Europa", "América",
                    "ochenta", "cuatro", "Franklin", "trampas", "secreto", "alguien", "maestro", "escondido", "asiento", "imanes", "palancas", "Poe", "truco", "incendio",
                    "inteligencia", "artificial", "persona", "escondida"])
