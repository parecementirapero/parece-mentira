"""Acabado de imagen (post-proceso) para los MP4 del motor — PRUEBA 2026-11-16 (Nico).

Toma un MP4 ya renderizado y le añade, sin coste y sin descargas:
  1. Halo/bloom: las luces "sangran" un poco, como en película.
  2. Etalonado documental: LUT .cube generado aquí (negros levantados, curva en S suave,
     sombras frías y altas luces cálidas, saturación al 90 %), aplicado al 75 %.
  3. Textura de papel: ruido multi-octava fijo en modo luz suave.
  4. Capa de partículas en primer plano: bokeh desenfocado + motas de polvo con parpadeo,
     que se mueven por delante de todo (más cosas por fotograma, sensación de profundidad).
  5. Parpadeo de exposición muy leve y aberración cromática mínima.
  6. Grano animado solo en luminancia, codificado con -tune grain y tope de 8 Mb/s.

Uso:  python3 -m motor.acabado ENTRADA.mp4 SALIDA.mp4 [--fuerza 1.0]
"""
import argparse, json, os, subprocess, tempfile

import numpy as np
from PIL import Image

W, H, FPS = 1080, 1920, 30


def _ffprobe_dur(p):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", p])
    return float(json.loads(out)["format"]["duration"])


# ---------------------------------------------------------------- 2. LUT documental
def crear_lut(ruta, n=33):
    g = np.linspace(0, 1, n)
    b, gg, r = np.meshgrid(g, g, g, indexing="ij")  # R varía más rápido en .cube
    rgb = np.stack([r, gg, b], -1).reshape(-1, 3)
    luma = rgb @ np.array([0.2126, 0.7152, 0.0722])
    # saturación 0.9
    rgb = luma[:, None] + (rgb - luma[:, None]) * 0.9
    # curva en S suave
    s = rgb + 0.12 * (rgb - rgb ** 2) * (2 * rgb - 1) * -1  # baja sombras, sube luces
    s = np.clip(s, 0, 1)
    l2 = s @ np.array([0.2126, 0.7152, 0.0722])
    sombra = np.clip(1 - l2 / 0.45, 0, 1)[:, None]
    luz = np.clip((l2 - 0.55) / 0.45, 0, 1)[:, None]
    s = s + sombra * np.array([-0.025, 0.005, 0.035]) + luz * np.array([0.035, 0.012, -0.03])
    # negros levantados y blancos un pelo apagados (look de copia de película)
    s = 0.035 + s * 0.94
    s = np.clip(s, 0, 1)
    with open(ruta, "w") as f:
        f.write(f'TITLE "PM documental"\nLUT_3D_SIZE {n}\n')
        for v in s:
            f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
    return ruta


# ---------------------------------------------------------------- 3. papel
def crear_papel(ruta, semilla=7):
    rng = np.random.default_rng(semilla)
    acc = np.zeros((H, W), np.float32)
    for esc, peso in [(240, 0.5), (60, 0.35), (12, 0.35), (3, 0.5), (1, 0.4)]:
        h, w = max(2, H // esc), max(2, W // esc)
        n = Image.fromarray(rng.normal(0, 1, (h, w)).astype(np.float32), "F").resize((W, H), Image.BICUBIC)
        acc += np.asarray(n) * peso
    # fibras: trazos finos alargados en horizontal
    fib = Image.fromarray(rng.normal(0, 1, (H // 2, W // 16)).astype(np.float32), "F").resize((W, H), Image.BICUBIC)
    acc += np.asarray(fib) * 0.3
    acc = (acc - acc.mean()) / acc.std()
    img = np.clip(128 + acc * 14, 0, 255).astype(np.uint8)
    Image.fromarray(img, "L").convert("RGB").save(ruta)
    return ruta


# ---------------------------------------------------------------- 4. partículas en primer plano
def _sprite(radio, dureza):
    d = int(radio * 2 + 3)
    y, x = np.mgrid[:d, :d] - d / 2
    r = np.sqrt(x * x + y * y) / radio
    return np.clip(1 - r, 0, 1) ** dureza


def crear_particulas(ruta, dur, semilla=11, escala=2):
    """Capa negra con bokeh y polvo (se mezcla en 'pantalla'). Se genera a media resolución."""
    w, h = W // escala, H // escala
    rng = np.random.default_rng(semilla)
    nf = int(np.ceil(dur * FPS))
    cols = np.array([[1.0, 0.86, 0.62], [0.75, 0.85, 1.0], [1.0, 0.95, 0.85]])
    parts = []
    for _ in range(14):  # bokeh grande, lento y muy tenue
        parts.append(dict(x=rng.uniform(0, w), y=rng.uniform(0, h), vx=rng.uniform(-6, 6), vy=rng.uniform(-10, -3),
                          r=rng.uniform(25, 70), a=rng.uniform(0.05, 0.12), dz=1.2, c=cols[rng.integers(3)],
                          fl=rng.uniform(0.2, 0.6), ph=rng.uniform(0, 6.3)))
    for _ in range(90):  # motas de polvo pequeñas que parpadean
        parts.append(dict(x=rng.uniform(0, w), y=rng.uniform(0, h), vx=rng.uniform(-8, 8), vy=rng.uniform(-14, 4),
                          r=rng.uniform(1.2, 3.2), a=rng.uniform(0.25, 0.6), dz=1.6, c=cols[2],
                          fl=rng.uniform(1.0, 3.0), ph=rng.uniform(0, 6.3)))
    for p in parts:
        p["spr"] = _sprite(p["r"], p["dz"])
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv444p", ruta]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(nf):
        t = i / FPS
        lien = np.zeros((h, w, 3), np.float32)
        for p in parts:
            x = (p["x"] + p["vx"] * t + 6 * np.sin(t * 0.7 + p["ph"])) % (w + 140) - 70
            y = (p["y"] + p["vy"] * t) % (h + 140) - 70
            a = p["a"] * (0.65 + 0.35 * np.sin(t * p["fl"] * 6.28 + p["ph"]))
            s = p["spr"]
            d = s.shape[0]
            x0, y0 = int(x - d / 2), int(y - d / 2)
            xa, ya, xb, yb = max(0, x0), max(0, y0), min(w, x0 + d), min(h, y0 + d)
            if xa >= xb or ya >= yb:
                continue
            lien[ya:yb, xa:xb] += s[ya - y0:yb - y0, xa - x0:xb - x0, None] * a * p["c"]
        pr.stdin.write((np.clip(lien, 0, 1) * 255).astype(np.uint8).tobytes())
    pr.stdin.close()
    pr.wait()
    return ruta


# ---------------------------------------------------------------- montaje final
def aplicar(entrada, salida, fuerza=1.0, tmp=None):
    tmp = tmp or tempfile.mkdtemp(prefix="acabado_")
    dur = _ffprobe_dur(entrada)
    lut = crear_lut(os.path.join(tmp, "documental.cube"))
    papel = crear_papel(os.path.join(tmp, "papel.png"))
    part = crear_particulas(os.path.join(tmp, "particulas.mp4"), dur)
    f = fuerza
    fc = (
        f"[0:v]format=gbrp,split=2[base][hl];"
        f"[hl]curves=all='0/0 0.62/0 1/1',gblur=sigma=38[glow];"
        f"[base][glow]blend=all_mode=screen:all_opacity={0.38 * f:.3f}[b1];"
        f"[b1]split=2[o][g];[g]lut3d=file={lut}:interp=tetrahedral[gr];"
        f"[gr][o]blend=all_mode=normal:all_opacity={min(1, 0.75 * f):.3f}[b2];"
        f"[1:v]format=gbrp[pap];[b2][pap]blend=all_mode=softlight:all_opacity={min(1, 0.55 * f):.3f}[b3];"
        f"[2:v]scale={W}:{H}:flags=bicubic,format=gbrp[pt];[b3][pt]blend=all_mode=screen:all_opacity={min(1, f):.3f}:shortest=0[b4];"
        f"[b4]rgbashift=rh=-2:bh=2,"
        f"eq=brightness='{0.010 * f:.4f}*sin(2*PI*t*2.3)+{0.006 * f:.4f}*sin(2*PI*t*7.1)':eval=frame,"
        f"format=yuv420p,noise=c0s={round(9 * f)}:c0f=t+u[v]"
    )
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", entrada, "-loop", "1", "-framerate", str(FPS), "-i", papel,
           "-i", part, "-filter_complex", fc, "-map", "[v]", "-map", "0:a?", "-t", f"{dur:.3f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-tune", "grain", "-maxrate", "8M", "-bufsize", "16M",
           "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", salida]
    subprocess.check_call(cmd)
    return salida


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada")
    ap.add_argument("salida")
    ap.add_argument("--fuerza", type=float, default=1.0)
    a = ap.parse_args(argv)
    print(aplicar(a.entrada, a.salida, a.fuerza))


if __name__ == "__main__":
    main()
