# Estado — vídeo extra 2026-11-19 (El Niño)

- **Estado**: **publicado en YouTube** (Nico: «súbelo», 20:19): https://youtube.com/shorts/HGERZv5VWiU (público 20:23, portada puesta por API). TikTok: página de subida abierta en el navegador integrado, a la espera de que Nico elija el archivo.
- **Quién**: Nico (chat https://claude.ai/code/session_019BG1dHVpM78Z8196Jiin3v), 2026-11-19 19:53–20:15. No es un lote: es un vídeo suelto pedido a partir de las tendencias del día.
- **Carpeta local**: `Documents/Parece Mentira/lotes/2026-11-19-extra` (Mac de Nico): `01-locucion.mp3`, `01-alineacion.json`. `01-el-nino_v1.mp4` (copiado al tercer intento, SHA igual), `01-portadas/portada.jpg`, `metadatos.json`.
- **Redes**: YouTube y TikTok.

## Tendencias de hoy
Fuentes: Google Trends (RSS de MX, ES, AR, CO; los de AR y CO venían con noticias de finales de octubre, poco fiables) y prensa del día. TikTok Creative Center y Studio no se miraron.
Elegida: **«el niño»** (México; El Niño 2026 lleva semanas en las noticias de toda Latinoamérica). Descartadas: GTA 6 (ya hecho), aceite de oliva (solo España), papa en Argentina, fútbol, dólar, muertes, política.

## Vídeo
- 01 «Este niño cambia el clima» · 153 palabras · voz oficial por API (57,7 s; créditos antes: 25.638) · 40 planos (0,35–2,93 s) · `motor.guion` ✓ · `construir` sin ⚠ · `motor.calidad --mp4` **100/100** sin ❌ ni ⚠ (`calidad-01.md`) · 1080×1920, 30 fps, h264/AAC 48 kHz, 58,1 s · SHA corto 394f455c8a81 (MP4 recomprimido a CRF 21 para el chat).
- Primer segundo: la Tierra con la franja caliente del Pacífico sube hacia cámara · «Este niño cambia el clima.» (5) · universal.
- Etiquetas: tema Ciencia, gancho paradoja, `tendencia`: «el niño».

## No hecho
- Portada elegida sin «ok»: «ESTE NIÑO CAMBIA EL CLIMA», diseño «abajo», 52,8 s (la mancha roja sobre el Pacífico). Ficha de variables y correo: no se hicieron.
- `motor/` no se tocó. Ilustraciones nuevas en `generadores/ilus_nino.py` (mapa del Pacífico, Tierra con la franja, barca, peces, pesebre, desierto, sequía, monitor, boya…).

## 02 y 03 (pedido de Nico a las 20:20: «genérame 2 más») — en revisión, falta el «ok»
- 02 «El dólar no es americano» · tendencia «dólar hoy» (MX) · voz oficial por API (61,6 s → 58,6 s quitando una frase con `omitir`) · 39 planos · `construir` sin ⚠ · `motor.calidad --mp4` 89/100 sin ❌; ⚠ justificados: densidad 4,6 elementos por plano (monedas y letras grandes sobre fondo limpio para que se lean), planos 14→15 parecidos (táler → dáler: la moneda cambia, el encuadre no, a propósito) y 43,8–48,9 s con el mismo encuadre (el pergamino donde se escriben la p y la s). SHA corto 0d8f42f4752c.
- 03 «Esta máquina engañó a Napoleón» · tendencia: inteligencia artificial · voz oficial por API (62,8 s → 59,2 s quitando dos frases) · 44 planos · `construir` sin ⚠ · `motor.calidad --mp4` 100/100. SHA corto 5249ff1a0ee1. `motor.guion` avisaba de un tramo de ≈16 s sin pregunta ni dato: es la explicación del truco, montada con cortes cortos.
- **Hay que oír los empalmes** de las frases quitadas antes de publicar (02 hacia el segundo 54; 03 hacia los segundos 4 y 50).
- MP4 enviados al chat (CRF 23). Sin portada ni ficha todavía. Ilustraciones en `generadores/ilus_extra2.py`.
- Créditos de ElevenLabs tras las tres voces: 24.954.

## Publicación de 02 y 03 (Nico: «súbelos», 20:45)
- YouTube por API desde el Mac de Nico, separados 1 h (DECISIONS): 02 https://youtube.com/shorts/Ve63IT5wgpY programado a las 21:25 · 03 https://youtube.com/shorts/QUFe8ovVpJE programado a las 22:25. Portadas puestas por API: 02 «EL DÓLAR NO ES AMERICANO» (arriba, 55,8 s) · 03 «ENGAÑÓ A NAPOLEÓN» (abajo, 11,8 s). `--prueba` antes: sin duplicados; SHA de los MP4 del Mac iguales.
- TikTok de 01, 02 y 03: pendiente de que Nico elija cada archivo en el navegador integrado (`lotes/2026-11-19-extra/`).
- Comentarios fijados de los tres en YouTube: pendientes (aviso programado en el chat a las 22:30). Fichas de variables: no hechas.
- **TikTok 01** (Nico eligió el archivo y escribió «sube el primero», 20:53): https://www.tiktok.com/@parece.mentira85/video/7709973442979974422 — publicado a las 20:55 con el texto de `metadatos.json`; portada = fotograma 0 (no se cambió). Al comprobarlo salía «Contenido en revisión · Solo yo» (revisión de TikTok). Falta 02 y 03.
- **TikTok 02** (Nico eligió el archivo, «dale tú», 20:56): https://www.tiktok.com/@parece.mentira85/video/7709974123442670870 — publicado a las 20:58, portada = fotograma 0; en revisión de TikTok al comprobarlo. El 01 ya sale como «Todo el mundo». Falta el 03.
