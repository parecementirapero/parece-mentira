# Lote 2026-11-18-tarde — estado

**Estado: en revisión** (v1 de los 3 vídeos en el chat) — Agente 20:00 (Jorge)

Chat del lote: https://claude.ai/code/session_019BG1dJgL6wqDoQhqXJ6S2H

## Registro
- 19:55–20:05: el Mac de Jorge no contestaba al puente («not connected to the bridge», 4 intentos). Se registró «ordenador no disponible» (commit 37e6cf2).
- 20:07: el Mac vuelve a responder (`device_list_dir` OK) → se reserva y se produce el lote.
- 20:10–20:20: a las 20:09 el puente volvió a caerse. Créditos de ElevenLabs leídos a las 20:08: **27.748** (da para el lote). Mientras el Mac no está: temas verificados, guiones (`motor.guion` ✓ ×3) y montaje con tiempos provisionales en la nube (`generadores/`). Falta la voz (necesita `claves.txt` del Mac).
- 20:20–21:10: Mac sin puente en 12 comprobaciones (cada 5 min). Guiones 02 y 03 recortados a 154–155 palabras (la voz real va más lenta que 2,85 p/s: 155 palabras = 58,7 s en el lote de la mañana) y planos recolocados. Push al móvil a las 20:31.
- 21:10: el lote queda **«pendiente de voz»** (AGENTE §4: sin voz alternativa). Correo `[AVISO]` enviado (`1a1f04558a8c0298`). Este chat vuelve a comprobar el Mac a las 22:00 y a las 23:00 (aviso programado en la sesión); si responde, sigue con voz → render → calidad → portadas → vídeos aquí.

## Temas (3, verificados con ≥ 2 fuentes; ver `guiones.md`)
1. **GTA 6 tardó trece años** — Histórico · dato · comparación · universal · control. Reservado por Jorge.
2. **Este terrón pesa una montaña** (estrella de neutrones) — Espacio · contraste · comparación · universal · control.
3. **Ahora mides menos** (discos de la columna) — Cotidiano · dato · experimento · universal · **experimento: gancho en segunda persona** (H3).

## Decisiones según las estadísticas
- 01: tema pedido por Jorge con la actualidad del día (sale mañana); estructura «comparación», que es de las que más vistas tiene en YouTube (tendencia). Esperado: búsquedas del día; «se quedaron» ≥ 65 % por un gancho de 5 palabras que nombra GTA 6.
- 02: «Espacio» es el tema que mejor va (tendencia, 6× vistas) + gancho de contraste (el mejor en vistas de TikTok). Control.
- 03: **experimento** — gancho en segunda persona («Ahora mides menos.», 3 palabras) sobre un tema cotidiano; lo demás como los que mejor van (comparación de datos, cifras grandes, bucle). Esperado: «se quedaron» por encima del 54 % de la media de Cotidiano.

## Prueba del primer segundo
- 01: objeto: una hoja de calendario enorme arrancándose y volando (2013 → 2026); frase: «GTA seis tardó trece años.» (5).
- 02: objeto: un terrón brillante cayendo que revienta una báscula; frase: «Este terrón pesa una montaña.» (5).
- 03: objeto: la marca roja de altura bajando por el tallímetro junto a una silueta; frase: «Ahora mides menos.» (3).

## Hecho / falta
- Hecho: guiones (`motor.guion` ✓ ×3), metadatos, generadores con 35–39 planos (`generadores/gen_0N.py`, `ilus_tarde.py`), hojas de fotogramas con tiempos provisionales revisadas.
- Falta (con el Mac): voz por API → `gen_0N.py DIR MP3 JSON` → `motor.render` → `motor.calidad` → portadas → fichas → MP4 al chat.
- 22:00: reintento programado — el Mac de Jorge sigue sin conexión («not connected to the bridge»). Queda el reintento de las 23:00.
- 23:00: segundo reintento — el Mac de Jorge sigue sin conexión. No hay más reintentos automáticos: el lote sigue «pendiente de voz» (retomar en este chat con el Mac encendido, o que Nico/Jorge decidan si el 08:00 hace GTA 6).

## Retomado a petición de la persona en el chat (≈23:20)
- La persona escribió: «créame los vídeos que no has podido crear porque estaba apagado». El Mac de Jorge ya respondía.
- Voz por API desde el Mac (eleven_v4, 0.5/0.75, `with-timestamps`), sin fallos: 01 56,2 s · 02 59,4 s · 03 58,2 s. En el 02 se quitó al montar «¿Y lo más loco?» (`omitir`, empalme a 31,3 s) para no pasar de 60 s.
- Con los tiempos reales: quitados 2 micro planos del 01 (0,11 s y el que dejaba «NOV 2026» sin tiempo de lectura) y acortados 3 rótulos. `construir` sin ⚠ de lectura en los tres.
- Render en la nube. ffprobe: 1080×1920, 30 fps, h264 + AAC 48 kHz. Hojas de fotogramas revisadas; en el 03 se rehízo el primer plano (la marca de altura quedaba bajo el subtítulo y el primer segundo salía quieto).
- `motor.calidad --mp4`: **01 80/100 · 02 77/100 · 03 76/100, ningún ❌**. ⚠ que quedan, justificados: pocos micro planos (< 3) y densidad 4–5 elementos por plano (montaje hecho con prisa por la caída del Mac); en el 03, dos micro planos de la ventana marcados «pobres» (son zooms de un fondo, duran < 1 s); mismo encuadre 3–5 s en el tramo de la columna (01) y del párroco (03).
- Portadas elegidas sin «ok»: 01 «GTA 6 TARDÓ 13 AÑOS» (arriba, t=1,3, hoja 2026) · 02 «PESA UNA MONTAÑA» (abajo, t=9,8, estrella gigante: ninguna candidata enseñaba el terrón) · 03 «AHORA MIDES MENOS» (abajo, t=57,3, silueta y tallímetro).
- Fichas de variables creadas (`ficha comprobar`: 0 problemas). El experimento del 03 (gancho en segunda persona) va en `metadatos.json` → etiquetas; en la ficha, `experimento=no` porque no hay experimento abierto con id.
- MP4, SRT, manifiestos y portadas en el chat y en `Documents/Parece Mentira/lotes/2026-11-18-tarde/` del Mac de Jorge.

| Vídeo | Archivo | Duración | SHA-256 (corto) |
|---|---|---|---|
| 01 | 01-gta6-trece-anos_v1.mp4 | 56,7 s | eb0ff4dd18f3 |
| 02 | 02-terron-estrella-neutrones_v1.mp4 | 58,9 s | dfb4ed47de09 |
| 03 | 03-mides-menos_v1.mp4 | 58,7 s | 6a8c2e51fa19 |

Créditos de ElevenLabs tras el lote: ≈24.200 (se gastaron ≈3.550).
**Siguiente paso**: «ok» (o «ok 1 y 3») en este chat → publicar según AGENTE §8 desde el Mac de Jorge. Ojo: GTA 6 sale el 19-11.

## Publicación del 01 (GTA 6) — «ok 1» en el chat (2026-11-19 ≈00:20)
- La persona: «vamos a subir solo el del gta en youtube y tiktok y mañana los demás». Confirmó «ok 1» y, tras pedir muchos hashtags de GTA (15 en la descripción de YouTube, 22 etiquetas ocultas, 29 hashtags en TikTok), volvió a confirmar «ok 1» con ese texto.
- `publicar/subir_youtube.py` admite ahora `youtube.tags` (etiquetas ocultas) en `metadatos.json`.
- **YouTube**: público https://youtube.com/shorts/_9znalXgInI (`--prueba` antes: sin duplicado). Portada por API: 403 (el canal no tiene miniaturas propias) → falta elegir en Studio el fotograma `portada.t` = 1,3 s.
- **TikTok**: comprobado en TikTok Studio que no estaba. Subido desde el navegador integrado del Mac de Jorge (la persona eligió el archivo; se copió a Descargas para encontrarlo fácil): https://www.tiktok.com/@parece.mentira85/video/7709657865832697110 (a las 00:35 en «Content under review», como siempre al principio). Portada: fotograma 0 (calendario 2013 con el gancho «GTA seis tardó trece años» ya escrito), sin texto añadido.
- Pendiente: portada en YouTube Studio (fotograma 1,3 s) y comentarios («¿Lo vas a jugar mañana? 🎮 Te leo 👇») en YouTube y TikTok.
- 02 y 03: sin publicar, para mañana (pedido de la persona).

## Portada nueva del 01 (GTA 6) — pedida por la persona (2026-11-19 ≈00:50)
- La persona pidió una portada «relacionada con GTA». Hecha a mano con nuestras ilustraciones (ciudad de neón, coche patrulla genérico, mando genérico, hojas 2013/2026) y el texto «GTA 6 · 13 AÑOS · ESPERÁNDOLO»: sin logo, letras ni arte de Rockstar. Archivo: `Documents/Parece Mentira/lotes/2026-11-18-tarde/01-portadas/portada_gta6.jpg` (y en Descargas).
- **YouTube**: la persona verificó el canal → `subir_youtube.py --solo-portada _9znalXgInI` → «portada: puesta» (las miniaturas propias ya funcionan en este canal).
- **TikTok**: la web no deja subir imagen de portada en un vídeo ya publicado (solo elegir fotograma). Con el «sí» de la persona se borró el TikTok 7709657865832697110 (0 vistas; comprobado que el resto de vídeos siguen) y se vuelve a subir con la portada nueva.
