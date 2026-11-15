# Traspasos

Lo más reciente arriba. Cada entrada: fecha, quién, rama, commit, qué se hizo, pruebas, pendientes, siguiente paso.

---

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
