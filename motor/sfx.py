"""Efectos de sonido generados por código (sin licencias): whoosh, pop, tic, golpe, zap, brillo, ding, rumor, ola.

En episodio.json:  "sfx": [{"t": 1.2, "tipo": "whoosh", "db": -10, "dur": 0.45}, ...]
`t` en segundos absolutos. El motor los mezcla con la voz y la música (no se atenúan bajo la voz).
Prueba:  python3 -m motor.sfx demo.wav   (todos seguidos)
"""
import argparse, wave

import numpy as np

SR = 48000


def _env(n, ataque=0.005, caida=0.2):
    t = np.arange(n) / SR
    a = np.clip(t / max(ataque, 1e-4), 0, 1)
    return a * np.exp(-t / max(caida, 1e-3))


def _paso_bajo(x, corte):
    """Filtro de un polo con corte variable (array o escalar, en Hz)."""
    corte = np.broadcast_to(np.asarray(corte, np.float64), x.shape)
    a = np.exp(-2 * np.pi * corte / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc
        y[i] = acc
    return y


def whoosh(dur=0.45, rng=None):
    rng = rng or np.random.default_rng(1)
    n = int(dur * SR)
    u = np.linspace(0, 1, n)
    ruido = rng.normal(0, 1, n)
    corte = 300 + 5200 * np.sin(np.pi * u) ** 2
    lp = _paso_bajo(ruido, corte)
    bp = lp - _paso_bajo(lp, 180)
    env = np.sin(np.pi * u ** 0.8) ** 2
    return bp * env * 1.6


def pop(dur=0.12, f0=700, f1=180):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.02)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.035)


def tic(dur=0.05, rng=None):
    rng = rng or np.random.default_rng(2)
    n = int(dur * SR)
    x = rng.normal(0, 1, n)
    x = x - _paso_bajo(x, 2500)
    return (x * 0.5 + np.sin(2 * np.pi * 2600 * np.arange(n) / SR)) * _env(n, 0.0005, 0.008) * 0.8


def golpe(dur=0.7, rng=None):
    rng = rng or np.random.default_rng(3)
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 45 + 90 * np.exp(-t / 0.05)
    tono = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.22)
    ruido = _paso_bajo(rng.normal(0, 1, n), 1200) * _env(n, 0.001, 0.06) * 2.5
    return np.tanh((tono + ruido) * 1.6) * 0.9


def zap(dur=0.35, f0=2200, f1=260):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.07)
    fase = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(fase) + 0.4 * np.sin(2 * fase) + 0.2 * np.sign(np.sin(fase * 0.5))
    return x * _env(n, 0.002, 0.12) * 0.5


def brillo(dur=0.9):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t + i) * a for i, (f, a) in enumerate([(2637, 1), (3520, 0.7), (5274, 0.5), (4186, 0.6)]))
    trem = 0.6 + 0.4 * np.sin(2 * np.pi * 14 * t)
    return x * trem * _env(n, 0.01, 0.28) * 0.3


def ding(dur=1.4, f=880):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * m * t) * a * np.exp(-t / (0.5 / m)) for m, a in [(1, 1), (2.76, 0.4), (5.4, 0.2), (8.9, 0.1)])
    return x * _env(n, 0.002, 10) * 0.45


def rumor(dur=1.6, rng=None):
    rng = rng or np.random.default_rng(4)
    n = int(dur * SR)
    u = np.linspace(0, 1, n)
    x = _paso_bajo(_paso_bajo(rng.normal(0, 1, n), 220), 220) * 6
    return np.tanh(x) * np.sin(np.pi * u ** 0.5) ** 1.5 * 0.9


def ola(dur=1.4, rng=None):
    rng = rng or np.random.default_rng(5)
    n = int(dur * SR)
    u = np.linspace(0, 1, n)
    corte = 400 + 3000 * np.sin(np.pi * u) ** 3
    x = _paso_bajo(rng.normal(0, 1, n), corte)
    return x * np.sin(np.pi * u ** 0.7) ** 2 * 1.4


TIPOS = {"whoosh": whoosh, "pop": pop, "tic": tic, "golpe": golpe, "zap": zap, "brillo": brillo, "ding": ding,
         "rumor": rumor, "ola": ola}


def pista(eventos, dur, ruta):
    """Escribe un WAV estéreo 48 kHz de `dur` s con los efectos colocados (con algo de paneo)."""
    n = int(dur * SR) + SR
    est = np.zeros((n, 2), np.float64)
    for i, e in enumerate(eventos):
        kw = {k: v for k, v in e.items() if k not in ("t", "tipo", "db", "pan")}
        x = TIPOS[e["tipo"]](**kw)
        x = x / (np.abs(x).max() + 1e-9) * 10 ** (e.get("db", -12) / 20)  # db = pico del efecto
        pan = e.get("pan", 0.0)
        i0 = int(e["t"] * SR)
        i1 = min(n, i0 + len(x))
        if i0 >= n:
            continue
        seg = x[: i1 - i0]
        est[i0:i1, 0] += seg * np.sqrt((1 - pan) / 2) * 1.414
        est[i0:i1, 1] += seg * np.sqrt((1 + pan) / 2) * 1.414
    est = np.clip(est[: int(dur * SR)], -1, 1)
    with wave.open(ruta, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((est * 32767).astype("<i2").tobytes())
    return ruta


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("salida")
    a = ap.parse_args()
    ev = [{"t": 0.3 + i * 1.6, "tipo": k, "db": -6} for i, k in enumerate(TIPOS)]
    print(pista(ev, 0.5 + len(TIPOS) * 1.6, a.salida))
