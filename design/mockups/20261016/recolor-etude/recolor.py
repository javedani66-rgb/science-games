import sys, numpy as np, colorsys
from PIL import Image
from scipy import ndimage as ndi
C='/home/claude/science-games/design/mockups/20261016/character-menu/_cache'
def rgb2hsv(a):
    a=a/255.; mx=a.max(2); mn=a.min(2); d=mx-mn+1e-9
    r,g,b=a[...,0],a[...,1],a[...,2]
    h=np.where(mx==r,((g-b)/d)%6,np.where(mx==g,(b-r)/d+2,(r-g)/d+4))*60
    return h%360, np.where(mx>0,(mx-mn)/(mx+1e-9),0), mx
def hsv2rgb(h,s,v):
    h=(h%360)/60; c=v*s; x=c*(1-abs(h%2-1)); m=v-c
    z=np.zeros_like(h); 
    idx=h.astype(int)%6
    r=np.choose(idx,[c,x,z,z,x,c]); g=np.choose(idx,[x,c,c,x,z,z]); b=np.choose(idx,[z,z,x,c,c,x])
    return np.stack([r+m,g+m,b+m],-1)*255
def garment_mask(im):
    a=np.asarray(im).astype(float); h,s,v=rgb2hsv(a[...,:3]); H=a.shape[0]
    alpha=a[...,3]>200
    band=np.zeros_like(alpha); band[int(H*.37):int(H*.72)]=True   # از زیر چانه تا زانو
    sat=(s>.5)&(v>.4)&alpha&band
    hist,_=np.histogram(h[sat],bins=36,range=(0,360))
    hc=(np.argmax(hist)*10+5)
    d=np.minimum(abs(h-hc),360-abs(h-hc))
    m=sat&(d<22)
    core=ndi.binary_erosion(m,iterations=4)
    lab,n=ndi.label(core)
    if n:
        sz=ndi.sum(core,lab,range(1,n+1)); core=np.isin(lab,[i+1 for i,z in enumerate(sz) if z>=0.25*max(sz)])
    m=ndi.binary_dilation(core,iterations=4)&m
    return m,hc
def recolor(im,shift):
    m,hc=garment_mask(im); a=np.asarray(im).astype(float)
    h,s,v=rgb2hsv(a[...,:3]); h2=np.where(m,h+shift,h)
    out=hsv2rgb(h2,s,v); res=a.copy(); res[...,:3]=np.where(m[...,None],out,a[...,:3])
    return Image.fromarray(res.clip(0,255).astype('uint8'),'RGBA'),hc
if __name__=='__main__':
    outf=sys.argv[1]; names=['nima','roya','sam','tara','mani','goli']; shifts=[0,120,200,300]
    W=150;Hh=300; sheet=Image.new('RGB',(W*len(shifts)*2//2*1,Hh*len(names)),(255,243,196))
    sheet=Image.new('RGB',(W*len(shifts),Hh*len(names)),(255,243,196))
    for r,n in enumerate(names):
        im=Image.open(f'{C}/{outf}/{n}.webp').convert('RGBA')
        for c,sh in enumerate(shifts):
            o,hc=recolor(im,sh); o=o.resize((round(o.width*Hh/o.height),Hh),Image.LANCZOS)
            sheet.paste(o,(c*W+(W-o.width)//2,r*Hh),o)
    sheet.save(f'/tmp/claude-0/-home-claude-science-games/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/rc/sheet_{outf}.png')
