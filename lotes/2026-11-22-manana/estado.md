# Lote 2026-11-22-manana — estado

**Estado**: 🟢 **en revisión** (v1 de los 3 vídeos en el chat; falta el «ok»). Correo `1a202b869e5a1939`.
**Agente**: Agente 08:00 (Nico). Chat del lote (vídeos y «ok»): https://claude.ai/code/session_019BG1dJXULpjXQekLYXshSe · chat de la primera ejecución sin Mac: https://claude.ai/code/session_019BG1dJVmPqrtbuKRGs1cfJ

## Registro
- 2026-11-22 10:18 (Madrid): la tarea de las 07:52 se disparó a las 10:18 y arrancó en la nube **sin acceso al Mac de Nico** (la ejecución no tuvo el puente del ordenador: ni carpeta local, ni `claves.txt`, ni navegador integrado).
- Sin `claves.txt` no hay clave de ElevenLabs → no hay voz posible (no hay voz alternativa, DECISIONS). Siguiendo AGENTE §1.6 no se producen guiones ni montaje. Nada gastado ni publicado.
- 10:24: esta ejecución era el lanzamiento a mano de las 10:18, pedido en el chat del proyecto porque el turno de las 08:00 no se ejecutó. Al retomar (arranque idempotente), el lote ya existía y el Mac seguía sin conexión: no se duplica nada ni se manda otro correo.
- Sí se hizo el análisis de tendencias (solo lectura, desde la nube) para que lo tenga el turno de tarde: `lotes/tendencias/2026-11-22.md`.

## Retomado con el Mac (10:30)
- 10:26: nueva ejecución de la tarea (https://claude.ai/code/session_019BG1dJXULpjXQekLYXshSe). Esta vez el Mac de Nico **sí responde** (`get_device_info` y carpeta local OK). Créditos ElevenLabs: 20.837 (≈ 6 lotes). Se reserva el lote y se hace entero.

## Vídeos (v1)
| # | Título | Archivo (Mac de Nico, `lotes/2026-11-22-manana/`) | Duración | SHA-256 | Calidad |
|---|---|---|---|---|---|
| 01 | El baloncesto empezó con cestas de melocotones 🧺🏀 | `01-canasta-con-fondo_v1.mp4` | 54,0 s | `e6df8b7b8518` | 78/100, sin ❌ |
| 02 | Tu sangre viene de una estrella que explotó 💥🩸 | `02-sangre-de-estrellas_v1.mp4` | 55,0 s | `3314e2b1cb15` | 85/100, sin ❌ |
| 03 | Tus ojos ven el mundo al revés 👁️🙃 | `03-imagen-al-reves_v1.mp4` | 49,3 s | `a03b865fb890` | 80/100, sin ❌ |

Voz oficial por API desde el Mac (2.377 caracteres; créditos 20.837 → ≈18.460). 38/38/34 planos. ffprobe: 1080×1920, 30 fps, h264, AAC 48 kHz. Render en la nube; MP4 y portadas copiados al Mac. Los `.srt` y manifiestos se quedaron en la nube (no se copiaron al Mac).

## Tendencias de hoy
- Archivo: [`lotes/tendencias/2026-11-22.md`](../tendencias/2026-11-22.md).
- Elegida: **«bàsquet» (ES)** → 01. Motivo: dato universal, verificado con 4 fuentes, y con un objeto que se mueve en el fotograma 0 (el balón cae en la cesta y se queda).
- No usadas y libres para la tarde: «luz a precio negativo» (ES) y «fruta en la frontera» (MX), por verificar.
- 02 y 03 no salen de tendencias (no había más que encajaran): son temas nuevos elegidos con las estadísticas.

## Decisiones según las estadísticas
- **01** (Histórico, reconstrucción, gancho de dato de 4 palabras): histórico es el tema que peor retiene, así que se cuenta desde un objeto que todo el mundo conoce (la canasta) y se sube a la tendencia del día. Espero un resultado en la media del canal.
- **02** (Espacio, cadena de datos): Espacio gana en vistas y en «se quedan» [tendencia] y «cadena de datos» es la estructura que más retiene. **Experimento del lote: gancho en segunda persona (H3)**, «Tu sangre viene de estrellas.»; ficha con `experimento=H3`, `brazo=A`. Espero «se quedaron viendo» > 65 %.
- **03** (Ciencia, experimento, gancho de dato de 5 palabras): Ciencia es el segundo tema; 49 s, cerca del tramo 40–50 s que mejor va [tendencia]. Sin experimento.
- Tres estructuras distintas; ganchos de 4–5 palabras; fotograma 0 con un solo objeto en acción.

## Prueba del primer segundo
- 01: (1) un balón de cuero cae dentro de una cesta de mimbre; (2) «Esta canasta tenía fondo.» · alcance universal.
- 02: (1) una gota de sangre sale disparada de una estrella que explota; (2) «Tu sangre viene de estrellas.» · universal.
- 03: (1) un árbol y todo el paisaje dan la vuelta; (2) «Esta imagen está al revés.» · universal.

## Avisos de calidad justificados (ningún ❌)
- Los tres: «ritmo poco variado» (0,37–0,42; objetivo ≥ 0,45) y «poca densidad» (≈4,8 elementos por plano). Hay micro planos (0,4–0,7 s) y planos de 2–3 s, pero menos contraste del deseable; se deja así por tiempo del turno.
- 01: «pocos fondos» (casi todo pasa en el gimnasio, a propósito); planos «pobres» 17 y 22 (micro planos «13» y «3 M»: solo la cifra, a propósito).
- 02: plano «pobre» 30 (un punto de luz en negro antes del Big Bang, a propósito).
- 03: «no se mueve nada en los primeros 0,6 s» es un falso aviso del control estático: el árbol y el fondo giran desde el fotograma 0 (movimiento medido en el MP4: 12,2, el más alto de los tres). «DERECHA» llega a y=1387 (dentro de la zona segura). El cierre no enlaza del todo en bucle.
- Rótulos recolocados por la zona segura: revisados en las hojas de fotogramas.

## Portadas (sin «ok»)
- 01 «LA CANASTA TENÍA FONDO» · arriba · 7,3 s. 02 «TU SANGRE VIENE DE ESTRELLAS» · abajo · 1,2 s. 03 «VES EL MUNDO AL REVÉS» · arriba · 4,0 s. Las automáticas no sacaban al sujeto, así que se generaron con `motor.portadas.generar()` sobre fotogramas elegidos; la variante de texto de 02 y 03 se generó pero su hoja no se miró.

## Después de la entrega (11:45, nueva ejecución de la tarea: el lote ya existía, no se duplicó nada)
- **YouTube Studio (§1.8)**: «se quedaron viendo» de 7 Shorts con 24 h o más, en `estadisticas/studio.json`: el Turco 69,7 %, El Niño 65,9 %, el dólar 59,1 %, lote 18-tarde 02 71,5 % y 03 79,7 % (10,1 mil vistas), 16 amaneceres 45,5 %, Mulhacén 58,6 %. Los flamencos aún no tenían 24 h; `cjSc0D_gOaI` no cargó. Las horas de `ng543OmyPag` no se pudieron leer.
- **Comentarios (§8b)**: 6 respuestas en YouTube (todas las «sin responder»): el Turco (1), estrella de neutrones (2), GTA 6 (2), koala (1). Ninguno saltado. TikTok Studio no se miró.

## No hecho
- TikTok Creative Center y Studio → Investigación en el análisis de tendencias; comentarios de TikTok.
- Nada publicado: se espera el «ok» en el chat del lote.
