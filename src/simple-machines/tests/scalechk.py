"""Scale learning/interaction regressions. Run after build.py; fail on an assertion.

Checks observed evidence, fair exploration, optimization, solution guidance,
keyboard-only manipulation, hidden totals and stable progress topology.
"""
from t2 import *


def seed(pg, track):
    pg.goto(TURL)
    pg.evaluate("p=>localStorage.setItem('sm-workshop-v3',JSON.stringify(p))", {
        'prog': {f'{track}:scale': {'lv': [3] * 5, 'best': 0}},
        'nums': True, 'forces': True, 'formula': False, 'track': track})
    pg.reload()
    pg.click('.st[data-k=scale]')


def next_to(pg, g, kind):
    for _ in range(30):
        if spec(pg)['spec']['t'] == kind:
            return
        scale(g, pg, spec(pg)['spec'])
        pg.locator('#nv .next').click()
    raise AssertionError(f'no {kind} in this level')


def put(pg, v):
    pg.locator(f'[data-focus="weight-{v}"]').focus()
    pg.keyboard.press('Enter')
    pg.locator('[data-focus="pan-R"]').focus()
    pg.keyboard.press('Space')
    pg.wait_for_timeout(680)


with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
    errors = []
    pg.on('pageerror', lambda e: errors.append(str(e)))
    g = G(pg)
    # Direct manipulation can be completed without dragging; wrong prediction is free.
    for track in ('a', 'b', 'c', 'd'):
        seed(pg, track)
        pg.click('[data-l="1"]')
        pg.wait_for_timeout(100)
        sp = spec(pg)['spec']
        assert sp['t'] == 'heavier'
        assert pg.locator('#sc image').count() >= 4
        assert pg.locator('[data-drag="tray"]').count() == 2
        assert pg.locator('[data-focus]').count() == 0, 'prediction phase is frozen'
        mcq(pg, 1)
        for side in ('L', 'R'):
            pg.locator('[data-drag="tray"]').first.focus()
            pg.keyboard.press('Enter')
            pg.locator(f'[data-focus="pan-{side}"]').focus()
            pg.keyboard.press('Space')
            pg.wait_for_timeout(150)
            if side == 'L':
                # Repeated destination activation cannot clone a consumed object.
                pg.locator('[data-focus="pan-R"]').focus()
                pg.keyboard.press('Space')
                pg.wait_for_timeout(100)
                assert spec(pg)['balance']['R'] == 0
                assert pg.locator('[data-drag="tray"]').count() == 1
        sp = spec(pg)['spec']
        masses = spec(pg)['MASS'][sp['u']]
        ma, mb = masses[sp['L'][0]], masses[sp['R'][0]]
        mcq(pg, 0 if ma > mb else 1 if ma == mb else 2)
        assert pg.locator('#dots i').first.get_attribute('class') == 'p2'
        pg.locator('#nv .next').click()
        sp = spec(pg)['spec']
        assert sp['t'] == 'balance'
        assert 'کفهٔ پایین‌تر' in pg.locator('#pr').inner_text() or track == 'a'
        target = sum(spec(pg)['MASS'][sp['u']][i] for i in sp['obj'])
        # Test four overshoots with weights/cubes, then solve: exploration loses no points.
        for _ in range(4):
            put(pg, sp['tray'][-1])
            pg.locator('[data-drag="pan"]').first.focus()
            pg.keyboard.press('Enter')
            pg.wait_for_timeout(100)
        assert pg.locator('#nv .next').count() == 0
        assert pg.locator('#showme').count() == 1
        # Empty the editable pan by keyboard; then balance from the available denominations.
        while pg.locator('[data-drag="pan"]').count():
            pg.locator('[data-drag="pan"]').first.focus()
            pg.keyboard.press('Enter')
            pg.wait_for_timeout(100)
        for v in solve_coins(target, sp['tray'], 12):
            put(pg, v)
        assert pg.locator('#dots i').nth(1).get_attribute('class') == 'p2'
        print('OK evidence/keyboard/free exploration', track)
    # A valid nonminimum balance is acknowledged before requesting optimization.
    seed(pg, 'c')
    pg.click('[data-l="2"]')
    next_to(pg, g, 'fewest')
    sp = spec(pg)['spec']
    target = sum(spec(pg)['MASS'][sp['u']][i] for i in sp['obj'])
    for _ in range(target // 100):
        put(pg, 100)
    assert 'تعادل درست است' in pg.locator('#fb').inner_text()
    assert 'ترازو را درست صاف کردی' in pg.locator('#pr').inner_text()
    assert pg.locator('#nv .next').count() == 0
    assert abs(spec(pg)['balance']['a']) < .01
    while pg.locator('[data-drag="pan"]').count():
        pg.locator('[data-drag="pan"]').first.focus()
        pg.keyboard.press('Enter')
        pg.wait_for_timeout(50)
    for v in solve_coins(target, sp['tray'], 12):
        put(pg, v)
    assert pg.locator('#nv .next').count() == 1
    print('OK balance before optimization')
    # Unknown mass cannot leak through scene totals; after three failed sums help unblocks it.
    seed(pg, 'b')
    pg.click('[data-l="2"]')
    next_to(pg, g, 'mystery')
    sp = spec(pg)['spec']
    target = sum(spec(pg)['MASS'][sp['u']][i] for i in sp['obj'])
    for _ in range(3):
        put(pg, 1)
        pg.locator('[data-drag="pan"]').first.focus()
        pg.keyboard.press('Enter')
        pg.wait_for_timeout(100)
    assert pg.locator('#showme').count() == 1
    for v in solve_coins(target, sp['tray'], 12):
        put(pg, v)
    assert pg.locator('#showme').count() == 0, 'physical guidance cleared on sum phase'
    assert spec(pg)['balance']['hideL'] and spec(pg)['balance']['hideR']
    assert pg.locator('#ct').inner_text().count('؟') == 2
    pg.click('.stp button[data-d="1"]')
    for _ in range(3):
        click_text(pg, 'بررسی')
    assert pg.locator('#nv .next').count() == 0
    pg.click('#showme')
    assert pg.locator('#nv .next').count() == 1
    assert not spec(pg)['balance']['hideR']
    print('OK hidden answer/help exit')
    seed(pg, 'a')
    pg.click('[data-l="5"]')
    next_to(pg, g, 'water')
    pg.locator('[data-drag="hook"]').focus()
    pg.keyboard.press('End')
    assert pg.locator('[data-drag="hook"]').get_attribute('aria-valuetext') == 'کاملاً زیر آب'
    mcq(pg, 2)
    assert pg.locator('#nv .next').count() == 1
    print('OK water experiment by keyboard')
    pg.goto('file://'+D+'jtest.html')
    quiz=pg.evaluate("""()=>{const out=[];for(const tr of 'abcd')for(let k=0;k<100;k++){
      const qs=__J.quizPick(tr,1);if(qs.some(q=>q.after>1||['وزن','نیروسنج','نیروی شناوری'].includes(q.term)))out.push(tr);
      if(qs.length!==({a:4,b:5,c:6,d:6})[tr])out.push('count '+tr);
    }return out;}""")
    assert not quiz, quiz
    print('OK first quiz prerequisites (400 samples)')
    assert not errors, errors
    b.close()
print('ALL OK')
