"""Ilustraciones del lote 2026-11-20-manana (Agente 08:00, Nico): 01 hipopótamos, 02 Fórmula Uno por el techo, 03 el bólido eléctrico de 1899.
Uso: python3 ilus_1120m.py DIR_SVG. Ladrillos de motor/biblioteca/ilus.py. Sin logos, marcas, equipos ni personas reales reconocibles: todo dibujado aquí."""
import math, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
sys.path.insert(0, RAIZ)
from motor.biblioteca import ilus  # noqa: E402
from motor.biblioteca.ilus import guardar, lg, rg  # noqa: E402

W, H = 1080, 1920


def _p(pts, cerrar=True):
    return "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + (" Z" if cerrar else "")


def _grano_clip(cid, w, h):
    return f'<g clip-path="url(#{cid})"><rect width="{w}" height="{h}" fill="#888" filter="url(#grano)"/></g>'


# ====================================================================== 01 · HIPOPÓTAMOS
def bg_rio_fondo(nombre="bg_rio_fondo"):
    """Fondo de río africano visto bajo el agua: agua verde turbia, rayos de luz, fondo de arena y piedras, plantas."""
    r = random.Random(11)
    d = (lg("rf_a", (0, "#3f8a7a"), (0.25, "#1f5a52"), (0.7, "#0f3330"), (1, "#081c1a")) +
         lg("rf_s", (0, "#6a5a3a"), (1, "#2a2216")) + lg("rf_r", (0, "#e8fff0"), (1, "#e8fff000")))
    b = ['<rect width="1080" height="1920" fill="url(#rf_a)"/>']
    # superficie ondulada arriba
    b.append('<path d="M-20 170 Q140 140 300 172 T620 168 T940 170 T1120 160 L1120 -20 L-20 -20 Z" fill="#9ad8c8" opacity="0.55"/>')
    b.append('<path d="M-20 178 Q160 150 320 180 T640 176 T960 178 T1120 170" stroke="#e8fff6" stroke-width="5" fill="none" opacity="0.6"/>')
    for i in range(7):  # rayos de luz
        x = 60 + i * 160 + r.uniform(-30, 30)
        b.append(f'<path d="M{x:.0f} 170 L{x+70:.0f} 170 L{x+260:.0f} 1500 L{x+120:.0f} 1500 Z" fill="url(#rf_r)" opacity="{r.uniform(0.07,0.16):.2f}"/>')
    # bruma media
    b.append('<rect y="900" width="1080" height="700" fill="#0c2a26" opacity="0.35" filter="url(#blur40)"/>')
    # fondo de arena con relieve
    b.append('<path d="M-40 1560 Q200 1500 420 1540 T820 1520 T1120 1540 L1120 1960 L-40 1960 Z" fill="url(#rf_s)"/>')
    b.append('<path d="M-40 1620 Q260 1580 520 1610 T1120 1600" stroke="#a8946a" stroke-width="6" fill="none" opacity="0.4"/>')
    for _ in range(26):  # piedras
        x, y = r.uniform(0, 1080), r.uniform(1560, 1900)
        s = r.uniform(14, 50)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{s:.0f}" ry="{s*0.5:.0f}" fill="#3a3222"/>'
                 f'<ellipse cx="{x-s*0.2:.0f}" cy="{y-s*0.18:.0f}" rx="{s*0.55:.0f}" ry="{s*0.2:.0f}" fill="#8a7a5a" opacity="0.5"/>')
    for _ in range(9):  # plantas que ondean
        x = r.uniform(0, 1080); hgt = r.uniform(160, 380)
        b.append(f'<path d="M{x:.0f} 1600 Q{x-40:.0f} {1600-hgt*0.5:.0f} {x+r.uniform(-30,30):.0f} {1600-hgt:.0f}" stroke="#2f6a3a" stroke-width="{r.uniform(8,16):.0f}" fill="none" stroke-linecap="round" opacity="0.85"/>')
    for _ in range(60):  # motas en suspensión
        b.append(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(200,1600):.0f}" r="{r.uniform(1,3.5):.1f}" fill="#d8f0d0" opacity="{r.uniform(0.15,0.45):.2f}"/>')
    b.append('<rect width="1080" height="1920" fill="#888" filter="url(#grano)"/>')
    guardar(nombre, "".join(b), defs=d)


def bg_sabana(nombre="bg_sabana", hora="tarde", rio=True):
    """Sabana africana con río al atardecer: cielo cálido, acacias, orilla con barro."""
    r = random.Random(12 if hora == "tarde" else 13)
    if hora == "tarde":
        d = lg("sa_c", (0, "#2a2a5a"), (0.35, "#c0604a"), (0.62, "#f4a860"), (0.7, "#ffd890"))
        sol = '<circle cx="700" cy="1000" r="110" fill="#fff0c0"/><circle cx="700" cy="1000" r="260" fill="#ffd890" opacity="0.35" filter="url(#blur40)"/>'
    else:
        d = lg("sa_c", (0, "#5aa0d8"), (0.55, "#a8d4ee"), (0.7, "#f0e8c8"))
        sol = '<circle cx="820" cy="380" r="80" fill="#fffbe8"/><circle cx="820" cy="380" r="200" fill="#fff4c0" opacity="0.35" filter="url(#blur40)"/>'
    d += lg("sa_t", (0, "#8a6a3a"), (1, "#4a3418")) + lg("sa_ag", (0, "#6aa0a8"), (1, "#2a4a50"))
    b = ['<rect width="1080" height="1920" fill="url(#sa_c)"/>', sol]
    b.append('<path d="M-40 1110 Q200 1070 420 1100 T820 1080 T1120 1100 L1120 1300 L-40 1300 Z" fill="#6a5a7a" opacity="0.55"/>')  # montes lejanos
    b.append('<rect y="1150" width="1080" height="800" fill="url(#sa_t)"/>')
    for _ in range(5):  # acacias
        x, y, s = r.uniform(40, 1040), r.uniform(1140, 1200), r.uniform(0.6, 1.2)
        b.append(f'<path d="M{x:.0f} {y:.0f} L{x+4*s:.0f} {y-120*s:.0f}" stroke="#2a1a10" stroke-width="{10*s:.0f}"/>'
                 f'<ellipse cx="{x+4*s:.0f}" cy="{y-130*s:.0f}" rx="{110*s:.0f}" ry="{26*s:.0f}" fill="#2a2a1a"/>'
                 f'<ellipse cx="{x-20*s:.0f}" cy="{y-140*s:.0f}" rx="{70*s:.0f}" ry="{16*s:.0f}" fill="#3a3a22"/>')
    # río
    if not rio:
        b.append('<path d="M-40 1500 Q300 1470 600 1500 T1120 1490" stroke="#c8a060" stroke-width="10" fill="none" opacity="0.5"/>')
        for _ in range(30):
            x, y = r.uniform(0, 1080), r.uniform(1300, 1700)
            b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(20,60):.0f}" ry="{r.uniform(4,10):.0f}" fill="#3a2a14" opacity="0.35"/>')
    if rio:
      b.append('<path d="M-40 1380 Q300 1330 600 1370 T1120 1360 L1120 1720 Q700 1680 400 1720 T-40 1700 Z" fill="url(#sa_ag)"/>')
    for i in range(10 if rio else 0):
        y = 1400 + i * 30
        b.append(f'<path d="M{r.uniform(-20,400):.0f} {y} l{r.uniform(150,400):.0f} 0" stroke="#ffe0b0" stroke-width="4" opacity="0.35"/>')
    for _ in range(40):  # hierba
        x = r.uniform(0, 1080); y = r.uniform(1720, 1920)
        b.append(f'<path d="M{x:.0f} {y:.0f} l-8 -40 M{x:.0f} {y:.0f} l6 -48 M{x:.0f} {y:.0f} l14 -36" stroke="#c09a4a" stroke-width="4" opacity="0.8"/>')
    b.append('<rect width="1080" height="1920" fill="#888" filter="url(#grano)"/>')
    guardar(nombre, "".join(b), defs=d)


def _hipo_cuerpo(salto=False):
    """Paths del hipopótamo de perfil (mira a la derecha) en un lienzo 1100×620."""
    cuerpo = ("M150 330 C150 210 300 150 470 150 C600 150 690 170 760 200 C800 175 860 170 905 195 "
              "C960 205 1010 250 1030 300 C1050 330 1050 380 1020 405 C985 430 920 420 880 410 "
              "C850 440 800 450 760 440 C720 470 640 480 520 478 C380 480 240 470 190 440 C160 410 148 370 150 330 Z")
    if not salto:
        lejos = ["M250 430 L240 560 L300 560 L310 440 Z", "M680 440 L690 560 L750 560 L740 430 Z"]
        cerca = ["M330 440 L320 580 C320 595 390 595 392 580 L400 450 Z", "M760 420 L775 580 C775 595 845 595 845 580 L830 410 Z"]
    else:   # trote en el aire: patas recogidas y estiradas
        lejos = ["M250 430 L200 540 L250 556 L310 450 Z", "M690 440 L760 540 L805 520 L740 430 Z"]
        cerca = ["M330 440 L270 560 C266 575 330 590 336 575 L400 455 Z", "M770 420 L850 540 C858 552 912 530 902 516 L830 410 Z"]
    return cuerpo, lejos, cerca


def hipo(nombre="hipo", salto=False, ojo_cerrado=False):
    """Hipopótamo con volumen (gris violáceo, panza rosada), orejas, ojo y nariz arriba de la cabeza, sombra."""
    cuerpo, lejos, cerca = _hipo_cuerpo(salto)
    extra = [
        # hocico y boca
        '<path d="M1030 330 C1000 360 940 372 890 368" stroke="#3a2a34" stroke-width="5" fill="none" opacity="0.7"/>',
        '<path d="M960 300 C990 290 1015 300 1025 315" stroke="#e8a8b0" stroke-width="10" fill="none" opacity="0.55"/>',
        # fosas nasales arriba del hocico
        '<ellipse cx="985" cy="232" rx="16" ry="9" fill="#2a1a24"/><ellipse cx="1012" cy="246" rx="13" ry="8" fill="#2a1a24"/>',
        # orejas
        '<path d="M790 200 C780 160 800 140 818 156 C825 170 818 192 808 205 Z" fill="#6a5a6a"/><path d="M795 196 C790 170 802 158 812 168" stroke="#e8a8b0" stroke-width="5" fill="none"/>',
        '<path d="M760 214 C745 180 760 160 776 174 C782 186 778 205 770 216 Z" fill="#4a3a4a"/>',
        # arrugas del cuello
        '<path d="M760 210 C750 260 752 330 770 400" stroke="#2a1e28" stroke-width="5" fill="none" opacity="0.35"/>',
        '<path d="M735 212 C722 270 726 340 744 410" stroke="#2a1e28" stroke-width="4" fill="none" opacity="0.25"/>',
        # rubor rosado (piel)
        '<ellipse cx="520" cy="440" rx="260" ry="34" fill="#d8909a" opacity="0.35"/>',
        # cola
        '<path d="M152 320 C120 330 110 360 118 380" stroke="#4a3a4a" stroke-width="10" fill="none" stroke-linecap="round"/>',
    ]
    if ojo_cerrado:
        extra.append('<path d="M858 222 Q875 234 892 222" stroke="#1a1208" stroke-width="6" fill="none" stroke-linecap="round"/>')
        ojo = None
    else:
        extra.append('<ellipse cx="875" cy="220" rx="20" ry="14" fill="#5a4a5a"/>')
        ojo = (876, 222, 10)
    ilus._animal(nombre, 1100, 620, cuerpo, lejos, cerca, extra, "#7a6a7e", "#c89aa0", luz="#ffd0a8", manchas=14, sem=5,
                 ojo=ojo, sombra=(560, 590, 380, 22) if not salto else None)


def hipo_cabeza(nombre="hipo_cabeza", cerrado=False):
    """Cabeza asomando del agua (ojos, orejas y nariz por encima). cerrado=True: orejas plegadas y nariz cerrada."""
    w, h = 1000, 700
    d = (lg("hc_c", (0, "#8a7a8e"), (0.6, "#6a5a6e"), (1, "#4a3a4e")) + lg("hc_ag", (0, "#3f8a7a"), (1, "#0f3330")) +
         f'<clipPath id="{nombre}_cl"><path d="M120 470 C120 300 260 220 430 220 C560 220 640 250 720 270 C820 280 900 330 900 430 L900 470 Z"/></clipPath>')
    b = ['<path d="M120 470 C120 300 260 220 430 220 C560 220 640 250 720 270 C820 280 900 330 900 430 L900 470 Z" fill="url(#hc_c)"/>',
         _grano_clip(f"{nombre}_cl", w, h),
         '<path d="M150 400 C200 300 300 250 430 245" stroke="#ffd0a8" stroke-width="6" fill="none" opacity="0.5"/>']
    # orejas
    if cerrado:
        b.append('<path d="M300 250 C300 225 330 215 350 230 Z" fill="#5a4a5e"/><path d="M230 270 C232 248 258 240 275 252 Z" fill="#4a3a4e"/>')
    else:
        b.append('<path d="M300 250 C285 170 320 140 345 165 C355 190 345 225 330 248 Z" fill="#6a5a6e"/><path d="M308 236 C300 190 318 172 332 182" stroke="#e8a8b0" stroke-width="7" fill="none"/>'
                 '<path d="M235 268 C215 200 245 175 268 195 C275 215 268 245 258 265 Z" fill="#5a4a5e"/>')
    # ojos
    for x in (420, 520):
        b.append(f'<ellipse cx="{x}" cy="262" rx="38" ry="30" fill="#7a6a7e"/>')
        if cerrado:
            b.append(f'<path d="M{x-20} 262 Q{x} 276 {x+20} 262" stroke="#1a1208" stroke-width="6" fill="none"/>')
        else:
            b.append(f'<circle cx="{x}" cy="262" r="14" fill="#1a1208"/><circle cx="{x+5}" cy="257" r="5" fill="#fff6d8"/>')
    # fosas nasales
    for x in (780, 850):
        if cerrado:
            b.append(f'<path d="M{x-18} 300 L{x+18} 300" stroke="#2a1a24" stroke-width="7" stroke-linecap="round"/>')
        else:
            b.append(f'<ellipse cx="{x}" cy="300" rx="20" ry="13" fill="#2a1a24"/>')
    # agua por delante
    b.append('<rect x="0" y="430" width="1000" height="270" fill="url(#hc_ag)" opacity="0.92"/>')
    b.append('<path d="M0 432 Q120 418 250 434 T500 430 T750 434 T1000 428" stroke="#e8fff6" stroke-width="6" fill="none" opacity="0.8"/>')
    for i in range(6):
        b.append(f'<path d="M{80+i*150} {470+i%3*30} l90 0" stroke="#e8fff6" stroke-width="4" opacity="0.35"/>')
    guardar(nombre, "".join(b), w, h, d)


def piel_gotas(nombre="piel_gotas"):
    """Primer plano de la piel del hipopótamo con gotas rojo-anaranjadas (el «sudor rojo»)."""
    r = random.Random(21)
    d = lg("pg_c", (0, "#8a6a7a"), (1, "#5a4252")) + rg("pg_g", (0, "#ffb070", 1), (0.5, "#e04a2a", 1), (1, "#9a1a10", 1), cx=0.4, cy=0.35)
    b = ['<rect width="1080" height="1920" fill="url(#pg_c)"/>']
    for _ in range(140):  # poros y arrugas
        x, y = r.uniform(0, 1080), r.uniform(0, 1920)
        b.append(f'<path d="M{x:.0f} {y:.0f} q{r.uniform(20,60):.0f} {r.uniform(-10,10):.0f} {r.uniform(60,140):.0f} {r.uniform(-6,6):.0f}" stroke="#3a2a34" stroke-width="{r.uniform(2,5):.0f}" fill="none" opacity="0.35"/>')
    b.append('<rect width="1080" height="1920" fill="#888" filter="url(#grano)"/>')
    for _ in range(26):
        x, y, s = r.uniform(60, 1020), r.uniform(200, 1700), r.uniform(18, 46)
        b.append(f'<path d="M{x:.0f} {y-s*1.3:.0f} C{x+s*0.9:.0f} {y-s*0.2:.0f} {x+s:.0f} {y+s*0.9:.0f} {x:.0f} {y+s:.0f} C{x-s:.0f} {y+s*0.9:.0f} {x-s*0.9:.0f} {y-s*0.2:.0f} {x:.0f} {y-s*1.3:.0f} Z" fill="url(#pg_g)"/>'
                 f'<ellipse cx="{x-s*0.3:.0f}" cy="{y-s*0.1:.0f}" rx="{s*0.18:.0f}" ry="{s*0.3:.0f}" fill="#fff" opacity="0.7"/>')
    guardar(nombre, "".join(b), defs=d)


def gota_color(nombre, c1, c2):
    w, h = 300, 400
    d = rg(f"{nombre}_g", (0, c1, 1), (0.6, c2, 1), (1, c2, 1), cx=0.4, cy=0.4)
    b = (f'<path d="M150 20 C230 150 270 230 270 280 C270 350 215 390 150 390 C85 390 30 350 30 280 C30 230 70 150 150 20 Z" fill="url(#{nombre}_g)"/>'
         '<ellipse cx="105" cy="270" rx="26" ry="50" fill="#fff" opacity="0.6"/>')
    guardar(nombre, b, w, h, d)


def crema_solar(nombre="crema_solar"):
    """Tubo de crema genérico (sin marca) con un sol dibujado."""
    w, h = 400, 820
    d = lg("cs_c", (0, "#fff4d8"), (0.5, "#ffd890"), (1, "#e09a40"), x2=1, y2=0)
    b = ('<path d="M80 120 L320 120 L300 700 L100 700 Z" fill="url(#cs_c)" stroke="#8a5a20" stroke-width="6"/>'
         '<rect x="140" y="700" width="120" height="90" rx="14" fill="#e85a3a"/><rect x="60" y="100" width="280" height="36" rx="10" fill="#e09a40"/>'
         '<circle cx="200" cy="360" r="70" fill="#ffb020"/>' +
         "".join(f'<path d="M{200+90*math.cos(a):.0f} {360+90*math.sin(a):.0f} L{200+120*math.cos(a):.0f} {360+120*math.sin(a):.0f}" stroke="#ffb020" stroke-width="12" stroke-linecap="round"/>' for a in [i * math.pi / 4 for i in range(8)]) +
         '<rect x="120" y="480" width="160" height="22" rx="10" fill="#8a5a20" opacity="0.4"/><path d="M110 140 L120 680" stroke="#fff" stroke-width="14" opacity="0.5"/>')
    guardar(nombre, b, w, h, d)


def bacteria(nombre="bacteria", col="#7dff3a"):
    w, h = 500, 260
    d = lg(f"{nombre}_c", (0, col), (1, "#2a6a1a"))
    b = (f'<rect x="40" y="60" width="420" height="140" rx="70" fill="url(#{nombre}_c)"/>'
         '<rect x="70" y="80" width="340" height="40" rx="20" fill="#fff" opacity="0.3"/>' +
         "".join(f'<path d="M{60+i*50} {200 if i%2 else 60} q{10} {30 if i%2 else -30} {-10} {60 if i%2 else -60}" stroke="{col}" stroke-width="6" fill="none"/>' for i in range(8)) +
         '<circle cx="180" cy="130" r="18" fill="#1a4a10" opacity="0.6"/><circle cx="300" cy="140" r="14" fill="#1a4a10" opacity="0.6"/>')
    guardar(nombre, b, w, h, d)


def pantalla_video(nombre="pantalla_video"):
    """Monitor de laboratorio con una tira de fotogramas de un hipopótamo corriendo (siluetas) y una línea de tiempo."""
    w, h = 1000, 760
    d = lg("pv_c", (0, "#1a2232"), (1, "#0a0e18"))
    b = ['<rect x="20" y="20" width="960" height="620" rx="30" fill="#2a3040"/>', '<rect x="50" y="50" width="900" height="560" rx="14" fill="url(#pv_c)"/>',
         '<rect x="430" y="640" width="140" height="70" fill="#2a3040"/><rect x="330" y="700" width="340" height="30" rx="14" fill="#3a4050"/>']
    for i in range(4):
        x = 80 + i * 215
        b.append(f'<rect x="{x}" y="110" width="195" height="250" rx="8" fill="#16304a" stroke="#2ff3ff" stroke-width="3"/>')
        up = 30 if i in (1, 2) else 0
        b.append(f'<ellipse cx="{x+100}" cy="{230-up}" rx="80" ry="38" fill="#9a8aa0"/><circle cx="{x+170}" cy="{214-up}" r="26" fill="#9a8aa0"/>')
        for k, dx in enumerate((-50, -20, 30, 60)):
            if i in (1, 2):
                b.append(f'<path d="M{x+100+dx} {250-up} l{(-12 if k%2 else 12)} 40" stroke="#9a8aa0" stroke-width="12" stroke-linecap="round"/>')
            else:
                b.append(f'<path d="M{x+100+dx} {250} l0 70" stroke="#9a8aa0" stroke-width="12" stroke-linecap="round"/>')
        b.append(f'<path d="M{x+10} 330 L{x+185} 330" stroke="#c0a070" stroke-width="5"/>')
    b.append('<rect x="80" y="420" width="840" height="12" rx="6" fill="#3a4a60"/><rect x="80" y="420" width="500" height="12" rx="6" fill="#ff3df2"/>')
    b.append('<circle cx="580" cy="426" r="18" fill="#fff"/>')
    for i in range(10):
        b.append(f'<rect x="{90+i*84}" y="470" width="60" height="{30+ (i*37)%90}" fill="#2ff3ff" opacity="0.5"/>')
    guardar(nombre, "".join(b), w, h, d)


def pesa_tonelada(nombre="pesa_tonelada"):
    w, h = 700, 640
    d = lg("pt_c", (0, "#5a6070"), (0.5, "#2a3040"), (1, "#14181f"), x2=1, y2=0)
    b = ('<path d="M150 140 L550 140 L660 600 L40 600 Z" fill="url(#pt_c)"/><path d="M150 140 L550 140 L560 180 L140 180 Z" fill="#8a90a0"/>'
         '<path d="M260 140 C260 40 440 40 440 140" stroke="#3a4050" stroke-width="40" fill="none"/>'
         '<path d="M60 590 L640 590" stroke="#000" stroke-width="8" opacity="0.4"/><path d="M170 200 L120 560" stroke="#fff" stroke-width="10" opacity="0.25"/>')
    guardar(nombre, b, w, h, d)


# ====================================================================== 02 · FÓRMULA UNO
def f1(nombre="f1", col="#19b6c8", col2="#ff7a1a"):
    """Monoplaza genérico de perfil (mira a la derecha), sin equipo, patrocinadores ni números. Lienzo 1200×380."""
    w, h = 1200, 380
    d = (lg(f"{nombre}_c", (0, "#ffffff"), (0.25, col), (1, "#0a3a44")) + lg(f"{nombre}_r", (0, "#3a3a3a"), (1, "#0a0a0a")) +
         rg(f"{nombre}_ll", (0, "#6a6a6a", 1), (0.55, "#2a2a2a", 1), (0.62, "#111", 1), (1, "#000", 1)))
    b = ['<ellipse cx="600" cy="350" rx="560" ry="18" fill="#000" opacity="0.45" filter="url(#blur8)"/>']
    # alerón trasero
    b.append('<path d="M60 70 L200 70 L210 90 L70 96 Z" fill="#1a1a1a"/><path d="M60 110 L200 104 L205 122 L66 130 Z" fill="#1a1a1a"/>'
             f'<rect x="80" y="70" width="14" height="190" fill="#222"/><rect x="180" y="70" width="14" height="190" fill="#222"/><path d="M58 70 L60 140" stroke="{col2}" stroke-width="10"/>')
    # cuerpo
    b.append(f'<path d="M150 260 L170 190 C260 170 380 150 470 150 L560 120 C600 112 640 112 660 130 L700 170 C820 180 960 200 1090 230 '
             f'C1140 240 1170 255 1170 270 L1150 290 L180 300 Z" fill="url(#{nombre}_c)"/>')
    b.append(f'<path d="M700 172 C820 182 960 202 1090 232" stroke="{col2}" stroke-width="12" fill="none"/>')
    b.append('<path d="M560 122 C600 114 640 114 660 132 L640 150 L560 150 Z" fill="#0a0a12"/>')  # cabina
    b.append('<circle cx="608" cy="120" r="30" fill="#f4f4f4"/><path d="M584 118 L632 118 L630 130 L586 130 Z" fill="#1a2a3a"/>')  # casco sin marcas
    b.append('<path d="M540 110 C580 70 650 70 690 120" stroke="#222" stroke-width="10" fill="none"/>')  # halo
    b.append('<path d="M330 190 L470 160 L500 200 L340 225 Z" fill="#0a2a32" opacity="0.6"/>')  # toma lateral
    # alerón delantero
    b.append(f'<path d="M1030 280 L1190 278 L1195 300 L1020 305 Z" fill="#1a1a1a"/><path d="M1060 262 L1180 262 L1185 276 L1060 280 Z" fill="{col2}"/>')
    b.append('<path d="M180 290 L1150 288" stroke="#000" stroke-width="10" opacity="0.5"/>')  # fondo plano
    # ruedas
    for cx, rr in ((300, 92), (960, 86)):
        b.append(f'<circle cx="{cx}" cy="{280}" r="{rr}" fill="url(#{nombre}_ll)"/><circle cx="{cx}" cy="280" r="{rr*0.48:.0f}" fill="#2a2a2a" stroke="#888" stroke-width="5"/>'
                 f'<circle cx="{cx}" cy="280" r="{rr*0.14:.0f}" fill="#c0c0c0"/><path d="M{cx-rr*0.75:.0f} 260 A{rr*0.8:.0f} {rr*0.8:.0f} 0 0 1 {cx-rr*0.2:.0f} {280-rr*0.78:.0f}" stroke="#fff" stroke-width="5" fill="none" opacity="0.3"/>')
    b.append(f'<path d="M200 182 C400 150 560 140 700 165" stroke="#fff" stroke-width="5" fill="none" opacity="0.55"/>')
    guardar(nombre, "".join(b), w, h, d)


def bg_tunel(nombre="bg_tunel"):
    """Interior de un túnel recto en perspectiva, de noche, con lámparas en el techo y líneas de la calzada."""
    d = (lg("tu_c", (0, "#1a2232"), (0.5, "#0a0e18"), (1, "#1a2232")) + rg("tu_f", (0, "#ffe8b0", 1), (0.4, "#ffb050", 0.5), (1, "#ffb050", 0)))
    VX, VY = 540, 960
    b = ['<rect width="1080" height="1920" fill="url(#tu_c)"/>']
    # paredes y techo en perspectiva
    b.append(f'<path d="M-200 -200 L{VX-90} {VY-120} L{VX+90} {VY-120} L1280 -200 Z" fill="#2a3242"/>')  # techo
    b.append(f'<path d="M-200 2120 L{VX-90} {VY+120} L{VX+90} {VY+120} L1280 2120 Z" fill="#20242c"/>')  # suelo
    b.append(f'<path d="M-200 -200 L{VX-90} {VY-120} L{VX-90} {VY+120} L-200 2120 Z" fill="#3a4252"/>')  # pared izq
    b.append(f'<path d="M1280 -200 L{VX+90} {VY-120} L{VX+90} {VY+120} L1280 2120 Z" fill="#323a4a"/>')  # pared der
    b.append(f'<rect x="{VX-90}" y="{VY-120}" width="180" height="240" fill="url(#tu_f)"/>')  # salida al fondo
    for i in range(1, 12):  # lámparas del techo y anillos
        u = (i / 12) ** 1.8
        y = -200 + (VY - 120 + 200) * u
        hw = 740 - (740 - 90) * u
        b.append(f'<rect x="{VX-hw*0.15:.0f}" y="{y:.0f}" width="{hw*0.3:.0f}" height="{max(4, 26*(1-u)):.0f}" fill="#fff4c8" opacity="0.9"/>')
        b.append(f'<path d="M{VX-hw:.0f} {y:.0f} L{VX-90-(hw-90)*0:.0f} {y:.0f}" stroke="#000" stroke-width="0"/>')
        yb = 2120 - (2120 - VY - 120) * u
        b.append(f'<rect x="{VX-hw*0.02:.0f}" y="{yb:.0f}" width="{hw*0.04:.0f}" height="{max(4, 60*(1-u)):.0f}" fill="#f4f4f4" opacity="0.8"/>')
        b.append(f'<path d="M{VX-hw:.0f} {y:.0f} L{VX-hw:.0f} {yb:.0f}" stroke="#4a5262" stroke-width="{max(2, 14*(1-u)):.0f}" opacity="0.6"/>')
        b.append(f'<path d="M{VX+hw:.0f} {y:.0f} L{VX+hw:.0f} {yb:.0f}" stroke="#4a5262" stroke-width="{max(2, 14*(1-u)):.0f}" opacity="0.6"/>')
    b.append('<rect width="1080" height="1920" fill="#888" filter="url(#grano)"/>')
    guardar(nombre, "".join(b), defs=d)


def bg_pista(nombre="bg_pista_noche"):
    """Pista de carreras de noche con edificios iluminados de neón genéricos al fondo (sin nombres ni marcas)."""
    r = random.Random(31)
    d = lg("pn_c", (0, "#05030f"), (0.45, "#1a0a3a"), (0.62, "#3a1a5a")) + lg("pn_a", (0, "#2a2a34"), (1, "#121218"))
    b = ['<rect width="1080" height="1920" fill="url(#pn_c)"/>']
    for _ in range(14):  # edificios
        x, wd, ht = r.uniform(-40, 1040), r.uniform(70, 160), r.uniform(300, 760)
        col = r.choice(["#2ff3ff", "#ff3df2", "#ffe93d", "#7dff3a"])
        b.append(f'<rect x="{x:.0f}" y="{1180-ht:.0f}" width="{wd:.0f}" height="{ht:.0f}" fill="#0e0a1e"/>')
        b.append(f'<rect x="{x:.0f}" y="{1180-ht:.0f}" width="{wd:.0f}" height="8" fill="{col}" opacity="0.9"/>')
        for k in range(int(ht / 40)):
            for j in range(int(wd / 30)):
                if r.random() < 0.45:
                    b.append(f'<rect x="{x+8+j*30:.0f}" y="{1200-ht+k*40:.0f}" width="14" height="18" fill="#ffd890" opacity="{r.uniform(0.3,0.8):.2f}"/>')
        b.append(f'<rect x="{x:.0f}" y="{1180-ht:.0f}" width="{wd:.0f}" height="{ht:.0f}" fill="{col}" opacity="0.08" filter="url(#blur20)"/>')
    b.append('<rect y="1180" width="1080" height="740" fill="url(#pn_a)"/>')
    b.append('<path d="M-40 1240 L1120 1240" stroke="#fff" stroke-width="10"/><path d="M-40 1860 L1120 1860" stroke="#fff" stroke-width="10"/>')
    for i in range(14):  # piano rojo y blanco
        b.append(f'<rect x="{i*80}" y="1200" width="40" height="30" fill="#e8302a"/><rect x="{i*80+40}" y="1200" width="40" height="30" fill="#f4f4f4"/>')
    for i in range(30):
        b.append(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(1260,1840):.0f}" r="{r.uniform(1,3):.1f}" fill="#fff" opacity="0.15"/>')
    b.append('<rect width="1080" height="1920" fill="#888" filter="url(#grano)"/>')
    guardar(nombre, "".join(b), defs=d)


def perfil_ala(nombre="perfil_ala", invertido=False):
    """Perfil de ala (sección) con su luz; invertido=True: el del alerón de un coche (curva abajo)."""
    w, h = 900, 360
    d = lg(f"{nombre}_c", (0, "#e8eef8"), (1, "#7a8aa8"))
    path = "M60 180 C120 60 420 40 840 170 C600 210 300 220 60 190 Z"
    t = f' transform="translate(0 360) scale(1 -1)"' if invertido else ""
    b = f'<g{t}><path d="{path}" fill="url(#{nombre}_c)" stroke="#fff" stroke-width="5"/><path d="M110 150 C250 90 500 90 760 160" stroke="#fff" stroke-width="6" fill="none" opacity="0.6"/></g>'
    guardar(nombre, b, w, h, d)


def avion(nombre="avion"):
    """Avión de pasajeros genérico de perfil, sin aerolínea."""
    w, h = 1200, 420
    d = lg("av_c", (0, "#ffffff"), (1, "#a8b4c8"))
    b = ('<path d="M120 220 C120 180 180 160 260 160 L1000 160 C1100 160 1160 190 1170 220 C1160 250 1100 270 1000 270 L260 270 C180 270 120 250 120 220 Z" fill="url(#av_c)"/>'
         '<path d="M200 160 L120 40 L200 40 L330 160 Z" fill="#c8d4e8"/><path d="M560 230 L760 230 L560 400 L470 400 Z" fill="#8a9ab8"/>'
         '<path d="M1080 190 C1110 195 1140 205 1150 215 L1080 215 Z" fill="#2a3a5a"/>' +
         "".join(f'<circle cx="{330+i*55}" cy="200" r="11" fill="#2a3a5a"/>' for i in range(13)) +
         '<path d="M260 248 L1050 248" stroke="#5aa0ff" stroke-width="8"/>')
    guardar(nombre, b, w, h, d)


def velocimetro(nombre="velocimetro"):
    w, h = 800, 520
    d = lg("ve_c", (0, "#2a3040"), (1, "#0a0e18"))
    b = ['<path d="M60 460 A340 340 0 0 1 740 460 Z" fill="url(#ve_c)" stroke="#2ff3ff" stroke-width="8"/>']
    for k in range(13):
        a = math.pi + k * math.pi / 12
        x0, y0 = 400 + 300 * math.cos(a), 460 + 300 * math.sin(a)
        x1, y1 = 400 + 330 * math.cos(a), 460 + 330 * math.sin(a)
        b.append(f'<path d="M{x0:.0f} {y0:.0f} L{x1:.0f} {y1:.0f}" stroke="#ffffff" stroke-width="{8 if k%3==0 else 4}"/>')
    b.append('<path d="M100 460 A300 300 0 0 1 700 460" stroke="#ff3d3d" stroke-width="14" fill="none" stroke-dasharray="0 700 300" opacity="0.8"/>')
    b.append('<circle cx="400" cy="460" r="30" fill="#ff3d3d"/>')
    guardar(nombre, "".join(b), w, h, d)


def aguja_vel(nombre="aguja_vel"):
    guardar(nombre, '<path d="M300 22 L590 30 L300 38 Z" fill="#ff3d3d"/><circle cx="300" cy="30" r="22" fill="#ff3d3d"/>', 600, 60)


def motor_bloque(nombre="motor_bloque"):
    """Motor genérico con cárter de aceite y una gota de aceite que se escapa."""
    w, h = 800, 640
    d = lg("mb_c", (0, "#8a909a"), (1, "#3a404a")) + lg("mb_o", (0, "#e8b040"), (1, "#7a4a10"))
    b = ['<rect x="120" y="120" width="560" height="320" rx="30" fill="url(#mb_c)"/>']
    for i in range(6):
        b.append(f'<rect x="{160+i*85}" y="60" width="60" height="90" rx="10" fill="#5a606a"/><circle cx="{190+i*85}" cy="70" r="14" fill="#c0c4cc"/>')
    b.append('<rect x="160" y="440" width="480" height="90" rx="20" fill="#2a2e36"/><path d="M180 200 L620 200 M180 280 L620 280 M180 360 L620 360" stroke="#2a2e36" stroke-width="10"/>')
    b.append('<path d="M400 530 C430 570 440 590 440 605 C440 625 420 635 400 635 C380 635 360 625 360 605 C360 590 370 570 400 530 Z" fill="url(#mb_o)"/>')
    guardar(nombre, "".join(b), w, h, d)


def curva_arriba(nombre="curva_arriba"):
    """Pista vista desde arriba: una curva cerrada con piano y hierba."""
    d = lg("ca_h", (0, "#2a5a2a"), (1, "#163a16"))
    b = ['<rect width="1080" height="1920" fill="url(#ca_h)"/>',
         '<path d="M300 2000 L300 1000 C300 650 780 650 780 1000 L780 2000" stroke="#e8302a" stroke-width="340" fill="none"/>',
         '<path d="M300 2000 L300 1000 C300 650 780 650 780 1000 L780 2000" stroke="#f4f4f4" stroke-width="340" fill="none" stroke-dasharray="40 40"/>',
         '<path d="M300 2000 L300 1000 C300 650 780 650 780 1000 L780 2000" stroke="#2a2a32" stroke-width="300" fill="none"/>',
         '<path d="M300 2000 L300 1000 C300 650 780 650 780 1000 L780 2000" stroke="#fff" stroke-width="6" fill="none" stroke-dasharray="40 50" opacity="0.6"/>',
         '<rect width="1080" height="1920" fill="#888" filter="url(#grano)"/>']
    guardar(nombre, "".join(b), defs=d)


def f1_arriba(nombre="f1_arriba", col="#19b6c8", col2="#ff7a1a"):
    """Monoplaza visto desde arriba (morro hacia arriba), sin marcas. Lienzo 300×640."""
    w, h = 300, 640
    b = (f'<rect x="20" y="20" width="260" height="40" rx="8" fill="{col2}"/><path d="M130 60 L170 60 L190 300 L230 360 L230 520 L70 520 L70 360 L110 300 Z" fill="{col}"/>'
         '<rect x="10" y="120" width="56" height="110" rx="14" fill="#111"/><rect x="234" y="120" width="56" height="110" rx="14" fill="#111"/>'
         '<rect x="0" y="440" width="66" height="130" rx="14" fill="#111"/><rect x="234" y="440" width="66" height="130" rx="14" fill="#111"/>'
         '<circle cx="150" cy="330" r="26" fill="#f4f4f4"/><rect x="40" y="580" width="220" height="44" rx="6" fill="#1a1a1a"/>'
         f'<path d="M150 70 L150 300" stroke="#fff" stroke-width="6" opacity="0.5"/>')
    guardar(nombre, b, w, h)


# ====================================================================== 03 · EL BÓLIDO ELÉCTRICO DE 1899
def _rueda(cx, cy, r, radios=14, col="#2a1a10"):
    b = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1a1a1a" stroke-width="{r*0.18:.0f}"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r*0.9:.0f}" fill="none" stroke="#8a6a3a" stroke-width="4"/>']
    for k in range(radios):
        a = k * 2 * math.pi / radios
        b.append(f'<path d="M{cx} {cy} L{cx + r*0.88*math.cos(a):.0f} {cy + r*0.88*math.sin(a):.0f}" stroke="#c8a870" stroke-width="5"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.14:.0f}" fill="#c8a060"/>')
    return "".join(b)


def bolido_1899(nombre="bolido_1899"):
    """Coche eléctrico de récord con carrocería de torpedo metálica, ruedas de radios y el piloto sentado encima (silueta con barba y gorra).
    Dibujo propio inspirado en la forma general de los coches de récord de 1899 (no es una foto). Lienzo 1200×560."""
    w, h = 1200, 560
    d = (lg(f"{nombre}_c", (0, "#f4f0e8"), (0.3, "#c8c4bc"), (0.65, "#7a7a80"), (1, "#3a3a40")) +
         lg(f"{nombre}_p", (0, "#3a2a20"), (1, "#1a120c")))
    b = ['<ellipse cx="600" cy="530" rx="520" ry="16" fill="#000" opacity="0.4" filter="url(#blur8)"/>']
    # chasis bajo
    b.append('<path d="M200 380 L1000 380" stroke="#2a2a2a" stroke-width="16"/>')
    # torpedo
    b.append(f'<path d="M120 300 C160 220 320 180 600 180 C860 180 1060 230 1140 300 C1060 360 860 390 600 390 C320 390 160 370 120 300 Z" fill="url(#{nombre}_c)"/>')
    b.append('<path d="M180 260 C320 200 760 190 1080 270" stroke="#fff" stroke-width="10" fill="none" opacity="0.7"/>')
    for x in (330, 520, 710, 900):  # remaches/juntas
        b.append(f'<path d="M{x} 190 C{x+10} 260 {x+10} 330 {x} 386" stroke="#5a5a60" stroke-width="3" fill="none" opacity="0.7"/>')
    # piloto encima (silueta: gorra, barba, chaqueta)
    b.append(f'<path d="M520 190 C520 120 560 90 600 90 C640 90 660 120 660 190 Z" fill="url(#{nombre}_p)"/>')  # torso
    b.append('<circle cx="606" cy="62" r="34" fill="#d8a888"/><path d="M572 52 C572 22 640 16 644 50 Z" fill="#2a2a2a"/>')  # cabeza y gorra
    b.append('<path d="M578 70 C580 108 632 112 638 72 C626 86 590 86 578 70 Z" fill="#a83a20"/>')  # barba roja
    b.append('<path d="M640 130 L720 170" stroke="#3a2a20" stroke-width="22" stroke-linecap="round"/>')  # brazo al volante
    b.append('<path d="M700 150 L760 190" stroke="#1a1a1a" stroke-width="10"/><ellipse cx="760" cy="190" rx="10" ry="34" fill="#1a1a1a" transform="rotate(-30 760 190)"/>')
    # ruedas
    b.append(_rueda(300, 420, 110)); b.append(_rueda(900, 420, 110))
    guardar(nombre, "".join(b), w, h, d)


def bg_campo_1899(nombre="bg_campo_1899"):
    """Carretera de tierra entre álamos, a las afueras de una ciudad, con tono de foto antigua (sepia)."""
    r = random.Random(41)
    d = lg("c9_c", (0, "#c8b898"), (0.6, "#e8dcc0")) + lg("c9_s", (0, "#a89070"), (1, "#5a4a32"))
    b = ['<rect width="1080" height="1920" fill="url(#c9_c)"/>',
         '<path d="M-40 1100 Q300 1060 600 1090 T1120 1080 L1120 1200 L-40 1200 Z" fill="#9a9078" opacity="0.6"/>',
         '<rect y="1150" width="1080" height="800" fill="url(#c9_s)"/>',
         '<path d="M440 1150 L640 1150 L1200 1920 L-120 1920 Z" fill="#c8b490"/>',
         '<path d="M540 1160 L540 1920" stroke="#a89070" stroke-width="10" stroke-dasharray="40 60" opacity="0.5"/>']
    for side in (-1, 1):  # álamos en perspectiva
        for i in range(8):
            u = (i / 8) ** 1.5
            x = 540 + side * (120 + 700 * (1 - u))
            y = 1150 + 600 * (1 - u)
            s = 0.25 + 1.2 * (1 - u)
            b.append(f'<path d="M{x:.0f} {y:.0f} L{x:.0f} {y-260*s:.0f}" stroke="#4a3a2a" stroke-width="{8*s:.0f}"/>'
                     f'<ellipse cx="{x:.0f}" cy="{y-330*s:.0f}" rx="{55*s:.0f}" ry="{190*s:.0f}" fill="#5a6040"/>'
                     f'<ellipse cx="{x-12*s:.0f}" cy="{y-350*s:.0f}" rx="{30*s:.0f}" ry="{140*s:.0f}" fill="#7a8058" opacity="0.7"/>')
    b.append('<rect width="1080" height="1920" fill="#7a5a2a" opacity="0.12"/>')
    b.append('<rect width="1080" height="1920" fill="#888" filter="url(#grano)"/>')
    guardar(nombre, "".join(b), defs=d)


def bg_paris_1899(nombre="bg_paris_1899"):
    """Horizonte al atardecer con una torre de hierro de celosía y tejados (tono de época)."""
    d = lg("pa_c", (0, "#6a5a7a"), (0.5, "#e0a878"), (0.7, "#f4d8a8")) + lg("pa_t", (0, "#3a3040"), (1, "#1a1420"))
    b = ['<rect width="1080" height="1920" fill="url(#pa_c)"/>', '<circle cx="300" cy="1050" r="120" fill="#fff0c8" opacity="0.8"/>']
    # torre de celosía
    b.append('<path d="M620 1250 L700 450 L716 450 L796 1250 L760 1250 L720 900 L696 900 L656 1250 Z" fill="#2a2030"/>')
    b.append('<path d="M640 1100 L776 1100 M660 950 L756 950 M680 750 L736 750" stroke="#2a2030" stroke-width="14"/>')
    b.append('<path d="M690 1250 Q708 1150 726 1250" fill="#e0a878"/><path d="M706 450 L708 380" stroke="#2a2030" stroke-width="6"/>')
    for i in range(20):  # tejados
        x = i * 60 - 20
        hh = 120 + (i * 53) % 110
        b.append(f'<rect x="{x}" y="{1250-hh}" width="62" height="{hh}" fill="#3a3040"/><path d="M{x} {1250-hh} L{x+31} {1220-hh} L{x+62} {1250-hh} Z" fill="#4a4050"/>')
        if i % 3 == 0:
            b.append(f'<rect x="{x+20}" y="{1210-hh}" width="10" height="26" fill="#3a3040"/>')
    b.append('<rect y="1250" width="1080" height="700" fill="url(#pa_t)"/>')
    b.append('<rect width="1080" height="1920" fill="#7a5a2a" opacity="0.10"/><rect width="1080" height="1920" fill="#888" filter="url(#grano)"/>')
    guardar(nombre, "".join(b), defs=d)


def motor_electrico(nombre="motor_electrico"):
    """Motor eléctrico antiguo: carcasa cilíndrica abierta con bobinas de cobre y un rayo."""
    w, h = 700, 520
    d = lg("me_c", (0, "#8a8a92"), (1, "#3a3a42")) + lg("me_k", (0, "#ffb070"), (1, "#a8501a"))
    b = ['<rect x="80" y="100" width="540" height="320" rx="60" fill="url(#me_c)"/>',
         '<rect x="140" y="150" width="420" height="220" rx="30" fill="#1a1a20"/>']
    for i in range(9):
        b.append(f'<rect x="{160+i*44}" y="170" width="32" height="180" rx="12" fill="url(#me_k)"/><path d="M{166+i*44} 180 L{166+i*44} 340" stroke="#fff" stroke-width="4" opacity="0.4"/>')
    b.append('<rect x="620" y="235" width="70" height="50" rx="10" fill="#c0c0c8"/>')
    b.append('<path d="M330 30 L290 120 L340 120 L300 200 L400 90 L350 90 L390 30 Z" fill="#ffe93d" stroke="#fff" stroke-width="4"/>')
    guardar(nombre, "".join(b), w, h, d)


def bandera_cuadros(nombre="bandera_cuadros"):
    w, h = 520, 420
    b = ['<path d="M40 20 L40 400" stroke="#5a4030" stroke-width="16"/>']
    for i in range(6):
        for j in range(4):
            if (i + j) % 2 == 0:
                b.append(f'<rect x="{56+i*72}" y="{30+j*72+ (i*6)}" width="72" height="72" fill="#111"/>')
            else:
                b.append(f'<rect x="{56+i*72}" y="{30+j*72+ (i*6)}" width="72" height="72" fill="#f4f4f4"/>')
    guardar(nombre, "".join(b), w, h)


def taxi_1900(nombre="taxi_1900", col="#2a4a7a"):
    """Coche de punto eléctrico de 1900: cabina cerrada delante para el pasajero y el conductor sentado detrás, arriba."""
    w, h = 1000, 760
    d = lg(f"{nombre}_c", (0, "#ffffff"), (0.15, col), (1, "#0a1a30"))
    b = ['<ellipse cx="500" cy="730" rx="420" ry="14" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         f'<path d="M220 600 L240 300 C260 240 520 240 560 300 L600 600 Z" fill="url(#{nombre}_c)"/>',
         '<path d="M290 320 L510 320 L530 450 L280 450 Z" fill="#c8e0f0" opacity="0.8"/><path d="M300 330 L500 330" stroke="#fff" stroke-width="6" opacity="0.6"/>',
         f'<path d="M560 600 L600 360 L780 360 L800 600 Z" fill="{col}"/>',
         '<path d="M640 360 L640 220 C640 200 760 200 760 220 L760 360 Z" fill="#1a1a1a"/>',  # asiento alto
         '<circle cx="700" cy="170" r="34" fill="#d8a888"/><path d="M660 150 L740 150 L736 120 L664 120 Z" fill="#1a1a1a"/><path d="M650 152 L750 152" stroke="#1a1a1a" stroke-width="8"/>',
         '<path d="M660 210 L740 210 L760 340 L640 340 Z" fill="#3a2a20"/>',
         '<circle cx="190" cy="360" r="22" fill="#ffe8a0"/><circle cx="190" cy="360" r="60" fill="#ffe8a0" opacity="0.25" filter="url(#blur20)"/>']
    b.append(_rueda(260, 620, 90, 12)); b.append(_rueda(720, 600, 120, 14))
    guardar(nombre, "".join(b), w, h, d)


def bg_ciudad_1900(nombre="bg_ciudad_1900"):
    """Calle de una gran ciudad hacia 1900: edificios de ladrillo y piedra, farolas, adoquines (sin rótulos)."""
    r = random.Random(51)
    d = lg("cn_c", (0, "#a8b8c8"), (1, "#e8dcc8")) + lg("cn_s", (0, "#6a5a4a"), (1, "#3a2e24"))
    b = ['<rect width="1080" height="1920" fill="url(#cn_c)"/>']
    for i in range(8):
        x = i * 140 - 30; hh = r.uniform(600, 1000); col = r.choice(["#8a4a3a", "#9a8a72", "#7a5a4a", "#a89a80"])
        b.append(f'<rect x="{x}" y="{1300-hh:.0f}" width="146" height="{hh:.0f}" fill="{col}"/><rect x="{x}" y="{1300-hh:.0f}" width="146" height="20" fill="#3a2e24"/>')
        for k in range(int(hh / 110)):
            for j in range(3):
                b.append(f'<rect x="{x+18+j*42}" y="{1340-hh+k*110:.0f}" width="26" height="54" fill="#2a3040"/><rect x="{x+18+j*42}" y="{1340-hh+k*110:.0f}" width="26" height="8" fill="#e8dcc8" opacity="0.5"/>')
    b.append('<rect y="1300" width="1080" height="650" fill="url(#cn_s)"/>')
    for k in range(16):
        for j in range(14):
            b.append(f'<rect x="{j*80 + (k%2)*40 - 20}" y="{1310+k*40}" width="74" height="34" rx="8" fill="#5a4a3a" opacity="0.6"/>')
    for x in (120, 960):
        b.append(f'<path d="M{x} 1500 L{x} 1000" stroke="#1a1a1a" stroke-width="14"/><path d="M{x-30} 1000 L{x+30} 1000 L{x+20} 950 L{x-20} 950 Z" fill="#ffe8a0"/>')
    b.append('<rect width="1080" height="1920" fill="#7a5a2a" opacity="0.10"/><rect width="1080" height="1920" fill="#888" filter="url(#grano)"/>')
    guardar(nombre, "".join(b), defs=d)


def coche_1912(nombre="coche_1912"):
    """Coche de gasolina negro de principios de siglo (genérico), con radiador y manivela delante; tubo de escape."""
    w, h = 1100, 640
    d = lg(f"{nombre}_c", (0, "#5a5a62"), (0.2, "#1a1a20"), (1, "#050508"))
    b = ['<ellipse cx="560" cy="610" rx="460" ry="14" fill="#000" opacity="0.45" filter="url(#blur8)"/>',
         f'<path d="M180 470 L200 330 L470 330 L500 220 L740 220 L760 330 L960 360 L980 470 Z" fill="url(#{nombre}_c)"/>',
         '<path d="M510 230 L730 230 L748 320 L500 320 Z" fill="#c8e0f0" opacity="0.6"/>',
         '<path d="M500 210 L760 210 L770 190 L490 190 Z" fill="#111"/>',
         '<rect x="930" y="330" width="60" height="140" rx="8" fill="#b89040"/>' + "".join(f'<path d="M940 {345+i*16} L980 {345+i*16}" stroke="#5a4020" stroke-width="5"/>' for i in range(8)),
         '<path d="M990 440 L1040 440 L1040 480" stroke="#888" stroke-width="10" fill="none"/>',  # manivela
         '<circle cx="1000" cy="300" r="22" fill="#ffe8a0"/>',
         '<path d="M180 490 L120 500" stroke="#555" stroke-width="12"/>']
    b.append(_rueda(320, 500, 100, 12)); b.append(_rueda(840, 500, 100, 12))
    guardar(nombre, "".join(b), w, h, d)


def manivela(nombre="manivela"):
    """Manivela de arranque: palanca en Z con mango de madera (rota alrededor del centro del lienzo)."""
    w, h = 600, 600
    b = ('<circle cx="300" cy="300" r="40" fill="#888" stroke="#ccc" stroke-width="6"/>'
         '<path d="M300 300 L300 110 L380 110" stroke="#9aa0a8" stroke-width="30" fill="none" stroke-linejoin="round"/>'
         '<rect x="370" y="80" width="150" height="60" rx="28" fill="#8a5a2a"/><rect x="380" y="88" width="130" height="14" rx="7" fill="#c89060" opacity="0.7"/>')
    guardar(nombre, b, w, h)


def humo(nombre="humo"):
    w, h = 700, 500
    b = "".join(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="#5a5a5a" opacity="0.55"/>' for x, y, rr in [(200, 300, 120), (330, 240, 140), (470, 290, 120), (560, 220, 90), (300, 360, 100)])
    guardar(nombre, f'<g filter="url(#blur8)">{b}</g>', w, h)


def etiqueta_precio(nombre, texto_cifra, col):
    """Etiqueta de precio colgante con una cifra grande (se pone por motor como rótulo encima; aquí solo la forma)."""
    w, h = 520, 340
    b = (f'<path d="M120 40 L480 40 L480 300 L120 300 L20 170 Z" fill="{col}" stroke="#fff" stroke-width="8"/>'
         '<circle cx="90" cy="170" r="22" fill="#fff"/><path d="M90 170 L0 60" stroke="#fff" stroke-width="5"/>')
    guardar(nombre, b, w, h)


def surtidor(nombre="surtidor"):
    """Surtidor de gasolina antiguo con esfera de cristal arriba (genérico)."""
    w, h = 400, 1000
    d = lg("su_c", (0, "#ff6a4a"), (1, "#8a1a10"), x2=1, y2=0)
    b = ('<rect x="110" y="300" width="180" height="620" rx="24" fill="url(#su_c)"/><circle cx="200" cy="200" r="110" fill="#fff4c8" stroke="#c0c0c0" stroke-width="12"/>'
         '<circle cx="200" cy="200" r="70" fill="#ffd060" opacity="0.6"/><rect x="80" y="900" width="240" height="60" rx="10" fill="#3a3a3a"/>'
         '<path d="M290 450 C380 470 380 640 330 700" stroke="#1a1a1a" stroke-width="18" fill="none"/><rect x="310" y="690" width="40" height="80" rx="8" fill="#888"/>'
         '<rect x="140" y="420" width="120" height="120" rx="10" fill="#fff" opacity="0.9"/>')
    guardar(nombre, b, w, h, d)


def electrico_moderno(nombre="electrico_moderno"):
    """Coche eléctrico actual genérico (sin marca), con cable de carga enchufado."""
    w, h = 1200, 520
    d = lg(f"{nombre}_c", (0, "#ffffff"), (0.3, "#c8d8e8"), (1, "#4a5a70"))
    b = ['<ellipse cx="600" cy="490" rx="520" ry="16" fill="#000" opacity="0.4" filter="url(#blur8)"/>',
         f'<path d="M80 400 C80 330 140 300 260 290 L420 200 C520 160 760 160 860 210 L1000 290 C1100 300 1140 340 1140 400 L1130 430 L90 430 Z" fill="url(#{nombre}_c)"/>',
         '<path d="M440 215 C540 180 740 180 840 222 L880 280 L420 280 Z" fill="#1a2a3a"/><path d="M460 222 L860 240" stroke="#fff" stroke-width="5" opacity="0.4"/>',
         '<path d="M1060 330 L1130 340" stroke="#ff3d3d" stroke-width="12"/><path d="M90 340 L160 330" stroke="#2ff3ff" stroke-width="10"/>',
         '<path d="M240 320 C150 330 120 420 60 520" stroke="#1a1a1a" stroke-width="16" fill="none"/><rect x="225" y="305" width="40" height="34" rx="6" fill="#2ff3ff"/>']
    for cx in (300, 900):
        b.append(f'<circle cx="{cx}" cy="430" r="80" fill="#111"/><circle cx="{cx}" cy="430" r="46" fill="#c0c8d0"/><circle cx="{cx}" cy="430" r="14" fill="#333"/>')
    guardar(nombre, "".join(b), w, h, d)


def bg_estudio(nombre="bg_estudio", c1="#0a1a2a", c2="#020610"):
    """Fondo de estudio oscuro con viñeta y suelo reflectante."""
    d = rg("es_c", (0, "#2a4a6a", 1), (0.6, c1, 1), (1, c2, 1), cy=0.45, r=0.7) + lg("es_s", (0, "#16202c"), (1, "#05080c"))
    b = ['<rect width="1080" height="1920" fill="url(#es_c)"/>', '<rect y="1380" width="1080" height="540" fill="url(#es_s)"/>',
         '<path d="M-40 1380 L1120 1380" stroke="#2ff3ff" stroke-width="4" opacity="0.35"/>',
         '<rect width="1080" height="1920" fill="#888" filter="url(#grano)"/>']
    guardar(nombre, "".join(b), defs=d)


def generar(dirsvg):
    ilus.OUT = dirsvg
    # 01
    bg_rio_fondo(); bg_sabana("bg_sabana", "tarde"); bg_sabana("bg_sabana_tierra", "tarde", rio=False); bg_sabana("bg_sabana_dia", "dia")
    hipo("hipo"); hipo("hipo_salto", salto=True); hipo("hipo_dormido", ojo_cerrado=True)
    hipo_cabeza("hipo_cabeza"); hipo_cabeza("hipo_cabeza_cerrada", cerrado=True)
    piel_gotas(); gota_color("gota_roja", "#ffb070", "#d8301a"); gota_color("gota_sudor", "#e8fbff", "#7ac8f0"); gota_color("gota_sangre", "#ff5a5a", "#8a0a0a")
    crema_solar(); bacteria("bacteria"); bacteria("bacteria2", "#ff3df2"); pantalla_video(); pesa_tonelada()
    # 02
    f1("f1"); f1("f1_b", "#e8e8f0", "#7d3aff"); bg_tunel(); bg_pista(); perfil_ala("perfil_ala"); perfil_ala("perfil_alerón".replace("ó", "o"), invertido=True)
    avion(); velocimetro(); aguja_vel(); motor_bloque(); curva_arriba(); f1_arriba(); bg_estudio()
    # 03
    bolido_1899(); bg_campo_1899(); bg_paris_1899(); motor_electrico(); bandera_cuadros(); taxi_1900(); taxi_1900("taxi_1900_b", "#6a2a3a")
    bg_ciudad_1900(); coche_1912(); manivela(); humo(); etiqueta_precio("etiqueta_verde", "", "#2a9a4a"); etiqueta_precio("etiqueta_roja", "", "#c0392b")
    surtidor(); electrico_moderno()
    return dirsvg


if __name__ == "__main__":
    generar(sys.argv[1])
    print("SVG en", sys.argv[1])
