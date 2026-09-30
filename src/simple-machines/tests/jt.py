import sys
from harness import *
from t2 import SOL, spec
JURL='file://'+D+'jtest.html'
grade=int(sys.argv[1]); upto=int(sys.argv[2]) if len(sys.argv)>2 else 12
tag=f'g{grade}'
def solve_quiz(pg,log,shot=None):
    pg.click('#jqs'); pg.wait_for_timeout(300); k=0
    while pg.locator('.qo').count() and not pg.locator('#jm').count() and k<40:
        k+=1; a=pg.evaluate("()=>window.__Q.ans")
        if shot and k==1: pg.screenshot(path=OUT+shot+'_q.png')
        pg.click(f'.qo[data-i="{a}"]'); pg.wait_for_timeout(150)
        if shot and k==1: pg.screenshot(path=OUT+shot+'_q2.png')
        pg.click('#nv .btn'); pg.wait_for_timeout(200)
    if shot: pg.screenshot(path=OUT+shot+'_qres.png')
    if not pg.locator('#jm').count(): log.append('quiz no result')
    pg.click('#jm'); pg.wait_for_timeout(500)
def solve_level(pg,g,log):
    n=pg.locator('#dots i').count(); cur=pg.evaluate("()=>[...document.querySelectorAll('#dots i')].findIndex(e=>e.className==='cur')")
    for i in range(max(0,cur),n):
        T=spec(pg); sp=T['spec']; k=T['k']
        try: SOL[k](g,pg,sp)
        except Exception as e: log.append(f'EXC {k} {i} {sp.get("t")} {e}')
        pg.wait_for_timeout(450)
        if not pg.locator('#nv .btn').count(): pg.wait_for_timeout(1500)
        cls=pg.evaluate("i=>{const d=document.querySelectorAll('#dots i')[i];return d?d.className:''}",i)
        if cls!='p2': log.append(f'!! {k} {i} {sp.get("t")} {cls} {g.text("#fb")[:80]}')
        nb=pg.locator('#nv .btn')
        if nb.count()==0: log.append(f'no next {k} {i}'); return
        nb.first.click(); pg.wait_for_timeout(300)
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':400,'height':860},has_touch=False)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); g=G(pg); log=[]
    pg.goto(JURL); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(200)
    pg.screenshot(path=OUT+tag+'_w1.png')
    pg.fill('#jnm','سارا'); pg.click('#jnx'); pg.click('[data-t="1"]'); pg.click('[data-sh="#7A3FC8"]'); pg.wait_for_timeout(300); pg.screenshot(path=OUT+tag+'_w2.png'); pg.click('#jnx')
    pg.click(f'[data-g="{grade}"]'); pg.screenshot(path=OUT+tag+'_w3.png'); pg.click('#jnx'); pg.wait_for_timeout(500)
    pg.screenshot(path=OUT+tag+'_coach.png'); pg.click('#jok'); pg.wait_for_timeout(200)
    pg.screenshot(path=OUT+tag+'_map0.png')
    # validate all mission levels exist
    bad=pg.evaluate("()=>{const {curP,missions,levelsOf}=__J;const p=curP();const out=[];for(let i=0;i<12;i++)missions(p,i).forEach(([k,L])=>{if(!levelsOf(k)[L-1])out.push(i+':'+k+L)});return out}")
    print('bad levels',bad)
    for stop in range(upto):
        pg.click('#jgo'); pg.wait_for_timeout(300)
        if pg.locator('#jqs').count():
            solve_quiz(pg,log,tag+f'_quiz{stop}' if stop in (2,) else None); pg.wait_for_timeout(300)
            if pg.locator('.ovl').count(): pg.evaluate("__J.closeOv()")
            pg.click('#jgo'); pg.wait_for_timeout(300)
        if pg.locator('#jgo2').count():
            if stop in (0,2): pg.screenshot(path=OUT+f'{tag}_word{stop}.png')
            pg.click('#jgo2'); pg.wait_for_timeout(300)
        while True:
            if stop==1 and not pg.evaluate("()=>window.__rs"):
                # resume test: solve first challenge, go back to map, reload, continue
                T=spec(pg); SOL[T['k']](g,pg,T['spec']); pg.wait_for_timeout(500); pg.locator('#nv .btn').first.click(); pg.wait_for_timeout(300)
                i0=T['spec']; pg.click('#bk'); pg.wait_for_timeout(300); pg.screenshot(path=OUT+tag+'_backmap.png')
                pg.reload(); pg.wait_for_timeout(300); lab=g.text('#jgo'); print('continue label:',lab.replace('\n',' | '))
                pg.click('#jgo'); pg.wait_for_timeout(300)
                cur=pg.evaluate("()=>[...document.querySelectorAll('#dots i')].map(e=>e.className).join(',')"); print('resumed dots:',cur)
                pg.evaluate("()=>window.__rs=1")
            if stop==2: pg.screenshot(path=OUT+tag+'_mission.png')
            solve_level(pg,g,log)
            pg.wait_for_timeout(400)
            if stop in (0,4): pg.screenshot(path=OUT+f'{tag}_res{stop}.png')
            t=g.text('#jn') if pg.locator('#jn').count() else ''
            if 'بعدی' in t: pg.click('#jn'); pg.wait_for_timeout(300);
            else:
                pg.click('#jn'); pg.wait_for_timeout(700); break
        cs=pg.evaluate("()=>{const {curP,curStop}=__J;return curStop(curP())}"); print('stop',stop+1,'-> curStop',cs+1)
    if upto>=12:
        pg.click('#jgo'); pg.wait_for_timeout(300)
        if pg.locator('#jqs').count(): solve_quiz(pg,log,tag+'_final')
        pg.wait_for_timeout(400); pg.screenshot(path=OUT+tag+'_levelup.png')
        print('done levels', pg.evaluate("()=>__J.curP().done"))
        if pg.locator('#jup').count(): pg.click('#jup'); pg.wait_for_timeout(500); print('now level', pg.evaluate("()=>__J.trk(__J.curP())"))
        pg.evaluate("()=>{const p=__J.curP();}")
    pg.screenshot(path=OUT+tag+'_mapN.png')
    pg.screenshot(path=OUT+tag+'_mapN_full.png',full_page=True)
    # side quest on stop 1
    pg.evaluate("()=>{window.scrollTo(0,0)}"); pg.locator('[data-side="0"]').dispatch_event('click'); pg.wait_for_timeout(300); pg.screenshot(path=OUT+tag+'_side.png'); pg.click('#jsd'); pg.wait_for_timeout(300)
    for _ in range(12):
        if pg.locator('#jm').count(): break
        T=spec(pg); SOL[T['k']](g,pg,T['spec']); pg.wait_for_timeout(900)
        if pg.locator('#jm').count(): break
        nb=pg.locator('#nv .btn')
        if nb.count(): nb.first.click(); pg.wait_for_timeout(300)
    pg.screenshot(path=OUT+tag+'_sidewin.png'); print('side done', pg.evaluate("()=>{const {curP,curStop}=__J;return curP().side[0]}"))
    pg.click('#jm'); pg.wait_for_timeout(300)
    # stop sheet + home confirm
    pg.locator('[data-stop="0"]').dispatch_event('click'); pg.wait_for_timeout(300); pg.screenshot(path=OUT+tag+'_sheet.png')
    box=pg.locator('#jhh').bounding_box(); pg.mouse.move(box['x']+20,box['y']+20); pg.mouse.down(); pg.wait_for_timeout(2300); pg.mouse.up(); pg.wait_for_timeout(300)
    print('home0',pg.evaluate("()=>{const {curP,curStop}=__J;return curP().home[0]}")); pg.keyboard.press('Escape'); pg.evaluate("__J.closeOv()")
    # backpack + code roundtrip
    pg.click('#jbp'); pg.wait_for_timeout(200); pg.click('[data-tab="c"]'); pg.wait_for_timeout(200)
    msg=pg.input_value('#jmsg'); print(msg); pg.screenshot(path=OUT+tag+'_msg.png')
    before=pg.evaluate("()=>{const {curP,missions,mStars}=__J;return JSON.stringify({s:[...Array(12)].map((_,i)=>missions(curP(),i).map((_,j)=>mStars(curP(),i,j))),h:curP().home,sd:curP().side})}")
    pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(200)
    pg.fill('#jnm','سارا'); pg.click('#jnx'); pg.click('[data-t="0"]'); pg.click('#jnx'); pg.click('[data-g="0"]'); pg.click('#jnx'); pg.wait_for_timeout(300); pg.click('#jok')
    pg.click('#jbp'); pg.click('[data-tab="c"]'); pg.fill('#jin','سلام خانم\n'+msg); pg.click('#jld'); pg.wait_for_timeout(1300)
    after=pg.evaluate("()=>{const {curP,missions,mStars}=__J;return JSON.stringify({s:[...Array(12)].map((_,i)=>missions(curP(),i).map((_,j)=>mStars(curP(),i,j))),h:curP().home,sd:curP().side})}")
    print('roundtrip', before==after, pg.evaluate("()=>{const {curP,curStop}=__J;return [curP().g,curP().t,curP().shirt,curP().lvl,curP().done,curP().quiz.join('')]}"))
    # teacher page
    pg.goto(JURL+'#teacher'); pg.reload(); pg.wait_for_timeout(300); pg.fill('#jta',msg+'\n\nنام: علی\nکد: بببب'); pg.click('#jmk'); pg.wait_for_timeout(200); pg.screenshot(path=OUT+tag+'_teacher.png',full_page=True)
    print('LOG',log[:15]); print('ERR',errs[:8]); b.close()
