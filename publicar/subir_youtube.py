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
import argparse, json, os, ssl, sys, urllib.error, urllib.parse, urllib.request

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


def salir(msg, **extra):
    print(json.dumps({"ok": False, "error": msg, **extra}, ensure_ascii=False))
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claves", required=True)
    ap.add_argument("--metadatos", required=True)
    ap.add_argument("--clave", required=True, help="número del vídeo en metadatos.json, p. ej. 01")
    ap.add_argument("--video", required=True)
    ap.add_argument("--publicar-en", dest="publicar_en")
    ap.add_argument("--prueba", action="store_true")
    a = ap.parse_args()

    k = claves(a.claves)
    falta = [n for n in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_UPLOAD_REFRESH_TOKEN") if not k.get(n)]
    if falta:
        salir("Faltan en claves.txt: " + ", ".join(falta) + " (ver publicar/README.md)")
    m = json.load(open(a.metadatos, encoding="utf-8")).get(a.clave)
    if not m or "youtube" not in m:
        salir(f"metadatos.json no tiene el vídeo {a.clave} con su bloque «youtube»")
    if not os.path.isfile(a.video):
        salir("No encuentro el vídeo: " + a.video)
    yt = m["youtube"]
    titulo = yt["titulo"][:100]

    # 1. token de acceso
    st, _, cuerpo = peticion("https://oauth2.googleapis.com/token", urllib.parse.urlencode({
        "client_id": k["YT_CLIENT_ID"], "client_secret": k["YT_CLIENT_SECRET"],
        "refresh_token": k["YT_UPLOAD_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode())
    if st != 200:
        salir("Google rechaza el token de subida (repite la autorización con --subir)", detalle=cuerpo.decode()[:300])
    auth = {"Authorization": "Bearer " + json.loads(cuerpo)["access_token"]}

    # 2. no duplicar: busca el mismo título entre las últimas subidas del canal
    st, _, cuerpo = peticion(f"{API}/channels?part=contentDetails&mine=true", cabeceras=auth)
    if st == 200 and json.loads(cuerpo).get("items"):
        subidas = json.loads(cuerpo)["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        st, _, cuerpo = peticion(f"{API}/playlistItems?part=snippet&maxResults=50&playlistId={subidas}", cabeceras=auth)
        for it in json.loads(cuerpo).get("items", []) if st == 200 else []:
            if it["snippet"]["title"].strip().lower() == titulo.strip().lower():
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
    print(json.dumps({"ok": True, "id": v["id"], "url": f"https://youtube.com/shorts/{v['id']}",
                      "estado": v.get("status", {}).get("privacyStatus"), "publicaEn": a.publicar_en}, ensure_ascii=False))


if __name__ == "__main__":
    main()
