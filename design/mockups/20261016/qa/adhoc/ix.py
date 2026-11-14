from playwright.sync_api import sync_playwright
import pathlib
E=pathlib.Path('/home/claude/science-games/design/mockups/20261016/entry-page').resolve()
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,h,n in((390,780,'a'),(360,640,'b'),(412,915,'c'),(1280,720,'d')):
        pg=b.new_context(viewport={'width':w,'height':h}).new_page(); pg.goto((E/'index.html').as_uri()); pg.wait_for_timeout(5000); pg.screenshot(path=f'/tmp/ix_{n}.png')
        print(n,pg.evaluate("(()=>{const q=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();return [Math.round(r.top),Math.round(r.bottom)]};return [q('.ttl'),q('#world'),q('h1'),q('#pf'),q('#ring'),q('.stage')]})()"))
    b.close()
