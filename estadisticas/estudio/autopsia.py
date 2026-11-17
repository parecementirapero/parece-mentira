"""Autopsia por vídeo: qué pasó, dónde se fue la gente y cuál es el diagnóstico. Un diagnóstico, no cinco.

Se hace cuando el vídeo tiene lecturas con 24 h o más (lo ideal, 48 h). Cruza la curva de retención con
el guion: cada caída fuerte se apunta junto a la frase que sonaba en ese momento.

Aviso: los tiempos de cada frase se ESTIMAN repartiendo las palabras por la duración (las alineaciones
exactas están en el Mac, no en el repo). El error típico es de 1 a 2 segundos.
"""
import glob
import json
import os
import re

import estadistica as E
import ficha as F
import mediciones as M
import tabla as T

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTADISTICAS = os.path.dirname(AQUI)
RAIZ = os.path.dirname(ESTADISTICAS)
SALIDA = os.path.join(ESTADISTICAS, "datos", "autopsias.md")

CAIDA = 1.5      # puntos por segundo: mínimo para hablar de escalón
INICIO_ESCALONES = 5   # segundos: antes de aquí la pérdida es del gancho
AGUANTA = 0.35   # puntos por segundo: por debajo, el tramo retiene
BAJO, ALTO = 0.90, 1.15   # índices frente a la mediana del canal

DIAGNOSTICOS = {
    "tema": "Fallo de tema: el primer segundo está dentro de norma y aun así la gente desliza.",
    "primer segundo": "Fallo de primer segundo: gancho bajo y el arranque se sale de la norma.",
    "ritmo": "Fallo de ritmo: entran, pero se van a mitad.",
    "distribución": "Fallo de distribución: buenos porcentajes y pocas vistas. La plataforma no lo enseñó; no es culpa del vídeo.",
    "acierto": "Acierto: gancho y retención claramente por encima de lo normal del canal.",
    "normal": "Dentro de lo normal del canal.",
    "sin datos": "Aún no hay lecturas con 24 h o más.",
}


def guion_de(ficha):
    """Busca la locución del vídeo en el repo. Devuelve el texto o None."""
    lote, num = ficha.get("lote"), ficha.get("numero")
    if ficha.get("guion"):
        candidatos = [os.path.join(RAIZ, ficha["guion"])]
    else:
        candidatos = [os.path.join(RAIZ, "lotes", lote or "", "generadores", f"{num}-guion.txt"),
                      os.path.join(RAIZ, "lotes", lote or "", "guion.txt")]
        candidatos += glob.glob(os.path.join(RAIZ, "motor", "ejemplos", (lote or "").replace("prueba-", ""), "guion.txt"))
    for c in candidatos:
        if os.path.isfile(c):
            return open(c, encoding="utf-8").read()
    md = os.path.join(RAIZ, "lotes", lote or "", "guiones.md")
    if os.path.isfile(md) and num and num.isdigit():
        t = open(md, encoding="utf-8").read()
        bloques = re.findall(r"\*\*Locución\*\*[^\n]*\n\n(?:>\s*)?(.+?)\n\n", t, re.S)
        if len(bloques) >= int(num):
            return bloques[int(num) - 1]
    return None


def frases_con_tiempo(texto, duracion):
    """[(inicio, fin, frase)] repartiendo las palabras de forma uniforme por la duración."""
    frases = [f.strip() for f in re.split(r"(?<=[.?!:])\s+|(?<=…)\s+(?=[A-ZÁÉÍÓÚÑ¿¡])", " ".join((texto or "").split())) if f.strip()]
    total = sum(len(F.palabras_de(f)) for f in frases) or 1
    res, hechas = [], 0
    for f in frases:
        n = len(F.palabras_de(f))
        res.append((hechas / total * duracion, (hechas + n) / total * duracion, f))
        hechas += n
    return res


def frase_en(frases, segundo):
    for ini, fin, f in frases:
        if ini <= segundo < fin:
            return f
    return frases[-1][2] if frases else None


def analizar_curva(curva):
    """curva = {segundo: % que sigue viendo}. Devuelve escalones (caídas fuertes) y tramos que aguantan."""
    pts = sorted((float(k), float(v)) for k, v in (curva or {}).items())
    if len(pts) < 4:
        return None
    escalones, aguantan = [], []
    tramos = [((t0, p0), (t1, p1), (p0 - p1) / (t1 - t0)) for (t0, p0), (t1, p1) in zip(pts, pts[1:]) if t1 > t0]
    # En los 5 primeros segundos todos los vídeos pierden mucho: eso lo mide el gancho, no es un «escalón».
    # Después, es escalón lo que cae bastante más deprisa que el resto de ESTE vídeo.
    tarde = [pend for (t0, _), _, pend in tramos if t0 >= INICIO_ESCALONES]
    umbral = max(CAIDA, 2.5 * E.mediana(tarde)) if tarde else CAIDA
    for (t0, p0), (t1, p1), pendiente in tramos:
        if t0 >= INICIO_ESCALONES and pendiente >= umbral:
            escalones.append({"desde": t0, "hasta": t1, "de": p0, "a": p1, "por_segundo": pendiente})
        elif t0 >= INICIO_ESCALONES and t1 - t0 >= 3 and pendiente <= AGUANTA:
            aguantan.append({"desde": t0, "hasta": t1, "de": p0, "a": p1})
    en3 = next((p for t, p in pts if t >= 3), None)
    en10 = next((p for t, p in pts if t >= 10), None)
    return {"puntos": pts, "en_3s": en3, "en_10s": en10, "pierde_en_3s": None if en3 is None else 100 - en3,
            "escalones": sorted(escalones, key=lambda e: -e["por_segundo"])[:3], "aguantan": aguantan[:3]}


def diagnostico(indices, variables):
    g = indices.get("yt_se_quedan") or indices.get("tt_sigue_3s")
    r = indices.get("yt_seg_por_vista") or indices.get("tt_medio_s")
    a = indices.get("yt_vistas")
    if g is None and r is None:
        return "sin datos"
    if g is not None and g < BAJO:
        fuera = []
        if (variables.get("f0_palabras") or 0) > 5:
            fuera.append(f"{variables['f0_palabras']} palabras en pantalla en el fotograma 0 (norma: 5 o menos)")
        if (variables.get("gancho_palabras") or 0) > 9:
            fuera.append(f"primera frase de {variables['gancho_palabras']} palabras (norma: 9 como mucho)")
        if variables.get("f0_literal") is False:
            fuera.append("el primer fotograma es una metáfora, no la cosa de la que se habla")
        return ("primer segundo", fuera) if fuera else "tema"
    if r is not None and r < BAJO:
        return "ritmo"
    if g is not None and r is not None and g >= ALTO and r >= ALTO:
        return "acierto"
    if g is not None and r is not None and g >= 1 and r >= 1 and a is not None and a < 0.7:
        return "distribución"
    return "normal"


def autopsia(fila, referencias, mediciones, data=None):
    indices = {}
    for m, x in fila["metricas"].items():
        indices[m] = E.indice_relativo(x["valor"], referencias.get(m)) if x["valor"] is not None else None
    d = diagnostico(indices, fila["variables"])
    fuera = []
    if isinstance(d, tuple):
        d, fuera = d
    bloque = ((mediciones.get("videos") or {}).get(fila["id"]) or {})
    curva_tt = None
    for edad in ("48", "168", "24"):
        curva_tt = ((bloque.get("tiktok") or {}).get(edad) or {}).get("curva") or curva_tt
        if curva_tt:
            break
    curva_tt = curva_tt or ((bloque.get("tiktok") or {}).get("ultima") or {}).get("curva")
    dur = fila["variables"].get("duracion_s")
    curva_yt = None
    for v in (data or {}).get("videos") or []:
        if v["id"] == fila["id"] and v.get("curva") and dur:
            curva_yt = {round(x * dur, 1): y for x, y in v["curva"]}
    guion = guion_de(fila["variables"]) if fila["ficha"] else None
    frases = frases_con_tiempo(guion, dur) if guion and dur else []
    return {"id": fila["id"], "titulo": fila["titulo"], "indices": indices, "diagnostico": d, "fuera_de_norma": fuera,
            "curva_tiktok": analizar_curva(curva_tt), "curva_youtube": analizar_curva(curva_yt), "frases": frases,
            "metricas": fila["metricas"], "variables": fila["variables"]}


def accion(a):
    d = a["diagnostico"]
    if d == "primer segundo":
        return "Rehacer el arranque del próximo vídeo parecido: " + "; ".join(a["fuera_de_norma"]) + "."
    if d == "tema":
        return "No repetir este tipo de tema sin cambiar el ángulo; apuntarlo en `lotes/IDEAS.md`."
    if d == "ritmo":
        c = a["curva_tiktok"] or a["curva_youtube"]
        if c and c["escalones"] and a["frases"]:
            e = c["escalones"][0]
            return f"Revisar el tramo del segundo {round(e['desde'])}–{round(e['hasta'])} («{frase_en(a['frases'], e['desde'])}»)."
        return "Mirar la curva de retención cuando la plataforma la dé y localizar el tramo."
    if d == "acierto":
        return "Apuntar qué tenía de distinto (ver variables) y repetirlo en otro tema para comprobar que no fue el tema."
    if d == "distribución":
        return "Ninguna sobre el vídeo. Comprobar hora de publicación y si salió pegado a otro."
    return "Ninguna."


def a_markdown(a):
    from analisis import n1, n0
    L = [f"### {a['titulo']} (`{a['id']}`)", ""]
    if a["diagnostico"] == "sin datos":
        return "\n".join(L + [DIAGNOSTICOS["sin datos"], ""])
    L += ["| | Valor | Edad de la lectura | Frente al canal |", "|---|---|---|---|"]
    for m in ("yt_se_quedan", "tt_sigue_3s", "yt_seg_por_vista", "tt_medio_s", "tt_completo", "yt_vistas", "tt_vistas"):
        x = a["metricas"][m]
        if x["valor"] is None:
            continue
        num = n0(x["valor"]) if m.endswith("vistas") else n1(x["valor"])
        L.append(f"| {T.METRICAS[m][2]} | {num} {T.METRICAS[m][4]} | {round(x['edad_h'])} h{' (provisional)' if x['provisional'] else ''} | {n1(a['indices'][m], 2)} |")
    L += ["", f"**Diagnóstico: {DIAGNOSTICOS[a['diagnostico']]}**"]
    if a["fuera_de_norma"]:
        L.append("Fuera de norma: " + "; ".join(a["fuera_de_norma"]) + ".")
    for nombre, c in (("TikTok", a["curva_tiktok"]), ("YouTube", a["curva_youtube"])):
        if not c:
            continue
        L += ["", f"Curva de {nombre}: se va el **{n1(c['pierde_en_3s'], 0)} %** en los 3 primeros segundos"
              + (f"; en el segundo 10 queda el {n1(c['en_10s'], 0)} %." if c["en_10s"] is not None else ".")]
        for e in c["escalones"]:
            f = frase_en(a["frases"], e["desde"])
            L.append(f"- Escalón en {round(e['desde'])}–{round(e['hasta'])} s ({n1(e['de'], 0)} → {n1(e['a'], 0)} %)"
                     + (f": «{f}»" if f else ""))
        for e in c["aguantan"]:
            f = frase_en(a["frases"], (e["desde"] + e["hasta"]) / 2)
            L.append(f"- Aguanta en {round(e['desde'])}–{round(e['hasta'])} s ({n1(e['de'], 0)} → {n1(e['a'], 0)} %)"
                     + (f": «{f}»" if f else ""))
    if a["frases"] and (a["curva_tiktok"] or a["curva_youtube"]):
        L.append("_Las frases se sitúan por estimación (±2 s)._")
    L += ["", f"**Acción:** {accion(a)}", ""]
    return "\n".join(L)


def ejecutar(escribir=True, fichas=None, mediciones=None, data=None, edad_minima=24):
    import analisis as A
    fichas = F.cargar() if fichas is None else fichas
    mediciones = M.cargar() if mediciones is None else mediciones
    if data is None:
        ruta = os.path.join(ESTADISTICAS, "datos", "data.json")
        data = json.load(open(ruta, encoding="utf-8")) if os.path.exists(ruta) else {}
    filas = T.construir(fichas, mediciones, edad_minima=edad_minima)
    filas.sort(key=lambda f: f.get("publicado") or "", reverse=True)
    ref = {m: E.mediana([f["metricas"][m]["valor"] for f in filas]) for m in T.METRICAS}
    autos = [autopsia(f, ref, mediciones, data) for f in filas]
    con = [a for a in autos if a["diagnostico"] != "sin datos"]
    if escribir:
        L = ["# Autopsias por vídeo", "",
             "Generado por `python3 estadisticas/estudio todo`. Una por vídeo con lecturas de 24 h o más, la más reciente arriba. "
             "El índice «frente al canal» es el valor dividido por la mediana del canal (1,00 = lo normal).", "",
             f"Vídeos con autopsia: {len(con)} de {len(autos)}. "
             + ("Con menos de 5 vídeos la «mediana del canal» es muy inestable: los diagnósticos son orientativos." if len(con) < 5 else ""), ""]
        L += [a_markdown(a) for a in con]
        pendientes = [a["titulo"] for a in autos if a["diagnostico"] == "sin datos"]
        if pendientes:
            L += ["## Aún sin lecturas de 24 h", "", ", ".join(pendientes) + ".", ""]
        os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
        with open(SALIDA, "w", encoding="utf-8") as f:
            f.write("\n".join(L))
    return autos
