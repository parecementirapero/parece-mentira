"""03 — Los moáis no son solo cabezas. Tiempos de la alineación de ElevenLabs."""
from comun import F, guardar, salida

CIELO = {"colores": ["#7cc3e8", "#b6e0f0", "#f4e3b5"]}
PIEDRA = ["#8a7d6e", "#5d5247"]

def moai(x, y, s=1.0, z=0.5, espalda=False, keys=None, anim=None, grabados_t=None):
    """Moái con el origen en la barbilla: la cabeza ocupa de -400·s a 0 y el torso de 0 a 520·s."""
    S = lambda v: v * s
    oscuro = "#3f362e"
    h = [
        # torso
        F(forma="redondeado", ancho=S(300), alto=S(540), relleno=PIEDRA, esquinas=S(60), y=S(260)),
        # cabeza
        F(forma="poligono", puntos=[[S(-112), S(-400)], [S(112), S(-400)], [S(128), S(-10)], [S(-128), S(-10)]], relleno=PIEDRA, y=S(-205) + S(205)),
        F(forma="redondeado", ancho=S(46), alto=S(220), relleno="#6f6357", esquinas=S(20), x=S(-140), y=S(-190)),
        F(forma="redondeado", ancho=S(46), alto=S(220), relleno="#6f6357", esquinas=S(20), x=S(140), y=S(-190)),
    ]
    if not espalda:
        h += [
            F(forma="redondeado", ancho=S(250), alto=S(46), relleno="#4c433a", esquinas=S(14), y=S(-280)),
            F(forma="elipse", ancho=S(70), alto=S(40), relleno=oscuro, x=S(-55), y=S(-238)),
            F(forma="elipse", ancho=S(70), alto=S(40), relleno=oscuro, x=S(55), y=S(-238)),
            F(forma="poligono", puntos=[[0, S(-110)], [S(42), S(95)], [S(-42), S(95)]], relleno=["#94877a", "#6a5e52"], y=S(-150)),
            F(forma="redondeado", ancho=S(130), alto=S(18), relleno=oscuro, esquinas=S(8), y=S(-50)),
            # brazos tallados y manos sobre el vientre
            F(forma="redondeado", ancho=S(18), alto=S(330), relleno="#4c433a", esquinas=S(9), x=S(-118), y=S(190)),
            F(forma="redondeado", ancho=S(18), alto=S(330), relleno="#4c433a", esquinas=S(9), x=S(118), y=S(190)),
            F(forma="redondeado", ancho=S(110), alto=S(18), relleno="#4c433a", esquinas=S(9), x=S(-68), y=S(355)),
            F(forma="redondeado", ancho=S(110), alto=S(18), relleno="#4c433a", esquinas=S(9), x=S(68), y=S(355)),
        ]
    else:
        gk = (lambda i: [{"t": grabados_t + i * 0.25, "op": 0}, {"t": grabados_t + 0.3 + i * 0.25, "op": 1}]) if grabados_t is not None else (lambda i: [])
        h += [
            F(forma="circulo", radio=S(46), relleno="#ffffff", op_relleno=0, grosor=S(10), borde="#e9d9b8", y=S(80), keys=gk(0)),
            F(forma="circulo", radio=S(20), relleno="#ffffff", op_relleno=0, grosor=S(8), borde="#e9d9b8", y=S(80), keys=gk(0)),
            F(forma="poligono", puntos=[[S(-90), 0], [0, S(-40)], [S(90), 0]], relleno="#ffffff", op_relleno=0, grosor=S(10),
              borde="#e9d9b8", y=S(220), keys=gk(1)),
            F(forma="redondeado", ancho=S(200), alto=S(12), relleno="#e9d9b8", esquinas=S(6), y=S(300), keys=gk(2)),
            F(forma="redondeado", ancho=S(12), alto=S(140), relleno="#e9d9b8", esquinas=S(6), y=S(400), keys=gk(3)),
        ]
    g = {"tipo": "grupo", "x": x, "y": y, "ancho": S(380), "alto": S(1100), "z": z, "keys": keys or [], "hijos": h}
    if anim: g["anim"] = anim
    return g

def ladera(borde, z=0.5, color=("#6db35a", "#3f7f3a"), alto=1100):
    return F(forma="rect", ancho=1300, alto=alto, relleno=list(color), x=540, y=borde + alto / 2, z=z)

def estratos(borde, z=0.6, op=0.88, keys=None, alto=1100):
    """Tierra cortada en capas (vista en sección)."""
    capas = ["#8a6a45", "#7a5c3b", "#6b4f33", "#5d442c", "#503a26"]
    out = [F(forma="rect", ancho=1300, alto=alto, relleno=["#8a6a45", "#4a3423"], op_relleno=op, x=540, y=borde + alto / 2, z=z,
             keys=keys or [])]
    out += [F(forma="rect", ancho=1300, alto=6, relleno="#3a2a1c", op_relleno=0.5, x=540, y=borde + 90 + i * 110, z=z, keys=keys or [])
            for i in range(len(capas))]
    return out

hierba = {"tipo": "particulas", "clase": "polvo", "color": "#a7e08a", "area": [0, 900, 1080, 1500], "n": 40, "tam": [2, 4],
          "vel": [20, -6], "z": 0.7, "semilla": 5}
nubes = [F(forma="elipse", ancho=w, alto=w * 0.35, relleno="#ffffff", op_relleno=0.85, desenfoque=10, y=yy, z=0.1,
           x=xx, anim={"deriva": [18, 0]}) for xx, yy, w in [(180, 260, 300), (760, 380, 360), (520, 160, 220)]]

# ---------------------------------------------------------------- escenas
e1 = {  # 0 – 4.55: si crees que son solo cabezas...
    "inicio": 0, "fin": 4.55,
    "fondo": CIELO, "camara": {"zoom": [1.0, 1.06], "pan": [[0, 0], [0, -30]]}, "vineta": 0.35,
    "elementos": [
        *nubes,
        moai(540, 1150, 1.25, z=0.45),
        ladera(1150, z=0.5),
        hierba,
        # ojo que parpadea: lo que ves engaña
        {"tipo": "grupo", "x": 860, "y": 360, "ancho": 260, "alto": 160, "z": 0.6,
         "keys": [{"t": 2.9, "escala": 0, "ease": "rebote"}, {"t": 3.3, "escala": 1}, {"t": 3.8, "ey": 1}, {"t": 3.9, "ey": 0.1}, {"t": 4.0, "ey": 1}],
         "hijos": [F(forma="elipse", ancho=240, alto=130, relleno="#ffffff", grosor=8, borde="#2a2a33"),
                   F(forma="circulo", radio=44, relleno=["#5aa0d8", "#2c5f8a"]), F(forma="circulo", radio=20, relleno="#111111")]},
    ],
}

pista = lambda t0: F(forma="circulo", radio=70, relleno=["#ffe07a", "#d49b16"], grosor=8, borde="#ffffff", x=150, y=220, z=0.7,
                     brillo=True, keys=[{"t": t0, "escala": 0, "ease": "rebote"}, {"t": t0 + 0.4, "escala": 1}])
lupa_icono = lambda t0: {"tipo": "grupo", "x": 150, "y": 220, "ancho": 140, "alto": 140, "z": 0.72,
                         "keys": [{"t": t0 + 0.2, "escala": 0}, {"t": t0 + 0.5, "escala": 1, "ease": "rebote"}],
                         "hijos": [F(forma="redondeado", ancho=14, alto=50, relleno="#5a3d0e", x=22, y=22, rot=-45),
                                   F(forma="circulo", radio=24, relleno="#ffffff", op_relleno=0.4, grosor=8, borde="#5a3d0e", x=-6, y=-6)]}
cabezas = [(120, 1000, 0.42), (330, 930, 0.38), (560, 1010, 0.45), (780, 950, 0.4), (980, 1030, 0.44),
           (220, 1230, 0.55), (470, 1190, 0.6), (730, 1250, 0.58), (950, 1210, 0.5)]
e2 = {  # 4.55 – 11.8: primera pista, ciento cincuenta cabezas en la ladera
    "inicio": 4.55, "fin": 11.8, "entrada": "barrido",
    "fondo": CIELO, "camara": {"zoom": [1.0, 1.05], "pan": [[0, 0], [-30, -20]]}, "vineta": 0.4,
    "elementos": [
        *nubes,
        F(forma="poligono", puntos=[[-700, 300], [-200, -260], [200, -260], [700, 300]], relleno=["#6f9e58", "#4c7d3e"], x=540, y=720, z=0.3),
        F(forma="elipse", ancho=400, alto=60, relleno="#3f6a34", x=540, y=465, z=0.3),
        *[dict(moai(x, y, s, z=0.45), keys=[{"t": 0.6 + i * 0.25, "op": 0, "y": y + 120 * s}, {"t": 1.0 + i * 0.25, "op": 1, "y": y, "ease": "salida"}])
          for i, (x, y, s) in enumerate(cabezas[:5])],
        ladera(1000, z=0.46, color=("#7cc066", "#4f8f44")),
        *[dict(moai(x, y, s, z=0.55), keys=[{"t": 1.9 + i * 0.25, "op": 0, "y": y + 120 * s}, {"t": 2.3 + i * 0.25, "op": 1, "y": y, "ease": "salida"}])
          for i, (x, y, s) in enumerate(cabezas[5:])],
        ladera(1220, z=0.56, color=("#86c96f", "#4f8f44")),
        hierba, pista(0.1), lupa_icono(0.1),
    ],
}

e3 = {  # 11.8 – 17.1: segunda pista, 1914: alguien empieza a cavar
    "inicio": 11.8, "fin": 17.1, "entrada": "barrido",
    "fondo": {"colores": ["#e9c27c", "#e8d6a6", "#c9b48a"]}, "camara": {"zoom": [1.0, 1.04], "pan": [[0, 0], [0, -10]]}, "vineta": 0.45,
    "elementos": [
        *nubes,
        moai(560, 1000, 1.0, z=0.45),
        ladera(1000, z=0.5, color=("#9cba6a", "#6d8a45")),
        # hoyo que se agranda
        F(forma="elipse", ancho=360, alto=90, relleno="#4a3423", x=560, y=1030, z=0.52,
          keys=[{"t": 2.0, "escala": 0.2}, {"t": 5.2, "escala": 1.0}]),
        {"tipo": "persona", "alto": 300, "ropa": "#8a7350", "pelo": "#3b2a1c", "z": 0.6, "x": 860, "y": 1060,
         "keys": [{"t": 0, "op": 0, "x": 1100}, {"t": 1.2, "op": 1, "x": 860, "paso": 1.0}, {"t": 1.4, "paso": 0},
                  *[k for i in range(6) for k in ({"t": 2.0 + i * 0.5, "brazo_i": 140, "brazo_d": 140}, {"t": 2.25 + i * 0.5, "brazo_i": 40, "brazo_d": 40})]]},
        F(forma="redondeado", ancho=16, alto=220, relleno="#6b4a2a", x=760, y=1030, z=0.61, rot=-30,
          keys=[{"t": 1.2, "op": 0}, {"t": 1.5, "op": 1}, *[k for i in range(6) for k in ({"t": 2.0 + i * 0.5, "rot": -55}, {"t": 2.25 + i * 0.5, "rot": -20})]]),
        {"tipo": "particulas", "clase": "chispas", "color": "#7a5c3b", "area": [620, 880, 820, 1040], "n": 24, "tam": [5, 9],
         "vel": [60, -80], "z": 0.62, "semilla": 3, "keys": [{"t": 2.0, "op": 0}, {"t": 2.3, "op": 1}]},
        pista(0.0), lupa_icono(0.0),
        # páginas del calendario que pasan (1914)
        *[F(forma="redondeado", ancho=140, alto=170, relleno=["#ffffff", "#e8e2d4"], grosor=6, borde="#2c5f8a", x=900 - i * 26,
            z=0.7, rot=8 - i * 6, sombra={"radio": 10},
            keys=[{"t": 0.8 + i * 0.3, "y": -150}, {"t": 1.4 + i * 0.3, "y": 230 + i * 20, "ease": "rebote"}])
          for i in range(3)],
    ],
}

e4 = {  # 17.1 – 24.3: debajo hay un torso entero; la erosión lo fue enterrando
    "inicio": 17.1, "fin": 24.3, "entrada": "fundido",
    "fondo": CIELO, "camara": {"zoom": [1.0, 1.04], "pan": [[0, 0], [0, -20]]}, "vineta": 0.35,
    "elementos": [
        *nubes,
        F(forma="rect", ancho=1300, alto=1200, relleno=["#4a3726", "#2a1d12"], x=540, y=780 + 600, z=0.44),
        moai(540, 760, 1.15, z=0.45),
        # la tierra se vuelve transparente: aparece el torso
        *estratos(780, z=0.5, keys=[{"t": 0, "op": 1}, {"t": 1.6, "op": 0.35}, {"t": 3.6, "op": 0.35}]),
        F(forma="rect", ancho=1300, alto=40, relleno=["#7cc066", "#4f8f44"], x=540, y=780, z=0.51),
        {"tipo": "brillo", "x": 540, "y": 1030, "radio": 360, "color": "#fff1c0", "intensidad": 0.5, "z": 0.52,
         "keys": [{"t": 1.2, "op": 0}, {"t": 2.0, "op": 1}, {"t": 3.6, "op": 0}]},
        # erosión: capas que caen y lo vuelven a cubrir hasta los hombros
        {"tipo": "particulas", "clase": "lluvia", "color": "#8a6a45", "area": [0, 0, 1080, 760], "n": 50, "tam": [4, 6],
         "vel": [10, 380], "z": 0.55, "semilla": 6, "keys": [{"t": 3.6, "op": 0}, {"t": 4.0, "op": 1}]},
        {"tipo": "flecha", "puntos": [[880, 300], [880, 520], [880, 700]], "grosor": 16, "color": "#ffffff", "contorno": "#00000055",
         "z": 0.6, "keys": [{"t": 3.8, "progreso": 0}, {"t": 4.5, "progreso": 1}]},
        {"tipo": "flecha", "puntos": [[200, 300], [200, 520], [200, 700]], "grosor": 16, "color": "#ffffff", "contorno": "#00000055",
         "z": 0.6, "keys": [{"t": 4.0, "progreso": 0}, {"t": 4.7, "progreso": 1}]},
    ],
}

e5 = {  # 24.3 – 32.2: 2010-2014, Van Tilburg desentierra dos y halla grabados en la espalda
    "inicio": 24.3, "fin": 32.2, "entrada": "barrido",
    "fondo": {"colores": ["#e9c27c", "#e8d6a6", "#c9b48a"]}, "camara": {"zoom": [1.0, 1.05], "pan": [[0, 0], [0, -20]]}, "vineta": 0.45,
    "elementos": [
        *nubes,
        moai(340, 640, 0.85, z=0.45), moai(760, 680, 0.85, z=0.45, espalda=True, grabados_t=4.3),
        # zanjas: el suelo baja y deja ver los cuerpos
        *estratos(700, z=0.5, op=0.97, keys=[{"t": 0.0, "y": 700 + 550}, {"t": 3.4, "y": 1150 + 550, "ease": "suave"}]),
        F(forma="rect", ancho=1300, alto=40, relleno=["#9cba6a", "#6d8a45"], x=540, z=0.51,
          keys=[{"t": 0.0, "y": 700}, {"t": 3.4, "y": 1150, "ease": "suave"}]),
        {"tipo": "particulas", "clase": "polvo", "color": "#c7a77a", "area": [100, 700, 980, 1200], "n": 30, "tam": [4, 8],
         "vel": [15, -40], "z": 0.55, "semilla": 8},
        *[F(forma="redondeado", ancho=14, alto=220, relleno="#6b4a2a", x=x, y=1120, rot=r, z=0.58)
          for x, r in [(150, 20), (960, -20)]],
        {"tipo": "brillo", "x": 760, "y": 900, "radio": 260, "color": "#fff1c0", "intensidad": 0.7, "z": 0.5,
         "anim": {"pulso": [0.15, 1.2]}, "keys": [{"t": 4.2, "op": 0}, {"t": 4.8, "op": 1}]},
        {"tipo": "grupo", "ancho": 420, "alto": 420, "z": 0.6,
         "keys": [{"t": 4.6, "x": 900, "y": 1000, "escala": 0}, {"t": 5.0, "escala": 1, "ease": "rebote"}, {"t": 7.9, "x": 780, "y": 880}],
         "hijos": [F(forma="redondeado", ancho=50, alto=190, relleno=["#4b3b6b", "#2a2140"], x=120, y=120, rot=-45),
                   F(forma="circulo", radio=130, relleno="#e8f6ff", op_relleno=0.16, grosor=18, borde="#f2f4fb", brillo=True)]},
    ],
}

fila = [(90 + i * 112, 1030, 0.34) for i in range(9)]
e6 = {  # 32.2 – 36.0: casi mil moáis; algunos de diez metros
    "inicio": 32.2, "fin": 36.0, "entrada": "fundido",
    "fondo": {"colores": ["#f2a35e", "#f7c873", "#b6e0f0"]}, "camara": {"zoom": [1.0, 1.04], "pan": [[0, 0], [20, 0]]}, "vineta": 0.4,
    "elementos": [
        {"tipo": "brillo", "x": 900, "y": 400, "radio": 420, "color": "#fff1c0", "intensidad": 0.6, "z": 0.05},
        F(forma="rect", ancho=1300, alto=80, relleno=["#2f6f8f", "#2a5f7a"], x=540, y=880, z=0.3),
        *[dict(moai(x, y - 175, s, z=0.4), keys=[{"t": 0.1 + i * 0.12, "op": 0, "escala": 0.6}, {"t": 0.4 + i * 0.12, "op": 1, "escala": 1}])
          for i, (x, y, s) in enumerate(fila)],
        F(forma="rect", ancho=1300, alto=60, relleno=["#9a8f80", "#6f6556"], x=540, y=1050, z=0.42),
        F(forma="rect", ancho=1300, alto=900, relleno=["#86c96f", "#4f8f44"], x=540, y=1530, z=0.45),
        # escala: un moái de diez metros junto a una persona
        dict(moai(400, 1000, 0.9, z=0.5), keys=[{"t": 1.9, "op": 0, "y": 1200}, {"t": 2.4, "op": 1, "y": 1000, "ease": "salida"}]),
        {"tipo": "persona", "alto": 130, "ropa": "#c0392b", "z": 0.52, "x": 720, "y": 1400,
         "keys": [{"t": 2.4, "op": 0}, {"t": 2.7, "op": 1}, {"t": 3.0, "brazo_d": 150}]},
        {"tipo": "flecha", "puntos": [[600, 1470], [600, 1060], [600, 650]], "grosor": 10, "color": "#ffffff", "contorno": "#00000055",
         "z": 0.55, "keys": [{"t": 2.5, "progreso": 0}, {"t": 3.3, "progreso": 1}]},
    ],
}

e7 = {  # 36.0 – fin: lo que asoma es solo la mitad
    "inicio": 36.0, "fin": 38.95, "entrada": "fundido",
    "fondo": CIELO, "camara": {"zoom": [1.0, 1.08], "pan": [[0, 0], [0, 20]]}, "vineta": 0.4,
    "elementos": [
        *nubes,
        F(forma="rect", ancho=1300, alto=1200, relleno=["#4a3726", "#2a1d12"], x=540, y=780 + 600, z=0.44),
        moai(540, 760, 1.15, z=0.45),
        *estratos(780, z=0.5, op=0.45),
        F(forma="rect", ancho=1300, alto=40, relleno=["#7cc066", "#4f8f44"], x=540, y=780, z=0.51),
        {"tipo": "brillo", "x": 540, "y": 500, "radio": 300, "color": "#fff6d0", "intensidad": 0.5, "z": 0.52,
         "anim": {"pulso": [0.1, 1.5]}},
        F(forma="rect", ancho=1300, alto=8, relleno="#ffffff", op_relleno=0.9, x=540, y=780, z=0.53,
          keys=[{"t": 0.4, "ex": 0}, {"t": 1.2, "ex": 1}]),
    ],
}

ep = {
    "id": "2026-11-15-tarde-03-moais-con-cuerpo", "version": 1,
    "audio": "03-locucion.mp3",
    "subtitulos": {"alineacion": "03-alineacion-original.json", "max_chars": 26},
    "estilo_subtitulos": {"y": 1600, "tam": 60},
    "escenas": [e1, e2, e3, e4, e5, e6, e7],
}
guardar(ep, salida())
