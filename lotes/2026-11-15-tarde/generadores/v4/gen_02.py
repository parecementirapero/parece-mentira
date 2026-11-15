"""02 — La Luna se aleja, v4 (ilustración SVG + un plano por frase). Audio v2. Uso: python3 gen_02.py DIR_SALIDA"""
import sys
from comun_v4 import IMG, BG, ROT, AMARILLO, CONTEXTO, polvo, brillo, cam, Montaje

M = Montaje(sys.argv[1])
ESP = ["#02030a", "#0a1030"]
estrellas = polvo("#ffffff", 40, (0, 0, 1080, 1920), 3, "estrellas")


def tierra(x, y, ancho, z=0.4, giro=4): return IMG("tierra_hd", ancho=ancho, x=x, y=y, z=z, anim={"girar": giro})
def luna(x, y, ancho, z=0.4, keys=None): return IMG("luna_hd", ancho=ancho, x=x, y=y, z=z, keys=keys or [])


# 1 · «Mira tus uñas»: primer plano de la uña
dedo = IMG("dedo", ancho=520, x=540, z=0.6, keys=[{"t": 0, "y": 1500}, {"t": 0.6, "y": 1250, "ease": "salida"}])
M.plano(0, 1.03, ["#2a1a14", "#120a08"], [brillo(540, 700, 650, "#ffcf9a", 0.45), dedo], cam(1.15, 1.3, (540, 1000), (540, 960)), vineta=0.7)

# 2 · la Luna se aleja (espacio) — y la uña crece
M.plano(1.03, 2.95, ESP, [BG("bg_espacio"), tierra(300, 1150, 560), luna(760, 760, 200, keys=[{"t": 0, "x": 720, "y": 800}, {"t": 1.9, "x": 860, "y": 640}]),
        {"tipo": "flecha", "puntos": [[700, 820], [900, 640]], "grosor": 8, "color": "#ffffffaa", "discontinua": [20, 14], "z": 0.5,
         "keys": [{"t": 0.3, "progreso": 0}, {"t": 1.4, "progreso": 1}]}], cam(1.0, 1.06, (540, 960), (580, 900)), entrada="desenfoque", dur=0.35)
dedo2 = IMG("dedo", ancho=520, x=540, z=0.6, ey=1.0, keys=[{"t": 0, "y": 1250, "ey": 1.0}, {"t": 1.9, "y": 1180, "ey": 1.06}])
M.plano(2.95, 5.0, ["#2a1a14", "#120a08"], [brillo(540, 700, 650, "#ffcf9a", 0.45), dedo2, IMG("luna_hd", ancho=140, x=860, y=560, z=0.3,
        keys=[{"t": 0, "x": 820, "y": 600}, {"t": 2, "x": 900, "y": 520}])], cam(1.0, 1.05, (540, 1000), (540, 960)), vineta=0.7)
M.add(CONTEXTO(0.2, 1.8, "UÑA ≈ LUNA"))

# 3 · 3,8 cm al año: regla
M.plano(5.0, 7.6, ["#1b2236", "#0b0f1c"], [brillo(540, 900, 600, "#9fb3ff", 0.25), IMG("regla", ancho=1000, x=540, y=1050, z=0.5),
        {"tipo": "barra", "x": 540 - 480 + 18 + 182, "y": 920, "ancho": 365, "alto": 40, "color": "#ff5a4a", "fondo": "#ffffff15", "z": 0.55,
         "keys": [{"t": 0.3, "progreso": 0}, {"t": 1.6, "progreso": 1, "ease": "salida"}]}], cam(1.2, 1.35, (330, 1000), (330, 1000)), entrada="zoom", dur=0.35, vineta=0.6)
M.add(ROT(0.6, 2.4, "3,8", unidad="CM/AÑO", tam=120, x=540, y=1450))

# 4 · ¿cómo lo sabemos?
M.plano(7.6, 9.95, ESP, [BG("bg_espacio"), tierra(260, 1300, 620), luna(800, 650, 220)], cam(1.0, 1.08, (540, 960), (540, 920)), entrada="desenfoque", dur=0.35)
M.add(AMARILLO(0.5, 2.0, "¿CÓMO LO SABEMOS?", y=1700))

# 5 · astronautas del Apolo en la Luna
astro = IMG("astronauta", ancho=360, y=1260, z=0.7, anim={"balanceo": [3, 0.9]}, keys=[{"t": 0, "x": -80}, {"t": 2.2, "x": 420, "ease": "salida"}])
M.plano(9.95, 13.5, ["#02030a", "#02030a"], [BG("bg_superficie"), IMG("tierra_hd", ancho=260, x=820, y=420, z=0.1, anim={"girar": 3}), astro,
        IMG("retro", ancho=380, x=720, y=1420, z=0.65, keys=[{"t": 0, "op": 0}, {"t": 2.4, "op": 0}, {"t": 2.8, "op": 1}])],
        cam(1.0, 1.08, (540, 1100), (600, 1150)), entrada="zoom", dur=0.4, vineta=0.6)
M.add(AMARILLO(2.4, 3.3, "ESPEJOS", y=1700))

# 6 · Apolo 11, 1969: el retrorreflector de cerca
M.plano(13.5, 17.19, ["#02030a", "#02030a"], [BG("bg_superficie"), IMG("retro", ancho=760, x=540, y=1300, z=0.65),
        brillo(470, 1240, 120, "#ffffff", 0.9, 0.7, pulso=[0.4, 0.9])], cam(1.0, 1.1, (540, 1250), (540, 1220)), vineta=0.6)
M.add(CONTEXTO(0.4, 2.4, "APOLO 11 · 1969"), AMARILLO(0.8, 2.5, "RETRORREFLECTORES", y=1720))
M.plano(17.19, 18.5, ["#02030a", "#02030a"], [BG("bg_superficie"), IMG("retro", ancho=760, x=540, y=1300, z=0.65),
        brillo(470, 1240, 160, "#bfe0ff", 1.0, 0.7, pulso=[0.5, 0.5])], cam(1.4, 1.5, (470, 1260), (470, 1260)))
M.add(ROT(0.1, 1.1, "SIGUEN", unidad="FUNCIONANDO", tam=100, x=540, y=1600))

# 7 · el láser desde la Tierra
laser = {"tipo": "flecha", "puntos": [[520, 1080], [770, 290]], "grosor": 10, "color": "#5dff7a", "punta": False, "z": 0.5,
         "keys": [{"t": 0.3, "progreso": 0}, {"t": 1.0, "progreso": 1}]}
M.plano(18.5, 20.35, ["#05070f", "#0b1430"], [BG("bg_espacio"), luna(780, 260, 200), IMG("observatorio", ancho=1180, x=540, y=960, z=0.3), laser,
        brillo(520, 1080, 140, "#5dff7a", 0.8, 0.5, pulso=[0.3, 0.4])], cam(1.0, 1.06, (540, 1000), (560, 900)), entrada="desenfoque", dur=0.35)
M.add(AMARILLO(0.6, 1.6, "LÁSER", y=1700))

# 8 · rebota y vuelve
ida = {"tipo": "flecha", "puntos": [[330, 1250], [780, 640]], "grosor": 9, "color": "#5dff7a", "punta": True, "z": 0.5,
       "keys": [{"t": 0.1, "progreso": 0}, {"t": 0.8, "progreso": 1}]}
vuelta = {"tipo": "flecha", "puntos": [[760, 690], [350, 1290]], "grosor": 9, "color": "#ff5a8a", "punta": True, "discontinua": [22, 14], "z": 0.5,
          "keys": [{"t": 0.9, "progreso": 0}, {"t": 1.6, "progreso": 1}]}
M.plano(20.35, 22.7, ESP, [BG("bg_espacio"), tierra(260, 1340, 560), luna(820, 620, 220), ida, vuelta,
        brillo(800, 650, 120, "#ffffff", 0.9, 0.5, keys=[{"t": 0.75, "op": 0}, {"t": 0.85, "op": 1}, {"t": 1.3, "op": 0}])],
        cam(1.0, 1.04, (540, 960), (540, 940)))
M.add(CONTEXTO(0.3, 2.0, "TIERRA · LUNA · TIERRA"))

# 9 · cronómetro: cuánto tarda (≈2,5 s)
aguja = {"tipo": "forma", "forma": "poligono", "puntos": [[-7, 0], [0, -190], [7, 0], [0, 26]], "relleno": "#d62f22", "x": 540, "y": 1060, "z": 0.62,
         "keys": [{"t": 0.3, "rot": 0, "ease": "lineal"}, {"t": 2.8, "rot": 900}]}
M.plano(22.7, 26.6, ["#1b2236", "#0b0f1c"], [brillo(540, 1000, 700, "#9fb3ff", 0.3), IMG("cronometro", ancho=640, x=540, y=1040, z=0.6), aguja,
        {"tipo": "forma", "forma": "circulo", "radio": 16, "relleno": "#1b2233", "x": 540, "y": 1060, "z": 0.63}],
        cam(1.0, 1.1, (540, 1050), (540, 1050)), entrada="zoom", dur=0.35, vineta=0.65)
M.add(CONTEXTO(0.4, 2.6, "IDA Y VUELTA ≈ 2,5 s"))

# 10 · 384.000 km
M.plano(26.6, 29.2, ESP, [BG("bg_espacio"), tierra(200, 1500, 380), luna(880, 420, 160),
        {"tipo": "flecha", "puntos": [[300, 1380], [820, 500]], "grosor": 6, "color": "#ffffffcc", "discontinua": [18, 14], "z": 0.5,
         "keys": [{"t": 0.1, "progreso": 0}, {"t": 1.0, "progreso": 1}]}], cam(1.0, 1.05), entrada="desenfoque", dur=0.35)
M.add({**ROT(0.3, 2.3, "", tam=120, x=560, y=960), "contar": [0, 384000, 1.2], "contar_desde": 0.3, "unidad": "KM"})

# 11 · las mareas frenan la Tierra
M.plano(29.2, 31.1, ESP, [BG("bg_espacio"), IMG("marea", ancho=900, x=540, y=1050, z=0.35, rot=-10), tierra(540, 1050, 560, giro=-14),
        luna(980, 880, 150)], cam(1.0, 1.06, (540, 1000), (560, 1000)), entrada="zoom", dur=0.4)
M.add(AMARILLO(0.3, 1.6, "MAREAS", y=1650))
freno = {"tipo": "flecha", "puntos": [[300, 780], [540, 680], [780, 780]], "grosor": 14, "color": "#ffd23f", "z": 0.6,
         "keys": [{"t": 0.2, "progreso": 0}, {"t": 1.0, "progreso": 1}]}
M.plano(31.1, 34.2, ESP, [BG("bg_espacio"), IMG("marea", ancho=900, x=540, y=1050, z=0.35, rot=-10), tierra(540, 1050, 560, giro=-6), freno,
        luna(980, 880, 150)], cam(1.2, 1.3, (540, 950), (540, 950)))
M.add(CONTEXTO(1.0, 2.8, "LA TIERRA GIRA MÁS DESPACIO"))

# 12 · empuja a la Luna a una órbita más amplia
orb1 = {"tipo": "forma", "forma": "elipse", "ancho": 700, "alto": 700, "relleno": "#ffffff", "op_relleno": 0, "grosor": 3, "borde": "#ffffff55", "x": 540, "y": 1000, "z": 0.3}
orb2 = {"tipo": "forma", "forma": "elipse", "ancho": 900, "alto": 900, "relleno": "#ffffff", "op_relleno": 0, "grosor": 4, "borde": "#ffd23f",
        "x": 540, "y": 1000, "z": 0.3, "keys": [{"t": 0.6, "op": 0, "escala": 0.78}, {"t": 2.2, "op": 1, "escala": 1.0}]}
M.plano(34.2, 37.45, ESP, [BG("bg_espacio"), orb1, orb2, tierra(540, 1000, 300),
        luna(0, 0, 130, keys=[{"t": 0, "x": 890, "y": 1000}, {"t": 1.2, "x": 838, "y": 700}, {"t": 2.4, "x": 958, "y": 640}, {"t": 3.2, "x": 990, "y": 900}])],
        cam(1.0, 1.04), entrada="desenfoque", dur=0.35)
M.add(AMARILLO(0.8, 2.6, "ÓRBITA MÁS AMPLIA", y=1680))

# 13 · los días se alargan, muy despacio
caracol = IMG("caracol", ancho=300, y=1580, z=0.7, keys=[{"t": 0, "x": 160}, {"t": 6, "x": 520, "ease": "lineal"}])
M.plano(37.45, 40.4, ["#4f9be0", "#fbe8c2"], [BG("campo_dia"), brillo(760, 560, 300, "#fff3c0", 0.6, 0.07, pulso=[0.06, 2.5]),
        {"tipo": "barra", "x": 540, "y": 1300, "ancho": 820, "alto": 34, "color": "#ffd23f", "fondo": "#ffffff40", "z": 0.6,
         "keys": [{"t": 0.3, "progreso": 0.6}, {"t": 2.6, "progreso": 0.61}]}, caracol, polvo("#ffffff", 20)],
        cam(1.0, 1.06, (540, 1100), (560, 1150)), entrada="zoom", dur=0.4, vineta=0.4)
M.add(CONTEXTO(0.3, 2.4, "EL DÍA SE ALARGA"))
M.plano(40.4, 43.1, ["#4f9be0", "#fbe8c2"], [BG("campo_dia"), caracol], cam(1.5, 1.6, (330, 1560), (380, 1560)), vineta=0.4)
M.S[-1]["elementos"][1]["keys"] = [{"t": 0, "x": 330}, {"t": 3, "x": 400, "ease": "lineal"}]
M.add(ROT(0.2, 2.3, "+1 s", unidad="CADA 40.000 AÑOS", tam=120, x=540, y=1150))

# 14 · tranquilo: Tierra y Luna en calma (vuelve al primer plano del espacio)
M.plano(43.1, 46.66, ESP, [BG("bg_espacio"), tierra(300, 1150, 560), luna(760, 760, 200, keys=[{"t": 0, "x": 740, "y": 780}, {"t": 3.5, "x": 770, "y": 750}])],
        cam(1.1, 1.0, (540, 960), (540, 960)), entrada="desenfoque", dur=0.4)
M.add(AMARILLO(1.0, 3.0, "TRANQUILO", y=1700))

M.guardar("02", "luna-se-aleja", 46.66, ["uñas", "tres", "coma", "ocho", "centímetros", "espejos", "láser", "kilómetros", "mareas", "segundo", "mañana"],
          {"generar": "curiosidad", "semilla": 3})
