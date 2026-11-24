# Cómo escribir los planos del vídeo largo «500 días en una cueva»

Lo lee quien escribe los planos de una parte (`generadores/planos_pN.py`). Lee también:
- `ARTE.md`: cómo son los dibujos.
- `PIEZAS.txt`: qué piezas hay.
- `generadores/comun.py`: los ayudantes. Lee su cabecera entera.
- `generadores/planos_p1.py`: los primeros planos ya hechos, que son el modelo.
- `/home/claude/parece-mentira/motor/denso.py`: `P`, `K`, `IMG`, `rotulo`, `contador`, `amarillo`, `flecha`, `senala`, `aparece`, `cae`, `lanza`, `late`, `sigue`, `arranque`, `brillo`, `recorrido`, `fx`, `fx_espaciado`.
- `/home/claude/parece-mentira/motor/DENSO.md` y `motor/GUIA_CALIDAD.md`: las reglas del canal. Échales un vistazo.

## El encargo (de Nico, el dueño del canal)
- Vídeo de 8 min 31 s con una voz ya grabada (`indices.txt`: índice, segundo y palabra de cada palabra del guion; `guion.txt`).
- Sale en **horizontal 16:9 para YouTube** y en **vertical 9:16 para TikTok**, cortado en 5 partes.
- **Un solo montaje para los dos formatos**: cada plano se escribe UNA vez en coordenadas del vertical (1080×1920) y `comun.adaptar` lo recompone para el horizontal (ver la cabecera de `comun.py`).
- Partes, por palabra de inicio:

| Parte | Palabras | Duración |
|---|---|---|
| 1 | 0–286 | 0:00–1:47 |
| 2 | 287–582 | hasta 3:36 |
| 3 | 583–843 | hasta 5:17 |
| 4 | 844–1034 | hasta 6:38 |
| 5 | 1035–1341 | hasta el final |

- Tu parte DEBE tener un plano que empiece exactamente en su primera palabra (`@plano(INICIO, …)`) y no puede tener planos de otras partes.

## Lo que pide Nico (no negociable)
- **Método denso**: muchos planos de duración variable, de 0,3 a 3 s, cada uno atado a la palabra exacta del guion.
  - En ráfagas, micro planos de 0,3–0,7 s: cifras, golpes, detalles.
  - En planos de respiro, 2–3 s para entender algo.
  - Objetivo: **≈30–36 cortes por minuto** de media, es decir unos 50–60 planos por parte. Ningún plano de más de 4 s.
  - Micro escenas de detalles secundarios: la gota que cae, la página que pasa, la lámpara que parpadea, la mano que hace la raya.
- **Que pase algo en pantalla todo el rato**: nada quieto más de un segundo.
  - Cada plano lleva una acción: algo cae, aparece, crece, se mueve, se enciende, pasa la página, aletea.
  - Además, un movimiento de cámara suave: `cam(z0, z1, foco0, foco1)` con zoom siempre ≥ 1.
- **Pantalla completa**: fondo con varios tonos. Sin título arriba, sin rótulos blancos con borde azul, sin la mascota.
  - El subtítulo karaoke lo pone el motor solo, así que no repitas en rótulos lo que dice la voz.
  - Rótulos solo para cifras o 1–3 palabras clave: `contador`, `rotulo` con cápsula de color o `amarillo`. Pocos.
- **Detalles de fondo que duren varios segundos**: murciélagos (`comun.VUELOS` + `ambiente_cueva`), gotas (`goteo`), estalactitas (`techo`), polvo en la luz, la luz del frontal.
  - En la cueva, usa `ambiente_cueva(d, sem=…)` en casi todos los planos.
- **Sonido**: efectos bajos para lo que pasa (`sfx=[(t, tipo, dB)]` con t en s del plano). Tipos en `motor/sfx.py`: tic, golpe, zap, brillo, ding, rumor, burbuja, roce, agua, tictac, subida, impacto, senal, trazo, pop, whoosh…
  - Niveles: detalles −30…−24 dB, acciones −24…−16. Pocos golpes fuertes.
  - Las entradas `"desenfoque"`, `"zoom"` y `"barrido"` meten un «shhh» de transición: úsalas poco, una cada 10–15 s como mucho. Lo normal es `"corte"`.
  - Para la revelación fuerte de tu parte, una vez: `(t, "subida", -18, {"dur": 1.0})` antes e `"impacto"` en el golpe.
- **Este vídeo va del tiempo: pocos relojes**.
  - En todo el vídeo solo puede haber 2 escenas con reloj (`reloj_interno`, `reloj_bolsillo`, `cronometro`), y nunca dos seguidas. Esas dos se las reserva la parte 2 («reloj interno»).
  - `reloj_arena` ya sale en la parte 1; no lo repitas.
  - Enseña el tiempo de otras formas: velas que se consumen (`vela_a/b`, `vela_corta`), libros que se apilan, rayas de tiza en la pared (`tiza`), gorros de lana que se acumulan, garrafas vacías, estaciones que pasan arriba (`hoja_otono`, `copo_nieve`, `flor_primavera`, `sol_verano`), hojas de calendario que vuelan, contadores.
- **No repitas el mismo objeto con la misma animación**: si un objeto vuelve, cambia de escala, de escenario o de movimiento.
- **Caras**: para los momentos de emoción usa los bustos `bea_cara_*` en primer plano.
  - Personajes posados con `pie(nombre, x, suelo, alto)`, de modo que los pies queden en el suelo del fondo (`comun.ANCLA` da el suelo de cada fondo en el vertical).
  - Coherencia: Beatriz es siempre la misma.
- **Personas reales**: Beatriz Flamini y Michel Siffre se dibujan como figuras genéricas (las piezas ya lo son). No les pongas texto en la boca. Nada que no esté en el guion.
- **Variedad**: el vídeo es largo, así que cambia de escenario y alterna ráfagas con planos de respiro.
  - No dejes el mismo fondo más de ≈10 s seguidos sin meter un inserto (un primer plano de objeto o de cara, un corte de la montaña, un plano de la superficie…).
- **Los dos formatos**:
  - Rellena los laterales del horizontal: pon cosas en x < 0 o x > 1080 (solo se ven en 16:9). Más estalactitas, más libros, otra persona del grupo, rocas…
  - En el vertical, lo importante va entre y=420 y y=1400. Arriba está el subtítulo (y≈320) y abajo los botones de TikTok. A la derecha, por debajo de y=800, no pongas rótulos (x < 900).
  - Rótulos: en y 450–1350 del vertical.
  - En el horizontal los rótulos y el sujeto no pueden caer en la franja del subtítulo (abajo). Con el ancla de cada fondo, el suelo del vertical se convierte en el suelo del horizontal: lo que esté muy abajo en el vertical (y > 1500) se sale por abajo en el horizontal.
- **Lectura**: todo rótulo tiene que estar al menos 0,25 s + 1 s por cada 17 letras. `construir` avisa con ⚠, y no se entrega con avisos.

## Ayudantes que más se usan (en `comun.py`)
- `fondo("bg_…")`: fondo a pantalla completa (el `_h` lo pone solo).
- `pie(n, x, suelo, alto, z, keys)`: personaje u objeto posado.
- `pieza(n, x, y, ancho, z, keys)`: centrado.
- `flip([n_a, n_b], d, fps, base=lambda n: pie(n, …))`: fotogramas que se alternan.
- `ambiente_cueva(d, sem, oscura, gotas, murc, primer_plano)`, `techo(sem)`, `goteo(...)`, `tiza(x, y, t0, alto)`.
- `cam`, `polvo`, `estrellas`, `fundido_blanco`, `negro`: versiones que trabajan en coordenadas del vertical. Usa ESTAS, no las del motor.
- `murcielagos(d)`: añade a `comun.VUELOS` tus cruces con tiempos de palabra `(v.w(i), v.w(i)+6, (x0,y0), (x1,y1), ancho)` al principio de `planos()`.
- `K(d, (0, {...}), (0.5, {...}), (1, {...}))`: claves en fracción del plano. Movimiento: `aparece(t)`, `cae(t0, t1, y0, y1)`, `lanza`, `late`, `arranque(x, y, d)` para sujetos que tienen que moverse desde el fotograma 0.
- `"_solo": "v"` / `"_solo": "h"` en un elemento lo deja solo en ese formato. `"_ancho": True` estira su x a todo el ancho. `"_full": True` lo pone a pantalla completa.

## Cómo probar (obligatorio, en los dos formatos)
```
cd /home/claude/parece-mentira/lotes/largo-cueva-500-dias/generadores
S=/tmp/prueba_pN                       # carpeta tuya
python3 gen.py $S/v --partes N                       # vertical: lista de planos, duraciones y avisos ⚠
MOTOR_FORMATO=16:9 python3 gen.py $S/h --partes N    # horizontal
python3 hoja_tramo.py $S/v/episodio.json T0 T1 0.75 $S/hv.jpg
MOTOR_FORMATO=16:9 python3 hoja_tramo.py $S/h/episodio.json T0 T1 0.75 $S/hh.jpg
```
- T0 y T1 son los segundos de tu parte (columna 2 de `indices.txt`). Para mirar mejor, haz hojas de tramos de ≈30 s.
- Mira las hojas con la herramienta Read y corrige:
  - planos vacíos o pobres;
  - sujetos cortados en el vertical;
  - laterales vacíos en el horizontal;
  - rótulos encima del sujeto o en la franja del subtítulo;
  - caras raras, cosas que flotan, repeticiones, más de 1 s sin movimiento.
- Itera hasta que esté bien. Al final, `construir` no puede dar ningún ⚠ de lectura en tu parte.
- El último plano de la parte anterior se alarga hasta tu primer plano. Si pruebas tu parte sola, el último plano se estira hasta el final del audio: no pasa nada, no lo mires.
- La máquina tiene 2 núcleos y comparte con otros. No lances renders de vídeo, solo hojas de tramos.

## Entrega (tu respuesta final)
- Número de planos y cortes por minuto.
- Rutas de las dos hojas finales.
- Lista corta de lo que no te convence.
- No toques `comun.py`, `gen.py`, `marcas.py` ni las partes de otros. Si necesitas un ayudante nuevo, defínelo dentro de tu `planos_pN.py`. No hagas commits.
