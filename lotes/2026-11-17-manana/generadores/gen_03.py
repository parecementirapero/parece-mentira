"""03 · Esta huella no es humana (koala) — método denso (motor/DENSO.md). Lote 2026-11-17-manana, Agente 08:00 (Nico).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_lote  # noqa: E402

SVG = ilus_lote.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

OSCURO = ["#0a0c14", "#040508"]
LAB = ["#06121a", "#041018"]
BOSQUE = ["#c88a5a", "#2a2018"]
T_PAJ0, T_PAJ1 = v.w(35), v.w(48)   # pájaros que cruzan el bosque (detalle de fondo que dura)


def pajaros(d):
    return [{"tipo": "forma", "forma": "poligono", "puntos": [[-22, 0], [0, 8], [22, 0], [0, 3]], "relleno": "#2a2018", "z": 0.15,
             "anim": {"flotar": [6, 0.5 + k * 0.1]}, "keys": recorrido(T_PAJ0, T_PAJ1, (1150 + k * 70, 420 + k * 40), (-120 + k * 70, 360 + k * 30), d)} for k in range(4)]


def micro_cerca(svg, ancho, x, y, fondo, color, anim=None, sfx="tic", db=-20, extra=(), bg=None, rot=0):
    def fn(d):
        return P(fondo, [*([BG(bg)] if bg else []), polvo("#ffffff", 20, (0, 300, 1080, 1600), 10), brillo(540, 960, 520, color, 0.45, pulso=[0.2, 0.2]),
                 IMG(svg, ancho=ancho, x=x, y=y, z=0.5, rot=rot, anim=anim or {"flotar": [10, 0.5]},
                     keys=[{"t": 0, "escala": 0.92}, {"t": d, "escala": 1.06, "ease": "salida"}]), *extra],
                 cam(1.0, 1.1), "corte", sfx=[(0.02, sfx, db)])
    return fn


# ================================================================== PLANOS
@v.plano(0, "gancho: la huella se estampa y la lupa pasa")
def _(d):
    return P(OSCURO, [polvo("#ffe9a0", 25, (0, 300, 1080, 1700), 7), brillo(540, 960, 650, "#2ff3ff", 0.12), brillo(540, 1000, 700, "#ffd23f", 0.3, pulso=[0.1, 0.5]),
             IMG("huella", ancho=760, x=540, z=0.5, keys=[{"t": 0, "y": 1050, "escala": 1.5, "op": 0.6}, {"t": 0.25, "escala": 1.0, "op": 1, "ease": "golpe"}, {"t": d, "y": 1020, "escala": 1.06, "ease": "suave"}]),
             IMG("lupa", ancho=520, z=0.7, keys=[{"t": 0, "x": 950, "y": 1500, "rot": 20}, {"t": d, "x": 600, "y": 1150, "rot": -5, "ease": "suave"}])],
             cam(1.0, 1.25, (540, 1050), (540, 1050)), vineta=0.7, sfx=[(0.2, "golpe", -12)])


@v.plano(5, "es de un koala")
def _(d):
    return P(BOSQUE, [BG("bg_bosque"), polvo("#fff2c8", 25, (0, 300, 1080, 1600), 8), IMG("koala", ancho=760, x=520, z=0.5, keys=arranque(520, 1050, d, "derecha", 300, 30))],
             cam(1.0, 1.1, (540, 1000), (520, 960)), "desenfoque", hud=[amarillo(0.02, d - 0.01, "KOALA", y=560, color=AMBAR)], sfx=[(0.05, "whoosh", -14, {"dur": 0.4})])


@v.plano(9, "crestas")
def _(d):
    return P(OSCURO, [polvo("#ffe9a0", 25, (0, 300, 1080, 1700), 7), brillo(540, 960, 650, "#2ff3ff", 0.12), IMG("huella_koala", ancho=1100, x=540, y=1000, z=0.5, anim={"pulso": [0.02, 1.0]}),
             senala(420, 820, d * 0.2, d - 0.05, 120, AMBAR), senala(700, 1150, d * 0.4, d - 0.05, 100, MAGENTA)],
             cam(1.0, 1.15, (540, 1000), (540, 960)), "zoom", hud=[amarillo(0.1, d - 0.05, "CRESTAS", y=560, color=CIAN)])


@v.plano(11, "curvas y remolinos")
def _(d):
    return P(OSCURO, [polvo("#ffe9a0", 25, (0, 300, 1080, 1700), 7), brillo(540, 960, 650, "#2ff3ff", 0.12), IMG("huella_koala", ancho=2200, x=540, y=1100, z=0.5, anim={"girar": 4})],
             cam(1.3, 1.6, (540, 1100), (540, 1080)), hud=[rotulo(0.1, d - 0.05, "REMOLINOS", tam=96, color=MAGENTA, capsula="#0d1330e6", y=560)], sfx=[(0.1, "brillo", -20)])


@v.plano(14, "como la tuya")
def _(d):
    return P(["#2a1a14", "#120a08"], [brillo(540, 900, 600, "#ffcf9a", 0.4), IMG("dedo", ancho=520, x=330, z=0.5, keys=[{"t": 0, "y": 1250, "rot": -5}, {"t": d * 0.4, "y": 1150, "ease": "salida"}]),
             IMG("huella_tinta", ancho=380, x=780, y=980, z=0.55, keys=aparece(d * 0.35, 0.35))],
             cam(1.0, 1.06), "desenfoque", hud=[amarillo(0.1, d - 0.05, "COMO LA TUYA", y=560, tam=84)], sfx=[(d * 0.35, "golpe", -18)])


@v.plano(17, "mediados de los noventa")
def _(d):
    return P(["#1b2236", "#0b0f1c"], [brillo(540, 1000, 600, "#ffcf6a", 0.3), IMG("calendario", ancho=620, x=540, y=1050, z=0.5),
             IMG("calendario", ancho=620, x=540, y=1050, z=0.51, keys=[{"t": 0.1, "y": 1050, "rot": 0, "op": 1}, {"t": d * 0.7, "y": 450, "rot": -30, "op": 0, "ease": "entrada"}])],
             cam(1.0, 1.06), "zoom", hud=[rotulo(0.1, d - 0.05, "AÑOS 90", tam=120, color=AMBAR, capsula="#0d1330d8", y=560)], sfx=[(0.1, "whoosh", -16, {"dur": 0.3})])


@v.plano(22, "el antropólogo forense")
def _(d):
    return P(LAB, [BG("bg_lab"), polvo("#9dffb0", 20, (0, 300, 1080, 1600), 9), IMG("microscopio", ancho=520, x=330, y=1100, z=0.5),
             IMG("huella_tinta", ancho=340, x=780, y=1000, z=0.5, rot=6, keys=late(0.3, 2, 0.06, 0.4)), polvo("#9dffb0", 20, (100, 600, 980, 1400), 2, "chispas")],
             cam(1.0, 1.08, (540, 1050), (560, 1030)), "desenfoque",
             hud=[rotulo(0.1, d - 0.05, "ANTROPÓLOGO FORENSE", tam=64, color="#ffffff", capsula="#c0392be6", y=520),
                  rotulo(d * 0.35, d - 0.05, "M. HENNEBERG", tam=74, color=CIAN, capsula="#0d1330d8", y=1340)])


@v.plano(27, "los dedos de los koalas")
def _(d):
    return P(BOSQUE, [BG("bg_bosque"), polvo("#fff2c8", 25, (0, 300, 1080, 1600), 8), IMG("mano_koala", ancho=1000, x=540, z=0.5, keys=[{"t": 0, "y": 1150}, {"t": d * 0.5, "y": 1050, "ease": "salida"}, {"t": d, "y": 1060}]),
             senala(470, 820, d * 0.35, d - 0.05, 110, CIAN)],
             cam(1.0, 1.12, (540, 1000), (500, 900)), "zoom", sfx=[(d * 0.35, "pop", -20)])


@v.plano(35, "un parque australiano")
def _(d):
    return P(BOSQUE, [BG("bg_bosque"), polvo("#fff2c8", 25, (0, 300, 1080, 1600), 8), *pajaros(d), IMG("koala", ancho=420, x=300, y=1100, z=0.5, anim={"balanceo": [3, 1.4]}),
             IMG("koala", ancho=300, x=820, y=900, z=0.45, ex=-1, anim={"balanceo": [3, 1.7]})],
             cam(1.05, 1.0), hud=[contexto(0.05, d - 0.05, "AUSTRALIA")])


@v.plano(39, "al microscopio")
def _(d):
    return P(LAB, [BG("bg_lab"), polvo("#9dffb0", 20, (0, 300, 1080, 1600), 9), *pajaros(d), IMG("microscopio", ancho=700, x=540, z=0.5, keys=arranque(540, 1050, d, "abajo", 160, 20)),
             brillo(560, 1300, 140, "#7df9ff", 0.7, 0.55, pulso=[0.3, 0.3])],
             cam(1.0, 1.1, (540, 1000), (540, 960)), "desenfoque", sfx=[(0.1, "brillo", -18)])


@v.plano(43, "sorpresa: en el ocular")
def _(d):
    circ = {"tipo": "forma", "forma": "circulo", "radio": 420, "relleno": "#0a0c14", "x": 540, "y": 960, "z": 0.3}
    return P(["#000000", "#000000"], [circ, IMG("huella_koala", ancho=900, x=540, y=960, z=0.5, anim={"girar": 3}, keys=[{"t": 0, "escala": 1.4}, {"t": d * 0.6, "escala": 0.9, "ease": "salida"}]),
             {"tipo": "forma", "forma": "elipse", "ancho": 860, "alto": 860, "relleno": "#ffffff", "op_relleno": 0, "grosor": 30, "borde": "#20242c", "x": 540, "y": 960, "z": 0.6}],
             cam(1.0, 1.05), "zoom", hud=[amarillo(d * 0.25, d - 0.02, "¡SORPRESA!", y=1360, color=AMBAR)], sfx=[(d * 0.4, "ding", -16)])


@v.plano(48, "no las distinguía")
def _(d):
    return P(OSCURO, [polvo("#ffe9a0", 25, (0, 300, 1080, 1700), 7), brillo(540, 960, 650, "#2ff3ff", 0.12), IMG("huella_koala", ancho=440, x=290, y=980, z=0.5, keys=aparece(0.05, 0.35)), IMG("huella", ancho=440, x=790, y=980, z=0.5, keys=aparece(0.3, 0.35)),
             flecha([[440, 1300], [640, 1300]], d * 0.5, d * 0.8, AMBAR, 6), flecha([[640, 1300], [440, 1300]], d * 0.5, d * 0.8, AMBAR, 6)],
             cam(1.0, 1.05), hud=[rotulo(0.1, d - 0.05, "KOALA", tam=60, color=CIAN, capsula="#0d1330d8", x=290, y=600, fijo=True),
                                  rotulo(0.35, d - 0.05, "HUMANO", tam=60, color=AMBAR, capsula="#0d1330d8", x=790, y=600, fijo=True)],
             sfx=[(0.05, "pop", -18), (0.3, "pop", -18)])


@v.plano(53, "huellas que se confunden")
def _(d):
    return P(OSCURO, [polvo("#ffe9a0", 25, (0, 300, 1080, 1700), 7), brillo(540, 960, 650, "#2ff3ff", 0.12), IMG("huella_koala", ancho=640, y=1000, z=0.5, op=0.85, keys=[{"t": 0, "x": 290}, {"t": d * 0.7, "x": 540, "ease": "suave"}]),
             IMG("huella", ancho=640, y=1000, z=0.51, op=0.6, keys=[{"t": 0, "x": 790}, {"t": d * 0.7, "x": 540, "ease": "suave"}])],
             cam(1.0, 1.1), hud=[rotulo(d * 0.5, d - 0.05, "?", tam=200, color=MAGENTA, capsula=None, y=560, fijo=True)], sfx=[(d * 0.7, "brillo", -18)])


@v.plano(57, "despistar a un detective")
def _(d):
    return P(["#1a1410", "#0a0806"], [brillo(700, 600, 600, "#ffcf8a", 0.4), IMG("detective", ancho=560, x=380, y=1150, z=0.5, anim={"balanceo": [2, 1.2]}),
             IMG("lupa", ancho=380, x=700, z=0.6, keys=[{"t": 0, "y": 1050, "rot": -10}, {"t": d, "y": 950, "rot": 10, "ease": "suave"}]),
             IMG("huella_koala", ancho=200, x=700, y=950, z=0.55, op=0.8)],
             cam(1.0, 1.08, (540, 1050), (580, 1000)), "desenfoque", hud=[amarillo(0.1, d - 0.05, "DETECTIVE", y=560)])


@v.plano(65, "la escena de un crimen")
def _(d):
    return P(["#141820", "#080a0e"], [brillo(540, 1100, 500, "#ffffff", 0.2),
             {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 800, "relleno": ["#2a2e36", "#14161c"], "x": 540, "y": 1500, "z": 0.1},
             IMG("huella_tinta", ancho=260, x=560, y=1320, z=0.4, rot=-15, keys=aparece(d * 0.4, 0.3)),
             IMG("cinta", ancho=1400, x=540, y=900, z=0.6, rot=-8, keys=[{"t": 0, "x": -200}, {"t": d * 0.35, "x": 540, "ease": "salida"}]),
             brillo(200, 300, 200, "#ff3d3d", 0.6, 0.65, pulso=[0.5, 0.25]), brillo(880, 300, 200, "#3d6aff", 0.6, 0.65, pulso=[0.5, 0.25])],
             cam(1.0, 1.08, (540, 1100), (540, 1150)), "zoom", sfx=[(0.1, "whoosh", -14, {"dur": 0.4}), (d * 0.4, "pop", -18)])


@v.plano(77, "sería rarísimo")
def _(d):
    return P(["#141820", "#080a0e"], [IMG("cinta", ancho=1400, x=540, y=1350, z=0.6, rot=-8), IMG("koala", ancho=560, x=540, y=900, z=0.5, keys=aparece(0.05, 0.4) + [{"t": d, "rot": 6}])],
             cam(1.0, 1.06), hud=[amarillo(0.1, d - 0.05, "RARÍSIMO", y=560, color=MAGENTA)], energia=0.3)


@v.plano(79, "no es pariente cercano")
def _(d):
    return P(["#0a0618", "#04020c"], [brillo(540, 960, 600, "#7aa8ff", 0.3), IMG("arbol_familia", ancho=860, x=540, y=1000, z=0.4),
             IMG("koala", ancho=280, x=290, y=650, z=0.5, keys=aparece(d * 0.2, 0.35)), IMG("dedo", ancho=200, x=790, y=650, z=0.5, keys=aparece(d * 0.4, 0.35))],
             cam(1.0, 1.06), "desenfoque", hud=[rotulo(d * 0.3, d - 0.05, "NO ES PARIENTE CERCANO", tam=60, color="#ffffff", capsula="#0d1330d8", y=1360)])


@v.plano(90, "un marsupial, como el canguro")
def _(d):
    salto = [{"t": 0, "x": -150, "y": 1150}, {"t": d * 0.35, "x": 300, "y": 900, "ease": "salida"}, {"t": d * 0.7, "x": 650, "y": 1150, "ease": "entrada"}, {"t": d, "x": 900, "y": 980, "ease": "salida"}]
    return P(BOSQUE, [BG("bg_bosque"), polvo("#fff2c8", 25, (0, 300, 1080, 1600), 8), IMG("canguro", ancho=560, z=0.5, keys=salto)],
             cam(1.0, 1.04), hud=[amarillo(0.1, d - 0.05, "MARSUPIAL", y=560, color=AMBAR)], sfx=[(d * 0.7, "golpe", -18)])


@v.plano(96, "último antepasado común")
def _(d):
    return P(["#0a0618", "#04020c"], [brillo(540, 1400, 500, "#ffd23f", 0.3), IMG("arbol_familia", ancho=1300, x=540, y=900, z=0.4),
             senala(540, 1240, d * 0.3, d - 0.05, 120, AMBAR)],
             cam(1.1, 1.3, (540, 1200), (540, 1250)), "zoom", hud=[rotulo(0.1, d - 0.05, "ANTEPASADO", tam=84, color=AMBAR, capsula="#0d1330d8", y=560)])


@v.plano(100, "cien millones de años")
def _(d):
    return P(["#1b2236", "#0b0f1c"], [brillo(540, 1000, 700, "#ff9a7a", 0.3), *cronometro(0, -1440, 0, d)],
             cam(1.0, 1.08, (540, 1050), (540, 1050)), "desenfoque", 0.2,
             hud=[{**contador(0.05, d - 0.05, 0, 100, d * 0.6, "MILLONES DE AÑOS", tam=100, y=560, capsula="#c0392be6"), "contar_prefijo": "+"}],
             sfx=[(0.0, "whoosh", -14, {"dur": d}), (0.1, "tictac", -18, {"dur": d * 0.6, "ritmo": 0.08})])


@v.plano(108, "canguros y wombats: sin huellas")
def _(d):
    tacha = lambda x, t: flecha([[x - 150, 1250], [x + 150, 950]], t, t + 0.25, "#ff3d3d", 14, punta=False, z=0.7)
    return P(BOSQUE, [BG("bg_bosque"), polvo("#fff2c8", 25, (0, 300, 1080, 1600), 8), IMG("canguro", ancho=420, x=300, y=1080, z=0.5), IMG("wombat", ancho=440, x=790, y=1180, z=0.5, keys=aparece(0.2, 0.35)),
             tacha(300, d * 0.5), tacha(790, d * 0.65)],
             cam(1.0, 1.05), "desenfoque", hud=[rotulo(0.1, d - 0.05, "SIN HUELLAS", tam=90, color="#ffffff", capsula="#c0392be6", y=560)],
             sfx=[(d * 0.5, "zap", -18), (d * 0.65, "zap", -18)])


@v.plano(116, "¿y el koala sí?")
def _(d):
    return P(BOSQUE, [BG("bg_bosque"), polvo("#fff2c8", 25, (0, 300, 1080, 1600), 8), IMG("koala", ancho=760, x=540, y=1050, z=0.5, keys=late(0.2, 2, 0.06, 0.4))],
             cam(1.1, 1.25, (540, 960), (540, 900)), "zoom", hud=[rotulo(0.1, d - 0.05, "¿POR QUÉ?", tam=120, color=CIAN, capsula=None, y=560)], energia=0.35)


@v.plano(122, "agarrado a los eucaliptos")
def _(d):
    return P(BOSQUE, [BG("bg_bosque"), polvo("#fff2c8", 25, (0, 300, 1080, 1600), 8), IMG("rama_eucalipto", ancho=1100, x=700, y=650, z=0.4, anim={"balanceo": [2, 2.0]}),
             IMG("koala", ancho=640, x=430, y=1100, z=0.5, anim={"balanceo": [2, 1.6]}), polvo("#fff2c8", 20, (0, 400, 1080, 1400), 4)],
             cam(1.0, 1.08, (540, 1000), (500, 960)), "desenfoque", hud=[contexto(0.05, d - 0.05, "EUCALIPTO")])


@v.plano(127, "cogiendo hojas una a una")
def _(d):
    return P(BOSQUE, [BG("bg_bosque"), polvo("#fff2c8", 25, (0, 300, 1080, 1600), 8), IMG("rama_eucalipto", ancho=1300, x=540, y=760, z=0.4, anim={"balanceo": [3, 1.0]}),
             IMG("mano_koala", ancho=760, x=540, z=0.5, keys=[{"t": 0, "y": 1400}, {"t": d * 0.4, "y": 1000, "ease": "salida"}, {"t": d * 0.7, "y": 1040}, {"t": d, "y": 1000}])],
             cam(1.0, 1.1, (540, 960), (540, 900)), sfx=[(d * 0.4, "mordisco", -18)])


@v.plano(132, "sujetar: las crestas agarran")
def _(d):
    return P(BOSQUE, [BG("bg_bosque"), polvo("#fff2c8", 25, (0, 300, 1080, 1600), 8), IMG("mano_koala", ancho=1500, x=540, y=1000, z=0.5, keys=[{"t": 0, "escala": 0.95}, {"t": d * 0.4, "escala": 1.02, "ease": "golpe"}, {"t": d, "escala": 1.05}]),
             senala(400, 640, d * 0.3, d - 0.05, 110, LIMA)],
             cam(1.0, 1.08, (540, 900), (480, 820)), "zoom", hud=[rotulo(0.1, d - 0.05, "SUJETAR", tam=96, color=LIMA, capsula="#0d1330e6", y=1330)])


@v.plano(138, "sentir lo que toca")
def _(d):
    ondas = [{"tipo": "forma", "forma": "elipse", "ancho": 300, "alto": 300, "relleno": "#ffffff", "op_relleno": 0, "grosor": 6, "borde": CIAN, "x": 540, "y": 1000, "z": 0.6,
              "keys": [{"t": k * d / 4, "escala": 0.6, "op": 1}, {"t": k * d / 4 + d * 0.6, "escala": 2.6, "op": 0}]} for k in range(3)]
    return P(OSCURO, [polvo("#ffe9a0", 25, (0, 300, 1080, 1700), 7), brillo(540, 960, 650, "#2ff3ff", 0.12), IMG("huella_koala", ancho=760, x=540, y=1000, z=0.5, anim={"pulso": [0.03, 0.6]}), *ondas],
             cam(1.0, 1.08), hud=[amarillo(0.1, d - 0.05, "SENTIR", y=1380, color=CIAN)], sfx=[(k * d / 4, "senal", -24) for k in range(3)])


@v.plano(144, "dos veces la misma solución")
def _(d):
    return P(OSCURO, [polvo("#ffe9a0", 25, (0, 300, 1080, 1700), 7), brillo(540, 960, 650, "#2ff3ff", 0.12), {"tipo": "forma", "forma": "rect", "ancho": 6, "alto": 1300, "relleno": "#ffffff30", "x": 540, "y": 1000, "z": 0.2},
             IMG("dedo", ancho=360, x=290, y=1150, z=0.5, keys=aparece(0.05, 0.35)), IMG("huella", ancho=300, x=290, y=760, z=0.5, keys=aparece(0.3, 0.35)),
             IMG("mano_koala", ancho=440, x=790, y=1150, z=0.5, keys=aparece(d * 0.25, 0.35)), IMG("huella_koala", ancho=300, x=790, y=760, z=0.5, keys=aparece(d * 0.4, 0.35))],
             cam(1.0, 1.05), hud=[rotulo(d * 0.5, d - 0.05, "×2", tam=160, color=AMBAR, capsula="#0d1330d8", y=1340, fijo=True)],
             sfx=[(d * 0.5, "impacto", -12)], energia=0.9)


@v.plano(153, "¿qué otro animal? (cierre en bucle)")
def _(d):
    return P(OSCURO, [polvo("#ffe9a0", 25, (0, 300, 1080, 1700), 7), brillo(540, 960, 650, "#2ff3ff", 0.12), brillo(540, 1000, 700, "#ffd23f", 0.3, pulso=[0.1, 0.5]), IMG("huella", ancho=760, x=540, y=1030, z=0.5, keys=[{"t": 0, "escala": 0.9}, {"t": d, "escala": 1.4, "op": 0.7, "ease": "suave"}]),
             IMG("lupa", ancho=520, z=0.7, keys=[{"t": 0, "x": 600, "y": 1150}, {"t": d, "x": 950, "y": 1500, "ease": "suave"}])],
             cam(1.0, 1.1), "desenfoque")


# ------------------------------------------------------------------ micro planos (golpes de 0,4–0,7 s)
v.plano(8, "micro: la nariz del koala", mas=0.25)(micro_cerca("koala", 1700, 540, 1000, BOSQUE, "#fff2c8", anim={"balanceo": [3, 0.3]}, sfx="pop", db=-18, bg="bg_bosque"))
v.plano(13, "micro: el centro del remolino", mas=0.35)(micro_cerca("huella_koala", 3400, 540, 900, OSCURO, "#7df9ff", anim={"girar": 12}, sfx="brillo", db=-20))
v.plano(21, "micro: la hoja del calendario", mas=0.15)(micro_cerca("calendario", 900, 540, 1000, ["#1b2236", "#0b0f1c"], "#ffcf6a", anim={"balanceo": [6, 0.2]}, sfx="tic"))
v.plano(47, "micro: ¡flash!", mas=0.5)(lambda d: P(OSCURO, [polvo("#ffe9a0", 25, (0, 300, 1080, 1700), 7), brillo(540, 960, 650, "#2ff3ff", 0.12), IMG("huella_koala", ancho=1200, x=540, y=960, z=0.5), fundido_blanco([{"t": 0, "op": 0.9}, {"t": d, "op": 0}])],
                                                 cam(1.1, 1.2), "corte", sfx=[(0.0, "brillo", -16)]))
v.plano(64, "micro: la lupa", mas=0.35)(micro_cerca("lupa", 1000, 540, 960, ["#1a1410", "#0a0806"], "#ffcf8a", anim={"balanceo": [8, 0.25]}, sfx="tic"))
v.plano(89, "micro: el koala de cerca", mas=0.25)(micro_cerca("koala", 1000, 540, 1100, BOSQUE, "#fff2c8", sfx="pop", db=-20, bg="bg_bosque"))
v.plano(107, "micro: la aguja se para", mas=0.25)(lambda d: P(["#1b2236", "#0b0f1c"], [brillo(540, 1000, 700, "#ff9a7a", 0.3), *cronometro(-1440, -1460, 0, d)],
                                                           cam(1.25, 1.3, (540, 1050), (540, 1050)), "corte", sfx=[(0.02, "tic", -16)]))
v.plano(115, "micro: el canguro de cerca", mas=0.25)(micro_cerca("canguro", 1600, 640, 1200, BOSQUE, "#fff2c8", sfx="tic", bg="bg_bosque"))
v.plano(131, "micro: una hoja", mas=0.1)(micro_cerca("rama_eucalipto", 2400, 400, 960, BOSQUE, "#d8f0e4", anim={"balanceo": [4, 0.3]}, sfx="mordisco", db=-20, bg="bg_bosque"))
v.plano(143, "micro: la yema", mas=0.2)(micro_cerca("mano_koala", 3000, 900, 1700, BOSQUE, "#e8b4a8", sfx="pop", db=-20, bg="bg_bosque"))


v.construir("2026-11-17-manana-03-huella-koala", version=1, bucle=0.35, musica={"generar": "misterio", "semilla": 5, "db": -13},
            claves=["humana", "koala", "crestas", "remolinos", "microscopio", "detective", "marsupial", "cien", "millones", "eucaliptos", "solución"])
