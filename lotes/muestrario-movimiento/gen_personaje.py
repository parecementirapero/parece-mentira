"""Muestra del experimento H6 (motor/APRENDIZAJE.md): el mismo arranque de la Luna, con un personaje que reacciona.
Uso: python3 gen_personaje.py DIR  →  python3 -m motor.render DIR/episodio.json --salida DIR/out   (sin voz)"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403

v = Video(sys.argv[1], os.path.join(AQUI, "guion_personaje.txt"))


@v.plano(0, "se mira las uñas")
def _(d):
    return P(["#2a1a14", "#120a08"], [brillo(540, 650, 700, "#ffcf9a", 0.5), estrellas(20, 9), luna(820, 420, 150, 0.2),
             *reaccion(540, 1180, 820, [(0, "neutral"), (d * 0.45, "pensando")])],
             cam(1.1, 1.18, (540, 1000), (540, 950)), vineta=0.7, sfx=[(d * 0.45, "pop", -16)])


@v.plano(3, "la Luna se va: sorpresa")
def _(d):
    return P(ESPACIO, [BG("bg_esp_violeta"), estrellas(), tierra(250, 1500, 520, giro=6),
             luna(0, 0, 230, 0.5, keys=lanza(0.2, d * 0.8, (620, 760), (900, 420))), *lineas_vel(820, 600, 2),
             flecha([[520, 900], [800, 520]], 0.25, d * 0.8, CIAN, 9, [20, 14]),
             *reaccion(800, 1420, 460, [(0, "pensando"), (d * 0.3, "sorpresa")], z=0.8, espejo=True)],
             cam(1.0, 1.06, (500, 1000), (580, 900)), "desenfoque", sfx=[(d * 0.3, "subida", -20, {"dur": 0.5}), (d * 0.3, "pop", -15)])


@v.plano(9, "misma velocidad: señala")
def _(d):
    return P(ESPACIO, [BG("bg_esp_petroleo"), estrellas(25, 4), IMG("dedo", ancho=330, x=760, y=1050, z=0.5, keys=K(d, (0, {"ey": 1.0}), (1, {"ey": 1.1}))),
             luna(0, 620, 150, 0.5, keys=K(d, (0, {"x": 640, "ease": "lineal"}), (1, {"x": 900}))),
             *reaccion(270, 1330, 500, [(0, "senala")], z=0.8)], cam(1.0, 1.05), "zoom")


@v.plano(17, "3,8 cm: feliz")
def _(d):
    return P(ESPACIO, [BG("bg_esp_petroleo"), estrellas(25, 5), IMG("regla", ancho=1000, x=540, y=800, z=0.5),
             luna(0, 600, 120, 0.56, keys=K(d, (0.05, {"x": 260}), (0.6, {"x": 625, "ease": "salida"}))),
             *reaccion(540, 1400, 560, [(0, "sorpresa"), (d * 0.5, "feliz")], z=0.8)],
             cam(1.0, 1.06), hud=[{**contador(0.1, d - 0.1, 0, 3.8, d * 0.5, "CM", tam=110, y=1000), "decimales": 1}])


v.construir("muestrario-personaje", version=1, bucle=0.3, claves=["uñas", "Luna", "centímetros"])
