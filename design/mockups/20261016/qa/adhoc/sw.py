from playwright.sync_api import sync_playwright
import pathlib
from PIL import Image
E=pathlib.Path('/home/claude/science-games/design/mockups/20261016/entry-page').resolve()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_context(viewport={'width':390,'height':780},reduced_motion='reduce').new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto((E/'map.html').as_uri()+'#enter-M07'); pg.wait_for_timeout(6000)
    pg.evaluate("(()=>{const b=document.getElementById('tn'); if(b) b.click();})()"); pg.wait_for_function("!document.getElementById('goenv').hidden",timeout=20000); pg.click('#goenv'); pg.wait_for_timeout(3500)
    pg.click('.sc[data-p="0"]',position={'x':150,'y':12})
    for i in range(6): pg.wait_for_timeout(150); pg.screenshot(path=f'/tmp/w{i}.png')
    print(errs); b.close()
ims=[Image.open(f'/tmp/w{i}.png').resize((260,520)) for i in range(6)]
sh=Image.new('RGB',(260*6,520));[sh.paste(im,(260*i,0)) for i,im in enumerate(ims)];sh.save('/tmp/wall.png')
