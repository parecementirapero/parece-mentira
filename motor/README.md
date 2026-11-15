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
