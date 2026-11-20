"""03 · Este bólido eléctrico es de 1899 — método denso. Lote 2026-11-20-manana (Agente 08:00, Nico). Tendencia del día: «tesla argentina» (sin marcas).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]
Versión corta: se quitan «Su nombre, en francés, significa "la nunca contenta".» (11–18) y «Y no era una rareza.» (59–63) para no pasar de 60 s.
EXPERIMENTO del lote: gancho de contraste de época en dos golpes («Este bólido es eléctrico. / Y de 1899.»)."""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_1120m  # noqa: E402

SVG = ilus_1120m.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG, omitir=[(11, 19), (59, 64)])

SEPIA = ["#c8b898", "#5a4a32"]
CIUDAD = ["#a8b8c8", "#3a2e24"]
OSC = ["#0a1a2a", "#020610"]
PARIS = ["#6a5a7a", "#1a1420"]


def campo(): return BG("bg_campo_1899")
def ciudad(): return BG("bg_ciudad_1900")
def estudio(): return BG("bg_estudio")
def polvareda(x, y, sem=1): return polvo("#e8d8b0", 50, (x - 300, y - 40, x + 200, y + 60), sem)


def bolido(ancho=900, x=540, y=1500, z=0.5, keys=None, **k):
    """Lienzo 1200×560 → con ancho 900 mide 420 de alto; ruedas abajo en y+≈160; piloto en (x+5, y-150)."""
    return IMG("bolido_1899", ancho=ancho, x=x, y=y, z=z, keys=keys or [], **k)


def anio(t0, t1, desde, hasta, dur, y=560):
    return contador(t0, t1, desde, hasta, dur, "", y=y, tam=150, color="#ffd23f", miles=False)


# ================================================================== PLANOS
@v.plano(0, "gancho: el bólido de torpedo corre por la carretera levantando polvo")
def _(d):
    return P(SEPIA, [campo(), bolido(ancho=1100, keys=arranque(560, 1450, d, "izquierda", 560, 60)), polvareda(300, 1600, 1), *lineas_vel(180, 1450, 1, "#5a4a32aa")],
             cam(1.0, 1.1, (540, 1350)), vineta=0.6, sfx=[(0.02, "whoosh", -12, {"dur": 0.6}), (0.3, "zap", -20)])


@v.plano(3, "eléctrico: un rayo cae sobre el bólido y se enciende")
def _(d):
    return P(SEPIA, [campo(), bolido(y=1480, keys=[{"t": 0, "x": 520}, {"t": d, "x": 600}]), brillo(560, 1400, 500, "#2ff3ff", 0.5, 0.4, keys=[{"t": 0, "op": 1}, {"t": d, "op": 0.2}]),
                     flecha([[620, 600], [520, 900], [600, 920], [500, 1260]], 0.0, 0.2, CIAN, 14, punta=False, z=0.6)],
             cam(1.1, 1.15, (540, 1300)), "corte", hud=[rotulo(0.05, d - 0.03, "ELÉCTRICO", tam=120, color="#141414", capsula="#2ff3ffe6", y=560)], sfx=[(0.02, "zap", -14)])


@v.plano(4, "y de mil ochocientos noventa y nueve: el año corre hasta 1899 sobre el calendario")
def _(d):
    return P(SEPIA, [campo(), IMG("calendario", ancho=560, x=540, y=1200, z=0.5, keys=aparece(0.0)), {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#2a1a0a", "op": 0.3, "x": 540, "y": 960, "z": 0.1}],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[anio(0.05, d - 0.03, 2025, 1899, d * 0.6)], sfx=[(0.05, "tictac", -22, {"dur": min(1.2, d * 0.6), "ritmo": 0.06}), (d * 0.6, "impacto", -16)])


@v.plano(10, "micro: «nueve», fogonazo de foto antigua sobre el bólido")
def _(d):
    return P(SEPIA, [campo(), bolido(ancho=1100, y=1400, keys=[{"t": 0, "escala": 1.1}, {"t": d, "escala": 1.0, "ease": "salida"}]), fundido_blanco([{"t": 0, "op": 0.9}, {"t": 0.3, "op": 0}])],
             cam(1.0, 1.06, (540, 1300)), "corte", hud=[rotulo(0.05, d + 0.05, "1899", tam=150, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.0, "impacto", -16)])


@v.plano(19, "tenía forma de: el bólido de frente, se gira")
def _(d):
    return P(OSC, [estudio(), bolido(ancho=1000, y=1250, keys=[{"t": 0, "ex": 0.35}, {"t": d, "ex": 1.0, "ease": "salida"}])], cam(1.0, 1.05, (540, 1200)), "corte", sfx=[(0.05, "roce", -20)])


@v.plano(22, "torpedo: el bólido gira despacio y se marca su silueta")
def _(d):
    return P(OSC, [estudio(), bolido(ancho=1000, y=1250, keys=[{"t": 0, "rot": -3}, {"t": d, "rot": 2, "ease": "suave"}]),
                   flecha([[90, 1230], [300, 1110], [560, 1090], [820, 1120], [1000, 1220]], 0.1, d * 0.7, AMBAR, 8, punta=False, z=0.6)],
             cam(1.0, 1.05, (540, 1200)), "corte", sfx=[(0.1, "roce", -20)])


@v.plano(24, "y dos motores eléctricos: dos motores aparecen con su rayo")
def _(d):
    return P(OSC, [estudio(), IMG("motor_electrico", ancho=520, x=320, y=1150, z=0.5, keys=aparece(0.0)), IMG("motor_electrico", ancho=520, x=770, y=1150, z=0.5, keys=aparece(0.2)),
                   brillo(540, 1150, 600, "#ffe93d", 0.3, 0.06, pulso=[0.1, 0.5])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[rotulo(0.3, d - 0.05, "2 MOTORES", tam=110, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "zap", -18), (0.25, "zap", -18)])


@v.plano(27, "¿y qué tan rápido iba? la aguja tiembla en cero")
def _(d):
    return P(OSC, [estudio(), IMG("velocimetro", ancho=800, x=540, y=1100, z=0.5),
                   IMG("aguja_vel", ancho=640, x=540, y=1300, z=0.55, keys=[{"t": 0, "rot": -180}, {"t": d * 0.3, "rot": -172}, {"t": d * 0.6, "rot": -178}, {"t": d, "rot": -170}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[amarillo(0.05, d - 0.03, "¿QUÉ TAN RÁPIDO?", y=560, tam=96, color=CIAN)], sfx=[(0.1, "roce", -20)])


@v.plano(32, "cerca de París: el bólido cruza delante del horizonte con la torre de hierro")
def _(d):
    return P(PARIS, [BG("bg_paris_1899"), bolido(ancho=620, y=1560, keys=[{"t": 0, "x": -200}, {"t": d, "x": 700, "ease": "lineal"}]), polvo("#e0a878", 40, (0, 1600, 1080, 1720), 2)],
             cam(1.0, 1.05, (540, 1200)), "desenfoque", hud=[contexto(0.1, d - 0.05, "PARÍS · 1899")], sfx=[(0.05, "rumor", -20, {"dur": min(1.5, d)})])


@v.plano(35, "el piloto belga Camille Jenatzy: primer plano del piloto de barba roja")
def _(d):
    return P(SEPIA, [campo(), bolido(ancho=1500, x=560, y=1500, keys=[{"t": 0, "x": 600}, {"t": d, "x": 520, "ease": "suave"}]), polvareda(200, 1700, 3)],
             cam(1.0, 1.08, (560, 1200)), "corte", hud=[rotulo(0.15, d - 0.05, "CAMILLE JENATZY", tam=92, color="#ffffff", capsula="#2a2030e6", y=560)], sfx=[(0.1, "pop", -20)])


@v.plano(40, "lo puso a: el bólido arranca con un tirón")
def _(d):
    return P(SEPIA, [campo(), bolido(y=1480, keys=lanza(0.0, d, (300, 1480), (900, 1480))), *lineas_vel(300, 1480, 4, "#5a4a32aa"), polvareda(250, 1620, 4)],
             cam(1.0, 1.06, (540, 1350)), "corte", sfx=[(0.02, "whoosh", -14, {"dur": 0.5})])


@v.plano(43, "ciento cinco kilómetros por hora: la aguja sube y la cifra corre")
def _(d):
    return P(OSC, [estudio(), brillo(540, 1250, 500, "#ff3d3d", 0.25, 0.06), IMG("velocimetro", ancho=800, x=540, y=1100, z=0.5),
                   IMG("aguja_vel", ancho=640, x=540, y=1300, z=0.55, keys=[{"t": 0, "rot": -180}, {"t": d * 0.6, "rot": -117, "ease": "salida"}, {"t": d, "rot": -115}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[contador(0.05, d - 0.03, 0, 105, d * 0.6, " KM/H", y=560, tam=120, color="#ffd23f")],
             sfx=[(0.05, "subida", -18, {"dur": min(1.0, d * 0.6)}), (d * 0.6, "impacto", -16)])


@v.plano(48, "fue el primer coche de la historia: cruza la meta y ondea la bandera")
def _(d):
    return P(SEPIA, [campo(), IMG("bandera_cuadros", ancho=360, x=860, y=1150, z=0.45, keys=[{"t": 0, "rot": -8}, {"t": d * 0.5, "rot": 8, "ease": "suave"}, {"t": d, "rot": -6, "ease": "suave"}]),
                     bolido(ancho=760, y=1560, keys=[{"t": 0, "x": -100}, {"t": d * 0.8, "x": 700, "ease": "lineal"}]), polvareda(250, 1700, 5)],
             cam(1.0, 1.05, (540, 1350)), "corte", hud=[rotulo(0.2, d - 0.05, "EL PRIMERO", tam=120, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "ding", -18)])


@v.plano(56, "en pasar de cien: un 100 enorme que se rompe")
def _(d):
    return P(OSC, [estudio(), brillo(540, 1000, 600, "#ffd23f", 0.4, 0.06, pulso=[0.1, 0.8]), bolido(ancho=700, y=1550, keys=[{"t": 0, "x": 300}, {"t": d, "x": 800, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[rotulo(0.05, d - 0.05, "+100 KM/H", tam=170, color="#141414", capsula="#ffd23fe6", y=1000)], sfx=[(0.05, "impacto", -14)])


@v.plano(64, "hacia mil novecientos: la calle de una gran ciudad y el año 1900")
def _(d):
    return P(CIUDAD, [ciudad(), IMG("taxi_1900", ancho=560, y=1560, z=0.5, keys=[{"t": 0, "x": 260}, {"t": d, "x": 460, "ease": "lineal"}])],
             cam(1.0, 1.05, (540, 1200)), "desenfoque", hud=[anio(0.05, d - 0.03, 1899, 1900, 0.3)], sfx=[(0.1, "ding", -20)])


@v.plano(67, "cerca de un tercio de los coches: tres coches, uno se ilumina")
def _(d):
    return P(OSC, [estudio(), IMG("coche_1912", ancho=330, x=200, y=1250, z=0.5, op=0.45, keys=aparece(0.0)), IMG("coche_1912", ancho=330, x=880, y=1250, z=0.5, op=0.45, keys=aparece(0.15)),
                   IMG("taxi_1900", ancho=330, x=540, y=1230, z=0.5, keys=aparece(0.3) + late(0.8, 1)), brillo(540, 1230, 300, "#2ff3ff", 0.45, 0.4)],
             cam(1.0, 1.05, (540, 1200)), "corte", hud=[rotulo(0.4, d - 0.05, "1 DE CADA 3", tam=120, color="#141414", capsula="#2ff3ffe6", y=560)], sfx=[(0.05, "pop", -20), (0.35, "zap", -20)])


@v.plano(75, "de Estados Unidos eran eléctricos: el coche eléctrico avanza por la calle con chispa cian")
def _(d):
    return P(CIUDAD, [ciudad(), IMG("taxi_1900_b", ancho=700, y=1520, z=0.5, keys=[{"t": 0, "x": 1000}, {"t": d, "x": 300, "ease": "lineal"}]), brillo(500, 1450, 260, "#2ff3ff", 0.3, 0.45, pulso=[0.1, 0.6])],
             cam(1.0, 1.08, (540, 1250)), "corte", hud=[amarillo(0.2, v.w(79) - v.w(75) - 0.03, "ELÉCTRICOS", y=560, tam=120, color="#ffd23f"), contexto(v.w(79) - v.w(75) + 0.05, d - 0.05, "NUEVA YORK · 1900")], sfx=[(0.1, "zap", -22)])


@v.plano(84, "micro: «más de», un taxi frena de golpe")
def _(d):
    return P(CIUDAD, [ciudad(), IMG("taxi_1900_b", ancho=900, x=540, y=1450, z=0.5, keys=[{"t": 0, "x": 800}, {"t": d, "x": 560, "ease": "salida"}])], cam(1.2, 1.25, (540, 1400)), "corte", sfx=[(0.02, "roce", -20)])


@v.plano(85, "más de sesenta taxis eléctricos: una fila de taxis cruza y la cifra corre")
def _(d):
    return P(CIUDAD, [ciudad()] + [IMG("taxi_1900" if i % 2 else "taxi_1900_b", ancho=300, y=1450 + (i % 2) * 180, z=0.5 + i * 0.01,
                                       keys=[{"t": 0, "x": -150 - i * 260}, {"t": d, "x": 1200 - i * 260, "ease": "lineal"}]) for i in range(6)],
             cam(1.0, 1.04, (540, 1300)), "corte", hud=[contador(0.05, d - 0.03, 0, 60, d * 0.6, " TAXIS", y=560, tam=120, color="#ffd23f", contar_prefijo="+")],
             sfx=[(0.05, "tictac", -24, {"dur": 0.8, "ritmo": 0.06})])


@v.plano(87, "eran silenciosos: el taxi pasa y todo queda en calma")
def _(d):
    return P(CIUDAD, [ciudad(), IMG("taxi_1900_b", ancho=700, y=1520, z=0.5, keys=[{"t": 0, "x": 260}, {"t": d, "x": 700, "ease": "suave"}])],
             cam(1.25, 1.3, (540, 1450)), "corte", hud=[rotulo(0.1, d - 0.05, "SILENCIOSOS", tam=104, color="#141414", capsula="#b8ff3ae6", y=560)], sfx=[(0.1, "brillo", -26)])


@v.plano(89, "no echaban humo: el coche de gasolina echa humo, el eléctrico no")
def _(d):
    return P(CIUDAD, [ciudad(), IMG("coche_1912", ancho=600, x=330, y=1350, z=0.5), IMG("humo", ancho=420, x=60, y=1280, z=0.55, keys=[{"t": 0, "escala": 0.5, "op": 0.2}, {"t": d, "escala": 1.3, "op": 0.9, "x": 0, "ease": "suave"}]),
                      IMG("taxi_1900", ancho=480, x=820, y=1650, z=0.5)],
             cam(1.0, 1.05, (540, 1400)), "corte", sfx=[(0.1, "rumor", -20, {"dur": min(1.0, d)})])


@v.plano(92, "y no había que arrancarlos con manivela: la manivela gira con esfuerzo")
def _(d):
    return P(OSC, [estudio(), IMG("coche_1912", ancho=1500, x=200, y=1250, z=0.45), IMG("manivela", ancho=560, x=760, y=1300, z=0.55, keys=[{"t": 0, "rot": 0}, {"t": d * 0.5, "rot": 200, "ease": "suave"}, {"t": d, "rot": 340, "ease": "suave"}])],
             cam(1.0, 1.06, (650, 1250)), "corte", hud=[rotulo(0.2, d - 0.05, "MANIVELA", tam=110, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "tictac", -22, {"dur": min(1.4, d), "ritmo": 0.18})])


@v.plano(99, "¿entonces qué pasó? la calle se oscurece, la lupa busca")
def _(d):
    return P(CIUDAD, [ciudad(), {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#0a0a14", "op": 0.45, "x": 540, "y": 960, "z": 0.1},
                      IMG("lupa", ancho=380, z=0.7, keys=[{"t": 0, "x": 300, "y": 1300}, {"t": d, "x": 760, "y": 1100, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1200)), "corte", hud=[amarillo(0.05, d - 0.03, "¿QUÉ PASÓ?", y=560, tam=130, color=AMBAR)], sfx=[(0.1, "roce", -20)])


@v.plano(102, "llegaron los coches de gasolina baratos: tres coches negros entran en fila")
def _(d):
    return P(CIUDAD, [ciudad()] + [IMG("coche_1912", ancho=420, y=1400 + i * 170, z=0.5 + i * 0.01, keys=[{"t": 0, "x": -300 - i * 200}, {"t": d * 0.8, "x": 300 + i * 220, "ease": "salida"}]) for i in range(3)],
             cam(1.0, 1.04, (540, 1350)), "corte", hud=[rotulo(0.3, v.w(108) - v.w(102) - 0.05, "GASOLINA BARATA", tam=96, color="#141414", capsula="#ffd23fe6", y=560),
                  anio(v.w(108) - v.w(102) + 0.05, d - 0.03, 1900, 1912, 0.6)], sfx=[(0.1, "rumor", -18, {"dur": min(1.6, d)})])


@v.plano(112, "uno costaba casi: los dos coches, uno frente a otro")
def _(d):
    return P(OSC, [estudio(), IMG("taxi_1900", ancho=500, x=290, y=1300, z=0.5, keys=aparece(0.0)), IMG("coche_1912", ancho=500, x=800, y=1330, z=0.5, keys=aparece(0.15)),
                   brillo(290, 1300, 260, "#2ff3ff", 0.3, 0.06), brillo(800, 1330, 260, "#ffd23f", 0.3, 0.06)],
             cam(1.0, 1.04, (540, 1300)), "corte", sfx=[(0.05, "pop", -20), (0.2, "pop", -20)])


@v.plano(115, "tres veces menos: etiqueta roja grande para el eléctrico, verde pequeña para el de gasolina")
def _(d):
    return P(OSC, [estudio(), IMG("taxi_1900", ancho=380, x=290, y=1500, z=0.5), IMG("coche_1912", ancho=380, x=800, y=1520, z=0.5),
                   IMG("etiqueta_roja", ancho=520, x=290, y=1040, z=0.55, keys=aparece(0.1) + [{"t": d, "escala": 1.12}]),
                   IMG("etiqueta_verde", ancho=210, x=800, y=1180, z=0.55, keys=aparece(0.5))],
             cam(1.0, 1.04, (540, 1250)), "corte",
             hud=[rotulo(0.15, d - 0.05, "× 3", tam=150, color="#ffffff", capsula=None, x=320, y=1040), rotulo(0.6, d - 0.05, "1", tam=80, color="#ffffff", capsula=None, x=805, y=1180),
                  rotulo(0.9, d - 0.05, "CASI 3 VECES MENOS", tam=84, color="#141414", capsula="#b8ff3ae6", y=560)],
             sfx=[(0.1, "pop", -18), (0.5, "pop", -18), (0.9, "ding", -20)])


@v.plano(121, "ese mismo año apareció el arranque eléctrico: un rayo enciende el motor")
def _(d):
    return P(OSC, [estudio(), IMG("coche_1912", ancho=900, x=540, y=1300, z=0.5, keys=late(d * 0.4, 1, 0.05)),
                   flecha([[980, 700], [880, 960], [960, 980], [880, 1230]], d * 0.3, d * 0.4, CIAN, 14, punta=False, z=0.6), brillo(900, 1230, 300, "#2ff3ff", 0.5, 0.55, keys=[{"t": 0, "op": 0}, {"t": d * 0.4, "op": 1}, {"t": d, "op": 0.3}])],
             cam(1.0, 1.06, (540, 1250)), "corte", hud=[rotulo(0.15, d - 0.05, "ARRANQUE ELÉCTRICO", tam=82, color="#141414", capsula="#2ff3ffe6", y=560)], sfx=[(d * 0.4, "zap", -14)])


@v.plano(128, "y adiós manivela: la manivela sale volando")
def _(d):
    return P(OSC, [estudio(), IMG("manivela", ancho=560, x=540, z=0.55, keys=[{"t": 0, "y": 1150, "rot": 0}, {"t": d, "y": 2300, "x": 760, "rot": 300, "ease": "entrada"}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[amarillo(0.05, d - 0.03, "ADIÓS", y=560, tam=140, color=MAGENTA)], sfx=[(0.05, "whoosh", -16, {"dur": 0.5}), (d * 0.8, "golpe", -22)])


@v.plano(131, "la gasolina se abarató: el surtidor y la etiqueta que baja")
def _(d):
    return P(CIUDAD, [ciudad(), IMG("surtidor", ancho=320, x=330, y=1350, z=0.5, keys=aparece(0.0)),
                      IMG("etiqueta_verde", ancho=380, x=760, z=0.55, keys=[{"t": 0, "y": 900, "escala": 1.0}, {"t": d * 0.8, "y": 1250, "escala": 0.7, "ease": "suave"}]),
                      flecha([[960, 900], [960, 1350]], 0.1, d * 0.7, LIMA, 12, z=0.6)],
             cam(1.0, 1.05, (540, 1200)), "corte", hud=[rotulo(0.2, d - 0.05, "MÁS BARATA", tam=104, color="#141414", capsula="#b8ff3ae6", y=560)], sfx=[(0.1, "pop", -20)])


@v.plano(135, "y hacia mil novecientos treinta y cinco: el año corre")
def _(d):
    return P(CIUDAD, [ciudad(), {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#0a0a14", "op": 0.35, "x": 540, "y": 960, "z": 0.1},
                      IMG("coche_1912", ancho=500, y=1560, z=0.5, keys=[{"t": 0, "x": 200}, {"t": d, "x": 500, "ease": "lineal"}])],
             cam(1.0, 1.05, (540, 1250)), "corte", hud=[anio(0.05, d - 0.03, 1912, 1935, d * 0.6)], sfx=[(0.05, "tictac", -24, {"dur": 0.6, "ritmo": 0.06})])


@v.plano(142, "los eléctricos casi habían desaparecido: el taxi eléctrico se desvanece en la calle vacía")
def _(d):
    return P(CIUDAD, [ciudad(), IMG("taxi_1900", ancho=700, x=540, y=1520, z=0.5, keys=[{"t": 0, "op": 1, "escala": 1.0}, {"t": d * 0.85, "op": 0.05, "escala": 0.9, "ease": "suave"}]),
                      polvo("#ffffff", 30, (200, 1200, 900, 1700), 8)],
             cam(1.0, 1.08, (540, 1400)), "corte", hud=[amarillo(0.2, d - 0.03, "DESAPARECIDOS", y=560, tam=104, color="#ffd23f")], sfx=[(0.1, "fugaz", -20)])


@v.plano(146, "micro: «desaparecido», la calle vacía")
def _(d):
    return P(CIUDAD, [ciudad(), {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#0a0a14", "op": 0.5, "x": 540, "y": 960, "z": 0.1}, polvo("#ffffff", 30, (100, 1300, 1000, 1700), 9)],
             cam(1.0, 1.08, (540, 1450)), "corte", sfx=[(0.02, "roce", -22)])


@v.plano(147, "tardaron casi cien años en volver: el eléctrico de hoy junto al bólido de 1899 (bucle)")
def _(d):
    return P(OSC, [estudio(), IMG("electrico_moderno", ancho=860, x=540, y=1150, z=0.5, keys=arranque(540, 1150, d, "derecha", 300, 30)),
                   bolido(ancho=760, x=540, y=1600, keys=[{"t": 0, "x": -300}, {"t": d * 0.6, "x": 540, "ease": "salida"}, {"t": d, "x": 580}]), brillo(540, 1150, 500, "#2ff3ff", 0.3, 0.06)],
             cam(1.0, 1.06, (540, 1350)), "corte", hud=[rotulo(0.3, d - 0.4, "≈ 100 AÑOS", tam=130, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "impacto", -16), (d * 0.6, "ding", -22)])


v.construir("2026-11-20-manana-03-bolido-electrico-1899", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 63, "db": -13},
            claves=["bólido", "eléctrico", "noventa", "nueve", "torpedo", "motores", "rápido", "París", "Camille", "Jenatzy", "ciento", "cinco", "primer", "cien",
                    "novecientos", "tercio", "eléctricos", "Nueva", "York", "sesenta", "taxis", "humo", "manivela", "pasó", "gasolina", "tres", "veces", "arranque",
                    "adiós", "treinta", "desaparecido", "cien", "años"])
