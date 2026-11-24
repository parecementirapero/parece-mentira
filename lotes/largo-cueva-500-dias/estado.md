# Vídeo largo «¿Qué pasaría si te encerraras 500 días en una cueva sin reloj?» — estado

**Estado**: 🟡 **v1 en revisión**. Falta el «ok» de Nico. No se ha publicado nada.
**Quién**: Nico (encargo del 24-11), con el agente, en el chat https://claude.ai/code/session_019BG1dFtXHqVXWrKbh8QXsf (el de Jorge; misma cuenta).
**Carpeta local**: `Documents/Parece Mentira/lotes/largo-cueva-500-dias/` en el Mac de Jorge. Ahí están:
- los 5 MP3 de voz y sus alineaciones,
- `largo-cueva-500-dias-16x9.mp4`,
- las 5 partes `parte-N-de-5.mp4`.

## Entregables
| Archivo | Formato | Duración | SHA-256 corto |
|---|---|---|---|
| largo-cueva-500-dias-16x9.mp4 | 1920×1080 · 30 fps · YouTube | 8:31,86 | 8149a05c77af |
| parte-1-de-5.mp4 … parte-5-de-5.mp4 | 1080×1920 · 30 fps · TikTok | 1:47,3 · 1:48,9 · 1:41,2 · 1:21,0 · 1:53,3 | ver `partes.json` |

Las 5 partes suman exactamente los 15.356 fotogramas del vídeo largo y llevan su mismo audio: la mezcla del horizontal cortada en los mismos puntos.

## Voz (un solo intento)
- Clon `op8soO9fvP07F3mjbJuB`, `eleven_v4`, 0,5 / 0,75, `/with-timestamps`; generada en 5 bloques, uno por parte, con `previous_text`/`next_text` (`generadores/voz.py`, desde el Mac de Jorge).
- Guion exacto: 7.429 caracteres. La alineación coincide letra a letra en los 5 bloques.
- Coste real: 17.947 → 15.648 créditos (≈2.300). No se regeneró nada.
- Cada bloque se igualó a −18 LUFS y se unieron con 0,45 s de silencio (`voz/`, `cortes.json`). Los MP3 no van a git (DECISIONS); las alineaciones sí (`voz/*.json`).
- La clave no tiene permiso para leer voces ni modelos: se comprobó con el saldo y con la generación del lote 2026-11-23-tarde, hecha con la misma clave y voz.

## Montaje
- Método denso: **294 planos** (0,4–3,6 s, ≈34,5 cortes/min). Un solo montaje para los dos formatos: cada plano se escribe en coordenadas del vertical y `generadores/comun.py` (`adaptar`) lo recompone en 16:9.
  - Los fondos están dibujados en los dos formatos (`_h`).
  - En el horizontal, los laterales se rellenan con piezas que solo existen fuera del cuadro vertical.
- Arte propio: 190 SVG (`ARTE.md`, `ilus_*.py`).
  - Beatriz y Siffre son figuras genéricas: sin retratos, sin fotos y sin frases que no estén en el guion.
  - Relojes: 2 escenas, ambas en la parte 2 y no seguidas.
- Marcas de TikTok (solo en el vertical, `marcas.py`):
  - «PARTE N DE 5».
  - Ganchos de las partes 2–5, legibles desde el fotograma 0 y con movimiento.
  - «SIGUE EN LA PARTE N+1».
  - Cortes 0,23 s antes de la primera palabra de cada parte, en el silencio entre bloques, con fundidos de 0,15 s.
- Primer fotograma de las partes 2–5: el subtítulo de la frase anterior se quedaba 0,25 s en pantalla. Se volvió a renderizar ese inicio sin ella (`parche_inicios.py`) y el corte se movió al primer fotograma entero del plano nuevo.
- Motor: `MOTOR_FORMATO=16:9` (`motor/core.py`, `denso.py`, `render.py`, `calidad.py`). `python3 -m motor.prueba` OK.
- Render en la nube en dos tramos por formato: el render en paralelo se quedaba sin memoria. Para entregar se recodificó a 5,5 Mbps (horizontal) y 6 Mbps (partes).

## Control de calidad
- `construir`: todos los textos se pueden leer en los dos formatos.
- `motor.calidad --mp4`: **ningún ❌ en ninguno de los dos**. Informes en `calidad-16x9.md` (49/100) y `calidad-9x16.md` (43/100). La nota baja por la cantidad de ⚠ de las reglas de imagen, pensadas para Shorts de 55 s y que con 294 planos se acumulan. Justificación de los ⚠:
  - Primera frase de 6 palabras: es el guion de Nico, que no se cambia.
  - 24 fondos: la regla es para Shorts. Salen todos los escenarios.
  - Ritmo 0,38: hay planos de respiro largos a propósito, porque es un vídeo largo.
  - Planos pobres, calcados o con el mismo encuadre: sobre todo en la cueva oscura y en los «días iguales» de la parte 4, que son iguales a propósito. Quedan para la v2 si Nico quiere más variedad.
  - Poco contraste en «?» (60 s), «=» (462 s) y «≈ 1 AÑO» (358 s): son detalles menores.
  - Primer segundo con movimiento 2,0–2,5: es la bajada por el pozo, que ya se mueve desde el fotograma 0.
- Sincronía de voz y subtítulos comprobada en los minutos 1, 4 y 8: la palabra resaltada es la que suena.
- Ningún corte de parte cae dentro de una palabra: los silencios son 107,12→107,57, 216,05→216,50, 317,30→317,75 y 398,31→398,76.

## Textos
`metadatos.json` lleva:
- título, descripción con capítulos y comentario fijado del vídeo largo;
- título y texto de TikTok de cada parte.

Las fuentes están en `fuentes.md`.

## Siguiente paso
«ok» de Nico. Después se publica como diga: YouTube por la API y TikTok desde el navegador integrado, eligiendo él los archivos.
