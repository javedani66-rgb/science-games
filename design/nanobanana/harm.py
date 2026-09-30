from PIL import Image
import numpy as np, cv2, json
from scipy import ndimage as nd
from sklearn.cluster import KMeans
B=json.load(open('boxes.json'))
INK=np.array([0x3B,0x24,0x17])
def cut(sheet,idxs,pad=6,holes=True):
    im=np.asarray(Image.open(sheet+'.jpg').convert('RGB')).astype(np.uint8)
    bx=[B[sheet][i] for i in idxs];x0=min(b[0] for b in bx)-pad;y0=min(b[1] for b in bx)-pad;x1=max(b[2] for b in bx)+pad;y1=max(b[3] for b in bx)+pad
    x0=max(0,x0);y0=max(0,y0);c=im[y0:y1,x0:x1].copy()
    white=c.min(axis=2)>(226 if holes else 246);L,n=nd.label(white);border=set(np.unique(np.concatenate([L[0],L[-1],L[:,0],L[:,-1]])))-{0}
    bg=np.isin(L,list(border))
    # remove enclosed large white holes (gaps) — keep small ones
    for i in range(1,n+1):
        if i in border: continue
        m=L==i
        if holes and m.sum()>1500: bg|=m
    alpha=np.where(bg,0,255).astype(np.uint8)
    if not holes:
        L2,n2=nd.label(alpha>0)
        if n2>1:
            sz=nd.sum(alpha>0,L2,range(1,n2+1));alpha=np.where(L2==np.argmax(sz)+1,255,0).astype(np.uint8)
    alpha=cv2.erode(alpha,np.ones((2,2),np.uint8))
    return c,alpha
def harmonize(c,alpha,k=7,sat=0.9):
    sm=cv2.bilateralFilter(c,9,40,9)
    sm=cv2.bilateralFilter(sm,9,40,9)
    lab=cv2.cvtColor(sm,cv2.COLOR_RGB2LAB).astype(float)
    m=alpha>0
    X=lab[m]
    km=KMeans(k,n_init=3,random_state=0).fit(X[::7])
    lbl=km.predict(X);cent=km.cluster_centers_
    q=lab.copy();q[m]=cent[lbl]
    out=cv2.cvtColor(np.clip(q,0,255).astype(np.uint8),cv2.COLOR_LAB2RGB)
    # desaturate slightly
    hsv=cv2.cvtColor(out,cv2.COLOR_RGB2HSV).astype(float);hsv[...,1]*=sat;out=cv2.cvtColor(np.clip(hsv,0,255).astype(np.uint8),cv2.COLOR_HSV2RGB)
    # unify outline: dark pixels in original -> INK
    Lorig=cv2.cvtColor(c,cv2.COLOR_RGB2LAB)[...,0]
    ink=(Lorig<70)&m
    out[ink]=INK
    out=cv2.medianBlur(out,3)
    return out
def rgba(c,a): return Image.fromarray(np.dstack([c,a]),'RGBA')

def harmonize2(c,alpha,k=6,sat=0.92,sp=10,sr=28):
    m=alpha>0
    base=c.copy();base[~m]=255
    ms=cv2.pyrMeanShiftFiltering(base,sp,sr)
    ms=cv2.pyrMeanShiftFiltering(ms,sp//2,sr)
    lab=cv2.cvtColor(ms,cv2.COLOR_RGB2LAB).astype(float)
    X=lab[m];km=KMeans(k,n_init=3,random_state=0).fit(X[::5])
    lbl=np.full(m.shape,-1);lbl[m]=km.predict(X)
    # mode filter on label map to kill specks
    for _ in range(2):
        best=np.zeros(m.shape,int);bc=np.zeros(m.shape)
        for j in range(k):
            cnt=cv2.boxFilter((lbl==j).astype(np.float32),-1,(5,5),normalize=False)
            upd=cnt>bc;best[upd]=j;bc[upd]=cnt[upd]
        lbl[m]=best[m]
    q=lab.copy();q[m]=km.cluster_centers_[lbl[m]]
    out=cv2.cvtColor(np.clip(q,0,255).astype(np.uint8),cv2.COLOR_LAB2RGB)
    hsv=cv2.cvtColor(out,cv2.COLOR_RGB2HSV).astype(float);hsv[...,1]*=sat;out=cv2.cvtColor(np.clip(hsv,0,255).astype(np.uint8),cv2.COLOR_HSV2RGB)
    Lorig=cv2.cvtColor(c,cv2.COLOR_RGB2LAB)[...,0]
    ink=(cv2.medianBlur((Lorig<75).astype(np.uint8)*255,3)>0)&m
    out[ink]=INK
    # defringe: outer ring of alpha -> ink
    er=cv2.erode(alpha,np.ones((3,3),np.uint8),iterations=2)
    ring=(alpha>0)&(er==0);out[ring]=INK
    return out

def gentle(c,alpha,land_rgb,grade=0.07):
    m=alpha>0;out=c.astype(float)
    # unify outline colour
    Lorig=cv2.cvtColor(c,cv2.COLOR_RGB2LAB)[...,0].astype(float)
    w=np.clip((55-Lorig)/25,0,1)[...,None]*m[...,None]
    out=out*(1-w)+INK*w
    # tiny grade toward land ambient (soft-light-ish)
    out=out*(1-grade)+np.array(land_rgb)*grade
    out=np.clip(out,0,255).astype(np.uint8)
    # defringe ring
    er=cv2.erode(alpha,np.ones((3,3),np.uint8),iterations=1)
    ring=(alpha>0)&(er==0);out[ring]=INK
    a2=cv2.GaussianBlur(alpha,(3,3),0)
    return out,a2
