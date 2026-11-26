"""01 · Tu teléfono no ha vibrado (vibración fantasma) — método denso, estilo del vídeo largo. Lote 2026-11-25-tarde (Jorge, con el agente).
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comun_1125t as C  # noqa: E402
from comun_1125t import *  # noqa: E402,F401,F403
import ilus_1125t  # noqa: E402

SVG = ilus_1125t.generar(os.path.join(sys.argv[1], "_svg_lote"))
C.SVG_DIR = SVG
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
CIU = ["#141a3e", "#0c0c14"]
OFI = ["#d8dce2", "#8a9098"]
CER = ["#0b0f24", "#1b1340"]
S_C, S_O = SUELO["bg_ciudad"], SUELO["bg_oficina_gris"]


def bolsillo(d, t0=0.0, t1=None, ancho=980, y=1000):
    t1 = d if t1 is None else t1
    return [OB("bolsillo", 540, y, ancho, keys=vibra(t0, t1, 540, 10) + [{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.05, "ease": "suave"}]),
            OB("ondas_vibra", 540, y - 60, ancho * 1.1, z=0.6, keys=[{"t": 0, "op": 0}, {"t": t0 + 0.05, "op": 1}, {"t": t1, "op": 1}, {"t": t1 + 0.1, "op": 0}] + late(t0, 3, 0.06, 0.3))]


@v.plano(0, "gancho: el bolsillo vibra y suenan las ondas")
def _(d):
    return P(OSC, bolsillo(d, 0.0, min(1.6, d)), cam(1.0, 1.1, (540, 1000)), vineta=0.4, sfx=[(0.02, "zap", -20), (0.5, "zap", -22)])


@v.plano(5, "lo has notado en el bolsillo: la chica en la calle se lleva la mano al bolsillo")
def _(d):
    return P(CIU, [BG("bg_ciudad"), PZ("chica_bolsillo", 540, S_C, 1000, keys=[{"t": 0, "escala": 0.98}, {"t": d, "escala": 1.03, "ease": "suave"}]),
                   OB("ondas_vibra", 600, 1150, 420, z=0.6, keys=late(0.1, 3, 0.08, 0.3))],
             cam(1.0, 1.15, (540, 1100), (560, 1150)), "corte", sfx=[(0.1, "zap", -22)])


@v.plano(11, "lo sacas: el teléfono sube rápido hasta la cara")
def _(d):
    return P(CIU, [BG("bg_ciudad"), OB("telefono_movil", 540, 1000, 440, keys=[{"t": 0, "y": 1900, "rot": 20}, {"t": 0.45, "y": 1000, "rot": 0, "ease": "salida"}, {"t": d, "y": 980}])],
             cam(1.0, 1.06, (540, 1000)), "corte", sfx=[(0.05, "whoosh", -20)])


@v.plano(13, "y no hay nada: pantalla quieta y la cara de duda")
def _(d):
    return P(OSC, [BG("bg_ciudad"), OB("cara_chica_pensativa", 540, 1080, 900, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.04}]),
                   OB("telefono_movil", 820, 1240, 260, z=0.6, keys=[{"t": 0, "rot": -8}, {"t": d, "rot": -4}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[cap(0.15, d - 0.05, "0 AVISOS", "#ffffff", "#c0392be6", 110)], sfx=[(0.1, "pop", -20)])


@v.plano(17, "tranquilo, no te pasa solo a ti: fila de gente en la calle")
def _(d):
    xs = [150, 340, 540, 740, 930]
    ps = ["voluntario_1", "voluntario_2", "chica_bolsillo", "voluntario_4", "voluntario_5"]
    return P(CIU, [BG("bg_ciudad")] + [PZ(p, x, S_C, 700, keys=aparece(0.08 * i)) for i, (p, x) in enumerate(zip(ps, xs))],
             cam(1.0, 1.05, (540, 1100)), "corte", sfx=[(0.08 * i, "pop", -24) for i in range(5)])


@v.plano(24, "le pasa a casi todo el mundo: la Tierra gira con ondas de vibración")
def _(d):
    return P(ESP, [estrellas(80, 1), OB("foto_mundo", 540, 1000, 760, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 12}] + aparece(0.0)),
                   OB("ondas_vibra", 540, 1000, 1000, z=0.6, keys=late(0.3, 3, 0.06, 0.35))],
             cam(1.0, 1.06, (540, 1000)), "desenfoque", hud=[cap(0.3, d - 0.05, "CASI TODO EL MUNDO", tam=80)], sfx=[(0.1, "brillo", -20)])


@v.plano(31, "en dos mil diez: un hospital de Estados Unidos, con médicos y enfermeros")
def _(d):
    return P(OFI, [BG("bg_oficina_gris"), PZ("medico_1", 300, S_O, 760, keys=aparece(0.3)), PZ("medica_2", 540, S_O - 30, 720, z=0.48, keys=aparece(0.45)),
                   PZ("enfermero_3", 780, S_O, 760, keys=aparece(0.6))],
             cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[BANDA(), contador(0.05, min(1.0, d - 0.05), 2000, 2010, 0.5, miles=False, tam=150, color="#141414", capsula="#ffffffe6", y=600)],
             sfx=[(0.1, "tic", -18), (0.3, "pop", -24), (0.6, "pop", -24)])


@v.plano(42, "un hospital de Estados Unidos: los tres, más cerca")
def _(d):
    return P(OFI, [BG("bg_oficina_gris"), PZ("medico_1", 330, S_O, 900), PZ("enfermero_3", 750, S_O, 900)],
             cam(1.05, 1.12, (540, 1100)), "corte", hud=[BANDA(), cap(0.1, d - 0.05, "HOSPITAL · EE. UU.", "#ffffff", "#2a5ae8e6", 80)], sfx=[(0.1, "roce", -22)])


@v.plano(46, "casi siete de cada diez lo habían sentido: se encienden siete de diez")
def _(d):
    ps = ("medico_1", "medica_2", "enfermero_3")
    return P(OFI, [BG("bg_oficina_gris")] + gente(10, 7, 0.2, 1130, 175, piezas=ps), cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[BANDA(), cap(0.4, d - 0.05, "7 DE CADA 10", "#141414", "#7df9ffe6", 120)], sfx=[(0.2 + 0.06 * i, "tic", -24) for i in range(7)])


@v.plano(54, "y en dos mil doce, con estudiantes universitarios: grupo de jóvenes")
def _(d):
    return P(CIU, [BG("bg_ciudad"), PZ("chico_bolsillo", 330, S_C, 800, keys=aparece(0.2)), PZ("chica_saluda", 560, S_C - 20, 780, z=0.48, keys=aparece(0.35)),
                   PZ("voluntario_5", 790, S_C, 800, keys=aparece(0.5))],
             cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[contador(0.05, min(1.0, d - 0.05), 2000, 2012, 0.5, miles=False, tam=150, color="#141414", capsula="#ffffffe6", y=600)],
             sfx=[(0.1, "tic", -18)])


@v.plano(62, "fueron casi nueve de cada diez: se encienden nueve")
def _(d):
    ps = ("chico_bolsillo", "chica_saluda", "voluntario_5", "voluntario_2", "voluntario_4")
    return P(CIU, [BG("bg_ciudad")] + gente(10, 9, 0.15, 1130, 175, "#ff3df2", ps), cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[cap(0.3, d - 0.05, "9 DE CADA 10", "#ffffff", "#c0392be6", 120)], sfx=[(0.15 + 0.06 * i, "tic", -24) for i in range(9)])


@v.plano(68, "tiene nombre, vibración fantasma: el teléfono se vuelve transparente entre neuronas")
def _(d):
    return P(CER, [BG("bg_cerebro"), OB("telefono_movil", 540, 1000, 420, keys=[{"t": 0, "op": 1}, {"t": d * 0.6, "op": 0.35, "ease": "suave"}] + flota(d, 16, 1000)),
                   OB("ondas_vibra", 540, 960, 760, z=0.6, keys=late(0.2, 3, 0.06, 0.4))],
             cam(1.0, 1.08, (540, 1000)), "corte", hud=[amarillo(d * 0.35, d - 0.05, "VIBRACIÓN FANTASMA", y=1420, tam=84, color=CIAN)], sfx=[(d * 0.35, "brillo", -18)])


@v.plano(72, "¿por qué pasa?: la chica piensa")
def _(d):
    return P(OSC, [BG("bg_ciudad"), OB("cara_chica_pensativa", 540, 1100, 980, keys=[{"t": 0, "escala": 1.05}, {"t": d, "escala": 1.0, "ease": "salida"}])],
             cam(1.0, 1.04, (540, 1000)), "corte", hud=[amarillo(0.05, d - 0.03, "¿POR QUÉ?", y=560, tam=130, color=AMBAR)], sfx=[(0.05, "impacto", -18)])


@v.plano(75, "tu cerebro vive pendiente de ese aviso: el cerebro dentro de la cabeza, con el teléfono al lado")
def _(d):
    return P(CER, [BG("bg_seccion_cabeza"), OB("cerebro", 505, 700, 520, keys=late(0.2, 1, 0.04)),
                   OB("telefono_movil", 860, 1100, 200, z=0.6, keys=flota(d, 12, 1100)),
                   flecha([[820, 1020], [640, 820]], 0.3, 0.8, CIAN, 10, disc=[16, 12], z=0.6)],
             cam(1.0, 1.05, (540, 900)), "corte", sfx=[(0.3, "senal", -22)])


@v.plano(82, "así que está en alerta todo el día: el cerebro se enciende y late")
def _(d):
    return P(CER, [BG("bg_cerebro"), OB("cerebro_brillo", 540, 960, 760, keys=late(0.1, 4, 0.05, 0.4)), brillo(540, 960, 460, "#2ff3ff", 0.4, 0.06, pulso=[0.2, 0.5])],
             cam(1.0, 1.08, (540, 960)), "corte", hud=[cap(0.2, d - 0.05, "EN ALERTA", "#ffffff", "#c0392be6", 120)], sfx=[(0.1, "senal", -20)])


@v.plano(90, "cuando nota un roce de la ropa: la tela del bolsillo se frota")
def _(d):
    return P(OSC, [OB("bolsillo", 540, 1000, 1000, keys=[{"t": 0, "x": 520}, {"t": d * 0.5, "x": 560, "ease": "suave"}, {"t": d, "x": 530, "ease": "suave"}]),
                   flecha([[260, 1250], [820, 1150]], 0.2, 0.8, "#ffffffcc", 12, z=0.6)],
             cam(1.1, 1.2, (540, 1000)), "corte", hud=[cap(0.3, d - 0.05, "UN ROCE", tam=110)], sfx=[(0.2, "roce", -16)])


@v.plano(97, "o un pequeño tirón de un músculo: anillo en la pierna del chico")
def _(d):
    return P(CIU, [BG("bg_ciudad"), PZ("chico_bolsillo", 540, S_C, 1100), senala(600, 1170, 0.2, d - 0.05, 100, MAGENTA)],
             cam(1.1, 1.3, (540, 1050), (580, 1150)), "corte", hud=[cap(0.3, d - 0.05, "UN TIRÓN", "#ffffff", "#c0392be6", 110)], sfx=[(0.25, "pop", -18)])


@v.plano(104, "prefiere equivocarse: el cerebro con un interrogante")
def _(d):
    return P(CER, [BG("bg_cerebro"), OB("cerebro", 540, 1000, 680, keys=[{"t": 0, "rot": -4}, {"t": d, "rot": 4, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[amarillo(0.2, d - 0.05, "MEJOR EQUIVOCARSE", y=560, tam=84, color=AMBAR)], sfx=[(0.1, "whoosh", -22)])


@v.plano(106, "mejor creer que vibra y mirar, que perderse un mensaje: la mujer mira el teléfono por la calle")
def _(d):
    return P(CIU, [BG("bg_ciudad"), PZ("adulto_camina", 540, S_C, 1000, keys=[{"t": 0, "x": 380}, {"t": d, "x": 700, "ease": "lineal"}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[cap(0.4, d - 0.05, "POR SI ACASO, MIRA", tam=80)], sfx=[(0.2, "pop", -22)])


@v.plano(116, "es lo mismo que oír tu nombre entre el ruido de una cafetería: gente charlando y el chico se gira")
def _(d):
    S = SUELO["bg_ventana_invierno"]
    return P(["#3a2418", "#120a06"], [BG("bg_ventana_invierno"), PZ("voluntario_2", 170, S, 760), PZ("voluntario_3", 380, S - 20, 720, z=0.48),
                                     PZ("voluntario_6", 900, S - 10, 740, z=0.48), OB("cara_chico_alerta", 640, 1260, 760, z=0.55, keys=aparece(d * 0.5)),
                                     OB("taza_cafe", 900, 1420, 200, z=0.6)],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[amarillo(d * 0.5, d - 0.05, "¡TU NOMBRE!", y=560, tam=120, color=AMBAR)], sfx=[(0.1, "rumor", -24, {"dur": d}), (d * 0.5, "ding", -18)])


@v.plano(130, "¿y cómo se quita?: el teléfono flota delante")
def _(d):
    return P(OSC, [OB("telefono_movil", 540, 1000, 440, keys=flota(d, 18, 1000) + [{"t": 0, "rot": -6}, {"t": d, "rot": 6}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[amarillo(0.1, d - 0.05, "¿CÓMO SE QUITA?", y=560, tam=100, color=CIAN)], sfx=[(0.05, "pop", -20)])


@v.plano(134, "cambiar el teléfono de bolsillo: el teléfono salta de un bolsillo al otro")
def _(d):
    return P(CIU, [BG("bg_ciudad"), PZ("chica_saluda", 540, S_C, 1000),
                   OB("telefono_movil", 640, 1180, 120, z=0.6, keys=[{"t": 0, "x": 600, "y": 1190}, {"t": d * 0.7, "x": 430, "y": 900, "ease": "suave"}, {"t": d, "x": 440, "y": 880}])],
             cam(1.0, 1.08, (540, 1050)), "corte", hud=[cap(0.3, d - 0.05, "OTRO BOLSILLO", tam=100)], sfx=[(0.2, "whoosh", -20)])


@v.plano(144, "o quitar la vibración: las ondas se tachan")
def _(d):
    return P(OSC, [OB("telefono_movil_b", 540, 1000, 420), OB("ondas_vibra", 540, 960, 760, z=0.6, keys=[{"t": 0, "op": 1}, {"t": d * 0.5, "op": 0.3}]), *tacha(540, 980, 0.25, 240)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.3, d - 0.05, "SIN VIBRACIÓN", "#ffffff", "#2a5ae8e6", 100)], sfx=[(0.25, "zap", -18)])


@v.plano(148, "¿a ti te pasa?: el bolsillo vuelve a vibrar (bucle)")
def _(d):
    return P(OSC, bolsillo(d, 0.2, d - 0.1), cam(1.0, 1.06, (540, 1000)), "corte", sfx=[(0.2, "zap", -22)])


v.construir("2026-11-25-tarde-01-vibracion-fantasma", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 1251, "db": -13},
            claves=["teléfono", "vibrado", "bolsillo", "nada", "médicos", "enfermeros", "hospital", "siete", "nueve", "universitarios",
                    "vibración", "fantasma", "cerebro", "alerta", "roce", "músculo", "mensaje", "nombre", "cafetería"],
            ep_extra={"sfx_bajo_voz": True})
