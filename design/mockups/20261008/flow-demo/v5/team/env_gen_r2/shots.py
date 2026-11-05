import sys, pathlib
from playwright.sync_api import sync_playwright
import layout as L
SH = L.OUT / 'shots'; SH.mkdir(exist_ok=True)
src = 'file://' + str(L.OUT / 'env_sheet.html')
ys = [int(a) for a in sys.argv[1:]] or [0, 600, 1100, 1700, 2500, 3560, 4000, 4551]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox'])
    for (w, h) in ((390, 800), (360, 640)):
        pg = b.new_page(viewport={'width': w, 'height': h})
        for y in ys:
            for g in ('', '&gray=1'):
                pg.goto(src + '?y=%d%s' % (y, g)); pg.wait_for_timeout(150)
                pg.screenshot(path=str(SH / ('env_%dx%d_y%d%s.png' % (w, h, y, '_gray' if g else ''))))
    b.close()
