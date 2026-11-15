"""Pasa un episodio v1 del lote 2026-11-15-tarde al estilo del motor v2 (DECISIONS.md, motor/OBJETIVO.md).

- Reajusta los tiempos de cada escena a la locución v2 (guion ampliado a 45–60 s) emparejando las
  palabras de la alineación v1 con las de la v2: lo añadido estira la escena en la que cae.
- Subtítulo karaoke arriba con palabras clave, transiciones v2, rótulos de dato, música generada y grano.
- Baja los elementos que ocupaban la franja del karaoke (y < LIM) para que no se tapen.

Uso: python3 a_v2.py NN episodio_v1.json alineacion_v1.json alineacion_v2.json DIR_SALIDA
"""
import copy, difflib, json, os, re, sys, unicodedata

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from motor.tiempos import palabras_de_alineacion  # noqa: E402

LIM, BAJA = 520, 230

CONF = {
    "01": dict(slug="guerra-38-minutos", musica={"generar": "curiosidad", "semilla": 7},
               claves=["fútbol", "Zanzíbar", "ultimátum", "atrincheró", "fuego", "ruinas", "treinta", "ocho", "minutos", "quinientos", "solo", "menos"],
               rotulos=[("cruceros", 1, "5", "BARCOS", 540, 1560), ("treinta", 1, "38", "MIN", 540, 1600),
                        ("quinientos", 1, "500", "BAJAS", 540, 1560), ("registrada", 1, "RÉCORD", "MUNDIAL", 540, 1600)]),
    "02": dict(slug="luna-se-aleja", musica={"generar": "curiosidad", "semilla": 3},
               claves=["uñas", "tres", "coma", "ocho", "centímetros", "espejos", "láser", "kilómetros", "mareas", "segundo", "mañana"],
               rotulos=[("coma", 1, "3,8", "CM/AÑO", 540, 1560), ("sesenta", 1, "1969", "APOLO 11", 540, 1640),
                        ("ochenta", 1, "384.000", "KM", 680, 1720), ("segundo", 1, "+1 s", "CADA 40.000 AÑOS", 540, 1600)]),
    "03": dict(slug="moais-con-cuerpo", musica={"generar": "misterio", "semilla": 5},
               claves=["cabezas", "pista", "Rano", "Raraku", "torso", "erosión", "grabados", "diez", "metros", "mitad"],
               rotulos=[("ciento", 1, "150", "ESTATUAS", 540, 1560), ("catorce,", 1, "1914", "EXCAVACIÓN", 540, 1560),
                        ("casi", 2, "~1.000", "MOÁIS", 540, 1640), ("diez", 2, "10 m", "DE ALTO", 360, 1640)]),
}
ENTRADA = {"barrido": "desenfoque", "fundido": "zoom", "corte": "corte", None: None}


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def mapeo(p1, p2):
    a, b = [norm(p["texto"]) for p in p1], [norm(p["texto"]) for p in p2]
    pares = [(0.0, 0.0)]
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            pares.append((p1[blk.a + k]["inicio"], p2[blk.b + k]["inicio"]))
    pares.sort()

    def f(t):
        for (x0, y0), (x1, y1) in zip(pares, pares[1:]):
            if x0 <= t <= x1:
                return y0 if x1 == x0 else y0 + (t - x0) * (y1 - y0) / (x1 - x0)
        x0, y0 = pares[-1]
        return y0 + (t - x0)
    return f


def escalar_t(obj, r):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "keys" and isinstance(v, list):
                for kf in v:
                    if "t" in kf:
                        kf["t"] = round(kf["t"] * r, 3)
            elif k == "contar" and isinstance(v, list) and len(v) == 3:
                v[2] = round(v[2] * r, 3)
            elif k == "contar_desde":
                obj[k] = round(v * r, 3)
            else:
                escalar_t(v, r)
    elif isinstance(obj, list):
        for x in obj:
            escalar_t(x, r)


def bajar(el):
    """Baja elementos de primer nivel cuyo centro cae en la franja del karaoke."""
    if el.get("tipo") in ("suelo", "particulas", "agua") or (el.get("tipo") == "brillo" and el.get("radio", 0) > 300):
        return
    ys = [el["y"]] if isinstance(el.get("y"), (int, float)) else []
    ys += [k["y"] for k in el.get("keys", []) if isinstance(k.get("y"), (int, float))]
    if ys and max(ys) < LIM and min(ys) > -100:
        if isinstance(el.get("y"), (int, float)):
            el["y"] += BAJA
        for k in el.get("keys", []):
            if isinstance(k.get("y"), (int, float)):
                k["y"] += BAJA


def pop(t0, t1):
    return [{"t": t0, "escala": 0.0, "op": 0}, {"t": t0 + 0.08, "op": 1}, {"t": t0 + 0.35, "escala": 1.0, "ease": "rebote"},
            {"t": t1, "escala": 1.0, "op": 1}, {"t": t1 + 0.25, "escala": 0.6, "op": 0}]


def main():
    n, ep1, al1, al2, out = sys.argv[1:6]
    c = CONF[n]
    ep = json.load(open(ep1))
    p1, p2 = palabras_de_alineacion(al1), palabras_de_alineacion(al2)
    f = mapeo(p1, p2)
    fin_audio = p2[-1]["fin"] + 0.5
    escenas = ep["escenas"]
    for i, e in enumerate(escenas):
        i0 = 0.0 if i == 0 else f(e["inicio"])
        i1 = fin_audio if i == len(escenas) - 1 else f(e["fin"])
        r = (i1 - i0) / (e["fin"] - e["inicio"])
        escalar_t(e.get("elementos", []), r)
        if "camara" in e:
            pass  # zoom/pan van de inicio a fin de escena: se estiran solos
        e["inicio"], e["fin"] = round(i0, 3), round(i1, 3)
        if "entrada" in e:
            e["entrada"] = ENTRADA.get(e["entrada"], e["entrada"])
            if e["entrada"] in ("desenfoque", "zoom"):
                e["dur_entrada"] = 0.4
        for el in e.get("elementos", []):
            bajar(el)
    # el fin de cada escena = inicio de la siguiente
    for a, b in zip(escenas, escenas[1:]):
        a["fin"] = b["inicio"]
    # rótulos de dato en el momento en que se dicen
    for palabra, nth, texto, unidad, rx, ry in c["rotulos"]:
        hits = [j for j, p in enumerate(p2) if norm(p["texto"]) == norm(palabra)]
        if len(hits) < nth:
            print("rótulo sin palabra:", palabra)
            continue
        w = hits[nth - 1]
        t = p2[w]["inicio"]
        e = next(e for e in escenas if e["inicio"] <= t < e["fin"])
        rel = t - e["inicio"]
        dur = min(2.6, e["fin"] - t - 0.3)
        e["elementos"].append({"tipo": "rotulo", "texto": texto, "unidad": unidad, "tam": 116, "x": rx, "y": ry,
                               "z": 0.3, "keys": pop(rel, rel + max(dur, 0.8))})
    ep.update({
        "id": f"2026-11-15-tarde-{n}-{c['slug']}", "version": 2,
        "audio": f"{n}-locucion.mp3",
        "subtitulos": {"alineacion": f"{n}-alineacion-original.json", "max_chars": 26},
        "estilo_subtitulos": {"modo": "karaoke", "y": 300, "tam": 62, "claves": c["claves"]},
        "musica": c["musica"], "lufs": -19, "grano": 0.035,
    })
    os.makedirs(out, exist_ok=True)
    json.dump(ep, open(os.path.join(out, "episodio.json"), "w"), ensure_ascii=False, indent=1)
    print(os.path.join(out, "episodio.json"), "dur", round(fin_audio, 2), "escenas", len(escenas))


if __name__ == "__main__":
    main()
