"""Fotograma de prueba del vídeo largo «El que copiaba en el colegio» (estilo del vídeo largo de la cueva).
Escena 5: Lucas se fija en la hamburguesería con cola hasta la esquina.
Uso: python3 frame_prueba.py DIR_SALIDA"""
import os, random, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
LARGO = os.path.join(RAIZ, "lotes", "largo-cueva-500-dias", "generadores")
sys.path.insert(0, RAIZ)
sys.path.insert(0, LARGO)
from motor.biblioteca import ilus  # noqa: E402
import ilus_personajes as IP  # noqa: E402
import ilus_escenarios as IE  # noqa: E402
from ilus_personajes import Lz, figura, _pj, mat, sombra_suelo, pie_suelo, PIEL2, PIEL3, PIEL4  # noqa: E402

CALLE = dict(luz=(0.7, -0.7), rim="#ffd9a0")   # luz cálida que sale de la tienda (a la derecha)

LUCAS = _pj(nombre="lucas", peinado="corto", pelo="#1e1612", top=mat("#2f6fb0", "#5f9fe0", "#173a60"), prenda="polar",
            pant=mat("#2e3440"), calzado="zapato", bota=mat("#e8e4dc", "#ffffff", "#9a968e"), edad=24, piel=PIEL4)
COLA = [
    _pj(nombre="c1", fem=True, peinado="melena", pelo="#2a1a10", top=mat("#c0392b", "#e66a58", "#6a1712"), prenda="polar",
        pant=mat("#3b5274", "#5f7aa0", "#1f2c42"), calzado="zapato", edad=27, piel=PIEL2),
    _pj(nombre="c2", peinado="rizado", pelo="#1a120c", top=mat("#3a8a5e", "#6ab88c", "#1d4a32"), prenda="chaqueta",
        pant=mat("#4a4038", "#6e6052", "#2a241e"), calzado="zapato", edad=33, piel=PIEL3),
    _pj(nombre="c3", fem=True, peinado="coleta", pelo="#8a5a2a", top=mat("#e0a92e", "#f4cc6a", "#8a6010"), prenda="polar",
        pant=mat("#2e3440"), calzado="zapato", edad=19, piel=PIEL4),
    _pj(nombre="c4", peinado="peinado60", pelo="#5a4a3a", barba="#5a4a3a", top=mat("#5a3a6a", "#8a64a0", "#2e1c38"), prenda="abrigo",
        pant=mat("#2a2a34"), calzado="zapato", edad=52),
    _pj(nombre="c5", fem=True, peinado="mono", pelo="#1a120c", top=mat("#2a7f9e", "#5fb3cf", "#174a5e"), prenda="chaqueta",
        pant=mat("#3a3f4a"), calzado="zapato", edad=40, piel=PIEL3),
    _pj(nombre="c6", peinado="corto", pelo="#3a2a1e", top=mat("#9e4a2a", "#cc7a54", "#4e2412"), prenda="camiseta", manga="corta",
        pant=mat("#3b5274", "#5f7aa0", "#1f2c42"), calzado="zapato", edad=17, piel=PIEL2),
]


def persona(n, pj, pose, ex, ang, vista="frente", w=520, h=940, u=108):
    z = IP._cuadro(n, w, h, CALLE)
    suelo = h - 25
    Pv = (w / 2, suelo - pie_suelo(u))
    sombra_suelo(z, w / 2, suelo - 6, 1.3 * u)
    poses = {
        "lado": [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)), dict(lado="R", a1=7, a2=3, mano=dict(t="lado", c=0.45, pal=-1))],
        "brazos": [dict(lado="L", obj=(Pv[0] + 0.3 * u, Pv[1] - 1.0 * u), flex=-1, ah=80, mano=dict(t="lado", c=0.5, pal=1)),
                   dict(lado="R", obj=(Pv[0] - 0.25 * u, Pv[1] - 1.1 * u), flex=1, ah=-80, mano=dict(t="lado", c=0.5, pal=-1), z=31)],
        "barbilla": [dict(lado="L", obj=(Pv[0] + 0.25 * u, Pv[1] - 1.2 * u), flex=-1, ah=80, mano=dict(t="lado", c=0.5, pal=1)),
                     dict(lado="R", obj=(Pv[0] + 0.05 * u, Pv[1] - 2.95 * u), flex=1, ah=150, mano=dict(t="lado", c=0.8, pal=-1), z=31)],
        "movil": [dict(lado="L", a1=-7, a2=-3, mano=dict(t="lado", c=0.45, pal=1)),
                  dict(lado="R", obj=(Pv[0] - 0.1 * u, Pv[1] - 1.7 * u), flex=1, ah=-60, mano=dict(t="lado", c=0.5, pal=-1), z=31)],
    }
    figura(z, Pv, u, pj, vista, cab=dict(ex=ex, ang=ang), brazos=poses[pose],
           piernas=[dict(lado="L", a1=-3, a2=-1, pie=dict(vista="frente")), dict(lado="R", a1=4, a2=1, pie=dict(vista="frente"))])
    z.guardar()
    return n


def persona_perfil(n, pj, ang=0, ex="neutra", u=108):
    """Persona de perfil, de pie, con los brazos caídos (esperando en la cola)."""
    w, h = 520, 960
    z = IP._cuadro(n, w, h, CALLE)
    suelo = h - 25
    Pv = (260, suelo - pie_suelo(u) + 0.07 * u)
    sombra_suelo(z, 260, suelo - 6, 1.4 * u)
    figura(z, Pv, u, pj, "perfil", tronco=182, cab=dict(ex=ex, ang=ang),
           brazos=[dict(lado="near", a1=-4, a2=8, mano=dict(t="lado", c=0.5, pal=1)),
                   dict(lado="far", a1=-8, a2=6, mano=dict(t="lado", c=0.5, pal=1))],
           piernas=[dict(lado="near", a1=4, a2=1, pie=dict(ang=0)), dict(lado="far", a1=-4, a2=-1, pie=dict(ang=0))])
    z.guardar()
    return n


def hamburgueseria():
    """Fachada de una hamburguesería de barrio de noche, con el interior cálido y un cartel con una hamburguesa (sin letras)."""
    n, w, h = "hamburgueseria", 900, 820
    z = Lz(n, w, h, luz=(-0.5, -0.8), rim="#ffd9a0")
    # halo de luz que sale a la calle
    gl = z.rad((450, 560), 520, [(0, "#ffcf8a", 0.45), (0.6, "#ffb15e", 0.12), (1, "#ffb15e", 0)])
    z(f'<ellipse cx="450" cy="600" rx="520" ry="300" fill="{gl}"/>')
    # muro de ladrillo
    gm = z.lin((0, 0), (900, 0), [(0, "#4a2e24"), (0.5, "#6a4232"), (1, "#3a241c")])
    z(f'<rect x="40" y="120" width="820" height="690" fill="{gm}"/>')
    r = random.Random(7)
    for fila in range(23):
        y = 124 + fila * 30
        off = 0 if fila % 2 else 30
        for c in range(14):
            x = 40 + off + c * 60
            if x > 840:
                continue
            col = r.choice(["#7a4a36", "#6a3e2c", "#84523c", "#5e3628"])
            z(f'<rect x="{x}" y="{y}" width="56" height="26" rx="3" fill="{col}" opacity="0.55"/>')
    # escaparate con interior cálido
    gi = z.lin((0, 330), (0, 760), [(0, "#ffe2b0"), (0.5, "#ffc47a"), (1, "#e08a3a")])
    z(f'<rect x="110" y="330" width="420" height="430" rx="10" fill="{gi}"/>')
    # mostrador, plancha y lámparas dentro
    z('<rect x="110" y="600" width="420" height="160" fill="#8a3a22"/>', '<rect x="110" y="596" width="420" height="16" fill="#c8a07a"/>')
    for x in (200, 320, 440):
        z(f'<path d="M{x} 330 L{x} 380" stroke="#3a2a20" stroke-width="3"/>', f'<path d="M{x-26} 400 Q{x} 370 {x+26} 400 Z" fill="#2a1a14"/>',
          f'<ellipse cx="{x}" cy="404" rx="22" ry="8" fill="#fff4d0"/>')
        gb = z.rad((x, 430), 90, [(0, "#fff6d8", 0.7), (1, "#fff6d8", 0)])
        z(f'<circle cx="{x}" cy="440" r="90" fill="{gb}"/>')
    # cocinero de espaldas (silueta cálida)
    z('<circle cx="390" cy="505" r="30" fill="#5a2a18"/>', '<path d="M345 600 Q350 540 390 535 Q430 540 436 600 Z" fill="#f4efe6"/>',
      '<rect x="365" y="462" width="52" height="26" rx="10" fill="#ffffff"/>')
    # reflejos en el cristal
    z('<path d="M140 340 L230 340 L150 750 L110 750 Z" fill="#ffffff" opacity="0.12"/>', '<path d="M260 340 L300 340 L220 750 L200 750 Z" fill="#ffffff" opacity="0.08"/>')
    z('<rect x="110" y="330" width="420" height="430" rx="10" fill="none" stroke="#1a1210" stroke-width="12"/>',
      '<path d="M320 330 L320 760" stroke="#1a1210" stroke-width="8"/>')
    # puerta abierta con luz
    gp = z.lin((0, 360), (0, 800), [(0, "#ffd89a"), (1, "#f0a050")])
    z(f'<rect x="590" y="360" width="200" height="450" fill="{gp}"/>', '<path d="M590 360 L560 380 L560 800 L590 810 Z" fill="#2a1a14"/>',
      '<rect x="590" y="360" width="200" height="450" fill="none" stroke="#1a1210" stroke-width="12"/>')
    # toldo a rayas rojas y crema
    for i in range(10):
        x0 = 30 + i * 84
        col = "#c8322a" if i % 2 == 0 else "#f3e6cf"
        som = "#8a1e18" if i % 2 == 0 else "#c8b89a"
        z(f'<path d="M{x0} 250 L{x0+84} 250 L{x0+94} 315 L{x0+10} 315 Z" fill="{col}"/>',
          f'<path d="M{x0+10} 315 Q{x0+52} 345 {x0+94} 315 Z" fill="{col}"/>',
          f'<path d="M{x0+10} 315 L{x0+94} 315 L{x0+92} 322 L{x0+12} 322 Z" fill="{som}" opacity="0.6"/>')
    z('<rect x="22" y="236" width="856" height="18" rx="6" fill="#2a1a14"/>')
    # cartel redondo con una hamburguesa
    gc = z.rad((450, 130), 120, [(0, "#3a2a20"), (1, "#1a1210")])
    z(f'<circle cx="450" cy="130" r="112" fill="{gc}"/>', '<circle cx="450" cy="130" r="112" fill="none" stroke="#ffcf6a" stroke-width="8"/>')
    gh = z.rad((450, 130), 170, [(0, "#ffd890", 0.55), (1, "#ffd890", 0)])
    z(f'<circle cx="450" cy="130" r="170" fill="{gh}"/>')
    # hamburguesa
    z('<path d="M380 120 Q380 62 450 60 Q520 62 520 120 Z" fill="#e8a040"/>',
      '<path d="M392 108 Q400 74 440 68" stroke="#ffd890" stroke-width="7" fill="none" stroke-linecap="round"/>',
      '<path d="M372 124 Q390 112 410 126 Q430 112 450 126 Q470 112 490 126 Q510 112 528 124 L528 132 L372 132 Z" fill="#6ab04a"/>',
      '<rect x="374" y="132" width="152" height="20" rx="8" fill="#e0c020"/>',
      '<rect x="370" y="150" width="160" height="26" rx="12" fill="#6a3418"/>',
      '<path d="M380 178 L520 178 Q520 204 450 206 Q380 204 380 178 Z" fill="#d8903a"/>')
    for sx, sy in ((420, 84), (450, 76), (478, 86), (436, 98), (466, 98)):
        z(f'<ellipse cx="{sx}" cy="{sy}" rx="5" ry="3" fill="#fff4d0"/>')
    z.guardar()
    return n


def bocadillo_cola():
    """Bocadillo de pensamiento de Lucas con una cola de gente = «aquí hay clientes»."""
    n, w, h = "pensamiento_cola", 560, 360
    z = Lz(n, w, h, luz=(-0.5, -0.8), rim="#ffffff")
    z('<ellipse cx="290" cy="150" rx="250" ry="130" fill="#f6f2ea"/>', '<circle cx="90" cy="300" r="26" fill="#f6f2ea"/>',
      '<circle cx="50" cy="340" r="14" fill="#f6f2ea"/>')
    for i in range(7):
        x = 140 + i * 42
        z(f'<circle cx="{x}" cy="{118}" r="15" fill="#3a3f4a"/>', f'<path d="M{x-17} 180 Q{x-16} 140 {x} 138 Q{x+16} 140 {x+17} 180 Z" fill="#3a3f4a"/>')
    z('<path d="M120 200 L470 200" stroke="#c8322a" stroke-width="8" stroke-linecap="round"/>',
      '<path d="M440 182 L476 200 L440 218" stroke="#c8322a" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    z.guardar()
    return n


def generar(dirsvg):
    os.makedirs(dirsvg, exist_ok=True)
    ilus.OUT = dirsvg
    IP_OUT = getattr(IP, "OUT", None)
    if hasattr(IP, "OUT"):
        IP.OUT = dirsvg
    hamburgueseria()
    bocadillo_cola()
    persona("lucas_piensa", LUCAS, "brazos", "pensativo", -6)
    exs = [("lado", "neutra", 2), ("movil", "neutra", -8), ("brazos", "sonrisa", 3), ("lado", "neutra", -2), ("movil", "neutra", 6), ("lado", "sonrisa", 0)]
    for i, (pj, (po, ex, a)) in enumerate(zip(COLA, exs)):
        persona_perfil(f"cola_{i}", pj, ang=a, ex=ex)
    L = IE.Lienzo("bg_ciudad", 1920, 1080, 4101)
    IE.bg_ciudad(L)
    L.guardar(dirsvg, "bg_ciudad_h")
    return dirsvg


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else "svg"))
