"""02 · El dólar no es americano — método denso. Vídeo extra 2026-11-19 (Nico, chat), tendencia «dólar hoy».
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]
La voz dura 61,6 s: se quita la frase «Así que, sea cual sea tu moneda, haz la prueba.» (palabras 138–147) para no pasar de 60 s."""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_extra2  # noqa: E402

SVG = ilus_extra2.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG, omitir=[(138, 148)] if len(VOZ) == 2 else ())

VERDE = ["#06180e", "#14402a"]
NOCHE = ["#040818", "#101c3a"]
MONTE = ["#2a3a5a", "#0c1810"]
MADERA = ["#3a2212", "#120a04"]
PUERTO = ["#3a2a5a", "#1a1430"]
AZUL = ["#0a1430", "#1a2a5a"]
ROJO = ["#3a0c08", "#7a2a14"]


def nube(d, a, b, y=520, ancho=420, op=0.4):
    ks = recorrido(v.w(a), v.w(b), (-300, y), (1380, y + 30), d)
    for k in ks: k["op"] = k["op"] * op
    return IMG("nube", ancho=ancho, z=0.2, keys=ks)


def gira_moneda(n, ancho, x, y, d, t0=0.0, z=0.5):
    """Moneda que entra girando sobre su eje vertical (ex de −1 a 1) y se asienta."""
    return IMG(n, ancho=ancho, x=x, y=y, z=z, keys=[{"t": t0, "ex": -1.0, "escala": 0.5, "op": 0}, {"t": t0 + 0.08, "op": 1}, {"t": t0 + 0.2, "ex": 0.1}, {"t": t0 + 0.4, "ex": 1.0, "escala": 1.05, "ease": "rebote"},
                                                      {"t": max(d, t0 + 0.5), "ex": 1.0, "escala": 1.0}])


# ================================================================== PLANOS
@v.plano(0, "gancho: un billete verde enorme entra girando hacia cámara")
def _(d):
    return P(VERDE, [brillo(540, 1050, 700, "#7fe08a", 0.45, 0.1, pulso=[0.2, 0.5]),
             IMG("billete", ancho=1020, z=0.5, keys=[{"t": 0, "x": 540, "y": 1350, "rot": -24, "escala": 0.8}, {"t": 0.4, "y": 1080, "rot": -6, "escala": 1.0, "ease": "elastico"}, {"t": d, "y": 1040, "rot": 4, "escala": 1.07, "ease": "suave"}]),
             polvo("#d8ffc8", 40, (100, 600, 980, 1500), 3, "chispas")],
             cam(1.0, 1.05, (540, 1060)), vineta=0.6, sfx=[(0.02, "whoosh", -12, {"dur": 0.6}), (0.4, "impacto", -15)])


@v.plano(2, "no es americano: la bandera ondea y el billete se va")
def _(d):
    return P(AZUL, [brillo(540, 900, 700, "#3f6ad8", 0.4, 0.1), IMG("bandera_eeuu", ancho=880, x=560, z=0.45, keys=[{"t": 0, "y": 1100, "rot": -3}, {"t": d, "y": 1060, "rot": 3, "ease": "suave"}]),
             IMG("billete", ancho=560, z=0.6, keys=[{"t": 0, "x": 540, "y": 1450, "rot": 4}, {"t": d, "x": 1300, "y": 1700, "rot": 40, "ease": "entrada"}])],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[rotulo(0.1, d - 0.05, "NO", tam=150, color="#ffffff", capsula="#c0392be6", y=540)], sfx=[(0.1, "golpe", -16)])


@v.plano(5, "nació en Europa: la moneda de plata entra girando")
def _(d):
    return P(NOCHE, [BG("bg_esp_petroleo"), tierra(540, 1900, 1500, 0.2, 2), gira_moneda("talero", 620, 540, 1000, d),
             brillo(540, 1000, 500, "#dfe8ff", 0.4, 0.3, pulso=[0.15, 0.6])],
             cam(1.0, 1.05), "corte", hud=[contexto(0.05, d - 0.05, "EUROPA")], sfx=[(0.05, "ding", -18)])


@v.plano(8, "micro: ¿dónde? la lupa busca", mas=0.05)
def _(d):
    return P(["#1a0a24", "#3a1a48"], [brillo(540, 1000, 520, "#ff3df2", 0.35, 0.1), IMG("lupa", ancho=560, z=0.5, keys=[{"t": 0, "x": 360, "y": 1200, "rot": -15}, {"t": d, "x": 700, "y": 1000, "rot": 10, "ease": "suave"}])],
             cam(1.0, 1.1), "corte", hud=[amarillo(0.0, d - 0.03, "¿DÓNDE?", y=560, tam=130, color=MAGENTA)], sfx=[(0.02, "pop", -18)])


@v.plano(9, "en un valle lleno de plata: el valle entre montañas, la bocamina brilla")
def _(d):
    return P(MONTE, [BG("bg_valle"), nube(d, 9, 36), brillo(860, 1660, 260, "#dfe8ff", 0.7, 0.3, pulso=[0.3, 0.4]),
             polvo("#f4f6fa", 40, (640, 1450, 1060, 1800), 5, "chispas")],
             cam(1.0, 1.18, (540, 1100), (760, 1500)), "desenfoque", sfx=[(0.1, "brillo", -18)])


@v.plano(15, "en mil quinientos veinte: cae la hoja del calendario", mas=0.05)
def _(d):
    return P(MONTE, [BG("bg_valle"), nube(d, 9, 36), IMG("hoja_1520", ancho=640, x=540, z=0.5, keys=cae(0.0, 0.42, 500, 1050))],
             cam(1.0, 1.05), "corte", sfx=[(0.3, "golpe", -18)])


@v.plano(19, "en Bohemia, hoy República Checa: el pueblo del valle al amanecer")
def _(d):
    return P(MONTE, [BG("bg_valle"), nube(d, 9, 36), senala(560, 1520, 0.2, d - 0.1, 190, AMBAR),
             polvo("#fff1c8", 30, (0, 900, 1080, 1700), 7)],
             cam(1.25, 1.35, (540, 1450), (560, 1500)), "corte", hud=[contexto(0.05, d - 0.05, "BOHEMIA · HOY REPÚBLICA CHECA")], sfx=[(0.2, "ding", -22)])


@v.plano(24, "abrieron una mina enorme: la vagoneta sale cargada de plata")
def _(d):
    return P(["#0a0c10", "#2a2018"], [brillo(540, 900, 600, "#ffd27a", 0.35, 0.08), IMG("vagoneta", ancho=820, z=0.5, keys=[{"t": 0, "x": 1300, "y": 1250, "ease": "salida"}, {"t": d * 0.6, "x": 560, "y": 1250}, {"t": d, "x": 520, "y": 1250}]),
             brillo(540, 1050, 300, "#f4f6fa", 0.6, 0.55, pulso=[0.4, 0.3]), polvo("#f4f6fa", 50, (200, 800, 880, 1300), 9, "chispas")],
             cam(1.0, 1.06, (540, 1200), temblor=1), "corte", hud=[amarillo(0.15, d - 0.03, "PLATA", y=560, tam=130, color=CIAN)], sfx=[(0.05, "rumor", -18, {"dur": 1.0}), (d * 0.6, "golpe", -16)])


@v.plano(28, "el lugar se llamaba valle de San Joaquín: vista del valle con su nombre")
def _(d):
    return P(MONTE, [BG("bg_valle"), nube(d, 9, 36), IMG("vagoneta", ancho=200, z=0.5, keys=[{"t": 0, "x": 860, "y": 1700, "ease": "lineal"}, {"t": d, "x": 520, "y": 1780}])],
             cam(1.1, 1.0, (600, 1300), (540, 1100)), "corte",
             hud=[rotulo(0.2, d - 0.05, "VALLE DE SAN JOAQUÍN", tam=72, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.2, "pop", -20)])


@v.plano(36, "micro: en alemán, la pluma sobre el pergamino", mas=0.05)
def _(d):
    return P(MADERA, [BG("bg_escritorio"), IMG("pergamino", ancho=820, x=540, y=1150, z=0.4, keys=[{"t": 0, "rot": -3}, {"t": d, "rot": -1}]),
             IMG("pluma", ancho=200, z=0.6, keys=[{"t": 0, "x": 420, "y": 900, "rot": 25}, {"t": d, "x": 700, "y": 980, "rot": 32, "ease": "suave"}])],
             cam(1.0, 1.08), "corte", hud=[contexto(0.02, d - 0.03, "EN ALEMÁN")], sfx=[(0.05, "roce", -18)])


@v.plano(38, "valle se dice tal: las dos palabras, una encima de otra")
def _(d):
    return P(MONTE, [BG("bg_valle"), {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#06101e", "x": 540, "y": 960, "z": 0.1, "keys": [{"t": 0, "op": 0.6}, {"t": d, "op": 0.6}]},
             flecha([[540, 760], [540, 980]], d * 0.3, d * 0.55, AMBAR, 12, z=0.6)],
             cam(1.0, 1.05), "corte",
             hud=[rotulo(0.05, d - 0.05, "VALLE", tam=130, color="#ffffff", capsula="#1a2a5ae6", y=640, fijo=True), rotulo(d * 0.5, d - 0.05, "TAL", tam=170, color="#141414", capsula="#ffd23fe6", y=1120, fijo=True)],
             sfx=[(0.05, "pop", -18), (d * 0.5, "ding", -16)])


@v.plano(42, "y a sus monedas las llamaron táleros: la moneda cae sobre el montón")
def _(d):
    return P(["#0a0c14", "#2a3040"], [brillo(540, 1000, 600, "#b8c0d0", 0.4, 0.1), IMG("monton_monedas", ancho=980, x=540, y=1500, z=0.4, keys=aparece(0.0, 0.3)),
             IMG("talero", ancho=560, x=540, z=0.55, keys=cae(0.1, 0.55, 300, 1020)), polvo("#f4f6fa", 40, (150, 600, 930, 1500), 11, "chispas")],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[amarillo(d * 0.45, d - 0.03, "TÁLEROS", y=560, tam=124, color=CIAN)], sfx=[(0.5, "ding", -14), (0.7, "ding", -22)])


@v.plano(49, "la palabra viajó y cambió: el galeón cruza el mar con la moneda")
def _(d):
    return P(PUERTO, [BG("bg_mar_tibio"), IMG("galeon", ancho=620, z=0.5, keys=[{"t": 0, "x": 160, "y": 1120, "ease": "lineal"}, {"t": d, "x": 600, "y": 1140}], anim={"balanceo": [2.5, 2.2], "flotar": [8, 1.8]}),
             IMG("talero", ancho=170, z=0.6, keys=[{"t": 0, "x": 300, "y": 700, "rot": 0, "ease": "lineal"}, {"t": d, "x": 760, "y": 660, "rot": 360}]),
             flecha([[160, 760], [460, 660], [820, 720]], 0.1, d * 0.8, AMBAR, 8, disc=[18, 14], z=0.4)],
             cam(1.0, 1.05, (540, 1000)), "desenfoque", sfx=[(0.1, "agua", -20, {"dur": 1.4})])


@v.plano(54, "micro: táler", mas=0.03)
def _(d):
    return P(["#0a0c14", "#2a3040"], [brillo(540, 1050, 500, "#b8c0d0", 0.4, 0.1), gira_moneda("talero", 640, 540, 1100, d)],
             cam(1.0, 1.08), "corte", hud=[rotulo(0.0, d - 0.03, "TÁLER", tam=130, color="#141414", capsula="#dfe4ece6", y=560, fijo=True)], sfx=[(0.02, "pop", -16)])


@v.plano(55, "micro: dáler, la moneda da otra vuelta", mas=0.03)
def _(d):
    return P(["#141008", "#3a2c14"], [brillo(540, 1050, 500, "#e8c890", 0.4, 0.1), gira_moneda("real_de_a_ocho", 640, 540, 1100, d)],
             cam(1.0, 1.08), "corte", hud=[rotulo(0.0, d - 0.03, "DÁLER", tam=130, color="#141414", capsula="#e8c890e6", y=560, fijo=True)], sfx=[(0.02, "pop", -15)])


@v.plano(56, "dólar: la moneda de oro con su símbolo")
def _(d):
    return P(VERDE, [brillo(540, 1050, 600, "#ffd23f", 0.5, 0.1, pulso=[0.2, 0.4]), gira_moneda("moneda_oro", 680, 540, 1100, d), polvo("#ffe07a", 50, (150, 600, 930, 1500), 13, "chispas")],
             cam(1.0, 1.08), "corte", hud=[rotulo(0.0, d - 0.03, "DÓLAR", tam=140, color="#141414", capsula="#ffd23fe6", y=560, fijo=True)], sfx=[(0.02, "impacto", -15), (0.3, "brillo", -18)])


@v.plano(57, "¿y cómo llegó a América? la Tierra gira y una flecha cruza el océano")
def _(d):
    return P(NOCHE, [BG("bg_esp_violeta"), tierra(540, 1150, 900, 0.4, 5), flecha([[760, 900], [540, 800], [300, 920]], 0.15, d * 0.7, AMBAR, 12, z=0.6),
             IMG("moneda_oro", ancho=150, z=0.65, keys=lanza(0.15, d * 0.75, (780, 900), (290, 930)))],
             cam(1.0, 1.06, (540, 1050)), "desenfoque", hud=[amarillo(0.05, d - 0.03, "¿Y AMÉRICA?", y=520, tam=110, color=CIAN)], sfx=[(0.15, "whoosh", -18, {"dur": 0.8})])


@v.plano(62, "por España: el galeón entra de golpe en primer plano", mas=0.05)
def _(d):
    return P(PUERTO, [BG("bg_mar_tibio"), IMG("galeon", ancho=980, z=0.5, keys=arranque(540, 1150, d, "derecha", 300, 40), anim={"balanceo": [2, 2.0]}), polvo("#ffe8c0", 30, (0, 1300, 1080, 1850), 15)],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[rotulo(0.05, d - 0.05, "ESPAÑA", tam=120, color="#141414", capsula="#ffd23fe6", y=540)], sfx=[(0.02, "agua", -16, {"dur": 0.9})])


@v.plano(64, "su moneda de plata, el real de a ocho: la moneda con las dos columnas y el 8")
def _(d):
    return P(["#141008", "#3a2c14"], [brillo(540, 1050, 640, "#e8c890", 0.45, 0.1, pulso=[0.15, 0.7]), gira_moneda("real_de_a_ocho", 820, 540, 1100, d),
             senala(540, 1090, d * 0.5, d - 0.1, 120, AMBAR), polvo("#f4f6fa", 40, (150, 600, 930, 1550), 17, "chispas")],
             cam(1.0, 1.08, (540, 1100)), "corte", hud=[rotulo(d * 0.3, d - 0.05, "REAL DE A OCHO", tam=86, color="#141414", capsula="#ffd23fe6", y=540)], sfx=[(0.05, "ding", -16), (d * 0.5, "pop", -20)])


@v.plano(72, "micro: el ocho de la moneda, muy de cerca", mas=0.03)
def _(d):
    return P(["#141008", "#3a2c14"], [IMG("real_de_a_ocho", ancho=1700, x=540, y=1010, z=0.5, keys=[{"t": 0, "escala": 0.9}, {"t": d, "escala": 1.02, "ease": "salida"}]),
             senala(540, 985, 0.0, d - 0.05, 190, AMBAR), polvo("#f4f6fa", 30, (100, 500, 980, 1500), 31, "chispas")],
             cam(1.0, 1.06, (540, 1000)), "corte", sfx=[(0.02, "ding", -18)])


@v.plano(73, "se usaba en medio mundo: las monedas salen disparadas alrededor de la Tierra")
def _(d):
    dest = [(180, 620), (900, 600), (160, 1500), (920, 1480), (540, 480), (540, 1640)]
    return P(NOCHE, [BG("bg_esp_petroleo"), tierra(540, 1050, 760, 0.4, 6),
             *[IMG("real_de_a_ocho", ancho=170, z=0.6, keys=lanza(0.05 + k * 0.07, 0.55 + k * 0.07, (540, 1050), p), anim={"girar": 60}) for k, p in enumerate(dest)]],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[amarillo(0.2, d - 0.03, "MEDIO MUNDO", y=540, tam=96, color=LIMA)], sfx=[(0.05 + k * 0.07, "pop", -22) for k in range(6)])


@v.plano(78, "los colonos ingleses: el colono con tricornio en el puerto")
def _(d):
    return P(PUERTO, [BG("bg_puerto"), IMG("galeon", ancho=300, x=260, y=1010, z=0.3, anim={"balanceo": [2, 2.4]}),
             IMG("tricornio", ancho=560, z=0.5, keys=[{"t": 0, "x": 760, "y": 1380, "escala": 0.94}, {"t": 0.3, "escala": 1.0, "ease": "rebote"}, {"t": d, "x": 740, "y": 1370}])],
             cam(1.0, 1.05, (600, 1250)), "corte", hud=[contexto(0.05, d - 0.05, "COLONOS")], sfx=[(0.1, "agua", -24, {"dur": 0.9})])


@v.plano(82, "la llamaban dólar español: la moneda sobre la mano del colono, con su apodo")
def _(d):
    return P(PUERTO, [BG("bg_puerto"), IMG("tricornio", ancho=560, x=800, y=1420, z=0.4), IMG("real_de_a_ocho", ancho=420, z=0.55, keys=[{"t": 0, "x": 380, "y": 1300, "escala": 0.6, "rot": -20}, {"t": 0.35, "y": 1150, "escala": 1.0, "rot": 0, "ease": "rebote"}, {"t": d, "y": 1130, "rot": 8}]),
             brillo(380, 1150, 320, "#f4f6fa", 0.5, 0.3, pulso=[0.2, 0.5])],
             cam(1.0, 1.06, (480, 1200)), "corte", hud=[rotulo(0.15, d - 0.05, "«DÓLAR ESPAÑOL»", tam=82, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.3, "ding", -18)])


@v.plano(85, "cuando nació Estados Unidos: la bandera sube")
def _(d):
    return P(AZUL, [brillo(540, 900, 700, "#3f6ad8", 0.4, 0.1), IMG("bandera_eeuu", ancho=900, x=560, z=0.5, keys=[{"t": 0, "y": 1700}, {"t": 0.5, "y": 1080, "ease": "rebote"}, {"t": d, "y": 1050, "rot": 2}]),
             polvo("#ffffff", 40, (0, 300, 1080, 1700), 19, "estrellas")],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[contexto(0.1, d - 0.05, "NACE ESTADOS UNIDOS")], sfx=[(0.05, "subida", -18, {"dur": 0.6}), (0.5, "golpe", -18)])


@v.plano(89, "copió esa moneda: del real de a ocho sale una copia")
def _(d):
    return P(AZUL, [brillo(540, 1050, 700, "#3f6ad8", 0.3, 0.1), IMG("real_de_a_ocho", ancho=420, x=290, y=1100, z=0.5, anim={"pulso": [0.03, 0.6]}),
             flecha([[480, 1100], [640, 1100]], 0.1, d * 0.45, AMBAR, 14, z=0.6),
             IMG("real_de_a_ocho", ancho=420, z=0.5, keys=[{"t": 0, "x": 290, "y": 1100, "op": 0}, {"t": d * 0.3, "op": 0.4}, {"t": d * 0.6, "x": 800, "op": 0}]),
             IMG("moneda_oro", ancho=420, z=0.55, keys=[{"t": d * 0.4, "x": 800, "y": 1100, "op": 0, "escala": 0.6}, {"t": d * 0.6, "op": 1, "escala": 1.08, "ease": "rebote"}, {"t": d, "escala": 1.0}])],
             cam(1.0, 1.05), "corte", hud=[amarillo(d * 0.45, d - 0.03, "COPIA", y=560, tam=124, color=AMBAR)], sfx=[(d * 0.5, "pop", -16)])


@v.plano(92, "y la española siguió siendo legal allí: la moneda española delante de la bandera")
def _(d):
    return P(AZUL, [IMG("bandera_eeuu", ancho=1300, x=640, y=1000, z=0.2, op=0.45), IMG("real_de_a_ocho", ancho=620, x=540, z=0.5, keys=[{"t": 0, "y": 1130, "rot": -6}, {"t": d, "y": 1100, "rot": 6, "ease": "suave"}]),
             brillo(540, 1100, 460, "#b6ff5a", 0.35, 0.3, pulso=[0.2, 0.5])],
             cam(1.0, 1.06, (540, 1080)), "corte", hud=[rotulo(d * 0.35, d - 0.05, "LEGAL", tam=130, color="#141414", capsula="#b6ff5ae6", y=540)], sfx=[(d * 0.35, "ding", -16)])


@v.plano(98, "micro: allí, la bandera a pantalla completa", mas=0.03)
def _(d):
    return P(AZUL, [IMG("bandera_eeuu", ancho=1700, x=760, y=1150, z=0.4, keys=[{"t": 0, "rot": -2, "escala": 1.0}, {"t": d, "rot": 2, "escala": 1.06}]), polvo("#ffffff", 30, (0, 300, 1080, 1700), 33, "estrellas")],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "roce", -18)])


@v.plano(99, "hasta mil ochocientos cincuenta y siete: cae la hoja y la moneda se retira")
def _(d):
    return P(AZUL, [IMG("bandera_eeuu", ancho=1300, x=640, y=1000, z=0.2, op=0.3), IMG("hoja_1857", ancho=640, x=540, z=0.5, keys=cae(0.0, 0.45, 400, 1000)),
             IMG("real_de_a_ocho", ancho=260, z=0.6, keys=[{"t": d * 0.4, "x": 540, "y": 1500, "rot": 0, "ease": "entrada"}, {"t": d, "x": 1250, "y": 1560, "rot": 300}])],
             cam(1.0, 1.05), "corte", sfx=[(0.3, "golpe", -18), (d * 0.5, "roce", -20)])


@v.plano(105, "¿y el símbolo? el signo dorado late")
def _(d):
    return P(VERDE, [brillo(540, 1050, 640, "#ffd23f", 0.45, 0.1, pulso=[0.25, 0.4]), IMG("signo_peso", ancho=900, x=540, y=1080, z=0.5, keys=late(0.05, 2, 0.12, 0.35)),
             polvo("#ffe07a", 40, (150, 600, 930, 1500), 21, "chispas")],
             cam(1.0, 1.08), "corte", hud=[amarillo(0.05, d - 0.03, "¿Y ESTO?", y=520, tam=110, color="#ffffff")], sfx=[(0.02, "pop", -16)])


@v.plano(108, "la teoría más aceptada dice: la lupa recorre un manuscrito antiguo")
def _(d):
    return P(MADERA, [BG("bg_escritorio"), IMG("pergamino", ancho=860, x=540, y=1150, z=0.4, keys=[{"t": 0, "rot": 2}, {"t": d, "rot": 0}]),
             IMG("lupa", ancho=420, z=0.6, keys=[{"t": 0, "x": 320, "y": 900}, {"t": d, "x": 720, "y": 1300, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1100)), "desenfoque", hud=[contexto(0.05, d - 0.05, "LA TEORÍA MÁS ACEPTADA")], sfx=[(0.1, "roce", -20)])


@v.plano(113, "que viene de la palabra pesos: la palabra escrita en el pergamino")
def _(d):
    return P(MADERA, [BG("bg_escritorio"), IMG("pergamino_vacio", ancho=900, x=540, y=1150, z=0.4),
             IMG("pluma", ancho=190, z=0.6, keys=[{"t": 0, "x": 300, "y": 1000, "rot": 25, "ease": "lineal"}, {"t": d * 0.7, "x": 840, "y": 1020, "rot": 30}, {"t": d, "x": 880, "y": 980}])],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[rotulo(0.15, d - 0.05, "PESOS", tam=170, color="#2a1808", capsula=None, y=1150, rot=-4, fijo=True, sin_pop=True)], sfx=[(0.1, "trazo", -18), (0.4, "trazo", -18), (0.7, "trazo", -18)])


@v.plano(119, "se abreviaba con: la pluma se acerca al pergamino en blanco")
def _(d):
    return P(MADERA, [BG("bg_escritorio"), IMG("pergamino_vacio", ancho=980, x=540, y=1150, z=0.4, keys=[{"t": 0, "rot": 3}, {"t": d, "rot": 0, "ease": "suave"}]),
             IMG("pluma", ancho=200, z=0.6, keys=[{"t": 0, "x": 860, "y": 620, "rot": 40}, {"t": d, "x": 380, "y": 880, "rot": 25, "ease": "suave"}]),
             polvo("#ffd27a", 24, (100, 500, 980, 1600), 35)],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[contexto(0.05, d - 0.05, "SE ABREVIABA")], sfx=[(0.1, "roce", -20)])


@v.plano(123, "micro: una pe", mas=0.03)
def _(d):
    return P(MADERA, [BG("bg_escritorio"), IMG("pergamino_vacio", ancho=1300, x=540, y=1150, z=0.4), IMG("letra_p", ancho=820, x=540, y=1120, z=0.55, keys=[{"t": 0, "escala": 0.6}, {"t": 0.2, "escala": 1.05, "ease": "rebote"}, {"t": d, "escala": 1.0}]),
             IMG("pluma", ancho=170, x=860, y=760, z=0.6, rot=30)],
             cam(1.0, 1.06, (540, 1100)), "corte", sfx=[(0.02, "pop", -15)])


@v.plano(124, "micro: y una… la pluma salta al otro lado", mas=0.03)
def _(d):
    return P(MADERA, [BG("bg_escritorio"), IMG("pergamino_vacio", ancho=1300, x=540, y=1150, z=0.4), IMG("letra_p", ancho=460, x=360, y=1120, z=0.55),
             IMG("pluma", ancho=200, z=0.6, keys=[{"t": 0, "x": 460, "y": 820, "rot": 25}, {"t": d, "x": 780, "y": 860, "rot": 32, "ease": "salida"}])],
             cam(1.0, 1.04, (540, 1100)), "corte", sfx=[(0.02, "roce", -18)])


@v.plano(126, "micro: una ese", mas=0.03)
def _(d):
    return P(MADERA, [BG("bg_escritorio"), IMG("pergamino_vacio", ancho=1300, x=540, y=1150, z=0.4), IMG("letra_s", ancho=820, x=540, y=1120, z=0.55, keys=[{"t": 0, "escala": 0.6}, {"t": 0.2, "escala": 1.05, "ease": "rebote"}, {"t": d, "escala": 1.0}]),
             IMG("pluma", ancho=170, x=220, y=760, z=0.6, rot=20)],
             cam(1.0, 1.06, (540, 1100)), "corte", sfx=[(0.02, "pop", -14)])


@v.plano(127, "micro: con las prisas, la pluma corre", mas=0.05)
def _(d):
    return P(MADERA, [BG("bg_escritorio"), IMG("pergamino", ancho=980, x=540, y=1150, z=0.4), IMG("pluma", ancho=260, z=0.6, keys=[{"t": 0, "x": 200, "y": 1000, "rot": 20, "ease": "lineal"}, {"t": d, "x": 950, "y": 1250, "rot": 40}]),
             *lineas_vel(500, 1100, 5, "#ffd27aaa")],
             cam(1.0, 1.1, temblor=2), "corte", hud=[amarillo(0.02, d - 0.03, "CON PRISAS", y=560, tam=100, color=AMBAR)], sfx=[(0.02, "whoosh", -16, {"dur": 0.6})])


@v.plano(130, "las dos letras se montaron una sobre otra: la p y la s se juntan y sale el símbolo")
def _(d):
    return P(MADERA, [BG("bg_escritorio"), IMG("pergamino_vacio", ancho=980, x=540, y=1150, z=0.4),
             IMG("letra_p", ancho=460, y=1120, z=0.55, keys=[{"t": 0, "x": 360, "op": 1}, {"t": d * 0.5, "x": 540, "ease": "suave"}, {"t": d * 0.62, "op": 1}, {"t": d * 0.75, "op": 0}]),
             IMG("letra_s", ancho=460, y=1120, z=0.56, keys=[{"t": 0, "x": 720, "op": 1}, {"t": d * 0.5, "x": 540, "ease": "suave"}, {"t": d * 0.62, "op": 1}, {"t": d * 0.75, "op": 0}]),
             IMG("signo_peso_tinta", ancho=560, x=540, y=1120, z=0.6, keys=[{"t": d * 0.6, "op": 0, "escala": 0.9}, {"t": d * 0.75, "op": 1, "escala": 1.1, "ease": "rebote"}, {"t": d, "escala": 1.0}]),
             flecha([[300, 860], [460, 860]], 0.05, d * 0.4, AMBAR, 10, z=0.7), flecha([[780, 860], [620, 860]], 0.05, d * 0.4, AMBAR, 10, z=0.7)],
             cam(1.0, 1.08, (540, 1100)), "corte", sfx=[(0.1, "roce", -18), (d * 0.62, "impacto", -14)])


@v.plano(148, "cada vez que escribes ese símbolo: una mano… el signo dorado sobre billetes y monedas")
def _(d):
    return P(VERDE, [brillo(540, 1050, 700, "#ffd23f", 0.45, 0.1, pulso=[0.2, 0.5]), IMG("billete", ancho=760, x=540, y=1560, z=0.3, keys=[{"t": 0, "rot": -8}, {"t": d, "rot": -4}]),
             IMG("moneda_oro", ancho=240, x=200, y=760, z=0.35, anim={"flotar": [14, 1.6]}), IMG("real_de_a_ocho", ancho=240, x=880, y=780, z=0.35, anim={"flotar": [14, 1.9]}),
             IMG("signo_peso", ancho=760, x=540, z=0.5, keys=[{"t": 0, "y": 1150, "escala": 0.9}, {"t": 0.35, "y": 1080, "escala": 1.0, "ease": "rebote"}, {"t": d, "y": 1060, "escala": 1.05}])],
             cam(1.0, 1.05, (540, 1080)), "desenfoque", sfx=[(0.05, "brillo", -18)])


@v.plano(154, "estás escribiendo pesos: el billete vuelve a entrar con la palabra (bucle)")
def _(d):
    return P(VERDE, [brillo(540, 1050, 700, "#7fe08a", 0.45, 0.1, pulso=[0.2, 0.5]),
             IMG("billete", ancho=1020, z=0.5, keys=[{"t": 0, "x": 540, "y": 1400, "rot": -20, "escala": 0.85}, {"t": 0.45, "y": 1100, "rot": -5, "escala": 1.0, "ease": "rebote"}, {"t": d, "y": 1060, "rot": 3, "escala": 1.05}]),
             polvo("#d8ffc8", 40, (100, 600, 980, 1500), 3, "chispas")],
             cam(1.0, 1.04, (540, 1060)), "corte", hud=[rotulo(0.15, d - 0.4, "PESOS", tam=150, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "impacto", -15), (d * 0.6, "ding", -22)])


v.construir("2026-11-19-extra-02-dolar", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 23, "db": -13},
            claves=["dólar", "americano", "Europa", "plata", "Bohemia", "mina", "Joaquín", "tal", "táleros", "táler", "dáler", "América", "España", "ocho",
                    "español", "Unidos", "copió", "legal", "símbolo", "pesos", "pe", "ese", "letras"])
