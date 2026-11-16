"""Piezas comunes del lote 2026-11-16-tarde — estilo v4 (Agente 20:00, Jorge).

Reutiliza los ayudantes de montaje de `lotes/2026-11-15-tarde/generadores/v4/comun_v4.py`
(IMG, BG, ROT, AMARILLO, CONTEXTO, polvo, brillo, cam) y la textura/degradados de `ilus.py`,
pero guarda las ilustraciones en ./svg/ de este lote.
"""
import copy, json, os, random, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.join(AQUI, "..", "..", "2026-11-15-tarde", "generadores", "v4")
sys.path.insert(0, os.path.abspath(V4))
from comun_v4 import IMG, BG, ROT, AMARILLO, CONTEXTO, polvo, brillo, cam  # noqa: E402,F401

OUT = os.path.join(AQUI, "svg")
os.makedirs(OUT, exist_ok=True)
R = random.Random(16)
W, H = 1080, 1920

TEXTURA = """
<filter id="grano" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3" result="n"/>
  <feColorMatrix type="saturate" values="0"/>
  <feComponentTransfer><feFuncA type="table" tableValues="0 0.10"/></feComponentTransfer>
  <feComposite operator="in" in2="SourceGraphic"/>
</filter>
<filter id="blur4"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="blur8"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="blur20"><feGaussianBlur stdDeviation="20"/></filter>
<filter id="blur40"><feGaussianBlur stdDeviation="40"/></filter>
<filter id="sombra" x="-20%" y="-20%" width="140%" height="140%">
  <feDropShadow dx="10" dy="16" stdDeviation="12" flood-color="#000" flood-opacity="0.45"/>
</filter>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
"""


def guardar(nombre, cuerpo, w=W, h=H, defs=""):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
           f'<defs>{TEXTURA}{defs}</defs>{cuerpo}</svg>')
    open(os.path.join(OUT, nombre + ".svg"), "w").write(svg)


def lg(id_, *stops, x1=0, y1=0, x2=0, y2=1):
    s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    return f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def rg(id_, *stops, cx=0.5, cy=0.5, r=0.5):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'


def grano(w=W, h=H):
    return f'<rect width="{w}" height="{h}" fill="#888" filter="url(#grano)"/>'


def copiar_v4(*nombres):
    """Copia ilustraciones ya hechas del lote 2026-11-15-tarde (v4) a ./svg/."""
    for n in nombres:
        shutil.copy(os.path.join(V4, "svg", n + ".svg"), os.path.join(OUT, n + ".svg"))


def CRAC(t0, t1, x, y, texto="CRAC", tam=84, rot=-8):
    return ROT(t0, t1, texto, tam=tam, color="#ffd23f", capsula=None, rot=rot, x=x, y=y)


class Montaje:
    def __init__(self, salida):
        self.S = []
        self.sfx = []
        self.out = salida
        os.makedirs(salida, exist_ok=True)
        shutil.copytree(OUT, os.path.join(salida, "svg"), dirs_exist_ok=True)

    def plano(self, ini, fin, fondo, elementos, camara, entrada="corte", vineta=0.55, dur=None):
        p = {"inicio": ini, "fin": fin, "fondo": {"colores": fondo}, "elementos": copy.deepcopy(elementos), "camara": camara,
             "entrada": entrada, "vineta": vineta}
        if dur:
            p["dur_entrada"] = dur
        self.S.append(p)
        return p

    def add(self, *els):
        self.S[-1]["elementos"].extend(els)

    def fx(self, t, tipo, db=-16):
        self.sfx.append({"t": round(t, 2), "tipo": tipo, "db": db})

    def guardar(self, n, slug, fin, claves, musica, audio_dir="."):
        self.S[-1]["fin"] = fin
        for a, b in zip(self.S, self.S[1:]):
            a["fin"] = b["inicio"]
        ep = {"id": f"2026-11-16-tarde-{n}-{slug}", "version": 1, "audio": os.path.join(audio_dir, f"{n}-locucion.mp3"),
              "subtitulos": {"alineacion": os.path.join(audio_dir, f"{n}-alineacion-original.json"), "max_chars": 26},
              "estilo_subtitulos": {"modo": "karaoke", "y": 300, "tam": 62, "claves": claves, "gancho": True},
              "musica": musica, "lufs": -19, "grano": 0.03, "sfx": self.sfx, "escenas": self.S}
        json.dump(ep, open(os.path.join(self.out, "episodio.json"), "w"), ensure_ascii=False, indent=1)
        print(len(self.S), "planos")
