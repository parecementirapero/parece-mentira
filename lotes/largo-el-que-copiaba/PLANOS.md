# Montaje de «El que copiaba en el colegio» — guía para escribir planos

## Qué hay
- Voz: `voz/locucion-completa.wav` (285 s) y `voz/alineacion-completa.json`. **Índice de cada palabra con su segundo**: `indices.txt` (`i segundo palabra`). Guion: `guion.txt`.
- Montaje: `generadores/gen.py` + `generadores/comun_cp.py` (ayudantes; importa el `comun.py` del vídeo de la cueva: `pie`, `pieza`, `flip`, `fondo`, `cam`, `polvo`, `negro`, `fundido_blanco`, `adaptar`…) + `generadores/planos_p1.py`, `planos_p2.py`, `planos_p3.py` (un archivo por tramo) + `planos_corto.py` (el corto).
- Arte ya generado (solo lectura): `/tmp/cp/_arte/*.svg`. Mira las hojas de contacto: `/tmp/arte_fondos/hoja.png`, `/tmp/arte_gente/hoja.png`, `/tmp/arte_cosas/hoja.png`, y el fotograma aprobado `/tmp/fr/frame.png`. También vale todo el arte del vídeo de la cueva (ciudad de noche `bg_ciudad`, oficina, estadio, cerebro, `telefono_movil`, `taza_cafe`, `calendario_hoja`, `voluntario_1..6`, `adulto_camina`…).
- Si te falta una pieza, créala en `generadores/ilus_extra_pN.py` (tu N) con `generar(dirsvg)` y nombres con prefijo `pN_`, en el estilo de `ARTE.md`, y míralas renderizadas. gen.py la carga sola.

## Cómo se escribe un plano (modelo: `lotes/largo-cueva-500-dias/generadores/planos_p1.py`; lee también `motor/DENSO.md` y `motor/GUIA_CALIDAD.md`)
```python
from comun_cp import *
def planos(v, plano):
    @plano(150, "Marta piensa meses")          # índice de la primera palabra del plano
    def _(d):                                  # d = duración del plano en s
        return P(["#f2e6c8", "#a08060"], [fondo("bg_cafe_dentro"), pie("marta_piensa", 540, 1430, 620, z=0.5), ...],
                 cam(1.0, 1.1, (540, 1200)), "corte", hud=[contador(...)], sfx=[(0.1, "ding", -22)])
```
- **Coordenadas del vertical (1080×1920)**; el largo sale en 16:9 y `adaptar` lo recoloca respecto al suelo de cada fondo (escala 0,8). Por eso: lo importante entre y≈420 y y≈1450; **rellena los laterales** (x<0 y x>1080, hasta −500 y 1580) porque en el horizontal se ven: más pupitres, más gente, más local, plantas, farolas.
- Suelo de cada fondo (y del vertical donde pisan los pies con `pie(nombre, x, suelo, alto)`): aula 1420, colegio fuera 1430, calle día 1440, café dentro/triste 1430, cocina 1440, habitación 1440, campo barrio 1440, estudio oscuro 1400, ciudad noche 1390. Altos orientativos: adulto ≈ 600–650, niño sentado ≈ 520, local (fachada) ≈ 560–620, persona en cola ≈ 430.
- Datos de piezas: niños sentados → la mesa (pupitre, canto delantero a 0,35 de su alto) delante, a la altura de sus manos (fracción «mesa» ≈ 0,47–0,51 desde arriba del niño). `persiana` va sobre `cafeteria_marta` en el hueco x=110–790, y=332–810 del lienzo 900×820 de la fachada (bájala con `ey` o moviendo y con la fachada por delante). `movil_mano`: pantalla blanca en 144,54–416,626 de su lienzo 560×940. `app_historias`: círculos en x=120+i·215, y=125 de 1100×260. `foco_luz`/`foco_luz_frio`: 900×1580, mancha del suelo a 0,949. Fotogramas a/b: usa `flip([...a, ...b], d, fps=…)`.
- Personajes fijos: **Marta** (coleta alta, chaqueta mostaza) y **Lucas** (polar azul; con delantal rojo en su local). Siempre los mismos.
- Rótulos: `rotulo`, `amarillo`, `contador`, `senala`, `flecha` del motor (las letras van como rótulo, nunca dentro del dibujo). Nombres de marcas solo como rótulo de texto si hace falta; **nunca logos**. Lectura: 0,25 s + 1 s por 17 letras; `construir` avisa con ⚠ y **no puede quedar ninguno**.

## Ritmo (largo de YouTube)
- ≈ 30–38 planos por minuto: planos principales de 2–3,5 s donde hay que entender algo y micro planos de 0,3–0,8 s en los golpes (cifras, detalles, reacciones). Nada quieto más de 4 s: cámara que se mueve, algo que entra, cae, late, cuenta. 5–9 elementos en capas.
- Que se **vea pasar** lo que se cuenta: la persiana baja, la cola cambia de calle, el contador de minutos baja de 20 a 5, la hucha se vacía, la bombilla se enciende.
- Sonido con `sfx=[(t, tipo, db)]` (lista en `motor/sfx.py`): bajos (−28…−18), un golpe fuerte de vez en cuando. La música «emprende» va sola.
- Variedad: no repitas el mismo encuadre seguido; alterna planos generales, medios, caras (`cara_*`) y detalles (objetos grandes sobre `bg_estudio_oscuro` con un foco).

## Probar tu tramo
```
cd lotes/largo-el-que-copiaba/generadores
ARTE_CP=/tmp/cp/_arte MOTOR_FORMATO=16:9 python3 gen.py /tmp/cp/pN --partes N      # avisos ⚠ de lectura: ninguno
MOTOR_FORMATO=16:9 python3 -m motor.render /tmp/cp/pN/episodio.json --salida /tmp/cp/pN --desde T0 --hasta T1
ffmpeg -i <mp4> -vf fps=1,scale=480:-1,tile=6x5 hoja.jpg       # y MÍRALA con Read
```
Revisa: pies en el suelo, nada cortado ni tapado por el subtítulo (abajo en 16:9), laterales llenos, caras visibles, cosas que se mueven, el texto se lee.
