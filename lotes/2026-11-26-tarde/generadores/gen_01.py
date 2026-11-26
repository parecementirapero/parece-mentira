"""01 · ¿Le das a posponer? — método denso, estilo del vídeo largo. Lote 2026-11-26-tarde (Agente 20:00 (Jorge)).
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comun_1126t as C  # noqa: E402
from comun_1126t import *  # noqa: E402,F401,F403
import ilus_1126t  # noqa: E402

SVG = ilus_1126t.generar(os.path.join(sys.argv[1], "_svg_lote"))
C.SVG_DIR = SVG
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
DOR = ["#1a2240", "#0c1020"]
CER = ["#0b0f24", "#1b1340"]
CIU = ["#141a3e", "#0c0c14"]
S_D = SUELO["bg_dormitorio"]


def dormitorio(extra, d, cama_n="cama_duerme", zoom=(1.0, 1.06), foco=(540, 1250)):
    return [BG("bg_dormitorio"), PZ(cama_n, 520, S_D, 520, z=0.45, pie=20), PZ("mesilla", 960, S_D - 10, 230, z=0.42)] + extra


@v.plano(0, "gancho: el despertador enorme salta sonando y la mano lo golpea")
def _(d):
    return P(DOR, [BG("bg_dormitorio")] + suena(540, 1000, 820, d, min(d - 0.05, 0.9), temblor=14) +
             [OB("boton_posponer", 540, 640, 520, z=0.6, keys=[{"t": 0, "y": 560}, {"t": 0.85, "y": 560}, {"t": 0.95, "y": 600, "ease": "golpe"}, {"t": d, "y": 600}])],
             cam(1.0, 1.08, (540, 900)), vineta=0.4, sfx=[(0.0, "ding", -16), (0.3, "ding", -18), (0.9, "pop", -14)])


@v.plano(4, "otra vez: vuelve a sonar sobre la mesilla, en la habitación oscura")
def _(d):
    return P(DOR, dormitorio([OB("zzz", 300, 980, 220, z=0.6, keys=flota(d, 12, 980))] + suena(960, 1330, 180, d, z=0.6, temblor=6), d),
             cam(1.0, 1.08, (600, 1250)), "corte", sfx=[(0.05, "ding", -18)])


@v.plano(6, "tranquilo, no eres el único: el dormilón sonríe")
def _(d):
    return P(DOR, [BG("bg_dormitorio"), OB("cara_dormilon_sueno", 540, 1120, 900, keys=[{"t": 0, "escala": 1.04}, {"t": d, "escala": 1.0, "ease": "salida"}])],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[cap(0.2, d - 0.05, "NO ERES EL ÚNICO", tam=84)], sfx=[(0.1, "pop", -22)])


@v.plano(11, "en dos mil veinticinco: el año corre")
def _(d):
    return P(CER, [BG("bg_cerebro"), OB("telefono_movil", 540, 1100, 460, keys=aparece(0.0) + flota(d, 12, 1100))],
             cam(1.0, 1.06, (540, 1050)), "corte",
             hud=[contador(0.05, min(1.0, d - 0.05), 2000, 2025, 0.6, miles=False, tam=150, color="#141414", capsula="#ffffffe6", y=620)], sfx=[(0.1, "tic", -18)])


@v.plano(15, "un estudio miró tres millones de noches: lunas que pasan")
def _(d):
    els = [estrellas(90, 4), OB("tierra_noche", 540, 1150, 760, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 10}])]
    els += [OB("luna_creciente", 140 + 200 * i, 640, 120, z=0.6, keys=aparece(0.15 + 0.12 * i)) for i in range(5)]
    return P(["#02030a", "#0a1030"], els, cam(1.0, 1.05, (540, 1000)), "corte",
             hud=[cap(0.5, d - 0.05, "3.000.000 DE NOCHES", "#141414", "#7df9ffe6", 84)], sfx=[(0.15 + 0.12 * i, "pop", -26) for i in range(5)])


@v.plano(23, "gente de todo el mundo: la Tierra gira")
def _(d):
    return P(["#02030a", "#0a1030"], [estrellas(80, 5), OB("foto_mundo", 540, 1050, 820, keys=[{"t": 0, "rot": -6}, {"t": d, "rot": 10}] + aparece(0.0))],
             cam(1.0, 1.06, (540, 1000)), "desenfoque", sfx=[(0.05, "brillo", -20)])


@v.plano(28, "con una aplicación de sueño: el móvil con la alarma en la mesilla")
def _(d):
    return P(DOR, dormitorio([OB("telefono_movil", 930, 1310, 80, z=0.6, keys=late(0.2, 2, 0.12))], d), cam(1.15, 1.25, (760, 1300)), "corte",
             hud=[cap(0.3, d - 0.05, "APP DE SUEÑO", "#ffffff", "#2a5ae8e6", 90)], sfx=[(0.2, "senal", -22)])


@v.plano(33, "más de la mitad de las mañanas: diez personas, se encienden seis")
def _(d):
    ps = ("voluntario_1", "voluntario_2", "voluntario_3", "voluntario_4", "voluntario_5", "voluntario_6")
    return P(CIU, [BG("bg_ciudad")] + gente(10, 6, 0.15, 1150, 170, "#ffd23f", ps), cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[cap(0.25, d - 0.05, "MÁS DE LA MITAD", "#141414", "#ffd23fe6", 100)], sfx=[(0.15 + 0.07 * i, "tic", -24) for i in range(6)])


@v.plano(42, "alguien dándole a posponer: el botón baja de golpe")
def _(d):
    return P(DOR, [BG("bg_dormitorio"), OB("boton_posponer", 540, 1050, 900, keys=[{"t": 0, "y": 1000}, {"t": 0.25, "y": 1060, "ease": "golpe"}, {"t": d, "y": 1060}])],
             cam(1.05, 1.12, (540, 1050)), "corte", hud=[amarillo(0.25, d - 0.05, "POSPONER", y=640, tam=120, color=AMBAR)], sfx=[(0.25, "impacto", -16)])


@v.plano(46, "de media, once minutos más: el reloj de arena")
def _(d):
    return P(DOR, [BG("bg_dormitorio"), OB("reloj_arena_a", 540, 1100, 460, keys=[{"t": 0, "rot": 180}, {"t": 0.4, "rot": 360, "ease": "salida"}])],
             cam(1.0, 1.06, (540, 1050)), "corte",
             hud=[contador(0.1, d - 0.05, 0, 11, 0.6, " MIN", tam=140, color="#141414", capsula="#7df9ffe6", y=640)], sfx=[(0.1, "whoosh", -22)])


@v.plano(53, "¿y es tan malo?: el despertador con un interrogante")
def _(d):
    return P(DOR, [BG("bg_dormitorio"), OB("despertador_a", 540, 1080, 560, keys=[{"t": 0, "rot": -6}, {"t": d, "rot": 6, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[amarillo(0.05, d - 0.05, "¿ES MALO?", y=600, tam=130, color=CIAN)], sfx=[(0.05, "impacto", -20)])


@v.plano(57, "al despertar: se incorpora en la cama y estira el brazo")
def _(d):
    return P(DOR, dormitorio([], d, "cama_despierta"), cam(1.1, 1.2, (500, 1350), (540, 1300)), "corte", sfx=[(0.1, "roce", -20)])


@v.plano(61, "tu cerebro va lento: el cerebro con poca luz que se enciende despacio")
def _(d):
    return P(CER, [BG("bg_cerebro"), OB("cerebro", 540, 1000, 700, keys=[{"t": 0, "op": 0.5}, {"t": d, "op": 1.0, "ease": "suave"}] + flota(d, 8, 1000, 3.0)),
                   brillo(540, 1000, 420, "#2ff3ff", 0.25, 0.06, keys=[{"t": 0, "op": 0}, {"t": d, "op": 0.6}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.2, d - 0.05, "LENTO", "#ffffff", "#c0392be6", 120)], sfx=[(0.1, "senal", -24)])


@v.plano(63, "se llama inercia del sueño: la cara somnolienta")
def _(d):
    return P(DOR, [BG("bg_dormitorio"), OB("cara_dormilon_sueno", 540, 1150, 960, keys=[{"t": 0, "rot": -2}, {"t": d, "rot": 3, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[amarillo(0.05, d - 0.05, "INERCIA DEL SUEÑO", y=620, tam=86, color=CIAN)], sfx=[(0.15, "brillo", -18)])


@v.plano(68, "de quince minutos a más de una hora: barra que se llena")
def _(d):
    return P(CER, [BG("bg_cerebro"), OB("reloj_interno", 540, 1100, 560, keys=aparece(0.0) + [{"t": 0, "rot": 0}, {"t": d, "rot": 40}])],
             cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[contador(0.1, d - 0.05, 15, 60, max(0.4, d * 0.6), " MIN", tam=140, color="#141414", capsula="#ffd23fe6", y=640)], sfx=[(0.1, "tic", -20)])


@v.plano(79, "esos minutos entre alarmas: suena, se duerme, suena")
def _(d):
    return P(DOR, dormitorio([OB("zzz", 300, 980, 200, z=0.6, keys=[{"t": 0, "op": 0}, {"t": d * 0.4, "op": 0}, {"t": d * 0.5, "op": 1}] + flota(d, 10, 980))] +
                             suena(960, 1330, 180, d, d * 0.35, z=0.6, temblor=6), d), cam(1.0, 1.06, (600, 1250)), "corte", sfx=[(0.05, "ding", -20)])


@v.plano(83, "son sueño ligero y a trozos: la barra de sueño se parte")
def _(d):
    els = [BG("bg_dormitorio")]
    for i in range(5):
        x = 180 + i * 180
        els.append({"tipo": "forma", "forma": "rect", "ancho": 150, "alto": 90, "relleno": "#7df9ff", "x": x, "y": 1100, "z": 0.6,
                    "keys": [{"t": 0, "y": 1100, "op": 0}, {"t": 0.1 + 0.08 * i, "op": 0.9}, {"t": 0.6 + 0.08 * i, "y": 1100 + (40 if i % 2 else -40), "rot": (8 if i % 2 else -8), "ease": "golpe"}]})
    return P(DOR, els, cam(1.0, 1.05, (540, 1100)), "corte", hud=[cap(0.05, d - 0.05, "SUEÑO LIGERO", "#141414", "#7df9ffe6", 100)],
             sfx=[(0.6 + 0.08 * i, "pop", -24) for i in range(5)])


@v.plano(89, "no un descanso de verdad: la cara cansada")
def _(d):
    return P(DOR, [BG("bg_dormitorio"), PZ("dormilon_sueno", 540, S_D, 900, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.03}])],
             cam(1.0, 1.08, (540, 1100)), "corte", hud=[cap(0.2, d - 0.05, "NO DESCANSA", "#ffffff", "#c0392be6", 100)], sfx=[(0.1, "pop", -22)])


@v.plano(94, "pero en Suecia: ventana con nieve")
def _(d):
    return P(["#3a2418", "#120a06"], [BG("bg_ventana_invierno"), OB("copo_nieve", 300, 800, 90, z=0.6, keys=flota(d, 20, 800)), OB("copo_nieve", 800, 700, 70, z=0.6, keys=flota(d, 16, 700))],
             cam(1.0, 1.06, (540, 1000)), "desenfoque", hud=[cap(0.2, d - 0.05, "SUECIA", "#ffffff", "#2a5ae8e6", 120)], sfx=[(0.1, "brillo", -20)])


@v.plano(97, "en dos mil veintitrés: cifra que corre")
def _(d):
    return P(["#3a2418", "#120a06"], [BG("bg_ventana_invierno")], cam(1.08, 1.12, (540, 1000)), "corte",
             hud=[contador(0.05, d - 0.05, 2000, 2023, 0.5, miles=False, tam=150, color="#141414", capsula="#ffffffe6", y=1000)], sfx=[(0.05, "tic", -18)])


@v.plano(101, "lo probaron con gente que pospone siempre: un grupo en el laboratorio")
def _(d):
    S = SUELO["bg_oficina_gris"]
    return P(["#d8dce2", "#8a9098"], [BG("bg_oficina_gris"), PZ("dormilon_sueno", 300, S, 760, keys=aparece(0.1)), PZ("voluntario_3", 540, S - 20, 720, z=0.48, keys=aparece(0.25)),
                                     PZ("voluntario_6", 780, S, 760, keys=aparece(0.4))],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[BANDA(), cap(0.5, d - 0.05, "POSPONEN SIEMPRE", tam=80)], sfx=[(0.1 + 0.15 * i, "pop", -24) for i in range(3)])


@v.plano(108, "media hora de alarmas: tres alarmas seguidas")
def _(d):
    els = [BG("bg_dormitorio")]
    for i in range(3):
        els.append(OB("despertador_a", 220 + i * 320, 1100, 260, z=0.6, keys=aparece(0.1 + 0.2 * i) + late(0.15 + 0.2 * i, 1, 0.12)))
    return P(DOR, els, cam(1.0, 1.04, (540, 1100)), "corte", hud=[cap(0.5, d - 0.05, "30 MIN", "#141414", "#ffd23fe6", 130)],
             sfx=[(0.1 + 0.2 * i, "ding", -22) for i in range(3)])


@v.plano(112, "no les hizo peores: cerebro tranquilo y marca verde")
def _(d):
    return P(CER, [BG("bg_cerebro"), OB("cerebro_brillo", 540, 1000, 700, keys=late(0.2, 2, 0.05, 0.4)),
                   flecha([[400, 1420], [500, 1520], [720, 1280]], 0.2, 0.6, "#5dff8a", 26, punta=False, z=0.8)],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[cap(0.3, d - 0.05, "SIN DAÑO", "#141414", "#5dff8ae6", 110)], sfx=[(0.3, "ding", -18)])


@v.plano(116, "y al levantarse pensaban un poco mejor: se levanta sonriendo")
def _(d):
    return P(DOR, [BG("bg_dormitorio"), PZ("dormilon_pie", 540, S_D, 880, keys=aparece(0.05))], cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[cap(0.4, d - 0.05, "UN POCO MEJOR", "#141414", "#7df9ffe6", 90)], sfx=[(0.05, "whoosh", -20)])


@v.plano(124, "lo que sí dicen los expertos: el médico")
def _(d):
    S = SUELO["bg_oficina_gris"]
    return P(["#d8dce2", "#8a9098"], [BG("bg_oficina_gris"), PZ("medica_2", 540, S, 1050, keys=[{"t": 0, "escala": 0.98}, {"t": d, "escala": 1.02}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[BANDA()], sfx=[(0.1, "pop", -22)])


@v.plano(130, "si lo necesitas cada mañana: calendario de mañanas con alarmas")
def _(d):
    return P(DOR, [BG("bg_dormitorio"), OB("calendario_hoja", 540, 1080, 620, keys=aparece(0.0))] +
             [OB("despertador_a", 330 + (i % 3) * 190, 980 + (i // 3) * 200, 110, z=0.6, keys=aparece(0.15 + 0.06 * i)) for i in range(6)],
             cam(1.0, 1.05, (540, 1080)), "corte", sfx=[(0.15 + 0.06 * i, "tic", -26) for i in range(6)])


@v.plano(135, "seguramente duermes poco: la cara cansada con poca batería")
def _(d):
    return P(DOR, [BG("bg_dormitorio"), OB("cara_dormilon_sueno", 540, 1150, 900)], cam(1.05, 1.1, (540, 1100)), "corte",
             hud=[cap(0.2, d - 0.05, "DUERMES POCO", "#ffffff", "#c0392be6", 100)], sfx=[(0.15, "impacto", -20)])


@v.plano(138, "el truco: pon la alarma a la hora real; las agujas se mueven")
def _(d):
    return P(DOR, [BG("bg_dormitorio"), OB("despertador_a", 540, 1080, 640, keys=late(0.3, 2, 0.06))], cam(1.0, 1.06, (540, 1050)), "corte",
             hud=[amarillo(0.05, min(1.2, d * 0.4), "EL TRUCO", y=600, tam=120, color=AMBAR), cap(min(1.3, d * 0.45), d - 0.05, "LA HORA REAL", "#141414", "#5dff8ae6", 100)],
             sfx=[(0.05, "impacto", -18), (0.3, "tic", -18)])


@v.plano(147, "y déjala lejos de la cama: el despertador vuela al otro lado")
def _(d):
    return P(DOR, dormitorio([OB("despertador_a", 900, 1290, 180, z=0.6, keys=[{"t": 0, "x": 900, "y": 1290}, {"t": d * 0.6, "x": 160, "y": 900, "ease": "suave"}, {"t": d, "x": 150, "y": 900}]),
                              flecha([[900, 1250], [500, 900], [230, 900]], 0.1, d * 0.55, CIAN, 10, disc=[18, 14], z=0.55)], d),
             cam(1.0, 1.04, (540, 1250)), "corte", hud=[cap(0.4, d - 0.05, "LEJOS DE LA CAMA", "#141414", "#7df9ffe6", 86)], sfx=[(0.1, "whoosh", -18)])


@v.plano(153, "¿cuántas veces le das tú? (bucle): el despertador vuelve a sonar")
def _(d):
    return P(DOR, [BG("bg_dormitorio")] + suena(540, 1000, 820, d, d - 0.05, temblor=14), cam(1.0, 1.08, (540, 900)), "corte", sfx=[(0.05, "ding", -18)])


def micro(fondo, els, txt=None, col="#ffffff", cap_f="#c0392be6", sfx="pop"):
    def fn(d):
        return P(fondo, els(d), cam(1.15, 1.3, (540, 1000)), "corte", hud=[cap(0.0, d - 0.02, txt, col, cap_f, 130)] if txt else [], sfx=[(0.01, sfx, -18)])
    return fn


v.plano(10, "micro: la mano en el botón en grande")(micro(DOR, lambda d: [BG("bg_dormitorio"), OB("boton_posponer", 540, 1000, 1000)], sfx="pop"))
v.plano(40, "micro: la mitad")(micro(CIU, lambda d: [BG("bg_amanecer"), brillo(540, 1000, 400, "#ffd23f", 0.5, 0.06)], "MITAD", "#141414", "#ffd23fe6", "impacto"))
v.plano(60, "micro: el cerebro se apaga un instante")(micro(CER, lambda d: [BG("bg_cerebro"), OB("cerebro", 540, 1000, 900, keys=[{"t": 0, "op": 0.9}, {"t": d, "op": 0.4}])], sfx="brillo"))
v.plano(88, "micro: zzz")(micro(DOR, lambda d: [BG("bg_dormitorio"), OB("zzz", 540, 1000, 520, keys=flota(d, 18, 1000))], sfx="pop"))
v.plano(121, "micro: la bombilla de pensar mejor")(micro(CER, lambda d: [BG("bg_cerebro"), OB("cerebro_brillo", 540, 1000, 900, keys=late(0.0, 1, 0.08))], sfx="ding"))


v.construir("2026-11-26-tarde-01-posponer-alarma", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 1261, "db": -13},
            claves=["posponer", "único", "estudio", "millones", "noches", "mitad", "once", "minutos", "malo", "cerebro", "lento", "inercia",
                    "ligero", "trozos", "Suecia", "peores", "mejor", "expertos", "poco", "truco", "real", "lejos", "cama"],
            ep_extra={"sfx_bajo_voz": True})
