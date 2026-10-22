#!/usr/bin/env python3
"""ایستگاه E02 «ایستگاه گاری‌ها» (سرزمین مزرعه، پالت farm). نمای کنار، بدون حیوان. (دور سوم بازطراحی؛ مختصات نهایی، xf=یک)
طرح قطعه‌به‌قطعه (واحد symbol، y منفی = بالا، زمین y=8):
 ۱ سایهٔ تماس زیر دو چرخ (ایستا)
 لایهٔ متحرک node_cart_station_roll (کل گاری؛ پایان = جای ایستا):
 ۲ دستهٔ بلند: متوازی‌الاضلاع ۱۳ پهن، از دیوارهٔ راست جعبه (-14,-42) رو به بالا-راست تا (40,-68)؛ ≈۴۸ بیرون از جعبه، شیب ≈۲۶°.
   عمداً بالا: نوکش بالای لبهٔ سکوست تا سایهٔ راست سکو روی آن نیفتد. چوب روشن.
 ۳ گونی (پیش از جعبه کشیده می‌شود): کف y=-40، لبهٔ بالای جعبه y=-46 ⇒ ۶ واحد فرو رفته.
 ۴ جعبهٔ چوبی x -76..-4، y -46..-18 (قرمزتر و تیره‌تر از سکو: رنگ‌مایهٔ ≈۱۶° در برابر ۵۰°)، دو شیار، نوار روشن، دو تیرک تیره.
 ۵ دو چرخ هم‌اندازه: مراکز (-58,-9) و (-18,-9)، شعاع ۱۷ (قطر ۳۴)، ۶ پره؛ لبهٔ آبی، داخل کرم، توپی تیره؛ بدون نقطهٔ زرد.
 چرخ‌ها داخل گروه‌های تودرتوی node_cart_station_roll_wheel و ..._wheel2 هستند."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/cart_station'

W_B, W_L, W_D, W_H = '#a14a2a', '#cf7a4c', '#6a2c16', '#f0a878'
WHL, WHD = '#6f8fe8', '#2f3f8f'; CREAM = '#fbeee0'
SK, SK_D = '#f4f7ff', '#cfd8ee'; BLUE = '#5f86d9'
G = 8
R = 17
W1 = (-52, -9, R)
W2 = (-14, -9, R)
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
    disc(p, cx, cy, 4.5, WHD)
    p.raw('</g>')


def build(out=OUTD):
    p = Pen('cart_station', 'farm'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (0.88, -4, 2)
    for (cx, cy, Rr) in (W1, W2):
        p.tipshadow(cx + 3, G - 1, Rr + 4); p.foot_tip(cx + 2, G - 1, Rr * .6)
    with layer(p, 'roll'):
        # دستهٔ بلند (از دیوارهٔ راست جعبه، رو به بالا-راست)
        a0, a1 = (-12, -42), (36, -70)
        dx, dy = a1[0] - a0[0], a1[1] - a0[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy * 6.5, ux * 6.5
        sh = [(a0[0] + nx, a0[1] + ny), (a1[0] + nx, a1[1] + ny), (a1[0] - nx, a1[1] - ny), (a0[0] - nx, a0[1] - ny)]
        p.shape(sh, W_L, PART, j=.1, step=8, clip=False)
        k0, k1, o = 14, L - 6, .55
        poly(p, [(a0[0] + ux * k0 + nx * o, a0[1] + uy * k0 + ny * o), (a0[0] + ux * k1 + nx * o, a0[1] + uy * k1 + ny * o),
                 (a0[0] + ux * k1 + nx * .2, a0[1] + uy * k1 + ny * .2), (a0[0] + ux * k0 + nx * .2, a0[1] + uy * k0 + ny * .2)], W_H)
        # گونی (کفش y=-40، زیر لبهٔ جعبه)
        sack = [(-54, -40), (-55, -53), (-50, -62), (-43, -67), (-41, -72), (-32, -72), (-30, -67), (-23, -62), (-18, -53), (-19, -40)]
        p.shape(sack, SK, PART, j=.1, step=6, clip=False)
        poly(p, [(-27.5, -43), (-22, -43), (-22, -53), (-25.5, -58.5), (-27.5, -58.5)], SK_D)
        poly(p, [(-51.5, -45), (-48.5, -45), (-48.5, -56), (-51.5, -54)], '#ffffff')
        poly(p, [(-42.5, -68.5), (-30.5, -68.5), (-30.5, -65.5), (-42.5, -65.5)], BLUE)
        # جعبهٔ چوبی
        box = [(-68, -46), (-4, -46), (-4, -18), (-68, -18)]
        p.shape(box, W_B, PART, j=.1, step=8, clip=False)
        for y in (-35.5, -26.5): p.ln((-64, y), (-8, y), INNER, W_D, j=0)
        poly(p, [(-64, -43), (-8, -43), (-8, -40), (-64, -40)], W_L)
        for x in (-65, -7): poly(p, [(x - 1.5, -43), (x + 1.5, -43), (x + 1.5, -21), (x - 1.5, -21)], W_D)
        p.stroke(box, PART, j=.1, step=8)
        wheel(p, 'node_cart_station_roll_wheel', W1)
        wheel(p, 'node_cart_station_roll_wheel2', W2)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    mo = {'roll': dict(offsets=[(SLIDE * i / 6, 0) for i in range(7)])}
    r = finish(p, 'cart_station', STAND, motion=mo, out=OUTD, shots=SHOTS)
    sp = r['spec']; hub = [round(v, 1) for v in p.X(W1[:2])]; hub2 = [round(v, 1) for v in p.X(W2[:2])]
    sp['motion_spec'] = {'node_cart_station_roll': dict(kind='translate', dx_from=SLIDE, dx_to=0, dur_s=1.8, count=1, ease='ease-out',
                         note='کل گاری از ۵ واحد (≈۴px) چپ می‌غلتد و در جای ایستا می‌ایستد؛ حالت ایستا = پایان؛ بدون حلقهٔ بیکار.'),
                         'node_cart_station_roll_wheel': dict(kind='rotate', about=hub, deg_from=-round(5 / W1[2] * 57.3), deg_to=0, note='چرخ عقب؛ ساعت‌گرد؛ هم‌زمان با غلتیدن'),
                         'node_cart_station_roll_wheel2': dict(kind='rotate', about=hub2, deg_from=-round(5 / W2[2] * 57.3), deg_to=0, note='چرخ جلو (هم‌اندازهٔ چرخ عقب)'),
                         'reduced_motion': 'ایستا'}
    (OUTD / 'cart_station.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
