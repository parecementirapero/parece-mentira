#!/usr/bin/env python3
"""Autorización de TikTok, desde un Mac (se repite como mucho cada ~6 meses).

Abre el navegador, entras con la cuenta del canal (parece.mentira85), aceptas y el script
te enseña el TIKTOK_REFRESH_TOKEN para pegarlo en los secretos de GitHub.

Uso (ver README.md):
  python3 estadisticas/autorizar_tiktok.py CLIENT_KEY CLIENT_SECRET
"""
import hashlib, http.server, json, os, secrets, select, ssl, sys, threading, urllib.parse, urllib.request, webbrowser

CTX = ssl.create_default_context(cafile="/etc/ssl/cert.pem") if os.path.exists("/etc/ssl/cert.pem") else ssl.create_default_context()

SCOPES = "user.info.basic,user.info.stats,video.list"
if len(sys.argv) != 3:
    sys.exit("Uso: python3 estadisticas/autorizar_tiktok.py CLIENT_KEY CLIENT_SECRET")
ck, cs = sys.argv[1], sys.argv[2]
estado = secrets.token_urlsafe(16)
verificador = secrets.token_urlsafe(48)
reto = hashlib.sha256(verificador.encode()).hexdigest()  # TikTok escritorio: SHA256 en HEX
resultado = {}


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        if u.path.startswith("/callback") and ("code" in q or "error" in q):
            resultado.update({k: v[0] for k, v in q.items()})
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
            self.wfile.write("<h2>Listo. Ya puedes cerrar esta pestaña y volver a la terminal.</h2>".encode())
        else:
            self.send_response(404); self.end_headers()

    def log_message(self, *a):
        pass


srv = http.server.HTTPServer(("127.0.0.1", 8766), H)
redir = f"http://127.0.0.1:{srv.server_port}/callback/"
url = "https://www.tiktok.com/v2/auth/authorize/?" + urllib.parse.urlencode({
    "client_key": ck, "scope": SCOPES, "response_type": "code", "redirect_uri": redir, "state": estado,
    "code_challenge": reto, "code_challenge_method": "S256"})
print("\nSe va a abrir el navegador. Entra con la cuenta de TikTok DEL CANAL y acepta.")
print("Si no se abre solo, copia esta dirección en el navegador:\n\n" + url + "\n")
print("Si al final el navegador muestra un error o una página en blanco, copia la dirección")
print("de la barra (empieza por http://127.0.0.1:8766/callback/) y pégala aquí + Intro.\n")
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
    sys.exit(f"TikTok devolvió un error: {resultado['error']} — {resultado.get('error_description', '')}")
if resultado.get("state") != estado:
    sys.exit("La respuesta no coincide con la petición (state). Vuelve a intentarlo.")
faltan = set(SCOPES.split(",")) - set(resultado.get("scopes", "").split(","))
if faltan:
    print("⚠️  No has aceptado todos los permisos (faltan: " + ", ".join(sorted(faltan)) + "). Repite y márcalos todos.")

cuerpo = urllib.parse.urlencode({"client_key": ck, "client_secret": cs, "code": resultado["code"],
                                 "grant_type": "authorization_code", "redirect_uri": redir,
                                 "code_verifier": verificador}).encode()
req = urllib.request.Request("https://open.tiktokapis.com/v2/oauth/token/", cuerpo,
                             {"Content-Type": "application/x-www-form-urlencoded"})
tok = json.loads(urllib.request.urlopen(req, context=CTX).read())
if "refresh_token" not in tok:
    sys.exit(f"TikTok no devolvió refresh_token: {tok}")
dias = tok.get("refresh_expires_in", 0) // 86400
print(f"✅ Autorizado (válido unos {dias} días). Pega esto como secreto TIKTOK_REFRESH_TOKEN en GitHub:\n")
print(tok["refresh_token"] + "\n")
if os.path.exists("claves.txt"):
    with open("claves.txt", "a", encoding="utf-8") as f:
        f.write("\nTIKTOK_REFRESH_TOKEN=" + tok["refresh_token"] + "\n")
    print("También lo he guardado al final de claves.txt (línea TIKTOK_REFRESH_TOKEN=).")
