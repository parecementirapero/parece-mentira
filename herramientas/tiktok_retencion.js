// Lee de TikTok Studio lo que su API no da: tiempo medio, % que ve el vídeo entero y la curva de retención.
// Uso (navegador integrado con la sesión de TikTok): abrir https://www.tiktok.com/tiktokstudio/analytics/<id del vídeo>,
// ejecutar este archivo y esperar ~35 s. La curva se lee del rótulo «0:12 (38%)» que TikTok va actualizando mientras se
// reproduce la vista previa; si sale vacía, hay que pulsar a mano el botón de reproducir de la vista previa y repetir.
// Los vídeos en «Solo yo» no dan estadísticas. Resultados → estadisticas/tiktok_studio.json
(async () => {
  for (let k = 0; k < 30 && !/Tasa de retención/.test(document.body.innerText); k++) await new Promise(r => setTimeout(r, 500));
  const el = [...document.querySelectorAll('*')].find(e => e.children.length === 0 && /Tasa de retención/.test(e.textContent));
  if (el) el.scrollIntoView({ block: 'start' });
  let v = null;
  for (let k = 0; k < 20 && !(v = document.querySelector('video')); k++) await new Promise(r => setTimeout(r, 400));
  await new Promise(r => setTimeout(r, 1500));
  const t = document.body.innerText.replace(/\n{2,}/g, '\n');
  const g = re => (t.match(re) || [])[1];
  const res = { vistas: g(/Visualizaciones del vídeo\n([\d.,KM]+)/), medio: g(/Tiempo promedio de visualización\n([\d.,]+s)/), completo: g(/Vieron el vídeo completo\n([\d.,]+%)/) };
  const ret = {};
  if (v) {
    v.muted = true; v.currentTime = 0; v.playbackRate = 3; await v.play().catch(() => {});
    const t0 = Date.now();
    while (Date.now() - t0 < 22000) {
      const m = document.body.innerText.match(/(\d):(\d\d)\s*\((\d+)\s*%\)/);
      if (m) ret[+m[1] * 60 + +m[2]] = +m[3];
      await new Promise(r => setTimeout(r, 90));
    }
    res.dur = Math.round(v.duration);
  }
  res.curva = ret;
  return res;
})()
