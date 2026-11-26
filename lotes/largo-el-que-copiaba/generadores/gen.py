"""Vídeo «El que copiaba en el colegio» — montaje denso.
  MOTOR_FORMATO=16:9 python3 gen.py DIR    → largo horizontal para YouTube (4:45)
  python3 gen.py DIR --corto               → corto vertical de ~1 min (estilo B: focos y contadores), MISMA locución recortada
  --partes 1,2 → solo esos planos (para probar)
"""
import importlib, json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
LOTE = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import comun_cp as C  # noqa: E402
from comun_cp import *  # noqa: E402,F401,F403
from motor.core import HORIZONTAL  # noqa: E402

SALIDA = sys.argv[1]
CORTO = "--corto" in sys.argv
PARTES = [1, 2, 3]
if "--partes" in sys.argv:
    PARTES = [int(x) for x in sys.argv[sys.argv.index("--partes") + 1].split(",")]

ARTE = os.environ.get("ARTE_CP") or os.path.join(SALIDA, "_arte")
if not os.path.exists(os.path.join(ARTE, "bg_aula_h.svg")):
    os.makedirs(ARTE, exist_ok=True)
    for m in ("ilus_personajes", "ilus_escenarios", "ilus_objetos_cueva", "ilus_objetos_mundo"):
        importlib.import_module(m).generar(ARTE)
    for m in ("frame_prueba", "ilus_fondos", "ilus_gente", "ilus_cosas"):
        importlib.import_module(m).generar(ARTE)
# piezas extra de cada parte (ilus_extra_pN.py, nombres con prefijo pN_): se regeneran siempre (son pocas)
for n in (1, 2, 3, 4):
    if os.path.exists(os.path.join(AQUI, f"ilus_extra_p{n}.py")):
        importlib.import_module(f"ilus_extra_p{n}").generar(ARTE)
C.comun.SVG_DIR = ARTE

# palabras que el corto quita (índices de alineacion-completa.json; i1 = primera que se queda)
OMITIR_CORTO = [(18, 150), (173, 211), (223, 243), (270, 290), (311, 328), (335, 592), (604, 705), (739, 749)]

v = Video(SALIDA, os.path.join(LOTE, "guion.txt"), os.path.join(LOTE, "voz", "locucion-completa.wav"),
          os.path.join(LOTE, "voz", "alineacion-completa.json"), svg_extra=ARTE, omitir=OMITIR_CORTO if CORTO else ())
plano = registrar(v)

if CORTO:
    importlib.import_module("planos_corto").planos(v, plano)
    v.construir("el-que-copiaba-corto-9x16", version=1, bucle=0.3,
                musica={"generar": "emprende", "semilla": 31, "db": -12},
                claves=["copiar", "rico", "Marta", "Lucas", "cafetería", "hamburguesería", "cola", "cinco", "dos", "locales",
                        "mejorar", "sola", "cosa", "primero", "mejor"],
                ep_extra={"sfx_bajo_voz": True})
else:
    for n in PARTES:
        importlib.import_module(f"planos_p{n}").planos(v, plano)
    v.construir("el-que-copiaba" + ("-16x9" if HORIZONTAL else "-9x16"), version=1, bucle=0.0,
                musica={"generar": "emprende", "semilla": 12, "db": -14},
                claves=["copiar", "copiaba", "rico", "trampa", "Marta", "Lucas", "colegio", "timbre", "cafetería", "tiempo",
                        "hamburguesería", "cola", "veinte", "cinco", "dos", "locales", "funciona", "golpes", "Google",
                        "Facebook", "Instagram", "Snapchat", "mejor", "copias", "mejoras", "rápido", "barato", "cerca",
                        "bonito", "sola", "cosa", "primero"],
                ep_extra={"sfx_bajo_voz": True})
