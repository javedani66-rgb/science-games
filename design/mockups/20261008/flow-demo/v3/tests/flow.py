"""آزمون جریان: کلیک‌های واقعی از نقشه تا کارت‌دان و برگشت؛ راهنما و «جای من»؛ قفل؛ جعبه؛ جستجو؛ کاهش حرکت."""
import pathlib, sys
from playwright.sync_api import sync_playwright
V3 = pathlib.Path(__file__).resolve().parents[1]; OUT = V3 / 'shots'
EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
fails = []; errs = []
def ok(c, m):
    if not c: fails.append(m)
    print(('PASS ' if c else 'FAIL ') + m)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=['--no-sandbox'])
    ctx = b.new_context(viewport={'width': 390, 'height': 800}, reduced_motion='no-preference')
    pg = ctx.new_page()
    pg.on('console', lambda m: errs.append(m.text) if m.type in ('error', 'warning') else None); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://' + str(V3 / 'index.html')); pg.wait_for_timeout(500)
    pg.evaluate("document.getElementById('rvbar').style.display='none'")
    # 1) آموزش خودکار نقشه شروع می‌شود و ردشدنی است
    pg.wait_for_timeout(1200)
    ok(pg.evaluate("!!__st.tut"), 'آموزش نقشه خودکار شروع شد')
    for _ in range(6):
        if pg.evaluate("!!__st.tut"):
            pg.click('#ov .coach button.btn--primary'); pg.wait_for_timeout(150)
    ok(pg.evaluate("!__st.tut"), 'آموزش با «بعدی/فهمیدم» تمام شد')
    # 2) «جای من»
    pg.evaluate("document.querySelector('#mapbody').scrollTop=0"); pg.wait_for_timeout(300)
    ok(pg.evaluate("!document.querySelector('#mebtn').classList.contains('off')"), '«جای من» وقتی راهنما بیرون است دیده می‌شود')
    pg.click('#mebtn'); pg.wait_for_timeout(1200)
    ok(pg.evaluate("document.querySelector('#mebtn').classList.contains('off')"), '«جای من» پس از رسیدن پنهان شد')
    # 3) گره قفل ← برگه ← ببرم‌ات آنجا
    pg.click('.node[data-n=M08]'); pg.wait_for_timeout(300)
    ok(pg.evaluate("document.querySelector('#ov .sheet')&&document.querySelector('#ov .chip--lock')"), 'لمس قفل برگهٔ دلیل را باز کرد')
    pg.click('#ov [data-act=lockgo]'); pg.wait_for_timeout(1000)
    ok(pg.evaluate("!document.querySelector('#ov .sheet')"), '«ببرم‌ات آنجا» برگه را بست')
    # 4) ورود: گره باز ← peek ← محیط ← کارت ← صحنه ← کارت درس
    pg.click('.node[data-n=M07]'); pg.wait_for_timeout(250); pg.click('#ov [data-act=enter]'); pg.wait_for_timeout(300)
    ok(pg.evaluate("__st.scr==='env'"), 'برویم به این محیط ← صفحهٔ محیط (ورود فقط با دکمه)')
    pg.click('.hc[data-p="2"]'); pg.wait_for_timeout(200); pg.click('#gobar'); pg.wait_for_timeout(300)
    ok(pg.evaluate("__st.scr==='scene'"), 'بزن بریم ← صحنه')
    pg.evaluate("__st.tutDone.scene=true;__st.tut=null;renderOv()")
    pg.click('[data-t=lesson]'); pg.wait_for_timeout(600)
    ok(pg.evaluate("!!document.querySelector('#cbig')"), 'کارت درس بزرگ شد')
    pg.click('#cbar [data-act=flip]') if False else pg.click('#flipbtn'); pg.wait_for_timeout(700)
    ok(pg.evaluate("__st.card.face==='back'"), 'پشت کارت')
    pg.click('.cbar [data-act=closecard]'); pg.wait_for_timeout(500)
    ok(pg.evaluate("!__st.card"), 'بستن کارت')
    # 5) کارت‌دان: «بذارش تو جعبه» توسط کودک؛ دیده‌ای ← توی جعبه
    pg.click('[data-t=menu]'); pg.wait_for_timeout(250); pg.click('.tile--cards'); pg.wait_for_timeout(300)
    ok(pg.evaluate("__st.scr==='box'"), 'منو ← کارت‌دان')
    ok(pg.evaluate("document.querySelectorAll('.pk').length")==33, 'سی‌وسه جای کارت (M12 موکول پنهان) دیده می‌شود')
    pg.click('.pk[data-pk=M07] .pocket'); pg.wait_for_timeout(600)
    ok(pg.evaluate("__st.seen.has('M07')"), 'باز کردن کارت = دیده‌ای')
    ok(pg.evaluate("!__st.coll.has('M07')"), 'جمع‌شدن خودکار نیست')
    pg.click('#flipbtn'); pg.wait_for_timeout(700); pg.click('[data-act=put]'); pg.wait_for_timeout(300)
    ok(pg.evaluate("__st.coll.has('M07')"), 'کودک «بذارش تو جعبه» زد ← جمع‌شده')
    pg.click('.cbar [data-act=closecard]'); pg.wait_for_timeout(500)
    ok(pg.evaluate("document.querySelector('.pk[data-pk=M07] .pocket').dataset.state==='collected'"), 'جیب M07 حالت جمع‌شده گرفت')
    # آیکون بازی روی کارت قفل نیست؛ روی باز هست
    ok(pg.evaluate("!document.querySelector('.pk[data-pk=M08] .pocket__game') && !!document.querySelector('.pk[data-pk=M07] .pocket__game')"), 'آیکون بازی فقط روی کارت‌های باز')
    # کارت قفل ← برگه ← نقشه
    pg.click('.pk[data-pk=M08] .pocket'); pg.wait_for_timeout(300)
    ok(pg.evaluate("!!document.querySelector('#ov .chip--lock')"), 'کارت قفل: برگهٔ دلیل')
    pg.click('#ov [data-act=lockgo]'); pg.wait_for_timeout(700)
    ok(pg.evaluate("__st.scr==='map'"), '«ببرم‌ات آنجا» از کارت‌دان به نقشه می‌رود')
    # 6) جستجو
    pg.evaluate("go('box',{},false)"); pg.wait_for_timeout(200); pg.click('[data-act=search]'); pg.fill('#q','قرقره'); pg.wait_for_timeout(300)
    n = pg.evaluate("document.querySelectorAll('.pk').length"); ok(1 <= n <= 4, f'جستجوی «قرقره» {n} کارت')
    # 7) پیشروی راهنما با انیمیشن (حرکت فعال)
    pg.evaluate("loadSample('mid');go('map',{},false)"); pg.wait_for_timeout(1200)
    pg.evaluate("advance()"); pg.wait_for_timeout(350); pg.screenshot(path=str(OUT / 'flow_advance_mid_anim.png')); pg.wait_for_timeout(1100)
    ok(pg.evaluate("__st.here!=='M07' && document.querySelector('.node[data-n=M07]').dataset.state==='done'"), 'راهنما به گرهٔ بعدی رفت و M07 «طی‌شده» شد')
    # 8) مه کنار می‌رود
    pg.evaluate("loadSample('end');go('map',{},false)"); pg.wait_for_timeout(500)
    ok(pg.evaluate("!!document.querySelector('[data-fog]')"), 'مه روی E04 است')
    pg.evaluate("st.fogClear=true;st.keepMap=true;render()"); pg.wait_for_timeout(300)
    ok(pg.evaluate("!document.querySelector('[data-fog]') && !document.querySelector('.fogsign')"), 'پس از کشف: مه و تابلو نیست')
    # 9) کاهش حرکت واقعی
    ctx2 = b.new_context(viewport={'width': 390, 'height': 800}, reduced_motion='reduce'); p2 = ctx2.new_page()
    p2.on('pageerror', lambda e: errs.append(str(e)))
    p2.goto('file://' + str(V3 / 'index.html')); p2.wait_for_timeout(900)
    ok(p2.evaluate("rm()"), 'prefers-reduced-motion شناسایی شد')
    ok(p2.evaluate("(()=>{const g=document.getElementById('guide');return !g||getComputedStyle(g).animationName==='none'})()"), 'کاهش حرکت: بدون انیمیشن روی راهنما')
    p2.evaluate("advance()"); p2.wait_for_timeout(300)
    ok(p2.evaluate("__st.scr==='map'"), 'کاهش حرکت: پیشروی بدون خطا')
    b.close()
print('ERRORS:', errs if errs else 'none'); print('FAILS:', fails if fails else 'none')
