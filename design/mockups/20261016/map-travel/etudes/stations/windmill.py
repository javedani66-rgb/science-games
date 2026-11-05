#!/usr/bin/env python3
"""ایستگاه E01 «آسیاب بادی» (سرزمین مزرعه)، اصلاح خط ۲۳ اکتبر: برج کرم ¾ سه‌بعدی (استوانهٔ ناقص، سه پلهٔ رنگ)، سقف مخروطی قهوه‌ای (سه پله)،
چهار پرهٔ پارچه‌ای با تیرک چوبی که با محور یک سیلوئت می‌شوند (اتصال = یک شکل). خط دور یکدست ۳٫۶، بدون خط بین وجه‌ها؛ فقط مرز سقف/برج و حلقهٔ محور خط نازک ۲٫۶ دارد.
لایهٔ دوّار: node_windmill_blades (مرکز = محور). حالت ایستا = ضربدر ×؛ بدون حلقهٔ بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from station_kit import *

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

OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/windmill'
import functools, station_kit as _k
_k.margin_check = functools.partial(_k.margin_check, min_margin=4); _k.motion_check = functools.partial(_k.motion_check, min_margin=4)

TW = ('#fffdf2', '#f3e2bd', '#cdb27c')       # برج: روشن / میانی / تیره
RF = ('#b97a40', '#8d5226', '#5b2e12')       # سقف
CL = ('#ff9d84', '#ef6a4a', '#b53b24')       # پارچهٔ پره
SPAR = '#6b3f17'; DOOR = '#4f240a'; GLASS = '#cfeaff'; YEL = '#ffd84d'; NAVY_ = '#241a5e'
XF = (1.15, -5.0, 2.0)
HUB = (0, -54); R = 50; CW = 16; STATIC = (-135, -45, 45, 135)


def build(out=OUTD):
    p = Pen('windmill', 'farm'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    p.tipshadow(2, 12, 34); p.foot_tip(0, 12, 22)
    tower = Fr(0, -78, 8, 20, 31); roof = Fr(0, -106, -78, 0, 25)
    S = sil([tower.body, roof.body])
    sil_open(p, S, TW[1])
    tower.paint(p, *TW)
    yb = lambda x: 8 + tower.k * 30 * (1 - (x / 30.) ** 2) ** .5
    poly(p, ell(0, -4, 7, 7, 180, 360, 12) + [(7, yb(7) - 2), (-7, yb(-7) - 2)], DOOR)          # در: گودی تیره
    roof.paint(p, *RF)
    arcline(p, roof.front_arc(-78, 25), NAVY_, M_PART)                                            # مرز سقف و برج
    sil_close(p, S)
    # پره‌ها: یک سیلوئت (پارچه‌ها + تیرک‌ها + محور)
    with layer(p, 'blades'):
        sails = []; cl = []; sp = []
        for a in STATIC:
            f = rot(HUB[0], HUB[1], a)
            sails.append(Polygon(TP(f, [(8, -CW), (R, -CW), (R, 0), (8, 0)])))
            sp.append(Polygon(TP(f, [(3, -1.5), (R, -1.5), (R, 3.5), (3, 3.5)])))
        hubp = Polygon(ell(HUB[0], HUB[1], 8.5, 8.5, 0, 360, 24))
        SB = sil(sails + sp + [hubp])
        sil_open(p, SB, CL[1])
        for a in STATIC:
            f = rot(HUB[0], HUB[1], a)
            poly(p, TP(f, [(8, -CW), (R, -CW), (R, -CW * .62), (8, -CW * .62)]), CL[0])          # لبهٔ روشن
            poly(p, TP(f, [(8, -CW * .3), (R, -CW * .3), (R, -1), (8, -1)]), CL[2])               # لبهٔ سایه
        for a in STATIC:
            f = rot(HUB[0], HUB[1], a)
            poly(p, TP(f, [(3, -1.5), (R, -1.5), (R, 3.5), (3, 3.5)]), SPAR)             # تیرک چوبی
        gfill(p, hubp, SPAR)
        sil_close(p, SB)
        p.shape(ell(HUB[0], HUB[1], 8.5, 8.5, 0, 360, 24), 'none', M_PART, j=0, step=99, clip=False)   # مرز محور و پره‌ها
        disc(p, HUB[0], HUB[1], 2.6, YEL)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    hm = p.X(HUB)
    r = finish(p, 'windmill', STAND, motion={'blades': dict(rotate=hm)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_windmill_blades': dict(center=[round(v, 1) for v in hm], dir='cw (جهت عقربه‌های ساعت)', turns=3,
                                                     note='چهار پرهٔ پارچه‌ای حول محور؛ حالت ایستا = ضربدر ×؛ چرخش آهسته فقط هنگام رسیدن؛ بدون حلقهٔ بیکار.'),
                         'reduced_motion': 'پره‌ها ثابت در حالت ضربدر ×'}
    (OUTD / 'windmill.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
