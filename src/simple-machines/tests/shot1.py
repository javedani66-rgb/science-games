from harness import *
from t2 import SOL, spec
import sys
k=sys.argv[1];L=sys.argv[2];tr=sys.argv[3];w=int(sys.argv[4]) if len(sys.argv)>4 else 390;h=int(sys.argv[5]) if len(sys.argv)>5 else 844
with sync_playwright() as pw:
    b=pw.chromium.launch();pg=b.new_page(viewport={'width':w,'height':h});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    g=G(pg);pg.goto('file://'+D+'test.html');pg.evaluate("p=>localStorage.setItem('sm-workshop-v3',JSON.stringify(p))",{"prog":{f"{tr}:{k}":{"lv":[3,3,3,3,3],"best":0}},"nums":True,"forces":True,"formula":True,"track":tr});pg.reload();pg.wait_for_timeout(200)
    pg.click(f'.st[data-k={k}]');pg.click(f'[data-l="{L}"]');pg.wait_for_timeout(500);pg.screenshot(path=OUT+f'v2_{k}{L}{tr}_a.png')
    sp=spec(pg)['spec'];SOL[k](g,pg,sp);pg.wait_for_timeout(1500);pg.screenshot(path=OUT+f'v2_{k}{L}{tr}_b.png');print(errs)
