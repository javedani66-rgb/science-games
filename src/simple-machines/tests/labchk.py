# «اول آزمایش آزاد؟» offer (2026-10-01): appears once before a stop's first mission (real page, not jtest),
# «شروع مأموریت» goes on to the mission, the offer does not come back. Prints nothing when fine.
from harness import *
with sync_playwright() as pw:
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':400,'height':860})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(URL); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(300)
    pg.fill('#jnm','آزمون'); pg.click('#jnx'); pg.click('[data-t="1"]'); pg.click('#jnx'); pg.click('[data-g="0"]'); pg.click('#jnx'); pg.wait_for_timeout(400)
    if pg.locator('#jok').count(): pg.click('#jok'); pg.wait_for_timeout(200)
    pg.click('#jgo'); pg.wait_for_timeout(400)
    if not pg.locator('#jlo').count(): print('no lab offer before first mission')
    else:
        pg.click('#jlm'); pg.wait_for_timeout(300)
        if pg.locator('#jgo2').count(): pg.click('#jgo2'); pg.wait_for_timeout(400)
        if not pg.locator('#sc').count(): print('mission did not start after «شروع مأموریت»')
        pg.goto(URL); pg.wait_for_timeout(400); pg.click('#jgo'); pg.wait_for_timeout(400)
        if pg.locator('#jlo').count(): print('offer came back')
    if errs: print('ERR',errs[:3])
    b.close()
