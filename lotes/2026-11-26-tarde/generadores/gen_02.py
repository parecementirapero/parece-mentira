"""02 · Nunca verás esta cara de la Luna — método denso, estilo del vídeo largo. Lote 2026-11-26-tarde (Agente 20:00 (Jorge)).
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import math, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comun_1126t as C  # noqa: E402
from comun_1126t import *  # noqa: E402,F401,F403
import ilus_1126t  # noqa: E402

SVG = ilus_1126t.generar(os.path.join(sys.argv[1], "_svg_lote"))
C.SVG_DIR = SVG
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
ESP = ["#02030a", "#0a1030"]
S_V = SUELO["bg_via_lactea"]


def orbita(d, cx, cy, r, vueltas, ancho, n="luna_llena", fase0=-90, z=0.55):
    """La Luna da vueltas alrededor de (cx, cy) mirando siempre hacia el centro (misma cara)."""
    ks, pasos = [], 24
    for i in range(pasos + 1):
        f = i / pasos
        a = math.radians(fase0 + 360 * vueltas * f)
        ks.append({"t": round(d * f, 3), "x": cx + r * math.cos(a), "y": cy + r * math.sin(a) * 0.9, "rot": round(math.degrees(a) + 90, 1), "ease": "lineal"})
    return OB(n, ks[0]["x"], ks[0]["y"], ancho, z=z, keys=ks)


@v.plano(0, "gancho: la cara oculta enorme girando despacio, con luz de borde")
def _(d):
    return P(ESP, [estrellas(120, 2), OB("luna_oculta", 540, 1000, 960, keys=arranque(540, 1000, d, "derecha", 300, 30) + [{"t": 0, "rot": -20}, {"t": d, "rot": 8, "ease": "suave"}]),
                   brillo(540, 1000, 560, "#cfe0ff", 0.3, 0.04)],
             cam(1.0, 1.06, (540, 1000)), vineta=0.4, sfx=[(0.02, "whoosh", -18), (0.4, "brillo", -20)])


@v.plano(4, "la Luna esconde la mitad: la cara visible tapa a la otra")
def _(d):
    return P(ESP, [estrellas(100, 3), OB("luna_oculta", 540, 1000, 820, z=0.4, keys=[{"t": 0, "x": 540}, {"t": d, "x": 860, "op": 0.6, "ease": "suave"}]),
                   OB("luna_llena", 540, 1000, 820, z=0.55, keys=[{"t": 0, "x": 1300}, {"t": 0.5, "x": 540, "ease": "salida"}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.15, d - 0.05, "LA MITAD", "#141414", "#7df9ffe6", 120)], sfx=[(0.1, "whoosh", -18)])


@v.plano(9, "desde la Tierra: persona mirando la Luna llena en el cielo")
def _(d):
    return P(ESP, [BG("bg_via_lactea"), OB("luna_llena", 700, 600, 300, z=0.2, keys=late(0.6, 1, 0.06)), PZ("mira_arriba", 360, S_V, 820)],
             cam(1.0, 1.05, (540, 1100)), "desenfoque", sfx=[(0.1, "rumor", -28, {"dur": d})])


@v.plano(12, "siempre vemos el mismo lado: la cara visible en grande con su mancha señalada")
def _(d):
    return P(ESP, [estrellas(90, 4), OB("luna_llena", 540, 1000, 860, keys=[{"t": 0, "escala": 0.96}, {"t": d, "escala": 1.02}]), senala(480, 900, 0.2, d - 0.1, 220, CIAN)],
             cam(1.0, 1.04, (540, 1000)), "corte", hud=[cap(0.05, d - 0.05, "EL MISMO LADO", tam=86)], sfx=[(0.2, "senal", -22)])


@v.plano(17, "¿por qué?: la chica que mira las estrellas")
def _(d):
    return P(ESP, [BG("bg_via_lactea"), OB("cara_mira_estrellas", 540, 1150, 900, keys=[{"t": 0, "escala": 1.05}, {"t": d, "escala": 1.0, "ease": "salida"}])],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[amarillo(0.05, d - 0.03, "¿POR QUÉ?", y=600, tam=130, color=AMBAR)], sfx=[(0.05, "impacto", -18)])


@v.plano(19, "porque gira sobre sí misma: la Luna rota sobre su eje")
def _(d):
    return P(ESP, [estrellas(90, 5), OB("luna_llena", 540, 1000, 760, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 120, "ease": "lineal"}]),
                   flecha([[220, 650], [540, 520], [860, 650]], 0.1, 0.7, MAGENTA, 12, z=0.7)],
             cam(1.0, 1.04, (540, 1000)), "corte", hud=[cap(0.3, d - 0.05, "GIRA", "#ffffff", "#c0392be6", 120)], sfx=[(0.1, "whoosh", -20)])


@v.plano(24, "justo una vez por cada vuelta: la Luna orbita la Tierra mirándola siempre")
def _(d):
    return P(ESP, [estrellas(90, 6), OB("foto_mundo", 540, 1050, 340, z=0.45, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 60}]),
                   orbita(d, 540, 1050, 360, 0.9, 190),
                   {"tipo": "forma", "forma": "elipse", "ancho": 720, "alto": 650, "relleno": "#ffffff", "op_relleno": 0, "grosor": 4, "borde": "#7df9ff66", "x": 540, "y": 1050, "z": 0.4}],
             cam(1.0, 1.03, (540, 1050)), "corte", hud=[cap(0.4, d - 0.05, "1 GIRO = 1 VUELTA", "#141414", "#7df9ffe6", 86)], sfx=[(0.1, "senal", -22)])


@v.plano(33, "en unos veintisiete días: las hojas del calendario vuelan")
def _(d):
    return P(ESP, [estrellas(80, 7), OB("calendario_taco", 540, 1100, 520, keys=aparece(0.0) + late(0.4, 2, 0.06))],
             cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[contador(0.05, d - 0.05, 1, 27, max(0.4, d * 0.6), " DÍAS", tam=130, color="#141414", capsula="#ffd23fe6", y=620)], sfx=[(0.05, "tic", -18)])


@v.plano(37, "hace miles de millones de años giraba más rápido: la Luna da vueltas deprisa")
def _(d):
    return P(["#1a0a06", "#05030a"], [estrellas(90, 8), OB("luna_llena", 540, 1000, 700, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 900, "ease": "lineal"}]),
                                     brillo(540, 1000, 450, "#ff9a50", 0.3, 0.05)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.2, d - 0.05, "MÁS RÁPIDO", "#ffffff", "#c0392be6", 110)], sfx=[(0.1, "whoosh", -16), (0.8, "whoosh", -20)])


@v.plano(46, "pero la gravedad de la Tierra la estiró: la Luna se alarga hacia la Tierra")
def _(d):
    return P(ESP, [estrellas(80, 9), OB("foto_mundo", 220, 1050, 380, z=0.45),
                   OB("luna_llena", 760, 1050, 420, keys=[{"t": 0, "ex": 1.0, "ey": 1.0}, {"t": d * 0.7, "ex": 1.22, "ey": 0.9, "ease": "suave"}]),
                   flecha([[420, 1050], [520, 1050]], 0.2, 0.6, CIAN, 14, z=0.7), flecha([[1000, 1050], [990, 1050]], 0.2, 0.6, CIAN, 14, punta=False, z=0.7)],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[cap(0.3, d - 0.05, "GRAVEDAD", "#141414", "#7df9ffe6", 110)], sfx=[(0.2, "senal", -20)])


@v.plano(54, "y ese roce la fue frenando: la Luna gira cada vez más despacio")
def _(d):
    return P(ESP, [estrellas(80, 10), OB("luna_llena", 540, 1000, 700, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 160, "ease": "salida"}]),
                   brillo(540, 1000, 420, "#ff6a3a", 0.3, 0.05, keys=[{"t": 0, "op": 0.8}, {"t": d, "op": 0.1}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.3, d - 0.05, "FRENO", "#ffffff", "#c0392be6", 120)], sfx=[(0.2, "roce", -18)])


@v.plano(60, "hasta dejarla así, mirándonos: la Luna quieta frente a la Tierra")
def _(d):
    return P(ESP, [estrellas(80, 11), OB("foto_mundo", 540, 1400, 520, z=0.45, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 20}]),
                   OB("luna_llena", 540, 760, 360, z=0.55, keys=late(0.3, 1, 0.05)), flecha([[540, 960], [540, 1110]], 0.2, 0.6, "#ffffffaa", 6, disc=[14, 10], z=0.5)],
             cam(1.0, 1.04, (540, 1050)), "corte", sfx=[(0.2, "pop", -22)])


@v.plano(64, "a la otra cara la llaman el lado oscuro: cara oculta en sombra")
def _(d):
    return P(["#000000", "#05060c"], [estrellas(60, 12), OB("luna_oculta", 540, 1000, 820, keys=[{"t": 0, "op": 0.25}, {"t": d, "op": 0.4}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[amarillo(0.2, d - 0.05, "¿LADO OSCURO?", y=620, tam=110, color=CIAN)], sfx=[(0.1, "rumor", -26, {"dur": d})])


@v.plano(73, "pero recibe tanto sol como esta: el sol la ilumina entera")
def _(d):
    return P(ESP, [estrellas(60, 13), OB("rayo_sol", 200, 600, 600, z=0.3, keys=[{"t": 0, "op": 0}, {"t": 0.3, "op": 1}]), brillo(160, 560, 520, "#ffd890", 0.6, 0.06),
                   OB("luna_oculta", 620, 1100, 760, keys=[{"t": 0, "op": 0.35}, {"t": 0.5, "op": 1, "ease": "suave"}])],
             cam(1.0, 1.04, (540, 1000)), "corte", hud=[cap(0.4, d - 0.05, "TANTO SOL", "#141414", "#ffd23fe6", 110)], sfx=[(0.2, "brillo", -18)])


@v.plano(79, "o incluso un poco más: la Tierra tapa el sol a la cara visible en un eclipse")
def _(d):
    return P(ESP, [estrellas(60, 14), brillo(120, 1000, 420, "#ffd890", 0.6, 0.06), OB("foto_mundo", 460, 1000, 300, z=0.45),
                   OB("luna_llena", 820, 1000, 200, z=0.5, keys=[{"t": 0, "op": 1}, {"t": d * 0.6, "op": 0.35, "ease": "suave"}])],
             cam(1.0, 1.04, (540, 1000)), "corte", hud=[cap(0.2, d - 0.05, "UN POCO MÁS", "#141414", "#ffd23fe6", 100)], sfx=[(0.2, "pop", -22)])


@v.plano(84, "la primera foto llegó en mil novecientos cincuenta y nueve: la sonda cruza")
def _(d):
    return P(ESP, [estrellas(80, 15), OB("luna_oculta", 820, 1300, 600, z=0.35),
                   OB("sonda_luna3", 540, 900, 520, keys=[{"t": 0, "x": -200, "rot": -8}, {"t": d, "x": 520, "rot": 4, "ease": "salida"}])],
             cam(1.0, 1.04, (540, 1000)), "corte",
             hud=[contador(0.05, min(1.2, d - 0.05), 1900, 1959, 0.7, miles=False, tam=150, color="#141414", capsula="#ffffffe6", y=620)], sfx=[(0.05, "whoosh", -18)])


@v.plano(94, "desde una sonda soviética: la sonda en grande con antenas")
def _(d):
    return P(ESP, [estrellas(80, 16), OB("sonda_luna3", 540, 1050, 900, keys=[{"t": 0, "rot": -4}, {"t": d, "rot": 4}] + flota(d, 10, 1050))],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[cap(0.2, d - 0.05, "SONDA SOVIÉTICA", tam=90)], sfx=[(0.1, "senal", -20)])


@v.plano(98, "y salió borrosa: la foto antigua llena de ruido")
def _(d):
    return P(["#1a1a1a", "#050505"], [OB("foto_borrosa", 540, 1050, 760, keys=aparece(0.0) + [{"t": 0, "rot": -4}, {"t": d, "rot": 2}])],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[cap(0.05, d - 0.05, "BORROSA", "#ffffff", "#c0392be6", 120)], sfx=[(0.05, "zap", -20)])


@v.plano(101, "en mil novecientos sesenta y ocho: la nave rodea la Luna")
def _(d):
    return P(ESP, [estrellas(80, 17), OB("luna_oculta", 540, 1300, 900, z=0.35, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 8}]),
                   OB("capsula_apolo", 540, 720, 520, keys=[{"t": 0, "x": 1300}, {"t": d, "x": 520, "ease": "salida"}])],
             cam(1.0, 1.04, (540, 1000)), "corte",
             hud=[contador(0.05, min(1.2, d - 0.05), 1900, 1968, 0.7, miles=False, tam=150, color="#141414", capsula="#ffffffe6", y=1000)], sfx=[(0.05, "whoosh", -18)])


@v.plano(107, "los tres astronautas del Apolo ocho: la nave pasa sobre los cráteres")
def _(d):
    return P(ESP, [OB("luna_oculta", 540, 1700, 1800, z=0.3, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 10}]), estrellas(60, 18),
                   OB("capsula_apolo", 540, 800, 760, keys=flota(d, 12, 800))],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.3, d - 0.05, "3 ASTRONAUTAS", "#141414", "#7df9ffe6", 100)], sfx=[(0.1, "senal", -22)])


@v.plano(113, "fueron los primeros en verla con sus propios ojos: un ojo que refleja la Luna")
def _(d):
    return P(ESP, [estrellas(60, 19), OB("ojo", 540, 1050, 860, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.06}]),
                   OB("luna_oculta", 540, 1050, 160, z=0.6, keys=[{"t": 0, "op": 0}, {"t": 0.3, "op": 0.85}])],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[cap(0.3, d - 0.05, "LOS PRIMEROS", "#141414", "#ffd23fe6", 100)], sfx=[(0.2, "brillo", -20)])


@v.plano(122, "y en dos mil diecinueve: cifra que corre")
def _(d):
    return P(ESP, [estrellas(80, 20), OB("luna_oculta", 540, 1050, 700)], cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[contador(0.05, d - 0.05, 2000, 2019, 0.5, miles=False, tam=150, color="#141414", capsula="#ffffffe6", y=620)], sfx=[(0.05, "tic", -18)])


@v.plano(127, "China aterrizó allí por primera vez: el módulo baja y se posa")
def _(d):
    return P(ESP, [estrellas(80, 21), OB("luna_oculta", 540, 2100, 2200, z=0.3),
                   OB("aterrizador", 540, 1150, 720, keys=cae(0.0, min(0.9, d * 0.6), 500, 1150))],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[cap(0.4, d - 0.05, "PRIMERA VEZ", "#141414", "#5dff8ae6", 100)], sfx=[(0.5, "golpe", -16)])


@v.plano(133, "es otra Luna: las dos caras lado a lado")
def _(d):
    return P(ESP, [estrellas(80, 22), OB("luna_llena", 290, 1050, 460, keys=aparece(0.0)), OB("luna_oculta", 790, 1050, 460, keys=aparece(0.15))],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[cap(0.05, d - 0.05, "OTRA LUNA", tam=100)], sfx=[(0.0, "pop", -22), (0.15, "pop", -22)])


@v.plano(136, "casi sin manchas oscuras: se señalan las manchas de la visible y no hay en la oculta")
def _(d):
    return P(ESP, [estrellas(80, 22), OB("luna_llena", 290, 1050, 460), OB("luna_oculta", 790, 1050, 460), senala(270, 1000, 0.1, d - 0.1, 150, MAGENTA),
                   senala(790, 1050, 0.4, d - 0.1, 230, CIAN)],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[cap(0.2, d - 0.05, "SIN MANCHAS", "#141414", "#7df9ffe6", 100)], sfx=[(0.1, "senal", -22)])


@v.plano(140, "y llena de cráteres: acercamiento a los cráteres")
def _(d):
    return P(ESP, [OB("luna_oculta", 540, 1000, 1700, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.12, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.05, d - 0.05, "CRÁTERES", "#ffffff", "#c0392be6", 120)], sfx=[(0.1, "impacto", -18)])


@v.plano(144, "¿sabías que nunca la habías visto? (bucle): la cara oculta gira como al principio")
def _(d):
    return P(ESP, [estrellas(120, 2), OB("luna_oculta", 540, 1000, 960, keys=[{"t": 0, "rot": 10}, {"t": d, "rot": -20, "ease": "suave"}]), brillo(540, 1000, 560, "#cfe0ff", 0.3, 0.04)],
             cam(1.04, 1.0, (540, 1000)), "corte", sfx=[(0.1, "brillo", -20)])


def micro(fondo, els, txt=None, col="#ffffff", cap_f="#c0392be6", sfx="pop"):
    def fn(d):
        return P(fondo, els(d), cam(1.15, 1.3, (540, 1000)), "corte", hud=[cap(0.0, d - 0.02, txt, col, cap_f, 130)] if txt else [], sfx=[(0.01, sfx, -18)])
    return fn


v.plano(16, "micro: media Luna en sombra")(micro(ESP, lambda d: [OB("luna_llena", 540, 1000, 1100, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 10}])], sfx="pop"))
v.plano(36, "micro: 27 enorme")(micro(ESP, lambda d: [estrellas(80, 7), brillo(540, 1000, 400, "#ffd23f", 0.5, 0.06)], "27", "#141414", "#ffd23fe6", "impacto"))
v.plano(70, "micro: la cara oculta apagada")(micro(["#000000", "#05060c"], lambda d: [OB("luna_oculta", 540, 1000, 1300, keys=[{"t": 0, "op": 0.3}, {"t": d, "op": 0.2}])], sfx="rumor"))
v.plano(119, "micro: el ojo se abre")(micro(ESP, lambda d: [OB("ojo", 540, 1000, 1200, keys=[{"t": 0, "ey": 0.3}, {"t": 0.2, "ey": 1.0, "ease": "salida"}])], sfx="brillo"))


v.construir("2026-11-26-tarde-02-cara-oculta-luna", version=1, bucle=0.35, musica={"generar": "misterio", "semilla": 1262, "db": -13},
            claves=["cara", "Luna", "mitad", "Tierra", "lado", "gira", "vuelta", "veintisiete", "rápido", "gravedad", "roce", "frenando", "oscuro", "sol",
                    "foto", "sonda", "borrosa", "astronautas", "Apolo", "ojos", "China", "aterrizó", "manchas", "cráteres"],
            ep_extra={"sfx_bajo_voz": True})
