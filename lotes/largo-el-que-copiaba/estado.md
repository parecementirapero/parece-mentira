# «El que copiaba en el colegio» — estado (pausado 2026-11-26, Jorge: «paramos y luego sigues»)

## Hecho
- Guion final = v3 (`guion.txt`, 749 palabras). Voz grabada en 3 bloques en el Mac de Jorge (`Documents/Parece Mentira/lotes/largo-el-que-copiaba/0N-locucion.mp3` + alineaciones), 285 s. En la nube: `voz/locucion-completa.wav` (no va a git) y `voz/alineacion-completa.json`; índices de palabra en `indices.txt`.
- Arte (3 generadores, revisados con hojas de contacto): `generadores/ilus_fondos.py` (9 fondos v+h: aula, colegio fuera, calle día, café dentro/triste, cocina, habitación, campo de barrio, estudio oscuro), `generadores/ilus_gente.py` (48 piezas: Marta/Lucas niños y adultos, profesora, clientes, regate, guitarrista, cocinero, bebé, padres, caras), `generadores/ilus_cosas.py` (49 piezas: cafeterías, persiana, hamburgueserías, pupitre, examen, timbre, hucha, billetes, móvil y apps genéricas, iconos, focos). Más `frame_prueba.py` (hamburguesería, cola de perfil, Lucas). Guía: `ARTE.md`.
- Decidido con Jorge: largo 16:9 solo YouTube con el estilo de la cueva; corto de ~1 min vertical (TikTok, Shorts, Reels) con el boceto **B** (fondo apagado, focos y contadores); una sola voz; música nueva con energía de emprender, distinta en cada vídeo.

## Falta
1. Música: estilo «emprende» en `motor/musica.py` (mayor, ~112 bpm, piano, bombo y palmas, crece) + `python3 -m motor.prueba`.
2. Montaje del largo (`generadores/gen.py` + `planos_*.py`, como la cueva: planos en coordenadas del vertical y `adaptar` a 16:9; anclas de suelo en el informe de fondos: aula 1420/870, colegio 1430/880, calle día 1440/880, café 1430/880, cocina 1440/880, habitación 1440/880, campo 1440/880, estudio 1400/860, ciudad 1390/830).
3. Corto: mismo audio con `Video(..., omitir=…)` quitando las palabras (18,28),(35,150),(173,211),(223,243),(270,290),(311,328),(335,592),(604,705),(739,749) → ≈ 62 s. Estilo B.
4. Render, `motor.calidad` sin ❌, portadas, entrega en el chat y en el Mac, correo, registro. Publicar solo con «ok».

## v2 (2026-11-27 00:45): música nueva
- Jorge no quería la música «emprende» (ni la prueba «ambicion»): «parece triste» con «cine»; aprobó «cine_epico» (Si m–Sol–Re–La, piano en golpes, metales, 808, batería a medio tiempo), hecha por código, sin ElevenLabs.
- Solo cambia el audio (vídeo copiado de la v1): largo v2 SHA 16beace90cf2, corto v2 SHA 28e46ca82205; −19,2/−19,3 LUFS; calidad igual (55 y 72, sin ❌).
- MP4 v2 y SRT copiados al Mac (`Documents/Parece Mentira/lotes/largo-el-que-copiaba/`).
- Pendiente: portadas, metadatos y «ok» para publicar.

## Publicado (2026-11-27, «súbelos a TikTok y YouTube con su portada»; luego «no quiero Short, solo el largo», Jorge)
- YouTube largo: https://youtu.be/olrobKKTa44 (público, portada `portada-16x9.jpg` puesta por API, comentario fijado).
- TikTok corto: https://www.tiktok.com/@parece.mentira85/video/7712633311755128086 (portada `portada-corto.jpg`, comentario escrito; la web no deja fijar).
- Short de YouTube zKW16umj_VE: subido programado y borrado sin publicarse, a petición de Jorge.
