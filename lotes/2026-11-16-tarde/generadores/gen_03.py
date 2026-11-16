"""03 — Tu móvil y el ordenador del Apolo 11. Uso: python3 gen_03.py DIR_SALIDA DIR_AUDIO"""
import sys
from base import IMG, BG, ROT, AMARILLO, CONTEXTO, polvo, brillo, cam, Montaje

M = Montaje(sys.argv[1])
ESP = ["#02030a", "#0a1030"]
TALLER = ["#1d2430", "#0b0f16"]
VERDE = ["#1f3a2a", "#0c1a12"]
estrellas = polvo("#ffffff", 40, (0, 0, 1080, 1920), 3, "estrellas")
COBRE = "#f0a050"


def movil(x, y, ancho, nombre="movil", z=0.55, **kw):
    return IMG(nombre, ancho=ancho, x=x, y=y, z=z, **kw)


def agc(x, y, ancho, z=0.5, **kw):
    return IMG("agc", ancho=ancho, x=x, y=y, z=z, **kw)


# 1 · gancho: el móvil enorme frente al ordenador del Apolo
M.plano(0, 2.3, TALLER, [brillo(540, 900, 650, "#6fa0ff", 0.3), movil(330, 1150, 440, anim={"flotar": [8, 2]}),
        agc(820, 1330, 330, keys=[{"t": 0, "escala": 1.0}, {"t": 2.3, "escala": 0.9}]), brillo(330, 1100, 260, "#9fc0ff", 0.4, 0.5, pulso=[0.2, 0.8])],
        cam(1.0, 1.05, (540, 1150), (540, 1120)), vineta=0.6)
M.add({"tipo": "rotulo", "texto": "×1.000.000", "unidad": "VECES", "tam": 100, "x": 540, "y": 1720, "hud": True, "z": 1, "anim": {"pulso": [0.04, 0.8]}})
M.fx(0.2, "zap", -16)
# 2 · el ordenador del Apolo 11 de cerca
M.plano(2.3, 4.45, TALLER, [brillo(540, 900, 600, "#ffffff", 0.2), agc(540, 1100, 900),
        brillo(700, 920, 120, "#3dff6e", 0.6, 0.6, pulso=[0.3, 0.6])], cam(1.0, 1.06, (540, 1050), (560, 1030)), vineta=0.6)
M.add(ROT(0.2, 2.0, "ORDENADOR DEL APOLO 11", tam=54, color="#ffffff", capsula="#c0392be6", x=540, y=1640))

# 3 · 1969: la nave que llevó a Armstrong y Aldrin a la Luna
nave = IMG("modulo_lunar", ancho=260, z=0.6, anim={"balanceo": [3, 2]}, keys=[{"t": 0, "x": 300, "y": 1400}, {"t": 4.4, "x": 720, "y": 760, "ease": "suave"}])
M.plano(4.45, 8.95, ESP, [BG("bg_espacio"), IMG("tierra_hd", ancho=520, x=200, y=1620, z=0.3, anim={"girar": 3}), IMG("luna_hd", ancho=420, x=820, y=560, z=0.3),
        nave, {"tipo": "flecha", "puntos": [[260, 1480], [520, 1100], [700, 820]], "grosor": 7, "color": "#ffffffaa", "discontinua": [18, 14], "z": 0.5,
               "keys": [{"t": 0, "progreso": 0}, {"t": 4.0, "progreso": 1}]}],
        cam(1.0, 1.06, (540, 1050), (580, 960)), entrada="desenfoque", dur=0.35, vineta=0.55)
M.add(CONTEXTO(0.1, 4.3, "1969 · ARMSTRONG Y ALDRIN"))
M.fx(4.5, "whoosh", -16)
# 4 · se guiaba con un ordenador de unos 32 kilos
M.plano(8.95, 12.25, TALLER, [brillo(540, 900, 600, "#ffffff", 0.2), agc(540, 1150, 820, keys=[{"t": 0, "y": 900}, {"t": 0.5, "y": 1150, "ease": "rebote"}]),
        brillo(700, 970, 110, "#3dff6e", 0.6, 0.6, pulso=[0.3, 0.6])], cam(1.0, 1.05, (540, 1100), (540, 1080)), entrada="zoom", dur=0.35, vineta=0.6)
M.add(ROT(1.6, 3.2, "32", unidad="KILOS", tam=130, x=540, y=1640, contar=[0, 32, 0.8], contar_desde=1.6))
M.fx(9.45, "golpe", -12)
# 5 · del tamaño de un maletín
M.plano(12.25, 14.05, TALLER, [agc(330, 1150, 480), IMG("maletin", ancho=440, x=800, y=1200, z=0.5,
        keys=[{"t": 0, "x": 1300}, {"t": 0.5, "x": 800, "ease": "salida"}])], cam(1.0, 1.04, (540, 1150), (540, 1150)), vineta=0.6)
M.add(ROT(0.6, 1.8, "=", tam=160, color="#ffffff", capsula=None, x=575, y=1150))
M.fx(12.3, "whoosh", -16)

# 6 · memoria de trabajo: 2.048 palabras (zoom al teclado)
M.plano(14.05, 17.6, TALLER, [agc(540, 1100, 900), brillo(700, 920, 160, "#3dff6e", 0.7, 0.6, pulso=[0.3, 0.4])],
        cam(1.7, 1.8, (720, 960), (720, 960)), entrada="desenfoque", dur=0.3, vineta=0.6)
M.add(ROT(1.6, 3.5, "2.048", unidad="PALABRAS", tam=120, x=540, y=1640, contar=[0, 2048, 1.0], contar_desde=1.6))
# 7 · 4 kilobytes, menos que una foto
def barra_h(y, prog, color, t0):
    return {"tipo": "barra", "x": 540, "y": y, "ancho": 860, "alto": 70, "color": color, "fondo": "#ffffff18", "z": 0.6,
            "keys": [{"t": t0, "progreso": 0}, {"t": t0 + 1.0, "progreso": prog, "ease": "salida"}]}


M.plano(17.6, 21.75, ["#16203a", "#080c18"], [movil(540, 900, 420, anim={"flotar": [6, 2]}), barra_h(1450, 0.012, "#3dff6e", 0.3), barra_h(1620, 1.0, "#ffb05a", 2.2),
        ROT(0.3, 4.1, "APOLO · 4 KB", tam=46, color="#ffffff", capsula="#0d1330d8", x=290, y=1370),
        ROT(2.2, 4.1, "UNA FOTO", tam=46, color="#ffffff", capsula="#0d1330d8", x=240, y=1540)],
        cam(1.0, 1.04, (540, 1100), (540, 1100)), entrada="zoom", dur=0.35, vineta=0.6)
M.fx(19.8, "trazo", -16)

# 8 · su reloj: 0,04 megahercios (un parpadeo lentísimo)
M.plano(21.75, 25.65, TALLER, [agc(540, 1100, 820), brillo(700, 920, 200, "#3dff6e", 0.8, 0.6, keys=[{"t": 0, "op": 0.2}, {"t": 1.3, "op": 1}, {"t": 2.6, "op": 0.2}, {"t": 3.9, "op": 1}])],
        cam(1.0, 1.05, (540, 1050), (560, 1030)), entrada="desenfoque", dur=0.3, vineta=0.6)
M.add(ROT(1.3, 3.8, "0,04", unidad="MHZ", tam=130, x=540, y=1640), CONTEXTO(0.2, 1.4, "RELOJ"))
M.fx(23.05, "tic", -14); M.fx(25.65 - 0.1, "tic", -14)
# 9 · un móvil de hoy: miles de megahercios y gigas de memoria
destellos = [brillo(540, 900, 260, "#9fc0ff", 0.7, 0.6, pulso=[0.35, 0.15])]
M.plano(25.65, 30.0, ["#16203a", "#080c18"], [movil(540, 1000, 560), *destellos, polvo("#9fc0ff", 40, (100, 300, 980, 1700), 5, "chispas")],
        cam(1.0, 1.06, (540, 1000), (540, 980)), entrada="zoom", dur=0.35, vineta=0.55)
M.add(ROT(0.6, 2.4, "MILES DE MHZ", tam=72, color="#ffffff", capsula="#0d1330d8", x=540, y=1640),
      ROT(2.4, 4.3, "GIGAS", tam=100, color="#ffd23f", capsula="#0d1330d8", x=540, y=1640))
M.fx(25.7, "zap", -14)
# 10 · más de un millón de veces más
M.plano(30.0, 32.45, TALLER, [movil(330, 1150, 440), agc(820, 1360, 240), brillo(330, 1100, 300, "#9fc0ff", 0.4, 0.5, pulso=[0.2, 0.6])],
        cam(1.0, 1.05, (540, 1150), (540, 1130)), entrada="desenfoque", dur=0.3, vineta=0.6)
M.add(ROT(0.1, 2.3, "1.000.000", unidad="VECES MÁS", tam=100, x=540, y=1720, contar=[1, 1000000, 1.4], contar_desde=0.1, contar_prefijo="+"))
M.fx(30.05, "brillo", -14)

# 11 · lo más increíble: el programa no se descargaba
M.plano(32.45, 35.75, VERDE, [BG("bg_nucleos"), brillo(540, 960, 500, "#ffcf8a", 0.25, 0.5, pulso=[0.1, 1.5])],
        cam(1.0, 1.05, (540, 1000), (540, 960)), entrada="zoom", dur=0.35, vineta=0.6)
M.add(AMARILLO(1.0, 3.3, "NO SE DESCARGABA", y=1720), CONTEXTO(0.2, 1.4, "MEMORIA DE CUERDA"))
# 12 · se tejía a mano
M.plano(35.75, 37.35, VERDE, [BG("bg_nucleos"), IMG("manos_tejer", ancho=900, x=540, y=1150, z=0.6, anim={"balanceo": [3, 0.6]})],
        cam(1.2, 1.25, (540, 1100), (540, 1100)), vineta=0.6)
M.add(AMARILLO(0.2, 1.6, "A MANO", y=1720))
# 13 · trabajadoras de una fábrica, hilos de cobre y anillos
hilo = {"tipo": "flecha", "puntos": [[60, 1080], [300, 1030], [460, 1130], [620, 1030], [780, 1130], [1020, 1060]], "grosor": 7, "color": COBRE,
        "punta": False, "z": 0.6, "keys": [{"t": 0.2, "progreso": 0}, {"t": 2.6, "progreso": 1}]}
M.plano(37.35, 40.05, VERDE, [BG("bg_nucleos"), hilo, IMG("manos_tejer", ancho=760, z=0.65, y=1250, anim={"balanceo": [3, 0.6]},
        keys=[{"t": 0, "x": 300}, {"t": 2.6, "x": 760}])], cam(1.0, 1.04, (540, 1050), (540, 1050)), vineta=0.6)
M.add(CONTEXTO(0.2, 2.6, "TRABAJADORAS · HILO DE COBRE"))
M.plano(40.05, 43.55, VERDE, [BG("bg_nucleos")], cam(2.0, 2.15, (380, 980), (420, 990)), vineta=0.65)
M.add(AMARILLO(0.8, 3.4, "ANILLOS MAGNÉTICOS", y=1720))

# 14 · dentro, un uno
def plano_anillo(ini, fin, puntos, cifra, color, dentro=False):
    def cable(pts, t0, t1):
        return {"tipo": "flecha", "puntos": pts, "grosor": 14, "color": COBRE, "punta": False, "z": 0.6,
                "keys": [{"t": t0, "progreso": 0}, {"t": t1, "progreso": 1}]}
    if dentro:  # entra por el agujero y sale por debajo del anillo (el tramo de salida va detrás)
        els = [brillo(540, 960, 500, "#3dff6e", 0.15), cable([[540, 1060], [700, 1200], [1080, 1330]], 0.55, 1.0),
               IMG("anillo", ancho=820, x=540, y=1000, z=0.5), cable([[0, 640], [300, 820], [540, 1000]], 0.05, 0.55)]
    else:
        els = [brillo(540, 960, 500, "#3dff6e", 0.15), IMG("anillo", ancho=820, x=540, y=1000, z=0.5), cable(puntos, 0.1, 1.0)]
    M.plano(ini, fin, VERDE, els, cam(1.0, 1.03, (540, 1000), (540, 1000)), vineta=0.6)
    M.add(ROT(0.6, fin - ini - 0.1, cifra, tam=200, color=color, capsula="#0d1330d8", x=540, y=1600))


plano_anillo(43.55, 45.2, None, "1", "#3dff6e", dentro=True)
M.add(CONTEXTO(0.1, 1.5, "POR DENTRO"))
M.fx(44.2, "ding", -14)
plano_anillo(45.2, 46.85, [[0, 760], [250, 800], [540, 760], [840, 800], [1080, 900]], "0", "#ff6a5a")
M.add(CONTEXTO(0.1, 1.5, "POR FUERA"))
M.fx(45.85, "tic", -12)

# 15 · con eso aterrizaron en la Luna
lm = IMG("modulo_lunar", ancho=420, x=560, z=0.6, keys=[{"t": 0, "y": 700}, {"t": 1.6, "y": 1230, "ease": "salida"}])
polvo_luna = {"tipo": "particulas", "clase": "polvo", "color": "#d8d8d8", "area": [300, 1300, 820, 1420], "n": 50, "tam": [4, 10], "vel": [0, -40], "z": 0.65, "semilla": 7}
M.plano(46.85, 48.95, ["#02030a", "#02030a"], [BG("bg_superficie"), IMG("tierra_hd", ancho=240, x=820, y=420, z=0.1, anim={"girar": 3}), lm, polvo_luna],
        cam(1.0, 1.05, (540, 1100), (560, 1150)), entrada="zoom", dur=0.35, vineta=0.6)
M.add(CONTEXTO(0.2, 2.0, "20 DE JULIO DE 1969"))
M.fx(46.9, "meteoro", -22); M.fx(48.4, "golpe", -14)
# 16 · bucle: y tú lo usas para ver vídeos como este
M.plano(48.95, 51.86, TALLER, [brillo(540, 900, 650, "#6fa0ff", 0.3), movil(540, 1100, 560, nombre="movil_video", anim={"flotar": [8, 2]}),
        agc(860, 1500, 240, keys=[{"t": 0, "op": 0}, {"t": 1.2, "op": 0}, {"t": 1.6, "op": 1}])],
        cam(1.15, 1.0, (540, 1050), (540, 1150)), entrada="zoom", dur=0.35, vineta=0.6)

M.guardar("03", "movil-apolo-11", 51.86, ["millón", "Apolo", "treinta", "kilos", "maletín", "memoria", "kilobytes", "megahercios", "gigas",
                                          "tejía", "mano", "anillos", "uno", "cero", "Luna"],
          {"generar": "misterio", "semilla": 31}, audio_dir=sys.argv[2])
