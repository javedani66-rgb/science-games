import sys,math,json;sys.path.insert(0,'.')
exec(open('m6/scenes.py').read().split("W,H,FL=800,540,450")[0])
W,H,FL=800,820,720;bg='#1E576A'
def base():
    S=Image.new('RGBA',(W,H),bg);d=ImageDraw.Draw(S)
    for x in range(0,W,40): d.line((x,0,x,FL),fill='#22607A',width=2)
    for y in range(0,FL,40): d.line((0,y,W,y),fill='#22607A',width=2)
    d.rectangle((0,FL,W,H),fill='#19495A');d.rectangle((0,FL,W,FL+5),fill='#0F3442')
    return S
wedge=obj('sheet_fix',[11],bg,h=56)
wa=np.asarray(wedge)[...,3];rows=np.where(wa.max(1)>128)[0];r0=rows[0]+2;cols=np.where(wa[r0]>128)[0]
apex_dx=(cols.mean()-wedge.size[0]/2)  # apex x offset from image centre
pl0=obj('sheet2',[0],bg,w=500,outline=2)
st=obj('sheet2',[3],bg,h=100,outline=2,holes=False)
PM=76;T=pl0.size[1]           # plank thickness in px (image height)
EXT=0.2                         # plank extends 0.2 m beyond stone point and force point
X0=110                          # stone x (before)
def scene(f,state,fname):
    S=base()
    fx=X0+f*PM if state=='before' else None
    # pivot = wedge apex
    if state=='before':
        px_=fx
    else:
        px_=X0+f*PM
    apexY=float(FL-wedge.size[1]+r0)
    wx=px_-apex_dx
    L_left=(f+EXT)*PM;L_right=(5-f+EXT)*PM
    if state=='before':   # left tip on floor (under stone)
        a=math.asin((FL-6-apexY)/L_left)
    else:                 # right end pressed onto floor
        a=-math.asin((FL-6-apexY)/L_right)
    ux,uy=math.cos(a),-math.sin(a)       # unit vector to the right along plank (screen coords)
    nx,ny=math.sin(a),math.cos(a)        # hmm normal pointing down? compute: perpendicular (-uy,ux)
    nx,ny=-uy,ux
    if ny<0: nx,ny=-nx,-ny               # downward normal
    # plank centreline is T/2 above apex
    cxl,cyl=px_-nx*T/2,apexY-ny*T/2
    P=lambda s:(cxl+ux*s*PM,cyl+uy*s*PM)             # point on centreline at s metres from pivot
    Q=lambda s:(px_+ux*s*PM,apexY+uy*s*PM)           # point on bottom surface
    Lp=L_left+L_right
    pl=pl0.resize((int(Lp),T),Image.LANCZOS);pr=pl.rotate(math.degrees(a),expand=True,resample=Image.BICUBIC)
    mid=(L_right-L_left)/2/PM;mc=P(mid)
    place(S,wedge,wx,FL)
    paste_c(S,pr,mc[0],mc[1])
    sp=P(-f)
    if state=='before':
        sx=sp[0];S.alpha_composite(st,(int(sx-st.size[0]/2),int(FL-st.size[1]+4)))   # stone on the floor, plank tip under it
        stone_pt=(sx,Q(-f)[1])
    else:
        top=(sp[0]-nx*T/2,sp[1]-ny*T/2)
        S.alpha_composite(st,(int(top[0]-st.size[0]/2),int(top[1]-st.size[1]+10)))
        stone_pt=Q(-f)
    fp=P(5-f)
    d=ImageDraw.Draw(S)
    if state=='after': arrow(d,fp[0],fp[1]-200,fp[1]-12,'#FF94C2')
    S.convert('RGB').save(f'm6/{fname}.png')
    return dict(pivot=(px_,apexY),stone=stone_pt,force=Q(5-f),f=f)
mb=scene(2,'before','lever3_before');ma=scene(1,'after','lever3_after')
json.dump({'before':mb,'after':ma},open('m6/lever3_meta.json','w'));print(mb,ma)
