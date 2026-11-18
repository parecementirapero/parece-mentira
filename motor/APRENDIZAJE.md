# Aprender a aprender — cuaderno del canal

Cómo mejora el canal de un lote al siguiente sin depender de opiniones. Tres fuentes, de más a menos fiable:

1. **Nuestros datos** (Studio + `estadisticas/`): lo único que dice qué funciona *en este canal*.
2. **Referentes vistos fotograma a fotograma**: qué hacen los Shorts del nicho con millones de vistas.
3. **Investigación publicada** (`motor/GUIA_CALIDAD.md`): por qué podría funcionar.

> **Desde el 2026-11-17 el nivel de cada conclusión lo pone el estudio** (`estadisticas/datos/estudio.md`, método en
> `estadisticas/estudio/README.md`): pista, indicio o regla, con vídeos comparados a la misma edad. Todo lo de este
> cuaderno es, hoy, **pista**: solo 3 vídeos tienen lecturas con 24 h o más. Los experimentos de la tabla de abajo se
> abren con ficha previa (`python3 estadisticas/estudio experimento nuevo …`), no con «1 vídeo de 3».

Regla: una idea sale de 2 o 3, se convierte en **hipótesis**, se prueba cambiando **una sola cosa** en un vídeo del
lote, y solo pasa a `DECISIONS.md` cuando los datos (1) la apoyan. Con menos de 5 vídeos por grupo todo es «pista».

---

## Rutina (qué hace el agente y cuándo)

| Cuándo | Qué | Con qué |
|---|---|---|
| Al arrancar cada lote | Leer `estadisticas/datos/aprendizajes.md` y la tabla de experimentos de abajo | — |
| Al arrancar cada lote | Apuntar «Se quedaron viendo», vistas y horas de los vídeos con 24 h o más | `herramientas/studio_shorts.js` → `estadisticas/studio.json` |
| Al arrancar cada lote | Tiempo medio, % que lo ve entero y curva de retención en TikTok Studio de los vídeos con 24 h o más | `herramientas/tiktok_retencion.js` → `estadisticas/tiktok_studio.json` |
| Una vez por semana (lunes) | Mirar 6 Shorts del nicho con muchas vistas y apuntar lo que se repite | `herramientas/hoja_short.js` → tabla de referentes |
| Antes de entregar | `python3 -m motor.calidad` y guardar `calidad.md` en el lote | — |
| Al publicar | Etiquetar el vídeo en `estadisticas/etiquetas.json` (tema, gancho, estructura, **experimento**) | — |
| A los 7 días | Cerrar el experimento: resultado y decisión en la tabla | — |

Tres números por vídeo, en este orden:

- **Se quedaron viendo (%)** → mide el gancho y el primer segundo.
- **Segundos por vista** (horas × 3600 / vistas) y, a las 48–72 h, **% medio visto** → mide el ritmo y la duración.
- **Vistas** → es la consecuencia; no se optimiza directamente.

---

## Nuestros datos (lectura de Studio del 2026-11-17 00:25)

| Vídeo | Dur. | Se quedan | Vistas | s por vista | Publicado hace |
|---|---|---|---|---|---|
| Huellas en la Luna (`D_2cV1qhmfA`) | 48 s | **79,4 %** | 7.400 | 26,5 | 31 h |
| **Luna densa** (`jQmhf8o1PfY`) | 55 s | **73,3 %** | 2.400 | 27,9 | 3,5 h |
| Luna v4 antiguo (`oZSuHN-46FI`, retirado) | — | 65,3 % | — | — | — |
| Nudillos (`7PoER_sR6R0`) | 58 s | 60,6 % | 1.800 | 20,6 | 2 h |
| Guerra de 38 min (`bS6AUPYxr7s`) | 53 s | 60,4 % | 1.300 | 18,3 | 25 h |
| Moáis (`XGf1wOPygU8`) | 47 s | 52,1 % | 1.100 | 17,3 | 25 h |
| Puertas (`cTRgkuY21mw`) | 55 s | 38,9 % | 612 | 18,2 | 1 h |
| Apolo 11 / móvil (`hfRveipHIdk`) | 52 s | 26,5 % | 55 | — | 10 min (sin valor aún) |

Lo que se ve (todo **pista**: 7 vídeos, edades distintas, vistas redondeadas por Studio):

1. **Las vistas siguen a «se quedaron viendo».** El orden de vistas es casi el mismo que el de ese porcentaje. Lo
   que más mueve el resultado es el primer segundo.
2. **El método denso mejoró el gancho del mismo tema:** Luna antigua 65,3 % → Luna densa 73,3 %, y lleva 2.400
   vistas en 3,5 h (la antigua tenía 1.711 a las ~18 h).
3. **Nadie ve más de ~28 s de media**, dure el vídeo 47 o 58 s. Los dos mejores retienen 26–28 s; el resto, 17–21 s.
   Pagamos 55 s de producción y la gente ve la mitad. → hipótesis H2.
4. **Espacio con un objeto físico en el primer fotograma** (huella, uña) queda por encima de los ganchos de «por
   qué te pasa X» (puertas 38,9 %, nudillos 60,6 %). Es pronto para los dos de la tarde; se revisa a las 48 h.

**Segunda lectura (01:37, 70 minutos después)** — sirve para corregirme:

| Vídeo | Se quedan | Vistas | s por vista | Cambio en 70 min |
|---|---|---|---|---|
| Huellas en la Luna | 80,1 % | 8.000 | 26,5 | +600 vistas (lleva 32 h y sigue creciendo) |
| Luna densa | 74,1 % | 2.500 | 28,7 | +100 vistas (se ha frenado) |
| Puertas | 47,4 % | 1.400 | 17,7 | +800 vistas |
| Nudillos | 60,5 % | 1.700 | 21,8 | sin cambio |
| Apolo 11 / móvil | 32,0 % | 533 | 8,1 | +480 vistas (primera hora) |

5. **Matiz al punto 1:** «Puertas» sumó 800 vistas en una hora con solo un 47 % de «se quedan». En las primeras
   horas YouTube reparte vistas de prueba a todos; el porcentaje decide **si sigue repartiendo después** (Huellas,
   con 80 %, sigue creciendo a las 32 h; Nudillos, con 60 %, ya está parado a las 3 h). Por eso los vídeos se
   comparan a las 48 h, no la primera noche.
   Tercera lectura (02:41): Huellas va por 8.500 vistas a las 33 h y sigue sumando unas 500 por hora en la tarde
   de Latinoamérica.
6. **El gancho «tu móvil frente al Apolo 11» es el peor hasta ahora (32 %)** y el que menos segundos retiene (8 s).
   A revisar su primer fotograma cuando tenga 24 h.

### El hallazgo más útil de la noche: el primer fotograma de NUESTROS vídeos

Mirados los primeros 5 s de nuestros Shorts publicados (`herramientas/hoja_short.js`) al lado de su «se quedaron
viendo»:

| Vídeo | Se quedan (YouTube) | Siguen al segundo 1 (TikTok) | Palabras en pantalla al empezar | Qué pasa en los 3 primeros segundos |
|---|---|---|---|---|
| Huellas en la Luna | 80 % | 84 % | 1 | Una bota grande **cae** y pisa. Se entiende sin leer |
| Luna densa | 74 % | 72 % | 3 | Un dedo grande sube; la Luna detrás |
| Nudillos | 60 % | — | 10 (tres líneas) | Dos manos casi quietas + dos rótulos |
| Guerra de 38 minutos | 60 % | — | 1–4 | Un marcador de fútbol en un estadio (metáfora: no se ve ninguna guerra) y un balón pequeño |
| Moáis | 52 % | 55 % | 1 | Una cabeza de moái grande… **completamente quieta 3 segundos** |
| Puertas | 47 % | — | 13 (tres líneas) | Personaje pequeño de pie, quieto, en un pasillo |
| Apolo 11 / móvil | 32 % | — | 14 (cuatro líneas) | Un móvil con iconos, fondo lleno de aparatos y un contador |

Lectura (7 vídeos, sigue siendo **pista**), corregida al añadir los dos últimos que miré:

- **Lo que mejor separa arriba de abajo es si algo grande se MUEVE en el primer segundo y se entiende sin leer.**
  Los moáis tienen muy poco texto y un solo objeto grande, pero no se mueve nada durante 3 s: 52 %.
- **El muro de texto empeora las cosas** (los tres peores tienen 10–14 palabras en pantalla), pero poco texto no
  basta por sí solo.
- **Las metáforas en el primer plano despistan:** un marcador de fútbol para hablar de una guerra obliga a esperar
  a la voz para entender de qué va.
- El «gancho entero en el fotograma 0» (DECISIONS 2026-11-16) funciona con frases de 3 palabras y se vuelve un
  muro con frases de 13.

**Comprobado fuera del canal (02:40):** medí cuánto cambia la imagen en el primer segundo de 32 Shorts del nicho
sacados de las mismas búsquedas (diferencia media entre fotogramas cada 0,25 s, en miniatura):

| Grupo | Movimiento en el primer segundo (mediana) | En los 3 primeros | Duración mediana |
|---|---|---|---|
| 16 con más de 100.000 vistas | **23,5** | 26,2 | 59 s |
| 16 con 300–3.000 vistas | 13,8 | 18,3 | 61 s |
| Nuestros 7 | Huellas 15,2 · Guerra 11,6 · Luna densa 7,6 · Apolo 6,8 · Puertas 4,1 · Nudillos 2,7 · Moáis 1,6 | | 47–58 s |

- Los que triunfan se mueven casi el doble en el primer segundo que los que no (los grupos se solapan: es una
  tendencia, no una ley). A diferencia de H9, esta hipótesis **sí aguanta** la comprobación externa.
- **Nuestros arranques son mucho más tranquilos que los del nicho:** solo Huellas, nuestro mejor vídeo, supera la
  mediana de los Shorts *sin éxito*. Es el sitio donde más margen tenemos.
- La duración no separa a los dos grupos (59 frente a 61 s): otro motivo para no tocar los 55 s.

Puesto en práctica: `python3 -m motor.guion guion.txt` revisa el guion **antes de gastar voz** (gancho, duración, cadena de preguntas, tramos sin dato, cifras en letra, palabras solo de España); `motor.calidad` da ❌ si la primera frase pasa de 9 palabras y ⚠ si pasa de 5, y avisa si el
primer segundo del MP4 casi no se mueve; AGENTE §3 pide primera frase de 5 palabras o menos y un solo objeto grande
en acción. El gancho de la Luna v7 se rehízo con eso (el aviso saltó en mi propia v6).

### TikTok Studio: las primeras curvas de retención reales (2026-11-17, 02:20)

YouTube aún no da curvas, pero TikTok sí (`herramientas/tiktok_retencion.js` → `estadisticas/tiktok_studio.json`).

| Vídeo | Vistas | Tiempo medio | Lo ven entero | Siguen a los 3 s | A los 10 s | A los 20 s |
|---|---|---|---|---|---|---|
| **Luna densa** (54 s) | 266 | **22,4 s** | 21,4 % | 60 % | 42 % | 34 % |
| Nudillos (58 s) | 263 | 20,7 s | 18,6 % | — | — | — |
| Huellas en la Luna (47 s) | 617 | 19,8 s | 21,7 % | 63 % | 45 % | 34 % |
| Guerra de 38 minutos (52 s) | 424 | 16,5 s | 13,0 % | — | — | — |
| Moáis (46 s) | 407 | 13,7 s | 16,1 % | 41 % | 26 % | 21 % |
| Puertas (55 s) | 229 | 9,3 s | 6,1 % | — | — | 14 % (a los 16 s) |

7. **TikTok ordena los vídeos casi igual que YouTube.** Tiempo medio en TikTok: Luna densa, Nudillos, Huellas,
   Guerra, Moáis, Puertas. «Se quedaron viendo» en YouTube: Huellas, Luna densa, Nudillos, Guerra, Moáis, Puertas.
   Dos redes distintas dicen lo mismo, así que no es ruido: Puertas es flojo de verdad y los dos de la Luna, fuertes.
8. **El método denso tiene el mejor tiempo medio del canal** (22,4 s), aunque sea solo con 266 vistas.
9. **La pérdida está al principio, no en medio.** Hasta los dos mejores pierden el 40 % en los 3 primeros segundos
   y la mitad antes del segundo 10. Después la curva cae muy despacio (medio punto por segundo). Mejorar el
   segundo 0–3 vale mucho más que pulir el segundo 30.
10. **Dentro de la Luna densa:** el mayor escalón intermedio está en el segundo 9–10 (46 → 42 %), justo en la
    cuenta atrás «3, 2, 1», que eran los tres planos casi vacíos que detectó el control y que la v6 rehízo. Los
    dinosaurios (30–38 s) son el tramo que mejor aguanta: no se va casi nadie (26 → 24 %). El siguiente escalón
    es al pasar a la almeja (38–39 s).
11. **Sobre la versión corta (H2), la evidencia está dividida.** A favor: casi el 80 % ya se ha ido en el segundo
    40, y varios referentes duran menos de 35 s. En contra: el mayor estudio público que conozco (Paddy Galloway
    y Chris Gileta, 2023: 5.400 Shorts de 33 canales, 3.300 millones de vistas) encontró que los Shorts de
    **50–60 s tenían más vistas de media** y que lo que mejor acompaña a las vistas es la duración media vista en
    segundos ([resumen](https://nowbam.com/decoding-the-youtube-shorts-algorithm/),
    [hilo original](https://threadreaderapp.com/thread/1646898356419981315.html)). Un vídeo de 35 s difícilmente
    superará los 28 s de media que ya consiguen los nuestros de 55. **Conclusión: se mantienen los 55 s como
    norma**; la versión corta queda como prueba suelta, no como recomendación.

### Lectura a 48 h (2026-11-18, 22:35) — primera comprobación de las reglas nuevas

| Vídeo | Publicado | Reglas del primer segundo | Se quedan (YouTube) | Vistas | s por vista | TikTok: tiempo medio |
|---|---|---|---|---|---|---|
| Huellas en la Luna | 15-11 | antes | **81,4 %** | 13.500 | 28,9 | 19,8 s |
| Luna densa | 16-11 | antes (gancho de 3 palabras) | **80,3 %** | 6.700 | 29,4 | 22,4 s |
| Nudillos | 16-11 | antes | 63,5 % | 2.200 | 23,6 | 20,7 s |
| Guerra de 38 minutos | 15-11 | antes | 60,1 % | 1.400 | 17,7 | 16,5 s |
| Moáis | 15-11 | antes | 52,0 % | 1.200 | 16,8 | 13,7 s |
| Puertas | 16-11 | antes | 47,7 % | 1.400 | 19,8 | 9,3 s |
| Apolo 11 / móvil | 17-11 (00:15) | antes | 35,2 % | 1.100 | 11,5 | — |
| Huella de koala | 17-11 | **con reglas** | 71,3 % | 2.800 | 24,9 | 6,4 s (58 vistas) |
| Saturno flotaría | 17-11 | **con reglas** | 67,4 % | 2.200 | 26,7 | 14,4 s |
| Plátano radiactivo | 17-11 | **con reglas** | 64,8 % | 1.400 | 23,9 | 12,3 s |
| El Sol que ves ya es pasado | 18-11 (7 h) | **con reglas** | 65,2 % | 373 | — | — |
| Día de 18 horas | 18-11 (14 h) | **con reglas** | 64,3 % | 316 | — | — |
| Cebolla | 18-11 (8 h) | **con reglas** | 60,8 % | 1.100 | 17,0 | — |
| Un rayo, 5 veces más caliente | 17-11 (23:00) | **con reglas** | 56,9 % | 1.600 | 18,0 | — |

- **H0 (método denso), a favor con claridad:** la Luna densa ha subido al 80,3 % (la antigua, 65,3 %), lleva 6.700
  vistas y es el vídeo con más segundos por vista del canal (29,4). Sigue siendo un solo par de vídeos.
- **H7 (primer segundo), a favor en YouTube, con matices:** los 7 vídeos hechos con las reglas están entre 57 y
  71 % (media 64 %); los 5 anteriores que no son de la Luna, entre 35 y 64 % (media 52 %). Ha subido el suelo:
  ya no hay ninguno por debajo del 55 %. Pero **ninguno llega al 80 %** de los dos de la Luna, así que el primer
  segundo no lo explica todo (¿el tema?, ¿la Luna como objeto?).
- **TikTok no lo confirma:** los tres del 17 por la mañana tienen un tiempo medio de 6–14 s, peor que los
  anteriores (20–22 s). Con 58–242 vistas es poco dato, pero hay que mirarlo: en YouTube esos mismos vídeos
  retienen 24–27 s.
- **Aviso:** «La Gran Muralla» y «Tu perro copia tus bostezos» (18-11 por la mañana) llevan 7 y 8 vistas en
  YouTube después de 12 horas. No es normal: comprobar en Studio que están en público y sin restricciones.
- YouTube ya dibuja la curva de retención de los vídeos del 15 y 16; es un gráfico y no la he leído punto a punto.

---

## Referentes vistos (2026-11-17, YouTube, búsqueda «dato curioso del espacio #shorts»)

Mirados con `herramientas/hoja_short.js`: 14 fotogramas por vídeo y detección de cortes. **Sin sonido** (no tengo
oído) y sin descargarlos.

| Short | Vistas | Dur. | Texto en pantalla | Imagen | Estructura |
|---|---|---|---|---|---|
| `y8oM-HNweN0` 3 curiosidades del espacio | 15 M | 55 s | Palabras sueltas enormes, centradas | Fondo negro, un objeto, personaje fijo del canal | Cuenta de 3 + personaje |
| `yA164RTA47Y` Un día miras al cielo y ves esto… | 6,6 M | 59 s | 2–3 palabras, centro de la pantalla | Persona a cámara + planos de cine oscuros | «Un día te despiertas…» (segunda persona) |
| `DOVZJRThzFQ` ¿Y si orbitamos la estrella más grande? | 2,5 M | 26 s | **Una palabra** cada vez, tercio inferior, blanco/amarillo | Simulación espacial, zoom continuo, flecha roja | «¿Qué pasaría si…?» |
| `Wk4EWnxS0T8` Así de grandes somos | 2,5 M | 18 s | **Ninguno** | Un solo plano: cada astro se vuelve diminuto junto al siguiente | Escala, sin cortes |
| `OMVcqDR3gxc` Dato curioso de Neptuno | 1,9 M | 43 s | Una frase corta por planeta | Un planeta centrado sobre negro | Patrón repetido que el último rompe (remate de humor) |
| `EZJYTZgwxvc` ¿Cuánto pesa el universo? | 717 K | 34 s | **Una palabra** cada vez, centro, clave en amarillo | Imagen saturada a pantalla completa, un sujeto | Pregunta → acumulación |
| `9d5AAGHaZyg` Cuánto sobrevives sin traje | 48 K (nuevo) | 25 s | **Una palabra** cada vez, tercio inferior | Astronauta, inserciones de meme | «Tú» en peligro |

Lo que se repite (y en qué nos diferenciamos):

| Patrón | Ellos | Nosotros hoy | Qué hacemos |
|---|---|---|---|
| Subtítulo | 1–3 palabras enormes, en el centro o tercio inferior (5 de 7) | Línea karaoke de ~26 letras, pequeña, **arriba** (y=320) | **H1**: modo «palabra» |
| Duración | Mediana 34 s; cuatro de siete duran menos de 35 s | 47–58 s | **H2**: un vídeo corto por lote |
| Sujeto | Uno solo, grande, centrado, a pantalla completa | Uno + muchos detalles | Mantener el sujeto dominante; los detalles no compiten (ya en la guía) |
| Gancho | Pregunta, «¿y si…?» o segunda persona («tú», «un día te despiertas») | Comparación con lo cotidiano | **H3**: probar segunda persona |
| Ritmo | De 0 cortes a 2 por segundo: **no hay un ritmo ganador**; lo constante es que algo nuevo aparece cada 1–2 s | 43 cortes/min | No subir más los cortes; cuidar que cada plano traiga algo nuevo |
| Remate | Patrón que se rompe, humor, personaje | Dato final + pregunta | **H4**: remate con giro |
| Personaje | Dos de siete tienen personaje fijo | Nova no sale en los vídeos (DECISIONS 2026-11-14) | No se toca: decisión de Nico |

### Segunda tanda (2026-11-17, historia y curiosidades)

| Short | Vistas | Dur. | Texto en pantalla | Imagen | Estructura |
|---|---|---|---|---|---|
| `Rs0WLQvh1A4` ¿Qué hay en el cerebro de Einstein? | 9,9 M | 38 s | **Una palabra** cada vez, centro, amarillo | Fotos reales a pantalla completa, siempre en movimiento | Pregunta sobre alguien conocido |
| `yJPzlcG_cfY` El invento que predijo la destrucción del imperio | 5,2 M | 74 s | Subtítulo pequeño | **Ilustración** con fondos pintados y **personajes con cara** que se asustan, sudan, se sorprenden | Historia con protagonista |
| `UIuWxBSEK0Y` Tres datos históricos alucinantes | 5,0 M | 39 s | **Una palabra** cada vez, centro | Imágenes pintadas, cálidas, con barridos | Tres datos |
| `0ojg988okNQ` El invento azteca… | 0,7 M | 67 s | **Una palabra** cada vez, tercio inferior | Primeros planos de personas comiendo (vídeo generado) | La acción ya está pasando en el fotograma 0 |

Con las dos tandas (11 vídeos): **8 de 11 usan subtítulo de 1–3 palabras enormes en el centro o tercio inferior**;
ninguno lo lleva arriba como nosotros. El único ilustrado como los nuestros (5,2 M) cuenta el dato a través de
**personajes con emociones**, no de objetos y cifras → hipótesis H6.

### Títulos: 383 Shorts del nicho (9 búsquedas en YouTube, 2026-11-17)

- **La mediana de vistas de un Short del nicho en el buscador es 73.** Solo 7 de 383 pasan del millón. Casi todo lo
  que se publica no lo ve nadie: nuestros 1.000–7.000 por vídeo ya están muy por encima de lo normal.
- **El título no explica las vistas.** Ningún rasgo (pregunta, mayúsculas, emoji, número, «sabías que», longitud)
  separa de forma fiable a los que triunfan: las diferencias que salen dependen de la búsqueda de la que venga cada
  vídeo. Cuadra con nuestro dato de que el 97 % de las vistas llega por el feed de Shorts.
- Única pista utilizable: los títulos de **lista genérica** («5 datos curiosos de…», «3 curiosidades…») son los más
  abundantes y tienen la mediana más baja (10 vistas frente a 148 del resto). Mejor un hecho concreto y raro en el
  título («Escapó de Alcatraz con una cuchara») que una lista.
- Conclusión práctica: **no gastar tiempo en optimizar títulos**; gastarlo en el primer segundo.

### Tercera tanda: ganadores frente a perdedores (2026-11-17, 02:15) — **me corrige**

Hasta aquí solo había mirado vídeos con muchas vistas. Esta vez comparé los primeros 3 s de 8 Shorts de las mismas
búsquedas con 0,1–1,4 M de vistas con los de 7 que se quedaron en ~2.000.

| | Con muchas vistas | Con ~2.000 vistas |
|---|---|---|
| Subtítulo de 1–3 palabras enormes | Sí, la mayoría | **También** (5 de 7) |
| Ilustración con personajes de dibujo | Alguno | **Varios** (3 de 7) |
| Mapas, fotos, vídeo generado | De todo | De todo |
| Tema | Einstein, la Tierra, Laika, «datos perturbadores», el cuerpo, el espacio | Un rey de España y Portugal, «zafarrancho de combate», una batalla desconocida, el primer semáforo |

1. **El subtítulo de palabra NO distingue a los que triunfan:** lo llevan casi todos, también los que nadie ve. Es
   una costumbre del nicho, no una ventaja demostrada. Rebajo H1: sigue mereciendo una prueba, pero ya no es «lo
   primero que probaría».
2. **Los personajes de dibujo tampoco:** aparecen igual entre los de 2.000 vistas. La decisión de Nico de no
   usarlos no pierde nada según esta muestra.
3. **Lo que sí cambia entre un grupo y otro es el tema:** los que suben hablan de algo que **cualquiera reconoce en
   un segundo** (una persona famosa, la Tierra, tu cuerpo, un perro en el espacio); los que no, de historia local o
   de un detalle erudito. Cuadra con nuestros datos: la Luna y las huellas en la Luna, arriba; Zanzíbar y los
   moáis, abajo. → hipótesis H9. **Comprobado después con los 383 títulos y no se sostiene** (ver la tabla de
   experimentos): era una impresión sacada de 15 vídeos.
4. **Existe otro formato: el micro-Short.** El de 1,4 M dura **5 segundos**: un fondo de meme con una lista de
   texto que no da tiempo a leer, así que la gente lo repite. Otro de 0,7 M dura 15 s. Ahí el «muro de texto» es el
   truco, no el fallo. Mi regla del gancho corto vale para vídeos narrados de 35–55 s, no para ese formato. →
   hipótesis H8.

### Lo que YouTube ha dicho del algoritmo (oficial) y lo que es folclore

Oficial:

- Desde el 31 de marzo de 2025, una «vista» de Short cuenta en cuanto empieza a reproducirse o se repite, sin
  tiempo mínimo; el recuento antiguo se llama ahora «vistas con interacción» (engaged views) y es el que vale para
  monetizar ([Tubefilter](https://www.tubefilter.com/2025/03/26/youtube-shorts-views-counting-stats/),
  [PPC Land](https://ppc.land/youtube-changes-how-shorts-views-are-counted-from-march-31/)). **Para nosotros:** las
  vistas que apuntamos incluyen a los que deslizan; por eso «se quedaron viendo» y los segundos por vista dicen más.
- El algoritmo busca una «audiencia semilla» para cada Short y, según cómo responda, le da mucho más tráfico o lo
  deja caer; por eso muchos vídeos suben y se paran. No hay una duración que ayude: que dure lo que pida la
  historia. Borrar y volver a subir un Short para que arranque se desaconseja, porque puede verse como spam (Todd
  Sherman, responsable de producto de Shorts, 2023:
  [TechCrunch](https://techcrunch.com/2023/08/25/youtube-demystifies-the-shorts-algorithm-views-and-answers-other-creator-questions/)).
  **Para nosotros:** republicar la Luna con la v7 tiene ese riesgo; mejor usarla de modelo.
- Señales que YouTube nombra: la proporción que elige ver, la duración media, el % medio visto, los «me gusta» y
  las encuestas de satisfacción. No hay preferencia por un formato, ni frecuencia mínima de publicación, ni
  umbral oficial de retención ([resumen con las fuentes de la ayuda de YouTube](https://www.truefuturemedia.com/articles/youtube-shorts-algorithm-data-backed-guide)).

- Publicar cuando la audiencia está activa puede ayudar a las primeras vistas, pero no se sabe que cambie las
  vistas a largo plazo ([ayuda de YouTube: rendimiento y preguntas frecuentes](https://support.google.com/youtube/answer/141805)).
- Definiciones oficiales de «Se mostró en el feed» y «Vistos (frente a deslizados)»:
  [ayuda de YouTube: alcance](https://support.google.com/youtube/answer/9314355?hl=en).

Folclore (lo repiten muchos blogs, YouTube no lo ha confirmado): que todos los Shorts pasan por «lotes de prueba»
fijos en la primera hora, que hay que publicar a una hora concreta, que publicar más da ventaja, que el algoritmo
castiga repetir formato, y cualquier porcentaje «mágico» (70 %, 75–80 %…).

Límites de estas muestras: 26 vídeos en total, pocos temas, elegidos por el buscador (los que fracasaron haciendo lo mismo no
salen), y sin sonido. Vale para generar hipótesis, no para dar nada por demostrado.

---

## Experimentos

Una hipótesis = un vídeo del lote con ese cambio y los otros dos sin él. Se etiqueta en
`estadisticas/etiquetas.json` → `"experimento": "H1 palabra"`.

| Id | Hipótesis | Cómo se prueba | Se mide con | Estado |
|---|---|---|---|---|
| H0 | El método denso retiene mejor que el v4 | Luna densa frente a Luna v4 (mismo tema) | Se quedan: 80,3 % frente a 65,3 %; 29,4 s por vista, el mejor del canal | **A favor** a las 48 h (2026-11-18). Un solo par de vídeos: se sigue como norma y se revisa con más temas |
| H1 | Subtítulo de 1–2 palabras, grande y centrado, sube «se quedan» y la retención | `v.construir(..., subtitulos="palabra")` en 1 de 3 vídeos | Se quedan, s por vista | Preparado en el motor. **Rebajado el 2026-11-17:** lo usan casi todos, también los Shorts con 2.000 vistas, así que no hay señal de que ayude; probarlo sigue siendo barato. Pendiente del «sí» de Nico/Jorge |
| H2 | Un vídeo de 30–38 s (95–110 palabras) consigue más % visto y más vistas que uno de 55 s | 1 de 3 vídeos corto, mismo nivel de montaje. Para probar sin gastar voz: `Video(..., omitir=[(i0, i1)])` quita frases enteras de una locución ya hecha | % medio visto, vistas a 48 h | Preparado (Luna corta de 35 s). **Rebajado el 2026-11-17:** un estudio de 5.400 Shorts dice lo contrario (los de 50–60 s tienen más vistas). No lo recomiendo como cambio de norma; como mucho, una prueba suelta |
| H3 | Gancho en segunda persona («Si mañana…», «Mira tu…») supera al gancho de dato | 1 de 3 vídeos | Se quedan | Pendiente. La Luna («Mira tus uñas») ya apunta a favor |
| H4 | Remate con giro (el último dato rompe el patrón) sube repeticiones y comentarios | 1 de 3 vídeos | % visto > 100 %, comentarios | Pendiente |
| H6 | Un personaje con cara que reacciona al dato retiene más que objetos y cifras solos | — | — | **Descartado por Nico el 2026-11-17** («no me mola lo de poner el personaje») antes de probarlo. El código y la muestra se han quitado del repo. No volver a proponerlo |
| H7 | Primer segundo con un solo objeto grande **en movimiento**, que se entiende sin leer, y gancho de 5 palabras o menos → «se quedan» por encima del 70 % | Regla ya en AGENTE §2–3, en `motor.guion` y en `motor.calidad` (❌ si el primer segundo está quieto); comparar los lotes desde el 2026-11-17 con los anteriores | Se quedan (YouTube), % al segundo 1 y 3 (TikTok) | **A favor en YouTube (2026-11-18):** 7 vídeos con la regla, 57–71 % (media 64 %); antes, 35–64 % (media 52 %). Ninguno llega al 80 % de los de la Luna y TikTok no lo confirma. Se mantiene la regla |
| H8 | Un micro-Short de 6–9 s en bucle (gancho + un dato) consigue más del 100 % de media vista y sirve de anzuelo hacia el vídeo largo | Uno a la semana, sacado de un vídeo ya hecho con `omitir=` (sin gastar voz). Muestra: Luna micro de 8 s | % medio visto, vistas, suscriptores | Preparado; pendiente del «sí» de Nico/Jorge |
| H9 | Los temas que cualquiera reconoce en un segundo superan a los de historia local o detalle erudito | Etiquetar cada vídeo como `alcance: universal` o `nicho` en `etiquetas.json` y comparar cuando haya 5 de cada | Se quedan, vistas a 48 h | **Sin apoyo por ahora.** Me lo sugirieron 15 vídeos mirados, pero al comprobarlo con los 383 títulos no se sostiene: dentro de la misma búsqueda de historia, los títulos «locales» (reyes, batallas, España) tienen mediana 6.500 frente a 1.500 del resto. Se queda como etiqueta para medir, no como regla |
| H5 | Temas de espacio con objeto físico en el primer fotograma superan a «por qué te pasa X» | Comparar por etiqueta `tema` cuando haya 5 de cada | Se quedan | Abierto; hoy 79/73/65 frente a 61/39 |

Cuando un experimento se cierra, se escribe aquí el resultado con fecha y, si cambia cómo hacemos los vídeos, pasa a
`DECISIONS.md`.

---

## Cómo criticar un vídeo propio (antes de enseñarlo)

1. Hoja de fotogramas cada 1,3 s. Para cada miniatura, tres preguntas: **¿qué miro primero?** (tiene que ser lo que
   dice la voz), **¿lo entendería sin sonido?**, **¿se parece demasiado a la anterior?**
2. Primer fotograma a tamaño de móvil (360 px de ancho): ¿se entiende de qué va en medio segundo?
3. `motor.calidad` sin ❌.
4. Lista de los 3 planos más flojos y por qué. Si no sale ninguna lista, es que no se ha mirado bien.
5. Arreglar esos 3 y repetir una vez. Dos vueltas, no infinitas.
