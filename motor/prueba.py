"""Prueba de humo del motor: comprueba en ~1 minuto que nada se ha roto antes de hacer commit de cambios en `motor/`.

    python3 -m motor.prueba

Monta la Luna de ejemplo sin voz (tiempos provisionales) en sus variantes, renderiza 2 s de cada una y pasa los dos
controles. No gasta créditos ni necesita el audio. Sale con código 1 si algo falla."""
import os, subprocess, sys, tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(RAIZ, "lotes", "prueba-luna-densa", "gen.py")
GUION = os.path.join(RAIZ, "lotes", "prueba-luna-densa", "guion.txt")


def run(*cmd):
    r = subprocess.run([sys.executable, *cmd], cwd=RAIZ, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)[-600:]


def main():
    fallos = []
    with tempfile.TemporaryDirectory() as tmp:
        pasos = [("guion", ("-m", "motor.guion", GUION), (0,))]
        for nombre in ("normal", "palabra"):
            d = os.path.join(tmp, nombre)
            # sin voz no se pueden pasar opciones por posición: las variantes se prueban con la voz provisional
            pasos.append((f"montar {nombre}", (GEN, d) if nombre == "normal" else (GEN, d, "-", "-", "palabra"), (0,)))
            pasos.append((f"render {nombre}", ("-m", "motor.render", os.path.join(d, "episodio.json"), "--salida", os.path.join(d, "out"), "--hasta", "2"), (0,)))
            pasos.append((f"calidad {nombre}", ("-m", "motor.calidad", os.path.join(d, "episodio.json")), (0, 1)))
        for nombre, cmd, validos in pasos:
            cod, salida = run(*cmd)
            ok = cod in validos and "Traceback" not in salida
            print(("✓" if ok else "✗"), nombre)
            if not ok: fallos.append((nombre, salida))
            if nombre.startswith("render") and ok:
                out = cmd[4]
                faltan = [e for e in (".mp4", ".srt", "_manifest.json") if not any(f.endswith(e) for f in os.listdir(out))]
                if faltan:
                    print("  ✗ faltan archivos:", faltan); fallos.append((nombre, f"faltan {faltan}"))
    for n, s in fallos:
        print(f"\n--- {n} ---\n{s}")
    print("\nTODO BIEN" if not fallos else f"\n{len(fallos)} FALLO(S)")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
