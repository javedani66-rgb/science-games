from playwright.sync_api import sync_playwright
import pathlib
E=pathlib.Path('/home/claude/science-games/design/mockups/20261016/entry-page').resolve()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_context(viewport={'width':390,'height':780}).new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    pg.goto((E/'map.html').as_uri()+'#enter-M07'); pg.wait_for_timeout(6000)
    pg.wait_for_timeout(1500); pg.evaluate("(()=>{const b=document.getElementById('tn'); if(b) b.click();})()"); pg.wait_for_function("!document.getElementById('goenv').hidden",timeout=20000); pg.click('#goenv'); pg.wait_for_timeout(3500); pg.screenshot(path='/tmp/i0.png')
    pg.click('.sc[data-p="0"]',position={'x':150,'y':12}); pg.wait_for_timeout(250); pg.screenshot(path='/tmp/i1.png'); pg.wait_for_timeout(250); pg.screenshot(path='/tmp/i2.png'); pg.wait_for_timeout(500); pg.screenshot(path='/tmp/i3.png')
    pg.click('.sc[data-p="2"]',position={'x':150,'y':150}); pg.wait_for_timeout(500); pg.screenshot(path='/tmp/i4.png')
    pg.click('.sc[data-p="2"] .gob'); pg.wait_for_timeout(2200); pg.screenshot(path='/tmp/i5.png')
    print(pg.evaluate("document.getElementById('envsc').hidden"), errs); b.close()
from PIL import Image
ims=[Image.open(f'/tmp/i{i}.png').resize((260,520)) for i in range(6)]
sh=Image.new('RGB',(260*6,520));[sh.paste(im,(260*i,0)) for i,im in enumerate(ims)];sh.save('/tmp/iall.png')
