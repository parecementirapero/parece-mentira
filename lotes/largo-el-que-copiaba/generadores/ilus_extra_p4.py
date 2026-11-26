"""Corto (estilo B «focos y contadores»): versiones apagadas y casi en gris de los fondos (`<fondo>_b.svg`).
Se hacen envolviendo el SVG original en un filtro (saturación 0,12 y brillo ×0,5)."""
import os, re

FONDOS = ["bg_aula", "bg_ciudad", "bg_calle_dia", "bg_cafe_dentro", "bg_cafe_dentro_triste", "bg_estudio_oscuro", "bg_colegio_fuera"]
FILTRO = ('<filter id="desatB" x="0" y="0" width="100%" height="100%"><feColorMatrix type="saturate" values="0.12"/>'
          '<feComponentTransfer><feFuncR type="linear" slope="0.48"/><feFuncG type="linear" slope="0.48"/>'
          '<feFuncB type="linear" slope="0.56"/></feComponentTransfer></filter>')


def generar(dirsvg):
    out = []
    for f in FONDOS:
        src = os.path.join(dirsvg, f + ".svg")
        if not os.path.exists(src):
            continue
        t = open(src, encoding="utf-8").read()
        m = re.search(r"<svg[^>]*>", t)
        i = m.end()
        t2 = t[:i] + "<defs>" + FILTRO + "</defs><g filter=\"url(#desatB)\">" + t[i:]
        t2 = t2[::-1].replace(">gvs/<", ">gvs/<>g/<", 1)[::-1]
        open(os.path.join(dirsvg, f + "_b.svg"), "w", encoding="utf-8").write(t2)
        out.append(f + "_b")
    return out
