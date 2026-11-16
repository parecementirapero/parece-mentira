# Estadísticas del canal

Web con las estadísticas de Parece Mentira en **YouTube, TikTok e Instagram**. Se actualiza sola cada mañana antes de las 9:00 (hora de Madrid), en la nube y sin ningún Mac encendido.

```
estadisticas/
  recoger.py         junta las tres redes -> datos/data.json (YouTube: Data API + Analytics API)
  tiktok.py          TikTok (Display API)
  instagram.py       Instagram (Reels, Instagram API with Instagram Login)
  comun.py           HTTP con reintentos y guardado de tokens renovados
  construir.py       mete los datos en plantilla.html -> web/index.html (una sola página)
  plantilla.html     la web: Resumen, Redes, Vídeos (con ficha), Laboratorio, Mejores horas
  etiquetas.json     etiquetas a mano por vídeo (tema, voz, gancho…), para el Laboratorio
  autorizar.py       autorización de Google, UNA vez, desde un Mac
  autorizar_tiktok.py  autorización de TikTok desde un Mac (cada ~6 meses)
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

| TikTok: vistas, likes, comentarios, compartidos, seguidores | TikTok Display API | al momento |
| Instagram: vistas, alcance, likes, comentarios, compartidos, guardados, tiempo medio visto, tasa de salto | Instagram Insights | horas |
| Vistas por día en TikTok e Instagram | foto diaria guardada en `data.json` (`historico`) | empieza el día que se conecta cada red |
| Mismo vídeo en las 3 redes | enlaces de `lotes/*/estado.md`; si no, fecha ±1 día y título parecido; a mano en `etiquetas.json` | — |

Solo salen los vídeos **públicos**. **TikTok no da retención** por API: la curva y el «% visto» solo están en TikTok Studio.
Cada red es independiente. Si falta una o falla un día, se conservan sus últimos datos y la web lo avisa abajo.

## Puesta en marcha de YouTube (una sola vez, ~15 min)

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

### 7. Token de GitHub para renovar permisos (TikTok e Instagram)
TikTok cambia su token cada vez que se usa, e Instagram lo renueva cada lunes. El trabajo diario guarda el token nuevo en los secretos y para eso necesita un token de GitHub:
1. Con la cuenta de GitHub del proyecto, entra en https://github.com/settings/personal-access-tokens/new (*fine-grained token*).
2. Nombre `estadisticas`. Caducidad: la máxima que deje. Apunta la fecha en `TASKS.md`.
3. **Repository access → Only select repositories →** `parece-mentira`.
4. **Permissions → Repository permissions → Secrets → Read and write**. Nada más.
5. Generar → copia el token → secreto `GH_PAT`.

## TikTok (~20 min)
1. Entra en https://developers.tiktok.com con la cuenta de TikTok del canal (**parece.mentira85**) → **Manage apps → Connect an app**. Nombre: `Parece Mentira Stats`.
2. Arriba, cambia a **Sandbox** y crea uno. Para uso propio no hace falta pasar la revisión de TikTok: en sandbox solo pueden entrar las cuentas que añadáis.
3. **Add products → Login Kit**. En Login Kit, marca la plataforma **Desktop** y añade esta Redirect URI:
   `http://127.0.0.1:*/callback/`
4. **Scopes**: `user.info.basic`, `user.info.stats`, `video.list`.
5. **Sandbox settings → Target users → Add account** → `parece.mentira85`.
6. Copia el **Client key** y el **Client secret** del sandbox.
7. En la terminal del Mac, dentro del repo:
   ```bash
   git pull
   python3 estadisticas/autorizar_tiktok.py "CLIENT_KEY" "CLIENT_SECRET"
   ```
   Entra con **parece.mentira85**, marca los 3 permisos y acepta. La terminal muestra el token.
8. Secretos en GitHub: `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET` y `TIKTOK_REFRESH_TOKEN`.
9. Lanza el workflow a mano (paso 6).

⚠️ El permiso de TikTok dura unos 180 días desde que se autoriza. La web avisa 20 días antes. Entonces se repite el paso 7 y se actualiza `TIKTOK_REFRESH_TOKEN`.
Si la web dice «no se pudo guardar el token renovado», revisa `GH_PAT`: sin él, TikTok deja de funcionar al día siguiente.

## Instagram (~15 min)
1. La cuenta **@parecementiramedia** tiene que ser **profesional** (creador o empresa). En la app: Configuración → Tipo de cuenta y herramientas → Cambiar a cuenta profesional → Creador.
2. Entra en https://developers.facebook.com. Hace falta una cuenta de Facebook, puede ser la tuya personal. **Mis apps → Crear app**. Caso de uso: **Gestionar mensajes y contenido en Instagram**. Tipo: Negocio. Nombre: `Parece Mentira Stats`.
3. En la app: **Instagram → Configuración de la API con inicio de sesión de Instagram**. En **Permisos**, comprueba que están `instagram_business_basic` e `instagram_business_manage_insights`.
4. **Generar identificadores de acceso → Añadir cuenta** → entra con **@parecementiramedia** → Permitir.
5. **Generar token** → cópialo. Solo se enseña una vez. Es un token de 60 días.
6. Secreto en GitHub: `IG_TOKEN`.
7. Lanza el workflow a mano (paso 6).

La app puede quedarse en «Desarrollo»: no hace falta revisión de Meta para leer vuestra propia cuenta. El token se renueva solo cada lunes. Si se pasan 60 días sin renovarse (por ejemplo, por fallos seguidos), se repiten los pasos 4–6.

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
- **Un vídeo sale separado en dos redes** (no se ha unido): añádelo a `etiquetas.json` con su id de YouTube y `"tiktok": "<número del vídeo>"` y/o `"instagram": "<código del reel>"`.
- **TikTok `invalid_grant`**: el permiso ha caducado o se perdió el token renovado. Repite el paso 7 de TikTok.
- **Instagram `OAuthException` / código 190**: el token ha caducado. Repite los pasos 4–6 de Instagram.
- **Etiquetas mal**: corrígelas en `etiquetas.json`. Se aplican en la siguiente actualización, o al lanzar el workflow a mano.
