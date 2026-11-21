"""02 · Desde el Mulhacén se ve África — método denso. Lote 2026-11-20-tarde (Agente 20:00, Jorge). Tendencia del día: «sierra nevada».
Uso: python3 gen_02.py DIR_SALIDA [02-locucion.mp3 02-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_1120t  # noqa: E402

SVG = ilus_1120t.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "02-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

CIELO = ["#1a4a9a", "#a8d4f8"]
OSC = ["#06122a", "#020610"]
ARCO_Y = 1450          # centro del casco de la Tierra (lienzo 1080×900): la cima del arco queda en y=1450
CIMA = 1450 - 0        # punto más alto del arco


def arco(): return IMG("tierra_arco", ancho=1080, x=540, y=ARCO_Y + 450 - 450, z=0.3)  # su cima (y=450 del lienzo) cae en ARCO_Y


def vista(rif=True, z=0.05): return BG("bg_vista_africa" if rif else "bg_vista_africa_sin", z=z)


def nieve(n=30, sem=1): return polvo("#ffffff", n, (0, 500, 1080, 1700), sem)



def amarillo(t0, t1, texto, y=1360, tam=96, color="#ffd23f", x=540):
    """Palabra clave con cápsula oscura (sobre la laguna y la nieve el texto suelto no llega a 3:1 de contraste)."""
    return {**rotulo(t0, t1, texto, tam=tam, color=color, capsula="#0a0a14c8", rot=-4, x=x, y=y), "_clave": True}


# ================================================================== PLANOS
@v.plano(0, "gancho: el montañero llega a la cima y delante aparecen las montañas de África al otro lado del mar")
def _(d):
    return P(CIELO, [vista(False), {**vista(True, 0.06), "keys": [{"t": 0, "op": 0.3}, {"t": d * 0.8, "op": 1, "ease": "suave"}]},
                     IMG("excursionista", ancho=520, x=540, z=0.6, keys=arranque(560, 1560, d, "abajo", 360, 40)), nieve(20, 1)],
             cam(1.0, 1.06, (540, 1100)), vineta=0.45, sfx=[(0.02, "rumor", -18, {"dur": 1.4}), (0.8, "brillo", -18)])


@v.plano(5, "esto es el Mulhacén: la cima nevada con el vértice de piedra")
def _(d):
    return P(CIELO, [BG("bg_cumbre"), nieve(30, 2)], cam(1.0, 1.25, (540, 1200), (560, 900)), "desenfoque", sfx=[(0.05, "rumor", -20, {"dur": d})])


@v.plano(9, "en Granada: mapa del sur de la península, la sierra señalada")
def _(d):
    return P(["#0a2a5a", "#0a2a5a"], [BG("mapa_estrecho"), senala(560, 470, 0.05, d - 0.1, 110, AMBAR)],
             cam(1.3, 1.4, (540, 700)), "corte", hud=[rotulo(0.1, d - 0.05, "GRANADA", tam=96, color="#141414", capsula="#ffd23fe6", y=900)], sfx=[(0.05, "pop", -20)])


@v.plano(11, "tres mil cuatrocientos setenta y nueve metros: la montaña y la altura que sube")
def _(d):
    return P(CIELO, [BG("bg_montanas_dia"), IMG("montana", ancho=1000, x=540, y=1300, z=0.4, keys=arranque(540, 1300, d, "abajo", 120, 10)),
                     flecha([[960, 1700], [960, 900]], 0.1, d * 0.75, LIMA, 10, z=0.6)],
             cam(1.0, 1.05, (540, 1200)), "corte", hud=[contador(0.05, d - 0.03, 0, 3479, d * 0.75, " M", y=560, tam=130, color=LIMA, capsula="#000000a0")],
             sfx=[(0.05, "subida", -18, {"dur": d * 0.75})])


@v.plano(18, "el pico más alto de la península: la cima destaca sobre las demás")
def _(d):
    return P(CIELO, [BG("bg_montanas_dia"), IMG("montana", ancho=820, x=540, y=1250, z=0.4, keys=late(0.2, 1)), senala(540, 900, 0.2, d - 0.1, 90, AMBAR)],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[rotulo(0.1, d - 0.03, "EL MÁS ALTO", tam=100, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.2, "ding", -20)])


@v.plano(25, "en un día muy claro: la cumbre bajo el sol, brillo que late")
def _(d):
    return P(CIELO, [BG("bg_cumbre"), brillo(860, 330, 300, "#fff4c0", 0.6, 0.07, pulso=[0.12, 1.5]), nieve(20, 3)],
             cam(1.05, 1.12, (700, 700)), "corte", sfx=[(0.1, "brillo", -20)])


@v.plano(30, "al sur: en el mapa, flecha de la sierra hacia abajo")
def _(d):
    return P(["#0a2a5a", "#0a2a5a"], [BG("mapa_estrecho"), flecha([[560, 520], [560, 1000]], 0.05, d * 0.8, CIAN, 12, z=0.6)],
             cam(1.0, 1.04, (540, 900)), "corte", hud=[amarillo(0.1, d - 0.05, "SUR", y=560, tam=140, color=CIAN)], sfx=[(0.05, "whoosh", -20)])


@v.plano(32, "al otro lado del Mediterráneo: la flecha cruza el mar hasta la otra orilla")
def _(d):
    return P(["#0a2a5a", "#0a2a5a"], [BG("mapa_estrecho"), flecha([[560, 520], [560, 1000], [420, 1340]], 0.0, d * 0.8, CIAN, 12, z=0.6), polvo("#ffffff", 20, (0, 900, 1080, 1250), 4)],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[rotulo(0.2, d - 0.05, "MEDITERRÁNEO", tam=84, color="#ffffff", capsula="#1a5a9ae6", y=1120)], sfx=[(0.1, "ola", -20)])


@v.plano(37, "aparecen las montañas del Rif: desde la cima, las sierras de África se encienden en el horizonte")
def _(d):
    return P(CIELO, [vista(False), {**vista(True, 0.06), "keys": [{"t": 0, "op": 0}, {"t": d * 0.6, "op": 1, "ease": "suave"}]}, senala(540, 940, d * 0.5, d - 0.1, 130, MAGENTA)],
             cam(1.3, 1.45, (540, 1000)), "corte", sfx=[(0.1, "subida", -18, {"dur": d * 0.6}), (d * 0.6, "impacto", -16)])


@v.plano(42, "en Marruecos: en el mapa, la otra orilla señalada")
def _(d):
    return P(["#0a2a5a", "#0a2a5a"], [BG("mapa_estrecho"), senala(330, 1390, 0.05, d - 0.1, 130, MAGENTA)],
             cam(1.2, 1.3, (420, 1300)), "corte", hud=[rotulo(0.1, d - 0.05, "MARRUECOS", tam=96, color="#ffffff", capsula="#c0397ae6", y=1080)], sfx=[(0.05, "pop", -20)])


@v.plano(44, "¿cómo puedes ver otro continente?: los prismáticos")
def _(d):
    return P(OSC, [BG("bg_cumbre"), {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#000010", "op": 0.45, "x": 540, "y": 960, "z": 0.2},
                   IMG("prismaticos", ancho=760, x=540, y=1150, z=0.5, keys=aparece(0.05) + [{"t": d, "rot": 4}])],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[amarillo(0.2, d - 0.05, "¿CÓMO?", y=560, tam=140, color=CIAN)], sfx=[(0.1, "roce", -20)])


@v.plano(49, "por la curva de la Tierra: el casquete azul se dibuja")
def _(d):
    return P(OSC, [estrellas(50, 5), {**arco(), "keys": [{"t": 0, "y": ARCO_Y + 300}, {"t": 0.5, "y": ARCO_Y, "ease": "salida"}]},
                   senala(540, ARCO_Y + 40, 0.5, d - 0.1, 120, AMBAR)],
             cam(1.0, 1.05, (540, 1400)), "corte", hud=[amarillo(0.2, d - 0.05, "CURVA", y=560, tam=140, color=AMBAR)], sfx=[(0.3, "trazo", -20)])


@v.plano(55, "en la playa: una persona mira el mar")
def _(d):
    return P(CIELO, [BG("bg_playa"), IMG("persona_pie", ancho=180, x=300, y=1500, z=0.5, keys=[{"t": 0, "x": 260}, {"t": d, "x": 320, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1200)), "desenfoque", sfx=[(0.05, "ola", -18)])


@v.plano(58, "con los ojos a un metro setenta del suelo: la altura de sus ojos")
def _(d):
    return P(CIELO, [BG("bg_playa"), IMG("persona_pie", ancho=260, x=420, y=1400, z=0.5), flecha([[260, 1640], [260, 1190]], 0.1, d * 0.6, LIMA, 10, z=0.6),
                     flecha([[230, 1180], [470, 1180]], d * 0.6, d * 0.7, LIMA, 6, punta=False, z=0.6)],
             cam(1.3, 1.35, (420, 1400)), "corte", hud=[rotulo(0.2, d - 0.05, "1,70 M", tam=110, color="#141414", capsula="#b8ff3ae6", y=880)], sfx=[(0.1, "subida", -20, {"dur": d * 0.6})])


@v.plano(67, "el horizonte está a unos cinco kilómetros: la mirada llega hasta la línea del mar")
def _(d):
    return P(CIELO, [BG("bg_playa"), IMG("persona_pie", ancho=180, x=200, y=1480, z=0.5), flecha([[230, 1330], [1000, 1000]], 0.05, d * 0.6, CIAN, 8, disc=[26, 18], z=0.6),
                     senala(1000, 1000, d * 0.6, d - 0.1, 60, CIAN)],
             cam(1.0, 1.04, (540, 1200)), "corte", hud=[contador(0.1, d - 0.03, 0, 5, d * 0.6, " KM", y=560, tam=130, color=CIAN, capsula="#000000a0")],
             sfx=[(0.05, "whoosh", -22)])


@v.plano(74, "más allá, el planeta se esconde: en el arco, la línea de la mirada pasa por encima del mar")
def _(d):
    return P(OSC, [estrellas(50, 6), arco(), IMG("persona_pie_clara", ancho=60, x=540, y=ARCO_Y - 40, z=0.55),
                   flecha([[555, ARCO_Y - 65], [1060, ARCO_Y - 65]], 0.05, d * 0.6, CIAN, 6, disc=[22, 14], z=0.6),
                   senala(820, ARCO_Y + 80, d * 0.6, d - 0.1, 90, MAGENTA)],
             cam(1.0, 1.05, (540, 1400)), "corte", hud=[amarillo(0.3, d - 0.05, "SE ESCONDE", y=560, tam=120, color=MAGENTA)], sfx=[(0.1, "roce", -20)])


@v.plano(80, "pero cuanto más alto subes: el montañero sube por la montaña")
def _(d):
    return P(CIELO, [BG("bg_montanas_dia"), IMG("montana", ancho=1100, x=540, y=1350, z=0.4),
                     IMG("excursionista", ancho=170, z=0.6, keys=[{"t": 0, "x": 260, "y": 1600}, {"t": d, "x": 520, "y": 1050, "ease": "suave"}]),
                     flecha([[860, 1700], [860, 1000]], 0.1, d * 0.8, LIMA, 10, z=0.6)],
             cam(1.0, 1.05, (540, 1300)), "corte", sfx=[(0.1, "subida", -20, {"dur": d})])


@v.plano(85, "más lejos se va el horizonte: desde lo alto, la línea de la mirada llega mucho más lejos")
def _(d):
    return P(OSC, [estrellas(50, 7), arco(), IMG("montana", ancho=260, x=540, y=ARCO_Y - 80, z=0.5),
                   flecha([[560, ARCO_Y - 175], [1060, ARCO_Y - 60]], 0.05, d * 0.7, LIMA, 7, disc=[22, 14], z=0.6)],
             cam(1.0, 1.05, (600, 1400)), "corte", hud=[amarillo(0.3, d - 0.05, "MÁS LEJOS", y=560, tam=120, color=LIMA)], sfx=[(0.1, "whoosh", -20)])


@v.plano(91, "desde la cima del Mulhacén: el vértice de la cumbre")
def _(d):
    return P(CIELO, [BG("bg_cumbre"), nieve(30, 8)], cam(1.6, 1.8, (560, 870)), "corte", sfx=[(0.05, "rumor", -20, {"dur": d})])


@v.plano(96, "a más de doscientos kilómetros: la vista al sur y la cifra que corre")
def _(d):
    return P(CIELO, [vista(True), flecha([[540, 1700], [540, 1060]], 0.05, d * 0.6, CIAN, 8, disc=[26, 18], z=0.6)],
             cam(1.0, 1.05, (540, 1100)), "corte", sfx=[(0.05, "subida", -20, {"dur": d * 0.6})])


@v.plano(101, "y el Rif también es alto: en el arco, una montaña al otro lado")
def _(d):
    return P(OSC, [estrellas(50, 9), arco(), IMG("montana", ancho=240, x=330, y=ARCO_Y - 20, z=0.5), IMG("montana", ancho=220, x=760, y=ARCO_Y - 10, z=0.5, keys=aparece(0.1) + late(0.6, 1))],
             cam(1.0, 1.05, (540, 1400)), "corte", hud=[rotulo(0.3, d - 0.05, "RIF", tam=120, color="#ffffff", capsula="#c0397ae6", y=1000, x=760)], sfx=[(0.1, "pop", -20)])


@v.plano(107, "sus cumbres asoman por encima de la curva: el Rif sube sobre el mar")
def _(d):
    return P(CIELO, [vista(False), {**vista(True, 0.06), "keys": [{"t": 0, "op": 0}, {"t": d * 0.7, "op": 1, "ease": "suave"}]}],
             cam(1.8, 1.9, (540, 960)), "corte", hud=[amarillo(0.3, d - 0.05, "ASOMAN", y=560, tam=120, color=MAGENTA)], sfx=[(0.1, "subida", -20, {"dur": d * 0.7})])


@v.plano(115, "se suman los dos horizontes: dos líneas de mirada que se tocan sobre el mar")
def _(d):
    return P(OSC, [estrellas(50, 10), arco(), IMG("montana", ancho=240, x=330, y=ARCO_Y - 20, z=0.5), IMG("montana", ancho=220, x=760, y=ARCO_Y - 10, z=0.5),
                   flecha([[330, ARCO_Y - 110], [545, ARCO_Y - 4]], 0.05, d * 0.45, LIMA, 7, z=0.6), flecha([[760, ARCO_Y - 100], [555, ARCO_Y - 4]], d * 0.35, d * 0.8, MAGENTA, 7, z=0.6),
                   senala(550, ARCO_Y, d * 0.8, d - 0.05, 50, AMBAR)],
             cam(1.0, 1.06, (540, 1400)), "corte", hud=[rotulo(0.2, d - 0.05, "+", tam=200, color="#ffffff", capsula=None, y=1000)], sfx=[(d * 0.8, "ding", -18)])


@v.plano(120, "y aunque haya un mar en medio: olas del Mediterráneo")
def _(d):
    return P(CIELO, [BG("bg_playa"), polvo("#ffffff", 30, (0, 1000, 1080, 1540), 11)], cam(1.4, 1.5, (540, 1150), (600, 1150)), "corte", sfx=[(0.05, "ola", -18)])


@v.plano(127, "África se ve: el montañero ante el horizonte con el Rif")
def _(d):
    return P(CIELO, [vista(True), IMG("excursionista", ancho=480, x=540, y=1560, z=0.6, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 1.05}]), senala(540, 940, 0.1, d - 0.1, 140, MAGENTA)],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[rotulo(0.15, d - 0.05, "ÁFRICA", tam=130, color="#ffffff", capsula="#c0397ae6", y=560)], sfx=[(0.05, "impacto", -16)])


@v.plano(130, "¿y el nombre?: la cumbre")
def _(d):
    return P(CIELO, [BG("bg_cumbre"), nieve(25, 12)], cam(1.2, 1.3, (560, 950)), "corte",
             hud=[amarillo(0.1, d - 0.05, "¿EL NOMBRE?", y=560, tam=120, color="#ffd23f")], sfx=[(0.05, "roce", -20)])


@v.plano(133, "viene de Muley Hacén, un rey de Granada: aparece la corona")
def _(d):
    return P(["#2a1a0a", "#0a0604"], [brillo(540, 1100, 600, "#ffd23f", 0.4, 0.06), IMG("corona", ancho=620, x=540, y=1100, z=0.5, keys=aparece(0.05) + [{"t": d, "rot": 3}])],
             cam(1.0, 1.06, (540, 1100)), "corte", hud=[rotulo(0.08, d - 0.03, "MULEY HACÉN", tam=96, color="#141414", capsula="#ffd23fe6", y=560)], sfx=[(0.05, "brillo", -18)])


@v.plano(141, "cuenta la leyenda: la corona flota sobre la cumbre con niebla")
def _(d):
    return P(CIELO, [BG("bg_cumbre"), IMG("corona", ancho=360, x=560, y=620, z=0.5, op=0.85, keys=[{"t": 0, "y": 660}, {"t": d, "y": 600, "ease": "suave"}]), nieve(40, 13)],
             cam(1.0, 1.05, (540, 900)), "desenfoque", hud=[amarillo(0.2, d - 0.05, "LEYENDA", y=1250, tam=110, color=AMBAR)], sfx=[(0.05, "rumor", -20, {"dur": d})])


@v.plano(146, "que lo enterraron ahí arriba, bajo la nieve: el montón de piedras nevado en la cima")
def _(d):
    return P(CIELO, [BG("bg_cumbre"), IMG("lapida_nieve", ancho=700, x=540, y=1250, z=0.5, keys=aparece(0.05)), nieve(60, 14)],
             cam(1.0, 1.08, (540, 1150)), "corte", sfx=[(0.1, "rumor", -18, {"dur": d})])


@v.plano(152, "desde su tumba, se ve otro continente: vista al sur con el Rif (bucle con el principio)")
def _(d):
    return P(CIELO, [vista(True), IMG("lapida_nieve", ancho=520, x=300, y=1700, z=0.6), senala(540, 940, 0.3, d - 0.3, 140, MAGENTA), nieve(30, 15)],
             cam(1.0, 1.06, (540, 1100)), "corte", sfx=[(0.1, "brillo", -20), (d * 0.6, "ding", -22)])


# ------------------------------------------------------------------ micro planos (ritmo)
@v.plano(8, "micro: «Mulhacén», el vértice de piedra de cerca")
def _(d):
    return P(CIELO, [BG("bg_cumbre")], cam(2.4, 2.6, (560, 830)), "corte", sfx=[(0.02, "pop", -20)])


@v.plano(39, "micro: «montañas», las sierras lejanas de cerca")
def _(d):
    return P(CIELO, [vista(True)], cam(2.2, 2.4, (400, 960), (600, 960)), "corte", sfx=[(0.02, "roce", -22)])


@v.plano(64, "micro: «setenta», los ojos")
def _(d):
    return P(OSC, [IMG("ojo_simple", ancho=860, x=540, y=1050, z=0.5, keys=late(0.05, 1))], cam(1.0, 1.06, (540, 1050)), "corte", sfx=[(0.02, "pop", -20)])


@v.plano(99, "micro: «doscientos», cifra enorme")
def _(d):
    return P(OSC, [brillo(540, 1000, 500, "#2ff3ff", 0.4, 0.06)], cam(1.0, 1.1, (540, 1000)), "corte",
             hud=[rotulo(0.0, d - 0.02, "200 KM", tam=220, color="#141414", capsula="#7df9ffe6", y=1000)], sfx=[(0.0, "golpe", -16)])


@v.plano(138, "micro: «rey», la corona late")
def _(d):
    return P(["#2a1a0a", "#0a0604"], [brillo(540, 1100, 600, "#ffd23f", 0.5, 0.06), IMG("corona", ancho=700, x=540, y=1100, z=0.5, keys=late(0.0, 1))],
             cam(1.1, 1.15, (540, 1100)), "corte", sfx=[(0.02, "ding", -20)])


v.construir("2026-11-20-tarde-02-mulhacen-africa", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 72, "db": -13},
            claves=["África", "Mulhacén", "Granada", "metros", "alto", "península", "claro", "sur", "Mediterráneo", "Rif", "Marruecos", "continente", "curva",
                    "playa", "setenta", "horizonte", "cinco", "esconde", "subes", "doscientos", "asoman", "suman", "mar", "nombre", "rey", "leyenda", "nieve", "tumba"])
