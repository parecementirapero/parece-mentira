"""Piezas comunes de los generadores del lote 2026-11-15-tarde."""
import json, os, sys

def F(**k): return {"tipo": "forma", **k}

def guardar(ep, salida):
    os.makedirs(salida, exist_ok=True)
    json.dump(ep, open(os.path.join(salida, "episodio.json"), "w"), ensure_ascii=False, indent=1)
    print(os.path.join(salida, "episodio.json"))

def salida():
    return sys.argv[1] if len(sys.argv) > 1 else "."

def aguja(largo, ancho, color, **k):
    """Aguja que gira sobre el centro del reloj (rot positiva = sentido horario; 0 = las 12)."""
    a = ancho / 2
    return F(forma="poligono", puntos=[[-a, 0], [-a * 0.6, -largo], [a * 0.6, -largo], [a, 0], [a, largo * 0.15], [-a, largo * 0.15]],
             relleno=color, **k)

def reloj(x, y, r, min0, min1, t0, t1, z=0.3, keys=None, anim=None):
    """Reloj con el horario cerca de las 9 y el minutero que avanza de min0 a min1 entre t0 y t1."""
    import math
    marcas = [F(forma="redondeado", ancho=10 if i % 3 else 14, alto=34 if i % 3 == 0 else 18, relleno="#2a2a33",
                x=round((r - 34) * math.sin(math.radians(i * 30))), y=round(-(r - 34) * math.cos(math.radians(i * 30))),
                rot=i * 30) for i in range(12)]
    g = {"tipo": "grupo", "x": x, "y": y, "ancho": 2 * r + 80, "alto": 2 * r + 80, "z": z, "keys": keys or [],
         "hijos": [
             F(forma="circulo", radio=r, relleno=["#fffaf0", "#e8dcc4"], grosor=14, borde="#7a5a2e", brillo=True),
             *marcas,
             aguja(r * 0.5, 22, "#2a2a33", keys=[{"t": t0, "rot": 270 + min0 * 0.5, "ease": "lineal"}, {"t": t1, "rot": 270 + min1 * 0.5}]),
             aguja(r * 0.78, 14, "#c0392b", keys=[{"t": t0, "rot": min0 * 6, "ease": "lineal"}, {"t": t1, "rot": min1 * 6}]),
             F(forma="circulo", radio=16, relleno="#2a2a33"),
         ]}
    if anim: g["anim"] = anim
    return g
