"""Imágenes reales con licencia abierta para Parece Mentira, sin poner en riesgo la monetización (2026-11-16, Nico).

Uso (desde la raíz del repo; necesita red a los dominios de DOMINIOS):
  python3 -m motor.openverse buscar "nuremberg 1561 broadsheet" [-n 10]
  python3 -m motor.openverse descargar <id de Openverse> --lote DIR_LOTE --video 01 [--uso "plano 7, grabado de Núremberg"]
  python3 -m motor.openverse creditos DIR_LOTE --video 01        → texto para pegar al final de la descripción

Reglas (DECISIONS 2026-11-16 — Nico; el objetivo es monetizar, así que ante la duda NO se usa):
1. Licencias aceptadas: dominio público (PDM), CC0 y CC BY (cualquier versión). Fuera: SA (compartir igual: recortar,
   animar o poner texto es adaptación y obligaría a licenciar el vídeo igual), NC (no comercial) y ND (sin cambios).
2. Solo fuentes institucionales donde la licencia se puede comprobar en origen: Wikimedia Commons y The Met.
3. Openverse NO verifica licencias: cada imagen se comprueba en la fuente original (API de Commons / API del Met)
   y se rechaza si la licencia no coincide, si hay restricciones (derechos de imagen, marca registrada…) o si falta algo.
4. Con CC BY el crédito es obligatorio: va en la descripción de cada red (`creditos`).
5. Todo queda en `<lote>/creditos.json` (qué, de dónde, licencia comprobada, fecha, SHA-256, dónde se usa).
6. Nada de personas reales identificables ni logotipos: lo revisa el agente mirando la imagen antes de usarla.
"""
import argparse
import datetime
import hashlib
import html
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.openverse.org/v1/images/"
LICENCIAS_OK = {"cc0", "pdm", "by"}
FUENTES_OK = {"wikimedia", "met"}
DOMINIOS = ["api.openverse.org", "commons.wikimedia.org", "upload.wikimedia.org",
            "collectionapi.metmuseum.org", "images.metmuseum.org"]
UA = "ParecementiraBot/1.0 (parecementirapero.media@gmail.com)"
RESTRICCIONES_MALAS = ("personality", "trademark", "insignia", "costume", "ngo", "nazi", "communist")


def _ctx():
    for ruta in ("/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt"):
        if os.path.isfile(ruta):
            return ssl.create_default_context(cafile=ruta)
    return ssl.create_default_context()


def _get(url, binario=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, context=_ctx(), timeout=60) as r:
            datos = r.read()
    except urllib.error.URLError as e:
        raise SystemExit(json.dumps({"ok": False, "error": f"sin acceso a {urllib.parse.urlparse(url).netloc}: {e}",
                                     "ayuda": "permitir en claude.ai → Settings → Capabilities: " + ", ".join(DOMINIOS)},
                                    ensure_ascii=False))
    return datos if binario else json.loads(datos)


def _limpio(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()


# ---------- 1. búsqueda ----------
def filtrar(resultados):
    """Primera criba con los datos de Openverse (luego se comprueba en origen)."""
    out = []
    for x in resultados:
        lic = (x.get("license") or "").lower()
        if lic not in LICENCIAS_OK or (x.get("source") or "").lower() not in FUENTES_OK:
            continue
        if x.get("mature"):
            continue
        if (x.get("width") or 0) and (x.get("width") or 0) < 1000 and (x.get("height") or 0) < 1000:
            continue      # demasiado pequeña para un plano 1080×1920
        out.append(x)
    return out


def buscar(q, n=10):
    params = {"q": q, "license": ",".join(sorted(LICENCIAS_OK)), "source": ",".join(sorted(FUENTES_OK)),
              "page_size": min(50, max(n * 3, 20)), "mature": "false"}
    r = _get(API + "?" + urllib.parse.urlencode(params))
    return filtrar(r.get("results", []))[:n]


# ---------- 2. comprobación en origen ----------
def licencia_commons(meta):
    """meta = extmetadata de la API de Commons. Devuelve (código, versión) o None si no vale."""
    corta = (meta.get("LicenseShortName", {}).get("value") or "").strip()
    url = (meta.get("LicenseUrl", {}).get("value") or "").lower()
    c = corta.lower()
    if any(t in c for t in ("sa", "nc", "nd")) and "cc" in c:
        return None
    if "nc" in url or "-nd" in url or "-sa" in url:
        return None
    if c in ("cc0", "cc-zero") or "publicdomain/zero" in url:
        return ("cc0", "1.0")
    if c.startswith("public domain") or c.startswith("pd") or "publicdomain/mark" in url:
        plantilla = (meta.get("License", {}).get("value") or "").lower()
        terminos = (meta.get("UsageTerms", {}).get("value") or "").lower() + " " + c
        solo_eeuu = (plantilla.startswith("pd-us") and not plantilla.startswith("pd-usgov")) or \
            ("united states" in terminos and "worldwide" not in terminos)
        if solo_eeuu or (meta.get("Copyrighted", {}).get("value") or "").lower() == "true":
            return None   # dominio público solo en EE. UU. (o marcado con derechos): no vale para España/Latinoamérica
        return ("pdm", "1.0")
    m = re.match(r"cc[ -]by[ -]?(\d\.\d)?$", c)
    if m:
        return ("by", m.group(1) or "")
    return None


def comprobar_commons(item):
    titulo = urllib.parse.unquote((item.get("foreign_landing_url") or "").rsplit("/", 1)[-1])
    if not titulo.lower().startswith("file:"):
        return {"ok": False, "motivo": "no es una página de archivo de Commons"}
    q = urllib.parse.urlencode({"action": "query", "titles": titulo, "prop": "imageinfo",
                                "iiprop": "url|extmetadata|size|sha1", "format": "json"})
    d = _get("https://commons.wikimedia.org/w/api.php?" + q)
    return evaluar_commons(d)


def evaluar_commons(d):
    pags = list(d.get("query", {}).get("pages", {}).values())
    if not pags or "imageinfo" not in pags[0]:
        return {"ok": False, "motivo": "Commons no devuelve el archivo (¿borrado?)"}
    ii = pags[0]["imageinfo"][0]
    meta = ii.get("extmetadata", {})
    lic = licencia_commons(meta)
    if not lic:
        return {"ok": False, "motivo": "licencia en Commons no aceptada: " + (meta.get("LicenseShortName", {}).get("value") or "?")}
    restr = (meta.get("Restrictions", {}).get("value") or "").lower()
    if any(r in restr for r in RESTRICCIONES_MALAS):
        return {"ok": False, "motivo": "restricciones en Commons: " + restr}
    if "Template:Copyvio" in json.dumps(meta) or "Deletion" in (meta.get("Categories", {}).get("value") or ""):
        return {"ok": False, "motivo": "archivo marcado para borrar o posible copia ilegal"}
    autor = _limpio(meta.get("Artist", {}).get("value")) or "Autor desconocido"
    return {"ok": True, "fuente": "Wikimedia Commons", "licencia": lic[0], "version": lic[1],
            "licencia_nombre": _limpio(meta.get("LicenseShortName", {}).get("value")),
            "licencia_url": meta.get("LicenseUrl", {}).get("value", ""),
            "autor": autor, "titulo": pags[0].get("title", "").replace("File:", ""),
            "pagina": ii.get("descriptionurl", ""), "archivo_url": ii.get("url", ""),
            "ancho": ii.get("width"), "alto": ii.get("height"), "restricciones": restr}


def comprobar_met(item):
    m = re.search(r"/(\d+)/?$", item.get("foreign_landing_url") or "")
    if not m:
        return {"ok": False, "motivo": "no encuentro el id del Met"}
    d = _get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{m.group(1)}")
    return evaluar_met(d)


def evaluar_met(d):
    if not d.get("isPublicDomain"):
        return {"ok": False, "motivo": "el Met no la marca como dominio público"}
    if not d.get("primaryImage"):
        return {"ok": False, "motivo": "el Met no da imagen en alta"}
    return {"ok": True, "fuente": "The Metropolitan Museum of Art", "licencia": "cc0", "version": "1.0",
            "licencia_nombre": "CC0 (Open Access del Met)", "licencia_url": "https://creativecommons.org/publicdomain/zero/1.0/",
            "autor": d.get("artistDisplayName") or "Autor desconocido", "titulo": d.get("title", ""),
            "pagina": d.get("objectURL", ""), "archivo_url": d["primaryImage"], "ancho": None, "alto": None, "restricciones": ""}


def comprobar(item):
    fuente = (item.get("source") or "").lower()
    if fuente == "wikimedia":
        r = comprobar_commons(item)
    elif fuente == "met":
        r = comprobar_met(item)
    else:
        r = {"ok": False, "motivo": "fuente no aceptada: " + fuente}
    # la licencia de origen manda; si Openverse decía otra cosa, se apunta
    if r.get("ok") and r["licencia"] != (item.get("license") or "").lower():
        r["aviso"] = f"Openverse decía «{item.get('license')}», en origen es «{r['licencia']}» (vale la de origen)"
    return r


# ---------- 3. descarga y registro ----------
def credito(e):
    if e["licencia"] == "by":
        lic = f"CC BY {e['version']}".strip()
        return f"{e['titulo']} — {e['autor']} ({e['fuente']}), {lic}: {e['pagina']}"
    nombre = "dominio público" if e["licencia"] == "pdm" else "CC0"
    return f"{e['titulo']} — {e['autor']} ({e['fuente']}), {nombre}: {e['pagina']}"


def descargar(item_id, lote, video, uso=""):
    item = _get(API + item_id + "/")
    if not filtrar([item]):
        raise SystemExit(json.dumps({"ok": False, "error": "no pasa la criba (licencia, fuente, tamaño o contenido sensible)"}, ensure_ascii=False))
    r = comprobar(item)
    if not r.get("ok"):
        raise SystemExit(json.dumps({"ok": False, "error": "rechazada al comprobar en origen", "motivo": r.get("motivo")}, ensure_ascii=False))
    datos = _get(r["archivo_url"], binario=True)
    ext = os.path.splitext(urllib.parse.urlparse(r["archivo_url"]).path)[1].lower() or ".jpg"
    carpeta = os.path.join(lote, "reales")
    os.makedirs(carpeta, exist_ok=True)
    nombre = f"{video}-{re.sub(r'[^a-z0-9]+', '-', r['titulo'].lower())[:40].strip('-')}{ext}"
    with open(os.path.join(carpeta, nombre), "wb") as fh:
        fh.write(datos)
    e = {**r, "video": video, "archivo": f"reales/{nombre}", "openverse_id": item_id,
         "sha256": hashlib.sha256(datos).hexdigest(), "comprobado": datetime.date.today().isoformat(),
         "uso": uso, "revision_visual": "pendiente (sin personas reales identificables ni logotipos)"}
    e["credito"] = credito(e)
    ruta = os.path.join(lote, "creditos.json")
    todos = json.load(open(ruta, encoding="utf-8")) if os.path.isfile(ruta) else []
    todos = [x for x in todos if not (x.get("openverse_id") == item_id and x.get("video") == video)] + [e]
    with open(ruta, "w", encoding="utf-8") as fh:
        json.dump(todos, fh, ensure_ascii=False, indent=1)
    return e


def creditos(lote, video):
    ruta = os.path.join(lote, "creditos.json")
    if not os.path.isfile(ruta):
        return ""
    es = [e for e in json.load(open(ruta, encoding="utf-8")) if e.get("video") == video]
    if not es:
        return ""
    return "Imágenes:\n" + "\n".join("- " + e["credito"] for e in es)


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("buscar"); b.add_argument("q"); b.add_argument("-n", type=int, default=10)
    d = sub.add_parser("descargar"); d.add_argument("id"); d.add_argument("--lote", required=True)
    d.add_argument("--video", required=True); d.add_argument("--uso", default="")
    c = sub.add_parser("creditos"); c.add_argument("lote"); c.add_argument("--video", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "buscar":
        res = buscar(a.q, a.n)
        print(json.dumps([{"id": x["id"], "titulo": x.get("title"), "fuente": x.get("source"), "licencia": x.get("license"),
                           "tam": f"{x.get('width')}×{x.get('height')}", "miniatura": x.get("thumbnail"),
                           "pagina": x.get("foreign_landing_url")} for x in res], ensure_ascii=False, indent=1))
    elif a.cmd == "descargar":
        print(json.dumps({"ok": True, **descargar(a.id, a.lote, a.video, a.uso)}, ensure_ascii=False, indent=1))
    else:
        print(creditos(a.lote, a.video))


if __name__ == "__main__":
    main()
