# Estado — lote 2026-11-17-tarde

- **Estado**: **en revisión** (v1). Esperando «ok» en el chat.
- **Agente**: Agente 20:00 (Jorge) · Mac de Jorge (`jorges-macbook-air-2`) · carpeta local `Documents/Parece Mentira/lotes/2026-11-17-tarde`
- **Chat del lote**: https://claude.ai/code/session_019BG1dHf6SfJ6MbfA5kmnCP (3 MP4 y 3 portadas enviados)
- **Correo de aviso**: enviado a parecementirapero.media@gmail.com, id `1a1eaf34810f56dd`.

## Vídeos (v1)
| # | Archivo (Mac de Jorge) | Duración | Planos | SHA-256 | Calidad | Portada |
|---|---|---|---|---|---|---|
| 1 | `01-rayo-sol_v1.mp4` | 54,9 s | 35 | `8c30ea42a04ee6e215fe9a8a25e7e9d243a968db1b6e8b06c0f80f6187a94707` | 84/100 | «Más caliente que el Sol» · centro · 0,75 s |
| 2 | `02-sol-pasado_v1.mp4` | 54,6 s | 28 | `b198ee1243a5c2d694878e5a4cb22bf777851e7e36f628973c4b57718b291b72` | 87/100 | «Ese Sol ya es pasado» · abajo · 31,75 s |
| 3 | `03-cebolla_v1.mp4` | 56,7 s | 35 | `5cad744e7ec55cd16eee6655f3fc6f0aaa911fa0f1a283be626b70d283764c3e` | 93/100 | «Por qué lloras» · dato · 55,25 s |

SHA en el Mac = SHA del render (comprobado con `shasum`). En la carpeta local: MP4, SRT, manifiestos, locuciones, alineaciones, `NN-portadas/portada.jpg`.

## Arranque
- Studio (§1.8): **no se abrió** en este turno (se priorizó el lote); `studio.json` sin cambios.
- No hay experimento aprobado en `motor/APRENDIZAJE.md` ni abierto en `estadisticas/experimentos/`.
- ElevenLabs: antes 29.828 libres; después **28.812** de 40.000 (≈8 lotes; se renuevan el 15-12).

## Decisiones según las estadísticas
Base: `aprendizajes.md` (8 vídeos: todo tendencia/pista) y `estudio.md` (nada pasa de «pista»).
- «Espacio» y «comparación» son lo que mejor va (pista): 02 es Espacio, 01 es comparación (rayo frente al Sol).
- Audiencia latinoamericana: referencias universales (rayo, Sol, cebolla), sin expresiones de España («coche» cambiado por «guepardo»).
- Histórico es lo último en «se quedan» (pista): este lote va sin tema histórico; se dice en el correo para que lo decidan Nico y Jorge.
- **Experimento del lote**: **gancho de orden** en el 03 («Corta una cebolla.», 3 palabras; el único precedente, las uñas, dio 74 %). 01 (contraste) y 02 (dato) son el control. Espero que el 03 iguale o supere a 01/02 en «se quedaron viendo».
- Duración 55–57 s: la pista «40–50 s» choca con DECISIONS (150–160 palabras) → no se aplica.

## Prueba del primer segundo (AGENTE §2)
| # | Objeto único y grande moviéndose en el fotograma 0 | Primera frase (≤ 5) | Alcance |
|---|---|---|---|
| 01 | Un rayo que cae sobre la ciudad, con un termómetro que se dispara | «Más caliente que el Sol.» (5) | universal |
| 02 | El Sol que sube desde abajo (con un reloj atrasado) | «Ese Sol ya es pasado.» (5) | universal |
| 03 | Un cuchillo que cae sobre una cebolla enorme y salta el chorro | «Corta una cebolla.» (3) | universal |

## Temas
- De `IDEAS.md` (candidatos con objeto claro para el fotograma 0). Cada dato con ≥ 2 fuentes (`guiones.md`).
- Descartado a propósito el truco de «enfriar la cebolla»: el estudio de 2025 vio que las cebollas frías sueltan **más** gotitas.

## Control de calidad
- `ffprobe`: 1080×1920, 30 fps, h264, AAC 48 kHz estéreo; duración = locución + ≈0,5 s (54,5 / 54,2 / 56,2 s de voz).
- `motor.guion`: ✓ los tres. `construir`: ✓ todos los textos se leen. `motor.calidad --mp4`: **sin ❌** (84/87/93; `calidad-0N.md`).
- Corregido antes de entregar (hojas cada 1 s miradas): 03 tenía ❌ ritmo plano → 4 micro planos nuevos (azufre, lágrima, gotas, filo); rótulos con poco contraste → cápsula (01, 02, 03); planos del Sol por dentro sin detalle → núcleo más pequeño con partículas; cierre del 01 en bucle con el gancho; glifo «✕» sin fuente → «X»; «÷ 3» tapado por el cronómetro.
- ⚠ que quedan, justificados: «ritmo poco variado» (0,41–0,43, límite 0,45) y «menos de 3 micro planos» en 01/02: con la voz real las palabras caen cada 0,7–1 s y partir más los planos dejaría cortes sin sentido; 01 «plano pobre» a 15,1 s = fogonazo blanco a propósito (el golpe del rayo); 01/02 «mismo encuadre» 4–6 s en tramos de tormenta / núcleo (mismo escenario, distinta acción); 03 «plano con menos de 3 elementos» = gafas sobre el ojo (1,1 s).
- Cifras y nombres revisados contra guion y fuentes. Sin personas reales (siluetas sin rasgos).

## Ficha de variables (AGENTE §6, en prueba)
- `estadisticas/fichas.json`: 2026-11-17-tarde/01, /02 y /03 creadas antes de publicar (`ficha comprobar`: 0 problemas). experimento=no en la ficha (no hay experimento con ficha previa abierto).

## Generadores
`generadores/`: `NN-guion.txt`, `ilus_tarde.py` (≈40 SVG nuevos: rayo ×3, nube, tormenta con ciudad, campo de noche, termómetros, onda, oreja, refugio, silueta contando; Sol cortado, fotón, ojo, ojo lloroso, cara, interruptor, neandertal en silueta, hoguera, cueva, multitud; cebolla ×2, media cebolla, cuchillo afilado y romo, tabla, gotitas, gas, células, enzima, molécula con azufre, cámara, guepardo, gafas, piedra de afilar; reutiliza `ilus_lote.py` de la mañana) y `gen_0N.py DIR [locucion.mp3 alineacion.json]`. Render en la nube; resultados copiados al Mac.

## Publicación
- Pendiente del «ok» en el chat del lote.
