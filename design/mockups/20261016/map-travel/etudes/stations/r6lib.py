"""کمک‌های سه‌بعدی دور ۶ (فقط برای ایستگاه‌های این گروه): بیرون‌کشی نیم‌رخ با سه پلهٔ رنگ مثل مهرهٔ پیچ‌کاری."""
import math
from shapely.geometry import Polygon
from shapely.ops import unary_union
from station_kit import *


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, (' stroke="%s" stroke-width=".6" stroke-linejoin="round"' % col) if op == 1 else ' opacity="%s"' % op))   # حاشیهٔ هم‌رنگ: درز مویی بین چندضلعی‌ها نماند


def circ(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r * p.xf[0], col))


import os
ROUND = float(os.environ.get('SYM_ROUND', '0'))   # گرد کردن گوشه‌های محدب نیم‌رخ (واحد symbol)


def extrude(p, pts, D, front, top, side, mid=None, sw=PART, sw_in=INNER, in_stroke=True):
    """pts: نیم‌رخ جلو (مختصات symbol)، D: بردار عمق. رویه=top، پهلو=side، بین=mid. خط دور یکدست."""
    mid = mid or side
    if ROUND > 0:
        g_ = Polygon(pts).buffer(0).buffer(-ROUND).buffer(ROUND, 4)
        if g_.geom_type == 'Polygon' and g_.area > .6 * Polygon(pts).buffer(0).area: pts = list(g_.exterior.coords)[:-1]
    n = len(pts)
    area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n)) / 2
    pieces = [Polygon(pts).buffer(0), Polygon([(x + D[0], y + D[1]) for x, y in pts]).buffer(0)]
    quads = []
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        q = [a, b, (b[0] + D[0], b[1] + D[1]), (a[0] + D[0], a[1] + D[1])]
        pg = Polygon(q).buffer(0)
        if pg.area > 0: pieces.append(pg)
        ex, ey = b[0] - a[0], b[1] - a[1]
        nx, ny = (ey, -ex) if area > 0 else (-ey, ex)
        L = math.hypot(nx, ny) or 1; nx, ny = nx / L, ny / L
        if nx * D[0] + ny * D[1] <= .35 * math.hypot(*D) * .5: continue
        t = -ny
        col = top if t > .55 else (mid if t > .15 else side)
        quads.append((q, col))
    sil = unary_union(pieces).buffer(0.01)
    if sil.geom_type != 'Polygon': sil = max(sil.geoms, key=lambda g: g.area)
    ext = list(sil.exterior.coords)[:-1]
    p.shape(ext, side, sw, j=0, step=6, clip=False)
    for q, col in quads: poly(p, q, col)
    p.shape(pts, front, sw_in, j=0, step=6, clip=False)
    p.stroke(ext, sw, j=0, step=6)
    return ext


def box3(p, x0, y0, x1, y1, D, front, top, side, **kw):
    return extrude(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], D, front, top, side, **kw)


def rect(p, x0, y0, x1, y1, col, op=1): poly(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col, op)
