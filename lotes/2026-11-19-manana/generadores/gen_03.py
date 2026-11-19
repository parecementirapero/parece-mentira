"""03 · Esta torre ya no cae (la torre de Pisa) — método denso. Lote 2026-11-19-manana, Agente 08:00 (Nico).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]"""
import math, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_hoy  # noqa: E402

SVG = ilus_hoy.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

CIELO = ["#3a7ad8", "#e8f4ff"]
TARDE = ["#3a2a6a", "#ffd8a0"]
TIERRA = ["#3a2418", "#1a100c"]
SIGNO = -1  # sentido de «rot» del motor: la torre se inclina hacia la derecha


def torre(xb, yb, ancho, angulos, nombre="torre_pisa", z=0.5, extra=None):
    """Torre que gira alrededor de su BASE (xb, yb). angulos = [(t, grados, ease)]: grados > 0 → inclinada a la derecha."""
    s = ancho / 600
    r = 780 * s  # distancia del centro del lienzo a la base
    ks = []
    for t, g, *e in angulos:
        a = math.radians(g)
        k = {"t": round(t, 3), "x": xb + math.sin(a) * r, "y": yb - math.cos(a) * r, "rot": SIGNO * g}
        if e:
            k["ease"] = e[0]
        ks.append(k)
    return IMG(nombre, ancho=ancho, z=z, keys=ks, **(extra or {}))


def arco_grados(xb, yb, largo, g, t0, t1, color=AMBAR):
    """Línea vertical de referencia y arco hasta la inclinación g."""
    pts = [[xb + math.sin(math.radians(g * i / 8)) * largo, yb - math.cos(math.radians(g * i / 8)) * largo] for i in range(9)]
    return [flecha([[xb, yb], [xb, yb - largo * 1.05]], t0, t0 + 0.3, "#ffffffaa", 5, punta=False, z=0.7),
            flecha(pts, t0 + 0.2, t1, color, 8, z=0.72)]


# ================================================================== PLANOS
@v.plano(0, "gancho: la torre se cae… y se queda inclinada")
def _(d):
    return P(CIELO, [BG("bg_plaza"), torre(540, 1640, 440, [(0, 14), (0.45, 4.5, "elastico"), (d, 5.5, "suave")]),
             polvo("#ffffff", 20, (200, 1450, 880, 1600), 3)],
             cam(1.0, 1.04, (540, 1050), (540, 1000)), vineta=0.6, sfx=[(0.02, "whoosh", -12, {"dur": 0.6}), (0.42, "golpe", -14)])


@v.plano(5, "pero estuvo a punto: la torre vuelve a irse y tiembla")
def _(d):
    return P(CIELO, [BG("bg_plaza"), torre(540, 1640, 440, [(0, 5.5), (d * 0.7, 9, "entrada"), (d, 8.5)])],
             cam(1.0, 1.05, (540, 1000), temblor=3), "corte", hud=[amarillo(0.05, d - 0.03, "¡A PUNTO!", y=560, tam=120, color="#ff2d55")],
             sfx=[(0.1, "rumor", -20, {"dur": d})])


@v.plano(9, "la empezaron en 1173: la hoja del calendario")
def _(d):
    return P(CIELO, [BG("bg_plaza"), IMG("hoja_1173", ancho=560, x=540, y=1000, z=0.5, keys=cae(0.0, 0.45, 500, 1000))],
             cam(1.0, 1.05), "corte", sfx=[(0.3, "golpe", -18)])


@v.plano(17, "en Pisa, Italia: la plaza con la torre a lo lejos")
def _(d):
    return P(CIELO, [BG("bg_plaza"), torre(780, 1500, 300, [(0, 5.5)]), IMG("personas_mirando", ancho=700, x=420, y=1650, z=0.6)],
             cam(1.0, 1.06, (540, 1100), (620, 1050)), "desenfoque", hud=[contexto(0.05, d - 0.05, "PISA · ITALIA")], sfx=[(0.1, "brillo", -20)])


@v.plano(20, "cinco años después, con solo tres pisos: la grúa y tres pisos")
def _(d):
    return P(CIELO, [BG("bg_plaza"), IMG("grua", ancho=700, x=760, y=900, z=0.4, anim={"balanceo": [2, 2]}),
             torre(480, 1560, 520, [(0, 0)], "torre_3")],
             cam(1.0, 1.05, (540, 1200)), "corte", hud=[contador(0.05, d - 0.05, 0, 3, d * 0.5, "PISOS", tam=120, y=560, borde=AMBAR, miles=False)],
             sfx=[(0.1, "golpe", -24), (0.4, "golpe", -24)])


@v.plano(27, "ya se inclinaba: los tres pisos se tuercen")
def _(d):
    return P(CIELO, [BG("bg_plaza"), torre(540, 1560, 560, [(0, 0), (d * 0.8, 4, "suave")], "torre_3"), *arco_grados(540, 1560, 700, 4, 0.1, d * 0.8)],
             cam(1.0, 1.05, (540, 1250)), "corte", hud=[amarillo(0.05, d - 0.03, "SE INCLINA", y=560, tam=110, color=MAGENTA)], sfx=[(0.1, "subida", -22, {"dur": d * 0.8})])


@v.plano(30, "¿por qué? la lupa mira el suelo")
def _(d):
    return P(CIELO, [BG("bg_plaza"), torre(540, 1560, 560, [(0, 4)], "torre_3"),
             IMG("lupa", ancho=380, z=0.6, keys=[{"t": 0, "x": 300, "y": 1650}, {"t": d, "x": 700, "y": 1620, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1400)), "corte", hud=[rotulo(0.05, d - 0.05, "¿POR QUÉ?", tam=110, color="#141414", capsula="#ffd23fe6", y=480)], sfx=[(0.1, "roce", -20)])


@v.plano(32, "el suelo era blando, de arena y arcilla: corte del suelo y la torre se hunde")
def _(d):
    return P(TIERRA, [IMG("suelo_corte", ancho=1080, x=540, y=1420, z=0.4), torre(540, 1010, 420, [(0, 2), (d, 5, "suave")], "torre_3"),
             *[flecha([[x, 1080], [x, 1260]], 0.2 + k * 0.15, 0.6 + k * 0.15, LIMA, 8, z=0.6) for k, x in enumerate((420, 660))]],
             cam(1.0, 1.04, (540, 1150)), "corte",
             hud=[rotulo(0.05, d * 0.5, "ARENA", tam=90, color="#141414", capsula="#ffd23fe6", y=560), rotulo(d * 0.5 + 0.05, d - 0.05, "ARCILLA", tam=90, color="#ffffff", capsula="#8a5a3ae6", y=560)],
             sfx=[(0.1, "rumor", -22, {"dur": d})])


@v.plano(40, "luego llegaron las guerras: espadas y escudo")
def _(d):
    return P(TARDE, [BG("bg_plaza_tarde"), IMG("espadas", ancho=700, x=540, y=1050, z=0.5, keys=aparece(0.05, 0.4)), polvo("#ffd27a", 30, (200, 800, 880, 1300), 7, "chispas")],
             cam(1.0, 1.05, temblor=2), "corte", hud=[amarillo(0.05, d - 0.03, "GUERRAS", y=560, tam=120, color="#ff2d55")], sfx=[(0.1, "golpe", -14), (0.4, "zap", -20)])


@v.plano(45, "y la obra se paró casi cien años: la grúa quieta y los años corren")
def _(d):
    return P(TARDE, [BG("bg_plaza_tarde"), IMG("grua", ancho=700, x=760, y=900, z=0.4), torre(460, 1560, 480, [(0, 4)], "torre_3"),
             IMG("nube", ancho=500, z=0.3, keys=recorrido(v.w(45), v.w(64), (1300, 500), (-300, 560), d))],
             cam(1.0, 1.04, (540, 1150)), "corte", hud=[contador(0.05, d - 0.05, 0, 100, d * 0.7, "AÑOS", tam=120, y=560, borde=AMBAR, miles=False)],
             sfx=[(0.1, "subida", -22, {"dur": d * 0.7})])


@v.plano(52, "y eso la salvó")
def _(d):
    return P(CIELO, [BG("bg_plaza"), torre(540, 1560, 560, [(0, 4)], "torre_3"), brillo(540, 1300, 500, "#7dff3a", 0.3, 0.3, pulso=[0.2, 0.5])],
             cam(1.0, 1.05, (540, 1250)), "corte", hud=[rotulo(0.05, d - 0.05, "LA SALVÓ", tam=110, color="#141414", capsula="#7dff3ae6", y=480)], sfx=[(0.05, "ding", -20)])


@v.plano(56, "la tierra se fue apretando bajo su peso: flechas que aprietan el suelo")
def _(d):
    return P(TIERRA, [IMG("suelo_corte", ancho=1080, x=540, y=1420, z=0.4, keys=[{"t": 0, "ey": 1.0}, {"t": d, "ey": 0.93, "ease": "suave"}]),
             torre(540, 1010, 420, [(0, 4), (d, 4.2)], "torre_3"),
             *[flecha([[x, 760], [x, 960]], 0.1 + k * 0.12, 0.5 + k * 0.12, CIAN, 10, z=0.6) for k, x in enumerate((260, 540, 820))]],
             cam(1.0, 1.04, (540, 1150)), "corte", hud=[amarillo(0.05, d - 0.03, "SE APRIETA", y=560, tam=110, color=CIAN)], sfx=[(0.1, "rumor", -22, {"dur": d})])


@v.plano(64, "para disimular, pisos de arriba torcidos hacia el otro lado: la torre curva")
def _(d):
    return P(CIELO, [BG("bg_plaza"), torre(540, 1640, 440, [(0, 4.5)], "torre_curva"),
             flecha([[860, 800], [820, 660], [700, 580]], 0.2, d * 0.6, MAGENTA, 10, z=0.7), senala(600, 760, 0.3, d - 0.05, 170, MAGENTA)],
             cam(1.0, 1.08, (560, 900), (560, 800)), "corte", hud=[rotulo(0.05, d - 0.05, "PISOS TORCIDOS", tam=88, color="#ffffff", capsula="#c0392be6", y=480)],
             sfx=[(0.2, "roce", -20)])


@v.plano(78, "tardaron ciento noventa y nueve años: contador")
def _(d):
    return P(CIELO, [BG("bg_plaza"), torre(540, 1640, 440, [(0, 5)], "torre_pisa"), IMG("hoja_1372", ancho=320, x=880, y=1450, z=0.6, keys=aparece(d * 0.6, 0.3))],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[contador(0.05, d - 0.05, 0, 199, d * 0.6, "AÑOS", tam=130, y=560, borde=AMBAR, miles=False)],
             sfx=[(0.05, "subida", -20, {"dur": d * 0.6}), (d * 0.6, "ding", -20)])


@v.plano(86, "en 1990: hoja del calendario sobre la plaza")
def _(d):
    return P(TARDE, [BG("bg_plaza_tarde"), torre(780, 1560, 360, [(0, 5.5)]), IMG("hoja_1990", ancho=480, x=420, y=1050, z=0.55, keys=cae(0.0, 0.45, 500, 1050))],
             cam(1.0, 1.05), "corte", sfx=[(0.3, "golpe", -18)])


@v.plano(90, "se inclinaba cinco grados y medio: el arco del ángulo")
def _(d):
    return P(TARDE, [BG("bg_plaza_tarde"), torre(540, 1640, 440, [(0, 5.5)]), *arco_grados(540, 1640, 1000, 5.5, 0.1, d * 0.6)],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[rotulo(0.05, d - 0.05, "5,5 °", tam=140, color="#141414", capsula="#ffd23fe6", y=480)],
             sfx=[(0.1, "subida", -20, {"dur": d * 0.6})])


@v.plano(96, "y la cerraron: cinta delante de la torre")
def _(d):
    return P(TARDE, [BG("bg_plaza_tarde"), torre(540, 1640, 420, [(0, 5.5)]), IMG("cinta", ancho=1200, x=540, y=1450, z=0.7, keys=[{"t": 0, "x": -700}, {"t": d * 0.5, "x": 540, "ease": "salida"}])],
             cam(1.0, 1.04, (540, 1200)), "corte", hud=[rotulo(0.05, d - 0.05, "CERRADA", tam=120, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.1, "whoosh", -20), (d * 0.5, "golpe", -18)])


@v.plano(99, "¿cómo la salvaron?")
def _(d):
    return P(CIELO, [BG("bg_plaza"), torre(540, 1640, 440, [(0, 5.5)]), IMG("lupa", ancho=360, z=0.6, keys=[{"t": 0, "x": 300, "y": 1500}, {"t": d, "x": 520, "y": 1450, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1200)), "corte", hud=[rotulo(0.05, d - 0.05, "¿CÓMO?", tam=120, color="#141414", capsula="#ffd23fe6", y=480)], sfx=[(0.1, "roce", -20)])


@v.plano(102, "seiscientas toneladas de plomo en el lado alto: los lingotes caen junto a la base")
def _(d):
    return P(CIELO, [BG("bg_plaza"), torre(600, 1640, 420, [(0, 5.5), (d, 5.4)]),
             IMG("lingotes", ancho=420, x=330, z=0.6, keys=cae(0.1, 0.6, 900, 1520))],
             cam(1.0, 1.05, (540, 1250)), "corte", hud=[contador(0.05, d - 0.05, 0, 600, d * 0.6, "T DE PLOMO", tam=110, y=560, borde=CIAN, miles=False)],
             sfx=[(0.45, "golpe", -12)])


@v.plano(111, "luego, con taladros, sacaron tierra de debajo de ese lado: la barrena entra en el suelo")
def _(d):
    tierra_sale = [IMG("polvo_lunar", ancho=260, z=0.6, keys=lanza(0.3 + k * 0.2, 0.9 + k * 0.2, (360, 1300), (120 + k * 40, 800 + k * 60))) for k in range(4)]
    return P(TIERRA, [IMG("suelo_corte", ancho=1080, x=540, y=1420, z=0.4), torre(560, 1010, 260, [(0, 5.5)]),
             IMG("taladro", ancho=200, z=0.5, rot=-30, keys=[{"t": 0, "x": 120, "y": 900}, {"t": d * 0.7, "x": 300, "y": 1200, "ease": "suave"}]), *tierra_sale],
             cam(1.0, 1.04, (540, 1150)), "corte", hud=[amarillo(0.05, d - 0.03, "TALADROS", y=560, tam=120, color=AMBAR)],
             sfx=[(0.1, "rumor", -18, {"dur": d})])


@v.plano(121, "poquito a poco: granos de tierra que salen", mas=0.05)
def _(d):
    return P(TIERRA, [IMG("suelo_corte", ancho=2000, x=600, y=1000, z=0.4), polvo("#e8c88a", 50, (200, 700, 880, 1300), 31)],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "tic", -20), (0.2, "tic", -22)])


@v.plano(124, "la torre bajó y se enderezó unos cuarenta centímetros")
def _(d):
    return P(CIELO, [BG("bg_plaza"), torre(540, 1640, 440, [(0, 5.5), (d * 0.8, 4.0, "suave")]),
             IMG("lingotes", ancho=300, x=260, y=1530, z=0.6), flecha([[880, 500], [700, 470]], 0.2, d * 0.7, LIMA, 12, z=0.7)],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[contador(0.05, d - 0.05, 0, 40, d * 0.7, "CM", tam=130, y=560, borde=LIMA, miles=False)],
             sfx=[(0.1, "subida", -20, {"dur": d * 0.7}), (d * 0.8, "ding", -20)])


@v.plano(133, "volvió a abrir en dos mil uno: la gente vuelve")
def _(d):
    return P(CIELO, [BG("bg_plaza"), torre(760, 1560, 420, [(0, 4.0)]), IMG("hoja_2001", ancho=360, x=300, y=900, z=0.55, keys=aparece(0.05, 0.35)),
             IMG("personas_mirando", ancho=760, z=0.6, keys=[{"t": 0, "x": 200, "y": 1700}, {"t": d, "x": 420, "y": 1680, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1200)), "desenfoque", hud=[contexto(0.05, d - 0.05, "REABIERTA")], sfx=[(0.05, "pop", -20)])


@v.plano(141, "aguantará al menos doscientos años más")
def _(d):
    return P(TARDE, [BG("bg_plaza_tarde"), torre(540, 1640, 440, [(0, 4.0)]), brillo(540, 1000, 600, "#ffd27a", 0.35, 0.2, pulso=[0.1, 1.0]),
             IMG("nube", ancho=500, z=0.3, keys=recorrido(v.w(133), v.w(156) + 2, (1300, 450), (-300, 520), d))],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[contador(0.05, d - 0.05, 0, 200, d * 0.6, "AÑOS MÁS", tam=110, y=560, borde=AMBAR, miles=False, contar_prefijo="+")],
             sfx=[(0.05, "subida", -20, {"dur": d * 0.6})])


@v.plano(147, "eso sí: sigue torcida")
def _(d):
    return P(TARDE, [BG("bg_plaza_tarde"), torre(540, 1640, 440, [(0, 4.0)]), *arco_grados(540, 1640, 1000, 4.0, 0.05, d * 0.6, MAGENTA),
             IMG("nube", ancho=500, z=0.3, keys=recorrido(v.w(133), v.w(156) + 2, (1300, 450), (-300, 520), d))],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[amarillo(0.05, d - 0.03, "SIGUE TORCIDA", y=480, tam=100, color=MAGENTA)], sfx=[(0.05, "pop", -20)])


@v.plano(151, "y nadie quiere enderezarla del todo (bucle a la plaza)")
def _(d):
    return P(CIELO, [BG("bg_plaza"), torre(540, 1640, 440, [(0, 4.0), (d, 5.0, "suave")]), IMG("personas_mirando", ancho=760, x=420, y=1700, z=0.6),
             polvo("#ffffff", 20, (200, 1450, 880, 1600), 3)],
             cam(1.0, 1.0, (540, 1000), (540, 1000)), "desenfoque", hud=[rotulo(0.05, d - 0.4, "¿RECTA? NO", tam=110, color="#141414", capsula="#ffd23fe6", y=480)],
             sfx=[(0.1, "ding", -22)])


# ------------------------------------------------------------------ micro planos
@v.plano(3, "micro: la base de la torre cruje", mas=0.05)
def _(d):
    return P(CIELO, [torre(540, 2400, 1500, [(0, 5.5), (d, 6.0)]), polvo("#e8dcc8", 40, (100, 1300, 980, 1800), 5)], cam(1.0, 1.08, temblor=5), "corte", sfx=[(0.02, "golpe", -14)])


@v.plano(15, "micro: los primeros sillares", mas=0.05)
def _(d):
    return P(CIELO, [torre(540, 2600, 1600, [(0, 0)], "torre_3"), polvo("#e8dcc8", 30, (100, 900, 980, 1700), 9)], cam(1.0, 1.1, (540, 1200), (540, 1100)), "corte", sfx=[(0.02, "golpe", -20)])


@v.plano(43, "micro: choque de espadas", mas=0.05)
def _(d):
    return P(TARDE, [IMG("espadas", ancho=1500, x=540, y=1000, z=0.5, keys=[{"t": 0, "rot": -10}, {"t": d, "rot": 0, "ease": "elastico"}]), IMG("chispa", ancho=500, x=540, y=800, z=0.6, keys=aparece(0.0, 0.2))],
             cam(1.0, 1.08, temblor=6), "corte", sfx=[(0.02, "zap", -14)])


@v.plano(92, "micro: grados en grande", mas=0.05)
def _(d):
    return P(TARDE, [torre(540, 2300, 1300, [(0, 5.5)])], cam(1.0, 1.1, (540, 900)), "corte", sfx=[(0.02, "tic", -18)])


@v.plano(106, "micro: un lingote de plomo de cerca", mas=0.05)
def _(d):
    return P(CIELO, [IMG("lingotes", ancho=1400, x=540, y=1000, z=0.5, keys=[{"t": 0, "escala": 1.1}, {"t": d, "escala": 1.0, "ease": "salida"}])], cam(1.0, 1.06, temblor=3), "corte", sfx=[(0.02, "golpe", -14)])


@v.plano(138, "micro: la gente sube las escaleras", mas=0.05)
def _(d):
    return P(CIELO, [torre(540, 3200, 2200, [(0, 4.0)]), IMG("personas_mirando", ancho=1000, x=540, y=1700, z=0.6, anim={"flotar": [10, 0.5]})], cam(1.0, 1.08), "corte", sfx=[(0.02, "pop", -20)])


v.construir("2026-11-19-manana-03-torre-pisa", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 73, "db": -13},
            claves=["torre", "punto.", "Pisa,", "tres", "inclinaba.", "arena", "arcilla.", "guerras", "cien", "salvó:", "torcidos", "noventa", "cinco", "cerraron.",
                    "seiscientas", "plomo", "taladros,", "cuarenta", "doscientos", "torcida."])
