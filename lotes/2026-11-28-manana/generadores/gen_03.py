"""03 · El vidrio no se escurre (las vidrieras antiguas no son más gruesas abajo porque el vidrio fluya) — método denso,
estilo del vídeo largo. Lote 2026-11-28-manana (Agente 08:00 (Nico)).
La toma salió a 60,7 s: se quitan dos frases enteras con `omitir` («Siglos goteando hacia el suelo.» y «Mucho menos que un virus.»).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comun_1128m as C  # noqa: E402
from comun_1128m import *  # noqa: E402,F401,F403
import ilus_1128m  # noqa: E402

SVG = ilus_1128m.generar(os.path.join(sys.argv[1], "_svg_lote"))
C.SVG_DIR = SVG
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG,
          omitir=[(32, 37), (122, 127)] if len(VOZ) == 2 else ())
CAT = ["#0e0c14", "#2a2420"]
TALLER = ["#140a06", "#2a160c"]
ESP = ["#02030a", "#0a1030"]
LAB = ["#101826", "#1e2a3a"]
CIAN, LIMA, MAGENTA = "#2ff3ff", "#5dff8a", "#ff4ad8"
S = SUELO["bg_catedral"]


def vid(x=540, y=980, ancho=640, gotea=False, keys=None, z=0.4):
    return OB("vidriera_gotea" if gotea else "vidriera", x, y, ancho, z=z, keys=keys)


def gotas(x0, y0, d, sem=0):
    els = []
    for k, x in enumerate((x0 - 200, x0 - 80, x0 + 40, x0 + 170)):
        t0 = (k * 0.37 + sem * 0.2) % 0.9
        els.append(OB("gota", x, y0, 46, z=0.6, keys=[{"t": 0, "op": 0, "y": y0}, {"t": t0, "op": 1, "y": y0}, {"t": t0 + 0.8, "y": y0 + 520, "op": 1, "ease": "entrada"}, {"t": t0 + 0.85, "op": 0}]))
    return els


@v.plano(0, "gancho: una vidriera de catedral que parece derretirse; caen gotas de colores")
def _(d):
    return P(CAT, [BG("bg_catedral"), vid(540, 1060, 700, True, keys=[{"t": 0, "y": 1010}, {"t": d, "y": 1060}])] + gotas(540, 1620, d),
             cam(1.0, 1.08, (540, 1100)), vineta=0.35, sfx=[(0.0, "whoosh", -16), (0.4, "agua", -22)])


@v.plano(5, "seguro te lo contaron así: una chica pensativa")
def _(d):
    return P(CAT, [BG("bg_catedral"), OB("cara_chica_pensativa", 540, 1200, 860, keys=aparece(0.0))],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[cap(0.3, d - 0.05, "TE LO CONTARON", "#141414", "#ffd23fe6", 96, y=560)], sfx=[(0.1, "pop", -20)])


@v.plano(10, "el vidrio es un líquido muy lento: el cristal ondula y un caracol lo adelanta")
def _(d):
    return P(LAB, [BG("bg_galeria"), OB("panel_vidrio", 540, 1000, 520, keys=[{"t": 0, "rot": -2}, {"t": d * 0.5, "rot": 2, "ease": "suave"}, {"t": d, "rot": -2, "ease": "suave"}]),
                   OB("caracol", 300, 1500, 260, z=0.6, keys=[{"t": 0, "x": 200}, {"t": d, "x": 420, "ease": "lineal"}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[cap(0.3, d - 0.05, "¿LÍQUIDO LENTO?", "#141414", "#7df9ffe6", 96, y=560)], sfx=[(0.1, "roce", -22)])


@v.plano(17, "por eso las ventanas de las catedrales antiguas: la cámara sube por la nave hasta la vidriera")
def _(d):
    return P(CAT, [BG("bg_catedral"), vid(540, 1000, 600)], cam(1.15, 1.15, (540, 1500), (540, 800)), "corte",
             hud=[cap(0.3, d - 0.05, "CATEDRALES", "#ffffff", "#c0392be6", 100, y=1450)], sfx=[(0.1, "whoosh", -20)])


@v.plano(26, "son más gruesas abajo que arriba: corte del cristal con dos flechas")
def _(d):
    return P(LAB, [BG("bg_galeria"), OB("corte_cristal", 540, 1050, 380, keys=aparece(0.0)),
                   flecha([[200, 640], [470, 640]], 0.2, 0.5, CIAN, 9, z=0.7), flecha([[880, 1460], [640, 1460]], 0.5, 0.9, AMBAR, 12, z=0.7)],
             cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[cap(0.2, d - 0.05, "FINO", "#141414", "#7df9ffe6", 90, y=560, x=250), cap(0.5, d - 0.05, "GRUESO", "#141414", "#ffd23fe6", 90, y=1360, x=820)],
             sfx=[(0.2, "tic", -20), (0.5, "tic", -20)])


@v.plano(37, "suena precioso…: la vidriera brilla con la luz")
def _(d):
    return P(CAT, [BG("bg_catedral"), vid(540, 1000, 640), brillo(540, 900, 420, "#ffe0a0", 0.4, 0.5, keys=late(0.1, 2, 0.1, 0.6))],
             cam(1.05, 1.1, (540, 1000)), "corte", sfx=[(0.1, "brillo", -18)])


@v.plano(39, "pero es falso: la vidriera que gotea se tacha")
def _(d):
    return P(CAT, [BG("bg_catedral"), vid(540, 1000, 600, True)] + tacha(540, 1000, 0.2, 280),
             cam(1.1, 1.15, (540, 1050)), "corte", hud=[cap(0.2, d - 0.05, "FALSO", "#ffffff", "#c0392be6", 140, y=1250)], sfx=[(0.2, "impacto", -16)])


@v.plano(42, "¿entonces por qué son más gruesas?: el corte del cristal gira")
def _(d):
    return P(LAB, [BG("bg_galeria"), OB("corte_cristal", 540, 1050, 380, keys=[{"t": 0, "rot": -8}, {"t": d, "rot": 8, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[amarillo(0.1, d - 0.05, "¿POR QUÉ?", y=560, tam=130, color=CIAN)], sfx=[(0.1, "pop", -20)])


@v.plano(48, "aquellos cristales se hacían a mano: taller con el horno al rojo y el cristalero")
def _(d):
    return P(TALLER, [BG("bg_taller_vidrio"), PZ("cristalero", 300, 1560, 760, z=0.6, keys=aparece(0.1))],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[cap(0.3, d - 0.05, "A MANO", "#141414", "#ffd23fe6", 110, y=560)], sfx=[(0.1, "rumor", -22)])


@v.plano(54, "se soplaba una bola: la bola al rojo se hincha en la punta de la caña")
def _(d):
    return P(TALLER, [BG("bg_taller_vidrio"), OB("bola_vidrio", 540, 1050, 500, keys=[{"t": 0, "ancho": 500}, {"t": d, "ancho": 900, "ease": "salida"}])],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[cap(0.2, d - 0.05, "BOLA", "#141414", "#ffd23fe6", 110, y=560)], sfx=[(0.1, "subida", -20)])


@v.plano(58, "o un cilindro de vidrio: el cilindro aparece y se marca el corte")
def _(d):
    return P(TALLER, [BG("bg_taller_vidrio"), OB("cilindro_vidrio", 540, 1050, 520, keys=aparece(0.0))],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[cap(0.2, d - 0.05, "CILINDRO", "#141414", "#7df9ffe6", 110, y=560)], sfx=[(0.1, "pop", -20)])


@v.plano(63, "se abría y se aplanaba: el disco de vidrio gira y se extiende")
def _(d):
    return P(TALLER, [BG("bg_taller_vidrio"), OB("disco_vidrio", 540, 1050, 600, keys=[{"t": 0, "rot": 0, "ancho": 300}, {"t": d, "rot": 300, "ancho": 860, "ease": "salida"}])],
             cam(1.0, 1.03, (540, 1050)), "corte", hud=[cap(0.3, d - 0.05, "SE APLANABA", "#141414", "#ffd23fe6", 100, y=1600)], sfx=[(0.1, "whoosh", -18)])


@v.plano(68, "nunca salía igual de grueso por todas partes: flechas al centro grueso y al borde fino")
def _(d):
    return P(TALLER, [BG("bg_taller_vidrio"), OB("disco_vidrio", 540, 1050, 820, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 20}]),
                      flecha([[540, 600], [540, 980]], 0.1, 0.5, AMBAR, 12, z=0.7), flecha([[1000, 1500], [880, 1360]], 0.5, 0.9, CIAN, 10, z=0.7)],
             cam(1.0, 1.04, (540, 1050)), "corte",
             hud=[cap(0.1, d - 0.05, "GRUESO", "#141414", "#ffd23fe6", 90, y=520), cap(0.5, d - 0.05, "FINO", "#141414", "#7df9ffe6", 90, y=1580, x=800)],
             sfx=[(0.1, "tic", -20), (0.5, "tic", -20)])


@v.plano(76, "y el cristalero: sostiene el cristal delante de la ventana")
def _(d):
    return P(CAT, [BG("bg_catedral"), PZ("cristalero", 380, S, 900, z=0.5), OB("panel_vidrio", 560, 1150, 300, z=0.6, keys=[{"t": 0, "rot": -10}, {"t": d, "rot": -4}])],
             cam(1.0, 1.05, (500, 1150)), "corte", sfx=[(0.1, "pop", -22)])


@v.plano(79, "casi siempre, ponía la parte gruesa abajo: el cristal baja y encaja en el marco con lo grueso abajo")
def _(d):
    return P(CAT, [BG("bg_catedral"), vid(540, 1000, 640), OB("panel_vidrio", 540, 1250, 300, z=0.6, keys=cae(0.1, min(0.8, d * 0.4), 600, 1250)),
                   flecha([[900, 1500], [720, 1390]], min(0.9, d * 0.45), min(1.3, d * 0.6), AMBAR, 12, z=0.7)],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[cap(min(0.9, d * 0.45), d - 0.05, "GRUESO ABAJO", "#141414", "#ffd23fe6", 96, y=1600)],
             sfx=[(min(0.8, d * 0.4), "golpe", -20)])


@v.plano(86, "¿y si de verdad fluyera?: la vidriera vuelve a gotear")
def _(d):
    return P(CAT, [BG("bg_catedral"), vid(540, 1000, 600, True)] + gotas(540, 1560, d, 1), cam(1.1, 1.15, (540, 1150)), "corte",
             hud=[amarillo(0.0, d - 0.02, "¿Y SI FLUYERA?", y=560, tam=110, color=CIAN)], sfx=[(0.1, "agua", -20)])


@v.plano(91, "en dos mil diecisiete, un equipo: la investigadora con el cristal")
def _(d):
    return P(LAB, [BG("bg_galeria"), PZ("investigadora", 380, 1600, 860, z=0.5, keys=aparece(0.0)), OB("panel_vidrio", 760, 1100, 260, z=0.6, keys=aparece(0.2))],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[cap(0.1, d - 0.05, "2017", "#141414", "#ffd23fe6", 130, y=560)], sfx=[(0.1, "pop", -20)])


@v.plano(97, "estudió el vidrio de la abadía de Westminster, del siglo trece: la fachada gótica")
def _(d):
    return P(TALLER, [BG("bg_cielo_naranja"), OB("abadia", 540, 1100, 900, keys=aparece(0.0))],
             cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[cap(0.2, d - 0.05, "WESTMINSTER", "#ffffff", "#c0392be6", 100, y=520), cap(min(1.6, d * 0.6), d - 0.05, "SIGLO XIII", "#141414", "#ffd23fe6", 100, y=1640)],
             sfx=[(0.2, "ding", -22)])


@v.plano(108, "a temperatura ambiente: el termómetro tranquilo junto al cristal")
def _(d):
    return P(LAB, [BG("bg_galeria"), OB("panel_vidrio", 420, 1050, 380), OB("termometro_amb" if False else "termo_calor", 820, 1100, 200, keys=aparece(0.1))],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[cap(0.2, d - 0.05, "AMBIENTE", "#141414", "#7df9ffe6", 110, y=560)], sfx=[(0.1, "tic", -22)])


@v.plano(111, "en mil millones de años: el cielo gira y el contador corre")
def _(d):
    return P(ESP, [BG("bg_via_lactea"), OB("panel_vidrio", 540, 1150, 300, z=0.5)], cam(1.0, 1.06, (540, 1000)), "corte",
             hud=[cap(0.0, d - 0.02, "MIL MILLONES DE AÑOS", "#141414", "#ffd23fe6", 84, y=600)], sfx=[(0.05, "subida", -20)])


@v.plano(116, "se movería como mucho un nanómetro: lupa sobre el borde del cristal, marca diminuta")
def _(d):
    return P(LAB, [BG("bg_galeria"), OB("corte_cristal", 540, 1100, 380), OB("lupa", 600, 1450, 420, z=0.6, keys=aparece(0.1) + [{"t": 0, "rot": -10}, {"t": d, "rot": 0}]),
                   flecha([[900, 1700], [640, 1560]], 0.4, 0.8, MAGENTA, 9, z=0.7)],
             cam(1.0, 1.06, (560, 1300)), "corte", hud=[cap(0.3, d - 0.05, "1 NANÓMETRO", "#ffffff", "#c0392be6", 100, y=600)], sfx=[(0.1, "tic", -20)])


@v.plano(127, "otros cálculos dicen: hoja de cálculos que se despliega")
def _(d):
    return P(LAB, [BG("bg_galeria"), OB("pergamino", 540, 1100, 640, keys=aparece(0.0) + [{"t": 0, "rot": -4}, {"t": d, "rot": 2}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[cap(0.05, d - 0.02, "OTROS CÁLCULOS", "#141414", "#7df9ffe6", 96, y=560)], sfx=[(0.2, "roce", -20)])


@v.plano(131, "que tardaría más que la edad del universo: la Vía Láctea y el cristal minúsculo")
def _(d):
    return P(ESP, [BG("bg_via_lactea"), estrellas(80, 9), OB("panel_vidrio", 540, 1250, 160, z=0.5, keys=[{"t": 0, "ancho": 300}, {"t": d, "ancho": 140, "ease": "suave"}])],
             cam(1.0, 1.08, (540, 1000)), "corte", hud=[amarillo(0.2, d - 0.05, "MÁS QUE EL UNIVERSO", y=600, tam=96, color=AMBAR)], sfx=[(0.1, "brillo", -18)])


@v.plano(138, "el vidrio es un sólido: el cristal golpea la mesa y no se deforma")
def _(d):
    return P(LAB, [BG("bg_galeria"), OB("panel_vidrio", 540, 1150, 440, keys=cae(0.05, 0.4, 500, 1150))],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[amarillo(0.4, d - 0.05, "SÓLIDO", y=560, tam=150, color=LIMA)], sfx=[(0.4, "golpe", -18)])


@v.plano(143, "solo que con los átomos desordenados: primero en fila (cristal), luego revueltos (vidrio)")
def _(d):
    t = min(1.0, d * 0.4)
    return P(LAB, [BG("bg_galeria"), OB("atomos_orden", 540, 1100, 760, keys=[{"t": 0, "op": 1}, {"t": t, "op": 1}, {"t": t + 0.2, "op": 0}]),
                   OB("atomos_desorden", 540, 1100, 760, keys=[{"t": 0, "op": 0}, {"t": t, "op": 0}, {"t": t + 0.2, "op": 1}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[cap(t, d - 0.05, "DESORDENADOS", "#141414", "#7df9ffe6", 100, y=560)], sfx=[(t, "zap", -20)])


@v.plano(149, "como un líquido congelado al instante: destello helado sobre los átomos")
def _(d):
    return P(LAB, [BG("bg_galeria"), OB("atomos_desorden", 540, 1100, 760, keys=late(0.3, 1, 0.05, 0.3)),
                   brillo(540, 1100, 480, CIAN, 0.6, 0.6, keys=[{"t": 0, "op": 0}, {"t": 0.3, "op": 0}, {"t": 0.4, "op": 0.8}, {"t": 0.9, "op": 0.2}]),
                   OB("copo_nieve", 860, 1550, 220, z=0.7, keys=aparece(0.35))],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[cap(0.4, d - 0.05, "CONGELADO", "#ffffff", "#2a5ae8e6", 100, y=560)], sfx=[(0.35, "impacto", -20)])


@v.plano(155, "¿tú también lo creías? (bucle): la vidriera que gotea, como al principio")
def _(d):
    return P(CAT, [BG("bg_catedral"), vid(540, 1060, 700, True, keys=[{"t": 0, "y": 1030}, {"t": d, "y": 1060}])] + gotas(540, 1620, d, 2),
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[cap(0.2, d - 0.05, "¿LO CREÍAS?", "#141414", "#ffd23fe6", 100, y=560)], sfx=[(0.05, "ding", -20)])


def micro(fondo, els, txt=None, col="#ffffff", cap_f="#c0392be6", sfx="pop"):
    def fn(d):
        return P(fondo, els(d), cam(1.15, 1.3, (540, 1000)), "corte", hud=[cap(0.0, d - 0.02, txt, col, cap_f, 120)] if txt else [], sfx=[(0.01, sfx, -18)])
    return fn




v.plano(4, "micro: gota de vidrio que cae", mas=0.6)(micro(CAT, lambda d: [BG("bg_catedral"), OB("gota", 540, 1000, 380, keys=[{"t": 0, "y": 850}, {"t": d, "y": 1100}])], sfx="agua"))
v.plano(25, "micro: la rosa de colores", mas=0.15)(micro(CAT, lambda d: [BG("bg_catedral"), OB("abadia", 540, 1500, 2300)], sfx="brillo"))
v.plano(47, "micro: el horno al rojo", mas=0.5)(micro(TALLER, lambda d: [BG("bg_taller_vidrio"), brillo(540, 1000, 500, "#ff8a20", 0.7, 0.5)], sfx="rumor"))
v.plano(75, "micro: el centro grueso del disco", mas=0.2)(micro(TALLER, lambda d: [BG("bg_taller_vidrio"), OB("disco_vidrio", 540, 1000, 1800, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 30}])], sfx="tic"))
v.plano(90, "micro: las gotas de colores", mas=0.4)(micro(CAT, lambda d: [BG("bg_catedral"), OB("vidriera_gotea", 540, 300, 1400)], sfx="agua"))
v.plano(137, "micro: galaxia", mas=0.5)(micro(ESP, lambda d: [BG("bg_via_lactea"), estrellas(120, 11)], sfx="brillo"))


v.construir("2026-11-28-manana-03-vidrio-no-se-escurre", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 1283, "db": -13},
            claves=["vidrio", "escurre", "líquido", "lento", "catedrales", "gruesas", "abajo", "falso", "mano", "bola", "cilindro", "aplanaba",
                    "cristalero", "gruesa", "fluyera", "Westminster", "trece", "millones", "nanómetro", "universo", "sólido", "átomos", "congelado"],
            ep_extra={"sfx_bajo_voz": True})
