#!/usr/bin/env python3
"""Pruebas del estudio. Sin red, sin tocar los datos reales. Uso: python3 estadisticas/estudio/prueba.py"""
import datetime as dt
import json
import os
import random
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import analisis as A          # noqa: E402
import autopsia as U          # noqa: E402
import comentarios as C       # noqa: E402
import estadistica as E       # noqa: E402
import experimento as X       # noqa: E402
import ficha as F             # noqa: E402
import informe as I           # noqa: E402
import mediciones as M        # noqa: E402
import recogida_extra as R    # noqa: E402
import tabla as T             # noqa: E402

OK = FALLOS = 0


def comprueba(nombre, condicion, detalle=""):
    global OK, FALLOS
    if condicion:
        OK += 1
    else:
        FALLOS += 1
        print(f"✘ {nombre} {detalle}")


# ---------------------------------------------------------------- estadística
comprueba("mediana", E.mediana([3, None, 1, 2]) == 2)
comprueba("tamaño de muestra 16/10", E.tamano_muestra(16, 10) == 41, E.tamano_muestra(16, 10))
comprueba("tamaño de muestra 16/20", E.tamano_muestra(16, 20) == 11, E.tamano_muestra(16, 20))
comprueba("diferencia detectable inversa", abs(E.diferencia_detectable(16, 41) - 10) < 0.2)
comprueba("permutación exacta 3 contra 3", abs(E.permutacion([1, 2, 3], [4, 5, 6]) - 0.1) < 1e-9)
comprueba("p mínimo 3 contra 3", abs(E.p_minimo_posible(3, 3) - 0.1) < 1e-9)
comprueba("permutación sin diferencia", E.permutacion([1, 2, 3, 4], [1, 2, 3, 4]) == 1.0)
comprueba("permutación 5 contra 5 separados", abs(E.permutacion([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]) - 2 / 252) < 1e-9)
comprueba("permutación: no le afecta un valor enorme", E.permutacion([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]) == E.permutacion([1, 2, 3, 4, 5], [6, 7, 8, 9, 10000]))
rr = random.Random(1)
uniformes = sum(E.permutacion([rr.gauss(0, 1) for _ in range(14)], [rr.gauss(0, 1) for _ in range(14)]) < 0.05 for _ in range(400))
comprueba("permutación aproximada: ~5 % de falsos positivos", 8 <= uniformes <= 34, f"{uniformes}/400")
comprueba("permutación aproximada: detecta grupos separados", E.permutacion(list(range(14)), list(range(14, 28))) < 0.0001)
comprueba("permutación aproximada ≈ exacta", abs(E.permutacion([1, 5, 6, 9, 12, 14, 15, 20, 3], [2, 4, 7, 8, 10, 11, 13, 16, 30]) - 0.86) < 0.08,
          E.permutacion([1, 5, 6, 9, 12, 14, 15, 20, 3], [2, 4, 7, 8, 10, 11, 13, 16, 30]))
comprueba("permutación con un valor", E.permutacion([1], [2, 3]) is None)
comprueba("bootstrap pide 3 por grupo", E.bootstrap_diferencia([1, 2], [3, 4, 5]) is None)
ic = E.bootstrap_diferencia([70, 72, 75, 78, 80, 74, 77, 79], [50, 52, 55, 58, 60, 54, 57, 59])
comprueba("bootstrap detecta 20 puntos", ic[1] > 10 and ic[2] < 30, ic)
comprueba("bootstrap repetible", ic == E.bootstrap_diferencia([70, 72, 75, 78, 80, 74, 77, 79], [50, 52, 55, 58, 60, 54, 57, 59]))
s = E.spearman([1, 2, 3, 4, 5, 6], [2, 4, 5, 9, 12, 20])
comprueba("spearman perfecta", abs(s[0] - 1) < 1e-9 and s[1] < 0.02, s)
s = E.spearman([1, 2, 3, 4, 5, 6], [6, 5, 4, 3, 2, 1])
comprueba("spearman inversa", abs(s[0] + 1) < 1e-9)
comprueba("spearman con empates", abs(E.spearman([1, 1, 2, 2], [1, 1, 2, 2])[0] - 1) < 1e-9)
comprueba("spearman pocos datos", E.spearman([1, 2, 3], [1, 2, 3]) is None)
comprueba("spearman sin variación", E.spearman([1, 1, 1, 1], [1, 2, 3, 4]) is None)
comprueba("nivel: pista con 4", E.nivel_evidencia(4, 20, (20, 5, 30), True, True, 0.001) == "pista")
comprueba("nivel: indicio", E.nivel_evidencia(6, 6, (10, -2, 20), True, False, 0.08) == "indicio")
comprueba("nivel: mismo sentido pero p alto no basta", E.nivel_evidencia(6, 6, (10, -2, 20), True, False, 0.4) == "pista")
comprueba("nivel: sin otra red hace falta p < 0,05", E.nivel_evidencia(6, 6, (10, 2, 20), None, False, 0.08) == "pista"
          and E.nivel_evidencia(6, 6, (10, 2, 20), None, False, 0.03) == "indicio")
comprueba("nivel: regla", E.nivel_evidencia(12, 12, (10, 2, 20), True, True, 0.001) == "regla")
comprueba("nivel: regla exige p corregido", E.nivel_evidencia(12, 12, (10, 2, 20), True, True, 0.01, comparaciones=50) == "indicio")
comprueba("nivel: sin réplica no es regla", E.nivel_evidencia(12, 12, (10, 2, 20), True, False, 0.001) == "indicio")
comprueba("nivel: intervalo que cruza no es regla", E.nivel_evidencia(12, 12, (10, -2, 20), True, True, 0.04) == "indicio")
comprueba("nivel: redes en contra", E.nivel_evidencia(12, 12, (10, 2, 20), False, True, 0.001) == "pista")
comprueba("correlación nunca es regla", E.nivel_correlacion(200, 0.0001, True) == "indicio")

# Falsos positivos: con datos sin ningún efecto, ¿cuántas veces el intervalo al 90 % excluye el cero?
rnd = random.Random(7)
falsos = 0
for i in range(200):
    a = [rnd.gauss(60, 16) for _ in range(12)]
    b = [rnd.gauss(60, 16) for _ in range(12)]
    ic = E.bootstrap_diferencia(a, b, n=600, semilla=i)
    falsos += not (ic[1] <= 0 <= ic[2])
comprueba("falsos positivos del intervalo ≤ 15 %", falsos <= 30, f"{falsos}/200")
# Potencia: con 20 puntos de efecto real y 12 por grupo, se detecta casi siempre
aciertos = 0
for i in range(100):
    a = [rnd.gauss(75, 16) for _ in range(12)]
    b = [rnd.gauss(55, 16) for _ in range(12)]
    ic = E.bootstrap_diferencia(a, b, n=600, semilla=i)
    aciertos += ic[1] > 0
comprueba("detecta 20 puntos con 12 por grupo ≥ 75 %", aciertos >= 75, f"{aciertos}/100")

# ---------------------------------------------------------------- ficha
d = F.derivar_de_guion("Mira tus uñas. La Luna se aleja. ¿Cómo lo sabemos? Por un láser.")
comprueba("gancho de 3 palabras", d["gancho_palabras"] == 3 and d["gancho_persona"] == "tú" and d["preguntas"] == 1, d)
d = F.derivar_de_guion("Esta pisada tiene más de cincuenta años… y sigue exactamente igual. Luego otra cosa.")
comprueba("los puntos suspensivos no cortan la frase", d["gancho_palabras"] == 11 and d["gancho_cifra"], d)
d = F.derivar_de_guion("Esta huella no es humana. Es de un koala.")
comprueba("negación", d["gancho_negacion"] and not d["gancho_pregunta"] and d["gancho_persona"] == "impersonal")
comprueba("«una» no es cifra", not F.derivar_de_guion("Hay una puerta en la casa.")["gancho_cifra"])
c = F.derivar_de_calidad("**Nota: 92/100**\n- cortes_min=39.7 · palabras_s=2.63\n- movimiento_primer_segundo=8.66")
comprueba("lee calidad", c == {"nota_calidad": 92.0, "cortes_min": 39.7, "palabras_seg": 2.63, "f0_movimiento": 8.66}, c)
buena = F.nueva("l", "01", "Mira tus uñas. Fin.", None, dict(tema="Espacio", alcance="universal", gancho="orden", f0_palabras=3,
                f0_sujeto="objeto", f0_literal=True, estructura="escala", remate="dato", duracion_s=55, montaje="denso", experimento="no"))
comprueba("ficha válida", F.validar(buena) == [], F.validar(buena))
mala = dict(buena, tema="Deportes", f0_literal="sí", duracion_s="55", inventada=1)
comprueba("ficha con 4 errores", len(F.validar(mala)) == 4, F.validar(mala))
comprueba("ficha incompleta", any("falta «remate»" in p for p in F.validar({k: v for k, v in buena.items() if k != "remate"})))
comprueba("convertir", F.convertir("f0_palabras", "3") == 3 and F.convertir("f0_literal", "sí") is True and F.convertir("tema", "Espacio") == "Espacio")
ac = F.acuerdo({"a": {"tema": "Espacio", "alcance": "nicho"}, "b": {"tema": "Ciencia"}}, {"a": {"tema": "Espacio", "alcance": "universal"}, "b": {"tema": "Espacio"}})
comprueba("acuerdo entre codificadores", ac["tema"] == (1, 2) and ac["alcance"] == (0, 1), ac)
reales = F.cargar()
comprueba("fichas reales válidas", all(F.validar(f) == [] for f in reales.values()), {k: F.validar(f) for k, f in reales.items() if F.validar(f)})

# ---------------------------------------------------------------- mediciones
comprueba("interpolación logarítmica", M.interpolar_vistas([(12, 100), (36, 10000)], 24) == (1000, "interpolada"))
comprueba("no extrapola", M.interpolar_vistas([(30, 100), (50, 200)], 24) == (None, None))
comprueba("no interpola entre lecturas muy separadas", M.interpolar_vistas([(1, 100), (60, 9000)], 24) == (None, None))
DATA = {"generado": "2026-12-03T09:20:00+01:00",
        "videos": [{"id": "AAA", "fecha": "2026-12-01", "hora": "08:00", "vistas": 4000, "likes": 50, "comentarios": 2,
                    "pctVisto": 55.0, "duracionMedia": 30}],
        "tiktok": {"videos": [{"id": "111", "fecha": "2026-12-01", "hora": "08:30", "vistas": 900, "likes": 9, "comentarios": 0, "compartidos": 1}]},
        "contenidos": [{"clave": "AAA", "youtube": "AAA", "tiktok": "111"}],
        "historico": {"2026-12-01": {"youtube": {"AAA": 100}, "tiktok": {"111": 50}},
                      "2026-12-02": {"youtube": {"AAA": 2000}, "tiktok": {"111": 600}},
                      "2026-12-03": {"youtube": {"AAA": 4000}, "tiktok": {"111": 900}}}}
STUDIO = {"AAA": {"seQuedan": 71.0, "fecha": "2026-12-02", "hora": "09:00", "vistas": 1900, "horas": 12.0,
                  "antes": [{"seQuedan": 50.0, "fecha": "2026-12-01", "hora": "10:00", "vistas": 300, "horas": 1.0}]}}
TTS = {"2026-12-02 10:00": {"111": {"medio_s": 20.0, "completo_pct": 20.0, "curva": {"1": 80, "3": 60, "10": 40}, "vistas": 610, "dur": 55}}}
m1 = M.construir(None, DATA, STUDIO, TTS)
yt, tt = m1["videos"]["AAA"]["youtube"], m1["videos"]["AAA"]["tiktok"]
comprueba("une TikTok con YouTube", "111" not in m1["videos"] and tt["id"] == "111")
comprueba("se_quedan a 24 h = lectura de 25 h, no la de 2 h", yt["24"]["se_quedan"] == 71.0 and yt["24"]["edad_h"]["se_quedan"] == 25.0, yt["24"])
comprueba("vistas a 24 h interpoladas", 1600 <= yt["24"]["vistas"] <= 2000 and yt["24"]["vistas_modo"] == "interpolada", yt["24"])
comprueba("48 h: vistas sí (interpoladas), se_quedan no", "vistas" in yt.get("48", {}) and "se_quedan" not in yt.get("48", {}), yt.get("48"))
comprueba("TikTok 24 h con curva", tt["24"]["medio_s"] == 20.0 and tt["24"]["sigue_3s"] == 60 and tt["24"]["curva"][10] == 40)
comprueba("no hay medición de 7 días aún", "168" not in yt)
# una medición guardada no se reescribe aunque lleguen lecturas distintas
STUDIO2 = {"AAA": {"seQuedan": 99.0, "fecha": "2026-12-02", "hora": "09:00", "vistas": 1900, "horas": 12.0}}
m2 = M.construir(json.loads(json.dumps(m1)), DATA, STUDIO2, TTS)
comprueba("lo guardado manda", m2["videos"]["AAA"]["youtube"]["24"]["se_quedan"] == 71.0)
comprueba("valor() provisional", M.valor(m1, "AAA", "youtube", "se_quedan") == (71.0, 25.0, True), M.valor(m1, "AAA", "youtube", "se_quedan"))
comprueba("valor() exige 24 h", M.valor({"videos": {"Z": {"youtube": {"ultima": {"se_quedan": 40, "edad_h": {"se_quedan": 3}}}}}}, "Z", "youtube", "se_quedan")[0] is None)
comprueba("mediciones con los datos reales", len(M.construir()["videos"]) >= 8)


# ---------------------------------------------------------------- estudio con una muestra inventada
def muestra_inventada(n=48, efecto=18, semilla=3):
    """n vídeos en 4 semanas; los de gancho en segunda persona retienen `efecto` puntos más, en las dos redes."""
    rnd = random.Random(semilla)
    fichas, videos = {}, {}
    for i in range(n):
        vid = f"V{i:03d}"
        tu = i % 2 == 0
        dia = dt.datetime(2026, 12, 1, 8 if i % 4 < 2 else 20) + dt.timedelta(days=i // 2)
        base = 55 + (efecto if tu else 0) + rnd.gauss(0, 10)
        fichas[f"l/{i:02d}"] = dict(buena, youtube=vid, titulo=vid, gancho_persona="tú" if tu else "impersonal",
                                    tema=["Espacio", "Ciencia", "Cotidiano"][i % 3], gancho_palabras=3 + i % 7,
                                    momento="previo", experimento="H3", brazo="A" if tu else "B")
        videos[vid] = {"youtube": {"id": vid, "publicado": dia.isoformat() + "+01:00",
                                   "48": {"se_quedan": base, "seg_por_vista": base / 3, "vistas": int(10 ** (2.5 + base / 60))}},
                       "tiktok": {"id": "t" + vid, "48": {"sigue_3s": base - 15 + rnd.gauss(0, 4), "medio_s": base / 4, "vistas": 300}}}
    return fichas, {"videos": videos}


fichas, med = muestra_inventada()
r = A.ejecutar(escribir=False, fichas=fichas, mediciones=med, data={})
c = next(x for x in r["categoricas"] if x["variable"] == "gancho_persona" and x["valor"] == "tú" and x["metrica"] == "yt_se_quedan")
comprueba("encuentra el efecto real", c["diferencia"] > 10 and c["intervalo"][0] > 0 and c["redes_coinciden"], c)
comprueba("efecto real replicado → regla", c["nivel"] == "regla" and c["replicado"], c["nivel"])
tema = [x for x in r["categoricas"] if x["variable"] == "tema" and x["metrica"] == "yt_se_quedan"]
comprueba("el tema (sin efecto) no llega a regla", all(x["nivel"] != "regla" for x in tema), [(x["valor"], x["nivel"]) for x in tema])
comprueba("detecta variables que no varían", ("montaje", "denso") in r["sin_variacion"])
comprueba("detecta variables pegadas", ("gancho_persona", "turno") not in r["confundidas"])
md = A.a_markdown(r)
comprueba("informe con la regla", "**regla**" in md and "gancho_persona" in md)
fichas0, med0 = muestra_inventada(efecto=0, semilla=11)
r0 = A.ejecutar(escribir=False, fichas=fichas0, mediciones=med0, data={})
reglas0 = [x for x in r0["categoricas"] if x["nivel"] == "regla"]
comprueba("sin efecto real no inventa reglas", not reglas0, [(x["variable"], x["valor"]) for x in reglas0])
real = A.ejecutar(escribir=False)
comprueba("estudio con los datos reales", real["muestra"]["videos"] >= 8 and A.a_markdown(real).count("##") >= 5)

# audiencia
DA = {"youtubeExtra": {"desde": "2026-11-01", "edadGenero": [["age18-24", "male", 30], ["age25-34", "female", 20], ["age35-44", "male", 50]],
                       "paises": [["ES", 250, 50], ["MX", 500, 120], ["US", 250, 40]]}}
a = A.audiencia(DA, {"estado": "x", "edades": ["age18-24", "age25-34"], "paises": ["ES", "MX"]})
comprueba("audiencia: objetivo", abs(a["objetivo"]["dentro_edad"] - 50) < 1e-9 and abs(a["objetivo"]["dentro_pais"] - 75) < 1e-9, a["objetivo"])
comprueba("audiencia: latam y segundos por vista", abs(a["latam"] - 50) < 1e-9 and abs(a["seg_por_vista_pais"]["ES"] - 12) < 1e-9)
comprueba("audiencia vacía", A.audiencia({}) is None)
filas = T.construir(fichas, med)
DV = {"videos": [{"id": "V000", "audiencia": {"vistas": 100, "edadGenero": [["age18-24", "male", 100]]}},
                 {"id": "V003", "audiencia": {"vistas": 300, "edadGenero": [["age35-44", "female", 100]]}}]}
g = A.audiencia_por_grupo(DV, filas, "tema")
comprueba("audiencia por tema ponderada", g["Espacio"]["vistas"] == 400 and abs(g["Espacio"]["edad"]["age35-44"] - 75) < 1e-9, g)

# ---------------------------------------------------------------- autopsia
c = U.analizar_curva({1: 80, 2: 70, 3: 62, 5: 55, 8: 52, 12: 50, 13: 40, 20: 38, 30: 36})
comprueba("curva: pierde 38 % en 3 s", c["pierde_en_3s"] == 38)
comprueba("curva: escalón en 12–13 s", c["escalones"] and c["escalones"][0]["desde"] == 12, c["escalones"])
comprueba("curva: tramo que aguanta", any(e["desde"] == 13 for e in c["aguantan"]), c["aguantan"])
comprueba("curva corta", U.analizar_curva({1: 50, 2: 40}) is None)
fr = U.frases_con_tiempo("Uno dos tres. Cuatro cinco seis siete… y ocho. Nueve diez.", 10)
comprueba("frases con tiempo", len(fr) == 3 and abs(fr[1][0] - 30 / 11) < 1e-9 and U.frase_en(fr, 9).startswith("Nueve"), fr)
comprueba("diagnóstico: primer segundo", U.diagnostico({"yt_se_quedan": 0.7}, {"f0_palabras": 13})[0] == "primer segundo")
comprueba("diagnóstico: tema", U.diagnostico({"yt_se_quedan": 0.7}, {"f0_palabras": 3, "gancho_palabras": 4, "f0_literal": True}) == "tema")
comprueba("diagnóstico: ritmo", U.diagnostico({"yt_se_quedan": 1.0, "yt_seg_por_vista": 0.7}, {}) == "ritmo")
comprueba("diagnóstico: acierto", U.diagnostico({"yt_se_quedan": 1.3, "yt_seg_por_vista": 1.2}, {}) == "acierto")
comprueba("diagnóstico: distribución", U.diagnostico({"yt_se_quedan": 1.05, "yt_seg_por_vista": 1.05, "yt_vistas": 0.3}, {}) == "distribución")
comprueba("diagnóstico: sin datos", U.diagnostico({}, {}) == "sin datos")
autos = U.ejecutar(escribir=False, fichas=fichas, mediciones=med, data={})
comprueba("autopsias de la muestra inventada", len(autos) == 48 and all(a["diagnostico"] in U.DIAGNOSTICOS for a in autos))
comprueba("autopsia a texto", "Diagnóstico" in U.a_markdown(autos[0]))
ar = U.ejecutar(escribir=False)
comprueba("autopsias reales con guion", any(a["frases"] for a in ar))

# ---------------------------------------------------------------- experimentos
with tempfile.TemporaryDirectory() as tmp:
    X.CARPETA = tmp
    filas = T.construir(fichas, med)
    exp = X.nuevo("H3", "Segunda persona retiene más", "gancho_persona", "yt_se_quedan", 15, inicio="2026-12-01",
                  filas=filas, hoy=dt.date(2026, 11, 30))
    comprueba("experimento: tamaño con desviación medida", exp["por_brazo"] >= 5 and "medida" in exp["desviacion_origen"], exp)
    comprueba("experimento: cierre después del último vídeo", exp["cierre"] > exp["ultimo_video"] >= exp["inicio"])
    cal = X.calendario(exp)
    comprueba("experimento: alterna el orden", cal[0][1] != cal[1][1])
    try:
        X.nuevo("H3", "otra", "x", "yt_se_quedan", 15, filas=filas)
        comprueba("experimento: no se reescribe la ficha previa", False)
    except ValueError:
        comprueba("experimento: no se reescribe la ficha previa", True)
    e = X.estado(exp, filas, dt.date(2026, 12, 5))
    comprueba("experimento: a favor", e["veredicto"] == "a favor" and e["medidos"] == {"A": 24, "B": 24}, e)
    try:
        X.cerrar("H3", filas, hoy=dt.date(2026, 12, 2))
        comprueba("experimento: no cierra antes de tiempo", False)
    except ValueError:
        comprueba("experimento: no cierra antes de tiempo", True)
    cerrado = X.cerrar("H3", filas, hoy=dt.date(2027, 1, 15))
    comprueba("experimento: efecto real y repetido → regla", cerrado["estado"] == "cerrado" and cerrado["nivel"] == "regla", cerrado["nivel"])
    filas0 = T.construir(fichas0, med0)
    exp0 = X.nuevo("H4", "Sin efecto", "gancho_persona", "yt_se_quedan", 15, inicio="2026-12-01", filas=filas0, hoy=dt.date(2026, 11, 30))
    for f in fichas0.values():
        f["experimento"] = "H4"
    e0 = X.estado(exp0, T.construir(fichas0, med0), dt.date(2026, 12, 30))
    comprueba("experimento sin efecto: no dice «a favor»", not e0["veredicto"].startswith("a favor"), e0["veredicto"])
    exp1 = X.nuevo("H9", "Sin datos aún", "tema", "tt_medio_s", 4, filas=[], hoy=dt.date(2026, 11, 30))
    comprueba("experimento: desviación de partida si no hay datos", "partida" in exp1["desviacion_origen"] and exp1["por_brazo"] > 5)
    comprueba("experimento a texto", "cierre el" in X.a_markdown(exp, e))
    texto, _ = I.ejecutar(dt.date(2026, 12, 14), escribir=False, fichas=fichas, mediciones=med, data=DA)
    comprueba("informe semanal", "Vídeos de la semana" in texto and "H3" in texto and "Propuestas" in texto and "V0" in texto)

# ---------------------------------------------------------------- comentarios
casos = {"Haz uno de los agujeros negros": "pide otro tema", "Eso es mentira": "duda de que sea verdad",
         "@pepe mira esto": "menciona a alguien", "¿Y por qué no se cae?": "pregunta", "jajaja increíble": "emoción o chiste",
         "En realidad fueron 45 minutos": "corrige", "La voz es de IA": "sobre la voz o el montaje",
         "Mira mi canal https://x.y": "spam", "Ok": "otros"}
for texto, esperado in casos.items():
    comprueba(f"comentario «{texto}»", C.clasificar(texto) == esperado, C.clasificar(texto))
comprueba("comentarios a texto", "pide otro tema" in C.a_markdown([{"video": "A", "texto": t} for t in casos]))
comprueba("sin comentarios", "Todavía no hay" in C.a_markdown([]))


# ---------------------------------------------------------------- recogida extra (YouTube simulado)
class YouTubeFalso:
    def __init__(self, sin_demografia=(), comentarios_prohibidos=False):
        self.sin, self.prohibido, self.llamadas = set(sin_demografia), comentarios_prohibidos, []

    def analytics(self, **p):
        self.llamadas.append(p)
        vid = p["filters"].split("==")[1]
        if p["dimensions"] == "ageGroup,gender":
            if vid in self.sin:
                raise RuntimeError("HTTP 400: not enough data")
            return [{"ageGroup": "age25-34", "gender": "male", "viewerPercentage": 60.0},
                    {"ageGroup": "age35-44", "gender": "female", "viewerPercentage": 40.0}]
        return [{"country": "MX", "views": 700, "estimatedMinutesWatched": 150}, {"country": "ES", "views": 300, "estimatedMinutesWatched": 50}]

    def data(self, recurso, **p):
        if self.prohibido:
            raise RuntimeError("HTTP 403 en commentThreads: insufficientPermissions")
        if p.get("pageToken"):
            return {"items": [{"id": "c2", "snippet": {"totalReplyCount": 0, "topLevelComment": {"snippet": {
                "textDisplay": "Haz otro de Marte", "publishedAt": "2026-12-02T10:00:00Z", "likeCount": 1, "authorDisplayName": "NO GUARDAR"}}}}]}
        return {"nextPageToken": "x", "items": [{"id": "c1", "snippet": {"totalReplyCount": 2, "topLevelComment": {"snippet": {
            "textDisplay": "Eso es mentira", "publishedAt": "2026-12-01T10:00:00Z", "likeCount": 3, "authorDisplayName": "NO GUARDAR"}}}}]}


with tempfile.TemporaryDirectory() as tmp:
    R.COMENTARIOS = os.path.join(tmp, "datos", "comentarios.json")
    vs = [{"id": "A", "horasPublicado": 60, "comentarios": 2}, {"id": "B", "horasPublicado": 10, "comentarios": 0},
          {"id": "C", "horasPublicado": 2000, "comentarios": 0}, {"id": "D", "horasPublicado": 80, "comentarios": 0}]
    yt = YouTubeFalso(sin_demografia={"D"})
    res = R.completar(yt, vs, "2026-11-01", "2026-12-03", previo=[{"id": "C", "audiencia": {"vistas": 5}}], avisar=lambda *_: None)
    comprueba("audiencia por vídeo", vs[0]["audiencia"]["vistas"] == 1000 and len(vs[0]["audiencia"]["edadGenero"]) == 2, vs[0])
    comprueba("vídeo joven: no se pide", "audiencia" not in vs[1])
    comprueba("vídeo viejo: conserva la anterior", vs[2]["audiencia"] == {"vistas": 5})
    comprueba("sin demografía: se queda con los países", vs[3]["audiencia"]["edadGenero"] == [] and vs[3]["audiencia"]["vistas"] == 1000)
    comprueba("solo pide lo necesario", res["audiencias_pedidas"] == 2 and len(yt.llamadas) == 4, len(yt.llamadas))
    guardado = json.load(open(R.COMENTARIOS, encoding="utf-8"))
    comprueba("comentarios guardados sin autor", len(guardado["comentarios"]) == 2 and "NO GUARDAR" not in json.dumps(guardado), guardado)
    res2 = R.completar(yt, vs, "2026-11-01", "2026-12-03", avisar=lambda *_: None)
    comprueba("comentarios sin duplicar", res2["comentarios"] == 2 and res2["comentarios_nuevos"] == 0)
    avisos = []
    R.completar(YouTubeFalso(comentarios_prohibidos=True), [dict(v, comentarios=1) for v in vs], "a", "b", avisar=avisos.append)
    comprueba("permiso denegado: avisa una vez y sigue", sum("no deja leer comentarios" in a for a in avisos) == 1, avisos)

print(f"{OK} de {OK + FALLOS} pruebas correctas")
sys.exit(1 if FALLOS else 0)
