#!/usr/bin/env python3
"""Saca conclusiones de datos/data.json y escribe datos/aprendizajes.md.

Lo usan:
  - construir.py, que mete las conclusiones en la web (vista «Conclusiones»);
  - el agente de los lotes (AGENTE.md), que lee aprendizajes.md antes de elegir temas,
    ganchos, estructura, duración y hora.

Cada conclusión lleva su «fuerza» según cuántos vídeos la respaldan:
  pista      -> menos de 5 vídeos: solo sirve para decidir qué probar
  tendencia  -> 5 a 14 vídeos: se puede inclinar la balanza
  firme      -> 15 o más vídeos (y al menos 5 por grupo): se puede convertir en regla
Uso: python3 estadisticas/analizar.py [ruta/data.json]
"""
import datetime as dt
import json
import re
import os
import statistics as st
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REDES = {"youtube": "YouTube", "tiktok": "TikTok", "instagram": "Instagram"}
ETIQUETAS = {"tema": "tema", "gancho": "tipo de gancho", "estructura": "estructura",
             "turno": "turno de publicación", "duracionTramo": "duración", "voz": "voz"}
FUENTES_NOMBRE = {"Feed de Shorts": "el feed de Shorts"}


def fuerza(n, minimo_grupo=None):
    if n >= 15 and (minimo_grupo is None or minimo_grupo >= 5):
        return "firme"
    if n >= 5:
        return "tendencia"
    return "pista"


def media(xs):
    xs = [x for x in xs if x is not None]
    return st.mean(xs) if xs else None


def mediana(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else None


def n1(x):
    return f"{x:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


def n0(x):
    return f"{round(x):,}".replace(",", ".")


PAISES = {"ES": "España", "MX": "México", "AR": "Argentina", "CO": "Colombia", "CL": "Chile", "PE": "Perú", "VE": "Venezuela",
          "US": "Estados Unidos", "EC": "Ecuador", "BO": "Bolivia", "GT": "Guatemala", "UY": "Uruguay", "PY": "Paraguay",
          "DO": "República Dominicana", "CR": "Costa Rica", "PA": "Panamá", "HN": "Honduras", "SV": "El Salvador", "NI": "Nicaragua", "CU": "Cuba", "PR": "Puerto Rico"}


def corta(t, n=60):
    t = re.split(r"\s#|\sFuentes:", str(t or ""))[0].strip()
    return t if len(t) <= n else t[: n - 1] + "…"


def momento(v):
    try:
        return dt.datetime.fromisoformat(f"{v['fecha']}T{v.get('hora') or '00:00'}")
    except ValueError:
        return None


def turno(v):
    lote = (v.get("lote") or (v.get("etiquetas") or {}).get("lote") or "")
    if lote.endswith("-manana"):
        return "mañana (08:00)"
    if lote.endswith("-tarde"):
        return "tarde (20:00)"
    h = int((v.get("hora") or "12:00")[:2])
    return "mañana (08:00)" if h < 14 else "tarde (20:00)"


def tramo_duracion(s):
    if not s:
        return None
    return "menos de 40 s" if s < 40 else "40–50 s" if s < 50 else "50–60 s" if s <= 60 else "más de 60 s"


try:
    MANUALES = {k: v for k, v in json.load(open(os.path.join(AQUI, "etiquetas.json"), encoding="utf-8")).items() if not k.startswith("_")}
except (OSError, ValueError):
    MANUALES = {}


def preparar(d):
    """Une cada contenido con sus vídeos de cada red y sus etiquetas."""
    vids = {"youtube": d.get("videos") or [],
            "tiktok": (d.get("tiktok") or {}).get("videos") or [],
            "instagram": (d.get("instagram") or {}).get("videos") or []}
    clave = {"youtube": "id", "tiktok": "id", "instagram": "codigo"}
    por_id = {r: {v.get(clave[r]): v for v in vs} for r, vs in vids.items()}
    filas = []
    for c in d.get("contenidos") or [{"youtube": v["id"], "titulo": v["titulo"], "fecha": v["fecha"]} for v in vids["youtube"]]:
        f = {"titulo": c.get("titulo"), "fecha": c.get("fecha")}
        for r in REDES:
            f[r] = por_id[r].get(c.get(r)) if c.get(r) else None
        base = f["youtube"] or f["tiktok"] or f["instagram"] or {}
        et = dict(base.get("etiquetas") or {})
        et.update({k: v for k, v in (MANUALES.get(c.get("youtube")) or {}).items() if k not in ("tiktok", "instagram")})
        et.setdefault("turno", turno(base))
        et.setdefault("duracionTramo", tramo_duracion(base.get("duracion")))
        f["etiquetas"] = {k: v for k, v in et.items() if v}
        f["duracion"] = base.get("duracion")
        filas.append(f)
    return vids, filas


def vistas48(v):
    """Vistas de YouTube en los 2 primeros días (comparables entre vídeos de distinta edad)."""
    vd = v.get("vistasDia") or []
    if vd and (v.get("horasPublicado") or 0) >= 48:
        return sum(x[1] for x in vd[:2])
    return None


def analizar(d):
    hoy = d.get("generado", "")[:10]
    vids, filas = preparar(d)
    # vídeos que la red casi no enseñó (menos del 10 % de la mediana): se excluyen de las comparaciones por grupo
    raros = set()
    for r in REDES:
        med = mediana([v.get("vistas") for v in vids[r]])
        if med and len(vids[r]) >= 3:
            raros.update(id(v) for v in vids[r] if (v.get("vistas") or 0) < med * 0.1)
    conc, recos = [], []

    def add(area, texto, n, f=None, dato=None):
        conc.append({"area": area, "texto": texto, "n": n, "fuerza": f or fuerza(n), **({"dato": dato} if dato else {})})

    def reco(texto, n, f=None, motivo=""):
        recos.append({"texto": texto, "n": n, "fuerza": f or fuerza(n), "motivo": motivo})

    # ---------- 1. ranking por red ----------
    for r, nombre in REDES.items():
        vs = [v for v in vids[r] if v.get("vistas") is not None]
        if len(vs) < 2:
            continue
        vs.sort(key=lambda v: v["vistas"], reverse=True)
        top, med = vs[0], mediana([v["vistas"] for v in vs])
        texto = f"El más visto es «{corta(top.get('titulo'))}» con {n0(top['vistas'])} vistas"
        if med:
            texto += f", {n1(top['vistas'] / med)} veces la mediana del canal ({n0(med)})"
        add(nombre, texto + ".", len(vs))
        # vídeos que no arrancan (posible falta de empuje del algoritmo)
        flojos = [v for v in vs if med and v["vistas"] < med * 0.1 and (dt.datetime.fromisoformat(hoy) - dt.datetime.fromisoformat(v["fecha"])).days >= 0]
        for v in flojos:
            add(nombre, f"«{corta(v.get('titulo'))}» apenas tiene {n0(v['vistas'])} vistas frente a una mediana de {n0(med)}: "
                        f"{nombre} casi no lo ha enseñado. Revisa si se publicó pegado a otro vídeo, si tiene alguna restricción o si el gancho falla.", len(vs))

    # ---------- 2. ráfagas: vídeos publicados con pocos minutos de diferencia ----------
    for r, nombre in REDES.items():
        vs = [v for v in vids[r] if momento(v) and v.get("vistas") is not None]
        if len(vs) < 3:
            continue
        vs.sort(key=momento)
        rafaga = set()
        for a, b in zip(vs, vs[1:]):
            if (momento(b) - momento(a)).total_seconds() < 30 * 60:
                rafaga.update([id(a), id(b)])
        en = [v["vistas"] for v in vs if id(v) in rafaga]
        solos = [v["vistas"] for v in vs if id(v) not in rafaga]
        if en and solos:
            me, ms = mediana(en), mediana(solos)
            if ms and me < ms * 0.75:
                add(nombre, f"Los vídeos subidos con menos de 30 min entre uno y otro tienen una mediana de {n0(me)} vistas; "
                            f"los subidos solos, {n0(ms)}.", len(vs), dato={"rafaga": me, "solos": ms})
                if nombre in ("YouTube", "TikTok"):
                    reco(f"En {nombre}, separa las subidas del mismo lote (al menos 1–2 h entre vídeos) en vez de subir los 3 seguidos.",
                         len(vs), motivo=f"ráfaga {n0(me)} vs solos {n0(ms)} de mediana")

    # ---------- 3. comparar grupos por etiqueta ----------
    def comparar(etq, metrica, nombre_metrica, fmt, red="youtube", minimo=1):
        grupos = {}
        for f in filas:
            g = f["etiquetas"].get(etq)
            v = f.get(red)
            if not g or not v or id(v) in raros:
                continue
            x = metrica(v)
            if x is None:
                continue
            grupos.setdefault(g, []).append(x)
        grupos = {g: xs for g, xs in grupos.items() if len(xs) >= minimo}
        if len(grupos) < 2:
            return None
        orden = sorted(grupos.items(), key=lambda kv: media(kv[1]), reverse=True)
        n = sum(len(xs) for xs in grupos.values())
        mn = min(len(xs) for xs in grupos.values())
        (g1, x1), (g2, x2) = orden[0], orden[-1]
        partes = ", ".join(f"{g} {fmt(media(xs))} ({len(xs)})" for g, xs in orden)
        f_ = fuerza(n, mn)
        add(f"Por {ETIQUETAS.get(etq, etq)}", f"{nombre_metrica} en {REDES[red]}: {partes}. Gana «{g1}».", n, f_,
            dato={"grupos": {g: media(xs) for g, xs in orden}})
        return g1, g2, media(x1), media(x2), n, f_, mn

    hay48 = sum(1 for v in vids["youtube"] if vistas48(v) is not None) >= 4
    met_vistas = (vistas48, "Vistas medias en 2 días") if hay48 else (lambda v: v.get("vistas"), "Vistas medias")
    for etq in ETIQUETAS:
        r1 = comparar(etq, met_vistas[0], met_vistas[1], n0)
        comparar(etq, lambda v: v.get("pctVisto"), "% medio visto", lambda x: n1(x) + " %")
        comparar(etq, lambda v: v.get("vistas"), "Vistas medias", n0, red="tiktok")
        if r1 and r1[6] >= 2 and etq in ("tema", "gancho", "estructura") and r1[2] and r1[3] and r1[2] > r1[3] * 1.5:
            reco(f"Prioriza {ETIQUETAS[etq]} «{r1[0]}» y reduce «{r1[1]}» ({n1(r1[2] / r1[3])} veces más vistas).", r1[4], r1[5],
                 motivo="comparación por " + ETIQUETAS[etq])

    # ---------- 4. gancho y retención (YouTube) ----------
    yt = [v for v in vids["youtube"] if v.get("retencion3s") is not None]
    if yt:
        m3 = media([v["retencion3s"] for v in yt])
        add("Gancho", f"De media sigue viendo el {n1(m3)} % a los 3 segundos ({len(yt)} vídeos con datos).", len(yt))
        malo = min(yt, key=lambda v: v["retencion3s"])
        bueno = max(yt, key=lambda v: v["retencion3s"])
        if len(yt) >= 2 and bueno["retencion3s"] - malo["retencion3s"] >= 8:
            add("Gancho", f"Mejor gancho: «{corta(bueno['titulo'])}» ({n1(bueno['retencion3s'])} % a los 3 s). "
                          f"Peor: «{corta(malo['titulo'])}» ({n1(malo['retencion3s'])} %). Copia la forma de empezar del primero.", len(yt))
        if m3 < 70:
            reco("La primera frase y el primer plano tienen que enseñar el dato o la pregunta sin preámbulo: a los 3 s se va más de un 30 %.",
                 len(yt), motivo=f"retención a 3 s media {n1(m3)} %")
    pv = [v for v in vids["youtube"] if v.get("pctVisto") is not None and v.get("duracion")]
    if pv:
        mp = media([v["pctVisto"] for v in pv])
        add("Retención", f"% medio visto: {n1(mp)} % ({len(pv)} vídeos). En Shorts, por encima de 100 % significa que lo vuelven a ver.", len(pv))
        if len(pv) >= 5:
            try:
                c = st.correlation([v["duracion"] for v in pv], [v["pctVisto"] for v in pv])
                if abs(c) >= 0.4:
                    add("Retención", f"{'Cuanto más cortos, más % visto' if c < 0 else 'Los más largos retienen igual o mejor'} "
                                     f"(correlación {n1(c)} entre duración y % visto).", len(pv))
                    if c < 0:
                        reco("Acorta los guiones hacia la parte baja del rango (≈130–145 palabras).", len(pv), motivo=f"correlación {n1(c)}")
            except st.StatisticsError:
                pass
        # curva: dónde se cae la gente
        caidas = []
        for v in pv:
            cv = v.get("curva") or []
            if len(cv) > 10:
                saltos = [(cv[i][0], cv[i - 1][1] - cv[i][1]) for i in range(2, len(cv) - 2)]
                caidas.append(max(saltos, key=lambda x: x[1])[0])
        if len(caidas) >= 2:
            add("Retención", f"La mayor caída suele estar hacia el {round(media(caidas) * 100)} % del vídeo: revisa qué pasa en ese punto del guion.", len(caidas))

    # ---------- 5. comparación entre redes ----------
    pares = [(f, f["tiktok"]["vistas"], f["youtube"]["vistas"]) for f in filas
             if f.get("tiktok") and f.get("youtube") and f["tiktok"].get("vistas") is not None and f["youtube"].get("vistas")]
    if pares:
        gana_tt = [f for f, t, y in pares if t > y]
        add("Redes", f"TikTok supera a YouTube en {len(gana_tt)} de {len(pares)} vídeos publicados en las dos.", len(pares))
        for f, t, y in pares:
            if t > 5 * y:
                add("Redes", f"«{corta(f['titulo'])}»: {n0(t)} vistas en TikTok frente a {n0(y)} en YouTube. Funciona en TikTok, así que el vídeo vale; en YouTube no arrancó.", len(pares))
    for r, nombre in REDES.items():
        vs = [v for v in vids[r] if v.get("vistas")]
        if len(vs) >= 2:
            lk = sum(v.get("likes") or 0 for v in vs) / sum(v["vistas"] for v in vs) * 1000
            hay_sh = any(v.get("compartidos") is not None for v in vs)
            sh = sum(v.get("compartidos") or 0 for v in vs) / sum(v["vistas"] for v in vs) * 1000 if hay_sh else None
            add("Redes", f"{nombre}: {n1(lk)} likes" + (f" y {n1(sh)} compartidos" if hay_sh else "") + " por cada 1.000 vistas.", len(vs),
                dato={"likes1000": lk, "compartidos1000": sh})

    # ---------- 6. audiencia (YouTube) ----------
    x = d.get("youtubeExtra") or {}
    tot = sum(p[1] for p in x.get("paises") or []) or 0
    if x.get("paises") and tot:
        p = x["paises"]
        es = next((q[1] for q in p if q[0] == "ES"), 0)
        latam = sum(q[1] for q in p if q[0] not in ("ES", "US"))
        add("Audiencia", f"País nº 1: {PAISES.get(p[0][0], p[0][0])} ({round(p[0][1] / tot * 100)} %). España {round(es / tot * 100)} %, "
                         f"Latinoamérica {round(latam / tot * 100)} % de las vistas con país.", len(vids['youtube']))
        if latam > es:
            reco("Más de la mitad de la audiencia es de Latinoamérica: evita expresiones muy de España en el gancho y usa referencias que se entiendan en los dos lados (la voz puede seguir siendo de España).",
                 len(vids["youtube"]), motivo=f"Latinoamérica {round(latam / tot * 100)} % vs España {round(es / tot * 100)} %")
    if x.get("edadGenero"):
        g = {}
        for a, s_, pc in x["edadGenero"]:
            g[a] = g.get(a, 0) + pc
        top = max(g.items(), key=lambda kv: kv[1])
        hombres = sum(pc for a, s_, pc in x["edadGenero"] if s_ == "male")
        add("Audiencia", f"Edad más frecuente: {top[0].replace('age', '').replace('-', '–').rstrip('–')} años ({round(top[1])} %). Hombres {round(hombres)} %.", len(vids["youtube"]))
    if x.get("fuentes"):
        tf = sum(f[1] for f in x["fuentes"]) or 1
        f0 = x["fuentes"][0]
        add("Audiencia", f"El {round(f0[1] / tf * 100)} % de las vistas llega por {FUENTES_NOMBRE.get(f0[0], f0[0])}: "
                         f"el algoritmo decide casi todo; título y miniatura pesan poco, los 3 primeros segundos mucho.", len(vids["youtube"]))
    if x.get("suscritos"):
        sub = next((s for s in x["suscritos"] if s[0] == "SUBSCRIBED"), None)
        tv = sum(s[1] for s in x["suscritos"]) or 1
        if sub is not None:
            add("Audiencia", f"Los suscritos son el {n1(sub[1] / tv * 100)} % de las vistas: casi todo es público nuevo.", len(vids["youtube"]))

    # ---------- 7. evolución ----------
    dd = d.get("diario") or []
    if len(dd) >= 14:
        a, b = sum(x["vistas"] for x in dd[-7:]), sum(x["vistas"] for x in dd[-14:-7])
        if b:
            add("Evolución", f"Vistas del canal en YouTube: {n0(a)} en los últimos 7 días frente a {n0(b)} la semana anterior ({'+' if a >= b else ''}{n1((a - b) / b * 100)} %).", 14)

    # ---------- 8. qué falta medir ----------
    sin = [f for f in filas if not {"gancho", "estructura"} & set(f["etiquetas"])]
    if sin:
        reco(f"Etiqueta cada vídeo con «gancho» y «estructura» en estadisticas/etiquetas.json ({len(sin)} vídeos sin ellas): sin eso no se puede saber qué tipo de gancho funciona.",
             len(filas), "pista", motivo="faltan etiquetas")
    if len(filas) < 15:
        reco(f"Con {len(filas)} vídeos todo son pistas: cambia una sola cosa por lote (tema, gancho o estructura) para poder atribuir el resultado.",
             len(filas), "pista", motivo="muestra pequeña")

    orden_f = {"firme": 0, "tendencia": 1, "pista": 2}
    recos.sort(key=lambda r: orden_f[r["fuerza"]])
    return {"generado": d.get("generado"), "videos": len(filas), "conclusiones": conc, "recomendaciones": recos}


def a_markdown(a):
    L = [f"# Aprendizajes del canal — {a['generado'][:16].replace('T', ' ')}", "",
         "Generado solo cada mañana por `estadisticas/analizar.py` a partir de `datos/data.json`. "
         "Fuerza: **firme** (15+ vídeos), **tendencia** (5–14), **pista** (menos de 5: solo para decidir qué probar).",
         "", f"Vídeos analizados: {a['videos']}.", "", "## Recomendaciones para el próximo lote", ""]
    L += [f"- **[{r['fuerza']}]** {r['texto']}" + (f" _(motivo: {r['motivo']}; {r['n']} vídeos)_" if r.get("motivo") else "") for r in a["recomendaciones"]] or ["- Aún no hay datos suficientes."]
    L += ["", "## Conclusiones"]
    for area in dict.fromkeys(c["area"] for c in a["conclusiones"]):
        L += ["", f"### {area}", ""]
        L += [f"- **[{c['fuerza']}]** {c['texto']}" for c in a["conclusiones"] if c["area"] == area]
    return "\n".join(L).replace("\n\n\n", "\n\n") + "\n"


def main():
    ruta = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "datos", "data.json")
    d = json.load(open(ruta, encoding="utf-8"))
    a = analizar(d)
    if not d.get("ejemplo"):
        open(os.path.join(os.path.dirname(ruta), "aprendizajes.md"), "w", encoding="utf-8").write(a_markdown(a))
    print(a_markdown(a))


if __name__ == "__main__":
    main()
