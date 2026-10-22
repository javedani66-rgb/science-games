#!/usr/bin/env python3
"""ایستگاه «کارگاه کشتی‌سازی» (D127): کشتی چوبی کامل از کنار (بدنهٔ بلند، دماغهٔ بالا‌آمده، دکل، بادبان روشن، پرچم) روی سه پایهٔ لغزان کوتاه؛ چکش و یک تخته جلوی آن.
لایهٔ متحرک node_shipyard_hammer (چکش)."""
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


# D127 (۱۹ اکتبر): کشتی چوبی کامل از کنار روی سه پایهٔ لغزان کوتاه؛ دماغهٔ بالا‌آمده (چپ)، دکل، بادبان روشن و پرچم. چکش و یک تخته جلوی پایه‌ها.
PLANK2 = '#f7b36a'; SEAM_C = '#c9692a'; CREAM_ = '#fff3c4'
BOW = (-72, -50); STERN = (24, -38); KEEL_B = (-60, -2); KEEL_S = (16, -3)
MX, MTOP = -24, -126


def sheer():
    return bez(BOW, (-48, -50), (-30, -30), 18) + bez((-30, -30), (-4, -31), STERN)[1:]


def hull_pts():
    keel = bez(KEEL_S, (-20, 3), KEEL_B)[1:]
    stem = bez(KEEL_B, (-90, -4), (-85, -34), 18)[1:] + bez((-85, -34), (-86, -50), BOW, 12)[1:]       # دماغهٔ نرم و گرد
    return sheer() + [(19, -18), KEEL_S] + keel + stem


def slipway(p):
    """سه پایهٔ لغزان ضخیم و کوتاه زیر کیل (بدون تیر و تکهٔ ریز)."""
    for x in (-46, -20, 6):
        p.tipshadow(x, 17, 11)
        p.shape([(x - 8, -1), (x + 8, -1), (x + 9, 14), (x - 9, 14)], WOOD, PART, j=.2, step=8, clip=False)
        rect(p, x - 4, 3, x - 1, 9, WOOD_L)


def sail(p, pts, col):
    p.raw('<polygon points="%s" fill="%s" stroke="%s" stroke-width="5.8" stroke-linejoin="miter" stroke-miterlimit="6"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, NAVY))


def ship(p):
    # بادبان‌ها: اصلی بزرگ سمت راست دکل با تیرک پایینی؛ جلویی مثلثی کوچک‌تر بین دکل و دماغه؛ هر دو بالاتر از بدنه و زیر پرچم
    BY = -42
    sail(p, [(MX, -108), (MX + 34, BY), (MX, BY)], CREAM_)                       # بادبان اصلی: مثلث قائم تیز سمت راست دکل
    sail(p, [(MX, -84), (MX, BY), (MX - 25, BY)], '#ffb23e')                     # بادبان جلویی: مثلث کوچک‌تر سمت چپ دکل
    p.ln((MX, -28), (MX, MTOP), PART, MAST, j=.1, probe='دکل (جزء)')                                       # دکل
    p.shape([(MX, MTOP), (MX + 20, MTOP + 6), (MX, MTOP + 12)], FLAG, INNER, j=.1, step=99, clip=False)   # پرچم
    # بدنهٔ بلند
    p.shape(hull_pts(), PLANK, PART, j=.15, step=99, clip=False)
    T = sheer()
    p.raw('<path d="M%s" fill="none" stroke="%s" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"/>' % (' L'.join('%.1f,%.1f' % q for q in p.X([(x + 1, y + 5) for x, y in T[3:]])), DARK))   # لبهٔ تیرهٔ عرشه
    for d, xmax in ((11, 12), (18, 4)):                                                                                        # درز تخته‌ها
        p.raw('<path d="M%s" fill="none" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>' % (' L'.join('%.1f,%.1f' % q for q in p.X([(x, y + d) for x, y in T[4:] if x < xmax])), SEAM_C))
    for x in (-52, -28, -4):                                                                                                    # سه روزنه
        y = min(q[1] for q in T if abs(q[0] - x) < 4) + 11
        p.raw('<circle cx="%.1f" cy="%.1f" r="3.6" fill="%s"/>' % (*p.X((x, y)), CREAM_))


def hammer(p):
    """چکش درشت خوابیده جلوی پایه‌ها: دستهٔ چوبی ضخیم + سر آبی‌خاکستری."""
    p.shape([(-62, 23), (-36, 23), (-36, 31), (-62, 31)], WOOD, PART, j=.1, step=8, clip=False)
    p.shape([(-42, 17), (-28, 17), (-28, 37), (-42, 37)], '#aab3d9', PART, j=.1, step=8, clip=False)


def boards(p):
    """یک تختهٔ درشت روی کف، کنار چکش."""
    p.shape([(-14, 20), (16, 20), (16, 33), (-14, 33)], PLANK2, PART, j=.1, step=8, clip=False); rect(p, -9, 24, 11, 26.5, SEAM_C)


def build(out=OUTD):
    p = Pen('shipyard', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    slipway(p)
    ship(p)
    boards(p)
    with layer(p, 'hammer'): hammer(p)
    return p


XF = (0.94, 8.0, -9.0)
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
