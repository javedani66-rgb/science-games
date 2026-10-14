#!/usr/bin/env python3
"""عکس مقایسهٔ «v4 | جدید» برای نمای جلو/پشت/قفسه در 390×800 و 360×640 + خاکستری؛ و «قبل (دور ۱) | جدید» برای سه هنر و دو صحنه."""
import pathlib
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / 'assets_r2/card'; SH = OUT / 'shots'; OLD = HERE.parent / 'assets/card/shots'
V4 = HERE.parents[2] / 'v4/style/card-night.html'
pairs = [('front', 'front', 'stack'), ('back', 'back', 'back'), ('shelf', 'shelf', 'shelf')]
def side(a, b, path, gap=16):
    h = max(a.height, b.height); W = Image.new('RGB', (a.width + b.width + gap, h), '#888')
    W.paste(a, (0, 0)); W.paste(b, (a.width + gap, 0)); W.save(path)
    W.convert('L').save(str(path).replace('.png', '_gray.png'))
with sync_playwright() as p:
    b = p.chromium.launch()
    for (name, v4v, newv) in pairs:
        pg = b.new_page(viewport={'width': 390, 'height': 800}); pg.goto(V4.as_uri() + '?v=' + v4v); pg.wait_for_timeout(500)
        pg.screenshot(path=str(SH / f'_v4_{name}.png')); pg.close()
    b.close()
for (name, v4v, newv) in pairs:
    v4 = Image.open(SH / f'_v4_{name}.png').convert('RGB')
    side(v4, Image.open(SH / f'card_{newv}_390x800.png').convert('RGB'), SH / f'cmp_{name}_390x800.png')
    v4s = v4.resize((round(390 * 640 / 800), 640), Image.LANCZOS)   # v4 فقط در 390×800 ساخته شده؛ برای 360×640 کوچک می‌شود
    side(v4s, Image.open(SH / f'card_{newv}_360x640.png').convert('RGB'), SH / f'cmp_{name}_360x640.png')
    (SH / f'_v4_{name}.png').unlink()
# هنرها و صحنه‌ها: دور ۱ | دور ۲
def stack(imgs):
    W = Image.new('RGB', (imgs[0].width, sum(i.height for i in imgs) + 6 * (len(imgs) - 1)), '#888'); y = 0
    for i in imgs: W.paste(i, (0, y)); y += i.height + 6
    return W
old = stack([Image.open(OLD / f'art_{k}.png').convert('RGB') for k in ('day', 'dusk', 'night')])
new = stack([Image.open(SH / f'art_{k}.png').convert('RGB') for k in ('day', 'dusk', 'night')])
side(old, new, SH / 'cmp_art_old_new.png')
for s in ('orange-dusk', 'red-night', 'green'):
    o = Image.open(OLD / f'card_harbor-scene-{s}_390x800.png').convert('RGB').crop((0, 0, 390, 530)); n = Image.open(SH / f'card_harbor-scene-{s}_390x800.png').convert('RGB').crop((0, 0, 390, 530))
    side(o, n, SH / f'cmp_scene_{s}_old_new.png')
print('ok')
