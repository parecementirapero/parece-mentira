# Arte del vídeo «El que copiaba en el colegio» — guía común

Lo leen todos los que dibujan piezas para este vídeo. Si algo no está aquí, decide con criterio y apúntalo en tu informe.

## Qué es
- Vídeo de 4:45 para YouTube (16:9) y uno de 1 min vertical (9:16) con la misma voz. Guion: `lotes/largo-el-que-copiaba/guion.txt`.
- Historia: Marta (original) y Lucas (copiaba) en el colegio; de mayores, Marta abre una cafetería original donde pagas por tiempo y fracasa (persiana abajo); Lucas copia una hamburguesería con cola, la mejora (espera 5 min en vez de 20) y triunfa (dos locales). Luego: el móvil (buscador, red social, historias: genéricos, SIN logos), cómo aprendes en la vida (niño que regatea, guitarrista, cocinero), la trampa (copiar tal cual = repartir clientes; hay que mejorar UNA cosa: más rápido, barato, cerca, bonito) y el final (Marta abre una cafetería normal con su toque y tiene cola).
- Se monta con `motor/denso.py`: cada pieza es un SVG que el motor rasteriza y mueve (posición, escala, giro, opacidad, estirar). No hay esqueletos: si algo se mueve por dentro, se entregan fotogramas `_a`, `_b` idénticos salvo lo que cambia (misma caja).

## Estilo: el del vídeo largo de la cueva (DECISIONS 2026-11-26)
**Es obligatorio reutilizar sus módulos**: `lotes/largo-cueva-500-dias/generadores/` (`ilus_personajes`: `Lz`, `figura`, `busto`, `_pj`, `mat`, `sombra_suelo`, `pie_suelo`, `_cuadro`, pieles `PIEL2/3/4`, `PIEL_BEA`; `ilus_escenarios`: `Lienzo`, `suave`, `_edificios`, `_nube`, `_olivo`, `mezcla`…; y sus objetos). Léete `lotes/largo-cueva-500-dias/ARTE.md` (luz principal + luz de borde, degradados, grano, sombra de contacto, fondos con capas y profundidad, caras bien dibujadas, cabeza = 1/7 de la altura, nada de monigotes).
- Modelos ya hechos en este estilo que puedes copiar: `lotes/2026-11-25-tarde/generadores/ilus_1125t.py` (`p_de_pie`, `p_mira_arriba`, `caras`, `medalla`, `caballete`, `farola`, fondos `bg_galeria`…) y `lotes/largo-el-que-copiaba/generadores/frame_prueba.py` (`persona`, `persona_perfil`, `hamburgueseria`, `bocadillo_cola`) — esa hamburguesería, la cola de perfil y Lucas ya están aprobados por Jorge: mismo nivel.
- **Prohibido**: letras o números dentro de los dibujos (los rótulos los pone el motor), logotipos o marcas reales (nada de la G de Google, la f de Facebook, el icono de Instagram ni el fantasma de Snapchat: usa iconos genéricos como lupa, globo de perfil, círculos de historias con colores inventados), personajes conocidos, nada sangriento.

## Personajes fijos (siempre igual)
- **Marta**: pelo castaño rojizo (#7a3a22, brillo #b5643a) en **coleta alta**, piel PIEL4, iris verde #3d6a5a. De niña: jersey mostaza (#e0a92e / luz #f4cc6a / sombra #8a6010). De adulta: chaqueta mostaza igual + camiseta blanca, vaquero (#3b5274), zapatillas blancas. Expresiva y simpática: no es tonta, es creativa.
- **Lucas**: pelo corto casi negro (#1e1612), piel PIEL4, polar azul (#2f6fb0 / #5f9fe0 / #173a60), pantalón gris oscuro (#2e3440), zapatillas blancas. Es el de `frame_prueba.py` (`LUCAS`). De niño, misma ropa en pequeño. En su local lleva delantal rojo (#c8322a) encima del polar.
- **Niños**: usa `figura(..., alto=…)` o una `u` menor y `edad` baja para que parezcan de 10–12 años (cabeza proporcionalmente más grande, 1/6).
- **Profesora**: unos 45 años, pelo corto gris (#8a8a90), gafas finas, rebeca granate (#7a2a3a), falda gris.

## Formatos y tamaños
- Fondos: cada uno en `nombre.svg` (1080×1920) y `nombre_h.svg` (1920×1080), recompuestos (no recortados). En el vertical, lo importante entre y=420 y y=1450; en el horizontal entre y=60 y y=880. Sin personajes ni objetos animables dentro. Apunta la **y del suelo** de cada formato en tu informe (la necesito para el ancla).
- Piezas: fondo transparente, lienzo ajustado a la pieza, centrada. Apunta el punto de apoyo (fracción de la altura donde están los pies o la base).
- Los fondos de `ilus_escenarios` se crean con `L = IE.Lienzo(nombre, 1080, 1920, semilla)`, `f(L)`, `L.guardar(dir, nombre)`; para el horizontal, `Lienzo(nombre, 1920, 1080, semilla)` (mira cómo lo hace `ilus_escenarios.generar`).

## Cómo programar
- Tu archivo: `lotes/largo-el-que-copiaba/generadores/ilus_<tuyo>.py` con `generar(dirsvg)` que escribe todas tus piezas en `dirsvg` y devuelve la lista de nombres. Importa así (como `frame_prueba.py`): `sys.path.insert(0, RAIZ); sys.path.insert(0, LARGO)`; `from motor.biblioteca import ilus`; `import ilus_personajes as IP`; `import ilus_escenarios as IE`; pon `ilus.OUT = dirsvg` antes de guardar.
- Ids de degradados con prefijo propio. Aleatoriedad con semilla fija. Cada SVG debe rasterizar en < 3 s (`rsvg-convert`); pocos filtros de desenfoque grandes.
- Ojo, ya visto: con vista de frente, `_pj` sin `largo` (abrigo largo) porque falla; manos solo `t="lado"` o `t="plana"`; para que una figura de perfil mire hacia arriba, ángulo positivo.
- **Revisión obligatoria**: renderiza cada pieza con `rsvg-convert` a PNG, haz una hoja de contacto (PIL) y **mírala** (Read). Corrige lo que se vea mal (manos raras, caras sin ojos, piezas cortadas por el borde del lienzo, flotando). No entregues sin mirar.
- No toques archivos fuera de tu `ilus_<tuyo>.py` y tu carpeta de pruebas en /tmp. No hagas commit (lo hago yo).
