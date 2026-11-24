"""Parte 3 (palabras 583–843): «Beatriz aguantó la cuenta hasta el día sesenta y cinco.» … «Y cuando lo arreglaron, volvió a bajar.»"""
import math
import random

from comun import *  # noqa: F401,F403
import comun


# ------------------------------------------------------------------ ayudantes propios de esta parte
def grupos_tiza(x0, x1, y, alto=120, paso=150, z=0.34, sem=1, op=0.9):
    """Grupos de cinco rayas ya hechos en la pared (de x0 a x1, una fila)."""
    r = random.Random(sem)
    out, x = [], x0
    while x <= x1:
        out.append(IMG("marca_grupo", ancho=round(alto * 330 / 340), x=round(x + r.uniform(-12, 12)), y=round(y + r.uniform(-10, 10)),
                       z=z, rot=r.uniform(-5, 5), op=op))
        x += paso
    return out


def onda(x, y, t0, r=120, color=CIAN, dur=0.9, z=0.8, grosor=6, op=0.9):
    """Anillo de sonido que nace en (x, y) y se abre hasta desaparecer."""
    return {"tipo": "forma", "forma": "elipse", "ancho": r * 2, "alto": r * 2, "relleno": "#ffffff", "op_relleno": 0, "grosor": grosor,
            "borde": color, "x": x, "y": y, "z": z,
            "keys": [{"t": 0, "op": 0, "escala": 0.25}, {"t": t0, "escala": 0.25, "op": 0}, {"t": t0 + 0.06, "op": op},
                     {"t": t0 + dur, "escala": 1.9, "op": 0, "ease": "salida"}]}


def bocadillo(x, y, t0, ancho=230, mira=1, color="#f4efe6", z=0.8, puntos="#3a2e28", t1=None):
    """Bocadillo hecho con formas (sin texto): globo, cola de dos burbujas y tres puntos. mira=1 → la cola va a la izquierda."""
    alto = ancho * 0.68
    fin = [] if t1 is None else [{"t": t1, "op": 1}, {"t": t1 + 0.15, "op": 0, "escala": 0.6}]
    ks = aparece(t0, 0.35) + fin
    def f(dx, dy, w, h, c, zz=0.0):
        return {"tipo": "forma", "forma": "elipse", "ancho": w, "alto": h, "relleno": c, "x": x + dx, "y": y + dy, "z": z + zz,
                "keys": [{"t": 0, "op": 0}] + [dict(q) for q in ks], "anim": {"flotar": [8, 1.6]}}
    out = [f(0, 0, ancho, alto, color), f(-mira * ancho * 0.38, alto * 0.55, ancho * 0.16, ancho * 0.16, color),
           f(-mira * ancho * 0.52, alto * 0.82, ancho * 0.09, ancho * 0.09, color)]
    for j in (-1, 0, 1):
        out.append(f(j * ancho * 0.22, 0, ancho * 0.11, ancho * 0.11, puntos, 0.002))
    return out


def tachon(x, y, t0, largo=520, color="#e2412f", z=0.9):
    """Aspa roja que se dibuja de golpe encima de algo."""
    out = []
    for i, g in enumerate((45, -45)):
        out.append({"tipo": "forma", "forma": "redondeado", "ancho": largo, "alto": 34, "relleno": color, "esquinas": 17, "x": x, "y": y, "z": z,
                    "rot": g, "sombra": True,
                    "keys": [{"t": 0, "op": 0, "ex": 0}, {"t": t0 + 0.12 * i, "op": 1, "ex": 0}, {"t": t0 + 0.12 * i + 0.18, "ex": 1, "ease": "golpe"}]})
    return out


def mosca(x, y, ancho, d, keys, z=0.8, fase=0.0):
    """Mosca aleteando (dos fotogramas muy rápidos) con sus claves de posición/escala."""
    out = flip(["mosca_a", "mosca_b"], d, fps=14, t0=fase, base=lambda n: pieza(n, x, y, ancho, z=z, keys=[dict(q) for q in keys]))
    for e in out:
        e["anim"] = {"balanceo": [14, 0.35 + fase]}
        e["fase"] = fase
    return out


def lados_roca(sem=1, suelo=1300, z=0.48):
    """Estalagmitas y rocas en los laterales (solo se ven en el horizontal)."""
    r = random.Random(sem)
    out = []
    for x in (-470, -260, 1330, 1540):
        n = r.choice(["estalagmita_a", "estalagmita_b"])
        out.append(pie(n, x + r.uniform(-40, 40), suelo + r.uniform(-10, 20), r.uniform(180, 320), z=z + r.uniform(-0.04, 0.04)))
    return out


ESTACIONES = ["hoja_otono", "copo_nieve", "flor_primavera", "sol_verano"]


def planos(v, plano):
    w = v.w
    comun.VUELOS += [(w(599), w(599) + 7, (1350, 520), (-320, 600), 140), (w(708), w(708) + 6.5, (-300, 560), (1350, 480), 150),
                     (w(778), w(778) + 6, (1300, 600), (-300, 520), 120), (w(804), w(804) + 6, (-300, 500), (1300, 580), 130)]

    # ============================================================ DÍA 65: deja de contar
    @plano(583, "aguantó la cuenta: pared llena de rayas")
    def _(d):
        # gancho de la parte 3 (dura lo que el rótulo «DÍA 65: DEJA DE CONTAR»): barrido fuerte por la pared de rayas y ella marca
        # una raya tras otra. Nada en y 560–720 los primeros 2,6 s; abajo a la izquierda va «PARTE 3 DE 5».
        tt = [0.5, 0.95, 1.4, 1.85]
        nuevas = [tiza(440 + 46 * i, 985, t, 150, z=0.56) for i, t in enumerate(tt)]
        return P(["#3d2a1f", "#120c08"], [
            fondo("bg_cueva_campamento"), brillo(560, 980, 520, "#ffcf8a", 0.4, 0.3),
            IMG("moho_pared", ancho=380, x=930, y=1210, z=0.32, op=0.55),
            *grupos_tiza(-560, 1640, 850, 125, 150, sem=1), *grupos_tiza(680, 1600, 1000, 125, 150, sem=2),
            *grupos_tiza(-560, 200, 1000, 125, 150, sem=3),
            *nuevas,
            pie("bea_marca_b", 250, 1420, 600, z=0.6, keys=arranque(250, round(1420 - 0.47 * 600), d, "izquierda", 320, 25)),
            *ambiente_cueva(d, sem=31, murc=False)],
            cam(1.4, 1.08, (700, 1040), (520, 1010)),
            hud=[contador(0.45, d - 0.05, 60, 64, 1.5, "", tam=110, x=700, y=1180, color="#ffd23f", capsula="#0b0f1ed8", contar_prefijo="DÍA ")],
            sfx=[(0.0, "whoosh", -20), (0.2, "rumor", -28, {"dur": 2.4})] + [(t + 0.05, "trazo", -22) for t in tt])

    @plano(590, "sesenta y cinco: la raya que cierra el grupo", mas=0.19)  # tras el gancho (2,6 s) y con «PARTE 3 DE 5» legible
    def _(d):
        rayas = [IMG("marca_raya", ancho=round(230 * 70 / 320), x=400 + 62 * i, y=900, z=0.55) for i in range(4)]
        quinta = {**tiza(495, 900, 0.12, 250), "rot": 62}
        return P(["#3d2a1f", "#120c08"], [
            fondo("bg_cueva_campamento"), brillo(540, 900, 480, "#ffcf8a", 0.45, 0.3, pulso=[0.06, 1.3]),
            *grupos_tiza(-600, 300, 900, 230, 270, sem=4), *grupos_tiza(780, 1700, 900, 230, 270, sem=5),
            *rayas, quinta,
            *ambiente_cueva(d, sem=32, murc=False, gotas=False)],
            cam(1.4, 1.25, (520, 930), (500, 920)), "corte",
            hud=[contador(0.05, d - 0.05, 64, 65, 0.3, "", tam=140, x=540, y=1120, color="#ffd23f", capsula="#0b0f1ed8", contar_prefijo="DÍA ")],
            sfx=[(0.15, "trazo", -18), (0.35, "golpe", -22)])

    @plano(593, "ahí se rindió: cierra los ojos y cae la tiza")
    def _(d):
        return P(["#2a1d14", "#07090f"], [
            fondo("bg_cueva_campamento_oscura"), brillo(420, 760, 380, "#ffcf8a", 0.4, 0.3, keys=K(d, (0, {"op": 1}), (1, {"op": 0.5}))),
            pieza("bea_cara_ojos_cerrados", 540, 980, 980, z=0.6, keys=K(d, (0, {"y": 960, "escala": 1.0}), (1, {"y": 1010, "escala": 1.05, "ease": "suave"}))),
            IMG("marca_raya", ancho=46, x=820, y=760, z=0.85, rot=20, keys=cae(0.1, 0.8, 760, 1380) + [{"t": 0.1, "rot": 20}, {"t": 0.8, "rot": 95}]),
            IMG("estalactita_c", ancho=200, x=-250, y=420, z=0.8), IMG("estalactita_a", ancho=150, x=1330, y=400, z=0.8)],
            cam(1.0, 1.1, (540, 980)), "corte", vineta=0.7,
            sfx=[(0.62, "tic", -20), (0.75, "golpe", -27)])

    @plano(596, "dejó de contar: las rayas se apagan")
    def _(d):
        filas = []
        for j, y in enumerate((820, 1000, 1180)):
            for e in grupos_tiza(-560 + 40 * j, 1620, y, 125, 150, sem=10 + j):
                u = min(1, max(0, (1080 - e["x"]) / 1700))
                e["keys"] = [{"t": 0, "op": 0.9}, {"t": 0.1 + 0.7 * u * d, "op": 0.9}, {"t": 0.3 + 0.7 * u * d, "op": 0.05, "ease": "entrada"}]
                filas.append(e)
        return P(["#2a1d14", "#07090f"], [
            fondo("bg_cueva_campamento"), *filas,
            negro(K(d, (0, {"op": 0}), (0.4, {"op": 0}), (1, {"op": 0.55}))),
            *ambiente_cueva(d, sem=33, murc=False)],
            cam(1.2, 1.0, (540, 1000)), "corte",
            hud=[rotulo(0.05, d * 0.7, "DÍA 65", tam=110, color="#ffd23f", capsula="#0b0f1ed8", x=540, y=1330)],
            sfx=[(0.1, "rumor", -26, {"dur": d})])

    @plano(599, "a partir de ese momento: la vela en la oscuridad")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            pie("bea_lee_a", 420, 1300, 300, z=0.45), pie("libro_c", 560, 1300, 50, z=0.46),
            *flip(["vela_a", "vela_b"], d, fps=4, base=lambda n: pie(n, 760, 1380, 420, z=0.7)),
            brillo(760, 1080, 300, "#ffb15e", 0.6, 0.71, pulso=[0.1, 0.7]),
            brillo(450, 1240, 260, "#ffcf8a", 0.3, 0.2),
            *lados_roca(34),
            *ambiente_cueva(d, sem=34, oscura=True)],
            cam(1.0, 1.15, (600, 1150), (680, 1120)), "corte",
            sfx=[(0.1, "rumor", -27, {"dur": d})])

    @plano(605, "difícil de imaginar: dentro de la cabeza")
    def _(d):
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_seccion_cabeza"),
            *flip(["cerebro", "cerebro_brillo"], d, fps=2.5, base=lambda n: pieza(n, 505, 700, 300, z=0.6, keys=late(0.2, 3, 0.06, 0.6))),
            brillo(505, 700, 260, MAGENTA, 0.35, 0.55, pulso=[0.15, 0.8]),
            estrellas(30, 35)],
            cam(1.0, 1.18, (505, 760), (505, 720)), "zoom",
            sfx=[(0.1, "brillo", -24)])

    @plano(610, "el tiempo desaparece: el taco se deshoja y se pierde")
    def _(d):
        hojas = [pieza("calendario_hoja", 540, 900, 300, z=0.7 + 0.01 * i,
                       keys=[{"t": 0, "op": 0}, {"t": 0.15 + 0.22 * i, "op": 1, "x": 540, "y": 900, "rot": 0},
                             {"t": 0.15 + 0.22 * i + 0.8, "op": 0, "x": 540 + (-1) ** i * (380 + 60 * i), "y": 620 + 40 * i, "rot": (-1) ** i * 50,
                              "escala": 0.6, "ease": "salida"}])
                 for i in range(5)]
        return P(["#141018", "#050507"], [
            fondo("bg_negro_cueva"), brillo(540, 930, 420, "#ffcf8a", 0.35, keys=K(d, (0, {"op": 1}), (1, {"op": 0.2}))),
            pie("calendario_taco", 540, 1180, 400, z=0.6, keys=K(d, (0, {"escala": 1.0, "op": 1}), (0.55, {"op": 1}),
                                                                (1, {"escala": 0.45, "op": 0.0, "y": 980, "ease": "entrada"}))),
            *hojas, IMG("estalactita_c", ancho=180, x=-300, y=430, z=0.8), IMG("estalactita_b", ancho=140, x=1380, y=420, z=0.8),
            polvo("#9fc4ff", 30, (-400, 500, 1480, 1400), 36)],
            cam(1.0, 1.08, (540, 950)), "corte",
            sfx=[(0.15 + 0.22 * i, "roce", -27) for i in range(0, 5, 2)])

    @plano(613, "no hay lunes")
    def _(d):
        return P(["#141018", "#050507"], [
            fondo("bg_negro_cueva"),
            pieza("calendario_hoja", 540, 950, 560, z=0.6, keys=K(d, (0, {"rot": -6, "x": 470}), (0.55, {"op": 1}),
                                                                  (1, {"rot": 14, "x": 620, "y": 1060, "op": 0.0, "ease": "entrada"}))),
            brillo(540, 950, 360, "#ffcf8a", 0.3), *ambiente_cueva(d, sem=37, oscura=True, murc=False)],
            cam(1.05, 1.0, (540, 950)), "corte",
            hud=[rotulo(0.05, d - 0.12, "LUNES", tam=80, color="#1d1a18", capsula=None, x=540, y=990, rot=-6)],
            sfx=[(0.1, "roce", -26)])

    @plano(616, "ni domingo")
    def _(d):
        return P(["#141018", "#050507"], [
            fondo("bg_negro_cueva"),
            pieza("calendario_hoja", 560, 930, 600, z=0.6, keys=K(d, (0, {"rot": 8, "escala": 1.0}), (0.5, {"rot": 2, "op": 1}),
                                                                  (1, {"rot": -30, "escala": 0.2, "op": 0.0, "ease": "entrada"}))),
            brillo(560, 930, 360, "#ffcf8a", 0.3), *ambiente_cueva(d, sem=38, oscura=True, murc=False)],
            cam(1.0, 1.1, (560, 940)), "corte",
            hud=[rotulo(0.05, d - 0.12, "DOMINGO", tam=72, color="#c0392b", capsula=None, x=560, y=970, rot=4)],
            sfx=[(d * 0.5, "roce", -26)])

    @plano(618, "no hay mañana: el sol se apaga")
    def _(d):
        return P(["#1b1410", "#050507"], [
            fondo("bg_negro_cueva"),
            brillo(540, 900, 520, "#ffd59a", 0.7, 0.1, keys=K(d, (0, {"op": 1}), (0.35, {"op": 1}), (1, {"op": 0.0}))),
            pieza("sol_dibujo", 540, 900, 440, z=0.6, keys=K(d, (0, {"escala": 0.9, "op": 1, "rot": 0}), (0.35, {"escala": 1.0}),
                                                            (1, {"escala": 0.5, "op": 0.08, "rot": 40, "y": 1000, "ease": "entrada"}))),
            *ambiente_cueva(d, sem=39, oscura=True, murc=False, gotas=False)],
            cam(1.0, 1.06, (540, 920)), "corte", sfx=[(0.05, "brillo", -25)])

    @plano(621, "ni noche: la luna se hunde")
    def _(d):
        return P(["#0b1020", "#050507"], [
            fondo("bg_negro_cueva"), {**estrellas(50, 40), "keys": K(d, (0, {"op": 1}), (1, {"op": 0.0}))},
            brillo(560, 860, 380, "#cfe0ff", 0.4, 0.1, keys=K(d, (0, {"op": 1}), (1, {"op": 0.0}))),
            pieza("luna_creciente", 560, 860, 380, z=0.6, keys=K(d, (0, {"y": 820, "op": 1, "rot": -10}), (0.4, {"op": 1}),
                                                                (1, {"y": 1150, "op": 0.0, "rot": 15, "ease": "entrada"}))),
            *ambiente_cueva(d, sem=40, oscura=True, murc=False, gotas=False)],
            cam(1.08, 1.0, (560, 900)), "corte", sfx=[(0.05, "zap", -28)])

    @plano(623, "no hay semana: siete hojas que se disuelven")
    def _(d):
        hojas = []
        for i in range(7):
            x = 130 + 137 * i
            tt = 0.35 + 0.17 * i
            hojas.append(pie("calendario_hoja", x, 1260 - 40 * (i % 2), 190, z=0.55,
                             keys=[{"t": 0, "op": 0, "y": 1300}, {"t": 0.04 * i, "op": 1, "y": 1260 - 40 * (i % 2) - 0.5 * 190 * 0.46, "ease": "salida"},
                                   {"t": tt, "op": 1, "escala": 1.0, "rot": 0}, {"t": tt + 0.5, "op": 0, "escala": 0.7, "rot": (-1) ** i * 25,
                                                                                 "y": 1000, "ease": "salida"}]))
        hojas += [pie("calendario_hoja", x, 1250, 170, z=0.5, op=0.8) for x in (-420, -250, 1330, 1500)]
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"), brillo(540, 1150, 520, "#ffcf8a", 0.3, 0.2),
            *hojas, polvo("#ffd9a0", 40, (0, 900, 1080, 1300), 41),
            *ambiente_cueva(d, sem=41, oscura=True)],
            cam(1.12, 1.0, (540, 1150)), "corte",
            sfx=[(0.35 + 0.17 * i, "roce", -29) for i in range(0, 7, 2)])

    @plano(629, "solo hay un ahora muy largo: flota en calma")
    def _(d):
        # plano de respiro: ella flota dormida en la oscuridad y la cámara se aleja muy despacio
        return P(["#101624", "#030304"], [
            fondo("bg_negro_cueva"),
            brillo(540, 960, 520, "#7fa6ff", 0.3, 0.1, pulso=[0.08, 2.4]),
            pie("bea_duerme", 540, 1100, 260, z=0.6, keys=K(d, (0, {"rot": -3}), (1, {"rot": 3, "x": 560})), anim={"flotar": [16, 2.6]}),
            pie("lampara_led", 820, 1240, 110, z=0.55, anim={"flotar": [10, 3.1]}), brillo(820, 1200, 160, "#ffcf8a", 0.4, 0.54),
            pie("libro_b", 250, 1250, 50, z=0.55, rot=-15, anim={"flotar": [12, 2.9]}),
            pie("gorro_lana_c", 1350, 1150, 110, z=0.55, rot=10, anim={"flotar": [12, 3.3]}),
            pie("vela_corta", -250, 1200, 160, z=0.55, anim={"flotar": [10, 2.7]}),
            polvo("#cfe0ff", 50, (-500, 400, 1580, 1500), 42),
            *ambiente_cueva(d, sem=42, oscura=True, gotas=False)],
            cam(1.3, 1.0, (540, 1060)), "desenfoque",
            sfx=[(0.2, "rumor", -28, {"dur": d})], energia=0.3)

    @plano(635, "qué haces con un ahora infinito: todo aparece a su alrededor")
    def _(d):
        objs = [("libro_abierto", 220, 760, 260), ("ovillo_lana", 860, 760, 170), ("cuaderno_dibujo", 230, 1250, 250),
                ("garrafa_agua", 860, 1240, 150), ("vela_a", -260, 900, 90), ("gorro_lana_a", 1340, 900, 170),
                ("libro_d", -300, 1250, 230), ("botella_agua", 1330, 1250, 70)]
        els = [pieza(n, x, y, an, z=0.7, keys=aparece(0.3 + 0.22 * i), anim={"flotar": [10, 1.8 + 0.2 * i]}) for i, (n, x, y, an) in enumerate(objs)]
        return P(["#2a1d14", "#07090f"], [
            fondo("bg_cueva_campamento_oscura"), brillo(540, 980, 520, "#ffcf8a", 0.35, 0.3),
            pieza("bea_cara_neutra", 540, 1020, 760, z=0.6, keys=K(d, (0, {"escala": 0.96}), (1, {"escala": 1.04}))),
            *els, *ambiente_cueva(d, sem=43, oscura=True, gotas=False, murc=False)],
            cam(1.0, 1.1, (540, 1000)), "corte",
            sfx=[(0.3 + 0.22 * i, "pop", -27) for i in range(0, 8, 2)])

    # ============================================================ ráfaga de actividades
    @plano(641, "ella leyó")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            *flip(["bea_lee_a", "bea_lee_b"], d, fps=4, base=lambda n: pie(n, 540, 1300, 560, z=0.55)),
            pie("lampara_led", 840, 1300, 150, z=0.56), brillo(840, 1220, 240, "#ffcf8a", 0.5, 0.55, pulso=[0.08, 1.2]),
            *lados_roca(44), *ambiente_cueva(d, sem=44)],
            cam(1.25, 1.4, (540, 1100), (540, 1080)), "corte", sfx=[(0.1, "roce", -24)])

    @plano(643, "sesenta libros: la pila crece")
    def _(d):
        libros = []
        n = 9
        for i in range(n):
            t0 = 0.05 + i * (d * 0.6 / n)
            y = 1300 - i * 46
            nm = ["libro_a", "libro_b", "libro_c", "libro_d"][i % 4]
            libros.append(pie(nm, 540 + (i % 3 - 1) * 14, y, 130, z=0.55 + 0.002 * i,
                              keys=[{"t": 0, "op": 0}, {"t": t0, "op": 1}] + cae(t0, t0 + 0.3, y - 600 - 0.38 * 130, y - 0.38 * 130)))
        lados = [pie(["libro_b", "libro_a", "libro_d", "libro_c"][j % 4], x, 1300 - 44 * j, 120, z=0.5)
                 for x in (-300, 1380) for j in range(7)]
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"), brillo(540, 1150, 380, "#ffcf8a", 0.4, 0.3), *libros, *lados,
            *ambiente_cueva(d, sem=45, murc=False)],
            cam(1.05, 1.15, (540, 1080), (540, 1020)), "corte",
            hud=[contador(0.05, d - 0.05, 0, 60, d * 0.62, " libros", tam=110, x=540, y=560, color="#ffd23f", capsula="#0b0f1ed8")],
            sfx=[(0.05 + i * (d * 0.6 / 9) + 0.2, "golpe", -28) for i in range(0, 9, 2)])

    @plano(645, "hacía ejercicio")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            *flip(["bea_ejercicio_a", "bea_ejercicio_b"], d, fps=2.6, base=lambda n: pie(n, 520, 1300, 680, z=0.55)),
            pie("colchon", 560, 1310, 120, z=0.5), pie("garrafa_agua", 900, 1300, 170, z=0.5),
            pie("mesa_campamento", -320, 1300, 260, z=0.5), pie("mochila", 1380, 1300, 260, z=0.5),
            *ambiente_cueva(d, sem=46)],
            cam(1.0, 1.08, (520, 1050), (560, 1030)), "corte",
            sfx=[(0.38 + 0.77 * i, "golpe", -28) for i in range(2)])

    @plano(647, "dibujaba")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            pieza("cuaderno_dibujo", 540, 960, 900, z=0.6, keys=arranque(540, 960, d, "abajo", 120, 10)),
            flecha([[420, 1000], [500, 900], [580, 960], [680, 860]], 0.15, d * 0.85, "#3a2e28", 6, z=0.62),
            pie("bea_dibuja", -330, 1300, 380, z=0.5), pie("lampara_led", 1340, 1300, 140, z=0.5),
            *ambiente_cueva(d, sem=47, gotas=False, murc=False)],
            cam(1.0, 1.1, (540, 960)), "corte", sfx=[(0.15, "roce", -24)])

    @plano(648, "tejía gorros de lana: se amontonan")
    def _(d):
        g = []
        pos = [(330, 1300), (560, 1300), (790, 1300), (440, 1200), (680, 1200), (560, 1100)]
        for i, (x, y) in enumerate(pos):
            t0 = 0.5 + i * 0.14
            nm = ["gorro_lana_a", "gorro_lana_b", "gorro_lana_c"][i % 3]
            g.append(pie(nm, x, y, 150, z=0.6 + 0.01 * i, keys=[{"t": 0, "op": 0}, {"t": t0, "op": 1}] + cae(t0, t0 + 0.3, y - 700 - 0.4 * 150, y - 0.4 * 150)))
        teje = flip(["bea_teje_a", "bea_teje_b"], 0.36, fps=7, base=lambda n: pie(n, 540, 1300, 420, z=0.55))
        for e in teje:
            e["keys"].append({"t": 0.44, "op": 0.0})
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            *teje,
            *g, pie("ovillo_lana", 900, 1300, 110, z=0.58, anim={"balanceo": [6, 0.8]}),
            *[pie(["gorro_lana_b", "gorro_lana_a", "gorro_lana_c"][j % 3], x, 1300, 130, z=0.5) for j, x in enumerate((-420, -260, 1340, 1500))],
            *ambiente_cueva(d, sem=48, murc=False)],
            cam(1.15, 1.0, (540, 1180)), "corte",
            sfx=[(0.1, "roce", -25)] + [(0.5 + i * 0.14 + 0.15, "pop", -27) for i in range(0, 6, 2)])

    @plano(652, "se bebió")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            pie("bea_bebe", 540, 1300, 680, z=0.55, keys=K(d, (0, {"rot": -2}), (1, {"rot": 3}))),
            pie("garrafa_agua", 820, 1300, 190, z=0.5), pie("garrafa_agua", -300, 1300, 180, z=0.5), pie("garrafa_agua", 1350, 1300, 180, z=0.5),
            *ambiente_cueva(d, sem=49, gotas=False)],
            cam(1.3, 1.4, (540, 880), (540, 860)), "corte", sfx=[(0.15, "agua", -26, {"dur": 0.5})])

    @plano(654, "mil litros de agua: las garrafas se multiplican")
    def _(d):
        gs = []
        k = 0
        for fila, (y, an) in enumerate(((1300, 200), (1120, 180), (960, 160))):
            for c in range(-3, 8):
                x = 100 + 175 * c + 85 * fila
                t0 = 0.05 + 0.035 * k
                ya = fila == 0 and c in (1, 2, 3, 4)   # unas cuantas ya están en el fotograma 0
                gs.append(pie("garrafa_agua", x, y, an, z=0.6 - 0.03 * fila,
                              keys=late(0.0, 1, 0.08) if ya else [{"t": 0, "op": 0}] + aparece(min(t0, d * 0.7), 0.3)))
                k += 1
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"), brillo(540, 1100, 520, "#9fd6ff", 0.3, 0.3),
            *gs, *ambiente_cueva(d, sem=50, murc=False, gotas=False)],
            cam(1.2, 1.0, (540, 1100)), "corte",
            hud=[contador(0.05, d - 0.05, 0, 1000, d * 0.7, " litros", tam=110, x=540, y=600, color="#7fdcff", capsula="#0b0f1ed8")],
            sfx=[(0.1, "agua", -24, {"dur": 1.0})])

    @plano(658, "ni una sola ducha")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            pieza("ducha", 540, 960, 520, z=0.6, keys=arranque(540, 960, d, "arriba", 160, 10)),
            *tachon(560, 980, d * 0.5, 600),
            polvo("#c9a26b", 40, (200, 700, 880, 1300), 51),
            *lados_roca(51), *ambiente_cueva(d, sem=51, murc=False)],
            cam(1.0, 1.08, (540, 980)), "corte", sfx=[(d * 0.5, "golpe", -20), (d * 0.5 + 0.12, "golpe", -24)])

    @plano(665, "en un año y medio: la vela se consume")
    def _(d):
        def vela(n, a, b):
            return pie(n, 540, 1340, 640, z=0.6, keys=[{"t": 0, "op": 1 if a == 0 else 0}, {"t": a * d, "op": 1}, {"t": b * d, "op": 1 if b >= 1 else 0}])
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            vela("vela_a", 0, 0.33), vela("vela_b", 0.33, 0.66), vela("vela_corta", 0.66, 1.0),
            brillo(540, 900, 340, "#ffb15e", 0.6, 0.55, keys=K(d, (0, {"y": 760}), (0.33, {"y": 790}), (0.66, {"y": 900}), (1, {"y": 1180})), pulso=[0.1, 0.5]),
            *[pie("vela_corta", x, 1340, 260, z=0.55) for x in (-420, -230, 1310, 1500)],
            *ambiente_cueva(d, sem=52, oscura=True, murc=False)],
            cam(1.0, 1.1, (540, 1100), (540, 1180)), "corte",
            sfx=[(d * 0.33, "tic", -27), (d * 0.66, "tic", -27)])

    # ============================================================ hablar sola
    @plano(670, "tampoco habló con nadie: camina sola por la galería")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_galeria"),
            *flip(["bea_camina_a", "bea_camina_b"], d, fps=3, base=lambda n: pie(n, 540, 1360, 380, z=0.55,
                  keys=K(d, (0, {"x": 420, "escala": 1.0}), (1, {"x": 620, "escala": 0.8, "ease": "lineal"})))),
            brillo(560, 1120, 300, "#fff1c8", 0.4, 0.4, pulso=[0.12, 0.5]),
            *bocadillo(640, 900, 0.3, 170, mira=1, t1=d * 0.65),
            *lados_roca(53, 1360), *ambiente_cueva(d, sem=53)],
            cam(1.15, 1.0, (540, 1150)), "corte", sfx=[(0.1, "golpe", -30), (0.6, "golpe", -30), (1.1, "golpe", -30), (0.3, "pop", -28)])

    @plano(674, "lo contó ella misma al salir: micrófonos")
    def _(d):
        mics = [("microfono_a", 230, 1150, -28), ("microfono_b", 850, 1180, 28), ("microfono_c", 540, 1330, 0)]
        els = []
        for i, (n, x, y, r) in enumerate(mics):
            els.append(pieza(n, x, y, 110, z=0.7, rot=r, keys=lanza(0.1 + 0.12 * i, 0.5 + 0.12 * i, (x + (x - 540) * 1.2, y + 500), (x, y))))
        return P(["#fff6e0", "#3d2a1f"], [
            fondo("bg_salida_luz"),
            pie("bea_prensa", 540, 1340, 640, z=0.55, keys=K(d, (0, {"escala": 0.97}), (1, {"escala": 1.02}))),
            *els, pie("camara_tripode", -300, 1340, 380, z=0.5), pie("camara_tripode", 1380, 1340, 380, z=0.5, ex=-1),
            fundido_blanco(K(d, (0, {"op": 0}), (0.55, {"op": 0}), (0.58, {"op": 0.7}), (0.75, {"op": 0}))),
            polvo("#fff6e0", 40, (-400, 400, 1480, 1400), 54)],
            cam(1.0, 1.1, (540, 980)), "corte", sfx=[(d * 0.56, "zap", -24), (0.1, "roce", -26)])

    @plano(680, "llevaba un año y medio: las estaciones pasan arriba")
    def _(d):
        est = []
        for i, n in enumerate(ESTACIONES + ESTACIONES[:2]):
            t0 = 0.05 + i * d / 6.2
            est.append(pieza(n, 540, 700, 230, z=0.7, keys=[{"t": 0, "op": 0}, {"t": t0, "op": 0, "x": 1240, "y": 760},
                                                          {"t": t0 + 0.05, "op": 1}, {"t": t0 + 0.6, "x": -160, "y": 640, "rot": 160, "ease": "lineal"},
                                                          {"t": t0 + 0.62, "op": 0}]))
            est[-1]["_ancho"] = True
        return P(["#6fb6e8", "#c9a26b"], [
            fondo("bg_entrada_dia"),
            brillo(605, 1220, 160, "#ffcf8a", 0.3, 0.2, pulso=[0.2, 0.6]),
            *est,
            negro(K(d, (0, {"op": 0}), (0.25, {"op": 0.45}), (0.5, {"op": 0}), (0.75, {"op": 0.45}), (1, {"op": 0})), color="#0b1430")],
            cam(1.0, 1.06, (605, 1000)), "corte", sfx=[(0.05, "whoosh", -27)])

    @plano(685, "sin hablar con nadie: el bocadillo se vacía")
    def _(d):
        return P(["#2a1d14", "#07090f"], [
            fondo("bg_cueva_campamento_oscura"), brillo(380, 760, 360, "#ffcf8a", 0.35, 0.3),
            pieza("bea_cara_neutra", 480, 1020, 880, z=0.6, keys=K(d, (0, {"escala": 1.0}), (1, {"escala": 1.05}))),
            *bocadillo(840, 640, 0.0, 240, mira=1, t1=d * 0.55),
            IMG("estalactita_c", ancho=200, x=-260, y=420, z=0.8), IMG("estalactita_a", ancho=150, x=1330, y=400, z=0.8),
            pie("rocas_primer_plano_b", 540, 1920, 460, z=0.9)],
            cam(1.0, 1.1, (500, 980)), "corte", sfx=[(d * 0.55, "pop", -26)])

    @plano(689, "más que consigo misma: habla sola")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            *flip(["bea_habla_a", "bea_habla_b"], d, fps=3.5, base=lambda n: pie(n, 470, 1300, 520, z=0.55)),
            *bocadillo(780, 800, 0.2, 200, mira=1, t1=0.9), *bocadillo(260, 720, 0.8, 170, mira=-1),
            pie("lampara_led", 820, 1300, 130, z=0.56), brillo(820, 1230, 220, "#ffcf8a", 0.5, 0.55, pulso=[0.08, 1.2]),
            *lados_roca(55), *ambiente_cueva(d, sem=55)],
            cam(1.08, 1.0, (520, 1060)), "corte", sfx=[(0.2, "pop", -27), (0.8, "pop", -27)])

    @plano(693, "tú también acabarías haciéndolo: su reflejo en el charco")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            pieza("charco", 540, 1330, 1100, z=0.5),
            pie("bea_habla_b", 540, 1240, 480, z=0.55),
            IMG("bea_habla_b", ancho=round(480 * 760 / 820), x=540, y=round(1240 + 0.43 * 480), z=0.52, ey=-0.55, op=0.35,
                anim={"flotar": [4, 1.2]}),
            brillo(540, 1250, 360, "#9fc4ff", 0.3, 0.3, pulso=[0.1, 1.6]),
            *[goteo(540 + dx, 420, 1300, 2.2, f, d, z=0.7) for dx, f in ((-160, 0.3), (190, 1.4))],
            *lados_roca(56, 1300), *ambiente_cueva(d, sem=56, oscura=True, gotas=False)],
            cam(1.0, 1.2, (540, 1100), (540, 1300)), "corte", sfx=[(0.1, "agua", -28, {"dur": 0.8})])

    @plano(697, "comentando en voz alta lo que lees")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            *flip(["bea_lee_a", "bea_lee_b"], d, fps=1.8, base=lambda n: pie(n, 420, 1300, 520, z=0.55)),
            *bocadillo(760, 780, 0.25, 220, mira=1, t1=1.1), *bocadillo(820, 640, 1.2, 180, mira=1),
            pie("libro_a", 760, 1300, 70, z=0.52), pie("libro_c", 760, 1270, 70, z=0.53),
            pie("vela_b", -300, 1300, 260, z=0.5), pie("libro_abierto", 1360, 1300, 110, z=0.5),
            *ambiente_cueva(d, sem=57)],
            cam(1.0, 1.1, (480, 1050), (560, 1000)), "corte", sfx=[(0.25, "pop", -27), (1.2, "pop", -27), (0.6, "roce", -27)])

    @plano(704, "discutiendo contigo: dos Beatriz")
    def _(d):
        pinchos = [[0, -110], [40, -60], [110, -80], [80, -20], [140, 20], [70, 40], [80, 110], [10, 60], [-50, 120], [-60, 50],
                   [-140, 60], [-90, 0], [-150, -60], [-60, -50], [-40, -120]]
        def grito(x, y, t0, t1, c):
            return {"tipo": "forma", "forma": "poligono", "puntos": pinchos, "relleno": c, "x": x, "y": y, "z": 0.8,
                    "keys": [{"t": 0, "op": 0}] + aparece(t0, 0.25) + [{"t": t1, "op": 1}, {"t": t1 + 0.1, "op": 0}], "anim": {"balanceo": [6, 0.3]}}
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            pie("bea_habla_a", 300, 1300, 460, z=0.55, keys=late(0.1, 1, 0.05)),
            pie("bea_habla_a", 790, 1300, 460, z=0.55, ex=-1, keys=late(0.8, 1, 0.05)),
            grito(470, 820, 0.1, 0.75, "#f4efe6"), grito(620, 800, 0.8, d - 0.1, "#ffd23f"),
            *lados_roca(58), *ambiente_cueva(d, sem=58, murc=False)],
            cam(1.0, 1.12, (540, 1080)), "corte", sfx=[(0.1, "pop", -24), (0.8, "pop", -24)])

    @plano(706, "riéndote solo")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"), brillo(380, 700, 320, "#ffcf8a", 0.4, 0.65),
            pieza("bea_cara_rie", 540, 990, 960, z=0.6, keys=late(0.05, 4, 0.03, 0.3)),
            *[pieza("nota_musical_a" if i % 2 else "nota_musical_b", x, 700, 110, z=0.8,
                    keys=[{"t": 0, "op": 0}, {"t": 0.2 + 0.3 * i, "op": 0.0, "y": 760}, {"t": 0.25 + 0.3 * i, "op": 0.9},
                          {"t": 0.9 + 0.3 * i, "op": 0, "y": 560, "ease": "salida"}]) for i, x in enumerate((830, 250, 880))],
            IMG("estalactita_c", ancho=200, x=-260, y=420, z=0.8), IMG("estalactita_b", ancho=150, x=1330, y=420, z=0.8),
            pie("libro_d", -330, 1300, 70, z=0.5), pie("gorro_lana_b", 1380, 1300, 150, z=0.5)],
            cam(1.0, 1.08, (540, 960)), "corte", sfx=[(0.2, "burbuja", -26), (0.5, "burbuja", -27), (0.8, "burbuja", -27)])

    # ============================================================ el precio: el silencio
    @plano(708, "la cueva te cobra un precio: la galería se oscurece")
    def _(d):
        return P(["#1a120d", "#030304"], [
            fondo("bg_cueva_galeria"),
            brillo(540, 1050, 380, "#ffcf8a", 0.45, 0.3, keys=K(d, (0, {"op": 1}), (1, {"op": 0.15}))),
            negro(K(d, (0, {"op": 0}), (1, {"op": 0.5}))),
            *lados_roca(60, 1360), *ambiente_cueva(d, sem=60)],
            cam(1.0, 1.35, (540, 1050), (540, 1000)), "corte",
            sfx=[(0.1, "rumor", -24, {"dur": d})], energia=0.35)

    @plano(715, "el primero es el silencio: una sola gota")
    def _(d):
        tg = d * 0.62
        return P(["#0b0d14", "#020203"], [
            fondo("bg_negro_cueva"),
            IMG("estalactita_c", ancho=180, x=540, y=380, z=0.6),
            IMG("gota", ancho=34, x=540, y=650, z=0.65, keys=[{"t": 0, "y": 640, "op": 1, "ey": 0.7}, {"t": tg * 0.6, "y": 660, "ey": 1.0},
                                                            {"t": tg, "y": 1250, "ease": "entrada"}, {"t": tg + 0.01, "op": 0}]),
            pieza("charco", 540, 1280, 520, z=0.55),
            pieza("salpicadura", 540, 1250, 220, z=0.6, keys=[{"t": 0, "op": 0}, {"t": tg, "op": 0, "escala": 0.3}, {"t": tg + 0.05, "op": 1},
                                                              {"t": tg + 0.6, "escala": 1.2, "op": 0, "ease": "salida"}]),
            onda(540, 1290, tg + 0.05, 160, "#9fc4ff", 1.1, 0.56, 4, 0.6),
            brillo(540, 1270, 260, "#9fc4ff", 0.25, 0.3),
            IMG("estalactita_a", ancho=140, x=-200, y=420, z=0.7, op=0.6), IMG("estalactita_b", ancho=130, x=1300, y=400, z=0.7, op=0.6)],
            cam(1.08, 1.0, (540, 960)), "corte", vineta=0.8,
            sfx=[(tg, "burbuja", -20, {"f": 1000})], energia=0.25)

    @plano(721, "en tu vida normal: la ciudad")
    def _(d):
        return P(["#1b2540", "#0b0f1e"], [
            fondo("bg_ciudad"),
            pie("adulto_camina", 540, 1390, 520, z=0.6, keys=K(d, (0, {"x": 260}), (1, {"x": 640, "ease": "lineal"}))),
            pie("voluntario_4", 1380, 1390, 480, z=0.55), pie("voluntario_6", -320, 1390, 480, z=0.55),
            *[onda(x, y, t, 90, "#ffd59a", 0.9, 0.4, 4, 0.5) for x, y, t in ((200, 900, 0.1), (860, 820, 0.5), (500, 760, 0.9))],
            polvo("#ffe9b0", 30, (-400, 500, 1480, 1300), 61)],
            cam(1.0, 1.06, (540, 1100)), "corte", sfx=[(0.1, "rumor", -24, {"dur": d})])

    @plano(725, "nunca estás en silencio de verdad: la oficina zumba")
    def _(d):
        return P(["#9aa0a8", "#3c4048"], [
            fondo("bg_oficina_gris"),
            pie("adulto_pantalla", 540, 1440, 460, z=0.55),
            *[onda(x, y, t, 80, c, 0.9, 0.7, 5, 0.7) for x, y, t, c in ((690, 1180, 0.1, CIAN), (300, 1000, 0.4, AMBAR), (760, 900, 0.8, CIAN),
                                                                         (420, 860, 1.2, AMBAR), (650, 1100, 1.5, CIAN))],
            *[pieza("nota_musical_b" if i % 2 else "nota_musical_a", x, 900, 90, z=0.75,
                    keys=[{"t": 0, "op": 0}, {"t": 0.2 + 0.45 * i, "op": 0, "y": 980}, {"t": 0.25 + 0.45 * i, "op": 0.8},
                          {"t": 1.1 + 0.45 * i, "op": 0, "y": 700, "ease": "salida"}]) for i, x in enumerate((300, 820, 450, 760))],
            pie("taza_cafe", -280, 1440, 160, z=0.5), pie("telefono_campo", 1350, 1440, 160, z=0.5)],
            cam(1.0, 1.08, (540, 1150)), "corte", sfx=[(0.1, "senal", -30), (0.8, "tic", -28), (1.5, "senal", -30)])

    @plano(731, "siempre hay un coche")
    def _(d):
        return P(["#1b2540", "#0b0f1e"], [
            fondo("bg_ciudad"),
            pieza("recuerdo_8", 540, 980, 520, z=0.65, keys=lanza(0.0, 0.45, (1400, 1050), (540, 980)) + [{"t": 0, "rot": 12}, {"t": 0.45, "rot": -4}]),
            *[onda(560, 1060, t, 200, "#ffd59a", 0.8, 0.7, 6, 0.7) for t in (0.4, 0.8)],
            brillo(540, 1100, 400, "#ffd59a", 0.3, 0.2),
            polvo("#ffe9b0", 30, (-400, 500, 1480, 1300), 62)],
            cam(1.0, 1.1, (540, 1000)), "corte", sfx=[(0.05, "whoosh", -26), (0.4, "rumor", -25, {"dur": 0.8})])

    @plano(735, "una nevera")
    def _(d):
        return P(["#4a2a1c", "#1a0e08"], [
            fondo("bg_ventana_invierno"),
            pie("caja_comida", 540, 1330, 330, z=0.6, keys=arranque(540, 1330 - 0.42 * 330, d, "abajo", 140, 8)),
            *[onda(540, 1150, t, 170, CIAN, 0.6, 0.7, 5, 0.6) for t in (0.15, 0.45)],
            pie("taza_cafe", -300, 1480, 160, z=0.5), pie("periodico", 1380, 1480, 200, z=0.5)],
            cam(1.08, 1.0, (540, 1150)), "corte", sfx=[(0.1, "senal", -29, {"f": 120})])

    @plano(737, "un vecino")
    def _(d):
        return P(["#4a2a1c", "#1a0e08"], [
            fondo("bg_ventana_invierno"),
            pie("voluntario_5", 540, 1480, 700, z=0.6, keys=arranque(540, 1480 - 0.47 * 700, d, "derecha", 200, 15)),
            *[pieza("nota_musical_a" if i % 2 else "nota_musical_b", x, 800, 100, z=0.75,
                    keys=[{"t": 0, "op": 0}, {"t": 0.15 + 0.3 * i, "op": 0, "y": 860}, {"t": 0.2 + 0.3 * i, "op": 0.9},
                          {"t": 0.9 + 0.3 * i, "op": 0, "y": 640, "ease": "salida"}]) for i, x in enumerate((830, 260))],
            pie("bici_nino", -300, 1480, 200, z=0.5), pie("voluntario_2", 1400, 1480, 600, z=0.55)],
            cam(1.0, 1.08, (540, 1100)), "corte", sfx=[(0.2, "golpe", -27), (0.4, "golpe", -28)])

    @plano(739, "ahí abajo no hay nada")
    def _(d):
        return P(["#0b0d14", "#020203"], [
            fondo("bg_negro_cueva"),
            pie("bea_oye", 540, 1344, 420, z=0.55, keys=K(d, (0, {"escala": 1.15}), (1, {"escala": 0.9}))),
            brillo(560, 1100, 240, "#ffcf8a", 0.35, 0.4, keys=K(d, (0, {"op": 1}), (1, {"op": 0.5}))),
            *ambiente_cueva(d, sem=63, oscura=True)],
            cam(1.2, 1.0, (540, 1150)), "corte", vineta=0.8, sfx=[], energia=0.25)

    @plano(744, "tu cerebro no lo soporta")
    def _(d):
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_cerebro"),
            pieza("cerebro", 540, 960, 640, z=0.6, keys=late(0.1, 5, 0.05, 0.36)),
            brillo(540, 960, 420, MAGENTA, 0.3, 0.3, pulso=[0.2, 0.36]),
            *[pieza("cerebro", x, y, 300, z=0.4, op=0.35, anim={"flotar": [10, 2]}) for x, y in ((-380, 900), (1460, 1000))]],
            cam(1.0, 1.12, (540, 960), temblor=4), "corte",
            sfx=[(0.1, "golpe", -27), (0.46, "golpe", -27), (0.82, "golpe", -26), (1.18, "golpe", -25)])

    @plano(750, "empieza a fabricar sonidos: ondas en la oscuridad")
    def _(d):
        pts = [(300, 760), (820, 900), (520, 1180), (200, 1150), (880, 640), (600, 820), (-350, 900), (1400, 1000), (400, 1000)]
        cs = [CIAN, MAGENTA]
        return P(["#0b0d14", "#020203"], [
            fondo("bg_negro_cueva"),
            *[onda(x, y, 0.0 + 0.23 * i, 130, cs[i % 2], 1.0, 0.7, 6, 0.9) for i, (x, y) in enumerate(pts)],
            *[onda(x, y, 0.4 + 0.23 * i, 90, cs[(i + 1) % 2], 0.9, 0.7, 4, 0.7) for i, (x, y) in enumerate(pts[::-1])],
            brillo(540, 960, 380, MAGENTA, 0.18, 0.2, pulso=[0.3, 0.9]),
            *[pieza("nota_musical_a" if i % 2 else "nota_musical_b", x, y, 120, z=0.75, keys=[{"t": 0, "op": 0}] + aparece(0.3 + 0.4 * i, 0.3) +
                    [{"t": 0.9 + 0.4 * i, "op": 0}], anim={"flotar": [12, 1.5]}) for i, (x, y) in enumerate(pts[:5])],
            *ambiente_cueva(d, sem=64, oscura=True, murc=False)],
            cam(1.0, 1.12, (540, 960)), "corte",
            sfx=[(0.15 + 0.46 * i, "senal", -29, {"f": 900 + 200 * i}) for i in range(4)])

    @plano(756, "alucinaciones auditivas: se lleva la mano a la oreja")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            pie("bea_oye", 540, 1300, 720, z=0.55, keys=K(d, (0, {"escala": 0.98}), (1, {"escala": 1.04}))),
            *[onda(470 + (i % 2) * 120, 700, 0.2 + 0.4 * i, 90, [CIAN, MAGENTA][i % 2], 0.9, 0.7, 5, 0.8) for i in range(5)],
            brillo(560, 720, 260, "#ffcf8a", 0.4, 0.4),
            *lados_roca(65), *ambiente_cueva(d, sem=65, oscura=True)],
            cam(1.0, 1.25, (540, 950), (540, 800)), "corte",
            sfx=[(0.2 + 0.4 * i, "senal", -30, {"f": 1300 + 150 * i}) for i in range(0, 5, 2)])

    @plano(760, "lo explicó con una frase: micrófonos de cerca")
    def _(d):
        return P(["#fff6e0", "#3d2a1f"], [
            fondo("bg_salida_luz"),
            pie("bea_prensa", 540, 1340, 1000, z=0.55, keys=K(d, (0, {"x": 500}), (1, {"x": 560}))),
            pieza("microfono_b", 700, 1100, 150, z=0.7, rot=20, keys=lanza(0.05, 0.4, (1100, 1500), (700, 1080))),
            pieza("microfono_a", 380, 1150, 150, z=0.7, rot=-20, keys=lanza(0.2, 0.55, (-100, 1500), (390, 1120))),
            pieza("camara_flash", -330, 900, 300, z=0.6), pieza("camara_flash", 1420, 950, 300, z=0.6, ex=-1),
            fundido_blanco(K(d, (0, {"op": 0}), (0.6, {"op": 0}), (0.63, {"op": 0.6}), (0.8, {"op": 0})))],
            cam(1.0, 1.08, (540, 900)), "corte", sfx=[(0.05, "roce", -26), (d * 0.61, "zap", -26)])

    @plano(766, "que da escalofríos: cara de miedo")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"), brillo(540, 760, 360, "#9fc4ff", 0.35, 0.3, pulso=[0.15, 0.4]),
            pieza("bea_cara_miedo", 540, 1000, 960, z=0.6, keys=K(d, (0, {"escala": 1.0}), (1, {"escala": 1.08}))),
            IMG("estalactita_c", ancho=200, x=-260, y=420, z=0.8), IMG("estalactita_a", ancho=150, x=1330, y=400, z=0.8),
            polvo("#9fc4ff", 30, (-300, 500, 1380, 1400), 67)],
            cam(1.0, 1.1, (540, 960), temblor=3), "corte", sfx=[(0.1, "rumor", -24, {"dur": d})])

    @plano(769, "estás en silencio: negro total")
    def _(d):
        return P(["#060709", "#010102"], [
            fondo("bg_negro_cueva"),
            pieza("haz_frontal", 600, 1000, 900, z=0.5, rot=-8, keys=K(d, (0, {"op": 0.9, "rot": -12}), (1, {"op": 0.1, "rot": 6}))),
            brillo(240, 1060, 160, "#fff1c8", 0.5, 0.5, keys=K(d, (0, {"op": 1}), (1, {"op": 0.15}))),
            polvo("#9fc4ff", 25, (-300, 500, 1380, 1400), 68),
            *ambiente_cueva(d, sem=68, oscura=True, murc=False, gotas=False)],
            cam(1.0, 1.15, (540, 1150)), "corte", vineta=0.9,
            sfx=[(d - 1.0, "subida", -18, {"dur": 1.0})], energia=0.2)

    @plano(772, "y el cerebro se lo inventa")
    def _(d):
        cs = [CIAN, MAGENTA]
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_cerebro"),
            pieza("cerebro_brillo", 540, 960, 680, z=0.6, keys=aparece(0.0, 0.45)),
            brillo(540, 960, 520, CIAN, 0.45, 0.3, pulso=[0.2, 0.5]),
            *[onda(540, 960, 0.1 + 0.25 * i, 300, cs[i % 2], 1.1, 0.5, 7, 0.9) for i in range(7)],
            *[pieza("nota_musical_b" if i % 2 else "nota_musical_a", x, y, 120, z=0.75,
                    keys=lanza(0.2 + 0.15 * i, 0.9 + 0.15 * i, (540, 960), (x, y)) + [{"t": 0, "op": 0}, {"t": 0.2 + 0.15 * i, "op": 1}])
              for i, (x, y) in enumerate(((180, 640), (900, 700), (200, 1250), (880, 1280), (-380, 960), (1460, 960)))],
            fundido_blanco(K(d, (0, {"op": 0.8}), (0.15, {"op": 0.0})), color="#e8f6ff")],
            cam(1.15, 1.0, (540, 960)), "corte",
            sfx=[(0.0, "impacto", -14)], energia=0.85)

    # ============================================================ las moscas
    @plano(778, "su peor momento: parpadea")
    def _(d):
        return P(["#2a1d14", "#07090f"], [
            fondo("bg_cueva_campamento_oscura"), brillo(400, 760, 360, "#ffcf8a", 0.35, 0.3),
            *flip(["bea_cara_neutra", "bea_cara_parpadea", "bea_cara_neutra", "bea_cara_neutra"], d, fps=6,
                  base=lambda n: pieza(n, 540, 1000, 920, z=0.6, keys=K(d, (0, {"x": 600, "escala": 1.0}), (1, {"x": 500, "escala": 1.04})))),
            IMG("estalactita_b", ancho=160, x=-260, y=420, z=0.8), IMG("estalactita_c", ancho=180, x=1330, y=400, z=0.8),
            pieza("mosca_a", 980, 600, 110, z=0.85, keys=K(d, (0, {"x": 1100, "y": 700}), (1, {"x": 820, "y": 620})), anim={"balanceo": [20, 0.2]})],
            cam(1.0, 1.08, (540, 960)), "corte", sfx=[(0.3, "zap", -32, {"f0": 400, "f1": 300})], energia=0.4)

    @plano(783, "no fue un sonido: la nota cae")
    def _(d):
        return P(["#0b0d14", "#020203"], [
            fondo("bg_negro_cueva"),
            pieza("nota_musical_b", 540, 900, 320, z=0.6, keys=K(d, (0, {"rot": 0}), (1, {"rot": 40})) + cae(0.15, 0.75, 760, 1240)
                  + [{"t": 0.9, "op": 1}, {"t": d, "op": 0}]),
            onda(540, 1240, 0.45, 200, MAGENTA, 0.8, 0.55, 5, 0.6),
            *tachon(540, 980, 0.5, 440, "#c0392b"),
            *ambiente_cueva(d, sem=70, oscura=True, murc=False)],
            cam(1.0, 1.08, (540, 1000)), "corte", sfx=[(0.5, "golpe", -24)])

    @plano(787, "una invasión de moscas")
    def _(d):
        r = random.Random(71)
        ms = []
        for i in range(22):
            ang = r.uniform(0, 6.28)
            x0, y0 = 540 + 1300 * math.cos(ang), 960 + 1100 * math.sin(ang)
            x1, y1 = r.uniform(-200, 1280), r.uniform(560, 1380)
            t0 = r.uniform(0, d * 0.5)
            ms += mosca(x0, y0, r.uniform(60, 120), d, [{"t": 0, "x": x0, "y": y0}, {"t": t0, "x": x0, "y": y0},
                                                         {"t": t0 + 0.6, "x": x1, "y": y1, "ease": "salida"},
                                                         {"t": d, "x": x1 + r.uniform(-60, 60), "y": y1 + r.uniform(-60, 60)}],
                        z=0.7 + 0.005 * i, fase=r.uniform(0, 0.07))
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"), brillo(540, 1150, 420, "#ffcf8a", 0.35, 0.3),
            pie("bea_lee_b", 540, 1300, 330, z=0.5), pie("lampara_led", 720, 1300, 110, z=0.52),
            *ms, *ambiente_cueva(d, sem=71, oscura=True, murc=False)],
            cam(1.0, 1.1, (540, 1050)), "corte", sfx=[(0.0, "rumor", -22, {"dur": d}), (0.4, "zap", -30, {"f0": 500, "f1": 350})])

    @plano(792, "llegó a cubrirla por completo")
    def _(d):
        r = random.Random(72)
        ms = []
        for i in range(34):
            x, y = r.gauss(540, 150), r.gauss(820, 220)
            t0 = 0.05 + i * (d * 0.75 / 34)
            ms += mosca(x, y, r.uniform(55, 95), d, [{"t": 0, "escala": 0.0}, {"t": t0, "escala": 0.0, "x": x + r.uniform(-300, 300), "y": y - 300},
                                                      {"t": t0 + 0.3, "escala": 1.0, "x": x, "y": y, "ease": "salida"},
                                                      {"t": d, "x": x + r.uniform(-25, 25), "y": y + r.uniform(-25, 25)}],
                        z=0.7 + 0.003 * i, fase=r.uniform(0, 0.07))
        for i in range(12):
            x, y = r.choice([r.uniform(-500, -60), r.uniform(1140, 1580)]), r.uniform(500, 1300)
            ms += mosca(x, y, r.uniform(60, 100), d, [{"t": 0, "x": x, "y": y}, {"t": d, "x": x + r.uniform(-120, 120), "y": y + r.uniform(-80, 80)}],
                        z=0.7, fase=r.uniform(0, 0.07))
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"), brillo(540, 900, 380, "#ffcf8a", 0.35, 0.3),
            pie("bea_moscas", 540, 1300, 740, z=0.55, keys=K(d, (0, {"rot": -1}), (0.5, {"rot": 2}), (1, {"rot": -2}))),
            *ms, negro(K(d, (0, {"op": 0}), (0.6, {"op": 0}), (1, {"op": 0.35}))),
            *ambiente_cueva(d, sem=72, oscura=True, murc=False, gotas=False)],
            cam(1.0, 1.22, (540, 950), (540, 860), temblor=2), "corte",
            sfx=[(0.0, "rumor", -20, {"dur": d}), (0.6, "zap", -28, {"f0": 520, "f1": 380}), (1.4, "zap", -28, {"f0": 480, "f1": 360})])

    @plano(798, "sola, a setenta metros bajo tierra")
    def _(d):
        return P(["#7fb6dd", "#2a1d14"], [
            fondo("bg_corte_tierra"),
            brillo(605, 1330, 140, "#ffcf8a", 0.8, 0.5, pulso=[0.25, 0.7]),
            senala(605, 1330, 0.4, d - 0.1, 90, AMBAR),
            *[pieza("mosca_a", 605 + dx, 1310 + dy, 14, z=0.55, anim={"flotar": [5, 0.4 + 0.05 * j]}) for j, (dx, dy) in
              enumerate(((-30, -10), (20, -20), (40, 10), (-10, 15), (5, -30)))],
            polvo("#ffe9b0", 25, (-300, 600, 1380, 1400), 73)],
            cam(1.9, 1.0, (605, 1300), (605, 1000)), "zoom",
            sfx=[(0.1, "rumor", -26, {"dur": d}), (0.4, "ding", -26)], energia=0.35)

    # ============================================================ el fallo técnico
    @plano(804, "y hubo un susto más")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"), brillo(540, 760, 380, "#ffcf8a", 0.4, 0.3),
            pieza("bea_cara_sorpresa", 540, 1000, 960, z=0.6, keys=late(0.15, 1, 0.08) + K(d, (0, {"y": 1030}), (1, {"y": 990}))),
            IMG("estalactita_c", ancho=200, x=-260, y=420, z=0.8), IMG("estalactita_b", ancho=150, x=1330, y=420, z=0.8)],
            cam(1.0, 1.15, (540, 960), temblor=4), "corte", sfx=[(0.12, "golpe", -18)])

    @plano(809, "cerca del día trescientos: todo lo acumulado")
    def _(d):
        pila = [pie(["libro_a", "libro_b", "libro_c", "libro_d"][j % 4], 230, 1300 - 44 * j, 130, z=0.5) for j in range(8)]
        gor = [pie(n, x, 1300, 140, z=0.52) for n, x in (("gorro_lana_a", 760), ("gorro_lana_c", 890), ("gorro_lana_b", 825))]
        gor += [pie("gorro_lana_b", 825, 1190, 130, z=0.53)]
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            *pila, *gor, pie("vela_corta", 520, 1300, 230, z=0.52), brillo(520, 1150, 200, "#ffb15e", 0.5, 0.5, pulso=[0.1, 0.6]),
            *[pie("garrafa_agua", x, 1300, 170, z=0.5) for x in (-460, -300, -140)], *[pie("bolsa_basura", x, 1300, 180, z=0.5) for x in (1240, 1400)],
            *ambiente_cueva(d, sem=74)],
            cam(1.0, 1.08, (540, 1100), (540, 1060)), "corte",
            hud=[contador(0.05, d - 0.05, 240, 300, d * 0.6, "", tam=130, x=540, y=640, color="#ffd23f", capsula="#0b0f1ed8", contar_prefijo="DÍA ")],
            sfx=[(0.05, "tictac", -28, {"dur": d * 0.6, "ritmo": 0.08})])

    @plano(813, "un fallo técnico: chispa y la lámpara se apaga")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            pie("lampara_led", 540, 1300, 420, z=0.6, keys=K(d, (0, {"rot": 0}), (0.3, {"rot": -4}), (0.5, {"rot": 3}), (1, {"rot": 0}))),
            brillo(540, 1060, 380, "#ffcf8a", 0.7, 0.55,
                   keys=[{"t": 0, "op": 1}, {"t": 0.12, "op": 0.1}, {"t": 0.2, "op": 1}, {"t": 0.3, "op": 0.0}, {"t": 0.38, "op": 0.7}, {"t": 0.5, "op": 0.0}]),
            pieza("destello", 640, 1000, 260, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0.3}, {"t": 0.12, "op": 1, "escala": 1.0, "rot": 20},
                                                           {"t": 0.35, "op": 0, "escala": 0.5, "rot": 60}]),
            pieza("piloto_rojo", 440, 1220, 46, z=0.7, anim={"parpadeo": [0.0, 0.25]}),
            negro(K(d, (0, {"op": 0}), (0.45, {"op": 0}), (0.6, {"op": 0.5}))),
            *ambiente_cueva(d, sem=75, oscura=True, murc=False, gotas=False)],
            cam(1.1, 1.18, (540, 1150), temblor=3), "corte", sfx=[(0.1, "zap", -18), (0.3, "zap", -24)])

    @plano(816, "la obligó a salir: sube por el pozo")
    def _(d):
        return P(["#0d0b0a", "#030304"], [
            fondo("bg_cueva_pozo"),
            brillo(540, 430, 260, "#fff3d6", 0.6, 0.1, pulso=[0.1, 1.1]),
            pie("bea_baja_cuerda", 560, 1500, 1050, z=0.6, keys=K(d, (0, {"y": 1250}), (1, {"y": 760, "ease": "suave"}))),
            {**polvo("#fff3d6", 40, (300, 420, 780, 1500), 76), "vel": [4, -50]},
            IMG("estalactita_a", ancho=160, x=-200, y=420, z=0.8), IMG("estalactita_c", ancho=180, x=1300, y=400, z=0.8),
            pie("rocas_primer_plano_a", 540, 1920, 520, z=0.9)],
            cam(1.15, 1.0, (560, 1000), (540, 860)), "corte",
            sfx=[(0.1, "roce", -22), (0.8, "roce", -25), (1.5, "roce", -25)])

    @plano(823, "ocho días en una tienda de campaña")
    def _(d):
        return P(["#0b1020", "#1a1626"], [
            fondo("bg_tienda_noche"),
            pie("tienda_campana", 454, 1380, 300, z=0.55, keys=aparece(0.05, 0.4)),
            brillo(454, 1290, 260, "#ffb15e", 0.6, 0.56, pulso=[0.1, 0.9]),
            pieza("luna_creciente", 540, 620, 150, z=0.3, keys=K(d, (0, {"x": 160, "y": 700}), (1, {"x": 900, "y": 560, "ease": "lineal"}))),
            estrellas(40, 77),
            pie("mochila", 760, 1380, 150, z=0.56), pie("rocas_primer_plano_b", 454, 1920, 420, z=0.9)],
            cam(1.0, 1.12, (454, 1200)), "desenfoque",
            hud=[contador(0.1, d - 0.05, 1, 8, d * 0.75, " días", tam=110, x=480, y=820, color="#ffd23f", capsula="#0b0f1ed8")],
            sfx=[(0.1, "tictac", -29, {"dur": d * 0.7, "ritmo": 0.3})])

    @plano(831, "sola y sin hablar con nadie: noche tras noche")
    def _(d):
        return P(["#0b1020", "#1a1626"], [
            fondo("bg_tienda_noche"),
            pie("tienda_campana", 300, 1380, 240, z=0.55),
            brillo(300, 1310, 200, "#ffb15e", 0.5, 0.56, pulso=[0.1, 1.3]),
            pie("bea_habla_b", 640, 1380, 300, z=0.56, keys=K(d, (0, {"rot": -1}), (1, {"rot": 1}))),
            fugaz(0.5, 900, 560, 500, 700), estrellas(50, 78),
            negro(K(d, (0, {"op": 0}), (0.5, {"op": 0.35}), (1, {"op": 0})), color="#060a18"),
            pie("rocas_primer_plano_a", 454, 1920, 420, z=0.9)],
            cam(1.2, 1.0, (500, 1250)), "corte", sfx=[(0.5, "fugaz", -27)], energia=0.3)

    @plano(837, "cuando lo arreglaron, volvió a bajar: el frontal se enciende y baja por el pozo")
    def _(d):
        # corte limpio al final de la parte: el frontal se enciende y ella vuelve a bajar
        return P(["#0d0b0a", "#030304"], [
            fondo("bg_cueva_pozo"),
            brillo(540, 430, 260, "#fff3d6", 0.5, 0.1, keys=K(d, (0, {"op": 1}), (1, {"op": 0.4}))),
            pie("bea_baja_cuerda", 560, 1500, 1050, z=0.6, keys=K(d, (0, {"y": 620, "escala": 1.0}), (0.3, {"y": 660}), (1, {"y": 1120, "escala": 0.75, "ease": "entrada"}))),
            brillo(640, 600, 200, "#ffe2a8", 0.7, 0.62, keys=K(d, (0, {"op": 0, "y": 420}), (0.2, {"op": 0, "y": 440}), (0.24, {"op": 1}),
                                                                (0.28, {"op": 0.2}), (0.33, {"op": 1, "y": 470}), (1, {"y": 880, "ease": "entrada"}))),
            {**polvo("#fff3d6", 40, (300, 420, 780, 1500), 80), "vel": [4, 80]},
            IMG("estalactita_c", ancho=200, x=-150, y=420, z=0.8), IMG("estalactita_b", ancho=150, x=1250, y=380, z=0.8),
            pie("rocas_primer_plano_b", 540, 1920, 520, z=0.9)],
            cam(1.0, 1.2, (540, 800), (560, 1100)), "corte",
            sfx=[(d * 0.22, "ding", -22), (d * 0.4, "roce", -20), (d * 0.8, "golpe", -26)])
