"""03 · El Black Friday lo bautizó la policía — método denso, estilo del vídeo largo. Lote 2026-11-26-tarde (Agente 20:00 (Jorge)).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comun_1126t as C  # noqa: E402
from comun_1126t import *  # noqa: E402,F401,F403
import ilus_1126t  # noqa: E402

SVG = ilus_1126t.generar(os.path.join(sys.argv[1], "_svg_lote"))
C.SVG_DIR = SVG
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
CIU = ["#141a3e", "#0c0c14"]
OSC = ["#141428", "#06060e"]
S_C = SUELO["bg_ciudad"]
COCHES = ("coche_rojo", "coche_azul", "coche_crema")


def trafico(d, y=1440, ancho=520, vel=1.0, n=4, z=0.6, sentido=1):
    els = []
    for i in range(n):
        x0 = -300 + i * 420 if sentido > 0 else 1380 - i * 420
        els.append(OB(COCHES[i % 3], x0, y + (i % 2) * 30, ancho, z=z + 0.01 * (i % 2),
                      keys=[{"t": 0, "x": x0}, {"t": d, "x": x0 + sentido * 260 * vel * d, "ease": "lineal"}]))
    return els


@v.plano(0, "gancho: el policía levanta el brazo y para el tráfico en el cruce")
def _(d):
    return P(CIU, [BG("bg_ciudad")] + trafico(d, 1470, 460, 0.6) +
             [PZ("policia_para", 540, S_C + 120, 1080, z=0.7, keys=arranque(540, S_C + 120 - 540 + 25 / 940 * 1080, d, "abajo", 220, 20)),
              OB("silbato", 700, 760, 150, z=0.75, keys=late(0.2, 3, 0.12, 0.25))],
             cam(1.0, 1.06, (540, 1100)), vineta=0.4, sfx=[(0.05, "senal", -16, {"f": 2800}), (0.5, "senal", -18, {"f": 2800})])


@v.plano(4, "el Black Friday nació en un atasco: fila de coches parados")
def _(d):
    return P(CIU, [BG("bg_ciudad")] + trafico(d, 1300, 480, 0.15, 5, 0.5) + trafico(d, 1500, 560, 0.1, 4, 0.6, -1),
             cam(1.0, 1.05, (540, 1250)), "corte", hud=[amarillo(0.05, d - 0.05, "BLACK FRIDAY", y=640, tam=120, color=AMBAR)], sfx=[(0.1, "rumor", -24, {"dur": d})])


@v.plano(11, "Filadelfia, hace más de sesenta años: periódico antiguo")
def _(d):
    return P(OSC, [OB("periodico", 540, 1080, 820, keys=aparece(0.0) + [{"t": 0, "rot": -8}, {"t": d, "rot": 2}])], cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[cap(0.05, min(1.2, d * 0.5), "FILADELFIA", "#ffffff", "#2a5ae8e6", 110), cap(min(1.25, d * 0.52), d - 0.05, "+60 AÑOS", "#141414", "#ffd23fe6", 120)],
             sfx=[(0.05, "whoosh", -20)])


@v.plano(17, "el día después de Acción de Gracias: la hoja del calendario")
def _(d):
    return P(OSC, [BG("bg_ventana_invierno"), OB("calendario_hoja", 540, 1080, 560, keys=aparece(0.0) + late(0.5, 1, 0.06))], cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[cap(0.1, d - 0.05, "ACCIÓN DE GRACIAS", "#141414", "#ffd23fe6", 80)], sfx=[(0.05, "pop", -20)])


@v.plano(24, "miles de personas llenaban el centro: la calle se llena de gente")
def _(d):
    ps = ("voluntario_1", "compradora", "voluntario_2", "voluntario_3", "chica_saluda", "voluntario_4", "voluntario_5", "chico_bolsillo", "voluntario_6", "adulto_camina")
    return P(CIU, [BG("bg_ciudad")] + gente(10, 10, 0.1, 1150, 170, "#ffd23f", ps), cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[cap(0.1, d - 0.05, "MILES", "#141414", "#ffd23fe6", 120)], sfx=[(0.1 + 0.05 * i, "pop", -28) for i in range(10)])


@v.plano(30, "para comprar: la compradora con sus bolsas")
def _(d):
    return P(CIU, [BG("bg_ciudad"), PZ("compradora", 420, S_C, 950), OB("bolsas_compras", 760, 1250, 380, z=0.6, keys=aparece(0.1))],
             cam(1.0, 1.05, (540, 1100)), "corte", sfx=[(0.1, "pop", -20)])


@v.plano(32, "y el sábado llegaban todavía más: más gente que entra por los lados")
def _(d):
    ps = ("voluntario_2", "voluntario_4", "chico_bolsillo", "voluntario_6", "voluntario_1")
    xs = [150, 340, 540, 740, 930]
    return P(CIU, [BG("bg_ciudad")] + [PZ(p, x, S_C, 700, keys=[{"t": 0, "x": x + (-600 if x < 540 else 600)}, {"t": 0.3 + 0.08 * i, "x": x, "ease": "salida"}])
                                     for i, (p, x) in enumerate(zip(ps, xs))],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[cap(0.3, d - 0.05, "SÁBADO: MÁS", "#ffffff", "#c0392be6", 100)], sfx=[(0.1, "whoosh", -20)])


@v.plano(38, "para el gran partido entre el Ejército y la Marina: el balón vuela en el estadio")
def _(d):
    return P(["#0a0e1e", "#020308"], [BG("bg_estadio_noche"), OB("balon_americano", 540, 900, 360, z=0.7, keys=lanza(0.0, d * 0.8, (-200, 1300), (760, 820)) + [{"t": 0, "rot": -30}, {"t": d, "rot": 330}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[cap(0.4, d - 0.05, "EJÉRCITO VS. MARINA", "#141414", "#7df9ffe6", 76)], sfx=[(0.1, "whoosh", -18), (0.3, "rumor", -24, {"dur": d})])


@v.plano(48, "tráfico y aglomeraciones: los coches cruzan deprisa")
def _(d):
    return P(CIU, [BG("bg_ciudad")] + trafico(d, 1380, 520, 1.2, 6, 0.6), cam(1.05, 1.1, (540, 1300)), "corte",
             hud=[cap(0.0, d - 0.02, "TRÁFICO", "#ffffff", "#c0392be6", 120)], sfx=[(0.05, "whoosh", -18)])


@v.plano(51, "y robos en las tiendas: una bolsa desaparece")
def _(d):
    return P(CIU, [BG("bg_ciudad"), OB("bolsas_compras", 540, 1150, 520, keys=[{"t": 0, "x": 540}, {"t": d * 0.45, "x": 540}, {"t": d * 0.75, "x": 1300, "ease": "entrada"}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[cap(0.1, d - 0.05, "ROBOS", "#ffffff", "#c0392be6", 130)], sfx=[(d * 0.5, "whoosh", -18)])


@v.plano(55, "ningún policía podía librar: el policía y el calendario tachado")
def _(d):
    return P(CIU, [BG("bg_ciudad"), PZ("policia_pie", 330, S_C, 900), OB("calendario_hoja", 780, 1050, 360, z=0.6)] + tacha(780, 1050, 0.35, 140),
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[cap(0.2, d - 0.05, "SIN LIBRAR", "#ffffff", "#c0392be6", 110)], sfx=[(0.35, "zap", -18)])


@v.plano(60, "y todos hacían turnos larguísimos: la cara cansada del policía")
def _(d):
    return P(CIU, [BG("bg_ciudad"), OB("cara_policia", 540, 1150, 940, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.05}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[cap(0.02, d - 0.05, "TURNOS ETERNOS", "#141414", "#ffd23fe6", 90)], sfx=[(0.1, "pop", -22)])


@v.plano(64, "¿cómo lo llamaban?: el policía mira")
def _(d):
    return P(CIU, [BG("bg_ciudad"), OB("cara_policia", 540, 1150, 1040)], cam(1.05, 1.1, (540, 1100)), "corte",
             hud=[amarillo(0.02, d - 0.03, "¿CÓMO?", y=600, tam=130, color=CIAN)], sfx=[(0.05, "impacto", -20)])


@v.plano(67, "viernes negro: la ciudad se oscurece de golpe")
def _(d):
    return P(["#000000", "#000000"], [BG("bg_ciudad"), {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2100, "relleno": "#000000", "x": 540, "y": 960, "z": 0.5,
                                                         "keys": [{"t": 0, "op": 0}, {"t": 0.2, "op": 0.75, "ease": "golpe"}]}],
             cam(1.0, 1.08, (540, 1000)), "corte", hud=[cap(0.02, d - 0.03, "VIERNES NEGRO", "#ffffff", "#000000f0", 130)], sfx=[(0.1, "impacto", -14)])


@v.plano(69, "a las tiendas no les gustó nada: las bolsas caen")
def _(d):
    return P(CIU, [BG("bg_ciudad"), OB("bolsas_compras", 540, 1200, 560, keys=cae(0.0, 0.6, 700, 1200))], cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[cap(0.4, d - 0.05, "A LAS TIENDAS, NO", "#ffffff", "#c0392be6", 90)], sfx=[(0.45, "golpe", -16)])


@v.plano(77, "en mil novecientos sesenta y uno: el periódico")
def _(d):
    return P(OSC, [OB("periodico", 540, 1100, 760, keys=[{"t": 0, "rot": 6}, {"t": d, "rot": -2}])], cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[contador(0.05, min(1.2, d - 0.05), 1900, 1961, 0.7, miles=False, tam=150, color="#141414", capsula="#ffffffe6", y=620)], sfx=[(0.05, "tic", -18)])


@v.plano(83, "intentaron cambiarlo por gran viernes: el rótulo nuevo")
def _(d):
    return P(CIU, [BG("bg_ciudad"), brillo(540, 1000, 420, "#5dff8a", 0.35, 0.06)], cam(1.0, 1.05, (540, 1000)), "corte",
             hud=[cap(0.05, d - 0.05, "«GRAN VIERNES»", "#141414", "#5dff8ae6", 110, y=1000)], sfx=[(0.05, "ding", -18)])


@v.plano(88, "no funcionó: el rótulo se tacha")
def _(d):
    return P(CIU, [BG("bg_ciudad")] + tacha(540, 1000, 0.1, 260), cam(1.05, 1.1, (540, 1000)), "corte",
             hud=[cap(0.0, d - 0.02, "«GRAN VIERNES»", "#141414", "#5dff8ae6", 110, y=1000)], sfx=[(0.1, "zap", -16)])


@v.plano(90, "¿y lo de los números rojos?: la pizarra en rojo")
def _(d):
    return P(OSC, [OB("grafico_cae", 540, 1100, 820, keys=aparece(0.0))], cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[cap(0.05, d - 0.05, "¿NÚMEROS ROJOS?", "#ffffff", "#c0392be6", 100)], sfx=[(0.05, "impacto", -20)])


@v.plano(96, "que las tiendas pasaban de rojos a negros: rojo que se vuelve negro")
def _(d):
    m = max(0.6, d * 0.45)
    return P(OSC, [OB("bolsas_compras", 540, 1150, 560, keys=late(m, 1, 0.08))], cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[cap(0.05, m, "ROJO", "#ffffff", "#c0392be6", 130), cap(m + 0.05, d - 0.05, "NEGRO", "#ffffff", "#000000f0", 130)], sfx=[(m, "ding", -18)])


@v.plano(106, "se inventó después, en los años ochenta")
def _(d):
    return P(OSC, [OB("periodico", 540, 1100, 700, keys=aparece(0.0))], cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[cap(0.05, min(1.0, d * 0.4), "INVENTADO", "#141414", "#ffd23fe6", 110),
                  contador(min(1.05, d * 0.42), d - 0.05, 1900, 1980, 0.5, miles=False, tam=140, color="#141414", capsula="#ffffffe6", y=620)], sfx=[(0.05, "whoosh", -20)])


@v.plano(113, "y el primer viernes negro de la historia fue otro: monedas de oro")
def _(d):
    return P(["#1a1408", "#050302"], [OB("monedas_oro", 540, 1100, 640, keys=aparece(0.0)), brillo(540, 1050, 400, "#ffd86a", 0.4, 0.05)],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[cap(0.2, d - 0.05, "EL PRIMERO", "#141414", "#ffd23fe6", 110)], sfx=[(0.05, "brillo", -18)])


@v.plano(123, "en mil ochocientos sesenta y nueve")
def _(d):
    return P(["#1a1408", "#050302"], [OB("grafico_cae", 540, 1100, 760, keys=[{"t": 0, "escala": 0.96}, {"t": d, "escala": 1.0}])], cam(1.0, 1.04, (540, 1050)), "corte",
             hud=[contador(0.05, d - 0.05, 1800, 1869, 0.7, miles=False, tam=150, color="#141414", capsula="#ffffffe6", y=620)], sfx=[(0.05, "tic", -18)])


@v.plano(129, "cuando el precio del oro se hundió en Nueva York: la línea cae")
def _(d):
    return P(["#1a1408", "#050302"], [OB("grafico_cae", 540, 1100, 900), flecha([[700, 800], [760, 1150], [840, 1250]], 0.1, 0.7, "#ff4a3a", 16, z=0.7)],
             cam(1.05, 1.12, (600, 1100)), "corte", hud=[cap(0.3, d - 0.05, "EL ORO SE HUNDE", "#ffffff", "#c0392be6", 96)], sfx=[(0.2, "whoosh", -16)])


@v.plano(139, "hoy se celebra en medio mundo: la Tierra rodeada de bolsas")
def _(d):
    els = [estrellas(80, 9), OB("foto_mundo", 540, 1050, 640, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 25}])]
    for i, (x, y) in enumerate(((220, 760), (860, 780), (180, 1340), (880, 1330))):
        els.append(OB("bolsas_compras", x, y, 190, z=0.6, keys=aparece(0.15 + 0.12 * i)))
    return P(["#02030a", "#0a1030"], els, cam(1.0, 1.04, (540, 1050)), "corte", hud=[cap(0.4, d - 0.05, "MEDIO MUNDO", "#141414", "#7df9ffe6", 110)],
             sfx=[(0.15 + 0.12 * i, "pop", -24) for i in range(4)])


@v.plano(145, "¿tú vas a comprar algo este viernes? (bucle): el policía vuelve a pitar")
def _(d):
    return P(CIU, [BG("bg_ciudad")] + trafico(d, 1470, 460, 0.6) + [PZ("policia_para", 540, S_C + 120, 1080, z=0.7), OB("silbato", 700, 760, 150, z=0.75, keys=late(0.2, 2, 0.12, 0.25))],
             cam(1.03, 1.0, (540, 1100)), "corte", sfx=[(0.1, "senal", -18, {"f": 2800})])


def micro(fondo, els, txt=None, col="#ffffff", cap_f="#c0392be6", sfx="pop"):
    def fn(d):
        return P(fondo, els(d), cam(1.15, 1.3, (540, 1000)), "corte", hud=[cap(0.0, d - 0.02, txt, col, cap_f, 130)] if txt else [], sfx=[(0.01, sfx, -18)])
    return fn


v.plano(10, "micro: los coches pegados")(micro(CIU, lambda d: [BG("bg_ciudad")] + trafico(d, 1100, 900, 0.05, 2, 0.6), "ATASCO", sfx="impacto"))
v.plano(28, "micro: la calle llena")(micro(CIU, lambda d: [BG("bg_ciudad"), PZ("compradora", 540, S_C, 1050)], sfx="pop"))
v.plano(135, "micro: monedas que caen")(micro(["#1a1408", "#050302"], lambda d: [OB("monedas_oro", 540, 1000, 800, keys=[{"t": 0, "y": 1000}, {"t": d, "y": 1150, "ease": "entrada"}])], sfx="golpe"))


v.construir("2026-11-26-tarde-03-black-friday-policia", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 1263, "db": -13},
            claves=["policía", "Black", "Friday", "atasco", "Filadelfia", "sesenta", "Gracias", "miles", "comprar", "sábado", "partido", "Ejército", "Marina",
                    "Tráfico", "robos", "librar", "turnos", "Viernes", "negro", "gran", "funcionó", "rojos", "negros", "ochenta", "oro", "mundo"],
            ep_extra={"sfx_bajo_voz": True})
