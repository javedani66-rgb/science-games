import sys,pathlib
from playwright.sync_api import sync_playwright
H=pathlib.Path(__file__).resolve().parents[1]
def shots(tag,views=('stadium','space','farm','city','join12','join23','join34','menu','menu2')):
    with sync_playwright() as pw:
        b=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium',args=['--no-sandbox'])
        pg=b.new_page(viewport={'width':390,'height':800})
        errs=[]
        pg.on('console',lambda m: errs.append(m.text) if m.type in('error','warning') else None); pg.on('pageerror',lambda e: errs.append(str(e)))
        for v in views:
            pg.goto(f'file://{H}/proof.html?v={v}'); pg.wait_for_function("document.documentElement.dataset.ready==='1'"); pg.wait_for_timeout(500)
            pg.screenshot(path=str(H/'shots'/f'{tag}_{v}.png'))
        b.close()
    print('errs',errs)
if __name__=='__main__': shots(sys.argv[1],tuple(sys.argv[2:]) or ('stadium','space','farm','city','join12','join23','join34','menu','menu2'))
