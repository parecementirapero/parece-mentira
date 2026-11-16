"""Ilustraciones extra para la v2 «densa» del lote 2026-11-16-tarde: detalles secundarios que se mueven
(gato, polilla, reloj de pared, llaves, taza, planta, calendario de hojas) y piezas de la prueba de la Luna
(satélite, fondos de espacio ricos, superficie, cohete). Uso: python3 ilus_extra.py"""
import os, shutil, subprocess, tempfile
from base import guardar, lg, rg, grano, OUT, AQUI, R

LUNA = os.path.join(AQUI, "..", "..", "prueba-luna-densa", "ilus_luna.py")


def gato(nombre="gato"):
    """Gato atigrado caminando de perfil hacia la derecha (lienzo 520x340)."""
    d = lg("pelo", (0, "#e0a060"), (1, "#a8662e")) + lg("panza", (0, "#f2d2a8"), (1, "#d8a870"))
    b = ['<ellipse cx="260" cy="326" rx="200" ry="12" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<path d="M80 150 Q40 60 90 30 Q70 90 110 150 Z" fill="#a8662e"/>',  # cola
         '<rect x="110" y="200" width="34" height="120" rx="16" fill="#a8662e"/><rect x="330" y="200" width="34" height="120" rx="16" fill="#a8662e"/>',
         '<ellipse cx="250" cy="190" rx="170" ry="70" fill="url(#pelo)"/>',
         '<ellipse cx="250" cy="225" rx="130" ry="30" fill="url(#panza)" opacity="0.8"/>',
         '<rect x="150" y="200" width="34" height="122" rx="16" fill="url(#pelo)"/><rect x="370" y="200" width="34" height="122" rx="16" fill="url(#pelo)"/>']
    for i in range(5):
        b.append(f'<path d="M{170+i*40} 128 q10 30 0 60" stroke="#8a4e1e" stroke-width="10" fill="none" opacity="0.7"/>')
    b += ['<circle cx="420" cy="130" r="62" fill="url(#pelo)"/>',
          '<path d="M378 90 L390 30 L420 78 Z M440 78 L470 30 L476 96 Z" fill="#a8662e"/>',
          '<path d="M388 84 L394 50 L410 78 Z" fill="#f2a8a0"/>',
          '<ellipse cx="440" cy="124" rx="10" ry="13" fill="#2a3a1a"/><ellipse cx="443" cy="120" rx="3" ry="4" fill="#fff"/>',
          '<ellipse cx="478" cy="146" rx="9" ry="6" fill="#d86a6a"/>',
          '<path d="M470 156 L520 150 M470 162 L520 168" stroke="#fff" stroke-width="2" opacity="0.8"/>',
          '<path d="M420 70 Q446 64 470 84" stroke="#fff" stroke-width="5" fill="none" opacity="0.35"/>']
    guardar(nombre, "".join(b), 520, 340, d)


def polilla():
    d = rg("ala", (0, "#efe2c8", 1), (1, "#a8916a", 1))
    b = ['<ellipse cx="60" cy="60" rx="52" ry="34" fill="url(#ala)" transform="rotate(-25 60 60)"/>',
         '<ellipse cx="140" cy="60" rx="52" ry="34" fill="url(#ala)" transform="rotate(25 140 60)"/>',
         '<circle cx="62" cy="58" r="10" fill="#7a6040" opacity="0.6"/><circle cx="138" cy="58" r="10" fill="#7a6040" opacity="0.6"/>',
         '<ellipse cx="100" cy="74" rx="14" ry="38" fill="#6a5434"/>',
         '<path d="M94 40 Q80 10 70 8 M106 40 Q120 10 130 8" stroke="#6a5434" stroke-width="3" fill="none"/>']
    guardar("polilla", "".join(b), 200, 130, d)


def reloj_pared():
    d = rg("esf", (0, "#ffffff", 1), (1, "#e8e0cc", 1))
    b = ['<circle cx="150" cy="156" r="140" fill="#000" opacity="0.35" filter="url(#blur8)"/>',
         '<circle cx="150" cy="150" r="140" fill="#3a2a1a"/><circle cx="150" cy="150" r="118" fill="url(#esf)"/>']
    for i in range(12):
        import math
        a = math.radians(i * 30)
        b.append(f'<rect x="146" y="40" width="8" height="{22 if i % 3 == 0 else 12}" fill="#2a2a30" transform="rotate({i*30} 150 150)"/>')
    guardar("reloj_pared", "".join(b), 300, 300, d)
    guardar("aguja_larga", '<rect x="16" y="0" width="8" height="110" rx="4" fill="#2a2a30"/>', 40, 220)
    guardar("aguja_corta", '<rect x="15" y="40" width="10" height="70" rx="5" fill="#2a2a30"/>', 40, 220)


def llaves():
    b = ('<circle cx="80" cy="90" r="58" fill="none" stroke="#e8b830" stroke-width="22"/><circle cx="80" cy="90" r="58" fill="none" stroke="#fff3b0" stroke-width="5" opacity="0.6"/>'
         '<rect x="128" y="78" width="200" height="26" rx="6" fill="#e8b830"/><rect x="270" y="100" width="20" height="40" fill="#e8b830"/>'
         '<rect x="300" y="100" width="18" height="28" fill="#e8b830"/><rect x="128" y="78" width="200" height="8" fill="#fff3b0" opacity="0.6"/>'
         '<circle cx="110" cy="190" r="40" fill="none" stroke="#9aa6b2" stroke-width="16"/>')
    guardar("llaves", b, 360, 250)


def taza():
    d = lg("cer", (0, "#ffffff"), (1, "#c9d3de"), x2=1, y2=0)
    b = ('<path d="M40 60 L220 60 L200 240 Q130 270 60 240 Z" fill="url(#cer)"/>'
         '<path d="M220 100 Q290 110 280 170 Q270 220 205 210" stroke="#c9d3de" stroke-width="22" fill="none"/>'
         '<ellipse cx="130" cy="60" rx="90" ry="20" fill="#5a3418"/><rect x="70" y="120" width="120" height="40" rx="10" fill="#3fa0a8"/>')
    guardar("taza", b, 300, 280, d)


def planta():
    b = ['<path d="M70 300 L230 300 L210 420 L90 420 Z" fill="#c0603a"/><rect x="60" y="290" width="180" height="26" rx="8" fill="#a84e2e"/>']
    for i in range(9):
        x = 150 + R.uniform(-60, 60)
        b.append(f'<path d="M150 300 Q{x:.0f} {200-i*10} {x+R.uniform(-60,60):.0f} {R.uniform(20,160):.0f}" stroke="#2f7a3a" stroke-width="10" fill="none"/>'
                 f'<ellipse cx="{x+R.uniform(-40,40):.0f}" cy="{R.uniform(40,200):.0f}" rx="34" ry="14" fill="#3f9a4a" transform="rotate({R.uniform(-60,60):.0f} 150 150)"/>')
    guardar("planta", "".join(b), 300, 430)


def hoja_calendario(nombre, texto, color="#e8402f"):
    b = (f'<rect x="10" y="10" width="280" height="320" rx="18" fill="#fffaf0"/><rect x="10" y="10" width="280" height="80" rx="18" fill="{color}"/>'
         f'<rect x="10" y="60" width="280" height="30" fill="{color}"/>'
         f'<text x="150" y="58" font-family="DejaVu Sans" font-weight="bold" font-size="40" fill="#fff" text-anchor="middle">AÑO</text>'
         f'<text x="150" y="250" font-family="DejaVu Sans" font-weight="bold" font-size="130" fill="#2a2a33" text-anchor="middle">{texto}</text>')
    guardar(nombre, b, 300, 340)


def de_la_luna():
    tmp = tempfile.mkdtemp()
    subprocess.run(["python3", LUNA, tmp], check=True, capture_output=True)
    for src, dst in (("satelite", "satelite"), ("cohete", "cohete"), ("bg_esp_violeta", "bg_esp_violeta"), ("bg_esp_petroleo", "bg_esp_petroleo"),
                     ("bg_esp_ambar", "bg_esp_ambar"), ("bg_superficie_rica", "bg_superficie_rica"), ("modulo_lunar", "modulo_lunar_det"),
                     ("calendario", "calendario")):
        p = os.path.join(tmp, src + ".svg")
        if os.path.exists(p):
            shutil.copy(p, os.path.join(OUT, dst + ".svg"))
        else:
            print("falta", src)


def todo():
    gato(); polilla(); reloj_pared(); llaves(); taza(); planta()
    hoja_calendario("hoja_1", "1"); hoja_calendario("hoja_30", "30", "#3a8ad0"); hoja_calendario("hoja_60", "60", "#1f9a5a")
    de_la_luna()


if __name__ == "__main__":
    todo()
    print("ok")


def bg_taller():
    """Sala de control de los años 60: pared azul con paneles, armarios de ordenadores con luces, mesa (lienzo completo)."""
    d = (lg("pared_t", (0, "#2a3a5a"), (0.6, "#1d2430"), (1, "#0b0f16")) + lg("mesa_t", (0, "#5a4a3a"), (1, "#2a2016")) +
         rg("lamp_t", (0, "#cfe0ff", 0.5), (1, "#cfe0ff", 0)))
    b = ['<rect width="1080" height="1920" fill="url(#pared_t)"/>', '<circle cx="540" cy="300" r="700" fill="url(#lamp_t)"/>']
    for i in range(6):  # armarios de cintas y luces
        x = 20 + i * 180
        b.append(f'<rect x="{x}" y="420" width="150" height="760" rx="8" fill="#3a4658"/><rect x="{x+10}" y="440" width="130" height="200" rx="6" fill="#1a2230"/>')
        b.append(f'<circle cx="{x+45}" cy="540" r="40" fill="#0d1218" stroke="#7a8696" stroke-width="6"/><circle cx="{x+105}" cy="540" r="40" fill="#0d1218" stroke="#7a8696" stroke-width="6"/>')
        for j in range(12):
            c = R.choice(["#ffb05a", "#7dff3a", "#ff4a3a", "#2ff3ff", "#3a4658"])
            b.append(f'<circle cx="{x+25+(j%4)*33}" cy="{700+(j//4)*40}" r="9" fill="{c}" opacity="0.9"/>')
        b.append(f'<rect x="{x}" y="420" width="18" height="760" fill="#fff" opacity="0.06"/>')
    b += ['<rect y="1180" width="1080" height="740" fill="#141a24"/>',
          '<path d="M0 1400 L1080 1400 L1080 1480 L0 1480 Z" fill="url(#mesa_t)"/><rect y="1400" width="1080" height="10" fill="#8a7a62" opacity="0.6"/>',
          '<rect y="1480" width="1080" height="440" fill="#0d1218"/>', grano()]
    guardar("bg_taller", "".join(b), defs=d)


bg_taller()
