from playwright.sync_api import sync_playwright
import pathlib
E=pathlib.Path('/home/claude/science-games/design/mockups/20261016/entry-page').resolve()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_context(viewport={'width':390,'height':780}).new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and errs.append(m.text))
    pg.goto((E/'map.html').as_uri()+'#enter-M07'); pg.wait_for_timeout(6000)
    print(pg.evaluate("[!!document.getElementById('tut'),document.getElementById('goenv')&&getComputedStyle(document.getElementById('goenv')).display,document.getElementById('env')&&document.getElementById('env').hidden]"))
    pg.evaluate("document.getElementById('tut')&&document.getElementById('tut').remove()")
    pg.click('#goenv',force=True); pg.wait_for_timeout(3500)
    print(pg.evaluate("[document.getElementById('env').hidden,document.querySelectorAll('.sc').length,document.getElementById('envbody').innerHTML.length]"),errs)
    pg.screenshot(path='/tmp/i0.png'); b.close()
