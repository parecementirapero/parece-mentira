"""01 · Este segundo no existe (el segundo intercalar) — método denso, estilo del vídeo largo. Lote 2026-11-28-tarde (Jorge con el agente).
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comun_1128t as C  # noqa: E402
from comun_1128t import *  # noqa: E402,F401,F403
import ilus_1128t  # noqa: E402

SVG = ilus_1128t.generar(os.path.join(sys.argv[1], "_svg_lote"))
C.SVG_DIR = SVG
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
OSCU = ["#0b0f24", "#1b1340"]
ESP = ["#02030a", "#0a1030"]
CASA = ["#d8dce2", "#8a9098"]
SALA = ["#e8dcc4", "#a89272"]
CIAN, LIMA, ROJO = "#2ff3ff", "#5dff8a", "#ff3d3d"
S_O = SUELO["bg_oficina_gris"]


def relojes(t, x=540, y=1100, ancho=960, z=0.5, fin="reloj_595960"):
    """El reloj pasa de 23:59:59 a la pieza `fin` en el instante t (con golpe)."""
    return [OB("reloj_595959", x, y, ancho, z=z, keys=[{"t": 0, "op": 1}, {"t": t, "op": 1}, {"t": t + 0.02, "op": 0}]),
            OB(fin, x, y, ancho, z=z + 0.01, keys=[{"t": 0, "op": 0}, {"t": t, "op": 0}, {"t": t + 0.02, "op": 1}] + late(t, 2, 0.06, 0.25))]


@v.plano(0, "gancho: el reloj enorme salta de 23:59:59 a 23:59:60 en rojo")
def _(d):
    return P(OSCU, [BG("bg_cerebro")] + relojes(0.15, 540, 1100, 1040) + [brillo(540, 1100, 520, ROJO, 0.6, 0.3, keys=[{"t": 0, "op": 0}, {"t": 0.17, "op": 1}])],
             cam(1.0, 1.08, (540, 1100)), vineta=0.35, sfx=[(0.0, "tic", -14), (0.15, "impacto", -14)])


@v.plano(4, "mira el reloj: veintitrés, cincuenta y nueve, sesenta, cuenta en grande")
def _(d):
    return P(OSCU, [BG("bg_cerebro")] + relojes(max(0.3, d * 0.75), 540, 1100, 980), cam(1.1, 1.18, (540, 1100)), "corte",
             sfx=[(0.1, "tic", -18), (d * 0.4, "tic", -18), (d * 0.75, "impacto", -16)])


@v.plano(12, "ese minuto tuvo sesenta y un segundos: contador de 59 a 61")
def _(d):
    return P(OSCU, [BG("bg_cerebro"), OB("reloj_595960", 540, 1250, 760, keys=late(0.2, 1, 0.04, 0.3))], cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[contador(0.05, d - 0.05, 59, 61, 0.8, " S", tam=140, color="#141414", capsula="#ff5a4ae6", y=640)], sfx=[(0.05, "tic", -18), (0.8, "ding", -18)])


@v.plano(19, "se llama segundo intercalar")
def _(d):
    return P(OSCU, [BG("bg_cerebro"), OB("reloj_595960", 540, 1150, 900)], cam(1.05, 1.12, (540, 1150)), "corte",
             hud=[amarillo(0.05, d - 0.05, "SEGUNDO INTERCALAR", y=650, tam=86, color=AMBAR)], sfx=[(0.05, "brillo", -18)])


@v.plano(23, "los relojes atómicos casi no fallan: el reloj atómico brilla")
def _(d):
    return P(CASA, [BG("bg_oficina_gris"), PZ("reloj_atomico", 540, S_O, 1000, keys=aparece(0.0)),
                    brillo(540, 990, 260, CIAN, 0.6, 0.6, keys=late(0.1, 3, 0.15, 0.4))],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[BANDA(), cap(0.3, d - 0.05, "RELOJ ATÓMICO", "#141414", "#7df9ffe6", 96, y=760)], sfx=[(0.1, "senal", -20)])


@v.plano(29, "pero la Tierra no gira siempre igual de rápido: la Tierra gira con tirones")
def _(d):
    ks = [{"t": 0, "rot": 0}, {"t": d * 0.3, "rot": 30, "ease": "lineal"}, {"t": d * 0.45, "rot": 34}, {"t": d * 0.8, "rot": 70, "ease": "lineal"}, {"t": d, "rot": 76}]
    return P(ESP, [estrellas(100, 4), OB("foto_mundo", 540, 1150, 820, keys=ks)], cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[cap(0.3, d - 0.05, "NO GIRA IGUAL", "#141414", "#ffd23fe6", 96, y=640)], sfx=[(0.1, "whoosh", -20)])


@v.plano(38, "a la larga se va frenando, un poquito: la Tierra gira cada vez más despacio")
def _(d):
    return P(ESP, [estrellas(100, 5), OB("foto_mundo", 540, 1150, 820, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 40, "ease": "salida"}])],
             cam(1.0, 1.04, (540, 1100)), "corte", hud=[cap(0.3, d - 0.05, "SE FRENA", "#ffffff", "#c0392be6", 110, y=640)], sfx=[(0.1, "roce", -22)])


@v.plano(46, "cuando la hora de los relojes y la del planeta se separan casi un segundo: dos líneas que se separan")
def _(d):
    t1 = min(1.2, d * 0.6)
    return P(ESP, [estrellas(80, 6), OB("reloj_atomico", 280, 1100, 300, keys=aparece(0.0)), OB("foto_mundo", 800, 1100, 380, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 25}]),
                   flecha([[140, 1450], [940, 1450]], 0.1, t1, CIAN, 10, z=0.6),
                   flecha([[140, 1450], [940, 1560]], 0.1, t1, AMBAR, 10, z=0.6)],
             cam(1.0, 1.04, (540, 1200)), "corte", hud=[cap(t1, d - 0.05, "CASI 1 SEGUNDO", "#141414", "#ffd23fe6", 90, y=640)], sfx=[(0.1, "tic", -20)])


@v.plano(63, "se mete uno extra justo antes de medianoche: 59, 60 y luego 00")
def _(d):
    t1, t2 = d * 0.3, d * 0.7
    return P(OSCU, [BG("bg_cerebro"),
                    OB("reloj_595959", 540, 1150, 900, keys=[{"t": 0, "op": 1}, {"t": t1, "op": 1}, {"t": t1 + 0.02, "op": 0}]),
                    OB("reloj_595960", 540, 1150, 900, z=0.51, keys=[{"t": 0, "op": 0}, {"t": t1, "op": 0}, {"t": t1 + 0.02, "op": 1}, {"t": t2, "op": 1}, {"t": t2 + 0.02, "op": 0}]),
                    OB("reloj_000000", 540, 1150, 900, z=0.52, keys=[{"t": 0, "op": 0}, {"t": t2, "op": 0}, {"t": t2 + 0.02, "op": 1}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[cap(0.1, d - 0.05, "+1 SEGUNDO", "#141414", "#ff5a4ae6", 110, y=640)],
             sfx=[(0.05, "tic", -20), (t1, "impacto", -18), (t2, "ding", -18)])


@v.plano(71, "desde mil novecientos setenta y dos se han añadido veintisiete: veintisiete marcas que se encienden")
def _(d):
    els = [BG("bg_cerebro")]
    for i in range(27):
        f, c = divmod(i, 9)
        ti = 0.6 + i * min(0.05, (d - 0.9) / 30)
        els.append({"tipo": "forma", "forma": "rect", "ancho": 70, "alto": 70, "relleno": "#ff5a4a", "x": 180 + c * 90, "y": 1050 + f * 100, "z": 0.6,
                    "keys": [{"t": 0, "op": 0.15}, {"t": ti, "op": 0.15}, {"t": ti + 0.05, "op": 1}]})
    return P(OSCU, els, cam(1.0, 1.04, (540, 1150)), "corte",
             hud=[contador(0.05, 0.6, 1960, 1972, 0.4, miles=False, tam=130, color="#141414", capsula="#ffffffe6", y=640),
                  cap(0.65, d - 0.05, "27 SEGUNDOS", "#141414", "#ffd23fe6", 110, y=640)], sfx=[(0.6 + i * 0.15, "tic", -26) for i in range(6)])


@v.plano(81, "¿el problema?: el servidor")
def _(d):
    return P(CASA, [BG("bg_oficina_gris"), PZ("servidor", 540, S_O, 1000, keys=aparece(0.0))], cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[BANDA(), amarillo(0.05, d - 0.05, "¿EL PROBLEMA?", y=760, tam=110, color=AMBAR)], sfx=[(0.05, "impacto", -20)])


@v.plano(83, "a los ordenadores no les gusta: puede hacer fallar sistemas, el servidor se pone en rojo con chispa")
def _(d):
    t = min(0.8, d * 0.4)
    return P(CASA, [BG("bg_oficina_gris"), PZ("servidor", 540, S_O, 1000, keys=[{"t": 0, "op": 1}, {"t": t, "op": 1}, {"t": t + 0.05, "op": 0}]),
                    PZ("servidor_fallo", 540, S_O, 1000, z=0.51, keys=[{"t": 0, "op": 0}, {"t": t, "op": 0}, {"t": t + 0.05, "op": 1}] + vibra(t, t + 0.5, 540, 8)),
                    brillo(540, 1000, 500, ROJO, 0.6, 0.6, keys=[{"t": 0, "op": 0}, {"t": t, "op": 0.8}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[BANDA(), cap(t, d - 0.05, "FALLOS", "#ffffff", "#c0392be6", 120, y=760)], sfx=[(t, "impacto", -16)])


@v.plano(98, "Google lo reparte poco a poco en las horas de alrededor: barra que se llena despacio")
def _(d):
    return P(CASA, [BG("bg_oficina_gris"), OB("pantalla_ordenador", 540, 1150, 760, keys=aparece(0.0)),
                    {"tipo": "forma", "forma": "rect", "ancho": 600, "alto": 40, "relleno": "#5dff8a", "x": 540, "y": 1500, "z": 0.7,
                     "keys": [{"t": 0, "escala": 0.05}, {"t": d, "escala": 1.0, "ease": "lineal"}]}],
             cam(1.0, 1.04, (540, 1200)), "corte", hud=[BANDA(), cap(0.3, d - 0.05, "POCO A POCO", "#141414", "#5dff8ae6", 100, y=760)], sfx=[(0.1, "tic", -22)])


@v.plano(111, "por eso, en dos mil veintidós, cerca de París, se votó jubilarlo: la sala, manos arriba")
def _(d):
    S = 1360
    ps = ["oyente", "chica_saluda", "oyente", "chica_saluda"]
    els = [BG("bg_sala_votacion")] + [PZ(p, 180 + i * 240, S + (i % 2) * 30, 560, z=0.5 + i * 0.01, keys=aparece(0.3 + 0.12 * i)) for i, p in enumerate(ps)]
    return P(SALA, els, cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[BANDA(), contador(0.05, min(0.8, d * 0.4), 2015, 2022, 0.4, miles=False, tam=120, color="#141414", capsula="#ffffffe6", y=760),
                  cap(min(0.85, d * 0.42), d - 0.05, "SE VOTA", "#ffffff", "#2a5ae8e6", 110, y=760)], sfx=[(0.3 + 0.12 * i, "pop", -22) for i in range(4)])


@v.plano(123, "hacia dos mil treinta y cinco no se añadirán más: el reloj se tacha")
def _(d):
    return P(OSCU, [BG("bg_cerebro"), OB("reloj_595960", 540, 1150, 900)] + tacha(540, 1150, 0.4, 260),
             cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[contador(0.05, d - 0.05, 2022, 2035, 0.5, miles=False, tam=140, color="#141414", capsula="#7df9ffe6", y=640)], sfx=[(0.4, "impacto", -16)])


@v.plano(133, "dejarán que la diferencia crezca hasta un minuto: las líneas se separan mucho")
def _(d):
    return P(ESP, [estrellas(80, 7), flecha([[140, 1150], [940, 1150]], 0.0, 0.3, CIAN, 10, z=0.6),
                   flecha([[140, 1150], [940, 1500]], 0.1, d * 0.8, AMBAR, 12, z=0.6)],
             cam(1.0, 1.04, (540, 1250)), "corte", hud=[cap(0.3, d - 0.05, "HASTA 1 MINUTO", "#141414", "#ffd23fe6", 96, y=640)], sfx=[(0.1, "whoosh", -20)])


@v.plano(141, "y para eso hará falta un siglo: contador de cien años")
def _(d):
    return P(ESP, [estrellas(80, 8), OB("foto_mundo", 540, 1150, 760, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 200, "ease": "lineal"}])],
             cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[contador(0.05, d - 0.05, 0, 100, max(0.5, d * 0.7), " AÑOS", tam=120, color="#141414", capsula="#ffffffe6", y=640)], sfx=[(0.05, "tic", -20)])


@v.plano(148, "¿tú lo sabías? (bucle): el reloj vuelve a saltar a 23:59:60")
def _(d):
    return P(OSCU, [BG("bg_cerebro")] + relojes(min(0.4, d * 0.4), 540, 1100, 1040), cam(1.0, 1.06, (540, 1100)), "corte",
             sfx=[(min(0.4, d * 0.4), "impacto", -18)])


def micro(fondo, els, txt=None, col="#ffffff", cap_f="#c0392be6", sfx="pop"):
    def fn(d):
        return P(fondo, els(d), cam(1.15, 1.3, (540, 1000)), "corte", hud=[cap(0.0, d - 0.02, txt, col, cap_f, 120)] if txt else [], sfx=[(0.01, sfx, -18)])
    return fn


v.plano(57, "micro: el planeta")(micro(ESP, lambda d: [estrellas(60, 10), OB("foto_mundo", 540, 1050, 900, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 20}])], sfx="tic"))
v.plano(88, "micro: pantalla")(micro(CASA, lambda d: [BG("bg_oficina_gris"), OB("pantalla_ordenador", 540, 1100, 1100)], sfx="pop"))
v.plano(11, "micro: el 60 en rojo")(micro(OSCU, lambda d: [BG("bg_cerebro"), OB("reloj_595960", 700, 1050, 1700)], sfx="impacto"))


v.construir("2026-11-28-tarde-01-segundo-intercalar", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 1281, "db": -13},
            claves=["segundo", "existe", "reloj", "sesenta", "intercalar", "atómicos", "Tierra", "rápido", "frenando", "medianoche",
                    "veintisiete", "problema", "ordenadores", "fallar", "Google", "París", "jubilarlo", "treinta", "minuto", "siglo"],
            ep_extra={"sfx_bajo_voz": True})
