#!/usr/bin/env python3
"""اتود خط ضخیم روی نیما (۱۶ اکتبر): سه حالت در اندازه‌های کوچک. رنگ خط #241a5e.
ستون‌ها: اصلی | فقط دورگیری بیرونی | دورگیری بیرونی + ضخیم‌کردن خط‌های داخل. خروجی: sheet.png"""
import sys, pathlib, numpy as np
from PIL import Image, ImageFilter, ImageChops
ROOT = pathlib.Path(__file__).resolve().parents[4]
NAVY = (36, 26, 94)
src = Image.open(ROOT / 'design/mockups/20261016/character-menu/_cache/base/nima.webp').convert('RGBA')
BG = (127, 191, 74)  # سبز نقشه
def at(h): return src.resize((round(src.width * h / src.height), h), Image.LANCZOS)
def outer(im, t):
    a = im.getchannel('A').point(lambda v: 255 if v > 90 else 0)
    big = a.filter(ImageFilter.MaxFilter(2 * t + 1))
    base = Image.new('RGBA', im.size, NAVY + (0,)); base.putalpha(big)
    base.alpha_composite(im); return base
def inner(im, k):
    rgb = im.convert('RGB'); a = im.getchannel('A')
    lum = np.asarray(rgb.convert('L')).astype(int)
    dark = Image.fromarray(((lum < 50) * 255).astype('uint8')).filter(ImageFilter.MaxFilter(k))
    out = np.asarray(rgb).copy(); d = np.asarray(dark) > 0
    out[d & (np.asarray(a) > 90)] = NAVY
    o = Image.fromarray(out).convert('RGBA'); o.putalpha(a); return o
rows = [(64, 2, 3), (96, 2, 3), (140, 3, 3), (200, 3, 3)]
pad = 12; W = 3 * 200 + 4 * pad; H = sum(h + 2 * pad for h, _, _ in rows)
sheet = Image.new('RGB', (W, H), BG); y = 0
for h, t, k in rows:
    im = at(h); v = [im, outer(im, t), outer(inner(im, k), t)]
    for c, x in enumerate(v):
        bgc = Image.new('RGBA', x.size, BG + (255,)); bgc.alpha_composite(x)
        sheet.paste(bgc.convert('RGB'), (pad + c * (200 + pad), y + pad))
    y += h + 2 * pad
sheet = sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST)  # بزرگ‌نمایی فقط برای دیدن
sheet.save(pathlib.Path(__file__).parent / 'sheet.png'); print(sheet.size)
