"""03 · Test de atención: cuenta los botes amarillos (y el astronauta que no ves) — método denso. Lote 2026-11-22-tarde (Jorge, con el agente).
Formato pedido por Jorge a partir de un vídeo de otra cuenta: es una VERSIÓN PROPIA (escena, personajes, guion y montaje nuestros), no una copia.
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]

La escena del test (segundos 0–12,5) es continua aunque haya cortes: las pelotas, el astronauta y el color del fondo
se calculan con el tiempo ABSOLUTO del vídeo (D._V.ini), así que cada plano enseña el mismo instante de la misma escena.
La pelota amarilla bota 11 veces (BOTES); la respuesta va en el comentario fijado."""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
import motor.denso as D  # noqa: E402
from motor.denso import *  # noqa: E402,F401,F403
import ilus_1122t  # noqa: E402

SVG = ilus_1122t.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

AZUL = ["#2a4a9a", "#14204a"]
NAR = ["#d0702a", "#6a2a10"]
OSC = ["#0a0a14", "#02020a"]

# ------------------------------------------------------------------ la escena del test (tiempo absoluto) · v2 estilo cartoon
# v2 (Jorge: «lo veo muy simple» y «no cambies el plano en los botes, porque lía»): muñecos propios con contorno, brazos que
# siguen la pelota, ojos que la miran, escenario con rejilla; un solo plano fijo durante todo el test.
import math  # noqa: E402
SUELO_Y, MANO_Y = 1462, 1240
A_X, B_X = 470, 610                 # manos de los dos que se pasan la amarilla
PA, PB = 330, 750                   # centros de esos dos muñecos (ancho 300, y=1200)
PC, PD = 150, 930                   # los de atrás (ancho 250, y=1190), pelota blanca
C_X, D_X, MANO2_Y, SUELO2_Y = 270, 810, 1230, 1420
BOTES = [4.56, 5.36, 6.10, 6.85, 7.60, 8.35, 9.10, 9.80, 10.40, 10.90, 11.40]   # 11 botes
FIN_TEST = 12.48
CAM_TEST = cam(1.12, 1.12, (540, 1150))


def _manos():
    manos, lado = [(4.2, A_X)], A_X
    for i, tb in enumerate(BOTES):
        lado = B_X if lado == A_X else A_X
        manos.append(((tb + BOTES[i + 1]) / 2 if i + 1 < len(BOTES) else tb + 0.36, lado))
    return manos


MANOS = _manos()


def _amarilla(T):
    if T < 4.2:
        k = int(T // 0.9); u = (T - k * 0.9) / 0.9
        x0, x1 = (A_X, B_X) if k % 2 == 0 else (B_X, A_X)
        return x0 + (x1 - x0) * u, MANO_Y - 300 * 4 * u * (1 - u)
    for i, tb in enumerate(BOTES):
        ta, xa = MANOS[i]; tc, xc = MANOS[i + 1]
        if ta <= T <= tb:
            u = (T - ta) / (tb - ta)
            return xa + (540 - xa) * u, MANO_Y + (SUELO_Y - MANO_Y) * u * u
        if tb <= T <= tc:
            u = (T - tb) / (tc - tb)
            return 540 + (xc - 540) * u, SUELO_Y - (SUELO_Y - MANO_Y) * (1 - (1 - u) ** 2)
    if T < 4.56:
        return A_X, MANO_Y
    return MANOS[-1][1], MANO_Y


def _blanca(T):
    T = min(T, FIN_TEST - 0.3)
    k = int(T // 0.7); u = (T - k * 0.7) / 0.7
    x0, x1 = (C_X, D_X) if k % 2 == 0 else (D_X, C_X)
    return x0 + (x1 - x0) * u, MANO2_Y + (SUELO2_Y - MANO2_Y) * (1 - abs(1 - 2 * u)) ** 0.8


def _astro(T):
    u = min(max((T - 5.4) / 5.4, 0), 1)
    return -260 + 1600 * u, 1185 - 10 * abs(((T * 2.4) % 2) - 1)


def _muestras(d, paso=1 / 15):
    n = max(2, int(d / paso) + 1)
    return [min(d, i * paso) for i in range(n + 1)]


def _keys(fn, d):
    t0 = D._V.ini
    return [{"t": round(t, 3), "x": round(fn(t0 + t)[0], 1), "y": round(fn(t0 + t)[1], 1), "ease": "lineal"} for t in _muestras(d)]


def _ang_brazo(T, hombro, idle, bola):
    """Ángulo del brazo: apunta a la pelota cuando está cerca; si no, se balancea."""
    bx, by = bola(T)
    dx, dy = bx - hombro[0], by - hombro[1]
    dist = math.hypot(dx, dy)
    apunta = math.degrees(math.atan2(-dx, max(dy, 1)))
    w = min(max((330 - dist) / 130, 0), 1)
    return w * apunta + (1 - w) * (idle + 6 * math.sin(T * 5 + hombro[0]))


def _muneco(nombre, brazo, x, y, ancho, bola, d, z, lado_dentro):
    """Muñeco con brazos que siguen la pelota y pupilas que la miran."""
    t0 = D._V.ini; k = ancho / 360
    hy = y + (272 - 380) * k
    h_in, h_out = (x + 85 * k * lado_dentro, hy), (x - 85 * k * lado_dentro, hy)
    cab = (x, y + (150 - 380) * k)
    def bob(T): return y + 4 * math.sin(T * 7 + x)
    ks_cuerpo = [{"t": round(t, 3), "y": round(bob(t0 + t), 1), "ease": "lineal"} for t in _muestras(d, 0.1)]
    ks_in = [{"t": round(t, 3), "rot": round(_ang_brazo(t0 + t, h_in, -18 * lado_dentro, bola), 1), "ease": "lineal"} for t in _muestras(d)]
    ks_out = [{"t": round(t, 3), "rot": round(14 * lado_dentro + 8 * math.sin((t0 + t) * 4 + x), 1), "ease": "lineal"} for t in _muestras(d, 0.1)]
    def pup(T):
        bx, by = bola(T)
        return x + max(-11, min(11, (bx - cab[0]) / 25)), bob(T) + max(-8, min(8, (by - cab[1]) / 40))
    ks_pup = [{"t": round(t, 3), "x": round(pup(t0 + t)[0], 1), "y": round(pup(t0 + t)[1], 1), "ease": "lineal"} for t in _muestras(d)]
    ab = 120 * k
    return [IMG(brazo, ancho=ab, x=h_out[0], y=h_out[1], z=z - 0.01, keys=ks_out),
            IMG(nombre, ancho=ancho, x=x, y=y, z=z, keys=ks_cuerpo),
            IMG("pupilas", ancho=ancho, x=x, y=y, z=z + 0.005, keys=ks_pup),
            IMG(brazo, ancho=ab, x=h_in[0], y=h_in[1], z=z + 0.01, keys=ks_in)]


def escena(d, zoom=False):
    """La escena del test (mismo instante en cualquier plano)."""
    t0 = D._V.ini
    def op_nar(T): return min(max((T - 2.5) / 9.0, 0), 1)
    def paso(T): return 1 if int(T * 4) % 2 else 0
    ts = _muestras(d)
    return [BG("esc_azul"), {**BG("esc_naranja", z=0.06), "keys": [{"t": 0, "op": op_nar(t0), "ease": "lineal"}, {"t": d, "op": op_nar(t0 + d)}]},
            IMG("astro_c0", ancho=290, z=0.3, keys=[{**k, "op": 1 - paso(t0 + k["t"])} for k in _keys(_astro, d)]),
            IMG("astro_c1", ancho=290, z=0.3, keys=[{**k, "op": paso(t0 + k["t"])} for k in _keys(_astro, d)]),
            *_muneco("mu_c", "br_c", PC, 1190, 250, _blanca, d, 0.35, 1), *_muneco("mu_d", "br_d", PD, 1190, 250, _blanca, d, 0.35, -1),
            IMG("pel_blanca", ancho=70, z=0.42, keys=_keys(_blanca, d)),
            *_muneco("mu_a", "br_a", PA, 1200, 300, _amarilla, d, 0.5, 1), *_muneco("mu_b", "br_b", PB, 1200, 300, _amarilla, d, 0.5, -1),
            IMG("pel_amarilla", ancho=86, z=0.6, keys=_keys(_amarilla, d))]


def quietos(extra=(), op=1.0):
    """Los dos jugadores de la amarilla quietos (para los planos después del test)."""
    els = []
    for nm, br, x, lado in (("mu_a", "br_a", PA, 1), ("mu_b", "br_b", PB, -1)):
        k = 300 / 360; hy = 1200 + (272 - 380) * k
        els += [IMG(br, ancho=100, x=x - 71 * lado, y=hy, z=0.49, rot=14 * lado, op=op), IMG(nm, ancho=300, x=x, y=1200, z=0.5, op=op),
                IMG("pupilas", ancho=300, x=x, y=1200, z=0.505, op=op), IMG(br, ancho=100, x=x + 71 * lado, y=hy, z=0.51, rot=-18 * lado, op=op)]
    return els + list(extra)


def gente(n=10, marcados=(), y=1300):
    """Fila de siluetas; las de `marcados` se encienden en ámbar."""
    els = []
    for i in range(n):
        x = 100 + i * 98
        marc = i in marcados
        els.append(IMG("persona_pie_clara" if not marc else "persona_pie_ambar", ancho=80, x=x, y=y, z=0.5, keys=aparece(0.05 + i * 0.04)))
    return els


# ================================================================== PLANOS · el test
@v.plano(0, "el test entero en UN SOLO PLANO FIJO (sin cortes ni zoom: Jorge, «no cambies el plano en los botes»)")
def _(d):
    return P(["#1a2a6a", "#2f55b0"], escena(d), CAM_TEST, vineta=0.45, energia=0.6,
             hud=[{**rotulo(1.9, 4.4, "SOLO LA AMARILLA", tam=78, color="#141414", capsula="#ffd23fe6", y=560), "fijo": True, "sin_pop": True}],
             sfx=[(0.02, "pop", -18)] + [(tb, "golpe", -22) for tb in BOTES])


# ================================================================== PLANOS · la revelación
@v.plano(27, "¿cuántos botes has contado?: el bocadillo aparece sobre la escena quieta")
def _(d):
    return P(NAR, [BG("esc_naranja"), *quietos(), IMG("pel_amarilla", ancho=86, x=B_X, y=MANO_Y, z=0.6, keys=late(0.1, 2)),
                   IMG("bocadillo", ancho=520, x=540, y=760, z=0.7, keys=aparece(0.3))],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[amarillo(0.05, d - 0.05, "¿CUÁNTOS?", y=1640 - 300, tam=120, color="#ffd23f")], sfx=[(0.3, "pop", -18)])


@v.plano(31, "apúntalo: el bocadillo late")
def _(d):
    return P(OSC, [IMG("bocadillo", ancho=760, x=540, y=1000, z=0.6, keys=late(0.0, 1))], cam(1.0, 1.06, (540, 1000)), "corte", sfx=[(0.02, "pop", -20)])


@v.plano(32, "ahora, la pregunta de verdad: fogonazo y pantalla oscura")
def _(d):
    return P(OSC, [brillo(540, 1000, 600, "#ff3df2", 0.4, 0.06, pulso=[0.12, 0.8])], cam(1.0, 1.08, (540, 1000)), "corte",
             hud=[rotulo(0.05, d - 0.05, "LA PREGUNTA DE VERDAD", tam=84, color="#ffffff", capsula="#c0397ae6", y=1000)], sfx=[(0.02, "subida", -16, {"dur": d})])


@v.plano(37, "¿has visto al astronauta?: la escena repetida con el astronauta rodeado")
def _(d):
    return P(AZUL, [BG("esc_azul"), {**BG("esc_naranja", z=0.06), "op": 0.6},
                    IMG("astro_c0", ancho=290, z=0.3, keys=[{"t": 0, "x": 380, "y": 1185}, {"t": d, "x": 700, "y": 1185, "ease": "lineal"}]),
                    *quietos(op=0.45),
                    {**senala(540, 1180, 0.3, d - 0.1, 240, MAGENTA), "keys": [{"t": 0.3, "escala": 1.6, "op": 0, "x": 460}, {"t": 0.55, "escala": 1.0, "op": 1, "ease": "golpe"}, {"t": d, "x": 700, "op": 1}]}],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[amarillo(0.4, d - 0.05, "¿EL ASTRONAUTA?", y=560, tam=110, color=MAGENTA)], sfx=[(0.3, "impacto", -16)])


@v.plano(46, "¿y que el fondo ha pasado de azul a naranja?: el fondo cambia ante tus ojos")
def _(d):
    return P(AZUL, [BG("esc_azul"), {**BG("esc_naranja", z=0.06), "keys": [{"t": 0, "op": 0}, {"t": d * 0.8, "op": 1, "ease": "suave"}]}, *quietos()],
             cam(1.0, 1.04, (540, 1100)), "corte", hud=[rotulo(0.1, d * 0.45, "AZUL", tam=120, color="#ffffff", capsula="#2a4a9ae6", y=560),
                                                       rotulo(d * 0.5, d - 0.05, "NARANJA", tam=120, color="#141414", capsula="#ff9a3ae6", y=560)], sfx=[(0.1, "brillo", -20)])


@v.plano(56, "si no, tranquilo: le pasa a casi todo el mundo: una fila de gente aparece")
def _(d):
    return P(OSC, [brillo(540, 1200, 600, "#7df9ff", 0.25, 0.06), *gente(10, (), 1250)], cam(1.0, 1.05, (540, 1200)), "corte",
             hud=[amarillo(0.4, d - 0.05, "CASI TODOS", y=560, tam=120, color=CIAN)], sfx=[(0.1, "pop", -22)])


@v.plano(66, "se llama ceguera por falta de atención: un foco ilumina solo un trozo del cerebro")
def _(d):
    return P(OSC, [IMG("cerebro", ancho=820, x=540, y=1100, z=0.4, op=0.35), brillo(420, 1050, 260, "#fff6c0", 0.8, 0.5, keys=[{"t": 0, "x": 380}, {"t": d, "x": 640, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1100)), "desenfoque", hud=[rotulo(0.2, d - 0.05, "CEGUERA", tam=130, color="#141414", capsula="#ffd23fe6", y=560), rotulo(0.8, d - 0.05, "POR FALTA DE ATENCIÓN", tam=64, color="#ffffff", capsula="#000000b0", y=720)],
             sfx=[(0.1, "roce", -20)])


@v.plano(73, "en mil novecientos noventa y nueve: el calendario corre hasta 1999")
def _(d):
    return P(["#0a1a2a", "#020610"], [BG("bg_estudio"), IMG("calendario", ancho=600, x=540, y=1100, z=0.5, keys=aparece(0.0))],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[contador(0.05, d - 0.03, 1980, 1999, d * 0.6, "", y=560, tam=150, color="#ffd23f", miles=False)],
             sfx=[(0.05, "tictac", -22, {"dur": d * 0.6, "ritmo": 0.07})])


@v.plano(79, "dos psicólogos pidieron contar pases de baloncesto: jugadores se pasan el balón en un gimnasio")
def _(d):
    t = d / 3
    return P(["#5a3a2a", "#2a1a10"], [BG("bg_gimnasio"), IMG("jugador_a", ancho=320, x=300, y=1300, z=0.5), IMG("jugador_b2", ancho=320, x=780, y=1300, z=0.5),
                                      IMG("balon_moderno", ancho=110, z=0.6, keys=[{"t": 0, "x": 360, "y": 1060}, {"t": t, "x": 720, "y": 1060, "ease": "suave"}, {"t": 2 * t, "x": 360, "y": 1060, "ease": "suave"}, {"t": d, "x": 720, "y": 1060, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[rotulo(0.3, d - 0.05, "CUENTA LOS PASES", tam=86, color="#141414", capsula="#ffd23fe6", y=560)],
             sfx=[(t, "golpe", -24), (2 * t, "golpe", -24)])


@v.plano(90, "en mitad del vídeo, alguien disfrazado de gorila cruzaba")
def _(d):
    return P(["#5a3a2a", "#2a1a10"], [BG("bg_gimnasio"), IMG("jugador_a", ancho=320, x=230, y=1300, z=0.5), IMG("jugador_b2", ancho=320, x=850, y=1300, z=0.5),
                                      IMG("gorila", ancho=420, y=1220, z=0.45, keys=[{"t": 0, "x": -150}, {"t": d, "x": 540, "ease": "salida"}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[amarillo(0.3, d - 0.05, "¡UN GORILA!", y=560, tam=120, color="#ffd23f")], sfx=[(0.1, "golpe", -22), (0.6, "golpe", -22)])


@v.plano(99, "se paraba y se golpeaba el pecho")
def _(d):
    n = 4
    ks_a = [{"t": round(d * i / n, 3), "op": 1 if i % 2 == 0 else 0} for i in range(n + 1)]
    ks_b = [{"t": round(d * i / n, 3), "op": 0 if i % 2 == 0 else 1} for i in range(n + 1)]
    return P(["#5a3a2a", "#2a1a10"], [BG("bg_gimnasio"), IMG("gorila", ancho=520, x=540, y=1200, z=0.5, keys=ks_a), IMG("gorila_golpe", ancho=520, x=540, y=1200, z=0.51, keys=ks_b)],
             cam(1.15, 1.25, (540, 1050), temblor=3), "corte", sfx=[(d * i / n, "golpe", -16) for i in range(1, n, 1)])


@v.plano(106, "más o menos la mitad no lo vio: la mitad de la fila se apaga")
def _(d):
    return P(OSC, [brillo(540, 1200, 600, "#ffd23f", 0.25, 0.06), *gente(10, (0, 2, 4, 6, 8), 1250)], cam(1.0, 1.04, (540, 1200)), "corte",
             hud=[rotulo(0.3, d - 0.05, "≈ LA MITAD", tam=110, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.2, "ding", -20)])


@v.plano(114, "en dos mil trece lo probaron con radiólogos: el escáner del hospital")
def _(d):
    return P(["#0a2a2a", "#02100a"], [BG("bg_lab"), IMG("escaner", ancho=900, x=540, y=1150, z=0.5, keys=aparece(0.0))], cam(1.0, 1.06, (540, 1150)), "corte",
             hud=[contador(0.05, d - 0.03, 2000, 2013, d * 0.5, "", y=560, tam=140, color=CIAN, miles=False)], sfx=[(0.05, "senal", -22)])


@v.plano(122, "escondieron un gorila: la imagen de pulmón")
def _(d):
    return P(OSC, [BG("tac_pulmon")], cam(1.0, 1.08, (540, 1000)), "corte", sfx=[(0.05, "senal", -22)])


@v.plano(124, "micro: «gorila», zoom al gorila diminuto escondido en el pulmón")
def _(d):
    return P(OSC, [BG("tac_pulmon"), senala(733, 890, 0.05, d - 0.05, 60, MAGENTA)], cam(3.5, 4.0, (733, 890)), "corte", sfx=[(0.05, "impacto", -16)])


@v.plano(126, "del tamaño de una caja de cerillas: la caja aparece al lado")
def _(d):
    return P(OSC, [BG("tac_pulmon"), IMG("caja_cerillas", ancho=360, x=540, y=1520, z=0.6, keys=aparece(0.1)), senala(733, 890, 0.05, d - 0.05, 60, MAGENTA)],
             cam(1.1, 1.15, (600, 1100)), "corte", hud=[rotulo(0.4, d - 0.05, "CAJA DE CERILLAS", tam=80, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "pop", -20)])


@v.plano(137, "ochenta y tres de cada cien no lo vieron: la cifra corre")
def _(d):
    return P(OSC, [BG("tac_pulmon"), {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#000000", "op": 0.5, "x": 540, "y": 960, "z": 0.2}],
             cam(1.0, 1.04, (540, 1000)), "corte", hud=[contador(0.05, d - 0.03, 0, 83, d * 0.6, " %", y=1000, tam=200, color=MAGENTA, capsula="#000000a0"),
                                                       rotulo(d * 0.6, d - 0.05, "NO LO VIO", tam=90, color="#ffffff", capsula="#c0397ae6", y=1300)], sfx=[(0.05, "subida", -18, {"dur": d * 0.6})])


@v.plano(146, "aunque sus ojos pasaron por encima: el ojo y el recorrido de la mirada por el pulmón")
def _(d):
    return P(OSC, [BG("tac_pulmon"), IMG("ojo_mira", ancho=520, x=540, y=560, z=0.6, keys=aparece(0.0)),
                   flecha([[300, 900], [500, 1000], [700, 880], [740, 900], [620, 1150], [400, 1100]], 0.1, d * 0.85, CIAN, 6, disc=[18, 12], z=0.6)],
             cam(1.0, 1.04, (540, 1000)), "corte", sfx=[(0.1, "roce", -20)])


@v.plano(152, "comenta cuántos botes contaste: la escena del test otra vez (bucle) con el bocadillo")
def _(d):
    return P(AZUL, [BG("esc_azul"), *quietos(),
                    IMG("pel_amarilla", ancho=86, z=0.6, keys=[{"t": 0, "x": A_X, "y": MANO_Y}, {"t": d * 0.5, "x": 540, "y": MANO_Y - 320, "ease": "salida"}, {"t": d, "x": B_X, "y": MANO_Y, "ease": "entrada"}]),
                    IMG("bocadillo", ancho=460, x=540, y=700, z=0.7, keys=aparece(0.2))],
             cam(1.0, 1.04, (540, 1150)), "corte", sfx=[(0.2, "pop", -18)])


import json as _json  # noqa: E402
_v_construir = v.construir


def _construir_sin_empujon(*a, **k):
    r = _v_construir(*a, **k)
    ruta = os.path.join(sys.argv[1], "episodio.json")
    ep = _json.load(open(ruta))
    ep["escenas"][0]["camara"] = {**ep["escenas"][0]["camara"], "zoom": list(CAM_TEST["zoom"])}
    _json.dump(ep, open(ruta, "w"), ensure_ascii=False)
    print("  ⇢ plano del test fijo: sin el empujón automático de cámara (petición de Jorge)")
    return r


v.construir = _construir_sin_empujon
v.construir("2026-11-22-tarde-03-test-astronauta", version=2, bucle=0.35, musica={"generar": "curiosidad", "semilla": 83, "db": -14},
            claves=["botes", "amarillos", "amarilla", "uno", "dos", "rápido", "mano", "deprisa", "contado", "astronauta", "azul", "naranja", "ceguera", "atención",
                    "noventa", "baloncesto", "gorila", "pecho", "mitad", "trece", "radiólogos", "cerillas", "pulmón", "ochenta", "tres", "ojos", "comenta"])
