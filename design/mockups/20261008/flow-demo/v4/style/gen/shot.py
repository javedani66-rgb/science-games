import sys, os
from playwright.sync_api import sync_playwright
STYLE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rnd = sys.argv[1]; what = sys.argv[2:]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 390, 'height': 800})
    for w in what:
        name, _, q = w.partition('?')
        pg.goto('file://%s/%s.html%s' % (STYLE, name, ('?' + q) if q else ''))
        pg.wait_for_timeout(700)
        tag = w.replace('?', '_').replace('=', '').replace('&', '_')
        pg.screenshot(path='%s/shots/r%s_%s.png' % (STYLE, rnd, tag))
    b.close()
