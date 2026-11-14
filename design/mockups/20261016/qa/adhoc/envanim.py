from playwright.sync_api import sync_playwright
import pathlib
E=pathlib.Path('/home/claude/science-games/design/mockups/20261016/entry-page').resolve()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_context(viewport={'width':390,'height':780}).new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    pg.goto((E/'map.html').as_uri()+'#enter-M07'); pg.wait_for_timeout(6000); pg.wait_for_timeout(1500)
    pg.click('#goenv')
    for i,ms in enumerate((350,700,1300)): pg.wait_for_timeout(ms if i==0 else ms-[350,700,1300][i-1]); pg.screenshot(path=f'/tmp/a{i}.png')
    pg.wait_for_timeout(1800); pg.screenshot(path='/tmp/a3.png')
    pg.click('#envgo'); pg.wait_for_timeout(450); pg.screenshot(path='/tmp/a4.png'); pg.wait_for_timeout(1500); pg.screenshot(path='/tmp/a5.png')
    print('scene hidden', pg.evaluate("document.getElementById('envsc').hidden"))
    pg.click('#envsbk'); pg.wait_for_timeout(3000); pg.screenshot(path='/tmp/a6.png')
    pg.click('#envb'); pg.wait_for_timeout(500); pg.screenshot(path='/tmp/a7.png'); pg.wait_for_timeout(1200)
    print('env hidden', pg.evaluate("document.getElementById('env').hidden"), errs); b.close()
from PIL import Image
ims=[Image.open(f'/tmp/a{i}.png').resize((260,520)) for i in range(8)]
sh=Image.new('RGB',(260*8,520));[sh.paste(im,(260*i,0)) for i,im in enumerate(ims)];sh.save('/tmp/aall.png')
