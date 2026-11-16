# Tablero de tareas

Formato en curso: `- [ ] tarea — Nico|Jorge — AAAA-MM-DD HH:MM — nota`
Regla: si una tarea está en curso por la otra persona, no se toca.

## En curso
- [ ] Voz nueva «Narrador PM - Curiosidades v2» con Voice Design (prompt de documental de misterio de Nico; motivo: la v1 suena robótica/plana, nasal y con mal ritmo) — Nico — 2026-11-16 09:58 — falta generarla en ElevenLabs y pasar el voice_id

## Pendiente
- [ ] Estadísticas: conectar Instagram siguiendo `estadisticas/README.md` — Nico — 2026-11-16 17:26 — EN PAUSA: se usa el Facebook personal de Jorge (la cuenta nueva de Nico quedó suspendida en revisión: no crear más cuentas nuevas). Registro en Meta for Developers a medias: falta verificar el móvil (el SMS no llega; probar desde la app de Facebook del móvil → Centro de cuentas → Información de contacto, o por WhatsApp/llamada). Después: crear app, «API setup with Instagram login», añadir @parecementiramedia (debe ser cuenta profesional), generar token → secreto `IG_TOKEN`
- [ ] Estadísticas: tarea programada en la nube que republique cada mañana (≈9:15) la página de Claude «Parece Mentira · Estadísticas» (https://claude.ai/artifact/JMkrEuUZrAmq7yzqVao8ea) con `estadisticas/web/index.html`
- [ ] Estadísticas: rellenar `estadisticas/etiquetas.json` (tema, voz, gancho) de los vídeos publicados para el Laboratorio
- [ ] 2026-11-17 — Nico y Jorge: decidir si se prueba el lote de la mañana en la nube (tarea programada sin depender del Mac: voz por API, montaje y vídeos en el chat; publicar sigue necesitando un Mac encendido en el «ok»). Antes: decidir si la clave de ElevenLabs se guarda en la configuración del entorno en la nube (nunca en el repo) y copiar MP3/MP4 a la carpeta local al publicar. Si sale bien, pasar también el de las 20:00 — propuesto por Jorge 2026-11-16
- [ ] Revisar la prueba «Luna densa» v4 (39 planos de 0,3 a 2,7 s, dinosaurios y fondos nuevos, efectos de sonido; vídeo en el chat de Nico) y decidir si ese ritmo pasa a ser el estándar; si gusta, generar la locución con el texto de `lotes/prueba-luna-densa/guion.txt` (155 palabras, velocidad normal) y volver a montarlo con `gen.py DIR audio.mp3 alineacion.json`
- [ ] Nico y Jorge: tras ver el lote 2026-11-16-tarde (prueba de temas cotidianos), decidir el 2026-11-17 si la mezcla 2 cotidianos + 1 histórico se queda fija, pasa a todo cotidiano o se vuelve a lo de antes; apuntarlo en `DECISIONS.md`
- [ ] Motor: etiqueta con línea hacia el objeto (callout) y planos en sección reutilizables (REFERENCIAS_2 §2 y §4)
- [ ] Mejorar el encuadre automático de `a_v3.py` (algunos detalles cortan personajes): focos a mano por escena
- [ ] Decidir si se activan en TikTok las «revisiones automáticas de contenido» (ajuste de cuenta que ofrece TikTok al subir)
- [ ] Revisar el lote 2026-11-15-tarde **v4** (01 v4c, 02 v4, 03 v4) y decir «ok» o cambios (Mac de Jorge, `lotes/2026-11-15-tarde/v3/`, y chat de Jorge)
- [ ] Elegir música definitiva (hoy el motor genera una base por código, sin licencias)
- [ ] Lote 2026-11-15-tarde v2 con el motor v2 cuando Nico lo termine (subtítulo karaoke arriba, música, 45–60 s / 130–170 palabras, rótulos de dato, gancho más claro, finales con acción) y volver a pedir «ok» en su chat — decidido por Nico 2026-11-15
- [ ] Motor: CRF configurable y SHA del manifiesto igual al archivo entregado
- [ ] Música de fondo: preparar en el motor la mezcla a −19 LUFS con pista de Pixabay o de ElevenLabs y guardar el certificado de licencia por lote
- [ ] Aplicar al motor las mejoras de la revisión del 005 (ver `HANDOFF.md` 2026-11-15 17:05): subtítulo con zona reservada, huella de bota reconocible, módulo lunar reconocible, colisiones Tierra/Sol/barra, final con más acción
- [ ] Desactivar la tarea antigua de Codex de las 08:00 para que no produzca lotes en paralelo
- [ ] Nico o Jorge: contratar ElevenLabs Pro desde la cuenta del proyecto y avisar en `HANDOFF.md` (decidido, ver `DECISIONS.md`)
- [ ] Concretar el importe mensual del presupuesto ampliado y apuntarlo en `DECISIONS.md`
- [ ] Prueba comparativa: mismo vídeo con escenas SVG vs. ilustraciones IA, para decidir si se paga un servicio de imagen
- [ ] Pasar a «Solo yo» el TikTok «Mi cerebro cuando toca callarse» desde el móvil
- [ ] Lista de 20–30 temas iniciales en `lotes/IDEAS.md`
- [ ] Decidir si se limpian los títulos de los vídeos antiguos (ahora privados)

## Hecho
- [x] Estadísticas: TikTok conectado (app sandbox «Parece Mentira Stats», usuario de prueba parece.mentira85, secretos TIKTOK_* + GH_PAT; el token se renueva y se guarda solo); 4 vídeos unidos con YouTube — Nico (en el Mac de Jorge) — 2026-11-16
- [x] «Luna densa» v4: detalles de fondo persistentes (satélites, estrellas fugaces, pterosaurios), 5 dinosaurios detallados (braquiosaurio, tiranosaurio, triceratops, estegosaurio, raptores) y fondos con más tonos (3 paletas de espacio, Luna, eclipse, jungla) — Nico — 2026-11-16
- [x] Estadísticas: YouTube conectado (Google Cloud en producción, cliente «stats», 3 secretos YT_* en GitHub; workflow manual OK: 4 vídeos públicos, 7 suscriptores); `autorizar.py` mejorado (puerto 8765, pegar URL a mano, certificados del sistema, guarda el token en claves.txt) — Nico (en el Mac de Jorge) — 2026-11-16
- [x] Estadísticas de TikTok (Display API) e Instagram (insights de Reels) en la web: pestaña «Redes», ficha con «En las otras redes», unión del mismo vídeo entre redes, vistas por día con foto diaria, renovación automática de tokens — Nico — 2026-11-16
- [x] Web de estadísticas: `estadisticas/` (recoger.py, construir.py, plantilla, autorizar.py, etiquetas) + workflow diario `.github/workflows/estadisticas.yml`; página de Claude publicada con datos de ejemplo — Nico — 2026-11-16
- [x] «Luna densa» v3: ritmo variable (0,3–2,7 s), planos atados a palabras, control de lectura, guion de 155 palabras — Nico — 2026-11-16
- [x] «Luna densa» v2 con micro escenas y detalles secundarios (38 planos) — Nico — 2026-11-16
- [x] Prueba «Luna densa» desde cero: guion de 169 palabras, 29 planos en 46,6 s, 7 ilustraciones nuevas, 110 efectos de sonido; motor con `sfx` y rótulos con decimales — Nico — 2026-11-16
- [x] Nivel de acabado decidido: ninguno, se queda como el v4 (Nico) — 2026-11-16
- [x] Prueba de acabado visual antes/después del 02 v4 (Luna) con `motor/acabado.py`: bloom, LUT documental, papel, partículas en primer plano, parpadeo, grano animado — Nico — 2026-11-16
- [x] Se deja Drive: la revisión se hace en el chat de Claude (AGENTE §7, DECISIONS) — Jorge — 2026-11-16
- [x] Publicar lote 2026-11-15-tarde v4 (01 v4c, 02 v4, 03 v4) en YouTube, Instagram y TikTok (aprobado por Jorge: «súbelos») — Jorge — 2026-11-15 23:42 → hecho 2026-11-16 00:05: 3 redes, enlaces en `lotes/2026-11-15-tarde/estado.md`
- [x] Estilo de ilustración v4 en los 3 vídeos del lote 2026-11-15-tarde (balanza del 01 arreglada) — Jorge — 2026-11-15
- [x] Referencias 2 (9 vídeos) analizadas → `motor/REFERENCIAS_2.md`, DECISIONS y AGENTE; motor v2.1 (cámara con foco, elementos HUD) — Jorge — 2026-11-15
- [x] Lote 2026-11-15-tarde v3 (mismo audio, 17–19 planos por vídeo, etiquetas) — Jorge — 2026-11-15
- [x] Prueba v2 «Huellas en la Luna» publicada: YouTube https://youtube.com/shorts/D_2cV1qhmfA · Instagram https://www.instagram.com/reel/DfxOzoPR6pD/ · TikTok https://www.tiktok.com/@parece.mentira85/video/7708440623040269590 — Nico — 2026-11-15
- [x] Lote 2026-11-15-tarde v2 con motor v2 (52 / 47 / 46 s, karaoke, rótulos, música) — Jorge — 2026-11-15
- [x] Prueba v2 revisada: a Nico y Jorge les encanta; se publica (mejoras más adelante) — Nico — 2026-11-15
- [x] Motor v2 en `main` (subtítulo karaoke, transiciones desenfoque/zoom, rótulos de dato, SVG, música generada + mezcla a −19 LUFS, grano) y vídeo de prueba v2 de 47 s — Nico — 2026-11-15
- [x] Lote 2026-11-15-tarde (3 vídeos, en revisión; MP4 solo en el Mac de Jorge, Drive solo SRT por límite de tamaño del conector) — Agente 20:00 (Jorge) — 2026-11-15
- [x] Presupuesto ampliado y prioridad de gasto aceptados (ElevenLabs Pro → prueba SVG vs. IA → música gratis) → `DECISIONS.md`, `CLAUDE.md` — Nico — 2026-11-15
- [x] Confirmados por Nico los cambios de estilo de `motor/OBJETIVO.md` (subtítulo karaoke arriba, 45–60 s, música) → `DECISIONS.md` — Nico — 2026-11-15
- [x] Análisis de los 13 vídeos objetivo → `motor/OBJETIVO.md` (hojas en `~/Documents/Parece Mentira/referencias-objetivo/`) — Nico — 2026-11-15
- [x] Revisión de la prueba del motor (005 Huellas en la Luna): pasa formato y estilo base; lista de mejoras en `HANDOFF.md` — Nico — 2026-11-15
- [x] Mac de Nico: carpeta `/Users/nico/Documents/Parece Mentira` (claves.txt, lotes/, renders/); clave API «Parece Mentira - Nico» (solo texto a voz + usuario, sin caducidad) pegada por Nico en `claves.txt`; audio de prueba OK — Nico — 2026-11-15
- [x] Mac de Nico: sesiones de ElevenLabs, YouTube Studio, Instagram (@parecementiramedia) y TikTok (parece.mentira85) en el navegador integrado — Nico — 2026-11-15
- [x] Tarea programada 20:00 creada desde el Mac de Jorge (19:52, carpeta `/Users/jorgegomez/Documents/Parece Mentira`); carpeta apuntada en AGENTE.md — Jorge — 2026-11-15
- [x] Motor de montaje 9:16 en `motor/` (13 tipos de elemento, subtítulos, SRT, manifiesto, hoja de fotogramas) y prueba con el 005 — Nico — 2026-11-15
- [x] Clave de API «Parece Mentira» (solo texto a voz + usuario) creada y guardada en el Mac de Jorge; `api.elevenlabs.io` permitido en la red; audio de prueba OK — Jorge — 2026-11-15
- [x] Carpeta local `Documents/Parece Mentira` (claves.txt, lotes/, renders/) en el Mac de Jorge — Jorge — 2026-11-15
- [x] Agente diario (`AGENTE.md`), registro de temas (`lotes/IDEAS.md`) y tarea programada de las 08:00 en el Mac de Nico — Nico — 2026-11-15
- [x] Comprobar la voz nueva en ElevenLabs: «Narrador PM - Curiosidades v1» existe — Jorge — 2026-11-15
- [x] Gmail y Drive conectados a la cuenta del proyecto — Jorge — 2026-11-15
- [x] Drive vaciado y carpeta «Parece Mentira — Revisión» creada — Jorge — 2026-11-15
- [x] Sesiones de YouTube, Instagram y TikTok en el navegador integrado (ordenador de Jorge) — Jorge — 2026-11-15
- [x] Retirar lo publicado en las tres redes — Jorge — 2026-11-15
- [x] Repo `parecementirapero/parece-mentira` creado, app de Claude instalada con acceso solo a este repo — Jorge — 2026-11-15
- [x] Estructura base del repo (este protocolo) — Jorge — 2026-11-15
