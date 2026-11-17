"""01 · Este plátano es radiactivo — método denso (motor/DENSO.md). Lote 2026-11-17-manana, Agente 08:00 (Nico).
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_lote  # noqa: E402

SVG = ilus_lote.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

COCINA = ["#2a1c14", "#3a2414"]
LAB = ["#06121a", "#041018"]


def chispas_en(x, y, d, n=4, sem=1, r=120, z=0.7):
    """Átomos que «se rompen»: destellos verdes que saltan dentro de una zona, escalonados."""
    import random
    rr = random.Random(sem)
    out = []
    for k in range(n):
        t = d * (0.1 + 0.8 * k / max(1, n))
        px, py = x + rr.uniform(-r, r), y + rr.uniform(-r * 0.4, r * 0.4)
        out.append(IMG("chispa", ancho=110, x=px, y=py, z=z, keys=[{"t": t, "op": 0, "escala": 0.2}, {"t": t + 0.06, "op": 1, "escala": 1.0},
                                                                   {"t": t + 0.35, "op": 0, "escala": 1.4}]))
    return out


def platanos_rejilla(n, d, x0=150, y0=520, cols=5, paso=(190, 120), ancho=170, z=0.5, t_total=0.6):
    out = []
    for k in range(n):
        x, y = x0 + (k % cols) * paso[0], y0 + (k // cols) * paso[1]
        t = d * t_total * k / max(1, n)
        out.append(IMG("platano" if k % 2 else "platano_b", ancho=ancho, x=x, y=y, z=z + k * 0.001, rot=-8 + (k * 7) % 16,
                       keys=aparece(t, 0.3)))
    return out


# ================================================================== PLANOS
@v.plano(0, "gancho: el plátano cae y chispea")
def _(d):
    return P(COCINA, [BG("bg_cocina"), brillo(540, 900, 600, "#b6ff5a", 0.35, 0.1, pulso=[0.25, 0.4]),
             IMG("platano", ancho=900, x=540, z=0.6, keys=cae(0, d * 0.55, 600, 1100, 0.12) + [{"t": 0, "rot": -25}, {"t": d * 0.55, "rot": -6, "ease": "salida"}]),
             *chispas_en(540, 1080, d, 4, 1, 260), polvo("#d8ffb0", 30, (100, 700, 980, 1400), 2, "chispas")],
             cam(1.0, 1.3, (540, 1050), (540, 1080)), vineta=0.7, sfx=[(d * 0.2, "golpe", -12), (d * 0.5, "zap", -18)])


@v.plano(4, "micro: no es broma")
def _(d):
    return P(COCINA, [BG("bg_cocina"), brillo(540, 1000, 420, "#b6ff5a", 0.6, 0.1, pulso=[0.3, 0.25]),
             IMG("platano", ancho=760, x=540, y=1050, z=0.6, rot=-6, anim={"balanceo": [2, 0.12]}), *chispas_en(540, 1050, d, 3, 2, 220)],
             cam(1.25, 1.35, (540, 1050), (560, 1050)), "desenfoque", 0.2, sfx=[(0.1, "zap", -20)])


@v.plano(9, "el detector")
def _(d):
    return P(LAB, [BG("bg_lab"), IMG("platano", ancho=520, x=330, y=1180, z=0.5, rot=-10),
             IMG("detector", ancho=520, x=750, z=0.6, keys=[{"t": 0, "x": 1150, "y": 980}, {"t": d * 0.4, "x": 760, "y": 980, "ease": "salida"}]),
             flecha([[640, 1060], [470, 1150]], d * 0.45, d * 0.85, LIMA, 7, [16, 12])],
             cam(1.0, 1.08, (560, 1050), (540, 1040)), "zoom", hud=[amarillo(0.2, d - 0.05, "DETECTOR", y=640, color=CIAN)],
             sfx=[(0.05, "whoosh", -14, {"dur": 0.4})])


@v.plano(14, "micro: la aguja salta")
def _(d):
    return P(LAB, [BG("bg_lab"), IMG("detector", ancho=1200, x=540, y=1120, z=0.6),
             IMG("aguja_geiger", ancho=470, x=540, y=1104, z=0.62, keys=[{"t": 0, "rot": -70}, {"t": d * 0.3, "rot": -20, "ease": "elastico"}, {"t": d * 0.6, "rot": -35}, {"t": d, "rot": -15, "ease": "elastico"}])],
             cam(1.4, 1.5, (540, 1000), (540, 990)), sfx=[(t, "tic", -20) for t in (0.1, 0.3, 0.6)])


@v.plano(17, "la culpa: el potasio")
def _(d):
    return P(LAB, [BG("bg_lab"), brillo(540, 960, 500, "#2fd1a6", 0.4), IMG("atomo", ancho=760, x=540, y=960, z=0.5, anim={"girar": 18}, keys=aparece(0.05, 0.45)),
             polvo("#9dffb0", 30, (100, 500, 980, 1400), 4, "chispas")],
             cam(1.0, 1.1), hud=[rotulo(0.15, d - 0.05, "POTASIO", tam=110, color="#ffffff", capsula="#0d1330d8", borde=LIMA, y=1360)],
             sfx=[(0.05, "brillo", -16)])


@v.plano(22, "medio gramo")
def _(d):
    return P(COCINA, [BG("bg_cocina"),
             IMG("platano", ancho=620, x=540, z=0.6, keys=cae(0, d * 0.4, 600, 1180, 0.1)),
             brillo(540, 930, 300, "#ffe08a", 0.3, 0.3)],
             cam(1.0, 1.06, (540, 1000), (540, 980)), "desenfoque",
             hud=[{**contador(d * 0.35, d - 0.05, 0, 0.5, d * 0.35, "GRAMOS", tam=110, y=600), "decimales": 1}],
             sfx=[(d * 0.4 * 0.36, "golpe", -14)])


@v.plano(28, "micro: una pizca")
def _(d):
    return P(["#2a2010", "#1a1408"], [IMG("platano", ancho=2600, x=540, y=1100, z=0.3, rot=-8),
             brillo(600, 980, 160, "#b6ff5a", 0.9, 0.5, pulso=[0.3, 0.3]), polvo("#fff3a8", 40, (300, 800, 900, 1200), 5)],
             cam(1.1, 1.3, (600, 980), (600, 980)), "zoom", 0.25, sfx=[(0.1, "brillo", -20)])


@v.plano(35, "potasio cuarenta")
def _(d):
    return P(LAB, [BG("bg_lab"), brillo(540, 960, 600, "#ff7a3a", 0.35), IMG("atomo", ancho=900, x=540, y=980, z=0.5, anim={"girar": 30}),
             senala(540, 980, d * 0.2, d - 0.05, 150, AMBAR)],
             cam(1.05, 1.2, (540, 980), (540, 980)), hud=[rotulo(0.1, d - 0.05, "POTASIO-40", tam=104, color=AMBAR, capsula="#0d1330d8", y=520)],
             sfx=[(0.1, "pop", -18)])


@v.plano(37, "átomo inestable: tiembla")
def _(d):
    return P(LAB, [BG("bg_lab"), brillo(540, 960, 600, "#ff3d6e", 0.4, pulso=[0.2, 0.15]),
             IMG("atomo", ancho=900, x=540, y=980, z=0.5, anim={"balanceo": [6, 0.09], "girar": 40})],
             cam(1.2, 1.32, (540, 980), (540, 980)), hud=[amarillo(0.1, d - 0.05, "INESTABLE", y=1380, color=MAGENTA)], sfx=[(0, "rumor", -18, {"dur": d})])


@v.plano(40, "cada segundo: cronómetro")
def _(d):
    return P(["#1b2236", "#0b0f1c"], [brillo(540, 1000, 700, "#7ad0ff", 0.3), *cronometro(0, 360, 0, d)],
             cam(1.05, 1.15, (540, 1050), (540, 1050)), "desenfoque", 0.2, sfx=[(0.0, "tictac", -16, {"dur": d, "ritmo": 0.25})])


@v.plano(42, "quince átomos se rompen")
def _(d):
    return P(["#2a2010", "#120c06"], [brillo(540, 1000, 600, "#b6ff5a", 0.3), IMG("platano", ancho=1000, x=540, y=1050, z=0.4, rot=-6),
             *chispas_en(540, 1060, d, 8, 3, 330)],
             cam(1.0, 1.08, (540, 1000), (540, 1020)), hud=[contador(0.1, d - 0.05, 0, 15, d * 0.7, "POR SEGUNDO", tam=120, y=560, borde=LIMA)],
             sfx=[(d * (0.1 + 0.8 * k / 8), "tic", -25) for k in range(8)])


@v.plano(49, "micro: dentro del plátano")
def _(d):
    return P(["#2a2010", "#120c06"], [IMG("platano", ancho=2400, x=540, y=1000, z=0.3, rot=-6), *chispas_en(560, 1000, d, 3, 4, 200, 0.6),
             IMG("atomo", ancho=300, x=560, y=1000, z=0.5, anim={"balanceo": [8, 0.08]})],
             cam(1.2, 1.4, (560, 1000), (560, 1000)), "zoom", 0.2, sfx=[(0.05, "zap", -20)])


@v.plano(52, "chispazo de radiación")
def _(d):
    return P(["#040806", "#0a1a10"], [brillo(540, 960, 700, "#7dff3a", 0.4, pulso=[0.3, 0.2]),
             IMG("atomo", ancho=520, x=540, y=960, z=0.4, keys=[{"t": 0, "escala": 1}, {"t": d * 0.3, "escala": 1.2}, {"t": d * 0.35, "escala": 0.6, "op": 0.3}]),
             IMG("chispa", ancho=900, x=540, y=960, z=0.6, keys=[{"t": d * 0.3, "op": 0, "escala": 0.2}, {"t": d * 0.36, "op": 1, "escala": 1.0}, {"t": d, "op": 0.3, "escala": 1.6}]),
             *[flecha([[540, 960], [540 + 420 * dx, 960 + 420 * dy]], d * 0.35, d * 0.7, LIMA, 6) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (0.7, 0.7), (-0.7, -0.7)]]],
             cam(1.0, 1.12), hud=[amarillo(d * 0.35, d - 0.05, "RADIACIÓN", y=1380, color=LIMA)], sfx=[(d * 0.32, "impacto", -12)])


@v.plano(58, "¿y eso es mucho?")
def _(d):
    return P(COCINA, [BG("bg_cocina"), IMG("platano", ancho=700, x=540, y=1050, z=0.5, rot=-6, keys=late(0.1, 2, 0.08, 0.35))],
             cam(1.05, 1.15, (540, 1000), (540, 1020)), "desenfoque", 0.2, hud=[rotulo(0.05, d - 0.05, "¿MUCHO?", tam=130, color=AMBAR, capsula=None, y=560)],
             energia=0.3)


@v.plano(62, "los científicos")
def _(d):
    return P(LAB, [BG("bg_lab"), IMG("microscopio", ancho=420, x=260, y=1120, z=0.4),
             IMG("platano", ancho=420, x=720, y=1050, z=0.55, keys=[{"t": 0, "rot": -10, "y": 1080}, {"t": d, "rot": 6, "y": 1020, "ease": "suave"}]),
             brillo(720, 1050, 260, "#ffe08a", 0.5, 0.5, pulso=[0.2, 0.5]),
             {"tipo": "forma", "forma": "rect", "ancho": 360, "alto": 30, "relleno": "#2ff3ff", "x": 720, "y": 1200, "z": 0.5, "op": 0.6}],
             cam(1.0, 1.08, (540, 1050), (600, 1050)), "zoom", sfx=[(0.1, "brillo", -18)])


@v.plano(70, "micro: como unidad (regla)")
def _(d):
    return P(LAB, [BG("bg_lab"), IMG("regla", ancho=1000, x=540, y=1050, z=0.4, rot=-3),
             IMG("platano", ancho=300, y=930, z=0.6, keys=[{"t": 0, "x": 250}, {"t": d * 0.8, "x": 800, "ease": "salida"}])],
             cam(1.1, 1.2, (540, 1000), (560, 1000)), "desenfoque", 0.2, sfx=[(0.1 + i * 0.15, "tic", -22) for i in range(4)])


@v.plano(72, "LA DOSIS PLÁTANO")
def _(d):
    return P(LAB, [BG("bg_lab"), brillo(540, 1000, 500, "#ffe08a", 0.5), IMG("platano", ancho=800, x=540, y=1050, z=0.5, keys=aparece(0.0, 0.4) + [{"t": d, "rot": 4}]),
             polvo("#fff3a8", 40, (100, 700, 980, 1400), 6, "chispas")],
             cam(1.0, 1.1), hud=[rotulo(0.1, d - 0.05, "DOSIS PLÁTANO", tam=96, color="#141414", capsula="#ffd23fe6", y=560)],
             sfx=[(0.05, "ding", -16)])


@v.plano(75, "comerte uno")
def _(d):
    return P(COCINA, [BG("bg_cocina"), IMG("platano", ancho=760, x=540, y=1050, z=0.5, keys=[{"t": 0, "rot": -20, "x": 520}, {"t": d, "rot": 8, "x": 560, "ease": "suave"}])],
             cam(1.0, 1.1, (540, 1050), (540, 1030)), "desenfoque", sfx=[(d * 0.6, "mordisco", -14)])


@v.plano(77, "una décima de microsievert")
def _(d):
    return P(LAB, [BG("bg_lab"), IMG("detector", ancho=700, x=540, y=1080, z=0.5),
             IMG("aguja_geiger", ancho=274, x=540, y=1071, z=0.52, keys=[{"t": 0, "rot": -75}, {"t": d * 0.5, "rot": -68, "ease": "elastico"}])],
             cam(1.0, 1.06, (540, 1000), (540, 1000)),
             hud=[{**contador(0.1, d - 0.05, 0, 0.1, d * 0.4, "µSv", tam=130, y=560, borde=CIAN), "decimales": 1}], sfx=[(0.2, "tic", -18)])


@v.plano(83, "radiación natural de cada día")
def _(d):
    return P(ESPACIO, [BG("bg_esp_ambar"), *sol(800, 420, 150), tierra(400, 1250, 700, giro=6),
             *[flecha([[700 - k * 60, 500 + k * 40], [480 - k * 60, 1000 + k * 30]], 0.1 + k * 0.12, d * 0.7, AMBAR, 6, [14, 10]) for k in range(3)]],
             cam(1.0, 1.06, (540, 900), (540, 960)), "zoom", hud=[contexto(0.05, d - 0.05, "CADA DÍA")])


@v.plano(90, "cien plátanos")
def _(d):
    return P(COCINA, [BG("bg_cocina"), *platanos_rejilla(25, d, 140, 560, 5, (200, 150), 190, 0.4, 0.7)],
             cam(1.0, 0.98 + 0.12, (540, 900), (540, 920)), hud=[contador(0.05, d - 0.05, 0, 100, d * 0.7, "PLÁTANOS", tam=110, y=1340, capsula="#0d1330d8")],
             sfx=[(d * 0.7 * k / 10, "pop", -24) for k in range(10)])


@v.plano(94, "escáner de tórax")
def _(d):
    return P(["#dfe6ee", "#9aa6b4"], [brillo(540, 900, 700, "#ffffff", 0.5), IMG("escaner", ancho=1000, x=540, z=0.5, keys=[{"t": 0, "y": 1150, "escala": 0.95}, {"t": d, "y": 1100, "escala": 1.03, "ease": "suave"}]),
             brillo(640, 1060, 180, "#2ff3ff", 0.6, 0.55, pulso=[0.3, 0.3])],
             cam(1.0, 1.08, (540, 1050), (580, 1050)), "zoom", hud=[contexto(0.05, d - 0.05, "ESCÁNER")], sfx=[(0, "rumor", -20, {"dur": d})])


@v.plano(98, "setenta mil plátanos")
def _(d):
    import random
    rr = random.Random(12)
    lluvia = [IMG("platano" if k % 2 else "platano_b", ancho=rr.uniform(140, 260), x=rr.uniform(60, 1020), z=0.4 + k * 0.002,
                  keys=[{"t": rr.uniform(0, d * 0.6), "y": -200, "rot": rr.uniform(-90, 90)}, {"t": d, "y": rr.uniform(900, 1900), "rot": rr.uniform(-180, 180), "ease": "entrada"}])
              for k in range(36)]
    return P(["#dfe6ee", "#9aa6b4"], [IMG("escaner", ancho=1000, x=540, y=1300, z=0.3), *lluvia],
             cam(1.0, 1.05, (540, 960), (540, 1000)), hud=[contador(0.05, d - 0.05, 0, 70000, d * 0.75, "PLÁTANOS", tam=110, y=560, capsula="#c0392be6")],
             sfx=[(0.1, "subida", -16, {"dur": d * 0.8})])


@v.plano(101, "¿y tú?")
def _(d):
    return P(["#020814", "#0a1a38"], [brillo(540, 960, 600, "#3aa0ff", 0.4), IMG("cuerpo_rayos", ancho=560, x=540, z=0.5, keys=arranque(540, 1050, d, "abajo", 200, 30))],
             cam(1.1, 1.25, (540, 900), (540, 860)), "desenfoque", 0.2, hud=[rotulo(0.05, d - 0.05, "¿Y TÚ?", tam=130, color=CIAN, capsula=None, y=560)],
             sfx=[(0.05, "golpe", -14)], energia=0.4)


@v.plano(103, "tú también llevas potasio-40")
def _(d):
    import random
    rr = random.Random(5)
    atomos = [IMG("atomo", ancho=90, x=540 + rr.uniform(-150, 150), y=rr.uniform(600, 1350), z=0.6, anim={"girar": 60}, keys=aparece(d * k / 14, 0.3)) for k in range(12)]
    return P(["#020814", "#0a1a38"], [brillo(540, 960, 600, "#3aa0ff", 0.35), IMG("cuerpo_rayos", ancho=600, x=540, y=1000, z=0.5), *atomos],
             cam(1.0, 1.06, (540, 1000), (540, 980)), hud=[amarillo(0.1, d - 0.05, "POTASIO-40", y=560, color=AMBAR)])


@v.plano(107, "dentro de tu cuerpo, ahora mismo")
def _(d):
    return P(["#020814", "#0a1a38"], [IMG("cuerpo_rayos", ancho=1500, x=540, y=1500, z=0.4), *chispas_en(540, 1000, d, 7, 6, 300)],
             cam(1.1, 1.25, (540, 1000), (540, 980)), "zoom", sfx=[(d * (0.1 + 0.8 * k / 7), "tic", -25) for k in range(7)])


@v.plano(113, "cuatro mil por segundo")
def _(d):
    return P(["#020814", "#0a1a38"], [IMG("cuerpo_rayos", ancho=700, x=540, y=1050, z=0.4), *chispas_en(540, 950, d, 14, 7, 220, 0.6)],
             cam(1.6, 1.35, (540, 900), (540, 950)), hud=[contador(0.1, d - 0.05, 0, 4000, d * 0.7, "POR SEGUNDO", tam=120, y=560, borde=LIMA)],
             sfx=[(0.1, "subida", -18, {"dur": d * 0.7})])


@v.plano(121, "más radiactivo que…")
def _(d):
    return P(["#020814", "#0a1a38"], [brillo(300, 960, 300, "#3aa0ff", 0.5), brillo(800, 960, 260, "#ffe08a", 0.3),
             IMG("cuerpo_rayos", ancho=330, x=300, y=980, z=0.5, keys=late(0.2, 2, 0.08, 0.4)),
             IMG("racimo", ancho=360, x=800, y=1000, z=0.5, keys=aparece(0.1, 0.4))],
             cam(1.0, 1.06, (540, 1000), (540, 980)), "desenfoque", hud=[amarillo(0.1, d - 0.05, "MÁS RADIACTIVO", y=560, color=MAGENTA, tam=84),
                                                  rotulo(0.3, d - 0.05, ">", tam=200, color=AMBAR, capsula=None, x=550, y=980, fijo=True)])


@v.plano(125, "casi trescientos plátanos")
def _(d):
    return P(COCINA, [BG("bg_cocina"), *platanos_rejilla(40, d, 120, 520, 5, (210, 110), 200, 0.4, 0.6),
             IMG("cuerpo_rayos", ancho=380, x=880, y=1080, z=0.7)],
             cam(1.06, 1.0, (540, 960), (540, 960)), hud=[contador(0.05, d - 0.05, 0, 300, d * 0.6, "PLÁTANOS", tam=110, y=1340, capsula="#0d1330d8", contar_prefijo="≈")],
             sfx=[(d * 0.6, "impacto", -12)], energia=0.9)


@v.plano(129, "no pasa nada")
def _(d):
    return P(["#0a1a20", "#04100c"], [brillo(540, 960, 600, "#7dff3a", 0.25), IMG("cuerpo_rayos", ancho=1100, x=540, y=1500, z=0.5, anim={"flotar": [10, 1.6]}),
             IMG("platano", ancho=360, x=820, y=1300, z=0.6, rot=-20, anim={"balanceo": [5, 1.4]})],
             cam(1.0, 1.08, (540, 1000), (540, 980)), "desenfoque", 0.25, hud=[amarillo(0.1, d - 0.05, "TRANQUILO", y=560, color=LIMA)], energia=0.3)


@v.plano(133, "tu cuerpo expulsa lo que sobra")
def _(d):
    import random
    rr = random.Random(9)
    salen = [IMG("atomo", ancho=90, z=0.6, anim={"girar": 80}, keys=[{"t": d * k / 10, "x": 540 + rr.uniform(-60, 60), "y": rr.uniform(800, 1100), "op": 1},
                                                                       {"t": d * k / 10 + 0.9, "x": rr.choice([60, 1020]), "y": rr.uniform(500, 1500), "op": 0, "ease": "entrada"}]) for k in range(9)]
    return P(["#0a1a20", "#04100c"], [IMG("cuerpo_rayos", ancho=640, x=540, y=1050, z=0.5), *salen,
             flecha([[640, 960], [960, 960]], 0.1, d * 0.5, LIMA, 8), flecha([[440, 1060], [120, 1060]], d * 0.2, d * 0.6, LIMA, 8)],
             cam(1.0, 1.05), hud=[amarillo(0.1, d - 0.05, "LO EXPULSA", y=560, color=LIMA)], sfx=[(0.1, "whoosh", -16, {"dur": 0.5})])


@v.plano(141, "no se acumula")
def _(d):
    return P(LAB, [BG("bg_lab"), IMG("platano", ancho=520, x=300, y=1050, z=0.5, rot=-10),
             {"tipo": "barra", "x": 760, "y": 1120, "ancho": 300, "alto": 50, "color": "#7dff3a", "fondo": "#ffffff15", "z": 0.55,
              "keys": [{"t": 0, "progreso": 0.15}, {"t": d * 0.5, "progreso": 0.2}, {"t": d, "progreso": 0.15}]},
             IMG("detector", ancho=380, x=760, y=1220, z=0.5)],
             cam(1.0, 1.06, (540, 1050), (540, 1040)), hud=[rotulo(0.1, d - 0.05, "NO SE ACUMULA", tam=90, color="#ffffff", capsula="#0d1330d8", borde=LIMA, y=560)])


@v.plano(148, "¿te comerías uno? (cierre en bucle)")
def _(d):
    return P(COCINA, [BG("bg_cocina"), brillo(540, 900, 600, "#b6ff5a", 0.35, 0.1, pulso=[0.25, 0.4]),
             IMG("platano", ancho=900, x=540, y=1080, z=0.6, keys=[{"t": 0, "rot": -6, "escala": 0.9}, {"t": d, "rot": -20, "escala": 1.05, "ease": "suave"}]),
             *chispas_en(540, 1080, d, 3, 8, 260)],
             cam(1.1, 1.0, (540, 1080), (540, 1050)), "desenfoque", sfx=[(d * 0.5, "zap", -20)])


# ------------------------------------------------------------------ micro planos (golpes de 0,4–0,7 s)
def micro_cerca(svg, ancho, x, y, fondo, color, rot=0, anim=None, sfx="tic", db=-20, extra=()):
    def fn(d):
        return P(fondo, [brillo(540, 960, 520, color, 0.45, pulso=[0.2, 0.2]), IMG(svg, ancho=ancho, x=x, y=y, z=0.5, rot=rot, anim=anim or {"balanceo": [4, 0.1]},
                 keys=[{"t": 0, "escala": 0.92}, {"t": d, "escala": 1.06, "ease": "salida"}]), *extra],
                 cam(1.0, 1.1), "corte", sfx=[(0.02, sfx, db)])
    return fn


v.plano(16, "micro: clic, clic")(micro_cerca("detector", 1500, 540, 1250, LAB, "#7dff3a", sfx="tic", db=-14))
v.plano(33, "micro: K", mas=0.2)(lambda d: P(LAB, [BG("bg_lab"), brillo(540, 960, 400, "#ff7a3a", 0.6, pulso=[0.3, 0.15])], cam(1.0, 1.1), "corte",
                                       hud=[rotulo(0.0, d, "K", tam=260, color=AMBAR, capsula=None, y=960, fijo=True, sin_pop=True)], sfx=[(0.0, "pop", -16)]))
v.plano(47, "micro: se rompe")(micro_cerca("atomo", 1100, 540, 960, ["#040806", "#0a1a10"], "#7dff3a", anim={"balanceo": [10, 0.06]}, sfx="zap", db=-16,
                                          extra=[IMG("chispa", ancho=700, x=540, y=960, z=0.6, keys=[{"t": 0.15, "op": 0}, {"t": 0.2, "op": 1}, {"t": 0.6, "op": 0}])]))
v.plano(68, "micro: el ocular")(micro_cerca("microscopio", 1600, 700, 1300, LAB, "#2fd1a6", rot=0, sfx="tic"))
v.plano(88, "micro: el Sol")(lambda d: P(ESPACIO, [BG("bg_esp_ambar"), *sol(540, 960, 330)], cam(1.0, 1.12), "corte", sfx=[(0.02, "brillo", -18)]))
v.plano(112, "micro: un átomo dentro")(micro_cerca("atomo", 900, 540, 960, ["#020814", "#0a1a38"], "#3aa0ff", anim={"girar": 90}, sfx="zap", db=-18))


v.construir("2026-11-17-manana-01-platano-radiactivo", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 11, "db": -13},
            claves=["radiactivo", "potasio", "cuarenta", "quince", "dosis", "plátano", "cien", "setenta", "cuatro", "mil", "trescientos"])
