#!/usr/bin/env python3
"""ایستگاه «کارخانهٔ کشتی‌سازی» (بازطراحی ۱۷ اکتبر): قایق چوبی کوچک روی دو پایهٔ چوبی (قایق در حال ساخت)، سکوی دریایی.
بدنهٔ منحنی (هلال)، دکل مستقیم، یک بادبان مثلثی ساده. پایه‌ها ثابت‌اند و تا زیر بدنه بالا آمده‌اند.
لایهٔ متحرک node_shipyard_hull = بدنه + دکل + بادبان؛ فقط کمی بالا و پایین می‌رود (پایه‌ها همیشه زیر بدنه کامل‌اند)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit3/shipyard'
HULL = '#e8803a'; HULL_D = '#b85a1c'; HULL_L = '#ffc46b'; SAIL = '#fff3c4'; SAIL_B = '#ef6a4a'; MAST = '#8a5f0c'; WOOD = '#ffd84d'; WOOD_D = '#d9961c'
BOB = 3


def bez(p0, c, p1, n=14):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1])
            for t in [i / n for i in range(n + 1)]]


import functools, station_kit as _k   # D122/D123: حاشیهٔ چپ/راست ≥۴px (بدون دست‌زدن به کیت)
_k.margin_check = functools.partial(_k.margin_check, min_margin=4); _k.motion_check = functools.partial(_k.motion_check, min_margin=4)
DARK = '#7a3a12'; PLANK = '#f09a52'; RIB = '#ffd84d'; FLAG = '#ef6a4a'


def cradle(p):
    """لنگرگاه: دو پایهٔ چوبی بلند + یک تخته که کنارشان افتاده؛ ثابت و تا زیر بدنه کامل (حتی با بالا‌رفتن بدنه)."""
    for x in (-44, -4):
        p.tipshadow(x, 15, 15); p.foot_tip(x, 13, 7)
        p.shape([(x - 8, -12), (x + 8, -12), (x + 8, 15), (x - 8, 15)], WOOD, INNER, j=.2, step=6)
        p.ln((x - 3, 0), (x + 3, 0), INNER, WOOD_D, j=.1); p.ln((x - 3, 8), (x + 3, 8), INNER, WOOD_D, j=.1)
    p.shape([(-30, 15), (-14, 15), (-14, 21), (-30, 21)], WOOD, INNER, j=.2, step=8, clip=False)      # تختهٔ افتاده
    p.ln((-26, 18), (-18, 18), INNER, WOOD_D, j=.1)


OY = -9


def boat(p):
    """کشتی چوبی نیمه‌ساز: بدنه با دنده‌های باز (بالا، جداره‌ها نیمه‌کاره) و تخته‌کاری کامل (پایین) با پنجرهٔ گرد؛
    تیر لبهٔ بالایی؛ دکل، بادبان بزرگ، بادبان جلو، پرچم. همه یک لایهٔ متحرک."""
    Y = lambda pts: [(x, y + OY) for x, y in pts]
    p.shape(Y([(-24, -90), (-24, -48), (-60, -45)]), SAIL, INNER, j=.1, step=4, clip=False)           # بادبان بزرگ
    p.shape(Y([(-18, -84), (-18, -50), (10, -48)]), SAIL_B, INNER, j=.1, step=4, clip=False)          # بادبان جلو
    p.shape(Y([(-25, -106), (-25, -92), (26, -100), (13, -99)]), FLAG, INNER, j=.1, step=4, clip=False)            # پرچم
    A_, B_, C_ = (-24, -90), (-24, -48), (-60, -45)
    lerp = lambda u, v, t: (u[0] + (v[0] - u[0]) * t, u[1] + (v[1] - u[1]) * t + OY)
    for t in (.4, .65): p.ln(lerp(A_, B_, t), lerp(A_, C_, t), INNER, '#e8c970', j=.05)       # درز بادبان
    p.ln((-21, -108 + OY), (-21, -22 + OY), PART, MAST, j=.1, probe='دکل (جزء)')
    hull = [(-66, -37), (-60, -12), (-48, 2), (-8, 3), (6, -8), (14, -45), (-6, -39), (-42, -38)]
    p.shape(Y(hull), DARK, PART, j=.15, step=99)
    for x in (-54, -41, -28, -15, -2):                                                                  # دنده‌های باز: رنگ تخت
        t = -35 + (-6 if x > -10 else 0)
        p.fill(Y([(x - 4, t), (x + 4, t), (x + 4, -10), (x - 4, -10)]), RIB)
    p.shape(Y([(-62, -22), (12, -22), (6, -8), (-8, 3), (-48, 2)]), PLANK, PART, j=.15, step=99)       # تخته‌کاری
    p.ln((-58, -13 + OY), (4, -13 + OY), INNER, HULL_D, j=.1)
    p.ln((-50, -4 + OY), (-6, -4 + OY), INNER, HULL_D, j=.1)
    for x in (-52, -2):
        p.raw('<circle cx="%.1f" cy="%.1f" r="2.2" fill="%s"/>' % (x, -18 + OY, HULL_D))                 # میخ
    p.shape(ell(-27, -8 + OY, 5.2, 5.2, 0, 360, 18), '#9ad4ff', INNER, j=.1, step=99, clip=False)      # پنجرهٔ گرد
    p.ln((-62, -38 + OY), (11, -46 + OY), PART, WOOD, j=.1)                                              # تیر لبهٔ بالا


def build(out=OUTD):
    p = Pen('shipyard', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = (1.0, 0.0, 0.0)
    cradle(p)
    with layer(p, 'hull'): boat(p)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    offs = [(0, 0), p.V((0, -BOB))]
    r = finish(p, 'shipyard', STAND, motion={'hull': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(layer='node_shipyard_hull', translate=[0, -BOB], note='بدنه+دکل+بادبان کمی بالا و پایین می‌رود؛ دو پایهٔ چوبی ثابت و تا زیر بدنه کامل‌اند')
    (OUTD / 'shipyard.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
