import math, random, sys
from common import *
random.seed(7)
W, H = 390, 2400
SW = 3.6  # ضخامت خط دور بناها (مهم=ضخیم)
TH = 1.6  # تزئین نازک

# ---------- رنگ‌ها ----------
Z = dict(sea='#075a73', grass='#3f9a2b', farm='#9a8a10', space='#c4502f', ice='#d4efff')
CREAM = '#fff3c4'

# ---------- مسیر ----------
def wob(k, x): return 9 * math.sin(x / 55.0 + k * 1.7)
node_y = {k: 2215 - 182 * (k - 1) for k in range(1, 13)}
node_x = {k: (255 if k % 2 == 1 else 135) for k in range(1, 13)}
pts = []; node_idx = {}
def run(y, k, ltr, xs):
    if not ltr: xs = xs[::-1]
    for x in xs:
        pts.append((x, y + wob(k, x)))
        if k in node_x and k > 0 and x == node_x[k]: node_idx[k] = len(pts) - 1
XS = [70, 135, 195, 255, 320]
rows = [(0, 2340, True, [95, 150, 210, 270, 320])] + [(k, node_y[k], k % 2 == 0, XS) for k in range(1, 13)]
for i, (k, y, ltr, xs) in enumerate(rows):
    if k == 12: xs = [70, 135]
    run(y, k, ltr, xs)
    if i < len(rows) - 1:
        y2 = rows[i + 1][1]
        xe = pts[-1][0]
        bx = 360 if xe > 195 else 26
        pts.append((bx, (y + y2) / 2))
# توجه: برای k=0 هیچ گره‌ای نیست
def bez(P):
    segs = []
    n = len(P)
    for i in range(n - 1):
        p0 = P[max(i - 1, 0)]; p1 = P[i]; p2 = P[i + 1]; p3 = P[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        segs.append((p1, c1, c2, p2))
    return segs
SEGS = bez(pts)
def dstr(s0, s1):
    d = "M%.1f,%.1f" % SEGS[s0][0]
    for s in SEGS[s0:s1]:
        d += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (s[1] + s[2] + s[3])
    return d
HERE_K = 6
done_end = node_idx[HERE_K]
D_DONE = dstr(0, done_end)
D_REST = dstr(done_end, len(SEGS))
D_ALL = dstr(0, len(SEGS))
poly = []
for (p0, c1, c2, p3) in SEGS:
    for i in range(0, 21):
        t = i / 20; u = 1 - t
        poly.append((u**3*p0[0]+3*u*u*t*c1[0]+3*u*t*t*c2[0]+t**3*p3[0], u**3*p0[1]+3*u*u*t*c1[1]+3*u*t*t*c2[1]+t**3*p3[1]))
def pdist(x, y): return min(math.hypot(x - a, y - b) for a, b in poly)
def path_y_at(x, near_y):
    c = [(abs(b - near_y), b) for a, b in poly if abs(a - x) < 3 and abs(b - near_y) < 60]
    return min(c)[1] if c else near_y

NODE = {k: (node_x[k], path_y_at(node_x[k], node_y[k])) for k in node_x}
START = pts[0]

# ---------- ابزار شکل ----------
def ell(cx, cy, rx, ry, fill, sw=SW, extra=''):
    return '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s" %s/>' % (cx, cy, rx, ry, fill, OUT, sw, extra)
def rect(x, y, w, h, fill, sw=SW, r=3, extra=''):
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" %s/>' % (x, y, w, h, r, fill, OUT, sw, extra)
def poly_(pp, fill, sw=SW, extra=''):
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" %s/>' % (' '.join('%.1f,%.1f' % p for p in pp), fill, OUT, sw, extra)
def line(x1, y1, x2, y2, col=OUT, sw=TH, extra=''):
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s" stroke-linecap="round" %s/>' % (x1, y1, x2, y2, col, sw, extra)
def circ(cx, cy, r, fill, sw=SW, extra=''):
    return ell(cx, cy, r, r, fill, sw, extra)
def pth(d, fill='none', stroke=OUT, sw=SW, extra=''):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round" %s/>' % (d, fill, stroke, sw, extra)

def slab(rx, top, side, h=10, shadow=True):
    ry = rx * 0.36
    s = ''
    if shadow: s += '<ellipse cx="6" cy="%.1f" rx="%.1f" ry="%.1f" fill="#10083a" opacity=".28"/>' % (h + 8, rx + 6, ry + 2)
    s += ell(0, h, rx, ry, side) + ell(0, 0, rx, ry, top)
    return s

# ---------- بناها ----------
def b_harbor():
    s = ''
    # قایق سبز پشت
    s += poly_([(-112, -34), (-30, -34), (-44, -12), (-98, -12)], '#1f7a45')
    s += line(-108, -29, -34, -29, '#fff3c4', 3)
    s += rect(-92, -62, 42, 28, '#fff6dc', 3.2)
    s += rect(-86, -55, 8, 9, '#8fe3f0', 2) + rect(-72, -55, 8, 9, '#8fe3f0', 2)
    s += rect(-52, -52, 14, 18, '#1f7a45', 3)  # دودکش
    s += '<circle cx="-47" cy="-62" r="5" fill="#fff" opacity=".9"/><circle cx="-42" cy="-72" r="7" fill="#fff" opacity=".8"/>'
    s += line(-70, -62, -70, -88, OUT, 3) + circ(-70, -90, 3.5, '#ffd23f', 2)
    s += slab(78, '#f6dba0', '#a8672f')
    for x in range(-60, 70, 20): s += line(x, -8, x + 6, 8, '#a46f36', 1.5)
    # شمع بست + طناب
    s += rect(-60, -8, 12, 16, '#7a5026', 3)
    s += pth('M-54,-1 Q-70,-30 -92,-24', 'none', '#e9d7a0', 3.2)
    # جرثقیل
    s += rect(42, -112, 13, 112, '#2f9a55', SW)
    s += rect(-16, -118, 76, 10, '#2f9a55', SW)
    s += poly_([(42, -92), (42, -108), (4, -108)], '#2f9a55', 3)
    s += line(-8, -108, -8, -66, '#6b4a22', 2.5)
    s += rect(-21, -66, 26, 22, '#c98a45', 3) + line(-21, -66, 5, -44, OUT, 1.6) + line(5, -66, -21, -44, OUT, 1.6)
    # مرغ دریایی
    s += '<ellipse cx="22" cy="-12" rx="7" ry="5" fill="#fff" stroke="%s" stroke-width="2"/><circle cx="28" cy="-17" r="3.5" fill="#fff" stroke="%s" stroke-width="2"/><path d="M31,-17 l5,1 -5,2z" fill="#ff9d1c"/>' % (OUT, OUT)
    return s

def b_rink():
    s = slab(80, '#eaf9ff', '#e5496e', h=13)
    s += ell(0, 0, 58, 20, 'none', 1.6, 'stroke-opacity=".5"')
    s += pth('M-40,2 Q-10,-12 30,4', 'none', '#6bb6ee', 2)
    s += line(0, -20, 0, 20, '#e5496e', 1.5, 'opacity=".6"')
    # غرفک تیز
    s += rect(30, -42, 44, 30, '#fff6dc', SW)
    s += poly_([(24, -42), (80, -42), (52, -92)], '#e5496e', SW)
    s += poly_([(52, -92), (66, -42), (52, -42)], '#fff', 0)
    s += line(52, -92, 52, -112, OUT, 3) + poly_([(52, -112), (70, -106), (52, -100)], '#ffd23f', 2.5)
    s += rect(46, -28, 12, 16, '#6b8cff', 2.5)
    # اسکیت‌باز
    s += circ(-34, -34, 6, '#ffd2a8', 2.8) + poly_([(-39, -30), (-29, -30), (-32, -14), (-36, -14)], '#2fa4ff', 2.8)
    s += line(-35, -14, -42, 0, OUT, 3) + line(-32, -14, -22, -6, OUT, 3) + line(-44, 1, -36, 1, '#ffd23f', 2.5)
    s += line(-38, -24, -50, -30, OUT, 3) + line(-29, -24, -17, -32, OUT, 3)
    return s

def b_stadium():
    s = '<ellipse cx="6" cy="20" rx="86" ry="30" fill="#10083a" opacity=".28"/>'
    s += ell(0, 10, 82, 29, '#a8350f') + rect(-82, -18, 164, 28, '#d4491f', SW, 0)
    s += ell(0, -18, 82, 29, '#ffe3a6')
    for x in range(-70, 80, 14): s += line(x, -10, x, 8, '#ffd38a', 2.4)
    s += pth('M-82,10 A82,29 0 0 0 82,10', 'none', OUT, SW)
    s += ell(0, -18, 62, 20, '#58c04a', 3) + ell(0, -18, 14, 6, 'none', 1.6, 'stroke="#fff"')
    s += line(-62, -18, 62, -18, '#fff', 1.6)
    # برج‌های نور
    for sx in (-1, 1):
        x = sx * 74
        s += line(x, -22, x, -94, OUT, 6) + line(x, -22, x, -94, '#d9d4ec', 2.6)
        s += rect(x - 14, -112, 28, 18, '#fff6dc', 3.2)
        for dx in (-7, 0, 7): s += '<circle cx="%d" cy="-103" r="2.8" fill="#ffd23f"/>' % (x + dx)
    return s

def b_space():
    s = slab(84, '#c9cfe6', '#6e72a8', h=11)
    # پنل‌های خورشیدی
    for sx in (-1, 1):
        x = sx * 62
        s += line(x, -8, x, -26, OUT, 3.5)
        pp = [(x - 22, -28), (x + 22, -28), (x + 30, -52), (x - 14, -52)] if sx > 0 else [(x - 22, -28), (x + 22, -28), (x + 14, -52), (x - 30, -52)]
        s += poly_(pp, '#2d62e8', 3.4) + line(x - 4, -28, x + (6 if sx>0 else -6), -52, '#9cc0ff', 1.4) + line(x-10, -40, x+10, -40, '#9cc0ff', 1.4)
    # گنبد
    s += pth('M-46,0 A46,46 0 0 1 46,0 Z', '#f4f6ff', 'none', 0)
    s += pth('M-46,0 A46,46 0 0 1 46,0 Z', '#f4f6ff', OUT, SW)
    s += pth('M-36,-14 A36,36 0 0 1 36,-14', 'none', '#7fd4ff', 7)
    s += pth('M-36,-14 A36,36 0 0 1 36,-14', 'none', OUT, 1.8, 'transform="translate(0,5)"')
    s += line(0, -46, 0, -100, OUT, 4) + circ(0, -102, 5, '#ff4b4b', 3)
    s += line(-12, -70, 12, -70, OUT, 3.4)
    s += rect(-12, -22, 24, 22, '#ffd23f', 3, 8)  # در
    s += cog(-62, -64, 12, '#ffd23f', 3)
    return s

def b_rocket():
    s = slab(62, '#c9cfe6', '#6e72a8', h=10)
    # برج پرتاب
    s += rect(34, -118, 14, 118, '#8a90c0', SW, 2)
    for y in range(-110, -4, 22): s += line(34, y, 48, y + 22, OUT, 1.8) + line(48, y, 34, y + 22, OUT, 1.8)
    s += line(34, -96, 20, -96, OUT, 4)
    # موشک
    s += poly_([(-26, -10), (-40, 4), (-18, -22)], '#ff4b4b', 3.4)
    s += poly_([(26, -10), (40, 4), (18, -22)], '#ff4b4b', 3.4)
    s += pth('M-20,-6 L-20,-70 Q0,-150 20,-70 L20,-6 Z', '#fafaff', OUT, SW)
    s += pth('M-17,-86 Q0,-146 17,-86 Z', '#ff4b4b', 'none', 0) + pth('M-20,-74 Q0,-150 20,-74', 'none', OUT, SW)
    s += circ(0, -62, 9, '#7fd4ff', 3.2) + line(-20, -30, 20, -30, OUT, 2) 
    s += poly_([(-10, -4), (10, -4), (0, 14)], '#ffb21c', 2.5, 'opacity=".95"')
    return s

def cog(x, y, r, fill='#ffd23f', sw=3):
    n = 8; pp = []
    for i in range(n * 2):
        a = math.pi * i / n; rr = r if i % 2 == 0 else r * .74
        for da in (-.12, .12):
            pp.append((x + rr * math.cos(a + da), y + rr * math.sin(a + da)))
    return poly_(pp, fill, sw) + circ(x, y, r * .3, '#fff6dc', sw * .7)
# ---- گره‌های کوچک ----
def s_buoy():
    s = slab(34, '#f6dba0', '#a8672f', h=8)
    s += line(0, -18, 0, -50, OUT, 3.5) + circ(0, -52, 4, '#ffd23f', 2.4)
    s += ell(0, -14, 15, 15, '#fff', SW) + pth('M-15,-14 A15,15 0 0 1 15,-14', '#ff4b4b', OUT, 0) 
    s += pth('M-15,-14 A15,15 0 0 1 15,-14 Z', '#ff4b4b', OUT, SW) + pth('M-15,-14 A15,15 0 0 0 15,-14', '#fff', OUT, SW)
    return s
def s_crates():
    s = slab(40, '#f6dba0', '#a8672f', h=8)
    s += poly_([(-5, 0), (5, 0), (0, -12)], '#8a90c0', 3)
    s += poly_([(-34, -22), (34, -14), (34, -9), (-34, -17)], '#e2a95d', 3)
    s += rect(-32, -44, 22, 22, '#c98a45', 3.2, 2) + line(-32, -44, -10, -22, OUT, 1.5) + line(-10, -44, -32, -22, OUT, 1.5)
    s += circ(30, -24, 6, '#ff4b4b', 2.8)
    return s
def s_ball():
    s = slab(38, '#c9f5ad', '#2c7a2a', h=8)
    s += poly_([(-30, -2), (28, -2), (28, -34)], '#f2a33a', SW)
    s += line(-14, -8, 14, -8, '#c4701a', 1.6) + line(-4, -14, 18, -14, '#c4701a', 1.6)
    s += circ(-6, -20, 11, '#fff', 3.4) + poly_([(-6, -26), (0, -21), (-2, -14), (-10, -14), (-12, -21)], OUT, 1.2)
    return s
def s_goal():
    s = slab(38, '#c9f5ad', '#2c7a2a', h=8)
    s += rect(-24, -40, 48, 38, 'rgba(255,255,255,.35)', 3.6, 1)
    for x in range(-16, 24, 8): s += line(x, -40, x, -2, '#fff', 1.2)
    for y in (-30, -20, -10): s += line(-24, y, 24, y, '#fff', 1.2)
    return s
def s_snowman():
    s = slab(34, '#f4fcff', '#9fd0f0', h=8)
    s += circ(0, -12, 15, '#fff', SW) + circ(0, -36, 11, '#fff', SW)
    s += poly_([(0, -36), (14, -33), (0, -31)], '#ff8a1c', 2) + circ(-4, -39, 1.6, OUT, 0) + circ(4, -39, 1.6, OUT, 0)
    s += rect(-9, -56, 18, 11, '#e5496e', 3) + line(-13, -45, 13, -45, OUT, 3.4)
    return s
def s_pine():
    s = slab(36, '#f4fcff', '#9fd0f0', h=8)
    s += rect(-4, -10, 8, 12, '#7a5026', 2.8)
    for (y, w) in [(-8, 28), (-28, 22), (-46, 15)]:
        s += poly_([(-w, y), (w, y), (0, y - 26)], '#2a8a58', 3.4)
        s += poly_([(-w * .55, y - 11), (w * .55, y - 11), (0, y - 26)], '#fff', 0)
    return s
def s_dish():
    s = slab(36, '#d6dbef', '#6e72a8', h=8)
    s += line(0, -6, 0, -26, OUT, 5) + line(-12, 0, 0, -22, OUT, 3.4) + line(12, 0, 0, -22, OUT, 3.4)
    s += pth('M-24,-52 Q-2,-14 24,-34 Q6,-60 -24,-52 Z', '#f4f6ff', OUT, SW)
    s += line(0, -34, 14, -62, OUT, 3) + circ(15, -64, 3.4, '#ff4b4b', 2.2)
    return s


def s_scale():  # ترازو: جرم
    s = slab(38, '#d6dbef', '#6e72a8', h=8)
    s += line(0, -4, 0, -40, OUT, 5) + rect(-26, -45, 52, 7, '#ffd23f', 3, 3) + circ(0, -48, 5, '#fff6dc', 2.6)
    for sx in (-1, 1):
        x = sx * 24
        s += line(x, -40, x - 9, -22, OUT, 1.8) + line(x, -40, x + 9, -22, OUT, 1.8) + pth('M%d,-22 h18 a9,9 0 0 1 -18,0z' % (x - 9), '#c9cfe6', OUT, 3)
    s += rect(-30, -34, 12, 12, '#ff6a4b', 2.8, 2)
    return s
def s_grav():  # گرانش: سیب و فلش
    s = slab(36, '#d6dbef', '#6e72a8', h=8)
    s += circ(0, -18, 11, '#ff4b4b', 3.2) + pth('M0,-29 q2,-8 9,-8', 'none', '#2fa44a', 3)
    s += line(0, -40, 0, -64, '#ffd23f', 4, 'stroke-dasharray="1 8"') 
    s += poly_([(-8, -50), (8, -50), (0, -38)], '#ffd23f', 2.6)
    return s
def s_seesaw():  # تاب: اهرم
    s = slab(40, '#f4e6a0', '#8a7a2a', h=8)
    s += poly_([(-8, 0), (8, 0), (0, -14)], '#8a90c0', 3)
    s += poly_([(-34, -32), (34, -12), (34, -7), (-34, -27)], '#e2a95d', 3.2)
    s += rect(-36, -52, 18, 18, '#e5496e', 3, 3) + circ(28, -22, 5, '#ffd23f', 2.6)
    return s
def s_wedge():  # گوه: تبر در تنه
    s = slab(36, '#f4e6a0', '#8a7a2a', h=8)
    s += rect(-26, -26, 52, 26, '#a8672f', SW, 5) + ell(-26, -13, 6, 13, '#d9a05a', 3)
    s += poly_([(-8, -26), (10, -26), (1, -52)], '#c9cfe6', SW) + line(1, -52, 1, -28, OUT, 1.6)
    return s
def s_pulley():  # قرقره
    s = slab(36, '#f6dba0', '#a8672f', h=8)
    s += rect(-4, -56, 8, 56, '#2f9a55', 3) + rect(-4, -58, 30, 8, '#2f9a55', 3)
    s += circ(22, -40, 8, '#fff6dc', 3) + line(14, -40, 14, -24, '#6b4a22', 2.2) + line(30, -40, 30, -34, '#6b4a22', 2.2)
    s += rect(8, -24, 14, 14, '#c98a45', 3, 2)
    return s
def b_windmill():
    s = slab(60, '#f4e6a0', '#8a7a2a', h=10)
    s += poly_([(-24, 0), (24, 0), (15, -84), (-15, -84)], '#fff0d0', SW)
    s += poly_([(-19, -84), (19, -84), (0, -110)], '#d4491f', SW)
    s += rect(-7, -22, 14, 22, '#a8672f', 3, 6) + rect(-4, -62, 8, 10, '#7fd4ff', 2.4)
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2; ex, ey = 54 * math.cos(a), 54 * math.sin(a)
        nx, ny = -math.sin(a) * 9, math.cos(a) * 9
        s += poly_([(0, -84), (ex + 0, -84 + ey), (ex + nx, -84 + ey + ny), (nx * .3, -84 + ny * .3)], '#fff6dc', 3) if False else poly_([(0, -84 + 0), (ex, -84 + ey), (ex + nx, -84 + ey + ny), (nx * .35, -84 + ny * .35)], '#fff6dc', 3)
    s += circ(0, -84, 6, '#ffd23f', 3)
    return s
def b_factory():
    s = slab(80, '#cfd3e2', '#6e72a8', h=11)
    s += rect(-56, -46, 112, 46, '#c4502f', SW, 2)
    for x in range(-40, 50, 20): s += line(x, -46, x, 0, '#8e2c1a', 1.6)
    s += poly_([(-56, -46), (-56, -66), (-30, -46), (-30, -66), (-4, -46), (-4, -66), (22, -46), (22, -66), (48, -46), (56, -46)], '#8a90c0', SW)
    s += rect(36, -100, 16, 54, '#7d4a2a', SW, 2) + rect(-50, -86, 14, 42, '#7d4a2a', SW, 2)
    s += '<circle cx="44" cy="-110" r="8" fill="#fff" opacity=".85"/><circle cx="52" cy="-122" r="10" fill="#fff" opacity=".75"/><circle cx="-42" cy="-96" r="8" fill="#fff" opacity=".8"/>'
    s += cog(0, -24, 20, '#ffd23f', 3.4) + rect(30, -22, 18, 22, '#241a5e', 2.6, 6)
    return s
BUILD = {1: (s_ball, 38), 2: (b_rink, 82), 3: (b_stadium, 82), 4: (s_scale, 38), 5: (s_grav, 36), 6: (b_space, 86),
         7: (s_seesaw, 40), 8: (b_windmill, 60), 9: (s_wedge, 36), 10: (s_pulley, 36), 11: (b_factory, 80), 12: (b_harbor, 80)}
LOCKED = (10, 11, 12)

def done_badge(x, y):
    return ('<g transform="translate(%.1f,%.1f)">%s<polyline points="-5,0 -1.5,4 5.5,-4" fill="none" stroke="%s" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></g>'
            % (x, y, circ(0, 0, 10, CREAM, 3), OUT))

# ---------- تزئین ----------
def cloud(x, y, s=1, op=.95):
    cs = [(-18, 2, 12), (-4, -6, 16), (14, -2, 13), (28, 4, 9), (4, 6, 14)]
    g = '<g transform="translate(%.1f,%.1f) scale(%.2f)" opacity="%.2f">' % (x, y, s, op)
    g += ''.join('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (a, b, r + 1.8, OUT) for a, b, r in cs)
    g += ''.join('<circle cx="%d" cy="%d" r="%d" fill="#fff"/>' % (a, b, r) for a, b, r in cs)
    return g + '</g>'
def bird(x, y, s=1):
    return '<path d="M%.1f,%.1f q%.1f,-%.1f %.1f,0 q%.1f,-%.1f %.1f,0" fill="none" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>' % (x, y, 5*s, 6*s, 10*s, 5*s, 6*s, 10*s, OUT)
def wave(x, y, s=1, col='#fff', op=.32):
    return '<path d="M%.1f,%.1f q%.1f,-%.1f %.1f,0 t%.1f,0 t%.1f,0" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round" opacity="%s"/>' % (x, y, 6*s, 7*s, 12*s, 12*s, 12*s, col, op)
def tree(x, y, s=1):
    return ('<g transform="translate(%.1f,%.1f) scale(%.2f)"><rect x="-3" y="0" width="6" height="12" fill="#6b4a22" stroke="%s" stroke-width="1.6"/>'
            '<circle cx="0" cy="-6" r="14" fill="#2f8a2b" stroke="%s" stroke-width="1.8"/><circle cx="-4" cy="-10" r="5" fill="#6fcf5e" opacity=".7"/></g>' % (x, y, s, OUT, OUT))
def pinet(x, y, s=1):
    return ('<g transform="translate(%.1f,%.1f) scale(%.2f)"><polygon points="-11,8 11,8 0,-22" fill="#2a8a58" stroke="%s" stroke-width="1.6" stroke-linejoin="round"/>'
            '<polygon points="-5,-6 5,-6 0,-22" fill="#fff"/></g>' % (x, y, s, OUT))
def crater(x, y, r):
    return '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#8e2c1a" opacity=".35"/><ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="#ffb08a" stroke-width="2" opacity=".35"/>' % (x, y, r, r*.45, x, y-1.5, r, r*.45)
def lamp(x, y):
    return ('<g transform="translate(%.1f,%.1f)"><circle cx="0" cy="-22" r="14" fill="#ffe27a" opacity=".35"/><line x1="0" y1="0" x2="0" y2="-22" stroke="%s" stroke-width="3" stroke-linecap="round"/>'
            '<circle cx="0" cy="-24" r="5" fill="#ffe27a" stroke="%s" stroke-width="2.2"/></g>' % (x, y, OUT, OUT))
def snowpatch(x, y, rx):
    return '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#fff" opacity=".28"/>' % (x, y, rx, rx*.35)

def scatter(n, ymin, ymax, fn, mind=62, xr=(14, 376), taken=None):
    out = ''; tries = 0; c = 0
    taken = taken if taken is not None else []
    while c < n and tries < 4000:
        tries += 1
        x = random.uniform(*xr); y = random.uniform(ymin, ymax)
        if pdist(x, y) < mind: continue
        if any(math.hypot(x - a, y - b) < 80 for a, b in taken): continue
        if any(math.hypot(x - NODE[k][0], y - NODE[k][1] + 40) < 110 for k in NODE): continue
        taken.append((x, y)); out += fn(x, y); c += 1
    return out


def lock_badge(x, y):
    return ('<g transform="translate(%.1f,%.1f)">%s<path d="M-3.6,-1 v-2.4 a3.6,3.6 0 0 1 7.2,0 v2.4" fill="none" stroke="%s" stroke-width="2.4"/><rect x="-5.6" y="-1" width="11.2" height="8" rx="2" fill="%s"/></g>'
            % (x, y, circ(0, 0, 10, CREAM, 3), OUT, OUT))
