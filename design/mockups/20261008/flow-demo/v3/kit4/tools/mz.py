"""مقیاس‌گیری جداسازی لایه‌ها (WCAG 1.4.11 / 1.4.3). نه ادعای آزمون با کودک؛ فقط نسبت روشنایی پیکسل‌ها.
روش: سه رندر از یک صفحه (فقط زمینه / فقط گروه مسیر یا گره / کامل)، ماسک = تفاوت، حلقهٔ زمینه = پیکسل‌های رندر «فقط زمینه» در فاصلهٔ ۲ تا ۱۲px بیرون ماسک."""
import numpy as np, io
from PIL import Image
from scipy import ndimage as ndi
from playwright.sync_api import sync_playwright
EXE='/opt/pw-browsers/chromium'

def lin(c):
    c=np.asarray(c,dtype=float)/255.0
    return np.where(c<=0.03928,c/12.92,((c+0.055)/1.055)**2.4)
def lum(rgb):
    l=lin(rgb); return 0.2126*l[...,0]+0.7152*l[...,1]+0.0722*l[...,2]
def cr(l1,l2):
    a=np.maximum(l1,l2);b=np.minimum(l1,l2);return (a+0.05)/(b+0.05)
def hex2rgb(h):
    h=h.lstrip('#');return np.array([int(h[i:i+2],16) for i in (0,2,4)],float)

class Page:
    def __init__(s,url,setup_js,w=390,h=1000):
        s.pw=sync_playwright().start()
        s.b=s.pw.chromium.launch(executable_path=EXE,args=['--no-sandbox'])
        s.pg=s.b.new_page(viewport={'width':w,'height':h})
        s.pg.goto(url); s.pg.wait_for_timeout(500)
        if setup_js: s.pg.evaluate(setup_js)
        s.pg.wait_for_timeout(500)
    def css(s,txt):
        s.pg.evaluate("t=>{let e=document.getElementById('mz');if(!e){e=document.createElement('style');e.id='mz';document.head.appendChild(e)}e.textContent=t}",txt)
        s.pg.wait_for_timeout(120)
    def shot(s):
        return np.array(Image.open(io.BytesIO(s.pg.screenshot())).convert('RGB')).astype(float)
    def close(s): s.b.close(); s.pw.stop()

def ring_stats(bare,full,mask,roi,edge_px=1.6,fill_px=3.0,r0=2,r1=12):
    """mask: bool silhouette. returns dict"""
    dt_in=ndi.distance_transform_edt(mask)
    dt_out=ndi.distance_transform_edt(~mask)
    ring=(dt_out>r0)&(dt_out<=r1)&roi
    edge=mask&(dt_in<=edge_px)&roi
    fill=mask&(dt_in>=fill_px)&roi
    if ring.sum()<50 or fill.sum()<10 or edge.sum()<10: return None
    Lbg=lum(bare[ring]); Lf=float(np.median(lum(full[fill]))); Le=float(np.median(lum(full[edge])))
    cf=cr(Lbg,Lf); ce=cr(Lbg,Le)
    best=np.maximum(cf,ce)
    # busy-ness: std of bg luminance in the ring
    return dict(n=int(ring.sum()),Lfill=round(Lf,3),Ledge=round(Le,3),Lbg_med=round(float(np.median(Lbg)),3),
        bg_std=round(float(np.std(Lbg)),3),cr_fill_med=round(float(np.median(cf)),2),cr_edge_med=round(float(np.median(ce)),2),
        pct_fill3=round(100*float((cf>=3).mean()),1),pct_edge3=round(100*float((ce>=3).mean()),1),pct_any3=round(100*float((best>=3).mean()),1),
        best_p10=round(float(np.percentile(best,10)),2))

def disc_mask(shape,cx,cy,r):
    yy,xx=np.mgrid[0:shape[0],0:shape[1]]
    return (xx-cx)**2+(yy-cy)**2<=r*r

def node_stats(bare,full,cx,cy,r,roi,r0=3,r1=12,edge_w=3,fill_in=(8,14)):
    H,W=bare.shape[:2]
    yy,xx=np.mgrid[0:H,0:W]; d=np.hypot(xx-cx,yy-cy)
    ring=(d>r+r0)&(d<=r+r1)&roi
    edge=(d>r-edge_w)&(d<=r-0.5)
    fill=(d>r-fill_in[1])&(d<=r-fill_in[0])
    if ring.sum()<50: return None
    Lbg=lum(bare[ring]); Lf=float(np.median(lum(full[fill]))); Le=float(np.median(lum(full[edge])))
    cf=cr(Lbg,Lf); ce=cr(Lbg,Le); best=np.maximum(cf,ce)
    return dict(n=int(ring.sum()),Lfill=round(Lf,3),Ledge=round(Le,3),Lbg_med=round(float(np.median(Lbg)),3),bg_std=round(float(np.std(Lbg)),3),
        pct_fill3=round(100*float((cf>=3).mean()),1),pct_edge3=round(100*float((ce>=3).mean()),1),pct_any3=round(100*float((best>=3).mean()),1),best_p10=round(float(np.percentile(best,10)),2))
