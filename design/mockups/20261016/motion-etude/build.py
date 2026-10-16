#!/usr/bin/env python3
"""ماکت حرکت اسکله و تلوتلوی عروسکی (B68/D83): index.html و artifact.html. متن‌ها فقط از strings.fa.json (B49/B50).
شخصیت‌ها: کش برش‌ها در ../character-menu/_cache (ساخت با ../character-menu/build.py)."""
import json, base64, io, pathlib, re
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CACHE = HERE.parent / 'character-menu/_cache/sailor'
NAMES = ['nima', 'roya', 'sam', 'tara', 'goli', 'mani']

def enc(im, q=80):
    b = io.BytesIO(); im.save(b, 'WEBP', quality=q, method=4)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()

def scaled(im, h):
    return im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)

SPRITE = ROOT / 'design/mockups/20261008/flow-demo/v5/team/assets_r2/env/sprite_env.svg'
SYMS = ['node_10', 'node_12', 'env_dec_city_sail', 'env_dec_city_lighthouse', 'env_dec_city_buoy', 'env_dec_city_crate', 'env_dec_city_islet']

def sprite():
    # فقط نمادهای لازم از همان دارایی‌های نقشه (v5 r2b)؛ سبک و فیلتر از همان فایل
    s = SPRITE.read_text(encoding='utf-8')
    style = re.search(r'<style>.*?</style>', s, re.S).group(0)
    syms = ''.join(re.search(r'<symbol id="%s".*?</symbol>' % i, s, re.S).group(0) for i in SYMS)
    return '<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true"><defs>%s</defs>%s</svg>' % (style, syms)

def main():
    strings = json.load(open(HERE / 'strings.fa.json', encoding='utf-8'))
    review = json.load(open(HERE / 'review.fa.json', encoding='utf-8'))
    ims = {}
    for n in NAMES:
        im = Image.open(CACHE / f'{n}.webp').convert('RGBA')
        ims[n] = dict(big=enc(scaled(im, 260)), thumb=enc(scaled(im, 110), 75))
    f = lambda p: base64.b64encode(open(ROOT / 'assets/fonts' / p, 'rb').read()).decode()
    t = open(HERE / 'template.html', encoding='utf-8').read()
    for k, v in dict(FONT_VR=f('Vazirmatn-Regular.woff2'), FONT_VB=f('Vazirmatn-Bold.woff2'), FONT_L=f('Lalezar-Regular.woff2'),
                     STRINGS=json.dumps(strings, ensure_ascii=False), REVIEW=json.dumps(review, ensure_ascii=False),
                     IMAGES=json.dumps(ims, ensure_ascii=False), NAMES=json.dumps(NAMES), SPRITE=sprite()).items():
        t = t.replace('{{%s}}' % k, v)
    (HERE / 'index.html').write_text(t, encoding='utf-8')
    a = re.sub(r'<!doctype html>\s*<html[^>]*>\s*<head>\s*<meta[^>]*>\s*<meta[^>]*>\s*', '', t, count=1, flags=re.I)
    a = a.replace('</head>\n<body>', '<div id="root" dir="rtl" lang="fa">', 1).replace('</body>\n</html>', '</div>', 1)
    a = a.replace("const S=", "document.documentElement.setAttribute('dir','rtl');document.documentElement.setAttribute('lang','fa');\nconst S=", 1)
    (HERE / 'artifact.html').write_text(a, encoding='utf-8')
    print('index.html', len(t) // 1024, 'KB; artifact.html', len(a) // 1024, 'KB')

if __name__ == '__main__':
    main()
