"""02 · Tu sangre viene de estrellas (nucleosíntesis: hierro, carbono, oxígeno, calcio; hidrógeno del Big Bang; oro de estrellas
de neutrones) — método denso. Lote 2026-11-22-manana (Agente 08:00, Nico). Experimento del lote: gancho en segunda persona (H3).
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import math, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_1122m  # noqa: E402

SVG = ilus_1122m.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

OSC = ESPACIO


def bola(x, y, r, col, keys=None, z=0.55):
    return {"tipo": "forma", "forma": "circulo", "radio": r, "relleno": col, "x": x, "y": y, "z": z, "keys": keys or []}


def nucleo(x0, y0, x1, y1, r, col, t0, t1, z=0.55):
    """Núcleo que viaja de (x0,y0) a (x1,y1) y desaparece al chocar en t1."""
    return [brillo(x0, y0, r * 2.2, col, 0.6, z - 0.01, keys=[{"t": 0, "x": x0, "y": y0}, {"t": t1, "x": x1, "y": y1, "ease": "entrada"}, {"t": t1 + 0.05, "op": 0}]),
            bola(x0, y0, r, col, [{"t": 0, "x": x0, "y": y0, "op": 1}, {"t": t0, "x": x0, "y": y0}, {"t": t1, "x": x1, "y": y1, "ease": "entrada"}, {"t": t1 + 0.04, "op": 0}], z)]


def fusion(d, a, b, res, ta=0.65):
    a, b, res = (a[0], a[1] * 1.7), (b[0], b[1] * 1.7), (res[0], res[1] * 1.7)
    """Dos núcleos (a, b = (color, radio)) chocan en el centro y sale uno más grande (res) con un destello."""
    t1 = min(ta, d * 0.55)
    return (nucleo(220, 1000, 540, 1000, a[1], a[0], 0.05, t1) + nucleo(860, 1000, 540, 1000, b[1], b[0], 0.05, t1)
            + [brillo(540, 1000, 300, "#ffffff", 0.9, 0.6, keys=[{"t": 0, "op": 0}, {"t": t1, "op": 1}, {"t": t1 + 0.35, "op": 0}]),
               bola(540, 1000, res[1], res[0], aparece(t1, 0.35), 0.62), brillo(540, 1000, res[1] * 2.4, res[0], 0.6, 0.6, keys=[{"t": 0, "op": 0}, {"t": t1, "op": 1}])])


# ================================================================== PLANOS
@v.plano(0, "gancho: una gota de sangre sale disparada de una estrella que explota")
def _(d):
    return P(OSC, [BG("bg_esp_ambar"), IMG("supernova", ancho=1300, x=540, y=760, z=0.2, keys=[{"t": 0, "escala": 0.55, "rot": 0}, {"t": d, "escala": 1.0, "rot": 20, "ease": "salida"}]),
                   IMG("gota_sangre", ancho=420, x=540, z=0.6, keys=[{"t": 0, "y": 820, "escala": 0.55, "rot": -12}, {"t": 0.45, "y": 1060, "escala": 1.0, "rot": 0, "ease": "elastico"},
                                                                     {"t": d, "y": 1100, "escala": 1.08, "rot": 6, "ease": "suave"}]),
                   estrellas(50, 1)],
             cam(1.0, 1.12, (540, 1000)), vineta=0.5, sfx=[(0.02, "impacto", -12), (0.3, "brillo", -18)])


@v.plano(5, "su hierro: glóbulos rojos que pasan con el rótulo del hierro")
def _(d):
    els = [brillo(540, 1000, 700, "#ff2a2a", 0.35, 0.05)]
    for k, (x, y, s) in enumerate([(300, 760, 300), (760, 980, 380), (420, 1240, 340), (860, 1360, 260), (180, 1080, 220)]):
        els.append(IMG("globulo", ancho=s, x=x, y=y, z=0.4 + k * 0.03, keys=[{"t": 0, "x": x + 160, "rot": k * 20}, {"t": d, "x": x - 160, "rot": k * 20 + 30, "ease": "lineal"}]))
    return P(["#3a0408", "#12000a"], els, cam(1.0, 1.05, (540, 1000)), "corte",
             hud=[rotulo(0.05, d - 0.02, "HIERRO", tam=110, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "burbuja", -20), (0.4, "burbuja", -22)])


@v.plano(9, "se fabricó dentro de una estrella: una supergigante roja crece en pantalla")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), IMG("estrella_roja", ancho=900, x=540, y=1000, z=0.4, keys=[{"t": 0, "escala": 0.6}, {"t": d, "escala": 1.0, "ease": "salida"}]),
                   brillo(540, 1000, 600, "#ff6a2a", 0.4, 0.35, pulso=[0.08, 1.2])],
             cam(1.0, 1.05, (540, 1000)), "desenfoque", sfx=[(0.1, "rumor", -18, {"dur": min(1.6, d)})])


@v.plano(13, "que explotó: la estrella revienta en un fogonazo")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), IMG("supernova", ancho=1200, x=540, y=1000, z=0.4, keys=[{"t": 0, "escala": 0.2, "rot": 0}, {"t": 0.4, "escala": 1.0, "ease": "golpe"}, {"t": d, "escala": 1.1, "rot": 15}]),
                   fundido_blanco([{"t": 0, "op": 0.9}, {"t": 0.35, "op": 0}])],
             cam(1.0, 1.08, (540, 1000), temblor=6), "corte", hud=[amarillo(0.3, d - 0.05, "¡EXPLOTÓ!", y=560, tam=120, color=AMBAR)], sfx=[(0.0, "impacto", -10)])


@v.plano(15, "¿cómo?: la estrella cortada por capas gira despacio")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), IMG("estrella_capas", ancho=820, x=540, y=1000, z=0.45, keys=aparece(0.0) + [{"t": 0.4, "rot": 0}, {"t": d, "rot": 25}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[amarillo(0.1, d - 0.05, "¿CÓMO?", y=1000, tam=150, color="#ffffff")], sfx=[(0.05, "roce", -18)])


@v.plano(16, "una estrella es un horno: el Sol hierve y late")
def _(d):
    return P(OSC, [BG("bg_esp_ambar"), *sol(540, 1000, 300, 0.4)],
             cam(1.0, 1.08, (540, 1000)), "corte", hud=[rotulo(0.3, d - 0.03, "UN HORNO", tam=110, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "rumor", -16, {"dur": d})])


@v.plano(21, "que aprieta átomos pequeños hasta pegarlos: dos núcleos chocan y se funden")
def _(d):
    return P(OSC, [BG("bg_esp_ambar", z=0.03), brillo(540, 1000, 700, "#ff8a3a", 0.3, 0.05), *fusion(d, ("#2ff3ff", 50), ("#2ff3ff", 50), ("#ffe93d", 80), ta=1.4),
                   flecha([[180, 1150], [480, 1050]], 0.05, 1.2, CIAN, 6, z=0.5), flecha([[900, 1150], [600, 1050]], 0.05, 1.2, CIAN, 6, z=0.5)],
             cam(1.0, 1.1, (540, 1000)), "corte", hud=[amarillo(0.2, d - 0.05, "¡APRIETA!", y=560, tam=110, color=AMBAR)], sfx=[(1.35, "golpe", -12), (1.35, "brillo", -18)])


@v.plano(27, "con hidrógeno hace helio: H + H → He")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo", z=0.03), *fusion(d, ("#2ff3ff", 46), ("#2ff3ff", 46), ("#ffe93d", 76))],
             cam(1.0, 1.04, (540, 1000)), "corte",
             hud=[rotulo(0.05, d * 0.55, "H", tam=90, color=CIAN, capsula="#000000a0", x=220, y=1180), rotulo(0.05, d * 0.55, "H", tam=90, color=CIAN, capsula="#000000a0", x=860, y=1180),
                  rotulo(d * 0.55, d - 0.03, "HELIO", tam=100, color="#141414", capsula="#ffe93de6", y=560)], sfx=[(min(0.65, d * 0.55), "golpe", -14)])


@v.plano(31, "con helio hace carbono: helio + helio → carbono gris")
def _(d):
    return P(OSC, [BG("bg_esp_violeta", z=0.03), estrellas(40, 6), *fusion(d, ("#ffe93d", 56), ("#ffe93d", 56), ("#9aa4b4", 92))],
             cam(0.8 + 0.5, 1.4, (540, 1000)), "corte", hud=[rotulo(d * 0.5, d - 0.03, "CARBONO", tam=100, color="#141414", capsula="#c8d0dce6", y=560)],
             sfx=[(min(0.65, d * 0.55), "golpe", -14)])


@v.plano(35, "y oxígeno: carbono + helio → oxígeno rojo")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo", z=0.03), *fusion(d, ("#9aa4b4", 60), ("#ffe93d", 46), ("#ff5a5a", 100), ta=0.35)],
             cam(1.0, 1.02, (540, 1000)), "corte", hud=[rotulo(0.3, d - 0.03, "OXÍGENO", tam=100, color="#141414", capsula="#ff8a8ae6", y=560)],
             sfx=[(0.3, "golpe", -14)])


@v.plano(37, "los mismos que forman la mayor parte de tu cuerpo: una persona se ilumina por dentro")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), brillo(540, 1000, 420, "#ff5a5a", 0.4, 0.3, pulso=[0.1, 1.0]), brillo(540, 900, 300, "#9aa4b4", 0.35, 0.31),
                   IMG("persona_pie", ancho=420, x=540, y=1040, z=0.45, keys=arranque(540, 1040, d, "abajo", 140, 20))],
             cam(1.0, 1.05, (540, 1000)), "corte",
             hud=[rotulo(0.1, d - 0.03, "LA MAYOR PARTE", tam=74, color="#141414", capsula="#2ff3ffe6", y=560)], sfx=[(0.2, "brillo", -18)])


@v.plano(44, "de tu cuerpo: la cara de perfil se ilumina con puntos rojos y grises")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), IMG("cara_perfil", ancho=760, x=520, y=1080, z=0.45, keys=[{"t": 0, "x": 560}, {"t": d, "x": 500, "ease": "suave"}]),
                   polvo("#ff5a5a", 25, (300, 800, 800, 1400), 3), polvo("#c8d0dc", 25, (300, 800, 800, 1400), 4)],
             cam(1.0, 1.06, (520, 1050)), "corte", hud=[amarillo(0.1, d - 0.05, "TU CUERPO", y=560, tam=110, color=CIAN)], sfx=[(0.1, "brillo", -20)])


@v.plano(47, "las más grandes siguen hasta llegar al hierro: zoom al centro de la estrella por capas")
def _(d):
    return P(OSC, [BG("bg_esp_ambar"), IMG("estrella_capas", ancho=1000, x=540, y=1000, z=0.45, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 30}]),
                   senala(540, 1000, d * 0.55, d - 0.1, 130, CIAN)],
             cam(1.0, 1.8, (540, 1000)), "corte", hud=[rotulo(d * 0.5, d - 0.03, "HIERRO", tam=100, color="#141414", capsula="#c8d0dce6", y=560)],
             sfx=[(0.05, "subida", -20, {"dur": d * 0.7})])


@v.plano(55, "y ahí se acaba el combustible: la estrella se apaga y oscurece")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), IMG("estrella_roja", ancho=820, x=540, y=1000, z=0.45, keys=[{"t": 0, "op": 1}, {"t": d, "op": 0.35, "escala": 0.92}]),
                   brillo(540, 1000, 600, "#ff6a2a", 0.5, 0.4, keys=[{"t": 0, "op": 1}, {"t": d, "op": 0}])],
             cam(1.0, 1.04, (540, 1000)), "corte", sfx=[(0.1, "roce", -20)])


@v.plano(58, "se acaba el combustible: la estrella casi apagada")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), IMG("estrella_roja", ancho=760, x=540, y=1000, z=0.45, op=0.35, keys=[{"t": 0, "escala": 0.92}, {"t": d, "escala": 0.88}])],
             cam(1.06, 1.1, (540, 1000)), "corte", hud=[amarillo(0.05, d - 0.03, "SIN COMBUSTIBLE", y=560, tam=96, color="#ff8a5a")])


@v.plano(61, "la estrella: la estrella tiembla antes de caer")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), IMG("estrella_roja", ancho=820, x=540, y=1000, z=0.45, keys=late(0.0, 2, 0.04, 0.25)), polvo("#ffb04a", 30, (200, 600, 880, 1400), 6)],
             cam(1.5, 1.6, (600, 950), temblor=4), "corte", sfx=[(0.0, "rumor", -16, {"dur": d})])


@v.plano(63, "se derrumba: se encoge de golpe")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), IMG("estrella_roja", ancho=820, x=540, y=1000, z=0.45, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 0.15, "ease": "entrada"}]),
                   brillo(540, 1000, 200, "#ffffff", 0.6, 0.5, keys=[{"t": 0, "op": 0}, {"t": d, "op": 1}])],
             cam(1.0, 1.06, (540, 1000), temblor=5), "corte", sfx=[(0.0, "subida", -14, {"dur": d})])


@v.plano(65, "y revienta en una supernova: la explosión llena la pantalla")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), IMG("supernova", ancho=1400, x=540, y=1000, z=0.45, keys=[{"t": 0, "escala": 0.1, "rot": 0}, {"t": 0.5, "escala": 1.1, "ease": "golpe"}, {"t": d, "escala": 1.25, "rot": 25}]),
                   fundido_blanco([{"t": 0, "op": 1}, {"t": 0.4, "op": 0}])],
             cam(1.0, 1.06, (540, 1000), temblor=8), "corte", hud=[rotulo(0.5, d - 0.03, "SUPERNOVA", tam=110, color="#141414", capsula="#ff3df2e6", y=560)],
             sfx=[(0.0, "impacto", -8), (0.05, "golpe", -12)])


@v.plano(70, "que siembra esos átomos por la galaxia: trazos que salen disparados del centro")
def _(d):
    els = [BG("bg_esp_petroleo"), IMG("supernova", ancho=500, x=540, y=1000, z=0.3, op=0.7)]
    cols = [CIAN, MAGENTA, LIMA, AMBAR]
    for k in range(10):
        a = math.radians(k * 36 + 8)
        p1 = (540 + 520 * math.cos(a), 1000 + 640 * math.sin(a))
        els.append(flecha([[540 + 120 * math.cos(a), 1000 + 120 * math.sin(a)], list(p1)], 0.05 + k * 0.04, d * 0.8, cols[k % 4], 5, z=0.5))
    return P(OSC, els, cam(1.06, 1.0, (540, 1000)), "corte", hud=[amarillo(0.3, d - 0.05, "POR LA GALAXIA", y=560, tam=96, color=LIMA)], sfx=[(0.05, "whoosh", -14)])


@v.plano(77, "mucho tiempo después: la galaxia en calma, una estrella fugaz")
def _(d):
    return P(OSC, [BG("bg_esp_ambar"), estrellas(80, 4), fugaz(0.1, 900, 500, 300, 900)],
             cam(1.1, 1.0, (540, 960)), "desenfoque", hud=[rotulo(0.2, d - 0.03, "MUCHO DESPUÉS", tam=86, color="#ffffff", capsula="#000000b0", y=560)])


@v.plano(80, "con ese polvo se formaron el Sol: el disco de polvo gira y en el centro nace el Sol")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), IMG("disco_proto", ancho=1150, x=540, y=1000, z=0.45, keys=[{"t": 0, "escala": 0.85, "rot": -4}, {"t": d, "escala": 1.05, "rot": 4, "ease": "suave"}]),
                   brillo(540, 1000, 260, "#fff0a0", 0.7, 0.5, pulso=[0.12, 0.8])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[rotulo(d * 0.6, d - 0.03, "EL SOL", tam=100, color="#141414", capsula="#ffe93de6", y=560)], sfx=[(0.1, "brillo", -18)])


@v.plano(87, "la Tierra: la Tierra aparece girando")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), tierra(540, 1000, 700, 0.45, giro=12, keys=aparece(0.0))],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[rotulo(0.1, d - 0.03, "TIERRA", tam=110, color="#141414", capsula="#2ff3ffe6", y=560)], sfx=[(0.05, "pop", -18)])


@v.plano(89, "y, al final, tú: una persona aparece sobre la Tierra")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), tierra(540, 1750, 1400, 0.3, giro=4), brillo(540, 900, 380, "#fff0c0", 0.4, 0.35),
                   IMG("persona_pie", ancho=360, x=540, y=930, z=0.5, keys=aparece(0.15, 0.5))],
             cam(1.0, 1.08, (540, 1000)), "corte", sfx=[(0.15, "brillo", -16)])


@v.plano(92, "tú: la persona de cerca con un brillo")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), brillo(540, 900, 420, "#2ff3ff", 0.5, 0.35), IMG("persona_pie", ancho=600, x=540, y=1150, z=0.5), estrellas(40, 12)],
             cam(1.2, 1.3, (540, 900)), "corte", hud=[rotulo(0.0, d - 0.02, "TÚ", tam=160, color=CIAN, capsula=None, y=560, sin_pop=True)], sfx=[(0.0, "golpe", -16)])


@v.plano(93, "el calcio de tus huesos: un fémur grande gira con brillo")
def _(d):
    return P(["#0a1020", "#02040a"], [brillo(540, 1000, 500, "#e8f0ff", 0.3, 0.1),
                                      IMG("femur", ancho=300, x=540, y=1000, z=0.45, keys=aparece(0.0) + [{"t": 0.4, "rot": -30}, {"t": d, "rot": 20, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[rotulo(0.3, d - 0.03, "CALCIO", tam=110, color="#141414", capsula="#ffffffe6", y=560)], sfx=[(0.05, "pop", -18)])


@v.plano(98, "también salió de una estrella: el esqueleto con una estrella brillando detrás")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), IMG("estrella_roja", ancho=700, x=540, y=900, z=0.3, keys=[{"t": 0, "escala": 0.8}, {"t": d, "escala": 1.0}]),
                   IMG("esqueleto", ancho=380, x=540, y=1050, z=0.5, keys=arranque(540, 1050, d, "abajo", 120, 20))],
             cam(1.0, 1.05, (540, 1000)), "corte", sfx=[(0.1, "brillo", -18)])


@v.plano(103, "¿y el hidrógeno?: un átomo de hidrógeno gira")
def _(d):
    return P(["#0a2a4a", "#02101e"], [IMG("atomo", ancho=560, x=540, y=1000, z=0.5, keys=aparece(0.0) + [{"t": 0.4, "rot": 0}, {"t": d, "rot": 90}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[rotulo(0.05, d - 0.02, "HIDRÓGENO", tam=100, color="#141414", capsula="#2ff3ffe6", y=560)], sfx=[(0.05, "pop", -18)])


@v.plano(107, "del agua que bebes: un vaso de agua con burbujas")
def _(d):
    return P(["#0a2a4a", "#02101e"], [brillo(540, 1000, 500, "#7ad0ff", 0.35, 0.1), IMG("vaso_agua", ancho=460, x=540, y=1050, z=0.45, keys=aparece(0.0)),
                                      polvo("#cff4ff", 30, (380, 900, 700, 1300), 5)],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[amarillo(0.2, d - 0.05, "DEL AGUA", y=560, tam=120, color=CIAN)], sfx=[(0.2, "agua", -20, {"dur": 1.0})])


@v.plano(110, "ese es aún más viejo: un átomo de hidrógeno sale del vaso")
def _(d):
    return P(["#0a2a4a", "#02101e"], [IMG("vaso_agua", ancho=460, x=540, y=1250, z=0.4, op=0.6),
                                      IMG("atomo", ancho=420, x=540, z=0.5, keys=[{"t": 0, "y": 1150, "escala": 0.3, "rot": 0}, {"t": 0.6, "y": 850, "escala": 1.0, "ease": "elastico"}, {"t": d, "rot": 60}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[rotulo(0.5, d - 0.03, "AÚN MÁS VIEJO", tam=90, color="#141414", capsula="#7dff3ae6", y=560)], sfx=[(0.1, "brillo", -18)])


@v.plano(115, "nació: un punto de luz en la oscuridad")
def _(d):
    return P(["#000000", "#000000"], [brillo(540, 1000, 60, "#ffffff", 1.0, 0.4, pulso=[0.3, 0.3]), estrellas(15, 13), {"tipo": "forma", "forma": "circulo", "radio": 10, "relleno": "#ffffff", "x": 540, "y": 1000, "z": 0.5, "keys": late(0.0, 2, 0.5, 0.3)}],
             cam(1.0, 1.1, (540, 1000)), "corte", sfx=[(0.0, "subida", -16, {"dur": d})])


@v.plano(118, "en el Big Bang: el punto estalla y lo llena todo")
def _(d):
    return P(["#000000", "#000000"], [estrellas(60, 14), polvo("#fff6e0", 40, (100, 400, 980, 1600), 15), IMG("bigbang", ancho=1500, x=540, y=1000, z=0.4, keys=[{"t": 0, "escala": 0.05, "rot": 0}, {"t": 0.5, "escala": 0.9, "ease": "golpe"}, {"t": d, "escala": 1.2, "rot": 30}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[rotulo(0.05, d - 0.02, "BIG BANG", tam=120, color="#141414", capsula="#ffffffe6", y=560)],
             sfx=[(0.0, "impacto", -12)])


@v.plano(120, "hace casi: el Big Bang se aleja, la cámara retrocede")
def _(d):
    return P(OSC, [BG("bg_esp_ambar"), IMG("bigbang", ancho=900, x=540, y=1000, z=0.3, keys=[{"t": 0, "escala": 1.2}, {"t": d, "escala": 0.6}]), estrellas(50, 16)],
             cam(1.2, 1.0, (540, 1000)), "corte", hud=[rotulo(0.0, d - 0.02, "CASI", tam=130, color="#141414", capsula="#ffe93de6", y=560, sin_pop=True)])


@v.plano(122, "catorce mil millones de años: la cifra corre sobre el universo")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), IMG("bigbang", ancho=500, x=540, y=1150, z=0.3, op=0.5, keys=[{"t": 0, "escala": 0.8}, {"t": d, "escala": 1.1}]), estrellas(60, 8)],
             cam(1.0, 1.05, (540, 1000)), "corte",
             hud=[contador(0.05, d - 0.03, 0, 14000, d * 0.6, "", y=800, tam=150, color=AMBAR), rotulo(0.2, d - 0.03, "MILLONES DE AÑOS", tam=78, color="#141414", capsula="#ffe93de6", y=980)],
             sfx=[(0.05, "tictac", -22, {"dur": d * 0.6, "ritmo": 0.06})])


@v.plano(127, "¿y el oro de un anillo?: un anillo de oro gira y brilla")
def _(d):
    return P(["#1a1206", "#060402"], [brillo(540, 1000, 500, "#ffd23f", 0.4, 0.1, pulso=[0.1, 0.9]),
                                      IMG("anillo_oro", ancho=620, x=540, y=1000, z=0.45, keys=aparece(0.0) + [{"t": 0.4, "rot": -15}, {"t": d, "rot": 15, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[amarillo(0.2, d - 0.05, "¿Y EL ORO?", y=560, tam=120, color="#ffd23f")], sfx=[(0.1, "ding", -18)])


@v.plano(133, "probablemente, del choque: dos estrellas muertas giran una alrededor de la otra")
def _(d):
    def espiral(fase):
        ks = []
        for i in range(13):
            u = i / 12; a = fase + u * 4 * math.pi; r = 330 * (1 - 0.75 * u)
            ks.append({"t": round(d * u, 3), "x": 540 + r * math.cos(a), "y": 1000 + r * 0.55 * math.sin(a), "ease": "lineal"})
        return ks
    return P(OSC, [BG("bg_esp_violeta"), IMG("bola_neutrones", ancho=220, z=0.5, keys=espiral(0)), IMG("bola_neutrones", ancho=220, z=0.5, keys=espiral(math.pi)),
                   brillo(540, 1000, 300, "#7ad0ff", 0.3, 0.4, pulso=[0.1, 0.4])],
             cam(1.0, 1.1, (540, 1000)), "corte", hud=[rotulo(0.3, d - 0.03, "2 ESTRELLAS", tam=100, color="#141414", capsula="#2ff3ffe6", y=560)],
             sfx=[(0.05, "subida", -16, {"dur": d})])


@v.plano(136, "de dos estrellas muertas: el choque estalla y salen chispas doradas")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), IMG("choque", ancho=1300, x=540, y=1000, z=0.45, keys=[{"t": 0, "escala": 0.1, "rot": 0}, {"t": 0.45, "escala": 1.0, "ease": "golpe"}, {"t": d, "escala": 1.15, "rot": 20}]),
                   polvo("#ffd23f", 50, (200, 700, 880, 1300), 9), fundido_blanco([{"t": 0, "op": 0.9}, {"t": 0.3, "op": 0}])],
             cam(1.0, 1.06, (540, 1000), temblor=6), "corte", hud=[rotulo(0.4, d - 0.05, "¡ORO!", tam=130, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.0, "impacto", -10)])


@v.plano(140, "literalmente: la silueta hecha de estrellas aparece en el espacio")
def _(d):
    return P(OSC, [BG("bg_esp_ambar"), IMG("cuerpo_estrellas", ancho=520, x=540, y=1050, z=0.45, keys=arranque(540, 1050, d, "abajo", 160, 20))],
             cam(1.0, 1.05, (540, 1000)), "corte", sfx=[(0.1, "brillo", -16)])


@v.plano(141, "eres polvo de estrellas: la cámara se aleja y la silueta brilla en la galaxia")
def _(d):
    return P(OSC, [BG("bg_esp_ambar"), brillo(540, 1050, 500, "#ff4aa8", 0.35, 0.3, pulso=[0.1, 1.0]), IMG("cuerpo_estrellas", ancho=520, x=540, y=1050, z=0.45),
                   fugaz(0.2, 950, 400, 600, 650), estrellas(60, 17), polvo("#ffb0e0", 30, (150, 500, 930, 1600), 18)],
             cam(1.15, 1.0, (540, 1050)), "corte", hud=[rotulo(0.2, d - 0.03, "POLVO DE ESTRELLAS", tam=80, color="#141414", capsula="#ff3df2e6", y=560)],
             sfx=[(0.1, "impacto", -16)])


avisos = v.construir("2026-11-22-manana-02-sangre-de-estrellas", claves=["SANGRE", "ESTRELLAS", "HIERRO", "SUPERNOVA", "CALCIO", "ORO", "BIG", "BANG"],
                     musica={"generar": "curiosidad", "semilla": 23, "db": -13}, bucle=0.35)
