"""Alineación y audio PROVISIONALES (sin voz) para montar antes de tener la locución de ElevenLabs.
Reparte el guion en DUR segundos por caracteres, con pausas en la puntuación. Uso: python3 provisional.py DIR"""
import json, os, subprocess, sys
DUR = round(len(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "guion.txt"), encoding="utf-8").read().split()) / 3.28 + 0.5, 2)  # ritmo natural de la voz v1 (152 palabras en 46,3 s)
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
txt = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "guion.txt"), encoding="utf-8").read().strip()
PAUSA = {".": 0.32, "?": 0.32, ":": 0.22, ",": 0.12}
peso = [0.0 if c == " " else 1.0 for c in txt]
extra = [PAUSA.get(c, 0.0) for c in txt]
inicio = 0.25
k = (DUR - 0.6 - sum(extra)) / (sum(peso) + 0.6 * peso.count(0.0))
t = inicio; ini, fin = [], []
for c, p, e in zip(txt, peso, extra):
    ini.append(round(t, 3)); t += p * k if p else k * 0.6; fin.append(round(t, 3)); t += e
json.dump({"characters": list(txt), "character_start_times_seconds": ini, "character_end_times_seconds": fin},
          open(os.path.join(out, "alineacion-provisional.json"), "w"), ensure_ascii=False)
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(DUR),
                       "-c:a", "libmp3lame", "-q:a", "4", os.path.join(out, "locucion-provisional.mp3")])
print("ok", round(t, 2))
