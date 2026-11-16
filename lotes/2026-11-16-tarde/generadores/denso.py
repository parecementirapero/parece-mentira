"""Método «denso» (DECISIONS 2026-11-16, Nico) para el lote 2026-11-16-tarde v2.

Copia el mecanismo de `lotes/prueba-luna-densa/gen.py` en forma de módulo reutilizable:
- planos atados a PALABRAS del guion (índice en la alineación de ElevenLabs), no a segundos;
- duración variable (micro planos en los golpes, planos largos donde hay que entender algo);
- claves en fracción del plano (`K`), detalles de fondo que duran (`recorrido`, en tiempo absoluto);
- control de lectura: todo texto ≥ 0,25 s + 1 s por cada 17 letras (avisa si no);
- neones con halo sobre fondos oscuros; flechas con tic por raya; whoosh de transición como mucho cada 5 s y a −24 dB;
- música a −13 dB, gancho entero en el fotograma 0.

Uso desde un gen_0N_v2.py:
    D = Denso(salida, audio_mp3, alineacion_json)
    @D.plano(0, "gancho")
    def _(d): return D.P(fondo, elementos, camara, hud=[...], sfx=[...])
    D.construir("01", "slug", claves, {"generar": "curiosidad", "semilla": 1})
"""
import json, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
from base import IMG, BG, polvo, brillo, cam, Montaje  # noqa: E402,F401
from motor.tiempos import palabras_de_alineacion  # noqa: E402

CIAN, MAGENTA, LIMA, AMBAR = "#2ff3ff", "#ff3df2", "#7dff3a", "#ffe93d"
LEER = lambda txt: 0.25 + len(txt) / 17  # noqa: E731


class Denso:
    def __init__(self, salida, audio, alineacion):
        self.out = salida
        self.audio, self.alin = os.path.abspath(audio), os.path.abspath(alineacion)
        self.PAL = palabras_de_alineacion(self.alin)
        self.FIN = self.PAL[-1]["fin"] + 0.6
        self.M = Montaje(salida)
        self.FX, self.PLANOS, self.AVISOS = [], [], []
        self.INI = 0.0
        self.ult_whoosh = -9

    # ---------------------------------------------------------------- tiempo
    def w(self, i, adelanto=0.06):
        return max(0.0, self.PAL[i]["inicio"] - adelanto) if i else 0.0

    def plano(self, i_palabra, nombre, mas=0.0):
        def reg(fn):
            self.PLANOS.append((self.w(i_palabra) + mas, nombre, fn))
            return fn
        return reg

    @staticmethod
    def K(d, *pares):
        return [{"t": round(f * d, 3), **v} for f, v in pares]

    def recorrido(self, T0, T1, p0, p1, d, esc=None):
        """Objeto que cruza entre los segundos ABSOLUTOS T0 y T1: sigue en su sitio de un plano a otro."""
        def en(T):
            u = min(max((T - T0) / (T1 - T0), 0), 1)
            k = {"x": p0[0] + (p1[0] - p0[0]) * u, "y": p0[1] + (p1[1] - p0[1]) * u, "op": 1 if T0 <= T <= T1 else 0}
            if esc:
                k["escala"] = esc[0] + (esc[1] - esc[0]) * u
            return k
        return [{"t": 0, **en(self.INI), "ease": "lineal"}, {"t": d, **en(self.INI + d)}]

    # ---------------------------------------------------------------- sonido
    def fx(self, t, tipo, db=-14, **k):
        self.FX.append({"t": round(max(0, t), 3), "tipo": tipo, "db": db, **k})

    # ---------------------------------------------------------------- rótulos
    @staticmethod
    def rotulo(t0, t1, texto="", **k):
        ks = [{"t": t0, "escala": 0.0, "op": 0}, {"t": t0 + 0.05, "op": 1}, {"t": t0 + min(0.25, (t1 - t0) / 3), "escala": 1.0, "ease": "rebote"},
              {"t": t1, "escala": 1.0, "op": 1}, {"t": t1 + 0.15, "op": 0}]
        return {"tipo": "rotulo", "texto": texto, "hud": True, "z": 1, "keys": ks, **k}

    def amarillo(self, t0, t1, texto, y=1640, tam=96, color="#ffd23f"):
        return self.rotulo(t0, t1, texto, tam=tam, color=color, capsula=None, rot=-6, x=540, y=y)

    def contexto(self, t0, t1, texto, y=520):
        return self.rotulo(t0, t1, texto, tam=54, color="#ffffff", capsula="#c0392be6", borde="#ffffff30", x=540, y=y)

    def dato(self, t0, t1, texto, unidad="", y=1640, tam=120, borde=None, **k):
        r = self.rotulo(t0, t1, texto, unidad=unidad, tam=tam, x=k.pop("x", 540), y=y, **k)
        if borde:
            r["borde"] = borde
        return r

    def contador(self, t0, t1, desde, hasta, dur, unidad="", **k):
        tam, x, y = k.pop("tam", 120), k.pop("x", 540), k.pop("y", 1640)
        return {**self.rotulo(t0, t1, "", tam=tam, x=x, y=y, **k), "contar": [desde, hasta, dur], "contar_desde": t0, "unidad": unidad}

    # ---------------------------------------------------------------- trazos
    def flecha(self, pts, t0, t1, color="#ffffffcc", g=8, disc=None, punta=True, z=0.5):
        f = {"tipo": "flecha", "puntos": pts, "grosor": g, "color": color, "punta": punta, "z": z,
             "keys": [{"t": t0, "progreso": 0}, {"t": t1, "progreso": 1, "ease": "salida"}]}
        if disc:
            f["discontinua"] = disc
            largo = sum(((pts[i + 1][0] - pts[i][0]) ** 2 + (pts[i + 1][1] - pts[i][1]) ** 2) ** 0.5 for i in range(len(pts) - 1))
            n = int(min(8, max(3, largo / (disc[0] + disc[1]) / 2)))
            for i in range(n):
                self.fx(self.INI + t0 + (t1 - t0) * (i / n) ** 1.4, "trazo", -27, f=820 + 55 * i)
        return f

    def fugaz(self, t0, x0, y0, x1, y1, z=0.12):
        self.fx(self.INI + t0, "fugaz", -25, pan=round((x0 + x1) / 1080 - 1, 2))
        return {"tipo": "flecha", "puntos": [[x0, y0], [x1, y1]], "grosor": 3, "color": "#ffffffee", "punta": False, "z": z,
                "keys": [{"t": t0, "progreso": 0, "op": 1}, {"t": t0 + 0.7, "progreso": 1}, {"t": t0 + 1.0, "op": 1}, {"t": t0 + 1.6, "op": 0}]}

    def destello(self, x, y, t, color="#ffd23f", r=70, z=0.6):
        return brillo(x, y, r, color, 0.95, z, keys=[{"t": 0, "op": 0}, {"t": max(0, t - 0.01), "op": 0}, {"t": t, "op": 1, "escala": 0.4},
                                                  {"t": t + 0.25, "op": 0, "escala": 1.6}])

    @staticmethod
    def P(fondo, els, camara, entrada="corte", dur_entrada=0.3, vineta=0.55, hud=(), sfx=()):
        return dict(fondo=fondo, els=els, cam=camara, entrada=entrada, dur=dur_entrada, vineta=vineta, hud=list(hud), sfx=list(sfx))

    # ---------------------------------------------------------------- montaje
    def construir(self, n, slug, claves, musica):
        self.PLANOS.sort(key=lambda p: p[0])
        informe = []
        for k, (ini, nombre, fn) in enumerate(self.PLANOS):
            fin = self.PLANOS[k + 1][0] if k + 1 < len(self.PLANOS) else self.FIN
            d = round(fin - ini, 3)
            self.INI = ini
            p = fn(d)
            els = []
            for e in p["els"]:  # halo de neón: copia ancha y translúcida detrás de cada flecha gruesa
                if e.get("tipo") == "flecha" and e.get("grosor", 0) >= 6:
                    els.append({**e, "grosor": e["grosor"] * 3, "color": e["color"][:7] + "38", "punta": False})
                els.append(e)
            self.M.plano(ini, fin, p["fondo"], els, p["cam"], entrada=p["entrada"], vineta=p["vineta"],
                         dur=p["dur"] if p["entrada"] != "corte" else None)
            if p["entrada"] in ("desenfoque", "zoom", "barrido") and ini - self.ult_whoosh >= 5:
                self.fx(ini - 0.12, "whoosh", -24, dur=0.35)
                self.ult_whoosh = ini
            for h in p["hud"]:
                txt = ((h.get("texto") or "") + " " + (h.get("unidad") or "")).strip()
                if h.get("contar"):
                    txt = (f"{h['contar'][1]} " + txt).strip()
                visible = h["keys"][-2]["t"] - h["keys"][0]["t"] if h.get("keys") else d
                if visible + 1e-3 < LEER(txt):
                    self.AVISOS.append(f"  ⚠ «{txt}» en «{nombre}»: {visible:.2f} s, harían falta {LEER(txt):.2f} s")
                if h.get("keys"):
                    self.fx(ini + h["keys"][0]["t"], "pop", -18)
            self.M.add(*p["hud"])
            for s in p["sfx"]:
                t, tipo, db = s[:3]
                self.fx(ini + t, tipo, db, **(s[3] if len(s) > 3 else {}))
            informe.append((d, nombre))
        self.M.sfx = []
        self.M.guardar(n, slug, self.FIN, claves, musica)
        ruta = os.path.join(self.out, "episodio.json")
        ep = json.load(open(ruta))
        ep["version"] = 2
        ep["audio"], ep["subtitulos"]["alineacion"] = self.audio, self.alin
        ep["sfx"] = sorted(self.FX, key=lambda e: e["t"])
        json.dump(ep, open(ruta, "w"), ensure_ascii=False, indent=1)
        ds = [d for d, _ in informe]
        print(f"{len(ds)} planos · {len(self.FX)} efectos · {self.FIN:.1f} s · más corto {min(ds):.2f} s · más largo {max(ds):.2f} s")
        print("  < 0,7 s:", sum(d < 0.7 for d in ds), "· 0,7–1,5 s:", sum(0.7 <= d < 1.5 for d in ds), "· ≥ 1,5 s:", sum(d >= 1.5 for d in ds))
        for d, nm in informe:
            if d < 0.25:
                print(f"  ⚠ plano demasiado corto: {nm} ({d:.2f} s)")
        print("\n".join(self.AVISOS) if self.AVISOS else "  ✓ todos los textos se pueden leer")
