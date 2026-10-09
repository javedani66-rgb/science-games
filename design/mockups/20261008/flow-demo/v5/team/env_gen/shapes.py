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
# لکهٔ زمینِ هم‌زون زیر بنا (بدون خط، بدون دیسک)؛ سایه با esd در svg()
PATCH = {'sports': ('#a6d86a', '#66993b', '#7fbf4a'), 'space': ('#9a7ee0', '#5c459c', '#b9a3f0'), 'farm': ('#ece2ae', '#aba16e', '#c7a56a'), 'city': ('#7a93ae', '#44566c', '#9db3c9'), 'dirt': ('#c7a56a', '#9b7a48', '#e0c48a')}
def pad(b, zone, rx, seed=3):
    r = random.Random(seed * 7 + len(zone)); ry = rx * r.uniform(.27, .38); patch, shade, tick = PATCH[zone]; dx = r.uniform(-4, 4)
    b.raw('<path transform="translate(%s %s)" d="%s" fill="%s" opacity=".75"/>' % (f(dx + 5), f(7), blob(rx * 1.04, ry * 1.04, 13, .1, seed), shade))
    b.raw('<path transform="translate(%s 0)" d="%s" fill="%s"/>' % (f(dx), blob(rx, ry, 13, .1, seed + 1), patch))
    for k in range(3):
        x = r.uniform(-rx * .7, rx * .7); y = r.uniform(-ry * .5, ry * .6)
        if zone == 'sports': b.raw('<path d="M%s,%sl-2,-6M%s,%sl2,-6" stroke="%s" stroke-width="1.2" stroke-linecap="round" fill="none"/>' % (f(x), f(y), f(x + 3), f(y), shade))
        elif zone == 'space': b.raw('<ellipse cx="%s" cy="%s" rx="4" ry="1.8" fill="%s"/>' % (f(x), f(y), shade))
        elif zone in ('farm', 'dirt'): b.raw('<path d="M%s,%sl7,-1" stroke="%s" stroke-width="1.2" stroke-linecap="round"/>' % (f(x), f(y), shade))
        else: b.raw('<path d="M%s,%sl8,3" stroke="%s" stroke-width="1.2" stroke-linecap="round"/>' % (f(x), f(y), shade))
