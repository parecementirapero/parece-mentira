"""03 · ¿Ves la Vía Láctea? (contaminación lumínica, atlas de 2016) — método denso, estilo del vídeo largo.
Experimento del lote: gancho de pregunta. Lote 2026-11-25-tarde (Jorge, con el agente).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comun_1125t as C  # noqa: E402
from comun_1125t import *  # noqa: E402,F401,F403
import ilus_1125t  # noqa: E402

SVG = ilus_1125t.generar(os.path.join(sys.argv[1], "_svg_lote"))
C.SVG_DIR = SVG
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
VL = ["#02030a", "#14204a"]
NAR = ["#4a2e3a", "#1a1218"]
CIU = ["#141a3e", "#0c0c14"]
S_V, S_N, S_C = SUELO["bg_via_lactea"], SUELO["bg_cielo_naranja"], SUELO["bg_ciudad"]


def via(d, z0=1.0, z1=1.12, foco=(540, 640)):
    return BG("bg_via_lactea"), cam(z0, z1, foco)


@v.plano(0, "gancho: la Vía Láctea enorme cruza el cielo y cae una estrella fugaz")
def _(d):
    return P(VL, [BG("bg_via_lactea"), fugaz(0.3, 900, 200, 400, 700), polvo("#ffffff", 50, (0, 0, 1080, 1300), 7, "estrellas")],
             cam(1.0, 1.2, (540, 700), (540, 600)), vineta=0.35, sfx=[(0.05, "brillo", -18)])


@v.plano(4, "seguramente no: la misma chica, en la ciudad, mira un cielo naranja sin estrellas")
def _(d):
    return P(NAR, [BG("bg_cielo_naranja"), PZ("mira_arriba_b", 540, S_N, 900, keys=[{"t": 0, "x": 520}, {"t": d, "x": 560, "ease": "suave"}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.1, d - 0.05, "NO", "#ffffff", "#c0392be6", 150)], sfx=[(0.1, "zap", -18)])


@v.plano(6, "en dos mil dieciséis: la Tierra de noche gira")
def _(d):
    return P(ESP, [estrellas(80, 2), OB("tierra_noche", 540, 1050, 820, keys=[{"t": 0, "rot": -6}, {"t": d, "rot": 4}] + aparece(0.0))],
             cam(1.0, 1.05, (540, 1000)), "desenfoque",
             hud=[contador(0.05, d - 0.05, 2000, 2016, 0.5, miles=False, tam=160, color="#141414", capsula="#ffffffe6", y=560)], sfx=[(0.1, "tic", -18)])


@v.plano(10, "un equipo de científicos hizo el primer gran atlas del brillo del cielo nocturno: zoom a las luces")
def _(d):
    return P(ESP, [estrellas(80, 3), OB("tierra_noche", 540, 1050, 820, keys=[{"t": 0, "rot": 4}, {"t": d, "rot": 10}])],
             cam(1.0, 1.4, (540, 1050), (600, 900)), "corte", hud=[cap(0.4, d - 0.05, "ATLAS DEL CIELO NOCTURNO", "#141414", "#7df9ffe6", 70)], sfx=[(0.2, "subida", -22, {"dur": 1.2})])


@v.plano(24, "con datos de satélite: el satélite cruza por encima de la Tierra")
def _(d):
    return P(ESP, [estrellas(80, 4), OB("tierra_noche", 540, 1450, 1100, z=0.4, keys=[{"t": 0, "rot": 10}, {"t": d, "rot": 14}]),
                   OB("satelite_obs", 540, 760, 520, z=0.6, keys=[{"t": 0, "x": 150, "rot": -8}, {"t": d, "x": 930, "rot": 6, "ease": "lineal"}])],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.3, d - 0.05, "DATOS DE SATÉLITE", tam=90)], sfx=[(0.1, "senal", -20)])


@v.plano(28, "y la conclusión fue tremenda: la cara de sorpresa")
def _(d):
    return P(VL, [BG("bg_via_lactea"), OB("cara_mira_estrellas", 540, 1150, 960, keys=[{"t": 0, "escala": 1.08}, {"t": 0.4, "escala": 1.0, "ease": "golpe"}])],
             cam(1.0, 1.05, (540, 1000)), "corte", sfx=[(0.05, "impacto", -16)])


@v.plano(33, "un tercio de la humanidad ya no puede verla: tres personas, una se apaga")
def _(d):
    xs = (260, 540, 820)
    ps = ("voluntario_1", "voluntario_2", "voluntario_5")
    els = [BG("bg_cielo_naranja")]
    for i, (p, x) in enumerate(zip(ps, xs)):
        els.append(PZ(p, x, S_N, 760, keys=aparece(0.08 * i) + ([{"t": 1.0, "op": 1}, {"t": 1.4, "op": 0.35}] if i == 2 else [])))
    els += tacha(820, 1050, 1.2, 160)
    return P(NAR, els, cam(1.0, 1.04, (540, 1100)), "corte", hud=[cap(0.4, d - 0.05, "1 DE CADA 3", "#ffffff", "#c0392be6", 120)], sfx=[(1.2, "zap", -18)])


@v.plano(45, "en Europa, el sesenta por ciento de la gente")
def _(d):
    return P(NAR, [BG("bg_cielo_naranja")] + gente(10, 6, 0.3, 1130, 175, "#ff9a50"), cam(1.0, 1.04, (540, 1100)), "corte",
             hud=[cap(0.05, d - 0.05, "EUROPA", "#141414", "#ffd23fe6", 100, y=520),
                  contador(0.3, d - 0.05, 0, 60, 0.8, " %", tam=120, color="#ffffff", capsula="#c0392be6", y=1560)], sfx=[(0.3, "subida", -22, {"dur": 0.8})])


@v.plano(54, "en Norteamérica, el ochenta")
def _(d):
    return P(NAR, [BG("bg_cielo_naranja")] + gente(10, 8, 0.2, 1130, 175, "#ff9a50"), cam(1.0, 1.04, (540, 1100)), "corte",
             hud=[cap(0.05, d - 0.05, "NORTEAMÉRICA", "#141414", "#ffd23fe6", 90, y=520),
                  contador(0.2, d - 0.05, 0, 80, 0.8, " %", tam=120, color="#ffffff", capsula="#c0392be6", y=1560)], sfx=[(0.2, "subida", -22, {"dur": 0.8})])


@v.plano(58, "¿qué la tapa?: la Vía Láctea se apaga bajo un velo naranja")
def _(d):
    return P(VL, [BG("bg_via_lactea"), {**BG("bg_cielo_naranja", z=0.06), "keys": [{"t": 0, "op": 0}, {"t": d, "op": 0.85, "ease": "suave"}]}],
             cam(1.0, 1.06, (540, 900)), "corte", hud=[amarillo(0.05, d - 0.03, "¿QUÉ LA TAPA?", y=560, tam=110, color=AMBAR)], sfx=[(0.05, "whoosh", -20)])


@v.plano(61, "la luz de nuestras ciudades: la ciudad iluminada")
def _(d):
    return P(CIU, [BG("bg_ciudad"), PZ("adulto_camina", 540, S_C, 900, keys=[{"t": 0, "x": 300}, {"t": d, "x": 600, "ease": "lineal"}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[cap(0.3, d - 0.05, "LA LUZ DE LAS CIUDADES", tam=80)], sfx=[(0.1, "rumor", -24, {"dur": d})])


@v.plano(66, "las farolas: una farola enorme se enciende")
def _(d):
    return P(CIU, [BG("bg_ciudad"), OB("farola", 700, 1000, 460, keys=[{"t": 0, "op": 0.5}, {"t": 0.2, "op": 1}]), brillo(780, 420, 260, "#ffc070", 0.6, 0.44, pulso=[0.1, 0.4])],
             cam(1.1, 1.18, (700, 800)), "corte", hud=[cap(0.05, d - 0.05, "FAROLAS", tam=110)], sfx=[(0.1, "zap", -20)])


@v.plano(68, "los carteles y las ventanas: los edificios se encienden")
def _(d):
    return P(CIU, [BG("bg_ciudad"), polvo("#ffd38a", 70, (0, 500, 1080, 1200), 9)], cam(1.2, 1.35, (540, 800)), "corte",
             hud=[cap(0.05, d - 0.05, "CARTELES Y VENTANAS", tam=80)], sfx=[(0.1, "pop", -22)])


@v.plano(73, "iluminan el polvo y la humedad del aire: partículas que brillan bajo la farola")
def _(d):
    return P(CIU, [BG("bg_ciudad"), OB("farola", 700, 1000, 460), polvo("#ffc070", 120, (300, 200, 1080, 1100), 11), brillo(780, 420, 420, "#ffb050", 0.5, 0.44)],
             cam(1.1, 1.3, (700, 600)), "corte", hud=[cap(0.3, d - 0.05, "POLVO Y HUMEDAD", tam=90)], sfx=[(0.2, "brillo", -22)])


@v.plano(81, "y el cielo se queda de un gris anaranjado, como un velo por encima de las estrellas")
def _(d):
    return P(NAR, [BG("bg_cielo_naranja"), polvo("#ffffff", 40, (0, 0, 1080, 600), 13, "estrellas"),
                   {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 1300, "relleno": "#e08a4a", "x": 540, "y": 450, "z": 0.3,
                    "keys": [{"t": 0, "op": 0}, {"t": d * 0.8, "op": 0.45, "ease": "suave"}]}],
             cam(1.0, 1.08, (540, 800)), "corte", hud=[cap(0.4, d - 0.05, "UN VELO NARANJA", tam=100)], sfx=[(0.1, "subida", -24, {"dur": d * 0.8})])


@v.plano(98, "más de ocho de cada diez personas viven bajo un cielo con contaminación lumínica: la Tierra brilla")
def _(d):
    return P(ESP, [estrellas(70, 5), OB("tierra_noche", 540, 1050, 860, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 8}]), brillo(560, 900, 520, "#ffb050", 0.35, 0.45, pulso=[0.3, 0.6])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[cap(0.3, d - 0.05, "8 DE CADA 10", "#ffffff", "#c0392be6", 120)], sfx=[(0.3, "ding", -20)])


@v.plano(114, "y la Vía Láctea es nuestra propia galaxia: vuelve el cielo oscuro")
def _(d):
    return P(VL, [BG("bg_via_lactea"), polvo("#ffffff", 60, (0, 0, 1080, 1300), 17, "estrellas")], cam(1.0, 1.15, (540, 700)), "desenfoque",
             hud=[cap(0.4, d - 0.05, "NUESTRA GALAXIA", "#141414", "#7df9ffe6", 100)], sfx=[(0.2, "brillo", -18)])


@v.plano(122, "cientos de miles de millones de estrellas: zoom al núcleo")
def _(d):
    return P(VL, [BG("bg_via_lactea"), polvo("#fff1c8", 120, (200, 200, 900, 1100), 19, "estrellas")], cam(1.4, 2.0, (540, 640)), "corte",
             hud=[cap(0.2, d - 0.05, "100.000 MILLONES O MÁS", tam=76)], sfx=[(0.1, "subida", -22, {"dur": 1.4})])


@v.plano(129, "y muchos solo la han visto en fotos: la chica mira la galaxia en el teléfono")
def _(d):
    return P(CIU, [BG("bg_ciudad"), PZ("adulto_camina", 420, S_C, 1000), OB("telefono_movil_b", 800, 1000, 280, z=0.6, keys=aparece(0.2))],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[cap(0.4, d - 0.05, "SOLO EN FOTOS", tam=100)], sfx=[(0.2, "pop", -20)])


@v.plano(137, "para verla, aléjate de las ciudades en una noche sin luna: la chica llega al campo oscuro")
def _(d):
    return P(VL, [BG("bg_via_lactea"), PZ("mira_arriba", 540, S_V, 900, keys=[{"t": 0, "x": 200}, {"t": d * 0.7, "x": 520, "ease": "salida"}, {"t": d, "x": 540}])],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[cap(0.4, d - 0.05, "SIN LUNA, LEJOS DE LA CIUDAD", tam=66)], sfx=[(0.1, "roce", -22)])


@v.plano(148, "¿tú la has visto alguna vez?: la chica mira arriba bajo la Vía Láctea (bucle)")
def _(d):
    return P(VL, [BG("bg_via_lactea"), PZ("mira_arriba", 540, S_V, 900), fugaz(0.4, 200, 300, 600, 600)], cam(1.0, 1.12, (540, 900), (540, 700)), "corte",
             sfx=[(0.4, "brillo", -20)])


v.construir("2026-11-25-tarde-03-via-lactea", version=1, bucle=0.35, musica={"generar": "misterio", "semilla": 1253, "db": -13},
            claves=["Vía", "Láctea", "atlas", "satélite", "tercio", "humanidad", "Europa", "sesenta", "Norteamérica", "ochenta", "luz", "ciudades",
                    "farolas", "carteles", "ventanas", "polvo", "humedad", "anaranjado", "velo", "contaminación", "lumínica", "galaxia", "luna"],
            ep_extra={"sfx_bajo_voz": True})
