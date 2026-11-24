"""Solo en el vertical: marcas de las 5 partes de TikTok sobre el montaje de un tirón.

- El primer plano de cada parte empieza 0,25 s antes de su primera palabra. Ahí se corta la parte, en el silencio entre bloques
  de voz, así que hay sitio para los fundidos.
- Al principio de cada parte: «PARTE N DE 5». En las partes 2–5, además, un gancho legible desde el fotograma 0 y con movimiento.
- En los últimos 2 s de las partes 1–4: «SIGUE EN LA PARTE N+1».
Las horas de corte resultantes se guardan en salida/cortes_video.json (las usa partir.py).
"""
import json, os

GANCHO = {2: "SIN SOL, TU RELOJ FALLA", 3: "DÍA 65: DEJA DE CONTAR", 4: "ARRIBA, NADIE TE ESPERA", 5: "DÍA 500: LA SALIDA"}
ADELANTO = 0.25


def _fijo(t0, t1, texto, **k):
    """Rótulo que ya está en pantalla en el fotograma 0 de su plano (sin aparecer desde cero) y late un poco."""
    ks = [{"t": t0, "escala": 1.0, "op": 1}, {"t": t0 + 0.35, "escala": 1.07, "ease": "salida"}, {"t": t0 + 0.75, "escala": 1.0, "ease": "suave"},
          {"t": t1, "escala": 1.0, "op": 1}, {"t": t1 + 0.15, "op": 0}]
    return {"tipo": "rotulo", "texto": texto, "hud": True, "z": 1, "keys": ks, "fijo": True, "sin_pop": True, **k}


def _sale(t0, t1, texto, **k):
    ks = [{"t": t0, "escala": 0.0, "op": 0}, {"t": t0 + 0.05, "op": 1}, {"t": t0 + 0.25, "escala": 1.0, "ease": "rebote"},
          {"t": t1, "escala": 1.0, "op": 1}, {"t": t1 + 0.12, "op": 0}]
    return {"tipo": "rotulo", "texto": texto, "hud": True, "z": 1, "keys": ks, "fijo": True, **k}


def poner(v, cortes, inicio_parte, partes):
    v.PLANOS.sort(key=lambda p: p[0])
    # 1) el primer plano de cada parte arranca 0,25 s antes de su primera palabra
    inicio = {}
    for n in partes:
        i0 = inicio_parte[n]
        t_pal = v.PAL[i0]["inicio"]
        k = next((j for j, p in enumerate(v.PLANOS) if abs(p[0] - v.w(i0)) < 1e-6), None)
        if k is None:
            raise SystemExit(f"La parte {n} no empieza con un plano propio en la palabra {i0}: añade un @plano({i0}, …)")
        ini = 0.0 if n == 1 else round(t_pal - ADELANTO, 3)
        v.PLANOS[k] = (ini, v.PLANOS[k][1], v.PLANOS[k][2])
        inicio[n] = ini
    fin_total = v.FIN
    fin = {n: (inicio.get(n + 1) if n + 1 in inicio else (cortes[n]["inicio"] - ADELANTO if n < 5 else fin_total)) for n in partes}
    # 2) rótulos atados al plano que esté en pantalla en cada momento
    marcas = []   # (t_abs0, t_abs1, fabrica)
    for n in partes:
        a, b = inicio[n], fin[n]
        marcas.append((a, a + 3.6, lambda t0, t1, n=n: _fijo(t0, t1, f"PARTE {n} DE 5", tam=50, color="#ffffff", capsula="#c0392be6", x=270, y=1260)))
        if n in GANCHO:
            marcas.append((a, a + 2.6, lambda t0, t1, n=n: _fijo(t0, t1, GANCHO[n], tam=70, color="#ffd23f", capsula="#0b0f1ee6", x=540, y=640)))
        if n < 5:
            marcas.append((b - 2.2, b - 0.12, lambda t0, t1, n=n: _sale(t0, t1, f"SIGUE EN LA PARTE {n + 1}", tam=52, color="#141414", capsula="#ffd23ff0", x=500, y=1260)))
    nuevos = []
    for j, (ini, nombre, fn) in enumerate(v.PLANOS):
        fin_p = v.PLANOS[j + 1][0] if j + 1 < len(v.PLANOS) else v.FIN
        mias = [(max(a, ini) - ini, min(b, fin_p) - ini, f) for a, b, f in marcas if a < fin_p - 1e-3 and b > ini + 1e-3]
        if mias:
            def envuelto(d, fn=fn, mias=mias):
                p = fn(d)
                for t0, t1, f in mias:
                    p["hud"] = list(p["hud"]) + [f(round(t0, 3), round(min(t1, d - 0.02), 3))]
                return p
            nuevos.append((ini, nombre, envuelto))
        else:
            nuevos.append((ini, nombre, fn))
    v.PLANOS[:] = nuevos
    json.dump({"partes": [{"parte": n, "inicio": inicio[n], "fin": fin[n]} for n in partes]},
              open(os.path.join(v.out, "cortes_video.json"), "w"), indent=1)
