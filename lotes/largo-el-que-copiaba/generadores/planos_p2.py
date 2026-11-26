"""Parte 2 (palabras 247–490, 94,8–186,9 s): Lucas y su hamburguesería · ¿por qué? · en tu móvil.
Escrito en coordenadas del vertical (1080×1920), pensado para el largo 16:9 (se ve de x≈−660 a x≈1740)."""
from comun_cp import *  # noqa: F401,F403
import comun

GRIS = "#9aa3b0"
NOCHE = ["#1b1f3a", "#0b0d18"]
DIA = ["#bfe3ff", "#d8d2c8"]
OSCURO = ["#1a1d26", "#07080c"]


# ------------------------------------------------------------------ ayudantes de la parte 2
def pos(nombre, x, suelo, alto, esc=1.0, **mas):
    """Clave {x, y, escala} que deja los pies de una pieza posada en `suelo` aunque cambie de escala."""
    return {"t": 0, "x": x, "y": round(suelo - (comun.APOYO.get(nombre, 0.97) - 0.5) * alto * esc, 1), "escala": esc, **mas}


def mece(d, amp=3, periodo=2.4, base=0):
    """Balanceo suave (rot) para que una figura quieta respire (el `mecer` de comun_cp usa «giro», que el motor no anima)."""
    ks, t, s = [], 0.0, 1
    while t <= d + periodo:
        ks.append({"t": round(t, 3), "rot": base + s * amp, "ease": "suave"})
        t += periodo / 2; s = -s
    return ks


def ypie(nombre, suelo, alto):
    return round(suelo - (comun.APOYO.get(nombre, 0.97) - 0.5) * alto, 1)


def aspa(cx, cy, r, t0, color=ROJO, g=22, z=0.8):
    return [flecha([[cx - r, cy - r], [cx + r, cy + r]], t0, t0 + 0.16, color, g, punta=False, z=z),
            flecha([[cx + r, cy - r], [cx - r, cy + r]], t0 + 0.14, t0 + 0.3, color, g, punta=False, z=z)]


def visto(cx, cy, r, t0, color=VERDE, g=34, z=0.85):
    """✓ que se dibuja de un trazo."""
    return flecha([[cx - r, cy], [cx - r * 0.3, cy + r * 0.7], [cx + r, cy - r * 0.8]], t0, t0 + 0.35, color, g, punta=False, z=z)


def onda(x, y, t0, r=160, color=CIAN, dur=0.8, g=6, z=0.7):
    return {"tipo": "forma", "forma": "elipse", "ancho": r * 2, "alto": r * 2, "relleno": "#ffffff", "op_relleno": 0,
            "grosor": g, "borde": color, "x": x, "y": y, "z": z,
            "keys": [{"t": 0, "escala": 0.15, "op": 0}, {"t": t0, "escala": 0.15, "op": 0}, {"t": t0 + 0.05, "op": 0.9},
                     {"t": t0 + dur, "escala": 1.0, "op": 0.0, "ease": "salida"}]}


def camina(base, x0, x1, suelo, alto, d, fps=4.0, z=0.6, esc=(1.0, 1.0), t0=0.0, t1=None, **k):
    """Personaje que camina de x0 a x1 (fotogramas base_a / base_b)."""
    t1 = d if t1 is None else t1
    def mk(n):
        ks = [pos(n, x0, suelo, alto, esc[0]), {**pos(n, x0, suelo, alto, esc[0]), "t": t0},
              {**pos(n, x1, suelo, alto, esc[1]), "t": t1, "ease": "lineal"}]
        return pie(n, x0, suelo, alto, z=z, keys=ks, **k)
    return flip([base + "_a", base + "_b"], d, fps=fps, base=mk)


def tienda(nombre, x, suelo, alto=700, z=0.4, keys=None, **k):
    return pie(nombre, x, suelo, alto, z=z, keys=keys, **k)


def puerta_x(x, alto):
    """x de la puerta de una fachada de 900×820 colocada en x con ese alto."""
    return x + 0.267 * alto * 900 / 820


def cae_pieza(nombre, x, suelo, alto, t0, t1, z=0.5, desde=-300):
    y1 = ypie(nombre, suelo, alto)
    return pie(nombre, x, suelo, alto, z=z, keys=[{"t": 0, "op": 0, "y": desde}, {"t": t0, "op": 0, "y": desde},
                                                    {"t": t0 + 0.02, "op": 1}] + cae(t0, t1, desde, y1)[1:])


def gente_lado(suelo, sem=1, z=0.45, alto=600, dia=True, d=3.0):
    """Peatones en los laterales (solo se ven en 16:9): uno camina, otros esperan o miran el móvil."""
    r = random.Random(sem)
    quietos = ["voluntario_1", "voluntario_2", "voluntario_3", "voluntario_4", "voluntario_5", "voluntario_6"]
    r.shuffle(quietos)
    out = [pie(quietos[0], -560 + r.uniform(-30, 30), suelo, alto * 0.97, z=z, keys=mece(d, 1.5, 2.2)),
           pie(quietos[1], 1640 + r.uniform(-30, 30), suelo, alto * 0.95, z=z, keys=mece(d, 1.5, 2.6))]
    x0 = r.choice([-700, 1760])
    out += camina("cliente_se_va", x0, x0 + (260 if x0 < 0 else -260), suelo, alto, d, fps=3.5, z=z + 0.01,
                  ex=(1 if x0 < 0 else -1))
    return out


def ciudad_noche(d, sem=1, luna=True):
    """Detalles de la ciudad de noche: farolas que laten, polvo de luz y la luna."""
    out = [brillo(-380, 1180, 260, "#ffcf8a", 0.35, 0.08, pulso=[0.05, 1.7]), brillo(1480, 1180, 260, "#ffcf8a", 0.35, 0.08, pulso=[0.05, 2.1]),
           {**polvo("#ffe2b0", 26, (-600, 500, 1700, 1400), sem), "_ancho": False}]
    if luna:
        out.append(pieza("luna_creciente", 1500, 520, 150, z=0.07, keys=K(d, (0, {"y": 520, "rot": -4}), (1, {"y": 505, "rot": 4}))))
    return out


def calle_dia(d, sem=1):
    return [brillo(200, 500, 520, "#fff3c0", 0.35, 0.07, pulso=[0.04, 3.0]),
            {**polvo("#fffbe8", 20, (-600, 500, 1700, 1400), sem), "_ancho": False}]


def foco(x, suelo, alto=1500, frio=False, z=0.1, op=0.9):
    return pie("foco_luz_frio" if frio else "foco_luz", x, suelo, alto, z=z, op=op)


def barra(x, base, ancho, alto, color, t0, t1, z=0.5):
    """Barra que crece hacia arriba desde `base` (y del suelo de la barra) hasta `alto`."""
    return {"tipo": "forma", "forma": "redondeado", "ancho": ancho, "alto": alto, "esquinas": 18, "relleno": color, "x": x,
            "y": base - alto / 2, "z": z, "sombra": True, "brillo": True,
            "keys": [{"t": 0, "ey": 0.0, "y": base}, {"t": t0, "ey": 0.0, "y": base},
                     {"t": t1, "ey": 1.0, "y": base - alto / 2, "ease": "salida"}]}


def planos(v, plano):
    w = v.w

    def rel(i0):
        return lambda j: round(w(j) - w(i0), 3)

    SC = SUELO["bg_ciudad"]          # 1390
    SD = SUELO["bg_calle_dia"]       # 1440
    SE = SUELO["bg_estudio_oscuro"]  # 1400
    SF = SUELO["bg_cafe_dentro"]     # 1430
    SN = comun.ANCLA["bg_alpes_nieve"][1]   # 1340
    SH = SUELO["bg_habitacion"]      # 1440

    # ================================================================== LUCAS (247–334)
    @plano(247, "mientras tanto: cara de Lucas en la ciudad")
    def _(d):
        return P(NOCHE, [
            fondo("bg_ciudad"), *ciudad_noche(d, 247),
            brillo(300, 800, 380, "#5f9fe0", 0.3, 0.2, pulso=[0.08, 1.2]),
            pieza("cara_lucas_sonrie", 540, 1000, 820, z=0.6, keys=arranque(540, 1000, d, "izquierda", 300, 30)),
            pie("voluntario_3", -420, SC, 640, z=0.4), pie("voluntario_5", 1560, SC, 620, z=0.4)],
            cam(1.05, 1.12, (540, 950)), "barrido", sfx=[(0.02, "whoosh", -22)])

    @plano(249, "Lucas da un paseo por el barrio")
    def _(d):
        return P(NOCHE, [
            fondo("bg_ciudad"), *ciudad_noche(d, 249),
            *camina("lucas_camina", -300, 520, SC, 640, d, fps=3.5, z=0.6),
            pie("hamburgueseria", 1450, SC, 640, z=0.35),
            *cola(1360, SC, n=4, alto=520, paso=110, z=0.4),
            *gente_lado(SC, 249, d=d)],
            cam(1.1, 1.0, (200, 1100), (600, 1050)), "corte",
            sfx=[(0.3, "roce", -30), (0.9, "roce", -30), (1.5, "roce", -30)])

    @plano(256, "y se fija: los ojos de Lucas")
    def _(d):
        return P(NOCHE, [
            fondo("bg_ciudad"), *ciudad_noche(d, 256, luna=False),
            brillo(900, 700, 420, "#ffcf8a", 0.4, 0.2),
            pieza("cara_lucas_listo", 520, 1020, 900, z=0.6, keys=K(d, (0, {"rot": -5, "escala": 1.0}), (0.35, {"rot": 3, "ease": "salida"}), (1, {"escala": 1.06})))],
            cam(1.1, 1.3, (520, 820)), "corte", sfx=[(0.12, "tic", -20)])

    @plano(260, "en una cosa: la hamburguesería con cola (fotograma aprobado)")
    def _(d):
        tx = 1265
        return P(NOCHE, [
            fondo("bg_ciudad"), *ciudad_noche(d, 260),
            tienda("hamburgueseria", tx, SC + 10, 775, z=0.4),
            brillo(tx, ypie("hamburgueseria", SC + 10, 775) - 260, 200, "#ffd890", 0.55, 0.41, pulso=[0.12, 0.7]),
            *cola(1140, SC + 8, n=6, alto=550, paso=131, z=0.5),
            pie("lucas_piensa", -210, SC + 94, 675, z=0.62, keys=mece(d, 1.2, 2.0)),
            senala(tx, ypie("hamburgueseria", SC + 10, 775) - 260, d * 0.45, d, 120, AMBAR),
            pie("voluntario_6", 1700, SC, 600, z=0.3)],
            cam(1.0, 1.08, (560, 1050), (700, 1030)), "corte", sfx=[(d * 0.45, "ding", -24)])

    @plano(262, "hay una hamburguesería con cola: la cámara recorre la cola")
    def _(d):
        tx = 1050
        return P(NOCHE, [
            fondo("bg_ciudad"), *ciudad_noche(d, 262),
            tienda("hamburgueseria", tx, SC, 840, z=0.4),
            *cola(940, SC + 6, n=12, alto=600, paso=140, z=0.5, avanza=(d * 0.5, 36)),
            pie("voluntario_2", 1650, SC, 620, z=0.45)],
            cam(1.15, 1.15, (1000, 1050), (250, 1050)), "corte",
            sfx=[(d * 0.5, "roce", -26), (d * 0.5 + 0.3, "roce", -28)])

    @plano(267, "hasta la esquina: la cola se sale por el lateral")
    def _(d):
        tx = 1500
        return P(NOCHE, [
            fondo("bg_ciudad"), *ciudad_noche(d, 267),
            tienda("hamburgueseria", tx, SC, 560, z=0.4),
            *cola(1410, SC, n=20, alto=420, paso=104, z=0.5),
            flecha([[1300, 900], [-700, 900]], 0.1, d * 0.8, AMBAR + "cc", 7, [26, 18], z=0.6)],
            cam(1.0, 1.1, (1300, 1100), (-200, 1080)), "corte", sfx=[(0.05, "whoosh", -24)])

    @plano(270, "todos (de día): la cola sigue")
    def _(d):
        tx = 1100
        return P(DIA, [
            fondo("bg_calle_dia"), *calle_dia(d, 270),
            tienda("hamburgueseria", tx, SD, 720, z=0.4),
            *cola(1000, SD, n=10, alto=560, paso=125, z=0.5, avanza=(0.1, 30)),
            brillo(-200, 480, 300, "#fff2a0", 0.8, 0.06, keys=K(d, (0, {"x": -400}), (1, {"x": 200})))],
            cam(1.08, 1.12, (600, 1050)), "corte", sfx=[(0.02, "pop", -24)])

    @plano(272, "los días (de noche): hojas del calendario que vuelan")
    def _(d):
        tx = 1100
        hojas = [pieza("calendario_hoja", 540 + 360 * (i - 1), 760, 240, z=0.7 + 0.01 * i,
                       keys=[{"t": 0, "rot": 0, "op": 1}, {"t": 0.12 + 0.2 * i, "rot": 0, "y": 760, "x": 540 + 360 * (i - 1)},
                             {"t": 0.12 + 0.2 * i + 0.45, "rot": -40 + 30 * i, "y": 300, "x": 540 + 360 * (i - 1) + 260, "op": 0, "ease": "entrada"}])
                 for i in range(3)]
        return P(NOCHE, [
            fondo("bg_ciudad"), *ciudad_noche(d, 272),
            tienda("hamburgueseria", tx, SC, 720, z=0.4),
            *cola(1000, SC, n=10, alto=560, paso=125, z=0.5, oscuro=0.1),
            *hojas],
            cam(1.12, 1.08, (600, 1000)), "corte", sfx=[(0.12 + 0.2 * i, "roce", -24) for i in range(3)])

    @plano(273, "Lucas no piensa «qué idea más vista»")
    def _(d):
        o = rel(273)
        t0 = max(0.1, o(276) - 0.08)
        return P(NOCHE, [
            fondo("bg_ciudad"), *ciudad_noche(d, 273),
            tienda("hamburgueseria", 1450, SC, 700, z=0.35),
            *cola(1340, SC, n=6, alto=540, paso=125, z=0.4, oscuro=0.15),
            pie("lucas_piensa", 260, SC + 40, 760, z=0.6, keys=mece(d, 2.0, 1.6)),
            {"tipo": "forma", "forma": "circulo", "radio": 22, "relleno": "#f6f2ea", "x": 420, "y": 760, "z": 0.7, "keys": aparece(t0 - 0.1, 0.25)},
            {"tipo": "forma", "forma": "circulo", "radio": 36, "relleno": "#f6f2ea", "x": 480, "y": 690, "z": 0.7, "keys": aparece(t0 - 0.05, 0.25)},
            *aspa(640, 560, 170, o(279) + 0.15, z=1.0),
            pie("voluntario_4", -520, SC, 620, z=0.45)],
            cam(1.0, 1.1, (500, 1000), (480, 900)), "corte",
            hud=[rotulo(t0, d - 0.05, "¿QUÉ IDEA MÁS VISTA?", tam=64, color="#2a2a33", capsula="#f6f2eaf2", borde="#ffffff", x=640, y=560)],
            sfx=[(o(279) + 0.15, "zap", -20)])

    @plano(280, "piensa: cara de Lucas que se ilumina")
    def _(d):
        return P(NOCHE, [
            fondo("bg_ciudad"), *ciudad_noche(d, 280, luna=False),
            brillo(560, 760, 520, "#ffd890", 0.5, 0.2, keys=K(d, (0, {"op": 0.2}), (0.4, {"op": 1.0}))),
            pieza("cara_lucas_sonrie", 540, 1050, 880, z=0.6, keys=K(d, (0, {"escala": 0.95}), (1, {"escala": 1.06}))),
            pieza("destello", 820, 600, 260, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.2, "op": 1, "escala": 1, "ease": "salida"}, {"t": 0.7, "op": 0}])],
            cam(1.0, 1.15, (540, 850)), "corte", sfx=[(0.2, "ding", -22)])

    @plano(281, "aquí hay gente que quiere hamburguesas: el bocadillo con la cola")
    def _(d):
        o = rel(281)
        tx = 1350
        th = o(286)
        hb = [pieza("hamburguesa", 1240 - 125 * i, 860, 90, z=0.6,
                    keys=[{"t": 0, "op": 0, "escala": 0}, {"t": th + 0.08 * i, "op": 0, "escala": 0.2},
                          {"t": th + 0.08 * i + 0.3, "op": 1, "escala": 1.0, "ease": "rebote"}, {"t": d, "y": 840}]) for i in range(5)]
        return P(NOCHE, [
            fondo("bg_ciudad"), *ciudad_noche(d, 281),
            tienda("hamburgueseria", tx, SC, 720, z=0.4),
            *cola(1240, SC, n=7, alto=560, paso=125, z=0.5),
            pie("lucas_piensa", -120, SC + 40, 700, z=0.6, keys=mece(d, 1.5, 2.0)),
            pieza("pensamiento_cola", 200, 600, 560, z=0.7, keys=aparece(0.1, 0.45) + [{"t": d, "y": 585}]),
            *hb],
            cam(1.0, 1.06, (540, 1000), (620, 980)), "corte",
            sfx=[(0.1, "burbuja", -22), (th, "pop", -22)])

    @plano(287, "y está esperando: la cola de cerca, impaciente")
    def _(d):
        gente = []
        for i, (n, x) in enumerate([("cola_1", 860), ("cola_3", 520), ("cola_4", 180), ("cola_0", -160), ("cola_5", -500), ("cola_2", 1200)]):
            gente.append(pie(n, x, SC + 60, 1000, z=0.5 + 0.01 * i, keys=mece(d, 2.0, 0.9 + 0.2 * i)))
        return P(NOCHE, [
            fondo("bg_ciudad"), *ciudad_noche(d, 287, luna=False),
            brillo(1300, 900, 500, "#ffcf8a", 0.5, 0.2, pulso=[0.06, 1.2]), *gente],
            cam(1.0, 1.08, (400, 900), (600, 900)), "corte",
            sfx=[(0.05, "tictac", -26, {"dur": d - 0.1, "ritmo": 0.3})])

    @plano(290, "así que abre otra hamburguesería: cae del cielo")
    def _(d):
        tx = 640
        return P(DIA, [
            fondo("bg_calle_dia"), *calle_dia(d, 290),
            cae_pieza("hamburgueseria_lucas", tx, SD, 760, 0.1, 0.75, z=0.4, desde=-400),
            {**polvo("#e8dccb", 30, (200, 1300, 1100, 1450), 290), "vel": [40, -30]},
            pie("lucas_delantal", -10, SD, 640, z=0.6, keys=[pos("lucas_delantal", -10, SD, 640)] + late(0.8, 1, 0.06)),
            *gente_lado(SD, 290, d=d)],
            cam(1.0, 1.06, (540, 1050), temblor=0), "corte",
            sfx=[(0.55, "golpe", -14), (0.9, "ding", -24)])

    @plano(295, "dos calles más allá: de la vieja a la nueva")
    def _(d):
        return P(DIA, [
            fondo("bg_calle_dia"), *calle_dia(d, 295),
            tienda("hamburgueseria", -260, SD, 600, z=0.4),
            *cola(-380, SD, n=4, alto=470, paso=110, z=0.45),
            tienda("hamburgueseria_lucas", 1360, SD, 600, z=0.4, keys=late(d * 0.7, 1, 0.05)),
            flecha([[-60, 760], [550, 560], [1160, 760]], 0.1, d * 0.7, CIAN, 9, [28, 18], z=0.7)],
            cam(1.1, 1.1, (-100, 1050), (1200, 1050)), "corte",
            hud=[rotulo(0.15, d - 0.05, "2 CALLES", tam=80, color="#ffffff", capsula="#173a60e6", x=550, y=470)])

    @plano(299, "igual de buena: dos hamburguesas iguales")
    def _(d):
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"),
            foco(130, SE), foco(950, SE),
            pie("hamburguesa", 130, SE - 20, 380, z=0.5, keys=[pos("hamburguesa", 130, SE - 20, 380)] + K(d, (0, {"rot": -3}), (1, {"rot": 3}))),
            pie("hamburguesa", 950, SE - 20, 380, z=0.5, keys=[pos("hamburguesa", 950, SE - 20, 380)] + K(d, (0, {"rot": 3}), (1, {"rot": -3}))),
            pieza("icono_igual", 540, 1180, 200, z=0.6, keys=aparece(0.25, 0.4)),
            pie("bolsa_comida", -450, SE, 300, z=0.45), pie("bolsa_comida", 1530, SE, 300, z=0.45)],
            cam(1.0, 1.06, (540, 1150)), "corte", sfx=[(0.25, "pop", -20)])

    @plano(302, "con una diferencia: Lucas levanta el dedo")
    def _(d):
        tx = 900
        return P(DIA, [
            fondo("bg_calle_dia"), *calle_dia(d, 302),
            tienda("hamburgueseria_lucas", tx, SD, 820, z=0.4),
            pie("lucas_senala", 360, SD + 60, 820, z=0.6, keys=[pos("lucas_senala", 360, SD + 60, 820)] + late(0.35, 1, 0.05)),
            brillo(560, 700, 160, "#ffffff", 0.6, 0.65, keys=[{"t": 0, "op": 0}, {"t": 0.35, "op": 1}, {"t": d, "op": 0.3}]),
            *gente_lado(SD, 302, d=d)],
            cam(1.0, 1.15, (450, 1000), (420, 880)), "corte", sfx=[(0.35, "ding", -24)])

    @plano(305, "allí esperabas veinte minutos: la cola de la vieja")
    def _(d):
        tx = 1100
        return P(["#c9c2c8", "#7a6e78"], [
            fondo("bg_calle_dia"),
            tienda("hamburgueseria", tx, SD, 720, z=0.4),
            *cola(1000, SD, n=12, alto=560, paso=125, z=0.5, avanza=(d * 0.6, 22))],
            cam(1.1, 1.0, (700, 1050), (500, 1050)), "corte",
            hud=[contador(0.15, d - 0.05, 0, 20, d * 0.75, " MIN", tam=120, x=540, y=560, color="#ffffff", capsula="#c0392be6", miles=False)],
            sfx=[(0.15, "tictac", -24, {"dur": d * 0.75, "ritmo": 0.16})])

    @plano(309, "aquí, cinco: la cola de Lucas entra rápido")
    def _(d):
        tx = 900
        px = puerta_x(tx, 720)
        cl = [pie(n, x, SD, 560, z=0.5, keys=[pos(n, x, SD, 560), {**pos(n, x, SD, 560), "t": 0.1 + 0.25 * i},
                                                   {**pos(n, px, SD, 560, 0.9), "t": 0.6 + 0.25 * i, "op": 1, "ease": "suave"},
                                                   {"t": 0.7 + 0.25 * i, "op": 0}])
              for i, (n, x) in enumerate([("cola_2", 760), ("cola_5", 630)])]
        return P(DIA, [
            fondo("bg_calle_dia"), *calle_dia(d, 309),
            tienda("hamburgueseria_lucas", tx, SD, 720, z=0.4),
            brillo(px, 1150, 260, "#ffd890", 0.5, 0.41, pulso=[0.1, 0.8]),
            *cl, pie("lucas_delantal", 180, SD, 640, z=0.55, keys=mece(d, 1.5, 1.6)),
            *gente_lado(SD, 309, d=d)],
            cam(1.0, 1.08, (600, 1050)), "corte",
            hud=[contador(0.05, d - 0.05, 20, 5, 0.6, " MIN", tam=130, x=540, y=560, color="#ffffff", capsula="#1e8a4ee6", miles=False)],
            sfx=[(0.05, "zap", -22), (0.7, "ding", -18)])

    @plano(311, "a nadie tiene que explicarle nada: entran solos")
    def _(d):
        tx = 900
        px = puerta_x(tx, 760)
        entra = []
        for j, (x0, t0) in enumerate([(-400, 0.0), (-650, 0.6)]):
            ks_x = lambda n, x0=x0, t0=t0: [pos(n, x0, SD, 600), {**pos(n, x0, SD, 600), "t": t0},
                                             {**pos(n, px - 60, SD, 600, 0.92), "t": t0 + 1.4, "ease": "lineal"}, {"t": t0 + 1.35, "op": 1}, {"t": t0 + 1.5, "op": 0}]
            entra += flip(["cliente_se_va_a", "cliente_se_va_b"], d, fps=3.5, t0=0.1 * j, base=lambda n, f=ks_x: pie(n, 0, SD, 600, z=0.55 + 0.01 * j, keys=f(n)))
        return P(DIA, [
            fondo("bg_calle_dia"), *calle_dia(d, 311),
            tienda("hamburgueseria_lucas", tx, SD, 760, z=0.4),
            pie("lucas_entrega", px + 140, SD + 20, 620, z=0.5, keys=mece(d, 1.2, 1.4)),
            pie("cliente_feliz_1", 1500, SD, 610, z=0.5, keys=[pos("cliente_feliz_1", 1350, SD, 610), {**pos("cliente_feliz_1", 1600, SD, 610), "t": d}]),
            pie("cliente_feliz_2", 300, SD + 30, 620, z=0.6, keys=[pos("cliente_feliz_2", 340, SD + 30, 620), {**pos("cliente_feliz_2", 200, SD + 30, 620), "t": d}]),
            *entra],
            cam(1.0, 1.05, (500, 1050), (650, 1050)), "corte",
            sfx=[(0.3, "roce", -28), (1.2, "pop", -26), (1.8, "pop", -26)])

    @plano(317, "la gente ve hamburguesas: detalle")
    def _(d):
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"), foco(540, SE),
            brillo(540, 1000, 420, "#ffcf8a", 0.5, 0.2, pulso=[0.08, 1.0]),
            pie("hamburguesa", 540, SE - 40, 560, z=0.6, keys=[pos("hamburguesa", 540, SE - 40, 560, 0.85), {**pos("hamburguesa", 540, SE - 40, 560, 1.05), "t": d, "ease": "suave"}]
                + [{"t": 0, "rot": -4}, {"t": d, "rot": 2}]),
            pie("bolsa_comida", 120, SE, 340, z=0.55, keys=aparece(0.3)), pie("bolsa_comida", 960, SE, 300, z=0.55, keys=aparece(0.45)),
            pieza("destello", 700, 900, 220, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.5, "op": 1, "escala": 1, "ease": "salida"}, {"t": 1.0, "op": 0}]),
            pie("cliente_feliz_2", -450, SE, 620, z=0.5), pie("cliente_feliz_3", 1530, SE, 620, z=0.5)],
            cam(1.0, 1.1, (540, 1100)), "corte", sfx=[(0.05, "mordisco", -22), (0.5, "brillo", -26)])

    @plano(321, "ve que no hay cola, y entra: la cola se cambia de tienda")
    def _(d):
        viejo, nuevo = -300, 1300
        pn = puerta_x(nuevo, 640)
        gente = []
        for i in range(7):
            n = f"cola_{i % 6}"
            x0 = -400 - i * 110
            t0 = 0.15 + 0.12 * i
            x1 = pn - 120 - i * 115
            gente.append(pie(n, x0, SD, 520, z=0.5 - 0.002 * i, keys=[pos(n, x0, SD, 520), {**pos(n, x0, SD, 520), "t": t0},
                                                                      {**pos(n, x1, SD, 520), "t": t0 + 1.3, "ease": "suave"},
                                                                      {"t": t0 + 0.3, "ey": 0.97}, {"t": t0 + 0.6, "ey": 1.0}, {"t": t0 + 0.9, "ey": 0.97}, {"t": t0 + 1.2, "ey": 1.0}]))
        return P(DIA, [
            fondo("bg_calle_dia"), *calle_dia(d, 321),
            tienda("hamburgueseria", viejo, SD, 640, z=0.4),
            tienda("hamburgueseria_lucas", nuevo, SD, 640, z=0.4, keys=late(d * 0.75, 1, 0.05)),
            *gente,
            flecha([[-200, 700], [1100, 700]], 0.2, d * 0.7, CIAN, 8, [26, 16], z=0.7)],
            cam(1.05, 1.05, (100, 1050), (900, 1050)), "corte",
            sfx=[(0.3, "roce", -26), (0.8, "roce", -27), (1.3, "roce", -26), (d * 0.75, "ding", -22)])

    @plano(328, "en un año: doce meses en un suspiro")
    def _(d):
        hojas = [pieza("calendario_hoja", 540, 940, 420, z=0.6 + 0.01 * (5 - i),
                       keys=[{"t": 0, "rot": 0, "op": 1, "x": 540, "y": 940}, {"t": 0.05 + 0.12 * i, "rot": 0, "y": 940, "x": 540},
                             {"t": 0.05 + 0.12 * i + 0.35, "rot": 50 - 25 * (i % 3), "y": 500, "x": 1100, "op": 0, "ease": "entrada"}])
                 for i in range(6)]
        return P(DIA, [
            fondo("bg_calle_dia"),
            {"tipo": "forma", "forma": "rect", "ancho": 2600, "alto": 2400, "relleno": "#0b0d18", "x": 540, "y": 960, "z": 0.06, "op": 0.0,
             "keys": [{"t": 0, "op": 0.0}, {"t": 0.2, "op": 0.6}, {"t": 0.4, "op": 0.0}, {"t": 0.6, "op": 0.6}, {"t": 0.8, "op": 0.0}]},
            pie("calendario_hoja", 540, 1150, 420, z=0.55), *hojas,
            pie("hamburgueseria_lucas", -400, SD, 600, z=0.4), pie("hamburgueseria_lucas", 1480, SD, 600, z=0.4, op=0.0)],
            cam(1.0, 1.12, (540, 950)), "corte",
            hud=[contador(0.05, d - 0.05, 1, 12, 0.6, " MESES", tam=90, x=540, y=1330, color="#ffffff", capsula="#173a60e6", miles=False)],
            sfx=[(0.05 + 0.12 * i, "roce", -26) for i in range(0, 6, 2)])

    @plano(331, "Lucas tiene dos locales")
    def _(d):
        o = rel(331)
        t2 = max(0.2, o(333) - 0.3)
        return P(DIA, [
            fondo("bg_calle_dia"), *calle_dia(d, 331),
            tienda("hamburgueseria_lucas", 80, SD, 680, z=0.4),
            cae_pieza("hamburgueseria_lucas", 1000, SD, 680, t2, t2 + 0.55, z=0.4, desde=-400),
            *cola(-60, SD, n=3, alto=520, paso=115, z=0.45),
            *cola(860, SD, n=3, alto=520, paso=115, z=0.45, avanza=(t2 + 0.6, 20)),
            pie("lucas_contento", 540, SD + 80, 700, z=0.65, keys=[pos("lucas_contento", 540, SD + 80, 700)] + late(t2 + 0.5, 2, 0.06)),
            {**polvo("#ffd23f", 40, (-400, 400, 1500, 1200), 331), "vel": [20, 40]},
            pie("voluntario_1", -560, SD, 600, z=0.45), pie("voluntario_4", 1660, SD, 600, z=0.45)],
            cam(1.0, 1.06, (540, 1050)), "corte",
            hud=[rotulo(t2 + 0.35, d - 0.05, "2 LOCALES", tam=96, color="#ffffff", capsula="#c8322ae6", x=540, y=470)],
            sfx=[(t2 + 0.35, "golpe", -14), (t2 + 0.6, "ding", -20)])

    # ================================================================== ¿POR QUÉ? (335–402)
    @plano(335, "¿qué ha pasado?: persiana de Marta frente a la cola de Lucas")
    def _(d):
        return P(DIA, [
            fondo("bg_calle_dia"),
            tienda("cafeteria_marta_cerrada", -200, SD, 660, z=0.4),
            pie("marta_triste", 240, SD, 620, z=0.55, keys=mece(d, 1.0, 1.6)),
            tienda("hamburgueseria_lucas", 1280, SD, 660, z=0.4),
            *cola(1160, SD, n=4, alto=520, paso=115, z=0.45),
            pie("lucas_contento", 700, SD, 640, z=0.55, keys=mece(d, 1.5, 1.2))],
            cam(1.15, 1.15, (0, 1050), (1100, 1050)), "barrido", sfx=[(0.05, "whoosh", -20)])

    @plano(338, "Marta tuvo que hacer dos trabajos a la vez: hace malabares")
    def _(d):
        def bota(t_off):
            ks, t, arriba = [], t_off, True
            while t <= d + 0.4:
                ks.append({"t": round(t, 3), "y": 520 if arriba else 760, "rot": 15 if arriba else -10, "ease": "suave"}); t += 0.4; arriba = not arriba
            return ks
        return P(["#e9d8b8", "#6b4a30"], [
            fondo("bg_cafe_dentro"),
            *flip(["marta_explica_a", "marta_explica_b"], d, fps=2.5, base=lambda n: pie(n, 540, SF, 700, z=0.55)),
            pieza("bombilla_b", 280, 640, 230, z=0.6, keys=[{"t": 0, "y": 760}] + bota(0.0)),
            pieza("taza_cafe_latte", 810, 640, 260, z=0.6, keys=[{"t": 0, "y": 520}] + bota(0.4)),
            pie("cliente_confuso_1", -420, SF, 620, z=0.5), pie("cliente_confuso_2", 1520, SF, 620, z=0.5)],
            cam(1.0, 1.08, (540, 1000)), "corte",
            hud=[rotulo(0.3, d - 0.05, "2 TRABAJOS", tam=90, color="#ffffff", capsula="#7a3a22e6", x=540, y=360)],
            sfx=[(0.4 * i, "pop", -28) for i in range(1, int(d / 0.4), 2)])

    @plano(347, "inventar algo: la bombilla se enciende")
    def _(d):
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"), foco(540, SE, 1600),
            pieza("bombilla_a", 540, 900, 380, z=0.6, keys=[{"t": 0, "op": 1, "rot": -6}, {"t": 0.35, "op": 1, "rot": 4}, {"t": 0.37, "op": 0}]),
            pieza("bombilla_b", 540, 900, 380, z=0.61, keys=[{"t": 0, "op": 0, "rot": 4}, {"t": 0.35, "op": 0}, {"t": 0.37, "op": 1}, {"t": d, "rot": -2, "escala": 1.08}]),
            brillo(540, 860, 460, "#ffe38a", 0.7, 0.3, keys=[{"t": 0, "op": 0}, {"t": 0.37, "op": 1}]),
            onda(540, 860, 0.37, 320, "#ffe38a")],
            cam(1.0, 1.1, (540, 950)), "corte", sfx=[(0.35, "brillo", -18)])

    @plano(349, "y convencer a la gente: pantalla partida")
    def _(d):
        o = rel(349)
        return P(["#e9d8b8", "#6b4a30"], [
            fondo("bg_cafe_dentro"),
            # mitad izquierda: el invento
            {"tipo": "forma", "forma": "rect", "ancho": 1100, "alto": 2600, "relleno": ["#20232e", "#0a0b10"], "x": -260, "y": 960, "z": 0.3},
            {"tipo": "forma", "forma": "rect", "ancho": 12, "alto": 2600, "relleno": "#ffffff", "x": 290, "y": 960, "z": 0.31},
            brillo(-200, 880, 330, "#ffe38a", 0.6, 0.32, pulso=[0.08, 0.9]),
            pieza("bombilla_b", -200, 880, 260, z=0.4, keys=K(d, (0, {"rot": -4}), (1, {"rot": 4}))),
            pieza("icono_mas", 290, 900, 150, z=0.45, keys=aparece(0.15) + late(0.8, 1, 0.12)),
            # mitad derecha: convencer
            *flip(["marta_explica_a", "marta_explica_b"], d, fps=3, base=lambda n: pie(n, 640, SF, 680, z=0.55)),
            pie("cliente_confuso_1", 1080, SF, 640, z=0.5, keys=mece(d, 2.5, 1.0)),
            pie("cliente_confuso_2", 1400, SF, 630, z=0.5, keys=mece(d, 2.5, 1.2, 1)),
            pie("cliente_se_va_a", 1680, SF, 620, z=0.48, keys=[pos("cliente_se_va_a", 1600, SF, 620), {**pos("cliente_se_va_a", 1800, SF, 620), "t": d}])],
            cam(1.0, 1.05, (540, 1000), (600, 1000)), "corte",
            sfx=[(0.15, "pop", -22), (o(351) if o(351) < d else 1.0, "roce", -26)])

    @plano(359, "Lucas se saltó la parte más difícil: salta la valla")
    def _(d):
        n = "lucas_camina_b"
        y0 = ypie(n, SD, 600)
        ts = d * 0.35
        return P(DIA, [
            fondo("bg_calle_dia"), *calle_dia(d, 359),
            pie("p2_valla", 560, SD, 420, z=0.5),
            pie("marta_triste", -300, SD, 600, z=0.45),
            pie("p2_piedra_a", -60, SD, 150, z=0.46), pie("p2_piedra_a", 1500, SD, 170, z=0.46),
            pie(n, 0, SD, 600, z=0.6, keys=[{"t": 0, "x": 60, "y": y0, "rot": 0}, {"t": ts, "x": 340, "y": y0, "rot": 0, "ease": "lineal"},
                                            {"t": ts + 0.35, "x": 560, "y": y0 - 560, "rot": 12, "ease": "salida"},
                                            {"t": ts + 0.7, "x": 800, "y": y0, "rot": 0, "ease": "entrada"},
                                            {"t": d, "x": 1000, "y": y0, "ease": "lineal"}]),
            flecha([[220, 1200], [560, 480], [900, 1200]], ts - 0.1, ts + 0.7, AMBAR + "cc", 7, [22, 14], z=0.4),
            pie("voluntario_6", 1680, SD, 600, z=0.45)],
            cam(1.0, 1.06, (560, 1050)), "corte",
            sfx=[(ts, "whoosh", -20), (ts + 0.7, "golpe", -20)])

    @plano(366, "porque la cola le estaba diciendo: la cola brilla")
    def _(d):
        tx = 1300
        cl = cola(1190, SC, n=8, alto=560, paso=125, z=0.5)
        luces = [brillo(1190 - 125 * i, 1100, 140, "#7dffb0", 0.55, 0.45,
                        keys=[{"t": 0, "op": 0}, {"t": 0.15 + 0.15 * i, "op": 0}, {"t": 0.3 + 0.15 * i, "op": 1}]) for i in range(8)]
        return P(NOCHE, [
            fondo("bg_ciudad"), *ciudad_noche(d, 366),
            tienda("hamburgueseria", tx, SC, 720, z=0.4), *luces, *cl,
            pie("lucas_piensa", -330, SC + 40, 700, z=0.6, keys=mece(d, 1.5, 1.8))],
            cam(1.0, 1.08, (500, 1050), (650, 1030)), "corte",
            sfx=[(0.3 + 0.3 * i, "tic", -28) for i in range(4)])

    @plano(373, "«esto funciona»: un visto verde enorme")
    def _(d):
        tx = 1000
        return P(NOCHE, [
            fondo("bg_ciudad"), *ciudad_noche(d, 373),
            tienda("hamburgueseria", tx, SC, 820, z=0.4),
            *cola(880, SC, n=8, alto=620, paso=135, z=0.5),
            brillo(540, 800, 520, VERDE, 0.45, 0.6, keys=[{"t": 0, "op": 0}, {"t": 0.15, "op": 1}]),
            visto(540, 780, 230, 0.12, VERDE, 44, z=0.9)],
            cam(1.0, 1.08, (600, 1000)), "corte",
            hud=[rotulo(0.35, d - 0.05, "ESTO FUNCIONA", tam=88, color="#ffffff", capsula="#1e8a4ee6", x=540, y=1180)],
            sfx=[(0.12, "trazo", -20), (0.35, "ding", -16)])

    # el camino en la nieve: Marta abre camino, Lucas va detrás
    def huellas(x0, x1, t0, t1, suelo, d, paso=95):
        out = []
        nn = max(1, int((x1 - x0) / paso))
        for k in range(nn + 1):
            x = x0 + k * paso
            tk = t0 + (t1 - t0) * k / nn
            if tk > d:
                break
            out.append(pieza("p2_huella_nieve", round(x), suelo + 8, 110, z=0.45,
                             keys=[{"t": 0, "op": 0 if tk > 0 else 1}, {"t": max(0, tk), "op": 0 if tk > 0 else 1}, {"t": max(0, tk) + 0.05, "op": 0.85}]))
        return out

    @plano(375, "el primero que abre un camino: Marta en la nieve")
    def _(d):
        return P(["#dfeaf6", "#9fb4cc"], [
            fondo("bg_alpes_nieve"),
            *camina("marta_camina", -200, 700, SN, 620, d, fps=2.5, z=0.6),
            *huellas(-500, 640, -0.6, d, SN, d),
            pie("p2_piedra_b", 1250, SN, 220, z=0.5), pie("p2_piedra_b", -550, SN, 180, z=0.5),
            {**polvo("#ffffff", 50, (-600, 350, 1700, 1400), 375, "nieve"), "vel": [20, 60]}],
            cam(1.05, 1.1, (100, 1050), (600, 1030)), "corte",
            sfx=[(0.3, "roce", -24), (0.7, "roce", -24), (1.1, "roce", -24)])

    @plano(381, "se come todos los golpes: le caen piedras")
    def _(d):
        n = "marta_camina_a"
        y0 = ypie(n, SN, 700)
        golpes = [0.25, 0.85, 1.45]
        piedras = []
        for j, tg in enumerate(golpes):
            px = 520 + 60 * (j - 1)
            piedras.append(pieza("p2_piedra_a" if j % 2 == 0 else "p2_piedra_b", px, 300, 200 + 30 * j, z=0.7,
                                 keys=[{"t": 0, "op": 0, "y": 300, "x": px}, {"t": tg - 0.22, "op": 1, "y": 300, "x": px, "rot": 0},
                                       {"t": tg, "y": 640, "rot": 25, "ease": "entrada"},
                                       {"t": tg + 0.35, "y": SN - 50, "x": px + (200 if j % 2 else -220), "rot": -10 if j % 2 else 15, "ease": "rebote"}]))
        mk = []
        for tg in golpes:
            mk += [{"t": tg, "rot": 0, "y": y0}, {"t": tg + 0.08, "rot": -9 if tg != 0.85 else 9, "y": y0 + 30, "ease": "salida"},
                   {"t": tg + 0.4, "rot": 0, "y": y0, "ease": "elastico"}]
        return P(["#dfeaf6", "#9fb4cc"], [
            fondo("bg_alpes_nieve"),
            pie(n, 540, SN, 700, z=0.6, keys=[{"t": 0, "x": 480}, {"t": d, "x": 600}] + mk),
            *[onda(540, 640, tg + 0.02, 140, "#ffffff", 0.5, 8) for tg in golpes],
            *piedras,
            *huellas(-600, 400, -1, -1, SN, d),
            pie("p2_piedra_b", 1350, SN, 200, z=0.5), pie("p2_piedra_a", -350, SN, 160, z=0.5),
            {**polvo("#ffffff", 50, (-600, 350, 1700, 1400), 381, "nieve"), "vel": [20, 60]}],
            cam(1.08, 1.12, (540, 1000), temblor=0), "corte",
            sfx=[(tg, "golpe", -12) for tg in golpes])

    @plano(389, "prueba: Marta sube la persiana")
    def _(d):
        fx_, fa = 540, 720
        fw = fa * 900 / 820
        x0 = fx_ - fw / 2 + PERSIANA["x0"] * fw / 900 + PERSIANA["w"] * fw / 900 / 2
        ytop = ypie("cafeteria_marta", SD, fa) - fa / 2
        yc = ytop + (PERSIANA["y0"] + PERSIANA["h"] / 2) * fa / 820
        ph = PERSIANA["h"] * fa / 820
        return P(DIA, [
            fondo("bg_calle_dia"),
            tienda("cafeteria_marta", fx_, SD, fa, z=0.4),
            pieza("persiana", round(x0), round(yc), round(PERSIANA["w"] * fw / 900), z=0.41,
                  keys=[{"t": 0, "y": yc, "ey": 1.0}, {"t": d * 0.8, "y": yc - ph / 2 + 20, "ey": 0.08, "ease": "suave"}]),
            pie("marta_delantal", 1000, SD, 640, z=0.55, keys=late(d * 0.5, 1, 0.05)),
            pieza("cartel_abierto", 80, 760, 170, z=0.6, keys=aparece(d * 0.55, 0.3)),
            pie("voluntario_2", -500, SD, 600, z=0.45), pie("voluntario_5", 1600, SD, 600, z=0.45)],
            cam(1.0, 1.06, (540, 1000)), "corte", sfx=[(0.05, "roce", -18, {"dur": 0.6}), (d * 0.55, "pop", -22)])

    @plano(390, "se equivoca: el cliente se va")
    def _(d):
        return P(["#5a4a3a", "#1a1410"], [
            fondo("bg_cafe_dentro_triste"),
            pie("marta_triste", 380, SF, 680, z=0.55, keys=mece(d, 1.5, 1.4)),
            *camina("cliente_se_va", 640, 1400, SF, 640, d, fps=3.5, z=0.6),
            *aspa(1150, 700, 110, d * 0.45, z=0.9),
            pie("cliente_confuso_2", -400, SF, 620, z=0.5)],
            cam(1.05, 1.1, (700, 1000)), "corte", sfx=[(0.1, "roce", -26), (d * 0.45, "zap", -20)])

    @plano(392, "gasta: la hucha se rompe")
    def _(d):
        mon = [pieza("monedas", 540, 1150, 160, z=0.62, keys=[{"t": 0, "op": 0}, {"t": 0.15, "op": 1, "x": 540, "y": 1150},
                                                              {"t": 0.6, "x": 540 + dx, "y": 1350, "rot": dx / 3, "op": 0.0, "ease": "entrada"}])
               for dx in (-420, -160, 200, 460)]
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"), foco(540, SE),
            pie("hucha", 540, SE - 20, 420, z=0.6, keys=[{"t": 0, "op": 1}, {"t": 0.12, "op": 1}, {"t": 0.13, "op": 0}]),
            pie("hucha_rota", 540, SE - 20, 380, z=0.6, keys=[{"t": 0, "op": 0}, {"t": 0.12, "op": 0}, {"t": 0.13, "op": 1}]),
            *mon],
            cam(1.05, 1.15, (540, 1150), temblor=0), "corte",
            hud=[contador(0.1, d - 0.05, 3000, 0, 0.5, " €", tam=110, x=540, y=600, color="#ffffff", capsula="#c0392be6", miles=True)],
            sfx=[(0.12, "golpe", -12), (0.25, "tic", -22)])

    @plano(393, "y el que viene detrás: Lucas por el camino abierto")
    def _(d):
        return P(["#dfeaf6", "#9fb4cc"], [
            fondo("bg_alpes_nieve"),
            *huellas(-600, 1500, -1, -1, SN, d, paso=100),
            pie("marta_camina_a", 1450, SN - 60, 300, z=0.4, keys=[pos("marta_camina_a", 1350, SN - 60, 300), {**pos("marta_camina_a", 1480, SN - 60, 300), "t": d}]),
            *camina("lucas_camina", -350, 250, SN, 640, d, fps=3.5, z=0.6),
            pie("p2_piedra_a", 600, SN + 40, 150, z=0.5), pie("p2_piedra_b", 900, SN + 30, 130, z=0.5), pie("p2_piedra_a", 1150, SN + 30, 120, z=0.5),
            {**polvo("#ffffff", 40, (-600, 350, 1700, 1400), 393, "nieve"), "vel": [20, 50]}],
            cam(1.0, 1.05, (300, 1050), (500, 1050)), "corte", sfx=[(0.3, "roce", -28), (0.8, "roce", -28)])

    @plano(398, "aprende gratis de sus errores: esquiva las piedras")
    def _(d):
        o = rel(398)
        return P(["#dfeaf6", "#9fb4cc"], [
            fondo("bg_alpes_nieve"),
            *huellas(-600, 1600, -1, -1, SN, d, paso=100),
            *camina("lucas_camina", 150, 900, SN, 700, d, fps=3.0, z=0.6),
            pie("p2_piedra_a", 540, SN + 60, 220, z=0.65), pie("p2_piedra_b", 1250, SN + 50, 200, z=0.65), pie("p2_piedra_a", -350, SN + 40, 180, z=0.65),
            flecha([[380, 1500], [540, 1320], [700, 1500]], 0.2, 0.9, CIAN, 7, [20, 12], z=0.7),
            {**polvo("#ffffff", 40, (-600, 350, 1700, 1400), 398, "nieve"), "vel": [20, 50]}],
            cam(1.05, 1.12, (450, 1050), (750, 1000)), "corte",
            hud=[amarillo(o(399), d - 0.05, "GRATIS", y=520, tam=120, color="#ffd23f")],
            sfx=[(o(399), "ding", -20)])

    # ================================================================== EN TU MÓVIL (403–490)
    @plano(403, "y esto no pasa solo en tu barrio: la ciudad se abre")
    def _(d):
        return P(NOCHE, [
            fondo("bg_ciudad"), *ciudad_noche(d, 403),
            tienda("hamburgueseria_lucas", 300, SC, 600, z=0.4), tienda("hamburgueseria_lucas", 1100, SC, 600, z=0.4),
            tienda("cafeteria_marta_cerrada", -450, SC, 600, z=0.4), tienda("hamburgueseria", 1650, SC, 600, z=0.4),
            *cola(180, SC, n=3, alto=470, paso=105, z=0.45), *cola(980, SC, n=3, alto=470, paso=105, z=0.45)],
            cam(1.45, 1.0, (700, 1100), (560, 1000)), "corte", sfx=[(0.05, "subida", -24, {"dur": d})])

    @plano(411, "pasa en el móvil que tienes en la mano")
    def _(d):
        sx, sy = 540, 1060
        k = 760 / 560
        cy = sy + (340 - 470) * k
        ic = [("app_buscador", -1, -1), ("app_red", 1, -1), ("app_fantasma_generico", -1, 1), ("app_buscador_viejo_1", 1, 1)]
        apps = [pieza(n, round(sx + 85 * i), round(cy - 60 + 170 * j), 130, z=0.62,
                      keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.5 + 0.12 * q, "op": 0, "escala": 0.2}, {"t": 0.8 + 0.12 * q, "op": 1, "escala": 1.0, "ease": "rebote"}])
                for q, (n, i, j) in enumerate(ic)]
        sube = [{"t": 0, "y": sy + 700}, {"t": 0.45, "y": sy, "ease": "elastico"}, {"t": d, "y": sy - 30}]
        return P(["#3a3f5a", "#14162a"], [
            fondo("bg_habitacion"),
            {"tipo": "forma", "forma": "rect", "ancho": 2600, "alto": 2400, "relleno": "#0b0d18", "x": 540, "y": 960, "z": 0.06, "op": 0.45},
            brillo(sx, cy, 420, "#bfe0ff", 0.55, 0.3, keys=[{"t": 0, "op": 0}, {"t": 0.5, "op": 1}]),
            pieza("movil_mano", sx, sy, 760, z=0.6, keys=sube),
            *[{**a, "keys": a["keys"] + [{"t": 0, "y": a["y"] + 700}, {"t": 0.45, "y": a["y"], "ease": "elastico"}, {"t": d, "y": a["y"] - 30}]} for a in apps]],
            cam(1.0, 1.06, (540, 950)), "corte", sfx=[(0.05, "whoosh", -20), (0.5, "senal", -24)] + [(0.8 + 0.12 * q, "pop", -26) for q in range(4)])

    @plano(420, "Google no fue el primer buscador: los de antes")
    def _(d):
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"), foco(140, SE, 1400, True), foco(940, SE, 1400, True, op=0.4),
            pieza("app_buscador_viejo_1", -250, 900, 380, z=0.55, keys=aparece(0.1) + [{"t": d, "y": 880}]),
            pieza("app_buscador_viejo_2", 330, 900, 380, z=0.55, keys=aparece(0.4) + [{"t": d, "y": 880}]),
            {"tipo": "forma", "forma": "redondeado", "ancho": 380, "alto": 380, "esquinas": 76, "relleno": "#ffffff", "op_relleno": 0.04,
             "grosor": 6, "borde": "#ffffff55", "x": 910, "y": 900, "z": 0.5, "keys": [{"t": 0, "escala": 1.0}] + late(d * 0.6, 2, 0.06)},
            flecha([[-500, 1150], [1350, 1150]], 0.05, d * 0.8, "#ffffff88", 6, z=0.45)],
            cam(1.0, 1.05, (300, 950)), "corte",
            hud=[rotulo(0.1, d * 0.55, "GOOGLE", tam=84, color="#ffffff", capsula="#1b2233e6", x=910, y=600),
                 rotulo(0.25, d - 0.05, "1º", tam=70, color="#ffffff", capsula=None, x=-250, y=1240),
                 rotulo(0.55, d - 0.05, "2º", tam=70, color="#ffffff", capsula=None, x=330, y=1240)],
            sfx=[(0.1, "pop", -24), (0.4, "pop", -24)])

    @plano(426, "llegó cuando ya había otros: entra el buscador nuevo")
    def _(d):
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"), foco(940, SE, 1400, True),
            pieza("app_buscador_viejo_1", -250, 900, 380, z=0.55, keys=K(d, (0, {"rot": 0}), (0.4, {"rot": -4}), (1, {"rot": 0}))),
            pieza("app_buscador_viejo_2", 330, 900, 380, z=0.55, keys=K(d, (0, {"rot": 0}), (0.4, {"rot": 4}), (1, {"rot": 0}))),
            pieza("app_buscador", 910, 900, 380, z=0.6, keys=lanza(0.05, 0.6, (1900, 900), (910, 900))),
            brillo(910, 900, 320, CIAN, 0.5, 0.5, keys=[{"t": 0, "op": 0}, {"t": 0.6, "op": 1}]),
            flecha([[-500, 1150], [1350, 1150]], 0.0, 0.01, "#ffffff88", 6, z=0.45)],
            cam(1.05, 1.08, (500, 950), (600, 950)), "corte",
            hud=[rotulo(0.65, d - 0.05, "3º", tam=70, color="#ffffff", capsula=None, x=910, y=1240)],
            sfx=[(0.05, "whoosh", -20), (0.6, "golpe", -22)])

    @plano(431, "y encontraba mejor las cosas: la lupa atrae lo que buscas")
    def _(d):
        cosas = [("hamburguesa", -500, 500), ("balon_futbol", 1600, 520), ("guitarra", -450, 1300), ("libro_recetas", 1600, 1300), ("taza_cafe_latte", 540, 300)]
        vuelan = [pieza(n, x, y, 210, z=0.65, keys=[{"t": 0, "x": x, "y": y, "op": 1, "escala": 1.0}, {"t": 0.6 + 0.3 * i, "x": x, "y": y},
                                                   {"t": 1.1 + 0.3 * i, "x": 500, "y": 880, "escala": 0.3, "op": 0, "ease": "entrada"}])
                  for i, (n, x, y) in enumerate(cosas)]
        return P(["#0d1a2a", "#05070c"], [
            fondo("bg_estudio_oscuro"), foco(540, SE, 1600, True),
            pieza("app_buscador_viejo_1", -300, 1150, 200, z=0.4, keys=K(d, (0, {"op": 0.9}), (0.5, {"op": 0.25, "x": -450}))),
            pieza("app_buscador_viejo_2", 1400, 1150, 200, z=0.4, keys=K(d, (0, {"op": 0.9}), (0.5, {"op": 0.25, "x": 1550}))),
            brillo(540, 920, 420, CIAN, 0.55, 0.45, pulso=[0.08, 0.7]),
            pieza("app_buscador", 540, 920, 420, z=0.6, keys=[{"t": 0, "escala": 1.0}, {"t": 0.5, "escala": 1.35, "ease": "elastico"}] + late(1.5, 3, 0.05)),
            *vuelan],
            cam(1.0, 1.06, (540, 950)), "corte",
            sfx=[(0.3, "subida", -24)] + [(1.1 + 0.3 * i, "burbuja", -22) for i in range(5)])

    @plano(437, "Facebook no fue la primera red social: las viejas")
    def _(d):
        viejas = [pieza("app_red_vieja", x, y, 290, z=0.5, op=0.85, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.1 + 0.15 * i, "op": 0, "escala": 0.3},
                                                                          {"t": 0.35 + 0.15 * i, "op": 0.85, "escala": 1.0, "ease": "rebote"}, {"t": d, "y": y - 20, "rot": r}])
                  for i, (x, y, r) in enumerate([(-350, 760, -6), (200, 620, 4), (880, 640, -3), (1420, 780, 6)])]
        return P(["#3a3f5a", "#14162a"], [
            fondo("bg_habitacion"),
            {"tipo": "forma", "forma": "rect", "ancho": 2600, "alto": 2400, "relleno": "#0b0d18", "x": 540, "y": 960, "z": 0.06, "op": 0.35},
            *viejas,
            pie("voluntario_2", 540, SH, 640, z=0.55, keys=mece(d, 1.5, 1.6)),
            pie("voluntario_4", 1100, SH, 620, z=0.55, keys=mece(d, 1.5, 2.0)),
            pie("voluntario_5", -40, SH, 620, z=0.55, keys=mece(d, 1.5, 1.8))],
            cam(1.0, 1.06, (540, 950)), "corte",
            hud=[rotulo(0.1, d - 0.05, "FACEBOOK", tam=84, color="#ffffff", capsula="#2a4a9ae6", x=540, y=400)],
            sfx=[(0.35 + 0.15 * i, "pop", -26) for i in range(4)])

    @plano(444, "llegó cuando ya había otras: la red nueva cae entre las grises")
    def _(d):
        return P(["#3a3f5a", "#14162a"], [
            fondo("bg_habitacion"),
            {"tipo": "forma", "forma": "rect", "ancho": 2600, "alto": 2400, "relleno": "#0b0d18", "x": 540, "y": 960, "z": 0.06, "op": 0.45},
            *[pieza("app_red_vieja", x, 1000, 300, z=0.5, op=0.8, keys=[{"t": 0, "rot": 0}, {"t": 0.62, "rot": 0}, {"t": 0.7, "rot": r, "y": 990}, {"t": 1.0, "rot": 0, "y": 1000, "ease": "elastico"}])
              for x, r in [(-420, -8), (-60, -5), (1140, 5), (1500, 8)]],
            pieza("app_red", 540, 1000, 420, z=0.6, keys=[{"t": 0, "y": 200, "op": 1}] + cae(0.1, 0.7, 200, 1000)[1:]),
            brillo(540, 1000, 300, "#6a9aff", 0.55, 0.45, keys=[{"t": 0, "op": 0}, {"t": 0.6, "op": 1}]),
            onda(540, 1000, 0.62, 260, "#6a9aff")],
            cam(1.0, 1.05, (540, 1000)), "corte", sfx=[(0.55, "golpe", -16)])

    @plano(449, "y lo hizo más fácil: un camino recto a tus amigos")
    def _(d):
        return P(["#3a3f5a", "#14162a"], [
            fondo("bg_habitacion"),
            {"tipo": "forma", "forma": "rect", "ancho": 2600, "alto": 2400, "relleno": "#0b0d18", "x": 540, "y": 960, "z": 0.06, "op": 0.3},
            pieza("app_red_vieja", -380, 620, 200, z=0.5, op=0.7),
            flecha([[-380, 740], [-250, 820], [-450, 900], [-200, 980], [-420, 1060], [-150, 1140]], 0.05, d * 0.9, "#9aa3b0aa", 6, z=0.48),
            pieza("app_red", 260, 640, 340, z=0.6, keys=late(0.15, 2, 0.1)),
            flecha([[450, 700], [960, 880]], 0.3, 0.75, CIAN, 10, z=0.58),
            pie("padres_hablan", 1100, SH, 640, z=0.55, keys=aparece(0.7) + [{"t": d, "escala": 1.0}]),
            pie("cliente_feliz_2", 1550, SH, 620, z=0.52, keys=mece(d, 2.0, 1.2))],
            cam(1.0, 1.05, (540, 950)), "corte", sfx=[(0.15, "pop", -22), (0.75, "ding", -22)])

    def historias_xy(cx, cy, ancho):
        k = ancho / 1100
        return [(round(cx + (120 + 215 * i - 550) * k), round(cy + (125 - 130) * k)) for i in range(5)], 95 * k

    @plano(454, "las historias que subes cada día")
    def _(d):
        cx, cy, an = 540, 820, 1500
        pts, r = historias_xy(cx, cy, an)
        return P(["#3a3f5a", "#14162a"], [
            fondo("bg_habitacion"),
            {"tipo": "forma", "forma": "rect", "ancho": 2600, "alto": 2400, "relleno": "#0b0d18", "x": 540, "y": 960, "z": 0.06, "op": 0.55},
            pieza("app_historias", cx, cy, an, z=0.55, keys=K(d, (0, {"escala": 0.9}), (1, {"escala": 1.0}))),
            *[senala(x, y, 0.2 + 0.3 * i, 0.5 + 0.3 * i, round(r * 1.15), [MAGENTA, AMBAR, CIAN, LIMA, MAGENTA][i]) for i, (x, y) in enumerate(pts)],
            pie("voluntario_3", 540, SH + 40, 560, z=0.6, keys=mece(d, 1.5, 1.5)),
            pie("voluntario_1", -400, SH, 600, z=0.55), pie("voluntario_6", 1500, SH, 600, z=0.55)],
            cam(1.0, 1.05, (540, 900)), "corte", sfx=[(0.2 + 0.3 * i, "tic", -26) for i in range(5)])

    @plano(461, "Instagram las copió: la flecha de copia")
    def _(d):
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"), foco(-150, SE, 1400), foco(1080, SE, 1400, True),
            pieza("app_fantasma_generico", -150, 900, 420, z=0.55, keys=K(d, (0, {"rot": -3}), (1, {"rot": 3}))),
            pieza("app_historias", 1080, 900, 940, z=0.55, keys=[{"t": 0, "op": 0.0, "x": 300, "escala": 0.5}, {"t": 0.5, "op": 1.0, "x": 1080, "escala": 1.0, "ease": "salida"}]),
            flecha([[110, 900], [560, 900]], 0.1, 0.5, MAGENTA, 10, [22, 14], z=0.6)],
            cam(1.0, 1.05, (500, 950)), "corte",
            hud=[rotulo(0.1, d - 0.05, "INSTAGRAM", tam=80, color="#ffffff", capsula="#8a2a7ae6", x=1080, y=640)],
            sfx=[(0.1, "whoosh", -22)])

    @plano(465, "de Snapchat: el icono amarillo")
    def _(d):
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"), foco(540, SE, 1500),
            brillo(540, 900, 360, "#ffe93d", 0.5, 0.3, pulso=[0.1, 0.5]),
            pieza("app_fantasma_generico", 540, 900, 460, z=0.6, keys=[{"t": 0, "escala": 0.9}] + late(0.1, 2, 0.08)),
            senala(540, 900, 0.05, d, 300, AMBAR)],
            cam(1.0, 1.08, (540, 900)), "corte",
            hud=[rotulo(0.05, d - 0.05, "SNAPCHAT", tam=80, color="#1b1b1b", capsula="#ffe93df0", x=540, y=1250)],
            sfx=[(0.05, "pop", -20)])

    @plano(466, "pero tus amigos ya estaban en Instagram: las caras")
    def _(d):
        cx, cy, an = 540, 640, 1400
        pts, r = historias_xy(cx, cy, an)
        amigos = ["cliente_feliz_1", "voluntario_2", "cliente_feliz_3", "voluntario_5", "cliente_feliz_2"]
        gente, rayas = [], []
        for i, ((x, y), n) in enumerate(zip(pts, amigos)):
            t0 = 0.3 + 0.22 * i
            gente.append(pie(n, x, SH, 560, z=0.55 + 0.005 * i, keys=aparece(t0) + mece(d, 1.5, 1.4 + 0.2 * i)[1:]))
            rayas.append(flecha([[x, y + r + 10], [x, 940]], t0 + 0.1, t0 + 0.35, [MAGENTA, AMBAR, CIAN, LIMA, MAGENTA][i], 6, punta=False, z=0.5))
        return P(["#3a3f5a", "#14162a"], [
            fondo("bg_habitacion"),
            {"tipo": "forma", "forma": "rect", "ancho": 2600, "alto": 2400, "relleno": "#0b0d18", "x": 540, "y": 960, "z": 0.06, "op": 0.5},
            pieza("app_historias", cx, cy, an, z=0.55),
            *[brillo(x, y, round(r * 1.6), "#ffd0f0", 0.45, 0.5, keys=[{"t": 0, "op": 0}, {"t": 0.3 + 0.22 * i, "op": 1}]) for i, (x, y) in enumerate(pts)],
            *rayas, *gente],
            cam(1.0, 1.05, (540, 950)), "corte", sfx=[(0.3 + 0.22 * i, "pop", -26) for i in range(5)])

    @plano(473, "en un año: el reloj de arena gira")
    def _(d):
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"), foco(540, SE, 1500),
            pieza("reloj_arena_grande", 540, 900, 300, z=0.6, keys=[{"t": 0, "rot": 0}, {"t": d * 0.8, "rot": 180, "ease": "elastico"}]),
            brillo(540, 900, 300, "#ffcf8a", 0.4, 0.3)],
            cam(1.0, 1.1, (540, 920)), "corte",
            hud=[contador(0.02, d - 0.02, 1, 12, d * 0.6, " MESES", tam=80, x=540, y=1260, color="#ffffff", capsula="#1b2233e6", miles=False)],
            sfx=[(0.05, "whoosh", -24)])

    @plano(476, "más gente que Snapchat entero: la barra de historias la supera")
    def _(d):
        o = rel(476)
        base = 1250
        tb = max(0.6, o(481) - 0.2)
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"), foco(320, SE, 1400, op=0.6), foco(760, SE, 1400, True),
            barra(320, base, 260, 560, ["#fff07a", "#d8b400"], 0.1, 0.7, z=0.5),
            barra(760, base, 260, 780, ["#ff7ad8", "#8a3aff"], 0.3, tb + 0.5, z=0.5),
            flecha([[150, base - 560], [930, base - 560]], 0.7, 0.9, "#ffffffaa", 5, [16, 12], punta=False, z=0.55),
            pieza("app_fantasma_generico", 320, base + 120, 170, z=0.6),
            pieza("app_historias", 760, base + 120, 420, z=0.6),
            pieza("destello", 760, base - 780, 240, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": tb + 0.5, "op": 0, "escala": 0.2},
                                                                 {"t": tb + 0.65, "op": 1, "escala": 1.0, "ease": "salida"}, {"t": tb + 1.1, "op": 0}]),
            *[pie(n, x, SE, 600, z=0.45) for n, x in [("voluntario_1", -420), ("cliente_feliz_1", 1480), ("voluntario_6", 1700)]]],
            cam(1.0, 1.05, (540, 950)), "corte",
            sfx=[(0.1, "subida", -22, {"dur": tb + 0.4}), (tb + 0.55, "ding", -18)])

    @plano(483, "ninguno inventó la idea: la bombilla tachada")
    def _(d):
        ic = [("app_buscador", 0), ("app_red", 540), ("app_fantasma_generico", 1080)]
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"),
            pieza("bombilla_a", 540, 620, 280, z=0.55, keys=K(d, (0, {"rot": -5}), (1, {"rot": 5}))),
            *aspa(540, 620, 150, 0.4, z=0.8),
            *[pieza(n, x, 1020, 340, z=0.6, keys=aparece(0.05 + 0.1 * i)) for i, (n, x) in enumerate(ic)],
            pieza("app_historias", 540, 1330, 700, z=0.55, keys=aparece(0.35)),
            foco(-400, SE, 1400, op=0.4), foco(1500, SE, 1400, op=0.4)],
            cam(1.0, 1.05, (540, 950)), "corte", sfx=[(0.4, "zap", -20)])

    @plano(487, "todos la hicieron mejor: los tres brillan juntos")
    def _(d):
        ic = [("app_buscador", -160), ("app_red", 330), ("app_historias", 1130)]
        return P(["#2a1d40", "#07080c"], [
            fondo("bg_estudio_oscuro"),
            brillo(540, 950, 720, "#ffcf6a", 0.6, 0.2, keys=[{"t": 0, "op": 0.2}, {"t": 0.3, "op": 1}]),
            *[pieza(n, x, 950, 400 if n != "app_historias" else 900, z=0.6,
                    keys=[{"t": 0, "y": 1060, "escala": 0.85}, {"t": 0.35 + 0.08 * i, "y": 950, "escala": 1.05, "ease": "elastico"}] + late(0.9 + 0.12 * i, 1, 0.1))
              for i, (n, x) in enumerate(ic)],
            *[pieza("destello", x, 800, 200, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.4 + 0.12 * i, "op": 1, "escala": 1.0, "ease": "salida"},
                                                        {"t": 0.9 + 0.12 * i, "op": 0}]) for i, x in enumerate([-60, 430, 1300])],
            {**polvo("#ffd23f", 60, (-500, 400, 1600, 1400), 487), "vel": [10, -40]},
            pieza("icono_bonito", -520, 760, 200, z=0.5, keys=aparece(0.5)), pieza("icono_bonito", 1650, 760, 200, z=0.5, keys=aparece(0.6))],
            cam(1.0, 1.1, (540, 950)), "corte",
            hud=[rotulo(0.5, d - 0.05, "MEJOR", tam=110, color="#1b1b1b", capsula="#ffd23ff0", x=540, y=1300)],
            sfx=[(0.3, "brillo", -18), (0.9, "ding", -16)])
