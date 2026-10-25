#!/usr/bin/env python3
"""ماکت سفر کاراکتر روی نقشهٔ شهر (دریا + بندرها): مبنا r2b (نقشهٔ بازسازی v4). index.html و artifact.html.
نقشه از env_sheet.html (v5/team/assets_r2/env)؛ مسیر روی دریا نقطه‌چین (B70). متن‌ها از strings.fa.json."""
import json, base64, io, pathlib, re
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
EA = ROOT / 'design/mockups/20261008/flow-demo/v5/team/assets_r2/env'
CACHE = ROOT / 'design/mockups/20261016/character-menu/_cache'
H, COAST = 5351, 1039   # H=1650: برچسب چوب‌شکافی از لبهٔ پایین دور شود (R17-18)

def enc(im, q=80):
    b = io.BytesIO(); im.save(b, 'WEBP', quality=q, method=4)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()

def scaled(im, h):
    return im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)

STR = json.load(open(HERE / 'strings.fa.json', encoding='utf-8'))

OLD_J = 'C330.0,1106.4 362.0,1065.8 362.0,1038.8 C362.0,1011.7 337.8,969.8 320.0,957.7'
NEW_J = 'C334.0,1117.0 343.0,1106.0 343.0,1082.0 L343.0,966.0 C343.0,959.0 332.0,957.7 320.0,957.7'

PATHD = ['']

def map_parts():
    global NM
    NM = {n['id']: n for n in json.load(open(EA / 'node_map.json', encoding='utf-8'))['nodes']}
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
    # D173: رنگ جاده یکدست: روکش «طی‌شده» (کرم + خط‌چین نارنجی تا M05) حذف و روکش ملایم تمام مسیر کشیده شد (پیشرفت را ردپاهای ماکت نشان می‌دهند)
    _ps = re.findall(r'<path d="([^"]*)"', orig)
    orig = orig.replace(_ps[1], _ps[0])
    orig, _n = re.subn(r'<path d="M128\.0,5226\.0[^"]*104\.0,2099\.0"[^>]*/>', '', orig); assert _n == 2, _n
    rest = body[e:j]
    d = json.load(open(EA / 'slots.json', encoding='utf-8'))
    d['path_d'] = d['path_d'].replace(OLD_J, NEW_J)   # D118 v2: اسکله عمودی در x=340، نوک ۹۵۶؛ نقطه‌چین از نوک
    d['path_d'] = d['path_d'].replace('C302.2,945.6 275.8,964.9 255.0,966.1 C234.2,967.3 211.8,965.9 195.0,964.7 C178.2,963.5 164.0,960.5 154.0,959.0 C144.0,957.5 149.0,957.6 135.0,955.9 C121.0,954.2 87.8,965.2 70.0,948.9', 'C300,958.4 268,960.6 236,960.6 C205,960.6 172,959.8 156,959.4 C150,959.2 145,959.1 140,959 C120,958.7 90,957 70.0,948.9')   # مسیر دریایی ساده: از نوک اسکلهٔ ساحل مستقیم تا پهلوگاه راست M07 (x≈236) و عبور از مرکز تازهٔ M07 (140)
    for a_, b_ in (('C215.0,767.5 243.2,762.3 255.0,760.5 C266.8,758.7 255.2,759.7 266.0,759.0 C276.8,758.3 304.0,775.3 320.0,756.1', 'C215.0,767.5 232.0,763.2 242.0,761.3 C246.0,760.2 247.5,759.4 250.0,759.0 C268.0,758.3 304.0,775.3 320.0,756.1'),   # M08: 266→250
                   ('C215.0,314.9 237.5,319.4 255.0,321.4 C272.5,323.3 289.2,323.7 300.0,324.0 C310.8,324.3 309.7,334.7 320.0,323.3', 'C215.0,314.9 232.0,319.4 241.0,322.0 C245.0,323.1 247.5,323.7 250.0,324.0 C275.0,324.4 309.7,334.7 320.0,323.3'),   # E06: 300→250
                   ('C175.0,200.4 147.8,196.2 135.0,194.7 C122.2,193.3 128.8,193.6 118.0,192.0 C107.2,190.4 78.0,186.3 70.0,185.1', 'C175.0,200.4 156.0,197.0 148.0,195.0 C144.5,194.0 142.5,192.6 140.0,192.0 C122.0,190.4 88.0,186.3 70.0,185.1')):   # E04: 118→140
        assert a_ in d['path_d'], a_[:30]
        d['path_d'] = d['path_d'].replace(a_, b_)
    d['path_d'] += ' C52,182.5 30,158 30,125 C30,80 60,40 120,34 C170,28 225,52 272,96'   # راه دریایی تا ایستگاه نهایی (M12)
    # D178: تکهٔ راهِ چاه←دروازه که روی رودخانه افتاده بود به جنوب کشیده می‌شود (تنها یک تقاطع با رود = پل راست)
    _K = [(10, 0), (28, 22), (52, 38), (75, 40), (95, 36), (118, 28), (140, 18), (175, 8), (215, 0)]
    def _warp(x, y):
        if not (10 < x < 215 and 2735 < y < 2872): return y
        dy = 0
        for (x0, d0), (x1, d1) in zip(_K, _K[1:]):
            if x0 <= x <= x1: dy = d0 + (d1 - d0) * (x - x0) / (x1 - x0)
        v = 1.0 if y <= 2815 else max(0.0, (2872 - y) / 57.0)
        return y + dy * v
    def _warp_d(ds): return re.sub(r'(-?\d+\.?\d*),(-?\d+\.?\d*)', lambda m: '%s,%.1f' % (m.group(1), _warp(float(m.group(1)), float(m.group(2)))), ds)
    d['path_d'] = _warp_d(d['path_d'])
    orig = re.sub(r'(<path d=")(M128\.0,5226\.0[^"]*)(")', lambda m: m.group(1) + _warp_d(m.group(2)) + m.group(3), orig)
    PATHD[:] = [d['path_d']]
    new = ('<clipPath id="cl_land"><rect x="-40" y="%d" width="470" height="%d"/></clipPath><clipPath id="cl_sea"><rect x="-40" y="-40" width="470" height="%d"/></clipPath>' % (COAST, H, 966 + 40)
           + '<g clip-path="url(#cl_land)">' + orig + '</g>'
           + '<g id="seadots" filter="url(#env_wob)"></g>')
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
    body = re.sub(r'<use href="#env_dec_city_buoy"[^>]*/>', '', body)      # R17: بویه و صخرهٔ بی‌ربط کنار کشتی‌سازی حذف
    body = re.sub(r'<use href="#env_dec_city_islet"[^>]*/>', '', body)
    body = body.replace('<use href="#env_tree_round" x="316.8" y="1457.6"', '<use href="#env_tree_round" x="298" y="1457.6"')   # سایهٔ درخت راست بریده نشود
    body = re.sub(r'<g class="hero">(?:(?!</g>).)*تو اینجایی</text></g>', '', body, flags=re.S)   # D172: «تو اینجایی» محیط؛ ماکت آواتار خودش را دارد
    mm = re.search(r'<text x="280" y="2019"[^>]*>ابزارخانه</text>', body)
    assert mm, 'M05 label src'
    body = body.replace(mm.group(0), mm.group(0) + mm.group(0).replace('x="280" y="2019"', 'x="104" y="2159"').replace('ابزارخانه', 'تیرآهن\u200cها'), 1)   # D172: M05 در env برچسب نداشت (زیر «تو اینجایی» بود)
    body = re.sub(r'<use href="#env_dec_city_(truck_crane|truck_box|rail)"[^>]*/>', '', body)
    body, _n = re.subn(r'<use href="#env_dec_(farm_fence|farm_scare|sports_flags|sports_hedge|space_rock2)"[^>]*/>|<use href="#env_tree_round" x="-16\.2" y="3948\.6"[^>]*/>', '', body); assert _n == 6, _n   # D175: دکورهای تازه‌نمایان روی راه
    for a_, b_ in (('x="101.2" y="2985"', 'x="135" y="3092"'), ('rotate(-3 101.2 2985)', 'rotate(-3 135 3092)'), ('x="141.8" y="3360"', 'x="272" y="3190"'), ('rotate(-3 141.8 3360)', 'rotate(-3 272 3190)'), ('x="230.4" y="4515"', 'x="232" y="5285"'), ('rotate(-3 230.4 4515)', 'rotate(-3 232 5285)')):   # D175: عنوان «مزرعه و آسیاب» و «ورزشگاه» از برچسب ایستگاه‌ها دور شود
        assert a_ in body, a_
        body = body.replace(a_, b_)   # D173: «ماشین‌ها» (کامیون‌های دکور) زشت‌اند و روی راه می‌افتند؛ حذف
    for href, ux, uy, dx, dy in (('env_tree_bush', '225.8', '1456.2', -5, -8), ('env_tree_round', '298', '1457.6', 8, -12.5), ('env_tree_bush', '46', '1701', 8, 9), ('env_tree_round', '110', '2227', 2, 4)):   # D173: درخت/درختچه‌ها از لبهٔ راه دور شوند (ovl.py)
        a_ = re.search(r'<use href="#%s" x="%s" y="%s"' % (href, re.escape(ux), re.escape(uy)), body); assert a_, (href, ux, uy)
        body = body.replace(a_.group(0), '<use href="#%s" x="%.1f" y="%.1f"' % (href, float(ux) + dx, float(uy) + dy), 1)
    body, _n = re.subn(r'<use href="#env_tree_bush" x="315\.5" y="2566\.2"[^>]*/>', '', body); assert _n == 1   # روی پل می‌افتاد
    body, _n = re.subn(r'<g transform="translate\([\d.]+ [\d.]+\)"><circle r="10" fill="#fff3c4" stroke="#241a5e" stroke-width="3"/><polyline[^>]*/></g>', '', body); print('env ticks removed', _n)   # D173: تیک‌های ثابت محیط؛ جایش تیک ماکت (پیشرفت واقعی)
    body = re.sub(r'<use href="#env_dec_city_(crate|sail|low)"[^>]*/>', '', body)      # جعبه و بادبان بی‌معنا بالای نقشه، خانهٔ خاکستری کنار راه
    body = body.replace('stroke="#fff3c4" stroke-width="22" stroke-linecap="round" opacity=".34"', 'stroke="#fff3c4" stroke-width="22" stroke-linecap="round" opacity=".6"')
    # ایستگاه نهایی M12 (کارگاه ماشین مرکب): در قاب، با قفل و برچسب
    m12 = '<g style="filter:saturate(1.6) brightness(1.1)"><g class="node" data-id="M12" filter="url(#env_wob)"><use href="#node_final_workshop" x="200" y="-12" width="144" height="137" /></g></g>'
    m12lab = '<text x="294" y="%.1f" text-anchor="middle" font-family="Lalezar" font-size="20" fill="#fff3c4" stroke="#241a5e" stroke-width="6" paint-order="stroke" stroke-linejoin="round">%s</text>' % (158 + LABEL_DY.get('M12', 0), STR['maptravel.node.M12']['text'])
    body = body.replace('<g id="env_zone_titles"', m12lab + '<g id="env_zone_titles"', 1)
    seat = '<text x="105" y="1069" text-anchor="middle" font-family="Lalezar" font-size="27" fill="#fff" stroke="#241a5e" stroke-width="8" paint-order="stroke" stroke-linejoin="round" transform="rotate(-3 105 1069)">%s</text>' % STR['maptravel.zone.sea']['text']
    body = body.replace('<g id="env_zone_titles">', '<g id="env_zone_titles">' + seat, 1)   # D173: منطقهٔ دریایی از شهر صنعتی جدا
    body = body.replace('<g id="env_labels"', '<g id="dnlayer"></g><g id="env_labels"', 1)
    body = re.sub(r'<text x="301\.3" y="2068"([^>]*?)font-size="34"([^>]*?)rotate\(-3 301\.3 2068\)', r'<text x="238" y="2084"\1font-size="28"\2rotate(-3 238 2084)', body, count=1)   # D173: عنوان «شهر صنعتی» از برچسب اتاق ابزار و راه دور شود
    body = body.replace('<g id="env_labels"', m12 + '<g id="env_labels"', 1)
    # قفل یکدست (مالک ۱۸ اکتبر): همهٔ قفل‌ها یک شکل، یک رنگ، یک جای نسبی روی لبهٔ راست-پایین سکو، کاملاً روی سکو
    body, nlk = re.subn(r'<g transform="translate\([\d.]+ [\d.]+\)"><circle r="10" fill="#fff3c4"[^>]*/><path d="M-3\.6[^>]*/><rect x="-5\.6"[^>]*/></g>', '', body)
    assert nlk == 3, nlk      # E04 E06 M11 از env_sheet
    lk = ''.join('<g class="lock" data-lock="%s" transform="translate(%.1f %.1f)"><circle r="10" fill="#fff3c4" stroke="#241a5e" stroke-width="3"/><path d="M-3.6,-1 v-2.4 a3.6,3.6 0 0 1 7.2,0 v2.4" fill="none" stroke="#241a5e" stroke-width="2.4"/><rect x="-5.6" y="-1" width="11.2" height="8" rx="2" fill="#241a5e"/></g>' % (n, KIT_XY[n][0] + LOCK_DXY[0], KIT_XY[n][1] + LOCK_DXY[1]) for n in LOCKED)
    body = body.replace('<g id="env_labels"', lk + '<g id="env_labels"', 1)
    body = body.replace('<text x="154" y="1016"', '<text x="140" y="1016"')   # برچسب M07 همراه سکو
    body = re.sub(r'(<text[^>]*?)>(انبار الوار|جرثقیل بندر)</text>', r'\1 word-spacing="9">\2</text>', body)   # D119: فاصلهٔ کلمات برچسب دیده شود
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
    body, _n = re.subn(r'<use href="#env_(ice|tunnel)"[^>]*/>', '', body); assert _n == 2, _n   # D178: کوه/تونل و یخِ پس‌زمینه روی راه، برچسب و پیست می‌افتادند
    # D184: پهنهٔ آبیِ ژرف بالای نقشه (آب‌های ناشناخته)؛ بدون خط، محو در دریای موجود
    _dg = '<defs><linearGradient id="deepg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#04182b" stop-opacity=".92"/><stop offset=".5" stop-color="#06304f" stop-opacity=".45"/><stop offset="1" stop-color="#0a4a6e" stop-opacity="0"/></linearGradient></defs><rect x="-40" y="-60" width="470" height="230" fill="url(#deepg)"/>'
    body, _n = re.subn(r'(<g id="env_zones">.*?</g>)', lambda m: m.group(1) + _dg, body, count=1, flags=re.S); assert _n == 1
    body, _n = re.subn(r'<use href="#env_dec_space_dome"[^>]*/>', '', body); assert _n == 1, _n   # D181: گنبد شناور بی‌ربط
    body, _n = re.subn(r'<use href="#env_dec_farm_(bucket|wheat)"[^>]*/>|<use href="#env_tree_bush" x="(?:220\.8|54\.0)"[^>]*/>|<use href="#env_tree_round" x="(?:112\.0|325\.8)"[^>]*/>|<use href="#env_tree_pop" x="329\.5"[^>]*/>|<use href="#env_tree_oak" x="-9"[^>]*/>', '', body); assert _n == 8, _n   # D178: درخت/بوته/دکور چسبیده به راه یا ایستگاه
    # D178: پل‌ها دقیقاً روی راه: دو تقاطع راه و رودخانه (محاسبه با shapely) هر کدام یک پل هم‌جهت با راه
    body, _n = re.subn(r'<g transform="translate\(344 2665\.8\) rotate\(-129\.4\)" filter="url\(#env_wob\)"><use href="#env_bridge"[^>]*/></g>',
        '<g transform="translate(341.5 2669) rotate(50) scale(1 1.45)" filter="url(#env_wob)"><use href="#env_bridge" x="-42" y="-24.5" width="84" height="49" /></g>'
        '', body); assert _n == 1, _n
    body = re.sub(r'<use href="#env_dec_city_mid"[^>]*/>', '', body)   # بلوک‌های خاکستری نامفهوم
    body = body.replace('data-id="M10" filter="url(#env_wob)"', 'data-id="M10"')   # M10-nofilter: D107، نماد خط دستیِ برداری بدون فیلتر رستری
    body = body.replace('filter:grayscale(.8) brightness(.9)', 'filter:saturate(1.6) brightness(1.1)')
    for old, key in (('میدان شهر', 'E06'), ('لنگرگاه', 'M11'), ('تیرآهن\u200cها', 'M05'), ('ابزارخانه', 'M06'), ('آچارخانه', 'E05')):
        body = body.replace('>%s<' % old, '>%s<' % STR['maptravel.node.' + key]['text'])
    body = body.replace('translate(143 210)', 'translate(140 199)').replace('translate(248 570)', 'translate(205 536)')
    # D112 (گزارش بازبین flags_m10): برچسب‌ها زیر مرکز سکو و دور از لبه؛ درخت کنار E03 از راه دور
    for a, b in (('<text x="284" y="1435"', '<text x="256" y="1445.5"'), ('<text x="118" y="1599"', '<text x="118" y="1608"'), ('<text x="158" y="1304"', '<text x="158" y="1314"')):
        assert a in body, a
        body = body.replace(a, b)
    a = '<use href="#env_tree_round" x="13" y="1262" width="70.0" height="70.0" />'
    assert a in body, 'tree'
    body = body.replace(a, '<use href="#env_tree_round" x="1" y="1262" width="70.0" height="70.0" />')
    # R17-16: جزیرهٔ چوب‌شکافی روی ماسه گم نشود: هالهٔ روشن زیرش
    m9 = '<g class="node" data-id="M09" filter="url(#env_wob)">'
    assert m9 in body, 'M09'
    body = body.replace(m9, '<ellipse cx="118" cy="1556" rx="66" ry="31" fill="#fff6d0" opacity=".62"/>' + m9)
    # D115: ایستگاه‌های بازسازی‌شده با کیت (etudes/stations/out): مرکز سکو = مرکز گره؛ نماد برداری بدون فیلتر رستری
    for sid, nid in KIT_NODES.items():
        pat = r'<g class="node" data-id="%s"(?: filter="url\(#env_wob\)")?>(?:<use href="#[^"]+"[^>]*/>)+</g>' % nid
        assert re.search(pat, body), nid
        body = re.sub(pat, lambda m, sid=sid, nid=nid: '<g class="node" data-id="%s"><use href="#node_%s" x="%s" y="%s" width="144" height="137" /></g>' % (nid, sid, KIT_XY[nid][0] - 72, KIT_XY[nid][1] - 108), body)
    for a, b in (('<text x="118" y="244"', '<text x="140" y="256"'), ('<text x="300" y="376"', '<text x="250" y="388"'), ('<text x="162" y="605"', '<text x="162" y="591"'), ('<text x="266" y="832"', '<text x="250" y="836"')):   # R17-05/21/23: فاصلهٔ برچسب تا جزیره ≥ ۷
        assert a in body, a
        body = body.replace(a, b)
    body = body.replace('>برج ساعت<', '>%s<' % STR['maptravel.node.E04']['text'])
    for nid in ('F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08', 'F09', 'W01', 'W02', 'W03', 'W04', 'E01', 'E02', 'E07'):   # D175: برچسب هر ایستگاهٔ تازه زیر سکو
        et = NM[nid]['env_title']; cx, cy = KIT_XY[nid]
        m_ = re.search(r'<text x="[\d.]+" y="[\d.]+"([^>]*)>%s</text>' % re.escape(et), body)
        assert m_, (nid, et)
        body = body.replace(m_.group(0), '<text x="%s" y="%s"%s>%s</text>' % (cx, cy + 71 + {'E07': 1.5, 'F04': 1.5}.get(nid, 0), m_.group(1), STR['maptravel.node.' + nid]['text']), 1)
    for nid, dy in LABEL_DY.items():
        if nid == 'M12': continue
        t = re.escape(STR['maptravel.node.' + nid]['text'] if ('maptravel.node.' + nid) in STR else LABEL_TITLE[nid])
        body, c = re.subn(r'(<text x="[\d.]+" y=")([\d.]+)("[^>]*>%s</text>)' % t, lambda m: m.group(1) + ('%.1f' % (float(m.group(2)) + dy)) + m.group(3), body)
        assert c == 1, (nid, c)
    WAVE_AVOID[:] = [(x - 75, y - (85 if (x, y) == KIT_XY["M12"] else 50), x + 75, y + 38) for x, y in KIT_XY.values()] + [(346 - 30, 940, 380, 1040)]   # سکوها + اسکله
    for m in re.finditer(r'<text x="([\d.]+)" y="([\d.]+)"[^>]*>([^<]+)</text>', body):
        t = m.group(3)
        if t in set(v['text'] for k, v in STR.items() if k.startswith('maptravel.node.') and k != 'maptravel.node.label') | set(LABEL_TITLE.values()):
            cx, ly, w = float(m.group(1)), float(m.group(2)), 5.5 * len(t) + 14
            WAVE_AVOID.append((cx - w, ly - 26, cx + w, ly + 12))
    return style, sprite, '<svg class="map" xmlns="http://www.w3.org/2000/svg" width="390" height="%d" viewBox="0 0 390 %d">%s</svg>' % (H, H, body), d

LOCKED = ['E04', 'E06', 'M11', 'M12']
LOCK_DXY = (42, 14)   # جای قفل نسبت به مرکز سکو
LABEL_DY = {'E04': 3.0, 'E06': 7.5, 'M11': 6.0, 'M07': 11.5, 'M02': 15.0, 'E03': 8.0, 'M10': 8.0, 'M12': 7.5, 'M09': 6.0, 'M01': 17.5, 'B01': 17.5, 'B02': 17.5, 'M04': 10.0, 'M05': 12.0, 'M06': 17.5, 'E05': 17.5, 'M03': 10.0}   # جابه‌جایی عمودی برچسب هر ایستگاه (تنظیم با tools/measure_map.py؛ حداقل ۷px تا سکو/حلقه)
LABEL_TITLE = {'M07': 'اسکله', 'M02': 'بارانداز', 'M08': 'جرثقیل بندر', 'E03': 'انبار الوار', 'M10': 'پیچ‌کاری', 'M09': 'چوب‌شکافی'}
KIT_NODES = {'screw_workshop': 'M10', 'lumber': 'E03', 'wheel_dock': 'M02', 'pier': 'M07', 'harbor_crane': 'M08', 'shipyard': 'M11', 'floating_market': 'E06', 'lighthouse': 'E04', 'final_workshop': 'M12', 'chopwood': 'M09',
            'city_gate': 'M01', 'scaffold': 'B01', 'materials_store': 'B02', 'excavation': 'M04', 'beam_store': 'M05', 'tool_room': 'M06', 'wrench_room': 'E05', 'loading_ramp': 'M03',
            'football': 'F01', 'basketball_hall': 'F02', 'archery_range': 'F03', 'magnet_hockey': 'F04', 'ice_rink': 'F06', 'pool': 'F07', 'tug_field': 'F08', 'skate_park': 'F09',
            'launch_pad': 'F05', 'space_loading': 'W01', 'scale_lab': 'W02', 'moon': 'W03', 'space_station': 'W04', 'windmill': 'E01', 'cart_station': 'E02', 'well': 'E07'}   # D175: ورزشگاه، فضا، مزرعه   # D172: هشت ایستگاه شهر صنعتی
KIT_XY = {'M01': (118, 2627), 'B01': (284, 2495), 'B02': (108, 2363), 'M04': (288, 2231), 'M05': (104, 2099), 'M06': (280, 1967), 'E05': (112, 1835), 'M03': (286, 1703), 'M10': (256, 1385), 'E03': (158, 1251), 'M02': (302, 1119), 'M07': (140, 959), 'M08': (250, 759), 'M11': (162, 524), 'E06': (250, 324), 'E04': (140, 192), 'M12': (272, 96), 'M09': (118, 1543)}   # مرکز سکو = مرکز گره
_SL = json.load(open(EA / 'slots.json', encoding='utf-8'))['slots']
for _n in ('F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08', 'F09', 'W01', 'W02', 'W03', 'W04', 'E01', 'E02', 'E07'): KIT_XY[_n] = tuple(_SL[_n]['base_center'])   # D175
E03_SH = '<ellipse cx=\"7\" cy=\"21\" rx=\"46\" ry=\"18.5\" fill=\"#10083a\" opacity=\".3\"/>'

WAVE_AVOID = []

def drop_waves(sprite):
    # R17: موج‌های مویی که روی نقطه‌چین مسیر دریایی می‌افتند حذف شوند
    d = PATHD[0]
    toks = re.findall(r'[MLC]|-?\d+\.?\d*', d); pts = []; i = 0; cur = None
    while i < len(toks):
        c = toks[i]; i += 1
        n = {'M': 1, 'L': 1, 'C': 3}[c]
        while i < len(toks) and toks[i] not in 'MLC':
            q = [(float(toks[i + 2 * k]), float(toks[i + 2 * k + 1])) for k in range(n)]; i += 2 * n
            if c == 'C':
                for t in range(1, 11):
                    u = t / 10; a, b, c2, e = cur, q[0], q[1], q[2]
                    pts.append(tuple((1-u)**3*a[j] + 3*(1-u)**2*u*b[j] + 3*(1-u)*u*u*c2[j] + u**3*e[j] for j in (0, 1)))
            else: pts.append(q[0])
            cur = q[-1]
    extra = [(346, 938), (320, 958), (236, 961), (70, 949)]   # قوس لنگرگاه و بقیه (تقریب؛ فاصلهٔ ۲۲ کافی است)
    def bad(m):
        x, y = float(m.group(1)), float(m.group(2))
        if y < 0: return m.group(0)
        if any(l[0] - 8 < x + 48 and x - 8 < l[2] and l[1] - 14 < y + 4 and y - 14 < l[3] for l in WAVE_AVOID): return ''   # R17-28: موج روی برچسب/سکو/اسکله نیفتد
        if y > 1000: return m.group(0)
        return '' if any(min(abs(x + dx - px) ** 2 + (y - 3 - py) ** 2 for px, py in pts) < 20 ** 2 for dx in (0, 13, 26, 40)) else m.group(0)
    return re.sub(r'<path d="M([\d.]+),([\d.]+) q6\.6,-7\.7 13\.2,0 t13\.2,0 t13\.2,0"[^>]*/>', bad, sprite)

def add_assets(sprite):
    # D160: نمادهای ایستگاه همیشه از خروجی کیت (etudes/stations/out) خوانده می‌شوند، نه از کپی‌های قدیمیِ assets/ (که ۱۹ تا ۲۱ اکتبر مانده بودند)
    SO = HERE / 'etudes' / 'stations' / 'out'
    skip = {'node_%s.svg' % sid for sid in KIT_NODES}
    extra = ''.join((HERE / 'assets' / f).read_text(encoding='utf-8') for f in sorted(p.name for p in (HERE / 'assets').glob('*.svg')) if f not in skip)
    extra += ''.join((SO / ('node_%s.svg' % sid)).read_text(encoding='utf-8') for sid in KIT_NODES)
    sprite = re.sub(r'<path d="M-5\.2,10\.9l4\.2,45\.2,-3"[^>]*/>', '', sprite)   # مسیر خراب در node_09 (خط نازک زیر چوب‌شکافی)
    sprite = sprite.replace('in2="n" scale="3.4"', 'in2="n" scale="2"').replace('baseFrequency=".045"', 'baseFrequency=".03"')   # D106: لرزش کمتر
    sprite, _n = re.subn(r'<path d="[^"]*" fill="#2aa6c8" opacity="\.7"/>', '', sprite); assert _n == 1, _n   # D180: نوار سایهٔ رود با لبهٔ بُریده
    sprite, _n = re.subn(r'<path transform="translate\(\d+ 17[37]\.2\d*\)"[^>]*/>', '', sprite); assert _n == 3, _n   # D180: لکهٔ دایره‌ای آبی/قهوه‌ای ابتدای رودخانه
    assert '<feDisplacementMap in="SourceGraphic" in2="n" scale="2"/>' in sprite
    sprite = sprite.replace('<feDisplacementMap in="SourceGraphic" in2="n" scale="2"/>', '<feDisplacementMap in="SourceGraphic" in2="n" scale="2"/><feGaussianBlur stdDeviation=".45"/>')   # D180: پله‌پله‌شدن لبهٔ جاده روی صفحهٔ ۱×
    # D112: سایهٔ سکو نباید بیرون سکو روی راه بیفتد (کوچک‌تر و هم‌مرکز با سکو)
    sprite = sprite.replace('<ellipse cx="8" cy="6" rx="58" ry="20" class="esd"/>', '<ellipse cx="2" cy="5" rx="52" ry="17" class="esd"/>')
    sprite = sprite.replace('<ellipse cx="7" cy="21" rx="55" ry="20.9" fill="#10083a" opacity=".3"/>', '<ellipse cx="3" cy="19" rx="50" ry="18" fill="#10083a" opacity=".3"/>')
    extra = extra.replace('<ellipse cx="7" cy="6" rx="68" ry="22" fill="#10083a" opacity=".25"/>', '<ellipse cx="2" cy="5" rx="60" ry="19" fill="#10083a" opacity=".25"/>')
    # D112 دور دوم: سایهٔ تیرهٔ M09 و E03 روی راه نیفتد (هنوز کمی بیرون سکو دیده شود)
    extra = extra.replace('<ellipse cx="7" cy="21" rx="55" ry="20.9" fill="#10083a" opacity=".3"/>', E03_SH)
    a = extra.index('id="node_final_workshop"'); b2 = extra.index('</symbol>', a)
    seg = extra[a:b2]
    for o, n in (('fill="#8a7a2a" class="eo"', 'fill="#6c8fd6" class="eo"'), ('fill="#f4e6a0" class="eo"', 'fill="#a6bde8" class="eo"'), ('stroke="#d4c26a"', 'stroke="#d6e8ff"'), ('fill="#8f8bd6"', 'fill="#7b8fe0"'), ('<circle cx="58" cy="-16" r="3.5" fill="#8a7a2a"/>', '<circle cx="58" cy="-16" r="3.5" fill="#4d6fb0"/>')):
        seg = seg.replace(o, n)
    extra = extra[:a] + seg + extra[b2:]   # R17-25: جزیرهٔ قفل M12 هم‌رنگ بقیهٔ جزیره‌های قفل
    # R17-15: مثلث‌ها و نقطهٔ ریز روی سکوها (سنگ‌ریزه) حذف
    extra, npb = re.subn(r'<path d="M(?:14\.3,-23\.2|58\.6,5\.0)Q[^"]*"[^>]*/>|<circle cx="58" cy="-16" r="3\.5"[^>]*/>', '', extra)
    print('pebbles removed', npb)
    # E03: چوب‌ها ۸px به چپ تا جای ایستادن فیگور کنار آن‌ها روی سکو بماند
    extra = extra.replace('<use href="#prop_03" x="40" y="72" width="120" height="100"/>', '<use href="#prop_03" x="32" y="72" width="120" height="100"/>')
    a = sprite.index('id="node_09"'); b = sprite.index('</symbol>', a)
    seg = sprite[a:b].replace('fill="#f4e6a0"', 'fill="#fff6cf"').replace('fill="#8a7a2a" class="eo"', 'fill="#5e4e14" class="eo"')
    sprite = sprite[:a] + seg + sprite[b:]
    sprite = re.sub(r'<rect x="[\d.]+" y="[\d.]+" width="[\d.]+" height="[\d.]+" rx="8" fill="#a98343" opacity="\.5"/>', '', sprite)   # R17: لکه‌های مستطیلی روی ماسه
    sprite = re.sub(r'<polygon points="(?:34,-6 42,-2 38,-10|-40,-4 -33,0 -36,-8)" fill="#c98a45"[^>]*/>', '', sprite)   # R17-15/17: مثلث‌های ریز کنار کنده
    sprite = drop_waves(sprite)
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
    PAD = {'M07': (54, 19, 12, 100), 'M08': (97, 35, 14, 120), 'M11': (94, 32, 14, 120), 'M12': (75, 26, 11, 90),
           "M10": (55, 27, 12, 100), 'E06': (80, 27, 12, 100), 'E03': (48, 17, 14, 55), 'M02': (48, 17, 14, 55), 'E04': (48, 17, 14, 90)}
    # جای ایستادن فیگور [dx, dy] از مرکز سکو (D112 دور دوم): کنار بنا روی بیضی سکو، نه روی کنده/چوب
    STAND = {'E03': (31, 6), 'M10': (34, 9)}
    RING = {"M10": (0, 0, 0)}      # [افزایش rx، افزایش ry، جابه‌جایی مرکز x]
    for sid, nid in KIT_NODES.items():      # مشخصات هر ایستگاهِ کیت (etudes/stations/out/<id>.json) جایگزین مقدارهای دستی
        sp = json.load(open(HERE / 'etudes' / 'stations' / 'out' / (sid + '.json'), encoding='utf-8'))
        PAD[nid] = tuple(sp['pad']); STAND[nid] = tuple(sp['stand']); RING[nid] = tuple(sp['ring'])
        cx, cy = KIT_XY[nid]; nodes[nid]['hit'] = [cx - 72, cy - 108, 144, 137]
        nodes[nid]['x'], nodes[nid]['y'] = cx, cy
    for k, v in STAND.items(): nodes[k]['st'] = list(v)
    for k, v in RING.items(): nodes[k]['rg'] = list(v)
    for k, v in nodes.items(): v['pad'] = list(PAD.get(k, (48, 17, 14, 55)))
    HSU = re.findall(r'data:[a-z/+]+;base64,[A-Za-z0-9+/=]+', (HERE.parent / 'hideout-scene' / 'index.html').read_text(encoding='utf-8')); assert len(HSU) == 3   # D185: صحنهٔ مخفی‌گاه (ماکت ۱۶ اکتبر)
    im = {}
    for o in ['sailor', 'construction']:
        im[o] = enc(scaled(Image.open(CACHE / o / 'nima.webp').convert('RGBA'), 200))
    f = lambda p: base64.b64encode(open(ROOT / 'assets/fonts' / p, 'rb').read()).decode()
    t = open(HERE / 'template.html', encoding='utf-8').read()
    sym = re.search(r'<symbol id="env_dec_city_sail".*?</symbol>', (EA / 'sprite_env.svg').read_text(encoding='utf-8'), re.S).group(0)
    for k, v in dict(FONT_VR=f('Vazirmatn-Regular.woff2'), FONT_VB=f('Vazirmatn-Bold.woff2'), FONT_L=f('Lalezar-Regular.woff2'),
                     LIGHTCSS=style, SPRITE=add_assets(sprite if 'env_dec_city_sail' in sprite else sprite.replace('</defs>', sym + '</defs>', 1)), MAPSVG=mapsvg,
                     STRINGS=json.dumps(strings, ensure_ascii=False), REVIEW=json.dumps(review, ensure_ascii=False),
                     NODES=json.dumps(nodes, ensure_ascii=False), PATHD=json.dumps(d['path_d']), IMAGES=json.dumps(im), HS_BG=HSU[0], HS_MO=HSU[1], HS_CH=HSU[2], H=str(H), COAST=str(COAST)).items():
        t = t.replace('{{%s}}' % k, v)
    (HERE / 'index.html').write_text(t, encoding='utf-8')
    a = re.sub(r'<!doctype html>\s*<html[^>]*>\s*<head>\s*<meta[^>]*>\s*<meta[^>]*>\s*', '', t, count=1, flags=re.I)
    a = a.replace('</head>\n<body data-light="day">', '<div id="root" dir="rtl" lang="fa" data-light="day">', 1).replace('</body>\n</html>', '</div>', 1)
    a = a.replace("const S=", "document.documentElement.setAttribute('dir','rtl');document.documentElement.setAttribute('lang','fa');document.documentElement.setAttribute('data-light','day');\nconst S=", 1)
    (HERE / 'artifact.html').write_text(a, encoding='utf-8')
    import shutil; shutil.copyfile(HERE.parents[2] / 'mockups/20261008/flow-demo/v5/index.html', HERE / 'cardbox.html')   # D186: صفحهٔ مقصد جعبهٔ کارت/مرور (ماکت جریان v5؛ با #box و #prac)
    print('index.html', len(t) // 1024, 'KB; artifact.html', len(a) // 1024, 'KB')

if __name__ == '__main__':
    main()
