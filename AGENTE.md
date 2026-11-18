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

- **Aprender antes de producir** (2026-11-17, Nico): lee `motor/APRENDIZAJE.md`, `estadisticas/datos/aprendizajes.md` y `estadisticas/datos/estudio.md` (este último dice cuánto se puede confiar en cada cosa: una «pista» no es motivo para cambiar nada, solo para probar); apunta en `estadisticas/studio.json` «Se quedaron viendo», vistas y horas de los vídeos con 24 h o más (`herramientas/studio_shorts.js`); y, si hay un experimento aprobado en la tabla, aplícalo a **uno** de los tres vídeos y etiquétalo en `estadisticas/etiquetas.json`.

1. Clona `https://github.com/parecementirapero/parece-mentira` y sigue `CLAUDE.md` (pull, leer `PROJECT_STATE.md`, `TASKS.md`, `HANDOFF.md`, `DECISIONS.md`).
2. Calcula el lote: fecha de hoy en Europe/Madrid + turno → `AAAA-MM-DD-manana|tarde`.
3. Si `lotes/<lote>/estado.md` ya existe: **retoma** desde el último paso registrado; no empieces otro.
4. Si en `TASKS.md` el lote está «En curso» por otra persona/agente: no lo toques, registra el motivo en `HANDOFF.md` y termina.
5. Reserva en `TASKS.md` → «En curso»: `Lote <lote> — Agente HH:00 (Nico|Jorge) — fecha hora`. Commit + push **antes** de seguir.
6. Comprueba que la carpeta local del turno responde (`device_list_dir`). Si el ordenador no contesta: registra «ordenador no disponible», deja la tarea en «Pendiente» y termina.
7. **Créditos de ElevenLabs**: `GET https://api.elevenlabs.io/v1/user/subscription` con la clave de `claves.txt` → quedan `character_limit − character_count`. Un lote gasta ≈3.500. Si quedan menos de 10.000, dilo en el chat y en el correo del turno con la cifra («quedan para N lotes»); si no llega para este lote, el lote sale «pendiente de voz» y el asunto del correo empieza por `[AVISO]`.
8. **Datos de YouTube Studio** (no los da la API): en el navegador integrado, para cada Short de YouTube de los últimos 7 días, abre `https://studio.youtube.com/video/<id>/analytics/tab-overview/period-default` y copia el % de «Se quedaron viendo» (bloque «Cómo han interactuado los usuarios») en `estadisticas/studio.json` (`{"<id>": {"seQuedan": 65.3, "fecha": "AAAA-MM-DD"}}`). Commit en el mismo push de la reserva o del siguiente. Si Studio no carga, sigue sin ello.

## 2. Ideas (3 temas)

**Antes de elegir, lee las estadísticas** (son la base de las decisiones del lote):
- `estadisticas/datos/aprendizajes.md`: conclusiones y recomendaciones que se recalculan solas cada mañana (también en la web, vista «Conclusiones»). Cada una lleva su fuerza: **firme** (15+ vídeos) se aplica; **tendencia** (5–14) inclina la elección; **pista** (menos de 5) solo sirve para decidir qué probar.
- Si hace falta más detalle, `estadisticas/datos/data.json` (vistas, % visto, retención a 3 s y curva por vídeo, audiencia, comparación entre redes).
- Elige temas, gancho, estructura y duración apoyándote en lo que funciona. Si una recomendación choca con `DECISIONS.md` (por ejemplo, el horario o el idioma), **no la apliques**: proponla en el correo del turno para que Nico o Jorge decidan.
- **Un experimento por lote**: cambia a propósito una sola cosa respecto a lo que mejor funciona (un tipo de gancho, una estructura, una duración…) y deja las otras dos variables como en los vídeos que mejor van, para poder atribuir el resultado.
- Apunta en `lotes/<lote>/estado.md` una sección **«Decisiones según las estadísticas»**: qué conclusión aplicaste en cada vídeo, cuál es el experimento y qué esperas que pase. En el correo del turno, una línea por vídeo con eso.
- Etiqueta cada vídeo en `metadatos.json` → `"etiquetas"`: `tema` (Cotidiano, Histórico, Espacio, Ciencia, Misterio, Humor), `gancho` (pregunta, dato, contraste, reto, orden, historia, negacion, pov, paradoja), `estructura` (comparación, experimento, reconstrucción, misterio por pistas, metáfora visual) y `experimento` (qué se prueba, o «no»).

- **Prueba del primer segundo** (2026-11-17, `motor/APRENDIZAJE.md` H7): antes de dar un tema por bueno, contesta por escrito en `estado.md`: (1) ¿qué **objeto único y grande se está moviendo ya** en el fotograma 0, y se entiende sin leer nada? (la bota que cae: sí; una cabeza quieta, un personaje de pie o una metáfora como un marcador de fútbol para hablar de una guerra: no); (2) ¿cuál es la primera frase, de 5 palabras o menos? Si alguna no tiene respuesta clara, cambia de enfoque. Además etiqueta `alcance`: `universal` (lo reconoce cualquiera en un segundo: el cuerpo, la Tierra, animales, objetos de casa) o `nicho` (hay que explicar de qué va): es solo para medir H9, **no** es motivo para descartar un tema.
- Fuente de temas: `lotes/IDEAS.md`. **Si hay una sección «Reservados para el lote <lote>» con el lote de hoy, se usan esos temas** (y se quita la sección al pasarlos a «Usados»). Nunca repetir un tema de «Usados»; las continuaciones valen si aportan información nueva y se entienden solas.
- Mezcla: historia, ciencia, misterio/curiosidad. Tres estructuras distintas por lote (comparación visible, experimento, reconstrucción con salto temporal, misterio por pistas, metáfora visual).
- Cada dato central se contrasta con **al menos dos fuentes fiables** (WebSearch/WebFetch). Si no se puede verificar, se cambia de tema.
- Anota los 3 temas en `IDEAS.md` → «Usados» con el lote, en el mismo commit que los guiones.

## 3. Guiones

`lotes/<lote>/guiones.md`, por vídeo:
- **Primer segundo**: es lo que decide si YouTube sigue enseñando el vídeo (ver «Primer segundo» en `aprendizajes.md`; objetivo: que más del 65 % se quede en vez de deslizar). El **fotograma 0** ya enseña lo más llamativo del vídeo (nada de fundidos, títulos ni planos de situación) y la primera frase dice el dato o la pregunta sin introducción.
- **Gancho en pantalla desde el fotograma 0**: en `episodio.json` → `"estilo_subtitulos": {..., "gancho": true}` (la primera frase sale entera desde el inicio; ver `motor/README.md` v2.3). Por eso la primera frase tiene que ser **muy corta: 5 palabras o menos** (antes ≤ 12; cambiado el 2026-11-17 con nuestros datos: ganchos de 1–3 palabras → 74–80 % se queda; de 10–14 palabras → 32–60 %; `motor.calidad` da ❌ a partir de 10). Ejemplos: «Mira tus uñas.», «Esta pisada sigue ahí.». El resto del gancho va en la segunda frase. Y en el fotograma 0, **un solo objeto grande ya en acción** (la bota cayendo), no un personaje quieto ni una pantalla llena de cosas, acabar en punto o interrogación y entenderse sola. Formatos que funcionan en el nicho (análisis de Reels virales, 2026-11-16): **negación** («No son cabezas: los moáis tienen cuerpo.», «Esto NO es un fósil.»), **POV** («POV: vuelves del espacio y tu país ya no existe.»), **paradoja** («¿Por qué encontrar vida en Marte sería una mala noticia?») y **contraste de escala** que se vea en el primer plano. Prueba uno distinto por lote (punto 2) y etiquétalo (`gancho`: `negacion`, `pov`, `paradoja`, además de los de siempre).
- **Gancho** en la primera frase (el primer plano tiene que entenderse sin sonido). Que se entienda igual en España y en Latinoamérica: nada de expresiones solo de España (vale «¿sabías que…?», no «flipar», «tío», «mola»), y referencias que funcionen en los dos lados. La voz sigue siendo de España.
- **Locución**: 150–160 palabras (la voz oficial va a ≈2,85 palabras/s → 53–56 s; nunca más de 165: el Short no puede pasar de 60 s), con 10–12 datos o imágenes distintas (ver `motor/DENSO.md`), español de España, tono cercano, **cifras escritas en letra**.
- **Planos**: qué se ve en cada frase (acciones pequeñas que explican el dato).
- **Fuentes** con enlace: en `guiones.md` y en `metadatos.json` → `fuentes`. **No van en las descripciones** de ninguna red (DECISIONS 2026-11-16, Jorge).
- Título (sin «| elevenlabs.io»), descripción y hashtags por red → `lotes/<lote>/metadatos.json`.
- **Comentario fijado** → `metadatos.json` → `"comentario"`: una pregunta corta que invite a contestar, relacionada con el dato (p. ej. «¿Tú lo sabías? Te leo 👇» o «¿Qué otro misterio de la Isla de Pascua quieres?»). Va en el correo de revisión, así que el «ok» lo aprueba también.
- **Series**: si un tema ya publicado tiene más del doble de la mediana de vistas en alguna red (ver `aprendizajes.md`), uno de los 3 vídeos puede ser su **parte 2** con información nueva que se entienda sola. En ese caso: título con «(parte 2)», la locución acaba con «Si te perdiste la primera parte, está en el canal», y en `metadatos.json` → `"relacionado": "<id de YouTube de la parte 1>"`. Al final de cualquier vídeo de un tema con potencial de continuación, la última frase puede invitar a seguir el canal para la parte 2 (solo si de verdad se va a hacer: apúntalo en `lotes/IDEAS.md` → «Continuaciones prometidas» y hazla en los 3 días siguientes).

- **Antes de generar la voz**: `python3 -m motor.guion <guion.txt>` (un archivo por vídeo, solo la locución). Ningún ❌ (gancho de 10 o más palabras, cifras en números, más de 165 palabras) y los ⚠ arreglados o justificados: rehacer un guion después de la voz gasta créditos. Pasado sobre el lote 2026-11-16-tarde, marca los tres ganchos (10, 11 y 13 palabras), que son los tres peores «se quedaron viendo» del canal.

## 4. Voz (ElevenLabs)

- Voz oficial: **«Archivo Oculto — Narración (clon)»**, voice_id `op8soO9fvP07F3mjbJuB` (ver `DECISIONS.md`). Modelo **`eleven_v4`**, `voice_settings`: `stability` 0.5, `similarity_boost` 0.75 (probado con `with-timestamps`: devuelve audio y alineación).
- Orden de intentos:
  1. **API**: clave `ELEVENLABS_API_KEY` de `claves.txt` en la carpeta local del turno (en los dos Macs; nunca en el repo ni en el chat). Llamada `POST https://api.elevenlabs.io/v1/text-to-speech/op8soO9fvP07F3mjbJuB/with-timestamps` desde `device_bash` o desde el workspace (`api.elevenlabs.io` está permitido). Guarda el MP3 y el JSON de alineación: el motor lo usa para sincronizar los subtítulos.
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
- **Método denso obligatorio (DECISIONS 2026-11-16)**: antes de montar, lee **`motor/DENSO.md`** y sigue sus pasos y reglas. Cada vídeo se monta con `motor/denso.py` (planos atados a palabras del guion, 35–40 planos de 0,3 a 3 s, micro escenas de detalle, control de lectura, detalles de fondo que duran, neones sobre oscuro, efectos de sonido bajos y música presente). Modelo de calidad y ejemplo para copiar: `lotes/prueba-luna-densa/gen.py`. Ilustraciones: reutiliza `motor/biblioteca/` y dibuja las del tema con sus ladrillos (mismo nivel de detalle que los dinosaurios). **No se entrega un vídeo con avisos ⚠ de lectura.** Si el tiempo del turno no da para 3 vídeos a este nivel, haz 2 bien hechos y dilo en el correo: la calidad va antes que el número.
- Estilo de ilustración v4 (base del método denso): piezas antiguas en `lotes/2026-11-15-tarde/generadores/v4/` (`ilus.py`, `ilus_02.py`, `ilus_03.py`) por si sirven para un tema.
- **Antes de montar, lee `motor/REFERENCIAS_2.md` y `motor/OBJETIVO.md`** y aplica sus reglas (planos con `camara.foco`, etiquetas `hud`, sección, acción por frase). Ejemplo de troceo en planos: `lotes/2026-11-15-tarde/generadores/a_v3.py`.
- Referencias de estilo: `/Users/nico/Documents/Codex/Parece Mentira/referencias/` (INDICE.json y hojas de fotogramas; solo en el Mac de Nico). Se toma la técnica, nunca metraje, personajes ni textos.
- Sincroniza escenas y subtítulos con los tiempos reales del MP3 (alineación por palabras de la API de ElevenLabs si está disponible; si no, por duración de frases).
- Salida por vídeo en la carpeta local del lote: `NN-slug_v1.mp4`, `NN-slug_v1.srt`, `NN-slug_v1_manifest.json` (SHA-256 de vídeo, guion y voz).

## 5b. Imágenes reales (experimento desde el lote 2026-11-17-manana, Nico)

**Siempre desde `device_bash` en el Mac del turno** (desde la nube, Wikimedia corta la conexión con «429 demasiadas peticiones»). Solo si el tema tiene algo real que enseñar (un grabado, una foto de la NASA, un objeto de museo) y es el experimento del lote (punto 2). **El objetivo del canal es monetizar: ante cualquier duda, no se usa.**
1. `python3 -m motor.openverse buscar "<términos en inglés>"` → candidatas ya filtradas (solo dominio público, CC0 y CC BY; solo Wikimedia Commons y The Met; nada de SA, NC ni ND).
2. Mira la miniatura y descarta personas reales identificables, logotipos o marcas, y **fotos de obras modernas** (esculturas, cuadros, juguetes, carteles, edificios recientes, figuras de Lego…): la licencia de la foto no cubre la obra que sale en ella. Sí valen objetos antiguos, paisajes, grabados antiguos, documentos y fotos de la NASA.
3. `python3 -m motor.openverse descargar <id> --lote <carpeta local del lote> --video NN --uso "plano N, …"`: comprueba la licencia **en la fuente original** (si no coincide, hay restricciones o es dominio público solo en EE. UU., la rechaza), descarga la imagen y la apunta en `<lote>/creditos.json` con fecha y SHA-256. Mira la imagen descargada y pon `"revision_visual": "ok"` en su entrada. Copia `creditos.json` a `lotes/<lote>/` del repo (solo texto).
4. **Máximo 2 planos reales por vídeo y ≤ 20 % de la duración**, siempre con animación nuestra encima (cámara con foco, flechas, rótulos o capas) y con narración: nunca la imagen sola y quieta. Así el vídeo sigue siendo claramente nuestro (YouTube revisa el «contenido reutilizado» del canal entero, aunque la licencia lo permita).
5. **Créditos obligatorios**: añade la salida de `python3 -m motor.openverse creditos <lote> --video NN` al final de la descripción de YouTube, Instagram y TikTok en `metadatos.json`.
6. Etiqueta `"experimento": "plano real"`. Audio de Openverse: **no** de momento (riesgo de reclamaciones automáticas); la música sigue siendo la generada por el motor.
7. Si no hay acceso a los dominios de `motor/openverse.py` (`DOMINIOS`) o algo falla, sigue con ilustración y dilo en el correo; nunca uses una imagen sin pasar por el paso 3.

## 6. Control de calidad (no se entrega sin esto)

- `ffprobe`: resolución, fps, códecs, que haya audio y que dure lo que la locución.
- Hoja de fotogramas (1 cada 2 s) y **mirarla**: texto legible, nada cortado, sin panel en medio, sin título, sin Nova, flechas bien orientadas, algo en movimiento en cada plano.
- **Control automático**: `python3 -m motor.calidad DIR/episodio.json --mp4 DIR/out/<id>.mp4 --md DIR/calidad.md`. **Ningún ❌** (rótulos tapados por la app, textos sin tiempo de lectura, bordes negros por zoom < 1…); los ⚠ se arreglan o se justifican en `estado.md`. Qué mide y por qué: `motor/GUIA_CALIDAD.md`.
- Revisar cifras y nombres contra el guion y las fuentes.
- Si un vídeo no pasa, se corrige y se sube a `_v2`; nunca se entrega uno roto.
- **Ficha de variables** (2026-11-17, Nico; en prueba hasta que Nico y Jorge lo confirmen): antes de entregar, una ficha por vídeo para el estudio de audiencia y rendimiento (`estadisticas/estudio/README.md`). Se rellena **antes de publicar** y no se cambia al ver los resultados:
  `python3 estadisticas/estudio ficha nueva <lote> <NN> --guion <locución.txt> --calidad <calidad-NN.md> --quien "Agente HH:00" tema=… alcance=… epoca=… gancho=… f0_palabras=… f0_sujeto=… f0_literal=sí|no estructura=… remate=… duracion_s=… montaje=denso subtitulo=karaoke voz=clon reciclado=no experimento=no brazo=-`
  Lo demás (palabras del gancho, persona, cifra, preguntas, cortes, nota, movimiento del primer segundo) lo calcula solo. Valores permitidos: `python3 estadisticas/estudio ficha diccionario`. Comprobar: `python3 estadisticas/estudio ficha comprobar`. Si hay un experimento abierto en `estadisticas/experimentos/`, el vídeo que le toque lleva `experimento=<id>` y `brazo=A` (con el cambio) o `brazo=B` (sin él), con el orden de salida del calendario del experimento. Si la orden falla, se sigue con el lote y se apunta en `estado.md`.

## 6b. Portadas (las elige el agente, sin «ok»)

Para cada vídeo que pase el control de calidad, **lanza el subagente `portadas`** (`.claude/agents/portadas.md`) con la ruta del `episodio.json` (o del MP4), `metadatos.json`, el número del vídeo y la carpeta `<carpeta local del lote>/NN-portadas`. Lánzalos a la vez para los 3 vídeos. Si el subagente no está disponible en la sesión, haz tú los mismos pasos de ese archivo (es la fuente de verdad: texto de 2–5 palabras + una variante, 8 candidatas con `motor.portadas`, mirar las hojas, elegir con sus criterios, `--elegir` con motivo, apuntarlo en `metadatos.json`).

La portada **no necesita aprobación** (DECISIONS 2026-11-16): se manda al chat y al correo como información y se pone sola al publicar el vídeo. Si Nico o Jorge escriben otra cosa («portada 2 del vídeo 1», «cambia el texto a…»), se cambia y punto.

## 7. Entrega

1. **Vídeos en el chat (sin Drive)**: copia los 3 MP4 de la carpeta local al contenedor con `device_stage_files` y **envíalos con `SendUserFile`** (uno por vídeo, con un pie corto: «1/3 · título · duración»). Así se ven y se reproducen dentro del chat de Claude, desde el Mac o el móvil. Si un MP4 no se puede enviar, dilo en el chat y en el correo (el archivo sigue en la carpeta local).
2. **Correo** (conector de Gmail) a `parecementirapero.media@gmail.com` — **una sola notificación por turno**:
   - Asunto: `[Parece Mentira] Lote <lote> — 3 vídeos para revisar`
   - Antes del correo, en el chat: envía la **`portada.jpg` elegida** de cada vídeo con `SendUserFile` (pie: «portada 1/3 · texto · motivo»). Las hojas de candidatas no hace falta mandarlas salvo que las pidan. La portada no espera ningún «ok».
   - Cuerpo: **enlace a este chat** (la sesión de la ejecución, donde están los vídeos para verlos) y la instrucción: _«Abre el chat, mira los vídeos y escribe "ok" (o "ok 1 y 3" para solo esos). Para cambios, escríbelos ahí.»_; por vídeo: título, duración, versión y SHA-256 corto, fuentes, comentario fijado, **portada elegida (texto, diseño y motivo, sin pedir aprobación)** y, si lo hay, de qué vídeo es parte 2; vídeos «pendiente de voz» si los hay. Sin enlaces a Drive.
3. **Registro** en el repo: `lotes/<lote>/estado.md` (estado «en revisión», enlace al chat, id del correo), `TASKS.md` (el lote pasa a «Hecho» con nota «en revisión»), `PROJECT_STATE.md`, entrada en `HANDOFF.md`. Commit + push y comprobar que entró.
4. Responde en el chat con un resumen corto (los vídeos enviados arriba y qué falta) y **espera** el «ok».

## 8. Publicar tras «ok»

Solo cuando una persona escribe **«ok»** en el chat de ese lote (o «ok 1, 3» para algunos). Cualquier otro mensaje = cambios, no aprobación. La aprobación vale para **esa versión exacta**: si se toca algo, hay versión nueva y hace falta otro «ok».

1. Antes de cada subida, comprueba en la red que ese vídeo no está ya publicado (evitar duplicados).
2. **Subidas separadas solo en YouTube** (ver `DECISIONS.md`): el primero se publica ya y cada uno de los siguientes **1 hora después** del anterior. En TikTok e Instagram se publican todos seguidos al dar el «ok».
3. **YouTube, automático por la API** (`publicar/README.md`), desde `device_bash` en la carpeta local del turno:
   `python3 publicar/subir_youtube.py --claves claves.txt --metadatos <repo>/lotes/<lote>/metadatos.json --clave 01 --video lotes/<lote>/<archivo>.mp4` y, para los siguientes, `--publicar-en <hora con zona, +1 h, +2 h>`. Añade siempre `--portada <carpeta local del lote>/NN-portadas/portada.jpg`: el script intenta ponerla por la API y dice `"portada": "puesta"` o `"no: …"` (en Shorts YouTube solo deja miniaturas propias a algunos canales). Si dice que no, en Studio → el Short → Miniatura, elige el fotograma del segundo `portada.t` de `metadatos.json` (o sube `portada.jpg` si aparece «Subir miniatura»). Copia antes `publicar/subir_youtube.py` del repo a la carpeta local si falta o ha cambiado. Si el script dice que faltan claves o que la red no llega a Google, sube a YouTube desde el navegador como antes y avisa en el chat de qué falta.
3b. **Instagram y TikTok por la API oficial, solo si esa red ya está puesta en marcha** (`publicar/README.md`; preparado el 2026-11-17, pendiente de activar). Cómo saberlo: desde `device_bash`, en la carpeta local del turno (con la carpeta `publicar/` del repo copiada entera), lanza el comando con `--prueba`. Si contesta `"ok": true`, esa red va por API; si dice que faltan claves, esa red va por el navegador (punto 4) y no hay que avisar de nada.
   - Instagram: `python3 publicar/subir_instagram.py --claves claves.txt --metadatos lotes/<lote>/metadatos.json --clave 01 --video lotes/<lote>/<archivo>.mp4 --comentario` → publica el Reel con su texto y la portada del fotograma `portada.t`. Apunta la `url`.
   - TikTok: **solo si `DECISIONS.md` dice que TikTok va por borrador** (hoy no lo dice: falta la prueba real). `python3 publicar/subir_tiktok.py …` (mismos argumentos, sin `--comentario`) deja el vídeo en la bandeja de entrada de TikTok; manda al chat el `texto` que devuelve, uno por vídeo, para que la persona lo pegue en el móvil y publique. Después, `--estado` da el enlace.
   - Los scripts no duplican (apuntan en `publicado.json`, junto a `metadatos.json`; cópialo a `lotes/<lote>/` del repo en el commit del punto 6). `"estado": "procesando"` = repetir el mismo comando un minuto después. Con `"ok": false`, lee `error`: dice qué hacer; si no se arregla en el momento, esa red se publica por el navegador tras comprobar que no salió.
4. **TikTok e Instagram, desde el navegador integrado** (las redes que no vayan por API) del ordenador del turno, con las sesiones ya iniciadas. El selector de archivos no lo puede manejar Claude: pide en el chat que la persona elija el archivo (di cuál) y haz tú todo lo demás.
   - TikTok: todos seguidos, sin programar. **Portada**: «Editar portada» → si hay opción de subir imagen, pide a la persona que elija `NN-portadas/portada.jpg`; si no, elige el fotograma del segundo `portada.t` (de `metadatos.json`) y añade el texto de `portada.texto` con la herramienta de texto de la portada.
   - Instagram @parecementiramedia (Reel, formato original 9:16): todos seguidos. Pulsa «Compartir» con un clic real (no con un script: así el texto no se guardaba). **Después de compartir, abre cada Reel y comprueba que tiene el texto**: desde la web a veces se publica sin él (2026-11-16); si falta, ⋯ → Editar → texto → Hecho. **Portada**: en «Portada» → «Seleccionar del ordenador», pide a la persona que elija `NN-portadas/portada.jpg` (es el mismo tipo de paso que elegir el vídeo).
   Si el navegador integrado no deja elegir el archivo, usa Claude in Chrome si está disponible; si no, deja el vídeo listo, di exactamente qué paso falta y no insistas.
5. Si una red falla, solo se reintenta esa red tras comprobar que no se publicó.
6. Registra en `lotes/<lote>/estado.md` la URL de cada publicación (o el motivo del bloqueo), actualiza `HANDOFF.md` y push.
7. **Comentario fijado y vídeo relacionado** (sin pedir nada más: lo cubre el «ok»):
   - YouTube: cuando cada vídeo ya sea público, abre `https://www.youtube.com/shorts/<id>` en el navegador integrado, escribe el `comentario` de `metadatos.json` y fíjalo (⋮ del comentario → Fijar). Para los programados (+1 h, +2 h), programa un aviso en este mismo chat con `send_later` a esa hora y hazlo entonces. Si el vídeo es una parte 2, en Studio → Detalles → «Vídeo relacionado» elige la parte 1.
   - TikTok: en la página del vídeo, mismo comentario y fíjalo (⋯ → Fijar). Instagram: escribe el comentario (la web no siempre deja fijar; si no deja, se queda sin fijar).
8. **Etiquetas para las estadísticas**: añade cada vídeo publicado a `estadisticas/etiquetas.json` con su id de YouTube (las 11 letras de la URL del Short) y las etiquetas de `metadatos.json` (`tema`, `gancho`, `estructura`, `experimento`, `portada`). Sin esto, las conclusiones no pueden decir qué gancho o estructura funciona. Mismo commit que el punto 6. Y une la ficha con el vídeo: `python3 estadisticas/estudio ficha publicar <lote> <NN> <id de YouTube> tiktok=<número> instagram=<código>`.

## 8b. Contestar comentarios (2026-11-19, petición en el chat del lote 2026-11-18-tarde: «quiero que tú contestes a comentarios de la gente, con cosas con sentido a lo que escriben»; confirmado «sí, sin preguntar»)

En cada turno (08:00 y 20:00), después de la entrega y sin esperar «ok»:
1. YouTube Studio → Comunidad → Comentarios, filtro «Sin responder» (navegador integrado del Mac del turno, vista de escritorio con `resize_window` 1280×900). TikTok Studio → Comments.
2. Responder **a lo que dice cada persona**: corto (1–3 frases), español neutro (sin «tío», «mola», «hostia»…), cercano, con un dato correcto del vídeo o una pregunta que siga la conversación. Si el comentario se equivoca en un dato, corregir con amabilidad y con la fuente (como en `guiones.md`).
3. **No contestar**: insultos, spam o texto sin sentido, política, salud o temas delicados de la persona, peticiones de datos personales o enlaces. Esos se saltan y se apuntan en el correo del turno.
4. Nada de promesas («haremos parte 2») salvo que esté en `IDEAS.md` → «Continuaciones prometidas».
5. Apuntar en `lotes/<lote>/estado.md` cuántas respuestas y en qué vídeos.

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
