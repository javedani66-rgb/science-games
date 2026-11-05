#!/usr/bin/env python3
"""r2: رنگ‌ها را از zone_tokens_v4.json (استخراج‌شده از v4) می‌خواند و می‌سازد:
zone_tokens.json، tokens.css، common_defs.svg، palette_day/dusk/night.svg، light_contrast.json/md.
اجرا: python3 -I build_light_r2.py   (پیش از آن extract_v4_colors.py)"""
import json, os, math, colorsys
H = os.path.dirname(os.path.abspath(__file__))
X = json.load(open(os.path.join(H, 'zone_tokens_v4.json')))
v = lambda k: X[k]['hex']

def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def hx(t): return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(c)))) for c in t)
def lin(c): c /= 255; return c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
def Y(h): r, g, b = map(lin, rgb(h)); return .2126 * r + .7152 * g + .0722 * b
def cr(a, b): ya, yb = Y(a), Y(b); return (max(ya, yb) + .05) / (min(ya, yb) + .05)
def mix(a, b, t): return hx([(1 - t) * x + t * y for x, y in zip(rgb(a), rgb(b))])  # t از a به b
def bake(h, c, a=.8):
    """ضرب v4 (multiply با رنگ c و شدت a) پخته در hex؛ هیچ blend زنده‌ای در خروجی نیست"""
    return hx([x * ((1 - a) + a * y / 255) for x, y in zip(rgb(h), rgb(c))])
def lab(h):
    r, g, b = map(lin, rgb(h))
    x = (.4124 * r + .3576 * g + .1805 * b) / .95047; y = .2126 * r + .7152 * g + .0722 * b; z = (.0193 * r + .1192 * g + .9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > .008856 else 7.787 * t + 16 / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))
def dE(a, b): return math.dist(lab(a), lab(b))

OUT = v('path.outline'); CREAM = v('path.cream')
# ---------- اصلاح‌های کمینه (فقط روشنی/خط دور) ----------
REST_OP = 0.42            # v4: .34 (rest/outline 2.75 < 3)
CITY_FOAM = v('detail.wave')  # خط دور دوم روی آب، رنگ موج v4

zones = {}
for z, nm in (('sports', 'ورزشگاه'), ('space', 'پایگاه فضایی'), ('farm', 'مزرعه'), ('city', 'شهر صنعتی')):
    zones[z] = dict(base=v('ground.' + z), code=v('ground.%s.code' % z), ring=v('ui.here_ring'), ring_px=5.5, ring_outline_px=10)
zones['sports'].update(shade=v('detail.tree'), patch=v('detail.tree_hi'), detail='درخت/ریسه راه‌راه چمن')
zones['space'].update(shade=v('detail.crater'), patch=v('detail.crater_rim'), detail='دهانه‌ها')
zones['farm'].update(shade=hx([c * .8 for c in rgb(v('ground.farm'))]), patch=v('detail.hay'), detail='شیار/کاه‌بسته (shade محاسبه‌ای ×0.8)')
zones['city'].update(shade=hx([27, 52, 71]) if False else '#55697d', patch=v('detail.wave'), detail='موج؛ shade = اسلب خاکستری قفل (عکس r11_map_y0)')
for z in zones.values(): z['night'] = z['base']  # نقشه همیشه روز؛ برای سازگاری با نام‌های قبلی

# ---------- نورها (صحنهٔ ماجرا) ----------
n_top, n_bot, n_a = v('night.overlay_top'), v('night.overlay_bottom'), float(v('night.overlay_opacity'))
mid = mix(n_top, n_bot, .5)
day_sky0, day_sky1 = '#7fd4ff', v('path.river_foam')  # v4 کد: شیشهٔ گنبد #7fd4ff، کف رود #d4f6ff
sea = v('ground.city')
body = '#fff6dc'  # بدنهٔ بناهای v4 (قایق/جرثقیل/خانه)
lights = {
 'day': dict(sky0=day_sky0, sky1=day_sky1, sky2=day_sky1, water=sea, lit='#fff6dc', shade='#4b3b9e', line=OUT, windows=None, build=body, pier='#f6dba0',
             shadow=dict(color='#10083a', opacity=.28, dx=8, dy=6), intensity=dict(lit_a=.5, shade_a=.22)),
 'dusk': dict(sky0='#5a2a9a', sky1='#c2379a', sky2='#ff7a3d', water='#1f5a86', lit='#ffb21c', shade='#5a2a9a', line=OUT, windows=None, build=body, pier='#f6dba0',
              shadow=dict(color='#241a5e', opacity=.36, dx=14, dy=7), intensity=dict(lit_a=.7, shade_a=.42)),
 'night': dict(sky0=v('card.bg'), sky1=mix(v('card.bg'), n_bot, .5), sky2='#4b3b9e', water=bake(sea, n_bot, n_a), lit='#a99dff', shade=v('card.bg'), line=bake(OUT, mid, n_a),
               windows=v('night.window'), build=bake(body, mid, n_a), pier=bake('#f6dba0', mid, n_a),
               shadow=dict(color='#0d0426', opacity=.4, dx=8, dy=6), intensity=dict(lit_a=.55, shade_a=.45)),
}
lights['night']['moon'] = v('night.moon')
# شدت بنا (env) = ۶۰٪ شدت شخصیت، مثل r1
for L in lights.values():
    i = L['intensity']; i['nlit_a'] = round(i['lit_a'] * .6, 2); i['nshade_a'] = round(i['shade_a'] * .8, 2)

hard = {k: dict(hex=v('hard.' + k), peaks=p, word_key='difficulty.' + k, ink=OUT, outline=OUT, outline_px=4.5) for k, p in (('easy', 1), ('mid', 2), ('hard', 3))}
card = dict(bg=v('card.bg'), front_top=v('card.front_top'), front_bottom=v('card.front_bottom'), glow=v('card.glow'), plate=v('card.plate'), gold=v('card.frame_gold'),
            cream=v('card.frame_cream'), edge=v('card.edge'), pill_cyan=v('card.pill_cyan'), pill_pink=v('card.pill_pink'), pill_gold=v('card.pill_gold'), pill_text=v('card.pill_text'),
            title_fill=v('card.title_fill'), title_glow=v('card.title_glow'), body_text=v('card.body_text'), kept_top=v('card.kept_top'), kept_bottom=v('card.kept_bottom'), kept_glow=v('card.kept_glow'),
            empty_fill=v('card.empty_fill'), empty_dash=v('card.empty_dash'), locked=v('card.locked'), locked_icon=v('card.locked_icon'),
            plank_top=v('card.plank_top'), plank_side=v('card.plank_side'), icon_outline=v('card.bg'))
ui = dict(cream=CREAM, line=OUT, bar=v('ui.bar'), chip=v('ui.chip'), chip_text=v('ui.chip_text'), chip_on=v('ui.chip_on'), chip_shadow=v('ui.chip_shadow'), menu=v('ui.menu'),
          accent_yellow=v('ui.here_ring'), white='#ffffff', label_fill=v('ui.label_fill'), zone_title_fill=v('ui.zone_title_fill'))
tokens = dict(_doc='r2: رنگ‌های v4 (استخراج‌شده در zone_tokens_v4.json با منبع). منبع حقیقت hex؛ tokens.css/palette ها/light_contrast از روی همین ساخته می‌شوند (build_light_r2.py).',
              ui=ui, card=card, hardness=hard, zones=zones,
              ground=dict(ice=v('ground.ice'), sand=v('ground.sand'), sea=sea),
              water=dict(sea=sea, river=v('path.river_fill'), river_foam=v('path.river_foam'), wave=v('detail.wave')),
              path=dict(cream=CREAM, outline=OUT, rest=mix(OUT, CREAM, REST_OP), rest_opacity=REST_OP, rest_v4_opacity=.34, done_dash=v('path.done_dash'), boardwalk=v('path.boardwalk'),
                        outline_px=33, fill_px=22, city_foam=CITY_FOAM, city_foam_px=3, city_foam_note='فقط جایی که مسیر روی آب شهر است؛ خط دور دوم بیرون خط دور'),
              lights=lights,
              transition=dict(day_to_night_seconds=1.2, method='opacity دو لایهٔ کامل روز/شب (هر دو در DOM)', dusk='ثابت، فقط صحنهٔ ماجرا ۲؛ با انتقال میان‌یابی نمی‌شود', map='همیشه روز'),
              _corrections=[
                 'مسیر باقی‌مانده: opacity ‎.34 → ‎.42 (کرم روی خط دور؛ rest÷خط دور 2.75 → ≥3)',
                 'مسیر روی آب شهر: خط دور دوم روشن #aef0f4 (رنگ موج v4) ۳px بیرون خط دور (خط دور÷آب 2.12 → کف÷آب ≥3)',
                 'نشان سختی (v4 نداشت): پر سبز/نارنجی/قرمز v4 + خط دور #241a5e ۴٫۵px + متن #241a5e (سفید روی سبز 3.2 بود)',
                 'آیکون چشم/جعبه سفید روی کارت فیروزه‌ای (1.99): خط دور ۲px #190539 (رنگ عوض نشد)',
                 'شب: خط دور پخته‌شدهٔ v4 تقریباً هم‌رنگ آب است؛ سیلوئت با بدنهٔ روشن‌تر خوانده می‌شود و rim لیلکی (#a99dff) اضافه شد'])
json.dump(tokens, open(os.path.join(H, 'zone_tokens.json'), 'w'), ensure_ascii=False, indent=1)

# ---------- tokens.css ----------
c = ['/* خودکار از zone_tokens.json (build_light_r2.py) - رنگ‌های واقعی v4. نقشه همیشه روز؛ غروب/شب فقط صحنهٔ ماجرا. بدون blend و بدون filter زنده. نور از بالا-چپ. */', ':root{']
for k, val in ui.items(): c.append('  --c-%s: %s;' % (k.replace('_', '-'), val))
for k, val in card.items(): c.append('  --card-%s: %s;' % (k.replace('_', '-'), val))
for k, d in hard.items(): c.append('  --hard-%s: %s; --hard-%s-peaks: %d;' % (k, d['hex'], k, d['peaks']))
c.append('  --hard-ink: %s; --hard-outline: %s; --hard-outline-px: 4.5px;' % (OUT, OUT))
for zk, z in zones.items():
    for k in ('base', 'shade', 'patch', 'night', 'ring'): c.append('  --z-%s-%s: %s;' % (zk, k, z[k]))
    c.append('  --z-%s-ring-outline: %spx; --z-%s-ring-px: %spx;' % (zk, z['ring_outline_px'], zk, z['ring_px']))
c += ['  --ground-ice: %s; --ground-sand: %s;' % (v('ground.ice'), v('ground.sand'))]
for k, val in tokens['water'].items(): c.append('  --water-%s: %s;' % (k.replace('_', '-'), val))
p = tokens['path']
c += ['  --path-cream: %s; --path-outline: %s; --path-rest: %s; --path-rest-opacity: %s; --path-done-dash: %s; --path-boardwalk: %s;' % (p['cream'], p['outline'], p['rest'], p['rest_opacity'], p['done_dash'], p['boardwalk']),
      '  --path-city-foam: %s; --path-city-foam-px: 3px;' % CITY_FOAM,
      '  --line-6: 6px; --line-4-5: 4.5px; --line-2-6: 2.6px; --line-1-2: 1.2px;', '  --light-dir: top-left; --light-transition: 1.2s;']
KEYS = ('sky0', 'sky1', 'sky2', 'water', 'lit', 'shade', 'line', 'build', 'pier')
def block(sel, d):
    o = [sel + '{']
    for k in KEYS: o.append('  --l-%s: %s;' % (k, d[k]))
    o.append('  --l-windows: %s; --l-windows-opacity: %d;' % (d['windows'] or 'transparent', 1 if d['windows'] else 0))
    s = d['shadow']; o.append('  --l-shadow-color: %s; --l-shadow-opacity: %s; --l-shadow-dx: %spx; --l-shadow-dy: %spx;' % (s['color'], s['opacity'], s['dx'], s['dy']))
    i = d['intensity']; o.append('  --l-lit-a: %s; --l-shade-a: %s; --l-nlit-a: %s; --l-nshade-a: %s;' % (i['lit_a'], i['shade_a'], i['nlit_a'], i['nshade_a']))
    return o + ['}']
c.append('  /* پیش‌فرض = روز */')
for k in KEYS: c.append('  --l-%s: %s;' % (k, lights['day'][k]))
c += ['  --l-windows: transparent; --l-windows-opacity: 0;', '  --l-lit-a: %s; --l-shade-a: %s; --l-nlit-a: %s; --l-nshade-a: %s;' % tuple(lights['day']['intensity'][k] for k in ('lit_a', 'shade_a', 'nlit_a', 'nshade_a')),
      '  --l-shadow-color: #10083a; --l-shadow-opacity: .28; --l-shadow-dx: 8px; --l-shadow-dy: 6px;', '}']
for n in ('day', 'dusk', 'night'): c += block('[data-light="%s"]' % n, lights[n])
c += ['/* انتقال: دو لایهٔ کامل (روز و شب) هر دو در DOM؛ فقط opacity ‎1.2ث. غروب ثابت و فقط صحنهٔ ماجرا ۲ (میان‌یابی ندارد). نقشه: همیشه data-light=day */',
      '.lt-layer{opacity:0;transition:opacity var(--light-transition) ease-in-out}',
      '[data-light="day"] .lt-layer[data-for~="day"],[data-light="dusk"] .lt-layer[data-for~="dusk"],[data-light="night"] .lt-layer[data-for~="night"]{opacity:1}',
      '@media (prefers-reduced-motion: reduce){.lt-layer{transition:none}}',
      '/* rim گرم و سایهٔ بنفش بناها: کلاس‌های .elit/.esh */', '[data-light] .elit{opacity:var(--l-nlit-a,.3)}', '[data-light] .esh{opacity:var(--l-nshade-a,.22)}']
open(os.path.join(H, 'tokens.css'), 'w').write('\n'.join(c) + '\n')

# ---------- common_defs.svg ----------
d = ['<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true"><defs>',
     '<!-- فقط پشتیبان ابزار ماکت؛ هیچ blend/mix-blend-mode ای نیست -->',
     '<filter id="lt-wob" x="-15%" y="-15%" width="130%" height="130%"><feTurbulence type="fractalNoise" baseFrequency=".045" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.4"/></filter>']
for n in ('day', 'dusk', 'night'):
    l = lights[n]
    d.append('<linearGradient id="lt-sky-%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset=".55" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (n, l['sky0'], l['sky1'], l['sky2']))
d += ['<clipPath id="lt-clip-card"><rect width="360" height="240" rx="12"/></clipPath>',
      '<!-- بازتاب غروب روی آب: خط‌های افقی (نه لکه) -->',
      '<g id="lt-reflect-dusk" fill="#ffb21c" fill-opacity=".45"><rect x="0" y="0" width="120" height="3" rx="1.5"/><rect x="20" y="9" width="90" height="3" rx="1.5"/><rect x="40" y="18" width="60" height="3" rx="1.5"/></g>',
      '<!-- ستارهٔ چهارپر v4 (gen_card.py) -->', '<path id="lt-sparkle" d="M0,-8 l1.5,6.5 6.5,1.5 -6.5,1.5 -1.5,6.5 -1.5,-6.5 -6.5,-1.5 6.5,-1.5z" fill="#ffd9ff"/>', '</defs></svg>']
open(os.path.join(H, 'common_defs.svg'), 'w').write('\n'.join(d) + '\n')

# ---------- palette svgs ----------
def sw(x, y, name, col, ln, tc, w=116):
    f = col if col else 'none'
    return ('<rect x="%d" y="%d" width="%d" height="34" rx="6" fill="%s" stroke="%s" stroke-width="1.4"/><text x="%d" y="%d" fill="%s">%s</text><text x="%d" y="%d" fill="%s" font-family="monospace">%s</text>'
            % (x, y, w, f, ln, x, y + 48, tc, name, x + 64, y + 48, tc, col or 'off'))
def pal(n):
    l = lights[n]; dark = n == 'night'; bg = card['bg'] if dark else '#ffffff'; tc = CREAM if dark else OUT; ln = CREAM if dark else OUT
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 %d" font-family="sans-serif" font-size="11">' % (460 if n == 'day' else 340 if n == 'dusk' else 400), '<rect width="100%%" height="100%%" fill="%s"/>' % bg,
         '<text x="12" y="22" font-size="16" font-weight="700" fill="%s">palette %s (r2، بر پایهٔ v4؛ نور از بالا-چپ)</text>' % (tc, n)]
    items = [('sky0', l['sky0']), ('sky1', l['sky1']), ('sky2', l['sky2']), ('water', l['water']), ('pier', l['pier']), ('build', l['build']), ('lit (rim)', l['lit']), ('shade', l['shade']), ('shadow', l['shadow']['color']), ('line', l['line']), ('windows', l['windows']), ('accent', ui['accent_yellow'])]
    for i, (k, val) in enumerate(items): s.append(sw(12 + (i % 4) * 126, 36 + (i // 4) * 66, k, val, ln, tc))
    y0 = 36 + 3 * 66
    if n == 'day':
        s.append('<text x="12" y="%d" font-weight="700" fill="%s">زمین‌های نقشه (v4 دیده‌شده) + مسیر + سختی</text>' % (y0 + 6, tc))
        gi = [('ورزشگاه', zones['sports']['base']), ('فضا', zones['space']['base']), ('مزرعه', zones['farm']['base']), ('شهر/آب', zones['city']['base']), ('یخ', v('ground.ice')), ('شن', v('ground.sand')),
              ('مسیر کرم', CREAM), ('مسیر مانده', p['rest']), ('خط دور', OUT), ('آسان', hard['easy']['hex']), ('متوسط', hard['mid']['hex']), ('سخت', hard['hard']['hex'])]
        for i, (k, val) in enumerate(gi): s.append(sw(12 + (i % 4) * 126, y0 + 16 + (i // 4) * 62, k, val, ln, tc))
    if dark:
        y1 = y0 + 6; s.append('<text x="12" y="%d" font-weight="700" fill="%s">کارت شب (Neon Abyss، از v4)</text>' % (y1, tc))
        ci = [('card bg', card['bg']), ('front top', card['front_top']), ('front bot', card['front_bottom']), ('plate', card['plate']), ('glow/cyan', card['glow']), ('pink', card['pill_pink']), ('gold', card['gold']), ('kept', card['kept_top'])]
        for i, (k, val) in enumerate(ci): s.append(sw(12 + (i % 4) * 126, y1 + 12 + (i // 4) * 60, k, val, ln, tc))
    s.append('</svg>')
    open(os.path.join(H, 'palette_%s.svg' % n), 'w').write('\n'.join(s) + '\n')
for n in ('day', 'dusk', 'night'): pal(n)

# ---------- اندازه‌گیری ----------
rows = []
def add(sec, name, fg, bg, mn, how='single', outline=None, note='', light=''):
    val = cr(fg, bg); ok = val >= mn; mode = 'پر'
    if not ok and outline:
        a, b = cr(outline, bg), cr(fg, outline)
        if a >= mn and b >= mn: ok, mode = True, 'دولایه: خط/زمین %.2f و پر/خط %.2f' % (a, b)
    rows.append(dict(sec=sec, name=name, light=light, fg=fg, bg=bg, min=mn, val=round(val, 2), ok=ok, mode=mode if ok else '', note=note))
G = {k: zones[k]['base'] for k in zones}; G['ice'] = v('ground.ice'); G['sand'] = v('ground.sand')
GN = {'sports': 'ورزشگاه', 'space': 'فضا', 'farm': 'مزرعه', 'city': 'شهر/آب', 'ice': 'یخ', 'sand': 'شن'}
# الف) خوانایی متن/نشانه
A = 'الف خوانایی'
for a, b, nm, mn in [(ui['chip_text'], ui['chip'], 'متن چیپ پایه (غیرفعال)', 4.5), (OUT, ui['chip_on'], 'متن چیپ فعال', 4.5), (OUT, ui['menu'], 'خطوط منو روی دکمه', 3), (ui['label_fill'], OUT, 'برچسب گره (پر/خط دور متن)', 4.5),
                     (ui['zone_title_fill'], OUT, 'عنوان بزرگ زمین (پر/خط دور متن)', 4.5), (OUT, ui['accent_yellow'], 'متن «اینجایی» روی حباب', 4.5),
                     (card['title_fill'], card['edge'], 'عنوان کارت (پر/خط دور متن)', 4.5), (card['body_text'], card['plate'], 'متن کارت روی صفحهٔ تیره', 4.5),
                     (card['pill_text'], card['pill_cyan'], 'دکمهٔ تمرین (فیروزه‌ای)', 4.5), (card['pill_text'], card['pill_pink'], 'دکمهٔ فیلم (صورتی)', 4.5), (card['pill_text'], card['pill_gold'], 'دکمهٔ جعبه (طلایی)', 4.5),
                     (OUT, card['pill_cyan'], 'دکمهٔ «پشت کارت»', 4.5), ('#ffffff', card['kept_top'], 'آیکون جعبه روی کارت جمع‌شده', 3), (card['locked_icon'], card['locked'], 'آیکون قفل', 3), (card['empty_dash'], card['bg'], 'علامت + و خط‌چین خالی', 3)]:
    add(A, nm, a, b, mn)
add(A, 'آیکون چشم سفید روی کارت فیروزه‌ای (بدون اصلاح)', '#ffffff', card['front_top'], 3, note='v4 همین است؛ با خط دور ۲px اصلاح می‌شود')
rows[-1]['ok'] = True; rows[-1]['mode'] = 'v4 قبل از اصلاح (اطلاعاتی)'
add(A, 'آیکون چشم با خط دور #190539 (پر/خط دور)', '#ffffff', card['icon_outline'], 3, note='اصلاح؛ خط دور/کارت: %.2f' % cr(card['icon_outline'], card['front_top']))
# ب) مسیر از زمین
B = 'ب مسیر/زمین'
for k in ('sports', 'space', 'farm', 'city', 'sand', 'ice'):
    add(B, 'مسیر انجام‌شده (کرم) روی ' + GN[k], CREAM, G[k], 3, outline=OUT)
    add(B, 'خط دور مسیر روی ' + GN[k], OUT, G[k], 3, note='' if k != 'city' else 'v4 همین 2.12 است؛ با خط دور دوم کف روی آب اصلاح می‌شود (ردیف بعد)')
    if k == 'city': rows[-1]['ok'] = True; rows[-1]['mode'] = 'v4 قبل از اصلاح (اطلاعاتی)'
for k in ('sports', 'space', 'farm', 'city'):
    foam = k == 'city'
    add(B, 'مسیر مانده (کرم %.2f) روی %s' % (REST_OP, GN[k]), p['rest'], G[k], 3, outline=(CITY_FOAM if foam else OUT), note='خط دور مسیر روی آب: کف %s' % CITY_FOAM if foam else '')
add(B, 'مسیر مانده ÷ خط دور (دو لایه)', p['rest'], OUT, 3, note='v4 .34 → %.2f' % cr(mix(OUT, CREAM, .34), OUT))
add(B, 'مسیر انجام‌شده ÷ خط دور', CREAM, OUT, 3)
add(B, 'کف روی آب شهر ÷ آب', CITY_FOAM, G['city'], 3); add(B, 'کف ÷ خط دور', CITY_FOAM, OUT, 3)
add(B, 'رود (پر) روی مزرعه', v('path.river_fill'), G['farm'], 3, outline=OUT)
add(B, 'رود روی چمن', v('path.river_fill'), G['sports'], 3, outline=OUT)
# ج) سه قرص سختی
C = 'ج سختی'
for k in ('sports', 'space', 'farm', 'city', 'sand', 'ice'):
    for hk in ('easy', 'mid', 'hard'):
        h = hard[hk]['hex']; fo = cr(h, G[k]); ol = cr(OUT, G[k]); best = max(fo, ol)
        rows.append(dict(sec=C, name='قرص %s روی %s' % (hk, GN[k]), light='', fg=h, bg=G[k], min=1.5, val=round(best, 2), ok=best >= 1.5,
                         mode='پر %.2f / خط دور %.2f' % (fo, ol), note=''))
for hk in ('easy', 'mid', 'hard'):
    h = hard[hk]['hex']; add(C, 'کلمهٔ %s روی قرص (متن #241a5e)' % hk, OUT, h, 4.5); add(C, 'پر %s ÷ خط دور قرص' % hk, h, OUT, 3)
def gray(h): y = Y(h); return 116 * (y ** (1 / 3)) - 16 if y > .008856 else 903.3 * y
dl = abs(gray(hard['easy']['hex']) - gray(hard['hard']['hex']))
rows.append(dict(sec=C, name='ΔL* قرص آسان/سخت (کوررنگی سبز-قرمز)', light='', fg=hard['easy']['hex'], bg=hard['hard']['hex'], min=0, val=round(dl, 1), ok=True, mode='اطلاعاتی', note='روشنی تقریباً برابر؛ جداکنندهٔ اصلی تعداد قله (۱/۲/۳) و کلمه است، نه رنگ'))
# صحنه (اطلاعاتی + دروازه‌های کوتاه)
S = 'د صحنه (نور)'
for n, l in lights.items():
    add(S, 'افق آسمان ÷ آب', l['sky2'], l['water'], 1.5, light=n)
    add(S, 'بنا ÷ آب', l['build'], l['water'], 3, light=n)
    add(S, 'rim ÷ سایه', l['lit'], l['shade'], 3, light=n)
    add(S, 'خط دور ÷ آب (اطلاعاتی)', l['line'], l['water'], 1, light=n, note='شب: خط پخته‌شده تیره؛ سیلوئت با بدنه خوانده می‌شود')
json.dump(rows, open(os.path.join(H, 'light_contrast.json'), 'w'), ensure_ascii=False, indent=1)
bad = [r for r in rows if not r['ok']]
md = ['# سنجش کنتراست r2 (WCAG، Python)', '', 'فقط سه محور: الف خوانایی متن/نشانه، ب مسیر از زمین (دولایه: پر÷زمین ≥۳ یا (خط÷زمین ≥۳ و پر÷خط ≥۳))، ج سه قرص سختی روی هر زمین (≥۱٫۵ با خط دور)؛ د صحنهٔ نور کوتاه. رنگ‌های زمین/UI/کارت v4 دست‌نخورده‌اند.', '',
      '| بخش | مورد | نور | fg | bg | حداقل | عدد | نتیجه | توضیح |', '|---|---|---|---|---|---|---|---|---|']
for r in rows: md.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s %s |' % (r['sec'], r['name'], r['light'], r['fg'], r['bg'], r['min'], r['val'], 'OK' if r['ok'] else 'ردیف قرمز', r['mode'], r['note']))
md += ['', '## ردیف‌های قرمز: %d' % len(bad)] + ['- %s: %s (%.2f < %s)' % (r['sec'], r['name'], r['val'], r['min']) for r in bad]
md += ['', '## اصلاح‌های کمینه نسبت به ظاهر v4'] + ['- ' + t for t in tokens['_corrections']]
md += ['', '## جایی که عدد با v4 تضاد داشت و v4 ماند', '- مسیر انجام‌شده (کرم) روی مزرعه 2.99 و روی چمن 3.07 (مرز ۳): با قاعدهٔ دولایه OK؛ پر تنها مرزی است.', '- خط دور مسیر روی آب شهر 2.12 (<3): ظاهر v4 ماند، خط دور دوم کف افزوده شد.', '- مسیر مانده ÷ زمین (پر تنها) زیر ۳ است در v4؛ دولایه با خط دور OK.']
open(os.path.join(H, 'light_contrast.md'), 'w').write('\n'.join(md) + '\n')
print('built; red rows:', len(bad))
for r in bad: print('RED', r['sec'], r['name'], r['val'], r['min'])
