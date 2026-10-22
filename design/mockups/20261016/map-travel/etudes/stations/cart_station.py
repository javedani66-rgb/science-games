#!/usr/bin/env python3
"""ایستگاه E02 «ایستگاه گاری‌ها» (سرزمین مزرعه، پالت farm) — دور ۵ (فرمان مدیر هنری). نمای کنار، بدون حیوان.
قهرمان: گاری چوبی بزرگ با یک چرخ بزرگ، کپهٔ سه گونی، دستهٔ بلند؛ ≈۶۰٪ عرض سکو، وسط.
طرح قطعه‌به‌قطعه (واحد symbol، زمین y=8، xf=(0.92,dx,2)):
 ۱ سایهٔ تماس زیر چرخ و پایهٔ عقب.
 لایهٔ متحرک node_cart_station_roll (کل گاری؛ پایان = جای ایستا):
 ۲ دستهٔ بلند: متوازی‌الاضلاع ۱۳ پهن، از دیوارهٔ راست جعبه (14,-34) تا (66,-66)، چوب روشن.
 ۳ پایهٔ عقب: بلوک چوبی تیره ۱۴ پهن زیر انتهای چپ جعبه تا زمین (گاری نیفتد).
 ۴ سه گونی (سفید-لاجوردی #f4f7ff/#cfd8ee، گرهٔ قرمز #e0553a با دور INNER): دو گونی پایین کنار هم و یکی روی آن‌ها، هم‌پوشان با لبهٔ جعبه.
 ۵ جعبهٔ چوبی x -66..16، y -44..-14 (قرمز-قهوه‌ای #a14a2a، نوار روشن #cf7a4c، شیار تیره، دو تیرک).
 ۶ چرخ بزرگ r=24 مرکز (-26,-16): لبهٔ آبی #6f8fe8 (PART)، داخل کرم، ۶ پره، توپی تیره.
 چرخ داخل گروه تودرتوی node_cart_station_roll_wheel است."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/cart_station'

W_B, W_L, W_D, W_H = '#a14a2a', '#cf7a4c', '#6a2c16', '#f0a878'
WHL, WHD = '#6f8fe8', '#2f3f8f'; CREAM = '#fbeee0'
SK, SK_D = '#f4f7ff', '#cfd8ee'; RED = '#e0553a'
G = 8
R = 22
W1 = (-30, -14, R)
SLIDE = -5


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def wheel(p, gid, w, nsp=6):
    cx, cy, Rr = w; ri = Rr - 5.8
    p.raw('<g id="%s">' % gid)
    p.shape(ell(cx, cy, Rr, Rr, 0, 360, 40), WHL, PART, j=.05, step=99, clip=False)
    a, b = p.X((cx, cy)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, ri, CREAM))
    for k in range(nsp):
        t = math.radians(30 + k * 360 / nsp)
        p.ln((cx, cy), (cx + ri * math.cos(t), cy + ri * math.sin(t)), INNER, WHD, j=0)
    disc(p, cx, cy, 5, WHD)
    p.raw('</g>')


def sack(p, cx, yb, w=26, h=30):
    """گونی: بدنهٔ بالشی، گردن باریک بالا با گرهٔ قرمز."""
    hw = w / 2; yt = yb - h
    pts = [(cx - hw + 3, yb), (cx - hw, yb - 8), (cx - hw + 1, yb - 17), (cx - 9, yt + 5), (cx - 6, yt), (cx + 6, yt), (cx + 9, yt + 5), (cx + hw - 1, yb - 17), (cx + hw, yb - 8), (cx + hw - 3, yb)]
    p.shape(pts, SK, PART, j=.05, step=6, clip=False)
    poly(p, [(cx + 4, yb - 3), (cx + hw - 3.5, yb - 3), (cx + hw - 3.5, yb - 16), (cx + 9, yb - 21), (cx + 4, yb - 21)], SK_D)
    poly(p, [(cx - 6, yt + 9), (cx + 6, yt + 9), (cx + 6, yt + 13), (cx - 6, yt + 13)], RED)


def build(out=OUTD):
    p = Pen('cart_station', 'farm'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (0.92, 4, 2)
    p.tipshadow(W1[0] + 2, G - 1, 26); p.foot_tip(W1[0] + 2, G - 1, 20)
    p.tipshadow(-56, G - 1, 10)
    with layer(p, 'roll'):
        a0, a1 = (12, -34), (64, -64)
        dx, dy = a1[0] - a0[0], a1[1] - a0[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy * 6.5, ux * 6.5
        sh = [(a0[0] + nx, a0[1] + ny), (a1[0] + nx, a1[1] + ny), (a1[0] - nx, a1[1] - ny), (a0[0] - nx, a0[1] - ny)]
        p.shape(sh, W_L, PART, j=.1, step=8, clip=False)
        k0, k1, o = 14, L - 6, .55
        poly(p, [(a0[0] + ux * k0 + nx * o, a0[1] + uy * k0 + ny * o), (a0[0] + ux * k1 + nx * o, a0[1] + uy * k1 + ny * o),
                 (a0[0] + ux * k1 + nx * .2, a0[1] + uy * k1 + ny * .2), (a0[0] + ux * k0 + nx * .2, a0[1] + uy * k0 + ny * .2)], W_H)
        leg = [(-62, -20), (-48, -20), (-48, G - 2), (-62, G - 2)]
        p.shape(leg, W_D, PART, j=.1, step=6, clip=False)
        sack(p, -50, -38, 34, 28); sack(p, -16, -38, 34, 28); sack(p, -33, -56, 34, 28)
        box = [(-66, -44), (16, -44), (16, -14), (-66, -14)]
        p.shape(box, W_B, PART, j=.1, step=8, clip=False)
        for y in (-32.5, -23.5): p.ln((-62, y), (12, y), INNER, W_D, j=0)
        poly(p, [(-62, -41), (12, -41), (12, -38), (-62, -38)], W_L)
        for x in (-63, 13): poly(p, [(x - 1.5, -41), (x + 1.5, -41), (x + 1.5, -17), (x - 1.5, -17)], W_D)
        p.stroke(box, PART, j=.1, step=8)
        wheel(p, 'node_cart_station_roll_wheel', W1)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    mo = {'roll': dict(offsets=[(SLIDE * i / 6, 0) for i in range(7)])}
    r = finish(p, 'cart_station', STAND, motion=mo, out=OUTD, shots=SHOTS)
    sp = r['spec']; hub = [round(v, 1) for v in p.X(W1[:2])]
    sp['motion_spec'] = {'node_cart_station_roll': dict(kind='translate', dx_from=SLIDE, dx_to=0, dur_s=1.8, count=1, ease='ease-out',
                         note='کل گاری از ۵ واحد چپ می‌غلتد و در جای ایستا می‌ایستد؛ حالت ایستا = پایان؛ بدون حلقهٔ بیکار.'),
                         'node_cart_station_roll_wheel': dict(kind='rotate', about=hub, deg_from=-round(5 / W1[2] * 57.3), deg_to=0, note='چرخ بزرگ؛ ساعت‌گرد؛ هم‌زمان با غلتیدن'),
                         'reduced_motion': 'ایستا'}
    (OUTD / 'cart_station.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
