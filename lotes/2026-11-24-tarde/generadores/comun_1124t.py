"""Piezas comunes de los generadores del lote 2026-11-24-tarde (estilo cartoon, como el 2026-11-23-tarde)."""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403

OSC = ["#141428", "#06060e"]
ESP = ["#02030a", "#0a1030"]


def flota(d, amp=18, x=None, y=None, periodo=1.6):
    """Deriva suave arriba y abajo (ingravidez o respiración), sin quedarse quieto."""
    ks, t, s = [], 0.0, 1
    while t <= d + 0.01:
        k = {"t": round(t, 3), "y": (y or 0) + s * amp, "ease": "suave"}
        if x is not None:
            k["x"] = x
        ks.append(k); t += periodo / 2; s = -s
    return ks


def tacha(x, y, t0, r=170, z=0.9):
    """Aspa roja que se dibuja encima de algo (NO)."""
    return [flecha([[x - r, y - r], [x + r, y + r]], t0, t0 + 0.15, "#ff3d3d", 22, punta=False, z=z),
            flecha([[x + r, y - r], [x - r, y + r]], t0 + 0.1, t0 + 0.25, "#ff3d3d", 22, punta=False, z=z)]


def BANDA():
    """Franja oscura bajo el subtítulo en fondos claros (va en hud=[...]: no se mueve con la cámara)."""
    return {**IMG("banda_sub", ancho=1080, x=540, y=330), "hud": True, "z": 0.5, "sin_pop": True, "keys": [{"t": 0, "op": 1}, {"t": 98, "op": 1}, {"t": 99, "op": 1}]}
