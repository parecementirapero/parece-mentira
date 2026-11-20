"""02 · Naciste con trescientos huesos — método denso. Lote 2026-11-19-tarde (Agente 20:00, Jorge).
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_1119t  # noqa: E402

SVG = ilus_1119t.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

RX = ["#06142a", "#041020"]
CUARTO = ["#f4d8c0", "#7a4a3a"]
HUESO_C = "#f2ead8"


def rx(): return BG("bg_rayos_x")


def esq(n="esqueleto", ancho=380, x=540, y=1230, z=0.5, keys=None, **k):
    """Esqueleto (lienzo 700×1950). Con ancho=380 y y=1230: cabeza desde y≈700, manos a y≈1200 (x=540±128), pies a y≈1705 (x=540±65), fémur 1258–1476 (x=540±43). Bebé: ancho 420, y=1325."""
    return IMG(n, ancho=ancho, x=x, y=y, z=z, keys=keys or [], **k)


def pegar(t, x, y, d):
    """Dos piezas de hueso que se acercan y se sueldan con un destello."""
    return [IMG("femur", ancho=220, z=0.5, keys=[{"t": 0, "x": x - 200, "y": y, "rot": 90 - 20}, {"t": t, "x": x - 100, "rot": 90, "ease": "salida"}, {"t": d, "x": x - 96}]),
            IMG("femur", ancho=220, z=0.5, keys=[{"t": 0, "x": x + 200, "y": y, "rot": 90 + 20}, {"t": t, "x": x + 100, "rot": 90, "ease": "salida"}, {"t": d, "x": x + 96}]),
            brillo(x, y, 220, "#ffd23f", 0.9, 0.6, keys=[{"t": t - 0.05, "op": 0}, {"t": t, "op": 1}, {"t": t + 0.4, "op": 0}])]


# ================================================================== PLANOS
@v.plano(0, "gancho: el esqueleto de bebé cae y bota, y la cifra 300 late")
def _(d):
    return P(RX, [rx(), esq("esqueleto_bebe", 420, keys=arranque(540, 1325, d, "arriba", 300, 30)), polvo("#7ec8ff", 30, (0, 400, 1080, 1800), 2)],
             cam(1.0, 1.06, (540, 1100)), vineta=0.6, hud=[rotulo(0.3, d - 0.05, "300", tam=150, color="#141414", capsula="#ffd23fe6", y=560)],
             sfx=[(0.02, "whoosh", -14, {"dur": 0.5}), (0.4, "golpe", -14)])


@v.plano(4, "ahora tienes doscientos seis: el esqueleto adulto aparece al lado, la cifra baja")
def _(d):
    return P(RX, [rx(), esq("esqueleto_bebe", 300, 300, 1400, 0.45), esq("esqueleto", 380, 740, 1230, 0.5, keys=aparece(0.0, 0.4))],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[contador(0.05, d - 0.03, 300, 206, d * 0.6, "", y=560, tam=150, color="#ffd23f")], sfx=[(0.05, "tictac", -22, {"dur": 0.6, "ritmo": 0.07})])


@v.plano(8, "¿dónde están los demás? la lupa recorre el esqueleto")
def _(d):
    return P(RX, [rx(), esq(), IMG("lupa2", ancho=380, z=0.7, keys=[{"t": 0, "x": 760, "y": 800}, {"t": d, "x": 380, "y": 1400, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[amarillo(0.05, d - 0.03, "¿Y LOS DEMÁS?", y=560, tam=100, color=CIAN)], sfx=[(0.1, "roce", -20)])


@v.plano(12, "no se ha perdido ninguno: huesos sueltos flotan y se ordenan")
def _(d):
    return P(RX, [rx()] + [IMG("femur", ancho=110, z=0.5, keys=[{"t": 0, "x": 540 + dx * 3, "y": 1100 + dy * 3, "rot": r0}, {"t": d * 0.8, "x": 540 + dx, "y": 1100 + dy, "rot": r0 + 60, "ease": "suave"}])
                       for dx, dy, r0 in [(-200, -200, 10), (180, -240, 80), (-240, 120, -40), (220, 160, 130), (0, 260, 60), (0, -300, -80)]],
             cam(1.0, 1.06, (540, 1100)), "corte", sfx=[(0.1, "pop", -20), (0.4, "pop", -22)])


@v.plano(17, "se han soldado: dos piezas se juntan con un destello")
def _(d):
    return P(RX, [rx(), *pegar(d * 0.5, 540, 1100, d)], cam(1.2, 1.3, (540, 1100)), "corte",
             hud=[amarillo(0.1, d - 0.03, "SOLDADOS", y=560, tam=120, color="#ffd23f")], sfx=[(d * 0.5, "golpe", -14), (d * 0.5, "brillo", -18)])


@v.plano(20, "un recién nacido: el bebé duerme en su cuna")
def _(d):
    return P(CUARTO, [BG("bg_cuarto_bebe"), IMG("bebe", ancho=820, x=540, y=1420, z=0.5, keys=[{"t": 0, "escala": 1.0}, {"t": d * 0.5, "escala": 1.02, "ease": "suave"}, {"t": d, "escala": 1.0, "ease": "suave"}]),
             polvo("#fff4d0", 30, (0, 400, 1080, 1400), 4)],
             cam(1.0, 1.06, (540, 1300)), "desenfoque", sfx=[(0.1, "ding", -24)])


@v.plano(24, "unas trescientas piezas: rayos X del bebé, la cifra corre")
def _(d):
    return P(RX, [rx(), esq("esqueleto_bebe", 420, y=1325, keys=[{"t": 0, "escala": 0.96}, {"t": d, "escala": 1.02}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[contador(0.05, d - 0.03, 0, 300, d * 0.6, " PIEZAS", y=560, tam=110, color="#ffd23f")], sfx=[(0.05, "tictac", -22, {"dur": 0.6, "ritmo": 0.07})])


@v.plano(27, "muchas de cartílago blando: la pieza azulada se aplasta como goma")
def _(d):
    return P(RX, [rx(), IMG("cartilago", ancho=520, x=540, z=0.5, keys=cae(0.0, 0.6, 600, 1150)), brillo(540, 1150, 400, "#7ec8ff", 0.4, 0.07)],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[rotulo(0.3, d - 0.05, "CARTÍLAGO", tam=104, color="#141414", capsula="#7ec8ffe6", y=560)], sfx=[(0.4, "golpe", -18)])


@v.plano(31, "con los años se endurecen: el cartílago se vuelve hueso")
def _(d):
    return P(RX, [rx(), IMG("cartilago", ancho=460, x=540, y=1150, z=0.5, keys=[{"t": 0, "op": 1}, {"t": d * 0.6, "op": 0, "ease": "suave"}]),
             IMG("femur", ancho=300, x=540, y=1150, z=0.51, keys=[{"t": 0, "op": 0, "rot": 90, "escala": 0.7}, {"t": d * 0.6, "op": 1, "escala": 1.0, "ease": "salida"}, {"t": d, "rot": 96}])],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[amarillo(0.15, d - 0.03, "SE ENDURECEN", y=560, tam=100, color="#ffd23f")], sfx=[(d * 0.5, "brillo", -18)])


@v.plano(36, "y se pegan entre sí: otras dos piezas se sueldan")
def _(d):
    return P(RX, [rx(), *pegar(d * 0.45, 540, 1250, d), IMG("cartilago", ancho=200, x=540, y=1000, z=0.4, op=0.5, anim={"flotar": [16, 0.5]})],
             cam(1.35, 1.45, (540, 1180)), "corte", sfx=[(d * 0.45, "golpe", -15)])


@v.plano(41, "¿la prueba? el cráneo de bebé cae desde arriba")
def _(d):
    return P(RX, [rx(), IMG("craneo_bebe", ancho=760, x=540, z=0.5, keys=cae(0.0, 0.55, 500, 1150))],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[amarillo(0.05, d - 0.03, "¿LA PRUEBA?", y=560, tam=110, color=CIAN)], sfx=[(0.35, "golpe", -16)])


@v.plano(43, "la cabeza de un bebé: de cerca, el bebé respira")
def _(d):
    return P(CUARTO, [BG("bg_cuarto_bebe"), IMG("bebe", ancho=1500, x=760, y=1350, z=0.5, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.04, "ease": "suave"}])],
             cam(1.0, 1.05, (500, 1250)), "corte", sfx=[(0.1, "pop", -24)])


@v.plano(48, "tiene zonas blandas, las fontanelas: el anillo marca la zona rosada")
def _(d):
    return P(RX, [rx(), IMG("craneo_bebe", ancho=800, x=540, y=1150, z=0.5), senala(540, 960, 0.2, d - 0.1, 130, MAGENTA)],
             cam(1.0, 1.1, (540, 1150), (540, 1050)), "corte", hud=[rotulo(0.3, d - 0.05, "FONTANELAS", tam=100, color="#ffffff", capsula="#c0397ae6", y=560)], sfx=[(0.2, "pop", -18)])


@v.plano(53, "donde el cráneo aún no se ha cerrado: las placas separadas, de muy cerca")
def _(d):
    return P(RX, [rx(), IMG("craneo_bebe", ancho=800, x=540, y=1150, z=0.5, keys=[{"t": 0, "rot": -3}, {"t": d, "rot": 3, "ease": "suave"}]),
             flecha([[300, 1150], [470, 1150]], 0.1, d * 0.6, CIAN, 8, z=0.6), flecha([[780, 1150], [610, 1150]], 0.1, d * 0.6, CIAN, 8, z=0.6)],
             cam(1.6, 1.7, (540, 1000)), "corte", sfx=[(0.1, "roce", -22)])


@v.plano(61, "durante el primer año: rótulo de un año y el cráneo gira")
def _(d):
    return P(CUARTO, [BG("bg_cuarto_bebe"), IMG("craneo_bebe", ancho=640, x=540, y=1200, z=0.5, keys=[{"t": 0, "rot": -10}, {"t": d, "rot": 10, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[rotulo(0.1, d - 0.05, "PRIMER AÑO", tam=110, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "ding", -20)])


@v.plano(68, "el hueso las va tapando: las placas se cierran")
def _(d):
    return P(RX, [rx(), IMG("craneo_bebe", ancho=800, x=540, y=1150, z=0.5, keys=[{"t": 0, "op": 1}, {"t": d * 0.75, "op": 0, "ease": "suave"}]),
             IMG("craneo_cerrado", ancho=800, x=540, y=1150, z=0.51, keys=[{"t": 0, "op": 0}, {"t": d * 0.75, "op": 1, "ease": "suave"}])],
             cam(1.2, 1.1, (540, 1100)), "corte", sfx=[(0.1, "roce", -20), (d * 0.75, "golpe", -20)])


@v.plano(73, "y casi todos los demás se sueldan antes de llegar a adulto: el esqueleto de bebé crece hasta adulto")
def _(d):
    return P(RX, [rx(), esq("esqueleto_bebe", 300, 540, 1400, 0.5, keys=[{"t": 0, "op": 1, "escala": 1.0}, {"t": d * 0.6, "op": 0, "escala": 1.3, "ease": "suave"}]),
             esq("esqueleto", 380, 540, 1230, 0.51, keys=[{"t": 0, "op": 0, "escala": 0.75}, {"t": d * 0.6, "op": 1, "escala": 1.0, "ease": "suave"}, {"t": d, "escala": 1.02}])],
             cam(1.0, 1.04, (540, 1100)), "corte", hud=[amarillo(d * 0.5, d - 0.03, "ADULTO", y=560, tam=120, color="#ffd23f")], sfx=[(0.1, "subida", -18, {"dur": 1.2})])


@v.plano(85, "¿y dónde está la mayoría? el esqueleto gira un poco")
def _(d):
    return P(RX, [rx(), esq(keys=[{"t": 0, "rot": -3}, {"t": d, "rot": 3, "ease": "suave"}])],
             cam(1.0, 1.04, (540, 1100)), "corte", hud=[amarillo(0.05, d - 0.03, "¿LA MAYORÍA?", y=560, tam=110, color=CIAN)], sfx=[(0.1, "pop", -20)])


@v.plano(90, "en tus manos y tus pies: anillos sobre manos y pies")
def _(d):
    return P(RX, [rx(), esq(), senala(412, 1215, 0.05, d - 0.1, 80, LIMA), senala(668, 1215, 0.1, d - 0.1, 80, LIMA),
             senala(470, 1700, 0.25, d - 0.1, 70, AMBAR), senala(610, 1700, 0.3, d - 0.1, 70, AMBAR)],
             cam(1.0, 1.04, (540, 1300)), "corte", sfx=[(0.05, "pop", -18), (0.25, "pop", -18)])


@v.plano(96, "cada mano tiene veintisiete huesos: la mano enorme y la cifra")
def _(d):
    return P(RX, [rx(), IMG("mano_rx", ancho=900, x=540, y=1180, z=0.5, keys=arranque(540, 1180, d, "abajo", 200, 20))],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[contador(0.1, d - 0.03, 0, 27, d * 0.6, " HUESOS", y=560, tam=110, color="#ffd23f")], sfx=[(0.1, "tictac", -22, {"dur": 0.5, "ritmo": 0.06})])


@v.plano(101, "cada pie, veintiséis: el pie entra por la derecha")
def _(d):
    return P(RX, [rx(), IMG("pie_rx", ancho=900, x=540, y=1180, z=0.5, keys=arranque(540, 1180, d, "derecha", 240, 20))],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[rotulo(0.1, d - 0.05, "26", tam=150, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "whoosh", -20, {"dur": 0.4})])


@v.plano(104, "ciento seis en total: dos manos y dos pies juntos")
def _(d):
    return P(RX, [rx(), IMG("mano_rx", ancho=420, x=300, y=950, z=0.5, keys=aparece(0.0)), IMG("mano_rx", ancho=420, x=780, y=950, z=0.5, ex=-1, keys=aparece(0.1)),
             IMG("pie_rx", ancho=420, x=300, y=1500, z=0.5, keys=aparece(0.2)), IMG("pie_rx", ancho=420, x=780, y=1500, z=0.5, ex=-1, keys=aparece(0.3))],
             cam(1.0, 1.04, (540, 1200)), "corte", hud=[contador(0.05, d - 0.03, 0, 106, d * 0.6, "", y=560, tam=150, color="#ffd23f")], sfx=[(0.05, "pop", -20), (0.25, "pop", -20)])


@v.plano(108, "más de la mitad de tu esqueleto: barra que se llena por encima de la mitad")
def _(d):
    return P(RX, [rx(), esq(x=330),
             {"tipo": "forma", "forma": "redondeado", "ancho": 140, "alto": 900, "relleno": "#0a1a30", "x": 800, "y": 1150, "z": 0.5},
             {"tipo": "forma", "forma": "redondeado", "ancho": 120, "alto": 470, "relleno": LIMA, "x": 800, "y": 1365, "z": 0.51,
              "keys": [{"t": 0, "ey": 0.02}, {"t": d * 0.6, "ey": 1.0, "ease": "salida"}]},
             flecha([[680, 1150], [920, 1150]], 0.1, 0.5, "#ffffffcc", 5, disc=[14, 10], punta=False, z=0.6)],
             cam(1.0, 1.04, (540, 1150)), "corte", hud=[rotulo(0.3, d - 0.05, "MÁS DE LA MITAD", tam=90, color="#141414", capsula="#b8ff3ae6", y=560)], sfx=[(0.1, "subida", -20, {"dur": 0.8})])


@v.plano(115, "el más largo es el fémur: el fémur gira y se planta en vertical")
def _(d):
    return P(RX, [rx(), brillo(540, 1150, 500, "#7ec8ff", 0.4, 0.07), IMG("femur", ancho=360, x=540, y=1180, z=0.5, keys=[{"t": 0, "rot": -90, "escala": 0.7}, {"t": 0.45, "rot": 0, "escala": 1.0, "ease": "elastico"}, {"t": d, "rot": 3}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[rotulo(0.3, d - 0.05, "FÉMUR", tam=130, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "whoosh", -18, {"dur": 0.4})])


@v.plano(121, "el del muslo: el esqueleto con el fémur señalado")
def _(d):
    return P(RX, [rx(), esq(), senala(497, 1365, 0.1, d - 0.1, 90, AMBAR), senala(583, 1365, 0.15, d - 0.1, 90, AMBAR)],
             cam(1.3, 1.4, (540, 1330)), "corte", sfx=[(0.1, "pop", -20)])


@v.plano(124, "casi un cuarto de tu altura: corchete de altura y del fémur")
def _(d):
    return P(RX, [rx(), esq(),
             flecha([[800, 700], [800, 1720]], 0.05, d * 0.5, "#ffffffcc", 6, z=0.6), flecha([[680, 1258], [680, 1476]], d * 0.4, d * 0.8, AMBAR, 10, z=0.6)],
             cam(1.0, 1.04, (540, 1100)), "corte", hud=[rotulo(d * 0.4, d - 0.05, "≈ 1/4", tam=140, color="#141414", capsula="#ffb03ae6", y=560)], sfx=[(0.1, "trazo", -20), (d * 0.45, "pop", -18)])


@v.plano(130, "¿y el más pequeño? la lupa baja sobre la cabeza")
def _(d):
    return P(RX, [rx(), esq(), IMG("lupa2", ancho=360, z=0.7, keys=[{"t": 0, "x": 820, "y": 1400}, {"t": d, "x": 600, "y": 520, "ease": "suave"}])],
             cam(1.0, 1.2, (540, 1100), (540, 700)), "corte", hud=[amarillo(0.05, d - 0.03, "¿EL MÁS PEQUEÑO?", y=1500, tam=90, color=CIAN)], sfx=[(0.1, "roce", -20)])


@v.plano(134, "el estribo: el huesecillo aparece enorme")
def _(d):
    return P(RX, [rx(), brillo(540, 1100, 420, "#ffd23f", 0.4, 0.07), IMG("estribo", ancho=620, x=540, y=1150, z=0.5, keys=aparece(0.0, 0.4) + [{"t": d, "rot": 6}])],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[rotulo(0.08, d - 0.03, "ESTRIBO", tam=120, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "pop", -16)])


@v.plano(136, "escondido dentro de tu oído: el corte de la oreja y el estribo marcado")
def _(d):
    return P(["#2a1a24", "#120a10"], [brillo(540, 1100, 600, "#ffb0a0", 0.3, 0.06), IMG("oreja_corte", ancho=1000, x=540, y=1150, z=0.5), senala(755, 1110, 0.3, d - 0.1, 70, LIMA)],
             cam(1.0, 1.35, (540, 1150), (720, 1120)), "corte", sfx=[(0.3, "pop", -18)])


@v.plano(141, "como un grano de arroz: el estribo y el grano lado a lado")
def _(d):
    return P(RX, [rx(), IMG("estribo", ancho=330, x=330, y=1150, z=0.5), IMG("grano_arroz", ancho=230, x=760, y=1150, z=0.5, keys=cae(0.0, 0.5, 700, 1150))],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[amarillo(0.3, d - 0.03, "UN GRANO DE ARROZ", y=560, tam=90, color="#ffd23f")], sfx=[(0.35, "golpe", -20)])


@v.plano(146, "así que de bebé tenías casi cien huesos más: el bebé vuelve y el adulto se aparta (bucle)")
def _(d):
    return P(RX, [rx(), esq("esqueleto", 380, 800, 1230, 0.45, op=0.6, keys=[{"t": 0, "x": 760}, {"t": d, "x": 860, "ease": "suave"}]),
             esq("esqueleto_bebe", 420, 440, 1325, 0.5, keys=[{"t": 0, "escala": 0.9}, {"t": 0.4, "escala": 1.0, "ease": "elastico"}, {"t": d, "escala": 1.05}])],
             cam(1.0, 1.04, (540, 1100)), "corte", hud=[rotulo(0.3, d - 0.45, "≈ 100 MÁS", tam=120, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "impacto", -16), (d * 0.6, "ding", -22)])


v.construir("2026-11-19-tarde-02-naciste-300-huesos", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 43, "db": -13},
            claves=["trescientos", "huesos", "doscientos", "seis", "soldado", "cartílago", "endurecen", "fontanelas", "cráneo", "primer", "año", "adulto",
                    "manos", "pies", "veintisiete", "veintiséis", "Ciento", "mitad", "fémur", "cuarto", "estribo", "oído", "arroz", "cien"])
