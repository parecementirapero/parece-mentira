# Estado del proyecto

_Última actualización: 2026-11-28 12:25 — Agente 08:00 (Nico) (lote 2026-11-28-manana en revisión)_

## Resumen
Arranque de cero con cuentas compartidas. Nada publicado ahora mismo. Infraestructura casi lista; falta la voz y el montaje automático.

## Conexiones
| Pieza | Estado |
|---|---|
| Gmail (parecementirapero.media@gmail.com) | ✅ conectado |
| Google Drive | ⛔ ya no se usa (2026-11-16): los vídeos se revisan en el chat de Claude del agente |
| GitHub (`parecementirapero/parece-mentira`) | ✅ conectado |
| YouTube / Instagram / TikTok / ElevenLabs — ordenador de Jorge | ✅ sesión iniciada en el navegador integrado |
| YouTube / Instagram / TikTok / ElevenLabs — ordenador de Nico | ✅ sesión iniciada en el navegador integrado (2026-11-15) |
| ElevenLabs | ✅ (quedan ≈6.650 caracteres el 28-11, ≈2 lotes; se renuevan el 15-12) voz «Archivo Oculto — Narración (clon)» (`op8soO9fvP07F3mjbJuB`, `eleven_v4`, 0.5/0.75), clave API en el Mac de Jorge («Parece Mentira») y en el de Nico («Parece Mentira - Nico»), prueba OK en los dos |
| Carpeta local de trabajo | ✅ Nico: `/Users/nico/Documents/Parece Mentira` (referencias en `Documents/Codex/Parece Mentira/referencias`) · ✅ Jorge: `/Users/jorgegomez/Documents/Parece Mentira` |
| Web de estadísticas (`estadisticas/`) — YouTube, TikTok e Instagram | 🟢 YouTube y TikTok conectados: se actualiza solo cada mañana (GitHub Actions) y la página «Parece Mentira · Estadísticas» de Claude se republica a las 9:14. Navegación suave y audiencia de YouTube (edad, países, dispositivos, fuentes) con gráficas. Conclusiones automáticas diarias (`estadisticas/datos/aprendizajes.md`) que el agente de lotes usa para decidir. 🟡 Falta Instagram |
| Estudio de audiencia y rendimiento (`estadisticas/estudio/`) | 🟢 en marcha desde 2026-11-17: cada mañana, tras las estadísticas, se generan `estadisticas/datos/estudio.md` (qué se sabe y con qué nivel: pista / indicio / regla), `autopsias.md` y `mediciones.json` (24 h, 48 h, 7 d, 28 d); los lunes, informe semanal. 10 vídeos con ficha (todas retrospectivas). 🟡 Hoy solo 3 vídeos tienen lectura con 24 h o más: **nada pasa de «pista»**. 🟡 Audiencia por vídeo y comentarios: código listo, sin probar contra la API real. Pendiente de Nico y Jorge: público objetivo, primer experimento, confirmar la ficha en AGENTE |
| Publicación por API de Instagram y TikTok (`publicar/`) | 🟡 código listo y probado en simulación (2026-11-17), **sin activar**: falta la puesta en marcha de `publicar/README.md`. Instagram publicará el Reel entero; TikTok solo puede dejar un borrador en la bandeja (se termina en el móvil) y depende de una prueba real. Hasta entonces, navegador |
| Agente diario | ✅ manual en `AGENTE.md` (desde 2026-11-16: gancho en el fotograma 0, portadas elegidas por el agente sin «ok» §6b, imágenes reales de Openverse en prueba §5b) |
| Openverse (`motor/openverse.py`) | 🟡 en el Mac de Nico falla la descarga: `thumb.wikimedia.org` da 403 (2026-11-17). Antes: ✅ probado de verdad en el Mac de Jorge (moái CC0 de Commons); desde la nube Wikimedia da 429 → se ejecuta en los Macs. Experimento «plano real» desde el lote 2026-11-17-manana |
| Motor de montaje (v2.3) | ✅ en `main` (karaoke arriba, rótulos, SVG, música, −19 LUFS; v2.3: gancho entero en el fotograma 0). **Desde 2026-11-24 también en horizontal 16:9** con `MOTOR_FORMATO=16:9` (subtítulo abajo, zonas seguras, hoja y calidad) |
| Tarea programada 08:00 (Mac de Nico) | ✅ creada (`trig_01NLm6xzEFknTZ5Z7Uwr1qjU`, carpetas `Documents/Parece Mentira` + `Documents/Codex/Parece Mentira`); primera ejecución 2026-11-16 a las 07:52 |
| Tarea programada 20:00 (Mac de Jorge) | ✅ creada; primera ejecución 2026-11-15 a las 19:52 |

## Contenido
- En revisión: lote **2026-11-28-manana** v1 (en enero estamos más cerca del Sol, la nevada de Ciudad de México de 1967, el vidrio no se escurre; 55–58 s; los tres salen de tendencias; experimento: gancho POV en segunda persona en el 02). Vídeos en el chat https://claude.ai/code/session_019BG1dKjnnRjJqNw5DCuPje; la copia al Mac de Nico queda pendiente (se desconectó). El 03 lleva dos frases quitadas de la toma: oír los empalmes. ElevenLabs: quedan ≈6.650 caracteres.
- En revisión: lote **2026-11-27-tarde** v1 (anochece dos veces en el Burj Khalifa, la capa de ozono mide tres milímetros, la piel de gallina; 53–59 s; 01 y 02 salen de tendencias; experimento: gancho de paradoja en el 01). Vídeos en el chat https://claude.ai/code/session_019BG1dK7GpyrYsYXE518JkF; la copia al Mac de Jorge queda pendiente (se desconectó). ElevenLabs: quedan ≈7.700 caracteres.
- Pendiente de voz: lote **2026-11-26-tarde** (posponer la alarma, la cara oculta de la Luna, el Black Friday lo bautizó la policía; experimento: gancho de negación en el 02). Guiones, arte y generadores en `lotes/2026-11-26-tarde/`. El Mac de Jorge no respondió desde las 20:10. Se retoma con «sigue» en https://claude.ai/code/session_019BG1dJQa777yvYo7vRNCi3. ElevenLabs: quedan 10.285 caracteres (≈7.700 después de este lote).
- **Publicado** (26-11, YouTube y TikTok: 01 a las 13:55, 02 a las 16:00, 03 a las 18:00): lote **2026-11-25-tarde** v1 (vibración fantasma, medallas olímpicas por arte, la Vía Láctea que casi nadie ve; 52–60 s), **primer lote con el estilo de dibujo del vídeo largo** (personajes y escenarios de `lotes/largo-cueva-500-dias`, a petición de Jorge). Hecho el 26-11 porque la tarea de las 20:00 está en pausa (Mac ausente: hay que reactivarla desde el Mac de Jorge). Vídeos en el chat https://claude.ai/code/session_019BG1dJB3X8kpbAbFL1YoGS y en `Documents/Parece Mentira/lotes/2026-11-25-tarde/` (Mac de Jorge). ElevenLabs: quedan 12.233 caracteres.
- En revisión: lote **2026-11-25-manana** v1 (el Hubble nació miope, por qué se arrugan los dedos en el agua, el olivo que conoció a Roma; 55–57 s; dos salen de tendencias; experimento: gancho en segunda persona en el 02). Vídeos en el chat https://claude.ai/code/session_019BG1dKEg4xbEPyKDNcseyw y en `Documents/Parece Mentira/lotes/2026-11-25-manana/` (Mac de Nico). El 01 y el 03 llevan frases quitadas de la toma para bajar de 60 s: oír los empalmes. ElevenLabs: quedan 12.911 caracteres.
- Lote **2026-11-24-tarde** publicado y programado (YouTube y TikTok: 01 ya, 02 a las 10:00 y 03 a las 12:00 del 25-11).
- En revisión: **vídeo largo «¿Qué pasaría si te encerraras 500 días en una cueva sin reloj?»** (`lotes/largo-cueva-500-dias/`, encargo de Nico). 8:31 en horizontal 16:9 para YouTube, con 294 planos, más 5 partes verticales para TikTok (1:47, 1:49, 1:41, 1:21 y 1:53) sacadas del mismo audio. Vídeos en el chat https://claude.ai/code/session_019BG1dFtXHqVXWrKbh8QXsf y en `Documents/Parece Mentira/lotes/largo-cueva-500-dias/` (Mac de Jorge). **Publicado** el 24-11: YouTube https://youtu.be/cA3b0FdYA8A; TikTok, parte 1 a las 11:33 y el resto a las 13:30, 15:30, 17:30 y 19:30. ElevenLabs: quedan 15.648 caracteres.
- Lote **2026-11-23-tarde** publicado y programado (YouTube y TikTok: 01 ya, 02 a las 10:00, 03 a las 12:00 del 24-11). ElevenLabs: quedan 17.947 caracteres (se renueva el 15-12).
- Antes en revisión (ya programado): lote **2026-11-22-tarde** v1 (temas de Jorge: el punto ciego, el cerebro enamorado y un test de atención en versión propia de un formato de otra cuenta). Vídeos en el chat https://claude.ai/code/session_019BG1dFtXHqVXWrKbh8QXsf y en `Documents/Parece Mentira/lotes/2026-11-22-tarde/` (Mac de Jorge). ElevenLabs: quedan 18.867 caracteres.
- Sin hacer: lote **2026-11-22-manana** — ordenador no disponible (la ejecución de las 10:18 no tuvo el Mac de Nico). Tendencias del día en `lotes/tendencias/2026-11-22.md` (baloncesto, luz a precio negativo, fruta en la frontera: sin usar). Se retoma en https://claude.ai/code/session_019BG1dJVmPqrtbuKRGs1cfJ.
- En YouTube (ok de la persona, solo YouTube): lote **2026-11-20-tarde** v1 — W9NYUO0-CrU público, LvYkPN5jc6A a las 10:00 y kHT4ncQZNQ4 a las 12:00 del 21-11 (16 amaneceres en la Estación Espacial, desde el Mulhacén se ve África, los flamencos nacen grises; 56–58 s; experimento: gancho de orden en el 03). Vídeos en el chat https://claude.ai/code/session_019BG1dFtXHqVXWrKbh8QXsf y en `Documents/Parece Mentira/lotes/2026-11-20-tarde/` (Mac de Jorge). ElevenLabs: quedan 20.837 caracteres.
- En revisión: lote **2026-11-20-manana** v1 (los hipopótamos no saben nadar, un F1 podría ir por el techo, el primer coche en pasar de 100 km/h era eléctrico; 56–58 s; los tres salen de las tendencias del día; experimento: gancho de contraste de época en el 03). Vídeos en el chat https://claude.ai/code/session_019BG1dLEec78Rq3eZBDrkLR y en `Documents/Parece Mentira/lotes/2026-11-20-manana/` (Mac de Nico). ElevenLabs: quedan ≈21.400 caracteres.
- Tendencias del día: `lotes/tendencias/AAAA-MM-DD.md` (desde el 2026-11-20; la escribe el turno de mañana y la lee el de tarde). Regla en `DECISIONS.md` y `AGENTE.md` §2.
- Pendiente de voz: lote **2026-11-19-tarde** (atardecer azul en Marte, 300 huesos al nacer, las gotas no son lágrimas; experimento: gancho POV en el 01). Guiones, metadatos y montajes con tiempos provisionales en `lotes/2026-11-19-tarde/`; falta voz → render → «ok» en https://claude.ai/code/session_019BG1dKjUgmMjL827TDKKHq. ElevenLabs: quedan 24.584 caracteres.
- En revisión: lote **2026-11-18-tarde** v1 (GTA 6 tardó 13 años, terrón de estrella de neutrones, ahora mides menos; 57–59 s; experimento: gancho en segunda persona en el 03). Vídeos en el chat https://claude.ai/code/session_019BG1dJgL6wqDoQhqXJ6S2H y en `Documents/Parece Mentira/lotes/2026-11-18-tarde/` (Mac de Jorge). ElevenLabs: quedan ≈24.200 caracteres.
- En revisión: lote **2026-11-18-manana** v1 (día de 18 horas, la Gran Muralla no se ve desde el espacio, tu perro copia tus bostezos; 58–59 s; experimento: gancho de negación en el 02). Vídeos en el chat https://claude.ai/code/session_019BG1dJLtMKt7d9zxuM93s6 y en `Documents/Parece Mentira/lotes/2026-11-18-manana/` (Mac de Nico). ElevenLabs: quedan 27.748 caracteres.
- En revisión: lote **2026-11-17-tarde** v1 (rayo más caliente que el Sol, el Sol que ves ya es pasado, cebolla; 55–57 s; experimento: gancho de orden en el 03). Vídeos en el chat https://claude.ai/code/session_019BG1dHf6SfJ6MbfA5kmnCP y en `Documents/Parece Mentira/lotes/2026-11-17-tarde/` (Mac de Jorge). ElevenLabs: quedan 28.812 caracteres.
- Publicado: lote **2026-11-17-manana** v1 (plátano radiactivo, Saturno flotaría, huella de koala; 56–59 s; primer lote automático con método denso y `motor.calidad`). Vídeos en el chat https://claude.ai/code/session_019BG1dJfghaKYErZsy5CyPu y en `Documents/Parece Mentira/lotes/2026-11-17-manana/` (Mac de Nico). ElevenLabs: quedan 29.828 caracteres.
- En revisión: lote 2026-11-16-manana v1 (planetas, pulpo, vikingos; 53–54 s, voz clon nueva). Vídeos en el chat https://claude.ai/code/session_019BG1dHPaoMtT9aEtopJ3JF y en `Documents/Parece Mentira/lotes/2026-11-16-manana/`, en el Mac de Nico.
- Publicado: prueba v2 «Huellas en la Luna» (2026-11-15) en YouTube, Instagram y TikTok — ver `lotes/prueba-v2-huellas-luna/estado.md`.
- Publicado: lote 2026-11-15-tarde v4 (Zanzíbar, Luna, moáis) el 2026-11-16 en las 3 redes — ver `lotes/2026-11-15-tarde/estado.md`. Vídeos con «ok» en `~/Documents/Parece Mentira/PARA PUBLICAR/` (Mac de Jorge).
- Lotes producidos en el sistema nuevo: `2026-11-15-tarde` (publicado) y **`2026-11-16-tarde`** (prueba de temas cotidianos: nudillos, puertas, Apolo 11; v2 método denso **publicado** en las 3 redes el 2026-11-16; YouTube 2 y 3 programados a las 23:15 y 00:15). Primer lote con la voz clonada y `eleven_v4`.
- Vídeos antiguos (001–007 + piloto Venus): retirados de las redes; ver `DECISIONS.md`.

## Presupuesto
Ampliado el 2026-11-15 (importe por concretar). Gasto decidido: ElevenLabs Pro (pendiente de contratar). Ver `DECISIONS.md`.

- Prueba «Luna densa» (2026-11-16, Nico): 29 planos + efectos de sonido, sin voz todavía — `lotes/prueba-luna-densa/`.

- Método denso (2026-11-16): estándar de los lotes desde el 2026-11-17-manana — `motor/DENSO.md`.

- Publicado (2026-11-16): «La Luna se nos va…» (método denso) en las 3 redes — `lotes/prueba-luna-densa/estado.md`.

- Calidad (2026-11-17): control automático `python3 -m motor.calidad` obligatorio antes de entregar (AGENTE §6) y guía `motor/GUIA_CALIDAD.md`. Luna densa v5 (ejemplo con las mejoras, **no publicada**) en `lotes/prueba-luna-densa/gen.py`.

- Aprendizaje (2026-11-17): `motor/APRENDIZAJE.md` es el cuaderno de datos, referentes y experimentos; se lee al arrancar cada lote. Luna densa v6 (karaoke y «palabra») de muestra, **no publicada**.

## Siguiente paso
Ver los lotes 2026-11-16-manana (chat https://claude.ai/code/session_019BG1dHPaoMtT9aEtopJ3JF) y 2026-11-16-tarde en sus chats y escribir «ok» (o cambios). El 2026-11-17 decidir si la mezcla de temas cotidianos se queda (TASKS).

_Anterior:_ Los dos Macs ya tienen clave de ElevenLabs y sesiones. Revisar el primer lote de la tarde (Jorge) y la prueba del motor (Nico); primera ejecución de la mañana el 2026-11-16 a las 07:52.
