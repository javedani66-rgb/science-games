from harness import *
import math, sys
TURL='file://'+D+'test.html'
SHOT=False
def spec(pg): return pg.evaluate("()=>window.__T")
def stepper_set(pg,target):
    steps=pg.evaluate("()=>[...document.querySelectorAll('.stp button')].map(b=>+b.dataset.d).filter(v=>v>0)")
    steps=sorted(set(steps),reverse=True); v=0.0; clicks=[]
    for s in steps:
        while v+s<=target+1e-9: clicks.append(s); v+=s
    for s in clicks:
        pg.click(f'.stp button[data-d="{s:g}"]' if s!=int(s) else f'.stp button[data-d="{int(s)}"]')
    return abs(v-target)<1e-6
def click_text(pg,txt): pg.locator('#cl .btn',has_text=txt).first.click(); pg.wait_for_timeout(200)
def mcq(pg,i): pg.click(f'.mcq [data-i="{i}"]'); pg.wait_for_timeout(300)
def solve_coins(t,vals,maxn=6):
    best=None
    def f(s,acc):
        nonlocal best
        if s==0:
            if best is None or len(acc)<len(best): best=acc[:]
            return
        if len(acc)>=maxn or (best and len(acc)>=len(best)): return
        for v in sorted(vals,reverse=True):
            if v<=s: acc.append(v); f(s-v,acc); acc.pop()
    f(t,[]); return best

def force(g,pg,sp):
    t=sp['t']
    if t=='predict':
        sl,sr=sum(sp['L']),sum(sp['R']); mcq(pg,0 if sr>sl else 1 if sr==sl else 2); return
    if t=='fric':
        mcq(pg,0 if sp['q']==1 else 2); pg.wait_for_timeout(2000); return
    if t=='net':
        sl,sr=sum(sp['L']),sum(sp['R']); stepper_set(pg,abs(sr-sl)); d=1 if sr>sl else -1 if sr<sl else 0
        pg.click(f'#dirs [data-d="{d}"]'); click_text(pg,'بررسی'); return
    side=sp.get('side','R'); fixed=sum(sp['fixed']); tgt=0 if t=='balance' else sp['target']
    need=fixed+tgt if side=='R' else fixed-tgt
    combo=solve_coins(need,sp['tray'],4)
    tray=sp['tray']; x0=170 if side=='L' else 470
    for i,v in enumerate(combo):
        j=tray.index(v); tx=x0+(j-(len(tray)-1)/2)*84
        sx=(320-95-i*56) if side=="L" else (320+95+i*56)
        g.drag(tx,462,sx,300)
    if SHOT: g.shot(f'ch_force_{sp["t"]}_{need}')
    click_text(pg,'برو'); pg.wait_for_timeout(2300)

def scale(g,pg,sp):
    T=pg.evaluate("()=>window.__T"); MASS=T['MASS']; t=sp['t']
    SPR={'stone':(5,20),'brick':(2,10),'iron':(8,10)}
    if t in ('water','waterWhy','waterF'):
        g.drag(320,40,320,160,10); pg.wait_for_timeout(200)
        if SHOT: g.shot(f'ch_scale_{t}_{sp["obj"]}')
        if t=='waterF': stepper_set(pg,SPR[sp['obj']][1]); click_text(pg,'بررسی'); return
        mcq(pg,sp['ans']); return
    if t in ('moon','moonbal'):
        mcq(pg,0); pg.wait_for_timeout(1300); mcq(pg,1); return
    if 'ans' in sp:
        if SHOT: g.shot(f'ch_scale_{t}')
        mcq(pg,sp['ans']); return
    if t=='wcalc':
        ans=sp['m']*1.6 if sp['where']=='moon' else sp['m']*10; stepper_set(pg,round(ans,1)); click_text(pg,'بررسی'); return
    if t=='mcalc': stepper_set(pg,sp['W']/10); click_text(pg,'بررسی'); return
    u=sp['u']
    if t=='heavier':
        ma=MASS[u][sp['L'][0]]; mb=MASS[u][sp['R'][0]]
        mcq(pg,1); pg.wait_for_timeout(200)          # guess (free, never scored)
        g.drag(272,480,124,240); pg.wait_for_timeout(800); g.drag(320,480,516,240); pg.wait_for_timeout(1000)
        if SHOT: g.shot(f'ch_scale_heavier_{sp["L"][0]}')
        mcq(pg,0 if ma>mb else 1 if ma==mb else 2); return
    target=sum(MASS[u][i] for i in sp['obj'])
    combo=solve_coins(target,sp['tray'],12)
    n=len(sp['tray'])
    for v in combo:
        j=sp['tray'].index(v); x=320+(j-(n-1)/2)*min(90,560/n)
        g.drag(x,478,516,215); pg.wait_for_timeout(250)
    pg.wait_for_timeout(800)   # ترازوی زنده: بعد از ایستادن شاهین خودش داوری می‌کند
    if SHOT: g.shot(f'ch_scale_{t}_{u}_{target}')
    if t=='mystery':
        stepper_set(pg,target); click_text(pg,'بررسی'); return

def lever(g,pg,sp):
    T=pg.evaluate("()=>window.__T"); LM=T['LV_MASS']; t=sp['t']
    m=lambda it: it if isinstance(it,(int,float)) else LM[it]
    if t=='predict':
        tl=sum(-p*m(it) for p,it in sp['items'] if p<0); tr=sum(p*m(it) for p,it in sp['items'] if p>0)
        a=0 if tr>tl else 1 if tr==tl else 2
        if sp.get('poe') or pg.evaluate("()=>document.body.classList.contains('tr-a')"):
            mcq(pg,0); pg.wait_for_timeout(1800)
        mcq(pg,a); return
    if t=='mystery':
        my=[it for p,it in sp['items'] if isinstance(it,str)][0]; stepper_set(pg,LM[my]); click_text(pg,'بررسی'); return
    if t=='lift':
        W,Sv=sp['W'],sp['S']; best=None
        for f in range(-4,5):
            if W*(f+5)/(5-f)<=Sv+1e-9: best=f
        g.drag(320+2*52,340,320+best*52,340); pg.wait_for_timeout(200)
        if SHOT: g.shot(f'ch_lever_lift_{W}')
        click_text(pg,'فشار'); pg.wait_for_timeout(1500); return
    tl=sum(-p*m(it) for p,it in sp['items'] if p<0); tr=sum(p*m(it) for p,it in sp['items'] if p>0); need=tl-tr
    ps=sp['pieces']; sol=None
    def f(i,acc,s):
        nonlocal sol
        if sol: return
        if i==len(ps):
            if s==need: sol=acc[:]
            return
        for p in range(1,6): acc.append(p); f(i+1,acc,s+ps[i]*p); acc.pop()
    f(0,[],0)
    remaining=len(ps)
    for i,pos in enumerate(sol):
        n=remaining; x=320+(0-(n-1)/2)*min(96,560/max(n,1))
        g.drag(x,478,320+pos*52,250); remaining-=1; pg.wait_for_timeout(300)
    pg.wait_for_timeout(900)   # الاکلنگ زنده: بعد از ایستادن تخته خودش داوری می‌کند
    if SHOT: g.shot(f'ch_lever_bal_{need}')

def ramp(g,pg,sp):
    t=sp['t']; H=sp.get('H',1)
    if t=='cmp': mcq(pg,{1:2,2:2,3:0}[sp['q']]); return
    if t=='work': mcq(pg,1); return
    if t=='calcF': stepper_set(pg,sp['W']*H/sp['L']) or print('  stepper approx'); click_text(pg,'بررسی'); pg.wait_for_timeout(300); return
    if t=='calcL': stepper_set(pg,sp['W']*H/sp['S']); click_text(pg,'بررسی'); return
    L=H
    while sp['W']*H/L>sp['S']+1e-9: L+=.5
    run=math.sqrt(L*L-H*H)*70
    L0=min(6,H+1); x0=470-math.sqrt(L0*L0-H*H)*70
    g.drag(x0,380,470-run,380,20); pg.wait_for_timeout(150)
    if SHOT: g.shot(f'ch_ramp_fit_{sp["W"]}_{sp["S"]}')
    click_text(pg,'بکش'); pg.wait_for_timeout(2100)

def pull_until(g,pg,hx,maxn=12):
    for k in range(maxn):
        if pg.locator('#nv .btn').count(): break
        g.drag(hx,264,hx,264+150,10); pg.wait_for_timeout(300)
def pulley(g,pg,sp):
    t=sp['t']; HX={1:328,2:376,4:376,6:392}
    if t=='fixedq': mcq(pg,1); return
    if t=='fixedk': mcq(pg,0); return
    if t=='ropeq': mcq(pg,1); return
    if t=='count': stepper_set(pg,sp['n']); click_text(pg,'بررسی'); return
    if t=='calcF': stepper_set(pg,sp['W']/sp['n']); click_text(pg,'بررسی'); return
    if t=='calcRope': stepper_set(pg,sp['n']*sp['h']); click_text(pg,'بررسی'); return
    if t=='calcW': stepper_set(pg,sp['F']*sp['n']); click_text(pg,'بررسی'); return
    if t=='lift':
        if SHOT: g.shot(f'ch_pulley_lift_{sp["n"]}')
        pull_until(g,pg,HX[sp['n']]); return
    best=[n for n in sp['opts'] if sp['W']/n<=sp['S']+1e-9][0]
    pg.click(f'#sys [data-n="{best}"]'); pg.wait_for_timeout(150)
    if SHOT: g.shot(f'ch_pulley_choose_{best}')
    pull_until(g,pg,HX[best])

def crank(g,pg,R,turns):
    g.circle(420,137,R*14,turns+0.4,start=-math.pi/2)
def wheel(g,pg,sp):
    t=sp['t']
    if t=='mcq': mcq(pg,{1:0,2:2,3:0}[sp['q']]); return
    if t=='calcF': stepper_set(pg,sp['W']/sp['R']); click_text(pg,'بررسی'); return
    if t=='calcR': stepper_set(pg,math.ceil(sp['W']/sp['S'])); click_text(pg,'بررسی'); return
    if t=='calcPath': stepper_set(pg,sp['n']*sp['R']*.5); click_text(pg,'بررسی'); return
    if t=='crank':
        if SHOT: g.shot(f'ch_wheel_crank_{sp["R"]}')
        crank(g,pg,sp['R'],sp['h']/.5); return
    best=[R for R in sp['opts'] if sp['W']/R<=sp['S']+1e-9][0]
    pg.click(f'#rs [data-r="{best}"]'); pg.wait_for_timeout(150)
    if SHOT: g.shot(f'ch_wheel_choose_{best}')
    crank(g,pg,best,2)

def wedge(g,pg,sp):
    t=sp['t']
    if t=='mcq': mcq(pg,{1:0,2:1,3:1,4:1}[sp['q']]); return
    if t=='turns': stepper_set(pg,12/sp['p']); click_text(pg,'بررسی'); return
    if t=='wF': stepper_set(pg,sp['R']*2/sp['L']); click_text(pg,'بررسی'); return
    if t=='sF': stepper_set(pg,sp['R']*sp['p']/12); click_text(pg,'بررسی'); return
    if t=='wc':
        best=[L for L in sp['opts'] if sp['R']*2/L<=sp['S']+1e-9][0]
        pg.click(f'#vs [data-v="{best}"]'); pg.wait_for_timeout(150)
        top=240-best*9
        if SHOT: g.shot(f'ch_wedge_wc_{best}')
        g.drag(320,top-12,320,top-12+best*9*.85+30,15); pg.wait_for_timeout(900); return
    best=[p for p in sp['opts'] if sp['R']*p/12<=sp['S']+1e-9][0]
    pg.click(f'#vs [data-v="{best}"]'); pg.wait_for_timeout(150)
    if SHOT: g.shot(f'ch_wedge_sc_{best}')
    g.circle(320,150,62,12/best+0.4,start=-math.pi/2,ry=62*.45,steps_per_turn=24)

def sort(g,pg,sp):
    it=sp['item']; cat=it[1]; nb=sp['nb']
    cols=4 if nb==7 else 3; bw=146 if nb==7 else 196; bh=100
    row=cat//cols; inRow=min(cols,nb-row*cols); col=cat%cols; g2=(640-inRow*bw)/(inRow+1)
    x=g2+col*(bw+g2)+bw/2; y=200+row*(bh+14)+bh/2
    g.drag(320,92,x,y)

def fric(g,pg,sp):
    t=sp['t']
    if t=='fq':
        if sp.get('poe'): mcq(pg,1); pg.wait_for_timeout(2600)
        mcq(pg,{1:0,2:2,3:2,4:0,5:2}[sp['q']]); pg.wait_for_timeout(2000); return
    if t=='surf':
        a=sp['ans'] if sp['goal']=='flag' else (0 if sp['goal']=='move' else 2)
        pg.click(f'#surfs [data-s="{a}"]'); click_text(pg,'هل بده'); pg.wait_for_timeout(1900); return
    if t=='min':
        f=[4,15,35][sp['s']]; ans=(f//5)*5+5
        stepper_set(pg,ans-5); click_text(pg,'هل بده'); pg.wait_for_timeout(1900); return

SOL={'force':force,'fric':fric,'scale':scale,'lever':lever,'ramp':ramp,'pulley':pulley,'wheel':wheel,'wedge':wedge,'sort':sort}
if __name__=='__main__':
    track=sys.argv[3] if len(sys.argv)>3 else 'c'
    keys=sys.argv[1].split(',') if len(sys.argv)>1 and sys.argv[1]!='all' else list(SOL)
    with sync_playwright() as pw:
        b=pw.chromium.launch(); pg=b.new_page(viewport={'width':400,'height':900})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        g=G(pg)
        for k in keys:
            pg.goto(TURL); pg.evaluate("p=>localStorage.setItem('sm-workshop-v3',JSON.stringify(p))",{"prog":{f"{track}:{k}":{"lv":[3,3,3,3,3],"best":0}},"nums":True,"forces":True,"formula":True,"track":track}); pg.reload(); pg.wait_for_timeout(150)
            pg.click(f'.st[data-k={k}]'); nL=pg.locator('[data-l]').count()
            levels=[int(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 and sys.argv[2]!='all' else list(range(1,nL+1))
            for L in levels:
                pg.goto(TURL); pg.wait_for_timeout(100); pg.click(f'.st[data-k={k}]'); pg.click(f'[data-l="{L}"]'); pg.wait_for_timeout(300)
                got=[]; n=pg.locator('#dots i').count()
                for i in range(n):
                    sp=spec(pg)['spec']
                    try: SOL[k](g,pg,sp)
                    except Exception as e: print('  EXC',k,L,i,sp.get('t'),e)
                    pg.wait_for_timeout(500)
                    if not pg.locator('#nv .btn').count(): pg.wait_for_timeout(1500)
                    cls=pg.evaluate("i=>{const d=document.querySelectorAll('#dots i')[i];return d?d.className:''}",i)
                    got.append(cls)
                    if cls!='p2': print('  !!',k,L,i,sp.get('t'),cls,g.text('#fb')[:120].replace('\n',' '))
                    nb=pg.locator('#nv .btn')
                    if nb.count()==0: print('  no next button',k,L,i); break
                    nb.first.click(); pg.wait_for_timeout(300)
                res=g.text('.res') if pg.locator('.res').count() else ''
                print(track,k,L,got,res.replace('\n',' ')[:30])
        print('ERR',errs[:8]); b.close()
