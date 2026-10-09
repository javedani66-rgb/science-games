#!/usr/bin/env python3
"""سنجش پیکسلی بنا/آب برای ۱۲ بنا در سه نور (Playwright). پیکسل‌های «بدنه» = غیر از آب، غیر از خط دور (دور ≤40)، بدون سایهٔ ریخته.
خروجی light_render_check.md/json. معیار: میانهٔ بدنه ÷ آب ≥3  (و صدک ۲۵ برای اطلاع)."""
import json, os, sys, io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageFilter
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, '..', 'assets')
T = json.load(open(os.path.join(A, 'light', 'zone_tokens.json'))); L = T['lights']
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def lin(v): v /= 255; return v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
def Y(c): r, g, b = map(lin, c[:3]); return .2126 * r + .7152 * g + .0722 * b
def cr(a, b): ya, yb = Y(a), Y(b); return (max(ya, yb) + .05) / (min(ya, yb) + .05)
def dist(a, b): return sum((x - y) ** 2 for x, y in zip(a[:3], b[:3])) ** .5
base = 'file://' + os.path.join(A, 'light', 'light_layers_demo.html')
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 800}, device_scale_factor=2)
    pg.goto(base)
    pg.add_style_tag(content='[id$="_shadow"]{display:none!important} section{background:var(--l-water)!important}')
    for l in ('day', 'dusk', 'night'):
        wat = rgb(L[l]['water']); line = rgb(L[l]['line'])
        cells = pg.locator(f'section[data-light="{l}"] .c')
        for i in range(12):
            img = Image.open(io.BytesIO(cells.nth(i).screenshot())).convert('RGB')
            arr = np.asarray(img).astype(float)
            isbg = np.sqrt(((arr - np.array(wat)) ** 2).sum(2)) < 14
            m = Image.fromarray((~isbg * 255).astype('uint8')); er = np.asarray(m.filter(ImageFilter.MinFilter(9))) > 0   # داخل بنا
            edge = (~isbg) & (~er) & (np.sqrt(((arr - np.array(line)) ** 2).sum(2)) < 30)        # حلقهٔ ~4px بیرونی سیلوئت (روی 2x)
            body = (~isbg) & (np.sqrt(((arr - np.array(line)) ** 2).sum(2)) >= 40)
            def Yv(a): 
                f = np.where(a / 255 <= .03928, a / 255 / 12.92, ((a / 255 + .055) / 1.055) ** 2.4); return .2126 * f[..., 0] + .7152 * f[..., 1] + .0722 * f[..., 2]
            yv = Yv(arr); yw = Y(wat)
            ratio = lambda y: (np.maximum(y, yw) + .05) / (np.minimum(y, yw) + .05)
            ee = np.median(ratio(yv[edge])) if edge.any() else 0; bb = np.median(ratio(yv[body])) if body.any() else 0
            res.setdefault(l, {})[i + 1] = dict(edge=round(float(ee), 2), body=round(float(bb), 2), edge_p25=round(float(np.percentile(ratio(yv[edge]), 25)), 2))
    b.close()
json.dump(res, open(os.path.join(H, 'light_render_check.json'), 'w'), indent=1)
m = ['# بنا/آب روی خروجی واقعی env (پیکسلی)\n', 'لبهٔ سیلوئت = حلقهٔ بیرونی ≈2px پیکسل‌های بنا که به آب می‌چسبد؛ معیار: میانهٔ لبه ÷ آب ≥3 (همین چیزی است که چشم برای جدا کردن بنا از آب می‌بیند). «بدنه» = میانهٔ پیکسل‌های داخل (اطلاع، چون بدنهٔ میان‌روشن با آب میان‌روشن ممکن است ≈1 باشد). فقط روشنایی.\n', '| بنا | لبه روز | لبه غروب | لبه شب | بدنه روز | بدنه غروب | بدنه شب |', '|---|---|---|---|---|---|---|']
red = 0
for i in range(1, 13):
    r = [res[l][i] for l in ('day', 'dusk', 'night')]; c = []
    for x in r:
        ok = x['edge'] >= 3; red += (not ok); c.append(str(x['edge']) + ('' if ok else ' **قرمز**'))
    m.append(f'| node_{i:02d} | ' + ' | '.join(c) + ' | ' + ' | '.join(str(x['body']) for x in r) + ' |')
m.append(f'\nردیف قرمز: {red}')
open(os.path.join(H, 'light_render_check.md'), 'w').write('\n'.join(m) + '\n'); print(open(os.path.join(H, 'light_render_check.md')).read())
