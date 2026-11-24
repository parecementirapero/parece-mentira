"""01 · Tu gato ignora el dulce — método denso, estilo cartoon. Lote 2026-11-24-tarde (Agente 20:00 (Jorge)).
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
from comun_1124t import *  # noqa: E402,F401,F403
import ilus_1124t  # noqa: E402

SVG = ilus_1124t.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
COC = ["#ffe9c8", "#f6c98e"]
LAB = ["#dff4f4", "#a8d8dc"]


def gato(n="gato", x=540, y=1050, ancho=600, keys=None, z=0.5): return IMG(n, ancho=ancho, x=x, y=y, z=z, keys=keys or [])


@v.plano(0, "gancho: el gato saca la lengua delante de un pastel enorme y aparta la cara")
def _(d):
    return P(COC, [BG("bg_cocina"), gato("gato_lengua", y=980, ancho=640, keys=arranque(540, 980, d, "abajo", 280, 30)),
                   IMG("pastel", ancho=520, x=560, y=1330, z=0.6, keys=[{"t": 0, "x": 1200}, {"t": 0.35, "x": 560, "ease": "salida"}, {"t": d, "x": 600}])],
             cam(1.0, 1.08, (540, 1100)), vineta=0.45, hud=[BANDA()], sfx=[(0.05, "whoosh", -20), (0.4, "pop", -18)])


@v.plano(5, "no es que no le guste: el gato huele el pastel, con interrogación")
def _(d):
    return P(COC, [BG("bg_cocina"), gato(y=1000, keys=[{"t": 0, "rot": 0}, {"t": d * 0.5, "rot": -8, "ease": "suave"}, {"t": d, "rot": 0, "ease": "suave"}]),
                   IMG("pastel", ancho=420, x=300, y=1330, z=0.6, keys=late(0.3, 2, 0.06, 0.5))],
             cam(1.05, 1.12, (480, 1150)), "corte", hud=[BANDA(), rotulo(0.05, d - 0.03, "¿NO LE GUSTA?", tam=96, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.2, "roce", -20)])


@v.plano(11, "es que no lo nota: primer plano de la lengua del gato")
def _(d):
    return P(COC, [BG("bg_cocina"), gato("gato_lengua", y=1150, ancho=900, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.06, "ease": "suave"}]),
                   brillo(540, 1230, 200, "#ff6a86", 0.4, 0.55, pulso=[0.2, 0.6])],
             cam(1.0, 1.15, (540, 1100), (540, 1250)), "corte", hud=[BANDA(), rotulo(0.3, d - 0.05, "NO LO NOTA", tam=110, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.2, "pop", -20)])


@v.plano(16, "dale un pastel: el pastel cae sobre la encimera")
def _(d):
    return P(COC, [BG("bg_cocina"), IMG("pastel", ancho=600, x=540, y=1150, z=0.55, keys=cae(0.0, 0.5, 500, 1150))],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[BANDA()], sfx=[(0.35, "golpe", -18)])


@v.plano(19, "o un caramelo: el caramelo cae al lado, girando")
def _(d):
    return P(COC, [BG("bg_cocina"), IMG("pastel", ancho=460, x=330, y=1180, z=0.55),
                   IMG("caramelo", ancho=420, x=760, y=1150, z=0.6, keys=[{"t": 0, "y": 500, "rot": -90}, {"t": 0.45, "y": 1150, "rot": 10, "ease": "bote"}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[BANDA()], sfx=[(0.35, "pop", -16)])


@v.plano(22, "para él, nada de eso sabe dulce: el medidor de dulce se queda en cero")
def _(d):
    return P(COC, [BG("bg_cocina"), gato("gato_gris", x=540, y=1080, ancho=560, keys=[{"t": 0, "x": 520}, {"t": d, "x": 560, "ease": "suave"}]),
                   IMG("pastel", ancho=300, x=230, y=1320, z=0.6), IMG("caramelo", ancho=280, x=860, y=1330, z=0.6, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 30}])],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[BANDA(), rotulo(0.3, d - 0.05, "DULCE: 0", tam=120, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.3, "zap", -20)])


@v.plano(29, "¿por qué?: el gato inclina la cabeza")
def _(d):
    return P(OSC, [BG("bg_estudio"), gato(y=1000, ancho=640, keys=[{"t": 0, "rot": 0}, {"t": d * 0.5, "rot": 10, "ease": "salida"}]), brillo(540, 1000, 500, "#ffd23f", 0.3, 0.06)],
             cam(1.0, 1.08, (540, 1000)), "corte", hud=[amarillo(0.05, d - 0.03, "¿POR QUÉ?", y=560, tam=130, color=AMBAR)], sfx=[(0.05, "impacto", -18)])


@v.plano(31, "para notar el dulce, la lengua: aparece la lengua enorme")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("lengua", ancho=620, x=540, y=1000, z=0.5, keys=arranque(540, 1000, d, "abajo", 400, 20))],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[rotulo(0.4, d - 0.05, "LA LENGUA", tam=100, color="#141414", capsula="#ff9aa8e6", y=560)], sfx=[(0.1, "whoosh", -20)])


@v.plano(37, "necesita un receptor: zoom a una papila de la lengua")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("lengua", ancho=620, x=540, y=1000, z=0.5), senala(660, 900, 0.15, d - 0.05, 70, CIAN)],
             cam(1.0, 1.9, (540, 1000), (660, 900)), "corte", sfx=[(0.15, "ding", -20)])


@v.plano(40, "hecho con dos piezas: las dos piezas encajan")
def _(d):
    t = d * 0.55
    return P(OSC, [IMG("pieza_a", ancho=330, x=370, y=1000, z=0.5, keys=[{"t": 0, "x": 120}, {"t": t, "x": 395, "ease": "salida"}]),
                   IMG("pieza_b", ancho=330, x=690, y=1000, z=0.5, keys=[{"t": 0, "x": 960}, {"t": t, "x": 685, "ease": "salida"}]),
                   brillo(540, 1000, 300, "#7df9ff", 0.0, 0.4, keys=[{"t": t, "op": 0}, {"t": t + 0.1, "op": 1}, {"t": d, "op": 0.4}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[rotulo(0.1, d - 0.03, "RECEPTOR", tam=110, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(t, "ding", -16)])


@v.plano(44, "y la receta de una de ellas está en un gen: la pieza rosa late y sale la tira de ADN")
def _(d):
    return P(OSC, [IMG("pieza_a", ancho=260, x=200, y=1200, z=0.45, keys=[{"t": 0, "op": 1}, {"t": 0.4, "op": 0.3}]),
                   IMG("pieza_b", ancho=260, x=400, y=1200, z=0.5, keys=late(0.1, 2, 0.12, 0.35)),
                   IMG("adn", ancho=900, x=540, y=830, z=0.55, keys=[{"t": 0, "op": 0, "ex": 0.1}, {"t": d * 0.55, "op": 0, "ex": 0.1}, {"t": d * 0.75, "op": 1, "ex": 1.0, "ease": "salida"}]),
                   flecha([[400, 1060], [540, 960]], d * 0.4, d * 0.6, MAGENTA, 10, z=0.6)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[rotulo(d * 0.7, d - 0.03, "UN GEN", tam=110, color="#141414", capsula="#ff9af2e6", y=560)], sfx=[(d * 0.7, "brillo", -18)])


@v.plano(55, "en dos mil cinco: laboratorio, el año corre")
def _(d):
    return P(LAB, [BG("bg_lab_claro"), IMG("microscopio", ancho=380, x=760, y=1150, z=0.5, keys=aparece(0.1))],
             cam(1.0, 1.05, (540, 1000)), "desenfoque",
             hud=[BANDA(), contador(0.05, d - 0.03, 1990, 2005, 0.5, miles=False, tam=180, color="#141414", capsula="#ffffffe6", x=380, y=900)], sfx=[(0.1, "tic", -18)])


@v.plano(59, "unos científicos del Centro Monell, en Estados Unidos: dos científicos con el microscopio")
def _(d):
    return P(LAB, [BG("bg_lab_claro"), IMG("microscopio", ancho=380, x=620, y=1150, z=0.5),
                   IMG("profesor", ancho=300, x=300, y=1150, z=0.55, keys=[{"t": 0, "x": 240}, {"t": d, "x": 300, "ease": "suave"}]),
                   IMG("persona_pie", ancho=260, x=880, y=1170, z=0.52, keys=[{"t": 0, "x": 950}, {"t": d, "x": 880, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[BANDA(), rotulo(0.3, d - 0.05, "CENTRO MONELL · EE. UU.", tam=72, color="#ffffff", capsula="#2a5ae8e6", y=560)], sfx=[(0.2, "roce", -20)])


@v.plano(67, "miraron ese gen en los gatos: el ADN sobre el gato con la lupa")
def _(d):
    return P(LAB, [BG("bg_lab_claro"), gato("gato_gris", y=1150, ancho=520), IMG("adn", ancho=860, x=540, y=760, z=0.55, keys=[{"t": 0, "x": 600}, {"t": d, "x": 480, "ease": "suave"}]),
                   IMG("lupa", ancho=340, x=420, y=780, z=0.7, keys=[{"t": 0, "x": 250}, {"t": d, "x": 760, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[BANDA()], sfx=[(0.1, "whoosh", -22)])


@v.plano(73, "y estaba roto: el ADN se parte y le falta un trozo")
def _(d):
    return P(OSC, [IMG("adn_roto", ancho=960, x=540, y=1000, z=0.5, keys=[{"t": 0, "escala": 1.1}, {"t": 0.3, "escala": 1.0, "ease": "golpe"}]),
                   brillo(540, 1000, 250, "#ff3d3d", 0.6, 0.55, pulso=[0.2, 0.5])],
             cam(1.0, 1.1, (540, 1000), (540, 1000), temblor=6), "corte", hud=[rotulo(0.1, d - 0.03, "ROTO", tam=150, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.05, "impacto", -15)])


@v.plano(76, "le faltaban doscientas cuarenta y siete letras: la cuenta corre en el hueco")
def _(d):
    return P(OSC, [IMG("adn_roto", ancho=960, x=540, y=1000, z=0.5), polvo("#ffd23f", 30, (400, 860, 680, 1140), 3)],
             cam(1.0, 1.6, (540, 1000)), "corte", hud=[rotulo(0.1, d - 0.03, "FALTAN", tam=110, color="#ffffff", capsula="#c0392be6", y=560), contador(0.05, d - 0.03, 0, 247, min(1.4, d * 0.7), "", tam=150, color="#141414", capsula="#ffd23fe6", y=1300)],
             sfx=[(0.05, "subida", -22, {"dur": min(1.4, d * 0.7)})])


@v.plano(83, "sin esa pieza: la pieza rosa se agrieta")
def _(d):
    return P(OSC, [IMG("pieza_a", ancho=330, x=395, y=1000, z=0.5),
                   IMG("pieza_b", ancho=330, x=685, y=1000, z=0.5, keys=[{"t": 0, "op": 1}, {"t": d * 0.4, "op": 0}]),
                   IMG("pieza_b_rota", ancho=330, x=685, y=1000, z=0.51, keys=[{"t": 0, "op": 0}, {"t": d * 0.4, "op": 1}])],
             cam(1.0, 1.08, (540, 1000), temblor=3), "corte", sfx=[(d * 0.4, "golpe", -16)])


@v.plano(86, "el receptor no se monta: la pieza rota se cae y no encaja")
def _(d):
    return P(OSC, [IMG("pieza_a", ancho=330, x=395, y=1000, z=0.5, keys=late(0.6, 1, 0.05)),
                   IMG("pieza_b_rota", ancho=330, x=685, y=1000, z=0.51, keys=[{"t": 0, "x": 685, "y": 1000, "rot": 0}, {"t": d, "x": 800, "y": 1700, "rot": 40, "ease": "entrada"}])],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[rotulo(0.3, d - 0.05, "NO ENCAJA", tam=110, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.3, "zap", -18)])


@v.plano(91, "y el azúcar pasa sin avisar: el terrón cruza la lengua sin que pase nada")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("lengua", ancho=560, x=540, y=1050, z=0.45),
                   IMG("azucar", ancho=240, x=540, y=900, z=0.6, keys=[{"t": 0, "x": -150, "rot": 0}, {"t": d, "x": 1230, "rot": 200, "ease": "lineal"}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[amarillo(0.3, d - 0.05, "SIN AVISAR", y=1340, tam=100, color=CIAN)], sfx=[(0.1, "whoosh", -20)])


@v.plano(97, "lo mismo les pasa a los tigres: el tigre entra en la selva")
def _(d):
    return P(["#2a6a3a", "#0a2a14"], [BG("bg_jungla"), gato("tigre", y=1050, ancho=660, keys=arranque(540, 1050, d, "izquierda", 300, 20))],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[rotulo(0.3, d - 0.05, "TIGRE", tam=110, color="#141414", capsula="#ff9a2ae6", y=560)], sfx=[(0.1, "whoosh", -20)])


@v.plano(104, "y a los guepardos: el guepardo")
def _(d):
    return P(["#e8c070", "#a87a30"], [BG("bg_paisaje"), gato("guepardo", y=1050, ancho=620, keys=arranque(540, 1050, d, "derecha", 300, 20))],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[rotulo(0.2, d - 0.05, "GUEPARDO", tam=110, color="#141414", capsula="#ffd27ae6", y=560)], sfx=[(0.1, "whoosh", -22)])


@v.plano(108, "y tiene sentido: el gato asiente")
def _(d):
    return P(COC, [BG("bg_cocina"), gato(y=1050, ancho=600, keys=[{"t": 0, "y": 1050}, {"t": d * 0.3, "y": 1080, "ease": "salida"}, {"t": d * 0.6, "y": 1050, "ease": "suave"}])],
             cam(1.05, 1.1, (540, 1050)), "corte", hud=[BANDA()], sfx=[(0.1, "pop", -22)])


@v.plano(111, "los gatos solo comen carne: el filete cae en el cuenco")
def _(d):
    return P(COC, [BG("bg_cocina"), gato("gato_lengua", x=330, y=1050, ancho=520), IMG("cuenco", ancho=420, x=780, y=1300, z=0.55),
                   IMG("filete", ancho=380, x=780, y=1200, z=0.6, keys=cae(0.0, 0.5, 600, 1200))],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[BANDA(), rotulo(0.4, d - 0.05, "SOLO CARNE", tam=100, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.35, "golpe", -18)])


@v.plano(116, "y la carne casi no tiene azúcar: filete y terrón, el terrón se tacha")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("filete", ancho=520, x=540, y=850, z=0.5, keys=late(0.2, 1, 0.05)),
                   IMG("azucar", ancho=260, x=540, y=1230, z=0.55, keys=aparece(0.2)), *tacha(540, 1230, d * 0.55, 150)],
             cam(1.0, 1.05, (540, 1000)), "corte", sfx=[(d * 0.55, "zap", -18)])


@v.plano(123, "perder el dulce no les costó nada: el gato come tranquilo del cuenco")
def _(d):
    return P(COC, [BG("bg_cocina"), gato("gato_gris", x=420, y=1050, ancho=540, keys=[{"t": 0, "rot": 0}, {"t": d * 0.5, "rot": 6, "ease": "suave"}, {"t": d, "rot": 0}]),
                   IMG("cuenco", ancho=400, x=800, y=1330, z=0.6, keys=late(0.3, 2, 0.05, 0.6))],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[BANDA(), rotulo(0.4, d - 0.05, "NO LE HACE FALTA", tam=86, color="#141414", capsula="#7dff3ae6", y=560)], sfx=[(0.3, "mordisco", -20)])


@v.plano(130, "entonces, ¿por qué tu gato lame el helado?: el helado llega y el gato saca la lengua")
def _(d):
    return P(COC, [BG("bg_cocina"), gato("gato_lengua", x=380, y=1050, ancho=560),
                   IMG("helado", ancho=300, x=800, y=1050, z=0.6, keys=[{"t": 0, "x": 1250, "rot": 20}, {"t": 0.6, "x": 800, "rot": -8, "ease": "salida"}, {"t": d, "rot": 4}])],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[BANDA(), rotulo(0.6, d - 0.05, "¿Y EL HELADO?", tam=100, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.1, "whoosh", -20)])


@v.plano(138, "por la grasa: la bola del helado brilla")
def _(d):
    return P(OSC, [IMG("helado", ancho=420, x=540, y=1050, z=0.5, keys=late(0.1, 2, 0.08, 0.4)), brillo(540, 900, 260, "#fff4d8", 0.6, 0.45, pulso=[0.2, 0.5])],
             cam(1.0, 1.1, (540, 1000)), "corte", hud=[rotulo(0.2, d - 0.05, "GRASA", tam=130, color="#141414", capsula="#7dff3ae6", y=560)], sfx=[(0.2, "ding", -18)])


@v.plano(141, "no por el azúcar: el terrón tachado")
def _(d):
    return P(OSC, [IMG("azucar", ancho=360, x=540, y=1000, z=0.5, keys=aparece(0.0)), *tacha(540, 1000, 0.25, 190)],
             cam(1.0, 1.08, (540, 1000)), "corte", sfx=[(0.25, "zap", -18)])


@v.plano(145, "¿tu gato te roba comida?: el gato arrastra el filete por la encimera")
def _(d):
    return P(COC, [BG("bg_cocina"), gato(x=540, y=1050, ancho=560, keys=[{"t": 0, "x": 800}, {"t": d, "x": 380, "ease": "suave"}]),
                   IMG("filete", ancho=300, x=540, y=1300, z=0.6, keys=[{"t": 0, "x": 860}, {"t": d, "x": 440, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[BANDA()], sfx=[(0.1, "roce", -20)])


@v.plano(150, "cuéntame cuál: vuelve el gato con el pastel (bucle)")
def _(d):
    return P(COC, [BG("bg_cocina"), gato("gato_lengua", y=980, ancho=640, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.05, "ease": "suave"}]),
                   IMG("pastel", ancho=520, x=560, y=1330, z=0.6)],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[BANDA()], sfx=[(0.1, "pop", -22)])


v.construir("2026-11-24-tarde-01-gato-dulce", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 124, "db": -13},
            claves=["gato", "dulce", "nota", "pastel", "caramelo", "lengua", "receptor", "piezas", "gen", "Monell", "roto", "letras",
                    "azúcar", "tigres", "guepardos", "carne", "helado", "grasa"])
