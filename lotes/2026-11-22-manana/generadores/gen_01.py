"""01 · Esta canasta tenía fondo (el baloncesto empezó con cestas de melocotones, 1891) — método denso.
Lote 2026-11-22-manana (Agente 08:00, Nico). Tendencia del día: «bàsquet» (Google Trends ES).
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_1122m  # noqa: E402

SVG = ilus_1122m.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

MADERA = ["#3a2016", "#1a0e08"]
NOCHE = ["#0c1430", "#3a4a72"]


def gim(n="bg_gimnasio"): return BG(n)


def nieve(sem=1, n=70): return {**polvo("#ffffff", n, (0, 0, 1080, 1920), sem, "nieve"), "z": 0.88, "tam": [3, 8], "vel": [10, 60]}


def cesta_en(x, y, ancho, keys=None, z=0.5, n="cesta"): return IMG(n, ancho=ancho, x=x, y=y, z=z, keys=keys or [])


# ================================================================== PLANOS
@v.plano(0, "gancho: el balón cae dentro de la cesta de melocotones y se queda dentro")
def _(d):
    return P(MADERA, [gim("bg_gimnasio_luz"), cesta_en(540, 1060, 760, z=0.4),
                      IMG("balon_cuero", ancho=330, x=540, z=0.45, keys=cae(0.0, min(0.9, d * 0.5), 420, 930) + [{"t": d, "rot": 25}]),
                      cesta_en(540, 1060, 760, z=0.5, n="cesta_frente"), polvo("#ffe8b0", 30, (100, 500, 1000, 1500), 2)],
             cam(1.0, 1.12, (540, 1000)), vineta=0.5, sfx=[(0.02, "subida", -16, {"dur": 0.6}), (0.55, "golpe", -12)])


@v.plano(4, "el baloncesto empezó con cestas: la cesta grande sobre fondo cálido")
def _(d):
    return P(MADERA, [gim(), brillo(540, 1000, 500, "#ffd88a", 0.35, 0.2), cesta_en(540, 1060, 620, keys=[{"t": 0, "rot": -3}, {"t": d, "rot": 3, "ease": "suave"}]), polvo("#ffe8b0", 30, (100, 500, 1000, 1500), 4)],
             cam(1.0, 1.06, (540, 1000)), "desenfoque")


@v.plano(8, "de melocotones: los melocotones caen dentro de la cesta")
def _(d):
    els = [gim(), cesta_en(540, 1100, 620, z=0.4)]
    for k, (x, t) in enumerate([(460, 0.0), (600, 0.15), (520, 0.3), (640, 0.45), (430, 0.55)]):
        els.append(IMG("melocoton", ancho=150, x=x, z=0.45, keys=cae(t, t + 0.6, 300, 1000 + (k % 2) * 30)))
    els.append(cesta_en(540, 1100, 620, z=0.5, n="cesta_frente"))
    return P(MADERA, els, cam(1.0, 1.05, (540, 1000)), "corte", hud=[rotulo(0.2, d - 0.05, "MELOCOTONES", tam=96, color="#141414", capsula="#ffb070e6", y=560)],
             sfx=[(0.5, "golpe", -20), (0.75, "golpe", -22)])


@v.plano(11, "cada vez que alguien encestaba: un jugador lanza hacia la cesta de la barandilla")
def _(d):
    return P(MADERA, [gim(), cesta_en(780, 760, 300, z=0.4), IMG("jugador_a", ancho=360, x=330, y=1200, z=0.5, keys=[{"t": 0, "y": 1230}, {"t": 0.3, "y": 1150, "ease": "salida"}, {"t": d, "y": 1210, "ease": "suave"}]),
                      IMG("balon_cuero", ancho=110, z=0.45, keys=lanza(0.15, d * 0.95, (300, 950), (780, 690)) + [{"t": 0.15, "rot": 0}, {"t": d, "rot": 300}]),
                      cesta_en(780, 760, 300, z=0.5, n="cesta_frente"), flecha([[320, 950], [560, 560], [760, 640]], 0.1, d * 0.8, AMBAR, 6, disc=[22, 16], z=0.42)],
             cam(1.0, 1.04, (540, 900)), "corte", sfx=[(0.1, "whoosh", -16)])


@v.plano(16, "el balón se quedaba dentro: primer plano del balón atascado que tiembla")
def _(d):
    return P(MADERA, [gim("bg_gimnasio_luz"), cesta_en(540, 1100, 820, z=0.4),
                      IMG("balon_cuero", ancho=360, x=540, y=970, z=0.45, keys=late(0.1, 3, 0.05, 0.25) + [{"t": 0, "rot": -8}, {"t": d, "rot": 8, "ease": "suave"}]),
                      cesta_en(540, 1100, 820, z=0.5, n="cesta_frente")],
             cam(1.05, 1.12, (540, 1000)), "corte", hud=[amarillo(0.25, d - 0.05, "SE QUEDABA DENTRO", y=560, tam=96)], sfx=[(0.1, "golpe", -18), (0.35, "golpe", -24)])


@v.plano(21, "pasó en diciembre de 1891: la hoja del calendario cae con nieve")
def _(d):
    return P(NOCHE, [BG("bg_nieve_noche"), IMG("cal_1891", ancho=620, x=540, y=1000, z=0.5, keys=aparece(0.05) + [{"t": 0.5, "rot": -4}, {"t": d, "rot": 3, "ease": "suave"}]), nieve(3)],
             cam(1.0, 1.06, (540, 1000)), "desenfoque", hud=[rotulo(0.3, d - 0.05, "DICIEMBRE", tam=90, color="#141414", capsula="#ffffffe6", y=560)], sfx=[(0.05, "ding", -20)])


@v.plano(30, "en Springfield, Estados Unidos: el edificio de ladrillo de noche con nieve")
def _(d):
    return P(NOCHE, [BG("bg_nieve_noche"), nieve(5, 90), brillo(540, 1150, 380, "#ffcf7a", 0.35, 0.3, pulso=[0.1, 1.5])],
             cam(1.0, 1.1, (540, 1050)), "corte", hud=[contexto(0.2, d - 0.05, "SPRINGFIELD, EE. UU.")], sfx=[(0.1, "rumor", -22, {"dur": min(2.0, d)})])


@v.plano(34, "un profesor canadiense: la silueta del profesor junto al ventanal")
def _(d):
    return P(MADERA, [gim(), brillo(540, 700, 500, "#ffd88a", 0.3, 0.2), IMG("profesor", ancho=440, x=540, y=1120, z=0.5, keys=arranque(540, 1120, d, "izquierda", 200, 30))],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[rotulo(0.2, d - 0.05, "CANADIENSE", tam=86, color="#141414", capsula="#ffd23fe6", y=560)])


@v.plano(37, "James Naismith: el profesor de cerca con su nombre")
def _(d):
    return P(MADERA, [gim("bg_gimnasio_luz"), IMG("profesor", ancho=620, x=600, y=1300, z=0.5, keys=[{"t": 0, "x": 640}, {"t": d, "x": 580, "ease": "suave"}])],
             cam(1.05, 1.1, (560, 1000)), "corte", hud=[rotulo(0.05, d - 0.02, "NAISMITH", tam=100, color="#ffffff", capsula="#000000b0", y=560)])


@v.plano(39, "tenía un problema: la pizarra vacía con una interrogación que late")
def _(d):
    return P(MADERA, [gim(), IMG("pizarra", ancho=760, x=540, y=1000, z=0.45, keys=aparece(0.0))],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[amarillo(0.15, d - 0.05, "¿PROBLEMA?", y=1000, tam=140, color="#ffffff")], sfx=[(0.1, "roce", -20)])


@v.plano(42, "era invierno: un copo de nieve gigante girando")
def _(d):
    return P(NOCHE, [BG("bg_nieve_noche"), IMG("copo", ancho=640, x=540, y=1000, z=0.5, keys=aparece(0.0) + [{"t": 0, "rot": 0}, {"t": d, "rot": 60, "ease": "lineal"}]), nieve(7)],
             cam(1.0, 1.08, (540, 1000)), "corte", hud=[amarillo(0.15, d - 0.05, "INVIERNO", y=560, tam=110, color=CIAN)], sfx=[(0.05, "brillo", -18)])


@v.plano(44, "nevaba: el edificio entero bajo una nevada fuerte")
def _(d):
    return P(NOCHE, [BG("bg_nieve_noche"), nieve(9, 160), nieve(10, 80)], cam(1.15, 1.05, (540, 1100)), "corte", sfx=[(0.0, "rumor", -18, {"dur": d})])


@v.plano(45, "y sus alumnos se aburrían: jugadores quietos en el gimnasio, un balón rueda solo")
def _(d):
    return P(MADERA, [gim(), IMG("jugador_b", ancho=260, x=250, y=1190, z=0.45, keys=[{"t": 0, "rot": -2}, {"t": d, "rot": 2, "ease": "suave"}]),
                      IMG("jugador_a2", ancho=260, x=820, y=1190, z=0.45, keys=[{"t": 0, "rot": 2}, {"t": d, "rot": -2, "ease": "suave"}]),
                      IMG("balon_cuero", ancho=120, y=1330, z=0.5, keys=[{"t": 0, "x": 380, "rot": 0}, {"t": d, "x": 700, "rot": 260, "ease": "salida"}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[amarillo(0.3, d - 0.05, "ABURRIDOS", y=560, tam=110, color="#ffd23f")])


@v.plano(50, "encerrados en el gimnasio: el gimnasio entero visto desde lejos, con la nieve en los ventanales")
def _(d):
    return P(MADERA, [gim("bg_gimnasio_luz"), IMG("jugador_b", ancho=150, x=420, y=1260, z=0.45), IMG("jugador_a2", ancho=150, x=660, y=1260, z=0.45)],
             cam(1.2, 1.0, (540, 900)), "corte", sfx=[(0.1, "golpe", -24)])


@v.plano(54, "así que inventó un juego bajo techo: el balón se enciende como una idea sobre el profesor")
def _(d):
    return P(MADERA, [gim(), IMG("profesor", ancho=440, x=420, y=1150, z=0.45),
                      brillo(700, 760, 260, "#ffe08a", 0.7, 0.46, pulso=[0.15, 0.6]),
                      IMG("balon_cuero", ancho=240, x=700, y=760, z=0.5, keys=aparece(0.15) + late(0.6, 2, 0.08, 0.3))],
             cam(1.0, 1.05, (560, 950)), "corte", sfx=[(0.15, "brillo", -16)])


@v.plano(57, "un juego bajo techo: el balón bota en el suelo de tablas")
def _(d):
    return P(MADERA, [gim("bg_gimnasio_luz"), IMG("balon_cuero", ancho=300, x=540, z=0.5, keys=cae(0.0, min(0.7, d * 0.7), 700, 1180) + [{"t": 0, "rot": 0}, {"t": d, "rot": 90}])],
             cam(1.05, 1.1, (540, 1050)), "corte", hud=[rotulo(0.05, d - 0.02, "BAJO TECHO", tam=86, color="#141414", capsula="#7dff3ae6", y=560)], sfx=[(0.25, "golpe", -14)])


@v.plano(62, "trece: un 13 enorme de golpe")
def _(d):
    return P(["#3a2016", "#120804"], [brillo(540, 1000, 500, "#ffd23f", 0.5, 0.1)], cam(1.0, 1.1, (540, 1000), temblor=3), "corte",
             hud=[rotulo(0.0, d - 0.02, "13", tam=300, color="#ffd23f", capsula=None, y=1000, sin_pop=True)], sfx=[(0.0, "golpe", -12)])


@v.plano(63, "reglas: la hoja de reglas clavada en la pared y un contador")
def _(d):
    return P(MADERA, [gim(), IMG("hoja_reglas", ancho=640, x=540, y=1010, z=0.5, keys=aparece(0.0) + [{"t": 0.4, "rot": -2}, {"t": d, "rot": 1, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[contador(0.05, d - 0.03, 1, 13, d * 0.6, " REGLAS", y=560, tam=110, color="#141414", capsula="#ffd23fe6")],
             sfx=[(0.05, "tictac", -22, {"dur": d * 0.6, "ritmo": 0.07})])


@v.plano(64, "¿y las canastas?: la barandilla de la galería vacía")
def _(d):
    return P(MADERA, [gim("bg_gimnasio_luz"), senala(540, 650, 0.15, d - 0.1, 160, AMBAR)],
             cam(1.25, 1.35, (540, 700)), "corte", hud=[amarillo(0.1, d - 0.05, "¿CANASTAS?", y=1050, tam=110, color="#ffffff")], sfx=[(0.1, "roce", -20)])


@v.plano(67, "clavó dos cestas: el martillo golpea el clavo y la cesta queda en la barandilla")
def _(d):
    return P(MADERA, [gim(), cesta_en(540, 820, 460, z=0.4, keys=aparece(0.0)),
                      IMG("martillo", ancho=380, x=820, y=600, z=0.55, keys=[{"t": 0, "rot": -50}, {"t": d * 0.3, "rot": 15, "ease": "entrada"}, {"t": d * 0.45, "rot": -20},
                                                                        {"t": d * 0.7, "rot": 15, "ease": "entrada"}, {"t": d, "rot": -10}])],
             cam(1.1, 1.15, (600, 760)), "corte", sfx=[(d * 0.3, "golpe", -12), (d * 0.7, "golpe", -12)])


@v.plano(71, "de fruta en la barandilla de la galería: las dos cestas a cada lado de la galería")
def _(d):
    return P(MADERA, [gim(), cesta_en(200, 760, 260, z=0.45, keys=aparece(0.05)), cesta_en(880, 760, 260, z=0.45, keys=aparece(0.4)),
                      senala(200, 740, 0.2, d - 0.1, 150), senala(880, 740, 0.5, d - 0.1, 150, CIAN)],
             cam(1.0, 1.0, (540, 900)), "corte", sfx=[(0.05, "pop", -20), (0.4, "pop", -20)])


@v.plano(80, "tres metros: un 3 enorme")
def _(d):
    return P(["#3a2016", "#120804"], [brillo(540, 1000, 500, "#7dff3a", 0.4, 0.1)], cam(1.0, 1.1, (540, 1000), temblor=3), "corte",
             hud=[rotulo(0.0, d - 0.02, "3 M", tam=260, color=LIMA, capsula=None, y=1000, sin_pop=True)], sfx=[(0.0, "golpe", -12)])


@v.plano(82, "del suelo: flecha desde el suelo hasta la cesta y contador")
def _(d):
    return P(MADERA, [gim(), cesta_en(540, 760, 280, z=0.45), flecha([[540, 1270], [540, 840]], 0.05, d * 0.7, LIMA, 10, z=0.5)],
             cam(1.0, 1.04, (540, 1000)), "corte", hud=[contador(0.05, d - 0.03, 0, 3, d * 0.7, " METROS", y=1080, x=720, tam=120, color=LIMA, capsula="#000000a0")],
             sfx=[(0.05, "subida", -20, {"dur": d * 0.7})])


@v.plano(84, "y, por casualidad: la cesta antigua parpadea y la cámara se aleja")
def _(d):
    return P(MADERA, [gim("bg_gimnasio_luz"), cesta_en(540, 900, 520, z=0.45, keys=late(0.2, 2, 0.06, 0.4))],
             cam(1.1, 1.0, (540, 900)), "desenfoque", hud=[rotulo(0.3, d - 0.05, "POR CASUALIDAD", tam=86, color="#141414", capsula="#ffd23fe6", y=560)])


@v.plano(87, "esa es la misma altura: la cesta antigua con una línea de altura")
def _(d):
    return P(MADERA, [gim("bg_gimnasio_luz"),
                                      cesta_en(300, 760, 320, z=0.45, keys=aparece(0.0)),
                                      flecha([[90, 700], [990, 700]], 0.2, d * 0.9, CIAN, 6, disc=[26, 18], punta=False, z=0.5)],
             cam(1.0, 1.03, (540, 900)), "corte", sfx=[(0.05, "pop", -20)])


@v.plano(93, "que tienen hoy las canastas: llega la canasta moderna a la misma altura")
def _(d):
    return P(MADERA, [gim("bg_gimnasio_luz"),
                                      cesta_en(300, 760, 320, z=0.45),
                                      IMG("canasta_moderna", ancho=420, z=0.45, keys=[{"t": 0, "x": 1300, "y": 880}, {"t": 0.45, "x": 790, "ease": "elastico"}]),
                                      flecha([[90, 700], [990, 700]], 0.0, 0.01, CIAN, 6, disc=[26, 18], punta=False, z=0.5)],
             cam(1.0, 1.03, (540, 900)), "corte", hud=[rotulo(0.4, d - 0.02, "MISMA ALTURA", tam=84, color="#141414", capsula="#2ff3ffe6", y=1180)],
             sfx=[(0.1, "whoosh", -16), (0.45, "golpe", -18)])


@v.plano(97, "jugaron nueve: aparecen nueve jugadores de rojo")
def _(d):
    els = [gim()]
    for k in range(9):
        x, y = 140 + (k % 5) * 200, 980 + (k // 5) * 240
        els.append(IMG("jugador_a" if k % 2 else "jugador_a2", ancho=170, x=x, y=y, z=0.45 + k * 0.005, keys=aparece(0.03 + k * min(0.07, d * 0.6 / 9))))
    return P(MADERA, els, cam(1.0, 1.03, (540, 1000)), "corte", hud=[contador(0.05, d - 0.03, 1, 9, d * 0.6, "", y=560, tam=130, color="#ff6a5a")],
             sfx=[(0.05, "tictac", -22, {"dur": d * 0.6, "ritmo": 0.07})])


@v.plano(99, "contra nueve: llegan nueve de blanco enfrente")
def _(d):
    els = [gim()]
    for k in range(9):
        x, y = 140 + (k % 5) * 200, 980 + (k // 5) * 240
        els.append(IMG("jugador_a2", ancho=120, x=x, y=y - 140, z=0.44, op=0.6))
        els.append(IMG("jugador_b" if k % 2 else "jugador_b2", ancho=170, x=x + 60, y=y + 40, z=0.46 + k * 0.005, keys=aparece(0.03 + k * min(0.06, d * 0.6 / 9))))
    return P(MADERA, els, cam(1.0, 1.03, (540, 1000)), "corte", hud=[rotulo(0.05, d - 0.02, "9 CONTRA 9", tam=110, color="#141414", capsula="#ffffffe6", y=560)])


@v.plano(101, "con un balón de fútbol: el balón de cuero bota en primer plano")
def _(d):
    return P(MADERA, [gim("bg_gimnasio_luz"), IMG("balon_cuero", ancho=520, x=540, z=0.5, keys=cae(0.0, min(0.8, d * 0.6), 500, 1050) + [{"t": 0, "rot": -30}, {"t": d, "rot": 40}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[rotulo(0.3, d - 0.05, "DE FÚTBOL", tam=100, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.3, "golpe", -12)])


@v.plano(106, "¿y el marcador?: la pizarra del marcador aparece")
def _(d):
    return P(MADERA, [gim(), IMG("pizarra", ancho=820, x=540, y=1000, z=0.45, keys=aparece(0.0) + [{"t": 0.4, "rot": -2}, {"t": d, "rot": 2}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[amarillo(0.1, d - 0.05, "¿MARCADOR?", y=1000, tam=120, color="#ffffff")], sfx=[(0.05, "roce", -20)])


@v.plano(109, "uno: un 1 en tiza")
def _(d):
    return P(MADERA, [gim(), IMG("pizarra", ancho=820, x=540, y=1000, z=0.45)], cam(1.1, 1.15, (540, 1000)), "corte",
             hud=[rotulo(0.0, d - 0.02, "1", tam=220, color="#ffffff", capsula=None, y=1000, sin_pop=True)], sfx=[(0.0, "golpe", -14)])


@v.plano(111, "a cero: 1 - 0 en tiza")
def _(d):
    return P(MADERA, [gim(), IMG("pizarra", ancho=820, x=540, y=1000, z=0.45)],
             cam(1.05, 1.12, (540, 1000), temblor=3), "corte", hud=[rotulo(0.0, d - 0.05, "1 - 0", tam=220, color="#ffffff", capsula=None, y=1000, sin_pop=True)],
             sfx=[(0.02, "golpe", -10), (0.02, "impacto", -14)])


@v.plano(112, "una sola canasta en todo el partido: el balón entra despacio y se ilumina")
def _(d):
    return P(MADERA, [gim("bg_gimnasio_luz"), cesta_en(540, 1100, 700, z=0.4), brillo(540, 940, 300, "#ffd23f", 0.5, 0.42, pulso=[0.1, 0.8]),
                      IMG("balon_cuero", ancho=300, x=540, z=0.45, keys=[{"t": 0, "y": 500}, {"t": d * 0.6, "y": 990, "ease": "salida"}]),
                      cesta_en(540, 1100, 700, z=0.5, n="cesta_frente")],
             cam(1.0, 1.05, (540, 950)), "corte", hud=[rotulo(0.2, d - 0.05, "UNA SOLA CANASTA", tam=86, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(d * 0.55, "golpe", -16)])


@v.plano(119, "lo peor era sacar el balón: el balón atascado, la cámara sube hasta la galería")
def _(d):
    return P(MADERA, [gim(), cesta_en(540, 760, 360, z=0.4), IMG("balon_cuero", ancho=150, x=540, y=700, z=0.45, keys=late(0.1, 3, 0.06, 0.3)),
                      cesta_en(540, 760, 360, z=0.5, n="cesta_frente")],
             cam(1.0, 1.25, (540, 1100), (540, 760)), "corte", hud=[amarillo(0.3, d - 0.05, "¿CÓMO LO SACO?", y=1100, tam=96, color="#ffffff")])


@v.plano(125, "primero subían con una escalera: la escalera sube hasta la barandilla")
def _(d):
    return P(MADERA, [gim(), cesta_en(560, 760, 300, z=0.4), IMG("balon_cuero", ancho=130, x=560, y=710, z=0.45), cesta_en(560, 760, 300, z=0.5, n="cesta_frente"),
                      IMG("escalera", ancho=230, x=520, z=0.47, rot=8, keys=lanza(0.0, d * 0.5, (520, 1800), (520, 1180)))],
             cam(1.3, 1.4, (540, 900)), "corte", hud=[rotulo(0.3, d - 0.05, "ESCALERA", tam=90, color="#141414", capsula="#ffd23fe6", y=480)], sfx=[(d * 0.45, "golpe", -16)])


@v.plano(130, "luego con un palo: el palo empuja desde abajo y el balón salta fuera")
def _(d):
    return P(MADERA, [gim(), cesta_en(560, 760, 300, z=0.4),
                      IMG("balon_cuero", ancho=130, x=560, z=0.45, keys=[{"t": 0, "y": 710}, {"t": d * 0.45, "y": 710}, {"t": d * 0.75, "y": 420, "ease": "salida"}, {"t": d, "y": 520, "ease": "entrada"}]),
                      cesta_en(560, 760, 300, z=0.5, n="cesta_frente"),
                      IMG("palo", ancho=160, x=600, z=0.48, keys=[{"t": 0, "y": 1700}, {"t": d * 0.45, "y": 1380, "ease": "salida"}, {"t": d * 0.6, "y": 1380}, {"t": d, "y": 1500}])],
             cam(1.6, 1.5, (560, 800)), "corte", hud=[rotulo(0.3, d - 0.05, "UN PALO", tam=90, color="#141414", capsula="#ffd23fe6", y=1180)], sfx=[(d * 0.45, "golpe", -14)])


@v.plano(134, "hasta que a alguien se le ocurrió: la cesta de cerca, brillo de idea")
def _(d):
    return P(MADERA, [gim("bg_gimnasio_luz"), brillo(540, 900, 420, "#ffe08a", 0.5, 0.3, pulso=[0.12, 0.5]), cesta_en(540, 1000, 640, z=0.45, keys=late(0.3, 2, 0.05, 0.35))],
             cam(1.0, 1.06, (540, 1000)), "corte", sfx=[(0.1, "subida", -18, {"dur": min(1.2, d)})])


@v.plano(141, "quitarle el fondo: el fondo de mimbre cae y el balón pasa por el hueco")
def _(d):
    return P(MADERA, [gim("bg_gimnasio_luz"), cesta_en(540, 860, 640, z=0.4, n="cesta_sin_fondo"),
                      IMG("fondo_cesta", ancho=380, x=540, z=0.38, keys=[{"t": 0, "y": 1080, "rot": 0}, {"t": 0.5, "y": 1560, "rot": 25, "ease": "entrada"}, {"t": d, "y": 1580, "rot": 25}]),
                      IMG("balon_cuero", ancho=260, x=540, z=0.42, keys=[{"t": 0, "y": 300}, {"t": d * 0.75, "y": 1500, "ease": "entrada"}, {"t": d, "y": 1600}])],
             cam(1.0, 1.08, (540, 960)), "corte", hud=[rotulo(0.25, d - 0.05, "SIN FONDO", tam=110, color="#141414", capsula="#7dff3ae6", y=560)], sfx=[(0.45, "golpe", -12), (0.4, "impacto", -16)])


avisos = v.construir("2026-11-22-manana-01-canasta-con-fondo", claves=["MELOCOTONES", "TRECE", "TRES", "NUEVE", "UNO", "CERO", "FONDO"],
                     musica={"generar": "curiosidad", "semilla": 22, "db": -13}, bucle=0.35)
