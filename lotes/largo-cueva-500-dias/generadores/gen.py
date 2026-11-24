"""Vídeo largo «¿Qué pasaría si te encerraras 500 días en una cueva sin reloj?» — montaje denso en DOS formatos.

Uso:
  python3 gen.py DIR_SALIDA                   → vertical 9:16 (las 5 partes de TikTok, de un tirón)
  MOTOR_FORMATO=16:9 python3 gen.py DIR_SALIDA → horizontal 16:9 (YouTube)
  Opción --partes 1,2 → solo los planos de esas partes (para probar rápido)
Mismo audio (voz/locucion-completa.wav) y mismos cortes en los dos: cada plano se escribe una vez (comun.adaptar).
"""
import importlib, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
LOTE = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(LOTE, "..", ".."))
sys.path.insert(0, RAIZ); sys.path.insert(0, AQUI)
from motor.core import HORIZONTAL  # noqa: E402
import comun  # noqa: E402
from comun import *  # noqa: E402,F401,F403

SALIDA = sys.argv[1]
PARTES = [1, 2, 3, 4, 5]
if "--partes" in sys.argv:
    PARTES = [int(x) for x in sys.argv[sys.argv.index("--partes") + 1].split(",")]

# todo el arte del lote en una carpeta (se genera una vez)
SVG = os.path.join(SALIDA, "_arte")
if not os.path.exists(os.path.join(SVG, "bg_cueva_campamento_h.svg")):
    os.makedirs(SVG, exist_ok=True)
    for m in ("ilus_personajes", "ilus_escenarios", "ilus_objetos_cueva", "ilus_objetos_mundo"):
        importlib.import_module(m).generar(SVG)
comun.SVG_DIR = SVG

v = Video(SALIDA, os.path.join(LOTE, "guion.txt"), os.path.join(LOTE, "voz", "locucion-completa.wav"),
          os.path.join(LOTE, "voz", "alineacion-completa.json"), svg_extra=SVG)
CORTES = json.load(open(os.path.join(LOTE, "cortes.json")))["partes"]
plano = registrar(v)

# primera palabra de cada parte (para atar las marcas de parte y comprobar que hay corte de plano)
INICIO_PARTE = {1: 0, 2: 287, 3: 583, 4: 844, 5: 1035}
comun.INICIO_PARTE = INICIO_PARTE

for n in PARTES:
    importlib.import_module(f"planos_p{n}").planos(v, plano)

# ------------------------------------------------------------------ solo vertical: marcas de las partes de TikTok
if not HORIZONTAL:
    import marcas
    marcas.poner(v, CORTES, INICIO_PARTE, PARTES)

v.construir("largo-cueva-500-dias" + ("-16x9" if HORIZONTAL else "-9x16"), version=1, bucle=0.0,
            musica={"generar": "misterio", "semilla": 500, "db": -14},
            claves=["cueva", "setenta", "metros", "cerebro", "tiempo", "Beatriz", "Flamini", "quinientos", "reloj", "sol", "Siffre",
                    "recuerdos", "silencio", "moscas", "día", "días", "año", "rutina", "ventanas"],
            ep_extra={"sfx_bajo_voz": True})
