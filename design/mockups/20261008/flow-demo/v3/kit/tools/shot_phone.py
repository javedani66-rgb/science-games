# shot_phone.py <tag>: عکس هر ۴ صفحهٔ phone.html با Chromium نصب‌شده (playwright install ممنوع)
import sys,os
from playwright.sync_api import sync_playwright
EXE='/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
K=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
tag=sys.argv[1]
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=EXE,args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':390,'height':800}); errs=[]
    pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None); pg.on('requestfailed',lambda r: errs.append('FAIL '+r.url))
    pg.goto('file://'+K+'/phone.html'); pg.wait_for_timeout(900)
    for k in ('stadium','space','farm','city'):
        pg.locator('#m-'+k).screenshot(path=f'{K}/shots/{tag}_{k}.png')
    for j in ('stadium-space','farm-city'): pg.locator('#j-'+j).screenshot(path=f'{K}/shots/{tag}_join_{j}.png')
    print('errors',errs); b.close()
