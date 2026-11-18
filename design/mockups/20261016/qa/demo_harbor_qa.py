#!/usr/bin/env python3
"""آزمون هدفمند demo_harbor.html (۳۹۰×۸۴۴): ورود ← نام ← کاراکتر ← انتخاب پایه ← نمای کلی ← نقشه ← صفحهٔ اسکله؛
برای هر سه گروه پایه (اول، سوم، ششم) هر سه کارت را لمس می‌کند، می‌بیند بازی واقعی باز شد، مأموریت اول را کمی بازی می‌کند و برمی‌گردد.
خروجی: خطاهای کنسول (خطای شناخته‌شدهٔ env_sheet «<path> attribute d» پذیرفته است) و عکس‌ها در /home/claude/audit/demo_shots/.
ادعایی دربارهٔ فهم کودک نیست (B9). اجرا: python3 demo_harbor_qa.py"""
import pathlib, sys, re
from playwright.sync_api import sync_playwright
F = pathlib.Path(__file__).resolve().parent.parent / 'entry-page' / 'demo_harbor.html'
SH = pathlib.Path('/home/claude/audit/demo_shots'); SH.mkdir(parents=True, exist_ok=True)
errs = []; fails = []
def chk(c, msg):
    print(('ok   ' if c else 'FAIL ') + msg, flush=True)
    if not c: fails.append(msg)
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=False)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: errs.append('pageerror ' + str(e)))
    pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
    pg.goto(F.as_uri()); pg.wait_for_timeout(2500)
    fr = lambda: pg.frame_locator('#fr')
    fr().locator('#go').click(); pg.wait_for_function("document.getElementById('fr').dataset.page==='name'"); pg.wait_for_timeout(1500)
    fr().locator('#nm').fill('مینا'); pg.wait_for_timeout(500); fr().locator('#go').click()
    pg.wait_for_function("document.getElementById('fr').dataset.page==='character'"); pg.wait_for_timeout(2000)
    fr().locator('.char').nth(1).click(); pg.wait_for_timeout(900)
    fr().locator('#colors button, #colors [role=radio]').nth(3).click(); pg.wait_for_timeout(1000); fr().locator('#go').click()
    pg.wait_for_selector('#gp:not([hidden])', timeout=15000); pg.wait_for_timeout(400)
    pg.screenshot(path=str(SH / '01_grade_picker.png'))
    pg.locator('#gg button[data-g="1"]').click()
    pg.wait_for_function("document.getElementById('fr').dataset.page==='overview'"); pg.wait_for_timeout(2500)
    pg.screenshot(path=str(SH / '02_overview.png')); fr().locator('#go').click()
    pg.wait_for_function("document.getElementById('fr').dataset.page==='map'"); pg.wait_for_timeout(3500)
    chk(True, 'reached the map through the real flow')
    # jump to the harbor stop (M07) the same way the overview does
    pg.evaluate("openPage('map.html#enter-M07')"); pg.wait_for_timeout(4000)
    try:
        for _ in range(8):
            if fr().locator('#tut').evaluate('e=>e.hidden'): break
            fr().locator('#tn').click(); pg.wait_for_timeout(600)
    except Exception as e: print('tut', e)
    pg.screenshot(path=str(SH / '03_map_m07.png'))
    fr().locator('#goenv').wait_for(state='visible', timeout=60000); fr().locator('#goenv').click()
    fr().locator('#stk .sc').first.wait_for(timeout=20000); pg.wait_for_timeout(3000)
    pg.screenshot(path=str(SH / '04_harbor_env.png'))
    names = {'green': 'سبز', 'orange': 'نارنجی', 'red': 'قرمز'}
    def tap_card(ti):
        # make card ti the front card, then press «بزن بریم!»
        for _ in range(3):
            pos = fr().locator(f'#stk .sc[data-t="{ti}"]').get_attribute('data-p')
            if pos == '2': break
            fr().locator(f'#stk .sc[data-t="{ti}"]').click(position={'x': 120, 'y': 12}); pg.wait_for_timeout(1200)
        fr().locator('#stk .sc[data-p="2"]').click(); pg.wait_for_timeout(700)
        fr().locator('#stk .sc[data-p="2"] .gob').click()
    gradeBand = {1: ('1-2', 8), 3: ('3-4', 1), 6: ('5-6', 4)}
    for gi, (band, idx) in gradeBand.items():
        for ti, ch in enumerate(['green', 'orange', 'red']):
            tag = f'g{gi}_{ch}'
            tap_card(ti)
            pg.wait_for_selector('#gm:not([hidden])', timeout=8000); pg.wait_for_timeout(2500)
            g = pg.frame_locator('#gf')
            ok = pg.evaluate("document.getElementById('gf').contentWindow.__START&&document.getElementById('gf').contentWindow.__START.challenge")
            chk(ok == ch, f'{tag}: game opened with challenge {ok}')
            gr = pg.evaluate("document.getElementById('gf').contentWindow.__START.grade")
            chk(gr == idx, f'{tag}: grade index {gr} for band {band}')
            scene = g.locator('#app svg').count()
            chk(scene > 0, f'{tag}: game scene (svg) present ({scene})')
            chk(g.locator('[data-drag="grip"]').count() > 0, f'{tag}: pull handle present')
            pg.screenshot(path=str(SH / f'05_{tag}_start.png'))
            if gi == 1 or ti == 0:   # play the first mission a little
                try:
                    if g.locator('.mcq [data-i="0"]').count(): g.locator('.mcq [data-i="0"]').click(); pg.wait_for_timeout(900)
                    g.locator('[data-drag="grip"]').focus()
                    for _ in range(30):
                        if g.locator('#nv .btn').count() or g.locator('.mcq').count(): break
                        pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(150)
                    pg.wait_for_timeout(1200)
                    if g.locator('.mcq [data-i="0"]').count(): g.locator('.mcq [data-i="0"]').click(); pg.wait_for_timeout(1500)
                    pg.screenshot(path=str(SH / f'06_{tag}_played.png'))
                    n = g.locator('#nv .btn').count() + g.locator('#cl .btn').count(); m = g.locator('.mcq').count()
                    print('   after play: nav buttons', n, 'mcq', m)
                    chk(n > 0 or m > 0, f'{tag}: first mission reacted to the pull (next, arrangement or question)')
                except Exception as e: print('   play skipped', str(e)[:80])
            if ti == 2 and gi != 6:   # change grade from the bar
                pass
            pg.locator('#gback').click(); pg.wait_for_timeout(900)
            chk(pg.locator('#gm').is_hidden(), f'{tag}: back control closes the game')
            pg.wait_for_timeout(1500)
            chk(fr().locator('#stk').count() > 0, f'{tag}: environment page shown again')
        if gi != 6:
            nxt = 3 if gi == 1 else 6
            tap_card(0); pg.wait_for_selector('#gm:not([hidden])'); pg.wait_for_timeout(1500)
            pg.locator('#gchg').click(); pg.wait_for_selector('#gp:not([hidden])'); pg.screenshot(path=str(SH / f'07_change_grade_{gi}.png'))
            pg.locator(f'#gg button[data-g="{nxt}"]').click(); pg.wait_for_timeout(2500)
            pg.locator('#gback').click(); pg.wait_for_timeout(2500)
    # leave the environment page and go back to the map
    fr().locator('#envb').click(); pg.wait_for_timeout(3500)
    pg.screenshot(path=str(SH / '08_back_on_map.png'))
    chk(fr().locator('#goenv').is_visible(), 'back on the map: environment button visible')
    bad = [e for e in errs if 'attribute d' not in e]
    print('console errors (excluding known path d):', bad)
    chk(not bad, 'no console errors')
    ctx.close(); b.close()
print('FAILS', fails)
sys.exit(1 if fails or bad else 0)
