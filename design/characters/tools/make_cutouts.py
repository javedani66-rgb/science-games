#!/usr/bin/env python3
"""برش بدون پس‌زمینهٔ کاراکترها برای ماکت‌ها (فقط مشتق؛ اصل‌ها دست‌نخورده می‌مانند).

ورودی: design/characters/gemini-20261015/{base-standing,outfits/<لباس>}/<نام>.jpg
خروجی: پوشهٔ داده‌شده/<لباس>/<نام>.webp (پس‌زمینهٔ سفید شفاف، برش به لبهٔ کاراکتر، ارتفاع ثابت)

روش: سفیدِ متصل به لبهٔ تصویر شفاف می‌شود (flood fill از چهار گوشه)؛ سفیدِ داخل خط‌های بسته (لباس فضانوردی، دندان) می‌ماند.
محدودیت: اگر خطِ دور جایی باز باشد، پس‌زمینه به داخل نشت می‌کند؛ خروجی باید با چشم دیده شود.
استفاده: python3 design/characters/tools/make_cutouts.py <پوشهٔ خروجی> [ارتفاع=420]
"""
import sys, pathlib
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

ROOT = pathlib.Path(__file__).resolve().parents[3]
SRC = ROOT / 'design/characters/gemini-20261015'
NAMES = ['nima', 'roya', 'sam', 'tara', 'mani', 'goli']
OUTFITS = ['base', 'sports', 'winter', 'astronaut', 'farmer', 'construction', 'carpenter', 'sailor']


def src_path(outfit, name):
    d = SRC / 'base-standing' if outfit == 'base' else SRC / 'outfits' / outfit
    return d / f'{name}.jpg'


def cutout(path, height):
    im = Image.open(path).convert('RGB')
    if im.height > 1100:  # برای سرعت: برش از روی نسخهٔ کوچک‌شده (خروجی نهایی ۴۲۰px است)
        im = im.resize((round(im.width * 1100 / im.height), 1100), Image.LANCZOS)
    a = np.asarray(im).astype(np.int16)
    # «تقریباً سفید» = پس‌زمینه (کاغذ کمی کرم/خاکستری روشن هم می‌گیرد)
    near_white = (a.min(axis=2) >= 232) & ((a.max(axis=2) - a.min(axis=2)) <= 22)
    lab, n = ndi.label(near_white)
    h, w = near_white.shape
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge))
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    # لبهٔ نرم: یک پیکسل فرسایش + محو کم تا هالهٔ سفید نماند
    alpha_img = Image.fromarray(alpha).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    rgba = im.copy(); rgba.putalpha(alpha_img)
    bbox = alpha_img.point(lambda v: 255 if v > 40 else 0).getbbox()
    rgba = rgba.crop(bbox)
    r = height / rgba.height
    return rgba.resize((max(1, round(rgba.width * r)), height), Image.LANCZOS)


def main():
    out = pathlib.Path(sys.argv[1]); height = int(sys.argv[2]) if len(sys.argv) > 2 else 420
    for o in OUTFITS:
        (out / o).mkdir(parents=True, exist_ok=True)
        for n in NAMES:
            p = src_path(o, n)
            if not p.exists():
                print('نیست:', p); continue
            cutout(p, height).save(out / o / f'{n}.webp', quality=82, method=6)
    print('تمام شد:', out)


if __name__ == '__main__':
    main()
