"""Renderiza un episodio descrito en JSON a MP4 9:16.

Uso:
  python3 -m motor.render <episodio.json> [--salida DIR] [--hoja] [--cada 2] [--desde S --hasta S]

  --hoja     solo genera la hoja de fotogramas (1 cada --cada s) para revisar, sin vídeo
  --desde/--hasta  renderiza un tramo (pruebas rápidas)
"""
import argparse
import datetime as dt
import hashlib
import json
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .core import W, H, FPS, rgb, lerp_arr, vineta, EASE
from .elementos import crear
from . import tiempos
from .subtitulos import SubtitulosKaraoke
from . import musica as musica_mod

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTE = os.path.join(AQUI, "fuentes", "Poppins-Bold.ttf")


# ====================================================================== fondos
def fondo_img(spec):
    t = spec.get("tipo", "degradado")
    cols = spec.get("colores", ["#1b1f3b", "#0b0d1a"])
    if t == "radial":
        cx, cy = spec.get("centro", [W / 2, H * 0.35])
        y, x = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / spec.get("radio", H * 0.8)
        u = np.clip(d, 0, 1)
    else:
        u = np.linspace(0, 1, H, dtype=np.float32)[:, None].repeat(W, 1)
    if len(cols) == 3:
        arr = np.where((u < 0.5)[..., None], lerp_arr(cols[0], cols[1], np.clip(u * 2, 0, 1)),
                       lerp_arr(cols[1], cols[2], np.clip(u * 2 - 1, 0, 1)))
    else:
        arr = lerp_arr(cols[0], cols[1], u)
    # grano muy suave para que el degradado no haga bandas
    rng = np.random.default_rng(1)
    arr = arr + rng.normal(0, 1.4, arr.shape[:2])[..., None]
    out = np.concatenate([np.clip(arr, 0, 255), np.full((H, W, 1), 255.0)], 2).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


# ====================================================================== transiciones
def _desenfoque_h(img, k):
    """Desenfoque de movimiento horizontal barato (reducir y ampliar en x)."""
    if k < 2:
        return img
    return img.resize((max(8, int(W / k)), H), Image.BILINEAR).resize((W, H), Image.BILINEAR)


def _latigazo(prev, cur, u):
    """Barrido rápido de cámara con desenfoque de movimiento (como en los vídeos objetivo)."""
    k = 1 + 34 * math.sin(math.pi * u)
    off = int(W * u)
    comp = Image.new("RGBA", (W, H))
    comp.alpha_composite(_desenfoque_h(prev, k).crop((off, 0, W, H)), (0, 0))
    comp.alpha_composite(_desenfoque_h(cur, k).crop((0, 0, off, H)), (W - off, 0))
    return comp


def _zoom_paso(prev, cur, u):
    """Entra en la escena siguiente atravesando la anterior (zoom + fundido)."""
    z1 = 1 + 0.9 * u
    cw, ch = W / z1, H / z1
    a = prev.crop((int((W - cw) / 2), int((H - ch) / 2), int((W + cw) / 2), int((H + ch) / 2))).resize((W, H), Image.BILINEAR)
    z2 = 1.35 - 0.35 * u
    cw, ch = W / z2, H / z2
    b = cur.crop((int((W - cw) / 2), int((H - ch) / 2), int((W + cw) / 2), int((H + ch) / 2))).resize((W, H), Image.BILINEAR)
    return Image.blend(a, b, u)


# ====================================================================== escena
class Escena:
    def __init__(self, spec, base_dir):
        self.s = spec
        self.ini = float(spec["inicio"])
        self.fin = float(spec["fin"])
        self.fondo = fondo_img(spec.get("fondo", {}))
        self.elems = [crear(e, base_dir) for e in spec.get("elementos", [])]
        cam = spec.get("camara", {})
        self.zoom = cam.get("zoom", [1.0, 1.04])
        self.pan = cam.get("pan", [[0, 0], [0, -24]])
        self.temblor = cam.get("temblor", 0)
        self.entrada = spec.get("entrada", "fundido")
        self.dur_entrada = spec.get("dur_entrada", 0.35)
        self.vineta = spec.get("vineta", 0.5)

    def frame(self, t_abs, vin_cache):
        t = t_abs - self.ini
        dur = max(self.fin - self.ini, 1e-3)
        u = EASE["suave"](min(max(t / dur, 0), 1))
        dx = self.pan[0][0] + (self.pan[1][0] - self.pan[0][0]) * u
        dy = self.pan[0][1] + (self.pan[1][1] - self.pan[0][1]) * u
        if self.temblor:
            dx += self.temblor * math.sin(t * 23.0)
            dy += self.temblor * math.cos(t * 19.0)
        img = self.fondo.copy()
        for e in self.elems:
            e.dibujar(img, t, (dx, dy))
        z = self.zoom[0] + (self.zoom[1] - self.zoom[0]) * u
        if abs(z - 1) > 1e-3:
            cw, ch = W / z, H / z
            img = img.crop((int((W - cw) / 2), int((H - ch) / 2),
                            int((W + cw) / 2), int((H + ch) / 2))).resize((W, H), Image.BICUBIC)
        if self.vineta:
            k = round(self.vineta, 2)
            if k not in vin_cache:
                vin_cache[k] = vineta(k)
            img.alpha_composite(vin_cache[k])
        return img


# ====================================================================== subtítulos
class Subtitulos:
    def __init__(self, lineas, estilo):
        self.l = lineas
        self.e = estilo
        self.font = ImageFont.truetype(FUENTE, estilo.get("tam", 66))
        self.cache = {}

    def _render(self, texto):
        if texto in self.cache:
            return self.cache[texto]
        f = self.font
        maxw = self.e.get("ancho_max", 900)
        lineas = []
        for parte in texto.split("\n"):
            pal, cur = parte.split(), ""
            for p in pal:
                prueba = (cur + " " + p).strip()
                if f.getlength(prueba) > maxw and cur:
                    lineas.append(cur)
                    cur = p
                else:
                    cur = prueba
            if cur:
                lineas.append(cur)
        asc, desc = f.getmetrics()
        lh = int((asc + desc) * 1.08)
        w = int(max(f.getlength(x) for x in lineas)) + 80
        h = lh * len(lineas) + 80
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        sombra = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ds, d = ImageDraw.Draw(sombra), ImageDraw.Draw(img)
        for i, ln in enumerate(lineas):
            x = (w - f.getlength(ln)) / 2
            y = 40 + i * lh
            ds.text((x, y + 6), ln, font=f, fill=(0, 0, 10, 200), stroke_width=10, stroke_fill=(0, 0, 10, 200))
            d.text((x, y), ln, font=f, fill=(255, 255, 255, 255), stroke_width=self.e.get("contorno", 5),
                   stroke_fill=(16, 14, 32, 255))
        sombra = sombra.filter(ImageFilter.GaussianBlur(9))
        sombra.alpha_composite(img)
        self.cache[texto] = sombra
        return sombra

    def dibujar(self, lienzo, t):
        for ln in self.l:
            if ln["inicio"] <= t < ln["fin"]:
                spr = self._render(ln["texto"])
                k = min(1.0, (t - ln["inicio"]) / 0.12)
                esc = 0.9 + 0.1 * EASE["rebote"](k)
                if esc < 0.999:
                    spr = spr.resize((int(spr.width * esc), int(spr.height * esc)), Image.BICUBIC)
                if k < 1:
                    r, g, b, a = spr.split()
                    spr = Image.merge("RGBA", (r, g, b, a.point(lambda v: int(v * min(1, k * 1.5)))))
                cy = self.e.get("y", 1430)
                lienzo.alpha_composite(spr, (int((W - spr.width) / 2), int(cy - spr.height / 2)))
                return


# ====================================================================== episodio
class Episodio:
    def __init__(self, ruta):
        self.ruta = os.path.abspath(ruta)
        self.dir = os.path.dirname(self.ruta)
        with open(self.ruta, encoding="utf-8") as fh:
            self.s = json.load(fh)
        s = self.s
        self.audio = self._abs(s["audio"]) if s.get("audio") else None
        self.dur_audio = tiempos.duracion(self.audio) if self.audio else None
        self.duracion = float(s.get("duracion") or (self.dur_audio + s.get("cola", 0.5)))
        self.escenas = [Escena(e, self.dir) for e in s["escenas"]]
        self.escenas.sort(key=lambda e: e.ini)
        est = s.get("estilo_subtitulos", {})
        if est.get("modo", "karaoke") == "clasico":
            self.subs = Subtitulos(self._subtitulos(), est)
        else:
            self.subs = SubtitulosKaraoke(self._subtitulos(), est)
        self._vin = {}
        self.grano = float(s.get("grano", 0.0))
        self._granos = None

    def _abs(self, p):
        return p if os.path.isabs(p) else os.path.join(self.dir, p)

    def _subtitulos(self):
        s = self.s
        if "subtitulos" in s and isinstance(s["subtitulos"], list):
            return s["subtitulos"]
        src = s.get("subtitulos", {})
        if isinstance(src, dict) and src.get("srt"):
            return tiempos.leer_srt(self._abs(src["srt"]))
        if isinstance(src, dict) and src.get("alineacion"):
            pal = tiempos.palabras_de_alineacion(self._abs(src["alineacion"]))
            return tiempos.trocear(pal, src.get("max_chars", 26))
        if s.get("guion") and self.dur_audio:
            return tiempos.proporcional(s["guion"], self.dur_audio, src.get("max_chars", 26) if isinstance(src, dict) else 26)
        return []

    def escena_en(self, t):
        act = [e for e in self.escenas if e.ini <= t < e.fin + 1e-6]
        return act[-1] if act else self.escenas[-1]

    def frame(self, t):
        esc = self.escena_en(t)
        img = esc.frame(t, self._vin)
        i = self.escenas.index(esc)
        dt_ = t - esc.ini
        if i > 0 and esc.entrada != "corte" and dt_ < esc.dur_entrada:
            prev = self.escenas[i - 1].frame(t, self._vin)
            u = EASE["suave"](dt_ / esc.dur_entrada)
            if esc.entrada == "barrido":
                off = int(W * (1 - u))
                comp = prev.copy()
                comp.alpha_composite(img.crop((0, 0, W - off, H)), (off, 0))
                img = comp
            elif esc.entrada == "desenfoque":
                img = _latigazo(prev, img, u)
            elif esc.entrada == "zoom":
                img = _zoom_paso(prev, img, u)
            else:
                img = Image.blend(prev, img, u)
        self.subs.dibujar(img, t)
        out = img.convert("RGB")
        if self.grano > 0:
            out = self._con_grano(out, t)
        return out

    def _con_grano(self, img, t):
        # grano fijo (textura de papel): uno animado multiplica el peso del MP4 por 20
        if self._granos is None:
            rng = np.random.default_rng(7)
            g = rng.normal(0, 255 * self.grano, (H // 2, W // 2)).astype(np.float32)
            g = np.repeat(np.repeat(g, 2, 0), 2, 1)
            g = np.asarray(Image.fromarray(np.clip(g + 128, 0, 255).astype(np.uint8)).filter(
                ImageFilter.GaussianBlur(0.8)), np.float32) - 128
            self._granos = g[..., None]
        arr = np.asarray(img, np.float32) + self._granos
        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")

    # ------------------------------------------------------------------ salida
    def nombre(self):
        return f"{self.s['id']}_v{self.s.get('version', 1)}"

    def hoja(self, salida, cada=2.0):
        ts = list(np.arange(0.25, self.duracion, cada))
        miniaturas = [self.frame(float(t)).resize((270, 480), Image.LANCZOS) for t in ts]
        cols = 6
        filas = math.ceil(len(miniaturas) / cols)
        hoja = Image.new("RGB", (cols * 278, filas * 510), (20, 20, 24))
        d = ImageDraw.Draw(hoja)
        f = ImageFont.truetype(FUENTE, 20)
        for i, (t, m) in enumerate(zip(ts, miniaturas)):
            x, y = (i % cols) * 278 + 4, (i // cols) * 510 + 26
            hoja.paste(m, (x, y))
            d.text((x, y - 24), f"{t:5.2f}s", font=f, fill=(230, 230, 230))
        os.makedirs(salida, exist_ok=True)
        ruta = os.path.join(salida, self.nombre() + "_hoja.jpg")
        hoja.save(ruta, quality=88)
        return ruta

    def render(self, salida, desde=0.0, hasta=None):
        os.makedirs(salida, exist_ok=True)
        hasta = self.duracion if hasta is None else min(hasta, self.duracion)
        n = int(round((hasta - desde) * FPS))
        mp4 = os.path.join(salida, self.nombre() + ".mp4")
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
        audio = self._audio_final(salida) if self.audio else None
        if audio:
            cmd += ["-ss", f"{desde:.3f}", "-i", audio,
                    "-filter_complex", f"[1:a]apad,atrim=0:{hasta - desde:.3f},aresample=48000[a]",
                    "-map", "0:v", "-map", "[a]", "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-ar", "48000"]
        cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-maxrate", "8M", "-bufsize", "16M", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", "-t", f"{hasta - desde:.3f}", mp4]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for i in range(n):
            t = desde + i / FPS
            p.stdin.write(self.frame(t).tobytes())
            if i % 90 == 0:
                print(f"  {t:6.2f}s / {hasta:.2f}s", file=sys.stderr, flush=True)
        p.stdin.close()
        if p.wait() != 0:
            raise SystemExit("ffmpeg falló")
        srt = os.path.join(salida, self.nombre() + ".srt")
        tiempos.escribir_srt(self.subs.l, srt)
        self._manifiesto(salida, mp4, srt, n)
        return mp4

    def _audio_final(self, salida):
        """Voz sola (normalizada) o voz + música de fondo, a -19 LUFS (DECISIONS.md)."""
        m = self.s.get("musica")
        lufs = self.s.get("lufs", -19.0)
        mix = os.path.join(salida, self.nombre() + "_mezcla.wav")
        if not m:
            subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", self.audio, "-af",
                                   f"loudnorm=I={lufs}:TP=-1.5:LRA=11,aresample=48000", "-ac", "2", mix])
            return mix
        if m.get("archivo"):
            pista = self._abs(m["archivo"])
        else:
            pista = os.path.join(salida, self.nombre() + "_musica.wav")
            musica_mod.generar(pista, self.duracion + 0.2, m.get("generar", "curiosidad"), m.get("semilla", 1))
        self.musica_usada = pista
        return musica_mod.mezclar(self.audio, pista, mix, self.duracion, m.get("db", -17.0), lufs)

    def _manifiesto(self, salida, mp4, srt, n):
        def sha(p):
            h = hashlib.sha256()
            with open(p, "rb") as fh:
                for b in iter(lambda: fh.read(1 << 20), b""):
                    h.update(b)
            return h.hexdigest()
        try:
            commit = subprocess.check_output(["git", "-C", AQUI, "rev-parse", "--short", "HEAD"],
                                             text=True, stderr=subprocess.DEVNULL).strip()
        except Exception:
            commit = None
        ff = subprocess.check_output(["ffmpeg", "-version"], text=True).splitlines()[0]
        man = {
            "id": self.s["id"], "version": self.s.get("version", 1),
            "creado": dt.datetime.now().isoformat(timespec="seconds"),
            "duracion_s": round(self.duracion, 3), "fotogramas": n, "fps": FPS, "resolucion": [W, H],
            "sha256": {"mp4": sha(mp4), "srt": sha(srt), "episodio_json": sha(self.ruta),
                       "audio": sha(self.audio) if self.audio else None,
                       "musica": sha(self.musica_usada) if getattr(self, "musica_usada", None) else None},
            "musica": self.s.get("musica"),
            "motor_commit": commit, "ffmpeg": ff, "fuente": os.path.basename(FUENTE),
            "escenas": [{"inicio": e.ini, "fin": e.fin} for e in self.escenas],
        }
        with open(os.path.join(salida, self.nombre() + "_manifest.json"), "w", encoding="utf-8") as fh:
            json.dump(man, fh, ensure_ascii=False, indent=2)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episodio")
    ap.add_argument("--salida", default=None)
    ap.add_argument("--hoja", action="store_true")
    ap.add_argument("--cada", type=float, default=2.0)
    ap.add_argument("--desde", type=float, default=0.0)
    ap.add_argument("--hasta", type=float, default=None)
    a = ap.parse_args(argv)
    ep = Episodio(a.episodio)
    salida = a.salida or os.path.join(ep.dir, "out")
    if a.hoja:
        print(ep.hoja(salida, a.cada))
    else:
        print(ep.render(salida, a.desde, a.hasta))
        print(ep.hoja(salida, a.cada))


if __name__ == "__main__":
    main()
