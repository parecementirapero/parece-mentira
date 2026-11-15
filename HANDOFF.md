# Traspasos

Lo más reciente arriba. Cada entrada: fecha, quién, rama, commit, qué se hizo, pruebas, pendientes, siguiente paso.

---

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
