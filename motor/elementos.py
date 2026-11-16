"""Elementos dibujables. Cada tipo se registra en TIPOS con su nombre del JSON.

Propiedades comunes (todas animables con "keys"):
  x, y            centro en el lienzo 1080×1920
  escala, ex, ey  escala global y por eje (ey<1 = «tumbado» en perspectiva)
  rot             grados (sentido horario)
  op              opacidad 0..1
  z               profundidad para el paralaje de la cámara (0 = fondo quieto, 1 = primer plano)
Comportamientos continuos ("anim"):
  flotar: [amplitud_px, periodo_s]     girar: grados/s
  pulso:  [amplitud, periodo_s]        parpadeo: [min_op, periodo_s]
  deriva: [vx, vy] px/s                balanceo: [grados, periodo_s]
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from .core import (W, H, rgb, mezcla, interp, pegar, opacidad, transformar,
                   supermuestreo, ruido, lerp_arr, ease_onda)

TIPOS = {}


def tipo(nombre):
    def reg(cls):
        TIPOS[nombre] = cls
        cls.nombre = nombre
        return cls
    return reg


def crear(spec, base_dir="."):
    t = spec.get("tipo")
    if t not in TIPOS:
        raise ValueError(f"Tipo de elemento desconocido: {t!r}. Disponibles: {sorted(TIPOS)}")
    return TIPOS[t](spec, base_dir)


class Elemento:
    PROPS = {"x": W / 2, "y": H / 2, "escala": 1.0, "ex": 1.0, "ey": 1.0,
             "rot": 0.0, "op": 1.0, "z": 0.5}
    EXTRA = {}          # props propias animables del tipo
    dinamico = False    # True si el sprite cambia con t

    def __init__(self, spec, base_dir="."):
        self.s = spec
        self.base_dir = base_dir
        self.keys = sorted(spec.get("keys", []), key=lambda k: k["t"])
        self.anim = spec.get("anim", {})
        self._cache = None
        self._cache_key = None

    # estado en el instante t (relativo a la escena)
    def estado(self, t):
        st = {}
        for p, d in {**self.PROPS, **self.EXTRA}.items():
            st[p] = interp(self.keys, t, p, self.s.get(p, d))
        a = self.anim
        if "flotar" in a:
            amp, per = a["flotar"]
            st["y"] += amp * ease_onda(t, per, self.s.get("fase", 0))
        if "girar" in a:
            st["rot"] += a["girar"] * t
        if "balanceo" in a:
            g, per = a["balanceo"]
            st["rot"] += g * ease_onda(t, per, self.s.get("fase", 0))
        if "pulso" in a:
            amp, per = a["pulso"]
            st["escala"] *= 1 + amp * ease_onda(t, per, self.s.get("fase", 0))
        if "parpadeo" in a:
            mn, per = a["parpadeo"]
            u = 0.5 + 0.5 * ease_onda(t, per, self.s.get("fase", 0))
            st["op"] *= mn + (1 - mn) * u
        if "deriva" in a:
            vx, vy = a["deriva"]
            st["x"] += vx * t
            st["y"] += vy * t
        return st

    def sprite_estatico(self):
        raise NotImplementedError

    def sprite(self, t, st):
        if self._cache is None:
            self._cache = self.sprite_estatico()
        return self._cache

    def dibujar(self, lienzo, t, cam):
        st = self.estado(t)
        if st["op"] <= 0.003 or st["escala"] <= 0.003:
            return
        spr = self.sprite(t, st)
        if spr is None:
            return
        spr = transformar(spr, st["escala"], st["ex"], st["ey"], st["rot"])
        spr = opacidad(spr, max(0.0, min(1.0, st["op"])))
        dx, dy = cam
        pegar(lienzo, spr, st["x"] + dx * st["z"], st["y"] + dy * st["z"])


# ====================================================================== forma
def _gradiente_vertical(w, h, c1, c2):
    u = np.linspace(0, 1, h, dtype=np.float32)[:, None].repeat(w, 1)
    arr = lerp_arr(c1, c2, u)
    a = np.full((h, w, 1), 255, np.float32)
    return Image.fromarray(np.concatenate([arr, a], 2).astype(np.uint8), "RGBA")


def sombra_suave(spr, desplaz=(0, 18), radio=18, op=0.45, color="#000000"):
    pad = radio * 3
    w, h = spr.size
    out = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    a = spr.split()[3].point(lambda v: int(v * op))
    sh = Image.new("RGBA", spr.size, rgb(color))
    sh.putalpha(a)
    capa = Image.new("RGBA", out.size, (0, 0, 0, 0))
    capa.paste(sh, (pad + desplaz[0], pad + desplaz[1]))
    capa = capa.filter(ImageFilter.GaussianBlur(radio))
    out.alpha_composite(capa)
    out.alpha_composite(spr, (pad, pad))
    return out


@tipo("forma")
class Forma(Elemento):
    """forma: rect | redondeado | elipse | circulo | poligono
    ancho, alto (o radio), puntos [[x,y],..] relativos al centro (poligono),
    relleno: color o [color_arriba, color_abajo]; borde: color; grosor;
    esquinas (radio de redondeo); sombra: true|{desplaz, radio, op};
    brillo: true (reflejo superior suave); desenfoque: px (para sombras y luces difusas)."""

    def sprite_estatico(self):
        s = self.s
        f = s.get("forma", "redondeado")
        if f == "circulo":
            w = h = 2 * s.get("radio", 50)
        elif f == "poligono":
            pts = s["puntos"]
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            w = 2 * max(abs(v) for v in xs) + 4
            h = 2 * max(abs(v) for v in ys) + 4
        else:
            w, h = s.get("ancho", 100), s.get("alto", 100)
        g = s.get("grosor", 0)
        W2, H2 = int(w + 2 * g + 4), int(h + 2 * g + 4)

        def mascara(img, f2):
            d = ImageDraw.Draw(img)
            cx, cy = W2 * f2 / 2, H2 * f2 / 2
            bb = [cx - w * f2 / 2, cy - h * f2 / 2, cx + w * f2 / 2, cy + h * f2 / 2]
            if f in ("elipse", "circulo"):
                d.ellipse(bb, fill=255)
            elif f == "rect":
                d.rectangle(bb, fill=255)
            elif f == "poligono":
                d.polygon([(cx + px * f2, cy + py * f2) for px, py in s["puntos"]], fill=255)
            else:
                d.rounded_rectangle(bb, radius=s.get("esquinas", min(w, h) * 0.25) * f2, fill=255)

        def m_img(img, f2):
            tmp = Image.new("L", img.size, 0)
            mascara(tmp, f2)
            img.putalpha(tmp)

        relleno = s.get("relleno", "#ffffff")
        if isinstance(relleno, list) and len(relleno) == 2 and all(isinstance(c, str) for c in relleno):
            base = _gradiente_vertical(W2, H2, relleno[0], relleno[1])
        else:
            base = Image.new("RGBA", (W2, H2), rgb(relleno))
        alpha = supermuestreo(lambda im, f2: m_img(im, f2), W2, H2).split()[3]
        if "op_relleno" in s:
            alpha = alpha.point(lambda v: int(v * s["op_relleno"]))
        base.putalpha(alpha)
        if s.get("brillo"):
            hl = Image.new("RGBA", (W2, H2), (255, 255, 255, 0))
            ga = np.zeros((H2, W2), np.float32)
            ga[: H2 // 2] = np.linspace(0.35, 0, H2 // 2)[:, None]
            m = np.asarray(alpha, np.float32) / 255
            hl.putalpha(Image.fromarray((ga * m * 255).astype(np.uint8)))
            base.alpha_composite(hl)
        if g:
            def borde(img, f2):
                d = ImageDraw.Draw(img)
                cx, cy = W2 * f2 / 2, H2 * f2 / 2
                bb = [cx - w * f2 / 2, cy - h * f2 / 2, cx + w * f2 / 2, cy + h * f2 / 2]
                col = rgb(s.get("borde", "#ffffff"))
                if f in ("elipse", "circulo"):
                    d.ellipse(bb, outline=col, width=int(g * f2))
                elif f == "rect":
                    d.rectangle(bb, outline=col, width=int(g * f2))
                elif f == "poligono":
                    p = [(cx + px * f2, cy + py * f2) for px, py in s["puntos"]]
                    d.line(p + [p[0]], fill=col, width=int(g * f2), joint="curve")
                else:
                    d.rounded_rectangle(bb, radius=s.get("esquinas", min(w, h) * 0.25) * f2,
                                        outline=col, width=int(g * f2))
            base.alpha_composite(supermuestreo(borde, W2, H2))
        if s.get("desenfoque"):
            r = s["desenfoque"]
            big = Image.new("RGBA", (W2 + 6 * r, H2 + 6 * r), (0, 0, 0, 0))
            big.alpha_composite(base, (3 * r, 3 * r))
            base = big.filter(ImageFilter.GaussianBlur(r))
        sh = s.get("sombra")
        if sh:
            sh = sh if isinstance(sh, dict) else {}
            base = sombra_suave(base, tuple(sh.get("desplaz", (0, 16))), sh.get("radio", 16),
                                sh.get("op", 0.45))
        return base


# ====================================================================== brillo
@tipo("brillo")
class Brillo(Elemento):
    """Halo de luz radial: radio, color, intensidad (0..1), dureza (exponente)."""

    def sprite_estatico(self):
        r = int(self.s.get("radio", 200))
        y, x = np.mgrid[-r:r, -r:r].astype(np.float32)
        d = np.sqrt(x * x + y * y) / r
        a = np.clip(1 - d, 0, 1) ** self.s.get("dureza", 2.2) * self.s.get("intensidad", 0.8)
        c = rgb(self.s.get("color", "#fff2c0"))
        arr = np.zeros((2 * r, 2 * r, 4), np.uint8)
        arr[..., :3] = c[:3]
        arr[..., 3] = (a * 255).astype(np.uint8)
        return Image.fromarray(arr, "RGBA")


# ====================================================================== rayos
@tipo("rayos")
class Rayos(Elemento):
    """Rayos de luz desde el centro: n, longitud, apertura (grados por rayo), color.
    Úsalo con anim.girar lento (2–6 º/s) para que se muevan."""

    def sprite_estatico(self):
        L = int(self.s.get("longitud", 900))
        n = self.s.get("n", 12)
        ap = math.radians(self.s.get("apertura", 6))
        c = rgb(self.s.get("color", "#fff4cf"))

        def dib(img, f):
            d = ImageDraw.Draw(img)
            cx = cy = L * f
            for i in range(n):
                a0 = 2 * math.pi * i / n
                p = [(cx, cy),
                     (cx + math.cos(a0 - ap / 2) * L * f, cy + math.sin(a0 - ap / 2) * L * f),
                     (cx + math.cos(a0 + ap / 2) * L * f, cy + math.sin(a0 + ap / 2) * L * f)]
                d.polygon(p, fill=c[:3] + (255,))
        spr = supermuestreo(dib, 2 * L, 2 * L, 1)
        y, x = np.mgrid[-L:L, -L:L].astype(np.float32)
        fall = np.clip(1 - np.sqrt(x * x + y * y) / L, 0, 1) ** 1.5 * self.s.get("intensidad", 0.35)
        a = np.asarray(spr.split()[3], np.float32) * fall
        spr.putalpha(Image.fromarray(a.astype(np.uint8)))
        return spr.filter(ImageFilter.GaussianBlur(6))


# ====================================================================== esfera
@tipo("esfera")
class Esfera(Elemento):
    """Planeta/bola con volumen. radio, color, color2, textura:
    lisa | rocosa | crateres | bandas | tierra | sol ; giro (º/s de la textura),
    luz [lx, ly] (de dónde viene la luz, -1..1), halo (color atmósfera),
    cara: true (ojos y sonrisa que parpadean), semilla."""

    def __init__(self, spec, base_dir="."):
        super().__init__(spec, base_dir)
        self.dinamico = bool(spec.get("giro", 0)) or bool(spec.get("cara"))
        r = int(spec.get("radio", 120))
        self.r = r
        sem = spec.get("semilla", 3)
        base = 8 if spec.get("textura") == "tierra" else 4
        self.tex = ruido(512, 256, sem, 5, base)
        self.tex2 = ruido(512, 256, sem + 7, 4, base + 4)
        y, x = np.mgrid[-r:r, -r:r].astype(np.float32) + 0.5
        d2 = (x * x + y * y) / (r * r)
        self.mask = np.clip((r - np.sqrt(x * x + y * y)) + 0.5, 0, 1)
        nz = np.sqrt(np.clip(1 - d2, 0, 1))
        self.nx, self.ny, self.nz = x / r, y / r, nz
        self.lat = np.arcsin(np.clip(y / r, -1, 1))
        self.lon0 = np.arctan2(x / r, np.maximum(nz, 1e-3))
        lx, ly = spec.get("luz", [-0.55, -0.6])
        lz = math.sqrt(max(0.05, 1 - lx * lx - ly * ly))
        sh = np.clip(self.nx * lx + self.ny * ly + nz * lz, 0, 1)
        rim = np.clip(1 - nz, 0, 1) ** 3
        self.shade = 0.28 + 0.85 * sh
        self.rim = rim
        self._halo = None

    def _textura(self, fase):
        s = self.s
        tx = s.get("textura", "rocosa")
        lon = (self.lon0 + fase) % (2 * math.pi)
        u = ((lon / (2 * math.pi)) * 511).astype(np.int32)
        v = (((self.lat / math.pi) + 0.5) * 255).astype(np.int32).clip(0, 255)
        n = self.tex[v, u]
        n2 = self.tex2[v, u]
        c1, c2 = s.get("color", "#c9a27a"), s.get("color2", "#7a5a3c")
        if tx == "lisa":
            col = lerp_arr(c1, c1, n)
        elif tx == "bandas":
            b = 0.5 + 0.5 * np.sin(self.lat * 9 + n2 * 3)
            col = lerp_arr(c1, c2, b * 0.8 + n * 0.2)
        elif tx == "tierra":
            tierra = n > 0.55
            col = lerp_arr("#1f5fbf", "#2f86e8", n2)
            verde = lerp_arr("#3f9b4a", "#a88a4f", np.clip((n - 0.55) * 3, 0, 1))
            col = np.where(tierra[..., None], verde, col)
            nubes = np.clip((n2 - 0.62) * 4, 0, 1)
            col = col + (255 - col) * nubes[..., None] * 0.9
        elif tx == "crateres":
            base = lerp_arr(c1, c2, n * 0.6)
            cr = np.clip((n2 - 0.68) * 6, 0, 1)
            col = base * (1 - 0.35 * cr[..., None])
        elif tx == "sol":
            col = lerp_arr(c1, c2, n * 0.7 + n2 * 0.3)
        else:  # rocosa
            col = lerp_arr(c1, c2, n * 0.7 + n2 * 0.3)
        return col

    def _render(self, t):
        s = self.s
        fase = math.radians(s.get("giro", 0) * t)
        col = self._textura(fase)
        if s.get("textura") == "sol":
            col = col * (0.85 + 0.3 * self.nz[..., None])
        else:
            col = col * self.shade[..., None]
        halo = rgb(s.get("halo", "#9ad0ff"))
        if s.get("halo"):
            col = col + (np.array(halo[:3], np.float32) - col) * (self.rim[..., None] * 0.7)
        col = np.clip(col, 0, 255)
        r = self.r
        arr = np.zeros((2 * r, 2 * r, 4), np.uint8)
        arr[..., :3] = col.astype(np.uint8)
        arr[..., 3] = (self.mask * 255).astype(np.uint8)
        img = Image.fromarray(arr, "RGBA")
        if s.get("cara"):
            img = self._cara(img, t)
        if s.get("halo"):
            if self._halo is None:
                R = int(r * 1.35)
                yy, xx = np.mgrid[-R:R, -R:R].astype(np.float32)
                d = np.sqrt(xx * xx + yy * yy)
                a = np.clip(1 - (d - r) / (R - r), 0, 1) ** 2 * (d > r * 0.9) * 0.55
                h = np.zeros((2 * R, 2 * R, 4), np.uint8)
                h[..., :3] = halo[:3]
                h[..., 3] = (a * 255).astype(np.uint8)
                self._halo = Image.fromarray(h, "RGBA")
            out = self._halo.copy()
            off = (out.width - img.width) // 2
            out.alpha_composite(img, (off, off))
            img = out
        return img

    def _cara(self, img, t):
        r = self.r
        per = self.s.get("parpadeo_cada", 3.4)
        ph = (t + self.s.get("fase", 0)) % per
        abierto = 0.12 if ph < 0.12 else 1.0

        def dib(im, f):
            d = ImageDraw.Draw(im)
            ox, oy = img.width * f / 2, img.height * f / 2
            for sx in (-1, 1):
                ex, ey = ox + sx * r * 0.32 * f, oy - r * 0.08 * f
                rw, rh = r * 0.13 * f, r * 0.16 * f * abierto
                d.ellipse([ex - rw, ey - rh, ex + rw, ey + rh], fill=(255, 255, 255, 255))
                pr = r * 0.075 * f
                ph_ = min(pr, rh)
                d.ellipse([ex - pr + r * 0.02 * f, ey - ph_, ex + pr + r * 0.02 * f, ey + ph_],
                          fill=(25, 20, 40, 255))
            d.arc([ox - r * 0.25 * f, oy + r * 0.02 * f, ox + r * 0.25 * f, oy + r * 0.38 * f],
                  20, 160, fill=(40, 25, 50, 255), width=int(r * 0.06 * f))
            for sx in (-1, 1):
                cx = ox + sx * r * 0.5 * f
                cy = oy + r * 0.18 * f
                d.ellipse([cx - r * 0.1 * f, cy - r * 0.06 * f, cx + r * 0.1 * f, cy + r * 0.06 * f],
                          fill=(255, 120, 150, 90))
        img.alpha_composite(supermuestreo(dib, img.width, img.height))
        return img

    def sprite(self, t, st):
        if self.dinamico:
            return self._render(t)
        if self._cache is None:
            self._cache = self._render(0)
        return self._cache


# ====================================================================== partículas
@tipo("particulas")
class Particulas(Elemento):
    """Partículas en continuo: area [x0,y0,x1,y1], n, clase:
    polvo | estrellas | burbujas | lluvia | nieve | chispas ; color, tam [min,max],
    vel [vx,vy] px/s (con dispersión), semilla. Usa op/keys para que aparezcan."""
    dinamico = True

    def __init__(self, spec, base_dir="."):
        super().__init__(spec, base_dir)
        rng = np.random.default_rng(spec.get("semilla", 1))
        n = spec.get("n", 60)
        x0, y0, x1, y1 = spec.get("area", [0, 0, W, H])
        self.area = (x0, y0, x1, y1)
        self.p0 = np.stack([rng.uniform(x0, x1, n), rng.uniform(y0, y1, n)], 1)
        vx, vy = spec.get("vel", [0, -20])
        disp = spec.get("dispersion", 0.35)
        self.v = np.stack([vx * (1 + disp * rng.normal(size=n)), vy * (1 + disp * rng.normal(size=n))], 1)
        tmin, tmax = spec.get("tam", [3, 8])
        self.tam = rng.uniform(tmin, tmax, n)
        self.fase = rng.uniform(0, 6.28, n)
        self.clase = spec.get("clase", "polvo")
        self._spr = {}

    def _punto(self, tam):
        k = int(round(tam * 2)) / 2
        if k in self._spr:
            return self._spr[k]
        c = rgb(self.s.get("color", "#ffffff"))
        cl = self.clase
        if cl == "lluvia":
            w, h = max(2, int(k * 0.6)), int(k * 6)
            spr = supermuestreo(lambda im, f: ImageDraw.Draw(im).rounded_rectangle(
                [0, 0, w * f - 1, h * f - 1], radius=w * f / 2, fill=c), w, h)
        else:
            R = int(k * 3) + 2
            y, x = np.mgrid[-R:R, -R:R].astype(np.float32)
            d = np.sqrt(x * x + y * y)
            core = np.clip(k - d + 0.8, 0, 1)
            glow = np.clip(1 - d / R, 0, 1) ** 2 * (0.55 if cl in ("estrellas", "chispas") else 0.2)
            if cl == "burbujas":
                core = np.clip(1 - abs(d - k) / 1.6, 0, 1) * 0.9 + core * 0.15
            a = np.clip(core + glow, 0, 1) * c[3] / 255
            arr = np.zeros((2 * R, 2 * R, 4), np.uint8)
            arr[..., :3] = c[:3]
            arr[..., 3] = (a * 255).astype(np.uint8)
            spr = Image.fromarray(arr, "RGBA")
        self._spr[k] = spr
        return spr

    def dibujar(self, lienzo, t, cam):
        st = self.estado(t)
        if st["op"] <= 0.003:
            return
        x0, y0, x1, y1 = self.area
        p = self.p0 + self.v * t
        p[:, 0] = x0 + (p[:, 0] - x0) % (x1 - x0)
        p[:, 1] = y0 + (p[:, 1] - y0) % (y1 - y0)
        tw = self.clase in ("estrellas", "chispas")
        for i in range(len(p)):
            op = st["op"]
            if tw:
                op *= 0.45 + 0.55 * (0.5 + 0.5 * math.sin(t * 3 + self.fase[i]))
            spr = opacidad(self._punto(self.tam[i]), op)
            pegar(lienzo, spr, p[i, 0] + cam[0] * st["z"], p[i, 1] + cam[1] * st["z"])


# ====================================================================== suelo
@tipo("suelo")
class Suelo(Elemento):
    """Terreno desde y=borde hasta abajo (más 200 px de margen para el paralaje).
    material: arena | luna | hierba | tierra | roca ; colores [arriba, abajo];
    ondulacion (px del borde superior), crateres (n, solo luna), semilla.
    x/y del elemento se ignoran: se coloca con 'borde'."""

    def sprite_estatico(self):
        s = self.s
        b = int(s.get("borde", 1100))
        mat = s.get("material", "arena")
        pal = {"arena": ["#f3d9a4", "#d9b47a"], "luna": ["#b9b9c2", "#6e6e7c"],
               "hierba": ["#7cc46a", "#3f8a45"], "tierra": ["#a0754e", "#6b4a30"],
               "roca": ["#8a8d99", "#4d505c"]}[mat]
        c1, c2 = s.get("colores", pal)
        w, h = W + 400, H - b + 400
        u = np.linspace(0, 1, h, dtype=np.float32)[:, None].repeat(w, 1)
        col = lerp_arr(c1, c2, u)
        n = ruido(w, h, s.get("semilla", 5), 5, 6)
        fino = ruido(w, h, s.get("semilla", 5) + 11, 3, 60)
        col = col * (0.88 + 0.18 * n[..., None]) * (0.94 + 0.1 * fino[..., None])
        arr = np.zeros((h, w, 4), np.uint8)
        arr[..., :3] = np.clip(col, 0, 255).astype(np.uint8)
        arr[..., 3] = 255
        ond = s.get("ondulacion", 18)
        xs = np.arange(w)
        perfil = (ond * (np.sin(xs / 140 + 1.3) * 0.6 + np.sin(xs / 57) * 0.4) + ond).astype(int)
        for x in range(w):
            arr[: perfil[x], x, 3] = 0
        img = Image.fromarray(arr, "RGBA")
        if mat == "luna":
            rng = np.random.default_rng(s.get("semilla", 5))
            def dib(im, f):
                d = ImageDraw.Draw(im)
                for _ in range(s.get("crateres", 14)):
                    cx, cy = rng.uniform(0, w), rng.uniform(80, h)
                    rr = rng.uniform(18, 70) * (0.5 + cy / h)
                    ry = rr * 0.45
                    d.ellipse([(cx - rr) * f, (cy - ry) * f, (cx + rr) * f, (cy + ry) * f],
                              fill=(60, 60, 72, 110))
                    d.arc([(cx - rr) * f, (cy - ry) * f, (cx + rr) * f, (cy + ry) * f],
                          200, 340, fill=(235, 235, 245, 120), width=int(4 * f))
            img.alpha_composite(supermuestreo(dib, w, h, 1))
        return img

    def dibujar(self, lienzo, t, cam):
        st = self.estado(t)
        spr = self.sprite(t, st)
        spr = opacidad(spr, st["op"])
        b = self.s.get("borde", 1100)
        lienzo.alpha_composite(spr.crop((200 - int(cam[0] * st["z"]), 0,
                                         200 - int(cam[0] * st["z"]) + W, min(spr.height, H - b + 40))),
                               (0, max(0, int(b + cam[1] * st["z"]) - 0)))


# ====================================================================== agua / olas
@tipo("agua")
class Agua(Elemento):
    """Masa de agua vista desde arriba que entra desde 'lado' (arriba|abajo).
    nivel: posición y del borde (animable con keys), amplitud, colores [hondo, orilla], espuma."""
    dinamico = True
    EXTRA = {"nivel": 400.0}

    def dibujar(self, lienzo, t, cam):
        st = self.estado(t)
        s = self.s
        amp = s.get("amplitud", 22)
        nivel = st["nivel"] + cam[1] * st["z"]
        hondo, orilla = s.get("colores", ["#1d6fa8", "#5fd1e0"])
        arriba = s.get("lado", "arriba") == "arriba"
        xs = np.arange(0, W + 9, 8)
        borde = nivel + amp * (np.sin(xs / 90 + t * 2.1) * 0.6 + np.sin(xs / 37 - t * 3.3) * 0.4)
        top = 0 if arriba else int(max(0, borde.min() - 40))
        bot = int(min(H, borde.max() + 40)) if arriba else H
        if bot <= top:
            return
        hh = bot - top
        capa = Image.new("RGBA", (W, hh), (0, 0, 0, 0))
        u = np.linspace(0, 1, hh, dtype=np.float32)
        if not arriba:
            u = u[::-1]
        grad = lerp_arr(hondo, orilla, np.clip(u, 0, 1)[:, None].repeat(W, 1))
        mask = Image.new("L", (W * 2, hh * 2), 0)
        d = ImageDraw.Draw(mask)
        pts = [(x * 2, (y - top) * 2) for x, y in zip(xs, borde)]
        if arriba:
            d.polygon([(0, 0)] + pts + [(W * 2, 0)], fill=int(255 * s.get("opacidad", 0.92)))
        else:
            d.polygon([(0, hh * 2)] + pts + [(W * 2, hh * 2)], fill=int(255 * s.get("opacidad", 0.92)))
        mask = mask.resize((W, hh), Image.LANCZOS)
        g = np.concatenate([grad, np.asarray(mask, np.float32)[..., None]], 2)
        capa = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8), "RGBA")
        if s.get("espuma", True):
            esp = Image.new("RGBA", (W * 2, hh * 2), (0, 0, 0, 0))
            de = ImageDraw.Draw(esp)
            de.line(pts, fill=(255, 255, 255, 230), width=14, joint="curve")
            pts2 = [(x, y + (-1 if arriba else 1) * 26) for x, y in pts]
            de.line(pts2, fill=(255, 255, 255, 90), width=8, joint="curve")
            capa.alpha_composite(esp.resize((W, hh), Image.LANCZOS))
        lienzo.alpha_composite(opacidad(capa, st["op"]), (0, top))


# ====================================================================== huella
@tipo("huella")
class Huella(Elemento):
    """Huella vista desde arriba. clase: bota | pie ; largo (px), color (sombra de la huella),
    suela: true -> pinta la suela de la bota (para el pie que baja) con color_suela.
    marca 0..1 (aparece), borrado 0..1 (se deshace con ruido). lado: izq|der."""
    EXTRA = {"marca": 1.0, "borrado": 0.0}

    def __init__(self, spec, base_dir="."):
        super().__init__(spec, base_dir)
        self._base = None

    def _base_img(self):
        if self._base is not None:
            return self._base
        s = self.s
        L = s.get("largo", 260)
        Wd = L * 0.42
        bota = s.get("clase", "bota") == "bota"
        suela = s.get("suela", False)
        col = rgb(s.get("color", "#00000080"))
        cs = rgb(s.get("color_suela", "#e9e9ef"))
        espejo = -1 if s.get("lado", "der") == "izq" else 1

        def dib(im, f):
            d = ImageDraw.Draw(im)
            cx, cy = im.width / 2, im.height / 2
            def E(x, y, rx, ry, **k):
                d.ellipse([cx + (x - rx) * f, cy + (y - ry) * f, cx + (x + rx) * f, cy + (y + ry) * f], **k)
            fill = cs if suela else col
            if bota:
                d.rounded_rectangle([cx - Wd / 2 * f, cy - L / 2 * f, cx + Wd / 2 * f, cy + L * 0.08 * f],
                                    radius=Wd * 0.45 * f, fill=fill)
                d.rounded_rectangle([cx - Wd * 0.42 * f, cy + L * 0.12 * f, cx + Wd * 0.42 * f, cy + L / 2 * f],
                                    radius=Wd * 0.4 * f, fill=fill)
                ray = (255, 255, 255, 60) if not suela else (150, 150, 165, 255)
                for i in range(7):
                    y = -L * 0.44 + i * L * 0.075
                    d.line([cx - Wd * 0.38 * f, cy + y * f, cx + Wd * 0.38 * f, cy + y * f],
                           fill=ray, width=int(L * 0.022 * f))
                for i in range(3):
                    y = L * 0.2 + i * L * 0.09
                    d.line([cx - Wd * 0.32 * f, cy + y * f, cx + Wd * 0.32 * f, cy + y * f],
                           fill=ray, width=int(L * 0.022 * f))
            else:
                E(0, -L * 0.12, Wd * 0.48, L * 0.34, fill=fill)
                E(espejo * -Wd * 0.05, L * 0.3, Wd * 0.36, L * 0.2, fill=fill)
                dedos = [(-0.3, 0.06), (-0.1, 0.05), (0.08, 0.045), (0.24, 0.04), (0.36, 0.035)]
                for i, (dx, rr) in enumerate(dedos):
                    E(espejo * dx * Wd * 1.25, -L * 0.48 + abs(dx) * L * 0.18, rr * L * 0.55, rr * L * 0.6,
                      fill=fill)
        img = supermuestreo(dib, int(Wd + 40), int(L + 40))
        if not suela:
            img = img.filter(ImageFilter.GaussianBlur(1.2))
            rim = img.split()[3].filter(ImageFilter.GaussianBlur(5))
            luz = Image.new("RGBA", img.size, (255, 255, 255, 0))
            luz.putalpha(rim.point(lambda v: int(min(v, 255 - v) * 0.5)))
            out = Image.new("RGBA", (img.width, img.height), (0, 0, 0, 0))
            out.alpha_composite(luz, (0, -3))
            out.alpha_composite(img)
            img = out
        else:
            img = sombra_suave(img, (0, 10), 10, 0.35)
        self._base = img
        return img

    def sprite(self, t, st):
        img = self._base_img()
        m = max(0.0, min(1.0, st["marca"]))
        b = max(0.0, min(1.0, st["borrado"]))
        if m >= 0.999 and b <= 0.001:
            return img
        img = opacidad(img, m)
        if b > 0.001:
            n = ruido(img.width, img.height, self.s.get("semilla", 9), 4, 5)
            a = np.asarray(img.split()[3], np.float32)
            keep = np.clip((n - b) * 6, 0, 1) * (1 - b * 0.6)
            img = img.copy()
            img.putalpha(Image.fromarray((a * keep).astype(np.uint8)))
        return img


# ====================================================================== flecha
@tipo("flecha")
class Flecha(Elemento):
    """Trazo/flecha que se dibuja a lo largo de puntos (coordenadas del lienzo).
    puntos [[x,y],...] (curva suave que pasa por ellos), grosor, color, contorno,
    progreso 0..1 (animable), punta true|false, discontinua [trazo, hueco].
    La punta siempre apunta en la dirección final del trazo."""
    EXTRA = {"progreso": 1.0}

    def __init__(self, spec, base_dir="."):
        super().__init__(spec, base_dir)
        self.camino = self._muestrear(spec["puntos"])
        seg = np.diff(self.camino, axis=0)
        self.long = np.concatenate([[0], np.cumsum(np.hypot(seg[:, 0], seg[:, 1]))])

    @staticmethod
    def _muestrear(pts, n=24):
        pts = np.array(pts, np.float32)
        if len(pts) == 2:
            return np.linspace(pts[0], pts[1], n * 2)
        p = np.vstack([pts[0], pts, pts[-1]])
        out = []
        for i in range(1, len(p) - 2):
            p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
            for t in np.linspace(0, 1, n, endpoint=False):
                t2, t3 = t * t, t * t * t
                out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                                  + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
        out.append(pts[-1])
        return np.array(out, np.float32)

    def dibujar(self, lienzo, t, cam):
        st = self.estado(t)
        pr = max(0.0, min(1.0, st["progreso"]))
        if pr <= 0.001 or st["op"] <= 0.003:
            return
        s = self.s
        total = self.long[-1] * pr
        idx = int(np.searchsorted(self.long, total))
        pts = self.camino[:max(idx, 1)].tolist()
        if idx < len(self.camino):
            a, b = self.camino[max(idx - 1, 0)], self.camino[idx]
            la, lb = self.long[max(idx - 1, 0)], self.long[idx]
            u = 0 if lb == la else (total - la) / (lb - la)
            pts.append((a + (b - a) * u).tolist())
        if len(pts) < 2:
            return
        g = s.get("grosor", 14)
        dx, dy = cam[0] * st["z"], cam[1] * st["z"]
        P = np.array(pts) + [dx, dy]
        x0, y0 = P.min(0) - g * 4
        x1, y1 = P.max(0) + g * 4
        w, h = int(x1 - x0) + 1, int(y1 - y0) + 1
        col = rgb(s.get("color", "#ffffff"))
        cont = s.get("contorno")
        punta = s.get("punta", True)
        Q = P - [x0, y0]
        dirv = Q[-1] - Q[max(0, len(Q) - 4)]
        nrm = math.hypot(*dirv) or 1
        ux, uy = dirv / nrm
        tam = g * 2.6

        def dib(im, f):
            d = ImageDraw.Draw(im)
            q = [(x * f, y * f) for x, y in Q]
            fin = q
            if punta:
                fin = [(x, y) for x, y in q]
                fin[-1] = (fin[-1][0] - ux * tam * 0.6 * f, fin[-1][1] - uy * tam * 0.6 * f)
            capas = []
            if cont:
                capas.append((rgb(cont), g + 8))
            capas.append((col, g))
            for c, gg in capas:
                disc = s.get("discontinua")
                if disc:
                    acc, on = 0.0, True
                    for (ax, ay), (bx, by) in zip(fin, fin[1:]):
                        acc += math.hypot(bx - ax, by - ay) / f
                        if on:
                            d.line([(ax, ay), (bx, by)], fill=c, width=int(gg * f))
                        if acc > (disc[0] if on else disc[1]):
                            acc, on = 0.0, not on
                else:
                    d.line(fin, fill=c, width=int(gg * f), joint="curve")
                    r = gg * f / 2
                    for (px, py) in (fin[0], fin[-1]):
                        d.ellipse([px - r, py - r, px + r, py + r], fill=c)
                if punta:
                    ex, ey = q[-1]
                    k = tam * f + (gg - g) * f
                    px, py = -uy, ux
                    tri = [(ex + ux * k * 0.35, ey + uy * k * 0.35),
                           (ex - ux * k * 0.75 + px * k * 0.6, ey - uy * k * 0.75 + py * k * 0.6),
                           (ex - ux * k * 0.75 - px * k * 0.6, ey - uy * k * 0.75 - py * k * 0.6)]
                    d.polygon(tri, fill=c)
        spr = supermuestreo(dib, w, h)
        if s.get("sombra"):
            spr = sombra_suave(spr, (0, 8), 8, 0.35)
            x0 -= 24
            y0 -= 24
        spr = opacidad(spr, st["op"])
        pegar(lienzo, spr, x0 + spr.width / 2, y0 + spr.height / 2)


# ====================================================================== barra
@tipo("barra")
class Barra(Elemento):
    """Barra que se llena. ancho, alto, progreso 0..1, color, fondo, vertical (crece hacia arriba)."""
    EXTRA = {"progreso": 1.0}

    def sprite(self, t, st):
        s = self.s
        w, h = s.get("ancho", 600), s.get("alto", 48)
        pr = max(0.0, min(1.0, st["progreso"]))
        vert = s.get("vertical", False)

        def dib(im, f):
            d = ImageDraw.Draw(im)
            r = (min(w, h) / 2) * f
            d.rounded_rectangle([0, 0, w * f - 1, h * f - 1], radius=r, fill=rgb(s.get("fondo", "#00000066")))
            if pr > 0.01:
                if vert:
                    d.rounded_rectangle([0, h * f * (1 - pr), w * f - 1, h * f - 1], radius=r,
                                        fill=rgb(s.get("color", "#ffd34d")))
                else:
                    d.rounded_rectangle([0, 0, max(2 * r, w * f * pr), h * f - 1], radius=r,
                                        fill=rgb(s.get("color", "#ffd34d")))
        return sombra_suave(supermuestreo(dib, w, h), (0, 8), 10, 0.3)


# ====================================================================== persona
@tipo("persona")
class Persona(Elemento):
    """Personaje sencillo de frente. alto (px), piel, ropa, pelo, casco (astronauta),
    brazo_i / brazo_d (grados hacia fuera, animables: 0 = colgando, 90 = en cruz, 160 = arriba), parpadeo automático,
    paso (amplitud de balanceo al andar, animable)."""
    dinamico = True
    EXTRA = {"brazo_i": 12.0, "brazo_d": 12.0, "paso": 0.0}

    def sprite(self, t, st):
        s = self.s
        A = s.get("alto", 420)
        piel, ropa = rgb(s.get("piel", "#f2c3a0")), rgb(s.get("ropa", "#4f7cff"))
        pelo = rgb(s.get("pelo", "#2b1d16"))
        casco = s.get("casco", False)
        if casco:
            ropa = rgb(s.get("ropa", "#eef0f5"))
        w, h = int(A * 0.9), int(A * 1.1)
        per = s.get("parpadeo_cada", 3.1)
        ojo = 0.12 if ((t + s.get("fase", 0)) % per) < 0.12 else 1
        paso = st["paso"] * math.sin(t * 7)

        def dib(im, f):
            d = ImageDraw.Draw(im)
            cx = w / 2 * f
            def R(x0, y0, x1, y1, r, c):
                d.rounded_rectangle([cx + x0 * f, y0 * f, cx + x1 * f, y1 * f], radius=r * f, fill=c)
            sombra = tuple(int(v * 0.78) for v in ropa[:3]) + (255,)
            # piernas
            for sx, ph in ((-1, 1), (1, -1)):
                dy = max(0, paso * ph) * A * 0.04
                R(sx * A * 0.13 - A * 0.07, A * 0.66 - dy, sx * A * 0.13 + A * 0.07, A * 0.98 - dy, A * 0.05, sombra)
                R(sx * A * 0.13 - A * 0.09, A * 0.93 - dy, sx * A * 0.13 + A * 0.1, A * 1.0 - dy, A * 0.03,
                  (60, 60, 75, 255))
            # cuerpo
            R(-A * 0.25, A * 0.36, A * 0.25, A * 0.74, A * 0.12, ropa)
            if casco:
                R(-A * 0.13, A * 0.44, A * 0.13, A * 0.58, A * 0.03, (160, 170, 190, 255))
            # brazos
            for sx, ang in ((-1, st["brazo_i"]), (1, st["brazo_d"])):
                hx, hy = cx + sx * A * 0.23 * f, A * 0.42 * f
                a = math.radians(ang)
                L = A * 0.3 * f
                ex, ey = hx + sx * math.sin(a) * L, hy + math.cos(a) * L
                d.line([(hx, hy), (ex, ey)], fill=sombra, width=int(A * 0.1 * f))
                d.ellipse([ex - A * 0.055 * f, ey - A * 0.055 * f, ex + A * 0.055 * f, ey + A * 0.055 * f],
                          fill=ropa if casco else piel)
            # cabeza
            hy = A * 0.2
            r = A * 0.17
            if casco:
                d.ellipse([cx - r * 1.35 * f, (hy - r * 1.35) * f, cx + r * 1.35 * f, (hy + r * 1.35) * f],
                          fill=ropa)
                d.ellipse([cx - r * 1.0 * f, (hy - r * 0.8) * f, cx + r * 1.0 * f, (hy + r * 0.8) * f],
                          fill=(40, 70, 130, 255))
                d.ellipse([cx - r * 0.75 * f, (hy - r * 0.65) * f, cx - r * 0.2 * f, (hy - r * 0.25) * f],
                          fill=(190, 220, 255, 140))
            else:
                d.ellipse([cx - r * f, (hy - r) * f, cx + r * f, (hy + r) * f], fill=piel)
                d.chord([cx - r * 1.05 * f, (hy - r * 1.1) * f, cx + r * 1.05 * f, (hy + r * 0.5) * f],
                        180, 360, fill=pelo)
                for sx in (-1, 1):
                    ex, ey = cx + sx * r * 0.38 * f, (hy + r * 0.15) * f
                    rr = r * 0.11 * f
                    d.ellipse([ex - rr, ey - rr * ojo, ex + rr, ey + rr * ojo], fill=(30, 25, 40, 255))
                d.arc([cx - r * 0.35 * f, (hy + r * 0.2) * f, cx + r * 0.35 * f, (hy + r * 0.6) * f],
                      20, 160, fill=(120, 50, 50, 255), width=int(r * 0.08 * f))
        spr = supermuestreo(dib, w, h)
        return sombra_suave(spr, (0, 14), 14, 0.3)


# ====================================================================== imagen
_SVG = {}


def _ruta_raster(ruta, ancho):
    """PNG en caché de disco de un SVG a ese ancho (junto al SVG, en .raster/). Cambia si cambia el SVG."""
    import os
    st = os.stat(ruta)
    d = os.path.join(os.path.dirname(ruta), ".raster")
    return os.path.join(d, f"{os.path.splitext(os.path.basename(ruta))[0]}_{int(ancho)}_{st.st_size}_{int(st.st_mtime)}.png")


def rasterizar(ruta, ancho):
    """Rasteriza un SVG con rsvg-convert a la caché de disco (si no está ya) y devuelve la ruta del PNG.
    Los fondos con feTurbulence tardan 1–3 s cada uno: con la caché solo se pagan una vez, también entre
    ejecuciones de --hoja y entre los procesos del render en paralelo."""
    import os
    import subprocess
    png = _ruta_raster(ruta, ancho)
    if not os.path.exists(png):
        os.makedirs(os.path.dirname(png), exist_ok=True)
        tmp = f"{png}.{os.getpid()}.tmp"
        subprocess.check_call(["rsvg-convert", "-w", str(int(ancho)), ruta, "-o", tmp])
        os.replace(tmp, png)
    return png


def _svg(ruta, ancho, sombra=None):
    """SVG rasterizado a `ancho` px. Caché en memoria (por proceso) y en disco (.raster/)."""
    clave = (ruta, ancho, str(sombra))
    if clave not in _SVG:
        img = Image.open(rasterizar(ruta, ancho)).convert("RGBA")
        if sombra:
            img = sombra_suave(img, tuple(sombra.get("desplaz", (0, 20))), sombra.get("radio", 18),
                               sombra.get("op", 0.45))
        _SVG[clave] = img
    return _SVG[clave]


@tipo("imagen")
class Imagen(Elemento):
    """PNG externo (por ejemplo un sprite dibujado aparte). archivo (relativo al JSON), ancho."""

    def sprite_estatico(self):
        import os
        ruta = os.path.join(self.base_dir, self.s["archivo"])
        if ruta.lower().endswith(".svg"):
            return _svg(ruta, int(self.s.get("ancho", 600)), self.s.get("sombra"))
        img = Image.open(ruta).convert("RGBA")
        if "ancho" in self.s:
            k = self.s["ancho"] / img.width
            img = img.resize((int(img.width * k), int(img.height * k)), Image.LANCZOS)
        return img


# ====================================================================== rótulo
@tipo("rotulo")
class Rotulo(Elemento):
    """Rótulo de dato integrado en la escena (DECISIONS 2026-11-15): cifra grande + unidad pequeña.
    texto, unidad, tam (120), color, color_unidad, capsula (color de fondo o null), borde,
    contar: [desde, hasta, segundos] → la cifra corre desde `desde` hasta `hasta` (separador de miles «.»);
    decimales (coma decimal) y contar_prefijo opcionales.
    Animable: x, y, escala, op, rot."""
    dinamico = True

    def _fuentes(self):
        import os
        from PIL import ImageFont
        if not hasattr(self, "_fb"):
            aqui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fuentes")
            tam = self.s.get("tam", 120)
            self._fb = ImageFont.truetype(os.path.join(aqui, "Poppins-Bold.ttf"), tam)
            self._fu = ImageFont.truetype(os.path.join(aqui, "Poppins-Bold.ttf"), max(20, int(tam * 0.36)))
        return self._fb, self._fu

    def _texto(self, t):
        c = self.s.get("contar")
        if not c:
            return str(self.s.get("texto", ""))
        a, b, dur = c
        u = min(max(t - self.s.get("contar_desde", 0), 0) / max(dur, 1e-3), 1)
        u = 1 - (1 - u) ** 3
        dec = int(self.s.get("decimales", 0))
        v = a + (b - a) * u
        if dec:
            ent, fr = f"{v:,.{dec}f}".split(".")
            txt = ent.replace(",", ".") + "," + fr  # 3,8 · 23,5 (coma decimal)
        else:
            txt = f"{int(round(v)):,}".replace(",", ".") if self.s.get("miles", True) else str(int(round(v)))
        return self.s.get("contar_prefijo", "") + txt

    def sprite(self, t, st):
        txt = self._texto(t)
        clave = txt
        if clave == self._cache_key:
            return self._cache
        fb, fu = self._fuentes()
        uni = self.s.get("unidad", "")
        wt = fb.getlength(txt)
        wu = fu.getlength(uni) + (14 if uni else 0)
        asc, desc = fb.getmetrics()
        pad = int(self.s.get("tam", 120) * 0.28)
        w, h = int(wt + wu + 2 * pad), int(asc + desc * 0.4 + pad * 1.2)
        img = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        if self.s.get("capsula", "#0d1330d8"):
            d.rounded_rectangle((30, 30, 30 + w, 30 + h), radius=int(h * 0.28), fill=rgb(self.s.get("capsula", "#0d1330d8")),
                                outline=rgb(self.s.get("borde", "#ffffff40")), width=3)
        x0, y0 = 30 + pad, 30 + pad * 0.45
        d.text((x0, y0), txt, font=fb, fill=rgb(self.s.get("color", "#ffd34d")))
        if uni:
            ua, _ = fu.getmetrics()
            d.text((x0 + wt + 14, y0 + asc - ua - 2), uni, font=fu, fill=rgb(self.s.get("color_unidad", "#ffffff")))
        img = sombra_suave(img, (0, 12), 16, 0.5)
        self._cache, self._cache_key = img, clave
        return img


# ====================================================================== grupo
@tipo("grupo")
class Grupo(Elemento):
    """Agrupa elementos que se mueven juntos. ancho, alto del lienzo del grupo;
    'hijos': elementos con x,y relativos al centro del grupo."""
    dinamico = True

    def __init__(self, spec, base_dir="."):
        super().__init__(spec, base_dir)
        hijos = []
        for h in spec.get("hijos", []):
            h = dict(h)
            h.setdefault("x", 0)
            h.setdefault("y", 0)
            hijos.append(crear(h, base_dir))
        self.hijos = hijos

    def sprite(self, t, st):
        w, h = int(self.s.get("ancho", 600)), int(self.s.get("alto", 600))
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        for e in self.hijos:
            e2_st = e.estado(t)
            spr = e.sprite(t, e2_st) if not isinstance(e, (Particulas, Flecha, Agua, Suelo)) else None
            if spr is None:
                continue
            spr = transformar(spr, e2_st["escala"], e2_st["ex"], e2_st["ey"], e2_st["rot"])
            spr = opacidad(spr, max(0.0, min(1.0, e2_st["op"])))
            pegar(img, spr, w / 2 + e2_st["x"], h / 2 + e2_st["y"])
        return img
