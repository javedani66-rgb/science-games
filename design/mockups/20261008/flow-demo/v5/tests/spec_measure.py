#!/usr/bin/env python3
"""سنجش واقعی (با پیکسل) نسبت کنتراست متن به پس‌زمینه با احتساب سایه.

چرا: سایه را نمی‌شود با فرمول ساده حساب کرد. پس هر جفت را در Chromium نقاشی می‌کنیم (با همان فونت و اندازه و سایه) و دو تصویر می‌گیریم:
  A) فقط متن (بدون سایه) روی پر  ← شکل حروف
  B) فقط سایه (متن شفاف)         ← آنچه دور حروف دیده می‌شود
حلقهٔ ۲ پیکسلی بیرون حروف را از B برمی‌داریم؛ نسبت متن به هر پیکسل حلقه را حساب می‌کنیم و صدک پنجم (بدترین ۵٪) را برمی‌گردانیم.
اگر سایه نباشد حلقه همان پر است و عدد برابر نسبت متن به پر می‌شود.

استفاده:  from spec_measure import measure ;  measure([case, ...]) -> {key: {'p05':..,'mean':..}}
case = dict(key, fill, text, shadow=None|'#hex', layers=[[dx,dy],...], family, size, weight, stroke=None|(px,'#hex'))"""
import pathlib, base64
import numpy as np
from PIL import Image, ImageFilter
import io

V5 = pathlib.Path(__file__).resolve().parents[1]
ROOT = V5.parents[4]
EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
DPR = 3
SAMPLE = 'برویم به این محیط ۱۲۳ پایهٔ کارت'
CELL_W, CELL_H = 520, 84
BATCH = 36


def _lum_arr(a):
    c = a.astype(np.float64) / 255
    c = np.where(c <= .03928, c / 12.92, ((c + .055) / 1.055) ** 2.4)
    return .2126 * c[..., 0] + .7152 * c[..., 1] + .0722 * c[..., 2]


def _rgb(h):
    h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.uint8)


def _shadow_css(c):
    if not c.get('shadow'): return 'none'
    s = c['shadow']
    return ','.join(f'{dx}px {dy}px 0 {s}' for dx, dy in c['layers'])


def _page(cases):
    fonts = ''.join(f"@font-face{{font-family:'{n}';font-weight:{w};src:url(file://{ROOT}/assets/fonts/{f}) format('woff2')}}" for n, w, f in
                    (('Vazirmatn', 400, 'Vazirmatn-Regular.woff2'), ('Vazirmatn', 700, 'Vazirmatn-Bold.woff2'), ('Lalezar', 400, 'Lalezar-Regular.woff2')))
    cells = []
    for i, c in enumerate(cases):
        st = f'background:{c["fill"]};font-family:\'{c["family"]}\';font-weight:{c["weight"]};font-size:{c["size"]}px;'
        stroke = ''
        if c.get('stroke'):
            stroke = f'-webkit-text-stroke:{c["stroke"][0]}px {c["stroke"][1]};paint-order:stroke fill;stroke-linejoin:round;'
        cells.append(f'<div class="cell" style="{st}"><span class="t" data-i="{i}" style="color:{c["text"]};text-shadow:{_shadow_css(c)};{stroke}">{SAMPLE}</span></div>')
    css = (f'{fonts}html,body{{margin:0;background:#000;direction:rtl}}.cell{{width:{CELL_W}px;height:{CELL_H}px;display:flex;align-items:center;justify-content:center;line-height:1.3}}'
           'body.B .t{color:transparent !important}body.A .t{text-shadow:none !important;-webkit-text-stroke:0 !important}')
    return f'<!doctype html><meta charset="utf-8"><style>{css}</style><body class="A">{"".join(cells)}</body>'


def measure(cases, ring_px=2, percentile=5):
    from playwright.sync_api import sync_playwright
    out = {}
    tmp = V5 / 'spec' / '_measure_tmp.html'
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=['--no-sandbox'])
        pg = b.new_page(viewport={'width': CELL_W, 'height': CELL_H * 4}, device_scale_factor=DPR)
        for s in range(0, len(cases), BATCH):
            chunk = cases[s:s + BATCH]
            tmp.write_text(_page(chunk), encoding='utf-8')
            pg.goto('file://' + str(tmp)); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(250)
            imgs = {}
            for cls in ('A', 'B'):
                pg.evaluate(f"document.body.className='{cls}'")
                imgs[cls] = np.array(Image.open(io.BytesIO(pg.screenshot(full_page=True))).convert('RGB'))
            for i, c in enumerate(chunk):
                y0, y1 = i * CELL_H * DPR, (i + 1) * CELL_H * DPR
                A, B = imgs['A'][y0:y1], imgs['B'][y0:y1]
                fill = _rgb(c['fill']); txt = _rgb(c['text'])
                glyph = (np.abs(A.astype(int) - fill.astype(int)).max(axis=2) > 3)
                if glyph.sum() < 50:
                    out[c['key']] = {'p05': 0.0, 'mean': 0.0, 'error': 'no glyph pixels'}; continue
                m = Image.fromarray((glyph * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * int(round(ring_px * DPR)) + 1))
                ring = (np.array(m) > 0) & ~glyph
                # حاشیهٔ خود سلول را کنار بگذار
                ring[:6, :] = ring[-6:, :] = False; ring[:, :6] = ring[:, -6:] = False
                lt = _lum_arr(txt[None, None, :])[0, 0]
                lp = _lum_arr(B[ring])
                hi, lo = np.maximum(lt, lp), np.minimum(lt, lp)
                ratio = (hi + .05) / (lo + .05)
                out[c['key']] = {'p05': float(np.percentile(ratio, percentile)), 'mean': float(ratio.mean()), 'n': int(ring.sum())}
        b.close()
    try: tmp.unlink()
    except OSError: pass
    return out


if __name__ == '__main__':
    r = measure([dict(key='x', fill='#0d9c87', text='#ffffff', shadow='#06270c', layers=[[0, 3], [2, 0], [-2, 0], [0, -1.5]], family='Lalezar', size=24, weight=400),
                 dict(key='y', fill='#46f0d8', text='#ffffff', shadow=None, layers=[], family='Lalezar', size=24, weight=400)])
    print(r)
