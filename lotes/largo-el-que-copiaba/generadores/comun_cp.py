"""Piezas comunes del vídeo «El que copiaba en el colegio».
Reutiliza el montaje en dos formatos del vídeo de la cueva (`lotes/largo-cueva-500-dias/generadores/comun.py`):
cada plano se escribe UNA vez en coordenadas del vertical (1080×1920) y `adaptar` lo pasa a 16:9.
Lee la cabecera de ese comun.py: `pie`, `pieza`, `flip`, `fondo`, `cam`, `polvo`, `negro`, `fundido_blanco`,
`_ancho`/`_full`/`_solo`, y deja los laterales (x<0 o x>1080) llenos para el horizontal."""
import os, sys, random
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
CUEVA = os.path.join(RAIZ, "lotes", "largo-cueva-500-dias", "generadores")
sys.path.insert(0, RAIZ); sys.path.insert(0, CUEVA); sys.path.insert(0, AQUI)
import comun  # noqa: E402  (el de la cueva)
from comun import *  # noqa: E402,F401,F403

# suelo de cada fondo nuevo (vertical y, horizontal y) — informe de ilus_fondos.py
comun.ANCLA.update({
    "bg_aula": (540, 1420, 960, 870), "bg_colegio_fuera": (540, 1430, 960, 880), "bg_calle_dia": (540, 1440, 960, 880),
    "bg_cafe_dentro": (540, 1430, 960, 880), "bg_cafe_dentro_triste": (540, 1430, 960, 880), "bg_cocina": (540, 1440, 960, 880),
    "bg_habitacion": (540, 1440, 960, 880), "bg_campo_barrio": (540, 1440, 960, 880), "bg_estudio_oscuro": (540, 1400, 960, 860),
})
SUELO = {k: v[1] for k, v in comun.ANCLA.items()}

comun.APOYO.update({
    # gente
    'marta_nina_escribe_a': 0.957, 'marta_nina_escribe_b': 0.957, 'marta_nina_orgullosa': 0.957, 'marta_nina_mano': 0.958,
    'lucas_nino_reojo': 0.956, 'lucas_nino_pillado': 0.956, 'lucas_nino_triste': 0.955, 'profesora_senala': 0.969,
    'profesora_enfadada': 0.969, 'profesora_aplaude': 0.969, 'profesora_aplaude_b': 0.969, 'marta_piensa': 0.97, 'marta_idea': 0.97,
    'marta_explica_a': 0.97, 'marta_explica_b': 0.97, 'marta_triste': 0.969, 'marta_camina_a': 0.964, 'marta_camina_b': 0.964,
    'marta_sonrie': 0.97, 'marta_entiende': 0.97, 'marta_delantal': 0.97, 'lucas_camina_a': 0.964, 'lucas_camina_b': 0.964,
    'lucas_senala': 0.969, 'lucas_delantal': 0.969, 'lucas_entrega': 0.969, 'lucas_contento': 0.972, 'cliente_confuso_1': 0.97,
    'cliente_confuso_2': 0.97, 'cliente_se_va_a': 0.964, 'cliente_se_va_b': 0.964, 'cliente_feliz_1': 0.969, 'cliente_feliz_2': 0.97,
    'cliente_feliz_3': 0.969, 'nino_regate_a': 0.955, 'nino_regate_b': 0.955, 'guitarrista': 0.938, 'guitarrista_b': 0.938,
    'cocinero_receta': 0.988, 'bebe_habla': 0.855, 'bebe_habla_b': 0.855, 'padres_hablan': 0.96,
    'cara_marta_feliz': 1.0, 'cara_marta_triste': 1.0, 'cara_marta_sorpresa': 1.0, 'cara_lucas_listo': 1.0, 'cara_lucas_sonrie': 1.0,
    # cosas
    'cafeteria_marta': 0.988, 'cafeteria_marta_cerrada': 0.988, 'hamburgueseria_lucas': 0.988, 'hamburgueseria_vacia': 0.988,
    'cafeteria_nueva': 0.988, 'hamburgueseria': 0.988, 'pupitre': 0.954, 'pupitre_doble': 0.954, 'mochila_cole': 0.956,
    'hamburguesa': 0.93, 'bolsa_comida': 0.95, 'taza_cafe_latte': 0.966, 'reloj_arena_grande': 0.95, 'hucha': 0.928, 'hucha_rota': 0.91,
    'monedas': 0.91, 'saco_dinero': 0.944, 'balon_futbol': 0.892, 'guitarra': 0.974, 'libro_recetas': 0.94, 'olla': 0.936,
    'foco_luz': 0.949, 'foco_luz_frio': 0.949,
    # frame_prueba
    'lucas_piensa': 0.973, 'cola_0': 0.974, 'cola_1': 0.974, 'cola_2': 0.974, 'cola_3': 0.974, 'cola_4': 0.974, 'cola_5': 0.974,
})

# colores de la casa
ORO = "#ffcf6a"; ROJO = "#ff4a3d"; VERDE = "#4be08a"; CIAN = "#2ff3ff"; BLANCO = "#ffffff"

# Persiana sobre `cafeteria_marta` (lienzo 900×820): hueco de x=110..790, y=332..810 del lienzo de la fachada.
PERSIANA = dict(x0=110, y0=332, w=680, h=478, W=900, H=820)


def cola(x0, suelo, n=6, alto=430, paso=95, z=0.5, avanza=None, oscuro=0.0, d=99):
    """Cola de gente de perfil mirando a la derecha (hacia x0). La primera persona en x0, las demás hacia la izquierda.
    avanza=(t0, dx): toda la cola da un pasito a la derecha en t0."""
    out = []
    for i in range(n):
        nm = f"cola_{i % 6}"
        x = x0 - i * paso
        ks = []
        if avanza:
            t0, dx = avanza
            ks = [{"t": 0, "x": x}, {"t": t0 + 0.05 * i, "x": x}, {"t": t0 + 0.05 * i + 0.4, "x": x + dx, "ease": "suave"}]
        e = pie(nm, x, suelo, alto * (1 - 0.02 * i), z=z - 0.002 * i, keys=ks)
        if oscuro:
            e["op"] = 1 - oscuro
        out.append(e)
    return out


def mecer(d, amp=3, periodo=2.4, base=0):
    """Balanceo suave (giro) para que una figura quieta respire."""
    ks, t, s = [], 0.0, 1
    while t <= d + periodo:
        ks.append({"t": round(t, 3), "rot": base + s * amp, "ease": "suave"})
        t += periodo / 2; s = -s
    return ks


# Las piezas de ilus_gente.py llevan viewBox recortado con origen distinto de 0 0: tam_svg general.
import re as _re
def _tam_svg(nombre):
    if nombre not in comun._TAM:
        cab = open(os.path.join(comun.SVG_DIR, nombre + ".svg"), encoding="utf-8").read(600)
        m = _re.search(r'viewBox="\s*[-\d.]+[ ,]+[-\d.]+[ ,]+([\d.]+)[ ,]+([\d.]+)"', cab)
        comun._TAM[nombre] = (float(m.group(1)), float(m.group(2)))
    return comun._TAM[nombre]
comun.tam_svg = _tam_svg
