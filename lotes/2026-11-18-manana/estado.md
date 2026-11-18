# Estado — lote 2026-11-18-manana

- **Estado**: **en revisión** (v1 de los 3). Esperan el «ok» en el chat.
- **Agente**: Agente 08:00 (Nico) · MacBook Air de Nico · carpeta local `Documents/Parece Mentira/lotes/2026-11-18-manana`
- **Chat del lote**: https://claude.ai/code/session_019BG1dJLtMKt7d9zxuM93s6 (3 MP4 y 3 portadas enviados)
- **Correo de aviso**: enviado a parecementirapero.media@gmail.com, id `1a1ed968a22c00b4`.
- **Redes**: YouTube y TikTok (Instagram fuera, DECISIONS 2026-11-17).

## Vídeos (v1)
| # | Archivo (Mac de Nico) | Duración | Planos | SHA-256 | Calidad | Portada |
|---|---|---|---|---|---|---|
| 1 | `01-dia-18-horas_v1.mp4` | 59,2 s | 40 | `4907f8f27533c3e3d3e3b2da36d62c6d14f5619e3b430a1b565cbb98d1098eb6` | 95/100 | «UN DÍA DE 18 HORAS» · centro · 0,75 s |
| 2 | `02-gran-muralla_v1.mp4` | 58,2 s | 36 | `21bed650431590570b8cba27a54fda8c2c330093d1a2283ab77bc37e01b24de7` | 95/100 | «NO SE VE DESDE EL ESPACIO» · arriba · 3,8 s |
| 3 | `03-bostezo_v1.mp4` | 59,2 s | 42 | `7c50f7a9199a357d6c020c41009a6d881565ba94ebf7a133b4104db72b6c002f` | 91/100 | «TU PERRO TE COPIA» · arriba · 0,25 s |

SHA en el Mac = SHA del render (`shasum -a 256`). En la carpeta local: MP4, SRT, manifiestos, locuciones (`NN-locucion.mp3`, `02-locucion-corta.mp3`), alineaciones y `NN-portadas/portada.jpg`.

## Arranque
- Mac de Nico responde; lote nuevo (no existía `estado.md`).
- ElevenLabs: antes 28.812 libres; después **27.748** de 40.000 (≈7 lotes; se renuevan el 15-12).
- Studio (§1.8): **no se abrió** en este turno (se priorizó el lote); `studio.json` sin cambios.
- No hay experimento aprobado en `motor/APRENDIZAJE.md` ni abierto en `estadisticas/experimentos/`.
- La tarea programada pide Drive: no se usa (DECISIONS 2026-11-16, revisión en el chat).

## Decisiones según las estadísticas
Base: `aprendizajes.md` (8 vídeos, tendencia/pista) y `estudio.md` (nada pasa de «pista»).
- Espacio y un objeto grande en movimiento en el fotograma 0 son lo que mejor va (pista; H5/H7): 01 es Espacio; los tres abren con un solo objeto moviéndose y gancho de 5 palabras.
- Audiencia 72 % Latinoamérica: temas universales y sin expresiones de España.
- **Experimento del lote**: **gancho de negación** en el 02 («Esta muralla no se ve.»), primera vez en el canal. 01 y 03 (gancho de dato) son el control. Espero que el 02 iguale o supere a 01/03 en «se quedaron viendo».
- Vuelve un tema histórico (el lote anterior no tenía): se cuenta desde el presente (astronautas, la Estación Espacial).
- Duración 58–59 s: la pista «40–50 s» choca con DECISIONS (150–160 palabras) → no se aplica.

## Prueba del primer segundo (AGENTE §2)
| # | Objeto único y grande moviéndose en el fotograma 0 | Primera frase (≤ 5) | Alcance |
|---|---|---|---|
| 01 | La Tierra girando muy deprisa (entra con muelle) con la Luna enorme y cercana | «Un día duraba dieciocho horas.» (5) | universal |
| 02 | La muralla serpenteando por las montañas, cámara que se aleja y aspa roja a 0,9 s | «Esta muralla no se ve.» (5) | universal |
| 03 | Un perro grande con la boca abriéndose en un bostezo | «Tu perro copia tus bostezos.» (5) | universal |

## Temas
- 01: continuación de la Luna (candidato de `IDEAS.md`) con datos nuevos: rocas de Xiamaling, corales de Wells, tablillas babilónicas. Evitada la almeja fósil (ya salió en la Luna densa).
- 02: mito muy conocido (`reciclado=sí` en la ficha). 03: candidato «bostezo contagioso» de `IDEAS.md`, con el ángulo del perro.
- Cada dato con ≥ 2 fuentes (`guiones.md`). Descartado: la analogía «un pelo a X km» (las fuentes no coinciden en la distancia) y el % de contagio exacto (45–60 % frente a 60–70 %) → «más o menos la mitad».

## Voz
- API desde el Mac de Nico (eleven_v4, 0.5/0.75, `with-timestamps`), sin fallos. 01: 58,7 s · 02: 59,9 s · 03: 58,7 s.
- 02 pasaba de 60 s al montar: se quitó «Nadie había subido nunca.» con `omitir` (→ 57,7 s de voz; empalme revisado, sin clic). Sin gastar créditos de nuevo.

## Control de calidad
- `ffprobe`: 1080×1920, 30 fps, h264, AAC 48 kHz estéreo; duración = locución + ≈0,5 s.
- `motor.guion` ✓ los tres. `construir`: ✓ todos los textos se leen. `motor.calidad --mp4`: **sin ❌** (95/95/91; `calidad-0N.md`).
- Hojas de fotogramas miradas (cada 1 s durante el montaje y cada 2 s al final) y corregidas: costura de la esfera en 01, bulto de marea invisible, rótulos con poco contraste → cápsula (01, 02, 03), planos pobres o calcados rehechos, morro del perro cortado, bolsa y flecha mal colocadas en 03, ❌ de zoom < 1 en 03.
- ⚠ que quedan, justificados: «ritmo poco variado» (0,45 / 0,36 / 0,41): los cortes van atados a palabras de una voz a ≈2,7 palabras/s y ya hay 7 / 4 / 5 micro planos; 03 «mismo encuadre» 42–50 s = el diagrama de círculos familia → amigos → desconocidos, a propósito (cada plano enciende un anillo con otro foco).
- Relojes: 0 en los tres. Sin personajes que reaccionen; personas en silueta o perfil; sin logotipos ni banderas (astronautas sin cara, nave genérica).
- Cifras y nombres revisados contra guion y fuentes.

## Ficha de variables (AGENTE §6, en prueba)
- `estadisticas/fichas.json`: 2026-11-18-manana/01, /02 y /03 creadas antes de publicar (`ficha comprobar`: 0 problemas). experimento=no en la ficha (no hay experimento con ficha previa abierto; la negación del 02 es el experimento «de lote» de AGENTE §2).

## Generadores
`generadores/`: `NN-guion.txt`, `ilus_01.py` (Tierra antigua, capas, geólogos en silueta, corales vivo y fósil, freno, playa, Babilonia, tablilla…), `ilus_02.py` (montañas, muralla ×2, torre, carta de 1754, pluma, vista cenital, carretera y coche, Estación Espacial sin banderas, cápsula, casco, teleobjetivo, noche, descenso…), `ilus_03.py` (perro que bosteza por piezas en 4 razas, perritos de la cuadrícula, siluetas con boca abierta, vagón, Londres, salón, libro, bocadillo, móvil, cerebro, ventilador, bolsas fría y templada, ecografía) y `gen_0N.py DIR [locucion.mp3 alineacion.json]`. Render en la nube; resultados copiados al Mac.

## Publicación
Pendiente del «ok» (AGENTE §8): YouTube por API desde el Mac de Nico (1 h entre vídeos), TikTok por el navegador integrado (la persona elige el archivo).
