# Estado — lote 2026-11-17-manana

- **Estado**: **en revisión** (v1). Esperando «ok» en el chat del lote.
- **Agente**: Agente 08:00 (Nico) · MacBook Air de Nico · carpeta local `Documents/Parece Mentira/lotes/2026-11-17-manana`
- **Chat del lote**: https://claude.ai/code/session_019BG1dJfghaKYErZsy5CyPu (3 MP4 y 3 portadas enviados)
- **Correo de aviso**: enviado a parecementirapero.media@gmail.com, id `1a1e86caf2a125ea`.
- Primer lote automático con el método denso + `motor.calidad` obligatorio.

## Vídeos (v1)
| # | Archivo (Mac de Nico) | Duración | Planos | SHA-256 | Calidad | Portada |
|---|---|---|---|---|---|---|
| 1 | `01-platano-radiactivo_v1.mp4` | 58,6 s | 39 (0,44–2,8 s) | `b5ffe5031e87406f24593d43790a66ad741f0eb259e352c131d8d536242998cb` | 92/100 | «Eres más radiactivo» · dato · 50,8 s |
| 2 | `02-saturno-flotaria_v1.mp4` | 55,8 s | 38 (0,56–3,3 s) | `ae6ad5fab007769147e495194ddbf0eaedb35981a5b15be3258d9d57ce66566e` | 90/100 | «Saturno flotaría» · arriba · 1,8 s |
| 3 | `03-huella-koala_v1.mp4` | 58,9 s | 38 (0,61–3,4 s) | `6ff052cd69821a8bfe98be1a8478850e418f0493214199c4afeca3bb1617dfdf` | 100/100 | «Esta huella no es humana» · dato · 58,3 s |

SHA del archivo en el Mac = SHA del render (comprobado con `shasum`). En la carpeta local: MP4, SRT, manifiestos, locuciones, alineaciones y `NN-portadas/` (portada elegida + 2 hojas).

## Arranque
- Studio (§1.8): no se abrió. La última lectura (`studio.json`, 2026-11-17 00:25) ya tiene todos los Shorts con ≥ 24 h; los del 2026-11-16-tarde aún no llegan a 24 h.
- No hay experimento aprobado en la tabla de `motor/APRENDIZAJE.md` (H1, H2, H8 pendientes del «sí»).
- ElevenLabs: antes 9.128 / 40.000; después 10.172 / 40.000 → **quedan 29.828** (≈8 lotes; se renuevan el 15-12).

## Decisiones según las estadísticas
Base: `estadisticas/datos/aprendizajes.md` (4 vídeos: todo **pista**) y H7 (primer segundo) de `APRENDIZAJE.md`.
- Pistas aplicadas: «Espacio» y «comparación» van mejor (02 lo usa: es el control); audiencia latinoamericana → referencias universales (plátano, Saturno, huellas), sin expresiones de España; los tres con `alcance: universal`.
- Duración 55–59 s: la pista «40–50 s» (3 vídeos) choca con DECISIONS (150–160 palabras, H2 rebajada) → no se aplica; se menciona en el correo.
- **Experimento del lote**: estaba previsto «plano real» (foto de Saturno de Cassini/NASA en el 02, AGENTE §5b) pero **no se pudo**: `motor.openverse descargar` falla en el Mac con «Tunnel connection failed: 403» hacia `thumb.wikimedia.org` (no está en los dominios permitidos de la cuenta). Siguiendo §5b.7 se hizo todo ilustrado. En su lugar, el experimento es **gancho de negación** en el 03 (2.º dato tras el pulpo del 2026-11-16-manana); 01 y 02 con gancho de dato.
  - 01 plátano: dato «Este plátano es radiactivo.» (4 palabras), experimento. Espero ≥ 65 % «se quedan» (plátano enorme cayendo en el fotograma 0).
  - 02 Saturno: dato «Saturno flotaría en el agua.» (5), comparación. Control.
  - 03 koala: negación «Esta huella no es humana.» (5), misterio por pistas. Si la negación funciona, debería igualar o superar a 01/02 en «se quedan».

## Prueba del primer segundo (AGENTE §2)
| # | Objeto único y grande moviéndose en el fotograma 0 | Primera frase (≤ 5) | Alcance |
|---|---|---|---|
| 01 | Un plátano enorme cayendo sobre la encimera, con chispas verdes | «Este plátano es radiactivo.» (4) | universal |
| 02 | Saturno cayendo a una bañera (salpica a los 0,9 s) | «Saturno flotaría en el agua.» (5) | universal |
| 03 | Una huella dactilar que se estampa con una lupa que la cruza | «Esta huella no es humana.» (5) | universal |

## Temas
- Elegidos de `IDEAS.md` (candidatos con objeto claro para el fotograma 0). Cada dato con ≥ 2 fuentes (`guiones.md`).
- **Descartado**: miel comestible de las tumbas egipcias (mito sin fuente primaria). Sustituido por las huellas del koala.
- Sin tema histórico en este lote (ciencia, espacio, misterio/animales).

## Control de calidad
- `ffprobe`: 1080×1920, 30 fps, h264, AAC 48 kHz estéreo; duración = locución + 0,5 s (58,1 / 55,3 / 58,4 s de voz).
- −19,1 / −19,2 / −19,1 LUFS.
- `motor.guion`: ✓ los tres. `construir`: ✓ todos los textos se leen. `motor.calidad --mp4`: **sin ❌** (92/90/100; `calidad-0N.md`).
- ⚠ que quedan, justificados: 01 «plano pobre» = micro plano de 0,6 s con la letra K (a propósito); 01 variación de ritmo 0,44 (límite 0,45). 02 «planos pobres» = micro planos de 0,6 s a pantalla llena (cubo, nube de gas); «casi iguales» 6→7 (el mismo cubito: 1 cm → 1 g, continuidad buscada) y 20→21 (bañera → bañera en el espacio con la cifra).
- Corregido antes de entregar (hojas cada 1 s miradas): ritmo plano (❌) → 6–11 micro planos por vídeo; rótulos que pisaban la franja del subtítulo; balanza sin platos (01) → fuera; canguro mal dibujado (03) → redibujado; encuadre repetido 42–47 s (01) → planos más cerrados; cubitos sobre fondo vacío (02) → agua, Saturno y partículas; «ANILLOS», «REMOLINOS», «SUJETAR» con poco contraste → con cápsula; demasiados efectos en un segundo (01) → tics más bajos.
- Cifras y nombres revisados contra el guion y las fuentes. Sin personas reales dibujadas (Henneberg solo como rótulo).

## Generadores
`generadores/`: `NN-guion.txt` (locución), `ilus_lote.py` (37 SVG nuevos: plátano, racimo, contador Geiger con aguja, átomos, chispa, cocina, laboratorio, silueta en rayos X, escáner; Saturno con anillos, bañera, agua, cubitos, casa, hielo, edificio, nube de gas; huellas dactilares, koala, mano de koala, microscopio, detective, canguro, wombat, rama de eucalipto, bosque, árbol de dos ramas, cinta policial) y `gen_0N.py DIR [locucion.mp3 alineacion.json]`. Render en la nube; resultados copiados al Mac.

## Publicación
Pendiente del «ok».
