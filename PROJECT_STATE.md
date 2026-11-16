# Estado del proyecto

_Última actualización: 2026-11-16 20:30 — Agente 08:00 (Nico)_

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
| ElevenLabs | ✅ voz «Archivo Oculto — Narración (clon)» (`op8soO9fvP07F3mjbJuB`, `eleven_v4`, 0.5/0.75), clave API en el Mac de Jorge («Parece Mentira») y en el de Nico («Parece Mentira - Nico»), prueba OK en los dos |
| Carpeta local de trabajo | ✅ Nico: `/Users/nico/Documents/Parece Mentira` (referencias en `Documents/Codex/Parece Mentira/referencias`) · ✅ Jorge: `/Users/jorgegomez/Documents/Parece Mentira` |
| Web de estadísticas (`estadisticas/`) — YouTube, TikTok e Instagram | 🟢 YouTube y TikTok conectados: se actualiza solo cada mañana (GitHub Actions) y la página «Parece Mentira · Estadísticas» de Claude se republica a las 9:14. Navegación suave y audiencia de YouTube (edad, países, dispositivos, fuentes) con gráficas. Conclusiones automáticas diarias (`estadisticas/datos/aprendizajes.md`) que el agente de lotes usa para decidir. 🟡 Falta Instagram |
| Agente diario | ✅ manual en `AGENTE.md` (desde 2026-11-16: gancho en el fotograma 0, portadas elegidas por el agente sin «ok» §6b, imágenes reales de Openverse en prueba §5b) |
| Openverse (`motor/openverse.py`) | ✅ probado de verdad en el Mac de Jorge (moái CC0 de Commons); desde la nube Wikimedia da 429 → se ejecuta en los Macs. Experimento «plano real» desde el lote 2026-11-17-manana |
| Motor de montaje (v2.3) | ✅ en `main` (karaoke arriba, rótulos, SVG, música, −19 LUFS; v2.3: gancho entero en el fotograma 0) |
| Tarea programada 08:00 (Mac de Nico) | ✅ creada (`trig_01NLm6xzEFknTZ5Z7Uwr1qjU`, carpetas `Documents/Parece Mentira` + `Documents/Codex/Parece Mentira`); primera ejecución 2026-11-16 a las 07:52 |
| Tarea programada 20:00 (Mac de Jorge) | ✅ creada; primera ejecución 2026-11-15 a las 19:52 |

## Contenido
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
