"""عکس چند فریم و اندازهٔ مدت‌ها برای motion_demo.html. اجرا: python3 tests/motion_shots.py"""
import pathlib, json
from playwright.sync_api import sync_playwright
V5 = pathlib.Path(__file__).resolve().parents[1]; OUT = V5 / 'shots'; OUT.mkdir(exist_ok=True)
EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
errs = []; rep = {}
SEEK = "(t)=>{document.getAnimations().forEach(a=>{a.pause();a.currentTime=t})}"
STATS = """()=>{const A=document.getAnimations();let end=0;const props=new Set();let inf=false;
 A.forEach(a=>{const ct=a.effect.getComputedTiming();end=Math.max(end,ct.endTime);if(ct.iterations===Infinity)inf=true;if(a.transitionProperty)props.add(a.transitionProperty);else props.add('anim:'+a.animationName)});
 return {n:A.length,end,props:[...props],inf}}"""
def run(w, h):
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=['--no-sandbox'])
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg.on('console', lambda m: errs.append((w, m.type, m.text)) if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: errs.append((w, 'pageerror', str(e))))
        pg.goto('file://' + str(V5 / 'motion_demo.html?dev=0')); pg.wait_for_timeout(500)
        ph = pg.locator('#phone')
        def shot(name):
            ph.screenshot(path=str(OUT / f'motion_{w}x{h}_{name}.png'))
        def flush(): pg.evaluate("document.body.offsetWidth")
        def frames(tag, times):
            for t in times:
                pg.evaluate(SEEK, t); pg.wait_for_timeout(60); shot(f'{tag}_{t:04d}')
        def finish():
            pg.evaluate("document.getAnimations().forEach(a=>a.finish())"); pg.wait_for_timeout(100)
        def stats(key):
            flush(); rep.setdefault(w, {})[key] = pg.evaluate(STATS)
        shot('00_map')
        # باز شدن برگه
        pg.evaluate("__m.openSheet()"); flush(); stats('sheet_open'); frames('01_sheet', [0, 125, 250]); finish()
        # ورود به محیط
        pg.evaluate("__m.enter()"); flush(); stats('enter')
        frames('02_light', [0, 300, 600, 900, 1200, 1400]); finish()
        shot('03_env_front')
        # انتخاب کارت پشتی (نوار دوم = نارنجی)
        pg.evaluate("__m.pick(1)"); flush(); stats('pick_slot1')
        frames('04_pick1', [0, 60, 120, 200, 280]); finish()
        # انتخاب کارت قرمز از جای سوم
        pg.evaluate("__m.pick(2)"); flush(); stats('pick_slot2')
        frames('05_pick2', [0, 60, 120, 200, 280]); finish()
        # برگشت: لمس نوار کارت قبلی
        pg.evaluate("__m.pick(1)"); flush(); stats('return'); frames('06_return', [0, 100, 200, 280]); finish()
        # لمس واقعی با ماوس روی نوار
        pg.evaluate("__m.reset()"); pg.wait_for_timeout(50); pg.evaluate("__m.enter()"); pg.wait_for_timeout(1500)
        pg.locator('.ch[data-slot="2"] .fs').click(); flush(); stats('click_real'); finish()
        rep[w]['order_after_click'] = pg.evaluate("__m.order")
        # خروج
        pg.locator('#tomap').click(); flush(); stats('leave'); frames('07_leave', [0, 300, 600, 900, 1200]); finish()
        # کاهش حرکت
        pg.evaluate("__m.reset()"); pg.evaluate("document.getElementById('phone').classList.add('rm')"); pg.wait_for_timeout(50)
        pg.evaluate("__m.openSheet()"); pg.evaluate("__m.enter()"); flush(); stats('rm_enter'); shot('08_rm_env')
        pg.evaluate("__m.pick(1)"); flush(); stats('rm_pick'); shot('09_rm_pick')
        rep[w]['hscroll'] = pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth")
        # ضریب ۱۵۰ms
        pg.evaluate("__m.reset()"); pg.evaluate("document.getElementById('phone').classList.remove('rm')"); pg.evaluate("document.getElementById('phone').style.setProperty('--k',.535)")
        pg.evaluate("__m.enter()"); pg.wait_for_timeout(1500); pg.evaluate("__m.pick(2)"); flush(); stats('fast_pick')
        b.close()
for w, h in ((390, 800), (360, 640)): run(w, h)
print(json.dumps(rep, ensure_ascii=False, indent=1)); print('ERRS', errs)
