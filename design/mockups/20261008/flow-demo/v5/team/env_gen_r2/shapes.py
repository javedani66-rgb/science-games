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
# ---- r2: پایهٔ هر گره = قطعهٔ خط‌دار (v4: slab) ولی با ۸ شکل متفاوت؛ خط دور 4.5 (مهم)، جزئیات 1.2/2.6 ----
# (top, side, tick) برای هر زمین و شکل؛ رنگ‌ها از پالت v4
PATCH = {
 'sports': dict(disc=('#c9f5ad', '#2c7a2a', '#7fd06a'), plate=('#e9e4d6', '#a8a49a', '#c6c1b6'), hex=('#fff3c4', '#c4502f', '#e5496e'), mound=('#6fcf5e', '#2c7a2a', '#9be08a'),
                rock=('#cfd3e2', '#6e72a8', '#9a9fc6'), deck=('#e2a95d', '#a8672f', '#c98a45'), tier=('#9be08a', '#2c7a2a', '#c9f5ad'), pond=('#f4fcff', '#9fd0f0', '#6bb6ee')),
 'space': dict(disc=('#c9cfe6', '#6e72a8', '#9a9fc6'), plate=('#d6dbef', '#6e72a8', '#f4f6ff'), hex=('#f4f6ff', '#8a90c0', '#7fd4ff'), mound=('#e08a5f', '#8e2c1a', '#f0a77f'),
               rock=('#b9a3b0', '#6e4a5a', '#d6c0c8'), deck=('#9a9fc6', '#4b4f8a', '#c9cfe6'), tier=('#d6dbef', '#6e72a8', '#fff'), pond=('#7fd4ff', '#2d62e8', '#fff')),
 'farm': dict(disc=('#f4e6a0', '#8a7a2a', '#d4c26a'), plate=('#e8c64a', '#8a7a2a', '#f4e6a0'), hex=('#f4e6a0', '#a8672f', '#e2a95d'), mound=('#8fcf4e', '#3a6a1a', '#b9e87a'),
              rock=('#c9b38a', '#6e5a3a', '#e0cfa8'), deck=('#e2a95d', '#a8672f', '#c98a45'), tier=('#f4e6a0', '#8a7a2a', '#fff3c4'), pond=('#58d8ee', '#1f87b8', '#d4f6ff')),
 'city': dict(disc=('#f6dba0', '#a8672f', '#e9c27a'), plate=('#cfd3e2', '#6e72a8', '#e9e4d6'), hex=('#e9e4d6', '#6e72a8', '#ffd23f'), mound=('#c9b38a', '#6e5a3a', '#e0cfa8'),
              rock=('#a8a49a', '#5a5666', '#c6c1b6'), deck=('#c98a45', '#8f5a2e', '#e2a95d'), tier=('#f6dba0', '#a8672f', '#fff3c4'), pond=('#58d8ee', '#075a73', '#d4f6ff')),
}
PATCH['dirt'] = PATCH['farm']
SHAPES = ['disc', 'plate', 'hex', 'rock', 'deck', 'mound', 'tier', 'pond']
# شکل پایهٔ بناها (None = بنا پایهٔ خودش را دارد)
BASE_OF = {'node_01': ('city', 'deck'), 'node_02': None, 'node_03': None, 'node_04': ('space', 'hex'), 'node_05': ('space', 'rock'), 'node_06': ('space', 'tier'),
           'node_07': ('city', 'plate'), 'node_08': ('farm', 'mound'), 'node_09': ('farm', 'tier'), 'node_10': ('city', 'deck'), 'node_11': ('city', 'plate'), 'node_12': None}
def jag(rx, ry, n, a, seed):
    r = random.Random(seed); out = []
    for i in range(n):
        t = 2 * math.pi * i / n; k = 1 + r.uniform(-a, a); out.append((rx * k * math.cos(t), ry * k * math.sin(t)))
    return out
def pad(b, zone, rx, seed=3, shape=None):
    zone = BASE_OF.get(b.pre, (zone, None))[0] if b.pre in BASE_OF and BASE_OF[b.pre] else zone
    if b.pre in BASE_OF:
        if BASE_OF[b.pre] is None:       # بنا پایهٔ خودش را دارد؛ فقط سایهٔ نرم
            return
        shape = BASE_OF[b.pre][1]
    shape = shape or SHAPES[seed % len(SHAPES)]
    top, side, tick = PATCH[zone][shape]; r = random.Random(seed * 13 + 5); ry = rx * .36; h = 9 if rx < 50 else 12; W = 4.5
    if shape == 'disc':
        b.ell(0, h, rx, ry, side, W); b.ell(0, 0, rx, ry, top, W)
        b.path('M%s,%sq%s,%s %s,0' % (f(-rx * .5), f(ry * .2), f(rx * .25), f(-ry * .35), f(rx * .45)), 'none', 1.2, clip=False)
    elif shape == 'plate':      # سنگ‌فرش لوزی‌مانند
        P = [(-rx, 0), (-rx * .25, -ry * 1.05), (rx * .8, -ry * .85), (rx, 0), (rx * .3, ry * 1.05), (-rx * .75, ry * .85)]
        b.poly([(x, y + h) for x, y in P], side, W); b.poly(P, top, W)
        b.line(-rx * .5, 0, rx * .45, -ry * .2, tick, 1.2); b.line(-rx * .2, ry * .5, rx * .55, ry * .3, tick, 1.2)
    elif shape == 'hex':
        P = [(rx * math.cos(math.pi / 3 * k), ry * 1.05 * math.sin(math.pi / 3 * k)) for k in range(6)]
        b.poly([(x, y + h + 2) for x, y in P], side, W); b.poly(P, top, W)
        b.poly([(x * .55, y * .55) for x, y in P], 'none', 1.2); b.circ(0, 0, 2.6, tick, 0)
    elif shape == 'rock':       # تکهٔ سنگ ناهموار با رخ‌های تیز
        P = jag(rx, ry * 1.1, 9, .18, seed); b.poly([(x, y + h + 4) for x, y in P], side, W); b.poly(P, top, W)
        b.poly([P[1], P[2], (P[2][0] * .5, P[2][1] * .4 + 2), (P[1][0] * .4, P[1][1] * .4)], tick, 0, clip=False)
        b.line(P[4][0] * .6, P[4][1] * .6, P[5][0] * .3, P[5][1] * .3, side, 1.2)
    elif shape == 'deck':       # عرشهٔ تخته‌ای (اسکله)
        w2 = rx * .95; hh = ry * 1.05
        b.rect(-w2, -hh + h, 2 * w2, 2 * hh, side, W, 5); b.rect(-w2, -hh, 2 * w2, 2 * hh, top, W, 5)
        for k in range(-3, 4): b.line(k * w2 / 3.4, -hh + 2, k * w2 / 3.4, hh - 2, tick, 1.2)
        for sx in (-1, 1): b.circ(sx * (w2 - 6), -hh + 6, 2.6, side, 0)
    elif shape == 'mound':      # تپهٔ کوچک
        b.ell(0, ry * .4 + h, rx, ry * .55, side, W)
        b.path('M%s,%s Q%s,%s 0,%s Q%s,%s %s,%s Z' % (f(-rx), f(ry * .4 + h), f(-rx * .9), f(-ry * 1.8), f(-ry * 1.9), f(rx * .9), f(-ry * 1.8), f(rx), f(ry * .4 + h)), top, W)
        b.line(-rx * .3, -ry * .8, -rx * .1, -ry * .3, tick, 1.2); b.line(rx * .35, -ry * .9, rx * .5, -ry * .4, tick, 1.2)
    elif shape == 'tier':       # دو طبقه
        b.ell(0, h + 6, rx, ry, side, W); b.ell(0, 6, rx, ry, top, W); b.ell(0, 0 + 2, rx * .66, ry * .66, side, W); b.ell(0, -4, rx * .66, ry * .66, top, W)
    elif shape == 'pond':       # لکهٔ آبی/یخی داخل لبهٔ بالا (برکه)
        b.ell(0, h, rx, ry, side, W); b.ell(0, 0, rx, ry, top, W); b.ell(0, 0, rx * .6, ry * .55, tick, 0, clip=False); b.line(-rx * .3, -2, rx * .1, -3, '#fff', 1.2)
