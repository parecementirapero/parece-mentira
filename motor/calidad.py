"""Control de calidad automático de un vídeo (2026-11-17, Nico). Reglas y fuentes: `motor/GUIA_CALIDAD.md`.

Uso:  python3 -m motor.calidad DIR/episodio.json [--mp4 DIR/out/video.mp4] [--md informe.md]
Sin --mp4 revisa solo el montaje (ritmo, zonas seguras, lectura, gancho, densidad, variedad, sonido).
Con --mp4 mide además el movimiento real (instantes quietos), el bucle (último fotograma frente al primero)
y la mezcla (música y efectos frente a la voz), usando los WAV que deja el render junto al MP4.

Devuelve una nota de 0 a 100 y una lista de avisos. ❌ = hay que arreglarlo antes de entregar; ⚠ = revisar;
ℹ = dato. La nota solo ordena: lo que manda es la lista. Código de salida 1 si hay algún ❌.
"""
import argparse, glob, json, os, re, subprocess, sys, wave

import numpy as np

W, H, FPS = 1080, 1920, 30
# Zona segura común a Shorts, Reels y TikTok (las guías no coinciden; se toma un valor prudente). Ver GUIA_CALIDAD §4.
SEG_ARRIBA, SEG_ABAJO, SEG_IZQ, SEG_DER = 240, 1400, 60, 900
LEER = lambda txt: 0.25 + len(txt) / 17


def _texto(h):
    txt = ((h.get("texto") or "") + " " + (h.get("unidad") or "")).strip()
    if h.get("contar"):
        txt = (f"{h['contar'][1]} " + txt).strip()
    return txt


def _caja(h):
    """Caja aproximada de un rótulo (centro x,y; Poppins Bold ≈ 0,6 em por letra; la unidad va al 36 %)."""
    tam = h.get("tam", 120)
    principal = (str(h["contar"][1]) if h.get("contar") else (h.get("texto") or ""))
    ancho = len(principal) * tam * 0.6 + len(h.get("unidad") or "") * tam * 0.36 * 0.62 + tam * 0.56
    alto = tam * 1.35
    x, y = h.get("x", 540), h.get("y", 960)
    return x - ancho / 2, y - alto / 2, x + ancho / 2, y + alto / 2


def _animado(e):
    return bool(e.get("anim")) or len(e.get("keys") or []) > 1 or e.get("tipo") in ("particulas", "agua") or bool(e.get("contar")) or bool(e.get("giro"))


def _wav_db(ruta, ganancia_db=0.0):
    with wave.open(ruta) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float64) / 32768
    if x.size == 0:
        return None, None
    rms = np.sqrt(np.mean(x ** 2)) + 1e-12
    return 20 * np.log10(rms) + ganancia_db, 20 * np.log10(np.abs(x).max() + 1e-12) + ganancia_db


def _ventanas(ruta, v=0.25):
    """RMS en dB por ventanas de `v` segundos."""
    with wave.open(ruta) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float64) / 32768
    x = x.reshape(-1, ch).mean(1)
    n = int(sr * v)
    x = x[: len(x) // n * n].reshape(-1, n)
    return 20 * np.log10(np.sqrt((x ** 2).mean(1)) + 1e-9)


def _a_wav(ruta):
    out = ruta + ".calidad.wav"
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", ruta, "-ac", "2", "-ar", "48000", out])
    return out


def _fotogramas(mp4, fps=10, w=90, h=160):
    raw = subprocess.check_output(["ffmpeg", "-loglevel", "error", "-i", mp4, "-vf", f"fps={fps},scale={w}:{h}", "-pix_fmt", "gray", "-f", "rawvideo", "-"])
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)


def analizar(ruta_ep, mp4=None):
    ep = json.load(open(ruta_ep, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(ruta_ep))
    S = sorted(ep["escenas"], key=lambda e: e["inicio"])
    dur = max(e["fin"] for e in S)
    avisos, datos, nota = [], {}, 100.0

    def av(nivel, texto, resta=0.0):
        nonlocal nota
        avisos.append((nivel, texto))
        nota -= resta

    # ---------------------------------------------------------------- 1. ritmo
    d = np.array([e["fin"] - e["inicio"] for e in S])
    cv = float(d.std() / d.mean())
    datos["ritmo"] = dict(planos=len(d), cortes_min=round(len(d) / dur * 60, 1), mediana=round(float(np.median(d)), 2), min=round(float(d.min()), 2),
                          max=round(float(d.max()), 2), variacion=round(cv, 2), micro=int((d < 0.7).sum()), largos=int((d >= 2).sum()))
    if cv < 0.35: av("❌", f"Ritmo plano: casi todos los planos duran lo mismo (variación {cv:.2f}; hace falta ≥ 0,45). Mete micro planos de 0,3–0,7 s y alguno de 2–3 s.", 12)
    elif cv < 0.45: av("⚠", f"Ritmo poco variado (variación {cv:.2f}; mejor ≥ 0,45).", 5)
    if (d < 0.7).sum() < 3: av("⚠", "Menos de 3 micro planos (< 0,7 s): faltan golpes rápidos de detalle.", 4)
    if (d >= 2).sum() < 3: av("⚠", "Menos de 3 planos largos (≥ 2 s): no hay sitios donde respirar y entender.", 4)
    if d.max() > 4.5: av("⚠", f"Un plano dura {d.max():.1f} s: pártelo o métele una micro escena.", 4)
    if d.min() < 0.25: av("❌", f"Un plano dura {d.min():.2f} s: no da tiempo a verlo (mínimo 0,3 s).", 6)
    cm = len(d) / dur * 60
    if cm < 28: av("⚠", f"Pocos cambios de plano ({cm:.0f}/min; el método denso pide 35–50).", 5)
    if cm > 55: av("⚠", f"Demasiados cambios de plano ({cm:.0f}/min): por encima de 50 cansa.", 5)

    # ---------------------------------------------------------------- 2–3. rótulos: zona segura y lectura
    fuera, cortos, n_rot = [], [], 0
    for i, e in enumerate(S):
        for h in e["elementos"]:
            if h.get("tipo") != "rotulo" or not h.get("hud"):
                continue
            n_rot += 1
            txt = _texto(h)
            x0, y0, x1, y1 = _caja(h)
            donde = []
            if y1 > SEG_ABAJO: donde.append(f"abajo (llega a y={y1:.0f}; límite {SEG_ABAJO})")
            if y0 < SEG_ARRIBA: donde.append(f"arriba (y={y0:.0f}; límite {SEG_ARRIBA})")
            if x1 > SEG_DER and y1 > 800: donde.append(f"derecha, donde van los botones (x={x1:.0f}; límite {SEG_DER} por debajo de y=800)")
            if x0 < SEG_IZQ - 40 or x1 > W - SEG_IZQ + 40: donde.append(f"se sale por los lados (x={x0:.0f}…{x1:.0f})")
            if donde: fuera.append(f"«{txt}» (plano {i + 1}, {e['inicio']:.1f} s): " + ", ".join(donde))
            ks = h.get("keys") or []
            if len(ks) >= 2:
                visible = ks[-2]["t"] - ks[0]["t"]
                if visible + 1e-3 < LEER(txt): cortos.append(f"«{txt}» (plano {i + 1}): {visible:.2f} s, harían falta {LEER(txt):.2f} s")
    datos["rotulos"] = dict(total=n_rot, fuera_de_zona=len(fuera), sin_tiempo=len(cortos))
    if fuera:
        av("❌", f"{len(fuera)} rótulos fuera de la zona segura (los tapan los botones y textos de la app):\n      - " + "\n      - ".join(fuera[:12]) + ("\n      - …" if len(fuera) > 12 else ""), min(20, 2.5 * len(fuera)))
    if cortos:
        av("❌", f"{len(cortos)} rótulos sin tiempo para leerse:\n      - " + "\n      - ".join(cortos[:8]), min(15, 3 * len(cortos)))
    est = ep.get("estilo_subtitulos", {})
    ysub, tsub = est.get("y", 350), est.get("tam", 60)
    if ysub - tsub * 1.25 < SEG_ARRIBA: av("ℹ", f"El subtítulo (y={ysub}) roza la franja de arriba cuando ocupa dos líneas; y≈{int(SEG_ARRIBA + tsub * 1.35)} es más seguro.")
    choque = sum(1 for e in S for h in e["elementos"] if h.get("tipo") == "rotulo" and h.get("hud") and abs(_caja(h)[1] - ysub) < tsub * 1.6 and _caja(h)[1] < ysub + tsub * 2.2 and _caja(h)[3] > ysub - tsub * 1.2)
    if choque: av("⚠", f"{choque} rótulos pisan la franja del subtítulo (y≈{ysub}).", min(8, 2 * choque))

    # ---------------------------------------------------------------- 4. gancho
    g = {}
    al = (ep.get("subtitulos") or {}).get("alineacion") if isinstance(ep.get("subtitulos"), dict) else None
    if al and os.path.exists(al if os.path.isabs(al) else os.path.join(base, al)):
        from .tiempos import palabras_de_alineacion
        pal = palabras_de_alineacion(al if os.path.isabs(al) else os.path.join(base, al))
        n1 = next((i + 1 for i, p in enumerate(pal) if re.search(r"[.?!…]$", p["texto"])), len(pal))
        g = dict(palabras_primera_frase=n1, voz_empieza=round(pal[0]["inicio"], 2), fin_primera_frase=round(pal[n1 - 1]["fin"], 2),
                 palabras=len(pal), palabras_s=round(len(pal) / (pal[-1]["fin"] - pal[0]["inicio"]), 2))
        if n1 > 12: av("⚠", f"La primera frase tiene {n1} palabras: el gancho tiene que leerse de un vistazo (≤ 8 ideal, ≤ 12 máximo).", 5)
        if pal[0]["inicio"] > 0.5: av("⚠", f"La voz empieza en el segundo {pal[0]['inicio']:.2f}: que arranque antes de 0,4 s.", 4)
        if g["palabras_s"] > 3.3: av("⚠", f"Narración muy rápida ({g['palabras_s']} palabras/s): suena acelerada.", 4)
        if pal[-1]["fin"] > 59.3: av("❌", f"La locución acaba en {pal[-1]['fin']:.1f} s: el Short no puede pasar de 60 s.", 15)
    if not est.get("gancho"): av("⚠", "Sin `gancho`: en el fotograma 0 no se lee la primera frase entera (DECISIONS 2026-11-16).", 6)
    p0 = S[0]
    acc0 = [e for e in p0["elementos"] if any(0 < k.get("t", 0) <= 0.6 for k in (e.get("keys") or [])) or e.get("anim")]
    g["acciones_primer_plano"] = len(acc0)
    if not acc0: av("⚠", "En el primer plano no se mueve nada en los primeros 0,6 s: el gancho necesita acción desde el fotograma 0.", 6)
    datos["gancho"] = g

    # ---------------------------------------------------------------- 5–6. densidad y variedad
    n_el = [len(e["elementos"]) for e in S]
    quietos = [i + 1 for i, e in enumerate(S) if sum(_animado(x) for x in e["elementos"]) == 0 and e.get("camara", {}).get("zoom", [1, 1])[0] == e.get("camara", {}).get("zoom", [1, 1])[1]]
    pobres = [i + 1 for i, e in enumerate(S) if len(e["elementos"]) < 3 and e["fin"] - e["inicio"] > 1.0]
    fondos = [next((x["archivo"] for x in e["elementos"] if x.get("tipo") == "imagen" and x.get("ancho", 0) >= 1080), "|".join(e["fondo"]["colores"])) for e in S]
    svgs = {x["archivo"] for e in S for x in e["elementos"] if x.get("tipo") == "imagen"}
    racha, t0, peor = fondos[0], S[0]["inicio"], 0.0
    for e, f in zip(S, fondos):
        if f != racha: racha, t0 = f, e["inicio"]
        peor = max(peor, e["fin"] - t0)
    datos["imagen"] = dict(elementos_por_plano=round(float(np.mean(n_el)), 1), ilustraciones=len(svgs), fondos_distintos=len(set(fondos)), mismo_fondo_max_s=round(peor, 1))
    if quietos: av("❌", f"Planos sin nada que se mueva: {quietos}.", min(12, 4 * len(quietos)))
    if pobres: av("⚠", f"Planos de más de 1 s con menos de 3 elementos: {pobres}.", min(8, 2 * len(pobres)))
    if np.mean(n_el) < 5: av("⚠", f"Poca densidad: {np.mean(n_el):.1f} elementos por plano de media (la referencia tiene 7–8).", 5)
    if len(set(fondos)) < max(4, dur / 9): av("⚠", f"Pocos fondos distintos ({len(set(fondos))}) para {dur:.0f} s.", 4)
    if peor > 12: av("ℹ", f"El mismo fondo se mantiene {peor:.0f} s seguidos: valora otra paleta o un inserto.")

    # ---------------------------------------------------------------- 7. sonido (montaje)
    fx = ep.get("sfx") or []
    tipos = {}
    for e in fx: tipos[e["tipo"]] = tipos.get(e["tipo"], 0) + 1
    ts = np.array(sorted(e["t"] for e in fx)) if fx else np.array([])
    pico_dens = int(max((np.sum((ts >= t) & (ts < t + 1)) for t in ts), default=0))
    silencios = []
    if len(ts):
        borde = np.concatenate([[0], ts, [dur]])
        silencios = [(round(float(a), 1), round(float(b - a), 1)) for a, b in zip(borde, borde[1:]) if b - a > 4]
    fuertes = [e for e in fx if e.get("db", -14) > -9]
    datos["sonido"] = dict(efectos=len(fx), por_minuto=round(len(fx) / dur * 60), tipos=len(tipos), whoosh_min=round(tipos.get("whoosh", 0) / dur * 60, 1),
                           max_en_1s=pico_dens, musica_db=(ep.get("musica") or {}).get("db", -17))
    if not fx: av("⚠", "Sin efectos de sonido: lo que pasa en pantalla no suena.", 8)
    if tipos.get("whoosh", 0) / dur * 60 > 18: av("⚠", f"Demasiados «whoosh» ({tipos['whoosh']}): tapan la música y cansan.", 5)
    if pico_dens > 9: av("⚠", f"Hasta {pico_dens} efectos en un mismo segundo: satura.", 3)
    if len(tipos) < 5 and fx: av("ℹ", f"Solo {len(tipos)} tipos de efecto: más variedad (cada acción, su sonido).")
    if silencios: av("ℹ", "Tramos de más de 4 s sin ningún efecto: " + ", ".join(f"{a} s ({b} s)" for a, b in silencios[:5]))
    if len(fuertes) > 6: av("ℹ", f"{len(fuertes)} efectos a más de −9 dB: que los fuertes sean pocos (golpes y remates).")
    if not ep.get("musica"): av("⚠", "Sin música de fondo.", 5)

    # ---------------------------------------------------------------- 8–10. con el MP4: movimiento, bucle, mezcla
    if mp4 and os.path.exists(mp4):
        f = _fotogramas(mp4)
        dif = np.abs(np.diff(f, axis=0)).mean(axis=(1, 2))
        quieto = dif < 0.35
        tramos, ini = [], None
        for i, q in enumerate(quieto):
            if q and ini is None: ini = i
            if (not q or i == len(quieto) - 1) and ini is not None:
                if (i - ini) / 10 >= 0.8: tramos.append((round(ini / 10, 1), round((i - ini) / 10, 1)))
                ini = None
        bucle = float(np.abs(f[2] - f[-3]).mean())
        datos["movimiento"] = dict(quieto_pct=round(float(quieto.mean() * 100), 1), tramos_quietos=tramos, movimiento_medio=round(float(dif.mean()), 2),
                                   bucle_diferencia=round(bucle, 1))
        if tramos: av("⚠", "Tramos casi quietos de más de 0,8 s: " + ", ".join(f"{a} s ({b} s)" for a, b in tramos[:6]), min(8, 2 * len(tramos)))
        if bucle > 45: av("ℹ", f"El último fotograma no se parece al primero (diferencia {bucle:.0f}/255): el vídeo no enlaza en bucle. Los bucles suben el % visto.")
        d_out = os.path.dirname(mp4)
        mus = glob.glob(os.path.join(d_out, "*_musica.wav")); sf = glob.glob(os.path.join(d_out, "*_sfx.wav"))
        voz = ep.get("audio")
        voz = voz if voz and os.path.isabs(voz) else (os.path.join(base, voz) if voz else None)
        mez = {}
        if voz and os.path.exists(voz):
            vw = _a_wav(voz); v_rms, v_pico = _wav_db(vw); v_win = _ventanas(vw); os.remove(vw)
            if v_rms is not None and v_rms > -70:
                mez["voz_rms"] = round(v_rms, 1)
                if mus:
                    m_rms, _ = _wav_db(mus[0], (ep.get("musica") or {}).get("db", -17))
                    mez["musica_bajo_voz_db"] = round(m_rms - v_rms, 1)
                    # antes de la atenuación automática bajo la voz (sidechain), que quita varios dB más mientras se habla
                    if m_rms - v_rms > -5: av("⚠", f"La música queda solo {v_rms - m_rms:.0f} dB por debajo de la voz (antes de la atenuación automática): puede taparla. Objetivo: 6–16 dB.", 5)
                    if m_rms - v_rms < -18: av("⚠", f"La música queda {v_rms - m_rms:.0f} dB por debajo de la voz: casi no se oye. Objetivo: 6–16 dB.", 5)
                if sf:
                    s_rms, s_pico = _wav_db(sf[0])
                    mez["sfx_pico_frente_a_voz_db"] = round(s_pico - v_pico, 1)
                    mez["sfx_rms_bajo_voz_db"] = round(s_rms - v_rms, 1)
                    if s_pico - v_pico > 0: av("⚠", f"Algún efecto pica {s_pico - v_pico:.0f} dB por encima de la voz.", 4)
                    s_win = _ventanas(sf[0])
                    k = min(len(s_win), len(v_win))
                    tapa = np.where((v_win[:k] > -38) & (s_win[:k] > v_win[:k] - 3))[0]
                    grupos = []
                    for i in tapa:
                        if grupos and i * 0.25 - grupos[-1][1] <= 0.5: grupos[-1][1] = i * 0.25
                        else: grupos.append([i * 0.25, i * 0.25])
                    mez["efectos_que_tapan_voz"] = len(grupos)
                    atenua = ep.get("sfx_bajo_voz", True)
                    if grupos:
                        av("ℹ" if atenua else "⚠", f"En {len(grupos)} momentos un efecto suena tan alto como la voz de ese instante"
                           + (" (al mezclar, el motor los atenúa bajo la voz)" if atenua else " y no está activada la atenuación (`sfx_bajo_voz`)") + ": "
                           + ", ".join(f"{a:.1f} s" for a, _ in grupos[:10]) + ("…" if len(grupos) > 10 else ""), 0 if atenua else min(8, len(grupos)))
        if mez: datos["mezcla"] = mez

    datos["nota"] = max(0, round(nota))
    datos["avisos"] = avisos
    return datos


def informe(datos, titulo=""):
    L = [f"# Control de calidad{' — ' + titulo if titulo else ''}", "", f"**Nota: {datos['nota']}/100**", ""]
    for k in ("ritmo", "rotulos", "gancho", "imagen", "sonido", "movimiento", "mezcla"):
        if k in datos:
            L.append(f"- **{k}**: " + " · ".join(f"{a}={b}" for a, b in datos[k].items() if a != "tramos_quietos"))
    L.append("")
    orden = {"❌": 0, "⚠": 1, "ℹ": 2}
    for nivel, txt in sorted(datos["avisos"], key=lambda a: orden[a[0]]):
        L.append(f"- {nivel} {txt}")
    if not datos["avisos"]: L.append("- ✓ Sin avisos.")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episodio"); ap.add_argument("--mp4"); ap.add_argument("--md")
    a = ap.parse_args(argv)
    datos = analizar(a.episodio, a.mp4)
    txt = informe(datos, os.path.basename(os.path.dirname(os.path.abspath(a.episodio))))
    print(txt)
    if a.md: open(a.md, "w", encoding="utf-8").write(txt)
    sys.exit(1 if any(n == "❌" for n, _ in datos["avisos"]) else 0)


if __name__ == "__main__":
    main()
