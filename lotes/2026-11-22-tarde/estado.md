# Lote 2026-11-22-tarde — estado

**Estado**: 🟡 **en revisión** (v1). Falta el «ok».
**Quién**: Jorge, con el agente, en el chat https://claude.ai/code/session_019BG1dFtXHqVXWrKbh8QXsf. El turno de las 20:00 del 22-11 no se hizo, y Jorge pidió hacerlo hoy (23-11, ≈14:00) con sus temas.
**Carpeta local**: `Documents/Parece Mentira/lotes/2026-11-22-tarde/` (Mac de Jorge): MP4, SRT, manifiestos, locuciones, alineaciones, portadas y `metadatos.json`.

## Encargo de Jorge
«Quiero que veas el que hemos hecho de la imagen al revés, y para el lote me hagas uno así de esos temas, después quiero que me hagas uno de amor, y el último… como este vídeo que te voy a mandar, si hace falta cópialo». El vídeo de referencia es de otra cuenta. **No se copia**: así se acordó con Jorge en el chat («Sí, versión propia»). Se hace un test de atención con escena, personajes, guion y montaje nuestros (DECISIONS: se toma la técnica, nunca metraje, personajes ni textos).

## Vídeos
| # | Título | Duración | SHA-256 corto | Calidad | Portada |
|---|---|---|---|---|---|
| 01 | Tu vista tiene un AGUJERO (haz la prueba) 👁️⚫ | 50,6 s | 1d07f855b04e | 45/100 | «TU VISTA TIENE UN AGUJERO» · abajo · 0,75 s |
| 02 | Enamorarte cambia tu cerebro ❤️🧠 | 58,8 s | 27650c578d80 | 55/100 | «ENAMORARTE CAMBIA TU CEREBRO» · dato · 19,75 s |
| 03 | ¿Cuántos botes cuentas? Test de atención 🟡👨‍🚀 | 58,5 s | 6cdfb1160c94 | 58/100 | «¿CUÁNTOS BOTES CUENTAS?» · centro · 3,75 s |

SHA en el Mac = SHA del render. Voz oficial por API desde el Mac de Jorge; créditos de ElevenLabs al acabar: **18.867**. El 02 lleva versión corta: se quita «Pues eso.» para no pasar de 60 s.

## Decisiones
- Los temas los eligió Jorge, así que la regla de tendencias del día no se aplica en este lote.
- 01: Ciencia, experimento, gancho de dato de 5 palabras, igual que «la imagen al revés» del 22-11, que fue la referencia que pidió Jorge. Incluye una prueba de verdad: del segundo ≈21,7 al ≈31 la pantalla es la cruz y el punto, y se deja casi quieta a propósito. Por eso baja la nota de calidad (densidad y movimiento).
- 02: Ciencia, cadena de datos.
- 03: **experimento del lote: formato interactivo** (reto con la respuesta en los comentarios). La pelota amarilla bota **11 veces**, y la respuesta va en el comentario fijado. La escena del test es continua aunque haya cortes: las posiciones se calculan con el tiempo absoluto. La portada no enseña al astronauta para no estropear la sorpresa. Ficha con `reciclado=sí`, porque el formato ya fue viral en otra cuenta.

## Prueba del primer segundo
- 01: el agujero negro que se abre sobre el paisaje · «Tu vista tiene un agujero.» (5)
- 02: un corazón que late fuerte con un cerebro que se enciende detrás · «Enamorarte cambia tu cerebro.» (4)
- 03: la pelota amarilla volando entre dos jugadores · «Cuenta los botes amarillos.» (4)

## Control de calidad
- `motor.guion`: sin ❌.
- `construir`: todos los textos se pueden leer.
- ffprobe: 1080×1920, 30 fps, h264, AAC 48 kHz.
- `motor.calidad --mp4`: **sin ❌**. Notas 45/55/58 (`calidad-0N.md`). Los ⚠ son de densidad (menos elementos por plano que la referencia, 24–26 planos) y del tramo quieto de la prueba del 01, que es a propósito.
- Hojas de fotogramas revisadas. Arreglado antes del render: cámaras del test más cerca, rótulo largo de «ceguera por falta de atención» partido en dos, «⚠» que la fuente no tiene, versión corta del 02 (60,1 s → 58,8 s) y tiempos de lectura.
- Fichas de variables: 3 nuevas.

## Siguiente paso
«ok» (o «ok 1 y 3») en este chat → AGENTE §8 desde el Mac de Jorge.
- Correo de revisión: `1a20895152b1ce72`.
