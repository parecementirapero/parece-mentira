"""03 · Los vikingos no llevaban cuernos — método denso, estilo cartoon. Lote 2026-11-24-tarde (Agente 20:00 (Jorge)).
Experimento del lote: gancho de negación. Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
from comun_1124t import *  # noqa: E402,F401,F403
import ilus_1124t  # noqa: E402

SVG = ilus_1124t.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
PAP = ["#f8eed8", "#e8d4b0"]
FIO = ["#8ac8ff", "#e8f4ff"]
TEA = ["#1a0a10", "#2a1a2a"]
# casco_cuernos: lienzo 900x620; cuernos en (190, 190) y (710, 190) del lienzo


def casco_que_pierde(x, y, ancho, t, d, z=0.5):
    """Casco de disfraz al que se le caen los dos cuernos en el segundo t."""
    k = ancho / 900
    cx1, cy = x + (190 - 450) * k, y + (190 - 310) * k
    cx2 = x + (710 - 450) * k
    w = 300 * k
    return [IMG("casco_sin", ancho=ancho, x=x, y=y, z=z, keys=[{"t": 0, "rot": -10, "y": y + 60}, {"t": 0.25, "rot": 8, "y": y - 20, "ease": "salida"}, {"t": 0.5, "rot": -5, "y": y}, {"t": t, "rot": 3, "ease": "elastico"}, {"t": d, "rot": 0}]),
            IMG("cuerno", ancho=w, x=cx1, y=cy, z=z + 0.01, keys=[{"t": 0, "x": cx1, "y": cy + 60, "rot": -12, "op": 1}, {"t": 0.25, "y": cy - 20, "rot": 10, "ease": "salida"}, {"t": 0.5, "y": cy, "rot": -6}, {"t": t, "x": cx1, "y": cy, "rot": 0, "op": 1}, {"t": t + 0.7, "x": cx1 - 420, "y": cy - 300, "rot": -200, "op": 0, "ease": "salida"}]),
            IMG("cuerno_d", ancho=w, x=cx2, y=cy, z=z + 0.01, keys=[{"t": 0, "x": cx2, "y": cy + 60, "rot": -12, "op": 1}, {"t": 0.25, "y": cy - 20, "rot": 10, "ease": "salida"}, {"t": 0.5, "y": cy, "rot": -6}, {"t": t, "x": cx2, "y": cy, "rot": 0, "op": 1}, {"t": t + 0.7, "x": cx2 + 420, "y": cy - 300, "rot": 200, "op": 0, "ease": "salida"}])]


@v.plano(0, "gancho: el casco con cuernos entra y los cuernos salen disparados")
def _(d):
    return P(FIO, [BG("bg_fiordo"), *casco_que_pierde(540, 1000, 900, min(1.0, d * 0.6), d)],
             cam(1.0, 1.1, (540, 1000)), vineta=0.45, hud=[BANDA()], sfx=[(0.05, "whoosh", -20), (min(1.0, d * 0.6), "zap", -14)])


@v.plano(5, "ese casco es un invento: el vikingo con cuernos y el sello INVENTO")
def _(d):
    return P(FIO, [BG("bg_fiordo"), IMG("vikingo_cuernos", ancho=560, x=540, y=1050, z=0.5, keys=arranque(540, 1050, d, "abajo", 200, 20))],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[BANDA(), {**rotulo(0.5, d - 0.03, "INVENTO", tam=130, color="#ffffff", capsula="#c0392be6", y=700), "rot": -8}], sfx=[(0.5, "impacto", -16)])


@v.plano(10, "el único casco vikingo casi completo que se conoce: el casco real aparece sobre papel")
def _(d):
    return P(PAP, [BG("bg_papel"), IMG("casco_gjermundbu", ancho=780, x=540, y=1050, z=0.5, keys=aparece(0.1) + late(1.2, 1, 0.05))],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[BANDA(), rotulo(0.4, d - 0.05, "EL ÚNICO CASI COMPLETO", tam=72, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "pop", -18)])


@v.plano(19, "apareció en Noruega: un barco vikingo navega por el fiordo")
def _(d):
    return P(FIO, [BG("bg_fiordo"), IMG("drakkar_c", ancho=820, x=540, y=1250, z=0.5, keys=[{"t": 0, "x": 300, "rot": -3}, {"t": d * 0.5, "rot": 3, "ease": "suave"}, {"t": d, "x": 700, "rot": -2, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1100)), "desenfoque", hud=[BANDA(), rotulo(0.2, d - 0.05, "NORUEGA", tam=110, color="#ffffff", capsula="#2a5ae8e6", y=560)], sfx=[(0.1, "ola", -22)])


@v.plano(22, "en mil novecientos cuarenta y tres: excavación, la pala cava y el año corre")
def _(d):
    return P(["#a8d0f0", "#8a5a30"], [BG("bg_excavacion"), IMG("pala", ancho=200, x=700, y=900, z=0.55, keys=[{"t": 0, "y": 820, "rot": 10}, {"t": d * 0.3, "y": 950, "rot": -5, "ease": "salida"}, {"t": d * 0.6, "y": 820, "rot": 10}, {"t": d * 0.9, "y": 950, "rot": -5}]),
                   polvo("#6a3e1e", 30, (500, 900, 900, 1100), 3)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[BANDA(), contador(0.05, d - 0.03, 1900, 1943, 0.6, miles=False, tam=170, color="#141414", capsula="#ffffffe6", x=380, y=1250)], sfx=[(0.3, "golpe", -20), (0.9, "golpe", -20)])


@v.plano(28, "el casco de Gjermundbu: el casco sale de la tierra")
def _(d):
    return P(["#a8d0f0", "#8a5a30"], [BG("bg_excavacion"), IMG("casco_gjermundbu", ancho=640, x=540, y=1050, z=0.5, keys=[{"t": 0, "y": 1350, "op": 0.6}, {"t": d * 0.7, "y": 1050, "op": 1, "ease": "salida"}]),
                   brillo(540, 1050, 380, "#fff4c8", 0.0, 0.45, keys=[{"t": d * 0.5, "op": 0}, {"t": d * 0.8, "op": 1}])],
             cam(1.0, 1.08, (540, 1050)), "corte", hud=[BANDA(), rotulo(0.3, d - 0.05, "GJERMUNDBU", tam=110, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(d * 0.6, "brillo", -18)])


@v.plano(32, "es de hierro: primer plano del metal con óxido")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("casco_gjermundbu", ancho=780, x=540, y=1050, z=0.5)],
             cam(1.3, 1.45, (540, 900)), "corte", hud=[rotulo(0.3, d - 0.05, "HIERRO", tam=130, color="#141414", capsula="#c8ccd8e6", y=560)], sfx=[(0.2, "golpe", -18)])


@v.plano(35, "redondo: anillo alrededor de la cúpula")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("casco_gjermundbu", ancho=780, x=540, y=1050, z=0.5, keys=[{"t": 0, "rot": -3}, {"t": d, "rot": 3}]),
                   flecha([[280, 990], [320, 820], [540, 760], [760, 820], [800, 990]], 0.1, min(0.8, d - 0.1), CIAN, 12, punta=False, z=0.6)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[rotulo(0.05, d - 0.02, "REDONDO", tam=110, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(0.1, "roce", -20)])


@v.plano(36, "con una protección para los ojos y la nariz: zoom a la gafa del casco")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("casco_gjermundbu", ancho=780, x=540, y=1050, z=0.5), senala(540, 1200, 0.4, d - 0.05, 230, AMBAR)],
             cam(1.0, 1.4, (540, 1050), (540, 1200)), "corte", hud=[rotulo(0.5, d - 0.05, "OJOS Y NARIZ", tam=100, color="#141414", capsula="#ffe93de6", y=560)], sfx=[(0.4, "ding", -20)])


@v.plano(45, "ni un solo cuerno: un cuerno intenta pegarse y se tacha")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("casco_gjermundbu", ancho=640, x=540, y=1100, z=0.5),
                   IMG("cuerno", ancho=230, x=300, y=780, z=0.6, keys=[{"t": 0, "x": -100, "y": 600}, {"t": 0.4, "x": 300, "y": 780, "ease": "salida"}]), *tacha(300, 780, 0.5, 130)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[amarillo(0.3, d - 0.05, "NI UNO", y=1400, tam=130, color="#ff3d3d")], sfx=[(0.5, "zap", -16)])


@v.plano(49, "y en una batalla: dos vikingos frente a frente")
def _(d):
    return P(FIO, [BG("bg_fiordo"), IMG("vikingo", ancho=460, x=300, y=1080, z=0.5, keys=[{"t": 0, "x": 200}, {"t": d, "x": 300, "ease": "suave"}]),
                   IMG("vikingo_cuernos", ancho=460, x=780, y=1080, z=0.5, keys=[{"t": 0, "x": 880}, {"t": d, "x": 780, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[BANDA()], sfx=[(0.1, "whoosh", -20)])


@v.plano(53, "unos cuernos serían más un estorbo que una ayuda: el de los cuernos se engancha y se tambalea")
def _(d):
    return P(FIO, [BG("bg_fiordo"), IMG("vikingo", ancho=460, x=300, y=1080, z=0.5),
                   IMG("vikingo_cuernos", ancho=460, x=780, y=1080, z=0.5, keys=[{"t": 0, "rot": 0}, {"t": 0.4, "rot": 12, "ease": "golpe"}, {"t": 0.9, "rot": -6, "ease": "elastico"}, {"t": d, "rot": 0}]),
                   senala(700, 700, 0.3, d - 0.05, 120, "#ff3d3d")],
             cam(1.0, 1.06, (540, 1050), temblor=3), "corte", hud=[BANDA(), rotulo(0.3, d - 0.05, "ESTORBO", tam=120, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.35, "golpe", -16)])


@v.plano(62, "¿entonces de dónde salen?: el casco de cuernos gira con interrogación")
def _(d):
    return P(OSC, [IMG("casco_cuernos", ancho=800, x=540, y=1050, z=0.5, keys=[{"t": 0, "rot": -8}, {"t": d, "rot": 8, "ease": "suave"}]), brillo(540, 1050, 500, "#ffd23f", 0.3, 0.06)],
             cam(1.0, 1.08, (540, 1050)), "corte", hud=[amarillo(0.1, d - 0.05, "¿DE DÓNDE?", y=560, tam=130, color=AMBAR)], sfx=[(0.05, "impacto", -18)])


@v.plano(66, "de la ópera: se abre el telón y entra la luz")
def _(d):
    return P(TEA, [BG("bg_teatro"), brillo(540, 1150, 420, "#fff4c8", 0.0, 0.3, keys=[{"t": 0, "op": 0}, {"t": 0.5, "op": 1}]),
                   IMG("cantante_alas", ancho=440, x=540, y=1100, z=0.5, keys=aparece(0.3))],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[rotulo(0.3, d - 0.05, "LA ÓPERA", tam=120, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.2, "brillo", -18)])


@v.plano(69, "en mil ochocientos setenta y seis: el año corre en el escenario")
def _(d):
    return P(TEA, [BG("bg_teatro"), brillo(540, 1150, 420, "#fff4c8", 0.3, 0.3, pulso=[0.1, 0.4])],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[contador(0.05, d - 0.03, 1850, 1876, 0.6, miles=False, tam=180, color="#141414", capsula="#ffffffe6", y=1100)], sfx=[(0.1, "tic", -18)])


@v.plano(75, "se estrenó El anillo del nibelungo, de Wagner: el telón y un anillo dorado brillando")
def _(d):
    anillo = {"tipo": "forma", "forma": "elipse", "ancho": 300, "alto": 300, "relleno": "#ffffff", "op_relleno": 0, "grosor": 34, "borde": "#ffc83a", "x": 540, "y": 1050, "z": 0.55,
              "keys": aparece(0.2) + [{"t": 0.6, "rot": 0}, {"t": d, "rot": 30}]}
    return P(TEA, [BG("bg_teatro"), anillo, brillo(540, 1050, 260, "#ffd23f", 0.6, 0.5, pulso=[0.2, 0.6])],
             cam(1.0, 1.08, (540, 1050)), "corte", hud=[rotulo(0.4, d - 0.05, "EL ANILLO DEL NIBELUNGO", tam=66, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.2, "ding", -18)])


@v.plano(83, "y el diseñador Carl Emil Doepler: el lápiz dibuja el boceto")
def _(d):
    return P(PAP, [BG("bg_papel"), IMG("boceto", ancho=640, x=540, y=1050, z=0.5, keys=aparece(0.0)),
                   IMG("lapiz", ancho=420, x=600, y=900, z=0.6, keys=[{"t": 0, "x": 520, "y": 820, "rot": -30}, {"t": d * 0.3, "x": 680, "y": 900, "rot": -25}, {"t": d * 0.6, "x": 560, "y": 980, "rot": -35}, {"t": d, "x": 700, "y": 1060, "rot": -28}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[BANDA(), rotulo(0.4, d - 0.05, "EL DISEÑADOR", tam=100, color="#ffffff", capsula="#2a5ae8e6", y=560)], sfx=[(0.2, "roce", -18), (0.8, "roce", -18)])


@v.plano(89, "vistió a los guerreros con cascos con cuernos: el vikingo con cuernos en el escenario")
def _(d):
    return P(TEA, [BG("bg_teatro"), brillo(540, 1150, 420, "#fff4c8", 0.4, 0.3),
                   IMG("vikingo_cuernos", ancho=480, x=540, y=1120, z=0.5, keys=[{"t": 0, "x": 1300}, {"t": 0.5, "x": 540, "ease": "salida"}, {"t": d, "x": 520}])],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[rotulo(0.4, d - 0.05, "CUERNOS", tam=120, color="#141414", capsula="#fff0d0e6", y=560)], sfx=[(0.1, "whoosh", -20)])


@v.plano(97, "y alas: entra el cantante con alas")
def _(d):
    return P(TEA, [BG("bg_teatro"), IMG("vikingo_cuernos", ancho=420, x=330, y=1120, z=0.5), IMG("cantante_alas", ancho=420, x=760, y=1120, z=0.51, keys=aparece(0.0))],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[amarillo(0.05, d - 0.02, "¡Y ALAS!", y=560, tam=120, color="#ffffff")], sfx=[(0.05, "pop", -16)])


@v.plano(99, "y la imagen se quedó para siempre: fila de vikingos con cuernos que se multiplican")
def _(d):
    els = [IMG("vikingo_cuernos", ancho=300, x=140 + k * 200, y=1100 + (k % 2) * 40, z=0.5 + k * 0.01, keys=aparece(0.15 * k)) for k in range(5)]
    return P(FIO, [BG("bg_fiordo"), *els], cam(1.0, 1.06, (540, 1100)), "corte", hud=[BANDA(), rotulo(0.5, d - 0.05, "PARA SIEMPRE", tam=110, color="#141414", capsula="#ffd23fe6", y=560)],
             sfx=[(0.15 * k, "pop", -22) for k in range(5)])


@v.plano(106, "lo más curioso es que sí existen cascos con cuernos: fogonazo y casco de bronce")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("casco_vekso", ancho=820, x=540, y=1050, z=0.5, keys=aparece(0.3) + late(1.2, 1, 0.05)), brillo(540, 1050, 450, "#ffc83a", 0.4, 0.4, pulso=[0.2, 0.6])],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[amarillo(0.2, d - 0.05, "¡SÍ EXISTEN!", y=560, tam=120, color=AMBAR)], sfx=[(0.05, "subida", -20, {"dur": 0.3}), (0.3, "impacto", -16)])


@v.plano(118, "los de Veksø, en Dinamarca: el casco sale de la turbera")
def _(d):
    return P(["#c8d8c0", "#5a4a2a"], [BG("bg_turbera"), IMG("casco_vekso", ancho=620, x=540, y=1150, z=0.5, keys=[{"t": 0, "y": 1420, "op": 0.5}, {"t": d * 0.7, "y": 1150, "op": 1, "ease": "salida"}]),
                   polvo("#a8b870", 20, (300, 1200, 780, 1400), 4)],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[BANDA(), rotulo(0.3, d - 0.05, "VEKSØ · DINAMARCA", tam=86, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.2, "agua", -22)])


@v.plano(123, "pero son de hace unos tres mil años: la cuenta de años corre")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("casco_vekso", ancho=600, x=540, y=1150, z=0.5, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.05}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[contador(0.1, d - 0.03, 0, 3000, min(1.2, d * 0.6), " AÑOS", tam=130, color="#141414", capsula="#ffd23fe6", y=600)],
             sfx=[(0.1, "subida", -22, {"dur": 1.0})])


@v.plano(131, "de la Edad del Bronce: el casco brilla dorado")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("casco_vekso", ancho=760, x=540, y=1100, z=0.5, keys=late(0.2, 1, 0.05)), brillo(540, 1050, 420, "#ffc83a", 0.6, 0.45, pulso=[0.2, 0.6])],
             cam(1.0, 1.08, (540, 1100)), "corte", hud=[rotulo(0.2, d - 0.05, "EDAD DEL BRONCE", tam=90, color="#141414", capsula="#e8b860e6", y=560)], sfx=[(0.2, "brillo", -18)])


@v.plano(136, "más de mil quinientos años antes de los vikingos: línea del tiempo del casco de bronce al vikingo")
def _(d):
    return P(PAP, [BG("bg_papel"), IMG("casco_vekso", ancho=380, x=250, y=900, z=0.5, keys=aparece(0.0)),
                   IMG("vikingo", ancho=300, x=830, y=950, z=0.5, keys=aparece(d * 0.55)),
                   flecha([[200, 1260], [880, 1260]], 0.3, d * 0.55, "#c0392b", 14, z=0.55)],
             cam(1.0, 1.04, (540, 1000)), "corte",
             hud=[BANDA(), rotulo(0.2, d - 0.05, "≈900 a. C.", tam=64, color="#141414", capsula="#e8b860e6", x=260, y=1340),
                  rotulo(d * 0.55, d - 0.05, "793 d. C.", tam=64, color="#ffffff", capsula="#3a6a4ae6", x=740, y=1340),
                  rotulo(0.4, d - 0.05, "+1.500 AÑOS", tam=110, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.3, "whoosh", -20), (d * 0.55, "pop", -18)])


@v.plano(145, "¿qué otro mito quieres que desmonte?: el casco de disfraz vuelve a perder los cuernos (bucle)")
def _(d):
    return P(FIO, [BG("bg_fiordo"), *casco_que_pierde(540, 1000, 900, d * 0.6, d)], cam(1.0, 1.06, (540, 1000)), "corte",
             hud=[BANDA(), rotulo(0.2, d - 0.05, "¿OTRO MITO?", tam=110, color="#ffffff", capsula="#c0392be6", y=1250)], sfx=[(d * 0.6, "zap", -16)])


v.construir("2026-11-24-tarde-03-vikingos-cuernos", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 324, "db": -13},
            claves=["vikingos", "cuernos", "invento", "casco", "Noruega", "Gjermundbu", "hierro", "redondo", "ojos", "nariz", "batalla", "estorbo",
                    "ópera", "Wagner", "Doepler", "alas", "Veksø", "Dinamarca", "Bronce"])
