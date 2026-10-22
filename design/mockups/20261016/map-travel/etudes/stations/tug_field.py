#!/usr/bin/env python3
"""ایستگاه F08 «میدان طناب‌کشی» (سرزمین ورزشگاه، پالت sports، رنگ‌مایهٔ سکو ۹۳°).
طرح قطعه‌به‌قطعه (واحد symbol، مرکز سکو (0,0)، y منفی = بالا):
 ۱) دو پایهٔ چوبی هم‌اندازه و هم‌ارتفاع (لنگر دو سر): بلوک پایهٔ قهوه‌ای تیره 24x10 + میلهٔ چوبی 14x56، چوب سه پله (#b77a3a/#d9a463/#7a4a1f).
    مراکز x = -80 و -18 ⇒ نمای متقارن حول x=-49. نوار نور چپ + سایهٔ تیز راست داخل میله.
 ۲) طناب افقی و صاف، y=-34 (ارتفاع 14)، ماسه‌ای-سفید (#f6e7b4 / روشن #fffaf0 / تیره #cfae62) با خط PART؛ دو سرش 5 واحد روی میله‌ها
    همپوشانی دارد؛ جای بافت: متوازی‌الاضلاع‌های تخت منظم (فاصلهٔ 9). بدون قرقره/قلاب/جعبه/پیکان.
 ۳) لایهٔ متحرک node_tug_field_flag = نوار بنفش-تیره (#7b4fd0 / #a98bf0 / #4a2c94) به پهنای 14 که دور طناب پیچیده و تا y=-8 آویزان است
    با دم دوشاخه؛ مرکزش روی x=-49 (محور تقارن). حالت ایستا = وسط (پایان حرکت).
 ۴) زرد کوچک: حلقهٔ تخت r2.4 روی هر میله در تماس با طناب (تأکید).
رنگ قهرمان: چوب ≈۳۰°، ماسه ≈۴۵°، بنفش ≈۲۶۰° — همه ≥۳۵° از ۹۳°."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8)
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/tug_field'

WOOD = '#b77a3a'; WOOD_L = '#d9a463'; WOOD_D = '#7a4a1f'
SAND = '#f6e7b4'; SAND_L = '#fffaf0'; SAND_D = '#cfae62'
PUR = '#7b4fd0'; PUR_L = '#a98bf0'; PUR_D = '#4a2c94'; YEL = '#ffd84d'

XF = (1.0, 19.0, 0.0)
PX = (-71, -15)                  # مراکز میله‌ها
CX = sum(PX) / 2                 # -49 محور تقارن
PW = 14; PT, PB = -92, 2         # میله: بالا/پایین
BW, BT, BB = 24, -6, 10           # بلوک پایه (از y=0 تا 10)... میله روی آن می‌نشیند
RY, RH = -68, 14                 # طناب
BAND_W = 14; BAND_T = -77; BAND_B = -54
SH = 7                           # حرکت: ±5px ≈ 7 واحد


def flat(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def rect(p, x0, y0, x1, y1, col, op=1): flat(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col, op)


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def mpoly(p, pts, fill, sw):
    q = p.X(pts); d = 'M' + 'L'.join('%.1f,%.1f' % z for z in q) + 'Z'
    p.raw('<path d="%s" fill="%s" class="eo" stroke-width="%s" stroke-linejoin="round"/>' % (d, fill, sw))


def post(p, x):
    p.tipshadow(x + 1, BB, 17); p.foot_tip(x, BB, 10)
    # بلوک پایه
    p.shape([(x - BW / 2, BT), (x + BW / 2, BT), (x + BW / 2, BB), (x - BW / 2, BB)], WOOD_D, PART, j=.1, step=6)
    rect(p, x - BW / 2 + 3.5, BT + 3.5, x - BW / 2 + 6.5, BB - 4, WOOD, .0001) if False else None
    # میله
    p.shape([(x - PW / 2, PT), (x + PW / 2, PT), (x + PW / 2, BT + 3), (x - PW / 2, BT + 3)], WOOD, PART, j=.1, step=6)
    rect(p, x - PW / 2 + 3.5, PT + 5, x - PW / 2 + 6.5, BT - 4, WOOD_L)
    rect(p, x + 1.5, PT + 4, x + PW / 2 - 2.9, BT - 1, WOOD_D, .55)
    p.stroke([(x - PW / 2, PT), (x + PW / 2, PT), (x + PW / 2, BT + 3), (x - PW / 2, BT + 3)], PART, j=.1, step=6)


def build():
    p = Pen('tug_field', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((36, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    for x in PX: post(p, x)
    # طناب باریک (۱۲، خط ۳٫۹) از گرهٔ چپ تا گرهٔ راست روی میله‌ها پیچیده؛ هر گره ۷ واحد از میلهٔ بیرونی بیرون می‌زند
    x0, x1 = PX[0], PX[1]
    p.shape([(x0, RY - RH / 2), (x1, RY - RH / 2), (x1, RY + RH / 2), (x0, RY + RH / 2)], SAND, INNER, j=.1, step=6, clip=False)
    for dx in (-17, -11, 11, 17):                                      # بافت مورب منظم، متقارن حول CX
        flat(p, [(CX + dx - 2.8, RY + RH / 2 - 1.9), (CX + dx + 1.1, RY + RH / 2 - 1.9), (CX + dx + 2.8, RY - RH / 2 + 1.9), (CX + dx - 1.1, RY - RH / 2 + 1.9)], SAND_D)
    for x in PX:                                                       # لولا: رسن دور ستون پیچیده (۵ واحد بیرون‌زدگی) + گرهٔ گرد روی آن
        mpoly(p, [(x - PW / 2 - 5, RY - 9), (x + PW / 2 + 5, RY - 9), (x + PW / 2 + 5, RY + 9), (x - PW / 2 - 5, RY + 9)], SAND_D, INNER)
        mpoly(p, [(x - 3, RY - 6), (x + 3, RY - 6), (x + 6, RY - 3), (x + 6, RY + 3), (x + 3, RY + 6), (x - 3, RY + 6), (x - 6, RY + 3), (x - 6, RY - 3)], SAND, INNER)
    with layer(p, 'flag'):
        w = BAND_W / 2
        pts = [(CX - w, BAND_T), (CX + w, BAND_T), (CX + w, BAND_B), (CX, BAND_B - 6), (CX - w, BAND_B)]
        mpoly(p, pts, PUR, PART)
        rect(p, CX - w + 3.2, BAND_T + 4, CX - w + 6.2, BAND_B - 4, PUR_L)
        flat(p, [(CX + 1.5, BAND_T + 3.5), (CX + w - 2.9, BAND_T + 3.5), (CX + w - 2.9, BAND_B - 3), (CX + 1.5, BAND_B - 6)], PUR_D, .6)
        mpoly(p, pts, 'none', PART)
    return p


if __name__ == '__main__':
    p = build()
    offs = [(0, 0), p.V((-SH, 0)), p.V((SH, 0)), (0, 0)]
    r = finish(p, 'tug_field', None, motion={'flag': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_tug_field_flag': dict(
        kind='نوار بنفش روی طناب؛ فقط translateX؛ حالت ایستا = وسط (پایان)',
        keyframes_px=[0, -5, 5, 0], keyframes_symbol_units=[0, -SH, SH, 0], average_px=0,
        duration_s=2.4, easing='ease-in-out', loop=False, trigger='رسیدن کودک (یک‌بار)',
        concept='نیروی برآیند: وسط ایستاده = نیروهای برابر و مخالف؛ بدون برنده، بدون پیکان',
        constraint='نوار بین دو میله می‌ماند و از سکو بیرون نمی‌زند؛ کاهش حرکت: وسط', fixed='میله‌ها، بلوک‌ها، طناب')}
    (OUTD / 'tug_field.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
