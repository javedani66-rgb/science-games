#!/usr/bin/env python3
"""پیچ‌کاری، گزینهٔ «الف» (خط دستیِ برداری، D107): نسخهٔ ۲ با نقد ۲. ساخت: import build() -> Pen."""
import math, random, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from make_etudes import hd, ell, Pen as P0, NAVY

CREAM = '#fff3c4'; BRICK = '#8d3b2e'; THREAD = '#ffe08a'
def sm(t): return t * t * (3 - 2 * t)

def smooth_path(p, closed=True):
    f = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    n = len(p)
    if closed:
        s = f(p[-1], p[0]); d = 'M%.1f,%.1f' % s
        for i in range(n): m = f(p[i], p[(i + 1) % n]); d += 'Q%.1f,%.1f %.1f,%.1f' % (p[i][0], p[i][1], m[0], m[1])
        return d + 'Z'
    d = 'M%.1f,%.1f' % p[0]
    for i in range(1, n - 1): m = f(p[i], p[i + 1]); d += 'Q%.1f,%.1f %.1f,%.1f' % (p[i][0], p[i][1], m[0], m[1])
    return d + 'L%.1f,%.1f' % p[-1]

class Pen(P0):
    def ribbon(s, cl, wfun, fill, j=.5, seed=0, edge=None, ew=0):
        """خط با ضخامت متغیر: cl نقاط خط مرکزی، wfun(t) ضخامت."""
        r = random.Random(1000 + s.k + seed); s.k += 1
        n = len(cl); L = []; R = []
        for i, (x, y) in enumerate(cl):
            a = cl[max(0, i - 1)]; b = cl[min(n - 1, i + 1)]
            dx, dy = b[0] - a[0], b[1] - a[1]; ln = math.hypot(dx, dy) or 1
            nx, ny = -dy / ln, dx / ln; w = wfun(i / (n - 1)) / 2
            jx, jy = r.uniform(-j, j), r.uniform(-j, j)
            L.append((x + nx * w + jx, y + ny * w + jy)); R.append((x - nx * w + jx, y - ny * w + jy))
        pts = L + R[::-1]
        d = smooth_path(pts, True)
        if edge: s.o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%.1f" stroke-linejoin="round"/>' % (d, edge, edge, ew))
        s.o.append('<path d="%s" fill="%s"/>' % (d, fill))
    def raw(s, x): s.o.append(x)

def curve(x0, x1, y0, drop, wob, n=14, seed=0, hook=0):
    r = random.Random(seed); pts = []
    for i in range(n + 1):
        t = i / n; x = x0 + (x1 - x0) * t
        y = y0 + drop * sm(t) * .6 + drop * .4 * t + wob * math.sin(2 * math.pi * t + seed) + r.uniform(-.5, .5)
        pts.append((x, y))
    if hook:
        x, y = pts[-1]; pts += [(x + 2.5, y + 2.6), (x + 3.6, y + hook)]
    return pts

PADRX, PADRY, WALL = 64, 26, 12
PAD_TOP = '#ecdca8'; PAD_WALL = '#b08a52'; SEAM = '#b49a62'

def ln(p, a, b, sw, col, op=1, j=.3):
    """خط منظم: راست، لرزش حداکثر نیم‌پیکسل"""
    p.k += 1; r = random.Random(p.k)
    p.o.append('<path d="M%.1f,%.1f L%.1f,%.1f" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" opacity="%s"/>' % (
        a[0] + r.uniform(-j, j), a[1] + r.uniform(-j, j), b[0] + r.uniform(-j, j), b[1] + r.uniform(-j, j), col, sw, op))

def pad(p):
    base = ell(0, WALL, PADRX, PADRY, 0, 180, 24) + [(-PADRX, 0)] + ell(0, 0, PADRX, PADRY, 180, 360, 24)
    jj = p.j; p.j = .45
    p.shape(base, PAD_WALL, 5.5)
    p.shape(ell(0, 0, PADRX, PADRY), PAD_TOP, 5.5); p.j = jj
    # D111/D112: سکو بسیار انتزاعی: سطح تخت، نیم‌سایهٔ راست، سه وجه دیواره (٢٫٦px بعد از مقیاس)
    half = ell(0, 0, PADRX - 3, PADRY - 2.5, -90, 90, 20)
    p.raw('<path d="%s" fill="#10083a" opacity=".09"/>' % smooth_path(half, True))
    for x in (-33, 0, 33):
        yy = PADRY * math.sqrt(1 - (x / PADRX) ** 2)
        ln(p, (x, yy + 5), (x, yy + WALL - 5), 3.8, '#8a6a3a', .6, .1)

def house(p):
    # D110: بعد از مقیاس .62*.72=.446: خط دور ٧٫٦=3.4px، جزء ٦٫٨=3.0px، داخلی حذف
    W = 7.9; PART = 6.9
    p.shape([(-78, -50), (-12, -50), (-12, -4), (-78, -4)], '#c8553d', W)
    p.raw('<path d="M-75,-46 L-15,-46 L-15,-39 L-75,-39 Z" fill="#10083a" opacity=".2"/>')   # نوار سایهٔ زیر لبهٔ سقف
    p.shape([(-90, -50), (-45, -88), (0, -50)], BRICK, W)
    p.shape([(-34, -83), (-20, -83), (-20, -62), (-34, -68)], BRICK, PART)     # دودکش
    p.shape([(-70, -4), (-70, -22), (-66, -32), (-57, -36), (-48, -32), (-44, -22), (-44, -4)], '#2a1b4a', PART)   # در
    p.shape([(-37, -42), (-19, -42), (-19, -26), (-37, -26)], '#ffe9a0', PART)    # پنجرهٔ چراغ‌دار

SX = 52; L, R = 26, 78      # محور و لبه‌های بدنه
TOP = -83; TIPY = -16; TIP = 12
PITCH = 16; SLOPE = 12

def shaft_pts(ys):
    left = [(L, TOP)]
    for y in ys: left += [(L, y), (L - 4.6, y + 4), (L, y + 8)]
    left += [(L, TIPY), (SX, TIP)]
    right = [(R, TOP)]
    for y in ys: right += [(R, y + SLOPE - 4), (R + 4.6, y + SLOPE), (R, y + SLOPE + 4)]
    right += [(R, TIPY)]
    return left + right[::-1]

def screw(p):
    ys = [-66, -66 + PITCH, -66 + 2 * PITCH]
    pts = shaft_pts(ys)
    p.shape(pts, '#8fb5f2', 6.6)
    cid = 'node_screw_workshop_sc'
    p.raw('<clipPath id="%s"><path d="%s"/></clipPath>' % (cid, hd(pts, True, 7, 0.0)))
    r = random.Random(5); top = [(L - 6 + i * 12, -32 + r.uniform(-1.4, 1.4)) for i in range(0, 9)]
    p.raw('<g clip-path="url(#%s)"><path d="%s" fill="#8f8bd6"/>' % (cid, smooth_path(top + [(R + 6, 30), (L - 6, 30)], True)))
    sh = [(R - 11 + math.sin(i * 1.7) * 1.0, TOP + i * 7) for i in range(0, 13)]
    p.raw('<path d="%s" fill="#3b3f96" opacity=".42"/></g>' % smooth_path(sh + [(R + 8, TIPY + 2), (R + 8, TOP - 2)], True))
    for y0 in ys:    # ۳ رزوهٔ هم‌شیب و موازی؛ فقط ضخامت می‌تپد
        cl = [(L - 3 + (R - L + 6) * t / 12, y0 + 4 + (SLOPE * ((L - 3 + (R - L + 6) * t / 12) - L) / (R - L))) for t in range(13)]
        p.ribbon(cl, lambda t: 2.4 + 4.0 * math.sin(math.pi * t) ** .55, THREAD, .12, edge=NAVY, ew=9.2)
    p.raw('<path d="%s" fill="none" stroke="%s" stroke-width="6.6" stroke-linejoin="round" stroke-linecap="round"/>' % (hd(pts, True, 7, .7), NAVY))
    cap = [(SX - 35, -104), (SX + 35, -104)] + ell(SX, -83, 35, 10, 0, 180, 18)
    p.shape(cap, '#d6e8ff', 5.8)
    p.shape(ell(SX, -104, 35, 10.5, 0, 360, 28), '#f1f8ff', 6.6)
    sl = [(SX - 20, -108.5), (SX + 21, -100), (SX + 22, -96.8), (SX + 12, -97.2), (SX - 19, -105.2)]
    p.shape(sl, NAVY, 3.4)
    ln(p, (SX - 29, -99), (SX - 28.5, -88), 4.8, CREAM)     # تنها درخشش

HS = .62; HX = -60.2 + 78 * HS; HY = 3 + 4 * HS     # خانه: پای چپ x=-60.2 (≈۳px چپ‌تر)، کف y=3
SS = .70; TIPX = 37; TIPYB = 8
def build():
    p = Pen(False, 1.0); p.sw = 5.5
    pad(p)
    p.raw('<g transform="translate(%.1f %.1f) scale(%s)">' % (HX, HY, HS)); house(p); p.raw('</g>')
    p.raw('<g transform="translate(%.1f %.1f) scale(%s) translate(-52 -12)">' % (TIPX, TIPYB, SS)); screw(p); p.raw('</g>')
    return p

def symbol(p):
    return ('<symbol id="node_screw_workshop" viewBox="0 0 200 190" overflow="visible">'
            '<g id="node_screw_workshop_shadow" transform="translate(100 150)"><ellipse cx="6" cy="27" rx="54" ry="21" fill="#10083a" opacity=".25"/></g>'
            '<g id="node_screw_workshop_base" transform="translate(100 150)">' + p.svg() + '</g>'
            '<g id="node_screw_workshop_lit" transform="translate(100 150)"></g></symbol>')
