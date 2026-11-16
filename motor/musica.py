"""Música de fondo generada por código (sin licencias de terceros) y mezcla final.

Sirve como base mientras no se elija una fuente de música (ver DECISIONS.md, «Presupuesto y gastos»).
Estilos: "curiosidad" (re menor, pad + arpegio suave, 92 bpm), "misterio" (más grave y lento).

CLI:  python3 -m motor.musica salida.wav --dur 47 --estilo curiosidad --semilla 1
"""
import argparse
import subprocess
import wave

import numpy as np

SR = 48000
NOTAS = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}


def hz(nota, octava):
    return 440.0 * 2 ** ((NOTAS[nota] + 12 * (octava + 1) - 69) / 12)


ESTILOS = {
    "curiosidad": {"bpm": 92, "acordes": [("D", "m"), ("A#", "M"), ("F", "M"), ("C", "M")], "octava": 3,
                    "arpegio": True, "brillo": 0.35},
    "misterio": {"bpm": 70, "acordes": [("A", "m"), ("F", "M"), ("D", "m"), ("E", "M")], "octava": 2,
                  "arpegio": True, "brillo": 0.2},
}


def _acorde(raiz, tipo, octava):
    i = NOTAS[raiz]
    tercera = 3 if tipo == "m" else 4
    nombres = list(NOTAS)
    out = []
    for semi in (0, tercera, 7, 12):
        n = i + semi
        out.append(hz(nombres[n % 12], octava + n // 12))
    return out


def _paso_bajo(x, corte):
    from scipy.signal import lfilter  # filtro de un polo; si no hay scipy se usa el bucle de _lp
    a = np.exp(-2 * np.pi * corte / SR)
    return lfilter([1 - a], [1, -a], x)


def _lp(x, corte):
    try:
        return _paso_bajo(x, corte)
    except Exception:
        a = np.exp(-2 * np.pi * corte / SR)
        y = np.empty_like(x)
        acc = 0.0
        for i, v in enumerate(x):
            acc = (1 - a) * v + a * acc
            y[i] = acc
        return y


def generar(salida, dur, estilo="curiosidad", semilla=1):
    cfg = ESTILOS[estilo]
    rng = np.random.default_rng(semilla)
    n = int(dur * SR)
    t = np.arange(n) / SR
    L, R = np.zeros(n), np.zeros(n)
    compas = 4 * 60 / cfg["bpm"]
    dur_acorde = 2 * compas
    k = 0
    while k * dur_acorde < dur:
        raiz, tp = cfg["acordes"][k % len(cfg["acordes"])]
        f = _acorde(raiz, tp, cfg["octava"])
        a0, a1 = int(k * dur_acorde * SR), min(n, int(((k + 1) * dur_acorde + 1.2) * SR))
        tt = np.arange(a1 - a0) / SR
        env = np.minimum(1, tt / 1.4) * np.minimum(1, np.maximum(0, (a1 - a0) / SR - tt) / 1.2)
        for j, fr in enumerate(f):
            for det, lado in ((-0.18, 0.7), (0.18, 0.3)):
                ph = rng.random() * 2 * np.pi
                saw = 2 * ((fr * (1 + det / 100) * tt + ph / (2 * np.pi)) % 1) - 1
                v = saw * env * (0.10 if j < 3 else 0.06)
                L[a0:a1] += v * lado
                R[a0:a1] += v * (1 - lado)
        # bajo suave
        sub = np.sin(2 * np.pi * f[0] / 2 * tt) * env * 0.18
        L[a0:a1] += sub
        R[a0:a1] += sub
        # arpegio tipo «pluck» en corcheas
        if cfg["arpegio"]:
            corchea = 60 / cfg["bpm"] / 2
            m = 0
            while m * corchea < dur_acorde:
                fr = f[[0, 1, 2, 3, 2, 1][m % 6]] * 2
                b0 = a0 + int(m * corchea * SR)
                b1 = min(n, b0 + int(1.2 * SR))
                tb = np.arange(b1 - b0) / SR
                nota = (np.sin(2 * np.pi * fr * tb) + 0.3 * np.sin(4 * np.pi * fr * tb)) * np.exp(-tb * 4.5) * 0.05
                pan = 0.5 + 0.35 * np.sin(m * 1.3)
                L[b0:b1] += nota * pan
                R[b0:b1] += nota * (1 - pan)
                m += 1
        k += 1
    corte = 900 + 1400 * cfg["brillo"]
    L, R = _lp(L, corte), _lp(R, corte)
    # vaivén lento del volumen
    lfo = 0.85 + 0.15 * np.sin(2 * np.pi * t / 7.0)
    L, R = L * lfo, R * lfo
    # entrada y salida
    fade = np.minimum(1, t / 1.0) * np.minimum(1, (dur - t) / 1.5)
    L, R = L * fade, R * fade
    pico = max(np.abs(L).max(), np.abs(R).max(), 1e-6)
    est = np.stack([L, R], 1) / pico * 0.6
    with wave.open(salida, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((est * 32767).astype("<i2").tobytes())
    return salida


def mezclar(voz, musica, salida, dur, musica_db=-17.0, lufs=-19.0, sfx=None):
    """Voz + música (atenuada bajo la voz con sidechain) + efectos opcionales, normalizado a `lufs`.
    `musica` puede ser None (solo voz + efectos). Los efectos no se atenúan bajo la voz."""
    ins, f, n = ["-i", voz], [f"[0:a]aresample=48000,apad,atrim=0:{dur:.3f},asplit=2[v1][v2]"], 1
    capas = ["[v1]"]
    if musica:
        ins += ["-i", musica]
        f.append(f"[{n}:a]aresample=48000,volume={musica_db}dB,apad,atrim=0:{dur:.3f}[m]")
        f.append("[m][v2]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=400[md]")
        capas.append("[md]"); n += 1
    else:
        f.append("[v2]anullsink")
    if sfx:
        ins += ["-i", sfx]
        f.append(f"[{n}:a]aresample=48000,apad,atrim=0:{dur:.3f}[fx]")
        capas.append("[fx]"); n += 1
    f.append(f"{''.join(capas)}amix=inputs={len(capas)}:normalize=0,loudnorm=I={lufs}:TP=-1.5:LRA=11,aresample=48000[a]")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(f),
                           "-map", "[a]", "-ac", "2", "-ar", "48000", salida])
    return salida

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("salida")
    ap.add_argument("--dur", type=float, required=True)
    ap.add_argument("--estilo", default="curiosidad", choices=sorted(ESTILOS))
    ap.add_argument("--semilla", type=int, default=1)
    a = ap.parse_args()
    print(generar(a.salida, a.dur, a.estilo, a.semilla))
