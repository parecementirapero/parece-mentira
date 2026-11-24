"""Corta el vertical en las 5 partes de TikTok, con el MISMO audio del vídeo largo horizontal.

Uso: python3 partir.py VERTICAL.mp4 MEZCLA_HORIZONTAL.wav PARCHES_DIR SALIDA_DIR
- PARCHES_DIR es la salida de parche_inicios.py. Contiene cortes_fotograma.json (el primer fotograma de cada parte)
  e inicio-N.mp4 (los primeros fotogramas de las partes 2–5 vueltos a renderizar sin la frase de la parte anterior).
- Cortes en fotogramas exactos (30 fps): la suma de las partes es el vídeo entero, sin huecos ni solapes.
- Los cortes caen en el silencio entre bloques de voz (≈0,23 s antes de la primera palabra de cada parte), así que no cortan ninguna palabra.
- Fundido corto de audio (0,15 s) al principio de las partes 2–5 y al final de las 1–4, para que música y efectos no se corten en seco.
"""
import json, os, subprocess, sys

FPS = 30
mp4, mezcla, parches, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
C = json.load(open(os.path.join(parches, "cortes_fotograma.json")))
FR = {int(k): v for k, v in C["fotograma_corte"].items()}
NP = C["fotogramas_parche"]
total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4]))
nfr = int(round(total * FPS))
partes = sorted(FR)
res = []
VID = ["-c:v", "libx264", "-preset", "medium", "-b:v", "6M", "-maxrate", "9M", "-bufsize", "18M", "-pix_fmt", "yuv420p", "-r", str(FPS)]
for k, n in enumerate(partes):
    f0 = FR[n]
    f1 = nfr if k == len(partes) - 1 else FR[partes[k + 1]]
    a, b = f0 / FPS, f1 / FPS
    dur = b - a
    fades = []
    if k > 0: fades.append("afade=t=in:st=0:d=0.15")
    if k < len(partes) - 1: fades.append(f"afade=t=out:st={dur - 0.15:.3f}:d=0.15")
    af = ",".join(["aresample=48000"] + fades)
    dst = os.path.join(out, f"parte-{n}-de-5.mp4")
    if n == 1:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{a:.4f}", "-i", mp4, "-ss", f"{a:.4f}", "-t", f"{dur:.4f}", "-i", mezcla,
               "-map", "0:v", "-map", "1:a", "-frames:v", str(f1 - f0), "-af", af]
    else:
        a2 = (f0 + NP) / FPS
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(parches, f"inicio-{n}.mp4"), "-ss", f"{a2:.4f}", "-i", mp4,
               "-ss", f"{a:.4f}", "-t", f"{dur:.4f}", "-i", mezcla,
               "-filter_complex", f"[0:v]trim=end_frame={NP},setpts=PTS-STARTPTS[p];[1:v]trim=end_frame={f1 - f0 - NP},setpts=PTS-STARTPTS[r];[p][r]concat=n=2:v=1:a=0[v];[2:a]{af}[au]",
               "-map", "[v]", "-map", "[au]", "-frames:v", str(f1 - f0)]
    subprocess.check_call(cmd + VID + ["-c:a", "aac", "-b:a", "192k", "-ac", "2", "-movflags", "+faststart", dst])
    real = int(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v", "-count_frames", "-show_entries",
                                        "stream=nb_read_frames", "-of", "csv=p=0", dst]))
    res.append({"parte": n, "inicio_s": round(a, 3), "fin_s": round(b, 3), "duracion_s": round(dur, 3), "fotogramas": real,
                "fotogramas_esperados": f1 - f0, "archivo": os.path.basename(dst)})
    print(res[-1], flush=True)
json.dump({"fotogramas_total": nfr, "suma_partes": sum(r["fotogramas"] for r in res), "partes": res}, open(os.path.join(out, "partes.json"), "w"), indent=1)
print("total", nfr, "suma", sum(r["fotogramas"] for r in res))
