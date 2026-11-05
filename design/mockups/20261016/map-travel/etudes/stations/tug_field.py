#!/usr/bin/env python3
"""F08 «میدان طناب‌کشی» (سکوی sports، رنگ‌مایهٔ ۹۳°) — دور ۶ بازطراحی (هم‌سطح پیچ‌کاری).
قهرمان: طناب بسیار کلفت قهوه‌ای (کلفتی ۲۸) با تاب مورب، کشیده و کمی شل روی چمن، از چپ‌پایین تا راست‌بالا، ≈۸۰٪ عرض سکو.
طرح قطعه‌به‌قطعه (واحد symbol):
 ۱) طناب: لولهٔ منحنی (نیمرخ سهمی)، قهوه‌ای تیره #a8672c؛ نور بالا #e8b070 و سایهٔ پایین #6e3f16؛ ۱۰ نوار مورب روشن = تاب رشته‌ها.
 ۲) دو پارچهٔ بسته‌شده دور طناب: قرمز #e0443a (چپ) و آبی #3f74d9 (راست)، هرکدام سه پله.
 ۳) دو دستگیرهٔ کنده‌ای ایستاده (استوانهٔ چوب روشن کرم، r12، h40) در دو سر، سر طناب پشت آن‌ها؛ سایهٔ تماس.
 ۴) لایهٔ متحرک node_tug_field_flag: دکل سفید (۱۵) با پرچم زرد درشت، پایه روی وسط طناب؛ حالت ایستا = وسط.
رنگ قهرمان ≥۳۵° از ۹۳° (قهوه‌ای ۳۰°، قرمز ۵°، آبی ۲۲۰°، زرد ۴۸°). بدون پیکان/متن."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from station_kit import *
from r6_helpers import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/tug_field'
RP = ('#e0463a', '#ff9a86', '#a82a24')
WD = ('#f1dba6', '#fff7da', '#c19a55', '#fff0c0')
RR = 9; XL, XR = -46, 46


def cyl(p, cx, yb, r, h, cols, ry=None, sw=3.6, lit=.45, top=True):
    """استوانهٔ ایستاده؛ خط دور رویه هم‌ضخامت بدنه."""
    ry = ry or .34 * r; yt = yb - h
    sil = ell(cx, yb, r, ry, 0, 180, 16) + ell(cx, yt, r, ry, 180, 360, 16)
    p.shape(sil, cols[0], sw, j=.15, step=8)
    p.fill([(cx - r + 2, yt), (cx - r * (1 - lit), yt), (cx - r * (1 - lit), yb + ry), (cx - r + 2, yb)], cols[1])
    p.fill([(cx + r * .38, yt), (cx + r - 2, yt), (cx + r - 2, yb), (cx + r * .38, yb + ry * .9)], cols[2], .9)
    p.stroke(sil, sw, j=.15, step=8)
    if top: p.shape(ell(cx, yt, r, ry, 0, 360, 28), cols[3], sw, j=.1, step=99, clip=False)


def cy_(x): return -40 + 4 * (1 - (x / 48.) ** 2)          # طناب کشیده با افتادگی کم
def tan(x):
    h = .01; a, b = (x - h, cy_(x - h)), (x + h, cy_(x + h)); L = math.hypot(b[0] - a[0], b[1] - a[1]); return ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
def at(x, k):
    t = tan(x); n = (-t[1], t[0]); return (x + n[0] * RR * k, cy_(x) + n[1] * RR * k)


def build():
    p = Pen('tug_field', 'sports'); pad(p, line=((50, 30), (70, 27)), tri=((36, -22), (74, 6)), dot=(68, -14)); p.xf = (1.2, 0, -6)
    GYB = 14
    for x in (XL, XR):                                                                            # دو تیرک بلند
        p.fill(ell(x + 3, GYB + 3, 17, 5, 0, 360, 20), '#10083a', .25)
        cyl(p, x, GYB, 9.5, 92, WD, sw=3.6)
    xs = [XL + i * (XR - XL) / 48. for i in range(49)]
    top = [at(x, -1) for x in xs]; bot = [at(x, 1) for x in xs]
    rope = top + bot[::-1]
    p.fill([(x, y + 11) for x, y in rope], '#10083a', .2)
    p.shape(rope, RP[0], 3.6, j=.1, step=8)
    p.fill([at(x, -.85) for x in xs] + [at(x, -.35) for x in xs[::-1]], RP[1])
    p.fill([at(x, .5) for x in xs] + [at(x, .9) for x in xs[::-1]], RP[2], .85)
    for i in range(6):                                                                            # تاب رشته‌ها
        x = XL + 12 + i * 15
        t = tan(x); n = (-t[1], t[0])
        q = [(x - 4 + t[0] * 0 + n[0] * RR * -.85, cy_(x) - RR * .85), (x + 1, cy_(x) - RR * .85), (x + 7, cy_(x) + RR * .85), (x + 2, cy_(x) + RR * .85)]
        p.fill(q, RP[1], .9)
    p.stroke(rope, 3.6, j=.1, step=8)
    for x in (XL, XR):
        c = (x, cy_(x)); p.shape(ell(c[0], c[1], 11, 12, 0, 360, 24), '#8a1f1a', 3.6, j=.1, step=99, clip=False)
        p.fill(ell(c[0] - 3, c[1] - 3, 4, 3, 0, 360, 10), '#ff9a86')
    with layer(p, 'flag'):
        x0 = 0; yb = cy_(0) - 5
        cyl(p, x0, yb, 6, 40, ('#ffffff', '#ffffff', '#b8c4dc', '#ffffff'), sw=2.6)
        fl = [(x0 + 3, yb - 38), (x0 + 28, yb - 38), (x0 + 20, yb - 26), (x0 + 28, yb - 14), (x0 + 3, yb - 14)]
        p.shape(fl, '#ffd23f', 2.6, j=.1, step=4, clip=False)
        p.fill([(x0 + 8, yb - 34), (x0 + 23, yb - 34), (x0 + 23, yb - 30), (x0 + 8, yb - 30)], '#fff3a8')
    return p


if __name__ == '__main__':
    p = build(); SH = 9
    offs = [(0, 0), p.V((-SH, 1.3)), p.V((SH, -1.3)), (0, 0)]
    r = finish(p, 'tug_field', None, motion={'flag': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_tug_field_flag': dict(
        kind='دکل و پرچم روی وسط طناب؛ فقط translate در امتداد طناب؛ حالت ایستا = وسط (پایان)',
        keyframes_symbol_units=[[0, 0], [-SH, 1.3], [SH, -1.3], [0, 0]], duration_s=2.4, easing='ease-in-out', loop=False,
        trigger='رسیدن کودک (یک‌بار)', concept='نیروی برآیند: وسط ایستاده = برابر و مخالف؛ بدون برنده، بدون پیکان', reduced_motion='وسط')}
    (OUTD / 'tug_field.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')}, ensure_ascii=False))
