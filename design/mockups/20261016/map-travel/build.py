#!/usr/bin/env python3
"""ماکت سفر کاراکتر روی نقشهٔ شهر (دریا + بندرها): مبنا r2b (نقشهٔ بازسازی v4). index.html و artifact.html.
نقشه از env_sheet.html (v5/team/assets_r2/env)؛ مسیر روی دریا نقطه‌چین (B70). متن‌ها از strings.fa.json."""
import json, base64, io, pathlib, re
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
EA = ROOT / 'design/mockups/20261008/flow-demo/v5/team/assets_r2/env'
CACHE = ROOT / 'design/mockups/20261016/character-menu/_cache'
H, COAST = 1620, 1039

def enc(im, q=80):
    b = io.BytesIO(); im.save(b, 'WEBP', quality=q, method=4)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()

def scaled(im, h):
    return im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)

STR = json.load(open(HERE / 'strings.fa.json', encoding='utf-8'))

def map_parts():
    s = (EA / 'env_sheet.html').read_text(encoding='utf-8')
    style = re.search(r'<style>(.*?)</style>', s, re.S).group(1)
    style = re.sub(r"@font-face\{[^}]*\}", '', style)
    style = style[:style.index('html,body{')]          # فقط متغیرهای نور و کلاس‌ها
    b = s.index('<body'); b = s.index('>', b) + 1
    m = s.index('<svg class="map"')
    sprite = s[b:s.index('<div id="sc"')]                # دیو پنهانِ sprite
    body = s[s.index('>', m) + 1:s.rindex('</svg>')]
    i = body.index('<g id="env_path"'); j = body.index('<g id="env_labels"')
    e = body.index('</g>', i) + 4
    orig = body[i:e]
    rest = body[e:j]
    d = json.load(open(EA / 'slots.json', encoding='utf-8'))
    new = ('<clipPath id="cl_land"><rect x="-40" y="%d" width="470" height="%d"/></clipPath><clipPath id="cl_sea"><rect x="-40" y="-40" width="470" height="%d"/></clipPath>' % (COAST, H, COAST + 40)
           + '<g clip-path="url(#cl_land)">' + orig + '</g>'
           + '<g clip-path="url(#cl_sea)" filter="url(#env_wob)"><path d="%s" fill="none" stroke="#241a5e" stroke-width="9" stroke-linecap="round" stroke-dasharray="1 17" opacity=".35"/>'
             '<path d="%s" fill="none" stroke="#e8f6f8" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 17" opacity=".85"/></g>' % (d['path_d'], d['path_d']))
    body = body[:i] + new + rest + body[j:]
    # مالک (۱۶ اکتبر ۱۸:۱۹): فانوس تزئینی آخر صحنه حذف؛ «برج ساعت» (E04) فانوس دریایی روی صخره می‌شود
    body = re.sub(r'<use href="#env_dec_city_lighthouse" x="185" y="39"[^>]*/>', '', body)
    body = body.replace('<use href="#env_pad_city_metal" x="58" y="114" width="120" height="100" /><use href="#prop_15" x="58" y="114" width="120" height="100" />',
                        '<use href="#env_pad_city_stone" x="58" y="114" width="120" height="100" /><use href="#env_dec_city_lighthouse" x="53" y="74" width="130" height="130" />')
    assert 'prop_15' not in body, 'E04'
    # کارخانهٔ صنعتی ← کارخانهٔ کشتی‌سازی؛ میدان شهر ← بازارچهٔ شناور (دارایی‌های assets/)
    body = body.replace('<use href="#node_11"', '<use href="#node_shipyard"')
    body = body.replace('<use href="#env_pad_city_ice" x="240" y="246" width="120" height="100" /><use href="#prop_04" x="240" y="246" width="120" height="100" />',
                        '<use href="#prop_floating_market" x="240" y="246" width="120" height="100" />')
    assert 'prop_04' not in body, 'E06'
    for old, key in (('میدان شهر', 'E06'), ('لنگرگاه', 'M11')):
        body = body.replace('>%s<' % old, '>%s<' % STR['maptravel.node.' + key]['text'])
    body = body.replace('>برج ساعت<', '>%s<' % STR['maptravel.node.E04']['text'])
    return style, sprite, '<svg class="map" xmlns="http://www.w3.org/2000/svg" width="390" height="%d" viewBox="0 0 390 %d">%s</svg>' % (H, H, body), d

def add_assets(sprite):
    extra = ''.join((HERE / 'assets' / f).read_text(encoding='utf-8') for f in sorted(p.name for p in (HERE / 'assets').glob('*.svg')))
    i = sprite.rindex('</svg>')
    return sprite[:i] + '<defs>' + extra + '</defs>' + sprite[i:]

def main():
    strings = json.load(open(HERE / 'strings.fa.json', encoding='utf-8'))
    review = json.load(open(HERE / 'review.fa.json', encoding='utf-8'))
    style, sprite, mapsvg, d = map_parts()
    nm = {n['id']: n for n in json.load(open(EA / 'node_map.json', encoding='utf-8'))['nodes']}
    nodes = {k: dict(x=v['base_center'][0], y=v['base_center'][1], hit=v['hit_box'], title=(STR['maptravel.node.' + k]['text'] if ('maptravel.node.' + k) in STR else nm[k]['env_title']))
             for k, v in d['slots'].items() if v['base_center'][1] < H - 60}
    im = {}
    for o in ['sailor', 'construction']:
        im[o] = enc(scaled(Image.open(CACHE / o / 'nima.webp').convert('RGBA'), 200))
    f = lambda p: base64.b64encode(open(ROOT / 'assets/fonts' / p, 'rb').read()).decode()
    t = open(HERE / 'template.html', encoding='utf-8').read()
    sym = re.search(r'<symbol id="env_dec_city_sail".*?</symbol>', (EA / 'sprite_env.svg').read_text(encoding='utf-8'), re.S).group(0)
    for k, v in dict(FONT_VR=f('Vazirmatn-Regular.woff2'), FONT_VB=f('Vazirmatn-Bold.woff2'), FONT_L=f('Lalezar-Regular.woff2'),
                     LIGHTCSS=style, SPRITE=add_assets(sprite if 'env_dec_city_sail' in sprite else sprite.replace('</defs>', sym + '</defs>', 1)), MAPSVG=mapsvg,
                     STRINGS=json.dumps(strings, ensure_ascii=False), REVIEW=json.dumps(review, ensure_ascii=False),
                     NODES=json.dumps(nodes, ensure_ascii=False), PATHD=json.dumps(d['path_d']), IMAGES=json.dumps(im), H=str(H), COAST=str(COAST)).items():
        t = t.replace('{{%s}}' % k, v)
    (HERE / 'index.html').write_text(t, encoding='utf-8')
    a = re.sub(r'<!doctype html>\s*<html[^>]*>\s*<head>\s*<meta[^>]*>\s*<meta[^>]*>\s*', '', t, count=1, flags=re.I)
    a = a.replace('</head>\n<body data-light="day">', '<div id="root" dir="rtl" lang="fa" data-light="day">', 1).replace('</body>\n</html>', '</div>', 1)
    a = a.replace("const S=", "document.documentElement.setAttribute('dir','rtl');document.documentElement.setAttribute('lang','fa');document.documentElement.setAttribute('data-light','day');\nconst S=", 1)
    (HERE / 'artifact.html').write_text(a, encoding='utf-8')
    print('index.html', len(t) // 1024, 'KB; artifact.html', len(a) // 1024, 'KB')

if __name__ == '__main__':
    main()
