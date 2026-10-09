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
# پایه‌های خاص زمین (مرکز پایه = ۰،۰)
PAD = {'sports': ('#a6d86a', '#66993b'), 'space': ('#d9d3f0', '#a79fcb'), 'farm': ('#c7a56a', '#9b7a48'), 'city': ('#c6c1b6', '#9b968c')}
def pad(b, zone, rx, seed=3):
    top, side = PAD[zone]; ry = rx * .34; h = 9
    if zone == 'sports':
        b.raw('<g transform="translate(0 %s)"><path d="%s" fill="%s" class="eo" stroke-width="4.5"/></g>' % (h, blob(rx, ry, 14, .07, seed), side)); b.clip.append('<path transform="translate(0 %s)" d="%s"/>' % (h, blob(rx, ry, 14, .07, seed)))
        b.path(blob(rx, ry, 14, .07, seed), top, 4.5)
        b.line(-rx * .5, 2, -rx * .3, -3, '#7fbf4a', 1.2); b.line(rx * .35, 3, rx * .5, -2, '#7fbf4a', 1.2)
    elif zone == 'space':
        b.ell(0, h, rx, ry, side); b.rect(-rx, 0, 2 * rx, h, side, 0, 0); b.ell(0, 0, rx, ry, top)
        b.line(-rx * .5, 0, -rx * .3, 3, '#a79fcb', 1.2)
    elif zone == 'farm':
        b.path('M%s,%s Q%s,%s 0,%s Q%s,%s %s,%s Z' % (f(-rx), f(h), f(-rx * .7), f(-ry * 1.5), f(-ry * 1.4), f(rx * .7), f(-ry * 1.5), f(rx), f(h)), side, 4.5)
        b.ell(0, 1, rx * .86, ry * .9, top, 4.5)
        b.line(-rx * .3, 3, -rx * .1, 0, '#9b7a48', 1.2)
    else:
        b.rect(-rx, -ry, 2 * rx, 2 * ry + h, side, 4.5, 12); b.rect(-rx, -ry, 2 * rx, 2 * ry, top, 4.5, 12)
        b.line(-rx * .6, ry * .2, -rx * .1, ry * .2, '#9b968c', 1.2)
