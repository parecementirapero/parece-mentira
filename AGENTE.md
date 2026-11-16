# Agente diario — Parece Mentira

Manual que sigue **cada ejecución programada** (y cualquier Claude que produzca un lote a mano).
Si algo de aquí choca con `DECISIONS.md`, manda `DECISIONS.md`: se avisa y no se improvisa.

_Creado: 2026-11-15 — Nico_

---

## 0. Turnos y ordenadores

| Turno | Hora (Europe/Madrid) | Ordenador | Carpeta local de trabajo | Carpeta de lote |
|---|---|---|---|---|
| `manana` | 08:00 | MacBook Air de Nico | `/Users/nico/Documents/Parece Mentira` | `lotes/AAAA-MM-DD-manana` |
| `tarde` | 20:00 | Mac de Jorge (`jorges-macbook-air-2`) | `/Users/jorgegomez/Documents/Parece Mentira` | `lotes/AAAA-MM-DD-tarde` |

Carpeta local (ver `DECISIONS.md`): `claves.txt` (ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID; nunca al repo ni al chat), `lotes/<lote>/` (MP3, MP4, SRT y manifiestos del lote) y `renders/` (pruebas). Referencias de estilo: `/Users/nico/Documents/Codex/Parece Mentira/referencias` (solo en el Mac de Nico).

En el registro, el agente firma como **«Agente 08:00 (Nico)»** o **«Agente 20:00 (Jorge)»**.

Cada lote = **3 vídeos** 9:16. Dos lotes al día = 6 vídeos.

---

## 1. Arranque (idempotente: nunca duplicar un lote)

1. Clona `https://github.com/parecementirapero/parece-mentira` y sigue `CLAUDE.md` (pull, leer `PROJECT_STATE.md`, `TASKS.md`, `HANDOFF.md`, `DECISIONS.md`).
2. Calcula el lote: fecha de hoy en Europe/Madrid + turno → `AAAA-MM-DD-manana|tarde`.
3. Si `lotes/<lote>/estado.md` ya existe: **retoma** desde el último paso registrado; no empieces otro.
4. Si en `TASKS.md` el lote está «En curso» por otra persona/agente: no lo toques, registra el motivo en `HANDOFF.md` y termina.
5. Reserva en `TASKS.md` → «En curso»: `Lote <lote> — Agente HH:00 (Nico|Jorge) — fecha hora`. Commit + push **antes** de seguir.
6. Comprueba que la carpeta local del turno responde (`device_list_dir`). Si el ordenador no contesta: registra «ordenador no disponible», deja la tarea en «Pendiente» y termina.

## 2. Ideas (3 temas)

**Antes de elegir, lee las estadísticas** (son la base de las decisiones del lote):
- `estadisticas/datos/aprendizajes.md`: conclusiones y recomendaciones que se recalculan solas cada mañana (también en la web, vista «Conclusiones»). Cada una lleva su fuerza: **firme** (15+ vídeos) se aplica; **tendencia** (5–14) inclina la elección; **pista** (menos de 5) solo sirve para decidir qué probar.
- Si hace falta más detalle, `estadisticas/datos/data.json` (vistas, % visto, retención a 3 s y curva por vídeo, audiencia, comparación entre redes).
- Elige temas, gancho, estructura y duración apoyándote en lo que funciona. Si una recomendación choca con `DECISIONS.md` (por ejemplo, el horario o el idioma), **no la apliques**: proponla en el correo del turno para que Nico o Jorge decidan.
- **Un experimento por lote**: cambia a propósito una sola cosa respecto a lo que mejor funciona (un tipo de gancho, una estructura, una duración…) y deja las otras dos variables como en los vídeos que mejor van, para poder atribuir el resultado.
- Apunta en `lotes/<lote>/estado.md` una sección **«Decisiones según las estadísticas»**: qué conclusión aplicaste en cada vídeo, cuál es el experimento y qué esperas que pase. En el correo del turno, una línea por vídeo con eso.
- Etiqueta cada vídeo en `metadatos.json` → `"etiquetas"`: `tema` (Cotidiano, Histórico, Espacio, Ciencia, Misterio, Humor), `gancho` (pregunta, dato, contraste, reto, orden, historia), `estructura` (comparación, experimento, reconstrucción, misterio por pistas, metáfora visual) y `experimento` (qué se prueba, o «no»).

- Fuente de temas: `lotes/IDEAS.md`. **Si hay una sección «Reservados para el lote <lote>» con el lote de hoy, se usan esos temas** (y se quita la sección al pasarlos a «Usados»). Nunca repetir un tema de «Usados»; las continuaciones valen si aportan información nueva y se entienden solas.
- Mezcla: historia, ciencia, misterio/curiosidad. Tres estructuras distintas por lote (comparación visible, experimento, reconstrucción con salto temporal, misterio por pistas, metáfora visual).
- Cada dato central se contrasta con **al menos dos fuentes fiables** (WebSearch/WebFetch). Si no se puede verificar, se cambia de tema.
- Anota los 3 temas en `IDEAS.md` → «Usados» con el lote, en el mismo commit que los guiones.

## 3. Guiones

`lotes/<lote>/guiones.md`, por vídeo:
- **Gancho** en la primera frase (el primer plano tiene que entenderse sin sonido). Que se entienda igual en España y en Latinoamérica: nada de expresiones solo de España (vale «¿sabías que…?», no «flipar», «tío», «mola»), y referencias que funcionen en los dos lados. La voz sigue siendo de España.
- **Locución**: 130–170 palabras (≈45–60 s; ver `DECISIONS.md`), español de España, tono cercano, **cifras escritas en letra**.
- **Planos**: qué se ve en cada frase (acciones pequeñas que explican el dato).
- **Fuentes** con enlace (van a la descripción).
- Título (sin «| elevenlabs.io»), descripción y hashtags por red → `lotes/<lote>/metadatos.json`.

## 4. Voz (ElevenLabs)

- Voz oficial: **«Narrador PM - Curiosidades v1»**, voice_id `EuJOG4WNDCMcwTFrXKUc` (ver `DECISIONS.md`).
- Orden de intentos:
  1. **API**: clave `ELEVENLABS_API_KEY` de `claves.txt` en la carpeta local del turno (en los dos Macs; nunca en el repo ni en el chat). Llamada `POST https://api.elevenlabs.io/v1/text-to-speech/EuJOG4WNDCMcwTFrXKUc/with-timestamps` desde `device_bash` o desde el workspace (`api.elevenlabs.io` está permitido). Guarda el MP3 y el JSON de alineación: el motor lo usa para sincronizar los subtítulos.
  2. **Navegador integrado** (sesión de ElevenLabs ya iniciada en ese ordenador): Text to Speech con esa voz, descargar el MP3.
- Antes de generar, mira los créditos que quedan. Un lote gasta ≈2.500 caracteres. **Si no llegan, no se compra nada**: lote «pendiente de voz».
- Si la voz falla por cualquier motivo: el vídeo queda **«pendiente de voz»**. Prohibido usar otra voz (ni del sistema ni de otra cuenta).
- Guarda `NN-locucion.mp3` en la carpeta local del lote.

## 5. Montaje 9:16

- Motor reproducible en `motor/` (lee `motor/README.md`): un `episodio.json` por vídeo → `python3 -m motor.render episodio.json --salida <dir>`. Dependencias: `pip install -r requirements.txt` (Pillow, NumPy) y FFmpeg. Se renderiza en el workspace y los resultados se copian a la carpeta local del lote.
- Itera con `--hoja` (5 s) hasta que la hoja de fotogramas esté bien; luego render completo (~90 s por vídeo de 30 s).
- Ejemplo completo para copiar el estilo y la estructura: `motor/ejemplos/005-huellas-luna/generar.py`.
- Si un tema necesita un objeto que el motor no tiene, se añade un tipo nuevo en `motor/elementos.py` (sin romper el ejemplo 005) y se documenta en el README del motor.
- Especificación de salida: **1080×1920, 30 fps, H.264 yuv420p (`-preset veryfast`), AAC 48 kHz estéreo**, duración = locución + ~0,5 s.
- Estilo obligatorio (`DECISIONS.md`): ilustración a **pantalla completa**, sin título arriba, sin rótulos blancos con borde azul, **solo subtítulo blanco abajo** sincronizado con la voz, **sin Nova** dentro del vídeo. Ilustración 2.5D en capas, luces y sombras, **algo moviéndose siempre**, cámara estable, flechas y giros correctos. Nada de zooms sobre una imagen fija como única animación.
- **Estilo obligatorio v4**: dibuja cada escena como en `lotes/2026-11-15-tarde/generadores/v4/` (`ilus.py`, `ilus_02.py`, `ilus_03.py` para las ilustraciones SVG; `comun_v4.py` + `gen_0N.py` para el montaje por planos). Reutiliza y amplía esas piezas; crea ilustraciones nuevas con el mismo nivel de detalle para cada tema.
- **Antes de montar, lee `motor/REFERENCIAS_2.md` y `motor/OBJETIVO.md`** y aplica sus reglas (planos con `camara.foco`, etiquetas `hud`, sección, acción por frase). Ejemplo de troceo en planos: `lotes/2026-11-15-tarde/generadores/a_v3.py`.
- Referencias de estilo: `/Users/nico/Documents/Codex/Parece Mentira/referencias/` (INDICE.json y hojas de fotogramas; solo en el Mac de Nico). Se toma la técnica, nunca metraje, personajes ni textos.
- Sincroniza escenas y subtítulos con los tiempos reales del MP3 (alineación por palabras de la API de ElevenLabs si está disponible; si no, por duración de frases).
- Salida por vídeo en la carpeta local del lote: `NN-slug_v1.mp4`, `NN-slug_v1.srt`, `NN-slug_v1_manifest.json` (SHA-256 de vídeo, guion y voz).

## 6. Control de calidad (no se entrega sin esto)

- `ffprobe`: resolución, fps, códecs, que haya audio y que dure lo que la locución.
- Hoja de fotogramas (1 cada 2 s) y **mirarla**: texto legible, nada cortado, sin panel en medio, sin título, sin Nova, flechas bien orientadas, algo en movimiento en cada plano.
- Revisar cifras y nombres contra el guion y las fuentes.
- Si un vídeo no pasa, se corrige y se sube a `_v2`; nunca se entrega uno roto.

## 7. Entrega

1. **Vídeos en el chat (sin Drive)**: copia los 3 MP4 de la carpeta local al contenedor con `device_stage_files` y **envíalos con `SendUserFile`** (uno por vídeo, con un pie corto: «1/3 · título · duración»). Así se ven y se reproducen dentro del chat de Claude, desde el Mac o el móvil. Si un MP4 no se puede enviar, dilo en el chat y en el correo (el archivo sigue en la carpeta local).
2. **Correo** (conector de Gmail) a `parecementirapero.media@gmail.com` — **una sola notificación por turno**:
   - Asunto: `[Parece Mentira] Lote <lote> — 3 vídeos para revisar`
   - Cuerpo: **enlace a este chat** (la sesión de la ejecución, donde están los vídeos para verlos) y la instrucción: _«Abre el chat, mira los vídeos y escribe "ok" (o "ok 1 y 3" para solo esos). Para cambios, escríbelos ahí.»_; por vídeo: título, duración, versión y SHA-256 corto, fuentes; vídeos «pendiente de voz» si los hay. Sin enlaces a Drive.
3. **Registro** en el repo: `lotes/<lote>/estado.md` (estado «en revisión», enlace al chat, id del correo), `TASKS.md` (el lote pasa a «Hecho» con nota «en revisión»), `PROJECT_STATE.md`, entrada en `HANDOFF.md`. Commit + push y comprobar que entró.
4. Responde en el chat con un resumen corto (los vídeos enviados arriba y qué falta) y **espera** el «ok».

## 8. Publicar tras «ok»

Solo cuando una persona escribe **«ok»** en el chat de ese lote (o «ok 1, 3» para algunos). Cualquier otro mensaje = cambios, no aprobación. La aprobación vale para **esa versión exacta**: si se toca algo, hay versión nueva y hace falta otro «ok».

1. Antes de cada subida, comprueba en la red que ese vídeo no está ya publicado (evitar duplicados).
2. **Subidas separadas solo en YouTube** (ver `DECISIONS.md`): el primero se publica ya y cada uno de los siguientes **1 hora después** del anterior. En TikTok e Instagram se publican todos seguidos al dar el «ok».
3. **YouTube, automático por la API** (`publicar/README.md`), desde `device_bash` en la carpeta local del turno:
   `python3 publicar/subir_youtube.py --claves claves.txt --metadatos <repo>/lotes/<lote>/metadatos.json --clave 01 --video lotes/<lote>/<archivo>.mp4` y, para los siguientes, `--publicar-en <hora con zona, +1 h, +2 h>`. Copia antes `publicar/subir_youtube.py` del repo a la carpeta local si falta o ha cambiado. Si el script dice que faltan claves o que la red no llega a Google, sube a YouTube desde el navegador como antes y avisa en el chat de qué falta.
4. **TikTok e Instagram, desde el navegador integrado** del ordenador del turno, con las sesiones ya iniciadas. El selector de archivos no lo puede manejar Claude: pide en el chat que la persona elija el archivo (di cuál) y haz tú todo lo demás.
   - TikTok: todos seguidos, sin programar.
   - Instagram @parecementiramedia (Reel, formato original 9:16): todos seguidos.
   Si el navegador integrado no deja elegir el archivo, usa Claude in Chrome si está disponible; si no, deja el vídeo listo, di exactamente qué paso falta y no insistas.
5. Si una red falla, solo se reintenta esa red tras comprobar que no se publicó.
6. Registra en `lotes/<lote>/estado.md` la URL de cada publicación (o el motivo del bloqueo), actualiza `HANDOFF.md` y push.
7. **Etiquetas para las estadísticas**: añade cada vídeo publicado a `estadisticas/etiquetas.json` con su id de YouTube (las 11 letras de la URL del Short) y las etiquetas de `metadatos.json` (`tema`, `gancho`, `estructura`, `experimento`). Sin esto, las conclusiones no pueden decir qué gancho o estructura funciona. Mismo commit que el punto 6.

## 9. Límites

- No publica ni programa sin «ok». No compra nada ni cambia de plan. No mete contraseñas ni códigos (si una sesión caducó, avisa).
- Nada pesado en git (MP3/MP4 se quedan en la carpeta local; la revisión se hace con los vídeos enviados al chat).
- Si algo bloquea el lote, se registra la causa en `estado.md` y `HANDOFF.md`, y se avisa en el mismo correo del turno.

---

## Tareas programadas

Cada tarea programada se crea **desde el ordenador que la va a ejecutar** (queda ligada a ese ordenador y a su carpeta local).

- **08:00 — Nico**: «Parece Mentira — lote mañana (08:00, Nico)», arranca a las 07:52; creada el 2026-11-15 desde el MacBook Air de Nico con las carpetas `/Users/nico/Documents/Parece Mentira` y `/Users/nico/Documents/Codex/Parece Mentira` (referencias). Primera ejecución: 2026-11-16.
- **20:00 — Jorge**: creada el 2026-11-15 desde el Mac de Jorge (19:52 Europe/Madrid, ligada a ese Mac y a `/Users/jorgegomez/Documents/Parece Mentira`). Primera ejecución: 2026-11-15. Instrucciones originales:
  > Crea la tarea programada de la tarde de Parece Mentira según AGENTE.md del repo: todos los días a las 20:00 Europe/Madrid, que use este ordenador y mi carpeta de trabajo.

  El prompt de esa tarea es el mismo que el de la mañana cambiando `manana`→`tarde`, `08:00`→`20:00`, `Nico`→`Jorge` y la carpeta local. Después, Jorge rellena su carpeta en la tabla del punto 0.
