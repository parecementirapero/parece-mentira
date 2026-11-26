import subprocess, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
D='/tmp/fr/c/'
def png(n, h=None, w=None):
    out=f'/tmp/fr/{n}.png'
    a=['rsvg-convert']+(['-h',str(h)] if h else ['-w',str(w)])+[D+n+'.svg','-o',out]
    subprocess.run(a,check=True); return Image.open(out).convert('RGBA')
F=png('bg_ciudad_h', w=1920).convert('RGBA')
SUELO=880
def pon(im, x, suelo, pie=25, oscuro=0.0):
    h=im.height
    if oscuro:
        im=ImageEnhance.Brightness(im).enhance(1-oscuro)
    F.alpha_composite(im, (int(x-im.width/2), int(suelo-h+pie*h/940)))
tienda=png('hamburgueseria', h=620)
F.alpha_composite(tienda,(1920-tienda.width-40, SUELO-tienda.height+10))
# cola: de la puerta hacia la izquierda, más pequeños y oscuros al alejarse no; misma acera
xs=[1440,1335,1230,1125,1020,915]
for i,x in reversed(list(enumerate(xs))):
    p=png(f'cola_{i}', h=440)
    pon(p, x, SUELO+8, oscuro=0.05*i)
lucas=png('lucas_piensa', h=540)
pon(lucas, 360, SUELO+75)
bo=png('pensamiento_cola', w=330)
F.alpha_composite(bo,(370,190))
# subtítulo estilo karaoke del motor (aprox.)
d=ImageDraw.Draw(F)
f=ImageFont.truetype('/home/claude/parece-mentira/motor/fuentes/Poppins-Bold.ttf',62)
pal=['Y','se','fija','en','una','cosa:']
x=0; anchos=[d.textlength(w+' ',font=f) for w in pal]; tot=sum(anchos); x=(1920-tot)/2; y=950
for i,(w,a) in enumerate(zip(pal,anchos)):
    if i==2:
        bb=d.textbbox((x,y),w,font=f); d.rounded_rectangle((bb[0]-10,bb[1]-8,bb[2]+10,bb[3]+10),12,fill=(32,58,140,235),outline=(90,130,230),width=3)
    d.text((x+3,y+3),w,font=f,fill=(0,0,0,160)); d.text((x,y),w,font=f,fill='white'); x+=a
F.convert('RGB').save('/tmp/fr/frame.png')
