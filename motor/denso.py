"""Método «denso» (DECISIONS 2026-11-16): montaje por planos atados a palabras del guion. Guía: `motor/DENSO.md`.

Uso típico en el generador de un vídeo (ver `lotes/prueba-luna-densa/gen.py`, el ejemplo completo):

    from motor.denso import *
    v = Video(DIR_SALIDA, "guion.txt", audio="NN-locucion.mp3", alineacion="NN-alineacion.json")   # sin audio → tiempos provisionales

    @v.plano(0, "gancho")                       # empieza en la palabra 0 del guion
    def _(d):                                   # d = duración real del plano en segundos
        return P(fondo, [elementos...], cam(...), hud=[rótulos...], sfx=[(t, "golpe", -12)])

    v.construir("2026-11-17-manana-01-slug", claves=[...], musica={"generar": "curiosidad", "semilla": 3})

Qué hace solo:
- cortes en palabras (`v.w(i)`); las claves de animación en fracción del plano con `K(d, (0, {...}), (1, {...}))`;
- control de lectura (cada texto ≥ 0,25 s + 1 s por 17 letras): avisa con ⚠ y `construir` devuelve la lista;
- halo neón bajo flechas y órbitas; «pop» al aparecer cada rótulo; whoosh de transición como mucho cada 5 s y muy bajo;
- un tic por raya en las líneas discontinuas y el soplo de las estrellas fugaces;
- `recorrido(T0, T1, p0, p1, d)`: detalles de fondo que se mueven con el tiempo ABSOLUTO del vídeo y siguen de un plano a otro.
"""
import json, os, random, shutil, subprocess

from .tiempos import palabras_de_alineacion

AQUI = os.path.dirname(os.path.abspath(__file__))
CIAN, MAGENTA, LIMA, AMBAR = "#2ff3ff", "#ff3df2", "#7dff3a", "#ffe93d"  # neones para fondos oscuros
ESPACIO = ["#02030a", "#0a1030"]
LEER = lambda txt: 0.25 + len(txt) / 17  # segundos mínimos para leer un texto (una cifra suelta: ~0,3 s)

_V = None  # vídeo que se está construyendo (lo usan flecha, fugaz, recorrido y fx)


# ------------------------------------------------------------------ piezas básicas (del estilo v4)
def IMG(n, **k): return {"tipo": "imagen", "archivo": f"svg/{n}.svg", **k}
def BG(n, z=0.05, ancho=1180): return IMG(n, ancho=ancho, x=540, y=960, z=z)


def polvo(color="#fff1c8", n=40, area=(0, 300, 1080, 1700), sem=1, clase="polvo"):
    return {"tipo": "particulas", "clase": clase, "color": color, "area": list(area), "n": n, "tam": [2, 5],
            "vel": [6, -10], "z": 0.9, "semilla": sem}


def brillo(x, y, r, color, i=0.5, z=0.06, pulso=None, keys=None):
    b = {"tipo": "brillo", "x": x, "y": y, "radio": r, "color": color, "intensidad": i, "z": z}
    if pulso: b["anim"] = {"pulso": pulso}
    if keys: b["keys"] = keys
    return b


def cam(z0, z1, f0=(540, 960), f1=None, temblor=0):
    return {"zoom": [z0, z1], "foco": [list(f0), list(f1 or f0)], "pan": [[0, 0], [0, 0]], "temblor": temblor}


def P(fondo, els, camara, entrada="corte", dur_entrada=0.3, vineta=0.55, hud=(), sfx=()):
    """Un plano: fondo [arriba, abajo], elementos, cámara, entrada (corte|desenfoque|zoom|barrido),
    rótulos `hud` y sonidos `sfx` = [(t dentro del plano, tipo, dB[, {opciones}])]."""
    return dict(fondo=fondo, els=els, cam=camara, entrada=entrada, dur=dur_entrada, vineta=vineta, hud=list(hud), sfx=list(sfx))


def K(d, *pares):
    """Claves en FRACCIÓN de la duración del plano: K(d, (0, {...}), (0.6, {...}))."""
    return [{"t": round(f * d, 3), **v} for f, v in pares]


# ------------------------------------------------------------------ rótulos
def rotulo(t0, t1, texto="", **k):
    ks = [{"t": t0, "escala": 0.0, "op": 0}, {"t": t0 + 0.05, "op": 1}, {"t": t0 + min(0.25, (t1 - t0) / 3), "escala": 1.0, "ease": "rebote"},
          {"t": t1, "escala": 1.0, "op": 1}, {"t": t1 + 0.15, "op": 0}]
    return {"tipo": "rotulo", "texto": texto, "hud": True, "z": 1, "keys": ks, **k}


def amarillo(t0, t1, texto, y=1360, tam=96, color="#ffd23f"):
    """Palabra clave grande e inclinada, sin cápsula. Sobre fondos oscuros, pásale un neón (CIAN, MAGENTA, LIMA)."""
    return rotulo(t0, t1, texto, tam=tam, color=color, capsula=None, rot=-6, x=540, y=y)


def contexto(t0, t1, texto):
    """Etiqueta roja de contexto arriba (y=470)."""
    return rotulo(t0, t1, texto, tam=54, color="#ffffff", capsula="#c0392be6", borde="#ffffff30", x=540, y=470)


def contador(t0, t1, desde, hasta, dur, unidad="", **k):
    """Cifra que corre. Opciones del rótulo: decimales, contar_prefijo, miles=False (años), borde, capsula…"""
    tam, x, y = k.pop("tam", 120), k.pop("x", 540), k.pop("y", 1450)
    return {**rotulo(t0, t1, "", tam=tam, x=x, y=y, **k), "contar": [desde, hasta, dur], "contar_desde": t0, "unidad": unidad}


# ------------------------------------------------------------------ sonido y piezas con estado
def fx(t, tipo, db=-14, **k):
    """Efecto de sonido en el segundo ABSOLUTO t (tipos en `motor/sfx.py`)."""
    _V.FX.append({"t": round(t, 3), "tipo": tipo, "db": db, **k})


def fx_espaciado(clave, t, tipo, db, separacion, **k):
    """Como fx, pero solo si han pasado `separacion` s desde el último de esa `clave` (para sonidos que se repiten)."""
    if t - _V.ultimo.get(clave, -99) >= separacion:
        fx(t, tipo, db, **k)
        _V.ultimo[clave] = t
        return True
    return False


def flecha(pts, t0, t1, color="#ffffffcc", g=8, disc=None, punta=True, z=0.5):
    """Flecha/trazo que se dibuja entre t0 y t1 (s del plano). Con `disc=[raya, hueco]` suena un tic por raya.
    Regla: la punta nunca acaba dentro del objeto al que sigue (el objeto va por delante)."""
    f = {"tipo": "flecha", "puntos": pts, "grosor": g, "color": color, "punta": punta, "z": z,
         "keys": [{"t": t0, "progreso": 0}, {"t": t1, "progreso": 1, "ease": "salida"}]}
    if disc:
        f["discontinua"] = disc
        largo = sum(((pts[i + 1][0] - pts[i][0]) ** 2 + (pts[i + 1][1] - pts[i][1]) ** 2) ** 0.5 for i in range(len(pts) - 1))
        n = int(min(8, max(3, largo / (disc[0] + disc[1]) / 2)))  # un tic blando por raya (máx. 8 para no saturar)
        for i in range(n):
            fx(_V.ini + t0 + (t1 - t0) * (i / n) ** 1.4, "trazo", -27, f=820 + 55 * i)
    return f


def fugaz(t0, x0, y0, x1, y1, z=0.12):
    """Estrella fugaz lenta (se dibuja en 0,7 s y se apaga en 1,6 s), con su soplo."""
    fx(_V.ini + t0, "fugaz", -25, pan=round((x0 + x1) / 1080 - 1, 2))
    return {"tipo": "flecha", "puntos": [[x0, y0], [x1, y1]], "grosor": 3, "color": "#ffffffee", "punta": False, "z": z,
            "keys": [{"t": t0, "progreso": 0, "op": 1}, {"t": t0 + 0.7, "progreso": 1}, {"t": t0 + 1.0, "op": 1}, {"t": t0 + 1.6, "op": 0}]}


def recorrido(T0, T1, p0, p1, d, esc=None):
    """Claves de un objeto que cruza la pantalla entre los segundos ABSOLUTOS T0 y T1 (de p0 a p1).
    Como depende del tiempo del vídeo y no del plano, sigue en el mismo sitio de un plano al siguiente.
    Da T0/T1 con `v.w(i)` (palabras), no con segundos fijos."""
    def en(T):
        u = min(max((T - T0) / (T1 - T0), 0), 1)
        k = {"x": p0[0] + (p1[0] - p0[0]) * u, "y": p0[1] + (p1[1] - p0[1]) * u, "op": 1 if T0 <= T <= T1 else 0}
        if esc: k["escala"] = esc[0] + (esc[1] - esc[0]) * u
        return k
    return [{"t": 0, **en(_V.ini), "ease": "lineal"}, {"t": d, **en(_V.ini + d)}]


# ------------------------------------------------------------------ piezas hechas (usan SVG de la biblioteca)
def estrellas(n=40, sem=3): return polvo("#ffffff", n, (0, 0, 1080, 1920), sem, "estrellas")
def tierra(x, y, ancho, z=0.4, giro=4, keys=None): return IMG("tierra_hd", ancho=ancho, x=x, y=y, z=z, anim={"girar": giro}, keys=keys or [])
def luna(x, y, ancho, z=0.4, keys=None, **k): return IMG("luna_hd", ancho=ancho, x=x, y=y, z=z, keys=keys or [], **k)


def reloj(x, y, ancho, h0, m0, h1, m1, t0, t1, z=0.6):
    """Reloj de bolsillo cuyas agujas van de h0:m0 a h1:m1 entre t0 y t1. Sonido: (t, "tictac", dB, {"dur": …})."""
    k = ancho / 600; cx, cy = x, y + 20 * k
    return [IMG("reloj_bolsillo", ancho=ancho, x=x, y=y, z=z),
            IMG("aguja_hora", ancho=200 * k * 1.9, x=cx, y=cy, z=z + 0.01, keys=[{"t": t0, "rot": h0 * 30 + m0 * 0.5, "ease": "lineal"}, {"t": t1, "rot": h1 * 30 + m1 * 0.5}]),
            IMG("aguja_min", ancho=200 * k * 2.2, x=cx, y=cy, z=z + 0.02, keys=[{"t": t0, "rot": m0 * 6, "ease": "lineal"}, {"t": t1, "rot": m1 * 6}])]


def cronometro(rot0, rot1, t0, t1):
    ag = {"tipo": "forma", "forma": "poligono", "puntos": [[-7, 0], [0, -190], [7, 0], [0, 26]], "relleno": "#d62f22", "x": 540, "y": 1060, "z": 0.62,
          "keys": [{"t": t0, "rot": rot0, "ease": "lineal"}, {"t": t1, "rot": rot1}]}
    return [IMG("cronometro", ancho=640, x=540, y=1040, z=0.6), ag,
            {"tipo": "forma", "forma": "circulo", "radio": 16, "relleno": "#1b2233", "x": 540, "y": 1060, "z": 0.63}]


def lineas_vel(x, y, sem=1, color="#7df9ffaa"):
    r = random.Random(sem)
    return [flecha([[x - r.uniform(80, 220), y + dy], [x - 40, y + dy]], 0.05 + i * 0.05, 0.4 + i * 0.05, color, 4, punta=False, z=0.45)
            for i, dy in enumerate([-40, -10, 20, 50])]


def sol(x, y, r=170, z=0.3):
    return [brillo(x, y, r * 3.2, "#ffcf6a", 0.55, z - 0.01, pulso=[0.06, 2.0]),
            {"tipo": "esfera", "radio": r, "textura": "sol", "color": "#fff3b0", "color2": "#ffb02e", "giro": 6, "x": x, "y": y, "z": z, "luz": [0, 0]}]


def fundido_blanco(keys, color="#fff6e0"):
    """Fogonazo a pantalla completa por encima de todo (keys con `op`)."""
    return {"tipo": "forma", "forma": "rect", "ancho": 1300, "alto": 2200, "relleno": color, "x": 540, "y": 960, "hud": True, "z": 1, "keys": keys}


# ------------------------------------------------------------------ tiempos provisionales (sin voz)
def provisional(guion, salida, palabras_por_s=2.85):
    """Alineación estimada + MP3 en silencio para montar antes de tener la locución. La voz oficial
    («Archivo Oculto — Narración (clon)», eleven_v4) va a ≈2,85 palabras/s (155 palabras → 54,4 s)."""
    os.makedirs(salida, exist_ok=True)
    txt = open(guion, encoding="utf-8").read().strip()
    dur = round(len(txt.split()) / palabras_por_s + 0.5, 2)
    PAUSA = {".": 0.32, "?": 0.32, ":": 0.22, ",": 0.12}
    peso = [0.0 if c == " " else 1.0 for c in txt]
    extra = [PAUSA.get(c, 0.0) for c in txt]
    k = (dur - 0.6 - sum(extra)) / (sum(peso) + 0.6 * peso.count(0.0))
    t = 0.25; ini, fin = [], []
    for c, p, e in zip(txt, peso, extra):
        ini.append(round(t, 3)); t += p * k if p else k * 0.6; fin.append(round(t, 3)); t += e
    al = os.path.join(salida, "alineacion-provisional.json")
    mp3 = os.path.join(salida, "locucion-provisional.mp3")
    json.dump({"characters": list(txt), "character_start_times_seconds": ini, "character_end_times_seconds": fin}, open(al, "w"), ensure_ascii=False)
    subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", str(dur),
                           "-c:a", "libmp3lame", "-q:a", "4", mp3])
    return mp3, al


# ------------------------------------------------------------------ el vídeo
class Video:
    def __init__(self, salida, guion, audio=None, alineacion=None, svg_extra=None, palabras_por_s=2.85):
        """salida: carpeta del episodio. guion: ruta del .txt. Sin audio/alineacion → tiempos provisionales.
        svg_extra: carpeta con SVG propios de este vídeo (se copian a salida/svg, por encima de la biblioteca)."""
        global _V
        _V = self
        self.out = salida
        os.makedirs(os.path.join(salida, "svg"), exist_ok=True)
        self.provisional = not (audio and alineacion)
        if self.provisional:
            audio, alineacion = provisional(guion, salida, palabras_por_s)
        self.audio, self.alineacion = os.path.abspath(audio), os.path.abspath(alineacion)
        self.PAL = palabras_de_alineacion(self.alineacion)
        self.FIN = self.PAL[-1]["fin"] + 0.75
        from .biblioteca import ilus
        for f in os.listdir(os.path.join(AQUI, "biblioteca", "svg")):
            shutil.copy(os.path.join(AQUI, "biblioteca", "svg", f), os.path.join(salida, "svg", f))
        ilus.generar(os.path.join(salida, "svg"))
        if svg_extra:
            for f in os.listdir(svg_extra):
                shutil.copy(os.path.join(svg_extra, f), os.path.join(salida, "svg", f))
        self.FX, self.PLANOS, self.AVISOS, self.ultimo, self.ini = [], [], [], {}, 0.0

    def w(self, i, adelanto=0.06):
        """Segundo en que empieza la palabra i del guion (el corte va un pelo antes).
        Para ver los índices: `python3 -m motor.denso guion.txt`."""
        return max(0.0, self.PAL[i]["inicio"] - adelanto) if i else 0.0

    def plano(self, i_palabra, nombre, mas=0.0):
        """Decorador: registra un plano que empieza en la palabra i (+ `mas` s). La función recibe d y devuelve P(...)."""
        def reg(fn):
            self.PLANOS.append((self.w(i_palabra) + mas, nombre, fn))
            return fn
        return reg

    def construir(self, id_, claves=(), musica=None, version=1, gancho=True, y_subtitulo=300, grano=0.03):
        """Monta todos los planos y escribe salida/episodio.json. Devuelve la lista de avisos de lectura (vacía = bien)."""
        global _V
        _V = self
        self.PLANOS.sort(key=lambda p: p[0])
        escenas, informe = [], []
        for k, (ini, nombre, fn) in enumerate(self.PLANOS):
            fin = self.PLANOS[k + 1][0] if k + 1 < len(self.PLANOS) else self.FIN
            d = round(fin - ini, 3)
            self.ini = ini
            p = fn(d)
            els = []
            for e in p["els"]:  # halo neón: copia ancha y translúcida debajo de flechas y órbitas
                if e.get("tipo") == "flecha" and e.get("grosor", 0) >= 6:
                    els.append({**e, "grosor": e["grosor"] * 3, "color": e["color"][:7] + "38", "punta": False})
                if e.get("tipo") == "forma" and e.get("op_relleno") == 0 and e.get("borde"):
                    els.append({**e, "grosor": e["grosor"] * 4, "borde": e["borde"][:7] + "38"})
                els.append(e)
            esc = {"inicio": ini, "fin": fin, "fondo": {"colores": p["fondo"]}, "elementos": json.loads(json.dumps(els)), "camara": p["cam"],
                   "entrada": p["entrada"], "vineta": p["vineta"]}
            if p["entrada"] != "corte" and p["dur"]:
                esc["dur_entrada"] = p["dur"]
            # «whoosh» de transición: solo de vez en cuando (≥ 5 s) y muy bajo, para que no tape la música
            if p["entrada"] in ("desenfoque", "zoom", "barrido"):
                fx_espaciado("whoosh", ini, "whoosh", -24, 5, dur=0.35)
                if self.FX and self.FX[-1]["tipo"] == "whoosh" and self.FX[-1]["t"] == round(ini, 3):
                    self.FX[-1]["t"] = round(max(0, ini - 0.12), 3)
            for h in p["hud"]:
                txt = ((h.get("texto") or "") + " " + (h.get("unidad") or "")).strip()
                if h.get("contar"):
                    txt = (f"{h['contar'][1]} " + txt).strip()
                visible = h["keys"][-2]["t"] - h["keys"][0]["t"]
                if visible + 1e-3 < LEER(txt):
                    self.AVISOS.append(f"  ⚠ «{txt}» en «{nombre}»: {visible:.2f} s en pantalla, harían falta {LEER(txt):.2f} s")
                fx(ini + h["keys"][0]["t"], "pop", -16)
            esc["elementos"].extend(json.loads(json.dumps(p["hud"])))
            for s in p["sfx"]:
                t, tipo, db = s[:3]
                if tipo == "whoosh":
                    if db <= -20: continue      # fuera los whoosh pequeños repetidos
                    db -= 9                      # y los que quedan, bastante más bajos
                fx(ini + t, tipo, db, **(s[3] if len(s) > 3 else {}))
            escenas.append(esc)
            informe.append((d, nombre))
        ep = {"id": id_, "version": version, "audio": self.audio,
              "subtitulos": {"alineacion": self.alineacion, "max_chars": 26},
              "estilo_subtitulos": {"modo": "karaoke", "y": y_subtitulo, "tam": 62, "claves": list(claves)},
              "musica": musica or {"generar": "curiosidad", "semilla": 1, "db": -13}, "lufs": -19, "grano": grano,
              "escenas": escenas, "sfx": sorted(self.FX, key=lambda e: e["t"])}
        if gancho:
            ep["estilo_subtitulos"]["gancho"] = True  # DECISIONS 2026-11-16: gancho entero en el fotograma 0
        json.dump(ep, open(os.path.join(self.out, "episodio.json"), "w"), ensure_ascii=False, indent=1)
        ds = [d for d, _ in informe]
        print(f"{len(ds)} planos · {len(self.FX)} efectos · {self.FIN:.1f} s · plano más corto {min(ds):.2f} s · más largo {max(ds):.2f} s"
              + (" · TIEMPOS PROVISIONALES (sin voz)" if self.provisional else ""))
        print("  < 0,7 s:", sum(d < 0.7 for d in ds), "· 0,7–1,5 s:", sum(0.7 <= d < 1.5 for d in ds), "· ≥ 1,5 s:", sum(d >= 1.5 for d in ds))
        for d, n in informe:
            print(f"  {d:5.2f} s {'█' * int(d * 10)} {n}")
        print("\n".join(self.AVISOS) if self.AVISOS else "  ✓ todos los textos se pueden leer")
        return self.AVISOS


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("json", "os", "random", "shutil", "subprocess", "AQUI", "palabras_de_alineacion")]

if __name__ == "__main__":
    import sys, tempfile
    # índices de palabra de un guion (con tiempos provisionales o con la alineación real si se pasa)
    al = sys.argv[2] if len(sys.argv) > 2 else provisional(sys.argv[1], tempfile.mkdtemp())[1]
    for i, p in enumerate(palabras_de_alineacion(al)):
        print(f"{i:4d}  {p['inicio']:6.2f}  {p['texto']}")
