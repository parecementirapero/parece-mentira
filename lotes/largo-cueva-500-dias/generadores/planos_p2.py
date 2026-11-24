"""Parte 2 (palabras 287–582): «Tu cuerpo tiene un reloj interno…» … «Tus días ya no son días.»

Relojes: solo dos escenas en esta parte (y en todo el vídeo): «reloj interno» (287) y «va por libre» (317), separadas.
El resto del tiempo se enseña con barras, contadores, lunas, hojas de calendario, estaciones y rayas de tiza.
"""
import random

from comun import *  # noqa: F401,F403
import comun

FRIO = "#bfe2ff"
CALIDO = "#ffcf8a"


# ------------------------------------------------------------------ ayudantes propios de la parte 2
def _sin(ks, *props):
    """Copia unas claves quitando algunas propiedades (para que una pieza siga a otra sin heredar su giro)."""
    out = []
    for q in ks:
        q2 = {k: v for k, v in q.items() if k not in props}
        if len(q2) > 1 or "t" not in q2:
            out.append(q2)
    return out


def nieve(n=60, sem=1, z=0.88):
    """Copos que caen por todo el ancho (también en los laterales del horizontal)."""
    return {**polvo("#ffffff", n, (-600, 300, 1680, 1700), sem), "vel": [14, 95], "tam": [3, 7], "z": z, "_ancho": True}


def hielo(d, sem=1, gotas=True):
    """Lo que vive en la cueva helada: polvo de escarcha azulado, gotas de deshielo y frío en los laterales."""
    r = random.Random(sem)
    out = [{**polvo("#cfeaff", 30, (-500, 500, 1580, 1500), sem), "vel": [4, 22]}]
    if gotas:
        for j, x in enumerate([-380, 210, 880, 1400]):
            out.append(goteo(x + r.uniform(-40, 40), 470, 1330, r.uniform(2.4, 3.8), r.uniform(0, 3), d, z=0.72, suena=(j == 1)))
    out += [brillo(-350, 1000, 380, "#7fbfff", 0.25, 0.07), brillo(1430, 980, 380, "#7fbfff", 0.25, 0.07)]
    return out


def suelo_lados(suelo, sem=1, z=0.56):
    """Rocas/estalagmitas posadas en los laterales del horizontal."""
    r = random.Random(sem)
    out = []
    for x in (-520, -260, 1330, 1580):
        n = r.choice(["estalagmita_a", "estalagmita_b"])
        out.append(pie(n, x + r.uniform(-40, 40), suelo + 10, r.uniform(170, 300), z=z))
    return out


def hoja_notas(d, n0, n1, icono=None, t_ic=0.12, rot=-4):
    """Hoja del equipo de arriba: renglones que se escriben (de n0 a n1) y un icono que se estampa."""
    out = [{"tipo": "forma", "forma": "redondeado", "ancho": 640, "alto": 800, "relleno": "#f2ead6", "x": 540, "y": 960, "z": 0.5,
            "esquinas": 12, "rot": rot, "keys": K(d, (0, {"rot": rot}), (1, {"rot": rot + 1.5}))}]
    for i in range(n1):
        y = 640 + i * 70
        t = 0.0 if i < n0 else 0.05 + (i - n0) * min(0.18, d * 0.6 / max(1, n1 - n0))
        largo = 420 - (i * 37) % 140
        if icono and i == n1 - 1:
            largo = 250
        x = 330 + largo / 2
        out.append({"tipo": "forma", "forma": "redondeado", "ancho": largo, "alto": 12, "relleno": "#3a3428", "x": x,
                    "y": y, "z": 0.52, "rot": rot,
                    "keys": [{"t": 0, "ex": 1.0 if i < n0 else 0.0}, {"t": round(t, 3), "ex": 1.0 if i < n0 else 0.0},
                             {"t": round(t + 0.16, 3), "ex": 1.0, "ease": "salida"}]})
    if icono:
        out.append(pieza(icono, 720, 640 + (n1 - 1) * 70, 170, z=0.55, keys=aparece(t_ic, 0.35)))
    out.append(brillo(540, 900, 520, "#fff6e0", 0.25, 0.07))
    return out


def barra(x, y, ancho, alto, color, t0, t1, p1=1.0, fondo_c="#ffffff22", z=0.6, p0=0.0):
    return {"tipo": "barra", "x": x, "y": y, "ancho": ancho, "alto": alto, "color": color, "fondo": fondo_c, "z": z,
            "keys": [{"t": 0, "progreso": p0}, {"t": t0, "progreso": p0}, {"t": t1, "progreso": p1, "ease": "lineal"}]}


def planos(v, plano):
    w = v.w

    def T(i):
        """Segundo de la palabra i dentro del plano que se está montando."""
        return round(max(0.02, w(i) - comun.D._V.ini), 3)

    comun.VUELOS += [(w(479), w(479) + 6.5, (1350, 560), (-300, 500), 140), (w(563), w(563) + 6, (-300, 520), (1350, 600), 130)]

    # ============================================================== 1. EL RELOJ INTERNO
    @plano(287, "reloj interno (escena de reloj 1/2)")
    def _(d):
        ks = arranque(650, 1110, d, "abajo", 320, 30)
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_cerebro"),
            brillo(650, 1110, 440, "#ffd59a", 0.45, 0.1, pulso=[0.1, 0.9]),
            pieza("reloj_interno", 650, 1110, 480, z=0.6, keys=ks),
            pieza("aguja_interna", 650, 1110, 36, z=0.62, keys=_sin(ks, "rot") + [{"t": 0, "rot": -540}, {"t": d * 0.8, "rot": 0, "ease": "salida"}]),
            {**polvo("#ffd9a0", 30, (-500, 400, 1580, 1600), 7), "vel": [10, -30]},
            brillo(-380, 700, 200, MAGENTA, 0.3, 0.08, pulso=[0.2, 1.3]), brillo(1460, 1250, 220, CIAN, 0.3, 0.08, pulso=[0.2, 1.1])],
            cam(1.0, 1.2, (650, 1200)), "corte",
            sfx=[(0.0, "golpe", -18), (0.05, "tictac", -24, {"dur": d * 0.75, "ritmo": 0.07})])

    @plano(293, "pero necesita que lo pongan: el núcleo del cerebro, a oscuras", mas=0.2)
    def _(d):
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_seccion_cabeza"),
            pieza("cerebro", 525, 700, 400, z=0.5, keys=K(d, (0, {"escala": 0.8, "op": 0.6}), (0.3, {"escala": 1.0, "op": 1, "ease": "salida"}))),
            brillo(560, 720, 90, "#ffb15e", 0.9, 0.55, pulso=[0.5, 0.6]),
            senala(560, 720, d * 0.35, d - 0.1, 80, AMBAR),
            {**polvo("#2ff3ff", 20, (-500, 400, 1580, 1500), 9), "vel": [6, -12]}],
            cam(1.0, 1.18, (520, 820), (540, 760)), "corte", sfx=[(d * 0.35, "zap", -26)])

    @plano(299, "que lo pongan en hora: sale el sol")
    def _(d):
        s = sol(540, 1150, 120, z=0.2)
        for e in s:
            e["keys"] = K(d, (0, {"y": 1150}), (1, {"y": 930, "ease": "salida"}))
        return P(["#f7a85c", "#2b1a2e"], [
            fondo("bg_amanecer"), *s,
            brillo(540, 980, 700, "#ffd59a", 0.5, 0.15, keys=K(d, (0, {"op": 0.3}), (1, {"op": 1.0}))),
            {**polvo("#fff1c8", 30, (-500, 500, 1580, 1500), 4), "vel": [10, -20]}],
            cam(1.12, 1.0, (540, 1000), (540, 960)), "corte", sfx=[(0.05, "brillo", -22)])

    @plano(304, "cada mañana: la luz le da en la cara")
    def _(d):
        return P(["#f7a85c", "#2b1a2e"], [
            fondo("bg_amanecer"),
            pieza("bea_cara_luz", 540, 1010, 960, z=0.6, keys=arranque(540, 1010, d, "abajo", 90, 20)),
            brillo(140, 760, 380, "#fff3d0", 0.75, 0.7, keys=K(d, (0, {"x": -100, "op": 0.2}), (0.5, {"x": 180, "op": 1.0, "ease": "salida"}))),
            fundido_blanco(K(d, (0, {"op": 0.5}), (0.3, {"op": 0.0})))],
            cam(1.0, 1.1, (540, 900)), "corte", sfx=[(0.0, "brillo", -24)])

    @plano(306, "quien lo pone en hora: el ojo se abre")
    def _(d):
        return P(["#f7a85c", "#2b1a2e"], [
            fondo("bg_amanecer"), brillo(540, 960, 560, "#ffd59a", 0.5, 0.2),
            pieza("ojo", 540, 960, 920, z=0.6, keys=K(d, (0, {"ey": 0.08}), (0.3, {"ey": 1.0, "ease": "elastico"}))),
            {**polvo("#fff1c8", 26, (-500, 600, 1580, 1300), 5), "vel": [8, -10]}],
            cam(1.0, 1.15, (540, 960)), "corte", sfx=[(0.05, "roce", -24)])

    @plano(312, "es el sol: el rayo entra por el ojo")
    def _(d):
        return P(["#f7a85c", "#2b1a2e"], [
            fondo("bg_amanecer"),
            pieza("sol_dibujo", 110, 960, 330, z=0.55, keys=K(d, (0, {"rot": 0}), (1, {"rot": 25}))),
            pieza("rayo_sol", 280, 960, 860, z=0.58, keys=K(d, (0, {"x": -220, "op": 0}), (0.3, {"x": 280, "op": 1, "ease": "salida"}))),
            pieza("ojo", 760, 960, 640, z=0.6, keys=late(0.3, 1, 0.06, 0.4)),
            pieza("destello", 700, 960, 300, z=0.62, keys=aparece(0.3, 0.3) + [{"t": d, "op": 0.6}]),
            pieza("sol_dibujo", -420, 700, 260, z=0.4, op=0.6), {**polvo("#fff1c8", 30, (-500, 500, 1580, 1500), 6)}],
            cam(1.0, 1.12, (600, 960)), "corte", sfx=[(0.3, "brillo", -18)])

    @plano(315, "sin sol: el sol se apaga")
    def _(d):
        return P(["#141018", "#050507"], [
            fondo("bg_negro_cueva"),
            brillo(540, 960, 400, "#ffcf6a", 0.6, 0.1, keys=K(d, (0, {"op": 1}), (0.8, {"op": 0}))),
            pieza("sol_dibujo", 540, 960, 420, z=0.6, keys=K(d, (0, {"escala": 1.0, "op": 1, "rot": 0}), (0.85, {"escala": 0.35, "op": 0.0, "rot": -40, "y": 1060, "ease": "entrada"}))),
            IMG("estalactita_c", ancho=180, x=-350, y=430, z=0.8), IMG("estalactita_b", ancho=140, x=1400, y=420, z=0.8)],
            cam(1.0, 1.06, (540, 960)), "corte", sfx=[(0.05, "zap", -22)])

    @plano(317, "tu reloj va por libre (escena de reloj 2/2)")
    def _(d):
        giros = [(0, 0), (0.12, 160), (0.25, 70), (0.4, 330), (0.52, 250), (0.68, 560), (0.8, 470), (1.0, 830)]
        ag = [{"t": round(f * d, 3), "rot": r, "ease": "suave"} for f, r in giros]
        caja = K(d, (0, {"rot": -3, "escala": 1.0}), (0.3, {"rot": 4}), (0.6, {"rot": -5}), (1, {"rot": 3, "escala": 1.06}))
        return P(["#10141f", "#050507"], [
            fondo("bg_negro_cueva"),
            brillo(540, 1000, 420, "#9fc4ff", 0.35, 0.1, pulso=[0.15, 0.5]),
            pieza("reloj_interno", 540, 1000, 560, z=0.6, op=0.85, keys=caja),
            pieza("aguja_interna", 540, 1000, 42, z=0.62, keys=ag),
            negro(K(d, (0, {"op": 0.0}), (0.6, {"op": 0.0}), (1, {"op": 0.45}))),
            *ambiente_cueva(d, sem=21, oscura=True, murc=False)],
            cam(1.0, 1.14, (540, 1000), temblor=4), "corte",
            sfx=[(0.05, "tictac", -24, {"dur": d * 0.45, "ritmo": 0.11}), (d * 0.5, "tictac", -25, {"dur": d * 0.45, "ritmo": 0.31})])

    # ============================================================== 2. MICHEL SIFFRE, 1962
    @plano(324, "lo descubrió: un haz de luz en la cueva helada")
    def _(d):
        return P(["#22405e", "#0d1b2e"], [
            fondo("bg_cueva_hielo"),
            pieza("haz_frontal", 520, 1000, 1000, z=0.6, keys=K(d, (0, {"rot": -18, "op": 0.4}), (1, {"rot": 12, "op": 1.0, "ease": "suave"}))),
            brillo(800, 950, 260, "#e8f6ff", 0.5, 0.55, keys=K(d, (0, {"y": 1150}), (1, {"y": 850}))),
            *hielo(d, sem=24)],
            cam(1.1, 1.0, (540, 1000)), "corte", sfx=[(0.02, "roce", -24)])

    @plano(326, "en 1962: llega la tienda a la nieve")
    def _(d):
        return P(["#a9d6f5", "#e8f6ff"], [
            fondo("bg_alpes_nieve"),
            pie("tienda_1962", 540, 1340, 300, z=0.5, keys=cae(0.25, 0.85, 900, 1340 - 0.4 * 300 + 30)),
            pie("mochila", 820, 1345, 150, z=0.52, keys=aparece(0.9)),
            pie("tienda_1962", -380, 1300, 200, z=0.45), pie("mochila", 1450, 1320, 150, z=0.45),
            nieve(60, 26)],
            cam(1.0, 1.1, (540, 1000), (540, 1080)), "corte",
            hud=[contador(0.05, d - 0.05, 1900, 1962, d * 0.55, "", tam=150, x=540, y=760, color="#ffffff", capsula="#0d1b2ed8", miles=False)],
            sfx=[(0.85 - 0.15, "golpe", -20), (0.05, "tictac", -28, {"dur": d * 0.5, "ritmo": 0.06})])

    @plano(332, "un francés de 23 años: Siffre camina por la nieve")
    def _(d):
        return P(["#a9d6f5", "#e8f6ff"], [
            fondo("bg_alpes_nieve"),
            pie("tienda_1962", 860, 1300, 190, z=0.45),
            pie("siffre_camina", 300, 1360, 600, z=0.55, keys=K(d, (0, {"x": 180}), (1, {"x": 520, "ease": "lineal"})) + late(0.0, 3, 0.02, d / 3)),
            pie("huellas", 120, 1380, 80, z=0.5, keys=aparece(0.2)), pie("huellas", -60, 1385, 80, z=0.5),
            pie("equipo_1962", 1500, 1300, 300, z=0.45), nieve(60, 32)],
            cam(1.0, 1.1, (400, 1050), (560, 1050)), "corte",
            hud=[contador(0.1, d - 0.05, 0, 23, d * 0.6, " años", tam=120, x=560, y=560, color="#ffffff", capsula="#0d1b2ed8")],
            sfx=[(0.1, "roce", -26), (d * 0.5, "roce", -27)])

    @plano(337, "llamado Michel Siffre: primer plano")
    def _(d):
        return P(["#a9d6f5", "#e8f6ff"], [
            fondo("bg_alpes_nieve"),
            brillo(380, 760, 420, "#e8f6ff", 0.5, 0.3),
            pieza("siffre_cara", 540, 1000, 960, z=0.6, keys=arranque(540, 1000, d, "derecha", 300, 25)),
            nieve(50, 37, z=0.9)],
            cam(1.0, 1.12, (540, 900)), "corte", sfx=[(0.02, "golpe", -22)])

    @plano(340, "se metió solo en una cueva")
    def _(d):
        return P(["#22405e", "#0d1b2e"], [
            fondo("bg_cueva_hielo"),
            pie("siffre_camina", 540, 1420, 620, z=0.55, keys=K(d, (0, {"escala": 1.0, "y": 1420 - 0.47 * 620, "x": 420}),
                                                                 (1, {"escala": 0.55, "y": 1250 - 0.47 * 620 * 0.55, "x": 600, "ease": "lineal"}))),
            brillo(700, 1000, 220, "#fff1c8", 0.6, 0.56, keys=K(d, (0, {"x": 700, "y": 900}), (1, {"x": 680, "y": 1060}))),
            *hielo(d, sem=40)],
            cam(1.0, 1.15, (540, 1150)), "corte", sfx=[(0.1, "roce", -25), (d * 0.6, "roce", -27)])

    @plano(345, "helada, de los Alpes: las montañas")
    def _(d):
        return P(["#5f9fd1", "#e8f6ff"], [
            fondo("bg_alpes_nieve"),
            pie("tienda_1962", 560, 1340, 110, z=0.5),
            brillo(820, 520, 360, "#ffffff", 0.4, 0.1),
            nieve(90, 45, z=0.9)],
            cam(1.45, 1.0, (540, 700), (540, 1000)), "corte", sfx=[(0.0, "rumor", -26, {"dur": 1.3})])

    @plano(350, "a 130 metros de profundidad, y pasó allí")
    def _(d):
        return P(["#22405e", "#07090f"], [
            fondo("bg_cueva_pozo"),
            brillo(540, 900, 700, "#5f9fd1", 0.45, 0.1),
            flecha([[540, 460], [540, 1330]], 0.15, d * 0.55, CIAN, 8, [18, 14]),
            brillo(540, 470, 120, "#fff1c8", 0.9, 0.6, keys=K(d, (0, {"y": 470}), (0.6, {"y": 1320, "ease": "suave"}))),
            {**polvo("#cfeaff", 40, (200, 420, 880, 1500), 50), "vel": [4, 50]},
            IMG("estalactita_c", ancho=200, x=-260, y=430, z=0.8), IMG("estalactita_a", ancho=150, x=1350, y=400, z=0.8),
            senala(540, 1330, d * 0.62, d - 0.1, 90, CIAN)],
            cam(1.0, 1.12, (540, 900), (540, 1150)), "corte",
            hud=[contador(0.15, d - 0.05, 0, 130, d * 0.55, " m", tam=120, x=800, y=760, color="#ffffff", capsula="#0b0f1ed8", miles=False)],
            sfx=[(d * 0.62, "ding", -21)])

    @plano(359, "dos meses sin reloj: dos lunas")
    def _(d):
        return P(["#0d1b2e", "#050507"], [
            fondo("bg_negro_cueva"), brillo(540, 900, 520, "#a9d6f5", 0.3, 0.1),
            pieza("luna_creciente", 340, 900, 300, z=0.6, keys=aparece(0.05) + [{"t": d, "rot": 10}]),
            pieza("luna_creciente", 740, 900, 300, z=0.6, keys=aparece(0.55) + [{"t": d, "rot": -8}]),
            pieza("luna_creciente", -380, 860, 220, z=0.5, op=0.35), pieza("luna_creciente", 1460, 860, 220, z=0.5, op=0.35),
            estrellas(40, 59)],
            cam(1.0, 1.1, (540, 950)), "corte",
            hud=[rotulo(0.9, d - 0.05, "2 MESES", tam=110, color="#ffffff", capsula="#22405ee6", y=1200)],
            sfx=[(0.05, "brillo", -24), (0.55, "brillo", -23)])

    # ---- arriba el equipo apunta, abajo él llama
    @plano(363, "arriba, su equipo")
    def _(d):
        return P(["#a9d6f5", "#e8f6ff"], [
            fondo("bg_alpes_nieve"),
            pie("tienda_1962", 300, 1330, 260, z=0.48),
            pie("equipo_1962", 650, 1345, 430, z=0.55, keys=arranque(650, 1345 - 0.472 * 430, d, "derecha", 200, 10)),
            flecha([[820, 1280], [820, 1420], [700, 1520]], 0.2, d * 0.8, CIAN, 6, [14, 12]),
            pie("tienda_1962", -360, 1300, 220, z=0.45), pie("mochila", 1400, 1330, 160, z=0.45),
            nieve(70, 63)],
            cam(1.0, 1.12, (540, 1100), (620, 1150)), "corte", sfx=[(0.05, "roce", -25)])

    @plano(366, "apuntaba: la hoja de notas")
    def _(d):
        return P(["#a9d6f5", "#e8f6ff"], [
            fondo("bg_alpes_nieve"), *hoja_notas(d, 2, 4), nieve(40, 66)],
            cam(1.15, 1.25, (540, 900)), "corte", sfx=[(0.05, "trazo", -24), (0.25, "trazo", -25)])

    @plano(367, "cada vez que él: suena el teléfono de campo")
    def _(d):
        tiembla = [{"t": round(i * 0.06, 3), "rot": (5 if i % 2 else -5)} for i in range(int(d / 0.06) + 1)]
        return P(["#22405e", "#0d1b2e"], [
            fondo("bg_cueva_hielo"),
            pie("telefono_campo", 540, 1400, 420, z=0.6, keys=tiembla),
            senala(560, 1130, 0.05, d - 0.1, 220, CIAN), *hielo(d, sem=67, gotas=False)],
            cam(1.1, 1.2, (540, 1200)), "corte", sfx=[(0.02, "senal", -18)])

    @plano(371, "llamaba para decir: Siffre al teléfono, el cable sube")
    def _(d):
        return P(["#22405e", "#0d1b2e"], [
            fondo("bg_cueva_hielo"),
            pie("siffre_telefono", 500, 1400, 560, z=0.55, keys=K(d, (0, {"escala": 0.96}), (1, {"escala": 1.02}))),
            brillo(470, 1080, 200, "#fff1c8", 0.5, 0.56, pulso=[0.15, 0.7]),
            flecha([[760, 1340], [880, 1000], [880, 470]], 0.1, d * 0.85, CIAN, 6, [14, 12]),
            pie("telefono_campo", -360, 1400, 260, z=0.5), *hielo(d, sem=71)],
            cam(1.0, 1.1, (540, 1150), (600, 1050)), "corte", sfx=[(0.05, "tic", -24)])

    @plano(376, "que se despertaba: arriba lo apuntan (sol)")
    def _(d):
        return P(["#a9d6f5", "#e8f6ff"], [
            fondo("bg_alpes_nieve"), *hoja_notas(d, 4, 5, "sol_dibujo", 0.25, rot=3), nieve(40, 76)],
            cam(1.2, 1.3, (560, 980)), "corte", sfx=[(0.25, "pop", -22)])

    @plano(377, "que comía: la comida en el hielo")
    def _(d):
        return P(["#22405e", "#0d1b2e"], [
            fondo("bg_cueva_hielo"),
            pie("caja_comida", 420, 1400, 260, z=0.55, keys=cae(0.0, 0.4, 900, 1400 - 0.42 * 260)),
            pie("taza_cafe", 760, 1400, 220, z=0.56, keys=aparece(0.3)),
            brillo(600, 1250, 300, "#fff1c8", 0.4, 0.5),
            pie("mochila", -360, 1400, 220, z=0.5), *hielo(d, sem=77, gotas=False)],
            cam(1.15, 1.25, (580, 1250)), "corte", sfx=[(0.25, "golpe", -22)])

    @plano(379, "o que se iba a dormir: arriba lo apuntan (luna)")
    def _(d):
        return P(["#5f9fd1", "#22405e"], [
            fondo("bg_alpes_nieve"), *hoja_notas(d, 5, 6, "luna_creciente", 0.2, rot=-2),
            negro(K(d, (0, {"op": 0.0}), (0.4, {"op": 0.0}), (1, {"op": 0.35})), color="#0d1b2e"), nieve(40, 79)],
            cam(1.25, 1.12, (560, 1040)), "corte", sfx=[(0.2, "pop", -22)])

    # ---- la prueba de contar hasta 120
    @plano(385, "le hicieron una prueba muy simple")
    def _(d):
        return P(["#22405e", "#0d1b2e"], [
            fondo("bg_cueva_hielo"),
            pie("siffre_cuenta_a", 520, 1400, 640, z=0.55, keys=arranque(520, 1400 - 0.47 * 640, d, "izquierda", 220, 10)),
            brillo(520, 830, 240, "#fff1c8", 0.4, 0.5, pulso=[0.1, 0.9]),
            senala(520, 820, T(389), d - 0.1, 120, CIAN),
            *suelo_lados(1400, 85), *hielo(d, sem=85)],
            cam(1.0, 1.15, (520, 1100), (520, 950)), "corte", sfx=[(T(389), "ding", -24)])

    @plano(391, "contar hasta 120")
    def _(d):
        return P(["#22405e", "#0d1b2e"], [
            fondo("bg_cueva_hielo"),
            *flip(["siffre_cuenta_a", "siffre_cuenta_b"], d, fps=4, base=lambda n: pie(n, 320, 1400, 820, z=0.55,
                  keys=K(d, (0, {"x": 300}), (1, {"x": 340})))),
            brillo(750, 760, 260, CIAN, 0.3, 0.3), *hielo(d, sem=91)],
            cam(1.05, 1.15, (420, 900)), "corte",
            hud=[contador(0.05, d - 0.05, 1, 120, d * 0.85, "", tam=170, x=740, y=720, color="#ffffff", capsula="#0d1b2ed8")],
            sfx=[(0.05, "tictac", -27, {"dur": d * 0.8, "ritmo": 0.05})])

    @plano(395, "un número por segundo: una gota por segundo")
    def _(d):
        gotas = [IMG("gota", ancho=60, x=540, y=480, z=0.7, keys=[{"t": 0, "op": 0, "y": 480}, {"t": t, "op": 0, "y": 480}, {"t": t + 0.01, "op": 1},
                                                                    {"t": t + 0.5, "y": 1180, "ease": "entrada"}, {"t": t + 0.51, "op": 0}])
                 for t in (0.02, 1.0) if t < d]
        sal = [pie("salpicadura", 540, 1200, 90, z=0.7, keys=[{"t": 0, "op": 0}, {"t": t + 0.5, "op": 0, "escala": 0.4}, {"t": t + 0.55, "op": 1, "escala": 1.0},
                                                               {"t": t + 0.8, "op": 0}]) for t in (0.02, 1.0) if t + 0.5 < d]
        return P(["#0d1b2e", "#050507"], [
            fondo("bg_cueva_hielo"), negro([{"t": 0, "op": 0.45}]),
            *gotas, *sal,
            brillo(540, 860, 300, "#a9d6f5", 0.5, 0.4, keys=[{"t": 0, "op": 1}, {"t": 0.3, "op": 0.3}, {"t": 1.0, "op": 1}, {"t": 1.3, "op": 0.3}]),
            *hielo(d, sem=95, gotas=False)],
            cam(1.0, 1.08, (540, 900)), "corte",
            hud=[contador(0.02, d - 0.05, 1, 2, 1.0, "", tam=200, x=540, y=860, color="#ffffff", capsula=None)],
            sfx=[(0.02, "tic", -22), (1.0, "tic", -22), (0.52, "burbuja", -26), (1.5, "burbuja", -26)])

    # barras de «su cuenta» (cian) y «tiempo real» (ámbar) en la cueva helada
    def barras_siffre(d, p_cian, p_amb, t_amb=None):
        out = [barra(540, 780, 760, 70, CIAN, 0.05, 0.05 + 0.6, p_cian[1], p0=p_cian[0])]
        if p_amb:
            out.append(barra(540, 980, 760, 70, AMBAR, t_amb[0], t_amb[1], p_amb[1], p0=p_amb[0]))
        return out

    @plano(399, "dos minutos")
    def _(d):
        return P(["#0d1b2e", "#050507"], [
            fondo("bg_cueva_hielo"), negro([{"t": 0, "op": 0.5}]),
            *barras_siffre(d, (0.0, 0.4), None),
            pie("siffre_cuenta_b", 820, 1420, 360, z=0.55, op=0.9), *hielo(d, sem=99)],
            cam(1.0, 1.02, (540, 900)), "corte",
            hud=[rotulo(0.3, d - 0.05, "2 MIN", tam=80, color="#0d1b2e", capsula=CIAN, x=330, y=670)],
            sfx=[(0.05, "subida", -28, {"dur": 0.6})])

    @plano(401, "Siffre tardó cinco minutos")
    def _(d):
        return P(["#0d1b2e", "#050507"], [
            fondo("bg_cueva_hielo"), negro([{"t": 0, "op": 0.5}]),
            *barras_siffre(d, (0.4, 0.4), (0.0, 0.85), (0.1, d)),
            *flip(["siffre_cuenta_a", "siffre_cuenta_b"], d, fps=3, base=lambda n: pie(n, 820, 1420, 360, z=0.55)),
            *hielo(d, sem=101)],
            cam(1.02, 1.04, (540, 900)), "corte",
            hud=[rotulo(0.0, d - 0.05, "2 MIN", tam=80, color="#0d1b2e", capsula=CIAN, x=330, y=670),
                 contador(T(403), d - 0.05, 0, 5, d - T(403) - 0.1, " MIN", tam=80, color="#1a120d", capsula=AMBAR, x=380, y=1100)],
            sfx=[(0.1, "tictac", -26, {"dur": d - 0.2, "ritmo": 0.35})])

    @plano(405, "reales en terminar: la barra real llega al final")
    def _(d):
        return P(["#0d1b2e", "#050507"], [
            fondo("bg_cueva_hielo"), negro([{"t": 0, "op": 0.5}]),
            *barras_siffre(d, (0.4, 0.4), (0.85, 1.0), (0.0, 0.5)),
                        senala(910, 980, 0.5, d - 0.1, 70, AMBAR),
            pie("siffre_cuenta_a", 820, 1420, 360, z=0.55, keys=late(0.5, 1, 0.05)), *hielo(d, sem=105)],
            cam(1.04, 1.08, (540, 900)), "corte",
            hud=[rotulo(0.0, d - 0.05, "2 MIN", tam=80, color="#0d1b2e", capsula=CIAN, x=330, y=670),
                 rotulo(0.0, d - 0.05, "5 MIN", tam=80, color="#1a120d", capsula=AMBAR, x=380, y=1100)],
            sfx=[(0.5, "ding", -22)])

    @plano(408, "para él habían sido dos")
    def _(d):
        return P(["#22405e", "#0d1b2e"], [
            fondo("bg_cueva_hielo"),
            brillo(560, 760, 320, "#fff1c8", 0.35, 0.3, pulso=[0.1, 1.2]),
            pieza("siffre_cara", 540, 1020, 940, z=0.6, keys=K(d, (0, {"escala": 1.0, "rot": 0}), (1, {"escala": 1.07, "rot": -2.5}))),
            *hielo(d, sem=108, gotas=False)],
            cam(1.0, 1.12, (540, 860)), "corte", sfx=[(0.05, "roce", -26)])

    @plano(413, "cuando salió de la cueva: hacia la luz")
    def _(d):
        return P(["#3d2a1f", "#07090f"], [
            fondo("bg_salida_luz"),
            pie("siffre_camina", 520, 1440, 560, z=0.55, keys=K(d, (0, {"escala": 1.0, "y": 1440 - 0.47 * 560, "x": 470}),
                                                                 (1, {"escala": 0.6, "y": 1300 - 0.47 * 560 * 0.6, "x": 560, "ease": "lineal"}))),
            brillo(540, 720, 420, "#fff6e0", 0.7, 0.2, keys=K(d, (0, {"op": 0.6}), (1, {"op": 1.0}))),
            {**polvo("#fff1c8", 40, (200, 500, 880, 1400), 13), "vel": [6, -14]},
            fundido_blanco(K(d, (0, {"op": 0.0}), (0.65, {"op": 0.0}), (1, {"op": 0.9, "ease": "entrada"}))),
            *suelo_lados(1360, 113)],
            cam(1.0, 1.2, (540, 1000), (540, 850)), "corte", sfx=[(0.1, "roce", -25), (d * 0.7, "brillo", -22)])

    @plano(418, "creía que había pasado un mes")
    def _(d):
        return P(["#6fb6e8", "#e8f6ff"], [
            fondo("bg_alpes_nieve"), fundido_blanco(K(d, (0, {"op": 0.9}), (0.25, {"op": 0.0}))),
            pie("calendario_hoja", 540, 1300, 600, z=0.6, keys=K(d, (0, {"ex": -1.0, "rot": -8}), (0.3, {"ex": 1.0, "rot": 0, "ease": "salida"}),
                                                                  (1, {"rot": 3}))),
            pie("siffre_camina", -380, 1340, 420, z=0.5), pie("tienda_1962", 1450, 1330, 200, z=0.5), nieve(40, 118)],
            cam(1.0, 1.1, (540, 1000)), "corte",
            hud=[rotulo(0.35, d - 0.05, "¿1 MES?", tam=120, color="#1a120d", capsula=AMBAR, y=600)],
            sfx=[(0.1, "roce", -22)])

    @plano(424, "habían pasado dos: REVELACIÓN")
    def _(d):
        tg = T(426)
        return P(["#6fb6e8", "#e8f6ff"], [
            fondo("bg_alpes_nieve"),
            pie("calendario_hoja", 540, 1250, 520, z=0.6, keys=K(d, (0, {"x": 540, "rot": 3}), (0.4, {"rot": -3})) +
                [{"t": tg, "x": 330, "rot": -9, "escala": 0.85, "ease": "golpe"}]),
            pie("calendario_hoja", 760, 1270, 520, z=0.62, keys=[{"t": 0, "op": 0, "y": 300}, {"t": tg - 0.15, "op": 1, "y": 300},
                                                                   {"t": tg, "y": 1270 - 0.46 * 520 * 0.85, "escala": 0.85, "rot": 8, "ease": "entrada"}]),
            fundido_blanco([{"t": 0, "op": 0}, {"t": tg, "op": 0}, {"t": tg + 0.02, "op": 0.8}, {"t": tg + 0.3, "op": 0}]),
            nieve(50, 124)],
            cam(1.0, 1.08, (540, 1000), temblor=0), "corte",
            hud=[rotulo(tg, d - 0.03, "2 MESES", tam=140, color="#ffffff", capsula="#c0392be6", y=1320)],
            sfx=[(0.0, "subida", -18, {"dur": round(tg, 2)}), (tg, "impacto", -12)])

    # ============================================================== 3. EL RETO AL ESPECTADOR
    @plano(427, "puedes probarlo ahora mismo: tu turno")
    def _(d):
        return P(["#c9ced6", "#7d838c"], [
            fondo("bg_oficina_gris"),
            pie("adulto_pantalla", 540, 1440, 520, z=0.55, keys=K(d, (0, {"escala": 0.95}), (1, {"escala": 1.02}))),
            pie("pantalla_ordenador", -380, 1400, 330, z=0.5), pie("pantalla_ordenador", 1460, 1400, 330, z=0.5),
            brillo(700, 1200, 260, "#cfe6ff", 0.4, 0.5, pulso=[0.15, 0.8])],
            cam(1.0, 1.15, (540, 1150)), "corte",
            hud=[rotulo(0.15, d - 0.05, "TU TURNO", tam=120, color="#1a120d", capsula=AMBAR, y=760, rot=-4)],
            sfx=[(0.15, "ding", -20)])

    @plano(431, "cierra los ojos: el ojo se cierra")
    def _(d):
        return P(["#c9ced6", "#050507"], [
            fondo("bg_oficina_gris"), negro([{"t": 0, "op": 0.35}]),
            pieza("ojo", 540, 960, 1040, z=0.6, keys=K(d, (0, {"ey": 1.0}), (0.55, {"ey": 0.06, "ease": "entrada"}))),
            negro(K(d, (0, {"op": 0.0}), (0.55, {"op": 0.0}), (1, {"op": 1.0})))],
            cam(1.0, 1.15, (540, 960)), "corte", sfx=[(d * 0.45, "roce", -24)])

    @plano(434, "cuenta un minuto de cabeza: a oscuras")
    def _(d):
        pulsos = []
        for t in (0.0, 1.0):
            pulsos += [{"t": t, "op": 1.0}, {"t": t + 0.5, "op": 0.25}]
        return P(["#07090f", "#050507"], [
            fondo("bg_negro_cueva"),
            pieza("bea_cara_ojos_cerrados", 540, 1200, 900, z=0.55, op=0.7, keys=K(d, (0, {"escala": 1.0}), (1, {"escala": 1.06}))),
            brillo(540, 630, 260, "#ffffff", 0.35, 0.3, keys=pulsos),
            barra(540, 500, 600, 22, "#ffffff", 0.0, d, d / 60.0, fondo_c="#ffffff25", z=0.7),
            estrellas(20, 34)],
            cam(1.0, 1.06, (540, 900)), "corte",
            hud=[contador(0.02, d - 0.05, 1, 2, 1.0, " s", tam=110, x=540, y=630, color="#ffffff", capsula=None)],
            sfx=[(0.02, "tic", -24), (1.0, "tic", -24)])

    @plano(439, "abre los ojos cuando creas que ha terminado")
    def _(d):
        return P(["#c9ced6", "#7d838c"], [
            fondo("bg_oficina_gris"),
            *flip(["bea_cara_parpadea", "bea_cara_neutra"], d, fps=1 / 0.45, base=lambda n: pieza(n, 540, 1020, 940, z=0.6,
                  keys=K(d, (0, {"escala": 1.05}), (1, {"escala": 1.0})))),
            negro(K(d, (0, {"op": 0.9}), (0.25, {"op": 0.0, "ease": "salida"})))],
            cam(1.12, 1.0, (540, 900)), "corte",
            hud=[],
            sfx=[(0.1, "brillo", -24), (T(443) + 0.1, "pop", -22)])

    @plano(448, "mira cuánto te has desviado: dos barras")
    def _(d):
        return P(["#c9ced6", "#7d838c"], [
            fondo("bg_oficina_gris"), negro([{"t": 0, "op": 0.55}]),
            barra(540, 820, 800, 70, "#ffffff", 0.0, 0.7, 1.0, fondo_c="#ffffff30"),
            barra(540, 1020, 800, 70, MAGENTA, 0.15, 0.7, 0.72, fondo_c="#ffffff30"),
            flecha([[828, 1080], [972, 1080]], 0.8, 1.1, AMBAR, 8),
            senala(900, 1020, 0.8, d - 0.1, 100, AMBAR),
            pie("pantalla_ordenador", -380, 1400, 330, z=0.5), pie("pantalla_ordenador", 1460, 1400, 330, z=0.5)],
            cam(1.0, 1.05, (540, 920)), "corte",
            hud=[rotulo(0.1, d - 0.05, "1 MIN", tam=70, color="#1a120d", capsula="#ffffff", x=250, y=720),
                 rotulo(0.25, d - 0.05, "TÚ", tam=70, color="#ffffff", capsula="#9a1f8ae6", x=200, y=1130)],
            sfx=[(0.8, "golpe", -20)])

    @plano(453, "y eso que llevas toda la vida")
    def _(d):
        return P(["#1b2240", "#0b0f24"], [
            fondo("bg_ciudad"),
            pie("adulto_camina", 540, 1390, 600, z=0.55, keys=K(d, (0, {"x": 300}), (1, {"x": 640, "ease": "lineal"})) + late(0, 3, 0.02, d / 3)),
            pieza("telefono_movil", 600, 980, 90, z=0.6, keys=K(d, (0, {"x": 360}), (1, {"x": 700, "ease": "lineal"}))),
            pie("adulto_camina", -400, 1390, 520, z=0.5, keys=K(d, (0, {"x": -300}), (1, {"x": -480})), ex=-1),
            pie("adulto_camina", 1500, 1390, 500, z=0.5, keys=K(d, (0, {"x": 1450}), (1, {"x": 1600}))),
            {**polvo("#ffd59a", 30, (-500, 500, 1580, 1500), 53), "vel": [4, -10]}],
            cam(1.0, 1.1, (540, 1100)), "corte", sfx=[(0.1, "roce", -26)])

    @plano(460, "rodeado de relojes: pantallas por todas partes")
    def _(d):
        sitios = [(250, 640, 170, "telefono_movil", -12), (830, 660, 170, "telefono_movil", 10), (200, 1060, 300, "pantalla_ordenador", -6),
                  (880, 1080, 300, "pantalla_ordenador", 7), (540, 560, 150, "telefono_movil", 0), (540, 1300, 300, "pantalla_ordenador", 0),
                  (-300, 800, 180, "telefono_movil", -8), (1380, 820, 180, "telefono_movil", 8), (-380, 1200, 320, "pantalla_ordenador", 4),
                  (1460, 1200, 320, "pantalla_ordenador", -4)]
        els = [fondo("bg_ciudad"), negro([{"t": 0, "op": 0.35}])]
        for j, (x, y, an, n, r) in enumerate(sitios):
            els.append(pieza(n, x, y, an, z=0.55 + j * 0.005, rot=r, keys=aparece(0.04 + 0.08 * (j % 6), 0.35) + [{"t": d, "rot": r * 1.4}]))
        els.append(pieza("bea_cara_sorpresa", 540, 980, 560, z=0.6, keys=K(d, (0, {"escala": 0.9}), (1, {"escala": 1.0}))))
        return P(["#1b2240", "#0b0f24"], els, cam(1.0, 1.1, (540, 960)), "corte",
                 sfx=[(0.04 + 0.08 * j, "pop", -26) for j in range(0, 6, 2)])

    # ============================================================== 4. LOS DÍAS DE 48 HORAS
    @plano(463, "Siffre repitió el experimento durante años: pasan las estaciones")
    def _(d):
        est = ["hoja_otono", "copo_nieve", "flor_primavera", "sol_verano", "hoja_otono", "copo_nieve"]
        els = [fondo("bg_cueva_hielo")]
        for j, n in enumerate(est):
            t0 = j * d / len(est)
            els.append(pieza(n, 540, 680, 230, z=0.6, keys=[{"t": 0, "op": 0, "x": 1250}, {"t": t0, "op": 1, "x": 1250, "rot": 0},
                                                             {"t": t0 + d * 0.45, "x": -170, "rot": -160, "ease": "lineal"}, {"t": t0 + d * 0.46, "op": 0}],
                              _ancho=True))
        els += [pie("siffre_telefono", 480, 1400, 520, z=0.55), brillo(450, 1100, 200, "#fff1c8", 0.4, 0.5, pulso=[0.12, 0.8]),
                pie("telefono_campo", -380, 1400, 240, z=0.5), *suelo_lados(1400, 163), *hielo(d, sem=163)]
        return P(["#22405e", "#0d1b2e"], els, cam(1.0, 1.1, (540, 1050)), "corte",
                 sfx=[(j * d / len(est) + 0.2, "roce", -28) for j in range(0, 6, 2)])

    @plano(469, "con él mismo y con voluntarios: bajan por la galería")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_galeria"),
            pie("siffre_camina", 540, 1360, 380, z=0.55, keys=K(d, (0, {"escala": 0.7, "y": 1250 - 0.47 * 380 * 0.7}),
                                                                (1, {"escala": 1.0, "y": 1360 - 0.47 * 380, "ease": "suave"}))),
            pie("voluntario_1", 360, 1360, 400, z=0.53, keys=[{"t": 0, "op": 0}, {"t": T(473), "op": 0}] + aparece(T(473), 0.35)),
            pie("voluntario_5", 760, 1360, 400, z=0.53, keys=[{"t": 0, "op": 0}, {"t": T(474), "op": 0}] + aparece(T(474), 0.35)),
            brillo(560, 1100, 300, "#fff1c8", 0.4, 0.4, pulso=[0.12, 0.5]),
            *ambiente_cueva(d, sem=169)],
            cam(1.0, 1.1, (540, 1150)), "corte", sfx=[(T(473), "pop", -24), (T(474), "pop", -24)])

    @plano(475, "y vio algo increíble")
    def _(d):
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_cerebro"),
            pieza("cerebro", 540, 960, 620, z=0.55),
            pieza("cerebro_brillo", 540, 960, 620, z=0.56, keys=K(d, (0, {"op": 0.0}), (0.45, {"op": 1.0, "ease": "salida"}))),
            pieza("destello", 540, 940, 700, z=0.6, keys=[{"t": 0, "op": 0}, {"t": T(478), "op": 0}] + aparece(T(478), 0.35) + [{"t": d, "rot": 30}]),
            brillo(-380, 800, 260, MAGENTA, 0.3, 0.08, pulso=[0.2, 1.0]), brillo(1460, 1100, 260, CIAN, 0.3, 0.08, pulso=[0.2, 1.2])],
            cam(1.0, 1.15, (540, 960)), "zoom", sfx=[(T(478), "brillo", -18)])

    @plano(479, "sin sol, acababan viviendo")
    def _(d):
        parpadeo = [{"t": round(t, 3), "op": o} for t, o in [(0, 1), (0.4, 0.4), (0.47, 1), (1.1, 0.5), (1.16, 1)] if t < d]
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            pie("voluntario_3", 370, 1300, 500, z=0.5), pie("voluntario_6", 710, 1300, 500, z=0.5, keys=K(d, (0, {"x": 760}), (1, {"x": 700}))),
            pie("lampara_led", 540, 1300, 120, z=0.52),
            brillo(540, 1220, 280, "#ffcf8a", 0.6, 0.51, keys=parpadeo),
            pie("voluntario_4", 1450, 1300, 400, z=0.45),
            *ambiente_cueva(d, sem=179, oscura=True)],
            cam(1.2, 1.05, (540, 1150)), "corte", sfx=[(0.4, "zap", -28)])

    # barra de un «día»: 24 h (fantasma) y 48 h (36 despierto + 12 dormido)
    X0, AN = 140, 800          # la barra de 48 h va de x=140 a x=940

    @plano(483, "días de 48 horas")
    def _(d):
        return P(["#07090f", "#050507"], [
            fondo("bg_negro_cueva"),
            {"tipo": "barra", "x": X0 + AN / 4, "y": 800, "ancho": AN / 2, "alto": 60, "color": "#ffffff55", "fondo": "#ffffff20", "z": 0.6},
            barra(X0 + AN / 2, 980, AN, 90, AMBAR, 0.1, d * 0.8, 1.0, fondo_c="#ffffff18"),
            pieza("sol_dibujo", -350, 900, 260, z=0.5, op=0.5), pieza("luna_creciente", 1430, 900, 240, z=0.5, op=0.5),
            *ambiente_cueva(d, sem=183, oscura=True, gotas=False)],
            cam(1.0, 1.06, (540, 900)), "corte",
            hud=[rotulo(0.05, d - 0.05, "24 h", tam=64, color="#ffffff", capsula="#ffffff30", x=X0 + 110, y=700),
                 contador(0.1, d - 0.05, 0, 48, d * 0.8, " h", tam=130, x=540, y=1160, color="#1a120d", capsula=AMBAR)],
            sfx=[(0.1, "subida", -26, {"dur": d * 0.7})])

    @plano(489, "treinta y seis horas despiertos")
    def _(d):
        return P(["#07090f", "#050507"], [
            fondo("bg_negro_cueva"),
            {"tipo": "barra", "x": X0 + AN / 2, "y": 980, "ancho": AN, "alto": 90, "color": "#ffffff00", "fondo": "#ffffff18", "z": 0.59},
            barra(X0 + AN * 0.375, 980, AN * 0.75, 90, "#ffb15e", 0.05, d * 0.7, 1.0, fondo_c="#ffffff00"),
            pieza("sol_dibujo", X0 + AN * 0.375, 760, 220, z=0.6, keys=aparece(0.1) + [{"t": d, "rot": 30}]),
            pieza("sol_dibujo", -350, 900, 260, z=0.5), *ambiente_cueva(d, sem=189, oscura=True, gotas=False)],
            cam(1.04, 1.1, (500, 950)), "corte",
            hud=[contador(0.05, d - 0.05, 0, 36, d * 0.7, " h", tam=120, x=560, y=1160, color="#1a120d", capsula="#ffb15e")],
            sfx=[(0.1, "brillo", -24)])

    @plano(494, "y doce dormidos")
    def _(d):
        return P(["#07090f", "#050507"], [
            fondo("bg_negro_cueva"),
            barra(X0 + AN * 0.375, 980, AN * 0.75, 90, "#ffb15e", 0, 0.01, 1.0, fondo_c="#ffffff00", p0=1.0),
            barra(X0 + AN * 0.875, 980, AN * 0.25, 90, "#5f9fd1", 0.05, d * 0.6, 1.0, fondo_c="#ffffff18"),
            pieza("luna_creciente", X0 + AN * 0.875, 760, 180, z=0.6, keys=aparece(0.1) + [{"t": d, "rot": -15}]),
            pieza("luna_creciente", 1430, 900, 240, z=0.5), *ambiente_cueva(d, sem=194, oscura=True, gotas=False)],
            cam(1.1, 1.04, (640, 950)), "corte",
            hud=[contador(0.05, d - 0.05, 0, 12, d * 0.6, " h", tam=120, x=560, y=1160, color="#ffffff", capsula="#22405ee6")],
            sfx=[(0.1, "brillo", -26)])

    @plano(497, "y sin notar ninguna diferencia")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            pie("voluntario_2", 400, 1300, 460, z=0.5, keys=K(d, (0, {"x": 380}), (1, {"x": 420}))),
            pie("voluntario_5", 700, 1300, 460, z=0.5, keys=late(0.4, 2, 0.03, 0.5)),
            pie("lampara_led", 550, 1300, 110, z=0.52), brillo(550, 1230, 260, "#ffcf8a", 0.55, 0.51, pulso=[0.08, 1.4]),
            pie("voluntario_1", -380, 1300, 420, z=0.45), pie("voluntario_6", 1460, 1300, 420, z=0.45),
            *ambiente_cueva(d, sem=197, oscura=True)],
            cam(1.0, 1.12, (540, 1100)), "corte",
            hud=[rotulo(0.3, d - 0.05, "48 h = 1 DÍA", tam=90, color="#ffffff", capsula="#0b0f1ed8", y=620)],
            sfx=[(0.3, "ding", -24)])

    # ============================================================== 5. DEEP TIME, 2021
    @plano(502, "y no es cosa del pasado: 1962 se va")
    def _(d):
        return P(["#a9d6f5", "#e8f6ff"], [
            fondo("bg_alpes_nieve"),
            pie("tienda_1962", 380, 1330, 260, z=0.5, keys=K(d, (0, {"x": 380}), (0.4, {"x": 380}), (1, {"x": -700, "ease": "entrada"}))),
            pie("equipo_1962", 720, 1345, 400, z=0.55, keys=K(d, (0, {"x": 720}), (0.4, {"x": 720}), (1, {"x": -300, "ease": "entrada"}))),
            negro(K(d, (0, {"op": 0.0}), (0.5, {"op": 0.0}), (1, {"op": 0.5})), color="#3d2a1f"),
            nieve(60, 202)],
            cam(1.05, 1.15, (540, 1050)), "corte",
            hud=[rotulo(0.05, d * 0.7, "1962", tam=130, color="#ffffff", capsula="#0d1b2ed8", y=640)],
            sfx=[(d * 0.45, "whoosh", -26)])

    def francia(d, sem, extra=()):
        return [*techo(sem), {**polvo("#ffd9a0", 34, (-500, 500, 1580, 1500), sem)}, *murcielagos(d),
                brillo(-300, 1100, 300, "#ffcf8a", 0.4, 0.07, pulso=[0.1, 1.5]), brillo(1400, 1100, 300, "#ffcf8a", 0.4, 0.07, pulso=[0.1, 1.2]), *extra]

    @plano(508, "en 2021")
    def _(d):
        return P(["#3d2a1f", "#0b0705"], [
            fondo("bg_cueva_francia"),
            brillo(540, 1000, 520, "#ffcf8a", 0.4, 0.1, keys=K(d, (0, {"op": 0.3}), (1, {"op": 1.0}))),
            pie("lampara_led", 540, 1330, 140, z=0.55, keys=aparece(0.05)),
            *[pie(f"voluntario_{j + 1}", x0, 1190, 210, z=0.45, keys=K(d, (0, {"x": x0 + dx}), (1, {"x": x0, "ease": "suave"})))
              for j, (x0, dx) in enumerate([(300, -160), (420, -120), (690, 140), (800, 170), (-380, -120), (1460, 140)])],
            *francia(d, 208)],
            cam(1.15, 1.0, (540, 1000)), "barrido",
            hud=[contador(0.05, d - 0.05, 1962, 2021, d * 0.6, "", tam=150, x=540, y=800, color="#ffffff", capsula="#c0392be6", miles=False)],
            sfx=[(0.05, "tictac", -28, {"dur": d * 0.55, "ritmo": 0.06})])

    # grupo de 15 por profundidad: (nombre, x, suelo, alto)
    r = random.Random(15)
    GRUPO = []
    filas = [(1180, 230, [210, 330, 450, 630, 750, 870]), (1260, 300, [150, 300, 780, 930]), (1360, 400, [250, 540, 830]),
             (1230, 270, [-420, -200, 1300, 1520])]
    k = 0
    for suelo, alto, xs in filas:
        for x in xs:
            GRUPO.append((f"voluntario_{k % 6 + 1}", x + r.uniform(-15, 15), suelo, alto * r.uniform(0.94, 1.06), k))
            k += 1

    def grupo(d, t_base=None, paso=0.06, solo=None, op_resto=1.0):
        out = []
        for n, x, s, a, j in GRUPO:
            if solo is not None and j >= 15:
                continue
            z = 0.45 + (s - 1100) / 2000
            ks = [] if t_base is None else ([{"t": 0, "op": 0}, {"t": t_base + paso * (j % 15), "op": 0}] + aparece(t_base + paso * (j % 15), 0.3))
            op = op_resto if (solo is not None and n != solo) else 1.0
            out.append(pie(n, x, s, a, z=z, keys=ks, op=op, ex=(-1 if j % 3 == 1 else 1)))
        return out

    @plano(512, "quince personas se encerraron")
    def _(d):
        return P(["#3d2a1f", "#0b0705"], [
            fondo("bg_cueva_francia"), *grupo(d, 0.05, 0.06),
            brillo(540, 1150, 500, "#ffcf8a", 0.35, 0.1), *francia(d, 212)],
            cam(1.0, 1.08, (540, 1100)), "corte",
            hud=[contador(0.05, d - 0.05, 0, 15, 0.9, "", tam=140, x=540, y=620, color="#ffffff", capsula="#0b0f1ed8")],
            sfx=[(0.05 + 0.18 * j, "pop", -27) for j in range(5)])

    @plano(516, "cuarenta días en una cueva de Francia")
    def _(d):
        return P(["#3d2a1f", "#0b0705"], [
            fondo("bg_cueva_francia"), *grupo(d),
            pie("tienda_campana", 540, 1150, 150, z=0.4), pie("lampara_led", 400, 1260, 80, z=0.5), pie("lampara_led", 700, 1180, 70, z=0.44),
            brillo(400, 1220, 160, "#ffcf8a", 0.5, 0.42, pulso=[0.1, 0.9]),
            *francia(d, 216)],
            cam(1.3, 1.0, (540, 1200), (540, 1100)), "corte",
            hud=[contador(0.05, d - 0.05, 0, 40, d * 0.55, " días", tam=120, x=540, y=600, color="#ffffff", capsula="#0b0f1ed8")],
            sfx=[(0.05, "tictac", -28, {"dur": d * 0.5, "ritmo": 0.05})])

    @plano(523, "al salir, la mayoría creía…: salen a la luz del día")
    def _(d):
        gente = []
        for j, (n, x) in enumerate([("voluntario_2", 300), ("voluntario_4", 560), ("voluntario_1", 800), ("voluntario_6", -350), ("voluntario_3", 1450)]):
            gente.append(pie(n, x, 1420, 470, z=0.55, keys=K(d, (0, {"escala": 0.75, "y": 1330 - 0.47 * 470 * 0.75}),
                                                                (1, {"escala": 1.0, "y": 1420 - 0.47 * 470, "ease": "suave"}))))
        return P(["#6fb6e8", "#c9a26b"], [
            fondo("bg_entrada_dia"), *gente,
            fundido_blanco(K(d, (0, {"op": 1.0}), (0.35, {"op": 0.0, "ease": "salida"}))),
            {**polvo("#fff6e0", 30, (-500, 500, 1580, 1500), 23), "vel": [6, -10]}],
            cam(1.0, 1.08, (540, 1150)), "corte", sfx=[(0.02, "brillo", -20)])

    @plano(529, "unos treinta: el taco del calendario")
    def _(d):
        hojas = [pieza("calendario_hoja", 540, 900, 380, z=0.62 - 0.001 * j, keys=[{"t": 0, "op": 0}, {"t": 0.05 + 0.12 * j, "op": 1, "x": 540, "y": 920, "rot": 0},
                                                                                   {"t": 0.05 + 0.12 * j + 0.5, "x": 540 + (j % 2 * 2 - 1) * 700, "y": 420, "rot": 70 * (j % 2 * 2 - 1),
                                                                                    "op": 0, "ease": "entrada"}])
                 for j in range(6)]
        return P(["#6fb6e8", "#c9a26b"], [
            fondo("bg_entrada_dia"), negro([{"t": 0, "op": 0.25}]),
            pie("calendario_taco", 540, 1250, 640, z=0.6, keys=late(0.0, 3, 0.03, 0.4)), *hojas,
            pie("voluntario_5", -380, 1380, 420, z=0.5), pie("voluntario_2", 1460, 1380, 420, z=0.5, ex=-1)],
            cam(1.0, 1.1, (540, 1000)), "corte",
            hud=[contador(0.05, d - 0.05, 0, 30, d * 0.7, "", tam=170, x=540, y=960, color="#1a120d", capsula=None)],
            sfx=[(0.05 + 0.24 * j, "roce", -27) for j in range(3)])

    @plano(533, "una de las mujeres: foco en ella")
    def _(d):
        return P(["#3d2a1f", "#0b0705"], [
            fondo("bg_cueva_francia"), *grupo(d, solo="voluntario_2", op_resto=0.3),
            negro([{"t": 0, "op": 0.0}, {"t": 0.4, "op": 0.45}]),
            pie("voluntario_2", 540, 1400, 640, z=0.75, keys=arranque(540, 1400 - 0.47 * 640, d, "abajo", 120, 10)),
            brillo(540, 1080, 340, "#ffe2a8", 0.55, 0.74, keys=aparece(0.1, 0.5)),
            *francia(d, 233)],
            cam(1.0, 1.12, (540, 1080)), "corte", sfx=[(0.1, "ding", -24), (T(542), "roce", -26)])

    @plano(543, "23 veces en 40 días: 40 casillas, 23 lunas")
    def _(d):
        els = [fondo("bg_negro_cueva"), brillo(540, 900, 600, "#5f9fd1", 0.25, 0.1)]
        orden = list(range(40))
        random.Random(23).shuffle(orden)
        lunas = set(orden[:23])
        k = 0
        for j in range(40):
            x, y = 190 + (j % 8) * 100, 640 + (j // 8) * 110
            els.append({"tipo": "forma", "forma": "redondeado", "ancho": 84, "alto": 92, "relleno": "#22405e", "op": 0.7, "x": x, "y": y, "z": 0.5,
                        "esquinas": 14, "keys": aparece(0.02 * j, 0.25)})
            if j in lunas:
                t = 0.35 + 0.075 * k
                k += 1
                els.append(pieza("luna_creciente", x, y, 72, z=0.55, keys=[{"t": 0, "op": 0}, {"t": t, "op": 0}] + aparece(t, 0.25)))
        els += [estrellas(30, 43), pieza("luna_creciente", -380, 900, 240, z=0.4, op=0.4), pieza("luna_creciente", 1460, 900, 240, z=0.4, op=0.4)]
        return P(["#07090f", "#050507"], els, cam(1.0, 1.08, (540, 860)), "corte",
                 hud=[contador(0.35, d - 0.05, 0, 23, 0.075 * 23, "", tam=130, x=540, y=1260, color="#ffffff", capsula="#22405ee6")],
                 sfx=[(0.35 + 0.3 * j, "tic", -28) for j in range(6)])

    @plano(549, "y dos de cada tres")
    def _(d):
        tr = [("voluntario_1", 270), ("voluntario_4", 540), ("voluntario_6", 810)]
        els = [fondo("bg_cueva_francia"), negro([{"t": 0, "op": 0.5}])]
        for j, (n, x) in enumerate(tr):
            luz = j < 2
            t = T(550) + 0.25 * j if j < 2 else d
            els.append(pie(n, x, 1360, 560, z=0.55, keys=[{"t": 0, "op": 0.35}, {"t": t, "op": 0.35}, {"t": t + 0.15, "op": 1.0 if luz else 0.35}] +
                           (late(t, 1, 0.06) if luz else [])))
            if luz:
                els.append(brillo(x, 1100, 230, "#ffe2a8", 0.6, 0.5, keys=[{"t": 0, "op": 0}, {"t": t, "op": 0}, {"t": t + 0.15, "op": 1}]))
        els += [pie("voluntario_3", -380, 1330, 480, z=0.5, op=0.35), pie("voluntario_5", 1460, 1330, 480, z=0.5, op=0.35), *francia(d, 249)]
        return P(["#3d2a1f", "#0b0705"], els, cam(1.0, 1.08, (540, 1100)), "corte",
                 hud=[rotulo(T(550), d - 0.05, "2 DE 3", tam=110, color="#1a120d", capsula=AMBAR, y=640)],
                 sfx=[(T(550), "ding", -24), (T(550) + 0.25, "ding", -23)])

    @plano(554, "les habría gustado quedarse un poco más")
    def _(d):
        return P(["#3d2a1f", "#0b0705"], [
            fondo("bg_cueva_francia"), *grupo(d),
            pie("voluntario_5", 560, 1420, 620, z=0.75, keys=late(0.3, 3, 0.03, 0.6)),
            pie("tienda_campana", 840, 1300, 220, z=0.6), pie("lampara_led", 300, 1420, 120, z=0.76),
            brillo(320, 1350, 220, "#ffcf8a", 0.55, 0.74, pulso=[0.1, 1.1]),
            *francia(d, 254)],
            cam(1.15, 1.0, (560, 1150), (540, 1100)), "corte", sfx=[(0.3, "roce", -27)])

    # ============================================================== 6. VUELTA A GRANADA: TE ESTÁS ENGAÑANDO
    @plano(563, "así que ahí abajo: vuelta a Beatriz")
    def _(d):
        rayas = [IMG("marca_raya", ancho=34, x=300 + 40 * i + (12 if i % 5 == 4 else 0), y=760, z=0.4) for i in range(9)]
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"), *rayas,
            pie("bea_marca_a", 650, 1300, 600, z=0.55),
            pie("lampara_led", 880, 1300, 120, z=0.56), brillo(880, 1220, 240, "#ffcf8a", 0.55, 0.55, pulso=[0.08, 1.5]),
            *suelo_lados(1300, 263), *ambiente_cueva(d, sem=263)],
            cam(1.35, 1.0, (540, 700), (540, 1050)), "corte", sfx=[(0.05, "rumor", -26, {"dur": 1.2})])

    @plano(567, "cada vez que apuntas un día más: la raya nueva")
    def _(d):
        viejas = [IMG("marca_grupo", ancho=220, x=x, y=y, z=0.4, op=0.9) for x, y in [(180, 650), (440, 640), (180, 960), (440, 950)]]
        viejas += [IMG("marca_grupo", ancho=200, x=x, y=y, z=0.4, op=0.8) for x, y in [(-420, 700), (-180, 900), (1260, 720), (1500, 900)]]
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"), brillo(600, 820, 460, "#ffcf8a", 0.35, 0.3), *viejas,
            tiza(700, 820, T(572), 300, z=0.5),
            *flip(["bea_marca_a", "bea_marca_b"], d, fps=3, base=lambda n: pie(n, 880, 1400, 820, z=0.6)),
            IMG("moho_pared", ancho=380, x=880, y=520, z=0.32, op=0.5)],
            cam(1.0, 1.1, (560, 860)), "corte", sfx=[(T(572), "trazo", -20), (T(572) + 0.12, "trazo", -22)])

    @plano(574, "te estás engañando: la raya se tuerce")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"), negro([{"t": 0, "op": 0.3}]),
            brillo(540, 900, 420, "#ffcf8a", 0.35, 0.3, pulso=[0.12, 0.7]),
            IMG("marca_grupo", ancho=260, x=230, y=700, z=0.4, op=0.85),
            IMG("marca_raya", ancho=80, x=480, y=700, z=0.5, keys=K(d, (0, {"rot": 0, "op": 1}), (0.25, {"rot": 0}),
                                                                       (0.7, {"rot": 28, "x": 520, "ease": "anticipa"}), (1, {"rot": 34, "op": 0.5}))),
            pieza("bea_cara_miedo", 700, 1160, 760, z=0.6, keys=K(d, (0, {"escala": 1.0, "x": 730}), (1, {"escala": 1.05, "x": 700}))),
            IMG("marca_grupo", ancho=260, x=-380, y=880, z=0.4, op=0.7), IMG("marca_grupo", ancho=260, x=1460, y=880, z=0.4, op=0.7)],
            cam(1.0, 1.1, (560, 950)), "corte", sfx=[(d * 0.4, "zap", -24)])

    @plano(577, "tus días ya no son días: las rayas se deshacen (remate)")
    def _(d):
        r2 = random.Random(577)
        els = [fondo("bg_cueva_campamento")]
        tq = T(579)
        for i in range(12):
            x = 200 + (i % 4) * 230 + r2.uniform(-20, 20)
            y = 640 + (i // 4) * 230
            t = tq + 0.08 * i
            rot = r2.uniform(-35, 35)
            els.append(IMG("marca_grupo", ancho=190, x=x, y=y, z=0.4, keys=[{"t": 0, "op": 0.95, "rot": 0}, {"t": t, "rot": 0, "y": y},
                                                                             {"t": t + 0.5, "rot": rot, "y": y + 60, "op": 0.15, "ease": "entrada"}]))
        for x in (-420, -180, 1260, 1500):
            els.append(IMG("marca_grupo", ancho=190, x=x, y=880, z=0.4, keys=[{"t": 0, "op": 0.8}, {"t": tq, "op": 0.8}, {"t": tq + 0.6, "op": 0.1}]))
        els += [brillo(540, 900, 520, "#ffcf8a", 0.4, 0.3, keys=K(d, (0, {"op": 1}), (1, {"op": 0.4}))),
                pie("bea_marca_b", 900, 1300, 520, z=0.6, op=0.9),
                negro([{"t": 0, "op": 0}, {"t": d - 0.35, "op": 0}, {"t": d, "op": 0.9}]),
                *ambiente_cueva(d, sem=277, gotas=True, murc=False)]
        return P(["#3d2a1f", "#1a120d"], els, cam(1.12, 1.0, (540, 900)), "corte",
                 sfx=[(tq, "golpe", -18), (tq + 0.3, "roce", -24)])
