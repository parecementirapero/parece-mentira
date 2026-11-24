"""Hoja de fotogramas de un tramo: python3 hoja_tramo.py ep.json T0 T1 PASO salida.jpg  (respeta MOTOR_FORMATO)."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from PIL import Image, ImageDraw, ImageFont
from motor.render import Episodio, FUENTE
from motor.core import W, H
import numpy as np
ep = Episodio(sys.argv[1]); t0, t1, paso = map(float, sys.argv[2:5])
ts = list(np.arange(t0, t1, paso))
tw, th = (216, 384) if H > W else (384, 216)
cols = 8 if H > W else 5
ims = [ep.frame(float(t)).resize((tw, th), Image.LANCZOS) for t in ts]
fil = (len(ims) + cols - 1) // cols
hoja = Image.new("RGB", (cols * (tw + 6), fil * (th + 26)), (20, 20, 24)); d = ImageDraw.Draw(hoja); f = ImageFont.truetype(FUENTE, 18)
for i, (t, m) in enumerate(zip(ts, ims)):
    x, y = (i % cols) * (tw + 6) + 3, (i // cols) * (th + 26) + 22
    hoja.paste(m, (x, y)); d.text((x, y - 20), f"{t:6.2f}s", font=f, fill=(230, 230, 230))
hoja.save(sys.argv[5], quality=85); print(sys.argv[5])
