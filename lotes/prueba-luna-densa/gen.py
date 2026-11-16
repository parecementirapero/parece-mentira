"""«La Luna se aleja» — versión DENSA v3 (2026-11-16, Nico).

Cambios de la v3:
- Cada plano empieza en una PALABRA del guion (índice en la alineación), no en un segundo fijo:
  con la locución real los cortes se recolocan solos.
- Duración variable a propósito: micro planos de ~0,45 s y planos largos de 2–2,7 s donde hay que entender algo.
- Las animaciones se escalan a la duración real de cada plano (las claves se dan en fracción del plano).
- Control de lectura: todo texto en pantalla tiene que verse al menos 0,25 s + 1 s por cada 17 letras;
  si no, el script avisa.

Uso: python3 gen.py DIR_SALIDA [audio.mp3 alineacion.json]
Sin audio usa la locución/alineación PROVISIONALES de provisional.py (silencio + tiempos estimados a ritmo natural).
"""
import json, os, random, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(AQUI, "..", "2026-11-15-tarde", "generadores", "v4"))
sys.path.insert(0, RAIZ)
from comun_v4 import IMG, BG, polvo, brillo, cam, Montaje  # noqa: E402
from motor.tiempos import palabras_de_alineacion  # noqa: E402

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
if len(sys.argv) > 3:
    AUDIO, ALIN = os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3])
else:
    os.system(f"python3 {os.path.join(AQUI, 'provisional.py')} {OUT} >/dev/null")
    AUDIO, ALIN = os.path.join(OUT, "locucion-provisional.mp3"), os.path.join(OUT, "alineacion-provisional.json")
PAL = palabras_de_alineacion(ALIN)
FIN = PAL[-1]["fin"] + 0.75

M = Montaje(OUT)
nuevos = os.path.join(OUT, "svg-nuevos")
os.system(f"python3 {os.path.join(AQUI, 'ilus_luna.py')} {nuevos} >/dev/null")
for f in os.listdir(nuevos):
    shutil.copy(os.path.join(nuevos, f), os.path.join(OUT, "svg", f))

ESP = ["#02030a", "#0a1030"]
FX, PLANOS, AVISOS = [], [], []


def w(i, adelanto=0.06):
    """Segundo en que empieza la palabra i del guion (el corte va un pelo antes)."""
    return max(0.0, PAL[i]["inicio"] - adelanto) if i else 0.0


def plano(i_palabra, nombre, mas=0.0):
    """Decorador: registra un plano que empieza en la palabra i (+ `mas` segundos).
    La función recibe d (duración) y devuelve el plano."""
    def reg(fn):
        PLANOS.append((w(i_palabra) + mas, nombre, fn))
        return fn
    return reg


# ------------------------------------------------------------------ ayudantes
def fx(t, tipo, db=-14, **k): FX.append({"t": round(t, 3), "tipo": tipo, "db": db, **k})


def K(d, *pares):
    """Claves en FRACCIÓN de la duración del plano: K(d, (0, {...}), (0.6, {...}))."""
    return [{"t": round(f * d, 3), **v} for f, v in pares]


def rotulo(t0, t1, texto="", **k):
    ks = [{"t": t0, "escala": 0.0, "op": 0}, {"t": t0 + 0.05, "op": 1}, {"t": t0 + min(0.25, (t1 - t0) / 3), "escala": 1.0, "ease": "rebote"},
          {"t": t1, "escala": 1.0, "op": 1}, {"t": t1 + 0.15, "op": 0}]
    return {"tipo": "rotulo", "texto": texto, "hud": True, "z": 1, "keys": ks, **k}


def amarillo(t0, t1, texto, y=1360, tam=96):
    return rotulo(t0, t1, texto, tam=tam, color="#ffd23f", capsula=None, rot=-6, x=540, y=y)


def contexto(t0, t1, texto):
    return rotulo(t0, t1, texto, tam=54, color="#ffffff", capsula="#c0392be6", borde="#ffffff30", x=540, y=470)


def contador(t0, t1, desde, hasta, dur, unidad="", **k):
    tam, x, y = k.pop("tam", 120), k.pop("x", 540), k.pop("y", 1450)
    return {**rotulo(t0, t1, "", tam=tam, x=x, y=y, **k), "contar": [desde, hasta, dur], "contar_desde": t0, "unidad": unidad}


def estrellas(n=40, sem=3): return polvo("#ffffff", n, (0, 0, 1080, 1920), sem, "estrellas")
def tierra(x, y, ancho, z=0.4, giro=4, keys=None): return IMG("tierra_hd", ancho=ancho, x=x, y=y, z=z, anim={"girar": giro}, keys=keys or [])
def luna(x, y, ancho, z=0.4, keys=None, **k): return IMG("luna_hd", ancho=ancho, x=x, y=y, z=z, keys=keys or [], **k)


def flecha(pts, t0, t1, color="#ffffffcc", g=8, disc=None, punta=True, z=0.5):
    f = {"tipo": "flecha", "puntos": pts, "grosor": g, "color": color, "punta": punta, "z": z,
         "keys": [{"t": t0, "progreso": 0}, {"t": t1, "progreso": 1, "ease": "salida"}]}
    if disc: f["discontinua"] = disc
    return f


def fugaz(t0, x0, y0, x1, y1, z=0.12):
    return {"tipo": "flecha", "puntos": [[x0, y0], [x1, y1]], "grosor": 3, "color": "#ffffffee", "punta": False, "z": z,
            "keys": [{"t": t0, "progreso": 0, "op": 1}, {"t": t0 + 0.7, "progreso": 1}, {"t": t0 + 1.0, "op": 1}, {"t": t0 + 1.6, "op": 0}]}


INI = 0.0  # inicio absoluto del plano que se está construyendo (lo fija el bucle de abajo)


def recorrido(T0, T1, p0, p1, d):
    """Claves de un objeto que cruza la pantalla entre los segundos ABSOLUTOS T0 y T1 (de p0 a p1).
    Como depende del tiempo del vídeo y no del plano, sigue en el mismo sitio de un plano al siguiente."""
    def en(T):
        u = min(max((T - T0) / (T1 - T0), 0), 1)
        return {"x": p0[0] + (p1[0] - p0[0]) * u, "y": p0[1] + (p1[1] - p0[1]) * u, "op": 1 if T0 <= T <= T1 else 0}
    return [{"t": 0, **en(INI), "ease": "lineal"}, {"t": d, **en(INI + d)}]


# detalles de fondo que duran varios segundos (cruzan despacio y se ven en varios planos seguidos)
def satelite(d, z=0.15):
    return [IMG("satelite", ancho=150, z=z, rot=-15, anim={"girar": 4}, keys=recorrido(0.8, 19.0, (-100, 1680), (1180, 1480), d)),
            IMG("satelite", ancho=120, z=z, rot=20, anim={"girar": -4}, keys=recorrido(33.0, 47.5, (1180, 260), (-100, 420), d))]


def pterosaurios(d):
    return [IMG("pterosaurio", ancho=ancho, z=z, ex=-1, anim={"flotar": [14, 0.9 + i * 0.2]}, keys=recorrido(25.5, 32.0, (1200 + dx, y), (-250 + dx, y + 60), d))
            for i, (dx, y, ancho, z) in enumerate([(0, 430, 300, 0.3), (220, 360, 200, 0.22), (420, 500, 160, 0.18)])]


def reloj(x, y, ancho, h0, m0, h1, m1, t0, t1, z=0.6):
    k = ancho / 600; cx, cy = x, y + 20 * k
    return [IMG("reloj_bolsillo", ancho=ancho, x=x, y=y, z=z),
            IMG("aguja_hora", ancho=200 * k * 1.9, x=cx, y=cy, z=z + 0.01, keys=[{"t": t0, "rot": h0 * 30 + m0 * 0.5, "ease": "lineal"}, {"t": t1, "rot": h1 * 30 + m1 * 0.5}]),
            IMG("aguja_min", ancho=200 * k * 2.2, x=cx, y=cy, z=z + 0.02, keys=[{"t": t0, "rot": m0 * 6, "ease": "lineal"}, {"t": t1, "rot": m1 * 6}])]


def cronometro(rot0, rot1, t0, t1):
    ag = {"tipo": "forma", "forma": "poligono", "puntos": [[-7, 0], [0, -190], [7, 0], [0, 26]], "relleno": "#d62f22", "x": 540, "y": 1060, "z": 0.62,
          "keys": [{"t": t0, "rot": rot0, "ease": "lineal"}, {"t": t1, "rot": rot1}]}
    return [IMG("cronometro", ancho=640, x=540, y=1040, z=0.6), ag,
            {"tipo": "forma", "forma": "circulo", "radio": 16, "relleno": "#1b2233", "x": 540, "y": 1060, "z": 0.63}]


def lineas_vel(x, y, sem=1, color="#ffffff55"):
    r = random.Random(sem)
    return [flecha([[x - r.uniform(80, 220), y + dy], [x - 40, y + dy]], 0.05 + i * 0.05, 0.4 + i * 0.05, color, 4, punta=False, z=0.45)
            for i, dy in enumerate([-40, -10, 20, 50])]


def sol(x, y, r=170, z=0.3):
    return [brillo(x, y, r * 3.2, "#ffcf6a", 0.55, z - 0.01, pulso=[0.06, 2.0]),
            {"tipo": "esfera", "radio": r, "textura": "sol", "color": "#fff3b0", "color2": "#ffb02e", "giro": 6, "x": x, "y": y, "z": z, "luz": [0, 0]}]


def P(fondo, els, camara, entrada="corte", dur_entrada=0.3, vineta=0.55, hud=(), sfx=()):
    return dict(fondo=fondo, els=els, cam=camara, entrada=entrada, dur=dur_entrada, vineta=vineta, hud=list(hud), sfx=list(sfx))


# ================================================================== PLANOS (en orden de guion)
@plano(0, "uñas: gancho")
def _(d):
    return P(["#2a1a14", "#120a08"], [brillo(540, 650, 700, "#ffcf9a", 0.5), estrellas(20, 9),
             luna(820, 420, 150, 0.2, keys=K(d, (0, {"x": 800, "y": 440, "escala": 1.1}), (1, {"x": 860, "y": 380, "escala": 0.85}))),
             IMG("dedo", ancho=560, x=520, z=0.7, keys=K(d, (0, {"y": 1560, "rot": -6}), (0.4, {"y": 1240, "rot": 0, "ease": "salida"})))],
             cam(1.18, 1.3, (540, 1050), (540, 980)), vineta=0.7, sfx=[(0.02, "golpe", -12), (0.45, "brillo", -20)])


@plano(3, "la Luna se aleja")
def _(d):
    return P(ESP, [BG("bg_esp_violeta"), estrellas(), tierra(260, 1250, 620, giro=6),
             luna(0, 0, 220, 0.5, keys=K(d, (0, {"x": 640, "y": 900}), (0.9, {"x": 860, "y": 600, "ease": "salida"}))),
             *lineas_vel(780, 760, 2), flecha([[600, 980], [900, 560]], 0.1, d * 0.7, "#ffd23f", 9, [20, 14]),
             fugaz(0.2, 900, 200, 620, 380), *satelite(d)],
             cam(1.0, 1.08, (500, 1000), (600, 880)), "desenfoque", sfx=[(0.1, "whoosh", -12, {"dur": 0.7})])


@plano(9, "misma velocidad: uña = Luna")
def _(d):
    return P(["#120b1a", "#0a1030"], [
        {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 960, "relleno": ["#3a2418", "#1a0f0a"], "x": 540, "y": 480, "z": 0.05},
        brillo(540, 420, 520, "#ffcf9a", 0.4, 0.06),
        IMG("dedo", ancho=420, x=540, z=0.5, ey=1.0, keys=K(d, (0, {"y": 560, "ey": 1.0, "ease": "lineal"}), (1, {"y": 520, "ey": 1.12}))),
        {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 960, "relleno": ["#060814", "#0a1030"], "x": 540, "y": 1440, "z": 0.05},
        polvo("#ffffff", 30, (0, 970, 1080, 1920), 4, "estrellas"),
        IMG("tierra_hd", ancho=360, x=230, y=1500, z=0.4, anim={"girar": 5}),
        luna(0, 0, 150, 0.45, keys=K(d, (0, {"x": 640, "y": 1380, "ease": "lineal"}), (1, {"x": 900, "y": 1300}))),
        {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 10, "relleno": "#ffd23f", "x": 540, "y": 962, "z": 0.6},
        flecha([[650, 1450], [860, 1360]], 0.2, d * 0.8, "#ffffffaa", 6, [16, 12])],
        cam(1.0, 1.03), hud=[rotulo(0.3, d - 0.1, "=", tam=260, color="#ffd23f", capsula="#0d1330d8", x=540, y=960)])


@plano(17, "3,8 cm")
def _(d):
    return P(["#1b2236", "#0b0f1c"], [brillo(540, 900, 700, "#9fb3ff", 0.3), polvo("#cfe0ff", 25, sem=5),
             IMG("regla", ancho=1000, x=540, y=1050, z=0.5, keys=K(d, (0, {"rot": -4}), (1, {"rot": -1}))),
             {"tipo": "barra", "x": 540 - 480 + 18 + 182, "y": 920, "ancho": 365, "alto": 44, "color": "#ff5a4a", "fondo": "#ffffff15", "z": 0.55,
              "keys": K(d, (0.05, {"progreso": 0}), (0.7, {"progreso": 1, "ease": "salida"}))}],
             cam(1.15, 1.3, (380, 1000), (420, 980)), "zoom",
             hud=[{**contador(0.1, d - 0.1, 0, 3.8, d * 0.6, "CM", tam=130), "decimales": 1}],
             sfx=[(0.15 + i * 0.12, "tic", -24) for i in range(6)])


@plano(21, "al año: hoja de calendario")
def _(d):
    return P(["#3a2a1c", "#1a1410"], [brillo(540, 900, 700, "#ffcf8a", 0.35), IMG("calendario", ancho=640, x=540, y=1000, z=0.59),
             IMG("calendario", ancho=640, x=540, y=1000, z=0.6, keys=K(d, (0.15, {"y": 1000, "rot": 0, "op": 1}), (0.85, {"y": 380, "rot": -35, "op": 0, "ease": "entrada"})))],
             cam(1.0, 1.05, (540, 1000), (540, 1000)), sfx=[(0.15, "whoosh", -16, {"dur": 0.3})])


@plano(23, "¿cómo lo sabemos?")
def _(d):
    return P(ESP, [BG("bg_esp_violeta"), *satelite(d), estrellas(30, 6), luna(540, 960, 560, 0.5, anim={"girar": 3}),
             brillo(540, 960, 520, "#dfe6ff", 0.25, 0.45, pulso=[0.15, 0.6])], cam(1.0, 1.25, (540, 960), (540, 960)), "zoom",
             hud=[amarillo(0.05, d - 0.03, "¿CÓMO?", y=1520, tam=110)])


def cuenta(n):
    def fn(d):
        luces = [{"tipo": "forma", "forma": "circulo", "radio": 18, "relleno": c, "x": 200 + i * 110, "y": 1320 + (i % 2) * 60, "z": 0.5,
                  "anim": {"parpadeo": [0.25, 0.1 + i * 0.03]}} for i, c in enumerate(["#ff5a4a", "#5dff7a", "#ffd23f", "#5dd0ff", "#ff5a4a", "#5dff7a", "#ffd23f"])]
        zoom = {3: (1.0, 1.04), 2: (1.15, 1.2), 1: (1.35, 1.42)}[n]
        return P(["#0b0f1c", "#1b2236"], [brillo(540, 900, 600, "#ff7a4a", 0.25 + 0.1 * (3 - n), pulso=[0.2, 0.15]),
                 {"tipo": "forma", "forma": "redondeado", "ancho": 900, "alto": 360, "relleno": ["#2b3140", "#141822"], "esquinas": 30, "x": 540, "y": 1350, "z": 0.45}, *luces],
                 cam(*zoom, (540, 960), (540, 960)), "desenfoque" if n == 3 else "corte", 0.2,
                 hud=[rotulo(0.0, d, str(n), tam=240, x=540, y=820, color="#ff5a4a")], sfx=[(0.0, "tic", -14)])
    return fn


plano(26, "cuenta atrás 3")(cuenta(3))
plano(26, "cuenta atrás 2", mas=0.32)(cuenta(2))
plano(26, "cuenta atrás 1", mas=0.64)(cuenta(1))


@plano(29, "despegue 1969")
def _(d):
    humo = [brillo(540 + dx, 1640 + dy, 260, "#d9d2c8", 0.6, 0.55, keys=K(d, (0.05, {"op": 0, "escala": 0.5}), (0.6, {"op": 1, "escala": 1.4})))
            for dx, dy in [(-260, 30), (-120, 60), (0, 80), (140, 50), (270, 40)]]
    return P(["#0b1838", "#e88a4a"], [brillo(540, 1500, 900, "#ffb45a", 0.5), polvo("#ffffff", 30, (0, 0, 1080, 900), 7, "estrellas"),
             IMG("cohete", ancho=230, x=540, z=0.6, keys=K(d, (0, {"y": 1150}), (1, {"y": 600, "ease": "entrada"}))),
             brillo(540, 0, 140, "#ffe9a0", 1.0, 0.59, keys=K(d, (0, {"y": 1630}), (1, {"y": 1080, "ease": "entrada"})), pulso=[0.3, 0.12]), *humo],
             {"zoom": [1.0, 1.05], "foco": [[540, 1000], [540, 800]], "pan": [[0, 0], [0, 0]], "temblor": 6},
             hud=[{**contador(0.05, d - 0.05, 1960, 1969, d * 0.5, tam=120, y=560, capsula="#c0392be6"), "miles": False}],
             sfx=[(0, "golpe", -12), (0, "rumor", -9, {"dur": d + 0.3})])


@plano(32, "Apolo 11 aluniza")
def _(d):
    return P(["#02030a", "#02030a"], [BG("bg_superficie_rica"), IMG("tierra_hd", ancho=220, x=840, y=380, z=0.1, anim={"girar": 3}),
             IMG("modulo_lunar", ancho=600, x=520, z=0.6, keys=K(d, (0, {"y": 700}), (0.8, {"y": 1180, "ease": "salida"}))),
             *[brillo(520 + dx, 1400, 200, "#c9c6bb", 0.7, 0.62, keys=K(d, (0.75, {"op": 0, "escala": 0.4}), (1, {"op": 1, "escala": 1.3}))) for dx in (-220, 0, 220)],
             polvo("#dcd8cc", 30, (200, 1250, 880, 1500), 8)],
             cam(1.0, 1.08, (540, 1100), (540, 1150)), "zoom", hud=[contexto(0.05, d - 0.05, "APOLO 11")], sfx=[(d * 0.8, "golpe", -11)])


@plano(36, "micro: primera huella")
def _(d):
    return P(["#8d8a82", "#5d5a54"], [BG("bg_superficie_rica"), polvo("#dcd8cc", 25, (200, 800, 880, 1300), 30),
             {"tipo": "huella", "clase": "bota", "largo": 300, "x": 540, "y": 1150, "z": 0.6, "rot": 12, "keys": K(d, (0, {"marca": 0}), (0.5, {"marca": 1}))}],
             cam(1.6, 1.7, (540, 1150), (540, 1150)), sfx=[(0.02, "golpe", -20)])


@plano(38, "espejos")
def _(d):
    return P(["#02030a", "#02030a"], [BG("bg_superficie_rica"), IMG("astronauta", ancho=360, x=300, y=1240, z=0.6, anim={"balanceo": [3, 0.8]}),
             IMG("retro", ancho=520, x=700, y=1380, z=0.65, keys=K(d, (0, {"y": 1300, "op": 0}), (0.3, {"y": 1380, "op": 1, "ease": "salida"}))),
             brillo(640, 1330, 160, "#ffffff", 1.0, 0.7, keys=K(d, (0.35, {"op": 0, "escala": 0.3}), (0.55, {"op": 1, "escala": 1.2}), (1, {"op": 0.4})))],
             cam(1.15, 1.25, (560, 1280), (600, 1300)), hud=[amarillo(0.02, d - 0.02, "ESPEJOS", y=1720)], sfx=[(d * 0.4, "brillo", -13)])


@plano(39, "micro: el láser se carga")
def _(d):
    return P(["#05070f", "#0b1430"], [BG("bg_esp_petroleo"), IMG("observatorio", ancho=1180, x=540, y=960, z=0.3),
             brillo(520, 1080, 220, "#5dff7a", 0.9, 0.5, keys=K(d, (0, {"op": 0.1, "escala": 0.3}), (0.9, {"op": 1, "escala": 1.2})), pulso=[0.25, 0.1]),
             polvo("#9dffb0", 30, (420, 980, 620, 1180), 31, "chispas")],
             cam(2.2, 2.4, (520, 1100), (520, 1080)), "desenfoque", 0.25, sfx=[(0.05, "rumor", -20, {"dur": d})])


@plano(42, "se dispara un láser")
def _(d):
    return P(["#05070f", "#0b1430"], [BG("bg_esp_petroleo"), *satelite(d), luna(780, 260, 200), fugaz(d * 0.5, 160, 300, 420, 160),
             IMG("observatorio", ancho=1180, x=540, y=960, z=0.3),
             flecha([[520, 1080], [770, 290]], d * 0.3, d * 0.6, "#5dff7a", 10, punta=False),
             brillo(520, 1080, 160, "#5dff7a", 0.9, 0.5, keys=K(d, (0.25, {"op": 0}), (0.35, {"op": 1})), pulso=[0.3, 0.2])],
             cam(1.1, 1.0, (540, 1050), (560, 900)), hud=[amarillo(0.2, d - 0.05, "LÁSER", y=1700)], sfx=[(d * 0.3, "zap", -11)])


@plano(46, "la luz rebota")
def _(d):
    return P(ESP, [BG("bg_esp_petroleo"), *satelite(d), estrellas(25, 10), tierra(240, 1420, 520), luna(820, 560, 260),
             flecha([[330, 1300], [800, 590]], 0.0, d * 0.4, "#5dff7a", 9),
             flecha([[790, 640], [350, 1330]], d * 0.5, d * 0.95, "#ff5a8a", 9, [22, 14]),
             brillo(800, 590, 200, "#ffffff", 1.0, 0.55, keys=K(d, (0.35, {"op": 0, "escala": 0.3}), (0.48, {"op": 1, "escala": 1.4}), (0.9, {"op": 0})))],
             cam(1.05, 1.0, (560, 960), (540, 960)), sfx=[(d * 0.4, "ding", -16, {"f": 1320})])


@plano(50, "vuelve en 2,5 s")
def _(d):
    return P(["#1b2236", "#0b0f1c"], [brillo(540, 1000, 700, "#9fb3ff", 0.3), polvo("#cfe0ff", 20, sem=11), *cronometro(0, 900, 0.1, d * 0.75)],
             cam(1.0, 1.12, (540, 1050), (540, 1050)), "zoom", vineta=0.65,
             hud=[{**contador(0.1, d - 0.05, 0, 2.5, d * 0.6, "SEGUNDOS", y=1560), "decimales": 1},
                  contexto(0.1, d - 0.05, "384.400 KM HASTA LA LUNA")],
             sfx=[(0.15 + i * 0.16, "tic", -22) for i in range(int(d / 0.16) - 1)])


@plano(56, "¿y por qué se va?")
def _(d):
    return P(ESP, [BG("bg_esp_violeta"), *satelite(d), estrellas(30, 13), tierra(400, 1200, 600, giro=8),
             luna(0, 0, 200, 0.55, keys=K(d, (0, {"x": 700, "y": 760}), (1, {"x": 1000, "y": 420, "ease": "entrada"}))), *lineas_vel(900, 520, 4)],
             cam(1.0, 1.06, (540, 960), (600, 900)), "desenfoque", hud=[amarillo(0.1, d - 0.05, "¿POR QUÉ?", y=1650)])


@plano(61, "mareas")
def _(d):
    return P(["#0e3a5c", "#05192b"], [brillo(540, 600, 700, "#9fd8ff", 0.35),
             {"tipo": "agua", "nivel": 1000, "lado": "abajo", "amplitud": 40, "colores": ["#2a8bd0", "#0b4a7a"], "z": 0.4,
              "keys": K(d, (0, {"nivel": 1150}), (0.9, {"nivel": 820, "ease": "suave"}))},
             luna(860, 360, 220, 0.2), polvo("#e6f6ff", 30, (0, 900, 1080, 1700), 14, "burbujas"),
             IMG("yate", ancho=420, x=330, z=0.45, anim={"flotar": [10, 1.2], "balanceo": [4, 1.4]}, keys=K(d, (0, {"y": 1110}), (0.9, {"y": 790, "ease": "suave"})))],
             cam(1.0, 1.08, (540, 1000), (540, 1050)), "zoom", hud=[amarillo(0.1, d - 0.05, "MAREAS", y=1650)], sfx=[(0.02, "ola", -11)])


@plano(64, "el agua frena")
def _(d):
    return P(ESP, [BG("bg_esp_violeta"), *satelite(d), estrellas(25, 15), IMG("marea", ancho=900, x=540, y=1050, z=0.35, rot=-10, anim={"pulso": [0.02, 1.0]}),
             tierra(540, 1050, 560, giro=-4), luna(980, 880, 150),
             flecha([[300, 780], [540, 680], [780, 780]], 0.1, d * 0.7, "#ffd23f", 14, z=0.6),
             {"tipo": "forma", "forma": "poligono", "puntos": [[-60, -20], [60, -20], [60, 20], [-60, 20]], "relleno": "#d62f22", "x": 540, "y": 650, "z": 0.62,
              "keys": K(d, (0.6, {"op": 0, "escala": 0.5}), (0.8, {"op": 1, "escala": 1.0, "ease": "rebote"}))}],
             cam(1.0, 1.1, (540, 960), (540, 900)), "desenfoque", hud=[contexto(0.05, d - 0.05, "FRENA")], sfx=[(d * 0.6, "pop", -14)])


@plano(67, "como una patinadora")
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


@plano(72, "empuja a la Luna hacia fuera (plano largo)")
def _(d):
    orb1 = {"tipo": "forma", "forma": "elipse", "ancho": 600, "alto": 600, "relleno": "#ffffff", "op_relleno": 0, "grosor": 3, "borde": "#ffffff55", "x": 540, "y": 1000, "z": 0.3}
    orb2 = {"tipo": "forma", "forma": "elipse", "ancho": 880, "alto": 880, "relleno": "#ffffff", "op_relleno": 0, "grosor": 5, "borde": "#ffd23f",
            "x": 540, "y": 1000, "z": 0.3, "keys": K(d, (0.15, {"op": 0, "escala": 0.68}), (0.8, {"op": 1, "escala": 1.0}))}
    return P(ESP, [BG("bg_esp_violeta"), *satelite(d), estrellas(30, 16), orb1, orb2, tierra(540, 1000, 280, giro=10),
             luna(0, 0, 120, 0.5, keys=K(d, (0, {"x": 840, "y": 1000}), (0.35, {"x": 860, "y": 740}), (0.7, {"x": 820, "y": 640}), (1, {"x": 940, "y": 740}))),
             *[flecha([[540 + dx * 160, 1000 + dy * 160], [540 + dx * 400, 1000 + dy * 400]], d * (0.1 + i * 0.05), d * (0.35 + i * 0.05), "#ffd23faa", 6, z=0.35)
               for i, (dx, dy) in enumerate([(0.7, -0.7), (-0.7, -0.7), (0.7, 0.7), (-0.7, 0.7)])], fugaz(d * 0.7, 120, 300, 380, 420)],
             cam(1.0, 0.94), "zoom", hud=[amarillo(d * 0.35, d - 0.05, "HACIA FUERA", y=1680)], sfx=[(0.2, "whoosh", -13, {"dur": 1.2})])


@plano(81, "resultado")
def _(d):
    return P(["#1a1410", "#3a2a1c"], [brillo(540, 1000, 650, "#ffcf8a", 0.3), *reloj(540, 1000, 700, 3, 0, 9, 0, 0.0, d)],
             cam(1.25, 1.35, (540, 960), (540, 960)), "zoom", 0.25, vineta=0.7, sfx=[(i * 0.12, "tic", -20) for i in range(int(d / 0.12))])


@plano(82, "los días se alargan")
def _(d):
    soles = [{**s, "keys": K(d, (0, {"x": 120, "y": 760, "ease": "lineal"}), (1, {"x": 960, "y": 500}))} for s in sol(0, 0, 90, 0.07)]
    return P(["#4f9be0", "#fbe8c2"], [BG("campo_dia"), *soles, *reloj(540, 1180, 520, 6, 0, 18, 0, 0.1, d), polvo("#ffffff", 20, sem=17)],
             cam(1.0, 1.06, (540, 1100), (540, 1100)), vineta=0.4,
             hud=[{**contador(0.05, d - 0.03, 0, 1.8, d * 0.35, "MS POR SIGLO", tam=96, y=1620, contar_prefijo="+"), "decimales": 1}])


@plano(86, "dinosaurios")
def _(d):
    return P(["#2b1b3a", "#f6d08a"], [BG("bg_jungla"),
             IMG("dino_braquio", ancho=560, z=0.22, anim={"balanceo": [1, 1.4]}, keys=recorrido(25.5, 32.0, (760, 1170), (520, 1170), d)),
             IMG("dino_trice", ancho=500, z=0.5, anim={"balanceo": [1.2, 0.9]}, keys=recorrido(25.5, 32.0, (1100, 1430), (600, 1430), d), ex=-1),
             *pterosaurios(d), polvo("#ffd9a0", 25, sem=18),
             *[IMG("dino_raptor", ancho=330, z=0.8, anim={"balanceo": [3, 0.35]}, keys=K(d, (0, {"x": -200 - i * 160, "y": 1640 + i * 40, "ease": "lineal"}), (1, {"x": 520 - i * 160, "y": 1640 + i * 40})))
               for i in range(2)],
             {**brillo(300, 640, 200, "#6b5a5a", 0.5, 0.06), "anim": {"deriva": [10, -60]}}],
             cam(1.0, 1.06, (540, 1200), (500, 1200)), "zoom", vineta=0.5, sfx=[(0.1, "golpe", -15), (0.6, "golpe", -17)])


@plano(89, "23,5 horas (plano largo)")
def _(d):
    return P(["#2b1b3a", "#f6d08a"], [BG("bg_jungla"),
             IMG("dino_braquio", ancho=560, z=0.22, anim={"balanceo": [1, 1.4]}, keys=recorrido(25.5, 32.0, (760, 1170), (520, 1170), d)),
             IMG("dino_trex", ancho=620, z=0.35, anim={"balanceo": [1.5, 1.0]}, keys=K(d, (0, {"x": 1300, "y": 1360, "ease": "lineal"}), (1, {"x": 780, "y": 1360})), ex=-1),
             *pterosaurios(d),
             {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 1920, "relleno": "#000000", "x": 540, "y": 960, "z": 0.4, "op": 0.4},
             *reloj(540, 1000, 600, 0, 0, 23, 30, 0.1, d * 0.8),
             IMG("dino_estego", ancho=430, z=0.8, keys=K(d, (0, {"x": -260, "y": 1640, "ease": "lineal"}), (1, {"x": 260, "y": 1640})))],
             cam(1.0, 1.08, (540, 1000), (540, 1000)),
             hud=[{**contador(0.15, d - 0.05, 24, 23.5, d * 0.5, "HORAS", y=1560), "decimales": 1}, contexto(0.1, d - 0.05, "HACE 70 MILLONES DE AÑOS")],
             sfx=[(0.15 + i * 0.2, "tic", -22) for i in range(int(d * 0.8 / 0.2))] + [(0.3, "golpe", -20), (1.2, "golpe", -20)])


@plano(96, "372 días (plano largo)")
def _(d):
    n = 7
    hojas = [IMG("calendario", ancho=520, x=540, y=1000, z=0.6 - i * 0.001,
                 keys=[{"t": 0.15 + i * d * 0.09, "y": 1000, "rot": 0, "op": 1}, {"t": 0.45 + i * d * 0.09, "y": 300, "rot": -25 + i * 9, "op": 0, "ease": "entrada"}]) for i in range(n)]
    return P(["#3a2a1c", "#1a1410"], [brillo(540, 900, 700, "#ffcf8a", 0.35), IMG("calendario", ancho=520, x=540, y=1000, z=0.59), *reversed(hojas)],
             cam(1.0, 1.06, (540, 1000), (540, 980)), "desenfoque", vineta=0.65,
             hud=[contador(0.1, d - 0.05, 365, 372, d * 0.65, "DÍAS", tam=130, y=1580)],
             sfx=[(0.2 + i * d * 0.09, "whoosh", -24, {"dur": 0.18}) for i in range(n)])


@plano(105, "rayas: lupa")
def _(d):
    return P(["#2a241c", "#120f0a"], [brillo(540, 900, 700, "#ffe2b0", 0.35), polvo("#ffe9c0", 20, sem=21),
             IMG("almeja_fosil", ancho=880, x=540, y=1050, z=0.6),
             IMG("lupa", ancho=520, x=0, y=900, z=0.7, keys=K(d, (0.2, {"x": 900}), (0.6, {"x": 540, "ease": "salida"})))],
             cam(1.0, 1.08, (540, 1050), (540, 1000)), "zoom", vineta=0.65, hud=[contexto(0.05, d - 0.05, "1 RAYA = 1 DÍA")], sfx=[(d * 0.6, "brillo", -16)])


@plano(110, "almeja fósil de cerca")
def _(d):
    return P(["#2a241c", "#120f0a"], [IMG("almeja_fosil", ancho=880, x=540, y=1050, z=0.6), polvo("#ffe9c0", 15, sem=22)],
             cam(1.6, 1.8, (540, 820), (520, 800)))


@plano(113, "micro: un láser corta la concha")
def _(d):
    return P(["#2a241c", "#120f0a"], [IMG("almeja_fosil", ancho=880, x=540, y=1050, z=0.6),
             {"tipo": "forma", "forma": "rect", "ancho": 900, "alto": 6, "relleno": "#5dff7a", "x": 540, "z": 0.65, "keys": K(d, (0, {"y": 700, "ease": "lineal"}), (1, {"y": 1150}))},
             brillo(540, 0, 300, "#5dff7a", 0.6, 0.64, keys=K(d, (0, {"y": 700, "ease": "lineal"}), (1, {"y": 1150}))),
             polvo("#b8ffc8", 25, (300, 700, 780, 1150), 33, "chispas")],
             cam(1.3, 1.35, (540, 950), (540, 980)), sfx=[(0.02, "zap", -18, {"f0": 900, "f1": 600, "dur": d})])


@plano(114, "micro: tiempo hacia atrás")
def _(d):
    return P(["#1b2236", "#0b0f1c"], [brillo(540, 1000, 700, "#ff9a7a", 0.3), *cronometro(0, -1080, 0, d)],
             cam(1.1, 1.2, (540, 1050), (540, 1050)), "desenfoque", 0.2, vineta=0.7, sfx=[(0.0, "whoosh", -14, {"dur": d})])


@plano(116, "1.400 millones de años: la Luna cerca")
def _(d):
    return P(ESP, [BG("bg_esp_ambar"), *satelite(d), estrellas(40, 22), tierra(380, 1250, 560, giro=40),
             luna(0, 0, 330, 0.5, keys=K(d, (0, {"x": 880, "y": 600, "escala": 0.48}), (0.8, {"x": 720, "y": 820, "escala": 1.0, "ease": "salida"}))),
             flecha([[900, 560], [740, 790]], 0.1, d * 0.7, "#ff5a4a", 8, [18, 12])],
             cam(1.0, 1.05),
             hud=[{**contador(0.05, d - 0.05, 0, 1400, d * 0.55, "MILLONES DE AÑOS", tam=100, y=560), "capsula": "#c0392be6"}])


@plano(120, "18 horas (plano largo)")
def _(d):
    return P(ESP, [BG("bg_esp_ambar"), *satelite(d), estrellas(30, 23), tierra(540, 1150, 620, giro=70), luna(900, 520, 300),
             *reloj(260, 520, 300, 0, 0, 18, 0, 0.1, d * 0.7, z=0.65), fugaz(d * 0.6, 700, 200, 980, 320)],
             cam(1.0, 1.06, (540, 1000), (540, 1000)), hud=[rotulo(d * 0.4, d - 0.05, "18", unidad="HORAS", tam=150, x=540, y=1620)],
             sfx=[(0.1 + i * 0.16, "tic", -22) for i in range(int(d * 0.7 / 0.16))])


@plano(126, "micro: avance rápido")
def _(d):
    return P(["#1b2236", "#0b0f1c"], [brillo(540, 1000, 700, "#7ad0ff", 0.3), *cronometro(0, 1440, 0, d)],
             cam(1.1, 1.2, (540, 1050), (540, 1050)), "desenfoque", 0.2, vineta=0.7, sfx=[(0.0, "whoosh", -14, {"dur": d})])


@plano(129, "600 millones de años: la Luna lejos")
def _(d):
    return P(ESP, [BG("bg_esp_petroleo"), *satelite(d), estrellas(40, 24), tierra(300, 1350, 480, giro=3),
             luna(0, 0, 260, 0.5, keys=K(d, (0, {"x": 640, "y": 900, "escala": 1.0}), (0.9, {"x": 900, "y": 420, "escala": 0.35, "ease": "salida"}))),
             flecha([[620, 920], [880, 450]], 0.1, d * 0.7, "#5dd0ff", 8, [18, 12])],
             cam(1.0, 1.04), hud=[{**contador(0.05, d - 0.05, 0, 600, d * 0.5, "MILLONES DE AÑOS", tam=110, y=560), "contar_prefijo": "+"}])


@plano(134, "hoy / futuro")
def _(d):
    return P(ESP, [BG("bg_esp_petroleo"), *satelite(d), estrellas(30, 34), luna(300, 980, 340, 0.4), fugaz(d * 0.3, 820, 300, 1040, 180),
             luna(780, 980, 340, 0.4, keys=K(d, (0, {"escala": 1.0}), (0.6, {"escala": 0.55, "ease": "salida"})))],
             cam(1.0, 1.04), hud=[rotulo(0.05, d - 0.05, "HOY", tam=70, x=300, y=1260), rotulo(0.1, d - 0.05, "FUTURO", tam=70, x=780, y=1260)])


@plano(139, "ya no tapa el Sol")
def _(d):
    disco = {"tipo": "forma", "forma": "circulo", "radio": 140, "relleno": "#06070c", "z": 0.35, "keys": K(d, (0, {"x": 160, "y": 820}), (0.7, {"x": 540, "y": 900, "ease": "salida"}))}
    return P(["#020414", "#0d1638"], [BG("bg_eclipse"), *sol(540, 900, 175), disco, fugaz(d * 0.5, 150, 300, 420, 420),
             IMG("personas_mirando", ancho=1080, x=540, y=1660, z=0.8)],
             cam(1.0, 1.08, (540, 1000), (540, 940)), "zoom", hud=[contexto(0.02, d - 0.02, "NO LO TAPA")], sfx=[(0, "rumor", -18, {"dur": d})])


@plano(142, "adiós eclipses totales (plano largo)")
def _(d):
    apaga = K(d, (0, {"op": 1}), (0.55, {"op": 1}), (0.85, {"op": 0}))
    return P(["#020414", "#020414"], [BG("bg_eclipse"),
             {"tipo": "rayos", "n": 18, "longitud": 520, "apertura": 7, "intensidad": 0.6, "color": "#eaf2ff", "x": 540, "y": 900, "z": 0.3, "anim": {"girar": 6}, "keys": apaga},
             brillo(540, 900, 380, "#eaf2ff", 0.8, 0.31, keys=apaga),
             {"tipo": "forma", "forma": "circulo", "radio": 178, "relleno": "#06070c", "x": 540, "y": 900, "z": 0.35},
             IMG("personas_mirando", ancho=1080, x=540, y=1660, z=0.8)],
             cam(1.1, 1.18, (540, 950), (540, 920)), hud=[amarillo(0.15, d - 0.05, "ADIÓS, ECLIPSES TOTALES", y=1380, tam=66)], sfx=[(0.02, "golpe", -12)])


@plano(147, "no te lo pierdas (plano largo)")
def _(d):
    flashes = [(240, 1570, 0.25), (800, 1560, 0.45), (370, 1600, 0.65), (900, 1620, 0.8)]
    return P(["#020414", "#0d1638"], [BG("bg_eclipse"),
             {"tipo": "rayos", "n": 16, "longitud": 460, "apertura": 7, "intensidad": 0.55, "color": "#eaf2ff", "x": 540, "y": 820, "z": 0.3, "anim": {"girar": 5}},
             brillo(540, 820, 340, "#eaf2ff", 0.8, 0.31, pulso=[0.1, 1.2]),
             {"tipo": "forma", "forma": "circulo", "radio": 170, "relleno": "#06070c", "x": 540, "y": 820, "z": 0.35},
             IMG("personas_mirando", ancho=1180, x=540, y=1640, z=0.85),
             *[brillo(x, y, 90, "#ffffff", 1.0, 0.86, keys=[{"t": f * d, "op": 0}, {"t": f * d + 0.05, "op": 1}, {"t": f * d + 0.25, "op": 0}]) for x, y, f in flashes]],
             cam(1.0, 1.12, (540, 1100), (540, 900)), "desenfoque",
             hud=[amarillo(0.2, d - 0.05, "NO TE LO PIERDAS", y=1380)], sfx=[(f * d, "tic", -18) for _, _, f in flashes])


# ================================================================== construir
PLANOS.sort(key=lambda p: p[0])
_g = globals()
LEER = lambda txt: 0.25 + len(txt) / 17  # segundos mínimos para leer un texto (una cifra suelta: ~0,3 s)
informe = []
for k, (ini, nombre, fn) in enumerate(PLANOS):
    fin = PLANOS[k + 1][0] if k + 1 < len(PLANOS) else FIN
    d = round(fin - ini, 3)
    _g["INI"] = ini
    p = fn(d)
    M.plano(ini, fin, p["fondo"], p["els"], p["cam"], entrada=p["entrada"], vineta=p["vineta"], dur=p["dur"] if p["entrada"] != "corte" else None)
    if p["entrada"] in ("desenfoque", "zoom", "barrido"):
        fx(max(0, ini - 0.12), "whoosh", -15, dur=0.4)
    for h in p["hud"]:
        txt = ((h.get("texto") or "") + " " + (h.get("unidad") or "")).strip()
        if h.get("contar"):
            txt = (f"{h['contar'][1]} " + txt).strip()
        visible = h["keys"][-2]["t"] - h["keys"][0]["t"]
        if visible + 1e-3 < LEER(txt):
            AVISOS.append(f"  ⚠ «{txt}» en «{nombre}»: {visible:.2f} s en pantalla, harían falta {LEER(txt):.2f} s")
        fx(ini + h["keys"][0]["t"], "pop", -16)
    M.add(*p["hud"])
    for s in p["sfx"]:
        t, tipo, db = s[:3]
        fx(ini + t, tipo, db, **(s[3] if len(s) > 3 else {}))
    informe.append((d, nombre))

claves = ["uñas", "tres", "coma", "ocho", "centímetros", "espejos", "láser", "mareas", "dinosaurios", "almeja", "dieciocho", "eclipses"]
M.guardar("02", "luna-densa", FIN, claves, {"generar": "curiosidad", "semilla": 3})
ruta = os.path.join(OUT, "episodio.json")
ep = json.load(open(ruta))
ep["id"], ep["audio"], ep["subtitulos"]["alineacion"] = "prueba-luna-densa", AUDIO, ALIN
ep["sfx"] = sorted(FX, key=lambda e: e["t"])
json.dump(ep, open(ruta, "w"), ensure_ascii=False, indent=1)

ds = [d for d, _ in informe]
print(f"{len(ds)} planos · {len(FX)} efectos · {FIN:.1f} s · plano más corto {min(ds):.2f} s · más largo {max(ds):.2f} s")
print("  < 0,7 s:", sum(d < 0.7 for d in ds), "· 0,7–1,5 s:", sum(0.7 <= d < 1.5 for d in ds), "· ≥ 1,5 s:", sum(d >= 1.5 for d in ds))
for d, n in informe:
    print(f"  {d:5.2f} s {'█' * int(d * 10)} {n}")
print("\n".join(AVISOS) if AVISOS else "  ✓ todos los textos se pueden leer")
