"""Experimentos con ficha previa: la hipótesis, la métrica y el tamaño se escriben ANTES de publicar.

Cada experimento es un archivo en estadisticas/experimentos/<id>.json. Los vídeos se apuntan a él en su
ficha: "experimento": "<id>", "brazo": "A" (con el cambio) o "B" (sin él).

Diseño por bloques: cada día sale un vídeo de cada brazo, a ser posible del mismo tema, y se alterna
cuál sale primero para que la hora no se confunda con el cambio.
"""
import datetime as dt
import json
import math
import os

import estadistica as E
import ficha as F
import mediciones as M
import tabla as T

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTADISTICAS = os.path.dirname(AQUI)
CARPETA = os.path.join(ESTADISTICAS, "experimentos")
DESVIACION_POR_DEFECTO = {"yt_se_quedan": 16.0, "tt_sigue_3s": 12.0, "yt_seg_por_vista": 6.0, "tt_medio_s": 4.5}
MADURACION_DIAS = 2   # las mediciones valen a las 48 h


def ruta(ident):
    return os.path.join(CARPETA, f"{ident}.json")


def cargar_todos():
    res = {}
    if os.path.isdir(CARPETA):
        for n in sorted(os.listdir(CARPETA)):
            if n.endswith(".json"):
                res[n[:-5]] = json.load(open(os.path.join(CARPETA, n), encoding="utf-8"))
    return res


def desviacion_actual(metrica, filas=None):
    filas = T.construir() if filas is None else filas
    xs = E.limpio(T.columna(filas, metrica))
    d = E.desviacion(xs)
    if d and len(xs) >= 8:
        return d, f"medida en {len(xs)} vídeos"
    return DESVIACION_POR_DEFECTO.get(metrica, d), f"valor de partida (aún hay {len(xs)} vídeos con lectura comparable)"


def nuevo(ident, hipotesis, variable, metrica, diferencia, inicio=None, si_a_favor="", si_en_contra="",
          por_dia=1, filas=None, hoy=None, quien=None):
    """Crea la ficha previa. `diferencia` = la diferencia mínima que nos importaría (en unidades de la métrica)."""
    if metrica not in T.METRICAS:
        raise ValueError(f"métrica desconocida: {metrica}. Opciones: {', '.join(T.METRICAS)}")
    if os.path.exists(ruta(ident)):
        raise ValueError(f"ya existe {ruta(ident)}: una ficha previa no se reescribe")
    hoy = hoy or dt.date.today()
    inicio = dt.date.fromisoformat(inicio) if inicio else hoy + dt.timedelta(days=1)
    desv, origen = desviacion_actual(metrica, filas)
    por_brazo = E.tamano_muestra(desv, diferencia)
    dias = math.ceil(por_brazo / por_dia)
    exp = {
        "id": ident, "estado": "abierto", "creado": hoy.isoformat(), "creado_por": quien,
        "hipotesis": hipotesis, "variable": variable, "metrica": metrica,
        "diferencia_minima": diferencia, "desviacion_supuesta": round(desv, 1), "desviacion_origen": origen,
        "por_brazo": por_brazo, "inicio": inicio.isoformat(),
        "ultimo_video": (inicio + dt.timedelta(days=dias - 1)).isoformat(),
        "cierre": (inicio + dt.timedelta(days=dias - 1 + MADURACION_DIAS)).isoformat(),
        "si_a_favor": si_a_favor, "si_en_contra": si_en_contra,
        "reglas": ["Brazo A = con el cambio; brazo B = sin él. Todo lo demás, igual.",
                   "Cada día un vídeo de cada brazo, del mismo tema si se puede.",
                   "Días impares sale primero A; días pares, primero B.",
                   "Se cierra en la fecha de cierre, salga lo que salga. No se alarga «porque casi sale»."],
    }
    os.makedirs(CARPETA, exist_ok=True)
    with open(ruta(ident), "w", encoding="utf-8") as f:
        json.dump(exp, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return exp


def calendario(exp):
    """Qué brazo sale primero cada día."""
    ini, fin = dt.date.fromisoformat(exp["inicio"]), dt.date.fromisoformat(exp["ultimo_video"])
    dias, d, i = [], ini, 0
    while d <= fin:
        dias.append((d.isoformat(), "A, luego B" if i % 2 == 0 else "B, luego A"))
        d += dt.timedelta(days=1)
        i += 1
    return dias


def estado(exp, filas=None, hoy=None):
    """Cómo va un experimento con los vídeos apuntados hasta ahora."""
    filas = T.construir() if filas is None else filas
    hoy = hoy or dt.date.today()
    m = exp["metrica"]
    col = T.columna(filas, m)
    def brazo(letra, definitivos=True):
        return E.limpio([x for f, x in zip(filas, col)
                         if f["variables"].get("experimento") == exp["id"] and f["variables"].get("brazo") == letra
                         and not (definitivos and f["metricas"][m]["provisional"])])
    publicados = {l: sum(1 for f in filas if f["variables"].get("experimento") == exp["id"] and f["variables"].get("brazo") == l)
                  for l in ("A", "B")}
    a, b = brazo("A"), brazo("B")
    ic = E.bootstrap_diferencia(a, b)
    pareja = T.PAREJA.get(m)
    coincide = None
    if pareja:
        col2 = T.columna(filas, pareja)
        a2 = E.limpio([x for f, x in zip(filas, col2) if f["variables"].get("experimento") == exp["id"] and f["variables"].get("brazo") == "A"])
        b2 = E.limpio([x for f, x in zip(filas, col2) if f["variables"].get("experimento") == exp["id"] and f["variables"].get("brazo") == "B"])
        d1, d2 = E.diferencia_medianas(a, b), E.diferencia_medianas(a2, b2)
        if d1 and d2:
            coincide = (d1 > 0) == (d2 > 0)
    res = {"id": exp["id"], "publicados": publicados, "medidos": {"A": len(a), "B": len(b)},
           "mediana": {"A": E.mediana(a), "B": E.mediana(b)}, "diferencia": E.diferencia_medianas(a, b),
           "intervalo": [ic[1], ic[2]] if ic else None, "p": E.permutacion(a, b), "redes_coinciden": coincide,
           "dias_para_cierre": (dt.date.fromisoformat(exp["cierre"]) - hoy).days,
           "completo": min(len(a), len(b)) >= exp["por_brazo"]}
    # ¿se repite en las dos mitades del experimento? (primera y segunda mitad de los vídeos, por fecha)
    del_exp = sorted((f for f in filas if f["variables"].get("experimento") == exp["id"] and f["metricas"][m]["valor"] is not None
                      and not f["metricas"][m]["provisional"]), key=lambda f: f.get("publicado") or "")
    signos = []
    for mitad in (del_exp[:len(del_exp) // 2], del_exp[len(del_exp) // 2:]):
        ma = [f["metricas"][m]["valor"] for f in mitad if f["variables"].get("brazo") == "A"]
        mb = [f["metricas"][m]["valor"] for f in mitad if f["variables"].get("brazo") == "B"]
        d = E.diferencia_medianas(ma, mb) if len(ma) >= 3 and len(mb) >= 3 else None
        if d:
            signos.append(d > 0)
    res["replicado"] = len(signos) == 2 and signos[0] == signos[1]
    res["veredicto"] = veredicto(exp, res)
    return res


def veredicto(exp, e):
    """a favor / en contra / sin efecto relevante / no concluyente. Solo vale como definitivo al cierre."""
    ic, minima = e["intervalo"], exp["diferencia_minima"]
    if ic is None:
        return "no concluyente (menos de 3 vídeos medidos por brazo)"
    lo, hi = ic
    if lo > 0:
        return "a favor" if e["redes_coinciden"] is not False else "a favor en esta red, pero la otra dice lo contrario"
    if hi < 0:
        return "en contra (el cambio empeora)"
    if -minima < lo and hi < minima:
        return "sin efecto relevante (si lo hay, es menor que la diferencia mínima)"
    return "no concluyente"


def cerrar(ident, filas=None, hoy=None, forzar=False):
    exp = json.load(open(ruta(ident), encoding="utf-8"))
    hoy = hoy or dt.date.today()
    if exp["estado"] == "cerrado":
        raise ValueError(f"{ident} ya está cerrado")
    if hoy < dt.date.fromisoformat(exp["cierre"]) and not forzar:
        raise ValueError(f"{ident} cierra el {exp['cierre']}. Cerrar antes de tiempo al ver un resultado bonito es "
                         "la forma más fácil de engañarse; usa --forzar solo si se abandona.")
    e = estado(exp, filas, hoy)
    nivel = E.nivel_evidencia(e["medidos"]["A"], e["medidos"]["B"],
                              (e["diferencia"], *e["intervalo"]) if e["intervalo"] else None, e["redes_coinciden"],
                              e["replicado"], e["p"], 1)
    exp.update({"estado": "cerrado", "cerrado": hoy.isoformat(), "resultado": e, "nivel": nivel,
                "antes_de_tiempo": hoy < dt.date.fromisoformat(exp["cierre"])})
    with open(ruta(ident), "w", encoding="utf-8") as f:
        json.dump(exp, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return exp


def a_markdown(exp, e=None):
    from analisis import n1
    m = T.METRICAS[exp["metrica"]]
    L = [f"### {exp['id']} — {exp['hipotesis']}", "",
         f"- Variable: `{exp['variable']}` · métrica principal: {m[2]} · diferencia mínima que importa: {n1(exp['diferencia_minima'])} {m[4]}",
         f"- Vídeos por brazo: **{exp['por_brazo']}** (desviación {n1(exp['desviacion_supuesta'])}, {exp['desviacion_origen']})",
         f"- Del {exp['inicio']} al {exp['ultimo_video']}; **cierre el {exp['cierre']}**",
         f"- Si sale a favor: {exp['si_a_favor'] or '—'}", f"- Si sale en contra: {exp['si_en_contra'] or '—'}"]
    if e:
        ic = f"{n1(e['intervalo'][0])} a {n1(e['intervalo'][1])}" if e["intervalo"] else "—"
        L += [f"- Publicados A/B: {e['publicados']['A']}/{e['publicados']['B']} · medidos a 48 h: {e['medidos']['A']}/{e['medidos']['B']} de {exp['por_brazo']}",
              f"- Mediana A {n1(e['mediana']['A'])} · B {n1(e['mediana']['B'])} · diferencia {n1(e['diferencia'])} · intervalo al 90 %: {ic}",
              f"- Hoy: **{e['veredicto']}**" + ("" if exp["estado"] == "cerrado" else f" (provisional; faltan {max(e['dias_para_cierre'], 0)} días para el cierre)")]
    return "\n".join(L) + "\n"
