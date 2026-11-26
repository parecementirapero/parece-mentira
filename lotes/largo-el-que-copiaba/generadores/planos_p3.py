"""Parte 3 (palabras 491–748, 186,9 s → final): «Y no hace falta montar una empresa…» … «¿qué copiarías… y qué le cambiarías?»
EN TU VIDA (491–557) · LA TRAMPA (558–614) · EL REGRESO (615–688) · CIERRE (689–748)."""
from comun_cp import *  # noqa: F401,F403
import comun


# ------------------------------------------------------------------ ayudantes propios de la parte 3
def aspa(cx, cy, r, t0, color=ROJO, g=24, z=0.8):
    """Aspa (tachado) que se dibuja en dos trazos."""
    return [flecha([[cx - r, cy - r], [cx + r, cy + r]], t0, t0 + 0.16, color, g, punta=False, z=z),
            flecha([[cx + r, cy - r], [cx - r, cy + r]], t0 + 0.14, t0 + 0.3, color, g, punta=False, z=z)]


def onda(x, y, t0, r=160, color=CIAN, dur=0.8, g=6, z=0.7):
    """Anillo que se abre y se apaga (voz, sonido, aviso)."""
    return {"tipo": "forma", "forma": "elipse", "ancho": r * 2, "alto": r * 2, "relleno": "#ffffff", "op_relleno": 0,
            "grosor": g, "borde": color, "x": x, "y": y, "z": z,
            "keys": [{"t": 0, "escala": 0.15, "op": 0}, {"t": t0, "escala": 0.15, "op": 0}, {"t": t0 + 0.05, "op": 0.9},
                     {"t": t0 + dur, "escala": 1.0, "op": 0.0, "ease": "salida"}]}


def ypie(nombre, suelo, alto):
    """y del centro de una pieza posada en `suelo` (para claves que mueven una pieza de `pie`)."""
    return round(suelo - (comun.APOYO.get(nombre, 0.97) - 0.5) * alto, 1)


def camina(nombres, x0, x1, suelo, alto, d, t0=0.0, t1=None, fps=4, z=0.5, mira=1, op=None):
    """Figura que anda de x0 a x1 alternando fotogramas a/b (mira=-1: espejo)."""
    t1 = d if t1 is None else t1
    def base(n):
        e = pie(n, x0, suelo, alto, z=z, keys=[{"t": 0, "x": x0}, {"t": t0, "x": x0}, {"t": t1, "x": x1, "ease": "lineal"}])
        if mira < 0:
            e["ex"] = -1
        return e
    out = flip(nombres, d, fps=fps, base=base)
    if op:
        for e in out:
            e["keys"] = sorted(e["keys"] + [dict(q) for q in op], key=lambda q: q["t"])
    return out


def sale_suelo(nombre, x, suelo, alto, t0, z=0.5, desde=-600, dur=0.5):
    """Pieza posada que cae del cielo y bota en su suelo."""
    y1 = ypie(nombre, suelo, alto)
    return pie(nombre, x, suelo, alto, z=z, keys=[{"t": 0, "op": 0, "y": desde}, {"t": t0, "op": 0, "y": desde}, {"t": t0 + 0.02, "op": 1}]
               + cae(t0, t0 + dur, desde, y1)[1:])


def estudio(color="#ffcf8a", frio=False, sem=1, n=30):
    """Detalle sobre fondo oscuro: foco desde arriba, halo y polvo en la luz (a todo el ancho)."""
    return [fondo("bg_estudio_oscuro"),
            pie("foco_luz_frio" if frio else "foco_luz", 540, 1400, 1250, z=0.1),
            brillo(540, 1000, 520, color, 0.35, 0.12, pulso=[0.06, 1.4]),
            {**polvo("#fff1c8" if not frio else "#cfe6ff", n, (-500, 500, 1580, 1450), sem), "_ancho": False}]


def fantasmas(nombres, y=900, ancho=230, op=0.22, z=0.2):
    """Piezas tenues que flotan a los lados (solo se ven en el horizontal)."""
    xs = [-420, -200, 1280, 1500]
    return [pieza(n, xs[i % 4], y + (i % 2) * 260 - 130, ancho, z=z, op=op, anim={"flotar": [18, 2.6 + 0.4 * i]})
            for i, n in enumerate(nombres)]


def check(x, y, t0, z=0.8):
    """Visto verde que se dibuja (alguien entiende)."""
    return flecha([[x - 34, y], [x - 8, y + 28], [x + 42, y - 34]], t0, t0 + 0.25, VERDE, 14, punta=False, z=z)


def planos(v, plano):
    w = v.w

    def rel(i0):
        return lambda j: round(w(j) - w(i0), 3)

    # ============================================================ EN TU VIDA (491–557)
    @plano(491, "no hace falta montar una empresa")
    def _(d):
        o = rel(491)
        S = 1440
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pie("hamburgueseria_lucas", 120, S - 20, 720, z=0.3, keys=K(d, (0, {"escala": 1.0}), (1, {"escala": 0.97}))),
            pie("hamburgueseria_lucas", 960, S - 20, 720, z=0.3),
            pie("lucas_contento", 545, S, 540, z=0.5, keys=[{"t": 0, "rot": -2}, {"t": d, "rot": 2}]),
            *cola(-280, S, n=4, alto=470, z=0.45),
            pie("cliente_feliz_1", 1250, S, 600, z=0.5), pie("cliente_feliz_3", 1480, S, 620, z=0.5),
            *aspa(540, 1080, 420, o(495)),
            brillo(540, 1100, 500, "#ffffff", 0.2, 0.1)],
            cam(1.0, 1.08, (540, 1150), (540, 1120)), "corte",
            sfx=[(o(495) + 0.1, "golpe", -16)])

    @plano(500, "piensa en cómo aprendiste casi todo")
    def _(d):
        cosas = [("balon_futbol", 220, 640, 180), ("guitarra", 880, 700, 130), ("libro_recetas", 210, 1250, 260),
                 ("olla", 870, 1250, 220), ("nota_musical_a", 360, 470, 110), ("mochila_cole", 720, 470, 150),
                 ("cuaderno_dibujo", -330, 820, 300), ("nota_musical_b", 1400, 760, 150), ("balon_playa", -380, 1200, 200),
                 ("hoja_dibujo", 1450, 1180, 260)]
        els = [fondo("bg_habitacion"), brillo(540, 900, 520, "#ffe7a0", 0.45, 0.2, pulso=[0.1, 1.0]),
               pieza("bombilla_b", 540, 900, 300, z=0.6, keys=arranque(540, 900, d, "abajo", 200, 20))]
        for k, (n, x, y, an) in enumerate(cosas):
            t0 = 0.25 + 0.14 * k
            els.append(pieza(n, x, y, an, z=0.5, keys=[{"t": 0, "x": 540, "y": 900, "escala": 0, "op": 0}, {"t": t0, "x": 540, "y": 900, "escala": 0, "op": 0},
                                                         {"t": t0 + 0.05, "op": 1}, {"t": t0 + 0.4, "x": x, "y": y, "escala": 1, "ease": "salida"},
                                                         {"t": d, "y": y - 30, "rot": 8 if k % 2 else -8}]))
        return P(["#38405a", "#6a5040"], els, cam(1.0, 1.1, (540, 900)), "desenfoque",
                 sfx=[(0.05, "brillo", -22)] + [(0.25 + 0.14 * k, "pop", -27) for k in range(0, 10, 2)])

    @plano(506, "a hablar")
    def _(d):
        return P(["#38405a", "#6a5040"], [
            fondo("bg_habitacion"),
            *flip(["bebe_habla", "bebe_habla_b"], d, fps=7, base=lambda n: pie(n, 540, 1440, 560, z=0.5, keys=late(0.05, 1, 0.05))),
            onda(560, 870, 0.1, 120, AMBAR), onda(560, 870, 0.45, 150, AMBAR),
            pie("balon_playa", -280, 1440, 200, z=0.5), pie("libro_c", 1300, 1440, 70, z=0.5), pie("libro_a", 1300, 1395, 70, z=0.51)],
            cam(1.2, 1.3, (540, 1100)), "corte", sfx=[(0.1, "burbuja", -22), (0.45, "burbuja", -24)])

    @plano(508, "copiando a tus padres")
    def _(d):
        return P(["#38405a", "#6a5040"], [
            fondo("bg_habitacion"),
            pie("padres_hablan", 330, 1440, 660, z=0.5, keys=[{"t": 0, "x": 300}, {"t": d, "x": 340}]),
            *flip(["bebe_habla", "bebe_habla_b"], d, fps=5, t0=0.6, base=lambda n: pie(n, 820, 1440, 340, z=0.55)),
            onda(300, 870, 0.05, 140, AMBAR), onda(300, 870, 0.35, 140, AMBAR),
            flecha([[430, 900], [600, 860], [740, 1130]], 0.15, 0.7, AMBAR, 8, [22, 16], z=0.6),
            onda(830, 1180, 0.85, 110, CIAN),
            pie("balon_playa", -330, 1440, 190, z=0.5), pie("mochila_cole", 1380, 1440, 220, z=0.5)],
            cam(1.05, 1.0, (560, 1100)), "corte", sfx=[(0.05, "burbuja", -24), (0.85, "burbuja", -22)])

    @plano(512, "a jugar al fútbol")
    def _(d):
        return P(["#4a3a6a", "#2f7a3a"], [
            fondo("bg_campo_barrio"),
            sale_suelo("balon_futbol", 600, 1440, 240, 0.0, z=0.6, desde=500, dur=0.6),
            pie("nino_regate_a", 270, 1440, 560, z=0.5, keys=[{"t": 0, "x": 240}, {"t": d, "x": 300}]),
            pie("cliente_feliz_2", -350, 1440, 600, z=0.4), pie("cliente_feliz_1", 1420, 1440, 600, z=0.4),
            brillo(600, 1300, 200, "#ffffff", 0.3, 0.2)],
            cam(1.0, 1.06, (520, 1150)), "corte", sfx=[(0.35, "golpe", -16)])

    @plano(516, "copiando el regate")
    def _(d):
        xs = [300, 720, 360, 760]
        ks = [{"t": round(i * d / 3, 3), "x": x, "rot": i * 90, "ease": "suave"} for i, x in enumerate(xs)]
        return P(["#4a3a6a", "#2f7a3a"], [
            fondo("bg_campo_barrio"),
            *flip(["nino_regate_a", "nino_regate_b"], d, fps=6, base=lambda n: pie(n, 540, 1440, 760, z=0.5,
                  keys=[{"t": 0, "x": 470}, {"t": d, "x": 600}])),
            {**pie("balon_futbol", 300, 1440, 200, z=0.6), "keys": ks},
            flecha([[300, 1340], [720, 1300], [360, 1260], [760, 1220]], 0.0, d * 0.95, CIAN, 8, [22, 16], z=0.55),
            pie("cliente_feliz_2", -380, 1440, 640, z=0.4), pie("cliente_feliz_3", 1450, 1440, 640, z=0.4)],
            cam(1.25, 1.35, (540, 1250)), "corte", sfx=[(0.1, "roce", -22), (d * 0.6, "roce", -22)])

    @plano(519, "de tu jugador favorito")
    def _(d):
        return P(["#4a3a6a", "#2f7a3a"], [
            fondo("bg_campo_barrio"),
            *camina(["nino_regate_a", "nino_regate_b"], 80, 760, 1440, 560, d, fps=5, z=0.55),
            {**pie("balon_futbol", 230, 1440, 150, z=0.6), "keys": [{"t": 0, "x": 230, "rot": 0}, {"t": d, "x": 910, "rot": 540, "ease": "lineal"}]},
            {**pie("nino_regate_b", 820, 1400, 430, z=0.4), "ex": -1, "keys": [{"t": 0, "rot": 0}, {"t": d * 0.5, "rot": 0}, {"t": d * 0.7, "rot": -12, "ease": "salida"}]},
            pie("cliente_feliz_2", -380, 1440, 600, z=0.4), pie("cliente_feliz_1", 1450, 1440, 600, z=0.4),
            pie("cliente_feliz_3", -560, 1440, 620, z=0.39, keys=late(d * 0.6, 2, 0.06))],
            cam(1.0, 1.05, (440, 1150), (640, 1150)), "corte", sfx=[(d * 0.55, "roce", -20)])

    def notas(x0, y0, x1, y1, d, n=4, t=0.0, sep=0.35, z=0.6, an=110):
        out = []
        for k in range(n):
            t0 = t + sep * k
            nm = "nota_musical_a" if k % 2 == 0 else "nota_musical_b"
            out.append(pieza(nm, x0, y0, an, z=z, keys=[{"t": 0, "op": 0, "x": x0, "y": y0, "escala": 0.4}, {"t": t0, "op": 0, "x": x0, "y": y0, "escala": 0.4},
                                                       {"t": t0 + 0.08, "op": 1}, {"t": t0 + 1.1, "x": x1 + (k % 2) * 60, "y": y1 - k * 30, "escala": 1.0, "rot": 15 - 30 * (k % 2), "ease": "suave"},
                                                       {"t": t0 + 1.5, "op": 0}]))
        return out

    @plano(523, "cualquier guitarrista")
    def _(d):
        return P(["#38405a", "#6a5040"], [
            fondo("bg_habitacion"),
            *flip(["guitarrista", "guitarrista_b"], d, fps=6, base=lambda n: pie(n, 540, 1440, 700, z=0.5)),
            *notas(620, 1050, 760, 600, d, n=3, sep=0.25),
            brillo(560, 1100, 320, "#ffd59a", 0.35, 0.3, pulso=[0.1, 0.5]),
            pie("guitarra", -330, 1440, 520, z=0.45, rot=-6), pieza("nota_musical_b", 1400, 800, 160, z=0.4, anim={"flotar": [20, 2]})],
            cam(1.2, 1.12, (540, 1050)), "corte", sfx=[(0.05, "ding", -26)])

    @plano(525, "empieza tocando canciones de otros")
    def _(d):
        return P(["#38405a", "#6a5040"], [
            fondo("bg_habitacion"),
            *flip(["guitarrista", "guitarrista_b"], d, fps=5, base=lambda n: pie(n, 720, 1440, 640, z=0.5)),
            pieza("telefono_movil", 220, 1050, 170, z=0.55, rot=-8, keys=late(0.1, 2, 0.08)),
            brillo(220, 1050, 180, "#9fd0ff", 0.5, 0.5, pulso=[0.15, 0.6]),
            *notas(230, 960, 640, 820, d, n=5, sep=0.3, an=90),
            flecha([[300, 1000], [460, 880], [600, 900]], 0.2, 0.9, AMBAR, 7, [20, 14], z=0.58),
            pie("guitarra", -350, 1440, 520, z=0.45, rot=-6), pie("mochila_cole", 1400, 1440, 230, z=0.45)],
            cam(1.0, 1.08, (480, 1080), (560, 1080)), "corte", sfx=[(0.3, "ding", -25), (1.2, "ding", -27)])

    @plano(530, "cualquier cocinero empieza con la receta de alguien")
    def _(d):
        o = rel(530)
        return P(["#f2e6c8", "#c08a60"], [
            fondo("bg_cocina"),
            pie("cocinero_receta", 560, 1440, 880, z=0.5, keys=[{"t": 0, "x": 600}, {"t": d, "x": 540}]),
            pieza("libro_recetas", 250, 1180, 320, z=0.65, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": o(535) - 0.2, "op": 0, "escala": 0},
                                                                {"t": o(535) - 0.15, "op": 1}, {"t": o(535) + 0.25, "escala": 1, "ease": "elastico"},
                                                                {"t": d, "rot": -6}]),
            senala(250, 1180, o(535) + 0.1, d - 0.1, 190, AMBAR),
            {**polvo("#ffffff", 16, (520, 860, 760, 1060), 5), "vel": [4, -40]},
            pie("olla", -330, 1440, 220, z=0.5), pie("libro_recetas", 1400, 1440, 180, z=0.5)],
            cam(1.0, 1.1, (540, 1100)), "corte", sfx=[(o(535), "pop", -22)])

    @plano(538, "y un día le añade su toque")
    def _(d):
        o = rel(538)
        t1 = o(542) + 0.1
        return P(["#141018", "#050507"], [
            *estudio(),
            pie("olla", 540, 1400, 380, z=0.5, keys=late(t1 + 0.35, 1, 0.07)),
            {**polvo("#ffffff", 18, (440, 860, 640, 1060), 6), "vel": [4, -50]},
            pieza("icono_bonito", 540, 500, 160, z=0.6, keys=[{"t": 0, "y": 420, "rot": 0, "op": 1}, {"t": t1, "y": 420, "rot": 0},
                                                             {"t": t1 + 0.35, "y": 1060, "rot": 180, "escala": 0.5, "ease": "entrada"}, {"t": t1 + 0.37, "op": 0}]),
            pieza("destello", 540, 1060, 420, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": t1 + 0.35, "op": 0, "escala": 0},
                                                           {"t": t1 + 0.4, "op": 1}, {"t": t1 + 0.8, "escala": 1.2, "rot": 45, "ease": "salida"}, {"t": d, "op": 0.6}]),
            brillo(540, 1060, 400, "#ffe07a", 0.8, 0.65, keys=[{"t": 0, "op": 0}, {"t": t1 + 0.35, "op": 0}, {"t": t1 + 0.5, "op": 0.8}]),
            *fantasmas(["libro_recetas", "nota_musical_a", "balon_futbol", "guitarra"])],
            cam(1.0, 1.1, (540, 1050)), "corte", sfx=[(t1 + 0.35, "brillo", -16)])

    def paso(icono, texto, d, color, keys, ghost, sfx_t="golpe", frio=False, sem=1):
        return P(["#141018", "#050507"], [
            *estudio(color, frio, sem),
            pieza(icono, 540, 900, 540, z=0.6, keys=keys),
            *fantasmas(ghost)],
            cam(1.0, 1.08, (540, 1000)), "corte",
            hud=[rotulo(0.15, d - 0.05, texto, tam=120, color="#ffffff", capsula="#c0392be6", y=1330)],
            sfx=[(0.05, sfx_t, -15)])

    @plano(545, "primero copias")
    def _(d):
        return paso("icono_igual", "COPIAS", d, "#8ab8ff", arranque(540, 960, d, "izquierda", 300, 30),
                    ["icono_mas", "icono_bonito", "icono_mas", "icono_bonito"], frio=True, sem=2)

    @plano(547, "luego mejoras")
    def _(d):
        return paso("icono_mas", "MEJORAS", d, "#8aff9a", [{"t": 0, "rot": -90, "escala": 0.3}, {"t": 0.4, "rot": 0, "escala": 1.0, "ease": "elastico"},
                                                           {"t": d, "escala": 1.08}], ["icono_igual", "icono_bonito", "icono_igual", "icono_bonito"], sem=3)

    @plano(549, "y al final te sale algo que es tuyo")
    def _(d):
        o = rel(549)
        tb = 0.55
        return P(["#141018", "#050507"], [
            *estudio("#ffe07a", sem=4),
            pieza("icono_igual", 260, 900, 320, z=0.55, keys=aparece(0.0, 0.3) + [{"t": tb, "x": 260, "y": 900, "op": 1}, {"t": tb + 0.4, "x": 480, "y": 980, "escala": 0.2, "op": 0, "ease": "entrada"}]),
            pieza("icono_mas", 820, 900, 320, z=0.55, keys=aparece(0.1, 0.3) + [{"t": tb, "x": 820, "y": 900, "op": 1}, {"t": tb + 0.4, "x": 600, "y": 980, "escala": 0.2, "op": 0, "ease": "entrada"}]),
            pieza("icono_bonito", 540, 980, 540, z=0.6, keys=[{"t": 0, "escala": 0, "op": 0}, {"t": tb + 0.35, "escala": 0, "op": 0}, {"t": tb + 0.4, "op": 1},
                                                              {"t": tb + 0.8, "escala": 1.0, "ease": "elastico"}, {"t": d, "escala": 1.08, "rot": 8}]),
            pieza("destello", 540, 1000, 700, z=0.5, keys=[{"t": 0, "op": 0}, {"t": tb + 0.4, "op": 0}, {"t": tb + 0.5, "op": 0.8}, {"t": d, "rot": 30, "op": 0.4}]),
            *fantasmas(["icono_igual", "icono_mas", "icono_mas", "icono_igual"])],
            cam(1.0, 1.06, (540, 960)), "corte",
            hud=[rotulo(max(tb + 0.5, d - 0.95), d - 0.05, "ES TUYO", tam=130, color="#2a1a00", capsula="#ffcf6af0", y=1380)],
            sfx=[(tb + 0.4, "brillo", -16)])

    # ============================================================ LA TRAMPA (558–614)
    @plano(558, "aquí viene la trampa")
    def _(d):
        o = rel(558)
        tt = o(562)
        return P(["#1a0606", "#050507"], [
            *estudio("#ff4a3d", frio=True, sem=5),
            brillo(540, 1000, 600, "#ff2a1a", 0.8, 0.15, keys=[{"t": 0, "op": 0.1}, {"t": tt, "op": 0.1}, {"t": tt + 0.1, "op": 0.7}]),
            sale_suelo("icono_igual", 540, 1400, 360, 0.0, z=0.6, desde=300, dur=max(0.3, tt)),
            fundido_blanco([{"t": 0, "op": 0}, {"t": tt - 0.02, "op": 0}, {"t": tt, "op": 0.8}, {"t": tt + 0.25, "op": 0}], color="#ffdddd"),
            *fantasmas(["hamburgueseria", "hamburgueseria", "icono_igual", "icono_igual"], op=0.15, ancho=300)],
            cam(1.0, 1.12, (540, 1050), temblor=6), "corte",
            hud=[rotulo(0.3, d - 0.05, "LA TRAMPA", tam=140, color="#ffffff", capsula="#c0392bf0", y=600)],
            sfx=[(0.0, "subida", -18, {"dur": max(0.4, tt)}), (tt, "impacto", -10)])

    @plano(563, "que te prometí")
    def _(d):
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pieza("cara_lucas_listo", 540, 1040, 920, z=0.6, keys=[{"t": 0, "escala": 0.96, "rot": -2}, {"t": d, "escala": 1.04, "rot": 2}]),
            pieza("destello", 790, 640, 160, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.35, "op": 0, "escala": 0}, {"t": 0.4, "op": 1}, {"t": 0.7, "escala": 1, "rot": 45, "ease": "salida"}, {"t": d, "op": 0}]),
            pie("cliente_feliz_1", -350, 1440, 600, z=0.3), pie("cliente_feliz_2", 1450, 1440, 600, z=0.3)],
            cam(1.0, 1.06, (540, 1000)), "corte", sfx=[(0.4, "brillo", -24)])

    @plano(566, "copiar tal cual")
    def _(d):
        S = 1440
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pie("hamburgueseria", 160, S - 20, 680, z=0.4),
            {**pie("hamburgueseria", 160, S - 20, 680, z=0.39), "keys": [{"t": 0, "x": 160, "op": 0.0}, {"t": 0.2, "x": 160, "op": 0.6}, {"t": 0.7, "x": 920, "op": 1.0, "ease": "anticipa"}]},
            pieza("icono_igual", 540, 900, 180, z=0.6, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.7, "op": 0, "escala": 0}, {"t": 0.72, "op": 1}, {"t": 1.0, "escala": 1, "ease": "elastico"}]),
            pie("cliente_confuso_1", -350, S, 620, z=0.5), pie("cliente_confuso_2", 1420, S, 620, z=0.5)],
            cam(1.05, 1.0, (540, 1150)), "corte", sfx=[(0.2, "roce", -20), (0.72, "pop", -22)])

    @plano(569, "no sirve")
    def _(d):
        return P(["#141018", "#050507"], [
            *estudio("#ff8a7a", frio=True, sem=6),
            pieza("icono_igual", 540, 940, 540, z=0.6, keys=[{"t": 0, "escala": 1.1}, {"t": d, "escala": 0.95, "rot": -6}]),
            *aspa(540, 940, 320, 0.1, g=34),
            *fantasmas(["hamburgueseria", "hamburgueseria", "hamburgueseria", "hamburgueseria"], op=0.15, ancho=300)],
            cam(1.08, 1.0, (540, 980), temblor=4), "corte", sfx=[(0.15, "golpe", -13)])

    @plano(571, "si Lucas hubiera abierto la misma hamburguesería")
    def _(d):
        o = rel(571)
        S = 1390
        tc = o(576) - 0.1
        return P(["#1a1a3a", "#2a2030"], [
            fondo("bg_ciudad"),
            pie("hamburgueseria_lucas", 120, S, 680, z=0.4),
            {**pie("hamburgueseria_lucas", 960, S, 680, z=0.4), "keys": [{"t": 0, "op": 0, "escala": 0.9}, {"t": tc, "op": 0, "escala": 0.9}, {"t": tc + 0.3, "op": 1, "escala": 1.0, "ease": "salida"}]},
            flecha([[640, 880], [820, 880]], tc, tc + 0.4, AMBAR, 9, [20, 14], z=0.6),
            pie("lucas_senala", 520, S, 520, z=0.55, keys=[{"t": 0, "x": 480}, {"t": d, "x": 540}]),
            *cola(-200, S, n=5, alto=440, z=0.45),
            pie("cliente_feliz_3", 1500, S, 520, z=0.45), pie("cliente_feliz_1", 1660, S, 520, z=0.45)],
            cam(1.0, 1.06, (540, 1100)), "corte", vineta=0.65, sfx=[(tc, "pop", -22)])

    @plano(578, "con la misma cola y los mismos precios")
    def _(d):
        o = rel(578)
        S = 1390
        tp = o(584) - 0.15
        return P(["#1a1a3a", "#2a2030"], [
            fondo("bg_ciudad"),
            pie("hamburgueseria_lucas", 120, S, 680, z=0.35), pie("hamburgueseria_lucas", 960, S, 680, z=0.35),
            *cola(200, S, n=8, alto=440, z=0.45), *cola(1040, S, n=4, alto=440, z=0.44),
            pieza("icono_igual", 540, 820, 180, z=0.6, keys=aparece(0.15, 0.35)),
            pieza("billete", 120, 560, 240, z=0.6, keys=aparece(tp, 0.35)), pieza("billete", 960, 560, 240, z=0.6, keys=aparece(tp + 0.1, 0.35))],
            cam(1.08, 1.0, (540, 1050)), "corte", vineta=0.65,
            hud=[rotulo(tp + 0.1, d - 0.05, "5 €", tam=100, color="#ffffff", capsula="#1e7a40e6", x=120, y=430),
                 rotulo(tp + 0.2, d - 0.05, "5 €", tam=100, color="#ffffff", capsula="#1e7a40e6", x=960, y=430)],
            sfx=[(0.15, "pop", -24), (tp, "ding", -24)])

    @plano(586, "solo se habrían repartido los clientes")
    def _(d):
        o = rel(586)
        S = 1390
        ts = max(0.3, o(589) - 0.2)
        els = [fondo("bg_ciudad"), pie("hamburgueseria_lucas", 120, S, 680, z=0.35), pie("hamburgueseria_lucas", 960, S, 680, z=0.35)]
        for i in range(10):
            x = 260 - i * 95
            nm = f"cola_{i % 6}"
            ks = []
            if i % 2:
                t0 = ts + 0.06 * i
                xd = 1100 - (i // 2) * 95
                ks = [{"t": 0, "x": x}, {"t": t0, "x": x}, {"t": t0 + 0.7, "x": xd, "ease": "suave"}]
            els.append(pie(nm, x, S, 450 * (1 - 0.015 * i), z=0.45 - 0.002 * i - (0.02 if i % 2 else 0), keys=ks))
        return P(["#1a1a3a", "#2a2030"], els, cam(1.0, 1.0, (540, 1080)), "corte", vineta=0.65,
                 hud=[contador(ts, d - 0.05, 100, 50, 0.9, " clientes", tam=96, x=120, y=480, color="#ffffff", capsula="#0b0f1ed8"),
                      contador(ts, d - 0.05, 0, 50, 0.9, " clientes", tam=96, x=960, y=480, color="#ffffff", capsula="#0b0f1ed8")],
                 sfx=[(ts, "roce", -18), (ts + 0.9, "golpe", -20)])

    @plano(592, "el truco no es copiar")
    def _(d):
        return P(["#141018", "#050507"], [
            *estudio("#ffe07a", sem=7),
            *flip(["bombilla_a", "bombilla_b"], d, fps=1 / 0.45, base=lambda n: pieza(n, 540, 900, 340, z=0.6, keys=arranque(540, 900, d, "arriba", 220, 20))),
            brillo(540, 880, 380, "#ffe07a", 0.8, 0.55, keys=[{"t": 0, "op": 0}, {"t": 0.45, "op": 0}, {"t": 0.5, "op": 0.7}]),
            *fantasmas(["icono_igual", "icono_mas", "icono_rapido", "icono_cerca"])],
            cam(1.0, 1.08, (540, 960)), "corte",
            hud=[rotulo(0.5, d - 0.05, "EL TRUCO", tam=120, color="#2a1a00", capsula="#ffcf6af0", y=1330)],
            sfx=[(0.45, "zap", -20), (0.5, "brillo", -20)])

    @plano(597, "es copiar")
    def _(d):
        return P(["#141018", "#050507"], [
            *estudio("#8ab8ff", frio=True, sem=8),
            pieza("icono_igual", 300, 940, 440, z=0.6, keys=arranque(300, 940, d, "izquierda", 260, 20)),
            *fantasmas(["icono_igual", "icono_igual", "icono_mas", "icono_mas"])],
            cam(1.0, 1.05, (540, 960)), "corte", sfx=[(0.05, "pop", -18)])

    @plano(599, "y mejorar una sola cosa")
    def _(d):
        o = rel(599)
        t1 = o(601) - 0.05
        return P(["#141018", "#050507"], [
            *estudio("#8aff9a", sem=9),
            pieza("icono_igual", 300, 940, 440, z=0.6, keys=[{"t": 0, "escala": 1}, {"t": t1, "x": 300}, {"t": t1 + 0.3, "x": 60, "escala": 0.6, "op": 0.5}]),
            pieza("icono_mas", 780, 940, 440, z=0.6, keys=aparece(0.05, 0.35) + [{"t": t1, "x": 780}, {"t": t1 + 0.3, "x": 1020, "escala": 0.6, "op": 0.5}]),
            brillo(540, 960, 450, "#ffcf6a", 0.8, 0.5, keys=[{"t": 0, "op": 0}, {"t": t1, "op": 0}, {"t": t1 + 0.15, "op": 0.8}]),
            *fantasmas(["icono_igual", "icono_mas", "icono_mas", "icono_igual"])],
            cam(1.0, 1.08, (540, 960)), "corte",
            hud=[rotulo(t1, d - 0.05, "1", tam=420, color="#ffcf6a", capsula=None, y=960)],
            sfx=[(0.05, "pop", -20), (t1, "impacto", -12)])

    def mas(icono, texto, d, color, keys, sonido, ghost, sem):
        return P(["#141018", "#050507"], [
            *estudio(color, sem=sem),
            pieza(icono, 540, 900, 540, z=0.6, keys=keys),
            *fantasmas(ghost, op=0.18)],
            cam(1.0, 1.1, (540, 960)), "corte",
            hud=[rotulo(0.1, d - 0.05, texto, tam=110, color="#ffffff", capsula="#c0392be6", y=1340, sin_pop=True)],
            sfx=[(0.03, "golpe", -13), (0.1, sonido, -20)])

    @plano(604, "más rápido")
    def _(d):
        return mas("icono_rapido", "MÁS RÁPIDO", d, "#ffd23f", lanza(0.0, 0.35, (-300, 940), (540, 940)) + [{"t": d, "x": 580, "rot": 6}],
                   "zap", ["icono_barato", "icono_cerca", "icono_bonito", "icono_barato"], 10)

    @plano(606, "más barato")
    def _(d):
        return mas("icono_barato", "MÁS BARATO", d, "#ff8a7a", [{"t": 0, "y": 300}] + cae(0.0, 0.45, 300, 940)[1:] + [{"t": d, "rot": -8}],
                   "tic", ["icono_rapido", "icono_cerca", "monedas", "billete"], 11)

    @plano(608, "más cerca")
    def _(d):
        return mas("icono_cerca", "MÁS CERCA", d, "#7aa8ff", [{"t": 0, "escala": 2.4, "op": 0}, {"t": 0.3, "escala": 1.0, "op": 1, "ease": "golpe"}, {"t": d, "escala": 1.06}],
                   "burbuja", ["icono_rapido", "icono_barato", "icono_bonito", "icono_rapido"], 12)

    @plano(610, "más bonito")
    def _(d):
        return mas("icono_bonito", "MÁS BONITO", d, "#ffe07a", [{"t": 0, "rot": -180, "escala": 0.2}, {"t": 0.4, "rot": 0, "escala": 1.0, "ease": "elastico"}, {"t": d, "rot": 10}],
                   "brillo", ["icono_rapido", "icono_barato", "icono_cerca", "destello"], 13)

    @plano(612, "una sola cosa")
    def _(d):
        ics = ["icono_rapido", "icono_barato", "icono_cerca", "icono_bonito"]
        els = [*estudio("#ffcf6a", sem=14)]
        for k, n in enumerate(ics):
            x = 60 + 320 * k
            if n == "icono_rapido":
                ks = aparece(0.0, 0.25) + [{"t": 0.45, "x": x, "y": 920}, {"t": 0.85, "x": 540, "y": 900, "escala": 2.0, "ease": "elastico"}, {"t": d, "escala": 2.1}]
            else:
                ks = aparece(0.0, 0.25) + [{"t": 0.3 + 0.05 * k, "y": 920, "rot": 0, "op": 1},
                                             {"t": 0.75 + 0.05 * k, "y": 1700, "rot": 40 - 30 * k, "op": 0, "ease": "entrada"}]
            els.append(pieza(n, x, 920, 280, z=0.6 - 0.01 * k, keys=ks))
        els += fantasmas(["icono_igual", "icono_mas", "icono_mas", "icono_igual"], op=0.12)
        return P(["#141018", "#050507"], els, cam(1.0, 1.05, (540, 960)), "corte",
                 hud=[rotulo(0.5, d - 0.05, "UNA SOLA COSA", tam=100, color="#2a1a00", capsula="#ffcf6af0", y=1370)],
                 sfx=[(0.3, "roce", -18), (0.85, "golpe", -16)])

    # ============================================================ EL REGRESO (615–688)
    @plano(615, "un día Marta pasa por delante")
    def _(d):
        S = 1440
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pie("hamburgueseria_lucas", 1080, S - 30, 760, z=0.3),
            *cola(1000, S - 30, n=7, alto=440, z=0.4),
            *camina(["marta_camina_a", "marta_camina_b"], -260, 420, S, 560, d, fps=4, z=0.6),
            *camina(["cliente_se_va_a", "cliente_se_va_b"], -400, -650, S, 540, d, fps=4, z=0.55, mira=-1)],
            cam(1.0, 1.05, (380, 1150), (560, 1150)), "corte", sfx=[(0.1, "roce", -24)])

    @plano(621, "del local de Lucas")
    def _(d):
        S = 1440
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pie("hamburgueseria_lucas", 560, S, 980, z=0.35),
            pie("lucas_contento", 980, S, 600, z=0.55, keys=late(0.2, 1, 0.05)),
            *cola(380, S, n=10, alto=520, z=0.5),
            brillo(560, 830, 200, "#ffcf6a", 0.5, 0.4, pulso=[0.15, 0.7])],
            cam(1.0, 1.12, (560, 1050)), "corte", sfx=[(0.2, "ding", -24)])

    @plano(625, "ve la cola")
    def _(d):
        S = 1440
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pie("hamburgueseria_lucas", 1500, S - 20, 760, z=0.3),
            *cola(1300, S - 20, n=11, alto=460, z=0.4),
            pie("marta_camina_a", 100, S, 680, z=0.6, keys=[{"t": 0, "rot": 0}, {"t": d, "rot": -3}]),
            flecha([[220, 820], [980, 820]], 0.1, d * 0.85, AMBAR, 8, [22, 16], z=0.7)],
            cam(1.15, 1.2, (300, 1100), (760, 1100)), "corte")

    @plano(628, "entra")
    def _(d):
        S = 1440
        yd = ypie("marta_camina_a", S, 600)
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pie("hamburgueseria_lucas", 540, S, 1000, z=0.35),
            brillo(850, 1200, 260, "#ffe2a0", 0.6, 0.4),
            *camina(["marta_camina_a", "marta_camina_b"], 560, 830, S, 600, d, fps=6, z=0.6,
                    op=[{"t": 0, "op": 1, "escala": 1.0, "y": yd}, {"t": d * 0.6, "op": 1}, {"t": d, "op": 0.0, "escala": 0.85, "y": yd - 40}]),
            *cola(200, S, n=9, alto=520, z=0.5)],
            cam(1.0, 1.05, (620, 1100)), "corte", sfx=[(0.3, "roce", -20)])

    @plano(629, "pide")
    def _(d):
        S = 1440
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pie("hamburgueseria_lucas", 540, S - 20, 900, z=0.3),
            pie("lucas_entrega", 380, S, 650, z=0.55, keys=[{"t": 0, "x": 340}, {"t": 0.3, "x": 390, "ease": "salida"}]),
            {**pie("marta_camina_a", 780, S, 650, z=0.56), "ex": -1},
            pieza("hamburguesa", 600, 820, 140, z=0.7, keys=aparece(0.1, 0.3)),
            pie("cliente_feliz_1", -350, S, 620, z=0.5), pie("cliente_feliz_3", 1430, S, 620, z=0.5)],
            cam(1.15, 1.2, (580, 1060)), "corte", sfx=[(0.1, "pop", -22)])

    @plano(630, "y lo entiende")
    def _(d):
        o = rel(630)
        te = max(0.1, o(632) - 0.05)
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pieza("cara_marta_sorpresa", 540, 1020, 920, z=0.6, keys=[{"t": 0, "escala": 0.95}, {"t": d, "escala": 1.06}]),
            pieza("bombilla_b", 880, 620, 190, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": te, "op": 0, "escala": 0}, {"t": te + 0.05, "op": 1},
                                                             {"t": te + 0.4, "escala": 1, "ease": "elastico"}, {"t": d, "rot": 10}]),
            brillo(880, 620, 260, "#ffe07a", 0.8, 0.65, keys=[{"t": 0, "op": 0}, {"t": te, "op": 0}, {"t": te + 0.2, "op": 0.8}]),
            pie("cliente_feliz_2", -380, 1440, 620, z=0.4), pie("cliente_feliz_1", 1460, 1440, 620, z=0.4)],
            cam(1.0, 1.08, (540, 950)), "corte", sfx=[(te, "ding", -16)])

    @plano(633, "su problema nunca fue la creatividad")
    def _(d):
        flo = [("hoja_dibujo", 200, 700, 220), ("cuaderno_dibujo", 880, 760, 240), ("bombilla_b", 230, 1080, 130),
               ("nota_musical_a", 870, 1100, 90), ("hoja_dibujo", -330, 860, 260), ("reloj_arena_grande", 1420, 950, 160)]
        return P(["#2a2622", "#141210"], [
            fondo("bg_cafe_dentro_triste"),
            pie("marta_entiende", 540, 1430, 760, z=0.55, keys=[{"t": 0, "x": 520}, {"t": d, "x": 560}]),
            *[pieza(n, x, y, an, z=0.6, keys=aparece(0.1 + 0.12 * k, 0.4) + [{"t": d, "y": y - 50, "rot": 10 - 20 * (k % 2)}])
              for k, (n, x, y, an) in enumerate(flo)],
            brillo(540, 900, 520, "#ffcf8a", 0.3, 0.2, pulso=[0.1, 1.2])],
            cam(1.0, 1.08, (540, 1050)), "corte", sfx=[(0.1, "brillo", -24)])

    @plano(639, "fue usarla en el sitio equivocado")
    def _(d):
        o = rel(639)
        S = 1440
        ts = max(0.3, o(643) - 0.1)
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pie("cafeteria_marta_cerrada", 540, S - 20, 820, z=0.4),
            pieza("bombilla_b", 540, 560, 150, z=0.6, keys=[{"t": 0, "y": 540}, {"t": d * 0.5, "y": 575, "ease": "suave"}, {"t": d, "y": 540, "ease": "suave"}]),
            brillo(540, 580, 200, "#ffe07a", 0.6, 0.55, pulso=[0.12, 0.6]),
            senala(540, 730, ts, d - 0.05, 120, ROJO),
            pie("cliente_se_va_a", -360, S, 620, z=0.5), pie("cliente_confuso_2", 1420, S, 620, z=0.5)],
            cam(1.0, 1.1, (540, 1000), (540, 940)), "corte",
            hud=[rotulo(ts, d - 0.05, "SITIO EQUIVOCADO", tam=84, color="#ffffff", capsula="#c0392be6", y=1300)],
            sfx=[(ts, "golpe", -18)])

    @plano(645, "así que vuelve a empezar")
    def _(d):
        S = 1440
        k1 = [{"t": 0, "x": 160, "y": 700}, {"t": d, "x": 700, "y": 690, "ease": "lineal"}]
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pie("cafeteria_marta_cerrada", 60, S - 30, 760, z=0.3),
            *camina(["marta_camina_a", "marta_camina_b"], 60, 600, S, 600, d, fps=4, z=0.6),
            pieza("bombilla_b", 160, 700, 120, z=0.65, keys=sigue(k1, 0.15)),
            brillo(160, 700, 160, "#ffe07a", 0.5, 0.6, keys=sigue(k1, 0.15)),
            pie("cliente_feliz_3", 1420, S, 620, z=0.5)],
            cam(1.0, 1.04, (300, 1100), (560, 1100)), "corte", sfx=[(0.1, "roce", -24)])

    @plano(650, "pero al revés")
    def _(d):
        return P(["#141018", "#050507"], [
            *estudio("#ffe07a", sem=15),
            pieza("bombilla_b", 540, 940, 360, z=0.6, keys=[{"t": 0, "rot": 0, "escala": 0.95}, {"t": 0.15, "rot": 0}, {"t": 0.6, "rot": 180, "escala": 1.05, "ease": "elastico"}, {"t": d, "rot": 186}]),
            flecha([[820, 700], [900, 960], [800, 1200]], 0.1, 0.55, CIAN, 9, z=0.65),
            flecha([[260, 1200], [180, 940], [280, 700]], 0.1, 0.55, CIAN, 9, z=0.65),
            *fantasmas(["taza_cafe_latte", "cafeteria_nueva", "taza_cafe_latte", "cafeteria_nueva"])],
            cam(1.0, 1.06, (540, 960)), "corte", sfx=[(0.15, "zap", -18)])

    @plano(653, "abre una cafetería normal")
    def _(d):
        S = 1440
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            sale_suelo("cafeteria_nueva", 640, S - 20, 820, 0.0, z=0.35, desde=100, dur=0.55),
            pieza("cartel_abierto", 1150, 1000, 170, z=0.5, keys=[{"t": 0, "op": 0}, {"t": 0.5, "op": 0, "rot": 0}, {"t": 0.55, "op": 1, "rot": 20},
                                                              {"t": 0.9, "rot": -12, "ease": "suave"}, {"t": 1.3, "rot": 6, "ease": "suave"}, {"t": d, "rot": 0, "ease": "suave"}]),
            pie("marta_sonrie", 120, S, 600, z=0.6, keys=late(0.6, 1, 0.04)),
            pie("cliente_feliz_1", -380, S, 620, z=0.5), pie("cliente_feliz_2", 1420, S, 620, z=0.5)],
            cam(1.0, 1.05, (540, 1100)), "corte", sfx=[(0.35, "golpe", -15), (0.6, "ding", -24)])

    @plano(657, "de las que todo el mundo entiende")
    def _(d):
        S = 1440
        gente = [("cliente_feliz_1", -500), ("voluntario_1", -60), ("voluntario_3", 1140), ("cliente_feliz_3", 1560)]
        els = [fondo("bg_calle_dia"), pie("cafeteria_nueva", 540, S - 20, 760, z=0.35)]
        for k, (n, x) in enumerate(gente):
            t0 = 0.25 + 0.3 * k
            els.append(pie(n, x, S, 540, z=0.55, keys=late(t0, 1, 0.05)))
            els.append(check(x, 820, t0))
        els.append(pieza("taza_cafe_latte", 540, 480, 200, z=0.6, keys=aparece(0.05, 0.35) + [{"t": d, "rot": 6}]))
        return P(["#bfe3f7", "#c9c2b5"], els, cam(1.05, 1.0, (540, 1050)), "corte",
                 sfx=[(0.25 + 0.3 * k, "tic", -22) for k in range(4)])

    @plano(664, "y pone su toque")
    def _(d):
        return P(["#f2e6c8", "#a08060"], [
            fondo("bg_cafe_dentro"),
            pie("marta_delantal", 540, 1430, 800, z=0.55),
            pieza("destello", 660, 930, 220, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": 0.3, "op": 1, "escala": 1, "rot": 45, "ease": "salida"}, {"t": d, "op": 0.3, "rot": 90}]),
            pie("voluntario_4", -380, 1430, 620, z=0.5), pie("voluntario_1", 1440, 1430, 620, z=0.5)],
            cam(1.0, 1.2, (540, 1050), (620, 950)), "corte", sfx=[(0.3, "brillo", -22)])

    @plano(668, "en una sola cosa")
    def _(d):
        o = rel(668)
        tb = max(0.35, o(670))
        return P(["#141018", "#050507"], [
            *estudio("#ffcf8a", sem=16),
            pie("taza_cafe_latte", 540, 1400, 420, z=0.55),
            {**polvo("#ffffff", 14, (460, 860, 620, 1060), 17), "vel": [4, -40]},
            pieza("bombilla_b", 540, 500, 150, z=0.6, keys=[{"t": 0, "y": 430}, {"t": tb, "y": 1140, "escala": 0.4, "rot": 20, "ease": "entrada"}, {"t": tb + 0.02, "op": 0}]),
            pieza("destello", 540, 1140, 380, z=0.7, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": tb, "op": 0, "escala": 0}, {"t": tb + 0.05, "op": 1},
                                                           {"t": tb + 0.4, "escala": 1, "rot": 45, "ease": "salida"}, {"t": d, "op": 0.5}]),
            senala(540, 1160, tb + 0.1, d - 0.05, 150, AMBAR),
            *fantasmas(["cafeteria_nueva", "taza_cafe", "cafeteria_nueva", "taza_cafe"])],
            cam(1.0, 1.1, (540, 1150)), "corte", sfx=[(tb, "brillo", -16)])

    @plano(672, "la gente entra")
    def _(d):
        S = 1440
        dx = 880
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pie("cafeteria_nueva", 680, S - 20, 820, z=0.35),
            *camina(["cliente_se_va_a", "cliente_se_va_b"], 380, dx, S, 540, d, fps=5, z=0.55,
                    op=[{"t": 0, "op": 1}, {"t": d * 0.7, "op": 1}, {"t": d, "op": 0}]),
            *camina(["cliente_se_va_a", "cliente_se_va_b"], 60, 470, S, 550, d, fps=5, z=0.56),
            *cola(-160, S, n=4, alto=500, z=0.5),
            pie("voluntario_3", 1440, S, 620, z=0.5)],
            cam(1.0, 1.05, (560, 1100)), "corte", sfx=[(0.1, "roce", -24)])

    @plano(675, "sin que nadie le explique nada")
    def _(d):
        S = 1430
        return P(["#f2e6c8", "#a08060"], [
            fondo("bg_cafe_dentro"),
            pie("marta_delantal", 820, S, 700, z=0.45, keys=[{"t": 0, "x": 860}, {"t": d, "x": 800}]),
            pie("padres_hablan", 300, S, 700, z=0.55, keys=late(0.4, 1, 0.04)),
            pie("voluntario_1", -320, S, 640, z=0.5, keys=late(0.9, 1, 0.04)), pie("voluntario_4", 1380, S, 640, z=0.5, keys=late(1.2, 1, 0.04)),
            pieza("taza_cafe_latte", 300, 1040, 120, z=0.6, keys=aparece(0.2, 0.3)),
            pieza("taza_cafe_latte", 1380, 1040, 120, z=0.6, keys=aparece(0.5, 0.3)),
            check(300, 650, 0.6), check(-320, 650, 1.0), check(1380, 650, 1.3),
            brillo(540, 900, 520, "#ffe2a0", 0.3, 0.2)],
            cam(1.0, 1.06, (540, 1080), (580, 1080)), "corte", sfx=[(0.6, "tic", -22), (1.0, "tic", -24)])

    @plano(681, "esta vez")
    def _(d):
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pieza("cara_marta_feliz", 540, 1040, 900, z=0.6, keys=arranque(540, 1040, d, "derecha", 220, 20)),
            pie("cliente_feliz_1", -380, 1440, 620, z=0.4), pie("voluntario_3", 1460, 1440, 620, z=0.4)],
            cam(1.0, 1.05, (540, 1000)), "corte", sfx=[(0.05, "pop", -22)])

    @plano(683, "la cola está en su puerta")
    def _(d):
        S = 1440
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pie("cafeteria_nueva", 820, S - 20, 820, z=0.35),
            *cola(760, S, n=14, alto=470, z=0.5, avanza=(0.5, 40)),
            pie("marta_delantal", 1240, S, 560, z=0.45, keys=late(0.3, 1, 0.04)),
            brillo(1000, 1000, 300, "#ffe2a0", 0.4, 0.3, pulso=[0.1, 0.9])],
            cam(1.18, 1.0, (820, 1050), (540, 1100)), "corte", sfx=[(0.2, "ding", -20)])

    # ============================================================ CIERRE (689–748)
    @plano(689, "ojo")
    def _(d):
        return P(["#141018", "#050507"], [
            *estudio("#ff8a7a", sem=18),
            pieza("ojo", 540, 960, 760, z=0.6, keys=arranque(540, 960, d, "abajo", 160, 10) + [{"t": 0.45, "ey": 1.0}, {"t": 0.52, "ey": 0.1}, {"t": 0.6, "ey": 1.0}]),
            *fantasmas(["examen", "examen", "pupitre", "pupitre"])],
            cam(1.0, 1.08, (540, 960)), "corte", sfx=[(0.05, "golpe", -16)])

    @plano(690, "copiar en el examen sigue sin enseñarte nada")
    def _(d):
        o = rel(690)
        te = max(0.2, o(693) - 0.1)
        S = 1420
        def nino(n, x, alto=520, z=0.5, **k):
            ymesa = S - comun.APOYO.get(n, 0.956) * alto + 0.6 * alto      # canto delantero del pupitre
            an = alto * 0.85
            hp = an * 480 / 600
            return [pie(n, x, S, alto, z=z, **k), pieza("pupitre", x, round(ymesa + 0.15 * hp), round(an), z=z + 0.02)]
        return P(["#f2e6c8", "#a08060"], [
            fondo("bg_aula"),
            *nino("lucas_nino_pillado", 540, 560, 0.5, keys=late(te + 0.2, 1, 0.04)),
            *flip(["marta_nina_escribe_a", "marta_nina_escribe_b"], d, fps=3, base=lambda n: pie(n, -330, S, 520, z=0.45)),
            nino("marta_nina_escribe_a", -330, 520, 0.45)[1],
            pie("profesora_enfadada", 1400, S, 680, z=0.45),
            pieza("examen", 800, 780, 300, z=0.65, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": te, "op": 0, "escala": 0}, {"t": te + 0.05, "op": 1},
                                                         {"t": te + 0.4, "escala": 1, "rot": 8, "ease": "elastico"}, {"t": d, "rot": 4, "y": 760}]),
            senala(800, 760, te + 0.5, d - 0.05, 190, ROJO)],
            cam(1.0, 1.08, (560, 1050)), "corte", sfx=[(te, "pop", -20), (te + 0.5, "golpe", -20)])

    @plano(698, "pero la vida no es un examen")
    def _(d):
        S = 1440
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            *camina(["lucas_camina_a", "lucas_camina_b"], 150, 450, S, 620, d, fps=4, z=0.5),
            *camina(["marta_camina_a", "marta_camina_b"], -120, 180, S, 620, d, fps=4, z=0.52),
            pie("cafeteria_nueva", 1300, S - 20, 560, z=0.3), pie("hamburgueseria_lucas", 860, S - 20, 520, z=0.3),
            pieza("examen", 540, 960, 760, z=0.85, keys=[{"t": 0, "rot": -4, "x": 540, "y": 960}, {"t": 0.25, "rot": -6},
                                                          {"t": 0.75, "x": 1500, "y": 200, "rot": 70, "escala": 0.4, "ease": "anticipa"}, {"t": 0.8, "op": 0}])],
            cam(1.0, 1.06, (540, 1100)), "corte", sfx=[(0.3, "whoosh", -16)])

    @plano(705, "nadie te pide ser el primero")
    def _(d):
        o = rel(705)
        tp = min(max(0.5, o(711) - 0.1), d - 1.0)
        S = 1440
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pie("hamburgueseria", 540, S - 20, 600, z=0.35, keys=[{"t": 0, "escala": 1.0}, {"t": d, "escala": 0.97}]),
            *camina(["cliente_se_va_a", "cliente_se_va_b"], -300, 300, S, 610, d, fps=4, z=0.55),
            *camina(["lucas_camina_a", "lucas_camina_b"], 1450, 900, S, 620, d, fps=4, z=0.55, mira=-1),
            *aspa(540, 640, 230, tp + 0.55, g=20, z=0.95)],
            cam(1.0, 1.05, (540, 1050)), "corte",
            hud=[rotulo(tp, d - 0.05, "EL PRIMERO", tam=96, color="#ffffff", capsula="#6a6a78e6", y=640)],
            sfx=[(tp + 0.55, "golpe", -18)])

    @plano(714, "te piden ser el mejor")
    def _(d):
        o = rel(714)
        tm = min(max(0.3, o(718) - 0.1), d - 0.8)
        S = 1440
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pie("hamburgueseria_lucas", 230, S - 20, 640, z=0.3), pie("cafeteria_nueva", 850, S - 20, 640, z=0.3),
            pie("lucas_delantal", 300, S, 600, z=0.55, keys=late(tm, 1, 0.05)),
            pie("marta_delantal", 780, S, 600, z=0.55, keys=late(tm + 0.1, 1, 0.05)),
            *cola(-120, S, n=5, alto=560, z=0.5),
            *[{**pie(f"cola_{i}", 1200 + i * 110, S, 560, z=0.5 - 0.002 * i), "ex": -1} for i in range(4)],
            pieza("destello", 300, 820, 220, z=0.7, keys=[{"t": 0, "op": 0}, {"t": tm, "op": 0, "escala": 0}, {"t": tm + 0.3, "op": 1, "escala": 1, "rot": 45, "ease": "salida"}, {"t": d, "op": 0.4}]),
            pieza("destello", 780, 820, 220, z=0.7, keys=[{"t": 0, "op": 0}, {"t": tm + 0.1, "op": 0, "escala": 0}, {"t": tm + 0.4, "op": 1, "escala": 1, "rot": 45, "ease": "salida"}, {"t": d, "op": 0.4}])],
            cam(1.08, 1.0, (540, 1080)), "corte",
            hud=[rotulo(tm, d - 0.05, "EL MEJOR", tam=120, color="#2a1a00", capsula="#ffcf6af0", y=560)],
            sfx=[(tm, "brillo", -16)])

    @plano(719, "la próxima vez que quieras empezar algo")
    def _(d):
        S = 1440
        return P(["#38405a", "#6a5040"], [
            fondo("bg_habitacion"),
            pie("marta_piensa", 540, S, 780, z=0.55, keys=[{"t": 0, "x": 520}, {"t": d, "x": 560}]),
            *flip(["bombilla_a", "bombilla_b", "bombilla_a"], d, fps=2.2, base=lambda n: pieza(n, 800, 640, 170, z=0.6, anim={"flotar": [12, 1.6]})),
            pie("guitarra", -300, S, 500, z=0.5, rot=-5), pie("balon_futbol", -560, S, 180, z=0.5),
            pie("libro_recetas", 1340, S, 170, z=0.5), pie("olla", 1560, S, 220, z=0.5),
            brillo(800, 640, 240, "#ffe07a", 0.3, 0.55, pulso=[0.3, 0.9])],
            cam(1.0, 1.1, (540, 1050), (600, 1000)), "corte", sfx=[(0.5, "tic", -26), (1.4, "tic", -26)])

    @plano(728, "no busques la idea que nadie ha tenido")
    def _(d):
        o = rel(728)
        tn = min(max(0.8, o(733)), d - 0.6)
        pts = [(220, 700), (840, 820), (260, 1150), (820, 1250), (540, 960)]
        ks = [{"t": round(i * tn / (len(pts) - 1), 3), "x": x, "y": y, "ease": "suave"} for i, (x, y) in enumerate(pts)]
        bombs = [(150, 560), (930, 600), (120, 1300), (980, 1350), (-300, 800), (1400, 900), (-450, 1200), (1500, 600)]
        return P(["#0b0b14", "#050507"], [
            fondo("bg_estudio_oscuro"),
            *[pieza("bombilla_a", x, y, 130, z=0.3, op=0.4, anim={"parpadeo": [0.3, 1.3 + 0.2 * k], "flotar": [10, 2 + 0.3 * k]}) for k, (x, y) in enumerate(bombs)],
            {**pieza("app_buscador", 220, 700, 340, z=0.6), "keys": ks + [{"t": d, "escala": 0.9, "rot": -10}]},
            *aspa(540, 960, 230, tn + 0.1, g=26, z=0.8),
            {**polvo("#cfe6ff", 30, (-500, 400, 1580, 1500), 19), "_ancho": False}],
            cam(1.0, 1.05, (540, 960)), "corte", vineta=0.75, sfx=[(0.2, "roce", -24), (tn + 0.1, "golpe", -18)])

    @plano(736, "busca la cola")
    def _(d):
        S = 1440
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pie("cafeteria_nueva", 1720, S - 20, 600, z=0.3),
            *cola(1560, S, n=21, alto=500, paso=108, z=0.55, avanza=(0.4, 50)),
            brillo(1560, 1000, 300, "#ffe2a0", 0.5, 0.4, pulso=[0.15, 0.6]),
            fundido_blanco([{"t": 0, "op": 0.7}, {"t": 0.25, "op": 0.0}])],
            cam(1.12, 1.0, (540, 1100)), "corte",
            hud=[rotulo(0.12, d - 0.05, "BUSCA LA COLA", tam=130, color="#2a1a00", capsula="#ffcf6af0", y=620)],
            sfx=[(0.0, "impacto", -10)])

    @plano(739, "y ahora dime tú: ¿qué copiarías y qué le cambiarías?")
    def _(d):
        o = rel(739)
        t1 = o(743) - 0.1
        t2 = o(745) - 0.1
        S = 1440
        return P(["#bfe3f7", "#c9c2b5"], [
            fondo("bg_calle_dia"),
            pie("hamburgueseria_lucas", -120, S - 30, 680, z=0.3), pie("cafeteria_nueva", 1200, S - 30, 680, z=0.3),
            pie("lucas_contento", 360, S, 640, z=0.55, keys=[{"t": 0, "x": 340}, {"t": d, "x": 370, "ease": "suave"}]),
            pie("marta_sonrie", 740, S, 640, z=0.55, keys=[{"t": 0, "x": 760}, {"t": d, "x": 730, "ease": "suave"}]),
            *cola(-260, S, n=4, alto=520, z=0.5), *[{**pie(f"cola_{i}", 1340 + i * 105, S, 520, z=0.5 - 0.002 * i), "ex": -1} for i in range(3)],
            pieza("icono_igual", 230, 640, 130, z=0.65, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": t1, "op": 0, "escala": 0}, {"t": t1 + 0.05, "op": 1}, {"t": t1 + 0.4, "escala": 1, "ease": "elastico"}],
                  anim={"flotar": [14, 2.2]}),
            pieza("icono_mas", 850, 640, 130, z=0.65, keys=[{"t": 0, "op": 0, "escala": 0}, {"t": t2, "op": 0, "escala": 0}, {"t": t2 + 0.05, "op": 1}, {"t": t2 + 0.4, "escala": 1, "ease": "elastico"}],
                  anim={"flotar": [14, 2.6]}),
            brillo(540, 900, 600, "#ffe2a0", 0.3, 0.2, pulso=[0.06, 2.0])],
            cam(1.0, 1.1, (540, 1080), (540, 1040)), "corte", energia=0.4,
            hud=[rotulo(t1, t2 - 0.05, "¿QUÉ COPIARÍAS?", tam=100, color="#ffffff", capsula="#2f6fb0e6", y=480),
                 rotulo(t2, d - 0.05, "¿QUÉ LE CAMBIARÍAS?", tam=100, color="#2a1a00", capsula="#ffcf6af0", y=480)],
            sfx=[(t1, "pop", -22), (t2, "pop", -22)])
