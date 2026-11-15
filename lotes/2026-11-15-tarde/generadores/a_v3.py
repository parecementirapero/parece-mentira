"""v2 → v3 del lote 2026-11-15-tarde con las reglas de motor/REFERENCIAS_2.md, sin tocar el audio.

- Trocea cada escena en planos de ~2,8 s (cortes en el inicio de una palabra): general → primer plano →
  detalle, con camara.foco sobre el objeto principal y el segundo objeto de la escena.
- Rótulos de dato como HUD (no se cortan al acercar), término clave en amarillo inclinado y etiqueta
  roja de contexto bajo el subtítulo, en el momento en que se dicen.
- Viñeta más marcada en escenas oscuras.

Uso: python3 a_v3.py NN episodio_v2.json alineacion_v2.json DIR_SALIDA [focos.json]
"""
import copy, json, os, re, sys, unicodedata

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from motor.tiempos import palabras_de_alineacion  # noqa: E402

PLANO = 2.8          # duración objetivo de un plano (s)
MIN_PLANO = 1.5
FONDOS = {"suelo", "particulas", "agua", "brillo", "rayos"}

CONF = {
    "01": dict(
        amarillo=[("ultimátum", 1, "ULTIMÁTUM"), ("yate", 1, "YATE REAL"), ("cañoneras", 1, "CAÑONERAS"),
                  ("ruinas", 1, "EN RUINAS"), ("desigual", 1, "500 CONTRA 1")],
        contexto=[("Zanzíbar", 1, "27 AGO 1896 · ZANZÍBAR"), ("sultán", 1, "MUERE EL SULTÁN"),
                  ("nueve", 1, "09:02 · EMPIEZA"), ("cuarenta", 1, "09:40 · FIN"), ("Londres", 1, "SULTÁN NUEVO")]),
    "02": dict(
        amarillo=[("espejos", 1, "RETRORREFLECTORES"), ("láser", 1, "LÁSER"), ("mareas", 1, "MAREAS"),
                  ("órbita", 1, "ÓRBITA MÁS AMPLIA")],
        contexto=[("uñas", 1, "UÑA ≈ LUNA"), ("dispara", 1, "TIERRA → LUNA → TIERRA"),
                  ("vuelta", 1, "IDA Y VUELTA ≈ 2,5 s"), ("días", 1, "EL DÍA SE ALARGA")]),
    "03": dict(
        amarillo=[("Raraku,", 1, "CANTERA"), ("torso", 1, "TORSO ENTERRADO"), ("erosión", 1, "EROSIÓN"),
                  ("grabados", 1, "GRABADOS")],
        contexto=[("volcán", 1, "RANO RARAKU"), ("arqueólogos", 1, "1914 · PRIMERA EXCAVACIÓN"),
                  ("Tilburg", 1, "2010–2014 · VAN TILBURG"), ("isla", 2, "ISLA DE PASCUA")]),
}


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def desplazar(obj, d):
    """Resta d a los tiempos relativos (keys, contar_desde) para que el plano empiece en 0."""
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k == "keys" and isinstance(v, list):
                for kf in v:
                    if "t" in kf:
                        kf["t"] = round(kf["t"] - d, 3)
            elif k == "contar_desde":
                obj[k] = round(v - d, 3)
            elif k == "fase" and isinstance(v, (int, float)):
                obj[k] = v + d
            else:
                desplazar(v, d)
    elif isinstance(obj, list):
        for x in obj:
            desplazar(x, d)


def pos(el, t=1.0):
    x, y = el.get("x"), el.get("y")
    for k in el.get("keys", []):
        if k.get("t", 0) <= t:
            x, y = k.get("x", x), k.get("y", y)
    if x is None and el.get("tipo") in ("flecha",) and el.get("puntos"):
        p = el["puntos"][len(el["puntos"]) // 2]
        return p
    return (x if x is not None else 540, y if y is not None else 960)


def tam(el):
    if el.get("tipo") in FONDOS or el.get("tipo") == "rotulo":
        return 0
    if "radio" in el:
        return 2 * el["radio"] * el.get("escala", 1)
    a = el.get("ancho") or el.get("alto") or 0
    if el.get("tipo") == "persona":
        a = el.get("alto", 300)
    if el.get("tipo") == "forma" and el.get("ancho", 0) >= 1000:   # fondos rectangulares
        return 0
    return a


def focos_auto(escena):
    els = [e for e in escena["elementos"] if tam(e) > 0]
    els.sort(key=tam, reverse=True)
    if not els:
        return (540, 960), (540, 960)
    a = pos(els[0])
    b = pos(els[1]) if len(els) > 1 else a
    return a, b


def corte_en_palabra(t, palabras, lo, hi):
    cands = [p["inicio"] for p in palabras if lo <= p["inicio"] <= hi]
    return min(cands, key=lambda x: abs(x - t)) if cands else t


def hud_rotulo(texto, t_abs, escenas, dur, **k):
    e = next(e for e in escenas if e["inicio"] <= t_abs < e["fin"])
    rel = t_abs - e["inicio"]
    dur = min(dur, max(e["fin"] - t_abs - 0.15, 0.6))
    ks = [{"t": rel, "escala": 0.0, "op": 0}, {"t": rel + 0.06, "op": 1},
          {"t": rel + 0.3, "escala": 1.0, "ease": "rebote"}, {"t": rel + dur, "escala": 1.0, "op": 1},
          {"t": rel + dur + 0.2, "op": 0}]
    e["elementos"].append({"tipo": "rotulo", "texto": texto, "hud": True, "z": 1, "keys": ks, **k})


def buscar(palabras, palabra, nth):
    hits = [p for p in palabras if norm(p["texto"]) == norm(palabra)]
    return hits[nth - 1]["inicio"] if len(hits) >= nth else None


def main():
    n, ep2, al2, out = sys.argv[1:5]
    focos_man = json.load(open(sys.argv[5])) if len(sys.argv) > 5 else {}
    c = CONF[n]
    ep = json.load(open(ep2))
    pal = palabras_de_alineacion(al2)
    nuevas = []
    for i, e in enumerate(ep["escenas"]):
        for el in e["elementos"]:
            if el.get("tipo") == "rotulo":
                el["hud"] = True
        oscuro = any(x in json.dumps(e.get("fondo", {})).lower() for x in ("#0", "#1", "#2"))
        if oscuro:
            e["vineta"] = max(e.get("vineta", 0.5), 0.62)
        L = e["fin"] - e["inicio"]
        k = max(1, round(L / PLANO))
        cortes = [e["inicio"]]
        for j in range(1, k):
            ideal = e["inicio"] + L * j / k
            t = corte_en_palabra(ideal, pal, cortes[-1] + MIN_PLANO, e["fin"] - MIN_PLANO)
            if t - cortes[-1] >= MIN_PLANO and e["fin"] - t >= MIN_PLANO:
                cortes.append(t)
        cortes.append(e["fin"])
        hero, detalle = focos_auto(e)
        man = focos_man.get(str(i), {})
        hero, detalle = tuple(man.get("hero", hero)), tuple(man.get("detalle", detalle))
        tipos = man.get("planos") or ["general", "primer", "detalle", "primer", "general", "detalle"]
        for j, (a, b) in enumerate(zip(cortes, cortes[1:])):
            p = copy.deepcopy(e)
            d = a - e["inicio"]
            desplazar(p["elementos"], d)
            p["inicio"], p["fin"] = round(a, 3), round(b, 3)
            tipo = tipos[j % len(tipos)] if k > 1 else "general"
            if j > 0:
                p["entrada"] = "corte"
                p.pop("dur_entrada", None)
            if tipo == "primer":
                p["camara"] = {"zoom": [1.42, 1.52], "foco": [list(hero), list(hero)], "pan": [[0, 0], [0, 0]]}
            elif tipo == "detalle":
                p["camara"] = {"zoom": [1.85, 1.95], "foco": [list(detalle), list(detalle)], "pan": [[0, 0], [0, 0]]}
            nuevas.append(p)
    ep["escenas"] = nuevas
    for palabra, nth, texto in c["amarillo"]:
        t = buscar(pal, palabra, nth)
        if t is None:
            print("sin palabra:", palabra); continue
        hud_rotulo(texto, t, nuevas, 1.8, tam=96, color="#ffd23f", capsula=None, rot=-6, x=540, y=1330)
    for palabra, nth, texto in c["contexto"]:
        t = buscar(pal, palabra, nth)
        if t is None:
            print("sin palabra:", palabra); continue
        hud_rotulo(texto, t, nuevas, 2.6, tam=54, color="#ffffff", capsula="#c0392be6", borde="#ffffff30",
                   x=540, y=470)
    ep["version"] = 3
    os.makedirs(out, exist_ok=True)
    json.dump(ep, open(os.path.join(out, "episodio.json"), "w"), ensure_ascii=False, indent=1)
    dur = [s["fin"] - s["inicio"] for s in nuevas]
    print(n, "planos", len(nuevas), "media", round(sum(dur) / len(dur), 2), "s")


if __name__ == "__main__":
    main()
