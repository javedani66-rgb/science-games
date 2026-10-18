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


# بدنه: کشتی چوبی بلند از کنار؛ دماغهٔ بالا‌آمده چپ، پاشنه راست. u از 0 (دماغه) تا 1 (پاشنه)
HX0, HX1 = -64, 14
PLANK2 = '#f7b36a'; SEAM_C = '#c9692a'
def top_(u): return (HX0 + (HX1 - HX0) * u, -26 - 18 * (1 - u) ** 2.2)
def bot_(u): return (HX0 + (HX1 - HX0) * u, 10 - 30 * (1 - u) ** 3 - 8 * u ** 4)
def at(u, f):
    (x0, y0), (x1, y1) = bot_(u), top_(u); return (x0 + (x1 - x0) * f, y0 + (y1 - y0) * f)
def us_(a, b, n=10): return [a + (b - a) * i / n for i in range(n + 1)]


def cradles(p):
    """سه پایهٔ نگه‌دارندهٔ ساخت زیر کیل."""
    for u in (.28, .58, .88):
        x, y = bot_(u)
        p.tipshadow(x, 18, 9)
        p.shape([(x - 6, y - 4), (x + 6, y - 4), (x + 8, 18), (x - 8, 18)], WOOD, INNER, j=.2, step=8, clip=False)


def boat(p):
    """نیمهٔ جلو تختهٔ کامل (ردیف تخته + میخ)، نیمهٔ عقب فقط پنج دندهٔ زرد روی درونِ تیره؛ دکل لخت کوتاه."""
    p.ln((-22, -20), (-22, -66), PART, MAST, j=.1, probe='دکل (جزء)')
    p.shape([(-22, -66), (-10, -62), (-22, -58)], FLAG, INNER, j=.1, step=99, clip=False)
    sil = [top_(u) for u in us_(0, 1, 14)] + [bot_(u) for u in us_(1, 0, 14)]
    p.shape(sil, DARK, PART, j=.15, step=99, clip=False)
    for u in (.60, .70, .80, .90, .985):                                  # دنده‌های باز (عقب)
        (xa, ya), (xb, yb) = at(u, 1.02), at(u, -.02)
        poly(p, [(xa - 3, ya), (xa + 3, ya), (xb + 3, yb), (xb - 3, yb)], RIB)
    p.ln(top_(.56), top_(1), INNER, RIB, j=0)                              # لبهٔ بالای عقب
    ext = [.58, .50, .58, .50]                                            # ردیف‌های تخته، پله‌ای
    for k, ue in enumerate(ext):
        f0, f1 = k / 4, (k + 1) / 4
        pts = [at(u, f0) for u in us_(0, ue, 10)] + [at(u, f1) for u in us_(ue, 0, 10)]
        poly(p, pts, PLANK if k % 2 == 0 else PLANK2)
        if k: p.raw('<path d="M%s" fill="none" stroke="%s" stroke-width="2.2" stroke-linecap="round"/>' % (' L'.join('%.1f,%.1f' % q for q in p.X([at(u, f0) for u in us_(.03, ue, 10)])), SEAM_C))
        for u in (.12, .3, .46):
            if k % 2 == 0: p.raw('<circle cx="%.1f" cy="%.1f" r="1.6" fill="%s"/>' % (*p.X(at(u, (f0 + f1) / 2)), DARK))
    p.shape(sil, 'none', PART, j=.15, step=99, clip=False)


def hammer(p):
    """چکش بزرگ خوابیده روی کف جلوی پایه‌ها: سر آبی‌خاکستری چپ، دستهٔ چوبی."""
    p.ln((-22, 26), (0, 26), PART, WOOD_D, j=0)
    p.shape([(-34, 20), (-21, 20), (-21, 32), (-34, 32)], '#aab3d9', INNER, j=.1, step=99, clip=False)


def boards(p):
    """تختهٔ آماده روی کف کنار چکش."""
    poly(p, [(6, 22), (26, 22), (28, 28), (4, 28)], PLANK2); rect(p, 5, 26, 27, 28, SEAM_C)


def build(out=OUTD):
    p = Pen('shipyard', 'sea'); pad(p, line=((44, 30), (62, 27)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    cradles(p)
    boat(p)
    boards(p)
    with layer(p, 'hammer'): hammer(p)
    return p


XF = (1.0, 0.0, -4.0)
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
