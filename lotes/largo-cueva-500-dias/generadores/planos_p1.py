"""Parte 1 (palabras 0–286): «Imagina que bajas a una cueva.» … «Y está condenado a fallar.»"""
from comun import *  # noqa: F401,F403
import comun


def planos(v, plano):
    w = v.w
    # cruces de murciélagos de esta parte (tiempo absoluto: siguen de un plano a otro)
    comun.VUELOS += [(w(19), w(19) + 6.5, (1300, 560), (-300, 470), 150), (w(200), w(200) + 7, (-300, 520), (1350, 610), 130)]

    @plano(0, "gancho: bajas por el pozo")
    def _(d):
        # Gancho: ella ya está bajando en el fotograma 0, la luz de arriba se aleja y cae polvo
        return P(["#0d0b0a", "#030304"], [
            fondo("bg_cueva_pozo"),
            brillo(540, 430, 260, "#fff3d6", 0.5, 0.1, pulso=[0.1, 1.1]),
            {**polvo("#fff3d6", 40, (300, 420, 780, 1500), 3), "vel": [4, 60]},
            pie("bea_baja_cuerda", 560, 1500, 1150, z=0.6, keys=K(d, (0, {"y": 520}), (1, {"y": 1080, "ease": "suave"}))),
            brillo(640, 600, 170, "#ffe2a8", 0.65, 0.62, keys=K(d, (0, {"y": 160}), (1, {"y": 720, "ease": "suave"}))),
            IMG("estalactita_c", ancho=200, x=-150, y=420, z=0.8), IMG("estalactita_a", ancho=150, x=1250, y=380, z=0.8),
            pie("rocas_primer_plano_b", 540, 1920, 520, z=0.9)],
            cam(1.0, 1.18, (540, 960), (560, 1050)), vineta=0.7,
            sfx=[(0.02, "roce", -18), (0.4, "golpe", -24), (d * 0.6, "roce", -24)])

    @plano(6, "setenta metros: corte de la montaña")
    def _(d):
        return P(["#7fb6dd", "#2a1d14"], [
            fondo("bg_corte_tierra"),
            flecha([[605, 470], [605, 1250]], 0.1, d * 0.75, CIAN, 8, [18, 14]),
            brillo(605, 1330, 120, "#ffcf8a", 0.8, 0.5, pulso=[0.2, 0.6]),
            pie("bea_despide", 600, 470, 90, z=0.55, keys=aparece(0.05)),
            senala(605, 1330, d * 0.7, d - 0.05, 90, AMBAR)],
            cam(1.0, 1.08, (605, 900), (605, 1100)), "corte",
            hud=[contador(0.1, d - 0.05, 0, 70, d * 0.7, " m", tam=120, x=820, y=900, color="#ffffff", capsula="#0b0f1ed8", miles=False)],
            sfx=[(d * 0.72, "ding", -20)])

    @plano(10, "sin reloj: el reloj de arena se pierde en la oscuridad")
    def _(d):
        return P(["#141018", "#050507"], [
            fondo("bg_negro_cueva"), brillo(540, 900, 380, "#ffcf8a", 0.4),
            pieza("reloj_arena_a", 540, 900, 300, z=0.6, keys=K(d, (0, {"escala": 1.0, "rot": 0, "op": 1}), (1, {"escala": 0.55, "rot": 25, "op": 0.0, "y": 1050, "ease": "entrada"}))),
            IMG("estalactita_b", ancho=130, x=-200, y=400, z=0.8), IMG("estalactita_a", ancho=120, x=1300, y=420, z=0.8)],
            cam(1.08, 1.0, (540, 920)), "corte", sfx=[(0.05, "zap", -22)])

    @plano(12, "sin teléfono: el móvil se apaga")
    def _(d):
        return P(["#141018", "#050507"], [
            fondo("bg_negro_cueva"), brillo(540, 920, 420, "#9fc4ff", 0.5, keys=K(d, (0, {"op": 1}), (0.8, {"op": 0}))),
            pieza("telefono_movil", 540, 930, 300, z=0.6, keys=K(d, (0, {"rot": -8, "op": 1}), (0.85, {"rot": 6, "y": 1010, "op": 0.15, "ease": "entrada"}))),
            IMG("estalactita_c", ancho=180, x=-350, y=430, z=0.8), IMG("estalactita_b", ancho=140, x=1400, y=420, z=0.8)],
            cam(1.0, 1.06, (540, 930)), "corte", sfx=[(d * 0.55, "zap", -24)])

    @plano(15, "sin ver el sol: el amanecer se tapa")
    def _(d):
        return P(["#f7a85c", "#2b1a2e"], [
            fondo("bg_amanecer"), brillo(540, 1000, 500, "#ffd59a", 0.6, 0.1),
            negro(K(d, (0, {"op": 0.0}), (0.45, {"op": 0.0}), (1, {"op": 1.0, "ease": "entrada"})))],
            cam(1.0, 1.1, (540, 1000)), "corte", sfx=[(0.05, "brillo", -22)])

    @plano(19, "y te quedas ahí, completamente sola")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento_oscura"),
            pie("bea_lee_a", 540, 1300, 300, z=0.5),
            pie("lampara_led", 700, 1300, 110, z=0.52),
            brillo(690, 1230, 230, "#ffcf8a", 0.55, 0.51, pulso=[0.08, 1.6]),
            *ambiente_cueva(d, sem=2, oscura=True, primer_plano="rocas_primer_plano_a")],
            cam(1.45, 1.0, (540, 1150)), "corte",
            sfx=[(0.1, "rumor", -26, {"dur": 2.5})])

    @plano(25, "un día, alguien baja a buscarte")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_galeria"),
            *flip(["equipo_frontal_a", "equipo_frontal_b"], d, fps=3, base=lambda n: pie(n, 540, 1360, 330, z=0.5,
                  keys=K(d, (0, {"escala": 0.65, "y": 1250}), (1, {"escala": 1.05, "y": 1330, "ease": "suave"})))),
            brillo(560, 1120, 300, "#fff1c8", 0.4, 0.4, pulso=[0.12, 0.5]),
            *ambiente_cueva(d, sem=3, gotas=True)],
            cam(1.0, 1.12, (540, 1100)), "desenfoque",
            sfx=[(0.1, "golpe", -28), (0.6, "golpe", -29), (1.1, "golpe", -28)])

    @plano(32, "te dice que ya está")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento"),
            pie("colchon", 640, 1300, 160, z=0.45),
            pie("bea_lee_b", 650, 1290, 320, z=0.5, keys=late(0.3, 1, 0.04)),
            pie("equipo_frontal_a", 230, 1300, 340, z=0.55),
            pie("pila_libros" if False else "libro_c", 860, 1300, 60, z=0.52), pie("libro_a", 860, 1260, 60, z=0.53),
            pie("mesa_campamento", -250, 1300, 260, z=0.5), pie("garrafa_agua", 1300, 1300, 160, z=0.5),
            *ambiente_cueva(d, sem=4)],
            cam(1.0, 1.08, (540, 1150), (600, 1150)), "corte")

    @plano(42, "tú no lo entiendes")
    def _(d):
        return P(["#1a120d", "#050507"], [
            fondo("bg_cueva_campamento"),
            pieza("bea_cara_sorpresa", 540, 980, 980, z=0.6, keys=K(d, (0, {"escala": 0.96}), (1, {"escala": 1.04}))),
            brillo(380, 700, 300, "#ffcf8a", 0.35, 0.65)],
            cam(1.0, 1.15, (540, 900)), "corte", sfx=[(0.05, "golpe", -20)])

    @plano(46, "según tus cuentas: rayas en la pared")
    def _(d):
        rayas = [tiza(330 + 44 * i + (14 if i % 5 == 4 else 0), 760, 0.04 + 0.06 * i, 170) for i in range(10)]
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"), brillo(540, 760, 420, "#ffcf8a", 0.35, 0.3),
            IMG("moho_pared", ancho=420, x=820, y=640, z=0.32, op=0.6), *rayas,
            *[tiza(-420 + 44 * i, 740, 0.06 * i, 150) for i in range(7)], *[tiza(1180 + 44 * i, 720, 0.05 * i, 160) for i in range(8)],
            pie("bea_marca_b", 240, 1300, 640, z=0.6, keys=K(d, (0, {"x": 200}), (1, {"x": 230})))],
            cam(1.25, 1.12, (520, 900)), "corte", sfx=[(0.05 + 0.06 * i, "tic", -25) for i in range(0, 10, 2)])

    @plano(49, "cinco meses y medio")
    def _(d):
        return P(["#3d2a1f", "#1a120d"], [
            fondo("bg_cueva_campamento"),
            pie("cifra_marco", 540, 1150, 400, z=0.5, keys=aparece(0.05)),
            *ambiente_cueva(d, sem=5)],
            cam(1.0, 1.06, (540, 1000)), "corte",
            hud=[contador(0.2, d - 0.05, 0, 5.5, d * 0.6, " meses", decimales=1, tam=110, x=540, y=960, color="#ffd23f", capsula=None)],
            sfx=[(0.2, "tictac", -26, {"dur": d * 0.55, "ritmo": 0.09})])

    @plano(57, "llevas casi un año y medio")
    def _(d):
        return P(["#3d2a1f", "#0b0705"], [
            fondo("bg_cueva_campamento"),
            pieza("calendario_diciembre", 540, 950, 520, z=0.55, keys=K(d, (0, {"rot": -4}), (1, {"rot": 3}))),
            fundido_blanco(K(d, (0, {"op": 0.85}), (0.25, {"op": 0.0}))),
            *ambiente_cueva(d, sem=6)],
            cam(1.0, 1.2, (540, 950)), "corte",
            hud=[rotulo(0.15, d - 0.05, "500 DÍAS", tam=150, color="#ffffff", capsula="#c0392be6", y=1300)],
            sfx=[(0.0, "impacto", -12)])
