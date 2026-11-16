#!/usr/bin/env python3
"""Genera ejemplo/data.json con datos INVENTADOS y el mismo formato que recoger.py (para probar la web)."""
import json, os, random, datetime as dt
random.seed(7)
fin = dt.date(2026, 11, 15)
vids = [("Venus gira al revés","Espacio",50),("Cleopatra y las pirámides","Histórico",48),
 ("¿Por qué bostezamos si vemos bostezar?","Cotidiano",41),("Las huellas que siguen en la Luna","Espacio",45),
 ("El Gran Hedor de Londres (1858)","Histórico",52),("Mi cerebro cuando toca callarse","Humor",33),
 ("Lo que hace tu móvil mientras duermes","Cotidiano",44),("La tostada siempre cae del lado malo","Cotidiano",38),
 ("El día que llovieron ranas","Histórico",47),("Un día en Venus dura más que un año","Espacio",42),
 ("Por qué los lunes se hacen eternos","Cotidiano",36),("La guerra del emú","Histórico",49),
 ("Mi cerebro a las 3 de la mañana","Humor",31),("Tu cuerpo brilla en la oscuridad","Cotidiano",43)]
videos = []
for i, (t, tema, dur) in enumerate(vids):
    f = fin - dt.timedelta(days=max(27 - i*2 + random.randint(0, 1), 0))
    hora = random.choice(["08:00", "20:00", "20:00", "08:00", "14:00"])
    edad = (fin - f).days + 1
    base = {"Cotidiano": 9000, "Histórico": 5200, "Espacio": 6100, "Humor": 3800}[tema]
    vistas = int(base*random.uniform(.45, 1.8)*min(1, edad/4)) + random.randint(80, 400)
    pct = round({"Cotidiano": 92, "Histórico": 74, "Espacio": 81, "Humor": 96}[tema]*random.uniform(.85, 1.15), 1)
    hook = min(90, round(random.uniform(58, 82) + (6 if tema == "Cotidiano" else 0), 1))
    curva = [[0.0, 100.0]]
    for k in range(1, 101):
        x = k/100
        v = hook - (hook-38)*x**0.8*random.uniform(.95, 1.05)
        curva.append([round(x, 2), round(max(v, 20), 1)])
    if pct > 95: curva[-1][1] += 12
    pend = edad <= 2
    likes = int(vistas*random.uniform(.025, .07))
    vd, resto = [], vistas
    for d in range(edad):
        q = int(resto*(0.45 if d == 0 else 0.3)) if d < edad-1 else resto
        vd.append([(f+dt.timedelta(days=d)).isoformat(), q]); resto -= q
    videos.append({"id": f"ejemplo{i:03d}", "titulo": t, "url": "https://youtube.com/@parecementirapero",
        "fecha": f.isoformat(), "hora": hora, "duracion": dur, "vistas": vistas, "likes": likes,
        "comentarios": int(likes*random.uniform(.04, .12)), "compartidos": int(vistas*random.uniform(.004, .015)),
        "subs": int(vistas*random.uniform(.004, .012)), "vistasEnganchadas": int(vistas*random.uniform(.6, .8)),
        "minutosVistos": round(vistas*dur*pct/100/60), "duracionMedia": round(dur*pct/100),
        "pctVisto": None if pend else pct, "retencion3s": None if pend else hook, "curva": None if pend else curva,
        "fuentes": None if pend else {"Feed de Shorts": round(random.uniform(72, 90), 1), "Búsqueda": round(random.uniform(3, 10), 1),
                                      "Página del canal": round(random.uniform(2, 8), 1), "Externo": round(random.uniform(1, 5), 1)},
        "vistasDia": vd, "horasPublicado": edad*24, "lote": None,
        "etiquetas": {"tema": tema, "voz": random.choice(["v1", "v2"]), "gancho": random.choice(["pregunta", "dato", "orden"])},
        "tema": tema})
diario = []
for d in range(56):
    f = fin - dt.timedelta(days=55-d)
    v = max(int(400 + d*55 + random.uniform(-250, 350) + (900 if d % 7 in (5, 6) else 0)), 120)
    diario.append({"fecha": f.isoformat(), "vistas": v, "minutos": v//2, "subs": int(v*random.uniform(.004, .01)), "likes": int(v*.045)})
out = {"generado": "2026-11-16T09:00:00+01:00", "ejemplo": True, "canal": "Parece Mentira",
       "canalTotales": {"suscriptores": 1284, "vistas": sum(x["vistas"] for x in videos), "videos": len(videos)},
       "videos": videos, "diario": diario, "notas": []}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json"), "w"), ensure_ascii=False)
