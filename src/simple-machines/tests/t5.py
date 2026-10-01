from t2 import *
import t2
t2.SHOT=False
TR=sys.argv[1] if len(sys.argv)>1 else 'c'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':400,'height':900}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); g=G(pg)
    for k in ['force','fric','scale','lever','ramp','pulley','wheel','wedge','sort']:
        for rep in range(1):
            pg.goto(TURL); pg.evaluate("p=>localStorage.setItem('sm-workshop-v3',JSON.stringify(p))",{"prog":{f"{TR}:{k}":{"lv":[3,3,3,3,3],"best":0}},"nums":True,"forces":True,"formula":True,"track":TR}); pg.reload(); pg.wait_for_timeout(150)
            pg.click(f'.st[data-k={k}]'); pg.click('#end'); pg.wait_for_timeout(300)
            types=[]
            for n in range(8):
                sp=spec(pg)['spec']; types.append(sp.get('t','sort'))
                try: SOL[k](g,pg,sp)
                except Exception as e: print('  EXC',k,n,sp,e); break
                pg.wait_for_timeout(500)
                if not pg.locator('#nv .btn').count(): pg.wait_for_timeout(1500)
                if not pg.locator('#nv .btn').count(): print('  stuck',k,n,sp,g.text('#fb')[:90]); break
                sc=g.text('#scr')
                pg.locator('#nv .btn').first.click(); pg.wait_for_timeout(300)
            print(k,rep,sc,types)
    print('ERR',errs)
