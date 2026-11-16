"""Subtítulo karaoke arriba (estilo por defecto desde 2026-11-15, ver DECISIONS.md).

Cada bloque (1–2 líneas) aparece palabra a palabra al ritmo de la voz:
  - palabras ya dichas: gris translúcido (Poppins Medium)
  - palabra que suena: blanco (Poppins Bold), entra con un pequeño fundido
  - palabras clave: dentro de una cápsula oscura, desde que suenan hasta que cambia el bloque
  - palabras futuras: no se ven
El reparto en líneas se calcula con el bloque entero, así las palabras no saltan al aparecer.

estilo_subtitulos (episodio.json):
  modo: "karaoke" (por defecto) | "clasico" (blanco abajo con contorno, el de la v1)
  y: centro vertical del bloque (por defecto 350 ≈ 18 % de alto)
  tam: tamaño de letra (60)       ancho_max: ancho máximo de línea en px (860)
  claves: ["palabra", ...]  palabras resaltadas con cápsula (sin tildes ni signos da igual)
  color_dicha, color_actual, color_capsula: colores "#rrggbbaa"
  gancho: true | {"max_palabras": 16, "panel": true, "alfa": 225, "tam": 1,15 × tam}
      La primera frase (hasta . ? ! …) se ve ENTERA desde el fotograma 0, aunque la voz no
      haya empezado: así el gancho se lee sin sonido en el primer segundo. Dentro de ella
      sigue el karaoke (la palabra que suena en negrita). Al acabar la frase, karaoke normal.
      No es un título fijo: desaparece cuando termina la primera frase (2026-11-16, Nico,
      tras el análisis de Reels virales del nicho).
"""
import os
import unicodedata

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .core import W, rgb

AQUI = os.path.dirname(os.path.abspath(__file__))
F_BOLD = os.path.join(AQUI, "fuentes", "Poppins-Bold.ttf")
F_MED = os.path.join(AQUI, "fuentes", "Poppins-Medium.ttf")


def _norm(p):
    p = unicodedata.normalize("NFD", p.lower())
    p = "".join(c for c in p if unicodedata.category(c) != "Mn")
    return "".join(c for c in p if c.isalnum())


class SubtitulosKaraoke:
    def __init__(self, bloques, estilo):
        self.l = bloques
        self.e = estilo
        tam = estilo.get("tam", 60)
        self.fb = ImageFont.truetype(F_BOLD, tam)
        self.fm = ImageFont.truetype(F_MED, tam)
        self.y = estilo.get("y", 350)
        self.maxw = estilo.get("ancho_max", 860)
        self.claves = {_norm(c) for c in estilo.get("claves", [])}
        self.c_dicha = rgb(estilo.get("color_dicha", "#d9dbe6"), estilo.get("alfa_dicha", 150))
        self.c_actual = rgb(estilo.get("color_actual", "#ffffff"))
        self.c_caps = rgb(estilo.get("color_capsula", "#1d2c6ee0"))
        self.c_caps_borde = rgb(estilo.get("color_capsula_borde", "#8fa6ffb0"))
        self._lay = {}
        self._cache = {}
        self.l = [dict(b) for b in self.l]
        for b in self.l:
            if "palabras" not in b:   # SRT o lista sin tiempos por palabra: reparto por caracteres
                pal = b["texto"].split()
                tot = sum(len(p) + 1 for p in pal) or 1
                t, out = b["inicio"], []
                for p in pal:
                    d = (b["fin"] - b["inicio"]) * (len(p) + 1) / tot
                    out.append({"texto": p, "inicio": t, "fin": t + d})
                    t += d
                b["palabras"] = out
        g = estilo.get("gancho")
        self.gancho = (g if isinstance(g, dict) else {}) if g else None
        if self.gancho is not None and self.l:
            self._unir_gancho()
        if self.gancho is not None:
            self.c_futura = rgb(estilo.get("color_actual", "#ffffff"), self.gancho.get("alfa", 225))
            self.c_panel = rgb(self.gancho.get("color_panel", "#070b1e"), self.gancho.get("alfa_panel", 150))
            tg = int(self.gancho.get("tam", round(estilo.get("tam", 60) * 1.15)))
            self.fb_g = ImageFont.truetype(F_BOLD, tg)
            self.fm_g = ImageFont.truetype(F_MED, tg)

    def _fuentes(self, i):
        if self.l[i].get("gancho"):
            return self.fb_g, self.fm_g
        return self.fb, self.fm

    def _unir_gancho(self):
        """Junta en un solo bloque las palabras de la primera frase y lo hace empezar en 0."""
        maxp = int(self.gancho.get("max_palabras", 16))
        todas = [p for b in self.l for p in b["palabras"]]
        n = 0
        for p in todas:
            n += 1
            if p["texto"][-1] in ".?!…" or n >= maxp:
                break
        gan = [dict(p) for p in todas[:n]]
        resto, k = [], 0
        for b in self.l:
            pal = b["palabras"]
            quedan = pal[max(0, n - k):] if k < n else pal
            k += len(pal)
            if not quedan:
                continue
            nb = dict(b, palabras=quedan, texto=" ".join(p["texto"] for p in quedan))
            nb["inicio"] = min(b["inicio"], quedan[0]["inicio"]) if len(quedan) == len(pal) else quedan[0]["inicio"]
            resto.append(nb)
        fin = gan[-1]["fin"] + 0.15
        if resto:
            fin = max(gan[-1]["fin"], min(resto[0]["inicio"], fin))
        self.l = [{"texto": " ".join(p["texto"] for p in gan), "inicio": 0.0, "fin": fin,
                   "palabras": gan, "gancho": True}] + resto

    # reparto en líneas y posición x de cada palabra (con la fuente Bold, la más ancha)
    def _layout(self, i):
        if i in self._lay:
            return self._lay[i]
        pal = [p["texto"] for p in self.l[i]["palabras"]]
        fb, _ = self._fuentes(i)
        esp = fb.getlength(" ")
        lineas, cur, wcur = [], [], 0.0
        for j, p in enumerate(pal):
            w = fb.getlength(p)
            if cur and wcur + esp + w > self.maxw:
                lineas.append((cur, wcur))
                cur, wcur = [], 0.0
            cur.append((j, w))
            wcur = w if len(cur) == 1 else wcur + esp + w
        if cur:
            lineas.append((cur, wcur))
        asc, desc = fb.getmetrics()
        lh = int((asc + desc) * 1.12)
        pos = {}
        for k, (ws, ancho) in enumerate(lineas):
            x = (W - ancho) / 2
            for j, w in ws:
                pos[j] = (x, k * lh, w)
                x += w + esp
        self._lay[i] = (pos, lh, len(lineas))
        return self._lay[i]

    def _bloque_en(self, t):
        for i, b in enumerate(self.l):
            if b["inicio"] - 0.05 <= t < b["fin"]:
                return i
        return None

    def _sprite(self, i, actual):
        clave = (i, actual)
        if clave in self._cache:
            return self._cache[clave]
        pos, lh, nl = self._layout(i)
        pal = self.l[i]["palabras"]
        alto = lh * nl + 60
        img = Image.new("RGBA", (W, alto), (0, 0, 0, 0))
        caps = Image.new("RGBA", (W, alto), (0, 0, 0, 0))
        txt = Image.new("RGBA", (W, alto), (0, 0, 0, 0))
        dc, dt = ImageDraw.Draw(caps), ImageDraw.Draw(txt)
        fb, fm = self._fuentes(i)
        asc, desc = fb.getmetrics()
        es_gancho = bool(self.l[i].get("gancho"))
        if es_gancho and self.gancho.get("panel", True):
            xs = [pos[j][0] for j in pos] + [pos[j][0] + pos[j][2] for j in pos]
            dc.rounded_rectangle((min(xs) - 34, 30 - 18, max(xs) + 34, 30 + lh * nl + 6),
                                 radius=28, fill=self.c_panel)
        hasta = len(pal) if es_gancho else actual + 1
        for j in range(hasta):
            x, y, w = pos[j]
            y += 30
            p = pal[j]["texto"]
            es_clave = _norm(p) in self.claves
            if es_clave:
                pad_x, pad_y = 16, 6
                dc.rounded_rectangle((x - pad_x, y + 4 - pad_y, x + w + pad_x, y + asc + desc * 0.55 + pad_y),
                                     radius=14, fill=self.c_caps, outline=self.c_caps_borde, width=3)
            if j == actual or es_clave:
                dt.text((x, y), p, font=fb, fill=self.c_actual)
            elif es_gancho:
                dt.text((x + (w - fm.getlength(p)) / 2, y), p, font=fm, fill=self.c_futura)
            else:
                dt.text((x + (w - fm.getlength(p)) / 2, y), p, font=fm, fill=self.c_dicha)
        # sombra suave (sin contorno, como en los vídeos objetivo)
        sombra = Image.new("RGBA", (W, alto), (0, 0, 0, 0))
        a = txt.split()[3].point(lambda v: int(v * 0.75))
        negro = Image.new("RGBA", (W, alto), (5, 6, 18, 255))
        negro.putalpha(a)
        sombra.paste(negro, (0, 4))
        sombra = sombra.filter(ImageFilter.GaussianBlur(8))
        img.alpha_composite(sombra)
        img.alpha_composite(caps)
        img.alpha_composite(txt)
        self._cache[clave] = img
        return img

    def dibujar(self, lienzo, t):
        i = self._bloque_en(t)
        if i is None:
            return
        pal = self.l[i]["palabras"]
        actual = -1 if self.l[i].get("gancho") else 0
        for j, p in enumerate(pal):
            if p["inicio"] - 0.04 <= t:
                actual = j
        spr = self._sprite(i, actual)
        if actual < 0:   # gancho antes de que empiece la voz: frase entera, sin fundido
            _, lh, nl = self._layout(i)
            lienzo.alpha_composite(spr, (0, int(self.y - (lh * nl + 60) / 2)))
            return
        k = (t - (pal[actual]["inicio"] - 0.04)) / 0.09
        if k < 1 and actual > 0:
            prev = self._sprite(i, actual - 1)
            spr = Image.blend(prev, spr, max(0.0, k))
        elif k < 1 and not self.l[i].get("gancho"):
            r, g, b, a = spr.split()
            spr = Image.merge("RGBA", (r, g, b, a.point(lambda v: int(v * max(0.0, k)))))
        _, lh, nl = self._layout(i)
        lienzo.alpha_composite(spr, (0, int(self.y - (lh * nl + 60) / 2)))
