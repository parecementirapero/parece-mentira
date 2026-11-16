"""Estadísticas de Instagram (Reels) con la Instagram API with Instagram Login.

Necesita cuenta profesional (creador o empresa). Por reel: vistas, alcance, likes, comentarios,
compartidos, guardados, tiempo medio visto y tasa de salto (reels_skip_rate) si la API la da.

Secretos: IG_TOKEN (token largo de 60 días generado en el panel de Meta).
Se renueva solo una vez por semana (refresh_access_token) y se guarda el nuevo con GH_PAT.
"""
import datetime as dt, os, urllib.parse
from comun import http, ocultar, guardar_secreto, faltan

API = "https://graph.instagram.com"
METRICAS = ["views", "reach", "likes", "comments", "shares", "saved", "total_interactions",
            "ig_reels_avg_watch_time", "ig_reels_video_view_total_time", "reels_skip_rate"]


def _get(ruta, token, **p):
    p["access_token"] = token
    return http(f"{API}/{ruta}?" + urllib.parse.urlencode(p))


def renovar_si_toca(token, hoy):
    """Una vez por semana (lunes) amplía el token otros 60 días."""
    if hoy.weekday() != 0:
        return token, None
    try:
        r = http(f"{API}/refresh_access_token?" + urllib.parse.urlencode({"grant_type": "ig_refresh_token", "access_token": token}))
    except RuntimeError as e:
        return token, f"Instagram: no se pudo renovar el token ({str(e)[:120]})."
    nuevo = r.get("access_token")
    if nuevo and nuevo != token:
        ocultar(nuevo)
        if not guardar_secreto("IG_TOKEN", nuevo):
            return nuevo, "Instagram: no se pudo guardar el token renovado (revisa GH_PAT)."
        return nuevo, None
    return token, None


def insights(mid, token):
    """Pide todas las métricas; si la API rechaza alguna, la quita y reintenta."""
    metricas = list(METRICAS)
    while metricas:
        try:
            r = _get(f"{mid}/insights", token, metric=",".join(metricas))
            return {d["name"]: (d.get("values") or [{}])[0].get("value") for d in r.get("data", [])}
        except RuntimeError as e:
            malas = [m for m in metricas if m in str(e)]
            if not malas:
                if len(metricas) <= 3: return {}
                malas = [metricas[-1]]
            metricas = [m for m in metricas if m not in malas]
    return {}


def recoger(madrid):
    if faltan("IG_TOKEN"):
        return None
    hoy = dt.datetime.now(madrid).date()
    token, nota = renovar_si_toca(os.environ["IG_TOKEN"], hoy)
    ocultar(token)
    yo = _get("me", token, fields="user_id,username,followers_count,media_count")
    medios, url = [], None
    r = _get("me/media", token, fields="id,caption,media_type,media_product_type,timestamp,permalink,like_count,comments_count", limit=50)
    for _ in range(20):
        medios += r.get("data", [])
        url = r.get("paging", {}).get("next")
        if not url: break
        r = http(url)
    salida = []
    for m in medios:
        if m.get("media_product_type") != "REELS":
            continue
        pub = dt.datetime.strptime(m["timestamp"], "%Y-%m-%dT%H:%M:%S%z").astimezone(madrid)
        ins = insights(m["id"], token)
        corto = (m.get("permalink") or "").rstrip("/").split("/")[-1]
        avg_ms = ins.get("ig_reels_avg_watch_time")
        salida.append({
            "id": m["id"], "codigo": corto, "titulo": (m.get("caption") or "").split("\n")[0][:150],
            "url": m.get("permalink"), "fecha": pub.date().isoformat(), "hora": pub.strftime("%H:%M"),
            "vistas": ins.get("views"), "alcance": ins.get("reach"),
            "likes": ins.get("likes", m.get("like_count")), "comentarios": ins.get("comments", m.get("comments_count")),
            "compartidos": ins.get("shares"), "guardados": ins.get("saved"),
            "tiempoMedio": round(avg_ms / 1000, 1) if avg_ms else None,
            "tasaSalto": ins.get("reels_skip_rate")})
    return {"cuenta": yo.get("username"),
            "totales": {"seguidores": yo.get("followers_count"), "videos": len(salida)},
            "videos": sorted(salida, key=lambda x: x["fecha"])}, ([nota] if nota else [])
