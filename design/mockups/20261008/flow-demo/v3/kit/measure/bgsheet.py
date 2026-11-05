# bgsheet.py: عکس «فقط زمینه» برای هر ۴ صفحه (همه‌چیز غیر از زمین پنهان) کنار هم، تا جای تزئین نسبت به مسیر دیده شود
import sys,io
sys.path.insert(0,'.')
from measure import *
out=sys.argv[1]
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=EXE,args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':390,'height':800}); pg.goto('file://'+os.path.abspath('../phone.html')); pg.wait_for_timeout(800)
    pg.evaluate(style(f'{HIDE_ALL}{{visibility:hidden!important}}')); pg.wait_for_timeout(100)
    ims=[Image.open(io.BytesIO(pg.locator('#m-'+k).screenshot())).convert('RGB') for k in ('stadium','space','farm','city')]
    S=Image.new('RGB',(390*4+18,800),(30,30,30))
    for i,im in enumerate(ims): S.paste(im,(i*396,0))
    S.save(out); b.close()
