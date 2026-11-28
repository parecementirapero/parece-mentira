# Lote 2026-11-28-manana — estado

_Agente 08:00 (Nico). La tarea programada se disparó a las 11:45 (Madrid) en vez de a las 07:52. Chat: https://claude.ai/code/session_019BG1dKjnnRjJqNw5DCuPje_

## Pasos
- [x] Reserva en `TASKS.md` (commit 05ca281).
- [x] Mac de Nico responde (11:47). ElevenLabs: quedaban **9.286** caracteres; este lote ha gastado ≈2.630 → quedan ≈**6.650** (≈2 lotes; se renuevan el 15-12).
- [x] Tendencias → `lotes/tendencias/2026-11-28.md` (commit 7985e0a, antes de los guiones).
- [x] 3 temas verificados con dos o más fuentes (subagentes de lectura); guiones con `motor.guion` (sin ❌).
- [x] Voz por API desde el Mac (`voz.py`): 01 57,0 s · 02 55,1 s · 03 60,7 s. MP3 y alineación en `Documents/Parece Mentira/lotes/2026-11-28-manana/`.
- [x] 03 recortado sin gastar otra voz (`omitir`): fuera «Siglos goteando hacia el suelo.» y «Mucho menos que un virus.» → 56,6 s. **Empalmes sin oír** (el agente no puede escuchar): hacia los segundos 11,3 y 44,6.
- [x] Arte nuevo `generadores/ilus_1128m.py` (sobre `ilus_1127t` y los módulos del vídeo largo): termómetros frío y calor, muñeco y bola de nieve, franja de nieve, haz de luz recto y oblicuo, eje de la Tierra, fondo de órbita; columna con ángel dorado nevada, nieve sobre capota, foto de 1967, dos chicos de abrigo, abuela, avenida nevada de noche; vidriera (y vidriera que «gotea»), corte de cristal en cuña, bola de vidrio al rojo, disco y cilindro de vidrio, cristal suelto, abadía gótica, virus, átomos en red y desordenados, cristalero, interior de catedral y taller de vidriero. Hojas de contacto revisadas.
- [x] Generadores `gen_01..03.py` (planos atados a palabras, micro planos), hojas de fotogramas con la voz real revisadas, sin ⚠ de lectura.
- [x] Render en la nube (1080×1920, 30 fps, H.264 + AAC 48 kHz estéreo). `motor.calidad` sin ❌ (75, 84, 78/100; `calidad-0N.md`). Arreglados antes: ritmo plano (❌) en 02 y 03 con micro planos, rótulos con poco contraste, el año «1.967» con punto, la columna cortada por el gancho.
- [x] Portadas (`motor.portadas`, elegidas a ojo, en `metadatos.json`).
- [x] Fichas de variables (`estadisticas/fichas.json`, comprobadas).
- [x] Vídeos y portadas enviados al chat. Correo de aviso enviado (id 1a221e0aa9b3d90c).
- [ ] **Copia de MP4 y portadas a `Documents/Parece Mentira/lotes/2026-11-28-manana/` en el Mac**: el Mac se desconectó del puente al terminar. Hacerlo al dar el «ok» (están en el chat: file_uuid 01 67f3d252-10bc-4933-9673-4d65cf4ba959 · 02 664b51cc-3ad1-4cab-a39f-0ad724f01bc2 · 03 dbb34b67-600e-4e8c-902a-54744de7edee; portadas 4f4f2d02-9ff1-44fa-900c-ce2e1f79ec59, b16183db-a044-49d3-8746-0039db6e7257, 5580f64b-a9e5-4443-9b8a-bc08fa6e312e). Si el contenedor se ha reciclado, se vuelven a renderizar con `gen_0N.py` (MP3 en el Mac).

## Estado: **en revisión** (v1) — esperando «ok» en el chat

| # | Archivo | Duración | SHA-256 |
|---|---|---|---|
| 01 | `01-cerca-del-sol_v1.mp4` | 57,5 s | e816f58fd2f3d50c7a55b9b16fb6cb0f104eb15d31c3c3936e06586daa26cf35 |
| 02 | `02-nevada-1967_v1.mp4` | 55,6 s | 76832959f36df383eab221d15d0f8b1525427e9b1d27ef0ca79cc0e9d843b49b |
| 03 | `03-vidrio-no-se-escurre_v1.mp4` | 57,1 s | 0b4f90c77c2c012fa15c7cb01a0c7484997025880aec14f969b9c8c7454f9074 |

## Decisiones según las estadísticas
- **[firme] primer segundo**: los tres abren con un objeto grande ya en marcha (Tierra que se acerca a un Sol enorme con un copo cayendo; copo que cae ante la columna nevada; vidriera que gotea) y una primera frase de 4–5 palabras.
- **[firme] Latinoamérica**: dos vídeos hablan directamente de Latinoamérica (02 es México; 01 nombra México, Argentina y Chile). Sin expresiones solo de España.
- **[tendencia] Cotidiano**: el 01 parte del frío de estos días (cotidiano, etiquetado Espacio); el 03, de las ventanas.
- **Experimento del lote: gancho POV en segunda persona en el 02** («Despiertas y está nevando.»). El 01 (paradoja) y el 03 (negación) usan ganchos que ya hemos usado. Espero más del 65 % «se quedaron viendo» en el 02, sobre todo en México.

## Tendencias de hoy
Archivo: `lotes/tendencias/2026-11-28.md`. Los tres salen de tendencias: 01 ← «invierno» / «clima cdmx» (MX, 2 M+ búsquedas); 02 ← «nevada de la ciudad de méxico de 1967» (MX); 03 ← «vidrio» (ES). Se dejan para la tarde, sin verificar: el segundo intercalar (23:59:60) y «¿flota un reloj de arena?» (YouTube Studio · Investigación). TikTok Creative Center pide iniciar sesión: saltado.

## Prueba del primer segundo
| # | Objeto grande en acción en el fotograma 0 | Primera frase | Alcance |
|---|---|---|---|
| 01 | La Tierra deslizándose hacia un Sol enorme, con un copo de nieve cayendo y un termómetro azul | «Cerca del Sol, y helados.» (5) | universal |
| 02 | Copo de nieve que cae delante de la columna del ángel en la avenida nevada | «Despiertas y está nevando.» (4) | nicho |
| 03 | Vidriera de colores que gotea y deja caer gotas | «El vidrio no se escurre.» (5) | universal |

## Avisos del guion justificados
- 01: `motor.guion` avisa de que la afirmación llega en el segundo 4,9 (la frase 2 la dice sin introducción) y de un tramo de ≈17 s sin cifra; ese tramo tiene una pregunta («¿Y qué pasa?») y cada frase su plano.
- 03: tramo de ≈15 s sin pregunta ni cifra (la fabricación a mano): cada paso se ve (bola, cilindro, disco, cristalero).
- ⚠ de `motor.calidad` (pocos fondos, densidad 4–5 por plano, mismo encuadre): se dejan; cada plano tiene su acción y se lee.

## Datos con cuidado
- 01: «unos veintitrés grados» (USNO 23,4°, SciAm ≈23°, Space.com ≈23,5°). Distancias redondeadas (≈147 y ≈152 millones de km), como dan SciAm y Space.com. No se cita el 7 % de luz (solo una fuente).
- 02: profundidad «unos cinco centímetros» (las fuentes dan 4–5, 5, 5–8 y 8 cm). «Masa de aire polar» (Expansión cita a Conagua); ninguna fuente da número de frente frío. No se mencionan las víctimas del frío (regla: nada de muertes). «Más de dos mil metros de altura» es dato general de la ciudad, no de estas fuentes. Los chicos del dibujo no representan a nadie real.
- 03: «se soplaba una bola o un cilindro» (ACerS dice corona; SciAm y DoITPoMS, cilindro: se dicen los dos). «En mil millones de años… un nanómetro» (ACerS sobre Gulbiten y Mauro 2017). «Más que la edad del universo» (SciAm y DoITPoMS).

## Sin hacer en este turno
- Datos de YouTube Studio (§1.8) y contestar comentarios (§8b): el turno empezó a las 11:45 y el Mac se desconectó al final.
