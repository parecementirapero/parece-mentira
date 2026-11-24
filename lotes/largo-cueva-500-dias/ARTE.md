# Arte del vídeo largo «500 días en una cueva» — guía común

Este documento lo leen todos los que dibujan piezas para este vídeo. Si algo no está aquí, decide con criterio y apúntalo en tu informe.

## Qué es
- Vídeo de 8,5 min sobre Beatriz Flamini: 500 días sola a 70 m bajo tierra en una cueva de Granada (2021–2023), y por qué el cerebro pierde la cuenta del tiempo.
- También salen Michel Siffre (francés, 1962, cueva helada de los Alpes) y el experimento Deep Time (15 personas, 40 días, cueva de Francia, 2021).
- Se monta con el motor del repo (`motor/denso.py`): cada pieza es un SVG que el motor rasteriza y mueve (posición, escala, giro, opacidad, estirar ex/ey). No hay esqueletos: si algo tiene que moverse por dentro (pasar página, tejer, parpadear), se entregan **dos o tres fotogramas** de la misma pose (`_a`, `_b`, `_c`), idénticos salvo lo que cambia, y el motor los alterna.

## Estilo (v4 del canal, el que gusta)
Es ilustración detallada, no iconos planos ni dibujos de contorno grueso.
- **Luz con intención**: cada pieza tiene una luz principal clara (en la cueva, la luz cálida de las lámparas o del frontal; en los Alpes, luz fría).
  - Degradados en los volúmenes, sombra propia y luz de borde (rim light) del lado opuesto.
  - Sombra de contacto suave en el suelo, que se pueda desactivar con un parámetro.
- **Textura**: grano sutil (`grano()` / `filter="url(#grano)"`) en fondos y piezas grandes. Roca con vetas, manchas y capas; tela con pliegues; papel con borde.
- **Profundidad**: los fondos llevan varias capas (cerca oscuro y nítido; lejos más claro, azulado y desenfocado, con bruma entre capas). Nunca un degradado plano. Nada de bandas vacías.
- Contorno: no hay contorno negro grueso. Como mucho, una línea fina más oscura que el relleno en algún borde.
- **Paletas**:
  - Cueva de Granada:
    - Roca de #1a120d a #3d2a1f, #6b4a32 y #8a6446 en las zonas iluminadas.
    - Sombras frías #141b29 y negro azulado #07090f.
    - Luz cálida #ffcf8a / #ffb15e.
    - Acentos de cuarzo húmedo con brillos blancos.
  - Hielo de los Alpes (1962): #e8f6ff, #a9d6f5, #5f9fd1, #22405e y #0d1b2e.
  - Superficie de día: cielo #6fb6e8→#d6eefa; tierra andaluza #c9a26b, #a77b45; olivos #5b6b3a.
  - Cerebro y recuerdos: fondo #0b0f24→#1b1340, neones cian #2ff3ff y magenta #ff3df2 suaves, recuerdos en tonos cálidos.
- **Personas**: nada de monigotes, y nada de retratos realistas de personas reales.
  - **Beatriz** = una alpinista genérica, de unos 48 años, siempre con el mismo diseño:
    - Pelo castaño oscuro (#3b2618) recogido en coleta.
    - Piel #e8b48f, sombra #b97d5c, luz #f6cfae.
    - Forro polar verde azulado (#2a7f9e, luz #5fb3cf, sombra #174a5e) y pantalón gris oscuro #2e3440.
    - Botas marrones; casco amarillo mate #e0a92e con frontal cuando está en la cueva (el casco se puede quitar en algunas poses).
  - **Siffre** = hombre joven de 1962: barba corta castaña, gorro de lana rojo #b33a2e, parka caqui #6b7a3f y frontal antiguo.
  - **Caras bien dibujadas**:
    - Ojos con blanco, iris, pupila, brillo y párpado.
    - Cejas, nariz con sombra (sin línea), labios en dos tonos y orejas.
    - Pelo con mechones y brillo.
    - Proporción adulta: la cabeza es 1/7 de la altura. Las manos tienen forma de mano (pulgar y dedos juntos), no son bolas.
  - Coherencia: la misma persona tiene siempre la misma ropa, colores y peinado.
- **Prohibido**: texto o letras dentro de los dibujos (salvo que se pida), logotipos, banderas, marcas, fotos y personajes conocidos. Nada sangriento.

## Formatos y tamaños
- El vídeo sale en **dos formatos**: vertical 1080×1920 (TikTok) y horizontal 1920×1080 (YouTube).
- **Fondos**: cada fondo en dos archivos, `nombre.svg` (1080×1920) y `nombre_h.svg` (1920×1080).
  - Es la misma escena recompuesta, no recortada: en el horizontal el escenario se extiende a los lados con más roca, más cueva, más paisaje y más detalles.
  - En el vertical, lo importante va entre y=420 y y=1450: arriba va el subtítulo y abajo tapan los botones de la app. En el horizontal, lo importante va entre y=60 y y=880; abajo va el subtítulo.
  - Los fondos no llevan personajes ni objetos sueltos que haya que animar.
- **Piezas** (personajes y objetos): fondo transparente, lienzo del tamaño natural de la pieza (p. ej., 700×1000) y la pieza centrada y ajustada al lienzo, con poco margen.
  - Indica en el informe dónde quedan los pies o el punto de apoyo (fracción de la altura) para posarla en el suelo.
  - En las piezas con fotogramas, la misma caja y la misma posición en todos, para que al alternarlos no salte.

## Cómo programar
- Un archivo `lotes/largo-cueva-500-dias/generadores/ilus_<tuyo>.py` con una función `generar(dirsvg)` que escriba TODAS tus piezas en `dirsvg` y devuelva la lista de nombres.
- Usa `from motor.biblioteca import ilus` y `from motor.biblioteca.ilus import guardar, lg, rg, grano`. Pon `ilus.OUT = dirsvg` antes de `guardar`.
  - `guardar(nombre, cuerpo, w, h, defs)` mete ya los filtros `grano`, `papel`, `blur8`, `blur20`, `blur40` y `sombra`.
  - Mira `motor/biblioteca/ilus.py`: `bg_espacio_rico`, `_animal`, `bg_jungla_rica` y `meteorito` son buenos ejemplos de nivel.
- Prefijo propio en los ids de degradados para no chocar entre piezas.
- Aleatoriedad con semilla fija (`random.Random(n)`): el dibujo tiene que salir igual cada vez.
- Rendimiento: el motor rasteriza con `rsvg-convert`. Evita cientos de filtros de desenfoque grandes: un `blur40` sobre una capa vale, pero 300 elementos con filtro no. Cada SVG debe rasterizarse en menos de 3 s a su tamaño.
- **Revisión obligatoria**:
  - Rasteriza cada pieza con `rsvg-convert -w 400 x.svg -o x.png` y haz una hoja de contacto (PIL) con todas, sobre gris medio y con el nombre debajo. Mírala con la herramienta Read.
  - Corrige lo que se vea mal: caras raras, manos deformes, pies que flotan, piezas cortadas por el lienzo, colores que no casan, poses ilegibles.
  - Itera hasta que esté bien. Deja la hoja final en `/tmp/arte_<tuyo>/hoja.png`.
- No toques nada fuera de tu archivo `ilus_<tuyo>.py`, ni hagas commits: de eso se encarga el coordinador.

## Informe final (tu respuesta)
- Lista de nombres de pieza con su tamaño de lienzo y una línea de qué es: punto de apoyo, hacia dónde mira y fotogramas.
- Ruta de la hoja de contacto.
- Lo que no hayas podido hacer bien.
