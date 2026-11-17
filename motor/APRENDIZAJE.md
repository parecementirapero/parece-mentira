# Aprender a aprender — cuaderno del canal

Cómo mejora el canal de un lote al siguiente sin depender de opiniones. Tres fuentes, de más a menos fiable:

1. **Nuestros datos** (Studio + `estadisticas/`): lo único que dice qué funciona *en este canal*.
2. **Referentes vistos fotograma a fotograma**: qué hacen los Shorts del nicho con millones de vistas.
3. **Investigación publicada** (`motor/GUIA_CALIDAD.md`): por qué podría funcionar.

Regla: una idea sale de 2 o 3, se convierte en **hipótesis**, se prueba cambiando **una sola cosa** en un vídeo del
lote, y solo pasa a `DECISIONS.md` cuando los datos (1) la apoyan. Con menos de 5 vídeos por grupo todo es «pista».

---

## Rutina (qué hace el agente y cuándo)

| Cuándo | Qué | Con qué |
|---|---|---|
| Al arrancar cada lote | Leer `estadisticas/datos/aprendizajes.md` y la tabla de experimentos de abajo | — |
| Al arrancar cada lote | Apuntar «Se quedaron viendo», vistas y horas de los vídeos con 24 h o más | `herramientas/studio_shorts.js` → `estadisticas/studio.json` |
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
6. **El gancho «tu móvil frente al Apolo 11» es el peor hasta ahora (32 %)** y el que menos segundos retiene (8 s).
   A revisar su primer fotograma cuando tenga 24 h.

### El hallazgo más útil de la noche: el primer fotograma de NUESTROS vídeos

Mirados los primeros 5 s de nuestros Shorts publicados (`herramientas/hoja_short.js`) al lado de su «se quedaron
viendo»:

| Vídeo | Se quedan | Palabras del gancho en pantalla | Qué hay en el fotograma 0 |
|---|---|---|---|
| Huellas en la Luna | 80 % | 1 («Esta») | Una bota grande **cayendo** sobre la Luna. Nada más |
| Luna densa | 74 % | 3 («Mira tus uñas.») | Un dedo grande subiendo |
| Nudillos | 60 % | 10 (tres líneas) | Dos manos quietas + dos rótulos |
| Puertas | 47 % | 13 (tres líneas) | Personaje pequeño de pie, quieto, en un pasillo |
| Apolo 11 / móvil | 32 % | 14 (cuatro líneas) | Un móvil con iconos, un fondo lleno de aparatos y un contador |

Con solo 5 vídeos y temas distintos es una **pista**, pero es monótona y coincide con los referentes: cuanto más
texto y más cosas quietas hay en el primer fotograma, menos gente se queda. El «gancho entero en el fotograma 0»
(DECISIONS 2026-11-16) funciona con frases de 3 palabras y se vuelve un muro de texto con frases de 13.

Puesto en práctica: `python3 -m motor.guion guion.txt` revisa el guion **antes de gastar voz** (gancho, duración, cadena de preguntas, tramos sin dato, cifras en letra, palabras solo de España); `motor.calidad` da ❌ si la primera frase pasa de 9 palabras y ⚠ si pasa de 5, y avisa si el
primer segundo del MP4 casi no se mueve; AGENTE §3 pide primera frase de 5 palabras o menos y un solo objeto grande
en acción. El gancho de la Luna v7 se rehízo con eso (el aviso saltó en mi propia v6).

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
   moáis, abajo. → hipótesis H9.
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
| H0 | El método denso retiene mejor que el v4 | Luna densa frente a Luna v4 (mismo tema) | Se quedan: 73,3 % frente a 65,3 % | **A favor (pista).** Revisar % medio visto a las 72 h |
| H1 | Subtítulo de 1–2 palabras, grande y centrado, sube «se quedan» y la retención | `v.construir(..., subtitulos="palabra")` en 1 de 3 vídeos | Se quedan, s por vista | Preparado en el motor. **Rebajado el 2026-11-17:** lo usan casi todos, también los Shorts con 2.000 vistas, así que no hay señal de que ayude; probarlo sigue siendo barato. Pendiente del «sí» de Nico/Jorge |
| H2 | Un vídeo de 30–38 s (95–110 palabras) consigue más % visto y más vistas que uno de 55 s | 1 de 3 vídeos corto, mismo nivel de montaje. Para probar sin gastar voz: `Video(..., omitir=[(i0, i1)])` quita frases enteras de una locución ya hecha | % medio visto, vistas a 48 h | Preparado (Luna v6 corta de 35 s); pendiente: cambia la regla de 150–160 palabras, deciden Nico/Jorge |
| H3 | Gancho en segunda persona («Si mañana…», «Mira tu…») supera al gancho de dato | 1 de 3 vídeos | Se quedan | Pendiente. La Luna («Mira tus uñas») ya apunta a favor |
| H4 | Remate con giro (el último dato rompe el patrón) sube repeticiones y comentarios | 1 de 3 vídeos | % visto > 100 %, comentarios | Pendiente |
| H6 | Un personaje con cara que reacciona al dato retiene más que objetos y cifras solos | — | — | **Descartado por Nico el 2026-11-17** («no me mola lo de poner el personaje») antes de probarlo. El código y la muestra se han quitado del repo. No volver a proponerlo |
| H7 | Gancho de 5 palabras o menos + un solo objeto grande en acción en el fotograma 0 sube «se quedan» por encima del 70 % | Regla ya en AGENTE §3 y en `motor.calidad`; comparar los lotes desde el 2026-11-17 con los anteriores | Se quedan | **En marcha** (es regla desde hoy). Datos previos: 80/74 frente a 60/47/32 |
| H8 | Un micro-Short de 6–9 s en bucle (gancho + un dato) consigue más del 100 % de media vista y sirve de anzuelo hacia el vídeo largo | Uno a la semana, sacado de un vídeo ya hecho con `omitir=` (sin gastar voz). Muestra: Luna micro de 8 s | % medio visto, vistas, suscriptores | Preparado; pendiente del «sí» de Nico/Jorge |
| H9 | Los temas que cualquiera reconoce en un segundo (persona famosa, el cuerpo, la Tierra, animales, el espacio) superan a los de historia local o detalle erudito | Etiquetar cada vídeo como `alcance: universal` o `nicho` en `etiquetas.json` y comparar cuando haya 5 de cada | Se quedan, vistas a 48 h | Abierto. Hoy: Luna y huellas arriba; Zanzíbar y moáis abajo |
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
