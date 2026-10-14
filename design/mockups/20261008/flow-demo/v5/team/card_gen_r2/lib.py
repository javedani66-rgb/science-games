# ابزار مشترک مولد کارت (card-artist v5): شکل با لبهٔ قلم‌مویی پخته در هندسه (بدون filter و بدون blend)
import math, random
LINE = '#241a5e'
def n(x):
    s = '%.1f' % x
    return s[:-2] if s.endswith('.0') else s
def pd(pts, closed=True):
    return 'M' + 'L'.join(n(x) + ' ' + n(y) for x, y in pts) + ('Z' if closed else '')
def brush(pts, amp, seed, step=14, closed=True):
    r = random.Random(seed); dp = []; N = len(pts)
    segs = N if closed else N - 1
    for i in range(segs):
        a = pts[i]; b = pts[(i + 1) % N]
        d = math.hypot(b[0] - a[0], b[1] - a[1]); k = max(1, round(d / step))
        for j in range(k): dp.append((a[0] + (b[0] - a[0]) * j / k, a[1] + (b[1] - a[1]) * j / k, j == 0))
    if not closed: dp.append((pts[-1][0], pts[-1][1], True))
    ox = oy = 0; out = []
    for x, y, c in dp:
        ox = .55 * ox + .45 * r.uniform(-amp, amp); oy = .55 * oy + .45 * r.uniform(-amp, amp)
        k = .3 if c else 1
        out.append((x + ox * k, y + oy * k))
    return out
def rr(x, y, w, h, r=0, k=4):
    if r <= 0: return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    pts = []
    for cx, cy, a0 in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)):
        for i in range(k + 1):
            a = math.radians(a0 + 90 * i / k); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts
def el(cx, cy, rx, ry, k=18, a0=0, a1=360, closed=True):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / k)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / k))) for i in range(k + (0 if closed and a1 - a0 == 360 else 1))]
def S(pts, fill='none', sw=4.5, seed=1, stroke=LINE, amp=None, step=14, closed=True, extra='', cap=True):
    """شکل: فقط L6/L4.5 قلم‌مویی می‌شوند؛ L2.6 و L1.2 صاف."""
    if amp is None: amp = {6: 1.5, 4.5: 1.1}.get(sw, 0)
    if amp: pts = brush(pts, amp, seed, step, closed)
    st = f' stroke="{stroke}" stroke-width="{n(sw)}" stroke-linejoin="round" stroke-linecap="round"' if sw else ''
    return f'<path d="{pd(pts, closed)}" fill="{fill}"{st}{(" " + extra) if extra else ""}/>'
def L(pts, color, sw=2.6, op=None, extra=''):
    o = f' opacity="{op}"' if op is not None else ''
    return f'<path d="{pd(pts, False)}" fill="none" stroke="{color}" stroke-width="{n(sw)}" stroke-linecap="round" stroke-linejoin="round"{o}{(" " + extra) if extra else ""}/>'
def tube(pts, w, fill, ow=4.5, seed=1, op=None, jit=True):
    """لولهٔ ضخیم با خط دور (طناب/گردن): دو stroke، بدون filter"""
    if jit and ow >= 4.5: pts = brush(pts, 0.9, seed, 16, False)
    d = pd(pts, False)
    return (f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="{n(w + 2 * ow)}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{n(w)}" stroke-linecap="round" stroke-linejoin="round"/>')
def g(i, body, extra=''):
    return f'<g id="{i}"{(" " + extra) if extra else ""}>{body}</g>'
def circ(cx, cy, r, fill, sw=2.6, stroke=LINE, seed=1):
    return S(el(cx, cy, r, r, 16), fill, sw, seed, stroke)
def bez(p0, p1, p2, p3=None, k=16):
    out = []
    for i in range(k + 1):
        t = i / k
        if p3 is None:
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]; y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        else:
            x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t * t * p2[0] + t ** 3 * p3[0]
            y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t * t * p2[1] + t ** 3 * p3[1]
        out.append((x, y))
    return out
def svg(vb, body, w=None, h=None, extra=''):
    x, y, ww, hh = vb
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{n(x)} {n(y)} {n(ww)} {n(hh)}"{extra}>{body}</svg>'
def symbol(i, vb, body):
    x, y, ww, hh = vb
    return f'<symbol id="{i}" viewBox="{n(x)} {n(y)} {n(ww)} {n(hh)}" style="stroke-linejoin:round;stroke-linecap:round">{body}</symbol>'
