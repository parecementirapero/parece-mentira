"""02 · El Sol es blanco — método denso, estilo cartoon. Lote 2026-11-23-tarde (Jorge, con el agente).
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
from comun_1123t import *  # noqa: E402,F401,F403
import ilus_1123t  # noqa: E402

SVG = ilus_1123t.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
ESP = ["#02030a", "#0a1030"]
TARDE = ["#c0507a", "#3a1a3a"]


def sol(n="sol_blanco", x=540, y=950, ancho=760, keys=None, z=0.5): return IMG(n, ancho=ancho, x=x, y=y, z=z, keys=keys or [])


@v.plano(0, "gancho: un Sol blanco enorme entra latiendo en el espacio negro")
def _(d):
    return P(ESP, [estrellas(80, 1), sol(ancho=820, keys=arranque(540, 950, d, "abajo", 300, 30) + late(0.6, 2, 0.05, 0.5)), brillo(540, 950, 600, "#ffffff", 0.5, 0.06)],
             cam(1.0, 1.08, (540, 950)), vineta=0.5, sfx=[(0.02, "subida", -18, {"dur": 0.9}), (0.9, "brillo", -18)])


@v.plano(4, "no amarillo: el Sol de los dibujos se tacha")
def _(d):
    return P(CIELO, [BG("bg_cielo_dia"), IMG("sol_dibujo", ancho=640, x=540, y=950, z=0.5, keys=aparece(0.0)),
                     flecha([[300, 710], [780, 1190]], 0.4, 0.6, "#ff3d3d", 20, punta=False, z=0.8), flecha([[780, 710], [300, 1190]], 0.5, 0.7, "#ff3d3d", 20, punta=False, z=0.8)],
             cam(1.0, 1.05, (540, 950)), "corte", hud=[rotulo(0.1, d - 0.03, "NO AMARILLO", tam=100, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.45, "zap", -18)])


@v.plano(6, "visto desde el espacio, fuera del aire, es blanco: la Tierra abajo y el Sol blanco arriba")
def _(d):
    return P(ESP, [estrellas(80, 2), tierra(540, 1750, 900, 0.4, giro=6), sol(ancho=520, y=650, keys=late(0.3, 1, 0.05)), IMG("astro_c0", ancho=240, x=820, y=1150, z=0.55, keys=[{"t": 0, "y": 1180}, {"t": d, "y": 1130, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1000)), "desenfoque", hud=[rotulo(0.4, d - 0.05, "DESDE EL ESPACIO: BLANCO", tam=72, color="#141414", capsula="#ffffffe6", y=1080)], sfx=[(0.1, "whoosh", -22)])


@v.plano(15, "¿entonces por qué aquí lo vemos amarillo?: el Sol amarillento en el cielo azul")
def _(d):
    return P(CIELO, [BG("bg_cielo_dia"), sol("sol_amarillento", 760, 560, 480, keys=late(0.3, 2, 0.05)), *muneco("mu_a", "br_a", 330, 1420, 330, 0.5, pup=(10, -12), rot_out=-120)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[rotulo(0.2, d - 0.03, "¿POR QUÉ AMARILLO?", tam=86, color="#141414", capsula="#ffd23fe6", y=900)], sfx=[(0.1, "roce", -20)])


@v.plano(22, "por la atmósfera: la capa de aire alrededor de la Tierra")
def _(d):
    return P(ESP, [estrellas(60, 3), IMG("tierra_arco", ancho=1080, x=540, y=1450, z=0.4, keys=[{"t": 0, "y": 1650}, {"t": 0.5, "y": 1450, "ease": "salida"}]),
                   brillo(540, 1100, 600, "#7ad0ff", 0.5, 0.45, pulso=[0.15, 0.8])],
             cam(1.0, 1.05, (540, 1250)), "corte", hud=[rotulo(0.3, d - 0.05, "ATMÓSFERA", tam=120, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(0.1, "whoosh", -20)])


@v.plano(25, "la luz del Sol trae todos los colores mezclados: el espectro aparece")
def _(d):
    return P(OSC, [IMG("espectro", ancho=900, x=540, y=1050, z=0.5, keys=aparece(0.0)), sol(ancho=300, y=560, z=0.45)], cam(1.0, 1.05, (540, 1000)), "corte",
             hud=[amarillo(0.4, d - 0.05, "TODOS LOS COLORES", y=1500 - 150, tam=96, color="#ffffff")], sfx=[(0.05, "brillo", -18)])


@v.plano(34, "y todos juntos se ven blancos: el espectro se junta en un Sol blanco")
def _(d):
    return P(OSC, [IMG("espectro", ancho=900, x=540, y=1050, z=0.5, keys=[{"t": 0, "ex": 1, "op": 1}, {"t": d * 0.6, "ex": 0.05, "op": 0, "ease": "entrada"}]),
                   sol(ancho=600, y=1050, keys=[{"t": 0, "op": 0, "escala": 0.3}, {"t": d * 0.6, "op": 1, "escala": 1.0, "ease": "salida"}])],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[amarillo(d * 0.6, d - 0.05, "= BLANCO", y=560, tam=130, color="#ffffff")], sfx=[(d * 0.55, "impacto", -16)])


@v.plano(40, "pero al cruzar el aire, el azul y el violeta rebotan en las moléculas")
def _(d):
    mols = [IMG("molecula_aire", ancho=120, x=x, y=y, z=0.5, keys=late(0.3 + i * 0.1, 1)) for i, (x, y) in enumerate([(380, 900), (620, 1060), (500, 1250), (760, 820), (300, 1180)])]
    return P(CIELO, [BG("bg_cielo_dia"), IMG("rayo_blanco", ancho=900, x=540, y=1000, z=0.45, rot=35, keys=[{"t": 0, "op": 0}, {"t": 0.3, "op": 1}]), *mols,
                     IMG("rayo_azul", ancho=500, x=400, y=760, z=0.55, rot=-40, keys=[{"t": 0, "op": 0}, {"t": d * 0.5, "op": 0}, {"t": d * 0.6, "op": 1}]),
                     IMG("rayo_azul", ancho=500, x=760, y=1300, z=0.55, rot=60, keys=[{"t": 0, "op": 0}, {"t": d * 0.6, "op": 0}, {"t": d * 0.7, "op": 1}])],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[rotulo(0.3, d - 0.05, "EL AZUL REBOTA", tam=100, color="#ffffff", capsula="#2a5ae8e6", y=560)], sfx=[(d * 0.55, "pop", -20), (d * 0.65, "pop", -20)])


@v.plano(54, "y se esparcen por todo el cielo: puntitos azules llenan el cielo")
def _(d):
    return P(CIELO, [BG("bg_cielo_dia"), polvo("#3a7aff", 120, (0, 200, 1080, 1500), 5), polvo("#8a3ad8", 40, (0, 200, 1080, 1500), 6)],
             cam(1.0, 1.06, (540, 900)), "corte", sfx=[(0.1, "brillo", -22)])


@v.plano(61, "por eso el cielo es azul")
def _(d):
    return P(CIELO, [BG("bg_cielo_dia"), *muneco("mu_c", "br_c", 540, 1420, 360, 0.5, pup=(0, -14))], cam(1.0, 1.04, (540, 1000)), "corte",
             hud=[rotulo(0.1, d - 0.05, "CIELO AZUL", tam=130, color="#ffffff", capsula="#2a5ae8e6", y=560)], sfx=[(0.1, "ding", -20)])


@v.plano(67, "y al Sol, al que le han quitado parte del azul, lo vemos amarillento: el blanco se vuelve amarillo")
def _(d):
    return P(CIELO, [BG("bg_cielo_dia"), sol(ancho=600, y=900, keys=[{"t": 0, "op": 1}, {"t": d * 0.8, "op": 0}]), sol("sol_amarillento", ancho=600, y=900, z=0.51, keys=[{"t": 0, "op": 0}, {"t": d * 0.8, "op": 1}]),
                     IMG("rayo_azul", ancho=500, x=540, y=1350, z=0.55, keys=[{"t": 0, "x": 540}, {"t": d, "x": 1100, "op": 0, "ease": "entrada"}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[rotulo(0.3, d - 0.05, "MENOS AZUL = AMARILLENTO", tam=70, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.2, "whoosh", -22)])


@v.plano(81, "al atardecer, su luz atraviesa mucho más aire: la luz cruza la atmósfera de lado")
def _(d):
    return P(TARDE, [BG("bg_atardecer"), flecha([[60, 1000], [540, 1180], [1020, 1260]], 0.1, d * 0.8, "#ffb070", 12, z=0.6)], cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[amarillo(0.3, d - 0.05, "MÁS AIRE", y=560, tam=130, color="#ffd0a0")], sfx=[(0.1, "whoosh", -20)])


@v.plano(89, "se pierde todavía más azul, y el Sol se vuelve naranja y rojo: el Sol baja y se enrojece")
def _(d):
    return P(TARDE, [BG("bg_atardecer"), sol("sol_amarillento", ancho=420, y=900, keys=[{"t": 0, "op": 1, "y": 900}, {"t": d * 0.6, "op": 0, "y": 1150}]),
                     sol("sol_rojo", ancho=420, z=0.51, keys=[{"t": 0, "op": 0, "y": 900}, {"t": d * 0.6, "op": 1, "y": 1150}, {"t": d, "y": 1230}])],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[amarillo(0.4, d - 0.05, "NARANJA Y ROJO", y=560, tam=110, color="#ff8a4a")], sfx=[(0.1, "subida", -22, {"dur": d})])


@v.plano(102, "¿y lo más raro?: fogonazo")
def _(d):
    return P(ESP, [estrellas(60, 4), brillo(540, 1000, 600, "#3ac84a", 0.5, 0.06, pulso=[0.15, 0.6])], cam(1.0, 1.08, (540, 1000)), "corte",
             hud=[amarillo(0.05, d - 0.03, "¿LO MÁS RARO?", y=1000, tam=120, color="#ffd23f")], sfx=[(0.05, "impacto", -16)])


@v.plano(106, "el color que el Sol emite con más fuerza es el verde: la barra verde crece")
def _(d):
    return P(OSC, [IMG("espectro", ancho=900, x=540, y=1050, z=0.5), senala(546, 1050, 0.3, d - 0.1, 130, LIMA), brillo(546, 1050, 260, "#3ac84a", 0.8, 0.45, pulso=[0.2, 0.5])],
             cam(1.0, 1.3, (540, 1050), (546, 1050)), "corte", hud=[rotulo(0.4, d - 0.05, "EL VERDE", tam=130, color="#141414", capsula="#b8ff3ae6", y=560)], sfx=[(0.3, "ding", -18)])


@v.plano(118, "pero como manda todos los demás a la vez, no lo vemos verde: los colores se juntan otra vez")
def _(d):
    return P(OSC, [IMG("espectro", ancho=900, x=540, y=1050, z=0.5, keys=[{"t": 0, "ex": 1, "op": 1}, {"t": d * 0.7, "ex": 0.05, "op": 0, "ease": "entrada"}]),
                   sol(ancho=600, y=1050, keys=[{"t": 0, "op": 0, "escala": 0.3}, {"t": d * 0.7, "op": 1, "escala": 1.0, "ease": "salida"}])],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[amarillo(0.2, d - 0.05, "TODOS A LA VEZ", y=560, tam=110, color="#ffffff")], sfx=[(d * 0.65, "impacto", -18)])


@v.plano(131, "lo vemos blanco: el Sol blanco en el espacio")
def _(d):
    return P(ESP, [estrellas(80, 5), sol(ancho=820, keys=late(0.1, 1, 0.05)), brillo(540, 950, 600, "#ffffff", 0.5, 0.06)], cam(1.05, 1.12, (540, 950)), "corte",
             hud=[rotulo(0.1, d - 0.05, "BLANCO", tam=150, color="#141414", capsula="#ffffffe6", y=1650 - 300)], sfx=[(0.05, "brillo", -18)])


@v.plano(134, "así que el Sol amarillo de los dibujos… solo existe aquí abajo")
def _(d):
    return P(CIELO, [BG("bg_cielo_dia"), IMG("sol_dibujo", ancho=520, x=540, y=760, z=0.5, keys=aparece(0.0) + late(1.0, 2, 0.06, 0.5)), *muneco("mu_d", "br_d", 540, 1450, 330, 0.55, pup=(0, -14))],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[rotulo(0.4, d - 0.4, "SOLO AQUÍ ABAJO", tam=96, color="#141414", capsula="#ffd23fe6", y=1110)], sfx=[(0.1, "pop", -20), (d * 0.6, "ding", -22)])


v.construir("2026-11-23-tarde-02-sol-blanco", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 92, "db": -13},
            claves=["Sol", "blanco", "amarillo", "espacio", "atmósfera", "colores", "blancos", "azul", "violeta", "moléculas", "cielo", "amarillento",
                    "atardecer", "naranja", "rojo", "verde", "dibujos"])
