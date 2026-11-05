import sys, pathlib
from playwright.sync_api import sync_playwright
import layout as L
SH = L.OUT / 'shots'; SH.mkdir(exist_ok=True)
src = 'file://' + str(L.OUT / 'env_sheet.html')
ys = [int(a) for a in sys.argv[1:]] or [0, 1450, 1900]
with sync_playwright() as p:
    b = p.chromium.launch()
    for (w, h) in ((390, 800), (360, 640)):
        pg = b.new_page(viewport={'width': w, 'height': h})
        for y in ys:
            for g in ('', '&gray=1'):
                pg.goto(src + '?y=%d%s' % (y, g)); pg.wait_for_timeout(150)
                pg.screenshot(path=str(SH / ('env_%dx%d_y%d%s.png' % (w, h, y, '_gray' if g else ''))))
    b.close()
