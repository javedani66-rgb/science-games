#!/usr/bin/env python3
"""ماکت صفحهٔ ورود به بازی: index.html (خودبسنده) و artifact.html (بدون پوستهٔ سند) را می‌سازد.
متن‌ها فقط از strings.fa.json (بانک متن، B49/B50)؛ یادداشت بازبین از review.fa.json (در بانک نیست).
هنر: فقط نماد مرحله (از ماکت نقشه) روی زمینهٔ شبِ منو؛ حرکت رسیدنش همان کد ماکت نقشه است. مخفی‌گاه در ورود نیست (D188)."""
import json, base64, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def main():
    strings = json.load(open(HERE / 'strings.fa.json', encoding='utf-8'))
    review = json.load(open(HERE / 'review.fa.json', encoding='utf-8'))
    MT = HERE.parent / 'map-travel'
    SYMS = ''.join((MT / 'etudes/stations/out' / ('node_%s.svg' % n)).read_text(encoding='utf-8') for n in ('football', 'ice_rink', 'shipyard'))   # نمادهای نقشه
    mt = (MT / 'template.html').read_text(encoding='utf-8')
    END = 'const IT=3;let STA=[];function return_(a){if(a)STA.push(a)}'
    ANIM = mt[mt.index('function Lh(g,n)'):mt.index(END) + len(END)]   # حرکت رسیدن ایستگاه‌ها: یک منبع (ماکت نقشه)
    import shutil
    for n in ('index', 'cardbox'): shutil.copyfile(MT / (n + '.html'), HERE / ('map.html' if n == 'index' else 'cardbox.html'))   # مقصد «شروع/ادامه» (گیت‌نشده)
    f = lambda p: base64.b64encode(open(ROOT / 'assets/fonts' / p, 'rb').read()).decode()
    t = open(HERE / 'template.html', encoding='utf-8').read()
    for k, v in dict(FONT_VR=f('Vazirmatn-Regular.woff2'), FONT_VB=f('Vazirmatn-Bold.woff2'), FONT_L=f('Lalezar-Regular.woff2'),
                     STRINGS=json.dumps(strings, ensure_ascii=False), REVIEW=json.dumps(review, ensure_ascii=False),
                     SYMS=SYMS, ANIM=ANIM).items():
        t = t.replace('{{%s}}' % k, v)
    (HERE / 'index.html').write_text(t, encoding='utf-8')
    a = re.sub(r'<!doctype html>\s*<html[^>]*>\s*<head>\s*<meta[^>]*>\s*<meta[^>]*>\s*', '', t, count=1, flags=re.I)
    a = a.replace('</head>\n<body>', '<div id="root" dir="rtl" lang="fa">', 1).replace('</body>\n</html>', '</div>', 1)
    (HERE / 'artifact.html').write_text(a, encoding='utf-8')
    print('index.html', len(t) // 1024, 'KB; artifact.html', len(a) // 1024, 'KB')


if __name__ == '__main__':
    main()
