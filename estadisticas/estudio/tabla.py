"""La tabla del estudio: una fila por vídeo con su ficha y sus mediciones a edad fija."""
import datetime as dt
import math

import ficha as F
import mediciones as M

# nombre -> (red, métrica en mediciones.json, texto, qué mide, unidad)
METRICAS = {
    "yt_se_quedan": ("youtube", "se_quedan", "se quedaron viendo (YouTube)", "gancho", "%"),
    "tt_sigue_3s": ("tiktok", "sigue_3s", "siguen en el segundo 3 (TikTok)", "gancho", "%"),
    "yt_seg_por_vista": ("youtube", "seg_por_vista", "segundos por vista (YouTube)", "retención", "s"),
    "tt_medio_s": ("tiktok", "medio_s", "tiempo medio (TikTok)", "retención", "s"),
    "tt_completo": ("tiktok", "completo_pct", "lo ven entero (TikTok)", "retención", "%"),
    "yt_pct_visto": ("youtube", "pct_visto", "% medio visto (YouTube)", "retención", "%"),
    "yt_vistas": ("youtube", "vistas", "vistas (YouTube)", "alcance", ""),
    "tt_vistas": ("tiktok", "vistas", "vistas (TikTok)", "alcance", ""),
}
# La métrica principal de cada pregunta y la que la confirma en la otra red
PRINCIPALES = [("yt_se_quedan", "tt_sigue_3s"), ("yt_seg_por_vista", "tt_medio_s")]
PAREJA = {"yt_se_quedan": "tt_sigue_3s", "yt_seg_por_vista": "tt_medio_s", "yt_vistas": "tt_vistas",
          "tt_sigue_3s": "yt_se_quedan", "tt_medio_s": "yt_seg_por_vista", "tt_vistas": "yt_vistas"}
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def construir(fichas=None, mediciones=None, edad=48, edad_minima=24):
    """Filas del estudio. Cada métrica lleva su valor, la edad real de la lectura y si es provisional
    (el vídeo aún no llega a `edad`, pero tiene una lectura con al menos `edad_minima` horas)."""
    fichas = F.cargar() if fichas is None else fichas
    mediciones = M.cargar() if mediciones is None else mediciones
    por_yt = {f.get("youtube"): (clave, f) for clave, f in fichas.items() if f.get("youtube")}
    filas = []
    videos = mediciones.get("videos") or {}
    for vid in sorted(set(videos) | set(por_yt)):
        clave_ficha, f = por_yt.get(vid, (None, {}))
        fila = {"id": vid, "ficha": clave_ficha, "titulo": f.get("titulo") or vid, "variables": dict(f), "metricas": {}}
        pub = ((videos.get(vid) or {}).get("youtube") or {}).get("publicado")
        if pub:
            t = dt.datetime.fromisoformat(pub)
            fila["publicado"] = pub
            fila["variables"]["hora"] = t.hour
            fila["variables"]["dia_semana"] = DIAS[t.weekday()]
            fila["variables"]["turno"] = "mañana" if t.hour < 14 else "tarde"
        for nombre, (red, metrica, *_r) in METRICAS.items():
            v, e, prov = M.valor(mediciones, vid, red, metrica, edad=edad, edad_minima=edad_minima)
            if v is not None and e is not None and e < edad_minima:
                v = None
            u = (((videos.get(vid) or {}).get(red) or {}).get("ultima") or {})
            fila["metricas"][nombre] = {"valor": v, "edad_h": e if v is not None else None, "provisional": prov,
                                        "ultima": u.get(metrica), "ultima_edad_h": (u.get("edad_h") or {}).get(metrica)}
        filas.append(fila)
    return filas


def columna(filas, metrica, logaritmo=None):
    """Valores de una métrica (None donde no hay). Las vistas van en logaritmo: 800 y 8.000 son «10 veces»."""
    logaritmo = metrica.endswith("vistas") if logaritmo is None else logaritmo
    res = []
    for f in filas:
        v = f["metricas"][metrica]["valor"]
        res.append(None if v is None else (math.log10(v) if logaritmo and v > 0 else (None if logaritmo else v)))
    return res
