# Decisiones vigentes

Formato: decisión — fecha — quién — motivo. Si una decisión cambia, se tacha la antigua y se añade la nueva debajo.

## Cuentas e infraestructura
- Cuenta del proyecto: parecementirapero.media@gmail.com (Gmail, Drive, YouTube, TikTok). Instagram: @parecementiramedia. — 2026-11-15 — Jorge
- Un solo repo: `parecementirapero/parece-mentira`, empezado de cero (no se copia el repo antiguo de NICCOCASPER, que no funcionaba bien). — 2026-11-15 — Jorge
- Claude usa la cuenta de GitHub compartida `parecementirapero`, no la personal de Nico. — 2026-11-15 — Jorge
- ~~Drive dedicado solo al proyecto. Carpeta fija de revisión: «Parece Mentira — Revisión» (https://drive.google.com/drive/folders/1Sm8Yf72fJBxO7roWSOGT-hpRM0DK0j6i), una subcarpeta por lote. — 2026-11-15 — Jorge~~ → **sustituida el 2026-11-16 por Jorge**: no se usa Drive (los MP4 no se suben y da mucho trabajo).
- **Revisión en el chat de Claude** (2026-11-16 — Jorge): tras cada lote (08:00 y 20:00) el agente deja los 3 MP4 dentro de su chat (`SendUserFile`) para verlos allí, y el correo lleva el enlace a ese chat. El «ok» se escribe en ese mismo chat. Motivo: Drive no acepta los MP4 desde el conector y añade pasos.
- Publicación gratuita desde el navegador integrado de la app de Claude (sesiones ya iniciadas), no servicios de pago. — 2026-11-15 — Jorge

- Carpeta local de trabajo en cada Mac: `~/Documents/Parece Mentira/` con `claves.txt` (ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID; nunca al repo), `lotes/` y `renders/`. — 2026-11-15 — Jorge
- `api.elevenlabs.io` añadido a los dominios permitidos de la cuenta de Claude. — 2026-11-15 — Jorge

- Estadísticas del canal: web propia en `estadisticas/` actualizada cada mañana antes de las 9:00 por GitHub Actions (nube, 0 €), en vez de un correo diario. Credenciales de Google solo en los secretos de GitHub (`YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`), nunca en el repo; acceso de solo lectura (youtube.readonly + yt-analytics.readonly) — 2026-11-16 — Nico — motivo: ver histórico y comparar vídeos sin depender de un Mac encendido
- Web pública mínima en https://parecementirapero.github.io (repo público `parecementirapero/parecementirapero.github.io`: portada + `privacidad.html`). Motivo: Google exige página principal y política de privacidad en un dominio propio para pasar la app de OAuth a «En producción» (sin eso el permiso caduca cada 7 días); sirve también para TikTok/Meta y como enlace en bio. La app de Claude en GitHub no tiene acceso a ese repo: se edita desde la web de GitHub — 2026-11-16 — Nico
- Las estadísticas incluyen TikTok (Display API, app en sandbox con la cuenta del canal como usuario de prueba; sin retención) e Instagram (Instagram API with Instagram Login, app de Meta en desarrollo). Los tokens que se renuevan solos (TikTok rota en cada uso, Instagram cada lunes) los guarda el workflow en los secretos con `GH_PAT` (token de GitHub solo con «Secrets: read and write» en este repo) — 2026-11-16 — Nico — motivo: comparar las 3 redes sin tocar nada a mano

## Flujo diario
- Dos lotes al día: 08:00 en el ordenador de Nico y 20:00 en el de Jorge (una sola notificación por turno). — 2026-11-15 — Jorge
- Cada lote: ideas sin repetir temas (se admiten continuaciones con información nueva) → guiones → voz → montaje 9:16 → vídeos en el chat del agente → correo de aviso con el enlace al chat a parecementirapero.media@gmail.com. — 2026-11-15 — Jorge
- Se publica en YouTube, Instagram y TikTok solo cuando la persona responde «ok» en el chat de ese lote. — 2026-11-15 — Jorge
- **Prueba de temas cotidianos** (2026-11-16 — Jorge): solo el lote **2026-11-16-tarde** sale con 2 temas de vida cotidiana + 1 histórico conectado con hoy, usando los temas reservados en `lotes/IDEAS.md`. Regla de la prueba: cada idea toca algo que el espectador hace, ve o siente, y se nota en los 2 primeros segundos; lo histórico se cuenta desde el presente. Desde el 2026-11-17 Nico y Jorge deciden si se queda como mezcla fija. Motivo: Jorge cree que los datos del pasado sueltos conectan menos con la gente.

## Estilo de los vídeos
- Formato vertical 9:16, a pantalla completa (la ilustración ocupa todo el reel, sin panel/«cuadrito» en medio). — 2026-11-14 — Nico
- ~~Sin título arriba, sin rótulos blancos con borde azul; solo subtítulo blanco abajo. — 2026-11-14 — Nico~~
- Sin título fijo ni rótulos blancos con borde azul. **Subtítulo arriba (≈18 % de alto), tipo karaoke**: palabras dichas en gris translúcido, la actual en blanco negrita, palabras clave dentro de una cápsula oscura. Se permiten rótulos de dato integrados en la escena (cifra + unidad, barras con etiqueta). — 2026-11-15 — Nico — motivo: así lo hacen los 13 vídeos objetivo (`motor/OBJETIVO.md`)
- Duración objetivo **45–60 s** (≈130–170 palabras de locución). — 2026-11-15 — Nico — motivo: mediana de los vídeos objetivo ≈57 s
- **Música de fondo** baja bajo la voz, mezcla final ≈ −19 LUFS. Solo música con licencia que permita uso comercial en YouTube, Instagram y TikTok; fuente por decidir. — 2026-11-15 — Nico — motivo: todos los objetivos llevan base continua
- **Referencias 2** (`motor/REFERENCIAS_2.md`): un plano cada 1,5–4 s (general → primer plano → detalle), vistas en sección, una acción por frase, etiquetas que señalan (cifra en cápsula, etiqueta con línea, término clave en amarillo inclinado, etiqueta de contexto roja), luz con intención, final en bucle. Obligatorio para todos los lotes. — 2026-11-15 — Jorge — motivo: los 9 vídeos de referencia que pasó Jorge
- **Estilo de ilustración v4** (aprobado por Jorge: «me mola mucho este estilo»): cada escena es una ilustración SVG completa con degradados, luz, sombras y textura (`lotes/2026-11-15-tarde/generadores/v4/ilus*.py`), un plano por frase, algo moviéndose siempre; personajes en silueta a contraluz o ilustrados con volumen. Nada de formas sueltas sobre fondo plano. — 2026-11-15 — Jorge
- Nova (supernova de colores) sigue siendo la mascota del canal, pero no aparece dentro de los vídeos. — 2026-11-14 — Nico
- Más movimiento: que pase algo constantemente en pantalla, ilustración 2.5D en capas, luces y sombras, acciones pequeñas que expliquen, cámara estable. Flechas y giros bien hechos. — 2026-11-14 — Nico
- Títulos sin «| elevenlabs.io». — 2026-11-15 — Jorge
- Guiones de locución con las cifras escritas en letra. Cada dato con fuente citada en la descripción. — 2026-11-14 — Nico

## Voz
- ~~Voz ElevenLabs «Archivo Oculto — Narración», Eleven v4, estabilidad 50 %, similitud 75 %.~~
- Voz oficial: ElevenLabs «Narrador PM - Curiosidades v1» (voice_id `EuJOG4WNDCMcwTFrXKUc`), hombre ~30 años, acento de España, ritmo ágil. Cuenta nueva de ElevenLabs, plan Starter (licencia comercial). Si falla la voz, el vídeo se marca «pendiente de voz»; no se genera voz alternativa. — 2026-11-15 — Jorge

## Presupuesto y gastos
- ~~Presupuesto 50–150 €/mes entre ambos proyectos.~~
- Presupuesto **ampliado** (importe mensual por concretar). Prioridad de gasto: — 2026-11-15 — Nico (aceptado por Nico y Jorge) — motivo: llegar al nivel de los vídeos objetivo (`motor/OBJETIVO.md`) con 6 vídeos/día de 45–60 s
  1. **ElevenLabs Pro** (99 $/mes, 600k créditos): 6 vídeos/día × ~900 caracteres ≈ 160k/mes no caben en Creator (121k). Lo contrata una persona desde la cuenta.
  2. **Ilustraciones**: primero el motor con escenas SVG (gratis). Se hace una prueba comparando un vídeo SVG con uno con ilustraciones generadas por IA; solo si el SVG se queda corto se elige y se paga un servicio de imagen.
  3. **Música**: Pixabay Music (guardando el certificado de licencia de cada pista en la carpeta del lote, por si hay reclamaciones de Content ID) o la música de ElevenLabs incluida en el plan. Solo se paga una biblioteca si las reclamaciones se vuelven un problema.

## Redes
- Excepción a «no repetir temas»: se publica la prueba v2 «Huellas en la Luna» aunque el tema estaba usado en el sistema antiguo. — 2026-11-15 — Nico (con Jorge) — motivo: el vídeo antiguo está retirado y esta es la primera muestra del estilo nuevo
- Todo lo publicado antes del 2026-11-15 se retiró: YouTube en privado, TikTok en «Solo yo» (salvo «Mi cerebro cuando toca callarse», bloqueado; hay que hacerlo desde el móvil), Instagram borrado. — 2026-11-15 — Jorge
- **Sin post-proceso de acabado** (grano animado, LUT documental, papel, bokeh): probado sobre el 02 v4 y Nico prefiere el aspecto original («me gusta más como estaba antes»). `motor/acabado.py` se queda en el repo sin usar. — 2026-11-16 — Nico
