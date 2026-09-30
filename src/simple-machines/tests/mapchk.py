# نقشه: عکس بازیکن و «تو اینجایی» برای هر منزل ۱ تا ۱۲ باید داخل نقشه باشد و روی چیز دیگری نیفتد.
# استفاده: python3 mapchk.py [grade 0..7]   — فقط مشکل‌ها را چاپ می‌کند؛ عکس‌ها در shots/map_<w>_<stop>.png
import sys
from harness import *
JURL='file://'+D+'jtest.html'
grade=int(sys.argv[1]) if len(sys.argv)>1 else 0
CHK="""()=>{const svg=document.querySelector('.j-map'),h=svg.querySelector('.j-here');if(!h)return['no marker'];
 const vb=svg.viewBox.baseVal,out=[],inv=svg.getCTM().inverse();
 const shape=e=>{const r=e.getBBox(),m=inv.multiply(e.parentNode.getCTM()),X=(x,y)=>[m.a*x+m.c*y+m.e,m.b*x+m.d*y+m.f];
   if(e.tagName==='circle'||e.tagName==='image'){const c=X(r.x+r.width/2,r.y+r.height/2);return{c:[c[0],c[1],r.width/2]};}
   let [x0,y0]=X(r.x,r.y),[x1,y1]=X(r.x+r.width,r.y+r.height);const tf=e.getAttribute('transform');
   if(tf&&tf.startsWith('rotate')){const cx=(x0+x1)/2,cy=(y0+y1)/2,s=(x1-x0)*.71;return{c:[cx,cy,s*.9]};}
   return{b:[Math.min(x0,x1),Math.min(y0,y1),Math.max(x0,x1),Math.max(y0,y1)]};};
 const hit=(A,B)=>{if(A.b&&B.b)return A.b[0]<B.b[2]&&A.b[2]>B.b[0]&&A.b[1]<B.b[3]&&A.b[3]>B.b[1];
   if(A.c&&B.c)return Math.hypot(A.c[0]-B.c[0],A.c[1]-B.c[1])<A.c[2]+B.c[2];const c=(A.c||B.c),b=(A.b||B.b);
   return Math.hypot(c[0]-Math.max(b[0],Math.min(c[0],b[2])),c[1]-Math.max(b[1],Math.min(c[1],b[3])))<c[2];};
 const mine=[...h.querySelectorAll('circle,rect')].map(shape);
 mine.forEach(s=>{const b=s.b||[s.c[0]-s.c[2],0,s.c[0]+s.c[2],0];if(b[0]<0||b[2]>vb.width)out.push('outside x '+Math.round(b[0])+'..'+Math.round(b[2]));});
 const els=[...svg.querySelectorAll('text,circle,image,rect')].filter(e=>!h.contains(e)&&!(e.tagName==='rect'&&e.getAttribute('height')>200)&&e.getAttribute('fill-opacity')!=='0'&&!e.closest('text')||e.tagName==='text'&&!h.contains(e));
 for(const e of els){const s=shape(e);if(mine.some(m=>hit(m,s)))out.push('overlap '+e.tagName+' '+(e.textContent||e.getAttribute('class')||'').slice(0,20));}
 return [...new Set(out)];}"""
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for w,hgt in ((390,844),(1280,800)):
        pg=b.new_page(viewport={'width':w,'height':hgt}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(JURL); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(200)
        pg.fill('#jnm','سارا'); pg.click('#jnx'); pg.click('[data-t="1"]'); pg.click('#jnx')
        pg.click(f'[data-g="{grade}"]'); pg.click('#jnx'); pg.wait_for_timeout(400)
        if pg.locator('#jok').count(): pg.click('#jok'); pg.wait_for_timeout(200)
        for cs in range(12):
            pg.evaluate("""cs=>{const {curP,missions,trk,jmap,save}=__J;const p=curP();p.S.prog={};
              for(let i=0;i<cs;i++)missions(p,i).forEach(([k,L])=>{const key=trk(p)+':'+k;const g=p.S.prog[key]=p.S.prog[key]||{lv:[]};g.lv[L-1]=2;});
              save();jmap({});}""",cs)
            pg.wait_for_timeout(150)
            if pg.locator('.ovl').count(): pg.evaluate("__J.closeOv()"); pg.wait_for_timeout(100)
            cur=pg.evaluate("()=>__J.curStop(__J.curP())")
            if cur!=cs: print(w,'stop',cs+1,'curStop mismatch',cur+1); continue
            bad=pg.evaluate(CHK)
            # نشانگر روی صفحه (نه فقط داخل نقشه) هم باید کامل دیده شود
            r=pg.evaluate("()=>{const r=document.querySelector('.j-here').getBoundingClientRect();return [r.left,r.right]}")
            if r[0]<0 or r[1]>w: bad.append(f'off screen {r}')
            if bad: print(w,'stop',cs+1,bad)
            pg.evaluate("()=>document.querySelector('.j-here').scrollIntoView({block:'center'})"); pg.wait_for_timeout(150)
            pg.screenshot(path=OUT+f'map_{w}_{cs+1}.png')
        if errs: print('ERR',errs)
        pg.close()
    b.close()
