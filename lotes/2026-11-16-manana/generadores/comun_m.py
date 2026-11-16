"""Piezas comunes del lote 2026-11-16-manana. Reutiliza comun_v4 (lote 2026-11-15-tarde) y cambia el guardado:
id del lote, alineación NN-alineacion.json, gancho en el fotograma 0 (motor v2.3) y svg/ de este lote."""
import json, os, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "2026-11-15-tarde", "generadores", "v4"))
from comun_v4 import IMG, BG, ROT, AMARILLO, CONTEXTO, polvo, humo, brillo, cam  # noqa: E402,F401
import comun_v4  # noqa: E402

LOTE = "2026-11-16-manana"


class Montaje(comun_v4.Montaje):
    def __init__(self, salida):
        self.S = []
        self.out = salida
        os.makedirs(salida, exist_ok=True)
        shutil.copytree(os.path.join(AQUI, "svg"), os.path.join(salida, "svg"), dirs_exist_ok=True)

    def guardar(self, n, slug, fin, claves, musica, version=1):
        self.S[-1]["fin"] = fin
        for a, b in zip(self.S, self.S[1:]):
            a["fin"] = b["inicio"]
        ep = {"id": f"{LOTE}-{n}-{slug}", "version": version, "audio": f"{n}-locucion.mp3",
              "subtitulos": {"alineacion": f"{n}-alineacion.json", "max_chars": 26},
              "estilo_subtitulos": {"modo": "karaoke", "y": 300, "tam": 62, "claves": claves, "gancho": True},
              "musica": musica, "lufs": -19, "grano": 0.03, "escenas": self.S}
        json.dump(ep, open(os.path.join(self.out, "episodio.json"), "w"), ensure_ascii=False, indent=1)
        print(len(self.S), "planos")


def flecha(pts, t0, t1, color="#ffffff", grosor=8, punta=True, disc=None, z=0.5, hud=False):
    f = {"tipo": "flecha", "puntos": [list(p) for p in pts], "grosor": grosor, "color": color, "punta": punta, "z": z,
         "keys": [{"t": t0, "progreso": 0}, {"t": t1, "progreso": 1}]}
    if disc: f["discontinua"] = disc
    if hud: f["hud"] = True
    return f


def contador(t0, t1, hasta, unidad, x=540, y=1500, tam=120, dur=1.0, prefijo=None, **k):
    r = ROT(t0, t1, "", tam=tam, x=x, y=y, unidad=unidad, **k)
    r["contar"] = [0, hasta, dur]
    r["contar_desde"] = t0
    if prefijo: r["contar_prefijo"] = prefijo
    return r
