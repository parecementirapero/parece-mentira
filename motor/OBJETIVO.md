# Vídeos objetivo — análisis de estilo

_2026-11-15 — Nico. 13 vídeos de referencia (R01–R13) que pasó Nico; las hojas de fotogramas están en `~/Documents/Parece Mentira/referencias-objetivo/` del Mac de Nico (no en git). Se toma la **técnica**, nunca metraje, personajes, marcas ni textos._

## Ficha técnica (medida)

| | Valor en los objetivos | Nuestro motor hoy |
|---|---|---|
| Formato | 9:16 (576×1024, descargas de TikTok), 30 fps, H.264, AAC 44,1 kHz | 1080×1920, 30 fps ✅ |
| Duración | 32–73 s, **mediana ≈ 57 s** (8 de 13 entre 50 y 65 s) | 35–50 s (110–140 palabras) |
| Cambios de plano | 8–10 por vídeo, **uno cada ~6 s** (rango 3,6–7,3 s); 2 vídeos son un plano largo con cámara viva | ~5,5 s ✅ |
| Movimiento | nunca quieto: 5–19 % de instantes casi estáticos | final estático ❌ |
| Volumen | **−19 a −20 LUFS** integrados, sin silencios (voz + base musical continua) | sin medir; sin música |

## Lo que hacen todos

1. **Gancho en el fotograma 0**: primer plano grande del protagonista *ya en acción* (sierra, mandíbula, oso rugiendo, tiburón con la boca abierta) y la primera frase es una pregunta o una afirmación imposible. El subtítulo arranca en el segundo 0.
2. **Subtítulo arriba (≈18 % de alto)**, centrado, sans geométrica (tipo Poppins/Inter), tamaño medio, sin borde, sombra suave. **Karaoke**: las palabras ya dichas en gris translúcido, la actual en blanco negrita, y las **palabras clave dentro de una cápsula azul oscura** (`cabeza`, `turbo`, `insulina`, `verdad`). 1–2 líneas, 3–7 palabras.
3. **Ilustración 2.5D vectorial con textura**: degradados, grano/pelaje, luz ambiental, viñeta, brillos, profundidad de campo; capas con paralaje. Personajes simples pero con ojos muy expresivos.
4. **Cada frase = una acción visual** que explica el dato: metáforas (el tiburón con un «turbo» y su barra de combustible, la insulina como llaves, mensajeros como sobres con alas), rayos X para ver dentro del cuerpo, gráficas que se dibujan (curva de glucosa), contadores y relojes que corren.
5. **Rótulos de dato integrados en la escena** (no títulos): cifra grande con unidad pequeña (`300 kg`, `+7 °C`, `92.462 cal`, `7 LITROS/hora`, `2,5 cm`, `DÍA 10`), barras con etiquetas (`FRÍO … CALOR`), titular de periódico, pantallas de aparatos.
6. **Cámara viva** dentro de cada plano: zoom lento, paneo, empujes hacia el detalle; transiciones con desenfoque de movimiento, disolución en partículas (el tiburón se deshace en el diente), zoom a través de un objeto, corte a negro en los giros.
7. **Estructura**: gancho → contexto (quién/cuándo) → mecanismo explicado en 3–4 pasos → giro («Pero…», «Eso sí:») → remate corto. Muchos **vuelven a la imagen del principio al final** (bucle: el mono, el niño, la boca del tiburón, la linterna), lo que invita a reverlo.
8. **Paleta por vídeo**: una o dos dominantes con acento cálido (rojo/amarillo/naranja) para lo importante; fondos oscuros en misterio/terror, saturados en ciencia.

## Qué cambiar en el motor (prioridad)

1. Subtítulo karaoke arriba con resaltado de palabra clave — **requiere cambiar `DECISIONS.md`** (hoy: «solo subtítulo blanco abajo»). Pendiente de confirmación de Nico/Jorge.
2. Gancho: plano 0 en primer plano con acción desde el primer fotograma.
3. Cámara: zoom/paneo suave por plano + transiciones con desenfoque/partículas.
4. Rótulos de dato (cifra + unidad, barras etiquetadas, contadores).
5. Textura y luz: grano, degradados, viñeta, sombras y brillos; personajes con ojos expresivos.
6. Final en bucle con la imagen del principio.
7. Música de fondo baja bajo la voz y normalizar a −19 LUFS (requiere elegir fuente de música con licencia).
8. Duración objetivo 45–60 s (≈130–170 palabras) — **cambia `AGENTE.md`/créditos de ElevenLabs** (+~25 % de caracteres por lote).
