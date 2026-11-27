"""03 · Tu piel cree tener pelo (la piel de gallina) — método denso, estilo del vídeo largo. Lote 2026-11-27-tarde (Agente 20:00 (Jorge)).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comun_1127t as C  # noqa: E402
from comun_1127t import *  # noqa: E402,F401,F403
import ilus_1127t  # noqa: E402

SVG = ilus_1127t.generar(os.path.join(sys.argv[1], "_svg_lote"))
C.SVG_DIR = SVG
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
INV = ["#3a2418", "#120a06"]
CER = ["#0b0f24", "#1b1340"]
CASA = ["#d8dce2", "#8a9098"]
CUEVA = ["#2a1e16", "#0a0806"]
CIAN, LIMA = "#2ff3ff", "#5dff8a"
S_O = SUELO["bg_oficina_gris"]


def brazo(gallina, t_cambio=None, y=1150, ancho=1250, z=0.5):
    """Brazo liso que pasa a piel de gallina en t_cambio (o fijo)."""
    if t_cambio is None:
        return [OB("brazo_gallina" if gallina else "brazo_liso", 540, y, ancho, z=z)]
    return [OB("brazo_liso", 540, y, ancho, z=z, keys=[{"t": 0, "op": 1}, {"t": t_cambio, "op": 1}, {"t": t_cambio + 0.12, "op": 0}]),
            OB("brazo_gallina", 540, y, ancho, z=z + 0.01, keys=[{"t": 0, "op": 0}, {"t": t_cambio, "op": 0}, {"t": t_cambio + 0.12, "op": 1}])]


def nieve(n=6, sem=1):
    import random
    r = random.Random(sem)
    out = []
    for i in range(n):
        x = r.uniform(100, 980); y0 = r.uniform(500, 900)
        out.append(OB("copo_nieve", x, y0, r.uniform(50, 90), z=0.7, keys=[{"t": 0, "y": y0}, {"t": 6, "y": y0 + 600, "ease": "lineal"}]))
    return out


@v.plano(0, "gancho: el brazo enorme y los pelos se ponen de punta de golpe")
def _(d):
    return P(INV, [BG("bg_ventana_invierno")] + brazo(True, 0.35, 1150, 1500) + nieve(6, 1),
             cam(1.0, 1.08, (540, 1150)), vineta=0.35, sfx=[(0.35, "roce", -14), (0.4, "pop", -18)])


@v.plano(5, "mira tu brazo cuando hace frío: ventana con nieve, el brazo liso")
def _(d):
    return P(INV, [BG("bg_ventana_invierno")] + brazo(False, None, 1250, 1150) + nieve(5, 2), cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[cap(0.3, d - 0.05, "FRÍO", "#141414", "#7df9ffe6", 120, y=640)], sfx=[(0.1, "roce", -22)])


@v.plano(11, "piel de gallina: se eriza")
def _(d):
    return P(INV, [BG("bg_ventana_invierno")] + brazo(True, 0.1, 1150, 1400), cam(1.1, 1.2, (540, 1150)), "corte",
             hud=[amarillo(0.15, d - 0.05, "PIEL DE GALLINA", y=650, tam=110, color=AMBAR)], sfx=[(0.1, "pop", -16)])


@v.plano(14, "cada bultito es un músculo diminuto: corte de la piel con el músculo rojo")
def _(d):
    return P(CER, [BG("bg_cerebro"), OB("piel_corte_a", 540, 1150, 900, keys=aparece(0.0)), senala(700, 1000, 0.4, d - 0.05, 130, "#ff3d3d")],
             cam(1.0, 1.05, (600, 1100)), "corte", hud=[cap(0.4, d - 0.05, "MÚSCULO", "#ffffff", "#c0392be6", 110, y=640)], sfx=[(0.4, "pop", -20)])


@v.plano(20, "que tira de un pelo y lo pone de punta: el músculo se contrae y el pelo se levanta")
def _(d):
    t = min(0.6, d * 0.4)
    return P(CER, [BG("bg_cerebro"), OB("piel_corte_a", 540, 1150, 900, keys=[{"t": 0, "op": 1}, {"t": t, "op": 1}, {"t": t + 0.15, "op": 0}]),
                   OB("piel_corte_b", 540, 1150, 900, z=0.51, keys=[{"t": 0, "op": 0}, {"t": t, "op": 0}, {"t": t + 0.15, "op": 1}])],
             cam(1.05, 1.12, (500, 950)), "corte", hud=[cap(t + 0.1, d - 0.05, "DE PUNTA", "#141414", "#ffd23fe6", 110, y=640)], sfx=[(t, "impacto", -18)])


@v.plano(30, "a nuestros antepasados, cubiertos de pelo: la cueva con el fuego")
def _(d):
    return P(CUEVA, [BG("bg_cueva_campamento"), OB("llama_vela", 540, 1250, 200, z=0.6, keys=late(0.0, 3, 0.06, 0.3)), brillo(540, 1250, 400, "#ffb060", 0.6, 0.4)],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[cap(0.3, d - 0.05, "ANTEPASADOS", "#ffffff", "#8a4a1ee6", 100, y=640)], sfx=[(0.1, "roce", -22)])


@v.plano(36, "eso les servía: el corte con el pelo de punta")
def _(d):
    return P(CER, [BG("bg_cerebro"), OB("piel_corte_b", 540, 1150, 900)], cam(1.0, 1.05, (540, 1050)), "corte",
             hud=[cap(0.2, d - 0.05, "SERVÍA", "#141414", "#5dff8ae6", 110, y=640)], sfx=[(0.1, "ding", -20)])


@v.plano(39, "el pelo erizado atrapa una capa de aire caliente: brillo cálido entre los pelos")
def _(d):
    return P(INV, [BG("bg_ventana_invierno")] + brazo(True, None, 1200, 1450) +
             [brillo(540, 1040, 520, "#ffb060", 0.7, 0.55, keys=[{"t": 0, "op": 0}, {"t": d * 0.6, "op": 1, "ease": "suave"}])],
             cam(1.1, 1.15, (540, 1100)), "corte", hud=[cap(0.3, d - 0.05, "AIRE CALIENTE", "#141414", "#ffd23fe6", 100, y=640)], sfx=[(0.2, "brillo", -20)])


@v.plano(48, "como un abrigo: el gorro de lana")
def _(d):
    return P(INV, [BG("bg_ventana_invierno"), OB("gorro_lana_a", 540, 1150, 560, keys=cae(0.0, 0.3, 800, 1150))], cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[cap(0.35, d - 0.05, "ABRIGO", "#141414", "#7df9ffe6", 120, y=640)], sfx=[(0.3, "pop", -20)])


@v.plano(51, "y ante un peligro, te hace parecer más grande: el gato tranquilo")
def _(d):
    S = SUELO["bg_oficina_gris"]
    return P(CASA, [BG("bg_oficina_gris"), PZ("gato_calma", 540, S, 700, pie=40)], cam(1.0, 1.05, (540, 1250)), "corte",
             hud=[BANDA(), cap(0.3, d - 0.05, "PELIGRO", "#ffffff", "#c0392be6", 110, y=760)], sfx=[(0.1, "pop", -22)])


@v.plano(60, "por eso un animal asustado se eriza entero: el gato se arquea y se eriza")
def _(d):
    S = SUELO["bg_oficina_gris"]
    return P(CASA, [BG("bg_oficina_gris"), PZ("gato_calma", 540, S, 700, pie=40, keys=[{"t": 0, "op": 1}, {"t": 0.25, "op": 1}, {"t": 0.3, "op": 0}]),
                    PZ("gato_erizado", 540, S, 760, pie=40, keys=[{"t": 0, "op": 0}, {"t": 0.25, "op": 0}, {"t": 0.3, "op": 1}] + late(0.3, 2, 0.06, 0.2))],
             cam(1.05, 1.12, (540, 1250)), "corte", hud=[BANDA(), cap(0.4, d - 0.05, "MÁS GRANDE", "#141414", "#ffd23fe6", 110, y=760)], sfx=[(0.3, "impacto", -16)])


@v.plano(68, "nosotros perdimos casi todo el pelo: el brazo liso, casi sin pelo")
def _(d):
    return P(CASA, [BG("bg_oficina_gris"), PZ("voluntario_4", 540, S_O, 1050, keys=aparece(0.0))], cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[BANDA(), cap(0.3, d - 0.05, "CASI SIN PELO", "#141414", "#7df9ffe6", 100, y=760)], sfx=[(0.1, "pop", -22)])


@v.plano(74, "pero el reflejo se quedó: el corte con el músculo que late")
def _(d):
    return P(CER, [BG("bg_cerebro"), OB("piel_corte_b", 540, 1150, 900, keys=late(0.1, 2, 0.04, 0.35))], cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[cap(0.2, d - 0.05, "EL REFLEJO", "#ffffff", "#c0392be6", 110, y=640)], sfx=[(0.1, "senal", -20)])


@v.plano(79, "por eso se te eriza la piel con una canción que te emociona: la chica con auriculares y notas")
def _(d):
    return P(CASA, [BG("bg_oficina_gris"), OB("cara_oyente", 540, 1200, 900, keys=aparece(0.0)), OB("auriculares", 540, 980, 520, z=0.6),
                    OB("nota_musical_a", 220, 900, 140, z=0.7, keys=flota(d, 20, 900)), OB("nota_musical_b", 860, 820, 140, z=0.7, keys=flota(d, 16, 820))],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[BANDA()], sfx=[(0.1, "ding", -22)])


@v.plano(92, "o con un susto: cara de sorpresa")
def _(d):
    return P(CASA, [BG("bg_oficina_gris"), OB("cara_chica_sorpresa", 540, 1200, 900, keys=[{"t": 0, "escala": 1.08}, {"t": 0.2, "escala": 1.0, "ease": "golpe"}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[BANDA(), amarillo(0.05, d - 0.05, "¡SUSTO!", y=760, tam=130, color=AMBAR)], sfx=[(0.05, "impacto", -14)])


@v.plano(96, "lo manda el mismo sistema de alerta: el cerebro con un nervio amarillo hasta la piel")
def _(d):
    return P(CER, [BG("bg_cerebro"), OB("cerebro_brillo", 540, 900, 560, keys=late(0.1, 2, 0.05, 0.4)),
                   flecha([[540, 1100], [480, 1350], [700, 1650]], 0.2, min(0.9, d * 0.6), "#ffd23f", 14, z=0.6)],
             cam(1.0, 1.04, (540, 1100)), "corte", hud=[cap(0.3, d - 0.05, "ALERTA", "#141414", "#ffd23fe6", 120, y=1500)], sfx=[(0.2, "senal", -18)])


@v.plano(103, "¿ya no sirve para nada?: el brazo con interrogante")
def _(d):
    return P(INV, [BG("bg_ventana_invierno")] + brazo(True, None, 1200, 1400), cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[amarillo(0.05, d - 0.05, "¿PARA NADA?", y=650, tam=120, color=CIAN)], sfx=[(0.05, "impacto", -20)])


@v.plano(108, "en dos mil veinte, en Harvard: la investigadora en el laboratorio")
def _(d):
    return P(CASA, [BG("bg_oficina_gris"), PZ("investigadora", 540, S_O, 1050, keys=aparece(0.0))], cam(1.0, 1.05, (540, 1150)), "corte",
             hud=[BANDA(), contador(0.05, min(0.9, d * 0.5), 2000, 2020, 0.5, miles=False, tam=130, color="#141414", capsula="#ffffffe6", y=760),
                  cap(min(1.0, d * 0.55), d - 0.05, "HARVARD", "#ffffff", "#a8282ee6", 110, y=760)], sfx=[(0.05, "tic", -20)])


@v.plano(114, "vieron en ratones: el ratón blanco")
def _(d):
    return P(CASA, [BG("bg_oficina_gris"), OB("raton", 540, 1250, 760, keys=aparece(0.0) + [{"t": 0, "x": 500}, {"t": d, "x": 580}])],
             cam(1.0, 1.06, (540, 1200)), "corte", hud=[BANDA(), cap(0.05, d - 0.02, "RATONES", "#141414", "#7df9ffe6", 110, y=760)], sfx=[(0.1, "pop", -20)])


@v.plano(117, "que ese nervio y ese músculo: el corte con el nervio encendido")
def _(d):
    return P(CER, [BG("bg_cerebro"), OB("piel_corte_b", 540, 1150, 900), senala(800, 1000, 0.2, d - 0.05, 140, "#ffd23f")],
             cam(1.05, 1.1, (600, 1100)), "corte", hud=[cap(0.3, d - 0.05, "NERVIO + MÚSCULO", "#141414", "#ffd23fe6", 84, y=640)], sfx=[(0.2, "senal", -20)])


@v.plano(123, "también despiertan las células madre del pelo: se encienden verdes")
def _(d):
    return P(CER, [BG("bg_cerebro"), OB("piel_corte_c", 540, 1150, 900, keys=aparece(0.0)),
                   OB("celulas_madre", 840, 1550, 300, z=0.6, keys=[{"t": 0, "escala": 0.3, "op": 0}, {"t": 0.5, "escala": 1.0, "op": 1, "ease": "salida"}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[cap(0.4, d - 0.05, "CÉLULAS MADRE", "#141414", "#5dff8ae6", 96, y=640)], sfx=[(0.3, "brillo", -18)])


@v.plano(130, "con días de frío, crece pelo nuevo: calendario y el pelo que sale")
def _(d):
    return P(INV, [BG("bg_ventana_invierno"), OB("calendario_hoja", 300, 1000, 360, keys=aparece(0.0)), OB("raton", 640, 1350, 640, keys=late(0.3, 2, 0.04, 0.3))] + nieve(5, 3),
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[cap(0.3, d - 0.05, "PELO NUEVO", "#141414", "#5dff8ae6", 110, y=640)], sfx=[(0.3, "ding", -20)])


@v.plano(137, "la piel de gallina también avisa: hace falta abrigo")
def _(d):
    return P(INV, [BG("bg_ventana_invierno")] + brazo(True, None, 1200, 1400) + [OB("gorro_lana_b", 860, 800, 260, z=0.7, keys=aparece(0.3))],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[cap(0.2, d - 0.05, "AVISA", "#ffffff", "#c0392be6", 120, y=640)], sfx=[(0.1, "ding", -18)])


@v.plano(146, "¿a ti con qué se te pone? (bucle): el brazo se eriza otra vez")
def _(d):
    return P(INV, [BG("bg_ventana_invierno")] + brazo(True, 0.3, 1150, 1500) + nieve(6, 1), cam(1.0, 1.06, (540, 1150)), "corte", sfx=[(0.3, "roce", -18)])


def micro(fondo, els, txt=None, col="#ffffff", cap_f="#c0392be6", sfx="pop"):
    def fn(d):
        return P(fondo, els(d), cam(1.15, 1.3, (540, 1000)), "corte", hud=[cap(0.0, d - 0.02, txt, col, cap_f, 120)] if txt else [], sfx=[(0.01, sfx, -18)])
    return fn


v.plano(28, "micro: un pelo de punta")(micro(CER, lambda d: [BG("bg_cerebro"), OB("piel_corte_b", 540, 1300, 1600)], sfx="pop"))
v.plano(66, "micro: el gato bufa")(micro(CASA, lambda d: [BG("bg_oficina_gris"), OB("gato_erizado", 540, 1150, 1300)], sfx="impacto"))
v.plano(88, "micro: la nota")(micro(CASA, lambda d: [BG("bg_oficina_gris"), OB("nota_musical_a", 540, 1050, 500, keys=flota(d, 20, 1050))], sfx="ding"))


v.construir("2026-11-27-tarde-03-piel-de-gallina", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 1273, "db": -13},
            claves=["piel", "pelo", "brazo", "frío", "gallina", "músculo", "punta", "antepasados", "aire", "abrigo", "peligro", "grande",
                    "asustado", "reflejo", "canción", "susto", "alerta", "Harvard", "ratones", "nervio", "células", "madre", "nuevo", "avisa"],
            ep_extra={"sfx_bajo_voz": True})
