#!/usr/bin/env python3
"""ایستگاه «کارخانهٔ کشتی‌سازی» (بازطراحی ۱۸ اکتبر شب، D125): بدنهٔ نیمه‌ساختهٔ کشتی (دنده‌های باز + چند تخته) روی سکوی ساخت، داربست با نردبان، چکش و تخته‌های آماده؛ فقط دکل لخت.
لایهٔ متحرک node_shipyard_hammer (چکش). ----- توضیح قدیمی: 
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
WOOD_L = '#ffe88a'; DARK = '#7a3a12'; PLANK = '#f09a52'; RIB = '#ffd84d'; FLAG = '#ef6a4a'


def rect(p, x0, y0, x1, y1, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])), col))


def poly(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


# بدنه (قاب باز): کف منحنی b(x) و لبهٔ بالا s(x) (واحد symbol)
HX0, HX1 = -64, 8
def b_(x):
    t = (x - HX0) / (HX1 - HX0); return 2 + 8 * (2 * t - 1) ** 2                  # کف: 2 در وسط تا 10 در دو سر
def s_(x):
    t = (x - HX0) / (HX1 - HX0); return -42 - 4 * (1 - t) + 6 * (2 * t - 1) ** 2 * .0   # لبهٔ بالا: دماغهٔ چپ کمی بالاتر
def hull_pts(x0, x1, f0, f1, n=8):
    """ناحیهٔ بین دو منحنی (کسر f0 تا f1 از کف تا لبهٔ بالا) در بازهٔ x0..x1."""
    xs = [x0 + (x1 - x0) * i / n for i in range(n + 1)]
    lo = [(x, b_(x) + (s_(x) - b_(x)) * f0) for x in xs]; hi = [(x, b_(x) + (s_(x) - b_(x)) * f1) for x in xs]
    return lo + hi[::-1]


RIBX = (-56, -45, -34, -23, -12, -1)
SEAM_C = '#d9702a'


def boat(p):
    """بدنهٔ نیمه‌ساخته: کیل (تیر کف)، شش دندهٔ باز، تخته‌کاری فقط در سمت چپ (چهار ردیف پله‌ای)، دکل لخت."""
    # دکل لخت (پشت دنده‌ها)
    p.ln((-30, -86), (-30, -18), PART, MAST, j=.1, probe='دکل (جزء)')
    p.shape([(-30, -86), (-14, -82), (-30, -78)], FLAG, INNER, j=.1, step=99, clip=False)
    # دنده‌های باز: هر دنده کمی خمیده، رنگ تخت
    for x in RIBX:
        poly(p, [(x - 3.6, b_(x) - 2), (x + 3.6, b_(x) - 2), (x + 3.6 + 1, s_(x)), (x - 3.6 + 1, s_(x))], RIB)
    # تخته‌های نصب‌شده: چهار ردیف، سمت چپ کامل و به راست کوتاه‌تر
    ext = [-6, -22, -36, -50]      # آخرین x هر ردیف، از پایین به بالا
    for k, xe in enumerate(ext):
        p.shape(hull_pts(HX0 + 1, xe, k / 4, (k + 1) / 4), PLANK if k % 2 == 0 else '#f7b36a', INNER, j=.1, step=99, clip=False)
    # کیل
    p.shape([(HX0 - 2, b_(HX0) + 2), (HX1 + 2, b_(HX1) + 2), (HX1 - 6, b_(HX1) + 9), (HX0 + 6, b_(HX0) + 9)], DARK, INNER, j=.1, step=99, clip=False)
    # تیر لبهٔ بالا (فقط روی دنده‌ها، ادامهٔ نیمه‌کاره)
    p.ln((HX0 + 2, s_(HX0) - 1), (HX1 - 2, s_(HX1) - 1), PART, WOOD_D, j=.1)
    # میخ
    for (x, f) in ((-58, .5), (-47, .5), (-36, .25)):
        p.raw('<circle cx="%.1f" cy="%.1f" r="2" fill="%s"/>' % (*p.X((x, b_(x) + (s_(x) - b_(x)) * f)), DARK))


def slip(p):
    """سکوی ساخت: دو تیر زیر کیل روی پایه‌های کوتاه."""
    for x in (-52, -4):
        p.tipshadow(x + 5, 16, 11)
        p.shape([(x - 8, 11), (x + 10, 11), (x + 10, 18), (x - 8, 18)], WOOD, INNER, j=.2, step=8, clip=False)


def scaffold(p):
    """داربست چوبی: دو ستون، یک کف‌تخته‌ای بالا، نردبان تکیه‌داده؛ چکش روی کف و چند تختهٔ آماده روی زمین."""
    X0, X1, PY = 18, 44, -30
    for x in (X0, X1):
        rect(p, x - 3.5, PY - 16, x + 3.5, 16, WOOD); rect(p, x - 3.5, PY - 16, x - 1.2, 16, WOOD_L)
    p.ln((X0 + 3, 12), (X1 - 3, PY + 6), INNER, WOOD, j=0)                       # بادبند ضربدری
    p.ln((X0 + 3, PY + 6), (X1 - 3, 12), INNER, WOOD, j=0)
    p.shape([(X0 - 8, PY), (X1 + 8, PY), (X1 + 8, PY + 7), (X0 - 8, PY + 7)], '#f0b25a', INNER, j=.1, step=8, clip=False)   # کف‌تخته
    p.ln((X0 - 2, PY + 3.5), (X0 + 6, PY + 3.5), INNER * .7, WOOD_D, j=0)
    # نردبان: تکیه‌داده به لبهٔ کف، پایین سمت چپ
    lx0, lx1 = 6, 14
    p.ln((lx0, 14), (X0 - 4, PY + 7), INNER, WOOD, j=0); p.ln((lx0 + 9, 14), (X0 + 5, PY + 7), INNER, WOOD, j=0)
    for t in (.28, .52, .76):
        a = (lx0 + (X0 - 4 - lx0) * t, 14 + (PY + 7 - 14) * t); b = (lx0 + 9 + (X0 + 5 - lx0 - 9) * t, a[1])
        p.ln(a, b, INNER, WOOD_L, j=0)
    # تخته‌های آماده روی زمین
    for k, y in enumerate((8, 2)):
        p.shape([(26 + 2 * k, y), (50 + 2 * k, y), (50 + 2 * k, y + 6), (26 + 2 * k, y + 6)], '#f7b36a', INNER, j=.1, step=99, clip=False)
    p.tipshadow(38, 15, 14)


def hammer(p):
    """چکش روی کف داربست: دستهٔ چوبی و سر آبی‌خاکستری."""
    HXc, HYc = 34, -33
    p.ln((HXc - 12, HYc - 1), (HXc + 8, HYc - 1), PART, WOOD_D, j=0)
    p.shape([(HXc + 5, HYc - 12), (HXc + 17, HYc - 12), (HXc + 17, HYc + 7), (HXc + 5, HYc + 7)], '#aab3d9', INNER, j=.1, step=99, clip=False)


def build(out=OUTD):
    p = Pen('shipyard', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    slip(p)
    scaffold(p)
    boat(p)
    with layer(p, 'hammer'): hammer(p)
    return p


XF = (1.0, -2.0, 0.0)
HAMMER_LIFT = 5

STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'shipyard', STAND, motion={'hammer': dict(offsets=[(0, 0), p.V((0, -HAMMER_LIFT))])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_shipyard_hammer': dict(translate_y=[0, -HAMMER_LIFT], rotate_about='ته دسته (پیشنهادی ±15°)', cycle_s=1.2, note='چکش بلند می‌شود و می‌کوبد؛ بدنهٔ نیمه‌ساخته، داربست و تخته‌ها ثابت و کامل‌اند.'),
                         'reduced_motion': 'چکش ثابت'}
    (OUTD / 'shipyard.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
