"""Núcleo del motor: lienzo, tiempos, interpolación y composición."""
import math

import numpy as np
from PIL import Image

W, H, FPS = 1080, 1920, 30


# ---------------------------------------------------------------- colores
def rgb(c, a=None):
    """'#rrggbb' | '#rrggbbaa' | [r,g,b(,a)] -> (r,g,b,a)."""
    if isinstance(c, (list, tuple)):
        t = tuple(int(v) for v in c)
        if len(t) == 3:
            t = t + (255,)
    else:
        c = c.lstrip("#")
        t = tuple(int(c[i:i + 2], 16) for i in range(0, len(c), 2))
        if len(t) == 3:
            t = t + (255,)
    if a is not None:
        t = t[:3] + (int(a),)
    return t


def mezcla(c1, c2, u):
    a, b = rgb(c1), rgb(c2)
    return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(4))


# ---------------------------------------------------------------- easing
def _back(u, s=1.70158):
    u -= 1
    return u * u * ((s + 1) * u + s) + 1


EASE = {
    "lineal": lambda u: u,
    "suave": lambda u: u * u * (3 - 2 * u),
    "entrada": lambda u: u * u * u,
    "salida": lambda u: 1 - (1 - u) ** 3,
    "rebote": _back,
}


def interp(keys, t, prop, default):
    """Interpola `prop` en una lista de keyframes [{'t':s, prop:v, 'ease':..}]."""
    ks = [k for k in keys if prop in k]
    if not ks:
        return default
    if t <= ks[0]["t"]:
        return ks[0][prop]
    if t >= ks[-1]["t"]:
        return ks[-1][prop]
    for a, b in zip(ks, ks[1:]):
        if a["t"] <= t <= b["t"]:
            span = max(b["t"] - a["t"], 1e-6)
            u = EASE[b.get("ease", "suave")]((t - a["t"]) / span)
            return a[prop] + (b[prop] - a[prop]) * u
    return ks[-1][prop]


# ---------------------------------------------------------------- composición
def pegar(lienzo, spr, cx, cy):
    """Compone `spr` (RGBA) centrado en (cx, cy) recortando a los bordes."""
    w, h = spr.size
    x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    lx0, ly0 = max(0, x0), max(0, y0)
    lx1, ly1 = min(lienzo.width, x0 + w), min(lienzo.height, y0 + h)
    if lx1 <= lx0 or ly1 <= ly0:
        return
    trozo = spr.crop((lx0 - x0, ly0 - y0, lx1 - x0, ly1 - y0))
    lienzo.alpha_composite(trozo, (lx0, ly0))


def opacidad(spr, op):
    if op >= 0.999:
        return spr
    r, g, b, a = spr.split()
    a = a.point(lambda v: int(v * op))
    return Image.merge("RGBA", (r, g, b, a))


def transformar(spr, escala=1.0, ex=1.0, ey=1.0, rot=0.0):
    sx, sy = escala * ex, escala * ey
    if abs(sx - 1) > 1e-3 or abs(sy - 1) > 1e-3:
        nw, nh = max(1, int(spr.width * sx)), max(1, int(spr.height * sy))
        spr = spr.resize((nw, nh), Image.BICUBIC)
    if abs(rot) > 0.05:
        spr = spr.rotate(-rot, resample=Image.BICUBIC, expand=True)
    return spr


def supermuestreo(dibujar, w, h, f=2):
    """Dibuja a f× y reduce: bordes suaves con ImageDraw."""
    big = Image.new("RGBA", (int(w * f), int(h * f)), (0, 0, 0, 0))
    dibujar(big, f)
    return big.resize((int(w), int(h)), Image.LANCZOS)


# ---------------------------------------------------------------- ruido
_RUIDO = {}


def ruido(w, h, semilla=0, octavas=4, base=4):
    """Ruido suave (value noise por octavas) en [0,1], forma (h, w)."""
    clave = (w, h, semilla, octavas, base)
    if clave in _RUIDO:
        return _RUIDO[clave]
    rng = np.random.default_rng(semilla)
    acc = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octavas):
        n = base * (2 ** o)
        g = rng.random((n + 1, n + 1)).astype(np.float32)
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        acc += amp * (np.asarray(im, np.float32) / 255)
        tot += amp
        amp *= 0.5
    acc /= tot
    acc = (acc - acc.min()) / max(acc.max() - acc.min(), 1e-6)
    _RUIDO[clave] = acc
    return acc


def lerp_arr(c1, c2, u):
    a = np.array(rgb(c1)[:3], np.float32)
    b = np.array(rgb(c2)[:3], np.float32)
    return a + (b - a) * u[..., None]


def vineta(fuerza=0.55):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x - W / 2) / (W * 0.75)) ** 2 + ((y - H / 2) / (H * 0.62)) ** 2)
    a = np.clip((d - 0.55) / 0.6, 0, 1) ** 1.6 * fuerza
    arr = np.zeros((H, W, 4), np.uint8)
    arr[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def ease_onda(t, periodo, fase=0.0):
    return math.sin(2 * math.pi * (t / max(periodo, 1e-6)) + fase)
