# Lote 2026-11-25-manana — estado

**Estado**: 🟡 **pendiente de voz**. Guiones, metadatos, ilustraciones y montaje hechos (tiempos provisionales, hojas revisadas). Falta la locución de ElevenLabs → render → calidad → portadas → entrega.
**Quién**: Nico (con el agente), lote pedido a mano en https://claude.ai/code/session_019BG1dKEg4xbEPyKDNcseyw («haz el lote de la mañana para subirlo a las 11, 12 y 13»).
**Bloqueo**: el Mac de Nico contesta, pero la sesión no tiene conectada la carpeta `Documents/Parece Mentira` (la petición de acceso fue denegada por el modo automático). Sin ella no hay `claves.txt` ni dónde dejar los MP4. Se desbloquea con **+ → «Add folder» → `Documents/Parece Mentira`** en la app de escritorio y escribiendo en ese chat.

## Vídeos
| # | Título | Palabras | Caracteres de voz |
|---|---|---|---|
| 01 | El telescopio Hubble nació miope 🔭👓 | 160 | 974 |
| 02 | Por qué se te arrugan los dedos en el agua 🖐️💧 | 157 | 879 |
| 03 | Este olivo conoció a Roma (y sigue dando aceitunas) 🌳🏛️ | 155 | 898 |

Voz prevista: ≈2.750 caracteres de los ≈14.000 que quedaban el 24-11 por la noche.

## Cómo se retoma (≈25 min con el Mac)
1. Créditos (`/v1/user/subscription`) y voz por API desde `device_bash` (una toma por vídeo, `with-timestamps`) con `generadores/NN-guion.txt`.
2. `python3 generadores/gen_0N.py DIR NN-locucion.mp3 NN-alineacion.json` → `motor.render` → `motor.calidad --mp4`.
3. Portadas, fichas, entrega en el chat y correo.

## Tendencias de hoy
`lotes/tendencias/2026-11-25.md`. Dos vídeos salen de tendencias: 01 («nasa», Colombia: foto nueva del Hubble) y 03 («aceite de oliva», España; el feed de España venía con datos viejos, así que cuenta como tema de siempre). El 02 sale de las estadísticas.

## Decisiones según las estadísticas
- **01 Hubble**: tema Espacio, el mejor en % visto y en «se quedan» (tendencia). Gancho de dato de 4 palabras con el objeto ya moviéndose.
- **02 Dedos — experimento del lote: gancho en segunda persona (H3 de `motor/APRENDIZAJE.md`)**, «Mira tus dedos mojados.», en un tema Cotidiano (el de más vistas medias en YouTube) y con estructura de experimento (la mejor en «se quedan»). Se espera más del 65 % de «se quedaron viendo».
- **03 Olivo**: Histórico es el tema que peor retiene; se cuenta desde el presente (el árbol sigue vivo y da aceitunas) y con una comparación (Colón), la estructura con más vistas.
- Subidas separadas (firme): ver «Horario».

## Prueba del primer segundo
| # | Objeto que ya se mueve en el fotograma 0 | Primera frase |
|---|---|---|
| 01 | El telescopio entra desde abajo delante de una estrella borrosa que late | «Este telescopio nació miope.» (4) |
| 02 | Una mano con los dedos arrugados sale del agua chorreando | «Mira tus dedos mojados.» (4) |
| 03 | Un olivo enorme de tronco retorcido entra desde abajo | «Este árbol conoció a Roma.» (5) |
Alcance: universal en los tres.

## Control de calidad (hasta ahora)
- `motor.guion`: sin ❌ (160/157/155 palabras). ℹ en el 02: «pocos datos concretos» (9): el detector no cuenta los pasos del mecanismo (nervios, vasos, yema, piel), que son las imágenes del vídeo.
- `construir` con tiempos provisionales: sin avisos de lectura en los tres. Hay que volver a mirarlo con la voz real.
- Hojas de fotogramas (1 por segundo) revisadas en los tres. Arreglado: fondo claro bajo el subtítulo en los planos del espejo cortado (01), astronautas demasiado pequeños (01), plano de 4 s partido en dos (01), rótulos que no daban tiempo a leerse (01, 02, 03).
- Falta: `motor.calidad --mp4`, ffprobe, fichas de variables.

## Horario
Nico pidió 11:00, 12:00 y 13:00. A las 10:00 y a las 12:00 de hoy salen el 02 y el 03 del lote 2026-11-24-tarde (YouTube y TikTok), así que a las 12:00 coincidirían dos vídeos. Propuesta hecha en el chat: 11:00, 13:00 y 14:00. Pendiente de su respuesta y del «ok».

## No hecho
Datos de YouTube Studio (§1.8), TikTok Creative Center y Studio → Investigación (sin navegador en ese momento), comentarios (§8b).

## Fuentes
En `metadatos.json` → `fuentes` y en `guiones.md`.
