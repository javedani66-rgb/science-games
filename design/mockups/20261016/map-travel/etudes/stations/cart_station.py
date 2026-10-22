#!/usr/bin/env python3
"""ایستگاه E02 «ایستگاه گاری‌ها» (سرزمین مزرعه، پالت farm). نمای کنار، بدون حیوان.
طرح قطعه‌به‌قطعه (واحد symbol، y منفی = بالا، زمین y=8):
 ۱ سایهٔ تماس چرخ و سر دسته (بیرون از لایهٔ متحرک، ایستا)
 لایهٔ متحرک node_cart_station_roll (کل گاری؛ پایان = جای ایستا):
 ۲ دستهٔ بلند (شافت): متوازی‌الاضلاع ۱۳ پهن، از زیر تختهٔ بار (x=-26) رو به راست-پایین تا زمین (x=24)؛ چوب روشن #d9784a
 ۳ تختهٔ بار: x -80..-14، y -31..-19، چوب سرخ #b8572f، روشن #d9784a، تیره #7f3a1f
 ۴ دیوارهٔ عقب: x -80..-70، y -48..-19 (هم‌پوشان با تخته)
 ۵ گونی سفید-آبی #f4f7ff با بند #6f8fe8
 ۶ چرخ بلند: مرکز (-44,-16) شعاع ۲۴؛ لبه #6e2f1b، داخل کرم #fbeee0، ۸ پره، توپی زرد، میخ زرد روی لبه (تا چرخش دیده شود)
 چرخ داخل گروه تو‌در‌توی node_cart_station_roll_wheel است.
رنگ قهرمان رنگ‌مایهٔ ≈۱۵° در برابر سکوی مزرعه ۵۰°."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/cart_station'

W_B, W_L, W_D = '#b77a3a', '#d29255', '#7a4a1f'
WHL, WHD = '#6f8fe8', '#2f3f8f'; CREAM = '#fbeee0'; YEL = '#ffd84d'
SK, SK_D, BLUE = '#f4f7ff', '#cfd8ee', '#5f86d9'
G = 8
W1 = (-60, -11, 19)      # چرخ بزرگ عقب (x, y, شعاع)
W2 = (-22, -6, 14)      # چرخ کوچک‌تر جلو
POLE0, POLE1 = (-22, -6), (14, 4)
SLIDE = -5


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def wheel(p, gid, w, nsp):
    cx, cy, R = w; ri = R - 5.8
    p.raw('<g id="%s">' % gid)
    p.shape(ell(cx, cy, R, R, 0, 360, 40), WHL, PART, j=.05, step=99, clip=False)
    a, b = p.X((cx, cy)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, ri, CREAM))
    for k in range(nsp):
        t = math.radians(k * 360 / nsp + 10)
        p.ln((cx, cy), (cx + ri * math.cos(t), cy + ri * math.sin(t)), INNER, WHD, j=0)
    disc(p, cx, cy, 4.5, WHD); disc(p, cx, cy, 2, YEL)
    t = math.radians(10 + 180 / nsp + 0)
    disc(p, cx + ri * .62 * math.cos(t), cy + ri * .62 * math.sin(t), 1.9, YEL)
    p.raw('</g>')


def build(out=OUTD):
    p = Pen('cart_station', 'farm'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.0, 11, 0)
    for (cx, cy, R) in (W1, W2):
        p.tipshadow(cx + 3, G - 1, R + 4); p.foot_tip(cx + 2, G - 1, R * .6)
    p.tipshadow(POLE1[0] + 1, POLE1[1] + 3, 7)
    with layer(p, 'roll'):
        # میلهٔ جلو (کم‌شیب، از محور چرخ جلو تا زمین)
        dx, dy = POLE1[0] - POLE0[0], POLE1[1] - POLE0[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy * 6.5, ux * 6.5
        sh = [(POLE0[0] + nx, POLE0[1] + ny), (POLE1[0] + nx, POLE1[1] + ny), (POLE1[0] - nx, POLE1[1] - ny), (POLE0[0] - nx, POLE0[1] - ny)]
        p.shape(sh, W_L, PART, j=.1, step=8, clip=False)
        poly(p, [(POLE0[0] + 10 * ux + nx * .2, POLE0[1] + 10 * uy + ny * .2), (POLE1[0] - 3 * ux + nx * .2, POLE1[1] - 3 * uy + ny * .2),
                 (POLE1[0] - 3 * ux + nx * .5, POLE1[1] - 3 * uy + ny * .5), (POLE0[0] + 10 * ux + nx * .5, POLE0[1] + 10 * uy + ny * .5)], '#f2b583')
        # جعبهٔ بار با کناره‌های تخته‌ای
        box = [(-72, -48), (-10, -48), (-10, -22), (-72, -22)]
        p.shape(box, W_B, PART, j=.1, step=8, clip=False)
        for y in (-40.5, -32.5): p.ln((-68, y), (-14, y), INNER, W_D, j=0)
        poly(p, [(-68, -45.5), (-14, -45.5), (-14, -42.5), (-68, -42.5)], W_L)
        for x in (-69, -13): poly(p, [(x - 2, -46), (x + 2, -46), (x + 2, -25), (x - 2, -25)], W_D)
        p.stroke(box, PART, j=.1, step=8)
        # گونی با گردن گره‌خورده
        sack = [(-62, -48), (-63, -61), (-58, -70), (-51, -75), (-49, -80), (-39, -80), (-37, -75), (-32, -70), (-27, -61), (-28, -48)]
        p.shape(sack, SK, PART, j=.1, step=6, clip=False)
        poly(p, [(-36, -73), (-31, -69), (-27.5, -61), (-28.5, -50), (-36, -50)], SK_D)
        poly(p, [(-59, -66), (-56.5, -68), (-56.5, -52), (-59, -52)], '#ffffff')
        poly(p, [(-50.5, -78), (-37.5, -78), (-37.5, -74.5), (-50.5, -74.5)], BLUE)
        p.shape([(-50, -80.5), (-38, -80.5), (-33.5, -90), (-44, -84.5), (-54.5, -90)], SK, INNER, j=.1, step=99, clip=False)
        wheel(p, 'node_cart_station_roll_wheel', W1, 8)
        wheel(p, 'node_cart_station_roll_wheel2', W2, 5)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    mo = {'roll': dict(offsets=[(SLIDE * i / 6, 0) for i in range(7)])}
    r = finish(p, 'cart_station', STAND, motion=mo, out=OUTD, shots=SHOTS)
    sp = r['spec']; hub = [round(v, 1) for v in p.X(W1[:2])]; hub2 = [round(v, 1) for v in p.X(W2[:2])]
    sp['motion_spec'] = {'node_cart_station_roll': dict(kind='translate', dx_from=SLIDE, dx_to=0, dur_s=1.8, count=1, ease='ease-out',
                         note='کل گاری از ۵ واحد (≈۴px) چپ می‌غلتد و در جای ایستا می‌ایستد؛ حالت ایستا = پایان؛ بدون حلقهٔ بیکار.'),
                         'node_cart_station_roll_wheel': dict(kind='rotate', about=hub, deg_from=-round(5 / W1[2] * 57.3), deg_to=0, note='چرخ بزرگ عقب؛ ساعت‌گرد؛ هم‌زمان با غلتیدن'),
                         'node_cart_station_roll_wheel2': dict(kind='rotate', about=hub2, deg_from=-round(5 / W2[2] * 57.3), deg_to=0, note='چرخ کوچک جلو'),
                         'reduced_motion': 'ایستا'}
    (OUTD / 'cart_station.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
