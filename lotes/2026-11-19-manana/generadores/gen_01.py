"""01 · El espacio huele a filete — método denso. Lote 2026-11-19-manana, Agente 08:00 (Nico).
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_hoy  # noqa: E402

SVG = ilus_hoy.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

ESP = ["#02030a", "#0a1030"]
OSC = ["#0a0c1a", "#1a2040"]
CAL = ["#2a1408", "#5a2a14"]
RT = (1150, 380), (-150, 640)   # satélite que cruza el tramo de la órbita


def sat(d, a=5, b=36):
    return IMG("satelite", ancho=150, z=0.25, keys=recorrido(v.w(a), v.w(b), *RT, d), anim={"girar": 5})


# ================================================================== PLANOS
@v.plano(0, "gancho: el casco sube hacia cámara y le sale olor a filete")
def _(d):
    return P(ESP, [BG("bg_orbita"), IMG("casco", ancho=820, z=0.5, keys=arranque(540, 1150, d)),
             IMG("olor", ancho=420, x=540, z=0.6, keys=[{"t": 0, "y": 900, "op": 0.0, "ey": 0.6}, {"t": 0.3, "op": 1}, {"t": d, "y": 560, "ey": 1.1, "ease": "suave"}]),
             brillo(540, 700, 380, "#ffb46a", 0.35, 0.45, pulso=[0.15, 0.6])],
             cam(1.0, 1.04, (540, 1000), (540, 940)), vineta=0.6, sfx=[(0.02, "whoosh", -12, {"dur": 0.6}), (0.5, "brillo", -18)])


@v.plano(3, "micro: el filete chisporrotea", mas=0.05)
def _(d):
    return P(CAL, [IMG("filete", ancho=1300, z=0.5, keys=[{"t": 0, "x": 540, "y": 1050, "escala": 1.08}, {"t": d, "escala": 1.0, "ease": "salida"}]),
             polvo("#ffd27a", 50, (100, 600, 980, 1200), 3, "chispas")], cam(1.0, 1.08, temblor=2), "corte", sfx=[(0.02, "zap", -18)])


@v.plano(5, "lo cuentan los astronautas: astronauta junto a la estación")
def _(d):
    return P(ESP, [BG("bg_orbita"), IMG("iss", ancho=900, x=540, y=650, z=0.3, anim={"flotar": [8, 4]}), sat(d),
             IMG("astronauta", ancho=440, x=520, y=1150, z=0.5, anim={"flotar": [16, 2.4], "balanceo": [6, 3]})],
             cam(1.0, 1.05, (540, 1000)), "desenfoque", hud=[contexto(0.05, d - 0.05, "ASTRONAUTAS")], sfx=[(0.1, "senal", -22)])


@v.plano(9, "cuando vuelven de un paseo espacial: el astronauta vuelve a la estación")
def _(d):
    return P(ESP, [BG("bg_orbita"), sat(d), IMG("iss", ancho=1100, x=600, y=700, z=0.3),
             IMG("astronauta", ancho=380, z=0.5, keys=[{"t": 0, "x": 200, "y": 1400, "rot": -10}, {"t": d, "x": 520, "y": 1000, "rot": 5, "ease": "suave"}]),
             flecha([[150, 1500], [420, 1120]], 0.1, d * 0.6, CIAN, 8, z=0.45)],
             cam(1.0, 1.06, (500, 1100), (540, 950)), "corte", sfx=[(0.1, "roce", -20)])


@v.plano(13, "micro: el guante agarra la barandilla", mas=0.05)
def _(d):
    return P(ESP, [BG("bg_orbita"), IMG("guante", ancho=900, z=0.5, keys=[{"t": 0, "x": 520, "y": 1300, "rot": -8}, {"t": d, "x": 540, "y": 1100, "rot": 0, "ease": "salida"}])],
             cam(1.0, 1.08), "corte", sfx=[(0.05, "golpe", -20)])


@v.plano(16, "se quitan el casco: el casco sube y sale vapor")
def _(d):
    return P(OSC, [BG("bg_lab"), IMG("astronauta", ancho=620, x=540, y=1250, z=0.45),
             IMG("casco", ancho=360, z=0.55, keys=[{"t": 0, "x": 540, "y": 860}, {"t": d * 0.6, "x": 620, "y": 520, "rot": 12, "ease": "anticipa"}, {"t": d, "x": 640, "y": 500, "rot": 14}]),
             IMG("olor_gris", ancho=360, x=520, z=0.6, keys=[{"t": d * 0.4, "y": 900, "op": 0}, {"t": d * 0.6, "op": 0.9}, {"t": d, "y": 700}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[amarillo(0.05, d - 0.05, "FUERA CASCO", y=560, tam=100, color=CIAN)], sfx=[(d * 0.4, "zap", -20)])


@v.plano(20, "el traje trae un olor: ondas que suben del guante")
def _(d):
    return P(OSC, [BG("bg_lab"), IMG("guante", ancho=600, x=540, y=1250, z=0.5, anim={"balanceo": [3, 1.4]}),
             IMG("olor", ancho=520, x=540, z=0.6, keys=[{"t": 0, "y": 950, "op": 0, "ey": 0.5}, {"t": 0.3, "op": 1}, {"t": d, "y": 720, "ey": 1.1, "ease": "suave"}]),
             polvo("#ffb46a", 30, (250, 500, 830, 1100), 7)],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "OLOR", y=480, tam=120, color=AMBAR)], sfx=[(0.1, "roce", -20)])


@v.plano(25, "micro: un signo de interrogación (¿raro?)", mas=0.05)
def _(d):
    return P(["#1a0a24", "#3a1a48"], [brillo(540, 960, 500, "#ff3df2", 0.35, 0.1), IMG("olor_rosa", ancho=700, x=540, y=1000, z=0.5, keys=late(0.0, 1, 0.12, 0.3))],
             cam(1.0, 1.1), "corte", hud=[amarillo(0.0, d - 0.03, "¿RARO?", y=560, tam=130, color=MAGENTA)], sfx=[(0.02, "pop", -18)])


@v.plano(27, "carne a la plancha: el filete en la parrilla")
def _(d):
    return P(CAL, [BG("bg_cocina"), brillo(540, 1200, 500, "#ff7a3a", 0.4, 0.3, pulso=[0.2, 0.4]),
             IMG("filete", ancho=880, x=540, z=0.5, keys=cae(0.0, 0.5, 700, 1200)),
             IMG("olor", ancho=420, x=540, z=0.6, keys=[{"t": 0.4, "y": 1000, "op": 0}, {"t": 0.6, "op": 1}, {"t": d, "y": 800}]),
             polvo("#ffd27a", 40, (200, 900, 880, 1300), 9, "chispas")],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[rotulo(0.05, d - 0.05, "CARNE A LA PLANCHA", tam=78, color="#141414", capsula="#ffd23fe6", y=560)],
             sfx=[(0.35, "golpe", -16), (0.5, "agua", -26, {"dur": 0.9})])


@v.plano(33, "metal caliente: chispas y una barra al rojo")
def _(d):
    barra = {"tipo": "forma", "forma": "redondeado", "ancho": 760, "alto": 120, "relleno": "#ff5a1e", "x": 540, "y": 1150, "z": 0.5,
             "keys": [{"t": 0, "op": 0.5}, {"t": d * 0.5, "op": 1, "ease": "salida"}]}
    return P(["#0c0806", "#2a0c04"], [brillo(540, 1150, 520, "#ff7a1e", 0.6, 0.3, pulso=[0.15, 0.3]), barra, IMG("chispa", ancho=500, x=540, y=1150, z=0.6, anim={"pulso": [0.2, 0.25]}), polvo("#ffd27a", 60, (150, 900, 930, 1300), 11, "chispas")],
             cam(1.0, 1.06, temblor=2), "corte", hud=[rotulo(0.05, d - 0.05, "METAL CALIENTE", tam=88, color="#ffffff", capsula="#c0392be6", y=560)],
             sfx=[(0.05, "zap", -16)])


@v.plano(36, "el astronauta Don Pettit")
def _(d):
    return P(ESP, [BG("bg_esp_violeta"), tierra(860, 1700, 760, 0.2, 3), sat(d, 36, 60),
             IMG("astronauta", ancho=520, x=480, y=1050, z=0.5, keys=[{"t": 0, "rot": -6}, {"t": d, "rot": 6, "ease": "suave"}], anim={"flotar": [14, 2.2]})],
             cam(1.0, 1.06, (540, 1000)), "desenfoque", hud=[contexto(0.05, d - 0.05, "DON PETTIT · NASA")], sfx=[(0.1, "senal", -22)])


@v.plano(42, "con el humo de soldar: el soplete enciende el arco")
def _(d):
    return P(["#05080e", "#101a28"], [IMG("soldador", ancho=1100, x=560, y=1050, z=0.5, keys=[{"t": 0, "escala": 0.95}, {"t": d, "escala": 1.03}]),
             brillo(310, 1100, 300, "#bff6ff", 0.7, 0.55, pulso=[0.35, 0.12]), polvo("#ffd27a", 60, (100, 700, 600, 1200), 13, "chispas"),
             IMG("olor_gris", ancho=360, x=320, z=0.6, keys=[{"t": 0, "y": 950, "op": 0}, {"t": 0.4, "op": 0.8}, {"t": d, "y": 650}])],
             cam(1.0, 1.06, (480, 1050), temblor=1), "corte", hud=[amarillo(0.05, d - 0.03, "HUMO DE SOLDAR", y=560, tam=96, color=CIAN)],
             sfx=[(0.05, "zap", -16), (0.4, "zap", -20)])


@v.plano(47, "un olor metálico")
def _(d):
    return P(["#0a0c14", "#2a3040"], [brillo(540, 1000, 500, "#b8c0d0", 0.4, 0.2), IMG("lingotes", ancho=900, x=540, y=1150, z=0.5, keys=aparece(0.0, 0.35)),
             IMG("olor_gris", ancho=420, x=540, z=0.6, keys=[{"t": 0.1, "y": 950, "op": 0}, {"t": 0.4, "op": 0.9}, {"t": d, "y": 760}])],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "METÁLICO", y=560, tam=120, color=CIAN)], sfx=[(0.05, "ding", -22)])


@v.plano(50, "y dulce: un caramelo de olor rosa", mas=0.05)
def _(d):
    return P(["#1a0a24", "#3a1a48"], [IMG("olor_rosa", ancho=800, x=540, y=1000, z=0.5, keys=late(0.0, 1, 0.1, 0.35)), polvo("#ffc8e0", 40, (100, 500, 980, 1500), 15, "chispas")],
             cam(1.0, 1.08), "corte", hud=[amarillo(0.0, d - 0.03, "Y DULCE", y=560, tam=120, color=MAGENTA)], sfx=[(0.02, "brillo", -20)])


@v.plano(52, "¿y de dónde sale? la lupa recorre el traje")
def _(d):
    return P(OSC, [BG("bg_lab"), IMG("astronauta", ancho=640, x=540, y=1150, z=0.45),
             IMG("lupa", ancho=380, z=0.6, keys=[{"t": 0, "x": 380, "y": 1300}, {"t": d, "x": 640, "y": 900, "ease": "suave"}])],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "¿DE DÓNDE?", y=560, tam=120, color=AMBAR)], sfx=[(0.1, "roce", -20)])


@v.plano(56, "fuera no hay aire: la estación lejos en el vacío")
def _(d):
    return P(ESP, [BG("bg_esp_petroleo"), tierra(540, 2000, 1500, 0.2, 2), IMG("iss", ancho=520, x=540, y=900, z=0.4, anim={"flotar": [6, 3]}),
             fugaz(0.2, 900, 300, 500, 520)],
             cam(1.0, 0.94, (540, 960)), "desenfoque", hud=[rotulo(0.05, d - 0.05, "SIN AIRE", tam=110, color="#ffffff", capsula="#1a2040e6", y=560)],
             sfx=[(0.1, "rumor", -24, {"dur": d})])


@v.plano(60, "pero sí hay oxígeno suelto: átomos rojos que flotan")
def _(d):
    at = [IMG("oxigeno", ancho=a, x=x, y=y, z=0.5, keys=aparece(0.05 + k * 0.1, 0.35), anim={"flotar": [14, 1.5 + k * 0.3]})
          for k, (x, y, a) in enumerate([(300, 800, 220), (720, 700, 180), (540, 1150, 260), (220, 1350, 160), (850, 1250, 200)])]
    return P(ESP, [BG("bg_esp_violeta"), *at], cam(1.0, 1.05), "corte",
             hud=[amarillo(0.05, d - 0.03, "OXÍGENO", y=560, tam=120, color=MAGENTA)], sfx=[(0.05 + k * 0.1, "pop", -22) for k in range(5)])


@v.plano(65, "micro: átomo a átomo", mas=0.05)
def _(d):
    return P(ESP, [brillo(540, 1000, 420, "#ff3d3d", 0.4, 0.2), IMG("oxigeno", ancho=700, x=540, y=1000, z=0.5, keys=late(0.0, 2, 0.12, 0.3))],
             cam(1.0, 1.1), "corte", sfx=[(0.02, "pop", -16)])


@v.plano(68, "una explicación posible: se pega al traje (los átomos vuelan al guante)")
def _(d):
    at = [IMG("oxigeno", ancho=120, z=0.6, keys=lanza(0.05 + k * 0.12, d * 0.7 + k * 0.05, p, (480 + (k % 3) * 60, 1000 + (k // 3) * 90)))
          for k, p in enumerate([(100, 500), (1000, 600), (80, 1500), (1000, 1450), (540, 300), (900, 1000)])]
    return P(ESP, [BG("bg_esp_violeta"), IMG("guante", ancho=640, x=540, y=1100, z=0.5), *at],
             cam(1.0, 1.04), "corte", hud=[contexto(0.05, d - 0.05, "EXPLICACIÓN POSIBLE")], sfx=[(0.3, "burbuja", -20), (0.6, "burbuja", -20)])


@v.plano(75, "y al entrar reacciona: chispazos en el guante dentro de la estación")
def _(d):
    return P(OSC, [BG("bg_lab"), IMG("guante", ancho=640, x=540, y=1150, z=0.5),
             *[IMG("chispa", ancho=200, x=x, y=y, z=0.6, keys=[{"t": t, "escala": 0, "op": 0}, {"t": t + 0.08, "escala": 1.2, "op": 1}, {"t": t + 0.35, "escala": 0.4, "op": 0}])
               for t, x, y in [(0.1, 460, 950), (0.35, 640, 1050), (0.6, 520, 1200), (0.85, 600, 900)]],
             IMG("olor", ancho=420, x=540, z=0.65, keys=[{"t": 0.3, "y": 950, "op": 0}, {"t": 0.6, "op": 1}, {"t": d, "y": 720}])],
             cam(1.0, 1.05, temblor=1), "corte", hud=[amarillo(0.05, d - 0.03, "REACCIONA", y=560, tam=110, color=LIMA)],
             sfx=[(0.1, "zap", -20), (0.6, "zap", -22)])


@v.plano(79, "en dos mil ocho: la hoja del calendario")
def _(d):
    return P(OSC, [BG("bg_lab"), IMG("hoja_2008", ancho=560, x=540, y=1000, z=0.5, keys=cae(0.0, 0.45, 600, 1000))],
             cam(1.0, 1.05), "corte", sfx=[(0.3, "golpe", -18)])


@v.plano(84, "la NASA encargó a un químico: silueta con matraz")
def _(d):
    return P(["#0d1a1a", "#1a3a3a"], [BG("bg_lab"), IMG("sil", ancho=700, x=330, y=1250, z=0.45),
             IMG("matraz", ancho=420, x=760, y=1250, z=0.55, keys=late(0.2, 1, 0.08, 0.4)), polvo("#fff4c0", 20, (650, 1000, 880, 1300), 17, "chispas")],
             cam(1.0, 1.05, (540, 1150)), "desenfoque", hud=[contexto(0.05, d - 0.05, "UN QUÍMICO · 2008")], sfx=[(0.2, "burbuja", -20), (0.5, "burbuja", -22)])


@v.plano(89, "que fabricara ese olor: el matraz suelta ondas")
def _(d):
    return P(["#0d1a1a", "#1a3a3a"], [BG("bg_lab"), brillo(540, 1200, 400, "#ffd27a", 0.4, 0.3),
             IMG("matraz", ancho=560, x=540, y=1300, z=0.5),
             IMG("olor", ancho=440, x=540, z=0.6, keys=[{"t": 0, "y": 1000, "op": 0, "ey": 0.5}, {"t": 0.3, "op": 1}, {"t": d, "y": 760, "ey": 1.1}])],
             cam(1.0, 1.05), "corte", sfx=[(0.1, "burbuja", -20), (0.3, "burbuja", -22)])


@v.plano(93, "¿para qué?")
def _(d):
    return P(OSC, [BG("bg_lab"), IMG("matraz", ancho=300, x=800, y=1400, z=0.5), IMG("astronauta", ancho=420, x=360, y=1150, z=0.5, anim={"balanceo": [6, 0.8]})],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "¿PARA QUÉ?", y=560, tam=120, color=AMBAR)], sfx=[(0.05, "pop", -20)])


@v.plano(95, "para que no se sorprendieran al entrenar: astronauta huele y no se asusta")
def _(d):
    return P(OSC, [BG("bg_lab"), IMG("cara_perfil", ancho=760, x=420, y=1200, z=0.5),
             IMG("olor", ancho=380, z=0.6, keys=[{"t": 0, "x": 980, "y": 1000, "op": 0, "rot": -70}, {"t": 0.3, "op": 1}, {"t": d * 0.8, "x": 720, "y": 900, "ease": "suave"}]),
             IMG("matraz", ancho=260, x=930, y=1350, z=0.55)],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[contexto(0.05, d - 0.05, "ENTRENAMIENTO")], sfx=[(0.1, "roce", -20)])


@v.plano(104, "hoy se vende como perfume: el frasco gira y rocía")
def _(d):
    return P(["#1a0a3a", "#3a1a6a"], [BG("bg_esp_violeta"), IMG("perfume", ancho=560, x=540, y=1150, z=0.5, keys=aparece(0.0, 0.4), anim={"balanceo": [6, 1.2]}),
             polvo("#ffe9a0", 50, (300, 700, 800, 1000), 19, "chispas"), brillo(540, 1100, 450, "#7a3ad8", 0.4, 0.2)],
             cam(1.0, 1.06), "desenfoque", hud=[amarillo(0.05, d - 0.03, "PERFUME", y=560, tam=120, color=MAGENTA)], sfx=[(0.05, "brillo", -18)])


@v.plano(110, "¿y la Luna?: la Luna entra girando")
def _(d):
    return P(ESP, [BG("bg_esp_petroleo"), luna(540, 1000, 820, 0.5, keys=[{"t": 0, "x": 1100, "rot": 20, "escala": 0.8}, {"t": d * 0.6, "x": 540, "rot": 0, "escala": 1.0, "ease": "salida"}])],
             cam(1.0, 1.04), "corte", hud=[amarillo(0.05, d - 0.03, "¿Y LA LUNA?", y=480, tam=110, color=CIAN)], sfx=[(0.05, "whoosh", -18)])


@v.plano(113, "los que la pisaron: astronauta sobre la superficie con el módulo")
def _(d):
    return P(ESP, [BG("bg_superficie_rica"), IMG("modulo_lunar", ancho=520, x=800, y=1250, z=0.4), tierra(860, 640, 260, 0.2, 2),
             IMG("astronauta", ancho=380, z=0.5, keys=[{"t": 0, "x": 250, "y": 1400}, {"t": d, "x": 460, "y": 1380, "ease": "suave"}], anim={"flotar": [20, 0.7]}),
             polvo("#c8c8d0", 30, (200, 1450, 600, 1600), 21)],
             cam(1.0, 1.05, (540, 1250)), "desenfoque", sfx=[(0.2, "golpe", -24), (0.9, "golpe", -24)])


@v.plano(119, "su polvo huele a pólvora: el guante sucio suelta polvo gris")
def _(d):
    return P(["#141418", "#2a2a30"], [BG("bg_lab"), IMG("guante", ancho=620, x=540, y=1200, z=0.5),
             IMG("polvo_lunar", ancho=900, x=540, y=900, z=0.6, keys=[{"t": 0, "escala": 0.3, "op": 0}, {"t": d * 0.5, "escala": 1.0, "op": 0.9, "ease": "salida"}, {"t": d, "escala": 1.1, "op": 0.7}])],
             cam(1.0, 1.05), "corte", hud=[rotulo(0.05, d - 0.05, "PÓLVORA", tam=110, color="#ffffff", capsula="#3a3d44e6", y=560)], sfx=[(0.1, "rumor", -22, {"dur": 0.8})])


@v.plano(123, "micro: fogonazo de pólvora", mas=0.05)
def _(d):
    return P(["#141418", "#2a2a30"], [IMG("chispa", ancho=900, x=540, y=1000, z=0.5, keys=[{"t": 0, "escala": 0.3}, {"t": d, "escala": 1.2, "ease": "salida"}]),
             IMG("polvo_lunar", ancho=1300, x=540, y=1000, z=0.6, keys=[{"t": 0, "escala": 0.6, "op": 0.5}, {"t": d, "escala": 1.2, "op": 0.9}])],
             cam(1.0, 1.08, temblor=6), "corte", sfx=[(0.02, "golpe", -12)])


@v.plano(125, "¿y lo más raro?: una estrella fugaz hacia el centro de la galaxia")
def _(d):
    return P(ESP, [BG("bg_galaxia"), fugaz(0.05, 950, 250, 400, 800), brillo(540, 1000, 500, "#ffb46a", 0.3, 0.1, pulso=[0.1, 0.8])],
             cam(1.0, 1.08), "corte", hud=[amarillo(0.05, d - 0.03, "¿LO MÁS RARO?", y=560, tam=110, color=AMBAR)], sfx=[(0.05, "subida", -18, {"dur": d * 0.9})])


@v.plano(129, "en el centro de nuestra galaxia: zoom al núcleo brillante")
def _(d):
    return P(ESP, [BG("bg_galaxia"), brillo(540, 960, 520, "#ffd27a", 0.7, 0.3, pulso=[0.15, 1.0]), polvo("#fff4c0", 60, (200, 600, 880, 1300), 23, "estrellas")],
             cam(1.0, 1.4, (540, 960), (540, 960)), "desenfoque", hud=[contexto(0.05, d - 0.05, "CENTRO DE LA VÍA LÁCTEA")], sfx=[(0.1, "brillo", -18)])


@v.plano(135, "un telescopio en Sierra Nevada: la antena gira")
def _(d):
    return P(["#05081a", "#1a2240"], [BG("bg_esp_petroleo"), IMG("radiotelescopio", ancho=1080, x=540, y=1380, z=0.45, keys=[{"t": 0, "rot": -3}, {"t": d, "rot": 3, "ease": "suave"}]),
             flecha([[640, 820], [900, 300]], 0.1, d * 0.5, CIAN, 6, disc=[18, 14], z=0.4), fugaz(0.3, 200, 300, 500, 500)],
             cam(1.0, 1.05, (540, 1200)), "corte", hud=[contexto(0.05, d - 0.05, "SIERRA NEVADA · ESPAÑA")], sfx=[(0.1, "senal", -20)])


@v.plano(140, "encontró una molécula: gira y se ilumina")
def _(d):
    return P(ESP, [BG("bg_galaxia"), brillo(540, 1000, 420, "#ff3df2", 0.35, 0.2),
             IMG("molecula_fruta", ancho=820, x=540, y=1000, z=0.5, keys=aparece(0.0, 0.4), anim={"girar": 12})],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "MOLÉCULA", y=560, tam=120, color=CIAN)], sfx=[(0.05, "pop", -18)])


@v.plano(145, "que da sabor a las frambuesas: la frambuesa cae")
def _(d):
    return P(["#2a0814", "#5a1028"], [brillo(540, 1150, 500, "#ff3d6a", 0.5, 0.2), IMG("frambuesa", ancho=640, x=540, z=0.5, keys=cae(0.0, 0.5, 500, 1150)),
             IMG("molecula_fruta", ancho=420, x=800, y=1550, z=0.4, anim={"girar": 10})],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[amarillo(0.05, d - 0.03, "FRAMBUESA", y=480, tam=120, color=MAGENTA)], sfx=[(0.35, "golpe", -18)])


@v.plano(149, "el corazón de la Vía Láctea huele a fruta (bucle al olor que sube)")
def _(d):
    return P(ESP, [BG("bg_galaxia"), brillo(540, 1000, 600, "#ffb46a", 0.6, 0.2, pulso=[0.15, 1.0]),
             IMG("frambuesa", ancho=360, x=540, y=1050, z=0.5, anim={"pulso": [0.06, 0.8]}),
             IMG("olor_rosa", ancho=460, x=540, z=0.6, keys=[{"t": 0, "y": 900, "op": 0, "ey": 0.5}, {"t": 0.4, "op": 1}, {"t": d, "y": 620, "ey": 1.1}]),
             polvo("#ffc8e0", 50, (100, 300, 980, 1600), 25, "estrellas")],
             cam(1.0, 1.08, (540, 1000), (540, 940)), "desenfoque", hud=[rotulo(0.05, d - 0.4, "HUELE A FRUTA", tam=96, color="#141414", capsula="#ffd23fe6", y=480)],
             sfx=[(0.1, "brillo", -18), (d * 0.6, "ding", -22)])


v.construir("2026-11-19-manana-01-espacio-filete", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 71, "db": -13},
            claves=["filete", "astronautas", "casco", "olor", "carne", "metal", "Pettit", "soldar", "metálico", "dulce", "oxígeno", "NASA", "químico",
                    "perfume", "Luna", "pólvora", "galaxia", "telescopio", "molécula", "frambuesas", "fruta"])
