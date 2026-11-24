"""Locución del vídeo largo «500 días en una cueva» por bloques (uno por parte de TikTok).
Uso (en el Mac, desde ~/Documents/Parece Mentira): python3 voz.py bloques.json N DIR
Guarda DIR/0N-locucion.mp3 y DIR/0N-alineacion.json nada más recibirlos. No sobrescribe nunca.
Misma llamada que los lotes: voz clon op8soO9fvP07F3mjbJuB, eleven_v4, stability 0.5, similarity 0.75, /with-timestamps.
Pasa el final del bloque anterior y el principio del siguiente como contexto (previous_text / next_text)."""
import base64, json, os, re, sys, urllib.request, urllib.error

VOZ, MODELO = "op8soO9fvP07F3mjbJuB", "eleven_v4"
bl = json.load(open(sys.argv[1], encoding="utf-8")); n = int(sys.argv[2]); out = sys.argv[3]
os.makedirs(out, exist_ok=True)
mp3, ali = os.path.join(out, f"{n:02d}-locucion.mp3"), os.path.join(out, f"{n:02d}-alineacion.json")
if os.path.exists(mp3) or os.path.exists(ali):
    sys.exit(f"ya existe {mp3}: no se regenera")
k = re.search(r"ELEVENLABS_API_KEY\s*=\s*(\S+)", open("claves.txt").read()).group(1)
cuerpo = {"text": bl[n - 1], "model_id": MODELO, "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}
if n > 1: cuerpo["previous_text"] = bl[n - 2][-500:]
if n < len(bl): cuerpo["next_text"] = bl[n][:500]
sin_ctx = "--sin-contexto" in sys.argv
if sin_ctx: cuerpo.pop("previous_text", None); cuerpo.pop("next_text", None)
req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}/with-timestamps?output_format=mp3_44100_128",
                             json.dumps(cuerpo).encode(), {"xi-api-key": k, "Content-Type": "application/json"}, method="POST")
try:
    r = urllib.request.urlopen(req, timeout=170); d = json.load(r)
except urllib.error.HTTPError as e:
    sys.exit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:400]}")
open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
d.pop("audio_base64")
d["_peticion"] = {"bloque": n, "modelo": MODELO, "voz": VOZ, "contexto": not sin_ctx, "caracteres": len(bl[n - 1])}
json.dump(d, open(ali, "w", encoding="utf-8"), ensure_ascii=False)
print(json.dumps({"ok": True, "mp3": mp3, "bytes": os.path.getsize(mp3), "fin_s": d["alignment"]["character_end_times_seconds"][-1]}))
