#!/usr/bin/env python3
"""سنجش قالب‌نامهٔ کنترل‌ها (نسخهٔ ۲): component_spec.json را می‌خواند و همهٔ جفت‌رنگ‌ها را می‌سنجد.

اجرا:  python3 tests/spec_contrast.py [-v] [--tables]
  بدون گزینه: فقط خطاها و یک خط جمع‌بندی (کد خروج 1 اگر خطایی باشد). نتیجهٔ سنجش پیکسلی در spec/measured.json ذخیره می‌شود.
  -v        همهٔ جفت‌ها با نسبتشان
  --tables  جدول‌های Markdown (رنگ هر نوع، ممنوع) برای چسباندن در سند

بررسی‌ها:
 ۱) متن/پر با فرمول WCAG: ≥۴٫۵، یا ≥۳ اگر متن بزرگ (لالهزار ≥۲۴px یا Vazirmatn بولد ≥۱۸٫۶۶px)؛ آیکون/پر ≥۳؛ لبهٔ کنترل به سطح ≥۳.
 ۲) «سنجش مؤثر با حاشیه» (tests/spec_measure.py): متن در Chromium نقاشی می‌شود؛ نسبت متن به پیکسل‌های حلقهٔ ۱٫۵px دور حروف
    (که حاشیهٔ ضخیم و سایه در آن است) سنجیده می‌شود؛ صدک ۵ باید ≥۴٫۵ باشد. (نسخهٔ ۳) پر زنده تیره نمی‌شود؛ روی پر زنده (نسبت خام زیر ۴٫۵)
    حاشیهٔ هم‌خانواده الزامی است و باید از پر جدا باشد (حاشیه/پر ≥۳). روی پر تیره (خام ≥۴٫۵) حاشیه لازم نیست.
 ۳) حاشیه/سایه = mix(پر، #190539، ۰٫۸۲)؛ فشرده = mix(پر، لبه، ۰٫۱۲).
 ۴) ساختار: لمس ≥۴۸، شعاع مشخص، بدون clip-path و گوشهٔ تیز، نقش فونت (لالهزار: عنوان/برچسب/دکمه، Vazirmatn: متن توضیحی).
 ۵) ممنوع‌ها واقعاً زیر حد باشند؛ همهٔ کلیدهای متن در spec/strings.fa.json؛ نبودن clip-path در spec_sample.html."""
import json, re, sys, pathlib, colorsys

V5 = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from spec_measure import measure

SPEC = json.load(open(V5 / 'component_spec.json', encoding='utf-8'))
VERBOSE = '-v' in sys.argv
TABLES = '--tables' in sys.argv
errs, n_ok = [], 0
LOG = []          # برای جدول‌ها: (row, vid, mode, fill, text, shadow, ratio_fill, eff, pressed_ratio, need)


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

def hexs(r, g, b): return '#%02x%02x%02x' % (round(r * 255), round(g * 255), round(b * 255))

def derive(d):
    h = d['base'].lstrip('#'); r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    H, L, S = colorsys.rgb_to_hls(r, g, b)
    H = (H + d['h_shift'] / 360) % 1; S = min(1, S * d['s_scale']); L = round(L, 2)
    while True:
        c = hexs(*colorsys.hls_to_rgb(H, L, S))
        if cr('#ffffff', c) >= d['min_white']: return c
        L = round(L - 0.01, 2)

def err(msg): errs.append(msg)

def ok():
    global n_ok; n_ok += 1

def check(row, mode, name, fg, bg, need):
    r = cr(fg, bg)
    if r >= need - 1e-9:
        ok()
        if VERBOSE: print(f'  ok  {row:15} {mode:5} {name:30} {fg} / {bg}  {r:5.2f} (>= {need})')
    else:
        err(f'{row} [{mode}] {name}: {fg} on {bg} = {r:.2f} < {need}')
    return r

M = SPEC['meta']; W = M['wcag']; ST = SPEC['state_rules']; TS = SPEC['text_shadow']; FONTS = SPEC['fonts']
EDGE = {'day': '#120c3a', 'night': '#190539'}
SH_TOWARD, SH_T = TS['mix_toward'], TS['mix_t']

# ---- پالت تأییدشده + تیره‌شده‌های بازسازی‌پذیر
pal = set()
for f in ['team/assets_r2/light/zone_tokens.json', 'team/assets_r2/ui/ui_tokens.css', 'team/assets_r2/light/tokens.css']:
    pal |= set(h.lower() for h in re.findall(r'#[0-9a-fA-F]{6}\b', (V5 / f).read_text(encoding='utf-8')))
pal.add('#ffffff')
pal |= {v.lower() for v in SPEC['palette'].values() if isinstance(v, str) and v.startswith('#')}
DER = SPEC['derived_colors']
for k, d in DER.items():
    if d['base'].lower() not in pal: err(f'derived {k}: base {d["base"]} not in approved palette')
    if derive(d) != d['value']: err(f'derived {k}: value {d["value"]} != rebuilt {derive(d)}')
    else: ok()
    if cr('#ffffff', d['value']) < d['min_white']: err(f'derived {k}: white on {d["value"]} < {d["min_white"]}')
    else: ok()
DER_VALUES = {d['value'] for d in DER.values()}

def need_for(font):
    s, w = font.get('size_px'), font.get('weight')
    if not s: return W['text_min']
    large = s >= W['large_px'] or (w and w >= 700 and s >= W['large_bold_px'])
    return W['large_text_min'] if large else W['text_min']

def shadow_css_ok(sd): return sd.lower() in pal or True

# ---- نقش فونت
DISPLAY_ROLES = set(FONTS['display']['roles']); BASE_ROLES = set(FONTS['base']['roles'])
def check_font(rid, f, what='font'):
    fam, role = f.get('family'), f.get('role')
    if fam is None: return
    if fam == 'Lalezar':
        if role not in DISPLAY_ROLES: err(f'{rid} {what}: Lalezar only for {sorted(DISPLAY_ROLES)} (role={role})')
        if f['size_px'] < FONTS['display']['min_px']: err(f'{rid} {what}: Lalezar < {FONTS["display"]["min_px"]}px')
        if role == 'title' and f['size_px'] < FONTS['display']['large_min_px']: err(f'{rid} {what}: title < {FONTS["display"]["large_min_px"]}px')
        if (f.get('max_words') or 99) > FONTS['display']['max_words']: err(f'{rid} {what}: Lalezar max_words > {FONTS["display"]["max_words"]}')
    elif fam == 'Vazirmatn':
        if role not in BASE_ROLES: err(f'{rid} {what}: Vazirmatn only for explanatory/long text (role={role})')
    else: err(f'{rid} {what}: unknown font {fam}')
    if f['size_px'] < M['min_font_px'] and fam != 'Lalezar': err(f'{rid} {what}: font < {M["min_font_px"]}')
    else: ok()

def sh_of(fill): return mix(fill, SH_TOWARD, SH_T)

def run(cases, res):
    """cases: لیست موارد سنجش پیکسلی (در گذر اول پر می‌شود)؛ res: نتیجه (در گذر دوم)."""
    def eff(key, fill, text, shadow, font, stroke=None):
        if res is None:
            cases.append(dict(key=key, fill=fill, text=text, shadow=shadow, layers=TS['layers_px'], family=font['family'], size=font['size_px'], weight=font['weight'], stroke=stroke))
            return None
        r = res[key]['p05']
        if r >= W['effective_min'] - 1e-9: ok()
        else: err(f'{key}: effective ratio with shadow (p{W["ring_percentile"]}) {r:.2f} < {W["effective_min"]}')
        if VERBOSE: print(f'  eff {key:50} {r:6.2f}')
        return r

    for row in SPEC['rows']:
        rid = row['id']; font = row['font']; need = need_for(font)
        sh = row['shape']
        if sh.get('clip_path') != 'none': err(f'{rid}: clip_path must be none')
        if sh['corners'] not in ('all-equal', 'circle', 'text-only'): err(f'{rid}: corners must be all-equal')
        if sh['corners'] == 'all-equal' and not (sh.get('radius_px') and sh['radius_px'] > 0): err(f'{rid}: radius must be > 0')
        if row['interactive']:
            sz = row['size']
            if (sz.get('touch_px') or 0) < M['touch_min_px']: err(f'{rid}: touch {sz.get("touch_px")} < {M["touch_min_px"]}')
            if sz['min_height_px'] < M['touch_min_px']: err(f'{rid}: min_height {sz["min_height_px"]} < {M["touch_min_px"]}')
            if sz.get('min_width_px', 48) < 48 and rid != 'btn_icon': err(f'{rid}: min_width < 48')
        check_font(rid, font)
        if font.get('title'): check_font(rid, font['title'], 'title')
        if row.get('font_sub'): check_font(rid, row['font_sub'], 'font_sub')
        if rid == 'side_path' and sh.get('size_px', 0) < 48: err('side_path: node < 48')
        for mode in ('day', 'night'):
            surf = row['surface'][mode]
            surfs = [surf] + (list(row.get('surfaces_extra', {}).values()) if mode == 'day' else [])
            for var in row['variants']:
                o = var[mode]; vid = var['id']; tag = f'{rid}/{vid}/{mode}'
                for k in ('fill', 'text', 'rim'):
                    c = o[k].lower()
                    if c not in pal and c not in DER_VALUES: err(f'{rid}/{vid}[{mode}] {k} {c} not in approved palette or derived_colors')
                if o.get('derive'):
                    if o['derive'] not in DER or o['fill'] != DER[o['derive']]['value']: err(f'{tag}: fill is not derived_colors.{o["derive"]}')
                if o.get('shadow') and o['shadow'] != sh_of(o['fill']): err(f'{tag}: shadow {o["shadow"]} is not mix(fill, {SH_TOWARD}, {SH_T}) = {sh_of(o["fill"])}')
                if font.get('family') and rid != 'map_label':
                    sp = TS['stroke_px_title'] if font.get('role') == 'title' else TS['stroke_px']
                    stk = (sp, o['shadow']) if o.get('outline') else None
                    if o.get('outline'):
                        if not o.get('shadow'): err(f'{tag}: outline variant needs a shadow/outline colour')
                        check(rid, mode, f'{vid}: outline/fill', o['shadow'], o['fill'], W['outline_vs_fill_min'])
                    else:
                        check(rid, mode, f'{vid}: text/fill', o['text'], o['fill'], need)
                    e = eff(f'{tag}/normal', o['fill'], o['text'], o.get('shadow'), font, stroke=stk)
                    e2 = None
                    if 'pressed_fill' in o:
                        if o['pressed_fill'] != mix(o['fill'], EDGE[mode], .12): err(f'{tag}: pressed_fill is not mix(fill, edge, .12)')
                        if not o.get('outline'): check(rid, mode, f'{vid}: pressed text/fill', o['text'], o['pressed_fill'], need)
                        e2 = eff(f'{tag}/pressed', o['pressed_fill'], o['text'], o.get('shadow'), font, stroke=stk)
                    if res is not None:
                        LOG.append((rid, vid, mode, o['fill'], o['text'], o.get('shadow'), cr(o['text'], o['fill']), res[f'{tag}/normal']['p05'], need))
                elif 'pressed_fill' in o and o['pressed_fill'] != mix(o['fill'], EDGE[mode], .12):
                    err(f'{tag}: pressed_fill is not mix(fill, edge, .12)')
                if o.get('outline'):
                    pass          # آیکون روی پر زنده با همان حاشیهٔ هم‌خانواده؛ سنجشش همان «حاشیه/پر ≥۳» است
                elif o.get('icon'):
                    check(rid, mode, f'{vid}: icon/fill', o['icon'], o['fill'], W['nontext_min'])
                    if 'pressed_fill' in o: check(rid, mode, f'{vid}: pressed icon/fill', o['icon'], o['pressed_fill'], W['nontext_min'])
                elif not font.get('family'):
                    check(rid, mode, f'{vid}: icon/fill', o['text'], o['fill'], W['nontext_min'])
                for s in surfs:
                    if rid in ('zone_title', 'map_label'): continue
                    b = max(cr(o['fill'], s), cr(o['rim'], s))
                    if b < 3: err(f'{rid}/{vid}[{mode}] edge vs surface {s} = {b:.2f} < 3')
                    else:
                        ok()
                        if VERBOSE: print(f'  ok  {rid:15} {mode:5} {vid + ": edge/surface":30} {s}  {b:5.2f}')
                if rid in ('zone_title', 'map_label'):
                    for s in surfs:
                        b = max(cr(o['fill'], s), cr(o['text'], s))
                        if b < 3: err(f'{rid}[{mode}] halo/text vs surface {s} = {b:.2f}')
                        else: ok()
                    # حاشیه و سایهٔ پایین (نه فقط فرمول): ساده‌ترین سنجش پیکسلی روی حاشیه
                    eff(f'{tag}/halo', o['fill'], o['text'], None, font, stroke=(row['border']['width_px'], o['fill']))
            for p in row.get('parts', []):
                o = p[mode]; pf = p.get('font') or font; kind = p['kind']; tag = f'{rid}/{p["id"]}/{mode}'
                for k in ('fill', 'text'):
                    c = o[k].lower()
                    if c not in pal and c not in DER_VALUES: err(f'{tag} {k} {c} not in palette')
                if o.get('derive') and o['fill'] != DER[o['derive']]['value']: err(f'{tag}: fill is not derived_colors.{o["derive"]}')
                if o.get('shadow') and o['shadow'] != sh_of(o['fill']): err(f'{tag}: shadow is not mix(fill, ...)')
                if kind == 'line':
                    check(rid, mode, f'{p["id"]}: dots/casing', o['fill'], o['text'], W['nontext_min'])
                    for s in surfs:
                        b = max(cr(o['fill'], s), cr(o['text'], s))
                        if b < 3: err(f'{tag}: line vs surface {s} = {b:.2f} < 3')
                        else: ok()
                    continue
                need_p = W['nontext_min'] if kind == 'icon' else need_for(pf)
                if kind == 'text' and o.get('outline'):
                    check(rid, mode, f'part {p["id"]}: outline/fill', o['shadow'], o['fill'], W['outline_vs_fill_min'])
                else:
                    check(rid, mode, f'part {p["id"]}', o['text'], o['fill'], need_p)
                if kind == 'text':
                    check_font(rid, pf, f'part {p["id"]}')
                    sp = TS['stroke_px_title'] if pf.get('role') == 'title' else TS['stroke_px']
                    eff(f'{tag}/normal', o['fill'], o['text'], o.get('shadow'), pf, stroke=(sp, o['shadow']) if o.get('outline') else None)
                    if res is not None: LOG.append((rid, p['id'], mode, o['fill'], o['text'], o.get('shadow'), cr(o['text'], o['fill']), res[f'{tag}/normal']['p05'], need_p))
            ov = row.get('state_overrides', {})
            if 'pressed' in row.get('states_apply', []) or 'disabled' in row.get('states_apply', []):
                d = ov.get('disabled', {}).get(mode) or ST['disabled'][mode]
                for k in ('fill', 'text', 'rim'):
                    if d[k].lower() not in pal: err(f'disabled[{mode}] {k} {d[k]} not in palette')
                check(rid, mode, 'disabled text/fill', d['text'], d['fill'], W['text_min'])
                for s in surfs:
                    b = max(cr(d['rim'], s), cr(d['fill'], s))
                    if b < 3: err(f'{rid}[{mode}] disabled edge vs surface {s} = {b:.2f} < 3')
                    else: ok()
            if 'focus' in row.get('states_apply', []):
                if 'focus' in ov:
                    f2 = ov['focus']
                    check(rid, mode, 'focus ring/outline', f2['ring'], f2['outline'], W['nontext_min'])
                    for s in surfs:
                        b = max(cr(f2['ring'], s), cr(f2['outline'], s))
                        if b < 3: err(f'{rid}[{mode}] focus two-tone ring vs surface {s} = {b:.2f} < 3')
                        else: ok()
                else:
                    ring = ST['focus']['on_light_surface'] if lum(surf) > .3 else ST['focus']['on_dark_surface']
                    check(rid, mode, 'focus ring/surface', ring, surf, W['nontext_min'])
        if row.get('badge', {}).get('fixed_colors_day_night'):
            for p in row['parts']:
                if p['day'] != p['night']: err(f'{rid}/{p["id"]}: difficulty badge colors must be identical day/night')
        if row['interactive'] and row.get('states_apply') != ['normal', 'pressed', 'disabled', 'focus']:
            err(f'{rid}: interactive row must define all four states')
        # پشتهٔ چالش: ترتیب و شکل ایستا
        if rid == 'challenge_stack':
            s = row['stack']
            if s['order'] != ['easy', 'mid', 'hard'] or s['front'] != 'easy': err('challenge_stack: order must be easy (front), mid, hard (behind all)')
            if s['peek_px'] < 20: err('challenge_stack: peek too small')
            if s.get('strip_touch') and s.get('strip_px', 0) < 48: err('challenge_stack: peeking strips that are touch targets must be >= 48px')
            if {v['id'] for v in row['variants']} != {'easy', 'mid', 'hard'}: err('challenge_stack: three variants easy/mid/hard')
            for v in row['variants']:
                for m in ('day', 'night'):
                    if v[m].get('rim') is None: err('challenge_stack: rim needed to separate stacked cards')
                    else: ok()
    return


def forbidden(res_f):
    """ممنوع‌ها: raw زیر حد باشد؛ scope=all یعنی حتی برای متن بزرگ ناخوان (<۳)، scope=small یعنی فقط زیر ۲۴px ممنوع (۳ تا ۴٫۵)."""
    out = []
    for f in SPEC['forbidden_pairs']:
        r = cr(f['fg'], f['bg']); sc = f.get('scope')
        if sc not in ('all', 'small'): err(f'forbidden {f["fg"]}/{f["bg"]}: scope must be all|small'); continue
        if r >= W['text_min']: err(f'forbidden pair {f["fg"]} on {f["bg"]} = {r:.2f} is actually fine (>= {W["text_min"]}); remove it')
        elif sc == 'all' and r >= W['large_text_min']: err(f'forbidden pair {f["fg"]} on {f["bg"]} = {r:.2f}: scope all, but fine for large text (>=3); mark small')
        elif sc == 'small' and r < W['large_text_min']: err(f'forbidden pair {f["fg"]} on {f["bg"]} = {r:.2f}: below 3, so it is banned at every size; mark all')
        else: ok()
        if f.get('shadow_demo'):
            e = res_f.get(f'forbid/{f["fg"]}/{f["bg"]}', {}).get('p05', 0)
            if e < W['effective_min']: err(f'forbidden-bare pair {f["fg"]} on {f["bg"]}: even the outline gives only {e:.2f} (< {W["effective_min"]})')
            elif sh_of(f['bg']) and cr(sh_of(f['bg']), f['bg']) < W['outline_vs_fill_min']: err(f'outline of {f["bg"]} too close to the fill')
            else: ok()
        out.append((f, r, res_f.get(f'forbid/{f["fg"]}/{f["bg"]}', {}).get('p05')))
    return out


# گذر ۱: جمع‌کردن موارد؛ سنجش پیکسلی؛ گذر ۲: بررسی
cases = []
run(cases, None)
for f in SPEC['forbidden_pairs']:
    if f.get('shadow_demo'):
        cases.append(dict(key=f'forbid/{f["fg"]}/{f["bg"]}', fill=f['bg'], text=f['fg'], shadow=sh_of(f['bg']), layers=TS['layers_px'], family='Lalezar', size=24, weight=400, stroke=(TS['stroke_px'], sh_of(f['bg']))))
res = measure(cases, ring_px=W['ring_px'], percentile=W['ring_percentile'])
errs.clear(); n_ok = 0
run(cases, res)
forb = forbidden(res)
json.dump({k: round(v['p05'], 2) for k, v in res.items()}, open(V5 / 'spec' / 'measured.json', 'w'), indent=1)

# ---- مجاز روی تیره
A = SPEC['allowed_text_on_dark']
for bg in A['on']:
    for fg in A['colors']: check('allowed_dark', 'both', f'{fg} on dark', fg, bg, W['text_min'])
# ---- رشته‌ها
S = json.load(open(V5 / 'spec/strings.fa.json', encoding='utf-8'))
keys = set(re.findall(r'"((?:name|desc|note|why)_key)":\s*"([^"]+)"', (V5 / 'component_spec.json').read_text(encoding='utf-8')))
for kind, k in sorted(keys):
    if k not in S: err(f'strings.fa.json is missing {k}')
    else: ok()
for k, v in S.items():
    if v.get('kind') is None or v.get('text') is None: err(f'strings: {k} incomplete')
# ---- نمونه
html = V5 / 'spec_sample.html'
if html.exists():
    h = html.read_text(encoding='utf-8')
    if re.search(r'clip-path', h): err('spec_sample.html uses clip-path')
    else: ok()
    if re.search(r'border-radius:\s*0(px)?\s*[;}]', h): err('spec_sample.html has a zero radius')
    else: ok()
else: err('spec_sample.html is missing')

if TABLES:
    fa = lambda x, d=1: f'{x:.{d}f}'.translate(str.maketrans('0123456789.', '۰۱۲۳۴۵۶۷۸۹٫'))
    SS = json.load(open(V5 / 'spec/strings.fa.json', encoding='utf-8'))
    VN = dict(cyan='فیروزه‌ای', gold='زرد', pink='صورتی', violet='بنفش', plain='ساده', row='ردیف منو', opt_off='گزینهٔ خاموش', opt_on='گزینهٔ انتخاب‌شده', off='خاموش', on='روشن',
              shell='ردیف', badge_easy='نشان آسان', badge_mid='نشان متوسط', badge_hard='نشان سخت', easy='سبز (آسان)', mid='نارنجی (متوسط)', hard='قرمز (سخت)',
              sub_plate='پلاک جمله', node='گره', tag='پلاک «اختیاری»', label='برچسب گره', here='تو اینجایی', new='تازه', title_band='نوار عنوان', name_plate='پلاک نام',
              row_sub='جملهٔ زیر ردیف', seen='دیده‌شده', kept='جمع‌شده', locked='قفل')
    RN = lambda rid: SS['spec.row.' + rid]['text']
    print('| کنترل | نوع | حالت | پر | متن | سایه | متن به پر | با سایه | حد متن به پر |\n|---|---|---|---|---|---|---|---|---|')
    seen_rows = {}
    for rid, vid, mode, fill, text, shd, rf, eff, need in LOG: seen_rows.setdefault((rid, vid), {})[mode] = (fill, text, shd, rf, eff, need)
    for (rid, vid), m in seen_rows.items():
        same = 'day' in m and 'night' in m and m['day'][:3] == m['night'][:3] and abs(m['day'][4] - m['night'][4]) < .06
        for mode, label in ((('day', 'روز و شب'),) if same else (('day', 'روز'), ('night', 'شب'))):
            if mode not in m: continue
            fill, text, shd, rf, eff, need = m[mode]
            print(f'| {RN(rid)} | {VN.get(vid, vid)} | {label} | `{fill}` | `{text}` | {"`" + shd + "`" if shd else "—"} | {fa(rf)} | {fa(eff)} | {fa(need, 1)} |')
    print('\n--- forbidden ---')
    print('| نوشته | روی | نسبت | با سایه | ممنوع برای | چرا |\n|---|---|---|---|---|---|')
    for f, r, e in forb:
        print(f'| `{f["fg"]}` | `{f["bg"]}` | {fa(r, 2)} | {fa(e) if e else "—"} | {"هر اندازه" if f["scope"] == "all" else "زیر ۲۴px"} | {SS[f["why_key"]]["text"]} |')
for e in errs: print('FAIL', e)
print(f'{"OK" if not errs else "FAILED"}: {n_ok} checks passed, {len(errs)} failed; {len(SPEC["rows"])} rows, {len(forb)} forbidden pairs, {len(pal)} approved colors + {len(DER)} derived; {len(cases)} rendered measurements')
sys.exit(1 if errs else 0)
