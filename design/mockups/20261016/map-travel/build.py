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

OLD_J = 'C330.0,1106.4 362.0,1065.8 362.0,1038.8 C362.0,1011.7 337.8,969.8 320.0,957.7'
NEW_J = 'C333.0,1108.0 343.0,1080.0 343.0,1050.0 L343.0,966.0 C343.0,959.0 332.0,957.7 320.0,957.7'

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
    orig = orig.replace(OLD_J, NEW_J)   # D118 v2: راه خشکی هم تا اسکلهٔ x=340
    rest = body[e:j]
    d = json.load(open(EA / 'slots.json', encoding='utf-8'))
    d['path_d'] = d['path_d'].replace(OLD_J, NEW_J)   # D118 v2: اسکله عمودی در x=340، نوک ۹۵۶؛ نقطه‌چین از نوک
    d['path_d'] = d['path_d'].replace('C302.2,945.6 275.8,964.9 255.0,966.1 C234.2,967.3 211.8,965.9 195.0,964.7 C178.2,963.5 164.0,960.5 154.0,959.0 C144.0,957.5 149.0,957.6 135.0,955.9 C121.0,954.2 87.8,965.2 70.0,948.9', 'C346,938 346,911 320,906 C285,900 215,901 196,925 C184,941 196,962 180,964 C160,966 140,962 120,960 C110,959 105,959 100,959 C90,958 80,955 70.0,948.9')   # مسیر دریایی بلندتر: قوس لنگرگاه بین اسکلهٔ ساحل و M07
    d['path_d'] += ' C52,182.5 30,158 30,125 C30,80 60,40 120,34 C170,28 225,52 272,96'   # راه دریایی تا ایستگاه نهایی (M12)
    new = ('<clipPath id="cl_land"><rect x="-40" y="%d" width="470" height="%d"/></clipPath><clipPath id="cl_sea"><rect x="-40" y="-40" width="470" height="%d"/></clipPath>' % (COAST, H, 966 + 40)
           + '<g clip-path="url(#cl_land)">' + orig + '</g>'
           + '<g clip-path="url(#cl_sea)" filter="url(#env_wob)"><path d="%s" fill="none" stroke="#241a5e" stroke-width="9" stroke-linecap="round" stroke-dasharray="1 17" opacity=".35"/>'
             '<path d="%s" fill="none" stroke="#e8f6f8" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 17" opacity=".85"/></g>' % (d['path_d'], d['path_d']))
    body = body[:i] + new + rest + body[j:]
    # مالک (۱۶ اکتبر ۱۸:۱۹): فانوس تزئینی آخر صحنه حذف؛ «برج ساعت» (E04) فانوس دریایی روی صخره می‌شود
    body = re.sub(r'<use href="#env_dec_city_lighthouse" x="185" y="39"[^>]*/>', '', body)
    body = body.replace('<use href="#env_pad_city_metal" x="58" y="114" width="120" height="100" /><use href="#prop_15" x="58" y="114" width="120" height="100" />',
                        '<use href="#env_pad_city_stone" x="58" y="114" width="120" height="100" /><use href="#env_dec_city_lighthouse" x="53" y="74" width="130" height="130" />')
    assert 'prop_15' not in body, 'E04'
    # اصلاح بصری (flags.json ۱۶ اکتبر)
    body = body.replace('<use href="#env_pad_city_stone" x="58" y="114" width="120" height="100" /><use href="#env_dec_city_lighthouse" x="53" y="74" width="130" height="130" />',
                        '<use href="#node_lighthouse" x="18" y="42" width="200" height="190" />')
    assert 'node_lighthouse' in body, 'E04b'
    body = body.replace('<use href="#env_pad_city_metal" x="98" y="1173" width="120" height="100" /><use href="#prop_03" x="98" y="1173" width="120" height="100" />',
                        '<use href="#node_lumber" x="58" y="1101" width="200" height="190" />')
    assert 'node_lumber' in body, 'E03'
    body = body.replace('<use href="#env_pad_city_stone" x="242" y="1041" width="120" height="100" /><use href="#prop_05" x="242" y="1041" width="120" height="100" />',
                        '<use href="#node_wheel_dock" x="202" y="969" width="200" height="190" />')
    assert 'node_wheel_dock' in body, 'M02'
    body = body.replace('<use href="#node_12"', '<use href="#node_harbor_crane"')
    body = body.replace('<use href="#env_dec_city_buoy"', '<use href="#dec_buoy"')
    body = re.sub(r'<use href="#env_dec_city_(crate|sail|low)"[^>]*/>', '', body)      # جعبه و بادبان بی‌معنا بالای نقشه، خانهٔ خاکستری کنار راه
    body = body.replace('<use href="#env_dec_city_islet" x="-28"', '<use href="#env_dec_city_islet" x="-8"')
    body = body.replace('stroke="#fff3c4" stroke-width="22" stroke-linecap="round" opacity=".34"', 'stroke="#fff3c4" stroke-width="22" stroke-linecap="round" opacity=".6"')
    # ایستگاه نهایی M12 (کارگاه ماشین مرکب): در قاب، با قفل و برچسب
    m12 = ('<g style="filter:grayscale(.3) brightness(1)"><g class="node" data-id="M12" filter="url(#env_wob)"><use href="#node_final_workshop" x="192" y="-25" width="160" height="152" /></g></g>'
           '<g transform="translate(298 113)"><circle r="10" fill="#fff3c4" stroke="#241a5e" stroke-width="3"/><path d="M-3.6,-1 v-2.4 a3.6,3.6 0 0 1 7.2,0 v2.4" fill="none" stroke="#241a5e" stroke-width="2.4"/><rect x="-5.6" y="-1" width="11.2" height="8" rx="2" fill="#241a5e"/></g>')
    m12lab = '<text x="272" y="158" text-anchor="middle" font-family="Lalezar" font-size="20" fill="#fff3c4" stroke="#241a5e" stroke-width="6" paint-order="stroke" stroke-linejoin="round">%s</text>' % STR['maptravel.node.M12']['text']
    body = body.replace('<g id="env_zone_titles"', m12lab + '<g id="env_zone_titles"', 1)
    body = body.replace('<g id="env_labels"', m12 + '<g id="env_labels"', 1)
    body = body.replace('<text x="154" y="1016"', '<text x="100" y="1016"')   # برچسب M07 همراه سکو
    # کارخانهٔ صنعتی ← کارخانهٔ کشتی‌سازی؛ میدان شهر ← بازارچهٔ شناور (دارایی‌های assets/)
    body = body.replace('<use href="#node_11"', '<use href="#node_shipyard"')
    body = body.replace('<use href="#env_pad_city_ice" x="240" y="246" width="120" height="100" /><use href="#prop_04" x="240" y="246" width="120" height="100" />',
                        '<use href="#node_floating_market" x="215" y="196.5" width="170" height="161" />')
    assert 'prop_04' not in body, 'E06'
    # نمونهٔ ساختمانی (B77): پیچ‌کاری (M10) ساختمان با برج پیچ
    old = '<use href="#env_pad_city_stone" x="224" y="1305" width="120" height="100" /><use href="#prop_14" x="224" y="1305" width="120" height="100" />'
    assert old in body, 'M10'
    body = body.replace(old, '<use href="#node_screw_workshop" x="184" y="1277.5" width="144" height="137" />')
    # مالک (D97/D98): ماشین‌لیفتِ دکور روی پیچ‌کاری حذف؛ حالت «قفل» نرم‌تر تا رنگ‌ها گل‌آلود نشوند
    body = re.sub(r'<use href="#env_dec_city_forklift"[^>]*/>', '', body)
    body = re.sub(r'<use href="#env_dec_city_mid"[^>]*/>', '', body)   # بلوک‌های خاکستری نامفهوم
    body = body.replace('data-id="M10" filter="url(#env_wob)"', 'data-id="M10"')   # M10-nofilter: D107، نماد خط دستیِ برداری بدون فیلتر رستری
    body = body.replace('filter:grayscale(.8) brightness(.9)', 'filter:grayscale(.3) brightness(1)')
    for old, key in (('میدان شهر', 'E06'), ('لنگرگاه', 'M11')):
        body = body.replace('>%s<' % old, '>%s<' % STR['maptravel.node.' + key]['text'])
    body = body.replace('translate(143 210)', 'translate(140 199)').replace('translate(248 570)', 'translate(236 541)')
    # D112 (گزارش بازبین flags_m10): برچسب‌ها زیر مرکز سکو و دور از لبه؛ درخت کنار E03 از راه دور
    for a, b in (('<text x="284" y="1435"', '<text x="256" y="1445.5"'), ('<text x="118" y="1599"', '<text x="118" y="1608"'), ('<text x="158" y="1304"', '<text x="158" y="1314"')):
        assert a in body, a
        body = body.replace(a, b)
    a = '<use href="#env_tree_round" x="13" y="1262" width="70.0" height="70.0" />'
    assert a in body, 'tree'
    body = body.replace(a, '<use href="#env_tree_round" x="1" y="1262" width="70.0" height="70.0" />')
    # D115: ایستگاه‌های بازسازی‌شده با کیت (etudes/stations/out): مرکز سکو = مرکز گره؛ نماد برداری بدون فیلتر رستری
    for sid, nid in KIT_NODES.items():
        pat = r'<g class="node" data-id="%s"(?: filter="url\(#env_wob\)")?><use href="#[^"]+"[^>]*/></g>' % nid
        assert re.search(pat, body), nid
        body = re.sub(pat, lambda m, sid=sid, nid=nid: '<g class="node" data-id="%s"><use href="#node_%s" x="%s" y="%s" width="144" height="137" /></g>' % (nid, sid, KIT_XY[nid][0] - 72, KIT_XY[nid][1] - 108), body)
    body = body.replace('>برج ساعت<', '>%s<' % STR['maptravel.node.E04']['text'])
    return style, sprite, '<svg class="map" xmlns="http://www.w3.org/2000/svg" width="390" height="%d" viewBox="0 0 390 %d">%s</svg>' % (H, H, body), d

KIT_NODES = {'screw_workshop': 'M10', 'lumber': 'E03', 'wheel_dock': 'M02', 'pier': 'M07', 'harbor_crane': 'M08', 'shipyard': 'M11', 'floating_market': 'E06', 'lighthouse': 'E04', 'final_workshop': 'M12'}
KIT_XY = {'M10': (256, 1385), 'E03': (158, 1251), 'M02': (302, 1119), 'M07': (100, 959), 'M08': (266, 759), 'M11': (162, 524), 'E06': (300, 324), 'E04': (118, 192), 'M12': (272, 96)}   # مرکز سکو = مرکز گره
M09_SH = '<ellipse cx=\"0\" cy=\"21\" rx=\"51\" ry=\"19.5\" fill=\"#10083a\" opacity=\".3\"/>'
E03_SH = '<ellipse cx=\"7\" cy=\"21\" rx=\"46\" ry=\"18.5\" fill=\"#10083a\" opacity=\".3\"/>'

def add_assets(sprite):
    extra = ''.join((HERE / 'assets' / f).read_text(encoding='utf-8') for f in sorted(p.name for p in (HERE / 'assets').glob('*.svg')))
    sprite = re.sub(r'<path d="M-5\.2,10\.9l4\.2,45\.2,-3"[^>]*/>', '', sprite)   # مسیر خراب در node_09 (خط نازک زیر چوب‌شکافی)
    sprite = sprite.replace('in2="n" scale="3.4"', 'in2="n" scale="2"').replace('baseFrequency=".045"', 'baseFrequency=".03"')   # D106: لرزش کمتر
    # D112: سایهٔ سکو نباید بیرون سکو روی راه بیفتد (کوچک‌تر و هم‌مرکز با سکو)
    sprite = sprite.replace('<ellipse cx="8" cy="6" rx="58" ry="20" class="esd"/>', '<ellipse cx="2" cy="5" rx="52" ry="17" class="esd"/>')
    sprite = sprite.replace('<ellipse cx="7" cy="21" rx="55" ry="20.9" fill="#10083a" opacity=".3"/>', '<ellipse cx="3" cy="19" rx="50" ry="18" fill="#10083a" opacity=".3"/>')
    extra = extra.replace('<ellipse cx="7" cy="6" rx="68" ry="22" fill="#10083a" opacity=".25"/>', '<ellipse cx="2" cy="5" rx="60" ry="19" fill="#10083a" opacity=".25"/>')
    # D112 دور دوم: سایهٔ تیرهٔ M09 و E03 روی راه نیفتد (هنوز کمی بیرون سکو دیده شود)
    sprite = sprite.replace('<ellipse cx="7" cy="21" rx="60" ry="22.8" fill="#10083a" opacity=".3"/>', M09_SH)
    extra = extra.replace('<ellipse cx="7" cy="21" rx="55" ry="20.9" fill="#10083a" opacity=".3"/>', E03_SH)
    # E03: چوب‌ها ۸px به چپ تا جای ایستادن فیگور کنار آن‌ها روی سکو بماند
    extra = extra.replace('<use href="#prop_03" x="40" y="72" width="120" height="100"/>', '<use href="#prop_03" x="32" y="72" width="120" height="100"/>')
    i = sprite.rindex('</svg>')
    return sprite[:i] + '<defs>' + extra + '</defs>' + sprite[i:]

def main():
    strings = json.load(open(HERE / 'strings.fa.json', encoding='utf-8'))
    review = json.load(open(HERE / 'review.fa.json', encoding='utf-8'))
    style, sprite, mapsvg, d = map_parts()
    nm = {n['id']: n for n in json.load(open(EA / 'node_map.json', encoding='utf-8'))['nodes']}
    nodes = {k: dict(x=v['base_center'][0], y=v['base_center'][1], hit=v['hit_box'], title=(STR['maptravel.node.' + k]['text'] if ('maptravel.node.' + k) in STR else nm[k]['env_title']))
             for k, v in d['slots'].items() if v['base_center'][1] < H - 60}
    nodes['M12'].update(x=272, y=96, hit=[196, 8, 150, 128]); nodes['E06']['hit'] = [215, 196, 170, 161]; nodes["M10"]["hit"] = [184, 1277, 144, 137]
    nodes['M10'].update(x=256, y=1385)    # مرکز سکوی کشیده‌شده: use x=184 + 100*0.72
    # شکل سکوی هر ایستگاه برای مسیر ردپا: [نیم‌پهنا، نیم‌ارتفاع بیضی، ارتفاع دیواره، ارتفاع ساختمان]
    PAD = {'M09': (52, 19, 14, 60), 'M07': (54, 19, 12, 100), 'M08': (97, 35, 14, 120), 'M11': (94, 32, 14, 120), 'M12': (75, 26, 11, 90),
           "M10": (55, 27, 12, 100), 'E06': (80, 27, 12, 100), 'E03': (48, 17, 14, 55), 'M02': (48, 17, 14, 55), 'E04': (48, 17, 14, 90)}
    # جای ایستادن فیگور [dx, dy] از مرکز سکو (D112 دور دوم): کنار بنا روی بیضی سکو، نه روی کنده/چوب
    STAND = {'E03': (31, 6), 'M09': (39.5, 4), 'M10': (34, 9)}
    RING = {"M10": (0, 0, 0), 'M09': (0, 0, -1)}      # [افزایش rx، افزایش ry، جابه‌جایی مرکز x]
    for sid, nid in KIT_NODES.items():      # مشخصات هر ایستگاهِ کیت (etudes/stations/out/<id>.json) جایگزین مقدارهای دستی
        sp = json.load(open(HERE / 'etudes' / 'stations' / 'out' / (sid + '.json'), encoding='utf-8'))
        PAD[nid] = tuple(sp['pad']); STAND[nid] = tuple(sp['stand']); RING[nid] = tuple(sp['ring'])
        cx, cy = KIT_XY[nid]; nodes[nid]['hit'] = [cx - 72, cy - 108, 144, 137]
        nodes[nid]['x'], nodes[nid]['y'] = cx, cy
    for k, v in STAND.items(): nodes[k]['st'] = list(v)
    for k, v in RING.items(): nodes[k]['rg'] = list(v)
    for k, v in nodes.items(): v['pad'] = list(PAD.get(k, (48, 17, 14, 55)))
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
