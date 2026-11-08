#!/usr/bin/env python3
"""اجرای کامل ماکت جریان مثل یک کودک: ورود ← نام ← کاراکتر ← نقشه ← همهٔ ایستگاه‌ها ← مخفی‌گاه ← آب‌های آزاد.
پیش‌نیاز: python3 ../build_all.py  (صفحه‌ها ساخته باشند)  و  playwright + chromium.
استفاده:
  python3 full_run.py                 # اجرای کامل (حدود ۵ دقیقه)، ویدیو در qa/out/
  python3 full_run.py --max 3         # فقط ۳ ایستگاه اول (آزمون سریع)
  python3 full_run.py --no-video      # بدون ضبط
بعد از اجرا اگر ضبط شده باشد: ffmpeg -i out/*.webm -c:v libx264 -crf 28 -pix_fmt yuv420p flow.mp4
خروجی «errors []» یعنی هیچ خطای کنسول نبود. اگر وسط راه گیر کند، خطا و ایستگاه را چاپ می‌کند.
نکته: پروسهٔ پس‌زمینه ممکن است با پایان نشست قطع شود؛ در محیط ابری آن را در پیش‌زمینه اجرا کن."""
import argparse, pathlib, sys
from playwright.sync_api import sync_playwright
E = pathlib.Path(__file__).resolve().parent.parent / 'entry-page'
ap = argparse.ArgumentParser(); ap.add_argument('--max', type=int, default=0); ap.add_argument('--no-video', action='store_true')
ap.add_argument('--char', type=int, default=1); ap.add_argument('--color', type=int, default=3); a = ap.parse_args()
out = pathlib.Path(__file__).resolve().parent / 'out'; out.mkdir(exist_ok=True)
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 390, 'height': 780}, **({} if a.no_video else {'record_video_dir': str(out), 'record_video_size': {'width': 390, 'height': 780}}))
    pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
    pg.goto((E / 'index.html').as_uri()); pg.wait_for_timeout(2500)
    pg.click('#go'); pg.wait_for_url('**/name.html*'); pg.wait_for_timeout(1200); pg.fill('#nm', 'مینا'); pg.wait_for_timeout(500); pg.click('#go')
    pg.wait_for_url('**/character.html*'); pg.wait_for_timeout(1800)
    pg.query_selector_all('.char')[a.char].click(); pg.wait_for_timeout(1000)
    pg.query_selector_all('#colors button, #colors [role=radio]')[a.color].click(); pg.wait_for_timeout(1200); pg.click('#go')
    pg.wait_for_url('**/overview.html*'); pg.wait_for_timeout(2500); pg.click('#go')
    pg.wait_for_url('**/map.html*'); pg.wait_for_timeout(4000)
    pg.wait_for_function("document.getElementById('tut') && !document.getElementById('tut').hidden", timeout=60000)
    while pg.evaluate("!document.getElementById('tut').hidden"):
        pg.click('#tn'); pg.wait_for_timeout(700)
    n = 0
    while True:
        pg.wait_for_function("!busy&&!document.getElementById('fin').hidden", timeout=60000)
        here = pg.evaluate('here'); print(n, here, flush=True)
        if here == 'M12' or (a.max and n + 1 >= a.max):
            break
        pg.click('#fin'); pg.wait_for_function('!busy', timeout=60000); pg.wait_for_timeout(900); n += 1
    if here == 'M12':
        pg.click('#fin'); pg.wait_for_timeout(5000); pg.click('#bb2'); pg.wait_for_timeout(17000)
    print('errors', errs)
    ctx.close(); b.close()
sys.exit(1 if errs else 0)
