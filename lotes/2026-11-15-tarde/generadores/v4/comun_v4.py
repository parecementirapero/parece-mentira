"""Piezas comunes de los generadores v4 (ilustración SVG + planos por frase). Ver gen_01.py."""
import copy, json, os, random, shutil

AQUI = os.path.dirname(os.path.abspath(__file__))


def IMG(n, **k): return {"tipo": "imagen", "archivo": f"svg/{n}.svg", **k}
def BG(n, z=0.05, ancho=1180): return IMG(n, ancho=ancho, x=540, y=960, z=z)


def ROT(t0, t1, texto, **k):
    ks = [{"t": t0, "escala": 0.0, "op": 0}, {"t": t0 + 0.06, "op": 1}, {"t": t0 + 0.3, "escala": 1.0, "ease": "rebote"},
          {"t": t1, "escala": 1.0, "op": 1}, {"t": t1 + 0.2, "op": 0}]
    return {"tipo": "rotulo", "texto": texto, "hud": True, "z": 1, "keys": ks, **k}


def AMARILLO(t0, t1, texto, y=1360): return ROT(t0, t1, texto, tam=96, color="#ffd23f", capsula=None, rot=-6, x=540, y=y)
def CONTEXTO(t0, t1, texto): return ROT(t0, t1, texto, tam=54, color="#ffffff", capsula="#c0392be6", borde="#ffffff30", x=540, y=470)


def polvo(color="#fff1c8", n=40, area=(0, 300, 1080, 1700), sem=1, clase="polvo"):
    return {"tipo": "particulas", "clase": clase, "color": color, "area": list(area), "n": n, "tam": [2, 5],
            "vel": [6, -10], "z": 0.9, "semilla": sem}


def humo(x, y, n=30, ancho=260, sem=2, op=1.0, color="#2b2826"):
    r = random.Random(sem)
    return [{"tipo": "brillo", "x": x + r.uniform(-ancho / 2, ancho / 2), "y": y - r.uniform(0, 120), "radio": r.uniform(120, 200),
             "color": color, "intensidad": 0.55 * op, "z": 0.5,
             "anim": {"deriva": [r.uniform(8, 25), -r.uniform(55, 90)], "pulso": [0.15, r.uniform(2, 3)]}}
            for _ in range(max(5, n // 5))]


def brillo(x, y, r, color, i=0.5, z=0.06, pulso=None, keys=None):
    b = {"tipo": "brillo", "x": x, "y": y, "radio": r, "color": color, "intensidad": i, "z": z}
    if pulso: b["anim"] = {"pulso": pulso}
    if keys: b["keys"] = keys
    return b


def cam(z0, z1, f0=(540, 960), f1=None, temblor=0):
    return {"zoom": [z0, z1], "foco": [list(f0), list(f1 or f0)], "pan": [[0, 0], [0, 0]], "temblor": temblor}


class Montaje:
    def __init__(self, salida, svgs=None):
        self.S = []
        self.out = salida
        os.makedirs(salida, exist_ok=True)
        shutil.copytree(os.path.join(AQUI, "svg"), os.path.join(salida, "svg"), dirs_exist_ok=True)

    def plano(self, ini, fin, fondo, elementos, camara, entrada="corte", vineta=0.55, dur=None):
        p = {"inicio": ini, "fin": fin, "fondo": {"colores": fondo}, "elementos": copy.deepcopy(elementos), "camara": camara,
             "entrada": entrada, "vineta": vineta}
        if dur: p["dur_entrada"] = dur
        self.S.append(p)
        return p

    def add(self, *els):
        self.S[-1]["elementos"].extend(els)

    def guardar(self, n, slug, fin, claves, musica):
        self.S[-1]["fin"] = fin
        for a, b in zip(self.S, self.S[1:]):
            a["fin"] = b["inicio"]
        ep = {"id": f"2026-11-15-tarde-{n}-{slug}", "version": 4, "audio": f"{n}-locucion.mp3",
              "subtitulos": {"alineacion": f"{n}-alineacion-original.json", "max_chars": 26},
              "estilo_subtitulos": {"modo": "karaoke", "y": 300, "tam": 62, "claves": claves},
              "musica": musica, "lufs": -19, "grano": 0.03, "escenas": self.S}
        json.dump(ep, open(os.path.join(self.out, "episodio.json"), "w"), ensure_ascii=False, indent=1)
        print(len(self.S), "planos")
