# Traspasos

Lo más reciente arriba. Cada entrada: fecha, quién, rama, commit, qué se hizo, pruebas, pendientes, siguiente paso.

---

## 2026-11-16 00:05 — Jorge — rama `main` — ordenador de Jorge
**Hecho**: lote 2026-11-15-tarde v4 publicado en YouTube Shorts, Instagram Reels y TikTok desde el navegador integrado (Jorge elige cada archivo en el selector). Enlaces en `lotes/2026-11-15-tarde/estado.md`. Vídeos aprobados copiados a `~/Documents/Parece Mentira/PARA PUBLICAR/`.
**Trucos**: Instagram → icono de recorte → «Original»; texto con clic en el campo y escribir (no execCommand). TikTok → borrar el título por defecto seleccionando con un Range en JS + Backspace; cmd+a no funciona.
**Pendientes**: TikTok de los moáis en revisión; reel antiguo DfxOzoPR6pD en Instagram (¿borrar?); TikTok «Mi cerebro» aún público (poner «Solo yo» desde el móvil); Google Drive para ordenador.
**Siguiente paso**: próximo lote automático 07:52 (Nico).

## 2026-11-15 23:40 — Jorge — rama `main` — ordenador de Jorge
**Hecho**: a Jorge le gusta el estilo v4. Balanza del 01 rehecha (v4c). 02 y 03 hechos en el mismo estilo con ilustraciones nuevas (`ilus_02.py`, `ilus_03.py`) y montaje (`comun_v4.py`, `gen_02.py`, `gen_03.py`). Mismo audio. DECISIONS y AGENTE: el estilo v4 pasa a ser obligatorio.
**Pruebas**: hojas de fotogramas de los 3; ffprobe 1080×1920; ebur128 −19,3…−19,6 LUFS.
**Siguiente paso**: «ok» de Nico/Jorge y publicar; Google Drive para ordenador.

## 2026-11-15 19:55 — Agente 20:00 (Jorge) — rama `main` — ordenador de Jorge
**Hecho**: ejecución programada de las 19:52. El lote `2026-11-15-tarde` ya existe (`estado.md`; primera ejecución a las 16:52 y versiones v2, v3 y v4 del vídeo 01 hechas a mano por Jorge). Arranque idempotente (AGENTE.md §1.3): **no se crea otro lote ni se duplica nada**. El último paso registrado (v4 del vídeo 01) espera el visto bueno de una persona antes de rehacer 02 y 03, así que no hay trabajo automático que retomar.
**Pruebas**: carpeta local del Mac de Jorge responde (`lotes/2026-11-15-tarde/` con v1, v2, v3 y v4).
**No hecho a propósito**: sin ideas ni voz nuevas (0 créditos de ElevenLabs), sin correo (el aviso de este turno ya salió, id `1a1dff810fee0c30`; regla de un correo por turno), sin publicar.
**Siguiente paso**: Nico/Jorge deciden sobre la v4 del 01 (`lotes/2026-11-15-tarde/v4/` del Mac de Jorge): si gusta, mismo método para 02 y 03 y pedir «ok». Próximo lote automático: mañana 07:52 (Nico) y 19:52 (Jorge).

## 2026-11-15 18:45 — Jorge — rama `main` — ordenador de Jorge
**Hecho**: Jorge ve la v3 «estática y de dibujo infantil». Prueba v4 del vídeo 01 con ilustración SVG detallada hecha a mano por código (`generadores/v4/`), 23 planos y movimiento continuo; sin coste.
**Pruebas**: hojas de fotogramas (corregidos humo en bolas y balanza invertida/descolgada); ffprobe y ebur128.
**Siguiente paso**: si gusta, mismo método para 02 y 03 y convertir `ilus.py` en una biblioteca de piezas reutilizables para los agentes.

## 2026-11-15 18:20 — Jorge — rama `main` — ordenador de Jorge
**Hecho**: análisis de 9 vídeos de referencia (20 archivos de WhatsApp) → `motor/REFERENCIAS_2.md`, regla nueva en `DECISIONS.md` y aviso en `AGENTE.md`. Motor v2.1: `camara.foco` y elementos `"hud": true` (README). `generadores/a_v3.py` y lote 2026-11-15-tarde v3 con el audio v2 (sin gastar créditos).
**Pruebas**: hojas de fotogramas cada 1,5 s de los 3 vídeos; ffprobe (1080×1920, h264/AAC, 52,3/46,7/46,3 s); ebur128 −19,3…−19,6 LUFS.
**Pendientes**: callouts con línea y planos en sección en el motor; focos manuales donde el detalle corta personajes; «ok» de Nico/Jorge; Google Drive para ordenador.
**Siguiente paso**: revisar la v3.

## 2026-11-15 17:50 — Nico — rama `main` — ordenador de Nico
**Hecho**: Nico y Jorge aprueban la prueba v2 («súbelo»). Publicada en público en las tres redes desde el navegador integrado del Mac de Nico, con los textos de `lotes/prueba-v2-huellas-luna/metadatos.json`:
- YouTube: https://youtube.com/shorts/D_2cV1qhmfA (no para niños; derechos de autor: sin problemas)
- Instagram: https://www.instagram.com/reel/DfxOzoPR6pD/ (formato «Original» 9:16)
- TikTok: https://www.tiktok.com/@parece.mentira85/video/7708440623040269590 (pasó la revisión, «Todo el mundo»)
Excepción de tema repetido registrada en `DECISIONS.md` y en `lotes/IDEAS.md`.
**Aprendido para el agente**: el selector de archivos del navegador integrado no lo puede manejar Claude (la app de Claude no se puede controlar); la persona elige el archivo y Claude hace el resto. Instagram recorta a 1:1 por defecto. Las sugerencias de hashtags de Instagram se comen el clic de «Compartir»: escribir un espacio al final antes de compartir.
**Pendientes**: decidir las revisiones automáticas de TikTok; música definitiva; prueba SVG vs. IA.
**Siguiente paso**: lote de la tarde v2 (Jorge, en curso) y primer lote automático de mañana a las 07:52.

## 2026-11-15 17:45 — Jorge — rama `main` — ordenador de Jorge
**Hecho**: v2 del lote 2026-11-15-tarde con el motor v2. Guiones ampliados (155/152/142 palabras, `textos_v2.json` y `guiones.md`), voz nueva por API desde el Mac de Jorge (52,3 / 46,7 / 46,3 s), `generadores/a_v2.py` (paso v1→v2 reutilizable), render en el workspace y copia a `lotes/2026-11-15-tarde/v2/` del Mac de Jorge.
**Pruebas**: ffprobe, ebur128 (−19,3…−19,6 LUFS), hojas de fotogramas revisadas.
**Ojo**: karaoke a y=300 (≈16 %) en este lote para no tapar escenarios altos; el conector de Drive sigue sin admitir los MP4.
**Siguiente paso**: «ok» o cambios de Nico y Jorge; Google Drive para ordenador.

## 2026-11-15 17:30 — Nico — rama `motor-v2` fusionada en `main` — ordenador de Nico
**Hecho**
- Motor v2 (`motor/README.md` → «Novedades v2»): subtítulo karaoke arriba con palabras clave en cápsula (modo por defecto; `"modo": "clasico"` para el de la v1), transiciones `desenfoque` y `zoom`, elemento `rotulo` (cifra + unidad, puede contar), `imagen` con SVG, música generada por código (`motor/musica.py`) con sidechain y normalización a −19 LUFS, grano fijo y tope de 8 Mb/s.
- Prueba `motor/ejemplos/v2-huellas-luna/` (guion 155 palabras, 8 escenas, gancho en el fotograma 0, final en bucle, 8 SVG). Voz nueva con `/with-timestamps` desde el Mac de Nico (~830 caracteres). Vídeo en `~/Documents/Parece Mentira/renders/prueba/v2/` (no en git).
- `005-huellas-luna` fijado en `"modo": "clasico"` para que siga saliendo como la v1.

**Pruebas**: `ffprobe` → 1080×1920, 30 fps, h264, AAC 48 kHz estéreo, 47,2 s, 27 MB; `ebur128` → −19,5 LUFS; 0 % de instantes estáticos; hojas de fotogramas revisadas (corregidos: bota que no tapaba su huella, rótulos sobre la Tierra, «2011» tapado por la sonda, bota asomando en el bucle, peso de 212 MB por el grano animado). El 005 se sigue renderizando sin errores.
**Fuentes del guion**: The Planetary Society y ASU/phys.org (LRO a 21 km, 2011); erosión por micrometeoritos (Space.com, cita de Mark Robinson, ASU).
**Pendientes**: que Nico vea la prueba; música definitiva; prueba SVG vs. IA.
**Siguiente paso**: el chat del lote 2026-11-15-tarde ya puede rehacer los 3 vídeos con el motor v2 (estaba esperando a que `motor-v2` entrara en `main`).

## 2026-11-15 17:20 — Nico (en el chat del lote 2026-11-15-tarde) — rama `main`
**Hecho**: Nico revisa el lote de la tarde: está en el estilo antiguo (subtítulo abajo, sin música, 39–45 s). Decide **esperar al motor v2** y sacar la v2 de los 3 vídeos con el estilo nuevo; la v1 no se publica. Propuestas de mejora apuntadas en `TASKS.md` (gancho más claro, rótulos de dato, personajes más reconocibles, finales con acción, Drive para escritorio, CRF configurable).
**Siguiente paso**: cuando `motor-v2` esté en `main`, rehacer el lote con guiones de 130–170 palabras (voz nueva) y pedir «ok» en https://claude.ai/code/session_019BG1dGzAeKkhhB4LNjrkX3

## 2026-11-15 17:10 — Agente 20:00 (Jorge) — rama `main`
**Hecho**: lote `2026-11-15-tarde` (primera ejecución de la tarea de la tarde; arrancó a las 16:52 hora de Madrid). Tres temas verificados con dos fuentes cada uno: guerra anglo-zanzibariana de 38 minutos (historia, reconstrucción con reloj), la Luna se aleja 3,8 cm al año (ciencia, comparación con las uñas), moáis con cuerpo enterrado (misterio por pistas). Guiones de 125–135 palabras con cifras en letra (`lotes/2026-11-15-tarde/guiones.md`), metadatos por red (`metadatos.json`), generadores de `episodio.json` en `lotes/2026-11-15-tarde/generadores/` (nuevo helper de reloj con agujas que giran sobre el centro en `comun.py`). Voz por API desde el Mac de Jorge (`with-timestamps`, `eleven_multilingual_v2`), ~2.150 caracteres; quedan ~36.000 de 40.000. Render con `motor/` y QC. Correo único enviado (id `1a1dff810fee0c30`).
**Pruebas**: ffprobe de los 3 MP4 (1080×1920, 30 fps, h264 yuv420p, AAC 48 kHz estéreo, 45,2 / 41,5 / 39,0 s); hojas de fotogramas del motor y del MP4 revisadas.
**Bloqueo**: Drive. El conector rechaza archivos de más de 10 MB y, además, cada llamada tiene un tope de ≈3 MB de archivo; ni recodificando a CRF 24 (4–6 MB) entran. En Drive solo están los SRT. Los MP4 están en `Documents/Parece Mentira/lotes/2026-11-15-tarde` del Mac de Jorge. Además, la carpeta `/mnt/user-data/outputs` del workspace modifica los MP4 al copiarlos (añade ≈5,9 KB de metadatos): el SHA del archivo final no coincide con el del manifiesto; en `estado.md` va el SHA del archivo del Mac.
**Pendientes**: decidir la vía de subida a Drive (ver `TASKS.md`); `motor/`: valorar un CRF configurable; esperar «ok» en el chat del lote.
**Siguiente paso**: revisar los vídeos y responder «ok» (o «ok 1 y 3») o cambios en https://claude.ai/code/session_019BG1dGzAeKkhhB4LNjrkX3

## 2026-11-15 17:10 — Nico — rama `main` — ordenador de Nico
**Hecho**: Nico y Jorge aceptan ampliar el presupuesto. Registrado en `DECISIONS.md` («Presupuesto y gastos») y en `CLAUDE.md`: 1) ElevenLabs Pro; 2) ilustraciones SVG gratis primero y prueba comparativa con IA antes de pagar; 3) música gratis (Pixabay con certificado o ElevenLabs).
**Pendientes**: importe mensual exacto; contratar Pro (lo hace una persona, no Claude); prueba SVG vs. IA.
**Siguiente paso**: aplicar `motor/OBJETIVO.md` al motor.

## 2026-11-15 17:10 — Nico — rama `main` — ordenador de Nico
**Hecho**: Nico confirma los cambios de `motor/OBJETIVO.md` → `DECISIONS.md` (subtítulo karaoke arriba con palabra clave en cápsula, rótulos de dato permitidos, 45–60 s, música de fondo con licencia) y `AGENTE.md` (130–170 palabras). Antigua regla del subtítulo abajo tachada.
**Ojo créditos**: 6 vídeos/día × ~900 caracteres ≈ 160k/mes → no cabe en Creator (121k); ver tarea «Decidir plan de ElevenLabs».
**Siguiente paso**: aplicar `OBJETIVO.md` al motor; elegir fuente de música; Jorge debe saber que el estilo cambia antes del lote de las 19:52.

## 2026-11-15 17:15 — Nico — rama `main` — ordenador de Nico
**Hecho**: análisis de 13 vídeos objetivo (descargas de TikTok que pasó Nico) → `motor/OBJETIVO.md`: ficha técnica medida (duración, cortes, movimiento, LUFS), rasgos de estilo comunes y lista priorizada de cambios para el motor. Hojas de fotogramas en `~/Documents/Parece Mentira/referencias-objetivo/` (no en git).
**Pruebas**: `ffprobe`, detección de cortes (`scene>0.25`), `ebur128`, `silencedetect`, diferencia entre fotogramas; revisión visual de las 13 hojas y del gancho (0–3 s) de 4 vídeos.
**Ojo**: varios cambios contradicen `DECISIONS.md`/`AGENTE.md` (subtítulo arriba tipo karaoke, 45–60 s, música). No se ha cambiado nada: falta confirmación.
**Siguiente paso**: confirmar esos cambios y, después, aplicarlos al motor junto con las mejoras de la revisión del 005.

## 2026-11-15 17:05 — Nico — rama `main` — ordenador de Nico
**Hecho**: revisión de `renders/prueba/prueba-005-huellas-luna_v1.mp4` (fotograma cada 1 s + detalle a media resolución; hojas en `renders/prueba/hoja1s_*.jpg` y `revision_detalle.jpg`).
**Pruebas**: `ffprobe` → 1080×1920, 30 fps, h264, AAC 48 kHz estéreo, 32,9 s; sin congelados (`freezedetect`).
**Pasa**: pantalla completa, sin título, sin Nova, solo subtítulo blanco abajo, siempre hay algo moviéndose, la historia se entiende sin sonido (playa → Luna → sonda → rastro).
**A mejorar (por prioridad)**
1. **El subtítulo choca con los elementos**: la lupa tapa «desde tan lejos no distingue cada bota» y la huella de bota queda pegada a «No hay viento ni lluvia…». Hace falta una franja reservada para el subtítulo (≈70–82 % de alto) donde no entre ningún elemento, o que los elementos la esquiven.
2. **La huella de bota no se reconoce**: parecen dos pastillas con rayas. Necesita la silueta de una suela (puntera + tacón unidos) con las rayas por dentro, hundida en el polvo (sombra interior), no en relieve.
3. **El módulo lunar visto desde arriba parece una tuerca o una señal**. Mejor una vista lateral simplificada (cuerpo dorado + patas) o una sombra reconocible.
4. **Colisiones**: el Sol pasa por encima de la Tierra y la barra amarilla (¿50 años?) corta la Tierra y no tiene etiqueta, así que no se entiende qué mide. O se etiqueta («1969 → hoy») o se quita.
5. **Huella de la playa**: en el segundo 0 es enorme y en el 1 encoge de golpe; que aparezca pisándose (hundimiento + sombra) a su tamaño final.
6. **El final (≈29–33 s) es casi estático y repite el plano de la escena 2**: falta un cierre con acción (zoom lento a la huella iluminada, la Tierra que sale, un destello…) que deje el remate «todavía se puede ver».
7. **Poco 2.5D**: los fondos son planos. Añadir capas con paralaje (cráteres en primer plano, horizonte, estrellas) y sombras proyectadas por el Sol.
8. Menores: el icono de lluvia tachado apenas se ve; la cifra del subtítulo sale como «50» (la locución sí debe ir en letra; en el subtítulo vale el número, pero hay que decidirlo).
**Siguiente paso**: aplicar 1–4 antes del primer lote (07:52); 5–8 cuando se pueda.

## 2026-11-15 17:00 — Nico — rama `main` — ordenador de Nico (`macbook-air-de-nicolas-local`)
**Hecho**
- Carpeta `/Users/nico/Documents/Parece Mentira` con `lotes/`, `renders/` y `claves.txt` (`ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID=EuJOG4WNDCMcwTFrXKUc`). La tarea de las 08:00 (`trig_01NLm6xzEFknTZ5Z7Uwr1qjU`) ya apunta a esta carpeta; `AGENTE.md` y `PROJECT_STATE.md` actualizados (antes ponían `Documents/Codex/...`, que queda solo para `referencias/`).
- ElevenLabs (sesión ya iniciada con la cuenta del proyecto en el navegador integrado): clave API **«Parece Mentira - Nico»**, sin caducidad, restringida a «De texto a voz» y «Usuario». La copió y pegó Nico en `claves.txt`; Claude no la ha visto ni escrito.
- Navegador integrado del Mac de Nico: permiso «siempre» para instagram.com y tiktok.com. Sesiones: YouTube Studio (canal «Parece Mentira», ya estaba), Instagram **@parecementiramedia** y TikTok Studio **parece.mentira85** (iniciadas por Nico). No se ha publicado ni cambiado nada.

**Pruebas**: `claves.txt` → la clave empieza por `sk_` (comprobado sin mostrarla). TTS con voice_id `EuJOG4WNDCMcwTFrXKUc`, modelo `eleven_multilingual_v2` → HTTP 200, `renders/prueba/prueba-nico.mp3`, MP3 128 kbps 44,1 kHz, 4,0 s. Lectura de las tres redes: sesión dentro en las tres.

**Pendientes**: revisar la prueba del motor; plan de créditos de ElevenLabs (ahora hay dos claves sobre la misma cuenta y los mismos créditos); TikTok «Mi cerebro cuando toca callarse» sigue visible en TikTok Studio (pasarlo a «Solo yo» desde el móvil).

**Siguiente paso**: revisar el lote de la tarde de Jorge; primera ejecución de la mañana el 2026-11-16 a las 07:52 en este Mac (debe estar encendido con la app de Claude abierta).

---

## 2026-11-15 16:55 — Nico — rama `main`
**Hecho**: alineado con `DECISIONS.md` (carpeta `~/Documents/Parece Mentira` + `claves.txt`). Tarea de las 08:00 rehecha con esa carpeta y con la de referencias (`trig_01NLm6xzEFknTZ5Z7Uwr1qjU`); la anterior, ligada a `Documents/Codex/Parece Mentira`, está borrada. `AGENTE.md`: voz por `/with-timestamps` (MP3 + alineación para los subtítulos). Prueba del motor movida a `~/Documents/Parece Mentira/renders/prueba/`.
**Pruebas**: la carpeta existe en el Mac de Nico con `claves.txt` y `renders/prueba/prueba-nico.mp3`; tarea activa con las 2 carpetas.
**Siguiente paso**: lote de las 19:52 en el Mac de Jorge (primera ejecución real) y de las 07:52 en el de Nico.

---

## 2026-11-15 16:52 — Jorge — rama `main`
**Hecho**: tarea programada «Parece Mentira — lote tarde (20:00, Jorge)» creada desde el Mac de Jorge, ligada a ese Mac y a `/Users/jorgegomez/Documents/Parece Mentira`, a las 19:52 Europe/Madrid (modo automático). Mismo prompt que la de la mañana con turno «tarde». Carpeta de Jorge apuntada en AGENTE.md; en el Mac de Jorge la clave está en `claves.txt` (no `.env`).
**Ojo**: la primera ejecución es HOY a las 19:52 → primer lote real `2026-11-15-tarde`. El Mac de Jorge debe estar encendido con la app de Claude abierta.
**Pendientes**: Mac de Nico (clave/sesiones); revisar prueba del motor; plan de créditos ElevenLabs; desactivar la tarea antigua de Codex.
**Siguiente paso**: revisar el primer lote de la tarde y responder «ok» o cambios en su chat.

## 2026-11-15 16:55 — Nico — rama `main`
**Hecho**
- `motor/`: motor de montaje 9:16 en Python (Pillow + NumPy + FFmpeg). Escenas con fondo, cámara con paralaje, transiciones (fundido, barrido, corte), 13 tipos de elemento (forma, esfera con volumen y giro, brillo, rayos, partículas, suelo, agua, huella, flecha, barra, persona, imagen, grupo), subtítulo blanco abajo, SRT, manifiesto con SHA-256 y hoja de fotogramas. Documentado en `motor/README.md`.
- Ejemplo `motor/ejemplos/005-huellas-luna/` (6 escenas) renderizado con la locución antigua del 005 **solo como prueba técnica** (no es la voz nueva; no se publica).
- `AGENTE.md` punto 5 apunta al motor; `requirements.txt`; `.gitignore` ignora `out/`.

**Pruebas**: `ffprobe` → 1080×1920, 30 fps, h264 yuv420p, AAC 48 kHz estéreo, 32,94 s, 8,2 MB; render en 87 s; hoja de fotogramas revisada (corregidos: mancha en la playa, textura de la Tierra, sol encima de la barra, tamaño de la huella lunar, brillo final). Vídeo y hoja en `pruebas-motor/` de la carpeta local de Nico.

**Pendientes**: que Nico revise la prueba; sesiones de ElevenLabs y redes en el navegador integrado del Mac de Nico (o API key en `.env`); tarea de las 20:00 de Jorge.

**Siguiente paso**: primera ejecución automática mañana a las 07:52.

---

## 2026-11-15 16:40 — Jorge — rama `main`
**Hecho**: carpeta `~/Documents/Parece Mentira` en el Mac de Jorge; clave API de ElevenLabs «Parece Mentira» creada (permisos: texto a voz y usuario) y guardada por Jorge en `claves.txt`; dominio `api.elevenlabs.io` permitido; TTS de prueba con voice_id `EuJOG4WNDCMcwTFrXKUc` → HTTP 200, MP3 128 kbps 44,1 kHz.
**Nota**: el ordenador conectado a este chat es el de Jorge («jorges-macbook-air-2»); las sesiones de redes y ElevenLabs del navegador integrado están en ese Mac.
**Pendientes**: Mac de Nico (carpeta, claves.txt, sesiones); script de montaje; tareas programadas; plan de créditos ElevenLabs.
**Siguiente paso**: script de montaje 9:16.

## 2026-11-15 16:40 — Nico — rama `main`
**Hecho**
- `AGENTE.md`: manual del agente diario (arranque sin duplicar lotes, ideas verificadas, guiones, voz ElevenLabs «Narrador PM - Curiosidades v1», montaje 9:16, control de calidad, Drive, correo único por turno, publicación solo tras «ok» en el chat del lote).
- `lotes/IDEAS.md`: registro de temas usados (incluye los 10 del sistema antiguo) para no repetir.
- Tarea programada «Parece Mentira — lote mañana (08:00, Nico)» (`trig_01Eu8SmGMhYDCqaCPr3F9u6h`): todos los días a las 07:52 Europe/Madrid, ligada al MacBook Air de Nico y a la carpeta `/Users/nico/Documents/Codex/Parece Mentira`, aprobación automática, sin notificaciones push (el aviso es el correo).

**Pruebas**: la tarea programada aparece activa con la carpeta adjunta; próxima ejecución 2026-11-16 06:52 UTC. Aún no se ha ejecutado ningún lote.

**Pendientes**
- Jorge: crear la tarea de las 20:00 desde su Mac (instrucciones al final de `AGENTE.md`).
- Mac de Nico: iniciar sesión en ElevenLabs, YouTube Studio, Instagram y TikTok en el navegador integrado; o poner `ELEVENLABS_API_KEY` en `.env` de la carpeta local.
- `motor/` no existe: la primera ejecución lo creará si nadie lo prepara antes.
- Desactivar la tarea antigua de Codex de las 08:00.

**Siguiente paso**: preparar `motor/` y probar un lote a mano antes de mañana a las 07:52.

---

## 2026-11-15 16:30 — Jorge — rama `main`
**Hecho**: comprobada en ElevenLabs (navegador integrado, ordenador de Jorge) la voz «Narrador PM - Curiosidades v1», voice_id `EuJOG4WNDCMcwTFrXKUc`. Plan Starter con licencia comercial. Registrada en `DECISIONS.md`.
**Pruebas**: lectura de la lista de voces y de la página de suscripción.
**Pendientes**: API key en `.env`; decidir si el plan Starter basta (ver `TASKS.md`).
**Siguiente paso**: API key de ElevenLabs o carpeta local.

## 2026-11-15 16:25 — Jorge — rama `main`
**Hecho**
- Repo creado de cero en la cuenta compartida y estructura base: `CLAUDE.md` (protocolo), `TASKS.md`, `PROJECT_STATE.md`, `DECISIONS.md`, `HANDOFF.md`, `lotes/`.
- Gmail y Drive comprobados con parecementirapero.media@gmail.com; Drive vaciado; carpeta «Parece Mentira — Revisión» creada.
- Sesiones de YouTube Studio, Instagram y TikTok iniciadas en el navegador integrado del ordenador de Jorge.
- Retirado todo lo publicado (YouTube privado, TikTok «Solo yo» salvo un vídeo bloqueado, Instagram borrado).

**Pruebas**: lectura de Gmail y Drive con los conectores; comprobación de sesión en las tres redes; recarga de YouTube Studio (7 en privado) y TikTok Studio (6 en «Solo yo»); perfil de Instagram con 0 publicaciones.

**Pendientes**: ver `TASKS.md` → Pendiente.

**Siguiente paso**: voz nueva de ElevenLabs o carpeta local de trabajo.
