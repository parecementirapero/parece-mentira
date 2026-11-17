"""«La Luna se aleja» — ejemplo completo del MÉTODO DENSO (DECISIONS 2026-11-16). Guía: `motor/DENSO.md`.

Uso (desde cualquier sitio): python3 gen.py DIR_SALIDA [audio.mp3 alineacion.json]
Sin audio monta con tiempos provisionales (silencio + alineación estimada) para ir viendo la hoja de fotogramas.
Después:  python3 -m motor.render DIR_SALIDA/episodio.json --salida DIR_SALIDA/out
"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
from motor import denso  # noqa: E402

# Variantes (motor/APRENDIZAJE.md):  python3 gen.py DIR voz.mp3 alineacion.json [palabra] [corta]
#   palabra → subtítulo de 1–2 palabras enormes (H1)     corta → versión de ~35 s con la misma locución (H2)
#   micro → 8 s en bucle, solo gancho + dato (H8)
OPC = set(sys.argv[4:])
CORTA = [(23, 56), (105, 126)] if "corta" in OPC else ()
if "micro" in OPC:   # H8: micro-Short de ~8 s en bucle: solo el gancho y el dato («Mira tus uñas… tres coma ocho centímetros al año»)
    CORTA = [(23, 155)]   # fuera: «¿Cómo lo sabemos?…dos segundos y medio» y «almeja…dieciocho horas»
v = Video(sys.argv[1], os.path.join(AQUI, "guion.txt"), *(sys.argv[2:4] if len(sys.argv) > 3 else ()), omitir=CORTA)

# ------------------------------------------------------------------ detalles de fondo que duran (atados a palabras)
SAT = [(0.8, v.w(61), (-100, 1680), (1180, 1480)), (v.w(113), v.FIN, (1180, 260), (-100, 420))]  # dos satélites
T_DINO0, T_DINO1 = v.w(86) - 0.3, v.w(105) + 0.3  # tramo de los dinosaurios


def satelite(d, z=0.15):
    """Los dos satélites que cruzan despacio los planos de espacio. Señal suave al entrar en un plano donde se ven
    (como mucho cada 2,6 s), con paneo según por dónde van."""
    T = v.ini + 0.25
    for T0, T1, p0, p1 in SAT:
        if T0 + 0.3 <= T <= T1 - 0.5 and d >= 0.9:
            x = p0[0] + (p1[0] - p0[0]) * (T - T0) / (T1 - T0)
            fx_espaciado("satelite", T, "senal", -28, 2.6, pan=round(max(-0.8, min(0.8, x / 540 - 1)), 2))
    return [IMG("satelite", ancho=150, z=z, rot=-15, anim={"girar": 4}, keys=recorrido(*SAT[0], d)),
            IMG("satelite", ancho=120, z=z, rot=20, anim={"girar": -4}, keys=recorrido(*SAT[1], d))]


def pterosaurios(d):
    return [IMG("pterosaurio", ancho=ancho, z=z, ex=-1, anim={"flotar": [14, 0.9 + i * 0.2]}, keys=recorrido(T_DINO0, T_DINO1, (1200 + dx, y), (-250 + dx, y + 60), d))
            for i, (dx, y, ancho, z) in enumerate([(0, 430, 300, 0.3), (220, 360, 200, 0.22), (420, 500, 160, 0.18)])]


# ================================================================== PLANOS (en orden de guion)
@v.plano(0, "uñas: gancho")
def _(d):
    # El primer segundo decide si se quedan (APRENDIZAJE.md): el dedo ya está subiendo en el fotograma 0, la uña «crece»
    # y la Luna sale disparada a la vez. Nada quieto.
    return P(["#2a1a14", "#120a08"], [brillo(540, 650, 700, "#ffcf9a", 0.5, pulso=[0.12, 0.7]), estrellas(20, 9),
             brillo(0, 0, 130, "#dfe6ff", 0.55, 0.19, keys=K(d, (0, {"x": 820, "y": 900}), (0.35, {"x": 835, "y": 880}), (1, {"x": 960, "y": 640, "ease": "entrada"}))),
             luna(0, 0, 190, 0.2, keys=K(d, (0, {"x": 820, "y": 900, "escala": 1.15}), (0.35, {"x": 835, "y": 880, "escala": 1.1}), (1, {"x": 960, "y": 640, "escala": 0.6, "ease": "entrada"}))),
             flecha([[850, 860], [940, 690]], d * 0.4, d * 0.95, CIAN, 7, [16, 12], z=0.18),
             IMG("dedo", ancho=600, x=440, z=0.7, keys=K(d, (0, {"y": 1560, "rot": -7, "ey": 1.0}), (0.3, {"y": 1400, "rot": 0, "ease": "elastico"}), (1, {"y": 1350, "ey": 1.07, "ease": "suave"})))],
             cam(1.12, 1.3, (540, 1080), (560, 960)), vineta=0.7, sfx=[(0.02, "golpe", -12), (d * 0.4, "brillo", -20)])


@v.plano(3, "la Luna se aleja")
def _(d):
    return P(ESPACIO, [BG("bg_esp_violeta"), estrellas(), tierra(260, 1250, 620, giro=6),
             luna(0, 0, 220, 0.5, keys=K(d, (0, {"x": 700, "y": 820}), (0.75, {"x": 900, "y": 515, "ease": "salida"}))),
             *lineas_vel(820, 700, 2), flecha([[560, 1040], [826, 633]], 0.15, d * 0.85, CIAN, 9, [20, 14]),
             fugaz(0.2, 900, 200, 620, 380), *satelite(d)],
             cam(1.0, 1.08, (500, 1000), (600, 880)), "desenfoque", sfx=[(0.1, "whoosh", -12, {"dur": 0.7})])


@v.plano(9, "misma velocidad: uña = Luna")
def _(d):
    return P(["#120b1a", "#0a1030"], [
        {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 960, "relleno": ["#3a2418", "#1a0f0a"], "x": 540, "y": 480, "z": 0.05},
        brillo(540, 420, 520, "#ffcf9a", 0.4, 0.06),
        IMG("dedo", ancho=420, x=540, z=0.5, ey=1.0, keys=K(d, (0, {"y": 560, "ey": 1.0, "ease": "lineal"}), (1, {"y": 520, "ey": 1.12}))),
        {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 960, "relleno": ["#060814", "#0a1030"], "x": 540, "y": 1440, "z": 0.05},
        polvo("#ffffff", 30, (0, 970, 1080, 1920), 4, "estrellas"),
        IMG("tierra_hd", ancho=360, x=230, y=1500, z=0.4, anim={"girar": 5}),
        luna(0, 0, 150, 0.45, keys=K(d, (0, {"x": 640, "y": 1400, "ease": "lineal"}), (0.8, {"x": 900, "y": 1310}))),
        {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 10, "relleno": "#ffd23f", "x": 540, "y": 962, "z": 0.6},
        flecha([[440, 1470], [800, 1345]], 0.2, d * 0.8, MAGENTA, 6, [16, 12])],
        cam(1.0, 1.03), hud=[rotulo(0.3, d - 0.1, "=", tam=260, color="#ffd23f", capsula="#0d1330d8", x=540, y=960, fijo=True)])


@v.plano(17, "3,8 cm")
def _(d):
    x0, x1 = 540 - 480 + 18, 540 - 480 + 18 + 365   # 0 cm y 3,8 cm sobre la regla
    return P(ESPACIO, [BG("bg_esp_petroleo"), estrellas(25, 5), brillo(540, 900, 700, "#9fb3ff", 0.25),
             IMG("regla", ancho=1000, x=540, y=1050, z=0.5, keys=K(d, (0, {"rot": -4}), (1, {"rot": -1}))),
             # la Luna recorre en un año lo que mide la barra: el dato se VE, no solo se lee
             brillo(0, 800, 150, "#dfe6ff", 0.5, 0.54, keys=K(d, (0.05, {"x": x0 + 182}), (0.7, {"x": x1 + 182, "ease": "salida"}))),
             luna(0, 800, 120, 0.56, keys=K(d, (0.05, {"x": x0 + 182}), (0.7, {"x": x1 + 182, "ease": "salida"}))),
             flecha([[x0 + 182, 800], [x1 + 110, 800]], 0.08, d * 0.7, CIAN, 6, [14, 10], punta=False),
             IMG("dedo", ancho=210, x=175, y=1560, z=0.45, rot=8, keys=K(d, (0, {"y": 1640}), (0.5, {"y": 1540, "ease": "salida"}))),
             {"tipo": "barra", "x": 540 - 480 + 18 + 182, "y": 920, "ancho": 365, "alto": 44, "color": "#ff5a4a", "fondo": "#ffffff15", "z": 0.55,
              "keys": K(d, (0.05, {"progreso": 0}), (0.7, {"progreso": 1, "ease": "salida"}))}],
             cam(1.15, 1.3, (380, 1000), (420, 980)), "zoom",
             hud=[{**contador(0.1, d - 0.1, 0, 3.8, d * 0.6, "CM", tam=130), "decimales": 1}],
             sfx=[(0.15 + i * 0.12, "tic", -24) for i in range(6)])


@v.plano(21, "al año: hoja de calendario")
def _(d):
    return P(["#3a2a1c", "#1a1410"], [brillo(540, 900, 700, "#ffcf8a", 0.35), IMG("calendario", ancho=640, x=540, y=1000, z=0.59),
             IMG("calendario", ancho=640, x=540, y=1000, z=0.6, keys=K(d, (0.15, {"y": 1000, "rot": 0, "op": 1}), (0.85, {"y": 380, "rot": -35, "op": 0, "ease": "entrada"})))],
             cam(1.0, 1.05, (540, 1000), (540, 1000)), sfx=[(0.15, "whoosh", -16, {"dur": 0.3})])


@v.plano(23, "¿cómo lo sabemos?")
def _(d):
    return P(ESPACIO, [BG("bg_esp_violeta"), *satelite(d), estrellas(30, 6), luna(540, 800, 520, 0.5, anim={"girar": 3}),
             brillo(540, 800, 500, "#dfe6ff", 0.25, 0.45, pulso=[0.15, 0.6])], cam(1.0, 1.2, (540, 900), (540, 880)), "zoom",
             hud=[amarillo(0.05, d - 0.03, "¿CÓMO?", y=1300, tam=110, color=CIAN)])


def cuenta(n):
    """Cuenta atrás EN la rampa de lanzamiento: mismo encuadre que el despegue, cada número más cerca y con más humo,
    para que los tres micro planos y el despegue se lean como una sola acción."""
    def fn(d):
        k = 3 - n  # 0, 1, 2
        zoom = [(1.0, 1.05), (1.18, 1.24), (1.4, 1.48)][k]
        humo = [brillo(540 + dx, 1650 + dy, 200 + 40 * k, "#d9d2c8", 0.25 + 0.15 * k, 0.55, pulso=[0.15, 0.2])
                for dx, dy in [(-240, 30), (-110, 60), (0, 80), (130, 50), (250, 40)][:1 + 2 * k]]
        torre = [{"tipo": "forma", "forma": "rect", "ancho": 26, "alto": 620, "relleno": ["#5a6274", "#2b3140"], "x": 700, "y": 1300, "z": 0.5},
                 *[{"tipo": "forma", "forma": "rect", "ancho": 130, "alto": 12, "relleno": "#5a6274", "x": 640, "y": 1050 + i * 150, "z": 0.5} for i in range(3)],
                 {"tipo": "forma", "forma": "circulo", "radio": 12, "relleno": "#ff5a4a", "x": 700, "y": 975, "z": 0.52, "anim": {"parpadeo": [0.3, 0.0]}}]
        return P(["#0b1838", "#e88a4a"], [brillo(540, 1500, 900, "#ffb45a", 0.35 + 0.08 * k), polvo("#ffffff", 30, (0, 0, 1080, 900), 7, "estrellas"),
                 *torre, IMG("cohete", ancho=230, x=540, y=1150, z=0.6, anim={"temblor": [1.5 + 2 * k, 0.05]} if k else {}),
                 brillo(540, 1560, 120 + 50 * k, "#ffe9a0", 0.5 + 0.2 * k, 0.59, pulso=[0.3, 0.1]), *humo],
                 {"zoom": list(zoom), "foco": [[540, 1150], [540, 1150]], "pan": [[0, 0], [0, 0]], "temblor": 2 * k},
                 "desenfoque" if n == 3 else "corte", 0.2,
                 hud=[rotulo(0.0, d, str(n), tam=230, x=250, y=760, color="#ff5a4a", sin_pop=True, fijo=True)], sfx=[(0.0, "tic", -14)])
    return fn


v.plano(26, "cuenta atrás 3")(cuenta(3))
v.plano(26, "cuenta atrás 2", mas=0.32)(cuenta(2))
v.plano(26, "cuenta atrás 1", mas=0.64)(cuenta(1))


@v.plano(29, "despegue 1969")
def _(d):
    humo = [brillo(540 + dx, 1640 + dy, 260, "#d9d2c8", 0.6, 0.55, keys=K(d, (0.05, {"op": 0, "escala": 0.5}), (0.6, {"op": 1, "escala": 1.4})))
            for dx, dy in [(-260, 30), (-120, 60), (0, 80), (140, 50), (270, 40)]]
    return P(["#0b1838", "#e88a4a"], [brillo(540, 1500, 900, "#ffb45a", 0.5), polvo("#ffffff", 30, (0, 0, 1080, 900), 7, "estrellas"),
             IMG("cohete", ancho=230, x=540, z=0.6, keys=K(d, (0, {"y": 1150}), (1, {"y": 600, "ease": "entrada"}))),
             brillo(540, 0, 140, "#ffe9a0", 1.0, 0.59, keys=K(d, (0, {"y": 1630}), (1, {"y": 1080, "ease": "entrada"})), pulso=[0.3, 0.12]), *humo],
             {"zoom": [1.0, 1.05], "foco": [[540, 1000], [540, 800]], "pan": [[0, 0], [0, 0]], "temblor": 6},
             hud=[{**contador(0.05, d - 0.05, 1960, 1969, d * 0.5, tam=120, y=560, capsula="#c0392be6"), "miles": False}],
             sfx=[(0, "golpe", -12), (0, "rumor", -9, {"dur": d + 0.3})])


@v.plano(32, "Apolo 11 aluniza")
def _(d):
    return P(["#02030a", "#02030a"], [BG("bg_superficie_rica"), IMG("tierra_hd", ancho=220, x=840, y=380, z=0.1, anim={"girar": 3}),
             IMG("modulo_lunar", ancho=600, x=520, z=0.6, keys=cae(0, d * 0.85, 700, 1180, 0.05)),
             *[brillo(520 + dx, 1400, 200, "#c9c6bb", 0.7, 0.62, keys=K(d, (0.75, {"op": 0, "escala": 0.4}), (1, {"op": 1, "escala": 1.3}))) for dx in (-220, 0, 220)],
             polvo("#dcd8cc", 30, (200, 1250, 880, 1500), 8)],
             cam(1.0, 1.08, (540, 1100), (540, 1150)), "zoom", hud=[contexto(0.05, d - 0.05, "APOLO 11")], sfx=[(d * 0.85 * 0.36, "golpe", -11)])


@v.plano(36, "micro: primera huella")
def _(d):
    return P(["#8d8a82", "#5d5a54"], [BG("bg_superficie_rica"), polvo("#dcd8cc", 25, (200, 800, 880, 1300), 30),
             {"tipo": "huella", "clase": "bota", "largo": 300, "x": 540, "y": 1150, "z": 0.6, "rot": 12, "keys": K(d, (0, {"marca": 0}), (0.5, {"marca": 1}))}],
             cam(1.6, 1.7, (540, 1150), (540, 1150)), sfx=[(0.02, "golpe", -20)])


@v.plano(38, "espejos")
def _(d):
    return P(["#02030a", "#02030a"], [BG("bg_superficie_rica"), IMG("astronauta", ancho=360, x=300, y=1240, z=0.6, anim={"balanceo": [3, 0.8]}),
             IMG("retro", ancho=520, x=700, y=1380, z=0.65, keys=K(d, (0, {"y": 1300, "op": 0}), (0.3, {"y": 1380, "op": 1, "ease": "salida"}))),
             brillo(640, 1330, 160, "#ffffff", 1.0, 0.7, keys=K(d, (0.35, {"op": 0, "escala": 0.3}), (0.55, {"op": 1, "escala": 1.2}), (1, {"op": 0.4}))),
             senala(700, 1380, d * 0.3, d - 0.05, 250, AMBAR)],
             cam(1.15, 1.25, (560, 1280), (600, 1300)), hud=[amarillo(0.02, d - 0.02, "ESPEJOS", y=700, x=640)], sfx=[(d * 0.4, "brillo", -13)])


@v.plano(39, "micro: el láser se carga")
def _(d):
    return P(["#05070f", "#0b1430"], [BG("bg_esp_petroleo"), IMG("observatorio", ancho=1180, x=540, y=960, z=0.3),
             brillo(520, 1080, 220, "#5dff7a", 0.9, 0.5, keys=K(d, (0, {"op": 0.1, "escala": 0.3}), (0.9, {"op": 1, "escala": 1.2})), pulso=[0.25, 0.1]),
             polvo("#9dffb0", 30, (420, 980, 620, 1180), 31, "chispas")],
             cam(2.2, 2.4, (520, 1100), (520, 1080)), "desenfoque", 0.25, sfx=[(0.05, "rumor", -20, {"dur": d})])


@v.plano(42, "se dispara un láser")
def _(d):
    return P(["#05070f", "#0b1430"], [BG("bg_esp_petroleo"), *satelite(d), luna(780, 260, 200), fugaz(d * 0.5, 160, 300, 420, 160),
             IMG("observatorio", ancho=1180, x=540, y=960, z=0.3),
             flecha([[520, 1080], [770, 290]], d * 0.3, d * 0.6, LIMA, 10, punta=False),
             brillo(520, 1080, 160, "#5dff7a", 0.9, 0.5, keys=K(d, (0.25, {"op": 0}), (0.35, {"op": 1})), pulso=[0.3, 0.2])],
             cam(1.1, 1.0, (540, 1050), (560, 900)), hud=[amarillo(0.2, d - 0.05, "LÁSER", y=640, x=300, color=LIMA)], sfx=[(d * 0.3, "zap", -11)])


@v.plano(46, "la luz rebota")
def _(d):
    return P(ESPACIO, [BG("bg_esp_petroleo"), *satelite(d), estrellas(25, 10), tierra(240, 1420, 520), luna(820, 560, 260),
             flecha([[330, 1300], [800, 590]], 0.0, d * 0.4, LIMA, 9),
             flecha([[790, 640], [350, 1330]], d * 0.5, d * 0.95, MAGENTA, 9, [22, 14]),
             brillo(800, 590, 200, "#ffffff", 1.0, 0.55, keys=K(d, (0.35, {"op": 0, "escala": 0.3}), (0.48, {"op": 1, "escala": 1.4}), (0.9, {"op": 0})))],
             cam(1.05, 1.0, (560, 960), (540, 960)), sfx=[(d * 0.4, "ding", -16, {"f": 1320})])


@v.plano(50, "vuelve en 2,5 s")
def _(d):
    return P(["#1b2236", "#0b0f1c"], [brillo(540, 1000, 700, "#9fb3ff", 0.3), polvo("#cfe0ff", 20, sem=11), *cronometro(0, 900, 0.1, d * 0.75),
             # debajo, el viaje que se está cronometrando: la luz va a la Luna y vuelve
             tierra(190, 1620, 200, 0.5), luna(900, 1620, 120, 0.5),
             {"tipo": "forma", "forma": "rect", "ancho": 600, "alto": 3, "relleno": "#5dff7a55", "x": 545, "y": 1620, "z": 0.45},
             brillo(0, 1620, 60, "#5dff7a", 1.0, 0.55, keys=[{"t": 0.1, "x": 300, "ease": "lineal"}, {"t": 0.1 + d * 0.325, "x": 840, "ease": "lineal"}, {"t": 0.1 + d * 0.65, "x": 300}])],
             cam(1.0, 1.08, (540, 1100), (540, 1100)), "zoom", vineta=0.5,
             hud=[{**contador(0.1, d - 0.05, 0, 2.5, d * 0.6, "SEGUNDOS", y=1560), "decimales": 1},
                  contexto(0.1, d - 0.05, "384.400 KM HASTA LA LUNA")],
             sfx=[(0.15 + i * 0.16, "tic", -22) for i in range(int(d / 0.16) - 1)])


@v.plano(56, "¿y por qué se va?")
def _(d):
    return P(ESPACIO, [BG("bg_esp_violeta"), *satelite(d), estrellas(30, 13), tierra(400, 1200, 600, giro=8),
             luna(0, 0, 200, 0.55, keys=K(d, (0, {"x": 700, "y": 760}), (1, {"x": 1000, "y": 420, "ease": "entrada"}))), *lineas_vel(900, 520, 4)],
             cam(1.0, 1.06, (540, 960), (600, 900)), "desenfoque", hud=[amarillo(0.1, d - 0.05, "¿POR QUÉ?", y=600, x=360, color=MAGENTA)])


@v.plano(61, "mareas")
def _(d):
    return P(["#0e3a5c", "#05192b"], [brillo(540, 600, 700, "#9fd8ff", 0.35),
             {"tipo": "agua", "nivel": 1000, "lado": "abajo", "amplitud": 40, "colores": ["#2a8bd0", "#0b4a7a"], "z": 0.4,
              "keys": K(d, (0, {"nivel": 1150}), (0.9, {"nivel": 820, "ease": "suave"}))},
             luna(860, 360, 220, 0.2), polvo("#e6f6ff", 30, (0, 900, 1080, 1700), 14, "burbujas"),
             IMG("yate", ancho=420, x=330, z=0.45, anim={"flotar": [10, 1.2], "balanceo": [4, 1.4]}, keys=K(d, (0, {"y": 1110}), (0.9, {"y": 790, "ease": "suave"})))],
             cam(1.0, 1.08, (540, 1000), (540, 1050)), "zoom", hud=[amarillo(0.1, d - 0.05, "MAREAS", y=1650, color=CIAN)], sfx=[(0.02, "agua", -11, {"dur": d + 0.3})])


@v.plano(64, "el agua frena")
def _(d):
    return P(ESPACIO, [BG("bg_esp_violeta"), *satelite(d), estrellas(25, 15), IMG("marea", ancho=900, x=540, y=1050, z=0.35, rot=-10, anim={"pulso": [0.02, 1.0]}),
             tierra(540, 1050, 560, giro=-4), luna(980, 880, 150),
             flecha([[300, 780], [540, 680], [780, 780]], 0.1, d * 0.7, AMBAR, 14, z=0.6),
             {"tipo": "forma", "forma": "poligono", "puntos": [[-60, -20], [60, -20], [60, 20], [-60, 20]], "relleno": "#d62f22", "x": 540, "y": 650, "z": 0.62,
              "keys": K(d, (0.6, {"op": 0, "escala": 0.5}), (0.8, {"op": 1, "escala": 1.0, "ease": "elastico"}))}],
             cam(1.0, 1.1, (540, 960), (540, 900)), "desenfoque", hud=[contexto(0.05, d - 0.05, "FRENA")], sfx=[(d * 0.6, "pop", -14)])


@v.plano(67, "como una patinadora")
def _(d):
    giros, t, per = [], 0.0, 0.06
    while t < d:
        giros.append({"t": round(t, 3), "ex": 1.0 if len(giros) % 2 == 0 else -1.0, "ease": "lineal"})
        t += per; per *= 1.0 if t < d * 0.4 else 1.35
    corte = d * 0.4
    return P(["#0b1430", "#9fd0ff"], [BG("bg_pista"),
             IMG("patinadora_cerrada", ancho=620, x=540, y=1050, z=0.6, keys=[{"t": 0, "op": 1}, {"t": corte - 0.02, "op": 1}, {"t": corte, "op": 0}] + [g for g in giros if g["t"] < corte]),
             IMG("patinadora_abierta", ancho=620, x=540, y=1050, z=0.61, keys=[{"t": 0, "op": 0}, {"t": corte - 0.02, "op": 0}, {"t": corte, "op": 1}] + [g for g in giros if g["t"] >= corte - 0.02]),
             polvo("#ffffff", 25, (150, 1300, 930, 1650), 32, "chispas")],
             cam(1.0, 1.05, (540, 1100), (540, 1100)), hud=[contexto(0.03, d - 0.03, "PATINADORA")], sfx=[(0.02, "whoosh", -18, {"dur": d})])


@v.plano(72, "empuja a la Luna hacia fuera (plano largo)")
def _(d):
    orb1 = {"tipo": "forma", "forma": "elipse", "ancho": 600, "alto": 600, "relleno": "#ffffff", "op_relleno": 0, "grosor": 3, "borde": CIAN + "aa", "x": 540, "y": 1000, "z": 0.3}
    orb2 = {"tipo": "forma", "forma": "elipse", "ancho": 880, "alto": 880, "relleno": "#ffffff", "op_relleno": 0, "grosor": 5, "borde": MAGENTA,
            "x": 540, "y": 1000, "z": 0.3, "keys": K(d, (0.15, {"op": 0, "escala": 0.68}), (0.8, {"op": 1, "escala": 1.0}))}
    return P(ESPACIO, [BG("bg_esp_violeta"), *satelite(d), estrellas(30, 16), orb1, orb2, tierra(540, 1000, 280, giro=10),
             luna(0, 0, 120, 0.5, keys=K(d, (0, {"x": 840, "y": 1000}), (0.35, {"x": 860, "y": 740}), (0.7, {"x": 820, "y": 640}), (1, {"x": 940, "y": 740}))),
             *[flecha([[540 + dx * 160, 1000 + dy * 160], [540 + dx * 400, 1000 + dy * 400]], d * (0.1 + i * 0.05), d * (0.35 + i * 0.05), AMBAR, 6, z=0.35)
               for i, (dx, dy) in enumerate([(0.7, -0.7), (-0.7, -0.7), (0.7, 0.7), (-0.7, 0.7)])], fugaz(d * 0.7, 120, 300, 380, 420)],
             cam(1.07, 1.0), "zoom", hud=[amarillo(d * 0.35, d - 0.05, "HACIA FUERA", y=545, tam=80, color=CIAN)], sfx=[(0.2, "whoosh", -13, {"dur": 1.2}), (d * 0.15, "subida", -20, {"dur": d * 0.6})])


@v.plano(81, "resultado")
def _(d):
    return P(ESPACIO, [BG("bg_esp_ambar"), estrellas(25, 41),
             IMG("tierra_hd", ancho=1000, x=540, y=1000, z=0.3, op=0.55, keys=[{"t": 0, "rot": 0, "ease": "lineal"}, {"t": d, "rot": 55, "ease": "salida"}]),
             brillo(540, 1000, 520, "#ffcf8a", 0.3, 0.35), *reloj(540, 1000, 520, 3, 0, 9, 0, 0.0, d)],
             cam(1.15, 1.25, (540, 960), (540, 960)), "zoom", 0.25, vineta=0.6, sfx=[(0.0, "tictac", -15, {"dur": d, "ritmo": 0.2})])


@v.plano(82, "los días se alargan")
def _(d):
    soles = [{**s, "keys": K(d, (0, {"x": 120, "y": 760, "ease": "lineal"}), (1, {"x": 960, "y": 500}))} for s in sol(0, 0, 90, 0.07)]
    return P(["#4f9be0", "#fbe8c2"], [BG("campo_dia"), *soles, *reloj(540, 1180, 520, 6, 0, 18, 0, 0.1, d), polvo("#ffffff", 20, sem=17)],
             cam(1.0, 1.06, (540, 1100), (540, 1100)), vineta=0.4,
             hud=[{**contador(0.05, d - 0.03, 0, 1.8, d * 0.35, "MS POR SIGLO", tam=96, y=1620, contar_prefijo="+"), "decimales": 1}],
             sfx=[(0.05, "tictac", -17, {"dur": d - 0.1, "ritmo": 0.25})])


T_MET = v.w(103)  # segundo en que cae el meteorito (micro plano antes de salir de los dinosaurios)
BRAQ = (230, 1135, 620)  # braquiosaurio quieto junto a su rama (x, y, ancho); su cabeza queda en ≈(488, 958)


def comer(d, mordiscos, rama_antes, rama_despues, t_cambio=None):
    """Braquiosaurio que come de una rama: cabecea en cada mordisco (fracciones del plano), caen trocitos de hoja
    y suena el mordisco. La rama cambia de `rama_antes` a `rama_despues` en el primer mordisco."""
    ks = [{"t": 0, "rot": 0}]
    bits, son = [], []
    for f in mordiscos:
        t = f * d
        ks += [{"t": round(t - 0.16, 3), "rot": 0}, {"t": round(t, 3), "rot": 4}, {"t": round(t + 0.2, 3), "rot": 0}]
        son.append((t, "mordisco", -15))
        for i in range(5):
            bits.append({"tipo": "forma", "forma": "elipse", "ancho": 22, "alto": 10, "relleno": ["#62a83c", "#3f7a2a"], "z": 0.3, "rot": 30 * i,
                         "keys": [{"t": t, "x": 500 + i * 8, "y": 975, "op": 0}, {"t": t + 0.03, "op": 1},
                                  {"t": t + 0.55, "x": 470 + i * 26, "y": 1160 + i * 14, "rot": 200 + 40 * i, "op": 0, "ease": "entrada"}]})
    tc = (t_cambio if t_cambio is not None else (mordiscos[0] * d if mordiscos else 0))
    ramas = [IMG(rama_antes, ancho=300, x=600, y=950, z=0.24, keys=[{"t": 0, "op": 1}, {"t": tc, "op": 1}, {"t": tc + 0.02, "op": 0}]),
             IMG(rama_despues, ancho=300, x=600, y=950, z=0.24, keys=[{"t": 0, "op": 0}, {"t": tc, "op": 0}, {"t": tc + 0.02, "op": 1}])]
    return [*ramas, IMG("dino_braquio", ancho=BRAQ[2], x=BRAQ[0], y=BRAQ[1], z=0.25, keys=ks), *bits], son


def meteoro_lejos(d):
    """El meteorito, pequeño y lejano, que se acerca por el cielo durante todos los planos de dinosaurios."""
    return [brillo(0, 0, 150, "#ffb060", 0.5, 0.11, keys=recorrido(T_DINO0 + 0.2, T_MET, (90, 600), (230, 760), d, esc=(0.4, 1.2))),
            IMG("meteorito", ancho=420, z=0.12, ex=-1, rot=49, keys=recorrido(T_DINO0 + 0.2, T_MET, (90, 600), (230, 760), d, esc=(0.22, 0.62)))]


@v.plano(86, "dinosaurios comiendo")
def _(d):
    come, son = comer(d, [0.6], "rama_hojas", "rama_mordida1")
    f = 0.3  # el triceratops muerde su arbusto
    return P(["#2b1b3a", "#f6d08a"], [BG("bg_jungla"), *meteoro_lejos(d), *pterosaurios(d), *come,
             IMG("arbusto", ancho=250, x=540, y=1505, z=0.5),
             IMG("dino_trice", ancho=500, x=790, y=1440, z=0.5, ex=-1,
                 keys=[{"t": 0, "rot": 0}, {"t": f * d - 0.15, "rot": 0}, {"t": f * d, "rot": -5}, {"t": f * d + 0.2, "rot": 0}]),
             polvo("#ffd9a0", 25, sem=18),
             *[IMG("dino_raptor", ancho=330, z=0.8, anim={"balanceo": [3, 0.35]}, keys=K(d, (0, {"x": -200 - i * 160, "y": 1680 + i * 40, "ease": "lineal"}), (1, {"x": 520 - i * 160, "y": 1680 + i * 40})))
               for i in range(2)],
             {**brillo(300, 640, 200, "#6b5a5a", 0.5, 0.06), "anim": {"deriva": [10, -60]}}],
             cam(1.0, 1.06, (540, 1200), (500, 1200)), "zoom", vineta=0.5, sfx=[(f * d, "mordisco", -16), *son, (0.1, "golpe", -19)])


@v.plano(89, "23,5 horas (plano largo)")
def _(d):
    come, son = comer(d, [0.3, 0.75], "rama_mordida1", "rama_mordida2")
    return P(["#2b1b3a", "#f6d08a"], [BG("bg_jungla"), *meteoro_lejos(d), *pterosaurios(d), *come,
             IMG("dino_trex", ancho=560, z=0.35, anim={"balanceo": [1.5, 1.0]}, keys=K(d, (0, {"x": 1350, "y": 1400, "ease": "lineal"}), (1, {"x": 820, "y": 1400})), ex=-1),
             {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 1920, "relleno": "#000000", "x": 540, "y": 960, "z": 0.4, "op": 0.22},
             *reloj(800, 800, 380, 0, 0, 23, 30, 0.1, d * 0.8),
             IMG("dino_estego", ancho=430, z=0.8, keys=K(d, (0, {"x": -260, "y": 1680, "ease": "lineal"}), (1, {"x": 260, "y": 1680})))],
             cam(1.0, 1.05, (540, 1000), (540, 1000)),
             hud=[{**contador(0.15, d - 0.05, 24, 23.5, d * 0.5, "HORAS", tam=96, x=800, y=1090), "decimales": 1}, contexto(0.1, d - 0.05, "HACE 70 MILLONES DE AÑOS")],
             sfx=[(0.1, "tictac", -19, {"dur": d * 0.8, "ritmo": 0.25})] + son + [(0.3, "golpe", -21), (1.2, "golpe", -21)])


@v.plano(96, "372 días")
def _(d):
    n = 6
    come, son = comer(d, [0.45], "rama_mordida2", "rama_mordida2")
    hojas = [IMG("calendario", ancho=400, x=770, y=900, z=0.6 - i * 0.001,
                 keys=[{"t": 0.12 + i * d * 0.1, "y": 900, "rot": 0, "op": 1}, {"t": 0.42 + i * d * 0.1, "y": 330, "rot": -25 + i * 9, "op": 0, "ease": "entrada"}]) for i in range(n)]
    return P(["#2b1b3a", "#f6d08a"], [BG("bg_jungla"), *meteoro_lejos(d), *pterosaurios(d), *come,
             {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 1920, "relleno": "#000000", "x": 540, "y": 960, "z": 0.4, "op": 0.25},
             IMG("calendario", ancho=400, x=770, y=900, z=0.59), *reversed(hojas)],
             cam(1.32, 1.42, (620, 960), (660, 930)), "zoom", 0.2, vineta=0.55,   # más cerca: otro encuadre que el plano anterior
             hud=[contador(0.1, d - 0.05, 365, 372, d * 0.6, "DÍAS", tam=110, x=770, y=1230)],
             sfx=[(0.17 + i * d * 0.1, "whoosh", -25, {"dur": 0.18}) for i in range(n)] + son + [(0.0, "meteoro", -24, {"dur": d})])


@v.plano(103, "micro: cae el meteorito")
def _(d):
    cae = K(d, (0, {"x": 80, "y": 330, "escala": 0.7}), (1, {"x": 660, "y": 960, "escala": 1.3, "ease": "entrada"}))
    return P(["#2b1b3a", "#f6d08a"], [BG("bg_jungla"),
             {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 1920, "relleno": "#ff7a1a", "x": 540, "y": 960, "z": 0.05, "keys": K(d, (0, {"op": 0.05}), (1, {"op": 0.4}))},
             *pterosaurios(d), IMG("rama_mordida2", ancho=300, x=600, y=950, z=0.24),
             IMG("dino_braquio", ancho=BRAQ[2], x=BRAQ[0], y=BRAQ[1], z=0.25, keys=K(d, (0, {"rot": 0}), (0.4, {"rot": -5}))),
             IMG("dino_trice", ancho=500, x=790, y=1440, z=0.5, ex=-1),
             brillo(0, 0, 520, "#ffb060", 0.9, 0.55, keys=cae),
             IMG("meteorito", ancho=1150, z=0.6, ex=-1, rot=47, keys=cae),
             polvo("#ffd24a", 40, (0, 200, 1080, 1300), 44, "chispas"),
             {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#fff6e0", "x": 540, "y": 960, "hud": True, "z": 1, "keys": K(d, (0, {"op": 0}), (0.72, {"op": 0}), (1, {"op": 1}))}],
             {"zoom": [1.0, 1.1], "foco": [[540, 1000], [560, 1000]], "pan": [[0, 0], [0, 0]], "temblor": 12},
             sfx=[(-0.3, "meteoro", -9, {"dur": d + 0.3}), (-1.0, "subida", -17, {"dur": 1.0 + d}), (d - 0.02, "impacto", -8), (d, "rumor", -14, {"dur": 1.3})])


@v.plano(105, "rayas: lupa")
def _(d):
    return P(["#2a241c", "#120f0a"], [brillo(540, 900, 700, "#ffe2b0", 0.35), polvo("#ffe9c0", 20, sem=21),
             IMG("almeja_fosil", ancho=880, x=540, y=1050, z=0.6),
             IMG("lupa", ancho=520, x=0, y=900, z=0.7, keys=K(d, (0.2, {"x": 900}), (0.6, {"x": 540, "ease": "anticipa"}))),
             {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#fff6e0", "x": 540, "y": 960, "hud": True, "z": 1, "keys": [{"t": 0, "op": 1}, {"t": 0.4, "op": 0}]}],
             cam(1.0, 1.08, (540, 1050), (540, 1000)), "corte", vineta=0.65, hud=[contexto(0.05, d - 0.05, "1 RAYA = 1 DÍA")], sfx=[(d * 0.6, "brillo", -16)])


@v.plano(110, "almeja fósil de cerca")
def _(d):
    return P(["#2a241c", "#120f0a"], [IMG("almeja_fosil", ancho=880, x=540, y=1050, z=0.6), polvo("#ffe9c0", 15, sem=22)],
             cam(1.6, 1.8, (540, 820), (520, 800)))


@v.plano(113, "micro: un láser corta la concha")
def _(d):
    return P(["#2a241c", "#120f0a"], [IMG("almeja_fosil", ancho=880, x=540, y=1050, z=0.6),
             {"tipo": "forma", "forma": "rect", "ancho": 900, "alto": 6, "relleno": "#5dff7a", "x": 540, "z": 0.65, "keys": K(d, (0, {"y": 700, "ease": "lineal"}), (1, {"y": 1150}))},
             brillo(540, 0, 300, "#5dff7a", 0.6, 0.64, keys=K(d, (0, {"y": 700, "ease": "lineal"}), (1, {"y": 1150}))),
             polvo("#b8ffc8", 25, (300, 700, 780, 1150), 33, "chispas")],
             cam(1.3, 1.35, (540, 950), (540, 980)), sfx=[(0.02, "zap", -18, {"f0": 900, "f1": 600, "dur": d})])


@v.plano(114, "micro: tiempo hacia atrás")
def _(d):
    return P(["#1b2236", "#0b0f1c"], [brillo(540, 1000, 700, "#ff9a7a", 0.3), *cronometro(0, -1080, 0, d)],
             cam(1.1, 1.2, (540, 1050), (540, 1050)), "desenfoque", 0.2, vineta=0.7, sfx=[(0.0, "whoosh", -14, {"dur": d})])


@v.plano(116, "1.400 millones de años: la Luna cerca")
def _(d):
    return P(ESPACIO, [BG("bg_esp_ambar"), *satelite(d), estrellas(40, 22), tierra(380, 1250, 560, giro=40),
             luna(0, 0, 330, 0.5, keys=K(d, (0, {"x": 880, "y": 600, "escala": 0.48}), (0.8, {"x": 720, "y": 820, "escala": 1.0, "ease": "salida"}))),
             flecha([[965, 470], [828, 664]], 0.1, d * 0.7, "#ff3d6e", 8, [18, 12])],
             cam(1.0, 1.05),
             hud=[{**contador(0.05, d - 0.05, 0, 1400, d * 0.55, "MILLONES DE AÑOS", tam=100, y=560), "capsula": "#c0392be6"}])


@v.plano(120, "18 horas (plano largo)")
def _(d):
    return P(ESPACIO, [BG("bg_esp_ambar"), *satelite(d), estrellas(30, 23), tierra(540, 1150, 620, giro=70), luna(900, 520, 300),
             *reloj(260, 520, 300, 0, 0, 18, 0, 0.1, d * 0.7, z=0.65), fugaz(d * 0.6, 700, 200, 980, 320)],
             cam(1.0, 1.06, (540, 1000), (540, 1000)), hud=[rotulo(d * 0.4, d - 0.05, "18", unidad="HORAS", tam=130, x=270, y=800, borde=AMBAR)],
             sfx=[(0.1, "tictac", -16, {"dur": d * 0.7, "ritmo": 0.2})])


@v.plano(126, "micro: avance rápido")
def _(d):
    blanco = [fundido_blanco([{"t": 0, "op": 1}, {"t": 0.35, "op": 0}])] if CORTA else []   # en la versión corta viene del fogonazo del meteorito
    return P(["#1b2236", "#0b0f1c"], [brillo(540, 1000, 700, "#7ad0ff", 0.3), *cronometro(0, 1440, 0, d), *blanco],
             cam(1.1, 1.2, (540, 1050), (540, 1050)), "corte" if CORTA else "desenfoque", 0.2, vineta=0.7, sfx=[(0.0, "whoosh", -14, {"dur": d})])


@v.plano(129, "600 millones de años: la Luna lejos")
def _(d):
    return P(ESPACIO, [BG("bg_esp_petroleo"), *satelite(d), estrellas(40, 24), tierra(300, 1350, 480, giro=3),
             luna(0, 0, 260, 0.5, keys=K(d, (0, {"x": 640, "y": 900, "escala": 1.0}), (0.9, {"x": 900, "y": 420, "escala": 0.35, "ease": "salida"}))),
             flecha([[560, 1030], [866, 481]], 0.1, d * 0.85, CIAN, 8, [18, 12])],
             cam(1.0, 1.04), hud=[{**contador(0.05, d - 0.05, 0, 600, d * 0.5, "MILLONES DE AÑOS", tam=110, y=560), "contar_prefijo": "+", "borde": CIAN}])


@v.plano(134, "hoy / futuro")
def _(d):
    return P(ESPACIO, [BG("bg_esp_petroleo"), *satelite(d), estrellas(30, 34), luna(300, 980, 340, 0.4), fugaz(d * 0.3, 820, 300, 1040, 180),
             IMG("tierra_hd", ancho=1300, x=540, y=2150, z=0.3, anim={"girar": 3}),
             {"tipo": "forma", "forma": "rect", "ancho": 4, "alto": 900, "relleno": "#ffffff30", "x": 540, "y": 900, "z": 0.2},
             luna(780, 980, 340, 0.4, keys=K(d, (0, {"escala": 1.0, "y": 980}), (0.6, {"escala": 0.55, "y": 900, "ease": "salida"}))),
             flecha([[780, 1150], [780, 1010]], d * 0.15, d * 0.6, CIAN, 7, [14, 10], z=0.35)],
             cam(1.0, 1.04), hud=[rotulo(0.05, d - 0.05, "HOY", tam=70, x=300, y=1260), rotulo(0.1, d - 0.05, "FUTURO", tam=70, x=780, y=1260)])


@v.plano(139, "ya no tapa el Sol")
def _(d):
    disco = {"tipo": "forma", "forma": "circulo", "radio": 140, "relleno": "#06070c", "z": 0.35, "keys": K(d, (0, {"x": 160, "y": 820}), (0.7, {"x": 540, "y": 900, "ease": "salida"}))}
    return P(["#020414", "#0d1638"], [BG("bg_eclipse"), *sol(540, 900, 175), disco, fugaz(d * 0.5, 150, 300, 420, 420),
             IMG("personas_mirando", ancho=1080, x=540, y=1660, z=0.8)],
             cam(1.0, 1.08, (540, 1000), (540, 940)), "zoom", hud=[contexto(0.02, d - 0.02, "NO LO TAPA")], sfx=[(0, "rumor", -18, {"dur": d})])


@v.plano(142, "adiós eclipses totales (plano largo)")
def _(d):
    apaga = K(d, (0, {"op": 1}), (0.55, {"op": 1}), (0.85, {"op": 0}))
    return P(["#020414", "#020414"], [BG("bg_eclipse"),
             {"tipo": "rayos", "n": 18, "longitud": 520, "apertura": 7, "intensidad": 0.6, "color": "#eaf2ff", "x": 540, "y": 900, "z": 0.3, "anim": {"girar": 6}, "keys": apaga},
             brillo(540, 900, 380, "#eaf2ff", 0.8, 0.31, keys=apaga),
             {"tipo": "forma", "forma": "circulo", "radio": 178, "relleno": "#06070c", "x": 540, "y": 900, "z": 0.35},
             IMG("personas_mirando", ancho=1080, x=540, y=1660, z=0.8)],
             cam(1.1, 1.18, (540, 950), (540, 920)), hud=[amarillo(0.15, d - 0.05, "ADIÓS, ECLIPSES", y=1300, tam=84, x=470)], sfx=[(0.02, "golpe", -12)])


@v.plano(147, "no te lo pierdas (plano largo)")
def _(d):
    flashes = [(240, 1570, 0.25), (800, 1560, 0.45), (370, 1600, 0.65), (900, 1620, 0.8)]
    return P(["#020414", "#0d1638"], [BG("bg_eclipse"),
             {"tipo": "rayos", "n": 16, "longitud": 460, "apertura": 7, "intensidad": 0.55, "color": "#eaf2ff", "x": 540, "y": 820, "z": 0.3, "anim": {"girar": 5}},
             brillo(540, 820, 340, "#eaf2ff", 0.8, 0.31, pulso=[0.1, 1.2]),
             {"tipo": "forma", "forma": "circulo", "radio": 170, "relleno": "#06070c", "x": 540, "y": 820, "z": 0.35},
             IMG("personas_mirando", ancho=1180, x=540, y=1640, z=0.85),
             *[brillo(x, y, 90, "#ffffff", 1.0, 0.86, keys=[{"t": f * d, "op": 0}, {"t": f * d + 0.05, "op": 1}, {"t": f * d + 0.25, "op": 0}]) for x, y, f in flashes]],
             cam(1.5, 1.0, (540, 1560), (540, 960)), "desenfoque",
             hud=[amarillo(0.2, d - 0.05, "NO TE LO PIERDAS", y=1290, tam=84, x=470)], sfx=[(f * d, "tic", -18) for _, _, f in flashes])


# ================================================================== construir
PALABRA = "palabra" in OPC
v.construir("prueba-luna-densa" + ("-palabra" if PALABRA else "") + ("-micro" if "micro" in OPC else "-corta" if CORTA else ""), version=7, bucle=0.35, subtitulos="palabra" if PALABRA else "karaoke", musica={"generar": "curiosidad", "semilla": 3, "db": -13},
            claves=["uñas", "tres", "coma", "ocho", "centímetros", "espejos", "láser", "mareas", "dinosaurios", "almeja", "dieciocho", "eclipses"])
