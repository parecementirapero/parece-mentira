"""Piezas extra de la parte 1 (prefijo p1_): examen sin nota y la nota roja suelta (para que «caiga» sobre el examen).
Uso: python3 ilus_extra_p1.py DIR_SVG"""
import math, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import ilus_cosas as IC  # noqa: E402
from motor.biblioteca import ilus  # noqa: E402

NOMBRES = []


def p1_examen_blanco():
    """El mismo examen de `examen` (560×740) pero todavía sin corregir: sin la nota roja."""
    w, h = 560, 740
    z = IC._pz("p1_examen_blanco", w, h)
    d, caja = IC._hoja(z, w, h, -2)
    x0, y0, x1, y1 = caja
    z(f'<path d="M{x0 + 28} {y0} L{x0 + 28} {y1}" stroke="#e08a8a" stroke-width="2" opacity="0.7"/>')
    z(f'<rect x="{x0 + 40}" y="{y0 + 26}" width="200" height="14" rx="7" fill="#3a4a6a" opacity="0.6"/>')
    IC._renglones(z, caja, y0 + 220, y1 - 30, 41)
    z(f'<path d="M{x0 + 60} {y0 + 400} l90 -6 M{x0 + 60} {y0 + 406} l90 -8" stroke="#3a4a6a" stroke-width="4" opacity="0.8"/>')
    z('</g>')
    z.guardar(True)
    NOMBRES.append(z.n)


def p1_nota_roja():
    """La nota roja del examen (círculo tachado) suelta, 220×220, centrada. En `examen` está en (+126, −236) del centro."""
    w = h = 220
    z = IC._pz("p1_nota_roja", w, h)
    cx, cy, R = 110, 110, 78
    z(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#d01e24" stroke-width="13" opacity="0.95" '
      f'stroke-dasharray="{2 * math.pi * R - 30:.0f} 30" transform="rotate(-70 {cx} {cy})"/>',
      f'<path d="M{cx - 70} {cy + 66} L{cx + 66} {cy - 72}" stroke="#d01e24" stroke-width="14" stroke-linecap="round" opacity="0.95"/>')
    z.guardar(False)
    NOMBRES.append(z.n)


def generar(dirsvg):
    os.makedirs(dirsvg, exist_ok=True)
    ilus.OUT = dirsvg
    NOMBRES.clear()
    p1_examen_blanco(); p1_nota_roja()
    return list(NOMBRES)


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
