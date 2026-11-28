"""03 · Se te cae la tostada (cae del lado de la mantequilla) — método denso, estilo del vídeo largo. Lote 2026-11-28-tarde (Jorge con el agente).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comun_1128t as C  # noqa: E402
from comun_1128t import *  # noqa: E402,F401,F403
import ilus_1128t  # noqa: E402

SVG = ilus_1128t.generar(os.path.join(sys.argv[1], "_svg_lote"))
C.SVG_DIR = SVG
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
COC = ["#f6efe0", "#c8b090"]
CASA = ["#d8dce2", "#8a9098"]
CIAN, LIMA = "#2ff3ff", "#5dff8a"
SC = 1600  # suelo de la cocina (las patas de la mesa caen aquí)
MESA_Y = SC - 400 * 0.95  # parte de arriba de la mesa (mesa 1000x800 con ancho 1000)


def cocina(extra):
    return [BG("bg_cocina"), OB("mesa_cocina", 400, SC - 400 + 20, 1000, z=0.4)] + extra


def cae_tostada(t0, t1, x0=780, y0=1180, x1=980, y1=1560, giro=180, ancho=300, z=0.6):
    """La tostada resbala del borde y cae girando media vuelta (mantequilla abajo al llegar)."""
    return OB("tostada", x0, y0, ancho, z=z, keys=[{"t": 0, "x": x0, "y": y0, "rot": 0}, {"t": t0, "x": x0, "y": y0, "rot": 0},
                                                    {"t": t0 + (t1 - t0) * 0.25, "x": x0 + 60, "y": y0 + 30, "rot": giro * 0.2},
                                                    {"t": t1, "x": x1, "y": y1, "rot": giro, "ease": "entrada"}])


@v.plano(0, "gancho: la tostada enorme cae girando hacia el suelo")
def _(d):
    return P(COC, cocina([OB("tostada", 540, 700, 760, z=0.6, keys=[{"t": 0, "y": 640, "rot": -30}, {"t": d, "y": 1450, "rot": 170, "ease": "lineal"}])]),
             cam(1.0, 1.06, (540, 1100)), vineta=0.3, sfx=[(0.0, "whoosh", -14), (d - 0.1, "impacto", -16)])


@v.plano(5, "¿y cómo cae?: la tostada en el suelo, de canto")
def _(d):
    return P(COC, cocina([OB("tostada_sin", 760, 1560, 340, z=0.6, keys=late(0.1, 1, 0.06, 0.3))]), cam(1.15, 1.2, (700, 1400)), "corte",
             hud=[cap(0.05, d - 0.05, "¿CÓMO CAE?", "#ffffff", "#141414e6", 120, y=640)], sfx=[(0.05, "pop", -18)])


@v.plano(8, "con la mantequilla abajo: se levanta y se ve la mancha")
def _(d):
    return P(COC, cocina([OB("tostada", 760, 1540, 380, z=0.6, keys=[{"t": 0, "rot": 180}, {"t": d * 0.6, "rot": 180}]),
                          {"tipo": "forma", "forma": "rect", "ancho": 300, "alto": 20, "relleno": "#f0c838", "x": 760, "y": 1580, "z": 0.55}]),
             cam(1.2, 1.3, (760, 1450)), "corte", hud=[cap(0.2, d - 0.05, "MANTEQUILLA ABAJO", "#141414", "#ffd23fe6", 86, y=640)], sfx=[(0.2, "pop", -18)])


@v.plano(12, "no es mala suerte: es física")
def _(d):
    return P(CASA, [BG("bg_oficina_gris"), OB("tostada", 540, 1100, 700, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 360, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[BANDA(), cap(0.02, max(1.05, d * 0.45), "¿MALA SUERTE?", "#ffffff", "#c0392be6", 100, y=760),
                                                         cap(max(1.1, d * 0.5), d - 0.05, "FÍSICA", "#141414", "#7df9ffe6", 130, y=760)], sfx=[(0.05, "impacto", -18)])


@v.plano(18, "en mil novecientos noventa y cinco, el físico Robert Matthews lo explicó")
def _(d):
    S = SUELO["bg_oficina_gris"]
    return P(CASA, [BG("bg_oficina_gris"), PZ("fisico", 540, S, 1050, keys=aparece(0.0))], cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[BANDA(), contador(0.05, min(1.2, d * 0.5), 1980, 1995, 0.5, miles=False, tam=130, color="#141414", capsula="#ffffffe6", y=760),
                  cap(min(1.3, d * 0.55), d - 0.05, "ROBERT MATTHEWS", "#ffffff", "#2a5ae8e6", 86, y=760)], sfx=[(0.05, "tic", -20)])


@v.plano(30, "y no es por el peso de la mantequilla: casi no cuenta, una balanza")
def _(d):
    return P(COC, cocina([OB("tostada", 540, 1000, 600, z=0.6, keys=[{"t": 0, "rot": -6}, {"t": d, "rot": 4, "ease": "suave"}])] + tacha(540, 980, 0.6, 180)),
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[cap(0.2, d - 0.05, "NO ES EL PESO", "#ffffff", "#c0392be6", 100, y=640)], sfx=[(0.6, "impacto", -18)])


@v.plano(42, "cuando la tostada resbala por el borde de la mesa, empieza a girar")
def _(d):
    return P(COC, cocina([cae_tostada(0.2, d, 760, 1190, 880, 1330, 60, 300),
                          flecha([[700, 1120], [880, 1100], [960, 1230]], 0.3, d * 0.8, CIAN, 10, z=0.7)]),
             cam(1.1, 1.15, (720, 1250)), "corte", hud=[cap(0.3, d - 0.05, "EMPIEZA A GIRAR", "#141414", "#7df9ffe6", 90, y=640)], sfx=[(0.2, "roce", -18)])


@v.plano(55, "y desde la altura de una mesa normal: flecha de altura")
def _(d):
    return P(COC, cocina([flecha([[960, 1200], [960, 1590]], 0.1, 0.6, AMBAR, 12, z=0.7), OB("tostada", 780, 1180, 260, z=0.6)]),
             cam(1.0, 1.04, (600, 1300)), "corte", hud=[cap(0.4, d - 0.05, "UNOS 75 CM", "#141414", "#ffd23fe6", 110, y=640)], sfx=[(0.1, "tic", -20)])


@v.plano(63, "solo le da tiempo a dar media vuelta: cae girando 180 grados con su trazo")
def _(d):
    return P(COC, cocina([cae_tostada(0.05, d * 0.9, 780, 1180, 960, 1560, 180, 300),
                          flecha([[790, 1180], [920, 1300], [960, 1520]], 0.05, d * 0.85, AMBAR, 10, disc=[18, 14], z=0.55)]),
             cam(1.0, 1.04, (640, 1300)), "corte", hud=[cap(0.3, d - 0.05, "MEDIA VUELTA", "#141414", "#ffd23fe6", 110, y=640)], sfx=[(d * 0.9, "impacto", -16)])


@v.plano(71, "sale boca arriba y llega boca abajo: dos tostadas, arriba y abajo")
def _(d):
    return P(COC, cocina([OB("tostada", 780, 1170, 300, z=0.6, keys=aparece(0.0)), OB("tostada", 940, 1560, 300, z=0.6, keys=[{"t": 0, "rot": 180, "op": 0}, {"t": d * 0.5, "op": 0}, {"t": d * 0.5 + 0.1, "op": 1}]),
                          flecha([[820, 1220], [930, 1480]], 0.2, d * 0.5, CIAN, 10, z=0.55)]),
             cam(1.0, 1.04, (700, 1350)), "corte", hud=[cap(0.1, d * 0.5, "BOCA ARRIBA", "#141414", "#5dff8ae6", 100, y=640),
                                                        cap(d * 0.5 + 0.05, d - 0.05, "BOCA ABAJO", "#ffffff", "#c0392be6", 100, y=640)], sfx=[(d * 0.5, "pop", -18)])


@v.plano(78, "para dar la vuelta entera, la mesa tendría que medir unos tres metros: mesa gigante")
def _(d):
    return P(COC, [BG("bg_cocina"), OB("mesa_cocina", 540, 1150, 900, z=0.4, keys=[{"t": 0, "escala": 0.6, "y": 1350}, {"t": d * 0.6, "escala": 1.4, "y": 1000, "ease": "salida"}])],
             cam(1.0, 1.04, (540, 1100)), "corte", hud=[contador(0.1, d - 0.05, 75, 300, max(0.5, d * 0.6), " CM", miles=False, tam=130, color="#141414", capsula="#ffd23fe6", y=640)],
             sfx=[(0.1, "whoosh", -18)])


@v.plano(91, "por eso le dieron el premio Ig Nobel de física: el trofeo")
def _(d):
    S = SUELO["bg_oficina_gris"]
    return P(CASA, [BG("bg_oficina_gris"), PZ("fisico", 380, S, 1000), OB("trofeo", 760, 1150, 320, z=0.6, keys=aparece(0.2) + late(0.4, 1, 0.08, 0.3))],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[BANDA(), cap(0.3, d - 0.05, "IG NOBEL 1996", "#141414", "#ffd23fe6", 100, y=760)], sfx=[(0.3, "ding", -16)])


@v.plano(101, "y ojo: en la tele británica la lanzaron al aire trescientas veces: el televisor")
def _(d):
    return P(COC, [BG("bg_cocina"), OB("televisor", 540, 1150, 800, keys=aparece(0.0))], cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[contador(0.2, d - 0.05, 0, 300, max(0.6, d * 0.6), " VECES", tam=110, color="#141414", capsula="#ffffffe6", y=640)], sfx=[(0.1, "pop", -20)])


@v.plano(113, "y salió mitad y mitad: dos montones de tostadas")
def _(d):
    els = [BG("bg_cocina")]
    for i in range(5):
        els.append(OB("tostada", 300, 1450 - i * 40, 280, z=0.6 + i * 0.01, keys=aparece(0.1 + 0.08 * i)))
        els.append(OB("tostada", 780, 1450 - i * 40, 280, z=0.6 + i * 0.01, keys=[{"t": 0, "rot": 180}] + aparece(0.1 + 0.08 * i)))
    return P(COC, els, cam(1.0, 1.04, (540, 1300)), "corte", hud=[cap(0.4, d - 0.05, "50 / 50", "#141414", "#7df9ffe6", 130, y=640)],
             sfx=[(0.1 + 0.08 * i, "pop", -24) for i in range(5)])


@v.plano(118, "lo que la hace caer mal es el borde de la mesa: se señala el borde")
def _(d):
    return P(COC, cocina([OB("tostada", 820, 1185, 280, z=0.6), senala(880, 1200, 0.1, d - 0.05, 120, "#ff3d3d")]), cam(1.2, 1.3, (820, 1250)), "corte",
             hud=[cap(0.3, d - 0.05, "EL BORDE", "#ffffff", "#c0392be6", 120, y=640)], sfx=[(0.1, "pop", -18)])


@v.plano(130, "¿el truco?")
def _(d):
    return P(COC, cocina([OB("tostada", 760, 1180, 300, z=0.6)]), cam(1.1, 1.15, (700, 1250)), "corte",
             hud=[cap(0.05, d - 0.05, "EL TRUCO", "#141414", "#ffd23fe6", 130, y=640)], sfx=[(0.05, "impacto", -16)])


@v.plano(132, "si ves que se cae, empújala rápido hacia delante: sale disparada casi plana y aterriza bien")
def _(d):
    return P(COC, cocina([OB("tostada", 760, 1180, 300, z=0.6, keys=[{"t": 0, "x": 760, "y": 1180, "rot": 0}, {"t": d * 0.8, "x": 1040, "y": 1560, "rot": 25, "ease": "entrada"}]),
                          flecha([[720, 1150], [980, 1200]], 0.0, 0.3, LIMA, 12, z=0.7)]),
             cam(1.0, 1.04, (760, 1350)), "corte", hud=[cap(0.3, d - 0.05, "EMPÚJALA RÁPIDO", "#141414", "#5dff8ae6", 96, y=640)], sfx=[(0.05, "whoosh", -16), (d * 0.8, "pop", -18)])


@v.plano(144, "¿te ha pasado hoy? (bucle): la tostada vuelve a caer")
def _(d):
    return P(COC, cocina([OB("tostada", 540, 900, 760, z=0.6, keys=[{"t": 0, "y": 800, "rot": -10}, {"t": d, "y": 1300, "rot": 120, "ease": "entrada"}])]),
             cam(1.0, 1.06, (540, 1100)), "corte", sfx=[(0.05, "whoosh", -18)])


def micro(fondo, els, txt=None, col="#ffffff", cap_f="#c0392be6", sfx="pop"):
    def fn(d):
        return P(fondo, els(d), cam(1.15, 1.3, (540, 1000)), "corte", hud=[cap(0.0, d - 0.02, txt, col, cap_f, 120)] if txt else [], sfx=[(0.01, sfx, -18)])
    return fn


v.plano(27, "micro: la cara del físico")(micro(CASA, lambda d: [BG("bg_oficina_gris"), OB("cara_fisico", 540, 1150, 1000)], sfx="pop"))
v.plano(48, "micro: el borde")(micro(COC, lambda d: [BG("bg_cocina"), OB("mesa_cocina", 200, 1300, 2000), OB("tostada", 900, 960, 500)], sfx="roce"))
v.plano(88, "micro: tres metros")(micro(COC, lambda d: [BG("bg_cocina"), OB("mesa_cocina", 540, 1150, 1400)], "3 M", "#141414", "#ffd23fe6", "impacto"))
v.plano(127, "micro: el borde de cerca")(micro(COC, lambda d: [BG("bg_cocina"), OB("mesa_cocina", 100, 1300, 2000)], sfx="tic"))


v.construir("2026-11-28-tarde-03-tostada", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 1283, "db": -13},
            claves=["tostada", "mantequilla", "abajo", "física", "Matthews", "peso", "borde", "girar", "media", "vuelta", "arriba",
                    "tres", "metros", "Ig", "Nobel", "trescientas", "mitad", "truco", "rápido", "delante"],
            ep_extra={"sfx_bajo_voz": True})
