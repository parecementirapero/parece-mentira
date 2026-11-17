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


class SubtitulosPalabra:
    """Subtítulo «palabra»: 1–2 palabras a la vez, enormes y centradas (hipótesis H1 de motor/APRENDIZAJE.md: es lo
    que hacen 5 de 7 Shorts de referencia con millones de vistas). La palabra entra con un golpe de escala.

    estilo_subtitulos: modo "palabra", y (1180: tercio inferior, dentro de la zona segura), tam (104),
    claves (palabras en amarillo), color (#ffffff), color_clave (#ffd23f), max_letras (13: junta palabras cortas),
    gancho: true → la primera frase entera, en dos o tres líneas, desde el fotograma 0 (igual que en karaoke)."""

    def __init__(self, bloques, estilo):
        self.l = [dict(b) for b in bloques]   # bloques originales: los usa el render para escribir el .srt
        self.e = estilo
        self.tam = int(estilo.get("tam", 104))
        self.y = estilo.get("y", 1180)
        self.maxw = estilo.get("ancho_max", 900)
        self.claves = {_norm(c) for c in estilo.get("claves", [])}
        self.col = rgb(estilo.get("color", "#ffffff"))
        self.col_clave = rgb(estilo.get("color_clave", "#ffd23f"))
        maxl = int(estilo.get("max_letras", 13))
        pal = []
        for b in bloques:
            if "palabras" in b:
                pal += [dict(p) for p in b["palabras"]]
            else:
                ws = b["texto"].split(); tot = sum(len(p) + 1 for p in ws) or 1; t = b["inicio"]
                for p in ws:
                    d = (b["fin"] - b["inicio"]) * (len(p) + 1) / tot
                    pal.append({"texto": p, "inicio": t, "fin": t + d}); t += d
        f_med = ImageFont.truetype(F_BOLD, self.tam)
        self.g = []          # grupos: {"texto", "inicio", "fin", "clave", "gancho"}
        k = 0
        if estilo.get("gancho") and pal:
            n = 0
            for p in pal:
                n += 1
                if p["texto"][-1] in ".?!…" or n >= 16:
                    break
            self.g.append({"palabras": pal[:n], "texto": " ".join(p["texto"] for p in pal[:n]), "inicio": 0.0, "fin": pal[n - 1]["fin"] + 0.1, "gancho": True})
            k = n
        while k < len(pal):
            grupo = [pal[k]]; k += 1
            # junta la palabra siguiente si entre las dos son cortas y no hay pausa ni signo de puntuación en medio
            while (k < len(pal) and len(grupo) < 3 and grupo[-1]["texto"][-1] not in ".,;:?!…"
                   and sum(len(p["texto"]) for p in grupo) + 1 + len(pal[k]["texto"]) <= maxl
                   and f_med.getlength(" ".join(p["texto"] for p in grupo + [pal[k]]).upper()) <= self.maxw - 40
                   and pal[k]["inicio"] - grupo[-1]["fin"] < 0.25):
                grupo.append(pal[k]); k += 1
            self.g.append({"palabras": grupo, "texto": " ".join(p["texto"] for p in grupo), "inicio": grupo[0]["inicio"], "fin": grupo[-1]["fin"],
                           "clave": any(_norm(p["texto"]) in self.claves for p in grupo)})
        for a, b in zip(self.g, self.g[1:]):   # cada grupo se queda hasta que entra el siguiente (máx. 0,6 s de cola)
            a["fin"] = min(b["inicio"], a["fin"] + 0.6) if not a.get("gancho") else min(b["inicio"], a["fin"])
        self._cache = {}

    def _sprite(self, i):
        if i in self._cache:
            return self._cache[i]
        g = self.g[i]
        tam = int(self.tam * (0.74 if len(g["texto"]) > 28 else 0.92)) if g.get("gancho") else self.tam
        f = ImageFont.truetype(F_BOLD, tam)
        lineas, cur = [], ""
        for p in g["texto"].upper().split():
            if cur and f.getlength(cur + " " + p) > self.maxw:
                lineas.append(cur); cur = p
            else:
                cur = (cur + " " + p).strip()
        lineas.append(cur)
        while max(f.getlength(l) for l in lineas) > self.maxw and tam > 40:   # una palabra larguísima: se encoge
            tam = int(tam * 0.92); f = ImageFont.truetype(F_BOLD, tam)
        asc, desc = f.getmetrics(); lh = int((asc + desc) * 1.05); borde = max(5, tam // 13)
        alto = lh * len(lineas) + 80
        txt = Image.new("RGBA", (W, alto), (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
        claves_g = {_norm(p["texto"]) for p in g["palabras"] if _norm(p["texto"]) in self.claves}
        for n, l in enumerate(lineas):
            x = (W - f.getlength(l)) / 2
            for p in l.split():
                col = self.col_clave if (_norm(p) in claves_g or (g.get("clave") and len(g["palabras"]) == 1)) else self.col
                d.text((x, 40 + n * lh), p, font=f, fill=col, stroke_width=borde, stroke_fill=(8, 9, 20, 255))
                x += f.getlength(p + " ")
        sombra = Image.new("RGBA", (W, alto), (0, 0, 0, 0))
        negro = Image.new("RGBA", (W, alto), (0, 0, 0, 255)); negro.putalpha(txt.split()[3].point(lambda v: int(v * 0.6)))
        sombra.paste(negro, (0, 8)); sombra = sombra.filter(ImageFilter.GaussianBlur(10))
        sombra.alpha_composite(txt)
        self._cache[i] = sombra
        return sombra

    def cajas(self):
        """[(inicio, fin, y_arriba, y_abajo)] de cada grupo: para que el control de calidad vea choques con rótulos."""
        return [(g["inicio"], g["fin"], self.y - self._sprite(i).height / 2 + 30, self.y + self._sprite(i).height / 2 - 30) for i, g in enumerate(self.g)]

    def dibujar(self, lienzo, t):
        for i, g in enumerate(self.g):
            if g["inicio"] - 0.04 <= t < g["fin"]:
                break
        else:
            return
        spr = self._sprite(i)
        k = (t - (g["inicio"] - 0.04)) / 0.1
        if k < 1 and not g.get("gancho"):          # golpe de entrada: de 78 % a 104 % y asienta en 100 %
            e = 0.78 + 0.26 * k
            spr = spr.resize((max(2, int(spr.width * e)), max(2, int(spr.height * e))), Image.BILINEAR)
        elif k < 1.6 and not g.get("gancho"):
            e = 1.04 - 0.04 * (k - 1) / 0.6
            spr = spr.resize((int(spr.width * e), int(spr.height * e)), Image.BILINEAR)
        x, y = int((W - spr.width) / 2), int(self.y - spr.height / 2)
        if x < 0:
            spr = spr.crop((-x, 0, -x + W, spr.height)); x = 0
        lienzo.alpha_composite(spr, (x, max(0, y)))
