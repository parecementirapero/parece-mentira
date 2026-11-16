#!/usr/bin/env python3
"""Recoge las estadísticas de YouTube, TikTok e Instagram y las guarda en datos/data.json.

Solo usa la librería estándar de Python (nada que instalar).

Credenciales (variables de entorno / secretos de GitHub, NUNCA en el repo), ver README.md:
  YouTube:   YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN      (autorizar.py)
  TikTok:    TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET, TIKTOK_REFRESH_TOKEN  (autorizar_tiktok.py)
  Instagram: IG_TOKEN                                              (panel de Meta)
  GH_PAT:    para guardar los tokens que TikTok/Instagram renuevan
Cada red es independiente: si falta o falla una, se conservan sus datos del día anterior.

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
sys.path.insert(0, AQUI)
from comun import http as _http, faltan  # noqa: E402
import tiktok, instagram  # noqa: E402


def token_de_acceso():
    cuerpo = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    try:
        return _http("https://oauth2.googleapis.com/token", cuerpo)["access_token"]
    except RuntimeError as e:
        if "invalid_grant" in str(e):
            raise RuntimeError("El permiso de Google ha caducado o se ha revocado (invalid_grant). "
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
def audiencia_youtube(yt, hoy):
    """Datos de audiencia del canal (últimos 28 días). Cada consulta es opcional:
    YouTube no da algunos datos si hay pocas vistas (umbral de privacidad)."""
    ini = max(INICIO_CANAL, (hoy - dt.timedelta(days=28)).isoformat())
    fin = hoy.isoformat()
    def q(**p):
        try:
            return yt.analytics(startDate=ini, endDate=fin, **p)
        except Exception as e:
            print("  (aviso) Analytics sin", p.get("dimensions"), "->", str(e)[:120])
            return []
    paises = q(dimensions="country", metrics="views,estimatedMinutesWatched", sort="-views", maxResults=10)
    disp = q(dimensions="deviceType", metrics="views", sort="-views")
    subs = q(dimensions="subscribedStatus", metrics="views,averageViewPercentage")
    edad = q(dimensions="ageGroup,gender", metrics="viewerPercentage")
    fuentes = q(dimensions="insightTrafficSourceType", metrics="views", sort="-views")
    sistema = q(dimensions="operatingSystem", metrics="views", sort="-views", maxResults=6)
    return {
        "desde": ini,
        "paises": [[f["country"], f["views"], f["estimatedMinutesWatched"]] for f in paises],
        "dispositivos": [[f["deviceType"], f["views"]] for f in disp],
        "suscritos": [[f["subscribedStatus"], f["views"], f.get("averageViewPercentage")] for f in subs],
        "edadGenero": [[f["ageGroup"], f["gender"], f["viewerPercentage"]] for f in edad],
        "fuentes": [[FUENTES.get(f["insightTrafficSourceType"], f["insightTrafficSourceType"]), f["views"]] for f in fuentes],
        "sistemas": [[f["operatingSystem"], f["views"]] for f in sistema],
    }


def recoger_youtube():
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
        item["etiquetas"].update({k: x for k, x in etiquetas.get(vid, {}).items() if k not in ("tiktok", "instagram")})
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

    extra = audiencia_youtube(yt, hoy)
    return {
        "youtubeExtra": extra,
        "canal": canal["snippet"]["title"],
        "canalTotales": {"suscriptores": int(canal["statistics"].get("subscriberCount", 0)),
                         "vistas": int(canal["statistics"].get("viewCount", 0)),
                         "videos": len(publicos)},
        "videos": videos, "diario": diario,
        "notas": [] if engaged else ["La API no devolvió «vistas enganchadas» (engagedViews)."],
    }


# ---------------------------------------------------------------- unir redes
def _palabras(t):
    return {w for w in re.findall(r"[a-záéíóúñü0-9]{4,}", (t or "").lower())}


def enlaces_entre_redes(etiquetas):
    """Grupos {youtube, tiktok, instagram} sacados de lotes/*/estado.md y de etiquetas.json."""
    pat = {"youtube": r"youtube\.com/shorts/([A-Za-z0-9_-]{11})",
           "instagram": r"instagram\.com/(?:[\w.]+/)?reel/([A-Za-z0-9_-]+)",
           "tiktok": r"tiktok\.com/@[\w.]+/video/(\d+)"}
    grupos = []
    for f in sorted(glob.glob(os.path.join(RAIZ, "lotes", "*", "estado.md"))):
        texto = open(f, encoding="utf-8").read()
        sueltos = {}
        for linea in texto.splitlines():
            g = {red: m.group(1) for red, p in pat.items() if (m := re.search(p, linea))}
            if len(g) >= 2: grupos.append(g)
            elif len(g) == 1: sueltos.setdefault(*next(iter(g.items())))
        todos = {red: set(re.findall(p, texto)) for red, p in pat.items()}
        if all(len(v) <= 1 for v in todos.values()) and sum(len(v) for v in todos.values()) >= 2:
            grupos.append({red: next(iter(v)) for red, v in todos.items() if v})
    for yid, e in etiquetas.items():
        g = {"youtube": yid, **{r: e[r] for r in ("tiktok", "instagram") if e.get(r)}}
        if len(g) >= 2: grupos.append(g)
    return grupos


def construir_contenidos(datos, etiquetas):
    """Une el mismo vídeo publicado en varias redes. Primero por enlaces; si no, por fecha y título."""
    yt = {v["id"]: v for v in datos.get("videos", [])}
    tt = {v["id"]: v for v in (datos.get("tiktok") or {}).get("videos", [])}
    ig = {v["codigo"]: v for v in (datos.get("instagram") or {}).get("videos", [])}
    usados = {"youtube": set(), "tiktok": set(), "instagram": set()}
    cont = []
    for g in enlaces_entre_redes(etiquetas):
        g = {r: i for r, i in g.items() if i in {"youtube": yt, "tiktok": tt, "instagram": ig}[r]}
        if len(g) < 2 or any(i in usados[r] for r, i in g.items()): continue
        for r, i in g.items(): usados[r].add(i)
        cont.append(g)
    for yid in yt:
        if yid not in usados["youtube"]:
            usados["youtube"].add(yid); cont.append({"youtube": yid})
    for red, tabla in (("tiktok", tt), ("instagram", ig)):
        for i, v in tabla.items():
            if i in usados[red]: continue
            mejor, nota = None, 0.0
            f = dt.date.fromisoformat(v["fecha"])
            for c in cont:
                if red in c or "youtube" not in c: continue
                y = yt[c["youtube"]]
                if abs((dt.date.fromisoformat(y["fecha"]) - f).days) > 1: continue
                a, b = _palabras(y["titulo"]), _palabras(v["titulo"])
                j = len(a & b) / max(1, len(a | b))
                if j > nota: mejor, nota = c, j
            usados[red].add(i)
            if mejor and nota >= 0.25: mejor[red] = i
            else: cont.append({red: i})
    salida = []
    for c in cont:
        base = yt.get(c.get("youtube")) or tt.get(c.get("tiktok")) or ig.get(c.get("instagram"))
        salida.append({"clave": c.get("youtube") or c.get("tiktok") or c.get("instagram"),
                       "titulo": base["titulo"], "fecha": base["fecha"], **c})
    return sorted(salida, key=lambda x: x["fecha"])


def foto_del_dia(datos, previo, hoy):
    """Guarda cada día las vistas de cada vídeo: así hay vistas por día también en TikTok e Instagram."""
    hist = dict((previo or {}).get("historico") or {})
    hist[hoy] = {"seguidores": {"youtube": (datos.get("canalTotales") or {}).get("suscriptores"),
                                "tiktok": ((datos.get("tiktok") or {}).get("totales") or {}).get("seguidores"),
                                "instagram": ((datos.get("instagram") or {}).get("totales") or {}).get("seguidores")},
                 "youtube": {v["id"]: v["vistas"] for v in datos.get("videos", [])},
                 "tiktok": {v["id"]: v["vistas"] for v in (datos.get("tiktok") or {}).get("videos", [])},
                 "instagram": {v["codigo"]: v["vistas"] for v in (datos.get("instagram") or {}).get("videos", []) if v.get("vistas") is not None}}
    return {k: hist[k] for k in sorted(hist)[-120:]}


def cargar_previo():
    try:
        d = json.load(open(SALIDA, encoding="utf-8"))
        return None if d.get("ejemplo") else d
    except Exception:
        return None


def limpiar_secretos():
    """Quita espacios y saltos de línea pegados por error en los secretos."""
    for k in list(os.environ):
        if k.startswith(("YT_", "TIKTOK_", "IG_")) or k == "GH_PAT":
            v = os.environ[k]
            v = v.split("=", 1)[1] if v.startswith(k + "=") else v  # por si se pegó «NOMBRE=valor»
            os.environ[k] = v.strip()


def recoger_todo():
    limpiar_secretos()
    ahora = dt.datetime.now(MADRID)
    previo = cargar_previo() or {}
    datos, notas = {}, []

    if faltan("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"):
        notas.append("YouTube sin conectar.")
        yt = {k: previo[k] for k in ("canal", "canalTotales", "videos", "diario", "youtubeExtra") if k in previo}
    else:
        try:
            yt = recoger_youtube(); notas += yt.pop("notas", [])
        except Exception as e:
            print(f"::error::YouTube: {e}"); notas.append(f"YouTube falló hoy ({str(e)[:140]}); se muestran los datos anteriores.")
            yt = {k: previo[k] for k in ("canal", "canalTotales", "videos", "diario", "youtubeExtra") if k in previo}
    datos.update(yt)
    datos.setdefault("videos", []); datos.setdefault("diario", [])

    for nombre, mod in (("tiktok", tiktok), ("instagram", instagram)):
        try:
            r = mod.recoger(MADRID)
            if r is None:
                datos[nombre] = previo.get(nombre)
                if not datos[nombre]: notas.append(f"{ {'tiktok': 'TikTok', 'instagram': 'Instagram'}[nombre]} sin conectar.")
            else:
                datos[nombre], n = r; notas += n
        except Exception as e:
            print(f"::error::{nombre}: {e}")
            notas.append(f"{ {'tiktok': 'TikTok', 'instagram': 'Instagram'}[nombre]} falló hoy ({str(e)[:140]}); se muestran los datos anteriores.")
            datos[nombre] = previo.get(nombre)

    datos["contenidos"] = construir_contenidos(datos, cargar_etiquetas())
    datos["historico"] = foto_del_dia(datos, previo, ahora.date().isoformat())
    return {"generado": ahora.isoformat(timespec="seconds"), "ejemplo": False, **datos, "notas": notas}


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
    datos = recoger_todo()
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    tt, ig = datos.get("tiktok") or {}, datos.get("instagram") or {}
    print(f"OK: YouTube {len(datos['videos'])} · TikTok {len(tt.get('videos', []))} · Instagram {len(ig.get('videos', []))} "
          f"· {len(datos['contenidos'])} contenidos -> {SALIDA}")
    for n in datos["notas"]: print("  nota:", n)
