"""Informe semanal: lo publicado en la semana, cómo fue, cómo van los experimentos y qué se propone.

Se genera los lunes (o cuando se pida) en datos/informe-semanal-<lunes>.md. Las propuestas las decide
una persona: el informe no cambia DECISIONS.md.
"""
import datetime as dt
import json
import os

import analisis as A
import autopsia as U
import comentarios as C
import estadistica as E
import experimento as X
import ficha as F
import mediciones as M
import tabla as T

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTADISTICAS = os.path.dirname(AQUI)


def semana_de(dia):
    lunes = dia - dt.timedelta(days=dia.weekday())
    return lunes, lunes + dt.timedelta(days=6)


def propuestas(r, autos, experimentos, fichas):
    """Hasta 3 propuestas, de la más urgente a la menos. Cada una dice de dónde sale."""
    P = []
    mu = r["muestra"]
    sin_ficha = mu["videos"] - mu["con_ficha"]
    if sin_ficha:
        P.append(f"Rellenar la ficha de los {sin_ficha} vídeos que no la tienen: sin ficha no entran en el estudio.")
    abiertos = [e for e in experimentos.values() if e["estado"] == "abierto"]
    if not abiertos:
        pistas = [c for c in r["categoricas"] if min(c["n"], c["n_resto"]) >= 2]
        if pistas:
            c = max(pistas, key=lambda c: abs(c["diferencia"] or 0))
            P.append(f"Abrir un experimento sobre `{c['variable']}` (hoy la mayor diferencia: {A.texto_valor(c['valor'])} "
                     f"frente al resto, {A.n1(c['diferencia'])} en {T.METRICAS[c['metrica']][2]}, nivel {c['nivel']}). "
                     "No hay ninguno abierto.")
        else:
            P.append("Abrir el primer experimento con ficha previa (`python3 estadisticas/estudio experimento nuevo …`): "
                     "no hay ninguno abierto y sin experimento nada pasa de «pista».")
    if r["sin_variacion"]:
        v = ", ".join(f"`{x}`" for x, _ in r["sin_variacion"])
        P.append(f"Variables que no han variado nunca ({v}): no sabemos si importan. Si alguna interesa, hay que probarla a propósito.")
    diag = {}
    for a in autos:
        diag[a["diagnostico"]] = diag.get(a["diagnostico"], 0) + 1
    con = sum(v for k, v in diag.items() if k != "sin datos")
    for d in ("primer segundo", "ritmo", "tema"):
        if con >= 4 and diag.get(d, 0) / con >= 0.4:
            P.append(f"El diagnóstico más repetido es «{d}» ({diag[d]} de {con} autopsias): conviene atacarlo antes que nada.")
    if mu["fichas_previas"] == 0 and mu["con_ficha"]:
        P.append("Todas las fichas son retrospectivas: desde el próximo lote, rellenarlas antes de publicar (AGENTE).")
    return P[:3]


def ejecutar(dia=None, escribir=True, fichas=None, mediciones=None, data=None):
    dia = dia or dt.date.today()
    lunes, domingo = semana_de(dia - dt.timedelta(days=7))   # la semana anterior completa
    fichas = F.cargar() if fichas is None else fichas
    mediciones = M.cargar() if mediciones is None else mediciones
    r = A.ejecutar(escribir=False, fichas=fichas, mediciones=mediciones, data=data)
    autos = U.ejecutar(escribir=False, fichas=fichas, mediciones=mediciones, data=data)
    experimentos = X.cargar_todos()
    de_la_semana = [f for f in r["filas"] if f.get("publicado") and lunes.isoformat() <= f["publicado"][:10] <= domingo.isoformat()]
    por_id = {a["id"]: a for a in autos}

    L = [f"# Informe semanal — {lunes.isoformat()} a {domingo.isoformat()}", "",
         "Generado por `python3 estadisticas/estudio informe`. Detalle completo en `datos/estudio.md` y `datos/autopsias.md`.", "",
         "## Vídeos de la semana", ""]
    if de_la_semana:
        L += ["| Vídeo | Se quedan (YT) | s por vista (YT) | Vistas YT a 48 h | Diagnóstico |", "|---|---|---|---|---|"]
        for f in de_la_semana:
            def c(m, vistas=False):
                x = f["metricas"][m]
                if x["valor"] is None:
                    return "—"
                i = E.indice_relativo(x["valor"], r["referencias"].get(m))
                return f"{'~' if x['provisional'] else ''}{A.n0(x['valor']) if vistas else A.n1(x['valor'])} ({A.n1(i, 2)})"
            L.append(f"| {f['titulo']} | {c('yt_se_quedan')} | {c('yt_seg_por_vista')} | {c('yt_vistas', True)} | {por_id[f['id']]['diagnostico']} |")
        L += ["", "_Entre paréntesis, el índice frente a la mediana del canal. ~ = aún sin la medición de 48 h._", ""]
        medidos = [f for f in de_la_semana if f["metricas"]["yt_se_quedan"]["valor"] is not None]
        if medidos:
            mejor = max(medidos, key=lambda f: f["metricas"]["yt_se_quedan"]["valor"])
            peor = min(medidos, key=lambda f: f["metricas"]["yt_se_quedan"]["valor"])
            L += [f"- Mejor gancho: **{mejor['titulo']}** ({A.n1(mejor['metricas']['yt_se_quedan']['valor'])} %).",
                  f"- Peor gancho: **{peor['titulo']}** ({A.n1(peor['metricas']['yt_se_quedan']['valor'])} %).", ""]
    else:
        L += ["Ningún vídeo publicado en esa semana.", ""]

    L += ["## Experimentos", ""]
    if experimentos:
        for exp in experimentos.values():
            e = exp.get("resultado") if exp["estado"] == "cerrado" else X.estado(exp, r["filas"], dia)
            L.append(X.a_markdown(exp, e))
    else:
        L += ["Ninguno con ficha previa todavía.", ""]

    mu = r["muestra"]
    reglas = [c for c in r["categoricas"] if c["nivel"] == "regla"]
    indicios = [c for c in r["categoricas"] if c["nivel"] == "indicio"] + [c for c in r["numericas"] if c["nivel"] == "indicio"]
    L += ["## Qué sabemos ya", "",
          f"- Vídeos con lectura comparable: {mu['con_gancho_yt']} de {mu['videos']}.",
          f"- Reglas: {len(reglas)} · indicios: {len(indicios)} · el resto, pistas.", ""]
    for c in reglas + [c for c in indicios if "valor" in c]:
        L.append(f"- **{c['nivel']}**: `{c['variable']}` = {A.texto_valor(c['valor'])} → {A.n1(c['diferencia'])} en {T.METRICAS[c['metrica']][2]} "
                 f"({c['n']} frente a {c['n_resto']} vídeos).")
    if reglas or indicios:
        L.append("")

    a = r["audiencia"]
    if a:
        o = a.get("objetivo") or {}
        mayor = max(a["edad"].items(), key=lambda kv: kv[1]) if a["edad"] else None
        L += ["## Audiencia (YouTube)", "",
              f"- Hombres {A.n1(a['genero'].get('male'))} % · España {A.n1(a['espana'])} % · Latinoamérica {A.n1(a['latam'])} %."
              + (f" Tramo de edad más frecuente: {A.EDADES.get(mayor[0], mayor[0])} ({A.n1(mayor[1])} %)." if mayor else "")]
        if o:
            L.append(f"- Dentro del público objetivo ({o['estado']}): {A.n1(o['dentro_edad'])} % por edad, {A.n1(o['dentro_pais'])} % por país.")
        L.append("")

    titulos = {f["id"]: f["titulo"] for f in r["filas"]}
    L += [C.a_markdown(titulos=titulos)]

    L += ["## Propuestas para esta semana", ""]
    props = propuestas(r, autos, experimentos, fichas)
    L += [f"{i}. {p}" for i, p in enumerate(props, 1)] or ["Ninguna."]
    L += ["", "_Las decide una persona. Lo que se apruebe se apunta en `DECISIONS.md` con fecha, quién y motivo._", ""]
    texto = "\n".join(L)
    salida = os.path.join(ESTADISTICAS, "datos", f"informe-semanal-{lunes.isoformat()}.md")
    if escribir:
        with open(salida, "w", encoding="utf-8") as f:
            f.write(texto)
    return texto, salida
