"""Música de fondo generada por código (sin licencias de terceros) y mezcla final.

Sirve como base mientras no se elija una fuente de música (ver DECISIONS.md, «Presupuesto y gastos»).
Estilos: "curiosidad" (re menor, pad + arpegio suave, 92 bpm), "misterio" (más grave y lento),
"emprende" (do mayor I–V–vi–IV, 112 bpm, piano, bombo y palmas que entran pronto: motivador, de «a por ello»),
"cine" (hip hop cinematográfico oscuro y motivador: piano con reverb, cuerdas, 808 largo y pulso grave, batería
suave a medio tiempo; si menor Si m–Sol–Fa#; la base de los vídeos de «mentalidad de emprendedor»),
"ambicion" (trap oscuro de «mentalidad de negocio», si menor, 143 bpm a medio tiempo: 808 grave con glissando,
bombo, palmada en el 3, charles en semicorcheas con redobles, campana/pluck menor y pad; intro sin 808 y «drop»).

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
    "emprende": {"bpm": 112, "acordes": [("C", "M"), ("G", "M"), ("A", "m"), ("F", "M")], "octava": 3,
                  "arpegio": True, "brillo": 0.7, "umbral": 0.25, "palmas": True, "piano": True},
    "ambicion": {"bpm": 143, "acordes": [("B", "m"), ("G", "M"), ("E", "m"), ("F#", "M")], "octava": 3,
                  "arpegio": False, "brillo": 0.5, "trap": True},
    "cine": {"bpm": 143, "acordes": [("B", "m"), ("B", "m"), ("G", "M"), ("F#", "M")], "octava": 3,
              "arpegio": False, "brillo": 0.5, "cine": True},
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
    if cfg.get("trap"):
        return _trap(salida, dur, cfg, semilla, energia, bucle)
    if cfg.get("cine"):
        return _cine(salida, dur, cfg, semilla, energia, bucle)
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
                if cfg.get("piano"):
                    nota = (np.sin(2 * np.pi * fr * tb) + 0.45 * np.sin(4 * np.pi * fr * tb) + 0.18 * np.sin(6 * np.pi * fr * tb)) \
                        * np.exp(-tb * 3.2) * np.minimum(1, tb / 0.004) * 0.07
                else:
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
            um = cfg.get("umbral", 0.55)
            g = min(1.0, max(0.0, float(E[min(i0, n - 1)]) - um) / (1 - um))
            if g > 0:
                nb = min(n - i0, int(0.22 * SR)); tb = np.arange(nb) / SR
                bombo = np.sin(2 * np.pi * np.cumsum(45 + 70 * np.exp(-tb / 0.03)) / SR) * np.exp(-tb / 0.09) * 0.22 * g
                L[i0:i0 + nb] += bombo; R[i0:i0 + nb] += bombo
                j0 = i0 + int(negra / 2 * SR); ns = min(max(0, n - j0), int(0.06 * SR))
                if ns > 0:
                    sh = rng.normal(0, 1, ns); sh = (sh - _lp(sh, 5000)) * np.exp(-np.arange(ns) / SR / 0.015) * 0.05 * g
                    L[j0:j0 + ns] += sh * 0.4; R[j0:j0 + ns] += sh * 0.6
                if cfg.get("palmas") and m % 2 == 1:   # palmas en el 2 y el 4
                    npl = min(n - i0, int(0.12 * SR))
                    pl = rng.normal(0, 1, npl); pl = pl - _lp(pl, 900)
                    env_p = np.exp(-np.arange(npl) / SR / 0.035)
                    pl = pl * env_p * 0.09 * g
                    L[i0:i0 + npl] += pl * 0.55; R[i0:i0 + npl] += pl * 0.45
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


def _trap(salida, dur, cfg, semilla=1, energia=None, bucle=False):
    """Base trap oscura a medio tiempo (estilo de los vídeos de «emprender» que gustan a Jorge)."""
    rng = np.random.default_rng(semilla)
    n = int(dur * SR)
    t = np.arange(n) / SR
    L, R = np.zeros(n), np.zeros(n)
    negra = 60 / cfg["bpm"]            # 0,42 s
    compas = 4 * negra * 2             # medio tiempo: un «compás» = 8 negras (3,36 s)
    E = _curva(energia, t) if energia else np.full(n, 0.7)
    intro = min(4 * negra * 2, dur * 0.1)          # primeros ~3,4 s sin 808 ni bombo
    salida_t = dur - min(compas, 4.0)              # últimos segundos: se recoge
    acs = cfg["acordes"]

    def suma(x, i0, v, pan=0.5):
        i0 = int(i0)
        if i0 >= n or i0 < 0:
            return
        m = min(len(v), n - i0)
        L[i0:i0 + m] += v[:m] * (1 - pan) * 2 * 0.5
        R[i0:i0 + m] += v[:m] * pan * 2 * 0.5

    # pad oscuro (acordes largos, filtrado)
    k = 0
    while k * compas < dur:
        raiz, tp = acs[k % len(acs)]
        f = _acorde(raiz, tp, cfg["octava"])
        a0 = int(k * compas * SR); a1 = min(n, int(((k + 1) * compas + 0.8) * SR))
        tt = np.arange(a1 - a0) / SR
        env = np.minimum(1, tt / 0.8) * np.minimum(1, np.maximum(0, (a1 - a0) / SR - tt) / 0.8)
        pad = sum(np.sin(2 * np.pi * fr * tt + rng.random() * 6) + 0.25 * np.sin(4 * np.pi * fr * 1.003 * tt) for fr in f[:3])
        suma(None, a0, _lp(pad * env * 0.018, 900), 0.5)
        # 808: nota raíz grave, larga, con glissando al cambiar de acorde
        if a0 / SR >= intro and a0 / SR < salida_t:
            f0 = _acorde(raiz, tp, 1)[0]
            if f0 > 70: f0 /= 2
            nb = int(compas * SR)
            tb = np.arange(nb) / SR
            fsig = _acorde(*acs[(k + 1) % len(acs)], 1)[0]
            if fsig > 70: fsig /= 2
            fr = f0 + (fsig - f0) * np.clip((tb - (compas - 0.18)) / 0.18, 0, 1)
            fase = 2 * np.pi * np.cumsum(fr) / SR
            b = np.sin(fase) + 0.18 * np.sin(2 * fase)
            b = np.tanh(b * 1.6) * np.exp(-tb / 2.2) * np.minimum(1, tb / 0.01) * 0.42
            # dos golpes de 808 por compás (en la 1 y en la «y» del 3)
            suma(None, a0, b, 0.5)
            suma(None, a0 + int(5.5 * negra * SR), b[: int(2.4 * negra * SR)] * 0.8, 0.5)
        k += 1

    # batería
    paso = negra / 2                   # corchea a 143 bpm (= semicorchea a medio tiempo)
    m = 0
    while m * paso < dur:
        T = m * paso
        i0 = int(T * SR)
        e = float(E[min(i0, n - 1)])
        dentro = intro <= T < salida_t
        pos16 = m % 16                 # 16 corcheas = 1 compás de medio tiempo
        # bombo: 1 y algún síncopa
        if dentro and pos16 in (0, 7, 10):
            nb = int(0.25 * SR); tb = np.arange(nb) / SR
            kk = np.sin(2 * np.pi * np.cumsum(48 + 110 * np.exp(-tb / 0.025)) / SR) * np.exp(-tb / 0.12) * 0.55
            suma(None, i0, kk, 0.5)
        # palmada / caja en el 3 (medio tiempo)
        if (dentro or T >= intro * 0.5) and pos16 == 8:
            nc = int(0.22 * SR); ruido = rng.normal(0, 1, nc)
            cl = (ruido - _lp(ruido, 1200)) * np.exp(-np.arange(nc) / SR / 0.06) * 0.22
            tono = np.sin(2 * np.pi * 190 * np.arange(nc) / SR) * np.exp(-np.arange(nc) / SR / 0.04) * 0.12
            suma(None, i0, cl + tono, 0.5)
        # charles: corcheas, redoble de semicorcheas/fusas al final de cada 2 compases
        if T >= intro * 0.3 and T < dur - 1.0:
            redoble = (m % 32) >= 28
            subs = 3 if redoble and (m % 2 == 0) else (2 if redoble else 1)
            for s in range(subs):
                j0 = i0 + int(s * paso / subs * SR)
                nh = int(0.04 * SR); hh = rng.normal(0, 1, nh)
                hh = (hh - _lp(hh, 7000)) * np.exp(-np.arange(nh) / SR / 0.012) * (0.07 + 0.03 * (m % 2 == 0)) * (0.6 + 0.6 * e)
                suma(None, j0, hh, 0.62)
        m += 1

    # campana / pluck menor: motivo de 8 corcheas sobre el acorde (entra a la vez que el 808)
    motivo = [0, 2, 1, 2, 3, 2, 1, 0]
    m = 0
    while m * paso < dur:
        T = m * paso
        k = int(T // compas)
        raiz, tp = acs[k % len(acs)]
        f = _acorde(raiz, tp, cfg["octava"] + 1)
        if (m % 16) in (0, 3, 6, 8, 11, 14) and T >= intro * 0.6:
            fr = f[motivo[m % 8] % len(f)]
            nb = int(0.9 * SR); tb = np.arange(nb) / SR
            bell = (np.sin(2 * np.pi * fr * tb) + 0.5 * np.sin(2 * np.pi * fr * 2.76 * tb) * np.exp(-tb * 9)
                    + 0.2 * np.sin(2 * np.pi * fr * 5.4 * tb) * np.exp(-tb * 14)) * np.exp(-tb * 3.5) * 0.06
            suma(None, int(T * SR), bell, 0.35 + 0.3 * ((m // 3) % 2))
            # eco
            suma(None, int((T + paso * 3) * SR), bell * 0.35, 0.7)
        m += 1

    # barrido (subida) antes del drop
    if intro > 1.0:
        ns = int(min(intro, 3.0) * SR); a0 = int(intro * SR) - ns
        rr = rng.normal(0, 1, ns); rr = rr - _lp(rr, 2000)
        suma(None, max(0, a0), rr * np.linspace(0, 1, ns) ** 2 * 0.06, 0.5)

    L, R = L * (0.85 + 0.25 * E), R * (0.85 + 0.25 * E)
    fade = (np.minimum(1, t / 0.12) * np.minimum(1, (dur - t) / 0.2)) if bucle else (np.minimum(1, t / 0.4) * np.minimum(1, (dur - t) / 1.5))
    L, R = np.tanh(L * fade * 1.4), np.tanh(R * fade * 1.4)
    pico = max(np.abs(L).max(), np.abs(R).max(), 1e-6)
    est = np.stack([L, R], 1) / pico * 0.7
    with wave.open(salida, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((est * 32767).astype("<i2").tobytes())
    return salida


def _reverb(x, seg=2.2, mezcla=0.3, sem=3):
    from scipy.signal import fftconvolve
    r = np.random.default_rng(sem)
    n = int(seg * SR)
    ir = r.normal(0, 1, n) * np.exp(-np.arange(n) / SR / (seg / 5))
    ir = _lp(ir, 5000); ir /= np.sqrt(np.sum(ir ** 2))
    w = fftconvolve(x, ir)[: len(x)]
    return x * (1 - mezcla) + w * mezcla


def _cine(salida, dur, cfg, semilla=1, energia=None, bucle=False):
    """Hip hop cinematográfico oscuro (piano + cuerdas + 808 + pulso grave + batería suave a medio tiempo)."""
    rng = np.random.default_rng(semilla)
    n = int(dur * SR); t = np.arange(n) / SR
    negra = 60 / cfg["bpm"]; compas = 8 * negra          # compás de medio tiempo (3,36 s)
    E = _curva(energia, t) if energia else np.full(n, 0.7)
    acs = cfg["acordes"]
    intro = min(2 * compas * 0.5, dur * 0.12)             # 1 compás solo piano y cuerdas
    fin = dur - min(compas * 0.6, 3.0)
    piano, cuerdas, bajo, bat = (np.zeros(n) for _ in range(4))

    def pon(buf, i0, v):
        i0 = int(i0)
        if 0 <= i0 < n:
            m = min(len(v), n - i0); buf[i0:i0 + m] += v[:m]

    def nota_piano(fr, d=2.5, vel=1.0):
        nb = int(d * SR); tb = np.arange(nb) / SR
        v = sum(a * np.sin(2 * np.pi * fr * h * (1 + 0.0004 * h) * tb) * np.exp(-tb * (1.2 + 0.9 * h)) for h, a in
                ((1, 1.0), (2, 0.45), (3, 0.22), (4, 0.12), (5, 0.06)))
        return v * np.minimum(1, tb / 0.004) * 0.26 * vel

    k = 0
    while k * compas < dur:
        raiz, tp = acs[k % len(acs)]
        f3 = _acorde(raiz, tp, cfg["octava"])               # tríada media
        f2 = _acorde(raiz, tp, cfg["octava"] - 1)
        a0 = k * compas
        # cuerdas: acorde largo, ataque lento, saws filtrados + vibrato
        nb = int((compas + 1.2) * SR); tb = np.arange(nb) / SR
        env = np.minimum(1, tb / 1.0) * np.minimum(1, np.maximum(0, compas + 1.2 - tb) / 1.2)
        c = 0
        for fr in (f2[0], f3[0], f3[1], f3[2]):
            for det in (-0.25, 0.25):
                ph = rng.random()
                vib = 1 + 0.003 * np.sin(2 * np.pi * 5.2 * tb + ph * 6)
                c = c + (2 * ((fr * (1 + det / 100) * np.cumsum(vib) / SR + ph) % 1) - 1)
        pon(cuerdas, a0 * SR, _lp(c * env * 0.03, 3200))
        # piano: arpegio lento en negras de medio tiempo (cada 2 negras a 143), motivo oscuro
        motivo = [0, 2, 1, 2, 0, 2, 1, 3] if k % 2 == 0 else [0, 2, 1, 2, 3, 2, 1, 2]
        notas = [f3[0], f3[1], f3[2], f3[0] * 2]
        for j, idx in enumerate(motivo):
            pon(piano, (a0 + j * negra) * SR, nota_piano(notas[idx], 2.2, 0.9 if j % 2 == 0 else 0.7))
        pon(piano, a0 * SR, nota_piano(f2[0], 3.5, 0.8))     # nota grave del acorde
        # 808 largo + pulso grave en corcheas (tras la intro)
        if intro <= a0 < fin:
            f0 = _acorde(raiz, tp, 1)[0]
            if f0 > 62: f0 /= 2
            nb = int(compas * SR); tb = np.arange(nb) / SR
            b = np.tanh(1.4 * np.sin(2 * np.pi * f0 * tb)) * np.exp(-tb / 2.8) * np.minimum(1, tb / 0.01) * 0.26
            pon(bajo, a0 * SR, b)
            for j in range(16):
                if j % 4 in (1, 3):
                    nb2 = int(negra * 0.45 * SR); tp2 = np.arange(nb2) / SR
                    pu = np.sin(2 * np.pi * f0 * 2 * tp2) * np.exp(-tp2 / 0.09) * 0.10
                    pon(bajo, (a0 + j * negra / 2) * SR, pu)
        k += 1

    # batería suave a medio tiempo: bombo 1 (+ síncopa), palmada con cuerpo en el 3, charles discretos
    m = 0; paso = negra / 2
    while m * paso < dur:
        T = m * paso; i0 = T * SR; p16 = m % 16
        dentro = intro <= T < fin
        if dentro and p16 in (0, 6, 10):
            nb = int(0.3 * SR); tb = np.arange(nb) / SR
            pon(bat, i0, np.sin(2 * np.pi * np.cumsum(46 + 90 * np.exp(-tb / 0.03)) / SR) * np.exp(-tb / 0.16) * 0.42)
        if dentro and p16 == 8:
            nc = int(0.35 * SR); rr = rng.normal(0, 1, nc)
            sn = (_lp(rr, 4500) - _lp(rr, 700)) * np.exp(-np.arange(nc) / SR / 0.09) * 0.32
            sn += np.sin(2 * np.pi * 180 * np.arange(nc) / SR) * np.exp(-np.arange(nc) / SR / 0.05) * 0.12
            pon(bat, i0, sn)
        if dentro and p16 % 2 == 0:
            nh = int(0.05 * SR); hh = rng.normal(0, 1, nh)
            pon(bat, i0, (hh - _lp(hh, 6500)) * np.exp(-np.arange(nh) / SR / 0.02) * (0.06 + 0.03 * (p16 % 4 == 2)))
        m += 1

    piano = _reverb(piano, 2.6, 0.38, semilla)
    cuerdas = _reverb(cuerdas, 3.0, 0.3, semilla + 1)
    bat = _reverb(bat, 1.2, 0.15, semilla + 2)
    g = 0.85 + 0.25 * E
    L = (piano * 0.9 + cuerdas * 1.0 + bajo + bat) * g
    R = (piano * 1.0 + cuerdas * 0.9 + bajo + bat) * g
    fade = (np.minimum(1, t / 0.12) * np.minimum(1, (dur - t) / 0.2)) if bucle else (np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 2.0))
    L, R = np.tanh(L * fade * 1.3), np.tanh(R * fade * 1.3)
    pico = max(np.abs(L).max(), np.abs(R).max(), 1e-6)
    est = np.stack([L, R], 1) / pico * 0.7
    with wave.open(salida, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
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
