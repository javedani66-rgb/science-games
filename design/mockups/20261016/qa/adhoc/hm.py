from playwright.sync_api import sync_playwright
import pathlib
E=pathlib.Path('/home/claude/science-games/design/mockups/20261016/entry-page').resolve()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_context(viewport={'width':390,'height':780}).new_page()
    pg.goto((E/'map.html').as_uri()+'#enter-M02'); pg.wait_for_timeout(6000)
    pg.evaluate("(()=>{const b=document.getElementById('tn'); for(let i=0;i<8;i++){const x=document.getElementById('tn'); if(x&&!document.getElementById('tut').hidden) x.click();}})()")
    pg.wait_for_timeout(1500); pg.click('#home',force=True); pg.wait_for_timeout(2500); print(pg.url); b.close()
