"""Muestrario de movimiento y sonido (GUIA_CALIDAD §5 y §6): cada plano enseña un helper de `motor.denso`.
A la izquierda, el movimiento lineal de siempre; a la derecha, el mismo con el helper.

Uso: python3 gen.py DIR_SALIDA   →   python3 -m motor.render DIR_SALIDA/episodio.json --salida DIR_SALIDA/out
(sin voz: tiempos provisionales)."""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403

v = Video(sys.argv[1], os.path.join(AQUI, "guion.txt"))
IZQ, DER = 290, 790


def base(d, titulo, els, sfx=(), energia=None, color=CIAN):
    raya = {"tipo": "forma", "forma": "rect", "ancho": 6, "alto": 1100, "relleno": "#ffffff30", "x": 540, "y": 1000, "z": 0.2}
    return P(ESPACIO, [BG("bg_esp_petroleo"), estrellas(30, 5), raya, *els], cam(1.0, 1.03), sfx=sfx, energia=energia,
             hud=[amarillo(0.05, d - 0.05, titulo, y=560, tam=84, color=color),
                  rotulo(0.05, d - 0.05, "ANTES", tam=44, x=IZQ, y=1330, sin_pop=True), rotulo(0.05, d - 0.05, "AHORA", tam=44, x=DER, y=1330, sin_pop=True)])


@v.plano(0, "aparece")
def _(d):
    return base(d, "APARECE", [
        luna(IZQ, 950, 300, keys=[{"t": 0.3, "escala": 0, "op": 0}, {"t": 0.34, "op": 1}, {"t": 0.7, "escala": 1, "ease": "lineal"}]),
        luna(DER, 950, 300, keys=aparece(0.3, 0.5))], sfx=[(0.3, "pop", -14)])


@v.plano(3, "cae")
def _(d):
    return base(d, "CAE Y BOTA", [
        IMG("modulo_lunar", ancho=300, x=IZQ, z=0.5, keys=[{"t": 0.2, "y": 720}, {"t": 1.1, "y": 1050, "ease": "lineal"}]),
        IMG("modulo_lunar", ancho=300, x=DER, z=0.5, keys=[{"t": 0, "y": 720}, *[{**k, "t": k["t"]} for k in cae(0.2, 1.3, 720, 1050, 0.12)]])],
        sfx=[(0.2 + 1.1 * 0.36, "golpe", -12)], color=AMBAR)


@v.plano(8, "lanza")
def _(d):
    return base(d, "TOMA IMPULSO", [
        IMG("cohete", ancho=110, x=IZQ, z=0.5, keys=[{"t": 0.3, "y": 1150}, {"t": 1.2, "y": 800, "ease": "lineal"}]),
        IMG("cohete", ancho=110, z=0.5, keys=lanza(0.3, 1.2, (DER, 1150), (DER, 800)))], sfx=[(0.45, "roce", -14)], color=LIMA)


@v.plano(13, "late")
def _(d):
    return base(d, "LATE", [tierra(IZQ, 950, 300), tierra(DER, 950, 300, keys=late(0.3, 3, 0.16, 0.34))],
                sfx=[(0.3 + i * 0.34, "burbuja", -18) for i in range(3)], color=MAGENTA)


@v.plano(18, "señala")
def _(d):
    return base(d, "SEÑALA", [IMG("satelite", ancho=220, x=IZQ, y=950, z=0.5), IMG("satelite", ancho=220, x=DER, y=950, z=0.5),
                               senala(DER, 950, 0.4, d - 0.1, 170)], sfx=[(0.4, "ding", -16)])


@v.plano(25, "subida + impacto")
def _(d):
    t = d * 0.62
    return P(ESPACIO, [BG("bg_esp_ambar"), estrellas(30, 7),
                       IMG("meteorito", ancho=700, z=0.5, ex=-1, rot=47, keys=[{"t": 0, "x": 120, "y": 420, "escala": 0.3}, {"t": t, "x": 560, "y": 980, "escala": 1.1, "ease": "entrada"}]),
                       fundido_blanco([{"t": 0, "op": 0}, {"t": t - 0.05, "op": 0}, {"t": t, "op": 1}, {"t": t + 0.5, "op": 0}])],
             {"zoom": [1.0, 1.1], "foco": [[540, 960], [540, 960]], "pan": [[0, 0], [0, 0]], "temblor": 8}, energia=0.95,
             sfx=[(0, "subida", -14, {"dur": t}), (t, "impacto", -8)],
             hud=[amarillo(t + 0.1, d - 0.05, "SUBE Y GOLPEA", y=1250, tam=84, color=AMBAR)])


v.construir("muestrario-movimiento", version=1, gancho=False, bucle=0.3, musica={"generar": "curiosidad", "semilla": 5, "db": -15},
            claves=["muelle", "bota", "impulso", "Late", "anillo", "golpea"])
