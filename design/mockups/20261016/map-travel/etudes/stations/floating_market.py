#!/usr/bin/env python3
"""ایستگاه «بازارچهٔ شناور» (E06): قهرمان = یک غرفهٔ بازار روی یک قایق (سایبان راه‌راه، پیشخوان، میوه، پرچم)، سکوی دریایی.
بازطراحی ۱۸ اکتبر: بلم کوچک با غرفهٔ سایه‌بان‌دار (سایبان راه‌راه، سبد میوهٔ درهم، جعبه‌ها، پرچم)؛ کل قهرمان با حاشیهٔ ≥۴px درون رویهٔ سکو.
لایهٔ متحرک node_floating_market_boat = کل قایق و غرفه که روی موج بالا و پایین می‌رود (dy در -3..+3)؛ زیرش سکوی دریایی (ثابت و کامل) است.
طراحی دوباره برای خط ضخیم‌تر (D113، D110): یک قایق، یک غرفه با سایبان سه‌نواری؛ نوارها و میوه‌ها فقط رنگ تخت (بدون خط دور)."""
import sys, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
from station_kit import _shot, _poly
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit2/after/floating_market'
XF = (0.85, 7.0, 3.0)            # قاب قهرمان: (مقیاس هندسه، dx، dy) در واحد symbol؛ ضخامت خط ثابت می‌ماند
HULL = '#c98a4a'; HULL_D = '#8a5a2a'; RED = '#ef6a4a'; WH = '#fff8e0'; WOOD = '#ffd84d'
ORG = '#ff9b2f'; GRN = '#8bd45a'; YEL = '#ffe14d'; BASKET = '#b8742f'; BASKET_D = '#7a4a1c'
BOB = 3
X0, X1 = -56, 0                 # عرض غرفه


def flat(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def fruit(p, x, y, r, c):
    mx, my = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (mx, my, r * p.xf[0], c))


def boat(p):
    """بلم کوچک با غرفهٔ سایه‌بان‌دار: بدنهٔ قایق، دو ستون، سایبان راه‌راه، پرچم؛ سبد پر از میوهٔ درهم و نامساوی و دو جعبهٔ کج‌چین."""
    p.shape([(X0 - 6, 4), (X0 + 4, 8), (X1 - 4, 8), (X1 + 6, 4), (X1 - 2, 20), (X0 + 4, 20)], HULL, PART, j=.25, step=4)
    p.ln((X0 + 12, 14.5), (X1 - 10, 14.5), INNER, HULL_D, j=.1, probe='خط داخلی (تختهٔ قایق)')
    for x in (X0 + 4, X1 - 4):                                     # ستون‌های سایبان
        flat(p, [(x - 2.5, 6), (x + 2.5, 6), (x + 2.5, -9), (x - 2.5, -9)], HULL_D)
    # سایبان راه‌راه: شش نوار قرمز/کرم + یک خط دور (INNER)
    n = 6; w = (X1 - X0 + 14) / n; ax = X0 - 7; y0, y1 = -9, -23
    for i in range(n):
        flat(p, [(ax + i * w, y0), (ax + (i + 1) * w, y0), (ax + (i + 1) * w - 2, y1), (ax + i * w + 2, y1)], RED if i % 2 == 0 else WH)
    p.stroke([(ax, y0), (ax + n * w, y0), (ax + n * w - 2, y1), (ax + 2, y1)], INNER, j=.2, step=4)
    c = ax + 4.5 * w                                                 # پرچم کوچک روی نوار پنجم
    flat(p, [(c - 1.8, y1), (c + 1.8, y1), (c + 1.8, y1 - 8), (c - 1.8, y1 - 8)], NAVY)
    flat(p, [(c + 1.8, y1 - 9), (c + 12, y1 - 5.5), (c + 1.8, y1 - 2)], ORG)
    # سبد (چپ) با توده‌ای از میوه: اندازه و رنگ متفاوت، روی‌هم‌افتاده
    flat(p, [(X0 + 6, 2), (X0 + 38, 2), (X0 + 35, 9), (X0 + 9, 9)], BASKET)
    p.ln((X0 + 10, 5.5), (X0 + 34, 5.5), INNER, BASKET_D, j=.1)
    for x, y, r, col in ((X0 + 15, -3, 6.2, RED), (X0 + 28, -2, 5.2, ORG), (X0 + 21, -5, 4.8, YEL), (X0 + 33, -4, 3.4, GRN), (X0 + 10, -4, 3.6, ORG), (X0 + 23, 2, 3.4, GRN)):
        fruit(p, x, y, r, col)
    # دو جعبهٔ کج‌چین (راست) با میوه
    flat(p, [(X0 + 41, 0), (X1 - 3, 0), (X1 - 3, 9), (X0 + 41, 9)], WOOD)
    flat(p, [(X0 + 41, 6), (X1 - 3, 6), (X1 - 3, 9), (X0 + 41, 9)], HULL_D)
    flat(p, [(X0 + 45, -6.5), (X1 - 10, -6.5), (X1 - 10, 0), (X0 + 45, 0)], '#f0c23a')
    for x, y, r, col in ((X0 + 49, -7.5, 3.4, GRN), (X0 + 54, -8, 2.8, RED), (X1 - 14.5, -7.5, 2.6, YEL)):
        fruit(p, x, y, r, col)


def build(out=OUTD):
    p = Pen('floating_market', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-30, 20, 30); p.foot_tip(-30, 12, 12)
    with layer(p, 'boat'): boat(p)
    return p


STAND = None     # خودکار: find_stand

if __name__ == '__main__':
    p = build()
    offs = [p.V(o) for o in [(0, -BOB), (0, 0), (0, BOB)]]
    r = finish(p, 'floating_market', STAND, motion={'boat': dict(offsets=offs)}, out=OUTD, shots=SHOTS, strict=True)
    sp = r['spec']; sp['motion_spec'] = dict(offsets=offs, note='کل قایق و غرفه روی موج بالا و پایین؛ سکو ثابت؛ سایهٔ تماس ثابت')
    (OUTD / 'floating_market.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
