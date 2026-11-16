# Estado — lote 2026-11-16-manana

- **Estado**: en revisión (v1), esperando «ok» en el chat del lote.
- **Agente**: Agente 08:00 (Nico) · MacBook Air de Nico · carpeta local `Documents/Parece Mentira/lotes/2026-11-16-manana`
- **Chat del lote**: https://claude.ai/code/session_019BG1dHPaoMtT9aEtopJ3JF
- **Correo de aviso**: enviado a parecementirapero.media@gmail.com, id `1a1e5cd4c9bf08da`
- **Arranque**: la tarea programada (07:52) se disparó a las 19:48 Europe/Madrid. Reserva en TASKS a las 19:49.

## Vídeos (v1)
| # | Archivo (Mac de Nico) | Duración | SHA-256 (MP4 en el Mac = render) | LUFS | Voz |
|---|---|---|---|---|---|
| 1 | `01-planetas-entre-tierra-y-luna_v1.mp4` | 54,47 s | `806797a00e06ca51102178ab871b1edb580489e2105cad036b98008471f8110b` | −19,3 | OK |
| 2 | `02-pulpo-tres-corazones_v1.mp4` | 53,58 s | `a18027bd6c2945dc1e8002f8022405735b10466b082d26f04b9d4effb36c79fa` | −19,1 | OK |
| 3 | `03-vikingos-america-1021_v1.mp4` | 53,43 s | `4c3e99317d5aea1217467658117d5bb00904b3610d3f414f87952e16d5964b74` | −19,2 | OK |

Junto a cada MP4: `.srt`, `_manifest.json`, `NN-episodio.json`, `NN-locucion.mp3`, `NN-alineacion.json` y `NN-portadas/` (portada.jpg, hoja-portadas.jpg, portadas.json). Generadores en `generadores/` (repo): `ilus_m.py` (SVG nuevos: planetas, noche, mar, pulpo, corazones, casa con bombas, gotas, drakkar, carabela, mar del norte, Terranova, mapa, tronco, hacha, anillos, sol con tormenta, árbol) y `gen_0N.py` (un plano por frase sobre `comun_v4`).

## Voz
La voz v1 (`EuJOG4WNDCMcwTFrXKUc`) dio 404 «voice_not_found»: Nico la borró a las 19:55 de hoy y cambió la voz oficial (commit `d377b17`, que llegó durante este turno). Se generó con la voz oficial nueva de `DECISIONS.md` / AGENTE §4: «Archivo Oculto — Narración (clon)» `op8soO9fvP07F3mjbJuB`, `eleven_v4`, 0.5/0.75, `with-timestamps`. El texto de la tarea programada aún nombra la v1 (y Drive): hay que actualizarlo. ElevenLabs: 33.132 caracteres al empezar y ≈2.330 gastados → quedan ≈30.800.

## Decisiones según las estadísticas
`aprendizajes.md` (4 vídeos, todo «pista"): Espacio y la estructura de comparación ganan, el gancho de contraste gana en TikTok, 40–50 s algo mejor que 50–60 s, el 79 % de la audiencia con país es de Latinoamérica. «Se quedaron viendo»: pisada 76,5 %, moáis 55,6 % (studio.json ya tenía los datos de hoy).
- **01 Planetas**: Espacio + comparación + contraste, la combinación que mejor ha ido. Se espera que sea el más visto del lote. Sin experimento.
- **02 Pulpo**: **experimento del lote: gancho de negación** («No tiene un corazón: el pulpo tiene tres.», en pantalla desde el fotograma 0). Tema Ciencia con estructura de metáfora visual. Se espera más «se quedaron viendo» que los moáis (55,6 %), cerca del 65 %.
- **03 Vikingos**: Histórico + reconstrucción con salto temporal + contraste, como la guerra de Zanzíbar (1.270 vistas en YouTube). Sin experimento.
- Ganchos sin expresiones solo de España. Duración de 53–54 s: dentro de DECISIONS (45–60 s). No se recortó a 40–50 s porque es solo una pista.

## Control de calidad
- `ffprobe`: 1080×1920, 30 fps, h264 yuv420p, AAC 48 kHz estéreo; duración = locución + 0,5 s.
- Hojas de fotogramas sacadas del propio MP4 (1 cada 2 s) y revisadas: pantalla completa, sin título fijo, sin Nova, karaoke arriba, gancho entero en el fotograma 0, algo en movimiento en cada plano y final en bucle.
- Corregido antes de entregar:
  - 01: la Luna quedaba tapada bajo el panel del gancho; ahora va en y=640 y se dibuja por delante de Neptuno.
  - 01: Urano y Neptuno caían tarde.
  - 01: el brillo rojo de «no entran» no se veía.
  - 01: la etiqueta HUD «TIERRA» señalaba a Saturno en el primer plano.
  - 02: «O₂» no tenía glifo en la fuente; ahora pone «O2».
  - 02: la etiqueta «TÚ» estaba mal colocada.
  - 03: la carabela salía cortada en el borde.
- Cifras contrastadas con las fuentes (ver `guiones.md` → Verificación). En el 03 no se da el número de anillos ni el año exacto de la tormenta, porque las fuentes no coinciden (28 o 29 anillos, 992 o 993).

## Portadas (elegidas por el agente, sin «ok»)
- 01: «CABEN TODOS LOS PLANETAS», diseño dato, t = 41,8 s. La columna de planetas, igual que el fotograma 0.
- 02: «NO TIENE UN CORAZÓN», diseño dato, t = 47,3 s. El pulpo con los tres corazones.
- 03: «COLÓN LLEGÓ TARDE», diseño arriba, t = 3,3 s. El barco vikingo y la carabela al fondo. Las 8 candidatas automáticas salían todas de los anillos, así que se generaron candidatas solo con los planos de barcos usando `motor.portadas.generar`.

## Publicación
_(pendiente de «ok»)_
