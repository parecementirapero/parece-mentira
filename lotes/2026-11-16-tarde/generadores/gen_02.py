"""02 — Cruzar una puerta te hace olvidar (Radvansky, 2011). Uso: python3 gen_02.py DIR_SALIDA DIR_AUDIO"""
import sys
from base import IMG, BG, ROT, AMARILLO, CONTEXTO, polvo, brillo, cam, Montaje

M = Montaje(sys.argv[1])
NOCHE = ["#1a2036", "#0c1020"]
CREMA = ["#e8dcc8", "#b8a888"]


def persona(x, y, ancho=360, nombre="persona_casa", **kw):
    return IMG(nombre, ancho=ancho, x=x, y=y, z=0.6, **kw)


def bocadillo(nombre, x, y, ancho=320, **kw):
    return IMG(nombre, ancho=ancho, x=x, y=y, z=0.7, anim={"flotar": [10, 1.6]}, **kw)


# 1 · gancho: en el umbral, la idea (las llaves) se borra y queda la duda
M.plano(0, 1.6, NOCHE, [BG("bg_pasillo"), persona(540, 1380, 420, anim={"balanceo": [1.5, 1.2]}),
        bocadillo("bocadillo_llaves", 800, 760, keys=[{"t": 0, "op": 1}, {"t": 0.9, "op": 1}, {"t": 1.3, "op": 0}]),
        bocadillo("bocadillo_duda", 800, 760, keys=[{"t": 0, "op": 0}, {"t": 1.0, "op": 0}, {"t": 1.4, "op": 1}])],
        cam(1.0, 1.05, (540, 1100), (540, 1080)), vineta=0.6)
M.fx(1.1, "fugaz", -18)
# 2 · primer plano de la cara
M.plano(1.6, 3.3, NOCHE, [BG("bg_pasillo"), persona(540, 1380, 420), bocadillo("bocadillo_duda", 800, 760)],
        cam(1.8, 1.9, (560, 1000), (580, 960)), vineta=0.65)
M.add(ROT(0.2, 1.6, "?", tam=160, color="#ffd23f", capsula=None, x=280, y=1450, anim={"flotar": [8, 1.0]}))
# 3 · la culpa puede ser de la puerta
M.plano(3.3, 5.7, CREMA, [BG("puerta_cerca"), IMG("hoja_puerta", ancho=700, x=540, y=1040, z=0.4, keys=[{"t": 0, "ex": 0.35, "x": 312}, {"t": 2.2, "ex": 0.25, "x": 277}]),
        {"tipo": "flecha", "puntos": [[900, 1650], [440, 1250]], "grosor": 16, "color": "#e8402f", "contorno": "#00000055", "z": 0.6,
         "keys": [{"t": 0.3, "progreso": 0}, {"t": 0.9, "progreso": 1}]}],
        cam(1.0, 1.06, (540, 1040), (540, 1000)), entrada="desenfoque", dur=0.3, vineta=0.5)
M.add(AMARILLO(0.6, 2.3, "LA PUERTA", y=1720))
M.fx(3.35, "whoosh", -16)

# 4 · 2011, Universidad de Notre Dame
M.plano(5.7, 8.9, ["#2a4a8a", "#ffd8a0"], [BG("bg_universidad"), polvo("#fff6d8", 20)], cam(1.0, 1.06, (540, 1000), (540, 960)),
        entrada="zoom", dur=0.35, vineta=0.45)
M.add(CONTEXTO(0.1, 3.1, "2011 · NOTRE DAME · EE. UU."))
M.plano(8.9, 12.2, ["#2a4a8a", "#ffd8a0"], [BG("bg_universidad")], cam(1.6, 1.7, (540, 640), (540, 620)), vineta=0.5)
M.add(CONTEXTO(0.1, 2.0, "PSICÓLOGO G. RADVANSKY"), AMARILLO(2.4, 3.3, "EXPERIMENTO", y=1700))

# 5 · llevar objetos de una mesa a otra (vista desde arriba, sin puerta)
PL = ["#2a2a33", "#141418"]


def caja_que_viaja(t0, t1, x0=540, y0=600, x1=540, y1=1300):
    return {"tipo": "forma", "forma": "redondeado", "ancho": 70, "alto": 60, "esquinas": 8, "relleno": "#3a8ad0", "borde": "#1f4e80",
            "grosor": 5, "z": 0.62, "keys": [{"t": 0, "x": x0, "y": y0}, {"t": t0, "x": x0, "y": y0}, {"t": t1, "x": x1, "y": y1, "ease": "suave"}]}


def caminante(t0, t1, x0=540, y0=660, x1=540, y1=1240, color="#3fa0a8"):
    return {"tipo": "forma", "forma": "circulo", "radio": 34, "relleno": color, "borde": "#ffffff", "grosor": 6, "z": 0.6,
            "keys": [{"t": 0, "x": x0, "y": y0}, {"t": t0, "x": x0, "y": y0}, {"t": t1, "x": x1, "y": y1, "ease": "suave"}], "anim": {"pulso": [0.06, 0.35]}}


M.plano(12.2, 16.45, PL, [IMG("planta_sin", ancho=900, x=540, y=960, z=0.4), caminante(0.8, 3.6), caja_que_viaja(0.8, 3.6, y0=600, y1=1180)],
        cam(1.0, 1.04, (540, 960), (540, 960)), entrada="desenfoque", dur=0.3, vineta=0.6)
M.add(ROT(0.2, 4.0, "DE UNA MESA A OTRA", tam=56, color="#ffffff", capsula="#0d1330d8", x=540, y=1640))
M.fx(12.25, "whoosh", -16)
# 6 · unos cruzaban una puerta
M.plano(16.45, 18.4, PL, [IMG("planta_puerta", ancho=900, x=540, y=960, z=0.4), caminante(0.1, 1.8), caja_que_viaja(0.1, 1.8, y0=600, y1=1180),
        brillo(540, 960, 160, "#ffd23f", 0.6, 0.5, pulso=[0.2, 0.5])], cam(1.0, 1.04, (540, 960), (540, 960)), vineta=0.6)
M.add(ROT(0.1, 1.9, "CON PUERTA", tam=64, color="#ffffff", capsula="#c0392be6", x=540, y=1640))
M.fx(17.3, "golpe", -20)
# 7 · otros, la misma distancia sin puerta
M.plano(18.4, 22.15, PL, [IMG("planta_sin", ancho=900, x=540, y=960, z=0.4), caminante(0.2, 2.4), caja_que_viaja(0.2, 2.4, y0=600, y1=1180),
        {"tipo": "flecha", "puntos": [[780, 640], [780, 1280]], "grosor": 8, "color": "#ffffff", "discontinua": [20, 14], "z": 0.55,
         "keys": [{"t": 0.2, "progreso": 0}, {"t": 2.4, "progreso": 1}]}], cam(1.0, 1.04, (540, 960), (540, 960)), vineta=0.6)
M.add(ROT(0.1, 3.6, "SIN PUERTA", tam=64, color="#ffffff", capsula="#1f6e3ae6", x=540, y=1640))

# 8 · los que cruzaban la puerta olvidaban más
def barra(x, prog, color, t0):
    return {"tipo": "barra", "x": x, "y": 1050, "ancho": 220, "alto": 620, "vertical": True, "color": color, "fondo": "#ffffff14", "z": 0.5,
            "keys": [{"t": t0, "progreso": 0}, {"t": t0 + 1.2, "progreso": prog, "ease": "salida"}]}


M.plano(22.15, 25.05, ["#1a2036", "#0c1020"], [barra(340, 0.85, "#e8402f", 0.2), barra(740, 0.45, "#3ddc6e", 0.4),
        ROT(0.1, 2.9, "CON PUERTA", tam=46, color="#ffffff", capsula="#0d1330d8", x=340, y=1440),
        ROT(0.1, 2.9, "SIN PUERTA", tam=46, color="#ffffff", capsula="#0d1330d8", x=740, y=1440)],
        cam(1.0, 1.03, (540, 1000), (540, 1000)), entrada="desenfoque", dur=0.3, vineta=0.6)
M.add(AMARILLO(1.4, 2.9, "OLVIDAN MÁS", y=1680))
M.fx(22.3, "trazo", -18)

# 9 · lo repitió en habitaciones de verdad: alguien cruza con una caja
M.plano(25.05, 28.25, NOCHE, [BG("bg_pasillo"), persona(540, 1650, 520, nombre="persona_casa", anim={"balanceo": [3, 0.6]},
        keys=[{"t": 0, "y": 1750, "escala": 1.15}, {"t": 3.0, "y": 1360, "escala": 0.62, "ease": "suave"}]),
        {"tipo": "forma", "forma": "redondeado", "ancho": 170, "alto": 130, "esquinas": 10, "relleno": "#c08a5a", "borde": "#7a4e2c", "grosor": 6, "z": 0.65,
         "keys": [{"t": 0, "x": 540, "y": 1560, "escala": 1.15}, {"t": 3.0, "x": 540, "y": 1310, "escala": 0.62, "ease": "suave"}]}],
        cam(1.0, 1.06, (540, 1150), (540, 1080)), entrada="zoom", dur=0.35, vineta=0.6)
M.add(AMARILLO(0.4, 3.0, "EN LA VIDA REAL", y=1780))

# 10 · ¿por qué?
M.plano(28.25, 29.15, ["#2a1430", "#120814"], [brillo(540, 960, 500, "#ff8ab0", 0.35), IMG("cerebro", ancho=760, x=540, y=1050, z=0.5,
        anim={"pulso": [0.03, 0.8]})], cam(1.1, 1.0, (540, 1000), (540, 1000)), entrada="desenfoque", dur=0.25, vineta=0.65)
M.add(ROT(0.0, 0.9, "¿POR QUÉ?", tam=96, color="#ffd23f", capsula=None, rot=-6, x=540, y=1650))
M.fx(28.3, "pop", -16)
# 11 · no es una película continua
M.plano(29.15, 32.55, ["#2a1430", "#120814"], [brillo(540, 800, 500, "#ff8ab0", 0.3), IMG("cerebro", ancho=520, x=540, y=760, z=0.5, anim={"pulso": [0.03, 0.8]}),
        IMG("pelicula", ancho=2400, y=1400, z=0.6, keys=[{"t": 0, "x": 1500}, {"t": 3.4, "x": -100}])],
        cam(1.0, 1.04, (540, 1050), (540, 1050)), vineta=0.6)
M.add(AMARILLO(1.6, 3.4, "PELÍCULA", y=1720))
# 12 · lo corta en escenas
cortes = [{"tipo": "forma", "forma": "rect", "ancho": 12, "alto": 420, "relleno": "#ffffff", "x": x, "y": 1400, "z": 0.65,
           "keys": [{"t": 0, "op": 0}, {"t": 0.25 + i * 0.25, "op": 0}, {"t": 0.3 + i * 0.25, "op": 1}]} for i, x in enumerate((262, 558, 854))]
M.plano(32.55, 34.15, ["#2a1430", "#120814"], [IMG("cerebro", ancho=520, x=540, y=760, z=0.5),
        IMG("pelicula", ancho=2400, x=1100, y=1400, z=0.6, keys=[{"t": 0, "x": 1120}, {"t": 1.6, "x": 1100}]), *cortes],
        cam(1.0, 1.0, (540, 1050), (540, 1050)), vineta=0.6)
M.add(AMARILLO(0.3, 1.6, "ESCENAS", y=1720))
for i in range(3):
    M.fx(32.85 + i * 0.25, "tic", -14)

# 13 · una puerta es un corte perfecto (la puerta se cierra)
M.plano(34.15, 36.65, CREMA, [BG("puerta_cerca"), IMG("hoja_puerta", ancho=700, x=540, y=1040, z=0.4,
        keys=[{"t": 0, "ex": 0.2, "x": 260}, {"t": 0.9, "ex": 0.2, "x": 260}, {"t": 1.4, "ex": 1.0, "x": 540, "ease": "entrada"}])],
        cam(1.0, 1.05, (540, 1040), (540, 1040), temblor=0), entrada="zoom", dur=0.35, vineta=0.5)
M.add(AMARILLO(1.5, 2.5, "CORTE", y=1720))
M.fx(35.55, "golpe", -10)

# 14 · al cruzarla, cierra el capítulo y lo archiva
M.plano(36.65, 40.95, ["#2a2f3a", "#121620"], [brillo(540, 900, 600, "#cfe0ff", 0.25), IMG("archivador", ancho=600, x=540, y=1250, z=0.5),
        IMG("carpeta", ancho=300, x=540, z=0.6, keys=[{"t": 0, "y": 500, "rot": -10, "op": 1}, {"t": 1.2, "y": 520, "rot": -6}, {"t": 2.7, "op": 1},
                                                      {"t": 2.6, "y": 860, "rot": 0, "escala": 0.7, "ease": "entrada"}, {"t": 2.9, "op": 0}])],
        cam(1.0, 1.05, (540, 1000), (540, 1050)), entrada="desenfoque", dur=0.3, vineta=0.6)
M.add(AMARILLO(2.8, 4.2, "ARCHIVADO", y=1780))
M.fx(39.5, "golpe", -16)
# 15 · lo que ibas a hacer se queda dentro
M.plano(40.95, 43.65, ["#2a2f3a", "#121620"], [IMG("archivador", ancho=600, x=540, y=1250, z=0.5),
        IMG("bocadillo_llaves", ancho=320, x=540, z=0.6, keys=[{"t": 0, "y": 520, "escala": 1, "op": 1}, {"t": 1.0, "y": 560}, {"t": 2.0, "op": 1},
                                                               {"t": 2.0, "y": 880, "escala": 0.3, "ease": "entrada"}, {"t": 2.2, "op": 0}])],
        cam(1.2, 1.3, (540, 900), (540, 920)), vineta=0.6)
M.fx(43.0, "golpe", -18)

# 16 · lo más raro: volver no ayudaba
M.plano(43.65, 46.1, NOCHE, [BG("bg_pasillo"), persona(540, 1360, 400, nombre="persona_casa_izq", anim={"balanceo": [3, 0.6]},
        keys=[{"t": 0, "x": 540, "y": 1400, "escala": 0.7}, {"t": 2.4, "x": 540, "y": 1600, "escala": 1.1, "ease": "suave"}])],
        cam(1.0, 1.04, (540, 1100), (540, 1100)), entrada="zoom", dur=0.35, vineta=0.6)
M.add(AMARILLO(0.2, 2.3, "LO MÁS RARO", y=1780))
M.plano(46.1, 49.4, NOCHE, [BG("bg_pasillo"), persona(540, 1600, 440, nombre="persona_casa_izq", anim={"balanceo": [1.5, 1.2]}),
        bocadillo("bocadillo_duda", 820, 900)], cam(1.0, 1.04, (540, 1200), (540, 1180)), vineta=0.6)
M.add(ROT(0.2, 3.2, "VOLVER", tam=72, color="#ffffff", capsula="#0d1330d8", x=540, y=500), AMARILLO(1.2, 3.2, "NO AYUDA", y=1780))

# 17 · no culpes a tu memoria
M.plano(49.4, 52.6, ["#2a1430", "#120814"], [brillo(540, 960, 500, "#ff8ab0", 0.35), IMG("cerebro", ancho=760, x=540, y=1050, z=0.5,
        anim={"balanceo": [3, 1.4]})], cam(1.0, 1.05, (540, 1050), (540, 1030)), entrada="desenfoque", dur=0.3, vineta=0.65)
M.add(ROT(0.6, 3.1, "INOCENTE", tam=80, color="#ffffff", capsula="#1f6e3ae6", x=540, y=1600, rot=-4))
M.fx(50.0, "ding", -16)
# 18 · bucle: culpa a la puerta
M.plano(52.6, 54.74, NOCHE, [BG("bg_pasillo"), persona(540, 1380, 420), bocadillo("bocadillo_duda", 800, 760)],
        cam(1.6, 1.0, (540, 1000), (540, 1100)), entrada="zoom", dur=0.35, vineta=0.6)
M.add(ROT(0.5, 2.1, "CULPABLE", tam=80, color="#ffffff", capsula="#c0392be6", x=540, y=500, rot=-4))

M.guardar("02", "puertas-olvidar", 54.74, ["puerta", "Radvansky", "experimento", "olvidaban", "cerebro", "película", "escenas", "corte",
                                            "capítulo", "archiva", "memoria"],
          {"generar": "curiosidad", "semilla": 21}, audio_dir=sys.argv[2])
