#!/usr/bin/env python3
"""یک دستور برای کل ماکت جریان بازی (D209): ساخت همهٔ بخش‌ها به ترتیب و بررسی اینکه پوشهٔ entry-page همهٔ صفحه‌ها را دارد.
ترتیب: ماکت نقشه ← نقشهٔ کلی ← منوی کاراکتر ← صفحهٔ ورود (که بقیه را کنار خودش کپی می‌کند: name/character/overview/map/cardbox).
بعد هر صفحه با مرورگر باز می‌شود و خطای کنسول شمرده می‌شود. انتشار: entry-page/artifact.html + files بالا (نام «index.html» در files نیاید)."""
import subprocess, sys, pathlib
H = pathlib.Path(__file__).resolve().parent
for d in ('map-travel', 'overview-board', 'character-menu', 'entry-page'):
    r = subprocess.run([sys.executable, 'build.py'], cwd=H / d, capture_output=True, text=True)
    print(d, 'OK' if r.returncode == 0 else 'FAIL\n' + r.stderr[-800:])
    if r.returncode: sys.exit(1)
E = H / 'entry-page'
PAGES = ['index', 'name', 'character', 'overview', 'map', 'cardbox']
from playwright.sync_api import sync_playwright
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch(); 
    for n in PAGES:
        f = E / (n + '.html')
        if not f.exists(): print('MISSING', n); bad += 1; continue
        pg = b.new_page(viewport={'width': 390, 'height': 780}); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.goto(f.as_uri() + ('#flow-test' if n == 'character' else '')); pg.wait_for_timeout(1500)
        print(n, 'errors', errs); bad += len(errs); pg.close()
    b.close()
sys.exit(1 if bad else 0)
