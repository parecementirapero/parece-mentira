"""Parte 5 (palabras 1035–1341): «Y entonces llega el día quinientos.» … «¿cuánto crees que aguantarías tú ahí abajo?»"""
import math
import random

from comun import *  # noqa: F401,F403
import comun
from motor import denso as D

CALIDO, FRIO = "#ffcf8a", "#dfefff"


# ------------------------------------------------------------------ ayudantes propios de la parte 5
def lados_cueva(suelo, sem=1, z=0.55):
    """Estalagmitas y rocas en los laterales (solo se ven en el horizontal)."""
    r = random.Random(sem * 31)
    out = []
    for x in (-520, -300, 1380, 1600):
        n = r.choice(["estalagmita_a", "estalagmita_b"])
        out.append(pie(n, x + r.uniform(-40, 40), suelo + r.uniform(0, 30), r.uniform(220, 380), z=z + r.uniform(-0.05, 0.05)))
    return out


def haz(sx, sy, largo, r0, r1, d, z=0.62, op=0.85, pasos=6, t0=0.0, op0=None):
    """Haz de frontal que sale de (sx, sy) y barre del ángulo r0 al r1 (grados; 0 = la luz va hacia la izquierda),
    con el foco quieto (el centro de la pieza se recalcula en cada clave)."""
    ks = []
    for j in range(pasos + 1):
        u = j / pasos
        r = r0 + (r1 - r0) * (u * u * (3 - 2 * u))
        a = math.radians(r)
        ks.append({"t": round(t0 + (d - t0) * u, 3), "x": round(sx - largo / 2 * math.cos(a), 1), "y": round(sy - largo / 2 * math.sin(a), 1),
                   "rot": round(r, 2), "ease": "lineal"})
    if op0 is not None:
        ks[0]["op"] = op0
        ks.append({"t": round(t0 + 0.35, 3), "op": op})
        ks.sort(key=lambda q: q["t"])
    return IMG("haz_frontal", ancho=round(largo), x=ks[0]["x"], y=ks[0]["y"], z=z, op=op, keys=ks)


def barra(x, base, ancho, alto, color, t0, t1, z=0.6):
    """Barra que crece desde el suelo (base fija) entre t0 y t1."""
    return {"tipo": "forma", "forma": "rect", "ancho": ancho, "alto": alto, "relleno": color, "x": x, "y": base - alto / 2, "z": z,
            "keys": [{"t": 0, "ey": 0.001, "y": base, "op": 0}, {"t": t0, "ey": 0.001, "y": base, "op": 1},
                     {"t": t1, "ey": 1.0, "y": base - alto / 2, "ease": "salida"}]}


def rayos(x, y, color="#fff4cf", n=14, largo=1100, apertura=5, z=0.08, giro=4, keys=None, op=1.0):
    e = {"tipo": "rayos", "n": n, "longitud": largo, "apertura": apertura, "color": color, "x": x, "y": y, "z": z, "op": op,
         "anim": {"girar": giro}}
    if keys:
        e["keys"] = keys
    return e


def copos(n, d, sem=5, z=0.75, area=(-500, 380, 1580, 1500), ancho=(40, 90)):
    """Copos de nieve (pieza) que bajan girando, también en los laterales."""
    r = random.Random(sem)
    out = []
    for _ in range(n):
        x = r.uniform(area[0], area[2]); y = r.uniform(area[1], area[3])
        out.append(pieza("copo_nieve", x, y, r.uniform(*ancho), z=z + r.uniform(-0.1, 0.1),
                         keys=[{"t": 0, "y": y - 60, "rot": 0, "op": 0.85}, {"t": d, "y": y + 90 + r.uniform(0, 60), "rot": r.uniform(-90, 90), "ease": "lineal"}]))
    return out


def planos(v, plano):
    w = v.w

    def en(i):
        """Segundo, dentro del plano que se está construyendo, en que empieza la palabra i."""
        return round(max(0.0, v.PAL[i]["inicio"] - D._V.ini), 3)

    # cruces de murciélagos de esta parte (tiempo absoluto)
    comun.VUELOS += [(w(1035), w(1035) + 4.5, (1350, 520), (-350, 640), 150), (w(1043), w(1043) + 6, (-300, 600), (1350, 480), 120),
                     (w(1217) - 0.4, w(1217) + 3.5, (1300, 700), (-300, 520), 140),
                     (w(1335) + 0.3, w(1335) + 4.5, (-300, 560), (1350, 470), 110)]

    # ================================================================== DÍA 500
    @plano(1035, "y entonces llega el día quinientos: la cámara se lanza por la galería y cae el 500")
    def _(d):
        # Arranque de la parte 5 de TikTok (gancho «DÍA 500: LA SALIDA» en y≈640 durante 2,6 s: este plano dura eso justo).
        # La cámara entra disparada por la galería hacia una luz lejana; en «quinientos», fogonazo y el 500 cae de golpe.
        tq = en(1039) - 0.03
        rayas = [tiza(-600 + 46 * i + (18 if i % 5 == 4 else 0), 760, tq + 0.05 + 0.03 * i, 160) for i in range(10)]
        rayas += [tiza(1150 + 46 * i + (18 if i % 5 == 4 else 0), 740, tq + 0.05 + 0.03 * i, 160) for i in range(10)]
        tras = lambda e: {**e, "keys": sorted(e.get("keys", []) + [{"t": 0, "op": 0}, {"t": tq, "op": 0}, {"t": tq + 0.02, "op": 1}], key=lambda q: q["t"])}
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_galeria"),
            brillo(540, 1150, 260, CALIDO, 0.6, 0.2, pulso=[0.12, 0.5]),
            {**polvo("#ffe2b0", 60, (-500, 420, 1580, 1600), 7), "vel": [10, -160]},
            pie("rocas_primer_plano_a", 540, 2080, 620, z=0.95, keys=[{"t": 0, "y": 1700, "escala": 1.0}, {"t": tq, "y": 2150, "escala": 1.35, "ease": "entrada"}]),
            IMG("estalactita_c", ancho=210, x=170, y=430, z=0.9, keys=[{"t": 0, "x": 230, "y": 470}, {"t": tq, "x": -60, "y": 330, "ease": "entrada"}]),
            IMG("estalactita_a", ancho=170, x=930, y=420, z=0.9, keys=[{"t": 0, "x": 860, "y": 450}, {"t": tq, "x": 1160, "y": 320, "ease": "entrada"}]),
            *lados_cueva(1360, 1), *ambiente_cueva(d, sem=11, gotas=False),
            # --- el golpe del 500: otro escenario encima (lo tapa el fogonazo)
            {**fondo("bg_cueva_campamento_oscura", z=0.93), "keys": [{"t": 0, "op": 0}, {"t": tq, "op": 0}, {"t": tq + 0.02, "op": 1}]},
            tras(rayos(540, 960, "#ffd98a", n=16, largo=1300, apertura=4, z=0.94, giro=6,
                       keys=[{"t": tq, "escala": 0.4}, {"t": tq + 0.12, "escala": 1.0, "ease": "golpe"}], op=0.9)),
            tras(brillo(540, 960, 620, "#ffb15e", 0.6, 0.94, pulso=[0.1, 0.8])),
            tras(pie("cifra_marco", 540, 1120, 340, z=0.96, keys=[{"t": tq, "escala": 1.6}, {"t": tq + 0.3, "escala": 1.0, "ease": "golpe"},
                                                                  {"t": d, "escala": 1.05, "ease": "suave"}])),
            *[tras({**r_, "z": 0.95}) for r_ in rayas],
            fundido_blanco([{"t": 0, "op": 0}, {"t": tq - 0.01, "op": 0}, {"t": tq, "op": 0.9}, {"t": tq + 0.3, "op": 0.0}])],
            cam(1.0, 1.3, (540, 960), (540, 960)), "corte", vineta=0.75,
            hud=[contador(tq + 0.02, d - 0.02, 1, 500, 0.5, " días", tam=160, x=540, y=975, color="#ffd23f", capsula=None, miles=False)],
            sfx=[(0.02, "whoosh", -20), (max(0.05, tq - 1.0), "subida", -18, {"dur": 1.0}), (0.3, "roce", -26), (tq, "impacto", -14),
                 (tq + 0.35, "rumor", -26, {"dur": 0.8})], energia=0.9)

    @plano(1040, "oyes pasos: huellas que se acercan", mas=0.74)
    def _(d):
        t0 = en(1041)
        pasos = []
        for j in range(5):
            t = t0 + 0.06 + 0.24 * j
            x = 300 + (80 if j % 2 else -40) + 25 * j
            y = 880 + 110 * j
            pasos.append(pieza("huellas", x, y, 150 + 55 * j, z=0.4 + 0.02 * j, keys=[{"t": 0, "op": 0}, {"t": t, "op": 0, "escala": 1.25},
                                                                                     {"t": t + 0.08, "op": 1, "escala": 1.0, "ease": "golpe"}]))
        return P(["#141018", "#050507"], [
            fondo("bg_negro_cueva"),
            brillo(560, 760, 380, "#dfefff", 0.25, 0.1, keys=K(d, (0, {"op": 0.2}), (1, {"op": 1.0}))),
            *pasos,
            pie("bea_oye", 790, 1344, 640, z=0.55, keys=K(d, (0, {"x": 820, "rot": 2}), (1, {"x": 770, "rot": -2}))),
            brillo(790, 980, 300, CALIDO, 0.3, 0.54, pulso=[0.1, 1.2]),
            *lados_cueva(1344, 2), *ambiente_cueva(d, sem=13, oscura=True)],
            cam(1.18, 1.0, (540, 1150), (540, 1050)), "corte",
            sfx=[(t0 + 0.06 + 0.24 * j, "golpe", -27 - (2 if j % 2 else 0)) for j in range(5)])

    @plano(1043, "ves luces que no son la tuya")
    def _(d):
        t_tuya = en(1046)
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_galeria"),
            brillo(560, 1020, 200, FRIO, 0.3, 0.2, keys=K(d, (0, {"op": 0.2, "escala": 0.6}), (1, {"op": 1, "escala": 1.6}))),
            haz(560, 1010, 820, -60, -48, d, z=0.3, op=0.75, op0=0.0),
            haz(590, 1015, 760, -125, -140, d, z=0.3, op=0.7, op0=0.0, t0=0.25),
            pie("lampara_led", 240, 1420, 300, z=0.75, keys=K(d, (0, {"x": 250}), (1, {"x": 220}))),
            brillo(240, 1300, 260, CALIDO, 0.6, 0.76, keys=[{"t": 0, "op": 1}, {"t": t_tuya, "op": 1}, {"t": t_tuya + 0.08, "op": 0.35},
                                                             {"t": t_tuya + 0.16, "op": 1}, {"t": t_tuya + 0.26, "op": 0.5}, {"t": d, "op": 0.8}]),
            senala(240, 1290, t_tuya, d - 0.1, 130, AMBAR),
            *lados_cueva(1360, 3), *ambiente_cueva(d, sem=14)],
            cam(1.05, 1.2, (500, 1150), (420, 1200)), "corte",
            sfx=[(0.1, "rumor", -26, {"dur": 1.5}), (t_tuya + 0.05, "zap", -26)])

    @plano(1050, "es tu equipo: llegan con los frontales")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_galeria"),
            *flip(["equipo_frontal_a", "equipo_frontal_b"], d, fps=4, base=lambda n: pie(n, 470, 1360, 560, z=0.55,
                  keys=K(d, (0, {"x": 330, "escala": 0.8, "y": 1330}), (1, {"x": 520, "escala": 1.12, "y": 1380, "ease": "lineal"})))),
            brillo(760, 1000, 320, FRIO, 0.5, 0.5, pulso=[0.15, 0.4]),
            pie("voluntario_2", -330, 1360, 470, z=0.5), pie("voluntario_5", 1420, 1360, 450, z=0.5, ex=-1),
            *lados_cueva(1360, 4), *ambiente_cueva(d, sem=15)],
            cam(1.0, 1.1, (500, 1150), (560, 1150)), "corte",
            sfx=[(0.05, "golpe", -26), (0.35, "golpe", -28), (0.65, "golpe", -26), (0.95, "golpe", -28)])

    @plano(1053, "tu primera reacción: gira la cabeza en la oscuridad")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            pieza("bea_cara_miedo", 560, 1000, 980, z=0.6, keys=K(d, (0, {"x": 640, "rot": 4, "escala": 0.98}), (0.55, {"x": 540, "rot": -3, "ease": "suave"}),
                                                                 (1, {"x": 520, "rot": -2, "escala": 1.03, "ease": "suave"}))),
            brillo(1000, 760, 520, FRIO, 0.55, 0.65, keys=K(d, (0, {"op": 0.1}), (1, {"op": 1.0, "ease": "entrada"}))),
            IMG("estalactita_b", ancho=150, x=-260, y=470, z=0.8), IMG("estalactita_c", ancho=200, x=1350, y=450, z=0.8),
            pie("lampara_led", -330, 1300, 240, z=0.5), pie("mochila", 1430, 1300, 330, z=0.5),
            {**polvo("#9fc4ff", 30, (-400, 420, 1500, 1500), 16)}],
            cam(1.0, 1.1, (560, 900)), "corte",
            sfx=[(0.1, "roce", -26), (d * 0.6, "golpe", -28)])

    @plano(1059, "sorpresa: ¿ya?")
    def _(d):
        t_ya = en(1060)
        return P(["#2a1a12", "#050507"], [
            fondo("bg_cueva_campamento"),
            brillo(820, 640, 420, FRIO, 0.45, 0.62, pulso=[0.1, 0.5]),
            pieza("bea_cara_sorpresa", 540, 990, 1000, z=0.6, keys=[{"t": 0, "escala": 1.12, "y": 1060}, {"t": 0.3, "escala": 1.0, "y": 990, "ease": "golpe"}]
                  + late(t_ya, 1, 0.06, 0.35)),
            pieza("destello", 800, 720, 260, z=0.7, keys=[{"t": 0, "op": 0}, {"t": t_ya, "op": 0, "escala": 0.3},
                                                          {"t": t_ya + 0.12, "op": 1, "escala": 1.0, "rot": 30, "ease": "salida"}, {"t": t_ya + 0.5, "op": 0, "rot": 60}]),
            IMG("estalactita_a", ancho=150, x=-280, y=440, z=0.8), IMG("estalactita_b", ancho=160, x=1360, y=430, z=0.8),
            pie("equipo_frontal_a", -260, 1300, 420, z=0.5), pie("garrafa_agua", 1350, 1300, 180, z=0.5)],
            cam(1.0, 1.22, (540, 960), (540, 900)), "corte",
            sfx=[(0.02, "golpe", -20), (t_ya, "brillo", -24)])

    @plano(1061, "si no me ha dado tiempo a terminar el libro")
    def _(d):
        t_fin = en(1068)
        return P(["#2a1a12", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            brillo(540, 1000, 520, CALIDO, 0.55, 0.2, pulso=[0.06, 1.3]),
            pie("libro_abierto", 540, 1230, 470, z=0.6, keys=K(d, (0, {"rot": -3, "escala": 1.0}), (t_fin / d, {"rot": 2, "escala": 1.03, "x": 540}))
                + lanza(t_fin, t_fin + 0.5, (540, 1050), (215, 1150)) + [{"t": t_fin + 0.5, "rot": -4, "escala": 0.32, "ease": "salida"}]),
            pie("lampara_led", 870, 1300, 230, z=0.62, keys=K(d, (0, {"x": 880}), (1, {"x": 860}))),
            brillo(870, 1180, 220, CALIDO, 0.6, 0.63, pulso=[0.1, 0.9]),
            pie("libro_a", 200, 1300, 70, z=0.6), pie("libro_c", 200, 1265, 70, z=0.61), pie("libro_d", 195, 1230, 70, z=0.62),
            pie("libro_b", -300, 1300, 70, z=0.6), pie("libro_a", -300, 1265, 70, z=0.6), pie("libro_c", 1380, 1300, 70, z=0.6),
            *ambiente_cueva(d, sem=17, oscura=True)],
            cam(1.15, 1.25, (540, 1080), (600, 1080)), "corte",
            sfx=[(0.1, "roce", -27), (t_fin + 0.05, "whoosh", -24)])

    @plano(1071, "eso fue lo que pensó ella: lee junto a la lámpara")
    def _(d):
        return P(["#2a1a12", "#050507"], [
            fondo("bg_cueva_campamento"),
            pie("colchon", 470, 1300, 150, z=0.45),
            *flip(["bea_lee_a", "bea_lee_b"], d, fps=1.2, base=lambda n: pie(n, 450, 1290, 430, z=0.5)),
            pie("lampara_led", 720, 1300, 150, z=0.52),
            brillo(720, 1220, 260, CALIDO, 0.6, 0.51, pulso=[0.08, 1.4]),
            pie("libro_b", 780, 1300, 70, z=0.53), pie("libro_d", 780, 1265, 70, z=0.53), pie("libro_a", 785, 1230, 70, z=0.53),
            pie("mesa_campamento", -280, 1300, 260, z=0.5), pie("tienda_campana", 1420, 1300, 300, z=0.5),
            *ambiente_cueva(d, sem=18)],
            cam(1.25, 1.1, (480, 1120), (560, 1120)), "corte",
            sfx=[(0.6, "roce", -28), (1.45, "roce", -28), (2.3, "roce", -28)])

    @plano(1080, "calculaba: la pared llena de grupos de rayas")
    def _(d):
        marcas = []
        for j in range(12):
            col, fil = j % 4, j // 4
            marcas.append(pieza("marca_grupo", 230 + 205 * col, 700 + 230 * fil, 170, z=0.5,
                                keys=[{"t": 0, "op": 0}, {"t": 0.04 + 0.08 * j, "op": 0, "escala": 1.4}, {"t": 0.1 + 0.08 * j, "op": 1, "escala": 1.0, "ease": "golpe"}]))
        for j in range(8):
            x = (-560 + 190 * (j % 2)) if j < 4 else (1200 + 190 * (j % 2))
            marcas.append(pieza("marca_grupo", x, 760 + 230 * (j // 2 % 2), 150, z=0.5, op=0.8))
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"), brillo(540, 900, 560, CALIDO, 0.4, 0.3),
            IMG("moho_pared", ancho=380, x=-120, y=600, z=0.32, op=0.5), *marcas,
            *ambiente_cueva(d, sem=19, gotas=False)],
            cam(1.08, 1.18, (380, 900), (700, 960)), "corte",
            sfx=[(0.1 + 0.16 * j, "tic", -26) for j in range(6)])

    @plano(1083, "entre 160 y 170 días frente a 500")
    def _(d):
        t170, tdias = en(1087), en(1089)
        base = 1330
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            brillo(540, 1000, 600, CALIDO, 0.35, 0.2),
            barra(330, base, 230, 240, "#f2d6a2", 0.05, t170 + 0.4),
            barra(750, base, 230, 700, "#c0392b", tdias - 0.1, tdias + 0.6),
            brillo(750, 700, 300, "#ff7a5e", 0.5, 0.58, keys=[{"t": 0, "op": 0}, {"t": tdias + 0.5, "op": 0}, {"t": tdias + 0.7, "op": 1}]),
            pieza("marca_grupo", -330, 900, 200, z=0.5, op=0.7), pieza("marca_grupo", 1410, 880, 200, z=0.5, op=0.7),
            *ambiente_cueva(d, sem=20, oscura=True)],
            cam(1.0, 1.08, (540, 1050), (560, 1000)), "corte",
            hud=[contador(0.1, d - 0.05, 0, 170, t170 + 0.35, "", tam=110, x=330, y=1000, color="#ffffff", capsula="#0b0f1ed8", miles=False,
                          contar_prefijo="≈"),
                 contador(tdias, d - 0.05, 170, 500, 0.6, "", tam=130, x=750, y=540, color="#ffd23f", capsula="#0b0f1ee6", miles=False)],
            sfx=[(0.1, "tictac", -27, {"dur": t170 + 0.3, "ritmo": 0.1}), (tdias, "subida", -24, {"dur": 0.6}), (tdias + 0.6, "golpe", -18)])

    # ================================================================== LA SALIDA
    @plano(1090, "sales a la superficie: camina hacia la luz")
    def _(d):
        return P(["#3d2a1f", "#0b0705"], [
            fondo("bg_salida_luz"),
            rayos(540, 600, "#fff4cf", n=12, largo=1100, apertura=5, z=0.1, giro=3, op=0.7),
            brillo(540, 620, 420, "#fff6e0", 0.6, 0.12, keys=K(d, (0, {"escala": 0.8}), (1, {"escala": 1.3}))),
            *flip(["bea_camina_a", "bea_camina_b"], d, fps=4, base=lambda n: pie(n, 420, 1400, 600, z=0.55, ex=-1,
                  keys=K(d, (0, {"x": 260, "y": 1300, "escala": 1.05}), (1, {"x": 470, "y": 1110, "escala": 0.78, "ease": "lineal"})))),
            {**polvo("#fff6e0", 40, (200, 500, 900, 1400), 21), "vel": [5, -20]},
            *lados_cueva(1340, 5), IMG("estalactita_c", ancho=200, x=-300, y=440, z=0.8), IMG("estalactita_a", ancho=160, x=1380, y=430, z=0.8)],
            cam(1.0, 1.15, (500, 1100), (540, 900)), "corte",
            sfx=[(0.1, "golpe", -28), (0.5, "golpe", -29), (0.9, "golpe", -28), (0.3, "brillo", -26)])

    @plano(1094, "pierdes el equilibrio: la luz ciega")
    def _(d):
        return P(["#fff1d6", "#8a6446"], [
            fondo("bg_salida_luz"),
            brillo(540, 620, 700, "#fff6e0", 0.8, 0.1),
            pieza("bea_cara_luz", 540, 1000, 1000, z=0.6, keys=K(d, (0, {"rot": -7, "x": 500}), (0.4, {"rot": 6, "x": 590, "ease": "suave"}),
                                                              (0.75, {"rot": -3, "x": 530, "ease": "suave"}), (1, {"rot": 2, "x": 550, "ease": "suave"}))),
            rayos(540, 500, "#ffffff", n=14, largo=1300, apertura=6, z=0.66, giro=-5, op=0.4),
            fundido_blanco([{"t": 0, "op": 1.0}, {"t": 0.35, "op": 0.15, "ease": "salida"}, {"t": d, "op": 0.35}]),
            pie("estalagmita_a", -350, 1340, 380, z=0.5), pie("estalagmita_b", 1430, 1340, 300, z=0.5)],
            cam(1.0, 1.12, (540, 900), (560, 950), temblor=5), "corte",
            sfx=[(0.02, "brillo", -20), (0.5, "roce", -24)])

    @plano(1097, "y te tienen que sujetar")
    def _(d):
        return P(["#6fb6e8", "#c9a26b"], [
            fondo("bg_entrada_dia"),
            pie("bea_sujetada", 605, 1380, 620, z=0.55, keys=K(d, (0, {"rot": -5, "x": 570}), (0.5, {"rot": 2, "x": 615, "ease": "suave"}),
                                                              (1, {"rot": 0, "x": 605, "escala": 1.03, "ease": "suave"}))),
            pie("voluntario_3", -280, 1380, 560, z=0.5), pie("voluntario_6", 1480, 1380, 540, z=0.5, ex=-1),
            pie("mochila", 1180, 1390, 220, z=0.52), pie("camara_tripode", -60, 1390, 300, z=0.5),
            fundido_blanco([{"t": 0, "op": 0.85}, {"t": 0.6, "op": 0.0, "ease": "salida"}])],
            cam(1.3, 1.42, (605, 1100), (605, 1060)), "corte",
            sfx=[(0.1, "roce", -22), (0.45, "golpe", -24)])

    @plano(1102, "abrazas a gente")
    def _(d):
        return P(["#6fb6e8", "#c9a26b"], [
            fondo("bg_entrada_dia"),
            brillo(620, 900, 420, "#fff1c8", 0.4, 0.1, pulso=[0.08, 1.0]),
            pie("bea_abraza", 605, 1380, 700, z=0.55, keys=late(0.25, 2, 0.04, 0.5)),
            pie("voluntario_1", 200, 1390, 560, z=0.5, keys=K(d, (0, {"x": 160}), (1, {"x": 210}))),
            pie("voluntario_4", 1000, 1395, 540, z=0.5, ex=-1, keys=K(d, (0, {"x": 1040}), (1, {"x": 980}))),
            pie("voluntario_2", -360, 1380, 560, z=0.5), pie("voluntario_5", 1480, 1380, 540, z=0.5, ex=-1)],
            cam(1.45, 1.3, (605, 1000), (605, 1050)), "corte",
            sfx=[(0.2, "roce", -24)])

    @plano(1107, "un año y medio: las hojas del calendario vuelan")
    def _(d):
        r = random.Random(21)
        hojas = []
        for j in range(18):
            t = 0.05 + j * (d - 0.4) / 18
            dx = r.choice([-1, 1]) * r.uniform(500, 1100)
            hojas.append(pieza("calendario_hoja", 540, 1000, 330, z=0.6 + 0.001 * j,
                               keys=[{"t": 0, "op": 0}, {"t": t, "op": 1, "x": 540, "y": 1010, "rot": 0, "escala": 1.0},
                                     {"t": t + 0.6, "x": 540 + dx, "y": 420 - r.uniform(0, 300), "rot": r.uniform(-160, 160), "escala": 0.6, "op": 0.0, "ease": "salida"}]))
        return P(["#6fb6e8", "#c9a26b"], [
            fondo("bg_entrada_dia"),
            negro([{"t": 0, "op": 0.35}], color="#2b1a12"),
            pie("calendario_taco", 540, 1290, 520, z=0.55, keys=K(d, (0, {"rot": -2}), (1, {"rot": 2}))),
            *hojas],
            cam(1.0, 1.12, (540, 1050)), "corte",
            sfx=[(0.05 + j * (d - 0.4) / 18, "roce", -28) for j in range(0, 18, 4)])

    @plano(1113, "que la última vez que la viste: el grupo saluda")
    def _(d):
        return P(["#6fb6e8", "#c9a26b"], [
            fondo("bg_entrada_dia"),
            brillo(540, 900, 520, "#fff1c8", 0.35, 0.1),
            pie("voluntario_1", 330, 1385, 560, z=0.5, keys=late(0.2, 1, 0.05, 0.5)),
            pie("bea_despide", 600, 1395, 610, z=0.55, keys=K(d, (0, {"rot": -3}), (0.5, {"rot": 3, "ease": "suave"}), (1, {"rot": -2, "ease": "suave"}))),
            pie("voluntario_4", 860, 1390, 560, z=0.5, ex=-1, keys=late(0.6, 1, 0.05, 0.5)),
            pie("voluntario_3", -150, 1380, 540, z=0.48), pie("voluntario_6", 1230, 1380, 540, z=0.48, ex=-1),
            pie("voluntario_2", -460, 1380, 520, z=0.47), pie("mochila", 1520, 1390, 220, z=0.5)],
            cam(1.2, 1.32, (600, 1080), (560, 1050)), "corte",
            sfx=[(0.2, "roce", -26)])

    @plano(1120, "lo primero que pides: una ducha")
    def _(d):
        t_d = 0.3
        gotas = [pieza("gota", 500 + 40 * (j % 5) - 40, 900, 26, z=0.62,
                       keys=[{"t": 0, "op": 0}, {"t": t_d + 0.05 * j, "op": 1, "y": 900}, {"t": t_d + 0.05 * j + 0.5, "y": 1450, "op": 0.3, "ease": "entrada"}])
                 for j in range(10)]
        return P(["#cfe3ee", "#6a7d8a"], [
            fondo("bg_ventana_invierno"),
            negro([{"t": 0, "op": 0.55}], color="#18222b"),
            brillo(540, 1050, 560, "#ffffff", 0.45, 0.2),
            pieza("ducha", 540, 1050, 700, z=0.6, keys=[{"t": 0, "op": 1, "y": 700, "escala": 0.8, "rot": -6},
                                                         {"t": 0.35, "y": 1050, "escala": 1.0, "rot": 0, "ease": "rebote"}, {"t": d, "escala": 1.06, "ease": "suave"}]),
            *gotas,
            {**polvo("#ffffff", 40, (-500, 600, 1580, 1500), 22), "vel": [6, -50]},
            IMG("ventana", ancho=420, x=-360, y=980, z=0.4), pie("taza_cafe", 1400, 1480, 200, z=0.5)],
            cam(1.0, 1.1, (540, 1050)), "corte",
            sfx=[(t_d, "agua", -20, {"dur": 1.2})])

    @plano(1126, "una ducha: la toalla")
    def _(d):
        return P(["#cfe3ee", "#6a7d8a"], [
            fondo("bg_ventana_invierno"),
            brillo(540, 900, 600, "#fff6e0", 0.5, 0.2),
            pieza("bea_cara_toalla", 540, 1000, 980, z=0.6, keys=K(d, (0, {"rot": -3, "escala": 1.06}), (1, {"rot": 2, "escala": 1.0, "ease": "suave"}))),
            {**polvo("#ffffff", 50, (-500, 500, 1580, 1500), 23), "vel": [8, -70]},
            pie("ducha", -360, 1300, 600, z=0.5), IMG("ventana", ancho=420, x=1440, y=980, z=0.4)],
            cam(1.12, 1.0, (540, 900)), "corte",
            sfx=[(0.1, "brillo", -26)])

    # ================================================================== LA PRENSA
    @plano(1128, "lo resumió ante los periodistas: los micrófonos se acercan")
    def _(d):
        return P(["#6fb6e8", "#c9a26b"], [
            fondo("bg_entrada_dia"),
            pie("bea_prensa", 605, 1385, 640, z=0.5, keys=K(d, (0, {"escala": 0.98}), (1, {"escala": 1.02}))),
            pieza("microfono_a", 300, 1300, 130, z=0.65, keys=K(d, (0, {"x": 60, "y": 1450, "rot": 40}), (0.6, {"x": 420, "y": 1100, "rot": 32, "ease": "salida"}),
                                                                (1, {"x": 430, "y": 1090, "rot": 31}))),
            pieza("microfono_b", 900, 1300, 130, z=0.66, keys=K(d, (0, {"x": 1150, "y": 1500, "rot": -40}), (0.75, {"x": 800, "y": 1100, "rot": -32, "ease": "salida"}),
                                                                 (1, {"x": 790, "y": 1095, "rot": -31}))),
            pieza("microfono_c", 610, 1700, 130, z=0.67, keys=K(d, (0, {"y": 1800}), (0.9, {"y": 1150, "ease": "salida"}), (1, {"y": 1145}))),
            pie("camara_tripode", -260, 1390, 520, z=0.5), pie("camara_tripode", 1460, 1390, 520, z=0.5, ex=-1),
            pie("voluntario_5", -560, 1380, 520, z=0.45), pie("voluntario_6", 1700, 1380, 520, z=0.45, ex=-1)],
            cam(1.25, 1.45, (605, 1050), (605, 1000)), "corte",
            sfx=[(0.1, "roce", -26), (0.5, "roce", -27), (0.9, "roce", -26)])

    @plano(1132, "los periodistas: flashes")
    def _(d):
        r = random.Random(24)
        fl = []
        for j in range(5):
            t = 0.05 + j * (d - 0.3) / 5
            x, y = r.uniform(140, 940), r.uniform(560, 1300)
            fl.append(pieza("destello", x, y, 380, z=0.8, keys=[{"t": 0, "op": 0}, {"t": t, "op": 0, "escala": 0.3},
                                                               {"t": t + 0.08, "op": 1, "escala": 1.0, "ease": "salida"}, {"t": t + 0.35, "op": 0, "rot": 40}]))
        return P(["#141018", "#050507"], [
            fondo("bg_entrada_atardecer"),
            negro([{"t": 0, "op": 0.6}], color="#0b0f1e"),
            pieza("camara_flash", 540, 1000, 760, z=0.6, keys=K(d, (0, {"rot": -6, "escala": 0.92, "x": 600}), (1, {"rot": 3, "escala": 1.05, "x": 520, "ease": "suave"}))),
            *fl,
            pieza("camara_flash", -330, 900, 400, z=0.5, rot=12), pieza("camara_flash", 1420, 1050, 420, z=0.5, rot=-10, ex=-1),
            pieza("microfono_a", -560, 1200, 120, z=0.5, rot=20), pieza("microfono_b", 1650, 1200, 120, z=0.5, rot=-20)],
            cam(1.0, 1.12, (540, 1000)), "corte",
            sfx=[(0.05 + j * (d - 0.3) / 5, "zap", -25 - j % 2 * 2) for j in range(5)])

    @plano(1135, "sigo atrapada")
    def _(d):
        return P(["#1a2230", "#050507"], [
            fondo("bg_entrada_atardecer"),
            negro([{"t": 0, "op": 0.45}], color="#0b0f1e"),
            pieza("bea_cara_neutra", 540, 1000, 1000, z=0.6, keys=K(d, (0, {"escala": 1.0}), (1, {"escala": 1.05}))),
            pieza("destello", 220, 700, 300, z=0.7, keys=[{"t": 0, "op": 0}, {"t": 0.15, "op": 1, "ease": "salida"}, {"t": 0.45, "op": 0}]),
            pieza("destello", 880, 820, 260, z=0.7, keys=[{"t": 0, "op": 0}, {"t": 0.45, "op": 0}, {"t": 0.55, "op": 1, "ease": "salida"}, {"t": 0.8, "op": 0}]),
            brillo(540, 900, 520, "#9fc4ff", 0.35, 0.2, pulso=[0.1, 0.4]),
            pieza("microfono_a", -280, 1350, 140, z=0.6, rot=25), pieza("microfono_c", 1360, 1350, 140, z=0.6, rot=-25)],
            cam(1.0, 1.14, (540, 880)), "corte",
            sfx=[(0.15, "zap", -27), (0.55, "zap", -28)])

    @plano(1137, "21 de noviembre de 2021: el calendario se congela")
    def _(d):
        t21, tnov, t2021 = en(1139), en(1141), en(1143)
        hojas = [pieza("calendario_hoja", 540, 1010, 560, z=0.62 + 0.001 * j,
                       keys=[{"t": 0, "op": 1, "x": 540, "y": 1010, "rot": 0}, {"t": 0.04 * j, "op": 1, "x": 540, "y": 1010, "rot": 0},
                             {"t": 0.04 * j + 0.35, "x": 540 + (900 if j % 2 else -900), "y": 600, "rot": 120 if j % 2 else -120, "op": 0, "ease": "salida"}])
                 for j in range(6)]
        return P(["#1a2230", "#050507"], [
            fondo("bg_ventana_invierno"),
            negro([{"t": 0, "op": 0.5}], color="#0b0f1e"),
            brillo(540, 1000, 600, "#bfe3ff", 0.4, 0.2, keys=[{"t": 0, "op": 0}, {"t": t21, "op": 0}, {"t": t21 + 0.4, "op": 1}]),
            pieza("calendario_hoja", 540, 1010, 560, z=0.6, keys=[{"t": 0, "rot": 0}, {"t": t21, "rot": 0}, {"t": t21 + 0.05, "rot": -1.5},
                                                                  {"t": t21 + 0.1, "rot": 1.2}, {"t": t21 + 0.16, "rot": 0}, {"t": d, "escala": 1.04}]),
            *hojas,
            *copos(14, d, sem=25, z=0.75),
            pie("calendario_taco", -330, 1480, 380, z=0.5), pie("calendario_taco", 1410, 1480, 380, z=0.5)],
            cam(1.0, 1.1, (540, 1010)), "corte",
            hud=[rotulo(t21, d - 0.05, "21", tam=230, color="#c0392b", capsula=None, x=540, y=1040),
                 rotulo(tnov, d - 0.05, "NOV", tam=80, color="#2a2a2a", capsula=None, x=540, y=1200),
                 rotulo(t2021, d - 0.05, "2021", tam=80, color="#ffffff", capsula="#2a7f9ee6", x=540, y=660)],
            sfx=[(0.02, "roce", -24), (t21, "golpe", -20), (t21 + 0.1, "brillo", -26)])

    @plano(1146, "no sé nada del mundo: el mundo gira sin ella")
    def _(d):
        r = random.Random(26)
        per = []
        for j in range(4):
            y = 650 + 220 * j
            x0, x1 = (-700, 1800) if j % 2 == 0 else (1800, -700)
            per.append(pieza("periodico", x0, y, 360, z=0.7, keys=[{"t": 0, "x": x0, "rot": r.uniform(-20, 20)},
                                                                    {"t": d, "x": x1, "rot": r.uniform(-30, 30), "ease": "lineal"}]))
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_cerebro"),
            negro([{"t": 0, "op": 0.4}], color="#0b0f24"),
            brillo(540, 980, 520, "#6fb6e8", 0.4, 0.2),
            pieza("foto_mundo", 540, 980, 640, z=0.55, keys=K(d, (0, {"rot": 0, "escala": 0.95}), (1, {"rot": 25, "escala": 1.03, "ease": "lineal"}))),
            *per, estrellas(50, 26)],
            cam(1.0, 1.1, (540, 980)), "corte",
            sfx=[(0.1, "whoosh", -26), (d * 0.5, "roce", -27)])

    @plano(1151, "y dijo algo más: que la experiencia había sido…")
    def _(d):
        return P(["#f7a85c", "#c9a26b"], [
            fondo("bg_entrada_dia"),
            rayos(800, 500, "#ffe6a8", n=12, largo=1300, apertura=5, z=0.08, giro=3, op=0.6),
            brillo(820, 560, 520, "#ffd59a", 0.5, 0.1, pulso=[0.06, 1.6]),
            pie("bea_prensa", 480, 1385, 680, z=0.5, keys=K(d, (0, {"x": 440}), (1, {"x": 500}))),
            pieza("microfono_b", 900, 1300, 130, z=0.65, keys=K(d, (0, {"x": 1050, "y": 1450, "rot": -40}), (0.5, {"x": 660, "y": 1110, "rot": -34, "ease": "salida"}),
                                                                 (1, {"x": 650, "y": 1100}))),
            pieza("microfono_a", 100, 1300, 130, z=0.66, keys=K(d, (0, {"x": -150, "y": 1500, "rot": 40}), (0.7, {"x": 290, "y": 1120, "rot": 30, "ease": "salida"}),
                                                                (1, {"x": 300, "y": 1110}))),
            {**polvo("#fff1c8", 30, (-400, 500, 1500, 1400), 27)},
            pie("camara_tripode", -330, 1390, 520, z=0.5), pie("voluntario_4", 1350, 1390, 540, z=0.5, ex=-1)],
            cam(1.2, 1.45, (500, 1050), (480, 960)), "corte",
            sfx=[(0.2, "roce", -26), (1.6, "roce", -27)])

    @plano(1160, "excelente, insuperable: se ríe")
    def _(d):
        t_ins = en(1161)
        return P(["#f7a85c", "#8a5a32"], [
            fondo("bg_entrada_dia"),
            negro([{"t": 0, "op": 0.25}], color="#b8642a"),
            rayos(540, 760, "#ffe6a8", n=16, largo=1400, apertura=5, z=0.1, giro=6, op=0.7),
            brillo(540, 800, 620, "#ffd59a", 0.6, 0.12, pulso=[0.08, 1.2]),
            pieza("bea_cara_rie", 540, 1000, 1000, z=0.6, keys=[{"t": 0, "escala": 0.95, "y": 1040}, {"t": 0.35, "escala": 1.0, "y": 1000, "ease": "elastico"}]
                  + late(t_ins, 2, 0.04, 0.4)),
            {**polvo("#ffe6a8", 50, (-500, 450, 1580, 1500), 28), "vel": [6, -30]},
            pie("flor_blanca", -360, 1370, 300, z=0.4), pie("flor_blanca", 1420, 1370, 300, z=0.4)],
            cam(1.0, 1.12, (540, 900)), "corte",
            sfx=[(0.05, "brillo", -24), (t_ins, "ding", -22)], energia=0.6)

    # ================================================================== TÚ
    @plano(1162, "ahora viene la parte que te afecta a ti: la ciudad")
    def _(d):
        t_ti = en(1169)
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_ciudad"),
            pie("adulto_camina", 500, 1395, 760, z=0.55, keys=K(d, (0, {"x": 300, "y": 1395}), (0.5, {"y": 1385}), (1, {"x": 560, "y": 1395, "ease": "lineal"}))),
            senala(470, 1010, t_ti, d - 0.05, 260, CIAN),
            {**polvo("#ffd9a0", 40, (-500, 600, 1580, 1400), 29), "vel": [-20, -5]},
            pie("voluntario_6", -360, 1395, 520, z=0.45, op=0.7), pie("adulto_camina", 1430, 1395, 520, z=0.45, ex=-1, op=0.7)],
            cam(1.1, 1.2, (480, 1100), (540, 1100)), "barrido",
            sfx=[(0.3, "roce", -28), (t_ti, "senal", -26)])

    @plano(1171, "aunque no vayas a pisar una cueva en tu vida")
    def _(d):
        t_c = en(1177)
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_ciudad"),
            pie("adulto_camina", 640, 1395, 860, z=0.55, ex=-1, keys=K(d, (0, {"x": 860}), (1, {"x": 560, "ease": "lineal"}))),
            pieza("recuerdo_cueva", 300, 760, 380, z=0.65, keys=[{"t": 0, "op": 0, "escala": 0.5, "rot": -10}, {"t": max(0.05, t_c - 0.4), "op": 0, "escala": 0.5},
                                                                  {"t": t_c, "op": 1, "escala": 1.0, "rot": -6, "ease": "rebote"},
                                                                  {"t": d, "y": 900, "rot": 12, "escala": 0.8, "op": 0.0, "ease": "entrada"}]),
            {**polvo("#ffd9a0", 40, (-500, 600, 1580, 1400), 30), "vel": [20, -5]},
            pie("voluntario_3", -420, 1395, 520, z=0.45, op=0.7), pie("voluntario_1", 1450, 1395, 520, z=0.45, op=0.7)],
            cam(1.05, 1.15, (560, 1100), (520, 1050)), "corte",
            sfx=[(t_c, "pop", -24), (d - 0.4, "roce", -27)])

    @plano(1181, "¿recuerdas los veranos? el niño corre por la playa")
    def _(d):
        return P(["#6fb6e8", "#e8c98a"], [
            fondo("bg_playa_verano"),
            brillo(640, 330, 380, "#fff3c0", 0.5, 0.1, pulso=[0.06, 1.4]),
            pie("nino_corre", 300, 1350, 560, z=0.55, keys=K(d, (0, {"x": 160}), (1, {"x": 760, "ease": "lineal"})) + [{"t": 0.0, "y": 1150}]
                + [{"t": round(0.18 * j, 3), "y": 1140 if j % 2 else 1160, "ease": "suave"} for j in range(1, int(d / 0.18) + 1)]),
            pie("balon_playa", 860, 1350, 200, z=0.56, keys=[{"t": 0, "y": 1000}] + cae(0.0, 0.8, 900, 1270) + [{"t": 0.8, "y": 1270}]
                + [{"t": 1.1, "y": 1100, "ease": "salida"}, {"t": 1.5, "y": 1270, "ease": "entrada"}]),
            pie("helado", -300, 1350, 300, z=0.5), pie("bici_nino", 1430, 1350, 260, z=0.5)],
            cam(1.15, 1.25, (540, 1120), (600, 1120)), "corte",
            sfx=[(0.6, "golpe", -24), (0.1, "ola", -26)])

    @plano(1186, "los veranos de pequeño: bici y helado")
    def _(d):
        return P(["#6fb6e8", "#e8c98a"], [
            fondo("bg_playa_verano"),
            pie("bici_nino", 500, 1360, 380, z=0.5, keys=K(d, (0, {"x": -100}), (1, {"x": 640, "ease": "lineal"}))),
            pie("nino_corre", 420, 1330, 330, z=0.45, keys=K(d, (0, {"x": -300}), (1, {"x": 480, "ease": "lineal"}))),
            pieza("helado", 830, 1330, 400, z=0.8, keys=K(d, (0, {"rot": -10, "y": 1500}), (0.4, {"rot": 6, "y": 1320, "ease": "salida"}), (1, {"rot": -3, "y": 1340, "ease": "suave"}))),
            pie("balon_playa", 230, 1300, 120, z=0.4, keys=K(d, (0, {"rot": 0}), (1, {"rot": 90}))),
            pie("helado", -330, 1350, 300, z=0.5), pie("balon_playa", 1420, 1350, 160, z=0.5)],
            cam(1.08, 1.0, (560, 1100)), "corte",
            sfx=[(0.1, "tic", -27), (0.5, "ola", -27)])

    @plano(1191, "tres meses: el sol cruza el cielo")
    def _(d):
        return P(["#ffb15e", "#e8c98a"], [
            fondo("bg_playa_verano"),
            negro([{"t": 0, "op": 0.0}, {"t": d, "op": 0.3}], color="#b8642a"),
            *[{**e, "keys": K(d, (0, {"x": 120, "y": 900}), (0.5, {"x": 540, "y": 600}), (1, {"x": 960, "y": 900}))} for e in D.sol(540, 600, 110, z=0.4)],
            pie("helado", -320, 1350, 300, z=0.5), pie("bici_nino", 1430, 1350, 260, z=0.5)],
            cam(1.0, 1.08, (540, 900)), "corte",
            hud=[contador(0.02, d - 0.02, 0, 90, d * 0.6, " días", tam=120, x=520, y=1180, color="#ffffff", capsula="#c0392be6", miles=False)],
            sfx=[(0.05, "tictac", -27, {"dur": d * 0.7, "ritmo": 0.08})])

    @plano(1193, "parecían una vida entera: los recuerdos se apilan")
    def _(d):
        fotos = []
        for j, (n, x, y, rot) in enumerate([("recuerdo_1", 360, 1080, -8), ("recuerdo_4", 700, 1020, 7), ("recuerdo_3", 480, 900, -3),
                                            ("recuerdo_2", 640, 1170, 10), ("recuerdo_5", 420, 1220, -12)]):
            t = 0.05 + 0.3 * j
            fotos.append(pieza(n, x, y, 330, z=0.6 + 0.01 * j, keys=[{"t": 0, "op": 0}, {"t": t, "op": 1, "y": y - 500, "rot": rot * 3, "escala": 1.3},
                                                                       {"t": t + 0.3, "y": y, "rot": rot, "escala": 1.0, "ease": "salida"}]))
        return P(["#6fb6e8", "#e8c98a"], [
            fondo("bg_playa_verano"),
            brillo(540, 1050, 600, "#fff3c0", 0.4, 0.2),
            *fotos,
            pieza("recuerdo_6", -340, 1000, 300, z=0.5, rot=-8), pieza("recuerdo_8", 1420, 1000, 300, z=0.5, rot=8)],
            cam(1.0, 1.12, (540, 1080)), "corte",
            sfx=[(0.05 + 0.3 * j + 0.3, "tic", -25) for j in range(5)])

    @plano(1197, "y ahora parpadeas")
    def _(d):
        tp = en(1199)
        return P(["#6fb6e8", "#1a2230"], [
            fondo("bg_playa_verano"),
            {**fondo("bg_ventana_invierno", z=0.06), "keys": [{"t": 0, "op": 0}, {"t": tp + 0.15, "op": 0}, {"t": tp + 0.16, "op": 1}], "_bg": "bg_ventana_invierno"},
            negro([{"t": 0, "op": 0.35}], color="#0b0f1e"),
            pieza("ojo", 540, 980, 820, z=0.6, keys=[{"t": 0, "ey": 1.0, "escala": 1.0}, {"t": tp, "ey": 1.0}, {"t": tp + 0.15, "ey": 0.04, "ease": "entrada"},
                                                     {"t": tp + 0.35, "ey": 1.0, "ease": "salida"}, {"t": d, "escala": 1.06}]),
            pieza("recuerdo_1", -330, 980, 300, z=0.5, rot=-6), pieza("recuerdo_5", 1410, 980, 300, z=0.5, rot=6)],
            cam(1.0, 1.1, (540, 980)), "corte",
            sfx=[(tp + 0.12, "pop", -24)])

    @plano(1200, "y es otra vez diciembre")
    def _(d):
        return P(["#1a2230", "#3b2618"], [
            fondo("bg_ventana_invierno"),
            pieza("calendario_diciembre", 540, 1000, 480, z=0.6, keys=[{"t": 0, "y": 300, "rot": -12}] + cae(0.0, 0.6, 300, 1000)
                  + [{"t": 0.6, "rot": 4, "ease": "salida"}, {"t": d, "rot": -2, "ease": "suave"}]),
            *copos(16, d, sem=31, z=0.78),
            {**polvo("#ffffff", 40, (-500, 380, 1580, 1500), 31), "vel": [4, 60]},
            pie("calendario_taco", -340, 1480, 380, z=0.5), IMG("ventana_noche", ancho=420, x=1440, y=960, z=0.4)],
            cam(1.0, 1.1, (540, 1000), (540, 960)), "corte",
            sfx=[(0.4, "golpe", -20)])

    # ================================================================== LA EXPLICACIÓN
    @plano(1205, "la explicación de los psicólogos: el cerebro")
    def _(d):
        t_p = en(1212)
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_cerebro"),
            brillo(540, 980, 520, MAGENTA, 0.3, 0.2, pulso=[0.1, 1.0]),
            pieza("cerebro", 540, 980, 760, z=0.6, keys=aparece(0.05, 0.5) + [{"t": d, "escala": 1.05, "ease": "suave"}]),
            pieza("cerebro_brillo", 540, 980, 760, z=0.61, keys=[{"t": 0, "op": 0}, {"t": t_p, "op": 0}, {"t": t_p + 0.15, "op": 1}, {"t": t_p + 0.6, "op": 0.2},
                                                                  {"t": d, "escala": 1.05, "ease": "suave"}]),
            estrellas(60, 32)],
            cam(1.0, 1.12, (540, 980)), "corte",
            sfx=[(0.05, "brillo", -24), (t_p, "senal", -26)])

    @plano(1213, "es exactamente la misma que la de la cueva")
    def _(d):
        t_c = en(1221)
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_cerebro"),
            pieza("recuerdo_cueva", 300, 980, 420, z=0.6, keys=K(d, (0, {"x": -200, "rot": -12}), (0.45, {"x": 280, "rot": -5, "ease": "salida"}), (1, {"x": 300, "rot": -3}))),
            pieza("pantalla_ordenador", 780, 980, 440, z=0.6, keys=K(d, (0, {"x": 1300, "rot": 12}), (0.45, {"x": 800, "rot": 4, "ease": "salida"}), (1, {"x": 780, "rot": 2}))),
            brillo(300, 980, 300, CALIDO, 0.4, 0.55, keys=[{"t": 0, "op": 0}, {"t": t_c, "op": 0}, {"t": t_c + 0.2, "op": 1}]),
            senala(300, 960, t_c, d - 0.05, 260, AMBAR),
            estrellas(60, 33), pieza("cerebro", -360, 900, 400, z=0.4, op=0.6), pieza("cerebro", 1440, 900, 400, z=0.4, op=0.6)],
            cam(1.0, 1.1, (540, 980)), "corte",
            hud=[rotulo(0.6, d - 0.05, "=", tam=200, color="#ffd23f", capsula=None, x=540, y=960)],
            sfx=[(0.1, "whoosh", -26), (0.6, "ding", -24), (t_c, "golpe", -24)])

    @plano(1222, "de niño todo era nuevo: los recuerdos saltan")
    def _(d):
        fotos = []
        for j, (n, x, y, rot) in enumerate([("recuerdo_4", 250, 700, -10), ("recuerdo_2", 820, 640, 8), ("recuerdo_3", 220, 1020, 6),
                                            ("recuerdo_8", 850, 980, -7), ("recuerdo_5", -300, 900, 5), ("recuerdo_6", 1380, 900, -6)]):
            t = 0.25 + 0.36 * (j % 4)
            fotos.append(pieza(n, x, y, 280, z=0.6, keys=aparece(t, 0.45) + [{"t": t, "rot": rot * 3}, {"t": t + 0.45, "rot": rot, "ease": "salida"},
                                                                               {"t": d, "rot": -rot * 0.5, "ease": "suave"}]))
        return P(["#f7a85c", "#2b1a2e"], [
            fondo("bg_amanecer"),
            brillo(540, 1000, 600, "#ffd59a", 0.5, 0.1, pulso=[0.06, 1.3]),
            pie("nino_corre", 540, 1360, 440, z=0.55, keys=K(d, (0, {"x": 340}), (1, {"x": 640, "ease": "lineal"}))),
            *fotos],
            cam(1.0, 1.1, (540, 1050)), "corte",
            sfx=[(0.25 + 0.36 * j, "pop", -25) for j in range(4)])

    @plano(1229, "recuerdos distintos: lluvia de recuerdos")
    def _(d):
        r = random.Random(35)
        fotos = []
        for j in range(16):
            n = f"recuerdo_{j % 8 + 1}"
            x = r.uniform(-600, 1680); t = r.uniform(0, d * 0.5)
            y0 = r.uniform(-250, 900); y1 = y0 + r.uniform(700, 1000)
            fotos.append(pieza(n, x, y0, r.uniform(200, 320), z=r.uniform(0.4, 0.8),
                               keys=[{"t": 0, "op": 0}, {"t": t, "op": 1, "y": y0, "rot": r.uniform(-40, 40)},
                                     {"t": d, "y": y1, "rot": r.uniform(-30, 30), "ease": "lineal"}]))
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_cerebro"),
            brillo(540, 980, 600, "#ffcf8a", 0.4, 0.2), *fotos, estrellas(50, 35)],
            cam(1.0, 1.1, (540, 960)), "corte",
            sfx=[(0.05, "brillo", -24)] + [(0.2 + 0.3 * j, "tic", -28) for j in range(4)])

    # ================================================================== LA RUTINA
    @plano(1232, "de adulto, los días se parecen: el pasillo")
    def _(d):
        sombras = [pie("adulto_camina", 540, 1440, 600, z=0.5 - 0.01 * k, op=0.3 - 0.08 * k,
                       keys=sigue(K(d, (0, {"y": 1500, "escala": 1.05}), (1, {"y": 1260, "escala": 0.62, "ease": "lineal"})), 0.25 * k))
                   for k in (1, 2, 3)]
        return P(["#c9ced4", "#5f6670"], [
            fondo("bg_oficina_gris"),
            *sombras,
            pie("adulto_camina", 540, 1440, 600, z=0.55, keys=K(d, (0, {"y": 1500, "escala": 1.05}), (1, {"y": 1260, "escala": 0.62, "ease": "lineal"}))),
            pie("adulto_pantalla", -420, 1440, 420, z=0.5), pie("adulto_pantalla", 1500, 1440, 420, z=0.5, ex=-1)],
            cam(1.15, 1.25, (540, 1150)), "corte",
            sfx=[(0.1 + 0.4 * j, "golpe", -30) for j in range(5)])

    def rutina(nombre, i, que, var):
        @plano(i, nombre)
        def _(d):
            if que == "camino":
                suj = pie("adulto_camina", 440 + var * 30, 1440, 820, z=0.55, keys=K(d, (0, {"x": 400 + var * 30}), (1, {"x": 520 + var * 30, "ease": "lineal"})))
                sfx = [(0.05, "golpe", -29)]
            elif que == "pantalla":
                suj = pie("adulto_pantalla", 560, 1440, 720, z=0.55, keys=K(d, (0, {"escala": 1.0 + var * 0.02}), (1, {"escala": 1.04 + var * 0.02})))
                sfx = [(0.05, "tic", -27)]
            else:
                suj = pie("taza_cafe", 540 + var * 20, 1250, 460, z=0.6, keys=cae(0.0, 0.3, 900, 1030) + [{"t": d, "escala": 1.03}])
                sfx = [(0.12, "golpe", -24)]
            return P(["#c9ced4", "#5f6670"], [
                fondo("bg_oficina_gris"),
                brillo(560, 1050, 300, "#bfe3ff", 0.3, 0.2) if que == "pantalla" else brillo(540, 600, 400, "#ffffff", 0.2, 0.1),
                suj,
                pie("adulto_camina", -380, 1440, 560, z=0.45, op=0.6), pie("adulto_camina", 1460, 1440, 560, z=0.45, op=0.6)],
                cam(1.0 + 0.02 * var, 1.06 + 0.02 * var, (540, 1150)), "corte", sfx=sfx)

    rutina("el mismo", 1238, "camino", 0)
    rutina("camino", 1240, "camino", 1)
    rutina("la misma", 1241, "pantalla", 0)
    rutina("pantalla", 1243, "pantalla", 1)
    rutina("la misma", 1244, "taza", 0)
    rutina("rutina", 1246, "taza", 1)

    @plano(1247, "tu cerebro guarda muy poco")
    def _(d):
        r = random.Random(37)
        fotos = []
        for j in range(6):
            a = math.radians(60 * j + 20)
            x0, y0 = 540 + 560 * math.cos(a), 980 + 640 * math.sin(a)
            dentro = (j == 2)
            t = 0.1 + 0.18 * j
            fin = {"x": 540, "y": 980, "escala": 0.2, "op": 0.0} if dentro else {"x": 540 + 420 * math.cos(a), "y": 980 + 420 * math.sin(a), "op": 0.0}
            fotos.append(pieza(f"recuerdo_{j + 1}", x0, y0, 250, z=0.65,
                               keys=[{"t": 0, "op": 0}, {"t": t, "op": 1, "x": x0, "y": y0, "rot": r.uniform(-20, 20)}, {"t": t + 0.7, **fin, "ease": "salida"}]))
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_cerebro"),
            pieza("cerebro", 540, 980, 640, z=0.6, keys=K(d, (0, {"escala": 1.0, "op": 1}), (1, {"escala": 0.94, "op": 0.75}))),
            *fotos, estrellas(40, 37)],
            cam(1.05, 1.0, (540, 980)), "corte",
            sfx=[(0.8, "zap", -27), (1.2, "pop", -26)])

    @plano(1252, "y cuando miras atrás")
    def _(d):
        t_a = en(1255)
        return P(["#1a2230", "#3b2618"], [
            fondo("bg_ventana_invierno"),
            pie("adulto_camina", 540, 1480, 820, z=0.55, keys=[{"t": 0, "x": 700, "ex": 1.0}, {"t": t_a, "x": 560, "ex": 1.0, "ease": "lineal"},
                                                              {"t": t_a + 0.25, "ex": -1.0, "ease": "suave"}, {"t": d, "x": 540}]),
            *copos(8, d, sem=38, z=0.3, area=(380, 520, 700, 900), ancho=(20, 40)),
            pie("calendario_taco", -330, 1480, 380, z=0.5), IMG("ventana_noche", ancho=420, x=1440, y=960, z=0.4)],
            cam(1.0, 1.08, (560, 1150)), "corte",
            sfx=[(t_a, "roce", -24)])

    @plano(1256, "el año entero cabe en un puñado de recuerdos")
    def _(d):
        t_p = en(1262)
        r = random.Random(39)
        hojas = []
        for j in range(12):
            a = math.radians(30 * j)
            x0, y0 = 540 + 380 * math.cos(a), 960 + 380 * math.sin(a)
            hojas.append(pieza("calendario_hoja", x0, y0, 230, z=0.6,
                               keys=[{"t": 0, "op": 0, "escala": 0.5, "x": x0, "y": y0}, {"t": 0.05 + 0.04 * j, "op": 1, "escala": 1.0, "ease": "salida"},
                                     {"t": 0.7, "x": x0, "y": y0, "rot": 0},
                                     {"t": t_p - 0.2, "x": 540, "y": 1060, "rot": r.uniform(-200, 200), "escala": 0.1, "op": 0.0, "ease": "entrada"}]))
        fotos = [pieza(n, x, 1180, 250, z=0.66 + 0.01 * j, keys=[{"t": 0, "op": 0}, {"t": t_p + 0.18 * j, "op": 1, "y": 900, "rot": rot * 3}]
                       + cae(t_p + 0.18 * j, t_p + 0.18 * j + 0.4, 900, 1180 - 30 * j) + [{"t": t_p + 0.18 * j + 0.4, "rot": rot, "ease": "salida"}])
                 for j, (n, x, rot) in enumerate([("recuerdo_2", 520, -8), ("recuerdo_1", 560, 6), ("recuerdo_5", 530, -3)])]
        return P(["#1a2230", "#3b2618"], [
            fondo("bg_ventana_invierno"),
            negro([{"t": 0, "op": 0.4}], color="#0b0f1e"),
            brillo(540, 1150, 360, CALIDO, 0.45, 0.2, keys=[{"t": 0, "op": 0}, {"t": t_p, "op": 1}]),
            *hojas, *fotos,
            pie("calendario_taco", -340, 1480, 380, z=0.5), IMG("ventana_noche", ancho=420, x=1440, y=960, z=0.4)],
            cam(1.0, 1.15, (540, 1000), (540, 1120)), "corte",
            sfx=[(0.1, "whoosh", -26), (t_p - 0.2, "zap", -26)] + [(t_p + 0.18 * j + 0.3, "tic", -24) for j in range(3)])

    @plano(1265, "dicho de otra forma: la rutina es una cueva")
    def _(d):
        t_r, t_c = en(1270), en(1273)
        r = random.Random(40)
        estal = []
        for j, x in enumerate([-520, -280, 60, 220, 400, 700, 880, 1040, 1300, 1560]):
            n = ["estalactita_a", "estalactita_b", "estalactita_c"][j % 3]
            alto = r.uniform(300, 520)
            ww, hh = comun.tam_svg(n)
            y = 200 + alto / 2 - r.uniform(0, 50)
            t = t_r + 0.08 * (j % 5)
            estal.append(IMG(n, ancho=round(alto * ww / hh), x=x, y=round(y), z=0.82,
                             keys=[{"t": 0, "y": round(y) - 700}, {"t": t, "y": round(y) - 700}, {"t": t + 0.45, "y": round(y), "ease": "bote"}]))
        return P(["#c9ced4", "#1a120d"], [
            fondo("bg_oficina_gris"),
            pie("adulto_pantalla", 560, 1440, 560, z=0.55),
            negro([{"t": 0, "op": 0.0}, {"t": t_r, "op": 0.0}, {"t": t_c + 0.2, "op": 0.78, "ease": "suave"}], color="#0d0a08"),
            brillo(640, 1150, 260, "#bfe3ff", 0.6, 0.98, pulso=[0.1, 0.6], keys=[{"t": 0, "op": 0}, {"t": t_c, "op": 0}, {"t": t_c + 0.3, "op": 1}]),
            *estal,
            goteo(300, 420, 1400, 1.6, 0.3, d, z=0.85), goteo(820, 420, 1400, 2.1, 1.1, d, z=0.85, suena=False)],
            cam(1.0, 1.12, (560, 1100), (560, 1050)), "corte",
            sfx=[(t_r, "rumor", -22, {"dur": 1.5}), (t_c, "golpe", -20)])

    @plano(1274, "solo que con ventanas")
    def _(d):
        return P(["#0d0a08", "#050507"], [
            fondo("bg_oficina_gris"),
            negro([{"t": 0, "op": 0.78}], color="#0d0a08"),
            rayos(540, 800, "#fff4cf", n=14, largo=1400, apertura=5, z=0.9, giro=4, keys=[{"t": 0, "op": 0, "escala": 0.3}, {"t": 0.15, "op": 0},
                                                                                         {"t": 0.6, "op": 0.8, "escala": 1.0, "ease": "salida"}]),
            brillo(540, 820, 520, "#fff1c8", 0.7, 0.98, keys=[{"t": 0, "op": 0}, {"t": 0.15, "op": 0}, {"t": 0.5, "op": 1, "ease": "salida"}]),
            {**IMG("ventana", ancho=520, x=540, y=820, z=0.99), "keys": aparece(0.12, 0.5)},
            {**IMG("adulto_pantalla", ancho=440, x=600, y=1280, z=0.985, op=0.9)},
            *techo(41), {**polvo("#fff1c8", 50, (200, 700, 900, 1400), 41), "z": 0.99}],
            cam(1.0, 1.12, (540, 950), (540, 880)), "corte",
            sfx=[(0.12, "brillo", -18), (0.6, "ding", -24)], energia=0.7)

    @plano(1278, "la buena noticia: el truco funciona")
    def _(d):
        t_t = en(1284)
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_cerebro"),
            rayos(540, 980, "#ffe6a8", n=16, largo=1300, apertura=4, z=0.1, giro=8, keys=[{"t": 0, "op": 0}, {"t": t_t, "op": 0}, {"t": t_t + 0.3, "op": 0.8}]),
            pieza("cerebro", 540, 980, 680, z=0.6, keys=K(d, (0, {"escala": 0.9}), (1, {"escala": 1.04}))),
            pieza("cerebro_brillo", 540, 980, 680, z=0.61, keys=[{"t": 0, "op": 0, "escala": 0.9}, {"t": t_t, "op": 0}, {"t": t_t + 0.25, "op": 1, "ease": "salida"},
                                                                  {"t": d, "escala": 1.04}]),
            pieza("destello", 760, 760, 300, z=0.7, keys=[{"t": 0, "op": 0}, {"t": t_t + 0.1, "op": 0, "escala": 0.3}, {"t": t_t + 0.25, "op": 1, "escala": 1.0},
                                                          {"t": t_t + 0.7, "op": 0, "rot": 45}]),
            estrellas(60, 42)],
            cam(1.0, 1.12, (540, 980)), "corte",
            sfx=[(t_t, "subida", -26, {"dur": 0.4}), (t_t + 0.3, "ding", -22)])

    @plano(1286, "también al revés: las hojas vuelven al taco")
    def _(d):
        r = random.Random(43)
        hojas = []
        for j in range(10):
            t = 0.05 + j * 0.09
            dx = (1 if j % 2 else -1) * r.uniform(500, 1000)
            hojas.append(pieza("calendario_hoja", 540, 1000, 300, z=0.6 + 0.001 * j,
                               keys=[{"t": 0, "op": 0, "x": 540 + dx, "y": 420, "rot": r.uniform(-150, 150), "escala": 0.6},
                                     {"t": t, "op": 1}, {"t": t + 0.45, "x": 540, "y": 1000, "rot": 0, "escala": 1.0, "ease": "salida"}]))
        return P(["#f7a85c", "#2b1a2e"], [
            fondo("bg_amanecer"),
            brillo(540, 1000, 560, "#ffd59a", 0.45, 0.2),
            pie("calendario_taco", 540, 1290, 500, z=0.55, keys=K(d, (0, {"rot": 2}), (1, {"rot": -2}))),
            *hojas],
            cam(1.12, 1.0, (540, 1050)), "corte",
            sfx=[(0.05 + 0.09 * j + 0.4, "roce", -28) for j in range(0, 10, 3)])

    @plano(1289, "si quieres que tu vida dure más: hacia el sol")
    def _(d):
        return P(["#f7a85c", "#2b1a2e"], [
            fondo("bg_amanecer"),
            brillo(540, 1100, 520, "#ffd59a", 0.6, 0.1, keys=K(d, (0, {"escala": 0.85}), (1, {"escala": 1.2}))),
            rayos(540, 1180, "#ffe6a8", n=14, largo=1300, apertura=5, z=0.08, giro=3, op=0.6),
            pie("adulto_camina", 540, 1360, 520, z=0.55, keys=K(d, (0, {"x": 380, "escala": 1.05}), (1, {"x": 560, "escala": 0.92, "ease": "lineal"}))),
            {**polvo("#ffe6a8", 40, (-500, 600, 1580, 1400), 44), "vel": [10, -20]},
            pie("flor_primavera", -330, 1360, 260, z=0.5), pie("flor_primavera", 1420, 1360, 220, z=0.5)],
            cam(1.0, 1.1, (500, 1150), (540, 1100)), "corte",
            sfx=[(0.2, "golpe", -30), (0.7, "golpe", -30), (1.2, "golpe", -30)])

    @plano(1296, "no necesitas más años: los tacos se apilan grises")
    def _(d):
        tacos = [pie("calendario_taco", 540 + (12 if j % 2 else -12), 1440 - 290 * j, 360, z=0.55 + 0.01 * j,
                     keys=[{"t": 0, "op": 0}, {"t": 0.05 + 0.25 * j, "op": 1}] + cae(0.05 + 0.25 * j, 0.35 + 0.25 * j, 500 - 290 * j, 1440 - 290 * j - 0.04 * 360)
                     + [{"t": d - 0.4, "op": 1}, {"t": d, "op": 0.35}])
                 for j in range(3)]
        return P(["#c9ced4", "#5f6670"], [
            fondo("bg_oficina_gris"),
            *tacos,
            negro([{"t": 0, "op": 0}, {"t": d * 0.6, "op": 0}, {"t": d, "op": 0.4}], color="#3a3f47"),
            pie("calendario_taco", -360, 1440, 300, z=0.5, op=0.6), pie("calendario_taco", 1440, 1440, 300, z=0.5, op=0.6)],
            cam(1.0, 1.06, (540, 1050)), "corte",
            sfx=[(0.3 + 0.25 * j, "golpe", -24) for j in range(3)])

    @plano(1300, "necesitas más días: estallido de recuerdos")
    def _(d):
        fotos = []
        for j in range(8):
            a = math.radians(45 * j + 10)
            x1, y1 = 540 + 380 * math.cos(a) * 1.0, 980 + 520 * math.sin(a)
            fotos.append(pieza(f"recuerdo_{j + 1}", 540, 980, 250, z=0.6 + 0.005 * j,
                               keys=[{"t": 0, "op": 0, "escala": 0.2}, {"t": 0.08, "op": 1},
                                     {"t": 0.5, "x": x1, "y": y1, "escala": 1.0, "rot": (j - 4) * 6, "ease": "golpe"},
                                     {"t": d, "x": 540 + 430 * math.cos(a), "y": 980 + 580 * math.sin(a), "ease": "suave"}]))
        for j, x in enumerate([-400, -180, 1260, 1480]):
            fotos.append(pieza(f"recuerdo_{(j * 3) % 8 + 1}", x, 900 + 160 * (j % 2), 260, z=0.5, keys=aparece(0.2 + 0.1 * j)))
        return P(["#f7a85c", "#2b1a2e"], [
            fondo("bg_amanecer"),
            rayos(540, 980, "#ffffff", n=18, largo=1400, apertura=4, z=0.1, giro=10, keys=[{"t": 0, "op": 0, "escala": 0.3}, {"t": 0.3, "op": 0.8, "escala": 1.0, "ease": "golpe"}]),
            pieza("destello", 540, 980, 700, z=0.58, keys=[{"t": 0, "op": 1, "escala": 0.3}, {"t": 0.4, "op": 0, "escala": 1.4, "rot": 40}]),
            *fotos],
            cam(1.0, 1.08, (540, 980)), "corte",
            sfx=[(0.02, "impacto", -20), (0.3, "brillo", -24)], energia=0.8)

    @plano(1303, "que no se parezcan a los demás: las estaciones pasan")
    def _(d):
        est = ["hoja_otono", "copo_nieve", "flor_primavera", "sol_verano"]
        cols = ["#b8642a", "#9fc4ff", "#ff8fc8", "#ffd23f"]
        els = []
        n = len(est)
        for j, (e, c) in enumerate(zip(est, cols)):
            t0 = j * d / n; t1 = t0 + d / n
            els.append(pieza(e, 540, 980, 520, z=0.6, keys=[{"t": 0, "op": 0}, {"t": max(0, t0 - 0.01), "op": 0, "escala": 0.4, "rot": -40},
                                                            {"t": t0 + 0.2, "op": 1, "escala": 1.0, "rot": 0, "ease": "rebote"},
                                                            {"t": t1 - 0.05, "op": 1, "rot": 15}, {"t": t1 + 0.05, "op": 0, "escala": 1.3}]))
            els.append(brillo(540, 980, 560, c, 0.55, 0.2, keys=[{"t": 0, "op": 0}, {"t": max(0, t0 - 0.01), "op": 0}, {"t": t0 + 0.1, "op": 1}, {"t": t1, "op": 1}, {"t": t1 + 0.05, "op": 0}]))
        r = random.Random(46)
        for j in range(14):
            e = est[j % 4]
            x, y = r.uniform(-600, 1680), r.uniform(450, 1450)
            if 250 < x < 830 and 650 < y < 1300:
                x += 600 if x > 540 else -600
            els.append(pieza(e, x, y, r.uniform(90, 160), z=0.7, keys=[{"t": 0, "rot": 0, "y": y}, {"t": d, "rot": r.uniform(-120, 120), "y": y + r.uniform(-120, 120), "ease": "lineal"}]))
        return P(["#0b0f24", "#1b1340"], [fondo("bg_cerebro"), negro([{"t": 0, "op": 0.3}], color="#0b0f24"), *els],
                 cam(1.0, 1.1, (540, 980)), "corte",
                 sfx=[(j * d / 4, "pop", -24) for j in range(4)])

    # ================================================================== LA PREGUNTA
    @plano(1310, "así que la pregunta: la entrada al atardecer")
    def _(d):
        return P(["#f7a85c", "#2b1a2e"], [
            fondo("bg_entrada_atardecer"),
            brillo(320, 520, 380, "#ffd59a", 0.5, 0.1, pulso=[0.05, 1.6]),
            pie("bea_camina_a", 760, 1380, 220, z=0.55, ex=-1, keys=K(d, (0, {"x": 820}), (1, {"x": 690, "ease": "lineal"}))),
            {**polvo("#ffe6a8", 30, (-500, 500, 1580, 1400), 47), "vel": [6, -12]},
            pie("estalagmita_b", -420, 1380, 260, z=0.5), pie("mochila", 1450, 1380, 200, z=0.5)],
            cam(1.0, 1.15, (600, 1050), (600, 1030)), "desenfoque",
            sfx=[(0.1, "rumor", -28, {"dur": 1.5})], energia=0.4)

    @plano(1317, "si aguantarías quinientos días bajo tierra")
    def _(d):
        t_b = en(1321)
        return P(["#7fb6dd", "#2a1d14"], [
            fondo("bg_corte_tierra"),
            brillo(605, 1330, 160, CALIDO, 0.85, 0.5, pulso=[0.25, 0.8]),
            pie("bea_lee_a", 605, 1350, 70, z=0.52),
            pieza("cuerda", 605, 900, 18, z=0.4, op=0.6, keys=[{"t": 0, "ey": 0.0, "y": 470}, {"t": t_b, "ey": 0.0, "y": 470}, {"t": t_b + 0.5, "ey": 0.6, "y": 890, "ease": "salida"}]),
            pie("mochila", -420, 470, 120, z=0.5), pie("camara_tripode", 1560, 470, 150, z=0.5)],
            cam(1.0, 1.35, (605, 900), (605, 1250)), "corte",
            hud=[contador(0.1, d - 0.05, 0, 500, 0.9, " días", tam=110, x=470, y=880, color="#ffffff", capsula="#0b0f1ed8", miles=False)],
            sfx=[(0.1, "tictac", -27, {"dur": 0.85, "ritmo": 0.07}), (t_b, "rumor", -24, {"dur": 1.0})])

    @plano(1323, "la pregunta es cuántos días de este año")
    def _(d):
        t_c = en(1326)
        return P(["#1a2230", "#3b2618"], [
            fondo("bg_ventana_invierno"),
            pie("adulto_camina", 540, 1480, 640, z=0.55, ex=-1, keys=K(d, (0, {"x": 600}), (1, {"x": 520, "ease": "lineal"}))),
            pieza("calendario_taco", 820, 860, 220, z=0.6, keys=late(t_c, 2, 0.08, 0.3)),
            *copos(8, d, sem=48, z=0.3, area=(380, 520, 700, 900), ancho=(20, 40)),
            pie("calendario_taco", -330, 1480, 380, z=0.5), IMG("ventana_noche", ancho=420, x=1440, y=960, z=0.4)],
            cam(1.0, 1.1, (600, 1100), (640, 1000)), "corte",
            hud=[contador(t_c, d - 0.05, 0, 365, 0.9, " días", tam=100, x=420, y=620, color="#ffffff", capsula="#2a7f9ee6", miles=False)],
            sfx=[(t_c, "tictac", -27, {"dur": 0.9, "ritmo": 0.06})])

    @plano(1331, "vas a recordar: los recuerdos se encienden")
    def _(d):
        fotos = []
        for j in range(8):
            col, fil = j % 4, j // 4
            x = 170 + 247 * col; y = 820 + 330 * fil
            enciende = j in (1, 4, 6)
            t = 0.25 + 0.25 * [1, 4, 6].index(j) if enciende else None
            ks = [{"t": 0, "op": 0.25, "escala": 0.95}]
            if enciende:
                ks += [{"t": t, "op": 0.25}, {"t": t + 0.15, "op": 1.0, "escala": 1.08, "ease": "salida"}, {"t": d, "escala": 1.02}]
            fotos.append(pieza(f"recuerdo_{j + 1}", x, y, 220, z=0.6, rot=(j % 3 - 1) * 4, keys=ks))
        for j, x in enumerate([-420, -180, 1260, 1500]):
            fotos.append(pieza(f"recuerdo_{(j * 5) % 8 + 1}", x, 980, 220, z=0.55, op=0.25))
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_cerebro"),
            negro([{"t": 0, "op": 0.45}], color="#0b0f24"),
            *fotos,
            *[brillo(170 + 247 * (j % 4), 820 + 330 * (j // 4), 200, CALIDO, 0.5, 0.55,
                     keys=[{"t": 0, "op": 0}, {"t": 0.25 + 0.25 * k, "op": 0}, {"t": 0.4 + 0.25 * k, "op": 1}]) for k, j in enumerate((1, 4, 6))]],
            cam(1.08, 1.0, (540, 980)), "corte",
            sfx=[(0.25 + 0.25 * k, "ding", -26) for k in range(3)])

    @plano(1334, "cuéntamelo: la boca de la cueva")
    def _(d):
        return P(["#f7a85c", "#2b1a2e"], [
            fondo("bg_entrada_atardecer"),
            brillo(320, 520, 380, "#ffd59a", 0.45, 0.1),
            negro([{"t": 0, "op": 0.0}, {"t": d * 0.5, "op": 0.0}, {"t": d, "op": 0.6, "ease": "entrada"}], color="#050507"),
            {**polvo("#ffe6a8", 30, (-500, 500, 1580, 1400), 49), "vel": [6, -12]},
            pie("estalagmita_b", -420, 1380, 260, z=0.5), pie("estalagmita_a", 1500, 1380, 300, z=0.5)],
            cam(1.1, 1.9, (600, 1040), (600, 1040)), "corte",
            sfx=[(0.1, "whoosh", -26)])

    @plano(1335, "¿cuánto aguantarías tú ahí abajo? cierre: la lámpara en la oscuridad")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            pie("bea_lee_a", 520, 1300, 300, z=0.5),
            pie("lampara_led", 690, 1300, 120, z=0.52),
            brillo(690, 1220, 260, CALIDO, 0.65, 0.51, pulso=[0.1, 1.5]),
            *ambiente_cueva(d, sem=50, oscura=True, primer_plano="rocas_primer_plano_b"),
            *lados_cueva(1300, 50),
            negro([{"t": 0, "op": 0}, {"t": d - 1.0, "op": 0}, {"t": d - 0.1, "op": 0.9, "ease": "suave"}]),
            brillo(690, 1220, 120, CALIDO, 0.8, 0.99, keys=[{"t": 0, "op": 0}, {"t": d - 1.2, "op": 0}, {"t": d - 0.5, "op": 1}, {"t": d, "op": 0.6}])],
            cam(1.6, 1.0, (600, 1220), (540, 1100)), "desenfoque",
            sfx=[(0.1, "rumor", -26, {"dur": 2.5}), (d - 1.2, "ding", -28)], energia=0.3)
