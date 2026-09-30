from PIL import Image
import numpy as np
from scipy import ndimage as nd
def lab(x):
    x=x/255;x=np.where(x>0.04045,((x+0.055)/1.055)**2.4,x/12.92)
    M=np.array([[0.4124,0.3576,0.1805],[0.2126,0.7152,0.0722],[0.0193,0.1192,0.9505]])
    X=x@M.T/np.array([0.9505,1,1.089]);f=np.where(X>0.008856,np.cbrt(X),7.787*X+16/116)
    return np.stack([116*f[...,1]-16,500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2])],-1)
def recolor(path,keys,targets,line_L=24,tol=10):
    im=Image.open(path).convert('RGBA');a=np.asarray(im).astype(float);rgb=a[...,:3];al=a[...,3]
    L=lab(rgb);line=(L[...,0]<line_L)|(al<128)
    R,n=nd.label(~line)
    med=nd.median(L[...,0],R,range(1,n+1)),nd.median(L[...,1],R,range(1,n+1)),nd.median(L[...,2],R,range(1,n+1))
    med=np.stack(med,1)
    out=rgb.copy()
    for name,key in keys.items():
        if name not in targets: continue
        kl=lab(np.array(key,float)[None,None,:])[0,0]
        ids=[i+1 for i in range(n) if np.hypot(*(med[i,1:]-kl[1:]))<tol and abs(med[i,0]-kl[0])<25]
        m=np.isin(R,ids)
        # grow 2px into antialias pixels that are not line and closer to key hue
        g=nd.binary_dilation(m,iterations=2)&~m&(al>0)&(np.hypot(L[...,1]-kl[1],L[...,2]-kl[2])<tol*2)&(L[...,0]>=line_L-6)
        m=m|g
        ratio=np.array(targets[name],float)/np.array(key,float)
        out[m]=np.clip(rgb[m]*ratio,0,255)
    return Image.fromarray(np.dstack([out,al]).astype(np.uint8),'RGBA')
