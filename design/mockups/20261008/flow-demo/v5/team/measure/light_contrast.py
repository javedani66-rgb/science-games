#!/usr/bin/env python3
"""سنجش کنتراست/رنگ‌مایه/کوررنگی برای تیم گرافیک v5 (نور). فقط روشنایی و رنگ؛ آزمون کودک نیست.
اجرا:  python3 light_contrast.py [مسیر zone_tokens.json] [--out پوشه]
خروجی: light_contrast.md و light_contrast.json کنار این فایل (یا --out).  کد خروج 1 اگر ردیف قرمز باشد."""
import json, sys, os, colorsys, math

HERE = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
TOK = args[0] if args else os.path.join(HERE, '..', 'assets', 'light', 'zone_tokens.json')
OUT = HERE
if '--out' in sys.argv: OUT = sys.argv[sys.argv.index('--out') + 1]
T = json.load(open(TOK))

def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def lin(v): v /= 255; return v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
def Y(h): r, g, b = map(lin, rgb(h)); return .2126 * r + .7152 * g + .0722 * b
def cr(a, b): ya, yb = Y(a), Y(b); return (max(ya, yb) + .05) / (min(ya, yb) + .05)
def hsv(h): r, g, b = [c / 255 for c in rgb(h)]; return colorsys.rgb_to_hsv(r, g, b)
def hue(h): return hsv(h)[0] * 360
def hd(a, b): d = abs(hue(a) - hue(b)) % 360; return min(d, 360 - d)
def lab(h):
    r, g, b = map(lin, rgb(h))
    x = (.4124 * r + .3576 * g + .1805 * b) / .95047; y = (.2126 * r + .7152 * g + .0722 * b); z = (.0193 * r + .1192 * g + .9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > .008856 else 7.787 * t + 16 / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))
def dE(a, b): return math.dist(lab(a), lab(b))
def chroma(h): L, a, b = lab(h); return math.hypot(a, b)
def sim(h, M):  # شبیه‌سازی کوررنگی Machado 2009 (شدت کامل) در RGB خطی
    v = [lin(c) for c in rgb(h)]
    o = [max(0, min(1, sum(M[i][j] * v[j] for j in range(3)))) for i in range(3)]
    f = lambda x: round(255 * (12.92 * x if x <= .0031308 else 1.055 * x ** (1 / 2.4) - .055))
    return '#%02x%02x%02x' % tuple(f(x) for x in o)
DEUT = [[.367322, .860646, -.227968], [.280085, .672501, .047413], [-.01182, .04294, .968881]]
PROT = [[.152286, 1.052583, -.204868], [.114503, .786281, .099216], [-.003882, -.048116, 1.051998]]
def gray(h): y = Y(h); v = round(255 * (12.92 * y if y <= .0031308 else 1.055 * y ** (1 / 2.4) - .055)); return '#%02x%02x%02x' % (v, v, v)

U, P, Z, W, I = T['ui'], T['path'], T['zones'], T['water'], T['ice']
LI = T['lights']; H = T['hardness']
rows = []  # (بخش, نام, نور, fg, bg, حداقل, نتیجه‌متن, ok, توضیح)
def add(sec, name, light, fg, bg, mn, note='', two=None):
    """two=(outline) → قاعدهٔ دو‌لایه: پر/زمین ≥mn یا (خط/زمین ≥3 و پر/خط ≥3)."""
    v = cr(fg, bg); ok = v >= mn; how = 'پر'
    if not ok and two:
        a, b = cr(two, bg), cr(fg, two)
        if a >= 3 and b >= 3: ok, how = True, f'دو‌لایه: خط/زمین {a:.2f}، پر/خط {b:.2f}'
    rows.append(dict(sec=sec, name=name, light=light, fg=fg, bg=bg, min=mn, val=round(v, 2), ok=ok, how=how if ok else '', note=note))

for L, d in LI.items():
    add('۱ آسمان/آب', 'افق آسمان ÷ آب', L, d['sky2'], d['water'], 1.5)
    add('۲ آب/زمین', 'آب ÷ اسکلهٔ بتنی', L, d['water'], d['pier'], 1.5)
    add('۳ بنا/آب', 'بنا ÷ آب (پر)', L, d['build'], d['water'], 3, 'قاعدهٔ سند ۴-۳')
    add('۴ بنا/زمین', 'بنا ÷ پایهٔ بتنی (دو‌لایه)', L, d['build'], d['pier'], 1.5, '', two=d['line'])
    add('۵ سایه/زمین', 'سایهٔ خودی ÷ سطح روشن بنا', L, d['build'], d['shade'], 1.5)
    add('۵ سایه/زمین', 'rim ÷ سایه (بُعد دیده شود)', L, d['lit'], d['shade'], 3)
    add('۴ بنا/زمین', 'خط دور (لبهٔ سیلوئت) ÷ آب', L, d['line'], d['water'], 3)
add('۴ بنا/زمین', 'بنا شب Y≥0.20', 'night', LI['night']['build'], '#000000', 1, f"Y={Y(LI['night']['build']):.2f}")
for L, mn in (('dusk', .30), ('night', .20)):
    y = Y(LI[L]['build']); rows.append(dict(sec='۴ بنا/زمین', name=f'Y بنا ≥{mn}', light=L, fg=LI[L]['build'], bg='-', min=mn, val=round(y, 2), ok=y >= mn, how='', note=''))
rows = [r for r in rows if r['name'] != 'بنا شب Y≥0.20']

for zk, z in Z.items():
    s = f'زمین {zk}'
    add('۶ گره/زمین', f'{zk}: حلقه ÷ زمین', 'day', z['ring'], z['base'], 3, f'حلقه با خط دور {z["ring_outline_px"]}px', two=U['line'])
    add('۶ گره/زمین', f'{zk}: لکه ÷ پایه (≥1.2)', 'day', z['patch'], z['base'], 1.2)
    add('۶ گره/زمین', f'{zk}: سایهٔ زمین ÷ پایه (≥1.5)', 'day', z['shade'], z['base'], 1.5)
    add('۷ حلقه/خط', f'{zk}: حلقه ÷ خط دور', 'day', z['ring'], U['line'], 3)
    add('۸ مسیر/زمین', f'{zk}: خط دور مسیر ÷ زمین', 'day', P['outline'], z['base'], 3, '', two=None)
    add('۸ مسیر/زمین', f'{zk}: کرم مسیر ÷ خط دور', 'day', P['cream'], P['outline'], 3)
    add('۹ برچسب/زمین', f'{zk}: متن خط ÷ پلاک کرم', 'day', U['line'], U['cream'], 4.5)
    add('۹ برچسب/زمین', f'{zk}: خط پلاک ÷ زمین', 'day', U['line'], z['base'], 3)
    add('۱۰ قفل/گره', f'{zk}: قفل (کرم ÷ بنفش)', 'day', U['cream'], U['deep_violet'], 4.5)
    add('۱۰ قفل/گره', f'{zk}: بنفش قفل ÷ زمین', 'day', U['deep_violet'], z['base'], 3, '', two=U['cream'])
    for hk, h in H.items():
        add('۱۱ سختی/زمین', f'{zk}: قرص {hk} ÷ زمین', 'day', h['hex'], z['base'], 3, 'روز: خط 2.6 #0d0426 بدون حاشیهٔ کرم', two=U['badge_line_day'])
    add('۱۲ تیتر/کارت', f'{zk}: رنگ شب ÷ زمینهٔ کارت', 'night', z['night'], U['card_bg'], 4.5)
add('۱۲ تیتر/کارت', 'متن کرم ÷ زمینهٔ کارت', 'night', U['cream'], U['card_bg'], 4.5)
add('۱۲ تیتر/کارت', 'جملهٔ کارت کرم ÷ #12243a', 'night', U['cream'], U['card_text_bg'], 7)
add('۱۲ تیتر/کارت', 'قفسه ÷ زمینهٔ کارت', 'night', U['shelf'], U['card_bg'], 1.1)
add('۱۱ سختی/زمین', 'قرص آسان ÷ کارت شب', 'night', H['easy']['hex'], U['card_bg'], 3, 'با حاشیهٔ کرم', two=U['cream'])
add('۱۱ سختی/زمین', 'قرص قرمز ÷ کارت شب', 'night', H['hard']['hex'], U['card_bg'], 3, 'با حاشیهٔ کرم', two=U['cream'])
for hk, h in H.items():
    add('۱۱ سختی/قرص', f'قله‌های کرم ÷ پر {hk}', 'day', U['cream'], h['hex'], 3, 'قله با خط 1.2', two=U['line'])
add('رابط', 'دکمهٔ اصلی: متن خط ÷ فیروزه‌ای', 'day', U['line'], U['teal'], 4.5)
add('رابط', 'خطر/نگه‌دار: کرم ÷ بنفش #8a4fd0', 'day', U['cream'], U['danger_violet'], 4.5)
add('رابط', 'چیپ غیرفعال: کرم ÷ #3a2a7a', 'day', U['cream'], U['deep_violet'], 4.5)
add('بنا/آب', 'بنا ÷ دریای اسکله (پر)', 'day', LI['day']['build'], W['sea'], 3)
add('رابط', 'دکمهٔ فیلم: خط ÷ صورتی', 'day', U['line'], U['pink'], 4.5)
add('رابط', 'تیرهٔ کارت‌دان: سفید ÷ #190539', 'night', U['white'], U['card_bg'], 4.5)
add('یخ/مسیر', 'یخ (بدنه) ÷ ابر', 'day', I['body'], I['cloud'], 1.5, 'سند: ≥1.5 (ابر فقط آسمان؛ مرز لب)', two=None)
add('یخ/مسیر', 'لب یخ ÷ ابر', 'day', I['rim'], I['cloud'], 1.05, 'فقط اطلاع')
add('یخ/مسیر', 'خط دور مسیر ÷ بدنهٔ یخ', 'day', P['outline'], I['body'], 3)
add('یخ/مسیر', 'پلهٔ چوبی ÷ بدنهٔ یخ (پر)', 'day', P['boardwalk'], I['body'], 1.5)
add('یخ/مسیر', 'خط دور پله ÷ بدنهٔ یخ', 'day', P['outline'], I['body'], 3)

# --- رنگ‌مایه / اشباع / روشنایی هر زمین با سه سختی
hue_rows = []
def hue_check(zname, base):
    for hk, h in H.items():
        hx = h['hex']; d = hd(base, hx)
        dc = abs(chroma(base) - chroma(hx)); dl = abs(lab(base)[0] - lab(hx)[0]); ds = abs(hsv(base)[1] - hsv(hx)[1]); dv = abs(hsv(base)[2] - hsv(hx)[2])
        ok1 = d >= 35; ok2 = (dl >= 15 and dc >= 20)
        hue_rows.append(dict(zone=zname, level=hk, hue_zone=round(hue(base)), hue_hard=round(hue(hx)), dist=round(d), dL=round(dl, 1), dC=round(dc, 1), dS=round(ds, 2), dV=round(dv, 2),
                             rule='رنگ‌مایه ≥35°' if ok1 else ('قاعدهٔ دوم: ΔL*≥15 و ΔC*≥20' if ok2 else 'رد'), ok=ok1 or ok2))
for zk, z in Z.items(): hue_check(zk, z['base'])
for nm, hx_ in [('ui:teal', U['teal']), ('ui:danger_violet', U['danger_violet']), ('ui:pink', U['pink'])] + [('costume:' + c, c) for c in T['costume_allowed'][:-1]]: hue_check(nm, hx_)
if 'farm_alt' in T: hue_check('farm_alt(گزینهٔ ۲)', T['farm_alt']['base'])

# --- خاکستری (روشنایی)  و حلقهٔ ۱۰px مزرعه
gray_rows = []
for zk, z in Z.items():
    gray_rows.append(dict(zone=zk, base_gray=gray(z['base']), Y=round(Y(z['base']), 2), ring_gray=gray(z['ring']), outline_vs_zone=round(cr(U['line'], z['base']), 2), ring_vs_outline=round(cr(z['ring'], U['line']), 2),
                          ring_shape_reads=cr(U['line'], z['base']) >= 3 and cr(z['ring'], U['line']) >= 3))
zone_pairs = []
ks = list(Z)
for i in range(len(ks)):
    for j in range(i + 1, len(ks)):
        zone_pairs.append((ks[i], ks[j], round(cr(Z[ks[i]]['base'], Z[ks[j]]['base']), 2)))

# --- کوررنگی: سه سختی
cb = []
for name, M in (('deutan', DEUT), ('protan', PROT)):
    sims = {k: sim(h['hex'], M) for k, h in H.items()}
    for a, b in (('easy', 'mid'), ('mid', 'hard'), ('easy', 'hard')):
        cb.append(dict(sim=name, pair=f'{a}/{b}', dE=round(dE(sims[a], sims[b]), 1), ratio=round(cr(sims[a], sims[b]), 2), colors=f'{sims[a]} {sims[b]}'))
cb_ok = all(c['dE'] >= 15 or c['ratio'] >= 1.3 for c in cb)

bad = [r for r in rows if not r['ok']]; badh = [h for h in hue_rows if not h['ok'] and not h['zone'].startswith('farm_alt')]
res = dict(tokens=os.path.basename(TOK), rows=rows, hue=hue_rows, gray=gray_rows, zone_gray_pairs=zone_pairs, colorblind=cb, colorblind_ok=cb_ok,
           red_count=len(bad) + len(badh) + (0 if cb_ok else 1))
json.dump(res, open(os.path.join(OUT, 'light_contrast.json'), 'w'), ensure_ascii=False, indent=1)

m = [f'# سنجش نور و رنگ (خودکار)\n', f'منبع: `{os.path.basename(TOK)}`؛ ابزار: `light_contrast.py`. فقط روشنایی/رنگ؛ آزموده‌نشده با کودک.\n',
     f'**ردیف قرمز: {res["red_count"]}** (کنتراست {len(bad)}، رنگ‌مایه {len(badh)}، کوررنگی {0 if cb_ok else 1})\n', '## ۱) کنتراست (۱۲ جفت × نور)\n',
     '| بخش | جفت | نور | پیش‌زمینه | زمینه | مقدار | حداقل | حکم |', '|---|---|---|---|---|---|---|---|']
for r in rows:
    m.append(f"| {r['sec']} | {r['name']} | {r['light']} | `{r['fg']}` | `{r['bg']}` | {r['val']} | {r['min']} | {'قبول ' + r['how'] if r['ok'] else '**قرمز**'} |")
m += ['\n## ۲) رنگ‌مایه و فاصله از سه سختی\n', 'قبول اگر فاصلهٔ رنگ‌مایه ≥35° یا (ΔL*≥15 و ΔC*≥20).\n',
      '| زمین | رنگ‌مایه | سختی | رنگ‌مایه سختی | فاصله° | ΔL* | ΔC* | ΔS | ΔV | حکم |', '|---|---|---|---|---|---|---|---|---|---|']
for h in hue_rows: m.append(f"| {h['zone']} | {h['hue_zone']} | {h['level']} | {h['hue_hard']} | {h['dist']} | {h['dL']} | {h['dC']} | {h['dS']} | {h['dV']} | {h['rule'] if h['ok'] else '**قرمز**'} |")
m += ['\n(گزینهٔ دوم مزرعه #c9c46a اگر «رد» است قرمز شمرده نمی‌شود؛ فقط ثبت می‌شود که انتخاب نشد.)']
m += ['\n## ۳) آزمون خاکستری\n', '| زمین | خاکستری | Y | خط÷زمین | حلقه÷خط | شکل حلقه خوانده می‌شود |', '|---|---|---|---|---|---|']
for g in gray_rows: m.append(f"| {g['zone']} | `{g['base_gray']}` | {g['Y']} | {g['outline_vs_zone']} | {g['ring_vs_outline']} | {'بله' if g['ring_shape_reads'] else '**نه**'} |")
m += ['\nکنتراست روشنایی بین زمین‌ها (اطلاع؛ زمین‌ها عمداً کم‌اختلاف‌اند): ' + '، '.join(f'{a}/{b} {v}' for a, b, v in zone_pairs)]
m += ['\n## ۴) کوررنگی (شبیه‌سازی Machado، شدت کامل) روی سه سختی\n', 'قبول اگر ΔE≥15 یا کنتراست روشنایی ≥1.3 (علاوه بر قله و واژه).\n', '| شبیه‌سازی | جفت | ΔE | کنتراست | رنگ‌ها |', '|---|---|---|---|---|']
for c in cb: m.append(f"| {c['sim']} | {c['pair']} | {c['dE']} | {c['ratio']} | {c['colors']} |")
open(os.path.join(OUT, 'light_contrast.md'), 'w').write('\n'.join(m) + '\n')
print('red rows:', res['red_count'])
for r in bad: print('  RED', r['sec'], r['name'], r['light'], r['fg'], r['bg'], r['val'], '<', r['min'])
for h in badh: print('  RED hue', h['zone'], h['level'], h['dist'], h['dL'], h['dC'])
if not cb_ok: print('  RED colorblind', [c for c in cb if not (c['dE'] >= 15 or c['ratio'] >= 1.3)])
sys.exit(1 if res['red_count'] else 0)
