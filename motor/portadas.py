"""Portadas candidatas para cada vídeo y elección de la que más puede atraer (2026-11-16, Nico).

Uso (desde la raíz del repo):
  python3 -m motor.portadas DIR/episodio.json --texto "NO SON SOLO CABEZAS" --clave CABEZAS --salida DIR/portadas
  python3 -m motor.portadas --mp4 video.mp4 --texto "..." --salida DIR/portadas      (desde el MP4 ya montado)

Qué hace:
1. Saca un fotograma cada 0,5 s (sin subtítulos si viene de episodio.json).
2. Puntúa cada fotograma: color, detalle, brillo correcto y que el detalle esté dentro de la zona
   que se ve en las cuadrículas de perfil (Instagram/TikTok recortan a 3:4 por el centro).
3. Para cada diseño de texto (arriba, centro, abajo, dato) busca el fotograma donde el texto
   tape menos lo importante, sin repetir fotogramas parecidos (≥ 2 s de distancia).
4. Puntúa cada portada terminada (imagen + legibilidad a tamaño de cuadrícula + texto corto) y elige
   la mejor. Escribe portada-1..4.jpg, hoja-portadas.jpg (con la vista recortada 3:4) y portadas.json.

Elegir (lo hace Claude mirando hoja-portadas.jpg; la puntuación solo ordena, no basta para elegir):
  python3 -m motor.portadas --elegir DIR/portadas 2 --motivo "astronauta y Tierra: sujeto claro"
Criterios (en este orden): 1) sujeto grande y reconocible al tamaño de la cuadrícula (cara, objeto,
personaje; mejor si enseña la sorpresa que promete el texto); 2) el texto no tapa el sujeto y se lee en
la vista 3:4; 3) contraste y color fuertes; 4) coherente con el primer segundo del vídeo (sin engañar).
La elegida se copia como `portada.jpg`.

La elección es una PREDICCIÓN, no un dato: el diseño elegido se etiqueta (`portada` en
metadatos.json / etiquetas.json) para comprobar con las estadísticas qué diseño funciona de verdad.
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
F_BOLD = os.path.join(AQUI, "fuentes", "Poppins-Bold.ttf")
W, H = 1080, 1920
SEGURA = (0, 240, 1080, 1680)          # 3:4 centrado: lo que se ve en las cuadrículas de perfil
AMARILLO = (255, 210, 63)
OSCURO = (8, 11, 26)

# zona del texto (y centro) para cada diseño; todas dentro de la zona segura
DISENOS = {
    "arriba": {"y": 560, "banda": False},
    "centro": {"y": 960, "banda": True},
    "abajo": {"y": 1380, "banda": False},
    "dato": {"y": 520, "banda": False, "capsula": True},
}


# ---------- fotogramas ----------
def fotogramas_episodio(ruta, cada=0.5):
    sys.path.insert(0, os.path.dirname(AQUI))
    from motor import render
    with open(ruta, encoding="utf-8") as fh:
        s = json.load(fh)
    fin = max(e["fin"] for e in s["escenas"])
    s.pop("audio", None)
    for e in s["escenas"]:      # sin rótulos ni HUD del vídeo: chocarían con el texto de la portada
        e["elementos"] = [el for el in e.get("elementos", []) if el.get("tipo") != "rotulo" and not el.get("hud")]
    s["duracion"] = fin
    s["subtitulos"] = []
    tmp = os.path.join(os.path.dirname(os.path.abspath(ruta)), ".portadas-episodio.json")
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(s, fh, ensure_ascii=False)
    try:
        ep = render.Episodio(tmp)
        ep.subs.dibujar = lambda *a, **k: None
        out, t = [], 0.3
        while t < fin - 0.3:
            out.append((round(t, 2), ep.frame(t).convert("RGB")))
            t += cada
        return out
    finally:
        os.remove(tmp)


def fotogramas_mp4(ruta, cada=0.5):
    d = tempfile.mkdtemp()
    subprocess.check_call(["ffmpeg", "-loglevel", "error", "-i", ruta, "-vf", f"fps={1 / cada},scale={W}:{H}",
                           os.path.join(d, "f%04d.png")])
    out = []
    for i, f in enumerate(sorted(glob.glob(os.path.join(d, "f*.png")))):
        out.append((round(cada * i + cada / 2, 2), Image.open(f).convert("RGB")))
    return out


# ---------- medidas ----------
def _arr(img, w=270, h=480):
    return np.asarray(img.resize((w, h), Image.BILINEAR), dtype=np.float32) / 255.0


def _detalle(a):
    g = a.mean(axis=2)
    gx = np.abs(np.diff(g, axis=1))[:-1, :]
    gy = np.abs(np.diff(g, axis=0))[:, :-1]
    return gx + gy                      # mapa de bordes (h-1, w-1)


def medir(img):
    a = _arr(img)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    rg, yb = r - g, 0.5 * (r + g) - b
    color = float(np.sqrt(rg.std() ** 2 + yb.std() ** 2) + 0.3 * np.sqrt(rg.mean() ** 2 + yb.mean() ** 2))
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    brillo = float(lum.mean())
    contraste = float(lum.std())
    d = _detalle(a)
    y0, y1 = int(SEGURA[1] / H * d.shape[0]), int(SEGURA[3] / H * d.shape[0])
    dentro = float(d[y0:y1].mean())
    fuera = float(np.concatenate([d[:y0].ravel(), d[y1:].ravel()]).mean()) if y0 > 0 else 0.0
    return {"color": color, "brillo": brillo, "contraste": contraste, "detalle": dentro,
            "foco": dentro / (dentro + fuera + 1e-6), "sujeto": sujeto(a)[0], "caja": sujeto(a)[1], "mapa": d}


def sujeto(a):
    """Tamaño del sujeto principal dentro de la zona 3:4: extensión de los bordes fuertes a escala gruesa
    (una cara grande ocupa mucho; una fila de siluetas pequeñas, poco)."""
    g = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).resize((54, 96), Image.BILINEAR), dtype=np.float32) / 255
    d = _detalle(g)
    y0, y1 = int(SEGURA[1] / H * d.shape[0]), int(SEGURA[3] / H * d.shape[0])
    z = d[y0:y1]
    umbral = max(0.08, float(np.percentile(z, 85)))
    ys, xs = np.nonzero(z > umbral)
    if len(ys) < 6:
        return 0.0, None
    ya, yb = np.percentile(ys, 8), np.percentile(ys, 92)
    xa, xb = np.percentile(xs, 8), np.percentile(xs, 92)
    alto, ancho = (yb - ya) / z.shape[0], (xb - xa) / z.shape[1]
    esc_y = (SEGURA[3] - SEGURA[1]) / z.shape[0]
    caja = (SEGURA[1] + ya * esc_y, SEGURA[1] + yb * esc_y)      # franja vertical del sujeto (px)
    return float(min(alto, 1.0) * min(ancho * 1.4, 1.0)), caja


def puntuar_imagen(m):
    pen_brillo = max(0.0, 0.22 - m["brillo"]) * 4 + max(0.0, m["brillo"] - 0.72) * 4
    return (min(m["color"] / 0.35, 1.5) * 1.0 + min(m["detalle"] / 0.06, 1.5) * 1.0
            + min(m["contraste"] / 0.22, 1.3) * 0.6 + m["foco"] * 0.8 + m["sujeto"] * 2.5 - pen_brillo)


def pisa_sujeto(m, y, alto):
    """Parte de la franja del sujeto que queda bajo el texto (0–1)."""
    if not m.get("caja"):
        return 0.0
    a, b = m["caja"]
    t0, t1 = y - alto / 2, y + alto / 2
    return max(0.0, min(b, t1) - max(a, t0)) / max(1.0, b - a)


def tapado(m, y, alto):
    """Cuánto detalle queda bajo la zona del texto (0 = nada importante debajo)."""
    d = m["mapa"]
    a0 = int(max(0, y - alto / 2) / H * d.shape[0])
    a1 = int(min(H, y + alto / 2) / H * d.shape[0])
    if a1 <= a0:
        return 0.0
    return float(d[a0:a1].mean() / (d.mean() + 1e-6))


# ---------- texto ----------
def _lineas(texto, fuente, maxw):
    pal, lineas, cur = texto.split(), [], ""
    for p in pal:
        prueba = (cur + " " + p).strip()
        if cur and fuente.getlength(prueba) > maxw:
            lineas.append(cur)
            cur = p
        else:
            cur = prueba
    if cur:
        lineas.append(cur)
    return lineas


def maquetar(texto, maxw=930, max_lineas=3, tam_max=150, tam_min=70):
    texto = texto.upper()
    for tam in range(tam_max, tam_min - 1, -4):
        f = ImageFont.truetype(F_BOLD, tam)
        ls = _lineas(texto, f, maxw)
        if len(ls) <= max_lineas and all(f.getlength(l) <= maxw for l in ls):
            return f, ls, tam
    f = ImageFont.truetype(F_BOLD, tam_min)
    return f, _lineas(texto, f, maxw), tam_min


def _norm(p):
    import unicodedata
    p = unicodedata.normalize("NFD", p.upper())
    return "".join(c for c in p if c.isalnum() and unicodedata.category(c) != "Mn")


def componer(img, texto, clave, diseno):
    cfg = DISENOS[diseno]
    base = img.convert("RGBA").copy()
    f, ls, tam = maquetar(texto)
    asc, desc = f.getmetrics()
    lh = int((asc + desc) * 1.02)
    alto = lh * len(ls)
    y0 = int(cfg["y"] - alto / 2)
    # oscurecer detrás del texto para que se lea a tamaño de cuadrícula
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dc = ImageDraw.Draw(capa)
    if cfg.get("banda"):
        dc.rectangle((0, y0 - 60, W, y0 + alto + 50), fill=OSCURO + (165,))
        capa = capa.filter(ImageFilter.GaussianBlur(18))
    else:
        dc.ellipse((-200, y0 - 230, W + 200, y0 + alto + 230), fill=OSCURO + (150,))
        capa = capa.filter(ImageFilter.GaussianBlur(70))
    base.alpha_composite(capa)
    claves = {_norm(c) for c in (clave or "").split()}
    txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    caps = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dt, dcap = ImageDraw.Draw(txt), ImageDraw.Draw(caps)
    esp = f.getlength(" ")
    for k, linea in enumerate(ls):
        x = (W - f.getlength(linea)) / 2
        y = y0 + k * lh
        for p in linea.split():
            w = f.getlength(p)
            es_clave = _norm(p) in claves
            color = (255, 255, 255)
            if es_clave and cfg.get("capsula"):
                dcap.rounded_rectangle((x - 22, y + tam * 0.12, x + w + 22, y + tam * 1.1), radius=24,
                                       fill=AMARILLO + (255,))
                color = OSCURO
            elif es_clave:
                color = AMARILLO
            trazo = 0 if (es_clave and cfg.get("capsula")) else max(6, tam // 14)
            dt.text((x, y), p, font=f, fill=color + (255,), stroke_width=trazo, stroke_fill=OSCURO + (255,))
            x += w + esp
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    a = Image.alpha_composite(caps, txt).split()[3].point(lambda v: int(v * 0.7))
    negro = Image.new("RGBA", (W, H), OSCURO + (255,))
    negro.putalpha(a)
    sombra.paste(negro, (0, 10))
    sombra = sombra.filter(ImageFilter.GaussianBlur(14))
    base.alpha_composite(sombra)
    base.alpha_composite(caps)
    base.alpha_composite(txt)
    return base.convert("RGB"), {"tam": tam, "lineas": len(ls), "alto": alto, "y": cfg["y"]}


def legibilidad(portada, info):
    """Contraste del texto a tamaño de cuadrícula (180 px de ancho): alto = se lee en el perfil."""
    a = _arr(portada, 180, 320)
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    y0 = int((info["y"] - info["alto"] / 2) / H * 320)
    y1 = int((info["y"] + info["alto"] / 2) / H * 320)
    zona = lum[max(0, y0):max(y0 + 1, y1)]
    return float(np.percentile(zona, 95) - np.percentile(zona, 25))


# ---------- principal ----------
def generar(frames, texto, clave, salida, n=4):
    os.makedirs(salida, exist_ok=True)
    medidas = [(t, img, medir(img)) for t, img in frames]
    for t, img, m in medidas:
        m["puntos"] = puntuar_imagen(m)
    usados, cands = [], []
    f_tmp, ls_tmp, _ = maquetar(texto)
    asc, desc = f_tmp.getmetrics()
    alto_txt = (asc + desc) * len(ls_tmp) + 120
    for diseno in list(DISENOS)[:n]:
        cfg = DISENOS[diseno]
        mejor = None
        for t, img, m in medidas:
            if any(abs(t - u) < 2.0 for u in usados):
                continue
            v = m["puntos"] - 0.9 * tapado(m, cfg["y"], alto_txt) - 1.5 * pisa_sujeto(m, cfg["y"], alto_txt)
            if mejor is None or v > mejor[0]:
                mejor = (v, t, img, m)
        if mejor is None:
            continue
        v, t, img, m = mejor
        usados.append(t)
        portada, info = componer(img, texto, clave, diseno)
        leg = legibilidad(portada, info)
        pal = len(texto.split())
        total = v + min(leg / 0.6, 1.2) * 1.2 + (0.4 if pal <= 5 else 0.0) - (0.15 * max(0, info["lineas"] - 2))
        cands.append({"diseno": diseno, "t": t, "imagen": portada,
                      "puntuacion": round(total, 3),
                      "detalle": {"fotograma": round(m["puntos"], 3), "sujeto": round(m["sujeto"], 3), "tapa": round(tapado(m, cfg["y"], alto_txt), 3),
                                  "legibilidad": round(leg, 3), "lineas": info["lineas"], "tam_letra": info["tam"]}})
    cands.sort(key=lambda c: -c["puntuacion"])
    for i, c in enumerate(cands, 1):
        c["archivo"] = f"portada-{i}-{c['diseno']}.jpg"
        c["imagen"].save(os.path.join(salida, c["archivo"]), quality=90)
    hoja(cands, os.path.join(salida, "hoja-portadas.jpg"))
    res = {"texto": texto, "clave": clave, "elegida": cands[0]["archivo"] if cands else None,
           "candidatas": [{k: v for k, v in c.items() if k != "imagen"} for c in cands]}
    with open(os.path.join(salida, "portadas.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    return res


def hoja(cands, ruta):
    cw, ch, gh = 360, 640, 360 * 4 // 3
    img = Image.new("RGB", (cw * len(cands) + 20 * (len(cands) + 1), ch + gh // 2 + 110), (16, 18, 28))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(F_BOLD, 22)
    for i, c in enumerate(cands):
        x = 20 + i * (cw + 20)
        im = c["imagen"]
        img.paste(im.resize((cw, ch)), (x, 50))
        rec = im.crop(SEGURA).resize((cw // 2, gh // 2))       # cómo se ve en la cuadrícula del perfil
        img.paste(rec, (x + cw // 4, 60 + ch))
        etiqueta = f"{i + 1}. {c['diseno']} · {c['t']} s · {c['puntuacion']}"
        d.text((x, 14), ("» ELEGIDA  " if i == 0 else "") + etiqueta, font=f,
               fill=AMARILLO if i == 0 else (220, 222, 235))
        if i == 0:
            d.rectangle((x - 4, 46, x + cw + 3, 50 + ch + 3), outline=AMARILLO, width=4)
        d.text((x + cw // 4, 60 + ch + gh // 2 + 6), "cuadrícula 3:4", font=f, fill=(150, 152, 170))
    img.save(ruta, quality=88)


def elegir(carpeta, num, motivo):
    ruta = os.path.join(carpeta, "portadas.json")
    with open(ruta, encoding="utf-8") as fh:
        res = json.load(fh)
    c = res["candidatas"][num - 1]
    res["elegida"] = c["archivo"]
    res["eleccion"] = {"por": "revisión visual", "numero": num, "diseno": c["diseno"], "t": c["t"], "motivo": motivo}
    with open(ruta, "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
    Image.open(os.path.join(carpeta, c["archivo"])).save(os.path.join(carpeta, "portada.jpg"), quality=92)
    return res


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if argv and argv[0] == "--elegir":
        ap = argparse.ArgumentParser()
        ap.add_argument("--elegir", nargs=2, metavar=("CARPETA", "NUM"))
        ap.add_argument("--motivo", required=True)
        a = ap.parse_args(argv)
        r = elegir(a.elegir[0], int(a.elegir[1]), a.motivo)
        print(json.dumps({"elegida": r["elegida"], "eleccion": r["eleccion"]}, ensure_ascii=False))
        return
    ap = argparse.ArgumentParser()
    ap.add_argument("episodio", nargs="?")
    ap.add_argument("--mp4")
    ap.add_argument("--texto", required=True, help="texto de portada, 2–5 palabras")
    ap.add_argument("--clave", default="", help="palabra(s) a resaltar en amarillo")
    ap.add_argument("--salida", required=True)
    ap.add_argument("-n", type=int, default=4)
    a = ap.parse_args(argv)
    if a.mp4:
        frames = fotogramas_mp4(a.mp4)
    elif a.episodio:
        frames = fotogramas_episodio(a.episodio)
    else:
        ap.error("falta episodio.json o --mp4")
    res = generar(frames, a.texto, a.clave, a.salida, a.n)
    if res["elegida"]:
        Image.open(os.path.join(a.salida, res["elegida"])).save(os.path.join(a.salida, "portada.jpg"), quality=92)
    print(json.dumps({"elegida": res["elegida"],
                      "candidatas": [(c["archivo"], c["puntuacion"]) for c in res["candidatas"]]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
