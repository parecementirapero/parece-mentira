"""02 v2 (método denso) — Cruzar una puerta te hace olvidar. Uso: python3 gen_02_v2.py DIR_SALIDA DIR_AUDIO"""
import os, sys
from denso import Denso, IMG, BG, brillo, polvo, cam, CIAN, MAGENTA, LIMA, AMBAR

A = sys.argv[2]
D = Denso(sys.argv[1], os.path.join(A, "02-locucion.mp3"), os.path.join(A, "02-alineacion-original.json"))
K, w = D.K, D.w
NOCHE = ["#1a2036", "#0c1020"]
CREMA = ["#e8dcc8", "#b8a888"]
PL = ["#141826", "#080a12"]
CER = ["#2a1430", "#120814"]
MET = ["#2a2f3a", "#121620"]

# detalles de fondo que duran: el gato cruza el pasillo al principio y otra vez al final
GATO = [(0.0, w(18), (-250, 1720), (1350, 1700)), (w(122), D.FIN, (1350, 1720), (-250, 1700))]


def gato(d):
    els = []
    for i, (T0, T1, p0, p1) in enumerate(GATO):
        els.append(IMG("gato", ancho=300, z=0.75, ex=1 if i == 0 else -1, anim={"flotar": [4, 0.3]}, keys=D.recorrido(T0, T1, p0, p1, d)))
    return els


def pasillo(d, *extra, cerrada=False):
    return [BG("bg_pasillo_cerrada" if cerrada else "bg_pasillo"), *extra, *gato(d), polvo("#ffe2a8", 20, (300, 600, 780, 1400), 6)]


def persona(x, y, ancho=420, nombre="persona_casa", **kw):
    return IMG(nombre, ancho=ancho, x=x, y=y, z=0.6, **kw)


def boc(nombre, x, y, ancho=320, **kw):
    return IMG(nombre, ancho=ancho, x=x, y=y, z=0.7, anim={"flotar": [10, 1.6]}, **kw)


def hoja(d, ex):
    """Hoja de la puerta girando sobre la bisagra izquierda (ex: lista de (fracción, apertura))."""
    return IMG("hoja_puerta", ancho=700, y=1040, z=0.4, keys=K(d, *[(f, {"ex": e, "x": 190 + 350 * e}) for f, e in ex]))


# ================================================================== planos
@D.plano(0, "gancho: en el umbral, la idea se borra")
def _(d):
    return D.P(NOCHE, pasillo(d, persona(540, 1380, anim={"balanceo": [1.5, 1.2]}),
               boc("bocadillo_llaves", 800, 760, keys=K(d, (0, {"op": 1}), (0.6, {"op": 1}), (0.8, {"op": 0}))),
               boc("bocadillo_duda", 800, 760, keys=K(d, (0, {"op": 0}), (0.65, {"op": 0}), (0.85, {"op": 1})))),
               cam(1.0, 1.04, (540, 1100), (540, 1080)), vineta=0.6, sfx=[(0.65 * d, "fugaz", -20)])


@D.plano(4, "micro: las llaves se desvanecen")
def _(d):
    return D.P(NOCHE, [brillo(540, 900, 500, "#ffd890", 0.3), IMG("llaves", ancho=520, x=540, y=960, z=0.5, rot=-10,
               keys=K(d, (0, {"op": 1, "escala": 1}), (0.9, {"op": 0, "escala": 0.6})), anim={"balanceo": [6, 0.4]}),
               {"tipo": "particulas", "clase": "polvo", "color": "#ffd890", "area": [300, 800, 780, 1120], "n": 40, "tam": [3, 7], "vel": [0, -80], "z": 0.6, "semilla": 2}],
               cam(1.0, 1.1, (540, 960), (540, 960)), "desenfoque", vineta=0.7)


@D.plano(8, "cara de despiste")
def _(d):
    return D.P(NOCHE, pasillo(d, persona(540, 1380), boc("bocadillo_duda", 800, 760)), cam(1.8, 1.9, (560, 1000), (580, 960)), vineta=0.65)


@D.plano(11, "la culpa…: el pasillo se oscurece")
def _(d):
    return D.P(NOCHE, pasillo(d, persona(540, 1380, anim={"balanceo": [1.5, 1.2]}), cerrada=False), cam(1.0, 1.06, (540, 1000), (540, 900)), vineta=0.75)


@D.plano(15, "…de la puerta: flecha roja")
def _(d):
    return D.P(CREMA, [BG("puerta_cerca"), hoja(d, [(0, 0.35), (1, 0.28)]), D.flecha([[900, 1650], [440, 1250]], 0.05, 0.5, "#e8402f", 16)],
               cam(1.0, 1.06, (540, 1040), (540, 1000)), "desenfoque", vineta=0.5, hud=[D.amarillo(0.15, d - 0.02, "LA PUERTA", y=1720)])


@D.plano(18, "2011: la universidad")
def _(d):
    return D.P(["#2a4a8a", "#ffd8a0"], [BG("bg_universidad"), polvo("#fff6d8", 20)], cam(1.0, 1.05, (540, 1000), (540, 960)), "zoom", vineta=0.45,
               hud=[D.contexto(0.05, d - 0.02, "2011")])


@D.plano(22, "el psicólogo: la torre del reloj")
def _(d):
    return D.P(["#2a4a8a", "#ffd8a0"], [BG("bg_universidad")], cam(1.6, 1.7, (540, 640), (540, 620)), vineta=0.5,
               hud=[D.contexto(0.05, d - 0.02, "GABRIEL RADVANSKY")])


@D.plano(26, "Notre Dame, EE. UU.: ventanas que se encienden")
def _(d):
    luces = [brillo(190 + i * 125 + 30, 1040 + j * 170, 70, "#ffd27a", 0.8, 0.3, keys=K(d, (0, {"op": 0}), (0.1 + (i + j * 6) * 0.06, {"op": 0}), (0.15 + (i + j * 6) * 0.06, {"op": 1})))
             for i in range(6) for j in range(2)]
    return D.P(["#1a2a5a", "#e8a070"], [BG("bg_universidad"), *luces], cam(1.0, 1.04, (540, 1100), (540, 1100)), vineta=0.5,
               hud=[D.contexto(0.05, d - 0.02, "NOTRE DAME · EE. UU.")])


@D.plano(35, "hizo un experimento")
def _(d):
    return D.P(PL, [IMG("planta_sin", ancho=900, x=540, y=960, z=0.4, keys=K(d, (0, {"escala": 0.7, "op": 0}), (0.3, {"escala": 1, "op": 1, "ease": "salida"})))],
               cam(1.0, 1.03), "desenfoque", vineta=0.6, hud=[D.amarillo(0.1, d - 0.02, "EXPERIMENTO", y=1700)])


def caja(d, t0, t1, x0=540, y0=600, x1=540, y1=1180):
    return {"tipo": "forma", "forma": "redondeado", "ancho": 70, "alto": 60, "esquinas": 8, "relleno": "#3a8ad0", "borde": "#ffffff", "grosor": 4, "z": 0.62,
            "keys": K(d, (0, {"x": x0, "y": y0}), (t0, {"x": x0, "y": y0}), (t1, {"x": x1, "y": y1, "ease": "suave"}))}


def caminante(d, t0, t1, x0=540, y0=660, x1=540, y1=1240, color="#3fa0a8"):
    return {"tipo": "forma", "forma": "circulo", "radio": 34, "relleno": color, "borde": "#ffffff", "grosor": 6, "z": 0.6,
            "keys": K(d, (0, {"x": x0, "y": y0}), (t0, {"x": x0, "y": y0}), (t1, {"x": x1, "y": y1, "ease": "suave"})), "anim": {"pulso": [0.06, 0.35]}}


@D.plano(38, "los participantes llevaban objetos")
def _(d):
    return D.P(PL, [IMG("planta_sin", ancho=900, x=540, y=960, z=0.4), caminante(d, 0.1, 0.95), caja(d, 0.1, 0.95)],
               cam(1.0, 1.03), vineta=0.6, hud=[D.rotulo(0.05, d - 0.02, "DE UNA MESA A OTRA", tam=54, color="#ffffff", capsula="#0d1330d8", x=540, y=1660)])


@D.plano(47, "con puerta")
def _(d):
    return D.P(PL, [IMG("planta_puerta", ancho=900, x=540, y=960, z=0.4), caminante(d, 0.05, 0.9), caja(d, 0.05, 0.9),
               brillo(540, 960, 160, AMBAR, 0.7, 0.5, pulso=[0.3, 0.4])], cam(1.0, 1.03), vineta=0.6,
               hud=[D.rotulo(0.05, d - 0.02, "CON PUERTA", tam=64, color="#ffffff", capsula="#c0392be6", x=540, y=1660)], sfx=[(0.5 * d, "golpe", -22)])


@D.plano(51, "sin puerta, misma distancia")
def _(d):
    return D.P(PL, [IMG("planta_sin", ancho=900, x=540, y=960, z=0.4), caminante(d, 0.05, 0.9), caja(d, 0.05, 0.9),
               D.flecha([[780, 640], [780, 1280]], 0.05, d * 0.9, CIAN, 8, [20, 14])], cam(1.0, 1.03), vineta=0.6,
               hud=[D.rotulo(0.05, d - 0.02, "SIN PUERTA", tam=64, color="#111111", capsula=LIMA, x=540, y=1660)])


def barra(d, x, prog, color, f0):
    return {"tipo": "barra", "x": x, "y": 1050, "ancho": 220, "alto": 620, "vertical": True, "color": color, "fondo": "#ffffff14", "z": 0.5,
            "keys": K(d, (0, {"progreso": 0}), (f0, {"progreso": 0}), (f0 + 0.4, {"progreso": prog, "ease": "salida"}))}


@D.plano(59, "los de la puerta olvidaban más: barras")
def _(d):
    return D.P(NOCHE, [barra(d, 340, 0.85, "#ff4a3a", 0.05), barra(d, 740, 0.45, LIMA, 0.15)], cam(1.0, 1.03, (540, 1000), (540, 1000)), "desenfoque", vineta=0.6,
               hud=[D.rotulo(0.0, d - 0.02, "CON PUERTA", tam=46, color="#ffffff", capsula="#0d1330d8", x=340, y=1440),
                    D.rotulo(0.0, d - 0.02, "SIN PUERTA", tam=46, color="#ffffff", capsula="#0d1330d8", x=740, y=1440)], sfx=[(0.1, "trazo", -20)])


@D.plano(65, "olvidaban más: la barra roja late")
def _(d):
    return D.P(NOCHE, [barra(d, 340, 0.85, "#ff4a3a", -0.4), barra(d, 740, 0.45, LIMA, -0.4), brillo(340, 900, 260, "#ff4a3a", 0.5, 0.55, pulso=[0.25, 0.4])],
               cam(1.25, 1.3, (420, 1000), (420, 1000)), vineta=0.65, hud=[D.amarillo(0.05, d - 0.02, "OLVIDAN MÁS", y=1700)])


@D.plano(67, "en habitaciones de verdad: cruza con una caja")
def _(d):
    return D.P(NOCHE, pasillo(d, persona(540, 1650, 520, anim={"balanceo": [3, 0.6]}, keys=K(d, (0, {"y": 1650, "escala": 0.95}), (1, {"y": 1360, "escala": 0.62, "ease": "suave"}))),
               {"tipo": "forma", "forma": "redondeado", "ancho": 170, "alto": 130, "esquinas": 10, "relleno": "#c08a5a", "borde": "#7a4e2c", "grosor": 6, "z": 0.65,
                "keys": K(d, (0, {"x": 540, "y": 1480, "escala": 0.95}), (1, {"x": 540, "y": 1310, "escala": 0.62, "ease": "suave"}))}),
               cam(1.0, 1.06, (540, 1150), (540, 1080)), "zoom", vineta=0.6, hud=[D.amarillo(0.1, d - 0.02, "EN LA VIDA REAL", y=1780)])


@D.plano(73, "y pasó lo mismo: duda otra vez")
def _(d):
    return D.P(NOCHE, pasillo(d, persona(540, 1360, 300), boc("bocadillo_duda", 700, 980, 220, keys=K(d, (0, {"escala": 0}), (0.3, {"escala": 1, "ease": "rebote"})))),
               cam(1.5, 1.6, (560, 1150), (560, 1130)), vineta=0.65, sfx=[(0.3 * d, "pop", -18)])


@D.plano(77, "¿por qué? el cerebro")
def _(d):
    return D.P(CER, [brillo(540, 960, 500, "#ff8ab0", 0.35), IMG("cerebro", ancho=760, x=540, y=1050, z=0.5, anim={"pulso": [0.04, 0.6]})],
               cam(1.1, 1.0, (540, 1000), (540, 1000)), "desenfoque", vineta=0.65,
               hud=[D.rotulo(0.0, d - 0.02, "¿POR QUÉ?", tam=96, color="#ffd23f", capsula=None, rot=-6, x=540, y=1650)])


@D.plano(79, "no guarda el día como una película continua")
def _(d):
    return D.P(CER, [brillo(540, 800, 500, "#ff8ab0", 0.3), IMG("cerebro", ancho=520, x=540, y=760, z=0.5, anim={"pulso": [0.03, 0.8]}),
               IMG("pelicula", ancho=2400, y=1400, z=0.6, keys=K(d, (0, {"x": 1500}), (1, {"x": 0})))], cam(1.0, 1.03, (540, 1050), (540, 1050)), vineta=0.6,
               sfx=[(0.1, "tictac", -26, {"dur": d - 0.2})])


@D.plano(85, "película continua: la tira corre rápido")
def _(d):
    return D.P(CER, [IMG("pelicula", ancho=2400, y=1000, z=0.6, keys=K(d, (0, {"x": 1200}), (1, {"x": -100}))),
               *[D.flecha([[1000, 860 + i * 60], [800, 860 + i * 60]], 0.05 + i * 0.05, 0.4 + i * 0.05, CIAN, 5, punta=False) for i in range(4)]],
               cam(1.2, 1.25, (540, 1000), (540, 1000)), vineta=0.6, hud=[D.amarillo(0.1, d - 0.02, "PELÍCULA", y=1400)])


@D.plano(89, "lo corta en escenas")
def _(d):
    cortes = [{"tipo": "forma", "forma": "rect", "ancho": 12, "alto": 420, "relleno": "#ffffff", "x": x, "y": 1400, "z": 0.65,
               "keys": K(d, (0, {"op": 0}), (0.15 + i * 0.2, {"op": 0}), (0.18 + i * 0.2, {"op": 1}))} for i, x in enumerate((262, 558, 854))]
    for i in range(3):
        D.fx(D.INI + (0.18 + i * 0.2) * d, "tic", -14)
    return D.P(CER, [IMG("cerebro", ancho=520, x=540, y=760, z=0.5), IMG("pelicula", ancho=2400, x=1100, y=1400, z=0.6), *cortes],
               cam(1.0, 1.0, (540, 1050), (540, 1050)), vineta=0.6, hud=[D.amarillo(0.1, d - 0.02, "ESCENAS", y=1720)])


@D.plano(93, "y una puerta…")
def _(d):
    return D.P(CREMA, [BG("puerta_cerca"), hoja(d, [(0, 0.2)])], cam(1.0, 1.04, (540, 1040), (540, 1040)), "zoom", vineta=0.5)


@D.plano(96, "…es un corte perfecto: se cierra de golpe")
def _(d):
    return D.P(CREMA, [BG("puerta_cerca"), hoja(d, [(0, 0.2), (0.35, 1.0)])], cam(1.0, 1.05, (540, 1040), (540, 1040)), vineta=0.5,
               hud=[D.amarillo(0.4 * d, d - 0.02, "CORTE", y=1720)], sfx=[(0.35 * d, "golpe", -10)])


@D.plano(100, "al cruzarla: la persona pasa")
def _(d):
    return D.P(NOCHE, pasillo(d, persona(540, 1650, 480, anim={"balanceo": [3, 0.6]}, keys=K(d, (0, {"y": 1700, "escala": 1.1}), (1, {"y": 1400, "escala": 0.6, "ease": "suave"})))),
               cam(1.0, 1.05, (540, 1150), (540, 1100)), "desenfoque", vineta=0.6)


@D.plano(102, "cierra el capítulo: la carpeta")
def _(d):
    return D.P(MET, [brillo(540, 900, 600, "#cfe0ff", 0.25), IMG("carpeta", ancho=420, x=540, y=900, z=0.6, rot=-4, anim={"flotar": [8, 1.0]})],
               cam(1.0, 1.05, (540, 960), (540, 960)), vineta=0.6, hud=[D.amarillo(0.1, d - 0.02, "CAPÍTULO", y=1500)])


@D.plano(105, "de la habitación anterior: la taza y la planta dentro de la carpeta")
def _(d):
    return D.P(MET, [IMG("carpeta", ancho=520, x=540, y=900, z=0.5), IMG("taza", ancho=180, x=430, y=880, z=0.6, keys=K(d, (0, {"escala": 0}), (0.2, {"escala": 1, "ease": "rebote"}))),
               IMG("planta", ancho=150, x=650, y=860, z=0.6, keys=K(d, (0, {"escala": 0}), (0.4, {"escala": 0}), (0.6, {"escala": 1, "ease": "rebote"})))],
               cam(1.2, 1.25, (540, 900), (540, 900)), vineta=0.6, sfx=[(0.2 * d, "pop", -20), (0.6 * d, "pop", -20)])


@D.plano(109, "y lo archiva")
def _(d):
    return D.P(MET, [brillo(540, 900, 600, "#cfe0ff", 0.25), IMG("archivador", ancho=600, x=540, y=1250, z=0.5),
               IMG("carpeta", ancho=300, x=540, z=0.6, keys=K(d, (0, {"y": 520, "rot": -8, "op": 1}), (0.6, {"y": 860, "rot": 0, "escala": 0.7, "ease": "entrada", "op": 1}), (0.7, {"op": 0})))],
               cam(1.0, 1.04, (540, 1000), (540, 1050)), vineta=0.6, hud=[D.amarillo(0.2 * d, d - 0.02, "ARCHIVADO", y=1780)], sfx=[(0.6 * d, "golpe", -16)])


@D.plano(112, "lo que ibas a hacer: las llaves")
def _(d):
    return D.P(MET, [IMG("archivador", ancho=600, x=540, y=1250, z=0.5),
               IMG("bocadillo_llaves", ancho=340, x=540, y=560, z=0.6, anim={"flotar": [10, 1.0]})], cam(1.1, 1.15, (540, 900), (540, 900)), vineta=0.6)


@D.plano(118, "se queda allí dentro")
def _(d):
    return D.P(MET, [IMG("archivador", ancho=600, x=540, y=1250, z=0.5),
               IMG("bocadillo_llaves", ancho=340, x=540, z=0.6, keys=K(d, (0, {"y": 560, "escala": 1, "op": 1}), (0.6, {"y": 880, "escala": 0.3, "ease": "entrada", "op": 1}), (0.7, {"op": 0})))],
               cam(1.2, 1.3, (540, 900), (540, 920)), vineta=0.6, sfx=[(0.65 * d, "golpe", -18)])


@D.plano(122, "lo más raro: vuelve atrás")
def _(d):
    return D.P(NOCHE, pasillo(d, persona(540, 1360, 400, nombre="persona_casa_izq", anim={"balanceo": [3, 0.6]},
                                         keys=K(d, (0, {"y": 1400, "escala": 0.7}), (1, {"y": 1600, "escala": 1.1, "ease": "suave"})))),
               cam(1.0, 1.04, (540, 1100), (540, 1100)), "zoom", vineta=0.6, hud=[D.amarillo(0.1, d - 0.02, "LO MÁS RARO", y=1780)])


@D.plano(128, "volver a la habitación de antes")
def _(d):
    return D.P(NOCHE, pasillo(d, persona(540, 1600, 440, nombre="persona_casa_izq", anim={"balanceo": [1.5, 1.2]}),
               D.flecha([[860, 1700], [860, 1300], [680, 1150]], 0.05, d * 0.7, CIAN, 10, [20, 14])),
               cam(1.0, 1.04, (540, 1200), (540, 1180)), vineta=0.6, hud=[D.rotulo(0.05, d - 0.02, "VOLVER", tam=72, color="#111111", capsula=CIAN, x=540, y=520)])


@D.plano(134, "no ayudaba a recordar")
def _(d):
    return D.P(NOCHE, pasillo(d, persona(540, 1600, 440, nombre="persona_casa_izq"), boc("bocadillo_duda", 820, 900)),
               cam(1.3, 1.35, (600, 1150), (600, 1130)), vineta=0.65, hud=[D.amarillo(0.05, d - 0.02, "NO AYUDA", y=1780)])


@D.plano(138, "así que la próxima vez: el reloj")
def _(d):
    return D.P(CREMA, [brillo(540, 900, 500, "#ffffff", 0.3), IMG("reloj_pared", ancho=560, x=540, y=1000, z=0.5),
               IMG("aguja_larga", ancho=74, x=540, y=1000, z=0.55, keys=K(d, (0, {"rot": 0, "ease": "lineal"}), (1, {"rot": 360}))),
               IMG("aguja_corta", ancho=74, x=540, y=1000, z=0.56, keys=K(d, (0, {"rot": 90, "ease": "lineal"}), (1, {"rot": 120})))],
               cam(1.0, 1.04), "desenfoque", vineta=0.5, sfx=[(0.05, "tictac", -22, {"dur": d - 0.1})])


@D.plano(143, "no culpes a tu memoria: el cerebro inocente")
def _(d):
    return D.P(CER, [brillo(540, 960, 500, "#ff8ab0", 0.35), IMG("cerebro", ancho=760, x=540, y=1050, z=0.5, anim={"balanceo": [3, 1.4]})],
               cam(1.0, 1.05, (540, 1050), (540, 1030)), vineta=0.65,
               hud=[D.rotulo(0.1, d - 0.02, "INOCENTE", tam=80, color="#111111", capsula=LIMA, x=540, y=1600, rot=-4)], sfx=[(0.1, "ding", -16)])


@D.plano(148, "bucle: culpa a la puerta")
def _(d):
    return D.P(NOCHE, pasillo(d, persona(540, 1380), boc("bocadillo_duda", 800, 760)), cam(1.6, 1.0, (540, 1000), (540, 1100)), "zoom", vineta=0.6,
               hud=[D.rotulo(0.15, d - 0.02, "CULPABLE", tam=80, color="#ffffff", capsula="#c0392be6", x=540, y=1640, rot=-4)])


D.construir("02", "puertas-olvidar", ["puerta", "Radvansky", "experimento", "olvidaban", "cerebro", "película", "escenas", "corte",
                                      "capítulo", "archiva", "memoria"], {"generar": "curiosidad", "semilla": 21, "db": -13})
