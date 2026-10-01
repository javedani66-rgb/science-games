# «شروع دوباره» برای والدین: کد پیشرفت پیش از پاک کردن دیده شود، پیشرفت پاک شود، نام/پایه/شخصیت بماند،
# و با چسباندن همان کد در کوله‌پشتی پیشرفت برگردد. استفاده: python3 resetchk.py — «RESET OK» یعنی درست است.
from harness import *
JURL='file://'+D+'jtest.html'
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':400,'height':860}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(JURL); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(200)
    pg.fill('#jnm','سارا'); pg.click('#jnx'); pg.click('[data-t="1"]'); pg.click('#jnx'); pg.click('[data-g="2"]'); pg.click('#jnx'); pg.wait_for_timeout(400)
    if pg.locator('#jok').count(): pg.click('#jok')
    pg.evaluate("""()=>{const {curP,missions,trk,save}=__J;const p=curP();for(let i=0;i<3;i++)missions(p,i).forEach(id=>{p.S.ls=p.S.ls||{};p.S.ls[trk(p)+':'+id]=2;});p.home[0]=1;save();}""")
    before=pg.evaluate("()=>[__J.curStop(__J.curP()),__J.makeCode(__J.curP())]"); pg.evaluate("__J.adults()"); pg.wait_for_timeout(200)
    pg.click('#jrs'); shown=pg.locator('#jrsc b').inner_text(); pg.click('#jry'); pg.wait_for_timeout(400)
    after=pg.evaluate("()=>{const p=__J.curP();return [__J.curStop(p),p.name,p.g,p.t,p.home[0],JSON.parse(localStorage.getItem('sm-journey-v1')).profiles.length]}")
    ok=before[0]==3 and shown==before[1] and after[:5]==[0,'سارا',2,1,0] and after[5]==1
    back=pg.evaluate("c=>{const p=__J.curP();const r=__J.readCode(c);return r?true:false}",shown)
    print('before',before[0],'after',after,'code shown ok',shown==before[1],'code readable',back,'ERR',errs)
    print('RESET OK' if ok and back and not errs else 'RESET PROBLEM'); b.close()
