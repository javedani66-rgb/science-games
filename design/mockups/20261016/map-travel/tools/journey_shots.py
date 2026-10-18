#!/usr/bin/env python3
"""سفر M02→M07 روی ماکت و چند عکس ۳۹۰×۷۰۰ (scale 2). اجرا: python3 tools/journey_shots.py <پوشهٔ خروجی>"""
import sys, pathlib
from playwright.sync_api import sync_playwright
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
H = pathlib.Path(__file__).resolve().parent.parent
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 700}, device_scale_factor=2)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://%s/index.html' % H); pg.wait_for_timeout(800)
    pg.screenshot(path=str(out / 'j0_start.png'))
    def wait():
        pg.wait_for_function('!busy', timeout=30000); pg.wait_for_timeout(300)
    pg.click('.hit[data-id=M02]'); pg.wait_for_timeout(1100); pg.screenshot(path=str(out / 'j1_M02_walking.png')); wait(); pg.screenshot(path=str(out / 'j2_M02_arrived.png'))
    pg.click('.hit[data-id=M07]'); pg.wait_for_timeout(1000); pg.screenshot(path=str(out / 'j3_to_M07_a.png')); pg.wait_for_timeout(1800); pg.screenshot(path=str(out / 'j4_to_M07_b.png')); wait(); pg.screenshot(path=str(out / 'j5_M07_arrived.png'))
    print('here', pg.evaluate('here'), 'errors', errs)
    b.close()
