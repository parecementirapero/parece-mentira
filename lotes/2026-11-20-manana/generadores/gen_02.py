"""02 · Un Fórmula Uno podría ir por el techo — método denso. Lote 2026-11-20-manana (Agente 08:00, Nico). Tendencia del día: «gran premio de las vegas».
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]
Coches genéricos dibujados aquí: sin equipos, patrocinadores, números ni pilotos reales."""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_1120m  # noqa: E402

SVG = ilus_1120m.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

TUN = ["#1a2232", "#0a0e18"]
NOCHE = ["#1a0a3a", "#121218"]
OSC = ["#0a1a2a", "#020610"]
CIELO = ["#5aa0d8", "#a8d4ee"]


def tunel(): return BG("bg_tunel")
def pista(): return BG("bg_pista_noche")
def estudio(): return BG("bg_estudio")


def coche(n="f1", ancho=900, x=540, y=1500, z=0.5, keys=None, **k):
    """Lienzo 1200×380 → con ancho 900 mide 285 de alto; ruedas abajo en y+≈100."""
    return IMG(n, ancho=ancho, x=x, y=y, z=z, keys=keys or [], **k)


def techo(keys, ancho=900):
    """El coche boca abajo pegado al techo del túnel (rot 180: las ruedas tocan arriba)."""
    return coche(ancho=ancho, keys=keys)


def aire_abajo(x0, x1, y0, y1, t0, n=5, color=CIAN, sep=0.08):
    """Flechas de aire que bajan y empujan hacia el suelo."""
    paso = (x1 - x0) / max(1, n - 1)
    return [flecha([[x0 + i * paso, y0], [x0 + i * paso, y1]], t0 + i * sep, t0 + i * sep + 0.35, color, 8, z=0.6) for i in range(n)]


def chispas(x, y, sem=1): return polvo("#ffd060", 24, (x - 200, y - 20, x + 200, y + 30), sem)


# ================================================================== PLANOS
@v.plano(0, "gancho: el monoplaza va boca abajo pegado al techo del túnel")
def _(d):
    return P(TUN, [tunel(), techo([{"t": 0, "x": 900, "y": 680, "rot": 180, "escala": 0.94}, {"t": 0.4, "x": 640, "y": 640, "rot": 180, "escala": 1.0, "ease": "elastico"},
                                   {"t": d, "x": 420, "y": 640, "rot": 180, "escala": 1.06, "ease": "suave"}], 980),
                   *lineas_vel(1000, 520, 1, "#fff4c8cc"), chispas(560, 520, 2)],
             cam(1.0, 1.08, (540, 800)), vineta=0.6, sfx=[(0.02, "whoosh", -12, {"dur": 0.6}), (0.4, "zap", -20)])


@v.plano(5, "un Fórmula Uno: entra en la pista de noche")
def _(d):
    return P(NOCHE, [pista(), coche(keys=arranque(540, 1500, d, "derecha", 400, 60)), *lineas_vel(220, 1500, 2, "#ffffffaa")],
             cam(1.0, 1.05, (540, 1300)), "corte", sfx=[(0.05, "whoosh", -16, {"dur": 0.5})])


@v.plano(7, "micro: «Uno», el morro del coche de muy cerca")
def _(d):
    return P(NOCHE, [pista(), coche(ancho=2000, x=200, y=1450, keys=[{"t": 0, "x": 260}, {"t": d, "x": 140}]), *lineas_vel(900, 1450, 9, "#ffffffaa")],
             cam(1.0, 1.06, (540, 1400)), "corte", sfx=[(0.02, "zap", -22)])


@v.plano(8, "boca abajo: el coche da la vuelta en el aire")
def _(d):
    return P(OSC, [estudio(), coche(y=1100, keys=[{"t": 0, "rot": 0}, {"t": d * 0.8, "rot": 180, "ease": "suave"}]), brillo(540, 1100, 500, "#2ff3ff", 0.25, 0.06)],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[amarillo(0.03, d - 0.02, "BOCA ABAJO", y=560, tam=120, color=CIAN)], sfx=[(0.1, "roce", -18)])


@v.plano(10, "sin caerse: sigue pegado al techo y la flecha de caída se tacha")
def _(d):
    return P(TUN, [tunel(), techo([{"t": 0, "x": 640, "y": 640, "rot": 180}, {"t": d, "x": 460, "y": 640, "rot": 180}]),
                   flecha([[540, 760], [540, 1180]], 0.05, 0.4, "#ffffffcc", 8, z=0.6),
                   flecha([[440, 880], [640, 1080]], 0.45, 0.6, "#ff3d3d", 14, punta=False, z=0.7), flecha([[640, 880], [440, 1080]], 0.55, 0.7, "#ff3d3d", 14, punta=False, z=0.7)],
             cam(1.0, 1.05, (540, 900)), "corte", hud=[amarillo(0.1, d - 0.03, "SIN CAERSE", y=1350, tam=110, color=LIMA)], sfx=[(0.5, "zap", -20)])


@v.plano(12, "¿cómo? la lupa recorre el coche")
def _(d):
    return P(OSC, [estudio(), coche(y=1250), IMG("lupa", ancho=340, z=0.7, keys=[{"t": 0, "x": 300, "y": 1150}, {"t": d, "x": 820, "y": 1200, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1200)), "corte", hud=[amarillo(0.05, d - 0.03, "¿CÓMO?", y=560, tam=130, color=CIAN)], sfx=[(0.1, "roce", -20)])


@v.plano(13, "micro: «por sus», el coche gira hacia la cámara")
def _(d):
    return P(OSC, [estudio(), coche(ancho=1000, y=1250, keys=[{"t": 0, "ex": 0.6}, {"t": d, "ex": 1.0, "ease": "salida"}])], cam(1.0, 1.06, (540, 1200)), "corte", sfx=[(0.02, "roce", -20)])


@v.plano(15, "por sus alerones: anillos en el alerón trasero y en el delantero")
def _(d):
    return P(OSC, [estudio(), coche(ancho=1000, y=1250, keys=late(0.1, 1, 0.05)), senala(185, 1100, 0.05, d - 0.1, 100, MAGENTA), senala(985, 1335, d * 0.4, d - 0.1, 90, MAGENTA)],
             cam(1.0, 1.04, (540, 1200)), "corte", hud=[rotulo(0.1, d - 0.05, "ALERONES", tam=110, color="#ffffff", capsula="#c0397ae6", y=560)], sfx=[(0.05, "pop", -18), (d * 0.4, "pop", -18)])


@v.plano(16, "funcionan como las alas de un avión: el avión cruza el cielo")
def _(d):
    return P(CIELO, [BG("bg_sabana_dia"), IMG("avion", ancho=900, z=0.5, keys=[{"t": 0, "x": 200, "y": 900, "rot": -6}, {"t": d, "x": 800, "y": 760, "rot": -8, "ease": "lineal"}])],
             cam(1.0, 1.05, (540, 900)), "desenfoque", sfx=[(0.05, "rumor", -18, {"dur": min(2.0, d)})])


@v.plano(19, "alas: el perfil del ala con el aire empujándola hacia arriba")
def _(d):
    return P(CIELO, [BG("bg_sabana_dia"), IMG("perfil_ala", ancho=860, x=540, y=1100, z=0.5, keys=[{"t": 0, "y": 1150}, {"t": d, "y": 1060, "ease": "suave"}]),
                     *[flecha([[300 + i * 160, 1400], [300 + i * 160, 1230]], 0.05 + i * 0.08, 0.4 + i * 0.08, LIMA, 9, z=0.6) for i in range(4)]],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[rotulo(0.1, d - 0.05, "SUBE", tam=120, color="#141414", capsula="#b8ff3ae6", y=560)], sfx=[(0.1, "roce", -20)])


@v.plano(23, "pero puestas al revés: el ala gira y se convierte en alerón")
def _(d):
    t = d * 0.55
    return P(OSC, [estudio(), IMG("perfil_ala", ancho=860, x=540, y=1100, z=0.5, keys=[{"t": 0, "rot": 0, "op": 1}, {"t": t, "rot": 180, "op": 1, "ease": "suave"}, {"t": t + 0.01, "op": 0}]),
                   IMG("perfil_aleron", ancho=860, x=540, y=1100, z=0.51, keys=[{"t": 0, "op": 0}, {"t": t, "op": 0}, {"t": t + 0.01, "op": 1}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[amarillo(0.1, d - 0.03, "AL REVÉS", y=560, tam=120, color=MAGENTA)], sfx=[(0.1, "whoosh", -20, {"dur": 0.4})])


@v.plano(31, "micro: «el aire», solo las flechas de aire cayendo sobre la ciudad")
def _(d):
    return P(NOCHE, [pista(), *aire_abajo(160, 920, 700, 1300, 0.0, 6, CIAN, 0.04)], cam(1.0, 1.08, (540, 1000)), "corte", sfx=[(0.02, "whoosh", -20, {"dur": 0.3})])


@v.plano(34, "el aire lo aplasta contra el suelo: flechas de aire caen sobre el coche, que se aplasta")
def _(d):
    return P(NOCHE, [pista(), coche(y=1500, keys=[{"t": 0, "ey": 1.0}, {"t": 0.6, "ey": 0.93, "ease": "salida"}, {"t": d, "ey": 0.95}]),
                     *aire_abajo(220, 860, 900, 1320, 0.05, 5), chispas(540, 1610, 3)],
             cam(1.0, 1.05, (540, 1300)), "corte", hud=[amarillo(0.2, d - 0.03, "LO APLASTA", y=560, tam=120, color=CIAN)], sfx=[(0.3, "golpe", -16)])


@v.plano(38, "eso se llama carga aerodinámica: rótulo y el coche con las flechas")
def _(d):
    return P(NOCHE, [pista(), coche(y=1500, keys=[{"t": 0, "x": 520}, {"t": d, "x": 560}]), *aire_abajo(220, 860, 1000, 1330, 0.05, 5, AMBAR)],
             cam(1.0, 1.04, (540, 1300)), "corte", hud=[rotulo(0.1, d - 0.05, "CARGA AERODINÁMICA", tam=82, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "ding", -22)])


@v.plano(43, "y crece muchísimo con la velocidad: la aguja del velocímetro sube")
def _(d):
    return P(OSC, [estudio(), brillo(540, 1250, 500, "#2ff3ff", 0.25, 0.06), IMG("velocimetro", ancho=800, x=540, y=1100, z=0.5),
                   IMG("aguja_vel", ancho=640, x=540, y=1300, z=0.55, keys=[{"t": 0, "rot": -180}, {"t": d * 0.8, "rot": -40, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[amarillo(0.2, d - 0.03, "CRECE", y=560, tam=120, color=LIMA)], sfx=[(0.05, "subida", -18, {"dur": min(1.5, d)})])


@v.plano(49, "si vas el doble de rápido: el coche cruza a toda velocidad")
def _(d):
    return P(NOCHE, [pista(), coche(y=1500, keys=[{"t": 0, "x": -300}, {"t": d * 0.7, "x": 1400, "ease": "lineal"}]), *lineas_vel(540, 1500, 4, "#ffffffaa")],
             cam(1.0, 1.04, (540, 1300)), "corte", hud=[rotulo(0.05, d - 0.05, "× 2 VELOCIDAD", tam=104, color="#141414", capsula="#2ff3ffe6", y=560)], sfx=[(0.05, "whoosh", -14, {"dur": 0.6})])


@v.plano(55, "micro: «empuja», una flecha gorda golpea el coche")
def _(d):
    return P(NOCHE, [pista(), coche(y=1530, keys=[{"t": 0, "ey": 1.0}, {"t": 0.2, "ey": 0.9, "ease": "salida"}, {"t": d, "ey": 0.96}]), flecha([[540, 800], [540, 1360]], 0.0, 0.25, MAGENTA, 22, z=0.6)],
             cam(1.15, 1.2, (540, 1350)), "corte", sfx=[(0.15, "golpe", -16)])


@v.plano(56, "empuja cuatro veces más: cuatro flechas gordas caen una a una")
def _(d):
    return P(NOCHE, [pista(), coche(y=1530), *[flecha([[240 + i * 200, 820], [240 + i * 200, 1340]], 0.05 + i * 0.18, 0.4 + i * 0.18, MAGENTA, 16, z=0.6) for i in range(4)]],
             cam(1.0, 1.04, (540, 1250)), "corte", hud=[rotulo(0.1, d - 0.05, "× 4", tam=170, color="#141414", capsula="#ff3df2e6", y=560)],
             sfx=[(0.3, "golpe", -20), (0.48, "golpe", -20), (0.66, "golpe", -20), (0.84, "golpe", -18)])


@v.plano(59, "¿y cuándo basta para colgarse? el coche en el túnel, mirando al techo")
def _(d):
    return P(TUN, [tunel(), coche(y=1450, keys=[{"t": 0, "x": 380}, {"t": d, "x": 560, "ease": "suave"}]), flecha([[540, 1250], [540, 700]], 0.2, d * 0.7, "#ffffff99", 6, disc=[22, 16], z=0.6)],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[amarillo(0.1, d - 0.03, "¿CUÁNDO?", y=560, tam=130, color=AMBAR)], sfx=[(0.1, "roce", -20)])


@v.plano(64, "micro: «a unos», el coche pasa como un rayo")
def _(d):
    return P(NOCHE, [pista(), coche(y=1500, keys=[{"t": 0, "x": 1300}, {"t": d, "x": -200, "ease": "lineal"}]), *lineas_vel(900, 1500, 10, "#ffffffaa")],
             cam(1.0, 1.04, (540, 1350)), "corte", sfx=[(0.02, "whoosh", -16, {"dur": 0.4})])


@v.plano(66, "a unos doscientos kilómetros por hora: la aguja llega a 200 y la cifra corre")
def _(d):
    return P(OSC, [estudio(), brillo(540, 1250, 500, "#ff3d3d", 0.25, 0.06), IMG("velocimetro", ancho=800, x=540, y=1100, z=0.5),
                   IMG("aguja_vel", ancho=640, x=540, y=1300, z=0.55, keys=[{"t": 0, "rot": -180}, {"t": d * 0.6, "rot": -60, "ease": "salida"}, {"t": d, "rot": -58}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[contador(0.05, d - 0.03, 0, 200, d * 0.6, " KM/H", y=1520, tam=110, color="#ffd23f")],
             sfx=[(0.05, "subida", -18, {"dur": min(1.2, d * 0.6)}), (d * 0.6, "impacto", -16)])


@v.plano(70, "esa fuerza ya es igual al peso del coche: dos flechas iguales, una de aire y otra de peso")
def _(d):
    return P(OSC, [estudio(), coche(y=1150), flecha([[330, 700], [330, 1020]], 0.05, 0.5, CIAN, 16, z=0.6), flecha([[750, 1280], [750, 1600]], 0.3, 0.75, AMBAR, 16, z=0.6)],
             cam(1.0, 1.04, (540, 1150)), "corte", hud=[rotulo(0.2, d - 0.05, "AIRE = PESO", tam=120, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "pop", -18), (0.4, "pop", -18)])


@v.plano(79, "a partir de ahí, en teoría: el coche corre por el suelo del túnel")
def _(d):
    return P(TUN, [tunel(), coche(y=1450, keys=[{"t": 0, "x": 760}, {"t": d, "x": 460, "ease": "lineal"}]), *lineas_vel(1060, 1450, 5, "#fff4c8aa")],
             cam(1.0, 1.05, (540, 1200)), "corte", hud=[rotulo(0.3, d - 0.05, "EN TEORÍA", tam=104, color="#141414", capsula="#2ff3ffe6", y=560)], sfx=[(0.05, "rumor", -20, {"dur": min(1.6, d)})])


@v.plano(85, "podrías darle la vuelta: sube girando del suelo al techo")
def _(d):
    return P(TUN, [tunel(), coche(keys=[{"t": 0, "x": 460, "y": 1450, "rot": 0}, {"t": d * 0.85, "x": 560, "y": 640, "rot": 180, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1000)), "corte", sfx=[(0.05, "whoosh", -16, {"dur": 0.7}), (d * 0.85, "golpe", -16)])


@v.plano(89, "y seguiría pegado arriba: boca abajo en el techo, con las flechas del aire empujándolo hacia arriba")
def _(d):
    return P(TUN, [tunel(), techo([{"t": 0, "x": 560, "y": 640, "rot": 180}, {"t": d, "x": 420, "y": 640, "rot": 180}]),
                   *[flecha([[300 + i * 160, 1120], [300 + i * 160, 840]], 0.05 + i * 0.08, 0.4 + i * 0.08, CIAN, 9, z=0.6) for i in range(4)], chispas(500, 520, 6)],
             cam(1.0, 1.05, (540, 800)), "corte", hud=[amarillo(0.2, d - 0.03, "PEGADO ARRIBA", y=1350, tam=110, color=LIMA)], sfx=[(0.1, "zap", -22)])


@v.plano(93, "¿lo ha hecho alguien? la lupa sobre el túnel vacío")
def _(d):
    return P(TUN, [tunel(), IMG("lupa", ancho=380, z=0.7, keys=[{"t": 0, "x": 380, "y": 900}, {"t": d, "x": 700, "y": 1100, "ease": "suave"}])],
             cam(1.0, 1.08, (540, 960)), "corte", hud=[amarillo(0.05, d - 0.03, "¿ALGUIEN?", y=560, tam=130, color=CIAN)], sfx=[(0.1, "roce", -20)])


@v.plano(97, "no: un NO enorme cae con un golpe")
def _(d):
    return P(TUN, [tunel(), coche(y=1450)],
             cam(1.0, 1.05, (540, 1200)), "corte", hud=[rotulo(0.0, d - 0.03, "NO", tam=220, color="#ffffff", capsula="#c0392be6", y=760)], sfx=[(0.02, "golpe", -12)])


@v.plano(98, "el motor no está pensado para ir boca abajo: el motor se da la vuelta y gotea aceite")
def _(d):
    return P(OSC, [estudio(), IMG("motor_bloque", ancho=700, x=540, y=1100, z=0.5, keys=[{"t": 0, "rot": 0}, {"t": d * 0.4, "rot": 180, "ease": "suave"}, {"t": d, "rot": 186}]),
                   IMG("gota_roja", ancho=90, x=540, z=0.55, keys=[{"t": 0, "op": 0, "y": 820}, {"t": d * 0.5, "op": 1, "y": 820}, {"t": d, "y": 1500, "ease": "entrada"}], ),
                   brillo(540, 1100, 500, "#ffb050", 0.2, 0.06)],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[rotulo(0.2, d - 0.05, "MOTOR", tam=110, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(d * 0.4, "golpe", -18), (d * 0.9, "burbuja", -18)])


@v.plano(107, "y haría falta un túnel recto de cuatro o cinco kilómetros: la cámara viaja por el túnel")
def _(d):
    return P(TUN, [tunel(), brillo(540, 960, 300, "#ffe8b0", 0.4, 0.07, pulso=[0.1, 1.2])],
             cam(1.0, 1.8, (540, 960)), "corte", hud=[rotulo(0.3, d - 0.05, "4–5 KM RECTOS", tam=104, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "rumor", -18, {"dur": min(2.5, d)})])


@v.plano(118, "pero los números dicen que sí: el SÍ late sobre el coche del techo")
def _(d):
    return P(TUN, [tunel(), techo([{"t": 0, "x": 640, "y": 640, "rot": 180}, {"t": d, "x": 440, "y": 640, "rot": 180}])],
             cam(1.0, 1.05, (540, 800)), "corte", hud=[rotulo(0.15, d - 0.05, "LOS NÚMEROS: SÍ", tam=104, color="#141414", capsula="#b8ff3ae6", y=1300)], sfx=[(0.15, "ding", -18)])


@v.plano(124, "¿y para qué sirve? vista desde arriba de la curva")
def _(d):
    return P(["#2a5a2a", "#163a16"], [BG("curva_arriba"), IMG("f1_arriba", ancho=140, x=278, z=0.5, keys=[{"t": 0, "y": 1800}, {"t": d, "y": 1500, "ease": "lineal"}])],
             cam(1.0, 1.04, (540, 1200)), "corte", hud=[amarillo(0.05, d - 0.03, "¿PARA QUÉ?", y=560, tam=120, color=AMBAR)], sfx=[(0.1, "roce", -20)])


@v.plano(128, "para tomar las curvas rapidísimo: el coche traza la curva con estela")
def _(d):
    pts = [(0.0, 278, 1500, 0), (0.3, 278, 1004, 0), (0.55, 540, 720, 90), (0.8, 802, 1004, 180), (1.0, 802, 1500, 180)]
    return P(["#2a5a2a", "#163a16"], [BG("curva_arriba"), IMG("f1_arriba", ancho=140, z=0.5, keys=[{"t": round(f * d, 3), "x": x, "y": y, "rot": r, "ease": "lineal"} for f, x, y, r in pts]),
                                      flecha([[278, 1500], [278, 1004], [400, 760], [540, 720], [680, 760], [802, 1004], [802, 1500]], 0.0, d, "#ffe93dcc", 8, punta=False, z=0.45)],
             cam(1.0, 1.04, (540, 1100)), "corte", hud=[amarillo(0.3, d - 0.03, "RAPIDÍSIMO", y=560, tam=110, color=AMBAR)], sfx=[(0.05, "whoosh", -16, {"dur": 0.8})])


@v.plano(133, "el aire los sujeta al asfalto: el coche pegado al suelo con chispas")
def _(d):
    return P(NOCHE, [pista(), coche(y=1520, keys=[{"t": 0, "x": 460}, {"t": d, "x": 620}]), *aire_abajo(220, 860, 1000, 1350, 0.05, 5), chispas(540, 1630, 7)],
             cam(1.1, 1.15, (540, 1400)), "corte", hud=[rotulo(0.2, d - 0.05, "SUJETO AL ASFALTO", tam=88, color="#141414", capsula="#2ff3ffe6", y=560)], sfx=[(0.1, "zap", -22)])


@v.plano(139, "así que, en la próxima carrera: dos coches pasan por la pista de noche")
def _(d):
    return P(NOCHE, [pista(), coche(ancho=760, y=1400, keys=[{"t": 0, "x": 100}, {"t": d, "x": 1000, "ease": "lineal"}]),
                     coche("f1_b", ancho=760, y=1650, keys=[{"t": 0, "x": -150}, {"t": d, "x": 750, "ease": "lineal"}])],
             cam(1.0, 1.04, (540, 1400)), "corte", sfx=[(0.05, "whoosh", -16, {"dur": 0.6}), (d * 0.5, "whoosh", -18, {"dur": 0.6})])


@v.plano(146, "van aplastados por el aire: vuelve al túnel boca abajo (bucle)")
def _(d):
    return P(TUN, [tunel(), techo([{"t": 0, "x": 760, "y": 640, "rot": 180}, {"t": d, "x": 460, "y": 640, "rot": 180, "ease": "lineal"}], 980),
                   *aire_abajo(240, 840, 1100, 800, 0.1, 4, CIAN), chispas(560, 520, 8)],
             cam(1.0, 1.08, (540, 800)), "corte", hud=[amarillo(0.3, d - 0.4, "APLASTADOS", y=1300, tam=120, color=CIAN)], sfx=[(0.05, "impacto", -16), (d * 0.6, "ding", -22)])


v.construir("2026-11-20-manana-02-formula-uno-por-el-techo", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 62, "db": -13},
            claves=["techo", "Fórmula", "boca", "abajo", "caerse", "alerones", "alas", "avión", "revés", "aplasta", "suelo", "carga", "aerodinámica",
                    "velocidad", "doble", "cuatro", "doscientos", "kilómetros", "peso", "vuelta", "arriba", "No", "motor", "túnel", "sí", "curvas", "aire"])
