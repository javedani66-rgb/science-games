#!/usr/bin/env python3
"""سنجش قالب‌نامهٔ کنترل‌ها: component_spec.json را می‌خواند و همهٔ جفت‌رنگ‌ها را با فرمول WCAG می‌سنجد.

اجرا:  python3 tests/spec_contrast.py [-v] [--md]
  بدون گزینه: فقط خطاها و یک خط جمع‌بندی (کد خروج 1 اگر خطایی باشد).
  -v   همهٔ جفت‌ها با نسبتشان
  --md جدول نسبت‌ها به‌صورت Markdown (برای سند)

بررسی‌ها: متن/پر ≥۴٫۵ (متن بزرگ ≥۳)، آیکون/پر ≥۳، لبهٔ کنترل در برابر سطح ≥۳ (پر یا خط دور)،
حالت فشرده و غیرفعال و فوکوس، «ممنوع» واقعاً زیر حد باشد، رنگ‌ها از پالت تأییدشده یا مشتق‌شدهٔ قابل‌بازسازی،
لمس ≥۴۸، شعاع مشخص و بدون clip-path و بدون گوشهٔ تیز، فونت Vazirmatn (Lalezar فقط عنوان ≤۳ کلمه)،
همهٔ کلیدهای متن در spec/strings.fa.json، و نبودن clip-path در spec_sample.html."""
import json, re, sys, pathlib

V5 = pathlib.Path(__file__).resolve().parents[1]
SPEC = json.load(open(V5 / 'component_spec.json', encoding='utf-8'))
VERBOSE = '-v' in sys.argv
MD = '--md' in sys.argv
errs, rows_out, n_ok = [], [], 0


def lum(h):
    h = h.lstrip('#'); r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)

def cr(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True)
    return (x + .05) / (y + .05)

def mix(a, b, t):
    a, b = a.lstrip('#'), b.lstrip('#')
    return '#%02x%02x%02x' % tuple(round(int(a[i:i + 2], 16) * (1 - t) + int(b[i:i + 2], 16) * t) for i in (0, 2, 4))

def check(row, mode, name, fg, bg, need, kind='text'):
    global n_ok
    r = cr(fg, bg); ok = r >= need - 1e-9
    rows_out.append((row, mode, name, fg, bg, need, r, ok))
    if ok:
        n_ok += 1
        if VERBOSE: print(f'  ok  {row:14} {mode:5} {name:28} {fg} / {bg}  {r:5.2f} (>= {need})')
    else:
        errs.append(f'{row} [{mode}] {name}: {fg} on {bg} = {r:.2f} < {need}')

def err(msg): errs.append(msg)

# ---- پالت تأییدشده
pal = set()
for f in ['team/assets_r2/light/zone_tokens.json', 'team/assets_r2/ui/ui_tokens.css', 'team/assets_r2/light/tokens.css']:
    pal |= set(h.lower() for h in re.findall(r'#[0-9a-fA-F]{6}\b', (V5 / f).read_text(encoding='utf-8')))
pal.add('#ffffff')
M = SPEC['meta']; W = M['wcag']
EDGE = {'day': '#120c3a', 'night': '#190539'}
ST = SPEC['state_rules']

def need_for(font):
    s, w = font.get('size_px'), font.get('weight')
    if not s: return W['text_min']
    large = s >= W['large_px'] or (w and w >= 700 and s >= W['large_bold_px'])
    return W['large_text_min'] if large else W['text_min']

for row in SPEC['rows']:
    rid = row['id']; font = row['font']; need = need_for(font)
    # ---- ساختار
    sh = row['shape']
    if sh.get('clip_path') != 'none': err(f'{rid}: clip_path must be none')
    if sh['corners'] not in ('all-equal', 'circle', 'text-only'): err(f'{rid}: corners must be all-equal')
    if sh['corners'] == 'all-equal' and not (sh.get('radius_px') and sh['radius_px'] > 0): err(f'{rid}: radius must be > 0')
    if row['interactive']:
        sz = row['size']
        if (sz.get('touch_px') or 0) < M['touch_min_px']: err(f'{rid}: touch {sz.get("touch_px")} < {M["touch_min_px"]}')
        if sz['min_height_px'] < M['touch_min_px']: err(f'{rid}: min_height {sz["min_height_px"]} < {M["touch_min_px"]}')
        if sz.get('min_width_px', 48) < 48 and rid != 'btn_icon': err(f'{rid}: min_width < 48')
    fam = font.get('family')
    if fam == 'Lalezar':
        d = SPEC['fonts']['display']
        if rid not in d['allowed_rows']: err(f'{rid}: Lalezar not allowed here')
        if (font.get('max_words') or 99) > d['max_words']: err(f'{rid}: Lalezar max_words > {d["max_words"]}')
        if font['size_px'] < d['min_px']: err(f'{rid}: Lalezar size < {d["min_px"]}')
    elif fam not in (None, 'Vazirmatn'): err(f'{rid}: unknown font {fam}')
    if font.get('size_px') and font['size_px'] < M['min_font_px'] and fam != 'Lalezar': err(f'{rid}: font < {M["min_font_px"]}')
    t = font.get('title')
    if t and ((t.get('max_words') or 99) > 3 or t['size_px'] < 24): err(f'{rid}: title font rule')
    # ---- رنگ‌ها
    for mode in ('day', 'night'):
        surf = row['surface'][mode]
        surfs = [surf] + (list(row.get('surfaces_extra', {}).values()) if mode == 'day' else [])
        for var in row['variants']:
            o = var[mode]; vid = var['id']
            for k in ('fill', 'text', 'rim'):
                if o[k].lower() not in pal: err(f'{rid}/{vid}[{mode}] {k} {o[k]} not in approved palette')
            check(rid, mode, f'{vid}: text/fill', o['text'], o['fill'], need)
            if o.get('icon'): check(rid, mode, f'{vid}: icon/fill', o['icon'], o['fill'], W['nontext_min'], 'icon')
            # لبه در برابر سطح (هر سطح): پر یا خط دور باید ≥۳ باشد
            for s in surfs:
                if row['id'] == 'zone_title': continue
                b = max(cr(o['fill'], s), cr(o['rim'], s))
                rows_out.append((rid, mode, f'{vid}: edge/surface {s}', o['fill'] + '|' + o['rim'], s, 3, b, b >= 3))
                if b < 3: err(f'{rid}/{vid}[{mode}] edge vs surface {s} = {b:.2f} < 3')
                else:
                    globals()['n_ok'] += 1
                    if VERBOSE: print(f'  ok  {rid:14} {mode:5} {vid+": edge/surface":28} {s}  {b:5.2f}')
            if rid == 'zone_title':
                for s in surfs:  # حاشیه یا متن باید از زمین جدا شود
                    b = max(cr(o['fill'], s), cr(o['text'], s))
                    if b < 3: err(f'{rid}[{mode}] halo/text vs surface {s} = {b:.2f}')
            if 'pressed_fill' in o:
                if o['pressed_fill'] != mix(o['fill'], EDGE[mode], .12): err(f'{rid}/{vid}[{mode}] pressed_fill is not mix(fill, edge, .12)')
                check(rid, mode, f'{vid}: pressed text/fill', o['text'], o['pressed_fill'], need)
                if o.get('icon'): check(rid, mode, f'{vid}: pressed icon/fill', o['icon'], o['pressed_fill'], W['nontext_min'], 'icon')
        for p in row.get('parts', []):
            o = p[mode]
            for k in ('fill', 'text'):
                if o[k].lower() not in pal: err(f'{rid}/{p["id"]}[{mode}] {k} {o[k]} not in palette')
            check(rid, mode, f'part {p["id"]}', o['text'], o['fill'], W['nontext_min'] if p['kind'] == 'icon' else W['text_min'])
        if 'pressed' in row.get('states_apply', []) or 'disabled' in row.get('states_apply', []):
            d = ST['disabled'][mode]
            for k in ('fill', 'text', 'rim'):
                if d[k].lower() not in pal: err(f'disabled[{mode}] {k} {d[k]} not in palette')
            check(rid, mode, 'disabled text/fill', d['text'], d['fill'], W['text_min'])
            b = max(cr(d['rim'], surf), cr(d['fill'], surf))
            rows_out.append((rid, mode, 'disabled edge/surface', d['fill'] + '|' + d['rim'], surf, 3, b, b >= 3))
            if b < 3: err(f'{rid}[{mode}] disabled edge vs surface = {b:.2f} < 3')
            else: n_ok += 1
        if 'focus' in row.get('states_apply', []):
            ring = ST['focus']['on_light_surface'] if lum(surf) > .3 else ST['focus']['on_dark_surface']
            check(rid, mode, 'focus ring/surface', ring, surf, W['nontext_min'], 'edge')
    # نشان سختی: رنگ ثابت روز=شب
    if row.get('badge', {}).get('fixed_colors_day_night'):
        for p in row['parts']:
            if p['day'] != p['night']: err(f'{rid}/{p["id"]}: difficulty badge colors must be identical day/night')
    if row['interactive'] and row.get('states_apply') != ['normal', 'pressed', 'disabled', 'focus']:
        err(f'{rid}: interactive row must define all four states')
# ---- ممنوع‌ها: واقعاً باید زیر حد باشند
forb = []
for f in SPEC['forbidden_pairs']:
    r = cr(f['fg'], f['bg']); forb.append((f, r))
    if r >= W['text_min']: err(f'forbidden pair {f["fg"]} on {f["bg"]} = {r:.2f} is actually fine (>= {W["text_min"]}); remove it from the list')
    elif VERBOSE: print(f'  ban {f["fg"]} on {f["bg"]} = {r:.2f}')
# ---- مجاز روی تیره
A = SPEC['allowed_text_on_dark']
for bg in A['on']:
    for fg in A['colors']: check('allowed_dark', 'both', f'{fg} on dark', fg, bg, W['text_min'])
# ---- رشته‌ها
S = json.load(open(V5 / 'spec/strings.fa.json', encoding='utf-8'))
keys = set(re.findall(r'"((?:name|desc|note|why)_key)":\s*"([^"]+)"', (V5 / 'component_spec.json').read_text(encoding='utf-8')))
for kind, k in sorted(keys):
    if k not in S: err(f'strings.fa.json is missing {k}')
for k, v in S.items():
    if v.get('kind') is None or v.get('text') is None: err(f'strings: {k} incomplete')
# ---- نمونه
html = V5 / 'spec_sample.html'
if html.exists():
    h = html.read_text(encoding='utf-8')
    if re.search(r'clip-path', h): err('spec_sample.html uses clip-path')
    if re.search(r'border-radius:\s*0(px)?\s*[;}]', h): err('spec_sample.html has a zero radius')
else: err('spec_sample.html is missing')

if MD:
    print('| کنترل | حالت | جفت | رنگ‌ها | نسبت | حد |\n|---|---|---|---|---|---|')
    for r in rows_out:
        if 'edge/surface' in r[2]: continue
        print(f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} روی {r[4]} | {r[6]:.2f} | {r[5]} |')
for e in errs: print('FAIL', e)
tot = n_ok + len(errs)
print(f'{"OK" if not errs else "FAILED"}: {n_ok} checks passed, {len(errs)} failed; {len(SPEC["rows"])} rows, {len(forb)} forbidden pairs, {len(pal)} approved colors')
sys.exit(1 if errs else 0)
