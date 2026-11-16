"""03 v2 (método denso) — Tu móvil y el ordenador del Apolo 11. Uso: python3 gen_03_v2.py DIR_SALIDA DIR_AUDIO"""
import os, sys
from denso import Denso, IMG, BG, brillo, polvo, cam, CIAN, MAGENTA, LIMA, AMBAR

A = sys.argv[2]
D = Denso(sys.argv[1], os.path.join(A, "03-locucion.mp3"), os.path.join(A, "03-alineacion-original.json"))
K, w = D.K, D.w
ESP = ["#02030a", "#0a1030"]
TALLER = ["#1d2430", "#0b0f16"]
VERDE = ["#1f3a2a", "#0c1a12"]
AZUL = ["#16203a", "#080c18"]
COBRE = "#f0a050"

# detalles de fondo que duran: un satélite cruza las escenas de espacio; motas de polvo en el taller
SAT = (w(13) - 0.3, w(41), (1200, 300), (-150, 620))
SAT2 = (w(136) - 0.3, D.FIN, (-150, 380), (1200, 260))


def satelites(d):
    return [IMG("satelite", ancho=140, z=0.15, rot=-15, anim={"girar": 4}, keys=D.recorrido(*SAT, d)),
            IMG("satelite", ancho=110, z=0.15, rot=20, anim={"girar": -4}, keys=D.recorrido(*SAT2, d))]


def estrellas(n=40, sem=3):
    return polvo("#ffffff", n, (0, 0, 1080, 1920), sem, "estrellas")


def taller(*extra):
    return [BG("bg_taller"), brillo(540, 850, 650, "#6fa0ff", 0.15), polvo("#cfe0ff", 25, (0, 300, 1080, 1700), 8), *extra]


def movil(x, y, ancho, nombre="movil", z=0.55, **kw):
    return IMG(nombre, ancho=ancho, x=x, y=y, z=z, **kw)


def agc(x, y, ancho, z=0.5, led=True, **kw):
    k = ancho / 760
    els = [IMG("agc", ancho=ancho, x=x, y=y, z=z, **kw)]
    if led:
        els.append(brillo(x + (580 - 380) * k, y + (360 - 310) * k, int(150 * k), LIMA, 0.6, z + 0.01, pulso=[0.3, 0.6]))
    return els


# ================================================================== planos
@D.plano(0, "gancho: móvil enorme frente al Apolo")
def _(d):
    return D.P(TALLER, taller(movil(330, 1150, 460, anim={"flotar": [8, 2]}), *agc(830, 1340, 300, keys=K(d, (0, {"escala": 1.0}), (1, {"escala": 0.85}))),
               brillo(330, 1100, 260, "#9fc0ff", 0.4, 0.5, pulso=[0.2, 0.8])), cam(1.0, 1.04, (540, 1150), (540, 1120)), vineta=0.6,
               hud=[{"tipo": "rotulo", "texto": "×1.000.000", "unidad": "VECES", "tam": 100, "x": 540, "y": 1720, "hud": True, "z": 1, "borde": CIAN,
                     "anim": {"pulso": [0.04, 0.8]}}], sfx=[(0.05, "zap", -16)])


@D.plano(8, "micro: la memoria del móvil se llena de fotos")
def _(d):
    return D.P(AZUL, [movil(540, 1000, 600), brillo(540, 900, 300, "#9fc0ff", 0.5, 0.6, pulso=[0.3, 0.3])],
               cam(1.3, 1.4, (540, 900), (540, 880)), vineta=0.6)


@D.plano(10, "el Apolo once: el ordenador de cerca")
def _(d):
    return D.P(TALLER, taller(*agc(540, 1100, 900)), cam(1.0, 1.06, (540, 1050), (560, 1030)), "desenfoque", vineta=0.6,
               hud=[D.rotulo(0.05, d - 0.02, "APOLO 11", tam=64, color="#ffffff", capsula="#c0392be6", x=540, y=1640)])


@D.plano(13, "1969: despega el cohete")
def _(d):
    humo = {"tipo": "particulas", "clase": "polvo", "color": "#e8e0d0", "area": [380, 1500, 700, 1750], "n": 60, "tam": [10, 26], "vel": [0, 60], "z": 0.55, "semilla": 4}
    return D.P(["#1a2a5a", "#e8a070"], [brillo(540, 1650, 400, "#ffb05a", 0.7, 0.5, pulso=[0.2, 0.15]), humo,
               IMG("cohete", ancho=260, x=540, z=0.6, keys=K(d, (0, {"y": 1100}), (1, {"y": 720, "ease": "entrada"}))), *satelites(d)],
               cam(1.0, 1.05, (540, 1000), (540, 900), temblor=5), "zoom", vineta=0.5,
               hud=[D.contexto(0.05, d - 0.02, "1969")], sfx=[(0.05, "rumor", -18, {"dur": d})])


@D.plano(19, "la nave: el módulo en el espacio")
def _(d):
    return D.P(ESP, [BG("bg_esp_violeta"), estrellas(), *satelites(d), IMG("tierra_hd", ancho=480, x=200, y=1650, z=0.3, anim={"girar": 3}),
               IMG("modulo_lunar_det", ancho=320, z=0.6, anim={"balanceo": [3, 2]}, keys=K(d, (0, {"x": 380, "y": 1250}), (1, {"x": 560, "y": 1050})))],
               cam(1.0, 1.04, (540, 1100), (540, 1050)), "desenfoque", vineta=0.55)


@D.plano(21, "Armstrong y Aldrin: rumbo a la Luna")
def _(d):
    return D.P(ESP, [BG("bg_esp_violeta"), estrellas(40, 5), *satelites(d), IMG("luna_hd", ancho=440, x=820, y=560, z=0.3),
               IMG("modulo_lunar_det", ancho=240, z=0.6, anim={"balanceo": [3, 2]}, keys=K(d, (0, {"x": 300, "y": 1400}), (1, {"x": 620, "y": 860, "ease": "suave"}))),
               D.flecha([[260, 1500], [460, 1200], [600, 960]], 0.05, d * 0.9, CIAN, 8, [18, 14]), D.fugaz(0.3, 900, 1100, 620, 1300)],
               cam(1.0, 1.05, (540, 1050), (580, 960)), vineta=0.55,
               hud=[D.contexto(0.05, d - 0.02, "ARMSTRONG Y ALDRIN")])


@D.plano(27, "micro: la Luna de cerca")
def _(d):
    return D.P(ESP, [BG("bg_esp_violeta"), estrellas(30, 7), IMG("luna_hd", ancho=900, x=540, y=1000, z=0.4, anim={"girar": 1})],
               cam(1.0, 1.08, (540, 1000), (540, 1000)), vineta=0.6)


@D.plano(30, "se guiaba con un ordenador: aterriza en el taller")
def _(d):
    return D.P(TALLER, taller(*agc(540, 1150, 820, keys=K(d, (0, {"y": 850}), (0.3, {"y": 1150, "ease": "rebote"})))),
               cam(1.0, 1.05, (540, 1100), (540, 1080)), "zoom", vineta=0.6, sfx=[(0.3 * d, "golpe", -12)])


@D.plano(35, "treinta y dos kilos: una báscula")
def _(d):
    bascula = {"tipo": "forma", "forma": "redondeado", "ancho": 700, "alto": 80, "esquinas": 16, "relleno": ["#c9ccd2", "#7a8089"], "x": 540, "y": 1470, "z": 0.45}
    return D.P(TALLER, taller(bascula, *agc(540, 1180, 640, keys=K(d, (0, {"y": 1130}), (0.2, {"y": 1180, "ease": "rebote"})))),
               cam(1.0, 1.04, (540, 1200), (540, 1200)), vineta=0.6,
               hud=[D.contador(0.05, d - 0.02, 0, 32, d * 0.5, "KILOS", tam=130, y=1680, borde=AMBAR)], sfx=[(0.2 * d, "golpe", -18)])


@D.plano(41, "del tamaño de un maletín")
def _(d):
    return D.P(TALLER, taller(*agc(330, 1150, 480), IMG("maletin", ancho=440, x=800, y=1200, z=0.5, keys=K(d, (0, {"x": 1300}), (0.3, {"x": 800, "ease": "salida"})))),
               cam(1.0, 1.04, (540, 1150), (540, 1150)), vineta=0.6,
               hud=[D.rotulo(0.3, d - 0.02, "=", tam=160, color="#ffffff", capsula=None, x=575, y=1150)])


@D.plano(46, "su memoria de trabajo: el teclado")
def _(d):
    return D.P(TALLER, taller(*agc(540, 1100, 900)), cam(1.7, 1.8, (720, 960), (720, 960)), "desenfoque", vineta=0.6,
               hud=[D.rotulo(0.05, d - 0.02, "MEMORIA", tam=60, color="#111111", capsula=LIMA, x=540, y=1640)])


@D.plano(50, "2.048 palabras: casillas que se llenan")
def _(d):
    cas = [{"tipo": "forma", "forma": "rect", "ancho": 40, "alto": 40, "relleno": LIMA, "x": 180 + (i % 16) * 46, "y": 700 + (i // 16) * 46, "z": 0.5,
            "keys": K(d, (0, {"op": 0}), (0.05 + i * 0.006, {"op": 0}), (0.06 + i * 0.006, {"op": 0.9}))} for i in range(128)]
    return D.P(VERDE, [*cas], cam(1.0, 1.03, (540, 860), (540, 860)), vineta=0.6,
               hud=[D.contador(0.05, d - 0.02, 0, 2048, d * 0.75, "PALABRAS", tam=120, y=1640, borde=LIMA)], sfx=[(0.1, "trazo", -24)])


@D.plano(56, "unos cuatro kilobytes")
def _(d):
    return D.P(VERDE, [*agc(540, 1050, 640)], cam(1.2, 1.25, (600, 1000), (600, 1000)), vineta=0.6,
               hud=[D.dato(0.05, d - 0.02, "4", "KB", y=1640, tam=140, borde=LIMA)])


def barra_h(d, y, prog, color, f0):
    return {"tipo": "barra", "x": 540, "y": y, "ancho": 860, "alto": 70, "color": color, "fondo": "#ffffff18", "z": 0.6,
            "keys": K(d, (0, {"progreso": 0}), (f0, {"progreso": 0}), (f0 + 0.35, {"progreso": prog, "ease": "salida"}))}


@D.plano(59, "mucho menos que una sola foto")
def _(d):
    return D.P(AZUL, [movil(540, 900, 420, anim={"flotar": [6, 2]}), barra_h(d, 1450, 0.012, LIMA, 0.0), barra_h(d, 1620, 1.0, AMBAR, 0.25)],
               cam(1.0, 1.03, (540, 1100), (540, 1100)), "zoom", vineta=0.6,
               hud=[D.rotulo(0.0, d - 0.02, "APOLO · 4 KB", tam=46, color="#ffffff", capsula="#0d1330d8", x=290, y=1370),
                    D.rotulo(0.25, d - 0.02, "UNA FOTO", tam=46, color="#ffffff", capsula="#0d1330d8", x=240, y=1540)], sfx=[(0.3 * d, "trazo", -20)])


@D.plano(65, "de tu galería: zoom a una foto")
def _(d):
    return D.P(AZUL, [movil(540, 1000, 600)], cam(1.6, 2.2, (470, 640), (470, 640)), vineta=0.6)


@D.plano(68, "su reloj: luz que parpadea despacio")
def _(d):
    return D.P(TALLER, taller(*agc(540, 1100, 820, led=False),
               brillo(700, 920, 200, LIMA, 0.9, 0.6, keys=K(d, (0, {"op": 0.1}), (0.5, {"op": 1}), (1, {"op": 0.1})))),
               cam(1.0, 1.05, (540, 1050), (560, 1030)), "desenfoque", vineta=0.6,
               hud=[D.rotulo(0.05, d - 0.02, "RELOJ", tam=60, color="#ffffff", capsula="#c0392be6", x=540, y=520)], sfx=[(0.5 * d, "tic", -14)])


@D.plano(71, "0,04 megahercios: un caracol de luz")
def _(d):
    punto = {"tipo": "forma", "forma": "circulo", "radio": 22, "relleno": LIMA, "y": 1000, "z": 0.6, "keys": K(d, (0, {"x": 160}), (1, {"x": 360, "ease": "lineal"}))}
    return D.P(VERDE, [D.flecha([[140, 1000], [940, 1000]], 0.0, 0.2, "#ffffff40", 4, punta=False), punto, brillo(160, 1000, 80, LIMA, 0.6, 0.55)],
               cam(1.0, 1.02), vineta=0.6, hud=[D.dato(0.1, d - 0.02, "0,04", "MHZ", y=1640, tam=130, borde=LIMA)], sfx=[(0.1, "tic", -16), (0.6 * d, "tic", -16)])


@D.plano(78, "un móvil de hoy")
def _(d):
    return D.P(AZUL, [movil(540, 1000, 560, keys=K(d, (0, {"escala": 0.8}), (0.3, {"escala": 1, "ease": "rebote"}))), brillo(540, 900, 260, "#9fc0ff", 0.6, 0.6, pulso=[0.3, 0.2])],
               cam(1.0, 1.04, (540, 1000), (540, 980)), "zoom", vineta=0.55)


@D.plano(82, "miles de megahercios: la luz vuela")
def _(d):
    punto = {"tipo": "forma", "forma": "circulo", "radio": 22, "relleno": CIAN, "y": 1000, "z": 0.6, "keys": K(d, *[(i / 8, {"x": 160 if i % 2 == 0 else 920}) for i in range(9)])}
    return D.P(AZUL, [D.flecha([[140, 1000], [940, 1000]], 0.0, 0.1, "#ffffff40", 4, punta=False), punto,
               *[D.flecha([[900 - i * 30, 940 + i * 30], [600 - i * 30, 940 + i * 30]], 0.05 + i * 0.05, 0.3 + i * 0.05, CIAN, 5, punta=False) for i in range(4)]],
               cam(1.0, 1.02), vineta=0.6, hud=[D.rotulo(0.05, d - 0.02, "MILES DE MHZ", tam=72, color="#111111", capsula=CIAN, x=540, y=1640)])


@D.plano(87, "y gigas de memoria")
def _(d):
    return D.P(AZUL, [movil(540, 1000, 560), polvo(CIAN, 50, (100, 300, 980, 1700), 5, "chispas")], cam(1.05, 1.1, (540, 1000), (540, 980)), vineta=0.55,
               hud=[D.rotulo(0.05, d - 0.02, "GIGAS", tam=110, color="#ffd23f", capsula="#0d1330d8", x=540, y=1640)])


@D.plano(92, "más de un millón de veces más")
def _(d):
    return D.P(TALLER, taller(movil(330, 1150, 460), *agc(830, 1360, 240), brillo(330, 1100, 300, "#9fc0ff", 0.4, 0.5, pulso=[0.2, 0.6])),
               cam(1.0, 1.05, (540, 1150), (540, 1130)), "desenfoque", vineta=0.6,
               hud=[{**D.contador(0.05, d - 0.02, 1, 1000000, d * 0.6, "VECES MÁS", tam=100, y=1720, borde=CIAN), "contar_prefijo": "+"}], sfx=[(0.1, "brillo", -16)])


@D.plano(99, "lo más increíble: la memoria de cuerda")
def _(d):
    return D.P(VERDE, [BG("bg_nucleos"), brillo(540, 960, 500, "#ffcf8a", 0.25, 0.5, pulso=[0.1, 1.5])], cam(1.0, 1.05, (540, 1000), (540, 960)), "zoom", vineta=0.6,
               hud=[D.contexto(0.05, d - 0.02, "MEMORIA DE CUERDA")])


@D.plano(103, "no se descargaba: barra de descarga tachada")
def _(d):
    barra = {"tipo": "barra", "x": 540, "y": 1000, "ancho": 760, "alto": 60, "color": CIAN, "fondo": "#ffffff20", "z": 0.6,
             "keys": K(d, (0, {"progreso": 0}), (0.5, {"progreso": 0.35}), (1, {"progreso": 0.35}))}
    tacha = D.flecha([[160, 1180], [920, 820]], 0.55 * d, 0.75 * d, "#ff4a3a", 16, punta=False)
    return D.P(VERDE, [BG("bg_nucleos"), {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 500, "relleno": "#0c1a12", "x": 540, "y": 1000, "z": 0.45, "op": 0.8},
               barra, tacha], cam(1.0, 1.02), vineta=0.6, hud=[D.amarillo(0.05, d - 0.02, "NO SE DESCARGABA", y=1720, tam=84)], sfx=[(0.6 * d, "golpe", -16)])


@D.plano(108, "se tejía a mano")
def _(d):
    return D.P(VERDE, [BG("bg_nucleos"), IMG("manos_tejer", ancho=900, x=540, y=1150, z=0.6, anim={"balanceo": [3, 0.5]})],
               cam(1.2, 1.25, (540, 1100), (540, 1100)), vineta=0.6, hud=[D.amarillo(0.05, d - 0.02, "A MANO", y=1720)])


@D.plano(112, "trabajadoras de una fábrica")
def _(d):
    return D.P(TALLER, [brillo(540, 700, 600, "#ffe2a8", 0.35), IMG("bg_nucleos", ancho=900, x=540, y=1100, z=0.3, op=0.9),
               IMG("manos_tejer", ancho=700, x=540, y=1150, z=0.6, anim={"balanceo": [4, 0.4]})],
               cam(1.0, 1.04, (540, 1100), (540, 1100)), "desenfoque", vineta=0.6, hud=[D.contexto(0.05, d - 0.02, "TRABAJADORAS")])


@D.plano(116, "pasaban hilos de cobre")
def _(d):
    hilo = D.flecha([[60, 1080], [300, 1030], [460, 1130], [620, 1030], [780, 1130], [1020, 1060]], 0.05, d * 0.9, COBRE, 8, punta=False, z=0.6)
    return D.P(VERDE, [BG("bg_nucleos"), hilo, IMG("manos_tejer", ancho=700, z=0.65, y=1250, anim={"balanceo": [3, 0.5]}, keys=K(d, (0, {"x": 300}), (0.9, {"x": 760})))],
               cam(1.0, 1.04, (540, 1050), (540, 1050)), vineta=0.6,
               hud=[D.rotulo(0.05, d - 0.02, "COBRE", tam=64, color="#111111", capsula=AMBAR, x=540, y=1640)])


@D.plano(120, "por dentro o por fuera: dos flechas")
def _(d):
    return D.P(VERDE, [BG("bg_nucleos")], cam(1.6, 1.7, (380, 980), (420, 990)), vineta=0.65,
               hud=[D.rotulo(0.05, d - 0.02, "DENTRO", tam=56, color="#111111", capsula=LIMA, x=330, y=1560),
                    D.rotulo(0.35, d - 0.02, "FUERA", tam=56, color="#ffffff", capsula="#ff4a3ae6", x=750, y=1560)])


@D.plano(125, "diminutos anillos magnéticos")
def _(d):
    return D.P(VERDE, [BG("bg_nucleos")], cam(2.2, 2.4, (460, 1000), (460, 1000)), vineta=0.65,
               hud=[D.amarillo(0.05, d - 0.02, "ANILLOS MAGNÉTICOS", y=1720, tam=80)])


def cable(pts, t0, t1, g=14):
    return {"tipo": "flecha", "puntos": pts, "grosor": g, "color": COBRE, "punta": False, "z": 0.6, "keys": [{"t": t0, "progreso": 0}, {"t": t1, "progreso": 1}]}


@D.plano(129, "dentro: un uno")
def _(d):
    return D.P(VERDE, [brillo(540, 960, 500, LIMA, 0.15), cable([[540, 1060], [700, 1200], [1080, 1330]], 0.5 * d, 0.85 * d),
               IMG("anillo", ancho=820, x=540, y=1000, z=0.5), cable([[0, 640], [300, 820], [540, 1000]], 0.05, 0.5 * d)],
               cam(1.0, 1.03, (540, 1000), (540, 1000)), "desenfoque", vineta=0.6,
               hud=[D.dato(0.4 * d, d - 0.02, "1", "", y=1600, tam=200, color=LIMA)], sfx=[(0.45 * d, "ding", -14)])


@D.plano(133, "fuera: un cero")
def _(d):
    return D.P(VERDE, [brillo(540, 960, 500, "#ff4a3a", 0.12), IMG("anillo", ancho=820, x=540, y=1000, z=0.5),
               cable([[0, 760], [250, 800], [540, 760], [840, 800], [1080, 900]], 0.05, 0.6 * d)],
               cam(1.0, 1.03, (540, 1000), (540, 1000)), vineta=0.6,
               hud=[D.dato(0.35 * d, d - 0.02, "0", "", y=1600, tam=200, color="#ff6a5a")], sfx=[(0.4 * d, "tic", -12)])


@D.plano(136, "con eso aterrizaron: el módulo baja")
def _(d):
    pol = {"tipo": "particulas", "clase": "polvo", "color": "#d8d8d8", "area": [300, 1300, 820, 1420], "n": 50, "tam": [4, 10], "vel": [0, -40], "z": 0.65, "semilla": 7}
    return D.P(["#02030a", "#02030a"], [BG("bg_superficie_rica"), *satelites(d), IMG("tierra_hd", ancho=240, x=820, y=420, z=0.1, anim={"girar": 3}),
               IMG("modulo_lunar_det", ancho=420, x=560, z=0.6, keys=K(d, (0, {"y": 700}), (0.85, {"y": 1230, "ease": "salida"}))), pol],
               cam(1.0, 1.05, (540, 1100), (560, 1150)), "zoom", vineta=0.6, sfx=[(0.05, "meteoro", -24), (0.85 * d, "golpe", -14)])


@D.plano(139, "en la Luna: 20 de julio de 1969")
def _(d):
    return D.P(["#02030a", "#02030a"], [BG("bg_superficie_rica"), *satelites(d), IMG("tierra_hd", ancho=240, x=820, y=420, z=0.1, anim={"girar": 3}),
               IMG("modulo_lunar_det", ancho=420, x=560, y=1230, z=0.6), D.fugaz(0.2, 200, 300, 520, 200)],
               cam(1.15, 1.2, (560, 1150), (560, 1150)), vineta=0.6, hud=[D.contexto(0.0, d - 0.02, "ALUNIZAJE")])


@D.plano(142, "bucle: y tú lo usas para ver vídeos como este")
def _(d):
    return D.P(TALLER, taller(movil(540, 1100, 560, nombre="movil_video", anim={"flotar": [8, 2]}),
               *agc(860, 1500, 240, keys=K(d, (0, {"op": 0}), (0.5, {"op": 0}), (0.65, {"op": 1})))),
               cam(1.15, 1.0, (540, 1050), (540, 1150)), "zoom", vineta=0.6)


D.construir("03", "movil-apolo-11", ["millón", "Apolo", "treinta", "kilos", "maletín", "memoria", "kilobytes", "megahercios", "gigas",
                                     "tejía", "mano", "anillos", "uno", "cero", "Luna"], {"generar": "misterio", "semilla": 31, "db": -13})
