"""Datos extra que el estudio pide a YouTube: audiencia por vídeo y comentarios.

Lo llama estadisticas/recoger.py dentro de un try: si algo de aquí falla, la recogida diaria sigue igual.
Cada consulta es opcional: YouTube no da demografía si el vídeo no llega a su umbral (no publicado).
No importa nada del resto del estudio, para no depender de ello en la recogida.
"""
import datetime as dt
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTADISTICAS = os.path.dirname(AQUI)
COMENTARIOS = os.path.join(ESTADISTICAS, "datos", "comentarios.json")
EDAD_MINIMA_H = 48        # antes Analytics no suele tener nada por vídeo
EDAD_MAXIMA_DIAS = 14     # después casi no cambia: se conserva la última (y se ahorran consultas)


def audiencia_video(yt, vid, inicio, fin, avisar=print):
    """Edad × género y países de UN vídeo. Devuelve None si YouTube no da nada."""
    def q(**p):
        try:
            return yt.analytics(startDate=inicio, endDate=fin, filters=f"video=={vid}", **p)
        except Exception as e:  # umbral de privacidad, cuota o lo que sea: se sigue sin ese dato
            avisar(f"  (aviso) audiencia de {vid} sin {p.get('dimensions')} -> {str(e)[:100]}")
            return []
    edad = q(dimensions="ageGroup,gender", metrics="viewerPercentage")
    paises = q(dimensions="country", metrics="views,estimatedMinutesWatched", sort="-views", maxResults=10)
    if not edad and not paises:
        return None
    return {"hasta": fin,
            "vistas": sum(f["views"] for f in paises) or None,
            "edadGenero": [[f["ageGroup"], f["gender"], f["viewerPercentage"]] for f in edad],
            "paises": [[f["country"], f["views"], f["estimatedMinutesWatched"]] for f in paises]}


def comentarios_video(yt, vid, maximo=100):
    """Comentarios principales de un vídeo: texto, fecha y likes. Sin autor."""
    res, token = [], None
    while len(res) < maximo:
        p = dict(part="snippet", videoId=vid, maxResults=50, textFormat="plainText", order="time")
        if token:
            p["pageToken"] = token
        r = yt.data("commentThreads", **p)
        for it in r.get("items", []):
            s = it["snippet"]["topLevelComment"]["snippet"]
            res.append({"id": it["id"], "video": vid, "red": "youtube", "texto": s.get("textDisplay") or "",
                        "fecha": (s.get("publishedAt") or "")[:10], "likes": s.get("likeCount", 0),
                        "respuestas": it["snippet"].get("totalReplyCount", 0)})
        token = r.get("nextPageToken")
        if not token:
            break
    return res


def completar(yt, videos, inicio, fin, previo=None, avisar=print):
    """Añade «audiencia» a cada vídeo de la lista (en el sitio) y guarda los comentarios aparte.
    previo = vídeos del data.json anterior, para conservar la audiencia de los que ya no se piden."""
    anterior = {v["id"]: v.get("audiencia") for v in (previo or []) if v.get("audiencia")}
    pedidos = 0
    for v in videos:
        horas = v.get("horasPublicado") or 0
        if EDAD_MINIMA_H <= horas <= EDAD_MAXIMA_DIAS * 24:
            a = audiencia_video(yt, v["id"], inicio, fin, avisar)
            pedidos += 1
            v["audiencia"] = a or anterior.get(v["id"])
        elif anterior.get(v["id"]):
            v["audiencia"] = anterior[v["id"]]
    guardados = {}
    if os.path.exists(COMENTARIOS):
        try:
            guardados = {c["id"]: c for c in json.load(open(COMENTARIOS, encoding="utf-8")).get("comentarios", [])}
        except Exception:
            guardados = {}
    nuevos = 0
    for v in videos:
        if not v.get("comentarios"):
            continue
        try:
            for c in comentarios_video(yt, v["id"]):
                nuevos += c["id"] not in guardados
                guardados[c["id"]] = c
        except Exception as e:
            avisar(f"  (aviso) comentarios de {v['id']} -> {str(e)[:100]}")
            if "403" in str(e) or "401" in str(e):
                avisar("  (aviso) el permiso actual no deja leer comentarios: no se piden más hoy")
                break
    if guardados:
        os.makedirs(os.path.dirname(COMENTARIOS), exist_ok=True)
        with open(COMENTARIOS, "w", encoding="utf-8") as f:
            json.dump({"actualizado": dt.date.today().isoformat(),
                       "comentarios": sorted(guardados.values(), key=lambda c: (c["fecha"], c["id"]))},
                      f, ensure_ascii=False, indent=1)
            f.write("\n")
    return {"audiencias_pedidas": pedidos, "comentarios_nuevos": nuevos, "comentarios": len(guardados)}
