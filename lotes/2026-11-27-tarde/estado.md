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
- [x] Render en la nube (1080×1920, 30 fps, H.264 + AAC 48 kHz estéreo): 01 59,1 s · 02 58,8 s · 03 52,8 s. `motor.calidad` sin ❌ (64, 63, 70/100; `calidad-0N.md`). Arreglados: «¡SUSTO!» con poco contraste (03), micro «3 MM» que salía diminuto (02), «+2 MIN» (01).
- [x] Portadas (`motor.portadas`, elegidas a ojo, en `metadatos.json`).
- [x] Fichas de variables (`estadisticas/fichas.json`, comprobadas).
- [x] Vídeos y portadas enviados al chat. Correo de aviso enviado (id 1a21e77f9d68c858).
- [ ] **Copia de MP4, SRT, manifiestos y portadas a `Documents/Parece Mentira/lotes/2026-11-27-tarde/` en el Mac**: el Mac estaba fuera del puente al terminar. Hacerlo al dar el «ok» (están en el chat: file_uuid 01 a8c427ce-0d31-4329-92cb-9dfc334f4475 · 02 f6156625-4c18-47cd-ab9b-20ec008a506c · 03 fb726403-85b0-4cb6-b9de-60e52207d9bf; portadas 82e2f296-6a06-408d-aca2-8dcf51b107d1, ee9055a7-d65e-472a-a69c-d085d574ab28, a888c8b4-0c2c-4938-a147-16821c07b3ec).

## Estado: **en revisión** (v1) — esperando «ok» en el chat

| # | Archivo | Duración | SHA-256 |
|---|---|---|---|
| 01 | `01-anochece-dos-veces_v2.mp4` | 59,1 s | 540303fa19a1fbae0a602c4c4d76b497189958dc0a0a88f2aadea359cafc58ea |
| 02 | `02-capa-de-ozono_v1.mp4` | 58,8 s | 06d6bc4f53adf04585a91cb93a0f6a374a870cacccd4aa536547e210bed1c75e |
| 03 | `03-piel-de-gallina_v1.mp4` | 52,8 s | eb991b7e1d09fa19697e48e44180c019be4c80e0cef494bf9c43eb446b2df901 |

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
- Planos: 27–30 por vídeo (DENSO pide 35–40) y ⚠ de `motor.calidad` por densidad (4–5 elementos por plano), pocos micro planos y 4 fondos por vídeo. Se dejan así: el Mac se cayó del puente varias veces y se priorizó tener la voz y entregar; cada plano tiene su acción y se lee.

## Datos con cuidado
- 01: las fuentes no dan el año de la fatwa (Khaleej Times la publica en agosto de 2011): el guion no dice año. Los tramos varían un poco entre fuentes (80–150 / 151–160): se dice «de la ochenta a la ciento cincuenta, dos; por encima, tres». Lo de verlo dos veces es una consecuencia («en teoría podrías»), no algo que digan las fuentes: con 2–3 min de margen y 1 min de ascensor cuadra.
- 02: «en los años ochenta» (sin 1985 ni nombres, no verificados con dos fuentes). «Hacia 2070 estará curado» = vuelta a los niveles de 1980 en la Antártida (NASA «by 2070», ABC «2070s»). «Con el cloro del año 2000, habría sido mayor» (Paul Newman, NASA, en ABC).
- 03: el gato no sale en las fuentes (dicen perro, chimpancé, puercoespín): el guion dice «un animal asustado»; el gato solo es la imagen. El estudio de Harvard es en ratones y así se dice.
- El prompt de la tarea programada pide «estilo v4 obligatorio», pero DECISIONS 2026-11-26 (Jorge) manda el estilo del vídeo largo: se ha seguido DECISIONS (como ayer) y se avisa en el correo.

## Sin hacer en este turno
- Datos de YouTube Studio (§1.8) y contestar comentarios (§8b): el Mac se cayó del puente varias veces (≈20:10–21:05); se priorizó la voz y el lote.

## Cambios pedidos en el chat
- 2026-11-27 ≈20:45 — «Anda haz mejor el edificio q parece un cohete vertebrado» → **01 v2**: rascacielos rehecho (aguja fina que se estrecha poco a poco, retranqueos escalonados que se alternan a los lados, cristal con montantes verticales, sin bandas horizontales; de noche la sombra ya no forma un rectángulo). «+2 MIN» más grande y centrado. Portada nueva (segundo 41,25, diseño «arriba»). `motor.calidad` sin ❌ (64/100). file_uuid v2: 4ebeeb8f-2674-4d87-af08-351cefbcf3c7; portada b004636d-5588-4563-a7ce-917a51f10df9. El «ok» vale para 01 v2, 02 v1 y 03 v1.
