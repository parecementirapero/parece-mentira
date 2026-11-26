import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
A='/tmp/cp/_arte/'; FB='/home/claude/parece-mentira/motor/fuentes/Poppins-Bold.ttf'
def png(n,h=None,w=None):
    o=f'/tmp/cp/port/{n}_{h}_{w}.png'
    subprocess.run(['rsvg-convert']+(['-h',str(h)] if h else ['-w',str(w)])+[A+n+'.svg','-o',o],check=True)
    return Image.open(o).convert('RGBA')
W,H=1280,720
izq=png('bg_aula_h',w=1280).crop((0,0,1280,720))
der=png('bg_ciudad_h',w=1280).crop((0,0,1280,720))
# izquierda: Lucas niño copiando
lk=png('lucas_nino_reojo',h=430); izq.alpha_composite(lk,(170,700-lk.height+5))
pu=png('pupitre',h=230); izq.alpha_composite(pu,(170+lk.width//2-pu.width//2,700-pu.height+10))
ex=png('examen',h=250); ex=ex.rotate(12,expand=True); izq.alpha_composite(ex,(40,330))
# derecha: Lucas adulto con su local y cola
ham=png('hamburgueseria_lucas',h=420); der.alpha_composite(ham,(860,640-ham.height+5))
for i in range(6):
    c=png(f'cola_{i}',h=330); der.alpha_composite(c,(760-i*72-c.width//2,650-c.height))
lu=png('lucas_contento',h=470); der.alpha_composite(lu,(1060,700-lu.height+10))
# unir en diagonal
m=Image.new('L',(W,H),0); d=ImageDraw.Draw(m); d.polygon([(560,0),(W,0),(W,H),(470,H)],fill=255)
F=izq.copy(); F.paste(der,(0,0),m)
d=ImageDraw.Draw(F); d.line([(560,0),(470,H)],fill=(255,207,106),width=10)
# texto
def txt(t,xy,tam,color,stroke=10):
    f=ImageFont.truetype(FB,tam); d.text(xy,t,font=f,fill=color,stroke_width=stroke,stroke_fill=(15,15,20))
txt('EL QUE',(40,20),96,'white'); txt('COPIABA',(40,115),120,'white'); txt('GANÓ',(780,40),150,(255,207,106),12)
F.convert('RGB').save('/tmp/cp/port/portada-16x9.jpg',quality=92)
