# Estudio de audiencia y rendimiento

Método para saber **quién nos ve**, **qué vídeos funcionan y cuáles no**, y **por qué**, sin engañarnos con
muestras pequeñas. Nació el 2026-11-17 (Nico). El planteamiento completo está en el doc del Proyecto de Claude
`claude/framework-estudio-audiencia-rendimiento.md`; esto es cómo está montado en el repo.

Relación con lo que ya había:

| Archivo | Qué es | Quién manda |
|---|---|---|
| `datos/aprendizajes.md` (`analizar.py`) | Conclusiones diarias de la web, rápidas | Sirve para mirar |
| **`datos/estudio.md`** (esto) | Qué se sabe **y con cuánta seguridad** | Decide si algo es pista, indicio o regla |
| `motor/APRENDIZAJE.md` | Cuaderno: referentes vistos, hipótesis, historia | Contexto y hipótesis |

Solo librería estándar de Python. Coste: 0 €.

```
estadisticas/
  fichas.json              la ficha de variables de cada vídeo (clave «<lote>/<NN>»)
  experimentos/<id>.json   experimentos con ficha previa
  estudio/
    __main__.py            las órdenes (python3 estadisticas/estudio …)
    ficha.py               diccionario de variables, lo que se calcula solo, validación
    mediciones.py          mediciones a edad fija (24 h, 48 h, 7 d, 28 d)
    tabla.py               una fila por vídeo: ficha + mediciones
    estadistica.py         medianas, intervalos, permutación, tamaño de muestra, niveles
    analisis.py            el estudio (datos/estudio.md)
    autopsia.py            diagnóstico por vídeo (datos/autopsias.md)
    experimento.py         ficha previa, calendario, cierre
    informe.py             informe semanal
    comentarios.py         clasificación de comentarios
    recogida_extra.py      audiencia por vídeo y comentarios (lo llama recoger.py)
    objetivo.json          público objetivo (hoy: propuesta sin confirmar)
    prueba.py              113 pruebas, sin red
  datos/
    mediciones.json  estudio.md  estudio.json  autopsias.md  informe-semanal-<lunes>.md  comentarios.json
```

## Qué pasa solo cada mañana

`.github/workflows/estadisticas.yml`, después de recoger los datos y construir la web, ejecuta
`python3 estadisticas/estudio todo`: actualiza las mediciones, el estudio y las autopsias. Los lunes, además, el
informe semanal. Si falla, la web y los datos del día se guardan igual.

## Las cinco ideas

### 1. Ficha de variables, antes de publicar
Cada vídeo se describe con las mismas variables (`python3 estadisticas/estudio ficha diccionario`). Si se etiqueta
después de ver las vistas, uno acaba viendo en el vídeo lo que explica el resultado: por eso la ficha lleva
`momento: previo` o `retrospectivo`, y el estudio cuenta cuántas hay de cada.

```bash
python3 estadisticas/estudio ficha nueva 2026-11-18-manana 01 \
  --guion lotes/2026-11-18-manana/generadores/01-guion.txt --calidad lotes/2026-11-18-manana/calidad-01.md \
  --quien "Agente 08:00" tema=Espacio alcance=universal epoca="sin época" gancho=dato f0_palabras=4 \
  f0_sujeto=objeto f0_literal=sí estructura=comparación remate=pregunta duracion_s=56 montaje=denso \
  subtitulo=karaoke voz=clon reciclado=no experimento=no brazo=-
python3 estadisticas/estudio ficha comprobar
python3 estadisticas/estudio ficha publicar 2026-11-18-manana 01 <id de YouTube> tiktok=<número>   # al publicar
```

Las variables **subjetivas** (`tema`, `alcance`, `epoca`, `gancho`, `f0_sujeto`, `f0_literal`, `estructura`, `remate`)
hay que comprobarlas con dos personas: otro codificador rellena las mismas fichas en otro archivo y
`ficha acuerdo otro.json` dice en qué porcentaje coinciden. Por debajo del 80 %, la definición está mal escrita.

### 2. Mediciones a edad fija
Un vídeo con 31 h no se compara con otro de 2 h. `datos/mediciones.json` guarda, por vídeo y red, la foto a las
24 h, 48 h, 7 días y 28 días. Las vistas se interpolan a la edad exacta entre las lecturas que la rodean; los
porcentajes son la primera lectura hecha a partir de esa edad (con la edad real apuntada). **Una medición guardada
no se reescribe.** Las lecturas con menos de 24 h no entran en ningún cálculo.

Para que haya datos, sigue haciendo falta lo de siempre: `studio.json` («se quedaron viendo») y
`tiktok_studio.json` (retención) de los vídeos con 24 h o más, al arrancar cada lote.

### 3. Niveles de evidencia

| Nivel | Requisito | Qué se puede hacer |
|---|---|---|
| **pista** | Menos de 5 vídeos por grupo, o indistinguible del azar | Formular una hipótesis. Nada más |
| **indicio** | 5 o más por grupo, p < 0,10 y mismo sentido en YouTube y TikTok | Priorizar el experimento; aplicar solo si es gratis y reversible |
| **regla** | 10 o más por grupo, intervalo al 90 % que no cruza el cero, mismo sentido en la otra red, repetido en dos semanas y p < 0,05 repartido entre todas las comparaciones miradas | Pasa a `DECISIONS.md` |

Un **experimento con ficha previa** mira una sola comparación, así que no paga el reparto del p y llega a regla con
muchos menos vídeos. Ese es el camino normal para conseguir una regla.

Por qué son tan exigentes: se simularon estudios de 90 vídeos **sin ningún efecto real**. Con la primera versión
de los niveles (sin exigir p), la mitad de las comparaciones salían «indicio» y 7 de cada 10 estudios daban alguna
«regla» falsa. Con los actuales: 0 reglas falsas en 100 estudios y un 5 % de indicios falsos. Y con un efecto real
de 15 puntos en «se quedaron viendo», 90 vídeos lo convierten en regla 8 de cada 10 veces (40 vídeos: 4 de cada 10).

### 4. Experimentos
```bash
python3 estadisticas/estudio tamano 16 15        # ¿cuántos vídeos por grupo para ver 15 puntos? → 18
python3 estadisticas/estudio experimento nuevo H3 --hipotesis "El gancho en segunda persona retiene más" \
  --variable gancho_persona --metrica yt_se_quedan --diferencia 15 --por-dia 2 --quien Nico \
  --a-favor "Regla en AGENTE §3" --en-contra "Se deja de proponer"
python3 estadisticas/estudio experimento estado
python3 estadisticas/estudio experimento cerrar H3
```
La ficha previa no se reescribe y el experimento no se cierra antes de su fecha (salvo `--forzar`, que queda
apuntado). Diseño: cada día un vídeo de cada brazo, del mismo tema si se puede, alternando cuál sale primero.

### 5. Autopsia por vídeo
`datos/autopsias.md`: cada vídeo frente a la mediana del canal, **un** diagnóstico (tema · primer segundo · ritmo ·
distribución · acierto · normal) y **una** acción. Si hay curva de retención, cada escalón se apunta con la frase
que sonaba (tiempos estimados, ±2 s: las alineaciones exactas no están en el repo).

## Audiencia
- **Canal** (ya se recogía): edad × género, países, suscritos. El estudio añade segundos por vista por país y la
  distancia al público objetivo de `objetivo.json`.
- **Por vídeo** (nuevo, `recogida_extra.py`): edad × género y países de cada vídeo de entre 2 y 14 días. YouTube
  solo lo da a partir de un umbral que no publica; mientras no llegue, sale vacío. Con eso el estudio monta el
  «público por tema», sumando vídeos.
- **Comentarios** (nuevo): texto, fecha y likes, **sin autor**, en `datos/comentarios.json`.
- Límites que no dependen de nosotros: Instagram no da audiencia por Reel y pide 100 seguidores; TikTok solo la
  enseña en TikTok Studio; ninguna red da retención por edad o género.

⚠ `recogida_extra.py` está probado con un YouTube simulado, **no contra la API real** (no hay credenciales fuera
de GitHub Actions). Puede que el permiso actual de solo lectura no deje leer comentarios: en ese caso avisa una
vez en el registro del workflow y sigue.

## Órdenes
`python3 estadisticas/estudio` sin nada las lista. La más útil para mirar ya, antes de tener 48 h:
`python3 estadisticas/estudio estudio --orientativo` (mezcla edades; no se guarda y no vale como evidencia).

## Pruebas
```bash
python3 estadisticas/estudio/prueba.py
```
