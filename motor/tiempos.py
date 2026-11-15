"""Tiempos: duración del audio, SRT, alineación de ElevenLabs y troceo de subtítulos.

CLI:  python3 -m motor.tiempos palabras <alineacion.json>   -> tiempos por palabra (para planificar escenas)
"""
import json
import re
import subprocess
import sys


def duracion(audio):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "csv=p=0", audio], text=True)
    return float(out.strip())


def _seg(ts):
    h, m, rest = ts.replace(",", ".").split(":")
    return int(h) * 3600 + int(m) * 60 + float(rest)


def leer_srt(ruta):
    with open(ruta, encoding="utf-8-sig") as fh:
        bloques = re.split(r"\n\s*\n", fh.read().strip())
    out = []
    for b in bloques:
        ls = b.strip().splitlines()
        if len(ls) < 3 or "-->" not in ls[1]:
            continue
        a, z = [x.strip() for x in ls[1].split("-->")]
        out.append({"inicio": _seg(a), "fin": _seg(z), "texto": "\n".join(ls[2:])})
    return out


def _ts(s):
    ms = int(round(s * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def escribir_srt(lineas, ruta):
    with open(ruta, "w", encoding="utf-8") as fh:
        for i, l in enumerate(lineas, 1):
            fh.write(f"{i}\n{_ts(l['inicio'])} --> {_ts(l['fin'])}\n{l['texto']}\n\n")


def palabras_de_alineacion(ruta):
    """Lee la respuesta de ElevenLabs /with-timestamps (o solo su campo 'alignment' /
    'normalized_alignment') y devuelve [{'texto', 'inicio', 'fin'}] por palabra."""
    with open(ruta, encoding="utf-8") as fh:
        d = json.load(fh)
    al = d.get("alignment") or d.get("normalized_alignment") or d
    ch = al["characters"]
    ini = al["character_start_times_seconds"]
    fin = al["character_end_times_seconds"]
    pal, cur, t0, t1 = [], "", None, None
    for c, a, b in zip(ch, ini, fin):
        if c.isspace():
            if cur:
                pal.append({"texto": cur, "inicio": t0, "fin": t1})
            cur, t0 = "", None
            continue
        if t0 is None:
            t0 = a
        cur += c
        t1 = b
    if cur:
        pal.append({"texto": cur, "inicio": t0, "fin": t1})
    return pal


def trocear(palabras, max_chars=26):
    """Agrupa palabras en subtítulos cortos (1–2 líneas), cortando en signos de puntuación."""
    out, grupo = [], []
    def cerrar():
        if grupo:
            out.append({"texto": " ".join(p["texto"] for p in grupo),
                        "inicio": grupo[0]["inicio"], "fin": grupo[-1]["fin"],
                        "palabras": [dict(p) for p in grupo]})
            grupo.clear()
    for p in palabras:
        largo = len(" ".join(x["texto"] for x in grupo + [p]))
        if grupo and largo > max_chars:
            cerrar()
        grupo.append(p)
        if p["texto"][-1] in ".,;:?!…":
            cerrar()
    cerrar()
    # sin huecos: cada subtítulo dura hasta que empieza el siguiente (máx +0,6 s)
    for a, b in zip(out, out[1:]):
        a["fin"] = min(b["inicio"], a["fin"] + 0.6)
    return out


def proporcional(guion, dur, max_chars=26):
    """Sin alineación: reparte el tiempo según los caracteres (aproximado)."""
    pal = guion.split()
    total = sum(len(p) + 1 for p in pal)
    t, out = 0.15, []
    escala = (dur - 0.3) / total
    for p in pal:
        d = (len(p) + 1) * escala
        out.append({"texto": p, "inicio": t, "fin": t + d})
        t += d
    return trocear(out, max_chars)


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "palabras":
        for p in palabras_de_alineacion(sys.argv[2]):
            print(f"{p['inicio']:7.2f} {p['fin']:7.2f}  {p['texto']}")
    else:
        print(__doc__)
