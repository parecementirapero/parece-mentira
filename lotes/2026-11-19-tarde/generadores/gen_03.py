"""03 · Las gotas no son así (la forma real de una gota de lluvia) — método denso. Lote 2026-11-19-tarde (Agente 20:00, Jorge).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_1119t  # noqa: E402

SVG = ilus_1119t.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

GRIS = ["#3a4458", "#141a22"]
OSC = ["#0a1424", "#04080e"]
CIELO = ["#4a6a9a", "#a8c8e8"]
GX, GY = 540, 1150


def lluvia(sem=0, op=0.7, z=0.2):
    return IMG("lluvia_lineas", ancho=1080, x=540 + sem * 7, z=z, op=op, keys=[{"t": 0, "y": 900 - sem * 40, "ease": "lineal"}, {"t": 3, "y": 1500 - sem * 40}])


def gota(f="esfera", ancho=600, x=GX, y=GY, z=0.5, keys=None, **k):
    return IMG(f"gota_{f}", ancho=ancho, x=x, y=y, z=z, keys=keys or [], **k)


def aire_abajo(t0, d, n=4, y=1600, largo=260, color=AMBAR):
    return [flecha([[GX + dx, y], [GX + dx, y - largo]], t0 + i * 0.05, t0 + 0.45 + i * 0.05, color, 10, z=0.6) for i, dx in enumerate([-180, -60, 60, 180][:n])]


# ================================================================== PLANOS
@v.plano(0, "gancho: la gota con punta cae enorme y se le tacha encima un NO")
def _(d):
    return P(GRIS, [BG("bg_lluvia"), lluvia(0), gota("lagrima", 760, keys=arranque(GX, 1180, d, "arriba", 320, 30))],
             cam(1.0, 1.06, (540, 1150)), vineta=0.6, hud=[rotulo(0.35, d - 0.05, "NO", tam=170, color="#ffffff", capsula="#c0392be6", y=560)],
             sfx=[(0.02, "whoosh", -14, {"dur": 0.5}), (0.35, "golpe", -12)])


@v.plano(5, "no tienen punta de lágrima: el lápiz la dibuja y el anillo marca la punta")
def _(d):
    return P(["#f4efe4", "#d8d0c0"], [{"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#f4efe4", "x": 540, "y": 960, "z": 0.02},
             gota("lagrima", 560, y=1200), IMG("lapiz", ancho=520, z=0.6, keys=[{"t": 0, "x": 760, "y": 900, "rot": 120}, {"t": d * 0.7, "x": 640, "y": 1050, "rot": 130, "ease": "suave"}]),
             senala(GX, 940, 0.3, d - 0.1, 90, "#c0392b")],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[amarillo(0.2, d - 0.03, "SIN PUNTA", y=560, tam=120, color="#c0392b")], sfx=[(0.05, "trazo", -18), (0.3, "pop", -18)])


@v.plano(10, "¿entonces qué forma tienen? llueve sobre la ciudad")
def _(d):
    return P(GRIS, [BG("bg_lluvia"), lluvia(1), lluvia(2, 0.5, 0.4), IMG("nube_oscura", ancho=1100, x=540, y=380, z=0.3, anim={"flotar": [10, 0.3]})],
             cam(1.0, 1.05, (540, 1100)), "desenfoque", hud=[amarillo(0.05, d - 0.03, "¿QUÉ FORMA?", y=700, tam=120, color=CIAN)], sfx=[(0.05, "agua", -18, {"dur": 1.2})])


@v.plano(14, "una gota pequeña, de menos de dos milímetros: la regla y la gotita")
def _(d):
    return P(OSC, [brillo(540, 1150, 500, "#4ab0f0", 0.35, 0.06), IMG("regla", ancho=900, x=540, y=1450, z=0.4), gota(ancho=200, y=1250, keys=cae(0.0, 0.5, 700, 1250))],
             cam(1.0, 1.06, (540, 1300)), "corte", hud=[rotulo(0.3, d - 0.05, "< 2 MM", tam=130, color="#141414", capsula="#7ec8ffe6", y=560)], sfx=[(0.3, "agua", -18)])


@v.plano(22, "es una esfera casi perfecta: la esfera grande gira con su brillo")
def _(d):
    return P(OSC, [brillo(540, 1150, 600, "#4ab0f0", 0.4, 0.06), gota(ancho=720, keys=aparece(0.0, 0.4) + late(0.6, 1, 0.05, 0.5)), polvo("#c8ecff", 30, (0, 400, 1080, 1800), 4)],
             cam(1.0, 1.06), "corte", hud=[amarillo(0.2, d - 0.03, "ESFERA", y=560, tam=140, color=CIAN)], sfx=[(0.05, "pop", -16)])


@v.plano(27, "la tensión del agua la cierra como una piel: flechas que aprietan hacia dentro")
def _(d):
    fl = [flecha([[GX + dx * 2.2, GY + dy * 2.2], [GX + dx * 1.45, GY + dy * 1.45]], 0.1 + i * 0.08, 0.55 + i * 0.08, CIAN, 10, z=0.6)
          for i, (dx, dy) in enumerate([(0, -200), (200, 0), (0, 200), (-200, 0), (140, -140), (140, 140), (-140, 140), (-140, -140)])]
    return P(OSC, [brillo(540, 1150, 500, "#4ab0f0", 0.4, 0.06), gota(ancho=560, keys=late(0.4, 2, 0.04, 0.4)), *fl],
             cam(1.0, 1.05), "corte", hud=[rotulo(0.3, d - 0.05, "PIEL DE AGUA", tam=100, color="#141414", capsula="#7ec8ffe6", y=560)], sfx=[(0.1, "zap", -22)])


@v.plano(36, "pero al caer, el aire la empuja desde abajo: la gota cae y el aire sube")
def _(d):
    return P(GRIS, [BG("bg_lluvia", z=0.03) | {"op": 0.5}, lluvia(3, 0.8, 0.15), gota(ancho=460, y=1050, keys=[{"t": 0, "y": 1000}, {"t": d, "y": 1080}], anim={"flotar": [8, 0.2]}),
             *aire_abajo(0.15, d, 4, 1650, 330)],
             cam(1.0, 1.05, (540, 1200)), "corte", hud=[amarillo(0.3, d - 0.03, "AIRE", y=1780, tam=120, color=AMBAR)], sfx=[(0.1, "whoosh", -18, {"dur": 0.8})])


@v.plano(45, "cuanto más grande es la gota: la esfera crece")
def _(d):
    return P(OSC, [brillo(540, 1150, 500, "#4ab0f0", 0.35, 0.06), gota(ancho=400, keys=[{"t": 0, "escala": 0.7}, {"t": d, "escala": 1.6, "ease": "suave"}])],
             cam(1.0, 1.04), "corte", sfx=[(0.1, "subida", -20, {"dur": 0.9})])


@v.plano(51, "más gana el aire: flechas más gordas, la gota se achata")
def _(d):
    return P(OSC, [gota(ancho=620, keys=[{"t": 0, "ey": 1.0, "ex": 1.0}, {"t": d, "ey": 0.8, "ex": 1.1, "ease": "suave"}]), *aire_abajo(0.05, d, 4, 1650, 300)],
             cam(1.0, 1.05, (540, 1250)), "corte", hud=[amarillo(0.1, d - 0.03, "GANA EL AIRE", y=560, tam=110, color=AMBAR)], sfx=[(0.05, "whoosh", -18, {"dur": 0.6})])


@v.plano(55, "se aplasta: la esfera se convierte en pan")
def _(d):
    return P(OSC, [gota(ancho=620, keys=[{"t": 0, "op": 1, "ey": 0.8, "ex": 1.1}, {"t": d * 0.6, "op": 0, "ey": 0.6, "ease": "suave"}]),
             gota("pan", 700, z=0.51, keys=[{"t": 0, "op": 0}, {"t": d * 0.6, "op": 1, "ease": "suave"}]), *aire_abajo(0.0, d, 4, 1600, 200)],
             cam(1.1, 1.15, (540, 1200)), "corte", sfx=[(d * 0.5, "golpe", -20)])


@v.plano(58, "y queda como un pan de hamburguesa: la gota y el pan lado a lado")
def _(d):
    return P(["#2a1a10", "#120a06"], [brillo(540, 1150, 600, "#ffb070", 0.3, 0.06), gota("pan", 520, x=300, y=1100), IMG("pan_hamburguesa", ancho=520, x=780, z=0.5, keys=cae(0.0, 0.55, 700, 1150)), flecha([[440, 1120], [620, 1120]], 0.2, 0.6, "#ffffffcc", 8, z=0.6)],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[amarillo(0.0, d - 0.02, "HAMBURGUESA", y=560, tam=100, color="#ffb070")], sfx=[(0.35, "golpe", -18)])


@v.plano(61, "micro: pan, el panecillo enorme gira", mas=0.03)
def _(d):
    return P(["#2a1a10", "#120a06"], [IMG("pan_hamburguesa", ancho=1000, x=540, y=1150, z=0.5, keys=[{"t": 0, "rot": -8, "escala": 0.9}, {"t": d, "rot": 4, "escala": 1.0, "ease": "salida"}])],
             cam(1.0, 1.06), "corte", sfx=[(0.02, "pop", -18)])


@v.plano(64, "¿y si sigue creciendo? el pan de agua se hincha")
def _(d):
    return P(OSC, [brillo(540, 1150, 500, "#4ab0f0", 0.35, 0.06), gota("pan", 520, keys=[{"t": 0, "escala": 0.8}, {"t": d, "escala": 1.3, "ease": "suave"}])],
             cam(1.0, 1.04), "corte", hud=[amarillo(0.05, d - 0.03, "¿Y SI CRECE?", y=560, tam=120, color=CIAN)], sfx=[(0.1, "subida", -20, {"dur": 0.8})])


@v.plano(68, "cerca de un centímetro: la regla y la gota grande")
def _(d):
    return P(OSC, [IMG("regla", ancho=1000, x=540, y=1500, z=0.4), gota("pan", 640, y=1180, keys=late(0.2, 1, 0.05, 0.5))],
             cam(1.0, 1.05, (540, 1300)), "corte", hud=[rotulo(0.15, d - 0.05, "≈ 1 CM", tam=130, color="#141414", capsula="#7ec8ffe6", y=560)], sfx=[(0.15, "pop", -18)])


@v.plano(72, "el aire la hunde por el centro: una flecha empuja el centro hacia arriba")
def _(d):
    return P(OSC, [gota("pan", 700, keys=[{"t": 0, "op": 1}, {"t": d * 0.7, "op": 0.3, "ease": "suave"}]),
             gota("paracaidas", 700, z=0.51, keys=[{"t": 0, "op": 0}, {"t": d * 0.7, "op": 1, "ease": "suave"}]),
             flecha([[GX, 1650], [GX, 1250]], 0.1, d * 0.6, AMBAR, 16, z=0.6)],
             cam(1.1, 1.15, (540, 1250)), "corte", hud=[amarillo(0.2, d - 0.03, "SE HUNDE", y=560, tam=120, color=AMBAR)], sfx=[(0.1, "whoosh", -18, {"dur": 0.6})])


@v.plano(79, "se infla como un paracaídas: el paracaídas rojo baja junto a la gota")
def _(d):
    return P(CIELO, [BG("bg_perfil_nube", z=0.03) | {"op": 0.6}, gota("paracaidas", 520, x=330, y=1150, anim={"flotar": [10, 0.4]}),
             IMG("paracaidas", ancho=560, x=790, z=0.5, keys=[{"t": 0, "y": 800}, {"t": d, "y": 1100, "ease": "suave"}], anim={"flotar": [14, 0.3]})],
             cam(1.0, 1.04, (540, 1100)), "corte", hud=[amarillo(0.15, d - 0.03, "PARACAÍDAS", y=560, tam=120, color="#c0392b")], sfx=[(0.1, "whoosh", -20, {"dur": 0.8})])


@v.plano(84, "con un aro de agua: el anillo marca el aro de abajo")
def _(d):
    return P(OSC, [brillo(540, 1150, 500, "#4ab0f0", 0.35, 0.06), gota("paracaidas", 760, keys=[{"t": 0, "rot": -3}, {"t": d, "rot": 3}]),
             senala(GX, GY + 140, 0.15, d - 0.1, 260, CIAN)],
             cam(1.2, 1.3, (540, 1250)), "corte", hud=[rotulo(0.2, d - 0.05, "ARO DE AGUA", tam=100, color="#141414", capsula="#7ec8ffe6", y=560)], sfx=[(0.15, "pop", -18)])


@v.plano(89, "y revienta en gotas pequeñas: fogonazo y gotitas que salen disparadas")
def _(d):
    return P(OSC, [gota("paracaidas", 760, keys=[{"t": 0, "op": 1, "escala": 1.0}, {"t": 0.15, "op": 0, "escala": 1.3}]),
             IMG("gotitas", ancho=900, x=540, y=1150, z=0.5, keys=[{"t": 0.1, "escala": 0.2, "op": 0}, {"t": 0.15, "op": 1}, {"t": 0.6, "escala": 1.15, "ease": "salida"}, {"t": d, "escala": 1.25}]),
             fundido_blanco([{"t": 0.08, "op": 0}, {"t": 0.14, "op": 0.6}, {"t": 0.4, "op": 0}], "#e0f4ff")],
             cam(1.0, 1.08, (540, 1150), temblor=3), "corte", hud=[amarillo(0.2, d - 0.03, "¡PLOF!", y=560, tam=150, color=CIAN)], sfx=[(0.1, "impacto", -12), (0.15, "agua", -16)])


@v.plano(94, "que vuelven a ser esferas: las gotitas flotan redondas")
def _(d):
    return P(OSC, [brillo(540, 1150, 500, "#4ab0f0", 0.35, 0.06), IMG("gotitas", ancho=1000, x=540, y=1150, z=0.5, anim={"flotar": [14, 0.4]}, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 8}]),
             senala(400, 1050, 0.2, d - 0.1, 80, CIAN)],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.2, d - 0.03, "ESFERAS", y=560, tam=130, color=CIAN)], sfx=[(0.2, "pop", -20)])


@v.plano(99, "es un pulso entre la piel del agua y el aire: flechas cian hacia dentro, ámbar desde abajo")
def _(d):
    fl = [flecha([[GX + dx * 2.2, GY + dy * 2.2], [GX + dx * 1.5, GY + dy * 1.5]], 0.1 + i * 0.06, 0.5 + i * 0.06, CIAN, 9, z=0.6)
          for i, (dx, dy) in enumerate([(0, -180), (180, 0), (-180, 0), (130, -130), (-130, -130)])]
    return P(OSC, [gota(ancho=520, keys=[{"t": 0, "ey": 1.0}, {"t": d * 0.5, "ey": 0.88, "ex": 1.08, "ease": "suave"}, {"t": d, "ey": 1.0, "ex": 1.0, "ease": "suave"}]), *fl, *aire_abajo(d * 0.3, d, 3, 1700, 260)],
             cam(1.0, 1.04), "corte", hud=[contexto(0.0, d - 0.02, "PIEL CONTRA AIRE")], sfx=[(0.1, "zap", -22), (d * 0.35, "whoosh", -20, {"dur": 0.5})])


@v.plano(110, "las más grandes caen a unos diez metros por segundo: la gota cae dejando estela")
def _(d):
    return P(GRIS, [BG("bg_lluvia"), lluvia(4, 0.9, 0.3), gota("pan", 360, x=540, z=0.5, keys=[{"t": 0, "y": 500}, {"t": d, "y": 1500, "ease": "lineal"}]),
             flecha([[540, 300], [540, 1300]], 0.0, d, "#c8ecffaa", 6, punta=False, z=0.45)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[contador(0.1, d - 0.03, 0, 10, d * 0.5, " M/S", y=560, tam=120, color="#ffd23f")], sfx=[(0.05, "whoosh", -16, {"dur": 0.8})])


@v.plano(120, "treinta y seis kilómetros por hora: el marcador sube a 36")
def _(d):
    return P(OSC, [brillo(540, 1250, 500, "#7df9ff", 0.25, 0.06), IMG("velocimetro", ancho=800, x=540, y=1100, z=0.5),
             IMG("aguja_vel", ancho=640, x=540, y=1300, z=0.55, keys=[{"t": 0, "rot": -180}, {"t": d * 0.6, "rot": -126, "ease": "salida"}, {"t": d, "rot": -124}])],
             cam(1.0, 1.05, (540, 1200)), "corte", hud=[rotulo(0.2, d - 0.05, "36 KM/H", tam=130, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "subida", -18, {"dur": 0.8})])


@v.plano(126, "desde una nube a cuatro mil metros: perfil con la montaña y la nube alta")
def _(d):
    return P(CIELO, [BG("bg_perfil_nube"), IMG("nube", ancho=700, x=540, y=860, z=0.4, keys=aparece(0.0, 0.4)),
             flecha([[880, 980], [880, 1700]], 0.2, d * 0.8, "#ffffffcc", 6, disc=[18, 12], z=0.5)],
             cam(1.0, 1.04, (540, 1100)), "corte", hud=[rotulo(0.3, d - 0.05, "4.000 M", tam=110, color="#141414", capsula="#ffffffe6", x=700, y=1350)], sfx=[(0.1, "pop", -20)])


@v.plano(133, "tardan al menos siete minutos en llegar: la gota baja por la línea, la cifra corre")
def _(d):
    return P(CIELO, [BG("bg_perfil_nube"), IMG("nube", ancho=700, x=540, y=860, z=0.4), flecha([[880, 980], [880, 1700]], 0.0, 0.01, "#ffffffcc", 6, disc=[18, 12], z=0.5),
             gota("pan", 130, x=880, z=0.6, keys=[{"t": 0, "y": 1010, "ease": "lineal"}, {"t": d, "y": 1650}])],
             cam(1.0, 1.04, (540, 1100)), "corte", hud=[contador(0.05, d - 0.03, 0, 7, d * 0.8, " MIN", y=560, tam=130, color="#ffd23f")], sfx=[(0.05, "tictac", -22, {"dur": 0.8, "ritmo": 0.12})])


@v.plano(140, "y en todo ese viaje, nunca tienen punta: la lágrima se tacha")
def _(d):
    return P(GRIS, [BG("bg_lluvia"), lluvia(5), gota("lagrima", 520, keys=[{"t": 0, "rot": -6}, {"t": d, "rot": 6, "ease": "suave"}]),
             flecha([[300, 900], [780, 1420]], d * 0.35, d * 0.6, "#ff3d3d", 22, punta=False, z=0.6), flecha([[780, 900], [300, 1420]], d * 0.45, d * 0.7, "#ff3d3d", 22, punta=False, z=0.6)],
             cam(1.0, 1.04, (540, 1150)), "corte", hud=[rotulo(0.2, d - 0.05, "NUNCA", tam=130, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(d * 0.4, "trazo", -16), (d * 0.5, "trazo", -16)])


@v.plano(148, "la próxima vez que llueva: el charco con ondas bajo la lluvia")
def _(d):
    return P(GRIS, [BG("bg_lluvia"), lluvia(6), IMG("ondas_charco", ancho=1100, x=540, y=1650, z=0.5, keys=[{"t": 0, "escala": 0.5, "op": 1}, {"t": d, "escala": 1.3, "op": 0.3}]),
             IMG("ondas_charco", ancho=600, x=300, y=1720, z=0.5, keys=[{"t": d * 0.3, "escala": 0.4, "op": 1}, {"t": d, "escala": 1.0, "op": 0.4}])],
             cam(1.0, 1.05, (540, 1300)), "desenfoque", sfx=[(0.1, "agua", -18, {"dur": 1.0})])


@v.plano(153, "piénsalo: te caen panecillos de agua: llueven panes de agua, uno grande cae al frente (bucle)")
def _(d):
    caen = [gota("pan", 160 + i * 30, x=x, z=0.3 + i * 0.05, keys=[{"t": 0, "y": y0, "ease": "lineal"}, {"t": d, "y": y0 + 900}]) for i, (x, y0) in enumerate([(200, 300), (820, 100), (420, -100), (700, 500)])]
    return P(GRIS, [BG("bg_lluvia"), lluvia(7, 0.5), *caen, gota("pan", 700, keys=[{"t": 0, "y": 1100, "escala": 1.0}, {"t": 0.45, "y": 1180, "ease": "elastico"}, {"t": d, "y": 1150, "escala": 1.04}])],
             cam(1.0, 1.04, (540, 1150)), "corte", hud=[rotulo(0.2, d - 0.45, "PANECILLOS", tam=110, color="#141414", capsula="#ffb070e6", y=560)], sfx=[(0.1, "agua", -16), (d * 0.6, "ding", -22)])


@v.plano(104, "micro: piel, el borde de la gota con flechas cian", mas=0.03)
def _(d):
    return P(OSC, [gota(ancho=1400, y=1500), flecha([[540, 300], [540, 700]], 0.0, d * 0.7, CIAN, 14, z=0.6)],
             cam(1.0, 1.06, (540, 1000)), "corte", sfx=[(0.02, "zap", -20)])


@v.plano(116, "micro: diez, la gota pasa como una bala", mas=0.03)
def _(d):
    return P(GRIS, [BG("bg_lluvia"), lluvia(8, 0.9, 0.5), gota("pan", 520, x=540, z=0.5, keys=[{"t": 0, "y": 200, "ease": "lineal"}, {"t": d, "y": 1900}]),
             *lineas_vel(540, 900, 3, "#c8ecffaa")],
             cam(1.0, 1.04, (540, 1000), temblor=2), "corte", sfx=[(0.0, "whoosh", -14, {"dur": 0.4})])


v.construir("2026-11-19-tarde-03-gotas-no-son-asi", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 47, "db": -13},
            claves=["gotas", "punta", "lágrima", "forma", "milímetros", "esfera", "tensión", "piel", "aire", "abajo", "aplasta", "pan", "hamburguesa",
                    "centímetro", "centro", "paracaídas", "aro", "revienta", "esferas", "diez", "treinta", "seis", "cuatro", "siete", "minutos", "nunca", "panecillos"])
