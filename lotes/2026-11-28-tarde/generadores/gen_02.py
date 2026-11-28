"""02 · ¿Dónde están las estrellas? (fotos del Apolo) — método denso, estilo del vídeo largo. Lote 2026-11-28-tarde (Jorge con el agente).
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comun_1128t as C  # noqa: E402
from comun_1128t import *  # noqa: E402,F401,F403
import ilus_1128t  # noqa: E402

SVG = ilus_1128t.generar(os.path.join(sys.argv[1], "_svg_lote"))
C.SVG_DIR = SVG
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
LUNA = ["#000000", "#1a1a1a"]
CIU = ["#141a3e", "#0c0c14"]
CIAN, ROJO = "#2ff3ff", "#ff3d3d"
SL = 1150 + 60   # suelo de bg_luna_superficie


def luna(extra, quemada=False):
    return [BG("bg_luna_superficie_quemada" if quemada else "bg_luna_superficie")] + extra


def astro(x=540, alto=900, n="astronauta", keys=None, z=0.5):
    return PZ(n, x, SL + 250, alto, z=z, keys=keys)


@v.plano(0, "gancho: astronauta enorme en la Luna bajo un cielo negro, y una lupa busca estrellas")
def _(d):
    return P(LUNA, luna([astro(380, 1100, keys=[{"t": 0, "x": 330}, {"t": d, "x": 400}]), senala(760, 600, 0.1, d - 0.05, 140, CIAN)]),
             cam(1.0, 1.08, (540, 1000)), vineta=0.3, sfx=[(0.1, "whoosh", -16)])


@v.plano(4, "en las fotos del Apolo, ni una: la foto con marco")
def _(d):
    return P(LUNA, luna([OB("foto_luna", 540, 1000, 760, keys=aparece(0.0) + [{"t": 0, "rot": -4}, {"t": d, "rot": 2}])]),
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.1, d - 0.02, "NI UNA", "#ffffff", "#c0392be6", 120, y=1500)], sfx=[(0.05, "pop", -18)])


@v.plano(11, "el cielo de la Luna sale negro")
def _(d):
    return P(LUNA, luna([astro(700, 700)]), cam(1.1, 1.0, (540, 700), (540, 1000)), "corte",
             hud=[cap(0.3, d - 0.05, "CIELO NEGRO", "#ffffff", "#141414e6", 110, y=640)], sfx=[(0.1, "roce", -22)])


@v.plano(18, "y no, no es un truco: la foto se tacha")
def _(d):
    return P(LUNA, luna([OB("foto_luna", 540, 1000, 700)] + tacha(540, 1000, 0.2, 200)), cam(1.0, 1.05, (540, 1000)), "corte",
             hud=[amarillo(0.05, d - 0.05, "NO ES TRUCO", y=1500, tam=110, color=AMBAR)], sfx=[(0.2, "impacto", -18)])


@v.plano(24, "allí no hay aire, así que el cielo es negro también de día")
def _(d):
    return P(LUNA, luna([astro(300, 760), OB("sol_poniente", 820, 520, 360, z=0.2)]), cam(1.0, 1.05, (540, 1000)), "corte",
             hud=[cap(0.3, d - 0.05, "SIN AIRE", "#141414", "#7df9ffe6", 110, y=900)], sfx=[(0.1, "brillo", -20)])


@v.plano(37, "pero el sol pega igual de fuerte que aquí al mediodía: el sol enorme brilla")
def _(d):
    return P(LUNA, luna([OB("sol_poniente", 540, 800, 900, keys=late(0.1, 2, 0.05, 0.4)), astro(540, 760)]), cam(1.0, 1.05, (540, 1000)), "corte",
             hud=[cap(0.3, d - 0.05, "COMO AL MEDIODÍA", "#141414", "#ffd23fe6", 90, y=1600)], sfx=[(0.1, "brillo", -18)])


@v.plano(48, "la cámara se ajustó para el suelo iluminado y los trajes blancos: el astronauta con la cámara")
def _(d):
    return P(LUNA, luna([astro(540, 1000, "astronauta_camara")]), cam(1.1, 1.2, (540, 1250)), "corte",
             hud=[cap(0.3, d - 0.05, "TRAJES BLANCOS", "#141414", "#ffffffe6", 96, y=640)], sfx=[(0.1, "pop", -20)])


@v.plano(59, "muy poca luz y muy poco tiempo: el diafragma se cierra")
def _(d):
    return P(LUNA, [BG("bg_luna_superficie"), OB("diafragma", 540, 1050, 800, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 40}, {"t": 0, "escala": 1.1}, {"t": d * 0.5, "escala": 1.0}])],
             cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[cap(0.2, d - 0.05, "POCO TIEMPO", "#141414", "#7df9ffe6", 110, y=640)],
             sfx=[(0.3, "tic", -16)])


@v.plano(67, "y las estrellas son tan débiles que no les da tiempo a aparecer: asoman un instante y se apagan")
def _(d):
    est = {**BG("bg_luna_superficie_estrellas", z=0.06), "keys": [{"t": 0, "op": 0}, {"t": d * 0.4, "op": 0.45}, {"t": d * 0.8, "op": 0}]}
    return P(LUNA, luna([est, astro(540, 760)]), cam(1.0, 1.05, (540, 900)), "corte",
             hud=[cap(0.3, d - 0.05, "MUY DÉBILES", "#ffffff", "#2a5ae8e6", 110, y=640)], sfx=[(0.2, "brillo", -22)])


@v.plano(80, "es como hacerle una foto a un amigo bajo una farola, de noche")
def _(d):
    S = SUELO["bg_ciudad"]
    return P(CIU, [BG("bg_ciudad"), PZ("farola", 380, S, 1000, z=0.55), PZ("amigo_farola", 560, S, 640, z=0.5),
                   brillo(470, 900, 420, "#ffd890", 0.8, 0.6)],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[cap(0.05, d - 0.02, "BAJO UNA FAROLA", "#141414", "#ffd23fe6", 90, y=640)], sfx=[(0.1, "pop", -22)])


@v.plano(93, "él sale bien y el cielo, vacío: flash y foto")
def _(d):
    S = SUELO["bg_ciudad"]
    return P(CIU, [BG("bg_ciudad"), PZ("farola", 380, S, 900, z=0.45), PZ("amigo_farola", 560, S, 640, z=0.5),
                   brillo(540, 1000, 900, "#ffffff", 0.9, 0.9, keys=[{"t": 0, "op": 0}, {"t": 0.1, "op": 1}, {"t": 0.35, "op": 0}])],
             cam(1.1, 1.15, (520, 1100)), "corte", hud=[cap(0.5, d - 0.05, "CIELO VACÍO", "#ffffff", "#141414e6", 100, y=640)], sfx=[(0.1, "brillo", -16)])


@v.plano(100, "si dejas la cámara abierta mucho rato, las estrellas aparecen: el cielo se llena")
def _(d):
    est = {**BG("bg_luna_superficie_estrellas", z=0.06), "keys": [{"t": 0, "op": 0}, {"t": d * 0.8, "op": 1, "ease": "suave"}]}
    return P(LUNA, luna([est, astro(540, 760)]), cam(1.0, 1.05, (540, 900)), "corte",
             hud=[contador(0.05, d - 0.05, 1, 30, max(0.6, d * 0.7), " S", tam=120, color="#141414", capsula="#ffffffe6", y=640)], sfx=[(0.1, "tic", -20)])


@v.plano(110, "pero el suelo y los astronautas salen blancos, quemados")
def _(d):
    return P(["#ffffff", "#e0e0e0"], [BG("bg_luna_superficie_quemada"), astro(540, 800, keys=[{"t": 0, "op": 1}, {"t": d * 0.5, "op": 0.35}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.2, d - 0.05, "QUEMADOS", "#ffffff", "#c0392be6", 120, y=640)], sfx=[(0.1, "impacto", -18)])


@v.plano(119, "por eso casi ninguna foto de día en el espacio tiene estrellas: la Tierra desde la órbita")
def _(d):
    return P(["#02030a", "#0a1030"], [BG("bg_estratosfera"), OB("satelite_obs", 760, 700, 300, z=0.6, keys=[{"t": 0, "x": 860}, {"t": d, "x": 640}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[cap(0.3, d - 0.05, "SIN ESTRELLAS", "#141414", "#7df9ffe6", 100, y=640)], sfx=[(0.1, "senal", -22)])


@v.plano(131, "tampoco las de la Estación Espacial: foto que sale de la cámara")
def _(d):
    return P(["#02030a", "#0a1030"], [BG("bg_estratosfera"), OB("foto_luna", 540, 1000, 640, keys=aparece(0.0))], cam(1.0, 1.05, (540, 1000)), "corte",
             hud=[cap(0.3, d - 0.05, "ESTACIÓN ESPACIAL", "#141414", "#ffffffe6", 86, y=640)], sfx=[(0.1, "pop", -22)])


@v.plano(137, "estaban ahí: las estrellas se encienden todas sobre la Luna")
def _(d):
    return P(LUNA, [BG("bg_luna_superficie_estrellas"), astro(540, 760)], cam(1.1, 1.0, (540, 800), (540, 1000)), "corte",
             hud=[amarillo(0.05, d - 0.05, "ESTABAN AHÍ", y=640, tam=120, color=CIAN)], sfx=[(0.05, "brillo", -16)])


@v.plano(139, "¿lo sabías? (bucle): astronauta bajo el cielo negro")
def _(d):
    return P(LUNA, luna([astro(380, 1100)]), cam(1.0, 1.06, (540, 1000)), "corte", sfx=[(0.05, "whoosh", -20)])


def micro(fondo, els, txt=None, col="#ffffff", cap_f="#c0392be6", sfx="pop"):
    def fn(d):
        return P(fondo, els(d), cam(1.15, 1.3, (540, 1000)), "corte", hud=[cap(0.0, d - 0.02, txt, col, cap_f, 120)] if txt else [], sfx=[(0.01, sfx, -18)])
    return fn


v.plano(33, "micro: cielo negro")(micro(LUNA, lambda d: [BG("bg_luna_superficie"), OB("sol_poniente", 540, 1000, 500)], "NEGRO", "#ffffff", "#141414e6", "impacto"))
v.plano(62, "micro: objetivo")(micro(LUNA, lambda d: [BG("bg_luna_superficie"), OB("diafragma", 540, 1000, 1100, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 25}])], sfx="tic"))
v.plano(87, "micro: el amigo")(micro(["#141a3e", "#0c0c14"], lambda d: [BG("bg_ciudad"), OB("cara_mirador", 540, 1100, 1000)], sfx="pop"))
v.plano(128, "micro: la Tierra")(micro(["#02030a", "#0a1030"], lambda d: [BG("bg_estratosfera"), OB("foto_mundo", 540, 1100, 900)], sfx="whoosh"))

v.plano(10, "micro: foto en negro")(micro(LUNA, lambda d: [BG("bg_luna_superficie"), OB("foto_luna", 540, 1000, 1100)], sfx="pop"))
v.plano(23, "micro: truco")(micro(LUNA, lambda d: [BG("bg_luna_superficie"), OB("foto_luna", 540, 1000, 900, keys=[{"t": 0, "rot": -8}, {"t": d, "rot": 0}])], sfx="impacto"))
v.plano(47, "micro: sol de mediodía")(micro(LUNA, lambda d: [BG("bg_luna_superficie"), OB("sol_poniente", 540, 900, 1100)], sfx="brillo"))
v.plano(79, "micro: estrella que no llega")(micro(LUNA, lambda d: [BG("bg_luna_superficie_estrellas")], sfx="tic"))
v.plano(99, "micro: cielo vacío")(micro(["#141a3e", "#0c0c14"], lambda d: [BG("bg_ciudad")], sfx="pop"))
v.plano(118, "micro: quemado")(micro(["#ffffff", "#e0e0e0"], lambda d: [BG("bg_luna_superficie_quemada")], sfx="impacto"))


v.construir("2026-11-28-tarde-02-estrellas-luna", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 1282, "db": -13},
            claves=["estrellas", "Apolo", "negro", "truco", "aire", "sol", "mediodía", "cámara", "blancos", "luz", "tiempo", "débiles",
                    "farola", "vacío", "aparecen", "quemados", "espacio", "Estación", "ahí"],
            ep_extra={"sfx_bajo_voz": True})
