"""بررسی هم‌پوشانی: نقطه‌های مسیر (هر ۳px) با چسبک‌ها، لوحه، نشان فصل، راهنما، و قرص گره‌های غیرهمسایه. باید «0» چاپ کند."""
import sys,json
from playwright.sync_api import sync_playwright
H='/home/claude/science-games/design/mockups/20261008/flow-demo/v3/kit4/proof.html'
JS="""()=>{
 const out=[];
 document.querySelectorAll('.landwrap').forEach(w=>{
  const land=w.querySelector('.land'),svg=land.querySelector('.land__path'),m=svg.getScreenCTM();
  const rects=[...land.querySelectorAll('.node__labels .chip,.plate,.land__sym,.guide,.sign')].map(e=>({k:e.className.toString().slice(0,30)+':'+(e.textContent||'').trim().slice(0,10),r:e.getBoundingClientRect(),sign:e.classList.contains('sign')}));
  const nodes=[...land.querySelectorAll('.node')].map(n=>{const d=n.querySelector('.node__disc').getBoundingClientRect();return{id:n.dataset.id,cx:d.left+d.width/2,cy:d.top+d.height*.467,r:d.width*.45}});
  const paths=[...svg.querySelectorAll('.pt-fill')];
  paths.forEach(p=>{const L=p.getTotalLength();
   // قطعه‌ها: M جدید = ابتدای هر قطعه؛ برای همسایگی گره از نزدیک‌ترین دو گره به نقطهٔ شروع/پایان استفاده می‌کنیم
   for(let s=0;s<=L;s+=3){const q=p.getPointAtLength(s);const x=q.x*m.a+q.y*m.c+m.e,y=q.x*m.b+q.y*m.d+m.f;
     for(const R of rects){const r=R.r;if(x>r.left-3&&x<r.right+3&&y>r.top-3&&y<r.bottom+3){ if(R.sign)continue; out.push({what:R.k,x:Math.round(x),y:Math.round(y)});break}}
   }});
 });
 return out}"""
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':390,'height':1100}); pg.goto('file://'+H+'?v=stadium'); pg.wait_for_function("document.documentElement.dataset.ready==='1'"); pg.wait_for_timeout(300)
    pg.add_style_tag(content="#phone{height:100000px!important}.body{overflow:visible!important}")
    pg.wait_for_timeout(300)
    o=pg.evaluate(JS); b.close()
agg={}
for e in o: agg.setdefault(e['what'],[]).append((e['x'],e['y']))
print(len(o)); 
for k,v in agg.items(): print(k,len(v),v[:3])
