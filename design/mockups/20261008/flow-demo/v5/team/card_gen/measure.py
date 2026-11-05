#!/usr/bin/env python3
"""سنجش سطح گرم (رنگ‌مایه 340..50، اشباع>0.5) در سه هنر کارت، ناحیهٔ کامل 360×240 و ناحیهٔ امن؛ و فهرست ضخامت‌های خط. خروجی: card/measure_card.md"""
import pathlib, re, colorsys, sys
from playwright.sync_api import sync_playwright
from PIL import Image
OUT = pathlib.Path(__file__).resolve().parent.parent / 'assets/card'
rows = []; widths = {}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 360, 'height': 240})
    for k in ('day', 'dusk', 'night'):
        f = OUT / f'art_harbor_{k}.svg'
        pg.set_content(f'<body style="margin:0">{f.read_text()}</body>'); pg.wait_for_timeout(100)
        png = OUT / 'shots' / f'art_{k}.png'; pg.screenshot(path=str(png))
        im = Image.open(png).convert('RGB')
        def warm(box, mode):
            c = t = 0
            for x in range(box[0], box[2]):
                for y in range(box[1], box[3]):
                    r, g_, bl = [v / 255 for v in im.getpixel((x, y))]
                    h, s, v = colorsys.rgb_to_hsv(r, g_, bl); hh, l, ss = colorsys.rgb_to_hls(r, g_, bl)
                    sat = s if mode == 'hsv' else ss
                    d = h * 360; t += 1
                    if (d >= 340 or d <= 50) and sat > .5: c += 1
            return 100 * c / t
        rows.append((k, warm((0, 0, 360, 240), 'hsv'), warm((0, 0, 360, 240), 'hsl'), warm((20, 45, 340, 195), 'hsv'), warm((20, 45, 340, 195), 'hsl')))
    b.close()
for f in list(OUT.glob('*.svg')) + list((OUT / 'scene').glob('*.svg')):
    if f.name == 'sprite_card.svg': continue
    for w in re.findall(r'stroke-width="([\d.]+)"', f.read_text()): widths[w] = widths.get(w, 0) + 1
md = '# سنجش کارت (card-artist، خودکار؛ واقعیت فنی، نه ادعای کودک)\n\n## سطح گرم (رنگ‌مایه 340..50 و اشباع>0.5؛ سقف ۱۵٪)\n| هنر | کل HSV | کل HSL | ناحیهٔ امن HSV | ناحیهٔ امن HSL |\n|---|---|---|---|---|\n'
for r in rows: md += f'| {r[0]} | {r[1]:.1f}% | {r[2]:.1f}% | {r[3]:.1f}% | {r[4]:.1f}% |\n'
md += '\n## ضخامت‌های stroke-width در فایل‌های جدا (مقدار: تعداد)\n' + ', '.join(f'{k}: {v}' for k, v in sorted(widths.items(), key=lambda kv: float(kv[0]))) + '\n'
(OUT / 'measure_card.md').write_text(md, encoding='utf-8'); print(md)
