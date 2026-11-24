"""Parte 4 (palabras 844–1034): «Mientras tanto, arriba, el mundo no te espera.» … «Y al hacer la cuenta, le sale muy poco.»"""
from comun import *  # noqa: F401,F403
import comun

INICIO, FIN = 844, 1034


# ------------------------------------------------------------------ ayudantes propios de esta parte
def cy(nombre, suelo, alto):
    """y del centro de una pieza posada con pie() (para moverla con claves sin que despegue del suelo)."""
    return round(suelo - (comun.APOYO.get(nombre, 0.97) - 0.5) * alto)


def andar(nombre, x0, x1, suelo, alto, d, z=0.5, mira=1, bote=10, t0=0.0, t1=None, **k):
    """Figura que cruza andando (de x0 a x1) con un pequeño bote al paso."""
    y = cy(nombre, suelo, alto)
    t1 = d if t1 is None else t1
    ks = [{"t": t0, "x": x0, "ease": "lineal"}, {"t": t1, "x": x1}]
    paso, t, j = 0.22, t0, 0
    while t < t1:
        ks.append({"t": round(t, 3), "y": y - (bote if j % 2 else 0), "ease": "suave"})
        t += paso; j += 1
    return pie(nombre, x0, suelo, alto, z=z, keys=sorted(ks, key=lambda q: q["t"]), ex=mira, **k)


def hud_fijo(d, texto="", **k):
    """Rótulo que ya está en pantalla en el fotograma 0 (continúa del plano anterior), sin pop."""
    t1 = max(0.05, d - 0.02)
    return {"tipo": "rotulo", "texto": texto, "hud": True, "z": 1, "sin_pop": True, "fijo": True,
            "keys": [{"t": 0, "escala": 1.0, "op": 1}, {"t": t1 - 0.01, "escala": 1.0, "op": 1}, {"t": t1, "op": 1}], **k}


def nubes_hojas(d, n=5, sem=1, y=(760, 1150), t0=0.0, z=0.7, piezas=("calendario_hoja",), ancho=(90, 150)):
    """Hojas (de calendario, de otoño…) que cruzan volando, girando."""
    r = random.Random(sem)
    out = []
    for i in range(n):
        a = t0 + (d - t0) * i / max(1, n) * 0.8
        yy = r.uniform(*y)
        x0, x1 = (-700, 1750) if i % 2 == 0 else (1750, -700)
        out.append(IMG(r.choice(piezas), ancho=round(r.uniform(*ancho)), x=x0, y=yy, z=z + 0.01 * i,
                       keys=[{"t": 0, "op": 0, "x": x0, "y": yy}, {"t": a, "op": 1, "x": x0, "rot": 0},
                             {"t": a + r.uniform(0.9, 1.4), "x": x1, "y": yy + r.uniform(-160, 160), "rot": r.choice([-1, 1]) * 360, "ease": "lineal"}],
                       _ancho=True))
    return out


def ruta(nombre, x0, y0, x1, y1, t0, t1, ancho, z=0.6, esc=(1.0, 1.0), op1=1.0, rot=0, **k):
    """Pieza que va de (x0,y0) a (x1,y1) entre t0 y t1 (s del plano)."""
    return IMG(nombre, ancho=round(ancho), x=x0, y=y0, z=z,
               keys=[{"t": 0, "op": 0, "x": x0, "y": y0, "escala": esc[0]}, {"t": t0, "op": 1, "x": x0, "y": y0, "escala": esc[0], "rot": 0},
                     {"t": t1, "x": x1, "y": y1, "escala": esc[1], "op": op1, "rot": rot, "ease": "suave"}], **k)


def planos(v, plano):
    w = v.w
    comun.VUELOS += [(w(920), w(920) + 6.5, (1350, 560), (-350, 640), 140), (w(996), w(996) + 7, (-350, 600), (1350, 520), 120)]

    # contador de días de la ráfaga «quinientos días…» (893 → 920): corre por encima de todos los micro planos
    D0, D1 = w(893), w(920)

    def dia(T):
        u = min(max((T - D0) / (D1 - D0), 0.0), 1.0)
        return 1 + 499 * u

    def contador_dias(d):
        T0 = comun.D._V.ini
        a, b = dia(T0), dia(T0 + d)
        h = hud_fijo(d, tam=74, color="#ffd23f", capsula="#0b0f1ee6", x=540, y=470, contar_prefijo="DÍA ", miles=False, _full=True)
        h["contar"], h["contar_desde"] = [round(a), round(b), d], 0
        h["_solo"] = "v"
        hh = {**h, "x": 230, "y": 190, "_solo": "h", "keys": [dict(q) for q in h["keys"]]}
        return [h, hh]

    # ================================================================== «Mientras tanto, arriba, el mundo no te espera.»
    @plano(844, "arriba, el mundo no te espera: corte de la montaña")
    def _(d):
        # Gancho de la parte 4: la cámara sale disparada de la cámara de la cueva hacia la superficie, que bulle.
        S = 482   # suelo de la superficie en el corte
        return P(["#7fb6dd", "#2a1d14"], [
            fondo("bg_corte_tierra"),
            brillo(605, 1300, 160, "#ffcf8a", 0.8, 0.5, pulso=[0.2, 0.6]),
            *flip(["bea_lee_a", "bea_lee_b"], d, fps=2.5, base=lambda n: pie(n, 600, 1338, 92, z=0.55)),
            pie("lampara_led", 660, 1338, 34, z=0.56),
            andar("adulto_camina", 120, 430, S, 80, d, z=0.5, mira=-1),
            andar("nino_corre", 1010, 690, S, 62, d, z=0.5, mira=-1, bote=6),
            andar("bici_nino", 330, 700, S, 52, d, z=0.51),
            andar("voluntario_4", 860, 760, S, 86, d, z=0.49, bote=4),
            andar("adulto_camina", -900, -500, S, 80, d, z=0.5, mira=-1), andar("voluntario_6", 1500, 1250, S, 86, d, z=0.5),
            andar("nino_corre", -300, -60, S, 62, d, z=0.5, bote=6),
            ruta("sol_verano", 760, 250, 900, 180, 0.0, d, 120, z=0.12),
            *nubes_hojas(d, n=4, sem=4, y=(300, 440), piezas=("hoja_otono", "calendario_hoja"), ancho=(50, 80), z=0.45)],
            cam(1.6, 1.0, (605, 1250), (605, 880)), "corte",
            sfx=[(0.0, "whoosh", -14), (0.05, "rumor", -24, {"dur": 1.6}), (1.0, "roce", -26), (1.8, "roce", -27)])

    @plano(849, "no te espera: la ciudad a toda prisa", -0.21)
    def _(d):
        S = 1390
        return P(["#1b1a3a", "#0b0b16"], [
            fondo("bg_ciudad"),
            andar("adulto_camina", 1250, -250, S, 520, d, z=0.6, mira=1, bote=12),
            andar("nino_corre", -250, 1300, S, 380, d, z=0.62, mira=1, bote=14, t0=0.1),
            andar("bici_nino", 1400, 200, S, 260, d, z=0.58, mira=-1, bote=5, t0=0.25),
            andar("voluntario_5", -400, 300, S, 470, d, z=0.55, bote=8),
            andar("voluntario_3", 1700, 900, S, 470, d, z=0.55, mira=-1, bote=8),
            *nubes_hojas(d, n=5, sem=7, y=(560, 1100), t0=0.05, z=0.75),
            brillo(820, 900, 260, "#ffd59a", 0.3, 0.2, pulso=[0.15, 0.7])],
            cam(1.05, 1.18, (540, 1100), (600, 1040)), "corte",
            sfx=[(0.05, "whoosh", -15), (0.3, "roce", -24), (0.8, "roce", -26)])

    # ================================================================== «Cuando Beatriz entró en la cueva,»
    @plano(852, "cuando Beatriz entró en la cueva")
    def _(d):
        return P(["#6fb6e8", "#c9a26b"], [
            fondo("bg_entrada_dia"),
            *flip(["bea_camina_a", "bea_camina_b"], d, fps=4, base=lambda n: IMG(n, ancho=330, x=920, y=1300, z=0.6, ex=-1,
                  keys=K(d, (0, {"x": 920, "y": 1300, "escala": 1.0, "op": 1}), (0.8, {"x": 620, "y": 1080, "escala": 0.45, "op": 1, "ease": "suave"}),
                         (1, {"x": 590, "y": 1060, "escala": 0.38, "op": 0})))),
            brillo(585, 1060, 140, "#1a120d", 0.6, 0.3),
            pie("voluntario_5", 1290, 1370, 430, z=0.55), pie("voluntario_3", -230, 1370, 430, z=0.55),
            pie("mochila", 1450, 1380, 150, z=0.56), pie("camara_tripode", -480, 1380, 300, z=0.55),
            pie("rocas_primer_plano_a", 540, 1920, 420, z=0.9)],
            cam(1.0, 1.14, (600, 1200), (590, 1080)), "corte",
            sfx=[(0.1, "golpe", -29), (0.45, "golpe", -30), (0.8, "golpe", -30), (1.6, "rumor", -26)])

    # ================================================================== «Rusia todavía no había invadido Ucrania»
    @plano(858, "el periódico: las hojas pasan")
    def _(d):
        # tema delicado: solo un periódico genérico que pasa páginas (sin mapas, banderas ni armas)
        hojas = []
        for i, t in enumerate([0.25, 0.75, 1.25]):
            hojas.append(pieza("periodico", 540, 960, 620, z=0.6 + 0.01 * i,
                               keys=[{"t": 0, "ex": 1.0, "op": 1}, {"t": t, "ex": 1.0, "op": 1}, {"t": t + 0.3, "ex": -0.05, "op": 1, "ease": "entrada"},
                                     {"t": t + 0.31, "op": 0}]))
        return P(["#4a2e20", "#1d120c"], [
            fondo("bg_ventana_invierno"),
            pieza("periodico", 540, 960, 620, z=0.58, keys=K(d, (0, {"rot": -3}), (1, {"rot": 2}))), *hojas,
            ruta("periodico", 540, -200, 560, 1000, 1.45, 1.75, 600, z=0.65, rot=8),
            pie("taza_cafe", 1300, 1300, 170, z=0.55), pie("libro_b", -300, 1300, 60, z=0.55), pie("libro_a", -300, 1250, 60, z=0.56),
            brillo(540, 700, 380, "#ffd59a", 0.3, 0.2)],
            cam(1.0, 1.12, (540, 960), (540, 990)), "corte",
            sfx=[(0.3, "roce", -24), (0.8, "roce", -25), (1.3, "roce", -24), (1.72, "golpe", -22)])

    # ================================================================== «y medio planeta seguía pendiente de la pandemia.»
    @plano(864, "medio planeta: el mundo gira")
    def _(d):
        return P(["#0a1030", "#02030a"], [
            estrellas(60, sem=11),
            brillo(540, 940, 520, "#2f7bff", 0.45, 0.1, pulso=[0.1, 1.2]),
            pieza("foto_mundo", 540, 940, 560, z=0.6, keys=K(d, (0, {"escala": 0.75, "rot": -20}), (1, {"escala": 1.0, "rot": 25, "ease": "salida"}))),
            pieza("luna_creciente", 1400, 760, 200, z=0.3, keys=K(d, (0, {"y": 800}), (1, {"y": 740}))),
            pieza("foto_mundo", -420, 1100, 160, z=0.25, op=0.0)],
            cam(1.0, 1.1, (540, 940)), "corte",
            sfx=[(0.05, "brillo", -22)])

    @plano(868, "pendiente de la pandemia: mascarillas")
    def _(d):
        mas = []
        for i, (x, y, a, r) in enumerate([(230, 700, 230, -18), (850, 760, 210, 14), (300, 1220, 200, 10), (820, 1200, 240, -10),
                                          (-350, 900, 260, 8), (1450, 1000, 260, -12)]):
            mas.append(pieza("mascarilla", x, y, a, z=0.55, keys=[*aparece(0.12 + 0.12 * i, 0.35), {"t": 0.12 + 0.12 * i, "rot": r},
                                                                   {"t": d, "rot": -r * 0.5, "y": y - 30}]))
        return P(["#0a1030", "#02030a"], [
            estrellas(60, sem=12),
            brillo(540, 960, 480, "#2f7bff", 0.35, 0.1),
            pieza("foto_mundo", 540, 960, 420, z=0.5, anim={"girar": 18}),
            *mas,
            pieza("mascarilla", 540, 980, 640, z=0.7, keys=K(d, (0, {"y": 2300, "escala": 1.2}), (0.55, {"y": 2300}), (0.85, {"y": 990, "escala": 1.0, "ease": "rebote"}),
                                                            (1, {"y": 975})))],
            cam(1.05, 1.15, (540, 960)), "corte",
            sfx=[(0.12 + 0.12 * i, "pop", -26) for i in range(0, 6, 2)] + [(d * 0.75, "golpe", -20)])

    # ================================================================== «Ella no se enteró de nada.»
    @plano(872, "ella no se entera: abajo lee, arriba todo cambia")
    def _(d):
        S = 482
        return P(["#7fb6dd", "#2a1d14"], [
            fondo("bg_corte_tierra"),
            brillo(605, 1300, 170, "#ffcf8a", 0.85, 0.5, pulso=[0.15, 0.9]),
            *flip(["bea_lee_a", "bea_lee_b"], d, fps=1.5, base=lambda n: pie(n, 600, 1338, 92, z=0.55)),
            pie("lampara_led", 660, 1338, 34, z=0.56),
            pie("periodico", 260, S, 60, z=0.5, keys=aparece(0.1)), pie("mascarilla", 430, S - 40, 70, z=0.5, keys=aparece(0.35)),
            pie("urna_voto", 800, S, 60, z=0.5, keys=aparece(0.6)), pie("trofeo", 950, S, 60, z=0.5, keys=aparece(0.85)),
            andar("voluntario_2", 1300, 1700, S, 90, d, z=0.5), andar("voluntario_1", -500, -900, S, 90, d, z=0.5, mira=-1),
            *nubes_hojas(d, n=5, sem=9, y=(300, 440), piezas=("hoja_otono", "copo_nieve", "flor_primavera"), ancho=(40, 70), z=0.45)],
            cam(1.0, 1.4, (605, 900), (605, 1230)), "corte",
            sfx=[(0.1, "pop", -28), (0.6, "pop", -28), (1.2, "rumor", -28, {"dur": 0.8})])

    # ================================================================== «Tampoco de lo que pasaba con su propia familia.»
    @plano(878, "su familia, arriba, esperando")
    def _(d):
        S = 1370
        return P(["#f7a85c", "#2b1a2e"], [
            fondo("bg_entrada_atardecer"),
            pie("voluntario_2", 330, S, 440, z=0.55, keys=K(d, (0, {"x": 310}), (1, {"x": 345}))),
            pie("voluntario_1", 760, S, 470, z=0.55, keys=K(d, (0, {"x": 780}), (1, {"x": 740}))),
            andar("nino_corre", 1300, 560, S, 260, d, z=0.6, mira=-1, bote=10),
            pie("voluntario_6", -320, S, 440, z=0.5), pie("voluntario_3", 1450, S, 440, z=0.5),
            brillo(585, 1060, 150, "#1a120d", 0.6, 0.3),
            brillo(300, 380, 300, "#ffd59a", 0.4, 0.1, pulso=[0.1, 1.4])],
            cam(1.0, 1.1, (540, 1150), (560, 1100)), "corte",
            sfx=[(0.1, "roce", -27)])

    @plano(884, "ella, en paz, sin saber nada")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento"),
            pieza("bea_cara_ojos_cerrados", 540, 980, 960, z=0.6, keys=K(d, (0, {"escala": 1.0, "rot": -1.5}), (1, {"escala": 1.05, "rot": 1.5}))),
            brillo(760, 860, 320, "#ffcf8a", 0.4, 0.65, pulso=[0.15, 0.8]),
            pie("lampara_led", 1280, 1300, 160, z=0.5), pie("libro_abierto", -260, 1300, 120, z=0.5),
            *ambiente_cueva(d, sem=21, murc=False)],
            cam(1.0, 1.1, (540, 920)), "corte",
            sfx=[(0.1, "rumor", -28, {"dur": 1.4})])

    # ================================================================== «Piensa en tu caso. Quinientos días.»
    @plano(887, "piensa en tu caso: tú, en tu mesa")
    def _(d):
        return P(["#c7ccd4", "#6b707a"], [
            fondo("bg_oficina_gris"),
            pie("adulto_pantalla", 540, 1440, 560, z=0.55, keys=K(d, (0, {"x": 500}), (1, {"x": 560}))),
            brillo(760, 1150, 200, "#9fd0ff", 0.55, 0.6, pulso=[0.2, 0.5]),
            pie("taza_cafe", -250, 1440, 160, z=0.55), pie("voluntario_6", 1400, 1440, 520, z=0.5),
            ruta("calendario_hoja", 1500, 600, -600, 760, 0.3, d, 120, z=0.4, rot=-200, _ancho=True)],
            cam(1.0, 1.25, (540, 1150), (620, 1080)), "corte",
            sfx=[(0.15, "tic", -26), (0.5, "tic", -28)])

    @plano(891, "quinientos días: el taco se deshoja")
    def _(d):
        hojas = [ruta("calendario_hoja", 540, 900, x, y, 0.15 + 0.16 * i, 0.15 + 0.16 * i + 0.55, 300, z=0.62 + 0.01 * i, esc=(1.0, 0.6), op1=0.0, rot=r)
                 for i, (x, y, r) in enumerate([(-200, 500, -120), (1300, 620, 140), (-150, 1300, -200), (1250, 1250, 160), (540, -200, 90), (-400, 900, -60)])]
        return P(["#c7ccd4", "#6b707a"], [
            fondo("bg_oficina_gris"),
            pieza("calendario_taco", 540, 900, 380, z=0.6, keys=K(d, (0, {"escala": 1.0}), (1, {"escala": 1.06}))), *hojas,
            pie("pantalla_ordenador", -300, 1440, 340, z=0.5), pie("voluntario_6", 1400, 1440, 520, z=0.5)],
            cam(1.1, 1.2, (540, 960)), "corte",
            hud=[contador(0.1, d - 0.05, 0, 500, d * 0.75, " días", tam=110, x=540, y=1250, color="#ffd23f", capsula="#0b0f1ee6", miles=False)],
            sfx=[(0.15 + 0.16 * i, "roce", -26) for i in range(0, 6, 2)])

    # ================================================================== ráfaga: «Se juegan finales. Hay elecciones. …»
    @plano(893, "se juegan: el estadio ruge (micro)")
    def _(d):
        return P(["#0b1a2e", "#0d3b1e"], [
            fondo("bg_estadio_noche"),
            *[pie(n, x, 1395, 380, z=0.55, keys=late(0.0, 2, 0.07, 0.25)) for n, x in [("voluntario_1", 130), ("voluntario_4", 380), ("voluntario_2", 700),
                                                                                   ("voluntario_6", 950), ("voluntario_3", -350), ("voluntario_5", 1430)]],
            {**polvo("#ffd23f", 60, (-500, 400, 1600, 1200), 5), "vel": [40, 80], "_ancho": True}],
            cam(1.0, 1.12, (540, 1100)), "corte",
            hud=contador_dias(d),
            sfx=[(0.02, "rumor", -22, {"dur": 0.6})])

    @plano(895, "finales: el trofeo sube")
    def _(d):
        return P(["#0b1a2e", "#0d3b1e"], [
            fondo("bg_estadio_noche"),
            pie("trofeo", 540, 1395, 520, z=0.6, keys=[{"t": 0, "y": cy("trofeo", 1395, 520) + 500}, {"t": 0.3, "y": cy("trofeo", 1395, 520), "ease": "anticipa"},
                                                       *late(0.35, 1, 0.1)]),
            pieza("destello", 610, 1000, 420, z=0.65, keys=[{"t": 0, "op": 0, "escala": 0.2}, {"t": 0.28, "op": 0, "escala": 0.2},
                                                            {"t": 0.42, "op": 1, "escala": 1.0, "ease": "salida"}, {"t": d, "op": 0, "rot": 40}]),
            pie("voluntario_3", -330, 1395, 420, z=0.5, keys=late(0.3, 1, 0.06)), pie("voluntario_5", 1420, 1395, 420, z=0.5, keys=late(0.3, 1, 0.06)),
            {**polvo("#ffffff", 50, (0, 500, 1080, 1100), 5), "vel": [30, -60]}],
            cam(1.1, 1.3, (540, 1150), (540, 1100)), "corte",
            hud=contador_dias(d),
            sfx=[(0.0, "whoosh", -14), (0.3, "golpe", -18), (0.42, "brillo", -24)])

    @plano(896, "hay elecciones: el voto cae en la urna")
    def _(d):
        yu = cy("urna_voto", 1390, 380)
        return P(["#1b1a3a", "#0b0b16"], [
            fondo("bg_ciudad"),
            pie("urna_voto", 540, 1390, 380, z=0.6, keys=late(0.5, 1, 0.05)),
            IMG("carta", ancho=170, x=560, y=520, z=0.62, keys=[{"t": 0, "y": 520, "rot": -15}, {"t": 0.45, "y": yu - 170, "rot": 0, "ease": "entrada"},
                                                              {"t": 0.5, "y": yu - 120, "op": 0}]),
            IMG("carta", ancho=150, x=480, y=400, z=0.61, keys=[{"t": 0, "op": 0}, {"t": 0.55, "op": 1, "y": 400, "rot": 10},
                                                              {"t": 0.95, "y": yu - 170, "rot": 0, "ease": "entrada"}, {"t": 1.0, "y": yu - 120, "op": 0}]),
            pie("voluntario_2", 160, 1390, 440, z=0.55), pie("voluntario_6", 930, 1390, 440, z=0.55, keys=K(d, (0, {"x": 960}), (1, {"x": 920}))),
            pie("voluntario_1", -380, 1390, 440, z=0.5), pie("voluntario_4", 1450, 1390, 440, z=0.5)],
            cam(1.05, 1.18, (540, 1150)), "corte",
            hud=contador_dias(d),
            sfx=[(0.47, "tic", -20), (0.97, "tic", -22)])

    @plano(898, "sale música nueva")
    def _(d):
        notas = []
        for i, (n, x, y, a) in enumerate([("nota_musical_a", 300, 900, 200), ("nota_musical_b", 760, 820, 260), ("nota_musical_a", 600, 1150, 150),
                                          ("nota_musical_b", -300, 900, 220), ("nota_musical_a", 1400, 850, 220)]):
            notas.append(pieza(n, x, y, a, z=0.6 + 0.01 * i, anim={"balanceo": [12, 0.5]},
                               keys=[*aparece(0.08 + 0.18 * i, 0.35), {"t": 0.08 + 0.18 * i, "y": y + 60}, {"t": d, "y": y - 140, "ease": "lineal"}]))
        return P(["#6fb6e8", "#e8c98a"], [
            fondo("bg_playa_verano"),
            pie("voluntario_4", 300, 1350, 470, z=0.55, anim={"balanceo": [6, 0.45]}),
            pie("voluntario_5", 800, 1350, 470, z=0.55, anim={"balanceo": [-6, 0.5]}),
            pie("balon_playa", 560, 1350, 130, z=0.56, keys=[{"t": 0, "y": cy("balon_playa", 1350, 130)}, *cae(0.1, 0.7, cy("balon_playa", 1350, 130) - 300,
                                                                                                             cy("balon_playa", 1350, 130))]),
            *notas, pie("helado", -400, 1350, 260, z=0.5)],
            cam(1.0, 1.12, (540, 1050)), "corte",
            hud=contador_dias(d),
            sfx=[(0.08, "pop", -24), (0.44, "pop", -26), (0.62, "golpe", -26), (0.8, "pop", -26)])

    @plano(901, "teléfonos: el viejo tiembla y sale (micro)")
    def _(d):
        return P(["#141a3a", "#05060f"], [
            brillo(540, 960, 520, "#5f7bff", 0.35, 0.08, pulso=[0.1, 0.8]),
            {**polvo("#9fc4ff", 40, (-600, 400, 1700, 1500), 13), "_ancho": True},
            pieza("telefono_movil", 540, 930, 320, z=0.6, keys=[{"t": 0, "x": 540, "rot": -6}, {"t": 0.1, "rot": 6}, {"t": 0.2, "rot": -6}, {"t": 0.28, "x": 540, "rot": 4},
                                                              {"t": d, "x": -300, "rot": -30, "ease": "anticipa"}]),
            pieza("telefono_movil", -450, 1000, 200, z=0.4, keys=K(d, (0, {"rot": -10}), (1, {"rot": 0}))),
            pieza("telefono_movil", 1520, 950, 200, z=0.4, keys=K(d, (0, {"rot": 10}), (1, {"rot": 0})))],
            cam(1.0, 1.06, (540, 930)), "corte",
            hud=contador_dias(d),
            sfx=[(0.05, "zap", -24), (0.3, "whoosh", -16)])

    @plano(902, "nuevos: llega el teléfono nuevo")
    def _(d):
        return P(["#141a3a", "#05060f"], [
            brillo(540, 960, 520, "#2ff3ff", 0.35, 0.08, pulso=[0.1, 0.5]),
            {**polvo("#9fc4ff", 40, (-600, 400, 1700, 1500), 14), "_ancho": True},
            pieza("telefono_movil_b", 540, 930, 340, z=0.62, keys=[{"t": 0, "x": 1300, "rot": 20}, {"t": 0.25, "x": 540, "rot": 0, "ease": "rebote"}, {"t": d, "rot": 4}]),
            pieza("destello", 640, 720, 300, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0.3}, {"t": 0.22, "op": 0, "escala": 0.3}, {"t": 0.32, "op": 1, "escala": 1.0},
                                                         {"t": d, "op": 0, "rot": 45}]),
            pieza("telefono_movil_b", -450, 1000, 200, z=0.4, keys=aparece(0.15)),
            pieza("telefono_movil_b", 1520, 950, 200, z=0.4, keys=aparece(0.25))],
            cam(1.05, 1.15, (540, 930)), "corte",
            hud=contador_dias(d),
            sfx=[(0.25, "brillo", -22)])

    @plano(903, "bromas nuevas: todos se ríen")
    def _(d):
        gente = [("voluntario_1", 170), ("voluntario_2", 420), ("voluntario_4", 670), ("voluntario_6", 920), ("voluntario_3", -330), ("voluntario_5", 1420)]
        return P(["#c7ccd4", "#6b707a"], [
            fondo("bg_oficina_gris"),
            *[pie(n, x, 1440, 470, z=0.55 + 0.01 * i, keys=[{"t": 0, "rot": 0}, *late(0.05 + 0.07 * i, 3, 0.05, 0.28),
                                                           {"t": 0.3, "rot": (-1) ** i * 4}, {"t": d, "rot": (-1) ** (i + 1) * 3}])
              for i, (n, x) in enumerate(gente)],
            pie("taza_cafe", 560, 1440, 110, z=0.6)],
            cam(1.08, 1.0, (540, 1150)), "corte",
            hud=contador_dias(d),
            sfx=[(0.05, "burbuja", -24, {"f": 500}), (0.35, "burbuja", -25, {"f": 650}), (0.65, "burbuja", -25, {"f": 560})])

    @plano(905, "que no vas a entender: ella parpadea")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento"),
            *flip(["bea_cara_neutra", "bea_cara_parpadea", "bea_cara_neutra", "bea_cara_neutra"], d, fps=6,
                  base=lambda n: pieza(n, 540, 990, 940, z=0.6, keys=K(d, (0, {"rot": 0}), (0.4, {"rot": -5, "ease": "suave"}), (1, {"rot": -7})))),
            brillo(330, 760, 300, "#ffcf8a", 0.35, 0.65),
            *ambiente_cueva(d, sem=22, murc=False)],
            cam(1.0, 1.08, (540, 940)), "corte",
            hud=contador_dias(d),
            sfx=[(0.2, "tic", -28)])

    @plano(910, "gente que conoces tiene hijos: la cuna")
    def _(d):
        S = 1480
        tb = 1.42
        return P(["#4a2e20", "#1d120c"], [
            fondo("bg_ventana_invierno"),
            pie("cuna", 540, S, 520, z=0.55),
            pie("bebe", 540, S - 150, 260, z=0.57, keys=[{"t": 0, "op": 0}, *aparece(tb, 0.45), *late(tb + 0.5, 1, 0.06)]),
            pie("voluntario_2", 150, S, 560, z=0.6, keys=[*arranque(150, cy("voluntario_2", S, 560), d, "izquierda", 200, 20)]),
            pie("voluntario_1", 930, S, 580, z=0.6, keys=[*arranque(930, cy("voluntario_1", S, 580), d, "derecha", 200, 20)]),
            pieza("destello", 560, 1180, 260, z=0.7, keys=[{"t": 0, "op": 0}, {"t": tb, "op": 0, "escala": 0.3}, {"t": tb + 0.15, "op": 0.9, "escala": 1.0},
                                                          {"t": tb + 0.6, "op": 0}]),
            pie("ovillo_lana", -300, S, 110, z=0.55), pie("gorro_lana_b", 1350, S, 120, z=0.55),
            {**polvo("#ffffff", 30, (240, 480, 840, 1060), 6), "vel": [10, 40]}],
            cam(1.0, 1.15, (540, 1200), (540, 1250)), "corte",
            hud=contador_dias(d),
            sfx=[(tb, "ding", -24)])

    @plano(915, "gente que conoces se muere: una flor blanca")
    def _(d):
        return P(["#1c1626", "#07070c"], [
            brillo(540, 960, 520, "#6a5a8a", 0.35, 0.08),
            {**polvo("#fff1c8", 26, (-500, 500, 1580, 1400), 15), "vel": [3, -8], "_ancho": True},
            pieza("flor_blanca", 540, 980, 520, z=0.6, keys=K(d, (0, {"escala": 0.96, "rot": -1}), (1, {"escala": 1.02, "rot": 1}))),
            brillo(700, 1170, 160, "#ffcf8a", 0.6, 0.62, pulso=[0.2, 0.7]),
            ruta("hoja_otono", 380, 600, 300, 1400, 0.2, d, 90, z=0.7, rot=120),
            pieza("vela_corta", -320, 1100, 120, z=0.5), pieza("vela_corta", 1400, 1100, 120, z=0.5)],
            cam(1.0, 1.08, (540, 980)), "corte", vineta=0.75,
            hud=contador_dias(d),
            sfx=[(0.2, "brillo", -30)])

    # ================================================================== «Y tú sigues ahí, leyendo tu libro, convencido de que queda muchísimo.»
    @plano(920, "y tú sigues ahí, leyendo (respiro)")
    def _(d):
        return P(["#3d2a1f", "#0b0705"], [
            fondo("bg_cueva_campamento"),
            pie("colchon", 560, 1320, 210, z=0.45),
            *flip(["bea_lee_a", "bea_lee_b"], d, fps=0.9, base=lambda n: pie(n, 540, 1320, 470, z=0.5)),
            pie("lampara_led", 830, 1320, 170, z=0.52),
            brillo(820, 1200, 320, "#ffcf8a", 0.55, 0.51, pulso=[0.06, 1.8]),
            pie("libro_c", 220, 1320, 70, z=0.52), pie("libro_d", 220, 1270, 70, z=0.53), pie("libro_a", 230, 1220, 70, z=0.54),
            pie("tienda_campana", -330, 1300, 260, z=0.45), pie("mesa_campamento", 1400, 1300, 240, z=0.45),
            pie("garrafa_agua", 1180, 1300, 140, z=0.5),
            *ambiente_cueva(d, sem=23, primer_plano="rocas_primer_plano_b")],
            cam(1.15, 1.0, (560, 1120)), "corte",
            sfx=[(0.1, "rumor", -26, {"dur": 2.4}), (1.1, "roce", -28)], energia=0.35)

    @plano(927, "convencida de que queda muchísimo")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento"),
            pieza("bea_cara_rie", 540, 990, 960, z=0.6, keys=K(d, (0, {"escala": 1.0, "x": 520}), (1, {"escala": 1.06, "x": 560}))),
            brillo(300, 700, 320, "#ffcf8a", 0.4, 0.65, pulso=[0.1, 1.2]),
            pie("vela_a", -260, 1300, 300, z=0.5), brillo(-260, 1050, 90, "#ffcf8a", 0.6, 0.51, pulso=[0.2, 0.3]),
            pie("libro_abierto", 1320, 1300, 140, z=0.5),
            *ambiente_cueva(d, sem=24, murc=False)],
            cam(1.0, 1.08, (540, 920)), "corte", sfx=[(0.3, "brillo", -28)], energia=0.35)

    # ================================================================== «Y ahora la gran pregunta.» (subida → impacto)
    @plano(932, "y ahora la gran pregunta: la galería se cierra")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_galeria"),
            brillo(540, 900, 220, "#fff1c8", 0.35, 0.3, pulso=[0.2, 0.4]),
            *ambiente_cueva(d, sem=25, oscura=True),
            negro(K(d, (0, {"op": 0.0}), (0.6, {"op": 0.0}), (1, {"op": 0.55, "ease": "entrada"})))],
            cam(1.0, 1.45, (540, 1000), (540, 900)), "desenfoque",
            sfx=[(0.1, "rumor", -24, {"dur": 1.0})])

    @plano(935, "la gran pregunta: su cara de cerca")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            pieza("bea_cara_neutra", 540, 990, 960, z=0.6, keys=K(d, (0, {"escala": 1.0}), (1, {"escala": 1.12, "ease": "entrada"}))),
            brillo(540, 760, 300, "#ffcf8a", 0.3, 0.65)],
            cam(1.0, 1.35, (540, 880), (540, 820)), "corte", vineta=0.85,
            sfx=[(0.04, "subida", -18, {"dur": 1.0})])

    @plano(937, "¿cómo puede alguien perder…?: impacto")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            pieza("bea_cara_miedo", 540, 990, 960, z=0.6, keys=K(d, (0, {"escala": 1.12}), (0.2, {"escala": 1.0, "ease": "golpe"}), (1, {"escala": 1.04}))),
            fundido_blanco(K(d, (0, {"op": 0.9}), (0.18, {"op": 0.0}))),
            brillo(540, 600, 320, "#ffcf8a", 0.45, 0.65, pulso=[0.15, 0.3]),
            *ambiente_cueva(d, sem=26, oscura=True, murc=False)],
            cam(1.15, 1.0, (540, 920), temblor=6), "corte",
            sfx=[(0.0, "impacto", -12)])

    @plano(941, "casi un año: las hojas salen volando")
    def _(d):
        r = random.Random(41)
        hojas = []
        for i in range(10):
            ang = i / 10 * 6.283
            x1, y1 = 540 + 1100 * math.cos(ang), 940 + 900 * math.sin(ang)
            hojas.append(ruta("calendario_hoja", 540, 940, x1, y1, 0.02 + 0.05 * i, 0.5 + 0.05 * i, 280, z=0.6 + 0.005 * i,
                              esc=(1.0, 0.5), rot=r.choice([-1, 1]) * r.uniform(120, 300), _ancho=True))
        return P(["#141018", "#050507"], [
            fondo("bg_negro_cueva"),
            brillo(540, 940, 420, "#ffcf8a", 0.35, 0.1),
            pieza("calendario_taco", 540, 940, 300, z=0.55, keys=K(d, (0, {"escala": 1.0}), (1, {"escala": 0.9}))), *hojas],
            cam(1.0, 1.12, (540, 940)), "corte",
            hud=[amarillo(0.02, d - 0.03, "≈ 1 AÑO", y=1250, tam=110)],
            sfx=[(0.05, "whoosh", -15), (0.3, "roce", -24)])

    @plano(944, "sin darse cuenta: duerme, perdida en la oscuridad")
    def _(d):
        return P(["#141018", "#050507"], [
            fondo("bg_negro_cueva"),
            pie("bea_duerme", 540, 1344, 170, z=0.5, keys=late(0.2, 1, 0.02, 1.0)),
            pie("lampara_led", 700, 1344, 80, z=0.52),
            brillo(700, 1300, 160, "#ffcf8a", 0.5, 0.51, keys=K(d, (0, {"op": 1}), (1, {"op": 0.35}))),
            *ambiente_cueva(d, sem=27, oscura=True)],
            cam(1.7, 1.0, (560, 1310), (540, 1100)), "corte",
            sfx=[(0.2, "rumor", -26, {"dur": 1.1})])

    # ================================================================== «La respuesta es que tu cerebro no tiene ningún cronómetro…»
    @plano(947, "la respuesta: dentro de la cabeza")
    def _(d):
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_seccion_cabeza"),
            brillo(505, 699, 260, "#2ff3ff", 0.35, 0.3, pulso=[0.2, 0.6]),
            {**polvo("#2ff3ff", 30, (-500, 300, 1580, 1500), 17), "_ancho": True},
            senala(505, 699, 0.6, d - 0.05, 250, CIAN)],
            cam(1.0, 1.35, (540, 960), (505, 760)), "zoom",
            sfx=[(0.6, "senal", -26)])

    @plano(952, "tu cerebro: aparece dentro")
    def _(d):
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_seccion_cabeza"),
            brillo(505, 699, 300, "#ff3df2", 0.4, 0.3, pulso=[0.15, 0.5]),
            pieza("cerebro", 505, 699, 420, z=0.6, keys=[*aparece(0.05, 0.45), {"t": 0.5, "rot": -3}, {"t": d, "rot": 3}]),
            {**polvo("#ff3df2", 26, (-500, 300, 1580, 1500), 18), "_ancho": True}],
            cam(1.25, 1.4, (505, 760), (505, 720)), "corte",
            sfx=[(0.05, "pop", -20)])

    @plano(955, "ningún cronómetro para los meses: los meses rebotan")
    def _(d):
        hojas = []
        for i, (x0, y0, x1, y1) in enumerate([(-400, 600, 1400, 300), (1500, 1300, -300, 1500), (540, -200, 1400, 1500)]):
            t0 = 0.15 + 0.45 * i
            xm, ym = 540 + (x0 - 540) * 0.35, 900 + (y0 - 900) * 0.35
            hojas.append(IMG("calendario_hoja", ancho=200, x=x0, y=y0, z=0.65,
                             keys=[{"t": 0, "op": 0, "x": x0, "y": y0}, {"t": t0, "op": 1, "x": x0, "y": y0, "rot": 0},
                                   {"t": t0 + 0.3, "x": xm, "y": ym, "rot": 20, "ease": "entrada"},
                                   {"t": t0 + 0.75, "x": x1, "y": y1, "rot": 220, "op": 0.0, "ease": "salida"}], _ancho=True))
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_cerebro"),
            pieza("cerebro", 540, 900, 600, z=0.6, keys=[{"t": 0, "escala": 1.0}, *late(0.45, 3, 0.06, 0.45)]),
            brillo(540, 900, 380, "#2ff3ff", 0.3, 0.3), *hojas],
            cam(1.0, 1.1, (540, 940)), "corte",
            sfx=[(0.45 + 0.45 * i, "zap", -24) for i in range(3)])

    @plano(960, "no cuenta el tiempo: las rayas se borran")
    def _(d):
        rayas = []
        for i in range(12):
            x = 180 + 64 * i + (20 if i % 5 == 4 else 0)
            r = tiza(x, 1180, 0.03 + 0.05 * i, 200, z=0.6)
            r["keys"] += [{"t": 0.9, "op": 1, "y": 1180}, {"t": 1.35, "op": 0, "y": 1260, "ease": "entrada"}]
            rayas.append(r)
        lat = [tiza(-560 + 64 * i, 1150, 0.05 * i, 180) for i in range(7)] + [tiza(1180 + 64 * i, 1150, 0.05 * i, 180) for i in range(7)]
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_cerebro"),
            pieza("cerebro", 540, 720, 440, z=0.55, keys=[{"t": 0, "rot": 0}, {"t": 0.85, "rot": 0}, {"t": 1.0, "rot": -8}, {"t": 1.15, "rot": 8},
                                                          {"t": 1.3, "rot": -5}, {"t": 1.45, "rot": 0}]),
            *rayas, *lat],
            cam(1.05, 1.0, (540, 940)), "corte",
            sfx=[(0.03 + 0.1 * i, "tic", -27) for i in range(6)] + [(1.0, "roce", -24)])

    @plano(964, "cuenta recuerdos: el primero entra")
    def _(d):
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_cerebro"),
            pieza("cerebro", 540, 820, 560, z=0.55, keys=K(d, (0, {"op": 1}), (0.4, {"op": 1}), (0.55, {"op": 0}))),
            pieza("cerebro_brillo", 540, 820, 560, z=0.56, keys=[{"t": 0, "op": 0}, {"t": 0.4 * d, "op": 0}, {"t": 0.55 * d, "op": 1}, *late(0.55 * d, 1, 0.08)]),
            ruta("recuerdo_1", 540, 1340, 540, 820, 0.05, 0.5 * d, 260, z=0.6, esc=(1.0, 0.15), op1=0.0, rot=-10),
            ruta("recuerdo_3", 1500, 1300, 560, 820, 0.4, 0.85 * d, 220, z=0.6, esc=(1.0, 0.15), op1=0.0, rot=15, _ancho=True),
            ruta("recuerdo_4", -500, 1300, 520, 820, 0.5, 0.9 * d, 220, z=0.6, esc=(1.0, 0.15), op1=0.0, rot=-15, _ancho=True),
            brillo(540, 820, 360, "#ff3df2", 0.35, 0.3, pulso=[0.2, 0.5])],
            cam(1.0, 1.15, (540, 900), (540, 860)), "corte",
            sfx=[(0.5 * d, "ding", -22)])

    # ================================================================== «Cuando miras hacia atrás y te preguntas cuánto ha pasado,»
    @plano(966, "miras hacia atrás: la estela de recuerdos")
    def _(d):
        pos = [(330, 860, 240), (190, 1020, 200), (90, 1180, 170), (300, 1270, 150), (-120, 1060, 200), (-330, 1180, 170), (-520, 1000, 150)]
        recs = []
        for i, (x, y, a) in enumerate(pos):
            t0 = 0.15 + 0.32 * i
            recs.append(pieza(f"recuerdo_{i + 2}", x, y, a, z=0.6 - 0.01 * i,
                              keys=[*aparece(t0, 0.4), {"t": t0, "rot": (-1) ** i * 8}, {"t": d, "rot": (-1) ** i * 3, "x": x - 40}]))
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_seccion_cabeza"),
            pieza("cerebro_brillo", 505, 699, 400, z=0.55, keys=K(d, (0, {"rot": 0}), (1, {"rot": -4}))),
            brillo(505, 699, 300, "#2ff3ff", 0.35, 0.3, pulso=[0.1, 0.8]),
            flecha([[380, 760], [250, 900], [140, 1060], [60, 1260]], 0.2, 2.4, CIAN, 7, [16, 14]),
            *recs],
            cam(1.0, 1.12, (505, 860), (380, 960)), "corte",
            sfx=[(0.15 + 0.32 * i, "pop", -27) for i in range(0, 7, 2)])

    # ================================================================== «tu cerebro hace una trampa:»
    @plano(976, "tu cerebro hace una trampa")
    def _(d):
        tt = 1.26   # «trampa»
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_cerebro"),
            *flip(["cerebro", "cerebro_brillo"], d, fps=5, t0=tt, base=lambda n: pieza(n, 540, 900, 620, z=0.6,
                  keys=[{"t": 0, "escala": 0.9}, {"t": tt, "escala": 1.0, "ease": "suave"}, {"t": tt + 0.2, "escala": 1.12, "ease": "golpe"},
                        {"t": d, "escala": 1.05}])),
            brillo(540, 900, 480, "#ff3df2", 0.4, 0.3, keys=[{"t": 0, "op": 0.3}, {"t": tt, "op": 0.3}, {"t": tt + 0.15, "op": 1.0}, {"t": d, "op": 0.6}]),
            *[pieza(f"recuerdo_{i}", x, y, 150, z=0.5, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 25 * (-1) ** i}], anim={"flotar": [14, 1.2]})
              for i, (x, y) in zip(range(1, 7), [(-420, 700), (-250, 1250), (1350, 650), (1500, 1200), (170, 520), (930, 560)])]],
            cam(1.0, 1.08, (540, 920), temblor=0), "corte",
            hud=[amarillo(tt, d - 0.05, "TRAMPA", y=1300, tam=110, color=MAGENTA)],
            sfx=[(tt, "zap", -18), (tt + 0.1, "golpe", -24)])

    # ================================================================== «mira cuántos recuerdos distintos tiene guardados.»
    GRID = [(200, 720), (420, 720), (660, 720), (880, 720), (200, 1020), (420, 1020), (660, 1020), (880, 1020)]

    @plano(981, "mira cuántos recuerdos: aparecen en rejilla")
    def _(d):
        recs = [pieza(f"recuerdo_{i + 1}", x, y, 190, z=0.6, keys=[{"t": 0, "op": 1 if i < 2 else 0, "escala": 0.55, "rot": 0}, {"t": 0.09 * i, "op": 1, "escala": 0.55},
                                                                {"t": 0.09 * i + 0.3, "escala": 1.0, "rot": (-1) ** i * 5, "ease": "elastico"}])
                for i, (x, y) in enumerate(GRID)]
        lat = [pieza(f"recuerdo_{i}", x, y, 170, z=0.5, keys=aparece(0.2 + 0.1 * i, 0.35))
               for i, (x, y) in zip([5, 7, 2, 8], [(-300, 780), (-500, 1000), (1380, 780), (1580, 1000)])]
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_cerebro"), brillo(540, 870, 480, "#2ff3ff", 0.25, 0.3), *recs, *lat],
            cam(1.0, 1.06, (540, 900)), "corte",
            hud=[contador(0.1, d - 0.05, 1, 8, 0.85, " recuerdos", tam=96, x=540, y=1280, color="#2ff3ff", capsula="#0b0f1ee6")],
            sfx=[(0.05 + 0.2 * i, "tic", -25) for i in range(4)])

    @plano(984, "distintos, guardados: entran en el cerebro uno a uno")
    def _(d):
        recs = []
        for i, (x, y) in enumerate(GRID):
            t0 = 0.1 + 0.2 * i
            recs.append(pieza(f"recuerdo_{i + 1}", x, y, 190, z=0.62, keys=[{"t": 0, "op": 1, "x": x, "y": y, "escala": 1.0}, {"t": t0, "x": x, "y": y, "escala": 1.0},
                                                                            {"t": t0 + 0.3, "x": 540, "y": 900, "escala": 0.12, "op": 0.0, "ease": "entrada"}]))
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_cerebro"),
            pieza("cerebro", 540, 900, 520, z=0.55, keys=[*aparece(0.0, 0.3), *late(0.45, 7, 0.04, 0.2)]),
            pieza("cerebro_brillo", 540, 900, 520, z=0.56, keys=[{"t": 0, "op": 0}, {"t": 0.4, "op": 0}, {"t": 1.9, "op": 1}]),
            brillo(540, 900, 420, "#ff3df2", 0.35, 0.3, pulso=[0.15, 0.4]), *recs,
            pieza("recuerdo_6", -400, 900, 180, z=0.5, keys=K(d, (0, {"x": -400}), (1, {"x": -250, "rot": 10}))),
            pieza("recuerdo_2", 1480, 900, 180, z=0.5, keys=K(d, (0, {"x": 1480}), (1, {"x": 1330, "rot": -10})))],
            cam(1.0, 1.12, (540, 900)), "corte",
            sfx=[(0.4 + 0.2 * i, "burbuja", -26, {"f": 700 + 60 * i}) for i in range(0, 8, 2)])

    # ================================================================== «Muchos recuerdos nuevos, mucho tiempo. Pocos recuerdos, poco tiempo.»
    @plano(987, "muchos recuerdos: una fila larga, mucho tiempo")
    def _(d):
        tm = w(990) - w(987)   # «mucho tiempo»
        xs = [-560 + 124 * i for i in range(19)]
        recs = [pieza(f"recuerdo_{i % 8 + 1}", x, 820 + (18 if i % 2 else -18), 112, z=0.6,
                      keys=[*aparece(0.05 + 0.07 * j, 0.3), {"t": 0.05 + 0.07 * j, "rot": (-1) ** i * 6}], _ancho=False)
                for j, (i, x) in enumerate(sorted(enumerate(xs), key=lambda q: abs(q[1] - 540)))]
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_cerebro"), brillo(540, 820, 500, "#2ff3ff", 0.2, 0.3),
            *recs,
            flecha([[60, 1040], [1020, 1040]], tm, tm + 0.8, LIMA, 10),
            flecha([[1020, 1040], [60, 1040]], tm, tm + 0.8, LIMA, 10),
            flecha([[-560, 1040], [40, 1040]], tm, tm + 0.8, LIMA, 6, punta=False), flecha([[1040, 1040], [1640, 1040]], tm, tm + 0.8, LIMA, 6, punta=False)],
            cam(1.12, 1.0, (540, 900)), "corte",
            sfx=[(0.05 + 0.14 * i, "tic", -27) for i in range(6)] + [(tm, "trazo", -20)])

    @plano(992, "pocos recuerdos: una fila corta, poco tiempo")
    def _(d):
        tp = w(994) - w(992)   # «poco tiempo»
        largos = [IMG(f"recuerdo_{i % 8 + 1}", ancho=80, x=-560 + 124 * i, y=640, z=0.5, op=0.35) for i in range(19)]
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_cerebro"), brillo(380, 1100, 380, "#ff3df2", 0.2, 0.3),
            *largos,
            flecha([[60, 730], [1020, 730]], 0.0, 0.01, "#7dff3a66", 5, punta=False),
            pieza("recuerdo_cueva", 330, 1050, 150, z=0.6, keys=[*aparece(0.1, 0.35), {"t": 0.1, "rot": -6}]),
            pieza("recuerdo_5", 490, 1050, 150, z=0.6, keys=[*aparece(0.3, 0.35), {"t": 0.3, "rot": 6}]),
            flecha([[260, 1220], [560, 1220]], tp, tp + 0.4, MAGENTA, 10),
            flecha([[560, 1220], [260, 1220]], tp, tp + 0.4, MAGENTA, 10)],
            cam(1.0, 1.1, (540, 900), (460, 1000)), "corte",
            sfx=[(0.1, "pop", -25), (0.3, "pop", -26), (tp, "trazo", -22)])

    # ================================================================== «Y en una cueva, todos los días son el mismo día.»
    @plano(996, "y en una cueva")
    def _(d):
        return P(["#3d2a1f", "#0b0705"], [
            fondo("bg_cueva_campamento"),
            *flip(["bea_teje_a", "bea_teje_b"], d, fps=3, base=lambda n: pie(n, 500, 1300, 400, z=0.5)),
            pie("lampara_led", 760, 1300, 140, z=0.52), brillo(750, 1210, 260, "#ffcf8a", 0.55, 0.51, pulso=[0.08, 1.4]),
            pie("tienda_campana", -330, 1300, 260, z=0.45), pie("garrafa_agua", 1250, 1300, 150, z=0.5), pie("caja_comida", 1500, 1300, 150, z=0.5),
            *ambiente_cueva(d, sem=31)],
            cam(1.0, 1.15, (540, 700), (540, 1100)), "corte",
            sfx=[(0.1, "rumor", -26, {"dur": 1.2})])

    @plano(1000, "todos los días, el mismo día: hojas idénticas caen una encima de otra")
    def _(d):
        yh = 900
        hojas = [pieza("calendario_hoja", 540, yh, 360, z=0.6 + 0.01 * i, keys=[{"t": 0, "op": 0}, {"t": 0.05 + 0.5 * i, "op": 1},
                                                                             *cae(0.05 + 0.5 * i, 0.4 + 0.5 * i, 300, yh, 0.08)]) for i in range(5)]
        return P(["#3d2a1f", "#0b0705"], [
            fondo("bg_cueva_campamento"), brillo(540, 900, 380, "#ffcf8a", 0.35, 0.3),
            *hojas,
            *[pieza("calendario_hoja", x, 950, 260, z=0.5, op=0.85, keys=K(d, (0, {"rot": r}), (1, {"rot": -r}))) for x, r in [(-380, 6), (1460, -6)]],
            *ambiente_cueva(d, sem=32, murc=True)],
            cam(1.0, 1.1, (540, 940)), "corte",
            sfx=[(0.3 + 0.5 * i, "golpe", -27) for i in range(5)])

    # ================================================================== «La misma roca, la misma luz, la misma rutina.» (planos idénticos a propósito)
    def mismo(d, n_dia, accion):
        """El mismo encuadre exacto; solo cambian el número del día y un detalle mínimo."""
        lee = (flip(["bea_lee_a", "bea_lee_b"], d, fps=1 / 0.35, t0=0.35, base=lambda n: pie(n, 540, 1300, 360, z=0.5))
               if accion == "rutina" else [pie("bea_lee_a", 540, 1300, 360, z=0.5)])
        luz = (brillo(740, 1210, 260, "#ffcf8a", 0.6, 0.51, keys=[{"t": 0, "op": 1}, {"t": 0.3, "op": 1}, {"t": 0.36, "op": 0.2}, {"t": 0.44, "op": 1},
                                                                  {"t": 0.6, "op": 0.3}, {"t": 0.7, "op": 1}])
               if accion == "luz" else brillo(740, 1210, 260, "#ffcf8a", 0.6, 0.51))
        roca = ([senala(860, 1140, 0.15, d - 0.1, 120, AMBAR)] if accion == "roca" else [])
        return P(["#3d2a1f", "#0b0705"], [
            fondo("bg_cueva_campamento"), *lee, pie("lampara_led", 740, 1300, 130, z=0.52), luz,
            pie("estalagmita_a", 860, 1300, 220, z=0.48), *roca, pie("libro_c", 330, 1300, 55, z=0.52), pie("libro_a", 330, 1262, 55, z=0.53),
            pie("tienda_campana", -330, 1300, 260, z=0.45), pie("garrafa_agua", 1250, 1300, 150, z=0.5), pie("estalagmita_b", 1500, 1300, 200, z=0.45),
            *ambiente_cueva(d, sem=33, murc=False)],
            cam(1.1, 1.14, (540, 1100)), "corte",
            hud=[rotulo(0.05, d - 0.05, f"DÍA {n_dia}", tam=70, color="#ffffff", capsula="#0b0f1ee6", x=540, y=560)],
            sfx=[(0.05, "tic", -24)] + ([(0.36, "zap", -28)] if accion == "luz" else []) + ([(0.35, "roce", -28)] if accion == "rutina" else []))

    @plano(1007, "la misma roca (día 212)")
    def _(d):
        return mismo(d, 212, "roca")

    @plano(1010, "la misma luz (día 213)")
    def _(d):
        return mismo(d, 213, "luz")

    @plano(1013, "la misma rutina (día 214)")
    def _(d):
        return mismo(d, 214, "rutina")

    # ================================================================== «Tu cerebro no guarda quinientos días. Guarda uno solo, repetido.»
    @plano(1016, "no guarda quinientos días: llueven recuerdos de cueva")
    def _(d):
        r = random.Random(16)
        recs = []
        for i in range(12):
            x0, y0 = r.uniform(-500, 1600), r.uniform(-300, 200)
            t0 = 0.1 + 0.17 * i
            recs.append(IMG("recuerdo_cueva", ancho=round(r.uniform(150, 210)), x=x0, y=y0, z=0.62 + 0.002 * i,
                            keys=[{"t": 0, "op": 0, "x": x0, "y": y0}, {"t": t0, "op": 1, "x": x0, "y": y0, "rot": r.uniform(-30, 30)},
                                  {"t": t0 + 0.55, "x": 540, "y": 860, "rot": 0, "escala": 0.9, "ease": "entrada"}, {"t": t0 + 0.6, "op": 0}], _ancho=True))
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_cerebro"),
            pieza("cerebro", 540, 860, 560, z=0.55, keys=[*aparece(0.0, 0.3), *late(0.7, 6, 0.04, 0.3)]),
            brillo(540, 860, 380, "#2ff3ff", 0.3, 0.3), *recs],
            cam(1.0, 1.1, (540, 900)), "corte",
            hud=[contador(0.1, d - 0.05, 0, 500, d * 0.8, " días", tam=90, x=540, y=1280, color="#ffffff", capsula="#0b0f1ee6", miles=False)],
            sfx=[(0.65 + 0.34 * i, "burbuja", -27, {"f": 600}) for i in range(5)])

    @plano(1022, "guarda uno solo")
    def _(d):
        fantasmas = [IMG("recuerdo_cueva", ancho=360, x=540 + dx, y=900 + dy, z=0.58, op=0.5,
                         keys=[{"t": 0, "x": 540 + dx, "y": 900 + dy, "op": 0.5, "rot": dx / 20}, {"t": 0.6, "x": 540, "y": 900, "op": 0.0, "rot": 0, "ease": "entrada"}])
                     for dx, dy in [(-380, -260), (380, -240), (-360, 300), (360, 280), (-900, 0), (900, 0)]]
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_cerebro"),
            *fantasmas,
            pieza("recuerdo_cueva", 540, 900, 380, z=0.6, keys=[{"t": 0, "escala": 0.9}, {"t": 0.6, "escala": 1.0, "ease": "suave"}, *late(0.62, 1, 0.1),
                                                              {"t": d, "escala": 1.06}]),
            brillo(540, 900, 420, "#ffcf8a", 0.3, 0.3, keys=[{"t": 0, "op": 0.2}, {"t": 0.6, "op": 1.0}, {"t": d, "op": 0.6}]),
            senala(540, 900, 0.65, d - 0.05, 300, AMBAR)],
            cam(1.0, 1.12, (540, 900)), "corte",
            hud=[rotulo(0.65, d - 0.05, "1", tam=120, color="#ffd23f", capsula="#0b0f1ee6", x=540, y=1300)],
            sfx=[(0.6, "ding", -20)])

    @plano(1025, "repetido: la misma foto en eco")
    def _(d):
        ecos = [IMG("recuerdo_cueva", ancho=340, x=540, y=900, z=0.6 - 0.01 * i,
                    keys=[{"t": 0, "op": 0, "x": 540, "y": 900}, {"t": 0.06 * i, "op": 0.9 - 0.13 * i, "x": 540, "y": 900},
                          {"t": 0.06 * i + 0.3, "x": 540 + 60 * i, "y": 900 - 45 * i, "ease": "salida"}]) for i in range(7)]
        lat = [IMG("recuerdo_cueva", ancho=240, x=x, y=900, z=0.5, op=0.6, keys=K(d, (0, {"rot": r}), (1, {"rot": -r}))) for x, r in [(-400, 8), (1480, -8)]]
        return P(["#1b1340", "#0b0f24"], [
            fondo("bg_cerebro"), brillo(540, 900, 380, "#ffcf8a", 0.25, 0.3), *ecos, *lat],
            cam(1.05, 1.15, (560, 880)), "corte",
            sfx=[(0.06 * i, "tic", -27) for i in range(0, 7, 2)])

    # ================================================================== «Y al hacer la cuenta, le sale muy poco.» (remate)
    @plano(1026, "al hacer la cuenta, le sale muy poco: cinco meses y medio")
    def _(d):
        tp = w(1031) - w(1026)   # «le sale muy poco»
        return P(["#141018", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            pieza("recuerdo_cueva", 540, 640, 240, z=0.6, keys=[*arranque(540, 640, d, "arriba", 160, 10)]),
            flecha([[540, 790], [540, 900]], 0.25, 0.6, AMBAR, 8),
            pieza("cifra_marco", 540, 1040, 500, z=0.6, keys=[*aparece(0.5, 0.4), *late(tp + 0.5, 1, 0.08), {"t": d, "escala": 1.04}]),
            brillo(540, 1040, 300, "#ffcf8a", 0.3, 0.3, pulso=[0.1, 0.6]),
            pie("estalagmita_a", -380, 1344, 300, z=0.5), pie("estalagmita_b", 1460, 1344, 260, z=0.5),
            pie("vela_corta", -150, 1344, 200, z=0.52), brillo(-150, 1190, 80, "#ffcf8a", 0.6, 0.53, pulso=[0.2, 0.35]),
            IMG("recuerdo_cueva", ancho=200, x=1300, y=820, z=0.4, op=0.35, keys=K(d, (0, {"rot": -6}), (1, {"rot": 4}))),
            IMG("recuerdo_cueva", ancho=200, x=-220, y=760, z=0.4, op=0.35, keys=K(d, (0, {"rot": 6}), (1, {"rot": -4}))),
            *ambiente_cueva(d, sem=34, oscura=True, murc=False)],
            cam(1.0, 1.18, (540, 900), (540, 940)), "corte",
            hud=[contador(tp, d - 0.05, 0, 5.5, 0.5, " meses", decimales=1, tam=104, x=540, y=1040, color="#ffd23f", capsula=None, sin_pop=True)],
            sfx=[(0.3, "trazo", -24), (0.5, "pop", -24), (tp, "tic", -27), (tp + 0.2, "tic", -28), (tp + 0.4, "tic", -29), (tp + 0.5, "golpe", -18)])
