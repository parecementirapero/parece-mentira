#!/usr/bin/env python3
"""Autorización de Google, UNA sola vez, desde un Mac.

Abre el navegador, inicias sesión con la cuenta del canal (parecementirapero.media@gmail.com),
aceptas y el script te enseña el YT_REFRESH_TOKEN para pegarlo en los secretos de GitHub.

Uso (ver README.md):
  python3 estadisticas/autorizar.py CLIENT_ID CLIENT_SECRET
"""
import http.server, json, secrets, sys, urllib.parse, urllib.request, webbrowser

SCOPES = "https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/yt-analytics.readonly"

if len(sys.argv) != 3:
    sys.exit("Uso: python3 estadisticas/autorizar.py CLIENT_ID CLIENT_SECRET")
cid, csec = sys.argv[1], sys.argv[2]
estado = secrets.token_urlsafe(16)
resultado = {}


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if "code" in q or "error" in q:
            resultado.update({k: v[0] for k, v in q.items()})
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
            self.wfile.write("<h2>Listo. Ya puedes cerrar esta pestaña y volver a la terminal.</h2>".encode())
        else:
            self.send_response(404); self.end_headers()

    def log_message(self, *a):
        pass


srv = http.server.HTTPServer(("127.0.0.1", 0), H)
redir = f"http://127.0.0.1:{srv.server_port}"
url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
    "client_id": cid, "redirect_uri": redir, "response_type": "code", "scope": SCOPES,
    "access_type": "offline", "prompt": "consent", "state": estado})
print("\nSe va a abrir el navegador. Entra con la cuenta DUEÑA del canal y acepta.")
print("Si no se abre solo, copia esta dirección en el navegador:\n\n" + url + "\n")
webbrowser.open(url)
while "code" not in resultado and "error" not in resultado:
    srv.handle_request()

if "error" in resultado:
    sys.exit("Google devolvió un error: " + resultado["error"])
if resultado.get("state") != estado:
    sys.exit("La respuesta no coincide con la petición (state). Vuelve a intentarlo.")

cuerpo = urllib.parse.urlencode({"code": resultado["code"], "client_id": cid, "client_secret": csec,
                                 "redirect_uri": redir, "grant_type": "authorization_code"}).encode()
tok = json.loads(urllib.request.urlopen("https://oauth2.googleapis.com/token", cuerpo).read())
if "refresh_token" not in tok:
    sys.exit("Google no devolvió refresh_token. Quita el acceso de la app en myaccount.google.com/permissions y repite.")

print("✅ Autorizado. Pega esto como secreto YT_REFRESH_TOKEN en GitHub (no lo compartas ni lo subas al repo):\n")
print(tok["refresh_token"] + "\n")
