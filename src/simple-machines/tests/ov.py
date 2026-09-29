import sys
from harness import *
from t2 import SOL, spec, TURL
CHK=r"""()=>{const svg=document.querySelector('#sc');if(!svg)return [];const vb=svg.viewBox.baseVal;const out=[];
const txt=[...svg.querySelectorAll('text')].filter(t=>t.textContent.trim()&&!t.getAttribute('transform')&&getComputedStyle(t).display!=='none'&&t.getAttribute('opacity')!=='0');
const R=t=>{const b=t.getBBox();let m=t.getCTM(),s=svg.getCTM().inverse();const M=s.multiply(m);const p=(x,y)=>{const q=svg.createSVGPoint();q.x=x;q.y=y;return q.matrixTransform(M)};const a=p(b.x,b.y),c=p(b.x+b.width,b.y+b.height);return{x:Math.min(a.x,c.x),y:Math.min(a.y,c.y),w:Math.abs(c.x-a.x),h:Math.abs(c.y-a.y),s:t.textContent.trim().slice(0,18)}};
const rs=txt.map(R).filter(r=>r.w>0);
for(const r of rs){if(r.x<-1||r.x+r.w>vb.width+1||r.y<-1||r.y+r.h>vb.height+1)out.push('CLIP '+r.s);}
const sh=(r,d)=>({x:r.x+d,y:r.y+d,w:r.w-2*d,h:r.h-2*d});
const hit=(a,b)=>a.x<b.x+b.w&&b.x<a.x+a.w&&a.y<b.y+b.h&&b.y<a.y+a.h;
for(let i=0;i<rs.length;i++)for(let j=i+1;j<rs.length;j++){const a=sh(rs[i],3),b=sh(rs[j],3);if(hit(a,b))out.push('TT '+rs[i].s+' | '+rs[j].s);}
for(const pol of svg.querySelectorAll('polygon.farr')){const M=svg.getCTM().inverse().multiply(pol.getCTM());const pts=[...pol.points].map(q=>{const z=svg.createSVGPoint();z.x=q.x;z.y=q.y;return z.matrixTransform(M)});
  for(const r of rs){const a=sh(r,4);let bad=false;for(let k=0;k<pts.length&&!bad;k++){const p=pts[k],q=pts[(k+1)%pts.length];const n=Math.max(1,Math.ceil(Math.hypot(q.x-p.x,q.y-p.y)/2));for(let s=0;s<=n;s++){const x=p.x+(q.x-p.x)*s/n,y=p.y+(q.y-p.y)*s/n;if(x>a.x&&x<a.x+a.w&&y>a.y&&y<a.y+a.h){bad=true;break;}}}
  if(!bad){const cx=pts.reduce((s,p)=>s+p.x,0)/pts.length,cy=pts.reduce((s,p)=>s+p.y,0)/pts.length;if(cx>a.x&&cx<a.x+a.w&&cy>a.y&&cy<a.y+a.h)bad=true;}
  if(bad)out.push('AT '+r.s);}}
return [...new Set(out)];}"""
track=sys.argv[1]; keys=sys.argv[2].split(',') if len(sys.argv)>2 else list(SOL)
found={}
def check(pg,where):
    try: r=pg.evaluate(CHK)
    except Exception as e: r=['ERR '+str(e)[:60]]
    new=[x for x in r if x not in found]
    for x in r: found.setdefault(x,where)
    if new:
        import re
        fn=OUT+'ov_'+track+'_'+re.sub(r'[^a-zA-Z0-9]+','_',where)+'.png'
        try: pg.locator('#sc').screenshot(path=fn)
        except Exception: pass
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':400,'height':900}); g=G(pg)
    for k in keys:
        pg.goto(TURL); pg.evaluate("p=>localStorage.setItem('sm-workshop-v3',JSON.stringify(p))",{"prog":{f"{track}:{k}":{"lv":[3,3,3,3,3],"best":3}},"nums":True,"forces":True,"formula":True,"track":track}); pg.reload(); pg.wait_for_timeout(150)
        pg.click(f'.st[data-k={k}]'); nL=pg.locator('[data-l]').count()
        pg.click('#lab'); pg.wait_for_timeout(400); check(pg,f'{k} lab')
        for L in range(1,nL+1):
            pg.goto(TURL); pg.wait_for_timeout(100); pg.click(f'.st[data-k={k}]'); pg.click(f'[data-l="{L}"]'); pg.wait_for_timeout(300)
            n=pg.locator('#dots i').count()
            for i in range(n):
                sp=spec(pg)['spec']; check(pg,f'{k} L{L} c{i} {sp.get("t")} pre')
                try: SOL[k](g,pg,sp)
                except Exception as e: pass
                pg.wait_for_timeout(700)
                if not pg.locator('#nv .btn').count(): pg.wait_for_timeout(1800)
                check(pg,f'{k} L{L} c{i} {sp.get("t")} post')
                nb=pg.locator('#nv .btn')
                if nb.count()==0: break
                nb.first.click(); pg.wait_for_timeout(300)
    for x,w in found.items(): print(track,'|',w,'|',x)
    b.close()
