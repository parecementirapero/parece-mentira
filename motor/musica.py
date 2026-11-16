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


def _curva(energia, t):
    """Interpola [(segundo, nivel 0..1), ...] sobre el eje de tiempo t."""
    if not energia:
        return np.full(len(t), 0.5)
    e = sorted(energia)
    return np.interp(t, [a for a, _ in e], [b for _, b in e])


def generar(salida, dur, estilo="curiosidad", semilla=1, energia=None, bucle=False):
    """energia: [(segundo, nivel 0..1)] → la música se abre (más brillo y arpegio) y gana pulso (bombo suave y
    shaker por encima de 0,55) donde el vídeo aprieta, y se recoge donde hay que escuchar la voz.
    bucle: el último acorde es el que resuelve en el primero y no hay fundido largo: al reiniciarse el Short
    la música enlaza sin corte."""
    cfg = ESTILOS[estilo]
    rng = np.random.default_rng(semilla)
    n = int(dur * SR)
    t = np.arange(n) / SR
    L, R = np.zeros(n), np.zeros(n)
    compas = 4 * 60 / cfg["bpm"]
    dur_acorde = 2 * compas
    E = _curva(energia, t)
    Larp, Rarp = np.zeros(n), np.zeros(n)
    n_ac = int(np.ceil(dur / dur_acorde))
    desfase = (len(cfg["acordes"]) - n_ac % len(cfg["acordes"])) % len(cfg["acordes"]) if bucle else 0
    k = 0
    while k * dur_acorde < dur:
        raiz, tp = cfg["acordes"][(k + desfase) % len(cfg["acordes"])]
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
                Larp[b0:b1] += nota * pan
                Rarp[b0:b1] += nota * (1 - pan)
                m += 1
        k += 1
    corte = 900 + 1400 * cfg["brillo"]
    if energia is None:
        L, R = _lp(L + Larp, corte), _lp(R + Rarp, corte)
    else:
        # dos versiones (oscura y brillante) mezcladas según la energía; el arpegio entra con ella
        ga = 0.35 + 1.1 * E
        Lo, Ro = _lp(L + Larp * ga, corte * 0.7), _lp(R + Rarp * ga, corte * 0.7)
        Lb, Rb = _lp(L + Larp * ga, corte * 2.6), _lp(R + Rarp * ga, corte * 2.6)
        L, R = Lo * (1 - E) + Lb * E, Ro * (1 - E) + Rb * E
        # pulso: bombo suave en cada negra y shaker a contratiempo, solo donde la energía pasa de 0,55
        negra = 60 / cfg["bpm"]
        m = 0
        while m * negra < dur:
            i0 = int(m * negra * SR)
            g = max(0.0, float(E[min(i0, n - 1)]) - 0.55) / 0.45
            if g > 0:
                nb = min(n - i0, int(0.22 * SR)); tb = np.arange(nb) / SR
                bombo = np.sin(2 * np.pi * np.cumsum(45 + 70 * np.exp(-tb / 0.03)) / SR) * np.exp(-tb / 0.09) * 0.22 * g
                L[i0:i0 + nb] += bombo; R[i0:i0 + nb] += bombo
                j0 = i0 + int(negra / 2 * SR); ns = min(max(0, n - j0), int(0.06 * SR))
                if ns > 0:
                    sh = rng.normal(0, 1, ns); sh = (sh - _lp(sh, 5000)) * np.exp(-np.arange(ns) / SR / 0.015) * 0.05 * g
                    L[j0:j0 + ns] += sh * 0.4; R[j0:j0 + ns] += sh * 0.6
            m += 1
        L, R = L * (0.8 + 0.35 * E), R * (0.8 + 0.35 * E)
    # vaivén lento del volumen
    lfo = 0.85 + 0.15 * np.sin(2 * np.pi * t / 7.0)
    L, R = L * lfo, R * lfo
    # entrada y salida
    fade = (np.minimum(1, t / 0.12) * np.minimum(1, (dur - t) / 0.2)) if bucle else (np.minimum(1, t / 1.0) * np.minimum(1, (dur - t) / 1.5))
    L, R = L * fade, R * fade
    pico = max(np.abs(L).max(), np.abs(R).max(), 1e-6)
    est = np.stack([L, R], 1) / pico * 0.6
    with wave.open(salida, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((est * 32767).astype("<i2").tobytes())
    return salida


def mezclar(voz, musica, salida, dur, musica_db=-17.0, lufs=-19.0, sfx=None, sfx_bajo_voz=True):
    """Voz + música (atenuada bajo la voz con sidechain) + efectos opcionales, normalizado a `lufs`.
    `musica` puede ser None (solo voz + efectos). Con `sfx_bajo_voz` (por defecto) los efectos también se
    atenúan un poco mientras hay voz (compresión suave 3:1 con ataque rápido), para que ningún efecto la tape;
    en las pausas suenan a su nivel."""
    n_copias = 1 + bool(musica) + bool(sfx and sfx_bajo_voz)
    et = [f"[v{i}]" for i in range(n_copias)]
    ins, f, n = ["-i", voz], [f"[0:a]aresample=48000,apad,atrim=0:{dur:.3f},asplit={n_copias}{''.join(et)}" if n_copias > 1
                             else f"[0:a]aresample=48000,apad,atrim=0:{dur:.3f}[v0]"], 1
    capas, libre = ["[v0]"], 1
    if musica:
        ins += ["-i", musica]
        f.append(f"[{n}:a]aresample=48000,volume={musica_db}dB,apad,atrim=0:{dur:.3f}[m]")
        f.append(f"[m][v{libre}]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=400[md]")
        capas.append("[md]"); n += 1; libre += 1
    if sfx:
        ins += ["-i", sfx]
        f.append(f"[{n}:a]aresample=48000,apad,atrim=0:{dur:.3f}[fx0]")
        if sfx_bajo_voz:
            f.append(f"[fx0][v{libre}]sidechaincompress=threshold=0.05:ratio=3:attack=5:release=180[fx]")
            capas.append("[fx]")
        else:
            capas.append("[fx0]")
        n += 1
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
