# Referencias 2 — lo que copiar de los 9 vídeos que pasó Jorge (2026-11-15)

_Jorge, 2026-11-15. Complementa `OBJETIVO.md` (Nico). Se toma la técnica, nunca metraje, personajes ni textos._

Vídeos (480×848, 46–146 s; 20 archivos de WhatsApp = 9 vídeos distintos). Copia local, no en git:
`~/Documents/Parece Mentira/referencias-2/` del Mac de Jorge (`ref2_01…09_*.mp4`; el 07, de 23 MB, solo está en el chat de Jorge).

| # | Tema | Duración | Cortes (scene>0,25) | Lo mejor |
|---|---|---|---|---|
| 01 | Hotel y zombis: qué hacer en la primera hora | 77 s | 51 | Sección del edificio, contadores (59:30, 1:55 h, 150 litros), etiquetas con línea en la nevera |
| 02 | La luz del pasillo (terror) | 59 s | 36 | Luz práctica (bombilla, despertador 3:00 rojo), primeros planos de cara, puerta como motivo |
| 03 | Atragantarse / helado y cerebro | 65 s | 39 | Anatomía en sección, planos detalle, palabra en blanco grande sobre la imagen |
| 04 | La sacudida al dormirse | 46 s | 14 | Personaje recurrente visto desde arriba, metáfora (cerebro marioneta), bucle al final |
| 05 | Cómo funciona una lavadora | 78 s | 14 | Objeto transparente/en sección, palabra técnica en amarillo inclinada (FUELLE, CONTRAPESO), cifras en cápsula |
| 06 | La tumba de san Pedro | 77 s | 19 | Dorados y luz cenital, pared de grafitos, años en cápsula (1939, 1968), cortes de terreno |
| 07 | El mensaje de las 3:17 (terror) | 146 s | 28 | Planos POV (manos con el móvil), etiqueta roja de contexto bajo el subtítulo («03:17 AM», «REGLA 1») |
| 08 | Aprobar el teórico | 54 s | 2 (cambios dentro del plano) | Interfaz neón, números en círculo (1, 2, 3, 4), marcadores de acierto/fallo |
| 09 | Por qué no tienes visitas | 52 s | 6 | Rejilla de miniaturas con contador de vistas, metáforas visuales (anzuelo, ciudad que se ilumina) |

## Reglas que se aplican desde ya (todos los lotes)

1. **Un plano cada 1,5–4 s.** Una escena = un sitio; dentro, 2–3 planos: **general → primer plano → detalle** del objeto del que se habla, con corte seco (`"entrada": "corte"`, `camara.foco`). Cada cambio de idea, un plano nuevo.
2. **Enseñar por dentro.** Siempre que el tema sea «cómo funciona» o «qué hay debajo», un plano en sección (edificio sin fachada, tierra cortada, máquina transparente, cuerpo en corte).
3. **Una acción por frase.** Una mano pulsa, algo cae, gira, se enciende, se rompe. Nada de imagen fija con zoom como única animación.
4. **Etiquetas que señalan** (elementos con `"hud": true` para que no se corten al acercar):
   - cifra + unidad en cápsula pegada a lo que mide (`rotulo`);
   - etiqueta corta con línea hacia el objeto (`rotulo` pequeño + `flecha` sin punta);
   - **término clave en amarillo, grande, inclinado** (−6°) cuando se nombra algo técnico;
   - etiqueta de contexto roja pequeña bajo el subtítulo para hora, lugar o regla («1896 · ZANZÍBAR», «REGLA 1»).
5. **Luz con intención.** Fuente de luz visible (sol, bombilla, foco, pantalla) con `brillo`, viñeta 0,55–0,7 en escenas oscuras, color de escena según el tono (cálido = historia, frío = misterio/espacio).
6. **Personaje o objeto recurrente** que vuelve en varios planos; caras con emoción en el momento clave.
7. **Final en bucle**: el último plano conecta con el primero.
8. Se mantiene de `DECISIONS.md`: karaoke arriba, música suave, 45–60 s, sin título fijo, sin Nova.

## Límite actual
El acabado de render 3D (lavadora, anatomía, Vaticano) no se alcanza con formas y SVG por código. Para acercarse: prueba SVG vs. ilustración generada por IA (pendiente en `DECISIONS.md` → «Presupuesto y gastos»).
