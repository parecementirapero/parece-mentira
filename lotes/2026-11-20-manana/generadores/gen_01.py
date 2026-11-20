"""01 · Los hipopótamos no nadan — método denso. Lote 2026-11-20-manana (Agente 08:00, Nico). Tendencia del día: «fiona hipopótamo».
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]
Versión corta: se quita «Unas tres décimas de segundo.» (palabras 140–144) para no pasar de 60 s."""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_1120m  # noqa: E402

SVG = ilus_1120m.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG, omitir=[(140, 145)])

AGUA = ["#1f5a52", "#081c1a"]
SAB = ["#c0604a", "#4a3418"]
DIA = ["#5aa0d8", "#4a3418"]
OSC = ["#0a1a2a", "#020610"]


def rio(): return BG("bg_rio_fondo")
def burbujas(n=26, sem=1, area=(80, 300, 1000, 1500)): return polvo("#e8fff6", n, area, sem)


def hipo(n="hipo", ancho=900, x=540, y=1300, z=0.5, keys=None, **k):
    """Lienzo 1100×620 → con ancho 900 mide ≈507 de alto; patas abajo en y+≈230."""
    return IMG(n, ancho=ancho, x=x, y=y, z=z, keys=keys or [], **k)


def tacha(x, y, t0, t1, r=120):
    return [flecha([[x - r, y - r], [x + r, y + r]], t0, t0 + 0.2, "#ff3d3d", 16, punta=False, z=0.8),
            flecha([[x + r, y - r], [x - r, y + r]], t0 + 0.12, t0 + 0.32, "#ff3d3d", 16, punta=False, z=0.8)]


# ================================================================== PLANOS
@v.plano(0, "gancho: el hipopótamo entra desde arriba y se hunde en el río, con burbujas")
def _(d):
    return P(AGUA, [rio(), hipo(ancho=1040, keys=arranque(540, 1250, d, "arriba", 520, 60)), burbujas(40, 1), brillo(540, 600, 500, "#bff8e8", 0.3, 0.07)],
             cam(1.0, 1.08, (540, 1150)), vineta=0.6, sfx=[(0.02, "agua", -14, {"dur": 1.2}), (0.5, "burbuja", -18)])


@v.plano(4, "ni siquiera flotan: sigue bajando despacio, flecha hacia abajo")
def _(d):
    return P(AGUA, [rio(), hipo(keys=[{"t": 0, "y": 1150}, {"t": d, "y": 1320, "ease": "suave"}]), burbujas(30, 2),
                    flecha([[920, 700], [920, 1150]], 0.1, d * 0.7, LIMA, 10, z=0.6)],
             cam(1.05, 1.1, (540, 1150)), "corte", hud=[amarillo(0.1, d - 0.03, "NI FLOTAN", y=560, tam=110, color=LIMA)], sfx=[(0.1, "burbuja", -20)])


@v.plano(7, "pasan casi todo el día en el agua: cabeza asomando en el río de la sabana, el sol cruza")
def _(d):
    return P(DIA, [BG("bg_sabana_dia"), IMG("hipo_cabeza", ancho=1300, x=540, y=1500, z=0.5, keys=[{"t": 0, "y": 1560}, {"t": d * 0.4, "y": 1500, "ease": "salida"}, {"t": d, "x": 580}]),
                   brillo(820, 380, 220, "#fff4c0", 0.4, 0.06, keys=[{"t": 0, "x": 760}, {"t": d, "x": 880}])],
             cam(1.0, 1.06, (540, 1200)), "desenfoque", sfx=[(0.1, "ola", -22)])


@v.plano(15, "pero su cuerpo es tan denso: una pesa enorme cae al agua")
def _(d):
    return P(AGUA, [rio(), IMG("pesa_tonelada", ancho=520, x=540, z=0.5, keys=cae(0.0, 0.55, 500, 1250)), burbujas(30, 3)],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[amarillo(0.2, d - 0.03, "DENSO", y=560, tam=130, color=AMBAR)], sfx=[(0.35, "golpe", -14)])


@v.plano(20, "micro: «denso», primer plano del cuerpo hundiéndose con burbujas")
def _(d):
    return P(AGUA, [rio(), hipo(ancho=1700, x=600, keys=[{"t": 0, "y": 1050}, {"t": d, "y": 1180, "ease": "entrada"}]), burbujas(40, 21, (100, 400, 1000, 1000))],
             cam(1.0, 1.12, (540, 1100)), "corte", sfx=[(0.02, "burbuja", -18)])


@v.plano(21, "que se hunde: el hipopótamo toca el fondo y levanta arena")
def _(d):
    return P(AGUA, [rio(), hipo(keys=cae(0.0, 0.6, 1000, 1330)), polvo("#c8b490", 40, (200, 1450, 900, 1650), 4), burbujas(20, 5)],
             cam(1.1, 1.15, (540, 1300)), "corte", sfx=[(0.4, "golpe", -12)])


@v.plano(24, "¿y cómo se mueven? la lupa recorre al hipopótamo en el fondo")
def _(d):
    return P(AGUA, [rio(), hipo(y=1330), IMG("lupa", ancho=360, z=0.7, keys=[{"t": 0, "x": 300, "y": 1150}, {"t": d, "x": 780, "y": 1450, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1250)), "corte", hud=[amarillo(0.05, d - 0.03, "¿CÓMO?", y=560, tam=120, color=CIAN)], sfx=[(0.1, "roce", -20)])


@v.plano(28, "por el fondo: camina por el lecho del río, de izquierda a derecha")
def _(d):
    return P(AGUA, [rio(), hipo(keys=[{"t": 0, "x": 330, "y": 1330}, {"t": d, "x": 700, "y": 1320, "ease": "lineal"}]), polvo("#c8b490", 30, (100, 1500, 1000, 1650), 6), burbujas(18, 7)],
             cam(1.35, 1.4, (440, 1450), (620, 1450)), "corte", hud=[rotulo(0.1, d - 0.05, "POR EL FONDO", tam=96, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.2, "golpe", -24)])


@v.plano(31, "se impulsan con las patas: primer plano de las patas empujando la arena")
def _(d):
    return P(AGUA, [rio(), hipo(ancho=1500, x=560, y=1050, keys=[{"t": 0, "x": 600}, {"t": d, "x": 480, "ease": "suave"}]), polvo("#d8c4a0", 60, (100, 1450, 1000, 1700), 8),
                    flecha([[700, 1600], [880, 1520]], 0.1, 0.6, CIAN, 8, z=0.7)],
             cam(1.0, 1.08, (540, 1400)), "corte", sfx=[(0.15, "golpe", -20), (0.6, "golpe", -22)])


@v.plano(37, "y dan saltitos a cámara lenta: el hipopótamo bota despacio")
def _(d):
    t = d / 3
    return P(AGUA, [rio(), IMG("hipo_salto", ancho=900, x=540, z=0.5, keys=[{"t": 0, "y": 1330, "x": 380}, {"t": t, "y": 1120, "ease": "salida"}, {"t": 2 * t, "y": 1330, "ease": "entrada"},
                                                                                  {"t": d, "y": 1180, "x": 700, "ease": "salida"}]), burbujas(24, 9),
                    polvo("#d8c4a0", 30, (200, 1500, 900, 1650), 10)],
             cam(1.0, 1.05, (540, 1250)), "corte", hud=[amarillo(0.1, d - 0.03, "A CÁMARA LENTA", y=560, tam=96, color=LIMA)], sfx=[(2 * t, "golpe", -20)])


@v.plano(42, "micro: «como», el hipopótamo bota y se funde con la Luna")
def _(d):
    return P(ESPACIO, [estrellas(60, 5), luna(540, 1300, 1200, z=0.2), IMG("hipo_salto", ancho=700, x=540, z=0.5, keys=[{"t": 0, "y": 1000}, {"t": d, "y": 900, "ease": "salida"}])],
             cam(1.0, 1.06, (540, 1000)), "corte", sfx=[(0.02, "roce", -20)])


@v.plano(44, "como un astronauta en la Luna: el astronauta bota sobre la superficie gris")
def _(d):
    return P(ESPACIO, [BG("bg_superficie"), IMG("astronauta", ancho=420, x=540, z=0.5, keys=[{"t": 0, "y": 1350, "x": 420}, {"t": d * 0.5, "y": 1120, "ease": "salida"}, {"t": d, "y": 1350, "x": 660, "ease": "entrada"}]),
                       tierra(860, 420, 220, 0.2)],
             cam(1.0, 1.06, (540, 1200)), "corte", sfx=[(d * 0.95, "golpe", -22)])


@v.plano(47, "micro: «Luna», la Luna gira enorme")
def _(d):
    return P(ESPACIO, [estrellas(60, 4), luna(540, 1000, 820, keys=[{"t": 0, "rot": -4, "escala": 0.9}, {"t": d, "rot": 4, "escala": 1.0, "ease": "salida"}])],
             cam(1.0, 1.1, (540, 1000)), "corte", sfx=[(0.02, "brillo", -20)])


@v.plano(48, "aguantan la respiración: la cabeza se mete bajo el agua y salen burbujas")
def _(d):
    return P(DIA, [BG("bg_sabana_dia"), IMG("hipo_cabeza", ancho=1300, x=540, z=0.5, keys=[{"t": 0, "y": 1500}, {"t": d * 0.7, "y": 1720, "ease": "entrada"}]),
                   polvo("#e8fff6", 30, (300, 1380, 800, 1500), 11)],
             cam(1.0, 1.08, (540, 1350)), "corte", sfx=[(0.3, "agua", -18, {"dur": 0.8})])


@v.plano(51, "unos cinco minutos: el cronómetro corre bajo el agua")
def _(d):
    return P(AGUA, [rio(), *cronometro(0, 300, 0.05, d), burbujas(16, 12)],
             cam(1.0, 1.04, (540, 1040)), "corte", hud=[contador(0.05, d - 0.03, 0, 5, d * 0.6, " MIN", y=1530, tam=120, color="#ffd23f")],
             sfx=[(0.05, "tictac", -22, {"dur": min(1.2, d), "ritmo": 0.12})])


@v.plano(56, "cierran: la cabeza entera, todo abierto")
def _(d):
    return P(DIA, [BG("bg_sabana_dia"), IMG("hipo_cabeza", ancho=1300, x=540, y=1440, z=0.5, keys=late(0.05, 1, 0.04))],
             cam(1.1, 1.15, (540, 1300)), "corte", sfx=[(0.05, "pop", -20)])


@v.plano(58, "las orejas: primer plano, las orejas se pliegan")
def _(d):
    t = min(0.35, d * 0.5)
    return P(DIA, [BG("bg_sabana_dia"), IMG("hipo_cabeza", ancho=1300, x=540, y=1440, z=0.5, keys=[{"t": 0, "op": 1}, {"t": t, "op": 0}]),
                   IMG("hipo_cabeza_cerrada", ancho=1300, x=540, y=1440, z=0.51, keys=[{"t": 0, "op": 0}, {"t": t, "op": 1}]), senala(312, 1282, t, d - 0.05, 70, MAGENTA)],
             cam(1.9, 2.0, (380, 1300)), "corte", sfx=[(t, "pop", -18)])


@v.plano(61, "y la nariz: primer plano, las fosas se cierran")
def _(d):
    t = min(0.35, d * 0.5)
    return P(DIA, [BG("bg_sabana_dia"), IMG("hipo_cabeza", ancho=1300, x=540, y=1440, z=0.5, keys=[{"t": 0, "op": 1}, {"t": t, "op": 0}]),
                   IMG("hipo_cabeza_cerrada", ancho=1300, x=540, y=1440, z=0.51, keys=[{"t": 0, "op": 0}, {"t": t, "op": 1}]), senala(950, 1375, t, d - 0.05, 90, CIAN)],
             cam(1.9, 2.0, (880, 1340)), "corte", sfx=[(t, "pop", -18)])


@v.plano(62, "y duermen en el agua: el hipopótamo dormido flota quieto en la penumbra")
def _(d):
    return P(OSC, [rio(), {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#020a14", "op": 0.5, "x": 540, "y": 960, "z": 0.1},
                   hipo("hipo_dormido", keys=[{"t": 0, "y": 1330, "rot": -1}, {"t": d, "y": 1310, "rot": 1, "ease": "suave"}]), burbujas(10, 13)],
             cam(1.0, 1.06, (540, 1250)), "desenfoque", hud=[rotulo(0.2, d - 0.05, "Z z z", tam=110, color="#ffffff", capsula=None, y=900, x=820)], sfx=[(0.1, "burbuja", -24)])


@v.plano(67, "un reflejo los hace subir a respirar: sube dormido hasta la superficie, flecha hacia arriba")
def _(d):
    return P(OSC, [rio(), hipo("hipo_dormido", keys=[{"t": 0, "y": 1330}, {"t": d * 0.45, "y": 520, "ease": "suave"}, {"t": d, "y": 1250, "ease": "suave"}]),
                   flecha([[930, 1500], [930, 500]], 0.05, d * 0.4, CIAN, 10, z=0.6), burbujas(30, 14)],
             cam(1.0, 1.04, (540, 1000)), "corte", hud=[amarillo(0.1, d * 0.5, "REFLEJO", y=560, tam=120, color=CIAN), rotulo(d * 0.55, d - 0.05, "SIN DESPERTAR", tam=92, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "subida", -20, {"dur": 0.9})])


@v.plano(76, "¿y ese líquido rojo de su piel? primer plano de la piel con gotas rojas")
def _(d):
    return P(["#5a4252", "#3a2a34"], [BG("piel_gotas"), brillo(540, 1000, 600, "#ffb070", 0.3, 0.07)],
             cam(1.0, 1.25, (540, 1000), (500, 1100)), "corte", hud=[rotulo(0.2, d - 0.05, "¿ROJO?", tam=120, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(0.1, "roce", -20)])


@v.plano(83, "micro: «no es», un NO enorme")
def _(d):
    return P(["#2a0a10", "#120406"], [brillo(540, 1000, 500, "#ff3d3d", 0.3, 0.06)], cam(1.0, 1.08, (540, 1000)), "corte",
             hud=[rotulo(0.0, d + 0.06, "NO", tam=300, color="#ffffff", capsula="#c0392be6", y=1000)], sfx=[(0.0, "golpe", -16)])


@v.plano(85, "no es sangre: gota de sangre que se tacha")
def _(d):
    return P(["#2a0a10", "#120406"], [brillo(540, 1100, 500, "#ff3d3d", 0.25, 0.06), IMG("gota_sangre", ancho=380, x=540, z=0.5, keys=cae(0.0, 0.4, 700, 1100)),
                                      *tacha(540, 1100, 0.45, d)],
             cam(1.0, 1.05, (540, 1100)), "corte", sfx=[(0.3, "golpe", -18), (0.5, "zap", -20)])


@v.plano(86, "ni siquiera es sudor: gota de sudor que también se tacha")
def _(d):
    return P(["#0a2030", "#04101a"], [brillo(540, 1100, 500, "#7ac8f0", 0.25, 0.06), IMG("gota_sudor", ancho=380, x=540, z=0.5, keys=cae(0.0, 0.4, 700, 1100)),
                                      *tacha(540, 1100, 0.45, d)],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[rotulo(0.1, d - 0.05, "SUDOR", tam=110, color="#141414", capsula="#7ac8f0e6", y=560)], sfx=[(0.3, "golpe", -18), (0.5, "zap", -20)])


@v.plano(90, "es su propio protector solar: el tubo de crema y un sol detrás, la gota roja delante")
def _(d):
    return P(SAB, [BG("bg_sabana"), *sol(760, 700, 130, 0.3), IMG("crema_solar", ancho=330, x=380, y=1250, z=0.5, keys=aparece(0.05)),
                   IMG("gota_roja", ancho=250, x=760, y=1300, z=0.55, keys=aparece(0.3) + [{"t": d, "y": 1270}])],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[rotulo(0.2, d - 0.05, "PROTECTOR SOLAR", tam=90, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.1, "brillo", -18)])


@v.plano(95, "y además: la gota roja late sola")
def _(d):
    return P(["#0a2a1a", "#02100a"], [brillo(540, 1100, 600, "#ff7a5a", 0.25, 0.06), IMG("gota_roja", ancho=420, x=540, y=1100, z=0.6, keys=aparece(0.0) + late(0.4, 1))],
             cam(1.0, 1.06, (540, 1100)), "corte", sfx=[(0.05, "pop", -20)])


@v.plano(97, "frena algunas bacterias: las bacterias se encogen al tocar la gota")
def _(d):
    return P(["#0a2a1a", "#02100a"], [brillo(540, 1100, 600, "#7dff3a", 0.2, 0.06), IMG("gota_roja", ancho=300, x=540, y=1100, z=0.6, keys=late(0.1, 2)),
                                      IMG("bacteria", ancho=330, x=260, y=820, z=0.5, keys=[{"t": 0, "escala": 1.0, "rot": -20}, {"t": d * 0.8, "escala": 0.25, "op": 0.2, "x": 380, "ease": "suave"}]),
                                      IMG("bacteria2", ancho=330, x=830, y=1400, z=0.5, keys=[{"t": 0, "escala": 1.0, "rot": 30}, {"t": d * 0.8, "escala": 0.25, "op": 0.2, "x": 700, "ease": "suave"}]),
                                      IMG("bacteria", ancho=260, x=820, y=780, z=0.5, keys=[{"t": 0, "escala": 1.0, "rot": 60}, {"t": d * 0.8, "escala": 0.3, "op": 0.2, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[amarillo(0.1, d - 0.03, "BACTERIAS", y=560, tam=110, color=LIMA)], sfx=[(0.2, "zap", -20), (d * 0.6, "zap", -22)])


@v.plano(100, "fuera del agua tampoco son lentos: corre por la orilla con líneas de velocidad")
def _(d):
    return P(SAB, [BG("bg_sabana_tierra"), hipo(ancho=700, y=1620, keys=[{"t": 0, "x": 120}, {"t": d, "x": 900, "ease": "lineal"}]), *lineas_vel(300, 1620, 3, "#ffe0b0cc"),
                   polvo("#e8c890", 40, (0, 1650, 1080, 1800), 16)],
             cam(1.0, 1.04, (540, 1350)), "corte", sfx=[(0.1, "whoosh", -18, {"dur": 0.5}), (0.3, "golpe", -24)])


@v.plano(106, "aunque pesen más de una tonelada: la pesa cae junto al hipopótamo")
def _(d):
    return P(SAB, [BG("bg_sabana_tierra"), hipo(ancho=640, x=360, y=1640), IMG("pesa_tonelada", ancho=340, x=860, z=0.55, keys=cae(0.0, 0.5, 700, 1680))],
             cam(1.3, 1.35, (700, 1550)), "corte", hud=[rotulo(0.3, d - 0.05, "+1 TONELADA", tam=104, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.35, "golpe", -12)])


@v.plano(112, "en dos mil veinticuatro: el año corre")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("calendario", ancho=600, x=540, y=1150, z=0.5, keys=aparece(0.0))],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[contador(0.05, d - 0.03, 2000, 2024, d * 0.5, "", y=560, tam=150, color="#ffd23f", miles=False)],
             sfx=[(0.05, "tictac", -24, {"dur": 0.6, "ritmo": 0.06})])


@v.plano(116, "unos científicos analizaron vídeos: el monitor con fotogramas")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("pantalla_video", ancho=950, x=540, y=1150, z=0.5, keys=arranque(540, 1150, d, "abajo", 160, 20)), brillo(540, 1000, 500, "#2ff3ff", 0.25, 0.06)],
             cam(1.0, 1.7, (540, 1150), (520, 1000)), "corte", sfx=[(0.1, "senal", -22)])


@v.plano(124, "y descubrieron algo increíble: destello sobre la pantalla")
def _(d):
    return P(OSC, [BG("bg_estudio"), IMG("pantalla_video", ancho=950, x=540, y=1150, z=0.5, keys=late(d * 0.5, 1, 0.08)),
                   brillo(540, 1000, 700, "#ff3df2", 0.5, 0.6, keys=[{"t": 0, "op": 0}, {"t": d * 0.8, "op": 1}])],
             cam(1.0, 1.12, (540, 1100)), "corte", sfx=[(0.05, "subida", -16, {"dur": max(0.6, d)})])


@v.plano(127, "vuelan: el hipopótamo despega del suelo, golpe de revelación")
def _(d):
    return P(SAB, [BG("bg_sabana_tierra"), IMG("hipo_salto", ancho=880, x=540, z=0.5, keys=[{"t": 0, "y": 1560}, {"t": 0.35, "y": 1380, "ease": "salida"}, {"t": d, "y": 1350}]),
                   {"tipo": "forma", "forma": "elipse", "ancho": 520, "alto": 40, "relleno": "#000000", "op": 0.35, "x": 560, "y": 1830, "z": 0.45},
                   fundido_blanco([{"t": 0, "op": 0.8}, {"t": 0.25, "op": 0}])],
             cam(1.0, 1.08, (540, 1450)), "corte", hud=[rotulo(0.12, d - 0.05, "¡VUELAN!", tam=150, color="#ffffff", capsula="#c0397ae6", y=560)], sfx=[(0.02, "impacto", -12)])


@v.plano(128, "durante un instante: suspendido en el aire, todo se ralentiza")
def _(d):
    return P(SAB, [BG("bg_sabana_tierra"), IMG("hipo_salto", ancho=880, x=540, z=0.5, keys=[{"t": 0, "y": 1380}, {"t": d, "y": 1360, "x": 580, "ease": "suave"}]),
                   {"tipo": "forma", "forma": "elipse", "ancho": 520, "alto": 40, "relleno": "#000000", "op": 0.35, "x": 560, "y": 1830, "z": 0.45}],
             cam(1.5, 1.55, (560, 1650)), "corte", sfx=[(0.1, "brillo", -22)])


@v.plano(132, "micro: «cuatro», un 4 enorme")
def _(d):
    return P(OSC, [BG("bg_estudio"), brillo(540, 1000, 500, "#b8ff3a", 0.4, 0.06)],
             cam(1.0, 1.1, (540, 1000)), "corte", hud=[rotulo(0.0, d - 0.02, "4", tam=380, color="#141414", capsula="#b8ff3ae6", y=1000)], sfx=[(0.0, "golpe", -16)])


@v.plano(134, "sus cuatro patas despegan a la vez: anillos en las patas y el hueco con el suelo")
def _(d):
    return P(SAB, [BG("bg_sabana_tierra"), IMG("hipo_salto", ancho=880, x=540, y=1360, z=0.5),
                   {"tipo": "forma", "forma": "elipse", "ancho": 520, "alto": 40, "relleno": "#000000", "op": 0.35, "x": 560, "y": 1830, "z": 0.45},
                   senala(300, 1560, 0.05, d - 0.1, 70, LIMA), senala(410, 1580, 0.15, d - 0.1, 70, LIMA), senala(700, 1550, 0.25, d - 0.1, 70, LIMA), senala(800, 1540, 0.35, d - 0.1, 70, LIMA),
                   flecha([[980, 1820], [980, 1640]], 0.4, 0.9, CIAN, 8, z=0.6)],
             cam(1.0, 1.06, (540, 1500)), "corte", hud=[rotulo(0.3, d - 0.05, "4 PATAS EN EL AIRE", tam=88, color="#141414", capsula="#b8ff3ae6", y=560)],
             sfx=[(0.05, "pop", -20), (0.25, "pop", -20)])


@v.plano(145, "no saben nadar: vuelve al fondo del río (bucle con el principio)")
def _(d):
    return P(AGUA, [rio(), hipo(keys=[{"t": 0, "y": 1200}, {"t": d, "y": 1320, "ease": "suave"}]), burbujas(30, 17)],
             cam(1.0, 1.05, (540, 1200)), "corte", sfx=[(0.05, "agua", -18, {"dur": 0.8})])


@v.plano(148, "pero sí volar un poquito: salta sobre la sabana y se queda en el aire")
def _(d):
    return P(SAB, [BG("bg_sabana_tierra"), IMG("hipo_salto", ancho=880, x=540, z=0.5, keys=[{"t": 0, "y": 1560}, {"t": 0.4, "y": 1360, "ease": "salida"}, {"t": d, "y": 1300, "x": 600}]),
                   {"tipo": "forma", "forma": "elipse", "ancho": 520, "alto": 40, "relleno": "#000000", "op": 0.35, "x": 560, "y": 1830, "z": 0.45}],
             cam(1.0, 1.08, (540, 1400)), "corte", hud=[rotulo(0.3, d - 0.4, "UN POQUITO", tam=120, color="#ffffff", capsula="#c0397ae6", y=560)], sfx=[(0.1, "whoosh", -18), (d * 0.6, "ding", -22)])


v.construir("2026-11-20-manana-01-hipopotamos-no-nadan", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 61, "db": -13},
            claves=["hipopótamos", "nadan", "flotan", "agua", "denso", "hunde", "fondo", "patas", "saltitos", "astronauta", "Luna", "cinco", "minutos",
                    "orejas", "nariz", "duermen", "reflejo", "rojo", "sangre", "sudor", "protector", "solar", "bacterias", "tonelada", "vuelan", "cuatro", "volar"])
