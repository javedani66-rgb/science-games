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

PADRX, PADRY, WALL = 84, 28, 14
def pad(p):
    # لبهٔ زیر دو لایه
    base = ell(0, WALL, PADRX, PADRY, 0, 180, 24) + [(-PADRX, 0)] + ell(0, 0, PADRX, PADRY, 180, 360, 24)
    jj = p.j; p.j = .45
    p.shape(base, '#8a6f46', 5.2)
    p.shape(ell(0, WALL - .5, PADRX - 1.5, PADRY - .5, 0, 180, 24) + ell(0, WALL * .45, PADRX - 1.5, PADRY - .5, 180, 0, 24), '#6b5233', 2)
    for x, h in ((-58, .9), (-12, .95), (36, .9)):
        yy = PADRY * math.sqrt(1 - (x / PADRX) ** 2)
        p.line([(x, yy + 1), (x + 1.5, yy + WALL * h - 1)], 3.0, '#33240f', .85)
    p.shape(ell(0, 0, PADRX, PADRY), '#d9bd84', 5.2); p.j = jj
    # سنگ‌فرش درشت: ردیف‌های ناهم‌اندازه
    SEAM = '#8a6a36'
    rows = [(-18, [(-60, -34), (-20, 8), (30, 56)]), (-4, [(-72, -44), (-6, 34), (60, 70)]),
            (11, [(-62, -22), (10, 40)]), (21, [(-34, 12)])]
    for y, segs in rows:
        for a, b in segs:
            if y > -22:
                p.line([(a, y), ((a + b) / 2, y + 1.4), (b, y + .3)], 2.6, SEAM, .95)
    for (x, y0, y1) in ((-34, -18, -4), (8, -18, -4), (-44, -4, 11), (34, -4, 11), (-22, 11, 21), (12, 11, 21), (60, -4, 6), (-58, -18, -6)):
        p.line([(x, y0), (x + 1.4, y1)], 2.6, SEAM, .95)
    # سنگی که بیرون زده
    p.shape([(12, 6), (26, 4), (28, 11), (15, 14)], '#e8cf94', 3.4)
    p.shape([(15, 14), (28, 11), (28, 15), (16, 18)], '#8a6f46', 3.0)

def house(p):
    # سایهٔ خانه روی سکو
    p.raw('<path d="M-12,-4 L12,4 L4,10 L-28,6 Z" fill="#10083a" opacity=".22"/>')
    p.shape([(-78, -50), (-12, -50), (-12, -4), (-78, -4)], '#c8553d', 4.8)
    p.shape([(-90, -50), (-45, -88), (0, -50)], BRICK, 4.8)
    # دودکش
    p.shape([(-26, -83), (-14, -83), (-14, -62), (-26, -68)], BRICK, 4.0)
    p.line([(-29, -83), (-11, -83)], 3.4)
    # آجرهای درشت و کم
    for k, y in enumerate((-43, -32, -21, -12)):
        x0 = -74 if k % 2 == 0 else -68
        for j in range(2):
            a = x0 + j * 11
            if a < -56: p.line([(a, y), (a + 8.5, y + (.5 if k % 2 else -.4))], 3.0, BRICK, 1)
    for y in (-43, -32):
        p.line([(-27, y + 12), (-17, y + 12.5)], 3.0, BRICK, 1) if y == -32 else None
    p.line([(-19, -20), (-12.5, -19.5)], 3.0, BRICK, 1); p.line([(-30, -12), (-22, -12.5)], 3.0, BRICK, 1)
    p.hatch(-19, -49, -14, -7, 3, -4, 2, 2.4, NAVY, .5)
    # ردیف‌های فلس سقف: درشت
    for y, n in ((-57, 4), (-67, 3), (-77, 2)):
        h = y + 88; half = h * 1.0
        for i in range(n):
            x = -45 + (i - (n - 1) / 2) * 13
            p.line([(x - 5.5, y + 2.5), (x, y + 6), (x + 5.5, y + 2.5)], 3.0, '#d0725c', .95)
    # در و پنجرهٔ چراغ‌دار
    p.shape([(-58, -4), (-58, -22), (-54, -30), (-47, -33), (-40, -30), (-37, -22), (-37, -4)], '#2a1b4a', 3.8)
    for x in (-52, -47.5, -43): p.line([(x, -27 if x != -47.5 else -30), (x, -7)], 2.6, '#c9a0ff', .85)
    p.shape([(-31, -42), (-17, -42), (-17, -28), (-31, -28)], '#ffe9a0', 3.8)
    p.line([(-24, -42), (-24, -28)], 2.6); p.line([(-31, -35), (-17, -35)], 2.6)
    p.raw('<path d="M-29,-40 L-24,-40 L-24,-36 L-29,-36 Z" fill="#fff" opacity=".75"/>')
    # دود حلزونی (ضخامت متغیر)
    cl = []
    for i in range(0, 25):
        t = i / 24; a = t * 3.8 * math.pi; r = 1.2 + 4.2 * t
        cl.append((-20 + r * math.cos(a) + 3 * t, -87 - 16 * t - r * math.sin(a) * .8))
    p.ribbon(cl, lambda t: 1.5 + 3.0 * math.sin(math.pi * min(1, t * 1.05)) ** .7, '#ffffff', .25, edge=NAVY, ew=2.0)

SX = 52; L, R = 26, 78      # محور و لبه‌های بدنه
TOP = -83; TIPY = -16; TIP = 12

def shaft_pts(teeth):
    left = [(L, TOP)]
    for y in teeth: left += [(L, y), (L - 4.6, y + 4), (L + .5, y + 8)]
    left += [(L, TIPY), (SX, TIP)]
    right = [(R, TOP)]
    for y in teeth: right += [(R, y + 5), (R + 4.6, y + 9.5), (R - .5, y + 13)]
    right += [(R, TIPY)]
    # ترتیب: چپ از بالا به نوک، سپس راست از نوک به بالا
    return left + right[::-1]

def screw(p):
    gaps = [-69, -54.5, -38, -23.5]
    pts = shaft_pts(gaps)
    p.shape(pts, '#8fb5f2', 4.8)
    cid = 'node_screw_workshop_sc'
    p.raw('<clipPath id="%s"><path d="%s"/></clipPath>' % (cid, hd(pts, True, 7, 0.0)))
    # پله‌های رنگ بدنه (بالا روشن، پایین بنفش‌تر)
    def band(y0, y1, col, seed):
        r = random.Random(seed); top = [(L - 6 + i * 12, y0 + r.uniform(-1.6, 1.6)) for i in range(0, 9)]
        return '<path d="%s" fill="%s"/>' % (smooth_path(top + [(R + 6, y1), (L - 6, y1)], True), col)
    p.raw('<g clip-path="url(#%s)">' % cid + band(-52, 30, '#7d9fe6', 3) + band(-28, 30, '#8f8bd6', 5))
    # سایهٔ راست: نوار کامل با لبهٔ دست‌لرز
    sh = [(R - 11 + math.sin(i * 1.7) * 1.6, TOP + i * 7) for i in range(0, 13)]
    p.raw('<path d="%s" fill="#3b3f96" opacity=".42"/></g>' % smooth_path(sh + [(R + 8, TIPY + 2), (R + 8, TOP - 2)], True))
    # سایهٔ نیلی زیر هر رزوه و خود رزوه (ضخامت متغیر، منحنی S)
    for i, y0 in enumerate(gaps):
        drop = 11 + (1.5 if i % 2 else -.5)
        wob = 1.5 if i != 1 else 2.4
        x0, x1 = (L - 3, R + 3) if i < 3 else (L - 3, R - 8)
        cl = curve(x0, x1, y0, drop, wob, 16, seed=i * 2 + 1, hook=0)
        wf = lambda t: 1.6 + 3.7 * math.sin(math.pi * min(1, t / .96)) ** .6 if t < .96 else 1.6
        sh_cl = [(x, y + 4.6) for x, y in cl]
        p.raw('<g clip-path="url(#%s)">' % cid)
        p.ribbon(sh_cl, lambda t: 1.4 + 3.2 * math.sin(math.pi * t) ** .6, '#3b3f96', .3)
        p.raw('</g>')
        p.ribbon(cl, lambda t, i=i: 1.8 + 3.9 * math.sin(math.pi * t) ** .55 + (0 if i != 1 else .4), THREAD, .35, edge=NAVY, ew=2.0)
    # نوک: ضربهٔ سایه
    p.line([(SX + 10, TIPY + 1), (SX + 3, TIP - 3)], 2.6, '#3b3f96', .7)
    # خط دور بدنه دوباره (روی رنگ‌ها)
    p.raw('<path d="%s" fill="none" stroke="%s" stroke-width="4.8" stroke-linejoin="round" stroke-linecap="round"/>' % (hd(pts, True, 7, 1.0), NAVY))
    # کلاهک: بلند ۲۱، آبی-یخی
    cap = [(SX - 35, -104), (SX + 35, -104)] + ell(SX, -83, 35, 10, 0, 180, 18) 
    p.shape(cap, '#d6e8ff', 5.0)
    p.line([(SX - 33, -92), (SX - 20, -86), (SX, -83.5)], 2.6, '#8faee2', .8)
    p.shape(ell(SX, -104, 35, 10.5, 0, 360, 28), '#f1f8ff', 5.8)
    # شیار پهن و ناصاف
    sl = [(SX - 20, -108.5), (SX + 21, -100), (SX + 22, -96.8), (SX + 12, -97.2), (SX - 19, -105.2)]
    p.shape(sl, NAVY, 2.2)
    # دو لکهٔ درخشش کرم روی گوشهٔ چپ
    p.line([(SX - 29, -98), (SX - 28.5, -91)], 3.2, CREAM, 1)
    p.line([(SX - 25, -89.5), (SX - 24, -86)], 3.0, CREAM, 1)
    p.line([(SX - 30, -107), (SX - 25, -109.5)], 2.6, '#ffffff', .95)

def build():
    p = Pen(False, 1.0); p.sw = 4.8
    pad(p)
    # سایهٔ افتادهٔ پیچ روی سکو (سمت راست)
    p.raw('<path d="M%d,2 L%d,-1 L%d,10 L%d,15 L%d,18 L%d,14 Z" fill="#10083a" opacity=".24"/>' % (SX + 4, SX + 34, SX + 30, SX + 6, SX - 12, SX - 2))
    # مهرهٔ کنار در
    nut = [(-4 + 6 * math.cos(math.radians(a + 15)), 17 + 3.2 * math.sin(math.radians(a + 15))) for a in range(0, 360, 60)]
    p.shape(nut, '#f2c94c', 3.2); p.shape(ell(-4, 17, 2.1, 1.1, 0, 360, 10), '#d9bd84', 2)
    p.raw('<g transform="translate(-6 0)">'); house(p); p.raw('</g>')
    p.raw('<g transform="translate(46 12) scale(1.15) translate(-52 -12)">'); screw(p); p.raw('</g>')
    return p

def symbol(p):
    hl = ''
    return ('<symbol id="node_screw_workshop" viewBox="0 0 200 190" overflow="visible">'
            '<g id="node_screw_workshop_shadow" transform="translate(100 150)"><ellipse cx="8" cy="6" rx="92" ry="29" fill="#10083a" opacity=".25"/></g>'
            '<g id="node_screw_workshop_base" transform="translate(100 150)">' + p.svg() + '</g>'
            '<g id="node_screw_workshop_lit" transform="translate(100 150)"><path d="M%d,-100 L%d,-102" stroke="#fff" stroke-width="3" stroke-linecap="round" fill="none" opacity=".9"/></g></symbol>' % (SX - 24, SX - 14))
