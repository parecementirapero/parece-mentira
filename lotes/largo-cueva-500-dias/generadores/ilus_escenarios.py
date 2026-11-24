"""Fondos (escenarios) del vídeo largo «500 días en una cueva». Ver ARTE.md.

Uso:  python3 lotes/largo-cueva-500-dias/generadores/ilus_escenarios.py DIR_SVG
      from ilus_escenarios import generar; generar(DIR_SVG) → lista de nombres
Cada fondo sale en dos archivos recompuestos (no recortados): `nombre` (1080×1920) y `nombre_h` (1920×1080).
Todo con semillas fijas: sale igual cada vez.

Cómo está hecho (para quien lo amplíe):
- `Lienzo` lleva el tamaño, el prefijo de ids, los defs y el cuerpo. Cada escena es una función `escena(L)` que lee
  `L.v` (vertical) y coloca sus líneas clave (suelo, horizonte) según el formato.
- Ladrillos: `L.roca(...)` (masa de roca con estratos, vetas, manchas de humedad y brillos húmedos),
  `L.estalactita/estalagmita` (volumen con degradado lado luz/lado sombra, anillos y gota), `L.textura` (una pasada de
  ruido para toda la roca), `L.oscuridad` (viñeta que da la luz con intención), `L.brillo`, `L.bruma`, `L.polvo`.
- Rendimiento: cada `feTurbulence` a tamaño completo cuesta ~0,4 s en rsvg; cada escena usa como mucho 2-3.
"""
import math, os, random, re, sys

_AQUI = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_AQUI, "..", "..", ".."))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg, grano  # noqa: E402,F401

# Paleta de la cueva de Granada (ARTE.md)
ROCA = ["#1a120d", "#3d2a1f", "#6b4a32", "#8a6446"]
FRIO = ["#141b29", "#07090f"]
CALIDA = ["#ffcf8a", "#ffb15e"]
HIELO = ["#e8f6ff", "#a9d6f5", "#5f9fd1", "#22405e", "#0d1b2e"]


# ============================================================================ utilidades geométricas
def suave(pts, cerrado=True, t=0.5):
    """Curva Catmull-Rom → Bézier cúbica que pasa por todos los puntos."""
    n = len(pts)
    if n < 3:
        return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    out = [f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"]
    rng = range(n) if cerrado else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (cerrado or i > 0) else pts[0]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (cerrado or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        out.append(f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}")
    return " ".join(out) + (" Z" if cerrado else "")


def linea_ruido(r, x0, y0, x1, y1, n, amp, rugo=0.5):
    """Puntos de x0,y0 a x1,y1 con desplazamiento perpendicular multiescala (borde de roca orgánico)."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    fases = [r.uniform(0, 6.28) for _ in range(3)]
    pts = []
    for i in range(n + 1):
        t = i / n
        o = (math.sin(t * 6.28 * 1.3 + fases[0]) * amp * 0.6 + math.sin(t * 6.28 * 3.7 + fases[1]) * amp * 0.3
             + math.sin(t * 6.28 * 9.1 + fases[2]) * amp * 0.15 * rugo * 2 + r.uniform(-1, 1) * amp * 0.25 * rugo)
        if i in (0, n):
            o = 0
        pts.append((x0 + dx * t + nx * o, y0 + dy * t + ny * o))
    return pts


def mezcla(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(a[k] + (b[k] - a[k]) * t):02x}" for k in range(3))


# ============================================================================ lienzo
class Lienzo:
    def __init__(self, nombre, w, h, sem):
        self.nombre, self.w, self.h, self.v = nombre, w, h, h > w
        self.r = random.Random(sem)
        self.p = "es" + "".join(ch for ch in nombre if ch.isalnum())[-14:] + ("h" if w > h else "v") + "_"
        self.defs, self.b, self._n = [], [], 0

    # ids y defs ------------------------------------------------------------
    def id(self, s=""):
        self._n += 1
        return f"{self.p}{s}{self._n}"

    def lg(self, *stops, x1=0, y1=0, x2=0, y2=1, units=None, ops=None):
        i = self.id("g")
        u = f' gradientUnits="userSpaceOnUse"' if units else ""
        s = "".join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a is not None else "") + "/>"
                    for o, c, *rest in stops for a in [rest[0] if rest else None])
        self.defs.append(f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{u}>{s}</linearGradient>')
        return f"url(#{i})"

    def rgu(self, cx, cy, rx, ry, *stops, rot=0, fx=None, fy=None):
        """Degradado radial en coordenadas del lienzo (elipse rx×ry, girada rot)."""
        i = self.id("r")
        s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
        f = f' fx="{fx}" fy="{fy}"' if fx is not None else ""
        self.defs.append(f'<radialGradient id="{i}" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="1"{f} '
                         f'gradientTransform="translate({cx:.1f} {cy:.1f}) rotate({rot}) scale({rx:.1f} {ry:.1f})">{s}</radialGradient>')
        return f"url(#{i})"

    def clip(self, *paths):
        i = self.id("c")
        self.defs.append(f'<clipPath id="{i}">' + "".join(f'<path d="{p}"/>' for p in paths) + "</clipPath>")
        return f"url(#{i})"

    def ruido(self, color, sem, freq=0.012, contraste=2.4, corte=1.0, oct=4, tipo="fractalNoise"):
        i = self.id("n")
        rr, gg, bb = [int(color[k:k + 2], 16) / 255 for k in (1, 3, 5)]
        self.defs.append(f'<filter id="{i}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
                         f'<feTurbulence type="{tipo}" baseFrequency="{freq}" numOctaves="{oct}" seed="{sem}"/>'
                         f'<feColorMatrix type="matrix" values="0 0 0 0 {rr:.3f}  0 0 0 0 {gg:.3f}  0 0 0 0 {bb:.3f}  {contraste} 0 0 0 -{corte}"/></filter>')
        return f"url(#{i})"

    def add(self, *s):
        self.b.extend(s)

    def guardar(self, dirsvg, nombre):
        """Escribe el SVG. Grano propio (1 octava: mismo aspecto que `grano()`, la mitad de coste) y, en las formas sueltas,
        `opacity` → `fill-opacity/stroke-opacity` (rsvg no tiene que abrir una capa por cada forma: ~40 % más rápido)."""
        ilus.OUT = dirsvg
        gid = self.p + "grano"
        self.defs.append(f'<filter id="{gid}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
                         f'<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="1" seed="3"/>'
                         f'<feColorMatrix type="matrix" values="0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0.24 -0.02"/></filter>')
        cuerpo = "".join(self.b) + f'<rect width="{self.w}" height="{self.h}" filter="url(#{gid})"/>'

        def conv(m):
            t = m.group(0)
            if "filter=" in t or "opacity=" not in t or "mix-blend" in t:
                return t
            return re.sub(r'(?<![-\w])opacity="([0-9.]+)"', r'fill-opacity="\1" stroke-opacity="\1"', t)
        cuerpo = re.sub(r"<(path|ellipse|circle|rect|line|polygon)\b[^>]*/>", conv, cuerpo)
        guardar(nombre, cuerpo, self.w, self.h, "".join(self.defs))

    def relieve(self, sem, paths=None, freq="0.006 0.018", escala=9, az=90, elev=38, op=0.8, oct=5, modo="overlay", difusa=1.15,
                caja=None):
        """Relieve de roca de verdad: ruido → iluminación difusa (bump map) fundido en `overlay` sobre lo pintado.
        freq con dos valores (x y) anisótropos = estratos. az: de dónde viene la luz (90 = desde abajo, 270 = desde arriba)."""
        i = self.id("rel")
        self.defs.append(f'<filter id="{i}" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
                         f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="{oct}" seed="{sem}" result="t"/>'
                         f'<feDiffuseLighting in="t" surfaceScale="{escala}" diffuseConstant="{difusa}" lighting-color="#ffffff">'
                         f'<feDistantLight azimuth="{az}" elevation="{elev}"/></feDiffuseLighting></filter>')
        x, y, w, h = caja or (0, 0, self.w, self.h)
        r_ = f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" filter="url(#{i})" style="mix-blend-mode:{modo}" opacity="{op}"/>'
        if paths:
            return f'<g clip-path="{self.clip(*paths)}">{r_}</g>'
        return r_

    def luz(self, cx, cy, rx, ry, color, op=1.0, rot=0, modo="screen"):
        """Resplandor que suma luz (mezcla screen): ilumina sin lavar los negros."""
        g = self.rgu(cx, cy, rx, ry, (0, color, op), (0.4, color, op * 0.45), (1, color, 0), rot=rot)
        return f'<rect width="{self.w}" height="{self.h}" fill="{g}" style="mix-blend-mode:{modo}"/>'

    # ladrillos -------------------------------------------------------------
    def rect(self, fill, op=1, x=0, y=0, w=None, h=None, extra=""):
        w = self.w if w is None else w
        h = self.h if h is None else h
        return f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{fill}" opacity="{op}" {extra}/>'

    def brillo(self, cx, cy, rx, ry, color, op=1.0, rot=0, nucleo=0.0):
        g = self.rgu(cx, cy, rx, ry, (0, color, op), (max(0.01, nucleo), color, op), (0.45, color, op * 0.35),
                     (1, color, 0), rot=rot)
        return f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" transform="rotate({rot} {cx:.0f} {cy:.0f})" fill="{g}"/>'

    def oscuridad(self, cx, cy, rx, ry, color="#07090f", op=0.95, dentro=0.0, medio=0.55, rot=0):
        """Viñeta: transparente en (cx,cy) y opaca hacia fuera → la luz con intención."""
        g = self.rgu(cx, cy, rx, ry, (0, color, dentro), (0.35, color, dentro + (medio - dentro) * 0.4),
                     (0.7, color, medio), (1, color, op), rot=rot)
        return self.rect(g)

    def bruma(self, y, alto, color, op=0.5, x=0, w=None):
        g = self.lg((0, color, 0), (0.5, color, op), (1, color, 0))
        return self.rect(g, 1, x, y - alto / 2, w, alto)

    def polvo(self, n, x0, y0, x1, y1, color="#ffe6c0", rmax=2.6, opmax=0.7, sem=None):
        r = random.Random(sem) if sem is not None else self.r
        out = []
        for _ in range(n):
            x, y, rr = r.uniform(x0, x1), r.uniform(y0, y1), r.uniform(0.6, rmax)
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.1f}" fill="{color}" opacity="{r.uniform(0.15, opmax):.2f}"/>')
        return "".join(out)

    def textura(self, paths, sem, oscuro="#07090f", claro=None, freq=0.02, fuerza=1.0, oct=4):
        """Una pasada de ruido (moteado oscuro de la roca) sobre la unión de `paths`. `claro`: segunda pasada (cuesta ~0,4 s)."""
        c = self.clip(*paths)
        f1 = self.ruido(oscuro, sem, freq=freq, contraste=2.0, corte=0.78, oct=oct)
        s = f'<g clip-path="{c}"><rect width="{self.w}" height="{self.h}" filter="{f1}" opacity="{0.6 * fuerza:.2f}"/>'
        if claro:
            f2 = self.ruido(claro, sem + 11, freq=freq * 1.7, contraste=2.4, corte=1.45, oct=3)
            s += f'<rect width="{self.w}" height="{self.h}" filter="{f2}" opacity="{0.35 * fuerza:.2f}"/>'
        return s + "</g>"

    def roca(self, d, bbox, c_osc, c_med, c_luz, luz=(0.5, 0.0), sem=0, estratos=10, inclin=0.0, vetas=6,
             humedad=6, brillos=0, borde=None, borde_op=0.55, contraste=1.0, c_brillo="#fff4e0"):
        """Masa de roca con volumen. d: path; bbox=(x0,y0,x1,y1); luz=(fx,fy) dirección de la luz en la caja (0..1)."""
        r = random.Random(sem)
        x0, y0, x1, y1 = bbox
        bw, bh = x1 - x0, y1 - y0
        fx, fy = luz
        g = self.lg((0, c_luz), (0.45, c_med), (1, c_osc), x1=fx, y1=fy, x2=1 - fx, y2=1 - fy)
        c = self.clip(d)
        out = [f'<path d="{d}" fill="{g}"/>', f'<g clip-path="{c}">']
        # estratos: bandas onduladas alternas, más oscuras y más claras, y finas líneas de junta
        if estratos:
            paso = bh / estratos
            for k in range(estratos + 2):
                yb = y0 + k * paso + r.uniform(-paso * 0.3, paso * 0.3)
                amp, fr, ph = r.uniform(4, 14), r.uniform(0.004, 0.012), r.uniform(0, 6.28)
                pts = []
                for i in range(25):
                    xx = x0 - 20 + (bw + 40) * i / 24
                    pts.append((xx, yb + inclin * (xx - x0) + math.sin(xx * fr + ph) * amp + r.uniform(-2, 2)))
                gr = r.uniform(paso * 0.25, paso * 0.8)
                top = suave(pts, cerrado=False)
                bot = " ".join(f"L{px:.1f} {py + gr:.1f}" for px, py in reversed(pts))
                col = c_osc if k % 2 else c_luz
                out.append(f'<path d="{top} {bot} Z" fill="{col}" opacity="{r.uniform(0.05, 0.16) * contraste:.2f}"/>')
                out.append(f'<path d="{top}" stroke="{c_osc}" stroke-width="{r.uniform(1, 2.6):.1f}" '
                           f'opacity="{r.uniform(0.25, 0.5) * contraste:.2f}" fill="none"/>')
                out.append(f'<path d="{suave([(px, py + 2.5) for px, py in pts], cerrado=False)}" stroke="{c_luz}" '
                           f'stroke-width="1" opacity="{0.18 * contraste:.2f}" fill="none"/>')
        # manchas de humedad: chorreones verticales oscuros, todos en un grupo con un solo desenfoque
        if humedad:
            hm = []
            for _ in range(humedad):
                hx, hy = r.uniform(x0, x1), r.uniform(y0, y0 + bh * 0.7)
                hl, ha = r.uniform(bh * 0.12, bh * 0.45), r.uniform(10, 34)
                hm.append(f'<path d="M{hx - ha / 2:.0f} {hy:.0f} C{hx - ha / 2:.0f} {hy + hl * 0.6:.0f} {hx - ha * 0.15:.0f} {hy + hl:.0f} '
                          f'{hx:.0f} {hy + hl:.0f} C{hx + ha * 0.15:.0f} {hy + hl:.0f} {hx + ha / 2:.0f} {hy + hl * 0.6:.0f} {hx + ha / 2:.0f} {hy:.0f} Z" '
                          f'fill="#05070c" opacity="{r.uniform(0.25, 0.5):.2f}"/>')
                hm.append(f'<ellipse cx="{hx:.0f}" cy="{hy:.0f}" rx="{ha * 1.6:.0f}" ry="{ha * 0.8:.0f}" fill="#05070c" opacity="0.25"/>')
            out.append('<g filter="url(#blur8)">' + "".join(hm) + "</g>")
        # vetas: grietas finas oscuras con labio claro y alguna veta de cuarzo
        for _ in range(vetas):
            vx, vy = r.uniform(x0, x1), r.uniform(y0, y1)
            ang = r.uniform(-0.6, 0.6) + (math.pi / 2 if r.random() < 0.5 else 0)
            pts = [(vx, vy)]
            for _k in range(r.randint(4, 8)):
                ang += r.uniform(-0.5, 0.5)
                st = r.uniform(12, 40) * (bw / 600) ** 0.3
                pts.append((pts[-1][0] + math.cos(ang) * st, pts[-1][1] + math.sin(ang) * st))
            dd = "M" + " L".join(f"{px:.0f} {py:.0f}" for px, py in pts)
            if r.random() < 0.3:
                out.append(f'<path d="{dd}" stroke="#e8dccb" stroke-width="{r.uniform(1.5, 3):.1f}" opacity="0.35" fill="none" stroke-linejoin="round"/>')
            else:
                out.append(f'<path d="{dd}" stroke="#05070c" stroke-width="{r.uniform(1.2, 2.6):.1f}" opacity="0.6" fill="none" stroke-linejoin="round"/>'
                           f'<path d="{dd}" transform="translate(1.5 1.5)" stroke="{c_luz}" stroke-width="0.9" opacity="0.4" fill="none"/>')
        # brillos húmedos: chispitas y trazos cortos de agua que reflejan la luz
        for _ in range(brillos):
            bx = x0 + bw * min(1, max(0, r.gauss(fx, 0.25)))
            by = y0 + bh * min(1, max(0, r.gauss(fy, 0.3)))
            ln = r.uniform(3, 12)
            out.append(f'<path d="M{bx:.0f} {by:.0f} l{r.uniform(-1, 1):.1f} {ln:.1f}" stroke="{c_brillo}" stroke-width="{r.uniform(1, 2.4):.1f}" '
                       f'stroke-linecap="round" opacity="{r.uniform(0.4, 0.9):.2f}"/>')
            if r.random() < 0.3:
                out.append(f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{r.uniform(1.5, 3):.1f}" fill="#ffffff" opacity="0.9"/>')
        out.append("</g>")
        if borde:  # luz de borde por el lado iluminado (trazo grueso recortado por dentro)
            gb = self.lg((0, borde, borde_op), (0.35, borde, borde_op * 0.4), (0.7, borde, 0), x1=fx, y1=fy, x2=1 - fx, y2=1 - fy)
            out.append(f'<g clip-path="{c}"><path d="{d}" fill="none" stroke="{gb}" stroke-width="30" opacity="0.16"/>'
                       f'<path d="{d}" fill="none" stroke="{gb}" stroke-width="5" opacity="0.6"/></g>')
        return "".join(out)

    def _grad_cono(self, osc, med, luz, lado):
        """Degradado horizontal de un cono (estalactita): lado=+1 luz a la derecha, -1 a la izquierda."""
        if lado > 0:
            return self.lg((0, osc), (0.4, med), (0.8, luz), (0.93, mezcla(luz, "#ffffff", 0.12)), (1, med), x2=1, y2=0)
        return self.lg((0, med), (0.07, mezcla(luz, "#ffffff", 0.12)), (0.2, luz), (0.6, med), (1, osc), x2=1, y2=0)

    def estalactita(self, x, y, L, wb, grads, r=None, gota=True, c_osc="#000", anillos=True, c_brillo="#ffffff", gota_col="#dff4ff",
                    sombra_v=None):
        """Cono colgante con volumen. grads=(grad_luz_izq, grad_luz_der); el lado de luz lo elige el que llama."""
        r = r or self.r
        g = grads
        cv = r.uniform(-0.18, 0.18) * L
        tip = (x + cv, y + L)
        a, b_ = wb / 2, wb / 2
        d = (f"M{x - a:.1f} {y - 4:.1f} C{x - a * 0.9:.1f} {y + L * 0.35:.1f} {x - a * 0.25 + cv * 0.6:.1f} {y + L * 0.75:.1f} "
             f"{tip[0] - 1.2:.1f} {tip[1] - 2:.1f} Q{tip[0]:.1f} {tip[1] + 2:.1f} {tip[0] + 1.2:.1f} {tip[1] - 2:.1f} "
             f"C{x + b_ * 0.25 + cv * 0.6:.1f} {y + L * 0.75:.1f} {x + b_ * 0.9:.1f} {y + L * 0.35:.1f} {x + b_:.1f} {y - 4:.1f} Z")
        out = [f'<path d="{d}" fill="{g}"/>']
        if sombra_v:  # oscurece la raíz (pegada al techo) y deja la punta iluminada
            out.append(f'<path d="{d}" fill="{sombra_v}"/>')
        if anillos and L > 60:
            for k in range(1, int(L / 45)):
                t = k * 45 / L
                ww = wb * (1 - t) ** 1.2 * 0.5
                yy = y + L * t
                xx = x + cv * t * t
                out.append(f'<path d="M{xx - ww:.1f} {yy:.1f} Q{xx:.1f} {yy + ww * 0.25:.1f} {xx + ww:.1f} {yy:.1f}" stroke="{c_osc}" '
                           f'stroke-width="1.2" opacity="0.35" fill="none"/>')
        if gota and L > 40:
            out.append(f'<ellipse cx="{tip[0]:.1f}" cy="{tip[1] + 3:.1f}" rx="{max(1.5, wb * 0.035):.1f}" ry="{max(2.2, wb * 0.05):.1f}" fill="{gota_col}" opacity="0.85"/>'
                       f'<circle cx="{tip[0] - 0.6:.1f}" cy="{tip[1] + 2:.1f}" r="{max(0.7, wb * 0.012):.1f}" fill="{c_brillo}"/>')
        return "".join(out)

    def estalagmita(self, x, yb, L, wb, g, r=None, c_osc="#000", c_brillo="#ffffff", humedo=True, sombra_v=None):
        """Estalagmita orgánica: falda de colada ancha abajo, cuerpo con bultos, punta redondeada y húmeda."""
        r = r or self.r
        cv = r.uniform(-0.1, 0.1) * L
        n = 7
        izq, der = [], []
        for k in range(n + 1):
            t = k / n                      # 0 = base, 1 = punta
            ancho = wb / 2 * ((1 - t) ** 1.4 * 0.62 + 0.35 * (1 - t) ** 4 + 0.24) * (1 + r.uniform(-0.2, 0.2))
            yy = yb - L * t
            xx = x + cv * t * t
            izq.append((xx - ancho, yy))
            der.append((xx + ancho, yy))
        top = (x + cv, yb - L - wb * 0.1)
        pts = [(x - wb * 0.75, yb + 3)] + izq[:-1] + [top] + list(reversed(der[:-1])) + [(x + wb * 0.75, yb + 3)]
        d = suave(pts, cerrado=True, t=0.6)
        out = [f'<ellipse cx="{x:.1f}" cy="{yb + 2:.1f}" rx="{wb * 0.95:.1f}" ry="{wb * 0.13:.1f}" fill="#000" opacity="0.45"/>',
               f'<path d="{d}" fill="{g}"/>']
        if sombra_v:
            out.append(f'<path d="{d}" fill="{sombra_v}"/>')
        for k in range(1, max(2, int(L / 28))):
            t = k * 28 / L
            if t > 0.88:
                break
            ww = wb / 2 * ((1 - t) ** 0.75 * 0.85 + 0.06) * 0.9
            yy = yb - L * t + r.uniform(-3, 3)
            xx = x + cv * t * t
            out.append(f'<path d="M{xx - ww:.1f} {yy:.1f} Q{xx:.1f} {yy + ww * 0.35:.1f} {xx + ww:.1f} {yy:.1f}" stroke="{c_osc}" '
                       f'stroke-width="{r.uniform(0.8, 1.8):.1f}" opacity="{r.uniform(0.2, 0.4):.2f}" fill="none"/>')
        if humedo:
            out.append(f'<ellipse cx="{top[0] - wb * 0.02:.1f}" cy="{top[1] + wb * 0.1:.1f}" rx="{wb * 0.05:.1f}" ry="{wb * 0.025:.1f}" fill="{c_brillo}" opacity="0.75"/>')
        return "".join(out)

    def pedrusco(self, x, yb, ancho, alto, lado, cols, r=None, brillo=None, borde=None, sombra=True, facetas=True):
        """Bloque de roca facetado apoyado en yb. lado: +1 luz por la derecha, -1 por la izquierda, 0 desde arriba.
        cols=(oscuro, medio, claro)."""
        r = r or self.r
        c_osc, c_med, c_luz = cols
        n = 9
        pts = []
        for k in range(n + 1):
            a_ = math.pi + math.pi * k / n
            rr = 1 + r.uniform(-0.2, 0.1)
            pts.append((x + math.cos(a_) * ancho / 2 * rr, yb + math.sin(a_) * alto * rr if 0 < k < n else yb))
        pts += [(x + ancho * 0.42, yb + alto * 0.06), (x - ancho * 0.42, yb + alto * 0.06)]
        d = suave(pts, t=0.25)
        fx = 0.5 + 0.5 * lado
        g = self.lg((0, c_luz), (0.5, c_med), (1, c_osc), x1=fx, y1=0, x2=1 - fx, y2=1)
        out = []
        if sombra:
            out.append(f'<ellipse cx="{x - lado * ancho * 0.18:.1f}" cy="{yb + alto * 0.04:.1f}" rx="{ancho * 0.7:.1f}" ry="{max(2, alto * 0.12):.1f}" fill="#000" opacity="0.5"/>')
        out.append(f'<path d="{d}" fill="{g}"/>')
        if facetas and ancho > 14:
            # cara superior iluminada (faceta) y una arista de sombra
            top = [pts[k] for k in range(2, n - 1)]
            cx_, cy_ = x + lado * ancho * 0.08, yb - alto * 0.55
            fac = [top[0]] + top[1:-1] + [top[-1], (cx_ + lado * ancho * 0.1, cy_ + alto * 0.1), (cx_ - lado * ancho * 0.15, cy_)]
            out.append(f'<path d="{suave(fac, t=0.2)}" fill="{c_luz}" opacity="0.35"/>')
            kx = x - lado * ancho * r.uniform(0.05, 0.2)
            out.append(f'<path d="M{kx:.1f} {yb - alto * 0.8:.1f} L{kx - lado * ancho * 0.05:.1f} {yb - alto * 0.35:.1f} L{kx + lado * ancho * 0.02:.1f} {yb:.1f}" '
                       f'stroke="#000" stroke-width="{max(1, ancho * 0.012):.1f}" opacity="0.4" fill="none"/>')
        if borde:
            i0, i1 = (n // 2, n) if lado >= 0 else (0, n // 2 + 1)
            arco = pts[i0:i1 + 1]
            out.append(f'<path d="{suave(arco, cerrado=False, t=0.25)}" stroke="{borde}" stroke-width="{max(1.2, ancho * 0.012):.1f}" opacity="0.7" fill="none"/>')
        if brillo and ancho > 20:
            for _ in range(int(2 + ancho / 60)):
                bx = x + lado * r.uniform(0, ancho * 0.35)
                by = yb - alto * r.uniform(0.35, 0.85)
                out.append(f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{r.uniform(1.5, 4):.1f}" ry="{r.uniform(1, 2):.1f}" fill="{brillo}" opacity="{r.uniform(0.4, 0.9):.2f}"/>')
        return "".join(out)

    def colada(self, x, y0, y1, wb, g, r=None, c_osc="#000", c_luz="#fff", pliegues=6, abajo_libre=True, sombra_v=None):
        """Colada / cortina de roca: lámina que baja del techo con pliegues verticales y borde inferior ondulado."""
        r = r or self.r
        L = y1 - y0
        izq = linea_ruido(r, x - wb / 2, y0 - 10, x - wb * 0.42, y1, 6, wb * 0.06, 0.8)
        der = linea_ruido(r, x + wb * 0.42, y1, x + wb / 2, y0 - 10, 6, wb * 0.06, 0.8)
        fondo = []
        nf = pliegues * 2
        for k in range(1, nf):
            xx = x - wb * 0.42 + wb * 0.84 * k / nf
            fondo.append((xx, y1 + (r.uniform(10, 40) if k % 2 else r.uniform(-30, 0)) * (wb / 200)))
        pts = izq + fondo + der
        d = suave(pts, t=0.55)
        out = [f'<path d="{d}" fill="{g}"/>']
        cl = self.clip(d)
        out.append(f'<g clip-path="{cl}">')
        for k in range(1, nf, 2):
            xx = x - wb * 0.42 + wb * 0.84 * k / nf
            sw = wb / nf * 0.9
            out.append(f'<path d="M{xx:.1f} {y0:.1f} C{xx + r.uniform(-8, 8):.1f} {y0 + L * 0.4:.1f} {xx + r.uniform(-8, 8):.1f} {y0 + L * 0.7:.1f} {xx:.1f} {y1 + 40:.1f}" '
                       f'stroke="{c_osc}" stroke-width="{sw:.1f}" opacity="0.2" fill="none" filter="url(#blur8)"/>')
            xx2 = xx + wb / nf
            out.append(f'<path d="M{xx2:.1f} {y0 + L * 0.1:.1f} C{xx2 + r.uniform(-6, 6):.1f} {y0 + L * 0.45:.1f} {xx2 + r.uniform(-6, 6):.1f} {y0 + L * 0.75:.1f} {xx2:.1f} {y1 + 40:.1f}" '
                       f'stroke="{c_luz}" stroke-width="{max(1.5, sw * 0.16):.1f}" opacity="0.22" fill="none"/>')
        if sombra_v:
            out.append(f'<path d="{d}" fill="{sombra_v}"/>')
        out.append("</g>")
        for px, py in fondo[1::2]:  # gotas en los picos de la cortina
            out.append(f'<ellipse cx="{px:.1f}" cy="{py + 3:.1f}" rx="2" ry="3" fill="{c_luz}" opacity="0.7"/>')
        return "".join(out)


# ============================================================================ salas de cueva (Granada)
def _techo_estalactitas(L, y_techo_fn, x0, x1, n, Lmin, Lmax, wmin, wmax, grads, luz_x, sem, cosc="#07090f",
                        gota_col="#ffe9c8", brillo="#fff6e0", sombra_v=None):
    r = random.Random(sem)
    out = []
    xs = sorted(r.uniform(x0, x1) for _ in range(n))
    for x in xs:
        Lx = r.uniform(Lmin, Lmax) * (1.4 if r.random() < 0.15 else 1)
        wb = r.uniform(wmin, wmax) * (0.6 + Lx / Lmax * 0.5)
        g = grads[1] if x < luz_x else grads[0]
        out.append(L.estalactita(x, y_techo_fn(x), Lx, wb, g, r=r, c_osc=cosc, gota_col=gota_col, c_brillo=brillo, sombra_v=sombra_v))
        if r.random() < 0.45:  # racimo: hermanas pequeñas al lado
            for _ in range(r.randint(1, 3)):
                xx = x + r.uniform(-wb * 1.4, wb * 1.4)
                out.append(L.estalactita(xx, y_techo_fn(xx), Lx * r.uniform(0.25, 0.6), wb * r.uniform(0.3, 0.55),
                                         grads[1] if xx < luz_x else grads[0], r=r, c_osc=cosc, gota_col=gota_col, c_brillo=brillo,
                                         sombra_v=sombra_v))
    return "".join(out)


def _suelo_cueva(L, yf, yb, xl0, xr0, cols, luz, sem, despejado, n_piedras=40, charcos=3, brillo="#ffe6c0", c_luz=None):
    """Suelo de roca en perspectiva desde la línea yf (fondo) hasta yb (abajo). despejado=(x0,x1,y0,y1) sin piedras."""
    r = random.Random(sem)
    w, h = L.w, L.h
    c_lej, c_cer = cols
    out = []
    pts = linea_ruido(r, -40, yf, w + 40, yf, 18, 10, 0.6)
    d = suave(pts, cerrado=False) + f" L{w + 40} {yb + 40} L-40 {yb + 40} Z"
    g = L.lg((0, c_lej), (0.35, mezcla(c_lej, c_cer, 0.6)), (1, c_cer), y1=0, y2=1)
    out.append(f'<path d="{d}" fill="{g}"/>')
    cl = L.clip(d)
    out.append(f'<g clip-path="{cl}">')
    # roca del suelo en perspectiva (u = lado, z = profundidad 0 fondo → 1 espectador):
    # manchas de tono (placas) y grietas sinuosas que se ramifican, con labio iluminado
    vx = w / 2
    esc = lambda z: 0.3 + 0.7 * z
    P = lambda u, z: (vx + u * w * 0.5 * esc(z), yf + (yb - yf) * z)
    for _ in range(int(w / 9)):
        u, z = r.uniform(-2.4, 2.4), r.uniform(0, 1) ** 1.3
        ru, rz = r.uniform(0.06, 0.35), r.uniform(0.012, 0.06)
        X, Y = P(u, z)
        rx, ry = ru * w * 0.5 * esc(z), rz * (yb - yf) * (0.4 + z)
        pts = [(X + math.cos(a_) * rx * r.uniform(0.7, 1.15), Y + math.sin(a_) * ry * r.uniform(0.7, 1.15)) for a_ in [k * 0.9 for k in range(7)]]
        col = "#000" if r.random() < 0.55 else (c_luz or c_cer)
        out.append(f'<path d="{suave(pts)}" fill="{col}" opacity="{r.uniform(0.04, 0.13):.2f}"/>')
    for _ in range(int(w / 45)):
        u, z = r.uniform(-2.2, 2.2), r.uniform(0.02, 0.95)
        du = r.choice([-1, 1]) * r.uniform(0.04, 0.09)
        pts = [P(u, z)]
        for _k in range(r.randint(4, 12)):
            u += du * r.uniform(0.5, 1.3)
            z += r.uniform(-0.012, 0.02) * (1 + z)
            pts.append(P(u + r.uniform(-0.015, 0.015), min(1.05, z)))
        esp = 0.7 + z * 2.4
        dd = suave(pts, cerrado=False, t=0.4)
        out.append(f'<path d="{dd}" stroke="#050403" stroke-width="{esp:.1f}" opacity="0.55" fill="none" stroke-linecap="round"/>'
                   f'<path d="{dd}" transform="translate(0 {esp * 0.8:.1f})" stroke="{c_luz or c_cer}" stroke-width="{max(0.8, esp * 0.45):.1f}" opacity="0.3" fill="none"/>')
    # charcos: espejos que reflejan la luz (más claros por el lado de la luz), con borde mojado
    for _ in range(charcos):
        cx = r.choice([r.uniform(0, despejado[0]), r.uniform(despejado[1], w)])
        cy = r.uniform(yf + (yb - yf) * 0.12, yb - 40)
        t = (cy - yf) / (yb - yf)
        rx = r.uniform(50, 120) * (0.4 + t)
        ry = rx * (0.08 + t * 0.1)
        pc = [(cx + math.cos(a_) * rx * r.uniform(0.8, 1.1), cy + math.sin(a_) * ry * r.uniform(0.8, 1.1)) for a_ in [k * 0.785 for k in range(8)]]
        dc = suave(pc)
        gch = L.lg((0, "#05070c"), (0.55, mezcla(c_cer, "#000000", 0.55)), (1, brillo), x1=0, y1=0, x2=0, y2=1)
        out.append(f'<path d="{dc}" fill="{gch}" opacity="0.9"/>'
                   f'<ellipse cx="{cx + rx * 0.15:.0f}" cy="{cy + ry * 0.35:.0f}" rx="{rx * 0.5:.0f}" ry="{ry * 0.18:.0f}" fill="{brillo}" opacity="0.45"/>'
                   f'<path d="{dc}" fill="none" stroke="{brillo}" stroke-width="1.2" opacity="0.35"/>')
    # piedras sueltas (fuera de la zona despejada), más grandes cerca, cada una con su faceta iluminada
    dx0, dx1, dy0, dy1 = despejado
    piedras = []
    for _ in range(n_piedras):
        for _try in range(8):
            x, yy = r.uniform(-20, w + 20), r.uniform(yf + 8, yb)
            if not (dx0 < x < dx1 and dy0 < yy < dy1):
                break
        piedras.append((yy, x))
    for yy, x in sorted(piedras):
        t = (yy - yf) / (yb - yf)
        s_ = r.uniform(5, 14) * (0.5 + t * 3.2)
        lado = 1 if x < luz[0] else -1
        out.append(L.pedrusco(x, yy, s_ * 2.2, s_ * r.uniform(0.7, 1.2), lado,
                              (mezcla(c_cer, "#000000", 0.75), mezcla(c_cer, "#000000", 0.35), c_luz or brillo), r=r,
                              brillo=brillo if t > 0.3 else None))
    out.append("</g>")
    return "".join(out), d


def _ytec_fn(pts):
    def f(x):
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            if ax <= x <= bx:
                return ay + (by - ay) * (x - ax) / ((bx - ax) or 1) - 6
        return pts[0][1] if x < pts[0][0] else pts[-1][1]
    return f


def _sala(L, modo="calida", sem=11):
    """Sala de la cueva de Beatriz. modo: 'calida' (lámparas bajas fuera de cuadro) u 'oscura' (frontal frío).
    La geometría sale de `sem`: las dos versiones son la misma sala."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    oscura = modo == "oscura"
    yf = 1060 if V else 560           # pie de la pared del fondo (donde empieza el suelo)
    cx = w / 2
    ly = yf + (240 if V else 170)     # centro del charco de luz en el suelo = donde se posan los personajes
    ytec = 210 if V else 95
    if oscura:
        cR = ("#0b0c10", "#1a1b22", "#2c3040", "#3e4860")
        borde, brillo_c = "#7a9ad0", "#cfe2ff"
    else:
        cR = (ROCA[0], ROCA[1], ROCA[2], ROCA[3])
        borde, brillo_c = CALIDA[0], "#fff1d8"
    sv = L.lg((0, "#050506", 0.95), (0.55, "#050506", 0.45), (1, "#050506", 0))
    L.add(L.rect("#07080c"))
    # 1. pared del fondo: llena todo hasta el suelo, iluminada desde abajo en el centro
    dfar = f"M-40 -40 L{w + 40} -40 L{w + 40} {yf + 30} L-40 {yf + 30} Z"
    L.add(L.roca(dfar, (-40, -40, w + 40, yf + 30), "#0d0b0c", mezcla(cR[1], "#000000", 0.2), cR[2],
                 luz=(0.5, 1), sem=sem + 1, estratos=8, inclin=0.025, vetas=14, humedad=10, brillos=24, contraste=0.7,
                 c_brillo=brillo_c))
    # hueco al fondo: la galería sigue y se pierde en la oscuridad
    hx = w * (0.70 if V else 0.73)
    hw, hh = (300, 190) if V else (320, 150)
    hp = linea_ruido(r, hx - hw / 2, yf + 25, hx - hw * 0.25, yf - hh * 0.9, 5, 22, 1.0)[:-1]
    hp += linea_ruido(r, hx - hw * 0.25, yf - hh * 0.9, hx + hw * 0.3, yf - hh, 6, 16, 1.0)[:-1]
    hp += linea_ruido(r, hx + hw * 0.3, yf - hh, hx + hw / 2, yf + 25, 5, 22, 1.0)
    dh = suave(hp, t=0.35)
    if False:  # (el hueco se leía como una roca negra: se deja la oscuridad a la viñeta)
      L.add(f'<path d="{dh}" fill="{L.rgu(hx, yf, hw * 0.55, hh * 1.1, (0, "#000000", 1), (0.6, "#040304", 1), (1, mezcla(cR[1], "#000000", 0.5), 1))}"/>',
            f'<path d="{suave([(px + 6, py + 4) for px, py in hp[: len(hp) // 2]], cerrado=False, t=0.35)}" fill="none" stroke="{cR[3]}" stroke-width="3" opacity="0.35"/>',
            L.brillo(hx + hw * 0.1, yf - 20, hw * 0.45, hh * 0.3, "#5a4a52" if not oscura else "#30405a", 0.3))
    # 2. coladas (cortinas de roca) y columnas en la pared del fondo
    gl = (L._grad_cono("#0b0909", cR[1], cR[3], -1), L._grad_cono("#0b0909", cR[1], cR[3], 1))
    nc = 4 if V else 6
    for k in range(nc):
        bx = (k + 0.5) / nc * w + r.uniform(-50, 50)
        if abs(bx - hx) < hw * 0.75:
            continue
        y0c = r.uniform(-20, ytec + 80)
        y1c = yf - r.uniform(150, 420 if V else 230)
        wbc = r.uniform(120, 220)
        L.add(L.colada(bx, y0c, y1c, wbc, gl[1] if bx < cx else gl[0], r=r, c_osc="#050405", c_luz=cR[3], pliegues=r.randint(4, 7)))
        if r.random() < 0.6:  # estalagmita debajo que va a su encuentro
            L.add(L.estalagmita(bx + r.uniform(-20, 20), yf + r.uniform(4, 14), r.uniform(60, (yf - y1c) * 0.6), wbc * 0.5,
                                gl[1] if bx < cx else gl[0], r=r, c_brillo=brillo_c, c_osc="#050405"))
    for k in range(int(w / 170)):
        x = r.uniform(30, w - 30)
        if abs(x - cx) < w * 0.15 or abs(x - hx) < hw * 0.6:
            continue
        L.add(L.estalagmita(x, yf + r.uniform(0, 14), r.uniform(40, 140), r.uniform(26, 60), gl[1] if x < cx else gl[0], r=r,
                            c_brillo=brillo_c, c_osc="#050405"))
    L.add(L.bruma(yf - 10, 240 if V else 150, "#4a5a78" if oscura else "#7a5844", 0.22))
    # 3. paredes laterales (se pierden hacia arriba en la oscuridad)
    wl = [(-80, -40)] + linea_ruido(r, w * (0.30 if V else 0.20), -10, w * (0.17 if V else 0.10), yf + 60, 9, 45, 0.8)[1:-1]
    wl += [(w * (0.10 if V else 0.06), yf + 110), (-80, yf + 180)]
    wr = [(w + 80, -40)] + linea_ruido(r, w * (0.72 if V else 0.80), -10, w * (0.84 if V else 0.90), yf + 60, 9, 45, 0.8)[1:-1]
    wr += [(w * (0.90 if V else 0.94), yf + 110), (w + 80, yf + 180)]
    dl, dr = suave(wl), suave(wr)
    L.add(L.roca(dl, (-80, -40, w * 0.32, yf + 180), cR[0], cR[1], cR[3], luz=(1, 1), sem=sem + 3, estratos=8, inclin=0.08,
                 vetas=12, humedad=8, brillos=34, borde=borde, borde_op=0.55, c_brillo=brillo_c))
    L.add(L.roca(dr, (w * 0.68, -40, w + 80, yf + 180), cR[0], cR[1], cR[3], luz=(0, 1), sem=sem + 4, estratos=8, inclin=-0.07,
                 vetas=12, humedad=8, brillos=34, borde=borde, borde_op=0.55, c_brillo=brillo_c))
    # 4. techo con estalactitas grandes (raíz en sombra, punta que recoge la luz)
    pts_tec = linea_ruido(random.Random(sem + 5), -60, ytec, w + 60, ytec + 30, 14, 45, 0.9)
    dtec = suave([(-60, -60), (w + 60, -60)] + list(reversed(pts_tec)))
    L.add(L.roca(dtec, (-60, -60, w + 60, ytec + 80), "#050506", cR[0], cR[1], luz=(0.5, 1), sem=sem + 5, estratos=3,
                 vetas=5, humedad=3, brillos=10, c_brillo=brillo_c))
    gm = (L._grad_cono("#08070a", cR[1], cR[3], -1), L._grad_cono("#08070a", cR[1], cR[3], 1))
    L.add(_techo_estalactitas(L, _ytec_fn(pts_tec), -20, w + 20, int(w / 60), 90, 300 if V else 190, 24, 56, gm, cx, sem + 6,
                              sombra_v=sv, brillo=brillo_c, gota_col="#ffe9c8" if not oscura else "#cfe2ff"))
    # 5. suelo llano (zona central despejada para colchón, libros, lámparas…)
    desp = (w * 0.2, w * 0.8, yf + 20, h)
    suelo, dsuelo = _suelo_cueva(L, yf, h, 0, w, (mezcla(cR[1], "#000000", 0.3), mezcla(cR[2], "#000000", 0.2)), (cx, ly), sem + 7, desp,
                                 n_piedras=int(w / 20), charcos=3, brillo=borde, c_luz=cR[3])
    L.add(suelo)
    for k in range(int(w / 260)):
        x = r.choice([r.uniform(0, w * 0.15), r.uniform(w * 0.85, w)])
        L.add(L.estalagmita(x, yf + r.uniform(40, 200 if V else 100), r.uniform(90, 280 if V else 180), r.uniform(50, 100),
                            gm[1] if x < cx else gm[0], r=r, c_brillo=brillo_c, c_osc="#050405"))
    # 6. primer término: bloques casi negros y nítidos en las esquinas, con luz de borde
    rf = random.Random(sem + 9)
    for lado, x0 in ((1, -w * 0.02), (-1, w * 1.02)):
        for k in range(3):
            an = (w * (0.44 if V else 0.22)) * rf.uniform(0.8, 1.1) * (1 - k * 0.25)
            al = an * rf.uniform(0.55, 0.8) * (1.2 if V else 1.0)
            xx = x0 + lado * (k * an * 0.45 + rf.uniform(-20, 20))
            yy = h + rf.uniform(10, 60) - k * (90 if V else 40)
            L.add(L.pedrusco(xx, yy, an, al, lado, ("#020203", "#0a0809", "#2a1d16" if not oscura else "#1a2030"), r=rf,
                             borde=CALIDA[1] if not oscura else borde))
    # 7. luz (sumada), relieve de la roca (lejos fino y suave; paredes cerca más marcado; suelo aplastado) y viñeta
    az = 90 if not oscura else 270
    rel = [L.relieve(sem + 8, freq="0.009 0.022", escala=5, az=az, elev=45, op=0.35, oct=4, caja=(0, 0, w, yf + 20)),
           L.relieve(sem + 9, paths=[dl], freq="0.006 0.014", escala=8, az=0, elev=35, op=0.5, oct=4, caja=(0, 0, w * 0.34, yf + 190)),
           L.relieve(sem + 10, paths=[dr], freq="0.006 0.014", escala=8, az=180, elev=35, op=0.5, oct=4, caja=(w * 0.66, 0, w * 0.34, yf + 190)),
           L.relieve(sem + 11, freq="0.014 0.035", escala=4, az=270, elev=50, op=0.3, oct=3, caja=(0, yf, w, h - yf))]
    if not oscura:
        L.add(L.luz(cx, ly, w * 0.5, (h - yf) * 0.42, "#d07a30", 0.62))
        L.add(L.luz(cx, yf - 60, w * 0.5, 460 if V else 280, "#a8642e", 0.3))
        L.add(L.luz(-60, h * 0.98, w * 0.45, h * 0.35, "#d07a30", 0.45))      # lámparas fuera de cuadro
        L.add(L.luz(w + 60, h, w * 0.45, h * 0.35, "#d07a30", 0.40))
        L.add(*rel)
        L.add(L.oscuridad(cx, ly - (100 if V else 50), w * (0.72 if V else 0.55), h * (0.46 if V else 0.72), op=0.95, medio=0.5))
        L.add(L.luz(cx, ly + 20, w * 0.28, (h - yf) * 0.16, "#ffcf8a", 0.22))
        L.add(L.polvo(80 if V else 100, w * 0.22, yf - 450, w * 0.78, yf + 250, "#ffe2b0", 2.2, 0.55, sem=sem + 20))
    else:
        L.add(*rel)
        L.add(L.rect("#04060c", 0.45))
        L.add(L.oscuridad(cx, ly, w * (0.40 if V else 0.26), h * (0.26 if V else 0.42), color="#020308", op=0.97, medio=0.82))
        L.add(L.luz(cx, ly + (30 if V else 15), w * (0.30 if V else 0.19), (h - yf) * 0.2, "#5d86c8", 0.55))
        L.add(L.luz(cx, ly - (220 if V else 130), w * 0.22, 420 if V else 250, "#3a5a90", 0.18))
        L.add(L.polvo(30, cx - 200, ly - 400, cx + 200, ly + 60, "#cfe2ff", 1.8, 0.4, sem=sem + 20))
    return yf, ly


def bg_cueva_campamento(L):
    yf, ly = _sala(L, "calida")
    return {"suelo": ly, "nota": "suelo llano despejado en el centro"}


def bg_cueva_campamento_oscura(L):
    yf, ly = _sala(L, "oscura")
    return {"suelo": ly, "nota": "círculo de luz fría en el centro del suelo"}


def _aro(L, s, cx, yv, W0, Hc, Hf, r, amp=0.06, cerrado_suelo=True):
    """Contorno del hueco de un 'aro' de galería a escala s (perspectiva): pared izq → bóveda → pared dcha,
    y la cuña del suelo hasta abajo del lienzo. Devuelve (puntos_arco, path_hueco)."""
    w, h = L.w, L.h
    xl, xr, yfl = cx - W0 * s, cx + W0 * s, yv + Hf * s
    a = W0 * s * amp
    izq = linea_ruido(r, xl, yfl, xl - W0 * s * 0.04, yv - Hc * s * 0.25, 5, a, 0.9)
    arco = []
    for k in range(1, 12):
        th = math.pi * k / 12
        arco.append((cx - math.cos(th) * W0 * s * (1.0 + r.uniform(-0.05, 0.05)),
                     yv - Hc * s * 0.25 - math.sin(th) * Hc * s * 0.75 * (1 + r.uniform(-0.08, 0.06))))
    der = linea_ruido(r, xr + W0 * s * 0.04, yv - Hc * s * 0.25, xr, yfl, 5, a, 0.9)
    pts = izq + arco + der
    # cuña del suelo: las rectas desde el punto de fuga por los pies de las paredes, hasta abajo
    k_ = (h + 200 - yv) / (Hf * s)
    cuna = [(cx + (xr - cx) * k_, h + 200), (cx + (xl - cx) * k_, h + 200)]
    return pts, suave(pts, cerrado=False, t=0.45) + " " + " ".join(f"L{x:.1f} {y:.1f}" for x, y in cuna) + " Z"


def bg_cueva_galeria(L, sem=31):
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    cx = w / 2
    yv = 860 if V else 420
    W0 = w * (0.44 if V else 0.34)
    Hc = 1000 if V else 560
    Hf = (h - yv) / 0.85
    escalas = [0.035, 0.06, 0.09, 0.13, 0.18, 0.25, 0.34, 0.46, 0.62, 0.85]
    L.add(L.rect("#06070a"))
    # fondo del todo: negro con un leve resplandor frío (la galería sigue)
    L.add(L.brillo(cx, yv - 10, W0 * 0.12, Hc * 0.08, "#3a4a66", 0.6))
    # suelo (cuña) con piedras, escalones y charcos, de lejos a cerca
    dsuelo = f"M{cx:.0f} {yv:.0f} L{cx + W0 / 0.85 * 1.2 * (h + 200 - yv) / (Hf):.0f} {h + 200} L{cx - W0 / 0.85 * 1.2 * (h + 200 - yv) / Hf:.0f} {h + 200} Z"
    dsuelo = f"M{cx - 2:.0f} {yv:.0f} L{cx + 2:.0f} {yv:.0f} L{w + 2000} {h + 400} L{-2000} {h + 400} Z"
    L.add(f'<path d="{dsuelo}" fill="{L.lg((0, "#0c0b0d"), (0.25, "#2a2019"), (0.6, ROCA[2]), (1, ROCA[1]), y1=yv / h, y2=1, x1=0, x2=0)}"/>')
    gr = random.Random(sem + 1)
    for k in range(60 if V else 70):  # escalones/estratos del suelo: crestas transversales con labio claro
        t = gr.uniform(0.04, 1.0) ** 1.6 * 0.85 + 0.02
        y = yv + Hf * t
        half = W0 * t
        x0, x1 = cx + gr.uniform(-1, 0.2) * half, cx + gr.uniform(-0.2, 1) * half
        pts = linea_ruido(gr, x0, y, x1, y + gr.uniform(-6, 6) * t, 6, 3 + 14 * t, 1)
        dd = suave(pts, cerrado=False)
        L.add(f'<path d="{dd}" stroke="#050404" stroke-width="{1 + 4 * t:.1f}" opacity="0.5" fill="none"/>'
              f'<path d="{dd}" transform="translate(0 {1 + 3 * t:.1f})" stroke="{ROCA[3]}" stroke-width="{0.6 + 2 * t:.1f}" opacity="0.35" fill="none"/>')
    piedras = sorted((gr.uniform(0.05, 1) ** 1.3 * 0.9, gr.uniform(-1.1, 1.1)) for _ in range(46 if V else 60))
    for t, u in piedras:
        if abs(u) < 0.35 and t > 0.35:     # pasillo central despejado para los personajes
            continue
        x, y = cx + u * W0 * t, yv + Hf * t
        L.add(L.pedrusco(x, y, (14 + gr.uniform(0, 60)) * t * 2.4, (10 + gr.uniform(0, 40)) * t * 2.2, 1 if u < 0 else -1,
                         ("#060505", mezcla(ROCA[1], "#000000", 0.2), ROCA[3]), r=gr, brillo="#ffe9c8" if t > 0.3 else None))
    for _ in range(4):
        t = gr.uniform(0.25, 0.8)
        u = gr.choice([-1, 1]) * gr.uniform(0.25, 0.7)
        x, y = cx + u * W0 * t, yv + Hf * t
        rx, ry = 120 * t * 1.6, 18 * t * 1.6
        L.add(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{L.lg((0, "#050608"), (0.7, "#1a1612"), (1, "#5a4434"))}" opacity="0.9"/>'
              f'<ellipse cx="{x:.0f}" cy="{y + ry * 0.3:.0f}" rx="{rx * 0.45:.0f}" ry="{ry * 0.15:.0f}" fill="#ffd9a0" opacity="0.3"/>')
    # aros de la galería, de lejos a cerca
    luzf = lambda t: max(0.0, math.sin(math.pi * min(1, t / 0.9))) ** 1.2
    gm = (L._grad_cono("#08070a", ROCA[1], ROCA[3], -1), L._grad_cono("#08070a", ROCA[1], ROCA[3], 1))
    sv = L.lg((0, "#050506", 0.95), (0.6, "#050506", 0.4), (1, "#050506", 0))
    aros = []
    for i, s_ in enumerate(escalas):
        t = i / (len(escalas) - 1)
        lf = luzf(t) * (0.35 if i == len(escalas) - 1 else 1)
        pts, dh = _aro(L, s_, cx + math.sin(i * 1.3) * W0 * s_ * 0.12, yv, W0 * (1 + 0.12 * math.sin(i * 2.1)), Hc * (1 + 0.1 * math.cos(i * 1.7)), Hf, r, amp=0.1)
        d = f"M-300 -300 L{w + 300} -300 L{w + 300} {h + 300} L-300 {h + 300} Z " + dh
        aros.append(d)
        c_luz = mezcla(mezcla("#151217", ROCA[3], lf), "#3a4a62", (1 - t) * 0.5)
        c_med = mezcla(mezcla("#0c0a0d", ROCA[1], lf), "#1c2434", (1 - t) * 0.5)
        g = L.rgu(cx, yv - Hc * s_ * 0.2, W0 * s_ * 1.7, (Hc * 0.75 + Hf) * s_ * 0.9, (0, c_luz, 1), (0.55, c_luz, 1), (0.8, c_med, 1), (1, "#050406", 1))
        L.add(f'<path d="{d}" fill="{g}" fill-rule="evenodd"/>')
        cl = L.id("c")
        L.defs.append(f'<clipPath id="{cl}"><path d="{d}" clip-rule="evenodd"/></clipPath>')
        cuerpo = []
        # estratos concéntricos que siguen la forma del aro (capas de roca)
        for j in range(1, 6):
            f = 1 + j * 0.07 + r.uniform(-0.02, 0.02)
            pp = [(cx + (x - cx) * f + r.uniform(-3, 3) * s_ * 4, yv + (y - yv) * f + r.uniform(-3, 3) * s_ * 4) for x, y in pts]
            cuerpo.append(f'<path d="{suave(pp, cerrado=False)}" stroke="#050406" stroke-width="{max(0.6, 5 * s_):.1f}" opacity="0.35" fill="none"/>')
        # manchas de humedad que bajan por las paredes
        hm = []
        for _ in range(int(4 + 8 * s_)):
            px, py = r.choice(pts)
            hl = r.uniform(60, 300) * s_
            hm.append(f'<ellipse cx="{px + r.uniform(-30, 30) * s_:.0f}" cy="{py + hl / 2:.0f}" rx="{max(2, 18 * s_):.0f}" ry="{hl:.0f}" fill="#050407" opacity="0.4"/>')
        cuerpo.append('<g filter="url(#blur8)">' + "".join(hm) + "</g>")
        # brillos húmedos cerca del borde interior iluminado
        for _ in range(int(10 + 50 * s_ * lf)):
            px, py = r.choice(pts)
            px += (px - cx) * r.uniform(0.0, 0.08)
            py += (py - yv) * r.uniform(0.0, 0.08)
            cuerpo.append(f'<path d="M{px:.0f} {py:.0f} l0 {r.uniform(2, 9) * (0.4 + s_):.1f}" stroke="#fff1d8" stroke-width="{1 + s_ * 1.5:.1f}" opacity="{0.3 + 0.6 * lf:.2f}" stroke-linecap="round"/>')
        L.add(f'<g clip-path="url(#{cl})">' + "".join(cuerpo) + "</g>")
        # luz de borde en el canto interior
        L.add(f'<path d="{suave(pts, cerrado=False, t=0.45)}" stroke="{mezcla(c_luz, CALIDA[0], 0.5)}" stroke-width="{max(1, 5 * s_):.1f}" opacity="{0.2 + 0.6 * lf:.2f}" fill="none"/>')
        # estalactitas que cuelgan de la bóveda de este aro
        if s_ > 0.08:
            ga = (L._grad_cono("#060507", c_med, c_luz, -1), L._grad_cono("#060507", c_med, c_luz, 1))
            for (x, y) in pts[7:16]:
                if r.random() < 0.6:
                    L.add(L.estalactita(x + r.uniform(-20, 20) * s_, y - 4 * s_, r.uniform(60, 220) * s_, r.uniform(16, 44) * s_,
                                        ga[1] if x < cx else ga[0], r=r, c_osc="#000", sombra_v=sv, gota_col="#ffe9c8"))
            for (x, y) in (pts[1], pts[-2]):
                L.add(L.estalagmita(x + (40 if x < cx else -40) * s_, yv + Hf * s_ + 2, r.uniform(80, 220) * s_, r.uniform(40, 90) * s_,
                                    ga[1] if x < cx else ga[0], r=r, c_osc="#000", c_brillo="#fff1d8"))
        if i in (3, 5):
            L.add(L.bruma(yv + Hf * s_ * 0.6, Hc * s_ * 1.6, "#4a5872", 0.18))
    L.add(L.relieve(sem + 5, freq="0.007 0.016", escala=7, az=270, elev=40, op=0.55, oct=4))
    ly = yv + Hf * 0.42
    L.add(L.luz(cx, ly, W0 * 0.9, Hf * 0.35, "#d07a30", 0.45))
    L.add(L.oscuridad(cx, ly - Hf * 0.05, W0 * 1.6, Hf * 0.9, op=0.9, medio=0.45))
    L.add(L.polvo(70, cx - W0 * 0.6, yv - 300, cx + W0 * 0.6, yv + 400, "#ffe2b0", 2, 0.5, sem=sem + 9))
    return {"suelo": round(yv + Hf * 0.4), "nota": f"pasillo central despejado; punto de fuga ({cx:.0f},{yv})"}


def bg_cueva_pozo(L, sem=41):
    """Pozo vertical visto desde dentro mirando hacia arriba: boca de luz diurna pequeña arriba, paredes que bajan, abajo negro."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    cx = w / 2
    yo = 400 if V else 150      # boca de luz
    D = 520 if V else 240       # cuánto baja el centro de cada aro con la escala (perspectiva)
    R = w * (0.5 if V else 0.36)
    escalas = [0.06, 0.085, 0.12, 0.165, 0.22, 0.29, 0.38, 0.5, 0.66, 0.86, 1.12]
    L.add(L.rect(L.lg((0, "#0a0f18"), (0.5, "#05070b"), (1, "#010103"))))
    # cielo en la boca (dentro del primer aro)
    bx, by, brx, bry = cx, yo + D * 0.06 * 0.55, R * 0.06 * 1.15, R * 0.06 * 0.8
    L.add(L.brillo(bx, by, brx * 6, bry * 9, "#cfe6ff", 0.55))
    L.add(f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="{brx * 1.4:.0f}" ry="{bry * 1.4:.0f}" fill="{L.rgu(bx, by - bry * 0.3, brx * 1.4, bry * 1.4, (0, "#ffffff", 1), (0.6, "#e8f6ff", 1), (1, "#9cc8ee", 1))}"/>')
    # haz de luz que cae
    for k in range(7):
        dx = r.uniform(-1, 1)
        top = brx * 0.8
        bot = R * r.uniform(0.25, 0.6)
        xb = cx + dx * R * 0.3
        L.add(f'<path d="M{bx - top * (0.3 + dx * 0.4):.0f} {by:.0f} L{bx + top * (0.3 - dx * 0.4) + 8:.0f} {by:.0f} L{xb + bot / 2:.0f} {h:.0f} L{xb - bot / 2:.0f} {h:.0f} Z" '
              f'fill="{L.lg((0, "#dcefff", 0.22), (0.5, "#9cc4ee", 0.06), (1, "#9cc4ee", 0))}"/>')
    luzf = lambda t: (1 - t) ** 1.6
    for i, s_ in enumerate(escalas):
        t = i / (len(escalas) - 1)
        ccy = yo + D * s_ * 0.55
        rx, ry = R * s_ * 1.15, R * s_ * 0.8
        cxx = cx + math.sin(i * 1.9) * R * s_ * 0.1
        pts = []
        n = 22
        for k in range(n):
            a = 2 * math.pi * k / n
            rr = 1 + r.uniform(-0.12, 0.12) + 0.09 * math.sin(a * 3 + i * 1.7) + 0.05 * math.sin(a * 5 + i)
            pts.append((cxx + math.cos(a) * rx * rr, ccy + math.sin(a) * ry * rr))
        dh = suave(pts, t=0.5)
        d = f"M-300 -300 L{w + 300} -300 L{w + 300} {h + 300} L-300 {h + 300} Z " + dh
        lf = luzf(t)
        c_luz = mezcla(mezcla("#0d0f14", "#7f8fa6", lf), ROCA[2], 0.25 * (1 - lf) * t)
        c_med = mezcla("#07080c", mezcla("#2a3242", ROCA[1], 0.4), lf * 0.8 + 0.2 * (1 - t))
        g = L.rgu(bx, by, rx * 1.9, ry * 2.4 + D * s_ * 0.5, (0, c_luz, 1), (0.5, c_luz, 1), (0.8, c_med, 1), (1, "#030305", 1))
        L.add(f'<path d="{d}" fill="{g}" fill-rule="evenodd"/>')
        cl = L.id("c")
        L.defs.append(f'<clipPath id="{cl}"><path d="{d}" clip-rule="evenodd"/></clipPath>')
        cuerpo = []
        for j in range(1, 5):
            f = 1 + j * 0.08
            pp = [(cxx + (x - cxx) * f, ccy + (y - ccy) * f + r.uniform(-2, 2)) for x, y in pts]
            cuerpo.append(f'<path d="{suave(pp)}" stroke="#020203" stroke-width="{max(0.6, 4 * s_):.1f}" opacity="0.35" fill="none"/>')
        for _ in range(int(14 + 40 * s_)):  # brillos de agua que rezuma, hacia el lado de la luz (arriba)
            x, y = r.choice(pts[n // 2:])
            cuerpo.append(f'<path d="M{x:.0f} {y:.0f} l0 {r.uniform(2, 10) * (0.4 + s_):.1f}" stroke="#eaf6ff" stroke-width="{0.8 + s_:.1f}" '
                          f'opacity="{0.25 + 0.6 * lf:.2f}" stroke-linecap="round"/>')
        hm = [f'<ellipse cx="{x + r.uniform(-20, 20) * s_:.0f}" cy="{y + 120 * s_:.0f}" rx="{max(2, 16 * s_):.0f}" ry="{220 * s_:.0f}" fill="#020203" opacity="0.4"/>'
              for x, y in r.sample(pts, 6)]
        cuerpo.append('<g filter="url(#blur8)">' + "".join(hm) + "</g>")
        L.add(f'<g clip-path="url(#{cl})">' + "".join(cuerpo) + "</g>")
        L.add(f'<path d="{suave(pts[n // 2 + 2:] + pts[:2], cerrado=False)}" stroke="#d8ecff" stroke-width="{max(1, 3 * s_):.1f}" opacity="{0.05 + 0.4 * lf:.2f}" fill="none"/>')
    L.add(L.relieve(sem + 3, freq="0.012 0.006", escala=7, az=270, elev=35, op=0.5, oct=4))
    L.add(L.rect(L.lg((0, "#000000", 0), (0.55, "#000000", 0), (0.85, "#010103", 0.8), (1, "#000000", 0.97))))
    L.add(L.luz(bx, by, brx * 4, bry * 6, "#ffffff", 0.5))
    L.add(L.polvo(110 if V else 120, cx - R * 0.35, by + 20, cx + R * 0.35, h * 0.8, "#e6f2ff", 1.8, 0.5, sem=sem + 5))
    return {"centro": (round(cx), round(h * (0.55 if V else 0.5))), "nota": f"boca de luz en ({bx:.0f},{by:.0f}); la persona colgada va en el centro"}


def bg_corte_tierra(L, sem=51):
    """Corte transversal de la ladera: cielo y superficie andaluza arriba, capas de roca, sala con luz a «70 m»."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    ysup = 470 if V else 175            # superficie
    ysala = 1330 if V else 790          # sala (centro)
    xsala = w * (0.56 if V else 0.6)
    # cielo
    L.add(L.rect(L.lg((0, "#6fb6e8"), (1, "#d6eefa")), h=ysup + 40))
    for k in range(4 if V else 6):
        nx, ny = r.uniform(0, w), r.uniform(60, ysup - 150)
        L.add(f'<g opacity="0.85">' + "".join(f'<ellipse cx="{nx + j * 40 + r.uniform(-10, 10):.0f}" cy="{ny + r.uniform(-8, 8):.0f}" rx="{r.uniform(40, 70):.0f}" ry="{r.uniform(14, 24):.0f}" fill="#ffffff"/>' for j in range(4)) + '</g>')
    # sierra lejana
    sp = [(-20, ysup - 50)] + [(x, ysup - 60 - r.uniform(20, 110)) for x in range(0, w + 80, 80)] + [(w + 20, ysup - 50), (w + 20, ysup + 20), (-20, ysup + 20)]
    L.add(f'<path d="{suave(sp, t=0.3)}" fill="#9fb4c6" opacity="0.8"/>')
    # capas de roca (estratos inclinados de colores distintos)
    capas = ["#c9a26b", "#a77b45", "#8a5f3a", "#b08a60", "#6b4a32", "#7d5a48", "#5a3f2c", "#4a3528", "#3d2a1f", "#2e2018", "#1f1610"]
    ys = [ysup]
    while ys[-1] < h + 60:
        ys.append(ys[-1] + r.uniform(70, 170) * (1 if V else 0.6))
    paths = []
    for i in range(len(ys) - 1):
        top = linea_ruido(r, -20, ys[i] + (0 if i == 0 else 0), w + 20, ys[i] + (0 if i == 0 else r.uniform(-50, 50)), 12, 12 if i else 6, 0.7)
        if i == 0:
            top = [(x, y) for x, y in top]
        prev = top
        bot = [(w + 20, h + 100), (-20, h + 100)]
        d = suave(top, cerrado=False) + " " + " ".join(f"L{x:.0f} {y:.0f}" for x, y in bot) + " Z"
        c = capas[min(i, len(capas) - 1)]
        L.add(L.roca(d, (-20, ys[i] - 60, w + 20, h + 100), mezcla(c, "#000000", 0.35), c, mezcla(c, "#ffffff", 0.12),
                     luz=(0.3, 0), sem=sem + i, estratos=4, inclin=0.02, vetas=4, humedad=0, brillos=0, contraste=0.8))
        paths.append(d)
        # piedras/cantos y fósiles dentro de la capa
        for _ in range(int(w / 80)):
            x = r.uniform(0, w)
            y = ys[i] + r.uniform(20, ys[i + 1] - ys[i])
            sz = r.uniform(4, 14)
            L.add(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{sz:.0f}" ry="{sz * 0.6:.0f}" fill="{mezcla(c, "#000000", 0.3)}" opacity="0.7"/>'
                  f'<path d="M{x - sz * 0.6:.0f} {y - sz * 0.3:.0f} q{sz * 0.6:.0f} {-sz * 0.4:.0f} {sz * 1.2:.0f} 0" stroke="{mezcla(c, "#ffffff", 0.3)}" stroke-width="1.5" opacity="0.6" fill="none"/>')
    # superficie: tierra seca, matorral y olivos pequeños sobre la línea
    L.add(f'<path d="M-20 {ysup} L{w + 20} {ysup}" stroke="#e8c890" stroke-width="3" opacity="0.6"/>')
    for k in range(int(w / 70)):
        x = r.uniform(0, w)
        L.add(f'<ellipse cx="{x:.0f}" cy="{ysup - 4:.0f}" rx="{r.uniform(6, 14):.0f}" ry="{r.uniform(4, 8):.0f}" fill="#6f7a44"/>')
    for k in range(5 if V else 9):
        x = (k + 0.5) / (5 if V else 9) * w + r.uniform(-30, 30)
        if abs(x - w * 0.3) < 40:
            continue
        L.add(_olivo(L, x, ysup, r.uniform(0.45, 0.7), r))
    # pasadizo sinuoso desde la boca hasta la sala
    xb = w * 0.3
    camino = [(xb, ysup)]
    y = ysup
    while y < ysala - 40:
        y += r.uniform(60, 120) * (1 if V else 0.6)
        camino.append((camino[-1][0] + r.uniform(-60, 90) + (xsala - camino[-1][0]) * 0.18, min(y, ysala - 40)))
    camino.append((xsala - (90 if V else 70), ysala))
    dcam = suave(camino, cerrado=False)
    L.add(f'<path d="{dcam}" stroke="#e8c890" stroke-width="{18 if V else 13}" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.25"/>',
          f'<path d="{dcam}" stroke="#1a110c" stroke-width="{13 if V else 9}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
          f'<path d="{dcam}" transform="translate(-2 2)" stroke="#3a281c" stroke-width="{4 if V else 3}" fill="none" stroke-linecap="round" opacity="0.8"/>')
    L.add(f'<path d="M{xb - 26} {ysup + 2} Q{xb} {ysup - 18} {xb + 26} {ysup + 2} Z" fill="#0a0706"/>')
    # la sala: cavidad con suelo y un punto de luz cálida
    sw, sh = (360, 210) if V else (360, 170)
    sp = [(xsala - sw * 0.5, ysala + sh * 0.42), (xsala - sw * 0.52, ysala + sh * 0.05)]
    for k in range(1, 10):
        th = math.pi * k / 10
        sp.append((xsala - math.cos(th) * sw * 0.5 + r.uniform(-8, 8), ysala + sh * 0.05 - math.sin(th) * sh * 0.6 + r.uniform(-10, 10)))
    sp += [(xsala + sw * 0.52, ysala + sh * 0.08), (xsala + sw * 0.48, ysala + sh * 0.42)]
    dsala = suave(sp, t=0.4)
    L.add(f'<path d="{dsala}" fill="{L.rgu(xsala, ysala + sh * 0.25, sw * 0.6, sh * 0.8, (0, "#7a4a24", 1), (0.5, "#2a1a10", 1), (1, "#0a0706", 1))}"/>')
    gm = (L._grad_cono("#0a0706", "#2a1a10", "#8a5a30", -1), L._grad_cono("#0a0706", "#2a1a10", "#8a5a30", 1))
    for k in range(7):
        x = xsala - sw * 0.35 + k * sw * 0.11 + r.uniform(-8, 8)
        L.add(L.estalactita(x, ysala - sh * 0.45 + abs(x - xsala) * 0.25, r.uniform(16, 46), r.uniform(8, 14), gm[1] if x < xsala else gm[0], r=r, anillos=False))
    L.add(f'<path d="M{xsala - sw * 0.38:.0f} {ysala + sh * 0.38:.0f} Q{xsala:.0f} {ysala + sh * 0.3:.0f} {xsala + sw * 0.42:.0f} {ysala + sh * 0.36:.0f}" stroke="#c07a3a" stroke-width="3" opacity="0.6" fill="none"/>')
    L.add(L.luz(xsala, ysala + sh * 0.25, sw * 0.9, sh * 1.2, "#ff9a3a", 0.7))
    L.add(f'<circle cx="{xsala:.0f}" cy="{ysala + sh * 0.25:.0f}" r="7" fill="#fff2c8"/>', L.brillo(xsala, ysala + sh * 0.25, 40, 40, "#ffcf8a", 0.9))
    L.add(L.relieve(sem + 7, freq="0.004 0.02", escala=5, az=250, elev=45, op=0.35, oct=4, caja=(0, ysup, w, h - ysup)))
    # escala vertical: muescas sutiles en el lado izquierdo (sin números)
    xm = 46 if V else 56
    paso = (ysala - ysup) / 7
    marcas = []
    for k in range(29):
        y = ysup + k * paso / 4
        if y > h - 10:
            break
        larga = k % 4 == 0
        marcas.append(f'<path d="M{xm} {y + 1.5:.0f} L{xm + (26 if larga else 12)} {y + 1.5:.0f}" stroke="#1a110c" stroke-width="{2.4 if larga else 1.4}" opacity="0.5"/>'
                      f'<path d="M{xm} {y:.0f} L{xm + (26 if larga else 12)} {y:.0f}" stroke="#f3e6d0" stroke-width="{2.4 if larga else 1.4}" opacity="{0.8 if larga else 0.5}"/>')
    L.add(f'<path d="M{xm} {ysup} L{xm} {min(h - 10, ysup + 7 * paso):.0f}" stroke="#f3e6d0" stroke-width="2" opacity="0.6"/>' + "".join(marcas))
    L.add(L.oscuridad(w / 2, h * 0.4, w * 0.9, h * 0.8, op=0.5, medio=0.15))
    return {"centro": (round(xsala), round(ysala)), "nota": f"superficie y={ysup}; sala a «70 m» en ({xsala:.0f},{ysala}); muescas en x={xm}, una larga cada 10 m"}


def _olivo(L, x, y, s, r, sombra=None, c_hoja="#5b6b3a", c_luz="#8a9a5a", c_tronco="#4a3a2a"):
    """Olivo pequeño: tronco retorcido y copa de manchas de hoja (claras arriba a la izquierda)."""
    out = []
    if sombra:
        dx, op = sombra
        out.append(f'<ellipse cx="{x + dx * s:.0f}" cy="{y + 4 * s:.0f}" rx="{abs(dx) * s * 0.9 + 60 * s:.0f}" ry="{10 * s:.0f}" fill="#1a1020" opacity="{op}"/>')
    else:
        out.append(f'<ellipse cx="{x:.0f}" cy="{y + 3 * s:.0f}" rx="{70 * s:.0f}" ry="{9 * s:.0f}" fill="#2a2010" opacity="0.35"/>')
    out.append(f'<path d="M{x - 8 * s:.0f} {y:.0f} C{x - 4 * s:.0f} {y - 40 * s:.0f} {x - 18 * s:.0f} {y - 60 * s:.0f} {x - 6 * s:.0f} {y - 90 * s:.0f} '
               f'L{x + 6 * s:.0f} {y - 88 * s:.0f} C{x + 2 * s:.0f} {y - 60 * s:.0f} {x + 14 * s:.0f} {y - 40 * s:.0f} {x + 9 * s:.0f} {y:.0f} Z" fill="{c_tronco}"/>')
    for k in range(16):
        bx = x + r.uniform(-70, 70) * s
        by = y - 100 * s - r.uniform(-35, 40) * s - (70 * s - abs(bx - x)) * 0.25
        rr = r.uniform(20, 34) * s
        col = mezcla(c_hoja, "#000000", 0.25) if by > y - 100 * s else c_hoja
        out.append(f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="{rr:.0f}" ry="{rr * 0.75:.0f}" fill="{col}"/>')
    for k in range(8):
        bx = x + r.uniform(-60, 30) * s
        by = y - 130 * s + r.uniform(-15, 25) * s
        out.append(f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="{r.uniform(8, 16) * s:.0f}" ry="{r.uniform(5, 9) * s:.0f}" fill="{c_luz}" opacity="0.7"/>')
    return "".join(out)


# ============================================================================ exteriores
def _nube(L, x, y, s, r, c_luz="#ffffff", c_sombra="#c9dcef", op=0.95, n=9):
    """Cúmulo: muchas bolas de tamaños distintos (las del centro más altas), luz arriba, base en sombra que se funde."""
    out = []
    g = L.lg((0, c_luz), (0.5, c_luz), (1, c_sombra))
    ancho = n * 26 * s
    for capa in range(2):
        for k in range(n - capa * 3):
            t = (k + 0.5) / (n - capa * 3)
            bx = x - ancho / 2 + ancho * t + r.uniform(-12, 12) * s
            rr = (22 + 46 * math.sin(math.pi * t) ** 1.5) * s * r.uniform(0.75, 1.2) * (0.8 if capa else 1)
            by = y - rr * 0.55 - capa * 30 * s * math.sin(math.pi * t)
            out.append(f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{rr:.0f}" fill="{g}"/>')
    out.append(f'<ellipse cx="{x:.0f}" cy="{y - 4 * s:.0f}" rx="{ancho * 0.52:.0f}" ry="{14 * s:.0f}" fill="{c_sombra}" opacity="0.8" filter="url(#blur8)"/>')
    return f'<g opacity="{op}">' + "".join(out) + "</g>"


def _matorral(L, x, y, s, r, c="#6f7a44", luz="#b8c27a", sombra=None):
    out = []
    if sombra:
        dx, op = sombra
        out.append(f'<ellipse cx="{x + dx * s * 0.5:.0f}" cy="{y + 3 * s:.0f}" rx="{abs(dx) * s * 0.55 + 26 * s:.0f}" ry="{6 * s:.0f}" fill="#1a1020" opacity="{op}"/>')
    else:
        out.append(f'<ellipse cx="{x:.0f}" cy="{y + 2 * s:.0f}" rx="{30 * s:.0f}" ry="{6 * s:.0f}" fill="#2a2010" opacity="0.35"/>')
    for k in range(9):
        bx, by = x + r.uniform(-24, 24) * s, y - r.uniform(4, 26) * s
        rr = r.uniform(8, 15) * s
        out.append(f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="{rr:.0f}" ry="{rr * 0.8:.0f}" fill="{mezcla(c, "#000000", 0.3) if by > y - 12 * s else c}"/>')
    for k in range(5):
        bx, by = x + r.uniform(-18, 10) * s, y - r.uniform(16, 30) * s
        out.append(f'<ellipse cx="{bx:.0f}" cy="{by:.0f}" rx="{r.uniform(4, 8) * s:.0f}" ry="{r.uniform(3, 5) * s:.0f}" fill="{luz}" opacity="0.6"/>')
    return "".join(out)


ENTRADA = {
    "dia": dict(cielo=[(0, "#4f9ed8"), (0.5, "#6fb6e8"), (1, "#d6eefa")], sierra="#a9c3da", nieve="#f2f8ff", lomas=["#b9a27a", "#a68a5e", "#8f7448"],
                tierra=("#7a5a34", "#a77b45", "#c9a26b"), roca=("#4a3c2c", "#9a8462", "#d4c19a"), olivo="#5b6b3a", olivo_luz="#9aab6a",
                mat="#6f7a44", mat_luz="#b8c27a", nube=("#ffffff", "#c9dcef"), sombra=None, luz_borde="#fff4dc", boca="#0a0705"),
    "tarde": dict(cielo=[(0, "#2a1d4a"), (0.35, "#6a3a78"), (0.65, "#d0603a"), (0.85, "#f59a4a"), (1, "#ffd08a")], sierra="#8a6a8a", nieve="#ffc9a0",
                  lomas=["#8a5a50", "#704a44", "#583a38"], tierra=("#4a2e2a", "#7a4a34", "#b8743e"), roca=("#2e2030", "#7a5040", "#e89a5a"),
                  olivo="#3a3a28", olivo_luz="#c08a4a", mat="#4a4a2c", mat_luz="#d89a50", nube=("#ffc890", "#8a5a8a"), sombra=(150, 0.45),
                  luz_borde="#ffb060", boca="#080406"),
}


def _entrada(L, hora, sem=61):
    w, h, V = L.w, L.h, L.v
    P = ENTRADA[hora]
    r = random.Random(sem)
    yh = 640 if V else 300                       # horizonte (pie de la sierra)
    ysuelo = 1330 if V else 830                  # explanada delante de la boca
    bx, by = (w * 0.56, 1040) if V else (w * 0.6, 560)   # centro de la boca
    bw, bh = (330, 250) if V else (330, 230)
    L.add(L.rect(L.lg(*P["cielo"]), h=yh + 200))
    if hora == "tarde":   # sol bajo a la izquierda
        sx, sy = w * 0.16, yh - (300 if V else 150)
        L.add(L.brillo(sx, sy, w * 0.7, 420, "#ffcf8a", 0.55), L.brillo(sx, sy, 160, 160, "#fff0c8", 0.9),
              f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="44" fill="#fff4d8"/>')
    for k in range(3 if V else 5):
        L.add(_nube(L, r.uniform(0, w), r.uniform(120, yh - 260), r.uniform(0.6, 1.1), r, *P["nube"], op=0.92))
    # Sierra Nevada lejana: picos con nieve arriba (borde inferior dentado)
    sp = [(-20, yh + 10)]
    x = -20
    while x < w + 40:
        x += r.uniform(50, 120)
        alto = 70 + r.uniform(0, 140) + 70 * math.sin(x / w * 3.1 + 0.5)
        sp.append((x, yh - alto))
    sp.append((w + 20, yh + 10))
    dsi = suave(sp, t=0.15)
    L.add(f'<path d="{dsi}" fill="{L.lg((0, P["sierra"]), (1, mezcla(P["sierra"], P["cielo"][-1][1], 0.4)))}"/>')
    cls = L.clip(dsi)
    ny = yh - 175
    nv = [(-30, ny)] + [(xx, ny + r.uniform(-25, 30) + (18 if i % 2 else -10)) for i, xx in enumerate(range(0, w + 40, 30))] + [(w + 30, ny)]
    L.add(f'<g clip-path="{cls}"><path d="M-30 -10 L{w + 30} -10 ' + " ".join(f"L{a:.0f} {b:.0f}" for a, b in reversed(nv)) + f' Z" fill="{P["nieve"]}" opacity="0.92"/>'
          + "".join(f'<path d="M{a:.0f} {b - 60:.0f} l{r.uniform(-8, 8):.0f} {r.uniform(50, 90):.0f}" stroke="{P["sierra"]}" stroke-width="{r.uniform(2, 5):.0f}" opacity="0.6"/>' for a, b in sp[1:-1])
          + "</g>")
    # lomas con hileras de olivos
    for i, c in enumerate(P["lomas"]):
        y0 = yh + 20 + i * (90 if V else 55)
        pts = linea_ruido(r, -40, y0, w + 40, y0 + r.uniform(-30, 30), 10, 30, 0.5)
        d = suave(pts, cerrado=False) + f" L{w + 40} {h} L-40 {h} Z"
        L.add(f'<path d="{d}" fill="{c}"/>')
        for j in range(int(w / (26 - i * 4))):
            x = r.uniform(0, w)
            yy = y0 + 20 + r.uniform(0, 70 if V else 40) + (i * 6)
            rr = (3 + i * 2.2) * (1 if V else 0.9)
            L.add(f'<ellipse cx="{x:.0f}" cy="{yy:.0f}" rx="{rr * 1.3:.1f}" ry="{rr:.1f}" fill="{mezcla(P["olivo"], c, 0.35 - i * 0.1)}"/>')
            if P["sombra"]:
                L.add(f'<ellipse cx="{x + rr * 3:.0f}" cy="{yy + rr * 0.8:.0f}" rx="{rr * 3:.1f}" ry="{rr * 0.4:.1f}" fill="#1a1020" opacity="0.35"/>')
        L.add(L.bruma(y0 + 10, 60, mezcla(P["cielo"][-1][1], "#ffffff", 0.2), 0.3))
    # ladera cercana: tierra seca subiendo hacia la derecha
    lad = [(-40, ysuelo - (60 if V else 40)), (w * 0.25, ysuelo - (90 if V else 70)), (w * 0.4, by - bh * 0.9), (bx - bw * 0.3, by - bh * 1.25),
           (bx + bw * 0.6, by - bh * 1.45), (w * 0.9, by - bh * 1.65), (w + 40, by - bh * 1.7), (w + 40, h + 40), (-40, h + 40)]
    dl = suave(lad, t=0.4)
    L.add(L.roca(dl, (-40, by - bh * 1.7, w + 40, h), P["tierra"][0], P["tierra"][1], P["tierra"][2], luz=(0.1 if hora == "tarde" else 0.3, 0),
                 sem=sem + 1, estratos=10, inclin=-0.15, vetas=8, humedad=0, brillos=0, contraste=0.6))
    # afloramiento calizo alrededor de la boca
    af = linea_ruido(r, bx - bw * 1.3, by + bh * 0.8, bx - bw * 0.9, by - bh * 1.15, 6, 30, 1)[:-1] + \
        linea_ruido(r, bx - bw * 0.9, by - bh * 1.15, bx + bw * 0.8, by - bh * 1.5, 8, 26, 1)[:-1] + \
        linea_ruido(r, bx + bw * 0.8, by - bh * 1.5, bx + bw * 1.5, by + bh * 0.7, 6, 30, 1)
    da = suave(af, t=0.3)
    L.add(L.roca(da, (bx - bw * 1.3, by - bh * 1.5, bx + bw * 1.5, by + bh * 0.8), P["roca"][0], P["roca"][1], P["roca"][2],
                 luz=(0.0 if hora == "tarde" else 0.25, 0.1), sem=sem + 2, estratos=9, inclin=-0.12, vetas=14, humedad=6, brillos=0,
                 borde=P["luz_borde"], borde_op=0.6))
    # la boca: hueco oscuro irregular con profundidad (borde iluminado arriba, garganta negra)
    bp = []
    for k in range(16):
        a_ = 2 * math.pi * k / 16
        rr = 1 + r.uniform(-0.1, 0.1)
        yy = by + math.sin(a_) * bh / 2 * rr
        if math.sin(a_) > 0.3:
            yy = by + bh * 0.42 + r.uniform(-6, 6)     # labio inferior casi plano
        bp.append((bx + math.cos(a_) * bw / 2 * rr, yy))
    dbo = suave(bp, t=0.4)
    L.add(f'<path d="{dbo}" fill="{L.rgu(bx, by + bh * 0.1, bw * 0.55, bh * 0.6, (0, "#000000", 1), (0.6, P["boca"], 1), (1, mezcla(P["roca"][0], "#000000", 0.3), 1))}"/>')
    L.add(f'<path d="{suave(bp[9:16] + bp[:1], cerrado=False, t=0.4)}" stroke="{P["luz_borde"]}" stroke-width="4" opacity="0.55" fill="none"/>')
    L.add(f'<path d="{suave([(x, y + 8) for x, y in bp[9:16]], cerrado=False)}" stroke="#000" stroke-width="14" opacity="0.45" fill="none" filter="url(#blur8)"/>')
    # explanada delante de la boca: tierra pisada, más clara y llana
    exp = linea_ruido(r, -40, ysuelo - 30, w + 40, ysuelo - 50, 10, 14, 0.6)
    dex = suave(exp, cerrado=False) + f" L{w + 40} {h + 40} L-40 {h + 40} Z"
    L.add(f'<path d="{dex}" fill="{L.lg((0, P["tierra"][2]), (0.5, P["tierra"][1]), (1, P["tierra"][0]))}"/>')
    L.add(f'<path d="{suave(exp, cerrado=False)}" stroke="{P["luz_borde"]}" stroke-width="2" opacity="0.4" fill="none"/>')
    for _ in range(int(w / 12)):   # gravilla
        x, y = r.uniform(0, w), r.uniform(ysuelo - 20, h)
        t = (y - ysuelo) / (h - ysuelo + 1)
        sz = r.uniform(1.5, 4) * (1 + t * 2)
        L.add(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{sz:.1f}" ry="{sz * 0.6:.1f}" fill="{P["tierra"][0]}" opacity="0.6"/>'
              f'<ellipse cx="{x - sz * 0.3:.0f}" cy="{y - sz * 0.3:.0f}" rx="{sz * 0.5:.1f}" ry="{sz * 0.25:.1f}" fill="{P["luz_borde"]}" opacity="0.4"/>')
    # senda pisada que sale de la boca y piedras sueltas
    sen = [(bx, by + bh * 0.45), (bx - bw * 0.1, ysuelo - 20), (w * 0.42, ysuelo + (h - ysuelo) * 0.4), (w * 0.3, h + 20)]
    L.add(f'<path d="{suave(sen, cerrado=False)}" stroke="{P["tierra"][2]}" stroke-width="{70 if V else 60}" opacity="0.35" fill="none" stroke-linecap="round" filter="url(#blur8)"/>')
    for _ in range(14 if V else 18):
        x, y = r.uniform(0, w), r.uniform(ysuelo, h)
        if abs(x - w / 2) < w * 0.25 and y < ysuelo + (180 if V else 120):
            continue
        t = (y - ysuelo) / (h - ysuelo)
        an = (18 + r.uniform(0, 40)) * (0.7 + t * 2)
        L.add(L.pedrusco(x, y, an, an * 0.55, -1 if hora == "tarde" else -1, (P["roca"][0], P["roca"][1], P["roca"][2]), r=r))
        if P["sombra"]:
            L.add(f'<ellipse cx="{x + an * 1.3:.0f}" cy="{y + 2:.0f}" rx="{an * 1.4:.0f}" ry="{an * 0.12:.0f}" fill="#1a1020" opacity="0.4"/>')
    # olivos y matorral sobre la ladera (sin tapar la boca), y en primer término
    for k in range(4 if V else 7):
        x = r.uniform(0, w)
        if abs(x - bx) < bw:
            continue
        y = ysuelo - r.uniform(60, 160 if V else 110)
        L.add(_olivo(L, x, y, r.uniform(0.6, 0.9), r, sombra=P["sombra"], c_hoja=P["olivo"], c_luz=P["olivo_luz"]))
    for k in range(int(w / 70)):
        x = r.uniform(0, w)
        y = r.uniform(by - bh * 1.6, ysuelo - 30)
        if abs(x - bx) < bw * 0.8 and y > by - bh * 0.7:
            continue
        L.add(_matorral(L, x, y, r.uniform(0.5, 1.0), r, P["mat"], P["mat_luz"], sombra=P["sombra"]))
    for x in (r.uniform(-20, w * 0.12), r.uniform(w * 0.88, w + 20)):
        L.add(_matorral(L, x, h - r.uniform(60, 160), r.uniform(2.2, 3.2), r, P["mat"], P["mat_luz"], sombra=P["sombra"]))
    L.add(L.relieve(sem + 5, freq="0.008 0.02", escala=6, az=200 if hora == "tarde" else 230, elev=40, op=0.4, oct=4,
                    caja=(0, yh, w, h - yh)))
    if hora == "tarde":
        L.add(L.luz(w * 0.1, yh, w * 0.9, h * 0.5, "#ff9a50", 0.35))
        L.add(L.rect(L.lg((0, "#2a1040", 0), (0.6, "#2a1040", 0.1), (1, "#1a0820", 0.45))))
    else:
        L.add(L.luz(w * 0.3, 0, w * 0.9, h * 0.4, "#fff6e0", 0.25))
    return {"suelo": ysuelo + (40 if V else 30), "nota": f"explanada desde y≈{ysuelo}; boca de la cueva en ({bx:.0f},{by:.0f}) {bw}×{bh}"}


def bg_entrada_dia(L):
    return _entrada(L, "dia")


def bg_entrada_atardecer(L):
    return _entrada(L, "tarde")


def bg_cueva_hielo(L, sem=71):
    """Cueva helada de los Alpes (1962): hielo azul translúcido con burbujas y grietas, carámbanos, suelo de nieve y roca."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    yf = 1180 if V else 600
    cx = w / 2
    L.add(L.rect(L.lg((0, "#0d1b2e"), (0.6, "#16304c"), (1, "#0d1b2e"))))
    # resplandor del fondo: luz que atraviesa el hielo
    L.add(L.brillo(cx + w * 0.08, yf - (380 if V else 200), w * 0.7, 700 if V else 420, "#5f9fd1", 0.7))
    L.add(L.brillo(cx + w * 0.08, yf - (420 if V else 220), w * 0.3, 300 if V else 180, "#a9d6f5", 0.6))

    def hielo(d, bbox, c1, c2, c3, luz=(0.5, 0.5), burb=30, grietas=8, capas=8, sem_=0):
        rr = random.Random(sem_)
        x0, y0, x1, y1 = bbox
        g = L.lg((0, c3), (0.5, c2), (1, c1), x1=luz[0], y1=luz[1], x2=1 - luz[0], y2=1 - luz[1])
        cl = L.clip(d)
        out = [f'<path d="{d}" fill="{g}" opacity="0.92"/>', f'<g clip-path="{cl}">']
        for k in range(capas):   # capas de hielo onduladas (más claras y más oscuras)
            yy = y0 + (y1 - y0) * (k + rr.uniform(0, 1)) / capas
            pts = linea_ruido(rr, x0 - 20, yy, x1 + 20, yy + rr.uniform(-60, 60), 10, 25, 0.5)
            out.append(f'<path d="{suave(pts, cerrado=False)}" stroke="{rr.choice([HIELO[0], HIELO[3]])}" stroke-width="{rr.uniform(4, 18):.0f}" '
                       f'opacity="{rr.uniform(0.08, 0.2):.2f}" fill="none"/>')
        for _ in range(4):        # zonas interiores que brillan (luz atrapada)
            out.append(L.brillo(rr.uniform(x0, x1), rr.uniform(y0, y1), rr.uniform(60, 200), rr.uniform(40, 140), HIELO[1], 0.35))
        for _ in range(grietas):   # grietas: línea blanca nítida con sombra azul
            px, py = rr.uniform(x0, x1), rr.uniform(y0, y1)
            pts = [(px, py)]
            ang = rr.uniform(0, 6.28)
            for _k in range(rr.randint(3, 7)):
                ang += rr.uniform(-0.7, 0.7)
                pts.append((pts[-1][0] + math.cos(ang) * rr.uniform(15, 50), pts[-1][1] + math.sin(ang) * rr.uniform(15, 50)))
            dd = "M" + " L".join(f"{a:.0f} {b:.0f}" for a, b in pts)
            out.append(f'<path d="{dd}" stroke="{HIELO[3]}" stroke-width="3" opacity="0.5" fill="none"/>'
                       f'<path d="{dd}" transform="translate(-1 -1)" stroke="#ffffff" stroke-width="1.3" opacity="0.8" fill="none"/>')
        for _ in range(burb):     # burbujas atrapadas
            bx_, by_, br = rr.uniform(x0, x1), rr.uniform(y0, y1), rr.uniform(1.5, 7)
            out.append(f'<circle cx="{bx_:.0f}" cy="{by_:.0f}" r="{br:.1f}" fill="{HIELO[0]}" opacity="0.25"/>'
                       f'<circle cx="{bx_:.0f}" cy="{by_:.0f}" r="{br:.1f}" fill="none" stroke="#ffffff" stroke-width="0.8" opacity="0.6"/>'
                       f'<circle cx="{bx_ - br * 0.35:.1f}" cy="{by_ - br * 0.35:.1f}" r="{br * 0.3:.1f}" fill="#ffffff" opacity="0.9"/>')
        out.append("</g>")
        out.append(f'<path d="{d}" fill="none" stroke="{HIELO[0]}" stroke-width="2.5" opacity="0.45"/>')
        return "".join(out)

    # pared del fondo de hielo
    dfar = f"M-40 -40 L{w + 40} -40 L{w + 40} {yf + 20} L-40 {yf + 20} Z"
    L.add(hielo(dfar, (-40, -40, w + 40, yf + 20), HIELO[4], HIELO[3], HIELO[2], luz=(0.55, 0.6), burb=70, grietas=14, capas=12, sem_=sem + 1))
    L.add(L.brillo(cx + w * 0.08, yf - (380 if V else 200), w * 0.45, 520 if V else 300, "#a9d6f5", 0.3))
    # paredes laterales de hielo (más cerca: más saturadas, más burbujas)
    for lado in (-1, 1):
        x_in = cx + lado * w * (0.3 if V else 0.36)
        pts = [(cx + lado * (w * 0.5 + 80), -40)] + linea_ruido(r, x_in, -20, cx + lado * w * (0.4 if V else 0.42), yf + 80, 9, 50, 0.7)[1:-1] + \
            [(cx + lado * w * (0.44 if V else 0.45), yf + 120), (cx + lado * (w * 0.5 + 80), yf + 200)]
        d = suave(pts)
        xs = [p[0] for p in pts]
        L.add(hielo(d, (min(xs), -40, max(xs), yf + 200), HIELO[4], HIELO[3], HIELO[1], luz=(0.5 - lado * 0.5, 0.5), burb=90, grietas=12, capas=10, sem_=sem + 5 + lado))
    # techo de hielo con carámbanos (translúcidos, con brillo blanco)
    yt = 180 if V else 90
    pt = linea_ruido(r, -40, yt, w + 40, yt + 20, 14, 40, 0.8)
    dt = suave([(-40, -40), (w + 40, -40)] + list(reversed(pt)))
    L.add(hielo(dt, (-40, -40, w + 40, yt + 60), HIELO[4], HIELO[3], HIELO[2], luz=(0.5, 1), burb=40, grietas=6, capas=4, sem_=sem + 9))
    gi = (L.lg((0, "#e8f6ff", 0.9), (0.3, "#a9d6f5", 0.75), (0.7, "#5f9fd1", 0.6), (1, "#22405e", 0.7), x2=1, y2=0),
          L.lg((0, "#22405e", 0.7), (0.3, "#5f9fd1", 0.6), (0.7, "#a9d6f5", 0.75), (1, "#e8f6ff", 0.9), x2=1, y2=0))
    f_t = _ytec_fn(pt)
    for _ in range(int(w / 26)):
        x = r.uniform(-10, w + 10)
        Lc = r.uniform(40, 340 if V else 200) * (1.5 if r.random() < 0.12 else 1)
        wb = r.uniform(8, 26) * (0.5 + Lc / 300)
        L.add(L.estalactita(x, f_t(x), Lc, wb, gi[0] if x > cx else gi[1], r=r, c_osc="#22405e", gota_col="#ffffff", anillos=False))
        L.add(f'<path d="M{x - wb * 0.15:.0f} {f_t(x) + 4:.0f} L{x - wb * 0.05:.0f} {f_t(x) + Lc * 0.7:.0f}" stroke="#ffffff" stroke-width="{max(1, wb * 0.08):.1f}" opacity="0.6"/>')
    # suelo: nieve con bultos y roca asomando
    sn = linea_ruido(r, -40, yf, w + 40, yf + 10, 14, 14, 0.6)
    ds = suave(sn, cerrado=False) + f" L{w + 40} {h + 40} L-40 {h + 40} Z"
    L.add(f'<path d="{ds}" fill="{L.lg((0, "#a9c8e2"), (0.3, "#d8ecfa"), (1, "#8fb4d4"))}"/>')
    for _ in range(int(w / 40)):   # rocas oscuras con nieve encima
        x, y = r.uniform(0, w), r.uniform(yf + 20, h)
        if abs(x - cx) < w * 0.28 and y < yf + (500 if V else 300):
            continue
        t = (y - yf) / (h - yf)
        L.add(L.pedrusco(x, y, (20 + r.uniform(0, 50)) * (0.6 + t * 2.5), (14 + r.uniform(0, 30)) * (0.6 + t * 2), 1,
                         ("#0d1b2e", "#2a3444", "#5a6a7a"), r=r, facetas=True))
        an = (20 + 25) * (0.6 + t * 2.5)
        L.add(f'<path d="M{x - an * 0.45:.0f} {y - (10 + 20) * (0.6 + t * 2) * 0.75:.0f} q{an * 0.45:.0f} {-an * 0.25:.0f} {an * 0.9:.0f} 0 q{-an * 0.4:.0f} {an * 0.12:.0f} {-an * 0.9:.0f} 0 Z" fill="#eef8ff" opacity="0.85"/>')
    for _ in range(int(w / 9)):   # destellos en la nieve
        x, y = r.uniform(0, w), r.uniform(yf + 10, h)
        L.add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(0.8, 2.2):.1f}" fill="#ffffff" opacity="{r.uniform(0.4, 1):.2f}"/>')
    for k in range(10):   # ondulaciones de la nieve
        y = yf + (h - yf) * (k + 0.5) / 10
        pts = linea_ruido(r, -40, y, w + 40, y + r.uniform(-20, 20), 10, 8 + k * 2, 0.4)
        L.add(f'<path d="{suave(pts, cerrado=False)}" stroke="#7fa4c8" stroke-width="{2 + k * 0.6:.1f}" opacity="0.25" fill="none"/>'
              f'<path d="{suave([(a, b - 3 - k * 0.4) for a, b in pts], cerrado=False)}" stroke="#ffffff" stroke-width="{1.5 + k * 0.4:.1f}" opacity="0.35" fill="none"/>')
    L.add(L.relieve(sem + 3, freq="0.008 0.012", escala=4, az=270, elev=55, op=0.3, oct=3, modo="soft-light"))
    L.add(L.oscuridad(cx, yf - (100 if V else 60), w * (0.75 if V else 0.6), h * (0.55 if V else 0.8), color="#050c18", op=0.85, medio=0.3))
    L.add(L.polvo(80, 0, 0, w, h, "#ffffff", 2.2, 0.6, sem=sem + 7))   # cristalitos de hielo en el aire
    return {"suelo": yf + (220 if V else 160), "nota": "suelo de nieve despejado en el centro"}


def _pico(L, xp, yp, xb0, xb1, yb, r, cols, luz=-1, nieve_hasta=0.55, amp=30, rocas=14):
    """Montaña: cara iluminada (lado luz) y cara en sombra separadas por una arista; afloramientos de roca oscuros
    sobre las pendientes (con su lado claro) y canales de nieve; la base se funde en la bruma."""
    c_luz, c_sombra, c_roca, c_nieve_s = cols
    izq = linea_ruido(r, xb0, yb, xp, yp, 9, amp, 1.0)
    der = linea_ruido(r, xp, yp, xb1, yb, 9, amp, 1.0)
    d = suave(izq + der[1:], t=0.15) + " Z"
    arista = [(xp, yp)]
    for k in range(1, 8):
        t = k / 7
        arista.append((xp - luz * (xb1 - xb0) * 0.12 * t + r.uniform(-14, 14) * (1 + t), yp + (yb - yp) * t))
    out = [f'<path d="{d}" fill="{L.lg((0, c_sombra), (1, mezcla(c_sombra, "#ffffff", 0.25)))}"/>']
    cara = (izq + arista[::-1][1:]) if luz < 0 else (arista + der[1:])
    out.append(f'<path d="{suave(cara, t=0.15)}" fill="{L.lg((0, c_luz), (1, mezcla(c_luz, c_sombra, 0.35)))}"/>')
    cl = L.clip(d)
    out.append(f'<g clip-path="{cl}">')
    # afloramientos: vetas de roca que bajan por la línea de máxima pendiente (radiales desde la cima)
    for _ in range(rocas):
        t = r.uniform(0.1, 0.9)
        yy = yp + (yb - yp) * t
        half = (xb1 - xb0) / 2 * t
        x0 = xp + r.uniform(-half, half) * 0.9
        ang = math.atan2(yy - yp, x0 - xp)
        lado_luz = (x0 < xp) == (luz < 0)
        ln = r.uniform(40, 160) * ((yb - yp) / 600)
        pts = [(x0, yy)]
        for k in range(4):
            pts.append((pts[-1][0] + math.cos(ang) * ln / 4 + r.uniform(-4, 4), pts[-1][1] + math.sin(ang) * ln / 4))
        dd = suave(pts, cerrado=False)
        col = mezcla(c_roca, c_luz, 0.2) if lado_luz else c_roca
        ww = r.uniform(3, 11) * ((yb - yp) / 600)
        out.append(f'<path d="{dd}" stroke="{col}" stroke-width="{ww:.1f}" opacity="{r.uniform(0.45, 0.8):.2f}" fill="none" stroke-linecap="round"/>')
        if lado_luz:
            out.append(f'<path d="{dd}" transform="translate({-ww * 0.4:.1f} 0)" stroke="#ffffff" stroke-width="{ww * 0.3:.1f}" opacity="0.5" fill="none" stroke-linecap="round"/>')
    out.append("</g>")
    out.append(f'<path d="{suave(izq if luz < 0 else der, cerrado=False, t=0.15)}" stroke="#ffffff" stroke-width="1.5" opacity="0.35" fill="none"/>')
    return "".join(out)


def bg_alpes_nieve(L, sem=81):
    """Alpes nevados con un collado, cielo frío, luz de mañana; campo de nieve llano delante (para la tienda)."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    yh = 1000 if V else 560
    ysuelo = 1340 if V else 820
    L.add(L.rect(L.lg((0, "#3a78b8"), (0.45, "#6fa8d8"), (0.8, "#bfe0f6"), (1, "#fde8d0")), h=yh + 100))
    L.add(L.luz(-w * 0.1, -h * 0.05, w * 0.9, h * 0.5, "#fff2d8", 0.45))
    for k in range(2 if V else 4):
        nx, ny = r.uniform(0, w), r.uniform(150, 520 if V else 260)
        L.add(f'<ellipse cx="{nx:.0f}" cy="{ny:.0f}" rx="{r.uniform(160, 300):.0f}" ry="{r.uniform(8, 16):.0f}" fill="#ffffff" opacity="0.45" filter="url(#blur8)"/>')
    # cordillera lejana (pálida, azulada)
    for k in range(int(w / 220) + 2):
        xp = -100 + k * 220 + r.uniform(-50, 50)
        L.add(_pico(L, xp, yh - r.uniform(200, 340) * (1 if V else 0.65), xp - 300, xp + 300, yh, r,
                    ("#eef4fb", "#b4cce2", "#8aa6c4", "#d0e2f2"), luz=-1, nieve_hasta=0.75, amp=14, rocas=6))
    L.add(L.bruma(yh - 40, 200, "#e8f6ff", 0.55))
    # picos principales con un collado en el centro
    picos = [(w * 0.1, yh - (640 if V else 400), -w * (0.7 if V else 0.3), w * (0.62 if V else 0.5)),
             (w * 0.9, yh - (580 if V else 380), w * (0.38 if V else 0.5), w * (1.7 if V else 1.3))]
    if not V:
        picos += [(w * 0.5, yh - 230, w * 0.3, w * 0.7)]
    for xp, yp, x0, x1 in picos:
        L.add(_pico(L, xp, yp, x0, x1, yh + 60, r, ("#fbf4ea", "#7aa4cc", "#2e4a66", "#c8dcee"), luz=-1, nieve_hasta=0.6, amp=30, rocas=40))
    L.add(L.bruma(yh + 30, 160, "#e8f6ff", 0.5))
    # campo de nieve: ondas suaves, sastrugi, rocas con capuchón de nieve; llano en el centro
    sn = linea_ruido(r, -40, yh + 40, w + 40, yh + 60, 12, 26, 0.5)
    ds = suave(sn, cerrado=False) + f" L{w + 40} {h + 40} L-40 {h + 40} Z"
    L.add(f'<path d="{ds}" fill="{L.lg((0, "#f4f9ff"), (0.4, "#e4f0fb"), (1, "#a9c8e4"))}"/>')
    for k in range(14):
        y = yh + 60 + (h - yh) * ((k + 0.5) / 14) ** 1.3
        pts = linea_ruido(r, -40, y, w + 40, y + r.uniform(-30, 30), 10, 10 + k * 3, 0.5)
        L.add(f'<path d="{suave(pts, cerrado=False)}" stroke="#8fb4d8" stroke-width="{2 + k:.0f}" opacity="0.22" fill="none" filter="url(#blur8)"/>'
              f'<path d="{suave([(a, b - 4 - k * 0.6) for a, b in pts], cerrado=False)}" stroke="#ffffff" stroke-width="{1.5 + k * 0.4:.1f}" opacity="0.5" fill="none"/>')
    for k in range(5 if V else 7):   # ventisqueros: lomas suaves de nieve con su sombra azul
        x, y = r.uniform(0, w), yh + 60 + (h - yh) * r.uniform(0.05, 0.9)
        rx, ry = r.uniform(200, 500), r.uniform(30, 80) * (1 + (y - yh) / (h - yh))
        L.add(f'<ellipse cx="{x:.0f}" cy="{y + ry * 0.4:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="#9cbedc" opacity="0.35" filter="url(#blur20)"/>'
              f'<ellipse cx="{x - rx * 0.1:.0f}" cy="{y:.0f}" rx="{rx * 0.8:.0f}" ry="{ry * 0.6:.0f}" fill="#ffffff" opacity="0.45" filter="url(#blur20)"/>')
    for _ in range(9 if V else 14):
        x, y = r.uniform(0, w), r.uniform(yh + 80, h)
        if abs(x - w / 2) < w * 0.3 and abs(y - ysuelo) < (260 if V else 160):
            continue
        t = (y - yh) / (h - yh)
        an = (30 + r.uniform(0, 70)) * (0.5 + t * 2)
        L.add(L.pedrusco(x, y, an, an * 0.6, -1, ("#1a2a3c", "#3a4e64", "#8aa0b8"), r=r))
        L.add(f'<path d="M{x - an * 0.48:.0f} {y - an * 0.42:.0f} Q{x:.0f} {y - an * 0.78:.0f} {x + an * 0.46:.0f} {y - an * 0.38:.0f} Q{x:.0f} {y - an * 0.5:.0f} {x - an * 0.48:.0f} {y - an * 0.42:.0f} Z" fill="#f6fbff"/>')
    for _ in range(int(w / 5)):
        x, y = r.uniform(0, w), r.uniform(yh + 40, h)
        L.add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(0.6, 2):.1f}" fill="#ffffff" opacity="{r.uniform(0.5, 1):.2f}"/>')
    L.add(L.relieve(sem + 2, freq="0.006 0.02", escala=3, az=200, elev=60, op=0.35, oct=3, modo="soft-light", caja=(0, yh, w, h - yh)))
    L.add(L.brillo(w / 2, ysuelo, w * 0.5, 120, "#ffffff", 0.25))
    return {"suelo": ysuelo, "nota": "llano de nieve despejado en el centro (para la tienda)"}


def bg_cueva_francia(L, sem=91):
    """Gran sala tipo catedral (Deep Time, Francia 2021): altísima, columnas enormes, luces cálidas pequeñas a lo lejos."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    cx = w / 2
    yf = 1120 if V else 600
    ysuelo = 1330 if V else 830
    L.add(L.rect(L.lg((0, "#040508"), (0.6, "#0b0c12"), (1, "#14110f"))))
    # pared del fondo, muy lejana: apenas se intuye con bruma cálida en la base
    dfar = f"M-40 -40 L{w + 40} -40 L{w + 40} {yf + 30} L-40 {yf + 30} Z"
    L.add(L.roca(dfar, (-40, -40, w + 40, yf + 30), "#08080b", "#16141a", "#3a2c26", luz=(0.5, 1), sem=sem + 1, estratos=10, inclin=0.02,
                 vetas=10, humedad=8, brillos=0, contraste=0.6))
    # terrazas lejanas a distintas alturas con luces pequeñas
    luces = []
    for k in range(3):
        y0 = yf - (160 - k * 70) * (1 if V else 0.7)
        pts = linea_ruido(r, -40, y0, w + 40, y0 + r.uniform(-20, 20), 12, 16, 0.8)
        d = suave(pts, cerrado=False) + f" L{w + 40} {yf + 40} L-40 {yf + 40} Z"
        L.add(f'<path d="{d}" fill="{mezcla("#1a1614", "#3a2a20", k / 2)}" opacity="0.95"/>')
        L.add(f'<path d="{suave(pts, cerrado=False)}" stroke="#c08850" stroke-width="2" opacity="{0.25 + k * 0.15:.2f}" fill="none"/>')
        for j in range(3 + k):
            x = r.uniform(w * 0.05, w * 0.95)
            luces.append((x, y0 + 6, 0.5 + k * 0.25))
    # columnas gigantes (reloj de arena: estalactita y estalagmita unidas), las lejanas más claras y difusas
    def columna(x, ybase, wb, c1, c2, c3, lado, rr):
        pts_i, pts_d = [], []
        for k in range(13):
            t = k / 12                                   # 0 arriba, 1 abajo
            ancho = wb / 2 * (0.32 + 0.9 * (abs(t - 0.55) / 0.55) ** 2.2) * (1 + rr.uniform(-0.08, 0.08))
            y = -60 + (ybase + 60) * t
            pts_i.append((x - ancho, y))
            pts_d.append((x + ancho, y))
        d = suave(pts_i + list(reversed(pts_d)), t=0.4)
        g = L._grad_cono(c1, c2, c3, lado)
        out = [f'<path d="{d}" fill="{g}"/>']
        cl = L.clip(d)
        pl = "".join(f'<path d="M{x + rr.uniform(-0.4, 0.4) * wb:.0f} -60 C{x + rr.uniform(-0.3, 0.3) * wb:.0f} {ybase * 0.4:.0f} {x + rr.uniform(-0.15, 0.15) * wb:.0f} {ybase * 0.6:.0f} {x + rr.uniform(-0.5, 0.5) * wb:.0f} {ybase:.0f}" '
                     f'stroke="{rr.choice([c1, c3])}" stroke-width="{rr.uniform(2, 7):.0f}" opacity="0.3" fill="none"/>' for _ in range(9))
        out.append(f'<g clip-path="{cl}">{pl}</g>')
        out.append(f'<ellipse cx="{x:.0f}" cy="{ybase + 4:.0f}" rx="{wb * 0.7:.0f}" ry="{wb * 0.08:.0f}" fill="#000" opacity="0.5"/>')
        return "".join(out)
    cols_x = [(w * 0.3, 0), (w * 0.72, 0), (w * 0.08, 1), (w * 0.93, 1)] if V else [(w * 0.22, 0), (w * 0.47, 0), (w * 0.8, 0), (w * 0.06, 1), (w * 0.95, 1)]
    for x, cerca in cols_x:
        wb = (230 if cerca else 110) * (1 if V else 0.85)
        ybase = yf + (110 if cerca else 15)
        if cerca:
            L.add(columna(x, ybase, wb, "#050405", "#1a1412", "#7a5a40", 1 if x < cx else -1, r))
        else:
            L.add(columna(x, ybase, wb, "#141216", "#2e2622", "#6a5244", 1 if x < cx else -1, r))
            L.add(f'<rect x="{x - wb:.0f}" y="0" width="{wb * 2:.0f}" height="{ybase + 20:.0f}" fill="{L.lg((0, "#0b0c12", 0.35), (1, "#5a4030", 0.25))}"/>')
    # techo altísimo con estalactitas pequeñas (la distancia)
    gm = (L._grad_cono("#060507", "#1a1614", "#4a3a2e", -1), L._grad_cono("#060507", "#1a1614", "#4a3a2e", 1))
    sv = L.lg((0, "#050506", 0.95), (0.6, "#050506", 0.5), (1, "#050506", 0))
    pt = linea_ruido(r, -40, 60 if V else 30, w + 40, 80 if V else 40, 16, 30, 0.8)
    L.add(_techo_estalactitas(L, _ytec_fn(pt), 0, w, int(w / 30), 20, 90, 6, 16, gm, cx, sem + 3, sombra_v=sv))
    L.add(L.bruma(yf - 40, 300 if V else 200, "#8a6040", 0.35))
    # suelo amplio con su textura
    desp = (w * 0.1, w * 0.9, yf + 20, h)
    suelo, dsuelo = _suelo_cueva(L, yf, h, 0, w, ("#1a1512", "#4a3628"), (cx, ysuelo), sem + 4, desp, n_piedras=int(w / 30), charcos=4,
                                 brillo=CALIDA[0], c_luz=ROCA[3])
    L.add(suelo)
    # luces cálidas repartidas: puntos con halo y charco de luz en el suelo; dos más cerca en el suelo
    luces += [(w * 0.18, yf + (90 if V else 50), 1.3), (w * 0.84, yf + (130 if V else 70), 1.5)]
    for x, y, s_ in luces:
        L.add(L.luz(x, y, 110 * s_, 50 * s_, "#ff9a3a", 0.55), L.luz(x, y - 40 * s_, 40 * s_, 140 * s_, "#ffb15e", 0.22),
              L.brillo(x, y - 4 * s_, 14 * s_, 14 * s_, "#ffe0a0", 0.9),
              f'<circle cx="{x:.0f}" cy="{y - 4 * s_:.0f}" r="{2.2 * s_:.1f}" fill="#fff6dc"/>')
    L.add(L.relieve(sem + 6, freq="0.011 0.02", escala=5, az=90, elev=45, op=0.3, oct=3))
    # bloques oscuros de primer término en las esquinas
    rf = random.Random(sem + 9)
    for lado, x0 in ((1, -w * 0.03), (-1, w * 1.03)):
        for k in range(2):
            an = (w * (0.36 if V else 0.18)) * rf.uniform(0.8, 1.1) * (1 - k * 0.3)
            L.add(L.pedrusco(x0 + lado * k * an * 0.5, h + 30 - k * 50, an, an * 0.6, lado, ("#020203", "#0a0809", "#2a1d16"), r=rf, borde=CALIDA[1]))
    L.add(L.oscuridad(cx, yf + 60, w * (0.8 if V else 0.65), h * (0.5 if V else 0.75), op=0.95, medio=0.5))
    L.add(L.rect(L.lg((0, "#020204", 0.75), (0.45, "#020204", 0.2), (1, "#020204", 0)), h=yf))
    L.add(L.polvo(90, 0, yf - 600, w, yf + 200, "#ffd9a0", 1.6, 0.4, sem=sem + 7))
    return {"suelo": ysuelo, "nota": "suelo amplio en todo el ancho (grupo de personas)"}


def _edificios(L, r, y_base, n_min, n_max, alto_min, alto_max, col, ven_on, ven_off, prob, escala, x0=-40, x1=None, top_luz=None):
    x1 = L.w + 40 if x1 is None else x1
    out = []
    x = x0
    while x < x1:
        bw = r.uniform(n_min, n_max) * escala
        bh = r.uniform(alto_min, alto_max)
        yt = y_base - bh
        out.append(f'<rect x="{x:.0f}" y="{yt:.0f}" width="{bw + 1:.0f}" height="{bh + 300:.0f}" fill="{col}"/>')
        if r.random() < 0.3:   # remate / antena
            out.append(f'<rect x="{x + bw * 0.3:.0f}" y="{yt - 20 * escala:.0f}" width="{bw * 0.3:.0f}" height="{20 * escala:.0f}" fill="{col}"/>')
        if top_luz:
            out.append(f'<rect x="{x:.0f}" y="{yt:.0f}" width="{bw:.0f}" height="2" fill="{top_luz}" opacity="0.5"/>')
        cw, ch = 7 * escala, 10 * escala
        gx, gy = 13 * escala, 18 * escala
        cols_ = max(1, int((bw - 8 * escala) / gx))
        fil = max(1, int((bh - 16 * escala) / gy))
        pon = r.random() * 0.4 + prob
        for i in range(cols_):
            for j in range(min(fil, 60)):
                if r.random() < pon:
                    c = r.choice(ven_on)
                    out.append(f'<rect x="{x + 5 * escala + i * gx:.0f}" y="{yt + 10 * escala + j * gy:.0f}" width="{cw:.1f}" height="{ch:.1f}" fill="{c}" opacity="{r.uniform(0.6, 1):.2f}"/>')
                elif r.random() < 0.5:
                    out.append(f'<rect x="{x + 5 * escala + i * gx:.0f}" y="{yt + 10 * escala + j * gy:.0f}" width="{cw:.1f}" height="{ch:.1f}" fill="{ven_off}" opacity="0.6"/>')
        x += bw + r.uniform(0, 10) * escala
    return "".join(out)


def bg_ciudad(L, sem=101):
    """Ciudad moderna genérica al anochecer: ventanas encendidas, tráfico difuminado, vida."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    yr = 1180 if V else 650        # calzada (al fondo)
    ya = 1330 if V else 790        # acera donde se posan los personajes
    L.add(L.rect(L.lg((0, "#141a3e"), (0.4, "#3a3270"), (0.7, "#a0507a"), (0.88, "#f08a5a"), (1, "#ffc080"))))
    L.add(L.polvo(60, 0, 0, w, h * 0.25, "#ffffff", 1.4, 0.6, sem=sem))
    L.add(L.brillo(w * 0.6, yr - (420 if V else 260), w * 0.8, 200, "#ffb070", 0.35))
    L.add(_edificios(L, r, yr - (180 if V else 110), 50, 120, 300, 640 if V else 420, "#3a3a6a", ["#ffd9a0", "#bfe0ff"], "#2a2a50", 0.08, 1.0, top_luz="#ffb080"))
    L.add(L.bruma(yr - (200 if V else 120), 160, "#c87a8a", 0.35))
    L.add(_edificios(L, r, yr - (60 if V else 40), 90, 200, 260, 760 if V else 480, "#1f1f3c", ["#ffd38a", "#ffe8b0", "#9fd4ff", "#ffb060"], "#18182e", 0.18, 1.5, top_luz="#ff9a70"))
    L.add(L.bruma(yr - 40, 120, "#f0906a", 0.25))
    L.add(_edificios(L, r, yr + 10, 160, 320, 300, 1000 if V else 560, "#0e0e1c", ["#ffd38a", "#ffcf8a", "#bfe8ff"], "#0a0a14", 0.22, 2.3))
    # calzada con estelas de luz (faros blancos y pilotos rojos), y farolas
    L.add(f'<rect x="0" y="{yr:.0f}" width="{w}" height="{ya - yr + 10:.0f}" fill="{L.lg((0, "#1a1a28"), (1, "#0c0c14"))}"/>')
    est = []
    for k in range(26):
        y = yr + r.uniform(10, ya - yr - 10)
        x = r.uniform(-200, w)
        L_ = r.uniform(150, 600)
        c = r.choice(["#ff3a3a", "#ff5a3a", "#fff4d8", "#ffe0a0"])
        est.append(f'<path d="M{x:.0f} {y:.0f} L{x + L_:.0f} {y + r.uniform(-3, 3):.0f}" stroke="{c}" stroke-width="{r.uniform(2, 6):.1f}" opacity="{r.uniform(0.5, 0.95):.2f}" stroke-linecap="round"/>')
    L.add('<g filter="url(#blur8)">' + "".join(est) + "</g>", "".join(est[:12]))
    for k in range(int(w / 260) + 1):
        x = k * 260 + 80
        L.add(f'<rect x="{x - 3}" y="{ya - (300 if V else 200)}" width="6" height="{300 if V else 200}" fill="#08080e"/>'
              f'<path d="M{x} {ya - (300 if V else 200)} q30 -10 50 6" stroke="#08080e" stroke-width="5" fill="none"/>',
              L.luz(x + 50, ya - (290 if V else 192), 130, 130, "#ffc070", 0.6),
              f'<circle cx="{x + 50}" cy="{ya - (290 if V else 192) + 4}" r="5" fill="#fff4d0"/>')
    # acera: baldosas con reflejos de las luces
    L.add(f'<rect x="0" y="{ya:.0f}" width="{w}" height="{h - ya + 10:.0f}" fill="{L.lg((0, "#3a3048"), (1, "#141018"))}"/>')
    L.add(f'<rect x="0" y="{ya - 4:.0f}" width="{w}" height="8" fill="#6a5a70"/>')
    for k in range(12):
        y = ya + (h - ya) * ((k + 1) / 12) ** 1.4
        L.add(f'<path d="M0 {y:.0f} L{w} {y:.0f}" stroke="#0a0810" stroke-width="{1 + k * 0.3:.1f}" opacity="0.5"/>')
    for k in range(-6, 7):
        L.add(f'<path d="M{w / 2 + k * 60:.0f} {ya:.0f} L{w / 2 + k * 260:.0f} {h:.0f}" stroke="#0a0810" stroke-width="1.5" opacity="0.4"/>')
    for k in range(int(w / 260) + 1):
        L.add(L.luz(k * 260 + 130, ya + (h - ya) * 0.3, 140, 60, "#ffb060", 0.3))
    # bokeh: círculos de luz desenfocados
    bok = "".join(f'<circle cx="{r.uniform(0, w):.0f}" cy="{r.uniform(yr - 500, ya):.0f}" r="{r.uniform(10, 34):.0f}" fill="{r.choice(["#ffd08a", "#ff9a6a", "#9fd4ff", "#ffe8c0"])}" opacity="{r.uniform(0.15, 0.4):.2f}"/>' for _ in range(28))
    L.add(f'<g filter="url(#blur8)">{bok}</g>')
    L.add(L.oscuridad(w / 2, ya - 200, w * 0.95, h * 0.7, color="#0a0618", op=0.6, medio=0.15))
    return {"suelo": ya + (60 if V else 40), "nota": "acera delante; calzada con estelas detrás"}


def bg_estadio_noche(L, sem=111):
    """Estadio genérico de noche: focos, gradas llenas (puntos), césped con franjas. Sin marcas ni texto."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    cx = w / 2
    yc = 1120 if V else 560      # línea de fondo del campo (lejos)
    yn = h + 300                 # borde cercano (fuera de cuadro)
    L.add(L.rect(L.lg((0, "#03050e"), (0.5, "#0a1230"), (1, "#16224a"))))
    L.add(L.polvo(80, 0, 0, w, yc - 500, "#ffffff", 1.3, 0.6, sem=sem))
    # público: patrón de puntos de colores (barato y denso)
    pid = L.id("pub")
    dots = "".join(f'<circle cx="{r.uniform(0, 48):.1f}" cy="{r.uniform(0, 30):.1f}" r="{r.uniform(1.2, 2.4):.1f}" fill="{r.choice(["#e8e0d0", "#c84040", "#3a6ac8", "#f0c040", "#2a2a2a", "#d8d8e8", "#8a4a2a", "#ffffff", "#40a060"])}"/>' for _ in range(42))
    L.defs.append(f'<pattern id="{pid}" width="48" height="30" patternUnits="userSpaceOnUse"><rect width="48" height="30" fill="#1a1a26"/>{dots}</pattern>')
    pid2 = L.id("pub")
    dots2 = "".join(f'<circle cx="{r.uniform(0, 30):.1f}" cy="{r.uniform(0, 18):.1f}" r="{r.uniform(0.8, 1.5):.1f}" fill="{r.choice(["#c8c0b0", "#a83838", "#3a5aa8", "#d0a838", "#2a2a2a", "#ffffff"])}"/>' for _ in range(36))
    L.defs.append(f'<pattern id="{pid2}" width="30" height="18" patternUnits="userSpaceOnUse"><rect width="30" height="18" fill="#141420"/>{dots2}</pattern>')
    # gradas del fondo (anillos de elipse) y del lateral, con pasillos
    ytop = yc - (560 if V else 380)
    for k, (y0, y1, pat) in enumerate([(ytop, ytop + (200 if V else 130), pid2), (ytop + (215 if V else 140), yc - 10, pid)]):
        d = f"M-60 {y1 + 40:.0f} Q{cx:.0f} {y1 - 30:.0f} {w + 60} {y1 + 40:.0f} L{w + 60} {y0 + 30:.0f} Q{cx:.0f} {y0 - 40:.0f} -60 {y0 + 30:.0f} Z"
        L.add(f'<path d="{d}" fill="url(#{pat})"/>')
        L.add(f'<path d="{d}" fill="{L.lg((0, "#000000", 0.55), (1, "#000000", 0.0))}"/>')
        for j in range(1, 9):   # pasillos y filas
            xx = j * w / 9
            L.add(f'<path d="M{xx:.0f} {y0:.0f} L{cx + (xx - cx) * 1.15:.0f} {y1 + 30:.0f}" stroke="#0a0a12" stroke-width="5" opacity="0.7"/>')
        L.add(f'<path d="M-60 {y0 + 30:.0f} Q{cx:.0f} {y0 - 40:.0f} {w + 60} {y0 + 30:.0f}" stroke="#2a2a3a" stroke-width="10" fill="none"/>')
    # techo con baterías de focos
    yroof = ytop - (90 if V else 60)
    L.add(f'<path d="M-60 {yroof + 40:.0f} Q{cx:.0f} {yroof - 30:.0f} {w + 60} {yroof + 40:.0f} L{w + 60} {ytop + 20:.0f} Q{cx:.0f} {ytop - 50:.0f} -60 {ytop + 20:.0f} Z" fill="#0b0d18"/>')
    for k in range(5 if V else 8):
        fx = (k + 0.5) / (5 if V else 8) * w
        fy = yroof + 18 - 40 * math.sin(math.pi * (k + 0.5) / (5 if V else 8)) * 0.8
        for i in range(6):
            L.add(f'<rect x="{fx - 36 + i * 12:.0f}" y="{fy - 8:.0f}" width="9" height="12" rx="2" fill="#fffbe8"/>')
        L.add(L.luz(fx, fy, 260, 160, "#e8f0ff", 0.55), L.luz(fx, fy, 60, 40, "#ffffff", 0.9))
        # haces que bajan al campo
        L.add(f'<path d="M{fx - 30:.0f} {fy:.0f} L{fx + 30:.0f} {fy:.0f} L{cx + (fx - cx) * 0.3 + 220:.0f} {yc + 400:.0f} L{cx + (fx - cx) * 0.3 - 220:.0f} {yc + 400:.0f} Z" '
              f'fill="{L.lg((0, "#e8f0ff", 0.16), (1, "#e8f0ff", 0))}" style="mix-blend-mode:screen"/>')
    # campo: franjas de corte en perspectiva y líneas
    dcampo = f"M-400 {yn} L{w + 400} {yn} L{w + 120} {yc} L-120 {yc} Z"
    L.add(f'<path d="{dcampo}" fill="{L.lg((0, "#1f6a2a"), (1, "#2f8a38"))}"/>')
    cl = L.clip(dcampo)
    franjas = []
    for k in range(14):
        za, zb = k / 14, (k + 0.5) / 14
        ya_, yb_ = yc + (yn - yc) * za ** 1.6, yc + (yn - yc) * zb ** 1.6
        franjas.append(f'<rect x="-400" y="{ya_:.0f}" width="{w + 800}" height="{yb_ - ya_:.0f}" fill="#000" opacity="0.12"/>')
    L.add(f'<g clip-path="{cl}">' + "".join(franjas) + "</g>")
    yl = yc + 30
    L.add(f'<path d="M-100 {yl} L{w + 100} {yl}" stroke="#e8f0e8" stroke-width="3" opacity="0.8"/>')
    ya_ = yc + (yn - yc) * 0.18
    L.add(f'<path d="M{cx - w * 0.28:.0f} {yl} L{cx - w * 0.33:.0f} {ya_:.0f} L{cx + w * 0.33:.0f} {ya_:.0f} L{cx + w * 0.28:.0f} {yl}" stroke="#e8f0e8" stroke-width="3.5" opacity="0.75" fill="none"/>')
    L.add(f'<ellipse cx="{cx:.0f}" cy="{yc + (yn - yc) * 0.5:.0f}" rx="{w * 0.32:.0f}" ry="{(yn - yc) * 0.09:.0f}" stroke="#e8f0e8" stroke-width="5" opacity="0.6" fill="none"/>')
    L.add(f'<path d="M-100 {yc + (yn - yc) * 0.5:.0f} L{w + 100} {yc + (yn - yc) * 0.5:.0f}" stroke="#e8f0e8" stroke-width="5" opacity="0.6"/>')
    L.add(L.luz(cx, yc + 200, w * 0.7, 300, "#dff0ff", 0.2))
    L.add(L.bruma(yc - 40, 200, "#a8b8d8", 0.25))
    L.add(L.oscuridad(cx, yc, w * 1.0, h * 0.8, color="#02030a", op=0.6, medio=0.1))
    return {"suelo": round(yc + (yn - yc) * 0.25), "nota": "césped en la mitad baja; gradas y focos arriba"}


def bg_playa_verano(L, sem=121):
    """Playa de verano de la infancia: sol alto, mar con destellos, arena dorada, sombrilla lejana, día eterno."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    yhz = 860 if V else 420       # horizonte
    yor = 1130 if V else 640      # orilla
    ysuelo = 1350 if V else 840
    sx, sy = w * 0.62, (300 if V else 110)
    L.add(L.rect(L.lg((0, "#2a86d8"), (0.55, "#6cc0f0"), (1, "#e8f6ff")), h=yhz + 10))
    L.add(L.luz(sx, sy, w * 0.9, 700 if V else 450, "#fff4c8", 0.6), L.brillo(sx, sy, 200, 200, "#ffffff", 0.9),
          f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="58" fill="#fffef4"/>')
    for k in range(12):
        a_ = k * math.pi / 6 + 0.2
        L.add(f'<path d="M{sx + math.cos(a_) * 80:.0f} {sy + math.sin(a_) * 80:.0f} L{sx + math.cos(a_) * 420:.0f} {sy + math.sin(a_) * 420:.0f}" stroke="#fffbe0" stroke-width="{r.uniform(10, 30):.0f}" opacity="0.08" stroke-linecap="round"/>')
    for k in range(2 if V else 4):
        L.add(_nube(L, r.uniform(0, w), r.uniform(yhz - 260, yhz - 120), r.uniform(0.4, 0.7), r, "#ffffff", "#d8ecf8", 0.75))
    # mar: de azul profundo en el horizonte a turquesa en la orilla, con camino de destellos del sol
    dmar = f"M0 {yhz} L{w} {yhz} L{w} {yor + 40} L0 {yor + 40} Z"
    L.add(f'<path d="{dmar}" fill="{L.lg((0, "#1a5a9a"), (0.45, "#2a8ac0"), (0.85, "#3ac0c8"), (1, "#7ae0d0"))}"/>')
    L.add(f'<path d="M0 {yhz} L{w} {yhz}" stroke="#e8f6ff" stroke-width="2" opacity="0.6"/>')
    for k in range(int(w / 3)):
        t = r.random() ** 1.5
        y = yhz + 4 + (yor - yhz) * t
        x = sx + r.gauss(0, 30 + 160 * t)
        L.add(f'<path d="M{x:.0f} {y:.0f} l{r.uniform(4, 18) * (0.3 + t):.1f} 0" stroke="#ffffff" stroke-width="{1 + t * 2:.1f}" opacity="{r.uniform(0.4, 1):.2f}"/>')
    for k in range(int(w / 6)):
        y = yhz + 6 + (yor - yhz) * r.random() ** 1.2
        x = r.uniform(0, w)
        L.add(f'<path d="M{x:.0f} {y:.0f} q{6:.0f} -3 {12 + (y - yhz) / 20:.0f} 0" stroke="#bfe8f0" stroke-width="1.2" opacity="0.45" fill="none"/>')
    # espuma de las olas en la orilla
    for k in range(3):
        y = yor - 50 + k * 30
        pts = linea_ruido(r, -40, y, w + 40, y + 10, 14, 10, 0.8)
        L.add(f'<path d="{suave(pts, cerrado=False)}" stroke="#ffffff" stroke-width="{4 + k * 2}" opacity="{0.5 + k * 0.15:.2f}" fill="none"/>')
    # arena mojada y seca, ondulitas, conchitas
    pts = linea_ruido(r, -40, yor + 10, w + 40, yor + 20, 14, 8, 0.8)
    dar = suave(pts, cerrado=False) + f" L{w + 40} {h + 40} L-40 {h + 40} Z"
    L.add(f'<path d="{dar}" fill="{L.lg((0, "#c8a46a"), (0.12, "#ecd29a"), (0.5, "#f2dca8"), (1, "#d8b47a"))}"/>')
    L.add(f'<path d="{suave(pts, cerrado=False)}" stroke="#a8844a" stroke-width="6" opacity="0.35" fill="none"/>')
    for k in range(40):
        y = yor + 40 + (h - yor) * r.random() ** 0.8
        x = r.uniform(-50, w)
        ln = r.uniform(60, 220) * (1 + (y - yor) / (h - yor))
        L.add(f'<path d="M{x:.0f} {y:.0f} q{ln / 2:.0f} {-6:.0f} {ln:.0f} 0" stroke="#b89058" stroke-width="2" opacity="0.3" fill="none"/>'
              f'<path d="M{x:.0f} {y - 2:.0f} q{ln / 2:.0f} {-6:.0f} {ln:.0f} 0" stroke="#fff4d8" stroke-width="1.5" opacity="0.4" fill="none"/>')
    for k in range(30):
        x, y = r.uniform(0, w), r.uniform(yor + 60, h)
        L.add(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(2, 5):.1f}" ry="{r.uniform(1.5, 3):.1f}" fill="{r.choice(["#fff8ec", "#f0c8b0", "#e8d8c8"])}" opacity="0.85"/>')
    # sombrilla lejana (rayada) con su sombra
    ux, uy = w * (0.8 if V else 0.82), yor + (70 if V else 50)
    s_ = 0.9 if V else 0.8
    L.add(f'<ellipse cx="{ux + 14 * s_:.0f}" cy="{uy + 4:.0f}" rx="{46 * s_:.0f}" ry="{8 * s_:.0f}" fill="#a07848" opacity="0.5"/>'
          f'<path d="M{ux:.0f} {uy:.0f} L{ux - 6 * s_:.0f} {uy - 90 * s_:.0f}" stroke="#f4f0e8" stroke-width="{3 * s_:.1f}"/>')
    cu = (ux - 6 * s_, uy - 90 * s_)
    for i in range(6):
        a0, a1 = math.pi + i * math.pi / 6, math.pi + (i + 1) * math.pi / 6
        L.add(f'<path d="M{cu[0]:.0f} {cu[1] - 14 * s_:.0f} L{cu[0] + math.cos(a0) * 60 * s_:.0f} {cu[1] + 10 * s_ + math.sin(a0) * 6:.0f} '
              f'Q{cu[0] + math.cos((a0 + a1) / 2) * 62 * s_:.0f} {cu[1] + 2 * s_:.0f} {cu[0] + math.cos(a1) * 60 * s_:.0f} {cu[1] + 10 * s_ + math.sin(a1) * 6:.0f} Z" '
              f'fill="{["#e84a4a", "#fff8ee"][i % 2]}"/>')
    L.add(L.relieve(sem + 2, freq="0.02 0.06", escala=2, az=200, elev=55, op=0.25, oct=3, modo="soft-light", caja=(0, yor, w, h - yor)))
    L.add(L.luz(sx, yor, w * 1.2, (h - yor) * 1.2, "#ffd890", 0.25))
    L.add(L.rect(L.lg((0, "#fff0c8", 0.12), (1, "#ffcf8a", 0.12))))
    return {"suelo": ysuelo, "nota": "arena seca y llana en primer término"}


def bg_oficina_gris(L, sem=131):
    """Oficina de adulto: grises, fluorescentes fríos, ventana con día nublado al fondo."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    cx = w / 2
    vy = 860 if V else 470              # punto de fuga
    bx0, bx1 = w * (0.18 if V else 0.26), w * (0.82 if V else 0.74)    # pared del fondo
    by0, by1 = (520 if V else 150), (1180 if V else 700)
    # techo, paredes, suelo (perspectiva de un punto)
    L.add(f'<path d="M0 0 L{w} 0 L{bx1} {by0} L{bx0} {by0} Z" fill="{L.lg((0, "#8e949a"), (1, "#c8ccd0"))}"/>')
    L.add(f'<path d="M0 0 L{bx0} {by0} L{bx0} {by1} L0 {h} Z" fill="{L.lg((0, "#7a8088"), (1, "#a8aeb4"), x2=1, y2=0)}"/>')
    L.add(f'<path d="M{w} 0 L{bx1} {by0} L{bx1} {by1} L{w} {h} Z" fill="{L.lg((0, "#a0a6ac"), (1, "#6e747a"), x2=1, y2=0)}"/>')
    L.add(f'<path d="M0 {h} L{bx0} {by1} L{bx1} {by1} L{w} {h} Z" fill="{L.lg((0, "#7c8086"), (1, "#4e5258"))}"/>')
    L.add(f'<rect x="{bx0}" y="{by0}" width="{bx1 - bx0}" height="{by1 - by0}" fill="#b4b8bc"/>')
    # moqueta: líneas de losetas en perspectiva
    for k in range(1, 12):
        t = (k / 12) ** 1.8
        y = by1 + (h - by1) * t
        xl, xr = bx0 - bx0 * t, bx1 + (w - bx1) * t
        L.add(f'<path d="M{xl:.0f} {y:.0f} L{xr:.0f} {y:.0f}" stroke="#3a3e44" stroke-width="{1 + t * 2:.1f}" opacity="0.35"/>')
    for k in range(-8, 9):
        L.add(f'<path d="M{cx + k * (bx1 - bx0) / 8:.0f} {by1} L{cx + k * w / 4:.0f} {h}" stroke="#3a3e44" stroke-width="1.2" opacity="0.3"/>')
    # ventana grande en la pared del fondo con día nublado y edificios difusos
    wx0, wx1 = bx0 + (bx1 - bx0) * 0.12, bx1 - (bx1 - bx0) * 0.12
    wy0, wy1 = by0 + (by1 - by0) * 0.1, by0 + (by1 - by0) * 0.72
    L.add(f'<rect x="{wx0:.0f}" y="{wy0:.0f}" width="{wx1 - wx0:.0f}" height="{wy1 - wy0:.0f}" fill="{L.lg((0, "#c8ced4"), (1, "#e4e8ea"))}"/>')
    clw = L.clip(f"M{wx0} {wy0} L{wx1} {wy0} L{wx1} {wy1} L{wx0} {wy1} Z")
    nub = "".join(f'<ellipse cx="{r.uniform(wx0, wx1):.0f}" cy="{r.uniform(wy0, wy0 + (wy1 - wy0) * 0.6):.0f}" rx="{r.uniform(60, 160):.0f}" ry="{r.uniform(20, 40):.0f}" fill="{r.choice(["#b0b8c0", "#d8dce0", "#9aa2aa"])}" opacity="0.7"/>' for _ in range(16))
    edif = _edificios(L, r, wy1, 30, 70, 60, (wy1 - wy0) * 0.6, "#9aa0a8", ["#c8ccd0"], "#8a9098", 0.0, 0.6, x0=wx0, x1=wx1)
    L.add(f'<g clip-path="{clw}"><g filter="url(#blur8)">{nub}</g>{edif}<rect x="{wx0}" y="{wy0}" width="{wx1 - wx0}" height="{wy1 - wy0}" fill="#dde2e6" opacity="0.35"/></g>')
    # lamas de la persiana (medio bajada) y marco
    for k in range(14):
        y = wy0 + 4 + k * 9
        L.add(f'<rect x="{wx0:.0f}" y="{y:.0f}" width="{wx1 - wx0:.0f}" height="6" fill="#e8eaec"/><rect x="{wx0:.0f}" y="{y + 6:.0f}" width="{wx1 - wx0:.0f}" height="1.5" fill="#8a9096"/>')
    for x in (wx0, (wx0 + wx1) / 2, wx1):
        L.add(f'<rect x="{x - 5:.0f}" y="{wy0:.0f}" width="10" height="{wy1 - wy0:.0f}" fill="#6a7076"/>')
    L.add(f'<rect x="{wx0 - 8:.0f}" y="{wy0 - 8:.0f}" width="{wx1 - wx0 + 16:.0f}" height="10" fill="#5a6066"/><rect x="{wx0 - 12:.0f}" y="{wy1:.0f}" width="{wx1 - wx0 + 24:.0f}" height="14" fill="#7a8086"/>')
    # fluorescentes del techo (paneles en perspectiva con su resplandor frío)
    for k in range(4):
        t = (k + 0.7) / 4.5
        yy = by0 * (1 - t) ** 1.4 if by0 > 0 else 0
        y_ = by0 - (by0) * (1 - (k + 1) / 5) ** 1.2
        for xx in (-1, 1):
            xc = cx + xx * (bx1 - bx0) * 0.25 * (1 + (by0 - y_) / by0 * 1.6)
            ww = 80 * (1 + (by0 - y_) / by0 * 1.8)
            hh = 12 * (1 + (by0 - y_) / by0 * 2)
            L.add(f'<rect x="{xc - ww / 2:.0f}" y="{y_ - hh / 2:.0f}" width="{ww:.0f}" height="{hh:.0f}" fill="#f4fbff"/>',
                  L.luz(xc, y_, ww * 1.4, hh * 4, "#dff2ff", 0.6))
    # muebles de oficina (parte del decorado, no se mueven): archivadores a la izquierda, mesas con biombo a la derecha
    for k in range(3):
        x = bx0 * 0.15 + k * bx0 * 0.28
        top = by1 - (by1 - by0) * 0.4 + (bx0 - x) * 0.3
        bot = by1 + (h - by1) * (1 - x / bx0) * 0.55
        L.add(f'<path d="M{x:.0f} {top:.0f} L{x + bx0 * 0.26:.0f} {top + 20:.0f} L{x + bx0 * 0.26:.0f} {bot - 20:.0f} L{x:.0f} {bot:.0f} Z" fill="{L.lg((0, "#5a6068"), (1, "#7a8088"), x2=1, y2=0)}"/>')
        for j in range(4):
            yy = top + (bot - top) * (j + 0.5) / 4
            L.add(f'<path d="M{x + 6:.0f} {yy:.0f} L{x + bx0 * 0.24:.0f} {yy + 8:.0f}" stroke="#3a3e44" stroke-width="2"/><rect x="{x + bx0 * 0.1:.0f}" y="{yy + 10:.0f}" width="{bx0 * 0.06:.0f}" height="4" fill="#a8aeb4"/>')
    dx0 = bx1 + (w - bx1) * 0.08
    L.add(f'<path d="M{dx0:.0f} {by1 - 70:.0f} L{w + 10} {by1 - 160:.0f} L{w + 10} {by1 + 140:.0f} L{dx0:.0f} {by1 + 20:.0f} Z" fill="#5e646c"/>'
          f'<path d="M{dx0:.0f} {by1 - 70:.0f} L{w + 10} {by1 - 160:.0f}" stroke="#a8aeb4" stroke-width="4"/>')
    L.add(f'<path d="M{bx1 - 10:.0f} {by1 + 10:.0f} L{w + 10} {by1 + 60:.0f} L{w + 10} {by1 + 100:.0f} L{bx1 - 10:.0f} {by1 + 30:.0f} Z" fill="#8a9096"/>')
    L.add(L.relieve(sem + 1, freq="0.05 0.05", escala=1.5, az=270, elev=60, op=0.25, oct=2, modo="soft-light", caja=(0, by1, w, h - by1)))
    L.add(L.oscuridad(cx, (by0 + by1) / 2, w * 0.9, h * 0.75, color="#1a1e24", op=0.55, medio=0.15))
    L.add(L.rect("#c8d8e8", 0.08))
    return {"suelo": round(by1 + (h - by1) * 0.35), "nota": "moqueta despejada en el centro; ventana al fondo"}


def bg_ventana_invierno(L, sem=141):
    """Interior cálido junto a una ventana; fuera nieva de noche (diciembre)."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    wx0, wx1 = (w * 0.24, w * 0.76) if V else (w * 0.34, w * 0.72)
    wy0, wy1 = (440, 1120) if V else (110, 700)
    ysuelo = 1430 if V else 900
    # pared cálida iluminada por una lámpara fuera de cuadro (izquierda)
    L.add(L.rect(L.lg((0, "#6a3e26"), (0.5, "#4a2a1c"), (1, "#2a1810"), x2=1, y2=0.3)))
    pid = L.id("pap")
    L.defs.append(f'<pattern id="{pid}" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M30 8 l6 10 l-6 10 l-6 -10 Z" fill="#000" opacity="0.08"/>'
                  f'<path d="M0 38 l6 10 l-6 10 l-6 -10 Z M60 38 l6 10 l-6 10 l-6 -10 Z" fill="#000" opacity="0.08"/></pattern>')
    L.add(L.rect(f"url(#{pid})"))
    # fuera: noche nevada
    L.add(f'<rect x="{wx0:.0f}" y="{wy0:.0f}" width="{wx1 - wx0:.0f}" height="{wy1 - wy0:.0f}" fill="{L.lg((0, "#0a1430"), (0.7, "#1a2a50"), (1, "#2a3a60"))}"/>')
    clw = L.clip(f"M{wx0} {wy0} L{wx1} {wy0} L{wx1} {wy1} L{wx0} {wy1} Z")
    fuera = []
    yt = wy0 + (wy1 - wy0) * 0.62
    for k in range(6):   # tejados nevados con ventanas cálidas
        x0 = wx0 - 40 + k * (wx1 - wx0) / 4.5 + r.uniform(-20, 20)
        bw, bh = r.uniform(90, 160), r.uniform(80, 180)
        y0 = yt - bh * 0.4 + k % 2 * 30
        fuera.append(f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{bw:.0f}" height="{wy1 - y0:.0f}" fill="#141c34"/>'
                     f'<path d="M{x0 - 12:.0f} {y0 + 4:.0f} L{x0 + bw / 2:.0f} {y0 - 50:.0f} L{x0 + bw + 12:.0f} {y0 + 4:.0f} Z" fill="#1c2440"/>'
                     f'<path d="M{x0 - 14:.0f} {y0 + 2:.0f} L{x0 + bw / 2:.0f} {y0 - 52:.0f} L{x0 + bw + 14:.0f} {y0 + 2:.0f} L{x0 + bw + 6:.0f} {y0 - 6:.0f} L{x0 + bw / 2:.0f} {y0 - 40:.0f} L{x0 - 6:.0f} {y0 - 6:.0f} Z" fill="#e8f0ff"/>')
        for j in range(2):
            if r.random() < 0.7:
                vx_, vy_ = x0 + 20 + j * (bw - 50), y0 + 30
                fuera.append(f'<rect x="{vx_:.0f}" y="{vy_:.0f}" width="22" height="28" fill="#ffc870"/>')
                fuera.append(L.brillo(vx_ + 11, vy_ + 14, 40, 40, "#ffb050", 0.4))
    # abeto nevado
    tx = wx0 + (wx1 - wx0) * 0.78
    for k in range(6):
        yy = yt - 30 + k * 40
        ww = 30 + k * 22
        fuera.append(f'<path d="M{tx - ww:.0f} {yy + 50:.0f} L{tx:.0f} {yy - 20:.0f} L{tx + ww:.0f} {yy + 50:.0f} Z" fill="#0e2230"/>'
                     f'<path d="M{tx - ww * 0.8:.0f} {yy + 42:.0f} L{tx:.0f} {yy - 14:.0f} L{tx + ww * 0.5:.0f} {yy + 30:.0f}" stroke="#e8f0ff" stroke-width="5" fill="none" opacity="0.85"/>')
    fuera.append(f'<rect x="{wx0:.0f}" y="{wy1 - 60:.0f}" width="{wx1 - wx0:.0f}" height="60" fill="#d8e4f4"/>')
    # copos: lejanos pequeños, cercanos grandes y desenfocados
    fuera.append(L.polvo(260, wx0, wy0, wx1, wy1, "#ffffff", 2.2, 0.9, sem=sem + 1))
    grandes = "".join(f'<circle cx="{r.uniform(wx0, wx1):.0f}" cy="{r.uniform(wy0, wy1):.0f}" r="{r.uniform(4, 9):.1f}" fill="#ffffff" opacity="{r.uniform(0.4, 0.8):.2f}"/>' for _ in range(40))
    fuera.append(f'<g filter="url(#blur8)">{grandes}</g>')
    fuera.append(L.brillo((wx0 + wx1) / 2, wy0 + 40, (wx1 - wx0) * 0.6, 160, "#3a5a90", 0.4))
    L.add(f'<g clip-path="{clw}">' + "".join(fuera) + "</g>")
    # escarcha en las esquinas del cristal y nieve acumulada en el alféizar exterior
    for (fx, fy) in ((wx0, wy0), (wx1, wy0), (wx0, wy1), (wx1, wy1)):
        L.add(f'<g clip-path="{clw}">' + L.brillo(fx, fy, 90, 90, "#e8f4ff", 0.5) + "</g>")
    # marco de madera en cruz (con luz cálida en el canto izquierdo)
    mw = 26
    gm = L.lg((0, "#e8b07a"), (0.3, "#a86a3e"), (1, "#5a3420"), x2=1, y2=0)
    for x in (wx0 - mw, (wx0 + wx1) / 2 - mw / 2, wx1):
        L.add(f'<rect x="{x:.0f}" y="{wy0 - mw:.0f}" width="{mw}" height="{wy1 - wy0 + 2 * mw:.0f}" fill="{gm}"/>')
    for y in (wy0 - mw, (wy0 + wy1) / 2 - mw / 2):
        L.add(f'<rect x="{wx0 - mw:.0f}" y="{y:.0f}" width="{wx1 - wx0 + 2 * mw:.0f}" height="{mw}" fill="{L.lg((0, "#d09868"), (1, "#7a4a2a"))}"/>')
    # alféizar interior
    L.add(f'<path d="M{wx0 - 70:.0f} {wy1 + mw:.0f} L{wx1 + 70:.0f} {wy1 + mw:.0f} L{wx1 + 50:.0f} {wy1 + mw + 40:.0f} L{wx0 - 50:.0f} {wy1 + mw + 40:.0f} Z" fill="{L.lg((0, "#e0a874"), (1, "#7a4a2a"))}"/>'
          f'<rect x="{wx0 - 50:.0f}" y="{wy1 + mw + 40:.0f}" width="{wx1 - wx0 + 100:.0f}" height="16" fill="#3a2014"/>')
    # cortinas a los lados con pliegues
    for lado in (-1, 1):
        x_in = wx0 - mw - 10 if lado < 0 else wx1 + mw + 10
        x_out = x_in + lado * (w * (0.16 if V else 0.1))
        d = f"M{x_in:.0f} {wy0 - 80:.0f} C{x_in + lado * 10:.0f} {wy0 + 300:.0f} {x_in - lado * 20:.0f} {wy1:.0f} {x_in + lado * 30:.0f} {wy1 + 160:.0f} L{x_out:.0f} {wy1 + 170:.0f} L{x_out:.0f} {wy0 - 80:.0f} Z"
        L.add(f'<path d="{d}" fill="{L.lg((0, "#8a2a24"), (0.5, "#a83a2e"), (1, "#5a1a16"), x2=1, y2=0)}"/>')
        cl = L.clip(d)
        pl = "".join(f'<path d="M{x_in + lado * k * 22:.0f} {wy0 - 80:.0f} C{x_in + lado * (k * 22 + 10):.0f} {wy0 + 300:.0f} {x_in + lado * (k * 22 - 14):.0f} {wy1:.0f} {x_in + lado * (k * 22 + 24):.0f} {wy1 + 170:.0f}" stroke="{["#3a0e0c", "#e07a5a"][k % 2]}" stroke-width="{[10, 4][k % 2]}" opacity="0.4" fill="none"/>' for k in range(1, 14))
        L.add(f'<g clip-path="{cl}">{pl}</g>')
        L.add(f'<rect x="{min(x_in, x_out) - 10:.0f}" y="{wy0 - 100:.0f}" width="{abs(x_out - x_in) + 20:.0f}" height="14" rx="7" fill="#3a2414"/>')
    # zócalo y suelo de tarima
    L.add(f'<rect x="0" y="{ysuelo - 40:.0f}" width="{w}" height="40" fill="#3a2214"/>')
    L.add(f'<rect x="0" y="{ysuelo:.0f}" width="{w}" height="{h - ysuelo:.0f}" fill="{L.lg((0, "#7a4a2a"), (1, "#3a2010"))}"/>')
    for k in range(-10, 11):
        L.add(f'<path d="M{w / 2 + k * 70:.0f} {ysuelo:.0f} L{w / 2 + k * 200:.0f} {h:.0f}" stroke="#2a160c" stroke-width="2" opacity="0.6"/>')
    L.add(L.relieve(sem + 3, freq="0.003 0.06", escala=2, az=180, elev=60, op=0.3, oct=3, modo="soft-light", caja=(0, ysuelo, w, h - ysuelo)))
    # luz cálida de la lámpara (izquierda) y reflejo frío de la ventana
    L.add(L.luz(-w * 0.1, h * 0.55, w * 0.8, h * 0.55, "#ffa850", 0.5))
    L.add(L.luz((wx0 + wx1) / 2, ysuelo + 80, (wx1 - wx0) * 0.6, 120, "#6a8ac0", 0.25))
    L.add(L.oscuridad(w * 0.4, h * 0.45, w * 0.9, h * 0.7, color="#140a06", op=0.7, medio=0.2))
    return {"suelo": ysuelo + (50 if V else 40), "nota": f"ventana en x {wx0:.0f}–{wx1:.0f}, y {wy0}–{wy1}; suelo de tarima desde y={ysuelo}"}


# ============================================================================ cabeza, cerebro, cielo, silencio
CIAN, MAGENTA = "#2ff3ff", "#ff3df2"


def _neurona(x, y, s, col, r, ramas=6):
    out = [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{7 * s:.1f}" fill="{col}" opacity="0.9"/>',
           f'<circle cx="{x - 2 * s:.1f}" cy="{y - 2 * s:.1f}" r="{2.6 * s:.1f}" fill="#ffffff" opacity="0.85"/>']
    for k in range(ramas):
        a = 2 * math.pi * k / ramas + r.uniform(-0.4, 0.4)
        L_ = r.uniform(40, 110) * s
        pts = [(x, y)]
        for j in range(4):
            a += r.uniform(-0.35, 0.35)
            pts.append((pts[-1][0] + math.cos(a) * L_ / 4, pts[-1][1] + math.sin(a) * L_ / 4))
        out.append(f'<path d="{suave(pts, cerrado=False)}" stroke="{col}" stroke-width="{2.2 * s:.1f}" opacity="0.7" fill="none" stroke-linecap="round"/>')
        if r.random() < 0.7:   # ramificación
            bx, by = pts[2]
            a2 = a + r.choice([-0.8, 0.8])
            out.append(f'<path d="M{bx:.1f} {by:.1f} q{math.cos(a2) * 15 * s:.1f} {math.sin(a2) * 15 * s:.1f} {math.cos(a2) * 32 * s:.1f} {math.sin(a2) * 30 * s:.1f}" '
                       f'stroke="{col}" stroke-width="{1.2 * s:.1f}" opacity="0.55" fill="none"/>')
        ex, ey = pts[-1]
        out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="{1.6 * s:.1f}" fill="#ffffff" opacity="0.7"/>')
    return "".join(out)


def bg_cerebro(L, sem=151):
    """«Dentro de la cabeza»: red de neuronas difusa en capas (cian y magenta suaves), profundidad, partículas."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    L.add(L.rect(L.lg((0, "#0b0f24"), (0.6, "#140f34"), (1, "#1b1340"))))
    # nebulosa de fondo (una pasada de ruido, enmascarada al centro)
    f = L.ruido("#3a2a8a", sem, freq=0.004, contraste=2.0, corte=0.85, oct=4)
    L.add(f'<rect width="{w}" height="{h}" filter="{f}" opacity="0.55"/>')
    L.add(L.luz(w * 0.3, h * 0.35, w * 0.6, h * 0.3, "#1a8aa0", 0.35), L.luz(w * 0.72, h * 0.62, w * 0.6, h * 0.3, "#a02a9a", 0.3))
    capas = [(80, 0.5, "url(#blur8)", 0.75), (36, 0.8, "url(#blur8)", 0.85), (12, 1.25, None, 0.95)]
    puntos_cerca = []
    for n, esc, filt, op in capas:
        g = []
        pts = [(r.uniform(-50, w + 50), r.uniform(-50, h + 50)) for _ in range(int(n * (w * h) / (1080 * 1920)))]
        if filt is None:
            pts = [(r.uniform(w * 0.05, w * 0.95), r.uniform(h * 0.12, h * 0.88)) for _ in range(n if V else n + 2)]
            puntos_cerca = pts
        for i, (x, y) in enumerate(pts):   # conexiones con el vecino más cercano
            otros = sorted(pts, key=lambda q: (q[0] - x) ** 2 + (q[1] - y) ** 2)[1:3]
            for (x2, y2) in otros:
                col = CIAN if (i % 2) else MAGENTA
                mx, my = (x + x2) / 2 + r.uniform(-60, 60), (y + y2) / 2 + r.uniform(-60, 60)
                g.append(f'<path d="M{x:.0f} {y:.0f} Q{mx:.0f} {my:.0f} {x2:.0f} {y2:.0f}" stroke="{col}" stroke-width="{1.4 * esc:.1f}" opacity="0.35" fill="none"/>')
        for i, (x, y) in enumerate(pts):
            g.append(_neurona(x, y, esc * r.uniform(0.8, 1.3), CIAN if i % 3 else MAGENTA, r))
        attr = f' filter="{filt}"' if filt else ""
        L.add(f'<g opacity="{op}"{attr}>' + "".join(g) + "</g>")
    # chispas de sinapsis en las neuronas de delante
    for x, y in puntos_cerca:
        L.add(L.brillo(x, y, 46, 46, r.choice([CIAN, MAGENTA]), 0.45))
    L.add(L.polvo(260 if V else 300, 0, 0, w, h, "#bfefff", 1.8, 0.7, sem=sem + 2))
    L.add(L.polvo(80, 0, 0, w, h, "#ffb0f8", 1.6, 0.6, sem=sem + 3))
    L.add(L.oscuridad(w / 2, h / 2, w * 0.8, h * 0.7, color="#05061a", op=0.85, medio=0.25))
    return {"centro": (w // 2, h // 2), "nota": "red de neuronas sin centro marcado; viñeta oscura en los bordes"}


def bg_amanecer(L, sem=161):
    """Amanecer sobre colinas: el sol asomando en el horizonte, cielo de violeta a naranja, mucha luz."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    yhz = 1000 if V else 560
    ysuelo = 1360 if V else 840
    sx = w * 0.5
    L.add(L.rect(L.lg((0, "#2a1a58"), (0.3, "#6a3a8a"), (0.55, "#d0607a"), (0.75, "#f6964a"), (0.9, "#ffd07a"), (1, "#fff0c0")), h=yhz + 60))
    L.add(L.luz(sx, yhz, w * 1.1, 760 if V else 480, "#ffd890", 0.65))
    for k in range(16):   # rayos
        a_ = math.pi + math.pi * (k + 0.5) / 16
        L.add(f'<path d="M{sx:.0f} {yhz:.0f} L{sx + math.cos(a_ - 0.03) * 1600:.0f} {yhz + math.sin(a_ - 0.03) * 1600:.0f} L{sx + math.cos(a_ + 0.03) * 1600:.0f} {yhz + math.sin(a_ + 0.03) * 1600:.0f} Z" '
              f'fill="{L.rgu(sx, yhz, 1500, 1500, (0, "#fff4d0", 0.18), (1, "#fff4d0", 0))}"/>')
    for k in range(6 if V else 8):   # nubes alargadas encendidas por debajo
        y = r.uniform(yhz - (700 if V else 430), yhz - 120)
        x = r.uniform(-100, w)
        ln = r.uniform(250, 600)
        L.add(f'<path d="M{x:.0f} {y:.0f} q{ln * 0.5:.0f} {-r.uniform(10, 30):.0f} {ln:.0f} 0 q{-ln * 0.5:.0f} {r.uniform(14, 26):.0f} {-ln:.0f} 0 Z" fill="#8a4a8a" opacity="0.7"/>'
              f'<path d="M{x + 20:.0f} {y + 6:.0f} q{ln * 0.5:.0f} 10 {ln - 40:.0f} 0" stroke="#ffc080" stroke-width="4" opacity="0.8" fill="none"/>')
    # sol asomando (medio disco) con halo
    L.add(L.brillo(sx, yhz, 260, 260, "#fff2c0", 0.95), f'<circle cx="{sx:.0f}" cy="{yhz:.0f}" r="{96 if V else 80}" fill="#fffbe8"/>')
    # colinas en capas (perspectiva atmosférica: lejos claras y violáceas, cerca oscuras), bruma en los valles
    cols = ["#d89a9a", "#b07890", "#7a5078", "#4a3058", "#2a1a38"]
    for i, c in enumerate(cols):
        y0 = yhz - 10 + i * (85 if V else 55)
        pts = linea_ruido(r, -60, y0 + r.uniform(-20, 20), w + 60, y0 + r.uniform(-20, 20), 10, 40 + i * 10, 0.4)
        d = suave(pts, cerrado=False) + f" L{w + 60} {h + 40} L-60 {h + 40} Z"
        L.add(f'<path d="{d}" fill="{L.lg((0, mezcla(c, "#ffd0a0", 0.25)), (0.3, c), (1, mezcla(c, "#000000", 0.2)))}"/>')
        L.add(f'<path d="{suave(pts, cerrado=False)}" stroke="#ffd8a0" stroke-width="{3 - i * 0.4:.1f}" opacity="{0.7 - i * 0.1:.2f}" fill="none"/>')
        if i >= 2:   # árboles pequeños en la cresta
            for _ in range(5 + i * 2):
                x = r.uniform(0, w)
                yy = min(p[1] for p in pts if abs(p[0] - x) < w / 10 + 30) if any(abs(p[0] - x) < w / 10 + 30 for p in pts) else y0
                ss = 0.3 + i * 0.12
                L.add(f'<ellipse cx="{x:.0f}" cy="{yy + 6 - 20 * ss:.0f}" rx="{18 * ss:.0f}" ry="{22 * ss:.0f}" fill="{mezcla(c, "#000000", 0.25)}"/>')
        L.add(L.bruma(y0 + (60 if V else 40), 90 if V else 60, "#ffd8b0", 0.45 - i * 0.07))
    # cresta cercana donde se posan los personajes, con hierba a contraluz
    pts = linea_ruido(r, -60, ysuelo - 40, w + 60, ysuelo - 30, 10, 20, 0.4)
    d = suave(pts, cerrado=False) + f" L{w + 60} {h + 40} L-60 {h + 40} Z"
    L.add(f'<path d="{d}" fill="{L.lg((0, "#2a1a2a"), (1, "#120a14"))}"/>')
    hierba = []
    for _ in range(int(w / 3)):
        x = r.uniform(-20, w + 20)
        y = ysuelo - 35 + r.uniform(-8, 10) + 10 * math.sin(x / 90)
        hl = r.uniform(10, 34)
        hierba.append(f'<path d="M{x:.0f} {y + 6:.0f} q{r.uniform(-4, 4):.0f} {-hl / 2:.0f} {r.uniform(-8, 8):.0f} {-hl:.0f}" stroke="#1a0e18" stroke-width="2" fill="none"/>')
    L.add("".join(hierba))
    L.add(f'<path d="{suave(pts, cerrado=False)}" stroke="#ffb870" stroke-width="3" opacity="0.6" fill="none"/>')
    L.add(L.polvo(80, 0, yhz - 400, w, ysuelo, "#fff0c8", 2, 0.6, sem=sem + 4))
    L.add(L.luz(sx, yhz + 40, w * 0.7, 300, "#ffcf8a", 0.35))
    return {"suelo": ysuelo, "nota": f"sol en ({sx:.0f},{yhz}); cresta oscura a contraluz delante"}


def bg_tienda_noche(L, sem=171):
    """Explanada junto a la entrada de la cueva de noche, cielo estrellado, zona plana para una tienda."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    yhz = 1000 if V else 540
    ysuelo = 1340 if V else 830
    L.add(L.rect(L.lg((0, "#03040e"), (0.6, "#0b1430"), (1, "#1c2a50")), h=yhz + 80))
    # Vía Láctea en diagonal y estrellas
    L.add(f'<ellipse cx="{w * 0.5:.0f}" cy="{yhz * 0.45:.0f}" rx="{w * 0.9:.0f}" ry="{140 if V else 110}" fill="#c9d4ff" opacity="0.10" transform="rotate(-35 {w * 0.5:.0f} {yhz * 0.45:.0f})" filter="url(#blur40)"/>')
    L.add(f'<ellipse cx="{w * 0.5:.0f}" cy="{yhz * 0.45:.0f}" rx="{w * 0.8:.0f}" ry="{50 if V else 40}" fill="#fff4e0" opacity="0.10" transform="rotate(-35 {w * 0.5:.0f} {yhz * 0.45:.0f})" filter="url(#blur20)"/>')
    cs = ["#ffffff", "#cfe0ff", "#fff1c8", "#ffd2a0"]
    est = []
    for _ in range(int(700 * w * yhz / (1080 * 1000))):
        x, y = r.uniform(0, w), r.uniform(0, yhz)
        if r.random() < 0.5:   # concentradas en la banda
            t = r.uniform(-0.6, 0.6)
            x = w * 0.5 + math.cos(math.radians(-35)) * t * w * 1.6 + r.gauss(0, 60)
            y = yhz * 0.45 + math.sin(math.radians(-35)) * t * w * 1.6 + r.gauss(0, 60)
        est.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(0.5, 1.5):.1f}" fill="{r.choice(cs)}" opacity="{r.uniform(0.3, 0.95):.2f}"/>')
    L.add("".join(est))
    for _ in range(14):
        x, y = r.uniform(20, w - 20), r.uniform(20, yhz - 120)
        L.add(L.brillo(x, y, 14, 14, "#dfe8ff", 0.6), f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.4" fill="#ffffff"/>')
    # sierra lejana y luces del pueblo
    sp = [(-20, yhz + 20)] + [(x, yhz - 40 - r.uniform(0, 90)) for x in range(0, w + 100, 90)] + [(w + 20, yhz + 20)]
    L.add(f'<path d="{suave(sp, t=0.2)}" fill="#141c34"/>')
    L.add(L.bruma(yhz, 80, "#2a3a60", 0.5))
    L.add(f'<path d="M-20 {yhz + 10} L{w + 20} {yhz + 10} L{w + 20} {ysuelo} L-20 {ysuelo} Z" fill="{L.lg((0, "#0e1428"), (1, "#151c34"))}"/>')
    for _ in range(90 if V else 140):
        x = r.gauss(w * 0.3, w * 0.12)
        y = yhz + r.uniform(14, 60)
        L.add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(0.8, 2):.1f}" fill="{r.choice(["#ffd080", "#ffb050", "#fff0c0"])}" opacity="{r.uniform(0.5, 1):.2f}"/>')
    L.add(L.luz(w * 0.3, yhz + 40, w * 0.3, 60, "#ffb050", 0.3))
    # ladera de la cueva a la derecha con la boca oscura
    bx, by = (w * 0.8, ysuelo - 230) if V else (w * 0.84, ysuelo - 200)
    lad = [(w * 0.45, ysuelo - 30), (w * 0.6, ysuelo - 200), (w * 0.72, by - 220), (w * 0.88, by - 300), (w + 40, by - 330), (w + 40, h + 40), (w * 0.45, h + 40)]
    dl = suave(lad, t=0.35)
    L.add(L.roca(dl, (w * 0.45, by - 330, w + 40, h), "#06080e", "#121826", "#2e3850", luz=(0.2, 0), sem=sem + 1, estratos=8, inclin=-0.1,
                 vetas=8, humedad=0, brillos=0, borde="#a8c0f0", borde_op=0.5))
    bw, bh = 200, 150
    bp = [(bx + math.cos(2 * math.pi * k / 14) * bw / 2 * r.uniform(0.9, 1.1), by + min(bh * 0.4, math.sin(2 * math.pi * k / 14) * bh / 2 * r.uniform(0.9, 1.1))) for k in range(14)]
    L.add(f'<path d="{suave(bp)}" fill="#010103"/>', f'<path d="{suave(bp[7:] + bp[:1], cerrado=False)}" stroke="#a8c0f0" stroke-width="3" opacity="0.45" fill="none"/>')
    # explanada llana (tierra a la luz de la luna) con olivos en silueta y matorral
    exp = linea_ruido(r, -40, ysuelo - 60, w + 40, ysuelo - 50, 10, 10, 0.6)
    dex = suave(exp, cerrado=False) + f" L{w + 40} {h + 40} L-40 {h + 40} Z"
    L.add(f'<path d="{dex}" fill="{L.lg((0, "#3a4462"), (0.4, "#262e46"), (1, "#0e1220"))}"/>')
    L.add(f'<path d="{suave(exp, cerrado=False)}" stroke="#a8c0f0" stroke-width="2" opacity="0.4" fill="none"/>')
    for _ in range(int(w / 10)):
        x, y = r.uniform(0, w), r.uniform(ysuelo - 40, h)
        if abs(x - w * 0.42) < w * 0.25 and y < ysuelo + (160 if V else 110):
            continue
        sz = r.uniform(1.5, 4) * (1 + (y - ysuelo) / 300)
        L.add(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{sz:.1f}" ry="{sz * 0.6:.1f}" fill="#0a0d16" opacity="0.7"/>'
              f'<ellipse cx="{x:.0f}" cy="{y - sz * 0.4:.0f}" rx="{sz * 0.5:.1f}" ry="{sz * 0.2:.1f}" fill="#a8c0f0" opacity="0.35"/>')
    for x in (w * 0.06, w * 0.2) if V else (w * 0.05, w * 0.15, w * 0.6):
        L.add(_olivo(L, x, ysuelo - 50 + r.uniform(-10, 10), 0.9, r, c_hoja="#141a28", c_luz="#3a4a6a", c_tronco="#0e1018"))
    for x in (r.uniform(-20, w * 0.1), r.uniform(w * 0.9, w + 20)):
        L.add(_matorral(L, x, h - r.uniform(60, 160), 2.6, r, "#141a28", "#3a4a6a"))
    L.add(L.relieve(sem + 2, freq="0.01 0.03", escala=3, az=225, elev=50, op=0.3, oct=3, modo="soft-light", caja=(0, ysuelo - 60, w, h - ysuelo + 60)))
    L.add(L.luz(w * 0.42, ysuelo + 40, w * 0.4, 120, "#8aa4d8", 0.18))
    return {"suelo": ysuelo + (40 if V else 30), "nota": f"zona plana para la tienda centrada en x≈{w * 0.42:.0f}; boca de la cueva a la derecha ({bx:.0f},{by:.0f})"}


def bg_salida_luz(L, sem=181):
    """Desde dentro de la cueva mirando a la boca: contraluz cegador de día, polvo en el aire, roca en silueta."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    cx, cy = w / 2, (760 if V else 380)
    bw, bh = (520, 560) if V else (640, 440)
    ysuelo = 1340 if V else 830
    L.add(L.rect("#050403"))
    # la boca: luz blanca cálida, con un paisaje apenas intuido (quemado)
    bp = []
    for k in range(20):
        a = 2 * math.pi * k / 20
        rr = 1 + r.uniform(-0.12, 0.1) + 0.06 * math.sin(a * 3)
        y = cy + math.sin(a) * bh / 2 * rr
        if math.sin(a) > 0.5:
            y = cy + bh * 0.42 + r.uniform(-10, 10)
        bp.append((cx + math.cos(a) * bw / 2 * rr, y))
    dbo = suave(bp, t=0.35)
    L.add(f'<path d="{dbo}" fill="{L.lg((0, "#fffdf4"), (0.6, "#fff6dc"), (1, "#f8e2b0"))}"/>')
    L.add(f'<g clip-path="{L.clip(dbo)}"><path d="M{cx - bw:.0f} {cy + bh * 0.2:.0f} Q{cx - bw * 0.2:.0f} {cy + bh * 0.05:.0f} {cx + bw:.0f} {cy + bh * 0.25:.0f} L{cx + bw} {cy + bh} L{cx - bw} {cy + bh} Z" fill="#e8d8b0" opacity="0.5"/></g>')
    # haces de luz que entran hacia el espectador
    for k in range(9):
        x0 = cx + r.uniform(-0.4, 0.4) * bw
        x1 = cx + (x0 - cx) * 4 + r.uniform(-200, 200)
        wd0, wd1 = r.uniform(20, 70), r.uniform(150, 420)
        L.add(f'<path d="M{x0 - wd0:.0f} {cy:.0f} L{x0 + wd0:.0f} {cy:.0f} L{x1 + wd1:.0f} {h + 100} L{x1 - wd1:.0f} {h + 100} Z" '
              f'fill="{L.lg((0, "#fff2d0", 0.3), (1, "#fff2d0", 0))}" style="mix-blend-mode:screen"/>')
    # roca en silueta alrededor (anillo), con luz de borde cegadora
    d = f"M-100 -100 L{w + 100} -100 L{w + 100} {h + 100} L-100 {h + 100} Z " + dbo
    L.add(f'<path d="{d}" fill="{L.rgu(cx, cy, bw * 1.3, bh * 1.4, (0, "#5a4430", 1), (0.45, "#2a1e16", 1), (1, "#050403", 1))}" fill-rule="evenodd"/>')
    L.add(f'<path d="{dbo}" fill="none" stroke="#ffe6b0" stroke-width="10" opacity="0.6" filter="url(#blur8)"/>',
          f'<path d="{dbo}" fill="none" stroke="#fff4dc" stroke-width="3" opacity="0.9"/>')
    gm = (L._grad_cono("#050403", "#1a120d", "#c89860", -1), L._grad_cono("#050403", "#1a120d", "#c89860", 1))
    for k in range(9):   # estalactitas en contraluz colgando del borde superior
        x = cx + r.uniform(-0.45, 0.45) * bw
        y = cy - bh * 0.45 + abs(x - cx) * 0.3
        L.add(L.estalactita(x, y - 20, r.uniform(40, 140), r.uniform(16, 36), gm[1] if x < cx else gm[0], r=r, gota_col="#fff6dc"))
    # suelo que sube hacia la boca, con piedras de canto iluminado
    sp = [(-40, h * 0.86), (w * 0.12, cy + bh * 0.95), (cx - bw * 0.45, cy + bh * 0.44), (cx + bw * 0.45, cy + bh * 0.44), (w * 0.88, cy + bh * 0.92),
          (w + 40, h * 0.84), (w + 40, h + 40), (-40, h + 40)]
    ds = suave(sp, t=0.3)
    L.add(f'<path d="{ds}" fill="{L.rgu(cx, cy + bh * 0.44, w * 0.7, h - cy, (0, "#7a5c40", 1), (0.35, "#3a2a1e", 1), (1, "#070504", 1))}"/>')
    for _ in range(40 if V else 55):
        t = r.random()
        y = cy + bh * 0.46 + (h - cy - bh * 0.46) * t ** 0.8
        x = cx + r.uniform(-1, 1) * (bw * 0.45 + t * w * 0.6)
        if abs(x - cx) < w * 0.16 and y > ysuelo - 120 and y < ysuelo + 160:
            continue
        an = (10 + r.uniform(0, 40)) * (0.4 + t * 2)
        L.add(L.pedrusco(x, y, an, an * 0.6, 0, ("#030202", "#120d0a", "#3a2a1c"), r=r, borde="#ffe6b0", facetas=False))
    L.add(L.relieve(sem + 1, freq="0.008 0.016", escala=6, az=270, elev=35, op=0.4, oct=4))
    L.add(L.luz(cx, cy, bw * 1.6, bh * 1.6, "#ffe8c0", 0.55))
    L.add(L.brillo(cx, cy, bw * 0.55, bh * 0.5, "#ffffff", 0.7))
    L.add(L.polvo(260 if V else 320, cx - bw, cy - bh * 0.3, cx + bw, h, "#fff4dc", 2.6, 0.8, sem=sem + 3))
    return {"suelo": ysuelo, "nota": f"boca de luz centrada en ({cx:.0f},{cy}); suelo sube hacia ella; personaje en silueta en el centro"}


def bg_negro_cueva(L, sem=191):
    """Oscuridad casi total: apenas textura de roca y unas gotas brillando (planos de silencio)."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    L.add(L.rect("#040507"))
    d = f"M0 0 L{w} 0 L{w} {h} L0 {h} Z"
    L.add(L.roca(d, (0, 0, w, h), "#030405", "#08090c", "#14161c", luz=(0.5, 0.4), sem=sem, estratos=14, inclin=0.04, vetas=8, humedad=8, brillos=0, contraste=0.6))
    L.add(L.relieve(sem + 1, freq="0.006 0.015", escala=6, az=250, elev=35, op=0.35, oct=4))
    gm = (L._grad_cono("#020203", "#07080b", "#1a1e28", -1), L._grad_cono("#020203", "#07080b", "#1a1e28", 1))
    puntas = []
    for k in range(int(w / 110)):
        x = r.uniform(0, w)
        Lc = r.uniform(120, 480 if V else 300)
        rr = random.Random(sem + k)
        L.add(L.estalactita(x, -10, Lc, r.uniform(26, 60), gm[1] if x < w / 2 else gm[0], r=rr, gota=False, c_osc="#000"))
        puntas.append((x, Lc))
    for x, Lc in r.sample(puntas, min(5, len(puntas))):
        y = Lc + 4
        L.add(L.brillo(x, y, 18, 18, "#bfe0ff", 0.6), f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="3" ry="4.2" fill="#dff0ff"/>'
              f'<circle cx="{x - 1:.0f}" cy="{y - 1.5:.0f}" r="1.3" fill="#ffffff"/>')
    for _ in range(5):   # gotas sueltas en la roca y un charquito con onda
        x, y = r.uniform(w * 0.1, w * 0.9), r.uniform(h * 0.25, h * 0.75)
        L.add(L.brillo(x, y, 10, 10, "#cfe6ff", 0.5), f'<circle cx="{x:.0f}" cy="{y:.0f}" r="1.6" fill="#ffffff" opacity="0.9"/>')
    px, py = w * 0.5, h * (0.7 if V else 0.78)
    for k in range(3):
        L.add(f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="{30 + k * 34}" ry="{6 + k * 7}" fill="none" stroke="#9cc4ee" stroke-width="1.2" opacity="{0.35 - k * 0.1:.2f}"/>')
    L.add(L.oscuridad(w / 2, h * 0.45, w * 0.8, h * 0.6, color="#000000", op=0.9, medio=0.4))
    return {"centro": (round(px), round(py)), "nota": "casi negro; charquito con ondas en el centro-bajo"}


_PERFIL = [(0.30, 1.0), (0.28, 0.82), (0.19, 0.64), (0.16, 0.44), (0.22, 0.22), (0.36, 0.09), (0.52, 0.04), (0.66, 0.07),
           (0.76, 0.15), (0.80, 0.25), (0.815, 0.33), (0.795, 0.37), (0.815, 0.42), (0.85, 0.48), (0.895, 0.545), (0.88, 0.565),
           (0.85, 0.575), (0.855, 0.60), (0.87, 0.625), (0.855, 0.645), (0.86, 0.665), (0.845, 0.695), (0.835, 0.715), (0.85, 0.75),
           (0.82, 0.785), (0.74, 0.80), (0.64, 0.82), (0.62, 1.0)]


def bg_seccion_cabeza(L, sem=201):
    """Perfil de cabeza en corte (mira a la derecha), silueta suave sin rasgos, interior oscuro para el cerebro, luz de borde."""
    w, h, V = L.w, L.h, L.v
    r = random.Random(sem)
    if V:
        bw, bh, ox, oy = 840, 880, 110, 400
    else:
        bw, bh, ox, oy = 640, 670, 640, 70
    P = lambda u, v: (ox + u * bw, oy + v * bh)
    L.add(L.rect(L.lg((0, "#0b0f24"), (1, "#1b1340"))))
    L.add(L.polvo(160, 0, 0, w, h, "#bfefff", 1.4, 0.5, sem=sem))
    L.add(L.luz(ox + bw * 0.5, oy + bh * 0.4, bw * 0.9, bh * 0.7, "#3a2a8a", 0.4))
    pts = [P(u, v) for u, v in _PERFIL]
    vfin = (h + 60 - oy) / bh
    pts = [P(-0.25, vfin), P(-0.18, 1.22), P(0.12, 1.1), P(0.29, 1.02)] + pts[1:-1] + [P(0.63, 1.02), P(0.8, 1.1), P(1.1, 1.24), P(1.2, vfin)]
    d = suave(pts, t=0.45)
    L.add(f'<path d="{d}" fill="{L.lg((0, "#3a3478"), (0.5, "#24205a"), (1, "#0e0c2a"), x1=1, y1=0, x2=0, y2=1)}"/>')
    cl = L.clip(d)
    # cavidad del cráneo: hueso (banda) + interior muy oscuro donde va el cerebro
    ccx, ccy = P(0.47, 0.34)
    rx, ry = bw * 0.29, bh * 0.25
    L.add(f'<g clip-path="{cl}">'
          f'<ellipse cx="{ccx:.0f}" cy="{ccy:.0f}" rx="{rx * 1.1:.0f}" ry="{ry * 1.1:.0f}" fill="#2e2a5a" opacity="0.8"/>'
          f'<ellipse cx="{ccx:.0f}" cy="{ccy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{L.rgu(ccx, ccy, rx, ry, (0, "#05061a", 1), (0.8, "#080824", 1), (1, "#1a1640", 1))}"/>'
          f'<ellipse cx="{ccx:.0f}" cy="{ccy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="none" stroke="{CIAN}" stroke-width="2" opacity="0.25"/>'
          + L.brillo(ccx, ccy, rx * 0.8, ry * 0.8, "#3a2a8a", 0.25) + "</g>")
    # luz de borde: cian por la cara, magenta por la nuca
    cara = suave(pts[11:30], cerrado=False, t=0.45)
    nuca = suave(pts[2:11], cerrado=False, t=0.45)
    L.add(f'<g clip-path="{cl}"><path d="{cara}" stroke="{CIAN}" stroke-width="26" opacity="0.18" fill="none"/><path d="{cara}" stroke="{CIAN}" stroke-width="6" opacity="0.7" fill="none"/>'
          f'<path d="{nuca}" stroke="{MAGENTA}" stroke-width="26" opacity="0.15" fill="none"/><path d="{nuca}" stroke="{MAGENTA}" stroke-width="5" opacity="0.6" fill="none"/></g>')
    L.add(f'<path d="{cara}" stroke="{CIAN}" stroke-width="14" opacity="0.25" fill="none" filter="url(#blur8)"/>')
    L.add(L.oscuridad(w / 2, h / 2, w * 0.9, h * 0.8, color="#05061a", op=0.7, medio=0.15))
    return {"centro": (round(ccx), round(ccy)), "nota": f"hueco del cerebro: elipse centro ({ccx:.0f},{ccy:.0f}) {2 * rx:.0f}×{2 * ry:.0f}; mira a la derecha"}


ESCENAS = [bg_cueva_campamento, bg_cueva_campamento_oscura, bg_cueva_galeria, bg_cueva_pozo, bg_corte_tierra,
           bg_entrada_dia, bg_entrada_atardecer, bg_cueva_hielo, bg_alpes_nieve, bg_cueva_francia, bg_ciudad,
           bg_estadio_noche, bg_playa_verano, bg_oficina_gris, bg_ventana_invierno, bg_cerebro, bg_amanecer,
           bg_tienda_noche, bg_salida_luz, bg_negro_cueva, bg_seccion_cabeza]
INFO = {}


def generar(dirsvg, solo=None):
    nombres = []
    for i, f in enumerate(ESCENAS):
        nom = f.__name__
        if solo and nom not in solo:
            continue
        for w, h, suf in ((1080, 1920, ""), (1920, 1080, "_h")):
            L = Lienzo(nom + suf, w, h, 1000 + i * 37)
            INFO[nom + suf] = f(L) or {}
            L.guardar(dirsvg, nom + suf)
            nombres.append(nom + suf)
    return nombres


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg", sys.argv[2:] or None))
