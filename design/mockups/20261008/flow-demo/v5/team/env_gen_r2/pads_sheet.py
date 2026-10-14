#!/usr/bin/env python3
"""شیت پایه‌ها: ۴ زمین × ۸ شکل. اجرا پس از gen_env.py → assets_r2/env/shots/pads.png"""
import layout as L
from playwright.sync_api import sync_playwright
OUT = L.OUT; sp = (OUT / 'sprite_env.svg').read_text(encoding='utf-8')
from shapes import SHAPES
bg = {'sports': '#3f9a2b', 'space': '#c4502f', 'farm': '#9a8a10', 'city': '#075a73'}
h = '<body style="margin:0;font:12px sans-serif"><div style="position:absolute;width:0;height:0;overflow:hidden">%s</div>' % sp
for z in bg:
    h += '<div style="display:flex;background:%s">' % bg[z] + ''.join('<svg width="120" height="100"><use href="#env_pad_%s_%s" width="120" height="100"/><use href="#prop_%02d" width="120" height="100"/></svg>' % (z, s, 1 + i * 2) for i, s in enumerate(SHAPES)) + '</div>'
(OUT / 'shots').mkdir(exist_ok=True); open('/tmp/claude-0/-home-claude-science-games/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/pads.html', 'w').write(h)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox']); pg = b.new_page(viewport={'width': 960, 'height': 400}); pg.goto('file:///tmp/claude-0/-home-claude-science-games/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/pads.html'); pg.wait_for_timeout(300); pg.screenshot(path=str(OUT / 'shots' / 'pads.png')); b.close()
