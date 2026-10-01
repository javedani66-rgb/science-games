"""Lever evidence, keyboard physics, free exploration and real solution guidance."""
from t2 import *
import itertools


def seed(pg, track, level):
    pg.goto(TURL)
    pg.evaluate("p=>localStorage.setItem('sm-workshop-v3',JSON.stringify(p))", {
        'prog': {f'{track}:lever': {'lv': [3]*5}}, 'nums': True,
        'forces': True, 'formula': False, 'track': track})
    pg.reload(); pg.click('.st[data-k=lever]'); pg.click(f'[data-l="{level}"]')
    pg.wait_for_timeout(50)


def next_kind(pg, g, kind):
    for _ in range(30):
        sp = spec(pg)['spec']
        if sp['t'] == kind: return
        lever(g, pg, sp); pg.locator('#nv .next').click()
    raise AssertionError('missing '+kind)


def place(pg, pos):
    pg.locator('[data-drag="tray"]').first.focus(); pg.keyboard.press('Enter')
    pg.locator(f'[data-focus="pos-{pos}"]').focus(); pg.keyboard.press('Space')
    pg.wait_for_timeout(80)


with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e))); g = G(pg)
    for track in ('a', 'b', 'c', 'd'):
        seed(pg, track, 1)
        assert spec(pg)['spec']['t'] == 'predict' and spec(pg)['spec']['poe']
        mcq(pg, 0); pg.wait_for_timeout(1400)
        assert not pg.locator('#nv .next').count(), 'guess was graded'
        assert 'تخته چه شد' in g.text('#pr')
        sp = spec(pg)['spec']; lm = spec(pg)['LV_MASS']
        m = lambda v: v if isinstance(v, int) else lm[v]
        tl = sum(-p*m(v) for p, v in sp['items'] if p < 0)
        tr = sum(p*m(v) for p, v in sp['items'] if p > 0)
        mcq(pg, 0 if tr > tl else 1 if tr == tl else 2)
        pg.locator('#nv .next').click()
        sp = spec(pg)['spec']; assert sp['t'] == 'balance'
        for _ in range(4):
            for _ in sp['pieces']: place(pg, 5)
            assert not pg.locator('#nv .next').count()
            while pg.locator('[data-drag="stk"]').count():
                pg.locator('[data-drag="stk"]').first.focus()
                pg.keyboard.press('Enter'); pg.wait_for_timeout(80)
        assert pg.locator('#showme').count() == 1
        tl = sum(-p*m(v) for p, v in sp['items'] if p < 0)
        solution = next(pos for pos in itertools.product(range(1, 6), repeat=len(sp['pieces']))
                        if sum(v*p for v, p in zip(sp['pieces'], pos)) == tl)
        for pos in solution: place(pg, pos)
        assert pg.locator('#dots i').nth(1).get_attribute('class') == 'p2'
        assert spec(pg)['lever']['left'] == spec(pg)['lever']['right']
        print('OK observed evidence, keyboard balance and free trials', track)
    seed(pg, 'b', 2); next_kind(pg, g, 'balance')
    place(pg, 5); place(pg, 5)
    state = spec(pg)['lever']; assert state['a'] == 14
    # Remove the 20 kg brick from the tilted stack, then drop onto visible p4.
    angle = math.radians(state['a'])
    def beam_point(p, y):
        return (320+p*52*math.cos(angle)-(y-290)*math.sin(angle),
                290+p*52*math.sin(angle)+(y-290)*math.cos(angle))
    start = beam_point(5, 278-(10/5*13+3)-1-25)
    end = beam_point(4, 278)
    g.drag(*start, *end)
    pg.wait_for_timeout(150)
    assert spec(pg)['lever']['right'] == 130, spec(pg)['lever']
    print('OK drop on visibly tilted plank')
    seed(pg, 'b', 2); next_kind(pg, g, 'mystery')
    assert pg.locator('#ct').inner_text().count('؟') == 2
    assert pg.locator('#sc .farr').count() == 0, 'hidden mass cannot use a fake force scale'
    print('OK unknown mass totals and forces hidden')
    # Demonstration during the initial animation must cancel the old tilt tween.
    pg.emulate_media(reduced_motion='no-preference')
    pg.reload()  # reduceMotion is read when the page starts
    seed(pg, 'b', 2); next_kind(pg, g, 'balance')
    for _ in range(3): pg.get_by_role('button', name='راهنمای چیدن', exact=True).click()
    pg.click('#showme'); pg.wait_for_timeout(1200)
    state = spec(pg)['lever']
    assert state['left'] == state['right'] and state['a'] == 0
    assert all(p['used'] for p in state['pieces'])
    assert pg.locator('#dots i').nth(1).get_attribute('class') == 'p1'
    print('OK visible balance solution and animation cancellation')
    pg.emulate_media(reduced_motion='reduce'); pg.reload()
    seed(pg, 'a', 3)
    pg.locator('[data-focus="fulcrum"]').focus(); pg.keyboard.press('Home')
    for f in range(-4, 5):
        if f > -4: pg.keyboard.press('ArrowRight')
        state = spec(pg)['lift']; assert state['f'] == f
        assert abs(state['need']-state['W']*(f+5)/(5-f)) < 1e-9
        assert abs(state['rock']['y']-480) < 1e-9
        assert state['pivot']['y'] == 448
        assert pg.evaluate("()=>document.activeElement.dataset.focus") == 'fulcrum'
        assert pg.evaluate("()=>[...document.querySelectorAll('#sc .farr')].every(e=>e.getBBox().y>=60)")
    for _ in range(4): click_text(pg, 'فشار'); pg.wait_for_timeout(80)
    assert pg.locator('#showme').count() == 1 and not pg.locator('#nv .next').count()
    pg.locator('[data-focus="fulcrum"]').focus(); pg.keyboard.press('Home')
    pg.locator('[data-focus="press"]').focus(); pg.keyboard.press('Space'); pg.wait_for_timeout(100)
    assert pg.locator('#dots i').first.get_attribute('class') == 'p2'
    assert spec(pg)['lift']['rock']['y'] < 480
    print('OK pivot, grounded rock, force model, keyboard lift and free trials')
    seed(pg, 'a', 3)
    for _ in range(3): click_text(pg, 'فشار'); pg.wait_for_timeout(80)
    pg.click('#showme'); pg.wait_for_timeout(100)
    assert spec(pg)['lift']['a'] == 1 and spec(pg)['lift']['rock']['y'] < 480
    assert pg.locator('#dots i').first.get_attribute('class') == 'p1'
    print('OK visible lift solution')
    seed(pg, 'a', 3); next_kind(pg, g, 'liftq')
    assert not pg.locator('.mcq').count()
    click_text(pg, 'فشار'); pg.wait_for_timeout(80)
    assert pg.locator('.mcq').count() == 1 and spec(pg)['lift']['a'] == 1
    assert pg.locator('#sc path[stroke="#7A3FC8"]').count() == 1
    mcq(pg, 0)
    assert pg.locator('#dots i').nth(2).get_attribute('class') == 'p2'
    print('OK motion before assessment')
    assert not errs, errs
    print('ALL OK'); b.close()
