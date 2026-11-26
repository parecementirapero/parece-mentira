"""Piezas extra de la parte 2 (prefijo p2_): piedras que caen sobre el que abre camino, valla que salta Lucas,
huella en la nieve. Estilo del largo de la cueva (luz principal + borde, degradados, grano, sombra de contacto)."""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
LARGO = os.path.join(RAIZ, "lotes", "largo-cueva-500-dias", "generadores")
sys.path.insert(0, RAIZ)
sys.path.insert(0, LARGO)
from motor.biblioteca import ilus  # noqa: E402
from ilus_personajes import Lz  # noqa: E402


def piedra(n, forma, base, luz, sombra, w=420, h=340):
    """Piedra con volumen: degradado, aristas iluminadas, grietas y sombra de contacto. Apoyo ≈ 0,93."""
    z = Lz(n, w, h, luz=(-0.6, -0.8), rim="#ffe2b0")
    g = z.lin((0, 20), (w * 0.4, h * 0.9), [(0, luz), (0.55, base), (1, sombra)])
    gs = z.rad((w / 2, h * 0.93), w * 0.45, [(0, "#000000", 0.45), (1, "#000000", 0)])
    z(f'<ellipse cx="{w/2}" cy="{h*0.93}" rx="{w*0.44}" ry="{h*0.06}" fill="{gs}"/>')
    z(f'<path d="{forma}" fill="{g}"/>')
    # cara en sombra (derecha) y arista de luz (izquierda/arriba)
    gsh = z.lin((w * 0.55, 0), (w, 0), [(0, sombra, 0), (1, sombra, 0.75)])
    z(f'<path d="{forma}" fill="{gsh}"/>')
    z(f'<path d="{forma}" fill="none" stroke="#2a1c14" stroke-width="5" stroke-linejoin="round" opacity="0.55"/>')
    return z


def p2_piedras():
    out = []
    a = piedra("p2_piedra_a", "M40 300 Q20 220 70 150 Q120 70 210 50 Q300 40 360 110 Q405 170 392 250 Q380 305 320 318 L80 320 Q50 318 40 300 Z",
               "#8a7a6a", "#c9b9a2", "#3e3228")
    a('<path d="M110 120 Q160 80 230 72" stroke="#efe2c8" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.7"/>',
      '<path d="M220 150 L250 200 L235 250" stroke="#3a2c22" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.6"/>',
      '<path d="M120 230 L160 250" stroke="#3a2c22" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.5"/>',
      '<ellipse cx="290" cy="150" rx="26" ry="14" fill="#5a4a3c" opacity="0.4"/>')
    a.guardar(); out.append("p2_piedra_a")
    b = piedra("p2_piedra_b", "M30 296 Q40 200 110 160 L170 70 Q230 40 290 90 Q370 150 395 240 Q400 300 350 316 L70 320 Q35 316 30 296 Z",
               "#7a7470", "#bdb6ae", "#34302c")
    b('<path d="M150 110 Q190 70 250 70" stroke="#f2ece4" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.7"/>',
      '<path d="M200 140 L180 200 L210 240 L200 290" stroke="#2a2622" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.55"/>',
      '<path d="M300 200 L340 230" stroke="#2a2622" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.5"/>')
    # nieve encima
    b('<path d="M150 112 Q200 60 270 80 Q320 100 340 140 Q300 120 250 128 Q200 120 150 112 Z" fill="#f6fbff"/>',
      '<path d="M170 104 Q210 76 260 84" stroke="#ffffff" stroke-width="6" fill="none" stroke-linecap="round"/>')
    b.guardar(); out.append("p2_piedra_b")
    return out


def p2_valla():
    """Valla de obras a rayas rojas y blancas sobre dos patas (lo difícil que Lucas se salta). Apoyo ≈ 0,95."""
    w, h = 760, 460
    z = Lz("p2_valla", w, h, luz=(-0.6, -0.8), rim="#ffe2b0")
    gs = z.rad((w / 2, h * 0.95), w * 0.48, [(0, "#000000", 0.4), (1, "#000000", 0)])
    z(f'<ellipse cx="{w/2}" cy="{h*0.95}" rx="{w*0.46}" ry="22" fill="{gs}"/>')
    gp = z.lin((0, 0), (40, 0), [(0, "#b8bcc4"), (0.4, "#eef1f5"), (1, "#6a707a")])
    for x in (120, 600):
        z(f'<rect x="{x}" y="120" width="40" height="315" rx="8" fill="{gp}"/>',
          f'<path d="M{x-50} 440 L{x+90} 440 L{x+70} 410 L{x-30} 410 Z" fill="#2e3440"/>',
          f'<path d="M{x-30} 410 L{x+70} 410" stroke="#5a6270" stroke-width="5"/>')
    for y0 in (110, 250):
        cl = z.clip(f"M40 {y0} L720 {y0} L720 {y0+90} L40 {y0+90} Z")
        z(f'<g clip-path="{cl}">')
        z(f'<rect x="40" y="{y0}" width="680" height="90" fill="#f4f0ea"/>')
        for i in range(-2, 12):
            x = 40 + i * 90
            z(f'<path d="M{x} {y0+90} L{x+45} {y0} L{x+90} {y0} L{x+45} {y0+90} Z" fill="#d23a2e"/>')
        gl = z.lin((0, y0), (0, y0 + 90), [(0, "#ffffff", 0.45), (0.35, "#ffffff", 0), (1, "#000000", 0.28)])
        z(f'<rect x="40" y="{y0}" width="680" height="90" fill="{gl}"/>', '</g>')
        z(f'<rect x="40" y="{y0}" width="680" height="90" rx="6" fill="none" stroke="#2a1c14" stroke-width="5" opacity="0.6"/>')
    # piloto ámbar encima
    gb = z.rad((380, 70), 60, [(0, "#ffe9a0"), (0.5, "#ffb020"), (1, "#c06a00")])
    gh = z.rad((380, 70), 120, [(0, "#ffd27a", 0.55), (1, "#ffd27a", 0)])
    z(f'<circle cx="380" cy="70" r="120" fill="{gh}"/>', f'<rect x="360" y="90" width="40" height="22" fill="#2e3440"/>',
      f'<path d="M340 95 Q340 30 380 30 Q420 30 420 95 Z" fill="{gb}"/>',
      '<path d="M356 70 Q358 46 378 40" stroke="#fff6d8" stroke-width="7" fill="none" stroke-linecap="round"/>')
    z.guardar()
    return ["p2_valla"]


def p2_huella():
    """Huella hundida en la nieve vista en perspectiva (para el camino abierto)."""
    w, h = 220, 90
    z = Lz("p2_huella_nieve", w, h, luz=(-0.6, -0.8), rim="#ffffff")
    g = z.lin((0, 10), (0, 80), [(0, "#7f97b8"), (1, "#c9d8ea")])
    z(f'<ellipse cx="68" cy="46" rx="52" ry="20" fill="{g}"/>', f'<ellipse cx="152" cy="40" rx="52" ry="20" fill="{g}"/>',
      '<path d="M18 52 Q68 72 118 52" stroke="#ffffff" stroke-width="5" fill="none" opacity="0.9"/>',
      '<path d="M102 46 Q152 66 202 46" stroke="#ffffff" stroke-width="5" fill="none" opacity="0.9"/>')
    z.guardar(textura=False)
    return ["p2_huella_nieve"]


def generar(dirsvg):
    os.makedirs(dirsvg, exist_ok=True)
    ilus.OUT = dirsvg
    return p2_piedras() + p2_valla() + p2_huella()


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
