import sys,math,json;sys.path.insert(0,'.')
exec(open('m6/scenes.py').read().split("W,H,FL=800,540,450")[0])
from PIL import ImageDraw
bg='#F2C66D';W,H,FL=800,820,720
c,a=cut('sheet1',[11,14,15]);o,a2=gentle(c,a,hx(bg))
big=cv2.dilate(a2,np.ones((3,3),np.uint8));ring=(big>0)&(a2<128);o[ring]=INK;a2=np.maximum(a2,big)
X0,Y0=289-6,448-6
h,w=a2.shape;yy,xx=np.mgrid[0:h,0:w];sx=xx+X0;sy=yy+Y0
# light wood (ivory) recolour: wood pixels only
o=cv2.bilateralFilter(o,7,30,7)
lab=cv2.cvtColor(o,cv2.COLOR_RGB2LAB).astype(float)
hsv=cv2.cvtColor(o,cv2.COLOR_RGB2HSV).astype(float)
L0=lab[...,0]*100/255
wood=(hsv[...,1]>70)&(L0>22)&(a2>0)
Ln=np.clip(82+0.32*(L0-55),0,100)
lab2=lab.copy();lab2[...,0]=np.where(wood,Ln*255/100,lab[...,0])
lab2[...,1]=np.where(wood,128+(lab[...,1]-128)*0.55,lab[...,1]);lab2[...,2]=np.where(wood,128+(lab[...,2]-128)*0.75,lab[...,2])
o=cv2.cvtColor(np.clip(lab2,0,255).astype(np.uint8),cv2.COLOR_LAB2RGB)
op=(a2>0)&~((c.min(axis=2)>228)&(sy>=560)&(sy<=660)&(sx>=640)&(sx<=840))
# masks
ndl=np.zeros((h,w),np.uint8);cv2.fillPoly(ndl,[np.array([(737,500),(709,560),(737,790),(767,560)])-[X0,Y0]],1)
ndl=cv2.dilate(ndl,np.ones((5,5),np.uint8)).astype(bool)&op
arcbox=(sx>=648)&(sx<=827)&(sy>=583)&(sy<=650)
arc=arcbox&op&~ndl&~(o.min(axis=2)>215)
beam=(sy>=516)&(sy<=606)&op&~ndl&~arcbox&~((sx>=712)&(sx<=763)&(sy<520))
pan1=(sy>606)&(sy<1008)&(sx<648)&op; pan2=(sy>606)&(sy<1008)&(sx>827)&op
post=op&~ndl&~arc&~beam&~pan1&~pan2
print(o.dtype);Lx=cv2.cvtColor(np.clip(o,0,255).astype(np.uint8),cv2.COLOR_RGB2LAB)[...,0].astype(float)*100/255
def big(m,k=7):return cv2.morphologyEx(m.astype(np.uint8),cv2.MORPH_OPEN,np.ones((k,k),np.uint8)).astype(bool)
basem=(sy>1030)&op;bd=basem&big(Lx<45,15)&(sx>800)
print('base',basem.sum(),np.percentile(Lx[basem],[5,50,95]),Lx.shape,basem.shape)
good=basem&~bd&(Lx>55)
if good.sum(): o[bd]=np.median(o[good],0).astype(np.uint8)
edge=basem&~cv2.erode(op.astype(np.uint8),np.ones((7,7),np.uint8)).astype(bool);o[edge&bd]=INK
# beam pixels hidden behind needle: copy row from x=700
hid=ndl&(sy>=528)&(sy<=589)
ys,xs=np.where(hid);o[ys,xs]=o[ys,np.full_like(xs,700-X0)];a2[ys,xs]=a2[ys,np.full_like(xs,700-X0)]
beam=beam|(hid&(a2>0))
def layer(m,inpaint=None):
    oo=o.copy();aa=np.where(m,a2,0).astype(np.uint8)
    if inpaint is not None:
        oo=cv2.inpaint(oo,inpaint.astype(np.uint8),5,cv2.INPAINT_TELEA);aa=np.maximum(aa,np.where(inpaint,255,0).astype(np.uint8))
    return Image.fromarray(np.dstack([oo,aa]),'RGBA')
# fill post behind needle: post column pixels under needle
postcol=(sx>=713)&(sx<=762)&(sy>=478)&(sy<=800)
arcfill=ndl&arcbox&(sy>=588)&(sy<=645)
Lpost=layer(post)
_o=np.asarray(Lpost).copy();ys,xs=np.where(postcol)
_o[ys,xs]=_o[np.full_like(ys,805-Y0),xs]
_o[...,3][ys,xs]=_o[805-Y0,xs,3];Lpost=Image.fromarray(_o,'RGBA');Larc=layer(arc,arcfill)
Lrot=layer(beam);Lp1=layer(pan1);Lp2=layer(pan2)
S_=0.78
def sc(im):return im.resize((int(im.size[0]*S_),int(im.size[1]*S_)),Image.LANCZOS)
Lpost,Larc,Lrot,Lp1,Lp2=map(sc,(Lpost,Larc,Lrot,Lp1,Lp2))
bw,bh=Lpost.size;ox=(W-bw)/2;oy=FL-bh+2   # balance base on floor
P=lambda x,y:(ox+(x-X0)*S_,oy+(y-Y0)*S_)
piv=P(737,560);HK1=(435,575);HK2=(1055,575);hk1=P(*HK1);hk2=P(*HK2)
sh1=(HK1[0]-444)*S_;sh2=(HK2[0]-1026)*S_
crate=obj('sheet1',[0],bg,w=112,outline=1)
def wt(i,hgt):return obj('sheet1',[i],bg,h=hgt,outline=1)
W1,W2,W5=wt(8,54),wt(9,68),wt(5,86)
pan_floor=P(444,934)[1]   # inner bottom of pan (pan surface)
def render(theta,right_items,fname):
    S=Image.new('RGBA',(W,H),bg);d=ImageDraw.Draw(S)
    for x in range(0,W,100): d.rectangle((x,0,x+4,FL),fill='#EABA5E')
    d.rectangle((0,FL,W,H),fill='#E0A94F');d.rectangle((0,FL,W,FL+5),fill='#5B3A29')
    shadow(S,W/2,FL,bw*0.45)
    S.alpha_composite(Lpost,(int(ox),int(oy)))
    dd=ImageDraw.Draw(S);R1,R2=150,184;cxp,cyp=piv
    def pt(r,ang):return (cxp+r*math.cos(math.radians(ang)),cyp+r*math.sin(math.radians(ang)))
    A0,A1=90-24,90+24
    poly=[pt(R2,a_) for a_ in np.linspace(A0,A1,30)]+[pt(R1,a_) for a_ in np.linspace(A1,A0,30)]
    dd.polygon(poly,fill=(0xF6,0xF3,0xEC),outline=(0x3B,0x24,0x17),width=4)
    for k_ in range(-3,4):
        ang=90+k_*6.5;r0=R1+ (0 if k_==0 else 14)
        dd.line(pt(r0,ang)+pt(R2-3,ang),fill=(0x3B,0x24,0x17) if k_ else (0x1B,0x7F,0x4B),width=3 if k_ else 7)
    rings=[];t=math.radians(theta)
    def rot(p):dx,dy=p[0]-piv[0],p[1]-piv[1];return (piv[0]+dx*math.cos(t)-dy*math.sin(t),piv[1]+dx*math.sin(t)+dy*math.cos(t))
    # rotate beam layer about pivot
    R=Image.new('RGBA',(W,H),(0,0,0,0));R.alpha_composite(Lrot,(int(ox),int(oy)))
    R=R.rotate(-theta,center=piv,resample=Image.BICUBIC)
    n1,n2=rot(hk1),rot(hk2);d1=(n1[0]-hk1[0],n1[1]-hk1[1]);d2=(n2[0]-hk2[0],n2[1]-hk2[1])
    S.alpha_composite(Lp1,(int(ox+d1[0]+sh1),int(oy+d1[1])));S.alpha_composite(Lp2,(int(ox+d2[0]+sh2),int(oy+d2[1])))
    dd=ImageDraw.Draw(S)
    for (hx_,hy_),(dx,dy),sh,tops in ((hk1,d1,sh1,((432,621),(456,621))),(hk2,d2,sh2,((1013,621),(1039,621)))):
        rc=(hx_+dx,hy_+dy);r=8
        for tx,ty in tops:
            tp=P(tx,ty);tp=(tp[0]+dx+sh,tp[1]+dy)
            dd.line((rc[0],rc[1]+r-2,tp[0],tp[1]+2),fill=(0x3B,0x24,0x17),width=8);dd.line((rc[0],rc[1]+r-2,tp[0],tp[1]+2),fill=(0x6F,0x85,0x89),width=4)
        rings.append((rc,r))
    for (dx,dy),sh,ends in ((d1,sh1,((315,911),(572,909))),(d2,sh2,((899,911),(1156,909)))):
        for ex,ey in ends:
            e=P(ex,ey);e=(e[0]+dx+sh,e[1]+dy);b_=P(ex,927);b_=(b_[0]+dx+sh,b_[1]+dy)
            dd.line((e[0],e[1]-2,b_[0],b_[1]-6),fill=(0x3B,0x24,0x17),width=8);dd.line((e[0],e[1]-2,b_[0],b_[1]-6),fill=(0x6F,0x85,0x89),width=4)
            dd.ellipse((b_[0]-7,b_[1]-10,b_[0]+7,b_[1]+2),fill=(0x9A,0xAD,0xB1),outline=(0x3B,0x24,0x17),width=3)
    S.alpha_composite(R)
    NL=178;nd=[(0,-28),(-16,0),(0,NL),(16,0)]
    ndp=[(piv[0]+x_*math.cos(t)-y_*math.sin(t),piv[1]+x_*math.sin(t)+y_*math.cos(t)) for x_,y_ in nd]
    dd=ImageDraw.Draw(S);dd.polygon(ndp,fill=(0x2F,0x3D,0x44),outline=(0x3B,0x24,0x17),width=3)
    dd.ellipse((piv[0]-8,piv[1]-8,piv[0]+8,piv[1]+8),fill=(0xC9,0xD3,0xD6),outline=(0x3B,0x24,0x17),width=3)
    dd=ImageDraw.Draw(S)
    for (rc,r) in rings: dd.ellipse((rc[0]-r,rc[1]-r,rc[0]+r,rc[1]+r),outline=(0x3B,0x24,0x17),width=6);dd.ellipse((rc[0]-r+2,rc[1]-r+2,rc[0]+r-2,rc[1]+r-2),outline=(0x9A,0xAD,0xB1),width=2)
    # crate on left pan
    y1=pan_floor+d1[1];x1=P(444,0)[0]+d1[0]+sh1
    S.alpha_composite(crate,(int(x1-crate.size[0]/2),int(y1-crate.size[1]+3)))
    y2=pan_floor+d2[1];x2=P(1026,0)[0]+d2[0]+sh2
    tw=sum(i.size[0] for i in right_items)+8*(len(right_items)-1);cx=x2-tw/2
    for im in right_items:
        S.alpha_composite(im,(int(cx),int(y2-im.size[1]+3)));cx+=im.size[0]+8
    S.convert('RGB').save(f'm6/{fname}.png')
render(-8,[],'bal_before')     # left (crate) side down
render(0,[W1,W2],'bal_after')
for i,im in (('w1',W1),('w2',W2),('w5',W5)):im.save(f'm6/{i}.png')
