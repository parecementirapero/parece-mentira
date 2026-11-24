"""02 · Las lágrimas no caen (en el espacio) — método denso, estilo cartoon. Lote 2026-11-24-tarde (Agente 20:00 (Jorge)).
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
from comun_1124t import *  # noqa: E402,F401,F403
import ilus_1124t  # noqa: E402

SVG = ilus_1124t.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
MOD = ["#e8ecf4", "#b8c0d0"]
# la cara: lienzo 700x820; ojo izquierdo en (250, 400) del lienzo
CARA_W = 700


def cara(n="cara_astro", x=540, y=1050, ancho=760, keys=None, z=0.5): return IMG(n, ancho=ancho, x=x, y=y, z=z, keys=keys or [])


def ojo_en(x, y, ancho):
    """Posición en pantalla del ojo izquierdo de la cara colocada en (x, y) con ese ancho."""
    k = ancho / CARA_W
    return x + (250 - 350) * k, y + (400 - 410) * k


def bola(x, y, ancho, keys=None, z=0.6): return IMG("bola_agua", ancho=ancho, x=x, y=y, z=z, keys=keys or [])


@v.plano(0, "gancho: una bola de agua crece encima del ojo y no cae")
def _(d):
    ox, oy = ojo_en(540, 1050, 900)
    return P(MOD, [BG("bg_modulo"), cara(ancho=900, keys=arranque(540, 1050, d, "abajo", 220, 15)), bola(ox, oy, 230, keys=[{"t": 0, "escala": 0.55, "y": oy}, {"t": d, "escala": 1.1, "y": oy, "ease": "suave"}] + flota(d, 10, y=oy)[1:])],
             cam(1.0, 1.15, (540, 1000), (ox, oy)), vineta=0.45, hud=[BANDA()], sfx=[(0.05, "burbuja", -16), (0.6, "burbuja", -18)])


@v.plano(4, "al menos, en el espacio: la estación pasa sobre la Tierra")
def _(d):
    return P(ESP, [estrellas(80, 1), tierra(540, 1750, 1000, 0.4, giro=5), IMG("estacion", ancho=720, x=540, y=850, z=0.55, keys=[{"t": 0, "x": 300, "rot": -6}, {"t": d, "x": 760, "rot": 4, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1000)), "desenfoque", hud=[rotulo(0.3, d - 0.05, "EN EL ESPACIO", tam=100, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(0.1, "senal", -22)])


@v.plano(9, "en dos mil trece: el año corre dentro del módulo")
def _(d):
    return P(MOD, [BG("bg_modulo"), IMG("botella", ancho=170, x=850, y=1150, z=0.5, keys=flota(d, 20, y=1150) + [{"t": 0, "rot": 0}, {"t": d, "rot": 40}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[BANDA(), contador(0.05, d - 0.03, 2000, 2013, 0.5, miles=False, tam=180, color="#141414", capsula="#ffffffe6", x=470, y=1150)], sfx=[(0.1, "tic", -18)])


@v.plano(13, "el astronauta canadiense: un astronauta flota en el módulo")
def _(d):
    return P(MOD, [BG("bg_modulo"), IMG("astro_c0", ancho=380, x=540, y=1100, z=0.5, keys=flota(d, 30, y=1100) + [{"t": 0, "rot": -12}, {"t": d, "rot": 10, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[BANDA(), rotulo(0.3, d - 0.05, "ASTRONAUTA CANADIENSE", tam=72, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.1, "roce", -20)])


@v.plano(18, "lo probó en la Estación Espacial Internacional: la estación grande cruzando")
def _(d):
    return P(ESP, [estrellas(80, 2), IMG("tierra_arco", ancho=1080, x=540, y=1600, z=0.4),
                   IMG("estacion", ancho=980, x=540, y=900, z=0.55, keys=[{"t": 0, "x": 700}, {"t": d, "x": 380, "ease": "lineal"}])],
             cam(1.0, 1.08, (540, 950)), "corte", hud=[rotulo(0.4, d - 0.05, "ESTACIÓN ESPACIAL", tam=90, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "whoosh", -22)])


@v.plano(25, "se echó agua en el ojo: la botella suelta una gota que vuela al ojo")
def _(d):
    ox, oy = ojo_en(620, 1080, 700)
    return P(MOD, [BG("bg_modulo"), cara(x=620, y=1080, ancho=700), IMG("botella", ancho=170, x=200, y=900, z=0.6, keys=[{"t": 0, "rot": 60}, {"t": d, "rot": 50}]),
                   bola(260, 820, 70, keys=[{"t": 0, "x": 260, "y": 820, "op": 0}, {"t": 0.2, "op": 1}, {"t": d * 0.8, "x": ox, "y": oy, "ease": "suave"}]),
                   flecha([[260, 820], [ox - 60, oy - 30]], 0.2, d * 0.7, CIAN, 8, disc=[18, 14], z=0.55)],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[BANDA()], sfx=[(0.2, "burbuja", -16)])


@v.plano(31, "como si llorara: aparece una bolita en el ojo")
def _(d):
    ox, oy = ojo_en(540, 1080, 820)
    return P(MOD, [BG("bg_modulo"), cara(y=1080, ancho=820), bola(ox, oy, 110, keys=aparece(0.1) + late(0.6, 1, 0.08))],
             cam(1.0, 1.35, (540, 1050), (ox, oy)), "corte", hud=[BANDA()], sfx=[(0.1, "burbuja", -16)])


@v.plano(34, "y la lágrima no bajó por la mejilla: la lágrima amaga con bajar y la flecha se tacha")
def _(d):
    ox, oy = ojo_en(540, 1080, 820)
    return P(MOD, [BG("bg_modulo"), cara(y=1080, ancho=820), bola(ox, oy, 120, keys=[{"t": 0, "y": oy}, {"t": d * 0.3, "y": oy + 20, "ease": "suave"}, {"t": d * 0.6, "y": oy, "ease": "elastico"}]),
                   flecha([[ox - 90, oy + 80], [ox - 90, oy + 340]], 0.1, 0.5, "#ffffffcc", 12, z=0.65), *tacha(ox - 90, oy + 210, d * 0.5, 110)],
             cam(1.0, 1.1, (540, 1050)), "corte", hud=[BANDA()], sfx=[(d * 0.5, "zap", -18)])


@v.plano(42, "se quedó pegada al ojo: la bola tiembla pero se queda")
def _(d):
    ox, oy = ojo_en(540, 1080, 820)
    return P(MOD, [BG("bg_modulo"), cara(y=1080, ancho=820), bola(ox, oy, 140, keys=late(0.1, 3, 0.06, 0.35)), senala(ox, oy, 0.2, d - 0.05, 110, CIAN)],
             cam(1.3, 1.5, (ox, oy)), "corte", hud=[BANDA(), rotulo(0.3, d - 0.05, "PEGADA AL OJO", tam=96, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(0.2, "pop", -20)])


@v.plano(47, "cuanto más agua, más grande se hacía la bola: la bola crece")
def _(d):
    ox, oy = ojo_en(540, 1080, 820)
    return P(MOD, [BG("bg_modulo"), cara(y=1080, ancho=820), bola(ox, oy, 280, keys=[{"t": 0, "escala": 0.5}, {"t": d, "escala": 1.0, "ease": "suave"}]),
                   IMG("botella", ancho=150, x=180, y=780, z=0.6, keys=[{"t": 0, "rot": 55}, {"t": d, "rot": 70}])],
             cam(1.0, 1.1, (540, 1050)), "corte", hud=[BANDA()], sfx=[(0.1, "burbuja", -18), (0.6, "burbuja", -18), (1.1, "burbuja", -18)])


@v.plano(56, "hasta tapar el ojo entero: la bola cubre el ojo")
def _(d):
    ox, oy = ojo_en(540, 1080, 820)
    return P(MOD, [BG("bg_modulo"), cara(y=1080, ancho=820), bola(ox, oy, 340, keys=[{"t": 0, "escala": 0.85}, {"t": 0.4, "escala": 1.05, "ease": "golpe"}, {"t": d, "escala": 1.1}])],
             cam(1.1, 1.3, (540, 1050), (ox, oy)), "corte", hud=[BANDA(), rotulo(0.3, d - 0.05, "EL OJO ENTERO", tam=100, color="#ffffff", capsula="#2a5ae8e6", y=560)], sfx=[(0.3, "impacto", -16)])


@v.plano(61, "¿por qué?: fogonazo azul")
def _(d):
    return P(ESP, [estrellas(60, 3), bola(540, 1000, 300, keys=late(0.1, 2, 0.08, 0.4)), brillo(540, 1000, 500, "#7ad0ff", 0.5, 0.06)],
             cam(1.0, 1.08, (540, 1000)), "corte", hud=[amarillo(0.05, d - 0.03, "¿POR QUÉ?", y=560, tam=130, color=AMBAR)], sfx=[(0.05, "impacto", -18)])


@v.plano(63, "sin gravedad: en la Tierra la gota cae; arriba, flota")
def _(d):
    return P(OSC, [estrellas(60, 8), {"tipo": "forma", "forma": "rect", "ancho": 560, "alto": 2200, "relleno": "#8ac8ff", "x": 260, "y": 960, "z": 0.06},
                   IMG("bg_cielo_dia", ancho=560, x=260, y=1000, z=0.07),
                   IMG("lagrima", ancho=110, x=270, y=700, z=0.5, keys=[{"t": 0, "y": 650}, {"t": d * 0.8, "y": 1300, "ease": "entrada"}]),
                   IMG("lagrima", ancho=110, x=810, y=900, z=0.5, keys=flota(d, 25, y=900) + [{"t": 0, "rot": 0}, {"t": d, "rot": 60}])],
             cam(1.0, 1.03, (540, 960)), "corte", hud=[rotulo(0.2, d - 0.05, "TIERRA", tam=70, color="#141414", capsula="#ffffffe6", x=270, y=1360),
                                                        rotulo(0.2, d - 0.05, "ESPACIO", tam=70, color="#141414", capsula="#7df9ffe6", x=760, y=1360)], sfx=[(0.1, "roce", -20)])


@v.plano(65, "nada tira de la gota hacia abajo: la flecha de la gravedad se apaga")
def _(d):
    return P(ESP, [estrellas(60, 4), IMG("lagrima", ancho=200, x=540, y=850, z=0.5, keys=flota(d, 20, y=850)),
                   flecha([[540, 1050], [540, 1400]], 0.1, 0.5, "#ff3d3d", 16, z=0.55), *tacha(540, 1230, d * 0.5, 120)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[rotulo(0.3, d - 0.05, "NADA TIRA", tam=110, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(d * 0.5, "zap", -18)])


@v.plano(72, "lo que manda es la tensión superficial: la bola con su piel brillante")
def _(d):
    return P(ESP, [estrellas(60, 5), bola(540, 1000, 560, keys=[{"t": 0, "ex": 1.0, "ey": 1.0}, {"t": d * 0.3, "ex": 1.05, "ey": 0.95, "ease": "suave"}, {"t": d * 0.6, "ex": 0.97, "ey": 1.03, "ease": "suave"}, {"t": d, "ex": 1.0, "ey": 1.0}]),
                   senala(540, 1000, 0.3, d - 0.05, 300, CIAN)],
             cam(1.0, 1.06, (540, 1000)), "corte", sfx=[(0.3, "brillo", -18)])


@v.plano(79, "el agua se agarra a sí misma: las moléculas se juntan")
def _(d):
    pos = [(300, 800), (780, 820), (320, 1250), (770, 1240), (540, 1030)]
    els = [IMG("molecula_agua", ancho=280, x=x, y=y, z=0.5, keys=[{"t": 0, "x": x + (x - 540) * 0.6, "y": y + (y - 1030) * 0.6}, {"t": d * 0.7, "x": 540 + (x - 540) * 0.5, "y": 1030 + (y - 1030) * 0.5, "ease": "salida"}])
           for x, y in pos]
    return P(ESP, [estrellas(60, 6), brillo(540, 1030, 400, "#7ad0ff", 0.3, 0.06), *els], cam(1.0, 1.05, (540, 1030)), "corte",
             hud=[amarillo(0.3, d - 0.05, "SE AGARRA", y=560, tam=120, color=CIAN)], sfx=[(d * 0.6, "pop", -18)])


@v.plano(86, "y a todo lo que toca: la bola se pega a la botella")
def _(d):
    return P(MOD, [BG("bg_modulo"), IMG("botella", ancho=260, x=540, y=1100, z=0.5, keys=flota(d, 15, y=1100)),
                   bola(540, 820, 200, keys=[{"t": 0, "x": 850, "y": 700}, {"t": d * 0.6, "x": 600, "y": 860, "ease": "salida"}, {"t": d, "x": 600, "y": 860}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[BANDA()], sfx=[(d * 0.6, "burbuja", -16)])


@v.plano(92, "por eso, allí arriba: la estación en órbita")
def _(d):
    return P(ESP, [estrellas(80, 7), tierra(540, 1800, 1100, 0.4, giro=4), IMG("estacion", ancho=600, x=540, y=800, z=0.55, keys=flota(d, 15, y=800))],
             cam(1.0, 1.05, (540, 1000)), "corte", sfx=[(0.1, "senal", -24)])


@v.plano(96, "las lágrimas se quitan con una toalla: la toalla barre la bola del ojo")
def _(d):
    ox, oy = ojo_en(540, 1080, 820)
    return P(MOD, [BG("bg_modulo"), cara(y=1080, ancho=820), bola(ox, oy, 200, keys=[{"t": 0, "op": 1}, {"t": d * 0.5, "op": 0}]),
                   IMG("toalla", ancho=360, x=ox, y=oy, z=0.7, keys=[{"t": 0, "x": -250, "rot": -20}, {"t": d * 0.5, "x": ox + 60, "rot": 0, "ease": "salida"}, {"t": d, "x": 1300, "rot": 15, "ease": "entrada"}])],
             cam(1.0, 1.08, (540, 1050)), "corte", hud=[BANDA(), rotulo(0.3, d - 0.05, "CON TOALLA", tam=100, color="#141414", capsula="#ff9a3ae6", y=560)], sfx=[(d * 0.4, "roce", -16)])


@v.plano(103, "y no es lo único raro: el astronauta da una vuelta")
def _(d):
    return P(MOD, [BG("bg_modulo"), IMG("astro_c1", ancho=360, x=540, y=1100, z=0.5, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 160, "ease": "suave"}] + flota(d, 25, y=1100))],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[BANDA(), rotulo(0.2, d - 0.05, "Y HAY MÁS", tam=110, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.1, "whoosh", -22)])


@v.plano(109, "los líquidos del cuerpo también suben hacia la cabeza: flechas azules suben por el cuerpo")
def _(d):
    fl = [flecha([[x, 1500], [x, 800]], 0.2 + k * 0.2, 0.9 + k * 0.2, CIAN, 12, z=0.6) for k, x in enumerate((440, 540, 640))]
    return P(OSC, [BG("bg_estudio"), IMG("cuerpo_flujo", ancho=380, x=540, y=1050, z=0.5), *fl, brillo(540, 700, 200, "#7ad0ff", 0.0, 0.55, keys=[{"t": 0.8, "op": 0}, {"t": 1.3, "op": 1}])],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[rotulo(0.4, d - 0.05, "SUBEN A LA CABEZA", tam=80, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(0.2, "subida", -22, {"dur": 1.0})])


@v.plano(118, "la cara se hincha: la cara normal pasa a hinchada")
def _(d):
    return P(MOD, [BG("bg_modulo"), cara(y=1080, ancho=820, keys=[{"t": 0, "op": 1}, {"t": d * 0.5, "op": 0}]), cara("cara_hinchada", y=1080, ancho=820, z=0.51, keys=[{"t": 0, "op": 0}, {"t": d * 0.5, "op": 1, "escala": 1.0}, {"t": d, "escala": 1.04}])],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[BANDA()], sfx=[(d * 0.45, "pop", -18)])


@v.plano(122, "las piernas adelgazan: las piernas se afinan")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("cuerpo_flujo", ancho=380, x=540, y=1050, z=0.5, keys=[{"t": 0, "op": 1}, {"t": d * 0.5, "op": 0}]),
                   IMG("cuerpo_espacio", ancho=380, x=540, y=1050, z=0.51, keys=[{"t": 0, "op": 0}, {"t": d * 0.5, "op": 1}]), senala(540, 1250, 0.4, d - 0.05, 120, AMBAR)],
             cam(1.0, 1.15, (540, 1050), (540, 1200)), "corte", hud=[rotulo(0.3, d - 0.05, "PIERNAS FINAS", tam=96, color="#141414", capsula="#ffe93de6", y=560)], sfx=[(d * 0.45, "pop", -18)])


@v.plano(126, "y la nariz se tapa, como si tuvieras un resfriado: el pañuelo flota hacia la nariz")
def _(d):
    return P(MOD, [BG("bg_modulo"), cara("cara_hinchada", y=1080, ancho=820, keys=late(d * 0.6, 1, 0.04)),
                   IMG("panuelo", ancho=280, x=540, y=1180, z=0.6, keys=[{"t": 0, "x": 1000, "y": 800, "rot": 30}, {"t": d * 0.6, "x": 600, "y": 1150, "rot": -8, "ease": "salida"}, {"t": d, "x": 590, "y": 1160}])],
             cam(1.0, 1.08, (540, 1050)), "corte", hud=[BANDA(), rotulo(0.3, d - 0.05, "NARIZ TAPADA", tam=96, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.2, "roce", -20)])


@v.plano(135, "así que en el espacio puedes estar triste: el astronauta junto a la ventana con la Tierra")
def _(d):
    return P(MOD, [BG("bg_modulo"), IMG("astro_c0", ancho=320, x=760, y=1150, z=0.5, keys=flota(d, 20, y=1150) + [{"t": 0, "rot": -15}, {"t": d, "rot": -5}])],
             cam(1.0, 1.08, (540, 1000), (640, 900)), "corte", hud=[BANDA()], sfx=[(0.1, "roce", -22)])


@v.plano(143, "pero llorar es otra historia: la bola vuelve al ojo")
def _(d):
    ox, oy = ojo_en(540, 1050, 900)
    return P(MOD, [BG("bg_modulo"), cara(ancho=900), bola(ox, oy, 230, keys=[{"t": 0, "escala": 0.4}, {"t": d, "escala": 1.0, "ease": "suave"}])],
             cam(1.0, 1.12, (540, 1000), (ox, oy)), "corte", hud=[BANDA()], sfx=[(0.1, "burbuja", -18)])


@v.plano(148, "¿te atreverías a vivir allí arriba?: la estación sobre el amanecer en la Tierra")
def _(d):
    return P(ESP, [BG("bg_amanecer_orbital"), IMG("estacion", ancho=640, x=540, y=820, z=0.55, keys=[{"t": 0, "x": 460}, {"t": d, "x": 620, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[amarillo(0.3, d - 0.05, "¿TE ATREVES?", y=1250, tam=110, color=AMBAR)], sfx=[(0.1, "brillo", -20)])


def _micro_bola(d, ancho=520, txt=None, col=CIAN):
    return P(ESP, [estrellas(50, 9), bola(540, 1000, ancho, keys=[{"t": 0, "escala": 0.8}, {"t": d, "escala": 1.1, "ease": "salida"}]), brillo(540, 1000, 380, "#7ad0ff", 0.5, 0.06)],
             cam(1.1, 1.25, (540, 1000)), "corte", hud=[amarillo(0.02, d - 0.02, txt, y=1400, tam=130, color=col)] if txt else [], sfx=[(0.02, "burbuja", -16)])


@v.plano(37, "micro: «NO» en rojo sobre la lágrima")
def _(d):
    return P(OSC, [IMG("lagrima", ancho=260, x=540, y=1000, z=0.5, keys=[{"t": 0, "escala": 1.2}, {"t": d, "escala": 1.0}]), *tacha(540, 1000, 0.02, 160)],
             cam(1.0, 1.1, (540, 1000)), "corte", sfx=[(0.02, "zap", -16)])


@v.plano(37, "no bajó: la cara otra vez, la bola quieta en el ojo", mas=0.45)
def _(d):
    ox, oy = ojo_en(540, 1080, 820)
    return P(MOD, [BG("bg_modulo"), cara(y=1080, ancho=820), bola(ox, oy, 120, keys=late(0.1, 2, 0.06, 0.4))], cam(1.15, 1.25, (540, 1000), (ox, oy)), "corte", hud=[BANDA()], sfx=[(0.1, "pop", -22)])


@v.plano(55, "micro: la bola en grande", mas=0.0)
def _(d):
    return _micro_bola(d, 560)


@v.plano(77, "micro: la piel de la bola tiembla")
def _(d):
    return _micro_bola(d, 760)


@v.plano(77, "tensión superficial (sigue): la bola con el anillo", mas=0.45)
def _(d):
    return P(ESP, [estrellas(60, 5), bola(540, 1000, 560, keys=[{"t": 0, "ex": 1.03, "ey": 0.97}, {"t": d, "ex": 1.0, "ey": 1.0, "ease": "elastico"}]), senala(540, 1000, 0.05, d - 0.05, 300, CIAN)],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[rotulo(0.02, d - 0.05, "TENSIÓN", tam=120, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[])


@v.plano(121, "micro: la cara hinchada de golpe")
def _(d):
    return P(MOD, [BG("bg_modulo"), cara("cara_hinchada", y=1100, ancho=900, keys=[{"t": 0, "escala": 1.15}, {"t": d, "escala": 1.0, "ease": "golpe"}])],
             cam(1.2, 1.3, (540, 1000)), "corte", hud=[BANDA()], sfx=[(0.02, "pop", -16)])


v.construir("2026-11-24-tarde-02-lagrimas-espacio", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 224, "db": -13},
            claves=["lágrimas", "caen", "espacio", "Hadfield", "Estación", "ojo", "mejilla", "bola", "gravedad", "tensión", "superficial",
                    "toalla", "cabeza", "hincha", "piernas", "nariz", "resfriado", "llorar"])
