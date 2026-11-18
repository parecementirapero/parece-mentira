"""02 · Este terrón pesa una montaña (estrella de neutrones) — método denso. Lote 2026-11-18-tarde, Agente 20:00 (Jorge).
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import math, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_tarde  # noqa: E402

SVG = ilus_tarde.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

OSC = ["#02030a", "#0a1030"]
COCINA = ["#2a2d3a", "#14161e"]


def estrella_n(x, y, r, z=0.45, keys=None, giro=200, haces=True, t_haz=0.0):
    """Estrella de neutrones: bola blanca-azul que gira muy deprisa, halo y dos haces de luz (púlsar)."""
    e = [brillo(x, y, r * 3.2, "#7df9ff", 0.55, z - 0.02, pulso=[0.15, 0.25], keys=keys),
         {"tipo": "esfera", "radio": r, "textura": "crateres", "color": "#eaf6ff", "color2": "#6aa8ff", "giro": giro, "x": x, "y": y, "z": z,
          "luz": [-0.4, -0.4], "halo": "#7df9ff", "semilla": 9, **({"keys": keys} if keys else {})}]
    if haces:
        e.insert(0, {"tipo": "rayos", "n": 2, "longitud": 1400, "apertura": 7, "color": "#bff6ffaa", "x": x, "y": y, "z": z - 0.03,
                     "anim": {"girar": 260}, "keys": [{"t": 0, "op": 0}, {"t": t_haz + 0.01, "op": 0}, {"t": t_haz + 0.2, "op": 1}]})
    return e


def balanza(d, ang0, ang1, t_inc, izq, der, ancho_izq=200, ancho_der=320):
    """Báscula de dos platos (biblioteca v4): la viga pasa de ang0 a ang1 con rebote en t_inc; un objeto encima de cada plato."""
    PX, PY, L = 540, 930, 360

    def ends(th):
        r = math.radians(th)
        return (PX - L * math.cos(r), PY + L * math.sin(r)), (PX + L * math.cos(r), PY - L * math.sin(r))

    def ang(t):
        if t <= t_inc: return ang0
        u = min((t - t_inc) / 0.8, 1); c1, c3 = 1.70158, 2.70158
        return ang0 + (ang1 - ang0) * (1 + c3 * (u - 1) ** 3 + c1 * (u - 1) ** 2)
    ts = [0, t_inc] + [t_inc + 0.05 * i for i in range(1, 17)] + [max(d, t_inc + 0.9)]
    kv, ki, kd, oi, od = [], [], [], [], []
    for t in ts:
        th = ang(t); (lx, ly), (rx, ry) = ends(th)
        kv.append({"t": round(t, 3), "rot": round(-th, 3), "ease": "lineal"})
        ki.append({"t": round(t, 3), "x": round(lx, 1), "y": round(ly + 200, 1), "ease": "lineal"})
        kd.append({"t": round(t, 3), "x": round(rx, 1), "y": round(ry + 200, 1), "ease": "lineal"})
        oi.append({"t": round(t, 3), "x": round(lx, 1), "y": round(ly + 345 - ancho_izq * 0.4, 1), "ease": "lineal"})
        od.append({"t": round(t, 3), "x": round(rx, 1), "y": round(ry + 345 - ancho_der * 0.4, 1), "ease": "lineal"})
    return [IMG("balanza_base", ancho=800, x=540, y=1260, z=0.5),
            IMG("plato_vacio", ancho=320, z=0.51, keys=ki), IMG("plato_vacio", ancho=320, z=0.51, keys=kd),
            IMG(izq, ancho=ancho_izq, z=0.52, keys=oi), IMG(der, ancho=ancho_der, z=0.52, keys=od),
            IMG("balanza_viga", ancho=800, x=PX, y=PY, z=0.53, keys=kv)]


# ================================================================== PLANOS
@v.plano(0, "gancho: el terrón brillante cae y revienta la báscula")
def _(d):
    return P(COCINA, [brillo(540, 900, 700, "#2ff3ff", 0.25, 0.1),
             IMG("bascula_rota", ancho=760, x=540, y=1450, z=0.5, keys=[{"t": 0, "ey": 1}, {"t": d * 0.45, "ey": 1}, {"t": d * 0.5, "ey": 0.85}, {"t": d * 0.6, "ey": 1}]),
             IMG("terron", ancho=420, z=0.6, keys=[{"t": 0, "x": 540, "y": 500, "rot": -25}, {"t": d * 0.45, "x": 540, "y": 1270, "rot": 0, "ease": "entrada"},
                                                   {"t": d, "x": 540, "y": 1300}]),
             polvo("#bff6ff", 40, (300, 1300, 780, 1500), 3, "chispas")],
             cam(1.0, 1.0, (540, 1000), (540, 1150), temblor=0), vineta=0.6,
             sfx=[(0.02, "whoosh", -12, {"dur": 0.6}), (0.45 * 1.2, "impacto", -12)])


@v.plano(3, "micro: la montaña", mas=0.05)
def _(d):
    return P(["#2a2050", "#8a7aa8"], [brillo(540, 600, 700, "#ffd8a0", 0.4, 0.05), IMG("montana", ancho=1300, x=540, y=1350, z=0.4, keys=late(0.0, 1, 0.04, 0.3))],
             cam(1.0, 1.08, (540, 1200)), "corte", sfx=[(0.02, "golpe", -14)])


@v.plano(5, "no es azúcar: terrón normal frente al brillante")
def _(d):
    return P(COCINA, [IMG("terron_normal", ancho=320, x=300, y=1150, z=0.5, keys=aparece(0.0, 0.3)),
             IMG("terron", ancho=380, x=760, y=1130, z=0.5, keys=aparece(0.15, 0.3), anim={"flotar": [10, 1.4]}),
             {"tipo": "forma", "forma": "rect", "ancho": 360, "alto": 22, "relleno": "#ff2d55", "x": 300, "y": 1150, "z": 0.6, "rot": -35,
              "keys": [{"t": 0, "op": 0}, {"t": d * 0.4, "op": 0}, {"t": d * 0.5, "op": 1}]}],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "NO ES AZÚCAR", y=560, tam=100, color=MAGENTA)], sfx=[(d * 0.45, "zap", -18)])


@v.plano(8, "un trocito de estrella de neutrones: la estrella gira en el espacio")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), *estrella_n(540, 1050, 210, 0.45, t_haz=0.2),
             IMG("terron", ancho=200, z=0.6, keys=[{"t": 0, "x": 540, "y": 1050, "op": 0}, {"t": 0.2, "op": 1}, {"t": d, "x": 860, "y": 1500, "ease": "salida"}])],
             cam(1.0, 1.08, (540, 1050)), "zoom", hud=[contexto(0.05, d - 0.05, "ESTRELLA DE NEUTRONES")], sfx=[(0.2, "brillo", -16)])


@v.plano(15, "¿cómo puede pesar tanto? la balanza se vuelca")
def _(d):
    return P(["#0d1324", "#1f2b48"], [brillo(540, 700, 700, "#bff6ff", 0.25, 0.05), *balanza(d, 0, -16, d * 0.25, "terron", "terron_normal", 230, 230)],
             cam(1.0, 1.05, (540, 1050)), "desenfoque", hud=[amarillo(0.05, d - 0.03, "¿CÓMO?", y=560, tam=130, color=CIAN)], sfx=[(d * 0.25, "golpe", -14)])


@v.plano(19, "estrella gigante que se queda sin combustible")
def _(d):
    return P(["#1a0505", "#3a0a10"], [BG("bg_esp_ambar"),
             {"tipo": "esfera", "radio": 420, "textura": "sol", "color": "#ffb46a", "color2": "#c02a1a", "giro": 6, "x": 540, "y": 1050, "z": 0.4, "luz": [0, 0],
              "keys": [{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.06}], "anim": {"pulso": [0.03, 0.8]}},
             brillo(540, 1050, 700, "#ff6a2a", 0.4, 0.38, pulso=[0.2, 0.8])],
             cam(1.0, 1.04), "corte", hud=[contexto(0.05, d - 0.05, "ESTRELLA GIGANTE")], sfx=[(0.1, "rumor", -18)])


@v.plano(27, "su centro se hunde de golpe: colapso y destello")
def _(d):
    return P(["#1a0505", "#02030a"], [BG("bg_esp_ambar"),
             {"tipo": "esfera", "radio": 420, "textura": "sol", "color": "#ffb46a", "color2": "#c02a1a", "giro": 6, "x": 540, "y": 1050, "z": 0.4, "luz": [0, 0],
              "keys": [{"t": 0, "escala": 1.06}, {"t": d * 0.55, "escala": 0.05, "ease": "entrada"}, {"t": d * 0.6, "op": 0}]},
             *estrella_n(540, 1050, 60, 0.45, keys=[{"t": 0, "op": 0}, {"t": d * 0.55, "op": 0}, {"t": d * 0.6, "op": 1}], haces=False),
             {"tipo": "rayos", "n": 22, "longitud": 1300, "apertura": 5, "color": "#fff4d0cc", "x": 540, "y": 1050, "z": 0.5,
              "keys": [{"t": 0, "op": 0}, {"t": d * 0.55, "op": 0}, {"t": d * 0.62, "op": 1, "escala": 0.3}, {"t": d, "op": 0, "escala": 1.4}]},
             fundido_blanco([{"t": 0, "op": 0}, {"t": d * 0.55, "op": 0}, {"t": d * 0.62, "op": 0.85}, {"t": d, "op": 0}])],
             cam(1.0, 1.1, temblor=4), "corte", sfx=[(d * 0.55, "impacto", -12)])


@v.plano(33, "los átomos se aplastan")
def _(d):
    return P(["#0d1324", "#1f2b48"], [BG("bg_esp_violeta"),
             IMG("atomo", ancho=760, x=540, y=1050, z=0.5, keys=[{"t": 0, "ex": 1.0, "ey": 1.0}, {"t": d * 0.8, "ex": 0.45, "ey": 0.45, "ease": "entrada"}], anim={"girar": 30}),
             flecha([[100, 1050], [330, 1050]], 0.0, d * 0.6, MAGENTA, 12, z=0.6), flecha([[980, 1050], [750, 1050]], 0.0, d * 0.6, MAGENTA, 12, z=0.6),
             flecha([[540, 450], [540, 700]], 0.0, d * 0.6, MAGENTA, 12, z=0.6), flecha([[540, 1650], [540, 1400]], 0.0, d * 0.6, MAGENTA, 12, z=0.6)],
             cam(1.0, 1.06), "corte", sfx=[(0.1, "subida", -18, {"dur": d * 0.7})])


@v.plano(37, "solo quedan neutrones, pegados")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), IMG("bola_neutrones", ancho=820, x=540, y=1050, z=0.5, keys=[{"t": 0, "escala": 1.2}, {"t": d * 0.6, "escala": 1.0, "ease": "salida"}], anim={"girar": 8})],
             cam(1.0, 1.06), "desenfoque", hud=[amarillo(0.05, d - 0.03, "NEUTRONES", y=560, tam=110, color=CIAN)], sfx=[(0.1, "burbuja", -18)])


@v.plano(46, "más masa que el Sol: el Sol entero se encoge")
def _(d):
    return P(OSC, [BG("bg_esp_ambar"), *[{**s, "keys": [{"t": 0, "escala": 1.0}, {"t": d * 0.8, "escala": 0.12, "ease": "entrada"}]} for s in sol(540, 1050, 380, 0.4)],
             flecha([[540, 520], [540, 780]], 0.1, d * 0.6, AMBAR, 10, z=0.6), flecha([[540, 1580], [540, 1320]], 0.1, d * 0.6, AMBAR, 10, z=0.6)],
             cam(1.0, 1.05), "corte", hud=[rotulo(0.05, d - 0.05, "MÁS QUE EL SOL", tam=90, color="#141414", capsula="#ffe93de6", y=560)],
             sfx=[(0.1, "subida", -18, {"dur": d * 0.7})])


@v.plano(53, "metida en una bola de veinte kilómetros")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), *estrella_n(540, 1100, 230, 0.45, haces=False),
             flecha([[310, 1420], [770, 1420]], 0.1, d * 0.6, LIMA, 8, z=0.6)],
             cam(1.0, 1.05), "corte", hud=[contador(0.05, d - 0.05, 0, 20, d * 0.6, "KM", tam=140, y=560, borde=LIMA, miles=False)],
             sfx=[(0.1, "subida", -20, {"dur": d * 0.6})])


@v.plano(61, "el tamaño de una ciudad")
def _(d):
    return P(["#0a0620", "#2a0f4a"], [BG("bg_ciudad_noche"), IMG("mapa_ciudad", ancho=900, x=540, y=1100, z=0.4, op=0.85),
             *estrella_n(540, 1100, 330, 0.5, keys=[{"t": 0, "op": 0}, {"t": d * 0.4, "op": 0.75}], haces=False)],
             cam(1.0, 1.05), "desenfoque", hud=[contexto(0.05, d - 0.05, "TAMAÑO DE UNA CIUDAD")], sfx=[(0.1, "brillo", -20)])


@v.plano(66, "un terrón de su materia en la Tierra")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), tierra(540, 1450, 900, 0.4, 3),
             IMG("terron", ancho=300, z=0.6, keys=[{"t": 0, "x": 540, "y": 300, "rot": -20}, {"t": d * 0.8, "x": 540, "y": 920, "rot": 0, "ease": "entrada"}])],
             cam(1.0, 1.05), "corte", sfx=[(0.1, "whoosh", -14, {"dur": d * 0.8})])


@v.plano(77, "mil millones de toneladas")
def _(d):
    return P(COCINA, [IMG("terron", ancho=520, x=540, y=1150, z=0.5, keys=late(0.1, 2, 0.06, 0.35)), polvo("#bff6ff", 40, (200, 900, 880, 1400), 8, "chispas")],
             cam(1.0, 1.06, (540, 1100)), "corte",
             hud=[contador(0.05, d - 0.05, 0, 1000, d * 0.6, "MILLONES DE T", tam=130, y=560, borde=CIAN)], sfx=[(0.05, "subida", -18, {"dur": d * 0.6})])


@v.plano(82, "lo mismo que una montaña: la balanza se equilibra")
def _(d):
    return P(["#2a2050", "#8a7aa8"], [brillo(540, 600, 700, "#ffd8a0", 0.3, 0.05), *balanza(d, 18, 0, d * 0.3, "terron", "montana", 200, 420)],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[rotulo(d * 0.35, d - 0.05, "=", tam=200, color="#ffffff", capsula=None, y=560)],
             sfx=[(d * 0.3, "golpe", -14), (d * 0.6, "ding", -18)])


@v.plano(84, "¿y lo más loco? gira: haces del púlsar")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), *estrella_n(540, 1050, 170, 0.45, t_haz=0.0)],
             cam(1.0, 1.08), "zoom", hud=[amarillo(0.05, d - 0.03, "GIRA", y=560, tam=140, color=LIMA)], sfx=[(0.05, "senal", -20), (d * 0.5, "senal", -22)])


@v.plano(89, "setecientas dieciséis vueltas por segundo")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), *estrella_n(540, 1150, 150, 0.45, giro=900), *lineas_vel(540, 1150, 4, "#7df9ffaa")],
             cam(1.0, 1.06), "corte",
             hud=[contador(0.05, d - 0.05, 0, 716, d * 0.6, "VUELTAS/S", tam=140, y=560, borde=CIAN, miles=False)], sfx=[(0.05, "subida", -18, {"dur": d * 0.6})])


@v.plano(100, "más deprisa que una batidora")
def _(d):
    return P(COCINA, [brillo(540, 900, 600, "#ff7aa8", 0.3, 0.1), IMG("batidora", ancho=440, x=360, y=1150, z=0.5, anim={"balanceo": [2, 0.08]}),
             *estrella_n(820, 1000, 110, 0.5, giro=900, t_haz=0.0)],
             cam(1.0, 1.05), "corte", hud=[rotulo(0.05, d - 0.05, "MÁS RÁPIDO", tam=90, color="#141414", capsula="#7dff3ae6", y=560)], sfx=[(0.05, "rumor", -18)])


@v.plano(105, "un malvavisco cae hacia la estrella")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), *estrella_n(540, 1550, 260, 0.45, haces=False),
             IMG("malvavisco", ancho=220, z=0.6, keys=[{"t": 0, "x": 540, "y": 250, "rot": 0}, {"t": d, "x": 540, "y": 1180, "rot": 200, "ease": "entrada"}]),
             flecha([[540, 300], [540, 1100]], 0.0, d * 0.9, CIAN, 6, disc=[20, 18], z=0.55)],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[contexto(0.05, d - 0.05, "UN MALVAVISCO")], sfx=[(0.05, "fugaz", -18)])


@v.plano(117, "golpe: mil bombas de hidrógeno")
def _(d):
    return P(["#1a0505", "#02030a"], [IMG("bomba_flash", ancho=900, x=540, y=1200, z=0.5, keys=[{"t": 0, "escala": 0.3, "op": 0}, {"t": 0.25, "escala": 1.0, "op": 1, "ease": "salida"}]),
             polvo("#ffd06a", 70, (100, 700, 980, 1600), 19, "chispas"),
             fundido_blanco([{"t": 0, "op": 0.9}, {"t": 0.3, "op": 0}])],
             cam(1.0, 1.08, temblor=6), "corte",
             hud=[contador(0.05, d - 0.05, 0, 1000, d * 0.5, "BOMBAS H", tam=130, y=560, borde=AMBAR)], sfx=[(0.02, "impacto", -12)])


@v.plano(126, "1967: campo de antenas al amanecer")
def _(d):
    return P(["#1a2a4a", "#6a7aa8"], [BG("bg_antenas"), fugaz(0.2, 100, 300, 500, 450), polvo("#ffffff", 20, (0, 200, 1080, 900), 5, "estrellas")],
             cam(1.0, 1.08, (540, 1200), (540, 1150)), "desenfoque", hud=[contexto(0.05, d - 0.05, "1967 · CAMBRIDGE")], sfx=[(0.1, "brillo", -20)])


@v.plano(136, "Jocelyn Bell, una estudiante: la tira de papel")
def _(d):
    return P(["#f4ecd8", "#c8b898"], [IMG("papel_registro", ancho=1600, z=0.5, y=1100, keys=[{"t": 0, "x": 900}, {"t": d, "x": 300, "ease": "lineal"}]),
             IMG("lupa", ancho=380, x=600, y=1150, z=0.6, anim={"flotar": [10, 1.5]})],
             cam(1.0, 1.04), "corte", hud=[rotulo(0.05, d - 0.05, "JOCELYN BELL", tam=90, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.1, "roce", -20)])


@v.plano(140, "su señal era tan regular: pulsos que se repiten")
def _(d):
    return P(["#0d1324", "#1f2b48"], [IMG("papel_registro", ancho=1900, z=0.5, y=1100, keys=[{"t": 0, "x": 700}, {"t": d, "x": 380, "ease": "lineal"}]),
             senala(540, 950, 0.1, d - 0.05, 90, CIAN)],
             cam(1.0, 1.06), "corte", hud=[amarillo(0.05, d - 0.03, "TAN REGULAR", y=560, tam=100, color=CIAN)],
             sfx=[(0.05 + k * 0.45, "senal", -22) for k in range(int(d / 0.45))])


@v.plano(147, "la apodaron hombrecillos verdes: LGM-1")
def _(d):
    return P(OSC, [BG("bg_antenas"), brillo(540, 900, 600, "#7dff3a", 0.35, 0.3, pulso=[0.2, 0.45])],
             cam(1.0, 1.05), "corte", hud=[rotulo(0.05, d - 0.05, "LGM-1", tam=160, color="#141414", capsula="#7dff3ae6", y=700),
                                           amarillo(0.05, d - 0.03, "«LITTLE GREEN MEN»", y=1000, tam=70, color=LIMA)], sfx=[(0.1, "senal", -20)])


@v.plano(150, "¿te comerías ese terrón? (bucle)")
def _(d):
    return P(COCINA, [brillo(540, 900, 700, "#2ff3ff", 0.25, 0.1), IMG("terron", ancho=460, x=540, y=1050, z=0.6, anim={"flotar": [14, 1.6], "balanceo": [6, 2]}),
             polvo("#bff6ff", 30, (300, 800, 780, 1300), 3, "chispas")],
             cam(1.0, 1.05, (540, 1050), (540, 1000)), "desenfoque", hud=[amarillo(0.05, d - 0.4, "¿TE LO COMES?", y=560, tam=100, color=CIAN)], sfx=[(0.1, "pop", -16)])


# ------------------------------------------------------------------ micro planos
@v.plano(13, "micro: la superficie de la estrella de cerca", mas=0.05)
def _(d):
    return P(OSC, [*estrella_n(540, 1700, 1000, 0.4, giro=60, haces=False)], cam(1.0, 1.1, (540, 960)), "corte", sfx=[(0.02, "brillo", -18)])


@v.plano(31, "micro: destello del colapso", mas=0.05)
def _(d):
    return P(["#ffffff", "#bff6ff"], [{"tipo": "rayos", "n": 30, "longitud": 1400, "apertura": 4, "color": "#2ff3ffaa", "x": 540, "y": 960, "z": 0.4, "anim": {"girar": 60}}],
             cam(1.0, 1.15, temblor=8), "corte", sfx=[(0.02, "golpe", -12)])


@v.plano(42, "micro: dos neutrones chocan", mas=0.0)
def _(d):
    return P(OSC, [IMG("bola_neutrones", ancho=2400, x=540, y=960, z=0.5)], cam(1.0, 1.12, temblor=3), "corte", sfx=[(0.02, "pop", -18)])


@v.plano(59, "micro: regla de 20 km", mas=0.05)
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), IMG("regla", ancho=900, x=540, y=1100, z=0.5, rot=-90, keys=aparece(0.0, 0.2))],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "tic", -18)])


@v.plano(75, "micro: la Tierra tira del terrón", mas=0.05)
def _(d):
    return P(OSC, [tierra(540, 1500, 1500, 0.4, 5), IMG("terron", ancho=360, x=540, y=600, z=0.6, keys=[{"t": 0, "y": 500}, {"t": d, "y": 760, "ease": "entrada"}])],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "whoosh", -16, {"dur": 0.4})])


@v.plano(98, "micro: haces que barren la pantalla", mas=0.05)
def _(d):
    return P(OSC, [{"tipo": "rayos", "n": 2, "longitud": 1600, "apertura": 10, "color": "#bff6ffcc", "x": 540, "y": 960, "z": 0.4, "anim": {"girar": 600}},
                   brillo(540, 960, 200, "#ffffff", 0.9, 0.5)], cam(1.0, 1.1), "corte", sfx=[(0.02, "zap", -18)])


@v.plano(103, "micro: cuchillas de la batidora", mas=0.05)
def _(d):
    return P(COCINA, [brillo(540, 1000, 500, "#ff7aa8", 0.4, 0.1), IMG("batidora", ancho=700, x=540, y=1100, z=0.5, anim={"balanceo": [3, 0.06]}),
                      polvo("#ff9ac0", 50, (300, 700, 780, 1100), 31, "chispas")], cam(1.0, 1.12, (540, 1000), temblor=5), "corte",
             sfx=[(0.02, "rumor", -18)])


@v.plano(115, "micro: el malvavisco a punto de tocar", mas=0.05)
def _(d):
    return P(OSC, [*estrella_n(540, 2100, 900, 0.4, haces=False), IMG("malvavisco", ancho=500, x=540, y=900, z=0.6, keys=[{"t": 0, "y": 700}, {"t": d, "y": 1000, "ease": "entrada"}])],
             cam(1.0, 1.1, temblor=3), "corte", sfx=[(0.02, "whoosh", -14, {"dur": 0.3})])


@v.plano(133, "micro: un pulso en la tira", mas=0.05)
def _(d):
    return P(["#f4ecd8", "#c8b898"], [IMG("papel_registro", ancho=3200, x=540, y=1000, z=0.5)], cam(1.0, 1.1), "corte", sfx=[(0.02, "senal", -20)])


v.construir("2026-11-18-tarde-02-terron-estrella-neutrones", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 62, "db": -13},
            claves=["montaña", "azúcar", "neutrones", "gigante", "golpe", "aplastan", "Sol", "veinte", "ciudad", "toneladas", "Gira", "setecientas", "batidora", "malvavisco", "mil", "Jocelyn", "verdes"])
