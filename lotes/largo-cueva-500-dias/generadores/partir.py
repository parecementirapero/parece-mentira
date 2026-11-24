"""Corta el vertical en las 5 partes de TikTok, con el MISMO audio del vídeo largo horizontal.

Uso: python3 partir.py VERTICAL.mp4 MEZCLA_HORIZONTAL.wav cortes_video.json SALIDA_DIR
- Cortes en fotogramas exactos (30 fps): la suma de las partes = el vídeo entero, sin huecos ni solapes.
- Los cortes caen en el silencio entre bloques de voz (0,25 s antes de la primera palabra de cada parte), así que no cortan ninguna palabra.
- Fundido corto de audio (0,15 s) al principio de las partes 2–5 y al final de las 1–4, para que música y efectos no se corten en seco.
"""
import json, os, subprocess, sys

FPS = 30
mp4, mezcla, cortes, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
P = json.load(open(cortes))["partes"]
total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4]))
nfr = int(round(total * FPS))
res = []
for k, p in enumerate(P):
    f0 = int(round(p["inicio"] * FPS))
    f1 = nfr if k == len(P) - 1 else int(round(P[k + 1]["inicio"] * FPS))
    a, b = f0 / FPS, f1 / FPS
    dur = b - a
    fades = []
    if k > 0: fades.append("afade=t=in:st=0:d=0.15")
    if k < len(P) - 1: fades.append(f"afade=t=out:st={dur - 0.15:.3f}:d=0.15")
    af = ",".join(["aresample=48000"] + fades)
    dst = os.path.join(out, f"parte-{p['parte']}-de-5.mp4")
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{a:.4f}", "-i", mp4, "-ss", f"{a:.4f}", "-t", f"{dur:.4f}", "-i", mezcla,
                           "-map", "0:v", "-map", "1:a", "-frames:v", str(f1 - f0), "-af", af,
                           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
                           "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-movflags", "+faststart", dst])
    real = float(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v", "-count_frames", "-show_entries",
                                          "stream=nb_read_frames", "-of", "csv=p=0", dst]))
    res.append({"parte": p["parte"], "inicio_s": round(a, 3), "fin_s": round(b, 3), "duracion_s": round(dur, 3), "fotogramas": int(real),
                "fotogramas_esperados": f1 - f0, "archivo": os.path.basename(dst)})
    print(res[-1])
json.dump({"fotogramas_total": nfr, "suma_partes": sum(r["fotogramas"] for r in res), "partes": res}, open(os.path.join(out, "partes.json"), "w"), indent=1)
print("total", nfr, "suma", sum(r["fotogramas"] for r in res))
