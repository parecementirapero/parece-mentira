# Control de calidad — v01

**Nota: 84/100**

- **ritmo**: planos=35 · cortes_min=38.0 · mediana=1.33 · min=0.64 · max=3.12 · variacion=0.42 · micro=1 · largos=8
- **rotulos**: total=24 · fuera_de_zona=0 · en_franja_dudosa=7 · sin_tiempo=0
- **gancho**: palabras_primera_frase=5 · voz_empieza=0.0 · fin_primera_frase=1.6 · palabras=150 · palabras_s=2.75 · acciones_primer_plano=5
- **imagen**: elementos_por_plano=5.1 · ilustraciones=16 · fondos_distintos=12 · mismo_fondo_max_s=5.6
- **imagen_real**: detalle_medio=6.4 · detalle_min=2.3 · planos_pobres=1 · planos_calcados=0 · rachas_mismo_encuadre=1 · primer_fotograma_detalle=7.8 · rotulos_poco_contraste=0 · movimiento_primer_segundo=25.63
- **sonido**: efectos=100 · por_minuto=109 · tipos=13 · whoosh_min=7.6 · max_en_1s=4 · musica_db=-13
- **movimiento**: quieto_pct=2.0 · movimiento_medio=9.05 · bucle_diferencia=129.5
- **mezcla**: voz_rms=-20.5 · musica_bajo_voz_db=-9.5 · sfx_pico_frente_a_voz_db=-3.4 · sfx_rms_bajo_voz_db=-7.1 · efectos_que_tapan_voz=14

- ⚠ Ritmo poco variado (variación 0.42; mejor ≥ 0,45).
- ⚠ Menos de 3 micro planos (< 0,7 s): faltan golpes rápidos de detalle.
- ⚠ Planos pobres (casi sin dibujo: fondo liso con un objeto pequeño): plano 12 (15.1 s, detalle 2.3). Añade contexto o un sujeto más grande.
- ⚠ Mismo encuadre demasiado tiempo: 45.5–51.1 s (2 planos). Cambia de escala o de punto de vista.
- ℹ 7 rótulos entre y=1250 y y=1400: visibles en el feed normal, pero las guías de anuncios de las tres apps piden dejar libres ~660 px abajo (y≤1250). Si el texto es esencial, súbelo: «EL AIRE» (4.3 s, llega a y=1389); «UN INSTANTE» (12.2 s, llega a y=1389); «¡BUM!» (16.0 s, llega a y=1338); «SE ENFRÍA» (18.3 s, llega a y=1389); «TRUENO» (22.5 s, llega a y=1389); «LO MISMO» (23.6 s, llega a y=1389); «LEJOS DE LA TORMENTA» (45.5 s, llega a y=1290)
- ℹ El último fotograma no se parece al primero (diferencia 129/255): el vídeo no enlaza en bucle. Los bucles suben el % visto.
- ℹ En 14 momentos un efecto suena tan alto como la voz de ese instante (al mezclar, el motor los atenúa bajo la voz): 0.0 s, 1.8 s, 3.8 s, 6.5 s, 12.5 s, 15.0 s, 16.0 s, 22.5 s, 34.0 s, 41.0 s…
