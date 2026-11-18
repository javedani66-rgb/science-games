"""Plays every harbor mission (green, orange, red) for each band as a child would, through the real UI.
Checks: one single answer per question (model), nothing shown as stars/points/'n of m', text overlap/clipping in the scene (same
detector as ov.py), the scored question gives two chances then the cause, text comes from the string bank, saved state survives reload.
No claim about how children understand it (B9): this is a mechanical check only."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os, re, sys
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'tests' / 'shots'; OUT.mkdir(exist_ok=True)
CHK = re.search(r'CHK=r"""(.*?)"""', (ROOT / 'tests' / 'ov.py').read_text(encoding='utf-8'), re.S).group(1)
BANDS = {'1-2': 0, '3-4': 1, '5-6': 3}   # band -> grade index (دوم, سوم, پنجم)
BAD_TEXT = re.compile(r'★|⭐|امتیاز|ستاره|[۰-۹]+\s*از\s*[۰-۹]+')
problems = []; seen_over = set()

def profile(g):
    return {'id': 'hp%d' % g, 'name': 'آزمایش', 'g': g, 't': 0, 'lvl': None, 'coach': 0, 'sv': 2,
            'S': {'prog': {}, 'ls': {}, 'cb': {}, 'nums': True, 'forces': True, 'formula': True, 'track': 'abc'[0 if g <= 1 else 1 if g == 2 else 2]}}

def sh(pg, name):
    try: pg.screenshot(path=str(OUT / (name + '.png')))
    except Exception: pass

def scan(pg, where):
    txt = pg.evaluate("()=>document.querySelector('#app').innerText")
    m = BAD_TEXT.search(txt)
    if m: problems.append(f'{where}: child-visible score text "{m.group(0)}"')
    try: r = pg.evaluate(CHK)
    except Exception as e: r = ['ERR ' + str(e)[:60]]
    for x in r:
        key = where.split()[0] + ' ' + x
        if key not in seen_over: seen_over.add(key); problems.append(f'{where}: overlap {x}')

def pull(pg, times=1):
    for _ in range(times):
        pg.locator('[data-drag="grip"]').focus(); pg.keyboard.press('ArrowDown')

def finished(pg): return pg.locator('#nv .btn').count() > 0

def pull_until(pg, cond, limit=24):
    for _ in range(limit):
        if cond(): return True
        pull(pg)
    return cond()

def guess(pg):
    pg.locator('.mcq [data-i="0"]').click()

def arr(pg, k):   # arrangement button k (0-based) among the control buttons
    pg.locator('#cl .btn').nth(k).click()

def run_mission(pg, band, route, idx, tag, two_wrong=False):
    sp = pg.evaluate('()=>window.__T.spec')
    t = sp['t']
    scan(pg, f'{tag} start')
    guess(pg)
    scan(pg, f'{tag} after guess')
    if t == 'harborLift':
        pull_until(pg, lambda: finished(pg) or pg.locator('.mcq').count() > 0)
    elif t == 'harborTry':
        pull(pg); assert finished(pg), tag + ': observation mission must end after the blocked try'
    elif t == 'harborHelpers':
        pull(pg); assert not finished(pg), tag + ': pulling before the helper must be free and not end the mission'
        scan(pg, f'{tag} blocked')
        pg.locator('#cl .btn.go').click(); pull_until(pg, lambda: finished(pg))
    elif t == 'harborPick':
        best = sp['best']; wrong = [k for k in sp['opts'] if k != best]
        for k in wrong:
            arr(pg, sp['opts'].index(k)); pull(pg, 8); assert not finished(pg), f'{tag}: wrong arrangement {k} must not finish'
            scan(pg, f'{tag} wrong n={k}')
        arr(pg, sp['opts'].index(best)); pull_until(pg, lambda: finished(pg) or pg.locator('.mcq').count() > 0)
    elif t == 'harborCoils':
        for k in sp['opts']:
            arr(pg, sp['opts'].index(k)); pull_until(pg, lambda: finished(pg) or pg.locator('.cc svg').count() > 0, 30)
    elif t == 'harborPlan':
        b1, b2 = sp['best']
        # wrong first, then restart (free), then the right plan
        arr(pg, sp['opts'].index(2)); pull_until(pg, lambda: pg.locator('#fb').inner_text().startswith(''), 10)
        pull(pg, 12)
        scan(pg, f'{tag} plan wrong')
        pg.get_by_role('button', name='از اول', exact=True).click()
        arr(pg, sp['opts'].index(b1)); pull_until(pg, lambda: 'قفس' in pg.locator('#fb').inner_text() or pg.locator('.mcq').count() > 0, 12)
        arr(pg, sp['opts'].index(b2)); pull_until(pg, lambda: pg.locator('.mcq').count() > 0, 30)
    else:
        raise AssertionError('unknown type ' + t)
    scan(pg, f'{tag} lifted')
    if sp.get('q'):
        q = sp['q']; right = q['answer']
        assert pg.locator('.mcq .btn').count() == q['n'], f'{tag}: option count'
        wrong = (right + 1) % q['n']
        pg.locator(f'.mcq [data-i="{wrong}"]').click()
        assert not finished(pg), f'{tag}: first wrong answer must leave a second chance'
        scan(pg, f'{tag} after wrong')
        if two_wrong and q['n'] >= 3:
            pg.locator(f'.mcq [data-i="{(right + 2) % q["n"]}"]').click()
            assert finished(pg), f'{tag}: second wrong answer ends the question'
            assert pg.locator('.mcq .btn.right').count() == 1, f'{tag}: the right option is shown after two wrong answers'
            cause = pg.evaluate("([c,b])=>__J.hs('harbor.'+c+'.q.explain',b)", [sp['color'], band])
            assert cause in pg.locator('#fb').inner_text(), f'{tag}: the cause is shown after two wrong answers'
            return
        pg.locator(f'.mcq [data-i="{right}"]').click()
    assert finished(pg), f'{tag}: mission did not finish'
    scan(pg, f'{tag} done')

def run_band(pw_browser, band, g, width):
    pg = pw_browser.new_page(viewport={'width': width, 'height': 900}, reduced_motion='reduce')
    errors = []; pg.on('pageerror', lambda e: errors.append(str(e)))
    pg.goto((ROOT / 'jtest.html').as_uri())
    pg.evaluate("d=>{localStorage.clear();localStorage.setItem('sm-journey-v1',JSON.stringify({profiles:[d],cur:d.id,week:null}))}", profile(g)); pg.reload()
    pg.wait_for_selector('[data-harbor]')
    assert pg.evaluate('()=>__J.harborBand(__J.curP())') == band
    legacy = pg.evaluate("()=>{const p=__J.curP();return JSON.stringify({S:p.S,at:p.at,code:__J.makeCode(p)})}")
    for ri, rid in enumerate(['harbor.fishing', 'harbor.pirate', 'harbor.dragon']):
        for mi in range(3):
            tag = f'{band} {rid} m{mi+1} w{width}'
            pg.evaluate('()=>__J.harborSelector()')
            pg.locator(f'[data-route="{rid}"]').click()
            if mi > 0:
                assert pg.locator(f'[data-activity="{mi}"]').is_enabled(), tag + ': mission should be open after the previous one'
            else:
                assert pg.locator('[data-activity="1"]').is_disabled(), tag + ': mission 2 locked until mission 1'
            pg.locator(f'[data-activity="{mi}"]').click()
            pg.wait_for_selector('[data-drag="grip"]')
            if width == 390 and mi == 0: sh(pg, f'harbor_{band}_{rid.split(".")[1]}_m1')
            run_mission(pg, band, rid, mi, tag)
            rec = pg.evaluate("([rid,i])=>{const r=__J.harborRoute(rid),a=r.activities[i];return __J.harborState(__J.curP()).activities[a.id].latest}", [rid, mi])
            assert rec['correct'], tag + ': mission recorded as done'
            if not pg.evaluate('()=>!!window.__T.spec.q'): assert rec['independent'], tag + ': blocked tries cost nothing (A8): still independent'
            if width == 390 and mi == 2: sh(pg, f'harbor_{band}_{rid.split(".")[1]}_m3')
            if rid == 'harbor.fishing' and mi == 2:
                # lesson card after green (B15/B16): only the direction of pull; it must not give the orange/red answers
                assert pg.evaluate("()=>!(__J.curP().cards||[]).includes('harbor.card.pull')"), tag + ': card not yet taken'
                pg.locator('#nv .btn.go').click()
                pg.wait_for_selector('#hcardgo')
                ctext = pg.locator('.j-sheet').inner_text()
                for bad in ['متحرک', 'نیروی لازم', 'کم نمی', 'نصف', 'ستاره', 'امتیاز']:
                    assert bad not in ctext, f'{tag}: lesson card must not contain "{bad}"'
                assert 'جهت کشیدن' in ctext, tag + ': lesson card is about the direction of pull'
                assert pg.evaluate("()=>document.documentElement.scrollWidth<=innerWidth"), tag + ': card overflow'
                pg.locator('#hcardgo').click()
                pg.wait_for_selector('#hother')
                assert pg.evaluate("()=>(__J.curP().cards||[]).includes('harbor.card.pull')"), tag + ': card saved in the card box'
                pg.locator('#hmap').click()
                pg.evaluate("()=>__J.backpack('w')")
                assert 'جهت کشیدن' in pg.locator('#app').inner_text(), tag + ': card is listed in the backpack word notebook'
        pg.evaluate('()=>__J.harborSelector()')
        assert pg.evaluate("rid=>__J.harborRouteDone(__J.curP(),__J.harborRoute(rid))", rid), f'{band} {rid}: route should be done'
    # two wrong answers end the scored question with the cause shown; 'show me' after three blocked tries (replays do not change the record)
    for rid in ['harbor.fishing', 'harbor.pirate', 'harbor.dragon']:
        tag = f'{band} {rid} two-wrong'
        pg.evaluate("rid=>__J.harborPlay(rid,2,null,true)", rid); pg.wait_for_selector('[data-drag="grip"]')
        run_mission(pg, band, rid, 2, tag, two_wrong=True)
    pg.evaluate("([i])=>__J.harborPlay('harbor.dragon',i,null,true)", [0 if band == '1-2' else 1]); pg.wait_for_selector('[data-drag="grip"]')
    guess(pg); arr(pg, 0)
    for _ in range(3): pull(pg, 2)
    assert pg.locator('[data-show]').count() == 1, band + ': show-me appears after three blocked tries'
    pg.locator('[data-show]').click(); assert finished(pg), band + ': show-me ends the mission'
    # selector shows marks, no counts of the "n of m" kind
    pg.evaluate('()=>__J.harborSelector()'); scan(pg, f'{band} selector')
    # 'n of m' only on the teacher page, never for the child
    pg.evaluate('()=>__J.teacherPage()')
    ttxt = pg.locator('#app').inner_text()
    assert len(re.findall(r'۳ از ۳ مأموریت', ttxt)) == 3, f'{band}: teacher page shows n of m for the three challenges'
    pg.evaluate('()=>__J.harborSelector()')
    mm = re.search(r'.{0,30}[۰-۹]+\s*از\s*[۰-۹]+.{0,20}', pg.locator('.sheet').first.inner_text(), re.S)
    assert not mm, f'{band}: child must not see n of m: {mm and mm.group(0)!r}'
    assert pg.evaluate("()=>document.documentElement.scrollWidth<=innerWidth"), f'{band} w{width}: horizontal overflow'
    saved = pg.evaluate('()=>JSON.stringify(__J.curP().routeProgress)'); pg.reload()
    assert pg.evaluate('()=>JSON.stringify(__J.curP().routeProgress)') == saved, 'reload keeps harbor progress'
    assert pg.evaluate("()=>{const p=__J.curP();return JSON.stringify({S:p.S,at:p.at,code:__J.makeCode(p)})}") == legacy, 'harbor must not touch legacy save or progress code'
    assert not errors, errors
    pg.close()

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE') or None)
    for band, g in BANDS.items():
        for width in ([390, 1280] if band == '5-6' else [390]):
            try: run_band(b, band, g, width)
            except Exception as e: problems.append(f'{band} w{width}: EXC {type(e).__name__}: {str(e)[:300]}')
    b.close()
for p in problems: print('PROBLEM', p)
if problems: sys.exit(1)
print('harbor_play: 3 bands x 3 challenges x 3 missions played; one answer, two chances, no score text, no overlap, reload and legacy save intact')
