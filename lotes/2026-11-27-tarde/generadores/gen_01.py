"""01 · Aquí anochece dos veces (Burj Khalifa) — método denso, estilo del vídeo largo. Lote 2026-11-27-tarde (Agente 20:00 (Jorge)).
Uso: python3 gen_01.py DIR_SALIDA [01-locucion.mp3 01-alineacion.json]"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import comun_1127t as C  # noqa: E402
from comun_1127t import *  # noqa: E402,F401,F403
import ilus_1127t  # noqa: E402

SVG = ilus_1127t.generar(os.path.join(sys.argv[1], "_svg_lote"))
C.SVG_DIR = SVG
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "01-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)
TARDE = ["#5a3a6a", "#ff9a50"]
NOCHE = ["#060818", "#3a2a4a"]
ESP = ["#02030a", "#0a1030"]
CIAN, LIMA = "#2ff3ff", "#5dff8a"


def cielo(sol_y0=1180, sol_y1=None, d=1.0, noche=False, sol=True, x_sol=760):
    """Cielo + sol (que puede bajar) + ciudad delante: el sol se esconde detrás del horizonte."""
    els = [BG("bg_cielo_noche_dubai" if noche else "bg_cielo_dubai")]
    if sol:
        ks = [{"t": 0, "y": sol_y0}] + ([{"t": d, "y": sol_y1, "ease": "lineal"}] if sol_y1 is not None else [])
        els.append(OB("sol_poniente", x_sol, sol_y0, 560, z=0.2, keys=ks))
    els.append(OB("skyline_noche" if noche else "skyline_dubai", 540, 1560, 1100, z=0.6))
    return els


def torre_el(x=420, ancho=330, noche=False, keys=None, z=0.45, base=1640):
    alto = ancho * 1900 / 480
    return OB("torre_noche" if noche else "torre", x, base - alto / 2, ancho, z=z, keys=keys)


@v.plano(0, "gancho: la torre enorme y el sol que se esconde detrás de la ciudad mientras arriba sigue brillando")
def _(d):
    return P(TARDE, cielo(1250, 1500, d) + [torre_el(420, 360), brillo(420, 300, 160, "#ffd080", 0.6, 0.5, keys=late(0.2, 3, 0.1, 0.5))],
             cam(1.0, 1.06, (500, 1000)), vineta=0.35, sfx=[(0.0, "whoosh", -16), (0.6, "brillo", -18)])


@v.plano(4, "esto es el Burj Khalifa: la cámara sube por la torre")
def _(d):
    return P(TARDE, cielo(1300) + [torre_el(540, 420)], cam(1.15, 1.15, (540, 1500), (540, 500)), "corte",
             hud=[cap(0.3, d - 0.05, "DUBÁI", "#ffffff", "#c0392be6", 110, y=1500)], sfx=[(0.1, "whoosh", -20)])


@v.plano(11, "ochocientos veintiocho metros: contador junto a la aguja")
def _(d):
    return P(TARDE, cielo(1300) + [torre_el(400, 360), flecha([[700, 1600], [700, 260]], 0.05, 0.6, AMBAR, 10, z=0.7)],
             cam(1.0, 1.04, (540, 960)), "corte",
             hud=[contador(0.05, d - 0.05, 0, 828, 0.8, " M", tam=130, color="#141414", capsula="#ffd23fe6", y=900, x=760)], sfx=[(0.05, "tic", -18)])


@v.plano(14, "el edificio más alto del mundo: personas diminutas al pie")
def _(d):
    S = 1600
    return P(TARDE, cielo(1300) + [torre_el(540, 380), PZ("voluntario_2", 330, S + 40, 120, z=0.7, keys=aparece(0.1)), PZ("mira_sol", 760, S + 40, 120, z=0.7, keys=aparece(0.2))],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.3, d - 0.05, "EL MÁS ALTO", "#141414", "#7df9ffe6", 100)], sfx=[(0.2, "pop", -22)])


@v.plano(20, "¿y sabes qué pasa arriba?: la cámara mira la punta brillante")
def _(d):
    return P(TARDE, cielo(1250) + [torre_el(540, 420), brillo(540, 240, 200, "#ffd080", 0.7, 0.5, keys=late(0.0, 2, 0.12, 0.4))],
             cam(1.5, 1.6, (540, 600)), "corte", hud=[amarillo(0.05, d - 0.05, "¿ARRIBA?", y=1200, tam=130, color=AMBAR)], sfx=[(0.05, "impacto", -20)])


@v.plano(25, "que el atardecer dura más: el sol baja muy despacio")
def _(d):
    return P(TARDE, cielo(1150, 1300, d) + [torre_el(300, 300)], cam(1.0, 1.05, (640, 1150)), "desenfoque",
             hud=[cap(0.3, d - 0.05, "DURA MÁS", "#141414", "#ffd23fe6", 110)], sfx=[(0.1, "brillo", -20)])


@v.plano(30, "la Tierra es curva: el arco del planeta")
def _(d):
    return P(ESP, [estrellas(90, 6), OB("arco_tierra", 540, 1350, 1300, keys=[{"t": 0, "rot": -3}, {"t": d, "rot": 3}])],
             cam(1.0, 1.05, (540, 1250)), "corte", hud=[amarillo(0.1, d - 0.05, "CURVA", y=700, tam=130, color=CIAN)], sfx=[(0.1, "whoosh", -20)])


@v.plano(34, "cuanto más alto subes, más lejos queda el horizonte: dos líneas de mirada, abajo corta y arriba larga")
def _(d):
    # observador bajo (x 300, y 1180) y alto (x 300, y 820) sobre el arco
    return P(ESP, [estrellas(80, 7), OB("arco_tierra", 540, 1500, 1500), OB("torre", 300, 1040, 70, z=0.6),
                   flecha([[300, 1235], [560, 1255]], 0.1, 0.4, LIMA, 9, z=0.7),
                   flecha([[300, 860], [1020, 1250]], min(0.6, d * 0.4), min(1.1, d * 0.7), AMBAR, 11, z=0.7)],
             cam(1.0, 1.04, (560, 1100)), "corte",
             hud=[cap(min(0.6, d * 0.4), d - 0.05, "MÁS LEJOS", "#141414", "#ffd23fe6", 100, y=640)], sfx=[(0.1, "tic", -20), (min(0.6, d * 0.4), "whoosh", -18)])


@v.plano(43, "y el sol tarda más en esconderse: el sol roza el horizonte y se queda")
def _(d):
    return P(TARDE, cielo(1330, 1380, d), cam(1.1, 1.15, (700, 1300)), "corte", sfx=[(0.1, "brillo", -22)])


@v.plano(50, "abajo ya es de noche: la base se apaga y se encienden las ventanas")
def _(d):
    return P(NOCHE, cielo(0, sol=False, noche=True) + [torre_el(540, 400, noche=True)], cam(1.2, 1.25, (540, 1450)), "corte",
             hud=[cap(0.2, d - 0.05, "ABAJO: NOCHE", "#ffffff", "#2a5ae8e6", 96, y=1000)], sfx=[(0.1, "pop", -22)])


@v.plano(55, "pero en las plantas altas el sol sigue brillando: la punta encendida")
def _(d):
    return P(NOCHE, cielo(0, sol=False, noche=True) + [torre_el(540, 400, noche=True), brillo(540, 380, 260, "#ffb060", 0.8, 0.5, keys=late(0.1, 2, 0.1, 0.4))],
             cam(1.25, 1.3, (540, 700), (540, 600)), "corte", hud=[cap(0.3, d - 0.05, "ARRIBA: SOL", "#141414", "#ffd23fe6", 100, y=1300)], sfx=[(0.1, "brillo", -18)])


@v.plano(64, "tanto, que en Ramadán: luna creciente sobre la ciudad")
def _(d):
    return P(NOCHE, cielo(0, sol=False, noche=True) + [OB("luna_creciente", 700, 700, 300, z=0.3, keys=aparece(0.0) + flota(d, 10, 700))],
             cam(1.0, 1.05, (540, 1000)), "corte", hud=[cap(0.3, d - 0.05, "RAMADÁN", "#ffffff", "#2a5ae8e6", 110)], sfx=[(0.1, "brillo", -20)])


@v.plano(68, "cuando el ayuno se rompe al ponerse el sol: dátiles y agua")
def _(d):
    return P(TARDE, [BG("bg_cielo_dubai"), OB("datiles", 540, 1200, 860, keys=aparece(0.0))], cam(1.0, 1.06, (540, 1150)), "corte",
             sfx=[(0.1, "pop", -22)])


@v.plano(77, "las autoridades religiosas de Dubái dieron una regla aparte: documento que se firma")
def _(d):
    return P(TARDE, [BG("bg_cielo_dubai"), OB("pergamino", 540, 1150, 600, keys=aparece(0.0) + [{"t": 0, "rot": -4}, {"t": d, "rot": 2}])],
             cam(1.0, 1.05, (540, 1100)), "corte", hud=[cap(0.4, d - 0.05, "REGLA APARTE", "#141414", "#7df9ffe6", 96)], sfx=[(0.3, "roce", -20)])


@v.plano(86, "de la planta ochenta a la ciento cincuenta: franja que se ilumina en la torre")
def _(d):
    return P(NOCHE, cielo(0, sol=False, noche=True) + [torre_el(420, 380, noche=True),
             {"tipo": "forma", "forma": "rect", "ancho": 130, "alto": 380, "relleno": "#ffd23f", "x": 420, "y": 900, "z": 0.5,
              "keys": [{"t": 0, "op": 0}, {"t": 0.3, "op": 0.35}]}],
             cam(1.0, 1.05, (540, 1000)), "corte",
             hud=[cap(0.2, d - 0.05, "PLANTAS 80–150", "#141414", "#ffd23fe6", 84, x=760, y=900)], sfx=[(0.3, "tic", -20)])


@v.plano(94, "dos minutos más: contador")
def _(d):
    return P(NOCHE, cielo(0, sol=False, noche=True) + [torre_el(420, 380, noche=True)], cam(1.05, 1.08, (540, 1000)), "corte",
             hud=[cap(0.05, d - 0.05, "+2 MIN", "#141414", "#5dff8ae6", 130, y=1000, x=540)], sfx=[(0.1, "ding", -18)])


@v.plano(97, "por encima, tres: la punta, tres minutos")
def _(d):
    return P(NOCHE, cielo(0, sol=False, noche=True) + [torre_el(420, 380, noche=True), brillo(420, 420, 160, "#ffb060", 0.8, 0.5)],
             cam(1.2, 1.25, (500, 700)), "corte", hud=[cap(0.05, d - 0.05, "3 MIN", "#141414", "#ffd23fe6", 140, y=1100, x=760)], sfx=[(0.05, "ding", -16)])


@v.plano(100, "y al amanecer, al revés: el sol asoma primero en la punta")
def _(d):
    return P(["#1c1838", "#ff9a50"], [BG("bg_amanecer"), torre_el(540, 400, keys=[{"t": 0, "op": 0.7}, {"t": d, "op": 1}]),
                                      brillo(540, 300, 220, "#ffe0a0", 0.8, 0.5, keys=[{"t": 0, "op": 0}, {"t": d * 0.6, "op": 1}])],
             cam(1.0, 1.05, (540, 1000)), "desenfoque", hud=[cap(0.3, d - 0.05, "SALE ANTES", "#141414", "#ffd23fe6", 100, y=1350)], sfx=[(0.2, "brillo", -18)])


@v.plano(110, "ahora, el truco")
def _(d):
    return P(TARDE, cielo(1250) + [torre_el(540, 420)], cam(1.1, 1.15, (540, 900)), "corte",
             hud=[amarillo(0.05, d - 0.05, "EL TRUCO", y=1000, tam=140, color=AMBAR)], sfx=[(0.05, "impacto", -16)])


@v.plano(113, "el ascensor sube a diez metros por segundo: la cabina sube con estela")
def _(d):
    return P(["#1a2236", "#0a0e1a"], [BG("bg_cielo_dubai"), OB("ascensor", 540, 1300, 460, keys=[{"t": 0, "y": 1500}, {"t": d, "y": 900, "ease": "suave"}]),
                                      flecha([[540, 1750], [540, 1150]], 0.0, d * 0.8, CIAN, 14, disc=[30, 20], punta=False, z=0.4)],
             cam(1.0, 1.04, (540, 1150)), "corte",
             hud=[contador(0.1, d - 0.05, 0, 10, 0.5, " M/S", tam=120, color="#141414", capsula="#7df9ffe6", y=640)], sfx=[(0.1, "whoosh", -16)])


@v.plano(121, "planta ciento veinticuatro en un minuto: el contador de plantas corre")
def _(d):
    return P(TARDE, cielo(1250) + [torre_el(420, 380), OB("ascensor", 420, 1400, 60, z=0.6, keys=[{"t": 0, "y": 1450}, {"t": d, "y": 640, "ease": "suave"}])],
             cam(1.0, 1.04, (540, 1000)), "corte",
             hud=[contador(0.05, d - 0.05, 1, 124, max(0.5, d * 0.8), "", miles=False, tam=130, color="#141414", capsula="#ffd23fe6", y=900, x=780),
                  cap(min(1.0, d * 0.5), d - 0.05, "1 MINUTO", "#ffffff", "#c0392be6", 90, y=1150, x=780)], sfx=[(0.05, "tic", -20)])


@v.plano(127, "así que, en teoría, podrías ver ponerse el sol en la calle: persona mirando el sol que se esconde")
def _(d):
    S = 1640
    return P(TARDE, cielo(1350, 1500, d) + [PZ("mira_sol", 420, S, 620, z=0.7)], cam(1.0, 1.05, (540, 1300)), "corte",
             hud=[cap(0.3, d - 0.05, "EN LA CALLE", "#141414", "#ffd23fe6", 100, y=640)], sfx=[(0.1, "pop", -22)])


@v.plano(139, "subir corriendo: el ascensor dispara hacia arriba")
def _(d):
    return P(["#1a2236", "#0a0e1a"], [BG("bg_cielo_dubai"), OB("ascensor", 540, 1300, 520, keys=[{"t": 0, "y": 1700}, {"t": d, "y": 600, "ease": "entrada"}])],
             cam(1.0, 1.0, (540, 1100)), "corte", sfx=[(0.05, "whoosh", -14)])


@v.plano(141, "y verlo ponerse otra vez: desde arriba, el sol vuelve a estar sobre el horizonte y baja")
def _(d):
    return P(TARDE, cielo(1250, 1480, d) + [OB("cara_mirador", 300, 1250, 560, z=0.7, keys=aparece(0.0))], cam(1.0, 1.05, (600, 1200)), "corte",
             hud=[amarillo(0.2, d - 0.05, "OTRA VEZ", y=640, tam=130, color=AMBAR)], sfx=[(0.1, "brillo", -16), (0.2, "impacto", -20)])


@v.plano(146, "¿lo intentarías? (bucle): la torre con el sol escondiéndose, como al principio")
def _(d):
    return P(TARDE, cielo(1250, 1400, d) + [torre_el(420, 360)], cam(1.0, 1.06, (500, 1000)), "corte", sfx=[(0.05, "ding", -20)])


def micro(fondo, els, txt=None, col="#ffffff", cap_f="#c0392be6", sfx="pop"):
    def fn(d):
        return P(fondo, els(d), cam(1.15, 1.3, (540, 1000)), "corte", hud=[cap(0.0, d - 0.02, txt, col, cap_f, 120)] if txt else [], sfx=[(0.01, sfx, -18)])
    return fn


v.plano(19, "micro: el sol enorme")(micro(TARDE, lambda d: [BG("bg_cielo_dubai"), OB("sol_poniente", 540, 1050, 1000)], sfx="brillo"))
v.plano(47, "micro: el disco medio escondido")(micro(TARDE, lambda d: cielo(1420, 1460, d), sfx="tic"))
v.plano(73, "micro: la luna")(micro(NOCHE, lambda d: [BG("bg_cielo_noche_dubai"), OB("luna_creciente", 540, 1000, 700)], sfx="brillo"))
v.plano(92, "micro: 150")(micro(NOCHE, lambda d: [BG("bg_cielo_noche_dubai"), torre_el(540, 420, noche=True)], "150", "#141414", "#ffd23fe6", "impacto"))
v.plano(117, "micro: 10 m/s")(micro(["#1a2236", "#0a0e1a"], lambda d: [BG("bg_cielo_dubai"), OB("ascensor", 540, 1100, 700)], sfx="whoosh"))


v.construir("2026-11-27-tarde-01-anochece-dos-veces", version=2, bucle=0.35, musica={"generar": "curiosidad", "semilla": 1271, "db": -13},
            claves=["anochece", "dos", "Burj", "Khalifa", "Dubái", "metros", "alto", "atardecer", "curva", "horizonte", "noche", "sol",
                    "Ramadán", "regla", "ochenta", "cincuenta", "minutos", "tres", "amanecer", "truco", "ascensor", "minuto", "otra"],
            ep_extra={"sfx_bajo_voz": True})
