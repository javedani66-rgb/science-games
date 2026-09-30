# «جواب پیش از پاسخ لو نرود»: در هر چالشی که بچه باید عدد وارد کند، پیش از زدن دکمه‌ها
# بررسی می‌کند عددِ جواب (با رقم فارسی) در صحنه یا شمارنده‌ها دیده می‌شود یا نه.
# استفاده: python3 leakchk.py <track> [stations]   — فقط موارد مشکوک را چاپ می‌کند (بعد با چشم ببینید).
import sys, re
import t2
from t2 import *
FA=str.maketrans('0123456789.','۰۱۲۳۴۵۶۷۸۹٫')
def fa(x):
    s=('%g'%x); return s.translate(FA)
track=sys.argv[1]; keys=sys.argv[2].split(',') if len(sys.argv)>2 else [k for k in SOL if k!='sort']
_orig=t2.stepper_set
CUR={}
def spy(pg,target):
    if target not in (0,) and not CUR.get('done'):
        txt=pg.evaluate("()=>{const s=[...document.querySelectorAll('#sc text')].map(t=>t.textContent).join(' | ');const c=(document.querySelector('#ct')||{}).textContent||'';return s+' || '+c}")
        f=fa(target)
        if re.search(r'(?<![۰-۹٫])'+re.escape(f)+r'(?![۰-۹٫])',txt):
            print('LEAK?',track,CUR['k'],'L',CUR['L'],CUR['sp'].get('t'),'answer',f,'|',txt[:160].replace('\n',' '))
        CUR['done']=True
    return _orig(pg,target)
t2.stepper_set=spy
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':400,'height':900}); g=G(pg)
    for k in keys:
        pg.goto(TURL); pg.evaluate("p=>localStorage.setItem('sm-workshop-v3',JSON.stringify(p))",{"prog":{f"{track}:{k}":{"lv":[3,3,3,3,3],"best":0}},"nums":True,"forces":True,"formula":True,"track":track}); pg.reload(); pg.wait_for_timeout(150)
        pg.click(f'.st[data-k={k}]'); nL=pg.locator('[data-l]').count()
        for L in range(1,nL+1):
            pg.goto(TURL); pg.wait_for_timeout(100); pg.click(f'.st[data-k={k}]'); pg.click(f'[data-l="{L}"]'); pg.wait_for_timeout(300)
            for i in range(pg.locator('#dots i').count()):
                sp=spec(pg)['spec']; CUR.update(k=k,L=L,sp=sp,done=False)
                try: SOL[k](g,pg,sp)
                except Exception as e: print('  EXC',k,L,i,e)
                pg.wait_for_timeout(500)
                if not pg.locator('#nv .btn').count(): pg.wait_for_timeout(1500)
                nb=pg.locator('#nv .btn')
                if not nb.count(): break
                nb.first.click(); pg.wait_for_timeout(300)
    b.close()
print('leakchk done',track)
