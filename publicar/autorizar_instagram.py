#!/usr/bin/env python3
"""Permiso de Instagram para PUBLICAR Reels subiendo el archivo (Facebook Login), desde un Mac.

Convierte el token corto que da el «Explorador de la API Graph» de Meta en un token de página que no caduca
y lo guarda en claves.txt junto al número de la cuenta de Instagram. Pasos previos: publicar/README.md, «Instagram».

Uso, desde la carpeta local del canal:
  python3 publicar/autorizar_instagram.py --claves claves.txt [--cuenta parecementiramedia]

Te pide el identificador de la app, su clave secreta y el token corto (no se ven al pegarlos, salvo el
identificador). No enseña ningún token por pantalla.
"""
import argparse, getpass, os, sys, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import base  # noqa: E402

G = os.environ.get("PM_IG_FB", "https://graph.facebook.com").rstrip("/")
NECESARIOS = {"instagram_basic", "instagram_content_publish", "pages_show_list", "pages_read_engagement"}

ap = argparse.ArgumentParser()
ap.add_argument("--claves", required=True)
ap.add_argument("--cuenta", default="parecementiramedia", help="usuario de Instagram del canal, sin @")
a = ap.parse_args()
k = base.leer_claves(a.claves)
app_id = k.get("IG_APP_ID") or input("Identificador de la app de Meta (App ID): ").strip()
secreto = k.get("IG_APP_SECRET") or getpass.getpass("Clave secreta de la app (no se ve al pegarla): ").strip()
corto = getpass.getpass("Token de acceso de usuario del Explorador de la API Graph (no se ve al pegarlo): ").strip()
if not (app_id and secreto and corto):
    sys.exit("Hacen falta los tres datos.")


def get(ruta, **p):
    r = base.pedir(f"{G}/{ruta}?" + urllib.parse.urlencode(p))
    d = r.json()
    if r.estado != 200 or "error" in d:
        e = d.get("error") or {}
        sys.exit(f"Meta devolvió un error en «{ruta.split('?')[0]}»: {e.get('message', r.estado)} (código {e.get('code')})")
    return d


# 1. qué permisos trae el token
info = get("debug_token", input_token=corto, access_token=f"{app_id}|{secreto}").get("data", {})
if not info.get("is_valid"):
    sys.exit("Meta dice que ese token no vale (¿caducado? duran 1–2 horas). Genera otro en el Explorador y repite.")
faltan = NECESARIOS - set(info.get("scopes") or [])
if faltan:
    sys.exit("Al token le faltan permisos: " + ", ".join(sorted(faltan)) + ". En el Explorador, añádelos y genera el token otra vez.")

# 2. token de usuario largo (60 días) → token de página (sin caducidad)
largo = get("oauth/access_token", grant_type="fb_exchange_token", client_id=app_id, client_secret=secreto,
            fb_exchange_token=corto).get("access_token")
if not largo:
    sys.exit("Meta no dio el token largo.")
paginas = get("me/accounts", fields="name,access_token,instagram_business_account{id,username}", limit=100,
              access_token=largo).get("data", [])
con_ig = [p for p in paginas if p.get("instagram_business_account")]
if not con_ig:
    sys.exit("Ninguna de tus páginas de Facebook tiene una cuenta de Instagram enlazada. En Instagram (móvil): "
             "Editar perfil → Página → conectar o crear una página, y repite. Al generar el token, marca la página.")
quiere = a.cuenta.lstrip("@").lower()
elegidas = [p for p in con_ig if (p["instagram_business_account"].get("username") or "").lower() == quiere] or \
           (con_ig if len(con_ig) == 1 else [])
if not elegidas:
    sys.exit("No encuentro @" + quiere + " entre las cuentas enlazadas: " +
             ", ".join("@" + (p["instagram_business_account"].get("username") or "?") for p in con_ig) + ". Usa --cuenta.")
pag = elegidas[0]
ig = pag["instagram_business_account"]

# 3. comprobar la caducidad real del token de página
caduca = get("debug_token", input_token=pag["access_token"], access_token=f"{app_id}|{secreto}").get("data", {}).get("expires_at")
base.guardar_claves(a.claves, {"IG_APP_ID": app_id, "IG_APP_SECRET": secreto, "IG_USER_ID": ig["id"],
                               "IG_FB_TOKEN": pag["access_token"], "IG_CUENTA": ig.get("username") or quiere})
print(f"✅ Guardado en {a.claves}: cuenta @{ig.get('username')} (página «{pag.get('name')}»).")
print("   El token " + ("no caduca (deja de valer si se cambia la contraseña de Facebook o se pierde el papel en la página)."
                        if not caduca else "caduca: habrá que repetir este paso; Meta no ha dado uno permanente."))
print("   Prueba sin publicar nada:  python3 publicar/subir_instagram.py --claves claves.txt --metadatos <metadatos.json> --clave 01 --video <mp4> --prueba")
