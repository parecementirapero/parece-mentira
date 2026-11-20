"""01 · POV, atardece en Marte (el atardecer azul) — método denso. Lote 2026-11-19-tarde (Agente 20:00, Jorge).
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_1119t  # noqa: E402

SVG = ilus_1119t.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

OCRE = ["#1a1016", "#a87048"]
DIA = ["#b8784a", "#5a2410"]
NOCHE = ["#060814", "#1a2238"]
AZUL = "#7ec8ff"
SOLX, SOLY = 540, 1110


def halo(t0=0.0, i=0.85, r=520, pulso=True):
    return brillo(SOLX, SOLY, r, AZUL, i, 0.07, pulso=[0.12, 0.6] if pulso else None, keys=[{"t": t0, "op": 0}, {"t": t0 + 0.5, "op": 1}])


def tormenta(T0, T1, d):
    return IMG("tormenta_polvo", ancho=1500, z=0.25, op=0.7, keys=recorrido(T0, T1, (1300, 1250), (-200, 1150), d))


# ================================================================== PLANOS
@v.plano(0, "gancho: el Sol rosado baja hacia la cresta y el halo azul se enciende alrededor")
def _(d):
    return P(OCRE, [BG("bg_marte_atardecer"), brillo(SOLX, SOLY, 560, AZUL, 0.9, 0.07, keys=[{"t": 0, "radio": 300}, {"t": d, "radio": 620, "ease": "suave"}]),
             IMG("sol_marte", ancho=520, x=SOLX, z=0.08, keys=[{"t": 0, "y": 760, "escala": 1.15}, {"t": 0.4, "y": 820, "ease": "elastico"}, {"t": d, "y": 1060, "escala": 1.0, "ease": "suave"}]),
             polvo("#ffd8b0", 30, (0, 900, 1080, 1800), 3)],
             cam(1.0, 1.06, (540, 1000), (540, 1060)), vineta=0.6, sfx=[(0.02, "whoosh", -14, {"dur": 0.6}), (0.4, "brillo", -16)])


@v.plano(4, "y el cielo se vuelve azul: el día se apaga y el halo crece")
def _(d):
    return P(OCRE, [BG("bg_marte_atardecer"), BG("bg_marte_dia", z=0.06) | {"keys": [{"t": 0, "op": 1}, {"t": d * 0.7, "op": 0, "ease": "suave"}]},
             halo(0.1), IMG("sol_marte", ancho=360, x=SOLX, z=0.08, keys=[{"t": 0, "y": 980}, {"t": d, "y": 1090, "ease": "suave"}])],
             cam(1.0, 1.08, (540, 1050)), "corte", hud=[amarillo(0.3, d - 0.05, "AZUL", y=600, tam=150, color=AZUL)], sfx=[(0.1, "subida", -18, {"dur": 1.0})])


@v.plano(10, "en la Tierra: atardecer naranja sobre el mar, el Sol se hunde")
def _(d):
    return P(["#2a3a7a", "#1a1a3a"], [BG("bg_tierra_atardecer"), IMG("sol_tierra", ancho=560, x=540, z=0.1, keys=[{"t": 0, "y": 1050}, {"t": d, "y": 1180, "ease": "suave"}]),
             polvo("#ffe0a0", 20, (0, 1200, 1080, 1800), 5)],
             cam(1.0, 1.06, (540, 1100)), "desenfoque", hud=[contexto(0.05, d - 0.05, "EN LA TIERRA")], sfx=[(0.1, "ola", -22, {"dur": 1.2})])


@v.plano(15, "son naranjas: el disco de cerca, enorme y amarillo")
def _(d):
    return P(["#2a3a7a", "#1a1a3a"], [BG("bg_tierra_atardecer"), IMG("sol_tierra", ancho=900, x=540, y=1160, z=0.12, keys=late(0.1, 1, 0.06, 0.5))],
             cam(1.4, 1.5, (540, 1160)), "corte", hud=[rotulo(0.15, d - 0.03, "NARANJAS", tam=110, color="#ffffff", capsula="#c05a1ae6", y=640)], sfx=[(0.1, "pop", -20)])


@v.plano(17, "en Marte, al revés: el planeta rojo gira y entra")
def _(d):
    return P(NOCHE, [BG("bg_espacio"), estrellas(60, 2), IMG("marte_planeta", ancho=820, x=540, y=1120, z=0.4, anim={"girar": 10},
             keys=[{"t": 0, "escala": 0.5, "rot": -40}, {"t": 0.4, "escala": 1.0, "rot": 0, "ease": "elastico"}, {"t": d, "escala": 1.05}])],
             cam(1.0, 1.05), "desenfoque", hud=[rotulo(0.3, d - 0.05, "AL REVÉS", tam=110, color="#141414", capsula="#ffd23fe6", y=600)], sfx=[(0.05, "whoosh", -16, {"dur": 0.5})])


@v.plano(21, "de día el cielo tiene color de óxido: el rover avanza por las dunas")
def _(d):
    return P(DIA, [BG("bg_marte_dia"), IMG("rover", ancho=760, z=0.55, keys=[{"t": 0, "x": 300, "y": 1500}, {"t": d, "x": 560, "y": 1500, "ease": "lineal"}], anim={"flotar": [3, 0.4]}),
             polvo("#e0a874", 40, (0, 1300, 1080, 1800), 7)],
             cam(1.0, 1.05, (500, 1200)), "corte", hud=[amarillo(d * 0.5, d - 0.03, "ÓXIDO", y=620, tam=130, color="#ffb070")], sfx=[(0.05, "roce", -22), (d * 0.5, "pop", -20)])


@v.plano(29, "al bajar el Sol: el disco desciende hacia la cresta")
def _(d):
    return P(OCRE, [BG("bg_marte_atardecer"), BG("bg_marte_dia", z=0.06) | {"op": 0.5},
             IMG("sol_marte", ancho=320, x=SOLX, z=0.08, keys=[{"t": 0, "y": 700}, {"t": d, "y": 1080, "ease": "suave"}]),
             flecha([[760, 700], [760, 1000]], 0.1, d * 0.8, AZUL, 8, disc=[16, 12], z=0.6)],
             cam(1.0, 1.05, (540, 900), (540, 1050)), "corte", sfx=[(0.1, "subida", -20, {"dur": 0.9})])


@v.plano(34, "se enciende un halo azul a su alrededor: el anillo marca el halo")
def _(d):
    return P(OCRE, [BG("bg_marte_atardecer"), halo(0.0, 1.0, 600), IMG("sol_marte", ancho=300, x=SOLX, y=SOLY - 10, z=0.08), senala(SOLX, SOLY, 0.3, d - 0.1, 230, CIAN)],
             cam(1.3, 1.45, (540, 1100)), "corte", hud=[rotulo(0.2, d - 0.05, "HALO AZUL", tam=104, color="#141414", capsula="#7ec8ffe6", y=600)], sfx=[(0.1, "brillo", -16), (0.3, "pop", -20)])


@v.plano(42, "lo fotografió el rover: el rover entra y gira el mástil")
def _(d):
    return P(OCRE, [BG("bg_marte_atardecer"), halo(0, 0.7, 420, False), IMG("rover", ancho=860, z=0.55, keys=arranque(540, 1450, d, "derecha", 300, 30))],
             cam(1.0, 1.05, (540, 1250)), "corte", sfx=[(0.05, "roce", -18)])


@v.plano(46, "micro: Curiosity, la cámara del mástil hace la foto", mas=0.03)
def _(d):
    return P(OCRE, [BG("bg_marte_atardecer"), IMG("rover", ancho=1700, x=420, y=1600, z=0.55),
             fundido_blanco([{"t": 0, "op": 0}, {"t": 0.12, "op": 0.6}, {"t": 0.4, "op": 0}], "#e8f4ff")],
             cam(1.0, 1.06, (540, 1100)), "corte", sfx=[(0.1, "zap", -16)])


@v.plano(47, "el quince de abril de dos mil quince: la foto azul cae girando")
def _(d):
    return P(NOCHE, [BG("bg_marte_atardecer", z=0.05) | {"op": 0.4}, IMG("foto_azul", ancho=640, x=540, z=0.5, keys=cae(0.0, 0.6, 500, 1100) + [{"t": 0, "rot": -14}, {"t": 0.6, "rot": -4}]),
             IMG("foto_dia", ancho=420, x=820, y=1500, z=0.4, keys=[{"t": 0, "rot": 12, "op": 0}, {"t": 0.4, "op": 1}, {"t": d, "rot": 8}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[rotulo(0.4, d - 0.05, "15 · ABRIL · 2015", tam=84, color="#141414", capsula="#ffd23fe6", y=600)], sfx=[(0.4, "golpe", -18)])


@v.plano(55, "desde el cráter Gale: vista amplia, el rover pequeño en el fondo del cráter")
def _(d):
    return P(DIA, [BG("bg_marte_dia"), IMG("rover", ancho=260, z=0.5, keys=[{"t": 0, "x": 460, "y": 1560}, {"t": d, "x": 620, "y": 1560}]), senala(540, 1540, 0.3, d - 0.1, 170, CIAN)],
             cam(1.08, 1.0, (540, 1200)), "corte", hud=[contexto(0.05, d - 0.05, "CRÁTER GALE")], sfx=[(0.3, "pop", -20)])


@v.plano(59, "¿por qué azul? la foto azul late")
def _(d):
    return P(NOCHE, [BG("bg_marte_atardecer", z=0.05) | {"op": 0.35}, IMG("foto_azul", ancho=780, x=540, y=1150, z=0.5, keys=late(0.1, 2, 0.06, 0.4) + [{"t": 0, "rot": -3}])],
             cam(1.0, 1.05, (540, 1150)), "corte", hud=[amarillo(0.05, d - 0.03, "¿POR QUÉ?", y=600, tam=130, color=CIAN)], sfx=[(0.1, "pop", -18)])


@v.plano(62, "por el polvo: la nube de polvo barre el paisaje")
def _(d):
    return P(DIA, [BG("bg_marte_dia"), IMG("tormenta_polvo", ancho=1600, z=0.5, keys=[{"t": 0, "x": 1400, "y": 1200}, {"t": d, "x": 500, "y": 1150, "ease": "salida"}]),
             polvo("#e0a874", 80, (0, 600, 1080, 1800), 9)],
             cam(1.0, 1.06, (540, 1150), temblor=2), "corte", hud=[amarillo(0.15, d - 0.03, "POLVO", y=600, tam=140, color="#ffb070")], sfx=[(0.05, "rumor", -14, {"dur": 1.0})])


@v.plano(65, "en el aire marciano flota un polvo finísimo: granos que flotan en un rayo de luz")
def _(d):
    return P(OCRE, [BG("bg_marte_atardecer", z=0.05) | {"op": 0.6}, brillo(540, 1000, 600, "#ffd8b0", 0.35, 0.06),
             IMG("grano_polvo", ancho=200, x=300, y=900, z=0.5, anim={"flotar": [20, 0.4], "girar": 20}),
             IMG("grano_polvo", ancho=140, x=780, y=1200, z=0.55, anim={"flotar": [26, 0.3], "girar": -30}),
             IMG("grano_polvo", ancho=100, x=500, y=1450, z=0.45, anim={"flotar": [16, 0.5], "girar": 40}),
             polvo("#ffd8b0", 120, (0, 500, 1080, 1700), 11)],
             cam(1.0, 1.08, (540, 1100)), "corte", sfx=[(0.1, "rumor", -24, {"dur": 1.5})])


@v.plano(71, "micro: finísimo, un grano enorme a toda pantalla", mas=0.03)
def _(d):
    return P(["#2a1008", "#120402"], [brillo(540, 1000, 500, "#ffb070", 0.4, 0.06), IMG("grano_polvo", ancho=820, x=540, y=1050, z=0.5, keys=aparece(0.0, 0.3), anim={"girar": 25})],
             cam(1.0, 1.08), "corte", sfx=[(0.02, "pop", -18)])


@v.plano(73, "del tamaño justo: la lupa pasa sobre los granos")
def _(d):
    return P(OCRE, [BG("bg_marte_atardecer", z=0.05) | {"op": 0.5}, polvo("#ffd8b0", 90, (0, 500, 1080, 1700), 13),
             IMG("grano_polvo", ancho=180, x=560, y=1120, z=0.5, anim={"girar": 30}),
             IMG("lupa2", ancho=520, z=0.6, keys=[{"t": 0, "x": 300, "y": 1300}, {"t": d, "x": 620, "y": 1200, "ease": "suave"}])],
             cam(1.0, 1.06, (540, 1150)), "corte", hud=[rotulo(0.2, d - 0.05, "TAMAÑO JUSTO", tam=96, color="#141414", capsula="#ffd23fe6", y=600)], sfx=[(0.1, "roce", -20)])


@v.plano(78, "para que la luz azul lo atraviese mejor: el rayo blanco entra y el azul sigue recto")
def _(d):
    return P(["#0a0c18", "#1a1028"], [IMG("grano_polvo", ancho=260, x=520, y=1100, z=0.5, anim={"girar": 20}),
             IMG("rayo_luz", ancho=1100, x=560, y=1100, z=0.45, keys=[{"t": 0, "ex": 0.05, "x": 60}, {"t": d * 0.6, "ex": 1.0, "x": 560, "ease": "salida"}, {"t": d, "ex": 1.0}]),
             senala(1000, 1100, d * 0.6, d - 0.1, 90, CIAN)],
             cam(1.0, 1.05, (560, 1100)), "corte", hud=[amarillo(0.2, d - 0.03, "EL AZUL PASA", y=620, tam=104, color=CIAN)], sfx=[(0.05, "zap", -18)])


@v.plano(84, "al chocar con él: los colores rebotan y el azul vuelve hacia el Sol")
def _(d):
    return P(OCRE, [BG("bg_marte_atardecer"), IMG("sol_marte", ancho=300, x=SOLX, y=SOLY, z=0.08), halo(0.2, 0.9, 380),
             flecha([[540, 600], [540, 1040]], 0.05, d * 0.6, AZUL, 12, z=0.6),
             flecha([[540, 620], [200, 300]], 0.1, d * 0.7, "#ff5a3a", 10, z=0.6), flecha([[540, 620], [900, 360]], 0.15, d * 0.75, "#ffd23f", 10, z=0.6),
             IMG("grano_polvo", ancho=120, x=540, y=600, z=0.65, keys=late(0.05, 1, 0.2, 0.4))],
             cam(1.0, 1.05, (540, 900)), "corte", sfx=[(0.1, "golpe", -20), (0.3, "brillo", -20)])


@v.plano(88, "el azul se queda junto al Sol: el halo se cierra alrededor del disco")
def _(d):
    return P(OCRE, [BG("bg_marte_atardecer"), brillo(SOLX, SOLY, 400, AZUL, 1.0, 0.07, keys=[{"t": 0, "radio": 700}, {"t": d, "radio": 360, "ease": "suave"}]),
             IMG("sol_marte", ancho=300, x=SOLX, y=SOLY, z=0.08, keys=late(0.3, 1, 0.08, 0.5))],
             cam(1.2, 1.4, (540, 1100)), "corte", hud=[amarillo(0.2, d - 0.03, "JUNTO AL SOL", y=640, tam=104, color=CIAN)], sfx=[(0.1, "brillo", -18)])


@v.plano(95, "el rojo y el amarillo se reparten por el resto del cielo: abanico de flechas")
def _(d):
    fl = [flecha([[540, 1080], [x, y]], 0.05 + i * 0.06, 0.5 + i * 0.06, c, 9, z=0.6)
          for i, (x, y, c) in enumerate([(120, 500, "#ff5a3a"), (320, 380, "#ffd23f"), (760, 380, "#ff5a3a"), (960, 520, "#ffd23f"), (150, 800, "#ffd23f"), (930, 820, "#ff5a3a")])]
    return P(OCRE, [BG("bg_marte_atardecer"), halo(0, 0.7, 380, False), IMG("sol_marte", ancho=280, x=SOLX, y=SOLY, z=0.08), *fl],
             cam(1.0, 1.05, (540, 900)), "corte", hud=[rotulo(0.3, d - 0.05, "ROJO Y AMARILLO", tam=84, color="#141414", capsula="#ffb070e6", y=620)], sfx=[(0.1, "whoosh", -22, {"dur": 0.6})])


@v.plano(107, "¿y cuánto aire hay? dos botes: la Tierra lleno, Marte vacío")
def _(d):
    return P(NOCHE, [BG("bg_espacio"), estrellas(40, 4),
             IMG("aire_tierra", ancho=300, x=330, y=1150, z=0.5, keys=aparece(0.0)), IMG("aire_marte", ancho=300, x=750, y=1150, z=0.5, keys=aparece(0.2)),
             IMG("tierra_hd", ancho=180, x=330, y=1620, z=0.6), IMG("marte_planeta", ancho=180, x=750, y=1620, z=0.6)],
             cam(1.0, 1.05, (540, 1200)), "corte", hud=[amarillo(0.05, d - 0.03, "¿CUÁNTO AIRE?", y=600, tam=100, color=CIAN)], sfx=[(0.05, "pop", -18), (0.25, "pop", -18)])


@v.plano(111, "menos del uno por ciento: el bote de Marte casi vacío, la cifra corre")
def _(d):
    return P(NOCHE, [BG("bg_espacio"), estrellas(40, 4), IMG("aire_tierra", ancho=260, x=280, y=1180, z=0.4, op=0.6),
             IMG("aire_marte", ancho=420, x=700, y=1150, z=0.5, keys=late(0.2, 1, 0.06, 0.5)), senala(700, 1440, 0.4, d - 0.1, 90, MAGENTA)],
             cam(1.0, 1.06, (620, 1150)), "corte", hud=[contador(0.05, d - 0.03, 100, 1, d * 0.7, " %", y=640, tam=150, color="#ffd23f", contar_prefijo="< ")], sfx=[(0.05, "tictac", -22, {"dur": 0.6, "ritmo": 0.08})])


@v.plano(120, "allí el Sol se ve más pequeño: los dos discos lado a lado")
def _(d):
    return P(NOCHE, [BG("bg_espacio"), IMG("sol_tierra", ancho=520, x=300, y=1100, z=0.4), IMG("sol_marte", ancho=360, x=780, y=1100, z=0.45, keys=aparece(0.15)),
             flecha([[560, 1300], [700, 1300]], 0.3, d * 0.8, "#ffffffcc", 6, z=0.6)],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[contexto(0.05, d * 0.5, "TIERRA"), rotulo(d * 0.5, d - 0.05, "MARTE", tam=54, color="#ffffff", capsula="#c0392be6", x=540, y=470)],
             sfx=[(0.15, "pop", -18)])


@v.plano(128, "y su disco, rosado: el Sol de Marte de cerca, latiendo")
def _(d):
    return P(OCRE, [BG("bg_marte_atardecer"), IMG("sol_marte", ancho=900, x=540, y=1050, z=0.3, keys=late(0.1, 2, 0.05, 0.5)), halo(0, 0.6, 560, False)],
             cam(1.0, 1.06, (540, 1050)), "corte", hud=[amarillo(0.1, d - 0.03, "ROSADO", y=600, tam=140, color="#ff9ac0")], sfx=[(0.1, "brillo", -18)])


@v.plano(131, "y el polvo que suben las tormentas: la tormenta se levanta sobre la cresta")
def _(d):
    return P(OCRE, [BG("bg_marte_atardecer"), halo(0, 0.6, 420, False),
             IMG("tormenta_polvo", ancho=1600, x=540, z=0.45, keys=[{"t": 0, "y": 1700, "escala": 0.8}, {"t": d, "y": 1050, "escala": 1.2, "ease": "suave"}]),
             polvo("#e0a874", 80, (0, 700, 1080, 1800), 15)],
             cam(1.0, 1.06, (540, 1150), temblor=1), "corte", hud=[contexto(0.05, d - 0.05, "TORMENTAS")], sfx=[(0.05, "rumor", -15, {"dur": 1.4})])


@v.plano(138, "sigue reflejando luz dos horas o más: el Sol ya se ha ido y el brillo azul sigue")
def _(d):
    return P(["#060814", "#1a1016"], [BG("bg_marte_atardecer"), brillo(SOLX, SOLY + 60, 520, AZUL, 0.6, 0.07, pulso=[0.15, 0.4]),
             polvo("#a8d4ff", 60, (0, 300, 1080, 1100), 17), fugaz(0.3, 900, 300, 600, 520)],
             cam(1.0, 1.06, (540, 1000)), "corte", hud=[rotulo(0.3, d - 0.05, "+2 HORAS", tam=120, color="#141414", capsula="#7ec8ffe6", y=620)], sfx=[(0.3, "ding", -20)])


@v.plano(149, "un atardecer azul en el planeta rojo: el Sol vuelve arriba y baja otra vez (bucle)")
def _(d):
    return P(OCRE, [BG("bg_marte_atardecer"), brillo(SOLX, SOLY, 560, AZUL, 0.9, 0.07, keys=[{"t": 0, "radio": 620}, {"t": d, "radio": 320, "ease": "suave"}]),
             IMG("sol_marte", ancho=520, x=SOLX, z=0.08, keys=[{"t": 0, "y": 1060, "escala": 1.0}, {"t": d, "y": 780, "escala": 1.12, "ease": "suave"}]),
             IMG("rover", ancho=380, x=820, y=1560, z=0.55, op=0.95), polvo("#ffd8b0", 30, (0, 900, 1080, 1800), 3)],
             cam(1.04, 1.0, (540, 1060), (540, 1000)), "corte", hud=[rotulo(0.15, d - 0.45, "EL PLANETA ROJO", tam=96, color="#141414", capsula="#ffd23fe6", y=620)],
             sfx=[(0.1, "impacto", -16), (d * 0.6, "ding", -22)])


@v.plano(52, "micro: dos mil quince, la foto azul a toda pantalla", mas=0.03)
def _(d):
    return P(NOCHE, [IMG("foto_azul", ancho=1000, x=540, y=1050, z=0.5, keys=[{"t": 0, "rot": -6, "escala": 0.9}, {"t": d, "rot": 2, "escala": 1.0, "ease": "salida"}])],
             cam(1.0, 1.06, (540, 1050)), "corte", sfx=[(0.02, "pop", -18)])


@v.plano(101, "micro: se reparten, el cielo entero se tiñe de naranja", mas=0.03)
def _(d):
    return P(DIA, [BG("bg_marte_dia"), brillo(540, 700, 900, "#ffb070", 0.6, 0.07, pulso=[0.2, 0.5]),
             flecha([[100, 900], [980, 500]], 0.0, d * 0.8, "#ff5a3a", 10, z=0.6), flecha([[100, 600], [980, 800]], 0.05, d * 0.85, "#ffd23f", 10, z=0.6)],
             cam(1.0, 1.06, (540, 900)), "corte", sfx=[(0.02, "whoosh", -20, {"dur": 0.4})])


@v.plano(113, "micro: uno, el bote de la Tierra lleno a toda pantalla", mas=0.03)
def _(d):
    return P(NOCHE, [BG("bg_espacio"), IMG("aire_tierra", ancho=520, x=540, y=1100, z=0.5, keys=aparece(0.0, 0.3)), IMG("tierra_hd", ancho=240, x=540, y=1650, z=0.6)],
             cam(1.0, 1.05, (540, 1150)), "corte", sfx=[(0.02, "pop", -18)])


@v.plano(141, "micro: dos horas, el rover a oscuras bajo el resplandor azul", mas=0.03)
def _(d):
    return P(["#060814", "#1a1016"], [BG("bg_marte_atardecer"), brillo(SOLX, SOLY + 60, 480, AZUL, 0.55, 0.07),
             IMG("rover", ancho=900, x=540, y=1480, z=0.55, op=0.85, keys=[{"t": 0, "x": 480}, {"t": d, "x": 560}])],
             cam(1.0, 1.06, (540, 1250)), "corte", sfx=[(0.02, "roce", -22)])


v.construir("2026-11-19-tarde-01-atardecer-azul-marte", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 41, "db": -13},
            claves=["Marte", "azul", "Tierra", "naranjas", "óxido", "halo", "Curiosity", "Gale", "polvo", "finísimo", "tamaño", "luz", "Sol", "rojo", "amarillo",
                    "aire", "uno", "ciento", "pequeño", "rosado", "tormentas", "dos", "horas", "planeta"])
