import sys,math;sys.path.insert(0,'..');sys.path.insert(0,'.')
from harm import *
from PIL import Image, ImageDraw, ImageFilter
def hx(h):h=h.lstrip('#');return tuple(int(h[i:i+2],16) for i in (0,2,4))
def obj(sh,idx,land,h=None,w=None,outline=0,holes=True):
    c,a=cut(sh,idx,holes=holes);o,a2=gentle(c,a,hx(land))
    if outline:
        big=cv2.dilate(a2,np.ones((3,3),np.uint8),iterations=outline)
        ring=(big>0)&(a2<128);o[ring]=INK;a2=np.maximum(a2,big)
    im=Image.fromarray(np.dstack([o,a2]),'RGBA')
    if h: im=im.resize((int(im.size[0]*h/im.size[1]),h),Image.LANCZOS)
    if w: im=im.resize((w,int(im.size[1]*w/im.size[0])),Image.LANCZOS)
    return im
def shadow(S,cx,y,w,op=70):
    sh=Image.new('RGBA',S.size,(0,0,0,0));ImageDraw.Draw(sh).ellipse((cx-w/2,y-7,cx+w/2,y+7),fill=(0,0,0,op));S.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
def place(S,im,cx,floor,sh=True):
    if sh: shadow(S,cx,floor,im.size[0]*0.85)
    S.alpha_composite(im,(int(cx-im.size[0]/2),int(floor-im.size[1])))
def paste_c(S,im,cx,cy): S.alpha_composite(im,(int(cx-im.size[0]/2),int(cy-im.size[1]/2)))
def arrow(d,x,y1,y2,col,w=9):
    d.rectangle((x-w,y1,x+w,y2-30),fill=col);d.polygon([(x-24,y2-32),(x+24,y2-32),(x,y2)],fill=col)
def dashed_arc(d,p0,p1,p2,col):
    pts=[((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0],(1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1]) for t in [i/60 for i in range(61)]]
    for i in range(0,60,4): d.line(pts[i]+pts[i+2],fill=col,width=6)
W,H,FL=800,540,450
# ---------- LEVER (land2) ----------
bg='#1E576A';S=Image.new('RGBA',(W,H),bg);d=ImageDraw.Draw(S)
for x in range(0,W,40): d.line((x,0,x,FL),fill='#22607A',width=2)
for y in range(0,FL,40): d.line((0,y,W,y),fill='#22607A',width=2)
d.rectangle((0,FL,W,H),fill='#19495A');d.rectangle((0,FL,W,FL+5),fill='#0F3442')
for x in range(250,700,50): d.rounded_rectangle((x-3,FL+18,x+3,FL+36),3,fill='#24637A')
wb=obj('sheet_fix',[10],bg,w=210);place(S,wb,120,FL)
fx=440;wedge=obj('sheet_fix',[11],bg,h=64);place(S,wedge,fx,FL)
pl=obj('sheet2',[0],bg,w=470,outline=2);Lp=pl.size[0]
lx0,ly0=270,FL-12;a=math.atan2((ly0-(FL-68)),(fx-lx0));ang=math.degrees(a)
pr=pl.rotate(ang,expand=True,resample=Image.BICUBIC)
cx=lx0+Lp/2*math.cos(a);cy=ly0-Lp/2*math.sin(a)
st=obj('sheet2',[3],bg,h=100,outline=2,holes=False)
sx=lx0+60*math.cos(a);sy=ly0-60*math.sin(a)
paste_c(S,pr,cx,cy)
S.alpha_composite(st,(int(sx-st.size[0]/2),int(sy-st.size[1]+4)))
rx=lx0+(Lp-14)*math.cos(a);ry=ly0-(Lp-14)*math.sin(a)
d=ImageDraw.Draw(S)
dashed_arc(d,(sx-20,sy-110),(sx-80,sy-260),(130,FL-150),'#F2C14E')
arrow(d,rx,ry-170,ry-22,'#FF94C2')
d.ellipse((rx-18,ry-22,rx+18,ry+14),outline='#FF94C2',width=5)
S.convert('RGB').save('m6/lever.png')
# ---------- BALANCE (land1) ----------
bg='#F2C66D';S=Image.new('RGBA',(W,H),bg);d=ImageDraw.Draw(S)
for x in range(0,W,100): d.rectangle((x,0,x+4,FL),fill='#EABA5E')
d.rectangle((0,FL,W,H),fill='#E3AE52');d.rectangle((0,FL,W,FL+5),fill='#5B3A29')
bal=obj('sheet1',[11,14,15],bg,h=390);place(S,bal,400,FL)
bw,bh=bal.size;x0=400-bw/2;y0=FL-bh
# pans approx: left pan center at 0.18w, right at 0.82w ; pan top ~0.73h
crate=obj('sheet1',[0],bg,h=92);S.alpha_composite(crate,(int(x0+bw*0.17-crate.size[0]/2),int(y0+bh*0.735-crate.size[1])))
w1=obj('sheet1',[5],bg,h=72);S.alpha_composite(w1,(int(x0+bw*0.80-w1.size[0]),int(y0+bh*0.735-w1.size[1])))
w2=obj('sheet1',[9],bg,h=54);S.alpha_composite(w2,(int(x0+bw*0.85),int(y0+bh*0.735-w2.size[1])))
S.convert('RGB').save('m6/balance.png')
# weights for tray
for i,(idx,h) in enumerate([(8,50),(9,60),(4,70),(5,80)]):
    obj('sheet1',[idx],bg,h=h).save(f'm6/w{i}.png')
# ---------- badges ----------
bi=Image.open('badges_color.png').convert('RGB');cw=(1013-14)/6
rows=[(17,190),(203,375),(388,560)]
sel=[(0,0),(0,2),(0,3),(0,4),(1,0),(1,1),(1,3),(1,5),(2,0),(2,1),(2,3),(2,5)]
for k,(r,c) in enumerate(sel):
    x=14+c*cw;y0_,y1_=rows[r];cyb=(y0_+y1_)/2;cxb=x+cw/2;R=min(cw,y1_-y0_)/2-2
    cr=bi.crop((int(cxb-R),int(cyb-R),int(cxb+R),int(cyb+R))).resize((240,240),Image.LANCZOS)
    m=Image.new('L',(240,240),0);ImageDraw.Draw(m).ellipse((6,6,233,233),fill=255)
    o=Image.new('RGBA',(240,240));o.paste(cr,(0,0),m);o.save(f'm6/b{k+1}.png')
