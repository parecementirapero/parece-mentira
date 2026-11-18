# Lote 2026-11-18-tarde — estado

**Estado: pendiente de voz** (Mac de Jorge desconectado) — Agente 20:00 (Jorge)

Chat del lote: https://claude.ai/code/session_019BG1dJgL6wqDoQhqXJ6S2H

## Registro
- 19:55–20:05: el Mac de Jorge no contestaba al puente («not connected to the bridge», 4 intentos). Se registró «ordenador no disponible» (commit 37e6cf2).
- 20:07: el Mac vuelve a responder (`device_list_dir` OK) → se reserva y se produce el lote.
- 20:10–20:20: a las 20:09 el puente volvió a caerse. Créditos de ElevenLabs leídos a las 20:08: **27.748** (da para el lote). Mientras el Mac no está: temas verificados, guiones (`motor.guion` ✓ ×3) y montaje con tiempos provisionales en la nube (`generadores/`). Falta la voz (necesita `claves.txt` del Mac).
- 20:20–21:10: Mac sin puente en 12 comprobaciones (cada 5 min). Guiones 02 y 03 recortados a 154–155 palabras (la voz real va más lenta que 2,85 p/s: 155 palabras = 58,7 s en el lote de la mañana) y planos recolocados. Push al móvil a las 20:31.
- 21:10: el lote queda **«pendiente de voz»** (AGENTE §4: sin voz alternativa). Correo `[AVISO]` enviado. Este chat vuelve a comprobar el Mac a las 22:00 y a las 23:00 (aviso programado en la sesión); si responde, sigue con voz → render → calidad → portadas → vídeos aquí.

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
