"""Ilustraciones SVG del vídeo 03 (moáis con cuerpo) — estilo v4 (ver ilus.py)."""
import math
from ilus import guardar, lg, rg, grano, R

PIEDRA = lg("pie", (0, "#8a7d6c"), (0.55, "#6b5f51"), (1, "#3f362d"), x2=1, y2=0)
TEX = """<filter id="roca" x="0" y="0" width="100%" height="100%">
<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="4" seed="5"/>
<feColorMatrix type="matrix" values="0 0 0 0 0.2  0 0 0 0 0.17  0 0 0 0 0.13  0 0 0 0.5 0"/>
<feComposite operator="in" in2="SourceGraphic"/></filter>"""


def cara_moai(cuerpo=False, espalda=False, alto_total=None):
    """Moái de frente (o de espaldas). Lienzo 400 x (520 cabeza | 1100 entero)."""
    H = 1100 if cuerpo else 520
    p = []
    if not espalda:
        cab = ('M110 40 L290 40 L300 100 L310 300 Q318 380 300 470 L280 520 L120 520 L100 470 Q82 380 90 300 L100 100 Z')
    else:
        cab = ('M110 40 L290 40 L304 110 L312 320 Q316 400 300 470 L280 520 L120 520 L100 470 Q84 400 88 320 L96 110 Z')
    p.append(f'<path d="{cab}" fill="url(#pie)"/><path d="{cab}" filter="url(#roca)"/>')
    if not espalda:
        p += ['<path d="M96 150 L304 150 L300 190 Q200 215 100 190 Z" fill="#2b241e" opacity="0.85"/>',   # ceja
              '<ellipse cx="150" cy="215" rx="38" ry="22" fill="#1f1914"/><ellipse cx="250" cy="215" rx="38" ry="22" fill="#1f1914"/>',
              '<path d="M200 190 L232 330 Q200 350 168 330 Z" fill="#7d7061"/><path d="M200 190 L232 330 Q216 340 200 342 Z" fill="#3f362d" opacity="0.6"/>',
              '<path d="M150 400 Q200 390 250 400" stroke="#2b241e" stroke-width="10" fill="none"/>',
              '<path d="M160 430 Q200 450 240 430" stroke="#2b241e" stroke-width="6" fill="none" opacity="0.6"/>',
              '<rect x="64" y="160" width="40" height="190" rx="18" fill="#5e5346"/><rect x="296" y="160" width="40" height="190" rx="18" fill="#4a4137"/>']
    else:
        p.append('<rect x="64" y="160" width="40" height="190" rx="18" fill="#5e5346"/><rect x="296" y="160" width="40" height="190" rx="18" fill="#4a4137"/>')
    p.append('<path d="M110 40 L170 40 L150 520 L120 520 L100 470 Q82 380 90 300 L100 100 Z" fill="#fff3d6" opacity="0.12"/>')
    p.append('<path d="M240 40 L290 40 L300 100 L310 300 Q318 380 300 470 L280 520 L250 520 Z" fill="#000" opacity="0.18"/>')
    if cuerpo:
        tor = 'M90 510 L310 510 Q340 700 330 900 L320 1090 L80 1090 L70 900 Q60 700 90 510 Z'
        p.append(f'<path d="{tor}" fill="url(#pie)"/><path d="{tor}" filter="url(#roca)"/>')
        p.append('<path d="M240 510 L310 510 Q340 700 330 900 L320 1090 L260 1090 Z" fill="#000" opacity="0.2"/>')
        if not espalda:
            p += ['<path d="M95 640 Q120 840 200 900 Q140 830 125 640 Z" fill="#3f362d" opacity="0.7"/>',   # brazo izq
                  '<path d="M305 640 Q280 840 200 900 Q260 830 275 640 Z" fill="#3f362d" opacity="0.7"/>',
                  '<path d="M150 900 L250 900" stroke="#2b241e" stroke-width="6"/>',
                  '<ellipse cx="200" cy="740" rx="12" ry="10" fill="#2b241e"/>']
        else:  # grabados de la espalda (anillos y cinturón), con brillo
            p += ['<circle cx="200" cy="640" r="44" fill="none" stroke="#2b241e" stroke-width="8"/>',
                  '<circle cx="200" cy="640" r="20" fill="none" stroke="#2b241e" stroke-width="7"/>',
                  '<path d="M110 860 Q200 820 290 860" stroke="#2b241e" stroke-width="9" fill="none"/>',
                  '<path d="M110 890 Q200 850 290 890" stroke="#2b241e" stroke-width="9" fill="none"/>',
                  '<path d="M200 900 L170 980 L230 980 Z" fill="none" stroke="#2b241e" stroke-width="7"/>']
    return "".join(p), 400, H


def moais():
    for nombre, kw in (("moai_cabeza", {}), ("moai_entero", {"cuerpo": True}), ("moai_espalda", {"cuerpo": True, "espalda": True})):
        cuerpo, w, h = cara_moai(**kw)
        guardar(nombre, cuerpo, w, h, PIEDRA + TEX)


def cielo_isla(d_id="ci", tarde=False):
    if tarde:
        return lg(d_id, (0, "#2a2f6b"), (0.45, "#e8875a"), (0.75, "#ffc68a"), (1, "#ffe6b8"))
    return lg(d_id, (0, "#3e88d0"), (0.6, "#9fd0f0"), (1, "#e9f4f2"))


def nubes(n=6, ymax=800):
    b = []
    for i in range(n):
        x, y = R.uniform(-100, 1000), R.uniform(160, ymax)
        b.append(f'<g opacity="0.92"><ellipse cx="{x:.0f}" cy="{y:.0f}" rx="170" ry="48" fill="#ffffff"/>'
                 f'<ellipse cx="{x+70:.0f}" cy="{y-34:.0f}" rx="100" ry="58" fill="#ffffff"/>'
                 f'<ellipse cx="{x-40:.0f}" cy="{y+18:.0f}" rx="150" ry="30" fill="#dbe7f2"/></g>')
    return "".join(b)


def cabezas_ladera(n, y0, y1, s0, s1):
    b = []
    for i in range(n):
        t = R.random()
        y = y0 + (y1 - y0) * t
        s = s0 + (s1 - s0) * t
        x = R.uniform(40, 1040)
        b.append(f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.3f}) rotate({R.uniform(-8,8):.0f})">'
                 f'<path d="M-90 0 L-80 -260 L80 -260 L92 0 Z" fill="#6b5f51"/>'
                 f'<path d="M-92 -200 L92 -200 L88 -170 L-88 -170 Z" fill="#2b241e" opacity="0.8"/>'
                 f'<path d="M0 -180 L22 -90 L-22 -90 Z" fill="#7d7061"/>'
                 f'<path d="M30 -260 L80 -260 L92 0 L40 0 Z" fill="#000" opacity="0.2"/></g>')
    return "".join(b)


def bg_isla():
    d = cielo_isla() + lg("hi", (0, "#7fc35a"), (1, "#3f8a3a")) + lg("mar", (0, "#3a9ad0"), (1, "#1a5a8a"))
    b = ['<rect width="1080" height="1920" fill="url(#ci)"/>', nubes(),
         '<rect y="980" width="1080" height="120" fill="url(#mar)"/>',
         '<path d="M0 1060 C220 980 420 1040 640 990 C820 950 960 990 1080 980 L1080 1920 L0 1920 Z" fill="url(#hi)"/>']
    for i in range(160):
        x, y = R.uniform(0, 1080), R.uniform(1080, 1920)
        b.append(f'<path d="M{x:.0f} {y:.0f} l-5 -22 M{x:.0f} {y:.0f} l6 -20" stroke="#2f6e2c" stroke-width="3" opacity="0.55"/>')
    b.append(grano())
    guardar("bg_isla", "".join(b), defs=d)


def bg_volcan(con_cabezas=True):
    d = cielo_isla() + lg("vo", (0, "#5ea24a"), (1, "#2f6e2c")) + lg("hi", (0, "#86c860"), (1, "#3f8a3a"))
    b = ['<rect width="1080" height="1920" fill="url(#ci)"/>', nubes(5, 600),
         '<path d="M-100 1250 L300 560 Q540 470 780 560 L1180 1250 Z" fill="url(#vo)"/>',
         '<path d="M300 560 Q540 470 780 560 Q540 620 300 560 Z" fill="#244f20" opacity="0.7"/>',
         '<path d="M420 700 L470 900 L380 1000 M700 680 L640 880 L720 1010" stroke="#b9a27a" stroke-width="16" opacity="0.5" fill="none"/>',   # cortes de cantera
         '<path d="M0 1180 C300 1120 700 1160 1080 1120 L1080 1920 L0 1920 Z" fill="url(#hi)"/>']
    if con_cabezas:
        b.append(cabezas_ladera(26, 900, 1700, 0.28, 0.9))
    b.append(grano())
    guardar("bg_volcan" if con_cabezas else "bg_volcan_vacio", "".join(b), defs=d)


def bg_seccion():
    """Corte del terreno: cielo arriba, hierba, y estratos de tierra a la vista (lienzo completo)."""
    d = cielo_isla() + lg("t1", (0, "#7a5a3a"), (1, "#5a3f26")) + lg("t2", (0, "#5a3f26"), (1, "#3a2816"))
    b = ['<rect width="1080" height="1920" fill="url(#ci)"/>', nubes(4, 500),
         '<rect y="900" width="1080" height="1020" fill="url(#t1)"/>',
         '<rect y="1350" width="1080" height="570" fill="url(#t2)"/>']
    for j, y in enumerate((1010, 1140, 1280, 1460, 1640, 1800)):
        b.append(f'<path d="M0 {y} C300 {y-20} 700 {y+20} 1080 {y-10}" stroke="#2a1c10" stroke-width="5" opacity="0.4" fill="none"/>')
    for i in range(90):
        x, y = R.uniform(0, 1080), R.uniform(920, 1900)
        r = R.uniform(4, 16)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r:.0f}" ry="{r*0.7:.0f}" fill="{R.choice(["#8e7a62","#6e5a44","#a0896b"])}" opacity="0.8"/>')
    b.append('<rect y="880" width="1080" height="34" fill="#5fae4a"/><rect y="880" width="1080" height="8" fill="#a6e07a"/>')
    b.append('<rect y="880" width="1080" height="1040" fill="#888" filter="url(#grano)"/>')
    guardar("bg_seccion", "".join(b), defs=d)


def bg_costa():
    d = cielo_isla(tarde=True) + lg("mar", (0, "#f2a865"), (0.25, "#2a6e8f"), (1, "#0f3550")) + \
        rg("sol", (0, "#fff6d2", 1), (0.25, "#ffd27a", 0.8), (1, "#ffb05a", 0)) + lg("hi", (0, "#6aa84f"), (1, "#2f5e2a"))
    b = ['<rect width="1080" height="1920" fill="url(#ci)"/>', '<circle cx="540" cy="900" r="520" fill="url(#sol)"/>',
         '<rect y="960" width="1080" height="300" fill="url(#mar)"/>',
         '<rect x="60" y="1150" width="960" height="70" fill="#7d7164"/><rect x="60" y="1150" width="960" height="10" fill="#c9b9a0" opacity="0.6"/>']
    for i in range(15):  # ahu: moáis de espaldas al mar, a contraluz
        x = 100 + i * 63
        h = R.uniform(170, 220)
        b.append(f'<path d="M{x-24} 1150 L{x-20} {1150-h} L{x+20} {1150-h} L{x+24} 1150 Z" fill="#2a221c"/>'
                 f'<rect x="{x-22}" y="{1150-h-14}" width="44" height="20" fill="#7a3a22" opacity="{0.9 if i % 3 == 0 else 0}"/>')
    b.append('<path d="M0 1220 C300 1200 700 1240 1080 1210 L1080 1920 L0 1920 Z" fill="url(#hi)"/>')
    b.append(grano())
    guardar("bg_costa", "".join(b), defs=d)


def arqueologo():
    """Arqueólogo de 1914 con pala, ilustrado con volumen (lienzo 360x760)."""
    d = lg("cha", (0, "#b89a6a"), (1, "#7a5f38"), x2=1, y2=0) + lg("pan", (0, "#6a5a48"), (1, "#3f342a"), x2=1, y2=0)
    b = ['<ellipse cx="180" cy="740" rx="120" ry="16" fill="#000" opacity="0.3" filter="url(#blur8)"/>',
         '<path d="M120 430 L110 720 L160 720 L180 470 L200 720 L250 720 L240 430 Z" fill="url(#pan)"/>',
         '<rect x="100" y="710" width="66" height="26" rx="10" fill="#2a2016"/><rect x="196" y="710" width="66" height="26" rx="10" fill="#2a2016"/>',
         '<path d="M110 240 Q180 210 250 240 L262 450 L98 450 Z" fill="url(#cha)"/>',
         '<path d="M175 245 L185 445" stroke="#5a4428" stroke-width="4"/>',
         '<circle cx="180" cy="170" r="58" fill="#e2b089"/>',
         '<path d="M122 150 Q180 60 238 150 Z" fill="#c9b07a"/><ellipse cx="180" cy="150" rx="98" ry="18" fill="#b89a5a"/>',
         '<path d="M150 200 Q180 215 210 200" stroke="#5a3a22" stroke-width="5" fill="none"/>',
         '<path d="M140 190 Q180 180 220 190 L215 205 Q180 196 145 205 Z" fill="#4a3424"/>',
         '<path d="M250 260 L310 420 L292 430 L236 290 Z" fill="url(#cha)"/>',
         '<line x1="300" y1="330" x2="300" y2="700" stroke="#7a5a32" stroke-width="12"/>',
         '<path d="M268 690 L332 690 L326 760 L274 760 Z" fill="#8c9096"/>']
    guardar("arqueologo", "".join(b), 360, 780, d)


def persona():
    guardar("persona_escala", '<circle cx="40" cy="30" r="22" fill="#c0392b"/><rect x="20" y="54" width="40" height="80" rx="12" fill="#c0392b"/>'
            '<rect x="22" y="130" width="14" height="60" fill="#2a2a33"/><rect x="44" y="130" width="14" height="60" fill="#2a2a33"/>', 80, 200)


def lupa():
    d = rg("cri", (0, "#ffffff", 0.25), (1, "#bfe0ff", 0.1))
    guardar("lupa", '<circle cx="200" cy="200" r="150" fill="url(#cri)" stroke="#f2f2f2" stroke-width="22"/>'
            '<rect x="300" y="300" width="60" height="200" rx="20" fill="#5a3a22" transform="rotate(-45 330 400)"/>'
            '<path d="M110 150 Q140 100 200 90" stroke="#ffffff" stroke-width="10" opacity="0.6" fill="none"/>', 520, 520, d)


def todo():
    moais(); bg_isla(); bg_volcan(True); bg_seccion(); bg_costa(); arqueologo(); persona(); lupa()


if __name__ == "__main__":
    todo()
    print("ok")
