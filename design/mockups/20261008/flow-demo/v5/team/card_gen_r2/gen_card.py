#!/usr/bin/env python3
"""مولد دارایی کارت و صحنهٔ اسکله (card-artist، دور ۲: بازگشت به رنگ و کنتراست v4). اجرا: python3 gen_card.py  (خروجی: team/assets_r2/card/)
فقط SVG لایه‌ای (brush در هندسه پخته؛ بدون filter/blend)، assets.json، card.css، scene/diagram_style.json."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lib import *
import art, scene
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / 'assets_r2' / 'card'; SC = OUT / 'scene'
OUT.mkdir(parents=True, exist_ok=True); SC.mkdir(exist_ok=True)
ZONE = '#46f0d8'   # نئون فیروزه‌ای (v4: درخشش کارت شب)
FACE, PLATE, DARK, YEL, PINK, VIO, VIOL = '#25cdc0', '#07203a', '#190539', '#ffd23f', '#ff7be5', '#5b3fe0', '#a99dff'
CARD_BG, TEXT_BG, SHELF, NLINE = DARK, PLATE, '#2a1f5c', '#0d0426'
import math
NS = ' xmlns="http://www.w3.org/2000/svg"'
files = {}      # نام فایل -> (viewBox, body, id)
syms = []       # symbolها برای sprite
syms_sc = []    # symbolهای صحنه (scene/sprite_scene.svg)
meta = {}
def add(name, vb, body, role, anchor='top-start', layers=None, extra_meta=None, folder=OUT, symid=None):
    (folder / f'{name}.svg').write_text(svg(vb, body), encoding='utf-8')
    sid = symid or 'cd-' + name.replace('_', '-')
    (syms_sc if folder == SC else syms).append(symbol(sid, vb, body))
    meta[sid] = dict(file=('scene/' if folder == SC else '') + name + '.svg', viewBox=' '.join(n(v) for v in vb), role=role, anchor=anchor, layers=layers or re_layers(body), **(extra_meta or {}))
def re_layers(body):
    import re
    return re.findall(r'<g id="([^"]+)"', body)
def nse(s): return s.replace('<path ', '<path vector-effect="non-scaling-stroke" ')
def gl(pts, col, ws, amp=2.8, seed=7, step=9):
    """درخشش نئونی ایستا: چند stroke پهن و کم‌رنگ، بدون filter"""
    return ''.join(f'<path d="{pd(brush(pts, amp, seed, step))}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linejoin="round" opacity="{o}"/>' for w, o in ws)
def plate(y0, x0=24, x1=366, yb=380, r=16, seed=3):
    """صفحهٔ تیرهٔ متن: لبهٔ بالای موجی (v4)، گوشه‌های پایین هم‌شکل کارت"""
    top = [(x, y0 + 4 * math.sin((x - x0) / 21.0 + seed)) for x in range(x0, x1 + 1, 6)]
    br = el(x1 - r, yb - r, r, r, 6, 0, 90, False); bl = el(x0 + r, yb - r, r, r, 6, 90, 180, False)
    return top + br + bl
def frame_body(plate_y, slot):
    fr = rr(16, 6, 358, 382, 22, 5)
    body = g('cd-frame-glow', gl(fr, ZONE, ((34, .12), (26, .2), (18, .32), (11, .52))))
    body += g('cd-frame-band', S(fr, FACE, 4.5, 7, DARK, amp=2.8, step=9))
    body += g('cd-frame-plate', S(plate(plate_y), PLATE, 0, 3))
    body += g('cd-frame-trim', S(rr(24, 14, 342, 366, 16, 5), 'none', 3, 5, YEL, amp=1.0, step=12))
    if slot: body += g('cd-frame-slot', S(rr(28, 92, 334, 150, 10, 4), DARK, 4.5, 8, DARK))
    return nse(body)
# ---- قاب کارت جلو 390×392: بالا فیروزه‌ای، صفحهٔ تیرهٔ متن از y=248 ----
add('frame_night', (0, 0, 390, 392), frame_body(248, True), 'frame', extra_meta=dict(slots=dict(badge='28,10 56x30 (بالا-ابتدا؛ واژه کنارش، متن تیره روی فیروزه‌ای)', title='24,40 342x46', image='28,92 334x150', sentence='28,250 334x56 روی صفحهٔ تیره', button='28,314 334x48'), stretch='preserveAspectRatio=none + non-scaling-stroke'))
# ---- قاب درس/پشت کارت 390×392 (کشیده می‌شود): نوار فیروزه‌ای باریک بالا، صفحهٔ تیره از y=48 ----
add('frame_lesson', (0, 0, 390, 392), frame_body(48, False), 'frame', extra_meta=dict(note='برای هر دو روی کارتِ بزرگِ درس (.cface) و پشت کارت؛ متن بلند روی صفحهٔ تیره می‌افتد، نه فیروزه‌ای', stretch='preserveAspectRatio=none + non-scaling-stroke'))
# قاب تصویر (روی هنر): خط تیره 4.5 + خط کرم داخلی 2.6 (v4)
add('image_border', (0, 0, 334, 150), nse(g('cd-ib-line', S(rr(2.25, 2.25, 329.5, 145.5, 10, 4), 'none', 4.5, 9, DARK) + S(rr(6.5, 6.5, 321, 137, 7, 4), 'none', 2.6, 0, '#fff3c4', extra='opacity=".9"'))), 'overlay')
# ---- نوار عنوان 360×60: پلاک بنفش پررنگ با لبهٔ صورتی نئونی ----
tb = rr(14, 9, 332, 42, 12, 4)
tbody = g('cd-tb-glow', gl(tb, PINK, ((14, .18), (9, .3)), 1.1, 3, 10))
tbody += g('cd-tb-plaque', S(tb, '#3b1190', 4.5, 3, DARK, amp=2.0, step=10) + S(rr(19.5, 14.5, 321, 31, 8, 3), 'none', 2.6, 0, PINK, extra='opacity=".9"'))
add('title_bar', (0, 0, 360, 60), nse(tbody), 'title-plaque', extra_meta=dict(text='Lalezar >=24px سفید + text-shadow صورتی (CSS)؛ تیتر از strings'))
# ---- نوار عقب 360×56: کارت بنفش پررنگ (v4 «جمع‌شده») با درخشش ----
sp = rr(8, 6, 344, 44, 12, 4)
add('stack_strip', (0, 0, 360, 56), nse(g('cd-st-glow', gl(sp, VIOL, ((13, .14), (8, .26)), 1.4, 5, 10)) + g('cd-st-band', S(sp, VIO, 4.5, 5, DARK, amp=2.0, step=10)) + g('cd-st-line', S(rr(14, 12, 332, 32, 8, 3), 'none', 2.6, 0, VIOL, extra='opacity=".85"'))), 'strip', extra_meta=dict(note='قرص سختی ui + واژه در HTML؛ متن کرم؛ کل نوار هدف لمس'))
# ---- قفسهٔ چوبی 360×40 (v4: تخته‌ی چوبی با براکت) ----
sh = g('cd-sh-top', S([(10, 5), (350, 5), (360, 17), (0, 17)], '#e0a45c', 4.5, 41, DARK))
sh += g('cd-sh-front', S(rr(0, 17, 360, 14, 3), '#9a5f2e', 4.5, 42, DARK))
sh += g('cd-sh-grain', L([(18, 24), (90, 24)], '#5e3a1a', 2.6) + L([(120, 23), (210, 23)], '#5e3a1a', 2.6) + L([(236, 25), (330, 25)], '#5e3a1a', 2.6) + L([(60, 11), (150, 11)], '#8a5a2e', 2.6) + L([(200, 10), (300, 10)], '#8a5a2e', 2.6))
sh += g('cd-sh-brackets', S([(40, 31), (40, 40), (70, 31)], '#9a5f2e', 2.6, 0, DARK) + S([(290, 31), (320, 40), (320, 31)], '#9a5f2e', 2.6, 0, DARK))
add('shelf', (0, 0, 360, 40), sh, 'shelf')
# ---- مینی کارت ۴ حالت (80×120؛ کارت داخل حاشیهٔ ۵ برای درخشش؛ non-scaling-stroke) ----
def mini(ox, kind):
    c = rr(ox + 6, 6, 68, 108, 10, 4)
    trim = S(rr(ox + 11, 11, 58, 98, 7, 3), 'none', 2.6, 0, YEL, extra='opacity=".9"')
    if kind == 'seen':
        s = gl(c, ZONE, ((12, .28), (7, .5)), 1.2, 11, 10) + S(c, FACE, 4.5, 11, DARK) + trim
    elif kind == 'packed':
        s = gl(c, VIOL, ((12, .28), (7, .5)), 1.2, 12, 10) + S(c, VIO, 4.5, 12, DARK) + trim
    elif kind == 'empty':
        s = S(c, DARK, 0) + f'<path d="{pd(c)}" fill="none" stroke="#9a78e0" stroke-width="2.6" stroke-dasharray="7 6" stroke-linejoin="round"/>' + L([(ox + 40, 52), (ox + 40, 76)], '#b99cf0', 4.5) + L([(ox + 28, 64), (ox + 52, 64)], '#b99cf0', 4.5)
    else:
        s = S(c, '#34145f', 4.5, 13, DARK) + f'<clipPath id="cd-mlk"><path d="{pd(c)}"/></clipPath><g clip-path="url(#cd-mlk)">' + ''.join(L([(ox + 0, y), (ox + 80, y - 30)], '#5a2fa0', 2.6, .7) for y in (40, 70, 100, 130)) + '</g>' + S(rr(ox + 6, 6, 68, 108, 10, 4), 'none', 4.5, 13, DARK)
        s += L(bez((ox + 31, 58), (ox + 30, 38), (ox + 50, 38), (ox + 49, 58), 8), '#cdb8ff', 4.5) + S(rr(ox + 26, 56, 28, 22, 5), '#cdb8ff', 2.6, 0, DARK) + f'<circle cx="{ox + 40}" cy="66" r="3" fill="{DARK}"/>' + L([(ox + 40, 66), (ox + 40, 72)], DARK, 2.6)
    return nse(s)
mb = ''
for i, k in enumerate(('seen', 'packed', 'empty', 'locked')):
    mb += g(f'cd-mc-{k}', mini(i * 88, k), f'transform="translate(0 0)"')
    syms.append(symbol(f'cd-mini-{k}', (0, 0, 80, 120), mini(0, k)))
add('mini_card_4states', (0, 0, 344, 120), mb, 'mini-card', symid='cd-mini-4states')
# ---- پس‌زمینهٔ شب v4: ستاره، جرقه، چرخ‌دنده (روی گرادیان CSS) 390×800 ----
def night_bg_body():
    r = random.Random(3); s = ''
    for _ in range(70):
        x, y, rad = r.uniform(4, 386), r.uniform(4, 796), r.choice([.8, 1, 1.2, 1.6])
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="#e9dcff" opacity="{r.uniform(.35, .9):.2f}"/>'
    sp_ = ''
    for _ in range(7):
        x, y, rr_ = r.uniform(15, 375), r.uniform(15, 785), r.uniform(5, 9)
        sp_ += f'<path d="M{x:.1f},{y - rr_:.1f} l{rr_ * .18:.1f},{rr_ * .82:.1f} l{rr_ * .82:.1f},-{rr_ * .18:.1f} l-{rr_ * .82:.1f},{rr_ * .18:.1f} l-{rr_ * .18:.1f},{rr_ * .82:.1f} l-{rr_ * .18:.1f},-{rr_ * .82:.1f}z" fill="#ffd9ff" opacity=".75"/>'
    def cog(cx, cy, rad, op):
        pp = []
        for i in range(20):
            a = math.pi * i / 10; rr2 = rad if i % 2 == 0 else rad * .78
            for da in (-.1, .1): pp.append(f'{cx + rr2 * math.cos(a + da):.1f},{cy + rr2 * math.sin(a + da):.1f}')
        return f'<g opacity="{op}"><polygon points="{" ".join(pp)}" fill="#c9a6ff"/><circle cx="{cx}" cy="{cy}" r="{rad * .35:.1f}" fill="{DARK}"/></g>'
    return g('cd-nb-stars', s) + g('cd-nb-sparks', sp_) + g('cd-nb-cogs', cog(300, 710, 70, .1) + cog(40, 120, 46, .08))
add('night_bg', (0, 0, 390, 800), night_bg_body(), 'bg', extra_meta=dict(note='لایهٔ ستاره/چرخ‌دنده؛ گرادیان‌های بنفش/سرخابی در CSS (.cd-nightbg)'))
# ---- پشت کارت: نمودار قرقره 360×200 ----
d = g('cd-bd-panel', S(rr(8, 6, 344, 188, 14, 5), '#cdf7ff', 4.5, 21))
d += g('cd-bd-beam', S(rr(60, 16, 240, 14, 3), VIO, 4.5, 22))
def wheelb(cx, cy, r, sd):
    return S(el(cx, cy, r, r, 16), '#fff4d2', 4.5, sd) + S(el(cx, cy, r * .3, r * .3, 8), VIO, 2.6)
d += g('cd-bd-fixed', L([(210, 30), (210, 46)], LINE, 2.6) + wheelb(210, 66, 20, 23))
d += g('cd-bd-moving', L([(150, 140), (150, 152)], LINE, 2.6) + wheelb(150, 118, 22, 24))
under = [(128, 118), (131, 130), (140, 138), (150, 140), (160, 138), (169, 130), (172, 118)]
over = [(190, 66), (192, 56), (198, 49), (210, 46), (222, 49), (228, 56), (230, 66)]
rp = [(130, 30), (130, 118)] + under[1:-1] + [(172, 118), (190, 66)] + over[1:-1] + [(230, 66), (230, 160)]
d += g('cd-bd-rope', tube(rp, 4, '#f0a848', 2.6, 0, jit=False))
d += g('cd-bd-load', S(rr(124, 152, 52, 36, 4), '#f09a38', 4.5, 25) + L([(124, 152), (176, 188)], LINE, 1.2, .5) + L([(176, 152), (124, 188)], LINE, 1.2, .5))
d += g('cd-bd-arrows', S([(96, 146), (104, 146), (104, 164), (112, 164), (100, 184), (88, 164), (96, 164)], '#ff4fc0', 2.6, extra='class="farr"') + S([(226, 150), (234, 150), (234, 166), (242, 166), (230, 186), (218, 166), (226, 166)], '#14d4b8', 2.6, extra='class="farr"'))
add('back_pulley_diagram', (0, 0, 360, 200), d, 'diagram', extra_meta=dict(note='بدون متن؛ وزن=صورتی، کشیدن=فیروزه‌ای (همان دو رنگ صحنه)'))
# ---- هنرها ----
add('art_harbor_day', (0, 0, 360, 240), art.art_day('cd-ad'), 'art', anchor='center', extra_meta=dict(safe='x20..340 y45..195', adventure=1, light='day'))
add('art_harbor_dusk', (0, 0, 360, 240), art.art_dusk('cd-au'), 'art', anchor='center', extra_meta=dict(safe='x20..340 y45..195', adventure=2, light='dusk'))
add('art_harbor_night', (0, 0, 360, 240), art.art_night('cd-an'), 'art', anchor='center', extra_meta=dict(safe='x20..340 y45..195', adventure=3, light='night'))
# ---- بنر محیط (همان هنر روز، برش 390×200) ----
add('harbor_env_banner', (0, 30, 360, 185), art.art_day('cd-bn'), 'banner', anchor='center', folder=SC, symid='cd-harbor-banner')
# ---- صحنه‌ها ----
parts_done = False
for nm, (tone, bg, load) in scene.SCENES.items():
    p = 'cd-' + {'harbor_scene_green': 'sg', 'harbor_scene_orange': 'so', 'harbor_scene_orange_dusk': 'sod', 'harbor_scene_red': 'sr', 'harbor_scene_red_night': 'srn'}[nm]
    b = scene.build(p, tone, bg, load)
    add(nm, (0, 0, 390, 500), b, 'scene', anchor='top-start', folder=SC, symid='cd-' + nm.replace('_', '-'),
        extra_meta=dict(tone=tone, background=bg, load=load, origins=dict([(k, v) for k, v in __import__('re').findall(r'id="([^"]*-(?:wheel1|wheel2|rope|net))" data-origin="([^"]+)"', b)])))
    if nm == 'harbor_scene_green':
        L_ = scene.LAST
        add('crane', (90, 28, 230, 128), g('cd-cr-gantry', L_['gantry']) + g('cd-cr-wheel1', L_['w1'], 'data-origin="130 76"') + g('cd-cr-wheel2', L_['w2'], 'data-origin="222 76"'), 'part', folder=SC, symid='cd-crane')
        add('net_rope', (60, 300, 90, 110), g('cd-nr-rope', L_['rope']) + g('cd-nr-net', scene.net('cd-nr', scene.PAL['day'], 'fish'), 'data-origin="104 320"'), 'part', folder=SC, symid='cd-net-rope')
        add('pulley_wheel', (96, 42, 68, 68), g('cd-pw-wheel', scene.wheel('cd-pw', 130, 76, scene.PAL['day'], 5), 'data-origin="130 76"'), 'part', folder=SC, symid='cd-pulley-wheel')
# ---- diagram_style.json ----
(SC / 'diagram_style.json').write_text(json.dumps({
 '_doc': 'سبک نمودارهای JS صحنه (قرقره/طناب/فلش) به زبان نو؛ توسعه اعمال می‌کند. منبع: STYLE_BIBLE بخش ۲ و ۳.',
 'line': {'color': '#241a5e', 'color_night': '#0d0426', 'steps_px': [6, 4.5, 2.6, 1.2], 'main_object_px': 4.5, 'rope_outline_px': 2.6, 'rope_core_px': 4, 'join': 'round', 'cap': 'round'},
 'brush': 'در هندسه پخته؛ نمودارهای JS قلم‌مویی نمی‌شوند و خط صاف 4.5 می‌گیرند (بدون filter)',
 'colors': {'rope': '#f0a848', 'wheel_fill': '#fff4d2', 'wheel_hub': '#5b3fe0', 'beam': '#5b3fe0', 'load': '#f09a38', 'panel': '#cdf7ff', 'arrow_pull': '#14d4b8', 'arrow_weight': '#ff4fc0'},
 'arrows': {'rule': 'دو رنگ تخت، خط دور 2.6، class=farr، بدون متن روی فلش', 'shaft_w': 8, 'head_w': 24, 'head_h': 20},
 'text_on_diagram': False, 'min_text_px': 14, 'forbidden': ['filter', 'mix-blend-mode', 'متن روی طناب یا فلش', 'قرمز/نارنجی/سبز به‌جز نشان سختی'],
}, ensure_ascii=False, indent=1), encoding='utf-8')
# ---- sprite و assets.json ----
(SC / 'sprite_scene.svg').write_text(f'<svg{NS}>' + ''.join(syms_sc) + '</svg>', encoding='utf-8')
(OUT / 'sprite_card.svg').write_text(f'<svg{NS}>' + ''.join(syms) + '</svg>', encoding='utf-8')
(OUT / 'assets.json').write_text(json.dumps({'sprite': 'sprite_card.svg', 'sprite_scene': 'scene/sprite_scene.svg', 'prefix': 'cd-', 'zone_night': ZONE, 'assets': meta}, ensure_ascii=False, indent=1), encoding='utf-8')
tot = sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file() and p.suffix in ('.svg', '.json', '.css'))
print('files', len(meta), 'total KB', round(tot / 1024, 1))
for p in sorted(OUT.rglob('*.svg')): print(round(p.stat().st_size / 1024, 1), p.relative_to(OUT))

