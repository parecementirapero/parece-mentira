"""01 — Todos los planetas caben entre la Tierra y la Luna. Uso: python3 gen_01.py DIR_SALIDA
Planos de conjunto a escala real (Tierra abajo, Luna arriba, 1.410 px = 384.400 km entre centros);
planos de detalle con cada planeta grande y una barra lateral que se llena hacia la Luna."""
import sys
from comun_m import IMG, BG, ROT, AMARILLO, CONTEXTO, polvo, brillo, cam, Montaje, flecha, contador

M = Montaje(sys.argv[1])
ESP = ["#02030a", "#0a1030"]
E_Y, L_Y, X = 1880, 640, 540
DIST = 384400
K = (E_Y - L_Y) / DIST
# nombre, diámetro km, factor ancho_svg/diámetro_dibujado
PLANETAS = [("mercurio", 4879, 1 / 0.92), ("venus", 12104, 1 / 0.92), ("marte", 6779, 1 / 0.92), ("jupiter", 139820, 1 / 0.92),
            ("saturno", 116460, 2.3 / 0.92), ("urano", 50724, 1 / 0.92), ("neptuno", 49244, 1 / 0.92)]


def columna(aparecer=None, dt=0.18):
    """Los 7 planetas apilados entre los centros de la Tierra y la Luna (escala real).
    aparecer=t0 → caen uno a uno desde t0."""
    els, y = [], E_Y
    for i, (n, d, f) in enumerate(PLANETAS):
        h = d * K
        cy = y - h / 2
        y -= h
        e = IMG(n, ancho=max(8, round(h * f)), x=X, y=cy, z=0.45)
        if aparecer is not None:
            t = aparecer + i * dt
            e["keys"] = [{"t": t, "op": 0, "y": cy - 120}, {"t": t + 0.05, "op": 1}, {"t": t + 0.35, "y": cy, "ease": "rebote"}]
        els.append(e)
    return els


def luna_peq(luna_keys=None):
    return [brillo(X, L_Y, 60, "#ffffff", 0.6, 0.4, pulso=[0.15, 1.6], keys=luna_keys),
            IMG("luna_hd", ancho=16, x=X, y=L_Y, z=0.42, keys=luna_keys or [])]


def conjunto(luna_keys=None):
    return [BG("bg_espacio"), polvo("#ffffff", 30, (0, 0, 1080, 1920), 4, "estrellas"),
            IMG("tierra_hd", ancho=56, x=X, y=E_Y, z=0.4, anim={"girar": 6}),
            brillo(X, E_Y, 90, "#6fb6ff", 0.5, 0.4, pulso=[0.1, 2]),
            ROT(0, 99, "LUNA", tam=40, x=X + 150, y=L_Y, capsula="#0d1330b0", color="#ffffff"),
            ROT(0, 99, "TIERRA", tam=40, x=X - 170, y=E_Y - 10, capsula="#0d1330b0", color="#ffffff")]


def barra(p0, p1, t0=0.3, t1=1.4):
    """Barra lateral: cuánto del camino hasta la Luna llevamos ocupado."""
    return [{"tipo": "barra", "x": 1010, "y": 1150, "ancho": 34, "alto": 1300, "vertical": True, "color": "#ffd23f", "fondo": "#ffffff22",
             "hud": True, "z": 1, "keys": [{"t": t0, "progreso": p0}, {"t": t1, "progreso": p1, "ease": "salida"}]},
            IMG("luna_hd", ancho=70, x=1010, y=470, z=1, hud=True), IMG("tierra_hd", ancho=70, x=1010, y=1830, z=1, hud=True)]


def caer(n, ancho, x, y, t0, z=0.6, desde=-500, giro=0):
    return IMG(n, ancho=ancho, x=x, z=z, anim={"girar": giro} if giro else {},
               keys=[{"t": t0, "y": desde, "op": 1}, {"t": t0 + 0.55, "y": y, "ease": "rebote"}])


acum = [0]
for _, d, _ in PLANETAS:
    acum.append(acum[-1] + d)
P = [a / DIST for a in acum]  # progreso tras cada planeta

# 1 · gancho (0–3,45): la columna completa entre la Tierra y la Luna
M.plano(0, 3.45, ESP, conjunto() + columna() + luna_peq(), cam(1.0, 1.04, (540, 1170), (540, 1150)), vineta=0.55)

# 2 · «Parece imposible, pero haz la cuenta»
M.plano(3.45, 6.3, ESP, [BG("bg_espacio"), IMG("tierra_hd", ancho=760, x=330, y=1560, z=0.4, anim={"girar": 3}),
        IMG("luna_hd", ancho=200, x=820, y=640, z=0.3), flecha([(450, 1240), (770, 720)], 0.4, 1.6, "#ffffffaa", 7, disc=[22, 16])],
        cam(1.0, 1.06, (540, 1100), (560, 1060)), entrada="desenfoque", dur=0.35, vineta=0.6)
M.add(AMARILLO(0.3, 2.6, "¿IMPOSIBLE?", y=1000))

# 3 · 384.000 km de media
M.plano(6.3, 10.9, ESP, [BG("bg_espacio"), IMG("tierra_hd", ancho=420, x=260, y=1620, z=0.4, anim={"girar": 3}),
        IMG("luna_hd", ancho=150, x=860, y=560, z=0.3, anim={"flotar": [6, 3]}), flecha([(360, 1450), (800, 640)], 0.1, 1.2, "#ffffffcc", 6, disc=[18, 14])],
        cam(1.0, 1.05), entrada="corte")
M.add(contador(1.8, 4.5, 384000, "KM", x=540, y=1080, dur=1.6), CONTEXTO(0.6, 3.4, "DE MEDIA"))

# 4 · «Ponemos los planetas en fila, tocándose»
fila = []
for i, (n, _, f) in enumerate(PLANETAS):
    w = 130 if n != "saturno" else 300
    x = 150 + i * 130
    fila.append(IMG(n, ancho=w, x=x, y=1180, z=0.5, anim={"flotar": [8, 2.0 + i * 0.2]},
                    keys=[{"t": 0.2 + i * 0.12, "x": x + 1200}, {"t": 0.8 + i * 0.12, "x": x, "ease": "salida"}]))
M.plano(10.9, 14.2, ESP, [BG("bg_espacio"), polvo("#ffffff", 30, (0, 0, 1080, 1920), 6, "estrellas")] + fila,
        cam(1.0, 1.05, (540, 1150), (540, 1150)), entrada="zoom", dur=0.35)
M.add(AMARILLO(1.2, 3.2, "EN FILA", y=1500))

# 5 · Mercurio
M.plano(14.2, 17.45, ESP, [BG("bg_espacio"), brillo(540, 1100, 380, "#9fb3ff", 0.25), caer("mercurio", 520, 540, 1100, 0.0, giro=4)] + barra(0, P[1]),
        cam(1.0, 1.06, (540, 1100), (540, 1100)), entrada="desenfoque", dur=0.3)
M.add(ROT(0.6, 3.1, "≈5.000", unidad="KM", tam=110, x=480, y=1500), CONTEXTO(0.2, 2.0, "MERCURIO"))

# 6 · Venus y Marte
M.plano(17.45, 20.45, ESP, [BG("bg_espacio"), caer("venus", 500, 360, 1000, 0.0, giro=3), caer("marte", 330, 720, 1280, 0.5, giro=5)] + barra(P[1], P[3]),
        cam(1.0, 1.05, (540, 1100), (540, 1100)), entrada="desenfoque", dur=0.3)
M.add(ROT(0.9, 2.9, "+19.000", unidad="KM", tam=110, x=480, y=1600), CONTEXTO(0.2, 2.2, "VENUS + MARTE"))

# 7 · Júpiter, el gigante (entra desde abajo y llena la pantalla)
jup = IMG("jupiter", ancho=1150, x=540, z=0.5, anim={"girar": 2}, keys=[{"t": 0, "y": 2600}, {"t": 0.9, "y": 1150, "ease": "salida"}])
M.plano(20.45, 22.6, ESP, [BG("bg_espacio"), jup] + barra(P[3], P[3]), cam(1.0, 1.04, (540, 1100), (540, 1100), temblor=4),
        entrada="desenfoque", dur=0.3)
M.add(AMARILLO(0.7, 2.1, "GIGANTE", y=1700))
M.plano(22.6, 25.45, ESP, [BG("bg_espacio"), IMG("jupiter", ancho=1150, x=540, y=1150, z=0.5, anim={"girar": 2})] + barra(P[3], P[4], 0.2, 1.6),
        cam(1.25, 1.35, (620, 1250), (620, 1250)))
M.add(contador(0.3, 2.8, 140000, "KM", x=480, y=1650, dur=1.2))

# 8 · Saturno
M.plano(25.45, 28.35, ESP, [BG("bg_espacio"), IMG("saturno", ancho=1200, x=540, z=0.5, anim={"flotar": [10, 3]},
        keys=[{"t": 0, "x": -700, "rot": -8}, {"t": 0.9, "x": 520, "rot": 0, "ease": "salida"}])] + barra(P[4], P[5]),
        cam(1.0, 1.06, (540, 1100), (540, 1100)), entrada="desenfoque", dur=0.3)
M.S[-1]["elementos"][1]["y"] = 1080
M.add(ROT(0.8, 2.8, "116.000", unidad="KM", tam=110, x=480, y=1620), CONTEXTO(0.2, 2.0, "SATURNO"))

# 9 · Urano y Neptuno
M.plano(28.35, 32.3, ESP, [BG("bg_espacio"), caer("urano", 470, 330, 1000, 0.05, giro=3), caer("neptuno", 460, 740, 1260, 1.1, giro=4)] + barra(P[5], P[7], 0.6, 2.4),
        cam(1.0, 1.05, (540, 1100), (540, 1100)), entrada="desenfoque", dur=0.3)
M.add(ROT(2.0, 3.8, "50.000 ×2", unidad="KM", tam=100, x=480, y=1640), CONTEXTO(0.6, 2.8, "URANO + NEPTUNO"))

# 10 · Total: la columna se arma entre la Tierra y la Luna
M.plano(32.3, 35.85, ESP, conjunto() + columna(aparecer=0.1, dt=0.2) + luna_peq(), cam(1.0, 1.03, (540, 1170), (540, 1170)), entrada="zoom", dur=0.35)
M.add({**contador(1.4, 3.5, 380000, "KM", x=300, y=1300, tam=90, dur=1.2)})

# 11 · Sobran ~4.000 km: justo para Plutón
M.plano(35.85, 40.1, ESP, [BG("bg_espacio"), IMG("luna_hd", ancho=360, x=540, y=560, z=0.4),
        IMG("neptuno", ancho=1700, x=540, y=2280, z=0.4, anim={"girar": 1}),
        {"tipo": "flecha", "puntos": [[540, 760], [540, 1440]], "grosor": 6, "color": "#ffd23f", "punta": True, "z": 0.5,
         "keys": [{"t": 0.4, "progreso": 0}, {"t": 1.2, "progreso": 1}]},
        IMG("pluton", ancho=220, x=760, y=1100, z=0.6, anim={"flotar": [8, 2]},
            keys=[{"t": 0, "op": 0, "escala": 0.2}, {"t": 3.3, "op": 0, "escala": 0.2}, {"t": 3.45, "op": 1}, {"t": 3.75, "escala": 1.0, "ease": "rebote"}])],
        cam(1.0, 1.05, (540, 1100), (540, 1080)), entrada="desenfoque", dur=0.3)
M.add(ROT(1.0, 4.2, "SOBRAN ≈4.000", unidad="KM", tam=78, x=480, y=1600), CONTEXTO(3.4, 4.2, "PLUTÓN"))

# 12 · Eso sí: solo con la distancia media
M.plano(40.1, 43.25, ESP, conjunto() + columna() + luna_peq(), cam(1.1, 1.15, (540, 1050), (540, 1000)), entrada="corte")
M.add(AMARILLO(0.2, 1.4, "ESO SÍ", y=1250), CONTEXTO(1.0, 3.1, "SOLO A DISTANCIA MEDIA"))

# 13 · Cuando la Luna se acerca, ya no entran
acerca = [{"t": 0, "y": L_Y}, {"t": 1.4, "y": L_Y + 80, "ease": "suave"}]
M.plano(43.25, 45.9, ESP, conjunto() + columna() + [IMG("luna_hd", ancho=26, x=X, y=L_Y, z=0.42, keys=acerca)] +
        [brillo(X, 690, 200, "#ff3b3b", 0.8, 0.5, keys=[{"t": 1.2, "op": 0}, {"t": 1.5, "op": 0.8}, {"t": 2.6, "op": 0.4}])],
        cam(2.2, 2.3, (540, 780), (540, 800)))
M.S[-1]["camara"]["temblor"] = 0
M.S[-1]["elementos"] = [e for e in M.S[-1]["elementos"] if e.get("texto") != "TIERRA"]  # HUD: en el primer plano no está la Tierra
M.add(ROT(1.5, 2.6, "NO ENTRAN", tam=96, x=540, y=1500, color="#ff6b5a", capsula=None, rot=-6))

# 14 · Esta noche, cuando mires la Luna…
M.plano(45.9, 48.9, ["#050817", "#3a3d6a"], [BG("bg_noche"), brillo(800, 520, 260, "#dfe8ff", 0.55, 0.1, pulso=[0.08, 2.5]),
        IMG("luna_hd", ancho=190, x=800, y=520, z=0.12), polvo("#ffffff", 18, (0, 0, 1080, 1300), 9, "estrellas")],
        cam(1.0, 1.06, (540, 1000), (560, 960)), entrada="desenfoque", dur=0.4, vineta=0.65)
M.add(CONTEXTO(0.4, 2.6, "ESTA NOCHE"))
# … piensa en todo el espacio que hay entre tú y ella
M.plano(48.9, 52.2, ["#050817", "#3a3d6a"], [BG("bg_noche"), brillo(800, 520, 260, "#dfe8ff", 0.55, 0.1, pulso=[0.08, 2.5]),
        IMG("luna_hd", ancho=190, x=800, y=520, z=0.12),
        flecha([(420, 1180), (600, 900), (760, 600)], 0.3, 2.2, "#ffd23f", 7, punta=False, disc=[18, 14])],
        cam(1.12, 1.22, (600, 900), (680, 760)), vineta=0.65)

# 15 · bucle: vuelve la columna del principio
M.plano(52.2, 54.4, ESP, conjunto() + columna() + luna_peq(), cam(1.06, 1.0, (540, 1150), (540, 1170)), entrada="desenfoque", dur=0.35)

M.guardar("01", "planetas-entre-tierra-y-luna", 54.4,
          ["planetas", "Luna", "kilómetros", "Júpiter", "Saturno", "Plutón", "media", "cerca"], {"generar": "curiosidad", "semilla": 11})
