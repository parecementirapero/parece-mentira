"""Utilidades compartidas: HTTP con reintentos, guardar secretos rotados en GitHub y avisos."""
import json, os, subprocess, sys, time, urllib.error, urllib.request


def http(url, data=None, headers=None, metodo=None, intentos=4):
    """Petición HTTP que devuelve JSON. data puede ser bytes (form) o dict (JSON)."""
    headers = dict(headers or {})
    if isinstance(data, dict):
        data = json.dumps(data).encode(); headers.setdefault("Content-Type", "application/json")
    elif isinstance(data, bytes):
        headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
    for i in range(intentos):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=metodo)
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            cuerpo = e.read().decode(errors="replace")
            if e.code in (429, 500, 502, 503) and i < intentos - 1:
                time.sleep(2 ** i * 3); continue
            raise RuntimeError(f"HTTP {e.code} en {url.split('?')[0]}: {cuerpo[:500]}") from None
        except urllib.error.URLError:
            if i < intentos - 1:
                time.sleep(2 ** i * 3); continue
            raise


def ocultar(valor):
    """Que GitHub Actions no enseñe nunca este valor en los registros."""
    if os.environ.get("GITHUB_ACTIONS") and valor:
        print(f"::add-mask::{valor}")


def guardar_secreto(nombre, valor):
    """Guarda un token rotado como secreto del repo (GitHub Actions + GH_PAT). Fuera de Actions, lo avisa.

    Devuelve True si se guardó. Si falla, el token nuevo se perdería: por eso se avisa en rojo.
    """
    ocultar(valor)
    repo, pat = os.environ.get("GITHUB_REPOSITORY"), os.environ.get("GH_PAT")
    if not (repo and pat):
        print(f"AVISO: no se puede guardar el secreto {nombre} (falta GH_PAT o no es GitHub Actions). "
              f"Si el token anterior deja de valer, habrá que volver a autorizar.", file=sys.stderr)
        return False
    r = subprocess.run(["gh", "secret", "set", nombre, "--repo", repo, "--body", valor],
                       env={**os.environ, "GH_TOKEN": pat}, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"::error::No se pudo guardar el secreto {nombre}: {r.stderr.strip()[:300]}")
        return False
    return True


def faltan(*nombres):
    return [n for n in nombres if not os.environ.get(n)]
