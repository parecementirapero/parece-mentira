"""Parte 1 (palabras 0–246, 0–94,8 s): gancho, el colegio, el último timbre y la cafetería de Marta hasta la persiana.
Coordenadas del vertical (1080×1920); `adaptar` lo pasa a 16:9. Laterales (x<0, x>1080) llenos para el horizontal."""
import math, random
from comun_cp import *  # noqa: F401,F403
import comun

# ------------------------------------------------------------------ escalas comunes (misma escala para el mismo personaje)
U_NINO = 520 / 634      # px del vertical por unidad del lienzo de los niños sentados (todos acaban en y=861)
U_AD = 620 / 856        # px por unidad del lienzo de los adultos de ilus_gente
MANOS_NINO = 296        # unidades de lienzo entre los pies y las manos (mesa) de un niño sentado


def _alto(n, u):
    return comun.tam_svg(n)[1] * u


def nino(n, x, suelo=1420, esc=1.0, z=0.5, keys=None, **k):
    """Niño sentado en su silla (los pies en `suelo`)."""
    return pie(n, x, suelo, round(_alto(n, U_NINO) * esc), z=z, keys=keys, **k)


def mesa(x, suelo=1420, esc=1.0, doble=False, z=0.56, keys=None, **k):
    """Pupitre delante del niño: el borde de atrás del tablero justo a la altura de sus manos (se le ve el papel)
    y las patas un poco más cerca de la cámara que los pies del niño."""
    n = "pupitre_doble" if doble else "pupitre"
    hp = 300 * esc
    w_, h_ = comun.tam_svg(n)
    arriba = suelo - MANOS_NINO * U_NINO * esc - 6 * esc
    return pieza(n, x, round(arriba + hp / 2), round(hp * w_ / h_), z=z, keys=keys, **k)


def adulto(n, x, suelo, esc=1.0, z=0.5, keys=None, **k):
    return pie(n, x, suelo, round(_alto(n, U_AD) * esc), z=z, keys=keys, **k)


def cabeza(n, suelo, esc=1.0):
    """y de lo alto de la cabeza de un adulto de ilus_gente posado en `suelo`."""
    a = _alto(n, U_AD) * esc
    return suelo - comun.APOYO.get(n, 0.97) * a


def andar(pref, x0, x1, suelo, d, esc=1.0, z=0.5, fps=4, ex=1, alto=None):
    """Personaje que camina (fotogramas _a/_b) de x0 a x1 durante el plano."""
    def base(n):
        a = alto or round(_alto(n, U_AD) * esc)
        return pie(n, x0, suelo, a, z=z, ex=ex, keys=[{"t": 0, "x": x0}, {"t": d, "x": x1, "ease": "lineal"}])
    return flip([pref + "_a", pref + "_b"], d, fps=fps, base=base)


def mece(d, amp=3, periodo=2.4, base=0):
    """Balanceo suave (rot) para que una figura quieta respire (el `mecer` de comun_cp usa «giro», que el motor no anima)."""
    ks, t, sg = [], 0.0, 1
    while t <= d + periodo:
        ks.append({"t": round(t, 3), "rot": base + sg * amp, "ease": "suave"})
        t += periodo / 2; sg = -sg
    return ks


def aspa(cx, cy, r, t0, color=ROJO, g=22, z=0.8):
    return [flecha([[cx - r, cy - r], [cx + r, cy + r]], t0, t0 + 0.16, color, g, punta=False, z=z),
            flecha([[cx + r, cy - r], [cx - r, cy + r]], t0 + 0.14, t0 + 0.3, color, g, punta=False, z=z)]


def onda(x, y, t0, r=160, color=CIAN, dur=0.8, g=6, z=0.7):
    return {"tipo": "forma", "forma": "elipse", "ancho": r * 2, "alto": r * 2, "relleno": "#ffffff", "op_relleno": 0,
            "grosor": g, "borde": color, "x": x, "y": y, "z": z,
            "keys": [{"t": 0, "escala": 0.15, "op": 0}, {"t": t0, "escala": 0.15, "op": 0}, {"t": t0 + 0.05, "op": 0.9},
                     {"t": t0 + dur, "escala": 1.0, "op": 0.0, "ease": "salida"}]}


def lados_aula(sem=1, z=0.5):
    """Más pupitres y mochilas a los lados del aula (solo se ven en el horizontal)."""
    r = random.Random(sem)
    out = []
    for x in (-470, 1550):
        out.append(mesa(x + r.uniform(-30, 30), 1420, 1.0, z=z))
        out.append(pie("mochila_cole", x + 260 * (1 if x < 0 else -1), 1430, 150, z=z + 0.02, rot=r.uniform(-8, 8)))
    return out


def lados_calle(sem=1, z=0.45, suelo=1440):
    """Gente de paso a los lados de la calle (solo horizontal)."""
    r = random.Random(sem)
    gente = ["voluntario_1", "voluntario_2", "voluntario_4", "voluntario_5", "cliente_feliz_1", "cliente_feliz_3"]
    r.shuffle(gente)
    out = []
    for x, n in zip((-560, -330, 1420, 1640), gente):
        alto = 560 if n.startswith("voluntario") else round(_alto(n, U_AD) * 0.92)
        out.append(pie(n, x + r.uniform(-30, 30), suelo, alto, z=z, keys=mece(8, 1.2, 2.6 + r.uniform(0, 0.6))))
    return out


def fachada_geo(x, suelo, alto):
    """Escala y esquina de arriba a la izquierda de una fachada 900×820 posada con `pie`."""
    s = alto / 820
    yc = suelo - (comun.APOYO.get("cafeteria_marta", 0.988) - 0.5) * alto
    return s, x - 450 * s, yc - alto / 2


def persiana_baja(x, suelo, alto, t0, t1, hasta=1.0, z=0.56, ease="entrada"):
    """La persiana baja de verdad sobre el hueco de `cafeteria_marta` (crece hacia abajo con el borde de arriba fijo)."""
    s, izq, arr = fachada_geo(x, suelo, alto)
    pw, ph = PERSIANA["w"] * s, PERSIANA["h"] * s
    px, ytop = izq + (PERSIANA["x0"] + PERSIANA["w"] / 2) * s, arr + PERSIANA["y0"] * s
    e0 = 0.03
    ks = [{"t": 0, "ey": e0, "y": round(ytop + e0 * ph / 2, 1)}, {"t": t0, "ey": e0, "y": round(ytop + e0 * ph / 2, 1)},
          {"t": t1, "ey": hasta, "y": round(ytop + hasta * ph / 2, 1), "ease": ease}]
    return pieza("persiana", round(px, 1), round(ytop, 1), round(pw), z=z, keys=ks)


def ruido_persiana(t0, t1):
    n = max(3, int((t1 - t0) / 0.12))
    return [(t0, "tictac", -19, {"dur": t1 - t0, "ritmo": 0.035})] + \
           [(t0 + (t1 - t0) * i / n, "roce", -20 - (i % 2) * 2) for i in range(n)] + [(t1, "golpe", -13)]


def timbre_sfx(t0, dur=1.2):
    out = [(t0, "tictac", -18, {"dur": dur, "ritmo": 0.03})]
    for i in range(int(dur / 0.22)):
        out.append((t0 + i * 0.22, "ding", -22, {"f": 1320 if i % 2 else 1480}))
    return out


AULA = ["#f3e6c8", "#a07a50"]
CALLE = ["#9fd0f0", "#d8d0c4"]
OSCURO = ["#1c1f2a", "#08090d"]
CAFE = ["#2f5a52", "#6a4428"]


def planos(v, plano):
    w = v.w

    def rel(i0):
        return lambda j: round(w(j) - w(i0), 3)

    # ================================================================== GANCHO (0–9,7 s)
    @plano(0, "gancho: Lucas niño copia de reojo")
    def _(d):
        # fotograma 0 ya en movimiento: cámara entrando, Lucas inclinándose hacia el papel de Marta, flecha que se dibuja
        return P(AULA, [
            fondo("bg_aula"),
            brillo(760, 1150, 260, "#fff3d6", 0.5, 0.3, pulso=[0.1, 0.8]),
            nino("lucas_nino_reojo", 330, keys=[{"t": 0, "rot": -3, "x": 300}, {"t": 0.35, "rot": 5, "x": 345, "ease": "elastico"},
                                                 {"t": d, "rot": 6, "x": 352}]),
            *flip(["marta_nina_escribe_a", "marta_nina_escribe_b"], d, fps=7, base=lambda n: nino(n, 760)),
            mesa(540, doble=True),
            flecha([[400, 1000], [560, 1060], [700, 1150]], 0.0, 0.5, ROJO, 8, [18, 12], z=0.7),
            senala(735, 1170, 0.45, d, 95, ROJO),
            *lados_aula(1),
            {**polvo("#fff3d6", 30, (-400, 500, 1500, 1400), 1), "_ancho": False}],
            cam(1.5, 1.7, (560, 1100), (600, 1120)), vineta=0.6,
            sfx=[(0.02, "roce", -18), (0.45, "trazo", -22)])

    @plano(3, "gancho: el examen copiado")
    def _(d):
        return P(AULA, [
            fondo("bg_aula"),
            brillo(560, 980, 420, "#fff3d6", 0.45, 0.2),
            pieza("p1_examen_blanco", 600, 980, 560, z=0.5, keys=[{"t": 0, "rot": -12, "y": 1080, "x": 640},
                                                                   {"t": 0.35, "rot": -4, "y": 980, "x": 600, "ease": "salida"},
                                                                   {"t": d, "rot": -2, "y": 970}]),
            pieza("cara_lucas_listo", 110, 1250, 560, z=0.6, keys=[{"t": 0, "x": -150}, {"t": 0.4, "x": 90, "ease": "salida"}, {"t": d, "x": 120}]),
            pieza("cara_lucas_listo", 1500, 1000, 600, z=0.4, op=0.0),
            pieza("cuaderno_dibujo", -420, 1100, 420, z=0.45, rot=-14),
            pieza("hoja_dibujo", 1450, 950, 420, z=0.45, rot=10)],
            cam(1.0, 1.08, (560, 1000)), "corte", sfx=[(0.05, "roce", -20)])

    @plano(7, "gancho: suspenso (la nota roja se estampa)")
    def _(d):
        ex, ey, A = 560, 990, 640
        nx, ny = ex + 117.7 / 560 * A, ey - 240.3 / 560 * A
        return P(AULA, [
            fondo("bg_aula"),
            brillo(nx, ny, 300, ROJO, 0.4, 0.3, keys=[{"t": 0, "op": 0}, {"t": 0.22, "op": 0}, {"t": 0.3, "op": 1}, {"t": d, "op": 0.4}]),
            pieza("p1_examen_blanco", ex, ey, A, z=0.5, keys=[{"t": 0, "rot": -2}, {"t": d, "rot": 0, "escala": 1.03}]),
            pieza("p1_nota_roja", round(nx), round(ny), round(220 / 560 * A), z=0.6,
                  keys=[{"t": 0, "escala": 3.2, "op": 0, "rot": -30}, {"t": 0.08, "op": 0.6}, {"t": 0.26, "escala": 0.92, "op": 1, "rot": 0, "ease": "entrada"},
                        {"t": 0.4, "escala": 1.0, "ease": "elastico"}, {"t": d, "escala": 1.05}]),
            fundido_blanco([{"t": 0, "op": 0}, {"t": 0.25, "op": 0}, {"t": 0.28, "op": 0.5}, {"t": 0.5, "op": 0}], "#ffe0d8"),
            pieza("cuaderno_dibujo", -420, 1150, 420, z=0.45, rot=8), pieza("examen", 1480, 950, 380, z=0.45, rot=-9)],
            cam(1.12, 1.2, (600, 940)), "corte", sfx=[(0.24, "impacto", -12)])

    @plano(8, "gancho: en la vida real, Lucas con su local y su cola")
    def _(d):
        S = 1440
        return P(CALLE, [
            fondo("bg_calle_dia"),
            pie("hamburgueseria_lucas", 640, S, 600, z=0.4),
            *cola(500, S, n=10, alto=430, paso=100, z=0.5, avanza=(d * 0.5, 30)),
            adulto("lucas_delantal", 1040, S, 0.7, z=0.55, keys=mece(d, 1.5, 1.6)),
            brillo(640, 1150, 320, "#ffd9a0", 0.35, 0.3, pulso=[0.1, 1.2]),
            adulto("cliente_feliz_1", 1330, S, 0.7, z=0.45, keys=[{"t": 0, "x": 1300}, {"t": d, "x": 1420}]),
            adulto("cliente_feliz_3", 1560, S, 0.7, z=0.45, keys=mece(d, 1, 1.4)),
            {**polvo("#fff6e0", 24, (-400, 700, 1500, 1400), 8), "_ancho": False}],
            cam(1.25, 1.05, (700, 1150), (620, 1120)), "corte", sfx=[(0.05, "whoosh", -22)])

    @plano(12, "gancho: copiar bien (entrega la bolsa)")
    def _(d):
        S = 1440
        return P(CALLE, [
            fondo("bg_calle_dia"),
            pie("hamburgueseria_lucas", 160, S, 900, z=0.35),
            adulto("lucas_entrega", 420, S, z=0.55, keys=[{"t": 0, "x": 380}, {"t": 0.3, "x": 420, "ease": "salida"}]),
            adulto("cliente_feliz_2", 790, S, z=0.55, keys=[{"t": 0, "x": 840}, {"t": 0.35, "x": 790, "ease": "salida"}, {"t": d, "x": 780}]),
            *cola(1560, S, n=4, alto=600, paso=125, z=0.45),
            adulto("cliente_feliz_1", -500, S, 0.95, z=0.45, keys=[{"t": 0, "x": -460}, {"t": d, "x": -620}]),
            pieza("destello", 640, 1080, 160, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.35, "op": 0, "escala": 0.2},
                                                         {"t": 0.5, "op": 1, "escala": 1, "ease": "salida"}, {"t": 0.85, "op": 0}])],
            cam(1.3, 1.38, (600, 1120)), "corte", sfx=[(0.35, "pop", -20), (0.45, "brillo", -26)])

    @plano(14, "gancho: te puede hacer rico (dinero que sube)")
    def _(d):
        r = random.Random(14)
        billetes = []
        for i in range(9):
            x = r.uniform(-450, 1530); t0 = 0.05 + 0.1 * i
            billetes.append(pieza("billete", round(x), -200, 230, z=0.45 + 0.01 * i,
                                  keys=[{"t": 0, "y": -200, "rot": r.uniform(-40, 40)}, {"t": t0, "y": -200},
                                        {"t": t0 + 1.2, "y": r.uniform(1100, 1400), "rot": r.uniform(-90, 90), "ease": "suave"}]))
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"),
            pie("foco_luz", 540, 1400, 1300, z=0.1),
            brillo(540, 1150, 380, ORO, 0.55, 0.15, pulso=[0.15, 0.6]),
            *billetes,
            pie("saco_dinero", 540, 1400, 520, z=0.55, keys=cae(0.0, 0.45, 700, round(1400 - (0.944 - 0.5) * 520))),
            pie("monedas", 260, 1400, 140, z=0.56, keys=aparece(0.3)), pie("monedas", 830, 1400, 120, z=0.56, keys=aparece(0.4)),
            pie("monedas", -300, 1400, 160, z=0.5), pie("saco_dinero", 1400, 1400, 380, z=0.5)],
            cam(1.0, 1.1, (540, 1100)), "corte",
            hud=[contador(0.1, d - 0.05, 0, 250000, d * 0.8, " €", tam=120, x=540, y=600, color=ORO, capsula="#0b0f1ed8")],
            sfx=[(0.0, "subida", -18, {"dur": d}), (0.3, "golpe", -16), (d * 0.85, "ding", -20)])

    @plano(18, "gancho: pero hay una trampa")
    def _(d):
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"),
            brillo(540, 900, 520, ROJO, 0.45, 0.1, keys=[{"t": 0, "op": 0}, {"t": d * 0.4, "op": 1}]),
            pieza("cara_lucas_listo", 560, 1030, 900, z=0.5, keys=[{"t": 0, "escala": 1.0, "x": 600}, {"t": d, "escala": 1.08, "x": 560, "ease": "suave"}]),
            negro([{"t": 0, "op": 0.0}, {"t": d, "op": 0.35, "ease": "entrada"}]),
            pieza("examen", 1480, 900, 380, z=0.4, rot=12, op=0.6), pieza("saco_dinero", -520, 1150, 300, z=0.4, op=0.5)],
            cam(1.0, 1.12, (540, 900)), "corte",
            hud=[rotulo(d * 0.35, d - 0.05, "?", tam=300, color=ROJO, capsula=None, x=-120, y=760, rot=-8)],
            sfx=[(d * 0.35, "golpe", -18), (0.05, "rumor", -26, {"dur": d})])

    @plano(22, "gancho: te la cuento al final (la persiana amenaza)")
    def _(d):
        S, A = 1400, 620
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"),
            pie("foco_luz", 540, S, 1350, z=0.1),
            pie("cafeteria_marta", 540, S, A, z=0.4),
            persiana_baja(540, S, A, 0.15, d * 0.7, hasta=0.55, ease="suave"),
            negro([{"t": 0, "op": 0.15}, {"t": d, "op": 0.45}]),
            pie("hamburgueseria_vacia", -560, S, 520, z=0.3, op=0.6), pie("hamburgueseria", 1640, S, 520, z=0.3, op=0.6)],
            cam(1.15, 1.0, (540, 1150)), "corte",
            hud=[rotulo(d * 0.55, d - 0.05, "?", tam=260, color=ORO, capsula=None, x=860, y=640, rot=-8)],
            sfx=ruido_persiana(0.15, d * 0.7))

    # ================================================================== EL COLEGIO (9,7–37,4 s)
    @plano(28, "Esta es Marta")
    def _(d):
        return P(AULA, [
            fondo("bg_aula"),
            brillo(760, 1000, 320, "#fff3d6", 0.5, 0.3, pulso=[0.1, 1.0]),
            nino("lucas_nino_reojo", 330, op=0.85),
            nino("marta_nina_orgullosa", 760, keys=[{"t": 0, "rot": -2}, {"t": 0.4, "rot": 2, "ease": "elastico"}, {"t": d, "rot": 1}]),
            mesa(540, doble=True),
            *lados_aula(28),
            {**polvo("#fff3d6", 30, (-400, 500, 1500, 1400), 28), "_ancho": False}],
            cam(1.3, 1.45, (700, 1100), (760, 1090)), "corte",
            hud=[rotulo(0.1, d - 0.05, "MARTA", tam=96, color="#ffffff", capsula="#c98f1ee8", x=780, y=700)],
            sfx=[(0.1, "brillo", -26)])

    @plano(31, "y este es Lucas")
    def _(d):
        return P(AULA, [
            fondo("bg_aula"),
            brillo(330, 1000, 300, "#fff3d6", 0.4, 0.3),
            nino("lucas_nino_reojo", 330, keys=[{"t": 0, "rot": 0}, {"t": d * 0.5, "rot": 4, "ease": "suave"}, {"t": d, "rot": 1, "ease": "suave"}]),
            *flip(["marta_nina_escribe_a", "marta_nina_escribe_b"], d, fps=4, base=lambda n: nino(n, 760, op=0.85)),
            mesa(540, doble=True),
            *lados_aula(31)],
            cam(1.45, 1.45, (520, 1100), (340, 1100)), "corte",
            hud=[rotulo(0.25, d - 0.05, "LUCAS", tam=96, color="#ffffff", capsula="#2f6fb0e8", x=320, y=700)],
            sfx=[(0.0, "whoosh", -24)])

    @plano(35, "misma clase")
    def _(d):
        return P(AULA, [
            fondo("bg_aula"),
            nino("lucas_nino_reojo", 330, keys=mece(d, 1.5, 1.8)),
            *flip(["marta_nina_escribe_a", "marta_nina_escribe_b"], d, fps=4, base=lambda n: nino(n, 760)),
            mesa(540, doble=True),
            adulto("profesora_senala", -330, 1420, z=0.45, keys=mece(d, 1, 2.2)),
            pie("mochila_cole", 1180, 1430, 170, z=0.5, rot=-6),
            mesa(1550, z=0.5), pie("mochila_cole", -700, 1430, 150, z=0.5),
            brillo(300, 700, 300, "#fff3d6", 0.35, 0.2, pulso=[0.08, 1.4]),
            {**polvo("#fff3d6", 40, (-500, 400, 1600, 1400), 35), "_ancho": False}],
            cam(1.0, 1.08, (540, 1000)), "corte", sfx=[(0.05, "rumor", -28, {"dur": d})])

    @plano(37, "mismo pupitre")
    def _(d):
        return P(AULA, [
            fondo("bg_aula"),
            nino("lucas_nino_reojo", 330),
            *flip(["marta_nina_escribe_a", "marta_nina_escribe_b"], d, fps=5, base=lambda n: nino(n, 760)),
            mesa(540, doble=True),
            {"tipo": "forma", "forma": "elipse", "ancho": 900, "alto": 200, "relleno": "#ffffff", "op_relleno": 0, "grosor": 8,
             "borde": "#ff8a3d", "x": 540, "y": 1225, "z": 0.7,
             "keys": [{"t": 0, "escala": 1.4, "op": 0}, {"t": 0.15, "escala": 1.4, "op": 0}, {"t": 0.45, "escala": 1.0, "op": 1, "ease": "golpe"},
                      {"t": d, "escala": 1.04, "op": 1}]},
            *lados_aula(37)],
            cam(1.75, 1.6, (540, 1180)), "corte", sfx=[(0.4, "ding", -24)])

    @plano(39, "Marta lo hace todo sola")
    def _(d):
        return P(AULA, [
            fondo("bg_aula"),
            brillo(560, 1000, 360, "#fff3d6", 0.5, 0.3, pulso=[0.1, 1.2]),
            *flip(["marta_nina_escribe_a", "marta_nina_escribe_b"], d, fps=5, base=lambda n: nino(n, 560)),
            mesa(560),
            mesa(-60, z=0.5), mesa(1180, z=0.5), pie("mochila_cole", 1400, 1430, 150, z=0.52, rot=6),
            pieza("hoja_dibujo", 230, 1050, 170, z=0.58, rot=-8, keys=aparece(d * 0.5)),
            {**polvo("#fff3d6", 30, (-400, 500, 1500, 1400), 39), "_ancho": False}],
            cam(1.6, 1.75, (560, 1080)), "corte", sfx=[(0.1, "trazo", -26), (0.5, "trazo", -27), (1.0, "trazo", -26)])

    @plano(44, "sus dibujos son suyos")
    def _(d):
        return P(AULA, [
            fondo("bg_aula"),
            nino("marta_nina_orgullosa", 420, keys=[{"t": 0, "rot": 0}, {"t": 0.3, "rot": -3, "ease": "elastico"}, {"t": d, "rot": -2}]),
            mesa(420),
            pieza("hoja_dibujo", 820, 820, 430, z=0.6, keys=[{"t": 0, "op": 0, "escala": 0.3, "rot": -30, "x": 500, "y": 950},
                                                            {"t": 0.05, "op": 1}, {"t": 0.45, "escala": 1.0, "rot": 6, "x": 820, "y": 820, "ease": "salida"},
                                                            {"t": d, "rot": 3, "escala": 1.04}]),
            pieza("destello", 960, 680, 160, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.5, "op": 0, "escala": 0.2},
                                                         {"t": 0.65, "op": 1, "escala": 1, "ease": "salida"}, {"t": 1.0, "op": 0}]),
            pieza("hoja_dibujo", -350, 760, 300, z=0.4, rot=-8), pieza("hoja_dibujo", 1450, 760, 300, z=0.4, rot=7),
            *lados_aula(44)],
            cam(1.25, 1.35, (600, 1000)), "corte", sfx=[(0.05, "whoosh", -24), (0.6, "brillo", -24)])

    @plano(48, "sus redacciones son suyas: hojas que se apilan")
    def _(d):
        r = random.Random(48)
        hojas = []
        for i in range(4):
            t0 = 0.05 + 0.32 * i
            y1 = 1060 - 10 * i
            hojas.append(pieza("p1_examen_blanco", 540 + r.uniform(-30, 30), y1, 480, z=0.5 + 0.01 * i,
                               keys=[{"t": 0, "op": 0, "y": -300}, {"t": t0, "op": 0, "y": -300, "rot": r.uniform(-30, 30)},
                                     {"t": t0 + 0.02, "op": 1}, {"t": t0 + 0.35, "y": y1, "rot": r.uniform(-6, 6), "ease": "salida"}]))
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"),
            pie("foco_luz", 540, 1400, 1300, z=0.1),
            brillo(540, 1060, 400, "#fff3d6", 0.4, 0.15),
            *hojas,
            pieza("cuaderno_dibujo", -330, 1150, 420, z=0.4, rot=-10), pieza("hoja_dibujo", 1420, 1100, 400, z=0.4, rot=8)],
            cam(1.0, 1.1, (540, 1050)), "corte", sfx=[(0.3 + 0.32 * i, "roce", -24) for i in range(4)])

    @plano(52, "la profesora la pone de ejemplo")
    def _(d):
        hy = 1420 - 0.958 * _alto("marta_nina_orgullosa", U_NINO)
        return P(AULA, [
            fondo("bg_aula"),
            brillo(380, 900, 360, ORO, 0.45, 0.3, pulso=[0.15, 0.9]),
            nino("marta_nina_orgullosa", 380),
            mesa(380),
            *flip(["profesora_aplaude", "profesora_aplaude_b"], d, fps=5, base=lambda n: adulto(n, 860, 1420, z=0.5)),
            pieza("icono_bonito", 400, round(hy - 90), 190, z=0.7, keys=aparece(0.35) + late(0.9, 2, 0.12, 0.35)),
            nino("lucas_nino_triste", -280, z=0.45), mesa(-280, z=0.47),
            mesa(1550, z=0.5), pie("mochila_cole", 1300, 1430, 150, z=0.5)],
            cam(1.15, 1.25, (600, 1050)), "corte",
            sfx=[(0.1 + 0.2 * i, "pop", -26) for i in range(8)] + [(0.4, "brillo", -20)])

    @plano(59, "Lucas no")
    def _(d):
        return P(AULA, [
            fondo("bg_aula"),
            nino("lucas_nino_triste", 540, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": -3, "ease": "suave"}]),
            mesa(540),
            negro([{"t": 0, "op": 0.1}, {"t": d, "op": 0.35}]),
            mesa(-150, z=0.45), mesa(1250, z=0.45), pie("mochila_cole", 1500, 1430, 150, z=0.46)],
            cam(1.5, 1.7, (540, 1080)), "corte", vineta=0.8, sfx=[(0.05, "golpe", -24)])

    @plano(61, "Lucas mira de reojo")
    def _(d):
        top = 1420 - 0.956 * _alto("lucas_nino_reojo", U_NINO)
        return P(AULA, [
            fondo("bg_aula"),
            nino("lucas_nino_reojo", 480, keys=[{"t": 0, "rot": -2}, {"t": 0.3, "rot": 4, "ease": "elastico"}, {"t": d, "rot": 5}]),
            mesa(700, doble=True),
            flecha([[560, round(top + 70)], [760, round(top + 110)], [900, round(top + 200)]], 0.15, 0.6, ROJO, 7, [16, 10], z=0.7),
            *lados_aula(61)],
            cam(2.4, 2.6, (520, round(top + 120))), "corte", sfx=[(0.1, "roce", -22)])

    @plano(65, "al de al lado: el papel de Marta")
    def _(d):
        return P(AULA, [
            fondo("bg_aula"),
            nino("lucas_nino_reojo", 330, keys=[{"t": 0, "rot": 6}, {"t": d, "rot": 8}]),
            *flip(["marta_nina_escribe_a", "marta_nina_escribe_b"], d, fps=6, base=lambda n: nino(n, 760)),
            mesa(540, doble=True),
            flecha([[390, 1010], [560, 1060], [700, 1150]], 0.0, 0.35, ROJO, 8, [18, 12], z=0.7),
            senala(735, 1170, 0.3, d, 85, ROJO),
            *lados_aula(65)],
            cam(1.9, 2.05, (640, 1120)), "corte", sfx=[(0.3, "ding", -26)])

    @plano(69, "cuando lo pillan")
    def _(d):
        return P(AULA, [
            fondo("bg_aula"),
            nino("lucas_nino_pillado", 380, keys=[{"t": 0, "rot": 0}, {"t": 0.12, "rot": -4}, {"t": 0.3, "rot": 0, "ease": "elastico"}]),
            mesa(380),
            adulto("profesora_enfadada", 820, 1420, z=0.55, keys=[{"t": 0, "x": 1250}, {"t": 0.3, "x": 820, "ease": "anticipa"}]),
            mesa(1500, z=0.45), mesa(-400, z=0.45), pie("mochila_cole", -150, 1430, 150, z=0.46)],
            cam(1.2, 1.3, (600, 1050)), "corte",
            hud=[rotulo(0.3, d - 0.05, "!", tam=240, color=ROJO, capsula=None, x=640, y=640, rot=10)],
            sfx=[(0.25, "golpe", -14)])

    @plano(72, "suspenso")
    def _(d):
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"),
            pie("foco_luz_frio", 540, 1400, 1300, z=0.1),
            brillo(540, 950, 420, ROJO, 0.4, 0.15, keys=[{"t": 0, "op": 0}, {"t": 0.2, "op": 1}]),
            pieza("examen", 540, 960, 600, z=0.55, keys=[{"t": 0, "escala": 1.7, "rot": 20, "op": 0}, {"t": 0.04, "op": 1},
                                                         {"t": 0.2, "escala": 1.0, "rot": -3, "ease": "entrada"}, {"t": 0.35, "escala": 1.03, "ease": "elastico"},
                                                         {"t": d, "escala": 1.06, "rot": -2}]),
            pieza("examen", -360, 980, 400, z=0.4, rot=-14, op=0.5), pieza("examen", 1440, 960, 400, z=0.4, rot=12, op=0.5)],
            cam(1.05, 1.0, (540, 960), temblor=0.4), "corte", sfx=[(0.18, "impacto", -12)])

    @plano(73, "y castigo")
    def _(d):
        return P(AULA, [
            fondo("bg_aula"),
            nino("lucas_nino_triste", 760, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": -3}]),
            mesa(760),
            adulto("profesora_senala", 230, 1420, z=0.55, keys=[{"t": 0, "rot": -3}, {"t": 0.3, "rot": 0, "ease": "elastico"}]),
            negro([{"t": 0, "op": 0.0}, {"t": d, "op": 0.3}]),
            mesa(1500, z=0.45), mesa(-450, z=0.45)],
            cam(1.05, 1.2, (540, 1050), (640, 1050)), "corte", vineta=0.75, sfx=[(0.1, "golpe", -20)])

    @plano(75, "doce años: hojas de calendario que vuelan")
    def _(d):
        hojas = []
        r = random.Random(75)
        n = 11
        for i in range(n):
            t0 = 0.12 + i * (d * 0.75 / n)
            hojas.append(pieza("calendario_hoja", 540, 900, 520, z=0.6 - 0.01 * i,
                               keys=[{"t": 0, "x": 540, "y": 900, "rot": 0, "op": 1}, {"t": t0, "x": 540, "y": 900, "rot": 0},
                                     {"t": t0 + 0.5, "x": 540 + r.choice([-1, 1]) * r.uniform(700, 1100), "y": r.uniform(400, 800),
                                      "rot": r.uniform(-120, 120), "op": 0, "ease": "salida"}]))
        hojas.append(pieza("calendario_hoja", 540, 900, 520, z=0.45))
        return P(AULA, [
            fondo("bg_aula"),
            brillo(540, 900, 460, "#fff3d6", 0.5, 0.2, pulso=[0.1, 0.5]),
            *hojas,
            nino("marta_nina_orgullosa", -300, z=0.4), mesa(-300, z=0.42),
            nino("lucas_nino_reojo", 1400, z=0.4), mesa(1400, z=0.42)],
            cam(1.0, 1.08, (540, 950)), "corte",
            hud=[contador(0.1, d - 0.05, 1, 12, d * 0.8, " años", tam=120, x=540, y=1320, color="#ffffff", capsula="#2f6fb0e0", miles=False)],
            sfx=[(0.12 + i * (d * 0.75 / 11), "roce", -26) for i in range(0, 11, 2)])

    @plano(80, "el colegio repite siempre lo mismo: la profesora y la flecha que da vueltas")
    def _(d):
        pts = [[700 + 150 * math.cos(math.radians(a)), 720 + 110 * math.sin(math.radians(a))] for a in range(200, 520, 20)]
        return P(AULA, [
            fondo("bg_aula"),
            adulto("profesora_senala", 330, 1420, z=0.55, keys=mece(d, 1.5, 1.2)),
            flecha([[round(x), round(y)] for x, y in pts], 0.05, d * 0.45, "#ff8a3d", 9, z=0.6),
            flecha([[round(x), round(y) + 260] for x, y in pts], d * 0.45, d * 0.9, "#ff8a3d", 9, z=0.6),
            nino("marta_nina_mano", -350, z=0.45), mesa(-350, z=0.47),
            nino("lucas_nino_reojo", 1450, z=0.45), mesa(1450, z=0.47)],
            cam(1.0, 1.2, (540, 1000), (600, 900)), "corte", sfx=[(0.1, "trazo", -24), (d * 0.45, "trazo", -24)])

    @plano(86, "lo tuyo vale")
    def _(d):
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"),
            pie("foco_luz", 540, 1400, 1300, z=0.1),
            brillo(540, 950, 420, VERDE, 0.45, 0.15, pulso=[0.12, 0.8]),
            pieza("examen_bien", 540, 960, 560, z=0.55, keys=aparece(0.0, 0.35) + late(0.6, 1, 0.08, 0.4)),
            nino("marta_nina_orgullosa", -330, 1400, z=0.45), nino("marta_nina_escribe_a", 1420, 1400, z=0.45)],
            cam(1.0, 1.08, (540, 960)), "corte",
            hud=[amarillo(0.35, d - 0.05, "VALE", y=520, color=VERDE)],
            sfx=[(0.1, "ding", -18)])

    @plano(89, "lo copiado, no")
    def _(d):
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"),
            pie("foco_luz_frio", 540, 1400, 1300, z=0.1),
            brillo(540, 950, 420, ROJO, 0.4, 0.15),
            pieza("p1_examen_blanco", 540, 960, 560, z=0.55, keys=[{"t": 0, "rot": 8, "x": 600}, {"t": 0.3, "rot": 2, "x": 540, "ease": "salida"}]),
            *aspa(540, 960, 260, d * 0.45, ROJO, 30, 0.7),
            nino("lucas_nino_triste", 1420, 1400, z=0.45), nino("lucas_nino_pillado", -330, 1400, z=0.45)],
            cam(1.0, 1.08, (540, 960)), "corte",
            hud=[amarillo(d * 0.45, d - 0.05, "NO", y=520, color=ROJO)],
            sfx=[(d * 0.45, "zap", -16)])

    # ================================================================== EL ÚLTIMO TIMBRE (37,4–57,8 s)
    @plano(92, "pero un día: el colegio desde fuera")
    def _(d):
        return P(CALLE, [
            fondo("bg_colegio_fuera"),
            brillo(540, 900, 220, ORO, 0.5, 0.1, pulso=[0.2, 0.3]),
            pie("mochila_cole", 860, 1430, 160, z=0.5, rot=-8), pie("mochila_cole", -380, 1430, 150, z=0.5, rot=6)],
            cam(1.05, 1.4, (540, 1000), (540, 900)), "corte", sfx=[(0.05, "whoosh", -24)])

    @plano(95, "suena el último timbre")
    def _(d):
        return P(AULA, [
            fondo("bg_aula"),
            *flip(["timbre_a", "timbre_b"], d, fps=14, x=540, y=820, ancho=520, z=0.6),
            *[onda(540, 820, 0.05 + 0.3 * i, 330, ORO, 0.7, 8) for i in range(int(d / 0.3))],
            brillo(540, 820, 420, ORO, 0.4, 0.2, pulso=[0.2, 0.15]),
            nino("marta_nina_mano", -330, z=0.45), mesa(-330, z=0.47), nino("lucas_nino_pillado", 1420, z=0.45), mesa(1420, z=0.47)],
            cam(1.0, 1.06, (540, 860), temblor=0.25), "corte", sfx=timbre_sfx(0.02, d - 0.1))

    @plano(99, "salen a la calle (mochilas al aire)")
    def _(d):
        S = 1430
        mochis = [pie("mochila_cole", x, S, 150, z=0.6, keys=[{"t": 0, "x": x, "y": 1250, "rot": 0, "op": 1},
                                                             {"t": d * 0.5, "x": x + dx, "y": 500, "rot": rr, "ease": "salida"},
                                                             {"t": d, "x": x + 2 * dx, "y": 700, "rot": 2 * rr, "ease": "entrada"}])
                  for x, dx, rr in ((380, -60, -200), (700, 70, 220))]
        return P(CALLE, [
            fondo("bg_colegio_fuera"),
            *andar("marta_camina", 380, 560, S, d, z=0.5),
            *andar("lucas_camina", 640, 830, S, d, z=0.52),
            *mochis,
            pie("mochila_cole", -400, S, 150, z=0.5, rot=10), pieza("balon_futbol", 1450, S - 55, 110, z=0.5),
            {**polvo("#fff6e0", 26, (-400, 600, 1500, 1400), 99), "_ancho": False}],
            cam(1.05, 1.0, (600, 1050)), "corte", sfx=[(0.05, "whoosh", -20)])

    @plano(103, "y nadie les avisa: la calle")
    def _(d):
        S = 1440
        return P(CALLE, [
            fondo("bg_calle_dia"),
            *andar("marta_camina", 300, 470, S, d, z=0.5),
            *andar("lucas_camina", 560, 730, S, d, z=0.52),
            *andar("cliente_se_va", 1250, 900, S, d, z=0.45, esc=0.95),
            *lados_calle(103)[:2],
            {**polvo("#fff6e0", 20, (-400, 700, 1500, 1400), 103), "_ancho": False}],
            cam(1.0, 1.1, (540, 1100), (600, 1100)), "corte", sfx=[(0.1, "roce", -28), (0.6, "roce", -28)])

    @plano(109, "las reglas han cambiado: los exámenes se dan la vuelta")
    def _(d):
        tm = d * 0.35
        def gira(n_antes, n_despues, x, rot):
            a = pieza(n_antes, x, 960, 440, z=0.55, rot=rot, keys=[{"t": 0, "ex": 1.0}, {"t": tm, "ex": 1.0}, {"t": tm + 0.18, "ex": 0.0, "ease": "entrada"}])
            b = pieza(n_despues, x, 960, 440, z=0.56, rot=rot, keys=[{"t": 0, "ex": 0.0, "op": 0}, {"t": tm + 0.18, "ex": 0.0, "op": 0},
                                                                    {"t": tm + 0.19, "op": 1}, {"t": tm + 0.4, "ex": 1.0, "ease": "salida"},
                                                                    {"t": tm + 0.6, "escala": 1.06}, {"t": d, "escala": 1.0}])
            return [a, b]
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"),
            pie("foco_luz", 300, 1400, 1100, z=0.1), pie("foco_luz_frio", 780, 1400, 1100, z=0.1),
            *gira("examen", "examen_bien", 300, -5),
            *gira("examen_bien", "examen", 780, 5),
            pieza("calendario_hoja", -380, 900, 300, z=0.4, op=0.5, rot=-10), pieza("hoja_dibujo", 1450, 900, 360, z=0.4, op=0.5, rot=8)],
            cam(1.0, 1.06, (540, 960)), "corte",
            sfx=[(tm, "whoosh", -20), (tm + 0.4, "ding", -22)])

    @plano(113, "los dos quieren montar su propio negocio: las bombillas se encienden")
    def _(d):
        S = 1440
        o = rel(113)
        hm, hl = cabeza("marta_idea", S), cabeza("lucas_contento", S)
        def bomb(x, y, t0):
            return [pieza("bombilla_a", x, round(y), 150, z=0.6, keys=aparece(0.05) + [{"t": t0, "op": 1}, {"t": t0 + 0.05, "op": 0}]),
                    pieza("bombilla_b", x, round(y), 150, z=0.61, keys=[{"t": 0, "op": 0}, {"t": t0, "op": 0}, {"t": t0 + 0.05, "op": 1}] + late(t0, 1, 0.18, 0.3)),
                    brillo(x, round(y), 200, ORO, 0.6, 0.59, keys=[{"t": 0, "op": 0}, {"t": t0, "op": 0}, {"t": t0 + 0.1, "op": 1}])]
        return P(CALLE, [
            fondo("bg_calle_dia"),
            adulto("marta_idea", 330, S, z=0.5, keys=mece(d, 1.2, 1.6)),
            adulto("lucas_contento", 760, S, z=0.5, keys=mece(d, 1.2, 1.9)),
            *bomb(330, hm - 70, o(118)), *bomb(760, hl - 70, o(119)),
            pie("hamburgueseria_vacia", -480, S, 860, z=0.35), pie("hamburgueseria_vacia", 1580, S, 860, z=0.35, ex=-1)],
            cam(1.0, 1.35, (540, 1100), (540, 960)), "corte", sfx=[(o(118), "ding", -20), (o(119), "ding", -20, {"f": 990})])

    @plano(120, "y aquí Marta comete")
    def _(d):
        S = 1440
        return P(CALLE, [
            fondo("bg_calle_dia"),
            *andar("marta_camina", 260, 620, S, d, z=0.5, fps=4),
            *lados_calle(120),
            {**polvo("#fff6e0", 20, (-400, 700, 1500, 1400), 120), "_ancho": False}],
            cam(1.25, 1.25, (330, 1050), (620, 1050)), "corte", sfx=[(0.1, "roce", -28), (0.6, "roce", -28)])

    @plano(123, "el error")
    def _(d):
        return P(CALLE, [
            fondo("bg_calle_dia"),
            pieza("cara_marta_feliz", 540, 1050, 880, z=0.5, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.06}]),
            senala(540, 800, 0.0, d, 300, ROJO),
            negro([{"t": 0, "op": 0.0}, {"t": d, "op": 0.25}])],
            cam(1.2, 1.3, (540, 900), temblor=0.2), "corte",
            hud=[rotulo(0.02, d - 0.01, "ERROR", tam=110, color="#ffffff", capsula="#c0392be8", x=540, y=560, rot=-4)],
            sfx=[(0.02, "golpe", -14)])

    @plano(126, "que comete casi todo el mundo: bombillas sobre todos")
    def _(d):
        S = 1440
        gente = [("voluntario_1", -560), ("cliente_confuso_1", -330), ("voluntario_3", -100), ("marta_idea", 140), ("cliente_feliz_3", 380),
                 ("voluntario_5", 620), ("cliente_confuso_2", 860), ("voluntario_2", 1100), ("cliente_feliz_1", 1340), ("voluntario_6", 1580)]
        els = []
        for k, (n, x) in enumerate(gente):
            if n.startswith("voluntario"):
                a = 560; top = S - 0.97 * a
                els.append(pie(n, x, S, a, z=0.5))
            else:
                els.append(adulto(n, x, S, 0.92, z=0.5)); top = cabeza(n, S, 0.92)
            t0 = 0.1 + 0.13 * abs(k - 4.5)
            els.append(pieza("bombilla_b", x, round(top - 80), 120, z=0.6, keys=aparece(t0)))
        return P(CALLE, [fondo("bg_calle_dia"), *els,
                         {**polvo("#fff6e0", 20, (-400, 700, 1500, 1400), 126), "_ancho": False}],
                 cam(1.15, 1.0, (420, 1050), (540, 1080)), "corte",
                 sfx=[(0.1 + 0.13 * i, "pop", -24) for i in range(0, 6)])

    @plano(132, "busca una idea")
    def _(d):
        r = random.Random(132)
        bombs = []
        for k in range(7):
            ang = k / 7 * 6.283
            x, y = 540 + 380 * math.cos(ang) * 1.5, 850 + 300 * math.sin(ang)
            bombs.append(pieza("bombilla_a", round(x), round(y), 110, z=0.5, op=0.75,
                               keys=aparece(0.05 * k) + [{"t": d, "y": round(y) - 40, "rot": r.uniform(-20, 20)}]))
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"),
            pie("foco_luz", 540, 1400, 1300, z=0.1),
            adulto("marta_piensa", 540, 1400, z=0.55, keys=mece(d, 1.5, 1.4)),
            *bombs],
            cam(1.0, 1.08, (540, 1000)), "corte", sfx=[(0.1, "burbuja", -26), (0.4, "burbuja", -27)])

    @plano(135, "que no haya tenido nadie: la única bombilla")
    def _(d):
        r = random.Random(135)
        grises = []
        for k in range(10):
            x, y = r.uniform(-500, 1580), r.uniform(500, 1300)
            if 300 < x < 780:
                x += 500
            grises.append(pieza("bombilla_a", round(x), round(y), 120, z=0.4, op=0.6,
                                keys=[{"t": 0, "op": 0.6}, {"t": 0.2 + 0.06 * k, "op": 0.6}, {"t": 0.6 + 0.06 * k, "op": 0.0, "y": round(y) + 200, "ease": "entrada"}]))
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"),
            pie("foco_luz", 540, 1400, 1400, z=0.1),
            brillo(540, 900, 380, ORO, 0.6, 0.15, pulso=[0.15, 0.7]),
            *grises,
            pieza("bombilla_b", 540, 900, 380, z=0.6, keys=arranque(540, 900, d, "abajo", 160, 30))],
            cam(1.0, 1.1, (540, 920)), "corte", sfx=[(0.05, "brillo", -20)])

    @plano(140, "Lucas hace lo de siempre")
    def _(d):
        return P(CALLE, [
            fondo("bg_calle_dia"),
            pieza("cara_lucas_listo", 540, 1060, 900, z=0.5, keys=[{"t": 0, "x": 600, "rot": 2}, {"t": d, "x": 540, "rot": 0, "escala": 1.05, "ease": "suave"}] + late(d * 0.6, 1, 0.04, 0.4)),
            brillo(700, 800, 300, "#fff3d6", 0.3, 0.6)],
            cam(1.0, 1.06, (540, 960)), "corte", sfx=[(d * 0.6, "brillo", -26)])

    @plano(145, "mira al de al lado: la hamburguesería con cola")
    def _(d):
        S = 1440
        return P(CALLE, [
            fondo("bg_calle_dia"),
            pie("hamburgueseria", 1000, S, 880, z=0.4),
            *cola(760, S, n=4, alto=600, paso=120, z=0.5),
            pie("lucas_piensa", 0, S, 610, z=0.55, keys=mece(d, 1.0, 1.6)),
            flecha([[90, 890], [330, 850], [560, 960]], 0.1, d * 0.5, ROJO, 12, [20, 12], z=0.7),
            *lados_calle(145)[:2], pie("hamburgueseria_vacia", 1750, S, 860, z=0.35)],
            cam(1.0, 1.08, (480, 1100)), "corte", sfx=[(0.1, "roce", -26)])

    # ================================================================== MARTA (57,8–94,8 s)
    @plano(150, "Marta se pasa meses pensando")
    def _(d):
        S = 1440
        r = random.Random(150)
        bolas = [pieza("p1_examen_blanco", round(x), 1405, 70, z=0.52, keys=aparece(t0, 0.3), rot=r.uniform(-40, 40))
                 for x, t0 in ((760, 0.3), (840, 0.7), (300, 1.1), (900, 1.5), (220, 1.8))]
        return P(["#e8b48a", "#5a4a6a"], [
            fondo("bg_habitacion"),
            brillo(800, 800, 400, "#ffd9a0", 0.5, 0.1, keys=[{"t": 0, "op": 1}, {"t": d * 0.5, "op": 0.2}, {"t": d, "op": 1}]),
            adulto("marta_piensa", 540, S, z=0.55, keys=mece(d, 2, 1.2)),
            *bolas,
            pie("hoja_dibujo", -400, S, 200, z=0.5, rot=-10), pie("cuaderno_dibujo", 1450, S, 160, z=0.5)],
            cam(1.05, 1.15, (540, 1050)), "corte",
            hud=[contador(0.1, d - 0.05, 1, 8, d * 0.85, " meses", tam=110, x=540, y=560, color="#ffffff", capsula="#5a4a6ad8", miles=False)],
            sfx=[(0.1, "tictac", -26, {"dur": d * 0.8, "ritmo": 0.18})])

    @plano(155, "y al final la tiene")
    def _(d):
        S = 1440
        top = cabeza("marta_idea", S)
        return P(["#e8b48a", "#5a4a6a"], [
            fondo("bg_habitacion"),
            adulto("marta_idea", 540, S, z=0.55, keys=[{"t": 0, "rot": -3}, {"t": 0.35, "rot": 0, "ease": "elastico"}]),
            pieza("bombilla_b", 620, round(top - 90), 230, z=0.65, keys=aparece(0.25, 0.45) + late(1.0, 1, 0.1, 0.4)),
            brillo(620, round(top - 90), 380, ORO, 0.7, 0.6, keys=[{"t": 0, "op": 0}, {"t": 0.25, "op": 0}, {"t": 0.4, "op": 1}]),
            fundido_blanco([{"t": 0, "op": 0}, {"t": 0.25, "op": 0}, {"t": 0.3, "op": 0.55}, {"t": 0.6, "op": 0}]),
            pie("hoja_dibujo", -400, S, 200, z=0.5, rot=-10), pie("cuaderno_dibujo", 1450, S, 160, z=0.5)],
            cam(1.15, 1.25, (560, 950)), "corte", sfx=[(0.28, "ding", -16), (0.3, "brillo", -20)])

    @plano(160, "una cafetería")
    def _(d):
        S = 1440
        return P(CALLE, [
            fondo("bg_calle_dia"),
            pie("cafeteria_marta", 540, S, 860, z=0.45, keys=[{"t": 0, "escala": 0.6, "op": 0}, {"t": 0.04, "op": 1},
                                                              {"t": 0.35, "escala": 1.0, "ease": "elastico"}, {"t": d, "escala": 1.02}]),
            pieza("destello", 540, 780, 200, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.3, "op": 1, "escala": 1, "ease": "salida"}, {"t": 0.7, "op": 0}]),
            *lados_calle(160)],
            cam(1.05, 1.1, (540, 1100)), "corte", sfx=[(0.05, "pop", -18)])

    @plano(162, "donde no pagas el café")
    def _(d):
        return P(CAFE, [
            fondo("bg_cafe_dentro"),
            brillo(540, 1050, 380, "#ffd9a0", 0.5, 0.2, pulso=[0.1, 1.0]),
            pieza("taza_cafe_latte", 420, 1100, 460, z=0.5, keys=[{"t": 0, "y": 1130}, {"t": 0.3, "y": 1100, "ease": "salida"}]),
            pieza("billete", 780, 900, 360, z=0.55, keys=[{"t": 0, "x": 1300, "rot": 20}, {"t": 0.45, "x": 780, "rot": -6, "ease": "salida"}]),
            *aspa(780, 900, 170, d * 0.5, ROJO, 24, 0.7),
            pieza("taza_cafe_latte", -380, 1150, 300, z=0.45), pieza("taza_cafe_latte", 1450, 1150, 300, z=0.45)],
            cam(1.0, 1.06, (600, 1000)), "corte", sfx=[(0.1, "roce", -24), (d * 0.5, "zap", -18)])

    @plano(167, "pagas el tiempo que te quedas: el reloj de arena gira")
    def _(d):
        S = 1430
        return P(CAFE, [
            fondo("bg_cafe_dentro"),
            brillo(540, 950, 420, ORO, 0.5, 0.2, pulso=[0.12, 0.8]),
            pieza("reloj_arena_grande", 540, 960, 380, z=0.55, keys=[{"t": 0, "rot": 0}, {"t": 0.25, "rot": 0}, {"t": 0.75, "rot": 180, "ease": "anticipa"},
                                                                    {"t": d, "rot": 182}]),
            pieza("taza_cafe_latte", 200, 1300, 220, z=0.5), pieza("taza_cafe_latte", 880, 1300, 220, z=0.5, ex=-1),
            adulto("cliente_feliz_2", -380, S, z=0.45), adulto("cliente_feliz_3", 1480, S, z=0.45, ex=-1)],
            cam(1.0, 1.1, (540, 960)), "corte",
            hud=[contador(0.8, d - 0.05, 0, 45, d - 0.9, " min", tam=110, x=540, y=560, color=ORO, capsula="#0b0f1ed8", miles=False)],
            sfx=[(0.3, "whoosh", -22), (0.8, "tictac", -22, {"dur": d - 0.9, "ritmo": 0.2})])

    @plano(173, "es original")
    def _(d):
        S = 1440
        s, izq, arr = fachada_geo(440, S, 880)
        return P(CALLE, [
            fondo("bg_calle_dia"),
            pie("cafeteria_marta", 440, S, 880, z=0.4),
            adulto("marta_sonrie", 1000, S, 0.95, z=0.55, keys=[{"t": 0, "rot": -2}, {"t": 0.35, "rot": 1, "ease": "elastico"}]),
            pieza("destello", round(izq + 450 * s), round(arr + 70 * s), 220, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.15, "op": 1, "escala": 1, "ease": "salida"},
                                                                                            {"t": 0.6, "op": 0}]),
            brillo(round(izq + 450 * s), round(arr + 70 * s), 200, ORO, 0.5, 0.6, pulso=[0.2, 0.7]),
            *lados_calle(173)],
            cam(1.0, 1.1, (620, 1050)), "corte", sfx=[(0.15, "brillo", -22)])

    @plano(175, "es bonita: destellos en el café")
    def _(d):
        r = random.Random(175)
        dest = []
        for k in range(8):
            x, y, t0 = r.uniform(-400, 1500), r.uniform(500, 1100), 0.05 + 0.1 * k
            dest.append(pieza("destello", round(x), round(y), round(r.uniform(90, 160)), z=0.7,
                              keys=[{"t": 0, "op": 0, "escala": 0}, {"t": t0, "op": 0, "escala": 0}, {"t": t0 + 0.2, "op": 1, "escala": 1, "ease": "salida"},
                                    {"t": t0 + 0.55, "op": 0}]))
        return P(CAFE, [
            fondo("bg_cafe_dentro"),
            brillo(540, 700, 500, "#ffd9a0", 0.45, 0.2, pulso=[0.1, 0.9]),
            adulto("marta_sonrie", 540, 1430, z=0.55),
            *dest],
            cam(1.0, 1.1, (540, 900), (600, 900)), "corte", sfx=[(0.1, "brillo", -24)])

    @plano(177, "y no hay nada igual en su ciudad")
    def _(d):
        S = 1440
        return P(CALLE, [
            fondo("bg_calle_dia"),
            pie("cafeteria_marta", 540, S, 600, z=0.45),
            pie("hamburgueseria_vacia", -320, S, 560, z=0.4), pie("hamburgueseria", 1400, S, 560, z=0.4),
            pieza("icono_igual", 540, 620, 220, z=0.65, keys=aparece(0.2)),
            *aspa(540, 620, 130, d * 0.45, ROJO, 22, 0.7),
            senala(540, 1150, d * 0.2, d, 360, ORO),
            *cola(-600, S, n=2, alto=420),
            {**polvo("#fff6e0", 20, (-400, 700, 1500, 1400), 177), "_ancho": False}],
            cam(1.2, 0.98, (540, 1080)), "corte", sfx=[(0.2, "pop", -22), (d * 0.45, "zap", -20)])

    @plano(185, "pide un préstamo")
    def _(d):
        # el sello del contrato está abajo a la derecha (≈ 0,82, 0,86 del lienzo 560×740)
        A = 520; cx, cy = 540, 960
        sx, sy = cx + (0.82 - 0.5) * A, cy + (0.86 - 0.5) * A * 740 / 560
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"),
            pie("foco_luz", 540, 1400, 1300, z=0.1),
            pieza("contrato_prestamo", cx, cy, A, z=0.55, keys=[{"t": 0, "x": 1200, "rot": 25}, {"t": 0.35, "x": cx, "rot": -3, "ease": "salida"}]),
            senala(round(sx), round(sy), 0.55, d, 80, ROJO),
            *[pieza("billete", 540, 960, 200, z=0.5, keys=[{"t": 0, "op": 0}, {"t": 0.6 + 0.1 * k, "op": 1, "x": 540, "y": 960},
                                                            {"t": 1.1 + 0.1 * k, "x": 540 + (k - 1) * 700, "y": 650, "rot": (k - 1) * 40, "op": 0.0, "ease": "salida"}]) for k in range(3)]],
            cam(1.0, 1.08, (540, 960)), "corte", sfx=[(0.1, "roce", -22), (0.55, "golpe", -16)])

    @plano(188, "decora el local")
    def _(d):
        S = 1430
        return P(CAFE, [
            fondo("bg_cafe_dentro"),
            adulto("marta_explica_b", 540, S, z=0.55, keys=mece(d, 1.5, 1.0)),
            pieza("hoja_dibujo", 250, 700, 220, z=0.5, keys=[{"t": 0, "y": -200, "rot": -30}, {"t": 0.4, "y": 700, "rot": -4, "ease": "bote"}]),
            pieza("taza_cafe_latte", 860, 1200, 150, z=0.5, keys=aparece(0.3)),
            pieza("reloj_arena_grande", 200, 1220, 90, z=0.5, keys=aparece(0.5)),
            pieza("destello", 860, 700, 140, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.6, "op": 1, "escala": 1}, {"t": 0.9, "op": 0}]),
            pieza("hoja_dibujo", -350, 700, 220, z=0.5, rot=6), pieza("hoja_dibujo", 1420, 720, 220, z=0.5, rot=-5)],
            cam(1.1, 1.0, (540, 1000)), "corte", sfx=[(0.35, "golpe", -24), (0.3, "pop", -24), (0.5, "pop", -26)])

    @plano(191, "y abre: el cartel cambia")
    def _(d):
        S = 1440
        s, izq, arr = fachada_geo(540, S, 900)
        cx, cy = round(izq + 640 * s), round(arr + 460 * s)
        tm = 0.25
        return P(CALLE, [
            fondo("bg_calle_dia"),
            pie("cafeteria_marta", 540, S, 900, z=0.45),
            pieza("cartel_cerrado", cx, cy, 200, z=0.6, keys=[{"t": 0, "ex": 1}, {"t": tm, "ex": 1}, {"t": tm + 0.12, "ex": 0, "ease": "entrada"}]),
            pieza("cartel_abierto", cx, cy, 200, z=0.61, keys=[{"t": 0, "ex": 0, "op": 0}, {"t": tm + 0.12, "ex": 0, "op": 0}, {"t": tm + 0.13, "op": 1},
                                                              {"t": tm + 0.3, "ex": 1, "ease": "salida"}] + mece(d, 4, 0.8)[1:]),
            *lados_calle(191)],
            cam(1.3, 1.45, (cx - 100, cy + 60)), "corte", sfx=[(tm + 0.1, "ding", -18)])

    @plano(193, "el primer día entran tres personas")
    def _(d):
        S = 1430
        o = rel(193)
        tb = o(196)
        els = []
        for k, (n, x1) in enumerate((("cliente_confuso_1", 640), ("cliente_confuso_2", 860), ("cliente_feliz_3", 1080))):
            t0 = tb + 0.05 + 0.22 * k
            els.append(adulto(n, x1, S, z=0.55 + 0.01 * k, keys=[{"t": 0, "x": 1700}, {"t": t0, "x": 1700}, {"t": t0 + 0.4, "x": x1, "ease": "salida"}]))
        return P(CAFE, [
            fondo("bg_cafe_dentro"),
            brillo(540, 900, 420, "#ffd9a0", 0.45, 0.2, pulso=[0.1, 1.0]),
            adulto("marta_sonrie", 360, S, z=0.5, keys=[{"t": 0, "rot": 0}, {"t": tb, "rot": 2}, {"t": tb + 0.3, "rot": -1, "ease": "elastico"}]),
            pieza("taza_cafe_latte", 60, 1250, 140, z=0.5), pieza("reloj_arena_grande", -300, 1240, 110, z=0.5),
            *els],
            cam(1.15, 1.0, (420, 1000), (560, 1000)), "corte",
            hud=[rotulo(0.08, tb - 0.05, "DÍA 1", tam=110, color="#ffffff", capsula="#2f5a52e0", x=360, y=560),
                 contador(tb + 0.05, d - 0.05, 0, 3, 0.7, "", tam=150, x=860, y=560, color=ORO, capsula="#0b0f1ed8", miles=False)],
            sfx=[(0.1, "ding", -24)] + [(tb + 0.1 + 0.22 * k, "roce", -24) for k in range(3)] + [(tb + 0.75, "pop", -20)])

    @plano(199, "preguntan dónde está la carta")
    def _(d):
        S = 1430
        return P(CAFE, [
            fondo("bg_cafe_dentro"),
            adulto("cliente_confuso_1", 330, S, z=0.55, keys=mece(d, 2, 1.0)),
            adulto("cliente_confuso_2", 760, S, z=0.55, keys=mece(d, 2, 1.2, 1)),
            adulto("marta_sonrie", -330, S, 0.95, z=0.5), adulto("cliente_feliz_3", 1400, S, z=0.5, ex=-1)],
            cam(1.15, 1.25, (540, 1000)), "corte",
            hud=[rotulo(0.15, d - 0.05, "?", tam=200, color=ORO, capsula=None, x=330, y=560, rot=-8),
                 rotulo(0.45, d - 0.05, "?", tam=200, color=ORO, capsula=None, x=780, y=560, rot=8)],
            sfx=[(0.15, "burbuja", -22), (0.45, "burbuja", -22)])

    @plano(204, "Marta les explica la idea")
    def _(d):
        S = 1430
        return P(CAFE, [
            fondo("bg_cafe_dentro"),
            *flip(["marta_explica_a", "marta_explica_b"], d, fps=3, base=lambda n: adulto(n, 400, S, z=0.55)),
            pieza("reloj_arena_grande", 400, 640, 150, z=0.6, keys=aparece(0.3) + [{"t": d, "rot": 10}]),
            adulto("cliente_confuso_1", 900, S, 0.98, z=0.5, ex=-1),
            adulto("cliente_confuso_2", 1150, S, 0.98, z=0.5, ex=-1),
            adulto("cliente_feliz_3", -350, S, z=0.45)],
            cam(1.05, 1.15, (560, 1000)), "corte", sfx=[(0.3, "pop", -24)])

    @plano(209, "se van")
    def _(d):
        S = 1430
        return P(CAFE, [
            fondo("bg_cafe_dentro"),
            adulto("marta_triste", 280, S, z=0.5),
            *andar("cliente_se_va", 560, 1350, S, d, z=0.55, fps=6, ex=-1),
            *andar("cliente_se_va", 760, 1650, S, d, z=0.56, fps=6, ex=-1, esc=0.97)],
            cam(1.0, 1.0, (600, 1000)), "corte", sfx=[(0.05, "whoosh", -20), (0.3, "roce", -24)])

    @plano(211, "cada cliente que entra")
    def _(d):
        S = 1430
        nombres = ["cliente_confuso_1", "cliente_feliz_1", "cliente_confuso_2", "cliente_feliz_3", "cliente_feliz_2"]
        els = []
        paso = d / len(nombres)
        for k, n in enumerate(nombres):
            t0 = k * paso
            els.append(adulto(n, 1500, S, z=0.55, keys=[{"t": 0, "x": 1500, "op": 0}, {"t": max(0, t0 - 0.01), "x": 1500, "op": 0}, {"t": t0, "x": 1500, "op": 1},
                                                        {"t": t0 + paso * 0.4, "x": 760, "ease": "salida"},
                                                        {"t": t0 + paso * 0.75, "x": 760}, {"t": t0 + paso * 1.1, "x": 1600, "ease": "entrada"}]))
        return P(CAFE, [
            fondo("bg_cafe_dentro"),
            *flip(["marta_explica_a", "marta_explica_b"], d, fps=5, base=lambda n: adulto(n, 300, S, z=0.5)),
            *els],
            cam(1.0, 1.05, (560, 1000)), "corte", sfx=[(k * d / 5, "roce", -24) for k in range(5)])

    @plano(215, "necesita una explicación (y otra, y otra)")
    def _(d):
        S = 1430
        return P(CAFE, [
            fondo("bg_cafe_dentro"),
            *flip(["marta_explica_a", "marta_explica_b"], d, fps=3, base=lambda n: adulto(n, 540, S, z=0.55)),
            negro([{"t": 0, "op": 0.0}, {"t": d, "op": 0.2}]),
            adulto("cliente_confuso_2", 1400, S, z=0.5, ex=-1), adulto("cliente_confuso_1", -320, S, z=0.5)],
            cam(1.2, 1.5, (540, 900)), "corte",
            hud=[contador(0.1, d - 0.05, 1, 40, d * 0.85, " explicaciones", tam=84, x=540, y=560, color="#ffffff", capsula="#c0392be0", miles=False)],
            sfx=[(0.1, "tictac", -26, {"dur": d * 0.8, "ritmo": 0.12})])

    @plano(218, "y la mayoría no vuelve")
    def _(d):
        S = 1440
        return P(CALLE, [
            fondo("bg_calle_dia"),
            pie("cafeteria_marta", 160, S, 880, z=0.4),
            *andar("cliente_se_va", 760, 1250, S, d, z=0.55, fps=4, ex=-1),
            *andar("cliente_se_va", 980, 1550, S, d, z=0.5, fps=4, ex=-1, esc=0.95),
            pie("hamburgueseria_vacia", -700, S, 860, z=0.35),
            negro([{"t": 0, "op": 0.0}, {"t": d, "op": 0.25}])],
            cam(1.0, 1.08, (540, 1100), (640, 1100)), "corte", sfx=[(0.2, "roce", -26), (0.8, "roce", -27)])

    @plano(223, "al año ha gastado todos sus ahorros: la hucha se rompe")
    def _(d):
        o = rel(223)
        tb = o(225)
        tm = tb + (d - tb) * 0.35
        r = random.Random(225)
        monedas = []
        for k in range(8):
            ang = r.uniform(200, 340)
            dx, dy = math.cos(math.radians(ang)) * r.uniform(400, 800), math.sin(math.radians(ang)) * r.uniform(300, 600)
            monedas.append(pieza("monedas", 540, 1150, 110, z=0.6, keys=[{"t": 0, "op": 0}, {"t": tm - 0.01, "op": 0}, {"t": tm, "op": 1, "x": 540, "y": 1150, "rot": 0},
                                                                       {"t": tm + 0.6, "x": round(540 + dx), "y": round(1150 + dy), "rot": r.uniform(-180, 180), "ease": "salida"},
                                                                       {"t": tm + 1.2, "y": 1700, "op": 0, "ease": "entrada"}]))
        return P(OSCURO, [
            fondo("bg_estudio_oscuro"),
            pie("foco_luz_frio", 540, 1400, 1300, z=0.1),
            pieza("calendario_hoja", 540, 880, 240, z=0.5, keys=[{"t": 0, "op": 1, "rot": -6, "x": 540, "y": 880}, {"t": tb, "op": 1, "rot": 4, "x": 540, "y": 880},
                                                              {"t": tb + 0.4, "op": 0, "y": 300, "x": 900, "rot": 60, "ease": "salida"}]),
            pie("hucha", 540, 1400, 400, z=0.55, keys=[{"t": 0, "op": 1, "rot": 0}, {"t": tm - 0.15, "rot": -4, "op": 1}, {"t": tm - 0.05, "rot": 5, "op": 1}, {"t": tm, "op": 0}]),
            pie("hucha_rota", 540, 1400, 330, z=0.55, keys=[{"t": 0, "op": 0}, {"t": tm - 0.01, "op": 0}, {"t": tm, "op": 1}]),
            *monedas],
            cam(1.0, 1.08, (540, 1100), temblor=0.0), "corte",
            hud=[rotulo(0.03, tb - 0.02, "1 AÑO", tam=120, color="#ffffff", capsula="#0b0f1ed8", x=540, y=600),
                 contador(tb + 0.1, d - 0.05, 30000, 0, (d - tb) * 0.85, " €", tam=120, x=540, y=600, color=ROJO, capsula="#0b0f1ed8")],
            sfx=[(0.03, "tictac", -24, {"dur": tb * 0.8, "ritmo": 0.06}), (tm, "impacto", -14), (tm + 0.1, "tictac", -22, {"dur": 0.8, "ritmo": 0.05})])

    @plano(231, "en convencer a la gente")
    def _(d):
        S = 1430
        return P(["#3a3530", "#14110e"], [
            fondo("bg_cafe_dentro_triste"),
            *flip(["marta_explica_a", "marta_explica_b"], d, fps=3, base=lambda n: adulto(n, 380, S, z=0.55)),
            adulto("cliente_confuso_1", 820, S, 0.97, z=0.5, ex=-1, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": -3}]),
            *andar("cliente_se_va", 1000, 1500, S, d, z=0.5, fps=4, ex=-1, esc=0.95),
            brillo(500, 800, 300, "#ffd9a0", 0.4, 0.3, pulso=[0.15, 0.4])],
            cam(1.1, 1.15, (560, 1000)), "corte", sfx=[(0.2, "roce", -26)])

    @plano(237, "algo que nadie le había pedido")
    def _(d):
        S = 1430
        return P(["#3a3530", "#14110e"], [
            fondo("bg_cafe_dentro_triste"),
            brillo(560, 900, 380, "#ffd9a0", 0.45, 0.3, pulso=[0.2, 0.35]),
            adulto("marta_triste", 540, S, z=0.55, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": -2}]),
            {**polvo("#ffd9a0", 26, (200, 500, 900, 1400), 237), "_ancho": False}],
            cam(1.35, 1.05, (540, 1000)), "corte", vineta=0.8, sfx=[(0.1, "rumor", -28, {"dur": d})])

    @plano(243, "y baja la persiana")
    def _(d):
        S, A = 1440, 700
        T = round(w(247) - w(243), 3)          # duración real del plano en el montaje completo
        t1 = T * 0.75
        return P(CALLE, [
            fondo("bg_calle_dia"),
            pie("cafeteria_marta", 540, S, A, z=0.4),
            persiana_baja(540, S, A, 0.0, t1, 1.0, ease="lineal"),
            pie("cafeteria_marta_cerrada", 540, S, A, z=0.58, keys=[{"t": 0, "op": 0}, {"t": t1 + 0.02, "op": 0}, {"t": t1 + 0.08, "op": 1}]),
            negro([{"t": 0, "op": 0.1}, {"t": T, "op": 0.4}]),
            pie("hamburgueseria_vacia", -560, S, 560, z=0.35), pie("hamburgueseria_vacia", 1640, S, 560, z=0.35, ex=-1)],
            cam(1.05, 1.15, (540, 1100)), "corte", sfx=ruido_persiana(0.0, t1))
