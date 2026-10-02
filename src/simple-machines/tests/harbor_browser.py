"""Bounded H1 browser check; no publication or whole-game release claim."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json, os
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'tests'/'shots';OUT.mkdir(exist_ok=True)
profile={'id':'harbor-test','name':'آزمایش','g':3,'t':0,'lvl':None,'coach':0,'sv':2,'S':{'prog':{},'ls':{'c:force.2':2},'cb':{},'nums':True,'forces':True,'formula':True,'track':'c'},'at':{'i':0,'j':1,'r':{'i':1,'res':[2],'specs':[{'t':'predict'}]}}}
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE') or None)
    for width in [390,1280]:
        pg=b.new_page(viewport={'width':width,'height':900},reduced_motion='reduce');errors=[]
        pg.on('pageerror',lambda e:errors.append(str(e)))
        pg.goto((ROOT/'jtest.html').as_uri())
        pg.evaluate("d=>{localStorage.clear();localStorage.setItem('sm-journey-v1',JSON.stringify({profiles:[d],cur:d.id,week:null}))}",profile);pg.reload()
        pg.wait_for_selector('[data-harbor]');legacy=pg.evaluate("()=>{const p=__J.curP();return JSON.stringify({S:p.S,at:p.at,code:__J.makeCode(p),quiz:p.quiz,stash:p.stash})}")
        pg.locator('[data-harbor]').click();pg.wait_for_selector('[data-route]')
        assert pg.locator('[data-route]').count()==2
        assert pg.evaluate('()=>document.documentElement.scrollWidth<=innerWidth'), 'horizontal overflow'
        pg.screenshot(path=str(OUT/f'harbor_routes_{width}.png'))
        for rid in ['harbor.fishing','harbor.pirate']:
            pg.evaluate('()=>__J.harborSelector()');pg.locator(f'[data-route="{rid}"]').click()
            if rid.endswith('fishing'):assert pg.locator('[data-activity="1"]').is_disabled()
            pg.locator('[data-activity="0"]').click();pg.get_by_role('button',name='آزمایش را ببین',exact=True).click()
            pg.locator('.mcq [data-i="1"]').click();pg.wait_for_selector('#nv .next')
            # Same-spec replay cannot improve or change the original run.
            first=pg.evaluate('()=>JSON.stringify(__J.harborState(__J.curP()).activities)')
            pg.get_by_role('button',name='بیا یک بار دیگر انجامش بدهیم',exact=True).click()
            pg.get_by_role('button',name='آزمایش را ببین',exact=True).click();pg.locator('.mcq [data-i="1"]').click()
            assert pg.evaluate('()=>Object.values(__J.harborState(__J.curP()).activities)[0].runs')==1
            pg.get_by_role('button',name='فعالیت بعد',exact=True).click()
            def pull():
                grip=pg.locator('[data-drag="grip"]');grip.focus();pg.keyboard.press('ArrowDown')
            pull();assert pg.locator('.mcq').count()==0
            pg.get_by_role('button',name='ثابت و متحرک',exact=True).click()
            for _ in range(4):pull()
            pg.wait_for_selector('.mcq');assert pg.locator('#fm').inner_text()==''
            assert not any(ch.isdigit() for ch in pg.locator('#sc').text_content()), 'numeric scene leaked'
            pg.screenshot(path=str(OUT/f'harbor_compare_{width}_{rid.split(".")[1]}.png'))
            pg.locator(f'.mcq [data-i="{0 if rid.endswith("pirate") else 1}"]').click()
            pg.get_by_role('button',name='فعالیت بعد',exact=True).click()
            if rid.endswith('pirate'):
                pull();assert pg.locator('.mcq').count()==0
                pg.get_by_role('button',name='ثابت و متحرک',exact=True).click()
                for _ in range(4):pull()
                answer=1
            else:
                for _ in range(2):pull()
                answer=0
            pg.wait_for_selector('.mcq');pg.locator(f'.mcq [data-i="{answer}"]').click()
            pg.get_by_role('button',name='دیدن نتیجهٔ راه',exact=True).click()
            assert pg.get_by_text('فعالیت‌های این راه انجام شد',exact=True).is_visible()
            assert pg.evaluate('()=>{const p=__J.curP();return JSON.stringify({S:p.S,at:p.at,code:__J.makeCode(p),quiz:p.quiz,stash:p.stash})}')==legacy
        saved=pg.evaluate('()=>JSON.stringify(__J.curP().routeProgress)');pg.reload();assert pg.evaluate('()=>JSON.stringify(__J.curP().routeProgress)')==saved
        assert not errors,errors
        pg.close()
    b.close()
print('harbor_browser: two routes, gated observations/prerequisites, replay isolation, reload, legacy save/code and 390/1280 layout passed')
