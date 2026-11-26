"""02 · Medalla olímpica por pintar (concursos de arte de los Juegos, 1912–1948) — método denso, estilo del vídeo largo.
Lote 2026-11-25-tarde (Jorge, con el agente). Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comun_1125t as C  # noqa: E402
from comun_1125t import *  # noqa: E402,F401,F403
import ilus_1125t  # noqa: E402

SVG = ilus_1125t.generar(os.path.join(sys.argv[1], "_svg_lote"))
C.SVG_DIR = SVG
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
GAL = ["#3a1418", "#2a0e12"]
EST = ["#0a1020", "#102a14"]
S_G, S_E = SUELO["bg_galeria"], SUELO["bg_estadio_noche"]


def medalla_cae(n, x, t0, ancho=300, y=1000):
    return OB(n, x, y, ancho, z=0.6, keys=[{"t": 0, "y": -400, "rot": -20}, {"t": t0, "y": -400, "rot": -20}, {"t": t0 + 0.4, "y": y, "rot": 4, "ease": "bote"},
                                          {"t": t0 + 0.9, "rot": -3, "ease": "elastico"}])


ICONOS = [("caballete", 260), ("escultura_caballo", 330), ("planos", 300), ("pergamino", 240), ("nota_musical_b", 220)]


def iconos(t0, y=1050, esc=1.0):
    pos = [(250, y - 260), (800, y - 260), (540, y), (250, y + 270), (800, y + 270)]
    return [OB(n, x, yy, a * esc, keys=aparece(t0 + i * 0.12)) for i, ((n, a), (x, yy)) in enumerate(zip(ICONOS, pos))]


@v.plano(0, "gancho: la medalla de oro entra balanceándose delante del cuadro")
def _(d):
    return P(GAL, [BG("bg_galeria"), OB("caballete", 540, 1150, 560, z=0.45, keys=[{"t": 0, "op": 0.0}, {"t": 0.6, "op": 1}]),
                   OB("medalla_oro", 540, 760, 420, z=0.6, keys=[{"t": 0, "y": 560, "rot": 25}, {"t": 0.35, "y": 760, "rot": -14, "ease": "salida"},
                                                                {"t": 0.8, "rot": 9, "ease": "suave"}, {"t": 1.25, "rot": -5, "ease": "suave"}, {"t": d, "rot": 0, "ease": "suave"}])],
             cam(1.0, 1.08, (540, 1000)), vineta=0.4, sfx=[(0.05, "whoosh", -20), (0.35, "ding", -18)])


@v.plano(4, "y no es broma: el cuadro del corredor en la galería")
def _(d):
    return P(GAL, [BG("bg_galeria"), OB("caballete", 540, 1050, 760, keys=aparece(0.0))], cam(1.0, 1.06, (540, 1000)), "corte",
             hud=[cap(0.15, d - 0.05, "NO ES BROMA", "#ffffff", "#c0392be6", 110)], sfx=[(0.05, "pop", -20)])


@v.plano(8, "entre mil novecientos doce…: el estadio iluminado y el año")
def _(d):
    return P(EST, [BG("bg_estadio_noche")], cam(1.0, 1.08, (540, 1000)), "desenfoque",
             hud=[contador(0.05, d - 0.05, 1890, 1912, 0.6, miles=False, tam=180, color="#141414", capsula="#ffffffe6", y=900)], sfx=[(0.1, "tic", -18)])


@v.plano(12, "…y mil novecientos cuarenta y ocho: el año corre hasta 1948")
def _(d):
    return P(EST, [BG("bg_estadio_noche"), polvo("#ffe8c0", 30, (0, 300, 1080, 1100), 3)], cam(1.08, 1.14, (540, 1000)), "corte",
             hud=[contador(0.05, d - 0.05, 1912, 1948, 0.9, miles=False, tam=180, color="#141414", capsula="#ffd23fe6", y=900)], sfx=[(0.1, "subida", -22, {"dur": 0.9})])


@v.plano(18, "los Juegos daban medallas de oro, plata y bronce: caen en el podio")
def _(d):
    return P(EST, [BG("bg_estadio_noche"), OB("podio", 540, 1250, 820, z=0.5),
                   medalla_cae("medalla_oro", 540, 0.3, 240, 930), medalla_cae("medalla_plata", 300, 0.6, 220, 1030), medalla_cae("medalla_bronce", 780, 0.9, 220, 1060)],
             cam(1.0, 1.05, (540, 1100)), "corte", sfx=[(0.7, "ding", -18), (1.0, "ding", -20), (1.3, "ding", -22)])


@v.plano(28, "al arte: el cuadro se ilumina")
def _(d):
    return P(GAL, [BG("bg_galeria"), OB("caballete", 540, 1050, 720, keys=late(0.1, 1, 0.05)), brillo(540, 900, 380, "#ffd8a0", 0.5, 0.44, pulso=[0.15, 0.5])],
             cam(1.05, 1.12, (540, 950)), "corte", hud=[amarillo(0.0, d - 0.02, "¡AL ARTE!", y=560, tam=130, color=AMBAR)], sfx=[(0.05, "impacto", -16)])


@v.plano(30, "había cinco concursos: aparecen los cinco")
def _(d):
    return P(GAL, [BG("bg_galeria"), *iconos(0.1)], cam(1.0, 1.04, (540, 1050)), "corte",
             hud=[cap(0.1, d - 0.05, "5 CONCURSOS", tam=110)], sfx=[(0.1 + i * 0.12, "pop", -22) for i in range(5)])


@v.plano(33, "pintura")
def _(d):
    return P(GAL, [BG("bg_galeria"), OB("caballete", 540, 1050, 760, keys=[{"t": 0, "escala": 1.1}, {"t": d, "escala": 1.0, "ease": "salida"}])],
             cam(1.1, 1.15, (540, 1000)), "corte", hud=[cap(0.02, d - 0.02, "PINTURA", tam=110)], sfx=[(0.02, "pop", -20)])


@v.plano(34, "escultura")
def _(d):
    return P(GAL, [BG("bg_galeria"), OB("escultura_caballo", 540, 1150, 900, keys=[{"t": 0, "escala": 1.1}, {"t": d, "escala": 1.0, "ease": "salida"}])],
             cam(1.1, 1.15, (540, 1050)), "corte", hud=[cap(0.02, d - 0.02, "ESCULTURA", tam=110)], sfx=[(0.02, "pop", -20)])


@v.plano(35, "arquitectura")
def _(d):
    return P(["#0a1a3a", "#06102a"], [OB("planos", 540, 1000, 920, keys=[{"t": 0, "escala": 1.1, "rot": -4}, {"t": d, "escala": 1.0, "rot": 0, "ease": "salida"}])],
             cam(1.05, 1.1, (540, 1000)), "corte", hud=[cap(0.02, d - 0.02, "ARQUITECTURA", "#141414", "#7df9ffe6", 100)], sfx=[(0.02, "pop", -20)])


@v.plano(36, "literatura")
def _(d):
    return P(GAL, [BG("bg_galeria"), OB("pergamino", 540, 1050, 640, keys=[{"t": 0, "escala": 1.1}, {"t": d, "escala": 1.0, "ease": "salida"}])],
             cam(1.05, 1.1, (540, 1000)), "corte", hud=[cap(0.0, d - 0.02, "LETRAS", tam=120)], sfx=[(0.02, "pop", -20)])


@v.plano(38, "y música: notas que suben")
def _(d):
    return P(GAL, [BG("bg_galeria"), OB("nota_musical_b", 420, 1100, 300, keys=[{"t": 0, "y": 1250}, {"t": d, "y": 950, "ease": "suave"}]),
                   OB("nota_musical_a", 680, 1000, 220, keys=[{"t": 0, "y": 1150}, {"t": d, "y": 820, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[cap(0.02, d - 0.02, "MÚSICA", tam=110)], sfx=[(0.02, "ding", -20)])


@v.plano(39, "solo había una regla: la obra tenía que estar inspirada en el deporte: zoom al corredor del cuadro")
def _(d):
    return P(GAL, [BG("bg_galeria"), OB("caballete", 540, 1050, 760), senala(520, 820, d * 0.5, d - 0.05, 140, AMBAR)],
             cam(1.0, 1.6, (540, 1000), (520, 820)), "corte", hud=[cap(0.3, d - 0.05, "UNA REGLA: EL DEPORTE", tam=76)], sfx=[(d * 0.5, "ding", -20)])


@v.plano(52, "fue idea del barón Pierre de Coubertin: el barón en la galería")
def _(d):
    return P(GAL, [BG("bg_galeria"), PZ("baron", 540, S_G, 1050, keys=[{"t": 0, "x": 600}, {"t": d, "x": 520, "ease": "suave"}]),
                   OB("caballete", 880, 1150, 360, z=0.45)],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[cap(0.4, d - 0.05, "PIERRE DE COUBERTIN", "#ffffff", "#2a5ae8e6", 80)], sfx=[(0.1, "roce", -22)])


@v.plano(59, "el hombre que recuperó los Juegos: el barón ante el estadio")
def _(d):
    return P(EST, [BG("bg_estadio_noche"), PZ("baron", 540, S_E, 1000), polvo("#ffe8c0", 30, (0, 300, 1080, 1100), 4)],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[cap(0.3, d - 0.05, "RECUPERÓ LOS JUEGOS", tam=80)], sfx=[(0.1, "whoosh", -22)])


@v.plano(65, "y en mil novecientos doce, el oro de literatura se lo llevó un poema: medalla sobre el poema")
def _(d):
    return P(GAL, [BG("bg_galeria"), OB("pergamino", 540, 1100, 660), medalla_cae("medalla_oro", 760, 0.9, 260, 820)],
             cam(1.0, 1.06, (540, 1050)), "corte",
             hud=[contador(0.05, 1.3, 1900, 1912, 0.5, miles=False, tam=150, color="#141414", capsula="#ffffffe6", y=600)], sfx=[(0.1, "tic", -18), (1.3, "ding", -18)])


@v.plano(79, "«Oda al deporte»: el título del poema brilla")
def _(d):
    return P(GAL, [BG("bg_galeria"), OB("pergamino", 540, 1100, 720, keys=late(0.1, 1, 0.04)), brillo(540, 1000, 320, "#ffe8b0", 0.4, 0.44)],
             cam(1.1, 1.2, (540, 1000)), "corte", hud=[cap(0.05, d - 0.03, "«ODA AL DEPORTE»", tam=90)], sfx=[(0.05, "brillo", -20)])


@v.plano(82, "firmado con dos nombres inventados: anillo sobre la firma")
def _(d):
    return P(GAL, [BG("bg_galeria"), OB("pergamino", 540, 1100, 720), senala(700, 1350, 0.2, d - 0.05, 110, MAGENTA)],
             cam(1.0, 1.5, (540, 1100), (680, 1320)), "corte", hud=[cap(0.3, d - 0.05, "2 NOMBRES FALSOS", "#ffffff", "#c0392be6", 90)], sfx=[(0.2, "zap", -18)])


@v.plano(87, "detrás estaba el propio Coubertin: primer plano del barón y fogonazo")
def _(d):
    return P(GAL, [BG("bg_galeria"), OB("cara_baron", 540, 1100, 980, keys=[{"t": 0, "escala": 1.12}, {"t": 0.35, "escala": 1.0, "ease": "golpe"}]),
                   brillo(540, 900, 520, "#ffe8b0", 0.5, 0.4, pulso=[0.1, 0.4])],
             cam(1.0, 1.06, (540, 1000), temblor=3), "corte", hud=[amarillo(0.3, d - 0.05, "¡ERA ÉL!", y=560, tam=140, color=AMBAR)], sfx=[(0.05, "impacto", -15)])


@v.plano(92, "hubo hasta quien ganó en las dos cosas: dos medallas de oro")
def _(d):
    return P(EST, [BG("bg_estadio_noche"), medalla_cae("medalla_oro", 360, 0.1, 300, 1000), medalla_cae("medalla_oro", 720, 0.35, 300, 1000)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.4, d - 0.05, "DOS OROS", tam=110)], sfx=[(0.5, "ding", -18), (0.75, "ding", -18)])


@v.plano(100, "Walter Winans fue oro en tiro en mil novecientos ocho: el tirador y la diana")
def _(d):
    return P(EST, [BG("bg_estadio_noche"), PZ("tirador", 330, S_E, 900), OB("diana", 800, 1120, 360, z=0.48, keys=late(d * 0.6, 1, 0.06))],
             cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[contador(0.05, d - 0.05, 1890, 1908, 0.6, miles=False, tam=150, color="#141414", capsula="#ffffffe6", y=600)], sfx=[(d * 0.6, "golpe", -16)])


@v.plano(110, "y oro en escultura cuatro años después, con un caballo de bronce")
def _(d):
    return P(GAL, [BG("bg_galeria"), OB("escultura_caballo", 540, 1180, 960, keys=aparece(0.1)), medalla_cae("medalla_oro", 830, 1.0, 220, 760)],
             cam(1.0, 1.08, (540, 1100)), "corte", hud=[cap(0.4, d - 0.05, "ORO EN ESCULTURA", tam=90)], sfx=[(1.3, "ding", -18)])


@v.plano(122, "¿y por qué se acabó?: la medalla se balancea y se apaga")
def _(d):
    return P(OSC, [OB("medalla_oro", 540, 900, 420, keys=[{"t": 0, "rot": 10, "op": 1}, {"t": d, "rot": -10, "op": 0.5, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[amarillo(0.05, d - 0.03, "¿POR QUÉ SE ACABÓ?", y=1450, tam=90, color=AMBAR)], sfx=[(0.05, "whoosh", -20)])


@v.plano(127, "porque los artistas vivían de vender sus obras: el cuadro con un cartel de vendido")
def _(d):
    return P(GAL, [BG("bg_galeria"), OB("caballete", 540, 1050, 720), brillo(540, 900, 300, "#ffd8a0", 0.4, 0.44)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.3, d - 0.05, "VIVÍAN DE SU ARTE", "#ffffff", "#c0392be6", 90)], sfx=[(0.3, "pop", -20)])


@v.plano(135, "y entonces los Juegos eran solo para aficionados: un corredor en la pista")
def _(d):
    return P(EST, [BG("bg_estadio_noche"), PZ("nino_corre", 540, S_E, 600, keys=[{"t": 0, "x": 200}, {"t": d, "x": 880, "ease": "lineal"}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[cap(0.3, d - 0.05, "SOLO AFICIONADOS", tam=100)], sfx=[(0.1, "whoosh", -20)])


@v.plano(143, "hoy esas medallas no cuentan: las tres medallas se tachan")
def _(d):
    return P(OSC, [OB("medalla_plata", 270, 1000, 240), OB("medalla_oro", 540, 950, 280), OB("medalla_bronce", 810, 1000, 240), *tacha(540, 1000, 0.3, 300)],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.4, d - 0.05, "NO CUENTAN", "#ffffff", "#c0392be6", 110)], sfx=[(0.3, "zap", -16)])


@v.plano(148, "¿tú en qué competirías?: los cinco concursos y la medalla (bucle)")
def _(d):
    return P(GAL, [BG("bg_galeria"), *iconos(0.0, 1080, 0.9), OB("medalla_oro", 540, 760, 300, z=0.62, keys=[{"t": 0, "rot": 8}, {"t": d, "rot": -6, "ease": "suave"}])],
             cam(1.0, 1.04, (540, 1050)), "corte", sfx=[(0.1, "pop", -22)])


v.construir("2026-11-25-tarde-02-medallas-arte", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 1252, "db": -13},
            claves=["medalla", "olímpica", "pintar", "oro", "plata", "bronce", "arte", "pintura", "escultura", "arquitectura", "literatura", "música",
                    "deporte", "Coubertin", "poema", "inventados", "Winans", "tiro", "caballo", "aficionados"],
            ep_extra={"sfx_bajo_voz": True})
