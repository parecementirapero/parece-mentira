# Lote 2026-11-26-tarde — estado

_Agente 20:00 (Jorge). Arranque 2026-11-26 19:53 (Madrid). Chat: https://claude.ai/code/session_019BG1dJQa777yvYo7vRNCi3_

## Pasos
- [x] Reserva en `TASKS.md` (commit e235753).
- [x] Mac de Jorge responde (19:58). ElevenLabs: quedan **10.285** caracteres (se renuevan el 15-12); este lote gasta ≈2.620 → quedarán ≈7.700 (≈2 lotes).
- [x] Tendencias: no hay `lotes/tendencias/2026-11-26.md` (hoy no hubo turno de mañana). Feeds RSS de Google Trends sin respuesta desde la nube y desde el Mac. Se usa el calendario: hoy es Acción de Gracias en EE. UU. y mañana Black Friday (también en España y Latinoamérica) → vídeo 03.
- [x] 3 temas verificados con dos o más fuentes; guiones pasados por `motor.guion` (sin ❌).
- [x] Ilustración nueva (`generadores/ilus_1126t.py`, sobre los módulos del vídeo largo y `ilus_1125t`): despertador (2 fotogramas), botón de posponer, cama con durmiente (dormido / despierto), mesilla, zzz, dormilón de pie y caras, fondo `bg_dormitorio`; Luna visible y Luna oculta, sonda de 1959, nave de tres tripulantes, módulo de aterrizaje, foto borrosa; policías con gorra y placa, cara de policía, compradora, 3 coches de los sesenta, bolsas de compras, pizarra que cae, monedas de oro, balón, silbato. Hoja de contacto revisada.
- [x] Generadores `gen_01..03.py` (35, 31 y 30 planos atados a palabras), construidos con tiempos provisionales y hojas de fotogramas revisadas (enviadas al chat). Sin ⚠ de lectura salvo uno de 0,06 s en el 03 («GRAN VIERNES», se revisa con la voz real).
- [ ] **Voz — PENDIENTE DE VOZ**: el Mac de Jorge se cayó del puente a las ≈20:10, justo antes de generar la voz, y no volvió (reintentos cada 5 min hasta las 21:15). La clave de ElevenLabs solo está en el Mac. A la vez había otra sesión usando el mismo Mac (largo «El que copiaba», commit 3dc63f1 a las 20:15).
- [ ] Render, `motor.calidad`, portadas, fichas, entrega en el chat, «ok».
- [x] Correo de aviso enviado (id 1a2198087d4a87bc, asunto `[AVISO]`).

## Cómo seguir
En el chat del turno (https://claude.ai/code/session_019BG1dJQa777yvYo7vRNCi3), con el Mac encendido: «sigue». Pasos: copiar `bloques.json` y `voz.py` (de `lotes/largo-cueva-500-dias/generadores/voz.py`) a `Documents/Parece Mentira/lotes/2026-11-26-tarde/`, `python3 voz.py bloques.json N lotes/2026-11-26-tarde --sin-contexto` (N = 1, 2, 3); traer MP3 y alineación a la nube; `python3 gen_0N.py DIR NN-locucion.mp3 NN-alineacion.json`; render; calidad; portadas; fichas; entrega.

## Decisiones según las estadísticas
- 01 posponer la alarma: tema **Cotidiano** ([tendencia] 3,9× más vistas); gancho en segunda persona («Le diste a posponer.»), estructura comparación (lo que se dice frente a lo que dice el estudio sueco).
- 02 cara oculta de la Luna: tema **Espacio** (gana en % visto y en «se quedan»). **Experimento del lote: gancho de negación** («Nunca verás esta cara.»), solo 1 vídeo con él hasta ahora (71,3 % se quedan). Espero > 65 % «se quedaron viendo».
- 03 Black Friday: Histórico desde el presente (mañana es Black Friday), estructura reconstrucción ([tendencia] la que más vistas da en TikTok), gancho de dato.
- Duración: 150–158 palabras (≈53–56 s).

## Prueba del primer segundo
| # | Objeto grande en acción en el fotograma 0 | Primera frase | Alcance |
|---|---|---|---|
| 01 | Despertador enorme que salta y vibra, y una mano que baja a darle | «Le diste a posponer.» (4) | universal |
| 02 | La Luna llena enorme girando despacio con su sombra | «Nunca verás esta cara.» (4) | universal |
| 03 | Un policía que pita en un cruce con coches y bolsas de compras | «Lo bautizó la policía.» (4) | universal |

## Avisos del guion justificados
- 02 y 03: `motor.guion` avisa de un tramo de 13–16 s sin pregunta ni cifra; son tramos de explicación con acción en cada frase (roce que frena la Luna; atasco y policías).

## Datos con cuidado
- 01: el estudio de 2025 usó una app (Sleep Cycle, que ayudó a financiarlo): no se nombra la marca. Lo de los 9 minutos del despertador es folclore: no se usa. El vídeo no dice que posponer sea malo: dice que el sueño entre alarmas es ligero y que el estudio sueco no vio daño.
- 02: «unos veintisiete días» (rotación sideral 27,3 d, no el mes de fases de 29,5). Chang'e 4: 3-1-2019, hora de Pekín.
- 03: primer uso policial en los años cincuenta o sesenta según la fuente → «hace más de sesenta años». «Big Friday» en 1961 (History.com, Xataka).
