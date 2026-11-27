# Control de calidad — v03

**Nota: 70/100**

- **ritmo**: planos=27 · cortes_min=30.5 · mediana=1.76 · min=0.92 · max=3.76 · variacion=0.36 · micro=0 · largos=12
- **rotulos**: total=22 · fuera_de_zona=0 · en_franja_dudosa=1 · sin_tiempo=0
- **gancho**: palabras_primera_frase=5 · voz_empieza=0.0 · fin_primera_frase=1.6 · palabras=153 · palabras_s=2.92 · acciones_primer_plano=2
- **imagen**: elementos_por_plano=4.6 · ilustraciones=27 · fondos_distintos=4 · mismo_fondo_max_s=9.0
- **imagen_real**: detalle_medio=7.0 · detalle_min=3.3 · planos_pobres=0 · planos_calcados=0 · rachas_mismo_encuadre=3 · primer_fotograma_detalle=7.0 · rotulos_poco_contraste=0 · movimiento_primer_segundo=7.4
- **sonido**: efectos=50 · por_minuto=57 · tipos=7 · whoosh_min=0.0 · max_en_1s=3 · musica_db=-13
- **movimiento**: quieto_pct=4.4 · movimiento_medio=4.35 · bucle_diferencia=4.0
- **mezcla**: voz_rms=-20.5 · musica_bajo_voz_db=-8.9 · sfx_pico_frente_a_voz_db=-5.3 · sfx_rms_bajo_voz_db=-13.3 · efectos_que_tapan_voz=6

- ⚠ Ritmo poco variado (variación 0.36; mejor ≥ 0,45).
- ⚠ Menos de 3 micro planos (< 0,7 s): faltan golpes rápidos de detalle.
- ⚠ Planos de más de 1 s con menos de 3 elementos: [13, 17].
- ⚠ Poca densidad: 4.6 elementos por plano de media (la referencia tiene 7–8).
- ⚠ Pocos fondos distintos (4) para 53 s.
- ⚠ Mismo encuadre demasiado tiempo: 18.1–22.7 s (2 planos), 39.5–44.1 s (2 planos), 46.7–53.1 s (2 planos). Cambia de escala o de punto de vista.
- ℹ 1 rótulos entre y=1250 y y=1400: visibles en el feed normal, pero las guías de anuncios de las tres apps piden dejar libres ~660 px abajo (y≤1250). Si el texto es esencial, súbelo: «ALERTA» (32.6 s, llega a y=1389)
- ℹ En 6 momentos un efecto suena tan alto como la voz de ese instante (al mezclar, el motor los atenúa bajo la voz): 4.0 s, 8.0 s, 21.2 s, 22.8 s, 31.2 s, 35.0 s
