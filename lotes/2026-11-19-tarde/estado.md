# Estado — lote 2026-11-19-tarde

- **Estado**: en curso
- **Agente**: Agente 20:00 (Jorge) · Mac de Jorge (`jorges-macbook-air-2`) · carpeta local `Documents/Parece Mentira/lotes/2026-11-19-tarde`
- **Chat del lote**: https://claude.ai/code/session_019BG1dKjUgmMjL827TDKKHq
- **Redes**: YouTube y TikTok (Instagram fuera, DECISIONS 2026-11-17).
- La tarea programada de las 20:00 del 19-11 se disparó el **20-11 a las 12:49** (Madrid). El lote lleva el nombre del turno que faltaba (2026-11-19-tarde) para no chocar con el de esta noche (2026-11-20-tarde).

## Arranque
- Lote nuevo (no existía `estado.md`). Mac de Jorge responde (12:50).
- ElevenLabs a las 12:50: **24.584** caracteres libres de 40.000 (da para el lote: ≈3.500).
- 12:55: el puente del Mac se cae («not connected to the bridge»). Mientras tanto, en la nube: temas, fuentes, guiones, metadatos y montaje con tiempos provisionales. El Mac vuelve un momento a las ≈13:40 y se cae antes de poder lanzar la voz.
- Studio (§1.8): no se abrió (Mac sin puente). No hay experimento aprobado en `estadisticas/experimentos/`.

## Temas (3, verificados con ≥ 2 fuentes; ver `guiones.md`)
1. **Los atardeceres en Marte son azules** — Espacio · **pov** · comparación · universal · **experimento: gancho POV**.
2. **Naciste con trescientos huesos** — Ciencia · dato · reconstrucción · universal · control.
3. **Las gotas no son así** (forma real de una gota) — Cotidiano · negación · experimento · universal · control.

## Decisiones según las estadísticas
Base: `aprendizajes.md` (2026-11-20 09:20, 22 vídeos).
- **Firme**: primer fotograma y primera frase deciden → los tres abren con un solo objeto grande moviéndose (Sol bajando con halo, esqueleto que cae, gota con punta enorme) y frase de 4–5 palabras.
- **Firme**: 75 % Latinoamérica → sin expresiones de España; temas universales (Marte, el cuerpo, la lluvia).
- **Tendencia**: Espacio gana en todo → el 01 es Espacio; Ciencia segunda → el 02. Histórico, el peor → no se usa hoy. El 03 es Cotidiano con gancho de negación (71 % «se quedan», 1 vídeo).
- **Experimento del lote**: **gancho POV** en el 01 («POV, atardece en Marte.»), primera vez en el canal; tema (Espacio), duración y estructura como los que mejor van. 02 (dato) y 03 (negación) de control. Espero que el 01 iguale o supere el 65 % de «se quedaron viendo»; si queda por debajo de los otros Espacio (69,6 % de media), es una pista en contra del POV.

## Prueba del primer segundo (AGENTE §2)
| # | Objeto único y grande moviéndose en el fotograma 0 | Primera frase (≤ 5) | Alcance |
|---|---|---|---|
| 01 | El Sol rosado bajando hacia la cresta mientras el halo azul crece | «POV, atardece en Marte.» (4) | universal |
| 02 | El esqueleto de un bebé que cae y bota, con «300» | «Naciste con trescientos huesos.» (4) | universal |
| 03 | Una gota con punta enorme que cae y recibe un «NO» | «Las gotas no son así.» (5) | universal |

## Guiones
- `motor.guion`: 01 156 palabras · 02 157 · 03 159, ningún ❌. ⚠ «tramo de 15–16 s sin pregunta ni dato» en los tres: justificado, son tramos de explicación con cortes de 1–2 s y una cifra o rótulo en pantalla en cada uno.

## Montaje (tiempos provisionales, sin voz)
- `generadores/ilus_1119t.py`: 46 SVG nuevos (paisaje de Marte de día y al atardecer con halo, atardecer en la Tierra, rover genérico, fotos, planeta, grano de polvo, haz de colores, botes de aire, soles; rayos X, esqueletos adulto y bebé, mano, pie, cráneo con fontanelas abierto y cerrado, bebé, cuarto, fémur, estribo, grano de arroz, oreja en corte, cartílago; gotas lágrima/esfera/pan/paracaídas, gotitas, pan de hamburguesa, paracaídas, lápiz, nubes, lluvia, velocímetro, perfil con nube).
- `gen_01.py` 32 planos · `gen_02.py` 31 · `gen_03.py` 29. Hojas de fotogramas revisadas y corregidas (esqueleto más abajo para que los rótulos no le tapen el pecho, rótulos con cápsula sobre fondos claros, nube más baja para que no choque con la cifra).
