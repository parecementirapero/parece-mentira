"""02 · Este escudo mide tres milímetros (la capa de ozono) — método denso, estilo del vídeo largo. Lote 2026-11-27-tarde (Agente 20:00 (Jorge)).
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comun_1127t as C  # noqa: E402
from comun_1127t import *  # noqa: E402,F401,F403
import ilus_1127t  # noqa: E402

SVG = ilus_1127t.generar(os.path.join(sys.argv[1], "_svg_lote"))
C.SVG_DIR = SVG
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
ESP = ["#02030a", "#0a1030"]
CASA = ["#d8dce2", "#8a9098"]
CIAN, LIMA, VIOL = "#2ff3ff", "#5dff8a", "#d29aff"


def mundo(x=540, y=1100, A=760, giro=8, d=1.0, aura=True, hueco=False, z=0.4):
    els = [OB("foto_mundo", x, y, A, z=z, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": giro}])]
    if aura:
        els.append(OB("aura_ozono_hueco" if hueco else "aura_ozono", x, y, A * 1.06, z=z + 0.02, keys=late(0.1, 2, 0.03, 0.6)))
    return els


def rayo(x, y0, y1, t0, t1, ancho=110, z=0.6):
    return OB("rayo_uv", x, y0, ancho, z=z, keys=[{"t": 0, "op": 0}, {"t": t0, "y": y0, "op": 1}, {"t": t1, "y": y1, "ease": "lineal"}])


@v.plano(0, "gancho: el planeta con su escudo brillante y un rayo violeta que rebota")
def _(d):
    return P(ESP, [estrellas(100, 3)] + mundo(540, 1150, 820, 10, d) + [OB("sol_poniente", 980, 520, 380, z=0.2),
             OB("rayo_uv", 760, 560, 100, z=0.6, keys=[{"t": 0, "y": 560, "op": 1}, {"t": 0.6, "y": 700, "ease": "lineal"}, {"t": 0.7, "op": 0}]),
             brillo(700, 760, 120, VIOL, 0.8, 0.65, keys=[{"t": 0, "op": 0}, {"t": 0.6, "op": 1}, {"t": 1.0, "op": 0}])],
             cam(1.0, 1.06, (540, 1050)), vineta=0.35, sfx=[(0.0, "whoosh", -16), (0.6, "impacto", -18)])


@v.plano(5, "es la capa de ozono: el anillo se enciende")
def _(d):
    return P(ESP, [estrellas(90, 4)] + mundo(540, 1100, 900, 8, d), cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[cap(0.2, d - 0.05, "CAPA DE OZONO", "#141414", "#7df9ffe6", 96, y=600)], sfx=[(0.1, "brillo", -18)])


@v.plano(10, "flota a más de diez kilómetros: el borde del planeta desde muy alto")
def _(d):
    return P(ESP, [BG("bg_estratosfera"), flecha([[860, 1640], [860, 1350]], 0.1, 0.5, CIAN, 10, z=0.6)], cam(1.0, 1.05, (540, 1300)), "corte",
             hud=[contador(0.1, d - 0.05, 0, 10, 0.5, " KM", tam=120, color="#141414", capsula="#7df9ffe6", y=1150, x=760)], sfx=[(0.1, "whoosh", -20)])


@v.plano(18, "pero si la aplastaras a la presión del suelo: una prensa baja sobre el anillo")
def _(d):
    return P(ESP, [estrellas(80, 5)] + mundo(540, 1150, 820, 6, d) +
             [{"tipo": "forma", "forma": "rect", "ancho": 900, "alto": 60, "relleno": "#c8ccd4", "x": 540, "y": 600, "z": 0.7,
               "keys": [{"t": 0, "y": 500}, {"t": d * 0.8, "y": 720, "ease": "entrada"}]}],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[cap(0.3, d - 0.05, "APLASTADA", "#ffffff", "#c0392be6", 100, y=1700)], sfx=[(d * 0.8, "impacto", -18)])


@v.plano(27, "sería tan fina como dos monedas apiladas: las monedas de cerca")
def _(d):
    return P(CASA, [BG("bg_oficina_gris"), OB("dos_monedas", 540, 1150, 900, keys=cae(0.0, 0.3, 900, 1150))],
             cam(1.0, 1.08, (540, 1150)), "corte", hud=[BANDA(), cap(0.4, d - 0.05, "3 MM", "#141414", "#ffd23fe6", 150, y=780)], sfx=[(0.3, "ding", -18)])


@v.plano(34, "y esos milímetros frenan casi toda la luz ultravioleta más dañina: los rayos chocan con el anillo y rebotan")
def _(d):
    els = [estrellas(90, 6)] + mundo(540, 1300, 900, 5, d)
    for i, x in enumerate((300, 540, 780)):
        t0 = 0.1 + 0.25 * i
        els.append(OB("rayo_uv", x, 600, 90, z=0.6, keys=[{"t": 0, "op": 0}, {"t": t0, "y": 520, "op": 1}, {"t": t0 + 0.4, "y": 760, "ease": "lineal"}, {"t": t0 + 0.45, "op": 0}]))
        els.append(brillo(x, 860, 90, VIOL, 0.8, 0.65, keys=[{"t": 0, "op": 0}, {"t": t0 + 0.4, "op": 1}, {"t": t0 + 0.8, "op": 0}]))
    return P(ESP, els, cam(1.0, 1.04, (540, 1100)), "corte", hud=[cap(0.3, d - 0.05, "ULTRAVIOLETA", "#ffffff", "#7a2ad0e6", 100, y=1700)],
             sfx=[(0.5 + 0.25 * i, "pop", -20) for i in range(3)])


@v.plano(45, "del sol: el sol que quema")
def _(d):
    return P(ESP, [estrellas(60, 7), OB("sol_poniente", 540, 1000, 900, keys=late(0.0, 2, 0.05, 0.4))], cam(1.0, 1.05, (540, 1000)), "corte", sfx=[(0.05, "brillo", -18)])


@v.plano(47, "en los años ochenta apareció un agujero sobre la Antártida: el polo sur y la mancha que crece")
def _(d):
    return P(ESP, [estrellas(90, 8), OB("polo_sur", 540, 1150, 860, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 12}]),
                   OB("agujero_ozono", 540, 1150, 560, z=0.6, keys=[{"t": 0, "escala": 0.2, "op": 0}, {"t": d * 0.7, "escala": 1.0, "op": 1, "ease": "salida"}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[cap(0.05, min(0.8, d * 0.4), "AÑOS 80", "#141414", "#ffffffe6", 120, y=600),
                                                        cap(min(0.9, d * 0.45), d - 0.05, "ANTÁRTIDA", "#141414", "#7df9ffe6", 96, y=1700)], sfx=[(0.3, "whoosh", -18)])


@v.plano(57, "¿el culpable?: la mancha late")
def _(d):
    return P(ESP, [estrellas(80, 9), OB("polo_sur", 540, 1150, 900), OB("agujero_ozono", 540, 1150, 620, z=0.6, keys=late(0.0, 2, 0.08, 0.3))],
             cam(1.1, 1.15, (540, 1150)), "corte", hud=[amarillo(0.05, d - 0.05, "¿CULPABLE?", y=620, tam=130, color=AMBAR)], sfx=[(0.05, "impacto", -18)])


@v.plano(59, "gases de neveras: la nevera")
def _(d):
    S = SUELO["bg_oficina_gris"]
    return P(CASA, [BG("bg_oficina_gris"), PZ("nevera", 540, S, 900, keys=aparece(0.0))], cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[BANDA()], sfx=[(0.05, "pop", -20)])


@v.plano(62, "aires acondicionados: el aparato sopla")
def _(d):
    return P(CASA, [BG("bg_oficina_gris"), OB("aire_acond", 540, 1050, 900, keys=aparece(0.0))], cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[BANDA()], sfx=[(0.05, "whoosh", -22)])


@v.plano(64, "y espráis: el bote suelta su nube")
def _(d):
    S = SUELO["bg_oficina_gris"]
    return P(CASA, [BG("bg_oficina_gris"), PZ("spray", 460, S, 760, keys=late(0.1, 2, 0.06, 0.25))], cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[BANDA()], sfx=[(0.1, "roce", -18)])


@v.plano(66, "subían: la molécula sube hacia el cielo")
def _(d):
    return P(ESP, [BG("bg_estratosfera"), OB("molecula_cfc", 540, 1300, 360, keys=[{"t": 0, "y": 1600}, {"t": d, "y": 900, "ease": "suave"}, {"t": 0, "rot": 0}, {"t": d, "rot": 40}])],
             cam(1.0, 1.04, (540, 1200)), "corte", sfx=[(0.1, "whoosh", -20)])


@v.plano(67, "la luz del sol les arrancaba el cloro: el rayo la parte y sale el átomo verde")
def _(d):
    t = min(0.4, d * 0.3)
    return P(ESP, [estrellas(70, 10), OB("molecula_cfc", 540, 1100, 460, keys=[{"t": 0, "op": 1}, {"t": t + 0.1, "op": 0.6}]),
                   OB("rayo_uv", 540, 600, 90, z=0.6, keys=[{"t": 0, "y": 500}, {"t": t, "y": 800, "ease": "lineal"}, {"t": t + 0.1, "op": 0}]),
                   OB("atomo_cloro", 540, 1000, 220, z=0.65, keys=[{"t": 0, "op": 0}, {"t": t, "x": 540, "y": 1000, "op": 1}, {"t": d, "x": 860, "y": 720, "ease": "salida"}])],
             cam(1.0, 1.05, (600, 1000)), "corte", hud=[cap(t, d - 0.05, "CLORO", "#141414", "#5dff8ae6", 110, y=1500)], sfx=[(t, "impacto", -18)])


@v.plano(75, "y cada átomo de cloro rompía ozono: el cloro choca con la molécula azul y la parte")
def _(d):
    t = min(0.6, d * 0.4)
    return P(ESP, [estrellas(70, 11), OB("molecula_ozono", 600, 1100, 520, keys=[{"t": 0, "op": 1}, {"t": t, "op": 1}, {"t": t + 0.15, "op": 0}]),
                   OB("atomo_cloro", 200, 1100, 220, z=0.65, keys=[{"t": 0, "x": 200}, {"t": t, "x": 520, "ease": "entrada"}, {"t": d, "x": 500}]),
                   brillo(600, 1100, 260, "#ffffff", 0.8, 0.7, keys=[{"t": 0, "op": 0}, {"t": t, "op": 1}, {"t": t + 0.3, "op": 0}])],
             cam(1.0, 1.04, (540, 1100)), "corte", hud=[cap(t, d - 0.05, "ROMPE OZONO", "#ffffff", "#c0392be6", 100, y=1600)], sfx=[(t, "impacto", -16)])


@v.plano(82, "y salía intacto, listo para romper más: el cloro sigue y rompe otra")
def _(d):
    els = [estrellas(70, 12)]
    for i, x in enumerate((360, 720)):
        t = 0.3 + 0.5 * i
        els.append(OB("molecula_ozono", x, 1000 + 200 * i, 300, keys=[{"t": 0, "op": 1}, {"t": t, "op": 1}, {"t": t + 0.12, "op": 0}]))
        els.append(brillo(x, 1000 + 200 * i, 160, "#ffffff", 0.8, 0.7, keys=[{"t": 0, "op": 0}, {"t": t, "op": 1}, {"t": t + 0.25, "op": 0}]))
    els.append(OB("atomo_cloro", 100, 900, 180, z=0.65, keys=[{"t": 0, "x": 100, "y": 900}, {"t": 0.3, "x": 360, "y": 1000}, {"t": 0.8, "x": 720, "y": 1200}, {"t": d, "x": 980, "y": 1350}]))
    return P(ESP, els, cam(1.0, 1.04, (540, 1100)), "corte", hud=[cap(0.2, d - 0.05, "INTACTO", "#141414", "#5dff8ae6", 110, y=640)],
             sfx=[(0.3, "pop", -18), (0.8, "pop", -18)])


@v.plano(89, "en mil novecientos ochenta y siete: el año corre")
def _(d):
    return P(ESP, [estrellas(80, 13)] + mundo(540, 1150, 760, 6, d), cam(1.0, 1.04, (540, 1100)), "corte",
             hud=[contador(0.05, d - 0.05, 1980, 1987, 0.6, miles=False, tam=150, color="#141414", capsula="#ffffffe6", y=620)], sfx=[(0.05, "tic", -18)])


@v.plano(95, "el mundo firmó el Protocolo de Montreal: el documento se firma")
def _(d):
    return P(CASA, [BG("bg_oficina_gris"), OB("pergamino", 540, 1150, 640, keys=aparece(0.0) + [{"t": 0, "rot": -3}, {"t": d, "rot": 2}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[BANDA(), cap(0.3, d - 0.05, "MONTREAL", "#ffffff", "#2a5ae8e6", 110, y=720)], sfx=[(0.3, "roce", -18)])


@v.plano(102, "y prohibió esos gases: tachan la nevera y el espray")
def _(d):
    S = SUELO["bg_oficina_gris"]
    return P(CASA, [BG("bg_oficina_gris"), PZ("nevera", 330, S, 640), PZ("spray", 760, S, 480)] + tacha(330, 1150, 0.15, 170) + tacha(760, 1250, 0.3, 130),
             cam(1.0, 1.04, (540, 1150)), "corte", hud=[BANDA()], sfx=[(0.15, "impacto", -18), (0.3, "impacto", -18)])


@v.plano(106, "y pasó algo único: todos los países lo ratificaron, el planeta se llena de luces")
def _(d):
    import random
    r = random.Random(5)
    els = [estrellas(80, 14)] + mundo(540, 1150, 820, 8, d, aura=False)
    for i in range(18):
        a = r.uniform(0, 6.28); rr = r.uniform(40, 330)
        x, y = 540 + rr * 0.9 * __import__("math").cos(a), 1150 + rr * 0.9 * __import__("math").sin(a)
        ti = 0.2 + i * 0.06
        els.append(brillo(x, y, 34, "#ffd23f", 0.9, 0.6, keys=[{"t": 0, "op": 0}, {"t": ti, "op": 1}]))
    return P(ESP, els, cam(1.0, 1.05, (540, 1100)), "corte", hud=[amarillo(0.05, min(1.2, d * 0.35), "ÚNICO", y=620, tam=130, color=AMBAR),
                                                              cap(min(1.3, d * 0.4), d - 0.05, "TODOS LOS PAÍSES", "#141414", "#ffd23fe6", 86, y=620)],
             sfx=[(0.2 + i * 0.18, "tic", -26) for i in range(6)])


@v.plano(118, "este año el agujero ha sido grande: la mancha crece mucho")
def _(d):
    return P(ESP, [estrellas(90, 15), OB("polo_sur", 540, 1150, 900), OB("agujero_ozono", 540, 1150, 560, z=0.6, keys=[{"t": 0, "escala": 0.7}, {"t": d, "escala": 1.15, "ease": "salida"}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[cap(0.2, d - 0.05, "2026: GRANDE", "#ffffff", "#7a2ad0e6", 100, y=620)], sfx=[(0.1, "whoosh", -18)])


@v.plano(125, "por un frío polar muy fuerte: el remolino helado gira")
def _(d):
    return P(ESP, [estrellas(80, 16), OB("polo_sur", 540, 1150, 900), OB("vortice", 540, 1150, 900, z=0.6, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": -120}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[cap(0.2, d - 0.05, "FRÍO POLAR", "#141414", "#7df9ffe6", 100, y=620)], sfx=[(0.1, "roce", -18)])


@v.plano(131, "pero con el cloro del año dos mil, habría sido mayor: la mancha fantasma más grande")
def _(d):
    return P(ESP, [estrellas(80, 17), OB("polo_sur", 540, 1150, 900),
                   OB("agujero_ozono", 540, 1150, 760, z=0.55, keys=[{"t": 0, "op": 0}, {"t": 0.4, "op": 0.35}]),
                   OB("agujero_ozono", 540, 1150, 560, z=0.6)],
             cam(1.0, 1.04, (540, 1150)), "corte", hud=[cap(0.2, d - 0.05, "CLORO DEL 2000", "#141414", "#5dff8ae6", 90, y=620)], sfx=[(0.3, "pop", -20)])


@v.plano(142, "hacia dos mil setenta estará curado: el agujero se cierra y el anillo vuelve entero")
def _(d):
    return P(ESP, [estrellas(80, 18), OB("polo_sur", 540, 1150, 900),
                   OB("agujero_ozono", 540, 1150, 560, z=0.6, keys=[{"t": 0, "escala": 1.0, "op": 1}, {"t": d * 0.8, "escala": 0.1, "op": 0, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[contador(0.05, d - 0.05, 2026, 2070, max(0.5, d * 0.6), miles=False, tam=140, color="#141414", capsula="#5dff8ae6", y=620)], sfx=[(0.05, "tic", -18), (d * 0.8, "ding", -18)])


@v.plano(148, "¿sabías que lo estábamos arreglando? (bucle): el planeta con el escudo y el rayo, como al principio")
def _(d):
    return P(ESP, [estrellas(100, 3)] + mundo(540, 1150, 820, 10, d), cam(1.0, 1.06, (540, 1050)), "corte", sfx=[(0.05, "brillo", -20)])


def micro(fondo, els, txt=None, col="#ffffff", cap_f="#c0392be6", sfx="pop"):
    def fn(d):
        return P(fondo, els(d), cam(1.15, 1.3, (540, 1000)), "corte", hud=[cap(0.0, d - 0.02, txt, col, cap_f, 120)] if txt else [], sfx=[(0.01, sfx, -18)])
    return fn


v.plano(3, "micro: tres milímetros")(micro(ESP, lambda d: [estrellas(60, 2), OB("aura_ozono", 540, 1000, 1100)], "3 MM", "#141414", "#7df9ffe6", "impacto"))
v.plano(31, "micro: dos monedas")(micro(CASA, lambda d: [BG("bg_oficina_gris"), OB("dos_monedas", 540, 1050, 1000)], sfx="ding"))
v.plano(42, "micro: el rayo violeta")(micro(ESP, lambda d: [estrellas(60, 19), OB("rayo_uv", 540, 1000, 260)], sfx="brillo"))
v.plano(115, "micro: ONU")(micro(ESP, lambda d: [estrellas(60, 20), OB("foto_mundo", 540, 1050, 900)], "TODOS", "#141414", "#ffd23fe6", "impacto"))


v.construir("2026-11-27-tarde-02-capa-de-ozono", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 1272, "db": -13},
            claves=["escudo", "tres", "milímetros", "ozono", "diez", "kilómetros", "monedas", "ultravioleta", "agujero", "Antártida",
                    "culpable", "neveras", "espráis", "cloro", "intacto", "Montreal", "único", "ONU", "grande", "frío", "mayor", "setenta", "curado"],
            ep_extra={"sfx_bajo_voz": True})
