import sys, os
from playwright.sync_api import sync_playwright
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, 'shots')
os.makedirs(S, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox'])
    for w, hgt in ((390, 800), (360, 640)):
        pg = b.new_page(viewport={'width': w, 'height': hgt}); pg.set_default_timeout(20000)
        pg.goto('file://%s/scene_demo.html' % H); pg.wait_for_timeout(500)
        pg.screenshot(path='%s/scene_%dx%d_full.png' % (S, w, hgt), full_page=True)
        pg.goto('file://%s/samples_demo.html' % H); pg.wait_for_timeout(500)
        pg.screenshot(path='%s/samples_%dx%d.png' % (S, w, hgt), full_page=True)
        pg.close()
    # mid-transition
    pg = b.new_page(viewport={'width': 390, 'height': 800})
    pg.goto('file://%s/scene_demo.html' % H); pg.wait_for_timeout(300)
    pg.evaluate("document.getElementById('scene').scrollIntoView()")
    pg.click('#bn'); pg.wait_for_timeout(600)
    pg.screenshot(path='%s/transition_mid.png' % S)
    mid = pg.evaluate("[getComputedStyle(document.getElementById('tr-day')).opacity,getComputedStyle(document.getElementById('tr-night')).opacity]")
    pg.wait_for_timeout(900)
    end = pg.evaluate("[getComputedStyle(document.getElementById('tr-day')).opacity,getComputedStyle(document.getElementById('tr-night')).opacity]")
    dur = pg.evaluate("getComputedStyle(document.getElementById('tr-night')).transitionDuration+' '+getComputedStyle(document.getElementById('tr-night')).transitionProperty")
    print('mid', mid, 'end', end, dur)
    b.close()
