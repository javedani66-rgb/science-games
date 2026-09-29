import sys
from harness import *
from t2 import SOL, spec, TURL
from PIL import Image
track=sys.argv[1]; keys=sys.argv[2].split(',')
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':400,'height':900}); g=G(pg)
    for k in keys:
        shots=[]
        pg.goto(TURL); pg.evaluate("p=>localStorage.setItem('sm-workshop-v3',JSON.stringify(p))",{"prog":{f"{track}:{k}":{"lv":[3,3,3,3,3],"best":3}},"nums":True,"forces":True,"formula":True,"track":track}); pg.reload(); pg.wait_for_timeout(150)
        pg.click(f'.st[data-k={k}]'); nL=pg.locator('[data-l]').count()
        pg.click('#lab'); pg.wait_for_timeout(400); fn=OUT+f'gal_{track}_{k}_lab.png'; pg.locator('#sc').screenshot(path=fn); shots.append(fn)
        seen=set()
        for L in range(1,nL+1):
            pg.goto(TURL); pg.wait_for_timeout(100); pg.click(f'.st[data-k={k}]'); pg.click(f'[data-l="{L}"]'); pg.wait_for_timeout(300)
            n=pg.locator('#dots i').count()
            for i in range(n):
                sp=spec(pg)['spec']; tp=str(sp.get('t'))
                if tp not in seen:
                    seen.add(tp); fn=OUT+f'gal_{track}_{k}_{L}_{i}.png'; pg.locator('#sc').screenshot(path=fn); shots.append(fn)
                try: SOL[k](g,pg,sp)
                except Exception: pass
                pg.wait_for_timeout(700)
                if not pg.locator('#nv .btn').count(): pg.wait_for_timeout(1800)
                if tp+'_post' not in seen:
                    seen.add(tp+'_post'); fn=OUT+f'gal_{track}_{k}_{L}_{i}p.png'; pg.locator('#sc').screenshot(path=fn); shots.append(fn)
                nb=pg.locator('#nv .btn')
                if nb.count()==0: break
                nb.first.click(); pg.wait_for_timeout(300)
        ims=[Image.open(f) for f in shots]; W=360
        ims=[i.resize((W,int(i.height*W/i.width))) for i in ims]
        cols=4; rows=[ims[j:j+cols] for j in range(0,len(ims),cols)]
        H=sum(max(i.height for i in r) for r in rows)
        c=Image.new('RGB',(W*cols,H),'white'); y=0
        for r in rows:
            for j,i in enumerate(r): c.paste(i,(j*W,y))
            y+=max(i.height for i in r)
        c.save(OUT+f'sheet_{track}_{k}.png'); print(k,len(shots))
    b.close()
