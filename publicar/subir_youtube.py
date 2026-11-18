#!/usr/bin/env python3
"""Sube un vídeo del lote a YouTube por la API oficial (sin navegador).

Lo usa el agente del turno SOLO después de que una persona escriba «ok» en el chat del lote.
Necesita en claves.txt (carpeta local del turno, nunca en el repo):
  YT_CLIENT_ID=...
  YT_CLIENT_SECRET=...
  YT_UPLOAD_REFRESH_TOKEN=...   (se saca una vez con: python3 estadisticas/autorizar.py --subir CLIENT_ID CLIENT_SECRET)

Uso:
  python3 publicar/subir_youtube.py --claves "<carpeta>/claves.txt" --metadatos lotes/<lote>/metadatos.json \
      --clave 01 --video "<carpeta>/lotes/<lote>/01-....mp4" [--publicar-en 2026-11-17T10:00:00+01:00] [--prueba]

--publicar-en  sube el vídeo en privado y YouTube lo hace público a esa hora (separar las subidas del lote).
--prueba       comprueba claves, metadatos y archivo sin subir nada.
Imprime una línea JSON con el resultado: {"ok": true, "id": ..., "url": ..., "publicaEn": ...}.
"""
import argparse, json, os, re, ssl, sys, urllib.error, urllib.parse, urllib.request

CTX = ssl.create_default_context(cafile="/etc/ssl/cert.pem") if os.path.exists("/etc/ssl/cert.pem") else ssl.create_default_context()
API = "https://www.googleapis.com/youtube/v3"


def claves(ruta):
    d = {}
    for linea in open(ruta, encoding="utf-8"):
        if "=" in linea and not linea.lstrip().startswith("#"):
            k, v = linea.split("=", 1)
            d[k.strip()] = v.strip()
    return d


def peticion(url, datos=None, cabeceras=None, metodo=None):
    req = urllib.request.Request(url, data=datos, headers=cabeceras or {}, method=metodo)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=600) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def norma(t):
    """Compara títulos sin hashtags, emojis, mayúsculas ni signos (para no duplicar)."""
    return re.sub(r"[^\w]+", "", re.sub(r"#\w+", "", t or "").lower())


def salir(msg, **extra):
    print(json.dumps({"ok": False, "error": msg, **extra}, ensure_ascii=False))
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claves", required=True)
    ap.add_argument("--metadatos")
    ap.add_argument("--clave", help="número del vídeo en metadatos.json, p. ej. 01")
    ap.add_argument("--video")
    ap.add_argument("--publicar-en", dest="publicar_en")
    ap.add_argument("--prueba", action="store_true")
    ap.add_argument("--portada", help="JPEG de la portada elegida (motor.portadas → portada.jpg). Si YouTube no deja ponerla, sigue sin ella")
    ap.add_argument("--solo-portada", dest="solo_portada", help="id de un vídeo ya subido: solo pone la portada")
    a = ap.parse_args()

    if a.solo_portada and not a.portada:
        salir("--solo-portada necesita --portada")
    k = claves(a.claves)
    falta = [n for n in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_UPLOAD_REFRESH_TOKEN") if not k.get(n)]
    if falta:
        salir("Faltan en claves.txt: " + ", ".join(falta) + " (ver publicar/README.md)")
    if a.solo_portada:
        auth = _token(k)
        print(json.dumps({"ok": True, "id": a.solo_portada, "portada": poner_portada(auth, a.solo_portada, a.portada)}, ensure_ascii=False))
        return
    if not (a.metadatos and a.clave and a.video):
        salir("Faltan --metadatos, --clave y --video")
    m = json.load(open(a.metadatos, encoding="utf-8")).get(a.clave)
    if not m or "youtube" not in m:
        salir(f"metadatos.json no tiene el vídeo {a.clave} con su bloque «youtube»")
    if not os.path.isfile(a.video):
        salir("No encuentro el vídeo: " + a.video)
    yt = m["youtube"]
    titulo = yt["titulo"][:100]

    # 1. token de acceso
    auth = _token(k)

    # 2. no duplicar: busca el mismo título entre las últimas subidas del canal
    st, _, cuerpo = peticion(f"{API}/channels?part=contentDetails&mine=true", cabeceras=auth)
    if st == 200 and json.loads(cuerpo).get("items"):
        subidas = json.loads(cuerpo)["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        st, _, cuerpo = peticion(f"{API}/playlistItems?part=snippet&maxResults=50&playlistId={subidas}", cabeceras=auth)
        for it in json.loads(cuerpo).get("items", []) if st == 200 else []:
            if norma(it["snippet"]["title"]) == norma(titulo):
                vid = it["snippet"]["resourceId"]["videoId"]
                print(json.dumps({"ok": True, "yaEstaba": True, "id": vid, "url": f"https://youtube.com/shorts/{vid}"}, ensure_ascii=False))
                return
    if a.prueba:
        print(json.dumps({"ok": True, "prueba": True, "titulo": titulo, "bytes": os.path.getsize(a.video), "publicaEn": a.publicar_en}, ensure_ascii=False))
        return

    # 3. subida reanudable
    estado = {"privacyStatus": "public", "selfDeclaredMadeForKids": bool(yt.get("para_ninos", False))}
    if a.publicar_en:
        estado.update({"privacyStatus": "private", "publishAt": a.publicar_en})
    meta = {"snippet": {"title": titulo, "description": yt.get("descripcion", "")[:5000], "categoryId": "27",
                        "defaultLanguage": "es", "defaultAudioLanguage": "es"}, "status": estado}
    if yt.get("tags"):  # etiquetas ocultas de YouTube (máx. 500 caracteres en total)
        meta["snippet"]["tags"] = list(yt["tags"])
    tam = os.path.getsize(a.video)
    st, cab, cuerpo = peticion(f"https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                               json.dumps(meta).encode(), {**auth, "Content-Type": "application/json; charset=UTF-8",
                                                           "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(tam)})
    destino = cab.get("Location") or cab.get("location")
    if st != 200 or not destino:
        salir("YouTube no aceptó empezar la subida", estado=st, detalle=cuerpo.decode()[:400])
    with open(a.video, "rb") as f:
        st, _, cuerpo = peticion(destino, f.read(), {**auth, "Content-Type": "video/mp4"}, "PUT")
    if st not in (200, 201):
        salir("La subida falló", estado=st, detalle=cuerpo.decode()[:400])
    v = json.loads(cuerpo)
    portada = poner_portada(auth, v["id"], a.portada) if a.portada else None
    print(json.dumps({"ok": True, "id": v["id"], "url": f"https://youtube.com/shorts/{v['id']}",
                      "estado": v.get("status", {}).get("privacyStatus"), "publicaEn": a.publicar_en,
                      "portada": portada}, ensure_ascii=False))


def _token(k):
    st, _, cuerpo = peticion("https://oauth2.googleapis.com/token", urllib.parse.urlencode({
        "client_id": k["YT_CLIENT_ID"], "client_secret": k["YT_CLIENT_SECRET"],
        "refresh_token": k["YT_UPLOAD_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode())
    if st != 200:
        salir("Google rechaza el token de subida (repite la autorización con --subir)", detalle=cuerpo.decode()[:300])
    return {"Authorization": "Bearer " + json.loads(cuerpo)["access_token"]}


def poner_portada(auth, vid, ruta, intentos=4, espera=30):
    """thumbnails.set. En Shorts YouTube solo lo acepta en canales con miniaturas personalizadas
    (verificados / Programa de Socios) y cuando el vídeo ya está procesado: reintenta y, si no, lo dice."""
    import time
    if not os.path.isfile(ruta):
        return "no: no encuentro " + ruta
    datos = open(ruta, "rb").read()
    if len(datos) > 2 * 1024 * 1024:
        return "no: la portada pesa más de 2 MB"
    ultimo = ""
    for i in range(intentos):
        st, _, cuerpo = peticion(f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
                                 datos, {**auth, "Content-Type": "image/jpeg"}, "POST")
        if st == 200:
            return "puesta"
        ultimo = f"{st} {cuerpo.decode(errors='replace')[:200]}"
        if st == 403:      # el canal no puede poner miniaturas personalizadas: no tiene sentido reintentar
            break
        time.sleep(espera)
    return "no: " + ultimo


if __name__ == "__main__":
    main()
