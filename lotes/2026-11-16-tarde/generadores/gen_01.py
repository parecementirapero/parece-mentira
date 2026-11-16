"""01 — Crujirse los nudillos (Unger + resonancia 2015). Uso: python3 gen_01.py DIR_SALIDA DIR_AUDIO"""
import sys
from base import IMG, BG, ROT, AMARILLO, CONTEXTO, CRAC, polvo, brillo, cam, Montaje

M = Montaje(sys.argv[1])
CALIDO = ["#2a1610", "#120806"]
AZUL = ["#0a1622", "#03070c"]
NUD = [(150, 300), (232, 300), (314, 300), (392, 300)]  # nudillos en el lienzo 520x760 de la mano


def mano(nombre, x, y, ancho, z=0.5, **kw):
    return IMG(nombre, ancho=ancho, x=x, y=y, z=z, **kw)


def nudillo_abs(i, x, y, ancho, espejo=False):
    k = ancho / 520
    nx, ny = NUD[i]
    if espejo:
        nx = 520 - nx
    return x + (nx - 260) * k, y + (ny - 380) * k


def crujidos(x, y, ancho, tiempos, espejo=False):
    """Destellos amarillos en los nudillos en los instantes dados (relativos al plano)."""
    els = []
    for j, t in enumerate(tiempos):
        nx, ny = nudillo_abs(j % 4, x, y, ancho, espejo)
        els.append(brillo(nx, ny, 70, "#ffd23f", 0.9, 0.55, keys=[{"t": t - 0.01, "op": 0}, {"t": t, "op": 1, "escala": 0.4},
                                                                   {"t": t + 0.25, "op": 0, "escala": 1.6}]))
    return els


# 1 · gancho: las dos manos; la izquierda cruje, la derecha quieta
M.plano(0, 2.3, CALIDO, [brillo(540, 900, 700, "#ffb860", 0.35), mano("mano_izq", 290, 1150, 440, anim={"balanceo": [2, 0.5]}),
        mano("mano_der", 790, 1150, 440, anim={"flotar": [4, 3]}), *crujidos(290, 1150, 440, [0.15, 0.6, 1.05, 1.5, 1.95])],
        cam(1.0, 1.06, (540, 1100), (540, 1080)), vineta=0.6)
M.add(CRAC(0.15, 2.2, 230, 780), ROT(0.3, 2.2, "NUNCA", tam=70, color="#ffffff", capsula="#c0392be6", x=790, y=780))
for t in (0.15, 0.6, 1.05, 1.5, 1.95):
    M.fx(t, "tic", -12)
# 2 · primer plano: la izquierda cruje mientras pasan los años
M.plano(2.3, 4.15, CALIDO, [brillo(540, 900, 700, "#ffb860", 0.35), mano("mano_izq_roja", 540, 1150, 760, anim={"balanceo": [2, 0.4]}),
        *crujidos(540, 1150, 760, [0.1, 0.45, 0.8, 1.15, 1.5])], cam(1.0, 1.05, (540, 1000), (540, 980)), vineta=0.65)
M.add(ROT(0.1, 1.8, "60", unidad="AÑOS", tam=130, x=540, y=1650, contar=[0, 60, 1.2], contar_desde=0.1))
for t in (2.4, 2.75, 3.1, 3.45, 3.8):
    M.fx(t, "tic", -14)

# 3 · Donald Unger, médico, en su salón
M.plano(4.15, 7.0, CALIDO, [BG("bg_salon"), IMG("medico", ancho=420, x=560, y=1180, z=0.5, anim={"balanceo": [1.5, 1.6]}), polvo("#ffe9b0", 25)],
        cam(1.0, 1.06, (540, 1100), (560, 1060)), entrada="desenfoque", dur=0.35, vineta=0.55)
M.add(CONTEXTO(0.2, 2.7, "DONALD UNGER · MÉDICO"))
M.fx(4.15, "whoosh", -16)
# 4 · «quería comprobar algo que todos hemos oído»
M.plano(7.0, 10.2, CALIDO, [BG("bg_salon"), IMG("medico", ancho=420, x=560, y=1180, z=0.5, anim={"balanceo": [1.5, 1.6]}),
        ROT(0.6, 3.0, "?", tam=200, color="#ffd23f", capsula=None, x=760, y=640, anim={"flotar": [10, 1.4]})],
        cam(1.35, 1.45, (560, 900), (560, 880)), vineta=0.6)
M.fx(7.6, "pop", -16)
# 5 · «crujirse los dedos da artritis»: radiografía con articulaciones inflamadas
M.plano(10.2, 12.85, AZUL, [brillo(540, 960, 600, "#4fd2ff", 0.25), IMG("rx_artritis", ancho=720, x=540, y=1100, z=0.5),
        brillo(540, 900, 260, "#ff3b2f", 0.45, 0.6, pulso=[0.3, 0.6])], cam(1.0, 1.08, (540, 1050), (540, 960)), entrada="zoom", dur=0.35, vineta=0.6)
M.add(AMARILLO(1.3, 2.6, "¿ARTRITIS?", y=1700))
M.fx(10.2, "zap", -16)

# 6 · el experimento: la libreta
M.plano(12.85, 15.9, CALIDO, [BG("bg_salon"), IMG("cuaderno", ancho=760, x=540, y=1130, z=0.5, rot=-3,
        keys=[{"t": 0, "y": 1500, "op": 0}, {"t": 0.5, "y": 1130, "op": 1, "ease": "salida"}])],
        cam(1.0, 1.06, (540, 1100), (540, 1080)), entrada="desenfoque", dur=0.3, vineta=0.65)
M.add(AMARILLO(0.7, 3.0, "EXPERIMENTO", y=1720))
M.fx(12.9, "whoosh", -16)
# 7 · izquierda, todos los días
M.plano(15.9, 19.25, CALIDO, [brillo(540, 900, 700, "#ffb860", 0.35), mano("mano_izq", 540, 1180, 720, anim={"balanceo": [2, 0.45]}),
        *crujidos(540, 1180, 720, [0.4, 0.9, 1.4, 1.9, 2.4, 2.9])], cam(1.0, 1.05, (540, 1050), (540, 1050)), vineta=0.65)
M.add(CONTEXTO(0.1, 3.2, "IZQUIERDA · CADA DÍA"), CRAC(0.4, 3.2, 200, 640, tam=80))
for t in (16.3, 16.8, 17.3, 17.8, 18.3, 18.8):
    M.fx(t, "tic", -14)
# 8 · derecha, nunca
M.plano(19.25, 21.5, ["#16202c", "#080c12"], [brillo(540, 900, 600, "#9fc0ff", 0.25), mano("mano_der", 540, 1180, 720, anim={"flotar": [6, 2.5]})],
        cam(1.0, 1.04, (540, 1050), (540, 1040)), vineta=0.7)
M.add(CONTEXTO(0.1, 2.1, "DERECHA · NUNCA"), ROT(0.4, 2.1, "0", unidad="CRUJIDOS", tam=130, x=540, y=1700))

# 9 · sesenta años después: el médico ya mayor delante de las dos radiografías
rx = [IMG("rx_izq", ancho=400, x=330, y=990, z=0.4), IMG("rx_der", ancho=400, x=750, y=990, z=0.4)]
M.plano(21.5, 24.65, ["#0d141c", "#0d141c"], [BG("bg_negatoscopio"), *rx, IMG("medico_viejo", ancho=420, x=880, y=1500, z=0.6,
        keys=[{"t": 0, "x": 1200}, {"t": 1.0, "x": 880, "ease": "salida"}], anim={"balanceo": [1.5, 1.4]})],
        cam(1.0, 1.05, (540, 1080), (540, 1060)), entrada="zoom", dur=0.4, vineta=0.55)
M.add(ROT(0.1, 2.8, "60", unidad="AÑOS DESPUÉS", tam=110, x=540, y=440, contar=[0, 60, 1.0], contar_desde=0.1))
M.fx(21.5, "whoosh", -16)
# 10 · ni rastro de artritis, ninguna diferencia
M.plano(24.65, 29.0, ["#0d141c", "#0d141c"], [BG("bg_negatoscopio"), *rx,
        IMG("check", ancho=150, x=330, y=1420, z=0.6, keys=[{"t": 0.4, "escala": 0, "op": 0}, {"t": 0.7, "escala": 1, "op": 1, "ease": "rebote"}]),
        IMG("check", ancho=150, x=750, y=1420, z=0.6, keys=[{"t": 1.0, "escala": 0, "op": 0}, {"t": 1.3, "escala": 1, "op": 1, "ease": "rebote"}]),
        ROT(2.4, 4.4, "=", tam=200, color="#ffffff", capsula=None, x=540, y=1000, z=0.6)],
        cam(1.0, 1.06, (540, 1100), (540, 1080)), vineta=0.55)
M.add(AMARILLO(0.6, 2.2, "SIN ARTRITIS", y=1700), AMARILLO(2.4, 4.3, "SIN DIFERENCIAS", y=1700))
M.fx(25.05, "ding", -16); M.fx(25.95, "ding", -16)

# 11 · una sola persona
M.plano(29.0, 31.0, ["#1a1420", "#0a0810"], [brillo(540, 900, 500, "#ffe9b0", 0.3), IMG("persona_sola", ancho=420, x=540, y=1100, z=0.5,
        anim={"flotar": [6, 2]})], cam(1.0, 1.05, (540, 1050), (540, 1030)), entrada="desenfoque", dur=0.3, vineta=0.7)
M.add(ROT(0.2, 1.9, "1", unidad="PERSONA", tam=140, x=540, y=1640))
# 12 · Ig Nobel 2009
confeti = {"tipo": "particulas", "clase": "chispas", "color": "#ffd23f", "area": [0, 300, 1080, 1400], "n": 60, "tam": [4, 9], "vel": [0, 120], "z": 0.8, "semilla": 9}
M.plano(31.0, 34.75, ["#120408", "#120408"], [BG("bg_escenario"), IMG("trofeo", ancho=420, x=540, y=1180, z=0.5,
        keys=[{"t": 0, "escala": 0.6, "op": 0}, {"t": 0.5, "escala": 1, "op": 1, "ease": "rebote"}]),
        brillo(540, 1000, 300, "#fff2a8", 0.5, 0.5, pulso=[0.15, 1.2]), confeti], cam(1.0, 1.06, (540, 1100), (540, 1060)), entrada="zoom", dur=0.35, vineta=0.6)
M.add(CONTEXTO(0.2, 3.6, "2009 · PREMIO IG NOBEL"), AMARILLO(1.6, 3.6, "MEDICINA", y=1680))
M.fx(31.2, "brillo", -14)

# 13 · ¿y qué es ese ruido?
M.plano(34.75, 36.6, CALIDO, [brillo(540, 900, 700, "#ffb860", 0.35), mano("mano_izq", 540, 1200, 760, anim={"balanceo": [2, 0.4]}),
        IMG("ondas", ancho=220, x=880, y=760, z=0.6, anim={"pulso": [0.12, 0.4]}), *crujidos(540, 1200, 760, [0.3, 1.0])],
        cam(1.25, 1.35, (520, 900), (520, 880)), entrada="desenfoque", dur=0.3, vineta=0.65)
M.add(AMARILLO(0.2, 1.8, "¿EL RUIDO?", y=1700))
M.fx(35.05, "tic", -12); M.fx(35.75, "tic", -12)

# 14 · 2015, Canadá: dedos dentro de la resonancia
escaner = {"tipo": "forma", "forma": "rect", "ancho": 520, "alto": 10, "relleno": "#4fd2ff", "z": 0.55, "x": 540,
           "keys": [{"t": 0, "y": 700}, {"t": 1.3, "y": 1160}, {"t": 2.6, "y": 700}]}
M.plano(36.6, 39.25, ["#cfe2ee", "#8fb0c4"], [BG("bg_resonancia"), mano("mano_izq", 540, 1010, 300, z=0.5, rot=90), escaner,
        brillo(540, 930, 280, "#4fd2ff", 0.35, 0.5, pulso=[0.2, 0.8])], cam(1.0, 1.06, (540, 1000), (540, 980)), entrada="zoom", dur=0.35, vineta=0.4)
M.add(CONTEXTO(0.2, 2.5, "2015 · CANADÁ"))
M.fx(36.7, "senal", -18)
M.plano(39.25, 42.35, ["#1a1f26", "#0a0d12"], [IMG("pantalla_rm", ancho=1000, x=540, y=1000, z=0.4),
        {"tipo": "forma", "forma": "rect", "ancho": 880, "alto": 6, "relleno": "#4fd2ff", "z": 0.5, "x": 540,
         "keys": [{"t": 0, "y": 700}, {"t": 1.5, "y": 1260}, {"t": 3, "y": 700}]}], cam(1.0, 1.1, (540, 1000), (540, 980)), vineta=0.6)
M.add(AMARILLO(0.5, 2.9, "RESONANCIA", y=1580))

# 15 · al estirar, los huesos se separan
ART = ["#3a1a22", "#12060a"]
hsup = IMG("hueso_sup", ancho=520, x=540, y=580, z=0.5)
def hinf(k): return IMG("hueso_inf", ancho=520, x=540, z=0.5, keys=k)
M.plano(42.35, 46.2, ART, [BG("bg_articulacion"), hsup, hinf([{"t": 0, "y": 1230}, {"t": 0.8, "y": 1230}, {"t": 2.6, "y": 1360, "ease": "suave"}]),
        {"tipo": "flecha", "puntos": [[860, 1000], [860, 1300]], "grosor": 14, "color": "#ffd23f", "contorno": "#00000066", "z": 0.6,
         "keys": [{"t": 0.8, "progreso": 0}, {"t": 2.0, "progreso": 1}]}],
        cam(1.0, 1.04, (540, 960), (540, 980)), entrada="zoom", dur=0.35, vineta=0.6)
M.add(AMARILLO(0.8, 3.6, "SE SEPARAN", y=1720))
M.fx(43.2, "whoosh", -18)
# 16 · el líquido pierde presión
M.plano(46.2, 48.75, ART, [BG("bg_articulacion"), hsup, hinf([{"t": 0, "y": 1360}, {"t": 2.5, "y": 1380}]),
        {"tipo": "forma", "forma": "elipse", "ancho": 380, "alto": 170, "relleno": "#0a1a3a", "x": 540, "y": 1010, "desenfoque": 20, "z": 0.45,
         "keys": [{"t": 0, "op": 0}, {"t": 2.0, "op": 0.55}]},
        {"tipo": "barra", "x": 900, "y": 980, "ancho": 50, "alto": 360, "vertical": True, "color": "#4fd2ff", "fondo": "#ffffff20", "z": 0.6,
         "keys": [{"t": 0, "progreso": 1}, {"t": 2.0, "progreso": 0.15}]}],
        cam(1.2, 1.3, (560, 990), (560, 990)), vineta=0.65)
M.add(ROT(0.2, 2.4, "PRESIÓN", tam=72, color="#ffffff", capsula="#0a2a4ae6", x=540, y=1700))
# 17 · ¡de golpe, una burbuja de gas!
bur = IMG("burbuja", ancho=190, x=540, y=1010, z=0.55, keys=[{"t": 0, "escala": 0, "op": 0}, {"t": 1.25, "escala": 0, "op": 0},
                                                         {"t": 1.45, "escala": 1.15, "op": 1, "ease": "rebote"}, {"t": 3.3, "escala": 1.0}],
          anim={"pulso": [0.04, 0.5]})
M.plano(48.75, 52.15, ART, [BG("bg_articulacion"), hsup, hinf([{"t": 0, "y": 1380}]), bur,
        brillo(540, 990, 260, "#ffffff", 1.0, 0.6, keys=[{"t": 0, "op": 0}, {"t": 1.25, "op": 0}, {"t": 1.35, "op": 1.0}, {"t": 1.9, "op": 0}])],
        cam(1.0, 1.08, (540, 990), (540, 990)), vineta=0.6)
M.add(AMARILLO(1.5, 3.3, "BURBUJA DE GAS", y=1720))
M.fx(50.05, "pop", -10)
# 18 · el crujido es la burbuja naciendo
M.plano(52.15, 54.95, ART, [BG("bg_articulacion"), hsup, hinf([{"t": 0, "y": 1380}]),
        IMG("burbuja", ancho=190, x=540, y=1010, z=0.55, anim={"pulso": [0.05, 0.5]}), brillo(540, 990, 200, "#dff6ff", 0.4, 0.5, pulso=[0.2, 0.5])],
        cam(1.5, 1.7, (540, 990), (540, 990)), vineta=0.65)
M.add(CRAC(0.2, 2.6, 540, 1560, tam=130, rot=-6))
M.fx(52.35, "tic", -10)
# 19 · bucle: ¿con qué mano lo haces?
M.plano(54.95, 57.7, CALIDO, [brillo(540, 900, 700, "#ffb860", 0.35), mano("mano_izq", 290, 1150, 440, anim={"balanceo": [2, 0.5]}),
        mano("mano_der", 790, 1150, 440, anim={"balanceo": [2, 0.5]})], cam(1.06, 1.0, (540, 1080), (540, 1100)), entrada="zoom", dur=0.35, vineta=0.6)
M.add(ROT(0.8, 2.7, "?", tam=220, color="#ffd23f", capsula=None, x=540, y=760, anim={"flotar": [10, 1.2]}))

M.guardar("01", "crujir-nudillos", 57.7, ["sesenta", "Unger", "artritis", "experimento", "izquierda", "derecha", "Ig", "Nobel", "resonancia",
                                           "burbuja", "gas", "crujido"],
          {"generar": "curiosidad", "semilla": 11}, audio_dir=sys.argv[2])
