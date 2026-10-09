import sys
from playwright.sync_api import sync_playwright
V3='/home/claude/science-games/design/mockups/20261008/flow-demo/v3/'
out=sys.argv[1]
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':390,'height':800})
    pg.goto('file://'+V3+'index.html'); pg.wait_for_timeout(500)
    pg.evaluate("__st.tutOn=false;__st.tutDone.map=true;__st.tut=null;renderOv();document.body.classList.add('rm');document.getElementById('rvbar').style.display='none';render()")
    pg.wait_for_timeout(500)
    names={}
    for key,sel in [('stadium','.land[data-land=stadium]'),('space','.land[data-land=space]'),('farm','.land[data-land=farm]'),('city','.land[data-land=city]')]:
        pg.evaluate("""(sel)=>{const l=document.querySelector(sel);const b=document.querySelector('#mapbody');b.style.scrollBehavior='auto';const r=l.getBoundingClientRect(),br=b.getBoundingClientRect();b.scrollTop+= r.top-br.top-40;}""",sel)
        pg.wait_for_timeout(300)
        pg.screenshot(path=f'{out}/base_{key}.png')
    b.close()
