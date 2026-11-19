# Estudio de audiencia y rendimiento — 2026-11-19 10:04

Generado por `python3 estadisticas/estudio todo`. Método: `estadisticas/estudio/README.md`. Niveles: **pista** (menos de 5 vídeos por grupo o indistinguible del azar: solo para decidir qué probar), **indicio** (5 o más por grupo, p < 0,10 y mismo sentido en YouTube y TikTok), **regla** (10 o más por grupo, intervalo que no cruza el cero, repetido en dos semanas y p corregido por el número de comparaciones; o un experimento con ficha previa cerrado a favor).

## 1. Con qué contamos

- Vídeos públicos: **19** · con ficha de variables: **16** (codificadas antes de publicar: 6).
- Con «se quedaron viendo» leído a edad comparable (24 h o más): **10** (de ellos, ya con la medición de 48 h: 4).
- Con retención de TikTok Studio a edad comparable: **7**.

«Se quedaron viendo» varía con una desviación típica de **14,1 puntos** (10 vídeos). Con esa variación, para detectar una diferencia hacen falta:

| Diferencia | Vídeos por grupo |
|---|---|
| 20 puntos | 8 |
| 15 puntos | 14 |
| 10 puntos | 32 |
| 5 puntos | 125 |

_Aproximación normal, 80 % de potencia y 5 % de error; con tan pocos vídeos la desviación misma es incierta._

## 2. Vídeos

Valor a 48 h; si el vídeo aún no llega, la última lectura con 24 h o más (marcada con ~). Entre paréntesis, el índice frente a la mediana del canal (1,3 = 30 % mejor). Sin valor = todavía no hay lectura con 24 h.

| Vídeo | Se quedan (YT) | s por vista (YT) | Tiempo medio (TT) | Siguen a 3 s (TT) | Vistas YT | Vistas TT |
|---|---|---|---|---|---|---|
| Huellas en la Luna | ~79,4 (1,24) | ~26,5 (1,12) | ~19,8 (1,37) | ~63,0 (1,21) | 11.122 (7,18) | 618 (2,40) |
| Guerra de 38 minutos | 60,1 (0,94) | 17,7 (0,75) | ~16,5 (1,15) | — | 1.428 (0,92) | 426 (1,65) |
| Moáis | 52,0 (0,81) | 16,8 (0,71) | ~13,7 (0,95) | ~41,0 (0,79) | 1.220 (0,79) | 409 (1,59) |
| Luna densa | 80,3 (1,25) | 29,4 (1,24) | 22,4 (1,56) | _60,0 a las 5 h_ | 6.462 (4,17) | 285 (1,10) |
| Nudillos | 63,5 (0,99) | 23,6 (0,99) | _20,7 a las 4 h_ | — | 2.194 (1,42) | 275 (1,07) |
| Puertas | ~47,7 (0,74) | ~19,8 (0,83) | _9,2 a las 4 h_ | — | 1.405 (0,91) | 240 (0,93) |
| Apolo 11 / móvil | ~35,2 (0,55) | ~11,5 (0,48) | — | — | 1.114 (0,72) | 5 (0,02) |
| Plátano radiactivo | ~64,8 (1,01) | ~23,9 (1,01) | ~12,2 (0,85) | — | 1.491 (0,96) | ~241 (0,93) |
| Saturno flotaría | ~67,4 (1,05) | ~26,7 (1,12) | ~14,4 (1,00) | — | ~2.239 (1,45) | ~231 (0,90) |
| Huella de koala | ~71,3 (1,11) | ~24,9 (1,05) | ~6,4 (0,45) | — | ~2.300 (1,48) | ~56 (0,22) |
| cjSc0D_gOaI | — | — | — | — | _0 a las 10 h_ | — |
| dOdQj9QyoBI | _56,9 a las 24 h_ | _18,0 a las 24 h_ | — | — | ~1.607 (1,04) | _366 a las 18 h_ |
| 5pSKNws_e-s | _64,3 a las 14 h_ | _21,6 a las 14 h_ | — | — | ~611 (0,39) | _247 a las 16 h_ |
| rEiiPtGXz84 | _41,7 a las 13 h_ | — | — | — | _9 a las 24 h_ | _241 a las 16 h_ |
| tp7XFLAIkS0 | _54,6 a las 12 h_ | — | — | — | _8 a las 23 h_ | _217 a las 16 h_ |
| dMcGHyKbeaA | _60,8 a las 8 h_ | _17,0 a las 8 h_ | — | — | _1.246 a las 19 h_ | _288 a las 18 h_ |
| G_xEqU97krk | _65,2 a las 7 h_ | _21,2 a las 7 h_ | — | — | _605 a las 18 h_ | — |
| _9znalXgInI | — | — | — | — | _948 a las 9 h_ | _2 a las 9 h_ |
| 7709510485921582358 | — | — | — | — | — | _267 a las 18 h_ |

_En cursiva: lecturas con menos de 24 h. No entran en ningún cálculo._

## 3. Qué acompaña a mejores resultados

Cada fila compara los vídeos que tienen ese valor con todos los demás. «p» es la probabilidad de ver esa diferencia por puro azar; con grupos pequeños no puede bajar de cierto mínimo (3 contra 3: 0,10), así que un p alto con pocos vídeos no significa «no hay efecto».

| Variable | Métrica | Vídeos (con / resto) | Mediana (con / resto) | Diferencia | Intervalo al 90 % | p | ¿Igual en la otra red? | Nivel |
|---|---|---|---|---|---|---|---|---|
| `tema` = Histórico | se quedaron viendo (YouTube) | 2 / 8 | 47,7 / 66,1 | −18,4 | no calculable (menos de 3 por grupo) | 0,18 | sin datos | **pista** |
| `gancho_persona` = impersonal | se quedaron viendo (YouTube) | 6 / 4 | 66,1 / 49,9 | +16,2 | -9,0 a 29,8 | 0,26 | sí | **pista** |
| `tema` = Espacio | se quedaron viendo (YouTube) | 2 / 8 | 73,4 / 61,8 | +11,6 | no calculable (menos de 3 por grupo) | 0,27 | sí | **pista** |
| `tema` = Ciencia | se quedaron viendo (YouTube) | 2 / 8 | 72,5 / 61,8 | +10,8 | no calculable (menos de 3 por grupo) | 0,27 | sin datos | **pista** |
| `tema` = Cotidiano | se quedaron viendo (YouTube) | 2 / 8 | 55,6 / 66,1 | −10,5 | no calculable (menos de 3 por grupo) | 0,40 | sin datos | **pista** |
| `f0_sujeto` = objeto | se quedaron viendo (YouTube) | 8 / 2 | 66,1 / 55,6 | +10,5 | no calculable (menos de 3 por grupo) | 0,40 | sin datos | **pista** |
| `remate` = pregunta | se quedaron viendo (YouTube) | 4 / 6 | 66,1 / 56,0 | +10,0 | -13,3 a 21,6 | 0,48 | sin datos | **pista** |
| `montaje` = v4 | se quedaron viendo (YouTube) | 2 / 8 | 56,0 / 66,1 | −10,0 | no calculable (menos de 3 por grupo) | 0,40 | sí | **pista** |
| `tema` = Histórico | segundos por vista (YouTube) | 2 / 8 | 14,6 / 24,4 | −9,8 | no calculable (menos de 3 por grupo) | 0,09 | no | **pista** |
| `epoca` = sin época | se quedaron viendo (YouTube) | 3 / 7 | 67,4 / 60,1 | +7,3 | -3,9 a 28,3 | 0,18 | sin datos | **pista** |
| `montaje` = v4 | segundos por vista (YouTube) | 2 / 8 | 17,2 / 24,4 | −7,1 | no calculable (menos de 3 por grupo) | 0,18 | no | **pista** |
| `epoca` = sin época | segundos por vista (YouTube) | 3 / 7 | 26,7 / 19,8 | +6,9 | 0,3 a 11,7 | 0,07 | no | **pista** |
| `epoca` = siglo XX | se quedaron viendo (YouTube) | 2 / 8 | 57,3 / 64,2 | −6,9 | no calculable (menos de 3 por grupo) | 0,89 | no | **pista** |
| `gancho` = contraste | segundos por vista (YouTube) | 3 / 7 | 17,7 / 23,9 | −6,2 | -13,4 a 2,9 | 0,38 | no | **pista** |
| `remate` = dato | segundos por vista (YouTube) | 3 / 7 | 17,7 / 23,9 | −6,2 | -9,0 a 2,9 | 0,52 | no | **pista** |
| `montaje` = denso | segundos por vista (YouTube) | 7 / 3 | 23,9 / 17,7 | +6,2 | -2,9 a 9,0 | 0,52 | no | **pista** |
| `voz` = clon | segundos por vista (YouTube) | 7 / 3 | 23,9 / 17,7 | +6,2 | -2,9 a 9,0 | 0,52 | no | **pista** |
| `dia_semana` = domingo | segundos por vista (YouTube) | 3 / 7 | 17,7 / 23,9 | −6,2 | -9,0 a 2,9 | 0,52 | no | **pista** |
| `gancho_persona` = impersonal | segundos por vista (YouTube) | 6 / 4 | 24,4 / 18,3 | +6,1 | -3,8 a 12,2 | 0,35 | no | **pista** |
| `remate` = pregunta | segundos por vista (YouTube) | 4 / 6 | 24,4 / 18,8 | +5,6 | -2,2 a 9,4 | 0,35 | no | **pista** |
| `tema` = Ciencia | segundos por vista (YouTube) | 2 / 8 | 26,6 / 21,7 | +4,9 | no calculable (menos de 3 por grupo) | 0,27 | sí | **pista** |
| `tema` = Espacio | segundos por vista (YouTube) | 2 / 8 | 26,6 / 21,7 | +4,9 | no calculable (menos de 3 por grupo) | 0,18 | sí | **pista** |
| `epoca` = siglo XX | segundos por vista (YouTube) | 2 / 8 | 19,0 / 23,8 | −4,8 | no calculable (menos de 3 por grupo) | 0,71 | no | **pista** |
| `gancho` = contraste | se quedaron viendo (YouTube) | 3 / 7 | 60,1 / 64,8 | −4,7 | -32,2 a 15,9 | 0,67 | no | **pista** |

**Ninguna comparación pasa de «pista».** Las de arriba son las de mayor diferencia y sirven solo para elegir qué experimento hacer.

⚠ Se han mirado 92 comparaciones a la vez: por azar, alrededor de 1 de cada 20 parecerá «significativa». Por eso aquí una «regla» exige un p repartido entre todas ellas; un experimento con ficha previa (`estadisticas/experimentos/`) mira una sola y llega antes.

### Variables numéricas

| Variable | Métrica | Vídeos | Correlación (Spearman) | p | ¿Igual en la otra red? | Nivel |
|---|---|---|---|---|---|---|
| `palabras` | segundos por vista (YouTube) | 10 | 0,84 | 0,00 | no | **pista** |
| `gancho_palabras` | segundos por vista (YouTube) | 10 | -0,81 | 0,01 | sí | **pista** |
| `palabras` | se quedaron viendo (YouTube) | 10 | 0,78 | 0,01 | sin datos | **pista** |
| `gancho_palabras` | se quedaron viendo (YouTube) | 10 | -0,70 | 0,02 | sin datos | **pista** |
| `preguntas` | segundos por vista (YouTube) | 10 | 0,61 | 0,06 | no | **pista** |
| `preguntas` | se quedaron viendo (YouTube) | 10 | 0,44 | 0,20 | sin datos | **pista** |
| `f0_palabras` | se quedaron viendo (YouTube) | 10 | -0,43 | 0,21 | sin datos | **pista** |
| `f0_mov_hoja` | se quedaron viendo (YouTube) | 7 | 0,43 | 0,36 | sin datos | **pista** |
| `duracion_s` | segundos por vista (YouTube) | 10 | 0,41 | 0,23 | no | **pista** |
| `f0_mov_hoja` | segundos por vista (YouTube) | 7 | 0,39 | 0,41 | sí | **pista** |
| `duracion_s` | se quedaron viendo (YouTube) | 10 | 0,31 | 0,38 | sin datos | **pista** |
| `hora` | segundos por vista (YouTube) | 10 | -0,23 | 0,54 | no | **pista** |
| `f0_palabras` | segundos por vista (YouTube) | 10 | -0,20 | 0,56 | sí | **pista** |
| `hora` | se quedaron viendo (YouTube) | 10 | -0,19 | 0,61 | sin datos | **pista** |

_Una correlación no dice qué causa qué. Sin experimento, nunca pasa de «indicio»._

## 4. Lo que esta muestra NO puede decir

- **Variables que no varían** (todos los vídeos valen lo mismo, así que no se puede saber si importan): `subtitulo` = karaoke.
- **Variables pegadas** (en estos vídeos van siempre juntas; un efecto de una puede ser de la otra): `alcance` y `f0_literal`.
- **10 fichas se codificaron después de publicar**, sabiendo ya el resultado. Las variables subjetivas de esas fichas pueden estar contaminadas.
- Retención por edad o por género: ninguna plataforma la da.

## 5. Quién nos ve (YouTube, canal)

Desde 2026-11-01. Solo usuarios con sesión iniciada; edad y género los estima YouTube.

| Edad | % | Mujeres | Hombres |
|---|---|---|---|
| 13–17 | 7,0 | 1,9 | 5,1 |
| 18–24 | 12,4 | 2,6 | 9,8 |
| 25–34 | 32,9 | 11,4 | 21,5 |
| 35–44 | 25,4 | 11,6 | 13,8 |
| 45–54 | 13,6 | 5,2 | 8,4 |
| 55–64 | 5,1 | 1,7 | 3,4 |
| 65+ | 3,6 | 1,4 | 2,2 |

- Hombres 64,2 % · mujeres 35,8 %.
- España 24,6 % · Latinoamérica 72,4 % de las 25.618 vistas con país.
- Por país (% de vistas · segundos por vista): México 28,9 % · 24,9 s · España 24,6 % · 17,4 s · Argentina 12,0 % · 20,1 s · Colombia 8,9 % · 21,5 s · Perú 7,5 % · 21,4 s · Chile 5,9 % · 19,7 s · Venezuela 4,4 % · 20,7 s · Estados Unidos 3,0 % · 19,6 s.

**Público objetivo (propuesta de Claude, sin confirmar por Nico y Jorge)**: edades 18–24, 25–34; países España, México, Argentina, Colombia.
- Hoy el **45,3 %** de la audiencia está en esas edades y el **74,4 %** de las vistas viene de esos países.

### Público por tema

| Tema | Vídeos | Vistas | 18–34 | 35+ | Hombres |
|---|---|---|---|---|---|
| Espacio | 1 | 8.734 | 56,4 % | 39,9 % | 62,8 % |
| Cotidiano | 2 | 2.923 | 36,0 % | 54,5 % | 57,3 % |
| Ciencia | 1 | 2.845 | 46,1 % | 49,9 % | 60,8 % |
| Histórico | 2 | 2.068 | 80,9 % | 19,1 % | 100,0 % |
| Misterio | 1 | 1.019 | 100,0 % | 0,0 % | 69,8 % |

