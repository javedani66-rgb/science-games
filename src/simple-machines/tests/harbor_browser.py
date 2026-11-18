"""Harbor entry on the map for every band (full play-through is in harbor_play.py)."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'tests'/'shots';OUT.mkdir(exist_ok=True)
def profile(g):return {'id':'hb%d'%g,'name':'آزمایش','g':g,'t':0,'lvl':None,'coach':0,'sv':2,'S':{'prog':{},'ls':{'c:force.2':2},'cb':{},'nums':True,'forces':True,'formula':True,'track':'abc'[0 if g<=1 else 1 if g==2 else 2]},'at':{'i':0,'j':1,'r':{'i':1,'res':[2],'specs':[{'t':'predict'}]}}}
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE') or None)
    for g,band in [(0,'1-2'),(1,'3-4'),(2,'3-4'),(3,'5-6'),(4,'5-6')]:
        for width in [390,1280]:
            pg=b.new_page(viewport={'width':width,'height':900},reduced_motion='reduce');errors=[]
            pg.on('pageerror',lambda e:errors.append(str(e)))
            pg.goto((ROOT/'jtest.html').as_uri())
            pg.evaluate("d=>{localStorage.clear();localStorage.setItem('sm-journey-v1',JSON.stringify({profiles:[d],cur:d.id,week:null}))}",profile(g));pg.reload()
            pg.wait_for_selector('[data-harbor]');assert pg.evaluate('()=>__J.harborBand(__J.curP())')==band
            legacy=pg.evaluate("()=>{const p=__J.curP();return JSON.stringify({S:p.S,at:p.at,code:__J.makeCode(p)})}")
            pg.locator('[data-harbor]').click();pg.wait_for_selector('[data-route]')
            assert pg.locator('[data-route]').count()==3,'three challenges are offered in every band'
            assert pg.evaluate('()=>document.documentElement.scrollWidth<=innerWidth'),'horizontal overflow'
            assert pg.evaluate("()=>document.querySelector('.harbor-selector').innerText.includes('شکار اژدر!')")
            assert pg.evaluate("()=>!/★|ستاره|امتیاز|[۰-۹]+ از [۰-۹]+/.test(document.querySelector('.harbor-selector').innerText)"),'no score text'
            assert pg.evaluate("()=>{const p=__J.curP();return JSON.stringify({S:p.S,at:p.at,code:__J.makeCode(p)})}")==legacy,'opening the harbor does not touch the legacy save or progress code'
            assert not errors,errors
            pg.close()
    # a grade outside the active list gets no harbor entry
    pg=b.new_page(viewport={'width':390,'height':900});pg.goto((ROOT/'jtest.html').as_uri())
    assert pg.evaluate("()=>[5,6,7,-1].every(g=>!__J.harborEligible({g}))")
    b.close()
print('harbor_browser: harbor offered for bands 1-2, 3-4 and 5-6 (grades 2 to 6), three challenges each, legacy save and progress code untouched')
