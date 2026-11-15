"""02 — La Luna se aleja a la velocidad a la que crecen tus uñas. Tiempos de la alineación de ElevenLabs."""
from comun import F, guardar, salida, reloj
import math

ESPACIO = {"colores": ["#02030a", "#0b1030", "#1c2142"]}
estrellas = {"tipo": "particulas", "clase": "estrellas", "area": [0, 0, 1080, 1920], "n": 140, "tam": [1.2, 3.2],
             "vel": [-4, 0], "color": "#ffffff", "z": 0.1, "semilla": 4}

def tierra(x, y, r, giro=14, z=0.3, keys=None):
    return [{"tipo": "brillo", "x": x, "y": y, "radio": r * 2.2, "color": "#6fb6ff", "intensidad": 0.35, "z": z},
            {"tipo": "esfera", "x": x, "y": y, "radio": r, "textura": "tierra", "halo": "#8fd0ff", "giro": giro,
             "luz": [-0.7, -0.4], "z": z, "semilla": 8, "keys": keys or []}]

def luna(x, y, r, z=0.35, keys=None, anim=None):
    e = {"tipo": "esfera", "x": x, "y": y, "radio": r, "textura": "crateres", "color": "#d9d9df", "color2": "#8d8d99",
         "giro": 4, "luz": [-0.7, -0.4], "z": z, "semilla": 3, "keys": keys or []}
    if anim: e["anim"] = anim
    return e

def dedo(x, y, s=1.0, z=0.6, una0=20, una1=60, t0=0, t1=4, keys=None):
    """Dedo índice visto desde arriba con la uña que crece (la parte blanca)."""
    return {"tipo": "grupo", "x": x, "y": y, "ancho": 340 * s, "alto": 900 * s, "z": z, "keys": keys or [],
            "anim": {"flotar": [5, 3]},
            "hijos": [
                F(forma="redondeado", ancho=230 * s, alto=820 * s, relleno=["#f0b892", "#d48f68"], esquinas=115 * s, y=60 * s,
                  sombra={"radio": 20, "desplaz": [12, 16]}),
                F(forma="redondeado", ancho=120 * s, alto=22 * s, relleno="#c98260", esquinas=10 * s, y=110 * s, op_relleno=0.5),
                F(forma="redondeado", ancho=120 * s, alto=22 * s, relleno="#c98260", esquinas=10 * s, y=330 * s, op_relleno=0.5),
                # punta blanca de la uña que crece hacia arriba
                {"tipo": "forma", "forma": "redondeado", "ancho": 160 * s, "alto": 100 * s, "relleno": ["#fffaf2", "#efe2d0"], "esquinas": 30 * s,
                 "keys": [{"t": t0, "ey": una0 / 100, "y": -320 * s - una0 * s / 2}, {"t": t1, "ey": una1 / 100, "y": -320 * s - una1 * s / 2}]},
                F(forma="redondeado", ancho=170 * s, alto=210 * s, relleno=["#f9cdd0", "#e9a6ad"], esquinas=60 * s, y=-230 * s, brillo=True),
            ]}

def regla(x, y, largo, z=0.5, rot=0, keys=None):
    n = 10
    return {"tipo": "grupo", "x": x, "y": y, "ancho": largo + 40, "alto": 160, "z": z, "rot": rot, "keys": keys or [],
            "hijos": [F(forma="redondeado", ancho=largo, alto=110, relleno=["#ffd96b", "#e0a92a"], esquinas=10, sombra={"radio": 12}),
                      *[F(forma="rect", ancho=5, alto=46 if i % 5 == 0 else 26, relleno="#5a3d0e",
                          x=-largo / 2 + 30 + i * (largo - 60) / n, y=-55 + (23 if i % 5 == 0 else 13)) for i in range(n + 1)]]}

# ---------------------------------------------------------------- escenas
e1 = {  # 0 – 5.4: mira tus uñas / la Luna se aleja a la misma velocidad
    "inicio": 0, "fin": 5.4,
    "fondo": ESPACIO, "camara": {"zoom": [1.0, 1.05], "pan": [[0, 0], [0, -20]]}, "vineta": 0.4,
    "elementos": [
        estrellas, *tierra(250, 380, 150),
        luna(560, 330, 60, keys=[{"t": 1.2, "x": 560}, {"t": 5.4, "x": 900, "ease": "lineal"}]),
        {"tipo": "flecha", "puntos": [[620, 450], [760, 460], [900, 450]], "grosor": 10, "color": "#ffffffcc", "discontinua": [26, 18],
         "z": 0.35, "keys": [{"t": 1.4, "progreso": 0}, {"t": 4.8, "progreso": 1}]},
        dedo(540, 1380, 1.0, una0=10, una1=80, t0=1.2, t1=5.4,
             keys=[{"t": 0, "y": 2100}, {"t": 0.8, "y": 1380, "ease": "salida"}]),
        {"tipo": "brillo", "x": 540, "y": 960, "radio": 200, "color": "#ffffff", "intensidad": 0.5, "z": 0.65,
         "anim": {"pulso": [0.2, 1.0]}, "keys": [{"t": 1.3, "op": 0}, {"t": 1.8, "op": 1}]},
    ],
}

e2 = {  # 5.4 – 8.1: tres coma ocho centímetros al año (regla)
    "inicio": 5.4, "fin": 8.1, "entrada": "barrido",
    "fondo": {"tipo": "radial", "colores": ["#22305a", "#0b1030"]}, "camara": {"zoom": [1.0, 1.04], "pan": [[0, 0], [0, 0]]},
    "vineta": 0.4,
    "elementos": [
        estrellas,
        regla(540, 760, 900),
        # tramo de 3,8 cm marcado sobre la regla (38 % del largo útil)
        {"tipo": "barra", "x": 540 - 420 + 840 * 0.38 / 2, "y": 860, "ancho": 840 * 0.38, "alto": 30, "color": "#ff5a5a",
         "fondo": "#ffffff20", "z": 0.55, "keys": [{"t": 0.2, "progreso": 0}, {"t": 1.6, "progreso": 1}]},
        luna(120, 560, 70, z=0.5, keys=[{"t": 0.2, "x": 120}, {"t": 1.6, "x": 120 + 840 * 0.38}]),
        # calendario de un año: doce casillas que se encienden
        *[F(forma="redondeado", ancho=110, alto=110, relleno=["#ffffff", "#dfe6ff"], grosor=5, borde="#6c7bd9",
            x=210 + (i % 4) * 220, y=1100 + (i // 4) * 140, z=0.5, esquinas=16,
            keys=[{"t": 0.2 + i * 0.11, "op": 0.25}, {"t": 0.3 + i * 0.11, "op": 1, "escala": 1.12}, {"t": 0.5 + i * 0.11, "escala": 1}])
          for i in range(12)],
    ],
}

e3 = {  # 8.1 – 10.5: ¿cómo lo sabemos?
    "inicio": 8.1, "fin": 10.5, "entrada": "corte",
    "fondo": ESPACIO, "camara": {"zoom": [1.0, 1.06], "pan": [[0, 0], [0, -20]]},
    "elementos": [
        estrellas, *tierra(270, 1150, 220), luna(820, 420, 110),
        {"tipo": "flecha", "puntos": [[420, 990], [600, 720], [740, 520]], "grosor": 10, "color": "#ffffffaa", "discontinua": [26, 18],
         "z": 0.4, "keys": [{"t": 0.2, "progreso": 0}, {"t": 1.2, "progreso": 1}]},
        {"tipo": "grupo", "ancho": 420, "alto": 420, "z": 0.6,
         "keys": [{"t": 0, "x": 580, "y": 760, "escala": 0}, {"t": 0.4, "escala": 1, "ease": "rebote"}, {"t": 2.4, "x": 620, "y": 700}],
         "hijos": [F(forma="redondeado", ancho=50, alto=190, relleno=["#4b3b6b", "#2a2140"], x=120, y=120, rot=-45),
                   F(forma="circulo", radio=130, relleno="#e8f6ff", op_relleno=0.16, grosor=18, borde="#f2f4fb", brillo=True)]},
    ],
}

reflector = {"tipo": "grupo", "x": 640, "y": 1150, "ancho": 340, "alto": 300, "z": 0.65,
             "hijos": [F(forma="rect", ancho=12, alto=150, relleno="#9a9aa8", x=-100, y=60, rot=15),
                       F(forma="rect", ancho=12, alto=150, relleno="#9a9aa8", x=100, y=60, rot=-15),
                       F(forma="redondeado", ancho=280, alto=170, relleno=["#c9ccd6", "#7c7f8c"], esquinas=8, rot=-20, y=-30,
                         sombra={"radio": 12}),
                       *[F(forma="circulo", radio=16, relleno=["#e6f2ff", "#7aa6d6"], x=-105 + (i % 7) * 35, y=-75 + (i // 7) * 32 + ((i % 7) - 3) * -12,
                           brillo=True) for i in range(28)]]}
e4 = {  # 10.5 – 14.4: los astronautas dejaron espejos
    "inicio": 10.5, "fin": 14.4, "entrada": "barrido",
    "fondo": ESPACIO, "camara": {"zoom": [1.0, 1.05], "pan": [[0, 0], [0, -20]]},
    "elementos": [
        estrellas, *tierra(800, 330, 100),
        {"tipo": "suelo", "material": "luna", "borde": 1000, "crateres": 18, "z": 0.6, "semilla": 12},
        {"tipo": "persona", "casco": True, "alto": 380, "z": 0.62, "y": 1080,
         "keys": [{"t": 0, "x": 120, "paso": 1.0, "ease": "lineal"}, {"t": 1.6, "x": 380, "paso": 1.0},
                  {"t": 1.8, "paso": 0, "brazo_d": 18}, {"t": 2.3, "brazo_d": 80}]},
        dict(reflector, keys=[{"t": 1.6, "op": 0, "y": 1050}, {"t": 2.2, "op": 1, "y": 1150, "ease": "rebote"}]),
        {"tipo": "brillo", "x": 640, "y": 1110, "radio": 220, "color": "#bfe3ff", "intensidad": 0.8, "z": 0.66,
         "anim": {"parpadeo": [0.4, 0.8]}, "keys": [{"t": 2.4, "op": 0}, {"t": 2.8, "op": 1}]},
    ],
}

laser = lambda t0: [
    {"tipo": "flecha", "puntos": [[300, 1290], [560, 860], [800, 470]], "grosor": 12, "color": "#ff3b3b", "punta": True, "z": 0.5,
     "keys": [{"t": t0, "progreso": 0, "op": 1}, {"t": t0 + 0.7, "progreso": 1}, {"t": t0 + 1.6, "op": 0}]},
    {"tipo": "brillo", "x": 800, "y": 470, "radio": 140, "color": "#ff6b6b", "intensidad": 0.9, "z": 0.5,
     "keys": [{"t": t0 + 0.7, "op": 0, "escala": 0.3}, {"t": t0 + 0.8, "op": 1}, {"t": t0 + 1.4, "op": 0, "escala": 1.4}]},
    {"tipo": "flecha", "puntos": [[830, 500], [600, 900], [340, 1310]], "grosor": 8, "color": "#ffb3b3", "punta": True, "z": 0.5,
     "discontinua": [26, 18],
     "keys": [{"t": t0 + 0.8, "progreso": 0, "op": 1}, {"t": t0 + 1.5, "progreso": 1}, {"t": t0 + 2.2, "op": 0}]},
]
e5 = {  # 14.4 – 23.6: láser de ida y vuelta, y el cronómetro
    "inicio": 14.4, "fin": 23.6, "entrada": "fundido",
    "fondo": ESPACIO, "camara": {"zoom": [1.0, 1.04], "pan": [[0, 0], [0, -10]]},
    "elementos": [
        estrellas, *tierra(170, 1480, 330, giro=8), luna(840, 420, 120),
        F(forma="redondeado", ancho=60, alto=170, relleno=["#e8e8f0", "#8a8a99"], x=290, y=1250, rot=30, z=0.4, sombra={"radio": 8}),
        *laser(0.3), *laser(2.8), *laser(5.2), *laser(7.0),
        reloj(780, 1180, 150, 0, 0, 0, 1, z=0.45,
              keys=[{"t": 4.9, "escala": 0, "op": 0}, {"t": 5.3, "escala": 1, "op": 1, "ease": "rebote"}]),
        # aguja de cronómetro que corre mientras el pulso viaja
        {"tipo": "forma", "forma": "poligono", "puntos": [[-6, 0], [-4, -112], [4, -112], [6, 0], [6, 18], [-6, 18]], "relleno": "#2f80ed",
         "x": 780, "y": 1180, "z": 0.46,
         "keys": [{"t": 4.9, "op": 0, "rot": 0}, {"t": 5.3, "op": 1}, {"t": 9.2, "rot": 720, "ease": "lineal"}]},
    ],
}

orbita = lambda r0, r1, t0, t1: F(forma="circulo", radio=r0, relleno="#ffffff", op_relleno=0, grosor=5, borde="#ffffff55",
                                  x=540, y=860, z=0.3, keys=[{"t": t0, "escala": 1}, {"t": t1, "escala": r1 / r0}])
def luna_orbita(r0, r1, t0, t1, vueltas=1.0, z=0.35, rad=60, pasos=24, ang0=-30):
    ks = []
    for i in range(pasos + 1):
        f = i / pasos
        r = r0 + (r1 - r0) * f
        a = math.radians(ang0 + 360 * vueltas * f)
        ks.append({"t": t0 + (t1 - t0) * f, "x": 540 + r * math.cos(a), "y": 860 + r * math.sin(a), "ease": "lineal"})
    return luna(0, 0, rad, z=z, keys=ks)

e6 = {  # 23.6 – 32.0: mareas que frenan la Tierra y empujan la Luna
    "inicio": 23.6, "fin": 32.0, "entrada": "barrido",
    "fondo": ESPACIO, "camara": {"zoom": [1.0, 1.03], "pan": [[0, 0], [0, 0]]},
    "elementos": [
        estrellas,
        orbita(330, 400, 4.5, 8.4),
        # abultamiento de marea alrededor de la Tierra (se estira hacia la Luna)
        F(forma="elipse", ancho=440, alto=330, relleno="#3fa7ff", op_relleno=0.45, desenfoque=8, x=540, y=860, z=0.3,
          keys=[{"t": 0, "rot": -30, "op": 0}, {"t": 0.8, "op": 1}, {"t": 8.4, "rot": 330, "ease": "lineal"}]),
        *tierra(540, 860, 160, giro=60),
        # flecha curva que gira con la Tierra y se frena
        {"tipo": "flecha", "puntos": [[540 + 230 * math.cos(math.radians(a)), 860 + 230 * math.sin(math.radians(a))] for a in range(200, 340, 14)],
         "grosor": 12, "color": "#ffd34d", "punta": True, "z": 0.4,
         "keys": [{"t": 2.0, "progreso": 0}, {"t": 3.2, "progreso": 1}]},
        {"tipo": "forma", "forma": "redondeado", "ancho": 70, "alto": 24, "relleno": "#ff5a5a", "x": 540, "y": 590, "z": 0.45,
         "keys": [{"t": 3.4, "escala": 0}, {"t": 3.8, "escala": 1, "ease": "rebote"}]},
        luna_orbita(330, 400, 0, 8.4, vueltas=0.9),
        {"tipo": "flecha", "puntos": [[740, 1040], [800, 1100], [860, 1160]], "grosor": 14, "color": "#ffffff", "punta": True, "z": 0.45,
         "keys": [{"t": 5.8, "progreso": 0, "op": 0}, {"t": 6.0, "op": 1}, {"t": 6.6, "progreso": 1}]},
    ],
}

e7 = {  # 32.0 – 37.0: los días se alargan, muy despacio
    "inicio": 32.0, "fin": 37.0, "entrada": "fundido",
    "fondo": {"colores": ["#2a6fb0", "#79b8e6", "#f7d08a"]}, "camara": {"zoom": [1.0, 1.04], "pan": [[0, 0], [0, -10]]},
    "elementos": [
        {"tipo": "esfera", "radio": 80, "textura": "sol", "color": "#fff3b0", "color2": "#ffb347", "z": 0.2,
         "keys": [{"t": 0, "x": 100, "y": 1000, "ease": "lineal"}, {"t": 2.5, "x": 540, "y": 420}, {"t": 5.0, "x": 980, "y": 1000, "ease": "lineal"}]},
        {"tipo": "brillo", "radio": 300, "color": "#fff1c0", "intensidad": 0.5, "z": 0.2,
         "keys": [{"t": 0, "x": 100, "y": 1000, "ease": "lineal"}, {"t": 2.5, "x": 540, "y": 420}, {"t": 5.0, "x": 980, "y": 1000, "ease": "lineal"}]},
        {"tipo": "suelo", "material": "hierba", "borde": 1080, "ondulacion": 30, "z": 0.5, "semilla": 7},
        # barra del día con un trocito añadido diminuto que brilla
        {"tipo": "barra", "x": 540, "y": 1300, "ancho": 840, "alto": 48, "color": "#ffd34d", "fondo": "#00000040", "z": 0.55,
         "keys": [{"t": 0, "progreso": 0}, {"t": 2.4, "progreso": 0.985, "ease": "lineal"}, {"t": 4.6, "progreso": 1.0, "ease": "lineal"}]},
        {"tipo": "brillo", "x": 540 + 420 - 6, "y": 1300, "radio": 70, "color": "#ff7a3d", "intensidad": 0.9, "z": 0.56,
         "anim": {"pulso": [0.3, 0.6]}, "keys": [{"t": 2.6, "op": 0}, {"t": 3.0, "op": 1}]},
        # caracol que avanza (muy despacio)
        {"tipo": "grupo", "y": 1150, "ancho": 200, "alto": 140, "z": 0.6,
         "keys": [{"t": 0, "x": 160, "ease": "lineal"}, {"t": 5.0, "x": 300}],
         "hijos": [F(forma="redondeado", ancho=160, alto=34, relleno=["#b9d27a", "#7f9a3c"], esquinas=17, y=40),
                   F(forma="circulo", radio=52, relleno=["#d79a5c", "#9a5e2a"], x=-10, y=-4, brillo=True),
                   F(forma="circulo", radio=24, relleno="#b07a40", x=-10, y=-4),
                   F(forma="rect", ancho=5, alto=40, relleno="#7f9a3c", x=66, y=10, rot=20),
                   F(forma="circulo", radio=7, relleno="#2a2a33", x=72, y=-10)]},
    ],
}

e8 = {  # 37.0 – fin: tranquilo, la Luna no se va a escapar mañana
    "inicio": 37.0, "fin": 41.55, "entrada": "fundido",
    "fondo": ESPACIO, "camara": {"zoom": [1.04, 1.0], "pan": [[0, 0], [0, 0]]},
    "elementos": [
        estrellas,
        orbita(360, 360, 0, 1),
        *tierra(540, 860, 170, giro=20),
        luna_orbita(360, 362, 0, 4.6, vueltas=0.35, ang0=200, rad=70),
        {"tipo": "particulas", "clase": "chispas", "color": "#bfe3ff", "area": [140, 460, 940, 1260], "n": 30, "tam": [2, 4],
         "vel": [0, -20], "z": 0.5, "semilla": 9},
    ],
}

ep = {
    "id": "2026-11-15-tarde-02-luna-se-aleja", "version": 1,
    "audio": "02-locucion.mp3",
    "subtitulos": {"alineacion": "02-alineacion-original.json", "max_chars": 26},
    "estilo_subtitulos": {"y": 1600, "tam": 60},
    "escenas": [e1, e2, e3, e4, e5, e6, e7, e8],
}
guardar(ep, salida())
