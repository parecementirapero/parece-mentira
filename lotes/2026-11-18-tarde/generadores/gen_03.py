"""03 · Ahora mides menos (los discos de la columna) — método denso. Lote 2026-11-18-tarde, Agente 20:00 (Jorge).
Experimento del lote: gancho en segunda persona («Ahora mides menos.»).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_tarde  # noqa: E402

SVG = ilus_tarde.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

OSC = ["#0a0c1a", "#1a2040"]
DIA = ["#f4dcb8", "#d8b890"]
HUESO, DISCO = "#f2e6cc", "#4ac8e8"


def columna(x, y_base, n, d, t0, t1, ap0, ap1, ancho=220, alto_v=70, alto_d=34, z=0.5, horizontal=False, brillo_disco=True):
    """Columna de n vértebras (hueso) con discos (agua) entre ellas. Los discos pasan de altura ×ap0 a ×ap1 entre t0 y t1
    y las vértebras se recolocan encima (la columna entera encoge o crece). horizontal=True: tumbada (crece hacia la derecha)."""
    els = []

    def pos(k, ap, disco=False):
        # distancia desde la base al centro de la pieza k
        s = k * (alto_v + alto_d * ap) + (alto_v / 2 if not disco else alto_v + alto_d * ap / 2)
        return s
    for k in range(n):
        for disco in (False, True):
            if disco and k == n - 1:
                continue
            s0, s1 = pos(k, ap0, disco), pos(k, ap1, disco)
            if horizontal:
                k0, k1 = {"x": x + s0, "y": y_base}, {"x": x + s1, "y": y_base}
            else:
                k0, k1 = {"x": x, "y": y_base - s0}, {"x": x, "y": y_base - s1}
            if disco:
                e0, e1 = {"ey" if not horizontal else "ex": ap0}, {"ey" if not horizontal else "ex": ap1}
                els.append({"tipo": "forma", "forma": "elipse", "ancho": ancho * 0.92 if not horizontal else alto_d, "alto": alto_d if not horizontal else ancho * 0.92,
                            "relleno": DISCO, "z": z, "keys": [{"t": 0, **k0, **e0}, {"t": t0, **k0, **e0}, {"t": t1, **k1, **e1, "ease": "suave"}, {"t": max(d, t1 + 0.01), **k1, **e1}]})
                if brillo_disco:
                    els.append(brillo(k0["x"], k0["y"], 90, "#7df9ff", 0.35, z - 0.01,
                                      keys=[{"t": 0, **k0}, {"t": t0, **k0}, {"t": t1, **k1, "ease": "suave"}]))
            else:
                w_, h_ = (ancho, alto_v) if not horizontal else (alto_v, ancho)
                els.append({"tipo": "forma", "forma": "redondeado", "ancho": w_, "alto": h_, "relleno": HUESO, "borde": "#b8a888", "grosor": 4, "z": z + 0.01,
                            "keys": [{"t": 0, **k0}, {"t": t0, **k0}, {"t": t1, **k1, "ease": "suave"}, {"t": max(d, t1 + 0.01), **k1}]})
    return els


def marca(y0, y1, t0, t1, x=540, ancho=520, color="#ff2d55", z=0.7):
    """Línea roja de altura que baja (o sube) por el tallímetro."""
    return {"tipo": "forma", "forma": "rect", "ancho": ancho, "alto": 12, "relleno": color, "x": x, "z": z,
            "keys": [{"t": 0, "y": y0}, {"t": t0, "y": y0}, {"t": t1, "y": y1, "ease": "suave"}]}


# ================================================================== PLANOS
@v.plano(0, "gancho: la marca de altura baja por el tallímetro sobre la silueta")
def _(d):
    return P(["#2a1a3a", "#ffb46a"], [BG("bg_dormitorio_dia"), IMG("tallimetro", ancho=300, x=760, y=1000, z=0.4),
             IMG("perfil", ancho=420, x=480, z=0.5, keys=[{"t": 0, "y": 1020, "ey": 1.0}, {"t": d, "y": 1050, "ey": 0.97, "ease": "suave"}]),
             marca(360, 470, 0.0, d * 0.8, 600, 600), flecha([[900, 300], [900, 470]], 0.0, d * 0.8, MAGENTA, 10, z=0.75)],
             cam(1.0, 1.0, (540, 900), (540, 800)), vineta=0.6, sfx=[(0.05, "whoosh", -12, {"dur": 0.6}), (d * 0.7, "golpe", -16)])


@v.plano(3, "menos que esta mañana: el despertador suena junto a la cama")
def _(d):
    return P(DIA, [BG("bg_dormitorio_dia"), IMG("cama", ancho=900, x=520, y=1500, z=0.4),
             IMG("despertador", ancho=300, x=820, y=1150, z=0.55, anim={"balanceo": [8, 0.1]}), polvo("#fff4c0", 30, (500, 800, 1000, 1500), 3)],
             cam(1.0, 1.05, (600, 1300)), "corte", hud=[contexto(0.05, d - 0.05, "AL LEVANTARTE")], sfx=[(0.05, "tictac", -22, {"dur": 0.8})])


@v.plano(9, "¿por qué? la lupa recorre la espalda")
def _(d):
    return P(OSC, [BG("bg_dormitorio"), IMG("perfil_azul", ancho=520, x=540, y=1100, z=0.45),
             IMG("lupa", ancho=380, z=0.6, keys=[{"t": 0, "x": 420, "y": 600}, {"t": d, "x": 460, "y": 1000, "ease": "suave"}])],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "¿POR QUÉ?", y=560, tam=130, color=CIAN)], sfx=[(0.1, "roce", -20)])


@v.plano(11, "entre las vértebras: la columna se ilumina dentro de la silueta")
def _(d):
    return P(OSC, [BG("bg_dormitorio"), IMG("perfil_azul", ancho=640, x=540, y=1150, z=0.4),
             *columna(480, 1380, 9, d, 0.0, 0.01, 1, 1, 80, 40, 16, 0.5)],
             cam(1.0, 1.1, (540, 1100), (520, 1000)), "desenfoque", hud=[contexto(0.05, d - 0.05, "VÉRTEBRAS")], sfx=[(0.1, "brillo", -18)])


@v.plano(17, "hay unos discos blandos: columna de cerca")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), *columna(540, 1550, 6, d, 0.0, 0.01, 1, 1, 300, 90, 50, 0.5),
             senala(540, 1550 - 90 - 25, 0.2, d - 0.05, 170, CIAN)],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "DISCOS", y=560, tam=120, color=CIAN)], sfx=[(0.2, "pop", -18)])


@v.plano(21, "como cojines llenos de agua")
def _(d):
    return P(["#0d1324", "#1f2b48"], [brillo(540, 1050, 600, "#4ac8e8", 0.35, 0.1),
             IMG("cojin", ancho=760, x=540, y=1100, z=0.5, keys=late(0.1, 2, 0.06, 0.4)),
             IMG("gota", ancho=110, x=540, z=0.6, keys=[{"t": 0, "y": 500, "op": 0}, {"t": 0.1, "op": 1}, {"t": d * 0.6, "y": 1050, "op": 0, "ease": "entrada"}])],
             cam(1.0, 1.05), "corte", sfx=[(d * 0.55, "agua", -20, {"dur": 0.6})])


@v.plano(26, "de pie, la gravedad los aprieta: la columna encoge")
def _(d):
    return P(OSC, [BG("bg_esp_violeta"), *columna(540, 1600, 6, d, 0.2, d * 0.9, 1.0, 0.45, 280, 90, 60, 0.5),
             *[flecha([[x, 300], [x, 520]], 0.1 + k * 0.15, 0.6 + k * 0.15, LIMA, 10, z=0.7) for k, x in enumerate((340, 540, 740))]],
             cam(1.0, 1.04), "corte", hud=[amarillo(0.05, d - 0.03, "GRAVEDAD", y=700, tam=96, color=LIMA)], sfx=[(0.2, "subida", -20, {"dur": d * 0.6})])


@v.plano(37, "van soltando líquido: gotas que escapan del disco")
def _(d):
    gotas = [IMG("gota", ancho=80, z=0.6, keys=lanza(0.05 + k * 0.12, d, (540, 1100), (540 + dx, 1100 + dy))) for k, (dx, dy) in
             enumerate([(-380, -200), (380, -160), (-320, 260), (330, 300), (-60, -420), (60, 420)])]
    return P(["#0d1324", "#1f2b48"], [IMG("cojin", ancho=700, x=540, y=1100, z=0.5, keys=[{"t": 0, "ey": 1.0}, {"t": d, "ey": 0.7, "ease": "suave"}]), *gotas],
             cam(1.0, 1.05), "corte", sfx=[(0.1, "agua", -20, {"dur": d})])


@v.plano(41, "un estudio de 1985: ocho voluntarios en fila")
def _(d):
    per = [IMG("perfil", ancho=150, x=120 + k * 120, y=1150, z=0.5, keys=aparece(0.05 + k * 0.08, 0.25)) for k in range(8)]
    return P(DIA, [BG("bg_dormitorio_dia"), *per], cam(1.0, 1.04, (540, 1100)), "corte", hud=[contexto(0.05, d - 0.05, "ESTUDIO DE 1985")],
             sfx=[(0.05 + k * 0.16, "pop", -24) for k in range(4)])


@v.plano(50, "ocho voluntarios")
def _(d):
    per = [IMG("perfil", ancho=150, x=120 + k * 120, y=1150, z=0.5, keys=late(0.05 + k * 0.05, 1, 0.08, 0.25)) for k in range(8)]
    return P(DIA, [BG("bg_dormitorio_dia"), *per], cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[contador(0.05, d - 0.05, 0, 8, d * 0.5, "VOLUNTARIOS", tam=120, y=560, borde=AMBAR, miles=False)], sfx=[(0.1, "pop", -18)])


@v.plano(52, "perdieron diecinueve milímetros: la regla de cerca")
def _(d):
    return P(DIA, [IMG("tallimetro", ancho=700, x=540, y=1000, z=0.45), marca(820, 1000, 0.1, d * 0.7, 540, 700)],
             cam(1.0, 1.05), "corte", hud=[contador(0.05, d - 0.05, 0, 19, d * 0.6, "MM", tam=140, y=560, borde=MAGENTA, miles=False, contar_prefijo="−")],
             sfx=[(0.1, "subida", -20, {"dur": d * 0.6})])


@v.plano(60, "casi dos centímetros")
def _(d):
    return P(DIA, [BG("bg_dormitorio_dia"), IMG("perfil", ancho=480, x=430, y=1080, z=0.5), IMG("tallimetro", ancho=300, x=780, y=1000, z=0.4),
             marca(340, 340, 0, 0.01, 640, 560, "#ffffff80"), marca(340, 400, 0.05, d * 0.6, 640, 560)],
             cam(1.0, 1.08, (600, 700), (620, 500)), "corte", hud=[rotulo(0.05, d - 0.05, "≈ 2 CM", tam=130, color="#141414", capsula="#ffe93de6", y=820)],
             sfx=[(d * 0.6, "golpe", -16)])


@v.plano(63, "lo más rápido: más de la mitad en la primera hora")
def _(d):
    return P(DIA, [BG("bg_dormitorio_dia"), IMG("perfil", ancho=300, x=540, y=1500, z=0.55, keys=[{"t": 0, "ey": 1.0}, {"t": d * 0.4, "ey": 0.97, "ease": "salida"}]),
             {"tipo": "barra", "x": 540, "y": 1050, "ancho": 860, "alto": 80, "color": MAGENTA, "fondo": "#ffffff40", "z": 0.6,
              "keys": [{"t": 0.05, "progreso": 0}, {"t": d * 0.4, "progreso": 0.54, "ease": "salida"}, {"t": d, "progreso": 0.6}]}],
             cam(1.0, 1.04), "corte", hud=[rotulo(0.05, d - 0.05, "1.ª HORA: +50 %", tam=96, color="#ffffff", capsula="#c0392be6", y=560)],
             sfx=[(0.05, "subida", -18, {"dur": d * 0.4})])


@v.plano(78, "de noche, tumbado: la columna tumbada se estira")
def _(d):
    return P(OSC, [BG("bg_dormitorio"), IMG("cama", ancho=1000, x=540, y=1550, z=0.4),
             *columna(150, 1050, 7, d, 0.2, d * 0.95, 0.45, 1.0, 200, 70, 50, 0.55, horizontal=True)],
             cam(1.0, 1.05, (540, 1200)), "desenfoque", hud=[contexto(0.05, d - 0.05, "DE NOCHE")], sfx=[(0.2, "burbuja", -18), (d * 0.5, "burbuja", -18)])


@v.plano(87, "recuperas siete de cada diez partes")
def _(d):
    return P(OSC, [BG("bg_dormitorio"),
             {"tipo": "barra", "x": 540, "y": 1100, "ancho": 860, "alto": 80, "color": CIAN, "fondo": "#ffffff20", "z": 0.6,
              "keys": [{"t": 0.05, "progreso": 0}, {"t": d * 0.6, "progreso": 0.7, "ease": "salida"}]},
             IMG("cojin", ancho=300, x=540, y=1450, z=0.55, keys=[{"t": 0, "ey": 0.6}, {"t": d * 0.6, "ey": 1.0, "ease": "rebote"}])],
             cam(1.0, 1.04), "corte", hud=[contador(0.05, d - 0.05, 0, 7, d * 0.6, "DE 10", tam=140, y=560, borde=CIAN, miles=False)],
             sfx=[(0.05, "subida", -18, {"dur": d * 0.6})])


@v.plano(99, "¿cómo lo sabemos? campo inglés al atardecer")
def _(d):
    return P(["#2a2050", "#ffc890"], [BG("bg_campo"), IMG("lupa", ancho=360, z=0.6, keys=[{"t": 0, "x": 300, "y": 1300}, {"t": d, "x": 700, "y": 1250, "ease": "suave"}])],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "¿CÓMO?", y=560, tam=130, color=AMBAR)], sfx=[(0.1, "roce", -20)])


@v.plano(102, "1724: el párroco con su vara de medir")
def _(d):
    return P(["#2a2050", "#ffc890"], [BG("bg_campo"), IMG("parroco", ancho=380, z=0.5, keys=[{"t": 0, "x": 120, "y": 1350}, {"t": d, "x": 420, "y": 1340, "ease": "suave"}], anim={"balanceo": [2, 0.9]}),
             polvo("#fff0c0", 25, (0, 900, 1080, 1600), 5)],
             cam(1.0, 1.06, (540, 1300)), "desenfoque", hud=[contexto(0.05, d - 0.05, "1724 · JOSEPH WASSE")], sfx=[(0.1, "brillo", -20)])


@v.plano(115, "midió también a su caballo después de galopar")
def _(d):
    return P(["#2a2050", "#ffc890"], [BG("bg_campo"), IMG("caballo", ancho=760, z=0.5, keys=[{"t": 0, "x": -400, "y": 1450}, {"t": d * 0.8, "x": 560, "y": 1450, "ease": "salida"}],
                                                       anim={"flotar": [18, 0.35]}),
             polvo("#c8a870", 40, (0, 1550, 1080, 1700), 9)],
             cam(1.0, 1.04, (540, 1400)), "corte", sfx=[(0.05 + k * 0.33, "golpe", -24) for k in range(int(d * 0.8 / 0.33))])


@v.plano(124, "y el caballo no encogía")
def _(d):
    return P(["#2a2050", "#ffc890"], [BG("bg_campo"), IMG("caballo", ancho=760, x=520, y=1450, z=0.5), IMG("tallimetro", ancho=200, x=920, y=1300, z=0.45),
             marca(1170, 1170, 0, 0.01, 820, 300, LIMA)],
             cam(1.0, 1.05, (600, 1350)), "corte", hud=[rotulo(0.05, d - 0.05, "NO ENCOGE", tam=110, color="#141414", capsula="#7dff3ae6", y=560)],
             sfx=[(0.1, "ding", -18)])


@v.plano(127, "en el espacio, sin gravedad: astronauta flotando")
def _(d):
    return P(["#02030a", "#0a1030"], [BG("bg_esp_violeta"), tierra(860, 1650, 700, 0.2, 3),
             IMG("astronauta", ancho=420, x=480, y=1000, z=0.5, anim={"flotar": [20, 2.2], "balanceo": [10, 3]}),
             IMG("satelite", ancho=160, z=0.3, keys=recorrido(v.w(127), v.w(150), (1150, 400), (-150, 700), d), anim={"girar": 5})],
             cam(1.0, 1.06), "desenfoque", hud=[contexto(0.05, d - 0.05, "SIN GRAVEDAD")], sfx=[(0.1, "brillo", -20)])


@v.plano(135, "los astronautas crecen hasta un tres por ciento")
def _(d):
    return P(["#02030a", "#0a1030"], [BG("bg_esp_violeta"), *columna(540, 1600, 6, d, 0.1, d * 0.9, 1.0, 1.7, 260, 90, 40, 0.5),
             IMG("satelite", ancho=160, z=0.3, keys=recorrido(v.w(127), v.w(150), (1150, 400), (-150, 700), d), anim={"girar": 5})],
             cam(1.0, 1.04), "corte", hud=[contador(0.05, d - 0.05, 0, 3, d * 0.6, "%", tam=150, y=560, borde=LIMA, miles=False, contar_prefijo="+")],
             sfx=[(0.1, "subida", -18, {"dur": d * 0.7})])


@v.plano(143, "unos cinco centímetros")
def _(d):
    return P(["#02030a", "#0a1030"], [BG("bg_esp_petroleo"), IMG("astronauta", ancho=380, x=400, y=1050, z=0.5, keys=[{"t": 0, "ey": 1.0}, {"t": d * 0.7, "ey": 1.05}], anim={"flotar": [14, 2]}),
             IMG("regla", ancho=760, x=760, y=1050, z=0.45, rot=90)],
             cam(1.0, 1.05), "corte", hud=[contador(0.05, d - 0.05, 0, 5, d * 0.6, "CM", tam=140, y=560, borde=LIMA, miles=False, contar_prefijo="+")],
             sfx=[(0.1, "subida", -20, {"dur": d * 0.6})])


@v.plano(146, "al volver, los pierden: la columna encoge de golpe")
def _(d):
    return P(["#2a2050", "#ffc890"], [BG("bg_campo"), *columna(540, 1600, 6, d, 0.1, d * 0.6, 1.7, 1.0, 260, 90, 40, 0.5),
             flecha([[540, 260], [540, 480]], 0.05, d * 0.5, MAGENTA, 12, z=0.7)],
             cam(1.0, 1.05, temblor=2), "corte", sfx=[(d * 0.6, "golpe", -14)])


@v.plano(150, "mídete mañana nada más despertar (bucle al tallímetro)")
def _(d):
    return P(["#2a1a3a", "#ffb46a"], [BG("bg_dormitorio_dia"), IMG("tallimetro", ancho=300, x=760, y=1000, z=0.4),
             IMG("perfil", ancho=420, x=480, y=1020, z=0.5), IMG("despertador", ancho=220, x=240, y=1500, z=0.6, anim={"balanceo": [8, 0.1]}),
             marca(470, 360, 0.1, d * 0.7, 600, 600, LIMA)],
             cam(1.0, 1.0, (540, 900), (540, 900)), "desenfoque", hud=[amarillo(0.05, d - 0.4, "MAÑANA", y=600, tam=110, color=LIMA)],
             sfx=[(0.1, "tictac", -22, {"dur": 0.8})])


# ------------------------------------------------------------------ micro planos
@v.plano(7, "micro: el sol entra por la ventana", mas=0.05)
def _(d):
    return P(DIA, [BG("bg_dormitorio_dia", ancho=2600), brillo(700, 420, 300, "#fff8d0", 0.6, 0.3, pulso=[0.3, 0.3])], cam(1.0, 1.1, (700, 560), (700, 520)), "corte", sfx=[(0.02, "brillo", -18)])


@v.plano(24, "micro: el agua del disco tiembla", mas=0.05)
def _(d):
    return P(["#0d1324", "#1f2b48"], [IMG("cojin", ancho=2200, x=540, y=1000, z=0.5, anim={"pulso": [0.03, 0.25]})], cam(1.0, 1.08), "corte", sfx=[(0.02, "burbuja", -18)])


@v.plano(35, "micro: un disco aplastado", mas=0.05)
def _(d):
    return P(OSC, [*columna(540, 1400, 3, d, 0.0, d * 0.8, 0.9, 0.35, 700, 220, 160, 0.5)], cam(1.0, 1.05, temblor=3), "corte", sfx=[(0.02, "golpe", -16)])


@v.plano(47, "micro: 1985 en el calendario", mas=0.05)
def _(d):
    return P(DIA, [IMG("calendario", ancho=600, x=540, y=1100, z=0.5, keys=late(0.0, 1, 0.08, 0.3))], cam(1.0, 1.1), "corte",
             hud=[rotulo(0.0, d - 0.03, "1985", tam=180, color="#141414", capsula=None, y=1180, sin_pop=True)], sfx=[(0.02, "pop", -18)])


@v.plano(75, "micro: la marca cae de golpe", mas=0.05)
def _(d):
    return P(DIA, [IMG("tallimetro", ancho=900, x=540, y=900, z=0.45), marca(600, 900, 0.0, d * 0.8, 540, 900)], cam(1.0, 1.08), "corte", sfx=[(0.02, "zap", -18)])


@v.plano(85, "micro: luna en la ventana", mas=0.05)
def _(d):
    return P(OSC, [BG("bg_dormitorio", ancho=2600)], cam(1.0, 1.1, (790, 560), (790, 540)), "corte", sfx=[(0.02, "brillo", -20)])


@v.plano(97, "micro: el disco se hincha", mas=0.05)
def _(d):
    return P(["#0d1324", "#1f2b48"], [IMG("cojin", ancho=800, x=540, y=1000, z=0.5, keys=[{"t": 0, "ey": 0.5}, {"t": d, "ey": 1.1, "ease": "rebote"}])],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "burbuja", -16)])


@v.plano(112, "micro: la vara de medir de cerca", mas=0.05)
def _(d):
    return P(["#2a2050", "#ffc890"], [IMG("parroco", ancho=1500, x=200, y=1500, z=0.5)], cam(1.0, 1.1, (540, 1000), (540, 900)), "corte", sfx=[(0.02, "tic", -18)])


@v.plano(122, "micro: cascos al galope", mas=0.05)
def _(d):
    return P(["#2a2050", "#ffc890"], [IMG("caballo", ancho=2400, x=540, y=600, z=0.5, anim={"flotar": [30, 0.3]}), polvo("#c8a870", 60, (0, 1300, 1080, 1700), 19)],
             cam(1.0, 1.1, temblor=6), "corte", sfx=[(0.02, "golpe", -16), (0.25, "golpe", -18)])


@v.plano(133, "micro: el casco del astronauta", mas=0.05)
def _(d):
    return P(["#02030a", "#0a1030"], [BG("bg_esp_violeta"), IMG("astronauta", ancho=1700, x=540, y=1500, z=0.5, anim={"flotar": [20, 2]})],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "senal", -22)])


@v.plano(141, "micro: los discos se inflan", mas=0.05)
def _(d):
    return P(["#02030a", "#0a1030"], [*columna(540, 1400, 3, d, 0.0, d * 0.8, 0.8, 1.5, 700, 220, 120, 0.5)], cam(1.0, 1.06), "corte", sfx=[(0.02, "burbuja", -16)])


v.construir("2026-11-18-tarde-03-mides-menos", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 63, "db": -13},
            claves=["menos", "levantarte", "vértebras", "discos", "agua", "gravedad", "líquido", "ocho", "diecinueve", "centímetros", "mitad", "noche", "siete", "Wasse", "caballo", "espacio", "tres", "cinco"])
