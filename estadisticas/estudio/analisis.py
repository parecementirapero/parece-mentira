"""El estudio: qué rasgos del vídeo acompañan a mejores resultados, con qué nivel de evidencia, y quién nos ve.

Lee fichas.json + datos/mediciones.json + datos/data.json y escribe datos/estudio.md y datos/estudio.json.
No sustituye a analizar.py (las conclusiones diarias de la web): es la capa de rigor que dice cuánto
se puede confiar en cada cosa.
"""
import datetime as dt
import json
import os

import estadistica as E
import ficha as F
import mediciones as M
import tabla as T

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTADISTICAS = os.path.dirname(AQUI)
OBJETIVO = os.path.join(AQUI, "objetivo.json")
SALIDA_MD = os.path.join(ESTADISTICAS, "datos", "estudio.md")
SALIDA_JSON = os.path.join(ESTADISTICAS, "datos", "estudio.json")

LATAM = {"MX", "AR", "CO", "CL", "PE", "VE", "EC", "BO", "GT", "UY", "PY", "DO", "CR", "PA", "HN", "SV", "NI", "CU", "PR"}
PAISES = {"ES": "España", "MX": "México", "AR": "Argentina", "CO": "Colombia", "CL": "Chile", "PE": "Perú",
          "VE": "Venezuela", "US": "Estados Unidos", "EC": "Ecuador", "BO": "Bolivia", "GT": "Guatemala",
          "UY": "Uruguay", "PY": "Paraguay", "DO": "República Dominicana", "CR": "Costa Rica", "PA": "Panamá"}
EDADES = {"age13-17": "13–17", "age18-24": "18–24", "age25-34": "25–34", "age35-44": "35–44",
          "age45-54": "45–54", "age55-64": "55–64", "age65-": "65+"}
CATEGORICAS = [k for k, v in F.VARIABLES.items() if v[0] in (F.CAT, F.BOOL) and k not in ("experimento", "brazo")] + ["turno", "dia_semana"]
NUMERICAS = [k for k, v in F.VARIABLES.items() if v[0] == F.NUM] + ["hora"]


def n1(x, dec=1):
    if x is None:
        return "—"
    return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def n0(x):
    return "—" if x is None else f"{round(x):,}".replace(",", ".")


def texto_valor(v):
    if v is True:
        return "sí"
    if v is False:
        return "no"
    return str(v)


# ------------------------------------------------------------------ muestra y potencia
def muestra(filas):
    def con(m):
        return [f for f in filas if f["metricas"][m]["valor"] is not None]
    return {
        "videos": len(filas),
        "con_ficha": sum(1 for f in filas if f["ficha"]),
        "fichas_previas": sum(1 for f in filas if f["variables"].get("momento") == "previo"),
        "con_gancho_yt": len(con("yt_se_quedan")),
        "definitivas_yt": sum(1 for f in con("yt_se_quedan") if not f["metricas"]["yt_se_quedan"]["provisional"]),
        "con_retencion_tt": len(con("tt_medio_s")),
    }


def potencia(filas, metrica="yt_se_quedan"):
    xs = E.limpio(T.columna(filas, metrica))
    desv = E.desviacion(xs)
    res = {"metrica": metrica, "n": len(xs), "desviacion": desv, "tabla": []}
    if desv:
        for dif in (20, 15, 10, 5):
            res["tabla"].append({"diferencia": dif, "por_grupo": E.tamano_muestra(desv, dif)})
    return res


# ------------------------------------------------------------------ variables categóricas
def _semana(fila):
    try:
        return dt.datetime.fromisoformat(fila["publicado"]).isocalendar()[:2]
    except (KeyError, ValueError):
        return None


def _replicado(filas, variable, valor, metrica):
    """¿El mismo sentido en al menos dos semanas distintas, con 3 o más vídeos por grupo en cada una?"""
    signos = []
    for semana in sorted({_semana(f) for f in filas} - {None}):
        sub = [f for f in filas if _semana(f) == semana]
        a = [f["metricas"][metrica]["valor"] for f in sub if f["variables"].get(variable) == valor]
        b = [f["metricas"][metrica]["valor"] for f in sub if f["variables"].get(variable) not in (None, valor)]
        a, b = E.limpio(a), E.limpio(b)
        if len(a) >= 3 and len(b) >= 3:
            d = E.diferencia_medianas(a, b)
            if d:
                signos.append(d > 0)
    return len(signos) >= 2 and len(set(signos)) == 1


def _grupos(filas, variable, valor, metrica):
    col = T.columna(filas, metrica)
    a = [x for f, x in zip(filas, col) if f["variables"].get(variable) == valor]
    b = [x for f, x in zip(filas, col) if f["variables"].get(variable) not in (None, valor)]
    return E.limpio(a), E.limpio(b)


def comparar(filas, variable, valor, metrica):
    """Vídeos con variable = valor frente al resto, en una métrica."""
    a, b = _grupos(filas, variable, valor, metrica)
    res = {"variable": variable, "valor": valor, "metrica": metrica, "n": len(a), "n_resto": len(b),
           "mediana": E.mediana(a), "mediana_resto": E.mediana(b), "diferencia": E.diferencia_medianas(a, b)}
    ic = E.bootstrap_diferencia(a, b)
    res["intervalo"] = [ic[1], ic[2]] if ic else None
    res["p"] = E.permutacion(a, b)
    res["p_minimo"] = E.p_minimo_posible(len(a), len(b)) if a and b else None
    pareja = T.PAREJA.get(metrica)
    coincide = None
    if pareja and res["diferencia"]:
        a2, b2 = _grupos(filas, variable, valor, pareja)
        d2 = E.diferencia_medianas(a2, b2)
        if d2:
            coincide = (d2 > 0) == (res["diferencia"] > 0)
            res["diferencia_otra_red"] = d2
    res["redes_coinciden"] = coincide
    res["replicado"] = _replicado(filas, variable, valor, metrica)
    res["_ic"] = ic
    return res


def categoricas(filas, metricas=("yt_se_quedan", "yt_seg_por_vista")):
    res = []
    for var in CATEGORICAS:
        valores = sorted({f["variables"].get(var) for f in filas} - {None}, key=texto_valor)
        if len(valores) < 2:
            continue
        for m in metricas:
            for v in valores:
                if isinstance(v, bool) and v is False:
                    continue  # sí/no: basta con comparar «sí» frente al resto
                c = comparar(filas, var, v, m)
                if c["n"] and c["n_resto"]:
                    res.append(c)
    # el nivel se pone al final: depende de cuántas comparaciones se han mirado a la vez
    probadas = sum(1 for c in res if c["p"] is not None)
    for c in res:
        c["comparaciones"] = probadas
        c["nivel"] = E.nivel_evidencia(c["n"], c["n_resto"], c.pop("_ic"), c["redes_coinciden"], c["replicado"],
                                       c["p"], probadas)
    return res


def sin_variacion(filas):
    """Variables que valen lo mismo en todos los vídeos: no se puede saber nada de ellas hasta que varíen."""
    res = []
    for var in CATEGORICAS + NUMERICAS:
        valores = {f["variables"].get(var) for f in filas if f["ficha"]} - {None}
        if len(valores) == 1:
            res.append((var, texto_valor(next(iter(valores)))))
    return res


def confundidas(filas):
    """Parejas de variables que en esta muestra van siempre juntas: sus efectos no se pueden separar."""
    con = [f for f in filas if f["ficha"]]
    res = []
    for i, a in enumerate(CATEGORICAS):
        for b in CATEGORICAS[i + 1:]:
            pares = [(f["variables"].get(a), f["variables"].get(b)) for f in con]
            pares = [p for p in pares if p[0] is not None and p[1] is not None]
            va, vb = {p[0] for p in pares}, {p[1] for p in pares}
            if len(pares) < 4 or len(va) < 2 or len(vb) < 2:
                continue
            a_a_b = all(len({q[1] for q in pares if q[0] == x}) == 1 for x in va)
            b_a_a = all(len({q[0] for q in pares if q[1] == x}) == 1 for x in vb)
            if a_a_b and b_a_a:
                res.append((a, b))
    return res


# ------------------------------------------------------------------ variables numéricas
def numericas(filas, metricas=("yt_se_quedan", "yt_seg_por_vista")):
    res = []
    for var in NUMERICAS:
        x = [f["variables"].get(var) for f in filas]
        if len({v for v in x if v is not None}) < 3:
            continue
        for m in metricas:
            s = E.spearman(x, T.columna(filas, m))
            if not s:
                continue
            rho, p, n = s
            coincide = None
            s2 = E.spearman(x, T.columna(filas, T.PAREJA[m])) if m in T.PAREJA else None
            if s2 and rho:
                coincide = (s2[0] > 0) == (rho > 0)
            res.append({"variable": var, "metrica": m, "rho": rho, "p": p, "n": n, "redes_coinciden": coincide,
                        "nivel": E.nivel_correlacion(n, p, coincide)})
    return res


# ------------------------------------------------------------------ audiencia
def audiencia(data, objetivo=None):
    """Retrato de la audiencia de YouTube (canal) y distancia al público objetivo."""
    extra = (data or {}).get("youtubeExtra") or {}
    edad_genero = extra.get("edadGenero") or []
    paises = extra.get("paises") or []
    if not edad_genero and not paises:
        return None
    por_edad, por_genero = {}, {}
    for edad, genero, pct in edad_genero:
        por_edad[edad] = por_edad.get(edad, 0) + pct
        por_genero[genero] = por_genero.get(genero, 0) + pct
    total_paises = sum(p[1] for p in paises) or 0
    por_pais = {p[0]: p[1] / total_paises * 100 for p in paises} if total_paises else {}
    seg_por_vista = {p[0]: p[2] * 60 / p[1] for p in paises if p[1]}
    res = {
        "desde": extra.get("desde"), "edad": por_edad, "genero": por_genero, "paises": por_pais,
        "seg_por_vista_pais": seg_por_vista, "vistas_con_pais": total_paises,
        "latam": sum(v for k, v in por_pais.items() if k in LATAM), "espana": por_pais.get("ES", 0),
        "suscritos": extra.get("suscritos"), "edad_genero": edad_genero,
    }
    if objetivo:
        res["objetivo"] = {
            "estado": objetivo.get("estado"),
            "edades": objetivo.get("edades"), "paises": objetivo.get("paises"),
            "dentro_edad": sum(v for k, v in por_edad.items() if k in (objetivo.get("edades") or [])),
            "dentro_pais": sum(v for k, v in por_pais.items() if k in (objetivo.get("paises") or [])),
        }
    return res


def audiencia_por_grupo(data, filas, variable):
    """Composición de la audiencia por valor de una variable, sumando los vídeos de cada grupo.
    Necesita la audiencia por vídeo (data.json → videos[].audiencia), que YouTube solo da con volumen."""
    por_id = {v["id"]: v.get("audiencia") for v in (data or {}).get("videos") or [] if v.get("audiencia")}
    grupos = {}
    for f in filas:
        a, valor = por_id.get(f["id"]), f["variables"].get(variable)
        if not a or valor is None:
            continue
        peso = a.get("vistas") or 0
        g = grupos.setdefault(valor, {"videos": 0, "vistas": 0, "edad": {}, "genero": {}})
        g["videos"] += 1
        g["vistas"] += peso
        for edad, genero, pct in a.get("edadGenero") or []:
            g["edad"][edad] = g["edad"].get(edad, 0) + pct * peso
            g["genero"][genero] = g["genero"].get(genero, 0) + pct * peso
    for g in grupos.values():
        for d in (g["edad"], g["genero"]):
            for k in d:
                d[k] = d[k] / g["vistas"] if g["vistas"] else None
    return grupos


# ------------------------------------------------------------------ informe
def _linea_comparacion(c):
    m = T.METRICAS[c["metrica"]]
    signo = "+" if (c["diferencia"] or 0) >= 0 else "−"
    ic = f"{n1(c['intervalo'][0])} a {n1(c['intervalo'][1])}" if c["intervalo"] else "no calculable (menos de 3 por grupo)"
    otra = {True: "sí", False: "no", None: "sin datos"}[c["redes_coinciden"]]
    p = "—" if c["p"] is None else n1(c["p"], 2)
    return (f"| `{c['variable']}` = {texto_valor(c['valor'])} | {m[2]} | {c['n']} / {c['n_resto']} | "
            f"{n1(c['mediana'])} / {n1(c['mediana_resto'])} | {signo}{n1(abs(c['diferencia'] or 0))} | {ic} | {p} | {otra} | **{c['nivel']}** |")


def a_markdown(r):
    mu, po = r["muestra"], r["potencia"]
    L = [f"# Estudio de audiencia y rendimiento — {r['generado'][:16].replace('T', ' ')}", "",
         "Generado por `python3 estadisticas/estudio todo`. Método: `estadisticas/estudio/README.md`. "
         "Niveles: **pista** (menos de 5 vídeos por grupo o indistinguible del azar: solo para decidir qué probar), "
         "**indicio** (5 o más por grupo, p < 0,10 y mismo sentido en YouTube y TikTok), **regla** (10 o más por grupo, "
         "intervalo que no cruza el cero, repetido en dos semanas y p corregido por el número de comparaciones; "
         "o un experimento con ficha previa cerrado a favor).", "",
         "## 1. Con qué contamos", "",
         f"- Vídeos públicos: **{mu['videos']}** · con ficha de variables: **{mu['con_ficha']}** "
         f"(codificadas antes de publicar: {mu['fichas_previas']}).",
         f"- Con «se quedaron viendo» leído a edad comparable (24 h o más): **{mu['con_gancho_yt']}** "
         f"(de ellos, ya con la medición de 48 h: {mu['definitivas_yt']}).",
         f"- Con retención de TikTok Studio a edad comparable: **{mu['con_retencion_tt']}**.", ""]
    if po["desviacion"]:
        L += [f"«Se quedaron viendo» varía con una desviación típica de **{n1(po['desviacion'])} puntos** "
              f"({po['n']} vídeos). Con esa variación, para detectar una diferencia hacen falta:", "",
              "| Diferencia | Vídeos por grupo |", "|---|---|"]
        L += [f"| {t['diferencia']} puntos | {t['por_grupo']} |" for t in po["tabla"]]
        L += ["", "_Aproximación normal, 80 % de potencia y 5 % de error; con tan pocos vídeos la desviación "
              "misma es incierta._", ""]
    else:
        L += ["Aún no hay 2 vídeos con lectura comparable: no se puede estimar la variación.", ""]

    L += ["## 2. Vídeos", "",
          "Valor a 48 h; si el vídeo aún no llega, la última lectura con 24 h o más (marcada con ~). "
          "Entre paréntesis, el índice frente a la mediana del canal (1,3 = 30 % mejor). "
          "Sin valor = todavía no hay lectura con 24 h.", "",
          "| Vídeo | Se quedan (YT) | s por vista (YT) | Tiempo medio (TT) | Siguen a 3 s (TT) | Vistas YT | Vistas TT |",
          "|---|---|---|---|---|---|---|"]
    ref = r["referencias"]
    for f in r["filas"]:
        celdas = []
        for m in ("yt_se_quedan", "yt_seg_por_vista", "tt_medio_s", "tt_sigue_3s", "yt_vistas", "tt_vistas"):
            x = f["metricas"][m]
            if x["valor"] is None:
                if x["ultima"] is not None and x["ultima_edad_h"] is not None:
                    num = n0(x["ultima"]) if m.endswith("vistas") else n1(x["ultima"])
                    celdas.append(f"_{num} a las {round(x['ultima_edad_h'])} h_")
                else:
                    celdas.append("—")
                continue
            indice = E.indice_relativo(x["valor"], ref.get(m))
            num = n0(x["valor"]) if m.endswith("vistas") else n1(x["valor"])
            celdas.append(f"{'~' if x['provisional'] else ''}{num}" + (f" ({n1(indice, 2)})" if indice else ""))
        L.append(f"| {f['titulo']} | " + " | ".join(celdas) + " |")
    L += ["", "_En cursiva: lecturas con menos de 24 h. No entran en ningún cálculo._", ""]

    L += ["## 3. Qué acompaña a mejores resultados", ""]
    comps = r["categoricas"]
    if comps:
        orden = {"regla": 0, "indicio": 1, "pista": 2, "sin datos": 3}
        comps = sorted(comps, key=lambda c: (orden[c["nivel"]], -abs(c["diferencia"] or 0)))
        fuertes = [c for c in comps if c["nivel"] in ("regla", "indicio")]
        total = len(comps)
        # con un solo vídeo en un grupo no hay comparación que enseñar; y en las variables de dos valores
        # «A frente al resto» y «B frente al resto» son la misma fila al revés
        vistos, utiles = set(), []
        for c in comps:
            espejo = (c["variable"], c["metrica"], c["n_resto"], c["n"])
            if min(c["n"], c["n_resto"]) < 2 or espejo in vistos:
                continue
            vistos.add((c["variable"], c["metrica"], c["n"], c["n_resto"]))
            utiles.append(c)
        comps = utiles
        if comps:
            L += ["Cada fila compara los vídeos que tienen ese valor con todos los demás. «p» es la probabilidad de ver "
                  "esa diferencia por puro azar; con grupos pequeños no puede bajar de cierto mínimo "
                  "(3 contra 3: 0,10), así que un p alto con pocos vídeos no significa «no hay efecto».", "",
                  "| Variable | Métrica | Vídeos (con / resto) | Mediana (con / resto) | Diferencia | Intervalo al 90 % | p | ¿Igual en la otra red? | Nivel |",
                  "|---|---|---|---|---|---|---|---|---|"]
        L += [_linea_comparacion(c) for c in (fuertes or comps)[:24]]
        if not comps:
            L += ["**Todavía no hay ninguna comparación con al menos 2 vídeos por grupo** a edad comparable. "
                  "No se enseñan las de un solo vídeo: serían anécdotas con forma de dato."]
        elif not fuertes:
            L += ["", "**Ninguna comparación pasa de «pista».** Las de arriba son las de mayor diferencia y sirven "
                  "solo para elegir qué experimento hacer."]
        L += ["", f"⚠ Se han mirado {total} comparaciones a la vez: por azar, alrededor de 1 de cada 20 parecerá "
              "«significativa». Por eso aquí una «regla» exige un p repartido entre todas ellas; un experimento con "
              "ficha previa (`estadisticas/experimentos/`) mira una sola y llega antes."]
    else:
        L += ["Todavía no hay dos grupos con lecturas comparables en ninguna variable."]
    L.append("")

    if r["numericas"]:
        L += ["### Variables numéricas", "",
              "| Variable | Métrica | Vídeos | Correlación (Spearman) | p | ¿Igual en la otra red? | Nivel |", "|---|---|---|---|---|---|---|"]
        for c in sorted(r["numericas"], key=lambda c: -abs(c["rho"])):
            otra = {True: "sí", False: "no", None: "sin datos"}[c["redes_coinciden"]]
            L.append(f"| `{c['variable']}` | {T.METRICAS[c['metrica']][2]} | {c['n']} | {n1(c['rho'], 2)} | {n1(c['p'], 2)} | {otra} | **{c['nivel']}** |")
        L += ["", "_Una correlación no dice qué causa qué. Sin experimento, nunca pasa de «indicio»._", ""]

    L += ["## 4. Lo que esta muestra NO puede decir", ""]
    if r["sin_variacion"]:
        L.append("- **Variables que no varían** (todos los vídeos valen lo mismo, así que no se puede saber si importan): "
                 + ", ".join(f"`{v}` = {x}" for v, x in r["sin_variacion"]) + ".")
    if r["confundidas"]:
        L.append("- **Variables pegadas** (en estos vídeos van siempre juntas; un efecto de una puede ser de la otra): "
                 + "; ".join(f"`{a}` y `{b}`" for a, b in r["confundidas"]) + ".")
    if mu["fichas_previas"] < mu["con_ficha"]:
        L.append(f"- **{mu['con_ficha'] - mu['fichas_previas']} fichas se codificaron después de publicar**, sabiendo ya "
                 "el resultado. Las variables subjetivas de esas fichas pueden estar contaminadas.")
    L.append("- Retención por edad o por género: ninguna plataforma la da.")
    L.append("")

    a = r["audiencia"]
    L += ["## 5. Quién nos ve (YouTube, canal)", ""]
    if not a:
        L += ["Sin datos de audiencia todavía.", ""]
    else:
        L += [f"Desde {a['desde']}. Solo usuarios con sesión iniciada; edad y género los estima YouTube.", "",
              "| Edad | % | Mujeres | Hombres |", "|---|---|---|---|"]
        for clave, nombre in EDADES.items():
            if clave in a["edad"]:
                muj = sum(p for e, g, p in a["edad_genero"] if e == clave and g == "female")
                hom = sum(p for e, g, p in a["edad_genero"] if e == clave and g == "male")
                L.append(f"| {nombre} | {n1(a['edad'][clave])} | {n1(muj)} | {n1(hom)} |")
        L += ["", f"- Hombres {n1(a['genero'].get('male'))} % · mujeres {n1(a['genero'].get('female'))} %.",
              f"- España {n1(a['espana'])} % · Latinoamérica {n1(a['latam'])} % de las {n0(a['vistas_con_pais'])} vistas con país.",
              "- Por país (% de vistas · segundos por vista): "
              + " · ".join(f"{PAISES.get(k, k)} {n1(v)} % · {n1(a['seg_por_vista_pais'].get(k))} s"
                           for k, v in sorted(a["paises"].items(), key=lambda kv: -kv[1])[:8]) + "."]
        o = a.get("objetivo")
        if o:
            L += ["", f"**Público objetivo ({o['estado']})**: edades {', '.join(EDADES.get(e, e) for e in o['edades'])}; "
                  f"países {', '.join(PAISES.get(p, p) for p in o['paises'])}.",
                  f"- Hoy el **{n1(o['dentro_edad'])} %** de la audiencia está en esas edades y el "
                  f"**{n1(o['dentro_pais'])} %** de las vistas viene de esos países."]
        L.append("")
        grupos = r.get("audiencia_por_tema") or {}
        if grupos:
            L += ["### Público por tema", "", "| Tema | Vídeos | Vistas | 18–34 | 35+ | Hombres |", "|---|---|---|---|---|---|"]
            for tema, g in sorted(grupos.items(), key=lambda kv: -kv[1]["vistas"]):
                joven = sum(v or 0 for k, v in g["edad"].items() if k in ("age18-24", "age25-34"))
                mayor = sum(v or 0 for k, v in g["edad"].items() if k in ("age35-44", "age45-54", "age55-64", "age65-"))
                L.append(f"| {tema} | {g['videos']} | {n0(g['vistas'])} | {n1(joven)} % | {n1(mayor)} % | {n1(g['genero'].get('male'))} % |")
            L.append("")
        else:
            L += ["_Público por tema: todavía no hay audiencia por vídeo (YouTube la da a partir de cierto volumen; "
                  "`recoger.py` la pide para cada vídeo con 48 h o más)._", ""]
    return "\n".join(L) + "\n"


def ejecutar(escribir=True, fichas=None, mediciones=None, data=None):
    fichas = F.cargar() if fichas is None else fichas
    mediciones = M.cargar() if mediciones is None else mediciones
    if data is None:
        ruta = os.path.join(ESTADISTICAS, "datos", "data.json")
        data = json.load(open(ruta, encoding="utf-8")) if os.path.exists(ruta) else {}
    objetivo = json.load(open(OBJETIVO, encoding="utf-8")) if os.path.exists(OBJETIVO) else None
    filas = T.construir(fichas, mediciones)
    filas.sort(key=lambda f: f.get("publicado") or "9999")
    r = {
        "generado": dt.datetime.now(M.MADRID).isoformat(timespec="minutes"),
        "muestra": muestra(filas), "potencia": potencia(filas),
        "referencias": {m: E.mediana([f["metricas"][m]["valor"] for f in filas]) for m in T.METRICAS},
        "filas": filas, "categoricas": categoricas(filas), "numericas": numericas(filas),
        "sin_variacion": sin_variacion(filas), "confundidas": confundidas(filas),
        "audiencia": audiencia(data, objetivo), "audiencia_por_tema": audiencia_por_grupo(data, filas, "tema"),
    }
    if escribir:
        os.makedirs(os.path.dirname(SALIDA_MD), exist_ok=True)
        with open(SALIDA_MD, "w", encoding="utf-8") as f:
            f.write(a_markdown(r))
        with open(SALIDA_JSON, "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False, indent=1)
            f.write("\n")
    return r
