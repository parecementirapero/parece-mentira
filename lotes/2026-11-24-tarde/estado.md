# Lote 2026-11-24-tarde — estado

**Estado**: 🟡 **en revisión** — esperan el «ok» en https://claude.ai/code/session_019BG1dJB3X8kpbAbFL1YoGS (correo `1a20f922774c58fd`).
**Quién**: Agente 20:00 (Jorge). La tarea de las 19:52 se disparó a las 22:30 (Madrid); el Mac de Jorge respondía.
**Carpeta local**: `Documents/Parece Mentira/lotes/2026-11-24-tarde/` (Mac de Jorge): locuciones, alineaciones, MP4, SRT, manifiestos, portadas (`NN-portadas/portada.jpg`) y `metadatos.json`. El SHA es el del archivo en el Mac (al pasar por el chat se reempaqueta).

## Vídeos
| # | Título | Duración | SHA-256 corto | Calidad | Portada |
|---|---|---|---|---|---|
| 01 | Tu gato NO nota el dulce 🐱🍰 | 53,0 s | 3d00da573904 | 73/100 | «TU GATO NO NOTA EL DULCE» · arriba · 3,3 s |
| 02 | En el espacio las lágrimas NO caen 😢🚀 | 56,2 s | 4c5112431524 | 97/100 | «LAS LÁGRIMAS NO CAEN» · dato · 1,8 s |
| 03 | Los vikingos NO llevaban cuernos ⚔️ | 54,5 s | 42f5282fdd85 | 78/100 | «VIKINGOS SIN CUERNOS» · dato · 11,8 s |

Voz oficial: clon op8soO9fvP07F3mjbJuB, eleven_v4, 0,5 / 0,75, por API desde el Mac de Jorge (una toma por vídeo). Créditos: 14.978 → 14.012.
Render en la nube (estilo cartoon del 23-11, `ilus_1124t.py` reutiliza todo el 23-11 tarde).

## Registro
- 22:31 reserva. 22:32 voz. 22:35–23:55 ilustraciones, montaje, hojas, render, calidad, portadas. Entrega en el chat y en el Mac, correo `1a20f922774c58fd`.
- No hecho por la hora: datos de YouTube Studio (§1.8), análisis de tendencias, respuesta a comentarios (§8b).

## Tendencias de hoy
No hay `lotes/tendencias/2026-11-24.md` (no hubo turno de mañana) y no se hizo el análisis por la hora de arranque. Los tres temas salen de las estadísticas. `tendencia: no` en los tres.

## Decisiones según las estadísticas
- **01 Gato**: tema Cotidiano, el de más vistas medias en YouTube (tendencia). Gancho de dato de 5 palabras, animal grande en el fotograma 0.
- **02 Lágrimas**: tema Espacio, el mejor en % visto y en «se quedan» (tendencia). Estructura experimento (la mejor en «se quedan»).
- **03 Vikingos — experimento del lote: gancho de negación en un tema Histórico.** Histórico es el tema que peor retiene (55 % se quedan); la negación tiene un solo vídeo y fue 2.º en «se quedan» (71 %). Se espera > 60 % de «se quedaron viendo». (El 02 también empieza negando, porque es la forma natural del dato; el experimento se mide en el 03.)

## Prueba del primer segundo
| # | Objeto que ya se mueve en el fotograma 0 | Primera frase |
|---|---|---|
| 01 | El gato con la lengua fuera entra desde abajo y el pastel llega deslizando | «Tu gato ignora el dulce.» (5) |
| 02 | La cara del astronauta sube y una bola de agua crece sobre su ojo | «Las lágrimas no caen.» (4) |
| 03 | El casco de cuernos bota y los cuernos salen disparados | «Los vikingos no llevaban cuernos.» (5) |
Alcance: universal en los tres.

## Control de calidad
- `motor.guion`: sin ❌ (152/154/151 palabras). ⚠ «tramo de 14–16 s sin pregunta ni dato» en 01 y 03: justificado, en ese tramo salen Monell, 247 letras, tigres (01) y Doepler, Wagner, 1876 (03), que el detector no cuenta.
- `construir`: todos los textos se pueden leer, en los tres.
- ffprobe: 1080×1920, 30 fps, h264, AAC.
- `motor.calidad --mp4`: **sin ❌**. Notas 73/97/78 (`calidad-0N.md`). Los ⚠ que quedan son de ritmo y densidad (pocos micro planos y 4–5 elementos por plano, el precio del estilo cartoon con planos legibles) y en el 02 un micro plano oscuro de 0,45 s (la lágrima tachada), a propósito.
- Hojas de fotogramas revisadas. Arreglado antes del render final:
  - Subtítulo karaoke poco legible sobre fondos claros (cocina, laboratorio, módulo, papel): franja oscura difuminada detrás (`banda_sub`).
  - Cuernos invisibles en el gancho del 03 (opacidad) y primer segundo sin movimiento: ahora el casco bota y los cuernos se mueven desde el fotograma 0.
  - 02 con ❌ de ritmo plano: cuatro micro planos (0,45–0,7 s).
  - Pantalla partida Tierra/espacio del 02 mal encajada; rótulos sin cápsula con poco contraste; un «✔» que la fuente no tenía.
- Fichas de variables: 3 nuevas; `ficha comprobar`: 0 problemas.

## Fuentes
En `metadatos.json` → `fuentes` y en `guiones.md`.
