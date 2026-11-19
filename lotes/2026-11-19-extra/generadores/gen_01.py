"""01 · Este niño cambia el clima (El Niño) — método denso. Vídeo extra 2026-11-19, pedido por Nico en el chat a partir de las tendencias del día.
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_nino  # noqa: E402

SVG = ilus_nino.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

ESP = ["#02030a", "#0a1030"]
NOCHE = ["#040818", "#101c3a"]
MAPA = ["#06142e", "#05122a"]
FRIO = ["#0a3a5e", "#020e22"]
TIBIO = ["#5a2a20", "#1a1024"]
ARENA = ["#3a4a6a", "#2a1a10"]
ROJO = ["#3a0c08", "#7a2a14"]

ASIA_XY, AMERICA_XY, CENTRO = (300, 960), (780, 960), (540, 960)


def sat(d, a, b, p0=(1150, 420), p1=(-150, 700)):
    return IMG("satelite", ancho=140, z=0.25, keys=recorrido(v.w(a), v.w(b), p0, p1, d), anim={"girar": 5})


def nube_fondo(d, a, b, y=420, n="nube", ancho=620, op=0.9):
    """Nube que cruza despacio varios planos seguidos (detalle de fondo que dura)."""
    ks = recorrido(v.w(a), v.w(b), (-320, y), (1400, y + 40), d)
    for k in ks: k["op"] = k["op"] * op
    return IMG(n, ancho=ancho, z=0.2, keys=ks)


def mancha(n, ancho, keys, z=0.45, **k):
    return IMG(n, ancho=ancho, z=z, keys=keys, **k)


def rafagas(d, sentido=-1, y0=600, n=4, color="viento", frena=False, op=1.0):
    """Ráfagas de viento que cruzan el plano. sentido −1 = hacia la izquierda (hacia Asia)."""
    els = []
    for k in range(n):
        y = y0 + k * 210 + (k % 2) * 40
        xa, xb = (1250, -200) if sentido < 0 else (-200, 1250)
        t0 = k * 0.12
        if frena:
            ks = [{"t": 0, "x": xa, "y": y, "op": op, "ex": sentido}, {"t": d * 0.55, "x": (xa + xb) / 2 + sentido * -120, "op": op * 0.9, "ease": "salida"},
                  {"t": d, "x": (xa + xb) / 2 + sentido * -60, "op": 0.0, "ease": "suave"}]
        else:
            ks = [{"t": 0, "x": xa - sentido * k * 150, "y": y, "op": op, "ex": sentido, "ease": "lineal"}, {"t": max(d, 0.6) + t0, "x": xb, "op": op}]
        els.append(IMG(color, ancho=620 - k * 40, z=0.6, ex=sentido, keys=ks))
    return els


# ================================================================== PLANOS
@v.plano(0, "gancho: la Tierra sube hacia cámara con la franja caliente del Pacífico latiendo")
def _(d):
    return P(ESP, [BG("bg_esp_violeta"), IMG("tierra_nino", ancho=940, z=0.5, keys=arranque(540, 1080, d)),
             brillo(600, 1120, 300, "#ff7a1e", 0.75, 0.55, pulso=[0.35, 0.45]), sat(d, 0, 13),
             polvo("#ffd27a", 30, (150, 800, 930, 1400), 3, "chispas")],
             cam(1.0, 1.05, (540, 1080), (560, 1040)), vineta=0.6, sfx=[(0.02, "whoosh", -12, {"dur": 0.6}), (0.45, "impacto", -14)])


@v.plano(3, "micro: tormenta, el rayo cae de la nube", mas=0.05)
def _(d):
    return P(["#0a0c1e", "#1a1c38"], [BG("bg_tormenta"), IMG("nube_b", ancho=1300, x=540, y=560, z=0.4, keys=[{"t": 0, "x": 480}, {"t": d, "x": 600}]),
             IMG("rayo", ancho=520, x=560, y=1150, z=0.5, keys=[{"t": 0, "op": 0}, {"t": 0.08, "op": 1}, {"t": 0.22, "op": 0.3}, {"t": 0.3, "op": 1}, {"t": d, "op": 0.6}]),
             fundido_blanco([{"t": 0.06, "op": 0}, {"t": 0.1, "op": 0.5}, {"t": 0.3, "op": 0}], "#dfe8ff")],
             cam(1.0, 1.08, temblor=3), "corte", sfx=[(0.06, "zap", -14), (0.15, "rumor", -18, {"dur": 0.7})])


@v.plano(5, "su nombre viene de Navidad: la estrella baja sobre el mar de noche")
def _(d):
    return P(NOCHE, [BG("bg_esp_petroleo"), estrellas(50, 5),
             IMG("estrella_navidad", ancho=620, z=0.5, keys=[{"t": 0, "x": 540, "y": 560, "escala": 0.5, "op": 0.4}, {"t": 0.45, "y": 820, "escala": 1.0, "op": 1, "ease": "rebote"}, {"t": d, "y": 860, "escala": 1.06}]),
             brillo(540, 720, 420, "#ffe08a", 0.5, 0.3, pulso=[0.2, 0.7]), sat(d, 0, 13)],
             cam(1.0, 1.06, (540, 860)), "corte", hud=[amarillo(0.25, d - 0.03, "NAVIDAD", y=1210, tam=124, color=AMBAR)], sfx=[(0.1, "brillo", -16), (0.5, "ding", -22)])


@v.plano(11, "micro: ¿por qué? la Tierra pequeña late", mas=0.05)
def _(d):
    return P(["#1a0a24", "#3a1a48"], [brillo(540, 1050, 520, "#ff3df2", 0.35, 0.1), IMG("tierra_nino", ancho=520, x=540, y=1100, z=0.5, keys=late(0.0, 2, 0.1, 0.3), anim={"girar": -6})],
             cam(1.0, 1.1), "corte", hud=[amarillo(0.0, d - 0.03, "¿POR QUÉ?", y=560, tam=130, color=MAGENTA)], sfx=[(0.02, "pop", -18)])


@v.plano(13, "hace más de cien años, los pescadores del norte de Perú: la barca se acerca desde lejos hasta llenar el plano")
def _(d):
    return P(FRIO, [BG("bg_mar_frio"), nube_fondo(d, 13, 27, 660, "nube", 400, 0.45),
             IMG("barca", ancho=900, z=0.5, keys=[{"t": 0, "x": 260, "y": 1050, "escala": 0.36, "ease": "suave"}, {"t": d * 0.55, "x": 500, "y": 1160, "escala": 0.8}, {"t": d, "x": 540, "y": 1200, "escala": 1.0}],
                 anim={"balanceo": [2.5, 2.4], "flotar": [8, 2.0]}),
             polvo("#d8f4ff", 30, (0, 1000, 1080, 1850), 7)],
             cam(1.04, 1.0, (520, 1050), (540, 1150)), "desenfoque",
             hud=[contexto(0.05, d * 0.5, "HACE +100 AÑOS"), contexto(d * 0.5 + 0.2, d - 0.05, "NORTE DE PERÚ")], sfx=[(0.05, "agua", -22, {"dur": 1.3}), (d * 0.6, "agua", -20, {"dur": 1.2})])


@v.plano(23, "micro: el anillo marca el norte de Perú en el mapa", mas=0.05)
def _(d):
    return P(MAPA, [BG("bg_pacifico"), senala(935, 1020, 0.0, d - 0.05, 120, AMBAR), brillo(935, 1020, 200, "#ffd23f", 0.5, 0.3, pulso=[0.3, 0.25])],
             cam(1.5, 1.6, (860, 1010)), "corte", sfx=[(0.02, "pop", -16)])


@v.plano(24, "notaron algo raro: el termómetro en el agua empieza a subir y el mar cambia de color")
def _(d):
    return P(FRIO, [BG("bg_mar_frio"), IMG("bg_mar_tibio", ancho=1180, x=540, y=960, z=0.06, keys=[{"t": 0, "op": 0}, {"t": d, "op": 0.5, "ease": "suave"}]),
             IMG("termo_frio", ancho=300, x=540, z=0.5, keys=[{"t": 0, "y": 1320, "rot": -8}, {"t": d, "y": 1220, "rot": 6, "ease": "suave"}], anim={"flotar": [12, 1.4]}),
             senala(540, 1560, 0.15, d - 0.1, 120, AMBAR), polvo("#d8f4ff", 30, (0, 1000, 1080, 1850), 33)],
             cam(1.0, 1.08, (540, 1250)), "corte", hud=[rotulo(0.1, d - 0.05, "ALGO RARO", tam=92, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "ding", -20), (0.4, "burbuja", -20)])


@v.plano(27, "cada diciembre: cae la hoja del calendario", mas=0.05)
def _(d):
    return P(FRIO, [BG("bg_mar_frio"), IMG("hoja_dic", ancho=600, x=540, z=0.5, keys=cae(0.0, 0.42, 500, 1050)),
             polvo("#ffffff", 30, (0, 300, 1080, 1700), 11)],
             cam(1.0, 1.05), "corte", sfx=[(0.3, "golpe", -18)])


@v.plano(29, "el mar frío donde pescaban: bajo el agua azul, el banco de peces nada")
def _(d):
    return P(FRIO, [BG("bg_sub_frio"), IMG("banco_b", ancho=700, z=0.3, keys=[{"t": 0, "x": 900, "y": 620, "ease": "lineal"}, {"t": d, "x": 640, "y": 600}], op=0.6),
             IMG("banco", ancho=1000, z=0.5, keys=[{"t": 0, "x": 760, "y": 1150, "ease": "lineal"}, {"t": d, "x": 420, "y": 1120}], anim={"flotar": [10, 1.3]}),
             IMG("termo_frio", ancho=170, x=930, y=1250, z=0.6, keys=aparece(0.15, 0.35)), polvo("#d8f4ff", 40, (0, 300, 1080, 1800), 13)],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "FRÍO", y=560, tam=130, color=CIAN)], sfx=[(0.05, "burbuja", -20), (0.4, "burbuja", -22), (0.9, "burbuja", -22)])


@v.plano(34, "se volvía tibio: el agua cambia de color y el termómetro sube")
def _(d):
    return P(TIBIO, [BG("bg_sub_frio"), IMG("bg_sub_tibio", ancho=1180, x=540, y=960, z=0.06, keys=[{"t": 0, "op": 0}, {"t": d * 0.6, "op": 1, "ease": "suave"}]),
             IMG("banco", ancho=900, z=0.5, keys=[{"t": 0, "x": 460, "y": 1150, "ease": "lineal"}, {"t": d, "x": 300, "y": 1200}]),
             IMG("termo_frio", ancho=230, x=860, y=1150, z=0.6, keys=[{"t": 0, "op": 1}, {"t": d * 0.5, "op": 0}]),
             IMG("termo_tibio", ancho=230, x=860, y=1150, z=0.61, keys=[{"t": 0, "op": 0, "escala": 1.0}, {"t": d * 0.5, "op": 1}, {"t": d * 0.65, "escala": 1.12, "ease": "rebote"}, {"t": d, "escala": 1.0}]),
             brillo(540, 700, 600, "#ff7a1e", 0.3, 0.08, keys=[{"t": 0, "op": 0}, {"t": d, "op": 1}])],
             cam(1.0, 1.06), "corte", hud=[rotulo(d * 0.35, d - 0.05, "TIBIO", tam=110, color="#141414", capsula="#ffb02ee6", y=560)], sfx=[(0.1, "subida", -20, {"dur": 0.8})])


@v.plano(39, "micro: un pez se va a toda velocidad", mas=0.05)
def _(d):
    return P(TIBIO, [BG("bg_sub_tibio"), IMG("pez", ancho=820, z=0.5, ex=-1, keys=[{"t": 0, "x": 480, "y": 1050, "ex": -1, "rot": 0}, {"t": d, "x": 1500, "y": 1300, "ex": -1, "rot": 14, "ease": "entrada"}]),
             *lineas_vel(700, 1080, 3), polvo("#fff1c8", 30, (0, 600, 1080, 1500), 15)],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "whoosh", -16, {"dur": 0.5})])


@v.plano(40, "desaparecían: la barca con la red vacía sobre el mar tibio")
def _(d):
    return P(TIBIO, [BG("bg_mar_tibio"), IMG("barca_vacia", ancho=880, x=540, z=0.5, keys=[{"t": 0, "y": 1200, "escala": 1.02}, {"t": d, "y": 1215, "escala": 0.98, "ease": "suave"}], anim={"balanceo": [2, 2.6]}),
             senala(545, 1300, 0.25, d - 0.1, 120, MAGENTA), polvo("#ffe8c0", 24, (0, 1300, 1080, 1850), 17)],
             cam(1.0, 1.06, (540, 1200)), "corte", hud=[rotulo(0.08, d - 0.05, "RED VACÍA", tam=92, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.1, "agua", -22, {"dur": 1.0})])


@v.plano(41, "como pasaba cerca de Navidad: noche en el mar, la estrella sobre la barca")
def _(d):
    return P(NOCHE, [BG("bg_mar_frio"),
             {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#040a20", "x": 540, "y": 960, "z": 0.1, "keys": [{"t": 0, "op": 0.72}, {"t": d, "op": 0.72}]},
             estrellas(40, 9),
             IMG("estrella_navidad", ancho=420, x=700, z=0.4, keys=[{"t": 0, "y": 640}, {"t": d, "y": 600, "ease": "suave"}], anim={"pulso": [0.05, 0.9]}),
             IMG("barca", ancho=520, z=0.5, keys=[{"t": 0, "x": 330, "y": 1240, "ease": "lineal"}, {"t": d, "x": 420, "y": 1250}], anim={"balanceo": [3, 2.2]})],
             cam(1.0, 1.05, (540, 1000)), "desenfoque", hud=[contexto(0.05, d - 0.05, "CERCA DE NAVIDAD")], sfx=[(0.1, "brillo", -20)])


@v.plano(46, "lo llamaron la corriente del Niño: la corriente tibia baja pegada a la costa")
def _(d):
    return P(MAPA, [BG("bg_pacifico"), mancha("mancha_caliente", 460, [{"t": 0, "x": 800, "y": 900, "rot": 60, "escala": 0.8}, {"t": d, "x": 850, "y": 1150, "rot": 72, "escala": 1.05, "ease": "suave"}]),
             flecha([[760, 800], [800, 930], [840, 1060], [900, 1200]], 0.1, d * 0.6, AMBAR, 10, z=0.6)],
             cam(1.2, 1.3, (840, 1000), (860, 1080)), "corte",
             hud=[rotulo(0.3, d - 0.05, "CORRIENTE DEL NIÑO", tam=74, color="#141414", capsula="#ffd23fe6", y=540)], sfx=[(0.1, "agua", -20, {"dur": 1.2})])


@v.plano(52, "por el Niño Jesús: el pesebre con su luz")
def _(d):
    return P(["#1a1008", "#3a2410"], [brillo(540, 1000, 620, "#ffd27a", 0.55, 0.1, pulso=[0.12, 0.8]),
             IMG("estrella_navidad", ancho=300, x=540, y=560, z=0.3, anim={"pulso": [0.06, 0.7]}),
             IMG("pesebre", ancho=860, x=540, z=0.5, keys=[{"t": 0, "y": 1250, "escala": 0.9}, {"t": 0.35, "escala": 1.0, "ease": "rebote"}, {"t": d, "y": 1230, "escala": 1.04}]),
             polvo("#fff4c0", 50, (150, 500, 930, 1500), 19, "chispas")],
             cam(1.0, 1.06, (540, 1150)), "corte", sfx=[(0.1, "ding", -18), (0.4, "brillo", -20)])


@v.plano(56, "¿y qué ocurre en realidad? la lupa recorre el Pacífico")
def _(d):
    return P(ESP, [BG("bg_esp_violeta"), IMG("tierra_pacifico", ancho=900, x=540, y=1080, z=0.45, anim={"girar": 2}),
             IMG("lupa", ancho=420, z=0.6, keys=[{"t": 0, "x": 300, "y": 1300}, {"t": d, "x": 700, "y": 980, "ease": "suave"}]), sat(d, 56, 72, (-150, 480), (1200, 620))],
             cam(1.0, 1.06, (540, 1050)), "desenfoque", hud=[amarillo(0.05, d - 0.03, "¿QUÉ OCURRE?", y=520, tam=104, color=CIAN)], sfx=[(0.1, "roce", -20)])


@v.plano(61, "normalmente, el viento empuja: el mapa del Pacífico y las ráfagas hacia la izquierda")
def _(d):
    return P(MAPA, [BG("bg_pacifico"), mancha("mancha_caliente", 640, [{"t": 0, "x": 540, "y": 960, "escala": 0.9}, {"t": d * 0.5, "x": 520, "escala": 1.0}, {"t": d, "x": 440, "ease": "suave"}], anim={"pulso": [0.04, 0.9]}),
             *[{**e, "keys": [{**k, "t": round(k["t"] + d * 0.45, 3)} for k in e["keys"]]} for e in rafagas(d * 0.55, -1, 560, 4)]],
             cam(1.0, 1.04), "corte", hud=[contexto(0.05, d * 0.45, "NORMAL"), rotulo(d * 0.5, d - 0.05, "VIENTO", tam=100, color="#141414", capsula="#7df9ffe6", y=1230)],
             sfx=[(0.05, "pop", -20), (d * 0.45, "whoosh", -14, {"dur": 0.8})])


@v.plano(65, "el agua caliente del Pacífico: la mancha se desliza hacia Asia")
def _(d):
    return P(MAPA, [BG("bg_pacifico"), mancha("mancha_caliente", 640, [{"t": 0, "x": 440, "y": 960, "ease": "lineal"}, {"t": d, "x": 330}]),
             *rafagas(d, -1, 620, 3, op=0.7),
             flecha([[820, 1250], [600, 1250], [380, 1250]], 0.05, d * 0.7, CIAN, 10, z=0.6)],
             cam(1.0, 1.04, (540, 960), (480, 960)), "corte", hud=[rotulo(0.08, d - 0.05, "AGUA CALIENTE", tam=84, color="#ffffff", capsula="#c0392be6", y=520)], sfx=[(0.1, "agua", -22, {"dur": 1.2})])


@v.plano(71, "hacia Asia: la mancha se apila junto a Asia y Australia", mas=0.05)
def _(d):
    return P(MAPA, [BG("bg_pacifico"), mancha("mancha_caliente", 620, [{"t": 0, "x": 330, "y": 960, "escala": 1.0}, {"t": d, "x": 300, "escala": 1.12, "ease": "salida"}]),
             senala(150, 520, 0.05, d - 0.05, 150, AMBAR)],
             cam(1.25, 1.35, (300, 900)), "corte", sfx=[(0.02, "golpe", -18)])


@v.plano(72, "pero algunos años: la boya que mide el mar se balancea")
def _(d):
    return P(TIBIO, [BG("bg_mar_tibio"), IMG("boya", ancho=440, x=540, z=0.5, keys=[{"t": 0, "y": 1250}, {"t": d, "y": 1220, "ease": "suave"}], anim={"balanceo": [7, 1.6], "flotar": [14, 1.4]}),
             {"tipo": "forma", "forma": "elipse", "ancho": 220, "alto": 220, "relleno": "#ffffff", "op_relleno": 0, "grosor": 6, "borde": "#ff5a5a", "x": 540, "y": 915, "z": 0.6,
              "keys": [{"t": 0, "escala": 0.3, "op": 1}, {"t": d, "escala": 1.8, "op": 0, "ease": "salida"}]},
             polvo("#ffe8c0", 24, (0, 1300, 1080, 1850), 21)],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[contexto(0.05, d - 0.05, "ALGUNOS AÑOS")], sfx=[(0.1, "senal", -20)])


@v.plano(75, "ese viento: las ráfagas todavía cruzan")
def _(d):
    return P(MAPA, [BG("bg_pacifico"), mancha("mancha_caliente", 620, [{"t": 0, "x": 300, "y": 960}, {"t": d, "x": 310}], anim={"pulso": [0.05, 0.6]}),
             *rafagas(d, -1, 560, 4)],
             cam(1.0, 1.04), "corte", sfx=[(0.02, "whoosh", -18, {"dur": 0.8})])


@v.plano(78, "micro: se frena, las ráfagas se quedan clavadas y se apagan", mas=0.05)
def _(d):
    return P(["#1a0a24", "#0a1030"], [BG("bg_pacifico"), *rafagas(d, -1, 700, 3, frena=True)],
             cam(1.3, 1.25, (540, 960)), "corte", hud=[rotulo(0.0, d - 0.03, "FRENA", tam=120, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.02, "golpe", -14)])


@v.plano(79, "y el agua caliente: la mancha late y arranca", mas=0.05)
def _(d):
    return P(MAPA, [BG("bg_pacifico"), mancha("mancha_caliente", 640, [{"t": 0, "x": 310, "y": 960, "escala": 1.0}, {"t": d * 0.5, "escala": 1.15, "ease": "rebote"}, {"t": d, "x": 380, "escala": 1.05}]),
             brillo(320, 960, 380, "#ff7a1e", 0.5, 0.3, pulso=[0.3, 0.3])],
             cam(1.3, 1.2, (330, 960), (400, 960)), "corte", sfx=[(0.02, "subida", -18, {"dur": 0.7})])


@v.plano(83, "vuelve hacia América: la mancha cruza el océano hasta Perú, con su estela")
def _(d):
    mk = [{"t": 0, "x": 380, "y": 960, "escala": 1.0, "ease": "suave"}, {"t": d * 0.85, "x": 760, "escala": 1.1}, {"t": d, "x": 770, "escala": 1.14}]
    return P(MAPA, [BG("bg_pacifico"), flecha([[230, 960], [480, 960], [700, 960]], 0.0, d * 0.75, AMBAR, 14, z=0.4),
             mancha("mancha_caliente", 640, mk), mancha("mancha_caliente", 420, sigue(mk, 0.18), z=0.42, op=0.5),
             senala(940, 1010, d * 0.7, d - 0.05, 120, AMBAR)],
             cam(1.0, 1.06, (500, 960), (640, 960)), "corte",
             hud=[rotulo(0.1, d - 0.05, "HACIA AMÉRICA", tam=88, color="#141414", capsula="#ffd23fe6", y=520)], sfx=[(0.05, "agua", -18, {"dur": 1.3}), (d * 0.8, "impacto", -16)])


@v.plano(86, "con ella cambian las lluvias: sobre la Tierra, las nubes se van con el agua caliente")
def _(d):
    return P(ESP, [BG("bg_esp_violeta"), IMG("tierra_nino", ancho=900, x=540, y=1100, z=0.4, anim={"girar": 1.5}),
             IMG("nube", ancho=460, z=0.55, keys=[{"t": 0, "x": 260, "y": 1000, "ease": "suave"}, {"t": d, "x": 760, "y": 1080}]),
             IMG("nube_b", ancho=360, z=0.56, keys=[{"t": 0, "x": 200, "y": 1230, "ease": "suave"}, {"t": d, "x": 640, "y": 1260}]),
             flecha([[300, 860], [540, 820], [780, 880]], 0.1, d * 0.7, CIAN, 8, z=0.6), sat(d, 86, 94, (1150, 460), (-150, 600))],
             cam(1.0, 1.1, (540, 1050)), "desenfoque", hud=[amarillo(0.1, d * 0.55, "LLUVIAS", y=520, tam=120, color=CIAN), amarillo(d * 0.6, d - 0.03, "MEDIO MUNDO", y=520, tam=100, color=LIMA)], sfx=[(0.1, "rumor", -22, {"dur": 1.2})])


@v.plano(94, "diluvios en los desiertos de Perú: llega la nube, llueve sobre las dunas y sube el agua")
def _(d):
    return P(ARENA, [BG("bg_desierto"), IMG("nube_b", ancho=1300, z=0.4, keys=[{"t": 0, "x": -200, "y": 520}, {"t": d * 0.4, "x": 520, "ease": "salida"}, {"t": d, "x": 600}]),
             IMG("lluvia", ancho=1080, x=540, z=0.6, keys=[{"t": 0.25, "y": 300, "op": 0, "ease": "lineal"}, {"t": 0.45, "op": 1}, {"t": d, "y": 1400, "op": 1}]),
             IMG("riada", ancho=1300, x=540, z=0.7, keys=[{"t": 0.3, "y": 2500}, {"t": d, "y": 1960, "ease": "suave"}]),
             fundido_blanco([{"t": d * 0.55, "op": 0}, {"t": d * 0.58, "op": 0.35}, {"t": d * 0.7, "op": 0}], "#dfe8ff")],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[rotulo(0.1, d - 0.05, "PERÚ · DILUVIOS", tam=84, color="#ffffff", capsula="#1a4a8ae6", y=1220)],
             sfx=[(0.25, "agua", -16, {"dur": 1.6}), (d * 0.55, "rumor", -18, {"dur": 0.8})])


@v.plano(99, "micro: el agua marrón sube de golpe", mas=0.05)
def _(d):
    return P(["#2a2a3a", "#3a2a1c"], [BG("bg_tormenta"), IMG("lluvia", ancho=1080, x=540, z=0.6, keys=[{"t": 0, "y": 500, "ease": "lineal"}, {"t": d, "y": 1100}]),
             IMG("riada", ancho=1400, x=540, z=0.7, keys=[{"t": 0, "y": 1900}, {"t": d, "y": 1450, "ease": "salida"}])],
             cam(1.0, 1.1, temblor=3), "corte", sfx=[(0.02, "agua", -13, {"dur": 0.6})])


@v.plano(100, "y sequía: el suelo agrietado bajo el sol", mas=0.05)
def _(d):
    return P(ROJO, [BG("bg_sequia"), brillo(720, 620, 520, "#fff0a0", 0.5, 0.2, pulso=[0.2, 0.5]), polvo("#ffd27a", 40, (0, 1100, 1080, 1800), 23)],
             cam(1.0, 1.12, (540, 1300), (540, 1450)), "corte", sfx=[(0.02, "golpe", -18)])


@v.plano(102, "al otro lado, en Australia: el canguro cruza a saltos la tierra seca")
def _(d):
    salto = [{"t": 0, "x": 1250, "y": 1420, "ex": -1, "rot": 0}, {"t": d * 0.2, "x": 1010, "y": 1280, "ex": -1, "rot": -8, "ease": "salida"}, {"t": d * 0.4, "x": 800, "y": 1420, "ex": -1, "rot": 4, "ease": "entrada"},
             {"t": d * 0.6, "x": 600, "y": 1280, "ex": -1, "rot": -8, "ease": "salida"}, {"t": d * 0.8, "x": 420, "y": 1420, "ex": -1, "rot": 4, "ease": "entrada"}, {"t": d, "x": 300, "y": 1340, "ex": -1, "rot": -6, "ease": "salida"}]
    return P(ROJO, [BG("bg_sequia"), brillo(720, 620, 520, "#fff0a0", 0.5, 0.2, pulso=[0.2, 0.5]),
             IMG("canguro", ancho=460, z=0.5, ex=-1, keys=salto), polvo("#ffd27a", 50, (0, 1300, 1080, 1700), 25)],
             cam(1.0, 1.04, (560, 1200)), "corte", hud=[contexto(0.05, d - 0.05, "AUSTRALIA")], sfx=[(d * 0.4, "golpe", -22), (d * 0.8, "golpe", -22)])


@v.plano(107, "¿y si el agua se enfría de más? una mancha azul crece junto a América")
def _(d):
    return P(MAPA, [BG("bg_pacifico"), mancha("mancha_fria", 640, [{"t": 0, "x": 720, "y": 960, "escala": 0.3, "op": 0.4}, {"t": d, "x": 640, "escala": 1.15, "op": 1, "ease": "suave"}]),
             IMG("termo_frio", ancho=200, x=200, y=1380, z=0.6, keys=[{"t": 0, "y": 1300}, {"t": d, "y": 1400, "ease": "suave"}]),
             *rafagas(d, -1, 1180, 3, "viento_cian", op=0.8)],
             cam(1.0, 1.06, (560, 960), (620, 960)), "desenfoque", hud=[amarillo(0.1, d - 0.03, "¿Y SI SE ENFRÍA?", y=520, tam=92, color=CIAN)], sfx=[(0.1, "brillo", -20), (0.6, "whoosh", -20, {"dur": 0.8})])


@v.plano(114, "micro: el termómetro azul baja de golpe", mas=0.05)
def _(d):
    return P(["#041a30", "#0a3a5e"], [BG("bg_sub_frio"), IMG("termo_frio", ancho=420, x=540, z=0.5, keys=cae(0.0, 0.4, 500, 1150)), polvo("#d8f4ff", 40, (0, 300, 1080, 1800), 35)],
             cam(1.0, 1.1), "corte", sfx=[(0.3, "golpe", -18), (0.1, "burbuja", -20)])


@v.plano(115, "entonces se llama… el copo de nieve gira y entra")
def _(d):
    return P(["#041a30", "#0a3a5e"], [brillo(540, 1000, 520, "#7fd8ff", 0.45, 0.1),
             IMG("copo", ancho=620, x=540, y=1050, z=0.5, keys=[{"t": 0, "escala": 0.3, "rot": -90}, {"t": 0.35, "escala": 1.1, "rot": 0, "ease": "rebote"}, {"t": d, "escala": 1.0, "rot": 20}]),
             polvo("#ffffff", 50, (0, 300, 1080, 1700), 27)],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "brillo", -18)])


@v.plano(118, "La Niña: el Pacífico azul con su nombre")
def _(d):
    return P(MAPA, [BG("bg_pacifico"), mancha("mancha_fria", 700, [{"t": 0, "x": 620, "y": 960, "escala": 1.1}, {"t": d, "x": 600, "escala": 1.2}], anim={"pulso": [0.04, 0.7]}),
             IMG("copo", ancho=220, x=600, y=960, z=0.6, anim={"girar": 20})],
             cam(1.05, 1.1, (600, 960)), "corte", hud=[rotulo(0.05, d - 0.05, "LA NIÑA", tam=120, color="#141414", capsula="#7df9ffe6", y=540)], sfx=[(0.05, "ding", -18)])


@v.plano(120, "este año El Niño ha vuelto: la Tierra con la franja roja que crece")
def _(d):
    return P(ESP, [BG("bg_esp_violeta"), IMG("tierra_pacifico", ancho=920, x=540, y=1080, z=0.45, anim={"girar": 1}),
             IMG("tierra_nino", ancho=920, x=540, y=1080, z=0.46, keys=[{"t": 0, "op": 0}, {"t": d * 0.5, "op": 1, "ease": "suave"}], anim={"girar": 1}),
             brillo(600, 1120, 320, "#ff5a1e", 0.8, 0.55, pulso=[0.35, 0.4], keys=[{"t": 0, "op": 0}, {"t": d * 0.5, "op": 1}]), sat(d, 120, 138)],
             cam(1.0, 1.06, (540, 1080)), "desenfoque", hud=[contexto(0.05, d - 0.05, "2026: HA VUELTO")], sfx=[(0.1, "subida", -18, {"dur": 0.9}), (d * 0.5, "impacto", -15)])


@v.plano(126, "y los meteorólogos avisan: la pantalla con el mapa y la curva que sube")
def _(d):
    return P(["#05080e", "#101a28"], [brillo(540, 900, 600, "#3fb8ff", 0.3, 0.1), IMG("monitor", ancho=980, x=540, z=0.5, keys=[{"t": 0, "y": 1180, "escala": 0.94}, {"t": d, "y": 1150, "escala": 1.03, "ease": "suave"}]),
             senala(860, 1010, d * 0.45, d - 0.1, 70, AMBAR), polvo("#7df9ff", 20, (100, 500, 980, 1500), 29)],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[contexto(0.05, d - 0.05, "METEORÓLOGOS · OMM")], sfx=[(0.1, "senal", -20), (d * 0.45, "ding", -22)])


@v.plano(130, "podría ser de los más fuertes: el termómetro llega arriba sobre el mar caliente")
def _(d):
    return P(ROJO, [BG("bg_sub_tibio"), brillo(540, 900, 700, "#ff3d1e", 0.4, 0.08, pulso=[0.2, 0.5]),
             IMG("termo_tibio", ancho=330, x=540, y=1100, z=0.5, keys=[{"t": 0, "op": 1}, {"t": d * 0.5, "op": 0}]),
             IMG("termo_max", ancho=330, x=540, y=1100, z=0.51, keys=[{"t": 0, "op": 0, "escala": 1.0}, {"t": d * 0.5, "op": 1}, {"t": d * 0.62, "escala": 1.12, "ease": "rebote"}, {"t": d, "escala": 1.05}]),
             polvo("#ffd27a", 50, (150, 500, 930, 1600), 31, "chispas")],
             cam(1.0, 1.08, (540, 1000), temblor=1), "corte", hud=[amarillo(0.1, d - 0.03, "DE LOS MÁS FUERTES", y=560, tam=78, color="#ffffff")], sfx=[(0.05, "subida", -16, {"dur": 1.0})])


@v.plano(136, "micro: jamás medidos, la mancha roja enorme", mas=0.05)
def _(d):
    return P(MAPA, [BG("bg_pacifico"), mancha("mancha_caliente", 900, [{"t": 0, "x": 640, "y": 960, "escala": 0.9}, {"t": d, "escala": 1.2, "ease": "salida"}]),
             brillo(640, 960, 500, "#ff3d1e", 0.6, 0.3, pulso=[0.3, 0.3])],
             cam(1.1, 1.2, (620, 960), temblor=2), "corte", hud=[amarillo(0.0, d - 0.03, "¿RÉCORD?", y=540, tam=130, color=MAGENTA)], sfx=[(0.02, "impacto", -13)])


@v.plano(138, "micro: todo por… una ráfaga sola cruza", mas=0.05)
def _(d):
    return P(FRIO, [BG("bg_mar_frio"), nube_fondo(d, 138, 152, 660, "nube", 400, 0.45), *rafagas(d, -1, 900, 1),
             IMG("boya", ancho=260, x=760, y=1330, z=0.45, anim={"balanceo": [9, 1.2], "flotar": [10, 1.2]})],
             cam(1.0, 1.06, (540, 1000)), "desenfoque", sfx=[(0.02, "whoosh", -15, {"dur": 0.6})])


@v.plano(141, "un viento que deja de soplar: las ráfagas se apagan, el mar se calienta y se queda quieto")
def _(d):
    return P(FRIO, [BG("bg_mar_frio"), IMG("bg_mar_tibio", ancho=1180, x=540, y=960, z=0.06, keys=[{"t": d * 0.3, "op": 0}, {"t": d, "op": 0.9, "ease": "suave"}]),
             nube_fondo(d, 138, 152, 660, "nube", 400, 0.45), *rafagas(d, -1, 700, 3, frena=True),
             IMG("boya", ancho=260, x=760, y=1330, z=0.45, anim={"balanceo": [3, 2.4], "flotar": [4, 2.0]})],
             cam(1.04, 1.0, (540, 1000)), "corte", hud=[rotulo(0.08, d * 0.6, "UN VIENTO", tam=100, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(0.1, "roce", -22)])


@v.plano(146, "¿tú sabías por qué se llama así? la Tierra con la franja vuelve a subir (bucle)")
def _(d):
    return P(ESP, [BG("bg_esp_violeta"), IMG("tierra_nino", ancho=940, z=0.5, keys=[{"t": 0, "x": 540, "y": 1300, "escala": 0.92}, {"t": 0.45, "y": 1100, "escala": 1.0, "ease": "rebote"}, {"t": d, "y": 1080, "escala": 1.02}]),
             brillo(600, 1130, 300, "#ff7a1e", 0.75, 0.55, pulso=[0.35, 0.45]),
             IMG("estrella_navidad", ancho=200, x=870, y=520, z=0.3, anim={"pulso": [0.08, 0.7]}), polvo("#ffd27a", 30, (150, 800, 930, 1400), 3, "chispas")],
             cam(1.0, 1.04, (540, 1080)), "desenfoque", hud=[rotulo(0.1, d - 0.4, "¿LO SABÍAS?", tam=100, color="#141414", capsula="#ffd23fe6", y=520)],
             sfx=[(0.1, "brillo", -18), (d * 0.6, "ding", -22)])


v.construir("2026-11-19-extra-01-el-nino", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 19, "db": -13},
            claves=["niño", "clima", "Navidad", "pescadores", "Perú", "diciembre", "frío", "tibio", "peces", "Niño", "Jesús", "viento", "caliente",
                    "Pacífico", "Asia", "frena", "América", "lluvias", "diluvios", "sequía", "Australia", "Niña", "meteorólogos", "fuertes", "soplar"])
