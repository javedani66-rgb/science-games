"""Interaction regressions for ideal-machine scenes. Run after build.py.

Protects keyboard continuity, independent exploration scoring, guided exits,
and replacement of an animating configuration. Uses only public UI actions.
"""
from t2 import G, SOL, TURL, spec, sync_playwright

MACHINES = ('ramp', 'wheel', 'wedge', 'pulley')


def open_station(pg, station, level=None):
    pg.goto(TURL)
    pg.evaluate('''()=>localStorage.setItem('sm-workshop-v3',JSON.stringify({
      track:'b',nums:true,forces:true,formula:true,
      prog:Object.fromEntries(['ramp','wheel','wedge','pulley'].map(k=>
        ['b:'+k,{lv:[3,3,3,3,3],best:0}]))}))''')
    pg.reload()
    pg.locator('.st[data-k="%s"]' % station).click()
    if level is None:
        pg.get_by_role('button', name='آزمایشگاه', exact=False).click()
    else:
        pg.locator('[data-l="%s"]' % level).click()
    pg.locator('#sc').wait_for()


def keyboard(pg, key, count=1):
    pg.locator('#sc [data-drag]').first.focus()
    for _ in range(count):
        pg.keyboard.press(key)


def first_physical(pg, g, station, level):
    open_station(pg, station, level)
    while spec(pg)['spec']['t'] not in ('wc', 'sc', 'choose', 'fit'):
        SOL[station](g, pg, spec(pg)['spec'])
        pg.locator('#nv .next').wait_for()
        pg.locator('#nv .next').click()
    return spec(pg)['i']


def wait_point(pg, index, point):
    pg.wait_for_function('''([i,p])=>document.querySelectorAll('#dots i')[i]
      ?.classList.contains(p)''', arg=[index, point])


def fail_three(pg, station):
    for _ in range(3):
        if station == 'ramp':
            pg.locator('#cl .btn', has_text='بکش').click()
            # The feedback appears before the delayed reset; the third attempt
            # deliberately clicks show-me before that reset can run.
            pg.wait_for_function("()=>document.querySelector('#fb').textContent.includes('جعبه بالا نرفت')")
        else:
            keyboard(pg, 'ArrowDown')
    pg.locator('#showme').wait_for()


def successful_nonminimum(pg, station):
    if station == 'wedge':
        pg.locator('#vs [data-v="6"]').click()
    elif station == 'wheel':
        pg.locator('#rs [data-r="4"]').click()
    elif station == 'pulley':
        pg.locator('#sys [data-n="4"]').click()
    keyboard(pg, 'ArrowLeft' if station == 'ramp' else 'ArrowDown', 8)
    if station == 'ramp':
        pg.locator('#cl .btn', has_text='بکش').click()


def stable_scene(pg, milliseconds=1000):
    before = pg.locator('#sc').inner_html()
    # This bounded wait specifically detects a delayed obsolete repaint.
    pg.wait_for_timeout(milliseconds)
    assert pg.locator('#sc').inner_html() == before, 'obsolete callback repainted scene'


def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        pg = browser.new_page(viewport={'width': 400, 'height': 900})
        errors = []
        pg.on('pageerror', lambda e: errors.append(str(e)))
        g = G(pg)
        for station in MACHINES:
            open_station(pg, station)
            if station == 'wedge':
                pg.locator('#ws [data-l="8"]').click()
            keyboard(pg, 'ArrowDown')
            assert pg.evaluate("()=>document.activeElement.matches('#sc [data-drag]')"), station + ' lost focus'
            keyboard(pg, 'ArrowDown')
            assert pg.evaluate("()=>document.activeElement.matches('#sc [data-drag]')"), station + ' lost repeated focus'
            print('PASS keyboard', station)
        open_station(pg, 'wedge')
        pg.get_by_role('button', name='آزمایش پیچ', exact=True).click()
        keyboard(pg, 'ArrowRight', 2)
        assert pg.evaluate("()=>document.activeElement.matches('#sc [data-drag]')"), 'screw lost focus'
        print('PASS keyboard screw')

        for station, level in (('wedge', 1), ('wheel', 1), ('pulley', 2), ('ramp', 2)):
            index = first_physical(pg, g, station, level)
            fail_three(pg, station)
            pg.locator('#showme').click()
            wait_point(pg, index, 'p1')
            stable_scene(pg)
            print('PASS guided exit', station)

            index = first_physical(pg, g, station, level)
            fail_three(pg, station)
            successful_nonminimum(pg, station)
            wait_point(pg, index, 'p2')
            print('PASS nonminimum after exploration', station)

        open_station(pg, 'wedge')
        g.drag(320, 202, 320, 255, steps=2)
        pg.locator('#ws [data-l="8"]').click()
        stable_scene(pg)
        assert pg.locator('#fb').inner_text() == '', 'obsolete wedge completion feedback'
        print('PASS stale wedge completion')
        open_station(pg, 'pulley')
        g.drag(376, 267, 376, 325, steps=2)
        pg.locator('#sys [data-n="4"]').click()
        stable_scene(pg)
        assert pg.locator('#fb').inner_text() == '', 'obsolete pulley release feedback'
        print('PASS stale pulley release')
        assert not errors, errors
        browser.close()
    print('ALL MACHINE INTERACTION CHECKS PASSED')


if __name__ == '__main__':
    run()
