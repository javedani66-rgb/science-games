#!/usr/bin/env python3
"""measure.py: نسبت کنتراست روشنایی (WCAG 2.x) بین «شکل» (مسیر، گره، برچسب) و «زمینهٔ واقعی» در عکس‌ها.
روش: برای هر صفحه ۴ عکس از Chromium می‌گیرد (همه چیز / فقط زمینه / زمینه+مسیر / زمینه+گره‌ها)
و در همان نقطه‌ها روشنایی شکل را با روشنایی زمینهٔ زیر آن می‌سنجد (نسبت = (روشن‌تر+.05)/(تیره‌تر+.05)).
استفاده:  python3 measure.py <url> <برچسب> id1,id2,id3,id4 <خروجی.json> [--grayscale-dir DIR]
(playwright install ممنوع؛ از /opt/pw-browsers/chromium-1194 استفاده می‌شود)"""
import sys,os,json,math,io
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
EXE='/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
def lin(a):
    a=a/255.0; return np.where(a<=.03928,a/12.92,((a+.055)/1.055)**2.4)
def lum(img): # img HxWx3 uint8 -> HxW Y
    l=lin(img[...,:3].astype(float)); return .2126*l[...,0]+.7152*l[...,1]+.0722*l[...,2]
def patch(Y,x,y,r=1):
    h,w=Y.shape; x=int(round(x)); y=int(round(y))
    if x-r<0 or y-r<0 or x+r>=w or y+r>=h: return None
    return float(Y[y-r:y+r+1,x-r:x+r+1].mean())
def ratio(a,b):
    hi,lo=max(a,b),min(a,b); return (hi+.05)/(lo+.05)
HIDE_ALL='.land__path,.trail,.node,.guide,.mark,.mark__chip,.barrier,.foot,.land__head,.node__ring'
def style(css): return f"(()=>{{let s=document.getElementById('__m')||document.createElement('style');s.id='__m';s.textContent={json.dumps(css)};document.head.appendChild(s)}})()"
JS_PATHS="""([id,sel])=>{const scr=document.getElementById(id);const r=scr.getBoundingClientRect();const out=[];
 scr.querySelectorAll(sel).forEach(p=>{const L=p.getTotalLength(),m=p.getScreenCTM(),cs=getComputedStyle(p);
  const da=(cs.strokeDasharray||'none').split(/[ ,]+/).map(parseFloat).filter(v=>!isNaN(v));const per=da.length>=2?da[0]+da[1]:0;
  const sc=Math.hypot(m.a,m.b)||1;const pts=[];
  for(let s=0;s<L;s+=1.5){ if(per){const q=((s*1)%(per));if(q>da[0])continue}   // فقط «هستهٔ» خط‌چین، نه سرِ گردِ آن
   const a=p.getPointAtLength(s),b=p.getPointAtLength(Math.min(s+1.5,L));const pa=new DOMPoint(a.x,a.y).matrixTransform(m),pb=new DOMPoint(b.x,b.y).matrixTransform(m);pts.push([pa.x-r.left,pa.y-r.top,pb.x-pa.x,pb.y-pa.y])}
  out.push({cls:p.getAttribute('class'),ctx:p.closest('.trail')?'gap':'land',pts})});return out}"""
JS_NODES="""(id)=>{const scr=document.getElementById(id);const r=scr.getBoundingClientRect();
 return [...scr.querySelectorAll('.node__disc')].map(d=>{const b=d.getBoundingClientRect();return {cx:b.left+b.width/2-r.left,cy:b.top+b.height/2-r.top,w:b.width,st:d.closest('.node').dataset.state}})}"""
JS_CHIPS="""(id)=>{const scr=document.getElementById(id);const r=scr.getBoundingClientRect();
 return [...scr.querySelectorAll('.node__labels .chip, .mark__chip')].map(c=>{const b=c.getBoundingClientRect();return {l:b.left-r.left,t:b.top-r.top,w:b.width,h:b.height,cls:c.className,txt:c.textContent.trim()}})}"""
def run(url,tag,ids,out,gdir=None):
    res={}
    with sync_playwright() as pw:
        b=pw.chromium.launch(executable_path=EXE,args=['--no-sandbox'])
        pg=b.new_page(viewport={'width':390,'height':800}); pg.goto(url); pg.wait_for_timeout(900)
        for id in ids:
            loc=pg.locator('#'+id)
            def shot(css):
                pg.evaluate(style(css)); pg.wait_for_timeout(120)
                return np.array(Image.open(io.BytesIO(loc.screenshot())).convert('RGB'))
            A=shot('')
            Bimg=shot(f'{HIDE_ALL}{{visibility:hidden!important}}')
            Cimg=shot('.node,.guide,.mark,.mark__chip,.barrier,.foot,.land__head{visibility:hidden!important}')
            Dimg=shot('.land__path,.trail,.gate,.guide,.mark,.mark__chip,.barrier,.foot,.land__head,.node__ring,.node__labels{visibility:hidden!important}')
            pg.evaluate(style(''))
            if gdir:
                os.makedirs(gdir,exist_ok=True)
                Image.fromarray((lum(A)**(1/2.2)*255).clip(0,255).astype('uint8')).save(f'{gdir}/gray_{tag}_{id}.png')
            YA,YB,YC,YD=map(lum,(A,Bimg,Cimg,Dimg))
            r={}
            # ---- مسیر
            paths=pg.evaluate(JS_PATHS,[id,'path.path-done--top, path.path-todo'])
            nodes=pg.evaluate(JS_NODES,id)
            marks=pg.evaluate("(id)=>{const scr=document.getElementById(id),r=scr.getBoundingClientRect();return [...scr.querySelectorAll('.mark,.barrier')].map(m=>{const b=m.getBoundingClientRect();return [b.left-r.left,b.top-r.top,b.right-r.left,b.bottom-r.top]})}",id)
            lr=pg.evaluate("(id)=>{const scr=document.getElementById(id),r=scr.getBoundingClientRect();return [...scr.querySelectorAll('.land')].map(l=>{const b=l.getBoundingClientRect();return [b.left-r.left,b.top-r.top,b.right-r.left,b.bottom-r.top]})}",id)
            gr=pg.evaluate("(id)=>{const scr=document.getElementById(id),r=scr.getBoundingClientRect();return [...scr.querySelectorAll('.gate')].map(l=>{const b=l.getBoundingClientRect();return [b.left-r.left+30,b.top-r.top+10,b.right-r.left-30,b.bottom-r.top-10]})}",id)
            def in_land(x,y): return any(m[0]+6<=x<=m[2]-6 and m[1]+6<=y<=m[3]-6 for m in lr)
            def on_gate(x,y): return any(m[0]<=x<=m[2] and m[1]<=y<=m[3] for m in gr)
            def covered(x,y):
                if any(math.hypot(x-n['cx'],y-n['cy'])<52 for n in nodes): return True
                return any(m[0]<=x<=m[2] and m[1]<=y<=m[3] for m in marks)
            light=[];edge=[];gl=[];ge=[];low=[]
            for p in paths:
                for x,y,dx,dy in p['pts']:
                    if y<84 or y>792 or x<4 or x>386 or covered(x,y) or (p['ctx']=='land' and (not in_land(x,y) or on_gate(x,y))): continue
                    c=patch(YC,x,y);bg=patch(YB,x,y)
                    if c is None or bg is None: continue
                    L=math.hypot(dx,dy) or 1; nx,ny=-dy/L,dx/L
                    ev=[]
                    for sgn in (1,-1):
                        ex,ey=x+nx*7.5*sgn,y+ny*7.5*sgn
                        e=patch(YC,ex,ey,0);eb=patch(YB,ex,ey,0)
                        if e is not None and eb is not None: ev.append(ratio(e,eb))
                    ink=ratio(c,bg); ed=min(ev) if ev else 1.0
                    light.append(ink); edge.append(ed); gl.append(max(ink,ed))
                    if max(ink,ed)<3: low.append((round(max(ink,ed),2),round(x),round(y)))
            def st(a): 
                a=np.array(a) if len(a) else np.array([0.]); return dict(n=len(a),min=round(float(a.min()),2),p10=round(float(np.percentile(a,10)),2),med=round(float(np.median(a)),2),ok3=round(float((a>=3).mean()),3))
            r['path_best_vs_bg']=st(gl); r['path_lightfill_only_vs_bg']=st(light); r['path_contour_only_vs_bg']=st(edge)
            r['_low_ink_points']=sorted(low)[:10]
            # ---- گره‌ها (حلقه، نوار کرم، دورگیر بیرونی)
            ring=[];cream=[];outer=[];sil=[];lown=[]
            for ni,nd in enumerate(pg.evaluate(JS_NODES,id)):
                for k in range(24):
                    deg=k*15; a=2*math.pi*k/24
                    if (285<=deg<=345) or (nd['st']=='trial' and 105<=deg<=165): continue   # نشان‌های گوشه (پرچمک/ستاره/فلاسک) کنار گذاشته شد
                    vals={}
                    for name,frac in (('ring',.395),('cream',.331),('outer',.44)):
                        x=nd['cx']+math.cos(a)*frac*nd['w'];y=nd['cy']+math.sin(a)*frac*nd['w']
                        c=patch(YD,x,y,0);bg=patch(YB,x,y,0)
                        if c is not None and bg is not None: vals[name]=ratio(c,bg)
                    if 'ring' in vals: ring.append(vals['ring'])
                    if 'cream' in vals: cream.append(vals['cream'])
                    if 'outer' in vals: outer.append(vals['outer'])
                    if 'ring' in vals and 'outer' in vals:
                        sil.append(max(vals['ring'],vals['outer']))
                        if sil[-1]<3: lown.append((ni,deg,round(sil[-1],2),round(nd['cx']+math.cos(a)*.44*nd['w']),round(nd['cy']+math.sin(a)*.44*nd['w'])))
            r['_low_node_points']=lown; r['node_silhouette_vs_bg']=st(sil); r['node_ring_vs_bg']=st(ring); r['node_creamband_vs_bg']=st(cream); r['node_outer_vs_bg']=st(outer)
            # ---- چسبک‌ها
            cf=[];cb=[];cbest=[];ch_detail=[]
            for c in pg.evaluate(JS_CHIPS,id):
                cx=c['l']+c['w']/2
                f=patch(YA,cx,c['t']+4.5,0)
                bgs=[patch(YB,cx,c['t']-6,1),patch(YB,cx,c['t']+c['h']+8,1),patch(YB,c['l']-6,c['t']+c['h']/2,1),patch(YB,c['l']+c['w']+6,c['t']+c['h']/2,1)]
                bgs=[v for v in bgs if v is not None]
                if f is None or not bgs: continue
                bg=sum(bgs)/len(bgs); cf.append(ratio(f,bg))
                bd=patch(YA,cx,c['t']+1.0,0)
                if bd is not None: cb.append(ratio(bd,bg))
                hl=patch(YA,cx,c['t']-2.8,0)
                best=max(ratio(f,bg),ratio(bd,bg) if bd is not None else 1,ratio(hl,bg) if hl is not None else 1)
                cbest.append(best)
                ch_detail.append((c['txt'][:12],round(ratio(f,bg),2),round(ratio(bd,bg),2) if bd is not None else None,round(bg,3),round(ratio(hl,bg),2) if hl is not None else None,round(best,2)))
            r['_chip_detail']=ch_detail; r['chip_best_vs_bg']=st(cbest); r['chip_fill_vs_bg']=st(cf); r['chip_border_vs_bg']=st(cb)
            r['bg_Y_mean_inland']=round(float(YB[110:760,20:370].mean()),3)
            res[id]=r
        b.close()
    json.dump(res,open(out,'w'),ensure_ascii=False,indent=1)
    return res
if __name__=='__main__':
    url,tag,ids,out=sys.argv[1:5]; g=sys.argv[6] if len(sys.argv)>6 and sys.argv[5]=='--grayscale-dir' else None
    r=run(url,tag,ids.split(','),out,g)
    for k,v in r.items(): print(k,{a:(b['min'],b['p10'],b['med']) if isinstance(b,dict) else b if not isinstance(b,list) else len(b) for a,b in v.items()})
