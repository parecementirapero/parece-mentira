// Hoja de fotogramas + cortes de un Short AJENO, para estudiarlo sin descargarlo (GUIA_CALIDAD §11, APRENDIZAJE.md).
// Uso (navegador integrado de Claude): abrir https://www.youtube.com/shorts/<ID>, ejecutar este archivo con
// javascript_tool y después hacer una captura: la página queda tapada por una hoja de 14 fotogramas con su segundo.
// Devuelve {dur, titulo, n_cortes, cortes}. Los cortes se detectan comparando miniaturas cada 0,25 s (umbral 28/255):
// en vídeo real con mucho movimiento cuenta de más; sirve para comparar órdenes de magnitud, no como cifra exacta.
(async function () {
  await new Promise(r => setTimeout(r, 3500));
  const v = [...document.querySelectorAll('video')].find(x => x.duration > 0 && x.videoWidth > 0);
  if (!v) return 'sin video';
  v.muted = true; v.pause();
  const D = v.duration;
  const seek = async t => {
    v.currentTime = t;
    await new Promise(r => { const f = () => { v.removeEventListener('seeked', f); r(); }; v.addEventListener('seeked', f); setTimeout(r, 1200); });
    await new Promise(r => setTimeout(r, 60));
  };
  const ts = [0.05, 0.6, 1.2, 2, 3, 4.5, 6, 8, D * 0.35, D * 0.5, D * 0.65, D * 0.8, D * 0.92, D - 0.3].filter(t => t < D);
  let c = document.getElementById('__c');
  if (!c) { c = document.createElement('canvas'); c.id = '__c'; c.style.cssText = 'position:fixed;left:0;top:0;z-index:999999;background:#000'; document.body.appendChild(c); }
  c.width = window.innerWidth; c.height = window.innerHeight;
  const cols = 7, rows = 2, w = Math.floor(c.width / cols), h = Math.floor(c.height / rows), g = c.getContext('2d');
  g.fillStyle = '#000'; g.fillRect(0, 0, c.width, c.height);
  for (let i = 0; i < ts.length; i++) {
    await seek(ts[i]); await new Promise(r => setTimeout(r, 200));
    const ar = v.videoWidth / v.videoHeight; let dh = h - 14, dw = dh * ar; if (dw > w) { dw = w; dh = dw / ar; }
    g.drawImage(v, (i % cols) * w + (w - dw) / 2, Math.floor(i / cols) * h + 14, dw, dh);
    g.fillStyle = '#ff0'; g.font = '11px sans-serif'; g.fillText(ts[i].toFixed(1) + 's', (i % cols) * w + 3, Math.floor(i / cols) * h + 11);
  }
  const s = document.createElement('canvas'); s.width = 27; s.height = 48;
  const sg = s.getContext('2d', { willReadFrequently: true });
  let prev = null; const cortes = []; const t0 = performance.now();
  for (let t = 0; t < D - 0.1 && performance.now() - t0 < 22000; t += 0.25) {
    await seek(t); sg.drawImage(v, 0, 0, 27, 48);
    const d = sg.getImageData(0, 0, 27, 48).data;
    if (prev) { let df = 0; for (let k = 0; k < d.length; k += 4) df += Math.abs(d[k] - prev[k]) + Math.abs(d[k + 1] - prev[k + 1]) + Math.abs(d[k + 2] - prev[k + 2]); if (df / (27 * 48 * 3) > 28) cortes.push(+t.toFixed(2)); }
    prev = d;
  }
  return { dur: D, titulo: document.title, n_cortes: cortes.length, cortes: JSON.stringify(cortes) };
})()
