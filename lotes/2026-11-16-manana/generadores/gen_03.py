"""03 — Los vikingos llegaron a América en 1021 (reconstrucción con salto temporal). Uso: python3 gen_03.py DIR_SALIDA"""
import sys
from comun_m import IMG, BG, ROT, AMARILLO, CONTEXTO, polvo, brillo, cam, Montaje, flecha, contador

M = Montaje(sys.argv[1])
NORTE = ["#22324c", "#0c1a2a"]
DIA = ["#5f86b0", "#3d5a26"]
MADERA = ["#2a1c12", "#120c08"]
olas = {"tipo": "particulas", "clase": "polvo", "color": "#d6e6f0", "area": [0, 1150, 1080, 1920], "n": 30, "tam": [2, 4], "vel": [-30, 0], "z": 0.7, "semilla": 5}


def costa(extra=(), drakkar_x=(330, 360), carabela=True, t=4.3):
    els = [BG("bg_mar_norte"), olas,
           IMG("drakkar", ancho=720, y=1330, z=0.6, anim={"balanceo": [2.5, 2.2], "flotar": [8, 2.2]},
               keys=[{"t": 0, "x": drakkar_x[0]}, {"t": t, "x": drakkar_x[1]}])]
    if carabela:
        els.append(IMG("carabela", ancho=230, y=1075, z=0.3, anim={"balanceo": [2, 2.6]}, keys=[{"t": 0, "x": 930}, {"t": t, "x": 870}]))
    return els + list(extra)


# 1 · gancho: el barco vikingo ya está aquí; la carabela de Colón asoma al fondo
M.plano(0, 4.3, NORTE, costa([ROT(0, 4.5, "1021", tam=96, x=330, y=1700, capsula="#0d1330d8"),
        ROT(1.4, 4.5, "1492", tam=60, x=870, y=930, capsula="#7a1c14d8", color="#ffffff")]),
        cam(1.0, 1.05, (540, 1150), (520, 1150)), vineta=0.5)

# 2 · el año exacto
M.plano(4.3, 7.95, MADERA, [brillo(540, 1050, 600, "#ffb05a", 0.3), IMG("anillos", ancho=900, x=540, y=1050, z=0.5, anim={"girar": 4})],
        cam(1.0, 1.06, (540, 1050), (540, 1050)), entrada="desenfoque", dur=0.3, vineta=0.65)
M.add({**contador(1.9, 3.7, 1021, "", x=540, y=1050, tam=170, dur=1.4), "miles": False}, CONTEXTO(1.0, 3.6, "AÑO EXACTO"))

# 3 · viaje a Terranova (mapa)
ruta = flecha([(860, 560), (620, 560), (460, 520), (380, 700), (260, 860), (170, 950)], 0.1, 1.9, "#b8352a", 9, disc=[22, 12], z=0.6)
M.plano(7.95, 10.4, ["#8fb3b0", "#5f8c8f"], [BG("mapa_atlantico"), ruta, brillo(150, 960, 120, "#ffd23f", 0.0, 0.6, keys=[{"t": 1.6, "op": 0}, {"t": 2.0, "op": 0.8}]),
        IMG("drakkar", ancho=160, z=0.65, keys=[{"t": 0.1, "x": 860, "y": 540}, {"t": 1.0, "x": 470, "y": 520}, {"t": 1.9, "x": 190, "y": 930}])],
        cam(1.0, 1.08, (540, 900), (420, 900)), entrada="zoom", dur=0.35, vineta=0.45)
M.add(CONTEXTO(1.0, 2.4, "TERRANOVA · CANADÁ"))

# 4 · L'Anse aux Meadows
M.plano(10.4, 13.3, DIA, [BG("bg_terranova"), polvo("#ffffff", 14)], cam(1.0, 1.06, (540, 1100), (500, 1150)), entrada="desenfoque", dur=0.35, vineta=0.4)
M.add(CONTEXTO(1.0, 2.9, "L'ANSE AUX MEADOWS"))
# 5 · restos de casas vikingas
M.plano(13.3, 15.4, DIA, [BG("bg_terranova")], cam(1.6, 1.7, (330, 1200), (360, 1200)), vineta=0.45)
M.add(AMARILLO(0.3, 2.1, "CASAS VIKINGAS", y=1650))

# 6 · madera cortada con herramientas de metal
astillas = {"tipo": "particulas", "clase": "chispas", "color": "#e8c890", "area": [420, 900, 620, 1000], "n": 26, "tam": [4, 9], "vel": [60, -120], "z": 0.7, "semilla": 4}
hacha = IMG("hacha", ancho=300, x=640, y=780, z=0.7, keys=[{"t": 0, "rot": -60}, {"t": 0.5, "rot": 20, "ease": "entrada"}, {"t": 1.0, "rot": -50},
                                                           {"t": 1.5, "rot": 20, "ease": "entrada"}, {"t": 2.0, "rot": -50}, {"t": 2.6, "rot": 20, "ease": "entrada"}])
M.plano(15.4, 18.6, MADERA, [brillo(540, 1000, 600, "#ffb05a", 0.25), IMG("tronco", ancho=1000, x=540, y=1100, z=0.5), hacha, astillas],
        cam(1.0, 1.05, (540, 1000), (540, 1000)), entrada="zoom", dur=0.3, vineta=0.6)
M.add(AMARILLO(2.0, 3.2, "METAL", y=1500))
# 7 · algo que nadie más usaba allí
M.plano(18.6, 21.7, MADERA, [brillo(540, 1000, 600, "#ffb05a", 0.25), IMG("tronco", ancho=1000, x=540, y=1100, z=0.5)],
        cam(1.6, 1.7, (420, 1000), (440, 1010)), vineta=0.6)
M.add(CONTEXTO(0.3, 3.0, "ÚNICO EN AMÉRICA HACIA EL AÑO 1000"))

# 8 · ¿cómo se le pone fecha a un tronco?
M.plano(21.7, 24.5, MADERA, [brillo(540, 1000, 600, "#ffb05a", 0.25), IMG("tronco", ancho=1000, x=540, y=1100, z=0.5)],
        cam(1.0, 1.25, (700, 1080), (860, 1070)), entrada="corte", vineta=0.6)
M.add(AMARILLO(0.5, 2.7, "¿QUÉ AÑO?", y=1550))

# 9 · una tormenta solar
M.plano(24.5, 26.6, ["#1a0a04", "#05020a"], [BG("bg_espacio"), IMG("sol_tormenta", ancho=1000, x=480, y=1050, z=0.5, anim={"girar": 3, "pulso": [0.03, 0.8]})],
        cam(1.0, 1.08, (540, 1050), (560, 1050), temblor=3), entrada="desenfoque", dur=0.3, vineta=0.6)
M.add(AMARILLO(0.3, 2.0, "TORMENTA SOLAR", y=1720))
# 10 · poco antes del año mil: el Sol lanza la tormenta hacia la Tierra
viento = {"tipo": "particulas", "clase": "chispas", "color": "#ffcf5a", "area": [300, 700, 900, 1200], "n": 60, "tam": [3, 8], "vel": [260, 40], "z": 0.6, "semilla": 7}
M.plano(26.6, 30.6, ["#02030a", "#0a1030"], [BG("bg_espacio"), IMG("sol_tormenta", ancho=700, x=150, y=850, z=0.4, anim={"girar": 3}), viento,
        IMG("tierra_hd", ancho=300, x=880, y=1150, z=0.5, anim={"girar": 4}),
        brillo(880, 1150, 220, "#7fffb0", 0.0, 0.55, keys=[{"t": 1.2, "op": 0}, {"t": 2.0, "op": 0.8}, {"t": 4, "op": 0.6}])],
        cam(1.0, 1.05, (540, 1000), (560, 1000)), entrada="corte", vineta=0.55)
M.add(CONTEXTO(0.3, 3.8, "POCO ANTES DEL AÑO 1000"))

# 11 · marca química en los anillos de los árboles de todo el planeta
bosque = [IMG("arbol", ancho=w, x=x, y=y, z=0.5, anim={"balanceo": [1.5, 2 + i * 0.3]}) for i, (x, y, w) in
          enumerate([(150, 1250, 260), (400, 1200, 300), (650, 1230, 280), (900, 1260, 260), (270, 1450, 340), (780, 1470, 340)])]
M.plano(30.6, 32.5, DIA, [BG("bg_terranova"), *bosque, brillo(540, 1250, 600, "#ffd23f", 0.0, 0.6, keys=[{"t": 0.4, "op": 0}, {"t": 1.0, "op": 0.5}])],
        cam(1.0, 1.05, (540, 1200), (540, 1220)), entrada="desenfoque", dur=0.3, vineta=0.45)
M.plano(32.5, 34.9, MADERA, [IMG("anillos", ancho=900, x=540, y=1050, z=0.5, anim={"girar": 3}),
        brillo(540, 1050, 160, "#ff9a1f", 0.7, 0.55, pulso=[0.2, 0.8])], cam(1.0, 1.08, (540, 1050), (540, 1050)), entrada="zoom", dur=0.3, vineta=0.6)
M.add(AMARILLO(0.3, 2.3, "MARCA QUÍMICA", y=1640), CONTEXTO(0.8, 2.4, "EN TODO EL PLANETA"))

# 12 · la encuentran en la madera vikinga (lupa)
M.plano(34.9, 38.2, MADERA, [brillo(540, 1000, 600, "#ffb05a", 0.25), IMG("tronco", ancho=1000, x=540, y=1100, z=0.5),
        IMG("lupa", ancho=420, z=0.7, keys=[{"t": 0, "x": 300, "y": 900}, {"t": 1.6, "x": 880, "y": 1150, "ease": "suave"}])],
        cam(1.0, 1.1, (540, 1050), (700, 1080)), entrada="desenfoque", dur=0.3, vineta=0.6)
M.add(CONTEXTO(0.3, 3.1, "MADERA VIKINGA"))

# 13 · cuentan los anillos de después, uno por año, hasta la corteza
cuenta = flecha([(540 + 125, 1050), (540 + 420, 1050)], 0.6, 3.6, "#ffd23f", 10, z=0.6)
M.plano(38.2, 43.4, MADERA, [IMG("anillos", ancho=900, x=540, y=1050, z=0.5), brillo(540, 1050, 150, "#ff9a1f", 0.6, 0.55, pulso=[0.2, 0.8]), cuenta],
        cam(1.2, 1.35, (700, 1050), (760, 1050)), entrada="corte", vineta=0.6)
M.add(CONTEXTO(1.2, 5.1, "1 ANILLO = 1 AÑO"), AMARILLO(3.8, 5.1, "CORTEZA", y=1560))

# 14 · resultado: talados en 1021
cae = IMG("arbol", ancho=420, x=560, y=1180, z=0.55, keys=[{"t": 0, "rot": 0}, {"t": 0.6, "rot": 0}, {"t": 1.6, "rot": -82, "ease": "entrada"}])
M.plano(43.4, 47.3, DIA, [BG("bg_terranova"), cae, {"tipo": "particulas", "clase": "polvo", "color": "#c9b48c", "area": [200, 1300, 900, 1450],
        "n": 30, "tam": [4, 10], "vel": [0, -40], "z": 0.6, "semilla": 9}], cam(1.0, 1.06, (540, 1150), (520, 1180)), entrada="desenfoque", dur=0.3, vineta=0.45)
M.add(ROT(2.0, 3.9, "1021", tam=170, x=540, y=1600))

# 15 · 471 años antes de que llegara Colón
M.plano(47.3, 50.84, NORTE, [BG("bg_mar_norte"), olas, IMG("carabela", ancho=700, y=1360, z=0.6, anim={"balanceo": [2, 2.4], "flotar": [8, 2.4]},
        keys=[{"t": 0, "x": 1300}, {"t": 3.4, "x": 640, "ease": "salida"}])], cam(1.0, 1.05, (540, 1150), (540, 1150)), entrada="desenfoque", dur=0.3, vineta=0.5)
M.add({**contador(0.2, 3.5, 471, "AÑOS ANTES", x=540, y=820, tam=120, dur=1.2), "miles": False}, CONTEXTO(1.8, 3.5, "COLÓN · 1492"))

# 16 · «Y lo dejó escrito un árbol» → bucle con el plano del principio
M.plano(50.84, 52.1, MADERA, [IMG("anillos", ancho=900, x=540, y=1050, z=0.5, anim={"girar": 3}), brillo(540, 1050, 160, "#ff9a1f", 0.7, 0.55, pulso=[0.2, 0.6])],
        cam(1.1, 1.0, (540, 1050), (540, 1050)), entrada="corte", vineta=0.6)
M.plano(52.1, 53.46, NORTE, costa(t=1.4), cam(1.05, 1.0, (520, 1150), (540, 1150)), entrada="desenfoque", dur=0.3, vineta=0.5)

M.guardar("03", "vikingos-america-1021", 53.46,
          ["Colón", "vikingos", "América", "veintiuno", "Terranova", "metal", "tormenta", "solar", "anillos", "corteza", "árbol"],
          {"generar": "misterio", "semilla": 13})
