"""Mediciones a edad fija: los mismos números de cada vídeo a las 24 h, 48 h, 7 días y 28 días.

Problema que resuelve: hoy cada lectura se hace «cuando toca» y los vídeos se comparan con edades
distintas (uno con 31 h y otro con 2 h). Aquí cada vídeo tiene una medición por edad, y una vez
guardada NO se vuelve a tocar: es la foto de ese vídeo a esa edad.

Fuentes (todas ya existen en el repo):
  datos/data.json      foto diaria de vistas (historico) y los contadores de hoy de YouTube y TikTok
  studio.json          «se quedaron viendo», vistas y horas de YouTube Studio (lecturas con fecha y hora)
  tiktok_studio.json   tiempo medio, % que lo ve entero y curva de TikTok Studio

Salida: datos/mediciones.json
  {clave: {"youtube": {"48": {...}}, "tiktok": {"48": {...}}}}   clave = id de YouTube (o de TikTok si no hay)
"""
import datetime as dt
import json
import math
import os
from zoneinfo import ZoneInfo

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTADISTICAS = os.path.dirname(AQUI)
MADRID = ZoneInfo("Europe/Madrid")
SALIDA = os.path.join(ESTADISTICAS, "datos", "mediciones.json")

EDADES = (24, 48, 168, 672)                       # horas: 1 día, 2 días, 7 días, 28 días
MARGEN = {24: 24, 48: 24, 168: 48, 672: 72}       # una lectura vale para la edad E si se hizo entre E y E + margen
HORA_FOTO = "09:20"                               # la foto diaria de data.json se hace hacia esa hora
CUENTAS = ("vistas", "likes", "comentarios", "compartidos", "subs")   # se interpolan a la edad exacta
NOMBRE_EDAD = {24: "24 h", 48: "48 h", 168: "7 d", 672: "28 d"}


def _json(nombre):
    ruta = os.path.join(ESTADISTICAS, nombre)
    if not os.path.exists(ruta):
        return {}
    return json.load(open(ruta, encoding="utf-8"))


def _momento(fecha, hora=None):
    try:
        return dt.datetime.fromisoformat(f"{fecha}T{hora or '12:00'}").replace(tzinfo=MADRID)
    except (ValueError, TypeError):
        return None


def _horas(a, b):
    return (b - a).total_seconds() / 3600


def lecturas(data, studio, tiktok_studio):
    """Junta todas las lecturas con su momento. Devuelve (publicado, lecturas, union):
    publicado[(red, id)] = momento de publicación
    lecturas[(red, id)]  = lista de {"t": momento, "origen": ..., métricas...}
    union[id de TikTok]  = id de YouTube del mismo vídeo"""
    publicado, lect, union = {}, {}, {}
    generado = None
    try:
        generado = dt.datetime.fromisoformat(data.get("generado"))
        if generado.tzinfo is None:
            generado = generado.replace(tzinfo=MADRID)
    except (TypeError, ValueError):
        pass

    for c in data.get("contenidos") or []:
        if c.get("youtube") and c.get("tiktok"):
            union[c["tiktok"]] = c["youtube"]

    def anade(red, vid, lectura):
        if lectura.get("t") is not None:
            lect.setdefault((red, vid), []).append(lectura)

    # contadores de hoy
    for v in data.get("videos") or []:
        publicado[("youtube", v["id"])] = _momento(v.get("fecha"), v.get("hora"))
        seg = v.get("duracionMedia")
        anade("youtube", v["id"], {
            "t": generado, "origen": "api", "vistas": v.get("vistas"), "likes": v.get("likes"),
            "comentarios": v.get("comentarios"), "compartidos": v.get("compartidos"), "subs": v.get("subs"),
            "pct_visto": v.get("pctVisto"), "seg_por_vista_api": seg, "vistas_enganchadas": v.get("vistasEnganchadas"),
            "retencion_3s": v.get("retencion3s")})
    for v in (data.get("tiktok") or {}).get("videos") or []:
        publicado[("tiktok", v["id"])] = _momento(v.get("fecha"), v.get("hora"))
        anade("tiktok", v["id"], {"t": generado, "origen": "api", "vistas": v.get("vistas"), "likes": v.get("likes"),
                                  "comentarios": v.get("comentarios"), "compartidos": v.get("compartidos")})

    # foto diaria de vistas
    for fecha, foto in (data.get("historico") or {}).items():
        t = _momento(fecha, HORA_FOTO)
        if generado and fecha == generado.date().isoformat():
            continue  # la de hoy ya está, con su hora exacta y más métricas
        for red in ("youtube", "tiktok"):
            for vid, vistas in (foto.get(red) or {}).items():
                anade(red, vid, {"t": t, "origen": "foto diaria", "vistas": vistas})

    # YouTube Studio (lecturas a mano o con herramientas/studio_shorts.js)
    for vid, s in studio.items():
        if vid.startswith("_") or not isinstance(s, dict):
            continue
        for l in [s] + list(s.get("antes") or []):
            if l.get("seQuedan") is None:
                continue
            spv = l.get("seg_por_vista")
            if spv is None and l.get("horas") and l.get("vistas"):
                spv = round(l["horas"] * 3600 / l["vistas"], 1)
            anade("youtube", vid, {"t": _momento(l.get("fecha"), l.get("hora")), "origen": "studio",
                                   "hora_exacta": bool(l.get("hora")),
                                   "se_quedan": l.get("seQuedan"), "seg_por_vista": spv,
                                   "vistas_studio": l.get("vistas")})

    # TikTok Studio
    for cuando, videos in tiktok_studio.items():
        if cuando.startswith("_") or not isinstance(videos, dict):
            continue
        fecha, _, hora = cuando.partition(" ")
        t = _momento(fecha, hora or None)
        for vid, s in videos.items():
            if s.get("medio_s") is None and not s.get("curva"):
                continue
            curva = {int(k): v for k, v in (s.get("curva") or {}).items()}
            anade("tiktok", vid, {"t": t, "origen": "tiktok studio", "medio_s": s.get("medio_s"),
                                  "completo_pct": s.get("completo_pct"), "sigue_3s": curva.get(3),
                                  "vistas_studio": s.get("vistas"), "curva": curva or None, "duracion": s.get("dur")})
    return publicado, lect, union


def interpolar_vistas(puntos, edad):
    """Vistas a una edad exacta, interpolando en escala logarítmica entre las dos lecturas que la rodean.
    puntos = [(edad en horas, vistas)]. Devuelve (vistas, "interpolada") o (None, None) si no hay lecturas a los dos lados."""
    puntos = sorted((e, v) for e, v in puntos if v is not None and e >= 0)
    antes = [p for p in puntos if p[0] <= edad]
    despues = [p for p in puntos if p[0] >= edad]
    if not antes or not despues:
        return None, None
    (e0, v0), (e1, v1) = antes[-1], despues[0]
    if e1 == e0:
        return v0, "exacta"
    if e1 - e0 > 36:
        return None, None  # lecturas demasiado separadas: sería inventar
    f = (edad - e0) / (e1 - e0)
    if v0 > 0 and v1 > 0:
        return round(math.exp(math.log(v0) + f * (math.log(v1) - math.log(v0)))), "interpolada"
    return round(v0 + f * (v1 - v0)), "interpolada"


def medir(publicado, lect):
    """Para cada vídeo, red y edad, la medición que le corresponde (o nada si aún no toca)."""
    res = {}
    for (red, vid), lista in lect.items():
        pub = publicado.get((red, vid))
        if pub is None:
            continue
        con_edad = sorted(((_horas(pub, l["t"]), l) for l in lista), key=lambda x: x[0])
        series = {k: [(e, l.get(k)) for e, l in con_edad if l.get(k) is not None] for k in CUENTAS}
        # las vistas redondeadas de Studio también sirven de punto intermedio (la foto diaria es una al día)
        series["vistas"] += [(e, l["vistas_studio"]) for e, l in con_edad
                             if l.get("vistas_studio") is not None and l.get("origen") == "studio"]
        for edad in EDADES:
            m = {}
            for k in CUENTAS:
                v, modo = interpolar_vistas(series[k], edad)
                if v is not None:
                    m[k] = v
                    if k == "vistas":
                        m["vistas_modo"] = modo
            # porcentajes y tiempos: la primera lectura hecha entre la edad y la edad + margen
            for e, l in con_edad:
                if not (edad <= e <= edad + MARGEN[edad]):
                    continue
                for k, valor in l.items():
                    if k in ("t", "origen", "hora_exacta") or valor is None or k in m:
                        continue
                    m[k] = valor
                    m.setdefault("edad_h", {})[k] = round(e, 1)
            if m:
                res.setdefault((red, vid), {})[str(edad)] = m
    return res


def ultima(publicado, lect):
    """La lectura más reciente de cada métrica, con su edad: para ver los vídeos que aún no llegan a 48 h."""
    res = {}
    for (red, vid), lista in lect.items():
        pub = publicado.get((red, vid))
        if pub is None:
            continue
        m = {}
        for l in sorted(lista, key=lambda x: x["t"]):
            e = round(_horas(pub, l["t"]), 1)
            for k, valor in l.items():
                if k in ("t", "origen", "hora_exacta") or valor is None:
                    continue
                m[k] = valor
                m.setdefault("edad_h", {})[k] = e
        res[(red, vid)] = m
    return res


def construir(guardado=None, data=None, studio=None, tiktok_studio=None):
    """Mediciones nuevas + las ya guardadas. Lo guardado manda: una medición no se reescribe."""
    data = data if data is not None else _json(os.path.join("datos", "data.json"))
    studio = studio if studio is not None else _json("studio.json")
    tiktok_studio = tiktok_studio if tiktok_studio is not None else _json("tiktok_studio.json")
    publicado, lect, union = lecturas(data, studio, tiktok_studio)
    nuevas, ultimas = medir(publicado, lect), ultima(publicado, lect)
    salida = json.loads(json.dumps((guardado or {}).get("videos") or {}))
    claves = set(k for k in nuevas) | set(k for k in ultimas)
    for red, vid in sorted(claves):
        clave = union.get(vid, vid) if red == "tiktok" else vid
        entrada = salida.setdefault(clave, {})
        bloque = entrada.setdefault(red, {})
        bloque["id"] = vid
        pub = publicado.get((red, vid))
        if pub:
            bloque["publicado"] = pub.isoformat(timespec="minutes")
        for edad, m in (nuevas.get((red, vid)) or {}).items():
            previa = bloque.get(edad) or {}
            for k, valor in m.items():
                if k == "edad_h":
                    previa.setdefault("edad_h", {})
                    for kk, ee in valor.items():
                        previa["edad_h"].setdefault(kk, ee)
                elif k == "vistas_modo":
                    continue
                elif k not in previa:
                    previa[k] = valor
                    if k == "vistas":
                        previa["vistas_modo"] = m.get("vistas_modo")
            bloque[edad] = previa
        if (red, vid) in ultimas:
            bloque["ultima"] = ultimas[(red, vid)]
    return {"generado": dt.datetime.now(MADRID).isoformat(timespec="minutes"),
            "edades_h": list(EDADES), "videos": salida}


def cargar():
    if not os.path.exists(SALIDA):
        return {}
    return json.load(open(SALIDA, encoding="utf-8"))


def actualizar():
    m = construir(cargar())
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return m


def valor(mediciones, clave, red, metrica, edad=48, provisional=True, edad_minima=24):
    """Valor de una métrica a una edad. Si aún no existe y provisional=True, devuelve la última lectura
    siempre que el vídeo tenga al menos `edad_minima` horas en esa lectura. Devuelve (valor, edad real en horas, es_provisional)."""
    bloque = ((mediciones.get("videos") or {}).get(clave) or {}).get(red) or {}
    m = bloque.get(str(edad)) or {}
    if m.get(metrica) is not None:
        return m[metrica], (m.get("edad_h") or {}).get(metrica, edad), False
    if provisional:
        for menor in sorted((e for e in EDADES if e < edad), reverse=True):   # antes la medición fija anterior
            mm = bloque.get(str(menor)) or {}
            if mm.get(metrica) is not None:
                return mm[metrica], (mm.get("edad_h") or {}).get(metrica, menor), True
        u = bloque.get("ultima") or {}
        e = (u.get("edad_h") or {}).get(metrica)
        if u.get(metrica) is not None and e is not None and edad_minima <= e < edad:
            return u[metrica], e, True
    return None, None, False
