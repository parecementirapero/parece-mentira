"""Corto vertical (~62 s) de «El que copiaba»: MISMA locución recortada (gen.py --corto, OMITIR_CORTO).
Estilo B elegido por Jorge: fondos apagados y casi en gris (`<fondo>_b`), focos de luz sobre lo importante y
contadores arriba (debajo del subtítulo). Índices de palabra = los del largo."""
from comun_cp import *  # noqa: F401,F403
from planos_p2 import pos, mece, aspa, visto, onda, camina  # noqa: F401

FONDO_B = ["#15161c", "#07080b"]
HUD_Y = 650       # fila de contadores (bajo el subtítulo)


def foco(x, suelo, alto=1500, frio=False, z=0.08, t0=0.0, op=0.9):
    """Cono de luz de escenario que cae sobre x (se enciende en t0 con un parpadeo)."""
    n = "foco_luz_frio" if frio else "foco_luz"
    ks = [{"t": 0, "op": 0 if t0 > 0 else op}, {"t": t0, "op": 0}, {"t": t0 + 0.06, "op": op}, {"t": t0 + 0.1, "op": op * 0.4},
          {"t": t0 + 0.16, "op": op}] if t0 > 0 else [{"t": 0, "op": op}]
    return pie(n, x, suelo + 30, alto, z=z, keys=ks)


def etiqueta(t0, t1, texto, x, y=HUD_Y - 95, color="#dfe3ea", tam=46):
    return rotulo(t0, t1, texto, tam=tam, x=x, y=y, color=color, sin_pop=True)


def cifra(t0, t1, desde, hasta, dur, x, unidad="", color=BLANCO, y=HUD_Y, tam=110, **k):
    return contador(t0, t1, desde, hasta, dur, unidad, tam=tam, x=x, y=y, color=color, capsula="#0b0d14d0", **k)


def planos(v, plano):
    w = v.w

    # ------------------------------------------------------------------ GANCHO (0–17)
    @plano(0, "colegio: Lucas copia de reojo")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_aula_b"), foco(400, 1420, t0=0.0), foco(760, 1420, frio=True, op=0.5),
            pie("lucas_nino_reojo", 400, 1420, 560, z=0.5, keys=arranque(400, ypie("lucas_nino_reojo", 1420, 560), d, "abajo", 160)),
            pie("pupitre", 400, 1500, 330, z=0.55),
            pie("marta_nina_escribe_a", 760, 1420, 560, z=0.5, op=0.75), pie("pupitre", 760, 1500, 330, z=0.55, op=0.8),
            flecha([[470, 1010], [690, 1080]], 0.2, 0.7, ORO, 10, [16, 12], z=0.7)],
            cam(1.25, 1.0, (500, 1150)), "corte",
            hud=[rotulo(0.2, d - 0.02, "LUCAS", tam=64, x=400, y=820, color=CIAN, capsula="#0b0d14d0", sin_pop=True),
                 rotulo(0.25, d - 0.02, "MARTA", tam=64, x=760, y=820, color=ORO, capsula="#0b0d14d0", sin_pop=True)],
            sfx=[(0.05, "roce", -20)])

    @plano(3, "copiar = suspenso: la nota cae")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_estudio_oscuro_b"), foco(540, 1400),
            pieza("p1_examen_blanco", 540, 1000, 520, z=0.5, keys=[{"t": 0, "rot": -4}, {"t": d, "rot": 2}]),
            pieza("p1_nota_roja", 540, 980, 360, z=0.6, keys=cae(d * 0.55, d * 0.55 + 0.2, 300, 980))],
            cam(1.0, 1.08, (540, 1000)), "corte", hud=[etiqueta(0.05, d - 0.05, "EN EL COLEGIO", 540)],
            sfx=[(d * 0.55 + 0.2, "golpe", -14)])

    @plano(8, "en la vida real: Lucas ante su local con cola")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_calle_dia_b"), foco(700, 1440, alto=1600),
            pie("hamburgueseria_lucas", 760, 1440, 640, z=0.4),
            *cola(560, 1440, n=5, alto=420, paso=110, z=0.5, avanza=(d * 0.5, 30)),
            pie("lucas_delantal", 980, 1440, 600, z=0.55, keys=mece(d, 2)),
            pie("hamburgueseria", 1500, 1440, 640, z=0.4)],
            cam(1.0, 1.1, (700, 1150)), "desenfoque",
            hud=[etiqueta(0.1, d - 0.05, "EN LA VIDA", 540)], sfx=[(0.1, "brillo", -24)])

    @plano(12, "copiar bien: el dinero sube")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_estudio_oscuro_b"), foco(540, 1400),
            pie("saco_dinero", 540, 1400, 520, z=0.5, keys=late(d * 0.7, 2, 0.08)),
            *[pie("monedas", x, 1400, 140, z=0.52, keys=cae(0.1 + i * 0.12, 0.35 + i * 0.12, 200, ypie("monedas", 1400, 140)))
              for i, x in enumerate((300, 780, 420, 680))]],
            cam(1.05, 1.0, (540, 1150)), "corte",
            hud=[cifra(0.05, d - 0.05, 0, 250000, d * 0.85, 540, " €", color=ORO, miles=True)], sfx=[(0.2, "ding", -20)])

    # ------------------------------------------------------------------ MARTA (150–172, 211–222, 243–246)
    @plano(150, "Marta se pasa meses pensando")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_cafe_dentro_b"), foco(540, 1430),
            pie("marta_piensa", 540, 1430, 820, z=0.5, keys=mece(d, 2)),
            pie("bombilla_a", 760, 760, 220, z=0.6, keys=[{"t": 0, "op": 0.5}, {"t": d, "op": 0.9}])],
            cam(1.0, 1.1, (540, 1100)), "corte",
            hud=[etiqueta(0.05, d - 0.05, "MESES PENSANDO", 540), cifra(0.05, d - 0.05, 0, 14, d * 0.9, 540, color=ORO)])

    @plano(155, "y al final la tiene: la bombilla")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_estudio_oscuro_b"), foco(540, 1400),
            pieza("bombilla_a", 540, 1000, 420, z=0.5, keys=[{"t": 0, "op": 1}, {"t": d * 0.4, "op": 1}, {"t": d * 0.42, "op": 0}]),
            pieza("bombilla_b", 540, 1000, 420, z=0.51, keys=[{"t": 0, "op": 0}, {"t": d * 0.4, "op": 0}, {"t": d * 0.42, "op": 1}] + late(d * 0.45, 1, 0.1)),
            brillo(540, 960, 380, ORO, 0.6, 0.45, keys=[{"t": 0, "op": 0}, {"t": d * 0.42, "op": 0}, {"t": d * 0.5, "op": 1}])],
            cam(1.0, 1.12, (540, 1000)), "corte", sfx=[(d * 0.42, "ding", -16)])

    @plano(160, "una cafetería donde pagas el tiempo")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_calle_dia_b"), foco(540, 1440, alto=1600),
            pie("cafeteria_marta", 540, 1440, 760, z=0.45, keys=arranque(540, ypie("cafeteria_marta", 1440, 760), d, "abajo", 200)),
            pie("marta_idea", 920, 1440, 600, z=0.55)],
            cam(1.0, 1.08, (560, 1100)), "corte", hud=[etiqueta(0.1, d - 0.05, "CAFETERÍA", 540)], sfx=[(0.1, "golpe", -22)])

    @plano(167, "pagas el tiempo que te quedas")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_estudio_oscuro_b"), foco(540, 1400),
            pie("reloj_arena_grande", 540, 1400, 640, z=0.5, keys=[{"t": 0, "rot": 0}, {"t": d * 0.6, "rot": 0}, {"t": d, "rot": 180, "ease": "suave"}])],
            cam(1.08, 1.0, (540, 1100)), "corte",
            hud=[etiqueta(0.05, d - 0.05, "PAGAS EL TIEMPO", 540), cifra(0.05, d - 0.05, 0, 60, d * 0.85, 540, " min", color=ORO)],
            sfx=[(0.1, "tictac", -24)])

    @plano(211, "cada cliente necesita una explicación")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_cafe_dentro_b"), foco(380, 1430), foco(760, 1430, frio=True, op=0.6),
            *flip(["marta_explica_a", "marta_explica_b"], d, fps=3, base=lambda n: pie(n, 380, 1430, 760, z=0.5)),
            pie("cliente_confuso_1", 790, 1430, 740, z=0.52), pie("cliente_confuso_2", 1100, 1430, 740, z=0.5)],
            cam(1.0, 1.06, (560, 1120)), "corte",
            hud=[etiqueta(0.05, d - 0.05, "EXPLICACIONES", 540), cifra(0.05, d - 0.05, 0, 312, d * 0.9, 540, color=BLANCO)])

    @plano(218, "y la mayoría no vuelve")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_calle_dia_b"), foco(540, 1440, frio=True),
            pie("cafeteria_marta", 540, 1440, 760, z=0.4),
            *camina("cliente_se_va", 700, -300, 1440, 640, d, z=0.55)],
            cam(1.0, 1.05, (540, 1100)), "corte",
            hud=[etiqueta(0.05, d - 0.05, "CLIENTES", 540), cifra(0.05, d - 0.05, 3, 0, d * 0.8, 540, color=ROJO)])

    @plano(243, "y baja la persiana")
    def _(d):
        P0 = PERSIANA
        alto = 760
        k = alto / P0["H"]
        yfach = ypie("cafeteria_marta", 1440, alto)
        x_p = 540 + (P0["x0"] + P0["w"] / 2 - P0["W"] / 2) * k
        y_p = yfach + (P0["y0"] + P0["h"] / 2 - P0["H"] / 2) * k
        return P(FONDO_B, [
            fondo("bg_calle_dia_b"), foco(540, 1440, op=0.5),
            pie("cafeteria_marta", 540, 1440, alto, z=0.4),
            pieza("persiana", x_p, y_p, P0["w"] * k, z=0.45,
                  keys=[{"t": 0, "ey": 0.02, "y": y_p - P0["h"] * k / 2}, {"t": d * 0.75, "ey": 1.0, "y": y_p, "ease": "entrada"}]),
            pie("marta_triste", 980, 1440, 600, z=0.55)],
            cam(1.0, 1.06, (560, 1100)), "corte", sfx=[(0.05, "roce", -14), (d * 0.75, "golpe", -12)])

    # ------------------------------------------------------------------ LUCAS (247–269, 290–310, 328–334)
    @plano(247, "mientras tanto, Lucas pasea")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_ciudad_b"), foco(540, 1390, frio=True),
            *camina("lucas_camina", 160, 760, 1390, 640, d, z=0.55)],
            cam(1.0, 1.05, (540, 1100)), "corte", hud=[etiqueta(0.05, d - 0.05, "MIENTRAS TANTO…", 540)])

    @plano(256, "y se fija en una cosa")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_ciudad_b"), foco(300, 1390, frio=True),
            pie("lucas_piensa", 300, 1460, 640, z=0.55),
            pieza("pensamiento_cola", 560, 820, 420, z=0.6, keys=aparece(d * 0.3))],
            cam(1.1, 1.0, (420, 1100)), "corte", sfx=[(d * 0.3, "brillo", -22)])

    @plano(262, "hamburguesería con cola hasta la esquina")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_ciudad_b"), foco(760, 1390, alto=1600),
            pie("hamburgueseria", 820, 1390, 640, z=0.4),
            *cola(640, 1390, n=7, alto=430, paso=100, z=0.5, avanza=(d * 0.5, 25))],
            cam(1.0, 1.08, (600, 1100), (420, 1100)), "corte",
            hud=[etiqueta(0.05, d - 0.05, "EN LA COLA", 540), cifra(0.05, d - 0.05, 0, 37, d * 0.8, 540, " personas", color=ORO)])

    @plano(290, "así que abre otra dos calles más allá")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_calle_dia_b"), foco(560, 1440, t0=0.1),
            pie("hamburgueseria_lucas", 560, 1440, 760, z=0.45, keys=cae(0.05, 0.4, -600, ypie("hamburgueseria_lucas", 1440, 760))),
            pie("lucas_delantal", 960, 1440, 600, z=0.55, keys=aparece(0.5))],
            cam(1.0, 1.06, (600, 1100)), "corte", sfx=[(0.4, "golpe", -12)])

    @plano(299, "igual de buena")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_estudio_oscuro_b"), foco(330, 1400), foco(750, 1400),
            pieza("hamburguesa", 330, 1050, 320, z=0.5, keys=late(0.2, 1, 0.08)),
            pieza("icono_igual", 540, 1050, 160, z=0.55, keys=aparece(0.1)),
            pieza("hamburguesa", 750, 1050, 320, z=0.5, keys=late(0.35, 1, 0.08))],
            cam(1.0, 1.06, (540, 1050)), "corte")

    @plano(302, "con una diferencia")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_estudio_oscuro_b"), foco(540, 1400),
            pieza("icono_rapido", 540, 1020, 380, z=0.5, keys=arranque(540, 1020, d, "abajo", 200))],
            cam(1.0, 1.1, (540, 1020)), "corte", hud=[etiqueta(0.05, d - 0.05, "UNA DIFERENCIA", 540)], sfx=[(0.05, "zap", -20)])

    @plano(305, "allí esperabas veinte minutos")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_ciudad_b"), foco(620, 1390, frio=True),
            pie("hamburgueseria", 700, 1390, 640, z=0.4),
            *cola(560, 1390, n=7, alto=420, paso=95, z=0.5)],
            cam(1.0, 1.05, (560, 1100)), "corte",
            hud=[etiqueta(0.05, d - 0.05, "ALLÍ", 540), cifra(0.05, d - 0.05, 0, 20, d * 0.8, 540, " min", color=ROJO)],
            sfx=[(0.1, "tictac", -26)])

    @plano(309, "aquí, cinco")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_calle_dia_b"), foco(560, 1440),
            pie("hamburgueseria_lucas", 560, 1440, 760, z=0.45),
            pie("cliente_feliz_2", 900, 1440, 600, z=0.55, keys=aparece(0.1)),
            pie("cliente_feliz_1", 220, 1440, 600, z=0.55, keys=aparece(0.3))],
            cam(1.05, 1.0, (560, 1100)), "corte",
            hud=[etiqueta(0.05, d - 0.05, "AQUÍ", 540), cifra(0.05, d - 0.05, 20, 5, d * 0.6, 540, " min", color=VERDE)],
            sfx=[(d * 0.6, "ding", -16)])

    @plano(328, "en un año, dos locales")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_calle_dia_b"), foco(300, 1440), foco(800, 1440, t0=d * 0.45),
            pie("hamburgueseria_lucas", 300, 1440, 640, z=0.42),
            pie("hamburgueseria_lucas", 800, 1440, 640, z=0.4, keys=cae(d * 0.4, d * 0.6, -600, ypie("hamburgueseria_lucas", 1440, 640))),
            pie("lucas_contento", 540, 1460, 640, z=0.6, keys=late(d * 0.65, 1, 0.08))],
            cam(1.0, 1.06, (540, 1100)), "corte",
            hud=[etiqueta(0.05, d - 0.05, "LOCALES DE LUCAS", 540), cifra(0.05, d - 0.05, 1, 2, d * 0.6, 540, color=ORO)],
            sfx=[(d * 0.6, "golpe", -12)])

    # ------------------------------------------------------------------ EL TRUCO (592–603)
    @plano(592, "el truco no es copiar")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_estudio_oscuro_b"), foco(330, 1400, frio=True), foco(750, 1400, frio=True),
            pie("hamburgueseria", 330, 1400, 420, z=0.5), pieza("icono_igual", 540, 1230, 140, z=0.55),
            pie("hamburgueseria", 750, 1400, 420, z=0.5),
            *aspa(540, 1150, 330, d * 0.5)],
            cam(1.0, 1.05, (540, 1150)), "corte", hud=[etiqueta(0.05, d - 0.05, "COPIAR TAL CUAL", 540)], sfx=[(d * 0.5, "zap", -16)])

    @plano(597, "es copiar…")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_estudio_oscuro_b"), foco(540, 1400),
            pie("hamburgueseria", 540, 1400, 560, z=0.5, keys=arranque(540, ypie("hamburgueseria", 1400, 560), d, "abajo", 120))],
            cam(1.0, 1.08, (540, 1150)), "corte", hud=[etiqueta(0.05, d - 0.05, "COPIA…", 540)])

    @plano(599, "y mejorar una sola cosa")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_estudio_oscuro_b"), foco(540, 1400, t0=0.05),
            pieza("icono_mas", 540, 1000, 300, z=0.5, keys=aparece(0.05)),
            pieza("icono_rapido", 300, 1200, 200, z=0.5, keys=aparece(d * 0.3)),
            pieza("icono_barato", 780, 1200, 200, z=0.5, keys=aparece(d * 0.4)),
            pieza("icono_cerca", 380, 1420, 180, z=0.5, keys=aparece(d * 0.5)),
            pieza("icono_bonito", 700, 1420, 190, z=0.5, keys=aparece(d * 0.6))],
            cam(1.0, 1.06, (540, 1150)), "corte",
            hud=[etiqueta(0.05, d - 0.05, "…Y MEJORA", 540), cifra(0.05, d - 0.05, 4, 1, d * 0.8, 540, " cosa", color=ORO)],
            sfx=[(0.05, "ding", -18)])

    # ------------------------------------------------------------------ CIERRE (705–738)
    @plano(705, "nadie te pide ser el primero")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_calle_dia_b"), foco(380, 1440, frio=True, op=0.5),
            pie("cafeteria_marta_cerrada", 380, 1440, 640, z=0.4),
            pie("marta_triste", 760, 1440, 600, z=0.55), *aspa(540, HUD_Y + 20, 110, d * 0.6, z=0.95)],
            cam(1.0, 1.05, (540, 1100)), "corte",
            hud=[rotulo(0.1, d - 0.05, "1º", tam=150, x=540, y=HUD_Y + 20, color="#8a8f99", capsula="#0b0d14d0")],
            sfx=[(d * 0.6, "zap", -18)])

    @plano(714, "te piden ser el mejor")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_calle_dia_b"), foco(540, 1440, alto=1600),
            pie("hamburgueseria_lucas", 540, 1440, 700, z=0.4),
            *cola(380, 1440, n=4, alto=420, paso=100, z=0.5),
            pie("lucas_delantal", 860, 1440, 600, z=0.55, keys=mece(d, 2))],
            cam(1.0, 1.06, (540, 1100)), "corte",
            hud=[rotulo(0.1, d - 0.05, "EL MEJOR", tam=110, x=540, y=HUD_Y, color=ORO, capsula="#0b0d14d0")], sfx=[(0.1, "brillo", -18)])

    @plano(719, "la próxima vez que quieras empezar algo")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_estudio_oscuro_b"), foco(540, 1400),
            pie("marta_idea", 380, 1400, 640, z=0.5), pie("lucas_senala", 720, 1400, 640, z=0.5),
            pieza("bombilla_b", 540, 760, 200, z=0.6, keys=late(d * 0.4, 1, 0.1))],
            cam(1.0, 1.06, (540, 1100)), "corte")

    @plano(728, "no busques la idea que nadie ha tenido")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_estudio_oscuro_b"), foco(540, 1400, frio=True, op=0.5),
            pieza("bombilla_a", 540, 1000, 360, z=0.5, keys=[{"t": 0, "op": 1}, {"t": d, "op": 0.6}]),
            *aspa(540, 1000, 240, d * 0.55)],
            cam(1.0, 1.05, (540, 1000)), "corte", hud=[etiqueta(0.05, d - 0.05, "LA IDEA NUNCA VISTA", 540)], sfx=[(d * 0.55, "zap", -16)])

    @plano(736, "busca la cola")
    def _(d):
        return P(FONDO_B, [
            fondo("bg_ciudad_b"), foco(820, 1390, alto=1600), foco(380, 1390, op=0.6),
            pie("hamburgueseria", 900, 1390, 600, z=0.4),
            *cola(730, 1390, n=9, alto=420, paso=88, z=0.5, avanza=(d * 0.4, 30))],
            cam(1.0, 1.08, (560, 1100)), "corte",
            hud=[rotulo(0.1, d - 0.05, "BUSCA LA COLA", tam=110, x=540, y=HUD_Y, color=ORO, capsula="#0b0d14d0")],
            sfx=[(0.1, "golpe", -12)])


    # ------------------------------------------------------------------ micro planos (golpes)
    def golpe(i, nombre, pieza_n, ancho, texto=None, color=ORO, sfx="golpe", y=1000, fondo_n="bg_estudio_oscuro_b"):
        @plano(i, nombre)
        def _(d):
            els = [fondo(fondo_n), foco(540, 1400),
                   pieza(pieza_n, 540, y, ancho, z=0.5, keys=[{"t": 0, "escala": 1.35, "op": 0.0}, {"t": 0.08, "op": 1},
                                                              {"t": 0.22, "escala": 1.0, "ease": "rebote"}, {"t": d, "escala": 1.06}])]
            hud = [rotulo(0.0, d - 0.02, texto, tam=120, x=540, y=HUD_Y, color=color, capsula="#0b0d14d0", sin_pop=True)] if texto else []
            return P(FONDO_B, els, cam(1.12, 1.0, (540, y)), "corte", hud=hud, sfx=[(0.02, sfx, -14)])

    golpe(7, "suspenso: la nota", "p1_nota_roja", 520, None, sfx="golpe")
    golpe(17, "rico: monedas", "saco_dinero", 520, None, sfx="ding")
    golpe(221, "no vuelve: cliente que se va", "cartel_cerrado", 520, None, sfx="zap")
    golpe(269, "esquina: la cola entera", "hamburguesa", 460, None, sfx="pop")
    golpe(310, "cinco", "icono_rapido", 380, "5 MIN", color=VERDE, sfx="ding")
    golpe(333, "locales", "bolsa_comida", 420, None, sfx="golpe")
    golpe(603, "una sola cosa", "icono_mas", 380, "1", sfx="golpe")
    golpe(718, "el mejor", "hamburguesa", 460, None, sfx="ding")


def ypie(nombre, suelo, alto):
    import comun
    return round(suelo - (comun.APOYO.get(nombre, 0.97) - 0.5) * alto, 1)
