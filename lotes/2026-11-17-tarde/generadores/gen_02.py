"""02 · Ese Sol ya es pasado (la luz del Sol llega con retraso) — método denso. Lote 2026-11-17-tarde, Agente 20:00 (Jorge).
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_tarde  # noqa: E402

SVG = ilus_tarde.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

DENTRO = ["#3a0a00", "#1a0400"]


def sol_k(x, y, r, keys=None, z=0.3, giro=6):
    """Sol esférico con halo que acepta claves de movimiento (para el primer plano)."""
    h = brillo(x, y, r * 3.2, "#ffcf6a", 0.55, z - 0.01, pulso=[0.06, 2.0])
    s = {"tipo": "esfera", "radio": r, "textura": "sol", "color": "#fff3b0", "color2": "#ffb02e", "giro": giro, "x": x, "y": y, "z": z, "luz": [0, 0]}
    if keys:
        h["keys"] = [{k2: v2 for k2, v2 in k.items() if k2 in ("t", "x", "y", "ease")} for k in keys]
        s["keys"] = keys
    return [h, s]


def foton(x, y, z=0.7, ancho=120, keys=None):
    return IMG("foton", ancho=ancho, x=x, y=y, z=z, keys=keys or [], anim={"pulso": [0.12, 0.3]})


def zigzag(cx, cy, r, n, sem):
    import random
    rr = random.Random(sem)
    pts, x, y = [[cx, cy]], cx, cy
    for _ in range(n):
        x = min(max(x + rr.uniform(-r, r), cx - 2.4 * r), cx + 2.4 * r)
        y = min(max(y + rr.uniform(-r, r), cy - 2.4 * r), cy + 2.4 * r)
        pts.append([round(x), round(y)])
    return pts


# ================================================================== PLANOS
@v.plano(0, "gancho: el Sol sube con un reloj que va atrasado")
def _(d):
    return P(ESPACIO, [BG("bg_esp_ambar"), estrellas(40, 4),
             *sol_k(540, 1050, 380, keys=arranque(540, 1050, d, "abajo", 320, 40)),
             *reloj(840, 1500, 300, 12, 0, 11, 52, 0, d, z=0.7), fugaz(0.2, 100, 300, 500, 520)],
             cam(1.08, 1.0, (540, 1050), (540, 1000)), vineta=0.6, sfx=[(0.0, "subida", -14, {"dur": 0.6}), (0.4, "golpe", -16), (0.1, "tictac", -22, {"dur": d})])


@v.plano(5, "lo ves con retraso")
def _(d):
    return P(ESPACIO, [BG("bg_esp_petroleo"), *sol(220, 900, 150), tierra(900, 1000, 220, giro=8),
             flecha([[400, 920], [760, 990]], 0.05, d * 0.9, AMBAR, 8, [18, 14])],
             cam(1.0, 1.05, (540, 960), (560, 960)), "desenfoque", hud=[amarillo(0.1, d - 0.05, "CON RETRASO", y=1360, color=AMBAR)])


@v.plano(9, "la luz que te da en la cara")
def _(d):
    return P(["#3a2a10", "#120a04"], [brillo(200, 500, 700, "#ffcf6a", 0.6, pulso=[0.08, 2.0]),
             IMG("cara_sol", ancho=780, x=680, y=1150, z=0.5, keys=[{"t": 0, "x": 700}, {"t": d, "x": 660, "ease": "suave"}]),
             *[flecha([[60 + k * 40, 300 + k * 90], [420 + k * 30, 800 + k * 70]], 0.05 + k * 0.1, d * 0.8, "#ffe08acc", 5, punta=False) for k in range(4)],
             polvo("#ffe08a", 40, (0, 300, 900, 1500), 3)],
             cam(1.0, 1.08, (600, 1000), (620, 1000)), sfx=[(0.1, "brillo", -18)])


@v.plano(17, "salió de allí")
def _(d):
    return P(ESPACIO, [BG("bg_esp_ambar"), *sol(540, 960, 320),
             foton(540, 960, keys=[{"t": 0, "x": 700, "y": 900, "op": 0}, {"t": 0.1, "op": 1}, {"t": d, "x": 1100, "y": 700, "ease": "entrada"}])],
             cam(1.0, 1.1, (540, 960), (640, 900)), "zoom", sfx=[(0.1, "zap", -20)])


@v.plano(22, "ocho minutos y veinte segundos")
def _(d):
    return P(["#1b2236", "#0b0f1c"], [brillo(540, 1000, 700, "#ffcf6a", 0.25), *cronometro(0, 300, 0, d)],
             cam(1.05, 1.12, (540, 1050), (540, 1050)),
             hud=[rotulo(0.05, d - 0.05, "8 MIN 20 S", tam=120, color="#ffffff", capsula="#0d1330d8", borde=AMBAR, y=560)],
             sfx=[(0.0, "tictac", -16, {"dur": d, "ritmo": 0.2})])


@v.plano(27, "trescientos mil km por segundo")
def _(d):
    return P(ESPACIO, [BG("bg_esp_violeta"), estrellas(50, 6),
             foton(540, 1000, ancho=260, keys=[{"t": 0, "x": -100}, {"t": d, "x": 1200, "ease": "lineal"}]),
             *lineas_vel(540, 1000, 2, "#ffe08aaa")],
             cam(1.0, 1.04), "barrido", hud=[contador(0.05, d - 0.05, 0, 300000, d * 0.6, "KM/S", tam=110, y=560, borde=AMBAR)],
             sfx=[(0.05, "whoosh", -14, {"dur": 0.6})], energia=0.7)


@v.plano(35, "aun así tarda eso en cruzar")
def _(d):
    return P(ESPACIO, [BG("bg_esp_petroleo"), *sol(140, 960, 200), tierra(960, 960, 140, giro=10),
             flecha([[360, 960], [880, 960]], 0.1, d * 0.95, AMBAR, 7, [16, 14]),
             foton(360, 960, keys=[{"t": 0.1, "x": 360}, {"t": d * 0.95, "x": 900, "ease": "lineal"}], ancho=90)],
             cam(1.0, 1.04), hud=[amarillo(0.1, d - 0.05, "Y AUN ASÍ…", y=1360, color=AMBAR)])


@v.plano(42, "ciento cincuenta millones de kilómetros")
def _(d):
    return P(ESPACIO, [BG("bg_esp_petroleo"), *sol(140, 960, 200), tierra(960, 960, 140, giro=10),
             flecha([[360, 1060], [880, 1060]], 0.05, d * 0.5, CIAN, 6), flecha([[880, 1060], [360, 1060]], 0.05, d * 0.5, CIAN, 6)],
             cam(1.35, 1.25, (700, 980), (620, 980)), hud=[contador(0.1, d - 0.05, 0, 150, d * 0.6, "MILLONES DE KM", tam=100, y=560, borde=CIAN)],
             sfx=[(0.1, "subida", -18, {"dur": d * 0.6})])


@v.plano(50, "si se apagara ahora mismo")
def _(d):
    return P(["#1a1a24", "#0a0a10"], [IMG("interruptor_on", ancho=420, x=540, y=1000, z=0.5, keys=[{"t": 0, "op": 1}, {"t": d * 0.4, "op": 0}]),
             IMG("interruptor_off", ancho=420, x=540, y=1000, z=0.5, keys=[{"t": 0, "op": 0}, {"t": d * 0.4, "op": 1}]),
             brillo(540, 700, 500, "#ffcf6a", 0.6, keys=[{"t": 0, "intensidad": 0.6}, {"t": d * 0.42, "intensidad": 0.0}])],
             cam(1.0, 1.1, (540, 1000), (540, 1000)), "corte", sfx=[(d * 0.4, "golpe", -14)])


@v.plano(55, "lo seguirías viendo brillar")
def _(d):
    return P(ESPACIO, [BG("bg_esp_petroleo"),
             *sol(140, 960, 200),
             tierra(960, 960, 160, giro=10),
             *[foton(260 + k * 140, 960, ancho=70, keys=[{"t": 0, "x": 260 + k * 140}, {"t": d, "x": 400 + k * 140, "ease": "lineal"}]) for k in range(4)]],
             cam(1.0, 1.05), hud=[amarillo(0.1, d - 0.05, "SIGUE BRILLANDO", y=1360, color=AMBAR, tam=88)], sfx=[(0.1, "brillo", -20)])


@v.plano(59, "ocho minutos más")
def _(d):
    return P(["#1b2236", "#0b0f1c"], [*reloj(540, 1050, 640, 12, 0, 12, 8, 0, d)],
             cam(1.05, 1.12, (540, 1050), (540, 1050)), hud=[contador(0.05, d - 0.05, 0, 8, d * 0.7, "MIN", tam=130, y=560, borde=AMBAR, contar_prefijo="+")],
             sfx=[(0.0, "tictac", -16, {"dur": d})])


@v.plano(62, "pero lo más raro pasa antes")
def _(d):
    return P(ESPACIO, [BG("bg_esp_ambar"), *sol(540, 1000, 420)],
             cam(1.0, 1.35, (540, 1000), (540, 1000)), "desenfoque", 0.3, hud=[rotulo(0.1, d - 0.05, "LO MÁS RARO", tam=100, color="#ffffff", capsula="#0d1330d8", borde=MAGENTA, y=1250)], energia=0.3,
             sfx=[(0.0, "rumor", -20, {"dur": d})])


@v.plano(68, "¿dónde nace esa energía?")
def _(d):
    return P(DENTRO, [brillo(540, 1000, 700, "#ff8a1a", 0.4),
             IMG("sol_corte", ancho=980, x=540, y=1050, z=0.5, keys=aparece(0.0, 0.45), anim={"girar": 3})],
             cam(1.0, 1.06, (540, 1050), (540, 1050)), "zoom", hud=[rotulo(0.1, d - 0.05, "¿DÓNDE?", tam=130, color=AMBAR, capsula=None, y=560)],
             sfx=[(0.05, "whoosh", -16, {"dur": 0.5})])


@v.plano(72, "en el centro del Sol")
def _(d):
    return P(DENTRO, [IMG("sol_corte", ancho=980, x=540, y=1050, z=0.5, anim={"girar": 3}), senala(540, 1050, d * 0.2, d - 0.05, 150, CIAN)],
             cam(1.0, 1.5, (540, 1050), (540, 1050)), hud=[contexto(0.05, d - 0.05, "NÚCLEO")], sfx=[(d * 0.2, "pop", -18)])


@v.plano(77, "a quince millones de grados")
def _(d):
    return P(DENTRO, [IMG("sol_corte", ancho=1500, x=540, y=1050, z=0.4, anim={"girar": 4}), brillo(540, 1050, 300, "#ffffff", 0.7, 0.5, pulso=[0.2, 0.3]), polvo("#fff3a0", 50, (200, 700, 880, 1400), 7, "chispas"),
             IMG("termo_rayo", ancho=220, x=880, y=1250, z=0.7, keys=late(0.1, 2, 0.12, 0.35))],
             cam(1.0, 1.08), hud=[contador(0.1, d - 0.05, 0, 15, d * 0.6, "MILLONES °C", tam=110, y=560, borde=MAGENTA)],
             sfx=[(0.1, "subida", -16, {"dur": d * 0.6}), (d * 0.62, "golpe", -16)])


@v.plano(82, "no puede ir en línea recta")
def _(d):
    return P(DENTRO, [IMG("sol_corte", ancho=1500, x=540, y=1050, z=0.4, anim={"girar": 4}), polvo("#fff3a0", 50, (200, 700, 880, 1400), 8, "chispas"),
             flecha([[300, 1050], [800, 1050]], 0.05, d * 0.4, "#ffffffaa", 8, [16, 12]),
             foton(300, 1050, keys=[{"t": 0, "x": 300}, {"t": d * 0.4, "x": 470, "ease": "salida"}, {"t": d * 0.5, "x": 430}]),
             rotulo(d * 0.45, d - 0.05, "X", tam=160, color="#ffffff", capsula="#c0392be6", x=600, y=1050, fijo=True, sin_pop=True)],
             cam(1.0, 1.05), hud=[rotulo(0.1, d - 0.05, "NI EN LÍNEA RECTA", tam=76, color="#ffffff", capsula="#0d1330d8", borde=CIAN, y=1250)], sfx=[(d * 0.45, "golpe", -16)])


@v.plano(91, "micro: choca")
def _(d):
    return P(DENTRO, [IMG("sol_corte", ancho=1700, x=540, y=960, z=0.4), polvo("#fff3a0", 60, (150, 500, 930, 1400), 9, "chispas"), foton(540, 960, ancho=200, keys=[{"t": 0, "x": 300}, {"t": d * 0.5, "x": 540, "ease": "entrada"}, {"t": d, "x": 380}]),
             IMG("chispa", ancho=300, x=600, y=960, z=0.8, keys=[{"t": d * 0.45, "op": 0}, {"t": d * 0.5, "op": 1}, {"t": d, "op": 0}])],
             cam(1.0, 1.1), "corte", sfx=[(d * 0.5, "pop", -14)])


@v.plano(92, "micro: rebota")
def _(d):
    return P(DENTRO, [IMG("sol_corte", ancho=1700, x=700, y=900, z=0.4), polvo("#fff3a0", 60, (150, 500, 930, 1400), 10, "chispas"), foton(540, 960, ancho=200, keys=[{"t": 0, "y": 700}, {"t": d * 0.5, "y": 1150, "ease": "entrada"}, {"t": d, "y": 760, "ease": "salida"}])],
             cam(1.0, 1.1), "corte", sfx=[(d * 0.5, "pop", -14)])


@v.plano(94, "cambia de dirección una y otra vez")
def _(d):
    pts = zigzag(540, 1050, 120, 22, 5)
    return P(DENTRO, [IMG("sol_corte", ancho=1300, x=540, y=1050, z=0.4, anim={"girar": 4}), polvo("#fff3a0", 40, (200, 700, 880, 1400), 11, "chispas"),
             flecha(pts, 0.05, d * 0.95, CIAN, 6, punta=False), foton(pts[-1][0], pts[-1][1], keys=[{"t": 0, "op": 0}, {"t": d * 0.9, "op": 1}], ancho=110)],
             cam(1.0, 1.08), hud=[rotulo(0.1, d - 0.05, "UNA Y OTRA VEZ", tam=80, color="#ffffff", capsula="#0d1330d8", borde=CIAN, y=1250)],
             sfx=[(0.1 + k * 0.25, "tic", -22) for k in range(int(d / 0.25))])


@v.plano(101, "como salir de un estadio lleno")
def _(d):
    pts = zigzag(540, 1000, 150, 18, 9)
    return P(["#1a1a24", "#0a0a10"], [BG("gente_estadio"), brillo(540, 1000, 600, "#000000", 0.0),
             flecha(pts, 0.1, d * 0.95, AMBAR, 10, punta=False, z=0.6),
             IMG("foton", ancho=140, x=pts[-1][0], y=pts[-1][1], z=0.7, keys=[{"t": 0, "op": 0}, {"t": d * 0.9, "op": 1}])],
             cam(1.0, 1.1, (540, 1000), (540, 1000)), "barrido", hud=[contexto(0.05, d - 0.05, "ESTADIO LLENO")],
             sfx=[(0.0, "rumor", -16, {"dur": d})])


@v.plano(112, "según la NASA")
def _(d):
    return P(DENTRO, [IMG("sol_corte", ancho=980, x=540, y=1050, z=0.5, anim={"girar": 3}),
             flecha(zigzag(540, 1050, 60, 10, 3), 0.05, d * 0.9, CIAN, 5, punta=False)],
             cam(1.0, 1.06), "desenfoque", hud=[rotulo(0.05, d - 0.05, "NASA", tam=120, color="#ffffff", capsula="#0b3d91e6", y=560)])


@v.plano(115, "ciento setenta mil años")
def _(d):
    return P(["#141a2e", "#0a0e1a"], [IMG("calendario", ancho=520, x=540, y=1100, z=0.5, keys=late(0.1, 3, 0.06, 0.3)),
             *[IMG("calendario", ancho=360, x=x, y=y, z=0.3, op=0.35, anim={"flotar": [12, 1.4]}) for x, y in [(180, 800), (900, 1400), (880, 760)]]],
             cam(1.0, 1.06), hud=[contador(0.05, d - 0.05, 0, 170000, d * 0.7, "AÑOS", tam=120, y=560, borde=AMBAR, contar_prefijo="≈")],
             sfx=[(0.05, "subida", -16, {"dur": d * 0.7}), (d * 0.72, "impacto", -12)], energia=0.9)


@v.plano(121, "en llegar a la superficie")
def _(d):
    pts = zigzag(540, 1050, 70, 16, 11) + [[540 + 330, 1050 - 300]]
    return P(DENTRO, [IMG("sol_corte", ancho=980, x=540, y=1050, z=0.5, anim={"girar": 3}),
             flecha(pts, 0.05, d * 0.95, CIAN, 6), senala(870, 750, d * 0.8, d - 0.05, 70, LIMA)],
             cam(1.0, 1.08, (540, 1050), (640, 950)), hud=[rotulo(0.1, d - 0.05, "SUPERFICIE", tam=96, color="#ffffff", capsula="#0d1330d8", borde=LIMA, y=1250)])


@v.plano(126, "cuando empezó ese viaje")
def _(d):
    return P(DENTRO, [IMG("sol_corte", ancho=1200, x=540, y=960, z=0.4, anim={"girar": 3}), foton(540, 960, ancho=260, keys=aparece(0.0, 0.4)), polvo("#fff3a0", 40, (300, 700, 780, 1200), 12, "chispas"),
             brillo(540, 960, 300, "#ffffff", 0.7, pulso=[0.2, 0.2])], cam(1.0, 1.1), "zoom", sfx=[(0.05, "brillo", -18)])


@v.plano(130, "aún vivían los neandertales")
def _(d):
    return P(["#0a0604", "#2a1a10"], [BG("bg_cueva"), IMG("hoguera", ancho=360, x=720, y=1520, z=0.5, anim={"pulso": [0.08, 0.25]}),
             brillo(720, 1450, 400, "#ff9a3a", 0.6, 0.45, pulso=[0.15, 0.3]),
             IMG("neandertal", ancho=560, x=360, y=1220, z=0.6, keys=[{"t": 0, "x": 330}, {"t": d, "x": 380, "ease": "suave"}]),
             polvo("#ffb84a", 30, (600, 1200, 850, 1500), 5, "chispas")],
             cam(1.0, 1.08, (540, 1200), (560, 1180)), "desenfoque", hud=[contexto(0.05, d - 0.05, "NEANDERTALES")], sfx=[(0.0, "rumor", -22, {"dur": d})])


@v.plano(137, "después, ocho minutos de carrera")
def _(d):
    return P(ESPACIO, [BG("bg_esp_violeta"), *sol(120, 960, 160), tierra(960, 960, 160, giro=10),
             foton(300, 960, ancho=150, keys=[{"t": 0, "x": 300}, {"t": d, "x": 860, "ease": "entrada"}]), *lineas_vel(500, 960, 4, "#ffe08aaa")],
             cam(1.0, 1.04), "barrido", hud=[contador(0.05, d - 0.05, 0, 8, d * 0.7, "MIN", tam=120, y=560, borde=AMBAR)],
             sfx=[(0.05, "whoosh", -14, {"dur": 0.6})], energia=0.8)


@v.plano(143, "hasta tus ojos")
def _(d):
    return P(["#e8b090", "#b8724e"], [IMG("ojo", ancho=1150, x=540, y=1000, z=0.5, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.08, "ease": "suave"}]),
             brillo(400, 900, 260, "#fff3a0", 0.0, 0.6, keys=[{"t": 0, "intensidad": 0.0}, {"t": d * 0.4, "intensidad": 0.9}]),
             foton(-100, 600, keys=[{"t": 0, "x": -100, "y": 600}, {"t": d * 0.4, "x": 470, "y": 960, "ease": "entrada"}, {"t": d * 0.45, "op": 0}])],
             cam(1.0, 1.08), sfx=[(d * 0.4, "brillo", -16)])


@v.plano(146, "¿nunca has visto el Sol de ahora? (bucle)")
def _(d):
    return P(ESPACIO, [BG("bg_esp_ambar"), estrellas(40, 4), *sol(540, 1050, 380), *reloj(840, 1500, 300, 11, 52, 12, 0, 0, d, z=0.7)],
             cam(1.0, 1.08, (540, 1000), (540, 1050)), "desenfoque", sfx=[(0.1, "tictac", -22, {"dur": d})])


v.construir("2026-11-17-tarde-02-sol-pasado", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 22, "db": -13},
            claves=["pasado", "retraso", "ocho", "veinte", "trescientos", "ciento", "cincuenta", "millones", "quince", "NASA", "setenta", "neandertales"])
