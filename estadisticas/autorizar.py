#!/usr/bin/env python3
"""Autorización de Google, UNA sola vez, desde un Mac.

Abre el navegador, inicias sesión con la cuenta del canal (parecementirapero.media@gmail.com),
aceptas y el script te enseña el YT_REFRESH_TOKEN para pegarlo en los secretos de GitHub.

Uso (ver README.md):
  python3 estadisticas/autorizar.py CLIENT_ID CLIENT_SECRET
"""
import http.server, json, os, secrets, select, ssl, sys, threading, urllib.parse, urllib.request, webbrowser

# El Python de python.org en Mac a veces no trae certificados: usamos los del sistema si existen.
CTX = ssl.create_default_context(cafile="/etc/ssl/cert.pem") if os.path.exists("/etc/ssl/cert.pem") else ssl.create_default_context()

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


srv = http.server.HTTPServer(("127.0.0.1", 8765), H)
redir = f"http://127.0.0.1:{srv.server_port}"
url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
    "client_id": cid, "redirect_uri": redir, "response_type": "code", "scope": SCOPES,
    "access_type": "offline", "prompt": "consent", "state": estado})
print("\nSe va a abrir el navegador. Entra con la cuenta DUEÑA del canal y acepta.")
print("Si no se abre solo, copia esta dirección en el navegador:\n\n" + url + "\n")
print("Si al final el navegador muestra un error o una página en blanco, copia la dirección")
print("de la barra (empieza por http://127.0.0.1:8765/) y pégala aquí + Intro.\n")
webbrowser.open(url)


def escuchar():
    while "code" not in resultado and "error" not in resultado:
        srv.handle_request()


threading.Thread(target=escuchar, daemon=True).start()
while "code" not in resultado and "error" not in resultado:
    listo, _, _ = select.select([sys.stdin], [], [], 1)
    if listo:
        linea = sys.stdin.readline().strip()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(linea).query)
        if "code" in q or "error" in q:
            resultado.update({k: v[0] for k, v in q.items()})
        elif linea:
            print("Eso no parece la dirección buena (debe contener code=). Prueba otra vez.")

if "error" in resultado:
    sys.exit("Google devolvió un error: " + resultado["error"])
if resultado.get("state") != estado:
    sys.exit("La respuesta no coincide con la petición (state). Vuelve a intentarlo.")

cuerpo = urllib.parse.urlencode({"code": resultado["code"], "client_id": cid, "client_secret": csec,
                                 "redirect_uri": redir, "grant_type": "authorization_code"}).encode()
tok = json.loads(urllib.request.urlopen("https://oauth2.googleapis.com/token", cuerpo, context=CTX).read())
if "refresh_token" not in tok:
    sys.exit("Google no devolvió refresh_token. Quita el acceso de la app en myaccount.google.com/permissions y repite.")

print("✅ Autorizado. Pega esto como secreto YT_REFRESH_TOKEN en GitHub (no lo compartas ni lo subas al repo):\n")
print(tok["refresh_token"] + "\n")
if os.path.exists("claves.txt"):
    with open("claves.txt", "a", encoding="utf-8") as f:
        f.write("\nYT_REFRESH_TOKEN=" + tok["refresh_token"] + "\n")
    print("También lo he guardado al final de claves.txt (línea YT_REFRESH_TOKEN=).")
