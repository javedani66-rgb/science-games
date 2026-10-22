#!/usr/bin/env python3
"""ایستگاه «بازارچهٔ شناور» (E06؛ اصلاح خط ۲۳ اکتبر): قهرمان = بلم بازار ¾ سه‌بعدی. سه جزء درشت:
۱) عرشهٔ چوبی بلم (جعبهٔ ¾: رویه/جلو/پهلو)؛ ۲) غرفه: پیشخوان زرد + سایبان راه‌راه قرمز-سفید (راه‌راه‌ها از جلو روی رویهٔ سایبان می‌پیچند) + دو ستون؛ ۳) چهار میوهٔ درشت روی پیشخوان.
بین وجه‌ها خط نیست (فقط پلهٔ رنگ)؛ خط دور اصلی ۳٫۶، فرعی ۲٫۶ (ستون‌ها، میوه‌ها).
لایهٔ متحرک node_floating_market_boat = کل بلم و غرفه و میوه که روی موج بالا و پایین می‌رود (dy در -3..+3)؛ سکو و سایهٔ تماس ثابت."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
import station_kit
from station_kit import *
from functools import partial
station_kit.margin_check = partial(station_kit.margin_check, min_margin=4)   # D123: حاشیهٔ چپ/راست ≥۴px

# ---- کمک‌های ¾ سه‌بعدی (محلی؛ سه پلهٔ رنگ، بدون خط بین وجه‌ها، خط دور یکدست) ----
from shapely.geometry import Polygon, MultiPoint, box as sbox
from shapely.ops import unary_union
from g4_helpers import poly, disc, arcline
from r6lib import extrude
M_OUT, M_PART = 3.6, 2.6          # قاعدهٔ ۲۴: خط اصلی ۳٫۶، فرعی ۲٫۶


def gfill(p, g, col):
    for q in (g.geoms if hasattr(g, 'geoms') else [g]):
        if q.geom_type == 'Polygon' and q.area > .05: poly(p, list(q.exterior.coords)[:-1], col)


def sil(geoms):
    s = unary_union(geoms).buffer(.01)
    return s if s.geom_type == 'Polygon' else max(s.geoms, key=lambda g: g.area)


def sil_open(p, s, fill, sw=M_OUT):
    p.shape(list(s.exterior.coords)[:-1], fill, sw, j=0, step=6, clip=False)


def sil_close(p, s, sw=M_OUT):
    p.stroke(list(s.exterior.coords)[:-1], sw, j=0, step=6)


class Fr:
    """استوانه/مخروط ناقص ¾: مرکز رویه (cx,yt) شعاع rt (۰ = مخروط)، مرکز کف yb شعاع rb؛ ellipse با نسبت k."""
    def __init__(s, cx, yt, yb, rt, rb, k=.32):
        s.cx, s.yt, s.yb, s.rt, s.rb, s.k = cx, yt, yb, rt, rb, k
        s.bot = Polygon(ell(cx, yb, rb, rb * k, 0, 360, 40))
        s.top = Polygon(ell(cx, yt, rt, rt * k, 0, 360, 40)) if rt > 0 else None
        pts = list(s.bot.exterior.coords) + (list(s.top.exterior.coords) if s.top else [(cx, yt)])
        s.body = MultiPoint(pts).convex_hull

    def r(s, y): return s.rt + (s.rb - s.rt) * (y - s.yt) / (s.yb - s.yt)

    def above(s, y):
        r = s.r(y)
        return unary_union([sbox(s.cx - 400, s.yt - 400, s.cx + 400, y), Polygon(ell(s.cx, y, r, r * s.k, 0, 360, 40))])

    def strip(s, f0, f1):
        y0 = s.yt - (s.rt * s.k if s.rt > 0 else 0); y1 = s.yb + s.rb * s.k + 1
        return Polygon([(s.cx + f0 * s.r(y0), y0), (s.cx + f1 * s.r(y0), y0), (s.cx + f1 * s.r(y1), y1), (s.cx + f0 * s.r(y1), y1)])

    def region(s, ya=None, yb=None):
        g = s.body
        if yb is not None: g = g.intersection(s.above(yb))
        if ya is not None: g = g.difference(s.above(ya))
        return g

    def paint(s, p, L, M, D, TOP=None, bands=(), hl=None):
        """سه پله: روشن چپ، میانی، تیره راست؛ نوارهای رنگی دور بدنه می‌پیچند."""
        def tri(g, l, m, d):
            gfill(p, g, m); gfill(p, g.intersection(s.strip(-1.1, -.32)), l); gfill(p, g.intersection(s.strip(.28, 1.1)), d)
        tri(s.body, L, M, D)
        for ya, yb, (l, m, d) in bands: tri(s.region(ya, yb), l, m, d)
        if hl: gfill(p, s.body.intersection(s.strip(-.8, -.62)).intersection(s.above(s.yb - 1)), hl)
        if s.top is not None and TOP: gfill(p, s.top, TOP)

    def front_arc(s, y=None, r=None, a0=0, a1=180):
        y = s.yb if y is None else y; r = s.r(y) if r is None else r
        return ell(s.cx, y, r, r * s.k, a0, a1, 24)

HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/floating_market'
XF = (1.0, 0.0, -8.0)
DECK = ('#c98a4a', '#eab677', '#8a5a2a'); CNT = ('#ffd84d', '#fff0a0', '#d9961c')
AW_W = ('#fff8e0', '#ffffff', '#d9cba0'); AW_R = ('#ef6a4a', '#ff9a7e', '#b53b24')
POST = '#8a5a2a'; NAVY_ = '#241a5e'
FRUIT = (('#ef6a4a', '#b53b24'), ('#ff9b2f', '#c46a10'), ('#8bd45a', '#4f9a2f'), ('#ffe14d', '#d9a020'))
BOB = 3


def fruit(p, x, y, r, c):
    disc(p, x, y, r, c[0])
    from shapely.geometry import Point
    gfill(p, Point(x, y).buffer(r, 16).difference(Point(x - r * .32, y - r * .3).buffer(r * .98, 16)), c[1])     # هلال سایه
    disc(p, x - r * .38, y - r * .38, r * .26, '#ffffff')
    p.shape(ell(x, y, r, r, 0, 360, 24), 'none', 2.3, j=0, step=99, clip=False)


def boat(p):
    DD = (16, -12)
    extrude(p, [(-62, 4), (46, 4), (42, 22), (-58, 22)], DD, DECK[0], DECK[1], DECK[2], mid=DECK[0], sw=M_OUT, sw_in=0)
    # ستون‌های غرفه (جزء جدا، خط نازک)
    for x in (-54, 44):
        p.shape([(x - 3, -62), (x + 3, -62), (x + 3, -3), (x - 3, -3)], POST, M_PART, j=0, step=6, clip=False)
    # پیشخوان
    extrude(p, [(-50, -14), (34, -14), (34, 0), (-50, 0)], (8, -6), CNT[0], CNT[1], CNT[2], mid=CNT[0], sw=M_OUT, sw_in=0)
    # یک جعبهٔ باز روی پیشخوان: داخل تیره، میوه‌ها از دهانه، دیوارهٔ جلو روی پایین میوه‌ها
    BX0, BX1 = -42, 24
    extrude(p, [(BX0, -22), (BX1, -22), (BX1, -8), (BX0, -8)], (7, -6), '#b9722f', '#4a2a10', '#7a4a1c', mid='#b9722f', sw=M_PART, sw_in=0)
    for i, c in enumerate(FRUIT):
        fruit(p, BX0 + 11 + i * 15, -30 - (i % 2) * 2, 8, c)
    p.shape([(BX0, -22), (BX1, -22), (BX1, -8), (BX0, -8)], '#b9722f', M_PART, j=0, step=6, clip=False)
    poly(p, [(BX0 + 3, -17), (BX1 - 3, -17), (BX1 - 3, -13.5), (BX0 + 3, -13.5)], '#e0a468')
    # سایبان راه‌راه: قاب سفید، راه‌راه قرمز روی جلو و رویه
    ax0, n, w, y0, y1, Dx, Dy = -56, 8, 12, -46, -60, 10, -12
    ext = extrude(p, [(ax0, y1), (ax0 + n * w, y1), (ax0 + n * w, y0), (ax0, y0)], (Dx, Dy), AW_W[0], AW_W[1], AW_W[2], mid=AW_W[0], sw=M_OUT, sw_in=0)
    for i in range(0, n, 2):
        xa, xb = ax0 + i * w, ax0 + (i + 1) * w
        poly(p, [(xa, y1), (xb, y1), (xb, y0), (xa, y0)], AW_R[0])                                            # جلو
        poly(p, [(xa, y1), (xb, y1), (xb + Dx, y1 + Dy), (xa + Dx, y1 + Dy)], AW_R[1])                        # رویه (راه‌راه می‌پیچد)
    poly(p, [(ax0 + n * w, y1), (ax0 + n * w + Dx, y1 + Dy), (ax0 + n * w + Dx, y0 + Dy), (ax0 + n * w, y0)], AW_W[2])   # پهلو
    p.stroke(ext, M_OUT, j=0, step=6)                                                                           # خط دور یکدست


def build(out=OUTD):
    p = Pen('floating_market', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-2, 24, 56); p.foot_tip(-2, 24, 30)
    with layer(p, 'boat'): boat(p)
    return p


STAND = None     # خودکار: find_stand

if __name__ == '__main__':
    p = build()
    offs = [p.V(o) for o in [(0, -BOB), (0, 0), (0, BOB)]]
    r = finish(p, 'floating_market', STAND, motion={'boat': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(offsets=offs, note='کل بلم، غرفه و میوه‌ها روی موج بالا و پایین؛ سکو ثابت؛ سایهٔ تماس ثابت')
    (OUTD / 'floating_market.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'inside': r['inside'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
