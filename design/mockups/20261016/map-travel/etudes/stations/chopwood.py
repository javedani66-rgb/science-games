#!/usr/bin/env python3
"""ایستگاه «چوب‌شکافی» (M09) با station_kit: کندهٔ بزرگ ایستاده با رینگ‌های سالیانه و پوست، تبر بزرگ فرورفته در آن
(تیغهٔ فلزی روشن با لبهٔ برنده، دستهٔ چوبی) و دو تکهٔ هیزم شکافته روی سکو. سکوی پیش‌فرض کیت، فیگور سمت راست.
لایهٔ متحرک node_chopwood_axe = تبر؛ بالا می‌رود (کشیده در امتداد دسته) و فرود می‌آید. در حالت ایستا فرورفته در کنده است."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from functools import partial
import station_kit
from station_kit import *
station_kit.margin_check = partial(station_kit.margin_check, min_margin=4)
station_kit.motion_check = partial(station_kit.motion_check, min_margin=4)
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/chop/chopwood'

BARK = '#a8672f'; BARK_L = '#d29255'; BARK_D = '#7a4a1f'
FACE = '#f7d894'; FACE_L = '#fff0c4'; RING = '#c98f4a'; PITH = '#8a4f1f'
WOOD = '#b77a3a'; WOOD_L = '#d9a463'
STEEL = '#dbe9f8'; STEEL_S = '#a3bbd9'; STEEL_L = '#ffffff'; EYE = '#7f95b8'

CX, CR, TOPY, BOTY, RYE = -36, 36, -42, 2, 13      # کنده: مرکز x، شعاع، y رویه، y ته، نیم‌ارتفاع بیضی
AX, AY, LEAN = -52, -36, 48                        # نقطهٔ نشستن لبهٔ تیغه روی رویه و زاویهٔ خوابیدن دسته (درجه، به راست)
LIFT = 22


def stump(p):
    p.tipshadow(CX + 6, BOTY + 8, 40)
    body = ell(CX, BOTY, CR, RYE, 0, 180, 18) + [(CX - CR, TOPY), (CX + CR, TOPY)]
    p.shape(body, BARK, OUT, j=.5, step=14, clip=True)
    p.fill([(CX + CR - 12, TOPY), (CX + CR, TOPY), (CX + CR, BOTY), (CX + CR - 16, BOTY + 7)], BARK_D, .55)      # سایهٔ سمت راست
    p.fill([(CX - CR + 5, TOPY + 2), (CX - CR + 11, TOPY + 2), (CX - CR + 11, BOTY + 2), (CX - CR + 5, BOTY + 1)], BARK_L, .9)   # نور سمت چپ
    for (dx, y0, y1) in ((-17, -30, -10), (-4, -34, -2), (9, -28, -8), (20, -32, 0)):                    # شیار پوست
        p.ln((CX + dx, y0), (CX + dx, y1), INNER, BARK_D, j=.2)
    # رویهٔ بریده با رینگ‌های سالیانه
    p.shape(ell(CX, TOPY, CR, RYE, 0, 360, 36), FACE, OUT, j=.4, step=14, clip=False)
    for k in (.72, .46, .22):
        p.raw('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" stroke-width="%s"/>' % (*p.X((CX + 1, TOPY)), CR * k - 2, RYE * k - .6, RING, INNER))
    p.raw('<ellipse cx="%.1f" cy="%.1f" rx="3" ry="1.6" fill="%s"/>' % (*p.X((CX + 1, TOPY)), PITH))
    p.ln((CX - 22, TOPY + 3), (CX - 10, TOPY + 6), INNER, FACE_L, j=.1)


def piece_up(p, x0, w, ytop, ybot):
    """تکهٔ هیزم ایستادهٔ شکافته: نیمی پوست، نیمی سطح شکافِ روشن؛ بالا بیضی با حلقه."""
    body = ell(x0 + w / 2, ybot, w / 2, 5, 0, 180, 10) + [(x0, ytop), (x0 + w, ytop)]
    p.shape(body, BARK, OUT, j=.3, step=14, clip=True)
    p.fill([(x0 + 1, ytop + 2), (x0 + w * .46, ytop + 2), (x0 + w * .46, ybot + 2), (x0 + 1, ybot + 1)], FACE_L)
    p.ln((x0 + w * .46, ytop + 3), (x0 + w * .46, ybot + 2), INNER, BARK_D, j=.1)
    p.shape(ell(x0 + w / 2, ytop, w / 2, 5, 0, 360, 20), FACE, PART, j=.2, step=14, clip=False)
    p.raw('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="1.6" fill="none" stroke="%s" stroke-width="%s"/>' % (*p.X((x0 + w / 2, ytop)), w * .2, RING, INNER * .8))


def piece_lying(p, xl, xr, cy, r):
    """تکهٔ خوابیده: استوانه از کنار، سر راست = سطح شکاف روشن با حلقه."""
    pts = ell(xr, cy, 5, r, -90, 90, 8) + ell(xl, cy, 3, r, 90, 270, 8)
    p.shape(pts, BARK, PART, j=.2, step=14, clip=False)
    p.ln((xl + 6, cy - r + 4), (xr - 8, cy - r + 4), INNER, BARK_L, j=.1)
    p.ln((xl + 10, cy + 3), (xl + 20, cy + 3), INNER, BARK_D, j=.1)
    p.shape(ell(xr, cy, 5, r - 1.5, 0, 360, 14), FACE, INNER, j=.1, step=14, clip=False)
    p.raw('<ellipse cx="%.1f" cy="%.1f" rx="1.8" ry="%.1f" fill="none" stroke="%s" stroke-width="%s"/>' % (*p.X((xr, cy)), r * .4, RING, INNER * .7))


HANDLE = [(-6.5, 4), (6.5, 4), (6, -78), (9.5, -82), (9.5, -94), (-9.5, -94), (-9.5, -82), (-6, -78)]
POLL = [(-13, -28), (-2, -28), (-2, -8), (-13, -8)]
BLADE = [(-5, -32), (14, -34), (30, -48), (37, -30), (39, -16), (36, 0), (14, 4), (-5, -4)]
EDGE = ((32, -44), (35, -22), (33, -2))        # لبهٔ برندهٔ روشن (روی لبهٔ راست تیغه)


def axe_f():
    """تبر کلاسیک (دسته بالا، تیغه سمت راست، لبه موازی دسته) که حول نقطهٔ سر به راست می‌خوابد تا لبه در رویهٔ کنده بنشیند."""
    f = rot(0, 0, LEAN)
    ymax = max(f(q)[1] for q in BLADE)
    ox, oy = AX, AY - ymax
    return (lambda q: (ox + f(q)[0], oy + f(q)[1]))


def axe(p):
    F = axe_f()
    p.shape(TP(F, HANDLE), WOOD, PART, j=.25, step=16, clip=False)
    p.ln(F((-2.8, -6)), F((-2.8, -76)), INNER, WOOD_L, j=.1)
    p.ln(F((-6, -86)), F((6, -86)), INNER, BARK_D, j=.1)
    p.shape(TP(F, POLL), EYE, PART, j=.15, step=16, clip=False)                         # پشت تبر (کوبه)
    p.shape(TP(F, BLADE), STEEL, OUT, j=.3, step=16, clip=False)                         # تیغه
    p.fill(TP(F, [(-3, -30), (6, -30), (6, -2), (-3, -4)]), EYE)                        # چشمهٔ دسته
    p.fill(TP(F, [(18, -33), (30, -45), (33, -30), (31, -6), (18, 1)]), STEEL_S)       # سایهٔ نیمهٔ بیرونی
    p.ln(F((13, -22)), F((24, -37)), INNER, STEEL_L, j=.1)                               # برق
    p.ln(F(EDGE[0]), F(EDGE[2]), PART, STEEL_L, j=.1)                                    # لبهٔ تیز روشن


def crack(p):
    """شکاف تیره و تراشه‌های روشن روی رویهٔ کنده در جای فرورفتن تیغه (پشت تبر، ثابت)."""
    F = axe_f(); bot = sorted((F(q) for q in BLADE), key=lambda t: -t[1])[:2]
    (x0, y0), (x1, y1) = sorted(bot)
    L = math.hypot(x1 - x0, y1 - y0) or 1; ux, uy = (x1 - x0) / L, (y1 - y0) / L
    a = (x0 - ux * 9, y0 - uy * 9 + 1); b = (x1 + ux * 9, y1 + uy * 9 + 1)
    p.ln(a, b, PART, PITH, j=.05)
    p.ln((a[0] + 4, a[1] - 5), (b[0] - 6, b[1] - 6), INNER, FACE_L, j=.05)          # لبهٔ روشن بالای شکاف
    p.fill([(x0 + 2, y0 + 1), (x0 + 9, y0 + 7), (x0 + 12, y0 + 2)], FACE_L)         # تراشهٔ چوب
    p.fill([(x1 - 4, y1 + 2), (x1 + 6, y1 + 9), (x1 + 9, y1 + 2)], FACE_L)


def build(out=None, legacy_shadow=False):
    p = Pen('chopwood', 'land')
    pad(p, line=((-62, 33), (-44, 35)), tri=(), dot=(-12, 36))
    p.foot_tip(CX, BOTY + 4, 34); p.foot_tip(14, 6, 12); p.foot_tip(0, 23, 14)
    stump(p)
    p.tipshadow(14, 8, 14); p.tipshadow(2, 29, 18)
    piece_up(p, 3, 22, -20, 6)
    piece_lying(p, -14, 14, 23, 8.5)
    crack(p)
    with layer(p, 'axe'): axe(p)
    return p, symbol(p, 'chopwood', ['axe'], out=out, legacy_shadow=legacy_shadow)


STAND = None
if __name__ == '__main__':
    p, sym = build(out=OUTD)
    d = (math.sin(math.radians(LEAN)) * LIFT, -math.cos(math.radians(LEAN)) * LIFT)
    offs = [(0, 0), (d[0] / 2, d[1] / 2), d]
    r = finish(p, 'chopwood', STAND, motion={'axe': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = dict(axe=dict(layer='node_chopwood_axe', offsets=[[round(a, 1), round(b, 1)] for a, b in offs],
                                     note='تبر در امتداد دسته تا ۲۲ واحد بالا می‌رود و با فرود دوباره در کنده فرو می‌رود؛ حالت ایستا = فرورفته'))
    (OUTD / 'chopwood.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'inside': r['inside'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
