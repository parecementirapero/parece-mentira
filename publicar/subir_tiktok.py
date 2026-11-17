#!/usr/bin/env python3
"""Manda un vídeo del lote a TikTok por la API oficial (Content Posting API, modo «Upload»).

Qué hace: deja el vídeo como BORRADOR en la bandeja de entrada de la cuenta del canal. Para que salga
publicado, una persona abre TikTok en el móvil → Bandeja de entrada → notificación del vídeo → pega el
texto → Publicar. TikTok no deja publicar del todo por API a apps sin auditar (y no audita herramientas
de uso interno), así que este es el máximo automático posible. Ver publicar/README.md.

Lo usa el agente del turno SOLO después de que una persona escriba «ok» en el chat del lote.
Necesita en claves.txt (carpeta local del turno, nunca en el repo):
  TIKTOK_PUB_CLIENT_KEY=...
  TIKTOK_PUB_CLIENT_SECRET=...
  TIKTOK_PUB_REFRESH_TOKEN=...      (se saca una vez con: python3 publicar/autorizar_tiktok.py --claves claves.txt)
El token de TikTok cambia en cada renovación: el script guarda el nuevo en claves.txt él solo.

Uso:
  python3 publicar/subir_tiktok.py --claves claves.txt --metadatos lotes/<lote>/metadatos.json \
      --clave 01 --video "<carpeta>/lotes/<lote>/01-....mp4" [--prueba] [--estado] [--forzar]

--prueba   comprueba claves, permiso, metadatos y archivo sin subir nada.
--estado   no sube: pregunta a TikTok cómo va el envío ya hecho (si la persona ya lo publicó, da el enlace).
--forzar   vuelve a enviarlo aunque el registro diga que ya se envió.
Imprime una línea JSON: {"ok": true, "red": "tiktok", "estado": "en_bandeja", "texto": "...", ...}.
"""
import argparse
import os
import re
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base  # noqa: E402

API = os.environ.get("PM_TIKTOK_API", "https://open.tiktokapis.com").rstrip("/")
MB = 1024 * 1024
TROZO = 32 * MB            # entre 5 y 64 MB (guía de transferencia de TikTok)
UN_SOLO_TROZO = 64 * MB    # hasta aquí, el archivo entero en una petición
MAXIMO = 4 * 1024 * MB     # 4 GB
NECESARIAS = ("TIKTOK_PUB_CLIENT_KEY", "TIKTOK_PUB_CLIENT_SECRET", "TIKTOK_PUB_REFRESH_TOKEN")

ERRORES = {
    "spam_risk_too_many_pending_share": "TikTok no admite más borradores: hay 5 vídeos enviados por API en las últimas 24 h "
                                        "que aún no se han publicado. Publica o descarta los de la bandeja de entrada y repite.",
    "spam_risk_user_banned_from_posting": "TikTok tiene la cuenta bloqueada para publicar. No reintentar: mirar la cuenta en el móvil.",
    "scope_not_authorized": "El permiso no incluye «video.upload». Repite publicar/autorizar_tiktok.py y marca todos los permisos; "
                            "comprueba que el sandbox tiene el producto Content Posting API.",
    "access_token_invalid": "TikTok rechaza el token de acceso.",
    "rate_limit_exceeded": "Demasiadas peticiones seguidas a TikTok (máx. 6 por minuto). Espera un minuto y repite.",
    "invalid_param": "TikTok dice que la petición está mal formada.",
}
FALLOS = {
    "file_format_check_failed": "TikTok no admite el formato del vídeo (MP4 con H.264 es lo seguro).",
    "duration_check_failed": "La duración del vídeo no entra en los límites de TikTok.",
    "frame_rate_check_failed": "TikTok no admite los fotogramas por segundo del vídeo (23–60).",
    "picture_size_check_failed": "TikTok no admite el tamaño de imagen del vídeo (360–4096 px por lado).",
    "internal": "Fallo interno de TikTok: se puede reintentar.",
    "auth_removed": "Se retiró el permiso de la app mientras se procesaba: repetir publicar/autorizar_tiktok.py.",
    "spam_risk_too_many_posts": "La cuenta ha llegado al tope diario de publicaciones por API: publicar desde el móvil.",
    "spam_risk_user_banned_from_posting": "TikTok tiene la cuenta bloqueada para publicar.",
    "spam_risk": "TikTok ha marcado el envío como sospechoso. No reintentar.",
}


def plan_trozos(tam):
    """(tamaño de trozo, número de trozos) según las reglas de TikTok: total = suelo(tam / trozo) y el
    último trozo se lleva lo que sobra (puede pasar del tamaño declarado, hasta 128 MB)."""
    if tam <= UN_SOLO_TROZO:
        return tam, 1
    return TROZO, tam // TROZO


def rangos(tam, trozo, total):
    for i in range(total):
        ini = i * trozo
        fin = tam - 1 if i == total - 1 else ini + trozo - 1
        yield ini, fin


class TikTok:
    def __init__(self, ruta_claves):
        self.ruta = ruta_claves
        self.k = base.leer_claves(ruta_claves)
        falta = [n for n in NECESARIAS if not self.k.get(n)]
        if falta:
            base.salir("Faltan en claves.txt: " + ", ".join(falta) + " (ver publicar/README.md, «TikTok»)")
        self.acceso = None
        self.permisos = ""

    # -- token -------------------------------------------------------------
    def token(self, renovar=False):
        """Token de acceso. Reutiliza el guardado si le quedan más de 5 minutos; si no, lo renueva y
        guarda EN EL ACTO el refresh token nuevo (TikTok invalida el anterior)."""
        caduca = float(self.k.get("TIKTOK_PUB_ACCESS_CADUCA") or 0)
        if not renovar and self.k.get("TIKTOK_PUB_ACCESS_TOKEN") and caduca - time.time() > 300:
            self.acceso = self.k["TIKTOK_PUB_ACCESS_TOKEN"]
            self.permisos = self.k.get("TIKTOK_PUB_PERMISOS", "")
            return self.acceso
        r = base.pedir(f"{API}/v2/oauth/token/", formulario={
            "client_key": self.k["TIKTOK_PUB_CLIENT_KEY"], "client_secret": self.k["TIKTOK_PUB_CLIENT_SECRET"],
            "grant_type": "refresh_token", "refresh_token": self.k["TIKTOK_PUB_REFRESH_TOKEN"]})
        d = r.json()
        if r.estado != 200 or not d.get("access_token"):
            base.salir("TikTok no renueva el permiso (caducado, retirado o usado en otro ordenador). "
                       "Repite: python3 publicar/autorizar_tiktok.py --claves claves.txt",
                       detalle=f"{d.get('error', r.estado)}: {d.get('error_description', '')}"[:300])
        cambios = {"TIKTOK_PUB_ACCESS_TOKEN": d["access_token"],
                   "TIKTOK_PUB_ACCESS_CADUCA": str(int(time.time() + int(d.get("expires_in", 3600)))),
                   "TIKTOK_PUB_PERMISOS": d.get("scope", "")}
        if d.get("refresh_token"):
            cambios["TIKTOK_PUB_REFRESH_TOKEN"] = d["refresh_token"]
        if d.get("refresh_expires_in"):
            cambios["TIKTOK_PUB_REFRESH_CADUCA"] = str(int(time.time() + int(d["refresh_expires_in"])))
        try:
            base.guardar_claves(self.ruta, cambios)
        except OSError as e:
            base.salir("TikTok ha dado un token nuevo y NO se ha podido guardar en claves.txt. El anterior ya no vale: "
                       "arregla los permisos del archivo y repite publicar/autorizar_tiktok.py.", detalle=str(e)[:200])
        self.k.update(cambios)
        self.acceso, self.permisos = d["access_token"], d.get("scope", "")
        return self.acceso

    def dias_permiso(self):
        c = float(self.k.get("TIKTOK_PUB_REFRESH_CADUCA") or 0)
        return int((c - time.time()) // 86400) if c else None

    # -- llamadas ----------------------------------------------------------
    def api(self, ruta, cuerpo, repetible=True):
        """POST JSON con el token. Si TikTok dice que el token no vale, lo renueva una vez y repite."""
        for vuelta in (0, 1):
            r = base.pedir(f"{API}{ruta}", cuerpo_json=cuerpo, repetible=repetible,
                           cabeceras={"Authorization": "Bearer " + (self.acceso or self.token())})
            d = r.json()
            codigo = (d.get("error") or {}).get("code") or ("ok" if r.estado == 200 else f"http_{r.estado}")
            if codigo == "access_token_invalid" and vuelta == 0:
                self.token(renovar=True)
                continue
            return r.estado, codigo, d
        return r.estado, codigo, d

    def cuenta(self):
        r = base.pedir(f"{API}/v2/user/info/?fields=open_id,display_name",
                       cabeceras={"Authorization": "Bearer " + (self.acceso or self.token())})
        return (r.json().get("data") or {}).get("user", {}).get("display_name")

    def estado(self, publish_id):
        st, codigo, d = self.api("/v2/post/publish/status/fetch/", {"publish_id": publish_id})
        if codigo != "ok":
            return None, codigo, {}
        datos = d.get("data") or {}
        return datos.get("status"), codigo, datos


def explicar(codigo, d):
    msg = ERRORES.get(codigo, f"TikTok devolvió el error «{codigo}».")
    return msg, {"codigo": codigo, "detalle": ((d.get("error") or {}).get("message") or "")[:300],
                 "log_id": (d.get("error") or {}).get("log_id")}


def subir_archivo(url, ruta, tam, trozo, total):
    """PUT de cada trozo, en orden. 206 = sigue, 201 = completo. Reintenta el mismo trozo ante 5xx."""
    host = urllib.parse.urlparse(url).hostname or ""
    if not (url.startswith("https://") and host.endswith(".tiktokapis.com")) and not base.PRUEBAS:
        base.salir("TikTok ha devuelto una dirección de subida que no es suya: no subo nada",
                   host=host)
    with open(ruta, "rb") as f:
        for n, (ini, fin) in enumerate(rangos(tam, trozo, total), 1):
            f.seek(ini)
            datos = f.read(fin - ini + 1)
            cab = {"Content-Type": "video/mp4", "Content-Length": str(len(datos)),
                   "Content-Range": f"bytes {ini}-{fin}/{tam}"}
            r = base.pedir(url, metodo="PUT", datos=datos, cabeceras=cab, espera=900, intentos=4)
            esperado = 201 if n == total else 206
            if r.estado == 416 and _ya_recibido(r) > fin:
                continue   # el trozo llegó en un intento anterior cuya respuesta se perdió: no se repite
            if r.estado not in (esperado, 201):
                pista = {400: "cabeceras o tamaño del trozo incorrectos", 403: "la dirección de subida ha caducado (dura 1 h)",
                         404: "TikTok no reconoce esta subida", 416: "el trozo no coincide con lo ya subido"}.get(r.estado, "")
                base.salir(f"La subida a TikTok falló en el trozo {n} de {total}" + (f": {pista}" if pista else ""),
                           estado=r.estado, detalle=r.texto(300))


def _ya_recibido(r):
    """Bytes que TikTok dice tener ya (cabecera «Content-Range: bytes 0-N/TOTAL» de su respuesta)."""
    m = re.match(r"bytes \d+-(\d+)/", r.cabeceras.get("content-range", ""))
    return int(m.group(1)) + 1 if m else 0


def enlace_publicado(datos, cuenta):
    ids = datos.get("publicaly_available_post_id") or []
    # sin el usuario también funciona: TikTok redirige por el número del vídeo
    return f"https://www.tiktok.com/@{cuenta or ''}/video/{ids[0]}" if ids else None


def main():
    ap = argparse.ArgumentParser(description="Envía un vídeo a TikTok como borrador en la bandeja de entrada (API oficial).")
    ap.add_argument("--claves", required=True)
    ap.add_argument("--metadatos", required=True)
    ap.add_argument("--clave", required=True, help="número del vídeo en metadatos.json, p. ej. 01")
    ap.add_argument("--video")
    ap.add_argument("--registro", help="por defecto, publicado.json junto a metadatos.json")
    ap.add_argument("--prueba", action="store_true")
    ap.add_argument("--estado", action="store_true")
    ap.add_argument("--forzar", action="store_true")
    ap.add_argument("--espera", type=int, default=180, help="segundos máximos esperando a que TikTok procese el vídeo")
    a = ap.parse_args()

    m = base.cargar_metadatos(a.metadatos, a.clave, "tiktok")
    texto = m["tiktok"]["texto"].strip()
    reg_ruta = base.ruta_registro(a)
    previo = base.leer_registro(reg_ruta).get(a.clave, {}).get("tiktok", {})
    tt = TikTok(a.claves)
    usuario = tt.k.get("TIKTOK_PUB_USUARIO")   # el @ de la cuenta (sin @), solo para montar el enlace

    # -- solo consultar ----------------------------------------------------
    if a.estado:
        if not previo.get("publish_id"):
            base.salir(f"El registro no tiene ningún envío a TikTok del vídeo {a.clave}", registro=reg_ruta)
        est, codigo, datos = tt.estado(previo["publish_id"])
        if codigo != "ok":
            msg, extra = explicar(codigo, {})
            base.salir(msg, **extra)
        nuevo = {"PUBLISH_COMPLETE": "publicado", "SEND_TO_USER_INBOX": "en_bandeja", "FAILED": "fallido"}.get(est, "procesando")
        url = enlace_publicado(datos, usuario)
        base.apuntar(reg_ruta, a.clave, "tiktok", estado=nuevo, **({"url": url} if url else {}))
        base.listo(red="tiktok", clave=a.clave, estado=nuevo, estadoTikTok=est, url=url,
                   motivo=FALLOS.get(datos.get("fail_reason"), datos.get("fail_reason")))
        return

    if not a.video:
        base.salir("Falta --video")
    tam, avisos = base.revisar_mp4(a.video, MAXIMO)
    trozo, total = plan_trozos(tam)

    # -- no duplicar -------------------------------------------------------
    if previo.get("publish_id") and not a.forzar and not a.prueba:
        est, codigo, datos = tt.estado(previo["publish_id"])
        if est in ("SEND_TO_USER_INBOX", "PUBLISH_COMPLETE"):
            nuevo = "publicado" if est == "PUBLISH_COMPLETE" else "en_bandeja"
            url = enlace_publicado(datos, usuario)
            base.apuntar(reg_ruta, a.clave, "tiktok", estado=nuevo, **({"url": url} if url else {}))
            base.listo(red="tiktok", clave=a.clave, yaEstaba=True, estado=nuevo, url=url, texto=texto,
                       publish_id=previo["publish_id"])
            return
        entero = previo.get("estado") == "subido" or (previo.get("bytes") and datos.get("uploaded_bytes") == previo.get("bytes"))
        if est == "PROCESSING_UPLOAD" and entero:
            previo = dict(previo, estado="subido")  # llegó entero y TikTok sigue procesando: abajo solo se espera, sin volver a subir
        elif est is None and codigo not in ("invalid_publish_id",):
            msg, extra = explicar(codigo, {})
            base.salir("No puedo comprobar el envío anterior a TikTok, así que no lo repito (para no duplicar). " + msg,
                       publish_id=previo["publish_id"], **extra)
        else:
            previo = {}  # falló, se quedó a medias o TikTok ya no lo conoce: se empieza de nuevo

    # -- prueba ------------------------------------------------------------
    tt.token()
    if "video.upload" not in tt.permisos.split(","):
        msg, extra = explicar("scope_not_authorized", {})
        base.salir(msg, permisos=tt.permisos, **{k: v for k, v in extra.items() if k == "codigo"})
    nombre = tt.cuenta()
    dias = tt.dias_permiso()
    if dias is not None and dias < 20:
        avisos.append(f"El permiso de TikTok caduca en {dias} días: repite publicar/autorizar_tiktok.py.")
    if a.prueba:
        base.listo(red="tiktok", prueba=True, clave=a.clave, cuenta=nombre, bytes=tam, trozos=total,
                   caracteresTexto=len(texto), permisoCaducaDias=dias, avisos=avisos,
                   yaEnviado=bool(previo.get("publish_id")))
        return

    # -- envío -------------------------------------------------------------
    if previo.get("publish_id") and previo.get("estado") == "subido":
        publish_id = previo["publish_id"]
    else:
        st, codigo, d = tt.api("/v2/post/publish/inbox/video/init/", repetible=False, cuerpo={
            "source_info": {"source": "FILE_UPLOAD", "video_size": tam, "chunk_size": trozo, "total_chunk_count": total}})
        datos = d.get("data") or {}
        if codigo != "ok" or not datos.get("publish_id") or not datos.get("upload_url"):
            msg, extra = explicar(codigo, d)
            base.salir(msg, estado=st, **extra)
        publish_id = datos["publish_id"]
        base.apuntar(reg_ruta, a.clave, "tiktok", publish_id=publish_id, estado="subiendo", archivo=os.path.basename(a.video),
                     bytes=tam, cuenta=nombre, enviado=base.ahora())
        subir_archivo(datos["upload_url"], a.video, tam, trozo, total)
        base.apuntar(reg_ruta, a.clave, "tiktok", estado="subido")

    # -- esperar a que llegue a la bandeja -----------------------------------
    limite, est, datos = time.time() + a.espera, None, {}
    while True:
        est, codigo, datos = tt.estado(publish_id)
        if est in ("SEND_TO_USER_INBOX", "PUBLISH_COMPLETE", "FAILED") or time.time() >= limite:
            break
        base.dormir(5)
    if est == "FAILED":
        motivo = datos.get("fail_reason")
        base.apuntar(reg_ruta, a.clave, "tiktok", estado="fallido", motivo=motivo)
        base.salir(FALLOS.get(motivo, f"TikTok rechazó el vídeo ({motivo})."), publish_id=publish_id, motivo=motivo)
    if est not in ("SEND_TO_USER_INBOX", "PUBLISH_COMPLETE"):
        base.listo(red="tiktok", clave=a.clave, estado="procesando", publish_id=publish_id, texto=texto, avisos=avisos,
                   siguiente="TikTok aún lo está procesando. Repite con --estado en un minuto; no hace falta volver a subirlo.")
        return
    nuevo = "publicado" if est == "PUBLISH_COMPLETE" else "en_bandeja"
    base.apuntar(reg_ruta, a.clave, "tiktok", estado=nuevo)
    base.listo(red="tiktok", clave=a.clave, estado=nuevo, publish_id=publish_id, cuenta=nombre, texto=texto, avisos=avisos,
               siguiente="En el móvil: TikTok → Bandeja de entrada → notificación del vídeo → pegar el texto → Publicar. "
                         "Después, este mismo comando con --estado da el enlace.")


if __name__ == "__main__":
    try:
        main()
    except OSError as e:   # sin red, dominio no permitido, etc.
        base.salir(str(e)[:300], red="tiktok")
