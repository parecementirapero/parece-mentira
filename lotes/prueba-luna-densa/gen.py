"""«La Luna se aleja» — versión DENSA desde cero (prueba 2026-11-16, Nico).
169 palabras en ~46,6 s, 27 planos (uno cada ~1,7 s), más capas por plano y efectos de sonido.
Uso: python3 gen.py DIR_SALIDA [audio.mp3 alineacion.json]
Sin audio usa la locución y alineación PROVISIONALES de provisional.py (silencio + tiempos estimados)."""
import os, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "2026-11-15-tarde", "generadores", "v4"))
from comun_v4 import IMG, BG, ROT, AMARILLO, CONTEXTO, polvo, brillo, cam, Montaje  # noqa: E402

OUT = sys.argv[1]
M = Montaje(OUT)
nuevos = os.path.join(OUT, "svg-nuevos")
os.system(f"python3 {os.path.join(AQUI, 'ilus_luna.py')} {nuevos} >/dev/null")
for f in os.listdir(nuevos):
    shutil.copy(os.path.join(nuevos, f), os.path.join(OUT, "svg", f))

ESP = ["#02030a", "#0a1030"]
FX = []


def fx(t, tipo, db=-14, **k): FX.append({"t": round(t, 3), "tipo": tipo, "db": db, **k})


def P(ini, fin, fondo, els, camara, entrada="corte", dur=None, vineta=0.55):
    """Plano + whoosh automático en las transiciones con movimiento."""
    if entrada in ("desenfoque", "zoom", "barrido"):
        fx(max(0, ini - 0.15), "whoosh", -15, dur=0.4)
    return M.plano(ini, fin, fondo, els, camara, entrada=entrada, vineta=vineta, dur=dur)


def add(ini, *els):
    """Añade elementos HUD y un «pop» cuando aparece cada rótulo."""
    for e in els:
        if e.get("tipo") == "rotulo":
            t0 = (e.get("contar_desde") if e.get("contar") else e["keys"][0]["t"])
            fx(ini + t0, "pop", -16)
    M.add(*els)


def estrellas(n=40, sem=3): return polvo("#ffffff", n, (0, 0, 1080, 1920), sem, "estrellas")
def tierra(x, y, ancho, z=0.4, giro=4, keys=None): return IMG("tierra_hd", ancho=ancho, x=x, y=y, z=z, anim={"girar": giro}, keys=keys or [])
def luna(x, y, ancho, z=0.4, keys=None, **k): return IMG("luna_hd", ancho=ancho, x=x, y=y, z=z, keys=keys or [], **k)
def flecha(pts, t0, t1, color="#ffffffcc", g=8, disc=None, punta=True, z=0.5):
    f = {"tipo": "flecha", "puntos": pts, "grosor": g, "color": color, "punta": punta, "z": z,
         "keys": [{"t": t0, "progreso": 0}, {"t": t1, "progreso": 1, "ease": "salida"}]}
    if disc: f["discontinua"] = disc
    return f
def reloj(x, y, ancho, h0, m0, h1, m1, t0, t1, z=0.6):
    k = ancho / 600; cx, cy = x, y + 20 * k
    return [IMG("reloj_bolsillo", ancho=ancho, x=x, y=y, z=z),
            IMG("aguja_hora", ancho=200 * k * 1.9, x=cx, y=cy, z=z + 0.01, keys=[{"t": t0, "rot": h0 * 30 + m0 * 0.5, "ease": "lineal"}, {"t": t1, "rot": h1 * 30 + m1 * 0.5}]),
            IMG("aguja_min", ancho=200 * k * 2.2, x=cx, y=cy, z=z + 0.02, keys=[{"t": t0, "rot": m0 * 6, "ease": "lineal"}, {"t": t1, "rot": m1 * 6}])]
def lineas_vel(x, y, sem=1, color="#ffffff55"):
    import random; r = random.Random(sem)
    return [flecha([[x - r.uniform(80, 220), y + dy], [x - 40, y + dy]], 0.05 + i * 0.05, 0.45 + i * 0.05, color, 4, punta=False, z=0.45)
            for i, dy in enumerate([-40, -10, 20, 50])]
def sol(x, y, r=170, z=0.3, op=1.0):
    return [brillo(x, y, r * 3.2, "#ffcf6a", 0.55 * op, z - 0.01, pulso=[0.06, 2.0]),
            {"tipo": "esfera", "radio": r, "textura": "sol", "color": "#fff3b0", "color2": "#ffb02e", "giro": 6, "x": x, "y": y, "z": z, "luz": [0, 0]}]


# 1 · «Mira tus uñas» — gancho: dedo enorme y la Luna pequeña detrás, alejándose
P(0, 1.22, ["#2a1a14", "#120a08"], [brillo(540, 650, 700, "#ffcf9a", 0.5), estrellas(20, 9),
  luna(820, 420, 150, 0.2, keys=[{"t": 0, "x": 800, "y": 440, "escala": 1.1}, {"t": 1.2, "x": 860, "y": 380, "escala": 0.85}]),
  IMG("dedo", ancho=560, x=520, z=0.7, keys=[{"t": 0, "y": 1560, "rot": -6}, {"t": 0.5, "y": 1240, "rot": 0, "ease": "salida"}])],
  cam(1.18, 1.3, (540, 1050), (540, 980)), vineta=0.7)
fx(0.02, "golpe", -12); fx(0.45, "brillo", -20)

# 2 · «La Luna se aleja de nosotros»
P(1.22, 2.48, ESP, [BG("bg_espacio"), estrellas(), tierra(260, 1250, 620, giro=6),
  luna(0, 0, 220, 0.5, keys=[{"t": 0, "x": 640, "y": 900}, {"t": 1.2, "x": 860, "y": 600, "ease": "salida"}]),
  *lineas_vel(780, 760, 2), flecha([[600, 980], [900, 560]], 0.1, 0.9, "#ffd23f", 9, [20, 14])],
  cam(1.0, 1.08, (500, 1000), (600, 880)), entrada="desenfoque", dur=0.3)
fx(1.35, "whoosh", -12, dur=0.7)

# 3 · «a la misma velocidad a la que crecen» — pantalla partida uña / Luna, con «=»
P(2.48, 4.36, ["#120b1a", "#0a1030"], [
  {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 960, "relleno": ["#3a2418", "#1a0f0a"], "x": 540, "y": 480, "z": 0.05},
  brillo(540, 420, 520, "#ffcf9a", 0.4, 0.06),
  IMG("dedo", ancho=420, x=540, z=0.5, ey=1.0, keys=[{"t": 0, "y": 560, "ey": 1.0}, {"t": 1.8, "y": 520, "ey": 1.12, "ease": "lineal"}]),
  {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 960, "relleno": ["#060814", "#0a1030"], "x": 540, "y": 1440, "z": 0.05},
  polvo("#ffffff", 30, (0, 970, 1080, 1920), 4, "estrellas"),
  IMG("tierra_hd", ancho=360, x=230, y=1500, z=0.4, anim={"girar": 5}),
  luna(0, 0, 150, 0.45, keys=[{"t": 0, "x": 640, "y": 1380}, {"t": 1.8, "x": 900, "y": 1300, "ease": "lineal"}]),
  {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 10, "relleno": "#ffd23f", "x": 540, "y": 962, "z": 0.6},
  flecha([[650, 1450], [860, 1360]], 0.2, 1.6, "#ffffffaa", 6, [16, 12])],
  cam(1.0, 1.03), entrada="corte")
add(2.48, ROT(0.35, 1.8, "=", tam=200, color="#ffd23f", capsula=None, x=540, y=960))

# 4 · «tres coma ocho centímetros cada año» — regla, barra que se llena y contador
P(4.36, 6.32, ["#1b2236", "#0b0f1c"], [brillo(540, 900, 700, "#9fb3ff", 0.3), polvo("#cfe0ff", 25, sem=5),
  IMG("regla", ancho=1000, x=540, y=1050, z=0.5, keys=[{"t": 0, "rot": -4}, {"t": 1.9, "rot": -1}]),
  {"tipo": "barra", "x": 540 - 480 + 18 + 182, "y": 920, "ancho": 365, "alto": 44, "color": "#ff5a4a", "fondo": "#ffffff15", "z": 0.55,
   "keys": [{"t": 0.15, "progreso": 0}, {"t": 1.5, "progreso": 1, "ease": "salida"}]},
  IMG("calendario", ancho=260, x=880, y=560, z=0.6, rot=8, keys=[{"t": 0, "op": 0, "escala": 0.6}, {"t": 0.4, "op": 1, "escala": 1.0, "ease": "rebote"}])],
  cam(1.15, 1.3, (380, 1000), (420, 980)), entrada="zoom", dur=0.3, vineta=0.6)
add(4.36, {**ROT(0.2, 1.9, "", tam=130, x=540, y=1450), "contar": [0, 3.8, 1.3], "contar_desde": 0.2, "unidad": "CM/AÑO", "decimales": 1})
for i in range(9): fx(4.6 + i * 0.14, "tic", -24)

# 5 · «¿Cómo lo sabemos?» — empujón a la Luna con interrogación
P(6.32, 7.43, ESP, [BG("bg_espacio"), estrellas(30, 6), luna(540, 960, 560, 0.5, anim={"girar": 3}),
  brillo(540, 960, 520, "#dfe6ff", 0.25, 0.45, pulso=[0.15, 0.6])], cam(1.0, 1.25, (540, 960), (540, 960)), entrada="zoom", dur=0.3)
add(6.32, AMARILLO(0.15, 1.1, "¿CÓMO LO SABEMOS?", y=1520))

# 6 · «En 1969» — despega el cohete, humo y contador de año
humo_base = [brillo(540 + dx, 1640 + dy, 260, "#d9d2c8", 0.6, 0.55, keys=[{"t": 0.1, "op": 0, "escala": 0.5}, {"t": 0.8, "op": 1, "escala": 1.4}])
             for dx, dy in [(-260, 30), (-120, 60), (0, 80), (140, 50), (270, 40)]]
P(7.43, 9.14, ["#0b1838", "#e88a4a"], [brillo(540, 1500, 900, "#ffb45a", 0.5),
  polvo("#ffffff", 30, (0, 0, 1080, 900), 7, "estrellas"),
  IMG("cohete", ancho=230, x=540, z=0.6, keys=[{"t": 0, "y": 1160}, {"t": 0.4, "y": 1150}, {"t": 1.7, "y": 520, "ease": "entrada"}]),
  brillo(540, 0, 140, "#ffe9a0", 1.0, 0.59, keys=[{"t": 0, "y": 1640}, {"t": 0.4, "y": 1630}, {"t": 1.7, "y": 1010, "ease": "entrada"}], pulso=[0.3, 0.12]),
  *humo_base], {"zoom": [1.0, 1.05], "foco": [[540, 1000], [540, 800]], "pan": [[0, 0], [0, 0]], "temblor": 6}, entrada="desenfoque", dur=0.3)
add(7.43, {**ROT(0.1, 1.6, "", tam=120, x=540, y=560), "contar": [1960, 1969, 0.9], "contar_desde": 0.1, "miles": False, "capsula": "#c0392be6"})
fx(7.45, "rumor", -9, dur=1.8)

# 7 · «el Apolo once dejó allí arriba» — alunizaje con polvo
P(9.14, 10.50, ["#02030a", "#02030a"], [BG("bg_superficie"), IMG("tierra_hd", ancho=220, x=840, y=380, z=0.1, anim={"girar": 3}),
  IMG("modulo_lunar", ancho=600, x=520, z=0.6, keys=[{"t": 0, "y": 700}, {"t": 0.9, "y": 1180, "ease": "salida"}]),
  *[brillo(520 + dx, 1400, 200, "#c9c6bb", 0.7, 0.62, keys=[{"t": 0.8, "op": 0, "escala": 0.4}, {"t": 1.2, "op": 1, "escala": 1.3}, {"t": 1.4, "op": 0.6}])
    for dx in (-220, 0, 220)],
  polvo("#dcd8cc", 30, (200, 1250, 880, 1500), 8)],
  cam(1.0, 1.08, (540, 1100), (540, 1150)), entrada="zoom", dur=0.3)
add(9.14, CONTEXTO(0.2, 1.3, "APOLO 11"))
fx(9.95, "golpe", -11)

# 8 · «unos espejos» — astronauta deja el retrorreflector y destella
P(10.50, 11.45, ["#02030a", "#02030a"], [BG("bg_superficie"),
  IMG("astronauta", ancho=360, x=300, y=1240, z=0.6, anim={"balanceo": [3, 0.8]}),
  IMG("retro", ancho=520, x=700, y=1380, z=0.65, keys=[{"t": 0, "y": 1300, "op": 0}, {"t": 0.3, "y": 1380, "op": 1, "ease": "salida"}]),
  brillo(640, 1330, 160, "#ffffff", 1.0, 0.7, keys=[{"t": 0.35, "op": 0, "escala": 0.3}, {"t": 0.5, "op": 1, "escala": 1.2}, {"t": 0.9, "op": 0.4}])],
  cam(1.15, 1.25, (560, 1280), (600, 1300)))
add(10.50, AMARILLO(0.25, 0.95, "ESPEJOS", y=1720))
fx(10.85, "brillo", -13)

# 9 · «Desde la Tierra se dispara un láser»
P(11.45, 13.19, ["#05070f", "#0b1430"], [BG("bg_espacio"), luna(780, 260, 200),
  IMG("observatorio", ancho=1180, x=540, y=960, z=0.3),
  flecha([[520, 1080], [770, 290]], 0.7, 1.2, "#5dff7a", 10, punta=False),
  brillo(520, 1080, 160, "#5dff7a", 0.9, 0.5, keys=[{"t": 0.6, "op": 0}, {"t": 0.75, "op": 1}], pulso=[0.3, 0.2])],
  cam(1.1, 1.0, (540, 1050), (560, 900)), entrada="desenfoque", dur=0.3)
add(11.45, AMARILLO(0.8, 1.7, "LÁSER", y=1700))
fx(12.15, "zap", -11)

# 10 · «la luz rebota» — impacto en la Luna y vuelta
P(13.19, 14.18, ESP, [BG("bg_espacio"), estrellas(25, 10), tierra(240, 1420, 520), luna(820, 560, 260),
  flecha([[330, 1300], [800, 590]], 0.0, 0.35, "#5dff7a", 9),
  flecha([[790, 640], [350, 1330]], 0.45, 0.95, "#ff5a8a", 9, [22, 14]),
  brillo(800, 590, 200, "#ffffff", 1.0, 0.55, keys=[{"t": 0.3, "op": 0, "escala": 0.3}, {"t": 0.42, "op": 1, "escala": 1.4}, {"t": 0.8, "op": 0}])],
  cam(1.05, 1.0, (560, 960), (540, 960)))
fx(13.5, "ding", -16, f=1320)

# 11 · «y vuelve en dos segundos y medio» — cronómetro
aguja = {"tipo": "forma", "forma": "poligono", "puntos": [[-7, 0], [0, -190], [7, 0], [0, 26]], "relleno": "#d62f22", "x": 540, "y": 1060, "z": 0.62,
         "keys": [{"t": 0.1, "rot": 0, "ease": "lineal"}, {"t": 1.3, "rot": 900}]}
P(14.18, 15.59, ["#1b2236", "#0b0f1c"], [brillo(540, 1000, 700, "#9fb3ff", 0.3), polvo("#cfe0ff", 20, sem=11),
  IMG("cronometro", ancho=640, x=540, y=1040, z=0.6), aguja,
  {"tipo": "forma", "forma": "circulo", "radio": 16, "relleno": "#1b2233", "x": 540, "y": 1060, "z": 0.63}],
  cam(1.0, 1.12, (540, 1050), (540, 1050)), entrada="zoom", dur=0.3, vineta=0.65)
add(14.18, {**ROT(0.1, 1.4, "", tam=120, x=540, y=1560), "contar": [0, 2.5, 1.1], "contar_desde": 0.1, "unidad": "SEGUNDOS", "decimales": 1})
for i in range(8): fx(14.3 + i * 0.15, "tic", -22)

# 12 · «Así se mide la distancia casi al centímetro» — 384.400 km y lupa a «±1 cm»
P(15.59, 16.90, ESP, [BG("bg_espacio"), estrellas(30, 12), tierra(200, 1520, 400), luna(880, 420, 170),
  flecha([[300, 1400], [820, 500]], 0.05, 0.7, "#ffffffcc", 6, [18, 14])], cam(1.0, 1.05), entrada="desenfoque", dur=0.3)
add(15.59, {**ROT(0.15, 1.3, "", tam=110, x=560, y=960), "contar": [0, 384400, 0.9], "contar_desde": 0.15, "unidad": "KM"})
P(16.90, 17.89, ["#1b2236", "#0b0f1c"], [brillo(540, 960, 600, "#9fb3ff", 0.3),
  IMG("regla", ancho=1400, x=540, y=1000, z=0.5), IMG("lupa", ancho=520, x=600, y=980, z=0.7, keys=[{"t": 0, "x": 900, "rot": 10}, {"t": 0.5, "x": 560, "rot": 0, "ease": "salida"}])],
  cam(1.0, 1.06, (540, 1000), (540, 1000)), entrada="corte")
add(16.90, CONTEXTO(0.2, 0.95, "± 1 CENTÍMETRO"))

# 13 · «¿Y por qué se va?» — la Luna sale disparada del plano
P(17.89, 18.97, ESP, [BG("bg_espacio"), estrellas(30, 13), tierra(400, 1200, 600, giro=8),
  luna(0, 0, 200, 0.55, keys=[{"t": 0, "x": 700, "y": 760}, {"t": 1.0, "x": 1000, "y": 420, "ease": "entrada"}]), *lineas_vel(900, 520, 4)],
  cam(1.0, 1.06, (540, 960), (600, 900)), entrada="desenfoque", dur=0.3)
add(17.89, AMARILLO(0.15, 1.0, "¿POR QUÉ?", y=1650))

# 14 · «Por las mareas» — olas que suben
P(18.97, 20.00, ["#0e3a5c", "#05192b"], [brillo(540, 600, 700, "#9fd8ff", 0.35),
  {"tipo": "agua", "nivel": 1000, "lado": "abajo", "amplitud": 40, "colores": ["#2a8bd0", "#0b4a7a"], "z": 0.4,
   "keys": [{"t": 0, "nivel": 1150}, {"t": 0.9, "nivel": 820, "ease": "suave"}]},
  luna(860, 360, 220, 0.2), polvo("#e6f6ff", 30, (0, 900, 1080, 1700), 14, "burbujas")],
  cam(1.0, 1.08, (540, 1000), (540, 1050)), entrada="zoom", dur=0.3)
add(18.97, AMARILLO(0.2, 1.0, "MAREAS", y=1650))
fx(19.0, "ola", -11)

# 15 · «El agua frena el giro de la Tierra»
P(20.00, 21.67, ESP, [BG("bg_espacio"), estrellas(25, 15), IMG("marea", ancho=900, x=540, y=1050, z=0.35, rot=-10, anim={"pulso": [0.02, 1.0]}),
  tierra(540, 1050, 560, giro=-4), luna(980, 880, 150),
  flecha([[300, 780], [540, 680], [780, 780]], 0.2, 1.0, "#ffd23f", 14, z=0.6),
  {"tipo": "forma", "forma": "poligono", "puntos": [[-60, -20], [60, -20], [60, 20], [-60, 20]], "relleno": "#d62f22", "x": 540, "y": 650, "z": 0.62, "rot": 0,
   "keys": [{"t": 0.9, "op": 0, "escala": 0.5}, {"t": 1.1, "op": 1, "escala": 1.0, "ease": "rebote"}]}],
  cam(1.0, 1.1, (540, 960), (540, 900)), entrada="desenfoque", dur=0.3)
add(20.00, CONTEXTO(0.4, 1.6, "LA TIERRA GIRA MÁS DESPACIO"))
fx(20.9, "pop", -14)

# 16 · «y esa energía empuja a la Luna hacia fuera» — órbitas que crecen
orb1 = {"tipo": "forma", "forma": "elipse", "ancho": 600, "alto": 600, "relleno": "#ffffff", "op_relleno": 0, "grosor": 3, "borde": "#ffffff55", "x": 540, "y": 1000, "z": 0.3}
orb2 = {"tipo": "forma", "forma": "elipse", "ancho": 880, "alto": 880, "relleno": "#ffffff", "op_relleno": 0, "grosor": 5, "borde": "#ffd23f",
        "x": 540, "y": 1000, "z": 0.3, "keys": [{"t": 0.3, "op": 0, "escala": 0.68}, {"t": 1.8, "op": 1, "escala": 1.0}]}
P(21.67, 23.91, ESP, [BG("bg_espacio"), estrellas(30, 16), orb1, orb2, tierra(540, 1000, 280, giro=10),
  luna(0, 0, 120, 0.5, keys=[{"t": 0, "x": 840, "y": 1000}, {"t": 0.8, "x": 860, "y": 740}, {"t": 1.6, "x": 820, "y": 640}, {"t": 2.2, "x": 940, "y": 740}]),
  *[flecha([[540 + dx * 160, 1000 + dy * 160], [540 + dx * 400, 1000 + dy * 400]], 0.2 + i * 0.12, 0.8 + i * 0.12, "#ffd23faa", 6, z=0.35)
    for i, (dx, dy) in enumerate([(0.7, -0.7), (-0.7, -0.7), (0.7, 0.7), (-0.7, 0.7)])]],
  cam(1.0, 0.94), entrada="zoom", dur=0.3)
add(21.67, AMARILLO(0.9, 2.1, "HACIA FUERA", y=1680))
fx(22.0, "whoosh", -13, dur=1.2)

# 17 · «Resultado: los días se alargan» — reloj que corre y sol que cruza
P(23.91, 25.87, ["#4f9be0", "#fbe8c2"], [BG("campo_dia"),
  *[{**s, "keys": [{"t": 0, "x": 120, "y": 760}, {"t": 1.9, "x": 960, "y": 500, "ease": "lineal"}]} for s in sol(0, 0, 90, 0.07)],
  *reloj(540, 1180, 520, 6, 0, 18, 0, 0.1, 1.8), polvo("#ffffff", 20, sem=17)],
  cam(1.0, 1.06, (540, 1100), (540, 1100)), entrada="desenfoque", dur=0.3, vineta=0.4)
add(23.91, CONTEXTO(0.2, 1.8, "DÍAS MÁS LARGOS"))
for i in range(6): fx(24.05 + i * 0.3, "tic", -22)

# 18 · «Con los dinosaurios» — jungla con dinosaurios caminando
P(25.87, 26.93, ["#2b1b3a", "#f6d08a"], [BG("bg_jungla"),
  IMG("dino_peq", ancho=380, y=1330, z=0.35, keys=[{"t": 0, "x": 900}, {"t": 1.1, "x": 780, "ease": "lineal"}], ex=-1),
  IMG("dino", ancho=880, y=1450, z=0.7, anim={"balanceo": [1.5, 0.7]}, keys=[{"t": 0, "x": 160}, {"t": 1.1, "x": 440, "ease": "lineal"}]),
  polvo("#ffd9a0", 25, sem=18)],
  cam(1.0, 1.06, (540, 1200), (500, 1200)), entrada="zoom", dur=0.3, vineta=0.5)
fx(26.0, "golpe", -15); fx(26.5, "golpe", -17)

# 19 · «un día duraba 23 horas y media»
P(26.93, 28.81, ["#2b1b3a", "#f6d08a"], [BG("bg_jungla"), {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 1920, "relleno": "#000000", "x": 540, "y": 960, "z": 0.2, "op": 0.45},
  *reloj(540, 1000, 600, 0, 0, 23, 30, 0.1, 1.6, z=0.6), IMG("dino_peq", ancho=300, y=1600, z=0.75, keys=[{"t": 0, "x": 1200}, {"t": 1.9, "x": 800, "ease": "lineal"}], ex=-1)],
  cam(1.0, 1.08, (540, 1000), (540, 1000)))
add(26.93, {**ROT(0.2, 1.8, "", tam=120, x=540, y=1560), "contar": [24, 23.5, 1.0], "contar_desde": 0.2, "unidad": "HORAS", "decimales": 1})
for i in range(7): fx(27.1 + i * 0.2, "tic", -22)

# 20 · «y el año tenía 372 días» — hojas de calendario volando
hojas = [IMG("calendario", ancho=520, x=540, y=1000, z=0.6 - i * 0.001, keys=[{"t": 0.15 + i * 0.22, "y": 1000, "rot": 0, "op": 1},
         {"t": 0.5 + i * 0.22, "y": 300, "rot": -25 + i * 9, "op": 0, "ease": "entrada"}]) for i in range(7)]
P(28.81, 31.19, ["#3a2a1c", "#1a1410"], [brillo(540, 900, 700, "#ffcf8a", 0.35),
  IMG("calendario", ancho=520, x=540, y=1000, z=0.59), *reversed(hojas)],
  cam(1.0, 1.06, (540, 1000), (540, 980)), entrada="desenfoque", dur=0.3, vineta=0.65)
add(28.81, {**ROT(0.1, 2.3, "", tam=130, x=540, y=1580), "contar": [365, 372, 1.6], "contar_desde": 0.1, "unidad": "DÍAS"})
for i in range(7): fx(29.0 + i * 0.22, "whoosh", -24, dur=0.18)

# 21 · «Lo sabemos por las rayas de una almeja fósil» — lupa sobre los anillos
P(31.19, 32.35, ["#2a241c", "#120f0a"], [brillo(540, 900, 700, "#ffe2b0", 0.35), polvo("#ffe9c0", 20, sem=21),
  IMG("almeja_fosil", ancho=880, x=540, y=1050, z=0.6)], cam(1.0, 1.08, (540, 1050), (540, 1000)), entrada="zoom", dur=0.3, vineta=0.65)
add(31.19, AMARILLO(0.2, 1.1, "ALMEJA FÓSIL", y=1650))
P(32.35, 33.52, ["#2a241c", "#120f0a"], [IMG("almeja_fosil", ancho=880, x=540, y=1050, z=0.6),
  IMG("lupa", ancho=560, x=0, y=900, z=0.7, keys=[{"t": 0, "x": 860}, {"t": 0.6, "x": 520, "ease": "salida"}])],
  cam(1.6, 1.75, (540, 820), (520, 800)))
add(32.35, CONTEXTO(0.3, 1.1, "1 RAYA = 1 DÍA"))
fx(32.5, "brillo", -16)

# 22 · «Hace 1.400 millones de años» — rebobinado: la Luna vuelve cerca
P(33.52, 35.47, ESP, [BG("bg_espacio"), estrellas(40, 22), tierra(380, 1250, 560, giro=40),
  luna(0, 0, 330, 0.5, keys=[{"t": 0, "x": 880, "y": 600, "escala": 0.48}, {"t": 1.6, "x": 720, "y": 820, "escala": 1.0, "ease": "salida"}]),
  flecha([[900, 560], [740, 790]], 0.2, 1.4, "#ff5a4a", 8, [18, 12])],
  cam(1.0, 1.05), entrada="desenfoque", dur=0.3)
add(33.52, {**ROT(0.15, 1.9, "", tam=100, x=540, y=560), "contar": [0, 1400, 1.2], "contar_desde": 0.15, "unidad": "MILLONES DE AÑOS ATRÁS", "capsula": "#c0392be6"})
fx(33.55, "whoosh", -12, dur=1.0)

# 23 · «el día duraba solo 18 horas» — Tierra girando rapidísimo y reloj
P(35.47, 37.38, ESP, [BG("bg_espacio"), estrellas(30, 23), tierra(540, 1150, 620, giro=70), luna(900, 520, 300),
  *reloj(260, 520, 300, 0, 0, 18, 0, 0.1, 1.5, z=0.65)],
  cam(1.0, 1.06, (540, 1000), (540, 1000)))
add(35.47, ROT(0.2, 1.8, "18", unidad="HORAS", tam=150, x=540, y=1620))
for i in range(9): fx(35.6 + i * 0.16, "tic", -22)

# 24 · «Y dentro de unos 600 millones de años» — avance rápido: la Luna se hace pequeña
P(37.38, 39.58, ESP, [BG("bg_espacio"), estrellas(40, 24), tierra(300, 1350, 480, giro=3),
  luna(0, 0, 260, 0.5, keys=[{"t": 0, "x": 640, "y": 900, "escala": 1.0}, {"t": 2.0, "x": 900, "y": 420, "escala": 0.35, "ease": "salida"}]),
  flecha([[620, 920], [880, 450]], 0.2, 1.6, "#5dd0ff", 8, [18, 12])],
  cam(1.0, 1.04), entrada="desenfoque", dur=0.3)
add(37.38, {**ROT(0.15, 2.1, "", tam=110, x=540, y=560), "contar": [0, 600, 1.3], "contar_desde": 0.15, "unidad": "MILLONES DE AÑOS", "contar_prefijo": "+"})
fx(37.4, "whoosh", -12, dur=1.0)

# 25 · «la Luna se verá tan pequeña que ya no podrá tapar el Sol» — eclipse anular
disco_peq = {"tipo": "forma", "forma": "circulo", "radio": 140, "relleno": "#06070c", "z": 0.35,
             "keys": [{"t": 0, "x": 160, "y": 820}, {"t": 2.2, "x": 540, "y": 900, "ease": "salida"}]}
P(39.58, 42.40, ["#020414", "#0d1638"], [BG("bg_eclipse"), *sol(540, 900, 175), disco_peq,
  IMG("personas_mirando", ancho=1080, x=540, y=1660, z=0.8)],
  cam(1.0, 1.08, (540, 1000), (540, 940)), entrada="zoom", dur=0.3)
add(39.58, CONTEXTO(1.4, 2.7, "YA NO LO TAPA"))
fx(39.6, "rumor", -18, dur=2.6)

# 26 · «Se acabarán los eclipses totales» — eclipse total (corona) que se apaga
P(42.40, 44.24, ["#020414", "#020414"], [BG("bg_eclipse"),
  {"tipo": "rayos", "n": 18, "longitud": 520, "apertura": 7, "intensidad": 0.6, "color": "#eaf2ff", "x": 540, "y": 900, "z": 0.3, "anim": {"girar": 6},
   "keys": [{"t": 0, "op": 1}, {"t": 1.2, "op": 1}, {"t": 1.7, "op": 0}]},
  brillo(540, 900, 380, "#eaf2ff", 0.8, 0.31, keys=[{"t": 0, "op": 1}, {"t": 1.2, "op": 1}, {"t": 1.7, "op": 0.1}]),
  {"tipo": "forma", "forma": "circulo", "radio": 178, "relleno": "#06070c", "x": 540, "y": 900, "z": 0.35},
  IMG("personas_mirando", ancho=1080, x=540, y=1660, z=0.8)],
  cam(1.1, 1.18, (540, 950), (540, 920)), entrada="corte")
add(42.40, {**AMARILLO(0.2, 1.7, "ADIÓS, ECLIPSES TOTALES", y=1380), "tam": 66})
fx(42.42, "golpe", -12)

# 27 · «Si puedes ver uno, no te lo pierdas» — personas mirando un eclipse total hoy; vuelve a la Luna (bucle)
P(44.24, 46.6, ["#020414", "#0d1638"], [BG("bg_eclipse"),
  {"tipo": "rayos", "n": 16, "longitud": 460, "apertura": 7, "intensidad": 0.55, "color": "#eaf2ff", "x": 540, "y": 820, "z": 0.3, "anim": {"girar": 5}},
  brillo(540, 820, 340, "#eaf2ff", 0.8, 0.31, pulso=[0.1, 1.2]),
  {"tipo": "forma", "forma": "circulo", "radio": 170, "relleno": "#06070c", "x": 540, "y": 820, "z": 0.35},
  brillo(470, 760, 40, "#ffffff", 1.0, 0.36, keys=[{"t": 1.2, "op": 0}, {"t": 1.4, "op": 1}, {"t": 1.9, "op": 0.2}]),
  IMG("personas_mirando", ancho=1180, x=540, y=1640, z=0.85)],
  cam(1.0, 1.12, (540, 1100), (540, 900)), entrada="desenfoque", dur=0.3)
add(44.24, AMARILLO(0.3, 2.2, "NO TE LO PIERDAS", y=1380))
fx(45.5, "brillo", -14)

# ------------------------------------------------------------------ guardar
claves = ["uñas", "tres", "coma", "ocho", "centímetros", "espejos", "láser", "mareas", "dinosaurios", "almeja", "dieciocho", "eclipses"]
M.guardar("02", "luna-densa", 46.6, claves, {"generar": "curiosidad", "semilla": 3})
import json  # noqa: E402
p = os.path.join(OUT, "episodio.json")
ep = json.load(open(p))
ep["id"] = "prueba-luna-densa"
if len(sys.argv) > 3:
    ep["audio"], ep["subtitulos"]["alineacion"] = os.path.abspath(sys.argv[2]), os.path.abspath(sys.argv[3])
else:
    ep["audio"], ep["subtitulos"]["alineacion"] = "locucion-provisional.mp3", "alineacion-provisional.json"
ep["sfx"] = sorted(FX, key=lambda e: e["t"])
json.dump(ep, open(p, "w"), ensure_ascii=False, indent=1)
print(len(M.S), "planos ·", len(FX), "efectos")
