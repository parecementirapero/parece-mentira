"""03 · Tu perro copia tus bostezos — método denso. Lote 2026-11-18-manana, Agente 08:00 (Nico).
Uso: python3 gen_03.py DIR_SALIDA [03-locucion.mp3 03-alineacion.json]"""
import math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "..")))
from motor.denso import *  # noqa: E402,F401,F403
import ilus_03  # noqa: E402

SVG = ilus_03.generar(os.path.join(sys.argv[1], "_svg_lote"))
VOZ = sys.argv[2:4]
v = Video(sys.argv[1], os.path.join(AQUI, "03-guion.txt"), *(VOZ if len(VOZ) == 2 else ()), svg_extra=SVG)

SALON = ["#3a2a3a", "#1a1220"]
LAB = ["#06101e", "#0a0618"]
PIEL = ["#2a1c2a", "#120a14"]
TAN40 = math.tan(math.radians(ilus_03.ANG_MAX))


# ------------------------------------------------------------------ el perro que bosteza (3 piezas que giran en la bisagra)
def _interp(pts, t):
    if t <= pts[0][0]: return pts[0][1]
    for (t0, a), (t1, b) in zip(pts, pts[1:]):
        if t <= t1:
            u = (t - t0) / max(1e-6, t1 - t0)
            u = u * u * (3 - 2 * u)
            return a + (b - a) * u
    return pts[-1][1]


def bostezo(raza, x, y, ancho, d, apertura, z=0.5, espejo=False, pos=None, esc=None, paso=1 / 15):
    """apertura = [(t, f)] con f de 0 (cerrada) a 1 (bostezo entero). pos(t) → (x, y) opcional; esc(t) → escala."""
    sg = -1 if espejo else 1
    ks = {"sup": [], "mand": [], "boca": []}
    n = max(2, int(d / paso) + 1)
    for i in range(n + 1):
        t = min(d, i * paso)
        f = _interp(apertura, t)
        px, py = pos(t) if pos else (x, y)
        e = esc(t) if esc else 1.0
        base = {"t": round(t, 3), "x": round(px, 1), "y": round(py, 1), "escala": round(e, 4), "ease": "lineal"}
        ks["sup"].append({**base, "rot": round(-sg * 14 * f, 2)})
        ks["mand"].append({**base, "rot": round(sg * 26 * f, 2)})
        ey = max(0.002, math.tan(math.radians(ilus_03.ANG_MAX * f)) / TAN40)
        ks["boca"].append({**base, "rot": round(-sg * 14 * f, 2), "ey": round(ey, 4), "op": 0 if f < 0.03 else 1})
    exs = {"ex": -1} if espejo else {}
    return [IMG(f"perro_boca_{raza}", ancho=ancho, x=x, y=y, z=z - 0.02, keys=ks["boca"], **exs),
            IMG(f"perro_mand_{raza}", ancho=ancho, x=x, y=y, z=z - 0.01, keys=ks["mand"], **exs),
            IMG(f"perro_sup_{raza}", ancho=ancho, x=x, y=y, z=z, keys=ks["sup"], **exs)]


def _exs(k, ex):
    return [{**kk, "ex": ex} for kk in k] if ex != 1 else k


def entra(x, y, dy=200, t1=0.45, deriva=40):
    """posición para bostezo(): sube con muelle en t1 y luego deriva despacio."""
    def p(t):
        if t < t1:
            u = t / t1
            u = 1 - (1 - u) ** 3 * math.cos(u * 2.4)
            return x, y + dy * (1 - u)
        return x, y - deriva * (t - t1) / 3
    return p


def sil(n, x, y, ancho, abre=None, z=0.5, ex=1):
    """Silueta de persona; si abre=(t0, t1), bosteza entre t0 y t1 (cambia a la versión con la boca abierta)."""
    if not abre:
        return [IMG(n, ancho=ancho, x=x, y=y, z=z, **({"ex": ex} if ex != 1 else {}))]
    t0, t1 = abre
    a = [{"t": 0, "op": 1}, {"t": t0, "op": 1}, {"t": t0 + 0.06, "op": 0}, {"t": t1, "op": 0}, {"t": t1 + 0.06, "op": 1}]
    b = [{"t": 0, "op": 0}, {"t": t0, "op": 0}, {"t": t0 + 0.06, "op": 1, "rot": -4 * ex}, {"t": t1, "op": 1, "rot": -6 * ex}, {"t": t1 + 0.06, "op": 0}]
    exs = {"ex": ex} if ex != 1 else {}
    return [IMG(n, ancho=ancho, x=x, y=y, z=z, keys=a, **exs), IMG(n + "_b", ancho=ancho, x=x, y=y, z=z + 0.001, keys=b, **exs)]


def rejilla(d, t_cascada=None, bostezan=(), t_bos=None, gris=False, z=0.5):
    """29 perritos en 6 filas × 5 (sobra uno). bostezan = índices que pasan a bostezar en cascada desde t_bos."""
    els, r = [], random.Random(3)
    k = 0
    for fila in range(6):
        for col in range(5):
            if k == 29: break
            x, y = 150 + col * 195, 720 + fila * 170
            nom = "perrito2" if gris else ("perrito" if (fila + col) % 2 == 0 else "perrito2")
            base = aparece(t_cascada + k * 0.012, 0.3) if t_cascada is not None else []
            if k in bostezan:
                tb = t_bos + bostezan.index(k) * 0.05
                els.append(IMG(nom, ancho=190, x=x, y=y, z=z, keys=base + [{"t": tb, "op": 1}, {"t": tb + 0.05, "op": 0}]))
                els.append(IMG(nom + "_b", ancho=190, x=x, y=y, z=z + 0.01, keys=[{"t": 0, "op": 0}, {"t": tb, "op": 0}, {"t": tb + 0.05, "op": 1, "escala": 1.12},
                                                                                 {"t": tb + 0.3, "escala": 1.0, "ease": "elastico"}]))
                els.append(brillo(x, y, 110, "#b6ff5a", 0.0, z - 0.01, keys=[{"t": tb, "intensidad": 0}, {"t": tb + 0.1, "intensidad": 0.55}]))
            else:
                els.append(IMG(nom, ancho=190, x=x, y=y, z=z, keys=base, **({"op": 0.55} if gris else {})))
            k += 1
    return els


def fila(n_bos, color, t0=0.3):
    """10 personas en fila; las n_bos primeras bostezan (≈ el porcentaje del dato)."""
    els = []
    for k in range(10):
        x = 100 + k * 98
        if k < n_bos:
            els += [brillo(x, 860, 70, color, 0.0, 0.4, keys=[{"t": t0 + k * 0.12, "intensidad": 0}, {"t": t0 + k * 0.12 + 0.1, "intensidad": 0.6}]),
                    *sil("sil", x, 880, 120, abre=(t0 + k * 0.12, 99), z=0.5)]
        else:
            els.append(IMG("sil", ancho=120, x=x, y=880, z=0.5, op=0.45))
    return els


def anillo(x, y, rr, color, t0, i=1.0, grosor=8):
    return {"tipo": "forma", "forma": "elipse", "ancho": rr * 2, "alto": rr * 2, "relleno": "#ffffff", "op_relleno": 0, "grosor": grosor,
            "borde": color, "x": x, "y": y, "z": 0.3, "keys": [{"t": 0, "op": 0.25 * i}, {"t": t0, "op": 0.25 * i, "escala": 1.0},
                                                               {"t": t0 + 0.2, "op": 1, "escala": 1.06, "ease": "salida"}, {"t": t0 + 0.5, "escala": 1.0}]}


def barra(x, ancho, alto_final, color, t0, t1, z=0.5, y_base=1500):
    """Barra que crece hacia arriba desde y_base (con ey: la forma no anima su alto)."""
    h = alto_final
    ks = [{"t": 0, "ey": 0.002, "y": y_base}, {"t": max(0, t0), "ey": 0.002, "y": y_base}, {"t": t1, "ey": 1.0, "y": y_base - h / 2, "ease": "salida"}]
    if t0 < 0:
        ks = [{"t": 0, "ey": 1.0, "y": y_base - h / 2}]
    return {"tipo": "forma", "forma": "rect", "ancho": ancho, "alto": h, "relleno": color, "x": x, "y": y_base, "z": z, "keys": ks}




# ================================================================== PLANOS
@v.plano(0, "gancho: un perro enorme bostezando desde el fotograma 0")
def _(d):
    ap = [(0, 0.3), (0.9, 1.0), (1.7, 1.0), (d, 0.15)]
    return P(SALON, [BG("bg_salon"), brillo(760, 700, 500, "#ffd27a", 0.35, pulso=[0.1, 1.5]),
             *bostezo("dorado", 430, 1000, 1050, d, ap, pos=entra(430, 1000, 220)),
             polvo("#ffe2a0", 25, (0, 300, 1080, 1700), 2)],
             cam(1.0, 1.05, (540, 1000), (560, 980)), vineta=0.6, sfx=[(0.05, "rumor", -18, {"dur": 1.6}), (0.9, "brillo", -24)])


@v.plano(5, "bostezas (la persona, en silueta)")
def _(d):
    return P(SALON, [BG("bg_salon"), *sil("sil", 470, 1200, 980, abre=(0.15, d), z=0.5),
             IMG("perrito", ancho=420, x=880, y=1420, z=0.55, ex=-1)],
             cam(1.0, 1.05, (540, 1100), (520, 1080)), "desenfoque", sfx=[(0.15, "rumor", -20, {"dur": 0.8})])


@v.plano(6, "y él bosteza también (dálmata)")
def _(d):
    ap = [(0, 0.0), (0.35, 0.0), (1.0, 1.0), (d, 0.8)]
    return P(SALON, [BG("bg_salon"), *sil("sil", 180, 1300, 600, abre=(0, d), z=0.4),
             *bostezo("dalmata", 560, 1000, 980, d, ap), brillo(640, 900, 400, "#b6ff5a", 0.2)],
             cam(1.0, 1.05, (600, 1000), (620, 980)), "barrido", sfx=[(0.4, "rumor", -20, {"dur": 0.9})])


@v.plano(10, "en dos mil ocho")
def _(d):
    return P(["#141a2e", "#0a0e1a"], [IMG("calendario", ancho=560, x=540, y=1100, z=0.5, keys=aparece(0.0, 0.35)), polvo("#ffffff", 30, (0, 200, 1080, 1700), 5)],
             cam(1.0, 1.06), hud=[contador(0.05, d - 0.05, 2000, 2008, d * 0.6, "", tam=150, y=560, borde=CIAN, miles=False)], sfx=[(0.05, "tic", -18)])


@v.plano(14, "en Londres")
def _(d):
    return P(["#1a1440", "#0a0a1a"], [BG("bg_londres"), brillo(760, 980, 300, "#ffd27a", 0.4)],
             cam(1.0, 1.06, (540, 1000), (560, 990)), "barrido", hud=[rotulo(0.05, d - 0.05, "LONDRES", tam=110, color="#ffffff", capsula="#c0392be6", y=560)])


@v.plano(16, "un equipo bostezó delante del perro")
def _(d):
    return P(LAB, [BG("bg_lab"), *sil("sil", 330, 1180, 800, abre=(0.25, d - 0.1), z=0.5),
             IMG("perrito2", ancho=560, x=820, y=1360, z=0.55, ex=-1, keys=aparece(0.0, 0.35)),
             brillo(330, 1000, 360, "#7df9ff", 0.25), polvo("#7df9ff", 30, (0, 400, 1080, 1600), 6)],
             cam(1.0, 1.06, (560, 1150), (560, 1120)), "desenfoque", sfx=[(0.25, "rumor", -20, {"dur": 0.8})])


@v.plano(21, "micro: veintinueve")
def _(d):
    return P(LAB, [brillo(540, 960, 520, "#7df9ff", 0.5, pulso=[0.2, 0.2]), IMG("perrito", ancho=700, x=540, y=1150, z=0.5, keys=aparece(0.0, 0.25))],
             cam(1.1, 1.18), "corte", hud=[rotulo(0.0, d, "29", tam=200, color="#ffffff", capsula="#0d1330d8", borde=CIAN, y=560, fijo=True)], sfx=[(0.0, "pop", -16)])


@v.plano(22, "micro: los veintinueve perros aparecen en cascada")
def _(d):
    return P(LAB, [brillo(540, 1150, 700, "#7df9ff", 0.2), *rejilla(d, t_cascada=0.0)],
             cam(1.0, 1.03, (540, 1150)), "corte", sfx=[(0.05, "pop", -20), (0.25, "pop", -22)])


@v.plano(23, "y veintiuno bostezaron")
def _(d):
    rr = random.Random(9)
    idx = sorted(rr.sample(range(29), 21), key=lambda k: rr.random())
    return P(LAB, [brillo(540, 1150, 700, "#7df9ff", 0.2), *rejilla(d, bostezan=idx, t_bos=0.15)],
             cam(1.12, 1.08, (540, 1150), (540, 1150)),
             hud=[contador(0.1, d - 0.05, 0, 21, 1.1, "DE 29", tam=110, y=560, borde=LIMA)], sfx=[(0.15, "subida", -18, {"dur": 1.0}), (1.2, "impacto", -14)],
             energia=0.85)


@v.plano(26, "cuando solo abrían la boca sin bostezar")
def _(d):
    return P(LAB, [BG("bg_lab"), IMG("sil_b", ancho=780, x=330, y=1180, z=0.5, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": -2}]),
             *[IMG("perrito2", ancho=300, x=x, y=1480, z=0.55, ex=-1, keys=[{"t": 0, "y": 1480}, {"t": d * 0.5, "y": 1472}, {"t": d, "y": 1480}]) for x in (720, 920)],
             IMG("perrito", ancho=300, x=820, y=1260, z=0.52, ex=-1),
             senala(470, 1100, 0.3, d - 0.1, 90, MAGENTA)],
             cam(1.0, 1.05, (540, 1200), (560, 1180)), "desenfoque",
             hud=[rotulo(0.0, d, "LA BOCA", tam=96, color="#ffffff", capsula="#0d1330d8", borde=MAGENTA, y=560)])


@v.plano(33, "ninguno")
def _(d):
    return P(["#1a0610", "#0a0206"], [*rejilla(d, gris=True), brillo(540, 1150, 600, "#ff3df2", 0.25)],
             cam(1.04, 1.0, (540, 1150)), "corte", hud=[rotulo(0.0, d, "NINGUNO", tam=120, color="#ffffff", capsula="#c0392be6", y=560, fijo=True)],
             sfx=[(0.0, "golpe", -14)])


@v.plano(34, "¿y a nosotros? (vagón)")
def _(d):
    return P(["#2a2438", "#141018"], [BG("bg_vagon"), *sil("sil", 250, 1130, 560, z=0.5), *sil("sil_m", 560, 1150, 540, z=0.52),
             *sil("sil_a", 860, 1130, 560, z=0.5), brillo(540, 700, 500, "#ff7ad8", 0.2, pulso=[0.1, 1.2])],
             cam(1.0, 1.05, (540, 1000), (540, 980)), "barrido", hud=[rotulo(0.1, d - 0.05, "¿Y NOSOTROS?", tam=100, color=AMBAR, capsula=None, y=560)],
             sfx=[(0.05, "rumor", -24, {"dur": d})])


@v.plano(37, "más o menos la mitad")
def _(d):
    els = []
    for k in range(6):
        x, y = 200 + (k % 3) * 340, 900 + (k // 3) * 460
        if k in (0, 2, 4):
            els += [brillo(x, y - 40, 170, "#b6ff5a", 0.0, 0.4, keys=[{"t": 0.15 + k * 0.05, "intensidad": 0}, {"t": 0.3 + k * 0.05, "intensidad": 0.5}]),
                    *sil("sil_a", x, y, 360, abre=(0.15 + k * 0.05, d), z=0.5)]
        else:
            els.append(IMG("sil", ancho=360, x=x, y=y, z=0.5, op=0.45))
    return P(["#0a0e1a", "#06080e"], els, cam(1.0, 1.04, (540, 1100)), "corte",
             hud=[rotulo(0.05, d - 0.05, "LA MITAD", tam=120, color="#141414", capsula="#b6ff5ae6", y=560)], sfx=[(0.1, "pop", -18), (0.2, "rumor", -24, {"dur": 0.8})])


@v.plano(44, "los adultos se contagian en cadena al ver un bostezo")
def _(d):
    paso = d / 4.5
    return P(["#2a2438", "#141018"], [BG("bg_vagon"),
             *sil("sil", 220, 1130, 520, abre=(0.1, 0.1 + paso * 1.6), z=0.5), *sil("sil_m", 540, 1150, 500, abre=(0.1 + paso, 0.1 + paso * 2.6), z=0.52),
             *sil("sil_a", 860, 1130, 520, abre=(0.1 + paso * 2, d), z=0.5),
             flecha([[330, 900], [430, 880]], 0.1 + paso * 0.6, 0.1 + paso, LIMA, 7), flecha([[650, 900], [750, 880]], 0.1 + paso * 1.6, 0.1 + paso * 2, LIMA, 7)],
             cam(1.0, 1.05, (540, 1050), (560, 1030)), "desenfoque", sfx=[(0.1, "rumor", -22, {"dur": 0.6}), (0.1 + paso, "rumor", -22, {"dur": 0.6}), (0.1 + paso * 2, "rumor", -22, {"dur": 0.6})])


@v.plano(51, "a veces basta con…")
def _(d):
    return P(["#0a1020", "#06080e"], [*sil("sil", 360, 1200, 760, abre=(0.0, d), z=0.5),
             IMG("onda", ancho=500, x=760, y=1050, z=0.55, keys=[{"t": 0, "escala": 0.5, "op": 1}, {"t": d, "escala": 1.3, "op": 0.3}])],
             cam(1.0, 1.05), "corte", sfx=[(0.05, "rumor", -22, {"dur": 0.8})])


@v.plano(55, "oírlo")
def _(d):
    return P(["#2a1c2a", "#120a14"], [IMG("oreja", ancho=820, x=600, y=1050, z=0.5, keys=aparece(0.0, 0.3)),
             *[IMG("onda", ancho=380 + k * 120, x=260, y=1050, z=0.55, keys=[{"t": 0.05 * k, "op": 0, "escala": 0.6}, {"t": 0.05 * k + 0.1, "op": 1}, {"t": d, "op": 0.2, "escala": 1.2}]) for k in range(3)]],
             cam(1.0, 1.06), "corte", hud=[amarillo(0.05, d - 0.02, "OÍRLO", y=560, color=CIAN)], sfx=[(0.05, "senal", -24)])


@v.plano(56, "micro: leerlo")
def _(d):
    return P(["#1a1420", "#0a0810"], [brillo(540, 1050, 500, "#ffd27a", 0.35), IMG("libro", ancho=900, x=540, y=1100, z=0.5, keys=[{"t": 0, "ey": 0.2}, {"t": 0.25, "ey": 1.0, "ease": "elastico"}]),
             IMG("perrito_b", ancho=260, x=740, y=1050, z=0.55, keys=aparece(0.15, 0.3))],
             cam(1.06, 1.12), "corte", hud=[amarillo(0.0, d, "LEERLO", y=560, color=AMBAR)], sfx=[(0.02, "roce", -18)])


@v.plano(57, "o pensarlo")
def _(d):
    return P(PIEL, [IMG("cara_perfil", ancho=900, x=640, y=1300, z=0.5),
             IMG("bocadillo", ancho=620, x=330, y=760, z=0.6, keys=aparece(0.05, 0.35)),
             IMG("perrito_b", ancho=300, x=320, y=740, z=0.65, keys=aparece(0.25, 0.3) + late(0.6, 1, 0.1, 0.3))],
             cam(1.0, 1.05, (540, 1000), (520, 980)), "desenfoque", hud=[rotulo(0.05, d - 0.05, "PENSARLO", tam=96, color="#ffffff", capsula="#ff3df2d8", y=560)], sfx=[(0.05, "pop", -18)])


@v.plano(59, "puede que ya estés bostezando (móvil en la mano)")
def _(d):
    ap = [(0, 0.0), (0.5, 0.0), (1.2, 1.0), (d, 0.9)]
    return P(["#141428", "#06060e"], [brillo(540, 900, 500, "#7df9ff", 0.25),
             IMG("movil_mano", ancho=860, x=560, y=1180, z=0.4),
             *bostezo("beagle", 520, 1020, 430, d, ap, z=0.5), polvo("#7df9ff", 20, (0, 300, 1080, 1700), 7)],
             cam(1.0, 1.08, (540, 1050), (540, 1000)), "zoom", sfx=[(0.5, "rumor", -20, {"dur": 1.0})])


@v.plano(64, "¿y para qué sirve? (perro negro)")
def _(d):
    ap = [(0, 0.1), (0.6, 1.0), (d, 0.6)]
    return P(["#0a0a1e", "#04040c"], [brillo(560, 900, 600, "#c8b8ff", 0.35), *bostezo("negro", 520, 1050, 1200, d, ap, pos=lambda t: (520 - 20 * t, 1050)),
             polvo("#c8b8ff", 25, (0, 300, 1080, 1700), 8)],
             cam(1.0, 1.05), "desenfoque", hud=[rotulo(0.1, d - 0.05, "¿PARA QUÉ?", tam=110, color=AMBAR, capsula=None, y=560)], sfx=[(0.1, "rumor", -20, {"dur": 1.0})])


@v.plano(68, "una idea: enfría el cerebro")
def _(d):
    return P(LAB, [brillo(540, 1100, 600, "#ff7ad8", 0.3), IMG("cerebro", ancho=880, x=540, y=1150, z=0.5, keys=aparece(0.0, 0.35), anim={"balanceo": [2, 1.5]}),
             {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": "#5ad8ff", "x": 540, "y": 960, "z": 0.55,
              "keys": [{"t": 0, "op": 0}, {"t": d, "op": 0.18}]},
             *[IMG("copo", ancho=90, z=0.6, keys=[{"t": 0.2 + k * 0.15, "x": -60, "y": 900 + k * 70, "op": 0}, {"t": 0.3 + k * 0.15, "op": 1},
                                                  {"t": d, "x": 300 + k * 60, "y": 1000 + k * 40, "rot": 180}]) for k in range(6)],
             flecha([[60, 1200], [300, 1160]], 0.3, d * 0.8, CIAN, 9)],
             cam(1.0, 1.06), hud=[amarillo(0.1, d - 0.05, "ENFRÍA", y=560, color=CIAN)], sfx=[(0.3, "roce", -18), (0.6, "brillo", -22)])


@v.plano(75, "como un ventilador")
def _(d):
    return P(LAB, [brillo(700, 1100, 500, "#ff7ad8", 0.25), IMG("cerebro", ancho=700, x=720, y=1150, z=0.45),
             IMG("ventilador", ancho=560, x=240, y=1050, z=0.55, keys=aparece(0.0, 0.3), anim={"girar": 720}),
             *[flecha([[420, 960 + k * 90], [560, 960 + k * 90]], 0.15 + k * 0.08, 0.6 + k * 0.08, CIAN, 6) for k in range(3)],
             polvo("#bfe9ff", 40, (300, 800, 900, 1400), 9)],
             cam(1.0, 1.05), "corte", hud=[amarillo(0.1, d - 0.05, "VENTILADOR", y=560, color=CIAN, tam=90)], sfx=[(0.05, "whoosh", -14, {"dur": 0.8})])


@v.plano(81, "con una bolsa fría en la frente")
def _(d):
    return P(PIEL, [IMG("cara_perfil", ancho=1000, x=600, y=1300, z=0.5),
             IMG("bolsa_hielo", ancho=420, z=0.6, rot=-25, keys=[{"t": 0, "x": 300, "y": 300}, {"t": d * 0.55, "x": 450, "y": 900, "ease": "elastico"}, {"t": d, "x": 450, "y": 910}]),
             *[IMG("copo", ancho=70, x=x, y=y, z=0.62, keys=[{"t": d * 0.55, "op": 0}, {"t": d * 0.6, "op": 1}, {"t": d, "op": 0, "y": y + 120}]) for x, y in [(360, 1000), (540, 990), (450, 1040)]],
             brillo(450, 920, 260, "#7df9ff", 0.0, 0.55, keys=[{"t": d * 0.5, "intensidad": 0}, {"t": d * 0.65, "intensidad": 0.5}])],
             cam(1.0, 1.06, (540, 1000), (500, 940)), hud=[rotulo(0.1, d - 0.05, "BOLSA FRÍA", tam=100, color="#ffffff", capsula="#2a6ab0e6", y=560)],
             sfx=[(d * 0.55, "golpe", -20), (d * 0.6, "brillo", -22)])


@v.plano(88, "solo bostezó el nueve por ciento")
def _(d):
    return P(LAB, [{"tipo": "forma", "forma": "rect", "ancho": 900, "alto": 6, "relleno": "#ffffff", "x": 540, "y": 1503, "z": 0.4},
             barra(330, 260, 900 * 0.09 * 2.4, "#5ad8ff", 0.2, 1.0), IMG("bolsa_hielo", ancho=260, x=330, y=1640, z=0.5),
             *fila(1, "#7df9ff"),
             brillo(330, 1400, 200, "#7df9ff", 0.4), polvo("#bfe9ff", 25, (0, 400, 1080, 1600), 10)],
             cam(1.0, 1.04, (540, 1200)), "corte", hud=[contador(0.1, d - 0.05, 0, 9, 0.8, "%", tam=150, y=560, borde=CIAN)],
             sfx=[(0.2, "subida", -20, {"dur": 0.7}), (0.95, "pop", -16)])


@v.plano(94, "al ver vídeos de bostezos (pared de pantallas)")
def _(d):
    els = []
    for k in range(6):
        x, y = 280 + (k % 2) * 520, 760 + (k // 2) * 360
        els.append({"tipo": "forma", "forma": "rect", "ancho": 470, "alto": 310, "relleno": "#0b1226", "borde": CIAN, "grosor": 5, "x": x, "y": y, "z": 0.4})
        els += sil("sil" if k % 2 else "sil_m", x, y + 20, 300, abre=(0.1 + k * 0.12, d), z=0.45)
    return P(LAB, els + [brillo(540, 1100, 600, "#7df9ff", 0.15)], cam(1.0, 1.05), "desenfoque",
             hud=[rotulo(0.1, d - 0.05, "VÍDEOS DE BOSTEZOS", tam=72, color="#ffffff", capsula="#0d1330d8", borde=CIAN, y=560)], sfx=[(0.1, "senal", -24)])


@v.plano(99, "con una bolsa templada")
def _(d):
    return P(["#2a1410", "#120806"], [IMG("cara_perfil", ancho=1000, x=600, y=1300, z=0.5),
             IMG("bolsa_templada", ancho=420, z=0.6, rot=-25, keys=[{"t": 0, "x": 300, "y": 300}, {"t": d * 0.55, "x": 450, "y": 900, "ease": "elastico"}, {"t": d, "x": 450, "y": 910}]),
             brillo(450, 920, 280, "#ffb070", 0.0, 0.55, keys=[{"t": d * 0.5, "intensidad": 0}, {"t": d * 0.65, "intensidad": 0.6}])],
             cam(1.0, 1.06, (540, 1000), (500, 940)), "barrido", hud=[rotulo(0.1, d - 0.05, "TEMPLADA", tam=110, color="#141414", capsula="#ffb070e6", y=560)],
             sfx=[(d * 0.55, "golpe", -20)])


@v.plano(103, "el cuarenta y uno por ciento")
def _(d):
    return P(["#1a0e0a", "#0a0604"], [{"tipo": "forma", "forma": "rect", "ancho": 900, "alto": 6, "relleno": "#ffffff", "x": 540, "y": 1503, "z": 0.4},
             *fila(4, "#ffb070", 0.2), barra(330, 260, 900 * 0.09 * 2.4, "#5ad8ff", -1, 0.0), barra(750, 260, 900 * 0.41 * 2.4, "#ff8a3a", 0.1, 1.2),
             IMG("bolsa_hielo", ancho=220, x=330, y=1630, z=0.5), IMG("bolsa_templada", ancho=220, x=750, y=1630, z=0.5),
             brillo(750, 1100, 300, "#ffb070", 0.4)],
             cam(1.0, 1.04, (540, 1200)), "corte", hud=[contador(0.1, d - 0.05, 9, 41, 1.0, "%", tam=150, y=560, borde=AMBAR)],
             sfx=[(0.1, "subida", -18, {"dur": 1.0}), (1.15, "impacto", -14)], energia=0.85)


@v.plano(109, "respirando solo por la nariz")
def _(d):
    return P(PIEL, [IMG("cara_perfil", ancho=1500, x=760, y=1350, z=0.5),
             *[flecha([[40, 1120 + k * 60], [300, 1200 + k * 30]], 0.1 + k * 0.1, 0.8 + k * 0.1, CIAN, 7) for k in range(3)],
             senala(370, 1235, 0.3, d - 0.05, 80, CIAN)],
             cam(1.0, 1.06, (540, 1100), (500, 1120)), "desenfoque", hud=[rotulo(0.1, d - 0.05, "POR LA NARIZ", tam=90, color="#ffffff", capsula="#0d1330d8", borde=CIAN, y=560)],
             sfx=[(0.1, "roce", -18), (0.6, "roce", -20)])


@v.plano(115, "nadie se contagió")
def _(d):
    els = [IMG("sil" if k % 2 else "sil_a", ancho=330, x=190 + k * 233, y=1250, z=0.5,
               keys=[{"t": 0, "rot": 0}, {"t": 0.3 + k * 0.1, "rot": 5}, {"t": 0.6 + k * 0.1, "rot": -5}, {"t": 0.9 + k * 0.1, "rot": 0}]) for k in range(4)]
    return P(["#1a0610", "#0a0206"], els + [brillo(540, 1150, 600, "#ff3df2", 0.25, pulso=[0.15, 0.5]),
             {"tipo": "forma", "forma": "rect", "ancho": 1000, "alto": 14, "relleno": MAGENTA, "x": 540, "y": 1050, "z": 0.6, "rot": -8,
              "keys": [{"t": 0.1, "ex": 0.01}, {"t": 0.45, "ex": 1.0, "ease": "salida"}]}],
             cam(1.1, 1.0, (540, 1150), (540, 1150), temblor=3), "corte", hud=[rotulo(0.0, d - 0.05, "NADIE", tam=150, color="#ffffff", capsula="#c0392be6", y=560)],
             sfx=[(0.0, "golpe", -14), (0.3, "roce", -20)])


def circulos(d, activo):
    cols = [LIMA, CIAN, MAGENTA]
    els = [anillo(540, 1150, r_, c, (0.15 if k == activo else 99), 1.0, 9) for k, (r_, c) in enumerate(zip((190, 340, 490), cols))]
    els += sil("sil", 500, 1150, 210, z=0.5) + sil("sil_m", 600, 1170, 190, z=0.51)
    els += sil("sil_a", 240, 980, 170, z=0.5) + sil("sil_a", 820, 940, 170, z=0.5) + sil("sil", 300, 1420, 160, z=0.5)
    els += [IMG("sil", ancho=130, x=x, y=y, z=0.5, op=0.6) for x, y in [(100, 760), (960, 1380), (540, 640), (980, 760), (120, 1500)]]
    return els


@v.plano(118, "¿con quién se pega más?")
def _(d):
    return P(["#0a0e1a", "#06080e"], circulos(d, -1), cam(1.12, 1.0, (700, 1000), (540, 1150)), "desenfoque",
             hud=[rotulo(0.1, d - 0.05, "¿CON QUIÉN?", tam=110, color=AMBAR, capsula=None, y=560)], sfx=[(0.1, "pop", -20)])


@v.plano(123, "primero, la familia")
def _(d):
    return P(["#0a0e1a", "#06080e"], circulos(d, 0) + [brillo(540, 1150, 220, "#b6ff5a", 0.35)], cam(1.6, 1.7, (550, 1160)), "corte",
             hud=[rotulo(0.1, d - 0.05, "FAMILIA", tam=110, color="#141414", capsula="#b6ff5ae6", y=560)], sfx=[(0.15, "ding", -20)])


@v.plano(127, "luego, los amigos")
def _(d):
    return P(["#0a0e1a", "#06080e"], circulos(d, 1) + [brillo(540, 1150, 380, "#7df9ff", 0.25)], cam(1.3, 1.2, (540, 1150)), "corte",
             hud=[rotulo(0.1, d - 0.05, "AMIGOS", tam=110, color="#141414", capsula="#7df9ffe6", y=560)], sfx=[(0.15, "ding", -22, {"f": 660})])


@v.plano(131, "por último, los desconocidos")
def _(d):
    return P(["#0a0e1a", "#06080e"], circulos(d, 2) + [brillo(540, 1150, 540, "#ff3df2", 0.18)], cam(0.0 + 1.0, 1.08, (540, 1150), (600, 1100)), "corte",
             hud=[rotulo(0.1, d - 0.05, "DESCONOCIDOS", tam=96, color="#ffffff", capsula="#ff3df2d8", y=560)], sfx=[(0.15, "ding", -24, {"f": 440})])


@v.plano(137, "incluso los bebés bostezan antes de nacer (ecografía)")
def _(d):
    return P(["#05080c", "#0a0e14"], [IMG("ecografia", ancho=1000, x=540, y=1100, z=0.5, keys=aparece(0.0, 0.4) + [{"t": d, "escala": 1.06, "ease": "suave"}]),
             brillo(540, 1150, 400, "#7df9ff", 0.15, pulso=[0.15, 0.8]),
             senala(685, 1160, 0.9, d - 0.05, 70, CIAN), polvo("#bfe9ff", 25, (100, 600, 980, 1600), 11)],
             cam(1.0, 1.06, (540, 1100), (580, 1100)), "desenfoque",
             hud=[rotulo(0.05, d - 0.05, "BEBÉS", tam=110, color="#ffffff", capsula="#0d1330d8", borde=CIAN, y=560)], sfx=[(0.1, "senal", -22), (0.9, "brillo", -22)])


@v.plano(144, "ahora mira a tu perro y bosteza")
def _(d):
    return P(SALON, [BG("bg_salon"), *sil("sil", 300, 1220, 820, abre=(d * 0.55, d), z=0.5),
             IMG("perrito", ancho=520, x=840, y=1420, z=0.55, ex=-1, keys=[{"t": 0, "rot": 0}, {"t": d * 0.5, "rot": 4}, {"t": d, "rot": 0}])],
             cam(1.0, 1.05, (540, 1150), (560, 1130)), "desenfoque", hud=[amarillo(0.1, d - 0.05, "BOSTEZA", y=560, color=AMBAR)], sfx=[(d * 0.55, "rumor", -20, {"dur": 0.8})])


@v.plano(151, "¿te lo devolvió? (beagle)")
def _(d):
    ap = [(0, 0.0), (0.25, 0.0), (0.8, 1.0), (d, 0.9)]
    return P(SALON, [BG("bg_salon"), *bostezo("beagle", 450, 1020, 1050, d, ap, pos=entra(450, 1020, 120, 0.3, 30)),
             brillo(600, 900, 400, "#ffd27a", 0.25)],
             cam(1.0, 1.05, (560, 1000)), "corte", hud=[rotulo(0.0, d, "¿TE LO DEVOLVIÓ?", tam=84, color="#ffffff", capsula="#0d1330d8", borde=AMBAR, y=560)],
             sfx=[(0.3, "rumor", -18, {"dur": 0.9})])


@v.plano(154, "cierre: el perro dorado vuelve a bostezar (bucle con el gancho)")
def _(d):
    ap = [(0, 0.0), (d * 0.45, 0.0), (d, 0.3)]
    return P(SALON, [BG("bg_salon"), brillo(760, 700, 500, "#ffd27a", 0.35, pulso=[0.1, 1.5]),
             *bostezo("dorado", 430, 1000, 1050, d, ap, pos=lambda t: (430, 1000 + 40 * (1 - t / d))),
             polvo("#ffe2a0", 25, (0, 300, 1080, 1700), 2)],
             cam(1.1, 1.0, (540, 1000), (540, 1000)), "corte", sfx=[(d * 0.5, "rumor", -20, {"dur": 1.0})], energia=0.4)


@v.plano(30, "micro: solo la boca abierta")
def _(d):
    return P(LAB, [IMG("sil_b", ancho=2000, x=100, y=1244, z=0.5, keys=[{"t": 0, "escala": 1.0}, {"t": 0.6, "escala": 1.04}]), senala(600, 1150, 0.05, d - 0.05, 120, MAGENTA)],
             cam(1.0, 1.06, (500, 1150)), "corte", sfx=[(0.05, "pop", -20)])


@v.plano(114, "micro: la nariz")
def _(d):
    return P(PIEL, [IMG("cara_perfil", ancho=3200, x=1379, y=1256, z=0.5),
             *[flecha([[0, 900 + k * 90], [430, 980 + k * 30]], 0.0 + k * 0.05, 0.4 + k * 0.05, CIAN, 9) for k in range(3)]],
             cam(1.0, 1.05), "corte", sfx=[(0.02, "roce", -18)])


@v.plano(140, "micro: el bebé bosteza")
def _(d):
    return P(["#05080c", "#0a0e14"], [IMG("ecografia", ancho=2600, x=150, y=844, z=0.5, keys=[{"t": 0, "escala": 1.0}, {"t": 0.6, "escala": 1.05}]), brillo(540, 1000, 260, "#7df9ff", 0.3),
             senala(540, 1000, 0.05, d - 0.05, 120, CIAN)], cam(1.0, 1.06, (540, 1000)), "corte", sfx=[(0.05, "brillo", -22)])


@v.plano(31, "sin bostezar: los perros, tranquilos")
def _(d):
    return P(LAB, [BG("bg_lab"), *[IMG("perrito2", ancho=330, x=x, y=y, z=0.55, ex=-1, keys=[{"t": 0, "rot": 0}, {"t": d * 0.5, "rot": 3}, {"t": d, "rot": 0}])
                                   for x, y in [(280, 1350), (560, 1300), (840, 1360)]],
             polvo("#7df9ff", 30, (0, 400, 1080, 1600), 12)],
             cam(1.06, 1.0, (560, 1250)), "corte", hud=[rotulo(0.0, d, "SIN BOSTEZAR", tam=90, color="#ffffff", capsula="#0d1330d8", borde=MAGENTA, y=560)],
             sfx=[(0.1, "roce", -22)])


@v.plano(141, "antes de nacer")
def _(d):
    return P(["#05080c", "#0a0e14"], [IMG("ecografia", ancho=900, x=540, y=1150, z=0.5, keys=[{"t": 0, "escala": 1.08}, {"t": d, "escala": 1.0, "ease": "suave"}]),
             brillo(540, 1150, 400, "#7df9ff", 0.15, pulso=[0.15, 0.8]), polvo("#bfe9ff", 25, (100, 600, 980, 1600), 13)],
             cam(1.0, 1.04, (540, 1150)), "desenfoque",
             hud=[rotulo(0.05, d - 0.05, "ANTES DE NACER", tam=90, color="#ffffff", capsula="#0d1330d8", borde=CIAN, y=560)], sfx=[(0.1, "senal", -24)])


v.construir("2026-11-18-manana-03-bostezo", version=1, bucle=0.35, musica={"generar": "curiosidad", "semilla": 31, "db": -13},
            claves=["perro", "bostezos", "veintinueve", "veintiuno", "ninguno", "mitad", "cerebro", "ventilador", "nueve", "cuarenta", "nariz", "nadie", "familia", "bebés"])
