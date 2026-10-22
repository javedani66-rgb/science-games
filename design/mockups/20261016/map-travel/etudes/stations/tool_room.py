#!/usr/bin/env python3
"""ایستگاه M06 «اتاق ابزار» (سرزمین شهر، پالت city)، نسخهٔ دوم: فقط دو ابزار درشت.
طرح (واحد symbol، pen.xf = ۰٫۹):
 ۱) پایهٔ سنگی کرم (#efe3c4/#fff7e0/#cdbb90) زیر تخته.
 ۲) تختهٔ ابزار زرد-کهربایی (#f3cf7a/#ffe9a8/#d9a647)؛ نور بالا، سایهٔ تیز راست.
 ۳) چکش میخ‌کش عمودی (چپ): دستهٔ فیروزه‌ای، سر فولادی با سطح کوبه و چنگک کوچک.
 ۴) قیچی (راست، ×۱٫۲): دو تیغهٔ فولادی، دو دستهٔ بنفش با حلقه، پیچ مرکزی. نیمهٔ راست = لایهٔ متحرک node_tool_room_scissors.
 فاصلهٔ دو ابزار ≥ ۱۲ واحد؛ بدون انبر و بدون آچار. رنگ قهرمان ≥ ۳۵° از سکوی شهر (آبی-خاکستری)."""
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
BX0, BX1, BY0, BY1 = -73, 28, -122, -8
XF = (0.81, -4.0, 0.0)


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
    poly(p, [(BX1 - 5, BY0 + 5), (BX1 - 1.5, BY0 + 8), (BX1 - 1.5, BY1 - 1.5), (BX0 + 5, BY1 - 1.5), (BX0 + 8, BY1 - 5), (BX1 - 5, BY1 - 5)], W_D)  # سایهٔ تیز راست/پایین


def plinth(p):
    part(p, [(-77, -13), (32, -13), (32, 7), (-77, 7)], S_B, PART)
    rect(p, -72, -9, 22, -6.5, S_L)
    rect(p, 24, -6.5, 27, 2.5, S_D)
    rect(p, -72, 1.5, 27, 3.5, S_D)


def scissors(p, cx):
    k = 1.2
    P = (cx, -60); TIPY = P[1] - 32 * k; RC = (8.5 * k, P[1] + 28 * k - 0.0); R = 7.2 * k

    def half(sg):
        tip = (cx - sg * 6 * k, TIPY); rc = (cx + sg * RC[0], RC[1] - 4)
        part(p, bar(P, (rc[0], rc[1] - 3), 12.5, 12.5), H_B, INNER)
        ring(p, rc[0], rc[1], R, H_B, W_B)
        poly(p, strip(P, rc, -4.4, 2.2, .3, .6), H_L)
        part(p, bar((P[0], P[1] + 3), tip, 14, 4), F_B, INNER)       # تیغه
        poly(p, strip((P[0], P[1]), tip, -3.9 * sg, 2.0, .2, .84), F_L)
    half(1)                                                                         # نیمهٔ ثابت
    with layer(p, 'scissors'):                                                      # نیمهٔ متحرک
        half(-1)
    p.shape(ell(P[0], P[1] + 1, 5, 5, 0, 360, 14), F_D, INNER, j=.05, step=99, clip=False)
    p.fill(ell(P[0] - 1, P[1], 1.5, 1.5, 0, 360, 8), F_L)
    return P


def hammer(p, cx, oy):
    """چکش میخ‌کش عمودی: دسته پایین، سر فولادی بالا، چنگک کوچک چپ."""
    hx = cx + 2
    part(p, bar((hx, oy + 4), (hx, oy + 66), 13.5, 13.5), T_B, INNER)
    poly(p, strip((hx, oy + 4), (hx, oy + 66), -4.5, 2.2, .3, .96), T_L)
    poly(p, strip((hx, oy + 4), (hx, oy + 66), 2.3, 2.2, .3, .96), T_D)
    claw = [(-6, -15), (-12, -14.5), (-17, -9), (-20, 0), (-20, 10), (-15, 3.5), (-11, -2), (-6, -4)]
    part(p, [(cx + x, oy + y) for x, y in claw], F_B, INNER)
    part(p, [(cx - 8, oy - 17), (cx + 14, oy - 17), (cx + 14, oy + 9), (cx - 8, oy + 9)], F_B, INNER)
    rect(p, cx - 4.5, oy - 14.5, cx + 6, oy - 12, F_L)
    rect(p, cx + 8.5, oy - 14, cx + 11.5, oy + 6.5, F_D)


def build(out=OUTD):
    p = Pen('tool_room', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((44, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-24, 8, 48); p.foot_tip(-24, 7, 28)
    board(p)
    plinth(p)
    hammer(p, -47, -92)
    pivot = scissors(p, 2)
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
