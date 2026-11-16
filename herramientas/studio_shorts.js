// Lee de YouTube Studio lo que la API no da: «Se quedaron viendo» (lo contrario de deslizar), vistas y horas de cada Short.
// Uso (navegador integrado, con la sesión del canal): abrir https://studio.youtube.com, poner los ids en IDS, ejecutar,
// esperar ~7 s por vídeo y leer window.__st. Los resultados se apuntan en estadisticas/studio.json.
window.__st = {};
(async () => {
  const IDS = ['jQmhf8o1PfY'];
  for (const id of IDS) {
    history.pushState({}, '', '/video/' + id + '/analytics/tab-engagement/period-default');
    window.dispatchEvent(new PopStateEvent('popstate'));
    await new Promise(r => setTimeout(r, 6500));
    const t = document.body.innerText.replace(/\n{2,}/g, '\n');
    const i = t.indexOf('Métricas clave'), j = t.indexOf('Se quedaron viendo');
    window.__st[id] = { claves: t.slice(i, i + 230).replace(/\n/g, '|'), seQuedan: j > 0 ? t.slice(j - 12, j).replace(/\n/g, '|') : null };
  }
  window.__st.fin = true;
})(); 'lanzado'
