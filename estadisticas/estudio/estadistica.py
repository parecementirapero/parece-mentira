"""Estadística para muestras pequeñas. Solo librería estándar.

Todo aquí está pensado para pocos vídeos (5–80): medianas en vez de medias, intervalos por
remuestreo (bootstrap) y pruebas de permutación, que no suponen ninguna distribución.
Las funciones aleatorias usan una semilla fija: el mismo dato da siempre el mismo resultado.
"""
import itertools
import math
import random
import statistics as st

SEMILLA = 20261117


def limpio(xs):
    return [float(x) for x in xs if x is not None]


def mediana(xs):
    xs = limpio(xs)
    return st.median(xs) if xs else None


def desviacion(xs):
    xs = limpio(xs)
    return st.stdev(xs) if len(xs) >= 2 else None


def cuantil(ordenados, q):
    """Cuantil por interpolación lineal sobre una lista ya ordenada."""
    if not ordenados:
        return None
    pos = (len(ordenados) - 1) * q
    lo, hi = int(math.floor(pos)), int(math.ceil(pos))
    return ordenados[lo] + (ordenados[hi] - ordenados[lo]) * (pos - lo)


# ------------------------------------------------------------------ dos grupos
def diferencia_medianas(a, b):
    a, b = limpio(a), limpio(b)
    if not a or not b:
        return None
    return st.median(a) - st.median(b)


def bootstrap_diferencia(a, b, n=2000, confianza=0.90, semilla=SEMILLA):
    """Intervalo de confianza de mediana(a) − mediana(b) por remuestreo.

    Devuelve (diferencia, inferior, superior) o None si algún grupo tiene menos de 3 valores
    (con 1 o 2 valores el remuestreo da una falsa sensación de precisión)."""
    a, b = limpio(a), limpio(b)
    if len(a) < 3 or len(b) < 3:
        return None
    rnd = random.Random(semilla)
    difs = []
    for _ in range(n):
        ra = [a[rnd.randrange(len(a))] for _ in a]
        rb = [b[rnd.randrange(len(b))] for _ in b]
        difs.append(st.median(ra) - st.median(rb))
    difs.sort()
    cola = (1 - confianza) / 2
    return (st.median(a) - st.median(b), cuantil(difs, cola), cuantil(difs, 1 - cola))


def permutacion(a, b):
    """Probabilidad (dos colas) de ver dos grupos así de separados si el reparto en grupos fuera al azar.
    Compara los rangos medios (es la prueba de Mann-Whitney hecha por permutación): no le afecta un vídeo
    viral. Exacta cuando hay pocas combinaciones; si no, con la aproximación normal de siempre.
    Devuelve None si algún grupo tiene menos de 2 valores."""
    a, b = limpio(a), limpio(b)
    if len(a) < 2 or len(b) < 2:
        return None
    rangos, k, total_n = _rangos(a + b), len(a), len(a) + len(b)
    suma_total = sum(rangos)

    def separacion(suma_a):
        return abs(suma_a / k - (suma_total - suma_a) / (total_n - k))
    obs = separacion(sum(rangos[:k]))
    total = math.comb(total_n, k)
    eps = 1e-9
    if total <= 50000:
        cuenta = sum(1 for comb in itertools.combinations(rangos, k) if separacion(sum(comb)) >= obs - eps)
        return cuenta / total
    # Muchas combinaciones: aproximación normal de la suma de rangos (con corrección por empates).
    # Es la forma habitual de la prueba de Mann-Whitney y es inmediata, tenga 30 vídeos o 3.000.
    m2 = total_n - k
    media = k * (total_n + 1) / 2
    empates = {}
    for r in rangos:
        empates[r] = empates.get(r, 0) + 1
    correccion = sum(t ** 3 - t for t in empates.values()) / (total_n * (total_n - 1))
    varianza = k * m2 / 12 * ((total_n + 1) - correccion)
    if varianza <= 0:
        return 1.0
    z = (abs(sum(rangos[:k]) - media) - 0.5) / math.sqrt(varianza)
    return min(1.0, 2 * (1 - st.NormalDist().cdf(max(z, 0))))


def p_minimo_posible(na, nb):
    """El p más pequeño que puede dar la prueba de permutación con esos tamaños.
    Con 3 contra 3 es 0,10: no puede salir «significativo» pase lo que pase."""
    if na < 1 or nb < 1:
        return None
    return (2 if na == nb else 1) / math.comb(na + nb, na)


# ------------------------------------------------------------------ dos variables numéricas
def _rangos(xs):
    orden = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(orden):
        j = i
        while j + 1 < len(orden) and xs[orden[j + 1]] == xs[orden[i]]:
            j += 1
        medio = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[orden[k]] = medio
        i = j + 1
    return r


def _pearson(x, y):
    mx, my = st.mean(x), st.mean(y)
    sx = math.sqrt(sum((v - mx) ** 2 for v in x))
    sy = math.sqrt(sum((v - my) ** 2 for v in y))
    if sx == 0 or sy == 0:
        return None
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


def spearman(x, y, n=5000, semilla=SEMILLA):
    """Correlación por rangos y su p por permutación. Devuelve (rho, p, n) o None con menos de 4 pares."""
    pares = [(float(a), float(b)) for a, b in zip(x, y) if a is not None and b is not None]
    if len(pares) < 4:
        return None
    rx, ry = _rangos([p[0] for p in pares]), _rangos([p[1] for p in pares])
    rho = _pearson(rx, ry)
    if rho is None:
        return None
    rnd = random.Random(semilla)
    cuenta, ry2 = 0, list(ry)
    for _ in range(n):
        rnd.shuffle(ry2)
        r = _pearson(rx, ry2)
        if r is not None and abs(r) >= abs(rho) - 1e-12:
            cuenta += 1
    return (rho, (cuenta + 1) / (n + 1), len(pares))


# ------------------------------------------------------------------ tamaño de muestra
def tamano_muestra(desv, diferencia, alfa=0.05, potencia=0.80):
    """Vídeos por grupo para detectar `diferencia` con esa desviación típica (dos grupos, dos colas).
    Aproximación normal: orienta, no garantiza."""
    if not desv or not diferencia:
        return None
    z = st.NormalDist()
    za, zb = z.inv_cdf(1 - alfa / 2), z.inv_cdf(potencia)
    return math.ceil(2 * ((za + zb) * desv / abs(diferencia)) ** 2)


def diferencia_detectable(desv, n_por_grupo, alfa=0.05, potencia=0.80):
    """Lo contrario: con n vídeos por grupo, la diferencia más pequeña que se puede detectar."""
    if not desv or not n_por_grupo:
        return None
    z = st.NormalDist()
    return (z.inv_cdf(1 - alfa / 2) + z.inv_cdf(potencia)) * desv * math.sqrt(2 / n_por_grupo)


# ------------------------------------------------------------------ índice relativo
def indice_relativo(valor, referencia):
    """valor / mediana de referencia. 1,3 = un 30 % mejor que lo normal del canal."""
    if valor is None or not referencia:
        return None
    return valor / referencia


# ------------------------------------------------------------------ niveles de evidencia
NIVELES = ("sin datos", "pista", "indicio", "regla")


def nivel_evidencia(n_a, n_b, intervalo=None, redes_coinciden=None, replicado=False, p=None, comparaciones=1):
    """Nivel de una comparación entre dos grupos.

    pista    menos de 5 vídeos en algún grupo, o nada que la distinga del azar
    indicio  5 o más por grupo, p < 0,10 y el mismo sentido en la otra red
             (si la otra red no tiene datos, se exige p < 0,05)
    regla    10 o más por grupo, intervalo de confianza que no cruza el cero, mismo sentido en la otra red,
             repetido en dos semanas y p por debajo de 0,05 repartido entre todas las comparaciones miradas
             (corrección de Bonferroni). `comparaciones` = cuántas se han mirado a la vez; en un experimento
             con ficha previa es 1, y por eso un experimento llega a regla con muchos menos vídeos.

    Comprobado con simulaciones sin ningún efecto real (90 vídeos, 56 comparaciones): sin la exigencia de p
    la mitad de las comparaciones salían «indicio» y 7 de cada 10 estudios daban alguna «regla» falsa.
    """
    menor = min(n_a or 0, n_b or 0)
    if menor < 1:
        return "sin datos"
    if menor < 5 or p is None or redes_coinciden is False:
        return "pista"
    cruza = intervalo is None or (intervalo[1] <= 0 <= intervalo[2])
    if menor >= 10 and not cruza and replicado and redes_coinciden and p < 0.05 / max(comparaciones, 1):
        return "regla"
    if (redes_coinciden and p < 0.10) or (redes_coinciden is None and p < 0.05):
        return "indicio"
    return "pista"


def nivel_correlacion(n, p, redes_coinciden=None):
    """Nivel de una relación entre dos variables numéricas. Sin experimento, nunca pasa de indicio."""
    if not n or n < 4:
        return "sin datos"
    if n >= 20 and p is not None and p < 0.05 and redes_coinciden is not False:
        return "indicio"
    return "pista"
