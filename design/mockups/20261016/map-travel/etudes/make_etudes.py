#!/usr/bin/env python3
"""اتودهای «خط دستی» برای پیچ‌کاری (D107). لرزش در خودِ مسیرهای برداری پخته می‌شود (نه فیلتر رستری) تا لبه‌ها پیکسلی نشوند."""
import math, random, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
NAVY = '#241a5e'

def sub(pts, closed, step):
    out = []; n = len(pts)
    for i in range(n if closed else n - 1):
        a, b = pts[i], pts[(i + 1) % n]
        L = math.hypot(b[0] - a[0], b[1] - a[1]); k = max(1, int(L / step))
        for t in range(k): out.append((a[0] + (b[0] - a[0]) * t / k, a[1] + (b[1] - a[1]) * t / k))
    if not closed: out.append(pts[-1])
    return out

def hd(pts, closed=True, seed=1, j=1.1, step=11):
    r = random.Random(seed); p = [(x + r.uniform(-j, j), y + r.uniform(-j, j)) for x, y in sub(pts, closed, step)]
    f = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    n = len(p)
    if closed:
        s = f(p[-1], p[0]); d = 'M%.1f,%.1f' % s
        for i in range(n): m = f(p[i], p[(i + 1) % n]); d += 'Q%.1f,%.1f %.1f,%.1f' % (p[i][0], p[i][1], m[0], m[1])
        return d + 'Z'
    d = 'M%.1f,%.1f' % p[0]
    for i in range(1, n - 1): m = f(p[i], p[i + 1]); d += 'Q%.1f,%.1f %.1f,%.1f' % (p[i][0], p[i][1], m[0], m[1])
    return d + 'L%.1f,%.1f' % p[-1]

def ell(cx, cy, rx, ry, a0=0, a1=360, n=40):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + (0 if a1 - a0 >= 360 else 1))]

class Pen:
    def __init__(s, over=False, j=1.1, sw=4.5): s.o = []; s.over = over; s.j = j; s.sw = sw; s.k = 0
    def shape(s, pts, fill, sw=None, closed=True):
        s.k += 1; sw = sw or s.sw
        s.o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%.1f" stroke-linejoin="round" stroke-linecap="round"/>' % (hd(pts, closed, s.k, s.j), fill, NAVY, sw))
        if s.over: s.o.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.6" opacity=".55" stroke-linecap="round"/>' % (hd(pts, closed, s.k + 99, s.j * 1.5), NAVY))
    def line(s, pts, sw=2.2, col=NAVY, op=1, closed=False):
        s.k += 1
        s.o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" opacity="%s"/>' % (hd(pts, closed, s.k, s.j * .7, 9), col, sw, op))
    def hatch(s, x0, y0, x1, y1, n, dx, dy, sw=1.6, col=NAVY, op=.5):
        for i in range(n):
            t = i / max(1, n - 1); s.line([(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t), (x0 + (x1 - x0) * t + dx, y0 + (y1 - y0) * t + dy)], sw, col, op)
    def svg(s): return ''.join(s.o)

def building(p, detail):
    # سکو
    p.shape(ell(0, 14, 94, 32, 0, 180, 24) + [(-94, 0)] + ell(0, 0, 94, 32, 180, 360, 24)[::1], '#9c8660')
    p.shape(ell(0, 0, 94, 32), '#e8d6aa')
    if detail:
        p.line([(-62, 6), (-20, 11), (30, 10)], 2, '#b7a06e', 1); p.line([(40, 12), (70, 5)], 2, '#b7a06e', 1)
        for x in (-80, -40, 0, 40, 78): p.line([(x, 17 + 8 * (1 - abs(x) / 94)), (x + 3, 24 + 6 * (1 - abs(x) / 94))], 1.8, '#6d5a3c', .8)
    # خانه
    p.shape([(-84, -52), (-14, -52), (-14, -6), (-84, -6)], '#c8553d')
    p.shape([(-92, -52), (-49, -84), (-6, -52)], '#8d3b2e')
    p.shape([(-62, -6), (-62, -26), (-58, -34), (-49, -37), (-40, -34), (-36, -26), (-36, -6)], '#2a1b4a', 4)
    p.shape([(-31, -43), (-16, -43), (-16, -28), (-31, -28)], '#fff3c4', 3.6)
    if detail:
        p.line([(-23.5, -43), (-23.5, -28)], 2.2); p.line([(-31, -35.5), (-16, -35.5)], 2.2)
        for y in (-64, -73): p.line([(-80 + (y + 84) * -.0 + (-64 - y) * -.0 - (y + 52) * .0, y + 3), (-18 + 0 * y, y + 3)][:0] or [(-49 - (y + 84) * 1.0, y), (-49 + (y + 84) * 1.0, y)], 1.8, '#5a2a22', .8)
        for (x, y) in ((-76, -44), (-60, -44), (-46, -44), (-78, -30), (-66, -22), (-26, -18), (-76, -16)): p.line([(x, y), (x + 9, y)], 1.8, '#8d3b2e', .9)
        for (x, y) in ((-70, -38), (-22, -22)): p.line([(x, y - 5), (x, y)], 1.6, '#8d3b2e', .9)
        p.hatch(-24, -50, -16, -8, 5, -5, 2, 1.5, NAVY, .35)
        p.line([(-56, -29), (-49, -33), (-42, -29)], 1.8, '#c9a0ff', .55)
        p.shape([(-30, -76), (-20, -76), (-20, -62), (-30, -64)], '#8d3b2e', 3.6)
    # پیچ بزرگ
    zig = [(30, -80)]
    for i in range(4): zig += [(21, -72 + i * 16), (30, -64 + i * 16)]
    zig += [(47, -3)]
    zg2 = []
    for i in range(4): zg2 += [(64, -16 - i * 16), (73, -24 - i * 16)][::-1]
    right = [(64, -16), (73, -24), (64, -32), (73, -40), (64, -48), (73, -56), (64, -64), (73, -72), (64, -80)]
    p.shape(zig + right, '#aebbd8')
    p.shape([(17, -94), (77, -94), (77, -80), (17, -80)], '#dfe6f2')
    p.shape(ell(47, -94, 30, 9, 0, 360, 24), '#f4f7fc')
    p.line([(30, -94), (64, -94)], 6)
    if detail:
        for y in (-72, -56, -40, -24): p.line([(27, y), (60, y + 8)], 1.8, '#fff3c4', .85)
        p.hatch(52, -76, 62, -22, 5, 4, 3, 1.5, '#3f4a8a', .6)
        p.line([(22, -91), (30, -88)], 1.6, '#ffffff', .9); p.line([(20, -84), (74, -84)], 1.6, '#9aa8c8', .7)

def cell(title, body, flt=''):
    return '<div class="c"><h3>%s</h3><div class="r"><svg viewBox="-110 -105 220 170" width="440" height="340"><g %s>%s</g></svg><svg viewBox="-110 -105 220 170" width="220" height="170"><g %s>%s</g></svg></div></div>' % (title, flt, body, flt, body)

def main():
    out = []
    old = (HERE / 'v0_old.svg').read_text(encoding='utf-8')
    old = re.sub(r'<symbol id="node_screw_workshop"[^>]*>', '<g transform="translate(-100 -150)">', old).replace('</symbol>', '</g>')
    old = old.replace('node_screw_workshop_', 'v0_')
    out.append(cell('۰) نمونهٔ قدیمی (فیلتر رستری ۳٫۴)', old, 'filter="url(#w34)"'))
    p = Pen(False, 0.0); building(p, False); out.append(cell('۱) همان طرح ساده، خط دستیِ برداری (بدون فیلتر)', p.svg()))
    p = Pen(False, 1.0); building(p, True); out.append(cell('۲) خط دستی + جزئیات بیشتر (آجر، شینگل، رزوه، سایه‌خط)', p.svg()))
    p = Pen(True, 1.2); building(p, True); out.append(cell('۳) مثل ۲ + دومین خط ظریفِ روی لبه (خطِ مدادی/ریخته‌شده)', p.svg()))
    html = '''<!doctype html><meta charset=utf-8><title>اتود پیچ‌کاری</title><style>
body{margin:0;background:#e9c57e;font-family:Vazirmatn,system-ui,sans-serif;direction:rtl;color:#241a5e}
.c{padding:10px 14px}.r{display:flex;gap:18px;align-items:flex-end;flex-wrap:wrap}h3{margin:6px 0;font-size:16px}
.eo{stroke:#241a5e;stroke-linejoin:round}.esd{fill:#10083a;opacity:.25}.elit{fill:#fff;opacity:.3}</style>
<svg width="0" height="0" style="position:absolute"><filter id="w34" filterUnits="userSpaceOnUse" x="-200" y="-200" width="600" height="600"><feTurbulence type="fractalNoise" baseFrequency=".045" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.4"/></filter></svg>
''' + ''.join(out)
    (HERE / 'etudes.html').write_text(html, encoding='utf-8')
if __name__ == "__main__": main()
