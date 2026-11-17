"""Piezas comunes de los scripts de publicación (TikTok e Instagram). Solo biblioteca estándar.

- claves.txt: leer y actualizar sin tocar el resto de líneas (los tokens que rotan se guardan al momento).
- HTTP con reintentos solo donde repetir no puede duplicar nada.
- Registro `publicado.json` junto a `metadatos.json`: qué se ha enviado ya, para no duplicar.
- Comprobaciones del MP4 (tamaño y «moov» al principio, que Instagram exige).

Nada de aquí imprime claves ni tokens.
"""
import datetime as dt
import json
import os
import re
import ssl
import struct
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

CTX = ssl.create_default_context(cafile="/etc/ssl/cert.pem") if os.path.exists("/etc/ssl/cert.pem") else ssl.create_default_context()
PRUEBAS = os.environ.get("PM_PRUEBAS") == "1"      # solo lo activa publicar/prueba.py (servidor falso en 127.0.0.1)
PAUSA = float(os.environ.get("PM_PAUSA", "1"))      # multiplicador de las esperas (las pruebas lo ponen a 0)


# ---------------------------------------------------------------- salida

def salir(msg, **extra):
    """Termina con una línea JSON de error (misma forma que subir_youtube.py)."""
    print(json.dumps({"ok": False, "error": msg, **extra}, ensure_ascii=False))
    sys.exit(1)


def listo(**datos):
    print(json.dumps({"ok": True, **datos}, ensure_ascii=False))


def dormir(segundos):
    time.sleep(segundos * PAUSA)


def ahora():
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


# ---------------------------------------------------------------- claves.txt

def leer_claves(ruta):
    d = {}
    try:
        with open(ruta, encoding="utf-8") as f:
            for linea in f:
                if "=" in linea and not linea.lstrip().startswith("#"):
                    k, v = linea.split("=", 1)
                    d[k.strip()] = v.strip()
    except FileNotFoundError:
        salir("No encuentro el archivo de claves: " + ruta)
    return d


def guardar_claves(ruta, cambios):
    """Cambia o añade líneas CLAVE=valor sin tocar las demás. Escritura atómica y permisos 600.

    Un valor None borra la línea. Si no se puede escribir lanza OSError: quien llama decide
    (un token rotado que no se guarda obliga a volver a autorizar, así que hay que decirlo alto).
    """
    try:
        with open(ruta, encoding="utf-8") as f:
            lineas = f.read().splitlines()
    except FileNotFoundError:
        lineas = []
    pendientes = dict(cambios)
    salida = []
    for linea in lineas:
        k = linea.split("=", 1)[0].strip() if "=" in linea and not linea.lstrip().startswith("#") else None
        if k in pendientes:
            v = pendientes.pop(k)
            if v is not None:
                salida.append(f"{k}={v}")
        else:
            salida.append(linea)
    for k, v in pendientes.items():
        if v is not None:
            salida.append(f"{k}={v}")
    carpeta = os.path.dirname(os.path.abspath(ruta))
    fd, tmp = tempfile.mkstemp(prefix=".claves-", dir=carpeta)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write("\n".join(salida) + "\n")
        os.chmod(tmp, 0o600)
        os.replace(tmp, ruta)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


# ---------------------------------------------------------------- HTTP

class Respuesta:
    def __init__(self, estado, cabeceras, cuerpo):
        self.estado, self.cabeceras, self.cuerpo = estado, {k.lower(): v for k, v in cabeceras.items()}, cuerpo

    def json(self):
        try:
            return json.loads(self.cuerpo.decode("utf-8", "replace"))
        except ValueError:
            return {}

    def texto(self, n=400):
        return self.cuerpo.decode("utf-8", "replace")[:n]


def pedir(url, metodo=None, datos=None, cabeceras=None, cuerpo_json=None, formulario=None,
          espera=120, intentos=3, repetible=True):
    """Hace una petición y devuelve Respuesta (también con 4xx/5xx: no lanza por el código).

    repetible=False → un solo intento si la petición llegó a salir (publicar, crear): repetir a ciegas
    podría duplicar. Con repetible=True reintenta 429/5xx y cortes de red con espera creciente.
    Lanza OSError solo si no hay manera de conectar.
    """
    cabeceras = dict(cabeceras or {})
    if cuerpo_json is not None:
        datos = json.dumps(cuerpo_json).encode()
        cabeceras.setdefault("Content-Type", "application/json; charset=UTF-8")
    elif formulario is not None:
        datos = urllib.parse.urlencode(formulario).encode()
        cabeceras.setdefault("Content-Type", "application/x-www-form-urlencoded")
    if not (url.startswith("https://") or (PRUEBAS and url.startswith("http://127.0.0.1"))):
        raise OSError("Dirección no permitida (solo https): " + url.split("?")[0])
    ultimo = None
    for i in range(intentos if repetible else 1):
        try:
            req = urllib.request.Request(url, data=datos, headers=cabeceras, method=metodo)
            kw = {"context": CTX} if url.startswith("https://") else {}
            with urllib.request.urlopen(req, timeout=espera, **kw) as r:
                return Respuesta(r.status, dict(r.headers), r.read())
        except urllib.error.HTTPError as e:
            resp = Respuesta(e.code, dict(e.headers or {}), e.read())
            if repetible and e.code in (429, 500, 502, 503, 504) and i < intentos - 1:
                dormir(3 * 2 ** i)
                ultimo = resp
                continue
            return resp
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            ultimo = e
            if repetible and i < intentos - 1:
                dormir(3 * 2 ** i)
                continue
            raise OSError(f"No se pudo conectar con {urllib.parse.urlparse(url).netloc}: {getattr(e, 'reason', e)}") from None
    if isinstance(ultimo, Respuesta):
        return ultimo
    raise OSError("Sin respuesta de " + urllib.parse.urlparse(url).netloc)


# ---------------------------------------------------------------- metadatos y registro

def norma(t):
    """Compara textos sin hashtags, emojis, mayúsculas ni signos (para no duplicar)."""
    return re.sub(r"[^\w]+", "", re.sub(r"#\w+", "", t or "").lower())


def cargar_metadatos(ruta, clave, red):
    try:
        with open(ruta, encoding="utf-8") as f:
            todo = json.load(f)
    except FileNotFoundError:
        salir("No encuentro metadatos.json: " + ruta)
    except ValueError as e:
        salir(f"metadatos.json no es JSON válido: {e}")
    m = todo.get(clave)
    if not m or red not in m or not (m[red].get("texto") or "").strip():
        salir(f"metadatos.json no tiene el vídeo {clave} con su bloque «{red}» y su «texto»")
    return m


def ruta_registro(args):
    return args.registro or os.path.join(os.path.dirname(os.path.abspath(args.metadatos)), "publicado.json")


def leer_registro(ruta):
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except ValueError:
        salir("publicado.json está roto (no es JSON). Arréglalo o bórralo tras comprobar en la red qué se publicó: " + ruta)


def apuntar(ruta, clave, red, **datos):
    """Guarda (fusionando) lo que se sabe de un envío. Se llama en cada paso para poder retomar sin duplicar."""
    reg = leer_registro(ruta)
    entrada = reg.setdefault(clave, {}).setdefault(red, {})
    entrada.update(datos)
    entrada["actualizado"] = ahora()
    fd, tmp = tempfile.mkstemp(prefix=".publicado-", dir=os.path.dirname(os.path.abspath(ruta)))
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    os.replace(tmp, ruta)
    return entrada


# ---------------------------------------------------------------- vídeo

def revisar_mp4(ruta, max_bytes):
    """Comprobaciones baratas antes de gastar una subida. Devuelve (bytes, avisos)."""
    if not os.path.isfile(ruta):
        salir("No encuentro el vídeo: " + ruta)
    tam = os.path.getsize(ruta)
    if tam < 50_000:
        salir(f"El vídeo pesa solo {tam} bytes: parece un archivo roto", video=ruta)
    if tam > max_bytes:
        salir(f"El vídeo pesa {tam / 1e6:.0f} MB y el máximo de esta red es {max_bytes / 1e6:.0f} MB", video=ruta)
    avisos = []
    orden = _atomos(ruta)
    if "ftyp" not in orden[:1]:
        salir("El archivo no parece un MP4 (no empieza por «ftyp»)", video=ruta)
    if "moov" not in orden:
        salir("El MP4 no tiene índice («moov»): el render se cortó a medias", video=ruta)
    if "mdat" in orden and orden.index("moov") > orden.index("mdat"):
        avisos.append("El índice del MP4 («moov») va al final. Instagram lo pide al principio: "
                      "ffmpeg -i entrada.mp4 -c copy -movflags +faststart salida.mp4")
    return tam, avisos


def _atomos(ruta):
    """Nombres de los átomos de primer nivel del MP4, en orden."""
    nombres = []
    with open(ruta, "rb") as f:
        fin = os.path.getsize(ruta)
        pos = 0
        while pos + 8 <= fin and len(nombres) < 64:
            f.seek(pos)
            cab = f.read(16)
            tam, nombre = struct.unpack(">I4s", cab[:8])
            if tam == 1 and len(cab) == 16:
                tam = struct.unpack(">Q", cab[8:])[0]
            elif tam == 0:
                tam = fin - pos
            nombres.append(nombre.decode("latin-1"))
            if tam < 8:
                break
            pos += tam
    return nombres
