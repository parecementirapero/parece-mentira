"""03 · Esta imagen está al revés (la imagen llega invertida a la retina; Stratton, 1896, ocho días con lentes que giraban la vista)
— método denso. Lote 2026-11-22-manana (Agente 08:00, Nico).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_1122m  # noqa: E402

SVG = ilus_1122m.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

AZUL = ["#0a1a30", "#02060e"]
DIA = ["#3a8ae0", "#d8f0ff"]
SALON = ["#3a3020", "#1a1408"]


def mundo(n="bg_paisaje", keys=None, z=0.05):
    """Fondo grande (cubre la pantalla aunque gire)."""
    return IMG(n, ancho=2300, x=540, y=960, z=z, keys=keys or [])


def motas(sem=1, col="#cfe8ff", n=35): return polvo(col, n, (60, 400, 1020, 1600), sem)


def arbol_rev(x, y, ancho=260, rot=180, z=0.3, keys=None): return IMG("arbol_verde", ancho=ancho, x=x, y=y, z=z, rot=rot, keys=keys or [])


# ojo cortado: ancho 700 centrado en (640, 1000) → cristalino en (493, 1000), retina en x≈860
def ojo_c(keys=None, z=0.45): return IMG("ojo_corte", ancho=700, x=640, y=1000, z=z, keys=keys or [])


# ================================================================== PLANOS
@v.plano(0, "gancho: un árbol gigante da la vuelta y se queda boca abajo")
def _(d):
    return P(DIA, [mundo("bg_paisaje", [{"t": 0, "rot": 0}, {"t": 0.7, "rot": 180, "ease": "salida"}, {"t": d, "rot": 184}]),
                   IMG("arbol_verde", ancho=700, x=540, z=0.5, keys=[{"t": 0, "rot": 0, "y": 1150, "escala": 0.8}, {"t": 0.7, "rot": 180, "y": 1000, "escala": 1.0, "ease": "elastico"}, {"t": d, "rot": 188, "escala": 1.08}]),
                   motas(1, "#ffffff", 50)],
             cam(1.0, 1.12, (540, 1000)), vineta=0.5, sfx=[(0.05, "whoosh", -14), (0.55, "golpe", -14)])


@v.plano(5, "así llega el mundo al fondo de tu ojo: la cámara entra en la pupila")
def _(d):
    return P(["#d8a080", "#8a5040"], [IMG("ojo", ancho=1500, x=540, y=1000, z=0.4), IMG("arbol_verde", ancho=120, x=540, y=1000, z=0.45, rot=180, op=0.8), motas(2, "#ffe8d8"), brillo(540, 1000, 300, "#000000", 0.3, 0.42)],
             cam(1.0, 2.2, (540, 1000)), "desenfoque", sfx=[(0.1, "subida", -20, {"dur": d})])


@v.plano(14, "¿por qué?: el ojo cortado aparece")
def _(d):
    return P(AZUL, [brillo(540, 1000, 600, "#7ad0ff", 0.2, 0.05), ojo_c(aparece(0.0)), motas(3)],
             cam(0.8 + 0.2, 1.04, (600, 1000)), "corte", hud=[amarillo(0.1, d - 0.05, "¿POR QUÉ?", y=560, tam=130, color="#ffffff")], sfx=[(0.05, "roce", -18)])


@v.plano(16, "el cristalino: se señala la lente del ojo")
def _(d):
    return P(AZUL, [brillo(540, 1000, 600, "#7ad0ff", 0.2, 0.05), ojo_c(), senala(493, 1000, 0.1, d - 0.1, 110, CIAN), motas(4), flecha([[200, 760], [430, 940]], 0.1, d * 0.7, CIAN, 7, z=0.6)],
             cam(1.35, 1.45, (520, 980)), "corte", hud=[rotulo(0.2, d - 0.03, "CRISTALINO", tam=100, color="#141414", capsula="#2ff3ffe6", y=560)])


@v.plano(18, "la lente que tienes dentro del ojo: primer plano del cristalino que brilla")
def _(d):
    return P(["#102a4a", "#040a16"], [ojo_c(), brillo(493, 1000, 140, "#ffffff", 0.6, 0.5, pulso=[0.15, 0.6]), motas(5), brillo(300, 1000, 300, "#ffe93d", 0.25, 0.3)],
             cam(2.3, 2.6, (500, 1000)), "corte", hud=[rotulo(0.2, d - 0.03, "UNA LENTE", tam=100, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "brillo", -20)])


def rayos(d, t0=0.05, dur=None, img=True):
    dur = dur or d * 0.7
    els = [IMG("arbol_verde", ancho=200, x=150, y=1000, z=0.5), ojo_c(),
           flecha([[150, 860], [493, 1000], [835, 1140]], t0, t0 + dur, AMBAR, 6, z=0.55),
           flecha([[150, 1120], [493, 1000], [835, 860]], t0 + 0.1, t0 + 0.1 + dur, CIAN, 6, z=0.55)]
    if img:
        els.append(IMG("arbol_verde", ancho=110, x=815, y=1000, z=0.56, rot=180, keys=[{"t": 0, "op": 0}, {"t": t0 + dur, "op": 0}, {"t": t0 + dur + 0.2, "op": 1}]))
    return els


@v.plano(25, "cruza los rayos de luz: dos rayos del árbol se cruzan en la lente")
def _(d):
    return P(AZUL, [brillo(540, 1000, 600, "#7ad0ff", 0.2, 0.05), *rayos(d), motas(6)], cam(1.0, 1.08, (500, 1000)), "corte",
             hud=[amarillo(0.3, d - 0.05, "SE CRUZAN", y=560, tam=110, color=AMBAR)], sfx=[(0.1, "zap", -22)])


@v.plano(30, "lo de arriba: se señala la copa del árbol")
def _(d):
    return P(AZUL, [brillo(540, 1000, 600, "#7ad0ff", 0.2, 0.05), *rayos(d, 0.0, 0.01), senala(150, 900, 0.05, d - 0.05, 90, AMBAR), motas(7)],
             cam(1.7, 1.8, (280, 960)), "corte", hud=[rotulo(0.0, d - 0.01, "ARRIBA", tam=90, color="#141414", capsula="#ffe93de6", y=560)])


@v.plano(33, "cae abajo: la imagen de la copa aparece abajo, en la retina")
def _(d):
    return P(AZUL, [brillo(540, 1000, 600, "#7ad0ff", 0.2, 0.05), *rayos(d, 0.0, 0.01), senala(820, 1090, 0.02, d - 0.05, 80, AMBAR), motas(8)],
             cam(2.0, 2.2, (800, 1020)), "corte", hud=[rotulo(0.05, d - 0.02, "ABAJO", tam=90, color="#141414", capsula="#ffe93de6", y=560)], sfx=[(0.05, "pop", -20)])


@v.plano(35, "y lo de la izquierda pasa a la derecha: dos rayos se cruzan de lado a lado")
def _(d):
    return P(["#2a0a3a", "#0a0214"], [brillo(540, 1000, 600, "#ff3df2", 0.25, 0.05), motas(9, "#ffc8f4"), flecha([[880, 840], [540, 1000], [210, 1200]], 0.2, d * 0.8, CIAN, 7, z=0.54),
                    IMG("arbol_verde", ancho=150, x=880, y=760, z=0.5, keys=aparece(0.1)), IMG("arbol_verde", ancho=110, x=200, y=1240, z=0.5, keys=[{"t": 0, "op": 0}, {"t": d * 0.8, "op": 0}, {"t": d * 0.85, "op": 1}]),
                    IMG("melocoton", ancho=150, x=200, y=760, z=0.5, keys=aparece(0.0)),
                    {"tipo": "forma", "forma": "circulo", "radio": 70, "relleno": "#e8f6ff", "borde": "#9ad0f0", "grosor": 5, "x": 540, "y": 1000, "z": 0.45},
                    flecha([[200, 840], [540, 1000], [870, 1200]], 0.1, d * 0.7, MAGENTA, 7, z=0.55),
                    IMG("melocoton", ancho=110, x=880, y=1240, z=0.5, keys=[{"t": 0, "op": 0}, {"t": d * 0.7, "op": 0}, {"t": d * 0.75, "op": 1}])],
             cam(1.0, 1.04, (540, 1000)), "corte",
             hud=[rotulo(0.1, d - 0.03, "IZQUIERDA", tam=70, color="#141414", capsula="#ff3df2e6", x=260, y=560), rotulo(d * 0.5, d - 0.03, "DERECHA", tam=70, color="#141414", capsula="#ff3df2e6", x=760, y=1340)],
             sfx=[(0.1, "zap", -22)])


@v.plano(44, "como en una cámara antigua: la cámara de fuelle con el árbol al revés en el cristal")
def _(d):
    return P(SALON, [mundo("bg_salon_1896"), IMG("camara_fuelle", ancho=900, x=540, y=1050, z=0.45, keys=aparece(0.0)),
                     IMG("arbol_verde", ancho=120, x=948, y=1020, z=0.5, rot=180, keys=[{"t": 0, "op": 0}, {"t": 0.5, "op": 0}, {"t": 0.8, "op": 1}])],
             cam(1.0, 1.08, (600, 1050)), "corte", hud=[rotulo(0.2, d - 0.03, "CÁMARA ANTIGUA", tam=86, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.6, "tic", -14)])


@v.plano(49, "es tu cerebro: el cerebro aparece y se ilumina")
def _(d):
    return P(["#1a0a2a", "#06020e"], [brillo(540, 1000, 500, "#ff6ab0", 0.4, 0.1, pulso=[0.1, 0.8]), IMG("cerebro", ancho=760, x=540, y=1000, z=0.45, keys=aparece(0.0))],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[rotulo(0.03, d - 0.02, "CEREBRO", tam=110, color="#141414", capsula="#ff3df2e6", y=560)], sfx=[(0.05, "brillo", -18)])


@v.plano(53, "el que le da la vuelta: el árbol gira y queda derecho, con flecha circular")
def _(d):
    import math
    circ = [[540 + 330 * math.cos(math.radians(a)), 1000 + 330 * math.sin(math.radians(a))] for a in range(-60, 200, 10)]
    return P(["#1a0a2a", "#06020e"], [IMG("cerebro", ancho=500, x=540, y=1000, z=0.3, op=0.4),
                                      IMG("arbol_verde", ancho=420, x=540, y=1000, z=0.5, keys=[{"t": 0, "rot": 180}, {"t": d * 0.8, "rot": 360, "ease": "elastico"}]),
                                      flecha(circ, 0.0, d * 0.8, LIMA, 8, z=0.55), motas(10, "#ffc8f4"), brillo(540, 1000, 500, "#7dff3a", 0.25, 0.1)],
             cam(1.0, 1.04, (540, 1000)), "corte", sfx=[(0.05, "whoosh", -16)])


@v.plano(58, "sin que te enteres: una cara tranquila de perfil")
def _(d):
    return P(["#2a3a5a", "#0a1020"], [IMG("cara_perfil", ancho=820, x=520, y=1100, z=0.45, keys=[{"t": 0, "x": 560}, {"t": d, "x": 500, "ease": "suave"}]),
                                      IMG("arbol_verde", ancho=180, x=860, y=820, z=0.5, keys=aparece(0.2))],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[amarillo(0.2, d - 0.05, "SIN ENTERARTE", y=560, tam=96, color=LIMA)])


@v.plano(62, "¿y si lo engañas?: el tubo de lentes aparece girando")
def _(d):
    return P(AZUL, [brillo(540, 1000, 500, "#7ad0ff", 0.3, 0.1), IMG("tubo_lentes", ancho=760, x=540, y=1000, z=0.45, keys=aparece(0.0) + [{"t": 0.4, "rot": -10}, {"t": d, "rot": 10}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[amarillo(0.15, d - 0.05, "¿Y SI LO ENGAÑAS?", y=560, tam=90, color=CIAN)], sfx=[(0.1, "roce", -18)])


@v.plano(66, "en 1896: la hoja del calendario cae")
def _(d):
    return P(SALON, [mundo("bg_salon_1896"), IMG("cal_1896", ancho=620, x=540, z=0.5, keys=cae(0.0, 0.7, 500, 1000) + [{"t": 0.7, "rot": -3}, {"t": d, "rot": 3}])],
             cam(1.0, 1.05, (540, 1000)), "corte", sfx=[(0.45, "golpe", -16)])


@v.plano(72, "un psicólogo, George Stratton: la silueta con el tubo en el ojo")
def _(d):
    return P(SALON, [mundo("bg_salon_1896"), brillo(700, 700, 500, "#7ad0ff", 0.3, 0.1), IMG("stratton", ancho=820, x=500, y=1150, z=0.5, keys=arranque(500, 1150, d, "izquierda", 200, 30))],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[rotulo(0.1, d * 0.4, "PSICÓLOGO", tam=90, color="#141414", capsula="#ffd23fe6", y=560),
                                                       rotulo(d * 0.42, d - 0.03, "GEORGE STRATTON", tam=80, color="#ffffff", capsula="#000000b0", y=560)])


@v.plano(76, "quiso probarlo: el tubo se coloca de golpe")
def _(d):
    return P(AZUL, [brillo(540, 1000, 500, "#7ad0ff", 0.3, 0.1), IMG("tubo_lentes", ancho=900, x=540, z=0.45, keys=lanza(0.0, 0.5, (1400, 1000), (540, 1000)))],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[amarillo(0.3, d - 0.05, "¡A PRUEBA!", y=560, tam=120, color=AMBAR)], sfx=[(0.4, "golpe", -14)])


@v.plano(78, "se tapó un ojo: un parche negro baja sobre el ojo")
def _(d):
    return P(["#d8a080", "#8a5040"], [IMG("ojo", ancho=1300, x=540, y=1000, z=0.4),
                                      {"tipo": "forma", "forma": "elipse", "ancho": 760, "alto": 420, "relleno": "#14141a", "x": 540, "z": 0.5,
                                       "keys": [{"t": 0, "y": 300}, {"t": d * 0.5, "y": 1000, "ease": "salida"}]}],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[rotulo(0.05, d - 0.02, "TAPADO", tam=100, color="#141414", capsula="#ffffffe6", y=560)], sfx=[(d * 0.45, "golpe", -18)])


@v.plano(89, "tubo: el tubo de cerca, con reflejos")
def _(d):
    return P(SALON, [mundo("bg_salon_1896"), brillo(540, 1000, 500, "#7ad0ff", 0.4, 0.1), motas(11), IMG("tubo_lentes", ancho=1000, x=540, y=1000, z=0.45, keys=[{"t": 0, "rot": -6, "escala": 1.1}, {"t": d, "rot": 0, "escala": 1.0}])],
             cam(1.2, 1.3, (700, 1000)), "corte", sfx=[(0.05, "tic", -16)])


@v.plano(82, "y en el otro se puso un tubo con lentes: se señala el tubo")
def _(d):
    return P(SALON, [mundo("bg_salon_1896"), IMG("stratton", ancho=900, x=440, y=1180, z=0.5), senala(800, 990, 0.3, d - 0.1, 150, CIAN)],
             cam(1.1, 1.3, (620, 1000)), "corte", hud=[rotulo(0.1, d - 0.03, "LENTES", tam=100, color="#141414", capsula="#2ff3ffe6", y=560)])


@v.plano(92, "que le giraban la vista: el salón da media vuelta")
def _(d):
    return P(SALON, [mundo("bg_salon_1896", [{"t": 0, "rot": 0}, {"t": d * 0.8, "rot": 180, "ease": "suave"}, {"t": d, "rot": 180}]), motas(12, "#ffe8b0"),
                     flecha([[240, 700], [540, 520], [840, 700]], 0.05, d * 0.7, AMBAR, 8, z=0.6)],
             cam(1.0, 1.05, (540, 960)), "corte", sfx=[(0.05, "whoosh", -14)])


@v.plano(97, "lo llevó: la silueta con el tubo, de lado")
def _(d):
    return P(SALON, [mundo("bg_salon_1896", [{"t": 0, "rot": 180}]), IMG("stratton", ancho=700, x=560, y=1150, z=0.5, keys=[{"t": 0, "x": 600}, {"t": d, "x": 540}])],
             cam(1.0, 1.05, (540, 1050)), "corte")


@v.plano(99, "ocho días: ocho casillas se encienden")
def _(d):
    els = [mundo("bg_salon_1896", [{"t": 0, "rot": 180}]), {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 1920, "relleno": "#000000", "op": 0.55, "x": 540, "y": 960, "z": 0.1}]
    for k in range(8):
        x, y = 230 + (k % 4) * 207, 900 + (k // 4) * 230
        els.append({"tipo": "forma", "forma": "rect", "ancho": 170, "alto": 190, "relleno": "#ffd23f", "x": x, "y": y, "z": 0.5, "keys": aparece(0.05 + k * min(0.1, d * 0.7 / 8))})
    return P(SALON, els, cam(1.0, 1.04, (540, 1000)), "corte", hud=[contador(0.05, d - 0.03, 1, 8, d * 0.7, " DÍAS", y=560, tam=120, color="#ffd23f")],
             sfx=[(0.05, "tictac", -22, {"dur": d * 0.7, "ritmo": 0.1})])


@v.plano(101, "al principio, todo estaba patas arriba: el salón al revés se tambalea")
def _(d):
    return P(SALON, [mundo("bg_salon_1896", [{"t": 0, "rot": 176}, {"t": d * 0.5, "rot": 184}, {"t": d, "rot": 178}]), motas(13, "#ffe8b0"), arbol_rev(800, 600, 300, 180, 0.3, [{"t": 0, "rot": 176}, {"t": d, "rot": 186}])],
             cam(1.05, 1.1, (540, 960), temblor=3), "corte", hud=[amarillo(0.4, d - 0.05, "PATAS ARRIBA", y=1100, tam=110, color=AMBAR)], sfx=[(0.2, "rumor", -20, {"dur": d})])


@v.plano(106, "arriba: una taza cae hacia el techo")
def _(d):
    return P(SALON, [mundo("bg_salon_1896", [{"t": 0, "rot": 180}]), motas(21, "#ffe8b0"), flecha([[540, 1300], [540, 700]], 0.0, d * 0.8, AMBAR, 12, z=0.6)],
             cam(1.5, 1.7, (540, 900), temblor=4), "corte", sfx=[(0.0, "golpe", -14)])


@v.plano(107, "el suelo arriba: el paisaje al revés, se señala el suelo arriba")
def _(d):
    return P(DIA, [mundo("bg_paisaje", [{"t": 0, "rot": 180}]), senala(540, 420, 0.05, d - 0.05, 200, AMBAR), arbol_rev(300, 560, 320), motas(14, "#ffffff"), flecha([[540, 900], [540, 560]], 0.05, d * 0.7, AMBAR, 9, z=0.6)],
             cam(1.4, 1.5, (540, 560)), "corte", hud=[rotulo(0.1, d - 0.03, "SUELO", tam=100, color="#141414", capsula="#ffe93de6", y=760)], sfx=[(0.05, "pop", -18)])


@v.plano(110, "el cielo abajo: se señala el cielo abajo")
def _(d):
    return P(DIA, [mundo("bg_paisaje", [{"t": 0, "rot": 180}]), senala(540, 1300, 0.05, d - 0.05, 200, CIAN), motas(15, "#ffffff"), flecha([[540, 900], [540, 1240]], 0.05, d * 0.7, CIAN, 9, z=0.6)],
             cam(1.4, 1.5, (540, 1350)), "corte", hud=[rotulo(0.1, d - 0.03, "CIELO", tam=100, color="#141414", capsula="#2ff3ffe6", y=1100)], sfx=[(0.05, "pop", -18)])


@v.plano(113, "pero a los pocos días: el paisaje al revés empieza a temblar")
def _(d):
    return P(DIA, [mundo("bg_paisaje", [{"t": 0, "rot": 180}, {"t": d, "rot": 172, "ease": "suave"}]), arbol_rev(540, 900, 520, 180, 0.4, [{"t": 0, "rot": 180}, {"t": d, "rot": 168, "ease": "suave"}]), motas(16, "#ffffff")],
             cam(1.0, 1.08, (540, 960)), "desenfoque", hud=[rotulo(0.05, d - 0.02, "POCOS DÍAS", tam=96, color="#ffffff", capsula="#000000b0", y=560)])


@v.plano(118, "el mundo volvió a parecerle normal: el paisaje gira y queda derecho")
def _(d):
    return P(DIA, [mundo("bg_paisaje", [{"t": 0, "rot": 172}, {"t": d * 0.6, "rot": 360, "ease": "elastico"}, {"t": d, "rot": 360}]), arbol_rev(540, 1000, 520, 0, 0.4, [{"t": 0, "rot": 168}, {"t": d * 0.6, "rot": 360, "ease": "elastico"}]), motas(17, "#ffffff")],
             cam(1.0, 1.04, (540, 960)), "corte", hud=[rotulo(d * 0.6, d - 0.03, "NORMAL", tam=120, color="#141414", capsula="#7dff3ae6", y=560)],
             sfx=[(0.05, "whoosh", -14), (d * 0.55, "impacto", -14)])


@v.plano(124, "su cerebro se había adaptado: el cerebro late con flechas que giran")
def _(d):
    import math
    circ = [[540 + 380 * math.cos(math.radians(a)), 1000 + 300 * math.sin(math.radians(a))] for a in range(200, 470, 10)]
    return P(["#1a0a2a", "#06020e"], [brillo(540, 1000, 500, "#7dff3a", 0.35, 0.1, pulso=[0.1, 0.7]),
                                      IMG("cerebro", ancho=720, x=540, y=1000, z=0.45, keys=late(0.1, 2, 0.06, 0.4)), flecha(circ, 0.05, d * 0.8, LIMA, 8, z=0.5)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[rotulo(0.3, d - 0.03, "SE ADAPTÓ", tam=110, color="#141414", capsula="#7dff3ae6", y=560)], sfx=[(0.1, "brillo", -18)])


@v.plano(129, "¿y al quitárselo?: el tubo cae al suelo")
def _(d):
    return P(SALON, [mundo("bg_salon_1896"), IMG("tubo_lentes", ancho=600, x=540, z=0.5, keys=cae(0.0, min(0.9, d * 0.7), 700, 1350) + [{"t": 0, "rot": 0}, {"t": d, "rot": 25}])],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[amarillo(0.15, d - 0.05, "¿Y AL QUITÁRSELO?", y=560, tam=90, color="#ffffff")], sfx=[(0.5, "golpe", -12)])


@v.plano(132, "durante un rato: el salón derecho, pero torcido y mareado")
def _(d):
    return P(SALON, [mundo("bg_salon_1896", [{"t": 0, "rot": -8}, {"t": d * 0.5, "rot": 8}, {"t": d, "rot": -5}]), motas(18, "#ffe8b0"), IMG("tubo_lentes", ancho=420, x=540, y=1480, z=0.5, rot=25)],
             cam(1.05, 1.1, (540, 960), temblor=4), "corte", hud=[rotulo(0.1, d - 0.03, "UN RATO", tam=100, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "rumor", -20, {"dur": d})])


@v.plano(139, "el mundo de siempre: la casa del paisaje de cerca, derecha")
def _(d):
    return P(DIA, [mundo(), arbol_rev(760, 1000, 380, 0, 0.4, late(0.0, 1, 0.05, 0.4)), motas(19, "#ffffff")], cam(1.3, 1.4, (540, 1000)), "corte", sfx=[(0.05, "roce", -20)])


@v.plano(135, "lo raro era el mundo de siempre: el paisaje normal y el árbol que vuelve a girar")
def _(d):
    return P(DIA, [mundo(), IMG("arbol_verde", ancho=620, x=540, y=1000, z=0.5, keys=[{"t": 0, "rot": 0, "escala": 0.8}, {"t": d * 0.5, "rot": 0, "escala": 1.0}, {"t": d, "rot": 40, "ease": "entrada"}]), motas(20, "#ffffff")],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[rotulo(0.1, d - 0.03, "LO RARO", tam=110, color="#141414", capsula="#ffffffe6", y=560)], sfx=[(0.1, "brillo", -18)])


avisos = v.construir("2026-11-22-manana-03-imagen-al-reves", claves=["REVÉS", "CRISTALINO", "CEREBRO", "STRATTON", "OCHO", "ARRIBA", "ABAJO", "NORMAL"],
                     musica={"generar": "curiosidad", "semilla": 24, "db": -13}, bucle=0.35)
