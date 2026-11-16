#!/usr/bin/env python3
"""Mete los datos dentro de la plantilla y genera web/index.html (una sola página, sin dependencias).

Usa datos/data.json si existe; si no, los datos de ejemplo.
  python3 estadisticas/construir.py            # normal
  python3 estadisticas/construir.py --ejemplo  # fuerza los datos de ejemplo
"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
reales = os.path.join(AQUI, "datos", "data.json")
fuente = reales if os.path.exists(reales) and "--ejemplo" not in sys.argv else os.path.join(AQUI, "ejemplo", "data.json")
datos = json.load(open(fuente, encoding="utf-8"))
incrustado = json.dumps(datos, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = open(os.path.join(AQUI, "plantilla.html"), encoding="utf-8").read().replace("__DATA__", incrustado)
os.makedirs(os.path.join(AQUI, "web"), exist_ok=True)
salida = os.path.join(AQUI, "web", "index.html")
open(salida, "w", encoding="utf-8").write(html)
print(f"OK: {salida} ({len(html)//1024} KB) con {os.path.relpath(fuente, AQUI)}")
