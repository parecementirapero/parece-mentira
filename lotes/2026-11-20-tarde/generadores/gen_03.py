"""03 · Los flamencos nacen grises — método denso. Lote 2026-11-20-tarde (Agente 20:00, Jorge). Experimento: gancho de orden («Mira este pollito gris.»).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_1120t  # noqa: E402

SVG = ilus_1120t.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

LAG = ["#4a7ac8", "#5a7a9a"]
MIC = ["#000000", "#000000"]
OSC = ["#1a0a14", "#06020a"]


def laguna(n="bg_laguna"): return BG(n)


def flam(n="flamenco", ancho=620, x=540, y=1150, z=0.5, keys=None, **k):
    """Lienzo 700×1100. Con ancho 620 (escala 0,886): cabeza en (x+142, y−413); garganta en (x+106, y−284)."""
    return IMG(n, ancho=ancho, x=x, y=y, z=z, keys=keys or [], **k)


def cambio(a, b, t0, t1, **k):
    """Un flamenco que cambia de color: el dibujo `a` se funde en `b` entre t0 y t1."""
    return [flam(a, keys=[{"t": t0, "op": 1}, {"t": t1, "op": 0}], **k), flam(b, z=0.51, keys=[{"t": t0, "op": 0}, {"t": t1, "op": 1}], **k)]


def tacha(x, y, t0, t1, r=120):
    return [flecha([[x - r, y - r], [x + r, y + r]], t0, t0 + 0.2, "#ff3d3d", 16, punta=False, z=0.8),
            flecha([[x + r, y - r], [x - r, y + r]], t0 + 0.12, t0 + 0.32, "#ff3d3d", 16, punta=False, z=0.8)]


def gotas(n=24, sem=1, area=(300, 1300, 800, 1700)): return polvo("#bfe8ff", n, area, sem)



def amarillo(t0, t1, texto, y=1360, tam=96, color="#ffd23f", x=540):
    """Palabra clave con cápsula oscura (sobre la laguna y la nieve el texto suelto no llega a 3:1 de contraste)."""
    return {**rotulo(t0, t1, texto, tam=tam, color=color, capsula="#0a0a14c8", rot=-4, x=x, y=y), "_clave": True}


# ================================================================== PLANOS
@v.plano(0, "gancho: el pollito gris entra en la laguna dando saltitos")
def _(d):
    return P(LAG, [laguna(), IMG("pollito", ancho=760, x=540, z=0.55, keys=arranque(540, 1300, d, "derecha", 380, 60)), gotas(16, 1)],
             cam(1.0, 1.06, (540, 1250)), vineta=0.45, sfx=[(0.02, "pop", -16), (0.3, "agua", -20, {"dur": 0.8})])


@v.plano(4, "es un flamenco: a su lado aparece el flamenco adulto rosa")
def _(d):
    return P(LAG, [laguna(), flam(ancho=700, x=680, y=1100, keys=aparece(0.0)), IMG("pollito", ancho=360, x=280, y=1560, z=0.55, keys=[{"t": 0, "x": 320}, {"t": d, "x": 280}])],
             cam(1.0, 1.05, (540, 1200)), "corte", sfx=[(0.05, "brillo", -18)])


@v.plano(7, "todos nacen así: el pollito en lo alto de su nido de barro")
def _(d):
    return P(LAG, [laguna("bg_laguna_tarde"), IMG("nido", ancho=760, x=540, y=1500, z=0.45), IMG("pollito", ancho=420, x=540, y=1200, z=0.5, keys=late(0.3, 2, 0.08))],
             cam(1.0, 1.06, (540, 1350)), "corte", sfx=[(0.3, "pop", -20)])


@v.plano(10, "grises: la pluma gris cae despacio")
def _(d):
    return P(OSC, [brillo(540, 1000, 500, "#a8a8b0", 0.3, 0.06), IMG("pluma_gris", ancho=300, x=540, z=0.5, keys=[{"t": 0, "y": 800, "rot": -20}, {"t": d, "y": 1100, "rot": 15, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[amarillo(0.05, d - 0.03, "GRISES", y=560, tam=130, color="#d8d8dc")], sfx=[(0.05, "roce", -20)])


@v.plano(11, "sin nada de rosa: una pluma rosa se tacha")
def _(d):
    return P(OSC, [brillo(540, 1000, 500, "#ff7aa0", 0.3, 0.06), IMG("pluma_rosa", ancho=300, x=540, y=1000, z=0.5, keys=aparece(0.0)), *tacha(540, 1000, 0.35, d, 180)],
             cam(1.0, 1.05, (540, 1000)), "corte", sfx=[(0.35, "zap", -18)])


@v.plano(15, "¿entonces de dónde sale el color?: el flamenco rosa late en la laguna")
def _(d):
    return P(LAG, [laguna(), flam(ancho=720, keys=late(0.3, 2, 0.06, 0.4))], cam(1.0, 1.08, (540, 1100)), "desenfoque",
             hud=[amarillo(0.2, d - 0.05, "¿DE DÓNDE?", y=560, tam=120, color=MAGENTA)], sfx=[(0.1, "roce", -20)])


@v.plano(21, "de lo que comen: el flamenco baja la cabeza al agua")
def _(d):
    return P(LAG, [laguna(), *cambio("flamenco", "flamenco_comiendo", 0.1, 0.5, ancho=700), gotas(20, 2, (500, 1350, 900, 1600))],
             cam(1.0, 1.05, (540, 1200)), "corte", hud=[amarillo(0.08, d - 0.03, "LO QUE COMEN", y=560, tam=110, color=LIMA)], sfx=[(0.3, "agua", -20, {"dur": 0.6})])


@v.plano(25, "meten la cabeza del revés en el agua: primer plano de la cabeza boca abajo")
def _(d):
    return P(LAG, [laguna(), flam("flamenco_comiendo", ancho=1300, x=320, y=900, keys=[{"t": 0, "y": 860}, {"t": d, "y": 920, "ease": "suave"}]),
                   gotas(30, 3, (600, 1500, 1000, 1800))],
             cam(1.0, 1.06, (700, 1500)), "corte", hud=[rotulo(0.4, d - 0.05, "DEL REVÉS", tam=110, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "agua", -22, {"dur": 0.6})])


@v.plano(35, "y la filtran con el pico: el agua pasa por el pico")
def _(d):
    return P(LAG, [laguna(), flam("flamenco_comiendo", ancho=1300, x=320, y=880),
                   flecha([[1000, 1700], [820, 1620], [700, 1560]], 0.05, d * 0.6, CIAN, 8, z=0.6), gotas(40, 4, (600, 1450, 1050, 1800))],
             cam(1.4, 1.5, (720, 1520)), "corte", sfx=[(0.05, "burbuja", -20), (0.4, "burbuja", -22)])


@v.plano(41, "como un colador: el colador escurre agua")
def _(d):
    return P(["#0a2030", "#04101a"], [brillo(540, 1000, 500, "#7ac8f0", 0.3, 0.06), IMG("colador", ancho=820, x=540, y=1000, z=0.5, keys=aparece(0.0)),
                                      polvo("#7ad0ff", 50, (350, 1150, 750, 1700), 5)],
             cam(1.0, 1.05, (540, 1100)), "corte", sfx=[(0.1, "agua", -20, {"dur": 0.8})])


@v.plano(44, "se quedan con algas: al microscopio, algas rojas y naranjas")
def _(d):
    return P(MIC, [BG("bg_micro"), IMG("algas", ancho=820, x=540, y=1000, z=0.5, keys=[{"t": 0, "rot": -6, "escala": 0.9}, {"t": d, "rot": 6, "escala": 1.0, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[amarillo(0.1, d - 0.05, "ALGAS", y=1620 - 200, tam=120, color=LIMA)], sfx=[(0.05, "burbuja", -20)])


@v.plano(48, "y gambitas diminutas: una gambita cruza el microscopio")
def _(d):
    return P(MIC, [BG("bg_micro"), IMG("gambita", ancho=700, y=1000, z=0.5, keys=[{"t": 0, "x": 200, "rot": -5}, {"t": d, "x": 700, "rot": 5, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[amarillo(0.1, d - 0.05, "GAMBITAS", y=1420, tam=120, color=AMBAR)], sfx=[(0.05, "burbuja", -20)])


@v.plano(51, "y esas gambitas van cargadas de pigmentos: la gambita brilla naranja")
def _(d):
    return P(MIC, [BG("bg_micro"), IMG("gambita", ancho=800, x=540, y=1000, z=0.5, keys=late(0.3, 2, 0.08, 0.5)),
                   brillo(540, 1000, 380, "#ff8a3a", 0.6, 0.6, keys=[{"t": 0, "op": 0}, {"t": d * 0.7, "op": 1}])],
             cam(1.0, 1.08, (540, 1000)), "corte", hud=[rotulo(d * 0.5, d - 0.05, "PIGMENTOS", tam=100, color="#141414", capsula="#ffb02ee6", y=1420)], sfx=[(0.1, "subida", -20, {"dur": d * 0.7})])


@v.plano(59, "los carotenoides: las algas y el nombre")
def _(d):
    return P(MIC, [BG("bg_micro"), IMG("algas", ancho=900, x=540, y=1000, z=0.5, keys=late(0.1, 1))], cam(1.05, 1.1, (540, 1000)), "corte",
             hud=[rotulo(0.05, d - 0.03, "CAROTENOIDES", tam=96, color="#141414", capsula="#ffb02ee6", y=560)], sfx=[(0.05, "ding", -20)])


@v.plano(61, "de la misma familia que el naranja de la zanahoria: gambita y zanahoria juntas")
def _(d):
    return P(["#2a1a0a", "#0a0604"], [brillo(540, 1100, 600, "#ff8a3a", 0.35, 0.06), IMG("gambita", ancho=480, x=320, y=1050, z=0.5, keys=aparece(0.0)),
                                      IMG("zanahoria", ancho=300, x=790, y=1100, z=0.5, keys=aparece(0.5)), {"tipo": "forma", "forma": "circulo", "radio": 14, "relleno": "#ffffff", "x": 580, "y": 1060, "z": 0.5, "keys": aparece(0.4)},
                                      {"tipo": "forma", "forma": "circulo", "radio": 14, "relleno": "#ffffff", "x": 580, "y": 1120, "z": 0.5, "keys": aparece(0.4)}],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[amarillo(0.6, d - 0.05, "MISMA FAMILIA", y=560, tam=100, color=AMBAR)], sfx=[(0.5, "pop", -18)])


@v.plano(71, "¿y cómo llegan a las plumas?: la pluma gris con una flecha")
def _(d):
    return P(OSC, [brillo(540, 1050, 500, "#ff7aa0", 0.3, 0.06), IMG("pluma_gris", ancho=320, x=540, y=1050, z=0.5, keys=[{"t": 0, "rot": -6}, {"t": d, "rot": 6, "ease": "suave"}]),
                   flecha([[160, 1500], [400, 1200]], 0.1, d * 0.6, MAGENTA, 10, z=0.6)],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[amarillo(0.2, d - 0.05, "¿CÓMO?", y=560, tam=130, color=MAGENTA)], sfx=[(0.1, "roce", -20)])


@v.plano(77, "su cuerpo los procesa y los reparte, poco a poco: la pluma gris se vuelve rosa")
def _(d):
    return P(OSC, [brillo(540, 1050, 500, "#ff7aa0", 0.4, 0.06, keys=[{"t": 0, "op": 0.2}, {"t": d, "op": 1}]),
                   IMG("pluma_gris", ancho=320, x=540, y=1050, z=0.5, keys=[{"t": 0, "op": 1}, {"t": d * 0.8, "op": 0}]),
                   IMG("pluma_rosa", ancho=320, x=540, y=1050, z=0.51, keys=[{"t": 0, "op": 0}, {"t": d * 0.8, "op": 1}])],
             cam(1.0, 1.1, (540, 1050)), "corte", hud=[amarillo(d * 0.6, d - 0.05, "POCO A POCO", y=560, tam=110, color="#ff8aa8")], sfx=[(0.1, "brillo", -20)])


@v.plano(87, "por eso tardan unos tres años en ponerse rosas del todo: el joven gris se vuelve rosa")
def _(d):
    return P(LAG, [laguna(), *cambio("flamenco_joven", "flamenco", d * 0.2, d * 0.85, ancho=640, x=540, y=1180)],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[contador(0.1, d - 0.03, 0, 3, d * 0.6, " AÑOS", y=560, tam=130, color="#ffd23f", capsula="#000000a0")],
             sfx=[(0.1, "tictac", -22, {"dur": d * 0.6, "ritmo": 0.3})])


@v.plano(98, "¿y lo más raro?: el pollito mira")
def _(d):
    return P(LAG, [laguna("bg_laguna_tarde"), IMG("pollito", ancho=700, x=540, y=1300, z=0.5, keys=[{"t": 0, "rot": -8}, {"t": d * 0.5, "rot": 8}, {"t": d, "rot": 0}])],
             cam(1.0, 1.06, (540, 1250)), "corte", hud=[amarillo(0.05, d - 0.03, "¿MÁS RARO?", y=560, tam=120, color=MAGENTA)], sfx=[(0.1, "pop", -20)])


@v.plano(102, "cómo alimentan al pollito: el adulto se inclina sobre el nido")
def _(d):
    return P(LAG, [laguna("bg_laguna_tarde"), IMG("nido", ancho=600, x=330, y=1580, z=0.45), IMG("pollito", ancho=320, x=330, y=1340, z=0.5),
                   flam("flamenco_comiendo", ancho=700, x=600, y=1060, keys=[{"t": 0, "x": 680}, {"t": d, "x": 600, "ease": "suave"}])],
             cam(1.0, 1.05, (500, 1300)), "corte", sfx=[(0.1, "roce", -20)])


@v.plano(106, "con una especie de leche roja: la gota roja aparece")
def _(d):
    return P(OSC, [brillo(540, 1050, 600, "#ff3d3d", 0.35, 0.06), IMG("gota_leche", ancho=360, x=540, y=1050, z=0.5, keys=cae(0.0, 0.5, 700, 1050) + late(0.8, 1))],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[rotulo(0.3, d - 0.03, "LECHE ROJA", tam=104, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.35, "golpe", -18)])


@v.plano(112, "que fabrican en la garganta: anillo en el cuello del flamenco")
def _(d):
    return P(LAG, [laguna(), flam(ancho=620, x=480, y=1150), senala(586, 866, 0.1, d - 0.1, 80, LIMA),
                   flecha([[600, 760], [600, 960]], 0.2, d * 0.7, "#ff3d3d", 10, z=0.6)],
             cam(1.4, 1.5, (560, 900)), "corte", hud=[amarillo(0.2, d - 0.05, "GARGANTA", y=1320, tam=110, color=LIMA)], sfx=[(0.1, "pop", -20)])


@v.plano(117, "la hacen el padre y la madre: dos flamencos frente a frente")
def _(d):
    return P(LAG, [laguna(), flam(ancho=560, x=330, y=1200, keys=aparece(0.0)), flam(ancho=560, x=760, y=1200, z=0.51, keys=[{"t": 0, "ex": -1, "escala": 0, "op": 0}, {"t": 0.3, "op": 1}, {"t": 0.6, "escala": 1, "ex": -1, "ease": "elastico"}])],
             cam(1.0, 1.04, (540, 1150)), "corte", hud=[rotulo(0.1, d - 0.03, "LOS DOS", tam=110, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "pop", -20), (0.35, "pop", -20)])


@v.plano(124, "y esa leche lleva tanto pigmento: la gota roja brilla y late")
def _(d):
    return P(OSC, [brillo(540, 1050, 600, "#ff3d3d", 0.5, 0.06, pulso=[0.15, 0.8]), IMG("gota_leche", ancho=460, x=540, y=1050, z=0.5, keys=late(0.1, 3, 0.1, 0.5))],
             cam(1.0, 1.1, (540, 1050)), "corte", hud=[amarillo(0.3, d - 0.05, "PIGMENTO", y=560, tam=120, color="#ff6a6a")], sfx=[(0.1, "brillo", -20)])


@v.plano(131, "mientras crían, los padres se van quedando pálidos: el rosa se apaga")
def _(d):
    return P(LAG, [laguna("bg_laguna_tarde"), *cambio("flamenco", "flamenco_palido", d * 0.25, d * 0.9, ancho=660, x=600, y=1150),
                   IMG("pollito", ancho=300, x=260, y=1620, z=0.55)],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[amarillo(d * 0.5, d - 0.05, "PÁLIDOS", y=560, tam=130, color="#f4f0e8")], sfx=[(0.1, "roce", -20)])


@v.plano(139, "casi blancos: el flamenco pálido de cerca")
def _(d):
    return P(LAG, [laguna("bg_laguna_tarde"), flam("flamenco_palido", ancho=900, x=440, y=1150, keys=late(0.1, 1, 0.05))],
             cam(1.0, 1.06, (540, 900)), "corte", hud=[rotulo(0.1, d - 0.05, "CASI BLANCOS", tam=100, color="#141414", capsula="#f4f0e8e6", y=1380)], sfx=[(0.05, "ding", -20)])


@v.plano(141, "cuando el pollito ya come solo: el joven gris camina por la laguna")
def _(d):
    return P(LAG, [laguna(), flam("flamenco_joven", ancho=560, y=1200, keys=[{"t": 0, "x": 300}, {"t": d, "x": 600, "ease": "lineal"}]), gotas(20, 6)],
             cam(1.0, 1.04, (540, 1150)), "corte", sfx=[(0.1, "agua", -22, {"dur": 0.6})])


@v.plano(147, "recuperan su rosa: el pálido vuelve a ser rosa")
def _(d):
    return P(LAG, [laguna(), *cambio("flamenco_palido", "flamenco", 0.05, d * 0.8, ancho=700, x=540, y=1150), brillo(540, 1000, 500, "#ff8aa8", 0.4, 0.07)],
             cam(1.0, 1.08, (540, 1100)), "corte", hud=[amarillo(0.2, d - 0.03, "ROSA", y=560, tam=140, color="#ff8aa8")], sfx=[(0.1, "brillo", -18)])


@v.plano(150, "le han dado su color a su hijo: flecha del adulto al pollito")
def _(d):
    return P(LAG, [laguna("bg_laguna_tarde"), flam("flamenco_palido", ancho=620, x=700, y=1100), IMG("pollito", ancho=380, x=280, y=1560, z=0.55, keys=late(d * 0.6, 1)),
                   flecha([[600, 900], [400, 1100], [300, 1350]], 0.1, d * 0.6, MAGENTA, 10, z=0.6)],
             cam(1.0, 1.05, (540, 1250)), "corte", hud=[rotulo(0.3, d - 0.05, "SU COLOR", tam=104, color="#ffffff", capsula="#c0397ae6", y=560)], sfx=[(d * 0.6, "ding", -20)])


@v.plano(158, "literalmente: el pollito gris otra vez en la laguna (bucle con el principio)")
def _(d):
    return P(LAG, [laguna(), IMG("pollito", ancho=760, x=540, y=1300, z=0.55, keys=[{"t": 0, "x": 640}, {"t": d, "x": 560, "ease": "suave"}]), gotas(16, 7)],
             cam(1.0, 1.05, (540, 1250)), "corte", sfx=[(0.05, "pop", -18)])


# ------------------------------------------------------------------ micro planos (ritmo)
@v.plano(2, "micro: «pollito», la cara del pollito de cerca")
def _(d):
    return P(LAG, [laguna(), IMG("pollito", ancho=760, x=540, y=1300, z=0.55, keys=[{"t": 0, "x": 520}, {"t": d, "x": 500}])],
             cam(1.6, 1.7, (660, 1100)), "corte", sfx=[(0.02, "pop", -20)])



v.construir("2026-11-20-tarde-03-flamencos-nacen-grises", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 73, "db": -13},
            claves=["pollito", "gris", "flamenco", "grises", "rosa", "color", "comen", "cabeza", "revés", "pico", "colador", "algas", "gambitas", "pigmentos",
                    "carotenoides", "naranja", "zanahoria", "plumas", "tres", "años", "leche", "roja", "garganta", "padre", "madre", "pálidos", "blancos", "hijo"])
