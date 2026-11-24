"""Piezas comunes de los generadores del lote 2026-11-23-tarde (estilo cartoon)."""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403

OSC = ["#141428", "#06060e"]
CIELO = ["#2a6ad8", "#d8ecff"]


def muneco(nombre="mu_b", brazo="br_b", x=540, y=1200, ancho=300, z=0.5, pup=(0, 0), keys_pup=None, rot_in=-18, rot_out=14):
    """Muñeco cartoon quieto (cuerpo, brazos y pupilas). pup = desplazamiento de las pupilas."""
    k = ancho / 360; hy = y + (272 - 380) * k; ab = 120 * k
    return [IMG(brazo, ancho=ab, x=x - 85 * k, y=hy, z=z - 0.01, rot=rot_out), IMG(nombre, ancho=ancho, x=x, y=y, z=z),
            IMG("pupilas", ancho=ancho, x=x + pup[0], y=y + pup[1], z=z + 0.005, keys=keys_pup or []),
            IMG(brazo, ancho=ab, x=x + 85 * k, y=hy, z=z + 0.01, rot=-rot_out)]


def saltos(d, xs, t0=0.0, paso=0.35, y=0):
    """Claves de pupila que SALTAN entre posiciones (sin deslizarse)."""
    ks, t, i = [], t0, 0
    while t < d:
        ks += [{"t": round(t, 3), "x": xs[i % len(xs)], "y": y, "ease": "lineal"}, {"t": round(min(d, t + paso - 0.03), 3), "x": xs[i % len(xs)], "y": y, "ease": "lineal"}]
        t += paso; i += 1
    return ks


def palabra(t0, t1, texto, color, y=1000, tam=210, x=540):
    """Palabra de color sobre la pizarra (sin cápsula)."""
    return {**rotulo(t0, t1, texto, tam=tam, color=color, capsula=None, x=x, y=y), "fijo": True}
