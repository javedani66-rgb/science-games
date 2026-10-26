#!/usr/bin/env python3
"""پانورامای ورود: برشی از همین نقشهٔ روز (ورودی «شروع»، ورزشگاه، جادهٔ آغاز) بدون راهنما، تیک و ردپا → pano.jpg
نیاز: Playwright + ماکت نقشه (../map-travel/index.html). خروجی در گیت است (حدود ۱۵۰ کیلوبایت)."""
import pathlib
from playwright.sync_api import sync_playwright
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent
U = (HERE.parent / 'map-travel' / 'index.html').as_uri()
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 900}, device_scale_factor=2)
    pg.goto(U); pg.wait_for_timeout(2000)
    pg.evaluate("""()=>{visited.clear();done.clear();ORDER.filter(i=>NODES[i].y>=1200).forEach(i=>visited.add(i));here='F01';putAt(here);updateTrail();showPrints(false);
      for(const id of ['fig','boat','bar','rv','blk','dv']){const e=document.getElementById(id);if(e)e.style.display='none'}
      const r=document.getElementById('ringG');if(r)r.remove();document.querySelectorAll('.node .lbl,#dnlayer').forEach(e=>{if(e.id==='dnlayer')e.style.display='none'});
      sc.scrollTop=sc.scrollHeight}""")
    pg.wait_for_timeout(900)
    box = pg.locator('#sc').bounding_box()
    pg.screenshot(path=str(HERE / '_pano_full.png'), clip=box)
    b.close()
im = Image.open(HERE / '_pano_full.png').convert('RGB')
im.crop((0, 1300, 780, 1740)).save(HERE / 'pano.jpg', quality=84, optimize=True)   # دروازهٔ «شروع» + جادهٔ آغاز + برچسب «ورزشگاه»
(HERE / '_pano_full.png').unlink(); print('pano.jpg', (HERE / 'pano.jpg').stat().st_size // 1024, 'KB')
