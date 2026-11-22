# Control de calidad — e03b

**Nota: 80/100**

- **ritmo**: planos=34 · cortes_min=41.2 · mediana=1.33 · min=0.64 · max=2.52 · variacion=0.37 · micro=2 · largos=8
- **rotulos**: total=27 · fuera_de_zona=0 · en_franja_dudosa=1 · sin_tiempo=0
- **gancho**: palabras_primera_frase=5 · voz_empieza=0.0 · fin_primera_frase=2.08 · palabras=142 · palabras_s=2.91 · acciones_primer_plano=0
- **imagen**: elementos_por_plano=5.3 · ilustraciones=12 · fondos_distintos=8 · mismo_fondo_max_s=8.4
- **imagen_real**: detalle_medio=6.4 · detalle_min=2.4 · planos_pobres=1 · planos_calcados=0 · rachas_mismo_encuadre=0 · primer_fotograma_detalle=4.2 · rotulos_poco_contraste=0 · movimiento_primer_segundo=12.15
- **sonido**: efectos=58 · por_minuto=70 · tipos=11 · whoosh_min=7.3 · max_en_1s=3 · musica_db=-13
- **movimiento**: quieto_pct=3.0 · movimiento_medio=7.38 · bucle_diferencia=26.6
- **mezcla**: voz_rms=-20.9 · musica_bajo_voz_db=-8.6 · sfx_pico_frente_a_voz_db=-6.3 · sfx_rms_bajo_voz_db=-10.5 · efectos_que_tapan_voz=7

- ⚠ Ritmo poco variado (variación 0.37; mejor ≥ 0,45).
- ⚠ Menos de 3 micro planos (< 0,7 s): faltan golpes rápidos de detalle.
- ⚠ En el primer plano no se mueve nada en los primeros 0,6 s: el gancho necesita acción desde el fotograma 0.
- ⚠ Planos de más de 1 s con menos de 3 elementos: [15].
- ⚠ Planos pobres (casi sin dibujo: fondo liso con un objeto pequeño): plano 27 (36.7 s, detalle 2.4). Añade contexto o un sujeto más grande.
- ℹ 1 rótulos entre y=1250 y y=1400: visibles en el feed normal, pero las guías de anuncios de las tres apps piden dejar libres ~660 px abajo (y≤1250). Si el texto es esencial, súbelo: «DERECHA» (11.9 s, llega a y=1387)
- ℹ El último fotograma no se parece al primero (diferencia 27/255): el vídeo no enlaza en bucle. Los bucles suben el % visto.
- ℹ En 7 momentos un efecto suena tan alto como la voz de ese instante (al mezclar, el motor los atenúa bajo la voz): 0.5 s, 23.5 s, 25.2 s, 33.5 s, 34.8 s, 40.8 s, 44.5 s
