#!/usr/bin/env python3
"""اتودهای ۲ پیچ‌کاری (D107 + نقد ۱). خروجی etudes2.html و assets/node_screw_workshop.svg (جهت انتخاب‌شده، پیش‌فرض د)."""
import math, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from make_etudes import hd, ell, Pen as P0, NAVY, HERE

SHAFT = '#7fa9ee'; CREAM = '#fff3c4'; BRICK = '#8d3b2e'
class Pen(P0):
    f = staticmethod(lambda q: q)
    def shape(s, pts, fill, sw=None, closed=True): P0.shape(s, [s.f(q) for q in pts], fill, sw, closed)
    def line(s, pts, sw=2.2, col=NAVY, op=1, closed=False): P0.line(s, [s.f(q) for q in pts], max(sw, 1.8), col, op, closed)

IDF = lambda q: q
HF = lambda q: (-52 + (q[0] + 49) * .9, -6 + (q[1] + 6) * .9)         # خانه ۰٫۹
S = 1.3
SF = lambda q: (46 + (q[0] - 47) * S, q[1] * S - 2)                  # پیچ ۱٫۳ برابر

def pad(p, pave):
    p.f = IDF
    p.shape(ell(0, 14, 94, 32, 0, 180, 24) + [(-94, 0)] + ell(0, 0, 94, 32, 180, 360, 24), '#8a6f46', 5.2)
    p.shape(ell(0, 0, 94, 32), '#d9bd84', 5.2)
    if pave:
        for (a, b) in (((-70, 9), (-30, 15)), ((-24, 19), (22, 21)), ((30, 16), (66, 9)), ((-52, -9), (-12, -5)), ((24, -8), (58, -3))):
            p.line([a, b], 2.1, '#a88a50', .95)
        for (x, y) in ((-48, 12), (-3, 18), (46, 13), (-32, -7), (40, -5), (-72, 1), (74, 1)):
            p.line([(x, y - 4), (x + 1, y + 3)], 2, '#a88a50', .95)
    for x in (-78, -52, -24, 8, 38, 66):
        yy = 32 * math.sqrt(max(0, 1 - (x / 94) ** 2))
        p.line([(x, yy + 4), (x + 2, yy + 11)], 2.1, '#5e4a2c', .85)

def props(p):
    p.f = IDF
    nut = [(-30 + 6 * math.cos(math.radians(a + 15)), 10 + 3.4 * math.sin(math.radians(a + 15))) for a in range(0, 360, 60)]
    p.shape(nut, '#f2c94c', 3.2); p.shape(ell(-30, 10, 2.2, 1.2, 0, 360, 10), '#d9bd84', 2)
    p.shape([(-8, 12), (-4, 10), (11, 15), (10, 19), (-5, 17)], '#aebbd8', 3.2)          # پیچ افتاده
    p.line([(-1, 13), (1, 17)], 1.8, '#4d63b8', .8); p.line([(4, 14), (6, 18)], 1.8, '#4d63b8', .8)
    p.shape([(-65, 14), (-45, 20)], 'none', 5.4, closed=False)                          # دستهٔ آچار
    p.line([(-65, 14), (-45, 20)], 3, '#e05a47', 1)
    p.shape(ell(-68, 13, 5.5, 4, 40, 320, 10) , '#e05a47', 3, closed=True)

def house(p, rich):
    p.f = HF
    p.shape([(-84, -52), (-14, -52), (-14, -6), (-84, -6)], '#c8553d', 4.8)
    p.shape([(-92, -52), (-49, -84), (-6, -52)], BRICK, 4.8)
    p.shape([(-62, -6), (-62, -26), (-58, -34), (-49, -37), (-40, -34), (-36, -26), (-36, -6)], '#2a1b4a', 3.8)
    p.shape([(-31, -43), (-16, -43), (-16, -28), (-31, -28)], CREAM, 3.6)
    p.line([(-23.5, -43), (-23.5, -28)], 2.2); p.line([(-31, -35.5), (-16, -35.5)], 2.2)
    for x in (-55, -49, -43): p.line([(x, -31 if x != -49 else -36), (x, -8)], 1.8, '#c9a0ff', .75)
    for k, y in enumerate((-46, -38, -30, -22, -14)):
        xs = (-81, -69) if k % 2 == 0 else (-75, -64)
        for x in xs: p.line([(x, y), (x + 9.5, y + (.6 if k % 2 else -.4))], 2, BRICK, .95)
    for (x, y) in ((-58, -47), (-44, -44)): p.line([(x, y), (x + 8, y)], 2, BRICK, .95)
    p.hatch(-24, -50, -16, -8, 4, -5, 2, 2, NAVY, .45)
    for y, n in ((-58, 5), (-66, 4), (-74, 2)):
        h = (y + 84)
        for i in range(n):
            x = -49 - h + 9 + i * ((2 * h - 18) / max(1, n - 1)) if n > 1 else -49
            p.line([(x - 5, y + 3), (x, y + 6), (x + 5, y + 3)], 2, '#d0725c', .85)
    p.shape([(-28, -78), (-18, -78), (-18, -62), (-28, -66)], BRICK, 3.8)
    p.line([(-30, -78), (-16, -78)], 2.6)
    if rich:
        # دود حلزونی
        pts = []
        for i in range(0, 25):
            t = i / 24; a = t * 4.2 * math.pi; r = 1.5 + 4.5 * t
            pts.append((-23 + r * math.cos(a) + 2 * t, -84 - 14 * t - r * math.sin(a) * .8))
        p.line(pts, 2.4, '#ffffff', .95)

def screw(p, teeth, helix, shade=True):
    p.f = SF
    L, R, top = 24, 70, -80
    ys = [-72, -60.5, -48, -36.5, -25]
    if teeth:
        pts = [(L, top)]
        for y in ys: pts += [(L, y), (L - 7, y + 4), (L, y + 11)]
        pts += [(L, -12), (47, 2), (R, -12)]
        for y in reversed(ys): pts += [(R, y + 15), (R + 7, y + 9), (R, y + 4)][::-1] if False else [(R, y + 16), (R + 7, y + 10), (R, y + 5)]
        pts += [(R, top)]
        # بالا: نقاط راست از پایین به بالا مرتب‌اند
    else:
        pts = [(L, top), (L, -14), (47, 2), (R, -14), (R, top)]
    p.shape(pts, SHAFT, 4.8)
    if helix:
        for y in ys[:4]:
            arc = [(L + 2 + t * 44, y + 4 + 13 * t + 3.5 * math.sin(math.pi * t)) for t in [i / 8 for i in range(9)]]
            p.line([(x, yy + 3.2) for x, yy in arc], 1.8, '#3f4a8a', .6)
            p.line(arc, 2.8, CREAM, 1)
        arc = [(L + 3 + t * 34, ys[4] + 4 + 12 * t + 3 * math.sin(math.pi * t)) for t in [i / 6 for i in range(7)]]
        p.line(arc, 2.8, CREAM, 1)
    if shade:
        p.hatch(63, top + 8, 66, -22, 4, 2, 3, 2, '#3f4a8a', .45)
    p.line([(L - 1, -78), (R + 1, -78)], 2.4, '#3f4a8a', .75)        # سایهٔ زیر کلاهک
    p.shape([(15, -96), (79, -96), (79, -80), (15, -80)], '#e3e9f6', 4.8)
    p.shape(ell(47, -96, 32, 10, 0, 360, 28), '#f4f7fc', 4.8)
    c = math.cos(math.radians(15)); s = math.sin(math.radians(15))
    sl = [(47 + dx * c - dy * s, -96 + dx * s + dy * c) for dx, dy in ((-19, -1.6), (19, -1.6), (19, 1.6), (-19, 1.6))]
    p.shape(sl, '#241a5e', 2.4)

def build(teeth, helix, pave, rich, pr):
    p = Pen(False, 1.0); p.sw = 4.8
    pad(p, pave); 
    if pr: props(p)
    house(p, rich); screw(p, teeth, helix); return p

def cell(title, body):
    return '<div class="c"><h3>%s</h3><div class="r"><svg viewBox="-110 -150 220 215" width="440" height="430"><g>%s</g></svg><svg viewBox="-110 -150 220 215" width="220" height="215"><g>%s</g></svg></div></div>' % (title, body, body)

def main():
    V = [('الف) رزوهٔ مارپیچ پیوسته روی بدنهٔ صاف، سنگ‌فرش', build(False, True, True, False, False)),
         ('ب) دندانهٔ مورب نامتقارن لبه + هاشور سایه', build(True, False, True, False, False)),
         ('ج) دندانهٔ مورب + مارپیچ کرم (طرح نقد)', build(True, True, True, False, False)),
         ('د) ج + دود حلزونی، مهره و پیچ و آچار کنار در', build(True, True, True, True, True))]
    html = '''<!doctype html><meta charset=utf-8><title>اتودهای ۲ پیچ‌کاری</title><style>
body{margin:0;background:#e9c57e;font-family:Vazirmatn,system-ui,sans-serif;direction:rtl;color:#241a5e;display:grid;grid-template-columns:repeat(2,auto);width:max-content}
.c{padding:10px 14px}.r{display:flex;gap:14px;align-items:flex-end}h3{margin:6px 0;font-size:16px}</style>''' + ''.join(cell(t, p.svg()) for t, p in V)
    (HERE / 'etudes2.html').write_text(html, encoding='utf-8')
    ch = sys.argv[1] if len(sys.argv) > 1 else 'د'
    p = dict((t[0], q) for t, q in V)[ch]
    hl = [SF(q) for q in ((24, -84), (24, -92))]
    sym = ('<symbol id="node_screw_workshop" viewBox="0 0 200 190" overflow="visible">'
           '<g id="node_screw_workshop_shadow" transform="translate(100 150)"><ellipse cx="8" cy="6" rx="102" ry="32" fill="#10083a" opacity=".25"/></g>'
           '<g id="node_screw_workshop_base" transform="translate(100 150)">' + p.svg() + '</g>'
           '<g id="node_screw_workshop_lit" transform="translate(100 150)"><path d="M%.1f,%.1f L%.1f,%.1f" stroke="#fff" stroke-width="3.2" stroke-linecap="round" fill="none" opacity=".9"/></g></symbol>' % (hl[0][0] + 5, hl[1][1] + 1, hl[0][0] + 16, hl[1][1] - 1))
    (HERE.parent / 'assets' / 'node_screw_workshop.svg').write_text(sym, encoding='utf-8')
main()
