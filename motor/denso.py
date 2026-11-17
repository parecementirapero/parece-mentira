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
# Zona segura común a Shorts, Reels y TikTok (GUIA_CALIDAD §4): fuera de aquí, la app tapa el texto con sus botones.
SEG_ARRIBA, SEG_ABAJO, SEG_DER = 240, 1400, 900

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


def P(fondo, els, camara, entrada="corte", dur_entrada=0.3, vineta=0.55, hud=(), sfx=(), energia=None):
    """Un plano: fondo [arriba, abajo], elementos, cámara, entrada (corte|desenfoque|zoom|barrido),
    rótulos `hud` y sonidos `sfx` = [(t dentro del plano, tipo, dB[, {opciones}])].
    energia (0..1, opcional): fuerza la energía de la música en este plano (0,3 = recogida, 0,9 = clímax)."""
    return dict(fondo=fondo, els=els, cam=camara, entrada=entrada, dur=dur_entrada, vineta=vineta, hud=list(hud), sfx=list(sfx), energia=energia)


def K(d, *pares):
    """Claves en FRACCIÓN de la duración del plano: K(d, (0, {...}), (0.6, {...}))."""
    return [{"t": round(f * d, 3), **v} for f, v in pares]


# ------------------------------------------------------------------ movimiento con vida (principios de animación; GUIA_CALIDAD §3)
def aparece(t0, dur=0.4):
    """El objeto entra de golpe y se asienta como un muelle (se pasa y vuelve). Súmalo a sus otras claves."""
    return [{"t": t0, "escala": 0.0, "op": 0}, {"t": t0 + 0.04, "op": 1}, {"t": t0 + dur, "escala": 1.0, "ease": "elastico"}]


def cae(t0, t1, y0, y1, aplasta=0.16):
    """Caída con peso: se estira al caer, bota en el suelo y se aplasta al aterrizar (conserva el volumen).
    Sonido que le va: (t1 - 0.25*(t1-t0), "golpe", -14)."""
    tg = t0 + (t1 - t0) * 0.36  # primer contacto con el suelo en la curva «bote»
    return [{"t": t0, "y": y0, "ex": 1 - aplasta * 0.5, "ey": 1 + aplasta}, {"t": t1, "y": y1, "ease": "bote"},
            {"t": tg, "ex": 1 - aplasta * 0.5, "ey": 1 + aplasta, "ease": "lineal"}, {"t": tg + 0.06, "ex": 1 + aplasta, "ey": 1 - aplasta, "ease": "salida"},
            {"t": tg + 0.3, "ex": 1.0, "ey": 1.0, "ease": "elastico"}]


def lanza(t0, t1, p0, p1):
    """Sale disparado tomando impulso hacia atrás primero (anticipación) y pasándose un poco al llegar."""
    return [{"t": t0, "x": p0[0], "y": p0[1]}, {"t": t1, "x": p1[0], "y": p1[1], "ease": "anticipa"}]


def late(t0, veces=2, amp=0.14, periodo=0.3):
    """Latido para llamar la atención sobre el objeto del que se habla (señalización)."""
    ks = [{"t": t0, "escala": 1.0}]
    for i in range(veces):
        ks += [{"t": t0 + i * periodo + periodo * 0.35, "escala": 1 + amp, "ease": "salida"}, {"t": t0 + (i + 1) * periodo, "escala": 1.0, "ease": "suave"}]
    return ks


def sigue(keys, retraso=0.1):
    """Copia unas claves con retraso: para la pieza que va detrás de otra (inercia: cola, mochila, sombra, rótulo)."""
    return [{**k, "t": round(k["t"] + retraso, 3)} for k in keys]


def arranque(x, y, d, desde="abajo", recorrido_px=260, deriva=50):
    """Claves para el SUJETO DEL PRIMER PLANO (APRENDIZAJE.md, H7): en el fotograma 0 ya está en pantalla y moviéndose,
    se asienta con muelle en 0,4 s y sigue derivando despacio hasta el corte, para que no haya ni un instante quieto.
    desde: "abajo" | "arriba" | "izquierda" | "derecha". Úsalo como keys=arranque(540, 1300, d)."""
    dx, dy = {"abajo": (0, 1), "arriba": (0, -1), "izquierda": (-1, 0), "derecha": (1, 0)}[desde]
    return [{"t": 0, "x": x + dx * recorrido_px, "y": y + dy * recorrido_px, "rot": -6 * (dx or dy), "escala": 0.94},
            {"t": 0.4, "x": x, "y": y, "rot": 0, "escala": 1.0, "ease": "elastico"},
            {"t": d, "x": x - dx * deriva, "y": y - dy * deriva, "escala": 1.06, "ease": "suave"}]


def senala(x, y, t0, t1, radio=110, color=AMBAR, z=0.85):
    """Anillo que se dibuja alrededor de lo que se nombra (señalización: el ojo va donde va la voz)."""
    return {"tipo": "forma", "forma": "elipse", "ancho": radio * 2, "alto": radio * 2, "relleno": "#ffffff", "op_relleno": 0, "grosor": 7,
            "borde": color, "x": x, "y": y, "z": z,
            "keys": [{"t": t0, "escala": 1.6, "op": 0}, {"t": t0 + 0.25, "escala": 1.0, "op": 1, "ease": "golpe"},
                     {"t": t1, "escala": 1.06, "op": 1}, {"t": t1 + 0.2, "op": 0}]}


# ------------------------------------------------------------------ rótulos
def rotulo(t0, t1, texto="", **k):
    ks = [{"t": t0, "escala": 0.0, "op": 0}, {"t": t0 + 0.05, "op": 1}, {"t": t0 + min(0.25, (t1 - t0) / 3), "escala": 1.0, "ease": "rebote"},
          {"t": t1, "escala": 1.0, "op": 1}, {"t": t1 + 0.15, "op": 0}]
    return {"tipo": "rotulo", "texto": texto, "hud": True, "z": 1, "keys": ks, **k}


def amarillo(t0, t1, texto, y=1360, tam=96, color="#ffd23f", x=540):
    """Palabra clave grande e inclinada, sin cápsula. Sobre fondos oscuros, pásale un neón (CIAN, MAGENTA, LIMA)."""
    return {**rotulo(t0, t1, texto, tam=tam, color=color, capsula=None, rot=-6, x=x, y=y), "_clave": True}


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
    def __init__(self, salida, guion, audio=None, alineacion=None, svg_extra=None, palabras_por_s=2.85, omitir=()):
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
        self.OMITIDAS = set()
        if omitir:
            self._recortar(omitir)
        self.FIN = max(p["fin"] for p in self.PAL) + 0.75
        from .biblioteca import ilus
        for f in os.listdir(os.path.join(AQUI, "biblioteca", "svg")):
            shutil.copy(os.path.join(AQUI, "biblioteca", "svg", f), os.path.join(salida, "svg", f))
        ilus.generar(os.path.join(salida, "svg"))
        if svg_extra:
            for f in os.listdir(svg_extra):
                shutil.copy(os.path.join(svg_extra, f), os.path.join(salida, "svg", f))
        self.FX, self.PLANOS, self.AVISOS, self.ultimo, self.ini = [], [], [], {}, 0.0

    def _recortar(self, rangos, g=0.12):
        """VERSIÓN CORTA con la misma locución (experimento H2 de APRENDIZAJE.md): quita frases enteras.
        rangos = [(i0, i1), ...] en índices de palabra: se quitan las palabras i0…i1-1 (i1 = primera que se queda).
        Corta el audio un pelo antes de cada frase (conserva la pausa natural), lo guarda en salida/locucion-corta.mp3
        con su alineación, y mantiene los ÍNDICES ORIGINALES: `v.w(i)` y `@v.plano(i)` siguen valiendo, y los planos
        que empiezan en una palabra quitada se saltan solos. Hay que oír los empalmes antes de publicar."""
        P0 = [dict(p) for p in self.PAL]
        cortes = sorted((max(0.0, P0[a]["inicio"] - g), (P0[b]["inicio"] - g) if b < len(P0) else P0[-1]["fin"] + 0.3) for a, b in rangos)
        for a, b in rangos:
            self.OMITIDAS.update(range(a, b))
        def nuevo(t):   # tiempo original → tiempo en la versión corta
            return t - sum(min(t, c1) - c0 for c0, c1 in cortes if t > c0)
        for i, p in enumerate(self.PAL):
            if i in self.OMITIDAS:
                c0 = next(c0 for c0, c1 in cortes if c0 <= P0[i]["inicio"] + 1e-6 < c1 + g + 1e-6)
                p["inicio"] = p["fin"] = round(nuevo(c0), 3)
            else:
                p["inicio"], p["fin"] = round(nuevo(P0[i]["inicio"]), 3), round(nuevo(P0[i]["fin"]), 3)
        # audio: tramos que se quedan, con 15 ms de fundido en cada empalme para que no haga «clic»
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", self.audio]))
        cortes = [(c0, min(c1, dur)) for c0, c1 in cortes]
        tramos, t = [], 0.0
        for c0, c1 in cortes:
            if c0 > t: tramos.append((t, c0))
            t = c1
        if t < dur: tramos.append((t, dur))
        filtro = ";".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={b - a - 0.015:.3f}:d=0.015[a{k}]" for k, (a, b) in enumerate(tramos))
        filtro += ";" + "".join(f"[a{k}]" for k in range(len(tramos))) + f"concat=n={len(tramos)}:v=0:a=1[o]"
        mp3 = os.path.join(self.out, "locucion-corta.mp3")
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-i", self.audio, "-filter_complex", filtro, "-map", "[o]", "-c:a", "libmp3lame", "-q:a", "2", mp3])
        ch, ini, fin = [], [], []
        vivas = [p for i, p in enumerate(self.PAL) if i not in self.OMITIDAS]
        for k, p in enumerate(vivas):
            n = len(p["texto"]); paso = (p["fin"] - p["inicio"]) / n
            for j, c in enumerate(p["texto"]):
                ch.append(c); ini.append(round(p["inicio"] + j * paso, 3)); fin.append(round(p["inicio"] + (j + 1) * paso, 3))
            if k < len(vivas) - 1:
                ch.append(" "); ini.append(p["fin"]); fin.append(vivas[k + 1]["inicio"])
        al = os.path.join(self.out, "alineacion-corta.json")
        json.dump({"characters": ch, "character_start_times_seconds": ini, "character_end_times_seconds": fin}, open(al, "w"), ensure_ascii=False)
        self.audio, self.alineacion = os.path.abspath(mp3), os.path.abspath(al)
        print(f"versión corta: {len(vivas)} palabras de {len(self.PAL)} · {dur:.1f} s → {dur - sum(c1 - c0 for c0, c1 in cortes):.1f} s · empalmes en "
              + ", ".join(f"{nuevo(c0):.1f} s" for c0, _ in cortes))

    def w(self, i, adelanto=0.06):
        """Segundo en que empieza la palabra i del guion (el corte va un pelo antes).
        Para ver los índices: `python3 -m motor.denso guion.txt`."""
        return max(0.0, self.PAL[i]["inicio"] - adelanto) if i else 0.0

    def plano(self, i_palabra, nombre, mas=0.0):
        """Decorador: registra un plano que empieza en la palabra i (+ `mas` s). La función recibe d y devuelve P(...)."""
        def reg(fn):
            if i_palabra not in self.OMITIDAS:      # versión corta: los planos de las frases quitadas no existen
                self.PLANOS.append((self.w(i_palabra) + mas, nombre, fn))
            return fn
        return reg

    def _a_zona_segura(self, h, nombre):
        """Recoloca un rótulo que se sale de la zona segura: lo sube si baja de y=1400, lo encoge si no cabe a lo ancho
        y lo aparta de la columna de botones de la derecha. Devuelve True si lo ha tocado."""
        from .calidad import _caja
        tocado, M = False, 10  # M = margen para no quedarse justo en el borde
        for _ in range(10):
            x0, y0, x1, y1 = _caja(h)
            if x1 - x0 > 900 - M and h.get("tam", 120) > 44:
                h["tam"] = int(h.get("tam", 120) * 0.92); tocado = True; continue
            if y1 > SEG_ABAJO - M:
                h["y"] = int(h.get("y", 960) - (y1 - SEG_ABAJO + M)) - 1; tocado = True; continue
            if x1 > SEG_DER - M and y1 > 800:
                x_min = (x1 - x0) / 2 + 70  # sin salirse por la izquierda
                x_nuevo = int(h.get("x", 540) - (x1 - SEG_DER + M)) - 1
                if x_nuevo >= x_min:
                    h["x"] = x_nuevo
                elif h.get("tam", 120) > 44:      # no cabe a la izquierda de los botones: se encoge
                    h["x"] = int(max(x_nuevo, x_min)); h["tam"] = int(h.get("tam", 120) * 0.92)
                else:
                    break
                tocado = True; continue
            break
        if tocado:
            self.MOVIDOS.append(f"«{(h.get('texto') or '') or h.get('unidad', '')}» en «{nombre}» → x={h.get('x', 540)}, y={h.get('y', 960)}, tam={h.get('tam', 120)}")
        return tocado

    def construir(self, id_, claves=(), musica=None, version=1, gancho=True, y_subtitulo=320, grano=0.03, zona_segura=True,
                  musica_viva=True, bucle=0.0, subtitulos="karaoke"):
        """Monta todos los planos y escribe salida/episodio.json. Devuelve la lista de avisos de lectura (vacía = bien).
        zona_segura=True recoloca solos los rótulos que la app taparía (míralos luego en la hoja de fotogramas:
        al subirlos pueden pisar al sujeto; en ese caso, colócalos tú dentro de y=240…1400)."""
        self.MOVIDOS = []
        forzada = {}
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
            if subtitulos == "palabra":
                # el subtítulo ya enseña la palabra clave en grande y en amarillo: los rótulos de palabra sobran (redundancia)
                p["hud"] = [h for h in p["hud"] if not h.get("_clave")]
            for h in p["hud"]:
                h.pop("_clave", None)
                if zona_segura and h.get("tipo") == "rotulo":
                    self._a_zona_segura(h, nombre)
                if subtitulos == "palabra" and h.get("tipo") == "rotulo" and not h.get("fijo"):  # fijo=True: no se mueve
                    from .calidad import _caja
                    ysub = y_subtitulo if y_subtitulo > 600 else 1180
                    x0, y0, x1, y1 = _caja(h)
                    if y1 > ysub - 100 and y0 < ysub + 100:      # pisa la franja del subtítulo
                        # primero se intenta DEBAJO (entre el subtítulo y el límite de la zona segura), para no tapar al
                        # sujeto; si no cabe ni encogido, justo encima
                        h["tam"] = min(h.get("tam", 120), 92)
                        x0, y0, x1, y1 = _caja(h)
                        if (y1 - y0) <= SEG_ABAJO - 8 - (ysub + 80):
                            h["y"] = int(h.get("y", 960) + (ysub + 80 - y0)); donde = "debajo"
                        else:
                            h["y"] = int(h.get("y", 960) - (y1 - (ysub - 110))); donde = "encima"
                        self.MOVIDOS.append(f"«{(h.get('texto') or '') or h.get('unidad', '')}» en «{nombre}» → y={h['y']} ({donde} del subtítulo)")
                txt = ((h.get("texto") or "") + " " + (h.get("unidad") or "")).strip()
                if h.get("contar"):
                    txt = (f"{h['contar'][1]} " + txt).strip()
                visible = h["keys"][-2]["t"] - h["keys"][0]["t"]
                if visible + 1e-3 < LEER(txt):
                    self.AVISOS.append(f"  ⚠ «{txt}» en «{nombre}»: {visible:.2f} s en pantalla, harían falta {LEER(txt):.2f} s")
                if not h.pop("sin_pop", False):  # sin_pop=True: el rótulo ya trae su propio sonido
                    fx(ini + h["keys"][0]["t"], "pop", -16)
            esc["elementos"].extend(json.loads(json.dumps(p["hud"])))
            for s in p["sfx"]:
                t, tipo, db = s[:3]
                if tipo == "whoosh":
                    if db <= -20: continue      # fuera los whoosh pequeños repetidos
                    db -= 9                      # y los que quedan, bastante más bajos
                fx(ini + t, tipo, db, **(s[3] if len(s) > 3 else {}))
            if p.get("energia") is not None:
                forzada[k] = p["energia"]
            escenas.append(esc)
            informe.append((d, nombre))
        ep = {"id": id_, "version": version, "audio": self.audio,
              "subtitulos": {"alineacion": self.alineacion, "max_chars": 26},
              "estilo_subtitulos": {"modo": "karaoke", "y": y_subtitulo, "tam": 62, "claves": list(claves)},
              "musica": dict(musica or {"generar": "curiosidad", "semilla": 1, "db": -13}), "lufs": -19, "grano": grano,
              "escenas": escenas, "sfx": sorted(self.FX, key=lambda e: e["t"])}
        if musica_viva and "archivo" not in ep["musica"]:
            # la música sigue al montaje: se recoge en el gancho y en los planos largos y aprieta donde hay ráfagas de cortes;
            # termina en el acorde que resuelve en el primero (si el Short se repite, enlaza)
            ini = [e["inicio"] for e in escenas]
            curva = []
            for k, e in enumerate(escenas):
                c = (e["inicio"] + e["fin"]) / 2
                cortes = sum(1 for t in ini if abs(t - c) <= 2.0)
                nivel = forzada.get(k, min(0.95, max(0.3, 0.25 + 0.14 * cortes)))
                curva.append([round(c, 2), round(0.35 if c < 1.5 and k not in forzada else nivel, 2)])
            ep["musica"].setdefault("energia", curva)
            ep["musica"].setdefault("bucle", True)
        if subtitulos == "palabra":
            ep["estilo_subtitulos"] = {"modo": "palabra", "y": y_subtitulo if y_subtitulo > 600 else 1180, "tam": 104, "claves": list(claves)}
        if bucle:
            ep["bucle"] = bucle  # segundos finales que se funden con el primer fotograma (el Short enlaza al repetirse)
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
        if self.MOVIDOS:
            print(f"  ↥ {len(self.MOVIDOS)} rótulos recolocados dentro de la zona segura (compruébalos en la hoja):")
            for m in self.MOVIDOS: print("     " + m)
        return self.AVISOS


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("json", "os", "random", "shutil", "subprocess", "AQUI", "palabras_de_alineacion")]

if __name__ == "__main__":
    import sys, tempfile
    # índices de palabra de un guion (con tiempos provisionales o con la alineación real si se pasa)
    al = sys.argv[2] if len(sys.argv) > 2 else provisional(sys.argv[1], tempfile.mkdtemp())[1]
    for i, p in enumerate(palabras_de_alineacion(al)):
        print(f"{i:4d}  {p['inicio']:6.2f}  {p['texto']}")
