# Método denso — guía para montar un vídeo

Estándar desde el 2026-11-16 (`DECISIONS.md`). Ejemplo completo y modelo de calidad: `lotes/prueba-luna-densa/gen.py`
(«La Luna se aleja», 155 palabras, 40 planos, 55 s). Código: `motor/denso.py` (montaje) y `motor/biblioteca/` (ilustraciones).

## Pasos
1. **Guion** de ≈150–160 palabras (voz a velocidad normal → 50–58 s), con **10–12 datos o imágenes distintas**. Cada frase tiene que dar algo que dibujar.
2. **Índices de palabra**: `python3 -m motor.denso guion.txt` (o con la alineación real como segundo argumento). Cada plano empieza en una palabra.
3. **Lista de planos antes de programar** (35–40 para 55 s). Para cada frase: plano principal + 0–2 **micro escenas** de detalle secundario (0,3–0,8 s: un primer plano, un objeto, una consecuencia, una comparación cotidiana).
4. **Generador** `gen.py` con `from motor.denso import *`, un `@v.plano(i, "nombre")` por plano y `v.construir(...)`.
5. **Sin voz todavía**: se monta igual (tiempos provisionales) → `--hoja --cada 1` → corregir → voz → volver a ejecutar `gen.py DIR audio.mp3 alineacion.json` (los cortes se recolocan solos) → render.

## Reglas (todas vienen de correcciones de Nico sobre la prueba)
- **Ritmo variable**: micro planos de 0,3–0,7 s en los golpes (cuenta atrás, cifras, detalles) y planos de 2–3 s donde hay que entender algo. Si casi todos duran lo mismo, está mal. El informe de `construir` enseña las duraciones.
- **Lectura**: todo rótulo ≥ 0,25 s + 1 s por 17 letras. `construir` avisa con ⚠: se acorta el texto, se alarga el plano o se quita el rótulo si solo repite el subtítulo. **No se entrega con avisos.**
- **Siempre pasa algo**: en cada plano, una acción (algo cae, se enciende, gira, crece, cuenta) y 5–9 elementos en capas (`z` de 0,05 a 0,9).
- **Detalles de fondo que duran**: lo que cruza el fondo (satélite, bandada, nube, barco, meteorito lejano) se mueve con `recorrido(T0, T1, …)` usando `v.w(i)` para T0 y T1, y se repite en todos los planos de ese tramo. Mínimo 4–5 s en pantalla. Nada que aparezca y desaparezca en un instante.
- **Figuras detalladas, variadas y haciendo cosas**: volumen, textura, luz de borde, ojo y sombra (`ilus._animal`); varias especies o modelos, no uno repetido; que coman, corran o miren (ver `comer()` en el ejemplo).
- **Fondos con tonos y profundidad**: nebulosas por capas (`bg_espacio_rico`, 3 paletas), bruma entre capas, relieve lejano más claro y azulado, primer plano oscuro. Nunca un degradado plano.
- **Contraste**: sobre fondos oscuros, flechas, órbitas y palabras clave en `CIAN`, `MAGENTA`, `LIMA`, `AMBAR` (el halo lo pone `construir`).
- **Flechas**: la punta nunca acaba dentro del objeto al que sigue; el objeto va por delante.
- **Sonido**: un efecto bajo para lo que pasa en pantalla — `tictac` (relojes), `agua`, `mordisco`, `meteoro`, `zap`, `golpe`, `brillo`, `ding`, `senal`… (lista en `motor/sfx.py`). Automáticos: tic por raya, soplo de estrella fugaz, «pop» de rótulo y whoosh de transición (pocos y muy bajos). Niveles orientativos: detalles −28…−22 dB, acciones −18…−12, golpes fuertes −12…−8. **La música se tiene que oír** (`"db": -13`).
- **Final**: un micro plano fuerte antes del cambio de bloque (el meteorito) y último plano largo con cierre.

## Ilustraciones nuevas para un tema
Lo que ya existe está en `motor/biblioteca/svg/` (fijas) y `motor/biblioteca/ilus.py` (generadas: 3 espacios, superficie lunar, eclipse, jungla, pista de hielo, 5 dinosaurios, pterosaurio, cohete, módulo lunar, satélite, meteorito, almeja, calendario, ramas, arbusto, siluetas).
Para un tema nuevo, crea `ilus_tema.py` en la carpeta del lote usando los ladrillos de `ilus` (`guardar`, `lg`, `rg`, `grano`, `_animal`, `_neb`, `_estrellas_ricas`, `_hoja`…), escribe los SVG en una carpeta y pásala a `Video(..., svg_extra=carpeta)`. **Mira cada SVG rasterizado antes de montar** (`rsvg-convert -w 400`). Si una pieza es reutilizable (un animal, un fondo, un objeto común), añádela a `motor/biblioteca/ilus.py` y a `generar()` en el mismo commit.

## El primer segundo (lo que más pesa, según nuestros datos)
Un solo objeto grande, **ya en pantalla y moviéndose en el fotograma 0**, que se entienda sin leer (la bota que cae sobre la Luna: 80 % se queda; una cabeza de moái quieta 3 s: 52 %). Sin metáforas en el primer plano. Primera frase de 5 palabras o menos y la afirmación sorprendente dicha antes del segundo 3,5. Para el sujeto: `keys=arranque(x, y, d)` (entra con muelle y no se queda quieto) y una segunda acción hacia la mitad del plano. `motor.calidad --mp4` da ❌ si el primer segundo está quieto.

## Control antes de entregar
`python3 -m motor.calidad DIR/episodio.json --mp4 DIR/out/<id>.mp4` sin ❌ (ritmo, zona segura, lectura, gancho, sonido, movimiento, mezcla). El porqué de cada regla, los tipos de plano y de gancho, el movimiento (`aparece`, `cae`, `lanza`, `late`, `sigue`, `senala`), el sonido (`subida` + `impacto` antes y en la revelación) y el cierre en bucle (`v.construir(..., bucle=0.35)`) están en **`motor/GUIA_CALIDAD.md`**. Antes de empezar un lote, lee **`motor/APRENDIZAJE.md`** (qué dicen nuestros datos y qué experimento toca).

Subtítulo de una o dos palabras enormes (experimento H1): `v.construir(..., subtitulos="palabra")`. En ese modo los rótulos de palabra clave (`amarillo`) se quitan solos, porque el subtítulo ya la enseña en amarillo, y los contadores se colocan debajo del subtítulo. `fijo=True` en un rótulo impide que se mueva; `sin_pop=True` le quita el sonido automático.

`construir` sin ⚠ · hoja de fotogramas cada 1 s revisada · ningún rótulo tapa al sujeto ni choca con el subtítulo (y≈300) · detalles de fondo visibles varios planos · −19 LUFS.
