"""01 · Un día duraba dieciocho horas — método denso. Lote 2026-11-18-manana, Agente 08:00 (Nico).
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import os, sys, random

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_01  # noqa: E402

SVG = ilus_01.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

ROCA = ["#f2dcb0", "#7ab8e8"]
MAR = ["#4ac8d8", "#062236"]
OSC = ["#05060f", "#120a24"]

# satélite que cruza los planos de espacio del tramo de la Luna (detalle de fondo que dura)
SAT = (v.w(91), v.w(131), (1180, 300), (-120, 520))


def satelite(d, z=0.15):
    return IMG("satelite", ancho=140, z=z, rot=-15, anim={"girar": 4}, keys=recorrido(*SAT, d))


def tierra_esf(x, y, r, giro, z=0.4, keys=None, luz=(-0.7, -0.3)):
    e = {"tipo": "esfera", "radio": r, "textura": "tierra", "giro": giro, "x": x, "y": y, "z": z, "luz": list(luz), "halo": "#7ac8ff", "semilla": 3}
    if keys: e["keys"] = keys
    return e


def arco_sol(d, t0, t1, cx=540, cy=1350, R=640, z=0.2, r=110):
    """El Sol sale por la izquierda, cruza el cielo y se pone por la derecha entre t0 y t1 (s del plano)."""
    import math
    ks = []
    for k in range(9):
        a = math.pi * (1 - k / 8)
        ks.append({"t": round(t0 + (t1 - t0) * k / 8, 3), "x": cx + R * math.cos(a), "y": cy - R * 0.8 * math.sin(a), "ease": "lineal"})
    return [{**s, "keys": [dict(k) for k in ks]} for s in sol(0, 0, r, z)]


def barra_dia(d, x, y, horas_luz, color, t0=0.05, t1=None, ancho=820, z=0.6, desde=0):
    return {"tipo": "barra", "x": x, "y": y, "ancho": ancho, "alto": 70, "color": color, "fondo": "#ffffff18", "z": z,
            "keys": [{"t": t0, "progreso": desde / 24}, {"t": t1 or d * 0.6, "progreso": horas_luz / 24, "ease": "salida"}]}


# ================================================================== PLANOS
@v.plano(0, "gancho: la Tierra gira deprisa con la Luna enorme y cerca")
def _(d):
    ks = arranque(540, 1080, d, "abajo", 300, 40)
    return P(OSC, [BG("bg_esp_violeta"), tierra_esf(540, 1080, 400, 260, 0.4, ks),
             luna(0, 0, 330, 0.5, keys=[{"t": 0, "x": 980, "y": 560, "escala": 0.9}, {"t": d, "x": 900, "y": 600, "escala": 1.05, "ease": "suave"}], anim={"girar": 8}),
             brillo(540, 1080, 560, "#7ac8ff", 0.35, 0.39, pulso=[0.1, 0.4]),
             flecha([[160, 1300], [140, 1080], [230, 860]], 0.0, d * 0.9, CIAN, 9, z=0.6), *lineas_vel(300, 1500, 3, "#7df9ffaa")],
             cam(1.05, 1.0, (540, 1000), (540, 980)), vineta=0.6, sfx=[(0.02, "whoosh", -12, {"dur": 0.9}), (0.3, "brillo", -20)])


@v.plano(3, "micro: el Sol pasa como una raya")
def _(d):
    return P(["#ffb25a", "#5a2448"], [BG("bg_tierra_antigua"), brillo(540, 900, 700, "#fff2c0", 0.4),
             *arco_sol(d, 0.0, d, 540, 1350, 640, r=110),
             flecha([[-60, 1500], [100, 1000], [540, 800], [980, 1000], [1140, 1500]], 0.0, d, AMBAR, 7, punta=False, z=0.15)],
             cam(1.0, 1.05), "corte", sfx=[(0.02, "whoosh", -16, {"dur": 0.5})])


@v.plano(3, "dieciocho horas: barra del día", mas=0.62)
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), estrellas(30, 4), brillo(540, 900, 500, "#7ac8ff", 0.35),
             barra_dia(d, 540, 1250, 24, "#3a4a6a", 0.0, 0.01), barra_dia(d, 540, 1250, 18, CIAN, 0.1, d * 0.7),
             tierra_esf(540, 900, 300, 200, 0.5), *sol(1000, 500, 70, 0.3), fugaz(0.1, 100, 400, 380, 600)],
             cam(1.0, 1.05, (540, 1000), (540, 980)), hud=[contador(0.05, d - 0.05, 0, 18, d * 0.7, "H", tam=140, y=560, borde=CIAN, miles=False)],
             sfx=[(0.1, "subida", -18, {"dur": d * 0.6})])


@v.plano(5, "la Tierra giraba: flecha de giro alrededor")
def _(d):
    import math
    pts = [[540 + 470 * math.cos(math.radians(a)), 1000 + 160 * math.sin(math.radians(a))] for a in range(200, 520, 20)]
    return P(OSC, [BG("bg_esp_ambar"), tierra_esf(540, 1000, 330, 180, 0.4, [{"t": 0, "escala": 0.95}, {"t": d, "escala": 1.03}]),
             flecha(pts, 0.05, d * 0.85, LIMA, 10, z=0.6), brillo(540, 1000, 480, "#7ac8ff", 0.3, 0.39)],
             cam(1.0, 1.06), "desenfoque", hud=[amarillo(0.1, d - 0.05, "MÁS DEPRISA", y=560, color=LIMA, tam=90)], sfx=[(0.1, "whoosh", -16, {"dur": 0.8})])


@v.plano(10, "micro: la superficie pasa volando")
def _(d):
    return P(OSC, [tierra_esf(540, 2050, 1300, 120, 0.4), *lineas_vel(700, 700, 5, "#ffffffaa"), *lineas_vel(500, 900, 6, "#7df9ffaa")],
             cam(1.0, 1.08, (540, 1300), (540, 1250)), "corte", sfx=[(0.02, "whoosh", -14, {"dur": 0.5})])


@v.plano(13, "hace 1.400 millones de años: la Tierra antigua")
def _(d):
    return P(["#1a0f2e", "#3a1a10"], [BG("bg_tierra_antigua"),
             luna(820, 520, 360, 0.2, keys=[{"t": 0, "y": 600}, {"t": d, "y": 470, "ease": "suave"}], anim={"girar": 2}),
             brillo(820, 520, 300, "#ffe8c0", 0.25, 0.19), polvo("#ffb25a", 30, (0, 900, 1080, 1700), 5, "chispas"),
             fugaz(0.4, 100, 300, 420, 480)],
             cam(1.0, 1.08, (540, 1100), (540, 1000)), "desenfoque",
             hud=[contador(0.05, d - 0.05, 0, 1400, d * 0.55, "MILLONES DE AÑOS", tam=110, y=560, borde=AMBAR)], sfx=[(0.05, "subida", -18, {"dur": d * 0.5})])


@v.plano(11, "micro: un volcán escupe lava en la Tierra antigua", mas=0.0)
def _(d):
    return P(["#1a0f2e", "#3a1a10"], [BG("bg_tierra_antigua"), brillo(560, 1060, 300, "#ffb04a", 0.7, 0.5, pulso=[0.3, 0.12]),
             polvo("#ffd06a", 60, (420, 900, 700, 1100), 21, "chispas")],
             cam(2.2, 2.4, (560, 1060), (560, 1040), temblor=4), "corte", sfx=[(0.02, "golpe", -16)])


@v.plano(18, "el Sol salía y se ponía sobre la Tierra antigua")
def _(d):
    return P(["#1a0f2e", "#3a1a10"], [BG("bg_tierra_antigua"), *arco_sol(d, 0.0, d * 0.95, 540, 1300, 560, 0.1, 100),
             {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#05030f", "x": 540, "y": 960, "z": 0.95,
              "keys": [{"t": 0, "op": 0.55}, {"t": d * 0.25, "op": 0.0}, {"t": d * 0.75, "op": 0.0}, {"t": d, "op": 0.6}]},
             luna(860, 470, 280, 0.12, anim={"girar": 2})],
             cam(1.35, 1.45, (540, 1250), (560, 1230)), sfx=[(0.1, "brillo", -20), (d * 0.8, "whoosh", -18, {"dur": 0.6})])


@v.plano(25, "solo dieciocho horas: seis horas que faltan")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), barra_dia(d, 540, 1000, 24, "#ffffff40", 0.0, 0.01),
             barra_dia(d, 540, 1000, 18, AMBAR, 0.0, d * 0.5),
             {"tipo": "forma", "forma": "rect", "ancho": 205, "alto": 70, "relleno": "#ff2d55", "x": 540 + 410 - 102, "y": 1000, "z": 0.62,
              "keys": [{"t": d * 0.45, "op": 0}, {"t": d * 0.55, "op": 0.9}, {"t": d, "op": 0.9, "y": 1100, "rot": 12, "ease": "entrada"}]},
             tierra_esf(540, 1350, 220, 150, 0.4)],
             cam(1.0, 1.04), "corte", hud=[rotulo(0.05, d - 0.05, "18 H", tam=150, color="#141414", capsula="#ffe93de6", y=560)],
             sfx=[(d * 0.5, "golpe", -16)])


@v.plano(29, "¿cómo lo sabemos? la lupa recorre la roca")
def _(d):
    return P(ROCA, [BG("capas_cerca"), IMG("lupa", ancho=520, z=0.6, keys=[{"t": 0, "x": 300, "y": 1200}, {"t": d, "x": 760, "y": 1000, "ease": "suave"}]),
             brillo(540, 1100, 300, "#ffffff", 0.2, 0.5)],
             cam(1.0, 1.06), "zoom", hud=[amarillo(0.05, d - 0.03, "¿CÓMO?", y=560, tam=120, color="#ffffff")], sfx=[(0.1, "roce", -22)])


@v.plano(32, "rocas del norte de China: el acantilado")
def _(d):
    return P(ROCA, [BG("acantilado"), IMG("geologo_libreta", ancho=300, x=880, y=1580, z=0.5, keys=aparece(d * 0.4, 0.4)),
             polvo("#f2dcb0", 30, (0, 600, 1080, 1700), 7), senala(420, 1100, d * 0.5, d - 0.05, 160, AMBAR)],
             cam(1.08, 1.0, (540, 1100), (540, 1060)), "desenfoque", hud=[contexto(0.05, d - 0.05, "NORTE DE CHINA")], sfx=[(0.1, "roce", -22)])


@v.plano(39, "sus capas guardan los ritmos del clima")
def _(d):
    destellos = [{"tipo": "forma", "forma": "rect", "ancho": 1100, "alto": 38, "relleno": c, "x": 540, "y": y, "z": 0.6,
                  "keys": [{"t": t, "op": 0}, {"t": t + 0.1, "op": 0.95}, {"t": t + 0.6, "op": 0}]}
                 for (y, t, c) in [(700, 0.1, CIAN), (860, 0.45, MAGENTA), (1020, 0.8, CIAN), (1180, 1.15, MAGENTA), (1340, 1.5, CIAN), (1500, 1.85, MAGENTA)]]
    return P(ROCA, [BG("capas_cerca"), *destellos],
             cam(1.0, 1.08, (540, 1000), (540, 1080)), "corte", hud=[rotulo(0.1, d - 0.05, "RITMOS DEL CLIMA", tam=78, color="#141414", capsula="#ffe93de6", y=560)],
             sfx=[(t, "tic", -22) for t in (0.1, 0.45, 0.8, 1.15, 1.5, 1.85) if t < d])


@v.plano(46, "como los anillos de un árbol")
def _(d):
    return P(["#2a3a22", "#0e160a"], [brillo(540, 900, 600, "#cfe58a", 0.3), IMG("rama_hojas", ancho=700, x=180, y=420, z=0.2, rot=20, anim={"balanceo": [4, 1.2]}),
             IMG("tronco", ancho=820, x=540, y=1080, z=0.5, keys=aparece(0.0, 0.4) + [{"t": d, "rot": 18, "ease": "suave"}]),
             *[senala(540, 1080, 0.3 + k * 0.25, d - 0.05, 60 + k * 70, LIMA if k % 2 else AMBAR) for k in range(5)]],
             cam(1.0, 1.06), "desenfoque", sfx=[(0.05, "pop", -18)] + [(0.3 + k * 0.25, "tic", -24) for k in range(5)])


@v.plano(52, "micro: el martillo golpea la roca")
def _(d):
    return P(ROCA, [BG("capas_cerca"), IMG("martillo", ancho=700, z=0.6, keys=[{"t": 0, "x": 760, "y": 700, "rot": -40}, {"t": d * 0.6, "x": 560, "y": 980, "rot": 5, "ease": "entrada"}]),
             IMG("chispa", ancho=260, x=440, y=1000, z=0.7, keys=[{"t": d * 0.55, "op": 0}, {"t": d * 0.6, "op": 1}, {"t": d, "op": 0, "escala": 1.4}])],
             cam(1.15, 1.2, (540, 1000), (520, 1000), temblor=4), "corte", sfx=[(d * 0.6, "golpe", -14)])


@v.plano(53, "micro: saltan esquirlas de roca")
def _(d):
    r = random.Random(3)
    trozos = [{"tipo": "forma", "forma": "poligono", "puntos": [[-14, -10], [12, -14], [16, 10], [-10, 14]], "relleno": r.choice(ilus_01.CAPAS), "z": 0.6,
               "keys": [{"t": 0, "x": 540, "y": 1000, "rot": 0}, {"t": d, "x": 540 + r.uniform(-420, 420), "y": 1000 + r.uniform(-500, 200), "rot": r.uniform(-200, 200), "ease": "salida"}]}
              for _ in range(14)]
    return P(ROCA, [BG("capas_cerca"), *trozos, brillo(540, 1000, 240, "#ffffff", 0.4, 0.5)], cam(1.2, 1.3), "corte", sfx=[(0.02, "roce", -16)])


@v.plano(54, "dos geólogos calcularon el día")
def _(d):
    return P(ROCA, [BG("acantilado"), IMG("geologo_lupa", ancho=520, x=330, y=1450, z=0.5, keys=[{"t": 0, "x": 300}, {"t": d, "x": 340, "ease": "suave"}]),
             IMG("geologo_libreta", ancho=360, x=820, y=1400, z=0.5),
             flecha([[640, 1240], [700, 1050], [800, 980]], 0.3, d * 0.7, MAGENTA, 7, [16, 12], z=0.6),
             brillo(800, 980, 160, "#ff3df2", 0.4, 0.55, keys=[{"t": d * 0.6, "intensidad": 0}, {"t": d * 0.75, "intensidad": 0.6}])],
             cam(1.0, 1.05, (540, 1250), (560, 1200)), "desenfoque",
             hud=[rotulo(d * 0.55, d - 0.05, "18,7 H", tam=120, color="#ffffff", capsula="#0d1330d8", borde=MAGENTA, y=560)],
             sfx=[(0.3, "trazo", -24), (d * 0.6, "ding", -20)])


@v.plano(59, "un año: la Tierra da la vuelta al Sol marcando días")
def _(d):
    import math
    marcas = [{"tipo": "forma", "forma": "circulo", "radio": 5, "relleno": CIAN, "x": 540 + 380 * math.cos(a), "y": 1000 + 380 * math.sin(a), "z": 0.5,
               "keys": [{"t": d * 0.9 * k / 60, "op": 0}, {"t": d * 0.9 * k / 60 + 0.05, "op": 1}]}
              for k, a in enumerate([2 * math.pi * k / 60 - math.pi / 2 for k in range(60)])]
    ks = [{"t": d * 0.9 * k / 12, "x": 540 + 380 * math.cos(2 * math.pi * k / 12 - math.pi / 2), "y": 1000 + 380 * math.sin(2 * math.pi * k / 12 - math.pi / 2), "ease": "lineal"} for k in range(13)]
    return P(OSC, [BG("bg_esp_violeta"), *sol(540, 1000, 120, 0.3), *marcas, tierra_esf(0, 0, 60, 300, 0.6, ks)],
             cam(1.0, 1.04), "zoom", hud=[contexto(0.05, d - 0.05, "UN AÑO")], sfx=[(0.05, "tictac", -26, {"dur": d * 0.9, "ritmo": 0.12})])


@v.plano(65, "más de 450 días: el calendario se dispara")
def _(d):
    hojas = [IMG("calendario", ancho=600, x=540, y=1050, z=0.6 + k * 0.001,
                 keys=[{"t": k * d / 10, "y": 1050, "rot": 0, "op": 1}, {"t": k * d / 10 + 0.3, "y": 500, "rot": -40 + k * 8, "op": 0, "ease": "entrada"}])
             for k in range(8)]
    return P(["#3a2a1c", "#1a1410"], [brillo(540, 900, 700, "#ffcf8a", 0.35), IMG("calendario", ancho=600, x=540, y=1050, z=0.59), *hojas],
             cam(1.0, 1.05), hud=[contador(0.05, d - 0.05, 365, 450, d * 0.6, "DÍAS", tam=130, y=560, borde=AMBAR, contar_prefijo="+")],
             sfx=[(k * d / 10, "roce", -24) for k in range(8)])


@v.plano(67, "otra pista: bajamos al mar")
def _(d):
    return P(MAR, [BG("bg_mar_antiguo"), polvo("#d8ffff", 40, (0, 300, 1080, 1600), 8, "burbujas"),
             IMG("coral_vivo", ancho=380, x=540, y=1350, z=0.4, keys=[{"t": 0, "y": 1700}, {"t": d, "y": 1380, "ease": "salida"}])],
             cam(1.0, 1.08, (540, 700), (540, 1100)), "barrido", hud=[rotulo(0.05, d - 0.03, "OTRA PISTA", tam=90, color="#ffffff", capsula="#0d1330d8", borde=CIAN, y=560)],
             sfx=[(0.05, "agua", -20, {"dur": 0.8})])


@v.plano(69, "corales vivos en el mar antiguo")
def _(d):
    return P(MAR, [BG("bg_mar_antiguo"), polvo("#d8ffff", 40, (0, 300, 1080, 1600), 9, "burbujas"),
             IMG("coral_vivo", ancho=420, x=360, y=1300, z=0.45, anim={"balanceo": [3, 1.4]}),
             IMG("coral_vivo", ancho=300, x=760, y=1400, z=0.4, ex=-1, anim={"balanceo": [4, 1.1]}),
             IMG("coral_vivo", ancho=220, x=930, y=1480, z=0.35, anim={"balanceo": [3, 0.9]})],
             cam(1.0, 1.06, (540, 1200), (540, 1180)), "desenfoque", sfx=[(0.1, "burbuja", -22)])


@v.plano(74, "el coral fósil: 400 millones de años")
def _(d):
    return P(["#3a3a42", "#14141a"], [brillo(540, 900, 600, "#ffe8c0", 0.3), IMG("coral_fosil", ancho=880, x=540, y=1150, z=0.5, keys=aparece(0.0, 0.4) + [{"t": d, "rot": -6, "ease": "suave"}]),
             polvo("#e6d2a8", 25, (100, 700, 980, 1500), 11)],
             cam(1.0, 1.08), "corte", hud=[contador(0.05, d - 0.05, 0, 400, d * 0.55, "MILLONES DE AÑOS", tam=110, y=560, borde=AMBAR)],
             sfx=[(0.05, "pop", -18), (0.1, "subida", -20, {"dur": d * 0.5})])


@v.plano(78, "cada día una raya finísima")
def _(d):
    rayas = [{"tipo": "forma", "forma": "rect", "ancho": 820, "alto": 4, "relleno": "#3a2810", "x": 540, "y": 640 + k * 30, "z": 0.6,
              "keys": [{"t": 0.2 + k * (d - 0.4) / 24, "op": 0, "ex": 0.2}, {"t": 0.2 + k * (d - 0.4) / 24 + 0.08, "op": 0.9, "ex": 1}]}
             for k in range(24)]
    return P(["#d8c49a", "#a08458"], [BG("coral_superficie"), *rayas,
             IMG("lupa", ancho=620, x=700, y=1300, z=0.7, keys=[{"t": 0, "y": 1500}, {"t": d, "y": 1250, "ease": "suave"}])],
             cam(1.45, 1.6, (540, 900), (560, 880)), "zoom", hud=[contexto(0.05, d - 0.05, "1 RAYA = 1 DÍA")],
             sfx=[(0.2 + k * (d - 0.4) / 24, "tic", -28) for k in range(0, 24, 3)])


@v.plano(84, "en un año caben unas cuatrocientas")
def _(d):
    r = random.Random(5)
    rayas = [{"tipo": "forma", "forma": "rect", "ancho": r.uniform(300, 380), "alto": 2, "relleno": "#ffe9c0", "x": 760, "y": 560 + k * 2.2, "z": 0.6,
              "keys": [{"t": d * 0.75 * k / 400, "op": 0}, {"t": d * 0.75 * k / 400 + 0.03, "op": 0.8}]} for k in range(0, 400, 4)]
    return P(["#3a3a42", "#14141a"], [brillo(540, 900, 600, "#ffe8c0", 0.25), IMG("coral_fosil", ancho=700, x=300, y=1050, z=0.45, rot=-8),
             {"tipo": "forma", "forma": "rect", "ancho": 420, "alto": 920, "relleno": "#2a2018", "x": 760, "y": 780, "z": 0.55, "op": 0.85},
             *rayas, flecha([[420, 900], [560, 800]], 0.1, 0.6, AMBAR, 7, z=0.6)],
             cam(1.0, 1.04), hud=[contador(0.05, d - 0.05, 0, 400, d * 0.75, "RAYAS", tam=130, y=1180, borde=MAGENTA)],
             sfx=[(0.05, "subida", -18, {"dur": d * 0.7}), (d * 0.78, "ding", -18)])


@v.plano(91, "¿quién nos frenó?")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), satelite(d),
             IMG("tierra_hd", ancho=700, x=540, y=1050, z=0.4, keys=[{"t": 0, "rot": 0, "ease": "salida"}, {"t": d, "rot": 160}])],
             cam(1.0, 1.08), "desenfoque", hud=[amarillo(0.05, d - 0.03, "¿QUIÉN?", y=560, tam=120, color=MAGENTA)], sfx=[(0.05, "whoosh", -16, {"dur": 0.6})])


@v.plano(94, "micro: ¡la Luna! entra de golpe")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), luna(540, 1000, 760, 0.5, keys=[{"t": 0, "escala": 0.3, "x": 900, "y": 600}, {"t": 0.25, "escala": 1.0, "x": 540, "y": 1000, "ease": "golpe"}]),
             brillo(540, 1000, 600, "#dfe6ff", 0.4, 0.45, pulso=[0.2, 0.15])],
             cam(1.0, 1.08, temblor=5), "corte", sfx=[(0.0, "subida", -18, {"dur": 0.25}), (0.25, "impacto", -12)], energia=0.9)


@v.plano(94, "micro: cráteres de la Luna", mas=0.55)
def _(d):
    return P(OSC, [luna(380, 1300, 2100, 0.5, anim={"girar": 4})], cam(1.0, 1.06), "corte", sfx=[(0.02, "brillo", -20)])


@v.plano(96, "su gravedad levanta las mareas: el bulto de agua")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), satelite(d), tierra(420, 1100, 520, giro=5),
             {"tipo": "forma", "forma": "elipse", "ancho": 560, "alto": 560, "relleno": "#3ab8ff", "x": 420, "y": 1100, "z": 0.45, "op": 0.35,
              "keys": [{"t": 0.0, "ex": 1.0, "op": 0.3}, {"t": d * 0.5, "ex": 1.4, "op": 0.6, "ease": "salida"}, {"t": d, "ex": 1.45, "op": 0.6}]},
             luna(940, 1100, 200, 0.5),
             flecha([[880, 1100], [720, 1100]], 0.2, d * 0.6, CIAN, 8, [16, 12], z=0.6)],
             cam(1.0, 1.05, (620, 1100), (640, 1100)), "desenfoque", hud=[amarillo(0.1, d - 0.05, "MAREAS", y=560, color=CIAN)],
             sfx=[(0.2, "agua", -18, {"dur": 1.2})])


@v.plano(101, "el bulto de agua sube por la playa")
def _(d):
    return P(["#2a4a8a", "#a8804a"], [BG("playa"), IMG("mar_frente", ancho=1080, x=540, z=0.4, keys=[{"t": 0, "y": 1950}, {"t": d, "y": 1650, "ease": "suave"}]),
             luna(780, 520, 420, 0.2, anim={"girar": 2}), brillo(780, 520, 380, "#ffffff", 0.35, 0.19),
             polvo("#ffffff", 30, (0, 1300, 1080, 1800), 13, "burbujas"),
             flecha([[780, 760], [780, 1150]], 0.2, d * 0.6, CIAN, 8, [16, 12], z=0.5)],
             cam(1.0, 1.04, (540, 1100), (540, 1150)), "barrido", sfx=[(0.1, "agua", -16, {"dur": d})])


@v.plano(109, "como un freno: la pinza aprieta el disco y saltan chispas")
def _(d):
    chispas = [IMG("chispa", ancho=140, x=540 + dx, y=640 + dy, z=0.7, keys=[{"t": t, "op": 0}, {"t": t + 0.05, "op": 1}, {"t": t + 0.35, "op": 0, "y": 640 + dy - 120}])
               for dx, dy, t in [(-60, 0, 0.3), (40, 20, 0.45), (-20, -10, 0.6), (80, 10, 0.75), (0, 30, 0.9)] if t < d]
    return P(["#1a1e26", "#0a0c10"], [brillo(540, 1000, 600, "#ff6a3a", 0.25, keys=[{"t": 0.3, "intensidad": 0}, {"t": d, "intensidad": 0.6}]),
             IMG("disco_freno", ancho=900, x=540, y=1100, z=0.5, keys=[{"t": 0, "rot": 0, "ease": "salida"}, {"t": d, "rot": 240}]),
             IMG("pinza_freno", ancho=300, x=540, y=650, z=0.6, keys=[{"t": 0, "y": 520}, {"t": 0.3, "y": 650, "ease": "golpe"}]), *chispas],
             cam(1.0, 1.06, temblor=2), "corte", hud=[rotulo(0.1, d - 0.05, "FRENO", tam=120, color="#141414", capsula="#ffe93de6", y=1180)],
             sfx=[(0.3, "golpe", -16), (0.35, "roce", -16)])


@v.plano(112, "la Tierra pierde giro (flecha que se encoge)")
def _(d):
    import math
    pts = [[540 + 430 * math.cos(math.radians(a)), 1000 + 150 * math.sin(math.radians(a))] for a in range(200, 500, 20)]
    return P(OSC, [BG("bg_esp_ambar"), IMG("tierra_hd", ancho=600, x=540, y=1000, z=0.4, keys=[{"t": 0, "rot": 0, "ease": "salida"}, {"t": d, "rot": 25}]),
             {**flecha(pts, 0.0, 0.01, "#ff2d55", 10, z=0.6), "keys": [{"t": 0, "progreso": 1}, {"t": d * 0.8, "progreso": 0.3, "ease": "suave"}]}],
             cam(1.0, 1.04), "desenfoque", hud=[amarillo(0.1, d - 0.05, "PIERDE GIRO", y=560, color=MAGENTA, tam=90)], sfx=[(0.1, "rumor", -20)])


@v.plano(117, "la Luna lo gana y sale hacia fuera")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), satelite(d), tierra(200, 1250, 400, giro=4),
             luna(0, 0, 200, 0.5, keys=[{"t": 0, "x": 520, "y": 1000}, {"t": d, "x": 860, "y": 760, "ease": "salida"}]),
             flecha([[300, 1180], [790, 810]], 0.05, d * 0.9, LIMA, 9, z=0.45)],
             cam(1.0, 1.05, (540, 1000), (600, 950)), sfx=[(0.05, "subida", -18, {"dur": d * 0.8})])


@v.plano(121, "micro: la Luna sale disparada con estela")
def _(d):
    return P(OSC, [BG("bg_esp_ambar"), luna(0, 0, 360, 0.5, keys=[{"t": 0, "x": 300, "y": 1300, "escala": 1.2}, {"t": d, "x": 760, "y": 760, "escala": 0.8, "ease": "salida"}]),
             flecha([[160, 1460], [660, 880]], 0.0, d, LIMA, 12, punta=False, z=0.45)], cam(1.0, 1.1), "corte", sfx=[(0.02, "whoosh", -14, {"dur": 0.5})])


@v.plano(123, "se aleja casi 4 cm al año: la regla")
def _(d):
    x0, x1 = 540 - 480 + 18 + 182, 540 - 480 + 18 + 182 + 384
    return P(OSC, [BG("bg_esp_petroleo"), satelite(d), IMG("regla", ancho=1000, x=540, y=1150, z=0.5, rot=-2),
             luna(0, 980, 150, 0.56, keys=[{"t": 0.1, "x": x0}, {"t": d * 0.75, "x": x1, "ease": "salida"}]),
             flecha([[x0 - 80, 980], [x1 - 90, 980]], 0.1, d * 0.75, CIAN, 6, [14, 10], punta=False),
             tierra(120, 980, 180, 0.5, giro=6)],
             cam(1.1, 1.2, (540, 1050), (560, 1050)), "zoom",
             hud=[{**contador(0.1, d - 0.1, 0, 3.8, d * 0.7, "CM / AÑO", tam=120, y=560, borde=CIAN), "decimales": 1}],
             sfx=[(0.15 + i * 0.15, "tic", -24) for i in range(6)])


@v.plano(128, "y el freno sigue: la Tierra de hoy de noche")
def _(d):
    return P(OSC, [BG("bg_esp_ambar"), satelite(d), tierra(540, 1750, 1500, giro=2),
             polvo("#ffd27a", 50, (100, 900, 980, 1300), 12, "chispas"), fugaz(0.2, 900, 300, 600, 500)],
             cam(1.0, 1.05, (540, 1200), (540, 1150)), "desenfoque", hud=[amarillo(0.1, d - 0.05, "SIGUE", y=560, color=LIMA, tam=120)],
             sfx=[(0.1, "brillo", -22)])


@v.plano(132, "eclipse sobre Babilonia")
def _(d):
    return P(["#06081a", "#1a0e08"], [BG("bg_babilonia"), *sol(540, 820, 150, 0.2),
             {"tipo": "forma", "forma": "circulo", "radio": 152, "relleno": "#06081a", "z": 0.25,
              "keys": [{"t": 0, "x": 300, "y": 860}, {"t": d * 0.85, "x": 540, "y": 820, "ease": "suave"}]},
             {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#000010", "x": 540, "y": 960, "z": 0.9,
              "keys": [{"t": 0, "op": 0}, {"t": d * 0.85, "op": 0.45}]}],
             cam(1.0, 1.04, (540, 960), (540, 940)), "desenfoque", hud=[contexto(0.05, d - 0.05, "BABILONIA")], sfx=[(0.1, "subida", -22, {"dur": d * 0.8})])


@v.plano(135, "lo apuntan en una tablilla de arcilla")
def _(d):
    return P(["#3a2418", "#120a06"], [brillo(540, 1000, 600, "#ffb46a", 0.35, pulso=[0.1, 0.5]),
             IMG("tablilla", ancho=720, x=540, y=1100, z=0.5, keys=aparece(0.0, 0.35)),
             IMG("estilete", ancho=520, z=0.6, rot=-30, keys=[{"t": 0.2, "x": 760, "y": 880}, {"t": d * 0.5, "x": 700, "y": 920}, {"t": d * 0.75, "x": 740, "y": 890}, {"t": d, "x": 700, "y": 930}]),
             senala(722, 870, d * 0.4, d - 0.05, 80, AMBAR)],
             cam(1.0, 1.06, (540, 1050), (600, 980)), "corte", sfx=[(0.3, "roce", -20), (d * 0.6, "roce", -20)])


@v.plano(138, "el día crece: la barra del día se estira un pelo")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), barra_dia(d, 540, 1100, 24, CIAN, 0.0, 0.01),
             {"tipo": "forma", "forma": "rect", "ancho": 14, "alto": 70, "relleno": MAGENTA, "x": 540 + 410 + 7, "y": 1100, "z": 0.62,
              "keys": [{"t": d * 0.3, "op": 0, "ey": 0.2}, {"t": d * 0.5, "op": 1, "ey": 1.0, "ease": "elastico"}]},
             senala(957, 1100, d * 0.5, d - 0.05, 70, MAGENTA)],
             cam(1.0, 1.4, (540, 1100), (900, 1100)), "zoom", sfx=[(d * 0.5, "pop", -18)])


@v.plano(142, "dos milésimas de segundo cada siglo")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), satelite(d), brillo(540, 1100, 400, "#ff3df2", 0.3),
             IMG("calendario", ancho=420, x=540, y=1100, z=0.5, keys=late(0.3, 2, 0.08, 0.4))],
             cam(1.0, 1.05), "corte",
             hud=[{**contador(0.05, d - 0.05, 0, 0.002, d * 0.6, "S", tam=130, y=560, borde=MAGENTA, contar_prefijo="+"), "decimales": 3},
                  rotulo(d * 0.45, d - 0.05, "CADA SIGLO", tam=70, color="#ffffff", capsula="#c0392be6", y=760)],
             sfx=[(0.05, "subida", -20, {"dur": d * 0.55}), (d * 0.6, "ding", -18)])


@v.plano(148, "tú tienes seis horas más: 18 → 24")
def _(d):
    return P(["#ffb25a", "#2a1a3a"], [brillo(540, 700, 800, "#fff2c0", 0.4), *arco_sol(d, 0.0, d, 540, 1600, 600, 0.15, 110),
             barra_dia(d, 540, 1150, 24, LIMA, 0.2, d * 0.7, z=0.61, desde=18),
             {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 400, "relleno": "#1a1424", "x": 540, "y": 1800, "z": 0.3}],
             cam(1.0, 1.04), "desenfoque", hud=[contador(0.05, d - 0.05, 18, 24, d * 0.6, "H", tam=140, y=560, borde=LIMA, miles=False)],
             sfx=[(0.2, "subida", -18, {"dur": d * 0.5}), (d * 0.7, "brillo", -18)])


@v.plano(156, "¿en qué las gastas? (bucle hacia el gancho)")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), tierra_esf(540, 1080, 400, 260, 0.4, [{"t": 0, "escala": 0.85}, {"t": d, "escala": 1.0, "ease": "suave"}]),
             luna(0, 0, 330, 0.5, keys=[{"t": 0, "x": 1040, "y": 520, "escala": 0.8}, {"t": d, "x": 980, "y": 560, "escala": 0.9, "ease": "suave"}], anim={"girar": 8}),
             brillo(540, 1080, 560, "#7ac8ff", 0.35, 0.39)],
             cam(1.0, 1.05, (540, 980), (540, 1000)), "desenfoque", sfx=[(0.05, "brillo", -20)])


v.construir("2026-11-18-manana-01-dia-18-horas", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 41, "db": -13},
            claves=["dieciocho", "deprisa", "China", "capas", "geólogos", "cincuenta", "corales", "cuatrocientas", "Luna", "mareas", "freno", "centímetros", "babilonios", "siglo", "seis"])
