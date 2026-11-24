"""03 · Di el color, no leas (efecto Stroop) — interactivo, estilo cartoon. Lote 2026-11-23-tarde (Jorge, con el agente).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]
Las dos rondas del test van cada una en UN plano fijo (Jorge: no cambiar el plano durante la prueba)."""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
from comun_1123t import *  # noqa: E402,F401,F403
import motor.denso as D  # noqa: E402
import ilus_1123t  # noqa: E402

SVG = ilus_1123t.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
PIZ = ["#1a1a2e", "#0e0e1a"]
ROJO, AZUL, VERDE, AMAR, MORADO = "#e8302a", "#2a5ae8", "#1f9a3a", "#e8b800", "#8a3ad8"
CAM_FIJA = cam(1.0, 1.0, (540, 1000))


def pizarra(): return BG("bg_pizarra")


def en(T):
    """Segundo absoluto T → segundo dentro del plano actual."""
    return round(T - D._V.ini, 3)


@v.plano(0, "gancho: la palabra AZUL escrita en rojo aparece de golpe en la pizarra")
def _(d):
    return P(PIZ, [pizarra(), *muneco("mu_c", "br_c", 860, 1620, 260, 0.6, pup=(-10, -10))], cam(1.0, 1.06, (540, 1000)), vineta=0.4,
             hud=[{**palabra(0.0, d - 0.03, "AZUL", ROJO, y=1000, tam=260), "keys": late(0.05, 2, 0.1, 0.35) + [{"t": d, "op": 1}]}], sfx=[(0.02, "golpe", -16)])


@v.plano(5, "vas a ver palabras de colores: aparecen varias")
def _(d):
    ws = [("ROJO", AZUL, 760), ("VERDE", MORADO, 980), ("AMARILLO", VERDE, 1200)]
    return P(PIZ, [pizarra()], cam(1.0, 1.04, (540, 1000)), "corte", hud=[palabra(0.15 + i * 0.3, d - 0.03, t, c, y=y, tam=150) for i, (t, c, y) in enumerate(ws)],
             sfx=[(0.15 + i * 0.3, "pop", -20) for i in range(3)])


@v.plano(18, "di el color de la tinta, no la palabra: la palabra VERDE en azul y la respuesta")
def _(d):
    return P(PIZ, [pizarra(), flecha([[540, 1120], [540, 1260]], 0.4, 0.7, "#141414", 10, z=0.7)], cam(1.0, 1.04, (540, 1000)), "corte",
             hud=[palabra(0.0, d - 0.03, "VERDE", AZUL, y=900, tam=200), rotulo(0.7, d - 0.03, "DI: «AZUL»", tam=100, color="#ffffff", capsula="#2a5ae8e6", y=1340)],
             sfx=[(0.7, "ding", -20)])


@v.plano(27, "primera ronda, fácil: rojo, azul, verde (un solo plano fijo)")
def _(d):
    T = [10.48, 11.24, 12.00]
    ws = [("ROJO", ROJO), ("AZUL", AZUL), ("VERDE", VERDE)]
    hud = [rotulo(0.05, max(0.3, en(T[0]) - 0.1), "RONDA 1 · FÁCIL", tam=96, color="#141414", capsula="#b8ff3ae6", y=1000)]
    for i, (t, c) in enumerate(ws):
        hud.append(palabra(en(T[i]) - 0.15, en(T[i]) + 0.62 if i < 2 else d - 0.03, t, c, y=1000, tam=240))
    return P(PIZ, [pizarra()], CAM_FIJA, "corte", hud=hud, sfx=[(en(t) - 0.15, "pop", -22) for t in T])


@v.plano(33, "ahora la de verdad: ocho palabras que no coinciden con su color, una tras otra (un solo plano fijo)")
def _(d):
    ws = [("ROJO", VERDE), ("AZUL", AMAR), ("VERDE", ROJO), ("MORADO", AZUL), ("AZUL", ROJO), ("ROJO", MORADO), ("VERDE", AZUL)]
    t0 = en(14.0); paso = (en(18.85) - t0) / len(ws)
    hud = [rotulo(0.05, max(0.4, t0 - 0.05), "RONDA 2", tam=110, color="#ffffff", capsula="#c0397ae6", y=1000)]
    for i, (t, c) in enumerate(ws):
        a = t0 + i * paso
        hud.append(palabra(a, a + paso - 0.05 if i < len(ws) - 1 else d - 0.03, t, c, y=1000, tam=230 if len(t) < 6 else 185))
    return P(PIZ, [pizarra()], CAM_FIJA, "corte", hud=hud, sfx=[(t0 + i * paso, "tic", -24) for i in range(len(ws))])


@v.plano(46, "¿te has trabado?: el muñeco con cara de lío")
def _(d):
    return P(PIZ, [pizarra(), *muneco("mu_c", "br_c", 540, 1500, 700, 0.5, keys_pup=[{"t": 0, "x": 520, "y": 1500}, {"t": 0.2, "x": 560, "y": 1490}, {"t": 0.4, "x": 520, "y": 1510}, {"t": d, "x": 545, "y": 1500}])],
             cam(1.0, 1.05, (540, 1100), temblor=4), "corte", hud=[rotulo(0.0, d - 0.03, "¿TRABADO?", tam=110, color="#ffffff", capsula="#c0397ae6", y=470)], sfx=[(0.1, "zap", -20)])


@v.plano(49, "es normal")
def _(d):
    return P(PIZ, [pizarra(), *muneco("mu_c", "br_c", 540, 1500, 700, 0.5, rot_out=30)], cam(1.05, 1.0, (540, 1100)), "corte",
             hud=[rotulo(0.05, d - 0.03, "ES NORMAL", tam=110, color="#141414", capsula="#b8ff3ae6", y=470)], sfx=[(0.05, "ding", -22)])


@v.plano(51, "se llama efecto Stroop")
def _(d):
    return P(PIZ, [pizarra()], cam(1.0, 1.05, (540, 1000)), "corte", hud=[rotulo(0.05, d - 0.03, "EFECTO STROOP", tam=130, color="#141414", capsula="#ffd23fe6", y=1000)],
             sfx=[(0.05, "impacto", -18)])


@v.plano(55, "por el psicólogo John Ridley Stroop, que lo publicó en 1935")
def _(d):
    return P(["#0a1a2a", "#020610"], [BG("bg_estudio"), IMG("calendario", ancho=560, x=540, y=1150, z=0.5, keys=aparece(0.0))], cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[rotulo(0.1, d * 0.45, "J. RIDLEY STROOP", tam=96, color="#141414", capsula="#7df9ffe6", y=560),
                  contador(d * 0.45, d - 0.03, 1900, 1935, d * 0.4, "", y=560, tam=150, color="#ffd23f", miles=False)], sfx=[(d * 0.45, "tictac", -22, {"dur": d * 0.4, "ritmo": 0.06})])


@v.plano(70, "en su experimento, la gente tardaba mucho más: el reloj corre")
def _(d):
    return P(OSC, [IMG("reloj_cartoon", ancho=640, x=540, y=1100, z=0.5), IMG("segundero", ancho=640, x=540, y=1100, z=0.55, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 300, "ease": "lineal"}])],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[amarillo(0.3, d - 0.05, "MUCHO MÁS LENTO", y=560, tam=100, color="#ffd23f")], sfx=[(0.05, "tictac", -20, {"dur": d, "ritmo": 0.12})])


@v.plano(82, "y se equivocaba más si la palabra decía otro color: ROJO en verde, con una cruz")
def _(d):
    return P(PIZ, [pizarra(), flecha([[340, 860], [740, 1140]], 0.5, 0.7, ROJO, 18, punta=False, z=0.8), flecha([[740, 860], [340, 1140]], 0.6, 0.8, ROJO, 18, punta=False, z=0.8)],
             cam(1.0, 1.04, (540, 1000)), "corte", hud=[palabra(0.0, d - 0.03, "ROJO", VERDE, y=1000, tam=240), rotulo(0.9, d - 0.05, "MÁS FALLOS", tam=100, color="#ffffff", capsula="#c0392be6", y=1350)],
             sfx=[(0.6, "zap", -18)])


@v.plano(92, "¿por qué?: el cerebro aparece")
def _(d):
    return P(OSC, [IMG("cerebro", ancho=760, x=540, y=1050, z=0.5, keys=aparece(0.0))], cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[amarillo(0.0, d - 0.03, "¿POR QUÉ?", y=560, tam=130, color=CIAN)], sfx=[(0.05, "roce", -20)])


@v.plano(94, "porque leer es automático: la palabra entra sola en el cerebro")
def _(d):
    return P(OSC, [IMG("cerebro", ancho=760, x=540, y=1150, z=0.5), brillo(540, 1150, 400, "#ffd23f", 0.5, 0.45, pulso=[0.15, 0.4])], cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[{**palabra(0.05, d - 0.05, "AZUL", ROJO, y=700, tam=160), "keys": [{"t": 0.0, "y": 650, "op": 1}, {"t": d * 0.6, "y": 760, "op": 1}, {"t": d * 0.9, "y": 1050, "escala": 0.4, "op": 0.2, "ease": "entrada"}]},
                  rotulo(0.4, d - 0.05, "AUTOMÁTICO", tam=110, color="#141414", capsula="#ffd23fe6", y=1500)], sfx=[(0.3, "whoosh", -20)])


@v.plano(98, "tu cerebro lee la palabra antes de que puedas evitarlo")
def _(d):
    return P(PIZ, [pizarra(), *muneco("mu_c", "br_c", 860, 1620, 260, 0.6, pup=(-10, -10))], cam(1.0, 1.04, (540, 1000)), "corte",
             hud=[palabra(0.0, d - 0.03, "VERDE", MORADO, y=1000, tam=230), rotulo(0.4, d - 0.05, "LO LEES SIN QUERER", tam=80, color="#ffffff", capsula="#141414e6", y=1350)],
             sfx=[(0.05, "pop", -20)])


@v.plano(108, "y tiene que frenarla para decir el color: señal de STOP sobre la palabra")
def _(d):
    return P(PIZ, [pizarra()], cam(1.0, 1.05, (540, 1000)), "corte",
             hud=[palabra(0.0, d - 0.03, "VERDE", MORADO, y=1000, tam=230),
                  rotulo(0.3, d - 0.05, "FRENA", tam=150, color="#ffffff", capsula="#c0392be6", y=720), rotulo(d * 0.55, d - 0.05, "DI: «MORADO»", tam=96, color="#ffffff", capsula="#8a3ad8e6", y=1350)],
             sfx=[(0.3, "golpe", -18), (d * 0.55, "ding", -22)])


@v.plano(116, "hoy esta prueba se usa en consultas de neuropsicología")
def _(d):
    return P(["#0a2a2a", "#02100a"], [BG("bg_lab"), IMG("cerebro", ancho=620, x=540, y=1100, z=0.5, keys=late(0.2, 1))], cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[rotulo(0.3, d - 0.05, "NEUROPSICOLOGÍA", tam=96, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(0.1, "senal", -22)])


@v.plano(129, "para medir la atención, por ejemplo en el TDAH o en el alzhéimer")
def _(d):
    return P(["#0a2a2a", "#02100a"], [BG("bg_lab"), IMG("cerebro", ancho=620, x=540, y=1100, z=0.5), brillo(540, 1100, 360, "#7df9ff", 0.5, 0.45, pulso=[0.15, 0.6])],
             cam(1.05, 1.1, (540, 1100)), "corte", hud=[rotulo(0.3, d * 0.5, "TDAH", tam=130, color="#141414", capsula="#ffd23fe6", y=560),
                                                       rotulo(d * 0.5, d - 0.05, "ALZHÉIMER", tam=120, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(d * 0.5, "pop", -20)])


@v.plano(138, "comenta: ¿cuántas fallaste?: la pizarra con AZUL en rojo y el bocadillo (bucle)")
def _(d):
    return P(PIZ, [pizarra(), IMG("bocadillo", ancho=420, x=780, y=1560, z=0.7, keys=aparece(0.2))], cam(1.0, 1.04, (540, 1000)), "corte",
             hud=[palabra(0.0, d - 0.3, "AZUL", ROJO, y=1000, tam=260), rotulo(0.3, d - 0.4, "¿CUÁNTAS FALLASTE?", tam=86, color="#141414", capsula="#ffd23fe6", y=560)],
             sfx=[(0.2, "pop", -20)])


import json as _json  # noqa: E402
_c = v.construir


def _construir(*a, **k):
    """El primer plano no lleva el empujón automático de cámara: la palabra tiene que verse quieta."""
    r = _c(*a, **k)
    ruta = os.path.join(sys.argv[1], "episodio.json"); ep = _json.load(open(ruta))
    ep["escenas"][0]["camara"] = {**ep["escenas"][0]["camara"], "zoom": [1.0, 1.06]}
    _json.dump(ep, open(ruta, "w"), ensure_ascii=False)
    return r


v.construir = _construir
v.construir("2026-11-23-tarde-03-di-el-color", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 93, "db": -14},
            claves=["color", "leas", "palabras", "tinta", "palabra", "rojo", "azul", "verde", "verdad", "Rápido", "deprisa", "trabado", "Stroop", "treinta",
                    "colores", "equivocaba", "automático", "frenarla", "neuropsicología", "atención", "TDAH", "alzhéimer", "fallaste"])
