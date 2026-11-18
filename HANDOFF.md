# Traspasos

Lo más reciente arriba. Cada entrada: fecha, quién, rama, commit, qué se hizo, pruebas, pendientes, siguiente paso.

---

## 2026-11-18 14:55 — Agente 20:00 (Jorge) — rama `main` — YouTube del lote 2026-11-17-tarde
**Hecho**: permiso de subida de YouTube concedido en el Mac de Jorge (pedido y aprobado en el chat; token solo en `claves.txt`). Cebolla v2 publicada (dMcGHyKbeaA). El Sol tenía una subida rota del 17-11 (cjSc0D_gOaI, 0 s): borrada con aprobación y resubida la v3 (G_xEqU97krk, programada 15:49). Rayo ya estaba (dOdQj9QyoBI). `etiquetas.json` actualizado.
**Pendiente**: TikTok de los lotes 2026-11-17-tarde y 2026-11-18-manana (6 vídeos; hace falta alguien delante del Mac para elegir cada archivo). Comentarios de YouTube sin poner (fijar no se puede hasta verificar el canal).

## 2026-11-18 09:00 — Agente 08:00 (Nico) — rama `main` — lote 2026-11-18-manana publicado en YouTube
**Hecho**: «ok» a los 3 en el chat del lote (la persona no dijo nombre; desde el móvil). YouTube por API desde el Mac de Nico: 01 público `5pSKNws_e-s` (08:45), 02 `rEiiPtGXz84` programado 09:50, 03 `tp7XFLAIkS0` programado 10:50 (`--prueba` antes: sin duplicados). `etiquetas.json` y fichas unidas a los ids. Comentario del 01 escrito (sin emojis); fijar no se puede hasta verificar el canal en Studio. Avisos `send_later` en el chat a las 09:53 y 10:53 para los comentarios del 02 y 03.
**No hecho**: portada por API (403: el canal no tiene miniaturas personalizadas) → en Studio, fotograma `portada.t`. **TikTok**: la persona estaba en el móvil y el selector de archivos del navegador integrado necesita a alguien delante del Mac; Nico pide que **lo suba Jorge desde su ordenador** (tarea en TASKS → Pendiente, con dónde están los MP4 y los textos).
**Siguiente paso**: Jorge publica los 3 en TikTok y apunta los enlaces en `estado.md`.

## 2026-11-18 08:55 — Agente 08:00 (Nico) — rama `main` — lote 2026-11-18-manana
**Hecho**: lote `2026-11-18-manana`, 3 vídeos v1 en revisión: 01 «Hace 1.400 millones de años, un día duraba 18 horas» (Espacio, cadena de datos, gancho de dato, control), 02 «La Gran Muralla China NO se ve desde el espacio» (Histórico, mito y realidad, **experimento: gancho de negación**), 03 «Tu perro copia tus bostezos» (Ciencia, experimento, gancho de dato, control). Cada dato con ≥ 2 fuentes (`guiones.md`). Voz oficial por API desde el Mac de Nico (sin fallos); en el 02 se quitó al montar «Nadie había subido nunca.» (`omitir`) porque la voz salía de 59,9 s. Ilustraciones nuevas en `generadores/ilus_0N.py`, montaje con `motor/denso.py` (36–42 planos), render en la nube (los 3 vídeos montados en paralelo). Portadas elegidas sin «ok». Fichas de variables creadas antes de publicar. Vídeos y portadas en el chat y en el Mac (SHA iguales). Correo `1a1ed968a22c00b4`.
**Pruebas**: `motor.guion` ✓ ×3; `construir` sin ⚠ de lectura; `motor.calidad --mp4` 95/95/91 sin ❌ (⚠ justificados en `estado.md`); ffprobe 1080×1920/30 fps/h264/AAC 48 kHz; hojas de fotogramas revisadas; `ficha comprobar` 0 problemas. No se tocó `motor/`.
**No hecho**: Studio no se abrió (sin lecturas nuevas en `studio.json`). Sin publicar: falta el «ok». Drive no se usa aunque lo pida el texto de la tarea programada (DECISIONS manda; tarea ya apuntada en TASKS).
**Créditos ElevenLabs**: quedan 27.748 de 40.000 (≈7 lotes).
**Siguiente paso**: «ok» en https://claude.ai/code/session_019BG1dJLtMKt7d9zxuM93s6 → publicar según AGENTE §8 (YouTube por API desde el Mac de Nico, TikTok por navegador).

## 2026-11-17 23:10 — Nico (chat del Mac de Nico) — rama `main` — lote 2026-11-17-tarde: 01 y 02 en YouTube
**Hecho**: Nico pidió subir los vídeos descargados del lote de Jorge: en su Mac están 01 v3 y 02 v3 (SHA-256 iguales a `estado.md`); el 03 v2 no está descargado. Copiados a `~/Documents/Parece Mentira/lotes/2026-11-17-tarde/` con `metadatos.json`; `publicar/subir_youtube.py` del Mac actualizado al del repo. YouTube por API: 01 público (`dOdQj9QyoBI`), 02 programado a las 23:59 (`cjSc0D_gOaI`). `estado.md`, `etiquetas.json` y fichas (`ficha publicar`) al día.
**Pruebas**: SHA-256, ffprobe, `--prueba` ×2; tras un corte de conexión con el Mac, comprobado por la API (`videos.list`): 01 `public`/`processed`, 02 `private` con `publishAt` 22:59Z; sin duplicados.
**Pendiente**: TikTok de 01 y 02 (sesión iniciada en el navegador integrado del Mac de Nico, no están subidos; la persona elige el archivo en `Documents/Parece Mentira/lotes/2026-11-17-tarde/`). Portada: sin `portada.jpg` en este Mac → elegir fotograma `portada.t` en Studio. Comentarios fijados en YouTube y TikTok. 03 v2 sin publicar (bajarlo del chat del lote).
**Siguiente paso**: Nico elige el archivo en TikTok y Claude pone texto y publica.

## 2026-11-17 21:10 — Agente 20:00 (Jorge) — rama `main` — lote 2026-11-17-tarde v3 + reglas
**Hecho**: 01 y 02 en v3 con menos relojes (2 y 1; nunca dos planos seguidos con reloj). Reglas nuevas guardadas como pidió la persona en el chat: `DECISIONS.md` → «Variedad y claridad en los planos» (pocos relojes, no repetir objeto ni animación, lo que se explica se ve pasar, estelas, caras bien dibujadas y coherentes) y resumen en `motor/DENSO.md`. `motor.calidad` 79/87 sin ❌. Vídeos en el chat.
**Pendiente**: «ok» para 01 v3, 02 v3 y 03 v2. Los MP4 v2/v3 no están en el Mac: bajarlos del chat antes de publicar.

## 2026-11-17 20:25 — Agente 20:00 (Jorge) — rama `main` — lote 2026-11-17-tarde
**Hecho**: lote `2026-11-17-tarde`, 3 vídeos v1 en revisión: 01 «Un rayo es 5 veces más caliente que el Sol» (Ciencia, comparación, gancho de contraste, control), 02 «El Sol que ves ya es pasado» (Espacio, reconstrucción, gancho de dato, control), 03 «Por qué lloras al cortar cebolla» (Cotidiano, experimento, **experimento: gancho de orden**). Cada dato con ≥ 2 fuentes (`guiones.md`). Voz oficial por API desde el Mac de Jorge (eleven_v4, 0.5/0.75, sin fallos). ≈40 SVG nuevos (`generadores/ilus_tarde.py`), montaje con `motor/denso.py` (28–35 planos), render en la nube. Portadas elegidas sin «ok» (pasos de `.claude/agents/portadas.md` hechos a mano). Fichas de variables creadas (en prueba). Vídeos y portadas en el chat y en el Mac (SHA iguales). Correo `1a1eaf34810f56dd`.
**Pruebas**: `motor.guion` ✓ ×3; `construir` sin ⚠ de lectura; `motor.calidad --mp4` 84/87/93 sin ❌ (⚠ justificados en `estado.md`); ffprobe 1080×1920/30 fps/h264/AAC 48 kHz; hojas cada 1 s revisadas y corregidas (03 tenía ❌ de ritmo → micro planos). No se tocó `motor/`.
**No hecho**: Studio no se abrió (sin lecturas nuevas en `studio.json`); experimento «plano real» sigue bloqueado (thumb.wikimedia.org). Sin publicar: falta el «ok».
**Créditos ElevenLabs**: quedan 28.812 de 40.000.
**Siguiente paso**: «ok» en https://claude.ai/code/session_019BG1dHf6SfJ6MbfA5kmnCP → publicar según AGENTE §8 desde el Mac de Jorge.

## 2026-11-17 16:30 — Nico — rama `main` — chat en la nube (móvil) «Framework de estudio»
**Encargo**: «un framework para un estudio súper minucioso, analítico y científico de la audiencia (edad, género, target) y de qué vídeos funcionan y por qué» y después «trabaja en el framework un rato largo».
**Hecho** (commit `f2dbc18` + el de esta entrada):
- `estadisticas/estudio/` (solo librería estándar): `ficha.py` (diccionario de 28 variables; 7 se calculan solas del guion y 4 de `calidad-NN.md`), `mediciones.py` (24 h, 48 h, 7 d, 28 d; lo guardado no se reescribe), `estadistica.py` (medianas, intervalo por remuestreo, Mann-Whitney por permutación, Spearman, tamaño de muestra, niveles), `analisis.py` (`datos/estudio.md`), `autopsia.py` (`datos/autopsias.md`), `experimento.py` (ficha previa, calendario, cierre), `informe.py` (semanal), `comentarios.py`, `recogida_extra.py` (audiencia por vídeo y comentarios), `README.md`.
- `estadisticas/fichas.json`: los 10 vídeos públicos. Tema, gancho y estructura copiados de `etiquetas.json` (se pusieron al publicar); el resto de subjetivas las puse yo **sabiendo ya los resultados** (marcadas `retrospectivo`).
- `recoger.py`: llama a `recogida_extra` dentro de un `try`. Workflow diario: paso nuevo `python3 estadisticas/estudio todo` (si falla, avisa y sigue).
- `AGENTE.md` §1 (leer `estudio.md`), §6 (ficha antes de entregar, **en prueba**) y §8 (unir la ficha con el id). `DECISIONS.md`, `TASKS.md`, `PROJECT_STATE.md`, aviso arriba en `motor/APRENDIZAJE.md`.
**Lo que dicen los datos hoy**:
- Solo 3 de 10 vídeos tienen lectura con 24 h o más y ninguno la de 48 h: **ninguna comparación pasa de «pista»**. Las «tendencias» de `aprendizajes.md` por tema, gancho o estructura salen de grupos de 1 o 2 vídeos.
- Audiencia de YouTube: 49 % con 35 años o más, 42 % en 18–34, 8 % en 13–17; 67 % hombres. España es el país que menos segundos ve por vista (10,6 s; Argentina 14,7 s). Es un dato del canal entero, sin controlar por vídeo: pista.
- Ejemplo de por qué hace falta el método: mezclando edades, «palabras del guion» correlaciona 0,97 con «se quedaron viendo» en 5 vídeos (p 0,03). No es que más palabras retengan: los guiones largos son los del método nuevo.
**Corrección a lo que dije en el chat**: los niveles que propuse primero (indicio = 5 por grupo y mismo sentido en dos redes) eran demasiado blandos. Simulando 90 vídeos sin ningún efecto real, la mitad de las comparaciones salían «indicio» y 7 de cada 10 estudios daban alguna «regla» falsa. Los actuales exigen p: 0 reglas falsas en 100 estudios simulados, 5 % de indicios falsos; un efecto real de 15 puntos llega a regla 8 de cada 10 veces con 90 vídeos.
**Pruebas**: `python3 estadisticas/estudio/prueba.py` → 113 de 113 (incluye simulaciones con y sin efecto, YouTube simulado y los datos reales). `python3 -m motor.prueba` → TODO BIEN (no se tocó `motor/` salvo el aviso en APRENDIZAJE.md). `recoger_youtube()` ejecutado entero con un YouTube simulado. **Sin probar**: `recogida_extra` contra la API real (puede que el permiso de solo lectura no deje leer comentarios; avisa y sigue) y el paso nuevo del workflow en GitHub Actions (primera vez: mañana ≈9:20).
**Pendiente** (en `TASKS.md`): público objetivo, confirmar la ficha en AGENTE, primer experimento, segundo codificador, mirar el registro del workflow de mañana, TikTok Studio «Espectadores», y si `analizar.py` adopta estos niveles.
**Siguiente paso**: que Nico y Jorge digan sí o no a la ficha en AGENTE §6 y elijan el primer experimento.

---

## 2026-11-17 11:30 — Jorge (chat del Mac de Jorge) — rama `main`
**Hecho**: lote 2026-11-17-manana («ok» de Jorge a los 3 en este chat) publicado en **TikTok** (7709083847450807574 · 7709084200636255510 · 7709084597069401366) e **Instagram** (Df1twcSx6JN · Df1uAQJxhjZ · Df1uQs9xjyt) desde el navegador integrado del Mac de Jorge; YouTube ya estaba (bja3TleMy94 · aA9ji1Y1EPA · 0LBq1SkOWz4). Los MP4 llegaron desde el chat de Nico por https://claude.ai/artifact/FSpWCbNW59fpYPe46bZ2CH (partes unidas, SHA-256 igual al de `estado.md`). Comentarios en TikTok e Instagram (sin fijar). `estadisticas/etiquetas.json` con los 3.
**Aprendido**: en Instagram web, pulsar «Compartir» con clic real conserva el texto (por script se perdía) → AGENTE §8.
**Pendiente**: comentarios de YouTube de este lote (no se hicieron desde aquí).

## 2026-11-17 10:30 — Nico — rama `main` — chat en la nube «API de TikTok e Instagram» (Nico en el trabajo, sin nadie delante)
**Encargo**: «vamos a hacerlo, porque si no no podemos subirlo» → publicar en TikTok e Instagram por sus API oficiales (gratis).
**Hecho** (commit `6cae883` + el de esta entrada):
- `publicar/subir_instagram.py`: Reel por la API de Meta. Sube el archivo desde el Mac (Facebook Login, `rupload`) o por dirección pública (Instagram Login). Texto, portada por fotograma (`portada.t`), comentario opcional. Retoma envíos a medias y no duplica.
- `publicar/subir_tiktok.py`: Content Posting API en modo Upload: deja el vídeo como borrador en la bandeja de entrada y devuelve el texto para pegarlo en el móvil. `--estado` da el enlace cuando la persona publica. Guarda en `claves.txt` el token que TikTok cambia en cada uso.
- `publicar/autorizar_tiktok.py` y `autorizar_instagram.py` (permiso de una vez; no enseñan tokens), `publicar/base.py` (claves, HTTP, registro `publicado.json`, comprobación del MP4).
- `publicar/README.md` reescrito: qué puede y qué no puede cada API, puesta en marcha paso a paso, uso por el agente. `AGENTE.md` §8 punto 3b (solo se usa la API si `--prueba` dice que la red está activada; si no, navegador como siempre: el lote de las 20:00 no cambia). `DECISIONS.md`, `TASKS.md`, `PROJECT_STATE.md`.
**Lo importante que salió de la documentación oficial**:
- TikTok no deja publicar del todo: sin auditoría solo en privado, y no audita herramientas internas. Lo máximo es el borrador + terminar en el móvil. Además, el texto no viaja con el borrador.
- Instagram sí publica del todo y sin revisión de Meta para una cuenta propia. Valen cuentas de creador (corrijo lo que dije en el chat: no hace falta pasarla a empresa).
- Con la app de las estadísticas (Instagram Login) el vídeo tendría que estar en una URL pública; con Facebook Login + página enlazada se sube el archivo. Por eso se recomienda esa.
- El token de TikTok rota: hace falta un sandbox propio por Mac, aparte del de las estadísticas.
**Pruebas**: `python3 publicar/prueba.py` → 31 de 31, en Python 3.13 y 3.9 (servidor falso en 127.0.0.1 con las reglas de las dos API: rotación de token, trozos, reintentos, respuestas perdidas, límites, no duplicar). Comprobador de MP4 probado con archivos reales de ffmpeg. Textos de todos los lotes dentro de los límites de Instagram.
**No hecho / no verificado**: ninguna llamada a TikTok ni a Meta de verdad (sin cuentas de desarrollador y sin red hacia ellas desde la nube). No se sabe si TikTok deja publicar en público un borrador enviado desde un sandbox: lo decide la prueba del paso 9 del README. Nada publicado, ninguna cuenta tocada, ningún gasto.
**Pendiente (personas)**: registro en Meta for Developers + página de Facebook + app (Instagram); sandbox «Publicar Nico» + prueba real (TikTok); dominios permitidos. Todo en `TASKS.md`.
**Siguiente paso**: Instagram primero (es la que queda 100 % automática). Empezar por desbloquear el registro en Meta for Developers.

## 2026-11-17 08:55 — Agente 08:00 (Nico) — rama `main` — lote 2026-11-17-manana
**Hecho**: lote `2026-11-17-manana`, 3 vídeos v1 en revisión, primer lote automático con el método denso: 01 «Este plátano es radiactivo» (Ciencia, experimento), 02 «Saturno flotaría en el agua» (Espacio, comparación, control), 03 «Esta huella no es humana» (koala; Misterio, misterio por pistas; **experimento: gancho de negación**). Cada dato con ≥ 2 fuentes (`guiones.md`); la miel egipcia se descartó por ser un mito. Voz oficial por API desde el Mac (eleven_v4, 0.5/0.75, sin fallos). 37 SVG nuevos (`generadores/ilus_lote.py`), montaje con `motor/denso.py` (38–39 planos por vídeo, 6–11 micro planos), render en la nube. Portadas elegidas sin «ok» (pasos de `.claude/agents/portadas.md` hechos a mano). Vídeos y portadas en el chat y en el Mac (SHA iguales). Correo `1a1e86caf2a125ea`.
**Pruebas**: `motor.guion` ✓; `construir` sin ⚠ de lectura; `motor.calidad --mp4` 92/90/100 sin ❌ (⚠ justificados en `estado.md`); ffprobe 1080×1920/30 fps/h264/AAC 48 kHz; −19,1/−19,2/−19,1 LUFS; hojas cada 1 s revisadas y corregidas (2.ª vuelta de render).
**No hecho**: experimento «plano real» (Openverse en el Mac → 403 en `thumb.wikimedia.org`; TASKS). Studio no se abrió (nada nuevo con ≥ 24 h desde la lectura de las 00:25). Sin publicar: falta el «ok».
**Créditos ElevenLabs**: quedan 29.828 de 40.000.
**Siguiente paso**: «ok» en https://claude.ai/code/session_019BG1dJfghaKYErZsy5CyPu → publicar según AGENTE §8 desde el Mac de Nico.

## 2026-11-17 02:45 — Nico — rama `main` — chat en la nube «Luna densa» (4.ª ronda nocturna)
**Hecho**: comprobación de mis propias hipótesis con más datos (`motor/APRENDIZAJE.md`): H1 y H2 rebajadas, H9 sin apoyo, **H7 reforzada** (movimiento del primer segundo: 23,5 en Shorts con más de 100.000 vistas, 13,8 en los de ~2.000; los nuestros, 1,6–15,2). Curvas de retención reales de TikTok Studio (`estadisticas/tiktok_studio.json`, `herramientas/tiktok_retencion.js`): se pierde el 40 % en 3 s. Lo oficial del algoritmo con fuentes. H6 (personaje) descartada por Nico → quitada del motor y apuntada en DECISIONS.
**Motor**: `calidad` ❌ si el primer segundo está quieto; `guion` avisa si la afirmación tarda más de 3,5 s; `denso.arranque()`; `omitir=` también para micro-Shorts; Luna v8 y micro de 8 s. AGENTE §2 «prueba del primer segundo»; `IDEAS.md` con ganchos propuestos.
**Pruebas**: renders completos de v8, v8 palabra y micro; `motor.calidad --mp4` 100/100 los tres; primer segundo 5,5 (v7: 3,0).
**No hecho a propósito**: nada publicado ni gastado.
**Siguiente paso**: lote 2026-11-17-manana cuidando sobre todo el primer segundo. Reporte: `REPORTE_NOCHE_2026-11-17.md` §6.

## 2026-11-17 02:00 — Nico — rama `main` — chat en la nube «Luna densa» (3.ª ronda nocturna)
**Hecho**:
- **Hallazgo principal** (`motor/APRENDIZAJE.md`): en nuestros 5 vídeos, palabras del gancho en el fotograma 0 → «se quedaron viendo»: 1 → 80 %, 3 → 74 %, 10 → 60 %, 13 → 47 %, 14 → 32 %. Regla nueva en AGENTE §3 (primera frase ≤ 5 palabras, un objeto grande en acción) y en `motor.calidad` (❌ a partir de 10 palabras; ⚠ si el primer segundo no se mueve).
- 2.ª lectura de Studio (01:37), 4 Shorts de referencia más (8 de 11 con subtítulo de 1–3 palabras), 383 títulos del nicho (mediana 73 vistas; el título no explica las vistas).
- Motor: `Video(..., omitir=[(i0, i1)])` hace una versión corta con la misma locución (H2); personaje con 6 expresiones `pj_*.svg` + `denso.reaccion()` (H6); arreglado un fallo mío de la 2.ª ronda (el modo «palabra» no escribía el `.srt` ni el manifiesto).
- Luna v7: gancho rehecho; variantes `palabra`, `corta` y las dos juntas como 4.º/5.º argumento de `gen.py`.
**Pruebas**: 4 renders completos (54,9 s y 35,3 s), `motor.calidad --mp4`: 100/100 las largas, 91/100 las cortas (al cortar se pierden micro planos). Empalmes de audio de la versión corta en silencio digital (−87 dB), **sin oír**.
**No hecho a propósito**: nada publicado ni gastado. No he cambiado DECISIONS para H1/H2/H6: son de Nico y Jorge.
**Pendiente**: curva de retención (YouTube aún no la da); decisiones en TASKS.
**Reporte completo de las tres rondas**: `REPORTE_NOCHE_2026-11-17.md` (raíz del repo). `python3 -m motor.guion` añadido a AGENTE §3.
**Siguiente paso**: lote 2026-11-17-manana con la regla del gancho de 5 palabras.

## 2026-11-17 01:00 — Nico — rama `main` — chat en la nube «Luna densa» (2.ª ronda nocturna, pedida por Nico: «más tiempo, más exigente, aprende a aprender»)
**Hecho**:
- `motor/APRENDIZAJE.md`: rutina de aprendizaje + datos reales de Studio (se quedaron viendo / vistas / s por vista de 7 vídeos) + 7 Shorts del nicho con hasta 15 M de vistas mirados fotograma a fotograma (`herramientas/hoja_short.js`) + hipótesis H0–H5. `estadisticas/studio.json` actualizado. AGENTE §1 lo manda leer.
- Hallazgos (pistas): las vistas siguen a «se quedaron viendo»; Luna densa 73,3 % frente a 65,3 % del v4; nadie ve más de ~28 s de media; los referentes usan subtítulo de 1–2 palabras enormes y duran 18–35 s.
- Motor: subtítulo modo «palabra» (`subtitulos="palabra"`), rótulos que se apartan del subtítulo, `fijo=True`.
- `motor/calidad.py` más exigente con el MP4: planos pobres, planos calcados, mismo encuadre > 4,5 s, contraste de rótulos. Publicado 54 · v5 83 · v6 100.
- Luna v6 (`lotes/prueba-luna-densa/gen.py`): 6 planos flojos rehechos. Variante palabra: añadir `palabra` como 4.º argumento.
- DECISIONS: control de calidad y montaje tipo v5/v6 obligatorios desde el lote 2026-11-17-manana.
**Pruebas**: render completo de v6 y v6-palabra (1080×1920, 30 fps, 54,9 s), `motor.calidad --mp4` 100/100 en los dos, hojas revisadas.
**No hecho a propósito**: nada publicado, ningún crédito de voz gastado. Los referentes se miraron sin sonido.
**Pendiente**: que Nico/Jorge decidan H1 y H2 (TASKS); % medio visto de la Luna el 2026-11-19.
**Siguiente paso**: lote 2026-11-17-manana con AGENTE §1 (aprender) y §6 (calidad).

## 2026-11-17 00:30 — Nico — rama `main` — chat en la nube «Luna densa» (trabajo nocturno, sin nadie delante)
**Hecho** (commits `f39c380`, `2f9afeb`, `0f35102` y el de esta entrada):
- `motor/GUIA_CALIDAD.md`: investigación con fuentes (métricas de Shorts, gancho y curiosidad, principios de Mayer, tipos de plano y de estructura, movimiento, zonas seguras, sonido, música, bucle, Python) convertida en reglas y lista de control. También como doc del Proyecto de Claude.
- `motor/calidad.py`: nota 0–100 y avisos ❌/⚠/ℹ (ritmo, zona segura, lectura, gancho, sonido; con `--mp4`: movimiento, bucle, mezcla). Añadido a AGENTE §6 y DENSO.
- Motor: caché en disco de SVG (`.raster/`, ignorada) + `--procesos` → el vídeo de 55 s se renderiza en ~2 min; easings `elastico/bote/anticipa/golpe/expo`; efectos `subida/impacto/roce/burbuja`; música con curva de energía y final que enlaza; `bucle=` en `construir`; zona segura automática; `sin_pop`; helpers `aparece/cae/lanza/late/sigue/senala`.
- `lotes/prueba-luna-densa/gen.py` → v5 con todo eso (misma voz, sin gastar créditos).
**Pruebas**: calidad v4 antiguo ≈23 · Luna publicada 71 · Luna v5 100/100 con MP4 (1,6 % de tiempo quieto, 0 rótulos fuera de zona). Paralelo frente a un proceso: mismos fotogramas (PSNR 47,7 dB).
**No hecho a propósito**: no se ha publicado nada ni se ha gastado en voz. No he podido ver ni oír vídeos de terceros: la guía lo dice.
**Pendiente**: decisiones de GUIA_CALIDAD §10 (TASKS); apuntar estadísticas de retención.
**Siguiente paso**: lote 2026-11-17-manana con `motor.calidad` en el control; Nico ve la v5 con sonido y dice si la música y los efectos nuevos le gustan.

## 2026-11-17 00:25 — Agente 20:00 (Jorge) — rama `main` — aviso programado en el chat del lote
**Hecho**: YouTube 02 (cTRgkuY21mw) y 03 (hfRveipHIdk) públicos a su hora. Comentarios escritos en todas las publicaciones del lote 2026-11-16-tarde (YouTube 1–3, TikTok 1–3, Instagram 1–3), sin fijar. Antes (22:50) se añadieron las descripciones que faltaban en los 3 Reels de Instagram.
**Pendiente**: verificar el canal de YouTube para poder fijar comentarios (TASKS).
**Siguiente paso**: lote 2026-11-17-manana (Nico).

## 2026-11-16 22:35 — Agente 20:00 (Jorge) — rama `main` — chat del lote (Mac de Jorge)
**Hecho**: «ok» de Jorge a la v2 → publicado desde el navegador integrado (Jorge eligió cada archivo; copias aprobadas en `PARA PUBLICAR/2026-11-16-tarde/Vídeos` y `/Portadas`).
- YouTube: 01 https://youtube.com/shorts/7PoER_sR6R0 (público 22:12) · 02 cTRgkuY21mw (programado 23:15) · 03 hfRveipHIdk (programado 00:15). Miniatura: fotograma elegido en Studio (subir imagen no le funcionó a Jorge).
- TikTok: 7708881722745703702 · 7708882083015413014 · 7708882489892179222. Instagram: Df0UCk8RMdf · Df0UQzOxS49 · Df0Uzrsxo0A (el 03 hubo que repetirlo: el primer «compartido» no llegó al perfil).
- **Decisión de Jorge**: sin fuentes en las descripciones de ninguna red (DECISIONS/AGENTE actualizados; quitadas también de los 3 de YouTube). En TikTok los enlaces hacían saltar «Content may be restricted».
- `estadisticas/etiquetas.json` con los 3 (YouTube + TikTok + Instagram).
**Pendiente**: fijar comentarios en YouTube requiere verificar el canal (teléfono) → TASKS. Comentarios de TikTok 02/03 e Instagram: aviso en este chat a las 00:20.
**Siguiente paso**: lote 2026-11-17-manana (Nico) ya con «sin fuentes» en las descripciones.

## 2026-11-16 21:45 — Agente 20:00 (Jorge) — rama `main` — chat del lote (Mac de Jorge)
**Hecho**: Jorge dio «ok» a la v1 y enseguida pidió no subirla y rehacerla con el método «denso» (DECISIONS de Nico). No se publicó nada (comprobado en Studio). v2 de los 3 vídeos con el mismo audio: `lotes/2026-11-16-tarde/generadores/denso.py` (módulo reutilizable del método de la Luna: planos por palabra, control de lectura, detalles persistentes, neón, sonido bajo, música −13 dB) + `gen_0N_v2.py` + `ilus_extra.py`. 37/34/33 planos. Vídeos y portadas v2 en el chat y en el Mac.
**Pruebas**: ffprobe y LUFS OK; control de lectura OK; hojas cada 1 s revisadas.
**Bloqueo para publicar**: el Mac de Jorge no tiene `YT_UPLOAD_REFRESH_TOKEN` → YouTube por navegador (tarea nueva en TASKS).
**Siguiente paso**: «ok» a la v2 → publicar (AGENTE §8). `denso.py` puede servir de base para la biblioteca del motor que Nico tiene pendiente.

## 2026-11-16 21:35 — Nico — rama `main` — chat en la nube (Mac de Nico)
**Hecho**: «La Luna se nos va… y se llevará los eclipses 🌑» (método denso, con voz) **publicado en las 3 redes** con el «ok» de Nico; enlaces en `lotes/prueba-luna-densa/estado.md`. El vídeo antiguo de la Luna (02 del 2026-11-15-tarde): YouTube en privado y TikTok en «Solo yo». Excepción de tema repetido en `DECISIONS.md`. Portada elegida con `motor.portadas`.
**Aprendido**: el token de YouTube (`youtube.upload` + `readonly`) no deja cambiar la visibilidad por API: se hace en Studio (radio `PRIVATE` → Hecho → Guardar). En TikTok Studio → Publicaciones se cambia la privacidad desde el desplegable de cada fila (no hace falta el móvil). Instagram en la app de Claude sale en formato móvil: «+» abajo abre el selector directamente.
**Pendiente**: reel antiguo de Instagram `Dfx5sljx4kO` (decide Nico: borrar o archivar desde el móvil); comentario fijado en YouTube y TikTok.
**Siguiente paso**: lote 2026-11-17-manana, primero con el método denso.

## 2026-11-16 21:20 — Nico — rama `main` — chat en la nube (Mac de Nico)
**Hecho (método denso aplicado a los lotes)**:
- `motor/denso.py`: clase `Video` (planos atados a palabras, control de lectura, halo neón, pop/whoosh/tic automáticos), `recorrido`, rótulos, piezas hechas, `provisional`. `python3 -m motor.denso guion.txt` lista los índices de palabra.
- `motor/biblioteca/`: `svg/` (ilustraciones fijas del v4) + `ilus.py` (todas las generadas de la Luna y los ladrillos para dibujar nuevas).
- `motor/DENSO.md`: guía con pasos, reglas y control. `AGENTE.md` §3/§5: método denso obligatorio, 150–160 palabras, «mejor 2 vídeos bien hechos que 3 flojos». README del motor actualizado.
- `lotes/prueba-luna-densa/gen.py` reescrito sobre la biblioteca (ejemplo para copiar); `provisional.py` e `ilus_luna.py` del lote ya no hacen falta.
**Pruebas**: el `episodio.json` de la Luna generado con la biblioteca es **idéntico** al anterior (comparación campo a campo); los 28 SVG generados son idénticos byte a byte; montaje sin voz (provisional) y hoja OK.
**Ojo**: el primer lote automático con este método es el 2026-11-17-manana: revisar con lupa (ilustraciones de temas nuevos y tiempo del turno).
**Publicación**: ver la entrada siguiente / `lotes/prueba-luna-densa/estado.md`.

## 2026-11-16 20:50 — Nico — rama `main` — chat en la nube (Mac de Nico)
**Decisión**: Nico pide dejar en `DECISIONS.md` el método «denso» (prueba de la Luna) como estándar de los vídeos: planos atados a palabras, duración variable, micro escenas, tiempo de lectura, detalles de fondo que duran, figuras y fondos detallados, neones sobre oscuro, sonido de detalle bajo y música presente. Sustituye la regla de «un plano por frase» del v4.
**Ojo**: `AGENTE.md` y el motor aún no lo aplican; los lotes automáticos siguen como antes hasta hacer la biblioteca y reescribir el manual. Falta que Jorge lo vea.
**Siguiente paso**: biblioteca en `motor/` + `AGENTE.md`.

## 2026-11-16 20:35 — Nico — rama `main` — chat en la nube (Mac de Nico)
**Hecho**: a Nico le sonaba demasiado el «shhh» de los cambios de plano y poco la música. En `lotes/prueba-luna-densa/gen.py`: el whoosh automático de transición solo suena si han pasado ≥ 5 s desde el anterior y a −24 dB (antes en todas, a −15); fuera los whoosh pequeños repetidos; los demás 9 dB más bajos (29 → 14 en total). Música de −17 a −13 dB.
**Pruebas**: render 54,9 s, −19,1 LUFS. No escuchado desde la nube.
**Para el estándar**: regla «whoosh, pocos y bajos; la música se tiene que oír» cuando se pase el método a `AGENTE.md`.

## 2026-11-16 20:30 — Agente 08:00 (Nico) — rama `main` — lote 2026-11-16-manana
**Hecho**: lote `2026-11-16-manana`. La tarea programada de las 07:52 se disparó a las 19:48 hora de Madrid. Tres vídeos v1 en revisión:
- 01 · Todos los planetas caben entre la Tierra y la Luna (Espacio, comparación, contraste).
- 02 · El pulpo tiene tres corazones y sangre azul (Ciencia, metáfora visual; **experimento: gancho de negación**).
- 03 · Los vikingos llegaron a América en 1021 (Histórico, reconstrucción, contraste).
Cada tema contrastado con dos fuentes. Guiones de 133–139 palabras con cifras en letra (`lotes/2026-11-16-manana/guiones.md`), metadatos con comentario fijado, portada y etiquetas. Ilustraciones SVG nuevas en el estilo v4 (`generadores/ilus_m.py`) y montaje por planos (`gen_0N.py`) con gancho en el fotograma 0. Portadas elegidas sin «ok» (§6b, hecho a mano en lugar del subagente). Vídeos enviados al chat y copiados al Mac de Nico (el SHA coincide). Correo único `1a1e5cd4c9bf08da`.
**Voz**: la v1 dio 404 porque se borró hoy (`d377b17`, llegó a mitad del turno). Se usó la voz oficial nueva de DECISIONS (clon `op8soO9fvP07F3mjbJuB`, `eleven_v4`). ≈2.330 caracteres; quedan ≈30.800.
**Pruebas**: ffprobe (1080×1920, 30 fps, h264/AAC 48 kHz), −19,1 a −19,3 LUFS, hojas de fotogramas del MP4 revisadas. Correcciones antes de entregar en `estado.md`.
**No hecho**: datos de Studio (studio.json ya tenía los de hoy). Sin publicar: falta el «ok».
**Pendiente**: actualizar el texto de la tarea programada de las 08:00 (voz v1 y Drive; TASKS). Con «ok», publicar según AGENTE §8 desde el Mac de Nico.
**Siguiente paso**: esperar el «ok» en https://claude.ai/code/session_019BG1dHPaoMtT9aEtopJ3JF

## 2026-11-16 20:10 — Nico — rama `main` — chat en la nube (Mac de Nico)
**Hecho**: «Luna densa» montada con la **voz oficial nueva** («Archivo Oculto — Narración (clon)», `eleven_v4`, 0.5/0.75). Locución por API desde el Mac de Nico (`with-timestamps`, 822 caracteres; contador de la cuenta antes: 7.804 / 40.000). MP3 y alineación en `~/Documents/Parece Mentira/lotes/prueba-luna-densa/` (`luna-densa-locucion.mp3`, `luna-densa-alineacion.json`), y el vídeo final ahí también.
- La voz dura **54,4 s** (el provisional estimaba 47): los 40 planos se recolocaron solos sobre las palabras. `gen.py`: las ventanas de los satélites, los pterosaurios y el meteorito lejano ahora también van atadas a palabras (`SAT`, `T_DINO0/1`), no a segundos fijos; activado `"gancho": true`.
**Pruebas**: hoja de fotogramas cada 1,3 s revisada; 54,9 s, −19,1 LUFS, pico −4,4 dBFS; control de lectura OK. No escuchado (en la nube no se puede): falta el oído de Nico/Jorge para voz, ritmo y volumen de efectos.
**Siguiente paso**: «ok» o cambios; si gusta, pasar el método a `AGENTE.md` y hacer biblioteca.

## 2026-11-16 20:25 — Agente 20:00 (Jorge) — rama `main` — tarea programada (Mac de Jorge)
**Hecho**: lote **2026-11-16-tarde** (prueba de temas cotidianos, temas reservados en IDEAS): 01 crujirse los nudillos (Unger 60 años + resonancia 2015, 57,7 s), 02 las puertas te hacen olvidar (Radvansky 2011, 54,7 s), 03 el móvil y el ordenador del Apolo 11 (51,9 s). Voz clonada `op8soO9fvP07F3mjbJuB` con `eleven_v4` desde `claves.txt` del Mac (sin fallos). Estilo v4 con ilustraciones nuevas (`lotes/2026-11-16-tarde/generadores/`), gancho en el fotograma 0, 18–20 planos por vídeo, efectos de sonido. Portadas elegidas por el agente (§6b, sin subagente: no está en la sesión programada, pasos hechos a mano). Vídeos y portadas enviados al chat; correo `1a1e5cb7121de9d1`. Archivos en `Documents/Parece Mentira/lotes/2026-11-16-tarde/`.
**Pruebas**: ffprobe 1080×1920/30 fps/h264/AAC 48 kHz; −19,2/−19,0/−19,4 LUFS; hojas de fotogramas y fotogramas del MP4 revisados; SHA del Mac = SHA del render. Datos contrastados con 2–3 fuentes por vídeo (`guiones.md`).
**No hecho**: Studio (`studio.json` ya tenía hoy los 4 Shorts). El lote 2026-11-16-manana sigue «En curso» de Nico: no se ha tocado.
**Pendiente**: «ok» en el chat del lote → publicar según AGENTE §8 (YouTube por API con 1 h entre vídeos; TikTok e Instagram seguidos).
**Siguiente paso**: revisar los 3 vídeos y decidir el 2026-11-17 si la mezcla cotidiana se queda.

## 2026-11-16 19:55 — Nico — rama `main` — chat en la nube (Mac de Nico)
**Hecho**: voz oficial cambiada. La voz «Archivo Oculto — Narración» de la cuenta antigua de ElevenLabs (plan Free, Voice Design: no se puede compartir ni copiar) se ha clonado (clon instantáneo) en la cuenta nueva con las 9 locuciones originales que había en Descargas del Mac de Nico (unidas en `VOZ_ARCHIVO_OCULTO_para_clonar.mp3`, 4 min 53 s) → «Archivo Oculto — Narración (clon)», voice_id `op8soO9fvP07F3mjbJuB`. Borrada la v1 «Narrador PM - Curiosidades v1» (`EuJOG4WNDCMcwTFrXKUc`) a petición de Nico. A la clave «Parece Mentira - Nico» (…076b) se le dio el permiso Voces → Escribir. `claves.txt` del Mac de Nico actualizado (copia anterior en `claves.txt.bak`). AGENTE §4, DECISIONS y PROJECT_STATE actualizados: modelo `eleven_v4`, estabilidad 0.5, similitud 0.75 (antes los lotes usaban `eleven_multilingual_v2`).
**Pruebas**: TTS con el clon y `eleven_v4` → HTTP 200 (`Downloads/PRUEBA_clon_archivo_oculto.mp3`); `with-timestamps` con `eleven_v4` → audio + alineación OK.
**Pendiente**: Jorge debe cambiar `ELEVENLABS_VOICE_ID` en el `claves.txt` de su Mac (TASKS).
**Siguiente paso**: lote 2026-11-17-manana ya con la voz nueva.

## 2026-11-16 19:45 — Nico — rama `main` — chat en la nube (Mac de Nico)
**Hecho**: Nico ejecutó en su Terminal `estadisticas/autorizar.py --subir` → `YT_UPLOAD_REFRESH_TOKEN`, `YT_CLIENT_ID` y `YT_CLIENT_SECRET` en `/Users/nico/Documents/Parece Mentira/claves.txt`. El Mac de Nico ya puede subir a YouTube por API en el lote de las 08:00.
**Pruebas**: `subir_youtube.py --prueba` desde el Mac de Nico (metadatos del lote 2026-11-15-tarde, vídeo 02, archivo vacío): token canjeado y canal consultado sin errores, no se subió nada. Ojo: no detectó como «yaEstaba» el título de la Luna; puede que el título publicado sea distinto. Revisar en la primera subida real que no duplica.
**Seguridad**: Nico pegó todas las claves de `claves.txt` en el chat (incluidas `GH_PAT` y la de ElevenLabs). Se le recomendó rotarlas; él dijo que no importa.
**Siguiente paso**: lote 2026-11-17-manana con subida por API tras el «ok».

## 2026-11-16 19:40 — Nico — rama `main` — chat en la nube (Mac de Nico)
**Hecho**: el Mac de Nico no tenía código del repo (solo `claves.txt`, `lotes/`, `renders/`, `referencias-objetivo/`). Copiados a `/Users/nico/Documents/Parece Mentira/` los scripts que tienen que correr en el Mac del turno de las 08:00: `publicar/` (subir_youtube.py), `motor/` (openverse.py, portadas.py…) y `estadisticas/autorizar.py`, desde `main` commit `f47be02` (anotado en `VERSION_COPIA.txt`). El .tgz usado quedó en `_to_delete/` (borrar a mano).
**Pruebas**: `subir_youtube.py --prueba` corre en el Mac de Nico y dice que faltan `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_UPLOAD_REFRESH_TOKEN` (esperado).
**Pendiente**: pegar esas 3 líneas desde el `claves.txt` del Mac de Jorge (TASKS). Hasta entonces, el lote de las 08:00 sube YouTube por el navegador (AGENTE §8 ya lo prevé).
**Siguiente paso**: con las claves pegadas, repetir `--prueba` con un título ya publicado → `yaEstaba`.

## 2026-11-16 19:35 — Nico — rama `main` — chat en la nube
**Hecho**: «Luna densa» v6 (correcciones de Nico).
- **Flechas hacia la Luna**: la Luna va siempre por delante y la punta acaba antes de su borde (planos «la Luna se aleja», pantalla partida, 1.400 y 600 millones de años). Regla para el futuro: una flecha nunca termina dentro del objeto al que sigue.
- **Contraste sobre fondos oscuros**: paleta neón en `gen.py` (`CIAN`, `MAGENTA`, `LIMA`, `AMBAR`) para flechas, órbitas, rótulos y bordes en los planos de espacio; el bucle de montaje añade solo un halo (copia ancha y translúcida) a cada flecha y órbita.
- **Sonidos** (`motor/sfx.py`): `tictac` (tic agudo / tac grave alternos, para los relojes), `agua` (ola + espuma + burbujas, sustituye a `ola` en las mareas) y `mordisco` rehecho (chasquido, rasgado de hoja y dos masticadas, más agudo y crujiente).
**Pruebas**: 12 fotogramas revisados; render 48,3 s; niveles medidos (no escuchado: en la nube no hay forma de oírlo).
**Pendiente**: que Nico confirme de oído tictac, agua y mordisco.

## 2026-11-16 19:10 — Nico — rama `main` — chat en la nube
**Hecho**: «Luna densa» v5 (ideas de Nico).
- **Sonidos nuevos en `motor/sfx.py`**: `senal` (pitidos de satélite con eco), `fugaz` (soplo de estrella fugaz), `trazo` (tic blando por raya), `mordisco`, `meteoro` (rugido tipo cohete que crece). En `gen.py` son automáticos y bajos: `flecha(..., disc=...)` pone un tic por raya mientras se dibuja (máx. 8, tono que sube, −27 dB); `fugaz()` pone su sonido (−25 dB, con paneo); los satélites suenan al entrar en un plano donde se ven, como mucho cada 2,6 s (−28 dB).
- **Dinosaurios comiendo**: el braquiosaurio se queda quieto junto a una rama (`comer()`): cabecea, la rama pierde un bocado (`rama_hojas` → `rama_mordida1/2`), caen trocitos de hoja y suena el mordisco; el triceratops muerde un arbusto. Reloj y calendario más pequeños y a la derecha para que se vea la escena.
- **Meteorito** (`meteorito.svg`: roca con cráteres y grietas incandescentes, frente al rojo blanco, cola de fuego en capas, chispas): se ve pequeño y lejano acercándose durante los tres planos de dinosaurios (`meteoro_lejos`, tiempo absoluto) y cae en un micro plano nuevo (palabra 103, 0,8 s) con temblor, cielo que se enciende, fogonazo blanco y fundido desde blanco a la almeja fósil. Sonido: `meteoro` + `golpe` + `rumor`.
**Pruebas**: 12 fotogramas del tramo 26–32 s revisados; render 48,3 s, −19,5 LUFS, pico −1,1 dBFS; 40 planos, 176 efectos; control de lectura OK.
**Pendiente**: el reloj tapa un poco la rama en el plano de las 23,5 h; oírlo con la voz real para ajustar volúmenes.

## 2026-11-16 19:30 — Nico (en el Mac de Jorge) — rama `main`
**Hecho**: Nico permitió los 5 dominios. Prueba real de `motor/openverse.py`: 401 → Openverse sin cuenta no deja más de 20 por página (arreglado); Openverse da enlaces de Commons como `?curid=` (ahora se comprueban por `pageids`); desde la nube Wikimedia responde 429 (red compartida) → reintentos con espera y, sobre todo, **se ejecuta en los Macs**. En el Mac de Jorge (`~/Documents/Parece Mentira/_prueba-openverse/`, carpeta de prueba que se puede borrar): «moai easter island» → moái real con torso del Smithsonian, **CC0 comprobado en Commons, sin restricciones**, descargado, `creditos.json` con SHA-256 y crédito corto (`?curid=`). Revisión visual: sin personas ni logotipos, escultura antigua. Regla nueva: nada de fotos de obras modernas (salió una escultura de Lego con foto CC BY: la licencia de la foto no cubre la obra).
**Pruebas**: `prueba_openverse.py` OK; ciclo completo en el Mac (buscar → comprobar → descargar → créditos).
**Siguiente paso**: el lote de mañana 08:00 puede probar «plano real» (AGENTE §5b).

## 2026-11-16 19:25 — Nico — rama `main`
**Hecho**: Nico aprueba probar Openverse «siempre que no afecte a monetizar». `motor/openverse.py`: busca en Openverse solo PD/CC0/CC BY de Wikimedia Commons y el Met; **comprueba cada imagen en la fuente original** (API de Commons: licencia, plantilla, restricciones como derechos de imagen o marca, dominio público solo de EE. UU.; API del Met: `isPublicDomain`), descarga a `<lote>/reales/` y apunta todo en `<lote>/creditos.json` (licencia comprobada, fecha, SHA-256, uso, revisión visual); `creditos` da el texto para las descripciones. AGENTE §5b (cuándo y cómo: máx. 2 planos y ≤ 20 % del vídeo, siempre animados y narrados por la política de contenido reutilizado de YouTube; créditos en las 3 redes; sin personas reales ni logotipos; sin audio de Openverse). DECISIONS: excepción en prueba al estilo solo ilustrado.
**Pruebas**: `motor/prueba_openverse.py` (13 casos sin red: PD mundial/solo EE. UU., NASA, CC BY 2.0/4.0, CC0, SA, NC, restricción de derechos de imagen, Met sí/no, criba de Openverse, texto de crédito) → todo OK. **Sin probar contra las APIs reales**: el entorno de Claude no llega a esos dominios, y la consulta desde el navegador integrado la bloqueó el control de permisos (no se intentó otra vía).
**Pendiente**: permitir los 5 dominios (TASKS) y una primera prueba real.
**Siguiente paso**: con los dominios permitidos, `python3 -m motor.openverse buscar "nuremberg 1561"` y revisar que la comprobación en Commons da lo esperado.

## 2026-11-16 19:05 — Nico — rama `main`
**Hecho**: a petición de Nico, las portadas ya no necesitan «ok». Subagente nuevo `.claude/agents/portadas.md`: escribe el texto de portada (2–5 palabras) y una variante, genera 8 candidatas con `motor.portadas`, mira las hojas, elige con criterios fijos (sujeto grande y reconocible, texto que no lo tapa, legible en 3:4, coherente con el primer segundo; desempate hacia el diseño menos probado salvo que las estadísticas ya digan cuál va mejor), lo registra con motivo y lo apunta en `metadatos.json`. AGENTE §6b (lanzar el subagente para los 3 vídeos a la vez; si no está disponible, mismos pasos a mano), §7 (se manda `portada.jpg` al chat y la portada va en el correo como información). DECISIONS: tachado «el ok aprueba también las portadas». Los vídeos siguen necesitando «ok» (CLAUDE.md).
**Pruebas**: solo documentación y flujo; el script ya estaba probado (entrada de las 19:10). Sin comprobar si la tarea programada carga los subagentes del repo (por eso el plan B a mano).
**Pendiente**: Openverse (TASKS).
**Siguiente paso**: ver en el próximo lote que llega la portada elegida al chat.

## 2026-11-16 19:10 — Nico — rama `main`
**Hecho**: `motor/portadas.py`: 4 portadas candidatas por vídeo (fotogramas distintos, sin rótulos ni HUD del vídeo; texto de 2–5 palabras arriba / centro / abajo / dato en cápsula amarilla, siempre dentro del recorte 3:4 de las cuadrículas), `hoja-portadas.jpg` con la vista de cuadrícula, `portadas.json` con puntuación (color, detalle, tamaño del sujeto, texto que no lo pisa, legibilidad a 180 px). La puntuación solo ordena: en la prueba eligió mal 2 de 3 (caracol en vez de astronauta; moái tapado), así que la elección final es visual con `--elegir DIR N --motivo` → `portada.jpg`. `subir_youtube.py`: `--portada` (thumbnails.set con reintentos; si el canal no puede, lo dice y sigue) y `--solo-portada <id>`. AGENTE §6b (cómo hacerlas y elegirlas), §7 (hoja en el chat; el «ok» aprueba portadas), §8 (YouTube/Instagram/TikTok), etiqueta `portada`; `analizar.py` compara por diseño de portada. DECISIONS: decisión nueva. Portadas del lote 2026-11-15-tarde hechas y elegidas (01 dato · palacio y barcos; 02 abajo · astronauta y Tierra; 03 abajo · moái con el cuerpo enterrado), apuntadas en su `metadatos.json` (imágenes fuera de git, enviadas al chat de Nico).
**Pruebas**: portadas de los 3 vídeos del lote 2026-11-15-tarde regeneradas desde sus generadores v4 (~18 s por vídeo); `subir_youtube.py` comprobado solo en los errores de argumentos (sin claves en la nube: la llamada real a thumbnails.set no se ha probado); `analizar.py` corre sin errores.
**Pendiente**: ver si YouTube acepta miniaturas por API en este canal (primera subida con `--portada`); decidir si se cambian las portadas de los 3 ya publicados (TASKS).
**Siguiente paso**: el próximo lote ya debe hacer §6b.

## 2026-11-16 18:55 — Nico — rama `main`
**Hecho**: análisis de ~80 Reels del nicho en Instagram (navegador integrado, cuenta @parecementiramedia, solo lectura) → informe en el Proyecto de Claude (`claude/analisis-reels-virales-2026-11-16.md`). Conclusión principal: en los virales el gancho se lee entero en el primer fotograma; en los nuestros el fotograma 0 sale sin texto. Motor v2.3: `"estilo_subtitulos": {"gancho": true}` muestra la primera frase entera desde el fotograma 0 (+15 % de tamaño, panel oscuro translúcido, karaoke dentro) y luego sigue el karaoke normal. AGENTE.md: el agente lo activa siempre, primera frase ≤ 12 palabras, formatos negación/POV/paradoja/escala y etiquetas nuevas de `gancho`. DECISIONS.md: decisión nueva (no es título fijo).
**Pruebas**: fotogramas a 0 / 0,6 / 1,6 / 2,8 / 3,5 s con el gancho de los moáis y un fondo de prueba: frase entera en el 0, palabra actual en negrita, cápsula de clave, vuelta al karaoke normal; sin `gancho`, igual que antes. Sin render completo (no hay audio en la nube).
**Pendiente**: ver el primer lote con el gancho y comparar «se quedaron viendo» en `studio.json`.
**Siguiente paso**: el lote de las 20:00 de hoy ya lo aplica si hace `git pull` (AGENTE punto «Gancho en pantalla»).

## 2026-11-16 18:35 — Nico — rama `main`
**Hecho**: (1) Moáis revisado: sin avisos ni restricciones (API y Studio); YouTube lo enseñó a ≈9 personas y solo el 55,6 % se quedó (pisada 76,5 % → 3.481 vistas, Luna 65,3 %, guerra 60,5 %): el primer segundo decide. Nuevo `estadisticas/studio.json` (datos que solo da Studio) unido a los vídeos en `construir.py`, sección «Primer segundo» en el análisis y comparación por gancho/estructura/tema con «se quedan» y retención a 3 s; dato en la ficha de la web. (2) `AGENTE.md`: créditos de ElevenLabs y datos de Studio al arrancar, regla del primer segundo, comentario fijado (en el correo de revisión; se fija tras publicar, con `send_later` para los programados), series/parte 2 y vídeo relacionado; sección «Continuaciones prometidas» en `lotes/IDEAS.md`. (3) Tarea de las 9:14 ampliada: correo «[AVISO]» si falla la recogida, hay errores en `notas` o el permiso de TikTok caduca en menos de 30 días. Nueva tarea «Parece Mentira: resumen semanal por correo» (lunes 9:41, nube, `trig_01Fio936VfVUNaM7HguqEF7g`).
**Pruebas**: análisis y web con datos reales sin errores. ElevenLabs: 6.820 de 40.000 caracteres usados (plan starter, se renueva el 15-12).
**Pendiente**: decidir créditos de ElevenLabs (al ritmo de 2 lotes al día se acaban hacia el 21-11). Clave de subida de YouTube en el Mac de Nico.
**Siguiente paso**: ver que el lote de las 20:00 aplica las reglas nuevas.

## 2026-11-16 18:40 — Nico — rama `main`
**Hecho**: dominios `oauth2.googleapis.com` y `www.googleapis.com` permitidos en Claude (Nico). Permiso de subida concedido desde el navegador integrado del Mac de Jorge (cuenta del canal, scopes `youtube.upload` + `youtube.readonly`); el token se canjeó en el propio Mac y está en su `claves.txt` como `YT_UPLOAD_REFRESH_TOKEN` (no se ha mostrado en ningún sitio). Navegador integrado: permitido `http://127.0.0.1:8765` para la vuelta de Google. `subir_youtube.py` compara títulos sin hashtags ni emojis para no duplicar.
**Pruebas**: en el Mac de Jorge, `--prueba` con el título de un vídeo ya publicado → `yaEstaba` (bS6AUPYxr7s); con un título nuevo → listo para subir. No se ha subido nada.
**Pendiente**: llevar la clave y el script al Mac de Nico (lote de las 08:00).
**Siguiente paso**: primera subida real con el próximo «ok» del lote de las 20:00.

## 2026-11-16 18:30 — Nico — rama `main`
**Hecho**: Nico aprueba las dos propuestas del análisis → `DECISIONS.md`: subidas separadas cada 2 h y ganchos que se entiendan en España y Latinoamérica (voz de España). `publicar/subir_youtube.py`: sube a YouTube por la API oficial (subida reanudable, no duplica por título, `--publicar-en` para programar, `--prueba`). La documentación de `videos.insert` (actualizada el 2026-10-15) dice que los proyectos sin verificar ya no quedan forzados a privado. `estadisticas/autorizar.py --subir` saca un permiso aparte (`youtube.upload` + `youtube.readonly`) y lo guarda en `claves.txt`. `AGENTE.md` punto 8 reescrito (YouTube por API, TikTok programado en TikTok Studio, Instagram seguido; la persona solo elige el archivo en TikTok/Instagram). Scripts copiados al Mac de Jorge (`estadisticas/autorizar.py`, `publicar/subir_youtube.py`).
**Pruebas**: el script falla bien sin claves; ni el workspace ni el Mac llegan todavía a `oauth2.googleapis.com` (dominio no permitido en la cuenta de Claude).
**Pendiente**: permitir `oauth2.googleapis.com` y `www.googleapis.com` en Claude, ejecutar `autorizar.py --subir` y copiar las líneas al Mac de Nico. TikTok por API exige la auditoría de TikTok; Instagram, la verificación de Meta.
**Siguiente paso**: primera subida real con el próximo «ok».

## 2026-11-16 18:00 — Nico — rama `main` — commit `d197071`
**Hecho**: `estadisticas/analizar.py` saca conclusiones de `data.json` con su fuerza (pista <5 vídeos, tendencia 5–14, firme 15+): ranking por red, vídeos que la red no enseñó, efecto de subir en ráfaga, comparación por tema/gancho/estructura/turno/duración (excluye los vídeos sin empuje), gancho (retención a 3 s), % visto y duración, dónde cae la curva, TikTok vs YouTube, likes y compartidos por 1.000, audiencia (países, edad, fuentes, suscritos) y evolución semanal. `construir.py` lo ejecuta en cada actualización: escribe `estadisticas/datos/aprendizajes.md` y la web tiene la vista nueva «Conclusiones». `AGENTE.md` (punto 2 y 8.5): el agente lee las conclusiones antes de elegir, hace un experimento por lote, apunta «Decisiones según las estadísticas» en `estado.md` y etiqueta los vídeos (`tema`, `gancho`, `estructura`, `experimento`) en `metadatos.json` y `etiquetas.json`. Etiquetados a mano los 4 vídeos publicados. Decisión nueva en `DECISIONS.md`.
**Pruebas**: análisis con datos reales y de ejemplo; web en Chromium sin errores; artefacto republicado (1794848427-4e86).
**Pendiente**: Nico y Jorge deciden sobre dos propuestas del análisis que chocan con el flujo actual: separar las subidas de cada lote y adaptar los ganchos al público latinoamericano.
**Siguiente paso**: comprobar que el lote de las 20:00 aplica el punto 2 de `AGENTE.md`.

## 2026-11-16 17:50 — Nico — rama `main` — commits `eafdd11`, `f614cec`
**Hecho**: navegación suave en la web de estadísticas (View Transitions: al entrar hace zoom desde donde pulsas, al volver se aleja, el cambio 7/28 días funde; barras que crecen y líneas que se dibujan; respeta «reducir movimiento»). `recoger.py` ahora pide a YouTube Analytics la audiencia de 28 días (`youtubeExtra`: países, dispositivos, suscritos/no suscritos, edad y género, fuentes, sistema) y guarda los seguidores de cada red en `historico`. Gráficas nuevas: portada con calendario de publicaciones de 28 días y reparto de vistas/seguidores entre redes; YouTube con minutos vistos, dispersión vistas vs % visto («joyas ocultas»), curvas de retención de los 5 más vistos, el canal día a día (4 minigráficas), pirámide de edad, países con bandera, barras partidas de dispositivo/suscritos/sistema y fuentes de tráfico; TikTok/Instagram con likes por 1.000 vistas, seguidores en el tiempo, reparto de interacciones por vídeo y dispersión frente a YouTube; comparativa con dispersión TikTok vs YouTube y seguidores en el tiempo. Paleta categórica validada con el script de dataviz.
**Pruebas**: Chromium con datos de ejemplo y reales (todas las vistas + ficha + móvil), sin errores; workflow lanzado a mano (run 43910923712, éxito) y ya trae `youtubeExtra` real. Artefacto republicado (versión 1794847664-454c).
**Pendiente**: Instagram (verificación de móvil en Meta). La retención y la dispersión de YouTube aparecen cuando YouTube publique la retención (48–72 h).
**Siguiente paso**: revisar la web mañana tras la actualización de las 9:00.

## 2026-11-16 17:45 — Nico — rama `main`
**Hecho**: rediseño de `estadisticas/plantilla.html` («observatorio»): tema oscuro espacial (Unbounded + Instrument Sans), portada con mapa orbital (Nova en el centro con el total; un planeta por red, tamaño según vistas; Instagram punteado si no está conectado) y tarjeta por red con mini gráfico. Rutas `#inicio`, `#youtube`, `#tiktok`, `#instagram`, `#comparativa`, `#laboratorio`, `#horas`. Vista de red: cifras clave, vistas por día, destacados (p. ej. «funciona mejor aquí que en YouTube»), lista ordenable y ficha (en YouTube con curva de retención y fuentes; enlaces al mismo vídeo en las otras redes). Títulos de TikTok limpiados (usa el de YouTube si está unido).
**Pruebas**: Chromium con datos reales y de ejemplo (7 vistas + ficha + móvil 390 px), sin errores de consola.

## 2026-11-16 17:26 — Nico (en el Mac de Jorge) — rama `main` — en pausa
**Instagram**: Meta exige una cuenta personal real de Facebook para Meta for Developers. La cuenta nueva creada por Nico quedó suspendida en revisión (apelación enviada). Se entró con el Facebook de Jorge en el navegador integrado; registro de desarrollador a medias porque el SMS de verificación del móvil no llega. Retomar: verificar móvil desde la app de Facebook del móvil y seguir el README (sección Instagram).

## 2026-11-16 17:08 — Nico (en el Mac de Jorge) — rama `main` — commit `6824722`
**Hecho**: TikTok conectado a las estadísticas. App sandbox completada (icono subido por Nico, Desktop + Login Kit, scopes `user.info.basic/stats` + `video.list`, usuario de prueba parece.mentira85). `autorizar_tiktok.py` como el de YouTube (puerto 8766, pegar URL, certificados, sustituye el token en `claves.txt`) + `probar_tiktok.py` para comprobar el token. Secretos `TIKTOK_CLIENT_KEY/SECRET/REFRESH_TOKEN`. Arreglos: espacios pegados en secretos (`limpiar_secretos`), campo `username` quitado (pedía `user.info.profile`). Workflow OK: TikTok 4 vídeos públicos (5 en total), 2 seguidores, los 4 unidos con YouTube por `estado.md`. Página de Claude republicada.
**Ojo**: el token de TikTok de `claves.txt` ya NO vale (TikTok lo rota y el workflow guarda el nuevo en GitHub con GH_PAT). Si hay que reautorizar: `autorizar_tiktok.py` y actualizar el secreto.
**Siguiente paso**: Instagram.

## 2026-11-16 17:05 — Nico — rama `main` — chat en la nube
**Hecho**: «Luna densa» v4 a petición de Nico.
- **Detalles de fondo que duran**: `recorrido(T0, T1, …)` en `gen.py` mueve los objetos según el tiempo ABSOLUTO del vídeo, así siguen en el mismo sitio al cambiar de plano. Dos satélites cruzan despacio todos los planos de espacio (0,8–19 s y 33–47,5 s); bandada de 3 pterosaurios en los dos planos de dinosaurios (25,5–32 s); estrellas fugaces más lentas (se dibujan en 0,7 s y se apagan en 1,6 s).
- **Dinosaurios detallados y variados** (`ilus_luna.py`, `_animal`): volumen con degradado lomo→panza, manchas, textura de piel recortada a la silueta, luz de borde, ojo con brillo, patas lejanas más oscuras y sombra. Especies: braquiosaurio, tiranosaurio, triceratops (gola con puntos y tres cuernos), estegosaurio (placas iluminadas) y raptores; pterosaurio rehecho (membrana con dedos y cresta).
- **Fondos con más tonos**: `bg_espacio_rico` con 3 paletas (violeta, petróleo, ámbar) — nebulosas en 3 capas de ruido de color con máscaras, filamentos de polvo oscuro, banda de la Vía Láctea, estrellas de varios colores y tamaños con brillo, galaxias lejanas; Luna con cordillera lejana azulada, textura de regolito, cráteres con borde iluminado y piedras con sombra; eclipse con crepúsculo de 6 tonos y colinas por capas; jungla con rayos de sol, bruma entre capas y volcán con lava.
- Arreglado: los SVG de objetos llevaban un rectángulo de grano que se veía sobre el fondo.
**Pruebas**: fotogramas revisados (12 instantes); render 48,3 s, 49 MB.
**Siguiente paso**: que Nico/Jorge lo vean; si gusta, convertir fondos y animales en biblioteca reutilizable para los lotes.

## 2026-11-16 15:58 — Nico (en el Mac de Jorge) — rama `main` — en pausa
**Hecho**: tarea programada «Estadísticas Parece Mentira: republicar página» (9:14 Madrid, nube, modo automático, `trig_01M865HVYsaR3X7rTzNwALEt`). Secreto `GH_PAT` creado (token fine-grained sin caducidad, solo repo `parece-mentira`, solo Secrets lectura/escritura; copia en `claves.txt`). Página `condiciones.md` añadida a parecementirapero.github.io. TikTok for Developers: cuenta creada por Nico, app «Parece Mentira Stats» y sandbox «estadisticas» a medio configurar (ver TASKS).
**Siguiente paso**: terminar la app de TikTok (icono, scopes, target user, Apply changes) → `autorizar_tiktok.py` → secretos → Instagram.

## 2026-11-16 15:45 — Nico (en el Mac de Jorge) — rama `main` — commit `435c720`
**Hecho**: YouTube conectado a las estadísticas. Cliente OAuth «stats» (App de escritorio) creado; `autorizar.py` ejecutado en el Mac de Jorge (ID, secreto y token en `~/Documents/Parece Mentira/claves.txt`); secretos `YT_CLIENT_ID`, `YT_CLIENT_SECRET` y `YT_REFRESH_TOKEN` en GitHub. Workflow lanzado a mano: OK (commit «estadísticas: actualización 2026-11-16»): 4 vídeos públicos, 7 suscriptores; retención «pendiente» hasta que pasen 48–72 h.
**Problemas resueltos en el Mac**: licencia de Xcode sin aceptar (`sudo xcodebuild -license accept`); `git clone` del repo privado falla (sin sesión de GitHub en git) → se copió solo el script a `~/Documents/Parece Mentira/estadisticas/`; Python de python.org sin certificados → `autorizar.py` usa `/etc/ssl/cert.pem`; ahora además usa el puerto fijo 8765, deja pegar la URL de vuelta a mano y guarda el token en `claves.txt`.
**Siguiente paso**: `GH_PAT`, TikTok e Instagram (README); tarea programada que republique la página de Claude cada mañana.

## 2026-11-16 15:20 — Nico — rama `main`
**Hecho (navegador integrado del Mac de Nico, con permiso de Nico)**: aceptada la Política de Datos de Usuario de las APIs de Google y creado Google Auth Platform («Parece Mentira Stats», externo). Google ya exige página principal + privacidad en dominio propio para publicar → creado el repo público `parecementirapero.github.io` (GitHub Pages) con `index.md` (portada: TikTok, Instagram, contacto) y `privacidad.md`; puestos en «Información de marca» + dominio autorizado; app **En producción**. La app de Claude no tiene acceso de escritura a ese repo (se editó desde la web de GitHub).
**Siguiente paso**: en el Mac de Nico, pulsar «Crear» en el formulario del cliente «stats» ya preparado, copiar ID y secreto a `claves.txt` y seguir el README desde el paso 4.

## 2026-11-16 14:10 — Nico — rama `main` — en pausa
**Hecho (navegador integrado del Mac de Nico)**: proyecto de Google Cloud `parece-mentira-stats` con la cuenta parecementirapero.media@gmail.com (condiciones aceptadas por Nico); activadas YouTube Data API v3 y YouTube Analytics API; Google Auth Platform a medias (pasos 1–3 rellenos, sin pulsar «Crear»: puede que haya que repetirlos).
**Siguiente paso**: seguir `estadisticas/README.md` desde el paso 2 (consentimiento → «En producción» → credencial de escritorio → `autorizar.py` → secretos), después `GH_PAT`, TikTok e Instagram.

## 2026-11-16 14:30 — Nico — rama `main` — commit `609f4f8` — chat en la nube
**Hecho**: TikTok e Instagram en las estadísticas. `tiktok.py` (Display API: vistas, likes, comentarios, compartidos por vídeo + seguidores; TikTok **no da retención** por API) e `instagram.py` (insights de Reels: vistas, alcance, likes, comentarios, compartidos, guardados, tiempo medio visto, tasa de salto si la API la da; si rechaza una métrica, se quita y se reintenta). `recoger.py`: cada red es independiente (si falta o falla, se conservan sus datos anteriores y se avisa en la web); une el mismo vídeo entre redes (enlaces de `lotes/*/estado.md` → fecha ±1 día + título parecido → a mano en `etiquetas.json`); guarda una foto diaria (`historico`, 120 días) para tener vistas por día en TikTok/Instagram. Tokens renovados (TikTok rota el refresh token en cada uso; Instagram se renueva los lunes) se guardan con `gh secret set` usando el secreto `GH_PAT`. Web: pestaña **Redes** (cifras por red, barras apiladas por vídeo, vistas por día en cada red, tabla comparativa con enlaces) y bloque «En las otras redes» + vistas por día de las 3 redes en la ficha. `autorizar_tiktok.py` (Login Kit de escritorio con PKCE en hex). README con los pasos de TikTok, Instagram y `GH_PAT`.
**Pruebas**: `recoger_todo()` con las 3 APIs simuladas (rotación de token sin GH_PAT → aviso en notas; IG rechaza `reels_skip_rate` → reintento sin ella; post de feed ignorado; TikTok unido por título y fecha; IG unido por `estado.md`); web con datos de ejemplo en Chromium (Redes, salto de Redes a la ficha, sin errores). Sin probar contra las APIs reales: faltan credenciales.
**Pendientes**: conectar las 3 redes y `GH_PAT` (TASKS); comprobar con datos reales que `video.list` en sandbox devuelve los vídeos de parece.mentira85 y que Instagram da `views` en los reels.
**Siguiente paso**: puesta en marcha siguiendo `estadisticas/README.md` (YouTube → GH_PAT → TikTok → Instagram) y lanzar el workflow a mano.

## 2026-11-16 14:05 — Nico — rama `main` — chat en la nube
**Hecho**: «Luna densa» v3 — **ritmo variable**. Nico detectó que casi todos los planos duraban lo mismo. Ahora `gen.py` ata cada plano a una **palabra del guion** (índice en la alineación, no segundos fijos), las animaciones se escalan a la duración del plano y hay planos de **0,32 s a 2,72 s** (9 de menos de 0,7 s, 10 de 1,5 s o más; cuenta atrás 3-2-1 en tres cortes secos). **Control de lectura**: cada texto en pantalla tiene que verse ≥ 0,25 s + 1 s por cada 17 letras; el script avisa si no (quité rótulos que repetían el subtítulo y acorté otros). Guion recortado a **155 palabras** para que el narrador vaya a velocidad normal (≈47 s); `provisional.py` estima los tiempos a ese ritmo. 39 planos, 126 efectos.
**Para la voz real**: `python3 gen.py DIR audio.mp3 alineacion.json` → los cortes se recolocan solos sobre la voz.
**Pruebas**: hoja de fotogramas cada 0,8 s revisada; render 48,3 s, 48 MB.
**Siguiente paso**: si gusta, pasar a `AGENTE.md`/`DECISIONS.md` las reglas: planos atados a palabras, duraciones de 0,3 a 2,7 s, control de lectura y micro escenas de detalle.

## 2026-11-16 14:00 — Nico — rama `main` — commit `7398e59` — chat en la nube
**Hecho**: web de estadísticas del canal en `estadisticas/` (sustituye a la idea del correo diario a las 9:00). `recoger.py` saca de YouTube Data API + Analytics: vistas, likes, comentarios, compartidos, suscriptores por vídeo, % medio visto, curva de retención (100 puntos), «siguen a los 3 s», fuentes de tráfico, vistas por día y serie diaria del canal. `construir.py` mete los datos en `plantilla.html` → `web/index.html` (una página, sin dependencias). Pestañas: Resumen (cifras clave vs periodo anterior, vistas por día, «Lo destacado»), Vídeos (tabla ordenable + ficha), Laboratorio (compara por cualquier etiqueta: tema, lote, voz, gancho…) y Mejores horas. Etiquetas automáticas: tema por hashtags de la descripción y lote por `lotes/*/estado.md`; correcciones a mano en `etiquetas.json`. Workflow `.github/workflows/estadisticas.yml`: 07:05 y 08:05 UTC + `--si-toca` (una vez al día, antes de las 9:00 en Madrid con horario de invierno y de verano) y botón manual. Página de Claude «Parece Mentira · Estadísticas» publicada con datos de ejemplo.
**Pruebas**: `recoger.py` con la API simulada (vídeo privado excluido, sin engagedViews → nota, lote y tema detectados, curva y 3 s); web con datos de ejemplo en Chromium (4 pestañas, ficha y Laboratorio por gancho, sin errores de consola). Sin probar contra YouTube real: faltan credenciales.
**Pendientes**: pasos 1–6 de `estadisticas/README.md` (Google Cloud con la cuenta del proyecto, app «En producción», `autorizar.py` en un Mac, 3 secretos en GitHub, lanzar el workflow); después, tarea programada que republique la página de Claude cada mañana; rellenar `etiquetas.json`.
**Siguiente paso**: Nico o Jorge hace la puesta en marcha (~15 min) y lanza el workflow a mano para ver los primeros datos reales.

## 2026-11-16 13:40 — Nico — rama `main` — chat en la nube
**Hecho**: «Luna densa» v2 con **micro escenas** (0,5–0,9 s) de detalles secundarios: cuenta atrás antes del despegue, primera huella de bota, láser cargándose en la cúpula, patinadora que gira y frena al abrir los brazos (la comparación de Meyers, UW–Madison), +1,8 ms por siglo, láser que corta la concha, cronómetro hacia atrás, Luna de hoy frente a la del futuro, hoja de calendario que se arranca. Detalles de fondo: estrellas fugaces, satélite, barco que sube con la marea, pterosaurio, humo del volcán y flashes de móviles en el eclipse. **38 planos** (antes 29) y 130 efectos de sonido. Ilustraciones nuevas: pterosaurio, satélite, patinadora (dos siluetas), pista de hielo.
**Motor**: `core.transformar` admite `ex`/`ey` negativos (espejo; antes el dibujo desaparecía: por eso no se veía el dinosaurio pequeño). Animar `ex` entre 1 y −1 simula un giro.
**Pruebas**: fotogramas de cada micro escena revisados (corregidos: patinadora con aspecto infantil → silueta a contraluz; huella fuera de encuadre); render 47,1 s, −19,9 LUFS, 48 MB.
**Siguiente paso**: que Nico/Jorge lo vean; locución real.

## 2026-11-16 13:10 — Nico — rama `main` — chat en la nube (sin acceso a los Macs)
**Hecho**: prueba «La Luna se aleja» **densa, desde cero** (`lotes/prueba-luna-densa/`): guion nuevo de 169 palabras con datos nuevos (Apolo 11, láser 2,5 s, dinosaurios 23,5 h y 372 días por una almeja fósil, 18 h hace 1.400 millones de años, fin de los eclipses totales dentro de ~600 millones), **29 planos en 46,6 s** (v4: 18), una acción por plano y capas extra. Ilustraciones nuevas en `ilus_luna.py` (cohete, módulo lunar, jungla, dinosaurios, almeja fósil, calendario, cielo de eclipse, personas mirando). Motor: `motor/sfx.py` (efectos de sonido generados por código) + `sfx` en episodio.json; `rotulo` con `decimales`, `contar_prefijo` y `miles`.
**Voz**: no hay. Se montó con `provisional.py` (silencio + alineación estimada con pausas en la puntuación) para que el karaoke y los planos tengan tiempos. Con la locución real: `python3 gen.py DIR audio.mp3 alineacion.json`.
**Fuentes**: UW–Madison/PNAS 2018 (18 h hace 1.400 Ma; 3,82 cm/año); de Winter et al. 2020, Paleoceanography and Paleoclimatology (almeja *Torreites sanchezi*, 23,5 h y 372 días hace 70 Ma); Sky & Telescope (eclipses totales irregulares desde ~620 Ma, último hacia ~1.200 Ma).
**Pruebas**: hojas de fotogramas cada 1 s (corregidos: año «1.969», rótulo cortado, dinosaurios invisibles); render 1080×1920, 47,1 s, h264/AAC, −19,9 LUFS, 47 MB; render en ~3 min.
**Pendientes**: que Nico/Jorge lo vean; locución real; el `"="` del plano 3 se ve pequeño; comprobar `ejemplos/005` con el motor cambiado (la mezcla sin efectos no cambia).
**Siguiente paso**: si el ritmo gusta, pasarlo a `AGENTE.md`/`DECISIONS.md` como estándar (≈1 plano cada 1,5–2 s y efectos de sonido).

## 2026-11-16 12:58 — Nico — rama `main`
**Decisión**: tras ver la prueba de acabado, Nico prefiere el v4 tal cual. No se integra `motor/acabado.py` (queda en el repo sin usar). Apuntado en DECISIONS y TASKS.
**Siguiente paso**: si se quiere más carga visual, trabajarla en las ilustraciones (más capas y acciones por plano), no en el post-proceso.

## 2026-11-16 13:00 — Jorge (vía Claude) — rama main
- Qué: prueba de temas cotidianos para el lote de esta tarde. Jorge propone que las ideas conecten con la vida cotidiana y no solo datos del pasado. Se prueba solo en el lote 2026-11-16-tarde con 2 temas cotidianos + 1 histórico conectado con hoy (nudillos, efecto puerta, móvil vs. Apolo 11), reservados en `lotes/IDEAS.md`. `AGENTE.md` §2: el agente usa los temas reservados para su lote.
- Pruebas: ninguna (solo texto).
- Pendiente: Nico y Jorge deciden el 2026-11-17 si se queda (tarea en `TASKS.md`).
- Siguiente paso: lo hace el agente de las 20:00 sin tocar su tarea programada.

## 2026-11-16 12:55 — Nico — rama `main` — chat en la nube (sin acceso a los Macs)
**Hecho**: módulo nuevo `motor/acabado.py` (post-proceso sobre un MP4 ya renderizado, sin coste): halo/bloom en las luces, LUT «documental» generado por código (negros levantados, sombras frías, luces cálidas, saturación 90 %) al 75 %, textura de papel en luz suave, capa de bokeh y polvo en primer plano, parpadeo de exposición leve, aberración cromática de 2 px y grano animado solo en luminancia (`-tune grain`, tope 8 Mb/s). Parámetro `--fuerza` (1.0 normal, 1.7 intenso). **No está integrado en `render.py`** todavía.
**Pruebas**: render del 02 v4 (Luna) sin voz ni subtítulos (el audio está en el Mac de Jorge), 46,7 s; acabado normal e intenso; vídeo comparativo lado a lado; fotogramas revisados (1,5/6/11/20/32/42 s). Pesos: 38,6 MB antes → 47 MB después. Tiempo: ~4,5 min de acabado sobre 2 min de render (las partículas en Python son lo lento).
**Pendientes**: que Nico y Jorge elijan nivel; integrarlo en el motor; bajar la aberración a 1 px (en las estrellas deja puntitos de color); acelerar las partículas.
**Siguiente paso**: decisión de nivel en el chat y, si se aprueba, apuntarlo en `DECISIONS.md` y aplicarlo al próximo lote.

## 2026-11-16 00:10 — Jorge — rama `main` — ordenador de Jorge
**Decisión**: se deja Drive. Desde el próximo lote, el agente envía los 3 MP4 a su propio chat (`device_stage_files` + `SendUserFile`) y el correo de las 08:00/20:00 lleva el enlace a ese chat para verlos y dar el «ok» allí.
**Cambiado**: DECISIONS (Drive tachado + regla nueva), AGENTE §7, CLAUDE.md, TASKS (fuera las tareas de Drive para ordenador), PROJECT_STATE.
**Siguiente paso**: comprobar en el lote de las 07:52 (Nico) que los vídeos aparecen en el chat y el correo enlaza bien.

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
