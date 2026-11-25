"""02 · Por qué se te arrugan los dedos en el agua — método denso, estilo cartoon. Lote 2026-11-25-manana (Nico, con el agente).
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
from comun_1125m import *  # noqa: E402,F401,F403
import ilus_1125m  # noqa: E402

SVG = ilus_1125m.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
BAN = ["#cfeef4", "#8ccfe0"]
AGU = ["#5ad0f0", "#0a2a66"]


def burb(sem=1, n=26): return polvo("#e8f8ff", n, (40, 500, 1040, 1800), sem)


@v.plano(0, "gancho: la mano arrugada sale del agua chorreando")
def _(d):
    return P(BAN, [BG("bg_bano"), IMG("mano_arrugada", ancho=760, x=540, y=1150, z=0.5, keys=arranque(540, 1150, d, "abajo", 420, 40)), burb(2)],
             cam(1.0, 1.1, (540, 1050)), vineta=0.4, hud=[BANDA()], sfx=[(0.02, "agua", -16), (0.4, "pop", -20)])


@v.plano(4, "arrugados como pasas: la yema arrugada y una pasa que cae al lado")
def _(d):
    return P(BAN, [BG("bg_bano"), IMG("yema_arrugada", ancho=440, x=330, y=1180, z=0.5, keys=[{"t": 0, "escala": 0.94}, {"t": d, "escala": 1.04, "ease": "suave"}]),
                   IMG("pasa", ancho=400, x=800, y=1120, z=0.6, keys=cae(0.05, 0.5, 400, 1120))],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[BANDA(), rotulo(0.45, d - 0.03, "COMO PASAS", tam=96, color="#ffffff", capsula="#6a2a5ae6", y=620)], sfx=[(0.4, "golpe", -20)])


@v.plano(7, "seguro que crees que es porque la piel se hincha de agua: el agua entra en la yema (flechas)")
def _(d):
    return P(AGU, [BG("bg_bajo_agua"), burb(3), IMG("yema_lisa", ancho=460, x=540, y=1200, z=0.5, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.14, "ease": "suave"}]),
                   flecha([[120, 1000], [330, 1080]], 0.4, 0.9, "#e8f8ff", 10, z=0.6), flecha([[960, 1000], [750, 1080]], 0.7, 1.2, "#e8f8ff", 10, z=0.6),
                   flecha([[140, 1380], [320, 1300]], 1.0, 1.5, "#e8f8ff", 10, z=0.6), flecha([[940, 1380], [760, 1300]], 1.3, 1.8, "#e8f8ff", 10, z=0.6)],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[rotulo(d * 0.45, d - 0.03, "¿SE HINCHA?", tam=100, color="#141414", capsula="#ffffffe6", y=640)], sfx=[(0.4, "burbuja", -20), (1.0, "burbuja", -22)])


@v.plano(19, "pues no: la idea se tacha")
def _(d):
    return P(AGU, [BG("bg_bajo_agua"), IMG("yema_lisa", ancho=520, x=540, y=1200, z=0.5), *tacha(540, 1130, 0.05, 300)],
             cam(1.05, 1.12, (540, 1150), temblor=4), "corte", hud=[rotulo(0.02, d - 0.02, "NO", tam=170, color="#ffffff", capsula="#c0392be6", y=660)], sfx=[(0.05, "zap", -14)])


@v.plano(21, "lo hace tu cuerpo: la mano con los nervios encendidos")
def _(d):
    return P(OSC, [BG("bg_estudio"), brillo(540, 1100, 560, "#ffd23f", 0.35, 0.06, pulso=[0.2, 0.6]),
                   IMG("mano_nervio", ancho=700, x=540, y=1130, z=0.5, keys=arranque(540, 1130, d, "abajo", 200, 20))],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[rotulo(0.25, d - 0.03, "TU CUERPO", tam=110, color="#141414", capsula="#ffd23fe6", y=620)], sfx=[(0.1, "zap", -20)])


@v.plano(25, "a propósito: micro plano, la orden baja por el nervio")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("mano_nervio", ancho=700, x=540, y=1130, z=0.5),
                   flecha([[540, 1560], [540, 1340], [470, 1130], [465, 960]], 0.0, d * 0.8, LIMA, 12, z=0.7)],
             cam(1.1, 1.3, (540, 1250), (500, 1000)), "corte", hud=[amarillo(0.02, d - 0.02, "A PROPÓSITO", y=640, tam=100, color=LIMA)], sfx=[(0.02, "brillo", -20)])


@v.plano(27, "en los años treinta, unos médicos: el médico de época y el año")
def _(d):
    return P(["#3a2a1a", "#140c06"], [BG("bg_salon_1896"), IMG("profesor", ancho=300, x=330, y=1200, z=0.5, keys=va((260, 1200), (340, 1200), d)),
                                      IMG("lupa", ancho=260, x=740, y=1050, z=0.6, keys=[{"t": 0, "rot": -20, "x": 820}, {"t": d, "rot": 10, "x": 700, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1100)), "desenfoque",
             hud=[contador(0.05, d - 0.03, 1900, 1930, min(0.8, d * 0.5), miles=False, tam=150, color="#141414", capsula="#ffd27ae6", y=640)], sfx=[(0.1, "tic", -20)])


@v.plano(33, "vieron algo raro: la lupa sobre una mano")
def _(d):
    return P(["#3a2a1a", "#140c06"], [BG("bg_salon_1896"), IMG("mano", ancho=560, x=540, y=1200, z=0.5),
                                      IMG("lupa", ancho=420, x=540, y=1000, z=0.7, keys=[{"t": 0, "x": 250, "y": 900}, {"t": d, "x": 700, "y": 1150, "ease": "suave"}])],
             cam(1.0, 1.1, (540, 1100)), "corte", hud=[amarillo(0.1, d - 0.03, "ALGO RARO", y=640, tam=100, color=AMBAR)], sfx=[(0.1, "roce", -20)])


@v.plano(36, "a quien tenía dañado un nervio de la mano: el nervio se corta")
def _(d):
    return P(OSC, [BG("bg_estudio"), *cruza(IMG("mano_nervio", ancho=700, x=540, y=1130, z=0.5), IMG("mano_nervio_cortado", ancho=700, x=540, y=1130, z=0.5), d * 0.45, 0.12),
                   brillo(540, 1500, 260, "#ff3d3d", 0.6, 0.6, keys=[{"t": 0, "op": 0}, {"t": d * 0.45, "op": 0}, {"t": d * 0.5, "op": 1}, {"t": d, "op": 0.3}])],
             cam(1.0, 1.15, (540, 1150), (540, 1350), temblor=3), "corte", hud=[rotulo(d * 0.5, d - 0.03, "NERVIO DAÑADO", tam=84, color="#ffffff", capsula="#c0392be6", y=640)], sfx=[(d * 0.45, "golpe", -14)])


@v.plano(45, "esos dedos no se le arrugaban: la mano lisa dentro del agua, pasan los segundos y sigue lisa")
def _(d):
    return P(AGU, [BG("bg_bajo_agua"), burb(5), IMG("mano", ancho=640, x=540, y=1180, z=0.5, keys=flota(d, 16, x=540, y=1180, periodo=1.4))],
             cam(1.0, 1.06, (540, 1100)), "corte",
             hud=[contador(0.05, d - 0.03, 0, 30, d * 0.7, " min", tam=110, color="#141414", capsula="#ffffffe6", y=640)], sfx=[(0.1, "burbuja", -20), (d * 0.5, "burbuja", -22)])


@v.plano(51, "nunca: micro plano, la yema lisa enorme")
def _(d):
    return P(AGU, [BG("bg_bajo_agua"), IMG("yema_lisa", ancho=640, x=540, y=1250, z=0.5, keys=late(0.02, 1, 0.06, 0.3))],
             cam(1.0, 1.1, (540, 1150)), "corte", hud=[rotulo(0.02, d - 0.02, "NUNCA", tam=150, color="#ffffff", capsula="#c0392be6", y=660)], sfx=[(0.02, "impacto", -16)])


@v.plano(52, "porque es una orden: el cerebro manda la señal")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("cerebro", ancho=520, x=540, y=900, z=0.5, keys=late(0.1, 2, 0.07, 0.35)),
                   flecha([[540, 1150], [540, 1560]], 0.2, d * 0.8, AMBAR, 12, disc=[30, 18], z=0.6), brillo(540, 900, 460, "#ffd23f", 0.35, 0.06, pulso=[0.2, 0.5])],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[rotulo(0.15, d - 0.03, "ES UNA ORDEN", tam=90, color="#141414", capsula="#ffd23fe6", y=600)], sfx=[(0.1, "zap", -20)])


@v.plano(56, "tras unos minutos en el agua: la mano entra en el agua, los minutos corren")
def _(d):
    return P(AGU, [BG("bg_bajo_agua"), burb(7), IMG("mano", ancho=620, x=540, y=1200, z=0.5, rot=180, keys=[{"t": 0, "y": 300}, {"t": d * 0.5, "y": 1150, "ease": "salida"}, {"t": d, "y": 1190, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1100)), "corte",
             hud=[contador(d * 0.3, d - 0.03, 0, 5, d * 0.5, " min", tam=120, color="#141414", capsula="#ffffffe6", y=1300)], sfx=[(0.1, "agua", -18)])


@v.plano(62, "tus nervios estrechan los vasos de sangre de las yemas: la sección de la yema, los vasos se estrechan")
def _(d):
    return P(OSC, [BG("bg_estudio"), *cruza(IMG("yema_corte", ancho=640, x=540, y=1180, z=0.5), IMG("yema_corte_estrecho", ancho=640, x=540, y=1180, z=0.5), d * 0.55, 0.35),
                   senala(540, 1250, 0.3, d * 0.5, 190, AMBAR)],
             cam(1.0, 1.12, (540, 1150)), "corte",
             hud=[rotulo(0.15, d * 0.5, "VASOS DE SANGRE", tam=80, color="#ffffff", capsula="#c0392be6", y=600), rotulo(d * 0.6, d - 0.03, "SE ESTRECHAN", tam=90, color="#141414", capsula="#ffd23fe6", y=600)],
             sfx=[(0.3, "ding", -20), (d * 0.55, "roce", -16)])


@v.plano(72, "la yema pierde volumen: la yema se encoge (flechas hacia dentro)")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("yema_corte_estrecho", ancho=640, x=540, y=1180, z=0.5, keys=[{"t": 0, "escala": 1.1}, {"t": d, "escala": 0.94, "ease": "suave"}]),
                   flecha([[150, 1100], [300, 1100]], 0.1, 0.6, CIAN, 10, z=0.6), flecha([[930, 1100], [780, 1100]], 0.1, 0.6, CIAN, 10, z=0.6)],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[rotulo(0.1, d - 0.03, "MENOS VOLUMEN", tam=84, color="#141414", capsula="#7df9ffe6", y=600)], sfx=[(0.1, "roce", -20)])


@v.plano(76, "y la piel de encima se pliega: primer plano de la piel plegada, por fuera")
def _(d):
    return P(OSC, [BG("bg_estudio"), *cruza(IMG("yema_lisa", ancho=560, x=540, y=1220, z=0.5), IMG("yema_arrugada", ancho=560, x=540, y=1220, z=0.5), d * 0.3, 0.4)],
             cam(1.0, 1.25, (540, 1150), (540, 1000)), "corte", hud=[rotulo(d * 0.35, d - 0.03, "SE PLIEGA", tam=110, color="#141414", capsula="#ffd23fe6", y=600)], sfx=[(d * 0.3, "roce", -16)])


@v.plano(83, "¿y para qué?: la mano arrugada con interrogación")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("mano_arrugada", ancho=640, x=540, y=1180, z=0.5, keys=[{"t": 0, "rot": -6}, {"t": d, "rot": 6, "ease": "suave"}]), brillo(540, 1100, 500, "#7df9ff", 0.3, 0.06)],
             cam(1.0, 1.08, (540, 1100)), "corte", hud=[amarillo(0.03, d - 0.03, "¿PARA QUÉ?", y=640, tam=130, color=AMBAR)], sfx=[(0.03, "impacto", -18)])


@v.plano(86, "en dos mil trece, en la Universidad de Newcastle: laboratorio, el año corre")
def _(d):
    return P(LABC, [BG("bg_lab_claro"), IMG("mu_a", ancho=230, x=250, y=1200, z=0.5, keys=aparece(0.1)), IMG("mu_b", ancho=230, x=830, y=1200, z=0.5, keys=aparece(0.3)),
                    IMG("cubeta", ancho=360, x=540, y=1330, z=0.6, keys=cae(0.2, 0.6, 700, 1330))],
             cam(1.0, 1.05, (540, 1100)), "desenfoque",
             hud=[BANDA(), contador(0.05, d * 0.5, 2000, 2013, min(0.7, d * 0.3), miles=False, tam=150, color="#141414", capsula="#ffffffe6", y=640),
                  rotulo(d * 0.52, d - 0.03, "NEWCASTLE · 2013", tam=80, color="#ffffff", capsula="#2a5ae8e6", y=640)], sfx=[(0.5, "golpe", -20)])


@v.plano(95, "lo probaron: micro plano, la canica cae al agua")
def _(d):
    return P(LABC, [BG("bg_lab_claro"), IMG("cubeta", ancho=640, x=540, y=1300, z=0.5), IMG("canica", ancho=200, x=540, y=1100, z=0.6, keys=cae(0.0, 0.4, 500, 1260))],
             cam(1.1, 1.2, (540, 1200)), "corte", hud=[BANDA()], sfx=[(0.35, "agua", -16)])


@v.plano(97, "voluntarios pasando canicas mojadas de un recipiente a otro: las canicas viajan de una cubeta a otra")
def _(d):
    def can(n, t0):
        return IMG(n, ancho=150, x=260, y=1180, z=0.7, keys=[{"t": 0, "x": 260, "y": 1250, "op": 0}, {"t": t0, "x": 260, "y": 1250, "op": 1}, {"t": t0 + d * 0.14, "x": 540, "y": 820, "ease": "salida"},
                                                           {"t": t0 + d * 0.28, "x": 820, "y": 1250, "ease": "entrada"}, {"t": t0 + d * 0.3, "op": 0}])
    return P(LABC, [BG("bg_lab_claro"), IMG("cubeta", ancho=440, x=260, y=1330, z=0.5), IMG("cubeta_seca", ancho=440, x=820, y=1330, z=0.5),
                    can("canica", 0.05), can("canica_azul", d * 0.3), can("canica_roja", d * 0.6),
                    flecha([[300, 1000], [540, 800], [780, 1000]], 0.1, d * 0.5, "#2a5ae8", 9, disc=[26, 16], z=0.45)],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[BANDA(), rotulo(0.3, d - 0.03, "CANICAS MOJADAS", tam=80, color="#141414", capsula="#7dffb0e6", y=620)],
             sfx=[(0.05 + d * 0.28, "pop", -18), (d * 0.58, "pop", -18), (d * 0.88, "pop", -18)])


@v.plano(106, "con los dedos arrugados fueron un doce por ciento más rápidos: la mano arrugada coge la canica, la cifra")
def _(d):
    return P(LABC, [BG("bg_lab_claro"), IMG("mano_arrugada", ancho=520, x=360, y=1220, z=0.5, keys=va((300, 1260), (380, 1200), d)),
                    IMG("canica", ancho=190, x=700, y=980, z=0.6, keys=[{"t": 0, "x": 860, "y": 1300}, {"t": d * 0.5, "x": 600, "y": 900, "ease": "salida"}]),
                    *lineas_vel(600, 920, 3, "#2a5ae8aa")],
             cam(1.0, 1.06, (540, 1100)), "corte",
             hud=[BANDA(), contador(d * 0.35, d - 0.03, 0, 12, min(0.7, d * 0.3), " %", tam=170, color="#141414", capsula="#7dff3ae6", y=660, contar_prefijo="+")], sfx=[(d * 0.35, "subida", -22, {"dur": 0.6}), (d * 0.6, "ding", -16)])


@v.plano(117, "con canicas secas, ninguna diferencia: la canica seca y el signo igual")
def _(d):
    return P(LABC, [BG("bg_lab_claro"), IMG("mano", ancho=360, x=260, y=1220, z=0.5), IMG("mano_arrugada", ancho=360, x=820, y=1220, z=0.5),
                    IMG("canica_roja", ancho=170, x=540, y=900, z=0.6, keys=late(0.2, 2, 0.08, 0.4))],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[BANDA(), rotulo(0.3, d - 0.03, "SECAS: IGUAL", tam=96, color="#ffffff", capsula="#2a5ae8e6", y=640)], sfx=[(0.3, "pop", -20)])


@v.plano(122, "las arrugas funcionan como el dibujo de un neumático: la yema arrugada y el neumático rodando")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("yema_arrugada", ancho=380, x=280, y=1200, z=0.5, keys=aparece(0.0, 0.2)),
                   IMG("neumatico", ancho=560, x=760, y=1150, z=0.55, keys=[{"t": 0, "x": 1400, "rot": 0}, {"t": d * 0.45, "x": 760, "rot": -300, "ease": "salida"}, {"t": d, "rot": -360, "ease": "suave"}]),
                   flecha([[440, 1000], [560, 1000]], d * 0.5, d * 0.7, AMBAR, 10, z=0.6)],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[rotulo(d * 0.45, d - 0.03, "COMO UN NEUMÁTICO", tam=76, color="#141414", capsula="#ffd23fe6", y=620)], sfx=[(0.05, "rumor", -20, {"dur": d * 0.45})])


@v.plano(131, "sacan el agua: el agua corre por los canales del dibujo")
def _(d):
    return P(AGU, [BG("bg_bajo_agua"), IMG("banda_rodadura", ancho=820, x=540, y=1150, z=0.5, keys=va((540, 1050), (540, 1250), d, "lineal")),
                   flecha([[400, 820], [400, 1500]], 0.05, d * 0.7, "#e8f8ff", 10, z=0.7), flecha([[540, 820], [540, 1500]], 0.15, d * 0.8, "#e8f8ff", 10, z=0.7), flecha([[680, 820], [680, 1500]], 0.25, d * 0.9, "#e8f8ff", 10, z=0.7)],
             cam(1.0, 1.1, (540, 1150)), "corte", sfx=[(0.05, "agua", -16)])


@v.plano(134, "y agarran mejor: la mano arrugada atrapa una canica mojada")
def _(d):
    return P(AGU, [BG("bg_bajo_agua"), burb(9), IMG("mano_arrugada", ancho=640, x=540, y=1250, z=0.5, keys=[{"t": 0, "y": 1450}, {"t": d * 0.5, "y": 1230, "ease": "salida"}]),
                   IMG("canica_azul", ancho=190, x=540, y=820, z=0.6, keys=[{"t": 0, "y": 560}, {"t": d * 0.5, "y": 800, "ease": "entrada"}, {"t": d, "y": 810}])],
             cam(1.0, 1.08, (540, 1050)), "corte", sfx=[(d * 0.5, "ding", -16)])


@v.plano(137, "también pasa en los pies: el pie arrugado pisa un charco")
def _(d):
    return P(BAN, [BG("bg_bano"), IMG("pie", ancho=520, x=540, y=1150, z=0.5, keys=[{"t": 0, "y": 700, "rot": -8}, {"t": 0.4, "y": 1150, "rot": 0, "ease": "bote"}, {"t": d, "y": 1140}]), burb(4)],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[BANDA(), rotulo(0.4, d - 0.03, "Y EN LOS PIES", tam=90, color="#141414", capsula="#ffffffe6", y=620)], sfx=[(0.35, "agua", -14)])


@v.plano(142, "llevas ruedas de lluvia en las manos: la mano arrugada y el neumático, juntos bajo la lluvia")
def _(d):
    return P(OSC, [BG("bg_estudio"), polvo("#8ad0ff", 60, (0, 400, 1080, 1700), 3), IMG("neumatico", ancho=420, x=800, y=1250, z=0.45, anim={"girar": 3}),
                   IMG("mano_arrugada", ancho=560, x=380, y=1150, z=0.5, keys=late(0.3, 2, 0.05, 0.6))],
             cam(1.0, 1.08, (540, 1100)), "corte", hud=[rotulo(0.2, d - 0.03, "RUEDAS DE LLUVIA", tam=80, color="#141414", capsula="#7df9ffe6", y=620)], sfx=[(0.1, "agua", -20)])


@v.plano(149, "¿cuánto tardan en arrugarse los tuyos?: la mano lisa entra en el agua y la cuenta corre")
def _(d):
    return P(AGU, [BG("bg_bajo_agua"), burb(11), *cruza(IMG("mano", ancho=640, x=540, y=1180, z=0.5), IMG("mano_arrugada", ancho=640, x=540, y=1180, z=0.5), d * 0.6, 0.3)],
             cam(1.0, 1.08, (540, 1100)), "corte",
             hud=[contador(0.05, d - 0.03, 0, 5, d * 0.6, " min", tam=120, color="#141414", capsula="#ffffffe6", y=640)], sfx=[(0.1, "burbuja", -20)])


@v.plano(155, "pruébalo hoy: vuelve la mano arrugada saliendo del agua (bucle)")
def _(d):
    return P(BAN, [BG("bg_bano"), IMG("mano_arrugada", ancho=760, x=540, y=1150, z=0.5, keys=[{"t": 0, "y": 1400}, {"t": d, "y": 1150, "ease": "salida"}]), burb(2)],
             cam(1.0, 1.08, (540, 1050)), "corte", hud=[BANDA()], sfx=[(0.05, "agua", -18)])


# ---------------------------------------------------------------- micro planos (golpes de ≈0,5 s en la última palabra de la frase)
@v.plano(6, "micro: «pasas», la pasa en primer plano", mas=0.45)
def _(d):
    return P(BAN, [BG("bg_bano"), IMG("pasa", ancho=760, x=540, y=1100, z=0.5, keys=[{"t": 0, "escala": 0.85, "rot": -8}, {"t": d, "escala": 1.08, "rot": 4, "ease": "salida"}])],
             cam(1.05, 1.2, (540, 1100)), "corte", hud=[BANDA()], sfx=[(0.0, "pop", -22)])


@v.plano(24, "micro: «cuerpo», la chispa recorre el nervio de la palma", mas=0.5)
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("mano_nervio", ancho=700, x=540, y=1130, z=0.5), brillo(540, 1250, 300, "#ffd23f", 0.8, 0.6, keys=[{"t": 0, "y": 1500}, {"t": d, "y": 950, "ease": "lineal"}])],
             cam(1.5, 1.8, (540, 1300), (520, 1050)), "corte", sfx=[(0.0, "zap", -22)])


@v.plano(82, "micro: «pliega», las arrugas a pantalla completa", mas=0.3)
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("yema_arrugada", ancho=900, x=540, y=1500, z=0.5, keys=[{"t": 0, "y": 1560}, {"t": d, "y": 1460, "ease": "salida"}])],
             cam(1.1, 1.25, (540, 1050)), "corte", sfx=[(0.0, "roce", -20)])


@v.plano(116, "micro: «rápidos», la canica cruza con líneas de velocidad", mas=0.4)
def _(d):
    return P(LABC, [BG("bg_lab_claro"), IMG("canica", ancho=360, x=540, y=1050, z=0.5, keys=[{"t": 0, "x": 100}, {"t": d, "x": 900, "ease": "lineal"}]), *lineas_vel(400, 1050, 5, "#2a5ae8aa")],
             cam(1.1, 1.2, (540, 1050)), "corte", hud=[BANDA()], sfx=[(0.0, "whoosh", -22)])


@v.plano(136, "micro: «mejor», los dedos arrugados sujetan la canica", mas=0.26)
def _(d):
    return P(AGU, [BG("bg_bajo_agua"), IMG("mano_arrugada", ancho=900, x=540, y=1500, z=0.5), IMG("canica_azul", ancho=260, x=540, y=930, z=0.6, keys=late(0.0, 1, 0.1, 0.3))],
             cam(1.2, 1.35, (540, 1000)), "corte", sfx=[(0.0, "ding", -22)])


@v.plano(148, "micro: «manos», el dibujo del neumático en primer plano", mas=0.3)
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("neumatico", ancho=1100, x=700, y=1200, z=0.5, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": -40, "ease": "lineal"}]), polvo("#8ad0ff", 50, (0, 400, 1080, 1700), 5)],
             cam(1.1, 1.2, (540, 1100)), "corte", sfx=[(0.0, "agua", -22)])


v.construir("2026-11-25-manana-02-dedos-arrugados", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 252, "db": -13},
            claves=["dedos", "pasas", "hincha", "no.", "cuerpo.", "propósito.", "nervio", "Nunca.", "orden:", "vasos", "sangre", "volumen", "pliega.",
                    "Newcastle,", "canicas", "doce", "secas,", "neumático:", "agua", "pies.", "lluvia"])
