"""Focused route UI acceptance; additional routes exist only in the test fixture."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os, json
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'tests'/'shots';OUT.mkdir(exist_ok=True)
fixture=OUT/'harbor_selector_fixture.html'
fixture.write_text((ROOT/'jtest.html').read_text().replace('window.__J={harborCanPlay','window.__J={harborContent:HARBOR_CONTENT,harborCanPlay'))
profile={'id':'ui-test','name':'آزمایش','g':3,'t':0,'lvl':None,'coach':0,'sv':2,'S':{'prog':{},'ls':{},'cb':{},'nums':True,'forces':True,'formula':True,'track':'c'}}
metrics="""()=>{
 const box=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom}};
 const cards=[...document.querySelectorAll('[data-route]')];
 return cards.map(e=>({id:e.dataset.route,box:box(e),bg:getComputedStyle(e).backgroundColor,ink:getComputedStyle(e).color,
 pressed:e.getAttribute('aria-pressed'),parts:[...e.children].map(c=>({box:box(c),align:getComputedStyle(c).textAlign,ink:getComputedStyle(c).color,bg:getComputedStyle(c).backgroundColor,overflow:c.scrollWidth>c.clientWidth+1||c.scrollHeight>c.clientHeight+1}))}));
}"""
def rgb(s):return [float(n) for n in s[s.index('(')+1:s.index(')')].split(',')[:3]]
def luminance(v):
    vals=[x/255 for x in v];return sum((x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4)*w for x,w in zip(vals,[.2126,.7152,.0722]))
def contrast(a,b):
    x,y=sorted([luminance(a),luminance(b)]);return (y+.05)/(x+.05)
def check(pg):
    assert pg.evaluate('()=>document.documentElement.scrollWidth<=innerWidth'), 'page horizontal overflow'
    rows=pg.evaluate(metrics)
    for card in rows:
        assert card['box']['width']>=44 and card['box']['height']>=44
        assert contrast(rgb(card['bg']),rgb(card['ink']))>=4.5,(card['id'],'card text contrast')
        for part in card['parts']:
            b,c=part['box'],card['box'];assert not part['overflow'],(card['id'],'clipped role')
            vals=[float(n) for n in part['bg'][part['bg'].index('(')+1:part['bg'].index(')')].split(',')];alpha=vals[3] if len(vals)==4 else 1
            background=[alpha*x+(1-alpha)*y for x,y in zip(vals[:3],rgb(card['bg']))]
            assert contrast(rgb(part['ink']),background)>=4.5,(card['id'],'role text contrast')
            assert b['x']>=c['x']-1 and b['right']<=c['right']+1,(card['id'],'part outside card')
    for i,a in enumerate(rows):
        for b in rows[i+1:]:
            if abs(a['box']['y']-b['box']['y'])<2:
                for x,y in zip(a['parts'],b['parts']):assert abs(x['box']['y']-y['box']['y'])<2,'role alignment'
    assert pg.locator('.harbor-summary').evaluate_all("es=>es.every(e=>getComputedStyle(e).textAlign==='start'&&getComputedStyle(e).direction==='rtl')")
    assert pg.locator('.harbor-branches circle').count()==len(rows)+1,'branch destinations'
    assert pg.locator('[data-route] [id]').count()==0,'duplicate decorative IDs'
    return rows
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE') or None)
    for width in [320,390,1280]:
        pg=browser.new_page(viewport={'width':width,'height':900},reduced_motion='reduce');errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
        pg.goto(fixture.as_uri());pg.evaluate("p=>{localStorage.clear();localStorage.setItem('sm-journey-v1',JSON.stringify({profiles:[p],cur:p.id,week:null}))}",profile);pg.reload()
        pg.locator('[data-harbor]').click();pg.wait_for_selector('[data-route]');pg.wait_for_timeout(80);normal=check(pg)
        if width==390:assert abs(normal[0]['box']['y']-normal[1]['box']['y'])<2,'both choices should appear together'
        pg.screenshot(path=str(OUT/f'harbor_selector_{width}.png'))
        pg.keyboard.press('Tab');pg.keyboard.press('Shift+Tab');assert pg.locator('[data-route]').first.evaluate("e=>getComputedStyle(e).outlineStyle!=='none'")
        pg.evaluate("()=>{const p=__J.curP(),r=__J.harborRoute('harbor.fishing');__J.harborRecord(p,r.id,r.activities[0].id,{correct:true},false)}")
        pg.locator('[data-route="harbor.fishing"]').click()
        locked=pg.locator('[data-activity="2"]').locator('..').inner_text()
        assert 'مقایسهٔ دو آرایش' in locked and 'تغییر جهت کشیدن' not in locked,'lock lists only unmet goals'
        assert pg.locator('[data-activity="2"]').is_disabled()
        pg.evaluate('()=>__J.harborSelector()')
        pg.evaluate("()=>{const p=__J.curP(),r=__J.harborRoute('harbor.fishing');__J.harborState(p).routeId=r.id;for(const a of r.activities)__J.harborRecord(p,r.id,a.id,{correct:true},false);__J.harborSelector()}")
        pg.wait_for_timeout(80);check(pg)
        assert pg.locator('[aria-pressed="true"] .harbor-selection').inner_text()=='● راه انتخاب‌شده'
        assert 'فعالیت‌ها انجام شده‌اند' in pg.locator('[aria-pressed="true"] .harbor-completion').inner_text()
        pg.evaluate("""()=>{const es=[...document.querySelectorAll('.harbor-routes,.harbor-title,.harbor-difficulty,.harbor-summary,.harbor-selection,.harbor-completion,.harbor-card-action,.harbor-intro,.harbor-selector h2,.harbor-selector .chip-btn,.harbor-selector .j-note')];const sizes=es.map(e=>parseFloat(getComputedStyle(e).fontSize));es.forEach((e,i)=>e.style.fontSize=sizes[i]*2+'px')}""")
        pg.wait_for_timeout(80);check(pg);pg.screenshot(path=str(OUT/f'harbor_selector_{width}_text200.png'))
        pg.evaluate("""()=>{const c=__J.harborContent,base=c.routes[0];for(const [suffix,tier] of [['third','very-hard'],['fourth','unknown']])c.routes.push({...base,id:'harbor.'+suffix,title:'اسکلهٔ آزمایشی با عنوان بلند فارسی',difficulty:{...base.difficulty,tier},activities:base.activities.map((a,i)=>({...a,id:'harbor.'+suffix+'.'+i}))});c.routes.reverse();__J.harborSelector()}""")
        pg.wait_for_timeout(80);check(pg)
        assert pg.locator('[data-route="harbor.fishing"]').evaluate("e=>e.classList.contains('tier-core')")
        assert pg.locator('[data-route="harbor.third"]').evaluate("e=>e.classList.contains('tier-very-hard')")
        assert pg.locator('[data-route="harbor.fourth"]').evaluate("e=>e.classList.contains('tier-unknown')")
        assert not errors,errors
        pg.close()
    browser.close()
fixture.unlink()
print('harbor_selector: 320/390/1280, shared rows, RTL, 200% text, focus, separate states, contrast and four reordered routes passed')
