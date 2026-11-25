"""03 · El olivo que conoció a Roma — método denso, estilo cartoon. Lote 2026-11-25-manana (Nico, con el agente).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
from comun_1125m import *  # noqa: E402,F401,F403
import ilus_1125m  # noqa: E402

SVG = ilus_1125m.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
DIA = ["#8ad0ff", "#b87a3a"]
TAR = ["#ff9a5a", "#8a5a2a"]
ROM = ["#ffb86a", "#b8884a"]


def hojas(sem=1, n=24): return polvo("#a8c494", n, (0, 500, 1080, 1700), sem)
def oli(x=540, y=1120, ancho=900, n="olivo", keys=None, z=0.5): return IMG(n, ancho=ancho, x=x, y=y, z=z, keys=keys or [])


@v.plano(0, "gancho: el olivo enorme entra desde abajo en el olivar")
def _(d):
    return P(DIA, [BG("bg_olivar"), oli(keys=arranque(540, 1120, d, "abajo", 380, 30)), hojas(2)],
             cam(1.0, 1.1, (540, 1050)), vineta=0.4, hud=[BANDA()], sfx=[(0.03, "whoosh", -20), (0.4, "golpe", -20)])


@v.plano(5, "tiene más de mil setecientos años: la cuenta corre")
def _(d):
    return P(DIA, [BG("bg_olivar"), oli(y=1180, ancho=820, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.06, "ease": "suave"}]), hojas(3)],
             cam(1.0, 1.06, (540, 1100)), "corte",
             hud=[BANDA(), contador(0.05, d - 0.03, 0, 1700, min(1.3, d * 0.6), " años", tam=120, color="#141414", capsula="#ffd23fe6", y=640)], sfx=[(0.05, "subida", -22, {"dur": min(1.3, d * 0.6)})])


@v.plano(11, "es un olivo: la rama con aceitunas se balancea")
def _(d):
    return P(DIA, [BG("bg_olivar"), IMG("aceitunas", ancho=900, x=540, y=1050, z=0.5, keys=[{"t": 0, "rot": -7, "y": 900}, {"t": 0.3, "y": 1050, "ease": "salida"}, {"t": d, "rot": 6, "ease": "suave"}])],
             cam(1.05, 1.12, (540, 1050)), "corte", hud=[BANDA()], sfx=[(0.05, "roce", -20)])


@v.plano(14, "y está en Ulldecona, en España: el mapa y el punto")
def _(d):
    return P(["#2a7ad0", "#0a2a66"], [BG("bg_bajo_agua"), IMG("mapa_iberia", ancho=940, x=540, y=1130, z=0.5, keys=aparece(0.0, 0.2)), senala(785, 1080, 0.3, d - 0.03, 90, "#ff3d3d")],
             cam(1.0, 1.25, (540, 1130), (700, 1100)), "corte", hud=[rotulo(0.3, d - 0.03, "ULLDECONA · ESPAÑA", tam=74, color="#ffffff", capsula="#c0392be6", y=640)], sfx=[(0.3, "ding", -18)])


@v.plano(20, "lo plantaron en el año trescientos catorce: el campesino romano y el arbolito")
def _(d):
    return P(ROM, [BG("bg_roma"), IMG("romano", ancho=380, x=300, y=1300, z=0.5, keys=va((220, 1300), (310, 1300), d)),
                   IMG("olivo_joven", ancho=360, x=740, y=1380, z=0.55, keys=cae(0.15, 0.6, 900, 1380))],
             cam(1.0, 1.06, (540, 1200)), "desenfoque",
             hud=[BANDA(), contador(0.1, d - 0.03, 300, 314, min(0.9, d * 0.5), "", miles=False, tam=150, color="#141414", capsula="#ffffffe6", y=660, contar_prefijo="AÑO ")], sfx=[(0.5, "golpe", -18)])


@v.plano(27, "cuando mandaba el emperador Constantino: la moneda con el perfil y el laurel gira")
def _(d):
    return P(ROM, [BG("bg_roma"), brillo(540, 1100, 520, "#ffd23f", 0.4, 0.06, pulso=[0.2, 0.6]),
                   IMG("moneda_laurel", ancho=620, x=540, y=1100, z=0.5, keys=[{"t": 0, "ex": 0.1, "y": 800}, {"t": 0.45, "ex": 1.0, "y": 1100, "ease": "bote"}, {"t": d, "escala": 1.05, "ease": "suave"}])],
             cam(1.0, 1.08, (540, 1100)), "corte", hud=[BANDA(), rotulo(0.45, d - 0.03, "CONSTANTINO", tam=96, color="#141414", capsula="#ffd23fe6", y=640)], sfx=[(0.4, "ding", -16)])


@v.plano(32, "cuando Colón llegó a América: la carabela cruza el mar")
def _(d):
    return P(DIA, [BG("bg_cielo_dia"), IMG("carabela", ancho=760, x=540, y=1200, z=0.5, keys=[{"t": 0, "x": 200, "y": 1210, "rot": -3}, {"t": d * 0.5, "y": 1190, "rot": 3, "ease": "suave"}, {"t": d, "x": 760, "y": 1210, "rot": -2, "ease": "suave"}]),
                   {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 500, "relleno": "#1a6ab8", "x": 540, "y": 1760, "z": 0.6}],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[BANDA(), rotulo(0.3, d - 0.03, "1492", tam=150, color="#ffffff", capsula="#2a5ae8e6", y=660)], sfx=[(0.05, "ola", -18)])


@v.plano(37, "este olivo ya llevaba casi mil doscientos años ahí: el olivo al atardecer y la cuenta")
def _(d):
    return P(TAR, [BG("bg_olivar_tarde"), oli(y=1180, ancho=840, keys=late(0.3, 1, 0.03)), hojas(5)],
             cam(1.0, 1.06, (540, 1100)), "corte",
             hud=[BANDA(), contador(0.2, d - 0.03, 0, 1178, min(1.4, d * 0.5), " años", tam=110, color="#141414", capsula="#ffd23fe6", y=640)], sfx=[(0.2, "subida", -22, {"dur": min(1.4, d * 0.5)})])


@v.plano(46, "¿cómo lo saben?: micro plano, la lupa sobre el tronco")
def _(d):
    return P(DIA, [BG("bg_olivar"), oli(y=1000, ancho=1300), IMG("lupa", ancho=460, x=540, y=1250, z=0.7, keys=[{"t": 0, "x": 300, "y": 1350}, {"t": d, "x": 640, "y": 1200, "ease": "suave"}])],
             cam(1.1, 1.25, (540, 1250)), "corte", hud=[BANDA()], sfx=[(0.03, "pop", -20)])


@v.plano(49, "no pudieron contar sus anillos: los anillos, tachados")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("tronco_anillos", ancho=760, x=540, y=1130, z=0.5, keys=aparece(0.0, 0.2)), *tacha(540, 1110, d * 0.5, 280)],
             cam(1.0, 1.08, (540, 1100)), "corte", hud=[rotulo(0.1, d - 0.03, "¿ANILLOS?", tam=110, color="#141414", capsula="#ffd27ae6", y=620)], sfx=[(d * 0.5, "zap", -16)])


@v.plano(54, "los olivos viejos se quedan huecos por dentro: el centro del tronco desaparece")
def _(d):
    return P(OSC, [BG("bg_estudio"), *cruza(IMG("tronco_anillos", ancho=760, x=540, y=1130, z=0.5), IMG("tronco_hueco", ancho=760, x=540, y=1130, z=0.5), d * 0.35, 0.4),
                   polvo("#c89a5a", 30, (300, 900, 780, 1400), 4)],
             cam(1.0, 1.3, (540, 1110)), "corte", hud=[rotulo(d * 0.45, d - 0.03, "HUECO", tam=140, color="#ffffff", capsula="#c0392be6", y=620)], sfx=[(d * 0.35, "rumor", -18, {"dur": 0.6})])


@v.plano(62, "así que la Universidad Politécnica de Madrid: los investigadores llegan al árbol hueco")
def _(d):
    return P(DIA, [BG("bg_olivar"), oli(x=640, y=1100, ancho=800, n="olivo_hueco"), IMG("mu_c", ancho=210, x=200, y=1420, z=0.6, keys=va((60, 1420), (220, 1420), d, "salida")),
                   IMG("mu_b", ancho=200, x=90, y=1440, z=0.62, keys=va((-80, 1440), (80, 1440), d, "salida"))],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[BANDA(), rotulo(0.3, d - 0.03, "POLITÉCNICA DE MADRID", tam=68, color="#ffffff", capsula="#2a5ae8e6", y=640)], sfx=[(0.1, "roce", -22)])


@v.plano(69, "midió su tronco: la cinta métrica se despliega sobre el tronco")
def _(d):
    return P(DIA, [BG("bg_olivar"), oli(y=900, ancho=1400), IMG("cinta_metrica", ancho=1000, x=540, y=1300, z=0.7, keys=[{"t": 0, "x": -500}, {"t": d * 0.8, "x": 540, "ease": "salida"}])],
             cam(1.0, 1.06, (540, 1250)), "corte", hud=[BANDA()], sfx=[(0.03, "trazo", -18), (d * 0.4, "trazo", -18)])


@v.plano(72, "y calculó cuánto engorda cada año: el tronco crece, flechas hacia fuera")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("tronco_hueco", ancho=620, x=540, y=1130, z=0.5, keys=[{"t": 0, "escala": 0.8}, {"t": d, "escala": 1.12, "ease": "suave"}]),
                   flecha([[300, 1130], [110, 1130]], 0.2, 0.8, LIMA, 10, z=0.6), flecha([[780, 1130], [970, 1130]], 0.2, 0.8, LIMA, 10, z=0.6),
                   flecha([[540, 880], [540, 720]], 0.4, 1.0, LIMA, 10, z=0.6)],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[rotulo(0.3, d - 0.03, "CUÁNTO ENGORDA", tam=80, color="#141414", capsula="#7dff3ae6", y=1300)], sfx=[(0.2, "subida", -24, {"dur": 0.8})])


@v.plano(78, "y ese tronco mide ocho metros de contorno: el anillo rodea el tronco, la cifra")
def _(d):
    return P(DIA, [BG("bg_olivar"), oli(y=940, ancho=1300),
                   {"tipo": "forma", "forma": "elipse", "ancho": 760, "alto": 200, "relleno": "#ffffff", "op_relleno": 0, "grosor": 12, "borde": "#ff3d3d", "x": 540, "y": 1330, "z": 0.7,
                    "keys": [{"t": 0, "escala": 0.3, "op": 0}, {"t": 0.4, "escala": 1.0, "op": 1, "ease": "golpe"}, {"t": d, "escala": 1.03}]}],
             cam(1.0, 1.06, (540, 1200)), "corte",
             hud=[BANDA(), contador(0.2, d - 0.03, 0, 8, min(0.9, d * 0.4), " metros", tam=120, color="#ffffff", capsula="#c0392be6", y=660)], sfx=[(0.2, "ding", -18)])


@v.plano(86, "hacen falta cinco personas para abrazarlo: cinco figuras se colocan delante del tronco")
def _(d):
    ns = ["mu_a", "mu_b", "mu_c", "mu_d", "mu_a"]
    return P(DIA, [BG("bg_olivar"), oli(y=980, ancho=1150),
                   *[IMG(n, ancho=190, x=180 + i * 180, y=1440, z=0.6 + i * 0.01, keys=aparece(0.05 + i * d * 0.13, 0.2)) for i, n in enumerate(ns)]],
             cam(1.0, 1.06, (540, 1200)), "corte",
             hud=[BANDA(), contador(0.05, d - 0.03, 1, 5, d * 0.6, " personas", tam=100, color="#141414", capsula="#ffd23fe6", y=640)], sfx=[(0.05 + i * d * 0.13, "pop", -20) for i in range(5)])


@v.plano(92, "¿su truco para vivir tanto?: el olivo sobre fondo oscuro")
def _(d):
    return P(OSC, [BG("bg_estudio"), brillo(540, 1050, 560, "#7dff3a", 0.3, 0.06), oli(y=1150, ancho=760, keys=late(0.1, 1, 0.05))],
             cam(1.0, 1.08, (540, 1100)), "corte", hud=[amarillo(0.03, d - 0.03, "¿SU TRUCO?", y=640, tam=130, color=AMBAR)], sfx=[(0.03, "impacto", -18)])


@v.plano(97, "si el tronco muere: el árbol hueco se apaga")
def _(d):
    return P(OSC, [BG("bg_estudio"), oli(y=1150, ancho=760, n="olivo_hueco", keys=[{"t": 0, "op": 1}, {"t": d, "op": 0.35, "ease": "suave"}]),
                   brillo(540, 1250, 400, "#ff3d3d", 0.4, 0.06)],
             cam(1.0, 1.06, (540, 1150), temblor=2), "corte", sfx=[(0.05, "rumor", -18, {"dur": d})])


@v.plano(101, "vuelve a brotar desde la base: los brotes verdes salen del tocón")
def _(d):
    return P(OSC, [BG("bg_estudio"), brillo(540, 1150, 520, "#7dff3a", 0.5, 0.06, pulso=[0.2, 0.5]),
                   IMG("brote", ancho=760, x=540, y=1180, z=0.5, keys=[{"t": 0, "escala": 0.7, "y": 1280}, {"t": 0.45, "escala": 1.0, "y": 1180, "ease": "elastico"}, {"t": d, "escala": 1.05, "ease": "suave"}])],
             cam(1.0, 1.08, (540, 1150)), "corte", hud=[rotulo(0.3, d - 0.03, "VUELVE A BROTAR", tam=84, color="#141414", capsula="#7dff3ae6", y=620)], sfx=[(0.05, "brillo", -16)], energia=0.85)


@v.plano(107, "y no está solo: tres olivos en el olivar")
def _(d):
    return P(TAR, [BG("bg_olivar_tarde"), oli(x=540, y=1150, ancho=620), oli(x=160, y=1320, ancho=420, keys=aparece(0.1), z=0.55), oli(x=930, y=1330, ancho=420, keys=aparece(0.3), z=0.56), hojas(6)],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[BANDA()], sfx=[(0.1, "pop", -20), (0.3, "pop", -20)])


@v.plano(111, "en ese mismo pueblo hay más de mil trescientos olivos milenarios: los olivos llenan la pantalla")
def _(d):
    pos = [(180, 800), (540, 780), (900, 800), (360, 1020), (720, 1020), (180, 1250), (540, 1250), (900, 1250), (360, 1480), (720, 1480)]
    return P(TAR, [BG("bg_olivar_tarde"), *[oli(x=x, y=y, ancho=330, z=0.4 + y / 5000, keys=aparece(i * d * 0.05, 0.2)) for i, (x, y) in enumerate(pos)]],
             cam(1.0, 1.06, (540, 1100)), "corte",
             hud=[BANDA(), contador(0.2, d - 0.03, 0, 1300, d * 0.5, " olivos", tam=110, color="#141414", capsula="#ffd23fe6", y=640)], sfx=[(i * d * 0.12, "pop", -22) for i in range(4)])


@v.plano(122, "lo mejor: todavía da aceitunas: las aceitunas caen de la rama")
def _(d):
    return P(DIA, [BG("bg_olivar"), IMG("aceitunas", ancho=820, x=540, y=1000, z=0.5, keys=arranque(540, 1000, d, "arriba", 300, 20))],
             cam(1.0, 1.08, (540, 1050)), "corte", hud=[BANDA(), rotulo(0.3, d - 0.03, "TODAVÍA DA ACEITUNAS", tam=70, color="#ffffff", capsula="#3a6a2ae6", y=1300)], sfx=[(0.05, "roce", -20), (0.4, "pop", -20)])


@v.plano(127, "recién cogidas amargan muchísimo: primer plano de las aceitunas verdes, con el aviso")
def _(d):
    return P(OSC, [BG("bg_estudio"), brillo(540, 1100, 500, "#7dff3a", 0.3, 0.06), IMG("aceitunas", ancho=900, x=540, y=1050, z=0.5, keys=[{"t": 0, "rot": -3}, {"t": d * 0.5, "rot": 3, "ease": "suave"}, {"t": d, "rot": -2, "ease": "suave"}])],
             cam(1.2, 1.4, (540, 1150)), "corte", hud=[rotulo(0.3, d - 0.03, "AMARGAN", tam=130, color="#141414", capsula="#7dff3ae6", y=640)], sfx=[(0.3, "zap", -20)])


@v.plano(131, "no hay quien se las coma: las aceitunas, tachadas")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("aceitunas", ancho=760, x=540, y=1080, z=0.5), *tacha(540, 1130, 0.15, 260)],
             cam(1.0, 1.08, (540, 1100), temblor=3), "corte", sfx=[(0.15, "zap", -16)])


@v.plano(137, "pero con ellas se hace aceite cada año: las aceitunas negras y la botella que se llena de luz")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("aceitunas_negras", ancho=460, x=270, y=1100, z=0.5, keys=aparece(0.0, 0.2)),
                   flecha([[460, 1120], [640, 1120]], d * 0.25, d * 0.5, AMBAR, 12, z=0.6),
                   IMG("botella_aceite", ancho=300, x=810, y=1100, z=0.55, keys=cae(d * 0.3, d * 0.3 + 0.45, 500, 1100)),
                   brillo(810, 1150, 360, "#f4e04a", 0.5, 0.06, keys=[{"t": 0, "op": 0}, {"t": d * 0.5, "op": 0}, {"t": d * 0.6, "op": 1}])],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[rotulo(d * 0.5, d - 0.03, "ACEITE", tam=130, color="#141414", capsula="#f4e04ae6", y=640)], sfx=[(d * 0.3 + 0.4, "golpe", -18), (d * 0.6, "brillo", -18)])


@v.plano(145, "aceite de un árbol que plantó un romano: la botella, el olivo y el romano juntos")
def _(d):
    return P(TAR, [BG("bg_olivar_tarde"), oli(x=600, y=1080, ancho=780), IMG("romano", ancho=300, x=180, y=1380, z=0.6, keys=va((60, 1380), (190, 1380), d, "salida")),
                   IMG("botella_aceite", ancho=200, x=880, y=1400, z=0.62, keys=late(0.4, 2, 0.08, 0.5)), hojas(8)],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[BANDA()], sfx=[(0.4, "ding", -20)])


@v.plano(153, "¿lo probarías?: vuelve el olivo del principio (bucle)")
def _(d):
    return P(DIA, [BG("bg_olivar"), oli(keys=[{"t": 0, "escala": 0.96}, {"t": d, "escala": 1.04, "ease": "suave"}]), hojas(2),
                   IMG("botella_aceite", ancho=180, x=880, y=1420, z=0.6, keys=aparece(0.05, 0.2))],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[BANDA()], sfx=[(0.05, "pop", -20)])


v.construir("2026-11-25-manana-03-olivo-roma", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 253, "db": -13},
            claves=["Roma.", "años.", "olivo", "Ulldecona,", "catorce,", "Constantino.", "Colón", "América,", "anillos:", "huecos", "Politécnica",
                    "tronco", "ocho", "cinco", "truco", "brotar", "milenarios.", "aceitunas.", "amargan", "aceite", "romano."])
