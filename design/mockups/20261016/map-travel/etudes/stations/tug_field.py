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
RP = ('#a8672c', '#e8b070', '#6e3f16')
WD = ('#f1dba6', '#fff7da', '#c19a55', '#fff0c0')
RR = 17; XL, XR = -60, 58


def cy_(x): return -.30 * x - 3             # خط مرکز طناب (موج ملایم)
def tan(x):
    h = .01; a, b = (x - h, cy_(x - h)), (x + h, cy_(x + h)); L = math.hypot(b[0] - a[0], b[1] - a[1]); return ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
def at(x, k):                                                    # نقطه روی مقطع طناب: k=-1 بالا .. +1 پایین
    t = tan(x); n = (-t[1], t[0]); return (x + n[0] * RR * k, cy_(x) + n[1] * RR * k)


def cn(x, u, k):                                                  # نقطه با طول u و عمق k در چارچوب ثابتِ مقطع x
    t = tan(x); n = (-t[1], t[0]); return (x + t[0] * u + n[0] * RR * k, cy_(x) + t[1] * u + n[1] * RR * k)


def band(p, x, w, cols):
    q = [cn(x, -w, -1.1), cn(x, w, -1.1), cn(x, w, 1.1), cn(x, -w, 1.1)]
    p.shape(q, cols[0], INNER, j=.1, step=4, clip=False)
    p.fill([cn(x, -w + 2.5, -.85), cn(x, -w + 6, -.85), cn(x, -w + 6, .85), cn(x, -w + 2.5, .85)], cols[1])
    p.fill([cn(x, w - 6, -.85), cn(x, w - 2.5, -.85), cn(x, w - 2.5, .85), cn(x, w - 6, .85)], cols[2], .9)
    p.stroke(q, INNER, j=.1, step=4)


def build():
    p = Pen('tug_field', 'sports'); pad(p, line=((50, 30), (70, 27)), tri=((36, -22), (74, 6)), dot=(68, -14)); p.xf = (1.0, 0, 0)
    xs = [XL + i * (XR - XL) / 48. for i in range(49)]
    top = [at(x, -1) for x in xs]; bot = [at(x, 1) for x in xs]
    capR = [(XR + math.cos(math.radians(a)) * 0, cy_(XR) + math.sin(math.radians(a)) * RR) for a in range(-80, 81, 20)]
    capL = [(XL - math.cos(math.radians(a)) * 0, cy_(XL) + math.sin(math.radians(a)) * RR) for a in range(80, -81, -20)]
    rope = top + bot[::-1]
    p.fill([(x, y + 9) for x, y in rope], '#10083a', .22)                                          # سایهٔ تماس
    p.foot_tip(XL, cy_(XL) + 8, 12); p.foot_tip(XR, cy_(XR) + 8, 12)
    p.shape(rope, RP[0], OUT, j=.15, step=8)
    p.fill([at(x, -.88) for x in xs] + [at(x, -.4) for x in xs[::-1]], RP[1])                      # نور بالا
    p.fill([at(x, .45) for x in xs] + [at(x, .92) for x in xs[::-1]], RP[2], .85)                  # سایهٔ پایین
    for i in range(7):                                                                            # تاب رشته‌ها: نوار روشن مورب + درز
        x = XL + 12 + i * 16.5
        p.fill([cn(x, -9, -.8), cn(x, -2, -.8), cn(x, 9, .8), cn(x, 2, .8)], RP[1], .9)
        p.ln(cn(x, 3, -.98), cn(x, 14, .98), INNER, '#4a2a0c', j=.05)
    p.stroke(rope, OUT, j=.15, step=8)
    for x in (XL, XR):                                                                            # گرهٔ درشت دو سر
        c = (x, cy_(x)); p.shape(ell(c[0], c[1], 13, 13, 0, 360, 24), '#7a4a1c', PART, j=.1, step=99, clip=False)
        p.fill(ell(c[0] - 4, c[1] - 4, 4.5, 3.5, 0, 360, 10), '#d9a060')
    band(p, -26, 8, ('#e0443a', '#ff9a86', '#a82a24'))
    band(p, 24, 8, ('#3f74d9', '#8fb4ff', '#264c9a'))
    with layer(p, 'flag'):
        x0 = 0; yb = cy_(0) - 4
        cyl(p, x0, yb, 7.5, 62, ('#ffffff', '#ffffff', '#b8c4dc', '#ffffff'), sw=PART, top=True)
        fl = [(x0 + 3, yb - 58), (x0 + 50, yb - 58), (x0 + 38, yb - 44), (x0 + 50, yb - 30), (x0 + 3, yb - 30)]
        p.shape(fl, '#ffd23f', PART, j=.1, step=4, clip=False)
        p.fill([(x0 + 9, yb - 53), (x0 + 44, yb - 53), (x0 + 44, yb - 48), (x0 + 9, yb - 48)], '#fff3a8')
        p.fill([(x0 + 9, yb - 36), (x0 + 42, yb - 36), (x0 + 42, yb - 33.5), (x0 + 9, yb - 33.5)], '#d99a14', .9)
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
