# Estado — lote 2026-11-17-tarde

- **Estado**: **01 v3 y 02 v3 publicados en YouTube** (2026-11-17, Nico); TikTok pendiente; 03 v2 sin publicar.
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

## Publicación (2026-11-17, chat del Mac de Nico)
Aprobación: Nico, «sube los vídeos que me he descargado del lote de Jorge» (en su Mac: 01 v3 y 02 v3, SHA-256 iguales a los de abajo). El 03 v2 no estaba descargado: sin publicar.
| # | YouTube | TikTok |
|---|---|---|
| 01 v3 | https://youtube.com/shorts/dOdQj9QyoBI — público, 23:00 | pendiente |
| 02 v3 | https://youtube.com/shorts/cjSc0D_gOaI — programado 2026-11-17 23:59 (hora de Madrid) | pendiente |
- YouTube por API (`subir_youtube.py`) desde el Mac de Nico. Sin `--portada` (los `NN-portadas/portada.jpg` no están en ese Mac): falta elegir en Studio el fotograma `portada.t` (0,75 s y 31,75 s).
- Instagram: no se publica (DECISIONS, cuenta cerrada).
- Falta: TikTok (navegador; la persona elige el archivo), comentarios fijados.

## v3 de 01 y 02 (≈21:10): menos relojes
Pedido: «que no salgan tantos relojes, alguno que otro está bien pero muchos no, y que si una escena acaba con un reloj no salga al principio de la siguiente; guarda todo lo demás y esto también».
- 01: de 5 relojes a 2 («¿cuánto dura?» y «nueve segundos»); «el sonido tarda tres segundos» = ondas que viajan hacia la oreja sobre el mar; «divide entre tres» = la silueta cuenta con los dedos. `01-rayo-sol_v3.mp4` · 54,9 s · `d222c71c3c548c068eef2976cace9ced5de862c64e0349c433ef8ce557b490fa` · 79/100 sin ❌.
- 02: de 4 a 1 («8 min 20 s»); fuera el reloj del gancho y del cierre (el Sol sube con estrellas fugaces); «+8 min» = la última luz llegando a la Tierra con estela. `02-sol-pasado_v3.mp4` · 54,6 s · `2855b9726c7b21da89f8c98c63cd201b6d5805e22c4bc9321944016a131a1949` · 87/100 sin ❌.
- 03: sin relojes; sigue la v2.
- Reglas guardadas en `DECISIONS.md` («Variedad y claridad en los planos») y `motor/DENSO.md`. MP4 v3 solo en el chat (sin enlace con el Mac).

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
- ≈21:20: en el chat piden «súbelos a TikTok e YT» (01 v3, 02 v3, 03 v2; Instagram no). **Bloqueado**: el Mac de Jorge no responde (bridge desconectado), así que no se pueden copiar los MP4 a la carpeta local, ni usar `subir_youtube.py` (el token está en `claves.txt` del Mac), ni el navegador integrado para TikTok. Además el protocolo pide escribir «ok» tal cual para publicar. Nada publicado.
- ≈22:50 («hazlo ya», desde el Mac de Nico): el Mac de Jorge volvió a responder; los MP4 finales (01 v3, 02 v3, 03 v2) ya están en `Documents/Parece Mentira/lotes/2026-11-17-tarde/` del Mac de Jorge (SHA comprobado). Comprobado en Studio que no estaban subidos. **Sigue bloqueado**: el Mac de Jorge no tiene el permiso de subida de YouTube (`YT_UPLOAD_REFRESH_TOKEN`, TASKS) y en el navegador integrado el archivo lo tiene que elegir una persona delante de ese Mac (Claude no puede manejar el selector; no hay Chrome conectado). Camino: publicar desde el Mac de Nico (tiene el permiso de YouTube) bajando los MP4 de este chat, o con alguien delante del Mac de Jorge.
- ≈23:00: la persona dice que ha descargado los MP4 (Mac de Nico) y que la cuenta de Instagram la han cerrado → solo YouTube y TikTok (DECISIONS). Desde esta sesión sigue sin poder subirse; se dejan en el chat los textos listos para subirlos a mano o desde una sesión en el Mac de Nico.

- 2026-11-18 (comprobado en YouTube Studio y TikTok Studio desde el Mac de Jorge): **YouTube**: 01 rayo publicado el 17-11 (lo subió una persona; no consta si es la v1 o la v3); **faltan 02 Sol y 03 cebolla**. **TikTok**: **faltan los 3**.
