"""01 · Tu vista tiene un agujero (el punto ciego) — método denso. Lote 2026-11-22-tarde (Jorge, con el agente). Mismo estilo que «la imagen al revés» (22-11 mañana).
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]
Del segundo ≈21,7 al ≈31 la pantalla es la prueba del punto ciego (cruz y punto): se deja casi quieta a propósito para que se pueda hacer."""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_1122t  # noqa: E402

SVG = ilus_1122t.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

DIA = ["#5aa0d8", "#3a8a3a"]
OSC = ["#1a0a14", "#06020a"]
CLARO = ["#f4f1ea", "#f4f1ea"]
CORTE = ["#5a3a1a", "#2a1a0a"]


def paisaje(): return BG("bg_paisaje")
def mancha(x=640, y=900, ancho=360, keys=None, **k): return IMG("mancha_negra", ancho=ancho, x=x, y=y, z=0.5, keys=keys or [], **k)
def tarjeta(): return BG("tarjeta_test")


# ================================================================== PLANOS
@v.plano(0, "gancho: el paisaje y un agujero negro que se abre en medio de la vista")
def _(d):
    return P(DIA, [paisaje(), mancha(ancho=420, keys=[{"t": 0, "escala": 0.5, "x": 700, "y": 980}, {"t": 0.4, "escala": 1.0, "ease": "elastico"}, {"t": d, "x": 600, "y": 900, "escala": 1.1, "ease": "suave"}])],
             cam(1.0, 1.08, (560, 950)), vineta=0.5, sfx=[(0.02, "zap", -16), (0.4, "subida", -20, {"dur": 0.8})])


@v.plano(5, "en cada ojo hay un punto ciego: el ojo de cerca con un anillo")
def _(d):
    return P(["#c08a70", "#8a5a40"], [IMG("ojo", ancho=1000, x=540, y=1000, z=0.5, keys=arranque(540, 1000, d, "abajo", 100, 10)), senala(620, 1010, 0.4, d - 0.1, 90, MAGENTA)],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[amarillo(0.3, d - 0.05, "PUNTO CIEGO", y=560, tam=120, color="#ffd23f")], sfx=[(0.4, "pop", -20)])


@v.plano(12, "¿por qué?: el ojo cortado aparece")
def _(d):
    return P(OSC, [IMG("ojo_corte", ancho=900, x=440, y=1000, z=0.5, keys=aparece(0.0))], cam(1.0, 1.05, (540, 1000)), "corte",
             hud=[amarillo(0.1, d - 0.05, "¿POR QUÉ?", y=560, tam=130, color=CIAN)], sfx=[(0.05, "whoosh", -20)])


@v.plano(14, "es el sitio por donde sale el nervio óptico: anillo en la salida del nervio")
def _(d):
    return P(OSC, [IMG("ojo_corte", ancho=900, x=440, y=1000, z=0.5), senala(842, 1000, 0.3, d - 0.1, 90, LIMA)], cam(1.0, 1.35, (540, 1000), (760, 1000)), "corte",
             hud=[rotulo(0.25, d - 0.03, "NERVIO ÓPTICO", tam=96, color="#141414", capsula="#b8ff3ae6", y=560)], sfx=[(0.3, "pop", -20)])


@v.plano(21, "micro: «nervio», la salida del nervio muy de cerca")
def _(d):
    return P(OSC, [IMG("ojo_corte", ancho=900, x=440, y=1000, z=0.5)], cam(2.6, 2.8, (860, 1000)), "corte", sfx=[(0.02, "roce", -20)])


@v.plano(23, "el cable que lleva la imagen al cerebro: trazo del nervio al cerebro")
def _(d):
    return P(OSC, [IMG("ojo_corte", ancho=560, x=280, y=1300, z=0.5), IMG("cerebro", ancho=560, x=760, y=760, z=0.5, keys=aparece(0.3)),
                   flecha([[480, 1300], [620, 1200], [700, 980]], 0.1, d * 0.7, LIMA, 10, z=0.6)],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[amarillo(0.4, d - 0.05, "AL CEREBRO", y=1640 - 250, tam=110, color=LIMA)], sfx=[(0.1, "whoosh", -22)])


@v.plano(31, "ahí no hay ni una sola célula que detecte la luz: la fila de células con un hueco")
def _(d):
    return P(OSC, [IMG("retina_fila", ancho=1080, x=540, y=1050, z=0.4, keys=aparece(0.0)), senala(540, 960, 0.4, d - 0.1, 150, MAGENTA)], cam(1.0, 1.08, (540, 1050)), "corte",
             hud=[rotulo(0.5, d - 0.05, "0 CÉLULAS", tam=110, color="#ffffff", capsula="#c0397ae6", y=560)], sfx=[(0.4, "zap", -20)])


@v.plano(37, "micro: «célula», una célula que detecta la luz brilla")
def _(d):
    return P(OSC, [IMG("celula_luz", ancho=300, x=540, y=1000, z=0.5, keys=late(0.0, 1)), brillo(540, 830, 200, "#7df9ff", 0.6, 0.4)], cam(1.0, 1.08, (540, 1000)), "corte",
             sfx=[(0.02, "brillo", -20)])


@v.plano(42, "¿y por qué no ves una mancha negra?: el paisaje con la mancha")
def _(d):
    return P(DIA, [paisaje(), mancha(keys=late(0.2, 2, 0.08, 0.4))], cam(1.0, 1.06, (560, 950)), "corte",
             hud=[amarillo(0.2, d - 0.05, "¿MANCHA NEGRA?", y=560, tam=110, color="#ffd23f")], sfx=[(0.1, "roce", -20)])


@v.plano(50, "porque tu cerebro la rellena con lo que hay alrededor: la mancha se llena de paisaje")
def _(d):
    return P(DIA, [paisaje(), mancha(keys=[{"t": 0, "op": 1}, {"t": d * 0.8, "op": 0, "escala": 0.6, "ease": "suave"}]),
                   {"tipo": "forma", "forma": "elipse", "ancho": 400, "alto": 400, "relleno": "#ffffff", "op_relleno": 0, "grosor": 6, "borde": CIAN, "x": 600, "y": 900, "z": 0.6,
                    "keys": [{"t": 0.3, "op": 0}, {"t": 0.6, "op": 1}, {"t": d, "op": 1, "escala": 0.8}]}],
             cam(1.0, 1.08, (580, 920)), "corte", hud=[rotulo(0.3, d - 0.05, "LA RELLENA", tam=110, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(0.3, "brillo", -20)])


@v.plano(60, "y con lo que ve el otro ojo: dos ojos que se cubren el hueco")
def _(d):
    return P(["#c08a70", "#8a5a40"], [IMG("ojo", ancho=480, x=290, y=1000, z=0.5, keys=aparece(0.0)), IMG("ojo", ancho=480, x=790, y=1000, z=0.5, keys=aparece(0.15)),
                                      flecha([[290, 1180], [540, 1360], [790, 1180]], 0.3, d * 0.8, LIMA, 8, z=0.6)],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[amarillo(0.4, d - 0.05, "EL OTRO OJO", y=560, tam=110, color=LIMA)], sfx=[(0.1, "pop", -20), (0.25, "pop", -20)])


@v.plano(68, "te lo inventa: el cerebro brilla")
def _(d):
    return P(OSC, [IMG("cerebro", ancho=820, x=540, y=1050, z=0.5, keys=late(0.1, 2, 0.06)), brillo(540, 1050, 500, "#ff3df2", 0.5, 0.4, pulso=[0.15, 0.6])],
             cam(1.0, 1.08, (540, 1050)), "corte", hud=[amarillo(0.05, d - 0.03, "TE LO INVENTA", y=560, tam=110, color=MAGENTA)], sfx=[(0.05, "impacto", -16)])


@v.plano(71, "pruébalo: aparece la prueba (cruz y punto)")
def _(d):
    return P(CLARO, [tarjeta(), fundido_blanco([{"t": 0, "op": 0.8}, {"t": 0.3, "op": 0}])], cam(1.0, 1.0, (540, 960)), "corte",
             hud=[rotulo(0.05, d - 0.03, "PRUÉBALO", tam=120, color="#ffffff", capsula="#c0397ae6", y=560)], sfx=[(0.02, "ding", -18)])


@v.plano(72, "tápate el ojo izquierdo: la mano tapa un ojo, la prueba detrás")
def _(d):
    return P(CLARO, [tarjeta(), IMG("mano_tapa", ancho=300, x=880, y=1520, z=0.6, keys=aparece(0.05) + [{"t": d, "rot": -8}])], cam(1.0, 1.0, (540, 960)), "corte",
             hud=[rotulo(0.05, d - 0.03, "OJO IZQUIERDO", tam=96, color="#ffffff", capsula="#141414e6", y=560)], sfx=[(0.05, "roce", -22)])


@v.plano(77, "y mira fijamente la cruz: anillo sobre la cruz")
def _(d):
    return P(CLARO, [tarjeta(), senala(240, 960, 0.1, d - 0.05, 110, MAGENTA)], cam(1.0, 1.0, (540, 960)), "corte",
             hud=[rotulo(0.2, d - 0.05, "MIRA LA CRUZ", tam=96, color="#ffffff", capsula="#c0397ae6", y=560)], sfx=[(0.1, "pop", -22)])


@v.plano(81, "acércate despacio a la pantalla: la prueba crece despacio")
def _(d):
    return P(CLARO, [tarjeta()], cam(1.0, 1.12, (560, 960)), "corte", hud=[rotulo(0.2, d - 0.05, "ACÉRCATE DESPACIO", tam=86, color="#ffffff", capsula="#141414e6", y=560)])


@v.plano(86, "en algún momento, el punto de la derecha desaparece: la prueba, quieta, para hacerla")
def _(d):
    return P(CLARO, [tarjeta()], cam(1.12, 1.12, (560, 960)), "corte", hud=[rotulo(0.3, d - 0.05, "¿HA DESAPARECIDO?", tam=86, color="#ffffff", capsula="#c0397ae6", y=1500)],
             sfx=[(d - 0.4, "ding", -22)])


@v.plano(95, "este agujero lo descubrió en el siglo diecisiete: el palacio")
def _(d):
    return P(CORTE, [BG("bg_corte")], cam(1.0, 1.1, (540, 900)), "desenfoque", hud=[rotulo(0.3, d - 0.05, "SIGLO XVII", tam=120, color="#141414", capsula="#ffd23fe6", y=560)],
             sfx=[(0.1, "whoosh", -20)])


@v.plano(103, "un francés, Edme Mariotte: un científico de la época con su peluca")
def _(d):
    return P(CORTE, [BG("bg_corte"), IMG("noble2", ancho=460, x=540, y=1350, z=0.5, keys=arranque(540, 1350, d, "derecha", 220, 20))], cam(1.0, 1.05, (540, 1200)), "corte",
             hud=[rotulo(0.4, d - 0.05, "EDME MARIOTTE", tam=96, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "roce", -20)])


@v.plano(107, "lo enseñó en la corte del rey Luis catorce: el salón con dos nobles")
def _(d):
    return P(CORTE, [BG("bg_corte"), IMG("noble", ancho=420, x=330, y=1380, z=0.5, keys=aparece(0.1)), IMG("noble2", ancho=420, x=760, y=1380, z=0.5, ex=-1)],
             cam(1.0, 1.06, (540, 1200)), "corte", hud=[rotulo(0.5, d - 0.05, "LUIS XIV", tam=120, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "ding", -22)])


@v.plano(116, "y dicen que los nobles se quedaron boquiabiertos")
def _(d):
    return P(CORTE, [BG("bg_corte"), IMG("noble", ancho=520, x=330, y=1380, z=0.5, keys=late(0.3, 2, 0.06)), IMG("noble2", ancho=520, x=760, y=1380, z=0.5, ex=-1, keys=late(0.45, 2, 0.06))],
             cam(1.15, 1.25, (540, 1150)), "corte", hud=[amarillo(0.3, d - 0.05, "¡OOOH!", y=560, tam=140, color="#ffd23f")], sfx=[(0.3, "brillo", -20)])


@v.plano(124, "una moneda desaparecía delante de sus ojos: la moneda se desvanece")
def _(d):
    return P(OSC, [brillo(540, 1000, 500, "#ffd23f", 0.4, 0.06), IMG("moneda_antigua", ancho=520, x=540, y=1000, z=0.5, keys=[{"t": 0, "op": 1, "rot": 0}, {"t": d * 0.4, "op": 1}, {"t": d * 0.9, "op": 0, "rot": 40, "escala": 0.8, "ease": "suave"}])],
             cam(1.0, 1.08, (540, 1000)), "corte", hud=[rotulo(0.3, d * 0.9, "¡DESAPARECE!", tam=100, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(d * 0.5, "zap", -18)])


@v.plano(131, "lo raro no es tener el agujero: el paisaje con la mancha que late")
def _(d):
    return P(DIA, [paisaje(), mancha(keys=late(0.1, 2, 0.1, 0.5))], cam(1.05, 1.1, (580, 920)), "corte", sfx=[(0.1, "roce", -20)])


@v.plano(138, "lo raro es que llevas toda la vida sin notarlo: el ojo parpadea y el agujero vuelve (bucle)")
def _(d):
    return P(["#c08a70", "#8a5a40"], [IMG("ojo", ancho=1000, x=540, y=1000, z=0.5, keys=[{"t": 0, "ey": 1}, {"t": d * 0.3, "ey": 0.1}, {"t": d * 0.4, "ey": 1}, {"t": d, "ey": 1}]),
                                      mancha(x=620, y=1010, ancho=200, keys=[{"t": 0, "op": 0}, {"t": d * 0.6, "op": 0}, {"t": d, "op": 1, "escala": 1.3}])],
             cam(1.0, 1.08, (560, 1000)), "corte", hud=[amarillo(0.3, d * 0.55, "SIN NOTARLO", y=560, tam=120, color="#ffd23f")], sfx=[(d * 0.3, "pop", -20), (d * 0.7, "subida", -20, {"dur": d * 0.3})])


v.construir("2026-11-22-tarde-01-punto-ciego", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 81, "db": -13},
            claves=["agujero", "punto", "ciego", "nervio", "óptico", "cerebro", "célula", "luz", "mancha", "rellena", "otro", "inventa", "izquierdo", "cruz",
                    "despacio", "desaparece", "diecisiete", "Mariotte", "Luis", "catorce", "boquiabiertos", "moneda", "notarlo"])
