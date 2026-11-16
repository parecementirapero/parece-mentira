#!/usr/bin/env python3
"""Recoge las estadísticas del canal de YouTube y las guarda en datos/data.json.

Solo usa la librería estándar de Python (nada que instalar).

Credenciales (variables de entorno, NUNCA en el repo):
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
  -> se consiguen una sola vez con autorizar.py (ver README.md)

Uso:
  python3 estadisticas/recoger.py                 # datos reales
  python3 estadisticas/recoger.py --si-toca       # solo si hoy aún no se ha actualizado (GitHub Actions)
"""
import argparse, datetime as dt, glob, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from zoneinfo import ZoneInfo

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALIDA = os.path.join(AQUI, "datos", "data.json")
MADRID = ZoneInfo("Europe/Madrid")
INICIO_CANAL = "2026-11-01"      # primera fecha que se pide a Analytics
DIAS_DIARIO = 90                 # días de la serie diaria del canal

FUENTES = {  # insightTrafficSourceType -> nombre en la web
    "SHORTS": "Feed de Shorts", "YT_SEARCH": "Búsqueda", "YT_CHANNEL": "Página del canal",
    "SUBSCRIBER": "Suscripciones", "BROWSE": "Inicio / explorar", "RELATED_VIDEO": "Vídeos sugeridos",
    "EXT_URL": "Externo", "NO_LINK_OTHER": "Directo / otros", "NOTIFICATION": "Notificaciones",
    "PLAYLIST": "Listas", "YT_OTHER_PAGE": "Otras páginas de YouTube", "HASHTAGS": "Hashtags",
    "SOUND_PAGE": "Página de sonido", "END_SCREEN": "Pantalla final",
}
TEMAS_HASHTAG = {  # hashtag de la descripción -> tema (si no hay etiqueta manual)
    "cotidiano": "Cotidiano", "vidacotidiana": "Cotidiano", "cuerpohumano": "Cotidiano",
    "historia": "Histórico", "espacio": "Espacio", "astronomia": "Espacio", "luna": "Espacio",
    "ciencia": "Ciencia", "misterio": "Misterio", "misterios": "Misterio", "humor": "Humor",
}


# ---------------------------------------------------------------- HTTP / OAuth
def _http(url, data=None, headers=None, intentos=4):
    for i in range(intentos):
        try:
            req = urllib.request.Request(url, data=data, headers=headers or {})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            cuerpo = e.read().decode(errors="replace")
            if e.code in (429, 500, 502, 503) and i < intentos - 1:
                time.sleep(2 ** i * 3); continue
            raise RuntimeError(f"HTTP {e.code} en {url.split('?')[0]}: {cuerpo[:500]}") from None
        except urllib.error.URLError:
            if i < intentos - 1:
                time.sleep(2 ** i * 3); continue
            raise


def token_de_acceso():
    faltan = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.environ.get(k)]
    if faltan:
        sys.exit("Faltan variables de entorno: " + ", ".join(faltan) + " (ver estadisticas/README.md)")
    cuerpo = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    try:
        return _http("https://oauth2.googleapis.com/token", cuerpo)["access_token"]
    except RuntimeError as e:
        if "invalid_grant" in str(e):
            sys.exit("El permiso de Google ha caducado o se ha revocado (invalid_grant). "
                     "Vuelve a ejecutar autorizar.py y actualiza el secreto YT_REFRESH_TOKEN. "
                     "Si pasa cada 7 días: la app de Google Cloud está en modo «Prueba»; pásala a «En producción».")
        raise


class YouTube:
    def __init__(self, token):
        self.h = {"Authorization": f"Bearer {token}"}

    def data(self, recurso, **p):
        return _http(f"https://www.googleapis.com/youtube/v3/{recurso}?" + urllib.parse.urlencode(p), headers=self.h)

    def analytics(self, **p):
        p.setdefault("ids", "channel==MINE")
        r = _http("https://youtubeanalytics.googleapis.com/v2/reports?" + urllib.parse.urlencode(p), headers=self.h)
        cols = [c["name"] for c in r.get("columnHeaders", [])]
        return [dict(zip(cols, fila)) for fila in r.get("rows", []) or []]


# ---------------------------------------------------------------- utilidades
def duracion_seg(iso):  # PT1M5S -> 65
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m: return None
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def lotes_por_video():
    """Busca en lotes/*/estado.md los enlaces de YouTube para saber de qué lote es cada vídeo."""
    res = {}
    for f in glob.glob(os.path.join(RAIZ, "lotes", "*", "estado.md")):
        lote = os.path.basename(os.path.dirname(f))
        for vid in re.findall(r"youtube\.com/shorts/([A-Za-z0-9_-]{11})", open(f, encoding="utf-8").read()):
            res.setdefault(vid, lote)
    return res


def tema_por_hashtags(descripcion):
    for tag in re.findall(r"#(\w+)", (descripcion or "").lower()):
        if tag in TEMAS_HASHTAG:
            return TEMAS_HASHTAG[tag]
    return "Sin etiquetar"


def cargar_etiquetas():
    f = os.path.join(AQUI, "etiquetas.json")
    if not os.path.exists(f): return {}
    return {k: v for k, v in json.load(open(f, encoding="utf-8")).items() if not k.startswith("_")}


# ---------------------------------------------------------------- recogida
def recoger():
    yt = YouTube(token_de_acceso())
    ahora = dt.datetime.now(MADRID)
    hoy = ahora.date()

    canal = yt.data("channels", part="snippet,contentDetails,statistics", mine="true")["items"][0]
    subidas = canal["contentDetails"]["relatedPlaylists"]["uploads"]

    ids, token = [], None
    while True:
        p = dict(part="contentDetails", playlistId=subidas, maxResults=50)
        if token: p["pageToken"] = token
        r = yt.data("playlistItems", **p)
        ids += [it["contentDetails"]["videoId"] for it in r.get("items", [])]
        token = r.get("nextPageToken")
        if not token: break

    info = {}
    for i in range(0, len(ids), 50):
        r = yt.data("videos", part="snippet,contentDetails,statistics,status", id=",".join(ids[i:i + 50]))
        for v in r.get("items", []):
            info[v["id"]] = v
    publicos = [v for v in info.values() if v["status"]["privacyStatus"] == "public"]

    # --- totales por vídeo desde Analytics (llevan 1-2 días de retraso; los contadores van de la Data API)
    metricas = "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,likes,comments,shares,subscribersGained,subscribersLost"
    base = dict(startDate=INICIO_CANAL, endDate=hoy.isoformat(), dimensions="video", maxResults=200, sort="-views")
    engaged = True
    try:
        filas = yt.analytics(metrics=metricas + ",engagedViews", **base)
    except RuntimeError:
        engaged = False
        filas = yt.analytics(metrics=metricas, **base)
    an = {f["video"]: f for f in filas}

    etiquetas, lotes = cargar_etiquetas(), lotes_por_video()
    videos = []
    for v in sorted(publicos, key=lambda x: x["snippet"]["publishedAt"]):
        vid, sn, st = v["id"], v["snippet"], v["statistics"]
        pub = dt.datetime.fromisoformat(sn["publishedAt"].replace("Z", "+00:00")).astimezone(MADRID)
        dur = duracion_seg(v["contentDetails"]["duration"])
        a = an.get(vid, {})
        horas = (ahora - pub).total_seconds() / 3600
        item = {
            "id": vid, "titulo": re.sub(r"\s*#\w+", "", sn["title"]).strip(),
            "url": f"https://youtube.com/shorts/{vid}",
            "fecha": pub.date().isoformat(), "hora": pub.strftime("%H:%M"), "duracion": dur,
            "vistas": int(st.get("viewCount", 0)), "likes": int(st.get("likeCount", 0)),
            "comentarios": int(st.get("commentCount", 0)),
            "compartidos": a.get("shares"), "subs": (a["subscribersGained"] - a["subscribersLost"]) if a else None,
            "vistasEnganchadas": a.get("engagedViews") if engaged else None,
            "minutosVistos": a.get("estimatedMinutesWatched"),
            "duracionMedia": a.get("averageViewDuration"),
            "pctVisto": round(a["averageViewPercentage"], 1) if a.get("averageViewPercentage") else None,
            "retencion3s": None, "curva": None, "fuentes": None, "vistasDia": None,
            "horasPublicado": round(horas, 1),
            "lote": lotes.get(vid),
        }
        # etiquetas: automáticas y luego las manuales encima
        item["etiquetas"] = {"tema": tema_por_hashtags(sn.get("description"))}
        if item["lote"]: item["etiquetas"]["lote"] = item["lote"]
        item["etiquetas"].update(etiquetas.get(vid, {}))
        item["tema"] = item["etiquetas"].get("tema", "Sin etiquetar")

        if horas >= 48:  # antes Analytics no suele tener la curva
            filtro = f"video=={vid}"
            curva = yt.analytics(startDate=INICIO_CANAL, endDate=hoy.isoformat(), filters=filtro,
                                 dimensions="elapsedVideoTimeRatio", metrics="audienceWatchRatio")
            if curva:
                pts = [(c["elapsedVideoTimeRatio"], c["audienceWatchRatio"] * 100) for c in curva]
                item["curva"] = [[round(x, 3), round(y, 1)] for x, y in pts]
                if dur:
                    objetivo = min(1.0, 3 / dur)
                    item["retencion3s"] = round(min(pts, key=lambda p: abs(p[0] - objetivo))[1], 1)
            fu = yt.analytics(startDate=INICIO_CANAL, endDate=hoy.isoformat(), filters=filtro,
                              dimensions="insightTrafficSourceType", metrics="views", sort="-views")
            tot = sum(f["views"] for f in fu) or 0
            if tot:
                item["fuentes"] = {FUENTES.get(f["insightTrafficSourceType"], f["insightTrafficSourceType"]):
                                   round(f["views"] / tot * 100, 1) for f in fu if f["views"]}
        dias = yt.analytics(startDate=pub.date().isoformat(), endDate=hoy.isoformat(), filters=f"video=={vid}",
                            dimensions="day", metrics="views", sort="day")
        if dias:
            item["vistasDia"] = [[d["day"], d["views"]] for d in dias]
        videos.append(item)

    ini = (hoy - dt.timedelta(days=DIAS_DIARIO)).isoformat()
    diario = yt.analytics(startDate=max(ini, INICIO_CANAL), endDate=hoy.isoformat(), dimensions="day",
                          metrics="views,estimatedMinutesWatched,subscribersGained,subscribersLost,likes", sort="day")
    diario = [{"fecha": d["day"], "vistas": d["views"], "minutos": d["estimatedMinutesWatched"],
               "subs": d["subscribersGained"] - d["subscribersLost"], "likes": d["likes"]} for d in diario]

    return {
        "generado": ahora.isoformat(timespec="seconds"), "ejemplo": False,
        "canal": canal["snippet"]["title"],
        "canalTotales": {"suscriptores": int(canal["statistics"].get("subscriberCount", 0)),
                         "vistas": int(canal["statistics"].get("viewCount", 0)),
                         "videos": len(publicos)},
        "videos": videos, "diario": diario,
        "notas": [] if engaged else ["La API no devolvió «vistas enganchadas» (engagedViews)."],
    }


def ya_actualizado_hoy():
    try:
        g = json.load(open(SALIDA, encoding="utf-8")).get("generado", "")
        return not json.load(open(SALIDA, encoding="utf-8")).get("ejemplo") and g[:10] == dt.datetime.now(MADRID).date().isoformat()
    except Exception:
        return False


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--si-toca", action="store_true", help="no hace nada si ya se actualizó hoy o si aún no son las 8:00 en Madrid")
    args = ap.parse_args()
    if args.si_toca:
        h = dt.datetime.now(MADRID).hour
        if h < 8 or ya_actualizado_hoy():
            print(f"Nada que hacer (hora de Madrid: {h}, ya actualizado hoy: {ya_actualizado_hoy()})")
            sys.exit(0)
    datos = recoger()
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    print(f"OK: {len(datos['videos'])} vídeos públicos, {len(datos['diario'])} días -> {SALIDA}")
