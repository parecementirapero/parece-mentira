"""01 · Cerca del Sol, y helados (en enero estamos más cerca del Sol) — método denso, estilo del vídeo largo.
Lote 2026-11-28-manana (Agente 08:00 (Nico)). Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import math, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comun_1128m as C  # noqa: E402
from comun_1128m import *  # noqa: E402,F401,F403
import ilus_1128m  # noqa: E402

SVG = ilus_1128m.generar(os.path.join(sys.argv[1], "_svg_lote"))
C.SVG_DIR = SVG
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
ESPACIO = ["#02030a", "#0a1030"]
INV = ["#1a2236", "#0a0e1a"]
VER = ["#4aa8e8", "#ffe6a0"]
CIAN, LIMA, MAGENTA = "#2ff3ff", "#5dff8a", "#ff4ad8"
SX, SY = 420, 1000           # Sol en la órbita
RX, RY, OX = 400, 170, 560   # elipse de la órbita (exagerada)


def fondo_esp():
    return [BG("bg_espacio_orbita"), estrellas(70, 8)]


def orbita(t0=0.0, t1=0.5, color="#ffffff66"):
    pts = [[OX + RX * math.cos(a / 40 * 2 * math.pi), SY + RY * math.sin(a / 40 * 2 * math.pi)] for a in range(41)]
    return flecha(pts, t0, t1, color, 5, disc=[18, 14], punta=False, z=0.2)


def pos(a):   # a en grados: 180 = perihelio (izquierda, junto al Sol), 0 = afelio
    r = math.radians(a)
    return OX + RX * math.cos(r), SY + RY * math.sin(r)


def planeta(x, y, ancho, rot=23, keys=None, z=0.45, eje=True):
    els = [tierra(x, y, ancho, z=z, keys=keys)]
    if eje:
        kk = [{**k} for k in (keys or [])]
        for k in kk:
            k.pop("ancho", None)
        els.append(OB("eje_tierra", x, y, ancho * 0.16, z=z + 0.02, keys=[{"t": 0, "rot": rot}] + kk))
    return els


@v.plano(0, "gancho: la Tierra pegada a un Sol enorme… y nevando en ella; el termómetro baja")
def _(d):
    return P(ESPACIO, fondo_esp() + sol(250, 900, 330) + planeta(800, 980, 380, 23, keys=[{"t": 0, "x": 900}, {"t": d, "x": 780, "ease": "suave"}]) +
             [OB("copo_nieve", 820, 760, 170, z=0.6, keys=[{"t": 0, "rot": 0, "y": 640}, {"t": d, "rot": 90, "y": 820}]),
              OB("termo_frio", 920, 1420, 150, z=0.7, keys=aparece(0.15))],
             cam(1.0, 1.08, (560, 1000)), vineta=0.35, sfx=[(0.0, "whoosh", -16), (0.3, "brillo", -18)])


@v.plano(3, "y helados: muñeco de nieve en plena calle, cae nieve")
def _(d):
    return P(INV, [BG("bg_alpes_nieve"), polvo("#ffffff", 70, (0, 0, 1080, 1700), 3), PZ("muneco_nieve", 540, 1560, 780, keys=aparece(0.0))],
             cam(1.1, 1.2, (540, 1200)), "corte", sfx=[(0.05, "pop", -20)])


@v.plano(5, "en enero estamos más cerca del Sol: la Tierra recorre la órbita y se acerca al Sol")
def _(d):
    x0, y0 = pos(230); x1, y1 = pos(180)
    return P(ESPACIO, fondo_esp() + [orbita(0.0, 0.4)] + sol(SX, SY, 95) + planeta(x0, y0, 150, keys=[{"t": 0, "x": x0, "y": y0}, {"t": d, "x": x1, "y": y1, "ease": "suave"}], eje=False),
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.3, d - 0.05, "ENERO", "#ffffff", "#2a5ae8e6", 120, y=640)], sfx=[(0.1, "whoosh", -20)])


@v.plano(14, "ciento cuarenta y siete millones de kilómetros: regla de luz entre el Sol y la Tierra")
def _(d):
    x1, y1 = pos(180)
    return P(ESPACIO, fondo_esp() + [orbita(0, 0.01)] + sol(SX, SY, 95) + planeta(x1, y1, 150, eje=False) +
             [flecha([[x1 + 70, y1 - 110], [SX - 100, SY - 110]], 0.05, 0.5, CIAN, 9, z=0.7)],
             cam(1.25, 1.3, (300, 1000)), "corte",
             hud=[contador(0.1, d - 0.05, 0, 147, 1.0, " MILLONES KM", tam=86, color="#141414", capsula="#7df9ffe6", y=700, x=540)], sfx=[(0.1, "tic", -18)])


@v.plano(22, "en julio, ciento cincuenta y dos: la Tierra da media vuelta hasta la otra punta")
def _(d):
    x0, y0 = pos(180); x1, y1 = pos(0)
    return P(ESPACIO, fondo_esp() + [orbita(0, 0.01)] + sol(SX, SY, 95) +
             planeta(x0, y0, 150, eje=False, keys=[{"t": 0, "x": x0, "y": y0}, {"t": min(1.2, d * 0.5), "x": OX, "y": SY + RY, "ease": "lineal"}, {"t": min(2.0, d * 0.8), "x": x1, "y": y1, "ease": "suave"}]),
             cam(1.0, 1.04, (540, 1000)), "corte",
             hud=[cap(0.1, min(1.0, d * 0.45), "JULIO", "#141414", "#ffd23fe6", 120, y=640),
                  contador(min(1.0, d * 0.45), d - 0.05, 147, 152, 0.8, " MILLONES KM", tam=86, color="#141414", capsula="#ffd23fe6", y=640, x=540)],
             sfx=[(0.1, "whoosh", -18)])


@v.plano(29, "cinco millones más lejos: la flecha se estira hacia la Tierra lejana")
def _(d):
    x1, y1 = pos(0)
    return P(ESPACIO, fondo_esp() + [orbita(0, 0.01)] + sol(SX, SY, 95) + planeta(x1, y1, 150, eje=False) +
             [flecha([[SX + 120, SY], [x1 - 100, y1]], 0.05, 0.7, AMBAR, 10, z=0.7)],
             cam(1.1, 1.15, (640, 1000)), "corte", hud=[cap(0.3, d - 0.05, "+5 MILLONES", "#141414", "#ffd23fe6", 110, y=700)], sfx=[(0.1, "whoosh", -20)])


@v.plano(33, "y en México, en España o en Nueva York: playa de verano y nombres que aparecen")
def _(d):
    t = [0.05, min(0.75, d * 0.3), min(1.6, d * 0.6)]
    return P(VER, [BG("bg_playa_verano"), OB("sol_verano", 760, 560, 380, z=0.3, keys=late(0.2, 2, 0.06, 0.6))],
             cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[cap(t[0], d - 0.05, "MÉXICO", "#ffffff", "#c0392be6", 96, y=900), cap(t[1], d - 0.05, "ESPAÑA", "#ffffff", "#c0392be6", 96, y=1040),
                  cap(t[2], d - 0.05, "NUEVA YORK", "#ffffff", "#c0392be6", 96, y=1180)], sfx=[(t[0], "pop", -20), (t[1], "pop", -20), (t[2], "pop", -20)])


@v.plano(42, "julio es pleno verano: el termómetro sube al rojo")
def _(d):
    return P(VER, [BG("bg_playa_verano"), OB("termo_calor", 540, 1050, 300, keys=aparece(0.0)),
                   brillo(540, 1380, 220, "#ff5a2a", 0.6, 0.5, keys=late(0.3, 2, 0.12, 0.4))],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[amarillo(0.2, d - 0.05, "VERANO", y=560, tam=130, color="#ff7a2a")], sfx=[(0.1, "subida", -20)])


@v.plano(46, "entonces, ¿por qué hace frío en enero?: ventana de invierno, nieva fuera")
def _(d):
    return P(INV, [BG("bg_ventana_invierno"), polvo("#ffffff", 40, (180, 300, 900, 1100), 5), OB("gorro_lana_a", 540, 1450, 420, keys=cae(0.1, 0.5, 1100, 1450))],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[amarillo(0.2, d - 0.05, "¿POR QUÉ?", y=560, tam=130, color=CIAN)], sfx=[(0.5, "pop", -20)])


@v.plano(53, "porque la distancia casi no importa: la flecha de la distancia se tacha")
def _(d):
    x1, y1 = pos(180)
    return P(ESPACIO, fondo_esp() + sol(SX, SY, 95) + planeta(x1, y1, 150, eje=False) +
             [flecha([[x1 + 70, y1 - 60], [SX - 100, SY - 60]], 0.0, 0.01, CIAN, 9, z=0.6)] + tacha(290, 940, 0.5, 110),
             cam(1.3, 1.35, (300, 1000)), "corte", hud=[cap(0.5, d - 0.05, "CASI NO IMPORTA", "#ffffff", "#c0392be6", 90, y=700)], sfx=[(0.5, "impacto", -20)])


@v.plano(59, "lo que manda es la inclinación: la Tierra se ladea delante de la cámara")
def _(d):
    return P(ESPACIO, fondo_esp() + [tierra(540, 1000, 560, z=0.45), OB("eje_tierra", 540, 1000, 90, z=0.47, keys=[{"t": 0, "rot": 0}, {"t": min(1.2, d * 0.6), "rot": 23, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[amarillo(0.2, d - 0.05, "INCLINACIÓN", y=560, tam=120, color=AMBAR)], sfx=[(0.1, "whoosh", -18)])


@v.plano(65, "la Tierra gira ladeada, unos veintitrés grados: arco de ángulo y contador")
def _(d):
    return P(ESPACIO, fondo_esp() + planeta(540, 1000, 560, 23) +
             [flecha([[540, 560], [540, 640]], 0.0, 0.01, "#ffffff88", 5, disc=[12, 10], punta=False, z=0.6),
              flecha([[540, 600], [565, 602], [590, 610]], 0.1, 0.5, LIMA, 8, z=0.7)],
             cam(1.0, 1.05, (540, 900)), "corte",
             hud=[contador(0.1, d - 0.05, 0, 23, 0.8, "°", tam=150, color="#141414", capsula="#5dff8ae6", y=1500, x=540)], sfx=[(0.1, "tic", -18)])


@v.plano(72, "en diciembre y enero, el norte mira hacia fuera del Sol: el polo norte se inclina hacia fuera")
def _(d):
    return P(ESPACIO, fondo_esp() + sol(130, 1000, 200) + planeta(700, 1000, 460, 23) +
             [flecha([[760, 640], [860, 540]], 0.3, 0.7, CIAN, 10, z=0.7)],
             cam(1.0, 1.05, (600, 1000)), "corte", hud=[cap(0.3, d - 0.05, "NORTE: HACIA FUERA", "#141414", "#7df9ffe6", 84, y=560)], sfx=[(0.3, "whoosh", -20)])


@v.plano(86, "que los rayos llegan bajos, de lado: el haz entra inclinado")
def _(d):
    return P(INV, [BG("bg_alpes_nieve"), OB("haz_oblicuo", 540, 1250, 1080, keys=aparece(0.0))],
             cam(1.0, 1.05, (540, 1250)), "corte", hud=[cap(0.3, d - 0.05, "DE LADO", "#141414", "#ffd23fe6", 110, y=600)], sfx=[(0.1, "brillo", -20)])


@v.plano(93, "repartidos en más suelo: al lado, el haz recto; la mancha inclinada es más larga y floja")
def _(d):
    return P(INV, [BG("bg_alpes_nieve"), OB("haz_vertical", 280, 1200, 560, keys=aparece(0.0)), OB("haz_oblicuo", 800, 1200, 560, keys=aparece(0.15)),
                   flecha([[560, 1420], [1020, 1420]], 0.5, 0.9, AMBAR, 8, z=0.7)],
             cam(1.0, 1.04, (540, 1250)), "corte", hud=[cap(0.5, d - 0.05, "MÁS SUELO", "#141414", "#ffd23fe6", 110, y=700)], sfx=[(0.3, "pop", -22)])


@v.plano(97, "y los días son cortos: el sol hace un arco pequeño y bajo")
def _(d):
    return P(INV, [BG("bg_alpes_nieve"), flecha([[120, 1150], [540, 900], [960, 1150]], 0.0, d * 0.9, "#ffd040aa", 7, disc=[14, 12], punta=False, z=0.3)] +
             [OB("sol_dibujo", 120, 1150, 200, z=0.35, keys=[{"t": 0, "x": 120, "y": 1150}, {"t": d * 0.5, "x": 540, "y": 900, "ease": "lineal"}, {"t": d, "x": 960, "y": 1150, "ease": "lineal"}])],
             cam(1.0, 1.03, (540, 1100)), "corte", hud=[cap(0.3, d - 0.05, "DÍAS CORTOS", "#ffffff", "#2a5ae8e6", 110, y=600)], sfx=[(0.1, "whoosh", -22)])


@v.plano(102, "menos horas de sol, y más flojas: muñeco de nieve y el termómetro azul")
def _(d):
    return P(INV, [BG("bg_alpes_nieve"), polvo("#ffffff", 60, (0, 0, 1080, 1700), 4), PZ("muneco_nieve", 380, 1580, 640), OB("termo_frio", 800, 1150, 240, keys=aparece(0.2))],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[cap(0.4, d - 0.05, "MÁS FLOJAS", "#ffffff", "#2a5ae8e6", 100, y=600)], sfx=[(0.2, "tic", -20)])


@v.plano(109, "mientras, el sur mira de frente al Sol: la cámara baja al polo sur, que brilla")
def _(d):
    return P(ESPACIO, fondo_esp() + sol(130, 1000, 200) + planeta(700, 1000, 460, 23) +
             [brillo(620, 1200, 220, "#ffb040", 0.5, 0.5, keys=late(0.2, 2, 0.12, 0.4)), flecha([[350, 1150], [560, 1200]], 0.2, 0.6, AMBAR, 10, z=0.7)],
             cam(1.1, 1.15, (600, 1050), (600, 1150)), "corte", hud=[cap(0.3, d - 0.05, "SUR: DE FRENTE", "#141414", "#ffd23fe6", 96, y=560)], sfx=[(0.2, "brillo", -18)])


@v.plano(117, "por eso en Argentina, en Chile o en Australia: playa, nombres")
def _(d):
    t = [0.1, min(0.95, d * 0.35), min(1.8, d * 0.65)]
    return P(VER, [BG("bg_playa_verano"), OB("balon_playa", 300, 1500, 260, keys=[{"t": 0, "rot": 0, "y": 1500}, {"t": d * 0.5, "y": 1380, "ease": "salida"}, {"t": d, "y": 1500, "rot": 180, "ease": "entrada"}])],
             cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[cap(t[0], d - 0.05, "ARGENTINA", "#141414", "#ffd23fe6", 96, y=900), cap(t[1], d - 0.05, "CHILE", "#141414", "#ffd23fe6", 96, y=1040),
                  cap(t[2], d - 0.05, "AUSTRALIA", "#141414", "#ffd23fe6", 96, y=1180)], sfx=[(t[0], "pop", -20), (t[1], "pop", -20), (t[2], "pop", -20)])


@v.plano(126, "enero es verano: el termómetro se pone rojo")
def _(d):
    return P(VER, [BG("bg_playa_verano"), OB("termo_calor", 540, 1050, 300, keys=aparece(0.0)), OB("helado", 820, 1300, 220, keys=aparece(0.3))],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[amarillo(0.0, d - 0.02, "ENERO: VERANO", y=560, tam=110, color="#ff7a2a")], sfx=[(0.1, "subida", -20)])


@v.plano(129, "con días largos y calor: el sol hace un arco grande y alto")
def _(d):
    return P(VER, [BG("bg_playa_verano"), flecha([[60, 1200], [540, 380], [1020, 1200]], 0.0, d * 0.9, "#ffd040cc", 7, disc=[14, 12], punta=False, z=0.3),
                   OB("sol_dibujo", 60, 1200, 220, z=0.35, keys=[{"t": 0, "x": 60, "y": 1200}, {"t": d * 0.5, "x": 540, "y": 380, "ease": "lineal"}, {"t": d, "x": 1020, "y": 1200, "ease": "lineal"}])],
             cam(1.0, 1.03, (540, 1000)), "corte", hud=[cap(0.3, d - 0.05, "DÍAS LARGOS", "#141414", "#ffd23fe6", 110, y=1400)], sfx=[(0.1, "whoosh", -22)])


@v.plano(134, "el mismo planeta, con dos estaciones a la vez: arriba nieva, abajo brilla el sol")
def _(d):
    return P(ESPACIO, fondo_esp() + planeta(540, 1000, 600, 23) +
             [OB("copo_nieve", 330, 620, 160, z=0.6, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 120}] + aparece(0.1)),
              OB("sol_dibujo", 760, 1400, 200, z=0.6, keys=aparece(0.4) + late(0.6, 2, 0.08, 0.5))],
             cam(1.0, 1.05, (540, 1000)), "corte",
             hud=[cap(0.1, d - 0.05, "NORTE: FRÍO", "#ffffff", "#2a5ae8e6", 90, y=460), cap(0.4, d - 0.05, "SUR: CALOR", "#141414", "#ffd23fe6", 90, y=1560 if False else 1390, x=380)],
             sfx=[(0.1, "pop", -20), (0.4, "brillo", -20)])


@v.plano(143, "¿en tu país ahora hace frío o calor? (bucle): la Tierra junto al Sol enorme, como al principio")
def _(d):
    return P(ESPACIO, fondo_esp() + sol(250, 900, 330) + planeta(800, 980, 380, 23, keys=[{"t": 0, "x": 860}, {"t": d, "x": 820}]) +
             [OB("termo_frio", 920, 1420, 150, z=0.7)], cam(1.0, 1.06, (560, 1000)), "corte",
             hud=[cap(0.2, d - 0.05, "¿FRÍO O CALOR?", "#141414", "#7df9ffe6", 100, y=560)], sfx=[(0.05, "ding", -20)])


def micro(fondo, els, txt=None, col="#ffffff", cap_f="#c0392be6", sfx="pop"):
    def fn(d):
        return P(fondo, els(d), cam(1.15, 1.3, (540, 1000)), "corte", hud=[cap(0.0, d - 0.02, txt, col, cap_f, 120)] if txt else [], sfx=[(0.01, sfx, -18)])
    return fn


v.plano(11, "micro: el Sol enorme")(micro(ESPACIO, lambda d: fondo_esp() + sol(540, 1000, 380), sfx="brillo"))
v.plano(50, "micro: copo de nieve")(micro(INV, lambda d: [BG("bg_ventana_invierno"), OB("copo_nieve", 540, 1000, 600, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 40}])], sfx="tic"))
v.plano(83, "micro: ¿y qué pasa?")(micro(ESPACIO, lambda d: fondo_esp() + planeta(540, 1000, 700, 23), "¿Y QUÉ PASA?", "#141414", "#ffd23fe6", "impacto"))
v.plano(138, "micro: dos estaciones")(micro(ESPACIO, lambda d: fondo_esp() + planeta(540, 1000, 700, 23), "2 ESTACIONES", "#141414", "#5dff8ae6", "impacto"))


v.construir("2026-11-28-manana-01-cerca-del-sol", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 1281, "db": -13},
            claves=["Sol", "helados", "enero", "cerca", "millones", "kilómetros", "julio", "lejos", "verano", "frío", "distancia", "inclinación",
                    "ladeada", "veintitrés", "grados", "norte", "rayos", "bajos", "suelo", "cortos", "sur", "frente", "calor", "estaciones"],
            ep_extra={"sfx_bajo_voz": True})
