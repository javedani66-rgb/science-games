# ابزار شکل: هر شکل هم نسخهٔ رنگی دارد هم هندسهٔ لخت (برای clip نور/سایه)
import math, random
REG = {}
CSS = '<style>.eo{stroke:var(--l-line,#241a5e);stroke-linejoin:round;stroke-linecap:round}.elit{fill:var(--l-lit,#fff4cf);opacity:.3}.esh{fill:var(--l-shade,#4a3a8c);opacity:.22}.ew{fill:var(--l-windows,transparent);opacity:var(--l-windows-opacity,0)}.esd{fill:var(--l-shadow-color,#10083a);opacity:var(--l-shadow-opacity,.28)}</style>'
def f(x): return ('%.1f' % x).rstrip('0').rstrip('.')
class B:
    """سازندهٔ یک نماد: لایه‌های shadow/base/lit/shade/windows"""
    def __init__(s, pre): s.pre = pre; s.base = []; s.clip = []; s.win = []
    def _add(s, geo, fill, w, clip=True, extra=''):
        st = ('fill="%s" class="eo" stroke-width="%s"' % (fill, w)) if w else 'fill="%s"' % fill
        s.base.append('<%s %s %s/>' % (geo[0], geo[1], st + (' ' + extra if extra else '')))
        if clip and fill != 'none': s.clip.append('<%s %s/>' % geo)
    def poly(s, pts, fill, w=4.5, **k): s._add(('polygon', 'points="%s"' % ' '.join('%s,%s' % (f(x), f(y)) for x, y in pts)), fill, w, **k)
    def rect(s, x, y, wd, h, fill, w=4.5, r=3, rot=None, **k):
        g = 'x="%s" y="%s" width="%s" height="%s" rx="%s"' % (f(x), f(y), f(wd), f(h), r)
        if rot is not None: g += ' transform="rotate(%s %s %s)"' % (rot[0], f(rot[1]), f(rot[2]))
        s._add(('rect', g), fill, w, **k)
    def ell(s, cx, cy, rx, ry, fill, w=4.5, **k): s._add(('ellipse', 'cx="%s" cy="%s" rx="%s" ry="%s"' % (f(cx), f(cy), f(rx), f(ry))), fill, w, **k)
    def circ(s, cx, cy, r, fill, w=4.5, **k): s._add(('circle', 'cx="%s" cy="%s" r="%s"' % (f(cx), f(cy), f(r))), fill, w, **k)
    def path(s, d, fill='none', w=4.5, **k): s._add(('path', 'd="%s"' % d), fill, w, **k)
    def line(s, x1, y1, x2, y2, col='var(--l-line,#241a5e)', w=2.6):
        s.base.append('<path d="M%s,%sL%s,%s" fill="none" stroke-linecap="round" style="stroke:%s" stroke-width="%s"/>' % (f(x1), f(y1), f(x2), f(y2), col, w))
    def raw(s, x): s.base.append(x)
    def window(s, x, y, wd, h, r=2): s.win.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" class="ew"/>' % (f(x), f(y), f(wd), f(h), r))
    def wcirc(s, x, y, r): s.win.append('<circle cx="%s" cy="%s" r="%s" class="ew"/>' % (f(x), f(y), f(r)))
    def svg(s, vb, ox, oy, rx, ry, bbox, windows=True):
        """ox,oy = جای مرکز پایه در viewBox؛ bbox=(x0,y0,x1,y1) محلی برای نوار نور"""
        p = s.pre; x0, y0, x1, y1 = bbox; wd = x1 - x0; REG[p] = list(s.clip)
        tr = 'transform="translate(%s %s)"' % (ox, oy)
        o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s">' % vb, CSS,
             '<defs><clipPath id="%s_clip">%s</clipPath></defs>' % (p, ''.join(s.clip)),
             '<g id="%s_shadow" %s><ellipse cx="8" cy="6" rx="%s" ry="%s" class="esd"/></g>' % (p, tr, f(rx + 6), f(ry + 2)),
             '<g id="%s_base" %s>%s</g>' % (p, tr, ''.join(s.base)),
             '<g id="%s_lit" %s clip-path="url(#%s_clip)"><polygon points="%s,%s %s,%s %s,%s %s,%s" class="elit"/></g>' % (p, tr, p, f(x0 - 4), f(y0 - 4), f(x0 + wd * .3), f(y0 - 4), f(x0 + wd * .12), f(y1 + 30), f(x0 - 4), f(y1 + 30)),
             '<g id="%s_shade" %s clip-path="url(#%s_clip)"><polygon points="%s,%s %s,%s %s,%s %s,%s" class="esh"/></g>' % (p, tr, p, f(x0 + wd * .68), f(y0 - 4), f(x1 + 4), f(y0 - 4), f(x1 + 4), f(y1 + 30), f(x0 + wd * .5), f(y1 + 30))]
        if windows and s.win: o.append('<g id="%s_windows" %s>%s</g>' % (p, tr, ''.join(s.win)))
        o.append('</svg>'); return ''.join(o)
def jig(pts, a, seed):
    r = random.Random(seed); return [(x + r.uniform(-a, a), y + r.uniform(-a, a)) for x, y in pts]
def blob(rx, ry, n=14, a=.06, seed=1):
    r = random.Random(seed); pts = []
    for i in range(n):
        t = 2 * math.pi * i / n; k = 1 + r.uniform(-a, a)
        pts.append((rx * k * math.cos(t), ry * k * math.sin(t)))
    d = 'M%s,%s' % (f(pts[0][0]), f(pts[0][1]))
    for i in range(n):
        p1, p2 = pts[i], pts[(i + 1) % n]; m = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        d += ' Q%s,%s %s,%s' % (f(p1[0]), f(p1[1]), f(m[0]), f(m[1]))
    return d + 'Z'
# ---- r2b: پایهٔ هر گره = یکی از ۳ نوع v4: سنگ / فلز / یخ؛ لبهٔ ضخیم 5.5، دیوارهٔ بلند، سایهٔ قرصی ----
# سنگ رنگ زمین دارد (رنگ‌های slab v4)؛ فلز و یخ ثابت‌اند. (top, side, tick)
STONE = {'sports': ('#c9f5ad', '#2c7a2a', '#7fd06a'), 'space': ('#d6dbef', '#6e72a8', '#9a9fc6'), 'farm': ('#f4e6a0', '#8a7a2a', '#d4c26a'), 'city': ('#cfd3e2', '#6e72a8', '#9a9fc6')}
STONE['dirt'] = STONE['farm']
METAL = ('#aeb9dc', '#3a3f86', '#e6ebff'); ICEP = ('#f4fcff', '#7fc0e6', '#bfe6fa')
SHAPES = ['stone', 'metal', 'ice']
ORDER_BY_ZONE = {'sports': ['stone', 'ice', 'metal'], 'space': ['metal', 'stone', 'ice'], 'farm': ['stone', 'metal'], 'yard': ['metal', 'stone'], 'sea': ['stone', 'ice', 'metal']}   # یخ فقط در ورزشگاه/فضا/دریا (در مزرعه و حیاط شنی بی‌معنی است)
# شکل پایهٔ بناها (None = بنا پایهٔ خودش را دارد)
BASE_OF = {'node_01': ('city', 'stone'), 'node_02': None, 'node_03': None, 'node_04': ('space', 'metal'), 'node_05': ('space', 'stone'), 'node_06': ('space', 'metal'),
           'node_07': ('city', 'stone'), 'node_08': ('farm', 'stone'), 'node_09': ('farm', 'stone'), 'node_10': None, 'node_11': None, 'node_12': None}
def jag(rx, ry, n, a, seed):
    r = random.Random(seed); out = []
    for i in range(n):
        t = 2 * math.pi * i / n; k = 1 + r.uniform(-a, a); out.append((rx * k * math.cos(t), ry * k * math.sin(t)))
    return out
def _slab(b, P, h, top, side, W, tick_lines=(), inner=None):
    """P: نقطه‌ها به ترتیب زاویه (۰=راست، رو به پایین)؛ دیوارهٔ جلویی = نیمهٔ پایینی منتقل‌شده."""
    n = len(P); lo = P[:n // 2 + 1]
    b.poly(lo + [(x, y + h) for x, y in reversed(lo)], side, W); b.poly(P, top, W)
def pad(b, zone, rx, seed=3, shape=None):
    zone = BASE_OF.get(b.pre, (zone, None))[0] if b.pre in BASE_OF and BASE_OF[b.pre] else zone
    if b.pre in BASE_OF:
        if BASE_OF[b.pre] is None:       # بنا پایهٔ خودش را دارد
            return
        shape = BASE_OF[b.pre][1]
    shape = shape if shape in SHAPES else SHAPES[seed % 3]
    ry = rx * .38; h = 14 if rx < 55 else 17; W = 5.5
    b.raw('<ellipse cx="7" cy="%s" rx="%s" ry="%s" fill="#10083a" opacity=".3"/>' % (f(h + 7), f(rx + 8), f(ry + 3)))        # سایهٔ قرصی (v4)
    if shape == 'stone':
        top, side, tick = STONE[zone]; P = jag(rx, ry, 14, .06, seed * 7 + 1)
        _slab(b, P, h, top, side, W)
        b.line(-rx * .55, ry * .1, -rx * .2, ry * .35, tick, 2.6); b.line(rx * .25, -ry * .3, rx * .6, -ry * .05, tick, 2.6)
        b.path('M%s,%sl%s,%s%s,%s' % (f(-rx * .1), f(ry * .55), f(rx * .08), f(ry * .2), f(rx * .1), f(-ry * .15)), 'none', 1.2, clip=False)
        b.circ(rx * .5, ry * .3, 2.6, side, 0, clip=False); b.circ(-rx * .62, -ry * .1, 2, side, 0, clip=False); b.circ(rx * .1, -ry * .45, 1.8, side, 0, clip=False)
    elif shape == 'metal':     # صفحهٔ هشت‌ضلعی فولادی با پیچ و درز
        top, side, tick = METAL
        P = [(rx * math.cos(math.pi / 4 * k + math.pi / 8 - math.pi / 8), ry * 1.04 * math.sin(math.pi / 4 * k)) for k in range(8)]
        _slab(b, P, h + 1, top, side, W)
        b.poly([(x * .72, y * .72) for x, y in P], 'none', 2.6)
        b.line(-rx * .72, 0, rx * .72, 0, tick, 1.2); b.line(0, -ry * .75, 0, ry * .75, tick, 1.2)
        for x, y in P: b.circ(x * .86, y * .86, 2.8, tick, 1.2, clip=False)
    elif shape == 'ice':       # قطعهٔ یخ تیز و شکافدار
        top, side, tick = ICEP
        P = []
        for k in range(14):
            t = 2 * math.pi * k / 14; rr = rx * (1.04 if k % 2 == 0 else .84) * (1 + random.Random(seed * 5 + k).uniform(-.05, .05)); P.append((rr * math.cos(t), rr * ry / rx * math.sin(t) * 1.08))
        _slab(b, P, h + 1, top, side, W)
        b.poly([P[10], P[11], (P[11][0] * .45, P[11][1] * .4), (P[10][0] * .4, P[10][1] * .4)], '#c9ecfb', 0, clip=False)
        b.poly([P[2], P[3], (P[3][0] * .5, P[3][1] * .45), (P[2][0] * .45, P[2][1] * .4)], '#c9ecfb', 0, clip=False)
        b.path('M%s,%sL%s,%sL%s,%sL%s,%s' % (f(-rx * .45), f(-ry * .2), f(-rx * .15), f(ry * .2), f(-rx * .22), f(ry * .6), f(rx * .08), f(ry * .85)), 'none', 1.4, clip=False, extra='style="stroke:#4a9cc8"')
        b.line(rx * .2, -ry * .35, rx * .48, -ry * .1, '#fff', 2)
