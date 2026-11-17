# Reporte de la noche del 16 al 17 de noviembre de 2026

Encargo de Nico: aprender a hacer mejores vídeos, aprender del nicho y del algoritmo, aplicar lo aprendido por mi
cuenta y contarlo. Cuatro rondas (23:45 → 02:45). No se ha publicado nada ni se ha gastado ningún crédito de voz.

---

## 1. Lo que he aprendido

### De nuestros propios datos (YouTube Studio, dos lecturas: 00:25 y 01:37)

| Vídeo | Se quedan viendo | Vistas | Segundos por vista | Palabras del gancho en el fotograma 0 |
|---|---|---|---|---|
| Huellas en la Luna (48 s) | 80 % | 8.000 | 26,5 | 1 |
| Luna densa (55 s) | 74 % | 2.500 | 28,7 | 3 |
| Luna antigua v4 (retirada) | 65 % | — | — | — |
| Nudillos (58 s) | 60 % | 1.700 | 21,8 | 10 |
| Puertas (55 s) | 47 % | 1.400 | 17,7 | 13 |
| Apolo 11 / móvil (52 s) | 32 % | 533 | 8,1 | 14 |

1. **Cuanto más texto y más cosas quietas hay en el primer fotograma, menos gente se queda.** Es el hallazgo más
   útil: 1 palabra → 80 %, 3 → 74 %, 10 → 60 %, 13 → 47 %, 14 → 32 %. El mejor arranca con una bota cayendo y casi
   sin texto; el peor, con cuatro líneas de texto sobre un móvil lleno de iconos.
2. **El método denso mejoró el gancho del mismo tema:** Luna antigua 65 % → Luna densa 74 %.
3. **Nadie ve más de unos 28 s de media**, dure el vídeo 47 o 58 s.
4. **La primera noche engaña:** YouTube reparte vistas de prueba a todos (Puertas sumó 800 en una hora con un 47 %).
   El porcentaje decide si sigue repartiendo después: Huellas sigue creciendo a las 32 h. Hay que comparar a las 48 h.

Todo esto son **pistas**: son 5–7 vídeos, de temas y edades distintas.

### De 11 Shorts del nicho con hasta 15 M de vistas (mirados fotograma a fotograma, sin sonido)

- **8 de 11 llevan subtítulo de 1–3 palabras enormes, en el centro o tercio inferior.** Ninguno lo lleva pequeño y
  arriba, como nosotros.
- **Duran menos:** de los 7 primeros, cuatro no llegan a 35 s.
- **Un sujeto grande a pantalla completa**, con la acción ya empezada en el fotograma 0.
- **No hay un ritmo de cortes ganador** (de 0 cortes a 2 por segundo). Lo constante es que aparece algo nuevo cada
  1–2 s.
- El único ilustrado como los nuestros (5,2 M) cuenta el dato con **personajes que se asustan y se sorprenden**.

### De 383 títulos del nicho

- **La mediana de vistas es 73.** Solo 7 de 383 pasan del millón. Nuestros 1.000–8.000 ya están muy por encima.
- **El título no explica las vistas.** Ningún rasgo (pregunta, mayúsculas, emoji, número) separa de forma fiable a
  los que triunfan. Cuadra con que el 97 % de nuestras vistas llega por el feed.
- Única pista: las listas genéricas («5 datos curiosos de…») son lo más abundante y lo que peor mediana tiene.

### De la investigación publicada (resumen; detalle en `motor/GUIA_CALIDAD.md`)

- La curiosidad nace de un hueco concreto de información; se mantiene encadenando preguntas.
- Palabra e imagen a la vez, lo importante señalado, nada que distraiga, poco texto repetido.
- Zonas seguras: las guías de anuncios de las tres apps piden dejar libres unos 660 px abajo.

### Lo que no he podido aprender

- **No oigo.** Música, efectos, voz y los empalmes de la versión corta están sin escuchar.
- **YouTube aún no da la curva de retención** de ningún vídeo nuestro («No hay suficientes datos»).
- Los referentes son pocos, de pocos temas, y solo veo a los que triunfaron.

---

## 2. Lo que he mejorado

| Qué | Antes | Ahora |
|---|---|---|
| Render | Un tramo de 12 s tardaba 71 s | El mismo tramo, 32–37 s; el vídeo entero de 55 s, unos 2 min (caché de dibujos + procesos en paralelo) |
| Control de calidad | A ojo, con la hoja de fotogramas | `python3 -m motor.calidad`: nota y avisos (zona segura, lectura, gancho, planos pobres, cortes que no aportan, mismo encuadre, contraste, primer segundo quieto, mezcla) |
| Revisión del guion | Después de pagar la voz | `python3 -m motor.guion` **antes** de la voz |
| Movimiento | Entradas lineales | Muelle, bote, impulso, latido, anillo que señala |
| Sonido | Efectos sueltos | Tensión que sube + impacto en la revelación; música que sigue al montaje y enlaza al repetirse |
| Final | Corte seco | Últimos 0,35 s fundidos con el primer fotograma (bucle) |
| Subtítulos | Solo línea pequeña arriba | Además, modo «palabra» (1–2 palabras enormes) |
| Duración | Solo 55 s | Además, versión corta con la misma locución, sin pagar voz nueva |

Vídeo de la Luna, medido con el control (versión exigente): **publicado 54 → v5 83 → v6 94 → v7 100**.
Fallos que tenía el publicado y que nadie vio a ojo: 15 rótulos donde la app pinta botones, un plano con bordes
negros, tres planos casi vacíos y dos tramos con el mismo encuadre.

---

## 3. Lo que he puesto en práctica por mi cuenta

**Ya es norma para los próximos lotes** (en DECISIONS y en el manual del agente):

1. Ningún vídeo se entrega con ❌ del control de calidad.
2. El guion se revisa antes de generar la voz.
3. Primera frase de **5 palabras o menos** y un solo objeto grande en acción en el fotograma 0.
4. El agente lee `motor/APRENDIZAJE.md` al arrancar y apunta los datos de Studio de los vídeos con más de 24 h.

**Hecho y probado, a falta de vuestro sí** (cambian decisiones vuestras, así que no los he activado):

| Experimento | Qué es | Muestra |
|---|---|---|
| H1 | Subtítulo de 1–2 palabras enormes | `luna-densa_v7_palabra.mp4` |
| H2 | Vídeo de 35 s | `luna-densa_v7_corta35s.mp4` |
| H1 + H2 | Las dos cosas | `luna-densa_v7_corta35s_palabra.mp4` |
| H6 | Personaje que reacciona al dato | **Descartado por Nico** (02:10); quitado del repo |

**Errores míos de esta noche, ya corregidos:**

- El modo «palabra» de la segunda ronda no escribía el archivo de subtítulos ni el manifiesto. Lo encontré al
  renderizar la versión corta.
- La primera versión del control daba 100 a todo: no era exigente. La endurecí dos veces.
- Mi propia v6 tenía el primer segundo casi quieto; lo detectó el control nuevo y rehíce el gancho (v7).
- El personaje (H6) me quedó con aire infantil, que es justo lo que Jorge rechazó el día 15. Lo dejo como muestra,
  no como recomendación.

---

## 4. Lo que os toca decidir

1. **H1, subtítulo de palabra**, en uno de los tres vídeos del próximo lote. Es el primero que probaría: es la
   diferencia más repetida con los referentes y ya está hecho.
2. **H2, un vídeo de 35 s por lote.** Cambia la regla de 150–160 palabras.
3. ~~H6, personaje~~: descartado por Nico.
4. ¿Republicar la Luna con la v7 o usarla solo de modelo?
5. Volumen de la música (ahora unos 10 dB bajo la voz, más alta de lo habitual porque lo pediste) y los efectos
   nuevos: hace falta que alguien lo oiga.

## 5. Próximas lecturas

- **18 de noviembre:** Studio de los tres vídeos de la tarde del 16, ya con 48 h.
- **19 de noviembre:** % medio visto y curva de retención de la Luna densa, para confirmar si retiene mejor.
- Los lotes desde hoy llevan gancho de 5 palabras: en una semana se podrá ver si «se quedan viendo» sube.

## 6. Cuarta ronda (02:10 → 02:45): lo que cambió al seguir investigando

Seguir mirando sirvió sobre todo para **corregirme**. Tres cosas que había dado por buenas no aguantaron la
comprobación, y una salió reforzada.

| Idea | Cómo la comprobé | Resultado |
|---|---|---|
| El subtítulo de palabra ayuda (H1) | Miré también Shorts con ~2.000 vistas | **Rebajada.** Lo llevan casi todos, también los que nadie ve |
| Un vídeo de 35 s rinde más (H2) | Estudio de 5.400 Shorts (Galloway, 2023) + duración de 32 Shorts | **Rebajada.** Los de 50–60 s tenían más vistas; ganadores y perdedores duran lo mismo (59 y 61 s) |
| Los temas «universales» ganan (H9) | 383 títulos, dentro de la misma búsqueda | **Sin apoyo.** Los de historia local no rinden peor |
| El primer segundo en movimiento retiene (H7) | Movimiento del primer segundo en 32 Shorts y en los 7 nuestros | **Reforzada.** Mediana 23,5 en los de más de 100.000 vistas frente a 13,8 en los de 300–3.000 |

Lo nuevo que aprendí:

- **Nuestros arranques son los más tranquilos del nicho.** En la misma escala: Huellas 15,2, Guerra 11,6, Luna
  densa 7,6, Apolo 6,8, Puertas 4,1, Nudillos 2,7, Moáis 1,6. Solo nuestro mejor vídeo supera la mediana de los
  Shorts sin éxito. Es donde más margen hay.
- **Primeras curvas de retención reales (TikTok Studio).** Hasta nuestros dos mejores vídeos pierden el 40 % en
  3 segundos y la mitad antes del segundo 10; después casi nadie se va. En la Luna densa, el mayor escalón
  intermedio cae justo en la cuenta atrás «3, 2, 1» (los planos vacíos que rehíce en la v6) y los dinosaurios son
  el tramo que mejor aguanta.
- **TikTok y YouTube ordenan nuestros vídeos casi igual**, así que las diferencias entre vídeos son reales. La
  Luna densa tiene el mejor tiempo medio del canal en TikTok (22,4 s).
- **Lo oficial del algoritmo:** una vista de Short cuenta en cuanto empieza a reproducirse (desde marzo de 2025),
  así que las vistas incluyen a los que deslizan; borrar y volver a subir se desaconseja; YouTube no publica
  duración ideal, frecuencia mínima ni umbral de retención. Lo de los «lotes de prueba» y las horas mágicas es
  folclore de blogs.
- **Existe el micro-Short:** uno de 5 segundos tiene 1,4 M de vistas. Es otro formato, pensado para repetirse.

Lo que puse en práctica:

- Personaje (H6): **descartado por Nico** y quitado del repo; apuntado en DECISIONS.
- Control de calidad: ❌ si el primer segundo está quieto y ⚠ si se mueve menos que nuestro mejor vídeo.
- Revisión del guion: avisa si la afirmación sorprendente tarda más de 3,5 s en quedar dicha.
- `arranque()` en el motor para que el sujeto del primer plano entre moviéndose.
- Luna **v8**: primer segundo con el doble de movimiento que la v7 (5,5 frente a 3,0 en la escala del control).
- Micro-Short de la Luna de 8 s en bucle (H8), hecho con la misma locución.
- `IDEAS.md`: primera frase y fotograma 0 propuestos para los 5 temas candidatos, y 6 temas nuevos (sin verificar).
- Herramientas guardadas para repetir todo esto: `herramientas/hoja_short.js`, `studio_shorts.js`,
  `tiktok_retencion.js`.

Cómo queda la lista de decisiones después de esta ronda:

1. **Nada que cambiar en la duración:** se quedan los 55 s.
2. Subtítulo de palabra (H1): prueba barata, sin prisa.
3. Micro-Short de 8 s (H8): ¿probamos uno por semana, sacado de un vídeo ya hecho?
4. ¿Republicar la Luna? YouTube lo desaconseja; mejor usar la v8 de modelo.
5. Música y efectos: sigue haciendo falta que alguien los oiga.

## Dónde está todo

- Repo `parecementirapero/parece-mentira`, rama `main`: `motor/APRENDIZAJE.md`, `motor/GUIA_CALIDAD.md`,
  `motor/calidad.py`, `motor/guion.py`, `motor/denso.py`, `herramientas/`, `lotes/prueba-luna-densa/gen.py`,
  `lotes/muestrario-movimiento/`.
- Proyecto de Claude: guía de calidad y cuaderno de aprendizaje.
