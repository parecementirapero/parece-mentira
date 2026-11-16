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

Límites de esta muestra: 7 vídeos, un solo tema, elegidos por el buscador (los que fracasaron haciendo lo mismo no
salen), y sin sonido. Vale para generar hipótesis, no para dar nada por demostrado.

---

## Experimentos

Una hipótesis = un vídeo del lote con ese cambio y los otros dos sin él. Se etiqueta en
`estadisticas/etiquetas.json` → `"experimento": "H1 palabra"`.

| Id | Hipótesis | Cómo se prueba | Se mide con | Estado |
|---|---|---|---|---|
| H0 | El método denso retiene mejor que el v4 | Luna densa frente a Luna v4 (mismo tema) | Se quedan: 73,3 % frente a 65,3 % | **A favor (pista).** Revisar % medio visto a las 72 h |
| H1 | Subtítulo de 1–2 palabras, grande y centrado, sube «se quedan» y la retención | `estilo_subtitulos.modo = "palabra"` en 1 de 3 vídeos | Se quedan, s por vista | Preparado en el motor; pendiente del «sí» de Nico/Jorge |
| H2 | Un vídeo de 30–38 s (95–110 palabras) consigue más % visto y más vistas que uno de 55 s | 1 de 3 vídeos corto, mismo nivel de montaje | % medio visto, vistas a 48 h | Pendiente (cambia la regla de 150–160 palabras: decide Nico/Jorge) |
| H3 | Gancho en segunda persona («Si mañana…», «Mira tu…») supera al gancho de dato | 1 de 3 vídeos | Se quedan | Pendiente. La Luna («Mira tus uñas») ya apunta a favor |
| H4 | Remate con giro (el último dato rompe el patrón) sube repeticiones y comentarios | 1 de 3 vídeos | % visto > 100 %, comentarios | Pendiente |
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
