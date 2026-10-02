# Primary-only public choices; preserve historical secondary profile/code indices.
from harness import *
JURL='file://'+D+'jtest.html'
with sync_playwright() as pw:
    b=pw.chromium.launch()
    pg=b.new_page(viewport={'width':400,'height':860})
    errors=[]
    pg.on('pageerror',lambda e:errors.append(str(e)))
    pg.goto(JURL)
    pg.locator('#jnm').fill('آزمایش')
    pg.locator('#jnx').click()
    pg.locator('[data-t="0"]').click()
    pg.locator('#jnx').click()
    assert pg.locator('[data-g]').count()==5
    assert not pg.locator('[data-g="5"], [data-g="6"], [data-g="7"]').count()
    pg.screenshot(path='/tmp/primary-grade-mobile.png')
    assert pg.evaluate('document.documentElement.scrollWidth<=innerWidth')
    pg.locator('[data-g="4"]').click()
    pg.locator('#jnx').click()
    pg.evaluate('''()=>{const p=__J.curP();p.coach=0;p.done="abc";p.quiz=[1,1,1,1,1];p.S.ls={};for(let i=0;i<12;i++)for(const id of __J.missions(p,i))p.S.ls["c:"+id]=3;__J.save();}''')
    pg.reload()
    pg.locator('#jgo').click()
    assert pg.locator('#jok').count()==1
    assert pg.locator('#jup').count()==0 # completed c never promotes to d
    # Capture the settled sheet, rather than the existing 200ms fade-in.
    pg.locator('.ovl').evaluate_all('els=>els.forEach(el=>el.getAnimations().forEach(a=>a.finish()))')
    pg.screenshot(path='/tmp/primary-finish-mobile.png')
    assert pg.evaluate('document.documentElement.scrollWidth<=innerWidth')
    pg.evaluate('__J.closeOv();__J.adults()')
    assert pg.locator('[data-g]').count()==5
    assert pg.locator('[data-lv="d"]').count()==0
    assert pg.locator('[data-lv]').count()==3
    # Real legacy saves retain all three historical grades, data and code identities.
    for g in [5,6,7]:
        pg.evaluate('''g=>{const p=__J.curP();p.g=g;p.lvl=null;p.S.track="d";p.S.ls={"d:force.2":2};p.done="abcd";p.quiz=[1,0,0,0,0];p.quizEvidence={d:{0:{first:{complete:true,total:1,items:[{id:"old",first:false,corrected:true}]}}}};p.stash.d={words:[1],quiz:[1],side:[1]};__J.save();}''',g)
        pg.reload()
        r=pg.evaluate('''()=>{const p=__J.curP(),code=__J.makeCode(p),r=__J.readCode(code);return {g:p.g,tr:__J.trk(p),g2:r.g,tr2:r.lvl,star:p.S.ls["d:force.2"],evidence:p.quizEvidence.d[0].first.items[0],done:p.done};}''')
        assert r['g']==g and r['g2']==g and r['tr']==r['tr2']=='d'
        assert r['star']==2 and r['done']=='abcd' and r['evidence']['corrected']
        pg.evaluate('__J.adults()')
        assert 'نسخهٔ قبلی' in pg.locator('#app').inner_text()
        assert pg.locator('[data-g]').count()==5 and pg.locator('[data-lv="d"]').count()==0
        pg.locator('[data-g="4"]').click()
        pg.locator('#jgy').click()
        r=pg.evaluate('''()=>{const p=__J.curP();return {g:p.g,tr:__J.trk(p),star:p.S.ls["d:force.2"],evidence:p.quizEvidence.d[0].first.items[0],stash:p.stash.d.quiz};}''')
        assert r['g']==4 and r['tr']=='c' and r['star']==2 and r['stash'][0]==1 and r['evidence']['corrected']
    pg.goto('file://'+D+'test.html')
    pg.locator('#tk').click() if not pg.locator('[data-t="a"]').count() else None
    assert pg.locator('.trk').count()==3 and pg.locator('.trk[data-t="d"]').count()==0
    assert not errors,errors
    b.close()
print('primaryonly: primary choices, c finish, historical 7/8/9 saves/codes/evidence, explicit migration and station choices passed')
