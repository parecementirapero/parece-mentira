# Control de calidad — v01

**Nota: 75/100**

- **ritmo**: planos=36 · cortes_min=38.2 · mediana=1.54 · min=0.52 · max=3.33 · variacion=0.38 · micro=3 · largos=10
- **rotulos**: total=19 · fuera_de_zona=0 · en_franja_dudosa=3 · sin_tiempo=0
- **gancho**: palabras_primera_frase=4 · voz_empieza=0.0 · fin_primera_frase=1.92 · palabras=156 · palabras_s=2.8 · acciones_primer_plano=1
- **imagen**: elementos_por_plano=4.5 · ilustraciones=22 · fondos_distintos=10 · mismo_fondo_max_s=10.8
- **imagen_real**: detalle_medio=5.9 · detalle_min=2.6 · planos_pobres=1 · planos_calcados=2 · rachas_mismo_encuadre=0 · primer_fotograma_detalle=5.2 · rotulos_poco_contraste=0 · movimiento_primer_segundo=4.29
- **sonido**: efectos=76 · por_minuto=81 · tipos=10 · whoosh_min=5.3 · max_en_1s=3 · musica_db=-13
- **movimiento**: quieto_pct=1.4 · movimiento_medio=5.35 · bucle_diferencia=10.3
- **mezcla**: voz_rms=-20.2 · musica_bajo_voz_db=-8.3 · sfx_pico_frente_a_voz_db=-7.9 · sfx_rms_bajo_voz_db=-16.6 · efectos_que_tapan_voz=3

- ⚠ Ritmo poco variado (variación 0.38; mejor ≥ 0,45).
- ⚠ Planos de más de 1 s con menos de 3 elementos: [2, 5, 17, 27, 30].
- ⚠ Poca densidad: 4.5 elementos por plano de media (la referencia tiene 7–8).
- ⚠ Planos pobres (casi sin dibujo: fondo liso con un objeto pequeño): plano 15 (23.0 s, detalle 2.6). Añade contexto o un sujeto más grande.
- ⚠ Planos casi iguales que el anterior (el corte no aporta nada nuevo): planos 5→6 (8.2 s), planos 7→8 (10.9 s)
- ℹ 3 rótulos entre y=1250 y y=1400: visibles en el feed normal, pero las guías de anuncios de las tres apps piden dejar libres ~660 px abajo (y≤1250). Si el texto es esencial, súbelo: «28000 KM/H» (9.7 s, llega a y=1388); «8 KM» (12.3 s, llega a y=1389); «¿POR QUÉ?» (14.7 s, llega a y=1338)
- ℹ Tramos de más de 4 s sin ningún efecto: 0.6 s (4.8 s), 5.3 s (4.4 s), 14.8 s (4.4 s)
- ℹ En 3 momentos un efecto suena tan alto como la voz de ese instante (al mezclar, el motor los atenúa bajo la voz): 42.2 s, 45.2 s, 55.2 s
