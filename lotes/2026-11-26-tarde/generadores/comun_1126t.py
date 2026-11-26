"""Piezas comunes de los generadores del lote 2026-11-26-tarde (copia de comun_1125t; estilo del vídeo largo)."""
import os, re, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403

SVG_DIR = None
_DIM = {}
OSC = ["#141428", "#06060e"]
ESP = ["#02030a", "#0a1030"]
# suelo (y) de cada fondo vertical
SUELO = {"bg_ciudad": 1390, "bg_estadio_noche": 1395, "bg_oficina_gris": 1440, "bg_cielo_naranja": 1370, "bg_via_lactea": 1450,
         "bg_galeria": 1380, "bg_amanecer": 1360, "bg_ventana_invierno": 1480, "bg_tienda_noche": 1380, "bg_cerebro": 1300, "bg_dormitorio": 1560}


def dim(n):
    if n not in _DIM:
        t = open(os.path.join(SVG_DIR, n + ".svg")).read(400)
        m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', t)
        _DIM[n] = (float(m.group(1)), float(m.group(2)))
    return _DIM[n]


def PZ(n, x, suelo, alto, z=0.5, keys=None, pie=25, **k):
    """Pieza posada en el suelo: `alto` = altura en pantalla del lienzo; los pies (h - pie) caen en `suelo`."""
    w, h = dim(n)
    ancho = alto * w / h
    y = suelo - alto / 2 + pie / h * alto
    return IMG(n, ancho=ancho, x=x, y=y, z=z, keys=keys or [], **k)


def OB(n, x, y, ancho, z=0.5, keys=None, **k):
    return IMG(n, ancho=ancho, x=x, y=y, z=z, keys=keys or [], **k)


def flota(d, amp=14, y=0, periodo=2.0):
    ks, t, s = [], 0.0, 1
    while t <= d + 0.01:
        ks.append({"t": round(t, 3), "y": y + s * amp, "ease": "suave"})
        t += periodo / 2
        s = -s
    return ks


def vibra(t0, t1, x, amp=9, paso=0.05):
    """Temblor horizontal rápido (vibración del teléfono) entre t0 y t1."""
    ks, t, s = [{"t": 0, "x": x}], t0, 1
    while t < t1:
        ks.append({"t": round(t, 3), "x": x + s * amp, "ease": "lineal"})
        t += paso
        s = -s
    ks.append({"t": round(t1 + 0.02, 3), "x": x})
    return ks


def tacha(x, y, t0, r=150, z=0.9):
    return [flecha([[x - r, y - r], [x + r, y + r]], t0, t0 + 0.15, "#ff3d3d", 22, punta=False, z=z),
            flecha([[x + r, y - r], [x - r, y + r]], t0 + 0.1, t0 + 0.25, "#ff3d3d", 22, punta=False, z=z)]


def cap(t0, t1, txt, color="#141414", fondo="#ffd23fe6", tam=100, y=560, x=540):
    return rotulo(t0, t1, txt, tam=tam, color=color, capsula=fondo, y=y, x=x)


def BANDA():
    """Franja oscura bajo el subtítulo en fondos claros (fija, sin sonido)."""
    return {**IMG("banda_sub", ancho=1080, x=540, y=330), "hud": True, "z": 0.5, "sin_pop": True,
            "keys": [{"t": 0, "op": 1}, {"t": 98, "op": 1}, {"t": 99, "op": 1}]}


def gente(n_tot, n_on, t0, y=1100, ancho=150, color="#2ff3ff", piezas=("voluntario_1", "voluntario_2", "voluntario_3", "voluntario_4", "voluntario_5", "voluntario_6")):
    """Personas en dos filas de cinco; las n_on primeras se encienden (halo) una tras otra desde t0."""
    els = []
    por_fila = (n_tot + 1) // 2
    for i in range(n_tot):
        fila, col = divmod(i, por_fila)
        x = 140 + col * (800 / (por_fila - 1))
        yy = y - 170 + fila * 330
        p = piezas[i % len(piezas)]
        alto = ancho * dim(p)[1] / dim(p)[0]
        on = i < n_on
        ti = t0 + i * 0.07
        els.append(IMG(p, ancho=ancho, x=x, y=yy, z=0.5 + fila * 0.01, keys=[{"t": 0, "op": 0.4}, {"t": ti, "op": 0.4}, {"t": ti + 0.1, "op": 1.0 if on else 0.3}]))
        if on:
            els.append(brillo(x, yy, alto * 0.5, color, 0.5, 0.45 + fila * 0.01, keys=[{"t": ti, "op": 0}, {"t": ti + 0.12, "op": 0.55}]))
    return els


def flip(nombres, d, fps=10.0, base=None):
    """Fotogramas que se alternan (martillo del despertador): lista de IMG con claves de opacidad."""
    out, paso = [], 1.0 / fps
    for i, nm in enumerate(nombres):
        e = base(nm)
        ks, t, j = [{"t": 0, "op": 1.0 if i == 0 else 0.0}], 0.0, 0
        while t < d + paso:
            on = (j % len(nombres) == i)
            ks += [{"t": round(t, 3), "op": 1.0 if on else 0.0, "ease": "lineal"}, {"t": round(t + 0.001, 3), "op": 1.0 if on else 0.0}]
            t += paso
            j += 1
        e["keys"] = e.get("keys", []) + ks
        out.append(e)
    return out


def suena(x, y, ancho, d, t1=None, z=0.55, temblor=8):
    """Despertador sonando: martillo que alterna, temblor y ondas."""
    t1 = d if t1 is None else t1
    els = flip(["despertador_a", "despertador_b"], min(t1, d), 14, base=lambda n: OB(n, x, y, ancho, z=z, keys=vibra(0.0, t1, x, temblor, 0.04)))
    if t1 < d:   # se calla: queda el a
        els[1]["keys"].append({"t": round(t1 + 0.01, 3), "op": 0})
        els[0]["keys"].append({"t": round(t1 + 0.01, 3), "op": 1})
    els.append(OB("ondas_vibra", x, y - ancho * 0.25, ancho * 1.5, z=z + 0.05, keys=[{"t": 0, "op": 1}, {"t": t1, "op": 1}, {"t": t1 + 0.08, "op": 0}] + late(0.0, 3, 0.07, 0.25)))
    return els
