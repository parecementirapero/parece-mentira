"""Prueba del motor v2 (estilo de los vídeos objetivo, motor/OBJETIVO.md): huellas en la Luna, 47 s.

Tiempos sacados de la alineación de ElevenLabs (python3 -m motor.tiempos palabras alineacion.json).
El MP3 y la alineación no están en git: carpeta local de Nico, renders/prueba/v2/.
Uso:  python3 motor/ejemplos/v2-huellas-luna/generar.py RUTA_AUDIO_Y_ALINEACION
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else AQUI


def F(**k): return {"tipo": "forma", **k}
def IMG(nombre, **k): return {"tipo": "imagen", "archivo": f"svg/{nombre}.svg", **k}
def ROT(**k): return {"tipo": "rotulo", **k}


def pop(t0, t1=None, escala=1.0):
    """Entrada con rebote (y salida opcional)."""
    ks = [{"t": t0, "escala": 0.0, "op": 0}, {"t": t0 + 0.08, "op": 1},
          {"t": t0 + 0.35, "escala": escala, "ease": "rebote"}]
    if t1 is not None:
        ks += [{"t": t1, "escala": escala, "op": 1}, {"t": t1 + 0.25, "escala": escala * 0.6, "op": 0}]
    return ks


NOCHE = {"colores": ["#01020a", "#070b24", "#151a3d"]}
estrellas = {"tipo": "particulas", "clase": "estrellas", "area": [0, 0, 1080, 1100], "n": 140,
             "tam": [1.2, 3.4], "vel": [-6, 0], "color": "#ffffff", "z": 0.08, "semilla": 4}


def tierra(x=880, y=590, r=100):
    return [{"tipo": "brillo", "x": x, "y": y, "radio": r * 2.4, "color": "#6fb6ff", "intensidad": 0.35, "z": 0.15},
            {"tipo": "esfera", "x": x, "y": y, "radio": r, "textura": "tierra", "halo": "#8fd0ff", "giro": 12,
             "luz": [-0.7, -0.4], "z": 0.15, "semilla": 8, "anim": {"flotar": [6, 5]}}]


def suelo_luna(borde=1060, semilla=12, cr=20):
    return {"tipo": "suelo", "material": "luna", "borde": borde, "crateres": cr, "z": 0.55, "semilla": semilla}


def golpe_polvo(t0, x, y, r=320):
    return [{"tipo": "brillo", "x": x, "y": y, "radio": r, "color": "#e6e7ef", "intensidad": 0.85, "ey": 0.45, "z": 0.7,
             "keys": [{"t": t0, "escala": 0.3, "op": 0}, {"t": t0 + 0.06, "op": 0.9},
                      {"t": t0 + 1.1, "escala": 1.5, "op": 0, "ease": "salida"}]},
            {"tipo": "particulas", "clase": "polvo", "color": "#f1f2f7", "area": [x - 260, y - 60, x + 260, y + 40],
             "n": 70, "tam": [2.5, 6], "vel": [0, -90], "dispersion": 1.0, "z": 0.75, "semilla": 9,
             "keys": [{"t": t0, "op": 0}, {"t": t0 + 0.05, "op": 1}, {"t": t0 + 1.4, "op": 0}]}]


def pisada_luna(t_baja, x=540, y=1420, sube=None, ancho=360):
    """La bota baja, deja la huella y (opcional) vuelve a subir."""
    ks = [{"t": t_baja - 0.45, "y": y - 1100, "escala": 1.35, "op": 1},
          {"t": t_baja, "y": y - 150, "escala": 1.0, "ease": "entrada"}]
    if sube is not None:
        ks += [{"t": sube, "y": y - 150}, {"t": sube + 0.6, "y": y - 1900, "escala": 1.3, "ease": "entrada"}]
    return [
        IMG("huella_bota", ancho=ancho, x=x, y=y, ey=0.52, z=0.62,
            keys=[{"t": t_baja - 0.01, "op": 0}, {"t": t_baja + 0.05, "op": 1}]),
        *golpe_polvo(t_baja, x, y + 40),
        IMG("bota", ancho=520, x=x + 30, z=0.85, sombra={"radio": 24, "op": 0.5}, keys=ks),
    ]


# ------------------------------------------------------------------ escenas (tiempos absolutos)
S = []

# 1 · 0 – 4.45  GANCHO: la bota pisa desde el fotograma 0
S.append({"inicio": 0, "fin": 4.45, "fondo": NOCHE, "vineta": 0.55,
          "camara": {"zoom": [1.0, 1.10], "pan": [[0, 0], [0, -40]]},
          "elementos": [estrellas, *tierra(), suelo_luna(),
                        *pisada_luna(0.40, sube=2.3),
                        ROT(texto="+50", unidad="AÑOS", tam=130, x=540, y=830, z=0.3, keys=pop(1.25)),
                        {"tipo": "brillo", "x": 540, "y": 1440, "radio": 300, "color": "#fff3c4", "intensidad": 0.35,
                         "ey": 0.5, "z": 0.62, "keys": [{"t": 2.6, "op": 0}, {"t": 3.2, "op": 1}],
                         "anim": {"pulso": [0.06, 1.6]}}]})

# 2 · 4.45 – 9.10  PLAYA vista desde arriba: la huella se borra en horas
S.append({"inicio": 4.45, "fin": 9.10, "entrada": "desenfoque", "dur_entrada": 0.4,
          "fondo": {"colores": ["#f3d9a4", "#d9b47a"]}, "vineta": 0.35,
          "camara": {"zoom": [1.04, 1.12], "pan": [[0, 0], [0, -20]]},
          "elementos": [
              {"tipo": "suelo", "material": "arena", "borde": -120, "ondulacion": 0, "z": 0.5, "semilla": 3},
              F(forma="poligono", puntos=[[0, -46], [12, -14], [44, -14], [18, 6], [28, 40], [0, 18], [-28, 40],
                                          [-18, 6], [-44, -14], [-12, -14]], relleno=["#ffb05a", "#f27c35"],
                brillo=True, sombra={"radio": 8, "desplaz": [0, 7]}, x=200, y=1500, rot=15, z=0.5),
              IMG("huella_pie", ancho=300, x=560, y=1250, z=0.6,
                  keys=[{"t": 0.25, "op": 0, "escala": 1.25}, {"t": 0.45, "op": 1, "escala": 1.0, "ease": "salida"},
                        {"t": 3.0, "op": 1}, {"t": 3.9, "op": 0}]),
              {"tipo": "agua", "lado": "arriba", "z": 0.5, "amplitud": 26, "colores": ["#1a6fa6", "#68d6e4"],
               "keys": [{"t": 0, "nivel": 520}, {"t": 2.4, "nivel": 560}, {"t": 3.2, "nivel": 1560, "ease": "salida"},
                        {"t": 4.65, "nivel": 600}]},
              *[{"tipo": "flecha", "puntos": [[1150, y], [900, y - 30], [650, y + 25], [380, y - 15]], "grosor": 9,
                 "color": "#ffffffcc", "punta": False, "z": 0.8, "anim": {"deriva": [-160, 0]},
                 "keys": [{"t": t0, "progreso": 0, "op": 1}, {"t": t0 + 0.7, "progreso": 1}, {"t": t0 + 1.4, "op": 0}]}
                for y, t0 in [(980, 2.9), (1380, 3.15), (1700, 3.4)]],
              ROT(contar=[0, 6, 1.2], contar_desde=1.85, unidad="HORAS", tam=120, x=540, y=830, z=0.3,
                  keys=pop(1.85, 4.2)),
          ]})

# 3 · 9.10 – 14.62  LUNA: casi sin atmósfera → ni viento ni lluvia
S.append({"inicio": 9.10, "fin": 14.62, "entrada": "zoom", "dur_entrada": 0.45, "fondo": NOCHE, "vineta": 0.55,
          "camara": {"zoom": [1.0, 1.06], "pan": [[0, 0], [-24, -10]]},
          "elementos": [estrellas, *tierra(840, 1000, 140), suelo_luna(1180, 21, 16),
                        # la Tierra tiene un halo de aire; la Luna no
                        {"tipo": "brillo", "x": 840, "y": 1000, "radio": 260, "color": "#7fc8ff", "intensidad": 0.6,
                         "z": 0.15, "keys": [{"t": 0.8, "op": 0}, {"t": 1.3, "op": 1}, {"t": 2.2, "op": 0.4}]},
                        IMG("huella_bota", ancho=280, x=300, y=1560, ey=0.5, z=0.62),
                        IMG("icono_viento", ancho=330, x=290, y=800, z=0.35, keys=pop(2.55)),
                        IMG("tachado", ancho=330, x=290, y=800, z=0.36, keys=pop(3.3)),
                        IMG("icono_lluvia", ancho=330, x=660, y=800, z=0.35, keys=pop(4.1)),
                        IMG("tachado", ancho=330, x=660, y=800, z=0.36, keys=pop(4.75)),
                        ]})

# 4 · 14.62 – 20.13  ASTRONAUTAS del Apolo: sus huellas siguen ahí
pasos = [(150 + i * 130, 1500 + (24 if i % 2 else -24)) for i in range(7)]
S.append({"inicio": 14.62, "fin": 20.13, "entrada": "desenfoque", "dur_entrada": 0.4, "fondo": NOCHE, "vineta": 0.5,
          "camara": {"zoom": [1.0, 1.0], "pan": [[0, 0], [0, 0]]},
          "elementos": [estrellas, *tierra(), suelo_luna(1150, 33, 18),
                        *[IMG("huella_bota", ancho=110, x=x, y=y, ey=0.45, rot=90, z=0.6,
                              keys=[{"t": 0.25 + i * 0.42, "op": 0}, {"t": 0.32 + i * 0.42, "op": 1}])
                          for i, (x, y) in enumerate(pasos)],
                        IMG("astronauta", ancho=380, y=1200, z=0.65, sombra={"radio": 20, "op": 0.45},
                            anim={"balanceo": [4, 0.84]},
                            keys=[{"t": 0, "x": 60, "ease": "lineal"}, {"t": 3.2, "x": 1000, "ease": "lineal"},
                                  {"t": 3.6, "x": 1400}]),
                        ROT(texto="APOLO", unidad="1969–1972", tam=110, x=540, y=830, z=0.3, keys=pop(1.75, 3.9)),
                        # «Y no es una suposición»: empuje hacia las huellas
                        {"tipo": "brillo", "x": 540, "y": 1500, "radio": 420, "color": "#fff3c4", "intensidad": 0.3,
                         "ey": 0.4, "z": 0.6, "keys": [{"t": 4.0, "op": 0}, {"t": 4.6, "op": 1}]}]})

# 5 · 20.13 – 28.22  2011: la sonda baja a 21 km y fotografía
S.append({"inicio": 20.13, "fin": 28.22, "entrada": "zoom", "dur_entrada": 0.45, "fondo": NOCHE, "vineta": 0.5,
          "camara": {"zoom": [1.0, 1.08], "pan": [[0, 0], [0, 30]]},
          "elementos": [estrellas, *tierra(200, 700, 80), suelo_luna(1500, 44, 14),
                        ROT(texto="2011", tam=120, x=540, y=620, z=0.3, keys=pop(0.25, 1.9)),
                        IMG("sonda", ancho=520, z=0.5, sombra={"radio": 18, "op": 0.35}, anim={"balanceo": [2.5, 3]},
                            keys=[{"t": 0.3, "x": 1400, "y": 900}, {"t": 1.6, "x": 600, "y": 900, "ease": "salida"},
                                  {"t": 3.6, "x": 560, "y": 1080}, {"t": 7.4, "x": 500, "y": 1100}]),
                        {"tipo": "flecha", "puntos": [[560, 1260], [560, 1490]], "grosor": 6, "color": "#ffffffaa",
                         "discontinua": [22, 16], "punta": True, "z": 0.5,
                         "keys": [{"t": 2.7, "progreso": 0, "op": 1}, {"t": 3.3, "progreso": 1}, {"t": 4.9, "op": 0}]},
                        ROT(contar=[50, 21, 1.1], contar_desde=2.2, unidad="KM", tam=120, x=820, y=1380, z=0.4,
                            keys=pop(2.2, 4.9)),
                        # cono de la cámara y fogonazo de la foto
                        F(forma="poligono", puntos=[[-40, 0], [40, 0], [260, 420], [-260, 420]],
                          relleno=["#bfe6ff88", "#bfe6ff00"], x=480, y=1250, z=0.5,
                          keys=[{"t": 5.0, "op": 0}, {"t": 5.3, "op": 1}, {"t": 7.6, "op": 0.8}]),
                        F(forma="rect", ancho=1300, alto=2200, relleno="#ffffff", x=540, y=960, z=0.0,
                          keys=[{"t": 5.3, "op": 0}, {"t": 5.38, "op": 0.85}, {"t": 5.9, "op": 0}])]})

# 6 · 28.22 – 34.30  Vista desde arriba: no se ve cada bota, se ve el rastro
sendero = [[180, 1820], [300, 1560], [520, 1460], [640, 1250], [560, 1020], [760, 860], [980, 820]]
S.append({"inicio": 28.22, "fin": 34.30, "entrada": "zoom", "dur_entrada": 0.45,
          "fondo": {"colores": ["#8f919c", "#6f717c"]}, "vineta": 0.5,
          "camara": {"zoom": [1.0, 1.08], "pan": [[0, 0], [0, -30]]},
          "elementos": [{"tipo": "suelo", "material": "luna", "borde": -150, "ondulacion": 0, "crateres": 26,
                         "z": 0.5, "semilla": 51},
                        {"tipo": "flecha", "puntos": sendero, "grosor": 26, "color": "#3b3d48d0", "punta": False,
                         "z": 0.55, "keys": [{"t": 0.1, "progreso": 0}, {"t": 2.2, "progreso": 1}]},
                        # lupa: dentro no se distinguen las botas
                        {"tipo": "grupo", "ancho": 420, "alto": 560, "z": 0.7,
                         "hijos": [F(forma="circulo", radio=150, relleno="#ffffff", op_relleno=0.08, grosor=16,
                                     borde="#ffffff", sombra={"radio": 10}),
                                   F(forma="redondeado", ancho=40, alto=170, relleno=["#3a3f7a", "#1c1f45"],
                                     x=120, y=200, rot=-40)],
                         "keys": [{"t": 0.9, "x": 1300, "y": 1300, "op": 1}, {"t": 1.6, "x": 600, "y": 1300, "ease": "salida"},
                                  {"t": 2.6, "x": 560, "y": 1150}, {"t": 3.2, "x": 600, "y": 1260}, {"t": 3.6, "op": 0}]},
                        {"tipo": "flecha", "puntos": sendero, "grosor": 36, "color": "#ffd34d", "punta": False, "z": 0.56,
                         "keys": [{"t": 3.2, "progreso": 0, "op": 0.8}, {"t": 4.2, "progreso": 1}]},
                        {"tipo": "brillo", "x": 600, "y": 1300, "radio": 700, "color": "#ffd34d", "intensidad": 0.25,
                         "z": 0.56, "keys": [{"t": 3.3, "op": 0}, {"t": 4.2, "op": 1}]}]})

# 7 · 34.30 – 42.95  ¿Para siempre? Micrometeoritos que liman muy despacio
S.append({"inicio": 34.30, "fin": 42.95, "entrada": "zoom", "dur_entrada": 0.45, "fondo": NOCHE, "vineta": 0.6,
          "camara": {"zoom": [1.0, 1.12], "pan": [[0, 0], [0, -60]], "temblor": 0},
          "elementos": [estrellas, *tierra(), suelo_luna(1000, 61, 22),
                        IMG("huella_bota", ancho=420, x=540, y=1420, ey=0.55, z=0.62),
                        ROT(texto="?", tam=170, x=540, y=830, z=0.3, keys=pop(0.6, 1.4), color="#ffffff"),
                        {"tipo": "particulas", "clase": "lluvia", "color": "#ffe9b0", "area": [0, -100, 1080, 1500],
                         "n": 26, "tam": [2, 3], "vel": [-260, 900], "dispersion": 0.2, "z": 0.7, "semilla": 21,
                         "keys": [{"t": 2.3, "op": 0}, {"t": 2.6, "op": 1}]},
                        {"tipo": "particulas", "clase": "chispas", "color": "#fff3c4",
                         "area": [200, 1250, 880, 1600], "n": 22, "tam": [3, 6], "z": 0.75, "semilla": 22,
                         "keys": [{"t": 2.6, "op": 0}, {"t": 2.9, "op": 1}]},
                        ROT(texto="< 1", unidad="MM", tam=120, x=540, y=830, z=0.3, keys=pop(3.95, 6.1)),
                        # la huella pierde contraste poquísimo
                        F(forma="elipse", ancho=440, alto=480, relleno="#8e909c", desenfoque=30, x=540, y=1420,
                          ey=0.55, z=0.63, keys=[{"t": 5.0, "op": 0}, {"t": 8.6, "op": 0.18}])]})

# 8 · 42.95 – fin  BUCLE: vuelve el plano del principio; la bota vuelve a bajar
S.append({"inicio": 42.95, "fin": 47.2, "entrada": "desenfoque", "dur_entrada": 0.4, "fondo": NOCHE, "vineta": 0.55,
          "camara": {"zoom": [1.10, 1.0], "pan": [[0, -40], [0, 0]]},
          "elementos": [estrellas, *tierra(), suelo_luna(),
                        IMG("huella_bota", ancho=360, x=540, y=1420, ey=0.52, z=0.62),
                        ROT(texto="MILLONES", unidad="DE AÑOS", tam=110, x=540, y=830, z=0.3, keys=pop(2.5)),
                        # la bota asoma arriba en el último segundo, como en el fotograma 0
                        IMG("bota", ancho=520, x=570, z=0.85, sombra={"radio": 24, "op": 0.5},
                            keys=[{"t": 3.39, "op": 0}, {"t": 3.4, "y": 1420 - 1500, "escala": 1.35, "op": 1}, {"t": 4.25, "y": 1420 - 1100,
                                                                                "escala": 1.35, "ease": "entrada"}])]})

ep = {
    "id": "prueba-v2-huellas-luna", "version": 1,
    "audio": os.path.join(SRC, "locucion.mp3"),
    "duracion": 47.2,
    "subtitulos": {"alineacion": os.path.join(SRC, "alineacion.json"), "max_chars": 30},
    "estilo_subtitulos": {"modo": "karaoke", "y": 350, "tam": 62,
                          "claves": ["pisada", "borrado", "atmósfera", "Apolo", "suposición", "NASA",
                                     "veintiún", "rastro", "Tampoco", "millones"]},
    "musica": {"generar": "curiosidad", "semilla": 3, "db": -16},
    "grano": 0.035,
    "escenas": S,
}
with open(os.path.join(AQUI, "episodio.json"), "w", encoding="utf-8") as fh:
    json.dump(ep, fh, ensure_ascii=False, indent=1)
print(os.path.join(AQUI, "episodio.json"))
