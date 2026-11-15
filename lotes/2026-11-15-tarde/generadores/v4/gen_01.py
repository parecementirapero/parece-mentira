"""01 — Zanzíbar v4: ilustraciones SVG detalladas (ilus.py) + un plano por frase + movimiento continuo.
Audio y alineación de la v2 (no gasta créditos). Uso: python3 gen_01.py DIR_SALIDA
"""
import copy, json, os, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
shutil.copytree(os.path.join(AQUI, "svg"), os.path.join(OUT, "svg"), dirs_exist_ok=True)


def IMG(n, **k): return {"tipo": "imagen", "archivo": f"svg/{n}.svg", **k}
def BG(n, z=0.05, ancho=1180): return IMG(n, ancho=ancho, x=540, y=960, z=z)
def ROT(t0, t1, texto, **k):
    ks = [{"t": t0, "escala": 0.0, "op": 0}, {"t": t0 + 0.06, "op": 1}, {"t": t0 + 0.3, "escala": 1.0, "ease": "rebote"},
          {"t": t1, "escala": 1.0, "op": 1}, {"t": t1 + 0.2, "op": 0}]
    return {"tipo": "rotulo", "texto": texto, "hud": True, "z": 1, "keys": ks, **k}
def AMARILLO(t0, t1, texto, y=1360): return ROT(t0, t1, texto, tam=96, color="#ffd23f", capsula=None, rot=-6, x=540, y=y)
def CONTEXTO(t0, t1, texto): return ROT(t0, t1, texto, tam=54, color="#ffffff", capsula="#c0392be6", borde="#ffffff30", x=540, y=470)
def polvo(color="#fff1c8", n=40, area=(0, 300, 1080, 1700), sem=1):
    return {"tipo": "particulas", "clase": "polvo", "color": color, "area": list(area), "n": n, "tam": [2, 5],
            "vel": [6, -10], "z": 0.9, "semilla": sem}
def humo(x, y, n=30, ancho=260, sem=2, op=1.0):
    """Columna de humo: bocanadas suaves (brillos grises) que suben, crecen y se desvanecen en bucle."""
    import random
    r = random.Random(sem)
    out = []
    for i in range(max(5, n // 5)):
        x0 = x + r.uniform(-ancho / 2, ancho / 2)
        out.append({"tipo": "brillo", "x": x0, "y": y - r.uniform(0, 120), "radio": r.uniform(120, 200), "color": "#2b2826",
                    "intensidad": 0.55 * op, "z": 0.5, "anim": {"deriva": [r.uniform(8, 25), -r.uniform(55, 90)], "pulso": [0.15, r.uniform(2, 3)]}})
    return out
def fogonazo(x, y, t0, r=220, z=0.6):
    return {"tipo": "brillo", "x": x, "y": y, "radio": r, "color": "#ffcf6a", "intensidad": 1.0, "z": z,
            "keys": [{"t": t0, "escala": 0.2, "op": 0}, {"t": t0 + 0.05, "op": 1}, {"t": t0 + 0.55, "escala": 1.6, "op": 0, "ease": "salida"}]}
def cam(z0, z1, f0=(540, 960), f1=None, temblor=0):
    return {"zoom": [z0, z1], "foco": [list(f0), list(f1 or f0)], "pan": [[0, 0], [0, 0]], "temblor": temblor}


S = []
def plano(ini, fin, fondo, elementos, camara, entrada="corte", vineta=0.55, dur=None):
    p = {"inicio": ini, "fin": fin, "fondo": {"colores": fondo}, "elementos": copy.deepcopy(elementos), "camara": camara,
         "entrada": entrada, "vineta": vineta}
    if dur: p["dur_entrada"] = dur
    S.append(p)


NOCHE = ["#05070f", "#121a33"]
# ---------------------------------------------------------------- 1. gancho: partido vs guerra
marc = IMG("marcador", ancho=900, x=540, y=640, z=0.3)
barras = [{"tipo": "barra", "x": 640, "y": 618, "ancho": 520, "alto": 46, "color": "#e8ecf7", "fondo": "#ffffff18", "z": 0.3,
           "keys": [{"t": 0.0, "progreso": 0}, {"t": 2.6, "progreso": 1, "ease": "lineal"}]},
          {"tipo": "barra", "x": 640 - 260 + 260 * 38 / 90, "y": 748, "ancho": 520 * 38 / 90, "alto": 46, "color": "#ff5a4a",
           "fondo": "#00000000", "z": 0.3, "keys": [{"t": 1.4, "progreso": 0}, {"t": 2.6, "progreso": 1, "ease": "lineal"}]}]
balon = {"tipo": "esfera", "radio": 44, "color": "#ffffff", "color2": "#bfc4cc", "textura": "lisa", "giro": 200, "z": 0.7,
         "keys": [{"t": 0, "x": 120, "y": 1750}, {"t": 1.9, "x": 760, "y": 1480, "ease": "salida"}, {"t": 3.9, "x": 420, "y": 1340}]}
plano(0, 1.9, NOCHE, [BG("bg_estadio"), balon, polvo("#dfe8ff", 30), marc, *barras],
      cam(1.0, 1.08, (540, 1000), (540, 900)), vineta=0.6)
plano(1.9, 3.85, NOCHE, [BG("bg_estadio"), balon, marc, *barras,
                         ROT(0.9, 1.9, "38", unidad="MIN", tam=110, x=860, y=900)],
      cam(1.45, 1.6, (560, 690), (600, 700)), vineta=0.6)
for b in S[-1]["elementos"]:
    if b.get("tipo") == "barra":
        for k in b["keys"]:
            k["t"] = round(k["t"] - 1.9, 2)
S[-1]["elementos"][1]["keys"] = [{"t": k["t"] - 1.9, **{a: v for a, v in k.items() if a != "t"}} for k in balon["keys"]]

# ---------------------------------------------------------------- 2. mapa
pin = IMG("chincheta", ancho=120, x=690, z=0.5,
          keys=[{"t": 0.35, "y": 500, "op": 0}, {"t": 0.45, "op": 1}, {"t": 0.85, "y": 960, "ease": "rebote"}])
plano(3.85, 5.04, ["#d9bf85", "#b89a5a"], [BG("bg_mapa"), pin], cam(1.0, 1.06), entrada="desenfoque", dur=0.4, vineta=0.4)
pin2 = dict(pin, keys=[{"t": 0, "y": 960, "op": 1}])
plano(5.04, 8.29, ["#d9bf85", "#b89a5a"], [BG("bg_mapa"), pin2,
      {"tipo": "brillo", "x": 690, "y": 1010, "radio": 160, "color": "#ff6a4a", "intensidad": 0.6, "z": 0.45, "anim": {"pulso": [0.25, 1.0]}},
      ROT(0.4, 3.0, "27·08·1896", tam=96, x=540, y=1500, capsula="#3a2410e0", color="#f7ebcd")],
      cam(1.55, 1.75, (690, 1000), (700, 990)), vineta=0.45)

# ---------------------------------------------------------------- 3. palacio: muere el sultán, entra Jalid
band = IMG("bandera_roja", ancho=170, x=640, z=0.36, anim={"balanceo": [3, 1.6]},
           keys=[{"t": 0, "y": 230}, {"t": 0.9, "y": 230}, {"t": 2.0, "y": 380, "ease": "suave"}])
sol = {"tipo": "brillo", "x": 820, "y": 560, "radio": 420, "color": "#ffd59a", "intensidad": 0.4, "z": 0.06, "anim": {"pulso": [0.05, 3]}}
gaviotas = [{"tipo": "flecha", "puntos": [[0, 0], [22, -14], [44, 0], [66, -14], [88, 0]], "grosor": 6, "color": "#3a2a2a",
             "punta": False, "z": 0.2, "anim": {"deriva": [40, -4], "flotar": [8, 1.4]}, "x": gx, "y": gy}
            for gx, gy in [(-480, -1350), (-200, -1260), (-360, -1180)]]
plano(8.29, 10.47, ["#2c3a6b", "#ffc97a"], [BG("bg_palacio"), sol, *gaviotas, band, polvo()],
      cam(1.0, 1.07, (540, 900), (560, 820)), entrada="zoom", dur=0.4, vineta=0.5)
CONTEXTO_SULTAN = CONTEXTO(0.9, 2.0, "MUERE EL SULTÁN")
S[-1]["elementos"].append(CONTEXTO_SULTAN)
jalid = IMG("jalid", ancho=300, y=1380, z=0.75, anim={"balanceo": [2.5, 0.7]},
            keys=[{"t": 0, "x": -120}, {"t": 2.0, "x": 430, "ease": "salida"}, {"t": 2.45, "x": 450}])
plano(10.47, 12.92, ["#2c3a6b", "#ffc97a"], [BG("bg_palacio"), sol, band, jalid, polvo()],
      cam(1.2, 1.32, (420, 1100), (470, 1060)))
S[-1]["elementos"][2]["keys"] = [{"t": 0, "y": 380}]
oficial = IMG("oficial", ancho=420, x=860, y=1500, z=0.85, keys=[{"t": 0, "x": 1200}, {"t": 0.6, "x": 860, "ease": "salida"}])
plano(12.92, 14.81, ["#2c3a6b", "#ffc97a"], [BG("bg_palacio"), sol, IMG("jalid", ancho=260, x=450, y=1330, z=0.7), oficial],
      cam(1.12, 1.2, (640, 1150), (680, 1180)))
S[-1]["elementos"].append(ROT(0.7, 1.8, "NO", unidad="APROBADO", tam=110, color="#ff4a3a", capsula=None, x=450, y=900))

# ---------------------------------------------------------------- 4. ultimátum y barcos
carta = IMG("carta", ancho=640, x=540, y=1050, z=0.6,
            keys=[{"t": 0, "y": 2400, "rot": -18}, {"t": 0.7, "y": 1050, "rot": -4, "ease": "salida"}, {"t": 2.2, "rot": -2, "escala": 1.05}])
plano(14.81, 16.97, ["#3a2a1c", "#1a120c"], [{"tipo": "brillo", "x": 540, "y": 900, "radio": 700, "color": "#ffcf8a", "intensidad": 0.35, "z": 0.05},
      polvo("#ffd9a0", 30), carta], cam(1.0, 1.12, (540, 1000), (540, 900)), entrada="desenfoque", dur=0.35, vineta=0.7)
S[-1]["elementos"].append(AMARILLO(1.3, 2.1, "ULTIMÁTUM", y=1700))
flota = []
for i, (y, s, fase) in enumerate([(1500, 640, 0), (1640, 760, 0.6), (1380, 520, 1.2)]):
    flota.append(IMG("crucero", ancho=s, y=y, z=0.6 + i * 0.05, anim={"flotar": [7, 2.6], "balanceo": [1.5, 2.6]}, fase=fase,
                     keys=[{"t": 0, "x": 1500 + i * 200}, {"t": 1.6, "x": 360 + i * 230, "ease": "salida"}]))
plano(16.97, 18.84, ["#6aa6d9", "#fbe6c0"], [BG("bg_puerto_manana"), *flota, polvo("#ffffff", 20)],
      cam(1.0, 1.06, (540, 1100), (560, 1150)))
S[-1]["elementos"].append(CONTEXTO(0.2, 1.8, "O TE VAS… O DISPARAMOS"))

# ---------------------------------------------------------------- 5. Jalid se atrinchera y arma el yate
plano(18.84, 21.44, ["#6aa6d9", "#fbe6c0"], [BG("bg_puerto_manana"), IMG("defensores", ancho=1240, x=540, y=1640, z=0.85,
      keys=[{"t": 0, "y": 2000}, {"t": 0.6, "y": 1640, "ease": "salida"}]), polvo("#ffe9c0", 30)],
      cam(1.15, 1.25, (540, 1400), (540, 1450)))
S[-1]["elementos"].append(ROT(1.4, 2.5, "≈3.000", unidad="HOMBRES", tam=110, x=540, y=1150))
plano(21.44, 23.13, ["#6aa6d9", "#fbe6c0"], [BG("bg_puerto_manana"),
      IMG("yate", ancho=720, y=1500, z=0.7, anim={"flotar": [6, 2.2], "balanceo": [2, 2.2]},
          keys=[{"t": 0, "x": -400}, {"t": 1.1, "x": 520, "ease": "salida"}])],
      cam(1.3, 1.42, (520, 1450), (520, 1450)))
S[-1]["elementos"].append(AMARILLO(0.7, 1.6, "YATE REAL", y=1820))

# ---------------------------------------------------------------- 6. 9:00 → fuego
def reloj(t_ini, h0, m0, h1, m1, t0, t1, x=540, y=1050, ancho=640):
    k = ancho / 600
    cx, cy = x, y + (320 - 300) * k
    return [IMG("reloj_bolsillo", ancho=ancho, x=x, y=y, z=0.6),
            IMG("aguja_hora", ancho=200 * k * 1.9, x=cx, y=cy, z=0.61,
                keys=[{"t": t0, "rot": h0 * 30 + m0 * 0.5, "ease": "lineal"}, {"t": t1, "rot": h1 * 30 + m1 * 0.5}]),
            IMG("aguja_min", ancho=200 * k * 2.2, x=cx, y=cy, z=0.62,
                keys=[{"t": t0, "rot": m0 * 6, "ease": "lineal"}, {"t": t1, "rot": m1 * 6}])]
plano(23.13, 24.96, ["#1a1410", "#3a2a1c"], [{"tipo": "brillo", "x": 540, "y": 1000, "radio": 650, "color": "#ffcf8a", "intensidad": 0.3, "z": 0.05},
      *reloj(0, 9, 0, 9, 2, 0.2, 1.8), polvo("#ffd9a0", 25)], cam(1.0, 1.1, (540, 1060), (540, 1060)), entrada="zoom", dur=0.35, vineta=0.7)
S[-1]["elementos"].append(CONTEXTO(0.3, 1.6, "09:02 · EMPIEZA"))
flota2 = [IMG("crucero", ancho=980, x=560, y=1400, z=0.7, anim={"flotar": [6, 2.4], "balanceo": [1.2, 2.4]})]
flota2 += [fogonazo(110, 1335, t) for t in (0.25, 0.9, 1.5)]
flota2 += [*humo(150, 1330, 20, 200, 4)]
plano(24.96, 26.86, ["#6aa6d9", "#fbe6c0"], [BG("bg_puerto_manana"), *flota2], cam(1.15, 1.25, (420, 1350), (380, 1330), temblor=3))
S[-1]["elementos"].append(ROT(0.2, 1.7, "5", unidad="BARCOS", tam=110, x=760, y=1700))
plano(26.86, 28.72, ["#2c3a6b", "#ffc97a"], [BG("bg_palacio"), band,
      *[fogonazo(x, y, t, 260, 0.4) for x, y, t in ((380, 880, 0.15), (700, 940, 0.6), (520, 620, 1.0), (300, 1020, 1.4))],
      *humo(540, 1100, 40, 700, 6), polvo("#ffcf9a", 40)], cam(1.0, 1.08, (540, 900), (540, 880), temblor=6))
S[-1]["elementos"][1]["keys"] = [{"t": 0, "y": 380}]
S[-1]["elementos"].append(AMARILLO(0.2, 1.4, "¡FUEGO!", y=1600))

# ---------------------------------------------------------------- 7. 9:40 silencio y ruinas
plano(28.72, 30.12, ["#1a1410", "#3a2a1c"], [*reloj(0, 9, 2, 9, 40, 0.0, 1.2), polvo("#ffd9a0", 25)],
      cam(1.1, 1.2, (540, 1060), (540, 1060)), vineta=0.7)
S[-1]["elementos"].append(CONTEXTO(0.4, 1.3, "09:40 · FIN"))
plano(30.12, 33.74, ["#3b3d45", "#c9a27a"], [BG("bg_ruinas"), *humo(380, 1000, 30, 300, 8, 0.8), *humo(760, 1000, 30, 300, 9, 0.8),
      polvo("#d9cbb8", 50)], cam(1.0, 1.12, (540, 1000), (540, 900)), entrada="desenfoque", dur=0.4, vineta=0.6)
S[-1]["elementos"].append(AMARILLO(3.0, 3.6, "EN RUINAS", y=1650))

# ---------------------------------------------------------------- 8. 38 minutos
plano(33.74, 35.99, ["#120d08", "#2a1c10"], [{"tipo": "rayos", "x": 540, "y": 1000, "n": 18, "longitud": 1100, "apertura": 8,
      "intensidad": 0.25, "z": 0.05, "anim": {"girar": 6}}, *reloj(0, 9, 2, 9, 40, 0.3, 1.9, y=1000, ancho=720)],
      cam(1.0, 1.08), entrada="zoom", dur=0.35, vineta=0.7)
S[-1]["elementos"].append({**ROT(0.6, 2.1, "", tam=150, x=540, y=1560), "contar": [0, 38, 1.0], "contar_desde": 0.6, "unidad": "MIN"})

# ---------------------------------------------------------------- 9. balanza 500 contra 1
def balanza(ang_t, t_inc):
    """Base + viga que gira sobre el pivote + platos que cuelgan en vertical de los extremos."""
    import math
    PX, PY, L = 540, 930, 360
    def ends(th):
        r = math.radians(th)
        return (PX - L * math.cos(r), PY + L * math.sin(r)), (PX + L * math.cos(r), PY - L * math.sin(r))
    tiempos = [0, t_inc] + [t_inc + 0.05 * i for i in range(1, 21)]
    def ang(t):
        if t <= t_inc:
            return ang_t[0]
        u = min((t - t_inc) / 1.0, 1)
        c1, c3 = 1.70158, 2.70158
        e = 1 + c3 * (u - 1) ** 3 + c1 * (u - 1) ** 2   # rebote suave (easeOutBack)
        return ang_t[0] + (ang_t[1] - ang_t[0]) * e
    kv, ki, kd = [], [], []
    for t in tiempos:
        th = ang(t)
        (lx, ly), (rx, ry) = ends(th)
        kv.append({"t": round(t, 3), "rot": round(-th, 3), "ease": "lineal"})
        ki.append({"t": round(t, 3), "x": round(lx, 1), "y": round(ly + 200, 1), "ease": "lineal"})
        kd.append({"t": round(t, 3), "x": round(rx, 1), "y": round(ry + 200, 1), "ease": "lineal"})
    return [IMG("balanza_base", ancho=800, x=540, y=1260, z=0.5),
            IMG("plato_izq", ancho=320, z=0.51, keys=ki), IMG("plato_der", ancho=320, z=0.51, keys=kd),
            IMG("balanza_viga", ancho=800, x=PX, y=PY, z=0.53, keys=kv)]
luz = {"tipo": "brillo", "x": 540, "y": 700, "radio": 700, "color": "#ffe9a8", "intensidad": 0.25, "z": 0.05}
plano(35.99, 38.37, ["#0d1324", "#1f2b48"], [luz, *balanza((0, 12), 0.9), polvo("#c8d4ff", 30)], cam(1.0, 1.04, (540, 1050), (540, 1040)),
      entrada="desenfoque", dur=0.4, vineta=0.65)
plano(38.37, 40.95, ["#0d1324", "#1f2b48"], [luz, *balanza((12, 12), 0)], cam(1.0, 1.05, (540, 1050), (520, 1060)), vineta=0.65)
S[-1]["elementos"].append(ROT(0.4, 2.3, "≈500", unidad="BAJAS", tam=120, x=540, y=1500))
plano(40.95, 43.63, ["#0d1324", "#1f2b48"], [luz, *balanza((12, 12), 0)], cam(1.0, 1.05, (540, 1050), (560, 1060)), vineta=0.65)
S[-1]["elementos"].append(ROT(0.6, 2.4, "1", unidad="HERIDO BRITÁNICO", tam=120, x=540, y=1500))

# ---------------------------------------------------------------- 10. sultán nuevo, elegido por Londres
nuevo = IMG("sultan_nuevo", ancho=330, x=540, z=0.7, keys=[{"t": 0, "y": 1700, "op": 0}, {"t": 0.8, "y": 1380, "op": 1, "ease": "salida"}])
halo = {"tipo": "brillo", "x": 540, "y": 1100, "radio": 380, "color": "#ffd27a", "intensidad": 0.7, "z": 0.6, "anim": {"pulso": [0.08, 1.6]},
        "keys": [{"t": 0.5, "op": 0}, {"t": 1.3, "op": 1}]}
plano(43.63, 46.82, ["#3b3d45", "#c9a27a"], [BG("bg_ruinas"), *humo(540, 900, 20, 500, 10, 0.5), halo, nuevo, polvo("#ffe9b0", 40)],
      cam(1.05, 1.18, (540, 1200), (540, 1150)), entrada="zoom", dur=0.4)
S[-1]["elementos"].append(CONTEXTO(1.2, 3.0, "SULTÁN NUEVO"))
plano(46.82, 48.05, ["#3b3d45", "#c9a27a"], [BG("bg_ruinas"), halo, IMG("sultan_nuevo", ancho=330, x=420, y=1380, z=0.7),
      IMG("oficial", ancho=360, x=820, y=1450, z=0.8), {"tipo": "flecha", "puntos": [[760, 1180], [640, 1100], [500, 1060]], "grosor": 12,
      "color": "#ffffff", "contorno": "#00000055", "z": 0.85, "keys": [{"t": 0.2, "progreso": 0}, {"t": 0.8, "progreso": 1}]}],
      cam(1.2, 1.3, (620, 1250), (620, 1250)))
S[-1]["elementos"].append(CONTEXTO(0.2, 1.1, "ELEGIDO POR LONDRES"))

# ---------------------------------------------------------------- 11. cierre en bucle: el marcador
plano(48.05, 52.33, NOCHE, [BG("bg_estadio"), polvo("#dfe8ff", 30), marc,
      {"tipo": "barra", "x": 640, "y": 618, "ancho": 520, "alto": 46, "color": "#e8ecf7", "fondo": "#ffffff18", "z": 0.3, "keys": [{"t": 0, "progreso": 1}]},
      {"tipo": "barra", "x": 640 - 260 + 260 * 38 / 90, "y": 748, "ancho": 520 * 38 / 90, "alto": 46, "color": "#ff5a4a", "fondo": "#00000000",
       "z": 0.3, "anim": {"parpadeo": [0.5, 0.8]}, "keys": [{"t": 0, "progreso": 1}]},
      ROT(1.4, 4.0, "RÉCORD", unidad="MUNDIAL", tam=120, x=540, y=1500)],
      cam(1.3, 1.0, (560, 700), (540, 960)), entrada="desenfoque", dur=0.4, vineta=0.6)

ep = {"id": "2026-11-15-tarde-01-guerra-38-minutos", "version": 4, "audio": "01-locucion.mp3",
      "subtitulos": {"alineacion": "01-alineacion-original.json", "max_chars": 26},
      "estilo_subtitulos": {"modo": "karaoke", "y": 300, "tam": 62,
                            "claves": ["fútbol", "Zanzíbar", "ultimátum", "atrincheró", "fuego", "ruinas", "treinta", "ocho",
                                       "minutos", "quinientos", "solo", "menos"]},
      "musica": {"generar": "curiosidad", "semilla": 7}, "lufs": -19, "grano": 0.03, "escenas": S}
json.dump(ep, open(os.path.join(OUT, "episodio.json"), "w"), ensure_ascii=False, indent=1)
print(len(S), "planos")
