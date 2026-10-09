#!/usr/bin/env python3
"""مولد دارایی کارت و صحنهٔ اسکله (card-artist، v5 گام ۳). اجرا: python3 gen_card.py  (خروجی: team/assets/card/)
فقط SVG لایه‌ای (brush در هندسه پخته؛ بدون filter/blend)، assets.json، card.css، scene/diagram_style.json."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lib import *
import art, scene
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / 'assets' / 'card'; SC = OUT / 'scene'
OUT.mkdir(parents=True, exist_ok=True); SC.mkdir(exist_ok=True)
ZONE = '#5fa8d6'   # شب بندر (zone_tokens.json zones.city.night)
CARD_BG, TEXT_BG, SHELF, NLINE = '#190539', '#12243a', '#2a1f5c', '#0d0426'
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

# ---- قاب شب 390×392 (کارت جلو) ----
fr = rr(16, 6, 358, 382, 22, 5)
glow = ''.join(f'<path d="{pd(brush(fr, 1.5, 7))}" fill="none" stroke="{ZONE}" stroke-width="{w}" stroke-linejoin="round" opacity="{o}"/>' for w, o in ((42, .05), (32, .07), (22, .10), (14, .14)))
body = g('cd-frame-glow', glow)
body += g('cd-frame-band', S(fr, CARD_BG, 6, 7, ZONE))
body += g('cd-frame-inner', S(rr(26, 16, 338, 362, 16, 4), 'none', 2.6, 0, ZONE, extra='opacity=".55"'))
body += g('cd-frame-slot', S(rr(28, 92, 334, 150, 10, 4), LINE, 4.5, 8, LINE))
body += g('cd-frame-text', S(rr(28, 250, 334, 56, 10, 4), TEXT_BG, 2.6, 0, ZONE, extra='stroke-opacity=".6"'))
add('frame_night', (0, 0, 390, 392), nse(body), 'frame', extra_meta=dict(slots=dict(badge='28,10 56x30 (بالا-ابتدا؛ واژه کنارش)', title='24,40 342x46', image='28,92 334x150', sentence='28,250 334x56', button='28,314 334x48'), stretch='preserveAspectRatio=none + non-scaling-stroke'))
# قاب تصویر (روی هنر)
add('image_border', (0, 0, 334, 150), nse(g('cd-ib-line', S(rr(2.25, 2.25, 329.5, 145.5, 10, 4), 'none', 4.5, 9, LINE))), 'overlay')
# ---- نوار عنوان 360×60 ----
tb = rr(14, 9, 332, 42, 12, 4)
tbody = g('cd-tb-glow', f'<path d="{pd(brush(tb, 1.1, 3))}" fill="none" stroke="{ZONE}" stroke-width="12" stroke-linejoin="round" opacity=".16"/><path d="{pd(brush(tb, 1.1, 3))}" fill="none" stroke="{ZONE}" stroke-width="8" stroke-linejoin="round" opacity=".22"/>')
tbody += g('cd-tb-plaque', S(tb, SHELF, 4.5, 3, ZONE))
add('title_bar', (0, 0, 360, 60), tbody, 'title-plaque', extra_meta=dict(text='Lalezar >=24px، تیتر از strings؛ درخشش متن = text-shadow CSS (غیر از filter)'))
# ---- نوار عقب 360×56 ----
sp = rr(8, 6, 344, 44, 12, 4)
add('stack_strip', (0, 0, 360, 56), g('cd-st-band', S(sp, '#241056', 4.5, 5, '#3d7fa8')) + g('cd-st-line', S(rr(14, 12, 332, 32, 8, 3), 'none', 1.2, 0, '#3d7fa8', extra='opacity=".5"')), 'strip', extra_meta=dict(note='بی‌درخشش؛ قرص سختی ui + واژه در HTML؛ کل نوار هدف لمس'))
# ---- قفسه 360×40 ----
sh = g('cd-sh-top', S([(0, 8), (360, 8), (350, 19), (10, 19)], '#3a2a7a', 2.6, 0, NLINE)) + L([(10, 9.5), (350, 9.5)], ZONE, 1.2, .8)
sh += g('cd-sh-front', S(rr(10, 19, 340, 13, 2), SHELF, 2.6, 0, NLINE))
sh += g('cd-sh-brackets', S([(36, 32), (56, 32), (36, 40)], SHELF, 2.6, 0, NLINE) + S([(304, 32), (324, 32), (324, 40)], SHELF, 2.6, 0, NLINE))
add('shelf', (0, 0, 360, 40), sh, 'shelf')
# ---- مینی کارت ۴ حالت ----
def mini(ox, kind):
    c = rr(ox + 2, 2, 76, 116, 10, 4)
    if kind == 'seen':
        s = S(c, '#2fb8a8', 4.5, 11, '#a9f0e6') + S(rr(ox + 10, 10, 60, 44, 6, 3), LINE, 2.6, 0, LINE)
        s += S(el(ox + 40, 76, 16, 9, 14), '#fff4d2', 2.6) + S(el(ox + 40, 76, 5, 5, 8), '#3a2a7a', 2.6)
    elif kind == 'packed':
        s = S(c, '#8a4fd0', 4.5, 12, '#c9a3f0') + S(rr(ox + 10, 10, 60, 44, 6, 3), LINE, 2.6, 0, LINE)
        s += S([(ox + 26, 70), (ox + 40, 64), (ox + 54, 70), (ox + 54, 86), (ox + 40, 92), (ox + 26, 86)], '#fff4d2', 2.6) + L([(ox + 26, 70), (ox + 40, 76), (ox + 54, 70)], LINE, 2.6) + L([(ox + 40, 76), (ox + 40, 92)], LINE, 2.6)
    elif kind == 'empty':
        s = f'<path d="{pd(c)}" fill="none" stroke="#8a4fd0" stroke-width="2.6" stroke-dasharray="7 6" stroke-linejoin="round"/>' + L([(ox + 40, 48), (ox + 40, 72)], '#c9a3f0', 2.6) + L([(ox + 28, 60), (ox + 52, 60)], '#c9a3f0', 2.6)
    else:
        s = S(c, '#241056', 4.5, 13, '#5b3490') + S(el(ox + 40, 56, 16, 16, 14), '#3a2a7a', 2.6)
        s += L([(ox + 34, 55), (ox + 34, 51), (ox + 37, 47), (ox + 43, 47), (ox + 46, 51), (ox + 46, 55)], '#fff4d2', 2.6) + S(rr(ox + 32, 54, 16, 12, 3), '#fff4d2', 0) + f'<circle cx="{ox + 40}" cy="60" r="1.8" fill="#3a2a7a"/>'
    return s
mb = ''
for i, k in enumerate(('seen', 'packed', 'empty', 'locked')):
    mb += g(f'cd-mc-{k}', mini(i * 88, k), f'transform="translate(0 0)"')
    syms.append(symbol(f'cd-mini-{k}', (0, 0, 80, 120), mini(0, k)))
add('mini_card_4states', (0, 0, 344, 120), mb, 'mini-card', symid='cd-mini-4states')
# ---- پشت کارت: نمودار قرقره 360×200 ----
d = g('cd-bd-panel', S(rr(8, 6, 344, 188, 14, 5), '#d6f1ee', 4.5, 21))
d += g('cd-bd-beam', S(rr(60, 16, 240, 14, 3), '#3a2a7a', 4.5, 22))
def wheelb(cx, cy, r, sd):
    return S(el(cx, cy, r, r, 16), '#fff4d2', 4.5, sd) + S(el(cx, cy, r * .3, r * .3, 8), '#3a2a7a', 2.6)
d += g('cd-bd-fixed', L([(210, 30), (210, 46)], LINE, 2.6) + wheelb(210, 66, 20, 23))
d += g('cd-bd-moving', L([(150, 140), (150, 152)], LINE, 2.6) + wheelb(150, 118, 22, 24))
under = [(128, 118), (131, 130), (140, 138), (150, 140), (160, 138), (169, 130), (172, 118)]
over = [(190, 66), (192, 56), (198, 49), (210, 46), (222, 49), (228, 56), (230, 66)]
rp = [(130, 30), (130, 118)] + under[1:-1] + [(172, 118), (190, 66)] + over[1:-1] + [(230, 66), (230, 160)]
d += g('cd-bd-rope', tube(rp, 4, '#c98a45', 2.6, 0, jit=False))
d += g('cd-bd-load', S(rr(124, 152, 52, 36, 4), '#c98a45', 4.5, 25) + L([(124, 152), (176, 188)], LINE, 1.2, .5) + L([(176, 152), (124, 188)], LINE, 1.2, .5))
d += g('cd-bd-arrows', S([(96, 146), (104, 146), (104, 164), (112, 164), (100, 184), (88, 164), (96, 164)], '#d070c0', 2.6, extra='class="farr"') + S([(226, 150), (234, 150), (234, 166), (242, 166), (230, 186), (218, 166), (226, 166)], '#2fb8a8', 2.6, extra='class="farr"'))
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
 'colors': {'rope': '#c98a45', 'wheel_fill': '#fff4d2', 'wheel_hub': '#3a2a7a', 'beam': '#3a2a7a', 'load': '#c98a45', 'panel': '#d6f1ee', 'arrow_pull': '#2fb8a8', 'arrow_weight': '#d070c0'},
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

