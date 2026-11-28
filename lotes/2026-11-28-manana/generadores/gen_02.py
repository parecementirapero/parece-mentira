"""02 · Despiertas y está nevando (la nevada de Ciudad de México de 1967) — método denso, estilo del vídeo largo.
Lote 2026-11-28-manana (Agente 08:00 (Nico)). Experimento del lote: gancho en segunda persona tipo POV.
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comun_1128m as C  # noqa: E402
from comun_1128m import *  # noqa: E402,F401,F403
import ilus_1128m  # noqa: E402

SVG = ilus_1128m.generar(os.path.join(sys.argv[1], "_svg_lote"))
C.SVG_DIR = SVG
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
NOCHE = ["#0a0e22", "#3a4868"]
INV = ["#1a2236", "#0a0e1a"]
SEPIA = ["#2a2218", "#14100c"]
CIAN, LIMA = "#2ff3ff", "#5dff8a"
S = SUELO["bg_reforma_nieve"]


def nieve(n=90, sem=1):
    return polvo("#ffffff", n, (0, 0, 1080, 1800), sem)


def calle(extra=(), sem=1, columna=True, cx=540, alto=1250):
    els = [BG("bg_reforma_nieve"), nieve(90, sem)]
    if columna:
        els.append(OB("columna_angel", cx, S - alto / 2 + 40, alto * 420 / 1700, z=0.3))
    return els + list(extra)


@v.plano(0, "gancho: la columna del ángel de noche, nevando; un copo grande cae delante")
def _(d):
    return P(NOCHE, calle([OB("copo_nieve", 830, 700, 260, z=0.8, keys=[{"t": 0, "y": 560, "rot": 0}, {"t": 0.6, "y": 760, "rot": 40, "ease": "lineal"}, {"t": d, "y": 1150, "rot": 120}]),
                           OB("nieve_suelo", 540, 1700, 1200, z=0.7)], 1, alto=1150),
             cam(1.0, 1.08, (540, 900)), vineta=0.35, sfx=[(0.0, "whoosh", -16), (0.4, "brillo", -20)])


@v.plano(4, "estás en Ciudad de México: la cámara baja por la avenida nevada")
def _(d):
    return P(NOCHE, calle([OB("nieve_suelo", 540, 1700, 1200, z=0.7)], 2), cam(1.1, 1.1, (540, 600), (540, 1300)), "corte",
             hud=[cap(0.2, d - 0.05, "CIUDAD DE MÉXICO", "#ffffff", "#c0392be6", 92, y=900)], sfx=[(0.1, "whoosh", -20)])


@v.plano(9, "once de enero de mil novecientos sesenta y siete: el año corre en el contador")
def _(d):
    return P(SEPIA, [BG("bg_ventana_invierno"), polvo("#ffffff", 40, (180, 300, 900, 1100), 5), OB("foto_1967", 540, 1150, 560, z=0.5, keys=aparece(0.0) + [{"t": 0, "rot": -6}, {"t": d, "rot": -2}])],
             cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[cap(0.05, d - 0.05, "11 DE ENERO", "#ffffff", "#2a5ae8e6", 90, y=520), cap(0.4, d - 0.05, "1967", "#141414", "#ffd23fe6", 140, y=700)],
             sfx=[(0.4, "impacto", -20)])


@v.plano(18, "¿nieve, aquí?: cara de sorpresa de un chico")
def _(d):
    return P(INV, [BG("bg_reforma_nieve"), nieve(60, 3), OB("cara_nino67", 540, 1200, 900, z=0.5, keys=aparece(0.0))],
             cam(1.05, 1.12, (540, 1100)), "corte", hud=[amarillo(0.1, d - 0.05, "¿NIEVE, AQUÍ?", y=560, tam=120, color=CIAN)], sfx=[(0.1, "pop", -18)])


@v.plano(20, "una masa de aire polar baja desde el norte: grandes flechas heladas sobre las montañas")
def _(d):
    return P(INV, [BG("bg_alpes_nieve"), nieve(50, 4),
                   flecha([[200, 300], [300, 700], [380, 1050]], 0.1, 0.8, CIAN, 16, z=0.6),
                   flecha([[600, 260], [620, 700], [620, 1080]], 0.3, 1.0, CIAN, 16, z=0.6),
                   flecha([[950, 320], [860, 720], [820, 1050]], 0.5, 1.2, CIAN, 16, z=0.6)],
             cam(1.0, 1.05, (540, 900)), "corte", hud=[cap(0.2, d - 0.02, "AIRE POLAR", "#141414", "#7df9ffe6", 110, y=1300)], sfx=[(0.1, "whoosh", -16)])


@v.plano(25, "lleva dos días blanqueando el norte del país: el paisaje se cubre")
def _(d):
    return P(INV, [BG("bg_alpes_nieve"), nieve(120, 6), OB("nieve_suelo", 540, 1600, 1300, z=0.6, keys=[{"t": 0, "y": 1900}, {"t": min(1.5, d * 0.7), "y": 1600, "ease": "salida"}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[cap(0.3, d - 0.05, "2 DÍAS", "#ffffff", "#2a5ae8e6", 120, y=700)], sfx=[(0.3, "roce", -20)])


@v.plano(33, "y a las dos de la madrugada: el reloj marca las dos detrás de una ventana de noche")
def _(d):
    return P(NOCHE, [BG("bg_ventana_invierno"), nieve(40, 7)] + reloj(540, 1250, 420, 1, 58, 2, 0, 0.1, min(1.0, d * 0.6)),
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[cap(0.3, d - 0.05, "2:00", "#141414", "#ffd23fe6", 120, y=640)], sfx=[(0.1, "tic", -18)])


@v.plano(40, "empieza a nevar en el Paseo de la Reforma: la avenida, nieve que se espesa")
def _(d):
    return P(NOCHE, calle([nieve(140, 8), OB("farola", 160, 1250, 140, z=0.5), OB("farola", 920, 1250, 140, z=0.5)], 9, alto=1300),
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.3, d - 0.05, "REFORMA", "#ffffff", "#c0392be6", 110, y=1350)], sfx=[(0.1, "brillo", -22)])


@v.plano(49, "cuatro grados bajo cero: el termómetro se hunde")
def _(d):
    return P(INV, [BG("bg_reforma_nieve"), nieve(60, 10), OB("termo_frio", 540, 1100, 300, keys=aparece(0.0))],
             cam(1.0, 1.06, (540, 1100)), "corte",
             hud=[contador(0.1, d - 0.05, 0, -4, 0.7, " °C", tam=150, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(0.1, "tic", -18)])


@v.plano(53, "la capital amanece blanca: la nieve del suelo sube y llega la luz del día")
def _(d):
    return P(["#8aa4c8", "#e8f0fa"], calle([OB("nieve_suelo", 540, 1650, 1300, z=0.7, keys=[{"t": 0, "y": 1900}, {"t": min(1.2, d * 0.6), "y": 1650, "ease": "salida"}]),
                                          brillo(540, 600, 700, "#ffe8c0", 0.4, 0.15, keys=[{"t": 0, "op": 0}, {"t": d, "op": 0.7}])], 11),
             cam(1.0, 1.05, (540, 1000)), "desenfoque", hud=[amarillo(0.3, d - 0.05, "BLANCA", y=560, tam=140, color="#ffffff")], sfx=[(0.1, "subida", -22)])


@v.plano(57, "unos cinco centímetros: una regla clavada en la nieve")
def _(d):
    return P(INV, [BG("bg_reforma_nieve"), nieve(50, 12), OB("regla", 540, 1250, 220, z=0.5, keys=[{"t": 0, "rot": 90}] + aparece(0.0)),
                   OB("nieve_suelo", 540, 1560, 1300, z=0.6)],
             cam(1.15, 1.2, (540, 1300)), "corte",
             hud=[contador(0.1, d - 0.05, 0, 5, 0.6, " CM", tam=140, color="#141414", capsula="#ffd23fe6", y=640)], sfx=[(0.1, "tic", -18)])


@v.plano(60, "en San Ángel, en Chapultepec y en el mismísimo Zócalo: los nombres caen uno tras otro")
def _(d):
    t = [0.05, min(0.8, d * 0.3), min(2.0, d * 0.62)]
    return P(NOCHE, calle([OB("nieve_suelo", 540, 1700, 1300, z=0.7)], 13, cx=820, alto=1100),
             cam(1.0, 1.04, (540, 1000)), "corte",
             hud=[cap(t[0], d - 0.05, "SAN ÁNGEL", "#141414", "#ffd23fe6", 92, y=700, x=420), cap(t[1], d - 0.05, "CHAPULTEPEC", "#141414", "#ffd23fe6", 92, y=850, x=420),
                  cap(t[2], d - 0.05, "ZÓCALO", "#ffffff", "#c0392be6", 110, y=1010, x=420)], sfx=[(t[0], "pop", -20), (t[1], "pop", -20), (t[2], "impacto", -20)])


@v.plano(70, "los niños salen a jugar: dos chicos junto a un muñeco de nieve")
def _(d):
    return P(["#8aa4c8", "#e8f0fa"], [BG("bg_reforma_nieve"), nieve(60, 14), PZ("muneco_nieve", 760, S + 60, 520, z=0.55, keys=aparece(0.0)),
                                      PZ("nino67", 300, S + 80, 560, z=0.6, keys=aparece(0.15)), PZ("nina67", 520, S + 90, 540, z=0.6, keys=aparece(0.3)),
                                      OB("nieve_suelo", 540, 1760, 1300, z=0.7)],
             cam(1.0, 1.05, (540, 1250)), "corte", hud=[cap(0.4, d - 0.05, "A JUGAR", "#141414", "#ffd23fe6", 110, y=640)], sfx=[(0.15, "pop", -20)])


@v.plano(75, "la gente se lanza bolas de nieve en plena calle: una bola cruza la pantalla")
def _(d):
    return P(["#8aa4c8", "#e8f0fa"], [BG("bg_reforma_nieve"), nieve(60, 15), PZ("nino67", 200, S + 80, 560, z=0.6),
                                      OB("bola_nieve", 260, 1050, 130, z=0.8, keys=lanza(0.15, min(0.9, d * 0.6), (260, 1050), (900, 900))),
                                      PZ("chica_saluda", 880, S + 80, 560, z=0.6), OB("nieve_suelo", 540, 1760, 1300, z=0.7)],
             cam(1.0, 1.05, (540, 1200)), "corte", hud=[cap(0.3, d - 0.05, "¡BOLAS DE NIEVE!", "#ffffff", "#c0392be6", 96, y=640)],
             sfx=[(0.15, "whoosh", -18), (min(0.9, d * 0.6), "golpe", -20)])


@v.plano(85, "y los periódicos llenan la portada: el periódico entra girando")
def _(d):
    return P(SEPIA, [BG("bg_galeria"), OB("periodico", 540, 1050, 900, z=0.5, keys=[{"t": 0, "rot": -200, "ancho": 200}, {"t": min(0.6, d * 0.4), "rot": -4, "ancho": 900, "ease": "salida"}])],
             cam(1.0, 1.05, (540, 1050)), "corte", hud=[cap(0.6, d - 0.05, "PORTADA", "#141414", "#ffd23fe6", 110, y=1500)], sfx=[(0.05, "whoosh", -16), (0.6, "impacto", -22)])


@v.plano(91, "con fotos de Reforma nevada: flash y la foto de 1967")
def _(d):
    return P(SEPIA, [BG("bg_galeria"), OB("camara_flash", 820, 1500, 320, z=0.6, keys=aparece(0.0)),
                     brillo(820, 1400, 400, "#ffffff", 0.9, 0.65, keys=[{"t": 0, "op": 0}, {"t": 0.15, "op": 0}, {"t": 0.2, "op": 0.9}, {"t": 0.45, "op": 0}]),
                     OB("foto_1967", 470, 1000, 640, z=0.5, keys=aparece(0.25) + [{"t": 0, "rot": 4}, {"t": d, "rot": 1}])],
             cam(1.0, 1.05, (540, 1100)), "corte", sfx=[(0.18, "brillo", -16)])


@v.plano(96, "la ciudad está a más de dos mil metros de altura: flecha de altura junto a la ciudad")
def _(d):
    return P(NOCHE, [BG("bg_ciudad"), nieve(50, 16), flecha([[900, 1650], [900, 500]], 0.1, 0.9, LIMA, 12, z=0.7)],
             cam(1.0, 1.04, (540, 1050)), "corte",
             hud=[contador(0.2, d - 0.05, 0, 2000, 1.0, " M", tam=130, color="#141414", capsula="#5dff8ae6", y=760, x=480)], sfx=[(0.1, "subida", -20)])


@v.plano(107, "pero desde que hay registros: el libro de registros se abre")
def _(d):
    return P(SEPIA, [BG("bg_galeria"), OB("libro_abierto", 540, 1150, 760, keys=aparece(0.0) + [{"t": 0, "rot": -3}, {"t": d, "rot": 0}])],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[cap(0.3, d - 0.05, "REGISTROS", "#ffffff", "#2a5ae8e6", 100, y=600)], sfx=[(0.1, "roce", -18)])


@v.plano(112, "solo ha nevado tres veces: un tres enorme")
def _(d):
    return P(INV, [BG("bg_reforma_nieve"), nieve(60, 17), OB("copo_nieve", 540, 1150, 520, z=0.4, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 60}])],
             cam(1.0, 1.08, (540, 1100)), "corte", hud=[amarillo(0.1, d - 0.05, "3 VECES", y=600, tam=150, color=CIAN)], sfx=[(0.1, "impacto", -18)])


def anio(txt, sem, foto=False):
    def fn(d):
        els = [BG("bg_galeria"), polvo("#ffffff", 50, (0, 0, 1080, 1800), sem)]
        els.append(OB("foto_1967" if foto else "copo_nieve", 540, 1150, 560 if foto else 420, z=0.5,
                      keys=aparece(0.0) + ([{"t": 0, "rot": -3}, {"t": d, "rot": 1}] if foto else [{"t": 0, "rot": 0}, {"t": d, "rot": 45}])))
        return P(SEPIA, els, cam(1.0, 1.06, (540, 1100)), "corte", hud=[cap(0.05, d - 0.05, txt, "#141414", "#ffd23fe6", 140, y=600)], sfx=[(0.05, "pop", -18)])
    return fn


v.plano(117, "en mil novecientos siete")(anio("1907", 18))
v.plano(121, "en mil novecientos veinte")(anio("1920", 19))
v.plano(125, "y esa, la de mil novecientos sesenta y siete: la foto")(anio("1967", 20, foto=True))


@v.plano(134, "desde entonces, ni un copo en el centro: el copo se tacha")
def _(d):
    return P(NOCHE, [BG("bg_ciudad"), OB("copo_nieve", 540, 1000, 520, z=0.5, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 30}])] + tacha(540, 1000, min(0.9, d * 0.4), 230),
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.2, d - 0.05, "NI UN COPO", "#ffffff", "#c0392be6", 110, y=1450)], sfx=[(min(0.9, d * 0.4), "impacto", -20)])


@v.plano(142, "casi sesenta años: el contador de años corre")
def _(d):
    return P(SEPIA, [BG("bg_galeria"), OB("foto_1967", 540, 1150, 520, z=0.5, keys=[{"t": 0, "rot": -2, "op": 1}, {"t": d, "rot": 2, "op": 0.6}])],
             cam(1.0, 1.06, (540, 1100)), "corte",
             hud=[contador(0.05, d - 0.05, 0, 59, 0.8, " AÑOS", tam=130, color="#141414", capsula="#ffd23fe6", y=600)], sfx=[(0.05, "tic", -18)])


@v.plano(145, "¿te lo contaron tus abuelos?: la abuela sonríe con la foto")
def _(d):
    return P(SEPIA, [BG("bg_ventana_invierno"), polvo("#ffffff", 40, (180, 300, 900, 1100), 21), OB("cara_abuela", 400, 1250, 820, z=0.5, keys=aparece(0.0)),
                     OB("foto_1967", 820, 1350, 360, z=0.6, keys=aparece(0.3) + [{"t": 0, "rot": 8}, {"t": d, "rot": 4}])],
             cam(1.0, 1.05, (540, 1200)), "corte", hud=[cap(0.2, d - 0.05, "¿TUS ABUELOS?", "#141414", "#ffd23fe6", 100, y=560)], sfx=[(0.05, "ding", -20)])


def micro(fondo, els, txt=None, col="#ffffff", cap_f="#c0392be6", sfx="pop"):
    def fn(d):
        return P(fondo, els(d), cam(1.15, 1.3, (540, 1000)), "corte", hud=[cap(0.0, d - 0.02, txt, col, cap_f, 120)] if txt else [], sfx=[(0.01, sfx, -18)])
    return fn


v.plano(2, "micro: copo enorme")(micro(NOCHE, lambda d: [BG("bg_reforma_nieve"), nieve(80, 22), OB("copo_nieve", 540, 1000, 720, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 30}])], sfx="brillo"))
v.plano(68, "micro: el ángel nevado")(micro(NOCHE, lambda d: [BG("bg_reforma_nieve"), nieve(90, 23), OB("columna_angel", 540, 1750, 640, z=0.3)], sfx="brillo"))
v.plano(103, "micro: 2.000 metros")(micro(NOCHE, lambda d: [BG("bg_ciudad"), nieve(40, 24)], "2.000 M", "#141414", "#5dff8ae6", "impacto"))


v.plano(17, "micro: el calendario de 1967", mas=0.35)(micro(SEPIA, lambda d: [BG("bg_galeria"), OB("calendario_hoja", 540, 1000, 640)], sfx="tic"))
v.plano(32, "micro: la nieve que cubre el norte", mas=0.2)(micro(INV, lambda d: [BG("bg_alpes_nieve"), nieve(160, 25), OB("copo_nieve", 700, 900, 380, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 25}])], sfx="roce"))
v.plano(52, "micro: el bulbo helado", mas=0.2)(micro(INV, lambda d: [BG("bg_reforma_nieve"), OB("termo_frio", 540, 700, 700)], sfx="tic"))
v.plano(84, "micro: bola de nieve en primer plano", mas=0.2)(micro(["#8aa4c8", "#e8f0fa"], lambda d: [BG("bg_reforma_nieve"), OB("bola_nieve", 540, 1000, 700, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 40}])], sfx="golpe"))
v.plano(116, "micro: muñeco de nieve", mas=0.2)(micro(INV, lambda d: [BG("bg_reforma_nieve"), nieve(80, 26), OB("muneco_nieve", 540, 1150, 760)], sfx="pop"))
v.plano(133, "micro: el ángel dorado", mas=0.2)(micro(NOCHE, lambda d: [BG("bg_reforma_nieve"), nieve(90, 27), OB("columna_angel", 540, 1950, 1000, z=0.3)], sfx="brillo"))


v.construir("2026-11-28-manana-02-nevada-1967", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 1282, "db": -13},
            claves=["nevando", "Ciudad", "México", "enero", "sesenta", "siete", "Nieve", "polar", "norte", "madrugada", "Reforma", "Cuatro", "cero",
                    "blanca", "cinco", "centímetros", "Zócalo", "niños", "bolas", "periódicos", "dos", "mil", "metros", "tres", "veces", "copo", "abuelos"],
            ep_extra={"sfx_bajo_voz": True})
