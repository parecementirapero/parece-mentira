# Estado — lote 2026-11-15-tarde

- **Estado**: en revisión — **v1 en espera**: Nico decide (2026-11-15) no publicar la v1 y rehacer los 3 vídeos (v2) con el motor v2 y el estilo nuevo de `DECISIONS.md`. Después se vuelve a pedir «ok».
- **Agente**: Agente 20:00 (Jorge) · Mac de Jorge · carpeta local `Documents/Parece Mentira/lotes/2026-11-15-tarde`
- **Chat del lote**: https://claude.ai/code/session_019BG1dGzAeKkhhB4LNjrkX3
- **Drive**: https://drive.google.com/drive/folders/1nNCCTMwP2WMKok84Ykactyt2aj5Wvdtc — **solo los 3 SRT**. Los MP4 no se subieron: el conector de Drive acepta ≈3 MB por llamada (y 10 MB por archivo) y los vídeos pesan 7–12 MB. Los MP4 están en la carpeta local del Mac de Jorge.
- **Correo de aviso**: enviado a parecementirapero.media@gmail.com, id `1a1dff810fee0c30`.

## Vídeos (v1)
| # | Archivo | Duración | SHA-256 (archivo en el Mac) | Voz |
|---|---|---|---|---|
| 1 | `01-guerra-38-minutos_v1.mp4` | 45,17 s | `2daf15a57f1da61f8657e8a80a07b77596885579fb239e2e83415639913a8df7` | OK |
| 2 | `02-luna-se-aleja_v1.mp4` | 41,54 s | `02f57ad0698860860c4b6352500d3ddb34c2e3f6cedc9bc764bc9ec0d012d020` | OK |
| 3 | `03-moais-con-cuerpo_v1.mp4` | 38,97 s | `637ea460f21acede3e5dc6454881032f3fc6f99ac11fc19d81cdabcd27ec1300` | OK |

Nota: el SHA del manifiesto (`*_manifest.json`) es el del render; al copiar al Mac el puente de archivos añade unos metadatos al MP4 (≈5,9 KB), por eso el SHA del archivo final es otro. La versión aprobable es la del Mac (tabla).

## Control de calidad
- `ffprobe`: 1080×1920, 30 fps, h264 yuv420p (CRF 19, veryfast), AAC 48 kHz estéreo; duración = locución + 0,5 s.
- Hojas de fotogramas (`--hoja` cada 1,5 s y del MP4 cada 2 s) revisadas: pantalla completa, sin título, sin rótulos, sin Nova, subtítulo blanco abajo, algo en movimiento en cada plano.
- Corregido antes del render: relleno negro en rectángulos «transparentes» (campo de fútbol), balanza cortada, tierra gris en la sección de los moáis, hierba que no llegaba abajo, subtítulo a 60 px para no partir líneas.

## Publicación
_(pendiente de «ok»)_

## Versión 2 (motor v2) — Jorge — 2026-11-15 17:45
Hecha desde el chat del Mac de Jorge con `generadores/a_v2.py` (reajusta las escenas v1 a la locución v2, karaoke arriba con palabras clave, rótulos de dato, transiciones v2, música generada `curiosidad|misterio`, grano 0,035).

| # | Archivo (Mac de Jorge, `lotes/2026-11-15-tarde/v2/`) | Duración | LUFS |
|---|---|---|---|
| 1 | `2026-11-15-tarde-01-guerra-38-minutos_v2.mp4` | 52,3 s | −19,4 |
| 2 | `2026-11-15-tarde-02-luna-se-aleja_v2.mp4` | 46,7 s | −19,6 |
| 3 | `2026-11-15-tarde-03-moais-con-cuerpo_v2.mp4` | 46,3 s | −19,3 |

QC: ffprobe 1080×1920, 30 fps, h264 + AAC; hojas de fotogramas revisadas (karaoke a y=300 para no pisar la torre del palacio y la cabeza del moái; rótulos en la mitad de abajo).
Drive: **no subidos** (el conector no admite >10 MB). Pendiente de Google Drive para ordenador.
Voz v2: ~2.500 caracteres.

## Versión 3 (referencias 2) — Jorge — 2026-11-15 18:20
Mismo audio que la v2 (0 créditos de ElevenLabs). `generadores/a_v3.py`: planos de ~2,7 s (19/18/17 planos) general → primer plano → detalle con `camara.foco`, rótulos HUD, término clave en amarillo, etiqueta roja de contexto, viñeta más marcada en escenas oscuras.
Archivos: `lotes/2026-11-15-tarde/v3/` del Mac de Jorge (52,3 / 46,7 / 46,3 s; −19,4 / −19,6 / −19,3 LUFS). Drive: pendiente (Google Drive para ordenador).
