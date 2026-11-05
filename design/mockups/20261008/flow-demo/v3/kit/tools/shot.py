import sys
from playwright.sync_api import sync_playwright
EXE='/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
def shot(url,out,w,h,full=False,reduced=False):
    with sync_playwright() as pw:
        b=pw.chromium.launch(executable_path=EXE,args=['--no-sandbox'])
        pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
        pg.goto(url); pg.wait_for_timeout(600)
        pg.screenshot(path=out,full_page=full); b.close()
if __name__=='__main__':
    shot(sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),len(sys.argv)>5)
