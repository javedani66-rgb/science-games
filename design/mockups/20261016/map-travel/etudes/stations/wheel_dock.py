#!/usr/bin/env python3
"""ایستگاه «بارانداز» (اصلاح خط ۲۳ اکتبر): قهرمان = چرخ‌دستیِ بارکش ¾ سه‌بعدی روی سکوی دریایی. سه جزء درشت:
۱) کفِ چرخ‌دستی (جعبهٔ ¾ با رویه/جلو/پهلو) + دستهٔ بلند؛ ۲) بار = صندوق بزرگ زرد با ضربدر نازک و بشکهٔ قهوه‌ای با دو حلقهٔ آهنی؛ ۳) دو چرخ هم‌اندازه و دارای فاصله.
بین وجه‌ها خط نیست (فقط پلهٔ رنگ)؛ خط دور اصلی ۳٫۶، فرعی ۲٫۶ (دسته، ضربدر، پره‌ها).
لایه‌های متحرک (چرخش حول مرکز خودش): node_wheel_dock_wheel = چرخ راست (id قدیمی)، node_wheel_dock_wheel_back = چرخ چپ. چرخ‌ها دایره‌اند و در هر زاویه از سکو بیرون نمی‌زنند."""
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

from shapely.geometry import LineString
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/wheel_dock'
XF = (1.0, 6.0, -8.0)
BED = ('#c98a3a', '#f0c070', '#8a5a1e')            # جلو / رویه / پهلو
CR = ('#ffd84d', '#fff0a0', '#d9961c'); CR_X = '#c98512'
BAR = ('#d29255', '#a8672f', '#6e3f17'); IRON = ('#e4ebf7', '#aab6d3', '#6c7aa0')
HAND = '#ffd84d'; NAVY_ = '#241a5e'
TIRE = '#3b3380'; RIM = '#7b8fe0'; RIM_L = '#a9b8f2'; SPK = '#fff3c4'
R = 14; WY = 6; WX = (-36, 18)


def wheel(p, cx):
    disc(p, cx, WY, R, TIRE)
    disc(p, cx, WY, R - 4.5, RIM)
    for a in (0, 60, 120):
        t = math.radians(a + 25)
        p.ln((cx - (R - 5) * math.cos(t), WY - (R - 5) * math.sin(t)), (cx + (R - 5) * math.cos(t), WY + (R - 5) * math.sin(t)), 3.2, SPK, j=0)
    disc(p, cx, WY, 4.2, NAVY_); disc(p, cx, WY, 1.8, '#ffd84d')
    p.shape(ell(cx, WY, R, R, 0, 360, 40), 'none', M_OUT, j=0, step=99, clip=False)


def build(out=None):
    p = Pen('wheel_dock', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    for cx in WX:
        p.tipshadow(cx, WY + R - 1, 15); p.foot_tip(cx, WY + R - 2, 8)
    # ۱) دسته (پشت کف)، سپس کف
    h1 = LineString([(-50, -6), (-68, -34)]).buffer(3.4); h2 = LineString([(-74, -35), (-62, -35)]).buffer(3.6)
    HS = sil([h1, h2])
    sil_open(p, HS, HAND, M_PART); sil_close(p, HS, M_PART)
    extrude(p, [(-56, -14), (38, -14), (38, 6), (-56, 6)], (14, -11), BED[0], BED[1], BED[2], mid=BED[0], sw=M_OUT, sw_in=0)
    # ۲) بار: صندوق و بشکه
    extrude(p, [(-46, -58), (-8, -58), (-8, -18), (-46, -18)], (12, -9), CR[0], CR[1], CR[2], mid=CR[0], sw=M_OUT, sw_in=0)
    p.ln((-42, -54), (-12, -22), 2.6, CR_X, j=0); p.ln((-12, -54), (-42, -22), 2.6, CR_X, j=0)
    bar = Fr(26, -56, -20, 15, 15)
    BS = sil([bar.body, bar.top])
    sil_open(p, BS, BAR[1])
    bar.paint(p, *BAR[:3] if False else (BAR[0], BAR[1], BAR[2]), TOP='#e8b57c', bands=[(-52, -48, IRON), (-32, -28, IRON)])
    sil_close(p, BS)
    # ۳) چرخ‌ها (هم‌اندازه، با فاصله؛ لایهٔ متحرک)
    with layer(p, 'wheel_back'): wheel(p, WX[0])
    with layer(p, 'wheel'): wheel(p, WX[1])
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    mo = {'wheel': dict(rotate=p.X((WX[1], WY))), 'wheel_back': dict(rotate=p.X((WX[0], WY)))}
    r = finish(p, 'wheel_dock', STAND, motion=mo, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(wheel=dict(layer='node_wheel_dock_wheel', rotate_about=[round(v, 1) for v in p.X((WX[1], WY))], note='چرخ راست؛ id قدیمی حفظ شد'),
                                             wheel_back=dict(layer='node_wheel_dock_wheel_back', rotate_about=[round(v, 1) for v in p.X((WX[0], WY))], note='چرخ چپ، لایهٔ جدید'))
    (OUTD / 'wheel_dock.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'inside': r['inside'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
