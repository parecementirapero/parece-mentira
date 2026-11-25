# Lote 2026-11-25-manana — estado

**Estado**: 🟢 **programado en YouTube** para el 26-11 a las 11:00, 12:00 y 13:00 («súbelos pero para mañana a las 11, 12, 13», Nico, 25-11 19:39). TikTok: ver «Publicación». Antes: en revisión (v1). Vídeos y portadas en el chat https://claude.ai/code/session_019BG1dKEg4xbEPyKDNcseyw; falta el «ok» de Nico y el horario. Sin correo: Nico estaba en el chat.
**Quién**: Nico (con el agente), lote pedido a mano («haz el lote de la mañana para subirlo a las 11, 12 y 13»). Por la mañana quedó pendiente de voz (la carpeta del Mac no estaba conectada y luego el Mac se desconectó); se retomó a las 19:20, cuando Nico escribió «sigue» y aprobó el acceso a `Documents/Parece Mentira`.
**Carpeta local**: `Documents/Parece Mentira/lotes/2026-11-25-manana/` (Mac de Nico): locuciones, alineaciones, MP4, SRT, manifiestos, portadas (`NN-portadas/portada.jpg`), `metadatos.json` y `voz.py`.

## Vídeos
| # | Título | Duración | SHA-256 corto (nube / Mac) | Calidad | Portada |
|---|---|---|---|---|---|
| 01 | El telescopio Hubble nació miope 🔭👓 | 56,8 s | cf5f40ab86f5 / 611563e0a705 | 91/100 | «LE PUSIERON GAFAS» · arriba · 56,2 s |
| 02 | Por qué se te arrugan los dedos en el agua 🖐️💧 | 57,0 s | 22918d61ed55 / c9d190d62e9f | 88/100 | «¿POR QUÉ SE ARRUGAN?» · arriba · 48,8 s |
| 03 | Este olivo conoció a Roma (y sigue dando aceitunas) 🌳🏛️ | 55,4 s | c94e0bafb40e / c0dc698f292d | 87/100 | «1.700 AÑOS VIVO» · abajo · 1,2 s |

Voz oficial: clon op8soO9fvP07F3mjbJuB, eleven_v4, 0,5 / 0,75, por API desde el Mac de Nico (una toma por vídeo, texto de la alineación idéntico al guion). Créditos: 14.012 → 12.911.

**Tomas largas, recortadas sin gastar otra voz** (`Video(..., omitir=…)`): la voz salió más lenta de lo previsto (≈2,5 palabras/s).
- 01: 64,2 s → 56,8 s. Fuera dos frases enteras: «Costó mil quinientos millones de dólares.» y «La causa: una pieza del aparato de medir estaba un milímetro fuera de su sitio.»
- 03: 60,5 s → 55,4 s. Fuera «Y no está solo: en ese mismo pueblo hay más de mil trescientos olivos milenarios.»
- **Los empalmes no se han oído** (el agente no puede escuchar): 01 hacia los segundos 6 y 22; 03 hacia el segundo 39. Hay que oírlos antes del «ok».

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

## Control de calidad
- `motor.guion`: sin ❌ (160/157/155 palabras). ℹ en el 02: «pocos datos concretos» (9): el detector no cuenta los pasos del mecanismo.
- `construir` con la voz real: todos los textos se pueden leer, en los tres.
- ffprobe: 1080×1920, 30 fps, h264, AAC, en los tres.
- `motor.calidad --mp4`: **sin ❌**. Notas 91/88/87 (`calidad-0N.md`). Arreglado antes del render final: ❌ de ritmo plano en el 01 y el 03 y ⚠ en el 02 (7, 6 y 8 micro planos de ≈0,5 s en la última palabra de la frase), dos rótulos sin tiempo de lectura, «MANCHAS» con poco contraste.
- ⚠ que quedan, sin arreglar: pocos fondos distintos (5–6) en los tres; en el 01 un plano con pocos elementos y otro pobre (la moneda sola, 39,9 s); en el 02 y el 03, tramos de 6–7 s con el mismo encuadre; en el 03, 4,8 elementos por plano.
- Hojas de fotogramas revisadas (con tiempos provisionales cada 1 s y, con la voz real, cada 2 s).
- Portadas: las 8 candidatas automáticas del 01 y del 03 no enseñaban al protagonista; se hicieron a medida con `motor.portadas.componer` sobre un fotograma elegido. La del 02 es la candidata 2 de la hoja.
- Fichas de variables: 3 nuevas; `ficha comprobar`: 0 problemas.

## Horario
Nico pidió 11:00, 12:00 y 13:00, pero el lote se terminó a las 19:45. Pendiente de que diga horas nuevas junto con el «ok» (separados entre sí y del lote de las 20:00).

## No hecho
Datos de YouTube Studio (§1.8), TikTok Creative Center y Studio → Investigación, comentarios (§8b), correo del turno.

## Fuentes
En `metadatos.json` → `fuentes` y en `guiones.md`.

## Publicación (2026-11-25 19:40–)
Nico: «súbelos pero para mañana a las 11, 12, 13».
- YouTube por API desde el Mac de Nico, en privado con publicación programada y portada puesta por la API en los tres:
  - 01 https://youtube.com/shorts/E1QFyVyJ7kU (26-11 11:00)
  - 02 https://youtube.com/shorts/0nGefmtqxcs (26-11 12:00)
  - 03 https://youtube.com/shorts/8ISC2-AoXSM (26-11 13:00)
- Copias para TikTok en `PARA PUBLICAR/2511m-*` (vídeos y portadas), Mac de Nico.
- `etiquetas.json` al día. Falta `ficha publicar` con los números de TikTok y los comentarios fijados (cuando sean públicos).
