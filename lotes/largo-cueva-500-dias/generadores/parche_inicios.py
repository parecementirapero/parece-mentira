"""Arregla el fotograma 0 de las partes 2–5 del vertical (TikTok).

El subtítulo karaoke deja la última frase de la parte anterior en pantalla hasta la primera palabra de la parte nueva
(0,25 s), así que la parte empezaba con la frase de otra parte. Este script vuelve a renderizar solo esos instantes
(0,4 s por parte) con el subtítulo de la frase anterior cortado en el punto de corte, y escribe un clip por parte.
Además, el corte se mueve al primer fotograma ENTERO del plano nuevo (techo, +1 ms), para que el fotograma 0 de la parte
ya sea su primer plano.

Uso: python3 parche_inicios.py ep_vertical.json cortes_video.json SALIDA_DIR
Escribe SALIDA_DIR/inicio-N.mp4 (solo vídeo, 12 fotogramas) y SALIDA_DIR/cortes_fotograma.json.
"""
import json, math, os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from motor.render import Episodio  # noqa: E402

FPS, N = 30, 12
ep_ruta, cortes, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
P = json.load(open(cortes))["partes"]
fr = {p["parte"]: (0 if p["parte"] == 1 else math.ceil(p["inicio"] * FPS + 0.001)) for p in P}
ep = Episodio(ep_ruta)
ep.audio = None
for n, f in fr.items():
    if n == 1:
        continue
    t = f / FPS
    for b in ep.subs.l:                      # la frase que venía de la parte anterior se acaba en el corte
        if b["inicio"] < t < b["fin"]:
            b["fin"] = t - 1e-3
    d = os.path.join(out, f"_p{n}")
    mp4 = ep.render(d, t, t + N / FPS, 1)
    os.replace(mp4, os.path.join(out, f"inicio-{n}.mp4"))
json.dump({"fps": FPS, "fotograma_corte": fr, "fotogramas_parche": N}, open(os.path.join(out, "cortes_fotograma.json"), "w"), indent=1)
print(fr)
