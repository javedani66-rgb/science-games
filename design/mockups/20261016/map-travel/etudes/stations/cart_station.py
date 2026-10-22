#!/usr/bin/env python3
"""ایستگاه E02 «ایستگاه گاری‌ها» (سرزمین مزرعه، سکوی farm ۵۰°) — دور ۶ (R6).
گاری دستی چوبی ¾ (نه نمای کنار تخت): جعبهٔ دو‌پله با رویهٔ باز، دو چرخ بزرگ حجم‌دار چوب‌پره‌دار (چرخ نزدیک + چرخ دور)، دستهٔ بلند مورب، سه گونی.
طرح (واحد symbol؛ زمین y≈10):
 ۱) چرخ دور (تیره‌تر) مرکز (-8,-27) r=26، پشت جعبه.
 ۲) پایهٔ چپ: بلوک چوبی تیره.
 ۳) جعبه: رویهٔ باز تیره (متوازی‌الاضلاع)، سه گونی (کرم #f4f7ff، سایهٔ #cfd8ee، گرهٔ قرمز)، وجههٔ جلو (#a8512c با نوار روشن #cf7a4c و دو شیار)، وجههٔ راست تیره (#6a2c16) x 34..46.
 ۴) دسته: از وجههٔ راست (46,-34) تا (96,-72)، ۱۳ پهن، روشن/تیره.
 ۵) چرخ نزدیک مرکز (-22,-16) r=26: لبهٔ آبی-خاکستری تیره‌پشت (ضخامت)، رویه کرم، ۸ پره، توپی.
لایه‌های متحرک جدا: node_cart_station_wheel_near و node_cart_station_wheel_far (هر چرخ حول مرکز خودش). ایستا = پایان؛ بدون حلقهٔ بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from station_kit import *
from g4_helpers import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/cart_station'

W_B, W_L, W_D = '#a8512c', '#d4824f', '#6a2c16'
H_B, H_L, H_D = '#d9a05a', '#f0c88a', '#a56a2a'
WHB, WHT = '#4f6fb5', '#2c3f7c'          # لبهٔ چرخ و ضخامتش
CREAM, CREAM_D = '#fbeee0', '#e6cfae'
SK, SK_D = '#f4f7ff', '#c4cfe8'; RED = '#e0402e'; INTR = '#4a2210'
G = 10


def sack(p, cx, yb, w=30, h=30):
    hw = w / 2; yt = yb - h
    pts = [(cx - hw + 3, yb), (cx - hw, yb - 8), (cx - hw + 1, yb - 18), (cx - 9, yt + 6), (cx - 6, yt), (cx + 6, yt), (cx + 9, yt + 6), (cx + hw - 1, yb - 18), (cx + hw, yb - 8), (cx + hw - 3, yb)]
    p.shape(pts, SK, PART, j=.05, step=99, clip=False)
    poly(p, [(cx + 4, yb - 3), (cx + hw - 3.5, yb - 3), (cx + hw - 3.5, yb - 17), (cx + 9, yb - 22), (cx + 4, yb - 22)], SK_D)
    poly(p, [(cx - 6.5, yt + 10), (cx + 6.5, yt + 10), (cx + 6.5, yt + 14.5), (cx - 6.5, yt + 14.5)], RED)


def wheel(p, gid, cx, cy, R, front=True):
    ri = R - 7
    p.shape(ell(cx, cy, R, R, 0, 360, 40), WHB if front else WHT, PART, j=.05, step=99, clip=False)
    if front: p.fill(ell(cx, cy, R - 1.5, R - 1.5, 200, 250, 8), '#8fb0f0')
    a, b = p.X((cx, cy)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, ri * p.xf[0], CREAM if front else CREAM_D))
    for k in range(8):
        t = math.radians(22.5 + k * 45)
        p.ln((cx, cy), (cx + ri * math.cos(t), cy + ri * math.sin(t)), INNER, INTR, j=0)
    disc(p, cx, cy, 6.5, INTR); disc(p, cx, cy, 2.6, '#ffd84d')


def build(out=OUTD, rot=0):
    p = Pen('cart_station', 'farm'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (0.98, -7, 6)
    p.tipshadow(-22, G, 34); p.foot_tip(-20, G - 1, 26); p.tipshadow(30, G - 1, 12)
    NX, NY, FX, FY, R = -24, -16, 16, -24, 24
    with layer(p, 'wheel_far'):
        wheel(p, None, FX, FY, R, front=False)
    # پایه
    sharp(p, rect(-56, -30, -42, G - 1), W_D, PART)
    # جعبه
    top = [(-54, -48), (30, -48), (44, -60), (-40, -60)]
    sharp(p, top, INTR, PART)
    sack(p, -34, -53, 30, 28); sack(p, -2, -53, 30, 28); sack(p, -18, -70, 30, 28)
    front = rect(-54, -48, 30, -20)
    sharp(p, front, W_B, PART)
    poly(p, rect(-51, -45, 27, -41), W_L)
    for y in (-34, -27): p.ln((-51, y), (27, y), INNER, W_D, j=0)
    poly(p, rect(19, -39, 27, -23), W_D, .55)
    sharp(p, [(30, -48), (44, -60), (44, -32), (30, -20)], W_D, PART)
    poly(p, [(33, -45), (41, -54), (41, -48), (33, -39)], W_B, .8)
    # دسته
    a0, a1 = (42, -50), (86, -74)
    dx, dy = a1[0] - a0[0], a1[1] - a0[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy * 8, ux * 8
    sh = [(a0[0] + nx, a0[1] + ny), (a1[0] + nx, a1[1] + ny), (a1[0] - nx, a1[1] - ny), (a0[0] - nx, a0[1] - ny)]
    sharp(p, sh, H_B, PART)
    poly(p, [(a0[0] + ux * 10 + nx * .6, a0[1] + uy * 10 + ny * .6), (a1[0] - ux * 6 + nx * .6, a1[1] - uy * 6 + ny * .6), (a1[0] - ux * 6 + nx * .1, a1[1] - uy * 6 + ny * .1), (a0[0] + ux * 10 + nx * .1, a0[1] + uy * 10 + ny * .1)], H_L)
    poly(p, [(a0[0] + ux * 10 - nx * .1, a0[1] + uy * 10 - ny * .1), (a1[0] - ux * 6 - nx * .1, a1[1] - uy * 6 - ny * .1), (a1[0] - ux * 6 - nx * .6, a1[1] - uy * 6 - ny * .6), (a0[0] + ux * 10 - nx * .6, a0[1] + uy * 10 - ny * .6)], H_D)
    # چرخ نزدیک
    with layer(p, 'wheel_near'):
        wheel(p, None, NX, NY, R, front=True)
    return p


STAND = None
NX, NY, FX, FY, R = -24, -16, 16, -24, 24
if __name__ == '__main__':
    p = build()
    r = finish(p, 'cart_station', STAND, motion={'wheel_near': dict(offsets=[(0, 0)]), 'wheel_far': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_cart_station_wheel_near': dict(kind='rotate', about=[round(v, 1) for v in p.X((NX, NY))], deg_from=-90, deg_to=0, dur_s=1.6, ease='ease-out', count=1),
                         'node_cart_station_wheel_far': dict(kind='rotate', about=[round(v, 1) for v in p.X((FX, FY))], deg_from=-90, deg_to=0, dur_s=1.6, ease='ease-out', count=1),
                         'note': 'هر دو چرخ هم‌زمان ۹۰° ساعت‌گرد می‌چرخند و می‌ایستند (پره‌ها ۸تایی؛ حالت ایستا = پایان)؛ بدون حلقهٔ بیکار.', 'reduced_motion': 'ایستا'}
    (OUTD / 'cart_station.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
