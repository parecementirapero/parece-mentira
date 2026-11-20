# Estado — lote 2026-11-20-manana

**Estado**: en revisión (v1) · Agente 08:00 (Nico) · rama `main`
**Chat del lote** (vídeos y «ok»): https://claude.ai/code/session_019BG1dLEec78Rq3eZBDrkLR
**Correo de aviso**: (se apunta al enviarlo)

## Cronología
- 17:26 (Madrid) se dispara la tarea de las 07:52 (≈9,5 h tarde). El lote no existía → se crea.
- 17:28 reserva en `TASKS.md` + regla «Temas según las tendencias del día» registrada en `DECISIONS.md` y `AGENTE.md` §2 (push `a970cb4`).
- 17:35–17:50 análisis de tendencias → `lotes/tendencias/2026-11-20.md` (push antes de los guiones).
- Voz oficial por API desde el Mac de Nico (créditos antes: 24.158). Montaje, render y control en la nube.
- El puente con el Mac se cayó un rato durante el render y volvió; los MP4 sí se copiaron a `Documents/Parece Mentira/lotes/2026-11-20-manana/`.

## Tendencias de hoy
Archivo: [`lotes/tendencias/2026-11-20.md`](../tendencias/2026-11-20.md). Fuentes: Google Trends MX/AR/CO/ES ✅; TikTok Creative Center ❌ (pide iniciar sesión); YouTube Studio → Investigación ❌ («se ha producido un error»).
Los **tres** vídeos salen de tendencias del día (encajaban sin forzar y sin depender de la noticia):
- 01 ← «fiona hipopótamo» (MX, CO, ES): no se habla de la noticia (la hipopótamo del zoo se tragó un gorro y está bien); el vídeo es sobre cómo «nadan» los hipopótamos.
- 02 ← «gran premio de las vegas» (MX, AR): física de la carga aerodinámica; Las Vegas solo en la descripción. Sin equipos, pilotos ni marcas.
- 03 ← «tesla argentina» (AR): historia del coche eléctrico, sin nombrar ninguna marca.
Quedan para la tarde: Vuelta de Obligado (con cuidado: batalla y fecha patria), Sierra Nevada / África, cambio climático.

## Decisiones según las estadísticas
- **[firme] primer segundo**: los tres arrancan con un único objeto grande ya moviéndose (hipopótamo hundiéndose, monoplaza en el techo, bólido levantando polvo) y gancho de 4–5 palabras. Espero > 65 % «se quedaron viendo».
- **[firme] Latinoamérica**: sin expresiones de España; «coche» se mantiene (lo marca `motor.guion` como ℹ) y en descripciones/hashtags va también «autos».
- **[tendencia] más Espacio, menos Histórico**: hoy ninguna tendencia daba un tema de espacio; el 01 usa la Luna como comparación (astronauta botando). El 03 es histórico, pero contado desde algo de hoy (los eléctricos).
- **Experimento (uno)**: 03 → gancho de **contraste de época en dos golpes** («Este bólido es eléctrico. / Y de 1899.»). Espero que el contraste antiguo/moderno retenga como un gancho de dato. 01 (negación) y 02 (dato) siguen lo que mejor va.
- Etiqueta nueva `tendencia` en `metadatos.json` → `etiquetas` para medir si los temas de tendencia funcionan mejor.

## Prueba del primer segundo
| Vídeo | Objeto grande moviéndose en el fotograma 0 | Primera frase |
|---|---|---|
| 01 | el hipopótamo cayendo al fondo del río | «Los hipopótamos no nadan.» (4) |
| 02 | el monoplaza boca abajo pegado al techo del túnel | «Podría ir por el techo.» (5) |
| 03 | el bólido de torpedo corriendo con polvo | «Este bólido es eléctrico.» (4) |
Alcance: los tres `universal`.

## Vídeos (v1)
| # | Archivo | Duración | SHA-256 (corto) | Calidad | Portada |
|---|---|---|---|---|---|
| 01 | `01-hipopotamos-no-nadan_v1.mp4` | 57,7 s | `3852405fbcb2` | 75/100, sin ❌ | «NO SABEN NADAR» · arriba · 3,8 s |
| 02 | `02-formula-uno-por-el-techo_v1.mp4` | 56,1 s | `842aac2f2ca8` | 69/100, sin ❌ | «BOCA ABAJO A 200» · dato · 2,8 s |
| 03 | `03-bolido-electrico-1899_v1.mp4` | 55,7 s | `1b6e4dcf7197` | 74/100, sin ❌ | «ELÉCTRICO EN 1899» · arriba · 0,8 s |

ffprobe: 1080×1920, 30 fps, H.264 + AAC 48 kHz en los tres. Hojas de fotogramas revisadas (se corrigieron: hipopótamo en la orilla dibujado dentro del agua → fondo de sabana sin río; agua de la cabeza que dejaba un rectángulo; coche del techo pegado al subtítulo; anillos de orejas/nariz; rótulos de poco contraste con cápsula).
**Versión corta (`omitir`)**: 01 sin «Unas tres décimas de segundo.» y 03 sin «Su nombre, en francés…» y «Y no era una rareza.», para no pasar de 60 s. Oír los empalmes antes del «ok» (01 a los ≈54 s; 03 a los ≈4,4 s y ≈18,6 s).

### ⚠ de `motor.calidad` que se quedan (justificados)
- Densidad 4,4–4,7 elementos por plano y algunos «planos pobres» (gotas, NO, etiquetas): son planos de golpe con un solo objeto a propósito.
- «Mismo encuadre» y «planos casi iguales» en tramos del túnel (02) y de la calle de 1900 (03): es el mismo escenario con acciones distintas.
- Movimiento del primer segundo 3,3–3,9 (objetivo 5,5): el sujeto entra con muelle y la cámara empuja; no hay ❌.
- 03 con 2 micro planos (pide 3); el ritmo pasa (variación 0,5).

## Fichas de variables
`estadisticas/fichas.json` → 2026-11-20-manana/01, 02, 03 (antes de publicar; `ficha comprobar` sin problemas).

## No hecho en este turno
- Lectura de YouTube Studio (§1.8) y respuestas a comentarios (§8b): el turno empezó 9,5 h tarde y el puente con el Mac se cortó durante el render; se priorizó entregar el lote.
- Nada publicado: falta el «ok».

## Siguiente paso
«ok» (o «ok 1 y 3») en el chat del lote → AGENTE §8 desde el Mac de Nico (YouTube por API con `--portada`, TikTok desde el navegador integrado). Instagram ya no se usa.
