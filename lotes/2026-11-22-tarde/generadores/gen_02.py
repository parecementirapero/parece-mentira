"""02 · Enamorarte cambia tu cerebro — método denso. Lote 2026-11-22-tarde (Jorge, con el agente). Tema pedido por Jorge: el amor.
Versión corta: se quita «Pues eso.» (palabras 135–136) para no pasar de 60 s.
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_1122t  # noqa: E402

SVG = ilus_1122t.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG, omitir=[(135, 137)])

ROSA = ["#3a0a2a", "#12020c"]
LAB = ["#0a2a2a", "#02100a"]
VTA = (513, 1135)   # zona profunda en cerebro_corte (ancho 900, centro 540,1000)


def corazones(n=24, sem=1): return polvo("#ff6aa0", n, (100, 500, 980, 1600), sem)
def cortado(keys=None, **k): return IMG("cerebro_corte", ancho=900, x=540, y=1000, z=0.45, keys=keys or [], **k)


def latido(t0, d, periodo=0.55, amp=0.1):
    return late(t0, max(1, int((d - t0) / periodo)), amp, periodo)


# ================================================================== PLANOS
@v.plano(0, "gancho: un corazón que late fuerte y, detrás, se enciende un cerebro")
def _(d):
    return P(ROSA, [brillo(540, 1000, 600, "#ff3d7a", 0.4, 0.06, pulso=[0.15, 0.55]), IMG("cerebro", ancho=900, x=540, y=980, z=0.3, keys=[{"t": 0, "op": 0}, {"t": d * 0.6, "op": 0.8}]),
                    IMG("corazon", ancho=560, x=540, y=1100, z=0.5, keys=arranque(540, 1100, d, "abajo", 260, 20) + latido(0.45, d)), corazones(20, 1)],
             cam(1.0, 1.08, (540, 1050)), vineta=0.5, sfx=[(0.05, "golpe", -16), (0.6, "golpe", -18), (1.15, "golpe", -18)])


@v.plano(4, "y se puede ver: el escáner del laboratorio")
def _(d):
    return P(LAB, [BG("bg_lab"), IMG("escaner", ancho=900, x=540, y=1150, z=0.5, keys=aparece(0.0))], cam(1.0, 1.06, (540, 1150)), "corte", sfx=[(0.05, "senal", -22)])


@v.plano(8, "la antropóloga Helen Fisher: el escáner con el nombre")
def _(d):
    return P(LAB, [BG("bg_lab"), IMG("escaner", ancho=900, x=540, y=1150, z=0.5)], cam(1.1, 1.15, (540, 1150)), "corte",
             hud=[rotulo(0.2, d - 0.05, "HELEN FISHER", tam=110, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(0.1, "pop", -22)])


@v.plano(12, "metió en un escáner a personas muy enamoradas: un corazón entra en el escáner")
def _(d):
    return P(LAB, [BG("bg_lab"), IMG("escaner", ancho=900, x=540, y=1150, z=0.5), IMG("corazon_rosa", ancho=220, z=0.55, keys=[{"t": 0, "x": 180, "y": 1180}, {"t": d * 0.8, "x": 590, "y": 1120, "ease": "suave"}] + latido(0.2, d, 0.5, 0.12))],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[amarillo(0.4, d - 0.05, "MUY ENAMORADOS", y=560, tam=110, color="#ff6aa0")], sfx=[(0.1, "whoosh", -22)])


@v.plano(20, "tanto que casi no comían ni dormían: cara de perfil con corazones alrededor")
def _(d):
    return P(ROSA, [IMG("cara_perfil", ancho=760, x=520, y=1150, z=0.5, keys=[{"t": 0, "rot": -2}, {"t": d, "rot": 2, "ease": "suave"}]), corazones(30, 2)],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[rotulo(0.3, d - 0.05, "NI COMER NI DORMIR", tam=86, color="#ffffff", capsula="#c0397ae6", y=560)], sfx=[(0.1, "brillo", -22)])


@v.plano(27, "les enseñaba una foto de su pareja")
def _(d):
    return P(ROSA, [brillo(540, 1050, 500, "#ff6aa0", 0.35, 0.06), IMG("foto_pareja", ancho=600, x=540, y=1050, z=0.5, keys=aparece(0.0) + [{"t": d, "rot": -3}])],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[amarillo(0.3, d - 0.05, "SU PAREJA", y=560, tam=120, color="#ff6aa0")], sfx=[(0.05, "pop", -20)])


@v.plano(34, "y luego la de un simple conocido: la otra foto tapa a la primera")
def _(d):
    return P(["#1a1a2a", "#06060e"], [IMG("foto_pareja", ancho=600, x=540, y=1050, z=0.4, op=0.5, rot=-3),
                                      IMG("foto_conocido", ancho=600, z=0.5, keys=[{"t": 0, "x": 1300, "y": 1080, "rot": 10}, {"t": 0.5, "x": 560, "rot": 2, "ease": "salida"}])],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[amarillo(0.4, d - 0.05, "UN CONOCIDO", y=560, tam=120, color="#c8c8d8")], sfx=[(0.1, "whoosh", -20)])


@v.plano(41, "¿qué pasaba?: las dos fotos, una al lado de otra")
def _(d):
    return P(["#1a1a2a", "#06060e"], [IMG("foto_pareja", ancho=430, x=300, y=1050, z=0.5, keys=late(0.2, 1)), IMG("foto_conocido", ancho=430, x=780, y=1050, z=0.5)],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[amarillo(0.1, d - 0.05, "¿QUÉ PASABA?", y=560, tam=110, color="#ffd23f")], sfx=[(0.05, "roce", -20)])


@v.plano(43, "con la persona amada se encendía una zona muy profunda del cerebro")
def _(d):
    return P(["#1a0a20", "#06020a"], [cortado(keys=aparece(0.0)), brillo(*VTA, 160, "#ffd23f", 0.9, 0.5, keys=[{"t": 0, "op": 0}, {"t": d * 0.6, "op": 1}], pulso=[0.2, 0.6]),
                                      IMG("foto_pareja", ancho=240, x=860, y=560, z=0.55, keys=aparece(0.2))],
             cam(1.0, 1.08, (540, 1000)), "corte", hud=[amarillo(0.5, d - 0.05, "SE ENCIENDE", y=1600 - 250, tam=110, color="#ffd23f")], sfx=[(d * 0.5, "subida", -18, {"dur": d * 0.5})])


@v.plano(53, "el área tegmental ventral: zoom a la zona")
def _(d):
    return P(["#1a0a20", "#06020a"], [cortado(), brillo(*VTA, 140, "#ffd23f", 1.0, 0.5, pulso=[0.2, 0.5]), senala(VTA[0], VTA[1], 0.1, d - 0.05, 80, AMBAR)],
             cam(1.6, 1.8, VTA), "corte", hud=[rotulo(0.1, d - 0.03, "ÁREA TEGMENTAL VENTRAL", tam=72, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "impacto", -16)])


@v.plano(57, "parte del circuito de recompensa: el circuito se dibuja por el cerebro")
def _(d):
    return P(["#1a0a20", "#06020a"], [cortado(), brillo(*VTA, 120, "#ffd23f", 0.8, 0.5),
                                      flecha([[VTA[0], VTA[1]], [600, 950], [700, 720], [560, 560], [380, 640], [330, 850], [470, 1060]], 0.05, d * 0.85, AMBAR, 9, z=0.6)],
             cam(1.0, 1.05, (540, 950)), "corte", hud=[amarillo(0.4, d - 0.05, "RECOMPENSA", y=1600 - 250, tam=120, color=AMBAR)], sfx=[(0.1, "trazo", -20)])


@v.plano(62, "ahí se fabrica dopamina: la molécula aparece y gira")
def _(d):
    return P(["#2a1a0a", "#0a0602"], [brillo(540, 1000, 500, "#ffd23f", 0.35, 0.06), IMG("dopamina", ancho=760, x=540, y=1000, z=0.5, keys=aparece(0.0) + [{"t": d, "rot": 8}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[rotulo(0.3, d - 0.05, "DOPAMINA", tam=120, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "brillo", -18)])


@v.plano(66, "la sustancia de las ganas y del placer: la molécula rodeada de corazones")
def _(d):
    return P(["#2a0a1a", "#0a0206"], [IMG("dopamina", ancho=620, x=540, y=1000, z=0.5, keys=[{"t": 0, "rot": 8}, {"t": d, "rot": 20, "ease": "suave"}]), corazones(40, 3)],
             cam(1.05, 1.12, (540, 1000)), "corte", hud=[amarillo(0.3, d - 0.05, "GANAS Y PLACER", y=560, tam=110, color="#ff6aa0")], sfx=[(0.1, "brillo", -20)])


@v.plano(74, "es el mismo circuito que se activa con el chocolate")
def _(d):
    return P(["#2a140a", "#0a0602"], [brillo(540, 1050, 500, "#ffb070", 0.3, 0.06), IMG("chocolate", ancho=460, x=540, y=1080, z=0.5, keys=aparece(0.3) + [{"t": d, "rot": -6}])],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[amarillo(0.5, d - 0.05, "CHOCOLATE", y=560, tam=120, color="#ffb070")], sfx=[(0.3, "pop", -18)])


@v.plano(84, "y con algunas drogas: señal de aviso roja")
def _(d):
    return P(["#2a0a0a", "#0a0202"], [brillo(540, 1000, 500, "#ff3d3d", 0.5, 0.06, pulso=[0.2, 0.4])], cam(1.0, 1.08, (540, 1000)), "corte",
             hud=[rotulo(0.05, d - 0.03, "DROGAS", tam=150, color="#ffffff", capsula="#c0392be6", y=1000)], sfx=[(0.05, "zap", -18)])


@v.plano(88, "por eso el amor engancha: un corazón colgado de un anzuelo")
def _(d):
    return P(ROSA, [IMG("anzuelo", ancho=320, x=540, y=760, z=0.5, keys=[{"t": 0, "rot": -6}, {"t": d * 0.5, "rot": 6}, {"t": d, "rot": -3}]),
                    IMG("corazon", ancho=300, x=600, y=1160, z=0.55, keys=[{"t": 0, "rot": -8, "y": 1100}, {"t": d * 0.5, "rot": 8, "y": 1170}, {"t": d, "rot": -4, "y": 1150}] + latido(0.2, d))],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[amarillo(0.3, d - 0.05, "ENGANCHA", y=1600 - 220, tam=130, color="#ff6aa0")], sfx=[(0.1, "pop", -18)])


@v.plano(93, "pero hay más: fogonazo")
def _(d):
    return P(OSC if False else ["#0a0a14", "#02020a"], [brillo(540, 1000, 600, "#ff3df2", 0.5, 0.06)], cam(1.0, 1.1, (540, 1000)), "corte",
             hud=[rotulo(0.05, d - 0.03, "HAY MÁS", tam=140, color="#ffffff", capsula="#c0397ae6", y=1000)], sfx=[(0.02, "impacto", -16)])


@v.plano(96, "en Italia, unos investigadores: el laboratorio")
def _(d):
    return P(LAB, [BG("bg_lab"), IMG("tubo_sangre", ancho=200, x=540, y=1100, z=0.5, keys=cae(0.0, 0.5, 700, 1100))], cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[rotulo(0.2, d - 0.05, "ITALIA", tam=120, color="#141414", capsula="#b8ff3ae6", y=560)], sfx=[(0.35, "golpe", -20)])


@v.plano(100, "midieron un marcador de la serotonina en la sangre")
def _(d):
    return P(LAB, [BG("bg_lab"), IMG("tubo_sangre", ancho=260, x=540, y=1050, z=0.5, keys=late(0.2, 1)), senala(540, 1180, 0.3, d - 0.1, 110, CIAN)],
             cam(1.1, 1.18, (540, 1050)), "corte", hud=[rotulo(0.3, d - 0.05, "SEROTONINA", tam=110, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(0.3, "senal", -22)])


@v.plano(109, "de veinte personas recién enamoradas: veinte corazones en cuadrícula")
def _(d):
    els = [brillo(540, 1050, 600, "#ff6aa0", 0.3, 0.06)]
    for i in range(20):
        x, y = 200 + (i % 5) * 170, 760 + (i // 5) * 170
        els.append(IMG("corazon_rosa", ancho=120, x=x, y=y, z=0.5, keys=aparece(0.05 + i * min(0.05, d * 0.6 / 20))))
    return P(ROSA, els, cam(1.0, 1.04, (540, 1050)), "corte", hud=[contador(0.05, d - 0.03, 1, 20, d * 0.6, "", y=560, tam=150, color="#ff6aa0")],
             sfx=[(0.05, "tictac", -24, {"dur": d * 0.6, "ritmo": 0.05})])


@v.plano(114, "sus valores se parecían a los de pacientes con trastorno obsesivo compulsivo: dos tubos iguales")
def _(d):
    return P(LAB, [BG("bg_lab"), IMG("tubo_sangre", ancho=220, x=320, y=1080, z=0.5, keys=aparece(0.0)), IMG("tubo_sangre", ancho=220, x=760, y=1080, z=0.5, keys=aparece(0.4)),
                   IMG("corazon_rosa", ancho=140, x=320, y=560 + 200, z=0.55, keys=aparece(0.2)), IMG("bucle", ancho=170, x=760, y=760, z=0.55, keys=aparece(0.6) + [{"t": d, "rot": 200}])],
             cam(1.0, 1.04, (540, 1000)), "corte", hud=[rotulo(0.8, d - 0.05, "=", tam=200, color="#ffffff", capsula=None, y=1080),
                                                       rotulo(1.2, d - 0.05, "COMO UN TOC", tam=100, color="#141414", capsula="#ffd23fe6", y=1500)], sfx=[(0.8, "ding", -20)])


@v.plano(126, "¿te suena no poder dejar de pensar en alguien?: la cara y el pensamiento que da vueltas")
def _(d):
    return P(ROSA, [IMG("cara_perfil", ancho=760, x=520, y=1150, z=0.45),
                    IMG("bucle", ancho=360, x=760, y=640, z=0.55, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 540, "ease": "lineal"}]),
                    IMG("foto_pareja", ancho=150, x=760, y=640, z=0.56, keys=aparece(0.2))],
             cam(1.0, 1.05, (560, 950)), "corte", hud=[amarillo(0.3, d - 0.05, "SIN PARAR", y=1600 - 250, tam=110, color="#ff6aa0")], sfx=[(0.1, "whoosh", -22, {"dur": 0.8})])


@v.plano(137, "la buena noticia: esa fase tan intensa no dura para siempre: el corazón se calma")
def _(d):
    return P(["#2a1a3a", "#0a0610"], [IMG("corazon_rosa", ancho=520, x=540, y=1050, z=0.5, keys=late(0.1, 2, 0.12, 0.5) + late(1.4, 2, 0.05, 1.0)), brillo(540, 1050, 500, "#ff9ab8", 0.3, 0.06)],
             cam(1.05, 1.0, (540, 1050)), "corte", hud=[rotulo(0.3, d - 0.05, "NO DURA PARA SIEMPRE", tam=80, color="#141414", capsula="#ff9ab8e6", y=560)], sfx=[(0.1, "brillo", -22)])


@v.plano(148, "lo que queda después ya es otra historia: la pareja al atardecer")
def _(d):
    return P(["#c0507a", "#3a1a3a"], [BG("bg_atardecer"), IMG("pareja", ancho=620, x=540, y=1400, z=0.5, keys=[{"t": 0, "y": 1440}, {"t": d, "y": 1400, "ease": "suave"}]), corazones(14, 4)],
             cam(1.0, 1.06, (540, 1200)), "desenfoque", hud=[amarillo(0.4, d - 0.4, "OTRA HISTORIA", y=560, tam=110, color="#ffd0e0")], sfx=[(0.1, "brillo", -20), (d * 0.6, "ding", -22)])


v.construir("2026-11-22-tarde-02-cerebro-enamorado", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 82, "db": -13},
            claves=["Enamorarte", "cerebro", "Fisher", "escáner", "enamoradas", "comían", "dormían", "foto", "pareja", "conocido", "profunda", "tegmental", "recompensa",
                    "dopamina", "placer", "chocolate", "drogas", "engancha", "Italia", "serotonina", "sangre", "veinte", "obsesivo", "pensar", "siempre", "historia"])
