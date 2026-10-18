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


# بدنه (قاب باز): هلال با دماغه/عقب مایل. پارامتر u از 0 (دماغهٔ چپ) تا 1 (عقب): کف از (-50..-12) و لبهٔ بالا از (-58..-4)
TX0, TX1, BX0, BX1 = -62, 0, -52, -10
def _t(u): return 2 * u - 1
def bot_(u): return (BX0 + (BX1 - BX0) * u, 16 - 3 * _t(u) ** 2)
def top_(u): return (TX0 + (TX1 - TX0) * u, -18 - 12 * _t(u) ** 2 - 4 * (1 - u))
def at(u, f):
    (x0, y0), (x1, y1) = bot_(u), top_(u); return (x0 + (x1 - x0) * f, y0 + (y1 - y0) * f)
def us_(a, b, n=10): return [a + (b - a) * i / n for i in range(n + 1)]
PLANK2 = '#f7b36a'; SEAM_C = '#c9692a'


def boat(p):
    """بدنهٔ نیمه‌ساخته (هلال): درونِ تیره، چهار دندهٔ باز، چهار ردیف تختهٔ نصب‌شده فقط سمت چپ (پله‌ای)، کیل، دکل لخت."""
    p.ln((-34, -76), (-34, -20), PART, MAST, j=.1, probe='دکل (جزء)')                  # دکل لخت (پشت بدنه)
    p.shape([(-34, -76), (-22, -72), (-34, -68)], FLAG, INNER, j=.1, step=99, clip=False)
    sil = [at(u, 0) for u in us_(0, 1)] + [at(u, 1) for u in us_(1, 0)]
    p.shape(sil, DARK, PART, j=.15, step=99, clip=False)                              # بدنهٔ هلالی، درون تیره
    for u in (.14, .34, .54, .74, .91):                                                     # دنده‌های باز
        (xa, ya), (xb, yb) = at(u, -.04), at(u, 1.04)
        poly(p, [(xa - 3, ya), (xa + 3, ya), (xb + 3, yb), (xb - 3, yb)], RIB)
    ext = [.84, .62, .42, .22]                                                          # تخته‌های نصب‌شده، پله‌ای
    for k, ue in enumerate(ext):
        f0, f1 = k / 4, (k + 1) / 4
        pts = [at(u, f0) for u in us_(.02, ue, 8)] + [at(u, f1) for u in us_(ue, .02, 8)]
        poly(p, pts, PLANK if k % 2 == 0 else PLANK2)
        if k: p.ln(at(.04, f0), at(ue, f0), INNER, SEAM_C, j=.05)
    p.shape(sil, 'none', PART, j=.15, step=99, clip=False)                             # لبهٔ بیرونی روی همه
    for (u, f) in ((.06, .5), (.17, .22), (.3, .22)):
        p.raw('<circle cx="%.1f" cy="%.1f" r="1.8" fill="%s"/>' % (*p.X(at(u, f)), DARK))
    kp = [at(u, 0) for u in us_(.08, .92)]                                             # کیل: تیر زیر کف
    p.shape([(x, y + 1) for x, y in kp] + [(x, y + 8) for x, y in kp[::-1]], WOOD_D, INNER, j=.1, step=99, clip=False)


def slip(p):
    """سکوی ساخت: دو تیر پشتیبان زیر کیل."""
    for x in (-44, -20):
        p.tipshadow(x, 19, 9)
        p.shape([(x - 7, 16), (x + 7, 16), (x + 7, 21), (x - 7, 21)], WOOD, INNER, j=.2, step=8, clip=False)


def scaffold(p):
    """داربست پشتِ بدنه: دو ستون بلند تا بالای بدنه، کف‌تختهٔ بالا، نردبان میانی (پایینش پشت بدنه)؛ روی کف: دو تخته و چکش."""
    X0, X1, PY = -10, 10, -44
    for x in (X0, X1):
        rect(p, x - 3.5, PY - 12, x + 3.5, 14, WOOD); rect(p, x - 3.5, PY - 12, x - 1.2, 14, WOOD_L)
    for x in (X0 + 6, X1 - 6): p.ln((x, PY + 7), (x, 6), INNER, WOOD_D, j=0)                              # ریل نردبان
    for y in (-32, -22, -12): p.ln((X0 + 6, y), (X1 - 6, y), INNER, WOOD_D, j=0)
    p.shape([(X0 - 8, PY), (X1 + 3, PY), (X1 + 3, PY + 7), (X0 - 8, PY + 7)], '#f0b25a', INNER, j=.1, step=8, clip=False)     # کف‌تخته
    p.tipshadow(0, 17, 12)


def hammer(p):
    """چکش ایستاده روی کف داربست: دستهٔ چوبی راست، سر افقی آبی‌خاکستری (شکل T)."""
    p.ln((5, -46), (5, -62), PART, WOOD_D, j=0)
    p.shape([(-3, -72), (14, -72), (14, -61), (-3, -61)], '#aab3d9', INNER, j=.1, step=99, clip=False)


def boards(p):
    """دو تختهٔ آمادهٔ روی کف داربست (سمت چپ): رنگ تخت، بدون خط دور."""
    for y in (-49, -55):
        rect(p, -17, y - 2.6, -4, y + 2.6, PLANK2); rect(p, -17, y + 1, -4, y + 2.6, SEAM_C)


def build(out=OUTD):
    p = Pen('shipyard', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    slip(p)
    scaffold(p)
    boards(p)
    with layer(p, 'hammer'): hammer(p)
    boat(p)
    return p


XF = (1.04, -1.0, -6.0)
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
