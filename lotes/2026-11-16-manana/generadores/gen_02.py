"""02 — El pulpo tiene tres corazones y sangre azul (gancho de negación, metáfora visual de la casa con bombas).
Uso: python3 gen_02.py DIR_SALIDA"""
import sys
from comun_m import IMG, BG, ROT, AMARILLO, CONTEXTO, polvo, brillo, cam, Montaje, flecha

M = Montaje(sys.argv[1])
MAR = ["#1f7fa8", "#041a33"]
OSC = ["#0b1a2e", "#05101e"]
PX, PY, PA = 540, 1150, 900          # pulpo: centro y ancho (lienzo 1000x1100 → escala 0.9)
S = PA / 1000
GRANDE = (PX, PY - 140)              # corazón sistémico (en el manto)
PEQ = [(PX - 120, PY - 60), (PX + 120, PY - 60)]   # corazones branquiales
burbujas = {"tipo": "particulas", "clase": "burbujas", "color": "#e0fbff", "area": [0, 300, 1080, 1700], "n": 26, "tam": [4, 12], "vel": [0, -60], "z": 0.8, "semilla": 2}


def pulpo(nombre="pulpo", x=PX, y=PY, ancho=PA, z=0.5, **k):
    return IMG(nombre, ancho=ancho, x=x, y=y, z=z, **k)


def corazones(t_latido=0.9, grande_para=None, op=1.0):
    els = []
    kg = [{"t": 0, "op": op}]
    if grande_para:
        a, b = grande_para
        kg = [{"t": 0, "op": op}, {"t": a, "op": op}, {"t": a + 0.15, "op": 0.35}, {"t": b, "op": 0.35}, {"t": b + 0.2, "op": op}]
    els.append(brillo(GRANDE[0], GRANDE[1], 150, "#ff4a3a", 0.55, 0.55, pulso=[0.25, t_latido]))
    els.append(IMG("corazon_rojo", ancho=150, x=GRANDE[0], y=GRANDE[1], z=0.56, anim={"pulso": [0.12, t_latido]}, keys=kg))
    for i, (x, y) in enumerate(PEQ):
        els.append(brillo(x, y, 90, "#ff4a3a", 0.45, 0.55, pulso=[0.25, t_latido * 0.8]))
        els.append(IMG("corazon_rojo", ancho=90, x=x, y=y, z=0.56, fase=0.3 * i, anim={"pulso": [0.14, t_latido * 0.8]}))
    return els


def escena_pulpo(extra=(), latido=0.9, **k):
    return [BG("bg_mar"), burbujas, pulpo(anim={"flotar": [12, 3.2]}), *corazones(latido, **k), *extra]


def rotor(x, y, r, vel):
    return {"tipo": "forma", "forma": "poligono", "puntos": [[-r * 0.15, -r], [r * 0.15, -r], [r * 0.15, r], [-r * 0.15, r]],
            "relleno": "#20283a", "x": x, "y": y, "z": 0.3, "anim": {"girar": vel}}


# 1 · gancho: el pulpo con sus tres corazones encendidos (fotograma 0)
M.plano(0, 1.6, MAR, escena_pulpo(), cam(1.0, 1.05, (540, 1050), (540, 1030)), vineta=0.5)
M.plano(1.6, 3.35, MAR, escena_pulpo(), cam(1.55, 1.65, (540, 1000), (540, 990)), vineta=0.55)
M.add(ROT(0.3, 1.8, "3", unidad="CORAZONES", tam=130, x=540, y=1500))

# 2 · sangre: no es roja, es azul
cruz = [flecha([(380, 780), (700, 1200)], 1.75, 2.0, "#ffffff", 16, punta=False, z=0.7),
        flecha([(700, 780), (380, 1200)], 1.85, 2.1, "#ffffff", 16, punta=False, z=0.7)]
M.plano(3.35, 6.4, OSC, [brillo(540, 1000, 600, "#2b6ad2", 0.25),
        IMG("gota_roja", ancho=360, x=540, y=990, z=0.6, keys=[{"t": 0, "y": 600, "op": 0}, {"t": 0.4, "y": 990, "op": 1, "ease": "rebote"}, {"t": 2.2, "op": 1}, {"t": 2.4, "op": 0}]),
        *cruz,
        IMG("gota_azul", ancho=360, x=540, y=990, z=0.6, anim={"flotar": [10, 2]}, keys=[{"t": 2.25, "op": 0, "escala": 0.5}, {"t": 2.55, "op": 1, "escala": 1.0, "ease": "rebote"}])],
        cam(1.0, 1.06, (540, 1000), (540, 980)), entrada="desenfoque", dur=0.3, vineta=0.6)
M.S[-1]["elementos"][2]["keys"].append({"t": 2.25, "progreso": 1})
M.S[-1]["elementos"][3]["keys"].append({"t": 2.25, "progreso": 1})
for i in (2, 3):  # la cruz desaparece con la gota roja
    M.S[-1]["elementos"][i]["keys"] = [{"t": 1.75 + 0.1 * (i - 2), "progreso": 0, "op": 1}, {"t": 2.0 + 0.1 * (i - 2), "progreso": 1}, {"t": 2.2, "op": 1}, {"t": 2.35, "op": 0}]
M.add(AMARILLO(2.4, 3.0, "AZUL", y=1450))

# 3 · metáfora: una casa con tres bombas de agua
M.plano(6.4, 10.1, ["#203048", "#203048"], [BG("casa_bombas"), rotor(300, 1000, 50, 300), rotor(780, 1000, 50, 300), rotor(540, 1260, 85, 220),
        polvo("#ffffff", 10)], cam(1.0, 1.06, (540, 1000), (540, 1050)), entrada="zoom", dur=0.35, vineta=0.5)
M.add(AMARILLO(1.6, 3.6, "3 BOMBAS", y=1680))

# 4 · dos bombas pequeñas, una junto a cada branquia
agua = [flecha([(300, 1070), (300, 1390), (520, 1390)], 0.4, 1.4, "#5aa8ff", 12, z=0.35),
        flecha([(780, 1070), (780, 1390), (560, 1390)], 0.5, 1.5, "#5aa8ff", 12, z=0.35)]
M.plano(10.1, 12.95, ["#203048", "#203048"], [BG("casa_bombas"), rotor(300, 1000, 50, 420), rotor(780, 1000, 50, 420), rotor(540, 1260, 85, 220),
        brillo(300, 1000, 120, "#ffd23f", 0.6, 0.4, pulso=[0.2, 0.6]), brillo(780, 1000, 120, "#ffd23f", 0.6, 0.4, pulso=[0.2, 0.6]), *agua],
        cam(1.3, 1.38, (540, 1050), (540, 1060)), vineta=0.55)
M.add(CONTEXTO(0.2, 2.6, "2 PEQUEÑAS"))
# … empujan la sangre por las branquias para que coja oxígeno
branq = [brillo(PX - 300, PY - 90, 160, "#7fe0ff", 0.6, 0.5, pulso=[0.2, 1.2]), brillo(PX + 300, PY - 90, 160, "#7fe0ff", 0.6, 0.5, pulso=[0.2, 1.2]),
         flecha([PEQ[0], (PX - 300, PY - 90)], 0.2, 0.9, "#7fe0ff", 10), flecha([PEQ[1], (PX + 300, PY - 90)], 0.3, 1.0, "#7fe0ff", 10),
         {**burbujas, "area": [120, 900, 960, 1150], "n": 30, "vel": [0, -90]}]
M.plano(12.95, 15.7, MAR, escena_pulpo(branq, latido=0.6), cam(1.25, 1.32, (540, 1030), (540, 1020)), entrada="desenfoque", dur=0.3, vineta=0.55)
M.add(AMARILLO(0.2, 1.3, "BRANQUIAS", y=1560), ROT(1.5, 2.7, "+ OXÍGENO", tam=86, x=540, y=1560, color="#7fe0ff"))

# 5 · la tercera, la grande, reparte la sangre por todo el cuerpo
rayos = [flecha([GRANDE, (GRANDE[0] + dx, GRANDE[1] + dy)], 0.8 + i * 0.12, 1.6 + i * 0.12, "#5aa8ff", 10)
         for i, (dx, dy) in enumerate([(-360, 420), (-200, 560), (0, 620), (200, 560), (360, 420), (0, -260)])]
M.plano(15.7, 17.4, ["#203048", "#203048"], [BG("casa_bombas"), rotor(300, 1000, 50, 220), rotor(780, 1000, 50, 220), rotor(540, 1260, 85, 520),
        brillo(540, 1260, 200, "#ffd23f", 0.7, 0.4, pulso=[0.2, 0.5])], cam(1.45, 1.55, (540, 1230), (540, 1230)), entrada="corte", vineta=0.55)
M.add(CONTEXTO(0.1, 1.6, "LA GRANDE"))
M.plano(17.4, 19.6, MAR, escena_pulpo(rayos, latido=0.6), cam(1.0, 1.04, (540, 1100), (540, 1100)), entrada="desenfoque", dur=0.3, vineta=0.5)
M.add(AMARILLO(0.6, 2.2, "A TODO EL CUERPO", y=1720))

# 6 · ¿y por qué azul?
M.plano(19.6, 21.2, OSC, [brillo(540, 1000, 600, "#2b6ad2", 0.35), IMG("gota_azul", ancho=420, x=540, y=1000, z=0.6, anim={"balanceo": [6, 1.2]})],
        cam(1.0, 1.08, (540, 1000), (540, 980)), entrada="zoom", dur=0.3, vineta=0.6)
M.add(AMARILLO(0.2, 1.6, "¿POR QUÉ AZUL?", y=1500))

# 7 · nuestra sangre: hierro · la del pulpo: cobre (hemocianina)
roja = IMG("gota_roja", ancho=300, x=300, y=1000, z=0.6, anim={"flotar": [8, 2.2]})
azul = IMG("gota_azul", ancho=300, x=780, y=1000, z=0.6, anim={"flotar": [8, 2.4]}, keys=[{"t": 0, "op": 0}, {"t": 1.8, "op": 0}, {"t": 2.1, "op": 1}])
M.plano(21.2, 27.7, OSC, [brillo(300, 1000, 300, "#d22b2b", 0.3), brillo(780, 1000, 300, "#2b6ad2", 0.3, keys=[{"t": 1.8, "op": 0}, {"t": 2.2, "op": 1}]), roja, azul],
        cam(1.0, 1.05, (540, 1050), (540, 1030)), entrada="desenfoque", dur=0.3, vineta=0.6)
M.add(ROT(0.3, 6.5, "Fe", unidad="HIERRO", tam=100, x=300, y=1370, color="#ff8a7a"),
      ROT(2.2, 6.5, "Cu", unidad="COBRE", tam=100, x=780, y=1370, color="#8ab8ff"),
      AMARILLO(4.6, 6.4, "HEMOCIANINA", y=1640), {**CONTEXTO(0.3, 6.4, "TÚ"), "x": 300}, {**CONTEXTO(2.2, 6.4, "PULPO"), "x": 780})

# 8 · con oxígeno se vuelve azul
M.plano(27.7, 30.7, OSC, [brillo(540, 1000, 600, "#2b6ad2", 0.3, keys=[{"t": 0, "op": 0.2}, {"t": 2.4, "op": 1}]),
        IMG("gota_azul", ancho=420, x=540, y=1000, z=0.6, keys=[{"t": 0, "op": 0.25}, {"t": 2.5, "op": 1}]),
        {**burbujas, "area": [200, 700, 880, 1400], "n": 40, "vel": [0, -80], "color": "#ffffff"}],
        cam(1.0, 1.08, (540, 1000), (540, 980)), entrada="corte", vineta=0.6)
M.add(ROT(0.4, 2.9, "+ O2", tam=110, x=540, y=1500, color="#7fe0ff"))

# 9 · un detalle rarísimo: al nadar, el corazón grande se para
M.plano(30.7, 33.0, MAR, escena_pulpo(), cam(1.25, 1.4, (540, 1050), (540, 1000)), entrada="desenfoque", dur=0.3, vineta=0.55)
M.add(AMARILLO(0.6, 2.2, "RARÍSIMO", y=1600))
ecg = {"tipo": "flecha", "puntos": [[140, 1700], [260, 1700], [290, 1620], [320, 1780], [350, 1700], [470, 1700], [500, 1620], [530, 1780], [560, 1700], [940, 1700]],
       "grosor": 8, "color": "#ff5a4a", "punta": False, "z": 1, "hud": True, "keys": [{"t": 0, "progreso": 0}, {"t": 3.3, "progreso": 1, "ease": "lineal"}]}
nada = pulpo("pulpo_nada", ancho=760, keys=[{"t": 0, "y": 1700, "x": 600}, {"t": 3.5, "y": 820, "x": 480}], anim={"balanceo": [5, 0.8]})
M.plano(33.0, 36.5, MAR, [BG("bg_mar"), burbujas, nada, ecg, IMG("corazon_rojo", ancho=130, x=900, y=1540, z=1, hud=True,
        anim={"pulso": [0.12, 0.7]}, keys=[{"t": 0, "op": 1}, {"t": 2.3, "op": 1}, {"t": 2.5, "op": 0.3, "escala": 0.8}])],
        cam(1.0, 1.04, (540, 1100), (540, 1050)), entrada="corte", vineta=0.5)
M.add(ROT(2.4, 3.5, "PAUSA", tam=90, x=700, y=1440, color="#ff6b5a"))

# 10 · por eso prefiere arrastrarse por el fondo
M.plano(36.5, 40.6, MAR, [BG("bg_mar"), burbujas, pulpo(ancho=620, y=1380, z=0.6, anim={"balanceo": [4, 1.2]}, keys=[{"t": 0, "x": 1250}, {"t": 4.1, "x": 640}])],
        cam(1.2, 1.25, (600, 1350), (560, 1360)), entrada="desenfoque", dur=0.3, vineta=0.5)
M.add(AMARILLO(2.7, 4.0, "NADAR LE AGOTA", y=900))

# 11 · y aún hay más: dos tercios de sus neuronas, en los brazos
M.plano(40.6, 42.0, MAR, escena_pulpo(), cam(1.0, 1.06, (540, 1100), (540, 1100)), entrada="zoom", dur=0.3, vineta=0.55)
M.add(AMARILLO(0.2, 1.3, "AÚN HAY MÁS", y=1700))
chispas = {"tipo": "particulas", "clase": "chispas", "color": "#9ff6ff", "area": [140, 1220, 940, 1640], "n": 70, "tam": [3, 7], "vel": [0, -10], "z": 0.7, "semilla": 8}
M.plano(42.0, 46.3, OSC, [BG("bg_mar"), {"tipo": "forma", "forma": "rect", "ancho": 1100, "alto": 1940, "relleno": "#020812", "x": 540, "y": 960, "z": 0.3, "op": 0.55},
        pulpo(anim={"flotar": [10, 3]}), chispas, brillo(540, 1450, 520, "#5ae0ff", 0.35, 0.6, pulso=[0.15, 1.3])],
        cam(1.0, 1.05, (540, 1200), (540, 1250)), entrada="desenfoque", dur=0.3, vineta=0.6)
M.add(ROT(0.4, 4.2, "2/3", unidad="DE SUS NEURONAS", tam=120, x=540, y=760), CONTEXTO(2.6, 4.2, "EN LOS BRAZOS"))

# 12 · remate: tres corazones, sangre azul y brazos que casi piensan solos
M.plano(46.3, 47.7, MAR, escena_pulpo(), cam(1.6, 1.7, (540, 1000), (540, 990)), entrada="corte", vineta=0.55)
M.add(ROT(0.1, 1.3, "×3", tam=110, x=540, y=1450))
M.plano(47.7, 48.65, OSC, [brillo(540, 1000, 600, "#2b6ad2", 0.4), IMG("gota_azul", ancho=420, x=540, y=1000, z=0.6, anim={"flotar": [10, 1.2]})],
        cam(1.0, 1.06), entrada="corte", vineta=0.6)
M.plano(48.65, 51.1, OSC, [BG("bg_mar"), {"tipo": "forma", "forma": "rect", "ancho": 1100, "alto": 1940, "relleno": "#020812", "x": 540, "y": 960, "z": 0.3, "op": 0.55},
        pulpo(anim={"balanceo": [4, 1.0]}), chispas], cam(1.3, 1.4, (540, 1400), (540, 1420)), entrada="corte", vineta=0.6)

# 13 · bucle: vuelve el plano del principio
M.plano(51.1, 53.6, MAR, escena_pulpo(), cam(1.05, 1.0, (540, 1030), (540, 1050)), entrada="desenfoque", dur=0.35, vineta=0.5)
M.add(AMARILLO(0.4, 2.4, "¿DE ESTE PLANETA?", y=1720))

M.guardar("02", "pulpo-tres-corazones", 53.6,
          ["corazón", "tres", "azul", "bombas", "branquia", "oxígeno", "hierro", "cobre", "hemocianina", "nada", "neuronas", "brazos"],
          {"generar": "misterio", "semilla": 12})
