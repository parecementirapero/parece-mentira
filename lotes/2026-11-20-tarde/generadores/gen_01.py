"""01 · Dieciséis amaneceres al día (Estación Espacial Internacional) — método denso. Lote 2026-11-20-tarde (Agente 20:00, Jorge).
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import math, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_1120t  # noqa: E402

SVG = ilus_1120t.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

OSC = ["#01020a", "#0a1030"]


def iss(ancho=760, x=540, y=900, z=0.55, keys=None, **k):
    return IMG("iss", ancho=ancho, x=x, y=y, z=z, keys=keys or [], **k)


def alba(n="bg_amanecer_orbital"): return BG(n)


def orbita_keys(d, cx=540, cy=1050, r=470, a0=200, a1=340, pasos=8, esc=(0.3, 0.3)):
    """La estación dando la vuelta alrededor de la Tierra (claves sobre un círculo)."""
    ks = []
    for i in range(pasos + 1):
        u = i / pasos; a = math.radians(a0 + (a1 - a0) * u)
        ks.append({"t": round(d * u, 3), "x": cx + r * math.cos(a), "y": cy + r * math.sin(a), "rot": (a0 + (a1 - a0) * u) + 90, "escala": esc[0], "ease": "lineal"})
    return ks


def circulo(cx, cy, r, a0=0, a1=360, n=40):
    return [[cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))] for i in range(n + 1)]


# ================================================================== PLANOS
@v.plano(0, "gancho: el Sol revienta por el borde de la Tierra y la Estación cruza delante")
def _(d):
    return P(OSC, [alba("bg_amanecer_orbital2"), iss(ancho=700, keys=arranque(560, 1080, d, "derecha", 420, 160)),
                   brillo(720, 700, 520, "#ffc070", 0.6, 0.07, keys=[{"t": 0, "op": 0.4}, {"t": d, "op": 1}])],
             cam(1.0, 1.08, (600, 900)), vineta=0.5, sfx=[(0.02, "subida", -16, {"dur": 1.2}), (0.6, "brillo", -18)])


@v.plano(4, "los ven en la Estación Espacial: la Estación grande sobre la Tierra")
def _(d):
    return P(OSC, [BG("bg_orbita"), iss(ancho=980, y=820, keys=[{"t": 0, "x": 600, "rot": -3}, {"t": d, "x": 500, "rot": 2, "ease": "suave"}])],
             cam(1.0, 1.08, (540, 900)), "desenfoque", sfx=[(0.1, "whoosh", -20)])


@v.plano(10, "da vueltas a la Tierra: la Tierra gira y la Estación la rodea")
def _(d):
    return P(OSC, [estrellas(60, 2), tierra(540, 1050, 760, 0.4, giro=10), iss(keys=orbita_keys(d, a0=180, a1=330), z=0.6),
                   flecha(circulo(540, 1050, 470, 180, 330), 0.0, d, CIAN, 6, z=0.5)],
             cam(1.0, 1.05, (540, 1000)), "corte", sfx=[(0.05, "whoosh", -22, {"dur": 0.8})])


@v.plano(15, "a cuatrocientos veinte kilómetros: flecha desde el suelo hasta la Estación")
def _(d):
    return P(OSC, [BG("bg_orbita"), iss(ancho=420, x=540, y=620, keys=late(0.2, 1)), flecha([[540, 1560], [540, 760]], 0.05, d * 0.6, LIMA, 10, z=0.6)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[contador(0.05, d - 0.03, 0, 420, d * 0.6, " KM", y=1150, tam=130, color=LIMA, capsula="#000000a0")],
             sfx=[(0.05, "subida", -20, {"dur": min(1.0, d)})])


@v.plano(22, "y va rapidísimo: la Estación cruza la pantalla con líneas de velocidad")
def _(d):
    return P(OSC, [BG("bg_orbita"), iss(ancho=620, y=900, keys=[{"t": 0, "x": -200}, {"t": d, "x": 1250, "ease": "lineal"}]), *lineas_vel(420, 900, 3)],
             cam(1.0, 1.04, (540, 900)), "corte", sfx=[(0.05, "whoosh", -16, {"dur": 0.6})])


@v.plano(25, "veintiocho mil kilómetros por hora: el velocímetro se dispara")
def _(d):
    return P(["#0a1a2a", "#020610"], [BG("bg_estudio"), IMG("velocimetro", ancho=900, x=540, y=1100, z=0.5),
                                      IMG("aguja_vel", ancho=900, x=540, y=1100, z=0.55, keys=[{"t": 0, "rot": -80}, {"t": d * 0.7, "rot": 80, "ease": "salida"}, {"t": d, "rot": 76}])],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[contador(0.05, d - 0.03, 0, 28000, d * 0.7, " KM/H", y=1450, tam=110, color="#ffd23f")],
             sfx=[(0.05, "subida", -18, {"dur": d * 0.7})])


@v.plano(31, "unos ocho kilómetros cada segundo: el cronómetro marca un segundo")
def _(d):
    return P(OSC, [estrellas(40, 4), *cronometro(0, 6, 0.05, d)], cam(1.0, 1.05, (540, 1040)), "corte",
             hud=[contador(0.1, d - 0.03, 0, 8, d * 0.6, " KM", y=1390, tam=130, color=CIAN), rotulo(0.3, d - 0.05, "CADA SEGUNDO", tam=80, color="#141414", capsula="#7df9ffe6", y=560)],
             sfx=[(0.05, "tictac", -20, {"dur": min(1.0, d), "ritmo": 0.25})])


@v.plano(36, "¿y por qué tantos amaneceres?: el Sol asoma otra vez")
def _(d):
    return P(OSC, [alba(), brillo(720, 700, 400, "#ffd08a", 0.5, 0.07, pulso=[0.1, 1.2])],
             cam(1.05, 1.12, (700, 800)), "corte", hud=[amarillo(0.1, d - 0.05, "¿POR QUÉ?", y=1250, tam=130, color=AMBAR)], sfx=[(0.1, "roce", -20)])


@v.plano(41, "porque a esa velocidad rodea el planeta entero: vuelta completa con trazo")
def _(d):
    return P(OSC, [estrellas(60, 5), tierra(540, 1050, 700, 0.4, giro=14), iss(keys=orbita_keys(d, a0=-90, a1=270, pasos=16), z=0.6),
                   flecha(circulo(540, 1050, 470, -90, 270, 60), 0.0, d, MAGENTA, 7, z=0.5)],
             cam(1.0, 1.04, (540, 1050)), "corte", sfx=[(0.05, "whoosh", -20, {"dur": d})])


@v.plano(49, "en unos noventa minutos: el reloj avanza hora y media")
def _(d):
    return P(OSC, [estrellas(40, 6), *reloj(540, 1050, 640, 12, 0, 1, 30, 0.05, d)], cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[contador(0.05, d - 0.03, 0, 90, d * 0.7, " MIN", y=560, tam=130, color="#ffd23f")], sfx=[(0.05, "tictac", -20, {"dur": min(1.2, d), "ritmo": 0.1})])


@v.plano(53, "en cada vuelta pasa la mitad del tiempo al sol: Sol a la izquierda, Estación iluminada")
def _(d):
    return P(OSC, [estrellas(40, 7), *sol(160, 760, 120, 0.3), tierra(620, 1150, 640, 0.4, giro=6),
                   iss(ancho=300, keys=[{"t": 0, "x": 300, "y": 1100}, {"t": d, "x": 420, "y": 780, "ease": "suave"}], z=0.6)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[amarillo(0.1, d - 0.05, "AL SOL", y=560, tam=120, color="#ffd23f")], sfx=[(0.1, "brillo", -20)])


@v.plano(63, "y la otra mitad a oscuras: la Tierra de noche con ciudades")
def _(d):
    return P(OSC, [BG("bg_noche"), iss(ancho=500, y=760, keys=[{"t": 0, "x": 300, "op": 0.8}, {"t": d, "x": 760, "ease": "lineal"}])],
             cam(1.0, 1.06, (540, 1100)), "desenfoque", hud=[amarillo(0.1, d - 0.05, "A OSCURAS", y=560, tam=110, color=CIAN)], sfx=[(0.1, "roce", -22)])


@v.plano(69, "un amanecer o un atardecer: el Sol sube por el borde y se apaga")
def _(d):
    return P(OSC, [alba(), brillo(720, 700, 520, "#ffc070", 0.7, 0.07, keys=[{"t": 0, "op": 0.2}, {"t": d * 0.5, "op": 1}, {"t": d, "op": 0.3}])],
             cam(1.1, 1.2, (720, 760)), "corte", sfx=[(0.05, "subida", -20, {"dur": d * 0.5})])


@v.plano(74, "cada cuarenta y cinco minutos: cronómetro media vuelta")
def _(d):
    return P(OSC, [estrellas(40, 8), *cronometro(0, 270, 0.05, d)], cam(1.0, 1.05, (540, 1040)), "corte",
             hud=[contador(0.05, d - 0.03, 0, 45, d * 0.7, " MIN", y=560, tam=130, color=MAGENTA)], sfx=[(0.05, "tictac", -20, {"dur": min(1.0, d), "ritmo": 0.1})])


@v.plano(81, "dieciséis veces: dieciséis soles se encienden en cuadrícula")
def _(d):
    els = [estrellas(40, 9)]
    for i in range(16):
        x, y = 240 + (i % 4) * 200, 760 + (i // 4) * 200
        t = 0.05 + i * min(0.09, (d * 0.8) / 16)
        els.append(brillo(x, y, 80, "#ffc070", 0.9, 0.5, keys=[{"t": 0, "op": 0}, {"t": t, "op": 1}]))
        els.append({"tipo": "forma", "forma": "circulo", "radio": 26, "relleno": "#fff6d0", "x": x, "y": y, "z": 0.55, "keys": [{"t": 0, "escala": 0, "op": 0}, {"t": t, "escala": 1, "op": 1, "ease": "golpe"}]})
    return P(OSC, els, cam(1.0, 1.04, (540, 1060)), "corte", hud=[contador(0.05, d - 0.03, 1, 16, d * 0.8, "", y=560, tam=140, color="#ffd23f")],
             sfx=[(0.05, "tictac", -22, {"dur": d * 0.8, "ritmo": 0.09})])


@v.plano(84, "cada veinticuatro horas: el despertador da un día entero")
def _(d):
    return P(OSC, [estrellas(40, 10), IMG("despertador", ancho=560, x=540, y=1050, z=0.5, keys=late(0.1, 2, 0.08, 0.25))], cam(1.0, 1.06, (540, 1050)), "corte",
             hud=[contador(0.05, d - 0.03, 0, 24, d * 0.7, " H", y=560, tam=130, color=LIMA)], sfx=[(0.1, "ding", -20)])


@v.plano(86, "en un solo día recorre: la Tierra abajo, el trazo empieza a subir")
def _(d):
    return P(OSC, [estrellas(70, 11), tierra(540, 1650, 520, 0.4, giro=6), flecha([[480, 1400], [400, 1000], [420, 700]], 0.05, d, CIAN, 8, disc=[26, 18], z=0.5)],
             cam(1.0, 1.04, (540, 1200)), "corte", sfx=[(0.05, "whoosh", -22)])


@v.plano(90, "lo mismo que ir a la Luna y volver: ida y vuelta entre la Tierra y la Luna")
def _(d):
    return P(OSC, [estrellas(70, 11), tierra(540, 1650, 520, 0.4, giro=6), luna(560, 560, 300, 0.4, keys=late(d * 0.5, 1)),
                   flecha([[480, 1400], [390, 1000], [470, 720]], 0.0, d * 0.45, CIAN, 8, disc=[26, 18], z=0.5),
                   flecha([[640, 720], [700, 1000], [610, 1400]], d * 0.5, d * 0.95, MAGENTA, 8, disc=[26, 18], z=0.5)],
             cam(1.0, 1.03, (540, 1100)), "corte", hud=[rotulo(0.2, d - 0.05, "IDA Y VUELTA", tam=90, color="#141414", capsula="#ffd23fe6", y=1100)],
             sfx=[(d * 0.45, "pop", -20)])


@v.plano(100, "entonces, ¿qué hora es ahí arriba?: la ventanilla con la Tierra")
def _(d):
    return P(OSC, [estrellas(50, 12), IMG("ventanilla", ancho=860, x=540, y=1050, z=0.5, keys=[{"t": 0, "rot": -4, "escala": 0.95}, {"t": d, "rot": 3, "escala": 1.0, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1050)), "desenfoque", hud=[amarillo(0.3, d - 0.05, "¿QUÉ HORA?", y=560, tam=120, color=CIAN)], sfx=[(0.1, "roce", -20)])


@v.plano(106, "para no volverse locos, usan la hora: el despertador tiembla y da vueltas")
def _(d):
    return P(["#1a0a2a", "#06020e"], [brillo(540, 1050, 600, "#ff3df2", 0.3, 0.06),
                                     IMG("despertador", ancho=520, x=540, y=1050, z=0.5, keys=[{"t": 0, "rot": -12}, {"t": d * 0.25, "rot": 12}, {"t": d * 0.5, "rot": -12}, {"t": d * 0.75, "rot": 12}, {"t": d, "rot": 0}])],
             cam(1.0, 1.08, (540, 1050), temblor=4), "corte", sfx=[(0.05, "ding", -18), (d * 0.5, "ding", -20)])


@v.plano(115, "la de Londres: torre de reloj junto al río")
def _(d):
    return P(OSC, [BG("bg_londres_noche"), IMG("torre_reloj", ancho=440, x=540, y=1040, z=0.5, keys=aparece(0.0)),
                   IMG("manecillas", ancho=170, x=540, y=731, z=0.56, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 90, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 900)), "corte", hud=[rotulo(0.3, d - 0.05, "LONDRES", tam=100, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.2, "ding", -18)])


@v.plano(118, "la estación mide casi lo mismo: la Estación entera, enorme")
def _(d):
    return P(OSC, [BG("bg_orbita"), iss(ancho=1250, y=900, keys=[{"t": 0, "escala": 0.85}, {"t": d, "escala": 1.0, "ease": "suave"}])],
             cam(1.0, 1.04, (540, 900)), "corte", sfx=[(0.1, "whoosh", -20)])


@v.plano(125, "que un campo de fútbol americano: la Estación encima del campo, casi igual de larga")
def _(d):
    return P(["#0a2a1a", "#02100a"], [IMG("campo_futbol", ancho=560, x=540, y=1080, z=0.4, keys=aparece(0.0)),
                                      iss(ancho=1120, x=540, y=1080, z=0.55, rot=90, op=0.92, keys=[{"t": 0, "y": 600, "op": 0}, {"t": 0.5, "y": 1080, "op": 0.92, "ease": "salida"}])],
             cam(1.0, 1.03, (540, 1080)), "corte", hud=[rotulo(0.6, d - 0.05, "≈ 109 M", tam=96, color="#141414", capsula="#b8ff3ae6", y=560)], sfx=[(0.5, "golpe", -18)])


@v.plano(130, "y lleva habitada sin parar: el casco con la Tierra reflejada")
def _(d):
    return P(OSC, [estrellas(50, 13), IMG("casco", ancho=760, x=540, y=1050, z=0.5, keys=[{"t": 0, "rot": -3, "escala": 0.96}, {"t": d, "rot": 3, "escala": 1.02, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[amarillo(0.2, d - 0.05, "SIN PARAR", y=560, tam=120, color=LIMA)], sfx=[(0.1, "brillo", -20)])


@v.plano(135, "desde noviembre del año dos mil: el calendario y el año que corre")
def _(d):
    return P(["#0a1a2a", "#020610"], [BG("bg_estudio"), IMG("calendario", ancho=600, x=540, y=1100, z=0.5, keys=aparece(0.0))],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[contador(0.05, d - 0.03, 1990, 2000, d * 0.6, "", y=560, tam=150, color="#ffd23f", miles=False)],
             sfx=[(0.05, "tictac", -22, {"dur": d * 0.6, "ritmo": 0.08})])


@v.plano(141, "ahora mismo, alguien está viendo amanecer desde allí: el casco ante el Sol que sale")
def _(d):
    return P(OSC, [alba(), IMG("casco", ancho=620, x=540, y=1350, z=0.5, keys=[{"t": 0, "y": 1450}, {"t": d, "y": 1330, "ease": "suave"}]),
                   brillo(720, 700, 500, "#ffc070", 0.6, 0.07, keys=[{"t": 0, "op": 0.3}, {"t": d, "op": 1}])],
             cam(1.0, 1.08, (600, 1000)), "desenfoque", sfx=[(0.1, "subida", -20, {"dur": d})])


@v.plano(149, "y dentro de noventa minutos, otra vez: la Estación vuelve a cruzar el amanecer (bucle)")
def _(d):
    return P(OSC, [alba("bg_amanecer_orbital2"), iss(ancho=700, keys=[{"t": 0, "x": 1300, "y": 1050}, {"t": d, "x": 600, "y": 1080, "ease": "salida"}]),
                   brillo(720, 700, 520, "#ffc070", 0.6, 0.07)],
             cam(1.0, 1.06, (600, 900)), "corte", hud=[contador(0.2, d - 0.3, 0, 90, d * 0.5, " MIN", y=560, tam=110, color="#ffd23f")],
             sfx=[(0.05, "whoosh", -20), (d * 0.6, "ding", -22)])


# ------------------------------------------------------------------ micro planos (ritmo)
@v.plano(19, "micro: «kilómetros de altura», la Tierra muy abajo vista desde la Estación")
def _(d):
    return P(OSC, [BG("bg_orbita"), iss(ancho=300, x=540, y=430, keys=[{"t": 0, "x": 480}, {"t": d, "x": 600}])],
             cam(1.0, 1.06, (540, 900)), "corte", sfx=[(0.02, "roce", -22)])


@v.plano(28, "micro: «kilómetros por hora», la aguja tiembla al máximo")
def _(d):
    return P(["#0a1a2a", "#020610"], [BG("bg_estudio"), IMG("velocimetro", ancho=900, x=540, y=1100, z=0.5),
                                      IMG("aguja_vel", ancho=900, x=540, y=1100, z=0.55, keys=[{"t": 0, "rot": 74}, {"t": d * 0.3, "rot": 80}, {"t": d * 0.6, "rot": 72}, {"t": d, "rot": 79}])],
             cam(1.15, 1.25, (540, 1050)), "corte", sfx=[(0.02, "zap", -20)])


@v.plano(47, "micro: «planeta entero», la Tierra gira deprisa muy cerca")
def _(d):
    return P(OSC, [estrellas(40, 14), tierra(540, 1000, 1200, 0.4, giro=40)], cam(1.0, 1.1, (540, 1000)), "corte", sfx=[(0.02, "whoosh", -20)])


@v.plano(61, "micro: «al sol», el Sol enorme")
def _(d):
    return P(OSC, [*sol(540, 1000, 260, 0.3)], cam(1.0, 1.1, (540, 1000)), "corte", sfx=[(0.02, "brillo", -18)])


@v.plano(73, "o un atardecer: el Sol se esconde tras el borde")
def _(d):
    return P(OSC, [alba(), brillo(720, 700, 520, "#ff7a3a", 0.7, 0.07, keys=[{"t": 0, "op": 1}, {"t": d, "op": 0.1}]),
                   {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#000010", "x": 540, "y": 960, "z": 0.5, "keys": [{"t": 0, "op": 0}, {"t": d, "op": 0.55}]}],
             cam(1.2, 1.1, (720, 760)), "corte", sfx=[(0.05, "roce", -22)])


@v.plano(79, "y eso: la Estación da otra vuelta rápida")
def _(d):
    return P(OSC, [estrellas(60, 15), tierra(540, 1050, 600, 0.4, giro=14), iss(keys=orbita_keys(d, r=420, a0=-90, a1=270, pasos=12), z=0.6)],
             cam(1.0, 1.04, (540, 1050)), "corte", sfx=[(0.05, "whoosh", -20, {"dur": d})])


@v.plano(104, "ahí arriba: la Estación muy alta sobre la Tierra, flecha hacia arriba")
def _(d):
    return P(OSC, [BG("bg_orbita"), iss(ancho=360, x=540, y=560, keys=late(0.1, 1)), flecha([[540, 1500], [540, 760]], 0.0, d * 0.6, CIAN, 10, z=0.6)],
             cam(1.0, 1.05, (540, 900)), "corte", sfx=[(0.05, "subida", -22, {"dur": d})])


@v.plano(114, "micro: «Greenwich», la línea del meridiano cruza la Tierra")
def _(d):
    return P(OSC, [estrellas(40, 16), tierra(540, 1050, 760, 0.4, giro=0), flecha([[540, 640], [540, 1460]], 0.0, d * 0.7, AMBAR, 8, punta=False, z=0.6)],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[rotulo(0.15, d - 0.03, "GMT", tam=150, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "trazo", -20)])


@v.plano(145, "viendo amanecer: la ventanilla se llena de luz")
def _(d):
    return P(OSC, [estrellas(50, 17), IMG("ventanilla", ancho=860, x=540, y=1050, z=0.5),
                   brillo(700, 900, 420, "#ffc070", 0.8, 0.6, keys=[{"t": 0, "op": 0}, {"t": d, "op": 1}])],
             cam(1.0, 1.1, (560, 1000)), "corte", sfx=[(0.05, "brillo", -20)])


v.construir("2026-11-20-tarde-01-dieciseis-amaneceres", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 71, "db": -13},
            claves=["amaneceres", "Estación", "Tierra", "cuatrocientos", "rapidísimo", "veintiocho", "ocho", "segundo", "noventa", "mitad", "sol", "oscuras",
                    "cuarenta", "dieciséis", "veinticuatro", "Luna", "volver", "hora", "Greenwich", "Londres", "campo", "fútbol", "habitada", "dos", "mil", "amanecer"])
