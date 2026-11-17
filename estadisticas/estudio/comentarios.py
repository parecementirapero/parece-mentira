"""Clasifica los comentarios por lo que dicen: lo que los números no cuentan.

Los comentarios están en datos/comentarios.json (los guarda recoger.py; sin nombres ni perfiles de quien
comenta). La clasificación es por reglas sencillas: sirve para contar, no para leer la mente. Con pocos
comentarios, lo mejor sigue siendo leerlos.
"""
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTADISTICAS = os.path.dirname(AQUI)
ARCHIVO = os.path.join(ESTADISTICAS, "datos", "comentarios.json")

# orden = prioridad: la primera categoría que encaja gana
CATEGORIAS = [
    ("spam", r"https?://|suscr[ií]bete a mi|s[ií]gueme|gana dinero|whats?app|telegram|promo"),
    ("menciona a alguien", r"(^|\s)@[\w.]+"),
    ("duda de que sea verdad", r"\bmentira\b|\bfalso\b|\bfake\b|no es (verdad|cierto)|no me lo creo|\bfuente\??$|\bfuentes\?|"
                               r"de d[oó]nde sac|inventad|eso no es as[ií]|\bbulo\b"),
    ("corrige", r"\ben realidad\b|\bcorrecci[oó]n\b|te equivocas|est[aá] mal|no (fue|era|son|es) .{0,30}\bsino\b|\bde hecho\b|error"),
    ("pide otro tema", r"\bhaz (uno|otro|un v[ií]deo)|\bhabla (de|sobre)|\bparte (2|dos)\b|\bsegunda parte\b|pod[eé]is hacer|"
                       r"puedes hacer|\bsiguiente\b.*\b(v[ií]deo|tema)|\bqueremos\b|otro de "),
    ("sobre la voz o el montaje", r"\bvoz\b|\bia\b|\binteligencia artificial\b|\brobot|\bm[uú]sica\b|\bedici[oó]n\b|"
                                  r"\banimaci[oó]n\b|\bsubt[ií]tulos?\b|\bnarrador\b|\bmontaje\b|\bdibujos?\b"),
    ("pregunta", r"\?"),
    ("aporta un dato", r"\d{3,}|\bseg[uú]n\b|\btambi[eé]n (hay|existe|pasa)\b|\bdato\b|\bestudi[oé]\b|\bsab[ií]a(s|n)? que\b|"
                       r"\bpor eso\b|\bporque\b"),
    ("emoción o chiste", r"jaja|jeje|xd+\b|😂|🤣|😱|🤯|😮|❤|🔥|👏|wow|incre[ií]ble|qu[eé] (fuerte|locura|pasada)|brutal|"
                         r"impresionante|me encanta|buen[ií]simo|genial"),
]
PARA_QUE = {
    "pide otro tema": "van a la lista de ideas (`lotes/IDEAS.md`)",
    "pregunta": "pueden ser el siguiente vídeo o el comentario fijado",
    "duda de que sea verdad": "dicen dónde conviene enseñar la fuente en pantalla",
    "corrige": "hay que comprobarlas una a una: si tienen razón, se corrige",
    "menciona a alguien": "es la señal más clara de que el vídeo se comparte",
    "sobre la voz o el montaje": "es la única crítica de forma que llega gratis",
}


def clasificar(texto):
    t = " ".join((texto or "").lower().split())
    for nombre, patron in CATEGORIAS:
        if re.search(patron, t):
            return nombre
    return "otros"


def cargar():
    if not os.path.exists(ARCHIVO):
        return []
    return json.load(open(ARCHIVO, encoding="utf-8")).get("comentarios") or []


def resumen(comentarios=None):
    """{categoría: [comentarios]} y recuento por vídeo."""
    comentarios = cargar() if comentarios is None else comentarios
    por_categoria, por_video = {}, {}
    for c in comentarios:
        cat = clasificar(c.get("texto"))
        por_categoria.setdefault(cat, []).append(c)
        v = por_video.setdefault(c.get("video"), {})
        v[cat] = v.get(cat, 0) + 1
    return por_categoria, por_video


def a_markdown(comentarios=None, titulos=None):
    por_categoria, por_video = resumen(comentarios)
    total = sum(len(v) for v in por_categoria.values())
    L = ["## Comentarios", ""]
    if not total:
        return "\n".join(L + ["Todavía no hay comentarios guardados (`datos/comentarios.json`).", ""])
    L += [f"{total} comentarios clasificados por reglas (orientativo).", "", "| Categoría | Nº | Para qué sirve |", "|---|---|---|"]
    for cat, lista in sorted(por_categoria.items(), key=lambda kv: -len(kv[1])):
        L.append(f"| {cat} | {len(lista)} | {PARA_QUE.get(cat, '—')} |")
    L.append("")
    for cat in ("pide otro tema", "duda de que sea verdad", "corrige", "sobre la voz o el montaje"):
        for c in (por_categoria.get(cat) or [])[:5]:
            titulo = (titulos or {}).get(c.get("video"), c.get("video"))
            L.append(f"- **{cat}** ({titulo}): «{(c.get('texto') or '')[:160]}»")
    return "\n".join(L) + "\n"
