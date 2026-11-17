# Guía de calidad audiovisual y persuasión — Parece Mentira

Noche del 16 al 17 de noviembre de 2026 (Nico, chat «Luna densa»). Complementa a `motor/DENSO.md` (cómo se monta) con
**por qué** se monta así y **cómo se comprueba**. Todo lo que aquí es una regla está ya en el motor o en
`python3 -m motor.calidad`.

> **Lo que esta guía no es.** No he podido ver ni oír vídeos de otros canales: no tengo oído ni un reproductor, solo
> puedo leer páginas, medir nuestros propios MP4 (fotogramas, niveles de audio) y aplicar investigación publicada.
> Las cifras de «qué es un buen dato» vienen de blogs y herramientas del sector, no de YouTube: YouTube no publica
> umbrales oficiales. Sirven de orientación; lo que manda son **nuestras** estadísticas comparadas entre sí.

---

## 0. Resumen en una pantalla

| Qué | Regla | Dónde se comprueba |
|---|---|---|
| Gancho | Frase de **≤ 5 palabras**, voz desde el segundo 0, **un solo objeto grande ya en acción** en el fotograma 0 (dato propio: `APRENDIZAJE.md`) | `calidad`: gancho y primer segundo |
| Promesa | El gancho abre una pregunta que el vídeo **sí** responde; se cierra al final, no antes | lectura del guion |
| Ritmo | 28–55 cortes/min, duraciones **variadas** (0,3–3 s), micro planos y planos largos mezclados | `calidad`: ritmo |
| Texto | Como mucho una idea por rótulo; tiempo de lectura garantizado; nunca tapado por la app | `calidad`: rótulos |
| Imagen | Lo que se ve es lo que se dice **en ese instante**; lo que se nombra se señala | hoja de fotogramas |
| Movimiento | Nada quieto más de ~1 s; entradas con muelle, caídas con bote, impulsos con anticipación | `calidad --mp4`: movimiento |
| Sonido | Voz manda; efectos audibles ≤ 6 por segundo; whoosh contados; un sonido por acción | `calidad`: sonido y mezcla |
| Música | Sigue al montaje (se recoge en el gancho, aprieta en las ráfagas) y enlaza al repetirse | automático en `denso` |
| Final | Remate + pregunta para comentar + último fotograma que enlaza con el primero | `bucle=0.35` |

Nota del vídeo de la Luna con el control automático (versión exigente, con el MP4): **Luna densa publicada 54 →
v5 83 → v6 94 → v7 100**. La nota mide errores evitables, no si el vídeo gusta: un 100 significa «sin fallos técnicos
conocidos». Cuando todo saca 100 es que al control le falta exigencia: se le añaden comprobaciones (así se pasó de la
primera versión, que daba 100 a la v5, a esta, que le encontró 3 planos pobres y 2 tramos con el mismo encuadre).

**Cómo aprendemos de un lote al siguiente:** `motor/APRENDIZAJE.md` (datos de Studio, Shorts de referencia vistos
fotograma a fotograma, hipótesis y experimentos).

---

## 1. Qué decide que un Short se vea

Un Short pasa dos exámenes seguidos:

1. **¿Se queda o desliza?** YouTube lo enseña como «Vistos frente a deslizados» (Studio → Estadísticas → Contenido →
   Shorts → «Cuántos eligieron ver»). Es el examen del gancho: tema + primer segundo.
2. **¿Cuánto ve?** Porcentaje medio visto y duración media. Es el examen del ritmo y del guion. Si la gente lo ve
   más de una vez, el porcentaje pasa del 100 %: por eso importa el bucle.

Orientación del sector (no oficial): 70–80 % o más de «vistos» y un porcentaje medio visto alto (70–80 % o más) son
buenas señales. YouTube no publica un umbral universal; lo útil es comparar cada vídeo con los nuestros de duración
y tema parecidos.

**Cómo leer un mal dato:**

| Síntoma | Causa probable | Qué tocar |
|---|---|---|
| Muchos deslizan | Tema o primer segundo | Gancho, primer fotograma, primera frase |
| Se quedan pero se van a mitad | Tramo lento o confuso | Ritmo de ese tramo; mirar en qué segundo cae la curva |
| Ven casi todo, pocas repeticiones | Final que «se despide» | Remate más seco + bucle |
| Lo ven pero no comentan | Sin pregunta, o pregunta de sí/no sosa | Pregunta final concreta y fácil de contestar |

**Pendiente para nosotros:** apuntar estos dos datos de cada vídeo en `estadisticas/` a las 48 h y a los 7 días. Sin
eso, cualquier mejora es a ciegas.

---

## 2. Persuasión: por qué alguien se queda

### 2.1 El hueco de información

La curiosidad aparece cuando notamos un hueco entre lo que sabemos y lo que queremos saber (Loewenstein, 1994). Dos
consecuencias prácticas:

- El hueco tiene que **notarse**: no vale «la Luna es interesante»; vale «la Luna se aleja a la velocidad a la que
  te crecen las uñas». El espectador ya sabe algo (las uñas) y de pronto le falta algo (¿cómo que se aleja?).
- Preguntas cuya respuesta es obvia o aburrida no abren hueco.

### 2.2 Bucles abiertos encadenados

Un Short de 55 s no aguanta con una sola pregunta. La estructura que funciona es una cadena: cada respuesta abre la
siguiente pregunta antes de que el espectador se relaje.

Luna densa lo hace así: *se aleja* → ¿cómo lo sabemos? → *espejos y láser* → ¿y por qué se va? → *mareas* → ¿y qué
pasa entonces? → *los días se alargan* → ¿hay pruebas? → *almeja fósil* → ¿y en el futuro? → *adiós eclipses*.

**Regla de guion:** cada 8–12 s tiene que haber una pregunta nueva, dicha o implícita. Si un tramo solo «explica»,
se corta o se convierte en respuesta a una pregunta.

### 2.3 La línea con el clickbait

La promesa del gancho se cumple dentro del vídeo y con datos verificados. Prometer de más da el clic y pierde la
confianza (y la retención, que es lo que mide la app). Esto ya es regla del canal: fuentes comprobadas antes de
grabar.

### 2.4 Tipos de gancho que encajan con el canal

| Tipo | Ejemplo | Cuándo |
|---|---|---|
| Comparación con algo cotidiano | «Mira tus uñas. La Luna se aleja a esa velocidad.» | Cifras difíciles de imaginar |
| Negación de algo que se da por hecho | «Los vikingos no llevaban cuernos.» | Mitos |
| Consecuencia sorprendente primero | «Un día dejará de haber eclipses totales.» | Ciencia con final fuerte |
| Pregunta concreta | «¿Por qué el día duraba 18 horas?» | Cuando la respuesta no es obvia |
| Objeto extraño | «Esta almeja es un calendario.» | Historia y arqueología |

Ver también el doc del Proyecto `claude/analisis-reels-virales-2026-11-16.md` (gancho legible en el fotograma 0,
negación, pregunta de cierre).

### 2.5 Estructuras de vídeo

| Estructura | Forma | Ejemplo de tema |
|---|---|---|
| **Cadena de porqués** (la de la Luna) | dato → ¿cómo se sabe? → ¿por qué? → consecuencia → futuro | Ciencia |
| **Mito y realidad** | «todos creen X» → prueba → lo que pasó de verdad → por qué nació el mito | Historia |
| **Cuenta atrás** | 3 datos de menos a más increíble | Curiosidades sueltas de un mismo tema |
| **Misterio** | hecho raro → hipótesis 1 (falla) → hipótesis 2 (falla) → lo que se sabe hoy | Misterios (sin inventar la solución) |
| **Viaje en el tiempo** | hoy → hace 100 años → hace 1.000 → hace 1 millón | Cambios lentos |
| **Escala** | objeto cotidiano → zoom hacia fuera o hacia dentro | Tamaños, distancias |

Conviene alternarlas dentro del lote para que el canal no parezca siempre el mismo vídeo.

---

## 3. Que se entienda: imagen y palabra

Los principios de Mayer sobre aprendizaje multimedia son lo más sólido que hay publicado sobre cómo combinar voz,
imagen y texto. Los que nos afectan:

| Principio | Qué dice | Cómo lo aplicamos |
|---|---|---|
| **Contigüidad temporal** | Palabra e imagen correspondientes, a la vez | Planos atados a la palabra exacta (`v.w(i)`), no a tiempos a ojo |
| **Señalización** | Marcar lo importante ayuda | `senala()`, `late()`, flechas, palabra clave resaltada en el subtítulo |
| **Coherencia** | Sobra todo lo que no ayuda | Los detalles de fondo (satélites, fugaces) van bajos, lentos y lejos del sujeto |
| **Redundancia** | Con ritmo rápido, narración + gráficos + mucho texto repetido empeora | El rótulo es **una** palabra o cifra, no la frase entera |
| **Contigüidad espacial** | El texto, cerca de lo que nombra | Rótulo junto al objeto, no en una esquina fija |

**Tensión real con los subtítulos.** El principio de redundancia dice que repetir en pantalla todo lo que se oye
puede estorbar; pero mucha gente ve los vídeos sin sonido y los subtítulos suben el tiempo de visionado (los
estudios que se citan son de Facebook y de Verizon/Publicis sobre anuncios, no sobre Shorts, así que el número
exacto no es trasladable). Nuestra solución es un punto medio: subtítulo **karaoke corto** (pocas palabras a la vez,
arriba, siempre en el mismo sitio) y rótulos que **no repiten** la frase, solo fijan el dato.

**Coherencia frente a «más cosas por fotograma».** Más elementos no es mejor si compiten con el sujeto. La regla
que seguimos: un sujeto por plano, en el centro de atención; todo lo demás es ambiente (más pequeño, más lento, menos
contraste, menos sonido).

---

## 4. Escenas

### 4.1 Tipos de plano y para qué sirve cada uno

| Tipo | Duración | Para qué |
|---|---|---|
| **Gancho** | 1–1,5 s | Sujeto ya en pantalla, texto del gancho legible, movimiento desde el fotograma 0 |
| **Dato** | 1–2 s | Una cifra que corre o una palabra clave. Necesita tiempo de lectura |
| **Explicación** (plano largo) | 2–3 s | Un proceso que se ve ocurrir (órbita que crece, marea que sube) |
| **Micro plano** | 0,3–0,7 s | Detalle que enriquece: la huella, el láser que se carga, el cronómetro. Sin texto |
| **Pregunta** | 0,8–1,3 s | Cambia de tramo: «¿CÓMO?», «¿POR QUÉ?» |
| **Respiro** | 1,5–2,5 s | Después de una ráfaga, un plano amplio y tranquilo |
| **Remate** | 2–3 s | La consecuencia final + llamada a comentar |

### 4.2 Ritmo

- Las duraciones tienen que **variar**: ráfaga de micro planos → plano largo → dato. El control de calidad mide la
  variación (desviación/media ≥ 0,45).
- Una ráfaga de 3 micro planos seguidos funciona como un redoble antes de un dato fuerte (cuenta atrás 3‑2‑1 antes
  del despegue).
- Tiempo de lectura de cualquier texto: 0,25 s + 1 s por cada 17 letras. Si no cabe, se acorta el texto, no se
  acelera la voz.
- Cada plano largo necesita **dos** cosas que pasen dentro (por ejemplo: la órbita crece y después aparece la
  palabra), para que no parezca parado.

### 4.3 Escenas secundarias (detalles de fondo)

- Duran: cruzan varios planos seguidos con un recorrido continuo (`recorrido()` con tiempo absoluto), no aparecen y
  desaparecen.
- No se llevan el ojo: pequeños, lentos, en la periferia, con su sonido muy bajo (−26 dB o menos) y como mucho cada
  2,5 s.
- Cuentan una mini historia propia cuando se puede: el meteorito que se va acercando durante todos los planos de
  dinosaurios y cae en el último.

### 4.4 Composición y zonas seguras

Las apps pintan botones y textos encima del vídeo. Las guías no coinciden entre sí:

| Fuente | Arriba | Abajo | Derecha |
|---|---|---|---|
| Guías de anuncios (las más estrictas): TikTok / Reels / Shorts | 240–288 px | 660–672 px | 120–192 px |
| Guías «de creador» (feed normal) | 108–220 px | 250–480 px | 120–180 px |
| «Zona común» que proponen varias guías | 900 × 1400 px centrada | | |

Lo que hace el motor:

- **Límite duro** (el motor recoloca solo y `calidad` marca ❌): texto entre y = 240 y y = 1400, y nada a la derecha
  de x = 900 por debajo de y = 800.
- **Franja dudosa** (aviso ℹ): entre y = 1250 y y = 1400. Se ve en el feed normal, pero si el texto es esencial es
  mejor subirlo.
- Cuando el motor sube un rótulo, puede pisar al sujeto: hay que mirarlo en la hoja de fotogramas y colocarlo a mano
  (en la Luna v5: ESPEJOS al cielo, LÁSER a la izquierda del rayo, ¿POR QUÉ? junto a la Luna).
- Cámara con zoom menor que 1 deja bordes negros: prohibido (`calidad` lo marca ❌). El vídeo publicado tenía uno.

**Decisión pendiente de Nico y Jorge:** si bajamos el límite duro de 1400 a 1250 para todo texto esencial.

---

## 5. Movimiento

Los 12 principios clásicos de la animación explican por qué un movimiento parece vivo o parece PowerPoint. Los que
más rinden en gráficos animados, y cómo están en el motor (`motor/denso.py`, `motor/core.py`):

| Principio | Qué es | En el motor |
|---|---|---|
| Aceleración y frenada | Nada arranca ni para de golpe | easings `suave`, `entrada`, `salida`, `expo` |
| Anticipación | Tomar impulso hacia atrás antes de salir | `lanza()`, easing `anticipa` |
| Acción continuada | Pasarse un poco y volver | `aparece()`, easing `elastico` |
| Estirar y aplastar | Se estira al caer y se aplasta al aterrizar | `cae()`, easing `bote` |
| Acción solapada | Las piezas de detrás llegan un poco después | `sigue(keys, retraso)` |
| Acción secundaria | Algo pequeño acompaña a la acción principal | polvo, chispas, trocitos de hoja |
| Puesta en escena | Que se vea de un vistazo qué es lo importante | `senala()`, `late()`, viñeta |

Reglas:

- Lineal solo para lo mecánico (agujas de reloj, satélites). Todo lo demás, con curva.
- Entradas rápidas (0,2–0,4 s) y con un poco de exceso; salidas más rápidas todavía.
- La cámara siempre se mueve un poco (zoom 1,00 → 1,05), pero el movimiento de cámara nunca sustituye a que pase
  algo en el plano.
- Un movimiento, un sonido (ver §6).

---

## 6. Sonido

### 6.1 Jerarquía

La voz manda. Referencias habituales de mezcla para vídeo con narración: música entre 18 y 25 dB por debajo de la
voz mientras se habla, efectos algo más altos, y bajar la música automáticamente cuando entra la voz («ducking»).

**Dónde estamos nosotros:** la música queda unos **10 dB** por debajo de la voz (medido en el MP4), más alta que esa
referencia. Es una decisión consciente: Nico pidió que se oyera más la música y menos los «shhh». La voz se sigue
entendiendo porque la música generada no tiene melodía en la zona de la voz y los efectos se atenúan solos cuando
coinciden con ella. Si alguien comenta que no se entiende, lo primero que hay que tocar es `musica.db` (de −13 a
−16).

### 6.2 Efectos

- **Un sonido por acción visible**, sincronizado al fotograma. Sonido sin imagen que lo justifique, fuera.
- **Capas por volumen:** remates (−8 a −12 dB, uno o dos por vídeo), acciones (−14 a −18), textura (−22 o menos:
  rayas de flecha, tics, satélites).
- **No más de 6 efectos audibles en un mismo segundo** (`calidad` avisa). La textura no cuenta.
- **Whoosh contados:** como mucho uno cada 5 s y bajo. Para cambios de plano discretos existe `roce`.
- **Tensión y descarga:** `subida` (1–1,5 s que crecen y se cortan en seco) justo antes de la revelación, `impacto`
  en la revelación. Usado una o dos veces por vídeo; más, cansa. En la Luna v5: antes del meteorito.
- **Silencio:** medio segundo casi sin efectos antes del dato fuerte hace que el dato pegue más.

Catálogo actual (`motor/sfx.py`): whoosh, roce, pop, tic, tictac, golpe, impacto, subida, zap, brillo, ding, rumor,
ola, agua, burbuja, senal, fugaz, trazo, mordisco, meteoro.

### 6.3 Música

- Se genera sola y **sigue al montaje**: baja en el gancho (para que la primera frase se oiga limpia) y en los
  planos largos, sube donde hay ráfagas de cortes. Se puede forzar por plano con `P(..., energia=0.9)`.
- Acaba en el acorde que resuelve en el primero: si el Short se repite, la música enlaza.
- Límite honesto: es música sintetizada sencilla. Una pista con licencia elegida por una persona sonará mejor; el
  motor la admite (`musica={"archivo": ...}`), pero elegirla requiere oído y revisar la licencia.

---

## 7. Final y bucle

- La última frase es la consecuencia, no un resumen ni una despedida.
- Pregunta final concreta y fácil («¿Has visto alguna vez un eclipse total?»), también como comentario fijado.
- **Bucle:** `v.construir(..., bucle=0.35)` funde los últimos 0,35 s con el primer fotograma. Al repetirse, no hay
  salto. Mejor todavía si la última frase deja la primera a punto («…no te lo pierdas.» → «Mira tus uñas.»).

---

## 8. Python y rendimiento

Hecho esta noche:

- **Caché en disco de los SVG** (`.raster/` junto a cada SVG, ignorado en git) y render en paralelo
  (`--procesos N`). El cuello de botella era rasterizar cada fondo en cada ejecución (~1 s por SVG con textura).
  Un tramo de 12 s pasó de 71 s a 32–37 s; el vídeo entero de 55 s se renderiza en unos 2 min.
- Easings nuevos: `elastico`, `bote`, `anticipa`, `golpe`, `expo`.
- Efectos nuevos: `subida`, `impacto`, `roce`, `burbuja`.
- Música con curva de energía y final que enlaza.
- Control de calidad automático (`motor/calidad.py`).

Qué **no** conviene cambiar (valorado y descartado):

| Opción | Por qué no ahora |
|---|---|
| Pasar a Manim, MoviePy o Remotion | El motor ya hace lo que necesitamos y lo controlamos entero; migrar es rehacer la biblioteca de ilustraciones |
| Post‑proceso de acabado (color, brillo) | Probado el día 16: a Nico le gustaba más sin él (DECISIONS) |
| Vídeo generado por IA | Coste por vídeo y resultados no reproducibles; choca con «montaje reproducible en Python» |

Qué sí podría merecer la pena más adelante (sin coste):

- **Skia (`skia-python`) o Cairo** para dibujar formas y texto con mejor suavizado y más rápido que Pillow.
- **Desenfoque de movimiento** en los objetos rápidos (promediar 2–3 subfotogramas solo en esos planos).
- **Partículas con física sencilla** (gravedad y rozamiento) para polvo, chispas y agua.
- **Ilustraciones:** el mayor salto visual que queda está en los dibujos, no en el código. Más figuras detalladas
  por tema (como los dinosaurios) rinde más que cualquier librería.

---

## 9. Lista de control antes de publicar

1. `python3 gen.py DIR voz.mp3 alineacion.json` → sin avisos de lectura.
2. `python3 -m motor.render DIR/episodio.json --salida DIR/out --hoja --cada 1.3` → mirar la hoja: ¿algún rótulo
   pisa al sujeto?, ¿algún plano vacío?
3. `python3 -m motor.render DIR/episodio.json --salida DIR/out`
4. `python3 -m motor.calidad DIR/episodio.json --mp4 DIR/out/<id>.mp4 --md DIR/calidad.md` → **ningún ❌**; los ⚠
   se arreglan o se justifican en `estado.md`.
5. Revisión humana en el chat: una persona lo ve **con sonido** y otra vez **sin sonido**. El control automático no
   sabe si el vídeo aburre ni si la música molesta.
6. Publicar solo con el «ok» de ese lote.

---

## 9b. Qué mira el control con el MP4 (además del montaje)

| Comprobación | Cómo | Aviso |
|---|---|---|
| Planos pobres | Cantidad de dibujo (bordes) en el fotograma central de cada plano | ⚠ si es un fondo liso con un objeto pequeño |
| Planos calcados | Parecido entre el fotograma central de un plano y el del siguiente | ⚠ si el corte no trae nada nuevo |
| Mismo encuadre demasiado tiempo | Varios planos seguidos parecidos durante más de 4,5 s | ⚠ cambia de escala o de punto de vista |
| Contraste de rótulos sin cápsula | Color del texto frente a los píxeles que tiene debajo en el MP4 | ⚠ por debajo de 3:1 |
| Tramos quietos | Diferencia entre fotogramas a 10 por segundo | ⚠ más de 0,8 s sin que se mueva nada |
| Bucle | Primer fotograma frente al último | ℹ si no enlaza |
| Mezcla | Música y efectos frente a la voz, en ventanas de 0,25 s | ⚠ si tapan la voz |

Lo que el control **no** ve: si un rótulo tapa justo la parte importante del sujeto, si el vídeo aburre, si un
chiste funciona, cómo suena. Eso sigue siendo la hoja de fotogramas y una persona con sonido.

---

## 10. Qué queda por decidir o probar

0. **Subtítulo «palabra» (H1) y vídeo corto (H2).** Son las dos diferencias más claras entre nuestros vídeos y
   los 7 Shorts de referencia mirados (`motor/APRENDIZAJE.md`). El modo palabra ya está en el motor
   (`v.construir(..., subtitulos="palabra")`) y hay una Luna v6 de muestra con él. El vídeo corto cambia la regla
   de 150–160 palabras: lo deciden Nico y Jorge.
1. **Medir.** Primera lectura hecha el 2026-11-17 00:25 (`motor/APRENDIZAJE.md`): la Luna densa retiene al 73,3 %
   en el primer segundo frente al 65,3 % del v4 antiguo. Falta el % medio visto a las 72 h.
2. **Prueba A/B barata:** mismo vídeo, dos ganchos distintos, en días distintos (o uno en TikTok y otro en Shorts).
3. Límite inferior de texto: ¿1400 o 1250? (§4.4)
4. Volumen de la música: ¿se queda en −13 dB? (§6.1). Hace falta oído humano.
5. ¿Republicar la Luna con la v5? El vídeo publicado tiene 17 rótulos en la zona que tapa la app y un plano con
   bordes negros. Republicar gasta la excepción de «tema repetido» otra vez; quizá mejor aplicar la v5 solo a lo
   nuevo.

---

## Fuentes

Métricas de Shorts
- [YouTube Ayuda — Understand your YouTube content performance](https://support.google.com/youtube/answer/12220281)
- [Social Media Examiner — How to analyze your YouTube Shorts](https://www.socialmediaexaminer.com/how-to-analyze-your-youtube-shorts/)
- [Buffer — The Creator's Guide to YouTube Shorts Analytics](https://buffer.com/resources/the-creators-guide-to-youtube-shorts-analytics)
- [Subscribr — YouTube Shorts Analytics: what metrics matter](https://subscribr.ai/youtube-strategy/youtube-shorts-analytics-metrics-growth) (cifra orientativa 75–80 %)
- [Vaizle — análisis de Paddy Galloway sobre 3.300 millones de Shorts](https://insights.vaizle.com/?p=3156) (70–90 %)
- [Creator Essentials — Swiped Away](https://www.creatoressentials.com/glossary/swiped-away/) (no hay umbral oficial)

Curiosidad y gancho
- Loewenstein, G. (1994). *The psychology of curiosity: A review and reinterpretation.* Psychological Bulletin, 116(1), 75–98. Resumen en [Learning Loop — Curiosity effect](https://learningloop.io/plays/psychology/curiosity-effect)
- [HubSpot — psychology‑backed hacks for engaging videos](https://blog.hubspot.com/marketing/psychology-hacks-for-making-engaging-videos) (Wojtowicz y Loewenstein, «Curiosity and the Economics of Attention»)
- [SocialRails — Curiosity gap vs clickbait](https://socialrails.com/blog/curiosity-gap-guide)

Imagen y palabra
- [Mayer (2020), Multimedia Principles (resumen en PDF)](https://ugc.futurelearn.com/uploads/files/7d/d6/7dd6188d-c343-4311-b064-ac98d2c95abc/Multimedia_Principles._R._E._Mayer__2020.pdf)
- [Mayer (2017), Using multimedia for e‑learning — tamaños de efecto](https://zendy.io/title/10.1111/jcal.12197)
- [Cambridge Handbook of Multimedia Learning, cap. 12](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/CD5B7AE1279A9AB81F8EEBB53DBEC86E)
- [Dartmouth — Mayer's 12 Principles](https://services.dartmouth.edu/TDClient/1806/Portal/KB/PrintArticle?ID=171655)

Subtítulos
- [3Play Media — Studies find captions improve engagement](https://3playmedia.com/blog/studies-find-captions-improve-engagement)
- [Kapwing — Subtitle statistics](https://kapwing.com/resources/subtitle-statistics)

Zonas seguras
- [Upload‑Post — Safe zone checker (px por plataforma)](https://www.upload-post.com/tools/safe-zone-checker/)
- [bundle.social — Safe zone checker (cita la guía de anuncios de Meta)](https://bundle.social/tools/safe-zone-checker)
- [AdaptlyPost — Social media safe zones 2026](https://adaptlypost.com/blog/social-media-safe-zones-2026-complete-guide)
- [AdMake — Vertical video dimensions 2026](https://www.admakeai.com/blog/vertical-video-dimensions-2026)

Sonido
- [Overseer — How loud should background music be under a voiceover](https://www.overseeros.com/blog/background-music-volume-under-voiceover)
- [Adorama — Mastering audio levels](https://www.adorama.com/alc/?p=118366)
- [Pixflow — Mixing dialogue, music and sound effects](https://pixflow.net/blog/audio-mixing-premiere-pro/)
- [CapCut — Audio ducking for clear dialogue](https://www.capcut.com/create/audio-ducking-for-clear-dialogue-in-video)

Animación
- Thomas, F. y Johnston, O. (1981). *The Illusion of Life: Disney Animation* (los 12 principios). De conocimiento
  general; esta noche no lo he vuelto a contrastar con una fuente enlazable.
