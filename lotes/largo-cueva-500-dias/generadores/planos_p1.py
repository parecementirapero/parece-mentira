"""Parte 1 (palabras 0–286): «Imagina que bajas a una cueva.» … «Y está condenado a fallar.»"""
from comun import *  # noqa: F401,F403
import comun

ROJO = "#ff3b3b"


# ------------------------------------------------------------------ ayudantes propios de la parte 1
def pos(nombre, x, suelo, alto, esc=1.0, **mas):
    """Clave {x, y, escala} que deja los pies de una pieza posada (`pie`) en `suelo` aunque cambie de escala."""
    return {"t": 0, "x": x, "y": round(suelo - (comun.APOYO.get(nombre, 0.97) - 0.5) * alto * esc, 1), "escala": esc, **mas}


def aspa(cx, cy, r, t0, color=ROJO, g=22, z=0.8):
    """Aspa (tachado) que se dibuja en dos trazos sobre un objeto."""
    return [flecha([[cx - r, cy - r], [cx + r, cy + r]], t0, t0 + 0.16, color, g, punta=False, z=z),
            flecha([[cx + r, cy - r], [cx - r, cy + r]], t0 + 0.14, t0 + 0.3, color, g, punta=False, z=z)]


def onda(x, y, t0, r=160, color=CIAN, dur=0.8, g=6, z=0.7, ey=1.0):
    """Anillo que se abre y se apaga (sonido, gota en el agua, señal que se pierde)."""
    return {"tipo": "forma", "forma": "elipse", "ancho": r * 2, "alto": round(r * 2 * ey), "relleno": "#ffffff", "op_relleno": 0,
            "grosor": g, "borde": color, "x": x, "y": y, "z": z,
            "keys": [{"t": 0, "escala": 0.15, "op": 0}, {"t": t0, "escala": 0.15, "op": 0}, {"t": t0 + 0.05, "op": 0.9},
                     {"t": t0 + dur, "escala": 1.0, "op": 0.0, "ease": "salida"}]}


def lados(suelo, sem=1, z=0.5):
    """Estalagmitas y rocas en los laterales (solo se ven en el horizontal)."""
    r = random.Random(sem)
    out = []
    for x in (-560, -260, 1340, 1620):
        n = r.choice(["estalagmita_a", "estalagmita_b"])
        out.append(pie(n, x + r.uniform(-40, 40), suelo, r.uniform(260, 420), z=z))
    return out


def cae_vela(nombre, x, suelo, alto, t0, t1, z=0.5, desde=-500):
    """Objeto posado que cae del cielo con bote hasta su suelo."""
    y1 = pos(nombre, x, suelo, alto)["y"]
    return pie(nombre, x, suelo, alto, z=z, keys=[{"t": 0, "op": 0, "y": desde}, {"t": t0, "op": 0, "y": desde}, {"t": t0 + 0.02, "op": 1}] + cae(t0, t1, desde, y1)[1:])


def planos(v, plano):
    w = v.w
    # cruces de murciélagos de esta parte (tiempo absoluto: siguen de un plano a otro)
    comun.VUELOS += [(w(19), w(19) + 6.5, (1300, 560), (-300, 470), 150), (w(200), w(200) + 7, (-300, 520), (1350, 610), 130),
                     (w(94), w(94) + 5, (-300, 640), (1350, 520), 160), (w(181), w(181) + 6, (1350, 560), (-300, 650), 120),
                     (w(239), w(239) + 7, (1350, 600), (-300, 520), 120), (w(263), w(263) + 6.5, (-300, 560), (1350, 640), 110)]

    def rel(i0):
        return lambda j: round(w(j) - w(i0), 3)

    @plano(0, "gancho: bajas por el pozo")
    def _(d):
        # Gancho: ella ya está bajando en el fotograma 0, la luz de arriba se aleja y cae polvo
        return P(["#0d0b0a", "#030304"], [
            fondo("bg_cueva_pozo"),
            brillo(540, 430, 260, "#fff3d6", 0.5, 0.1, pulso=[0.1, 1.1]),
            {**polvo("#fff3d6", 40, (300, 420, 780, 1500), 3), "vel": [4, 60]},
            pie("bea_baja_cuerda", 560, 1500, 1150, z=0.6, keys=K(d, (0, {"y": 520}), (1, {"y": 1080, "ease": "suave"}))),
            brillo(640, 600, 170, "#ffe2a8", 0.65, 0.62, keys=K(d, (0, {"y": 160}), (1, {"y": 720, "ease": "suave"}))),
            IMG("estalactita_c", ancho=200, x=-150, y=420, z=0.8), IMG("estalactita_a", ancho=150, x=1250, y=380, z=0.8),
            pie("rocas_primer_plano_b", 540, 1920, 520, z=0.9)],
            cam(1.0, 1.18, (540, 960), (560, 1050)), vineta=0.7,
            sfx=[(0.02, "roce", -18), (0.4, "golpe", -24), (d * 0.6, "roce", -24)])

    @plano(6, "setenta metros: corte de la montaña")
    def _(d):
        return P(["#7fb6dd", "#2a1d14"], [
            fondo("bg_corte_tierra"),
            flecha([[605, 470], [605, 1250]], 0.1, d * 0.75, CIAN, 8, [18, 14]),
            brillo(605, 1330, 120, "#ffcf8a", 0.8, 0.5, pulso=[0.2, 0.6]),
            pie("bea_despide", 600, 470, 90, z=0.55, keys=aparece(0.05)),
            senala(605, 1330, d * 0.7, d - 0.05, 90, AMBAR)],
            cam(1.0, 1.08, (605, 900), (605, 1100)), "corte",
            hud=[contador(0.1, d - 0.05, 0, 70, d * 0.7, " m", tam=120, x=820, y=900, color="#ffffff", capsula="#0b0f1ed8", miles=False)],
            sfx=[(d * 0.72, "ding", -20)])

    @plano(10, "sin reloj: el reloj de arena se pierde en la oscuridad")
    def _(d):
        return P(["#141018", "#050507"], [
            fondo("bg_negro_cueva"), brillo(540, 900, 380, "#ffcf8a", 0.4),
            pieza("reloj_arena_a", 540, 900, 300, z=0.6, keys=K(d, (0, {"escala": 1.0, "rot": 0, "op": 1}), (1, {"escala": 0.55, "rot": 25, "op": 0.0, "y": 1050, "ease": "entrada"}))),
            IMG("estalactita_b", ancho=130, x=-200, y=400, z=0.8), IMG("estalactita_a", ancho=120, x=1300, y=420, z=0.8)],
            cam(1.08, 1.0, (540, 920)), "corte", sfx=[(0.05, "zap", -22)])

    @plano(12, "sin teléfono: el móvil se apaga")
    def _(d):
        return P(["#141018", "#050507"], [
            fondo("bg_negro_cueva"), brillo(540, 920, 420, "#9fc4ff", 0.5, keys=K(d, (0, {"op": 1}), (0.8, {"op": 0}))),
            pieza("telefono_movil", 540, 930, 300, z=0.6, keys=K(d, (0, {"rot": -8, "op": 1}), (0.85, {"rot": 6, "y": 1010, "op": 0.15, "ease": "entrada"}))),
            IMG("estalactita_c", ancho=180, x=-350, y=430, z=0.8), IMG("estalactita_b", ancho=140, x=1400, y=420, z=0.8)],
            cam(1.0, 1.06, (540, 930)), "corte", sfx=[(d * 0.55, "zap", -24)])

    @plano(15, "sin ver el sol: el amanecer se tapa")
    def _(d):
        return P(["#f7a85c", "#2b1a2e"], [
            fondo("bg_amanecer"), brillo(540, 1000, 500, "#ffd59a", 0.6, 0.1),
            negro(K(d, (0, {"op": 0.0}), (0.45, {"op": 0.0}), (1, {"op": 1.0, "ease": "entrada"})))],
            cam(1.0, 1.1, (540, 1000)), "corte", sfx=[(0.05, "brillo", -22)])

    @plano(19, "y te quedas ahí, completamente sola")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            pie("bea_lee_a", 540, 1300, 300, z=0.5),
            pie("lampara_led", 700, 1300, 110, z=0.52),
            brillo(690, 1230, 230, "#ffcf8a", 0.55, 0.51, pulso=[0.08, 1.6]),
            *ambiente_cueva(d, sem=2, oscura=True, primer_plano="rocas_primer_plano_a")],
            cam(1.45, 1.0, (540, 1150)), "corte",
            sfx=[(0.1, "rumor", -26, {"dur": 2.5})])

    @plano(25, "un día, alguien baja a buscarte")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_galeria"),
            *flip(["equipo_frontal_a", "equipo_frontal_b"], d, fps=3, base=lambda n: pie(n, 540, 1360, 330, z=0.5,
                  keys=K(d, (0, {"escala": 0.65, "y": 1250}), (1, {"escala": 1.05, "y": 1330, "ease": "suave"})))),
            brillo(560, 1120, 300, "#fff1c8", 0.4, 0.4, pulso=[0.12, 0.5]),
            *ambiente_cueva(d, sem=3, gotas=True)],
            cam(1.0, 1.12, (540, 1100)), "desenfoque",
            sfx=[(0.1, "golpe", -28), (0.6, "golpe", -29), (1.1, "golpe", -28)])

    @plano(32, "te dice que ya está")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento"),
            pie("colchon", 640, 1300, 160, z=0.45),
            pie("bea_lee_b", 650, 1290, 320, z=0.5, keys=late(0.3, 1, 0.04)),
            pie("equipo_frontal_a", 230, 1300, 340, z=0.55),
            pie("libro_c", 860, 1300, 60, z=0.52), pie("libro_a", 860, 1260, 60, z=0.53),
            pie("mesa_campamento", -250, 1300, 260, z=0.5), pie("garrafa_agua", 1300, 1300, 160, z=0.5),
            *ambiente_cueva(d, sem=4)],
            cam(1.0, 1.08, (540, 1150), (600, 1150)), "corte")

    @plano(42, "tú no lo entiendes")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento"),
            pieza("bea_cara_sorpresa", 540, 980, 980, z=0.6, keys=K(d, (0, {"escala": 0.96}), (1, {"escala": 1.04}))),
            brillo(380, 700, 300, "#ffcf8a", 0.35, 0.65)],
            cam(1.0, 1.15, (540, 900)), "corte", sfx=[(0.05, "golpe", -20)])

    @plano(46, "según tus cuentas: rayas en la pared")
    def _(d):
        rayas = [tiza(330 + 44 * i + (14 if i % 5 == 4 else 0), 760, 0.04 + 0.06 * i, 170) for i in range(10)]
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"), brillo(540, 760, 420, "#ffcf8a", 0.35, 0.3),
            IMG("moho_pared", ancho=420, x=820, y=640, z=0.32, op=0.6), *rayas,
            *[tiza(-420 + 44 * i, 740, 0.06 * i, 150) for i in range(7)], *[tiza(1180 + 44 * i, 720, 0.05 * i, 160) for i in range(8)],
            pie("bea_marca_b", 240, 1300, 640, z=0.6, keys=K(d, (0, {"x": 200}), (1, {"x": 230})))],
            cam(1.25, 1.12, (520, 900)), "corte", sfx=[(0.05 + 0.06 * i, "tic", -25) for i in range(0, 10, 2)])

    @plano(49, "cinco meses y medio")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            pie("cifra_marco", 540, 1150, 400, z=0.5, keys=aparece(0.05)),
            *ambiente_cueva(d, sem=5)],
            cam(1.0, 1.06, (540, 1000)), "corte",
            hud=[contador(0.2, d - 0.05, 0, 5.5, d * 0.6, " meses", decimales=1, tam=110, x=540, y=960, color="#ffd23f", capsula=None)],
            sfx=[(0.2, "tictac", -26, {"dur": d * 0.55, "ritmo": 0.09})])

    @plano(57, "llevas casi un año y medio")
    def _(d):
        return P(["#3d2a1f", "#0b0705"], [
            fondo("bg_cueva_campamento"),
            pieza("calendario_diciembre", 540, 950, 520, z=0.55, keys=K(d, (0, {"rot": -4}), (1, {"rot": 3}))),
            fundido_blanco([{"t": 0, "op": 0.85}, {"t": 0.5, "op": 0.0}]),
            *ambiente_cueva(d, sem=6)],
            cam(1.0, 1.2, (540, 950)), "corte",
            hud=[rotulo(0.15, d - 0.05, "500 DÍAS", tam=150, color="#ffffff", capsula="#c0392be6", y=1300)],
            sfx=[(0.0, "impacto", -12)])

    # ================================================================== a partir de aquí: palabra 63 en adelante
    @plano(63, "tu cerebro")
    def _(d):
        rec = [("recuerdo_1", 190, 640, -12), ("recuerdo_4", 890, 600, 10), ("recuerdo_3", 170, 1250, 8), ("recuerdo_7", 900, 1280, -9),
               ("recuerdo_5", -330, 760, 6), ("recuerdo_6", 1420, 820, -7), ("recuerdo_8", -520, 1180, -10), ("recuerdo_2", 1600, 1150, 9)]
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_cerebro"),
            brillo(540, 940, 520, MAGENTA, 0.35, 0.2, pulso=[0.15, 0.8]),
            *[pieza(n, x, y, 190, z=0.4, keys=[{"t": 0, "rot": r, "escala": 0.0, "op": 0}, {"t": 0.12 + 0.05 * k, "escala": 1.0, "op": 1, "ease": "rebote"},
                                                 {"t": d, "rot": -r, "y": y - 40}]) for k, (n, x, y, r) in enumerate(rec)],
            pieza("cerebro", 540, 940, 660, z=0.6, keys=arranque(540, 940, d, "abajo", 220, 20)),
            pieza("cerebro_brillo", 540, 940, 660, z=0.61, keys=[{"t": 0, "op": 0, "x": 540, "y": 1160}, {"t": 0.4, "y": 940, "ease": "elastico"},
                                                                 {"t": 0.45, "op": 0}, {"t": 0.75, "op": 1}, {"t": d, "y": 920, "escala": 1.06}]),
            estrellas(40, 63)],
            cam(1.0, 1.1, (540, 940)), "corte", sfx=[(0.05, "brillo", -22), (0.5, "burbuja", -26)])

    @plano(67, "acaba de perder un año entero de tu vida: los recuerdos se caen de la cabeza")
    def _(d):
        o = rel(67)
        r = random.Random(67)
        rec = ["recuerdo_1", "recuerdo_3", "recuerdo_5", "recuerdo_8", "recuerdo_4", "recuerdo_6", "recuerdo_7"]
        els = []
        for k, n in enumerate(rec):
            x0, y0 = 480 + r.uniform(-130, 130), 640 + r.uniform(-110, 90)
            t0 = 0.08 + 0.17 * k
            x1 = x0 + r.uniform(-260, 260)
            els.append(pieza(n, round(x0), round(y0), 150, z=0.5 + 0.01 * k, keys=[
                {"t": 0, "op": 0, "escala": 0.0}, {"t": t0 * 0.5, "op": 1, "escala": 1.0, "ease": "rebote"},
                {"t": t0 + 0.25, "y": round(y0), "x": round(x0), "rot": 0}, {"t": t0 + 1.1, "y": 1520, "x": round(x1), "rot": r.uniform(-60, 60), "escala": 0.7, "ease": "entrada"},
                {"t": t0 + 1.0, "op": 1}, {"t": t0 + 1.15, "op": 0}]))
        # el último y grande: «un año entero» (la tarta de cumpleaños) se apaga
        t2 = o(70)
        els.append(pieza("recuerdo_2", 480, 670, 300, z=0.62, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": t2, "op": 0, "escala": 0.2},
                                                                   {"t": t2 + 0.25, "op": 1, "escala": 1.0, "ease": "rebote"},
                                                                   {"t": d - 0.45, "op": 1, "rot": 0, "y": 670}, {"t": d, "op": 0.0, "rot": -14, "y": 900, "escala": 0.6, "ease": "entrada"}]))
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_seccion_cabeza"),
            brillo(480, 675, 300, "#ffcf8a", 0.5, 0.3, keys=K(d, (0, {"op": 1}), (1, {"op": 0.15}))),
            *els,
            *[pieza(n, x, y, 150, z=0.3, op=0.5, keys=K(d, (0, {"y": y}), (1, {"y": y + 260, "op": 0}))) for n, x, y in
              [("recuerdo_3", -380, 700), ("recuerdo_8", 1450, 760), ("recuerdo_1", -620, 1100), ("recuerdo_5", 1650, 1060)]],
            estrellas(30, 67)],
            cam(1.0, 1.12, (500, 760)), "corte",
            sfx=[(0.3, "roce", -27), (0.8, "roce", -28), (1.3, "roce", -27), (o(70) + 0.05, "zap", -24)])

    @plano(74, "y no es ciencia ficción: el periódico")
    def _(d):
        return P(["#141018", "#050507"], [
            fondo("bg_negro_cueva"),
            brillo(540, 940, 520, "#ffcf8a", 0.55, 0.2, pulso=[0.1, 0.9]),
            pieza("periodico", 540, 940, 640, z=0.6, keys=[{"t": 0, "escala": 0.05, "rot": -700, "op": 0}, {"t": 0.04, "op": 1},
                                                           {"t": 0.55, "escala": 1.0, "rot": -6, "ease": "salida"}, {"t": d, "escala": 1.08, "rot": -3}]),
            pieza("periodico", -330, 860, 460, z=0.4, rot=14, op=0.55, keys=K(d, (0, {"rot": 18}), (1, {"rot": 10}))),
            pieza("periodico", 1430, 1020, 460, z=0.4, rot=-12, op=0.55, keys=K(d, (0, {"rot": -16}), (1, {"rot": -8}))),
            pieza("destello", 760, 760, 300, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.6, "op": 0, "escala": 0.2},
                                                           {"t": 0.72, "op": 1, "escala": 1.0, "ease": "salida"}, {"t": 1.1, "op": 0}]),
            *techo(74)],
            cam(1.0, 1.1, (540, 940)), "corte", sfx=[(0.0, "whoosh", -22), (0.55, "golpe", -20), (0.7, "brillo", -24)])

    @plano(79, "le pasó a una española")
    def _(d):
        sa = 1330
        return P(["#6fb6e8", "#c9a26b"], [
            fondo("bg_entrada_dia"),
            brillo(590, 1050, 220, "#ffcf8a", 0.4, 0.2, pulso=[0.1, 1.0]),
            *flip(["bea_camina_a", "bea_camina_b"], d, fps=4, base=lambda n: pie(n, 300, sa, 330, z=0.6,
                  keys=[pos(n, 290, sa, 330), {**pos(n, 520, sa - 120, 330, 0.75), "t": d}])),
            pie("voluntario_1", -260, 1370, 520, z=0.55), pie("voluntario_3", -520, 1370, 500, z=0.55),
            pie("mochila", -120, 1370, 160, z=0.56),
            {**polvo("#fff3d6", 26, (0, 900, 1080, 1400), 79), "_ancho": True}],
            cam(1.0, 1.18, (560, 1150), (590, 1080)), "corte", sfx=[(0.2, "roce", -28), (0.7, "roce", -28)])

    @plano(85, "en dos mil veintitrés: la salida a la luz")
    def _(d):
        return P(["#f5efe0", "#2a1d14"], [
            fondo("bg_salida_luz"),
            brillo(540, 820, 520, "#fff6e0", 0.7, 0.2, pulso=[0.12, 0.7]),
            *flip(["bea_camina_a", "bea_camina_b"], d, fps=4, base=lambda n: pie(n, 380, 1340, 420, z=0.6, op=0.92,
                  keys=[pos(n, 360, 1340, 420), {**pos(n, 600, 1300, 420, 0.85), "t": d}])),
            pieza("rayo_sol", 400, 1000, 900, z=0.65, rot=28, op=0.5, keys=K(d, (0, {"op": 0.2}), (1, {"op": 0.6}))),
            *lados(1340, 85),
            {**polvo("#fff6e0", 40, (100, 600, 980, 1400), 85), "_ancho": True}],
            cam(1.0, 1.12, (540, 950)), "corte",
            hud=[contador(0.05, d - 0.05, 2000, 2023, 0.7, "", tam=150, x=540, y=520, color="#ffd23f", capsula="#0b0f1ed8", miles=False)],
            sfx=[(0.75, "ding", -22)])

    @plano(88, "todo quedó registrado por científicos: la cámara graba")
    def _(d):
        o = rel(88)
        cw, ch = tam_svg("camara_tripode")
        alto = 640
        ancho = alto * cw / ch
        cx, top = 330, 1300 - comun.APOYO["camara_tripode"] * alto
        px, py = cx + (0.343 - 0.5) * ancho, top + 0.2 * alto
        t9 = o(93)
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            pie("bea_lee_b", 760, 1300, 230, z=0.4), pie("lampara_led", 880, 1300, 90, z=0.41),
            brillo(860, 1240, 180, "#ffcf8a", 0.5, 0.39, pulso=[0.1, 1.4]),
            flecha([[px - 20, py + 10], [700, 1150]], 0.2, 0.7, "#ff5a5a88", 5, [14, 12], punta=False, z=0.55),
            pie("camara_tripode", cx, 1300, alto, z=0.6, keys=arranque(cx, round(1300 - (0.95 - 0.5) * alto), d, "izquierda", 200, 20)),
            {**IMG("piloto_rojo", ancho=60, x=round(px), y=round(py), z=0.61), "anim": {"parpadeo": [0.1, 0.5]},
             "keys": arranque(round(px), round(py), d, "izquierda", 200, 20)},
            pieza("pantalla_ordenador", 780, 640, 380, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": t9, "op": 0, "escala": 0},
                                                                    {"t": t9 + 0.05, "op": 1}, {"t": t9 + 0.35, "escala": 1.0, "ease": "elastico"},
                                                                    {"t": d, "escala": 1.04}]),
            pie("camara_tripode", 1400, 1300, 520, z=0.5, ex=-1), pie("mesa_campamento", -300, 1300, 300, z=0.5),
            pie("garrafa_agua", -560, 1300, 170, z=0.5),
            *ambiente_cueva(d, sem=88)],
            cam(1.0, 1.1, (480, 1000), (560, 950)), "corte",
            sfx=[(0.1, "senal", -26), (t9 + 0.05, "pop", -22)])

    @plano(94, "lo inquietante: la luz del frontal barre la oscuridad")
    def _(d):
        return P(["#0c0a0c", "#030304"], [
            fondo("bg_negro_cueva"),
            pieza("haz_frontal", 330, 900, 1100, z=0.5, op=0.8, keys=K(d, (0, {"rot": -28}), (0.6, {"rot": 12}), (1, {"rot": 4}))),
            brillo(560, 880, 260, "#fff1c8", 0.4, 0.45, keys=K(d, (0, {"x": 460, "y": 560}), (0.6, {"x": 760, "y": 1000}), (1, {"x": 720, "y": 940}))),
            pie("estalagmita_b", 820, 1344, 380, z=0.55), pie("estalagmita_a", 220, 1344, 300, z=0.55),
            *lados(1344, 94),
            *ambiente_cueva(d, sem=94, oscura=True)],
            cam(1.05, 1.18, (540, 960), (600, 980)), "corte", sfx=[(0.1, "rumor", -24, {"dur": 1.3})])

    @plano(99, "a ti te pasaría exactamente lo mismo: tú entrando en la cueva")
    def _(d):
        n, a = "adulto_camina", 560
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_galeria"),
            pie(n, 760, 1480, a, z=0.6, keys=[pos(n, 780, 1480, a, 1.0), {**pos(n, 560, 1190, a, 0.42), "t": d, "ease": "suave"}]),
            brillo(560, 1100, 240, "#bfe0ff", 0.4, 0.55, keys=K(d, (0, {"x": 720, "y": 1080}), (1, {"x": 560, "y": 1110}))),
            negro(K(d, (0, {"op": 0}), (0.55, {"op": 0}), (1, {"op": 0.55, "ease": "entrada"}))),
            *lados(1360, 99),
            *ambiente_cueva(d, sem=99)],
            cam(1.0, 1.15, (580, 1100), (560, 1050)), "corte",
            sfx=[(0.2 + 0.45 * k, "golpe", -30) for k in range(5)])

    @plano(105, "porque tu cerebro tiene un secreto")
    def _(d):
        o = rel(105)
        ts = o(110)
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_seccion_cabeza"),
            brillo(480, 675, 300, CIAN, 0.3, 0.3, pulso=[0.15, 0.9]),
            pieza("cerebro", 480, 680, 380, z=0.5, keys=aparece(0.05, 0.45) + [{"t": d, "escala": 1.05}]),
            pieza("cerebro_brillo", 480, 680, 380, z=0.51, keys=[{"t": 0, "op": 0}, {"t": ts, "op": 0}, {"t": ts + 0.12, "op": 1},
                                                                 {"t": ts + 0.5, "op": 0.5}, {"t": ts + 0.8, "op": 1}, {"t": d, "op": 0.7, "escala": 1.05}]),
            senala(480, 680, ts, d - 0.1, 260, MAGENTA),
            *[onda(480, 680, ts + 0.15 + 0.3 * k, 380, CIAN, 0.9, 4) for k in range(3)],
            estrellas(40, 105)],
            cam(1.0, 1.3, (520, 800), (480, 720)), "corte",
            sfx=[(0.05, "burbuja", -26), (ts, "brillo", -20)])

    @plano(111, "no sabe medir el tiempo: la regla se cae")
    def _(d):
        o = rel(111)
        tm = o(113)
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_cerebro"),
            brillo(540, 1000, 500, MAGENTA, 0.3, 0.2),
            {**pieza("cerebro", 540, 1020, 700, z=0.5, keys=arranque(540, 1020, d, "abajo", 120, 10)), "anim": {"balanceo": [4, 0.9]}},
            pieza("regla", 540, 680, 620, z=0.6, keys=[{"t": 0, "x": 1400, "y": 640, "rot": 0, "op": 1}, {"t": tm, "x": 1400, "y": 640},
                                                       {"t": tm + 0.35, "x": 540, "y": 680, "ease": "anticipa"},
                                                       {"t": tm + 0.6, "rot": 0, "y": 680}, {"t": tm + 0.85, "rot": 28, "y": 720, "ease": "salida"},
                                                       {"t": d, "rot": 70, "y": 1600, "x": 640, "ease": "entrada"}]),
            *[pieza("recuerdo_%d" % n, x, y, 160, z=0.3, op=0.55, keys=K(d, (0, {"rot": -8}), (1, {"rot": 8}))) for n, x, y in
              [(1, -380, 760), (6, 1460, 1180), (8, -560, 1250), (3, 1640, 700)]],
            estrellas(40, 111)],
            cam(1.0, 1.08, (540, 960)), "corte",
            hud=[amarillo(0.15, d - 0.05, "?", y=560, tam=230, color=AMBAR, x=230)],
            sfx=[(tm + 0.3, "tic", -22), (tm + 0.8, "roce", -24), (d - 0.15, "golpe", -24)])

    @plano(116, "y cuando entiendas por qué: las neuronas se encienden")
    def _(d):
        pts = [[140, 1580], [300, 1220], [180, 830], [420, 560], [760, 470], [900, 820], [620, 1000]]
        tr = [flecha([pts[k], pts[k + 1]], 0.05 + 0.17 * k, 0.22 + 0.17 * k, CIAN if k % 2 else MAGENTA, 7, punta=False, z=0.5) for k in range(len(pts) - 1)]
        nodos = [brillo(x, y, 90, CIAN, 0.8, 0.52, keys=[{"t": 0, "op": 0}, {"t": 0.05 + 0.17 * k, "op": 0}, {"t": 0.12 + 0.17 * k, "op": 1}, {"t": d, "op": 0.6}])
                 for k, (x, y) in enumerate(pts)]
        return P(["#0b0f24", "#1b1340"], [
            fondo("bg_cerebro"), *tr, *nodos,
            pieza("destello", 620, 1000, 420, z=0.6, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 1.15, "op": 0, "escala": 0.1},
                                                            {"t": 1.25, "op": 1, "escala": 1.0, "ease": "salida"}, {"t": d, "op": 0.6, "escala": 1.2, "rot": 20}]),
            *[flecha([[x0, y0], [x1, y1]], 0.1 + 0.2 * k, 0.4 + 0.2 * k, MAGENTA if k % 2 else CIAN, 6, punta=False, z=0.5) for k, (x0, y0, x1, y1) in
              enumerate([(-500, 600, -200, 900), (1300, 1300, 1600, 900), (-200, 900, -560, 1300), (1600, 900, 1300, 520)])],
            estrellas(50, 116)],
            cam(1.15, 1.0, (500, 900), (560, 960)), "corte",
            sfx=[(0.05 + 0.17 * k, "trazo", -28, {"f": 900 + 90 * k}) for k in range(0, 6, 2)] + [(1.2, "brillo", -22)])

    @plano(121, "vas a entender también: la línea de tu vida")
    def _(d):
        rec = ["recuerdo_8", "recuerdo_3", "recuerdo_1", "recuerdo_7", "recuerdo_6"]
        xs = [150, 345, 540, 735, 930]
        return P(["#5a3d2a", "#2b1a12"], [
            fondo("bg_ventana_invierno"),
            brillo(540, 1150, 520, "#ffcf8a", 0.4, 0.2),
            flecha([[-600, 1340], [1680, 1340]], 0.0, 1.2, CIAN, 8, z=0.45),
            *[pieza(n, x, 1150 + (20 if k % 2 else -20), 175, z=0.5, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.1 + 0.18 * k, "op": 0, "escala": 0, "rot": 0},
                                                                         {"t": 0.15 + 0.18 * k, "op": 1}, {"t": 0.45 + 0.18 * k, "escala": 1.0, "rot": -5 + 4 * k, "ease": "rebote"},
                                                                         {"t": d, "rot": -3 + 3 * k}]) for k, (n, x) in enumerate(zip(rec, xs))],
            *[pieza(n, x, 1150, 160, z=0.45, op=0.85, keys=[{"t": 0, "op": 0}, {"t": t, "op": 0}, {"t": t + 0.1, "op": 0.85}]) for n, x, t in
              [("recuerdo_4", -180, 0.05), ("recuerdo_5", -420, 0.0), ("recuerdo_2", 1260, 1.0), ("recuerdo_cueva", 1500, 1.2)]],
            *[{"tipo": "forma", "forma": "circulo", "radio": 12, "relleno": CIAN, "x": x, "y": 1340, "z": 0.46, "keys": aparece(0.1 + 0.18 * k, 0.3)}
              for k, x in enumerate(xs)]],
            cam(1.0, 1.08, (540, 1150), (600, 1150)), "corte",
            sfx=[(0.15 + 0.18 * k, "pop", -26) for k in range(5)])

    def hojas_calendario(d, x, y, ancho, tiempos, z=0.6, sem=1):
        """Hojas que se despegan del taco y salen volando, una en cada tiempo de `tiempos`."""
        r = random.Random(sem)
        out = []
        for k, t in enumerate(tiempos):
            dx = r.uniform(500, 900) * (1 if k % 2 else -1)
            out.append(pieza("calendario_hoja", x, y, ancho, z=z + 0.002 * k, keys=[
                {"t": 0, "op": 1, "x": x, "y": y, "rot": 0, "escala": 1}, {"t": t, "x": x, "y": y, "rot": 0},
                {"t": t + 0.45, "x": x + dx, "y": y - r.uniform(600, 900), "rot": r.uniform(120, 300) * (1 if dx > 0 else -1), "escala": 0.6, "ease": "entrada"},
                {"t": t + 0.4, "op": 1}, {"t": t + 0.46, "op": 0}]))
        return out

    @plano(127, "cada año de tu vida: el taco de calendario")
    def _(d):
        ts = [0.15, 0.6, 0.98]
        return P(["#5a3d2a", "#2b1a12"], [
            fondo("bg_ventana_invierno"),
            brillo(540, 960, 460, "#ffd59a", 0.45, 0.2),
            pie("calendario_taco", 540, 1240, 560, z=0.55),
            *hojas_calendario(d, 540, round(1240 - 0.46 * 560), 460, ts, sem=127),
            pieza("hoja_otono", -300, 700, 140, z=0.5, keys=K(d, (0, {"y": 600, "rot": 0}), (1, {"y": 1000, "rot": 90}))),
            pieza("copo_nieve", 1400, 680, 120, z=0.5, keys=K(d, (0, {"y": 560, "rot": 0}), (1, {"y": 960, "rot": 60}))),
            pie("taza_cafe", -500, 1480, 200, z=0.5), pie("libro_b", 1500, 1480, 90, z=0.5)],
            cam(1.0, 1.08, (540, 980)), "corte",
            sfx=[(t + 0.05, "roce", -25) for t in ts])

    @plano(132, "pasa más rápido que el anterior: estaciones y hojas en ráfaga")
    def _(d):
        ts, t, paso = [], 0.05, 0.3
        while t < d - 0.2:
            ts.append(round(t, 3)); t += paso; paso = max(0.06, paso * 0.72)
        r = random.Random(132)
        est = ["hoja_otono", "copo_nieve", "flor_primavera", "sol_verano"]
        cruces = []
        for k in range(16):
            n = est[k % 4]
            t0 = 0.1 + k * (d - 0.4) / 16 * (1 - 0.3 * k / 16)
            y = r.uniform(480, 1380)
            izq = k % 2 == 0
            cruces.append(pieza(n, -700 if izq else 1780, round(y), round(r.uniform(150, 230)), z=0.7, keys=[
                {"t": 0, "op": 0}, {"t": t0, "op": 1, "x": -700 if izq else 1780, "rot": 0},
                {"t": t0 + max(0.25, 0.6 - 0.025 * k), "x": 1780 if izq else -700, "y": round(y + r.uniform(-200, 200)), "rot": 360 if izq else -360, "ease": "lineal"}]))
            cruces[-1]["_ancho"] = True
        return P(["#5a3d2a", "#2b1a12"], [
            fondo("bg_ventana_invierno"),
            brillo(540, 900, 520, "#ffd59a", 0.45, 0.2, pulso=[0.2, 0.4]),
            pie("calendario_taco", 540, 1300, 720, z=0.55),
            *hojas_calendario(d, 540, round(1300 - 0.46 * 720), round(720 * 460 / 560), ts, sem=132),
            *cruces],
            cam(1.0, 1.25, (540, 960), (540, 920), temblor=3), "corte",
            sfx=[(t, "roce", -27) for t in ts[::2]] + [(0.2, "whoosh", -26)])

    @plano(138, "primer día: la mochila cae en la entrada")
    def _(d):
        return P(["#f7a85c", "#5a3d2a"], [
            fondo("bg_entrada_atardecer"),
            brillo(200, 420, 300, "#ffd59a", 0.5, 0.15, pulso=[0.08, 1.2]),
            cae_vela("mochila", 420, 1390, 300, 0.05, 0.5, z=0.6),
            pie("mosqueton", 820, 1390, 90, z=0.56, keys=aparece(0.4)),
            pie("garrafa_agua", -260, 1370, 200, z=0.5), pie("caja_comida", -560, 1370, 200, z=0.5),
            pie("voluntario_4", -860, 1370, 520, z=0.5),
            {**polvo("#ffd9a0", 26, (0, 1100, 1080, 1450), 138), "_ancho": True}],
            cam(1.08, 1.0, (500, 1200), (560, 1150)), "corte",
            hud=[rotulo(0.15, d - 0.05, "DÍA 1", tam=120, color="#ffffff", capsula="#c0392be6", x=540, y=620)],
            sfx=[(0.35, "golpe", -18)])

    @plano(140, "te despides de los tuyos: el abrazo")
    def _(d):
        return P(["#f7a85c", "#5a3d2a"], [
            fondo("bg_entrada_atardecer"),
            brillo(300, 640, 460, "#ffd59a", 0.45, 0.15, pulso=[0.08, 1.0]),
            pie("bea_abraza", 540, 1400, 980, z=0.6, keys=[{"t": 0, "rot": -2, "escala": 0.97}, {"t": d * 0.5, "rot": 1.5, "escala": 1.0}, {"t": d, "rot": 0, "escala": 1.02}]),
            pie("voluntario_2", -250, 1400, 780, z=0.5), pie("voluntario_6", -560, 1400, 760, z=0.5),
            pie("voluntario_5", 1350, 1400, 780, z=0.5, ex=-1),
            {**polvo("#ffd9a0", 24, (0, 600, 1080, 1400), 140), "_ancho": True}],
            cam(1.0, 1.1, (540, 900)), "corte", sfx=[(0.1, "roce", -26)])

    @plano(145, "en la entrada: ella saluda desde la boca de la cueva")
    def _(d):
        return P(["#f7a85c", "#5a3d2a"], [
            fondo("bg_entrada_atardecer"),
            brillo(590, 1060, 200, "#ffcf8a", 0.5, 0.2),
            pie("bea_despide", 600, 1170, 250, z=0.45, keys=[{"t": 0, "rot": -3}, {"t": d * 0.33, "rot": 3}, {"t": d * 0.66, "rot": -3}, {"t": d, "rot": 2}]),
            pie("voluntario_5", 250, 1520, 640, z=0.65, keys=[{"t": 0, "x": 230}, {"t": d, "x": 260}]),
            pie("voluntario_1", -220, 1450, 560, z=0.6), pie("voluntario_3", -520, 1450, 540, z=0.6)],
            cam(1.12, 1.0, (560, 1150)), "corte")

    @plano(148, "y empiezas a bajar: se pierde pozo abajo")
    def _(d):
        n, a = "bea_baja_cuerda", 760
        return P(["#0d0b0a", "#030304"], [
            fondo("bg_cueva_pozo"),
            brillo(540, 430, 300, "#fff3d6", 0.55, 0.1, pulso=[0.1, 1.0]),
            pieza("cuerda", 552, 600, 26, z=0.55),
            pieza(n, 540, 700, round(a * 820 / 1500), z=0.6, keys=[{"t": 0, "x": 545, "y": 760, "escala": 0.55, "rot": 0},
                                                                    {"t": d, "x": 560, "y": 1200, "escala": 0.2, "rot": 6, "ease": "suave"}]),
            brillo(600, 600, 140, "#ffe2a8", 0.6, 0.62, keys=[{"t": 0, "y": 420, "x": 600}, {"t": d, "y": 1080, "x": 580, "ease": "suave"}]),
            {**polvo("#fff3d6", 36, (300, 420, 780, 1500), 148), "vel": [4, 40]},
            IMG("estalactita_a", ancho=160, x=-300, y=480, z=0.8), IMG("estalactita_c", ancho=200, x=1380, y=460, z=0.8),
            IMG("estalactita_b", ancho=120, x=-620, y=420, z=0.8), IMG("estalactita_b", ancho=130, x=1700, y=430, z=0.8)],
            cam(1.0, 1.1, (540, 800), (560, 1000)), "corte",
            sfx=[(0.1, "roce", -24), (0.8, "roce", -26)])

    @plano(152, "las reglas son sencillas: el cuaderno de reglas")
    def _(d):
        y = 960
        lineas = [flecha([[340, y - 90 + 70 * k], [500 - 30 * (k == 2), y - 90 + 70 * k]], 0.5 + 0.18 * k, 0.65 + 0.18 * k, "#3d2a1f", 7, punta=False, z=0.62)
                  for k in range(3)]
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            brillo(540, 940, 420, "#ffcf8a", 0.5, 0.3),
            pieza("libro_abierto", 540, y, 680, z=0.6, keys=[{"t": 0, "y": 420, "op": 0}, {"t": 0.02, "op": 1}] + cae(0.02, 0.4, 420, y)[1:]),
            *lineas,
            *[{"tipo": "forma", "forma": "circulo", "radio": 9, "relleno": "#c0392b", "x": 320, "y": y - 90 + 70 * k, "z": 0.62, "keys": aparece(0.5 + 0.18 * k, 0.25)} for k in range(3)],
            pie("lampara_led", -260, 1300, 160, z=0.5), pie("libro_d", 1350, 1300, 70, z=0.5), pie("libro_a", 1350, 1262, 70, z=0.5),
            *ambiente_cueva(d, sem=152)],
            cam(1.0, 1.1, (540, 960)), "corte",
            sfx=[(0.3, "golpe", -20)])

    @plano(156, "y brutales: la luz de arriba se cierra")
    def _(d):
        return P(["#0d0b0a", "#030304"], [
            fondo("bg_cueva_pozo"),
            brillo(540, 430, 420, "#fff3d6", 0.8, 0.12, keys=[{"t": 0, "op": 1, "radio": 420}, {"t": d * 0.75, "op": 0.0, "ease": "entrada"}]),
            {**polvo("#fff3d6", 40, (200, 300, 880, 1500), 156), "vel": [4, 90]},
            negro([{"t": 0, "op": 0}, {"t": d * 0.35, "op": 0}, {"t": d * 0.85, "op": 0.85, "ease": "entrada"}]),
            IMG("estalactita_c", ancho=220, x=-260, y=440, z=0.8), IMG("estalactita_a", ancho=170, x=1360, y=420, z=0.8)],
            cam(1.0, 1.25, (540, 600), (540, 520), temblor=2), "corte",
            sfx=[(d * 0.7, "golpe", -16), (0.05, "rumor", -24)])

    @plano(158, "nadie va a hablar contigo: habla y el sonido se pierde")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            brillo(540, 1050, 380, "#ffcf8a", 0.4, 0.3, pulso=[0.1, 1.2]),
            *flip(["bea_habla_a", "bea_habla_b"], d, fps=5, base=lambda n: pie(n, 470, 1300, 560, z=0.55)),
            *[onda(620, 820, 0.15 + 0.35 * k, 220 + 30 * k, CIAN, 0.9, 5, z=0.6) for k in range(5)],
            pie("lampara_led", 820, 1300, 130, z=0.5, op=0.9),
            pie("mochila", -300, 1300, 220, z=0.5), pie("colchon", 1420, 1300, 150, z=0.5),
            *ambiente_cueva(d, sem=158, oscura=True)],
            cam(1.1, 1.0, (520, 1000), (540, 1050)), "corte",
            sfx=[(0.2, "senal", -28), (1.0, "senal", -32)])

    @plano(163, "nadie te va a decir: ella escucha y no llega nada")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_galeria"),
            brillo(560, 1000, 300, "#ffcf8a", 0.35, 0.3),
            pie("bea_oye", 520, 1360, 760, z=0.6, keys=arranque(520, round(1360 - 0.47 * 760), d, "derecha", 140, 15)),
            *[onda(1000 - 0 * k, 640, 0.1 + 0.3 * k, 120, "#ffffff", 0.7, 4, z=0.4) for k in range(3)],
            *lados(1360, 163),
            *ambiente_cueva(d, sem=163)],
            cam(1.0, 1.1, (520, 900)), "corte")

    @plano(168, "qué hora es, qué día es: sol y luna, el calendario en blanco")
    def _(d):
        o = rel(168)
        t2 = o(171)
        return P(["#141018", "#050507"], [
            fondo("bg_negro_cueva"),
            pieza("sol_dibujo", 540, 860, 380, z=0.55, keys=[{"t": 0, "x": 200, "y": 1150, "op": 0, "rot": 0}, {"t": 0.08, "op": 1},
                                                              {"t": t2 * 0.5, "x": 540, "y": 760}, {"t": t2, "x": 880, "y": 1150, "op": 0, "rot": 90}]),
            pieza("luna_creciente", 540, 860, 320, z=0.54, keys=[{"t": 0, "x": 880, "y": 1200, "op": 0}, {"t": t2 * 0.35, "op": 0, "x": 880, "y": 1200},
                                                                  {"t": t2 * 0.5, "op": 1}, {"t": t2 * 0.85, "x": 540, "y": 800}, {"t": t2, "x": 300, "y": 1100, "op": 0}]),
            pieza("calendario_hoja", 540, 960, 480, z=0.6, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": t2, "op": 0, "escala": 0.2, "rot": -20},
                                                                  {"t": t2 + 0.3, "op": 1, "escala": 1.0, "rot": 0, "ease": "rebote"}, {"t": d - 0.3, "rot": 0},
                                                                  {"t": d, "rot": 5}]),
            brillo(540, 900, 420, "#ffcf8a", 0.4, 0.2),
            pieza("sol_dibujo", -380, 820, 200, z=0.4, op=0.55, keys=K(d, (0, {"rot": 0}), (1, {"rot": 40}))),
            pieza("luna_creciente", 1460, 860, 180, z=0.4, op=0.55, keys=K(d, (0, {"y": 900}), (1, {"y": 820}))),
            *techo(168, oscura=True),
            estrellas(30, 168)],
            cam(1.0, 1.08, (540, 940)), "corte",
            hud=[amarillo(0.15, t2 - 0.05, "?", y=620, tam=200, color=CIAN, x=760),
                 amarillo(t2 + 0.2, d - 0.05, "?", y=980, tam=220, color=AMBAR, x=540)],
            sfx=[(0.1, "brillo", -26), (t2 + 0.05, "pop", -22)])

    @plano(174, "ni qué está pasando en el mundo: el mundo se aleja")
    def _(d):
        mics = [("microfono_a", 230, 760, -20), ("microfono_b", 860, 720, 18), ("microfono_c", 820, 1250, 30)]
        return P(["#0b0f24", "#050507"], [
            fondo("bg_negro_cueva"),
            brillo(540, 960, 460, "#9fc4ff", 0.45, 0.2, keys=K(d, (0, {"op": 1}), (1, {"op": 0.3}))),
            {**pieza("foto_mundo", 540, 980, 560, z=0.55, keys=[{"t": 0, "escala": 1.0, "op": 1}, {"t": d * 0.5, "escala": 0.95},
                                                                {"t": d, "escala": 0.35, "op": 0.25, "y": 900, "ease": "entrada"}]), "anim": {"girar": 25}},
            *[pieza(n, x, y, 120, z=0.6, rot=r, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.15 + 0.15 * k, "op": 1, "escala": 1.0, "ease": "rebote"},
                                                     {"t": d * 0.55, "op": 1, "x": x, "y": y}, {"t": d, "op": 0, "x": 540, "y": 960, "escala": 0.3, "ease": "entrada"}])
              for k, (n, x, y, r) in enumerate(mics)],
            pieza("periodico", -360, 900, 380, z=0.4, rot=10, op=0.45), pieza("pantalla_ordenador", 1420, 960, 380, z=0.4, op=0.45),
            *techo(174, oscura=True), estrellas(30, 174)],
            cam(1.0, 1.05, (540, 960)), "corte",
            sfx=[(0.15 + 0.15 * k, "pop", -28) for k in range(3)] + [(d * 0.6, "whoosh", -26)])

    @plano(181, "un equipo dejará comida en un punto de la cueva")
    def _(d):
        o = rel(181)
        tc, tp = o(184), o(187)
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            *flip(["equipo_frontal_a", "equipo_frontal_b"], d, fps=3, base=lambda n: pie(n, 200, 1300, 560, z=0.55,
                  keys=[{"t": 0, "x": 120}, {"t": d, "x": 430, "ease": "lineal"}])),
            pie("caja_comida", 700, 1300, 200, z=0.6, keys=aparece(tc, 0.45)),
            senala(700, 1225, tp, d - 0.1, 150, AMBAR),
            pie("estalagmita_b", 880, 1300, 260, z=0.5),
            *lados(1300, 181),
            *ambiente_cueva(d, sem=181)],
            cam(1.0, 1.12, (480, 1120), (640, 1150)), "corte",
            sfx=[(0.1, "golpe", -29), (0.55, "golpe", -29), (tc + 0.05, "golpe", -18)])

    @plano(191, "y se llevará tu basura")
    def _(d):
        n, a = "bolsa_basura", 460
        yb = pos(n, 540, 1300, a)["y"]
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            pieza("haz_frontal", 980, 1000, 900, z=0.45, ex=-1, op=0.6, keys=K(d, (0, {"rot": 10}), (1, {"rot": -6}))),
            pie(n, 540, 1300, a, z=0.6, keys=[{"t": 0, "y": yb, "rot": 0, "ey": 1.0}, {"t": 0.35, "ey": 0.94, "ease": "salida"},
                                              {"t": 0.5, "ey": 1.08, "y": yb - 30, "rot": -4},
                                              {"t": d, "y": -300, "x": 760, "rot": 12, "ease": "anticipa"}]),
            pie("caja_comida", 220, 1300, 170, z=0.55, op=0.95),
            *lados(1300, 191),
            *ambiente_cueva(d, sem=191)],
            cam(1.15, 1.05, (540, 1100)), "corte",
            sfx=[(0.4, "roce", -22), (0.9, "whoosh", -28)])

    @plano(196, "pero nunca os cruzaréis: ellos se van, ella llega")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_galeria"),
            *flip(["equipo_frontal_a", "equipo_frontal_b"], d, fps=3, base=lambda n: pie(n, 760, 1360, 440, z=0.5,
                  keys=[{"t": 0, "x": 620}, {"t": d, "x": 1400, "ease": "lineal"}])),
            *flip(["bea_camina_a", "bea_camina_b"], d, fps=3.5, base=lambda n: pie(n, 0, 1380, 440, z=0.55,
                  keys=[{"t": 0, "x": -450, "op": 1}, {"t": d, "x": 280, "ease": "lineal"}])),
            flecha([[540, 600], [540, 1340]], 0.2, 0.8, "#ffffff55", 5, [16, 16], punta=False, z=0.6),
            pie("caja_comida", 540, 1360, 120, z=0.48),
            *ambiente_cueva(d, sem=196)],
            cam(1.0, 1.05, (540, 1100)), "corte",
            sfx=[(0.2 + 0.5 * k, "golpe", -30) for k in range(3)])

    @plano(200, "tienes luz artificial: la lámpara se enciende")
    def _(d):
        o = rel(200)
        tl = o(201)
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            negro([{"t": 0, "op": 0.75}, {"t": tl, "op": 0.75}, {"t": tl + 0.06, "op": 0.2}, {"t": tl + 0.12, "op": 0.6}, {"t": tl + 0.2, "op": 0.0}]),
            pie("lampara_led", 540, 1250, 560, z=0.6, keys=arranque(540, round(1250 - 0.43 * 560), d, "abajo", 150, 10)),
            brillo(540, 900, 520, "#ffcf8a", 0.8, 0.59, keys=[{"t": 0, "op": 0}, {"t": tl, "op": 0}, {"t": tl + 0.06, "op": 1}, {"t": tl + 0.12, "op": 0.3},
                                                              {"t": tl + 0.2, "op": 1}]),
            pie("bea_lee_a", -330, 1300, 330, z=0.5), pie("libro_c", 1350, 1300, 70, z=0.5),
            *ambiente_cueva(d, sem=200, oscura=True)],
            cam(1.0, 1.1, (540, 950)), "corte",
            sfx=[(tl, "zap", -22), (tl + 0.15, "brillo", -24)])

    @plano(203, "libros: la pila de libros cae")
    def _(d):
        libros = ["libro_a", "libro_b", "libro_c", "libro_d", "libro_b"]
        els = []
        for k, n in enumerate(libros):
            t0 = 0.02 + 0.1 * k
            els.append(cae_vela(n, 540 + (14 if k % 2 else -12), 1300 - 62 * k, 80, t0, t0 + 0.28, z=0.6 + 0.01 * k, desde=360))
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            brillo(540, 1100, 380, "#ffcf8a", 0.45, 0.3),
            *els,
            *[pie(n, x, 1300, 80, z=0.5) for n, x in [("libro_d", -260), ("libro_a", 1340), ("libro_c", 1600)]],
            pie("libro_abierto", 840, 1300, 110, z=0.55),
            *ambiente_cueva(d, sem=203)],
            cam(1.25, 1.15, (540, 1120)), "corte",
            sfx=[(0.02 + 0.1 * k + 0.2, "golpe", -24) for k in range(0, 5, 2)])

    @plano(204, "papel: el cuaderno se desliza y el lápiz dibuja")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            brillo(540, 1000, 380, "#ffcf8a", 0.5, 0.3),
            pieza("cuaderno_dibujo", 540, 1000, 700, z=0.6, keys=[{"t": 0, "x": 1300, "rot": 8}, {"t": 0.3, "x": 540, "rot": -4, "ease": "anticipa"}, {"t": d, "rot": -2, "escala": 1.04}]),
            flecha([[430, 960], [480, 920], [530, 975], [590, 925]], 0.3, d - 0.05, "#3d2a1fcc", 6, punta=False, z=0.62),
            pie("libro_c", -300, 1300, 80, z=0.5), pie("lampara_led", 1400, 1300, 150, z=0.5),
            *techo(204)],
            cam(1.0, 1.08, (540, 1000)), "corte",
            sfx=[(0.05, "roce", -22)])

    @plano(205, "lana para tejer: el ovillo rueda")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            brillo(540, 1100, 360, "#ffcf8a", 0.45, 0.3),
            pie("ovillo_lana", 520, 1300, 300, z=0.6, keys=[{"t": 0, "x": -200, "rot": -400}, {"t": 0.6, "x": 500, "rot": 0, "ease": "salida"}, {"t": d, "x": 520, "rot": 10}]),
            pieza("agujas_tejer", 640, 1050, 440, z=0.62, keys=[{"t": 0, "op": 0, "y": 600}, {"t": 0.45, "op": 0, "y": 600}, {"t": 0.47, "op": 1},
                                                              {"t": 0.75, "y": 1120, "rot": -8, "ease": "bote"}]),
            pie("gorro_lana_b", -300, 1300, 200, z=0.5), pie("ovillo_lana", 1380, 1300, 180, z=0.5),
            *ambiente_cueva(d, sem=205)],
            cam(1.15, 1.25, (520, 1150)), "corte",
            sfx=[(0.1, "roce", -24), (0.7, "tic", -22)])

    @plano(208, "y unas: el piloto rojo, de muy cerca")
    def _(d):
        return P(["#141018", "#050507"], [
            fondo("bg_negro_cueva"),
            brillo(560, 900, 600, "#ffcf8a", 0.3, 0.1),
            # la cámara enorme, encuadrada para que el piloto quede en el centro (piloto en 0,343 × 0,2 del lienzo)
            pieza("camara_tripode", 760, 1727, 1400, z=0.55, keys=[{"t": 0, "escala": 1.0, "x": 760}, {"t": d, "escala": 1.05, "x": 740}]),
            brillo(540, 900, 260, "#ff3b3b", 0.7, 0.58, pulso=[0.4, 0.25]),
            {**pieza("piloto_rojo", 540, 900, 150, z=0.6, keys=[{"t": 0, "escala": 0.8}, {"t": d, "escala": 1.1}]), "anim": {"parpadeo": [0.2, 0.25]}},
            pieza("camara_tripode", -330, 1200, 300, z=0.5), pieza("camara_tripode", 1420, 1200, 300, z=0.5, ex=-1),
            *techo(208, oscura=True)],
            cam(1.0, 1.1, (540, 900)), "corte", sfx=[(0.02, "senal", -26)])

    @plano(210, "cámaras: tres cámaras con su piloto")
    def _(d):
        alto = 520
        cw, ch = tam_svg("camara_tripode")
        an = alto * cw / ch
        top = 1300 - comun.APOYO["camara_tripode"] * alto
        els = []
        for k, x in enumerate([200, 540, 880]):
            t0 = 0.03 + 0.12 * k
            ex = -1 if x > 540 else 1
            ox = (0.343 - 0.5) * an * ex
            els += [pie("camara_tripode", x, 1300, alto, z=0.6, ex=ex, keys=aparece(t0, 0.35)),
                    {**IMG("piloto_rojo", ancho=50, x=round(x + ox), y=round(top + 0.2 * alto), z=0.62), "anim": {"parpadeo": [0.15, 0.4 + 0.1 * k]},
                     "keys": [{"t": 0, "op": 0}, {"t": t0 + 0.2, "op": 0}, {"t": t0 + 0.25, "op": 1}]}]
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"), brillo(540, 1050, 420, "#ffcf8a", 0.4, 0.3),
            *els,
            pie("camara_tripode", -320, 1300, 440, z=0.5), pie("camara_tripode", 1400, 1300, 440, z=0.5, ex=-1),
            *ambiente_cueva(d, sem=208)],
            cam(1.0, 1.08, (540, 1050)), "corte",
            sfx=[(0.03 + 0.12 * k, "pop", -24) for k in range(3)])

    @plano(211, "para grabarte: la vista de la cámara")
    def _(d):
        marco = {"tipo": "forma", "forma": "rect", "ancho": 860, "alto": 860, "relleno": "#ffffff", "op_relleno": 0, "grosor": 6,
                 "borde": "#ffffffcc", "x": 540, "y": 1000, "z": 0.85, "keys": [{"t": 0, "escala": 1.15, "op": 0}, {"t": 0.2, "escala": 1.0, "op": 1, "ease": "salida"}]}
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            pie("colchon", 600, 1300, 150, z=0.45),
            *flip(["bea_lee_a", "bea_lee_b"], d, fps=1.6, base=lambda n: pie(n, 560, 1290, 420, z=0.5)),
            pie("lampara_led", 820, 1300, 140, z=0.5), brillo(820, 1220, 200, "#ffcf8a", 0.5, 0.49, pulso=[0.1, 1.3]),
            marco,
            {**IMG("piloto_rojo", ancho=70, x=180, y=640, z=0.86), "anim": {"parpadeo": [0.0, 0.5]}},
            pie("mesa_campamento", -300, 1300, 300, z=0.5), pie("garrafa_agua", 1380, 1300, 180, z=0.5),
            *ambiente_cueva(d, sem=211)],
            cam(1.3, 1.15, (560, 1050)), "corte",
            sfx=[(0.05, "senal", -26)])

    @plano(213, "nada más: la cueva enorme y vacía")
    def _(d):
        return P(["#3d2a1f", "#0b0705"], [
            fondo("bg_cueva_campamento"),
            pie("colchon", 560, 1300, 90, z=0.45), pie("lampara_led", 680, 1300, 70, z=0.46),
            brillo(680, 1260, 140, "#ffcf8a", 0.5, 0.45, keys=[{"t": 0, "op": 1}, {"t": d * 0.6, "op": 0.4}, {"t": d * 0.7, "op": 1}, {"t": d, "op": 0.7}]),
            pie("libro_a", 450, 1300, 40, z=0.46), pie("ovillo_lana", 500, 1300, 45, z=0.46),
            pie("camara_tripode", 380, 1300, 140, z=0.46), pie("caja_comida", 760, 1300, 60, z=0.46),
            *lados(1300, 213),
            *ambiente_cueva(d, sem=213, primer_plano="rocas_primer_plano_b")],
            cam(1.5, 1.0, (600, 1250), (540, 1000)), "corte",
            sfx=[(0.1, "rumor", -26, {"dur": 1.2})])

    @plano(215, "así empezó Beatriz Flamini")
    def _(d):
        return P(["#6fb6e8", "#c9a26b"], [
            fondo("bg_entrada_dia"),
            brillo(380, 700, 500, "#fff3d6", 0.4, 0.2, pulso=[0.08, 1.4]),
            pie("bea_despide", 560, 1380, 930, z=0.6, keys=arranque(560, round(1380 - 0.47 * 930), d, "derecha", 220, 20)),
            pie("mochila", 250, 1390, 260, z=0.62),
            pie("voluntario_4", -260, 1370, 640, z=0.5), pie("voluntario_2", -560, 1370, 620, z=0.5), pie("cuerda", -820, 1370, 400, z=0.5),
            {**polvo("#fff3d6", 26, (0, 700, 1080, 1400), 215), "_ancho": True}],
            cam(1.0, 1.1, (560, 900)), "corte",
            sfx=[(0.05, "whoosh", -26), (0.4, "brillo", -24)])

    @plano(219, "una alpinista española: el mosquetón engancha la cuerda")
    def _(d):
        return P(["#0d0b0a", "#030304"], [
            fondo("bg_cueva_pozo"),
            brillo(540, 430, 300, "#fff3d6", 0.5, 0.1, pulso=[0.1, 1.0]),
            pieza("cuerda", 520, 900, 70, z=0.55, keys=K(d, (0, {"rot": -2}), (1, {"rot": 2}))),
            pieza("mosqueton", 540, 960, 300, z=0.6, keys=[{"t": 0, "x": 1300, "y": 1150, "rot": 60}, {"t": 0.45, "x": 560, "y": 960, "rot": -8, "ease": "anticipa"},
                                                          {"t": 0.6, "rot": 4}, {"t": d, "rot": 0, "y": 940}]),
            pieza("destello", 540, 900, 220, z=0.65, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.45, "op": 0}, {"t": 0.5, "op": 1, "escala": 1.0, "ease": "salida"}, {"t": 0.85, "op": 0}]),
            {**polvo("#fff3d6", 30, (200, 420, 880, 1500), 219), "vel": [4, 40]},
            IMG("estalactita_c", ancho=200, x=-280, y=460, z=0.8), IMG("estalactita_a", ancho=160, x=1380, y=440, z=0.8),
            IMG("estalactita_b", ancho=130, x=-620, y=430, z=0.8), IMG("estalactita_b", ancho=140, x=1680, y=420, z=0.8)],
            cam(1.0, 1.12, (540, 940)), "corte",
            sfx=[(0.47, "tic", -16), (0.1, "whoosh", -28)])

    @plano(222, "en noviembre de dos mil veintiuno: hojas de otoño en la entrada")
    def _(d):
        r = random.Random(222)
        hojas = []
        for k in range(12):
            x = r.uniform(-600, 1680)
            t0 = r.uniform(-0.8, d * 0.6)
            hojas.append({**pieza("hoja_otono", round(x), 400, round(r.uniform(70, 130)), z=r.uniform(0.6, 0.8), keys=[
                {"t": 0, "y": round(400 + (0 - t0) * 420), "x": round(x), "rot": 0},
                {"t": d, "y": round(400 + (d - t0) * 420), "x": round(x + r.uniform(-160, 160)), "rot": r.uniform(-260, 260), "ease": "lineal"}]),
                "anim": {"balanceo": [20, 1.1]}})
        return P(["#6fb6e8", "#c9a26b"], [
            fondo("bg_entrada_dia"),
            brillo(590, 1050, 220, "#ffcf8a", 0.4, 0.2, pulso=[0.1, 1.0]),
            pie("bea_despide", 620, 1180, 230, z=0.45, op=0.95),
            *hojas,
            pie("voluntario_6", -300, 1370, 520, z=0.55), pie("mochila", -520, 1370, 170, z=0.55)],
            cam(1.0, 1.1, (560, 1050), (600, 1080)), "corte",
            hud=[contador(0.1, d - 0.05, 2000, 2021, 0.9, "", tam=150, x=540, y=600, color="#ffd23f", capsula="#0b0f1ed8", miles=False)],
            sfx=[(0.3, "roce", -27), (1.0, "ding", -22)])

    @plano(228, "tenía cuarenta y ocho años: primer plano de su cara")
    def _(d):
        return P(["#6fb6e8", "#c9a26b"], [
            fondo("bg_entrada_dia"),
            brillo(380, 640, 380, "#fff3d6", 0.4, 0.4, pulso=[0.1, 1.2]),
            pieza("bea_cara_neutra", 540, 860, 860, z=0.6, keys=[{"t": 0, "escala": 0.95, "x": 560}, {"t": d, "escala": 1.04, "x": 530}]),
            pieza("hoja_otono", -260, 700, 120, z=0.6, keys=K(d, (0, {"y": 600, "rot": 0}), (1, {"y": 1000, "rot": 120}))),
            pieza("hoja_otono", 1350, 640, 100, z=0.6, keys=K(d, (0, {"y": 520, "rot": 0}), (1, {"y": 940, "rot": -90})))],
            cam(1.0, 1.12, (540, 860)), "corte",
            hud=[contador(0.25, d - 0.05, 0, 48, 0.7, " años", tam=110, x=540, y=1330, color="#ffffff", capsula="#c0392be6", miles=False)],
            sfx=[(0.9, "ding", -24)])

    @plano(233, "y un objetivo: anillos que apuntan al fondo de la galería")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_galeria"),
            brillo(540, 900, 220, "#fff1c8", 0.5, 0.2, pulso=[0.15, 0.5]),
            *[senala(540, 900, 0.1 + 0.2 * k, d - 0.05, 300 - 80 * k, AMBAR if k != 1 else ROJO, z=0.7) for k in range(3)],
            pieza("destello", 540, 900, 200, z=0.72, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.7, "op": 0}, {"t": 0.8, "op": 1, "escala": 1.0, "ease": "salida"}, {"t": d, "op": 0.5}]),
            *lados(1360, 233),
            *ambiente_cueva(d, sem=233)],
            cam(1.0, 1.35, (540, 960), (540, 900)), "corte",
            sfx=[(0.1 + 0.2 * k, "tic", -24) for k in range(3)])

    @plano(236, "aguantar quinientos días: la vela se consume")
    def _(d):
        o = rel(236)
        tq = o(237)
        a, yv = 700, 1260
        cy = pos("vela_a", 540, yv, a)["y"]
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            brillo(540, 800, 420, "#ffcf8a", 0.55, 0.3, pulso=[0.12, 0.6], keys=[{"t": 0, "y": 700}, {"t": d, "y": 1000}]),
            pie("vela_a", 540, yv, a, z=0.55, keys=[{"t": 0, "op": 1}, {"t": tq, "op": 1}, {"t": d - 0.3, "op": 0}]),
            pie("vela_corta", 540, yv, a, z=0.56, keys=[{"t": 0, "op": 0}, {"t": tq, "op": 0}, {"t": d - 0.3, "op": 1}]),
            pie("vela_b", -300, 1300, 420, z=0.5), pie("vela_corta", -560, 1300, 420, z=0.5), pie("vela_corta", 1380, 1300, 420, z=0.5),
            pie("vela_b", 1640, 1300, 420, z=0.5),
            *ambiente_cueva(d, sem=236, oscura=True)],
            cam(1.0, 1.1, (540, 900), (540, 960)), "corte",
            hud=[contador(tq, d - 0.05, 0, 500, 1.0, " días", tam=130, x=540, y=540, color="#ffd23f", capsula="#0b0f1ed8", miles=False)],
            sfx=[(tq + 1.0, "ding", -20)])

    @plano(239, "los primeros días son casi agradables: dibuja con su café")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            brillo(620, 1150, 420, "#ffcf8a", 0.55, 0.3, pulso=[0.08, 2.0]),
            pie("bea_dibuja", 470, 1300, 520, z=0.55, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.03}]),
            pie("taza_cafe", 760, 1300, 150, z=0.56),
            pie("lampara_led", 880, 1300, 150, z=0.55), pie("colchon", -330, 1300, 170, z=0.5),
            pie("mesa_campamento", 1400, 1300, 320, z=0.5), pie("libro_b", -620, 1300, 80, z=0.5),
            {**polvo("#ffe9c0", 22, (640, 900, 880, 1220), 239), "vel": [3, -30]},
            *ambiente_cueva(d, sem=239)],
            cam(1.0, 1.1, (560, 1100), (600, 1120)), "corte",
            sfx=[(0.2, "trazo", -28), (0.9, "trazo", -28), (1.6, "trazo", -28)])

    @plano(245, "silencio total: una gota en el charco")
    def _(d):
        tg = 0.6
        return P(["#0c0a0c", "#030304"], [
            fondo("bg_negro_cueva"),
            pie("charco", 540, 1240, 200, z=0.5),
            pieza("gota", 540, 470, 60, z=0.6, keys=[{"t": 0, "y": 470, "op": 1}, {"t": tg, "y": 1190, "ease": "entrada"}, {"t": tg + 0.02, "op": 0}]),
            pie("salpicadura", 540, 1230, 140, z=0.61, keys=[{"t": 0, "op": 0, "escala": 0.3}, {"t": tg, "op": 0, "escala": 0.3},
                                                            {"t": tg + 0.04, "op": 1}, {"t": tg + 0.3, "escala": 1.0, "ease": "salida"}, {"t": tg + 0.6, "op": 0}]),
            *[onda(540, 1215, tg + 0.05 + 0.2 * k, 320, "#bfe0ff", 0.9, 4, z=0.52, ey=0.22) for k in range(3)],
            brillo(540, 1200, 260, "#9fc4ff", 0.35, 0.4),
            pie("estalagmita_a", 220, 1344, 300, z=0.45), pie("estalagmita_b", 900, 1344, 260, z=0.45),
            *techo(245, oscura=True), *lados(1344, 245)],
            cam(1.0, 1.12, (540, 1000), (540, 1100)), "corte",
            sfx=[(tg, "burbuja", -18, {"f": 1200})])

    @plano(247, "nadie te escribe: el móvil apagado, tachado")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            brillo(540, 960, 380, "#9fc4ff", 0.3, 0.3, pulso=[0.15, 0.9]),
            pieza("telefono_movil_b", 540, 960, 340, z=0.55, keys=[{"t": 0, "y": 1200, "rot": 20, "op": 0.8}, {"t": 0.35, "y": 960, "rot": -4, "ease": "elastico"},
                                                                   {"t": d, "rot": 2, "op": 0.45}]),
            *aspa(540, 960, 200, 0.5),
            pie("mochila", -300, 1300, 220, z=0.5), pie("telefono_movil", 1380, 1100, 220, z=0.5),
            *ambiente_cueva(d, sem=247, oscura=True)],
            cam(1.0, 1.08, (540, 960)), "corte",
            sfx=[(0.5, "zap", -22)])

    @plano(250, "nadie te pide nada: ojos cerrados, en calma")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            brillo(420, 700, 400, "#ffcf8a", 0.45, 0.4, pulso=[0.1, 1.6]),
            pieza("bea_cara_ojos_cerrados", 540, 950, 900, z=0.6, keys=[{"t": 0, "escala": 1.0, "y": 960}, {"t": d * 0.5, "escala": 1.02, "y": 950},
                                                                        {"t": d, "escala": 1.0, "y": 945}]),
            {**polvo("#ffe9c0", 30, (-400, 500, 1480, 1400), 250), "vel": [3, -12]},
            *techo(250)],
            cam(1.05, 1.15, (540, 900)), "corte",
            sfx=[(0.1, "rumor", -28, {"dur": 1.4})])

    @plano(254, "duermes cuando tienes sueño")
    def _(d):
        n, a = "bea_duerme", 300
        return P(["#141b29", "#07090f"], [
            fondo("bg_cueva_campamento_oscura"),
            pie("colchon", 540, 1290, 210, z=0.5),
            pie(n, 540, 1270, a, z=0.52, keys=[{"t": 0, "ey": 1.0}, {"t": 0.6, "ey": 1.03}, {"t": 1.2, "ey": 1.0}, {"t": 1.8, "ey": 1.03}]),
            pieza("luna_creciente", 760, 760, 180, z=0.45, keys=[{"t": 0, "op": 0, "y": 860}, {"t": 0.5, "op": 0.8}, {"t": d, "y": 700, "op": 0.8}]),
            brillo(760, 740, 200, "#bfe0ff", 0.35, 0.44),
            pie("lampara_led", 850, 1300, 120, z=0.5, op=0.6),
            pie("mochila", -300, 1300, 220, z=0.5), pie("libro_a", 1350, 1300, 80, z=0.5),
            *ambiente_cueva(d, sem=254, oscura=True)],
            cam(1.2, 1.05, (540, 1150)), "corte",
            sfx=[(0.3, "rumor", -28, {"dur": 1.2})])

    @plano(258, "y comes cuando tienes hambre")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            brillo(560, 1100, 400, "#ffcf8a", 0.5, 0.3),
            pie("bea_bebe", 420, 1300, 640, z=0.55, keys=[{"t": 0, "rot": 0}, {"t": 0.6, "rot": -3}, {"t": d, "rot": -1}]),
            pie("caja_comida", 760, 1300, 220, z=0.56, keys=aparece(0.1, 0.4)),
            pie("botella_agua", 920, 1300, 160, z=0.57, keys=aparece(0.3, 0.35)),
            pie("mesa_campamento", -320, 1300, 320, z=0.5), pie("garrafa_agua", 1400, 1300, 200, z=0.5),
            *ambiente_cueva(d, sem=258)],
            cam(1.0, 1.08, (580, 1050)), "corte",
            sfx=[(0.15, "pop", -26), (0.8, "agua", -26, {"dur": 0.8})])

    @plano(263, "y decides que vas a llevar la cuenta: se acerca a la pared")
    def _(d):
        n, a = "bea_marca_a", 700
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            brillo(520, 760, 420, "#ffcf8a", 0.4, 0.3),
            IMG("moho_pared", ancho=420, x=880, y=620, z=0.32, op=0.55),
            pie(n, 200, 1300, a, z=0.6, keys=[{"t": 0, "x": -60}, {"t": d * 0.55, "x": 220, "ease": "suave"}, {"t": d, "x": 240}]),
            tiza(410, 760, d * 0.72, 180),
            *lados(1300, 263),
            *ambiente_cueva(d, sem=263)],
            cam(1.0, 1.15, (420, 950), (480, 850)), "corte",
            sfx=[(0.3, "golpe", -30), (0.8, "golpe", -30), (d * 0.72, "trazo", -18)])

    @plano(271, "cada vez que duermas: se apaga la luz y vuelve")
    def _(d):
        n, a = "bea_duerme", 520
        return P(["#141b29", "#07090f"], [
            fondo("bg_cueva_campamento_oscura"),
            pie("colchon", 520, 1300, 330, z=0.5),
            pie(n, 520, 1270, a, z=0.52, keys=[{"t": 0, "ey": 1.0}, {"t": 0.5, "ey": 1.03}, {"t": 1.0, "ey": 1.0}]),
            pie("lampara_led", 900, 1300, 160, z=0.5),
            brillo(900, 1200, 260, "#ffcf8a", 0.6, 0.49, keys=[{"t": 0, "op": 1}, {"t": 0.25, "op": 0, "ease": "entrada"}, {"t": d - 0.35, "op": 0}, {"t": d - 0.2, "op": 1}]),
            negro([{"t": 0, "op": 0}, {"t": 0.25, "op": 0.8, "ease": "entrada"}, {"t": d - 0.35, "op": 0.8}, {"t": d - 0.2, "op": 0.0}]),
            pie("mochila", -320, 1300, 220, z=0.5), pie("libro_d", 1400, 1300, 80, z=0.5),
            *ambiente_cueva(d, sem=271, oscura=True)],
            cam(1.1, 1.2, (560, 1150)), "corte",
            sfx=[(0.2, "zap", -26), (d - 0.3, "zap", -26)])

    @plano(275, "un día más: la primera raya, de cerca")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            brillo(540, 900, 460, "#ffcf8a", 0.45, 0.3),
            IMG("moho_pared", ancho=520, x=860, y=700, z=0.32, op=0.5),
            tiza(420, 920, 0.02, 520, z=0.55),
            tiza(560, 920, 0.3, 520, z=0.55),
            tiza(-300, 900, 0.0, 400), tiza(1380, 900, 0.1, 400),
            *techo(275)],
            cam(1.3, 1.18, (500, 920)), "corte",
            hud=[amarillo(0.35, d - 0.05, "+1", y=640, tam=150, color=AMBAR, x=760)],
            sfx=[(0.02, "trazo", -18), (0.3, "trazo", -18)])

    @plano(278, "es un buen plan: la pared ordenada en grupos de cinco")
    def _(d):
        grupos = [(300, 700), (560, 700), (820, 700), (300, 980), (560, 980), (-300, 760), (-560, 760), (1380, 760), (1640, 760)]
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            brillo(540, 820, 520, "#ffcf8a", 0.45, 0.3, pulso=[0.1, 0.5]),
            *[pieza("marca_grupo", x, y, 200, z=0.5, keys=[{"t": 0, "op": 0, "escala": 0.6}, {"t": 0.02 + 0.04 * k, "op": 0},
                                                           {"t": 0.05 + 0.04 * k, "op": 1}, {"t": 0.2 + 0.04 * k, "escala": 1.0, "ease": "rebote"}])
              for k, (x, y) in enumerate(grupos)],
            tiza(780, 980, 0.3, 180),
            pie("bea_marca_b", 900, 1320, 560, z=0.6, ex=-1, keys=[{"t": 0, "x": 960}, {"t": 0.6, "x": 930}])],
            cam(1.0, 1.06, (560, 880)), "corte",
            sfx=[(0.05 + 0.08 * k, "tic", -27) for k in range(0, 5)] + [(0.3, "trazo", -24)])

    @plano(281, "plan. y está condenado a fallar: las rayas se tuercen, la luz se apaga (fin de la parte 1)")
    def _(d):
        # Tiempos absolutos desde el inicio del plano (probando la parte sola, el último plano se estira hasta el final del audio)
        o = rel(281)
        tc, tf = o(282), o(286)        # «Y está condenado» … «fallar»
        r = random.Random(282)
        rayas = []
        for k in range(15):
            x = 210 + 46 * k + (22 * (k // 5))
            r1, r2 = r.uniform(-25, 25), r.uniform(-80, 80)
            y1, y2 = 860 + r.uniform(-40, 40), 860 + r.uniform(-120, 120)
            rayas.append(pieza("marca_raya", round(x), 860, 46, z=0.5, keys=[
                {"t": 0, "rot": 0, "op": 1, "y": 860, "ey": 0.0}, {"t": 0.03 * k, "ey": 0.0}, {"t": 0.03 * k + 0.12, "ey": 1.0, "ease": "salida"},
                {"t": tc + 0.1 + 0.02 * k, "rot": 0, "y": 860},
                {"t": tf, "rot": r1, "y": round(y1), "op": r.uniform(0.5, 0.9), "ease": "entrada"},
                {"t": tf + 0.2, "rot": r2, "y": round(y2), "x": round(x + r.uniform(-70, 70)), "ease": "golpe"}]))
        lat = [pieza("marca_raya", x, 840, 40, z=0.5, keys=[{"t": 0, "rot": 0}, {"t": tf, "rot": rr * 0.4, "ease": "entrada"}, {"t": tf + 0.2, "rot": rr, "ease": "golpe"}])
               for x, rr in [(-260, 50), (-310, -45), (-360, 70), (-410, -30), (1340, -55), (1390, 40), (1440, -70), (1490, 35)]]
        luz = [{"t": 0, "op": 1}, {"t": tc + 0.35, "op": 1}, {"t": tc + 0.42, "op": 0.3}, {"t": tc + 0.5, "op": 1}, {"t": tc + 0.85, "op": 0.2},
               {"t": tc + 0.92, "op": 0.9}, {"t": tf, "op": 0.6}, {"t": tf + 0.2, "op": 0.0, "ease": "salida"}]
        oscuro = [{"t": 0, "op": 0}, {"t": tc + 0.35, "op": 0}, {"t": tc + 0.42, "op": 0.45}, {"t": tc + 0.5, "op": 0}, {"t": tc + 0.85, "op": 0.6},
                  {"t": tc + 0.92, "op": 0.1}, {"t": tf, "op": 0.3}, {"t": tf + 0.05, "op": 0.4}, {"t": tf + 0.55, "op": 0.93, "ease": "entrada"}]
        return P(["#3d2a1f", "#050507"], [
            fondo("bg_cueva_campamento"),
            brillo(540, 860, 540, "#ffcf8a", 0.55, 0.3, keys=luz),
            IMG("moho_pared", ancho=420, x=900, y=560, z=0.32, op=0.5),
            *rayas, *lat,
            negro(oscuro),
            *techo(285)],
            {**cam(1.0, 1.25, (540, 860), (540, 860)), "temblor": 3}, "corte",
            sfx=[(0.03, "trazo", -24), (tc + 0.05, "subida", -18, {"dur": 1.0}), (tc + 0.42, "zap", -27), (tc + 0.86, "zap", -25),
                 (tf, "impacto", -12), (tf + 0.03, "zap", -22)])
