"""02 · Tu cerebro canta sin música (la canción pegada) — método denso. Lote 2026-11-19-manana, Agente 08:00 (Nico).
Experimento del lote: gancho de paradoja («Tu cerebro canta sin música.»).
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import math, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_hoy  # noqa: E402

SVG = ilus_hoy.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

NOC = ["#120a24", "#2a1448"]
OSC = ["#0a0c1a", "#1a2040"]
DIA = ["#f4dcb8", "#d8b890"]
NOTAS = ["nota", "nota_cian", "nota_lima", "nota_ambar"]


def orbita(cx, cy, rx, ry, d, n=4, ancho=150, vueltas=0.6, fase=0.0, z=0.6):
    """n notas que giran alrededor de (cx, cy): claves cada 0,1 de la duración."""
    els = []
    for k in range(n):
        ks = []
        for j in range(11):
            t = d * j / 10
            a = 2 * math.pi * (fase + k / n + vueltas * j / 10)
            ks.append({"t": round(t, 3), "x": cx + rx * math.cos(a), "y": cy + ry * math.sin(a), "rot": 12 * math.sin(a), "ease": "lineal"})
        els.append(IMG(NOTAS[k % 4], ancho=ancho, z=z + (0.05 if math.sin(2 * math.pi * (fase + k / n)) > 0 else -0.2), keys=ks))
    return els


def barra(y, p0, p1, t0, t1, color=MAGENTA, ancho=860, alto=70):
    return {"tipo": "barra", "x": 540, "y": y, "ancho": ancho, "alto": alto, "color": color, "fondo": "#ffffff30", "z": 0.6,
            "keys": [{"t": t0, "progreso": p0}, {"t": t1, "progreso": p1, "ease": "salida"}]}


def hueco(x, y, t0, t1, ancho=110, alto=90, color="#0a0c1a"):
    """Rectángulo oscuro que tapa un trozo de la barra (el silencio) y se va con t1."""
    return {"tipo": "forma", "forma": "rect", "ancho": ancho, "alto": alto, "relleno": color, "x": x, "y": y, "z": 0.65,
            "keys": [{"t": 0, "op": 0}, {"t": t0, "op": 1}, {"t": t1, "op": 1}, {"t": t1 + 0.25, "op": 0}]}


# ================================================================== PLANOS
@v.plano(0, "gancho: el cerebro entra y las notas le dan vueltas")
def _(d):
    return P(NOC, [BG("bg_esp_violeta"), brillo(540, 1050, 520, "#ff3df2", 0.35, 0.2, pulso=[0.12, 0.5]),
             IMG("cerebro", ancho=880, z=0.5, keys=arranque(540, 1080, d)), *orbita(540, 1080, 430, 260, d, 4, 170, 0.5)],
             cam(1.0, 1.04, (540, 1050), (540, 1000)), vineta=0.6, sfx=[(0.02, "whoosh", -12, {"dur": 0.6}), (0.4, "ding", -20)])


@v.plano(5, "nos pasa a casi todos: siluetas con una nota encima")
def _(d):
    gente = [IMG(n, ancho=380, x=x, y=1350, z=0.5, keys=aparece(0.05 + k * 0.1, 0.3)) for k, (n, x) in enumerate([("sil", 200), ("sil_m", 540), ("sil_a", 880)])]
    notas = [IMG(NOTAS[k], ancho=120, x=x, z=0.6, keys=[{"t": 0.2 + k * 0.1, "y": 1000, "op": 0}, {"t": 0.4 + k * 0.1, "op": 1}, {"t": d, "y": 900}], anim={"balanceo": [10, 0.6]})
             for k, x in enumerate([200, 540, 880])]
    return P(OSC, [BG("bg_salon"), *gente, *notas], cam(1.0, 1.04, (540, 1200)), "corte", hud=[amarillo(0.05, d - 0.03, "CASI TODOS", y=560, tam=110, color=CIAN)],
             sfx=[(0.05 + k * 0.1, "pop", -22) for k in range(3)])


@v.plano(10, "más de nueve de cada diez: diez perfiles, nueve con nota")
def _(d):
    per = [IMG("perfil_azul" if k < 9 else "perfil", ancho=150, x=95 + k * 99, y=1250, z=0.5, keys=aparece(0.03 + k * 0.05, 0.25)) for k in range(10)]
    nts = [IMG(NOTAS[k % 4], ancho=70, x=95 + k * 99, y=1040, z=0.6, keys=aparece(0.2 + k * 0.06, 0.3)) for k in range(9)]
    return P(OSC, [BG("bg_salon"), *per, *nts], cam(1.0, 1.04, (540, 1150)), "corte",
             hud=[contador(0.05, d - 0.05, 0, 9, d * 0.5, "DE 10", tam=130, y=560, borde=MAGENTA, miles=False)], sfx=[(0.05, "subida", -20, {"dur": d * 0.5})])


@v.plano(17, "tienen una canción pegada: la nota se pega a la cabeza")
def _(d):
    return P(NOC, [BG("bg_salon"), IMG("cara_perfil", ancho=820, x=460, y=1200, z=0.5),
             IMG("nota", ancho=220, z=0.6, keys=[{"t": 0, "x": 1000, "y": 500, "rot": 30}, {"t": d * 0.4, "x": 470, "y": 760, "rot": 0, "ease": "anticipa"}, {"t": d, "x": 470, "y": 760}]),
             senala(470, 760, d * 0.45, d - 0.05, 150, MAGENTA)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[amarillo(0.05, d - 0.03, "PEGADA", y=560, tam=110, color=MAGENTA)], sfx=[(d * 0.4, "golpe", -18)])


@v.plano(21, "al menos una vez por semana: el calendario con notas")
def _(d):
    nts = [IMG(NOTAS[k % 4], ancho=90, x=330 + k * 70, y=1110 + (k % 2) * 60, z=0.6, keys=aparece(0.1 + k * 0.1, 0.3)) for k in range(6)]
    return P(DIA, [BG("bg_dormitorio_dia"), IMG("calendario", ancho=620, x=540, y=1100, z=0.5), *nts],
             cam(1.0, 1.05), "corte", hud=[rotulo(0.05, d - 0.05, "CADA SEMANA", tam=96, color="#141414", capsula="#ffd23fe6", y=560)],
             sfx=[(0.1 + k * 0.1, "pop", -24) for k in range(4)])


@v.plano(27, "y casi nunca es entera: la barra de la canción se queda en un trozo")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), IMG("onda", ancho=500, x=540, y=900, z=0.4, anim={"pulso": [0.08, 0.5]}), barra(1250, 0, 0.18, 0.1, d * 0.6)],
             cam(1.0, 1.04), "corte", hud=[amarillo(0.05, d - 0.03, "¿ENTERA? NO", y=560, tam=110, color=AMBAR)], sfx=[(0.1, "roce", -20)])


@v.plano(32, "es un trozo, el estribillo: el trozo da la vuelta")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), barra(1250, 0.18, 0.18, 0, 0.01, AMBAR),
             flecha([[160, 1150], [160, 950], [540, 860], [920, 950], [920, 1150]], 0.1, d * 0.7, AMBAR, 10, z=0.6),
             *orbita(540, 1000, 300, 120, d, 3, 120, 0.4)],
             cam(1.0, 1.04), "corte", hud=[rotulo(0.05, d - 0.05, "ESTRIBILLO", tam=110, color="#141414", capsula="#ffb02ee6", y=560)], sfx=[(0.1, "ding", -22)])


@v.plano(39, "que da vueltas y vueltas: las notas giran rápido en la cabeza")
def _(d):
    return P(NOC, [BG("bg_esp_violeta"), IMG("sil", ancho=820, x=540, y=1300, z=0.45), *orbita(560, 950, 330, 140, d, 4, 130, 1.4)],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[amarillo(0.05, d - 0.03, "VUELTAS", y=560, tam=120, color=LIMA)], sfx=[(0.1, "whoosh", -24, {"dur": 0.5})])


@v.plano(44, "¿por qué? la lupa sobre el cerebro")
def _(d):
    return P(NOC, [BG("bg_esp_violeta"), IMG("cerebro", ancho=640, x=540, y=1100, z=0.45),
             IMG("lupa", ancho=380, z=0.6, keys=[{"t": 0, "x": 360, "y": 1300}, {"t": d, "x": 660, "y": 1000, "ease": "suave"}])],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "¿POR QUÉ?", y=560, tam=130, color=CIAN)], sfx=[(0.1, "roce", -20)])


@v.plano(46, "en dos mil cinco: hoja del calendario")
def _(d):
    return P(OSC, [BG("bg_aula"), IMG("hoja_2005", ancho=560, x=540, y=1000, z=0.5, keys=cae(0.0, 0.45, 600, 1000))], cam(1.0, 1.05), "corte", sfx=[(0.3, "golpe", -18)])


@v.plano(50, "en la universidad de Dartmouth: el aula con la pizarra")
def _(d):
    return P(OSC, [BG("bg_aula"), IMG("libro", ancho=420, x=780, y=1500, z=0.5, keys=aparece(0.1, 0.35)), polvo("#fff4c0", 25, (100, 400, 980, 1000), 5)],
             cam(1.0, 1.06, (540, 900), (540, 960)), "desenfoque", hud=[contexto(0.05, d - 0.05, "DARTMOUTH · EE. UU.")], sfx=[(0.1, "brillo", -20)])


@v.plano(55, "pusieron canciones conocidas a voluntarios: auriculares sobre la cabeza")
def _(d):
    return P(NOC, [BG("bg_aula"), IMG("cara_perfil", ancho=760, x=460, y=1250, z=0.5),
             IMG("auriculares", ancho=520, x=520, z=0.6, keys=[{"t": 0, "y": 300}, {"t": d * 0.5, "y": 860, "ease": "rebote"}, {"t": d, "y": 860}]),
             *[IMG(NOTAS[k], ancho=100, z=0.65, keys=[{"t": d * 0.5 + k * 0.1, "x": 760, "y": 900, "op": 0}, {"t": d * 0.5 + k * 0.1 + 0.1, "op": 1}, {"t": d, "x": 900 + k * 40, "y": 600 - k * 80}]) for k in range(3)]],
             cam(1.0, 1.05, (540, 1050)), "corte", sfx=[(d * 0.5, "pop", -18), (d * 0.6, "ding", -22)])


@v.plano(60, "dentro de un escáner: la camilla entra")
def _(d):
    return P(["#0d1a1a", "#1a3a3a"], [BG("bg_lab"), IMG("escaner", ancho=980, x=540, y=1150, z=0.5),
             brillo(620, 1080, 260, "#2ff3ff", 0.35, 0.55, pulso=[0.3, 0.5])],
             cam(1.0, 1.08, (540, 1150), (600, 1100)), "corte", hud=[amarillo(0.05, d - 0.03, "ESCÁNER", y=560, tam=120, color=CIAN)], sfx=[(0.1, "senal", -20)])


@v.plano(64, "y cortaron trocitos: huecos negros en la barra de la canción")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), barra(1100, 0, 1.0, 0.0, d * 0.5, CIAN),
             hueco(330, 1100, d * 0.35, d + 1), hueco(620, 1100, d * 0.5, d + 1), hueco(860, 1100, d * 0.6, d + 1)],
             cam(1.0, 1.04), "corte", hud=[amarillo(0.05, d - 0.03, "CORTES", y=560, tam=120, color=MAGENTA)], sfx=[(d * 0.35, "zap", -20), (d * 0.5, "zap", -20), (d * 0.6, "zap", -20)])


@v.plano(67, "silencio: pantalla casi negra", mas=0.05)
def _(d):
    return P(["#030308", "#0a0a14"], [IMG("auriculares", ancho=600, x=540, y=1050, z=0.5, keys=[{"t": 0, "escala": 1.05}, {"t": d, "escala": 1.0}])],
             cam(1.0, 1.05), "corte", vineta=0.8, hud=[amarillo(0.0, d - 0.03, "SILENCIO", y=560, tam=120, color="#ffffff")], sfx=[])


@v.plano(68, "pero su cerebro siguió sonando: el cerebro se ilumina y suelta notas")
def _(d):
    nts = [IMG(NOTAS[k % 4], ancho=120, z=0.6, keys=lanza(0.1 + k * 0.12, 0.6 + k * 0.12, (540, 1050), p)) for k, p in enumerate([(200, 700), (880, 700), (180, 1400), (900, 1400), (540, 560)])]
    return P(NOC, [BG("bg_esp_violeta"), brillo(540, 1050, 520, "#ff3df2", 0.6, 0.3, pulso=[0.2, 0.3]),
             IMG("cerebro", ancho=700, x=540, y=1050, z=0.5, keys=late(0.05, 2, 0.08, 0.35)), *nts],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "SIGUE SONANDO", y=560, tam=96, color=LIMA)], sfx=[(0.1, "ding", -20), (0.4, "ding", -24)])


@v.plano(73, "la zona del oído trabajaba: la oreja brilla y salen ondas")
def _(d):
    return P(NOC, [BG("bg_esp_petroleo"), IMG("oreja", ancho=560, x=400, y=1100, z=0.5),
             *[IMG("onda", ancho=300, x=700, y=1050, z=0.45, keys=[{"t": 0.1 + k * 0.3, "escala": 0.3, "op": 0}, {"t": 0.2 + k * 0.3, "op": 1}, {"t": 0.8 + k * 0.3, "escala": 1.8, "op": 0}]) for k in range(4)],
             brillo(450, 1050, 320, "#2ff3ff", 0.45, 0.4, pulso=[0.25, 0.4])],
             cam(1.0, 1.05), "corte", hud=[contexto(0.05, d - 0.05, "ZONA DEL OÍDO")], sfx=[(0.1, "brillo", -20)])


@v.plano(78, "como si la música continuara: notas que salen de la oreja")
def _(d):
    nts = [IMG(NOTAS[k % 4], ancho=110, z=0.6, keys=lanza(0.05 + k * 0.15, 0.5 + k * 0.15, (420, 1100), (850 - (k % 2) * 120, 600 + k * 110))) for k in range(5)]
    return P(NOC, [BG("bg_esp_petroleo"), IMG("oreja", ancho=520, x=380, y=1100, z=0.5), *nts], cam(1.0, 1.04), "corte",
             hud=[amarillo(0.05, d - 0.03, "CONTINÚA", y=560, tam=120, color=MAGENTA)], sfx=[(0.05 + k * 0.15, "pop", -24) for k in range(4)])


@v.plano(83, "tu cabeza rellena los huecos: los huecos de la barra se llenan")
def _(d):
    return P(OSC, [BG("bg_esp_petroleo"), IMG("sil", ancho=560, x=540, y=1500, z=0.45), barra(1000, 1.0, 1.0, 0, 0.01, CIAN),
             hueco(330, 1000, 0, d * 0.3), hueco(620, 1000, 0, d * 0.45), hueco(860, 1000, 0, d * 0.6)],
             cam(1.0, 1.04), "corte", hud=[amarillo(0.05, d - 0.03, "RELLENA", y=560, tam=120, color=CIAN)], sfx=[(d * 0.3, "pop", -20), (d * 0.45, "pop", -20), (d * 0.6, "pop", -20)])


@v.plano(89, "¿y por qué esa canción? el móvil vibra con una nota")
def _(d):
    return P(NOC, [BG("bg_salon"), IMG("movil_mano", ancho=620, x=540, y=1250, z=0.5, anim={"balanceo": [3, 0.15]}),
             IMG("nota", ancho=180, x=560, y=1100, z=0.6, keys=late(0.1, 2, 0.15, 0.3))],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "¿ESA?", y=560, tam=130, color=AMBAR)], sfx=[(0.1, "zap", -24)])


@v.plano(94, "cuanto más la oyes, más se pega: notas que se acumulan")
def _(d):
    nts = [IMG(NOTAS[k % 4], ancho=100, x=300 + (k % 4) * 160, y=850 - (k // 4) * 150, z=0.6, keys=aparece(0.05 + k * 0.1, 0.25)) for k in range(8)]
    return P(NOC, [BG("bg_salon"), IMG("movil_mano", ancho=520, x=540, y=1350, z=0.5), *nts],
             cam(1.0, 1.04, (540, 1100)), "corte", hud=[rotulo(0.05, d - 0.05, "MÁS OÍDA, MÁS PEGADA", tam=64, color="#141414", capsula="#ffd23fe6", y=480)],
             sfx=[(0.05 + k * 0.1, "pop", -26) for k in range(6)])


@v.plano(101, "en otro estudio, al día siguiente: despertador y nota en la almohada")
def _(d):
    return P(DIA, [BG("bg_dormitorio_dia"), IMG("cama", ancho=900, x=520, y=1500, z=0.4),
             IMG("despertador", ancho=280, x=820, y=1150, z=0.55, anim={"balanceo": [8, 0.1]}),
             IMG("nota_ambar", ancho=150, x=400, z=0.6, keys=[{"t": 0, "y": 1300, "op": 0}, {"t": 0.3, "op": 1}, {"t": d, "y": 1050}], anim={"balanceo": [10, 0.5]})],
             cam(1.0, 1.05, (600, 1300)), "corte", hud=[contexto(0.05, d - 0.05, "AL DÍA SIGUIENTE")], sfx=[(0.05, "tictac", -22, {"dur": 0.8})])


@v.plano(110, "en alemán lo llaman gusano del oído: el gusanito con auriculares")
def _(d):
    return P(["#1a2a12", "#3a5a24"], [BG("bg_campo"), IMG("gusano", ancho=820, z=0.5, keys=[{"t": 0, "x": 1300, "y": 1350}, {"t": d * 0.6, "x": 540, "y": 1350, "ease": "salida"}],
                                                      anim={"flotar": [12, 0.4]}),
             IMG("nota", ancho=110, x=760, z=0.6, keys=[{"t": d * 0.5, "y": 1100, "op": 0}, {"t": d * 0.6, "op": 1}, {"t": d, "y": 900}])],
             cam(1.0, 1.05, (540, 1300)), "corte", hud=[rotulo(0.05, d - 0.05, "GUSANO", tam=110, color="#141414", capsula="#7dff3ae6", y=560)],
             sfx=[(0.1, "roce", -20), (d * 0.6, "pop", -20)])


@v.plano(117, "¿cómo se quita? la nota se resiste")
def _(d):
    return P(NOC, [BG("bg_esp_violeta"), IMG("sil", ancho=820, x=540, y=1300, z=0.45), *orbita(560, 950, 300, 120, d, 3, 120, 0.6)],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "¿CÓMO?", y=560, tam=130, color=AMBAR)], sfx=[(0.05, "subida", -20, {"dur": d * 0.8})])


@v.plano(120, "en dos mil quince, en Reading: hoja del calendario sobre la ciudad")
def _(d):
    return P(["#2a3048", "#5a6a8a"], [BG("bg_londres"), IMG("hoja_2015", ancho=480, x=540, y=1050, z=0.5, keys=cae(0.0, 0.45, 600, 1050))],
             cam(1.0, 1.05), "desenfoque", hud=[contexto(0.05, d - 0.05, "READING · INGLATERRA")], sfx=[(0.3, "golpe", -18)])


@v.plano(127, "probaron algo muy simple", mas=0.0)
def _(d):
    return P(["#2a3048", "#5a6a8a"], [BG("bg_londres"), IMG("lupa", ancho=420, z=0.6, keys=[{"t": 0, "x": 300, "y": 1300}, {"t": d, "x": 700, "y": 1150, "ease": "suave"}])],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "MUY SIMPLE", y=560, tam=110, color=CIAN)], sfx=[(0.1, "roce", -20)])


@v.plano(131, "masticar chicle: cae el paquete y se infla el globo")
def _(d):
    return P(["#1a2a3a", "#2a4a6a"], [brillo(540, 1100, 520, "#ff7ab8", 0.4, 0.2), IMG("chicle", ancho=760, x=540, z=0.5, keys=cae(0.0, 0.45, 600, 1250)),
             IMG("globo_chicle", ancho=420, x=540, y=850, z=0.55, keys=[{"t": 0.4, "escala": 0.0}, {"t": d, "escala": 1.0, "ease": "salida"}])],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.05, d - 0.03, "CHICLE", y=480, tam=130, color=MAGENTA)], sfx=[(0.3, "golpe", -18), (0.5, "subida", -22, {"dur": 0.6})])


@v.plano(133, "bajaron un tercio: la barra baja y una nota se va")
def _(d):
    return P(["#1a2a3a", "#2a4a6a"], [barra(1150, 1.0, 0.67, 0.1, d * 0.6, MAGENTA),
             *[IMG(NOTAS[k], ancho=110, x=320 + k * 220, y=900, z=0.6, keys=([{"t": 0, "op": 1}, {"t": d * 0.5, "op": 0, "y": 700}] if k == 2 else [])) for k in range(3)]],
             cam(1.0, 1.04), "corte", hud=[rotulo(0.05, d - 0.05, "UN TERCIO", tam=110, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.1, "subida", -20, {"dur": d * 0.5}), (d * 0.6, "ding", -20)])


@v.plano(139, "masticar ocupa la voz interior: la cara mastica con globo y la nota se apaga")
def _(d):
    return P(NOC, [BG("bg_salon"), IMG("cara_perfil", ancho=820, x=420, y=1200, z=0.5),
             IMG("globo_chicle", ancho=260, x=790, y=1080, z=0.55, keys=[{"t": 0, "escala": 0.2}, {"t": d * 0.6, "escala": 1.0, "ease": "salida"}, {"t": d * 0.7, "escala": 0.0}]),
             IMG("nota", ancho=160, x=460, y=700, z=0.6, keys=[{"t": 0, "op": 1, "escala": 1.0}, {"t": d * 0.8, "op": 0.0, "escala": 0.4}])],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[contexto(0.05, d - 0.05, "VOZ INTERIOR")], sfx=[(d * 0.68, "pop", -16)])


@v.plano(147, "con la que repites la melodía", mas=0.0)
def _(d):
    return P(NOC, [BG("bg_esp_violeta"), IMG("onda", ancho=600, x=540, y=1000, z=0.5, keys=[{"t": 0, "escala": 1.2, "op": 1}, {"t": d, "escala": 0.4, "op": 0.2}])],
             cam(1.0, 1.04), "corte", hud=[amarillo(0.05, d - 0.03, "MELODÍA", y=560, tam=120, color=CIAN)], sfx=[(0.1, "roce", -22)])


@v.plano(150, "¿qué canción tienes tú ahora? (bucle al cerebro con notas)")
def _(d):
    return P(NOC, [BG("bg_esp_violeta"), brillo(540, 1050, 520, "#ff3df2", 0.35, 0.2, pulso=[0.12, 0.5]),
             IMG("cerebro", ancho=700, x=540, y=1080, z=0.5, keys=late(0.1, 1, 0.08, 0.4)), *orbita(540, 1080, 420, 250, d, 4, 160, 0.4)],
             cam(1.0, 1.0, (540, 1050), (540, 1050)), "desenfoque", hud=[rotulo(0.05, d - 0.4, "¿Y TÚ?", tam=120, color="#141414", capsula="#ffd23fe6", y=480)],
             sfx=[(0.1, "ding", -20)])


# ------------------------------------------------------------------ micro planos
@v.plano(3, "micro: una nota enorme gira", mas=0.05)
def _(d):
    return P(NOC, [brillo(540, 1000, 500, "#ff3df2", 0.4, 0.2), IMG("nota", ancho=700, x=540, y=1000, z=0.5, keys=[{"t": 0, "rot": -20, "escala": 0.8}, {"t": d, "rot": 15, "escala": 1.05, "ease": "salida"}])],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "ding", -20)])


@v.plano(36, "micro: el estribillo se repite (flecha en bucle)", mas=0.05)
def _(d):
    return P(OSC, [IMG("onda", ancho=900, x=540, y=1000, z=0.5, anim={"girar": 90})], cam(1.0, 1.1), "corte", sfx=[(0.02, "whoosh", -24)])


@v.plano(107, "micro: el despertador salta", mas=0.05)
def _(d):
    return P(DIA, [IMG("despertador", ancho=900, x=540, y=1000, z=0.5, anim={"balanceo": [10, 0.08]})], cam(1.0, 1.1, temblor=4), "corte", sfx=[(0.02, "tictac", -20, {"dur": 0.5})])


@v.plano(114, "micro: el gusano mueve la cabeza", mas=0.05)
def _(d):
    return P(["#1a2a12", "#3a5a24"], [IMG("gusano", ancho=1800, x=260, y=1100, z=0.5, anim={"balanceo": [6, 0.3]})], cam(1.0, 1.08), "corte", sfx=[(0.02, "pop", -18)])


@v.plano(136, "micro: el globo de chicle explota", mas=0.05)
def _(d):
    return P(["#1a2a3a", "#2a4a6a"], [IMG("globo_chicle", ancho=900, x=540, y=1000, z=0.5, keys=[{"t": 0, "escala": 0.8}, {"t": d * 0.7, "escala": 1.2}, {"t": d * 0.75, "escala": 0.0}])],
             cam(1.0, 1.06), "corte", sfx=[(d * 0.72, "pop", -12)])


v.construir("2026-11-19-manana-02-cancion-pegada", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 72, "db": -13},
            claves=["cerebro", "música", "todos", "nueve", "pegada", "semana", "trozo", "estribillo", "vueltas", "Dartmouth", "escáner", "Silencio.",
                    "oído", "huecos", "gusano", "chicle", "tercio", "ahora?"])
