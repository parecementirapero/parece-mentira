# Lote 2026-11-20-tarde — estado

**Estado**: 🟢 **«ok» para YouTube** (v1). TikTok e Instagram: no pedidos.
**Agente**: Agente 20:00 (Jorge). Chat del lote: https://claude.ai/code/session_019BG1dFtXHqVXWrKbh8QXsf
**Carpeta local**: `Documents/Parece Mentira/lotes/2026-11-20-tarde/` (Mac de Jorge): MP4, SRT, manifiestos, `NN-episodio.json`, `NN-locucion.mp3`, `NN-alineacion.json`, `NN-portadas/portada.jpg`, `metadatos.json`.

## Vídeos
| # | Título | Duración | Versión | SHA-256 corto | Calidad | Portada |
|---|---|---|---|---|---|---|
| 01 | 16 amaneceres al día en la Estación Espacial 🌅🛰️ | 56,2 s | v1 | 57b0d69e3946 | 75/100 | «16 AMANECERES AL DÍA» · abajo · 3,25 s |
| 02 | Desde esta montaña de España se ve ÁFRICA 🏔️🌍 | 58,3 s | v1 | de1f3da5878e | 64/100 | «DESDE AQUÍ SE VE ÁFRICA» · centro · 1,25 s |
| 03 | Los flamencos nacen GRISES 🦩 | 57,3 s | v1 | 8e173fa2690b | 55/100 | «LOS FLAMENCOS NACEN GRISES» · centro · 2,75 s |

SHA en el Mac = SHA del render (comprobado con `shasum -a 256`).

## Registro
- 2026-11-20 22:47: la tarea de las 19:52 se disparó a las 22:47 con el Mac de Jorge fuera del puente → «ordenador no disponible», correo `[AVISO]` `1a1faef9e1379be2`.
- 2026-11-21 01:03: una persona escribe en el chat «créame los vídeos que no has podido crear hoy en mi lote». El Mac ya responde → reserva y lote entero.
- Créditos de ElevenLabs: 21.876 al empezar → **20.837** al acabar (voz por API desde el Mac, `with-timestamps`, una sola toma por vídeo).
- Render en la nube; MP4, portadas y textos copiados al Mac.

## Tendencias de hoy
Archivo: `lotes/tendencias/2026-11-20.md` (lo hizo el turno de mañana). Quedaban sin usar Vuelta de Obligado (descartada: batalla con muertos y fecha patria), Sierra Nevada / África (✔ **02**) y cambio climático (descartada: genérica). 01 y 03 salen del criterio de las estadísticas.

## Decisiones según las estadísticas
- **01 Estación Espacial**: tema Espacio, que es el que mejor va en las cuatro medidas (tendencia). Estructura «cadena de datos» (la mejor en «se quedan»). Gancho con cifra de 4 palabras.
- **02 Mulhacén**: tendencia del día; estructura «experimento» (la segunda en «se quedan»). Alcance `nicho` (apuntado para H9).
- **03 Flamencos** — **experimento del lote: gancho de orden** («Mira este pollito gris.»). Es el tipo del vídeo con más «se quedan» del canal (uñas, 80 %), pero solo hay 1 vídeo con él. Lo demás igual que los buenos: universal, 4 palabras, animal grande en el fotograma 0. Se espera > 65 % de «se quedaron viendo».

## Prueba del primer segundo
| # | Objeto que ya se mueve en el fotograma 0 | Primera frase |
|---|---|---|
| 01 | La Estación cruzando delante del Sol que asoma por el borde de la Tierra | «Dieciséis amaneceres al día.» (4) |
| 02 | El montañero que sube a la cima, con las montañas de África apareciendo al fondo | «Desde aquí se ve África.» (5) |
| 03 | El pollito gris que entra dando saltitos en la laguna | «Mira este pollito gris.» (4) |

## Control de calidad
- `motor.guion`: sin ❌ (156/159/159 palabras). ⚠ del 03 («tramo de ≈18 s sin pregunta ni dato»): está justificado, porque en ese tramo salen algas, gambitas, carotenoides y zanahoria, que el detector no cuenta como datos.
- `construir`: «todos los textos se pueden leer» en los tres.
- ffprobe: 1080×1920, 30 fps, h264, AAC 48 kHz; 56,2 / 58,3 / 57,3 s.
- `motor.calidad --mp4`: **sin ❌**. Notas 75 / 64 / 55 (`calidad-0N.md`). Los ⚠ que quedan son de densidad: 4–4,5 elementos por plano frente a 7–8 de la referencia, algunos planos parecidos seguidos y 31 planos en el 03. Se entregan así por tiempo, porque el lote se hizo de madrugada a petición de la persona. Los rótulos con poco contraste del 02 y del 03 se arreglaron (cápsula oscura) y se volvió a renderizar.
- Hojas de fotogramas revisadas. Arreglado antes del render: plano de «kilómetros de altura» sin la Estación, aguja del velocímetro fuera de la esfera, línea de la curva desplazada, Rif poco visible, micro plano «revés» que no se entendía y rótulos que no daban tiempo a leer.
- Portadas: elegidas por revisión visual. En el 03, las candidatas automáticas solo sacaban el microscopio, así que se generaron con fotogramas del pollito.
- Fichas de variables: 3 nuevas; `ficha comprobar` sin problemas.

## No hecho en este turno
- Lectura de YouTube Studio (§1.8) y respuestas a comentarios (§8b): el lote se hizo de madrugada y con prisa; quedan para el turno siguiente.

## Generadores
`generadores/`: `NN-guion.txt`, `ilus_1120t.py` (≈40 SVG nuevos: amanecer orbital ×2, ventanilla, campo de fútbol americano, torre de reloj, ciudad de noche, cumbre nevada, vista al sur con el Rif, casquete de la Tierra, personas, montañero, mapa del Estrecho, corona, piedras nevadas, prismáticos, playa, laguna ×2, flamenco ×4, pollito, gambita, algas, zanahoria, colador, nido, microscopio, gota de leche, plumas; reutiliza por ruta la Estación, la órbita, el casco, la montaña, la cara, el despertador y el velocímetro de lotes anteriores) y `gen_0N.py DIR [locucion.mp3 alineacion.json]`.

## Publicación (2026-11-21 01:37)
Petición en el chat: «súbelos a youtube los 3, uno ahora otro a las 10 de mañana y otro a las 12». Vale como «ok» solo para YouTube. Las horas las eligió la persona y cambian, para este lote, la separación de 1 h de DECISIONS.
- 01 https://youtube.com/shorts/W9NYUO0-CrU: **público**, portada puesta por API.
- 02 https://youtube.com/shorts/LvYkPN5jc6A: **programado** para el 2026-11-21 a las 10:00 (Madrid), portada puesta.
- 03 https://youtube.com/shorts/kHT4ncQZNQ4: **programado** para el 2026-11-21 a las 12:00 (Madrid), portada puesta.
- Sin duplicados: el script mira las últimas subidas del canal.
- Comentario del 01 escrito. **No se pudo fijar**: YouTube pide «una verificación breve y única en YouTube Studio» para fijar comentarios, y esa la tiene que hacer una persona. Avisos en este chat a las 10:05 y a las 12:05 para escribir los comentarios del 02 y del 03.

- 2026-11-21 10:05: aviso del 02. **El Mac de Jorge no está conectado** (dos intentos: «not connected to the bridge»), así que el comentario del 02 queda sin escribir. Se escribe cuando el Mac vuelva: escribiendo en este chat o en el aviso de las 12:05 junto con el del 03.
- 2026-11-21 12:06: aviso del 03. El Mac de Jorge **sigue sin conexión** (dos intentos), así que los comentarios del 02 y del 03 quedan sin escribir. Se escriben cuando alguien escriba en este chat con el Mac encendido.

## Siguiente paso
Comentarios del 02 y del 03 (avisos a las 10:05 y 12:05). Para fijarlos, Nico o Jorge tienen que hacer la verificación de YouTube Studio. TikTok, solo si lo piden.
- Correo de revisión: `1a1fb85d76e09223`.
