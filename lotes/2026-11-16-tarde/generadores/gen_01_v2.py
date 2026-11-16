"""01 v2 (método denso) — Crujirse los nudillos. Uso: python3 gen_01_v2.py DIR_SALIDA DIR_AUDIO"""
import os, sys
from denso import Denso, IMG, BG, brillo, polvo, cam, CIAN, MAGENTA, LIMA, AMBAR

A = sys.argv[2]
D = Denso(sys.argv[1], os.path.join(A, "01-locucion.mp3"), os.path.join(A, "01-alineacion-original.json"))
K, w = D.K, D.w
CALIDO = ["#2a1610", "#120806"]
FRIO = ["#16202c", "#080c12"]
RX = ["#0a1622", "#03070c"]
ART = ["#3a1a22", "#12060a"]
NUD = [(150, 300), (232, 300), (314, 300), (392, 300)]


def nud(i, x, y, ancho, espejo=False):
    k = ancho / 520
    nx, ny = NUD[i]
    nx = 520 - nx if espejo else nx
    return x + (nx - 260) * k, y + (ny - 380) * k


def mano(nombre, x, y, ancho, z=0.5, **kw):
    return IMG(nombre, ancho=ancho, x=x, y=y, z=z, **kw)


def crujir(x, y, ancho, ts, espejo=False, sonido=True):
    els = []
    for j, t in enumerate(ts):
        nx, ny = nud(j % 4, x, y, ancho, espejo)
        els.append(D.destello(nx, ny, t, r=int(80 * ancho / 520)))
        if sonido:
            D.fx(D.INI + t, "tic", -16)
    return els


# detalles de fondo que duran: polilla alrededor de la lámpara del salón, polvo dorado
T_POL0, T_POL1 = w(10) - 0.2, w(41)


def polilla(d):
    return [IMG("polilla", ancho=90, z=0.3, anim={"flotar": [30, 0.35], "balanceo": [25, 0.2]},
                keys=D.recorrido(T_POL0, T_POL1, (60, 620), (420, 520), d))]


def salon(d, *extra):
    return [BG("bg_salon"), *polilla(d), polvo("#ffe9b0", 30, (0, 300, 1080, 1500), 4), *extra]


# ================================================================== planos
@D.plano(0, "gancho: dos manos, una cruje y la otra no")
def _(d):
    return D.P(CALIDO, [brillo(540, 900, 700, "#ffb860", 0.35), mano("mano_izq", 290, 1150, 460, anim={"balanceo": [2, 0.5]}),
               mano("mano_der", 790, 1150, 460, anim={"flotar": [4, 3]}), *crujir(290, 1150, 460, [0.08, 0.5, 0.92])],
               cam(1.0, 1.04, (540, 1100), (540, 1080)), vineta=0.6,
               hud=[D.rotulo(0.0, d - 0.05, "CRAC", tam=80, color="#ffd23f", capsula=None, rot=-8, x=250, y=760),
                    D.rotulo(0.3, d - 0.05, "NUNCA", tam=64, color="#ffffff", capsula="#c0392be6", x=790, y=760)])


@D.plano(7, "micro: primer plano de la izquierda crujiendo")
def _(d):
    return D.P(CALIDO, [brillo(540, 900, 700, "#ffb860", 0.4), mano("mano_izq_roja", 540, 1180, 820, anim={"balanceo": [3, 0.3]}),
               *crujir(540, 1180, 820, [0.05, 0.3, 0.55])], cam(1.25, 1.35, (540, 900), (540, 880)), vineta=0.7)


@D.plano(8, "calendario: 60 años")
def _(d):
    hojas = [IMG(n, ancho=380, x=540, y=1050, z=0.5, rot=r, keys=K(d, (0, {"op": 1 if i == 0 else 0}), (0.3 * i, {"op": 1}),
                 (0.3 * i + 0.28, {"y": 1050}), (0.3 * i + 0.45, {"y": 700, "op": 0 if i < 2 else 1, "rot": r + 30})))
             for i, (n, r) in enumerate([("hoja_1", -4), ("hoja_30", 3), ("hoja_60", -2)])]
    return D.P(CALIDO, [brillo(540, 1000, 600, "#ffb860", 0.35), *hojas[::-1]], cam(1.0, 1.04, (540, 1050), (540, 1050)), vineta=0.65,
               hud=[D.contador(0.05, d - 0.05, 0, 60, d * 0.8, "AÑOS", tam=120, y=1620)], sfx=[(0.3, "tic", -18), (0.6, "tic", -18)])


@D.plano(10, "salón de noche: entra el médico")
def _(d):
    med = IMG("medico", ancho=420, z=0.5, anim={"balanceo": [2, 0.7]}, keys=K(d, (0, {"x": 1250, "y": 1180}), (0.6, {"x": 600, "ease": "salida"})))
    return D.P(CALIDO, salon(d, med), cam(1.0, 1.05, (540, 1100), (560, 1060)), "desenfoque", vineta=0.55,
               hud=[D.contexto(0.1, d - 0.05, "DONALD UNGER")])


@D.plano(14, "era médico: bata y fonendo de cerca")
def _(d):
    return D.P(CALIDO, salon(d, IMG("medico", ancho=420, x=600, y=1180, z=0.5)), cam(2.0, 2.15, (600, 900), (600, 880)), vineta=0.6,
               hud=[D.rotulo(0.05, d - 0.02, "MÉDICO", tam=60, color="#ffffff", capsula="#0d1330d8", x=540, y=1640)])


@D.plano(16, "quería comprobar: piensa")
def _(d):
    return D.P(CALIDO, salon(d, IMG("medico", ancho=420, x=600, y=1180, z=0.5, anim={"balanceo": [1.5, 1.4]}),
               IMG("bocadillo_duda", ancho=300, x=820, y=680, z=0.6, keys=K(d, (0, {"escala": 0}), (0.15, {"escala": 1, "ease": "rebote"})), anim={"flotar": [8, 1.2]})),
               cam(1.3, 1.4, (620, 920), (620, 900)), vineta=0.6, sfx=[(0.1, "pop", -18)])


@D.plano(19, "lo que todos hemos oído: ¡no te crujas!")
def _(d):
    gente = [IMG("persona_casa", ancho=300, x=x, y=1250, z=0.5, rot=r, anim={"balanceo": [3, 0.5 + i * 0.1]}) for i, (x, r) in enumerate([(220, -3), (540, 0), (860, 3)])]
    bocs = [IMG("bocadillo_duda", ancho=200, x=x + 120, y=720, z=0.6, keys=K(d, (0, {"op": 0}), (0.15 + i * 0.15, {"op": 0}), (0.2 + i * 0.15, {"op": 1})))
            for i, x in enumerate((220, 540, 860))]
    return D.P(["#1a2036", "#0c1020"], [BG("bg_pasillo_cerrada"), *gente, *bocs], cam(1.0, 1.04, (540, 1100), (540, 1080)), "desenfoque", vineta=0.6)


@D.plano(26, "crujirse los dedos…")
def _(d):
    return D.P(CALIDO, [brillo(540, 900, 700, "#ffb860", 0.35), mano("mano_izq", 540, 1180, 720, anim={"balanceo": [3, 0.3]}),
               *crujir(540, 1180, 720, [0.1, 0.4])], cam(1.1, 1.2, (540, 1000), (540, 980)), vineta=0.65)


@D.plano(31, "…da artritis: radiografía inflamada")
def _(d):
    return D.P(RX, [brillo(540, 960, 600, "#4fd2ff", 0.25), IMG("rx_artritis", ancho=760, x=540, y=1100, z=0.5),
               brillo(540, 880, 280, "#ff3b2f", 0.5, 0.6, pulso=[0.3, 0.5])], cam(1.0, 1.1, (540, 1050), (540, 940)), "zoom", vineta=0.6,
               hud=[D.amarillo(0.15, d - 0.02, "¿ARTRITIS?")], sfx=[(0.05, "zap", -18)])


@D.plano(32, "el experimento: libreta que cae en la mesa")
def _(d):
    return D.P(CALIDO, salon(d, IMG("cuaderno", ancho=760, x=540, z=0.5, rot=-3, keys=K(d, (0, {"y": 1550, "op": 0}), (0.25, {"y": 1130, "op": 1, "ease": "salida"})))),
               cam(1.0, 1.06, (540, 1100), (540, 1080)), "desenfoque", vineta=0.65,
               hud=[D.amarillo(0.25, d - 0.02, "EXPERIMENTO", y=1720)], sfx=[(0.25, "golpe", -18)])


@D.plano(37, "con su propio cuerpo: el médico se mira las manos")
def _(d):
    return D.P(CALIDO, salon(d, IMG("medico", ancho=460, x=540, y=1200, z=0.5),
               mano("mano_izq", 390, 1420, 240, z=0.6, anim={"balanceo": [4, 0.5]}), mano("mano_der", 690, 1420, 240, z=0.6)),
               cam(1.25, 1.3, (540, 1180), (540, 1200)), vineta=0.6)


@D.plano(41, "izquierda: cada día")
def _(d):
    return D.P(CALIDO, [brillo(540, 900, 700, "#ffb860", 0.4), mano("mano_izq", 540, 1180, 760, anim={"balanceo": [2, 0.4]}),
               *crujir(540, 1180, 760, [0.15 + i * 0.32 for i in range(int(d / 0.32))])],
               cam(1.0, 1.04, (540, 1050), (540, 1050)), vineta=0.65,
               hud=[D.rotulo(0.05, d - 0.02, "IZQUIERDA", tam=64, color="#111111", capsula=LIMA, x=540, y=1660)])


@D.plano(47, "micro: hojas del calendario vuelan")
def _(d):
    return D.P(CALIDO, [brillo(540, 1000, 600, "#ffb860", 0.35),
               *[IMG(n, ancho=300, z=0.5, rot=r, keys=K(d, (0, {"x": 540, "y": 1050, "op": 1}), (0.35 + i * 0.12, {"x": 540, "y": 1050, "op": 1}), (0.6 + i * 0.15, {"x": 540 + dx, "y": 300, "op": 0, "rot": r * 8} if i < 2 else {"x": 540, "y": 1000, "op": 1, "rot": 0, "escala": 1.2})))
                 for i, (n, r, dx) in enumerate([("hoja_1", -4, -300), ("hoja_30", 3, 260), ("hoja_60", -2, -80)])]],
               cam(1.0, 1.0), vineta=0.6, sfx=[(0.05, "fugaz", -22)])


@D.plano(50, "derecha, quieta")
def _(d):
    return D.P(FRIO, [brillo(540, 900, 600, "#9fc0ff", 0.25), mano("mano_der", 540, 1180, 760, anim={"flotar": [6, 2.5]})],
               cam(1.0, 1.03, (540, 1050), (540, 1040)), "desenfoque", vineta=0.7,
               hud=[D.rotulo(0.05, d - 0.02, "DERECHA", tam=64, color="#ffffff", capsula="#3a8ad0e6", x=540, y=1660)])


@D.plano(54, "nunca: cero")
def _(d):
    return D.P(FRIO, [brillo(540, 900, 600, "#9fc0ff", 0.25), mano("mano_der", 540, 1180, 760, anim={"flotar": [6, 2.5]})],
               cam(1.3, 1.35, (540, 960), (540, 960)), vineta=0.75,
               hud=[D.dato(0.05, d - 0.02, "0", "CRUJIDOS", y=1660, tam=130, borde=CIAN)])


@D.plano(55, "sesenta años después: el médico ya mayor")
def _(d):
    return D.P(CALIDO, salon(d, IMG("medico_viejo", ancho=440, x=560, y=1190, z=0.5, anim={"balanceo": [1.5, 1.6]})),
               cam(1.0, 1.05, (540, 1100), (540, 1080)), "zoom", vineta=0.6,
               hud=[D.contador(0.05, d - 0.02, 0, 60, d * 0.6, "AÑOS DESPUÉS", tam=100, y=1660)])


@D.plano(58, "compara las dos radiografías")
def _(d):
    rx = [IMG("rx_izq", ancho=400, x=330, y=990, z=0.4, keys=K(d, (0, {"op": 0}), (0.2, {"op": 1}))),
          IMG("rx_der", ancho=400, x=750, y=990, z=0.4, keys=K(d, (0, {"op": 0}), (0.4, {"op": 0}), (0.6, {"op": 1})))]
    return D.P(["#0d141c", "#0d141c"], [BG("bg_negatoscopio"), *rx, IMG("medico_viejo", ancho=420, x=900, y=1520, z=0.6)],
               cam(1.0, 1.04, (540, 1080), (540, 1060)), vineta=0.55, sfx=[(0.2, "zap", -22), (0.6 * d, "zap", -22)])


@D.plano(62, "ni rastro de artritis: dos marcas verdes")
def _(d):
    return D.P(["#0d141c", "#0d141c"], [BG("bg_negatoscopio"), IMG("rx_izq", ancho=400, x=330, y=990, z=0.4), IMG("rx_der", ancho=400, x=750, y=990, z=0.4),
               *[IMG("check", ancho=150, x=x, y=1420, z=0.6, keys=K(d, (0, {"escala": 0}), (f, {"escala": 0}), (f + 0.12, {"escala": 1, "ease": "rebote"})))
                 for x, f in ((330, 0.15), (750, 0.4))]],
               cam(1.1, 1.15, (540, 1100), (540, 1100)), vineta=0.55,
               hud=[D.amarillo(0.15, d - 0.02, "SIN ARTRITIS", y=1700)], sfx=[(0.15 * d, "ding", -16), (0.4 * d, "ding", -16)])


@D.plano(68, "ninguna diferencia: las radiografías se superponen")
def _(d):
    return D.P(RX, [brillo(540, 960, 600, "#4fd2ff", 0.25),
               IMG("rx_izq", ancho=560, y=1050, z=0.5, op=0.85, keys=K(d, (0, {"x": 300}), (0.6, {"x": 540, "ease": "suave"}))),
               IMG("rx_der", ancho=560, y=1050, z=0.5, op=0.6, keys=K(d, (0, {"x": 780}), (0.6, {"x": 540, "ease": "suave"})))],
               cam(1.0, 1.04, (540, 1050), (540, 1050)), vineta=0.6,
               hud=[D.dato(0.65 * d, d - 0.02, "=", "", y=1660, tam=150, borde=CIAN)])


@D.plano(73, "una sola persona")
def _(d):
    return D.P(["#1a1420", "#0a0810"], [brillo(540, 900, 500, "#ffe9b0", 0.3), IMG("persona_sola", ancho=420, x=540, y=1100, z=0.5, anim={"flotar": [6, 2]})],
               cam(1.0, 1.05, (540, 1050), (540, 1030)), "desenfoque", vineta=0.7,
               hud=[D.dato(0.1, d - 0.02, "1", "PERSONA", y=1640, tam=130)])


@D.plano(78, "2009: escenario, el foco se enciende")
def _(d):
    return D.P(["#120408", "#120408"], [BG("bg_escenario"), brillo(540, 700, 500, "#fff6d8", 0.5, 0.2, keys=K(d, (0, {"op": 0}), (0.3, {"op": 1})))],
               cam(1.0, 1.05, (540, 1000), (540, 1050)), "zoom", vineta=0.65,
               hud=[D.contexto(0.05, d - 0.02, "2009")], sfx=[(0.1, "golpe", -20)])


@D.plano(83, "premio Ig Nobel: trofeo y confeti")
def _(d):
    conf = {"tipo": "particulas", "clase": "chispas", "color": "#ffd23f", "area": [0, 300, 1080, 1400], "n": 70, "tam": [4, 9], "vel": [0, 140], "z": 0.8, "semilla": 9}
    return D.P(["#120408", "#120408"], [BG("bg_escenario"), IMG("trofeo", ancho=440, x=540, y=1180, z=0.5, keys=K(d, (0, {"escala": 0.5, "op": 0}), (0.2, {"escala": 1, "op": 1, "ease": "rebote"}))),
               brillo(540, 1000, 300, "#fff2a8", 0.5, 0.5, pulso=[0.15, 1.2]), conf], cam(1.0, 1.06, (540, 1100), (540, 1060)), vineta=0.6,
               hud=[D.contexto(0.1, d - 0.02, "PREMIO IG NOBEL")], sfx=[(0.15, "brillo", -16)])


@D.plano(89, "de medicina: primer plano del trofeo")
def _(d):
    return D.P(["#120408", "#120408"], [BG("bg_escenario"), IMG("trofeo", ancho=440, x=540, y=1180, z=0.5, anim={"balanceo": [2, 1]}),
               brillo(540, 1000, 300, "#fff2a8", 0.5, 0.5, pulso=[0.15, 1.2])], cam(1.6, 1.7, (540, 1000), (540, 980)), vineta=0.65,
               hud=[D.amarillo(0.05, d - 0.02, "MEDICINA", y=1680)])


@D.plano(91, "¿y qué es ese ruido? ondas de sonido")
def _(d):
    return D.P(CALIDO, [brillo(540, 900, 700, "#ffb860", 0.35), mano("mano_izq", 540, 1220, 760, anim={"balanceo": [2, 0.4]}),
               IMG("ondas", ancho=240, x=880, y=760, z=0.6, anim={"pulso": [0.15, 0.3]}), *crujir(540, 1220, 760, [0.2, 0.7, 1.2])],
               cam(1.25, 1.35, (520, 900), (520, 880)), "desenfoque", vineta=0.65,
               hud=[D.amarillo(0.1, d - 0.02, "¿EL RUIDO?", y=1700)])


@D.plano(96, "2015, Canadá: la resonancia")
def _(d):
    return D.P(["#cfe2ee", "#8fb0c4"], [BG("bg_resonancia"), brillo(540, 930, 280, "#4fd2ff", 0.3, 0.5, pulso=[0.2, 0.8])],
               cam(1.0, 1.05, (540, 1000), (540, 980)), "zoom", vineta=0.4,
               hud=[D.contexto(0.05, d - 0.02, "2015 · CANADÁ")], sfx=[(0.1, "senal", -22)])


@D.plano(104, "grabaron dedos: la mano entra en el túnel")
def _(d):
    esc = {"tipo": "forma", "forma": "rect", "ancho": 520, "alto": 10, "relleno": CIAN, "z": 0.55, "x": 540,
           "keys": K(d, (0, {"y": 700}), (0.5, {"y": 1160}), (1, {"y": 700}))}
    return D.P(["#cfe2ee", "#8fb0c4"], [BG("bg_resonancia"), mano("mano_izq", 540, 1010, 300, z=0.5, rot=90, keys=K(d, (0, {"x": 160}), (0.5, {"x": 540, "ease": "salida"}))), esc],
               cam(1.3, 1.4, (540, 960), (540, 960)), vineta=0.45, sfx=[(0.1, "senal", -24)])


@D.plano(109, "resonancia magnética: la pantalla")
def _(d):
    lin = {"tipo": "forma", "forma": "rect", "ancho": 880, "alto": 6, "relleno": CIAN, "z": 0.5, "x": 540, "keys": K(d, (0, {"y": 700}), (0.5, {"y": 1260}), (1, {"y": 700}))}
    return D.P(["#1a1f26", "#0a0d12"], [IMG("pantalla_rm", ancho=1000, x=540, y=1000, z=0.4), lin], cam(1.0, 1.1, (540, 1000), (540, 980)), vineta=0.6,
               hud=[D.amarillo(0.05, d - 0.02, "RESONANCIA", y=1580)])


# --- la articulación por dentro: los huesos se separan
def huesos(d, y_inf):
    return [BG("bg_articulacion"), IMG("hueso_sup", ancho=520, x=540, y=580, z=0.5), IMG("hueso_inf", ancho=520, x=540, z=0.5, keys=K(d, *y_inf))]


@D.plano(111, "al estirar: el dedo tira")
def _(d):
    return D.P(ART, [*huesos(d, [(0, {"y": 1230})]), D.flecha([[880, 900], [880, 1260]], 0.1, d * 0.7, AMBAR, 14)],
               cam(1.0, 1.04, (540, 960), (540, 980)), "zoom", vineta=0.6, hud=[D.rotulo(0.05, d - 0.02, "TIRAR", tam=64, color="#111111", capsula=AMBAR, x=540, y=1700)])


@D.plano(113, "las dos superficies: etiquetas")
def _(d):
    return D.P(ART, [*huesos(d, [(0, {"y": 1230})]), D.flecha([[160, 760], [330, 900]], 0.05, 0.4, CIAN, 7), D.flecha([[160, 1300], [330, 1090]], 0.2, 0.55, CIAN, 7),
                     brillo(540, 940, 120, CIAN, 0.6, 0.55, pulso=[0.3, 0.4]), brillo(540, 1090, 120, CIAN, 0.6, 0.55, pulso=[0.3, 0.4])],
               cam(1.15, 1.2, (540, 1000), (540, 1000)), vineta=0.6, hud=[D.rotulo(0.05, d - 0.02, "CARTÍLAGO", tam=52, color="#111111", capsula=CIAN, x=300, y=700)])


@D.plano(119, "se separan")
def _(d):
    return D.P(ART, [*huesos(d, [(0, {"y": 1230}), (0.8, {"y": 1370, "ease": "suave"})]), D.flecha([[880, 1000], [880, 1360]], 0.05, d * 0.7, AMBAR, 14)],
               cam(1.0, 1.04, (540, 990), (540, 1000)), vineta=0.6, hud=[D.amarillo(0.05, d - 0.02, "SE SEPARAN", y=1720)], sfx=[(0.1, "whoosh", -26, {"dur": 0.4})])


@D.plano(121, "el líquido: gotitas brillan")
def _(d):
    gotas = {"tipo": "particulas", "clase": "burbujas", "color": "#bff0ff", "area": [360, 900, 720, 1160], "n": 30, "tam": [3, 7], "vel": [0, -20], "z": 0.55, "semilla": 3}
    return D.P(ART, [*huesos(d, [(0, {"y": 1370})]), gotas], cam(1.4, 1.5, (540, 1010), (540, 1010)), vineta=0.65,
               hud=[D.rotulo(0.05, d - 0.02, "LÍQUIDO", tam=56, color="#111111", capsula=CIAN, x=540, y=1600)])


@D.plano(127, "pierde presión: el medidor baja")
def _(d):
    barra = {"tipo": "barra", "x": 900, "y": 1000, "ancho": 50, "alto": 360, "vertical": True, "color": CIAN, "fondo": "#ffffff20", "z": 0.6,
             "keys": K(d, (0, {"progreso": 1}), (0.8, {"progreso": 0.12}))}
    sombra = {"tipo": "forma", "forma": "elipse", "ancho": 380, "alto": 170, "relleno": "#0a1a3a", "x": 540, "y": 1010, "z": 0.45, "desenfoque": 20,
              "keys": K(d, (0, {"op": 0}), (0.8, {"op": 0.55}))}
    return D.P(ART, [*huesos(d, [(0, {"y": 1370})]), sombra, barra], cam(1.15, 1.2, (580, 1000), (580, 1000)), vineta=0.65,
               hud=[D.rotulo(0.05, d - 0.02, "PRESIÓN", tam=64, color="#ffffff", capsula="#0a2a4ae6", x=540, y=1700)])


@D.plano(129, "micro: de golpe")
def _(d):
    return D.P(ART, [*huesos(d, [(0, {"y": 1370})]), brillo(540, 1010, 300, "#ffffff", 1.0, 0.6, keys=K(d, (0, {"op": 0}), (0.5, {"op": 1})))],
               cam(1.5, 1.6, (540, 1010), (540, 1010), temblor=6), vineta=0.7)


@D.plano(132, "se forma una burbuja de gas")
def _(d):
    bur = IMG("burbuja", ancho=190, x=540, y=1010, z=0.55, anim={"pulso": [0.04, 0.5]}, keys=K(d, (0, {"escala": 0, "op": 0}), (0.08, {"escala": 1.2, "op": 1, "ease": "rebote"}), (0.3, {"escala": 1.0})))
    return D.P(ART, [*huesos(d, [(0, {"y": 1370})]), bur, brillo(540, 1010, 260, "#ffffff", 1.0, 0.6, keys=K(d, (0, {"op": 1}), (0.25, {"op": 0})))],
               cam(1.0, 1.06, (540, 1000), (540, 1000)), vineta=0.6,
               hud=[D.amarillo(0.1, d - 0.02, "BURBUJA DE GAS", y=1720)], sfx=[(0.02, "pop", -10)])


@D.plano(138, "el crujido: CRAC gigante")
def _(d):
    return D.P(ART, [*huesos(d, [(0, {"y": 1370})]), IMG("burbuja", ancho=190, x=540, y=1010, z=0.55, anim={"pulso": [0.06, 0.4]}),
               IMG("ondas", ancho=200, x=820, y=1010, z=0.6, anim={"pulso": [0.2, 0.3]})],
               cam(1.6, 1.75, (540, 1010), (540, 1010)), vineta=0.65,
               hud=[D.rotulo(0.05, d - 0.02, "CRAC", tam=150, color="#ffd23f", capsula=None, rot=-6, x=540, y=1560)], sfx=[(0.05, "tic", -12)])


@D.plano(141, "esa burbuja naciendo")
def _(d):
    return D.P(ART, [*huesos(d, [(0, {"y": 1370})]), IMG("burbuja", ancho=190, x=540, y=1010, z=0.55, keys=K(d, (0, {"escala": 0.3}), (0.6, {"escala": 1.1, "ease": "rebote"}))),
               brillo(540, 1010, 200, "#dff6ff", 0.5, 0.5, pulso=[0.2, 0.5])], cam(1.2, 1.3, (540, 1010), (540, 1010)), vineta=0.6)


@D.plano(144, "bucle: ¿con qué mano?")
def _(d):
    return D.P(CALIDO, [brillo(540, 900, 700, "#ffb860", 0.35), mano("mano_izq", 290, 1150, 460, anim={"balanceo": [2, 0.5]}),
               mano("mano_der", 790, 1150, 460, anim={"balanceo": [2, 0.5]})], cam(1.06, 1.0, (540, 1080), (540, 1100)), "zoom", vineta=0.6,
               hud=[D.rotulo(0.3, d - 0.02, "?", tam=220, color="#ffd23f", capsula=None, x=540, y=760)])


D.construir("01", "crujir-nudillos", ["sesenta", "Unger", "artritis", "experimento", "izquierda", "derecha", "nunca", "Ig", "Nobel", "resonancia",
                                      "burbuja", "gas", "crujido"], {"generar": "curiosidad", "semilla": 11, "db": -13})
