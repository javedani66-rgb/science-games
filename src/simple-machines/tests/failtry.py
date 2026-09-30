# سطح ۱ (کاوشگر): امتحانِ ناموفق در شیب، قرقره، چرخ و محور، گوه و پیچ نباید فرصت کم کند.
# برای هر ایستگاه: اولین چالشِ «امتحان کردنی» را پیدا می‌کند، n بار عمداً اشتباه امتحان می‌کند،
# بعد درست حلش می‌کند. انتظار: درست شدن تا امتحانِ سوم (۲ ناموفق) → ۲ امتیاز (p2)، دیرتر → ۱ امتیاز (p1)، هیچ‌وقت قفل/صفر نشود.
# در سطح ۲ (b) باید مثل قبل بماند: دو اشتباه = تمام (p0).
# استفاده: python3 failtry.py
from t2 import *
KIND={'ramp':('fit',),'pulley':('choose',),'wheel':('choose',),'wedge':('wc','sc')}
LEVEL={'a':{'ramp':2,'pulley':2,'wheel':2,'wedge':1},'b':{'ramp':2,'pulley':1,'wheel':1,'wedge':1}}
def fail_once(g,pg,k,sp):
    t=sp['t']
    if k=='ramp': click_text(pg,'بکش'); pg.wait_for_timeout(1800); return
    if k=='pulley':
        bad=[n for n in sp['opts'] if sp['W']/n>sp['S']+1e-9][0]
        pg.click(f'#sys [data-n="{bad}"]'); pg.wait_for_timeout(150); g.drag({1:328,2:376,4:376,6:392}[bad],264,{1:328,2:376,4:376,6:392}[bad],400,8); pg.wait_for_timeout(300); return
    if k=='wheel':
        bad=[R for R in sp['opts'] if sp['W']/R>sp['S']+1e-9][0]
        pg.click(f'#rs [data-r="{bad}"]'); pg.wait_for_timeout(150); crank(g,pg,bad,.5); pg.wait_for_timeout(300); return
    if t=='wc':
        bad=[L for L in sp['opts'] if sp['R']*2/L>sp['S']+1e-9][0]
        pg.click(f'#vs [data-v="{bad}"]'); pg.wait_for_timeout(150); top=240-bad*9; g.drag(320,top-12,320,top+60,10); pg.wait_for_timeout(600); return
    bad=[p for p in sp['opts'] if sp['R']*p/12>sp['S']+1e-9][0]
    pg.click(f'#vs [data-v="{bad}"]'); pg.wait_for_timeout(150); g.circle(320,150,62,1,start=-math.pi/2,ry=62*.45); pg.wait_for_timeout(300)
def dot(pg,i): return pg.evaluate("i=>{const d=document.querySelectorAll('#dots i')[i];return d?d.className:''}",i)
ok=True
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':400,'height':900}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); g=G(pg)
    for track,cases in (('a',((1,'p2'),(2,'p2'),(3,'p1'))),('b',((1,'cur'),(2,'p0')))):
        for k in KIND:
            for nfail,want in cases:
                pg.goto(TURL); pg.evaluate("p=>localStorage.setItem('sm-workshop-v3',JSON.stringify(p))",{"prog":{f"{track}:{k}":{"lv":[3,3,3,3,3],"best":0}},"nums":True,"forces":True,"formula":True,"track":track}); pg.reload(); pg.wait_for_timeout(150)
                pg.click(f'.st[data-k={k}]'); pg.click(f'[data-l="{LEVEL[track][k]}"]'); pg.wait_for_timeout(300)
                i=0
                while spec(pg)['spec']['t'] not in KIND[k]:
                    SOL[k](g,pg,spec(pg)['spec']); pg.wait_for_timeout(500); pg.locator('#nv .btn').first.click(); pg.wait_for_timeout(300); i+=1
                sp=spec(pg)['spec']; msgs=[]
                for n in range(nfail):
                    fail_once(g,pg,k,sp); msgs.append(g.text('#fb')[:60])
                    if pg.locator('#nv .btn').count(): break
                if nfail==3 and track=='a' and k=='ramp': g.shot('failtry_ramp_a')
                if want!='p0' and not pg.locator('#nv .btn').count():
                    SOL[k](g,pg,sp); pg.wait_for_timeout(600)
                    if not pg.locator('#nv .btn').count(): pg.wait_for_timeout(1500)
                got=dot(pg,i)
                if track=='b' and want=='cur': want='p1'   # یک اشتباه در سطح ۲ → بعد از حل، ۱ امتیاز
                good=got==want; ok&=good
                print(('OK ' if good else '!! '),track,k,sp['t'],'fails',nfail,'->',got,'(want',want+')','|',msgs[-1] if msgs else '')
    print('ERR',errs[:5]); print('ALL OK' if ok else 'PROBLEMS'); b.close()
