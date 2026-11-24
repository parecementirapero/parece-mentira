"""Piezas comunes del vídeo largo «500 días en una cueva» (dos formatos, un solo montaje).

CÓMO SE COMPONE PARA LOS DOS FORMATOS
- Cada plano se escribe UNA vez en coordenadas del vertical (1080×1920), como en cualquier Short.
- En el horizontal (MOTOR_FORMATO=16:9) el plano se recoloca solo (`adaptar`):
  - Cada fondo tiene un ancla (suelo o centro) en los dos formatos, y todo se coloca respecto a ella con escala KH (≈0,8).
  - Los pies que pisan el suelo en el vertical pisan el suelo en el horizontal.
  - El fondo se cambia por su versión `_h` (dibujada en 16:9, no recortada).
- Lo que se pone FUERA del vertical (x < 0 o x > 1080) solo se ve en el horizontal: rellena los laterales.
  - Ejemplo: estalactitas, murciélagos, más libros, otra persona. Úsalo en todos los planos para que el horizontal no tenga laterales vacíos.
- `_ancho: True` en un elemento: su x se estira a todo el ancho (cruces de murciélagos, partículas por toda la pantalla).
  `_full: True`: ocupa toda la pantalla en los dos formatos (fundidos, partículas de pantalla completa).
  `_solo: "v"` / `"h"`: solo en ese formato.
- Los rótulos (hud) se recolocan igual. Luego `construir` los mete en la zona segura de cada formato.
"""
import math, os, re, random

from motor.denso import *  # noqa: F401,F403
from motor import denso as D
from motor.core import HORIZONTAL, W, H

AQUI = os.path.dirname(os.path.abspath(__file__))


# Versiones de los ayudantes del motor que dan SIEMPRE coordenadas del vertical (el motor, en el proceso horizontal,
# las daría ya en 16:9 y `adaptar` las movería dos veces). Usa estas, no las de motor.denso.
def cam(z0, z1, f0=(540, 960), f1=None, temblor=0):
    return D.cam(z0, z1, f0, f1, temblor)


def polvo(color="#fff1c8", n=40, area=(0, 300, 1080, 1700), sem=1, clase="polvo"):
    return D.polvo(color, n, area, sem, clase)


def estrellas(n=40, sem=3):
    return {**D.polvo("#ffffff", n, (0, 0, 1080, 1920), sem, "estrellas"), "_full": True}


def fundido_blanco(keys, color="#fff6e0"):
    """Fogonazo/fundido a pantalla completa por encima de todo (keys con `op`), en los dos formatos."""
    return {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": color, "x": 540, "y": 960, "hud": True, "z": 1,
            "keys": keys, "_full": True}


def negro(keys, color="#050507"):
    """Fundido a negro a pantalla completa (no tapa el subtítulo: va en els con z alto)."""
    return {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": color, "x": 540, "y": 960, "z": 0.97,
            "keys": keys, "_full": True}
KH = 0.8         # escala vertical → horizontal

# ancla de cada fondo: (x_v, y_v, x_h, y_h[, k]). y = suelo (o centro de interés). Datos de ilus_escenarios.INFO
ANCLA = {
    "bg_cueva_campamento": (540, 1300, 960, 730), "bg_cueva_campamento_oscura": (540, 1300, 960, 730),
    "bg_cueva_galeria": (540, 1360, 960, 730), "bg_cueva_pozo": (540, 1056, 960, 540, 0.62),
    "bg_corte_tierra": (605, 1330, 1152, 790, 0.62), "bg_entrada_dia": (605, 1370, 1152, 860, 0.7),
    "bg_entrada_atardecer": (605, 1370, 1152, 860, 0.7), "bg_cueva_hielo": (540, 1400, 960, 760),
    "bg_alpes_nieve": (540, 1340, 960, 820), "bg_cueva_francia": (540, 1330, 960, 830),
    "bg_ciudad": (540, 1390, 960, 830), "bg_estadio_noche": (540, 1395, 960, 765), "bg_playa_verano": (540, 1350, 960, 840),
    "bg_oficina_gris": (540, 1440, 960, 833), "bg_ventana_invierno": (540, 1480, 960, 940, 0.86),
    "bg_cerebro": (540, 960, 960, 540, 0.7), "bg_amanecer": (540, 1360, 960, 840), "bg_tienda_noche": (454, 1380, 806, 860),
    "bg_salida_luz": (540, 1340, 960, 830), "bg_negro_cueva": (540, 1344, 960, 842),
    "bg_seccion_cabeza": (505, 699, 941, 298, 0.76),
}
ANCLA_DEF = (540, 1000, 960, 500)

# ------------------------------------------------------------------ medidas de las piezas (del propio SVG)
_TAM = {}


def tam_svg(nombre):
    """(ancho, alto) del lienzo de una pieza (lee el SVG de la carpeta común de arte)."""
    if nombre not in _TAM:
        ruta = os.path.join(SVG_DIR, nombre + ".svg")
        cab = open(ruta, encoding="utf-8").read(400)
        m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', cab)
        _TAM[nombre] = (float(m.group(1)), float(m.group(2)))
    return _TAM[nombre]


SVG_DIR = None   # lo fija gen.py (carpeta con todo el arte generado)

# punto de apoyo (fracción de la altura desde arriba) de cada personaje u objeto que se posa; por defecto 0,97
APOYO = {
    "bea_lee_a": 0.93, "bea_lee_b": 0.93, "bea_duerme": 0.9, "bea_teje_a": 0.93, "bea_teje_b": 0.93, "bea_habla_a": 0.93,
    "bea_habla_b": 0.93, "bea_dibuja": 0.965, "siffre_telefono": 0.973, "equipo_1962": 0.972, "bebe": 0.955, "nino_corre": 0.96,
    "libro_a": 0.88, "libro_b": 0.88, "libro_c": 0.88, "libro_d": 0.88, "libro_abierto": 0.89, "vela_a": 0.95, "vela_b": 0.95,
    "vela_corta": 0.95, "ovillo_lana": 0.87, "gorro_lana_a": 0.9, "gorro_lana_b": 0.9, "gorro_lana_c": 0.9, "garrafa_agua": 0.94,
    "botella_agua": 0.94, "caja_comida": 0.92, "bolsa_basura": 0.93, "camara_tripode": 0.95, "lampara_led": 0.93, "colchon": 0.8,
    "estalagmita_a": 0.96, "estalagmita_b": 0.95, "tienda_campana": 0.92, "tienda_1962": 0.9, "telefono_campo": 0.9,
    "mesa_campamento": 0.96, "mochila": 0.94, "trofeo": 0.96, "urna_voto": 0.94, "cuna": 0.93, "flor_blanca": 0.96,
    "periodico": 0.94, "bici_nino": 0.92, "balon_playa": 0.94, "taza_cafe": 0.93, "pantalla_ordenador": 0.95,
    "reloj_arena_a": 0.95, "reloj_arena_b": 0.95, "calendario_taco": 0.96, "calendario_hoja": 0.96, "cifra_marco": 0.97,
    "salpicadura": 0.78,
}


def pie(nombre, x, suelo, alto, z=0.5, keys=None, **k):
    """Pieza posada en el suelo: sus pies (o su base) quedan en y=suelo. `alto` = altura en px del vertical."""
    w, h = tam_svg(nombre)
    ancho = alto * w / h
    y = suelo - (APOYO.get(nombre, 0.97) - 0.5) * alto
    return IMG(nombre, ancho=round(ancho), x=x, y=round(y), z=z, keys=keys or [], **k)


def pieza(nombre, x, y, ancho, z=0.5, keys=None, **k):
    """Pieza centrada en (x, y) con un ancho dado."""
    return IMG(nombre, ancho=round(ancho), x=x, y=y, z=z, keys=keys or [], **k)


def flip(nombres, d, fps=3.0, t0=0.0, base=None, **k):
    """Fotogramas que se alternan (pasar página, tejer, alas, llama). Devuelve una lista de IMG con claves de opacidad.
    base: función que crea la pieza: base(nombre) → dict. Por defecto pieza(n, **k)."""
    n = len(nombres)
    paso = 1.0 / fps
    out = []
    for i, nm in enumerate(nombres):
        e = base(nm) if base else pieza(nm, **k)
        ks = [{"t": 0, "op": 1.0 if i == 0 else 0.0}]
        t, j = t0, 0
        while t < d + paso:
            on = (j % n == i)
            ks += [{"t": round(max(0.0, t), 3), "op": 1.0 if on else 0.0, "ease": "lineal"},
                   {"t": round(max(0.0, t) + 0.001, 3), "op": 1.0 if on else 0.0}]
            t += paso; j += 1
        # op en claves aparte de las de movimiento (se fusionan por propiedad en el motor)
        e["keys"] = sorted(list(e.get("keys", [])) + ks[1:], key=lambda q: q["t"])
        if i:
            e["z"] = e.get("z", 0.5) + 0.001 * i
        out.append(e)
    return out


def fondo(nombre, z=0.05):
    """Fondo a pantalla completa. En el horizontal se cambia por `nombre_h`."""
    return {**BG(nombre, z=z), "_bg": nombre}


# ------------------------------------------------------------------ detalles de fondo que duran (tiempo absoluto)
def goteo(x, y0, y1, periodo, fase, d, z=0.7, ancho=26, suena=True, **k):
    """Gota que cae una y otra vez desde (x,y0) hasta y1 (periodo s, fase s). Depende del tiempo ABSOLUTO:
    sigue igual de un plano a otro. Suena un «plic» bajo al caer (como mucho cada 3 s)."""
    T0 = D._V.ini
    caida = 0.55
    ks = [{"t": 0, "op": 0, "x": x, "y": y0}]
    n0 = math.floor((T0 - fase) / periodo) - 1
    for n in range(n0, n0 + int(d / periodo) + 3):
        a = fase + n * periodo - T0      # inicio de la caída (s del plano)
        b = a + caida
        if b < 0 or a > d:
            continue
        ks += [{"t": round(a - 0.002, 3), "op": 0, "y": y0, "ease": "lineal"}, {"t": round(a, 3), "op": 1, "y": y0, "ease": "lineal"},
               {"t": round(b, 3), "op": 1, "y": y1, "ease": "entrada"}, {"t": round(b + 0.002, 3), "op": 0, "y": y0, "ease": "lineal"}]
        if suena and 0 <= b <= d:
            fx_espaciado("gota", T0 + b, "burbuja", -30, 3.0, f=1100 + 180 * ((n * 7) % 5))
    ks = [q for q in ks if q["t"] >= 0] or [{"t": 0, "op": 0}]
    if ks[0]["t"] > 0:
        ks.insert(0, {"t": 0, "op": 0, "y": y0, "x": x})
    return {**IMG("gota", ancho=ancho, x=x, y=y0, z=z, **k), "keys": sorted(ks, key=lambda q: q["t"])}


VUELOS = []   # (T0, T1, (x0,y0), (x1,y1), ancho)   cruces de murciélagos; los llena gen.py con tiempos de palabra


def murcielagos(d, z=0.3):
    """Murciélagos que cruzan el fondo (tiempo absoluto, de un plano a otro), aleteando. Se estiran a todo el ancho."""
    out = []
    for i, (T0, T1, p0, p1, an) in enumerate(VUELOS):
        if T1 < D._V.ini or T0 > D._V.ini + d:
            continue
        ks = recorrido(T0, T1, p0, p1, d)
        mira = -1 if p1[0] < p0[0] else 1
        for e in flip(["murcielago_a", "murcielago_b"], d, fps=7, t0=0.07 * i, x=p0[0], y=p0[1], ancho=an, z=z, ex=mira):
            e["keys"] = sorted(e["keys"] + ks, key=lambda q: q["t"])
            e["_ancho"] = True
            out.append(e)
        if T0 + 0.4 >= D._V.ini and T0 + 0.4 <= D._V.ini + d:
            fx_espaciado("murcielago", T0 + 0.4, "roce", -27, 4.0)
    return out


def techo(sem=1, oscura=False, z=0.82):
    """Estalactitas colgando del borde de arriba (en el vertical, bajo el subtítulo; en el horizontal, por todo el ancho)."""
    r = random.Random(sem)
    out = []
    for x in [-560, -380, -180, 60, 250, 860, 1010, 1260, 1450, 1640]:
        n = r.choice(["estalactita_a", "estalactita_b", "estalactita_c"])
        alto = r.uniform(260, 520)
        w, h = tam_svg(n)
        y = 180 + alto / 2 - r.uniform(0, 60)
        out.append(IMG(n, ancho=round(alto * w / h), x=x + r.uniform(-30, 30), y=round(y), z=z + r.uniform(-0.05, 0.05),
                       op=0.75 if oscura else 1.0))
    return out


def ambiente_cueva(d, sem=1, oscura=False, gotas=True, polvo_c="#ffd9a0", murc=True, primer_plano=None):
    """Lo que vive en la cueva en cualquier plano: estalactitas arriba, gotas que caen, polvo en la luz y murciélagos."""
    out = techo(sem, oscura)
    if gotas:
        r = random.Random(sem * 13)
        for j, x in enumerate([-420, 170, 900, 1350]):
            out.append(goteo(x + r.uniform(-40, 40), 420, 1290, r.uniform(2.6, 4.2), r.uniform(0, 3), d, z=0.72, suena=(j == 1)))
    out.append({**polvo(polvo_c if not oscura else "#9fc4ff", 34, (-500, 500, 1580, 1500), sem), "_ancho": False})
    if murc:
        out += murcielagos(d)
    if primer_plano:
        out.append(IMG(primer_plano, ancho=1700, x=540, y=1660, z=0.92))
    return out


def tiza(x, y, t0, alto=150, z=0.55):
    """Una raya de tiza que se dibuja (crece de arriba abajo) en t0."""
    return IMG("marca_raya", ancho=round(alto * 70 / 320), x=x, y=y, z=z, keys=[{"t": 0, "ey": 0.0, "op": 0}, {"t": t0, "ey": 0.0, "op": 1},
                                                                                {"t": t0 + 0.25, "ey": 1.0, "ease": "salida"}])


# ------------------------------------------------------------------ adaptación al horizontal
def _ancla(els):
    for e in els:
        if e.get("_bg") in ANCLA:
            return ANCLA[e["_bg"]]
    return ANCLA_DEF


def _mapa(a):
    xv, yv, xh, yh = a[:4]
    k = a[4] if len(a) > 4 else KH
    return (lambda x: xh + (x - xv) * k), (lambda y: yh + (y - yv) * k), k


def _trans(e, X, Y, k, modo):
    if modo == "full":
        fx_, fy_ = (lambda x: x * W / 1080), (lambda y: y * H / 1920)
        kk = W / 1080
    elif modo == "ancho":
        fx_, fy_, kk = (lambda x: x * W / 1080), Y, k
    else:
        fx_, fy_, kk = X, Y, k
    if "x" in e: e["x"] = round(fx_(e["x"]), 1)
    if "y" in e: e["y"] = round(fy_(e["y"]), 1)
    for c in ("ancho", "alto", "radio", "grosor", "longitud"):
        if c in e and isinstance(e[c], (int, float)): e[c] = round(e[c] * (k if modo != "full" else max(W / 1080, H / 1920)), 1)
    if e.get("tipo") == "rotulo" and "tam" in e: e["tam"] = max(40, int(e["tam"] * max(k, 0.86)))
    if e.get("tipo") == "flecha" and "puntos" in e: e["puntos"] = [[round(fx_(p[0]), 1), round(fy_(p[1]), 1)] for p in e["puntos"]]
    if e.get("tipo") == "forma" and e.get("forma") == "poligono": e["puntos"] = [[p[0] * kk, p[1] * kk] for p in e["puntos"]]
    if e.get("tipo") == "particulas" and "area" in e:
        x0, y0, x1, y1 = e["area"]
        if modo == "full" or (x1 - x0) >= 1000:
            e["area"] = [-40, -40, W + 40, H + 40] if (y1 - y0) >= 1500 or modo == "full" else [-40, round(fy_(y0)), W + 40, round(fy_(y1))]
        else:
            e["area"] = [round(fx_(x0)), round(fy_(y0)), round(fx_(x1)), round(fy_(y1))]
    for q in e.get("keys", []):
        if "x" in q: q["x"] = round(fx_(q["x"]), 1)
        if "y" in q: q["y"] = round(fy_(q["y"]), 1)
    if "anim" in e and "flotar" in e["anim"]:
        e["anim"] = {**e["anim"], "flotar": [e["anim"]["flotar"][0] * k, e["anim"]["flotar"][1]]}


def adaptar(p):
    """Convierte un plano escrito en vertical al formato actual. En el vertical solo quita las marcas internas."""
    els, hud = p["els"], p["hud"]
    if not HORIZONTAL:
        p["els"] = [e for e in els if e.get("_solo") != "h"]
        p["hud"] = [h for h in hud if h.get("_solo") != "h"]
        for e in p["els"] + p["hud"]:
            for c in ("_bg", "_ancho", "_full", "_solo"): e.pop(c, None)
        return p
    X, Y, k = _mapa(_ancla(els))
    nuevos = []
    for e in els:
        if e.get("_solo") == "v":
            continue
        if e.get("_bg"):
            e = {**e, "archivo": f"svg/{e['_bg']}_h.svg", "x": W / 2, "y": H / 2, "ancho": W + 100}
        else:
            _trans(e, X, Y, k, "full" if e.get("_full") else ("ancho" if e.get("_ancho") else "punto"))
        for c in ("_bg", "_ancho", "_full", "_solo"): e.pop(c, None)
        nuevos.append(e)
    p["els"] = nuevos
    hs = []
    for h in hud:
        if h.get("_solo") == "v":
            continue
        _trans(h, X, Y, k, "full" if h.get("_full") else "punto")
        if h.get("tipo") == "rotulo":
            h["y"] = max(h.get("y", 540), 70 + h.get("tam", 100) * 0.7)
        for c in ("_bg", "_ancho", "_full", "_solo"): h.pop(c, None)
        hs.append(h)
    p["hud"] = hs
    c = p["cam"]
    c["foco"] = [[round(X(f[0]), 1), round(Y(f[1]), 1)] for f in c["foco"]]
    return p


def registrar(v):
    """Sustituye v.plano por uno que adapta cada plano al formato. Úsalo así: plano = registrar(v)."""
    def plano(i, nombre, mas=0.0):
        def reg(fn):
            v.plano(i, nombre, mas)(lambda d, fn=fn: adaptar(fn(d)))
            return fn
        return reg
    return plano
