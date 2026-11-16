# Estado — lote 2026-11-16-tarde

- **Estado**: **v2 aprobada** («ok» de Jorge 22:03) — publicando. La v1 no se publica.
- **Agente**: Agente 20:00 (Jorge) · Mac de Jorge · carpeta local `Documents/Parece Mentira/lotes/2026-11-16-tarde`
- **Chat del lote**: https://claude.ai/code/session_019BG1dKP8Ze8noFARTZpfbf (3 MP4 y 3 portadas enviados)
- **Correo de aviso**: enviado a parecementirapero.media@gmail.com, id `1a1e5cb7121de9d1`.
- **Prueba de temas cotidianos** (DECISIONS 2026-11-16, Jorge): temas reservados en `IDEAS.md` (2 cotidianos + 1 histórico contado desde hoy).

## Vídeos (v1)
| # | Archivo (Mac de Jorge) | Duración | SHA-256 | Voz | Portada |
|---|---|---|---|---|---|
| 1 | `01-crujir-nudillos_v1.mp4` | 57,7 s | `52ffe0361b090a504e2d297d46f5d7d32f5f350eafaaad78b3fde967705bca3c` | OK | «60 años crujiendo una mano» · arriba · 54,3 s |
| 2 | `02-puertas-olvidar_v1.mp4` | 54,7 s | `64b4909b63b2a660efd47f1f124727f24848948683d58608028bc8d293653a43` | OK | «La puerta te borra» · arriba · 2,3 s |
| 3 | `03-movil-apolo-11_v1.mp4` | 51,9 s | `38c78f7ae313b7b5cb9ebc490607ef865d368f14138274d17aaf73e634fd18bf` | OK | «Tu móvil vs el Apolo» · dato · 14,3 s |

El SHA del archivo en el Mac coincide con el del render (comprobado con `shasum` en el Mac).

## Decisiones según las estadísticas
Base: `estadisticas/datos/aprendizajes.md` del 2026-11-16 (4 vídeos: todo son **pistas**). `studio.json` ya tenía hoy los 4 Shorts («se quedaron viendo» 55,6–76,5 %): no se volvió a abrir Studio.
- **Experimento del lote**: el tipo de tema (cotidiano), por la prueba decidida por Jorge. Para poder atribuirlo, el resto se apoya en lo que va mejor:
- **01 nudillos**: gancho «dato» (cifra en la primera frase), estructura «experimento». Se espera que el «se quedaron viendo» esté ≥ 65 % porque el fotograma 0 enseña las dos manos (una cruje, la otra «NUNCA»).
- **02 puerta**: gancho «pregunta» (situación que todo el mundo ha vivido), estructura «metáfora visual». Si el tema cotidiano conecta más, aquí debería notarse más (es el más «de todos los días»).
- **03 Apolo**: gancho «contraste» y estructura «comparación» (lo que mejor va en YouTube y TikTok). Sirve de control: si este va mejor que 01 y 02, pesa más la estructura que el tema.
- Duración 52–58 s (dentro de 45–60 de DECISIONS). La pista «40–50 s va mejor» (3 vídeos) no se aplica todavía; se propone en el correo si se repite.
- Audiencia latinoamericana (79 %): sin expresiones solo de España; referencias universales (móvil, puertas, nudillos).

## Control de calidad
- `ffprobe`: 1080×1920, 30 fps, h264 yuv420p, AAC 48 kHz estéreo; duración = locución + 0,5 s (57,2/54,2/51,4 s de voz).
- Volumen integrado: −19,2 / −19,0 / −19,4 LUFS.
- Hojas de fotogramas (cada 1,5 s) y fotogramas sueltos del MP4 mirados: pantalla completa, sin título fijo, sin Nova, gancho legible en el fotograma 0, karaoke arriba, algo en movimiento en cada plano.
- Corregido antes del render: huesos de la articulación ya separados al empezar (01), rectángulo de presión → elipse difusa (01), burbuja más pequeña (01), carpeta y bocadillo invisibles en el archivador (02, faltaba `op` en las claves), hoja de la puerta girando sobre la bisagra (02), flecha que no señalaba la puerta (02), etiqueta tapada por el gancho (03), cifra del gancho visible desde el fotograma 0 (03), hilo de cobre que ahora entra por el agujero del anillo (03).
- Cifras y nombres revisados contra las fuentes (`guiones.md`).

## Generadores
`generadores/` (estilo v4): `base.py` (reutiliza `comun_v4.py` del lote 2026-11-15-tarde), `ilus_0N.py` (SVG nuevos: manos, radiografías, salón, médico, resonancia, articulación en sección; pasillo, persona, plantas, cerebro, película, archivador, puerta; móvil, ordenador del Apolo con DSKY, módulo lunar, memoria de cuerda, anillo) y `gen_0N.py DIR_SALIDA DIR_AUDIO`.

## Créditos ElevenLabs
Antes del lote: 31.861 restantes (40.000 − 8.139). Gastados ≈2.500.

## Versión 2 (método «denso») — Jorge — 2026-11-16 21:40
Jorge escribió «ok» a la v1 y, antes de subir nada, pidió no publicarla y rehacer los vídeos con el formato nuevo (método «denso», DECISIONS 2026-11-16, Nico). No se subió nada a ninguna red: YouTube Studio se miró y no había ninguno de los 3.
Mismo audio (0 créditos). `generadores/denso.py` (módulo con el mecanismo de `prueba-luna-densa/gen.py`: planos atados a palabras, duración variable, control de lectura, detalles que duran entre planos, neones con halo, whoosh ≤ cada 5 s a −24 dB, música −13 dB) + `gen_0N_v2.py` + `ilus_extra.py` (gato, polilla, reloj de pared, llaves, taza, planta, hojas de calendario, sala de control de los 60, y satélite/cohete/módulo/fondos ricos de la prueba de la Luna).

| # | Archivo (Mac de Jorge) | Duración | Planos | SHA-256 | Portada |
|---|---|---|---|---|---|
| 1 | `01-crujir-nudillos_v2.mp4` | 57,7 s | 37 (0,5–2,8 s) | `bd1453e5c6da9c52a5c8fe7df9076c1cd73baaaefcc7439b46e5e370f57c0c57` | arriba · 52,3 s |
| 2 | `02-puertas-olvidar_v2.mp4` | 54,7 s | 34 (0,8–3,7 s) | `8675665cefa6dafa1e64bbe6ad1ee7701cb356ace263e79c7e590cbbef8f8ac6` | arriba · 53,3 s |
| 3 | `03-movil-apolo-11_v2.mp4` | 51,9 s | 33 (0,4–3,1 s) | `3446258b96e65999425269275d9da416d97b9a2b0871aa68747bac9267a7c962` | dato · 15,3 s |

QC: 1080×1920/30 fps/h264/AAC; −19,2 / −19,0 / −19,3 LUFS; control de lectura OK en los 3; hojas cada 1 s revisadas (arreglados: hojas del calendario que dejaban el plano vacío, caja demasiado grande en primer plano, «ARCHIVADO» y la fecha del alunizaje sin tiempo de lectura; fondo nuevo de sala de control para el Apolo).

**Publicación por API en el Mac de Jorge**: no se puede todavía: en su `claves.txt` falta `YT_UPLOAD_REFRESH_TOKEN` (solo está en el Mac de Nico). Con «ok» se sube YouTube desde el navegador integrado (la persona elige los archivos).

## Publicación
- **«ok» de Jorge a la v2 (los 3 vídeos)**: 2026-11-16 22:03, en el chat del lote. Comprobado en Studio: ninguno publicado todavía. MP4 de la v1 movidos a `v1/` en la carpeta local para no confundirlos al elegir archivos.
- Copias aprobadas (mismo SHA-256 que la v2) en `Documents/Parece Mentira/PARA PUBLICAR/2026-11-16-tarde/`: subcarpeta `Vídeos/` («1 - Crujirse los nudillos.mp4», «2 - Las puertas te hacen olvidar.mp4», «3 - Tu móvil y el Apolo 11.mp4») y subcarpeta `Portadas/` («N - portada.jpg»), a petición de Jorge.

- **YouTube** (Studio desde el navegador integrado; Jorge eligió los 3 MP4; miniatura: fotograma elegido en Studio porque la subida de imagen no le funcionó a Jorge):
  - 01 https://youtube.com/shorts/7PoER_sR6R0 — público 2026-11-16 22:12 (miniatura: fotograma «60 años después»)
  - 02 https://youtube.com/shorts/cTRgkuY21mw — programado 2026-11-16 23:15 (Madrid)
  - 03 https://youtube.com/shorts/hfRveipHIdk — programado 2026-11-17 00:15 (Madrid)
- **YouTube**: comentario escrito en el 01 («¿Tú te crujes los dedos? ¿Con qué mano?») pero **sin fijar**: YouTube pide verificar el canal (teléfono) para fijar comentarios — lo tiene que hacer Nico o Jorge en Studio.
- **TikTok** (TikTok Studio, Jorge eligió cada MP4): 01, 02 y 03 publicados seguidos ~22:25–22:35, portada por defecto (fotograma 0 con el gancho). A petición de Jorge, **texto sin fuentes** (gancho + resumen + hashtags); con los enlaces TikTok avisaba «Content may be restricted». URLs: pendientes (aún procesando).
- **Instagram**: Reel 01 publicado (formato original 9:16, portada = fotograma 0 con el gancho, texto sin fuentes).
- **Sin fuentes en las descripciones** desde ahora (Jorge, DECISIONS 2026-11-16): `metadatos.json` actualizado; en YouTube se quitan de los 3.
