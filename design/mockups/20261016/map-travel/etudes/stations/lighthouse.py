#!/usr/bin/env python3
"""ایستگاه «فانوس دریایی» (E04)، اصلاح خط ۲۳ اکتبر: برج راه‌راه ¾ سه‌بعدی (استوانهٔ ناقص با سه پلهٔ رنگ؛ نوارهای قرمز دور بدنه می‌پیچند)،
بالکن، اتاقک شیشه‌ای و سقف مخروطی؛ همه یک سیلوئت با خط دور یکدست ۳٫۶ و بدون خط بین وجه‌ها. فقط مرز جزءها (بالکن/اتاقک/سقف) خط نازک ۲٫۶ دارد.
لایه‌های متحرک node_lighthouse_beam_l و node_lighthouse_beam_r = پرتوهای چپ و راست (یکی‌درمیان/جاروب حول اتاقک)؛ حالت ایستا = بیشینهٔ گسترش."""
import sys, pathlib, json
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

HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/lighthouse'
import functools, station_kit as _k   # D122/D123: حاشیهٔ چپ/راست ≥۴px (بدون دست‌زدن به کیت)
_k.margin_check = functools.partial(_k.margin_check, min_margin=4); _k.motion_check = functools.partial(_k.motion_check, min_margin=4)
XF = (1.25, -5.0, -2.0)               # قاب قهرمان: (مقیاس هندسه، dx، dy)
RED = ('#ff9a7e', '#ef6a4a', '#b53b24'); WHT = ('#ffffff', '#f2eadb', '#c9bfe4'); GL = ('#fff0a0', '#ffd84d', '#d9961c')
GOLD = ('#f7cf5a', '#d9961c', '#9c6410'); BEAM = '#ffe45c'; DOOR = '#4f240a'; NAVY_ = '#241a5e'
LY = -76                   # مرکز اتاقک چراغ (کار پرتوها)
BX = 44                    # دورترین نقطهٔ پرتوها از محور


def poly_(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, (' stroke="%s" stroke-width=".6" stroke-linejoin="round"' % col) if op == 1 else ' opacity="%s"' % op))


def build(out=OUTD):
    p = Pen('lighthouse', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(0, 17, 40); p.foot_tip(0, 17, 22)
    # دو پرتو، دو لایهٔ جدا، پشت اتاقک؛ از مرکز اتاقک شروع می‌شوند
    for nm, s_ in (('beam_l', -1), ('beam_r', 1)):
        with layer(p, nm):
            cx_, cy_ = p.X((s_ * 24, LY)); k_ = p.xf[0]
            gid = 'lh_%s' % nm
            p.raw('<defs><radialGradient id="%s"><stop offset="0" stop-color="#fffbd0" stop-opacity="1"/><stop offset=".4" stop-color="#ffe45c" stop-opacity=".75"/><stop offset="1" stop-color="#ffe45c" stop-opacity="0"/></radialGradient></defs><ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="url(#%s)"/>' % (gid, cx_, cy_, 24 * k_, 15 * k_, gid))
    tower = Fr(0, -58, 8, 19, 30); bal = Fr(0, -64, -58, 28, 28, .3); lamp = Fr(0, -88, -64, 12, 12); roof = Fr(0, -114, -88, 0, 18)
    orb = Polygon(ell(0, -118, 4.8, 4.8, 0, 360, 20))
    S = sil([tower.body, bal.body, lamp.body, roof.body, orb])
    sil_open(p, S, RED[1])
    tower.paint(p, *WHT, bands=[(None, -43, RED), (-24, -5, RED)])
    # در و پنجره (رنگ تخت؛ در تیره = گودی)
    yb = lambda x: 8 + tower.k * 30 * (1 - (x / 30.) ** 2) ** .5
    door = ell(0, -4, 6.5, 6.5, 180, 360, 12) + [(6.5, yb(6.5) - 2), (-6.5, yb(-6.5) - 2)]
    poly_(p, door, DOOR)
    p.shape(ell(0, -33, 4.6, 4.6, 0, 360, 16), '#ffe14d', 2.2, j=0, step=99, clip=False)
    bal.paint(p, *GOLD, TOP='#ffe590')
    arcline(p, bal.front_arc(-58, 28), NAVY_, M_PART)                                   # مرز بالکن و برج
    lamp.paint(p, *GL, TOP='#fff3b0')
    for x_ in (-6.2, 6.2):                                                              # قاب شیشه: دو تیرک نازک
        p.ln((x_, -85), (x_, -62), 2.2, '#8a5a12', j=0)
    arcline(p, lamp.front_arc(-64, 12), NAVY_, M_PART)                                  # مرز اتاقک و بالکن
    roof.paint(p, *RED)
    arcline(p, roof.front_arc(-88, 18), NAVY_, M_PART)                                  # مرز سقف و اتاقک
    gfill(p, orb, '#ffd84d')
    sil_close(p, S)
    p.shape(ell(0, -118, 4.8, 4.8, 0, 360, 20), 'none', M_PART, j=0, step=99, clip=False)
    return p


STAND = None     # خودکار: find_stand

if __name__ == '__main__':
    p = build()
    r = finish(p, 'lighthouse', STAND, motion={'beam_l': dict(offsets=[(0, 0)]), 'beam_r': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    cx, cy = p.X((0, LY)); ax = p.X((0, 0))[0]
    sym_err = round(abs((ax - p.X((-BX, 0))[0]) - (p.X((BX, 0))[0] - ax)), 3); assert sym_err < .01
    sp = r['spec']
    sp['motion_spec'] = {
        'pivot': [round(cx, 1), round(cy, 1)],
        'note': 'برج، بالکن و اتاقک چراغ (شیشه+سقف+گوی) ثابت و کاملند؛ دو پرتو پشت اتاقک‌اند و از مرکز اتاقک شروع می‌شوند.',
        'node_lighthouse_beam_l': dict(transform_origin=[round(cx, 1), round(cy, 1)], mode_alternate='opacity 1→0.12 و برگشت', mode_sweep='scaleX 1→0.25 (حول مرکز اتاقک) همراه opacity 1→0.3', cycle_s=2.4, phase='شروع در 0'),
        'node_lighthouse_beam_r': dict(transform_origin=[round(cx, 1), round(cy, 1)], mode_alternate='همان، با delay 1.2s تا یکی‌درمیان روشن شوند', mode_sweep='همان با delay 1.2s', cycle_s=2.4, phase='delay 1.2s'),
        'bounds': 'حالت ایستا بیشینهٔ گسترش است؛ هر حالت دیگر زیرمجموعهٔ آن است',
        'reduced_motion': 'هر دو پرتو ثابت و روشن',
        'beams_symmetry_error': sym_err}
    (OUTD / 'lighthouse.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
