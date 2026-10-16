#!/usr/bin/env python3
"""ماکت منوی انتخاب کاراکتر و رنگ: index.html (خودبسنده) و artifact.html (بدون پوستهٔ سند، برای انتشار) را می‌سازد.
متن‌ها فقط از strings.fa.json (بانک متن، B49/B50)؛ یادداشت بازبین از review.fa.json (در بانک نیست).
برش‌های بدون پس‌زمینه: ../../../characters/tools/make_cutouts.py (کش در _cache/، گیت‌نشده)."""
import json, base64, io, pathlib, importlib.util, re
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
spec = importlib.util.spec_from_file_location('mk', ROOT / 'design/characters/tools/make_cutouts.py')
mk = importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
CACHE = HERE / '_cache'
NAMES, OUTFITS = mk.NAMES, mk.OUTFITS


def ensure_cache():
    for o in OUTFITS:
        (CACHE / o).mkdir(parents=True, exist_ok=True)
        for n in NAMES:
            p = CACHE / o / f'{n}.webp'
            if not p.exists():
                mk.cutout(mk.src_path(o, n), 420).save(p, quality=80, method=6)


def enc(im, q=78):
    b = io.BytesIO(); im.save(b, 'WEBP', quality=q, method=3)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()


def scaled(im, h):
    return im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)


def images():
    ensure_cache()
    load = lambda o, n: Image.open(CACHE / o / f'{n}.webp').convert('RGBA')
    out = dict(head={}, big={}, thumbc={}, thumb={}, mini={})
    for n in NAMES:
        b = load('base', n)
        out['head'][n] = enc(scaled(b.crop((0, 0, b.width, round(b.height * .36))), 190))
        out['mini'][n] = enc(scaled(b, 180))
        out['big'][n] = {o: enc(load(o, n), 80) for o in OUTFITS}
        out['thumbc'][n] = {o: enc(scaled(load(o, n), 150)) for o in OUTFITS}
    out['thumb'] = out['thumbc']['nima']
    return out


def main():
    strings = json.load(open(HERE / 'strings.fa.json', encoding='utf-8'))
    review = json.load(open(HERE / 'review.fa.json', encoding='utf-8'))
    f = lambda p: base64.b64encode(open(ROOT / 'assets/fonts' / p, 'rb').read()).decode()
    t = open(HERE / 'template.html', encoding='utf-8').read()
    for k, v in dict(FONT_VR=f('Vazirmatn-Regular.woff2'), FONT_VB=f('Vazirmatn-Bold.woff2'), FONT_L=f('Lalezar-Regular.woff2'),
                     STRINGS=json.dumps(strings, ensure_ascii=False), REVIEW=json.dumps(review, ensure_ascii=False),
                     IMAGES=json.dumps(images(), ensure_ascii=False)).items():
        t = t.replace('{{%s}}' % k, v)
    (HERE / 'index.html').write_text(t, encoding='utf-8')
    # نسخهٔ انتشار: پوستهٔ سند را خود Artifact می‌سازد؛ جهت راست‌به‌چپ با اسکریپت و پوشش
    a = re.sub(r'<!doctype html>\s*<html[^>]*>\s*<head>\s*<meta[^>]*>\s*<meta[^>]*>\s*', '', t, count=1, flags=re.I)
    a = a.replace('</head>\n<body>', '<div id="root" dir="rtl" lang="fa">', 1).replace('</body>\n</html>', '</div>', 1)
    a = a.replace("const S=", "document.documentElement.setAttribute('dir','rtl');document.documentElement.setAttribute('lang','fa');\nconst S=", 1)
    (HERE / 'artifact.html').write_text(a, encoding='utf-8')
    print('index.html', len(t) // 1024, 'KB; artifact.html', len(a) // 1024, 'KB')


if __name__ == '__main__':
    main()
