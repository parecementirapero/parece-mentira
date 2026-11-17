#!/usr/bin/env python3
"""Estudio de audiencia y rendimiento. Uso: python3 estadisticas/estudio <orden>

  todo                      mediciones + estudio + autopsias (lo que corre cada mañana tras recoger.py)
  mediciones                actualiza datos/mediciones.json (mediciones a edad fija)
  estudio [--orientativo]   escribe datos/estudio.md; --orientativo lo enseña con lecturas de 3 h o más, sin guardar
  autopsias                 escribe datos/autopsias.md
  informe [AAAA-MM-DD]      informe de la semana anterior a esa fecha (por defecto, hoy)
  ficha nueva LOTE NN [--guion ARCHIVO] [--calidad ARCHIVO] [--quien NOMBRE] [clave=valor …]
  ficha comprobar           valida todas las fichas y dice qué falta
  ficha publicar LOTE NN ID_YOUTUBE [tiktok=… instagram=…]
  ficha acuerdo ARCHIVO     compara fichas.json con las de otro codificador (mismo formato)
  ficha diccionario         imprime el diccionario de variables
  experimento nuevo ID --hipotesis TEXTO --variable VAR --metrica MET --diferencia N [--inicio AAAA-MM-DD]
                           [--a-favor TEXTO] [--en-contra TEXTO] [--por-dia N] [--quien NOMBRE]
  experimento estado        cómo van los experimentos abiertos
  experimento cerrar ID [--forzar]
  tamano DESVIACION DIFERENCIA   vídeos por grupo para detectar esa diferencia
"""
import argparse
import datetime as dt
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import analisis as A      # noqa: E402
import autopsia as U      # noqa: E402
import estadistica as E   # noqa: E402
import experimento as X   # noqa: E402
import ficha as F         # noqa: E402
import informe as I       # noqa: E402
import mediciones as M    # noqa: E402
import tabla as T         # noqa: E402


def orden_ficha(args):
    if not args:
        sys.exit(__doc__)
    sub, resto = args[0], args[1:]
    if sub == "diccionario":
        print(F.diccionario_md())
    elif sub == "comprobar":
        fichas, mal = F.cargar(), 0
        for clave, f in fichas.items():
            problemas = F.validar(f)
            mal += bool(problemas)
            print(("✔ " if not problemas else "✘ ") + clave + ("" if not problemas else ": " + "; ".join(problemas)))
        previas = sum(1 for f in fichas.values() if f.get("momento") == "previo")
        print(f"{len(fichas)} fichas · {previas} codificadas antes de publicar · {mal} con problemas")
        sys.exit(1 if mal else 0)
    elif sub == "nueva":
        ap = argparse.ArgumentParser(prog="ficha nueva")
        ap.add_argument("lote"); ap.add_argument("numero")
        ap.add_argument("--guion"); ap.add_argument("--calidad"); ap.add_argument("--quien")
        ap.add_argument("--retrospectivo", action="store_true")
        ap.add_argument("valores", nargs="*")
        a = ap.parse_args(resto)
        valores = {}
        for par in a.valores:
            k, _, v = par.partition("=")
            valores[k] = F.convertir(k, v)
        guion = open(a.guion, encoding="utf-8").read() if a.guion else None
        calidad = open(a.calidad, encoding="utf-8").read() if a.calidad else None
        fichas = F.cargar()
        clave = f"{a.lote}/{a.numero}"
        if clave in fichas and fichas[clave].get("youtube"):
            sys.exit(f"{clave} ya está publicada: su ficha no se cambia. (Para corregir un error material, edita fichas.json y apúntalo en «notas».)")
        base = fichas.get(clave, {})
        nueva = F.nueva(a.lote, a.numero, guion, calidad, {**{k: v for k, v in base.items() if k not in ("lote", "numero")}, **valores},
                        momento="retrospectivo" if a.retrospectivo else "previo", codificador=a.quien)
        fichas[clave] = nueva
        F.guardar(fichas)
        problemas = F.validar(nueva)
        print(json.dumps(nueva, ensure_ascii=False, indent=1))
        print("Ficha completa." if not problemas else "Falta por rellenar: " + "; ".join(problemas))
    elif sub == "publicar":
        lote, numero, yt, *extra = resto
        fichas = F.cargar()
        clave = f"{lote}/{numero}"
        if clave not in fichas:
            sys.exit(f"No hay ficha {clave}: había que rellenarla antes de publicar. Créala con «ficha nueva … --retrospectivo».")
        fichas[clave]["youtube"] = yt
        for par in extra:
            k, _, v = par.partition("=")
            if k in ("tiktok", "instagram"):
                fichas[clave][k] = v
        F.guardar(fichas)
        print(f"{clave} → {yt}")
    elif sub == "acuerdo":
        otras = F.cargar(resto[0])
        for var, (ok, n) in F.acuerdo(F.cargar(), otras).items():
            if n:
                aviso = "" if ok / n >= 0.8 else "  ← por debajo del 80 %: hay que reescribir la definición"
                print(f"{var:12} {ok}/{n} ({ok / n * 100:.0f} %){aviso}")
    else:
        sys.exit(__doc__)


def orden_experimento(args):
    if not args:
        sys.exit(__doc__)
    sub, resto = args[0], args[1:]
    if sub == "nuevo":
        ap = argparse.ArgumentParser(prog="experimento nuevo")
        ap.add_argument("id"); ap.add_argument("--hipotesis", required=True); ap.add_argument("--variable", required=True)
        ap.add_argument("--metrica", required=True); ap.add_argument("--diferencia", type=float, required=True)
        ap.add_argument("--inicio"); ap.add_argument("--a-favor", default=""); ap.add_argument("--en-contra", default="")
        ap.add_argument("--quien"); ap.add_argument("--por-dia", type=int, default=1, help="vídeos de CADA brazo al día")
        a = ap.parse_args(resto)
        try:
            exp = X.nuevo(a.id, a.hipotesis, a.variable, a.metrica, a.diferencia, a.inicio, a.a_favor, a.en_contra,
                          por_dia=a.por_dia, quien=a.quien)
        except ValueError as e:
            sys.exit(str(e))
        print(X.a_markdown(exp))
        print("Calendario (qué brazo sale primero):")
        for dia, orden in X.calendario(exp):
            print(f"  {dia}: {orden}")
    elif sub == "estado":
        exps = X.cargar_todos()
        if not exps:
            print("No hay experimentos. Crea uno con «experimento nuevo».")
        filas = T.construir()
        for exp in exps.values():
            print(X.a_markdown(exp, exp.get("resultado") if exp["estado"] == "cerrado" else X.estado(exp, filas)))
    elif sub == "cerrar":
        try:
            exp = X.cerrar(resto[0], forzar="--forzar" in resto)
        except ValueError as e:
            sys.exit(str(e))
        print(X.a_markdown(exp, exp["resultado"]))
        print(f"Nivel de evidencia: {exp['nivel']}. Apúntalo en motor/APRENDIZAJE.md y, si cambia cómo hacemos los vídeos, en DECISIONS.md.")
    else:
        sys.exit(__doc__)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    orden, resto = argv[0], argv[1:]
    if orden == "todo":
        m = M.actualizar()
        r = A.ejecutar(mediciones=m)
        U.ejecutar(mediciones=m)
        mu = r["muestra"]
        print(f"OK: {mu['videos']} vídeos · {mu['con_ficha']} con ficha · {mu['con_gancho_yt']} con lectura comparable "
              f"-> datos/mediciones.json, datos/estudio.md, datos/autopsias.md")
        if dt.date.today().weekday() == 0:
            _, salida = I.ejecutar()
            print("Lunes: informe semanal ->", os.path.relpath(salida, os.path.dirname(os.path.dirname(AQUI))))
    elif orden == "mediciones":
        m = M.actualizar()
        print(f"OK: {len(m['videos'])} vídeos -> datos/mediciones.json")
    elif orden == "estudio":
        if "--orientativo" in resto:
            m = M.construir(M.cargar())
            filas = T.construir(mediciones=m, edad_minima=3)
            filas.sort(key=lambda f: f.get("publicado") or "9999")
            r = A.ejecutar(escribir=False, mediciones=m)
            r.update({"filas": filas, "muestra": A.muestra(filas), "potencia": A.potencia(filas),
                      "referencias": {k: E.mediana([f["metricas"][k]["valor"] for f in filas]) for k in T.METRICAS},
                      "categoricas": A.categoricas(filas), "numericas": A.numericas(filas)})
            print("⚠ ORIENTATIVO: mezcla lecturas de 3 h con lecturas de 30 h. No se guarda y no vale como evidencia.\n")
            print(A.a_markdown(r))
        else:
            A.ejecutar(mediciones=M.actualizar())
            print("OK -> datos/estudio.md")
    elif orden == "autopsias":
        U.ejecutar(mediciones=M.actualizar())
        print("OK -> datos/autopsias.md")
    elif orden == "informe":
        dia = dt.date.fromisoformat(resto[0]) if resto else None
        texto, salida = I.ejecutar(dia)
        print(texto)
        print("->", salida)
    elif orden == "ficha":
        orden_ficha(resto)
    elif orden == "experimento":
        orden_experimento(resto)
    elif orden == "tamano":
        desv, dif = float(resto[0]), float(resto[1])
        print(f"{E.tamano_muestra(desv, dif)} vídeos por grupo para detectar {dif} con desviación {desv} (80 % de potencia, 5 % de error)")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
