#!/usr/bin/env python3
"""عکس مقایسهٔ «v4 | جدید» در ۳۹۰×۸۰۰ برای ۳ بخش (بالا، میانه، پایین) + خاکستری. اجرا پس از sheet.py"""
import pathlib, io, sys
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
import layout as L
OUT = L.OUT; SH = OUT / 'shots'; SH.mkdir(exist_ok=True)
V4 = L.HERE.parents[2] / 'v4' / 'style' / 'map.html'
sections = [('y0', 0, 0), ('mid', 1450, 3780), ('bottom', 1600, L.H - 800)]       # (نام, y در v4, y در جدید)
def shot(pg, url, W=390, Hh=800):
    pg.goto(url); pg.wait_for_timeout(500); return Image.open(io.BytesIO(pg.screenshot()))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 390, 'height': 800}); res = {}
    for name, y4, yn in sections:
        pg.goto('file://%s?y=%d' % (V4, y4)); pg.add_style_tag(content='#bar{display:none!important}'); pg.wait_for_timeout(500)
        a = Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
        c = shot(pg, 'file://%s?y=%d' % (OUT / 'env_sheet.html', yn)).convert('RGB'); res[name] = (a, c)
    b.close()
def label(im, t):
    d = ImageDraw.Draw(im); d.rectangle([0, 0, 60, 18], fill=(16, 8, 58)); d.text((4, 3), t, fill=(255, 243, 196))
for name, (a, c) in res.items():
    im = Image.new('RGB', (790, 800), (255, 255, 255)); im.paste(a, (0, 0)); im.paste(c, (400, 0)); label(im, 'v4'); d = ImageDraw.Draw(im); d.rectangle([400, 0, 460, 18], fill=(16, 8, 58)); d.text((404, 3), 'new', fill=(255, 243, 196))
    im.save(SH / ('cmp_%s.png' % name))
g = Image.new('RGB', (790 * 3 // 1, 800), (255, 255, 255))
rows = Image.new('RGB', (1190, 1610), (255, 255, 255))
for i, (name, (a, c)) in enumerate(res.items()):
    rows.paste(a.convert('L').convert('RGB'), (i * 400, 0)); rows.paste(c.convert('L').convert('RGB'), (i * 400, 810))
d = ImageDraw.Draw(rows); d.text((4, 4), 'gray: top row v4, bottom row new (y0 | mid | bottom)', fill=(255, 0, 0))
rows.save(SH / 'cmp_gray.png'); print('ok')
