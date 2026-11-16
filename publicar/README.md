# Publicar sin navegador

Solo se publica cuando una persona escribe **«ok»** en el chat del lote (ver `AGENTE.md`, punto 8).

| Red | Cómo | Estado |
|---|---|---|
| YouTube | `subir_youtube.py` por la API oficial (sin tocar nada) | ✅ listo, falta la puesta en marcha de abajo |
| TikTok | Navegador integrado; la persona solo elige el archivo en el selector | La API pública exige la auditoría de TikTok (las subidas de apps sin auditar salen en privado) |
| Instagram | Igual que TikTok | La API se podrá usar cuando esté verificada la cuenta de Meta |

## Puesta en marcha de YouTube (una vez)

1. **Permitir los dominios de Google en Claude** (lo hace quien administra la cuenta, como se hizo con `api.elevenlabs.io`):
   Ajustes de Claude → Capacidades → dominios permitidos → añadir `oauth2.googleapis.com` y `www.googleapis.com`.
2. **Dar permiso de subida**, en la Terminal de un Mac, desde la carpeta del canal:
   ```
   cd ~/Documents/"Parece Mentira"
   python3 estadisticas/autorizar.py --subir "$(grep ^YT_CLIENT_ID= claves.txt | cut -d= -f2-)" "$(grep ^YT_CLIENT_SECRET= claves.txt | cut -d= -f2-)"
   ```
   (coge solo el `CLIENT_ID` y el `CLIENT_SECRET` de las estadísticas que ya están en `claves.txt`). Entra con la cuenta del canal; si sale «Google no ha verificado esta aplicación» → Configuración avanzada → Ir a Parece Mentira Stats. El script guarda `YT_CLIENT_ID`, `YT_CLIENT_SECRET` y `YT_UPLOAD_REFRESH_TOKEN` en `claves.txt`.
3. **Copiar esas 3 líneas** al `claves.txt` del otro Mac (cada turno usa su propio ordenador).
4. Prueba sin subir nada: `python3 publicar/subir_youtube.py --claves claves.txt --metadatos <metadatos.json> --clave 01 --video <mp4> --prueba`.

## Cómo lo usa el agente

Por cada vídeo con «ok», en este orden: el 1 se publica ya y los demás se programan cada hora (`--publicar-en`, hora con zona, p. ej. `2026-11-17T12:00:00+01:00`). El script no duplica: si ya existe un vídeo con el mismo título en el canal, devuelve su enlace sin subir nada. La salida es una línea JSON con `url`, que va a `lotes/<lote>/estado.md`.

Ninguna clave entra en el repo ni en el chat.
