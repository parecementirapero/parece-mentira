# Estado — lote 2026-11-19-manana

- **Estado**: en producción — **esperando al Mac de Nico para la voz** (ver «Bloqueo»).
- **Agente**: Agente 08:00 (Nico) · MacBook Air de Nico · carpeta local `Documents/Parece Mentira/lotes/2026-11-19-manana`
- **Chat del lote**: https://claude.ai/code/session_019BG1dHnK2nwYYSBBZnUxmf
- **Redes**: YouTube y TikTok (Instagram fuera, DECISIONS 2026-11-17).
- La tarea programada se disparó a las 18:35 (Madrid) en vez de a las 07:52.

## Arranque
- Lote nuevo (no existía `estado.md`). Reservado en `TASKS.md` (commit ffe429e).
- Mac de Nico respondió a las 18:36. ElevenLabs: **26.689** caracteres libres de 40.000 (≈7 lotes; se renuevan el 15-12).
- Studio (§1.8): no se abrió (se priorizó el lote). No hay experimento aprobado en `estadisticas/experimentos/`.

## Bloqueo
- 18:40: voz por API desde el Mac → **01 y 02 generados** (`NN-locucion.mp3` + `NN-alineacion.json` en la carpeta local). Durante el 03 el puente del Mac se cayó («disconnected», luego «not connected to the bridge»). No se sabe si el 03 terminó.
- Sin el Mac no hay clave de ElevenLabs (solo está en `claves.txt` del Mac), así que no se puede generar el 03 ni traer 01/02 al montaje.

## Decisiones según las estadísticas
Base: `aprendizajes.md` (2026-11-19, 18 vídeos).
- **Firme**: primer fotograma y primera frase deciden. Los tres abren con un solo objeto grande moviéndose y una frase de 5 palabras.
- **Firme**: audiencia 72 % Latinoamérica → sin expresiones de España; temas universales.
- **Tendencia**: Espacio gana en todo → el 01 es Espacio. Ciencia es segunda → el 02. El 03 es Histórico (el peor tema, pero AGENTE §2 pide mezcla) contado desde el presente («ya no cae») con gancho de negación (71 % «se quedan», 1 vídeo).
- **Experimento del lote**: **gancho de paradoja** en el 02 («Tu cerebro canta sin música.»), primera vez en el canal. 01 (dato) y 03 (negación) hacen de control. Espero que el 02 iguale o supere el 65 % de «se quedaron viendo».

## Prueba del primer segundo (AGENTE §2)
| # | Objeto único y grande moviéndose en el fotograma 0 | Primera frase (≤ 5) | Alcance |
|---|---|---|---|
| 01 | Casco de astronauta que sube hacia cámara soltando ondas de olor | «El espacio huele a filete.» (5) | universal |
| 02 | Cerebro que entra con muelle y notas girando alrededor | «Tu cerebro canta sin música.» (5) | universal |
| 03 | La Torre de Pisa cayéndose que frena y se queda inclinada | «Esta torre ya no cae.» (5) | universal |

## Guiones
- `motor.guion`: 01 158 palabras (⚠ «tramo de ≈18 s sin pregunta ni dato»: justificado, son las descripciones del olor —carne, metal, Pettit— que van con cortes de 1 s); 02 155 ✓; 03 157 ✓.
- Fuentes y cautelas en `guiones.md`.

## Montaje (con tiempos provisionales, sin voz)
- `generadores/ilus_hoy.py` (filete, soplete, ondas de olor, oxígeno, matraz, perfume genérico, polvo lunar, guante, frambuesa, radiotelescopio, molécula; notas, auriculares, gusano, chicle, aula; Torre de Pisa por pisos y curva, plaza, corte del suelo, espadas, lingotes, barrena, hojas de calendario) + reutiliza las de los lotes 2026-11-18.
- `gen_01.py` 36 planos · `gen_02.py` 36 planos · `gen_03.py` 32 planos. Hojas de fotogramas revisadas y corregidas (casco y cerebro más grandes, rótulos que tapaban la cara o la torre, torre que se salía por arriba, contrastes sobre cielo claro con cápsula).
- Falta: voz → `gen_0N.py DIR NN-locucion.mp3 NN-alineacion.json` → render → `motor.calidad --mp4` → portadas → fichas → MP4 al chat → correo.
