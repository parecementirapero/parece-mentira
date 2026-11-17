#!/usr/bin/env python3
"""Permiso de TikTok para ENVIAR vídeos (borradores a la bandeja), desde un Mac. Se repite como mucho cada ~6 meses.

Es un permiso aparte del de las estadísticas: usa su propio sandbox de la app de TikTok, uno por ordenador
(el token de TikTok cambia cada vez que se usa, así que dos ordenadores no pueden compartir el mismo).
Pasos previos en developers.tiktok.com: ver publicar/README.md, «TikTok».

Uso, desde la carpeta local del canal:
  python3 publicar/autorizar_tiktok.py --claves claves.txt

Te pide el Client key y el Client secret del sandbox (o los coge de claves.txt si ya están como
TIKTOK_PUB_CLIENT_KEY / TIKTOK_PUB_CLIENT_SECRET), abre el navegador, entras con la cuenta del canal,
aceptas, y lo guarda todo en claves.txt. No enseña ningún token por pantalla.
"""
import argparse, getpass, hashlib, http.server, os, secrets, select, sys, threading, time, urllib.parse, webbrowser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base  # noqa: E402

SCOPES = "user.info.basic,video.upload"
PUERTO = 8767

ap = argparse.ArgumentParser()
ap.add_argument("--claves", required=True)
ap.add_argument("--usuario", default="parece.mentira85", help="el @ de la cuenta de TikTok del canal, sin @")
a = ap.parse_args()
k = base.leer_claves(a.claves)
ck = k.get("TIKTOK_PUB_CLIENT_KEY") or input("Client key del sandbox de publicar: ").strip()
cs = k.get("TIKTOK_PUB_CLIENT_SECRET") or getpass.getpass("Client secret (no se ve al pegarlo): ").strip()
if not ck or not cs:
    sys.exit("Hacen falta el Client key y el Client secret del sandbox.")

estado = secrets.token_urlsafe(16)
verificador = secrets.token_urlsafe(48)
reto = hashlib.sha256(verificador.encode()).hexdigest()  # TikTok escritorio: SHA256 en HEX
resultado = {}


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        if u.path.startswith("/callback") and ("code" in q or "error" in q):
            resultado.update({c: v[0] for c, v in q.items()})
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
            self.wfile.write("<h2>Listo. Ya puedes cerrar esta pestaña y volver a la terminal.</h2>".encode())
        else:
            self.send_response(404); self.end_headers()

    def log_message(self, *args):
        pass


try:
    srv = http.server.HTTPServer(("127.0.0.1", PUERTO), H)
except OSError:
    sys.exit(f"El puerto {PUERTO} está ocupado (¿otra ventana con este mismo script abierta?). Ciérrala y repite.")
redir = f"http://127.0.0.1:{PUERTO}/callback/"
url = "https://www.tiktok.com/v2/auth/authorize/?" + urllib.parse.urlencode({
    "client_key": ck, "scope": SCOPES, "response_type": "code", "redirect_uri": redir, "state": estado,
    "code_challenge": reto, "code_challenge_method": "S256"})
print("\nSe va a abrir el navegador. Entra con la cuenta de TikTok DEL CANAL y acepta los dos permisos.")
print("Si no se abre solo, copia esta dirección en el navegador:\n\n" + url + "\n")
print("Si al final el navegador muestra un error o una página en blanco, copia la dirección")
print(f"de la barra (empieza por http://127.0.0.1:{PUERTO}/callback/) y pégala aquí + Intro.\n")
webbrowser.open(url)


def escuchar():
    while "code" not in resultado and "error" not in resultado:
        srv.handle_request()


threading.Thread(target=escuchar, daemon=True).start()
teclado = True
while "code" not in resultado and "error" not in resultado:
    if not teclado:
        time.sleep(0.5)
        continue
    hay, _, _ = select.select([sys.stdin], [], [], 1)
    if hay:
        linea = sys.stdin.readline()
        if not linea:          # no hay teclado (lanzado sin terminal): solo queda esperar al navegador
            teclado = False
            continue
        linea = linea.strip()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(linea).query)
        if "code" in q or "error" in q:
            resultado.update({c: v[0] for c, v in q.items()})
        elif linea:
            print("Eso no parece la dirección buena (debe contener code=). Prueba otra vez.")

if "error" in resultado:
    sys.exit(f"TikTok devolvió un error: {resultado['error']} — {resultado.get('error_description', '')}")
if resultado.get("state") != estado:
    sys.exit("La respuesta no coincide con la petición (state). Vuelve a intentarlo.")

r = base.pedir(os.environ.get("PM_TIKTOK_API", "https://open.tiktokapis.com").rstrip("/") + "/v2/oauth/token/", formulario={
    "client_key": ck, "client_secret": cs, "code": resultado["code"], "grant_type": "authorization_code",
    "redirect_uri": redir, "code_verifier": verificador})
tok = r.json()
if not tok.get("refresh_token"):
    sys.exit(f"TikTok no dio el permiso: {tok.get('error', r.estado)} — {tok.get('error_description', '')}")
dados = (tok.get("scope") or "").split(",")
if "video.upload" not in dados:
    sys.exit("⚠️  El permiso no incluye «video.upload». Comprueba que el sandbox tiene el producto «Content Posting API» "
             "(y pulsa Apply changes), y repite marcando todos los permisos. No he guardado nada.")
base.guardar_claves(a.claves, {
    "TIKTOK_PUB_CLIENT_KEY": ck, "TIKTOK_PUB_CLIENT_SECRET": cs, "TIKTOK_PUB_USUARIO": a.usuario.lstrip("@"),
    "TIKTOK_PUB_REFRESH_TOKEN": tok["refresh_token"],
    "TIKTOK_PUB_REFRESH_CADUCA": str(int(time.time() + int(tok.get("refresh_expires_in", 0)))) if tok.get("refresh_expires_in") else None,
    "TIKTOK_PUB_ACCESS_TOKEN": tok.get("access_token"),
    "TIKTOK_PUB_ACCESS_CADUCA": str(int(time.time() + int(tok.get("expires_in", 3600)))),
    "TIKTOK_PUB_PERMISOS": tok.get("scope", "")})
dias = int(tok.get("refresh_expires_in", 0)) // 86400
print(f"✅ Autorizado y guardado en {a.claves} (permiso válido unos {dias} días).")
print("   Prueba sin subir nada:  python3 publicar/subir_tiktok.py --claves claves.txt --metadatos <metadatos.json> --clave 01 --video <mp4> --prueba")
