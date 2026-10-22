#!/usr/bin/env python3
"""ایستگاه «کارگاه کشتی‌سازی» (D127): کشتی چوبی کامل از کنار (بدنهٔ بلند، دماغهٔ بالا‌آمده، دکل، بادبان روشن، پرچم) روی سه پایهٔ لغزان کوتاه؛ چکش و یک تخته جلوی آن.
لایهٔ متحرک node_shipyard_hammer (چکش)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/shipyard'
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


from r6lib import extrude, poly as fpoly, circ          # حجم ¾ با سه پلهٔ رنگ؛ بین وجه‌ها خط نیست (قاعده ۱۴)
HERO_W, HERO_T = 3.6, 2.8                                 # خط دور قهرمان / قطعهٔ فرعی (قاعده ۲۴)
D_H = (12, -8)
H_F, H_T, H_S = '#f09a52', '#ffd9a0', '#b85a1c'          # بدنه: جلو / رو / پهلو
SL_F, SL_T, SL_S = '#ffd84d', '#fff0a0', '#d9961c'      # پایه‌های لغزان
HM_F, HM_T, HM_S = '#aab3d9', '#dde2f5', '#6b75a8'       # سر چکش


def slipway(p):
    """سه پایهٔ لغزان کوتاه و هم‌ضخامت زیر کیل (قاعده ۲۰)."""
    for x in (-52, 8):
        p.tipshadow(x + 5, 11, 12)
        extrude(p, [(x - 10, -4), (x + 10, -4), (x + 14, 8), (x - 14, 8)], (7, -4), SL_F, SL_T, SL_S, sw=HERO_T, sw_in=0)


def sail(p, pts, col):
    """بادبان: ورقهٔ نازک و جدا (خط نازک)."""
    p.raw('<polygon points="%s" fill="%s" class="eo" stroke-width="%s" stroke-linejoin="miter" stroke-miterlimit="6"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, HERO_T))


def ship(p):
    BY = -50                                                                              # پای دکل: داخل کشتی، روی کف عرشه
    hull = bez((-90, -64), (-80, -48), (-66, -47), 8)[:-1] + [(-66, -47), (30, -47)] + bez((30, -47), (40, -50), (44, -64), 6)[1:] \
        + bez((44, -64), (38, -18), (14, -4), 12)[1:] + [(-48, -4)] + bez((-48, -4), (-82, -10), (-90, -64), 14)[1:-1]
    MXX = -22
    extrude(p, hull, D_H, H_F, H_T, H_S, mid=H_F, sw=HERO_W, sw_in=0)                    # بدنه: یک شکل
    dx, dy = D_H                                                                           # درون کشتی توخالی: دهانهٔ تیره با لبهٔ روشن جلو (قاعده ۱۹)
    fq = lambda u, x: (x + dx * u, -46 + dy * u)
    poly(p, [fq(.2, -66), fq(.2, 24), fq(.9, 24), fq(.9, -66)], '#7a3a12')
    poly(p, [fq(.2, -66), fq(.2, 24), fq(.32, 24), fq(.32, -66)], '#b85a1c')
    sail(p, [(MXX, -112), (MXX + 38, BY - 2), (MXX, BY - 2)], CREAM_)                    # بادبان بزرگ (جلوی دهانه، پایش در کشتی)
    sail(p, [(MXX - 3.6, -118), (MXX + 3.6, -118), (MXX + 3.6, BY), (MXX - 3.6, BY)], MAST)   # دکل
    sail(p, [(MXX + 2.2, -118), (MXX + 22, -112), (MXX + 2.2, -106)], FLAG)              # پرچم
    p.raw('<path d="M%s" fill="none" stroke="%s" stroke-width="1.8" stroke-linecap="round"/>' % (' L'.join('%.1f,%.1f' % q for q in p.X([(-68, -24), (20, -24)])), SEAM_C))
    for x in (-48, -22, 4):                                                               # سه روزنه
        a, b = p.X((x, -35)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, 3.8 * p.xf[0], CREAM_))


def hammer(p):
    """چکش درشت خوابیده: دستهٔ چوبی + سر آبی‌خاکستری."""
    extrude(p, [(-72, 24), (-34, 24), (-34, 32), (-72, 32)], (5, -3), SL_F, SL_T, SL_S, sw=HERO_T, sw_in=0)
    extrude(p, [(-40, 15), (-26, 15), (-26, 41), (-40, 41)], (6, -4), HM_F, HM_T, HM_S, sw=HERO_T, sw_in=0)


def boards(p):
    extrude(p, [(-14, 22), (16, 22), (16, 33), (-14, 33)], (8, -5), PLANK2, '#ffe0b0', SEAM_C, sw=HERO_T, sw_in=0)
    rect(p, -9, 26, 11, 28, SEAM_C)


def build(out=OUTD):
    p = Pen('shipyard', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    slipway(p)
    ship(p)
    boards(p)
    with layer(p, 'hammer'): hammer(p)
    return p


XF = (0.9, 6.0, -8.0)
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
