#!/usr/bin/env python3
"""ماکت «نقشهٔ کلی تخت» (D192): index.html (خودبسنده) و artifact.html.
۳۴ خانه، یکی برای هر ایستگاه نقشهٔ بلند، به همان ترتیب؛ نمادها همان نمادهای نقشه (etudes/stations/out).
متن‌ها فقط از strings.fa.json (بانک متن، B49/B50)؛ یادداشت بازبین از review.fa.json."""
import json, base64, io, pathlib, re, importlib.util
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
MT = HERE.parent / 'map-travel'
CACHE = HERE.parent / 'character-menu' / '_cache'
LANDS = [('sports', 8, '#3f9a2b', 'sports'), ('space', 5, '#c4502f', 'astronaut'), ('farm', 3, '#9a8a10', 'farmer'),
         ('city', 12, '#c9a35c', 'construction'), ('sea', 6, '#165f77', 'sailor')]   # رنگ زمین هر سرزمین = همان رنگ نقشهٔ بلند (نمونه‌برداری از تصویر)


def main():
    spec = importlib.util.spec_from_file_location('mtb', MT / 'build.py'); mtb = importlib.util.module_from_spec(spec); spec.loader.exec_module(mtb)
    sym_of = {nid: sid for sid, nid in mtb.KIT_NODES.items()}
    mi = (MT / 'index.html').read_text(encoding='utf-8')
    nodes = json.loads(re.search(r'const NODES=(\{.*?\});', mi, re.S).group(1))
    order = sorted(nodes, key=lambda i: -nodes[i]['y'])          # پایین ← بالا (همان ORDER نقشه؛ آزمون آن را می‌سنجد)
    assert len(order) == sum(n for _, n, _, _ in LANDS) == 34
    cells, k = [], 0
    for land, n, _, _ in LANDS:
        for _ in range(n):
            i = order[k]; sp = json.load(open(MT / 'etudes/stations/out' / (sym_of[i] + '.json'), encoding='utf-8'))
            cells.append(dict(id=i, sym=sym_of[i], title=nodes[i]['title'], land=land, pad=sp['pad'], rg=sp.get('ring', [0, 0, 0]))); k += 1
    out = MT / 'etudes/stations/out'
    strips = ''.join(re.search(r'<symbol id="zb_strip_%s".*?</symbol>' % z, mi, re.S).group(0) for z in ('sports', 'space', 'farm', 'city'))   # بافت زمین هر سرزمین = همان نقشهٔ بلند
    syms = strips + ''.join((out / ('node_%s.svg' % c['sym'])).read_text(encoding='utf-8') for c in cells if c['id'] != 'M12')   # مخفی‌گاه لو نمی‌رود
    def enc(p):
        im = Image.open(p).convert('RGBA'); im = im.resize((round(im.width * 150 / im.height), 150), Image.LANCZOS)
        b = io.BytesIO(); im.save(b, 'WEBP', quality=82, method=4); return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    figs = {land: enc(CACHE / o / 'nima.webp') for land, _, _, o in LANDS}
    strings = json.load(open(HERE / 'strings.fa.json', encoding='utf-8'))
    review = json.load(open(HERE / 'review.fa.json', encoding='utf-8'))
    f = lambda p: base64.b64encode(open(ROOT / 'assets/fonts' / p, 'rb').read()).decode()
    t = (HERE / 'template.html').read_text(encoding='utf-8')
    for key, v in dict(FONT_VR=f('Vazirmatn-Regular.woff2'), FONT_VB=f('Vazirmatn-Bold.woff2'), FONT_L=f('Lalezar-Regular.woff2'),
                       STRINGS=json.dumps(strings, ensure_ascii=False), REVIEW=json.dumps(review, ensure_ascii=False), SYMS=syms,
                       CELLS=json.dumps(cells, ensure_ascii=False), LANDS=json.dumps({l: c for l, _, c, _ in LANDS}), FIGS=json.dumps(figs)).items():
        t = t.replace('{{%s}}' % key, v)
    (HERE / 'index.html').write_text(t, encoding='utf-8')
    a = re.sub(r'<!doctype html>\s*<html[^>]*>\s*<head>\s*<meta[^>]*>\s*<meta[^>]*>\s*', '', t, count=1, flags=re.I)
    a = a.replace('</head>\n<body>', '<div id="root" dir="rtl" lang="fa">', 1).replace('</body>\n</html>', '</div>', 1)
    (HERE / 'artifact.html').write_text(a, encoding='utf-8')
    print('index.html', len(t) // 1024, 'KB')


if __name__ == '__main__':
    main()
