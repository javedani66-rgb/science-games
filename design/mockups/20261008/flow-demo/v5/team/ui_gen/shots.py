import pathlib, asyncio
from playwright.sync_api import sync_playwright
OUT = pathlib.Path(__file__).resolve().parent.parent / 'assets/ui'
SH = OUT / 'shots'; SH.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in ((390, 800), (360, 640)):
        pg = b.new_page(viewport={'width': w, 'height': h}); msgs = []
        pg.on('console', lambda m: msgs.append(m.text) if m.type == 'error' else None)
        pg.goto((OUT / 'ui_kit.html').as_uri()); pg.wait_for_timeout(500)
        ov = pg.evaluate('document.documentElement.scrollWidth-document.documentElement.clientWidth')
        pg.screenshot(path=str(SH / f'ui_kit_{w}.png'), full_page=True)
        print(w, 'hscroll', ov, 'errors', msgs)
    b.close()
from PIL import Image, ImageOps
for w in (390, 360):
    im = Image.open(SH / f'ui_kit_{w}.png').convert('L'); im.save(SH / f'ui_kit_{w}_gray.png')
