#!/usr/bin/env python3
"""ایستگاه «بازارچهٔ شناور» (E06؛ بازطراحی ۱۸ اکتبر شب، D123): قهرمان = بلمِ بازار، درشت و پرجزئیات، روی سکوی دریایی:
بدنهٔ بلم با لبهٔ روشن و تخته‌ها، غرفه با پیشخوان و سه سبد پر از میوه، سایبان راه‌راه با لبهٔ دندانه‌دار، دکل بلند با پرچم و
ریسمان فانوس‌ها که از بالای فیگور رد می‌شود (آزاد از بالا)؛ پایهٔ بلم سمت چپ می‌ماند.
لایهٔ متحرک node_floating_market_boat = کل بلم و غرفه و دکل که روی موج بالا و پایین می‌رود (dy در -3..+3)؛ سکو ثابت است.
نوارها و میوه‌ها و فانوس‌ها رنگ تخت (بدون خط دور) تا خط ضخیم آن‌ها را نبلعد (D110)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import station_kit
from station_kit import *
from functools import partial
station_kit.margin_check = partial(station_kit.margin_check, min_margin=4)   # D123: حاشیهٔ چپ/راست ≥۴px
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/v2/floating_market'
XF = (1.0, 0.0, -20.0)
HULL = '#c98a4a'; HULL_L = '#e8b070'; HULL_D = '#8a5a2a'; RED = '#ef6a4a'; RED_D = '#c24a30'; WH = '#fff8e0'; WOOD = '#ffd84d'; WOOD_D = '#d9a020'
ORG = '#ff9b2f'; GRN = '#8bd45a'; GRN_D = '#4f9a2f'; YEL = '#ffe14d'; BASKET = '#b8742f'; BASKET_D = '#7a4a1c'; PURP = '#b06ad6'
BOB = 3
X0, X1 = -58, 9          # طول بلم


def flat(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def rect(p, x0, y0, x1, y1, col): flat(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col)


def disc(p, x, y, r, col):
    mx, my = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (mx, my, r * p.xf[0], col))


def fruit(p, x, y, r, c):
    disc(p, x, y, r, c); disc(p, x - r * .35, y - r * .35, r * .28, '#ffffff')    # نقطهٔ نور


def hull(p):
    p.shape([(X0, 8), (X0 + 10, 14), (X1 - 10, 14), (X1, 8), (X1 - 6, 32), (X0 + 8, 32)], HULL, PART, j=.25, step=4)
    rect(p, X0 + 8, 16, X1 - 8, 20, HULL_L)                                   # لبهٔ روشن (نور)
    rect(p, X0 + 10, 27, X1 - 8, 29.5, HULL_D)                                # خط آب
    for x in range(-44, 4, 16): p.ln((x, 21), (x, 26), INNER, HULL_D, j=0)     # درز تخته‌ها
    p.ln((X0 + 12, 23.5), (X1 - 12, 23.5), INNER, HULL_D, j=0, probe='خط داخلی (تختهٔ قایق)')
    disc(p, X0 + 4, 10, 3, YEL); disc(p, X1 - 4, 10, 3, YEL)                  # میخ‌های سر و ته بلم


def stall(p):
    for x in (-54, 4):                                                        # ستون‌ها
        rect(p, x - 3, -46, x + 3, 12, HULL_D); rect(p, x - 3, -46, x - 1, 12, '#a8703c')
    p.shape([(-52, -8), (2, -8), (2, 14), (-52, 14)], WOOD, PART, j=.2, step=6)                # پیشخوان
    rect(p, -49, -5, -2, -1, '#fff08a')                                       # نور تخته
    for x in (-34, -17): p.ln((x, 2), (x, 11), INNER, WOOD_D, j=0)
    for bx0, bx1, cols in ((-50, -32, (RED, ORG, YEL)), (-30, -14, (GRN, YEL, GRN)), (-12, 0, (PURP, RED, ORG))):
        flat(p, [(bx0, -22), (bx1, -22), (bx1 - 2.5, -6), (bx0 + 2.5, -6)], BASKET)   # سبد
        flat(p, [(bx0, -22), (bx1, -22), (bx1 - .6, -18), (bx0 + .6, -18)], '#d9955a'); rect(p, bx0 + 4, -14, bx1 - 4, -11.5, BASKET_D); rect(p, bx0 + 4, -9, bx1 - 4, -6.5, BASKET_D)
        c = (bx0 + bx1) / 2; w = (bx1 - bx0) / 4
        for i, col in enumerate(cols): fruit(p, c + (i - 1) * w * 1.1, -27 - (i % 2) * 4, 5.2, col)
    # سایبان راه‌راه با لبهٔ دندانه‌دار
    ax, n, w, y0, y1 = -58, 8, 8.8, -46, -66
    for i in range(n):
        flat(p, [(ax + i * w, y0), (ax + (i + 1) * w, y0), (ax + (i + 1) * w - 2.5, y1), (ax + i * w + 2.5, y1)], RED if i % 2 == 0 else WH)
        flat(p, [(ax + i * w, y0), (ax + (i + 1) * w, y0), (ax + (i + .5) * w, y0 + 8)], RED_D if i % 2 == 0 else '#f3dfa8')   # دندانه
    p.stroke([(ax, y0), (ax + n * w, y0), (ax + n * w - 2.5, y1), (ax + 2.5, y1)], INNER, j=.2, step=4)


def mast(p):
    """دکل بلند، پرچم و ریسمان فانوس‌ها (از بالای فیگور رد می‌شود)."""
    rect(p, -57, -104, -51, -60, HULL_D); rect(p, -57, -104, -55, -60, '#a8703c')
    flat(p, [(-51, -108), (-34, -101), (-51, -94)], ORG)                       # پرچم
    flat(p, [(-51, -108), (-34, -101), (-40, -101)], '#ffb860')


def lights(p):
    p.ln((-52, -98), (42, -111), INNER, '#7a4a1c', j=0)                         # ریسمان
    for x, y, c in ((-30, -100, RED), (-12, -102, YEL), (6, -104.5, ORG), (26, -107.5, RED)):          # فانوس‌ها
        p.ln((x, y), (x, y + 6), INNER - 1.5, '#7a4a1c', j=0)
        flat(p, [(x - 3.5, y + 6), (x + 3.5, y + 6), (x + 2, y + 9), (x - 2, y + 9)], '#7a4a1c')
        disc(p, x, y + 16, 8, c); disc(p, x - 2.5, y + 13.5, 2.6, '#ffffff')
        flat(p, [(x - 3, y + 24), (x + 3, y + 24), (x + 2, y + 27), (x - 2, y + 27)], '#7a4a1c')


def boat(p):
    hull(p); mast(p); stall(p); lights(p)


def build(out=OUTD):
    p = Pen('floating_market', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-24, 34, 38); p.foot_tip(-24, 26, 18)
    with layer(p, 'boat'): boat(p)
    return p


STAND = None     # خودکار: find_stand

if __name__ == '__main__':
    p = build()
    offs = [p.V(o) for o in [(0, -BOB), (0, 0), (0, BOB)]]
    r = finish(p, 'floating_market', STAND, motion={'boat': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(offsets=offs, note='کل بلم، غرفه، دکل و ریسمان فانوس روی موج بالا و پایین؛ سکو ثابت؛ سایهٔ تماس ثابت')
    (OUTD / 'floating_market.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'inside': r['inside'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
