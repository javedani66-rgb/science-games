import sys, json, colorsys
sys.path.insert(0,'.')
from mz import *
V3K='file:///home/claude/science-games/design/mockups/20261008/flow-demo/v3/kit4/proof.html'
TAG=sys.argv[1] if len(sys.argv)>1 else 'm'
HIDE=".land__path,.node,.sign,.guide,.portal,.land__head,#gap4,.node__ring{visibility:hidden!important} #phone{height:1060px!important} .topbar{visibility:hidden}"
OUTLINE=".pt-sh,.pt-shine,.pt-dots{visibility:hidden!important}"
SHOW={'done':".land__path .pt-done .pt{visibility:visible!important}"+" .land__path .pt-done .pt-sh,.land__path .pt-done .pt-shine,.land__path .pt-done .pt-dots{visibility:hidden!important}",
      'todo':".land__path .pt-todo .pt{visibility:visible!important} .land__path .pt-todo .pt-sh{visibility:hidden!important}",
      'nodes':".node .node__disc{visibility:visible!important}"}
P=Page(V3K+'?v=stadium',None,390,1060)
P.css("#phone{height:1060px!important}"); P.pg.wait_for_timeout(300)
def hsv_conf(img,roi):
    px=img[roi]/255.0; mx=px.max(1); mn=px.min(1); d=mx-mn; s=np.where(mx>0,d/np.maximum(mx,1e-6),0)
    r,g,b=px[:,0],px[:,1],px[:,2]; h=np.zeros(len(px))
    m=d>1e-6; 
    rc=np.where(m&(mx==r),((g-b)/np.maximum(d,1e-6))%6,0); gc=np.where(m&(mx==g)&(mx!=r),(b-r)/np.maximum(d,1e-6)+2,0); bc=np.where(m&(mx==b)&(mx!=r)&(mx!=g),(r-g)/np.maximum(d,1e-6)+4,0)
    h=(rc+gc+bc)*60
    res={}
    for nm,hh in (('easy',140),('mid',33),('hard',3)):
        dh=np.minimum(np.abs(h-hh),360-np.abs(h-hh))
        res[nm]=round(100*float(((dh<=14)&(s>.5)&(mx>.45)).mean()),2)
    return res
NOM_H=float(lum(hex2rgb('#fff7e0')))*0.93+0.0   # هالهٔ #fff7e0 با شفافیت ۰٫۹۲ روی زمینی تیره‌تر: برآورد محافظه‌کارانه
NOM_E=float(lum(hex2rgb('#2b190a')))
res={}
for key in ('stadium','space','farm','city'):
    P.pg.evaluate("""k=>{const l=document.querySelector('.land[data-land='+k+']').parentElement;const b=document.querySelector('#mb');b.scrollTop=l.offsetTop-14;}""",key)
    P.pg.wait_for_timeout(250)
    info=P.pg.evaluate("""k=>{const l=document.querySelector('.land[data-land='+k+']');const r=l.getBoundingClientRect();
      const nd=[...l.querySelectorAll('.node')].map(n=>{const d=n.querySelector('.node__disc').getBoundingClientRect();return{id:n.dataset.id,st:n.dataset.state,cx:d.left+d.width/2,cy:d.top+d.height*.467,w:d.width}});
      return {l:[r.left,r.top,r.right,r.bottom],nodes:nd}}""",key)
    L=info['l'];H=1060;Wd=390
    roi=np.zeros((H,Wd),bool); roi[int(max(L[1],0))+6:int(min(L[3],H))-6, int(L[0])+8:int(L[2])-8]=True
    P.css(HIDE); bare=P.shot()
    out={'conf':hsv_conf(bare,roi)}
    for g in ('done','todo'):
        P.css(HIDE+SHOW[g]); gi=P.shot()
        mask=(np.abs(gi-bare).sum(2)>30)&roi
        if mask.sum()<80: continue
        dt_in=ndi.distance_transform_edt(mask); dt_out=ndi.distance_transform_edt(~mask)
        ring=(dt_out>2)&(dt_out<=12)&roi
        halo=mask&(dt_in>=0.9)&(dt_in<=1.9); edge=mask&(dt_in>=3.4)&(dt_in<=4.8); fill=mask&(dt_in>=6.8)
        if g=='todo': halo=mask&(dt_in>=.6)&(dt_in<=2.2); edge=mask&(dt_in>=3.4)&(dt_in<=4.8); fill=mask&(dt_in>=5.4)
        if min(ring.sum(),halo.sum(),edge.sum(),fill.sum())<10: continue
        Lbg=lum(bare[ring]); Lh,Le,Lf=NOM_H,NOM_E,float(np.median(lum(gi[fill])))
        ch,ce,cf=cr(Lbg,Lh),cr(Lbg,Le),cr(Lbg,Lf); best=np.maximum(ch,ce)
        out['path_'+g]=dict(n=int(ring.sum()),Lhalo=round(Lh,3),Ledge=round(Le,3),Lfill=round(Lf,3),Lbg_med=round(float(np.median(Lbg)),3),bg_std=round(float(np.std(Lbg)),3),
            pct_halo3=round(100*float((ch>=3).mean()),1),pct_edge3=round(100*float((ce>=3).mean()),1),pct_outer3=round(100*float((best>=3).mean()),1),pct_fill3=round(100*float((cf>=3).mean()),1),outer_p10=round(float(np.percentile(best,10)),2),outer_min=round(float(best.min()),2))
    P.css("#phone{height:1060px!important} .topbar{visibility:hidden} .land__head,.sign,.portal,#gap4{visibility:hidden!important} .node__labels,.guide,.node__ring{visibility:hidden!important}"); full=P.shot()
    ns=[]
    for n in info['nodes']:
        cx,cy,r=n['cx'],n['cy'],n['w']*57.5/120
        if cy<L[1]+20 or cy>min(L[3],H)-40: continue
        ns.append(node_ring(bare,full,cx,cy,r,roi) if False else None)
        Hh,Ww=bare.shape[:2]; yy,xx=np.mgrid[0:Hh,0:Ww]; d=np.hypot(xx-cx,yy-cy)
        ring=(d>r+2)&(d<=r+12)&roi; halo=(d>r-2)&(d<=r-.5); edge=(d>r-4.2)&(d<=r-3.0); pad=(d>r-7.4)&(d<=r-5.4)
        if ring.sum()<80: ns.pop(); continue
        Lbg=lum(bare[ring]); Lh,Le=NOM_H,NOM_E; Lp=float(np.median(lum(full[pad])))
        ch,ce,cp=cr(Lbg,Lh),cr(Lbg,Le),cr(Lbg,Lp); best=np.maximum(ch,ce)
        ns[-1]=dict(id=n['id'],state=n['st'],Lhalo=round(Lh,3),Ledge=round(Le,3),Lpad=round(Lp,3),Lbg_med=round(float(np.median(Lbg)),3),pct_halo3=round(100*float((ch>=3).mean()),1),pct_edge3=round(100*float((ce>=3).mean()),1),pct_outer3=round(100*float((best>=3).mean()),1),pct_pad3=round(100*float((cp>=3).mean()),1),outer_p10=round(float(np.percentile(best,10)),2),outer_min=round(float(best.min()),2))
    out['nodes']=ns; res[key]=out
    P.css("#phone{height:1060px!important}")
# متن‌ها: رنگ متن در برابر پس‌زمینهٔ واقعی چسبک/لوحه
P.css("#phone{height:1060px!important}")
txt=[]
for key in ('stadium','space','farm','city'):
    P.pg.evaluate("""k=>{const l=document.querySelector('.land[data-land='+k+']').parentElement;document.querySelector('#mb').scrollTop=l.offsetTop-14}""",key); P.pg.wait_for_timeout(200)
    els=P.pg.evaluate("""k=>{const l=document.querySelector('.land[data-land='+k+']');return [...l.querySelectorAll('.chip,.plate span')].map(e=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);return{t:e.textContent.trim(),c:cs.color,r:[r.left,r.top,r.right,r.bottom],fs:parseFloat(cs.fontSize),k:e.className}})}""",key)
    full=P.shot()
    for e in els:
        x0,y0,x1,y1=[int(round(v)) for v in e['r']]
        if y0<70 or y1>1060 or x1-x0<10: continue
        box=full[y0+4:y1-4,x0+8:x1-8]
        if box.size==0: continue
        import re
        c=[float(v) for v in re.findall(r'[\d.]+',e['c'])[:3]]
        dist=np.abs(box-np.array(c)).sum(2); bgpx=box[dist>90]
        if len(bgpx)<20: continue
        bg=np.median(bgpx,axis=0); Lt=float(lum(np.array(c))); Lb=float(lum(bg))
        txt.append(dict(land=key,t=e['t'][:22],fs=e['fs'],cr=round(float(cr(Lt,Lb)),2)))
res['text']=txt
P.close()
json.dump(res,open(f'new_measure_{TAG}.json','w'),ensure_ascii=False,indent=1)
for k in ('stadium','space','farm','city'):
    v=res[k]; print('==',k,'confusion%',v['conf'])
    for g in ('path_done','path_todo'):
        if g in v: print(' ',g,{a:v[g][a] for a in ('Lhalo','Ledge','Lfill','Lbg_med','bg_std','pct_halo3','pct_edge3','pct_outer3','pct_fill3','outer_p10','outer_min')})
    for n in v['nodes']: print('  node',n['id'],n['state'],{a:n[a] for a in ('Lbg_med','pct_halo3','pct_edge3','pct_outer3','pct_pad3','outer_min')})
bad=[t for t in txt if t['cr']<4.5]; print('text n',len(txt),'min cr',min(t['cr'] for t in txt),'below4.5:',bad)
