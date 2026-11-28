# Lote 2026-11-28-tarde — estado

_Hecho por adelantado (≈17:45–18:40) a petición de Jorge en el chat del lote 2026-11-27-tarde: «hazme el lote de hoy adelantado». Firma: Jorge (con el agente). Chat: https://claude.ai/code/session_019BG1dK7GpyrYsYXE518JkF_

## Estado: **en revisión** (v1) — esperando «ok» en el chat

| # | Archivo | Duración | SHA-256 |
|---|---|---|---|
| 01 | `01-segundo-intercalar_v1.mp4` | 56,1 s | bc3d89adf8fefc31fcbdf57e9882e2f8220d2caf80ffc4fb5b69cfb4056d1ca2 |
| 02 | `02-estrellas-luna_v1.mp4` | 48,1 s | 0293af4beba3e4f49e598309591b3264fbf00bf60bd39efcb8ff42a76cebc7e7 |
| 03 | `03-tostada_v1.mp4` | 49,2 s | fd502ebbf8e627dd584d809c37702ecd834b4fa5332bb3a10bfe9cffd2427678 |

## Pasos
- [x] Reserva en `TASKS.md` (aa243e0). Quién: Jorge (contestado en el chat).
- [x] Tendencias: se usa `lotes/tendencias/2026-11-28.md` (turno de mañana). Las tres de Google Trends ya estaban usadas; se toman dos ideas de YouTube Studio · Investigación (segundo intercalar, estrellas en las fotos de la Luna) + un cotidiano.
- [x] 3 temas verificados (subagentes de lectura; 2+ fuentes por dato; lo que solo tenía una fuente se quitó: el 62 % de los niños con tostadas, fallos concretos de Reddit/Qantas, el último segundo de 2016).
- [x] Guiones (`motor.guion` sin ❌). Voz API desde el Mac: 2.391 caracteres; quedan ≈5.900.
- [x] Arte nuevo `generadores/ilus_1128t.py`: relojes digitales (59/60/00), reloj atómico, servidores (normal y con fallo), sala de votación, astronauta (dos poses), suelo lunar (normal, con estrellas, quemado), fotos con marco, diafragma, tostada (con y sin mantequilla), mesa de cocina, cocina, televisor antiguo, físico.
- [x] Generadores `gen_01..03.py` (21, 27 y 22 planos), hojas revisadas, render, ffprobe, `motor.calidad` sin ❌ (66, 60, 55). Se arregló un ❌ de ritmo en el 02 con micro planos, el arranque del 03 (la tostada ya cae en el fotograma 0) y tres rótulos con poco contraste.
- [x] Portadas, fichas de variables, vídeos y portadas al chat, MP4 y portadas copiados al Mac, correo (id 1a2231f1ddc15690).

## Decisiones según las estadísticas
- **[firme] primer segundo**: reloj que salta a 23:59:60; astronauta bajo cielo negro; tostada cayendo. Primeras frases de 4–5 palabras.
- **[firme] guiones cortos**: 151, 141 y 148 palabras.
- **[tendencia] Cotidiano**: el 03.
- **Experimento del lote: gancho de negación en el 01** («Este segundo no existe.»).

## Prueba del primer segundo
| # | Objeto grande en acción en el fotograma 0 | Primera frase | Alcance |
|---|---|---|---|
| 01 | Reloj digital enorme que salta de 23:59:59 a 23:59:60 en rojo | «Este segundo no existe.» (4) | universal |
| 02 | Astronauta grande en la Luna con cielo negro y un círculo que busca estrellas | «¿Dónde están las estrellas?» (4) | universal |
| 03 | Tostada enorme cayendo y girando | «Se te cae la tostada.» (5) | universal |

## Datos con cuidado
- 01: «hasta un minuto en un siglo» es la propuesta de la CGPM (el límite exacto quedó para decidir en 2026); el guion lo dice como plan. No se dice el año del último segundo (solo una fuente).
- 02: la comparación con la farola es nuestra (analogía), no de las fuentes.
- 03: «una mesa normal» (el paper usa 75 cm; Wikipedia, 0,7–1,8 m). La prueba de la tele británica (BBC, 300 lanzamientos al aire, mitad y mitad) está en Wikipedia y en el paper.
- Ganchos de Studio · Investigación: son ideas de otros canales del nicho (`reciclado=sí` en el 02); versión y guion propios.

## Avisos justificados (⚠ de `motor.calidad`)
Densidad baja (3–5 elementos por plano), pocos fondos, ritmo poco variado y pocos micro planos: se dejan así en v1 por hacerlo por adelantado y rápido; los textos se leen todos y cada plano tiene acción.
