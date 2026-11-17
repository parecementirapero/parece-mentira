#!/usr/bin/env python3
"""Publica un vídeo del lote como Reel en Instagram por la API oficial de Meta (sin navegador).

Lo usa el agente del turno SOLO después de que una persona escriba «ok» en el chat del lote.
Hay dos maneras, según lo que haya en claves.txt (carpeta local del turno, nunca en el repo):

  A) Subida directa del archivo (recomendada; app de Meta con «Facebook Login» y la cuenta de Instagram
     enlazada a una página de Facebook):
       IG_USER_ID=...        (número de la cuenta de Instagram)
       IG_FB_TOKEN=...       (token de página; se saca con: python3 publicar/autorizar_instagram.py --claves claves.txt)
  B) Con dirección pública (app de Meta con «Instagram Login», la de las estadísticas). Meta se descarga el
     vídeo de una URL https pública, así que hay que pasar --video-url:
       IG_TOKEN=...          (token de 60 días con el permiso instagram_business_content_publish)

Uso:
  python3 publicar/subir_instagram.py --claves claves.txt --metadatos lotes/<lote>/metadatos.json \
      --clave 01 --video "<carpeta>/lotes/<lote>/01-....mp4" [--comentario] [--prueba] [--forzar]
      [--video-url https://...mp4] [--portada-url https://...jpg] [--metodo auto|directa|url]

--prueba       comprueba claves, cuenta, cupo, metadatos y archivo sin publicar nada.
--comentario   después de publicar, escribe el «comentario» de metadatos.json (no se puede fijar por API).
--forzar       publica aunque el registro o la cuenta digan que ya está.
La portada sale del fotograma `portada.t` de metadatos.json (o de --portada-url si se pasa una imagen pública).
Imprime una línea JSON: {"ok": true, "red": "instagram", "id": ..., "url": ...}.
"""
import argparse
import os
import re
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base  # noqa: E402

HOST_FB = os.environ.get("PM_IG_FB", "https://graph.facebook.com").rstrip("/")
HOST_IG = os.environ.get("PM_IG_IG", "https://graph.instagram.com").rstrip("/")
HOST_SUBIDA = "rupload.facebook.com"
MAXIMO = 300 * 1024 * 1024       # 300 MB (límite de Reels por API)
SEMANA = 7 * 86400

PISTAS = {
    190: "Meta rechaza el token (caducado o retirado). Vuelve a sacarlo: ver publicar/README.md, «Instagram».",
    10: "A la app de Meta le falta el permiso de publicar en Instagram para esta cuenta.",
    200: "A la app de Meta le falta el permiso de publicar en Instagram para esta cuenta.",
    4: "Meta está limitando las peticiones de la app. Espera unos minutos y repite.",
    9: "Meta está limitando las peticiones de la cuenta. Espera unos minutos y repite.",
    25: "La cuenta de Instagram tiene restringido publicar por API.",
    24: "Meta no encuentra la cuenta o el contenedor: revisa IG_USER_ID.",
    100: "Meta dice que algún dato de la petición no vale (mira el detalle).",
}
SUBPISTAS = {
    2207042: "La cuenta ha llegado al tope de publicaciones por API en 24 h.",
    2207026: "Instagram no admite el formato del vídeo (MP4/MOV, H.264 o HEVC, AAC, 23–60 fps, índice al principio).",
    2207003: "Instagram tardó demasiado en descargar el vídeo de la dirección pública.",
    2207052: "Instagram no pudo descargar el vídeo de esa dirección: tiene que ser https, pública y sin redirecciones raras.",
    2207020: "El contenedor ha caducado (pasaron 24 h). Repite el comando.",
    2207027: "El vídeo todavía no está listo para publicarse. Repite el comando en un minuto.",
    2207050: "La cuenta de Instagram está restringida o inactiva: entra en la app y resuelve el aviso.",
    2207051: "Instagram ha bloqueado la acción por parecerle automatizada. No insistir hoy.",
}


def explicar(d, por_defecto="Instagram devolvió un error."):
    e = d.get("error") or {}
    msg = SUBPISTAS.get(e.get("error_subcode")) or PISTAS.get(e.get("code")) or por_defecto
    return msg, {"codigo": e.get("code"), "subcodigo": e.get("error_subcode"),
                 "detalle": (e.get("error_user_msg") or e.get("message") or "")[:300], "traza": e.get("fbtrace_id")}


class Instagram:
    def __init__(self, ruta_claves, metodo):
        self.ruta = ruta_claves
        self.k = base.leer_claves(ruta_claves)
        tiene_fb = bool(self.k.get("IG_FB_TOKEN") and self.k.get("IG_USER_ID"))
        tiene_ig = bool(self.k.get("IG_TOKEN"))
        if not (tiene_fb or tiene_ig):
            base.salir("Faltan en claves.txt las claves de Instagram: IG_USER_ID + IG_FB_TOKEN (subida directa) "
                       "o IG_TOKEN (con dirección pública). Ver publicar/README.md, «Instagram».")
        # con las dos, manda la de Facebook Login (es la que permite subir el archivo), salvo que se pida «url»
        self.fb = tiene_fb and not (metodo == "url" and tiene_ig)
        self.token = self.k["IG_FB_TOKEN"] if self.fb else self.k["IG_TOKEN"]
        ver = (self.k.get("IG_API_VERSION") or "").strip("/")
        self.raiz = (HOST_FB if self.fb else HOST_IG) + ("/" + ver if ver else "")
        self.id = self.k.get("IG_USER_ID") if self.fb else None
        self.usuario = None

    def get(self, ruta, **p):
        p["access_token"] = self.token
        r = base.pedir(f"{self.raiz}/{ruta}?" + urllib.parse.urlencode(p))
        return r.estado, r.json()

    def post(self, ruta, repetible=False, **p):
        p["access_token"] = self.token
        r = base.pedir(f"{self.raiz}/{ruta}", formulario=p, repetible=repetible, espera=180)
        return r.estado, r.json()

    def renovar_si_toca(self):
        """Solo con Instagram Login: el token dura 60 días y se alarga pidiéndolo (como hacen las estadísticas)."""
        if self.fb:
            return None
        ultima = float(self.k.get("IG_TOKEN_RENOVADO") or 0)
        if not ultima:
            base.guardar_claves(self.ruta, {"IG_TOKEN_RENOVADO": str(int(time.time()))})
            return None
        if time.time() - ultima < SEMANA:
            return None
        r = base.pedir(f"{HOST_IG}/refresh_access_token?" + urllib.parse.urlencode(
            {"grant_type": "ig_refresh_token", "access_token": self.token}))
        nuevo = r.json().get("access_token")
        if r.estado != 200 or not nuevo:
            return "Instagram: no se pudo alargar el token de 60 días (se sigue con el actual)."
        base.guardar_claves(self.ruta, {"IG_TOKEN": nuevo, "IG_TOKEN_RENOVADO": str(int(time.time()))})
        self.token = nuevo
        return None

    def cuenta(self):
        if self.fb:
            st, d = self.get(self.id, fields="username")
        else:
            st, d = self.get("me", fields="user_id,username")
            self.id = str(d.get("user_id") or self.k.get("IG_USER_ID") or "")
        if st != 200 or not d.get("username") or not self.id:
            msg, extra = explicar(d, "Instagram no reconoce la cuenta con estas claves.")
            base.salir(msg, estado=st, **extra)
        self.usuario = d["username"]
        return self.usuario

    def cupo(self):
        st, d = self.get(f"{self.id}/content_publishing_limit", fields="quota_usage,config")
        fila = (d.get("data") or [{}])[0] if st == 200 else {}
        return fila.get("quota_usage"), (fila.get("config") or {}).get("quota_total")

    def recientes(self, n=25):
        st, d = self.get(f"{self.id}/media", fields="id,caption,permalink,timestamp,media_product_type", limit=n)
        return (d.get("data") or []) if st == 200 else []

    def contenedor(self, cid):
        st, d = self.get(cid, fields="status_code,status")
        return d.get("status_code"), d.get("status"), d


def buscar_ya_publicado(ig, texto):
    clave = base.norma(texto)[:70]
    for m in ig.recientes():
        if clave and base.norma(m.get("caption"))[:70] == clave:
            return m
    return None


def revisar_texto(texto):
    problemas = []
    if len(texto) > 2200:
        problemas.append(f"el texto tiene {len(texto)} caracteres (máximo 2.200)")
    if len(re.findall(r"#\w+", texto)) > 30:
        problemas.append("más de 30 hashtags")
    if len(re.findall(r"(?<![\w.])@\w+", texto)) > 20:
        problemas.append("más de 20 menciones")
    return problemas


def subir_archivo(uri, token, ruta, tam):
    host = urllib.parse.urlparse(uri).hostname or ""
    if not ((uri.startswith("https://") and host == HOST_SUBIDA) or base.PRUEBAS):
        base.salir("Meta ha devuelto una dirección de subida que no es suya: no subo nada", host=host)
    with open(ruta, "rb") as f:
        datos = f.read()
    r = base.pedir(uri, metodo="POST", datos=datos, espera=900, intentos=3,
                   cabeceras={"Authorization": "OAuth " + token, "offset": "0", "file_size": str(tam),
                              "Content-Type": "application/octet-stream"})
    d = r.json()
    if r.estado != 200 or not d.get("success"):
        info = d.get("debug_info") or {}
        base.salir("La subida del vídeo a Instagram falló" + (" (se puede reintentar)" if info.get("retriable") else ""),
                   estado=r.estado, detalle=(info.get("message") or r.texto(300)), tipo=info.get("type"))


def main():
    ap = argparse.ArgumentParser(description="Publica un Reel en Instagram por la API oficial.")
    ap.add_argument("--claves", required=True)
    ap.add_argument("--metadatos", required=True)
    ap.add_argument("--clave", required=True, help="número del vídeo en metadatos.json, p. ej. 01")
    ap.add_argument("--video", required=True)
    ap.add_argument("--video-url", dest="video_url", help="dirección https pública del mismo MP4 (solo con IG_TOKEN)")
    ap.add_argument("--portada-url", dest="portada_url", help="JPEG público para la portada (si no, fotograma portada.t)")
    ap.add_argument("--metodo", choices=("auto", "directa", "url"), default="auto")
    ap.add_argument("--comentario", action="store_true")
    ap.add_argument("--registro", help="por defecto, publicado.json junto a metadatos.json")
    ap.add_argument("--prueba", action="store_true")
    ap.add_argument("--forzar", action="store_true")
    ap.add_argument("--espera", type=int, default=600, help="segundos máximos esperando a que Instagram procese el vídeo")
    a = ap.parse_args()

    m = base.cargar_metadatos(a.metadatos, a.clave, "instagram")
    texto = m["instagram"]["texto"].strip()
    problemas = revisar_texto(texto)
    if problemas:
        base.salir("Instagram no aceptará el texto: " + "; ".join(problemas))
    tam, avisos = base.revisar_mp4(a.video, MAXIMO)
    for u, nombre in ((a.video_url, "--video-url"), (a.portada_url, "--portada-url")):
        if u and not (u.startswith("https://") and u.isascii()):
            base.salir(f"{nombre} tiene que ser una dirección https con caracteres normales (sin tildes ni espacios)")

    ig = Instagram(a.claves, a.metodo)
    directa = a.metodo == "directa" or (a.metodo == "auto" and ig.fb)
    if a.metodo == "directa" and not ig.fb:
        avisos.append("Subida directa con token de Instagram Login: Meta solo la documenta para Facebook Login; puede fallar.")
    if not directa and not a.video_url:
        base.salir("Con IG_TOKEN (Instagram Login) Meta necesita descargarse el vídeo de una dirección pública: "
                   "pasa --video-url https://…mp4, o configura la subida directa (IG_USER_ID + IG_FB_TOKEN). "
                   "Ver publicar/README.md, «Instagram».")
    aviso = ig.renovar_si_toca()
    if aviso:
        avisos.append(aviso)
    usuario = ig.cuenta()
    usados, total = ig.cupo()
    if usados is not None and total and usados >= total and not a.prueba:
        base.salir(SUBPISTAS[2207042], usados=usados, total=total)

    reg_ruta = base.ruta_registro(a)
    previo = base.leer_registro(reg_ruta).get(a.clave, {}).get("instagram", {})

    # -- no duplicar -------------------------------------------------------
    if not a.forzar:
        if previo.get("estado") == "publicado" and previo.get("id"):
            if a.prueba:
                base.listo(red="instagram", prueba=True, clave=a.clave, cuenta=usuario, yaPublicado=True, url=previo.get("url"))
            else:
                base.listo(red="instagram", clave=a.clave, yaEstaba=True, id=previo["id"], url=previo.get("url"))
            return
        ya = buscar_ya_publicado(ig, texto)
        if ya:
            if not a.prueba:
                base.apuntar(reg_ruta, a.clave, "instagram", estado="publicado", id=ya["id"], url=ya.get("permalink"), cuenta=usuario)
            base.listo(red="instagram", clave=a.clave, yaEstaba=True, id=ya["id"], url=ya.get("permalink"),
                       **({"prueba": True} if a.prueba else {}))
            return

    if a.prueba:
        base.listo(red="instagram", prueba=True, clave=a.clave, cuenta=usuario, bytes=tam,
                   metodo="directa" if directa else "url", login="facebook" if ig.fb else "instagram",
                   cupo=f"{usados}/{total}" if usados is not None else None, caracteresTexto=len(texto), avisos=avisos)
        return

    # -- contenedor (retoma el que hubiera a medias) -------------------------
    cid, codigo = None, None
    if previo.get("contenedor") and not a.forzar:
        codigo, _, _ = ig.contenedor(previo["contenedor"])
        if codigo in ("FINISHED", "PUBLISHED") or (codigo == "IN_PROGRESS" and previo.get("estado") == "subido"):
            cid = previo["contenedor"]
    if not cid:
        campos = {"media_type": "REELS", "caption": texto, "share_to_feed": "true"}
        if a.portada_url:
            campos["cover_url"] = a.portada_url
        else:
            t = (m.get("portada") or {}).get("t")
            if isinstance(t, (int, float)) and t >= 0:
                campos["thumb_offset"] = str(int(round(t * 1000)))
        if directa:
            campos["upload_type"] = "resumable"
        else:
            campos["video_url"] = a.video_url
        st, d = ig.post(f"{ig.id}/media", **campos)
        cid = d.get("id")
        if st != 200 or not cid:
            msg, extra = explicar(d, "Instagram no aceptó crear el Reel.")
            base.salir(msg, estado=st, **extra)
        base.apuntar(reg_ruta, a.clave, "instagram", contenedor=cid, estado="creado", cuenta=usuario,
                     archivo=os.path.basename(a.video), bytes=tam, enviado=base.ahora())
        if directa:
            uri = d.get("uri")
            if not uri:
                base.salir("Instagram no ha dado dirección de subida directa: esta app o este token no la admiten. "
                           "Usa --video-url con una dirección pública o configura Facebook Login (publicar/README.md).",
                           contenedor=cid)
            subir_archivo(uri, ig.token, a.video, tam)
        base.apuntar(reg_ruta, a.clave, "instagram", estado="subido")
        codigo = None

    # -- esperar a que Instagram lo procese ----------------------------------
    limite = time.time() + a.espera
    while codigo not in ("FINISHED", "PUBLISHED", "ERROR", "EXPIRED"):
        codigo, estado_txt, d = ig.contenedor(cid)
        if codigo in ("FINISHED", "PUBLISHED", "ERROR", "EXPIRED"):
            break
        if d.get("error"):
            msg, extra = explicar(d, "Instagram no deja consultar el vídeo que se está procesando.")
            base.salir(msg + " El envío queda apuntado: repetir el comando lo retoma.", contenedor=cid, **extra)
        if time.time() >= limite:
            base.listo(red="instagram", clave=a.clave, estado="procesando", contenedor=cid, avisos=avisos,
                       siguiente="Instagram sigue procesando el vídeo. Repite el mismo comando en un par de minutos: "
                                 "retoma este envío, no sube otro.")
            return
        base.dormir(10)
    if codigo in ("ERROR", "EXPIRED"):
        _, estado_txt, d = ig.contenedor(cid)
        base.apuntar(reg_ruta, a.clave, "instagram", estado="fallido", motivo=estado_txt or codigo)
        sub = re.search(r"\b(2207\d{3})\b", estado_txt or "")
        base.salir(SUBPISTAS.get(int(sub.group(1))) if sub and int(sub.group(1)) in SUBPISTAS
                   else "Instagram no pudo procesar el vídeo.", contenedor=cid, detalle=(estado_txt or codigo)[:300])

    # -- publicar (una sola vez: si la respuesta se pierde, se mira antes de repetir) --
    media_id = None
    if codigo != "PUBLISHED":
        try:
            st, d = ig.post(f"{ig.id}/media_publish", creation_id=cid)
        except OSError as e:
            st, d = 0, {"error": {"message": str(e)}}
        media_id = d.get("id")
        if not media_id:
            codigo, _, _ = ig.contenedor(cid)
            if codigo != "PUBLISHED":
                msg, extra = explicar(d, "Instagram no publicó el Reel.")
                base.salir(msg + " El vídeo ya está subido: repetir el comando solo reintenta publicar.",
                           estado=st, contenedor=cid, **extra)
    url = None
    if media_id:
        _, d = ig.get(media_id, fields="permalink,shortcode")
        url = d.get("permalink")
    else:   # se publicó pero no llegó el identificador: se busca por el texto
        ya = buscar_ya_publicado(ig, texto) or {}
        media_id, url = ya.get("id"), ya.get("permalink")
    base.apuntar(reg_ruta, a.clave, "instagram", estado="publicado", id=media_id, url=url)

    comentario = None
    if a.comentario and (m.get("comentario") or "").strip() and media_id:
        if previo.get("comentario_id"):
            comentario = "ya estaba"
        else:
            st, d = ig.post(f"{media_id}/comments", message=m["comentario"].strip())
            if d.get("id"):
                base.apuntar(reg_ruta, a.clave, "instagram", comentario_id=d["id"])
                comentario = "puesto (sin fijar: la API no deja fijar)"
            else:
                comentario = "no: " + explicar(d)[1]["detalle"][:150]
    base.listo(red="instagram", clave=a.clave, id=media_id, url=url, cuenta=usuario, comentario=comentario, avisos=avisos)


if __name__ == "__main__":
    try:
        main()
    except OSError as e:   # sin red, dominio no permitido, etc.
        base.salir(str(e)[:300], red="instagram")
