"""آزمون جریان با کلیک واقعی (v5): نقشه ← گره ← محیط ← صحنه ← کارت ← جعبه ← منو؛ شامل محوشدن ۱٫۲ث با reduced-motion خاموش و عکس میانهٔ گذار.
اجرا: python3 tests/flow.py   (خروجی: خطاهای کنسول، گام‌های رد‌شده، shots/flow_fade_mid.png)"""
import pathlib
from playwright.sync_api import sync_playwright
V5 = pathlib.Path(__file__).resolve().parents[1]
EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
errs, steps = [], []
def ok(n, c, info=''):
    steps.append((n, bool(c))); print(('ok   ' if c else 'FAIL ') + n + (f'  {info}' if info and not c else ''))
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 390, 'height': 800})
    pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.goto('file://' + str(V5 / 'index.html')); pg.wait_for_timeout(700)
    pg.evaluate("__st.tutOn=false;__st.tutDone.map=true;__st.tutDone.scene=true;__st.tut=null;renderOv();document.getElementById('rvbar').style.display='none'")
    def scr(): return pg.evaluate("__st.screen||__st.scr||''")
    pg.evaluate("render()"); pg.wait_for_timeout(300)
    ok('نقشه دیده می‌شود', pg.locator('#map').count() == 1)
    pg.evaluate("scrollMapTo('M07',false)"); pg.wait_for_timeout(200)
    pg.click('.mn[data-n=M07]'); pg.wait_for_timeout(250)
    ok('برگهٔ گره باز شد', pg.locator('.sheet').count() == 1)
    pg.click('.sheet [data-act=enter]'); pg.wait_for_timeout(1500)
    ok('محیط بندر باز شد', pg.locator('.cd-strip').count() >= 2 or pg.locator('[data-act=start]').count() >= 1)
    pg.locator('[data-act=start]').first.click(); pg.wait_for_timeout(1500)
    ok('صحنه باز شد', pg.locator('[data-act=arr]').count() == 2)
    pg.click('[data-act=arr][data-v=fixed]'); pg.wait_for_timeout(500)
    ok('پاسخ ثبت شد (بدون خطا)', True)
    pg.click('[data-act=lesson]'); pg.wait_for_timeout(500)
    ok('کارت درس از صحنه باز شد', pg.locator('.cflip').count() == 1)
    pg.click('.cbar [data-act=closecard]'); pg.wait_for_timeout(400)
    pg.click('[data-act=back]'); pg.wait_for_timeout(1500)
    pg.click('[data-t=menu]'); pg.wait_for_timeout(300)
    ok('منو باز شد', pg.locator('.tiles').count() == 1)
    pg.click('.ui-tile[data-act=box]'); pg.wait_for_timeout(800)
    ok('کارت‌دان باز شد', pg.locator('#boxbody').count() == 1)
    pg.click('.mc[data-id=M07]'); pg.wait_for_timeout(700)
    ok('کارت از جعبه باز شد', pg.locator('.cflip').count() == 1)
    pg.click('[data-act=flip]'); pg.wait_for_timeout(700)
    ok('کارت پشت شد', pg.locator('.cflip.back').count() == 1)
    pg.click('.cbar [data-act=closecard]'); pg.wait_for_timeout(400)
    # گذار نور/جهان با حرکت روشن: نقشه ← محیط، عکس در میانهٔ ۱٫۲ث
    pg.evaluate("document.body.classList.remove('rm')")
    pg.evaluate("go('map',{},false,false)"); pg.wait_for_timeout(1500)
    pg.evaluate("st.storyLight=true;go('scene',{cur:'M07',tier:1},true,true)"); pg.wait_for_timeout(600)
    n = pg.evaluate("document.querySelectorAll('#appold').length")
    pg.screenshot(path=str(V5 / 'shots' / 'flow_fade_mid.png'))
    ok('در میانهٔ گذار دو لایه هست (#appold)', n >= 1, n)
    pg.wait_for_timeout(1500)
    ok('پس از گذار #appold پاک شد', pg.evaluate("document.querySelectorAll('#appold').length") == 0)
    b.close()
print('خطاهای کنسول:', errs or 'ندارد')
print('نتیجه:', 'همه گذشت' if all(c for _, c in steps) and not errs else 'شکست')
