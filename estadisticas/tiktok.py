"""Estadísticas de TikTok con la Display API (Login Kit, scopes user.info.basic, user.info.stats, video.list).

TikTok solo da contadores públicos por vídeo (vistas, likes, comentarios, compartidos): NO da retención
ni tiempo de visionado. Las vistas por día se calculan comparando con la foto del día anterior.

Secretos: TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET, TIKTOK_REFRESH_TOKEN.
El refresh token ROTA en cada uso: se guarda el nuevo con comun.guardar_secreto (necesita GH_PAT).
"""
import datetime as dt, os, urllib.parse
from comun import http, ocultar, guardar_secreto, faltan

API = "https://open.tiktokapis.com/v2"
CAMPOS = "id,title,video_description,create_time,duration,share_url,view_count,like_count,comment_count,share_count"


def refrescar():
    r = http(f"{API}/oauth/token/", urllib.parse.urlencode({
        "client_key": os.environ["TIKTOK_CLIENT_KEY"], "client_secret": os.environ["TIKTOK_CLIENT_SECRET"],
        "grant_type": "refresh_token", "refresh_token": os.environ["TIKTOK_REFRESH_TOKEN"]}).encode())
    if "access_token" not in r:
        raise RuntimeError(f"TikTok no devolvió token ({r.get('error')}: {r.get('error_description')}). "
                           "Vuelve a ejecutar autorizar_tiktok.py y actualiza TIKTOK_REFRESH_TOKEN.")
    ocultar(r["access_token"])
    guardado = True
    if r.get("refresh_token") and r["refresh_token"] != os.environ["TIKTOK_REFRESH_TOKEN"]:
        guardado = guardar_secreto("TIKTOK_REFRESH_TOKEN", r["refresh_token"])
    return r["access_token"], r.get("refresh_expires_in"), guardado


def recoger(madrid):
    if faltan("TIKTOK_CLIENT_KEY", "TIKTOK_CLIENT_SECRET", "TIKTOK_REFRESH_TOKEN"):
        return None
    token, caduca_s, guardado = refrescar()
    h = {"Authorization": f"Bearer {token}"}
    u = http(f"{API}/user/info/?fields=open_id,display_name,username,follower_count,likes_count,video_count", headers=h)
    user = u.get("data", {}).get("user", {})
    videos, cursor = [], None
    for _ in range(50):  # tope de seguridad: 1.000 vídeos
        cuerpo = {"max_count": 20}
        if cursor: cuerpo["cursor"] = cursor
        r = http(f"{API}/video/list/?fields={CAMPOS}", cuerpo, headers=h)
        d = r.get("data", {})
        videos += d.get("videos", [])
        cursor = d.get("cursor")
        if not d.get("has_more"): break
    salida = []
    for v in videos:
        pub = dt.datetime.fromtimestamp(v["create_time"], madrid)
        salida.append({
            "id": str(v["id"]), "titulo": (v.get("title") or v.get("video_description") or "").strip()[:150],
            "url": v.get("share_url"), "fecha": pub.date().isoformat(), "hora": pub.strftime("%H:%M"),
            "duracion": v.get("duration"), "vistas": v.get("view_count", 0), "likes": v.get("like_count", 0),
            "comentarios": v.get("comment_count", 0), "compartidos": v.get("share_count", 0)})
    notas = []
    if caduca_s is not None and caduca_s < 20 * 86400:
        notas.append(f"El permiso de TikTok caduca en {caduca_s // 86400} días: vuelve a ejecutar autorizar_tiktok.py.")
    if not guardado:
        notas.append("TikTok: no se pudo guardar el token renovado (revisa el secreto GH_PAT).")
    return {"cuenta": user.get("username") or user.get("display_name"),
            "totales": {"seguidores": user.get("follower_count"), "likes": user.get("likes_count"),
                        "videos": user.get("video_count")},
            "videos": sorted(salida, key=lambda x: x["fecha"]),
            "permisoCaducaDias": caduca_s // 86400 if caduca_s else None}, notas
