#!/usr/bin/env python3
"""ایستگاه M06 «اتاق ابزار» (سرزمین شهر، پالت city).
طرح قطعه‌به‌قطعه (واحد symbol، قاب قهرمان pen.xf = ۰٫۸):
 ۱) پایهٔ سنگی (بلوک کرم #efe3c4 / روشن #fff7e0 / تیره #cdbb90): x -92..32، y -12..8، زیر تخته.
 ۲) تختهٔ ابزار دیواری (چوب زرد-کهربایی #f3cf7a / #ffe9a8 / #d9a647): x -88..30، y -118..-8؛ نوار ریل بالا قهوه‌ای کم‌رنگ
    و یک ردیف سوراخ تخت در پایین (تختهٔ سوراخ‌دار).
 ۳) قیچی (ستون چپ cx=-67): دو بازوی فولادی #d4dce8 (روشن #f6f9fd، تیره #94a2b8) با پیچ مرکزی و دو حلقهٔ دستهٔ بنفش #8b5fd0
    (روشن #b898ec، تیره #5d3a9e). نیمهٔ راست = لایهٔ متحرک node_tool_room_scissors حول پیچ؛ نیمهٔ چپ ثابت.
 ۴) چکش میخ‌کش (ستون میانی cx=-29): دستهٔ بنفش، سر فولادی با سطح کوبه (راست) و چنگک خمیده (چپ).
 ۵) انبردست (ستون راست cx=9): دو فک ضخیم کند، پیچ، دو دستهٔ بنفش راست. بدون آچار.
 رنگ قهرمان: چوب زرد ≈۴۵°، فولاد خنثی، بنفش ≈۲۶۰°؛ سکوی شهر آبی-خاکستری ≈۲۱۰° (فاصلهٔ ≥۳۵°).
 ماشین‌های ساده را نام نمی‌برد؛ فقط سه ابزار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/tool_room'

S_B, S_L, S_D = '#efe3c4', '#fff7e0', '#cdbb90'      # پایهٔ سنگی
W_B, W_L, W_D = '#f3cf7a', '#ffe9a8', '#d9a647'      # تخته
F_B, F_L, F_D = '#d4dce8', '#f6f9fd', '#94a2b8'      # فولاد
H_B, H_L, H_D = '#8b5fd0', '#b898ec', '#5d3a9e'      # دستهٔ بنفش
T_B, T_L, T_D = '#2fb5a8', '#7fe0d4', '#1f7f77'      # دستهٔ فیروزه‌ای (چکش)
SCREW = '#a8742a'
BX0, BX1, BY0, BY1 = -82, 26, -140, -8
XF = (0.85, 0.5, 0.0)


def poly(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def rect(p, x0, y0, x1, y1, col): poly(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col)


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r * p.xf[0], col))


def part(p, pts, col, sw=INNER):
    p.shape(pts, col, sw, j=.12, step=6, clip=False)


def ring(p, x, y, r, col, hole, sw=INNER):
    p.shape(ell(x, y, r, r, 0, 360, 20), col, sw, j=.05, step=99, clip=False)
    p.fill(ell(x, y, 3.2, 3.2, 0, 360, 14), hole)


def bar(a, b, w0, w1):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    return [(a[0] + nx * w0 / 2, a[1] + ny * w0 / 2), (b[0] + nx * w1 / 2, b[1] + ny * w1 / 2),
            (b[0] - nx * w1 / 2, b[1] - ny * w1 / 2), (a[0] - nx * w0 / 2, a[1] - ny * w0 / 2)]


def strip(a, b, off, w, t0=.12, t1=.88):
    """نوار روشن/تیرهٔ تخت موازی محور (off = فاصلهٔ عمود از محور)."""
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    p0 = (a[0] + dx * t0, a[1] + dy * t0); p1 = (a[0] + dx * t1, a[1] + dy * t1)
    return [(p0[0] + nx * off, p0[1] + ny * off), (p1[0] + nx * off, p1[1] + ny * off),
            (p1[0] + nx * (off + w), p1[1] + ny * (off + w)), (p0[0] + nx * (off + w), p0[1] + ny * (off + w))]


def board(p):
    part(p, [(BX0, BY0), (BX1, BY0), (BX1, BY1), (BX0, BY1)], W_B, PART)
    rect(p, BX0 + 5, BY0 + 5, BX1 - 5, BY0 + 8.5, W_L)                       # نور بالا
    rect(p, BX1 - 11, BY0 + 20, BX1 - 5, BY1 - 5, W_D)                       # سایهٔ تیز راست


def plinth(p):
    part(p, [(-86, -13), (28, -13), (28, 7), (-86, 7)], S_B, PART)
    rect(p, -81, -9, 18, -6.5, S_L)
    rect(p, 20, -6.5, 23, 2.5, S_D)
    rect(p, -81, 1.5, 23, 3.5, S_D)


def scissors(p, cx):
    P = (cx, -52); TIPY = -84; RC = (9.5, -29)

    def half(sg):
        tip = (cx - sg * 6, TIPY); rc = (cx + sg * RC[0], RC[1])
        part(p, bar(P, (rc[0], rc[1] - 3), 12.5, 12.5), H_B, INNER)
        ring(p, rc[0], rc[1], 7, H_B, W_B)
        poly(p, strip(P, rc, -4.4, 2.2, .3, .6), H_L)
        part(p, bar((P[0], P[1] + 3), tip, 13, 3.5), F_B, INNER)       # تیغه
        poly(p, strip((P[0], P[1]), tip, -3.7 * sg, 1.8, .2, .84), F_L)
    half(1)                                                                         # نیمهٔ ثابت (تیغه بالا-چپ)
    with layer(p, 'scissors'):                                                      # نیمهٔ متحرک
        half(-1)
    p.shape(ell(P[0], P[1] + 1, 4.6, 4.6, 0, 360, 14), F_D, INNER, j=.05, step=99, clip=False)
    p.fill(ell(P[0] - 1, P[1], 1.4, 1.4, 0, 360, 8), F_L)
    return P


def hammer(p, ox, oy):
    """چکش میخ‌کش افقی: دسته به راست، سطح کوبه بالا، چنگک پایین (چرخش ۹۰- درجه از طرح عمودی)."""
    f0 = rot(ox, oy, -90)
    f = lambda q: (lambda r: (r[0], 2 * oy - r[1]))(f0(q))     # آینهٔ عمودی: چنگک بالا، سطح کوبه پایین
    T = lambda pts: TP(f, pts)
    part(p, T(bar((0, 4), (0, 74), 13, 13)), T_B, INNER)
    poly(p, T(strip((0, 4), (0, 74), -4.3, 2.2, .3, .96)), T_L)
    poly(p, T(strip((0, 4), (0, 74), 2.2, 2.2, .3, .96)), T_D)
    claw = [(-4, -15), (-12, -14.5), (-19, -9), (-23, 0), (-24, 11), (-18, 3.5), (-13, -2), (-4, -4)]
    part(p, T(claw), F_B, INNER)
    part(p, T([(-8, -17), (16, -17), (16, 9), (-8, 9)]), F_B, INNER)
    poly(p, T([(-5, -14.5), (6, -14.5), (6, -12), (-5, -12)]), F_L)
    poly(p, T([(10.5, -14), (14, -14), (14, 6.5), (10.5, 6.5)]), F_D)


def pliers(p, cx):
    P = (cx, -54)
    for sg in (1, -1):                                                   # دو دستهٔ بنفش (زیر سر)
        rc = (cx + sg * 10, -25)
        part(p, bar((P[0], P[1] + 2), rc, 13, 13), H_B, INNER)
        poly(p, strip(P, rc, -4.3 if sg > 0 else 2.3, 2.2, .35, .92), H_L if sg > 0 else H_D)
    head = [(cx - 13, -46), (cx + 13, -46), (cx + 13, -62), (cx + 11, -88), (cx + 4.5, -88), (cx + 1.8, -68),
            (cx - 1.8, -68), (cx - 4.5, -88), (cx - 11, -88), (cx - 13, -62)]
    part(p, head, F_B, INNER)                                          # سر + دو فک با دهانهٔ V
    rect(p, cx - 9.5, -84, cx - 7.2, -60, F_L)
    rect(p, cx + 8, -80, cx + 10.5, -58, F_D)
    p.shape(ell(P[0], P[1], 4.8, 4.8, 0, 360, 14), F_D, INNER, j=.05, step=99, clip=False)
    p.fill(ell(P[0] - 1, P[1] - 1, 1.4, 1.4, 0, 360, 8), F_L)


def build(out=OUTD):
    p = Pen('tool_room', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-30, 8, 52); p.foot_tip(-30, 7, 30)
    board(p)
    for x, y in ((-75, -133), (19, -133)): disc(p, x, y, 2.4, SCREW)
    plinth(p)
    hammer(p, -56, -108)
    pliers(p, 1)
    pivot = scissors(p, -56)
    return p, pivot


STAND = None
if __name__ == '__main__':
    p, pivot = build()
    hm = p.X(pivot)
    r = finish(p, 'tool_room', STAND, motion={'scissors': dict(rotate=hm)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_tool_room_scissors': dict(center=[round(v, 1) for v in hm], angle_deg=25, dir='cw', note='نیمهٔ متحرک قیچی (تیغه+دسته) حول پیچ تا ≈۲۵° بیشتر باز می‌شود و به حالت ایستا برمی‌گردد؛ ۱٫۲ث؛ یک‌بار هنگام رسیدن؛ نیمهٔ چپ ثابت. حالت ایستا = نیمه‌باز پایان.'),
                         'reduced_motion': 'قیچی ثابت'}
    (OUTD / 'tool_room.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
