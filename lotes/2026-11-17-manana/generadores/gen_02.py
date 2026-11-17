"""02 · Saturno flotaría en el agua — método denso (motor/DENSO.md). Lote 2026-11-17-manana, Agente 08:00 (Nico).
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_lote  # noqa: E402

SVG = ilus_lote.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

BANO = ["#1a2a3a", "#0a1420"]
SAT = [(0.5, v.w(61), (-120, 1500), (1200, 1250))]   # un satélite cruza los planos de espacio de la primera mitad


def satelite(d):
    return [IMG("satelite", ancho=130, z=0.12, rot=-12, anim={"girar": 4}, keys=recorrido(*SAT[0], d))]


def azulejos():
    return [{"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 1920, "relleno": ["#2a4a64", "#12283a"], "x": 540, "y": 960, "z": 0.02},
            *[{"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 4, "relleno": "#ffffff", "op": 0.08, "x": 540, "y": y, "z": 0.03} for y in range(100, 1400, 130)],
            *[{"tipo": "forma", "forma": "rect", "ancho": 4, "alto": 1300, "relleno": "#ffffff", "op": 0.08, "x": x, "y": 700, "z": 0.03} for x in range(60, 1080, 130)],
            {"tipo": "forma", "forma": "rect", "ancho": 1080, "alto": 560, "relleno": ["#3a3430", "#1a1612"], "x": 540, "y": 1640, "z": 0.04}]


def banera_con(sat_keys, d, ancho_sat=620, gas=False, ola=True):
    els = [*azulejos(), brillo(540, 700, 600, "#fff2c8", 0.25, 0.05),
           IMG("banera", ancho=1080, x=540, y=1380, z=0.3),
           IMG("saturno", ancho=ancho_sat, x=540, z=0.4, keys=sat_keys),
           IMG("agua_frente", ancho=940, x=540, y=1350, z=0.5, op=0.75, anim={"flotar": [6, 1.2]})]
    if gas:
        els.append(IMG("nube_gas", ancho=900, x=540, y=1250, z=0.55, keys=[{"t": 0, "op": 0, "escala": 0.4}, {"t": d, "op": 0.95, "escala": 1.4, "ease": "suave"}]))
    return els


# ================================================================== PLANOS
@v.plano(0, "gancho: Saturno cae a la bañera")
def _(d):
    caida = [{"t": 0, "y": 420, "rot": -8}, {"t": d * 0.45, "y": 1090, "rot": 0, "ease": "entrada"}, {"t": d * 0.62, "y": 1130, "ease": "salida"}, {"t": d, "y": 1100, "ease": "suave"}]
    salpica = [brillo(540 + dx, 1200, 160, "#dff6ff", 0.9, 0.6, keys=[{"t": d * 0.45, "op": 0, "escala": 0.3}, {"t": d * 0.55, "op": 1, "escala": 1.2}, {"t": d, "op": 0}])
               for dx in (-260, 0, 260)]
    return P(BANO, [*banera_con(caida, d), *salpica, polvo("#dff6ff", 30, (200, 1050, 880, 1250), 3, "chispas")],
             cam(1.0, 1.25, (540, 1000), (540, 1150)), vineta=0.6, sfx=[(d * 0.45, "agua", -10), (d * 0.47, "golpe", -14)])


@v.plano(5, "flota: menos denso")
def _(d):
    return P(BANO, [*banera_con([{"t": 0, "y": 1100}, {"t": d, "y": 1080, "ease": "suave"}], d, 640)],
             cam(1.15, 1.25, (540, 1150), (540, 1130)), hud=[amarillo(0.1, d - 0.05, "MENOS DENSO", y=520, color=CIAN)],
             sfx=[(0.2, "agua", -22)])


@v.plano(10, "el único planeta así")
def _(d):
    return P(ESPACIO, [BG("bg_esp_violeta"), *satelite(d), estrellas(30, 4),
             tierra(180, 1200, 150, giro=8), IMG("luna_hd", ancho=110, x=330, y=1250, z=0.4),
             {"tipo": "esfera", "radio": 70, "textura": "rocosa", "color": "#e06a3a", "color2": "#8a2a14", "x": 860, "y": 1230, "z": 0.4, "giro": 6},
             IMG("saturno", ancho=760, x=540, z=0.5, keys=[{"t": 0, "y": 780, "escala": 0.8}, {"t": d * 0.3, "escala": 1.0, "ease": "elastico"}, {"t": d, "y": 760, "escala": 1.04}]),
             senala(540, 780, d * 0.3, d - 0.05, 230, AMBAR)],
             cam(1.0, 1.06, (540, 960), (540, 940)), "desenfoque", hud=[rotulo(0.05, d - 0.05, "EL ÚNICO", tam=70, color="#ffffff", capsula="#c0392be6", y=600)])


@v.plano(18, "un cubito de agua")
def _(d):
    return P(["#0a2030", "#04101a"], [IMG("agua_frente", ancho=1400, x=540, y=1700, z=0.1, op=0.6, anim={"flotar": [8, 1.5]}), polvo("#bfe8ff", 40, (0, 300, 1080, 1600), 21, "chispas"), IMG("saturno", ancho=300, x=860, y=520, z=0.2, anim={"flotar": [8, 1.6]}), brillo(540, 1000, 500, "#7fd4ff", 0.35), IMG("cubo_agua", ancho=520, x=540, z=0.5, keys=cae(0, d * 0.5, 500, 1000, 0.1)),
             flecha([[300, 1240], [660, 1240]], d * 0.5, d * 0.9, CIAN, 6, punta=False)],
             cam(1.0, 1.08, (540, 1000), (540, 990)), "zoom", hud=[rotulo(d * 0.5, d - 0.05, "1 CM", tam=90, color=CIAN, capsula="#0d1330d8", y=1340)],
             sfx=[(d * 0.5 * 0.36, "golpe", -16)])


@v.plano(25, "pesa un gramo")
def _(d):
    return P(["#0a2030", "#04101a"], [IMG("agua_frente", ancho=1400, x=540, y=1700, z=0.1, op=0.6, anim={"flotar": [8, 1.5]}), polvo("#bfe8ff", 40, (0, 300, 1080, 1600), 21, "chispas"), IMG("saturno", ancho=300, x=860, y=520, z=0.2, anim={"flotar": [8, 1.6]}), brillo(540, 1000, 500, "#7fd4ff", 0.35), IMG("cubo_agua", ancho=520, x=540, y=1000, z=0.5, keys=late(0.1, 2, 0.06, 0.35))],
             cam(1.08, 1.14, (540, 1000), (540, 990)), hud=[contador(0.02, d - 0.02, 0, 1, d * 0.4, "G", tam=130, y=520, borde=CIAN)])


@v.plano(28, "el mismo cubito, de Saturno")
def _(d):
    return P(["#1a1408", "#0a0804"], [polvo("#f6e2b0", 40, (0, 300, 1080, 1600), 22, "chispas"), IMG("saturno", ancho=1700, x=540, y=1750, z=0.1, op=0.45), brillo(540, 1000, 500, "#f0d8a0", 0.35),
             IMG("cubo_agua", ancho=360, x=270, y=1050, z=0.45),
             IMG("cubo_saturno", ancho=360, x=800, z=0.5, keys=cae(0, d * 0.5, 500, 1050, 0.1)),
             IMG("saturno", ancho=260, x=800, y=640, z=0.4, anim={"flotar": [8, 1.4]})],
             cam(1.0, 1.06, (540, 960), (540, 960)), "desenfoque", sfx=[(d * 0.5 * 0.36, "golpe", -16)])


@v.plano(34, "micro: pesaría…")
def _(d):
    return P(["#1a1408", "#0a0804"], [polvo("#f6e2b0", 40, (0, 300, 1080, 1600), 22, "chispas"), IMG("saturno", ancho=1700, x=540, y=1750, z=0.1, op=0.45), brillo(540, 1000, 500, "#f0d8a0", 0.45), IMG("cubo_saturno", ancho=760, x=540, y=1050, z=0.5, anim={"flotar": [12, 0.8]})],
             cam(1.25, 1.35, (540, 1050), (540, 1030)), "zoom", 0.2, energia=0.35)


@v.plano(37, "cero coma sesenta y nueve")
def _(d):
    return P(["#1a1408", "#0a0804"], [polvo("#f6e2b0", 40, (0, 300, 1080, 1600), 22, "chispas"), IMG("saturno", ancho=1700, x=540, y=1750, z=0.1, op=0.45), brillo(540, 1000, 500, "#f0d8a0", 0.35),
             IMG("cubo_agua", ancho=360, x=270, z=0.45, keys=[{"t": 0, "y": 1050}, {"t": d * 0.6, "y": 1110, "ease": "elastico"}]),
             IMG("cubo_saturno", ancho=360, x=800, z=0.5, keys=[{"t": 0, "y": 1050}, {"t": d * 0.6, "y": 980, "ease": "elastico"}])],
             cam(1.0, 1.05), hud=[rotulo(0.05, d - 0.05, "1 g", tam=90, color=CIAN, capsula="#0d1330d8", x=270, y=1330, fijo=True),
                                  {**contador(0.1, d - 0.05, 0, 0.69, d * 0.5, "g", tam=120, x=760, y=560, borde=AMBAR), "decimales": 2}],
             sfx=[(d * 0.6, "impacto", -12)])


@v.plano(42, "y eso que es gigante")
def _(d):
    return P(ESPACIO, [BG("bg_esp_ambar"), *satelite(d), estrellas(30, 5),
             IMG("saturno", ancho=1400, x=540, y=960, z=0.5, keys=[{"t": 0, "escala": 0.5}, {"t": d, "escala": 1.0, "ease": "salida"}])],
             cam(1.0, 1.08), "zoom", hud=[amarillo(0.2, d - 0.05, "GIGANTE", y=1380, color=AMBAR)], sfx=[(0.05, "rumor", -14, {"dur": d})])


@v.plano(47, "nueve veces más ancho que la Tierra")
def _(d):
    tierras = [tierra(100 + k * 110, 1300, 104, z=0.55, keys=aparece(d * 0.1 + k * d * 0.06, 0.25)) for k in range(9)]
    return P(ESPACIO, [BG("bg_esp_ambar"), *satelite(d), IMG("saturno", ancho=1600, x=540, y=820, z=0.4), *tierras,
             flecha([[60, 1400], [1020, 1400]], d * 0.1, d * 0.7, CIAN, 6, punta=False)],
             cam(1.0, 1.03), hud=[rotulo(d * 0.5, d - 0.05, "×9", tam=150, color=CIAN, capsula="#0d1330d8", y=620)],
             sfx=[(d * 0.1 + k * d * 0.06, "pop", -24) for k in range(9)])


@v.plano(55, "noventa y cinco veces más pesado")
def _(d):
    return P(ESPACIO, [BG("bg_esp_ambar"), *satelite(d), IMG("saturno", ancho=900, x=540, y=900, z=0.5, keys=[{"t": 0, "y": 860}, {"t": d * 0.6, "y": 960, "ease": "bote"}]),
             tierra(540, 1330, 120, z=0.55, keys=[{"t": 0, "y": 1300}, {"t": d * 0.6, "y": 1360, "ease": "bote"}])],
             cam(1.05, 1.0), hud=[contador(0.05, d - 0.05, 0, 95, d * 0.6, "VECES MÁS MASA", tam=110, y=560, capsula="#c0392be6")],
             sfx=[(d * 0.6, "golpe", -14)])


@v.plano(61, "¿cómo puede ser?")
def _(d):
    return P(ESPACIO, [BG("bg_esp_violeta"), estrellas(30, 6), IMG("saturno", ancho=800, x=540, y=960, z=0.5, anim={"flotar": [10, 1.4]}, keys=late(0.1, 2, 0.05, 0.4))],
             cam(1.1, 1.2, (540, 960), (540, 960)), "desenfoque", 0.2, hud=[rotulo(0.05, d - 0.05, "¿CÓMO?", tam=130, color=CIAN, capsula=None, y=520)], energia=0.3)


@v.plano(64, "hidrógeno y helio")
def _(d):
    return P(["#0a0618", "#04020c"], [brillo(540, 960, 600, "#7aa8ff", 0.3), IMG("saturno", ancho=1700, x=540, y=1700, z=0.2, op=0.5),
             IMG("atomo_h", ancho=430, x=290, y=860, z=0.5, anim={"girar": 30}, keys=aparece(0.05, 0.4)),
             IMG("atomo", ancho=430, x=790, y=860, z=0.5, anim={"girar": -30}, keys=aparece(d * 0.4, 0.4))],
             cam(1.0, 1.06), hud=[rotulo(0.1, d - 0.05, "H", tam=140, color=MAGENTA, capsula="#0d1330d8", x=290, y=1200, fijo=True),
                                  rotulo(d * 0.4, d - 0.05, "He", tam=140, color=CIAN, capsula="#0d1330d8", x=790, y=1200, fijo=True)],
             sfx=[(0.05, "pop", -18), (d * 0.4, "pop", -18)])


@v.plano(70, "los más ligeros: suben como globos")
def _(d):
    import random
    rr = random.Random(3)
    suben = [IMG("atomo_h" if k % 2 else "atomo", ancho=rr.uniform(120, 220), x=rr.uniform(120, 960), z=0.5, anim={"girar": 40},
                 keys=[{"t": 0, "y": rr.uniform(1300, 1800)}, {"t": d, "y": rr.uniform(300, 900), "ease": "suave"}]) for k in range(9)]
    return P(["#0a0618", "#04020c"], [brillo(540, 960, 600, "#7aa8ff", 0.3), *suben],
             cam(1.0, 1.05), hud=[amarillo(0.1, d - 0.05, "LOS MÁS LIGEROS", y=1300, color=LIMA, tam=84)], sfx=[(0.1, "subida", -18, {"dur": d})])


@v.plano(77, "eso sí, la bañera…")
def _(d):
    return P(BANO, [*banera_con([{"t": 0, "y": 1090}], d, 640)],
             cam(1.3, 1.0, (540, 1200), (540, 1000)), "desenfoque", sfx=[(0.1, "agua", -22)])


@v.plano(84, "ciento veinte mil kilómetros")
def _(d):
    return P(ESPACIO, [BG("bg_esp_petroleo"), estrellas(30, 7), IMG("banera", ancho=1060, x=540, y=1100, z=0.3),
             IMG("saturno", ancho=560, x=540, y=1000, z=0.4, anim={"flotar": [6, 1.4]}),
             IMG("agua_frente", ancho=930, x=540, y=1070, z=0.5, op=0.75),
             tierra(160, 560, 70, z=0.5, giro=10), flecha([[60, 760], [1020, 760]], 0.1, d * 0.7, AMBAR, 7, [16, 12])],
             cam(1.0, 1.04), hud=[contador(0.1, d - 0.05, 0, 120000, d * 0.6, "KM", tam=120, y=560, borde=AMBAR)])


@v.plano(89, "gira muy rápido")
def _(d):
    return P(ESPACIO, [BG("bg_esp_violeta"), estrellas(30, 8),
             {"tipo": "esfera", "radio": 330, "textura": "bandas", "color": "#e8c88a", "color2": "#a87a44", "x": 540, "y": 960, "z": 0.5, "giro": 160},
             *lineas_vel(900, 900, 2, "#f6e2b0aa"), *lineas_vel(900, 1040, 3, "#f6e2b0aa")],
             cam(1.0, 1.08), "zoom", sfx=[(0.05, "whoosh", -14, {"dur": d})])


@v.plano(95, "su día: diez horas y media")
def _(d):
    return P(ESPACIO, [BG("bg_esp_violeta"), estrellas(20, 9), IMG("saturno", ancho=560, x=760, y=560, z=0.4, anim={"flotar": [6, 1.6]}),
             *reloj(430, 1080, 560, 0, 0, 10, 30, 0.05, d * 0.8, z=0.6)],
             cam(1.0, 1.05, (540, 960), (500, 1000)), hud=[rotulo(d * 0.5, d - 0.05, "10,5 H", tam=110, color=AMBAR, capsula="#0d1330d8", x=760, y=900)],
             sfx=[(0.1, "tictac", -16, {"dur": d * 0.75, "ritmo": 0.12})])


@v.plano(102, "sus anillos")
def _(d):
    return P(ESPACIO, [BG("bg_esp_petroleo"), estrellas(25, 10), IMG("saturno", ancho=2600, x=760, y=960, z=0.4, rot=-6),
             senala(170, 1130, d * 0.3, d - 0.05, 140, CIAN)],
             cam(1.0, 1.1, (540, 960), (420, 1050)), "zoom", hud=[rotulo(0.1, d - 0.05, "ANILLOS", tam=96, color=CIAN, capsula="#0d1330e6", y=560)])


@v.plano(105, "hielo y roca")
def _(d):
    rocas = [IMG(n, ancho=a, x=x, y=y, z=z, anim={"girar": g, "flotar": [10, 1.3 + k * 0.2]}, keys=aparece(k * 0.15, 0.35))
             for k, (n, a, x, y, z, g) in enumerate([("hielo1", 420, 330, 900, 0.5, 8), ("hielo2", 300, 790, 760, 0.45, -10), ("hielo3", 240, 760, 1250, 0.55, 12),
                                                    ("hielo2", 160, 200, 1300, 0.4, -6), ("hielo1", 120, 600, 520, 0.35, 9)])]
    return P(ESPACIO, [BG("bg_esp_petroleo"), polvo("#dff6ff", 50, (0, 300, 1080, 1500), 11), *rocas],
             cam(1.0, 1.08), hud=[rotulo(0.3, d - 0.05, "HIELO Y ROCA", tam=90, color="#ffffff", capsula="#0d1330d8", borde=CIAN, y=1360)],
             sfx=[(k * 0.15, "pop", -22) for k in range(5)])


@v.plano(110, "grandes como una casa")
def _(d):
    return P(ESPACIO, [BG("bg_esp_petroleo"), polvo("#dff6ff", 40, (0, 300, 1080, 1500), 12),
             IMG("hielo1", ancho=620, x=340, y=980, z=0.5, anim={"girar": 4}),
             IMG("casa", ancho=360, x=820, y=1050, z=0.55, keys=aparece(d * 0.3, 0.4))],
             cam(1.0, 1.05), "desenfoque", hud=[amarillo(d * 0.15, d - 0.02, "COMO UNA CASA", y=560, color=AMBAR, tam=84)])


@v.plano(115, "cientos de miles de kilómetros")
def _(d):
    return P(ESPACIO, [BG("bg_esp_ambar"), estrellas(30, 13), IMG("saturno", ancho=1060, x=540, y=960, z=0.5, rot=-4),
             flecha([[60, 1180], [1020, 1050]], 0.1, d * 0.6, CIAN, 7), flecha([[1020, 1050], [60, 1180]], 0.1, d * 0.6, CIAN, 7)],
             cam(1.08, 1.0), hud=[rotulo(d * 0.3, d - 0.05, "CIENTOS DE MILES DE KM", tam=64, color="#ffffff", capsula="#0d1330d8", borde=CIAN, y=520)])


@v.plano(126, "solo diez metros de grosor")
def _(d):
    # el anillo visto de canto: una línea finísima; al lado, un edificio de tres pisos
    return P(ESPACIO, [BG("bg_esp_petroleo"), estrellas(20, 14),
             {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 16, "relleno": ["#f6e2b0", "#c8b48a"], "x": 540, "y": 1000, "z": 0.45,
              "keys": [{"t": 0, "ey": 8}, {"t": d * 0.45, "ey": 1, "ease": "salida"}]},
             IMG("edificio", ancho=180, x=760, y=900, z=0.5, keys=aparece(d * 0.5, 0.35)),
             flecha([[920, 840], [920, 980]], d * 0.55, d * 0.85, LIMA, 6)],
             cam(1.0, 1.15, (540, 1000), (700, 950)), "zoom",
             hud=[contador(d * 0.45, d - 0.05, 0, 10, d * 0.3, "METROS", tam=120, y=560, borde=LIMA)], sfx=[(d * 0.45, "impacto", -12)], energia=0.9)


@v.plano(135, "no lo intentes")
def _(d):
    return P(BANO, [*banera_con([{"t": 0, "y": 600}, {"t": d, "y": 700, "ease": "suave"}], d, 620)],
             cam(1.0, 1.05, (540, 1000), (540, 980)), "desenfoque", hud=[rotulo(0.1, d - 0.05, "NO LO INTENTES", tam=90, color="#ffffff", capsula="#c0392be6", y=1300)],
             energia=0.4)


@v.plano(139, "Saturno no tiene suelo")
def _(d):
    return P(ESPACIO, [BG("bg_esp_violeta"), estrellas(20, 15),
             {"tipo": "esfera", "radio": 420, "textura": "bandas", "color": "#e8c88a", "color2": "#a87a44", "x": 540, "y": 1000, "z": 0.4, "giro": 20},
             brillo(540, 1000, 260, "#ffcf6a", 0.6, 0.45, pulso=[0.15, 0.6]),
             flecha([[540, 520], [540, 1000]], 0.1, d * 0.7, MAGENTA, 8, [18, 12])],
             cam(1.0, 1.2, (540, 900), (540, 1000)), "zoom", hud=[amarillo(0.15, d - 0.05, "SIN SUELO", y=1360, color=MAGENTA)])


@v.plano(143, "el gas se mezcla con el agua")
def _(d):
    return P(BANO, [*banera_con([{"t": 0, "y": 1090, "op": 1, "escala": 1.0}, {"t": d, "y": 1140, "op": 0.25, "escala": 1.15, "ease": "suave"}], d, 640, gas=True)],
             cam(1.05, 1.2, (540, 1150), (540, 1200)), sfx=[(0.1, "agua", -16), (0.3, "rumor", -18, {"dur": d})])


@v.plano(151, "¿qué planeta comparamos? (cierre en bucle)")
def _(d):
    return P(BANO, [*banera_con([{"t": 0, "y": 700}, {"t": d, "y": 520, "ease": "suave"}], d, 600)],
             cam(1.1, 1.0, (540, 1100), (540, 1000)), "desenfoque", hud=[rotulo(0.1, d - 0.05, "¿CUÁL SIGUE?", tam=100, color=CIAN, capsula="#0d1330d8", y=1300)])


# ------------------------------------------------------------------ micro planos (golpes de 0,4–0,7 s)
def micro_cerca(svg, ancho, x, y, fondo, color, anim=None, sfx="tic", db=-20, extra=(), bg=None):
    def fn(d):
        return P(fondo, [*([BG(bg)] if bg else []), brillo(540, 960, 520, color, 0.45, pulso=[0.2, 0.2]), IMG(svg, ancho=ancho, x=x, y=y, z=0.5, anim=anim or {"flotar": [10, 0.5]},
                 keys=[{"t": 0, "escala": 0.92}, {"t": d, "escala": 1.06, "ease": "salida"}]), *extra],
                 cam(1.0, 1.1), "corte", sfx=[(0.02, sfx, db)])
    return fn


v.plano(9, "micro: onda en el agua")(lambda d: P(BANO, [*azulejos(), IMG("agua_frente", ancho=2400, x=540, y=1100, z=0.4, anim={"flotar": [20, 0.4]}),
                                                     brillo(540, 1060, 300, "#dff6ff", 0.6, 0.5, pulso=[0.3, 0.2])], cam(1.0, 1.1), "corte", sfx=[(0.02, "agua", -18)]))
v.plano(17, "micro: único", mas=0.1)(micro_cerca("saturno", 1500, 540, 960, ESPACIO, "#ffcf6a", sfx="brillo", db=-18, bg="bg_esp_violeta"))
v.plano(27, "micro: un gramo", mas=0.15)(micro_cerca("cubo_agua", 900, 540, 1000, ["#0a2030", "#04101a"], "#7fd4ff", sfx="ding", db=-18))
v.plano(36, "micro: de media", mas=0.1)(micro_cerca("cubo_saturno", 1100, 540, 1000, ["#1a1408", "#0a0804"], "#f0d8a0", anim={"balanceo": [6, 0.1]}, sfx="tic"))
v.plano(46, "micro: gigante (las bandas)", mas=0.4)(lambda d: P(ESPACIO, [{"tipo": "esfera", "radio": 1100, "textura": "bandas", "color": "#e8c88a", "color2": "#a87a44",
                                                      "x": 540, "y": 1500, "z": 0.4, "giro": 30}], cam(1.0, 1.08), "corte", sfx=[(0.02, "rumor", -16, {"dur": d})]))
v.plano(60, "micro: la Tierra, aplastada", mas=0.25)(lambda d: P(ESPACIO, [BG("bg_esp_ambar"), tierra(540, 1000, 500, keys=[{"t": 0, "ey": 1.0}, {"t": d * 0.4, "ey": 0.7, "ex": 1.2, "ease": "golpe"}, {"t": d, "ey": 0.8, "ex": 1.1}])],
                                                      cam(1.0, 1.08), "corte", sfx=[(d * 0.3, "golpe", -16)]))
v.plano(76, "micro: un globo que sube", mas=0.35)(micro_cerca("atomo_h", 900, 540, 960, ["#0a0618", "#04020c"], "#ff3df2", anim={"girar": 80}, sfx="subida", db=-20))
v.plano(101, "micro: la aguja corre", mas=0.2)(lambda d: P(["#1b2236", "#0b0f1c"], [brillo(540, 1000, 700, "#ffcf6a", 0.3), *cronometro(0, 540, 0, d)], cam(1.2, 1.3, (540, 1050), (540, 1050)), "corte",
                                                       sfx=[(0.0, "tictac", -16, {"dur": d, "ritmo": 0.08})]))
v.plano(114, "micro: la casa", mas=0.2)(micro_cerca("casa", 900, 540, 1000, ESPACIO, "#ffcf6a", sfx="pop", db=-18, bg="bg_esp_petroleo"))
v.plano(134, "micro: el anillo, de canto", mas=0.3)(lambda d: P(ESPACIO, [BG("bg_esp_petroleo"), {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 30, "relleno": ["#f6e2b0", "#c8b48a"], "x": 540, "y": 960, "z": 0.45},
                                                          IMG("edificio", ancho=420, x=540, y=780, z=0.5)], cam(1.0, 1.1), "corte", sfx=[(0.02, "tic", -18)]))
v.plano(150, "micro: se mezcla", mas=0.1)(micro_cerca("nube_gas", 1300, 540, 1000, BANO, "#f0d8a0", anim={"pulso": [0.1, 0.3]}, sfx="agua", db=-18))


v.construir("2026-11-17-manana-02-saturno-flotaria", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 7, "db": -13},
            claves=["Saturno", "flotaría", "agua", "gramo", "sesenta", "nueve", "noventa", "hidrógeno", "helio", "anillos", "diez", "metros"])
