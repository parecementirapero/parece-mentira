"""03 — Los moáis tienen cuerpo, v4 (ilustración SVG + un plano por frase). Audio v2. Uso: python3 gen_03.py DIR_SALIDA"""
import sys
from comun_v4 import IMG, BG, ROT, AMARILLO, CONTEXTO, polvo, brillo, cam, Montaje

M = Montaje(sys.argv[1])
CIELO = ["#3e88d0", "#e9f4f2"]
SUELO = 880          # línea de hierba en bg_seccion
ANCHO_M = 420        # moái entero: 400x1100 → escala 1.05
K = ANCHO_M / 400


def moai_seccion(x, nombre="moai_entero", ancho=ANCHO_M, z=0.5, **kw):
    """Moái entero con la cabeza asomando sobre SUELO (cuello a ras de hierba)."""
    k = ancho / 400
    return IMG(nombre, ancho=ancho, x=x, y=SUELO - 500 * k + 550 * k, z=z, **kw)


def tierra_encima(op_keys, z=0.55, y0=SUELO + 30):
    """Capa de tierra que tapa el cuerpo (se aclara para «ver» el torso)."""
    return {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 1100, "relleno": ["#6a4c30", "#3a2816"], "x": 540, "y": y0 + 550, "z": z, "keys": op_keys}


# 1 · gancho: una cabeza gigante en la hierba
cabeza = IMG("moai_cabeza", ancho=520, x=540, z=0.5, keys=[{"t": 0, "y": 900}, {"t": 3, "y": 860}])
M.plano(0, 3.15, CIELO, [BG("bg_isla"), cabeza, {"tipo": "suelo", "material": "hierba", "borde": 1110, "z": 0.55, "semilla": 4}, polvo("#ffffff", 15)],
        cam(1.0, 1.1, (540, 960), (540, 900)), vineta=0.45)
M.plano(3.15, 4.65, CIELO, [BG("bg_isla"), IMG("moai_cabeza", ancho=520, x=540, y=860, z=0.5)], cam(1.7, 1.85, (540, 760), (540, 740)), vineta=0.5)
M.add(AMARILLO(0.2, 1.3, "¿SOLO CABEZAS?", y=1650))

# 2 · primera pista: la ladera de Rano Raraku
M.plano(4.65, 8.4, CIELO, [BG("bg_volcan"), polvo("#ffffff", 15)], cam(1.0, 1.08, (540, 900), (540, 1000)), entrada="desenfoque", dur=0.35, vineta=0.45)
M.add(CONTEXTO(0.1, 1.2, "PISTA 1"), ROT(1.9, 3.6, "150", unidad="ESTATUAS", tam=120, x=540, y=1700))
M.plano(8.4, 11.35, CIELO, [BG("bg_volcan")], cam(1.5, 1.6, (520, 1420), (600, 1400)), vineta=0.5)
M.plano(11.35, 15.45, CIELO, [BG("bg_volcan")], cam(1.3, 1.4, (540, 820), (560, 860)), vineta=0.5)
M.add(CONTEXTO(0.1, 2.0, "RANO RARAKU"), AMARILLO(1.8, 3.6, "CANTERA", y=1650))

# 3 · segunda pista: 1914, empiezan a cavar
arq = IMG("arqueologo", ancho=330, y=1290, z=0.6, anim={"balanceo": [3, 0.8]}, keys=[{"t": 0, "x": 1250}, {"t": 1.2, "x": 820, "ease": "salida"}])
M.plano(15.45, 16.8, CIELO, [BG("bg_isla"), IMG("moai_cabeza", ancho=430, x=420, y=900, z=0.5), arq], cam(1.0, 1.06, (540, 1000), (560, 1000)),
        entrada="zoom", dur=0.35, vineta=0.45)
M.add(CONTEXTO(0.1, 1.2, "PISTA 2"))
cava = IMG("arqueologo", ancho=330, x=740, y=1290, z=0.6, anim={"balanceo": [9, 0.7]})
tierra_vuela = {"tipo": "particulas", "clase": "polvo", "color": "#7a5a3a", "area": [560, 1080, 760, 1250], "n": 40, "tam": [5, 12], "vel": [-60, -120], "z": 0.65, "semilla": 3}
M.plano(16.8, 21.2, ["#d9c49a", "#c9a46a"], [BG("bg_isla"), IMG("moai_cabeza", ancho=430, x=420, y=900, z=0.5), cava, tierra_vuela,
        {"tipo": "forma", "forma": "elipse", "ancho": 360, "alto": 70, "relleno": "#3a2816", "x": 470, "y": 1150, "z": 0.52,
         "keys": [{"t": 0.5, "escala": 0.2}, {"t": 4, "escala": 1.0}]}], cam(1.15, 1.25, (580, 1050), (560, 1080)), vineta=0.5)
M.add(CONTEXTO(0.2, 2.4, "1914 · PRIMERA EXCAVACIÓN"))

# 4 · la respuesta: un torso entero bajo tierra (vista en sección)
M.plano(21.2, 25.45, CIELO, [BG("bg_seccion"), moai_seccion(540), tierra_encima([{"t": 0, "op": 1}, {"t": 1.6, "op": 1}, {"t": 2.6, "op": 0.25}])],
        cam(1.0, 1.06, (540, 1100), (540, 1150)), entrada="zoom", dur=0.4, vineta=0.5)
M.add(AMARILLO(2.0, 3.8, "TORSO ENTERRADO", y=1780))
# 5 · siglos de erosión lo cubrieron
lluvia = {"tipo": "particulas", "clase": "polvo", "color": "#8a6a44", "area": [0, 300, 1080, 900], "n": 70, "tam": [3, 8], "vel": [10, 160], "z": 0.6, "semilla": 6}
M.plano(25.45, 29.05, CIELO, [BG("bg_seccion"), moai_seccion(540), tierra_encima([{"t": 0, "op": 0.25}, {"t": 3.2, "op": 0.85}]), lluvia],
        cam(1.25, 1.35, (540, 1000), (540, 1000)))
M.add(AMARILLO(0.3, 1.6, "EROSIÓN", y=1780), CONTEXTO(1.8, 3.4, "SIGLOS"))

# 6 · 2010–2014: el equipo de Van Tilburg desentierra dos
zanja = {"tipo": "forma", "forma": "rect", "ancho": 980, "alto": 1000, "relleno": ["#5a3f26", "#3a2816"], "x": 540, "y": SUELO + 540, "z": 0.45}
M.plano(29.05, 31.35, CIELO, [BG("bg_seccion"), zanja, moai_seccion(330, ancho=360, z=0.5), moai_seccion(760, "moai_espalda", 360, z=0.5),
        tierra_encima([{"t": 0, "op": 0.6}, {"t": 2, "op": 0.0}], z=0.55, y0=SUELO + 200)], cam(1.0, 1.05, (540, 1150), (540, 1150)), entrada="desenfoque", dur=0.35)
M.add(CONTEXTO(0.2, 2.0, "2010–2014 · VAN TILBURG"))
# 7 · grabados en la espalda
lupa = IMG("lupa", ancho=420, z=0.7, keys=[{"t": 0.3, "x": 1100, "y": 1500}, {"t": 1.6, "x": 600, "y": 1050, "ease": "salida"},
                                          {"t": 3.5, "x": 560, "y": 1300}, {"t": 5.5, "x": 600, "y": 1100}])
M.plano(31.35, 37.7, ["#5a3f26", "#3a2816"], [BG("bg_seccion"), zanja, moai_seccion(540, "moai_espalda", 520, z=0.5), lupa,
        brillo(540, 1150, 160, "#fff3c0", 0.6, 0.6, pulso=[0.2, 1.2])], cam(1.2, 1.3, (540, 1150), (540, 1200)), vineta=0.55)
M.add(AMARILLO(3.0, 5.6, "GRABADOS", y=1780))

# 8 · casi mil moáis en la isla
M.plano(37.7, 39.7, ["#2a2f6b", "#ffe6b8"], [BG("bg_costa"), brillo(540, 900, 300, "#fff3c0", 0.4, 0.07, pulso=[0.06, 2])],
        cam(1.0, 1.08, (540, 1100), (540, 1080)), entrada="zoom", dur=0.4, vineta=0.5)
M.add(ROT(0.3, 1.8, "~1.000", unidad="MOÁIS", tam=120, x=540, y=1600))
# 9 · hasta diez metros y decenas de toneladas
alto = IMG("moai_entero", ancho=420, x=480, y=1060, z=0.5)
regla = {"tipo": "flecha", "puntos": [[760, 1630], [760, 470]], "grosor": 8, "color": "#ffffff", "contorno": "#00000066", "z": 0.6,
         "keys": [{"t": 0.3, "progreso": 0}, {"t": 1.4, "progreso": 1}]}
M.plano(39.7, 43.4, CIELO, [BG("bg_isla"), alto, IMG("persona_escala", ancho=70, x=860, y=1550, z=0.6), regla],
        cam(1.0, 1.04, (540, 1050), (540, 1030)), entrada="desenfoque", dur=0.35, vineta=0.45)
M.add(ROT(0.6, 2.0, "10 m", unidad="DE ALTO", tam=110, x=540, y=1760), CONTEXTO(2.2, 3.5, "DECENAS DE TONELADAS"))

# 10 · cierre en bucle: la cabeza que asoma… y lo que hay debajo
M.plano(43.4, 46.24, CIELO, [BG("bg_seccion"), moai_seccion(540), tierra_encima([{"t": 0, "op": 1}, {"t": 1.0, "op": 0.2}])],
        cam(1.5, 1.0, (540, 700), (540, 1100)), entrada="zoom", dur=0.4, vineta=0.5)
M.add(AMARILLO(1.0, 2.6, "SOLO LA MITAD", y=1780))

M.guardar("03", "moais-con-cuerpo", 46.24, ["cabezas", "pista", "Rano", "Raraku", "torso", "erosión", "grabados", "diez", "metros", "mitad"],
          {"generar": "misterio", "semilla": 5})
