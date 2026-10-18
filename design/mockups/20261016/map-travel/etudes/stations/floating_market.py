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
XF = (1.0, 7.0, -11.0)            # قاب قهرمان: (مقیاس هندسه، dx، dy) در واحد symbol؛ ضخامت خط ثابت می‌ماند
HULL = '#c98a4a'; HULL_D = '#8a5a2a'; RED = '#ef6a4a'; WH = '#fff8e0'; WOOD = '#ffd84d'
ORG = '#ff9b2f'; GRN = '#8bd45a'; YEL = '#ffe14d'; BASKET = '#b8742f'; BASKET_D = '#7a4a1c'
BOB = 3
X0, X1 = -52, 0                 # عرض غرفه


def flat(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def fruit(p, x, y, r, c):
    mx, my = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (mx, my, r * p.xf[0], c))


def boat(p):
    """D122: غرفهٔ بلند و درشت روی بلم: بدنه، پیشخوان، دو ستون بلند، سایبان راه‌راه بزرگ، پرچم، سبد و جعبه‌های میوه؛ از بالای سکو بالا می‌زند."""
    W = X1 - X0
    p.shape([(X0 - 5, 12), (X0 + 4, 16), (X1 - 4, 16), (X1 + 5, 12), (X1 - 2, 32), (X0 + 4, 32)], HULL, PART, j=.25, step=4)
    p.ln((X0 + 10, 24), (X1 - 8, 24), INNER, HULL_D, j=.1, probe='خط داخلی (تختهٔ قایق)')
    for x in (X0 + 6, X1 - 6):                                     # ستون‌های بلند سایبان
        flat(p, [(x - 3, 10), (x + 3, 10), (x + 3, -47), (x - 3, -47)], HULL_D)
    # پیشخوان چوبی
    p.shape([(X0 + 2, -4), (X1 - 2, -4), (X1 - 2, 8), (X0 + 2, 8)], WOOD, PART, j=.2, step=6)
        # سایبان راه‌راه بزرگ: شش نوار + خط دور
    n = 6; w = (W + 10) / n; ax = X0 - 5; y0, y1 = -45, -68
    for i in range(n):
        flat(p, [(ax + i * w, y0), (ax + (i + 1) * w, y0), (ax + (i + 1) * w - 3, y1), (ax + i * w + 3, y1)], RED if i % 2 == 0 else WH)
    p.stroke([(ax, y0), (ax + n * w, y0), (ax + n * w - 3, y1), (ax + 3, y1)], INNER, j=.2, step=4)
    c = ax + 2.5 * w                                                 # پرچم
    flat(p, [(c - 2.2, y1), (c + 2.2, y1), (c + 2.2, y1 - 12), (c - 2.2, y1 - 12)], NAVY)
    flat(p, [(c + 2.2, y1 - 18), (c + 14, y1 - 10), (c + 2.2, y1 - 4)], ORG)
    # دو سبد بزرگ روی پیشخوان، پر از میوه
    for bx0, bx1 in ((X0 + 5, X0 + 27), (X0 + 29, X1 - 5)):
        flat(p, [(bx0, -14), (bx1, -14), (bx1 - 3, -5), (bx0 + 3, -5)], BASKET)
        p.ln((bx0 + 5, -9.5), (bx1 - 5, -9.5), INNER, BASKET_D, j=.1)
    for x, y, r, col in ((X0 + 11, -20, 7, RED), (X0 + 22, -19, 6, ORG), (X0 + 16, -26, 6, YEL),
                         (X0 + 35, -20, 6.5, GRN), (X1 - 11, -19, 6, YEL), (X0 + 42, -26, 5.5, RED)):
        fruit(p, x, y, r, col)


def build(out=OUTD):
    p = Pen('floating_market', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-26, 30, 32); p.foot_tip(-26, 22, 14)
    with layer(p, 'boat'): boat(p)
    return p


STAND = None     # خودکار: find_stand

if __name__ == '__main__':
    p = build()
    offs = [p.V(o) for o in [(0, -BOB), (0, 0), (0, BOB)]]
    r = finish(p, 'floating_market', STAND, motion={'boat': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(offsets=offs, note='کل قایق و غرفه روی موج بالا و پایین؛ سکو ثابت؛ سایهٔ تماس ثابت')
    (OUTD / 'floating_market.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
