#!/usr/bin/env python3
"""Pruebas de publicar/subir_tiktok.py y publicar/subir_instagram.py SIN red y sin claves reales.

Levanta en 127.0.0.1 un servidor que imita las API de TikTok y de Meta (con sus reglas: tokens que rotan,
trozos de subida, estados, límites) y lanza los scripts de verdad contra él. No publica nada en ningún sitio.

  python3 publicar/prueba.py        → tarda unos segundos; termina con «TODO BIEN» o con la lista de fallos.

Pasarlo siempre que se toque algo de publicar/ (igual que motor.prueba con el motor).
"""
import hashlib, http.server, json, os, shutil, struct, subprocess, sys, tempfile, threading, urllib.parse

AQUI = os.path.dirname(os.path.abspath(__file__))
MB = 1024 * 1024
TEXTO = "Este plátano es radiactivo (y tú también) 🍌☢️ Un dato «raro». #ciencia #parecementira"


class Mundo:
    """Estado del servidor falso. Cada prueba lo reinicia."""

    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self.n = 0
        self.refresh = "rft.0"
        self.acceso = None
        self.permisos = "user.info.basic,video.upload"
        self.tt_inits, self.tt_subidas, self.tt_error_init = [], {}, None
        self.tt_estados = ["PROCESSING_UPLOAD", "SEND_TO_USER_INBOX"]
        self.tt_fallo, self.tt_post_ids = None, []
        self.tt_put_503 = 0
        self.ig_contenedores, self.ig_publicados, self.ig_subidas, self.ig_comentarios = {}, [], {}, []
        self.ig_estados = ["IN_PROGRESS", "FINISHED"]
        self.ig_medios, self.ig_cupo = [], 3
        self.ig_token_malo = False
        self.ig_publicar_pierde_respuesta = False
        self.ig_refrescos = 0
        self.ig_permisos_token = ["instagram_basic", "instagram_content_publish", "pages_show_list", "pages_read_engagement"]
        self.peticiones = []


M = Mundo()


class Falso(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def _fin(self, estado, cuerpo, cabeceras=None):
        datos = json.dumps(cuerpo).encode() if not isinstance(cuerpo, bytes) else cuerpo
        self.send_response(estado)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(datos)))
        for k, v in (cabeceras or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(datos)

    def _cuerpo(self):
        return self.rfile.read(int(self.headers.get("Content-Length") or 0))

    def _ruta(self):
        u = urllib.parse.urlparse(self.path)
        return u.path, {k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()}

    def _tt_error(self, estado, codigo):
        self._fin(estado, {"data": {}, "error": {"code": codigo, "message": codigo, "log_id": "L1"}})

    def _tt_autorizado(self):
        if self.headers.get("Authorization") != f"Bearer {M.acceso}" or M.acceso is None:
            self._tt_error(401, "access_token_invalid")
            return False
        return True

    def _ig_error(self, codigo, sub=None, estado=400):
        self._fin(estado, {"error": {"message": f"error {codigo}", "type": "OAuthException", "code": codigo,
                                     "error_subcode": sub, "fbtrace_id": "T1"}})

    # ------------------------------------------------------------------ GET
    def do_GET(self):
        ruta, q = self._ruta()
        M.peticiones.append(("GET", ruta))
        if ruta == "/v2/user/info/":
            if self._tt_autorizado():
                self._fin(200, {"data": {"user": {"open_id": "o1", "display_name": "Parece Mentira"}}, "error": {"code": "ok"}})
            return
        if ruta.startswith(("/fb/", "/ig/")):
            modo, resto = ruta[1:3], ruta[4:]
            bueno = "TOKENFB" if modo == "fb" else f"TOKENIG{M.ig_refrescos or ''}"
            if resto == "refresh_access_token":
                M.ig_refrescos += 1
                return self._fin(200, {"access_token": f"TOKENIG{M.ig_refrescos}", "expires_in": 5184000})
            if modo == "fb" and resto == "debug_token":       # lo que usa autorizar_instagram.py
                if q.get("access_token") != "APP1|SECRETO":
                    return self._ig_error(190)
                corto = q.get("input_token") == "CORTO"
                return self._fin(200, {"data": {"is_valid": q.get("input_token") in ("CORTO", "TOKENFB"), "expires_at": 1 if corto else 0,
                                                "scopes": M.ig_permisos_token}})
            if modo == "fb" and resto == "oauth/access_token":
                if (q.get("fb_exchange_token"), q.get("client_id"), q.get("client_secret")) != ("CORTO", "APP1", "SECRETO"):
                    return self._ig_error(190)
                return self._fin(200, {"access_token": "LARGO", "token_type": "bearer", "expires_in": 5183944})
            if modo == "fb" and resto == "me/accounts" and q.get("access_token") == "LARGO":
                return self._fin(200, {"data": [
                    {"name": "Otra página", "access_token": "TOKENOTRA", "id": "1"},
                    {"name": "Parece Mentira", "access_token": "TOKENFB", "id": "2",
                     "instagram_business_account": {"id": "999", "username": "parecementiramedia"}}]})
            if M.ig_token_malo or q.get("access_token") != bueno:
                return self._ig_error(190)
            if resto == "me":
                return self._fin(200, {"user_id": "999", "username": "parecementiramedia"})
            if resto in ("999",):
                return self._fin(200, {"username": "parecementiramedia", "id": "999"})
            if resto == "999/content_publishing_limit":
                return self._fin(200, {"data": [{"quota_usage": M.ig_cupo, "config": {"quota_total": 100, "quota_duration": 86400}}]})
            if resto == "999/media":
                return self._fin(200, {"data": M.ig_medios})
            if resto in M.ig_contenedores:
                c = M.ig_contenedores[resto]
                if c["publicado"]:
                    return self._fin(200, {"status_code": "PUBLISHED", "id": resto})
                if modo == "fb" and not c.get("subido") and not c.get("video_url"):
                    return self._fin(200, {"status_code": "IN_PROGRESS", "id": resto})
                c["consultas"] += 1
                est = M.ig_estados[min(c["consultas"] - 1, len(M.ig_estados) - 1)]
                return self._fin(200, {"status_code": est, "status": "Error: 2207026 formato" if est == "ERROR" else est, "id": resto})
            for m in M.ig_medios:
                if m["id"] == resto:
                    return self._fin(200, {"permalink": m["permalink"], "shortcode": "ABC", "id": resto})
        self._fin(404, {"error": {"message": "no existe", "code": 24}})

    # ------------------------------------------------------------------ POST
    def do_POST(self):
        ruta, q = self._ruta()
        cuerpo = self._cuerpo()
        M.peticiones.append(("POST", ruta))
        if ruta == "/v2/oauth/token/":
            f = {k: v[0] for k, v in urllib.parse.parse_qs(cuerpo.decode()).items()}
            if f.get("grant_type") == "authorization_code":      # lo que usa autorizar_tiktok.py
                if f.get("code") != "CODIGO" or len(f.get("code_verifier", "")) < 43 or not f.get("redirect_uri", "").startswith("http://127.0.0.1:"):
                    return self._fin(400, {"error": "invalid_grant", "error_description": "código malo", "log_id": "L0"})
                M.refresh, M.acceso = "rft.nuevo", "act.nuevo"
                return self._fin(200, {"access_token": M.acceso, "expires_in": 7200, "refresh_token": M.refresh,
                                       "refresh_expires_in": 180 * 86400, "scope": M.permisos, "open_id": "o1", "token_type": "Bearer"})
            if f.get("refresh_token") != M.refresh or f.get("client_key") != "CK" or f.get("client_secret") != "CS":
                return self._fin(400, {"error": "invalid_grant", "error_description": "Refresh token is invalid or expired.", "log_id": "L0"})
            M.n += 1
            M.refresh, M.acceso = f"rft.{M.n}", f"act.{M.n}"
            return self._fin(200, {"access_token": M.acceso, "expires_in": 7200, "refresh_token": M.refresh,
                                   "refresh_expires_in": 180 * 86400, "scope": M.permisos, "open_id": "o1", "token_type": "Bearer"})
        if ruta == "/v2/post/publish/inbox/video/init/":
            if not self._tt_autorizado():
                return
            if "video.upload" not in M.permisos:
                return self._tt_error(401, "scope_not_authorized")
            if M.tt_error_init:
                return self._tt_error(403, M.tt_error_init)
            s = json.loads(cuerpo)["source_info"]
            tam, trozo, total = s["video_size"], s["chunk_size"], s["total_chunk_count"]
            # reglas de la guía de transferencia de TikTok
            valido = s["source"] == "FILE_UPLOAD" and 1 <= total <= 1000 and total == tam // trozo and (
                (total == 1 and trozo == tam and tam <= 64 * MB) or (5 * MB <= trozo <= 64 * MB and tam - trozo * (total - 1) <= 128 * MB))
            if not valido:
                return self._tt_error(400, "invalid_param")
            pid = f"v_inbox_file~v2.{len(M.tt_inits) + 1}"
            M.tt_inits.append({"id": pid, "tam": tam, "trozo": trozo, "total": total})
            M.tt_subidas[pid] = {"recibido": 0, "tam": tam, "hash": hashlib.sha256(), "trozos": 0, "consultas": 0, "completo": False}
            puerto = self.server.server_address[1]
            return self._fin(200, {"data": {"publish_id": pid, "upload_url": f"http://127.0.0.1:{puerto}/upload/{pid}?upload_token=x"},
                                   "error": {"code": "ok", "message": "", "log_id": "L2"}})
        if ruta == "/v2/post/publish/status/fetch/":
            if not self._tt_autorizado():
                return
            pid = json.loads(cuerpo).get("publish_id")
            s = M.tt_subidas.get(pid)
            if not s:
                return self._tt_error(400, "invalid_publish_id")
            if not s["completo"]:
                return self._fin(200, {"data": {"status": "PROCESSING_UPLOAD", "uploaded_bytes": s["recibido"]}, "error": {"code": "ok"}})
            if M.tt_fallo:
                return self._fin(200, {"data": {"status": "FAILED", "fail_reason": M.tt_fallo}, "error": {"code": "ok"}})
            s["consultas"] += 1
            est = M.tt_estados[min(s["consultas"] - 1, len(M.tt_estados) - 1)]
            return self._fin(200, {"data": {"status": est, "publicaly_available_post_id": M.tt_post_ids if est == "PUBLISH_COMPLETE" else []},
                                   "error": {"code": "ok"}})
        if ruta.startswith("/rupload/"):
            cid = ruta.split("/")[2]
            c = M.ig_contenedores.get(cid)
            bien = (c and self.headers.get("Authorization") == "OAuth TOKENFB" and self.headers.get("offset") == "0"
                    and self.headers.get("file_size") == str(len(cuerpo)))
            if not bien:
                return self._fin(400, {"debug_info": {"retriable": False, "type": "ProcessingFailedError", "message": "cabeceras mal"}})
            c["subido"] = True
            M.ig_subidas[cid] = hashlib.sha256(cuerpo).hexdigest()
            return self._fin(200, {"success": True, "message": "Upload successful."})
        if ruta.startswith(("/fb/", "/ig/")):
            modo, resto = ruta[1:3], ruta[4:]
            f = {k: v[0] for k, v in urllib.parse.parse_qs(cuerpo.decode()).items()}
            bueno = "TOKENFB" if modo == "fb" else f"TOKENIG{M.ig_refrescos or ''}"
            if M.ig_token_malo or f.get("access_token") != bueno:
                return self._ig_error(190)
            if resto == "999/media":
                if f.get("media_type") != "REELS" or not f.get("caption"):
                    return self._ig_error(100)
                if modo == "ig" and f.get("upload_type") == "resumable":
                    return self._ig_error(100)
                if not (f.get("upload_type") == "resumable") and not f.get("video_url"):
                    return self._ig_error(100)
                cid = f"c{len(M.ig_contenedores) + 1}"
                M.ig_contenedores[cid] = {"campos": f, "consultas": 0, "publicado": False, "video_url": f.get("video_url")}
                r = {"id": cid}
                if f.get("upload_type") == "resumable":
                    r["uri"] = f"http://127.0.0.1:{self.server.server_address[1]}/rupload/{cid}"
                return self._fin(200, r)
            if resto == "999/media_publish":
                c = M.ig_contenedores.get(f.get("creation_id"))
                if not c or c["publicado"]:
                    return self._ig_error(9007, 2207027)
                c["publicado"] = True
                mid = f"m{len(M.ig_publicados) + 1}"
                M.ig_publicados.append(mid)
                M.ig_medios.insert(0, {"id": mid, "caption": c["campos"]["caption"], "permalink": f"https://www.instagram.com/reel/{mid}/"})
                if M.ig_publicar_pierde_respuesta:
                    return self._fin(500, {"error": {"message": "se cayó", "code": 2}})
                return self._fin(200, {"id": mid})
            if resto.endswith("/comments"):
                M.ig_comentarios.append(f.get("message"))
                return self._fin(200, {"id": "com1"})
        self._fin(404, {"error": {"message": "no existe", "code": 24}})

    # ------------------------------------------------------------------ PUT (trozos de TikTok)
    def do_PUT(self):
        ruta, q = self._ruta()
        cuerpo = self._cuerpo()
        M.peticiones.append(("PUT", ruta))
        s = M.tt_subidas.get(ruta.split("/")[2])
        if not s:
            return self._fin(404, {})
        if M.tt_put_503 > 0:
            M.tt_put_503 -= 1
            return self._fin(503, {})
        rango = self.headers.get("Content-Range", "")
        try:
            tramo, total = rango.replace("bytes ", "").split("/")
            ini, fin = (int(x) for x in tramo.split("-"))
        except ValueError:
            return self._fin(400, {})
        if int(total) != s["tam"] or fin - ini + 1 != len(cuerpo) or self.headers.get("Content-Type") != "video/mp4":
            return self._fin(400, {})
        if ini != s["recibido"]:
            return self._fin(416, {})
        s["recibido"] += len(cuerpo)
        s["hash"].update(cuerpo)
        s["trozos"] += 1
        s["completo"] = s["recibido"] == s["tam"]
        self._fin(201 if s["completo"] else 206, {}, {"Content-Range": f"bytes 0-{s['recibido'] - 1}/{s['tam']}"})


# ---------------------------------------------------------------------- utilidades de las pruebas

def mp4_falso(ruta, tam, moov_al_final=False):
    """Un archivo con la estructura de átomos de un MP4 (ftyp, moov, mdat) y el tamaño pedido."""
    ftyp = struct.pack(">I4s", 24, b"ftyp") + b"isom\x00\x00\x02\x00isomiso2"
    moov = struct.pack(">I4s", 108, b"moov") + b"\x00" * 100
    resto = tam - len(ftyp) - len(moov)
    with open(ruta, "wb") as f:
        f.write(ftyp)
        if not moov_al_final:
            f.write(moov)
        f.write(struct.pack(">I4s", resto, b"mdat"))
        bloque = os.urandom(MB)
        escrito = 8
        while escrito < resto:
            n = min(MB, resto - escrito)
            f.write(bloque[:n])
            escrito += n
        if moov_al_final:
            f.write(moov)
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for b in iter(lambda: f.read(MB), b""):
            h.update(b)
    return h.hexdigest()


class Caso:
    def __init__(self, puerto):
        self.puerto = puerto
        self.dir = tempfile.mkdtemp(prefix="pm-prueba-")
        self.claves = os.path.join(self.dir, "claves.txt")
        self.metadatos = os.path.join(self.dir, "metadatos.json")
        self.video = os.path.join(self.dir, "01-platano_v1.mp4")
        self.registro = os.path.join(self.dir, "publicado.json")
        with open(self.metadatos, "w", encoding="utf-8") as f:
            json.dump({"01": {"archivo": "01-platano_v1.mp4", "tiktok": {"texto": TEXTO}, "instagram": {"texto": TEXTO},
                              "comentario": "¿Te comerías uno? 🍌", "portada": {"t": 50.75}}}, f, ensure_ascii=False)

    def poner_claves(self, texto):
        with open(self.claves, "w", encoding="utf-8") as f:
            f.write(texto)

    def claves_ahora(self):
        return dict(l.strip().split("=", 1) for l in open(self.claves, encoding="utf-8") if "=" in l and not l.startswith("#"))

    def reg(self):
        return json.load(open(self.registro, encoding="utf-8")) if os.path.exists(self.registro) else {}

    def entorno(self):
        env = dict(os.environ, PM_PRUEBAS="1", PM_PAUSA="0", PM_TIKTOK_API=f"http://127.0.0.1:{self.puerto}",
                   PM_IG_FB=f"http://127.0.0.1:{self.puerto}/fb", PM_IG_IG=f"http://127.0.0.1:{self.puerto}/ig")
        for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"):
            env.pop(k, None)
        env["NO_PROXY"] = "127.0.0.1"
        return env

    def lanzar(self, script, *extra):
        env = self.entorno()
        r = subprocess.run([sys.executable, os.path.join(AQUI, script), "--claves", self.claves, "--metadatos", self.metadatos,
                            "--clave", "01", "--video", self.video, *extra], capture_output=True, text=True, env=env, timeout=120)
        lineas = [l for l in r.stdout.strip().splitlines() if l.startswith("{")]
        if not lineas:
            raise AssertionError(f"{script} no imprimió JSON. salida={r.stdout[-400:]!r} error={r.stderr[-800:]!r}")
        return r.returncode, json.loads(lineas[-1])

    def cerrar(self):
        shutil.rmtree(self.dir, ignore_errors=True)


CLAVES_TT = "# claves del canal\nELEVENLABS_API_KEY=no-tocar\nTIKTOK_PUB_CLIENT_KEY=CK\nTIKTOK_PUB_CLIENT_SECRET=CS\nTIKTOK_PUB_REFRESH_TOKEN=rft.0\nTIKTOK_PUB_USUARIO=parece.mentira85\n"
CLAVES_FB = "ELEVENLABS_API_KEY=no-tocar\nIG_USER_ID=999\nIG_FB_TOKEN=TOKENFB\n"
CLAVES_IG = "IG_TOKEN=TOKENIG\n"
PRUEBAS = []


def prueba(f):
    PRUEBAS.append(f)
    return f


def igual(a, b, que=""):
    if a != b:
        raise AssertionError(f"{que}: esperaba {b!r} y salió {a!r}")


def cierto(x, que):
    if not x:
        raise AssertionError(que)


# ---------------------------------------------------------------------- TikTok

@prueba
def tiktok_prueba_no_sube_y_guarda_el_token_que_rota(c):
    c.poner_claves(CLAVES_TT); mp4_falso(c.video, 3 * MB)
    cod, r = c.lanzar("subir_tiktok.py", "--prueba")
    igual((cod, r["ok"], r.get("prueba")), (0, True, True), "resultado")
    igual(r["cuenta"], "Parece Mentira", "cuenta")
    igual(M.tt_inits, [], "no debe iniciar ninguna subida")
    k = c.claves_ahora()
    igual(k["TIKTOK_PUB_REFRESH_TOKEN"], "rft.1", "refresh token rotado guardado")
    igual(k["ELEVENLABS_API_KEY"], "no-tocar", "las demás claves no se tocan")
    cierto(open(c.claves, encoding="utf-8").read().startswith("# claves del canal"), "se conserva el comentario")
    igual(oct(os.stat(c.claves).st_mode & 0o777), "0o600", "permisos de claves.txt")
    igual(c.reg(), {}, "la prueba no escribe en el registro")


@prueba
def tiktok_envia_y_no_duplica(c):
    c.poner_claves(CLAVES_TT); h = mp4_falso(c.video, 3 * MB)
    cod, r = c.lanzar("subir_tiktok.py")
    igual((cod, r["ok"], r["estado"]), (0, True, "en_bandeja"), "resultado")
    igual(r["texto"], TEXTO, "devuelve el texto para pegarlo en el móvil")
    igual(M.tt_inits[0], {"id": r["publish_id"], "tam": 3 * MB, "trozo": 3 * MB, "total": 1}, "plan de trozos")
    igual(M.tt_subidas[r["publish_id"]]["hash"].hexdigest(), h, "el archivo llega idéntico")
    igual(c.reg()["01"]["tiktok"]["estado"], "en_bandeja", "registro")
    cod, r2 = c.lanzar("subir_tiktok.py")
    igual((cod, r2.get("yaEstaba"), len(M.tt_inits)), (0, True, 1), "segunda vez: no vuelve a subir")
    igual(M.n, 1, "y reutiliza el token de acceso guardado (no rota otra vez)")


@prueba
def tiktok_archivo_grande_en_trozos(c):
    c.poner_claves(CLAVES_TT); h = mp4_falso(c.video, 70 * MB + 123)
    cod, r = c.lanzar("subir_tiktok.py")
    igual((cod, r["estado"]), (0, "en_bandeja"), "resultado")
    igual((M.tt_inits[0]["trozo"], M.tt_inits[0]["total"]), (32 * MB, 2), "plan")
    s = M.tt_subidas[r["publish_id"]]
    igual((s["trozos"], s["hash"].hexdigest()), (2, h), "dos trozos y archivo idéntico")


@prueba
def tiktok_plan_de_trozos_cumple_las_reglas(c):
    sys.path.insert(0, AQUI)
    import subir_tiktok as t
    for tam in (1, 4 * MB, 5 * MB, 64 * MB, 64 * MB + 1, 95 * MB, 96 * MB, 500 * MB + 7, 4096 * MB):
        trozo, total = t.plan_trozos(tam)
        rs = list(t.rangos(tam, trozo, total))
        igual(total, tam // trozo, f"total para {tam}")
        igual((rs[0][0], rs[-1][1]), (0, tam - 1), f"cubre todo {tam}")
        cierto(all(rs[i][1] + 1 == rs[i + 1][0] for i in range(len(rs) - 1)), "trozos seguidos")
        cierto(total == 1 and tam <= 64 * MB or 5 * MB <= trozo <= 64 * MB, "tamaño de trozo permitido")
        cierto(rs[-1][1] - rs[-1][0] + 1 <= 128 * MB and total <= 1000, "último trozo y número de trozos")


@prueba
def tiktok_token_de_acceso_caducado_se_renueva_solo(c):
    c.poner_claves(CLAVES_TT + "TIKTOK_PUB_ACCESS_TOKEN=act.viejo\nTIKTOK_PUB_ACCESS_CADUCA=99999999999\nTIKTOK_PUB_PERMISOS=user.info.basic,video.upload\n")
    mp4_falso(c.video, 3 * MB)
    cod, r = c.lanzar("subir_tiktok.py")
    igual((cod, r["estado"], len(M.tt_inits)), (0, "en_bandeja", 1), "resultado")
    igual(c.claves_ahora()["TIKTOK_PUB_REFRESH_TOKEN"], "rft.1", "token nuevo guardado")


@prueba
def tiktok_cinco_borradores_pendientes(c):
    c.poner_claves(CLAVES_TT); mp4_falso(c.video, 3 * MB); M.tt_error_init = "spam_risk_too_many_pending_share"
    cod, r = c.lanzar("subir_tiktok.py")
    igual((cod, r["ok"], r["codigo"]), (1, False, "spam_risk_too_many_pending_share"), "resultado")
    cierto("5 vídeos" in r["error"], "explica el límite")
    igual(c.reg(), {}, "no apunta nada")


@prueba
def tiktok_sin_permiso_de_subida(c):
    c.poner_claves(CLAVES_TT); mp4_falso(c.video, 3 * MB); M.permisos = "user.info.basic"
    cod, r = c.lanzar("subir_tiktok.py")
    igual((cod, r["ok"]), (1, False), "resultado")
    cierto("video.upload" in r["error"] and M.tt_inits == [], "explica el permiso y no sube")


@prueba
def tiktok_permiso_caducado(c):
    c.poner_claves(CLAVES_TT.replace("rft.0", "rft.muerto")); mp4_falso(c.video, 3 * MB)
    cod, r = c.lanzar("subir_tiktok.py")
    igual((cod, r["ok"]), (1, False), "resultado")
    cierto("autorizar_tiktok.py" in r["error"], "dice cómo arreglarlo")
    igual(c.claves_ahora()["TIKTOK_PUB_REFRESH_TOKEN"], "rft.muerto", "no pisa claves")


@prueba
def tiktok_video_rechazado(c):
    c.poner_claves(CLAVES_TT); mp4_falso(c.video, 3 * MB); M.tt_fallo = "frame_rate_check_failed"
    cod, r = c.lanzar("subir_tiktok.py")
    igual((cod, r["ok"], r["motivo"]), (1, False, "frame_rate_check_failed"), "resultado")
    igual(c.reg()["01"]["tiktok"]["estado"], "fallido", "registro")
    M.tt_fallo = None
    cod, r = c.lanzar("subir_tiktok.py")
    igual((cod, r["estado"], len(M.tt_inits)), (0, "en_bandeja", 2), "tras un fallo se puede volver a enviar")


@prueba
def tiktok_estado_da_el_enlace_cuando_la_persona_publica(c):
    c.poner_claves(CLAVES_TT); mp4_falso(c.video, 3 * MB)
    c.lanzar("subir_tiktok.py")
    M.tt_estados, M.tt_post_ids = ["PUBLISH_COMPLETE"], [7708440623040269590]
    cod, r = c.lanzar("subir_tiktok.py", "--estado")
    igual((cod, r["estado"], r["url"]), (0, "publicado", "https://www.tiktok.com/@parece.mentira85/video/7708440623040269590"), "resultado")
    igual(c.reg()["01"]["tiktok"]["url"], r["url"], "registro")
    igual(len(M.tt_inits), 1, "--estado no sube nada")


@prueba
def tiktok_subida_cortada_se_reinicia(c):
    c.poner_claves(CLAVES_TT); mp4_falso(c.video, 3 * MB)
    c.lanzar("subir_tiktok.py", "--prueba")                      # deja token válido
    M.tt_inits.append({"id": "v_inbox_file~v2.1"})
    M.tt_subidas["v_inbox_file~v2.1"] = {"recibido": 100, "tam": 3 * MB, "hash": hashlib.sha256(), "trozos": 0, "consultas": 0, "completo": False}
    with open(c.registro, "w") as f:
        json.dump({"01": {"tiktok": {"publish_id": "v_inbox_file~v2.1", "estado": "subiendo"}}}, f)
    cod, r = c.lanzar("subir_tiktok.py")
    igual((cod, r["estado"], r["publish_id"]), (0, "en_bandeja", "v_inbox_file~v2.2"), "empieza una subida nueva")


@prueba
def tiktok_reintenta_el_trozo_si_tiktok_falla_un_momento(c):
    c.poner_claves(CLAVES_TT); h = mp4_falso(c.video, 3 * MB); M.tt_put_503 = 2
    cod, r = c.lanzar("subir_tiktok.py")
    igual((cod, r["estado"], len(M.tt_inits)), (0, "en_bandeja", 1), "resultado")
    igual(M.tt_subidas[r["publish_id"]]["hash"].hexdigest(), h, "el archivo llega idéntico y una sola vez")


@prueba
def sin_red_da_un_error_limpio(c):
    c.poner_claves(CLAVES_TT + CLAVES_FB); mp4_falso(c.video, 3 * MB)
    c.puerto = 9                                                  # nadie escucha ahí
    for script in ("subir_tiktok.py", "subir_instagram.py"):
        cod, r = c.lanzar(script)
        igual((cod, r["ok"]), (1, False), script)
        cierto("conectar" in r["error"], "dice que no hay conexión, sin traza de Python")
    igual(c.claves_ahora()["TIKTOK_PUB_REFRESH_TOKEN"], "rft.0", "no pierde el token")


@prueba
def archivo_que_no_es_mp4(c):
    c.poner_claves(CLAVES_TT + CLAVES_FB)
    with open(c.video, "wb") as f:
        f.write(b"esto no es un video" * 10000)
    for script in ("subir_tiktok.py", "subir_instagram.py"):
        cod, r = c.lanzar(script)
        igual((cod, r["ok"]), (1, False), script)
        cierto("MP4" in r["error"], "explica que no es un MP4")
    igual((M.tt_inits, M.ig_contenedores), ([], {}), "no se manda nada")


# ---------------------------------------------------------------------- Instagram

@prueba
def instagram_prueba_no_publica(c):
    c.poner_claves(CLAVES_FB); mp4_falso(c.video, 3 * MB)
    cod, r = c.lanzar("subir_instagram.py", "--prueba")
    igual((cod, r["ok"], r["prueba"], r["cuenta"], r["metodo"], r["cupo"]), (0, True, True, "parecementiramedia", "directa", "3/100"), "resultado")
    igual((M.ig_contenedores, M.ig_publicados, c.reg()), ({}, [], {}), "no crea ni publica ni apunta")


@prueba
def instagram_publica_subiendo_el_archivo_y_no_duplica(c):
    c.poner_claves(CLAVES_FB); h = mp4_falso(c.video, 3 * MB)
    cod, r = c.lanzar("subir_instagram.py", "--comentario")
    igual((cod, r["ok"], r["id"], r["url"]), (0, True, "m1", "https://www.instagram.com/reel/m1/"), "resultado")
    campos = M.ig_contenedores["c1"]["campos"]
    igual((campos["caption"], campos["media_type"], campos["upload_type"], campos["thumb_offset"], campos["share_to_feed"]),
          (TEXTO, "REELS", "resumable", "50750", "true"), "campos del Reel")
    cierto("video_url" not in campos, "no manda dirección pública")
    igual(M.ig_subidas["c1"], h, "el archivo llega idéntico")
    igual((len(M.ig_contenedores), M.ig_publicados, M.ig_comentarios), (1, ["m1"], ["¿Te comerías uno? 🍌"]), "una sola publicación y su comentario")
    igual(c.reg()["01"]["instagram"]["estado"], "publicado", "registro")
    cod, r2 = c.lanzar("subir_instagram.py", "--comentario")
    igual((cod, r2.get("yaEstaba"), len(M.ig_contenedores), M.ig_publicados), (0, True, 1, ["m1"]), "segunda vez: nada nuevo")


@prueba
def instagram_detecta_que_ya_esta_en_la_cuenta(c):
    c.poner_claves(CLAVES_FB); mp4_falso(c.video, 3 * MB)
    M.ig_medios = [{"id": "m77", "caption": TEXTO + " #otro", "permalink": "https://www.instagram.com/reel/m77/"}]
    cod, r = c.lanzar("subir_instagram.py")
    igual((cod, r.get("yaEstaba"), r["url"], M.ig_contenedores), (0, True, "https://www.instagram.com/reel/m77/", {}), "no republica")


@prueba
def instagram_video_rechazado(c):
    c.poner_claves(CLAVES_FB); mp4_falso(c.video, 3 * MB); M.ig_estados = ["IN_PROGRESS", "ERROR"]
    cod, r = c.lanzar("subir_instagram.py")
    igual((cod, r["ok"], M.ig_publicados), (1, False, []), "resultado")
    cierto("formato" in r["error"], "traduce el código 2207026")
    igual(c.reg()["01"]["instagram"]["estado"], "fallido", "registro")


@prueba
def instagram_respuesta_perdida_al_publicar_no_duplica(c):
    c.poner_claves(CLAVES_FB); mp4_falso(c.video, 3 * MB); M.ig_publicar_pierde_respuesta = True
    cod, r = c.lanzar("subir_instagram.py")
    igual((cod, r["ok"], r["url"], M.ig_publicados), (0, True, "https://www.instagram.com/reel/m1/", ["m1"]), "lo da por publicado una vez")
    cod, r = c.lanzar("subir_instagram.py")
    igual((r.get("yaEstaba"), M.ig_publicados), (True, ["m1"]), "y no repite")


@prueba
def instagram_si_tarda_se_retoma_el_mismo_envio(c):
    c.poner_claves(CLAVES_FB); mp4_falso(c.video, 3 * MB); M.ig_estados = ["IN_PROGRESS"] * 500
    cod, r = c.lanzar("subir_instagram.py", "--espera", "0")
    igual((cod, r["estado"], M.ig_publicados), (0, "procesando", []), "avisa de que sigue procesando")
    M.ig_estados = ["FINISHED"]
    cod, r = c.lanzar("subir_instagram.py")
    igual((cod, r["id"], len(M.ig_contenedores), len(M.ig_subidas)), (0, "m1", 1, 1), "retoma sin subir otro")


@prueba
def instagram_login_necesita_direccion_publica(c):
    c.poner_claves(CLAVES_IG); mp4_falso(c.video, 3 * MB)
    cod, r = c.lanzar("subir_instagram.py")
    igual((cod, r["ok"]), (1, False), "sin --video-url")
    cierto("--video-url" in r["error"] and M.ig_contenedores == {}, "lo explica y no crea nada")
    cod, r = c.lanzar("subir_instagram.py", "--video-url", "https://ejemplo.org/v/01.mp4")
    igual((cod, r["id"]), (0, "m1"), "con --video-url")
    campos = M.ig_contenedores["c1"]["campos"]
    igual((campos.get("video_url"), "upload_type" in campos, M.ig_subidas), ("https://ejemplo.org/v/01.mp4", False, {}), "usa la dirección y no sube archivo")


@prueba
def instagram_login_alarga_el_token_cada_semana(c):
    c.poner_claves(CLAVES_IG + "IG_TOKEN_RENOVADO=1000\n"); mp4_falso(c.video, 3 * MB)
    cod, r = c.lanzar("subir_instagram.py", "--prueba", "--video-url", "https://ejemplo.org/v/01.mp4")
    igual((cod, r["ok"], M.ig_refrescos), (0, True, 1), "renueva")
    igual(c.claves_ahora()["IG_TOKEN"], "TOKENIG1", "y guarda el token nuevo")


@prueba
def instagram_token_caducado(c):
    c.poner_claves(CLAVES_FB); mp4_falso(c.video, 3 * MB); M.ig_token_malo = True
    cod, r = c.lanzar("subir_instagram.py")
    igual((cod, r["ok"], r["codigo"]), (1, False, 190), "resultado")
    cierto("token" in r["error"], "lo explica")


@prueba
def instagram_cupo_agotado(c):
    c.poner_claves(CLAVES_FB); mp4_falso(c.video, 3 * MB); M.ig_cupo = 100
    cod, r = c.lanzar("subir_instagram.py")
    igual((cod, r["ok"], M.ig_contenedores), (1, False, {}), "no intenta publicar")


@prueba
def instagram_avisa_si_el_indice_va_al_final(c):
    c.poner_claves(CLAVES_FB); mp4_falso(c.video, 3 * MB, moov_al_final=True)
    cod, r = c.lanzar("subir_instagram.py", "--prueba")
    cierto(any("faststart" in x for x in r["avisos"]), "avisa del moov al final")


@prueba
def sin_claves_lo_dice_claro(c):
    c.poner_claves("ELEVENLABS_API_KEY=x\n"); mp4_falso(c.video, 3 * MB)
    for script, palabra in (("subir_tiktok.py", "TIKTOK_PUB_REFRESH_TOKEN"), ("subir_instagram.py", "IG_FB_TOKEN")):
        cod, r = c.lanzar(script, "--prueba")
        igual((cod, r["ok"]), (1, False), script)
        cierto(palabra in r["error"], f"{script} nombra la clave que falta")


@prueba
def autorizar_instagram_guarda_el_token_de_pagina(c):
    c.poner_claves("ELEVENLABS_API_KEY=no-tocar\nIG_APP_ID=APP1\nIG_APP_SECRET=SECRETO\n")
    r = subprocess.run([sys.executable, os.path.join(AQUI, "autorizar_instagram.py"), "--claves", c.claves],
                       input="CORTO\n", capture_output=True, text=True, env=c.entorno(), timeout=60, start_new_session=True)
    igual(r.returncode, 0, "termina bien: " + r.stdout[-300:] + r.stderr[-300:])
    k = c.claves_ahora()
    igual((k["IG_USER_ID"], k["IG_FB_TOKEN"], k["IG_CUENTA"], k["ELEVENLABS_API_KEY"]), ("999", "TOKENFB", "parecementiramedia", "no-tocar"), "claves guardadas")
    cierto("no caduca" in r.stdout, "dice que el token no caduca")
    cierto("TOKENFB" not in r.stdout + r.stderr and "LARGO" not in r.stdout + r.stderr, "no enseña tokens por pantalla")
    mp4_falso(c.video, 3 * MB)
    cod, r = c.lanzar("subir_instagram.py", "--prueba")
    igual((cod, r["ok"], r["cuenta"]), (0, True, "parecementiramedia"), "y con eso la prueba de publicar funciona")


@prueba
def autorizar_instagram_avisa_si_faltan_permisos(c):
    c.poner_claves("IG_APP_ID=APP1\nIG_APP_SECRET=SECRETO\n"); M.ig_permisos_token = ["instagram_basic", "pages_show_list"]
    r = subprocess.run([sys.executable, os.path.join(AQUI, "autorizar_instagram.py"), "--claves", c.claves],
                       input="CORTO\n", capture_output=True, text=True, env=c.entorno(), timeout=60, start_new_session=True)
    cierto(r.returncode != 0 and "instagram_content_publish" in r.stderr, "nombra el permiso que falta")
    cierto("IG_FB_TOKEN" not in c.claves_ahora(), "no guarda nada")


@prueba
def autorizar_tiktok_guarda_el_permiso(c):
    import re, time, urllib.request
    c.poner_claves("ELEVENLABS_API_KEY=no-tocar\nTIKTOK_PUB_CLIENT_KEY=CK\nTIKTOK_PUB_CLIENT_SECRET=CS\n")
    env = dict(c.entorno(), BROWSER="true", PYTHONUNBUFFERED="1")
    p = subprocess.Popen([sys.executable, os.path.join(AQUI, "autorizar_tiktok.py"), "--claves", c.claves],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env,
                         start_new_session=True)
    try:
        salida = ""
        while "state=" not in salida:
            linea = p.stdout.readline()
            if not linea:
                raise AssertionError("el script terminó antes de dar la dirección: " + p.stderr.read()[-300:])
            salida += linea
        q = urllib.parse.parse_qs(urllib.parse.urlparse(re.search(r"https://www\.tiktok\.com/\S+", salida).group(0)).query)
        igual((q["scope"][0], q["code_challenge_method"][0], q["redirect_uri"][0]),
              ("user.info.basic,video.upload", "S256", "http://127.0.0.1:8767/callback/"), "petición de permiso")
        for _ in range(50):
            try:
                urllib.request.build_opener(urllib.request.ProxyHandler({})).open(
                    f"http://127.0.0.1:8767/callback/?code=CODIGO&scopes=user.info.basic,video.upload&state={q['state'][0]}", timeout=5).read()
                break
            except OSError:
                time.sleep(0.1)
        resto, err = p.communicate(timeout=30)
    finally:
        if p.poll() is None:
            p.kill()
    igual(p.returncode, 0, "termina bien: " + err[-300:])
    k = c.claves_ahora()
    igual((k["TIKTOK_PUB_REFRESH_TOKEN"], k["TIKTOK_PUB_USUARIO"], k["TIKTOK_PUB_PERMISOS"], k["ELEVENLABS_API_KEY"]),
          ("rft.nuevo", "parece.mentira85", "user.info.basic,video.upload", "no-tocar"), "claves guardadas")
    cierto("rft.nuevo" not in salida + resto + err, "no enseña el token por pantalla")
    mp4_falso(c.video, 3 * MB)
    cod, r = c.lanzar("subir_tiktok.py")
    igual((cod, r["estado"], M.n), (0, "en_bandeja", 0), "y con eso se puede enviar sin renovar otra vez")


def main():
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Falso)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    fallos = []
    solo = sys.argv[1:]
    for f in PRUEBAS:
        if solo and not any(s in f.__name__ for s in solo):
            continue
        M.reiniciar()
        c = Caso(srv.server_address[1])
        try:
            f(c)
            print(f"  ✅ {f.__name__}")
        except Exception as e:   # noqa: BLE001
            fallos.append(f.__name__)
            print(f"  ❌ {f.__name__}: {e}")
        finally:
            c.cerrar()
    srv.shutdown()
    if fallos:
        print(f"\n{len(fallos)} FALLO(S): " + ", ".join(fallos))
        sys.exit(1)
    print("\nTODO BIEN")


if __name__ == "__main__":
    main()
