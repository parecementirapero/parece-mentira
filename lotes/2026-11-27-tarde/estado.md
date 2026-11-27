# Lote 2026-11-27-tarde — estado

_Agente 20:00 (Jorge). Arranque 2026-11-27 19:53 (Madrid). Chat: https://claude.ai/code/session_019BG1dK7GpyrYsYXE518JkF_

## Pasos
- [x] Reserva en `TASKS.md` (commit ed6a3b9).
- [x] Mac de Jorge responde (19:58). ElevenLabs: quedaban **10.285** caracteres; este lote ha gastado 2.567 → quedan ≈**7.700** (≈2 lotes; se renuevan el 15-12).
- [x] Tendencias: no había archivo de la mañana; el turno de tarde hizo el análisis (Google Trends en el navegador integrado: MX, ES, AR, CO) → `lotes/tendencias/2026-11-27.md`.
- [x] 3 temas verificados con dos o más fuentes (subagentes de lectura); guiones pasados por `motor.guion` (sin ❌).
- [x] Voz con la API desde el Mac (`voz.py`, sin contexto): 01 58,6 s · 02 58,3 s · 03 52,3 s. MP3 y alineación en `Documents/Parece Mentira/lotes/2026-11-27-tarde/`.
- [x] Arte nuevo `generadores/ilus_1127t.py` (sobre los módulos del vídeo largo y `ilus_1126t`): rascacielos de escalones (de día y anocheciendo), sol de atardecer, ciudad del desierto (dos luces), cielo del desierto (atardecer y noche), cabina de ascensor, arco de la Tierra, dátiles y agua; anillo de ozono (entero y con agujero), rayo ultravioleta, dos monedas, nevera, espray, aire acondicionado, moléculas de ozono y CFC, átomo de cloro, polo sur, agujero, vórtice, borde de la atmósfera; antebrazo liso y de gallina (con mano), corte de piel en tres estados, gato tranquilo y erizado, ratón, células madre, auriculares, oyente, investigadora. Hojas de contacto revisadas.
- [x] Generadores `gen_01..03.py` (30, 29 y 27 planos atados a palabras), hojas de fotogramas con la voz real revisadas. Sin ⚠ de lectura.
- [ ] Render, `motor.calidad`, portadas, fichas, entrega.

## Decisiones según las estadísticas
- **[firme] primer segundo**: los tres abren con un objeto grande ya en marcha y una frase de 3–5 palabras.
- **[firme] guiones cortos (130–145)**: 148, 153 y 153 palabras (AGENTE pide 150–160; quedan en medio). La voz salió algo más lenta de lo previsto: 01 y 02 rozan los 60 s (59,4 y 59,1 s con el bucle).
- **[firme] Latinoamérica**: ganchos y guiones sin expresiones solo de España.
- **[tendencia] Cotidiano**: el 03 (piel de gallina) es cotidiano; el 01 y el 02 salen de tendencias de hoy (México y Colombia).
- **Experimento del lote: gancho de paradoja en el 01** («Aquí anochece dos veces.»). El 02 y el 03, gancho de dato como los que mejor van. Espero > 65 % «se quedaron viendo» en el 01.

## Tendencias de hoy
Archivo: `lotes/tendencias/2026-11-27.md`. 01 ← «burj khalifa» (MX, CO); 02 ← «agujero de la capa de ozono» (MX, noticia del 2026: el más grande en una década). Sobran Iguazú y neumáticos de invierno (sin verificar, a `IDEAS.md`).

## Prueba del primer segundo
| # | Objeto grande en acción en el fotograma 0 | Primera frase | Alcance |
|---|---|---|---|
| 01 | Rascacielos enorme con el sol bajando detrás de la ciudad y la punta encendida | «Aquí anochece dos veces.» (4) | universal |
| 02 | La Tierra con su escudo brillante y un rayo violeta que choca | «Este escudo mide tres milímetros.» (5) | universal |
| 03 | Un antebrazo enorme cuyos pelos se ponen de punta de golpe | «Tu piel cree tener pelo.» (5) | universal |

## Avisos del guion justificados
- 01 y 03: `motor.guion` avisa de un tramo de ≈14 s sin pregunta ni cifra; cada frase tiene su acción en pantalla (horizonte que se aleja, sol que baja; gato que se eriza, auriculares).
- 02: una frase de más de 22 palabras (la del cloro): es una cadena de tres acciones, cada una con su plano.
- 01: 148 palabras (por debajo de 150) siguiendo la recomendación firme de guiones cortos.
- Planos: 27–30 por vídeo (DENSO pide 35–40). El turno se ha comido mucho tiempo con el Mac cayéndose del puente; se priorizó que cada plano se entienda.

## Datos con cuidado
- 01: las fuentes no dan el año de la fatwa (Khaleej Times la publica en agosto de 2011): el guion no dice año. Los tramos varían un poco entre fuentes (80–150 / 151–160): se dice «de la ochenta a la ciento cincuenta, dos; por encima, tres». Lo de verlo dos veces es una consecuencia («en teoría podrías»), no algo que digan las fuentes: con 2–3 min de margen y 1 min de ascensor cuadra.
- 02: «en los años ochenta» (sin 1985 ni nombres, no verificados con dos fuentes). «Hacia 2070 estará curado» = vuelta a los niveles de 1980 en la Antártida (NASA «by 2070», ABC «2070s»). «Con el cloro del año 2000, habría sido mayor» (Paul Newman, NASA, en ABC).
- 03: el gato no sale en las fuentes (dicen perro, chimpancé, puercoespín): el guion dice «un animal asustado»; el gato solo es la imagen. El estudio de Harvard es en ratones y así se dice.
- El prompt de la tarea programada pide «estilo v4 obligatorio», pero DECISIONS 2026-11-26 (Jorge) manda el estilo del vídeo largo: se ha seguido DECISIONS (como ayer) y se avisa en el correo.

## Sin hacer en este turno
- Datos de YouTube Studio (§1.8) y contestar comentarios (§8b): el Mac se cayó del puente varias veces (≈20:10–21:05); se priorizó la voz y el lote.
