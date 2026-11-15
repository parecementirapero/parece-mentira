"""Ilustraciones SVG del vídeo 02 (la Luna se aleja) — estilo v4 (ver ilus.py)."""
import math, os, shutil
from ilus import guardar, lg, rg, grano, R, OUT

AQUI = os.path.dirname(os.path.abspath(__file__))
NICO = os.path.join(AQUI, "..", "..", "..", "..", "motor", "ejemplos", "v2-huellas-luna", "svg")


def estrellas(n=260, h=1920, sem=0):
    b = []
    for i in range(n):
        x, y = R.uniform(0, 1080), R.uniform(0, h)
        r = R.choice([0.8, 1.0, 1.2, 1.6, 2.2, 3.0])
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#ffffff" opacity="{R.uniform(0.35,1):.2f}"/>')
    for i in range(10):
        x, y = R.uniform(0, 1080), R.uniform(0, h)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="10" fill="#cfe0ff" opacity="0.25" filter="url(#blur8)"/>')
    return "".join(b)


def bg_espacio():
    d = lg("esp", (0, "#02030a"), (0.5, "#0a1030"), (1, "#05071a")) + \
        rg("neb1", (0, "#6a3fb8", 0.55), (1, "#6a3fb8", 0), cx=0.3, cy=0.3) + \
        rg("neb2", (0, "#1f7ab8", 0.45), (1, "#1f7ab8", 0), cx=0.7, cy=0.7)
    b = ['<rect width="1080" height="1920" fill="url(#esp)"/>',
         '<ellipse cx="300" cy="500" rx="700" ry="420" fill="url(#neb1)"/>',
         '<ellipse cx="800" cy="1400" rx="700" ry="500" fill="url(#neb2)"/>',
         '<path d="M-100 1500 C300 1100 700 800 1200 300" stroke="#c9d6ff" stroke-width="220" opacity="0.07" filter="url(#blur40)" fill="none"/>',
         estrellas(), grano()]
    guardar("bg_espacio", "".join(b), defs=d)


def tierra(nombre="tierra_hd", tam=600):
    c = tam / 2
    d = rg("oc", (0, "#4fb3ff", 1), (0.6, "#1a5fb4", 1), (1, "#0a2a66", 1), cx=0.35, cy=0.35) + \
        rg("atm", (0.85, "#8fd0ff", 0), (0.95, "#8fd0ff", 0.55), (1, "#8fd0ff", 0)) + \
        rg("noche", (0.45, "#000010", 0), (1, "#000010", 0.85), cx=0.15, cy=0.2, r=0.9)
    b = [f'<circle cx="{c}" cy="{c}" r="{c*0.98}" fill="url(#atm)"/>',
         f'<clipPath id="clip"><circle cx="{c}" cy="{c}" r="{c*0.86}"/></clipPath>',
         f'<circle cx="{c}" cy="{c}" r="{c*0.86}" fill="url(#oc)"/>', '<g clip-path="url(#clip)">']
    for i in range(9):  # continentes
        x, y = R.uniform(0.15, 0.85) * tam, R.uniform(0.15, 0.85) * tam
        pts = " ".join(f"{x+math.cos(a)*R.uniform(30,90)*tam/600:.0f},{y+math.sin(a)*R.uniform(30,90)*tam/600:.0f}" for a in [k * 0.6 for k in range(11)])
        b.append(f'<polygon points="{pts}" fill="{R.choice(["#4f9a4a","#6aa84f","#c9b37a","#3f7d3a"])}" opacity="0.95"/>')
    for i in range(14):  # nubes
        x, y = R.uniform(0, tam), R.uniform(0, tam)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{R.uniform(40,110)*tam/600:.0f}" ry="{R.uniform(10,24)*tam/600:.0f}" fill="#ffffff" opacity="0.75" transform="rotate({R.uniform(-25,25):.0f} {x:.0f} {y:.0f})"/>')
    b.append(f'<circle cx="{c}" cy="{c}" r="{c*0.86}" fill="url(#noche)"/></g>')
    b.append(f'<ellipse cx="{c*0.7}" cy="{c*0.6}" rx="{c*0.3}" ry="{c*0.16}" fill="#ffffff" opacity="0.18" transform="rotate(-30 {c*0.7} {c*0.6})"/>')
    guardar(nombre, "".join(b), tam, tam, d)


def luna(nombre="luna_hd", tam=400):
    c = tam / 2
    d = rg("lu", (0, "#f4f2ea", 1), (0.7, "#c9c6bb", 1), (1, "#8d8a82", 1), cx=0.38, cy=0.35) + \
        rg("som", (0.4, "#000", 0), (1, "#000", 0.7), cx=0.15, cy=0.2, r=0.95)
    b = [f'<circle cx="{c}" cy="{c}" r="{c*0.98}" fill="#e8ecf5" opacity="0.15" filter="url(#blur8)"/>',
         f'<circle cx="{c}" cy="{c}" r="{c*0.9}" fill="url(#lu)"/>']
    for i in range(6):  # mares
        x, y = R.uniform(0.25, 0.75) * tam, R.uniform(0.25, 0.75) * tam
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{R.uniform(25,60)*tam/400:.0f}" ry="{R.uniform(18,45)*tam/400:.0f}" fill="#8f8c86" opacity="0.45"/>')
    for i in range(30):  # cráteres
        a, rr = R.uniform(0, 6.28), R.uniform(0, c * 0.8)
        x, y, r = c + math.cos(a) * rr, c + math.sin(a) * rr, R.uniform(3, 16) * tam / 400
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#9a978f" opacity="0.6"/>'
                 f'<path d="M{x-r:.0f} {y:.0f} A{r:.1f} {r:.1f} 0 0 1 {x+r:.0f} {y:.0f}" stroke="#ffffff" stroke-opacity="0.5" stroke-width="1.5" fill="none"/>')
    b.append(f'<circle cx="{c}" cy="{c}" r="{c*0.9}" fill="url(#som)"/>')
    guardar(nombre, "".join(b), tam, tam, d)


def dedo():
    """Dedo índice en primer plano, con uña brillante (lienzo 500x1100, uña arriba)."""
    d = lg("piel", (0, "#f2c09a"), (0.5, "#e2a07a"), (1, "#b8734f"), x2=1, y2=0) + \
        lg("una", (0, "#ffe9ea"), (0.6, "#f7c2c4"), (1, "#e7a2a4")) + lg("blanca", (0, "#ffffff"), (1, "#f2ece6"))
    b = ['<path d="M90 1100 L90 260 C90 90 410 90 410 260 L410 1100 Z" fill="url(#piel)"/>',
         '<path d="M340 1100 L340 260 C340 170 380 150 410 260 L410 1100 Z" fill="#000" opacity="0.12"/>',
         '<path d="M110 1100 L110 270 C110 200 150 160 170 150" stroke="#fff3e6" stroke-width="10" opacity="0.4" fill="none"/>',
         '<path d="M150 560 Q250 590 350 560" stroke="#a8613f" stroke-width="5" opacity="0.5" fill="none"/>',
         '<path d="M160 590 Q250 610 340 590" stroke="#a8613f" stroke-width="4" opacity="0.35" fill="none"/>',
         '<path d="M140 300 C140 150 360 150 360 300 L360 420 C300 440 200 440 140 420 Z" fill="url(#una)"/>',
         '<path d="M140 300 C140 190 360 190 360 300 L360 330 C300 300 200 300 140 330 Z" fill="url(#blanca)"/>',
         '<ellipse cx="200" cy="360" rx="18" ry="40" fill="#ffffff" opacity="0.6"/>']
    guardar("dedo", "".join(b), 500, 1100, d)


def regla():
    d = lg("rg", (0, "#ffe27a"), (1, "#e2a92a"))
    b = ['<rect x="0" y="0" width="1000" height="140" rx="10" fill="url(#rg)" filter="url(#sombra)"/>']
    for i in range(101):
        h = 60 if i % 10 == 0 else (40 if i % 5 == 0 else 24)
        b.append(f'<line x1="{20+i*9.6:.1f}" y1="0" x2="{20+i*9.6:.1f}" y2="{h}" stroke="#3a2a10" stroke-width="{3 if i % 10 == 0 else 2}"/>')
        if i % 10 == 0:
            b.append(f'<text x="{20+i*9.6:.1f}" y="100" font-family="DejaVu Sans" font-weight="bold" font-size="28" fill="#3a2a10" text-anchor="middle">{i//10}</text>')
    b.append('<text x="980" y="128" font-family="DejaVu Sans" font-size="20" fill="#3a2a10" text-anchor="end">cm</text>')
    guardar("regla", "".join(b), 1000, 150, d)


def bg_superficie():
    d = lg("sue", (0, "#a7a6a2"), (1, "#4a4945")) + rg("luzt", (0, "#9fd4ff", 0.35), (1, "#9fd4ff", 0))
    b = ['<rect width="1080" height="1920" fill="#02030a"/>', estrellas(180, 1100)]
    b.append('<circle cx="800" cy="420" r="300" fill="url(#luzt)"/>')
    b.append('<path d="M0 1080 C200 1050 400 1100 600 1060 C800 1020 950 1070 1080 1050 L1080 1920 L0 1920 Z" fill="url(#sue)"/>')
    for i in range(40):
        x, y = R.uniform(0, 1080), R.uniform(1120, 1900)
        rx = R.uniform(20, 110) * (0.5 + (y - 1100) / 1600)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{rx*0.32:.0f}" fill="#3e3d3a" opacity="0.55"/>'
                 f'<path d="M{x-rx:.0f} {y:.0f} A{rx:.0f} {rx*0.32:.0f} 0 0 0 {x+rx:.0f} {y:.0f}" stroke="#d8d6cf" stroke-width="3" opacity="0.6" fill="none"/>')
    b.append('<rect y="1050" width="1080" height="870" fill="#888" filter="url(#grano)"/>')
    guardar("bg_superficie", "".join(b), defs=d)


def retro():
    d = lg("al", (0, "#e9ecf2"), (1, "#8d939e"))
    b = ['<path d="M30 300 L470 300 L440 330 L60 330 Z" fill="#6b707a"/>',
         '<rect x="140" y="250" width="16" height="70" fill="#8d939e"/><rect x="344" y="250" width="16" height="70" fill="#8d939e"/>',
         '<g transform="translate(250 160) rotate(-8) translate(-220 -110)"><rect width="440" height="220" rx="10" fill="url(#al)"/>']
    for i in range(10):
        for j in range(5):
            x, y = 20 + i * 41, 18 + j * 39
            b.append(f'<circle cx="{x+18}" cy="{y+18}" r="16" fill="#1a3a8a"/><circle cx="{x+13}" cy="{y+12}" r="6" fill="#bfe0ff" opacity="0.8"/>')
    b.append('</g>')
    guardar("retro", "".join(b), 500, 340, d)


def observatorio():
    d = lg("cer", (0, "#26345e"), (1, "#0d1428")) + lg("cup", (0, "#f2f4f8"), (1, "#8e94a4"), x2=1, y2=0) + \
        lg("muro", (0, "#d9dce4"), (1, "#9aa0ae"), x2=1, y2=0)
    b = ['<path d="M0 1460 C260 1330 620 1380 1080 1290 L1080 1920 L0 1920 Z" fill="url(#cer)"/>',
         '<path d="M0 1460 C260 1330 620 1380 1080 1290" stroke="#6d82c8" stroke-width="4" opacity="0.6" fill="none"/>',
         '<rect x="330" y="1240" width="340" height="230" fill="url(#muro)"/>',
         '<path d="M310 1245 A190 190 0 0 1 690 1245 Z" fill="url(#cup)"/>',
         '<path d="M500 1062 L540 1062 L560 1245 L480 1245 Z" fill="#1a1f2b"/>',
         '<rect x="300" y="1236" width="400" height="14" fill="#7d8494"/>']
    for i in range(6):
        b.append(f'<rect x="{360+i*50}" y="1330" width="22" height="34" rx="3" fill="#ffd77a" opacity="0.85"/>')
    for i in range(14):
        x = R.uniform(0, 1080); y = 1480 + R.uniform(0, 380)
        b.append(f'<path d="M{x:.0f} {y:.0f} l20 -60 l20 60 Z" fill="#0a1022"/>')
    guardar("observatorio", "".join(b), defs=d)


def cronometro():
    d = rg("cr", (0, "#ffffff", 1), (1, "#d6dbe6", 1)) + lg("mt", (0, "#d9dde6"), (1, "#7d8494"))
    b = ['<circle cx="300" cy="330" r="270" fill="#000" opacity="0.4" filter="url(#blur20)"/>',
         '<rect x="265" y="20" width="70" height="60" rx="12" fill="url(#mt)"/>',
         '<circle cx="300" cy="320" r="260" fill="url(#mt)"/>', '<circle cx="300" cy="320" r="228" fill="url(#cr)"/>']
    for i in range(60):
        a = math.radians(i * 6)
        r1 = 200 if i % 5 else 180
        b.append(f'<line x1="{300+math.sin(a)*r1:.1f}" y1="{320-math.cos(a)*r1:.1f}" x2="{300+math.sin(a)*214:.1f}" y2="{320-math.cos(a)*214:.1f}" stroke="#1b2233" stroke-width="{5 if i % 5 == 0 else 2}"/>')
    b.append('<text x="300" y="420" font-family="DejaVu Sans" font-weight="bold" font-size="40" fill="#1b2233" text-anchor="middle">s</text>')
    guardar("cronometro", "".join(b), 600, 600, d)


def marea():
    """Tierra vista desde el polo con el agua abultada hacia la Luna (lienzo 900x900)."""
    d = rg("ag", (0.55, "#3aa0ff", 0.0), (0.7, "#3aa0ff", 0.55), (1, "#3aa0ff", 0))
    b = ['<ellipse cx="450" cy="450" rx="420" ry="300" fill="url(#ag)"/>',
         '<ellipse cx="450" cy="450" rx="400" ry="290" fill="none" stroke="#9ad2ff" stroke-width="4" stroke-dasharray="14 12" opacity="0.8"/>']
    guardar("marea", "".join(b), 900, 900, d)


def campo_dia():
    d = lg("cd", (0, "#4f9be0"), (0.7, "#a9d4f0"), (1, "#fbe8c2")) + lg("pr", (0, "#7cc35a"), (1, "#3d8a3a")) + \
        rg("sold", (0, "#fffbe6", 1), (0.3, "#ffe08a", 0.8), (1, "#ffe08a", 0))
    b = ['<rect width="1080" height="1920" fill="url(#cd)"/>', '<circle cx="760" cy="560" r="360" fill="url(#sold)"/>']
    for i in range(5):
        x, y = R.uniform(-100, 1000), R.uniform(250, 800)
        b.append(f'<g opacity="0.9"><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="150" ry="50" fill="#ffffff"/><ellipse cx="{x+60:.0f}" cy="{y-30:.0f}" rx="90" ry="55" fill="#ffffff"/></g>')
    b.append('<path d="M0 1200 C250 1120 500 1180 760 1120 C900 1090 1000 1110 1080 1100 L1080 1920 L0 1920 Z" fill="#9bcf6a"/>')
    b.append('<path d="M0 1320 C300 1240 600 1320 1080 1250 L1080 1920 L0 1920 Z" fill="url(#pr)"/>')
    for i in range(120):
        x, y = R.uniform(0, 1080), R.uniform(1330, 1920)
        b.append(f'<path d="M{x:.0f} {y:.0f} l-4 -18 M{x:.0f} {y:.0f} l5 -16" stroke="#2f6e2c" stroke-width="3" opacity="0.6"/>')
    b.append(grano())
    guardar("campo_dia", "".join(b), defs=d)


def caracol():
    d = rg("con", (0, "#f2c27a", 1), (1, "#9a5a22", 1), cx=0.4, cy=0.4)
    b = ['<ellipse cx="160" cy="232" rx="150" ry="14" fill="#000" opacity="0.25" filter="url(#blur8)"/>',
         '<path d="M20 230 C40 200 230 200 300 225 C310 235 300 240 280 240 L30 240 Z" fill="#c9b58a"/>',
         '<path d="M250 210 C260 160 275 140 285 120" stroke="#c9b58a" stroke-width="12" fill="none" stroke-linecap="round"/>',
         '<circle cx="287" cy="114" r="9" fill="#2a2016"/>',
         '<circle cx="140" cy="140" r="90" fill="url(#con)"/>',
         '<path d="M140 140 m-10 0 a10 10 0 1 1 20 0 a30 30 0 1 1 -60 0 a50 50 0 1 1 100 0 a70 70 0 1 1 -140 0" stroke="#6a3a12" stroke-width="7" fill="none"/>']
    guardar("caracol", "".join(b), 320, 260, d)


def todo():
    bg_espacio(); tierra("tierra_hd", 600); luna("luna_hd", 400); dedo(); regla(); bg_superficie(); retro()
    observatorio(); cronometro(); marea(); campo_dia(); caracol()
    for f in ("astronauta.svg",):
        shutil.copy(os.path.join(NICO, f), os.path.join(OUT, f))


if __name__ == "__main__":
    todo()
    print("ok")
