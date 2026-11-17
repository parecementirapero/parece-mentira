"""03 · Corta una cebolla (por qué lloras y el truco que funciona) — método denso. Lote 2026-11-17-tarde, Agente 20:00 (Jorge).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_tarde  # noqa: E402

SVG = ilus_tarde.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

COCINA = ["#2a1c14", "#3a2414"]
MICRO = ["#0c1a10", "#06100a"]
PIEL = ["#e8b090", "#b8724e"]


def cortes(d, n=3, y0=560, y1=930, x=600, t0=0.0, t1=None, romo=False):
    """Cuchillo que sube y baja n veces sobre la cebolla (claves en s del plano)."""
    t1 = t1 or d
    ks, paso = [], (t1 - t0) / n
    for k in range(n):
        a = t0 + k * paso
        ks += [{"t": a, "y": y0, "ease": "suave"}, {"t": a + paso * 0.45, "y": y1, "ease": "entrada"}, {"t": a + paso, "y": y0, "ease": "salida"}]
    return IMG("cuchillo_romo" if romo else "cuchillo", ancho=900, x=x, z=0.7, rot=-4, keys=ks)


def chorro(t, x=540, y=900, ancho=700, nombre="gotitas_b", dur=0.7, z=0.65):
    return IMG(nombre, ancho=ancho, x=x, y=y, z=z, keys=[{"t": 0, "op": 0}, {"t": t, "op": 0, "escala": 0.3}, {"t": t + 0.05, "op": 1},
                                                     {"t": t + dur, "op": 0, "escala": 1.3, "ease": "salida"}])


# ================================================================== PLANOS
@v.plano(0, "gancho: el cuchillo cae sobre una cebolla enorme y salta el chorro")
def _(d):
    return P(COCINA, [BG("bg_cocina"), IMG("tabla", ancho=1080, x=540, y=1480, z=0.3),
             IMG("cebolla", ancho=820, x=540, y=1150, z=0.5, keys=arranque(540, 1150, d, "abajo", 160, 20)),
             IMG("cuchillo", ancho=1000, x=600, z=0.7, rot=-4, keys=[{"t": 0, "y": 520}, {"t": 0.35, "y": 880, "ease": "entrada"}, {"t": d, "y": 860}]),
             chorro(0.36, 520, 640, 800, dur=0.9), IMG("gas", ancho=700, x=540, y=600, z=0.6, keys=[{"t": 0.3, "op": 0, "escala": 0.5}, {"t": d, "op": 0.8, "escala": 1.3}])],
             cam(1.1, 1.0, (540, 1000), (540, 980)), vineta=0.65, sfx=[(0.33, "golpe", -12), (0.38, "agua", -18, {"dur": 0.8})])


@v.plano(3, "lloras por un gas invisible")
def _(d):
    return P(PIEL, [IMG("ojo_lloroso", ancho=1150, x=540, y=1000, z=0.5, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.08, "ease": "suave"}]),
             IMG("gas", ancho=900, x=540, y=1400, z=0.6, keys=[{"t": 0, "y": 1600, "op": 0.2}, {"t": d, "y": 1100, "op": 0.7}])],
             cam(1.0, 1.06), "desenfoque", hud=[rotulo(0.1, d - 0.05, "GAS INVISIBLE", tam=88, color="#141414", capsula="#b6ff5ae6", y=560)], sfx=[(0.1, "roce", -20)])


@v.plano(8, "al cortarla rompes sus células")
def _(d):
    return P(MICRO, [BG("celulas"), IMG("cuchillo", ancho=1400, x=540, z=0.7, rot=-90, keys=[{"t": 0, "y": -400}, {"t": d * 0.6, "y": 900, "ease": "entrada"}]),
             IMG("chispa", ancho=400, x=540, y=1100, z=0.6, keys=[{"t": d * 0.55, "op": 0}, {"t": d * 0.6, "op": 1}, {"t": d, "op": 0}])],
             cam(1.0, 1.12, (540, 1000), (540, 1050)), "zoom", hud=[contexto(0.05, d - 0.05, "CÉLULAS")], sfx=[(d * 0.6, "roce", -14)])


@v.plano(13, "dos cosas separadas se mezclan")
def _(d):
    return P(MICRO, [BG("celulas"), brillo(540, 1000, 500, "#000000", 0.0),
             {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#06100a", "x": 540, "y": 960, "z": 0.2, "op": 0.55},
             IMG("molecula_s", ancho=360, x=260, y=1000, z=0.6, keys=[{"t": 0, "x": 200}, {"t": d, "x": 430, "ease": "suave"}], anim={"balanceo": [6, 0.8]}),
             IMG("enzima", ancho=340, x=820, y=1000, z=0.6, keys=[{"t": 0, "x": 880}, {"t": d, "x": 650, "ease": "suave"}], anim={"balanceo": [8, 0.6]}),
             flecha([[300, 1250], [480, 1250]], 0.1, d * 0.6, CIAN, 7), flecha([[780, 1250], [600, 1250]], 0.1, d * 0.6, MAGENTA, 7)],
             cam(1.0, 1.06), "desenfoque", hud=[amarillo(0.1, d - 0.05, "SE MEZCLAN", y=560, color=AMBAR)])


@v.plano(21, "moléculas con azufre")
def _(d):
    return P(MICRO, [BG("celulas"), {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#06100a", "x": 540, "y": 960, "z": 0.2, "op": 0.6},
             brillo(540, 1000, 400, "#ffd23f", 0.5), IMG("molecula_s", ancho=640, x=540, y=1000, z=0.6, keys=aparece(0.0, 0.4), anim={"girar": 12})],
             cam(1.3, 1.45, (540, 1000), (520, 1000)), hud=[rotulo(0.1, d - 0.05, "AZUFRE", tam=110, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "pop", -18)])


@v.plano(25, "y una enzima")
def _(d):
    return P(MICRO, [BG("celulas"), {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#06100a", "x": 540, "y": 960, "z": 0.2, "op": 0.6},
             brillo(540, 1000, 400, "#ff3df2", 0.45), IMG("enzima", ancho=560, x=540, y=1000, z=0.6, keys=aparece(0.0, 0.4) + late(0.5, 2, 0.08, 0.3))],
             cam(1.0, 1.08), "corte", hud=[rotulo(0.1, d - 0.05, "ENZIMA", tam=110, color="#ffffff", capsula="#0d1330d8", borde=MAGENTA, y=560)], sfx=[(0.05, "mordisco", -18)])


@v.plano(28, "juntas fabrican ese gas")
def _(d):
    return P(MICRO, [BG("celulas"), {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#06100a", "x": 540, "y": 960, "z": 0.2, "op": 0.7},
             IMG("molecula_s", ancho=300, x=420, y=1150, z=0.6, keys=[{"t": 0, "op": 1}, {"t": d * 0.5, "op": 0, "escala": 0.6}]),
             IMG("enzima", ancho=300, x=640, y=1150, z=0.61, keys=[{"t": 0, "x": 700}, {"t": d * 0.5, "x": 470, "ease": "entrada"}]),
             IMG("gas", ancho=600, x=540, y=1000, z=0.5, keys=[{"t": d * 0.4, "op": 0, "escala": 0.4, "y": 1150}, {"t": d, "op": 1, "escala": 1.4, "y": 900, "ease": "salida"}]),
             polvo("#d8ff9a", 40, (200, 600, 880, 1300), 4, "chispas")],
             cam(1.0, 1.08), sfx=[(d * 0.45, "burbuja", -16), (d * 0.6, "burbuja", -18)])


@v.plano(32, "el factor lacrimógeno")
def _(d):
    return P(COCINA, [BG("bg_cocina"), IMG("tabla", ancho=1080, x=540, y=1500, z=0.3), IMG("cebolla_mitad", ancho=620, x=540, y=1330, z=0.45),
             IMG("gas", ancho=1100, x=540, y=900, z=0.6, keys=[{"t": 0, "y": 1150, "op": 0.5}, {"t": d, "y": 800, "op": 0.9, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1100), (540, 1050)), "desenfoque",
             hud=[rotulo(0.1, d - 0.05, "FACTOR LACRIMÓGENO", tam=78, color="#141414", capsula="#b6ff5ae6", y=560)], sfx=[(0.1, "brillo", -20)])


@v.plano(35, "micro: sube")
def _(d):
    return P(COCINA, [BG("bg_cocina"), IMG("gas", ancho=1300, x=540, y=900, z=0.6, keys=[{"t": 0, "y": 1300}, {"t": d, "y": 700, "ease": "salida"}]),
             flecha([[540, 1300], [540, 700]], 0.0, d * 0.8, LIMA, 9)], cam(1.0, 1.08), "corte", sfx=[(0.02, "whoosh", -20, {"dur": 0.4})])


@v.plano(36, "te llega a los ojos")
def _(d):
    return P(PIEL, [IMG("ojo", ancho=1150, x=540, y=820, z=0.5),
             IMG("gas", ancho=900, x=540, y=1200, z=0.6, keys=[{"t": 0, "y": 1600, "op": 0.4}, {"t": d, "y": 950, "op": 0.85, "ease": "suave"}]),
             flecha([[540, 1500], [540, 1100]], 0.05, d * 0.7, "#2a6a10", 9)],
             cam(1.0, 1.06, (540, 960), (540, 900)), "desenfoque", sfx=[(0.05, "roce", -22)])


@v.plano(41, "irrita los nervios de la córnea")
def _(d):
    return P(PIEL, [IMG("ojo", ancho=1600, x=540, y=960, z=0.5), {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#ff2d2d", "x": 540, "y": 960, "z": 0.55,
             "keys": [{"t": 0, "op": 0}, {"t": d, "op": 0.25}]},
             *[IMG("chispa", ancho=180, x=x, y=y, z=0.6, keys=[{"t": t, "op": 0, "escala": 0.3}, {"t": t + 0.08, "op": 1, "escala": 1}, {"t": t + 0.4, "op": 0}])
               for x, y, t in [(380, 880, 0.1), (700, 1000, 0.35), (520, 1080, 0.6), (640, 860, 0.85), (420, 1020, 1.1)]]],
             cam(1.1, 1.25, (540, 960), (540, 960), temblor=3), hud=[rotulo(0.1, d - 0.05, "CÓRNEA", tam=100, color="#ffffff", capsula="#c0392be6", y=560)],
             sfx=[(0.1, "zap", -22), (0.6, "zap", -22)])


@v.plano(49, "tus ojos lloran para lavarlo")
def _(d):
    return P(PIEL, [IMG("ojo_lloroso", ancho=1150, x=540, y=900, z=0.5),
             {"tipo": "forma", "forma": "elipse", "ancho": 50, "alto": 70, "relleno": "#bfe9ff", "x": 720, "z": 0.6,
              "keys": [{"t": 0, "y": 1080, "op": 1}, {"t": d, "y": 1650, "ease": "entrada"}]}],
             cam(1.0, 1.08), "desenfoque", hud=[rotulo(0.1, d - 0.05, "LO LAVAN", tam=100, color="#ffffff", capsula="#0d1330d8", borde=CIAN, y=560)], sfx=[(d * 0.3, "agua", -20, {"dur": 0.8})])


@v.plano(53, "¿y eso es todo?")
def _(d):
    return P(COCINA, [BG("bg_cocina"), IMG("tabla", ancho=1080, x=540, y=1480, z=0.3),
             IMG("cebolla", ancho=640, x=540, y=1180, z=0.5, keys=late(0.1, 2, 0.08, 0.35))],
             cam(1.0, 1.08, (540, 1100), (540, 1080)), "desenfoque", hud=[rotulo(0.05, d - 0.05, "¿TODO?", tam=140, color=AMBAR, capsula=None, y=560)], energia=0.3)


@v.plano(57, "micro: no")
def _(d):
    return P(["#2a0a10", "#120406"], [brillo(540, 960, 500, "#ff2d55", 0.5, pulso=[0.2, 0.15]), IMG("cebolla_roja", ancho=500, x=540, y=1150, z=0.5, rot=8, anim={"balanceo": [6, 0.2]}),
             polvo("#ffb0c0", 30, (200, 800, 880, 1500), 6)],
             cam(1.1, 1.15), "corte", hud=[rotulo(0.0, d, "NO", tam=220, color="#ffffff", capsula=None, y=600, fijo=True, sin_pop=True)], sfx=[(0.0, "golpe", -14)])


@v.plano(58, "en dos mil veinticinco")
def _(d):
    return P(["#141a2e", "#0a0e1a"], [IMG("calendario", ancho=560, x=540, y=1100, z=0.5, keys=aparece(0.0, 0.35))],
             cam(1.0, 1.06), hud=[contador(0.05, d - 0.05, 2000, 2025, d * 0.6, "", tam=150, y=560, borde=CIAN, miles=False)], sfx=[(0.05, "tic", -18)])


@v.plano(62, "en la Universidad de Cornell")
def _(d):
    return P(["#1a2a48", "#0a1428"], [brillo(540, 900, 600, "#ffd27a", 0.25), IMG("edificio", ancho=820, x=540, y=1150, z=0.5, keys=aparece(0.0, 0.4)),
             polvo("#ffffff", 30, (0, 200, 1080, 900), 5, "estrellas")],
             cam(1.0, 1.06, (540, 1050), (540, 1030)), "barrido", hud=[rotulo(0.05, d - 0.05, "CORNELL", tam=110, color="#ffffff", capsula="#b31b1be6", y=560)])


@v.plano(67, "grabaron con cámaras de alta velocidad")
def _(d):
    return P(COCINA, [BG("bg_cocina"), IMG("tabla", ancho=1080, x=540, y=1480, z=0.3), IMG("cebolla", ancho=500, x=360, y=1200, z=0.5),
             cortes(d, 1, 700, 1030, 420, 0.2, d), IMG("camara", ancho=520, x=800, y=800, z=0.6, keys=aparece(0.0, 0.4), rot=-12),
             brillo(800, 800, 200, "#ff3d3d", 0.5, 0.65, pulso=[0.4, 0.5])],
             cam(1.0, 1.06, (540, 1050), (540, 1030)), hud=[amarillo(0.1, d - 0.05, "ALTA VELOCIDAD", y=560, color=CIAN, tam=84)],
             sfx=[(0.1, "senal", -22), (d * 0.6, "roce", -16)])


@v.plano(75, "cada corte lanza un chorro de gotitas")
def _(d):
    return P(["#05080c", "#101820"], [brillo(540, 1100, 600, "#5ad8ff", 0.3), IMG("cebolla_mitad", ancho=900, x=540, y=1350, z=0.4),
             cortes(d, 2, 700, 1080, 600, 0.0, d), chorro(d * 0.22, 540, 900, 900, dur=d * 0.4), chorro(d * 0.72, 560, 900, 900, "gotitas", dur=d * 0.3)],
             cam(1.0, 1.08, (540, 1050), (540, 1000)), "zoom", hud=[contexto(0.05, d - 0.05, "CÁMARA LENTA")],
             sfx=[(d * 0.22, "agua", -16, {"dur": 0.5}), (d * 0.72, "agua", -18, {"dur": 0.4})])


@v.plano(82, "hasta cuarenta metros por segundo")
def _(d):
    return P(["#05080c", "#101820"], [IMG("gotitas_b", ancho=1400, x=540, y=1000, z=0.5, keys=[{"t": 0, "y": 1300, "escala": 0.8}, {"t": d, "y": 800, "escala": 1.2, "ease": "salida"}]),
             *lineas_vel(540, 900, 3, "#bfe9ffaa")],
             cam(1.0, 1.1), hud=[contador(0.05, d - 0.05, 0, 40, d * 0.6, "M/S", tam=130, y=560, borde=CIAN)], sfx=[(0.05, "subida", -16, {"dur": d * 0.6})], energia=0.8)


@v.plano(88, "más rápido que un guepardo")
def _(d):
    return P(["#e8b860", "#a87a30"], [brillo(540, 700, 800, "#fff3c0", 0.4),
             {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 700, "relleno": "#b8904a", "x": 540, "y": 1600, "z": 0.1},
             IMG("guepardo", ancho=1050, x=540, y=1180, z=0.5, keys=[{"t": 0, "x": -200}, {"t": d, "x": 640, "ease": "lineal"}], anim={"balanceo": [4, 0.18]}),
             IMG("gotitas", ancho=300, x=540, y=1050, z=0.6, keys=[{"t": 0, "x": -200}, {"t": d * 0.6, "x": 1300, "ease": "lineal"}]),
             *lineas_vel(400, 1250, 5, "#ffffffaa")],
             cam(1.0, 1.04, (540, 1150), (600, 1150)), "barrido", hud=[amarillo(0.1, d - 0.05, "MÁS QUE UN GUEPARDO", y=560, color="#141414", tam=70)],
             sfx=[(0.05, "whoosh", -16, {"dur": 0.6})])


@v.plano(96, "cuanto más rápido cortas")
def _(d):
    return P(COCINA, [BG("bg_cocina"), IMG("tabla", ancho=1080, x=540, y=1480, z=0.3), IMG("cebolla_mitad", ancho=760, x=540, y=1260, z=0.45),
             cortes(d, 5, 700, 1020, 600), *[chorro(d * (k + 0.45) / 5, 540, 900, 700, dur=0.3) for k in range(5)]],
             cam(1.0, 1.06, (540, 1100), (540, 1080), temblor=4), hud=[amarillo(0.1, d - 0.05, "MÁS RÁPIDO", y=560, color=AMBAR)],
             sfx=[(d * (k + 0.45) / 5, "roce", -16) for k in range(5)])


@v.plano(101, "más desafilado el cuchillo")
def _(d):
    return P(["#1a1e26", "#0a0c10"], [brillo(540, 1000, 600, "#ffffff", 0.15), IMG("cuchillo_romo", ancho=1500, x=640, y=1000, z=0.5, keys=aparece(0.0, 0.35)),
             senala(380, 1130, d * 0.3, d - 0.05, 170, MAGENTA)],
             cam(1.0, 1.1, (540, 1000), (440, 1080)), hud=[amarillo(0.1, d - 0.05, "SIN FILO", y=560, color=MAGENTA)], sfx=[(d * 0.3, "pop", -18)])


@v.plano(108, "más gotas y con más fuerza")
def _(d):
    return P(["#05080c", "#101820"], [IMG("cebolla_mitad", ancho=900, x=540, y=1380, z=0.4), cortes(d, 1, 700, 1100, 600, 0.0, d * 0.6, True),
             chorro(d * 0.3, 540, 850, 1100, dur=d * 0.65), chorro(d * 0.35, 520, 900, 1000, "gotitas", dur=d * 0.6)],
             cam(1.0, 1.06, temblor=6), hud=[amarillo(0.1, d - 0.05, "MÁS FUERZA", y=560, color=CIAN)],
             sfx=[(d * 0.3, "agua", -14, {"dur": 0.8}), (d * 0.3, "golpe", -16)], energia=0.8)


@v.plano(113, "micro: una hoja sin filo")
def _(d):
    return P(["#1a1e26", "#0a0c10"], [IMG("cuchillo_romo", ancho=3000, x=1000, y=860, z=0.5), brillo(300, 1000, 300, "#ff3df2", 0.3)],
             cam(1.1, 1.2, (400, 1000), (420, 1000)), "corte", sfx=[(0.02, "roce", -16)])


@v.plano(118, "hasta cuarenta veces más")
def _(d):
    import random
    rr = random.Random(4)
    gotas = [{"tipo": "forma", "forma": "circulo", "radio": rr.uniform(8, 16), "relleno": "#bfe9ff", "x": rr.uniform(80, 1000), "y": rr.uniform(650, 1450), "z": 0.5,
              "keys": aparece(d * 0.7 * k / 40, 0.2)} for k in range(40)]
    return P(["#05080c", "#101820"], [brillo(540, 1000, 600, "#5ad8ff", 0.3), *gotas],
             cam(1.0, 1.06), hud=[contador(0.05, d - 0.05, 1, 40, d * 0.7, "", tam=150, y=560, borde=MAGENTA, contar_prefijo="×")],
             sfx=[(0.05, "subida", -16, {"dur": d * 0.7}), (d * 0.72, "impacto", -12)], energia=0.9)


@v.plano(124, "el truco que funciona")
def _(d):
    return P(COCINA, [BG("bg_cocina"), IMG("tabla", ancho=1080, x=540, y=1480, z=0.3), IMG("cebolla", ancho=600, x=540, y=1180, z=0.5, anim={"balanceo": [3, 1.2]}),
             brillo(540, 1100, 400, "#ffd23f", 0.4, 0.4, pulso=[0.2, 0.6])],
             cam(1.0, 1.06, (540, 1100), (540, 1080)), "desenfoque", hud=[rotulo(0.1, d - 0.05, "EL TRUCO", tam=120, color="#141414", capsula="#ffd23fe6", y=560)],
             sfx=[(0.05, "ding", -18)])


@v.plano(132, "cuchillo bien afilado")
def _(d):
    return P(["#1a1e26", "#0a0c10"], [IMG("piedra", ancho=900, x=540, y=1250, z=0.4),
             IMG("cuchillo", ancho=900, z=0.6, rot=-12, keys=[{"t": 0, "x": 380, "y": 1100}, {"t": d * 0.5, "x": 700, "y": 1090}, {"t": d, "x": 420, "y": 1100}]),
             brillo(400, 1150, 140, "#ffffff", 0.0, 0.7, keys=[{"t": d * 0.6, "intensidad": 0}, {"t": d * 0.7, "intensidad": 1}, {"t": d, "intensidad": 0}])],
             cam(1.0, 1.08, (540, 1150), (540, 1150)), hud=[amarillo(0.1, d - 0.05, "AFILADO", y=560, color=LIMA)],
             sfx=[(0.1, "roce", -16), (d * 0.55, "roce", -16), (d * 0.7, "brillo", -18)])


@v.plano(136, "y cortar despacio")
def _(d):
    return P(COCINA, [BG("bg_cocina"), IMG("tabla", ancho=1080, x=540, y=1480, z=0.3), IMG("cebolla_mitad", ancho=760, x=540, y=1260, z=0.45),
             cortes(d, 1, 700, 1020, 600, 0.0, d * 1.6), chorro(d * 0.6, 540, 1000, 300, "gotitas", dur=0.5)],
             cam(1.0, 1.05, (540, 1100), (540, 1090)), hud=[amarillo(0.1, d - 0.05, "DESPACIO", y=560, color=CIAN)],
             sfx=[(0.0, "tictac", -22, {"dur": d, "ritmo": 0.5})], energia=0.4)


@v.plano(138, "si quieres ir a lo seguro")
def _(d):
    return P(PIEL, [IMG("ojo", ancho=1150, x=540, y=1000, z=0.5), brillo(540, 1000, 500, "#bfe9ff", 0.2)],
             cam(1.0, 1.05), "desenfoque", hud=[amarillo(0.1, d - 0.05, "A LO SEGURO", y=560, color="#141414", tam=86)])


@v.plano(145, "unas gafas que cierren bien")
def _(d):
    return P(PIEL, [IMG("ojo", ancho=1150, x=540, y=1000, z=0.4),
             IMG("gafas", ancho=1300, x=540, z=0.6, keys=[{"t": 0, "y": 300, "op": 0}, {"t": 0.4, "y": 990, "op": 1, "ease": "elastico"}]),
             IMG("gas", ancho=900, x=540, y=1500, z=0.5, keys=[{"t": 0, "op": 0.6}, {"t": d, "op": 0.0}])],
             cam(1.0, 1.06), sfx=[(0.4, "pop", -16)])


@v.plano(150, "¿cuál es tu truco? (bucle hacia el gancho)")
def _(d):
    return P(COCINA, [BG("bg_cocina"), IMG("tabla", ancho=1080, x=540, y=1480, z=0.3),
             IMG("cebolla", ancho=820, x=540, y=1150, z=0.5, keys=[{"t": 0, "escala": 0.85}, {"t": d, "escala": 1.0, "ease": "suave"}]),
             IMG("cuchillo", ancho=1000, x=600, z=0.7, rot=-4, keys=[{"t": 0, "y": 300}, {"t": d, "y": 520, "ease": "suave"}])],
             cam(1.0, 1.1, (540, 1000), (540, 1000)), "desenfoque", sfx=[(0.05, "roce", -22)])



# ------------------------------------------------------------------ micro planos (golpes de 0,3–0,7 s)
@v.plano(24, "micro: el azufre")
def _(d):
    return P(MICRO, [brillo(540, 960, 500, "#ffd23f", 0.6, pulso=[0.2, 0.15]), IMG("molecula_s", ancho=1300, x=540, y=900, z=0.5, anim={"girar": 30}),
             polvo("#fff3a0", 30, (100, 500, 980, 1500), 13, "chispas")], cam(1.0, 1.1), "corte", sfx=[(0.02, "pop", -18)])


@v.plano(47, "micro: la lágrima")
def _(d):
    return P(PIEL, [IMG("ojo_lloroso", ancho=2600, x=300, y=500, z=0.5), brillo(700, 1100, 300, "#bfe9ff", 0.5),
             {"tipo": "forma", "forma": "elipse", "ancho": 120, "alto": 170, "relleno": "#bfe9ff", "x": 700, "z": 0.6, "keys": [{"t": 0, "y": 1000}, {"t": d, "y": 1300, "ease": "entrada"}]}],
             cam(1.0, 1.1), "corte", sfx=[(0.02, "agua", -20, {"dur": 0.4})])


@v.plano(106, "micro: más gotas")
def _(d):
    return P(["#05080c", "#101820"], [IMG("gotitas_b", ancho=1500, x=540, y=900, z=0.5, keys=[{"t": 0, "escala": 0.8}, {"t": d, "escala": 1.2}]),
             brillo(540, 1000, 500, "#5ad8ff", 0.4)], cam(1.1, 1.2), "corte", sfx=[(0.02, "agua", -18, {"dur": 0.4})])


@v.plano(116, "sin filo: el borde mellado")
def _(d):
    return P(["#1a1e26", "#0a0c10"], [IMG("cuchillo_romo", ancho=2400, x=900, y=900, z=0.5), senala(420, 1040, 0.05, d - 0.05, 140, MAGENTA),
             brillo(420, 1040, 300, "#ff3df2", 0.3)], cam(1.0, 1.08, (500, 1000), (480, 1000)), "corte", sfx=[(0.05, "roce", -18)])

v.construir("2026-11-17-tarde-03-cebolla", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 23, "db": -13},
            claves=["cebolla", "gas", "células", "azufre", "enzima", "lacrimógeno", "córnea", "Cornell", "cuarenta", "guepardo", "afilado", "despacio"])
