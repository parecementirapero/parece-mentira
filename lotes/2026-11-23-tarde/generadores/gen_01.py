"""01 · No ves tus ojos moverse (movimientos sacádicos) — método denso, estilo cartoon. Lote 2026-11-23-tarde (Jorge, con el agente).
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
from comun_1123t import *  # noqa: E402,F401,F403
import ilus_1123t  # noqa: E402

SVG = ilus_1123t.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
ESC = ["#1a2a6a", "#2f55b0"]


def ojo(d, x=540, y=1050, ancho=900, xs=(-150, 150), paso=0.45, t0=0.0, liso=False):
    k = ancho / 700
    if liso:
        kp = [{"t": 0, "x": x - 150 * k}, {"t": d, "x": x + 150 * k, "ease": "suave"}]
    else:
        kp = [{**kk, "x": x + kk["x"] * k, "y": y} for kk in saltos(d, list(xs), t0, paso)]
    return [IMG("ojo_cartoon", ancho=ancho, x=x, y=y, z=0.5), IMG("pupila_cartoon", ancho=330 * k, x=x, y=y + 10 * k, z=0.51, keys=[{**kk, "y": y + 10 * k} for kk in kp])]


@v.plano(0, "gancho: un ojo enorme cuya pupila salta de lado a lado")
def _(d):
    return P(OSC, [*ojo(d, paso=0.4)], cam(1.0, 1.08, (540, 1050)), vineta=0.5, sfx=[(0.02, "pop", -18), (0.4, "pop", -20), (0.8, "pop", -20), (1.2, "pop", -20)])


@v.plano(5, "pruébalo: aparece el espejo")
def _(d):
    return P(ESC, [BG("esc_azul"), IMG("espejo", ancho=620, x=540, y=1100, z=0.5, keys=aparece(0.0))], cam(1.0, 1.05, (540, 1100)), "corte",
             hud=[rotulo(0.05, d - 0.03, "PRUÉBALO", tam=130, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "ding", -18)])


@v.plano(6, "ponte delante de un espejo: el muñeco se mira en el espejo")
def _(d):
    return P(ESC, [BG("esc_azul"), IMG("espejo", ancho=620, x=540, y=1100, z=0.45), *muneco("mu_b", "br_b", 540, 1150, 330, 0.6)],
             cam(1.0, 1.05, (540, 1100)), "corte", sfx=[(0.1, "roce", -22)])


@v.plano(11, "mira tu ojo izquierdo: primer plano, las pupilas miran a un lado")
def _(d):
    return P(ESC, [BG("esc_azul"), *muneco("mu_b", "br_b", 540, 1500, 900, 0.5, pup=(-22, 0)), senala(430, 1067, 0.2, d - 0.1, 90, LIMA)],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[amarillo(0.2, d - 0.05, "IZQUIERDO", y=560, tam=120, color=LIMA)], sfx=[(0.2, "pop", -20)])


@v.plano(15, "y ahora el derecho: las pupilas saltan al otro lado")
def _(d):
    return P(ESC, [BG("esc_azul"), *muneco("mu_b", "br_b", 540, 1500, 900, 0.5, pup=(22, 0)), senala(650, 1067, 0.1, d - 0.1, 90, MAGENTA)],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[amarillo(0.1, d - 0.05, "DERECHO", y=560, tam=120, color=MAGENTA)], sfx=[(0.05, "pop", -20)])


@v.plano(19, "¿has visto el movimiento?")
def _(d):
    return P(OSC, [*ojo(d, paso=0.5)], cam(1.05, 1.12, (540, 1050)), "corte", hud=[amarillo(0.1, d - 0.05, "¿LO HAS VISTO?", y=560, tam=110, color="#ffd23f")], sfx=[(0.1, "roce", -20)])


@v.plano(23, "no: un NO enorme")
def _(d):
    return P(["#2a0a10", "#120406"], [brillo(540, 1000, 500, "#ff3d3d", 0.3, 0.06)], cam(1.0, 1.08, (540, 1000)), "corte",
             hud=[rotulo(0.0, d - 0.02, "NO", tam=300, color="#ffffff", capsula="#c0392be6", y=1000)], sfx=[(0.0, "golpe", -16)])


@v.plano(24, "pero cualquiera que te mire sí lo ve: otro muñeco mira cómo se mueven sus ojos")
def _(d):
    t = d / 4
    kp = [{"t": 0, "x": 760 - 15}, {"t": t, "x": 760 - 15}, {"t": t + 0.05, "x": 760 + 15}, {"t": 2 * t, "x": 760 + 15}, {"t": 2 * t + 0.05, "x": 760 - 15}, {"t": d, "x": 760 - 15}]
    return P(ESC, [BG("esc_azul"), *muneco("mu_a", "br_a", 320, 1250, 380, 0.5, pup=(14, 0)), *muneco("mu_b", "br_b", 760, 1250, 380, 0.5, keys_pup=[{**k, "y": 1250} for k in kp]),
                   flecha([[400, 1020], [660, 1030]], 0.2, d * 0.5, LIMA, 8, disc=[20, 14], z=0.7)],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[amarillo(0.4, d - 0.05, "ÉL SÍ LO VE", y=560, tam=110, color=LIMA)], sfx=[(t, "pop", -22), (2 * t, "pop", -22)])


@v.plano(32, "¿qué está pasando?: el ojo de cerca")
def _(d):
    return P(OSC, [*ojo(d, ancho=1000, paso=0.6)], cam(1.0, 1.08, (540, 1050)), "corte", hud=[amarillo(0.1, d - 0.05, "¿QUÉ PASA?", y=560, tam=120, color=CIAN)], sfx=[(0.1, "roce", -20)])


@v.plano(35, "tus ojos no se deslizan: la pupila se desliza suave y se tacha")
def _(d):
    return P(OSC, [*ojo(d, liso=True), flecha([[340, 1450], [740, 650]], d * 0.6, d * 0.6 + 0.2, "#ff3d3d", 18, punta=False, z=0.8),
                   flecha([[740, 1450], [340, 650]], d * 0.6 + 0.1, d * 0.6 + 0.3, "#ff3d3d", 18, punta=False, z=0.8)],
             cam(1.0, 1.04, (540, 1050)), "corte", hud=[rotulo(0.1, d - 0.05, "NO SE DESLIZAN", tam=90, color="#ffffff", capsula="#c0392be6", y=560)], sfx=[(d * 0.6, "zap", -18)])


@v.plano(40, "dan saltos rapidísimos: la pupila salta con arcos")
def _(d):
    return P(OSC, [*ojo(d, paso=0.3, xs=(-150, 0, 150, 0)), IMG("salto", ancho=600, x=540, y=760, z=0.6, keys=late(0.0, 3, 0.1, 0.3))],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[amarillo(0.1, d - 0.05, "SALTOS", y=560, tam=140, color="#ffd23f")],
             sfx=[(0.0, "pop", -20), (0.3, "pop", -20), (0.6, "pop", -20), (0.9, "pop", -20)])


@v.plano(43, "llamados movimientos sacádicos")
def _(d):
    return P(OSC, [*ojo(d, paso=0.35, xs=(-150, 150))], cam(1.12, 1.18, (540, 1050)), "corte",
             hud=[rotulo(0.1, d - 0.05, "MOVIMIENTOS SACÁDICOS", tam=78, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(0.1, "brillo", -20)])


@v.plano(46, "haces varios cada segundo: el reloj y la pupila que salta")
def _(d):
    return P(OSC, [IMG("reloj_cartoon", ancho=520, x=540, y=1350, z=0.5), IMG("segundero", ancho=520, x=540, y=1350, z=0.55, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": 6 * d, "ease": "lineal"}]),
                   *ojo(d, y=760, ancho=600, paso=0.3)], cam(1.0, 1.04, (540, 1050)), "corte",
             hud=[amarillo(0.2, d - 0.05, "VARIOS CADA SEGUNDO", y=1040, tam=80, color="#ffd23f")], sfx=[(0.05, "tictac", -22, {"dur": d, "ritmo": 0.3})])


@v.plano(50, "por ejemplo ahora, mientras lees: la mirada salta por las líneas de la pizarra")
def _(d):
    pasos = [[200 + 140 * k, 760] for k in range(6)] + [[200 + 140 * k, 900] for k in range(6)]
    return P(OSC, [BG("bg_pizarra"), *[{"tipo": "forma", "forma": "rect", "ancho": 760, "alto": 26, "relleno": "#b8b8c8", "x": 540, "y": yy, "z": 0.4} for yy in (760, 900, 1040, 1180, 1320)],
                   IMG("pupila_cartoon", ancho=110, z=0.6, keys=[{"t": round(i * d / len(pasos), 3), "x": p[0], "y": p[1], "ease": "lineal"} for i, p in enumerate(pasos)])],
             cam(1.0, 1.04, (540, 1000)), "corte", hud=[amarillo(0.2, d - 0.05, "AHORA MISMO", y=560 - 40, tam=110, color=CIAN)], sfx=[(0.1, "tictac", -24, {"dur": d, "ritmo": d / 12})])


@v.plano(55, "y durante cada salto, tu cerebro bloquea la imagen: la pantalla se apaga a golpes")
def _(d):
    n = 5
    ks = []
    for i in range(n):
        t = d * (i + 0.5) / n
        ks += [{"t": round(t - 0.01, 3), "op": 0}, {"t": round(t, 3), "op": 1}, {"t": round(t + 0.12, 3), "op": 1}, {"t": round(t + 0.13, 3), "op": 0}]
    return P(OSC, [IMG("cerebro", ancho=820, x=540, y=1050, z=0.5, keys=late(0.1, 2, 0.05)),
                   {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#000000", "x": 540, "y": 960, "z": 0.9, "keys": [{"t": 0, "op": 0}] + ks}],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[amarillo(0.2, d - 0.05, "LA BLOQUEA", y=560, tam=120, color=MAGENTA)], sfx=[(d * (i + 0.5) / n, "zap", -24) for i in range(n)])


@v.plano(64, "si no lo hiciera, verías el mundo borroso y temblando: el paisaje tiembla")
def _(d):
    return P(CIELO, [BG("bg_cielo_dia"), IMG("sol_dibujo", ancho=380, x=820, y=520, z=0.4)], cam(1.05, 1.1, (540, 1000), temblor=16), "corte",
             hud=[amarillo(0.3, d - 0.05, "BORROSO", y=560 + 300, tam=130, color="#ffffff")], sfx=[(0.1, "whoosh", -18, {"dur": d})])


@v.plano(77, "después, tu cerebro rellena el hueco con lo que ve al aterrizar")
def _(d):
    return P(OSC, [IMG("cerebro", ancho=820, x=540, y=1050, z=0.5), brillo(540, 1000, 500, "#7df9ff", 0.5, 0.6, keys=[{"t": 0, "op": 0}, {"t": d * 0.7, "op": 1}])],
             cam(1.0, 1.08, (540, 1050)), "desenfoque", hud=[rotulo(0.3, d - 0.05, "RELLENA EL HUECO", tam=88, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(0.2, "brillo", -20)])


@v.plano(89, "¿y cómo se nota?: el reloj aparece")
def _(d):
    return P(OSC, [IMG("reloj_cartoon", ancho=680, x=540, y=1100, z=0.5, keys=aparece(0.0)), IMG("segundero", ancho=680, x=540, y=1100, z=0.55, keys=aparece(0.0))],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[amarillo(0.1, d - 0.05, "¿CÓMO SE NOTA?", y=560, tam=110, color="#ffd23f")], sfx=[(0.05, "pop", -20)])


@v.plano(93, "mira de golpe un reloj con segundero: la mirada salta al reloj")
def _(d):
    return P(OSC, [IMG("reloj_cartoon", ancho=680, x=540, y=1100, z=0.5), IMG("segundero", ancho=680, x=540, y=1100, z=0.55, keys=[{"t": 0, "rot": 30}, {"t": d, "rot": 30 + 6 * int(d)}]),
                   IMG("pupila_cartoon", ancho=150, z=0.6, keys=[{"t": 0, "x": 160, "y": 1600}, {"t": 0.15, "x": 540, "y": 1100}])],
             cam(1.0, 1.06, (540, 1100)), "corte", sfx=[(0.1, "whoosh", -20), (0.5, "tictac", -20, {"dur": d - 0.5, "ritmo": 1.0})])


@v.plano(100, "el primer segundo parece durar más de la cuenta: el segundero se queda parado")
def _(d):
    return P(OSC, [IMG("reloj_cartoon", ancho=680, x=540, y=1100, z=0.5),
                   IMG("segundero", ancho=680, x=540, y=1100, z=0.55, keys=[{"t": 0, "rot": 42}, {"t": d * 0.75, "rot": 42}, {"t": d * 0.78, "rot": 48}, {"t": d, "rot": 48}])],
             cam(1.1, 1.25, (540, 1100)), "corte", hud=[amarillo(0.3, d - 0.05, "¿SE HA PARADO?", y=560, tam=110, color=MAGENTA)], sfx=[(d * 0.76, "tictac", -16, {"dur": 0.3, "ritmo": 0.3})])


@v.plano(109, "es tu cerebro tapando el salto")
def _(d):
    return P(OSC, [IMG("cerebro", ancho=760, x=540, y=1050, z=0.5, keys=late(0.1, 1)), IMG("salto", ancho=520, x=540, y=700, z=0.6)], cam(1.0, 1.06, (540, 1000)), "corte",
             hud=[amarillo(0.3, d - 0.05, "TAPA EL SALTO", y=1650 - 300, tam=110, color="#ffd23f")], sfx=[(0.1, "pop", -20)])


@v.plano(115, "así que hay ratitos de cada día en los que no ves nada: el cielo se apaga a ratos")
def _(d):
    ks = [{"t": 0, "op": 0}]
    for i in range(6):
        t = d * (i + 0.5) / 6
        ks += [{"t": round(t - 0.01, 3), "op": 0}, {"t": round(t, 3), "op": 1}, {"t": round(t + 0.1, 3), "op": 1}, {"t": round(t + 0.11, 3), "op": 0}]
    return P(CIELO, [BG("bg_cielo_dia"), IMG("sol_dibujo", ancho=380, x=820, y=520, z=0.4),
                     {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#000000", "x": 540, "y": 960, "z": 0.9, "keys": ks}],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[amarillo(0.3, d - 0.05, "NO VES NADA", y=560 + 300, tam=120, color="#ffffff")])


@v.plano(128, "y nunca te has dado cuenta: el muñeco sonríe y parpadea")
def _(d):
    return P(ESC, [BG("esc_azul"), *muneco("mu_b", "br_b", 540, 1500, 900, 0.5, keys_pup=[{"t": 0, "x": 540, "y": 1500}, {"t": d * 0.5, "x": 560, "y": 1500}, {"t": d * 0.5 + 0.05, "x": 520, "y": 1500}])],
             cam(1.0, 1.05, (540, 1050)), "corte", sfx=[(d * 0.5, "pop", -22)])


@v.plano(134, "haz la prueba en el espejo y cuéntame: el espejo con el ojo que salta (bucle)")
def _(d):
    return P(ESC, [BG("esc_azul"), IMG("espejo", ancho=620, x=540, y=1100, z=0.45, keys=late(0.2, 1, 0.05)), *muneco("mu_b", "br_b", 540, 1150, 330, 0.6)],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[rotulo(0.3, d - 0.4, "CUÉNTAME", tam=96, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.2, "ding", -22)])


v.construir("2026-11-23-tarde-01-ojos-sacadicos", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 91, "db": -13},
            claves=["ojos", "moverse", "espejo", "izquierdo", "derecho", "movimiento", "ve", "deslizan", "saltos", "sacádicos", "segundo", "lees", "bloquea",
                    "borroso", "temblando", "rellena", "reloj", "segundero", "cuenta", "salto", "nada", "prueba"])
