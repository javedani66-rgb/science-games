#!/usr/bin/env python3
"""demo ها (از tokens.css و zone_tokens.json): scene_demo.html (روز/غروب/شب + انتقال روز←شب ۱٫۲ث با opacity) و samples_demo.html (مسیر/قرص سختی روی زمین‌ها).
هنر بنا = همان b_harbor کد v4 (فقط خواندن). بدون mix-blend-mode و بدون filter زنده برای نور."""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.abspath(os.path.join(H, '../../../../v4/style/gen'))
sys.path.insert(0, GEN)
import gen_head as G   # فقط b_harbor و ابزار شکل؛ هیچ فایلی نمی‌نویسد
T = json.load(open(os.path.join(H, 'zone_tokens.json'))); L = T['lights']
CSS = open(os.path.join(H, 'tokens.css')).read(); DEFS = open(os.path.join(H, 'common_defs.svg')).read()
STR = json.load(open(os.path.join(H, '../../../strings.fa.json')))
rgb = lambda h: tuple(int(h.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
hx = lambda t: '#%02x%02x%02x' % tuple(max(0, min(255, round(c))) for c in t)
def bake(h, c, a): return hx([x * ((1 - a) + a * y / 255) for x, y in zip(rgb(h), rgb(c))])
n_top, n_bot = '#6a55d8', '#3a1c90'
mid = hx([(a + b) / 2 for a, b in zip(rgb(n_top), rgb(n_bot))])
art = G.b_harbor()
def recolor(svg, f):
    return re.sub(r'(fill|stroke)="(#[0-9a-fA-F]{6})"', lambda m: '%s="%s"' % (m.group(1), f(m.group(2))), svg)
def solid(svg, col):  # برای ماسک: همهٔ رنگ‌ها یک رنگ؛ شفافیت‌ها حذف
    s = re.sub(r'(fill|stroke)="(#[0-9a-fA-F]{3,6}|rgba?\([^)]*\))"', lambda m: '%s="%s"' % (m.group(1), col), svg)
    return re.sub(r'\sopacity="[^"]*"', '', s)
art_day = art
art_night = recolor(art, lambda h: bake(h, mid, .8))   # ضرب v4 پخته در هگز (بدون blend زنده)
SC = 1.25; AX, AY = 215, 262   # جای بنا در صحنه 390x330
def scene(light, tag):
    d = L[light]; a = art_night if light == 'night' else art_day
    horizon = 176
    o = ['<g data-light="%s">' % light, '<rect width="390" height="%d" fill="url(#lt-sky-%s)"/>' % (horizon, light)]
    if light == 'night':
        for x, y, r in [(40, 30, 1.6), (120, 62, 1.2), (190, 24, 1.8), (260, 70, 1.3), (320, 34, 1.6), (360, 96, 1.2), (80, 110, 1.2), (230, 120, 1.4), (300, 140, 1.2)]:
            o.append('<circle cx="%d" cy="%d" r="%s" fill="#e9dcff" opacity=".85"/>' % (x, y, r))
        o.append('<circle cx="330" cy="44" r="17" fill="%s"/>' % d['moon'])
    o.append('<rect y="%d" width="390" height="%d" fill="%s"/>' % (horizon, 330 - horizon, d['water']))
    if light == 'dusk':  # بازتاب: خط‌های افقی (نه لکه)
        o.append('<use href="#lt-reflect-dusk" transform="translate(40 %d)"/><use href="#lt-reflect-dusk" transform="translate(250 %d) scale(.8)"/>' % (horizon + 16, horizon + 52))
    else:
        o.append('<g fill="#aef0f4" opacity="%s"><rect x="30" y="%d" width="50" height="3" rx="1.5"/><rect x="290" y="%d" width="40" height="3" rx="1.5"/></g>' % (.28 if light == 'day' else .12, horizon + 20, horizon + 60))
    s = d['shadow']  # سایهٔ افتاده روی آب: بنفش، کشیده به سمت راست
    o.append('<ellipse cx="%d" cy="%d" rx="%d" ry="12" fill="%s" opacity="%s"/>' % (AX + 18 + s['dx'], AY + 22 + s['dy'], 108 + s['dx'] * 2, s['color'], s['opacity']))
    tr = 'translate(%d,%d) scale(%s)' % (AX, AY, SC)
    o.append('<g transform="%s">%s</g>' % (tr, a))
    i = d['intensity']
    # rim = سیلوئت \ سیلوئتِ جابه‌جاشده به پایین-راست؛ سایه = سیلوئت \ سیلوئتِ جابه‌جاشده به بالا-چپ (ماسک، blend عادی)
    for nm, dx, dy, col, op in (('rim', 5, 4.5, d['lit'], i['lit_a']), ('shd', -8, -6, d['shade'], i['shade_a'])):
        mid_ = 'm%s%s' % (nm, tag)
        o.append('<mask id="%s" maskUnits="userSpaceOnUse" x="-20" y="-20" width="430" height="360"><g transform="%s">%s</g><g transform="translate(%s,%s) %s">%s</g></mask>'
                 % (mid_, tr, solid(art, '#fff'), dx * SC, dy * SC, tr, solid(art, '#000')))
        o.append('<rect width="390" height="330" fill="%s" opacity="%s" mask="url(#%s)"/>' % (col, op, mid_))
    if d['windows']:
        for x, y in ((-86, -55), (-72, -55)):
            o.append('<g transform="%s"><rect x="%d" y="%d" width="8" height="9" fill="%s"/></g>' % (tr, x, y, d['windows']))
    return ''.join(o) + '</g>'
def svg(inner, id_=''): return '<svg %s viewBox="0 0 390 330" width="390" height="330" role="img" aria-label="scene">%s</svg>' % (('id="%s"' % id_) if id_ else '', inner)
PAGE = '''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=390"><title>%s</title><style>%s
*{box-sizing:border-box;margin:0}body{background:#190539;color:#fff3c4;font:700 15px Vazirmatn,system-ui,sans-serif;width:390px}
.tag{display:inline-block;margin:8px 10px 4px;padding:2px 12px;border:3px solid #fff3c4;border-radius:12px;background:#241a5e;font-size:15px}
.fr{border-block:4px solid #241a5e;line-height:0}button{min-height:48px;min-width:80px;margin:6px;border:3.5px solid #241a5e;border-radius:16px;background:#ffd23f;color:#241a5e;font:700 16px Vazirmatn,system-ui}
</style></head><body>%s%s</body></html>'''
# ---- scene_demo: سه نور + انتقال
tr_html = ('<div id="scene" data-light="day" class="fr"><svg viewBox="0 0 390 330" width="390" height="330" role="img" aria-label="day-night transition">'
           '<g class="lt-layer" data-for="day" id="tr-day">%s</g><g class="lt-layer" data-for="night" id="tr-night">%s</g></svg></div>' % (scene('day', 'td'), scene('night', 'tn')))
body = ''.join('<span class="tag">%s</span><div class="fr" data-light="%s">%s</div>' % (nm, k, svg(scene(k, 's' + k))) for k, nm in (('day', 'روز'), ('dusk', 'غروب (فقط صحنهٔ ماجرا ۲)'), ('night', 'شب')))
body += '<span class="tag">انتقال روز←شب ۱٫۲ث (opacity)</span>' + tr_html + '<div><button id="bd" type="button">روز</button><button id="bn" type="button">شب</button></div>'
body += '<script>var s=document.getElementById("scene");function set(v){s.setAttribute("data-light",v)}document.getElementById("bd").onclick=function(){set("day")};document.getElementById("bn").onclick=function(){set("night")};var q=location.search.match(/light=(day|night)/);if(q)set(q[1])</script>'
open(os.path.join(H, 'scene_demo.html'), 'w').write(PAGE % ('scene demo', CSS, body, DEFS))
# ---- نمونهٔ مسیر + قرص سختی روی زمین‌ها
Z = T['zones']; P = T['path']; HD = T['hardness']
def pill(x, y, k):
    h = HD[k]; w = 112
    pk = ''.join('<path d="M%d,%d l6,-11 l6,11z" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (x + 14 + 15 * j, y + 14, h['ink'], h['ink']) for j in range(h['peaks']))
    # راست‌چین: قله‌ها سمت راست، واژه سمت چپ
    return ('<rect x="%d" y="%d" width="%d" height="38" rx="14" fill="%s" stroke="%s" stroke-width="%s"/>%s<text x="%d" y="%d" text-anchor="middle" font-family="Vazirmatn" font-weight="700" font-size="17" fill="%s">%s</text>'
            % (x, y, w, h['hex'], h['outline'], h['outline_px'], '', x + w - 58 + 22, y + 26, h['ink'], STR['difficulty.' + k]['text'])) + \
           ''.join('<path d="M%d,%d l6,-11 l6,11z" fill="%s" stroke="%s" stroke-width="2" stroke-linejoin="round"/>' % (x + 12 + 14 * j, y + 27, h['ink'], h['ink']) for j in range(h['peaks']))
def strip(key, base, y0, city=False):
    d = 'M-10,%d C70,%d 120,%d 190,%d S320,%d 400,%d' % (y0 + 70, y0 + 20, y0 + 100, y0 + 52, y0 + 10, y0 + 56)
    dr = 'M-10,%d C70,%d 120,%d 190,%d' % (y0 + 70, y0 + 20, y0 + 100, y0 + 52)
    dm = 'M190,%d S320,%d 400,%d' % (y0 + 52, y0 + 10, y0 + 56)
    o = '<rect y="%d" width="390" height="130" fill="%s"/>' % (y0, base)
    if city: o += '<path d="%s" fill="none" stroke="%s" stroke-width="%d" stroke-linecap="round"/>' % (d, P['city_foam'], P['outline_px'] + 2 * P['city_foam_px'])
    o += '<path d="%s" fill="none" stroke="%s" stroke-width="%d" stroke-linecap="round"/>' % (d, P['outline'], P['outline_px'])
    o += '<path d="%s" fill="none" stroke="%s" stroke-width="%d" stroke-linecap="round"/>' % (dr, P['cream'], P['fill_px'])
    o += '<path d="%s" fill="none" stroke="%s" stroke-width="%d" stroke-linecap="round"/>' % (dm, P['rest'], P['fill_px'])
    o += '<path d="%s" fill="none" stroke="%s" stroke-width="5" stroke-dasharray="3 14" stroke-linecap="round"/>' % (dm, P['cream'])
    o += '<path d="%s" fill="none" stroke="%s" stroke-width="3.2" stroke-dasharray="10 12"/>' % (dr, P['done_dash'])
    for i, k in enumerate(('easy', 'mid', 'hard')): o += pill(14 + 126 * i, y0 + 80 + (0 if i != 1 else -4), k)
    return o
strips = ''.join(strip(k, base, i * 130, city=(k == 'city')) for i, (k, base) in enumerate((('sports', Z['sports']['base']), ('space', Z['space']['base']), ('farm', Z['farm']['base']), ('city', Z['city']['base']))))
samples = '<svg viewBox="0 0 390 520" width="390" height="520">%s</svg>' % strips
open(os.path.join(H, 'samples_demo.html'), 'w').write(PAGE % ('samples demo', CSS, samples, ''))
print('demos built')
