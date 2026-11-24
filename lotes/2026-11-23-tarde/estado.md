# Lote 2026-11-23-tarde — estado

**Estado**: 🟢 **publicado y programado en YouTube y TikTok**.
**Quién**: Jorge, con el agente, en el chat https://claude.ai/code/session_019BG1dFtXHqVXWrKbh8QXsf. El turno de las 20:00 del 23-11 no se hizo, y Jorge pidió hacerlo el 24-11 a las 00:47.
**Carpeta local**: `Documents/Parece Mentira/lotes/2026-11-23-tarde/` (Mac de Jorge). Ahí ya están las locuciones y las alineaciones. El Mac se desconectó durante el render. MP4, SRT, portadas y `metadatos.json` se copiaron al volver (01:20). Las copias para TikTok están en `PARA PUBLICAR/2311t-*`. Al pasar por el chat, el SHA de los MP4 cambia (MP4 reempaquetado, misma duración).

## Vídeos
| # | Título | Duración | SHA-256 corto | Calidad | Portada |
|---|---|---|---|---|---|
| 01 | No ves tus ojos moverse (pruébalo en el espejo) 👁️ | 51,8 s | fe583dc259a8 | 55/100 | «NO VES TUS OJOS MOVERSE» · ojo · 1,4 s |
| 02 | El Sol NO es amarillo ☀️ (es blanco) | 51,1 s | e8bf83b346bc | 59/100 | «EL SOL ES BLANCO» · Sol blanco en el espacio · 1,1 s |
| 03 | Di el COLOR, no leas 🎨 | 55,5 s | cb3430b1c921 | 46/100 | «DI EL COLOR, NO LEAS» · «AZUL» en rojo · 0,4 s |

Voz oficial: clon op8soO9fvP07F3mjbJuB, eleven_v4, 0,5 / 0,75. Llamada por API desde el Mac de Jorge.

## Decisiones
- Los temas los eligió el agente, siguiendo la línea que funcionó en el lote del 22-11: el cuerpo y la percepción, con prueba en casa. Estilo cartoon con contorno grueso, el que pidió Jorge el 23-11.
- 01 (Ciencia, experimento): movimientos sacádicos, enmascaramiento sacádico y la ilusión del reloj parado (cronostasis). Lleva prueba del espejo.
- 02 (Ciencia, mito y realidad): el Sol es blanco. La dispersión del azul explica el cielo azul y el Sol amarillento o rojo. El pico de emisión está en el verde. El guion dice «el color que emite con más fuerza es el verde», que es la formulación de Stanford Solar Center.
- 03: **experimento del lote: formato interactivo** (test Stroop). Las dos rondas del test van **cada una en un solo plano fijo**, sin cortes ni zoom, siguiendo la regla de Jorge del 23-11 («no cambies el plano… porque lía»). Se quita el empujón automático de cámara del primer plano. Ronda 2: 7 palabras de color que no coinciden, una cada ≈0,7 s. La portada no destripa el test.

## Prueba del primer segundo
- 01: un ojo grande que salta de lado a lado · «No ves tus ojos moverse.» (5)
- 02: un Sol blanco enorme en el espacio · «El Sol es blanco.» (4)
- 03: «AZUL» escrito en rojo en una pizarra · «Di el color.» (3)

## Control de calidad
- `construir`: todos los textos se pueden leer, en los tres.
- ffprobe: 1080×1920, h264, AAC.
- `motor.calidad --mp4`: **sin ❌**. Notas 55/59/46 (`calidad-0N.md`).
  - Los ⚠ son de ritmo y densidad: pocos micro planos y 19–28 cortes por minuto. Es el precio del estilo cartoon con planos legibles.
  - En el 03, el plano de 6 s es la ronda 2 del test, fija a propósito.
- Hojas de fotogramas revisadas. Arreglado antes del render:
  - Espejo con el muñeco delante.
  - Rótulos amarillos sin cápsula sobre cielo o pizarra, pasados a cápsula (ilegibles).
  - «AMARILLO» quitado de la ronda 2 (no daba tiempo a leerlo).
  - «FRENA» separado de la palabra.
- Fichas de variables: 3 nuevas. `ficha comprobar`: 0 problemas.

## Fuentes
En `metadatos.json` → `fuentes`. Son:
- Saccadic masking y Chronostasis (Wikipedia), y Yarrow et al. 2001.
- Stanford Solar Center, Science News Explores y WTAMU.
- APA, Stroop 1935 (York University), Simply Psychology y EBSCO.

## Publicación (2026-11-24 01:20–01:45)
Jorge: «quiero que subas ahora uno con su portada, el siguiente mañana a las 10 y el último a las 12», y luego «súbelos a youtube y tiktok en los horarios que te he dicho». Se entiende «mañana» como hoy 24-11 por la mañana (el mensaje es de la 01:15).
- YouTube por API desde el Mac, con portada:
  - 01 https://youtube.com/shorts/NcDWZOO-cEw (público)
  - 02 https://youtube.com/shorts/VIZRXKQ8eHQ (10:00)
  - 03 https://youtube.com/shorts/CcqDZeF_IjA (12:00)
- **Falta repasar en Studio que las portadas se han quedado**. El `--solo-portada` de repaso se cortó: Jorge paró la orden.
- TikTok desde el navegador integrado, con texto (comprobado con `innerText`) y portada de imagen elegida por Jorge:
  - 01 https://www.tiktok.com/@parece.mentira85/video/7711527702997650710 (publicado 01:26)
  - 02 https://www.tiktok.com/@parece.mentira85/video/7711528083202886934 (10:00)
  - 03 https://www.tiktok.com/@parece.mentira85/video/7711528522870836502 (12:00)

## Siguiente paso
Revisar las miniaturas en YouTube Studio. Comentarios fijados (necesitan la verificación de Studio).
- Correo de revisión: `1a20ae5fe9867987`.
