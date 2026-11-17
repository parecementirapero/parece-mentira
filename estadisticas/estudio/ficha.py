"""Ficha de variables: cada vídeo descrito con las mismas variables, ANTES de publicarlo.

Las fichas viven en estadisticas/fichas.json, con clave «<lote>/<NN>» (se conoce antes de publicar).
Al publicar se añade el id de YouTube («youtube») para unir la ficha con las estadísticas.

Hay tres clases de variable:
  auto        las calcula este módulo a partir del guion o del informe de motor.calidad
  objetiva    se mira y se apunta, sin interpretación (palabras en pantalla en el fotograma 0…)
  subjetiva   pide criterio (tema, tipo de gancho…): son las que se comprueban con dos codificadores
"""
import datetime as dt
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTADISTICAS = os.path.dirname(AQUI)
RAIZ = os.path.dirname(ESTADISTICAS)
FICHAS = os.path.join(ESTADISTICAS, "fichas.json")

CAT, NUM, BOOL = "categoría", "número", "sí/no"

# nombre -> (tipo, clase, valores permitidos o None, descripción)
VARIABLES = {
    # --- tema
    "tema": (CAT, "subjetiva", ["Cotidiano", "Histórico", "Espacio", "Ciencia", "Misterio", "Humor"],
             "De qué va. Mismos valores que etiquetas.json."),
    "alcance": (CAT, "subjetiva", ["universal", "nicho"],
                "universal = cualquiera reconoce el sujeto en un segundo (la Luna, tu móvil, un plátano); "
                "nicho = hay que saber algo antes (Zanzíbar, un sultán, un científico concreto)."),
    "epoca": (CAT, "subjetiva", ["actual", "siglo XX", "1500–1900", "antigua", "prehistoria", "futuro", "sin época"],
              "Cuándo ocurre lo principal que se cuenta."),
    "reciclado": (BOOL, "objetiva", None, "El tema ya fue viral en otra cuenta (ver análisis de Reels)."),
    # --- gancho (primera frase)
    "gancho": (CAT, "subjetiva", ["pregunta", "dato", "contraste", "comparación", "negación", "reto", "orden", "historia"],
               "Tipo de la primera frase. orden = imperativo («Mira tus uñas»); contraste = dos cosas que chocan; "
               "comparación = se mide con algo cotidiano; negación = desmiente algo («no es humana»); "
               "reto = desafía al espectador («si crees que…»)."),
    "gancho_palabras": (NUM, "auto", None, "Palabras de la primera frase."),
    "gancho_persona": (CAT, "auto", ["tú", "nosotros", "impersonal"], "A quién habla la primera frase."),
    "gancho_cifra": (BOOL, "auto", None, "La primera frase lleva una cifra."),
    "gancho_negacion": (BOOL, "auto", None, "La primera frase niega algo (no, ni, nunca…)."),
    "gancho_pregunta": (BOOL, "auto", None, "La primera frase es una pregunta."),
    # --- primer fotograma / primer segundo
    "f0_palabras": (NUM, "objetiva", None, "Palabras legibles en pantalla en el fotograma 0."),
    "f0_movimiento": (NUM, "auto", None, "movimiento_primer_segundo de motor.calidad (con el MP4)."),
    "f0_mov_hoja": (NUM, "objetiva", None, "Movimiento del primer segundo medido sobre el vídeo publicado con "
                    "herramientas/hoja_short.js. Escala distinta a f0_movimiento: no se mezclan."),
    "f0_sujeto": (CAT, "subjetiva", ["objeto", "persona", "animal", "lugar", "texto", "varios"],
                  "Lo que domina el primer fotograma."),
    "f0_literal": (BOOL, "subjetiva", None,
                   "El primer fotograma enseña la cosa de la que se habla (sí) o una metáfora de ella (no). "
                   "Ejemplo de «no»: un marcador de fútbol para hablar de una guerra."),
    # --- guion
    "estructura": (CAT, "subjetiva", ["comparación", "experimento", "reconstrucción", "misterio por pistas", "metáfora visual",
                                      "cadena de datos", "cuenta atrás", "mito y realidad", "escala"],
                   "Cómo avanza el vídeo. Mismos valores que etiquetas.json, más los de la guía de calidad."),
    "palabras": (NUM, "auto", None, "Palabras de la locución."),
    "palabras_seg": (NUM, "auto", None, "Palabras por segundo (motor.calidad)."),
    "preguntas": (NUM, "auto", None, "Preguntas dichas en la locución."),
    "remate": (CAT, "subjetiva", ["pregunta", "dato", "giro", "consejo", "bucle"],
               "Cómo acaba la locución: pregunta al espectador, último dato, giro que rompe lo anterior, "
               "consejo («no te lo pierdas»), o frase que enlaza con la primera."),
    # --- forma
    "duracion_s": (NUM, "objetiva", None, "Duración del vídeo en segundos."),
    "cortes_min": (NUM, "auto", None, "Cortes por minuto (motor.calidad)."),
    "nota_calidad": (NUM, "auto", None, "Nota de motor.calidad (0–100)."),
    "montaje": (CAT, "objetiva", ["v2", "v4", "denso"], "Método de montaje."),
    "subtitulo": (CAT, "objetiva", ["karaoke", "palabra"], "Modo de subtítulo."),
    "voz": (CAT, "objetiva", ["v1", "clon"], "Voz de la locución."),
    # --- control
    "experimento": (CAT, "objetiva", None, "Id del experimento (H3…) o «no»."),
    "brazo": (CAT, "objetiva", ["A", "B", "-"], "Brazo del experimento: A = con el cambio, B = sin él."),
}
SUBJETIVAS = [k for k, v in VARIABLES.items() if v[1] == "subjetiva"]
OBLIGATORIAS = ["tema", "alcance", "gancho", "gancho_palabras", "f0_palabras", "f0_sujeto", "f0_literal",
                "estructura", "remate", "duracion_s", "montaje", "experimento"]
META = ("titulo", "lote", "numero", "youtube", "tiktok", "instagram", "codificado", "momento", "codificador", "notas")

NUMEROS = set("""cero uno una dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciséis
diecisiete dieciocho diecinueve veinte veintiuno veintidós veintitrés veinticuatro veinticinco veintiséis veintisiete
veintiocho veintinueve treinta cuarenta cincuenta sesenta setenta ochenta noventa cien ciento doscientos trescientos
cuatrocientos quinientos seiscientos setecientos ochocientos novecientos mil millón millones medio mitad doble triple""".split())
SOLO_NUMERO = NUMEROS - {"uno", "una", "medio", "mitad"}  # «una» es casi siempre artículo
TU = {"tú", "tu", "tus", "te", "ti", "contigo", "tuyo", "tuya", "tuyos", "tuyas"}
IMPERATIVOS = {"mira", "imagina", "piensa", "prueba", "fíjate", "cuenta", "escucha", "busca", "haz", "toca", "abre", "cierra"}
NOSOTROS = {"nosotros", "nos", "nuestro", "nuestra", "nuestros", "nuestras"}
NEGACIONES = {"no", "ni", "nunca", "jamás", "nadie", "ningún", "ninguna", "ninguno", "tampoco"}


def palabras_de(texto):
    return re.findall(r"[0-9A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", texto or "")


def primera_frase(texto):
    """Hasta el primer punto, cierre de pregunta/exclamación o dos puntos."""
    t = " ".join((texto or "").split())
    m = re.match(r"(.+?(?:[.?!:]|…(?=\s+[A-ZÁÉÍÓÚÑ¿¡]|$)))(\s|$)", t)
    return (m.group(1) if m else t).strip()


def ultima_frase(texto):
    t = " ".join((texto or "").split())
    partes = [p for p in re.split(r"(?<=[.?!…])\s+", t) if p.strip()]
    return partes[-1].strip() if partes else ""


def derivar_de_guion(texto):
    """Variables que salen solas de la locución."""
    frase = primera_frase(texto)
    pal = [p.lower() for p in palabras_de(frase)]
    if set(pal) & TU or (pal and pal[0] in IMPERATIVOS):
        persona = "tú"
    elif set(pal) & NOSOTROS:
        persona = "nosotros"
    else:
        persona = "impersonal"
    return {
        "gancho_palabras": len(pal),
        "gancho_persona": persona,
        "gancho_cifra": bool(set(pal) & SOLO_NUMERO or re.search(r"\d", frase)),
        "gancho_negacion": bool(set(pal) & NEGACIONES),
        "gancho_pregunta": "?" in frase,
        "palabras": len(palabras_de(texto)),
        "preguntas": (texto or "").count("?"),
    }


def derivar_de_calidad(md):
    """Variables que salen del informe de motor.calidad (calidad-NN.md)."""
    def num(patron):
        m = re.search(patron, md or "")
        return float(m.group(1)) if m else None
    res = {
        "nota_calidad": num(r"Nota:\s*([\d.]+)\s*/\s*100"),
        "cortes_min": num(r"cortes_min=([\d.]+)"),
        "palabras_seg": num(r"palabras_s=([\d.]+)"),
        "f0_movimiento": num(r"movimiento_primer_segundo=([\d.]+)"),
    }
    return {k: v for k, v in res.items() if v is not None}


def validar(ficha):
    """Lista de problemas de una ficha (vacía = correcta)."""
    problemas = []
    for k in OBLIGATORIAS:
        if ficha.get(k) is None:
            problemas.append(f"falta «{k}»")
    for k, v in ficha.items():
        if k in META or v is None:
            continue
        if k not in VARIABLES:
            problemas.append(f"«{k}» no está en el diccionario de variables")
            continue
        tipo, _, valores, _ = VARIABLES[k]
        if tipo == NUM and (isinstance(v, bool) or not isinstance(v, (int, float))):
            problemas.append(f"«{k}» tiene que ser un número (es {v!r})")
        elif tipo == BOOL and not isinstance(v, bool):
            problemas.append(f"«{k}» tiene que ser true o false (es {v!r})")
        elif tipo == CAT and valores and v not in valores:
            problemas.append(f"«{k}»: {v!r} no es uno de {', '.join(valores)}")
    if ficha.get("momento") not in ("previo", "retrospectivo"):
        problemas.append("«momento» tiene que ser previo (codificada antes de publicar) o retrospectivo")
    return problemas


def cargar(ruta=FICHAS):
    if not os.path.exists(ruta):
        return {}
    return {k: v for k, v in json.load(open(ruta, encoding="utf-8")).items() if not k.startswith("_")}


def guardar(fichas, ruta=FICHAS):
    previo = json.load(open(ruta, encoding="utf-8")) if os.path.exists(ruta) else {}
    cabecera = {k: v for k, v in previo.items() if k.startswith("_")} or {
        "_instrucciones": "Ficha de variables de cada vídeo (estadisticas/estudio/README.md). Clave «<lote>/<NN>». "
                          "Se rellena ANTES de publicar (momento: previo) y no se cambia al ver los resultados; "
                          "al publicar solo se añade el id de YouTube. Comprobar: python3 estadisticas/estudio ficha comprobar"}
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump({**cabecera, **fichas}, f, ensure_ascii=False, indent=1)
        f.write("\n")


def nueva(lote, numero, guion=None, calidad=None, valores=None, momento="previo", codificador=None, hoy=None):
    """Monta una ficha con todo lo automático y los valores que se le pasen a mano."""
    ficha = {"lote": lote, "numero": numero, "momento": momento,
             "codificado": (hoy or dt.date.today()).isoformat()}
    if codificador:
        ficha["codificador"] = codificador
    if guion:
        ficha.update(derivar_de_guion(guion))
    if calidad:
        ficha.update(derivar_de_calidad(calidad))
    ficha.update(valores or {})
    return ficha


def convertir(clave, texto):
    """«clave=valor» de la línea de órdenes -> valor con el tipo del diccionario."""
    if clave in META or clave not in VARIABLES:
        return texto
    tipo = VARIABLES[clave][0]
    if tipo == NUM:
        return float(texto) if "." in texto else int(texto)
    if tipo == BOOL:
        return texto.strip().lower() in ("si", "sí", "true", "1", "s")
    return texto


def acuerdo(fichas_a, fichas_b):
    """Coincidencia entre dos codificadores en las variables subjetivas.
    Devuelve {variable: (coinciden, comparadas)} sobre los vídeos que tienen los dos."""
    res = {}
    for var in SUBJETIVAS:
        coinciden = comparadas = 0
        for clave in set(fichas_a) & set(fichas_b):
            a, b = fichas_a[clave].get(var), fichas_b[clave].get(var)
            if a is None or b is None:
                continue
            comparadas += 1
            coinciden += a == b
        res[var] = (coinciden, comparadas)
    return res


def diccionario_md():
    """El diccionario de variables en una tabla, para el README."""
    lineas = ["| Variable | Tipo | Clase | Valores | Qué es |", "|---|---|---|---|---|"]
    for k, (tipo, clase, valores, desc) in VARIABLES.items():
        lineas.append(f"| `{k}` | {tipo} | {clase} | {' · '.join(valores) if valores else '—'} | {desc} |")
    return "\n".join(lineas)
