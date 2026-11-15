"""01 — La guerra de 38 minutos (Zanzíbar, 1896). Tiempos de la alineación de ElevenLabs."""
from comun import F, guardar, salida, reloj
import math

MAR = {"colores": ["#0d3b66", "#145c8a", "#1d7fa8"]}
CIELO = {"colores": ["#f7c873", "#f2a35e", "#7fb7c9"]}

def palmera(x, y, s=1.0, z=0.4, fase=0):
    return {"tipo": "grupo", "x": x, "y": y, "ancho": 300 * s, "alto": 420 * s, "z": z,
            "anim": {"balanceo": [3, 3.4]}, "fase": fase,
            "hijos": [
                F(forma="redondeado", ancho=22 * s, alto=300 * s, relleno=["#8a5a2b", "#5e3b1a"], y=60 * s, rot=6),
                *[F(forma="elipse", ancho=170 * s, alto=46 * s, relleno=["#3fa34d", "#23702f"], x=dx * s, y=-95 * s + dy * s, rot=r)
                  for dx, dy, r in [(-70, 0, 25), (70, 0, -25), (-55, -25, -20), (55, -25, 20), (0, -35, 90)]],
            ]}

def palacio(x, y, z=0.45, ruinas=False, keys=None):
    piedra = ["#fbf3e2", "#d9c9a8"] if not ruinas else ["#a99f8c", "#6f6656"]
    hijos = [
        F(forma="elipse", ancho=640, alto=60, relleno="#000000", op_relleno=0.3, desenfoque=16, y=250),
        F(forma="rect", ancho=560, alto=330, relleno=piedra, y=80, sombra={"radio": 16, "desplaz": [10, 14]}),
        *[F(forma="redondeado", ancho=60, alto=110, relleno="#5b4630" if not ruinas else "#2e2a24", esquinas=30, x=dx, y=y0)
          for dx in (-200, -100, 0, 100, 200) for y0 in (20, 170)],
        F(forma="rect", ancho=120, alto=360, relleno=piedra, x=0, y=-130),  # torre del reloj
        F(forma="poligono", puntos=[[-80, 0], [80, 0], [0, -90]], relleno=["#c0392b", "#8e2a20"] if not ruinas else ["#6b5a4c", "#4a3f35"], y=-310),
        F(forma="circulo", radio=40, relleno="#fffaf0", grosor=6, borde="#7a5a2e", y=-200),
    ]
    if ruinas:
        hijos += [F(forma="poligono", puntos=[[-90, 40], [-30, -60], [20, 30], [80, -40], [110, 60], [-100, 70]],
                    relleno="#3b352d", x=dx, y=dy) for dx, dy in [(-170, -40), (150, 10), (0, 210)]]
    return {"tipo": "grupo", "x": x, "y": y, "ancho": 700, "alto": 760, "z": z, "keys": keys or [], "hijos": hijos}

def barco(x, y, s=1.0, z=0.6, keys=None, fase=0, humo=True):
    return {"tipo": "grupo", "x": x, "y": y, "ancho": 460 * s, "alto": 280 * s, "z": z, "keys": keys or [],
            "anim": {"balanceo": [2.5, 2.6], "flotar": [6, 2.6]}, "fase": fase,
            "hijos": [
                F(forma="poligono", puntos=[[-200 * s, 0], [200 * s, 0], [160 * s, 60 * s], [-170 * s, 60 * s]],
                  relleno=["#3a3f4b", "#1f232b"], y=60 * s),
                F(forma="rect", ancho=230 * s, alto=50 * s, relleno=["#d8d8d0", "#a8a89e"], y=10 * s),
                F(forma="rect", ancho=34 * s, alto=90 * s, relleno=["#c9a04a", "#8a6a28"], x=-50 * s, y=-50 * s),
                F(forma="rect", ancho=34 * s, alto=90 * s, relleno=["#c9a04a", "#8a6a28"], x=30 * s, y=-50 * s),
                F(forma="redondeado", ancho=150 * s, alto=12 * s, relleno="#2a2a33", x=150 * s, y=0, rot=-8),
            ]}

def humo(x, y, z=0.6, area=140, n=24):
    return {"tipo": "particulas", "clase": "polvo", "color": "#d5d5d0", "area": [x - area / 2, y - 260, x + area / 2, y],
            "n": n, "tam": [10, 26], "vel": [10, -60], "z": z, "semilla": int(x)}

def destello(x, y, t0, z=0.6, r=200, color="#ffd27a"):
    return {"tipo": "brillo", "x": x, "y": y, "radio": r, "color": color, "intensidad": 0.95, "z": z,
            "keys": [{"t": t0, "escala": 0.2, "op": 0}, {"t": t0 + 0.06, "op": 1},
                     {"t": t0 + 0.7, "escala": 1.5, "op": 0, "ease": "salida"}]}

olas = {"tipo": "particulas", "clase": "burbujas", "color": "#bfe7ff", "area": [0, 900, 1080, 1500], "n": 40,
        "tam": [3, 7], "vel": [-30, 0], "z": 0.5, "semilla": 3}
gaviotas = [{"tipo": "flecha", "puntos": [[0, 0], [22, -14], [44, 0], [66, -14], [88, 0]], "grosor": 6, "color": "#ffffff",
             "punta": False, "z": 0.2, "anim": {"deriva": [40, 0], "flotar": [8, 1.6]}, "x": gx, "y": gy}
            for gx, gy in [(-420, -1300), (-120, -1210)]]

# ---------------------------------------------------------------- escenas
e1 = {  # 0 – 3.85: 90 minutos de partido contra 38 de guerra
    "inicio": 0, "fin": 3.85,
    "fondo": {"colores": ["#2f8f46", "#237a3a", "#1a5f2d"]},
    "camara": {"zoom": [1.0, 1.04], "pan": [[0, 0], [0, -20]]}, "vineta": 0.45,
    "elementos": [
        *[F(forma="rect", ancho=1080, alto=110, relleno="#2c8743", y=180 + i * 220, x=540, z=0.3) for i in range(7)],
        F(forma="rect", ancho=900, alto=1500, relleno="#ffffff", op_relleno=0, grosor=10, borde="#ffffffcc", x=540, y=880, z=0.3),
        F(forma="circulo", radio=150, relleno="#ffffff", op_relleno=0, grosor=10, borde="#ffffffcc", x=540, y=880, z=0.3),
        F(forma="rect", ancho=900, alto=10, relleno="#ffffffcc", x=540, y=880, z=0.3),
        {"tipo": "esfera", "radio": 46, "color": "#ffffff", "color2": "#c8c8c8", "textura": "lisa", "giro": 120, "z": 0.5,
         "keys": [{"t": 0, "x": 260, "y": 1250}, {"t": 1.2, "x": 760, "y": 980, "ease": "salida"},
                  {"t": 2.4, "x": 420, "y": 720, "ease": "salida"}, {"t": 3.85, "x": 640, "y": 560}]},
        F(forma="redondeado", ancho=920, alto=300, relleno="#0b1d12", op_relleno=0.55, x=540, y=330, z=0.2, esquinas=40),
        {"tipo": "barra", "x": 540, "y": 270, "ancho": 800, "alto": 56, "color": "#ffffff", "fondo": "#ffffff30", "z": 0.2,
         "keys": [{"t": 0.0, "progreso": 0}, {"t": 2.8, "progreso": 1, "ease": "lineal"}]},
        {"tipo": "barra", "x": 540 - 400 + 400 * 38 / 90, "y": 390, "ancho": 800 * 38 / 90, "alto": 56, "color": "#ff4d4d",
         "fondo": "#00000000", "z": 0.2,
         "keys": [{"t": 1.75, "progreso": 0}, {"t": 2.95, "progreso": 1, "ease": "lineal"}]},
        {"tipo": "brillo", "x": 540 - 400 + 800 * 38 / 90, "y": 390, "radio": 90, "color": "#ff8080", "intensidad": 0.8, "z": 0.2,
         "anim": {"pulso": [0.2, 0.8]}, "keys": [{"t": 2.9, "op": 0}, {"t": 3.1, "op": 1}]},
    ],
}

isla = [[-330, -60], [-250, -170], [-120, -220], [20, -300], [150, -250], [260, -120], [300, 40], [240, 200],
        [120, 300], [-40, 330], [-190, 260], [-300, 130]]
e2 = {  # 3.85 – 8.6: Zanzíbar, 1896
    "inicio": 3.85, "fin": 8.6, "entrada": "barrido",
    "fondo": MAR, "camara": {"zoom": [1.08, 1.0], "pan": [[0, 0], [0, 0]]}, "vineta": 0.5,
    "elementos": [
        {"tipo": "particulas", "clase": "burbujas", "color": "#9fd8ff", "area": [0, 0, 1080, 1920], "n": 70, "tam": [3, 8],
         "vel": [-25, 0], "z": 0.2, "semilla": 9},
        F(forma="poligono", puntos=[[p[0] * 1.15, p[1] * 1.15] for p in isla], relleno="#7fd6e6", op_relleno=0.5, desenfoque=12,
          x=540, y=820, z=0.4, rot=-12),
        F(forma="poligono", puntos=isla, relleno=["#f3dfa2", "#d8bb72"], x=540, y=820, z=0.4, rot=-12, sombra={"radio": 18}),
        F(forma="poligono", puntos=[[p[0] * 0.78, p[1] * 0.78] for p in isla], relleno=["#59b65f", "#2f7f3b"], x=540, y=820, z=0.4, rot=-12),
        palmera(430, 760, 0.55, 0.42), palmera(640, 880, 0.5, 0.42, 1), palmera(560, 640, 0.45, 0.42, 2),
        {"tipo": "grupo", "x": 470, "z": 0.5, "ancho": 120, "alto": 170,
         "keys": [{"t": 0.3, "y": 400, "op": 0}, {"t": 0.4, "op": 1}, {"t": 0.9, "y": 880, "ease": "rebote"}],
         "hijos": [F(forma="poligono", puntos=[[-40, -30], [40, -30], [0, 70]], relleno="#e74c3c", y=10),
                   F(forma="circulo", radio=46, relleno=["#ff6b5b", "#c0392b"], y=-30, brillo=True),
                   F(forma="circulo", radio=18, relleno="#ffffff", y=-30)]},
        {"tipo": "brillo", "x": 470, "y": 940, "radio": 120, "color": "#ffffff", "intensidad": 0.6, "z": 0.5, "ey": 0.4,
         "anim": {"pulso": [0.25, 1.2]}, "keys": [{"t": 0.9, "op": 0}, {"t": 1.1, "op": 1}]},
        # 1896: páginas de calendario que caen
        *[F(forma="redondeado", ancho=150, alto=180, relleno=["#ffffff", "#e8e2d4"], grosor=6, borde="#c0392b", x=880 - i * 30,
            z=0.6, rot=8 - i * 6, sombra={"radio": 10},
            keys=[{"t": 1.4 + i * 0.35, "y": -150, "op": 1}, {"t": 2.1 + i * 0.35, "y": 260 + i * 25, "ease": "rebote"}])
          for i in range(3)],
    ],
}

coronita = lambda **k: {"tipo": "grupo", "ancho": 140, "alto": 100, **k,
                        "hijos": [F(forma="poligono", puntos=[[-60, 40], [60, 40], [66, -30], [30, 0], [0, -44], [-30, 0], [-66, -30]],
                                    relleno=["#ffe07a", "#d49b16"], brillo=True),
                                  *[F(forma="circulo", radio=9, relleno="#e74c3c", x=dx, y=24) for dx in (-30, 0, 30)]]}

e3 = {  # 8.6 – 15.5: muere el sultán y Jalid entra en el palacio
    "inicio": 8.6, "fin": 15.5, "entrada": "fundido",
    "fondo": CIELO, "camara": {"zoom": [1.0, 1.05], "pan": [[0, 0], [0, -30]]}, "vineta": 0.35,
    "elementos": [
        {"tipo": "brillo", "x": 820, "y": 260, "radio": 380, "color": "#fff1c0", "intensidad": 0.7, "z": 0.05},
        {"tipo": "suelo", "material": "arena", "borde": 1120, "ondulacion": 10, "z": 0.5, "semilla": 5},
        palacio(540, 830),
        palmera(120, 900, 0.9, 0.55), palmera(970, 920, 0.85, 0.55, 1.5),
        # corona del sultán que se apaga
        coronita(x=540, y=330, z=0.45, keys=[{"t": 0, "op": 1, "escala": 1.2}, {"t": 1.5, "op": 1},
                                              {"t": 2.2, "op": 0.0, "y": 420, "escala": 0.8}]),
        {"tipo": "persona", "alto": 300, "ropa": "#f4f1ea", "pelo": "#1a1410", "piel": "#9a6a45", "z": 0.6, "y": 1100,
         "brazo_i": 14, "brazo_d": 14,
         "keys": [{"t": 2.4, "x": -120, "paso": 1.0, "ease": "lineal"}, {"t": 5.0, "x": 540, "paso": 1.0},
                  {"t": 5.2, "paso": 0}, {"t": 5.6, "brazo_d": 14}, {"t": 6.0, "brazo_d": 150}]},
        coronita(z=0.6, keys=[{"t": 5.0, "x": 540, "y": 700, "op": 0}, {"t": 5.3, "op": 1},
                              {"t": 5.9, "y": 1015, "ease": "rebote"}]),
        # los británicos, al fondo, no lo aprueban
        {"tipo": "persona", "alto": 240, "ropa": "#b33a3a", "pelo": "#c9a36b", "z": 0.55, "x": 930, "y": 1180,
         "keys": [{"t": 4.5, "op": 0}, {"t": 5.0, "op": 1}, {"t": 5.2, "brazo_i": 12}, {"t": 5.8, "brazo_i": 100}]},
        F(forma="circulo", radio=60, relleno="#ffffffdd", grosor=8, borde="#e74c3c", x=930, y=920, z=0.6,
          keys=[{"t": 5.6, "escala": 0, "ease": "rebote"}, {"t": 6.0, "escala": 1}]),
        F(forma="redondeado", ancho=100, alto=14, relleno="#e74c3c", x=930, y=920, rot=-45, z=0.6,
          keys=[{"t": 5.8, "escala": 0}, {"t": 6.1, "escala": 1, "ease": "rebote"}]),
    ],
}

flota = [barco(260, 1300, 0.95, fase=0), barco(760, 1360, 1.05, fase=1.1), barco(520, 1230, 0.75, z=0.55, fase=0.5)]
e4 = {  # 15.5 – 21.0: ultimátum y atrincheramiento
    "inicio": 15.5, "fin": 21.0, "entrada": "barrido",
    "fondo": {"colores": ["#f2b56b", "#e9925a", "#2a6f97"]},
    "camara": {"zoom": [1.0, 1.04], "pan": [[0, 0], [0, 10]]}, "vineta": 0.4,
    "elementos": [
        {"tipo": "brillo", "x": 200, "y": 300, "radio": 360, "color": "#fff1c0", "intensidad": 0.6, "z": 0.05},
        F(forma="rect", ancho=1100, alto=260, relleno=["#e8d29a", "#cdb170"], x=540, y=830, z=0.4),
        palacio(540, 560, z=0.4),
        {"tipo": "agua", "lado": "abajo", "z": 0.5, "amplitud": 18, "colores": ["#1d6fa1", "#5cc3d9"],
         "keys": [{"t": 0, "nivel": 940}, {"t": 5.5, "nivel": 960}]},
        olas, *flota,
        # el ultimátum: un papel que vuela del barco al palacio
        {"tipo": "grupo", "ancho": 200, "alto": 240, "z": 0.7,
         "keys": [{"t": 0.0, "x": 760, "y": 1250, "escala": 0.4, "rot": -10}, {"t": 1.3, "x": 540, "y": 520, "escala": 1.4, "rot": 8, "ease": "suave"},
                  {"t": 3.6, "x": 540, "y": 520, "escala": 1.4}, {"t": 4.0, "escala": 0.0, "op": 0}],
         "hijos": [F(forma="redondeado", ancho=170, alto=210, relleno=["#fff7e0", "#e7d6ad"], esquinas=10, sombra={"radio": 12}),
                   *[F(forma="redondeado", ancho=110, alto=10, relleno="#8a7350", y=-60 + i * 28) for i in range(4)],
                   F(forma="circulo", radio=22, relleno="#c0392b", y=72)]},
        # o te vas (flecha que sale) / o disparamos (punto de mira)
        {"tipo": "flecha", "puntos": [[620, 520], [800, 470], [960, 420]], "grosor": 18, "color": "#ffffff", "contorno": "#00000055",
         "z": 0.75, "keys": [{"t": 2.1, "progreso": 0, "op": 1}, {"t": 2.6, "progreso": 1}, {"t": 3.6, "op": 0}]},
        F(forma="circulo", radio=110, relleno="#ffffff", op_relleno=0, grosor=10, borde="#ff4d4d", x=540, y=560, z=0.75,
          keys=[{"t": 2.8, "escala": 2.0, "op": 0}, {"t": 3.2, "escala": 1.0, "op": 1, "ease": "entrada"}, {"t": 5.5, "op": 1}]),
        F(forma="rect", ancho=280, alto=8, relleno="#ff4d4d", x=540, y=560, z=0.75, keys=[{"t": 2.8, "op": 0}, {"t": 3.2, "op": 1}]),
        F(forma="rect", ancho=8, alto=280, relleno="#ff4d4d", x=540, y=560, z=0.75, keys=[{"t": 2.8, "op": 0}, {"t": 3.2, "op": 1}]),
        # se atrinchera: sacos que se apilan delante del palacio
        *[F(forma="redondeado", ancho=110, alto=56, relleno=["#c2a26b", "#8d7244"], x=300 + (i % 5) * 120 + (60 if i >= 5 else 0),
            z=0.45, sombra={"radio": 6}, esquinas=26,
            keys=[{"t": 4.2 + i * 0.1, "y": 600, "op": 0}, {"t": 4.5 + i * 0.1, "y": 880 if i < 5 else 830, "op": 1, "ease": "rebote"}])
          for i in range(9)],
    ],
}

disparos = [(t, bx) for t, bx in [(1.6, 300), (1.9, 790), (2.3, 540), (2.8, 300), (3.2, 790), (3.6, 540), (4.1, 300), (4.5, 790)]]
e5 = {  # 21.0 – 26.35: pasadas las nueve, fuego
    "inicio": 21.0, "fin": 26.35, "entrada": "corte",
    "fondo": {"colores": ["#e9925a", "#c8643f", "#1f5c85"]},
    "camara": {"zoom": [1.0, 1.03], "pan": [[0, 0], [0, 0]], "temblor": 5}, "vineta": 0.5,
    "elementos": [
        F(forma="rect", ancho=1100, alto=260, relleno=["#e8d29a", "#cdb170"], x=540, y=830, z=0.4),
        palacio(540, 560, z=0.4),
        {"tipo": "agua", "lado": "abajo", "z": 0.5, "amplitud": 18, "colores": ["#1d6fa1", "#5cc3d9"], "nivel": 950},
        olas, *flota,
        reloj(870, 230, 120, 0, 3, 0, 5.3, z=0.3, keys=[{"t": 0, "escala": 0, "ease": "rebote"}, {"t": 0.5, "escala": 1}]),
        *[{"tipo": "flecha", "puntos": [[bx + 140, 1240], [(bx + 540) / 2 + 70, 820], [540 + (bx - 540) * 0.3, 600]], "grosor": 10,
           "color": "#fff1a8", "punta": False, "z": 0.65,
           "keys": [{"t": t, "progreso": 0, "op": 1}, {"t": t + 0.35, "progreso": 1}, {"t": t + 0.7, "op": 0}]}
          for t, bx in disparos],
        *[destello(bx + 140, 1240, t, r=110, z=0.65) for t, bx in disparos],
        *[destello(540 + (bx - 540) * 0.3, 600, t + 0.35, r=230, color="#ff9a4d", z=0.66) for t, bx in disparos],
        humo(540, 560, z=0.5, area=520, n=40),
    ],
}

e6 = {  # 26.35 – 31.5: a las nueve y cuarenta, silencio y ruinas
    "inicio": 26.35, "fin": 31.5, "entrada": "fundido",
    "fondo": {"colores": ["#8a8f96", "#6b6f75", "#2f4f66"]},
    "camara": {"zoom": [1.0, 1.06], "pan": [[0, 0], [0, -20]]}, "vineta": 0.55,
    "elementos": [
        F(forma="rect", ancho=1100, alto=260, relleno=["#b8a77e", "#968559"], x=540, y=1130, z=0.4),
        palacio(540, 860, z=0.4, ruinas=True),
        humo(400, 700, z=0.45, area=200, n=30), humo(700, 760, z=0.45, area=180, n=26),
        {"tipo": "agua", "lado": "abajo", "z": 0.5, "amplitud": 10, "colores": ["#3a6f8f", "#6aa9bf"], "nivel": 1260},
        reloj(540, 330, 190, 3, 40, 0.0, 1.6, z=0.3),
        {"tipo": "brillo", "x": 540, "y": 330, "radio": 300, "color": "#ffe9a8", "intensidad": 0.5, "z": 0.3,
         "keys": [{"t": 1.4, "op": 0}, {"t": 1.8, "op": 1}, {"t": 3.0, "op": 0.3}]},
    ],
}

e7 = {  # 31.5 – 33.55: unos treinta y ocho minutos
    "inicio": 31.5, "fin": 33.55, "entrada": "corte",
    "fondo": {"tipo": "radial", "colores": ["#3a2a1e", "#1a120c"]},
    "camara": {"zoom": [1.0, 1.05], "pan": [[0, 0], [0, 0]]}, "vineta": 0.5,
    "elementos": [
        {"tipo": "rayos", "x": 540, "y": 800, "n": 14, "longitud": 900, "apertura": 8, "intensidad": 0.25, "color": "#ffd27a",
         "anim": {"girar": 10}, "z": 0.1},
        reloj(540, 800, 300, 0, 38, 0.1, 1.6, z=0.3),
        {"tipo": "particulas", "clase": "chispas", "color": "#ffd27a", "area": [140, 400, 940, 1200], "n": 40, "tam": [2, 5],
         "vel": [0, -40], "z": 0.5, "semilla": 4},
    ],
}

# 500 contra 1: balanza
puntos = [F(forma="circulo", radio=7, relleno="#ff6b5b", x=-150 + (i % 20) * 16, y=-10 - (i // 20) * 16) for i in range(500)]
e8 = {  # 33.55 – 40.45: balance desigual
    "inicio": 33.55, "fin": 40.45, "entrada": "barrido",
    "fondo": {"colores": ["#1b2433", "#243248", "#33435c"]},
    "camara": {"zoom": [1.0, 1.04], "pan": [[0, 0], [0, -10]]}, "vineta": 0.45,
    "elementos": [
        {"tipo": "particulas", "clase": "polvo", "color": "#9fb3cc", "area": [0, 0, 1080, 1500], "n": 40, "tam": [2, 4],
         "vel": [8, -12], "z": 0.1, "semilla": 2},
        F(forma="poligono", puntos=[[-30, -380], [30, -380], [90, 380], [-90, 380]], relleno=["#c9a04a", "#7a5a20"], x=540, y=1010, z=0.4,
          sombra={"radio": 14}),
        {"tipo": "grupo", "x": 540, "y": 640, "ancho": 1080, "alto": 900, "z": 0.45,
         "keys": [{"t": 0, "rot": 0}, {"t": 1.9, "rot": 0}, {"t": 3.2, "rot": -14, "ease": "rebote"}],
         "hijos": [
             F(forma="redondeado", ancho=700, alto=26, relleno=["#e3c066", "#a77f2a"]),
             F(forma="circulo", radio=30, relleno=["#ffe07a", "#b8860b"]),
             # plato izquierdo con 500 puntos
             {"tipo": "grupo", "x": -330, "y": 210, "ancho": 380, "alto": 420,
              "hijos": [F(forma="rect", ancho=4, alto=220, relleno="#a77f2a", x=-150, y=-100, rot=-20),
                        F(forma="rect", ancho=4, alto=220, relleno="#a77f2a", x=150, y=-100, rot=20),
                        *[dict(p, keys=[{"t": 0.3 + (i // 20) * 0.06, "op": 0, "escala": 0}, {"t": 0.5 + (i // 20) * 0.06, "op": 1, "escala": 1}])
                          for i, p in enumerate(puntos)],
                        F(forma="elipse", ancho=340, alto=40, relleno=["#e3c066", "#a77f2a"], y=10)]},
             # plato derecho con uno solo
             {"tipo": "grupo", "x": 330, "y": 210, "ancho": 380, "alto": 420,
              "hijos": [F(forma="rect", ancho=4, alto=220, relleno="#a77f2a", x=-150, y=-100, rot=-20),
                        F(forma="rect", ancho=4, alto=220, relleno="#a77f2a", x=150, y=-100, rot=20),
                        F(forma="circulo", radio=12, relleno="#5dade2", y=-12,
                          keys=[{"t": 4.2, "escala": 0, "op": 0}, {"t": 4.6, "escala": 1.0, "op": 1, "ease": "rebote"}]),
                        F(forma="elipse", ancho=340, alto=40, relleno=["#e3c066", "#a77f2a"], y=10)]},
         ]},
        {"tipo": "brillo", "x": 540, "y": 640, "radio": 600, "color": "#ffe9a8", "intensidad": 0.18, "z": 0.3},
    ],
}

e9 = {  # 40.45 – fin: nuevo sultán elegido por Londres
    "inicio": 40.45, "fin": 45.2, "entrada": "fundido",
    "fondo": CIELO, "camara": {"zoom": [1.0, 1.05], "pan": [[0, 0], [0, -20]]}, "vineta": 0.35,
    "elementos": [
        {"tipo": "brillo", "x": 820, "y": 260, "radio": 380, "color": "#fff1c0", "intensidad": 0.7, "z": 0.05},
        *gaviotas,
        {"tipo": "suelo", "material": "arena", "borde": 1120, "ondulacion": 10, "z": 0.5, "semilla": 5},
        palacio(540, 830, ruinas=True),
        humo(540, 700, z=0.45, area=300, n=16),
        {"tipo": "persona", "alto": 300, "ropa": "#2f5aa8", "pelo": "#1a1410", "piel": "#9a6a45", "z": 0.6, "x": 540, "y": 1100,
         "keys": [{"t": 0, "op": 0}, {"t": 0.4, "op": 1}, {"t": 2.4, "brazo_i": 12, "brazo_d": 12}, {"t": 3.0, "brazo_i": 60, "brazo_d": 60}]},
        coronita(z=0.6, keys=[{"t": 0.6, "x": 540, "y": 600, "op": 0}, {"t": 0.9, "op": 1},
                              {"t": 1.6, "y": 1015, "ease": "rebote"}]),
        # mano británica que señala desde el barco
        barco(900, 1260, 0.9, z=0.62, fase=0.4),
        {"tipo": "flecha", "puntos": [[860, 1180], [760, 1080], [620, 1030]], "grosor": 14, "color": "#ffffff", "contorno": "#00000055",
         "z": 0.7, "keys": [{"t": 2.6, "progreso": 0}, {"t": 3.3, "progreso": 1}]},
    ],
}

ep = {
    "id": "2026-11-15-tarde-01-guerra-38-minutos", "version": 1,
    "audio": "01-locucion.mp3",
    "subtitulos": {"alineacion": "01-alineacion-original.json", "max_chars": 26},
    "estilo_subtitulos": {"y": 1600, "tam": 60},
    "escenas": [e1, e2, e3, e4, e5, e6, e7, e8, e9],
}
guardar(ep, salida())
