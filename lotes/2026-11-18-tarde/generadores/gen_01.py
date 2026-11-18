"""01 · GTA 6 tardó trece años — método denso. Lote 2026-11-18-tarde, Agente 20:00 (Jorge).
Sin logos, carátulas, personajes ni capturas del juego: todo genérico (DECISIONS / IDEAS).
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_tarde  # noqa: E402

SVG = ilus_tarde.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

OSC = ["#0a0620", "#2a0f4a"]
ATARDECER = ["#2a1a5a", "#ff8a4a"]
ROJO = "#ff2d55"


def hojas(d, nombres, x=540, y=980, ancho=760, z=0.5, cada=None):
    """Hojas de calendario que se arrancan una tras otra y salen volando (la última se queda)."""
    cada = cada or d / max(1, len(nombres))
    els = []
    for k, n in enumerate(nombres):
        t0 = k * cada
        ultima = k == len(nombres) - 1
        ks = [{"t": 0, "x": x, "y": y, "rot": 0, "op": 1 if k == 0 else 0}]
        if k:
            ks.append({"t": max(0.01, t0 - 0.02), "op": 0}); ks.append({"t": t0, "op": 1})
        if not ultima:
            ks += [{"t": t0 + cada * 0.55, "x": x + 20, "y": y - 10, "rot": -4},
                   {"t": t0 + cada, "x": x + 700, "y": y - 600, "rot": 50, "op": 0, "ease": "entrada"}]
        else:
            ks.append({"t": d, "x": x, "y": y, "rot": 0})
        els.append(IMG(n, ancho=ancho, z=z + 0.01 * (len(nombres) - k), keys=ks))
    return els


def coche(d, z=0.55, y=1600, ida=True):
    x0, x1 = (-500, 1600) if ida else (1600, -500)
    return IMG("coche_policia", ancho=620, z=z, keys=[{"t": 0, "x": x0, "y": y}, {"t": d, "x": x1, "y": y, "ease": "lineal"}], ex=1 if ida else -1)


def sirena(x, y, d, z=0.6):
    return [brillo(x, y, 260, "#ff2d55", 0.5, z, pulso=[0.45, 0.4]), brillo(x + 60, y, 260, "#2f7bff", 0.5, z, pulso=[0.45, 0.4])]


# ================================================================== PLANOS
@v.plano(0, "gancho: hojas del calendario arrancándose a toda velocidad")
def _(d):
    nombres = ["hoja_2013"] + ["calendario"] * 6 + ["hoja_2026"]
    return P(OSC, [BG("bg_ciudad_noche"), brillo(540, 980, 600, "#ff3df2", 0.35, 0.3, pulso=[0.15, 0.3]),
             *hojas(d, nombres, 540, 1000, 780, 0.5, d / 8.5), *lineas_vel(540, 900, 2, "#ffffff66")],
             cam(1.05, 1.0, (540, 1000), (540, 980)), vineta=0.6,
             sfx=[(0.02, "whoosh", -12, {"dur": 0.8})] + [(k * d / 8.5, "roce", -18) for k in range(1, 8)])


@v.plano(3, "micro: TRECE AÑOS en grande", mas=0.05)
def _(d):
    return P(OSC, [BG("bg_ciudad_noche"), IMG("hoja_2026", ancho=520, x=540, y=1150, z=0.5, keys=late(0.05, 1, 0.1, 0.3))],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[contador(0.02, d - 0.03, 0, 13, d * 0.6, "AÑOS", tam=150, y=560, borde=MAGENTA, miles=False)],
             sfx=[(0.05, "golpe", -14)])


@v.plano(5, "más que ir a la Luna: cohete despegando")
def _(d):
    return P(["#02030a", "#0a1030"], [BG("bg_esp_violeta"), luna(820, 480, 420, 0.2, anim={"girar": 2}),
             IMG("cohete", ancho=300, z=0.5, rot=20, keys=[{"t": 0, "x": 200, "y": 1700}, {"t": d, "x": 700, "y": 700, "ease": "entrada"}]),
             flecha([[180, 1800], [400, 1300], [700, 760]], 0.0, d * 0.9, AMBAR, 8, z=0.45), brillo(200, 1750, 300, "#ffb46a", 0.6, 0.4, pulso=[0.2, 0.2])],
             cam(1.0, 1.06), "desenfoque", sfx=[(0.05, "subida", -16, {"dur": d * 0.8})])


@v.plano(11, "GTA cinco: el mando sobre la ciudad al atardecer")
def _(d):
    return P(ATARDECER, [BG("bg_ciudad"), IMG("mando", ancho=700, x=540, y=1150, z=0.6, keys=[{"t": 0, "y": 1300, "op": 0}, {"t": 0.35, "y": 1150, "op": 1, "ease": "rebote"}], anim={"flotar": [10, 2]}),
             polvo("#ffe9a0", 30, (0, 700, 1080, 1500), 4)],
             cam(1.04, 1.0, (540, 1100)), "corte", hud=[contexto(0.05, d - 0.05, "GTA 5")], sfx=[(0.3, "pop", -16)])


@v.plano(15, "diecisiete de septiembre de dos mil trece: cae la hoja")
def _(d):
    return P(ATARDECER, [BG("bg_ciudad"), *cae_hoja(d, "hoja_2013")],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[rotulo(0.1, d - 0.05, "17 SEPT", tam=110, color="#141414", capsula="#ffe93de6", y=560)],
             sfx=[(d * 0.35, "golpe", -14)])


def cae_hoja(d, nombre, x=540, y=1100, ancho=620):
    return [IMG(nombre, ancho=ancho, z=0.5, keys=[{"t": 0, "x": x, "y": -300, "rot": -12},
            {"t": d * 0.35, "x": x, "y": y, "rot": 0, "ease": "entrada"}, {"t": d * 0.45, "ey": 0.9}, {"t": d * 0.55, "ey": 1.0}, {"t": d, "x": x, "y": y - 10}]),
            polvo("#ffffff", 20, (x - 300, y + 200, x + 300, y + 300), 9, "chispas")]


@v.plano(22, "el seis llega mañana: ciudad de noche, coche patrulla pasa")
def _(d):
    return P(OSC, [BG("bg_ciudad_noche"), coche(d, 0.55, 1580), *sirena(540, 1450, d, 0.5),
             IMG("consola", ancho=280, x=830, y=1050, z=0.4, keys=aparece(0.1, 0.4))],
             cam(1.0, 1.05, (540, 1200)), "desenfoque", sfx=[(0.1, "whoosh", -14, {"dur": d})])


@v.plano(26, "diecinueve de noviembre: cae la hoja de 2026")
def _(d):
    return P(OSC, [BG("bg_ciudad_noche"), *cae_hoja(d, "hoja_2026"), brillo(540, 1100, 500, "#2f7bff", 0.35, 0.3)],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[rotulo(0.1, d - 0.05, "19 NOV", tam=120, color="#141414", capsula="#2ff3ffe6", y=560)],
             sfx=[(d * 0.35, "golpe", -14)])


@v.plano(29, "trece años y dos meses: el reloj de arena se vacía")
def _(d):
    return P(["#1a0f2e", "#3a1a40"], [BG("bg_esp_ambar"), IMG("reloj_arena", ancho=440, x=540, y=1080, z=0.5, anim={"balanceo": [3, 2.4]}),
             polvo("#f2c060", 40, (480, 1000, 600, 1250), 6, "chispas"), brillo(540, 1080, 420, "#ffb46a", 0.35, 0.3)],
             cam(1.0, 1.08, (540, 1080)), "zoom",
             hud=[contador(0.05, d * 0.55, 0, 13, d * 0.45, "AÑOS", tam=120, y=520, borde=AMBAR, miles=False),
                  rotulo(d * 0.5, d - 0.05, "+2 MESES", tam=80, color="#ffffff", capsula="#c0392be6", y=700)],
             sfx=[(0.1, "subida", -20, {"dur": d * 0.5})])


@v.plano(36, "¿y cuánto es eso? lupa sobre la arena")
def _(d):
    return P(["#1a0f2e", "#3a1a40"], [BG("bg_esp_ambar"), IMG("reloj_arena", ancho=900, x=540, y=1100, z=0.4),
             IMG("lupa", ancho=480, z=0.6, keys=[{"t": 0, "x": 300, "y": 1300}, {"t": d, "x": 700, "y": 1000, "ease": "suave"}])],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "¿CUÁNTO?", y=560, tam=120, color=AMBAR)], sfx=[(0.1, "roce", -20)])


@v.plano(40, "Kennedy prometió ir a la Luna: atril con micrófonos (1961)")
def _(d):
    return P(["#0a1030", "#1a2a5a"], [brillo(540, 700, 700, "#fff4d0", 0.35, 0.1), IMG("atril", ancho=600, x=540, y=1350, z=0.5, keys=aparece(0.0, 0.3)),
             luna(860, 480, 300, 0.2, keys=[{"t": 0, "op": 0}, {"t": d * 0.6, "op": 1}], anim={"girar": 2}),
             flecha([[560, 900], [700, 700], [800, 560]], d * 0.45, d * 0.95, CIAN, 8, z=0.45)],
             cam(1.0, 1.05, (540, 1100)), "desenfoque", hud=[contexto(0.05, d - 0.05, "1961 · KENNEDY")], sfx=[(0.2, "brillo", -20)])


@v.plano(47, "micro: la Luna enorme", mas=0.0)
def _(d):
    return P(["#02030a", "#0a1030"], [BG("bg_esp_petroleo"), luna(540, 1000, 900, 0.4, keys=[{"t": 0, "escala": 0.9}, {"t": d, "escala": 1.0}], anim={"girar": 3})],
             cam(1.0, 1.04), "corte", sfx=[(0.02, "whoosh", -14, {"dur": 0.4})])


@v.plano(50, "Armstrong la pisó: astronauta y huella en la superficie")
def _(d):
    return P(["#05060f", "#2a2a3a"], [BG("bg_superficie_rica"), IMG("modulo_lunar", ancho=420, x=820, y=1150, z=0.3),
             IMG("astronauta", ancho=360, z=0.5, keys=[{"t": 0, "x": 260, "y": 1250}, {"t": d, "x": 420, "y": 1230, "ease": "suave"}], anim={"flotar": [12, 1.2]}),
             {"tipo": "huella", "clase": "bota", "largo": 220, "x": 560, "y": 1560, "z": 0.6, "rot": -10, "keys": [{"t": 0, "op": 0}, {"t": d * 0.5, "op": 1}]}],
             cam(1.0, 1.06, (540, 1300)), "corte", hud=[contexto(0.05, d - 0.05, "1969")], sfx=[(d * 0.5, "golpe", -18)])


def barra13(d, hasta, t1, color, z=0.6, y=1150):
    return {"tipo": "barra", "x": 540, "y": y, "ancho": 860, "alto": 90, "color": color, "fondo": "#ffffff20", "z": z,
            "keys": [{"t": 0.05, "progreso": 0}, {"t": t1, "progreso": hasta / 13, "ease": "salida"}]}


@v.plano(53, "pasaron ocho años: barra de 8 sobre 13")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), barra13(d, 13, 0.06, "#ffffff30", 0.58), barra13(d, 8, d * 0.6, CIAN),
             luna(150, 1150, 140, 0.65, keys=[{"t": 0, "x": 110}, {"t": d * 0.6, "x": 110 + 860 * 8 / 13, "ease": "salida"}], anim={"girar": 20})],
             cam(1.0, 1.04), "corte", hud=[contador(0.05, d - 0.05, 0, 8, d * 0.6, "AÑOS", tam=140, y=560, borde=CIAN, miles=False)],
             sfx=[(0.05, "subida", -18, {"dur": d * 0.6})])


@v.plano(56, "llegamos a la Luna y aún sobraban cinco años")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), barra13(d, 8, 0.06, CIAN),
             {"tipo": "barra", "x": 540, "y": 1150, "ancho": 860, "alto": 90, "color": MAGENTA, "fondo": "#ffffff00", "z": 0.59,
              "keys": [{"t": 0.05, "progreso": 8 / 13}, {"t": d * 0.6, "progreso": 1.0, "ease": "salida"}]},
             IMG("bandera_roja", ancho=120, x=540 - 430 + 860 * 8 / 13, y=1030, z=0.65, keys=aparece(0.05, 0.3)),
             senala(540 - 430 + 860 * 10.5 / 13, 1150, d * 0.6, d - 0.05, 120, MAGENTA)],
             cam(1.0, 1.06, (540, 1150), (640, 1150)), "corte", hud=[rotulo(d * 0.3, d - 0.05, "+5 AÑOS", tam=130, color="#ffffff", capsula="#ff3df2cc", y=560)],
             sfx=[(d * 0.6, "ding", -18)])


@v.plano(65, "el Empire State sube con la grúa")
def _(d):
    return P(ATARDECER, [BG("bg_ciudad"), IMG("grua", ancho=520, x=820, y=900, z=0.35),
             IMG("rascacielos", ancho=360, x=480, z=0.5, keys=[{"t": 0, "y": 2200}, {"t": d * 0.85, "y": 1150, "ease": "salida"}]),
             polvo("#ffe9a0", 40, (300, 1300, 700, 1600), 11, "chispas")],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[contexto(0.05, d - 0.05, "EMPIRE STATE · 1931")], sfx=[(0.1, "subida", -18, {"dur": d * 0.8})])


@v.plano(72, "cuatrocientos diez días", mas=0.0)
def _(d):
    return P(ATARDECER, [BG("bg_ciudad"), IMG("rascacielos", ancho=360, x=540, y=1150, z=0.5), IMG("calendario", ancho=300, x=850, y=1450, z=0.6, keys=late(0.1, 2, 0.1, 0.3))],
             cam(1.0, 1.05), "corte", hud=[contador(0.02, d - 0.03, 0, 410, d * 0.6, "DÍAS", tam=140, y=560, borde=AMBAR, miles=False)],
             sfx=[(0.05, "subida", -20, {"dur": d * 0.6})])


@v.plano(75, "con este tiempo lo habrías construido once veces")
def _(d):
    torres = []
    for k in range(11):
        x = 90 + k * 90; t = 0.1 + k * (d * 0.65 / 11)
        torres.append(IMG("rascacielos", ancho=110, x=x, z=0.5, keys=[{"t": 0, "y": 2100}, {"t": t, "y": 2100}, {"t": t + 0.25, "y": 1280, "ease": "rebote"}]))
    return P(ATARDECER, [BG("bg_ciudad"), *torres], cam(1.0, 1.04, (540, 1150)), "corte",
             hud=[contador(0.05, d - 0.05, 0, 11, d * 0.7, "VECES", tam=140, y=560, borde=LIMA, miles=False, contar_prefijo="×")],
             sfx=[(0.1 + k * (d * 0.65 / 11) + 0.2, "pop", -22) for k in range(0, 11, 2)])


@v.plano(83, "Rockstar ni siquiera lo confirmó: carta cerrada que se abre")
def _(d):
    return P(["#141018", "#2a1a3a"], [brillo(540, 1000, 600, "#ff3df2", 0.3, 0.1), IMG("consola", ancho=360, x=540, y=1150, z=0.5, op=0.6, keys=[{"t": 0, "escala": 0.9}, {"t": d, "escala": 1.0, "ease": "suave"}]),
             IMG("mando", ancho=480, x=540, y=1480, z=0.55, op=0.7),
             IMG("reloj_arena", ancho=200, x=880, y=1450, z=0.6, anim={"balanceo": [8, 1.2]})],
             cam(1.0, 1.06, (540, 1100)), "desenfoque", hud=[amarillo(0.1, d - 0.05, "NI CONFIRMADO", y=560, tam=96, color=MAGENTA), rotulo(0.3, d - 0.05, "?", tam=260, color="#ffffff", capsula=None, y=900)], sfx=[(0.2, "roce", -20)])


@v.plano(93, "febrero de dos mil veintidós: cae la hoja")
def _(d):
    return P(["#141018", "#2a1a3a"], [*cae_hoja(d, "hoja_2022"), brillo(540, 1100, 500, "#7a3ad8", 0.4, 0.3)],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[rotulo(0.1, d - 0.05, "FEB 2022", tam=110, color="#ffffff", capsula="#7a3ad8e6", y=560)],
             sfx=[(d * 0.35, "golpe", -14)])


@v.plano(98, "el primer tráiler: pantalla que se enciende")
def _(d):
    return P(OSC, [BG("bg_ciudad_noche"), IMG("tele", ancho=900, x=540, y=1100, z=0.5, keys=[{"t": 0, "op": 0.2, "escala": 0.85}, {"t": 0.3, "op": 1, "escala": 1.0, "ease": "rebote"}]),
             brillo(540, 1080, 520, "#ff3df2", 0.4, 0.45, pulso=[0.2, 0.5])],
             cam(1.0, 1.05, (540, 1100)), "zoom", hud=[contexto(0.05, d - 0.05, "DICIEMBRE 2023")], sfx=[(0.1, "brillo", -18)])


@v.plano(108, "en un solo día: noventa millones de vistas")
def _(d):
    return P(OSC, [BG("bg_ciudad_noche"), IMG("tele", ancho=720, x=540, y=1200, z=0.5, anim={"pulso": [0.02, 0.4]}),
             polvo("#ff3df2", 60, (100, 700, 980, 1500), 13, "chispas"), *lineas_vel(540, 1200, 7, "#ff3df2aa")],
             cam(1.0, 1.08, (540, 1150)), "corte",
             hud=[contador(0.05, d - 0.05, 0, 90, d * 0.7, "MILLONES", tam=140, y=560, borde=MAGENTA, miles=False, contar_prefijo="+"),
                  rotulo(0.1, d - 0.05, "24 H", tam=70, color="#141414", capsula="#ffe93de6", y=760)],
             sfx=[(0.05, "subida", -18, {"dur": d * 0.7})])


@v.plano(119, "récord: el trofeo con rayos")
def _(d):
    return P(["#1a0a2a", "#3a1a4a"], [{"tipo": "rayos", "n": 16, "longitud": 900, "apertura": 8, "color": "#ffe93d55", "x": 540, "y": 1000, "z": 0.2, "anim": {"girar": 20}},
             IMG("trofeo", ancho=460, x=540, y=1100, z=0.5, keys=[{"t": 0, "escala": 0.4, "op": 0}, {"t": 0.3, "escala": 1.0, "op": 1, "ease": "rebote"}]),
             polvo("#ffe93d", 50, (200, 700, 880, 1400), 15, "chispas")],
             cam(1.0, 1.06), "corte", hud=[amarillo(0.05, d - 0.03, "RÉCORD", y=560, tam=130, color=AMBAR)], sfx=[(0.25, "impacto", -14)])


@v.plano(123, "dos retrasos: la barra de carga se atasca y vuelve atrás")
def _(d):
    return P(OSC, [BG("bg_ciudad_noche"),
             {"tipo": "barra", "x": 540, "y": 1150, "ancho": 860, "alto": 70, "color": CIAN, "fondo": "#ffffff20", "z": 0.6,
              "keys": [{"t": 0.0, "progreso": 0.2}, {"t": d * 0.45, "progreso": 0.92, "ease": "salida"}, {"t": d * 0.6, "progreso": 0.5, "ease": "entrada"}, {"t": d, "progreso": 0.6}]},
             IMG("reloj_arena", ancho=200, x=540, y=1450, z=0.6, keys=[{"t": 0, "rot": 0}, {"t": d * 0.5, "rot": 0}, {"t": d * 0.7, "rot": 180, "ease": "rebote"}])],
             cam(1.0, 1.04), "corte", hud=[rotulo(0.05, d - 0.05, "2 RETRASOS", tam=110, color="#ffffff", capsula="#c0392be6", y=560)],
             sfx=[(d * 0.6, "golpe", -14)])


@v.plano(126, "de 2025 a mayo")
def _(d):
    return P(OSC, [BG("bg_ciudad_noche"), *hojas(d, ["calendario", "calendario"], 540, 1150, 520, 0.5, d * 0.6)],
             cam(1.0, 1.05), "corte", hud=[rotulo(0.05, d - 0.05, "MAYO 2026", tam=100, color="#141414", capsula="#ffe93de6", y=560)],
             sfx=[(d * 0.5, "roce", -18)])


@v.plano(132, "y de mayo a noviembre")
def _(d):
    return P(OSC, [BG("bg_ciudad_noche"), *hojas(d, ["calendario", "hoja_2026"], 540, 1150, 520, 0.5, d * 0.55), coche(d, 0.65, 1650, False)],
             cam(1.0, 1.05), "corte", hud=[rotulo(0.05, d - 0.05, "NOV 2026", tam=100, color="#141414", capsula="#2ff3ffe6", y=560)],
             sfx=[(d * 0.5, "roce", -18)])


@v.plano(137, "mañana, por fin: la consola se enciende")
def _(d):
    return P(OSC, [BG("bg_ciudad_noche"), brillo(540, 1000, 700, "#2ff3ff", 0.4, 0.3, pulso=[0.2, 0.8]),
             IMG("consola", ancho=380, x=540, y=1100, z=0.5, keys=[{"t": 0, "y": 1600, "op": 0}, {"t": 0.35, "y": 1100, "op": 1, "ease": "rebote"}]),
             IMG("mando", ancho=520, x=540, y=1500, z=0.65, keys=aparece(d * 0.4, 0.3), anim={"flotar": [8, 1.5]})],
             cam(1.0, 1.06, (540, 1200)), "desenfoque", hud=[rotulo(0.05, d - 0.05, "PS5 · XBOX SERIES", tam=80, color="#ffffff", capsula="#141414e6", y=560)],
             sfx=[(0.3, "brillo", -16)])


@v.plano(147, "¿cuántas horas le vas a dar? (bucle al calendario)")
def _(d):
    return P(OSC, [BG("bg_ciudad_noche"), IMG("mando", ancho=760, x=540, y=1150, z=0.5, keys=late(0.1, 2, 0.06, 0.4), anim={"balanceo": [4, 0.8]}),
             IMG("hoja_2013", ancho=780, x=540, y=1000, z=0.7, keys=[{"t": 0, "op": 0}, {"t": d - 0.4, "op": 0}, {"t": d, "op": 1}])],
             cam(1.0, 1.05, (540, 1100)), "desenfoque", hud=[amarillo(0.05, d - 0.45, "¿CUÁNTAS HORAS?", y=560, tam=96, color=CIAN)], sfx=[(0.1, "pop", -16)])


# ------------------------------------------------------------------ micro planos (golpes de 0,3–0,7 s)
@v.plano(9, "micro: llamarada del cohete", mas=0.1)
def _(d):
    return P(["#02030a", "#3a1a10"], [brillo(540, 1100, 700, "#ffb46a", 0.8, 0.3, pulso=[0.3, 0.15]), polvo("#ffd06a", 80, (300, 900, 780, 1500), 22, "chispas"),
             IMG("cohete", ancho=260, x=540, y=820, z=0.5, keys=[{"t": 0, "y": 900}, {"t": d, "y": 700}])], cam(1.0, 1.1, (540, 1000), (540, 960), temblor=6), "corte", sfx=[(0.02, "golpe", -16)])


@v.plano(20, "micro: la hoja de 2013 de cerca", mas=0.1)
def _(d):
    return P(ATARDECER, [BG("bg_ciudad"), IMG("hoja_2013", ancho=1000, x=540, y=1000, z=0.5, keys=late(0.0, 1, 0.06, 0.3))],
             cam(1.3, 1.45, (540, 1000), (520, 980)), "corte", sfx=[(0.02, "pop", -18)])


@v.plano(34, "micro: chispas de arena cayendo", mas=0.05)
def _(d):
    return P(["#1a0f2e", "#3a1a40"], [IMG("reloj_arena", ancho=1500, x=540, y=900, z=0.4), polvo("#f2c060", 80, (480, 700, 600, 1400), 23, "chispas")],
             cam(1.4, 1.55, (540, 960)), "corte", sfx=[(0.02, "roce", -20)])


@v.plano(63, "micro: +5 que late", mas=0.05)
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), brillo(540, 1000, 500, "#ff3df2", 0.5, 0.3)], cam(1.0, 1.08), "corte",
             hud=[rotulo(0.0, d - 0.03, "+5", tam=260, color="#ffffff", capsula="#ff3df2cc", y=900, sin_pop=True)], sfx=[(0.02, "golpe", -14)])


@v.plano(81, "micro: once torres de golpe", mas=0.05)
def _(d):
    torres = [IMG("rascacielos", ancho=150, x=60 + k * 96, y=1250, z=0.5) for k in range(11)]
    return P(ATARDECER, [BG("bg_ciudad"), *torres], cam(1.15, 1.3, (540, 1100), temblor=4), "corte",
             hud=[rotulo(0.0, d - 0.03, "×11", tam=220, color="#141414", capsula="#7dff3ae6", y=600, sin_pop=True)], sfx=[(0.02, "impacto", -16)])


@v.plano(91, "micro: el reloj de arena gira impaciente", mas=0.05)
def _(d):
    return P(["#141018", "#2a1a3a"], [IMG("reloj_arena", ancho=600, x=540, y=1000, z=0.5, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 180, "ease": "suave"}])],
             cam(1.0, 1.1), "corte", sfx=[(0.02, "whoosh", -16, {"dur": 0.4})])


@v.plano(106, "micro: botón de reproducir de cerca", mas=0.05)
def _(d):
    return P(OSC, [IMG("tele", ancho=2400, x=540, y=1000, z=0.5), brillo(540, 1000, 300, "#ffffff", 0.5, 0.6, pulso=[0.3, 0.2])],
             cam(1.0, 1.15, (540, 960)), "corte", sfx=[(0.02, "pop", -16)])


@v.plano(121, "micro: destello del trofeo", mas=0.05)
def _(d):
    return P(["#1a0a2a", "#3a1a4a"], [IMG("trofeo", ancho=1100, x=540, y=1100, z=0.5), brillo(420, 800, 260, "#ffffff", 0.9, 0.7, pulso=[0.5, 0.2])],
             cam(1.2, 1.3, (540, 900)), "corte", sfx=[(0.02, "ding", -18)])


@v.plano(130, "micro: hoja de mayo vuela", mas=0.05)
def _(d):
    return P(OSC, [BG("bg_ciudad_noche"), IMG("calendario", ancho=700, z=0.6, keys=lanza(0.0, d, (300, 1300), (900, 600)), anim={"girar": 120})],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "whoosh", -16, {"dur": 0.4})])


@v.plano(145, "micro: botones del mando de cerca", mas=0.05)
def _(d):
    return P(OSC, [IMG("mando", ancho=2200, x=200, y=1000, z=0.5), brillo(540, 1000, 300, "#2ff3ff", 0.5, 0.6, pulso=[0.3, 0.2])],
             cam(1.0, 1.1, (540, 1000)), "corte", sfx=[(0.02, "pop", -18)])


v.construir("2026-11-18-tarde-01-gta6-trece-anos", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 61, "db": -13},
            claves=["GTA", "trece", "Luna", "septiembre", "mañana", "noviembre", "Kennedy", "Armstrong", "ocho", "cinco", "Empire", "once", "Rockstar", "noventa", "récord", "retrasos"])
