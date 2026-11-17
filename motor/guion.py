"""Revisa un guion ANTES de generar la voz (para no gastar créditos de ElevenLabs en un guion que luego hay que rehacer).

    python3 -m motor.guion lotes/<lote>/guion.txt [--corto]

Comprueba lo que los datos del canal y la guía dicen que importa (motor/APRENDIZAJE.md, motor/GUIA_CALIDAD.md):
  - gancho: primera frase de 5 palabras o menos (❌ a partir de 10) y la afirmación sorprendente dicha antes del segundo 3,5
  - duración: 150–160 palabras (≈53–56 s) o, con --corto, 95–110 (≈33–38 s); nunca más de 165
  - cadena de preguntas: una pregunta nueva cada 8–12 s (al menos 2 en un guion normal, 1 en uno corto)
  - frases que se puedan decir de un tirón (aviso por encima de 22 palabras)
  - cifras escritas en letra (ninguna cifra en números: la voz las lee mal)
  - expresiones solo de España (el 79 % de la audiencia es de Latinoamérica)
  - remate: la última frase es corta y no es una despedida
  - densidad: datos o imágenes distintas (cifras, nombres propios) repartidos por todo el guion
Sale con código 1 si hay algún ❌.
"""
import argparse, re, sys

VOZ = 2.85  # palabras por segundo de la voz oficial
SOLO_ESPANA = ["flipar", "flipa", "flipante", "tío", "tía", "mola", "molar", "mogollón", "guay", "chulo", "vale,", "currar", "curro",
               "ordenador", "móvil", "coche", "patata", "zumo", "vosotros", "os ", "habéis", "tenéis", "podéis", "sabéis", "mirad", "fijaos"]
DESPEDIDAS = ["suscríbete", "sígueme", "hasta la próxima", "nos vemos", "dale like", "gracias por ver"]
NUM_LETRA = ("cero uno una dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince veinte treinta cuarenta cincuenta sesenta "
             "setenta ochenta noventa cien ciento doscientos trescientos cuatrocientos quinientos seiscientos setecientos ochocientos novecientos "
             "mil millón millones medio media").split()


def revisar(texto, corto=False):
    av = []
    frases = [f.strip() for f in re.split(r"(?<=[.?!…:])\s+", texto.strip()) if f.strip()]
    pal = texto.split()
    n = len(pal)
    dur = n / VOZ + 0.5
    # gancho
    g = len(frases[0].split())
    if g > 9: av.append(("❌", f"Gancho de {g} palabras («{frases[0][:60]}…»): muro de texto en el fotograma 0. Máximo 5; el resto, en la segunda frase."))
    elif g > 5: av.append(("⚠", f"Gancho de {g} palabras: mejor 5 o menos («Mira tus uñas.», «Esta pisada sigue ahí.»)."))
    # ¿cuándo queda dicha la afirmación sorprendente? (TikTok Studio, 2026-11-17: hasta nuestros mejores vídeos pierden el 40 %
    # en los 3 primeros segundos; lo que no se haya prometido para entonces no lo oye casi la mitad)
    n_promesa = g if g >= 6 or len(frases) < 2 else g + len(frases[1].split())
    if n_promesa / VOZ > 4.2:
        av.append(("⚠", f"La afirmación sorprendente no queda dicha hasta el segundo {n_promesa / VOZ:.1f} ({n_promesa} palabras entre las dos primeras frases). "
                        "Objetivo: antes del segundo 3,5 (unas 10 palabras). Ejemplo: «Mira tus uñas. La Luna se aleja igual de rápido.»"))
    # duración
    lo, hi = (95, 110) if corto else (150, 160)
    if n > 165: av.append(("❌", f"{n} palabras ≈ {dur:.0f} s: el Short puede pasar de 60 s. Máximo 165."))
    elif not lo <= n <= hi: av.append(("⚠", f"{n} palabras ≈ {dur:.0f} s (objetivo {lo}–{hi})."))
    # preguntas
    preg = [i for i, f in enumerate(frases) if "?" in f]
    minimo = 1 if corto else 2
    if len(preg) < minimo: av.append(("⚠", f"Solo {len(preg)} pregunta(s): la curiosidad se mantiene encadenando preguntas («¿Cómo lo sabemos?», «¿Y por qué?»). Mínimo {minimo}."))
    # tramos largos sin pregunta ni cifra (explicación seguida)
    acum, peor = 0, 0
    for f in frases:
        tiene_gancho = "?" in f or any(w.strip(".,;:¿?¡!").lower() in NUM_LETRA for w in f.split())
        acum = 0 if tiene_gancho else acum + len(f.split())
        peor = max(peor, acum)
    if peor / VOZ > 12: av.append(("⚠", f"Hay un tramo de ≈{peor / VOZ:.0f} s seguidos sin pregunta ni dato: ahí es donde la gente se va."))
    # frases largas
    largas = [f for f in frases if len(f.split()) > 22]
    if largas: av.append(("⚠", f"{len(largas)} frase(s) de más de 22 palabras (difíciles de decir y de montar): «{largas[0][:70]}…»"))
    # cifras en número
    cifras = re.findall(r"\d[\d.,]*", texto)
    if cifras: av.append(("❌", f"Cifras en números ({', '.join(cifras[:6])}): escríbelas en letra, la voz las lee mal."))
    # España
    bajo = " " + texto.lower() + " "
    esp = [e.strip() for e in SOLO_ESPANA if re.search(r"(?<![a-záéíóúñ])" + re.escape(e.strip()) + r"(?![a-záéíóúñ])", bajo)]
    if esp: av.append(("ℹ", "Palabras que suenan a España o cambian en Latinoamérica: " + ", ".join(sorted(set(esp))) + ". Revisa si hay una forma común (DECISIONS 2026-11-16)."))
    # remate
    ult = frases[-1]
    if len(ult.split()) > 12: av.append(("⚠", f"La última frase tiene {len(ult.split())} palabras: el remate tiene que ser seco (≤ 12)."))
    if any(d in ult.lower() for d in DESPEDIDAS): av.append(("⚠", "La última frase es una despedida: mejor la consecuencia final o una invitación ligada al dato."))
    # densidad
    datos = sum(1 for w in pal if w.strip(".,;:¿?¡!").lower() in NUM_LETRA) + len(re.findall(r"(?<=[a-záéíóúñ,] )[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+", texto))
    if datos < (6 if corto else 10): av.append(("ℹ", f"Pocos datos concretos detectados ({datos} entre cifras y nombres propios): el método denso pide 10–12 imágenes o datos distintos."))
    return dict(palabras=n, segundos=round(dur, 1), frases=len(frases), gancho_palabras=g, preguntas=len(preg), avisos=av)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("guion"); ap.add_argument("--corto", action="store_true", help="vídeo de 33–38 s (experimento H2)")
    a = ap.parse_args(argv)
    r = revisar(open(a.guion, encoding="utf-8").read(), a.corto)
    print(f"{r['palabras']} palabras ≈ {r['segundos']} s · {r['frases']} frases · gancho de {r['gancho_palabras']} palabras · {r['preguntas']} preguntas")
    for nivel, t in sorted(r["avisos"], key=lambda x: "❌⚠ℹ".index(x[0])):
        print(f"  {nivel} {t}")
    if not r["avisos"]: print("  ✓ guion listo para la voz")
    return 1 if any(n == "❌" for n, _ in r["avisos"]) else 0


if __name__ == "__main__":
    sys.exit(main())
