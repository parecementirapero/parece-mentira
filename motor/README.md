# Motor de montaje 9:16

Convierte un `episodio.json` + la locución en un MP4 listo para revisar (1080×1920, 30 fps, H.264 yuv420p, AAC 48 kHz estéreo) con subtítulo karaoke arriba (o el clásico abajo), música de fondo, mezcla a −19 LUFS, SRT, manifiesto con SHA-256 y hoja de fotogramas para el control de calidad.

Requisitos: Python 3.9+, `pip install pillow numpy`, FFmpeg con libx264 y ffprobe.

```bash
# desde la raíz del repo
python3 -m motor.render ruta/episodio.json --salida ruta/out           # vídeo + hoja de fotogramas
python3 -m motor.render ruta/episodio.json --hoja --cada 1.5            # solo la hoja (5 s) para iterar rápido
python3 -m motor.render ruta/episodio.json --desde 10 --hasta 16        # un tramo
python3 -m motor.tiempos palabras alineacion.json                       # tiempos por palabra de ElevenLabs
```

Tiempo de render aproximado: 2,5–3 s de cálculo por segundo de vídeo.

## Flujo recomendado para cada vídeo
1. Locución → MP3 y, si se puede, el JSON de alineación de ElevenLabs (`/v1/text-to-speech/{voice_id}/with-timestamps`).
2. `python3 -m motor.tiempos palabras alineacion.json` para saber en qué segundo empieza cada frase.
3. Escribir el `episodio.json` (o un `generar.py` que lo escriba, como el ejemplo) con una escena por idea y acciones sincronizadas con las frases.
4. `--hoja` y **mirarla**; corregir; repetir. Después, el render completo.

## episodio.json
```json
{
  "id": "2026-11-16-manana-01-slug", "version": 1,
  "audio": "01-locucion.mp3",
  "subtitulos": {"alineacion": "01-alineacion.json", "max_chars": 26},
  "estilo_subtitulos": {"y": 1560, "tam": 66},
  "escenas": [
    {"inicio": 0, "fin": 5.9, "entrada": "fundido|barrido|corte",
     "fondo": {"tipo": "degradado|radial", "colores": ["#arriba", "#medio", "#abajo"]},
     "camara": {"zoom": [1.0, 1.06], "pan": [[0, 0], [0, -30]], "temblor": 0},
     "vineta": 0.5,
     "elementos": [ ... ]}
  ]
}
```
- Subtítulos: `{"alineacion": ...}` (lo mejor), `{"srt": ...}`, una lista `[{"texto","inicio","fin"}]`, o nada + `"guion"` (reparto aproximado).
- Tiempos de escena en segundos absolutos; los `keys` de cada elemento, **relativos al inicio de su escena**.
- Los elementos se pintan en orden: el primero queda al fondo.

## Novedades v2 (2026-11-15, estilo de `motor/OBJETIVO.md`)
- **Subtítulo karaoke** (por defecto): `"estilo_subtitulos": {"modo": "karaoke", "y": 350, "tam": 62, "claves": ["palabra", ...]}`. Necesita la alineación de ElevenLabs (`/with-timestamps`). Las palabras clave salen en cápsula. `"modo": "clasico"` = el blanco abajo de la v1.
- **Transiciones**: `"entrada": "desenfoque"` (barrido rápido con desenfoque de movimiento) y `"zoom"` (atraviesa la escena anterior), además de `fundido|barrido|corte`.
- **Rótulos de dato**: elemento `rotulo` (`texto` o `contar: [desde, hasta, s]` + `contar_desde`, `unidad`, `tam`, `color`, `capsula`).
- **Ilustraciones SVG**: `imagen` acepta `.svg` (se rasteriza con `rsvg-convert`), con `sombra` opcional. Ejemplos en `ejemplos/v2-huellas-luna/svg/`.
- **Música**: `"musica": {"archivo": "pista.mp3", "db": -16}` o `{"generar": "curiosidad|misterio", "semilla": 1}` (música generada por código, sin licencias). La voz atenúa la música (sidechain) y la mezcla se normaliza a `"lufs": -19`.
- **Grano**: `"grano": 0.035` (textura fija; uno animado multiplicaba ×8 el peso del MP4). El vídeo lleva tope de 8 Mb/s.
- Ejemplo completo: `ejemplos/v2-huellas-luna/generar.py RUTA_AUDIO` (47 s, 8 escenas, gancho en el fotograma 0 y final en bucle). Render ≈ 2 min.

## Novedades v2.1 (2026-11-15, Jorge — referencias `motor/REFERENCIAS_2.md`)
- **Cámara con foco**: `"camara": {"zoom": [1.5, 1.6], "foco": [[x0, y0], [x1, y1]]}` encuadra ese punto del lienzo (primer plano / detalle) en vez del centro. Sin `foco`, igual que antes.
- **Elementos HUD**: cualquier elemento con `"hud": true` se pinta después de la cámara (etiquetas, palabras clave, cifras): no se recorta ni se agranda al acercar el plano.
- **Planos dentro de una escena**: se trocea una escena en planos con `"entrada": "corte"` y los `keys` desplazados (ver `lotes/2026-11-15-tarde/generadores/a_v3.py`).

## Novedades v2.2 (2026-11-16, Nico — prueba «Luna densa»)
- **Efectos de sonido por código** (`motor/sfx.py`, sin licencias): `"sfx": [{"t": 1.2, "tipo": "whoosh|pop|tic|golpe|zap|brillo|ding|rumor|ola|senal|fugaz|trazo|mordisco|meteoro", "db": -14}]`. `db` = pico del efecto. Se mezclan con voz y música y no se atenúan bajo la voz. Demo: `python3 -m motor.sfx demo.wav`.
- **Rótulo que cuenta**: `"decimales": 1` (coma decimal: 3,8 · 23,5), `"contar_prefijo": "+"` y `"miles": false` (años: 1969).
- `motor/acabado.py`: post-proceso de prueba (grano, LUT, papel, bokeh). **No se usa** (DECISIONS 2026-11-16).

## Novedades v2.3 (2026-11-16, Nico — gancho en el fotograma 0)
- `"estilo_subtitulos": {"gancho": true}`: la **primera frase** (hasta `.` `?` `!` `…`, máx. 16 palabras) se ve **entera desde el fotograma 0**, un 15 % más grande y sobre un panel oscuro translúcido; dentro sigue el karaoke (la palabra que suena en negrita). Al acabar esa frase vuelve el karaoke normal. Sin `gancho`, el fotograma 0 sale sin texto porque la voz aún no ha empezado.
- Opciones: `{"max_palabras": 16, "panel": true, "alfa": 225, "tam": 69, "color_panel": "#070b1e", "alfa_panel": 150}`.
- Motivo: en los Reels virales del nicho el gancho se lee entero en el primer fotograma (`claude/analisis-reels-virales-2026-11-16.md` en el Proyecto de Claude).

## Imágenes reales: `motor/openverse.py` (2026-11-16, Nico)
`buscar "términos"` → `descargar <id> --lote DIR --video NN --uso "…"` → `creditos DIR --video NN`. Solo PD/CC0/CC BY de Wikimedia Commons y el Met, comprobadas en origen (rechaza SA/NC/ND, restricciones y dominio público solo de EE. UU.); registro en `<lote>/creditos.json`. Necesita red a `api.openverse.org`, `commons.wikimedia.org`, `upload.wikimedia.org`, `collectionapi.metmuseum.org` e `images.metmuseum.org`. Pruebas sin red: `python3 motor/prueba_openverse.py`. Reglas de uso en `AGENTE.md` §5b. La imagen descargada se usa con el elemento `imagen` (PNG/JPG).

## Portadas (2026-11-16, Nico)
`python3 -m motor.portadas DIR/episodio.json --texto "NO SON SOLO CABEZAS" --clave cabezas --salida DIR/portadas` (o `--mp4 vídeo.mp4`) → 4 candidatas (fotogramas distintos sin rótulos del vídeo; texto arriba / centro / abajo / dato en cápsula amarilla, siempre dentro del recorte 3:4 de las cuadrículas de perfil), `hoja-portadas.jpg` y `portadas.json` con la puntuación. La puntuación (color, detalle, tamaño del sujeto, texto que no tapa el sujeto, legibilidad a 180 px) **solo ordena**: la elección final se hace mirando la hoja y se registra con `--elegir DIR/portadas N --motivo "…"` → `portada.jpg`. Criterios y flujo en `.claude/agents/portadas.md` (subagente que las crea y elige sin «ok», AGENTE §6b). ~20 s por vídeo.

## Elementos (`tipo`)
Propiedades comunes animables con `keys` (`[{"t": s, "x": .., "op": .., "ease": "suave|lineal|entrada|salida|rebote"}]`):
`x, y, escala, ex, ey, rot, op, z` (z = paralaje: 0 fondo quieto, 1 primer plano).
Movimiento continuo con `anim`: `flotar [px, s]`, `girar º/s`, `balanceo [º, s]`, `pulso [amp, s]`, `parpadeo [min_op, s]`, `deriva [vx, vy]`.

| tipo | para qué | claves propias |
|---|---|---|
| `forma` | cualquier objeto: rect, redondeado, elipse, circulo, poligono | ancho, alto, radio, puntos, relleno (color o [arriba, abajo]), borde, grosor, esquinas, sombra, brillo, desenfoque, op_relleno |
| `esfera` | planetas, bolas, sol (con volumen y luz) | radio, color, color2, textura (lisa, rocosa, crateres, bandas, tierra, sol), giro, luz, halo, cara |
| `brillo` | halos de luz, destellos, polvo que se levanta | radio, color, intensidad, dureza |
| `rayos` | rayos de luz (usar con girar lento) | n, longitud, apertura, intensidad |
| `particulas` | polvo, estrellas, burbujas, lluvia, nieve, chispas | area, n, clase, tam, vel, dispersion |
| `suelo` | terreno con textura (arena, luna, hierba, tierra, roca) | borde, material, colores, ondulacion, crateres |
| `agua` | agua vista desde arriba que avanza y retrocede | nivel (animable), lado, amplitud, colores, espuma |
| `huella` | huellas de pie o bota que aparecen o se borran | clase, largo, color, suela, marca, borrado, lado |
| `flecha` | flechas y trazos que se dibujan; la punta sigue la dirección final | puntos (lienzo), grosor, color, contorno, progreso, punta, discontinua |
| `barra` | barras que se llenan | ancho, alto, progreso, color, fondo, vertical |
| `persona` | personaje sencillo, también astronauta | alto, piel, ropa, pelo, casco, brazo_i, brazo_d, paso |
| `imagen` | PNG o SVG dibujado aparte | archivo, ancho, sombra |
| `rotulo` | cifra grande + unidad (dato en pantalla), puede contar | texto, contar, contar_desde, unidad, tam, color, capsula |
| `grupo` | objetos que se mueven juntos (hijos con x, y relativos) | ancho, alto, hijos |

Si un tema necesita algo que no existe, se añade un tipo nuevo en `elementos.py` con `@tipo("nombre")`, se documenta aquí y se comprueba que `ejemplos/005-huellas-luna` sigue saliendo igual.

## Reglas de estilo (de `DECISIONS.md`)
Pantalla completa, sin título fijo y sin Nova; subtítulo karaoke arriba y rótulos de dato integrados en la escena (ver `DECISIONS.md` y `OBJETIVO.md`). Siempre hay algo moviéndose; cada cambio de plano tiene que aportar información. Las flechas apuntan hacia donde va el movimiento. Las cifras van en letra en la locución; el subtítulo puede ponerlas en número.

## Ejemplo
`ejemplos/005-huellas-luna/generar.py` genera el `episodio.json` de la prueba del 2026-11-15 (6 escenas: playa vista desde arriba con ola y viento, pisada en la Luna, insignias de viento y lluvia tachadas, astronauta con rastro y años que pasan, sonda sobre el módulo con los senderos y lupa). El MP3 y el SRT no están en git; están en la carpeta local de Nico (`005-locucion.mp3`, `005-huellas-v1.srt`).
