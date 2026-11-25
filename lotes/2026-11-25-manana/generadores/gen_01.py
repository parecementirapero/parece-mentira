"""01 · El Hubble nació miope — método denso, estilo cartoon. Lote 2026-11-25-manana (Nico, con el agente).
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
from comun_1125m import *  # noqa: E402,F401,F403
import ilus_1125m  # noqa: E402

SVG = ilus_1125m.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
NEG = ["#070a1e", "#141a3e"]
SAT0, SAT1 = v.w(10), v.w(34)     # satélite de fondo que cruza durante varios planos
SAT2, SAT3 = v.w(130), v.w(159)


def sat(d, T0=None, T1=None, p0=(-120, 520), p1=(1200, 760)):
    return IMG("satelite", ancho=150, z=0.15, keys=recorrido(T0 or SAT0, T1 or SAT1, p0, p1, d))


def hub(x, y, ancho=560, gaf=False, p1=None, d=1.0, z=0.5, ease="suave", keys=None):
    """Hubble (y sus gafas, encajadas en la boca del tubo). Se mueve de (x, y) a p1 durante el plano."""
    k = ancho / 760
    ks = keys or ([{"t": 0, "x": x, "y": y}, {"t": d, "x": p1[0], "y": p1[1], "ease": ease}] if p1 else [])
    els = [IMG("hubble", ancho=ancho, x=x, y=y, z=z, keys=ks)]
    if gaf:
        dy = -305 * k
        kg = [{**q, **({"y": q["y"] + dy} if "y" in q else {})} for q in ks]
        els.append(IMG("gafas", ancho=ancho * 0.62, x=x, y=y + dy, z=z + 0.02, keys=kg))
    return els


@v.plano(0, "gancho: el Hubble entra desde abajo delante de una estrella borrosa enorme")
def _(d):
    return P(NEG, [BG("bg_esp_violeta"), estrellas(50, 4), IMG("estrella_borrosa", ancho=760, x=560, y=760, z=0.2, keys=late(0.1, 3, 0.1, 0.5)),
                   *hub(540, 1100, 640, keys=arranque(540, 1100, d, "abajo", 320, 40))],
             cam(1.0, 1.1, (540, 1000)), vineta=0.5, sfx=[(0.05, "whoosh", -20), (0.4, "pop", -18)])


@v.plano(4, "es el Hubble y veía borroso: llega volando una foto desenfocada")
def _(d):
    return P(NEG, [BG("bg_esp_violeta"), estrellas(50, 4), *hub(330, 1180, 460, p1=(300, 1150), d=d),
                   IMG("foto_borrosa", ancho=480, x=770, y=980, z=0.6, keys=[{"t": 0, "x": 1300, "rot": 18}, {"t": 0.4, "x": 770, "rot": -5, "ease": "salida"}, {"t": d, "rot": 3, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[rotulo(0.1, d - 0.03, "HUBBLE", tam=110, color="#141414", capsula="#7df9ffe6", y=600)], sfx=[(0.1, "whoosh", -20)])


@v.plano(10, "llegó al espacio en 1990: sube desde la Tierra, el año corre")
def _(d):
    return P(NEG, [BG("bg_esp_petroleo"), estrellas(50, 5), sat(d), IMG("tierra_arco", ancho=1500, x=540, y=1700, z=0.3, keys=va((540, 1640), (540, 1760), d)),
                   *hub(540, 1500, 420, p1=(540, 940), d=d, ease="salida"), flecha([[540, 1620], [540, 1300]], 0.0, d * 0.6, CIAN, 8, disc=[26, 18], punta=False, z=0.4)],
             cam(1.0, 1.06, (540, 1100)), "corte",
             hud=[contador(0.05, d - 0.03, 1980, 1990, min(0.9, d * 0.6), miles=False, tam=150, color="#141414", capsula="#ffd23fe6", y=600)], sfx=[(0.05, "subida", -22, {"dur": min(0.9, d * 0.6)})])


@v.plano(17, "costó mil quinientos millones de dólares: cae el fajo de billetes")
def _(d):
    return P(NEG, [BG("bg_estudio"), sat(d), IMG("billetes", ancho=640, x=540, y=1150, z=0.5, keys=cae(0.0, 0.45, 300, 1150)),
                   IMG("billetes", ancho=360, x=240, y=1420, z=0.55, keys=cae(0.25, 0.7, 300, 1420)), IMG("billetes", ancho=360, x=850, y=1430, z=0.56, keys=cae(0.4, 0.85, 300, 1430))],
             cam(1.0, 1.06, (540, 1100)), "corte",
             hud=[contador(0.1, d - 0.03, 0, 1500, min(1.1, d * 0.6), " M $", tam=120, color="#141414", capsula="#7dff3ae6", y=640)], sfx=[(0.35, "golpe", -16), (0.6, "golpe", -20)])


@v.plano(23, "y sus primeras fotos fueron un desastre: la foto borrosa tiembla")
def _(d):
    return P(NEG, [BG("bg_estudio"), sat(d), IMG("foto_borrosa", ancho=800, x=540, y=1100, z=0.5, keys=[{"t": 0, "escala": 0.8, "rot": -8}, {"t": 0.3, "escala": 1.0, "rot": 2, "ease": "golpe"}, {"t": d, "rot": -2, "escala": 1.04, "ease": "suave"}])],
             cam(1.0, 1.08, (540, 1100), temblor=5), "corte", hud=[rotulo(0.35, d - 0.03, "DESASTRE", tam=120, color="#ffffff", capsula="#c0392be6", y=600)], sfx=[(0.1, "impacto", -16)])


@v.plano(30, "las estrellas parecían manchas: la estrella nítida se convierte en mancha")
def _(d):
    return P(NEG, [BG("bg_esp_violeta"), estrellas(40, 7), sat(d),
                   *cruza(IMG("estrella_nitida", ancho=700, x=540, y=1050, z=0.5), IMG("estrella_borrosa", ancho=820, x=540, y=1050, z=0.5), d * 0.35, 0.3),
                   IMG("estrella_borrosa", ancho=300, x=220, y=1500, z=0.4, keys=aparece(d * 0.5)), IMG("estrella_borrosa", ancho=240, x=870, y=700, z=0.4, keys=aparece(d * 0.6))],
             cam(1.0, 1.08, (540, 1050)), "corte", hud=[amarillo(d * 0.45, d - 0.03, "MANCHAS", y=1300, tam=110, color=MAGENTA)], sfx=[(d * 0.35, "zap", -20)])


@v.plano(34, "¿el fallo?: micro plano, el Hubble con un anillo que busca")
def _(d):
    return P(NEG, [BG("bg_esp_petroleo"), estrellas(40, 5), *hub(540, 1080, 560), senala(540, 1000, 0.05, d - 0.03, 170, AMBAR)],
             cam(1.05, 1.2, (540, 1050)), "corte", sfx=[(0.05, "ding", -18)])


@v.plano(36, "su espejo principal: el espejo llega girando")
def _(d):
    return P(NEG, [BG("bg_estudio"), brillo(540, 1050, 520, "#7df9ff", 0.3, 0.06), IMG("espejo_hubble", ancho=760, x=540, y=1080, z=0.5, keys=arranque(540, 1080, d, "derecha", 360, 20))],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[rotulo(0.3, d - 0.03, "EL ESPEJO", tam=100, color="#141414", capsula="#7df9ffe6", y=600)], sfx=[(0.05, "whoosh", -20), (0.4, "brillo", -18)])


@v.plano(39, "mide dos metros cuarenta: una persona al lado para la escala y la cota")
def _(d):
    return P(NEG, [BG("bg_estudio"), IMG("espejo_hubble", ancho=620, x=460, y=1100, z=0.5, keys=late(0.2, 1, 0.04)),
                   IMG("persona_pie_clara", ancho=150, x=900, y=1180, z=0.55, keys=aparece(0.1)),
                   flecha([[150, 1470], [770, 1470]], 0.15, 0.6, LIMA, 9, z=0.6), flecha([[770, 1470], [150, 1470]], 0.15, 0.6, LIMA, 9, z=0.6)],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[rotulo(0.3, d - 0.03, "2,40 m", tam=120, color="#141414", capsula="#7dff3ae6", y=640)], sfx=[(0.2, "trazo", -20)])


@v.plano(43, "y el borde estaba demasiado plano: el espejo cortado, curva ideal y curva real")
def _(d):
    return P(NEG, [BG("bg_estudio"), IMG("espejo_corte", ancho=980, x=540, y=1100, z=0.5, keys=aparece(0.0, 0.25)),
                   senala(110, 960, d * 0.45, d - 0.03, 90, "#ff3d3d"), senala(970, 960, d * 0.55, d - 0.03, 90, "#ff3d3d")],
             cam(1.0, 1.08, (540, 1080)), "corte", hud=[rotulo(0.1, d - 0.03, "DEMASIADO PLANO", tam=84, color="#ffffff", capsula="#c0392be6", y=640)], sfx=[(d * 0.45, "ding", -20)])


@v.plano(49, "¿cuánto?: micro plano, zoom al borde")
def _(d):
    return P(NEG, [BG("bg_estudio"), IMG("espejo_corte", ancho=980, x=540, y=1100, z=0.5), senala(110, 960, 0.0, d, 90, "#ff3d3d")],
             cam(1.6, 2.3, (200, 1000), (130, 970)), "corte", sfx=[(0.02, "pop", -20)])


@v.plano(50, "dos milésimas de milímetro: la cifra")
def _(d):
    return P(NEG, [BG("bg_estudio"), IMG("regla", ancho=900, x=540, y=1250, z=0.5, keys=aparece(0.0, 0.2)), flecha([[540, 1100], [540, 1190]], 0.2, 0.5, "#ff3d3d", 10, z=0.6),
                   polvo("#7df9ff", 30, (100, 700, 980, 1500), 6)],
             cam(1.0, 1.1, (540, 1100)), "corte", hud=[rotulo(0.05, d - 0.03, "0,002 mm", tam=150, color="#141414", capsula="#ffd23fe6", y=900)], sfx=[(0.05, "impacto", -18)])


@v.plano(54, "cincuenta veces menos que el grosor de un pelo: el pelo enorme y la rayita")
def _(d):
    return P(NEG, [BG("bg_estudio"), IMG("pelo", ancho=1200, x=540, y=1000, z=0.5, keys=va((1500, 1000), (540, 1000), d, "salida") + []),
                   flecha([[120, 1330], [960, 1330]], d * 0.35, d * 0.6, "#ff3d3d", 6, punta=False, z=0.6),
                   flecha([[820, 1480], [820, 1360]], d * 0.55, d * 0.75, "#ffffff", 7, z=0.6)],
             cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[rotulo(0.3, d - 0.03, "UN PELO", tam=84, color="#141414", capsula="#ffd27ae6", y=760),
                  rotulo(d * 0.45, d - 0.03, "50 VECES MENOS", tam=84, color="#ffffff", capsula="#c0392be6", y=1290)], sfx=[(0.1, "roce", -20), (d * 0.6, "ding", -18)])


@v.plano(63, "la causa: una pieza del aparato de medir: el aparato entra")
def _(d):
    return P(NEG, [BG("bg_lab"), brillo(540, 1100, 500, "#7dff3a", 0.25, 0.06), IMG("aparato_medir", ancho=520, x=540, y=1100, z=0.5, keys=arranque(540, 1100, d, "arriba", 300, 20)),
                   IMG("espejo_hubble", ancho=260, x=880, y=1560, z=0.45, keys=aparece(0.3))],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[rotulo(0.3, d - 0.03, "EL APARATO DE MEDIR", tam=70, color="#141414", capsula="#7dff3ae6", y=600)], sfx=[(0.05, "whoosh", -22), (0.4, "pop", -20)])


@v.plano(71, "estaba un milímetro fuera de su sitio: la lente se descoloca y se pone roja")
def _(d):
    return P(NEG, [BG("bg_lab"), *cruza(IMG("aparato_medir", ancho=520, x=540, y=1100, z=0.5), IMG("aparato_mal", ancho=520, x=540, y=1100, z=0.5), 0.25, 0.2),
                   senala(540, 1128, 0.5, d - 0.03, 130, "#ff3d3d")],
             cam(1.1, 1.5, (540, 1100), (540, 1120)), "corte", hud=[rotulo(0.5, d - 0.03, "1 mm", tam=140, color="#ffffff", capsula="#c0392be6", y=640)], sfx=[(0.25, "zap", -16)])


@v.plano(78, "cambiar el espejo en órbita era imposible: el espejo junto al Hubble, tachado")
def _(d):
    return P(NEG, [BG("bg_amanecer_orbital"), *hub(330, 1180, 440, p1=(300, 1140), d=d), IMG("espejo_hubble", ancho=420, x=790, y=1050, z=0.5, keys=late(0.2, 1, 0.05)),
                   *tacha(790, 1040, d * 0.5, 200)],
             cam(1.0, 1.06, (540, 1080)), "corte", hud=[rotulo(d * 0.55, d - 0.03, "IMPOSIBLE", tam=110, color="#ffffff", capsula="#c0392be6", y=640)], sfx=[(d * 0.5, "zap", -18)])


@v.plano(85, "así que le hicieron gafas: las gafas caen sobre el Hubble (revelación)")
def _(d):
    t = min(0.75, d * 0.5)
    return P(NEG, [BG("bg_esp_ambar"), estrellas(50, 9), brillo(540, 900, 600, "#ffd23f", 0.4, 0.06, keys=[{"t": 0, "op": 0}, {"t": t, "op": 0}, {"t": t + 0.1, "op": 1}]),
                   IMG("hubble", ancho=640, x=540, y=1150, z=0.5, keys=[{"t": 0, "escala": 1.0}, {"t": t, "escala": 1.0}, {"t": t + 0.12, "escala": 1.07, "ease": "golpe"}, {"t": d, "escala": 1.02, "ease": "suave"}]),
                   IMG("gafas", ancho=400, x=540, y=893, z=0.55, keys=[{"t": 0, "y": 200, "rot": -25, "op": 1}, {"t": t, "y": 893, "rot": 0, "ease": "bote"}])],
             cam(1.0, 1.12, (540, 1050)), "corte", hud=[rotulo(t + 0.05, d - 0.03, "¡GAFAS!", tam=140, color="#141414", capsula="#ffd23fe6", y=620)],
             sfx=[(0.0, "subida", -20, {"dur": t}), (t, "impacto", -12)], energia=0.9)


@v.plano(90, "en diciembre de 1993: amanecer orbital, el año corre")
def _(d):
    return P(NEG, [BG("bg_amanecer_orbital"), fugaz(0.2, 150, 520, 620, 700), IMG("transbordador", ancho=200, x=540, y=1500, z=0.5, keys=va((540, 1560), (540, 1380), d))],
             cam(1.0, 1.06, (540, 1100)), "desenfoque",
             hud=[rotulo(0.05, d - 0.03, "DICIEMBRE", tam=84, color="#ffffff", capsula="#2a5ae8e6", y=640),
                  contador(0.05, d - 0.03, 1990, 1993, min(0.8, d * 0.5), miles=False, tam=170, color="#141414", capsula="#ffd23fe6", y=860)], sfx=[(0.1, "tic", -20)])


@v.plano(98, "siete astronautas: aparecen uno a uno")
def _(d):
    ps = [(210, 1020), (430, 1020), (650, 1020), (870, 1020), (320, 1330), (540, 1330), (760, 1330)]
    return P(NEG, [BG("bg_esp_petroleo"), estrellas(40, 2),
                   *[IMG("astro_c1" if i % 2 else "astro_c0", ancho=200, x=x, y=y, z=0.5, keys=aparece(0.02 + i * d * 0.09, 0.18)) for i, (x, y) in enumerate(ps)]],
             cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[contador(0.03, d - 0.03, 1, 7, d * 0.65, "", tam=150, color="#141414", capsula="#7df9ffe6", y=640)], sfx=[(0.05, "pop", -20), (d * 0.3, "pop", -20), (d * 0.6, "pop", -20)])


@v.plano(100, "subieron en un transbordador: despega con fuego y temblor")
def _(d):
    return P(NEG, [BG("bg_esp_petroleo"), estrellas(40, 2), IMG("tierra_arco", ancho=1500, x=540, y=1800, z=0.3),
                   IMG("transbordador", ancho=440, x=540, y=1150, z=0.5, keys=[{"t": 0, "y": 1500}, {"t": d, "y": 760, "ease": "entrada"}]),
                   brillo(540, 1500, 400, "#ffb02a", 0.6, 0.4, keys=[{"t": 0, "y": 1850}, {"t": d, "y": 1110, "ease": "entrada"}])],
             cam(1.0, 1.08, (540, 1100), temblor=7), "corte", sfx=[(0.0, "rumor", -14, {"dur": d})])


@v.plano(104, "hicieron cinco paseos espaciales: el astronauta flota junto al Hubble, la cuenta corre")
def _(d):
    return P(NEG, [BG("bg_amanecer_orbital"), *hub(340, 1150, 500, p1=(320, 1120), d=d),
                   IMG("astro_c0", ancho=230, x=800, y=1050, z=0.6, keys=flota(d, 26, x=800, y=1050, periodo=1.2)),
                   flecha([[700, 1080], [470, 1110]], 0.2, 0.7, "#ffffffcc", 5, punta=False, z=0.55)],
             cam(1.0, 1.06, (540, 1080)), "corte",
             hud=[contador(0.05, d - 0.03, 1, 5, d * 0.6, " PASEOS", tam=100, color="#141414", capsula="#7dff3ae6", y=640)], sfx=[(0.1, "senal", -24)])


@v.plano(108, "y le colocaron unos espejitos: el espejito viaja hasta dentro del Hubble")
def _(d):
    return P(NEG, [BG("bg_amanecer_orbital"), *hub(330, 1150, 520),
                   IMG("espejito", ancho=220, x=800, y=1000, z=0.6, keys=[{"t": 0, "x": 900, "y": 1400, "rot": 20, "escala": 1.0}, {"t": d * 0.85, "x": 360, "y": 1080, "rot": 0, "escala": 0.45, "ease": "suave"}]),
                   flecha([[860, 1340], [470, 1110]], 0.0, d * 0.7, LIMA, 8, disc=[24, 16], z=0.45)],
             cam(1.0, 1.1, (540, 1100), (420, 1100)), "corte", hud=[rotulo(0.2, d - 0.03, "ESPEJITOS", tam=96, color="#141414", capsula="#7dff3ae6", y=640)], sfx=[(d * 0.85, "ding", -16)])


@v.plano(113, "del tamaño de una moneda: el espejito y la moneda, igual de grandes")
def _(d):
    return P(NEG, [BG("bg_estudio"), IMG("espejito", ancho=380, x=320, y=1130, z=0.5, keys=aparece(0.0, 0.25)),
                   IMG("moneda_antigua", ancho=330, x=780, y=1030, z=0.5, keys=[{"t": 0, "y": 500, "rot": -120}, {"t": 0.45, "y": 1030, "rot": 0, "ease": "bote"}]),
                   flecha([[160, 800], [480, 800]], 0.4, 0.7, AMBAR, 7, punta=False, z=0.6), flecha([[620, 800], [940, 800]], 0.4, 0.7, AMBAR, 7, punta=False, z=0.6)],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[rotulo(0.15, d - 0.03, "UNA MONEDA", tam=90, color="#141414", capsula="#ffd23fe6", y=1300)], sfx=[(0.4, "ding", -18)])


@v.plano(118, "con el error contrario: la curva y su contraria se juntan")
def _(d):
    return P(NEG, [BG("bg_estudio"), IMG("espejo_corte", ancho=760, x=540, y=880, z=0.5, keys=va((540, 760), (540, 930), d * 0.6)),
                   IMG("espejo_corte", ancho=760, x=540, y=1400, z=0.5, rot=180, keys=va((540, 1560), (540, 1330), d * 0.6)),
                   brillo(540, 1130, 420, "#7dff3a", 0.5, 0.4, keys=[{"t": 0, "op": 0}, {"t": d * 0.6, "op": 0}, {"t": d * 0.7, "op": 1}])],
             cam(1.0, 1.05, (540, 1130)), "corte", hud=[rotulo(0.05, d - 0.03, "ERROR CONTRARIO", tam=76, color="#141414", capsula="#7dff3ae6", y=600)], sfx=[(d * 0.6, "ding", -16)])


@v.plano(122, "semanas después llegó la primera foto nueva: la foto llega, todavía sin verse")
def _(d):
    return P(NEG, [BG("bg_estudio"), IMG("foto_borrosa", ancho=760, x=540, y=1100, z=0.5, keys=[{"t": 0, "y": 2300, "rot": 10}, {"t": d * 0.7, "y": 1100, "rot": -2, "ease": "salida"}])],
             cam(1.0, 1.06, (540, 1100)), "corte", sfx=[(0.0, "subida", -20, {"dur": d})])


@v.plano(129, "nítida: la foto se enfoca de golpe")
def _(d):
    return P(NEG, [BG("bg_estudio"), brillo(540, 1100, 700, "#ffffff", 0.5, 0.06, pulso=[0.2, 0.5]),
                   *cruza(IMG("foto_borrosa", ancho=760, x=540, y=1100, z=0.5), IMG("foto_nitida", ancho=800, x=540, y=1100, z=0.5), 0.02, 0.12),
                   fundido_blanco([{"t": 0, "op": 0.7}, {"t": 0.25, "op": 0}])],
             cam(1.0, 1.1, (540, 1100)), "corte", hud=[rotulo(0.02, d - 0.02, "NÍTIDA", tam=140, color="#141414", capsula="#7dff3ae6", y=600)], sfx=[(0.0, "impacto", -12), (0.15, "brillo", -16)], energia=0.9)


@v.plano(130, "desde entonces, el Hubble: con gafas, dispara fotos (destellos)")
def _(d):
    return P(NEG, [BG("bg_esp_violeta"), estrellas(40, 3), sat(d, SAT2, SAT3, (1200, 620), (-120, 900)), *hub(540, 1150, 560, gaf=True, p1=(540, 1110), d=d),
                   brillo(540, 800, 380, "#ffffff", 0.7, 0.6, pulso=[0.5, 0.35]), IMG("foto_nitida", ancho=200, x=860, y=780, z=0.6, keys=aparece(d * 0.4, 0.2)),
                   IMG("foto_nitida", ancho=200, x=210, y=860, z=0.6, rot=-8, keys=aparece(d * 0.65, 0.2))],
             cam(1.0, 1.06, (540, 1050)), "corte", sfx=[(d * 0.4, "pop", -20), (d * 0.65, "pop", -20)])


@v.plano(134, "ha hecho más de un millón y medio de observaciones: las fotos llenan la pantalla")
def _(d):
    pos = [(200, 760), (540, 760), (880, 760), (200, 1120), (880, 1120), (200, 1480), (540, 1480), (880, 1480)]
    return P(NEG, [BG("bg_esp_violeta"), estrellas(40, 3), sat(d, SAT2, SAT3, (1200, 620), (-120, 900)),
                   *[IMG("foto_nitida", ancho=300, x=x, y=y, z=0.5, rot=(-6 + i * 3) % 9 - 4, keys=aparece(i * d * 0.06, 0.18)) for i, (x, y) in enumerate(pos)]],
             cam(1.0, 1.06, (540, 1100)), "corte",
             hud=[contador(0.15, d - 0.03, 0, 1500000, d * 0.55, "", tam=110, color="#141414", capsula="#ffd23fe6", y=1120)],
             sfx=[(0.05 + i * d * 0.14, "pop", -22) for i in range(4)])


@v.plano(144, "y sigue ahí arriba: el Hubble con gafas cruza sobre la Tierra")
def _(d):
    return P(NEG, [BG("bg_esp_petroleo"), estrellas(50, 6), sat(d, SAT2, SAT3, (1200, 620), (-120, 900)), IMG("tierra_arco", ancho=1600, x=540, y=1750, z=0.3, keys=va((600, 1750), (480, 1750), d)),
                   *hub(300, 1150, 440, gaf=True, p1=(760, 1020), d=d, ease="lineal"), fugaz(0.3, 700, 560, 1000, 700)],
             cam(1.0, 1.05, (540, 1100)), "corte", sfx=[(0.1, "senal", -24)])


@v.plano(148, "¿tú también llevas gafas?: las gafas, enormes, laten")
def _(d):
    return P(NEG, [BG("bg_estudio"), brillo(540, 1080, 520, "#ff4d5e", 0.3, 0.06), sat(d, SAT2, SAT3, (1200, 620), (-120, 900)),
                   IMG("gafas", ancho=860, x=540, y=1080, z=0.5, keys=late(0.15, 2, 0.08, 0.45))],
             cam(1.0, 1.08, (540, 1080)), "corte", hud=[rotulo(0.2, d - 0.03, "¿Y TÚ?", tam=130, color="#141414", capsula="#ffd23fe6", y=640)], sfx=[(0.15, "pop", -18)])


@v.plano(152, "ya tienes algo en común con él: vuelve el Hubble del principio, ahora con gafas (bucle)")
def _(d):
    return P(NEG, [BG("bg_esp_violeta"), estrellas(50, 4), IMG("estrella_nitida", ancho=620, x=560, y=760, z=0.2, keys=late(0.3, 3, 0.08, 0.6)),
                   *hub(540, 1100, 640, gaf=True, p1=(540, 1060), d=d)],
             cam(1.0, 1.06, (540, 1000)), "corte", sfx=[(0.1, "brillo", -20)])


v.construir("2026-11-25-manana-01-hubble-miope", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 251, "db": -13},
            claves=["miope", "Hubble", "borroso", "dólares", "desastre", "manchas", "espejo", "plano", "milésimas", "pelo", "aparato",
                    "imposible", "gafas", "astronautas", "transbordador", "espejitos", "moneda", "contrario", "Nítida", "observaciones"])
