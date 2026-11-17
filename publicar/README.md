# Publicar sin navegador

Solo se publica cuando una persona escribe **«ok»** en el chat del lote (ver `AGENTE.md`, punto 8).

| Red | Cómo | Estado (2026-11-17) |
|---|---|---|
| YouTube | `subir_youtube.py`, API oficial. Publica del todo | ✅ en uso |
| Instagram | `subir_instagram.py`, API oficial de Meta. Publica el Reel del todo, con texto y portada (fotograma) | 🟡 código listo y probado en simulación. Falta la puesta en marcha de abajo (bloqueada por el registro en Meta for Developers) |
| TikTok | `subir_tiktok.py`, API oficial. Deja el vídeo como **borrador en la bandeja de entrada**; una persona lo termina en el móvil (pegar texto → Publicar) | 🟡 código listo y probado en simulación. Falta la puesta en marcha y **una prueba real** que decide si se usa (ver «Lo que no se sabe») |

Mientras una red no esté puesta en marcha, se sigue publicando en ella desde el navegador integrado como hasta ahora.

Todo es gratis: ni TikTok ni Meta cobran por estas API. No hace falta ningún servicio de terceros.

## Por qué TikTok no puede ser 100 % automático

TikTok tiene dos modos de API:

- **Direct Post** (publica del todo): a una app sin auditar solo le deja publicar en privado («Solo yo») y en cuentas privadas. Para quitar el límite hay que pasar una auditoría, y sus normas dicen expresamente que **no aceptan herramientas de uso interno** para subir contenido a cuentas propias. O sea: para nosotros, cerrado.
- **Upload** (borrador a la bandeja): no pasa por esa auditoría. El vídeo llega al móvil como notificación y la persona lo publica desde la app. El texto **no** viaja con el vídeo: hay que pegarlo. Es lo que hace `subir_tiktok.py`.

Fuentes: [Content Sharing Guidelines](https://developers.tiktok.com/docs/en/content-sharing-guidelines), [Upload](https://developers.tiktok.com/docs/en/content-posting-api-reference-upload-video), [Sandbox](https://developers.tiktok.com/docs/en/add-a-sandbox).

Qué se gana frente al navegador: no hace falta un Mac con la sesión de TikTok abierta ni elegir el archivo en el selector; el «ok» se puede dar desde cualquier sitio y se termina en el móvil en unos 20 segundos por vídeo. Qué se pierde: Claude ya no pone el texto ni la portada; los pone la persona en el móvil.

## Lo que no se sabe todavía (hay que probarlo una vez)

1. **¿Deja TikTok publicar en público un borrador enviado desde una app en sandbox?** La documentación oficial solo limita Direct Post y dice que el sandbox «no da acceso a la Content Posting API para vídeos públicos», sin aclarar si eso incluye los borradores. Varias guías de terceros dicen que los borradores no tienen ese límite. Se sabe en 5 minutos con la prueba del paso 9 de TikTok. Si no deja: TikTok se queda en el navegador y `subir_tiktok.py` no se usa.
2. **Nada de esto se ha ejecutado contra TikTok ni Meta de verdad**: no había cuentas de desarrollador listas ni red hacia ellas desde donde se escribió. Está probado contra un simulador hecho siguiendo la documentación oficial (`python3 publicar/prueba.py`, 31 pruebas). La primera ejecución real puede destapar algún detalle.
3. Los nombres de los menús de Meta for Developers cambian a menudo. Si un paso no coincide con lo que ves, para y pregúntalo en el chat con una captura.

## Antes de nada: dominios permitidos en Claude

Igual que se hizo con `api.elevenlabs.io` (Ajustes de Claude → Capacidades → dominios permitidos), añadir:

- TikTok: `open.tiktokapis.com` y `open-upload.tiktokapis.com` (si el script dice que TikTok ha devuelto otra dirección de subida, añadir esa: puede ser regional)
- Instagram: `graph.facebook.com` y `rupload.facebook.com` (y `graph.instagram.com` si se usa la opción B)

## Los scripts van juntos

`subir_tiktok.py`, `subir_instagram.py` y los dos `autorizar_*.py` necesitan `base.py` al lado. Al copiar del repo a la carpeta local del turno se copia **la carpeta `publicar/` entera**.

---

## Instagram — puesta en marcha (una vez, ~30 min)

Requisito previo que hoy bloquea: tener una cuenta de **Meta for Developers** (en `TASKS.md` está a medias: falta verificar el móvil en la cuenta de Facebook de Jorge).

Hay dos opciones. **La A es la recomendada**: sube el archivo desde el Mac. La B (la app de las estadísticas, «Instagram Login») obliga a que el vídeo esté antes en una dirección pública de internet, y no tenemos dónde alojarlo.

### Opción A — subida directa (Facebook Login)

1. **Cuenta profesional.** @parecementiramedia tiene que ser profesional (creador o empresa; valen las dos).
2. **Página de Facebook enlazada.** Con la cuenta de Facebook que va a dar el permiso (la de Jorge): crear una página «Parece Mentira» y enlazarla. En Instagram (móvil): Editar perfil → Página → Conectar o crear. La cuenta de Facebook tiene que ser administradora de esa página.
3. **App de Meta.** En https://developers.facebook.com → Mis apps → Crear app, de tipo **Negocio** (Business). Nombre `Parece Mentira Publicar`. Puede quedarse en modo desarrollo: para publicar en una cuenta propia no hace falta revisión de Meta (acceso estándar).
4. **Token corto.** Abrir el [Explorador de la API Graph](https://developers.facebook.com/tools/explorer/). Elegir la app. En «Usuario o página» → **Token de usuario**. Añadir estos permisos: `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement` (y `business_management` si la página está dentro de un portfolio empresarial). Pulsar **Generate Access Token** y, en la ventana que sale, **marcar la página y la cuenta de Instagram**. Copiar el token (dura 1–2 horas: seguir sin parar).
5. **Identificador y clave secreta de la app**: en la app → Configuración → Básica.
6. **Guardar el permiso** (terminal del Mac, en la carpeta local del canal):
   ```
   cd ~/Documents/"Parece Mentira"
   python3 publicar/autorizar_instagram.py --claves claves.txt
   ```
   Pide el identificador, la clave secreta y el token (los dos últimos no se ven al pegarlos). Convierte el token en uno de página que no caduca y guarda `IG_USER_ID`, `IG_FB_TOKEN`, `IG_APP_ID`, `IG_APP_SECRET` en `claves.txt`.
7. **Prueba sin publicar nada:**
   ```
   python3 publicar/subir_instagram.py --claves claves.txt --metadatos <metadatos.json> --clave 01 --video <mp4> --prueba
   ```
   Tiene que decir `"ok": true`, la cuenta `parecementiramedia` y el cupo (`0/100` o parecido).
8. **Copiar** las líneas `IG_*` al `claves.txt` del otro Mac (este token sí se puede compartir: no cambia al usarse).

El token deja de valer si se cambia la contraseña de esa cuenta de Facebook o si deja de ser administradora de la página. Entonces se repiten los pasos 4–6.

### Opción B — con dirección pública (Instagram Login)

En `claves.txt`: `IG_TOKEN=<token de 60 días>` generado como en `estadisticas/README.md` («Instagram»), añadiendo antes el permiso `instagram_business_content_publish`. Cada vez hay que pasar `--video-url https://…mp4` con el mismo vídeo en una dirección https pública y directa. El script alarga el token cada semana.

---

## TikTok — puesta en marcha (una vez por Mac, ~20 min)

El permiso de TikTok **cambia cada vez que se usa**. Por eso no se puede compartir entre el Mac de Nico, el de Jorge y las estadísticas: cada uno necesita su propio sandbox (cada sandbox tiene su propio Client key). La app admite hasta 5 sandbox.

1. Entrar en https://developers.tiktok.com con la cuenta del canal → **Manage apps** → la app `Parece Mentira Stats`.
2. Arriba, en el selector de **Sandbox**, crear uno nuevo clonando el de las estadísticas. Nombre: `Publicar Nico` (y, cuando toque, `Publicar Jorge`).
3. En ese sandbox: **Add products → Content Posting API**. **No** activar «Direct Post».
4. **Login Kit**: plataforma **Desktop** y Redirect URI `http://127.0.0.1:*/callback/` (si se clonó, ya está).
5. **Scopes**: `user.info.basic` y `video.upload`.
6. **Sandbox settings → Target users → Add account** → `parece.mentira85`. Pulsar **Apply changes**. (La cuenta puede tardar hasta una hora en aparecer.)
7. Copiar el **Client key** y el **Client secret** de ese sandbox y, en la terminal del Mac:
   ```
   cd ~/Documents/"Parece Mentira"
   python3 publicar/autorizar_tiktok.py --claves claves.txt
   ```
   Entrar con **parece.mentira85** y aceptar los dos permisos. Lo guarda todo en `claves.txt` (`TIKTOK_PUB_*`).
8. **Prueba sin subir nada:** `python3 publicar/subir_tiktok.py --claves claves.txt --metadatos <metadatos.json> --clave 01 --video <mp4> --prueba` → `"ok": true`.
9. **La prueba real que decide** (con un vídeo que ya tenga «ok», o uno cualquiera que luego se descarta): el mismo comando sin `--prueba`. Debe decir `"estado": "en_bandeja"`. En el móvil: TikTok → Bandeja de entrada → notificación → se abre el editor. Mirar **si en «Quién puede ver este vídeo» deja elegir «Todo el mundo»**.
   - Si deja: TikTok por borrador funciona. Apuntarlo en `DECISIONS.md` y decidir si se usa.
   - Si solo deja «Solo yo»: no sirve. Descartar el borrador, apuntarlo en `DECISIONS.md` y seguir con el navegador.

Límites de TikTok: como mucho **5 borradores pendientes** (enviados y sin publicar) en 24 h, así que hay que publicarlos al llegar; 6 envíos por minuto. El permiso dura entre 6 y 12 meses (TikTok da la fecha y el script avisa 20 días antes); para renovarlo se repite el paso 7.

---

## Cómo lo usa el agente (tras el «ok»)

Desde `device_bash`, en la carpeta local del turno, por cada vídeo aprobado:

```
python3 publicar/subir_instagram.py --claves claves.txt --metadatos lotes/<lote>/metadatos.json --clave 01 --video lotes/<lote>/<archivo>.mp4 --comentario
python3 publicar/subir_tiktok.py    --claves claves.txt --metadatos lotes/<lote>/metadatos.json --clave 01 --video lotes/<lote>/<archivo>.mp4
```

- Cada comando imprime **una línea JSON**. `"ok": true` con `url` (Instagram) o `"estado": "en_bandeja"` con `texto` (TikTok: ese texto se manda al chat para que la persona lo pegue en el móvil). `"ok": false` trae `error` en castellano con lo que hay que hacer.
- **No duplican.** Apuntan cada paso en `publicado.json`, junto a `metadatos.json`. Si se repite el comando, retoma el envío o contesta `"yaEstaba": true`. Instagram además mira los últimos Reels de la cuenta por si ya está. `--forzar` se salta la protección (solo tras comprobar en la red a mano).
- `"estado": "procesando"`: la red aún está procesando el vídeo. Repetir el mismo comando un minuto después; no sube otro.
- TikTok, después de que la persona publique: `subir_tiktok.py … --estado` devuelve el enlace del vídeo.
- Al terminar, copiar `publicado.json` a `lotes/<lote>/` del repo en el mismo commit que `estado.md`.
- Instagram: la portada es el fotograma `portada.t` de `metadatos.json`. La imagen `portada.jpg` solo se puede poner por API si está en una dirección pública (`--portada-url`); si se quiere esa imagen, se cambia a mano en la app. El comentario se escribe pero la API no deja fijarlo.

## Pruebas

```
python3 publicar/prueba.py
```

Sin red y sin claves: levanta un servidor falso que imita a TikTok y a Meta y lanza los scripts de verdad contra él (tokens que rotan, subida por trozos, reintentos, límites, respuestas perdidas, no duplicar). Pasarlo siempre que se toque algo de `publicar/`.

---

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

## Cómo lo usa el agente (YouTube)

Por cada vídeo con «ok», en este orden: el 1 se publica ya y los demás se programan cada hora (`--publicar-en`, hora con zona, p. ej. `2026-11-17T12:00:00+01:00`). El script no duplica: si ya existe un vídeo con el mismo título en el canal, devuelve su enlace sin subir nada. La salida es una línea JSON con `url`, que va a `lotes/<lote>/estado.md`.

Ninguna clave entra en el repo ni en el chat.
