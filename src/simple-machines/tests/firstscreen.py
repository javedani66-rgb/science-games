# First screen of every challenge kind, per station and track (desktop layout: scene + text panel).
# Purpose: check that everything the question is about is visible on screen before the child acts.
# usage: python3 firstscreen.py <track> <stations>   → shots/first_<track>_<station>.png contact sheets
import sys
from harness import *
from t2 import SOL, spec, TURL
from PIL import Image, ImageDraw
track=sys.argv[1]; keys=sys.argv[2].split(',')
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':800}); g=G(pg)
    for k in keys:
        shots=[]
        pg.goto(TURL); pg.evaluate("p=>localStorage.setItem('sm-workshop-v3',JSON.stringify(p))",{"prog":{f"{track}:{k}":{"lv":[3,3,3,3,3],"best":3}},"nums":True,"forces":True,"formula":False,"track":track}); pg.reload(); pg.wait_for_timeout(150)
        pg.click(f'.st[data-k={k}]'); nL=pg.locator('[data-l]').count()
        seen=set()
        for L in range(1,nL+1):
            pg.goto(TURL); pg.wait_for_timeout(100); pg.click(f'.st[data-k={k}]'); pg.click(f'[data-l="{L}"]'); pg.wait_for_timeout(350)
            n=pg.locator('#dots i').count()
            for i in range(n):
                sp=spec(pg)['spec']; key=f"{sp.get('t')}|{sp.get('q','')}|{sp.get('goal','')}|{bool(sp.get('poe'))}"
                if key not in seen:
                    seen.add(key); fn=OUT+f'fs_{track}_{k}_{L}_{i}.png'; pg.screenshot(path=fn); shots.append((fn,f'{k} L{L} #{i+1} {key}'))
                try: SOL[k](g,pg,sp)
                except Exception: pass
                pg.wait_for_timeout(600)
                if not pg.locator('#nv .btn.next').count(): pg.wait_for_timeout(1800)
                nb=pg.locator('#nv .btn.next')
                if nb.count()==0: break
                nb.first.click(); pg.wait_for_timeout(300)
        W,H=640,400; cols=3; rows=(len(shots)+cols-1)//cols
        sheet=Image.new('RGB',(W*cols,(H+24)*rows),'white'); d=ImageDraw.Draw(sheet)
        for j,(f,lab) in enumerate(shots):
            im=Image.open(f).resize((W,H)); x=(j%cols)*W; y=(j//cols)*(H+24)
            sheet.paste(im,(x,y+24)); d.text((x+6,y+5),lab,fill='black')
        sheet.save(OUT+f'first_{track}_{k}.png'); print(k,len(shots),'kinds')
    b.close()
