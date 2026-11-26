import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps, ImageChops
D='/tmp/fr/c/'; FB='/home/claude/parece-mentira/motor/fuentes/Poppins-Bold.ttf'
def png(n, h=None, w=None):
    out=f'/tmp/fr/v_{n}_{h}_{w}.png'
    subprocess.run(['rsvg-convert']+(['-h',str(h)] if h else ['-w',str(w)])+[D+n+'.svg','-o',out],check=True)
    return Image.open(out).convert('RGBA')
BG=png('bg_ciudad_v', w=1080)
SUELO=1440
tienda=png('hamburgueseria', h=560)
cola=[png(f'cola_{i}', h=400) for i in range(4)]
lucas=png('lucas_piensa', h=620)
bocad=png('pensamiento_cola', w=360)
def capas(tf=lambda im:im, bgf=lambda im:im):
    F=bgf(BG.copy())
    F.alpha_composite(tf(tienda),(1080-tienda.width+170, SUELO-tienda.height+10))
    for i,x in reversed(list(enumerate([830,740,650,560]))):
        p=tf(cola[i]); F.alpha_composite(p,(int(x-p.width/2), SUELO+8-p.height+int(25*p.height/960)))
    l=tf(lucas); F.alpha_composite(l,(150-60, SUELO+260-l.height))
    return F
def sub(F, pal, hi, y=330, tam=66):
    d=ImageDraw.Draw(F); f=ImageFont.truetype(FB,tam)
    an=[d.textlength(w+' ',font=f) for w in pal]; x=(1080-sum(an))/2
    for i,(w,a) in enumerate(zip(pal,an)):
        if i==hi:
            bb=d.textbbox((x,y),w,font=f); d.rounded_rectangle((bb[0]-10,bb[1]-8,bb[2]+10,bb[3]+10),12,fill=(32,58,140,235),outline=(90,130,230),width=3)
        d.text((x+3,y+3),w,font=f,fill=(0,0,0,170)); d.text((x,y),w,font=f,fill='white'); x+=a
def hud(F, etiqueta, valor, x, y, col='white'):
    d=ImageDraw.Draw(F)
    d.text((x,y),etiqueta,font=ImageFont.truetype(FB,30),fill=(200,200,210),anchor='mm')
    d.text((x,y+52),valor,font=ImageFont.truetype(FB,78),fill=col,anchor='mm')
def foco(F, cx, top, ancho, alpha=95):
    cap=Image.new('RGBA',F.size,(0,0,0,0)); d=ImageDraw.Draw(cap)
    d.polygon([(cx-60,top),(cx+60,top),(cx+ancho,SUELO+40),(cx-ancho,SUELO+40)],fill=(255,240,210,alpha))
    d.ellipse((cx-ancho,SUELO+5,cx+ancho,SUELO+75),fill=(255,240,210,alpha+30))
    F.alpha_composite(cap.filter(ImageFilter.GaussianBlur(28)))
out=[]
# A — estilo cueva tal cual
A=capas(); A.alpha_composite(bocad,(60,640)); sub(A,['Y','se','fija','en','una','cosa:'],2); out.append(('A · Color, como la cueva',A))
# B — noche desaturada + focos + HUD (color solo en lo importante)
def apaga(im): 
    g=ImageEnhance.Color(im).enhance(0.15); return ImageEnhance.Brightness(g).enhance(0.45)
B=capas(bgf=apaga); foco(B,150,560,230); foco(B,700,560,330,70)
B.alpha_composite(bocad,(60,640)); hud(B,'CLIENTES',' 1.284',780,560,(255,207,106)); hud(B,'LUCAS','2 LOCALES',260,560)
sub(B,['Y','se','fija','en','una','cosa:'],2); out.append(('B · Focos y contadores',B))
# C — siluetas a contraluz con borde dorado
def silueta(im):
    a=im.split()[3]; base=Image.new('RGBA',im.size,(14,16,26,255)); base.putalpha(a)
    borde=ImageChops.subtract(a, a.filter(ImageFilter.MinFilter(7)))
    rim=Image.new('RGBA',im.size,(255,196,110,255)); rim.putalpha(borde.filter(ImageFilter.GaussianBlur(1.5)))
    base.alpha_composite(rim); return base
def ocaso(im):
    g=Image.new('RGBA',im.size); d=ImageDraw.Draw(g)
    for y in range(im.height):
        t=y/im.height; d.line([(0,y),(im.width,y)],fill=(int(250-120*t),int(150-90*t),int(80-20*t),255))
    return Image.blend(g, ImageEnhance.Brightness(im).enhance(0.6), 0.35)
C=ocaso(BG.copy())
C.alpha_composite(tienda,(1080-tienda.width+170, SUELO-tienda.height+10))
for i,x in reversed(list(enumerate([830,740,650,560]))):
    p=silueta(cola[i]); C.alpha_composite(p,(int(x-p.width/2), SUELO+8-p.height+int(25*p.height/960)))
l=silueta(lucas); C.alpha_composite(l,(90, SUELO+260-l.height))
C.alpha_composite(bocad,(60,640)); sub(C,['Y','se','fija','en','una','cosa:'],2); out.append(('C · Contraluz al atardecer',C))
# D — blanco luminoso sobre negro (guiño al de referencia) con nuestros dibujos
def blanco(im):
    g=ImageOps.grayscale(im.convert('RGB')); g=ImageEnhance.Contrast(g).enhance(1.25)
    g=ImageOps.autocontrast(g, cutoff=2).point(lambda v: 120+int(v*0.53))
    w=Image.merge('RGBA',(g,g,g,im.split()[3])); return w
D_=Image.new('RGBA',(1080,1920),(10,10,12,255))
d=ImageDraw.Draw(D_); d.line([(0,SUELO+10),(1080,SUELO+10)],fill=(90,90,96),width=3)
for x in range(0,1080,40): d.line([(x,SUELO+10),(x+20,SUELO+10)],fill=(10,10,12),width=4)
foco(D_,150,420,230,60); foco(D_,700,420,330,45)
t=blanco(tienda); D_.alpha_composite(t,(1080-t.width+170, SUELO-t.height+10))
for i,x in reversed(list(enumerate([830,740,650,560]))):
    p=blanco(cola[i]); D_.alpha_composite(p,(int(x-p.width/2), SUELO+8-p.height+int(25*p.height/960)))
l=blanco(lucas); D_.alpha_composite(l,(90, SUELO+260-l.height))
glow=D_.filter(ImageFilter.GaussianBlur(18)); D_=Image.blend(D_,ImageChops.screen(D_,glow),0.5)
D_.alpha_composite(blanco(bocad),(60,640)); hud(D_,'CLIENTES','1.284',780,560); hud(D_,'IDEAS ORIGINALES','0',260,560)
sub(D_,['Y','se','fija','en','una','cosa:'],2); out.append(('D · Blanco sobre negro',D_))
# hoja
W=Image.new('RGB',(4*540+5*30, 960+110),(20,20,24)); dd=ImageDraw.Draw(W); f=ImageFont.truetype(FB,34)
for k,(t,im) in enumerate(out):
    x=30+k*570; W.paste(im.convert('RGB').resize((540,960)),(x,90)); dd.text((x,30),t,font=f,fill='white')
    im.convert('RGB').save(f'/tmp/fr/boceto_{t[0]}.jpg',quality=92)
W.save('/tmp/fr/bocetos.jpg',quality=90)
