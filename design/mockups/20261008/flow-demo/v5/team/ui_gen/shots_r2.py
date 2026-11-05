import pathlib
from playwright.sync_api import sync_playwright
OUT = pathlib.Path(__file__).resolve().parent.parent / 'assets_r2/ui'
SH = OUT / 'shots'; SH.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox'])
    for w, h in ((390, 800), (360, 640)):
        pg = b.new_page(viewport={'width': w, 'height': h}); msgs = []
        pg.on('console', lambda m: msgs.append(m.text) if m.type == 'error' else None)
        pg.goto((OUT / 'ui_kit.html').as_uri()); pg.wait_for_timeout(600)
        ov = pg.evaluate('document.documentElement.scrollWidth-document.documentElement.clientWidth')
        small = pg.evaluate("""()=>[...document.querySelectorAll('button,.ui-chip,.ui-tile')].filter(e=>{const r=e.getBoundingClientRect();return r.height<47.5||r.width<47.5}).map(e=>e.className+' '+Math.round(e.getBoundingClientRect().width)+'x'+Math.round(e.getBoundingClientRect().height))""")
        fs = pg.evaluate("""()=>[...document.querySelectorAll('main *')].filter(e=>e.childNodes.length&&[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim())).map(e=>parseFloat(getComputedStyle(e).fontSize)).filter(x=>x<14)""")
        pg.screenshot(path=str(SH / f'ui_kit_{w}.png'), full_page=True)
        print(w, 'hscroll', ov, 'errors', msgs, 'small targets', small, 'fs<14', fs)
    b.close()
from PIL import Image
for w in (390, 360):
    Image.open(SH / f'ui_kit_{w}.png').convert('L').save(SH / f'ui_kit_{w}_gray.png')
