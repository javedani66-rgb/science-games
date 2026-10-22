#!/usr/bin/env python3
"""ایستگاه W04 «ایستگاه فضایی» (سرزمین فضا، سکوی بنفش ۲۵۶°) — دور ۶ (R6).
هدف: هم‌سطح «پیچ‌کاری»: بزرگ (≈۶۵٪ عرض سکو)، ¾، سه پلهٔ رنگ، ۶ جزء درشت. ماژول اصلی «استوانهٔ قائم» تا بالای آن رویه و بندر دیده شود.
طرح قطعه‌به‌قطعه (واحد symbol؛ مرکز بدنه x=0؛ محور بال‌ها y=-34):
 ۱) پایهٔ طلایی: ذوزنقه x ±14 تا y=12.
 ۲) ماژول اصلی: استوانهٔ قائم r=20 (ry=7)، y -58..-6، سفید-نقره‌ای سه پله (#eef1f7 / سفید / #aeb8d0)، دو دریچهٔ گرد r=5٫5، دو شیار منحنی.
 ۳) بندر (حلقهٔ طلایی روی رویه) + ماژول کوچک قائم r=9، y -72..-58 + آنتن با گوی قرمز.
 ۴) دو بال خورشیدی (لایهٔ panels): بازوی طلایی + پنل آبی روشن ۳۴×۵۸ مایل (¾) با شبکهٔ ۳×۴؛ سه پله (#3fb6f0 / #9be0ff / #1f78c4). حول (0,-34) ±۶°؛ ایستا = افقی."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from station_kit import *
from g4_helpers import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/space_station'

M_B, M_L, M_D = '#eef1f7', '#ffffff', '#aeb8d0'
G_B, G_L, G_D = '#f0b03c', '#ffd98a', '#b9741c'
P_B, P_L, P_D = '#3fb6f0', '#9be0ff', '#1f78c4'
GLASS = '#bfe6ff'; ROD = '#5b6684'; RED = '#e8503a'
CYA = -34


def wing(p, sg):
    X = lambda x, y: (sg * x, y)
    x0, x1 = 35, 63
    def Y(t, s):
        yt = -62 - 8 * t; yb = -2 - 8 * t
        return yt + s * (yb - yt)
    pn = [X(x0, -62), X(x1, -70), X(x1, -10), X(x0, -2)]
    arm = [(sg * 18, CYA - 5.5), (sg * 38, CYA - 5.5), (sg * 38, CYA + 5.5), (sg * 18, CYA + 5.5)]
    sharp(p, arm, G_B, 2.6)
    poly(p, [(sg * 21, CYA - 3.5), (sg * 36, CYA - 3.5), (sg * 36, CYA - 1.2), (sg * 21, CYA - 1.2)], G_L)
    sharp(p, pn, P_B, 3.6)
    xs = lambda t: x0 + (x1 - x0) * t
    poly(p, [X(xs(.06), Y(.06, .04)), X(xs(.3), Y(.3, .04)), X(xs(.3), Y(.3, .96)), X(xs(.06), Y(.06, .96))], P_L)
    poly(p, [X(xs(.72), Y(.72, .04)), X(xs(.94), Y(.94, .04)), X(xs(.94), Y(.94, .96)), X(xs(.72), Y(.72, .96))], P_D, .8)
    p.ln(X(xs(.5), Y(.5, .04)), X(xs(.5), Y(.5, .96)), 1.8, P_D, j=0)
    for s_ in (.33, .66):
        p.ln(X(xs(.04), Y(.04, s_)), X(xs(.96), Y(.96, s_)), 1.8, P_D, j=0)


def build(out=OUTD, ang=0):
    p = Pen('space_station', 'space'); pad(p, line=((-80, 12), (-66, 20)), tri=((74, -20), (80, 6)), dot=(-76, -14)); p.xf = (1.0, 0, 6)
    p.tipshadow(0, 10, 34); p.foot_tip(0, 9, 18)
    sharp(p, [(-15, 12), (15, 12), (10, -4), (-10, -4)], G_B, 3.6)
    poly(p, [(-10, 9), (-6, 9), (-5, -1), (-8, -1)], G_L)
    poly(p, [(5, -1), (8, -1), (11, 9), (7, 9)], G_D)
    with layer(p, 'panels'):
        cx_, cy_ = p.X((0, CYA))
        p.raw('<g transform="rotate(%s %.1f %.1f)">' % (ang, cx_, cy_))
        wing(p, -1); wing(p, 1)
        p.raw('</g>')
    # ماژول اصلی
    body = [(-21, -58), (21, -58)] + ell(0, -6, 21, 7.4, 0, 180, 24)
    p.shape(body, M_B, 3.6, j=.1, step=99, clip=False)
    poly(p, rect(-16, -54, -11, -8), M_L)
    arc = [(x, -6 + 7.4 * math.sqrt(1 - (x / 21) ** 2) - 1.8) for x in (19 - 6 * i / 8 for i in range(9))]
    poly(p, [(13, -53), (19, -53)] + arc, M_D)
    for y in (-53, -12): poly(p, band(0, y, 18.6, 6.6, 2.8), M_D)
    p.stroke(body, 3.6, j=.1, step=99)
    p.shape(ell(0, -58, 21, 7.4, 0, 360, 30), M_L, 3.6, j=.05, step=99, clip=False)
    for y in (-43, -24):
        p.shape(ell(-2, y, 6, 6, 0, 360, 16), GLASS, 2.6, j=.05, step=99, clip=False)
        poly(p, rect(-4.8, y - 3, -2.8, y - .8), '#ffffff')
    # ماژول کوچک (با کمربند بندر طلایی) + آنتن
    vcyl(p, 0, -74, -59, 10, 3.6, M_B, M_L, M_D, M_L, sw=3.6, lx=2.6)
    poly(p, band(0, -64, 9.4, 3.4, 3.4), G_B)
    p.ln((0, -76), (0, -91), 2.6, ROD, j=0)
    p.shape(ell(0, -93, 4, 4, 0, 360, 12), RED, 2.6, j=.05, step=99, clip=False)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    hm = p.X((0, CYA))
    r = finish(p, 'space_station', STAND, motion={'panels': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    st = r['spec']['stand']; ext = []
    for a_ in (-6, 6):
        q = build(ang=a_)
        ext.append((a_, motion_check(q, 'panels', offsets=[(0, 0)], stand=st), inside_check(q, {'panels': dict(offsets=[(0, 0)])})))
    print('EXT', json.dumps([(a, m['ok'], i['ok']) for a, m, i in ext], ensure_ascii=False))
    sp = r['spec']
    sp['motion_spec'] = {'node_space_station_panels': dict(center=[round(v, 1) for v in hm], max_angle_deg=6, pattern='0 -> +6 -> -6 -> 0', repeats=3, duration_s=6,
                                                          note='هر دو بال خورشیدی با بازو حول مرکز ماژول ±۶° مایل می‌شوند؛ فقط هنگام رسیدن؛ حالت ایستا = افقی (پایان)؛ بدون حلقهٔ بیکار.'),
                         'reduced_motion': 'بال‌ها ایستا'}
    (OUTD / 'space_station.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
