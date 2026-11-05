from shot import *
from playwright.sync_api import sync_playwright
K='file:///home/claude/science-games/design/mockups/20261008/flow-demo/v3/kit/'
SH='/home/claude/science-games/design/mockups/20261008/flow-demo/v3/kit/shots/'
import sys
tag=sys.argv[1]
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=EXE,args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':390,'height':800})
    pg.goto(K+'phone.html'); pg.wait_for_timeout(700)
    for sid in ('s-map','s-menu','s-cards'):
        pg.locator('#'+sid).screenshot(path=SH+f'{tag}_390x800_{sid[2:]}.png')
    pg.goto(K+'index.html'); pg.wait_for_timeout(700); pg.screenshot(path=SH+f'{tag}_index_390_full.png',full_page=True)
    pg2=b.new_page(viewport={'width':1200,'height':900}); pg2.goto(K+'index.html'); pg2.wait_for_timeout(700)
    pg2.screenshot(path=SH+f'{tag}_index_1200_full.png',full_page=True)
    errs=[]
    pg3=b.new_page(); pg3.on('console',lambda m: errs.append(m.text) if m.type=='error' else None); pg3.on('requestfailed',lambda r: errs.append('FAIL '+r.url)); pg3.goto(K+'index.html'); pg3.wait_for_timeout(500)
    print('errors',errs)
    b.close()
