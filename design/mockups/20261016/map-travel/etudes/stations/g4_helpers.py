"""کمک‌های ترسیم گروه ۴ دور ۶ (space_station, ice_rink, cart_station, well). به کیت دست نمی‌زند."""
import math
from station_kit import *


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, (' stroke="%s" stroke-width=".6" stroke-linejoin="round"' % col) if op == 1 else ' opacity="%s"' % op))   # حاشیهٔ هم‌رنگ: درز مویی بین چندضلعی‌ها نماند


def sharp(p, pts, col, sw):
    p.raw('<polygon points="%s" fill="%s" class="eo" stroke-width="%s" stroke-linejoin="miter" stroke-miterlimit="6"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, sw))


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r * p.xf[0], col))


def rect(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def band(cx, y, rx, ry, th, a0=0, a1=180, n=16):
    return ell(cx, y, rx, ry, a0, a1, n) + ell(cx, y + th, rx, ry, a1, a0, n)


def arcline(p, pts, col, w, op=1):
    q = p.X(pts)
    p.raw('<path d="M%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" opacity="%s"/>' % (' L'.join('%.1f,%.1f' % t for t in q), col, w, op))


def vcyl(p, cx, ytop, ybot, rx, ry, base, light, dark, top, sw=PART, lx=None):
    """استوانهٔ قائم ¾: بدنه + نوار روشن چپ + سایهٔ تیز راست + رویهٔ بیضی."""
    body = [(cx - rx, ytop), (cx + rx, ytop)] + ell(cx, ybot, rx, ry, 0, 180, 20)
    p.shape(body, base, sw, j=.1, step=99, clip=False)
    poly(p, rect(cx - rx + 3.5, ytop + 2, cx - rx + 3.5 + (lx or rx * .22), ybot - 2), light)
    x0 = cx + rx * .35
    arc = [(x, ybot + ry * math.sqrt(max(0, 1 - ((x - cx) / rx) ** 2))) for x in [x0 + (cx + rx - x0) * i / 8 for i in range(9)]][::-1]
    poly(p, [(x0, ytop + 2), (cx + rx, ytop + 2)] + arc, dark)
    p.stroke(body, sw, j=.1, step=99)
    p.shape(ell(cx, ytop, rx, ry, 0, 360, 28), top, sw, j=.05, step=99, clip=False)
