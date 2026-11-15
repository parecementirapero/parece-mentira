"""Genera episodio.json de la prueba 005 (huellas en la Luna). Tiempos tomados del SRT."""
import json

def F(**k): return {"tipo": "forma", **k}

estrellas = {"tipo": "particulas", "clase": "estrellas", "area": [0, 0, 1080, 1150], "n": 110,
             "tam": [1.2, 3.2], "vel": [-5, 0], "color": "#ffffff", "z": 0.1, "semilla": 4}
tierra = [
    {"tipo": "brillo", "x": 800, "y": 360, "radio": 260, "color": "#6fb6ff", "intensidad": 0.35, "z": 0.2},
    {"tipo": "esfera", "x": 800, "y": 360, "radio": 118, "textura": "tierra", "halo": "#8fd0ff",
     "giro": 14, "luz": [-0.7, -0.4], "z": 0.2, "semilla": 8, "anim": {"flotar": [6, 5]}},
]
suelo_luna = {"tipo": "suelo", "material": "luna", "borde": 1040, "crateres": 18, "z": 0.6, "semilla": 12}

def bota_baja(t0, x, y, ey=0.55, largo=330):
    return [
        F(forma="elipse", ancho=150, alto=300, relleno="#000000", op_relleno=0.55, desenfoque=22,
          x=x, y=y + 10, ey=ey, z=0.6,
          keys=[{"t": t0, "op": 0, "escala": 1.7}, {"t": t0 + 0.6, "op": 0.8, "escala": 1.0, "ease": "entrada"},
                {"t": t0 + 0.75, "op": 0}]),
        {"tipo": "huella", "clase": "bota", "suela": True, "color_suela": "#eceef4", "largo": largo,
         "x": x, "ey": ey, "z": 0.7,
         "keys": [{"t": t0, "escala": 2.8, "y": y - 520, "op": 0},
                  {"t": t0 + 0.15, "op": 1},
                  {"t": t0 + 0.6, "escala": 1.0, "y": y, "ease": "entrada"},
                  {"t": t0 + 0.95, "escala": 1.0, "y": y, "op": 1},
                  {"t": t0 + 1.4, "escala": 2.4, "y": y - 600, "op": 0, "ease": "entrada"}]},
    ]

huella_luna = lambda t0, x=540, y=1360: {
    "tipo": "huella", "clase": "bota", "largo": 420, "color": "#23232fcc", "x": x, "y": y, "ey": 0.55,
    "z": 0.6, "keys": [{"t": t0, "marca": 0}, {"t": t0 + 0.35, "marca": 1}]}

polvo_golpe = lambda t0, x=540, y=1360: {
    "tipo": "brillo", "x": x, "y": y, "radio": 260, "color": "#d9d9e6", "intensidad": 0.7, "ey": 0.5, "z": 0.6,
    "keys": [{"t": t0, "escala": 0.3, "op": 0}, {"t": t0 + 0.08, "op": 0.8},
             {"t": t0 + 0.9, "escala": 1.4, "op": 0, "ease": "salida"}]}

# ------------------------------------------------------------------ escenas
e1 = {  # 0 – 5.93 playa vista desde arriba
    "inicio": 0, "fin": 5.93, "fondo": {"colores": ["#f3d9a4", "#d9b47a"]},
    "camara": {"zoom": [1.0, 1.07], "pan": [[0, 0], [0, -30]]}, "vineta": 0.4,
    "elementos": [
        {"tipo": "suelo", "material": "arena", "borde": -120, "ondulacion": 0, "z": 0.5, "semilla": 3},
        *[F(forma="elipse", ancho=w, alto=w * 0.6, relleno=["#ffd9e2", "#e89aae"], sombra={"radio": 6, "desplaz": [0, 5]},
            x=x, y=y, rot=r, z=0.5, brillo=True)
          for x, y, w, r in [(190, 1500, 54, 20), (880, 1240, 42, -30), (820, 1660, 36, 60)]],
        F(forma="poligono", puntos=[[0, -46], [12, -14], [44, -14], [18, 6], [28, 40], [0, 18], [-28, 40], [-18, 6],
                                    [-44, -14], [-12, -14]], relleno=["#ffb05a", "#f27c35"], brillo=True,
          sombra={"radio": 8, "desplaz": [0, 7]}, x=240, y=1180, rot=15, z=0.5),
        {"tipo": "agua", "lado": "arriba", "z": 0.5, "amplitud": 26, "colores": ["#1a6fa6", "#68d6e4"],
         "keys": [{"t": 0, "nivel": 380}, {"t": 2.6, "nivel": 430}, {"t": 3.5, "nivel": 1260, "ease": "salida"},
                  {"t": 4.8, "nivel": 470}, {"t": 5.93, "nivel": 420}]},
        F(forma="elipse", ancho=150, alto=300, relleno="#5a3d1e", op_relleno=0.6, desenfoque=22, x=540, y=1050, z=0.6,
          keys=[{"t": 0.1, "op": 0, "escala": 1.8}, {"t": 0.8, "op": 0.7, "escala": 1.0, "ease": "entrada"},
                {"t": 0.95, "op": 0}]),
        {"tipo": "huella", "clase": "pie", "largo": 300, "color": "#7a5a2e88", "x": 540, "y": 1040, "z": 0.6,
         "semilla": 3,
         "keys": [{"t": 0.75, "marca": 0}, {"t": 1.0, "marca": 1}, {"t": 3.25, "borrado": 0},
                  {"t": 4.6, "borrado": 1}]},
        {"tipo": "huella", "clase": "pie", "suela": True, "color_suela": "#efbf98", "largo": 300, "x": 540, "z": 0.7,
         "keys": [{"t": 0.0, "escala": 2.8, "y": 520, "op": 0}, {"t": 0.15, "op": 1},
                  {"t": 0.8, "escala": 1.0, "y": 1040, "ease": "entrada"}, {"t": 1.25, "escala": 1.0, "y": 1040},
                  {"t": 1.75, "escala": 2.6, "y": 420, "op": 0, "ease": "entrada"}]},
        {"tipo": "particulas", "clase": "polvo", "color": "#fff1d2", "area": [-50, 0, 1130, 1920], "n": 80,
         "tam": [2, 4.5], "vel": [-320, 25], "z": 0.8, "semilla": 2,
         "keys": [{"t": 1.8, "op": 0}, {"t": 2.2, "op": 1}, {"t": 5.5, "op": 0.8}]},
        *[{"tipo": "flecha", "puntos": [[1150, y], [900, y - 30], [650, y + 25], [380, y - 15]], "grosor": 9,
           "color": "#ffffffcc", "punta": False, "z": 0.8, "anim": {"deriva": [-160, 0]},
           "keys": [{"t": t0, "progreso": 0, "op": 1}, {"t": t0 + 0.7, "progreso": 1}, {"t": t0 + 1.4, "op": 0}]}
          for y, t0 in [(820, 1.9), (1250, 2.25), (1600, 2.6)]],
        {"tipo": "brillo", "x": 120, "y": 120, "radio": 700, "color": "#fff3c4", "intensidad": 0.45, "z": 0.1},
    ],
}

e2 = {  # 5.93 – 11.93 Luna: misma pisada, pero no se borra
    "inicio": 5.93, "fin": 11.93, "entrada": "barrido",
    "fondo": {"colores": ["#02030a", "#0b1030", "#1c2142"]},
    "camara": {"zoom": [1.0, 1.04], "pan": [[0, 0], [-20, -10]]},
    "elementos": [
        estrellas, *tierra, suelo_luna,
        huella_luna(0.6), polvo_golpe(0.6), *bota_baja(0.0, 540, 1360, largo=420),
        # insignias: viento y lluvia, que luego se tachan
        F(forma="circulo", radio=135, relleno="#0e1430", op_relleno=0.8, grosor=7, borde="#dfe6ff",
          x=290, y=640, z=0.4, keys=[{"t": 1.9, "escala": 0, "ease": "rebote"}, {"t": 2.3, "escala": 1}]),
        F(forma="circulo", radio=135, relleno="#0e1430", op_relleno=0.8, grosor=7, borde="#dfe6ff",
          x=790, y=640, z=0.4, keys=[{"t": 2.1, "escala": 0, "ease": "rebote"}, {"t": 2.5, "escala": 1}]),
        *[{"tipo": "flecha", "puntos": [[200, y], [250, y - 18], [300, y + 12], [370, y - 6]], "grosor": 11,
           "color": "#bfe3ff", "punta": False, "z": 0.4, "anim": {"flotar": [4, 1.2]}, "fase": i,
           "keys": [{"t": 2.3 + i * 0.12, "progreso": 0}, {"t": 2.7 + i * 0.12, "progreso": 1}]}
          for i, y in enumerate([590, 640, 690])],
        {"tipo": "particulas", "clase": "lluvia", "color": "#9fd4ff", "area": [715, 555, 865, 725], "n": 16,
         "tam": [3, 4], "vel": [0, 420], "dispersion": 0.15, "z": 0.4, "semilla": 6,
         "keys": [{"t": 2.4, "op": 0}, {"t": 2.7, "op": 1}]},
        F(forma="redondeado", ancho=300, alto=26, relleno="#ff4d61", sombra={"radio": 6}, x=290, y=640, rot=-45, z=0.4,
          keys=[{"t": 3.75, "escala": 0, "ex": 0}, {"t": 4.05, "escala": 1, "ex": 1, "ease": "rebote"}]),
        F(forma="redondeado", ancho=300, alto=26, relleno="#ff4d61", sombra={"radio": 6}, x=790, y=640, rot=-45, z=0.4,
          keys=[{"t": 4.6, "escala": 0, "ex": 0}, {"t": 4.9, "escala": 1, "ex": 1, "ease": "rebote"}]),
    ],
}

pasos = [(170 + i * 125, 1440 + (18 if i % 2 else -18)) for i in range(7)]
e3 = {  # 11.93 – 17.33 astronauta, huellas y años que pasan
    "inicio": 11.93, "fin": 17.33,
    "fondo": {"colores": ["#02030a", "#0b1030", "#1c2142"]},
    "camara": {"zoom": [1.02, 1.0], "pan": [[0, 0], [0, 0]]},
    "elementos": [
        estrellas, *tierra, suelo_luna,
        {"tipo": "esfera", "x": -100, "y": 520, "radio": 62, "textura": "sol", "color": "#fff3b0",
         "color2": "#ffb347", "z": 0.15,
         "keys": [{"t": 2.6, "x": -100, "y": 560, "op": 1, "ease": "lineal"},
                  *[k for i in range(3) for k in (
                      {"t": 2.6 + i * 0.9, "x": -100, "y": 560, "ease": "lineal"},
                      {"t": 3.05 + i * 0.9, "y": 360},
                      {"t": 3.49 + i * 0.9, "x": 1180, "y": 560, "ease": "lineal"})]]},
        *[{"tipo": "huella", "clase": "bota", "largo": 120, "color": "#2c2c3aaa", "x": x, "y": y, "ey": 0.5,
           "lado": "izq" if i % 2 else "der", "rot": 90, "z": 0.6,
           "keys": [{"t": 0.25 + i * 0.36, "marca": 0}, {"t": 0.4 + i * 0.36, "marca": 1}]}
          for i, (x, y) in enumerate(pasos)],
        {"tipo": "persona", "casco": True, "alto": 360, "z": 0.65, "y": 1250, "paso": 1.0,
         "brazo_i": 18, "brazo_d": 18,
         "keys": [{"t": 0, "x": 120, "op": 1, "ease": "lineal"}, {"t": 2.6, "x": 960, "ease": "lineal"},
                  {"t": 2.9, "op": 0}]},
        {"tipo": "barra", "x": 540, "y": 230, "ancho": 760, "alto": 30, "color": "#ffd34d", "fondo": "#ffffff30",
         "z": 0.0, "keys": [{"t": 2.6, "progreso": 0, "op": 0}, {"t": 2.8, "op": 1},
                            {"t": 5.3, "progreso": 1, "ease": "lineal"}]},
    ],
}

lander = {"tipo": "grupo", "x": 540, "y": 980, "ancho": 420, "alto": 420, "z": 0.5,
          "hijos": [
              F(forma="elipse", ancho=330, alto=330, relleno="#000000", op_relleno=0.45, desenfoque=18, x=18, y=26),
              *[F(forma="redondeado", ancho=24, alto=170, relleno=["#d8d8e0", "#8b8b98"], x=dx, y=dy, rot=r)
                for dx, dy, r in [(-110, -110, -45), (110, -110, 45), (-110, 110, 45), (110, 110, -45)]],
              *[F(forma="circulo", radio=26, relleno=["#e6e6ee", "#9a9aa8"], x=dx, y=dy)
                for dx, dy in [(-165, -165), (165, -165), (-165, 165), (165, 165)]],
              F(forma="poligono", puntos=[[-50, -120], [50, -120], [120, -50], [120, 50], [50, 120], [-50, 120],
                                          [-120, 50], [-120, -50]], relleno=["#ffd36b", "#c98a1c"], brillo=True),
              F(forma="poligono", puntos=[[-30, -72], [30, -72], [72, -30], [72, 30], [30, 72], [-30, 72],
                                          [-72, 30], [-72, -30]], relleno=["#b8b8c4", "#7c7c8a"]),
          ]}
senderos = [
    [[600, 1130], [660, 1290], [610, 1440], [700, 1600], [820, 1680]],
    [[420, 1080], [300, 1200], [240, 1380], [150, 1480]],
    [[700, 900], [850, 820], [930, 700]],
]
sat = lambda keys: {"tipo": "grupo", "ancho": 520, "alto": 260, "z": 0.7, "y": 330, "keys": keys,
                    "anim": {"balanceo": [3, 3]},
                    "hijos": [
                        F(forma="redondeado", ancho=180, alto=70, relleno=["#3c6fd1", "#1b3c86"], grosor=4,
                          borde="#9fc0ff", x=-160, esquinas=6),
                        F(forma="redondeado", ancho=180, alto=70, relleno=["#3c6fd1", "#1b3c86"], grosor=4,
                          borde="#9fc0ff", x=160, esquinas=6),
                        F(forma="redondeado", ancho=110, alto=110, relleno=["#ffd36b", "#c98a1c"], brillo=True,
                          esquinas=18, sombra={"radio": 10}),
                        F(forma="circulo", radio=22, relleno="#eef2ff", x=0, y=70),
                    ]}
sat_keys = [{"t": 0, "x": -280, "ease": "lineal"}, {"t": 5.4, "x": 1360, "ease": "lineal"}]

e4 = {  # 17.33 – 22.77 vista cenital: módulo, senderos y la sonda
    "inicio": 17.33, "fin": 22.77,
    "fondo": {"colores": ["#9a9aa6", "#6e6e7c"]},
    "camara": {"zoom": [1.0, 1.06], "pan": [[0, 0], [0, 0]]}, "vineta": 0.6,
    "elementos": [
        {"tipo": "suelo", "material": "luna", "borde": -150, "crateres": 26, "ondulacion": 0, "z": 0.5, "semilla": 21},
        lander,
        *[{"tipo": "flecha", "puntos": p, "grosor": 11, "color": "#3e3e4c", "punta": False, "z": 0.5,
           "keys": [{"t": 1.4 + i * 0.4, "progreso": 0}, {"t": 3.4 + i * 0.4, "progreso": 1}]}
          for i, p in enumerate(senderos)],
        F(forma="poligono", puntos=[[-70, -560], [70, -560], [330, 560], [-330, 560]], relleno="#9fe0ff",
          op_relleno=0.18, desenfoque=10, y=900, z=0.7,
          keys=[{"t": 0, "x": -280, "ease": "lineal"}, {"t": 5.4, "x": 1360, "ease": "lineal"},
                {"t": 0.0, "op": 1}]),
        sat(sat_keys),
    ],
}

e5 = {  # 22.77 – 27.80 lupa: se ve el rastro, no cada bota
    "inicio": 22.77, "fin": 27.8, "entrada": "fundido",
    "fondo": {"colores": ["#9a9aa6", "#6e6e7c"]},
    "camara": {"zoom": [1.06, 1.12], "pan": [[0, 0], [-40, -60]]}, "vineta": 0.6,
    "elementos": [
        {"tipo": "suelo", "material": "luna", "borde": -150, "crateres": 26, "ondulacion": 0, "z": 0.5, "semilla": 21},
        lander,
        *[{"tipo": "flecha", "puntos": p, "grosor": 11, "color": "#3e3e4c", "punta": False, "z": 0.5}
          for p in senderos],
        *[{"tipo": "flecha", "puntos": p, "grosor": 30, "color": "#fff4b8", "punta": False, "z": 0.5,
           "keys": [{"t": 3.5, "op": 0, "progreso": 0}, {"t": 4.4, "op": 0.45, "progreso": 1}]}
          for p in senderos[:1]],
        {"tipo": "grupo", "ancho": 520, "alto": 520, "z": 0.6,
         "keys": [{"t": 0, "x": 470, "y": 1180, "escala": 0.0}, {"t": 0.4, "escala": 1.0, "ease": "rebote"},
                  {"t": 1.6, "x": 650, "y": 1380}, {"t": 3.2, "x": 700, "y": 1560}],
         "hijos": [
             F(forma="redondeado", ancho=56, alto=210, relleno=["#4b3b6b", "#2a2140"], x=150, y=150, rot=-45,
               sombra={"radio": 10}),
             F(forma="circulo", radio=165, relleno="#e8f6ff", op_relleno=0.16, grosor=20, borde="#f2f4fb",
               brillo=True, sombra={"radio": 12}),
         ]},
        sat([{"t": 0, "x": 1360, "ease": "lineal"}, {"t": 5.0, "x": -280, "ease": "lineal"}]),
    ],
}

e6 = {  # 27.80 – fin: la huella intacta
    "inicio": 27.8, "fin": 32.95,
    "fondo": {"colores": ["#02030a", "#0b1030", "#1c2142"]},
    "camara": {"zoom": [1.0, 1.14], "pan": [[0, 0], [0, -60]]},
    "elementos": [
        estrellas, *tierra, suelo_luna, huella_luna(-1),
        {"tipo": "brillo", "x": 540, "y": 1360, "radio": 320, "color": "#fffbe0", "ey": 0.5, "z": 0.6,
         "intensidad": 0.6, "anim": {"pulso": [0.08, 2.2]},
         "keys": [{"t": 0.8, "op": 0}, {"t": 2.0, "op": 1}]},
    ],
}

ep = {
    "id": "prueba-005-huellas-luna", "version": 1,
    "audio": "005-locucion.mp3",
    "subtitulos": {"srt": "005-huellas-v1.srt"},
    "estilo_subtitulos": {"modo": "clasico", "y": 1560, "tam": 66},
    "escenas": [e1, e2, e3, e4, e5, e6],
}
json.dump(ep, open("episodio.json", "w"), ensure_ascii=False, indent=1)
print("ok")
