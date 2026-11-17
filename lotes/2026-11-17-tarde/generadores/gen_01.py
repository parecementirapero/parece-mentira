"""01 · Más caliente que el Sol (el rayo) — método denso (motor/DENSO.md). Lote 2026-11-17-tarde, Agente 20:00 (Jorge).
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

TOR = ["#0a0a1e", "#1e1a40"]
NOCHE = ["#0b0b22", "#151228"]


def destello(t, dur=0.18, i=0.85):
    return fundido_blanco([{"t": 0, "op": 0}, {"t": t, "op": 0}, {"t": t + 0.04, "op": i}, {"t": t + dur, "op": 0}], "#e8f4ff")


def lluvia_nube(y=330, sem=1):
    """Nube de tormenta que deriva despacio (detalle de fondo que dura)."""
    return IMG("nube" if sem % 2 else "nube_b", ancho=1500, x=540, y=y, z=0.2, anim={"flotar": [12, 3.0]})


def lider(x0, y0, x1, y1, t0, t1, sem=1, color="#dff4ff"):
    """Líder escalonado: el camino del rayo se dibuja a saltos hacia abajo antes de la descarga."""
    import random
    rr = random.Random(sem)
    pts = [[x0, y0]]
    for k in range(1, 12):
        u = k / 12
        pts.append([round(x0 + (x1 - x0) * u + rr.uniform(-70, 70)), round(y0 + (y1 - y0) * u)])
    pts.append([x1, y1])
    return flecha(pts, t0, t1, color, 6, punta=False, z=0.55)


def crece(t0, dur=0.25):
    """El rayo entre nubes se abre de lado desde el centro."""
    return [{"t": 0, "ex": 0.02, "op": 0}, {"t": t0, "ex": 0.02, "op": 1}, {"t": t0 + dur, "ex": 1.0, "ease": "salida"}]


def parpadeo(*tiempos, dur=0.12):
    ks = [{"t": 0, "op": 0}]
    for t in tiempos:
        ks += [{"t": t, "op": 0}, {"t": t + 0.02, "op": 1}, {"t": t + dur, "op": 0}]
    return ks


# ================================================================== PLANOS
@v.plano(0, "gancho: el rayo cae y revienta el termómetro")
def _(d):
    return P(TOR, [BG("bg_tormenta"), lluvia_nube(260),
             brillo(540, 1000, 700, "#9fd8ff", 0.5, 0.1, pulso=[0.3, 0.12]),
             IMG("rayo", ancho=760, x=540, y=980, z=0.6, keys=[{"t": 0, "y": 700, "ey": 0.5, "op": 1}, {"t": 0.18, "y": 980, "ey": 1.0, "ease": "salida"},
                                                             {"t": d * 0.5, "escala": 1.04}, {"t": d, "escala": 1.0}], anim={"pulso": [0.08, 0.12]}),
             IMG("termo_rayo", ancho=230, x=860, y=1180, z=0.7, keys=arranque(860, 1180, d, "derecha", 220, 30) + late(d * 0.45, 2, 0.12, 0.3)),
             destello(0.0, 0.25, 0.9), destello(d * 0.6, 0.15, 0.6)],
             cam(1.12, 1.0, (540, 1000), (540, 980), temblor=6), vineta=0.7, sfx=[(0.0, "impacto", -10), (0.05, "zap", -16), (d * 0.6, "golpe", -16)])


@v.plano(4, "micro: el Sol")
def _(d):
    return P(ESPACIO, [BG("bg_esp_ambar"), *sol(540, 980, 300)], cam(1.0, 1.12), "corte", sfx=[(0.02, "brillo", -18)])


@v.plano(5, "un rayo… (entre nubes, se abre de lado)")
def _(d):
    return P(TOR, [BG("bg_tormenta"), lluvia_nube(420, 2),
             IMG("rayo_horizontal", ancho=1500, x=540, y=560, z=0.5, keys=crece(0.05, 0.3)),
             brillo(540, 560, 600, "#d8b8ff", 0.0, 0.3, keys=[{"t": 0.05, "intensidad": 0}, {"t": 0.15, "intensidad": 0.8}, {"t": d, "intensidad": 0.3}])],
             cam(1.0, 1.08, (540, 800), (540, 700)), sfx=[(0.05, "zap", -16), (0.2, "rumor", -20, {"dur": d})])


@v.plano(7, "cinco veces más")
def _(d):
    return P(["#120a20", "#2a1430"], [brillo(300, 1000, 380, "#ffb8f0", 0.5), *sol(800, 1000, 120),
             IMG("rayo_ramificado", ancho=520, x=300, y=1000, z=0.5, keys=parpadeo(0.05, 0.3, 0.55, dur=0.2) + [{"t": 0.8, "op": 1}]),
             rotulo(0.15, d - 0.05, ">", tam=200, color=AMBAR, capsula=None, x=600, y=1000, fijo=True, sin_pop=True)],
             cam(1.0, 1.06, (540, 1000), (540, 1000)),
             hud=[contador(0.1, d - 0.05, 1, 5, d * 0.5, "VECES", tam=120, y=560, borde=CIAN, contar_prefijo="×")],
             sfx=[(0.1, "subida", -18, {"dur": d * 0.5}), (d * 0.55, "ding", -18)])


@v.plano(10, "calienta el aire (el canal se pone al rojo)")
def _(d):
    return P(["#05050c", "#1a0c14"], [IMG("canal_plasma", ancho=1080, x=540, y=960, z=0.4, keys=[{"t": 0, "op": 0.3}, {"t": d, "op": 1.0}]),
             brillo(540, 960, 600, "#ff5a1a", 0.0, 0.3, keys=[{"t": 0, "intensidad": 0.0}, {"t": d, "intensidad": 0.7}]),
             polvo("#ffd27a", 50, (300, 300, 780, 1600), 4, "chispas")],
             cam(1.0, 1.15, (540, 600), (540, 1300)), "zoom", hud=[rotulo(0.15, d - 0.05, "EL AIRE", tam=100, color="#ffffff", capsula="#c0392be6", y=1250)],
             sfx=[(0.0, "rumor", -18, {"dur": d})])


@v.plano(14, "treinta mil grados")
def _(d):
    return P(["#1a0a14", "#2a0a14"], [brillo(540, 1000, 600, "#ff2d55", 0.35, pulso=[0.2, 0.3]),
             IMG("termo_rayo", ancho=330, x=540, y=1050, z=0.5, keys=[{"t": 0, "ey": 0.95}, {"t": d * 0.6, "ey": 1.02, "ease": "elastico"}]),
             IMG("canal_plasma", ancho=700, x=830, y=1000, z=0.4, anim={"pulso": [0.05, 0.3]})],
             cam(1.0, 1.08, (540, 1050), (540, 1000)),
             hud=[contador(0.1, d - 0.05, 0, 30000, d * 0.6, "°C", tam=120, y=560, borde=MAGENTA)],
             sfx=[(0.1, "subida", -16, {"dur": d * 0.6}), (d * 0.62, "golpe", -16)])


@v.plano(18, "la superficie del Sol")
def _(d):
    return P(ESPACIO, [BG("bg_esp_ambar"), *sol(540, 1100, 520), polvo("#ffcf6a", 30, (0, 400, 1080, 1700), 7, "chispas")],
             cam(1.0, 1.1, (540, 1000), (540, 1050)), "desenfoque", 
             sfx=[(0.0, "rumor", -20, {"dur": d})])


@v.plano(24, "cinco mil quinientos")
def _(d):
    return P(["#2a1a08", "#120a04"], [brillo(540, 1000, 600, "#ffb02e", 0.35),
             IMG("termo_sol", ancho=330, x=540, y=1050, z=0.5, keys=aparece(0.0, 0.35)), *sol(840, 760, 90)],
             cam(1.0, 1.06, (540, 1050), (540, 1030)),
             hud=[contador(0.1, d - 0.05, 0, 5500, d * 0.6, "°C", tam=120, y=560, borde=AMBAR)], sfx=[(0.1, "subida", -20, {"dur": d * 0.5})])


@v.plano(28, "¿y cuánto dura?")
def _(d):
    return P(["#1b2236", "#0b0f1c"], [brillo(540, 1000, 700, "#7ad0ff", 0.3), *cronometro(0, 40, 0, d)],
             cam(1.05, 1.15, (540, 1050), (540, 1050)), "desenfoque", 0.2, hud=[rotulo(0.05, d - 0.05, "¿CUÁNTO?", tam=120, color=CIAN, capsula=None, y=560)],
             sfx=[(0.0, "tictac", -16, {"dur": d, "ritmo": 0.25})])


@v.plano(31, "una fracción de segundo: tres rayos distintos parpadean")
def _(d):
    return P(TOR, [BG("bg_tormenta"),
             IMG("rayo_c", ancho=420, x=230, y=900, z=0.5, keys=parpadeo(d * 0.1)),
             IMG("rayo_ramificado", ancho=700, x=760, y=1000, z=0.5, keys=parpadeo(d * 0.4)),
             IMG("rayo_horizontal_b", ancho=1200, x=540, y=420, z=0.5, keys=parpadeo(d * 0.7)),
             destello(d * 0.4, 0.12, 0.5), lluvia_nube(260, 2)],
             cam(1.0, 1.05), hud=[rotulo(0.1, d - 0.05, "UN INSTANTE", tam=96, color="#ffffff", capsula="#0d1330d8", borde=CIAN, y=1250)],
             sfx=[(d * 0.1, "zap", -18), (d * 0.4, "zap", -16), (d * 0.7, "zap", -18)])


@v.plano(35, "el aire se calienta (primer plano del canal, ondas de calor)")
def _(d):
    return P(["#05050c", "#1a1430"], [IMG("canal_plasma", ancho=2000, x=540, y=960, z=0.4, anim={"balanceo": [1.5, 0.15]}),
             brillo(540, 960, 500, "#ff7a3a", 0.5, 0.55, pulso=[0.3, 0.2]),
             *[IMG("onda", ancho=260, x=540, y=960, z=0.5, keys=[{"t": k * 0.3, "escala": 0.5, "op": 0.6}, {"t": k * 0.3 + 0.9, "escala": 2.2, "op": 0}]) for k in range(4)],
             polvo("#ffd27a", 50, (200, 400, 880, 1500), 8, "chispas")],
             cam(1.15, 1.3, (540, 1100), (540, 860)), "zoom", sfx=[(0.0, "rumor", -18, {"dur": d})])


@v.plano(39, "micro: de golpe (dos descargas)", mas=0.0)
def _(d):
    return P(["#ffffff", "#bfe9ff"], [brillo(540, 960, 600, "#7ad8ff", 0.6), IMG("rayo_doble", ancho=1300, x=540, y=960, z=0.5, keys=parpadeo(0.0, 0.25, dur=0.18)),
             IMG("onda", ancho=700, x=540, y=960, z=0.6, keys=[{"t": 0, "escala": 0.4}, {"t": d, "escala": 1.6, "op": 0.3}])], cam(1.15, 1.25), "corte", sfx=[(0.0, "golpe", -12)])


@v.plano(42, "explosión: el rayo cae en un árbol")
def _(d):
    return P(NOCHE, [BG("campo_noche"), lluvia_nube(260, 1),
             IMG("arbol", ancho=620, x=540, y=1250, z=0.45, keys=[{"t": 0, "op": 1}, {"t": 0.15, "op": 0}]),
             IMG("arbol_quemado", ancho=620, x=540, y=1250, z=0.46, keys=[{"t": 0, "op": 0}, {"t": 0.15, "op": 1}]),
             lider(540, 300, 540, 900, 0.0, 0.1, 4),
             IMG("rayo_ramificado", ancho=760, x=520, y=620, z=0.5, keys=parpadeo(0.1, dur=0.35)),
             IMG("onda", ancho=400, x=540, y=900, z=0.6, keys=[{"t": 0.12, "escala": 0.3, "op": 1}, {"t": d, "escala": 3.2, "op": 0.1, "ease": "salida"}]),
             *[IMG("chispa", ancho=160, x=x, y=y, z=0.65, keys=[{"t": 0.15, "op": 0, "escala": 0.3}, {"t": 0.2, "op": 1, "escala": 1}, {"t": 0.7, "op": 0}]) for x, y in [(430, 820), (660, 860), (520, 760), (600, 950)]],
             destello(0.1, 0.2, 0.8)],
             cam(1.0, 1.06, (540, 1000), (540, 980), temblor=10), hud=[rotulo(0.1, d - 0.05, "¡BUM!", tam=130, color="#ffffff", capsula="#c0392be6", y=1250)],
             sfx=[(0.1, "impacto", -10), (0.15, "golpe", -14)], energia=0.9)


@v.plano(48, "justo después se enfría")
def _(d):
    return P(["#0a1830", "#04081a"], [brillo(540, 1000, 500, "#7ad0ff", 0.4),
             IMG("onda", ancho=400, x=540, y=1000, z=0.6, keys=[{"t": 0, "escala": 2.6, "op": 0.8}, {"t": d, "escala": 1.0, "op": 1, "ease": "suave"}]),
             IMG("termo_sol", ancho=200, x=860, y=1150, z=0.5, keys=[{"t": 0, "ey": 1.05}, {"t": d, "ey": 0.9}])],
             cam(1.0, 1.06), "desenfoque", hud=[amarillo(0.1, d - 0.05, "SE ENFRÍA", y=1420, color=CIAN)], sfx=[(0.0, "whoosh", -18, {"dur": 0.5})])


@v.plano(53, "micro: se encoge")
def _(d):
    return P(["#0a1830", "#04081a"], [brillo(540, 960, 500, "#7ad0ff", 0.4), polvo("#bfe9ff", 40, (200, 500, 880, 1400), 9),
             IMG("onda", ancho=600, x=540, y=960, z=0.5, keys=[{"t": 0, "escala": 1.4}, {"t": d, "escala": 0.5, "ease": "entrada"}]),
             IMG("termo_sol", ancho=200, x=860, y=1150, z=0.5, keys=[{"t": 0, "ey": 0.95}, {"t": d, "ey": 0.85}])],
             cam(1.0, 1.1), "corte", sfx=[(0.02, "pop", -18)])


@v.plano(56, "ese empujón del aire (sobre el mar)")
def _(d):
    return P(TOR, [BG("bg_mar_tormenta"), IMG("rayo_horizontal_b", ancho=1300, x=540, y=380, z=0.4, keys=parpadeo(0.05, dur=0.3) + [{"t": 0.4, "op": 0.5}]),
             *[IMG("onda", ancho=300, x=540, y=420, z=0.5, keys=[{"t": k * 0.25, "escala": 0.4, "op": 1}, {"t": k * 0.25 + 1.2, "escala": 3.0, "op": 0, "ease": "salida"}]) for k in range(4)],
             IMG("oreja", ancho=300, x=860, y=1350, z=0.6, keys=aparece(d * 0.3, 0.4))],
             cam(1.0, 1.05, (540, 800), (540, 900)), "barrido", sfx=[(0.1, "rumor", -16, {"dur": d})])


@v.plano(60, "es el trueno (dos rayos caen al mar)")
def _(d):
    return P(TOR, [BG("bg_mar_tormenta"),
             IMG("rayo_doble", ancho=1080, x=540, y=600, z=0.5, keys=parpadeo(0.0, 0.3, dur=0.2) + [{"t": 0.55, "op": 0.8}]),
             IMG("onda", ancho=500, x=540, y=1180, z=0.6, keys=[{"t": 0, "escala": 0.5, "op": 1}, {"t": d, "escala": 3.5, "op": 0, "ease": "salida"}]),
             destello(0.0, 0.2, 0.6)],
             cam(1.06, 1.0, (540, 900), (540, 960), temblor=14), hud=[rotulo(0.1, d - 0.05, "TRUENO", tam=130, color="#ffffff", capsula="#0d1330d8", borde=CIAN, y=1250)],
             sfx=[(0.0, "golpe", -9), (0.1, "rumor", -12, {"dur": d}), (0.1, "ola", -22)], energia=0.9)


@v.plano(63, "relámpago y trueno son lo mismo")
def _(d):
    return P(TOR, [BG("bg_tormenta"), IMG("rayo_ramificado", ancho=560, x=300, y=980, z=0.5, keys=parpadeo(0.0, 0.5, 1.0, dur=0.3)),
             IMG("onda", ancho=420, x=770, y=1000, z=0.5, anim={"pulso": [0.08, 0.6]}),
             rotulo(0.3, d - 0.05, "=", tam=220, color=LIMA, capsula=None, x=550, y=1000, fijo=True, sin_pop=True)],
             cam(1.0, 1.06), "desenfoque", hud=[amarillo(0.15, d - 0.05, "LO MISMO", y=1420, color=LIMA)], sfx=[(0.3, "ding", -18)])


@v.plano(73, "pero la luz llega antes")
def _(d):
    return P(NOCHE, [BG("campo_noche"), IMG("rayo_ramificado", ancho=360, x=860, y=640, z=0.3, keys=parpadeo(0.0, dur=0.5)),
             IMG("persona_cuenta", ancho=300, x=230, y=1350, z=0.6),
             flecha([[850, 820], [340, 1150]], 0.05, 0.3, CIAN, 10),
             IMG("onda", ancho=180, z=0.5, keys=[{"t": 0, "x": 860, "y": 860}, {"t": d, "x": 560, "y": 1050, "ease": "lineal"}])],
             cam(1.0, 1.05, (540, 1000), (520, 1020)), hud=[amarillo(0.1, d - 0.05, "LUZ: ANTES", y=560, color=CIAN)], sfx=[(0.05, "zap", -18)])


@v.plano(78, "el sonido tarda tres segundos (la onda viaja hacia la oreja)")
def _(d):
    return P(TOR, [BG("bg_mar_tormenta"), IMG("rayo_c", ancho=320, x=170, y=820, z=0.3, keys=parpadeo(0.0, dur=0.3)),
             *[IMG("onda", ancho=200, z=0.5, keys=[{"t": k * 0.35, "x": 200, "y": 1000, "escala": 0.5, "op": 1}, {"t": k * 0.35 + d * 0.8, "x": 820, "y": 1250, "escala": 1.6, "op": 0.2}]) for k in range(3)],
             IMG("oreja", ancho=260, x=880, y=1300, z=0.6, keys=late(d * 0.75, 2, 0.1, 0.3))],
             cam(1.0, 1.06, (540, 1100), (600, 1100)), hud=[contador(0.1, d - 0.05, 0, 3, d * 0.8, "SEGUNDOS", tam=110, y=560, borde=CIAN)],
             sfx=[(0.0, "rumor", -18, {"dur": d})])


@v.plano(84, "en recorrer un kilómetro")
def _(d):
    return P(NOCHE, [BG("campo_noche"), flecha([[540, 1880], [540, 1180]], 0.05, d * 0.8, LIMA, 9, [18, 14]),
             IMG("onda", ancho=160, z=0.5, keys=[{"t": 0, "x": 540, "y": 1180, "escala": 1.4}, {"t": d, "x": 540, "y": 1700, "escala": 2.2}])],
             cam(1.0, 1.06, (540, 1300), (540, 1250)), hud=[rotulo(0.15, d - 0.05, "1 KM", tam=120, color="#ffffff", capsula="#0d1330d8", borde=LIMA, y=560)])


@v.plano(88, "cuenta los segundos")
def _(d):
    return P(TOR, [BG("bg_tormenta"), lluvia_nube(280, 2), IMG("rayo_horizontal", ancho=1100, x=600, y=420, z=0.3, keys=crece(0.2, 0.25) + [{"t": 0.7, "op": 0}]),
             IMG("persona_cuenta", ancho=440, x=380, y=1300, z=0.6, keys=[{"t": 0, "x": 360}, {"t": d, "x": 400, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1100), (520, 1100)), hud=[contador(0.2, d - 0.05, 1, 3, d * 0.7, "", tam=150, y=560, borde=AMBAR)],
             sfx=[(0.2, "zap", -20), (0.5, "tic", -18), (0.9, "tic", -18), (1.3, "tic", -18)])


@v.plano(94, "micro: el destello (líder que baja)")
def _(d):
    return P(TOR, [BG("bg_tormenta"), lider(540, 200, 560, 1700, 0.0, d * 0.6, 9), brillo(540, 960, 600, "#bfe9ff", 0.4), destello(d * 0.6, 0.2, 0.8)],
             cam(1.0, 1.1), "corte", sfx=[(d * 0.6, "zap", -14)])


@v.plano(96, "micro: el trueno")
def _(d):
    return P(TOR, [BG("bg_tormenta"), IMG("onda", ancho=500, x=540, y=960, z=0.5, keys=[{"t": 0, "escala": 0.6}, {"t": d, "escala": 2.4, "op": 0.2}])],
             cam(1.0, 1.06, temblor=10), "corte", sfx=[(0.0, "golpe", -12)])


@v.plano(99, "divide entre tres (la silueta cuenta con los dedos)")
def _(d):
    return P(TOR, [BG("bg_tormenta"), lluvia_nube(260, 3), IMG("persona_cuenta", ancho=460, x=540, y=1300, z=0.6, keys=late(0.1, 2, 0.05, 0.3))],
             cam(1.05, 1.12, (540, 1100), (540, 1080)), "desenfoque", hud=[rotulo(0.05, d - 0.05, "÷ 3", tam=170, color=AMBAR, capsula="#0d1330d8", y=560)], sfx=[(0.1, "pop", -16)])


@v.plano(102, "a cuántos kilómetros cayó")
def _(d):
    return P(NOCHE, [BG("campo_noche"), lluvia_nube(260, 1),
             IMG("rayo_doble", ancho=520, x=820, y=850, z=0.3, keys=parpadeo(0.15, 0.6, dur=0.25)),
             flecha([[200, 1500], [760, 1120]], 0.2, d * 0.8, AMBAR, 8, [18, 12])],
             cam(1.0, 1.08, (540, 1200), (600, 1100)), hud=[amarillo(0.15, d - 0.05, "¿A CUÁNTOS KM?", y=560, color=AMBAR, tam=84)], sfx=[(0.15, "zap", -18)])


@v.plano(108, "nueve segundos")
def _(d):
    return P(["#1b2236", "#0b0f1c"], [*cronometro(0, 54, 0, d)], cam(1.1, 1.18, (540, 1050), (540, 1050)),
             hud=[contador(0.05, d - 0.05, 0, 9, d * 0.8, "s", tam=150, y=560, borde=CIAN)], sfx=[(0.0, "tictac", -16, {"dur": d, "ritmo": 0.12})])


@v.plano(110, "tres kilómetros")
def _(d):
    return P(NOCHE, [BG("campo_noche"), IMG("rayo_c", ancho=360, x=760, y=820, z=0.3, anim={"pulso": [0.06, 0.1]}),
             IMG("persona_cuenta", ancho=240, x=240, y=1450, z=0.6), flecha([[300, 1300], [700, 1020]], 0.05, d * 0.6, LIMA, 9, [18, 12])],
             cam(1.0, 1.06, (540, 1150), (540, 1150)), hud=[contador(0.05, d - 0.05, 0, 3, d * 0.6, "KM", tam=150, y=560, borde=LIMA)],
             sfx=[(d * 0.6, "ding", -18)])


@v.plano(112, "micro: ¡ojo!")
def _(d):
    return P(["#e8b090", "#b8724e"], [IMG("ojo", ancho=1100, x=540, y=960, z=0.5, keys=[{"t": 0, "ey": 0.2}, {"t": 0.15, "ey": 1.0, "ease": "elastico"}])],
             cam(1.0, 1.1), "corte", sfx=[(0.02, "pop", -16)])


@v.plano(114, "el trueno se oye a dieciséis km")
def _(d):
    return P(NOCHE, [BG("campo_noche"), lluvia_nube(240, 2),
             *[IMG("onda", ancho=300, x=540, y=900, z=0.5, keys=[{"t": k * 0.4, "escala": 0.4, "op": 1}, {"t": k * 0.4 + 1.6, "escala": 4.5, "op": 0, "ease": "salida"}]) for k in range(5)],
             IMG("oreja", ancho=200, x=900, y=1500, z=0.6, anim={"balanceo": [3, 1.0]})],
             cam(1.0, 1.04, (540, 1100), (540, 1100)), hud=[contador(0.15, d - 0.05, 0, 16, d * 0.6, "KM", tam=140, y=560, borde=CIAN, contar_prefijo="≈")],
             sfx=[(0.0, "rumor", -15, {"dur": d})])


@v.plano(123, "un rayo puede caer lejos: sale del yunque a cielo despejado")
def _(d):
    return P(["#0a0f2a", "#0a0c18"], [BG("bg_cielo_despejado"), IMG("yunque", ancho=900, x=250, y=700, z=0.3, anim={"flotar": [8, 3.0]}),
             flecha([[640, 520], [760, 600], [820, 760], [880, 1000], [900, 1300], [910, 1500]], d * 0.15, d * 0.45, "#e8f6ff", 7, punta=False, z=0.5),
             IMG("rayo_horizontal_b", ancho=600, x=760, y=520, z=0.45, keys=parpadeo(d * 0.45, dur=0.3)),
             flecha([[420, 1650], [880, 1650]], 0.1, d * 0.4, MAGENTA, 8, [20, 14]), destello(d * 0.45, 0.18, 0.5)],
             cam(1.0, 1.06, (540, 1000), (600, 1000)), hud=[rotulo(0.15, d - 0.05, "LEJOS DE LA TORMENTA", tam=66, color="#ffffff", capsula="#0d1330d8", borde=MAGENTA, y=1250)],
             sfx=[(d * 0.45, "impacto", -12)], energia=0.8)


@v.plano(134, "si lo oyes, estás a su alcance")
def _(d):
    return P(TOR, [BG("bg_tormenta"), lluvia_nube(260, 1), IMG("persona_cuenta", ancho=380, x=540, y=1300, z=0.6),
             IMG("oreja", ancho=160, x=760, y=900, z=0.6, keys=aparece(0.1, 0.35)),
             {"tipo": "forma", "forma": "elipse", "ancho": 900, "alto": 900, "relleno": "#ff2d55", "op_relleno": 0.08, "grosor": 8, "borde": MAGENTA,
              "x": 540, "y": 1150, "z": 0.4, "keys": [{"t": 0, "escala": 2.0, "op": 0}, {"t": d * 0.4, "escala": 1.0, "op": 1, "ease": "golpe"}]}],
             cam(1.0, 1.05, (540, 1100), (540, 1100)), hud=[amarillo(0.15, d - 0.05, "A SU ALCANCE", y=560, color=MAGENTA)], sfx=[(d * 0.4, "golpe", -14)])


@v.plano(142, "busca un refugio cerrado")
def _(d):
    return P(NOCHE, [BG("campo_noche"), lluvia_nube(220, 3), IMG("refugio", ancho=1000, x=540, y=1150, z=0.5, keys=aparece(0.0, 0.4)),
             brillo(540, 1200, 300, "#ffd27a", 0.4, 0.55, pulso=[0.2, 1.0])],
             cam(1.0, 1.08, (540, 1200), (540, 1180)), "desenfoque", hud=[rotulo(0.15, d - 0.05, "REFUGIO", tam=110, color="#ffffff", capsula="#0d1330d8", borde=LIMA, y=560)],
             sfx=[(0.0, "agua", -20, {"dur": d})], energia=0.4)


@v.plano(146, "¿tú cuentas los segundos? (bucle hacia el gancho)")
def _(d):
    return P(TOR, [BG("bg_tormenta"), lluvia_nube(260),
             brillo(540, 1000, 700, "#9fd8ff", 0.5, 0.1, pulso=[0.3, 0.12]),
             IMG("rayo", ancho=760, x=540, y=980, z=0.6, keys=[{"t": 0, "op": 0}, {"t": d * 0.3, "op": 1}], anim={"pulso": [0.08, 0.12]}),
             IMG("termo_rayo", ancho=230, x=860, y=1180, z=0.7, keys=[{"t": 0, "y": 1400, "op": 0}, {"t": d * 0.4, "y": 1180, "op": 1, "ease": "elastico"}]),
             destello(d * 0.3, 0.2, 0.6)],
             cam(1.0, 1.12, (540, 1000), (540, 1000)), sfx=[(d * 0.3, "zap", -16)])


# ------------------------------------------------------------------ micro planos (golpes de 0,4–0,7 s)
@v.plano(47, "micro: el árbol arde")
def _(d):
    return P(["#1a0a04", "#0a0402"], [IMG("arbol_quemado", ancho=1400, x=540, y=1300, z=0.5), brillo(540, 900, 400, "#ff8a1a", 0.6, pulso=[0.2, 0.15]),
             polvo("#ffb84a", 40, (300, 600, 780, 1300), 14, "chispas")], cam(1.1, 1.2), "corte", sfx=[(0.02, "golpe", -16)])


v.construir("2026-11-17-tarde-01-rayo-sol", version=3, bucle=0.35, musica={"generar": "curiosidad", "semilla": 21, "db": -13},
            claves=["caliente", "Sol", "cinco", "treinta", "mil", "quinientos", "trueno", "tres", "kilómetro", "nueve", "dieciséis", "alcance"])
