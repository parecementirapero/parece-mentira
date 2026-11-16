# Estadísticas del canal

Web con las estadísticas de YouTube de Parece Mentira. Se actualiza sola cada mañana antes de las 9:00 (hora de Madrid), en la nube y sin ningún Mac encendido.

```
estadisticas/
  recoger.py         saca los datos de YouTube (Data API + Analytics API) -> datos/data.json
  construir.py       mete los datos en plantilla.html -> web/index.html (una sola página)
  plantilla.html     la web: Resumen, Vídeos (con ficha), Laboratorio, Mejores horas
  etiquetas.json     etiquetas a mano por vídeo (tema, voz, gancho…), para el Laboratorio
  autorizar.py       autorización de Google, UNA vez, desde un Mac
  datos/data.json    datos reales (lo escribe GitHub Actions; se versiona = histórico)
  web/index.html     la web construida (lo escribe GitHub Actions)
  ejemplo/           datos inventados para probar la web sin conexión a YouTube
.github/workflows/estadisticas.yml   el trabajo diario
```

Coste: 0 €. GitHub Actions usa ~1 minuto al día de los 2.000 gratis al mes. Las APIs de YouTube son gratis, y el consumo diario se queda muy por debajo de la cuota.

## Qué sale de dónde

| Dato | Fuente | Retraso |
|---|---|---|
| Vistas, likes, comentarios | YouTube Data API | al momento |
| % medio visto, curva de retención, siguen a los 3 s | YouTube Analytics | 48–72 h (antes sale «pendiente») |
| Compartidos, suscriptores por vídeo, fuentes de tráfico, vistas por día | YouTube Analytics | 1–3 días |
| Tema y lote (etiquetas automáticas) | hashtags de la descripción y `lotes/*/estado.md` | — |

Solo salen los vídeos **públicos**.

## Puesta en marcha (una sola vez, ~15 min)

### 1. Proyecto de Google Cloud
1. Abre https://console.cloud.google.com con **parecementirapero.media@gmail.com** (la cuenta dueña del canal).
2. Arriba, selector de proyecto → **Proyecto nuevo** → nombre `parece-mentira-stats` → Crear. Comprueba que queda seleccionado.
3. Menú → **APIs y servicios → Biblioteca**. Busca y pulsa **Habilitar** en:
   - `YouTube Data API v3`
   - `YouTube Analytics API`

### 2. Pantalla de consentimiento
1. Menú → **APIs y servicios → Pantalla de consentimiento de OAuth** (puede llamarse «Google Auth Platform») → Empezar.
2. Nombre de la app: `Parece Mentira Stats`. Correo de asistencia: el del proyecto. Público: **Externo**. Contacto: el del proyecto. Crear.
3. En **Público**, pulsa **Publicar app** para pasarla a **En producción**.
   ⚠️ Si se queda en «Prueba», el permiso caduca cada 7 días y la web deja de actualizarse.
   No hace falta la verificación de Google, porque solo la usáis vosotros.

### 3. Credencial
1. **Clientes** (o «Credenciales») → **Crear cliente** → tipo **Aplicación de escritorio** → nombre `stats` → Crear.
2. Copia el **ID de cliente** y el **Secreto de cliente**. No los pegues en el repo ni en el chat.

### 4. Autorizar (en la terminal del Mac, dentro de la carpeta del repo)
```bash
git pull
python3 estadisticas/autorizar.py "ID_DE_CLIENTE" "SECRETO_DE_CLIENTE"
```
1. Se abre el navegador. Entra con **parecementirapero.media@gmail.com**. Si te pide elegir canal, elige **Parece Mentira**.
2. Saldrá «Google no ha verificado esta aplicación». Es normal, porque la app es vuestra: **Configuración avanzada → Ir a Parece Mentira Stats**.
3. Marca los dos permisos (ver YouTube y ver informes de YouTube Analytics) → Continuar.
4. La terminal muestra un **refresh token** largo. Cópialo.

### 5. Secretos en GitHub
Ve a https://github.com/parecementirapero/parece-mentira → **Settings → Secrets and variables → Actions → New repository secret**, y crea estos tres:

| Nombre | Valor |
|---|---|
| `YT_CLIENT_ID` | ID de cliente |
| `YT_CLIENT_SECRET` | Secreto de cliente |
| `YT_REFRESH_TOKEN` | el token del paso 4 |

### 6. Primera ejecución
Pestaña **Actions** → **Estadísticas del canal** → **Run workflow**. Si termina en verde, aparece un commit «estadísticas: actualización …» con `datos/data.json` y `web/index.html`.

## Cómo verla
- **En el Mac:** `git pull` y abre `estadisticas/web/index.html` en el navegador. Funciona sin internet.
- **En Claude:** página «Parece Mentira · Estadísticas» (sale en la lista de artifacts de la cuenta, compartida por Nico y Jorge). Se vuelve a publicar con el `web/index.html` del repo.

## Probar sin YouTube
```bash
python3 estadisticas/ejemplo/generar.py      # datos inventados
python3 estadisticas/construir.py --ejemplo  # web con esos datos
open estadisticas/web/index.html
```
No hagas commit de una `web/index.html` construida con `--ejemplo` si ya hay datos reales. Si pasa, la siguiente ejecución diaria la vuelve a dejar bien.

## Problemas
- **`invalid_grant`** en Actions: el permiso ha caducado o se ha quitado. Repite el paso 4 y actualiza `YT_REFRESH_TOKEN`. Si pasa cada 7 días, la app sigue en «Prueba» (paso 2.3).
- **Todo «pendiente»**: los vídeos tienen menos de 48 h. Espera.
- **Falta un vídeo**: no es público.
- **Etiquetas mal**: corrígelas en `etiquetas.json`. Se aplican en la siguiente actualización, o al lanzar el workflow a mano.
