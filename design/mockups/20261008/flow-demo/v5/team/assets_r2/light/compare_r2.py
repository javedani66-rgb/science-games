#!/usr/bin/env python3
"""عکس مقایسهٔ «v4 | جدید» -> shots/compare_palette_v4_vs_r2.png (ستون‌ها ۳۹۰px). برچسب‌ها فقط ابزار بازبینی‌اند، نه متن بازی."""
import json, os, base64, re
from playwright.sync_api import sync_playwright
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, 'shots'); V4 = os.path.abspath(os.path.join(H, '../../../../v4/style/shots'))
X = json.load(open(os.path.join(H, 'zone_tokens_v4.json'))); T = json.load(open(os.path.join(H, 'zone_tokens.json')))
# برش‌های زمین v4 (۳۹۰×۱۳۰)
crops = [('r10_map_y1900', (0, 560, 390, 690)), ('r10_map_y1450', (0, 60, 390, 190)), ('r11_map_y0', (0, 670, 390, 800)), ('r11_map_y0', (0, 300, 390, 430))]
im = Image.new('RGB', (390, 520))
for i, (f, b) in enumerate(crops): im.paste(Image.open(os.path.join(V4, f + '.png')).convert('RGB').crop(b), (0, i * 130))
im.save(os.path.join(S, '_v4_zones.png'))
Image.open(os.path.join(S,'samples_390x800.png')).crop((0,0,390,520)).save(os.path.join(S,'_new_zones.png'))
Image.open(os.path.join(S,'scene_390x800_full.png')).crop((0,0,390,1135)).save(os.path.join(S,'_new_light.png'))
def uri(p): return 'file://' + p
sw = lambda name, h, ch=False: '<div class="sw%s"><i style="background:%s"></i><b>%s</b><u>%s</u></div>' % (' ch' if ch else '', h, name, h)
items = [('ورزشگاه', 'ground.sports', T['zones']['sports']['base']), ('فضا', 'ground.space', T['zones']['space']['base']), ('مزرعه', 'ground.farm', T['zones']['farm']['base']), ('شهر/آب', 'ground.city', T['zones']['city']['base']),
         ('یخ', 'ground.ice', T['ground']['ice']), ('شن', 'ground.sand', T['ground']['sand']), ('مسیر کرم', 'path.done_seen', T['path']['cream']), ('مسیر مانده', 'path.rest_seen', T['path']['rest']),
         ('خط دور', 'path.outline', T['path']['outline']), ('چیپ', 'ui.chip_seen', T['ui']['chip']), ('چیپ فعال', 'ui.chip_on_seen', T['ui']['chip_on']), ('کارت بالا', 'card.front_top', T['card']['front_top']),
         ('صفحهٔ متن', 'card.plate', T['card']['plate']), ('دکمهٔ فیروزه‌ای', 'card.pill_cyan', T['card']['pill_cyan']), ('دکمهٔ صورتی', 'card.pill_pink', T['card']['pill_pink']), ('طلایی', 'card.pill_gold', T['card']['pill_gold'])]
left = ''.join(sw(n, X[k]['hex']) for n, k, _ in items)
right = ''.join(sw(n, new, X[k]['hex'].lower() != new.lower() and k not in ('ground.sports', 'ground.space', 'ground.farm', 'ground.city', 'ui.chip_seen', 'ui.chip_on_seen', 'path.done_seen', 'card.front_top', 'card.plate')) for n, k, new in items)
right += sw('قرص آسان', T['hardness']['easy']['hex'], True) + sw('قرص متوسط', T['hardness']['mid']['hex'], True) + sw('قرص سخت', T['hardness']['hard']['hex'], True) + sw('کف آب شهر', T['path']['city_foam'], True)
left += '<div class="sw"><i style="background:repeating-linear-gradient(45deg,#ccc,#ccc 4px,#eee 4px,#eee 8px)"></i><b>(v4 نداشت)</b><u>-</u></div>' * 4
css = '''*{box-sizing:border-box;margin:0}body{width:800px;background:#190539;color:#fff3c4;font:700 13px Vazirmatn,system-ui;padding:8px;direction:rtl}
.cols{display:grid;grid-template-columns:390px 390px;gap:10px;direction:ltr}h2{font-size:16px;margin:8px 0 4px;color:#ffd23f}h3{font-size:15px;background:#241a5e;border:3px solid #fff3c4;border-radius:10px;padding:2px 10px;margin-bottom:4px;text-align:center}
.g{display:grid;grid-template-columns:repeat(4,1fr);gap:5px}.sw{background:#241a5e;border-radius:6px;padding:3px;text-align:center;font-size:11px;line-height:1.2}.sw i{display:block;height:28px;border-radius:4px;border:1.5px solid #fff3c4}.sw b,.sw u{display:block;text-decoration:none;font-weight:400}
.sw.ch{outline:3px solid #ff4b4b}img{display:block;width:390px}'''
sc = 'file://' + H + '/scene_demo.html'
html = '''<!doctype html><html><head><meta charset=utf-8><style>%s</style></head><body>
<div class="cols"><h3>v4 (دیده‌شده در عکس‌ها)</h3><h3>جدید r2 (کادر قرمز = تغییر/افزوده)</h3></div>
<div class="cols"><div class="g">%s</div><div class="g">%s</div></div>
<h2>زمین + مسیر + قرص سختی</h2>
<div class="cols"><img src="%s"><img src="%s"></div>
<h2>نور: v4 (روز / غروب multiply / شب) | جدید (روز / غروب لبه+سایه / شب)</h2>
<div class="cols"><img src="%s"><img id="sc" src="%s"></div></body></html>''' % (css, left, right, uri(os.path.join(S, '_v4_zones.png')), uri(os.path.join(S, '_new_zones.png')), uri(os.path.join(V4, 'r11_transition.png')), uri(os.path.join(S, '_new_light.png')))
open(os.path.join(S, '_compare.html'), 'w').write(html)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox']); pg = b.new_page(viewport={'width': 816, 'height': 800})
    pg.goto('file://' + os.path.join(S, '_compare.html')); pg.wait_for_timeout(600)
    pg.screenshot(path=os.path.join(S, 'compare_palette_v4_vs_r2.png'), full_page=True); b.close()
print('ok')
