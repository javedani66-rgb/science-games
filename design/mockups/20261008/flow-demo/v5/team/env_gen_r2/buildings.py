# ۱۲ بنای شاخص + ۱۶ پروپ. مختصات محلی: مرکز پایه (۰،۰)، بالا منفی.
import math
from shapes import *
CR, TL, VI, PK, BL, ST, ST2, WD, WD2, DV, GRN, GRN2, ICE = '#fff4d2', '#2fb8a8', '#8a4fd0', '#d070c0', '#5aa0e0', '#e9e4d6', '#c6c1b6', '#c98a45', '#a06a30', '#3a2a7a', '#7fbf4a', '#a6d86a', '#eaf8ff'
def ball(b, x, y, r, w=2.6):
    b.circ(x, y, r, '#fff', w)
    b.poly([(x, y - r * .45), (x + r * .43, y - r * .14), (x + r * .27, y + r * .36), (x - r * .27, y + r * .36), (x - r * .43, y - r * .14)], DV, 0)
def cog(b, x, y, r, fill, w=2.6, n=8):
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n; rr = r if i % 2 == 0 else r * .76
        for da in (-.12, .12): pts.append((x + rr * math.cos(a + da), y + rr * math.sin(a + da)))
    b.poly(pts, fill, w); b.circ(x, y, r * .3, '#fff4d2', w)
def n01():
    b = B('node_01'); pad(b, 'city', 70, 6)
    b.poly([(-62, -4), (58, -4), (58, -62)], WD, 4.5)
    for x in range(-44, 56, 20): b.line(x, -4, x, -4 - (x + 64) * .483 + 0, WD2, 1.2)
    b.rect(52, -66, 10, 62, ST2, 4.5, 2)
    ball(b, -8, -46, 14)
    b.line(-30, -22, -24, -26, '#fff', 1.2); b.line(26, -28, 34, -32, '#fff', 1.2)
    return b.svg((200, 190), 100, 150, 70, 24, (-64, -70, 62, 0))
def n02():
    b = B('node_02'); pad(b, 'sports', 90, 14)
    b.ell(0, 11, 68, 22, PK); b.rect(-68, 0, 136, 11, PK, 0, 0); b.ell(0, 0, 68, 22, ICE)
    b.ell(0, 0, 52, 16, '#a3d5ea', 2.6); b.path('M-34,4 Q-12,-8 20,6', 'none', 2.6)
    b.line(-30, -6, -6, -2, '#6ab7d8', 1.2); b.line(14, 6, 38, 2, '#6ab7d8', 1.2)
    b.rect(30, -44, 44, 34, CR, 4.5, 4); b.poly([(22, -44), (82, -44), (52, -96)], PK, 4.5); b.poly([(52, -96), (68, -44), (52, -44)], CR, 0)
    b.line(52, -96, 52, -116, 'var(--l-line,#241a5e)', 2.6); b.poly([(52, -116), (72, -109), (52, -102)], BL, 2.6)
    b.rect(45, -30, 14, 20, BL, 2.6, 3); b.window(32, -38, 8, 8); b.window(64, -38, 8, 8)
    b.circ(-34, -36, 7, '#ffd2a8', 2.6); b.poly([(-40, -29), (-28, -29), (-31, -12), (-37, -12)], TL, 2.6)
    b.line(-35, -12, -42, 0, 'var(--l-line,#241a5e)', 3); b.line(-31, -12, -22, -6, 'var(--l-line,#241a5e)', 3); b.line(-37, -24, -50, -30, 'var(--l-line,#241a5e)', 3); b.line(-30, -24, -18, -32, 'var(--l-line,#241a5e)', 3)
    return b.svg((200, 190), 100, 150, 80, 27, (-82, -118, 84, 14), True)
def n03():
    b = B('node_03'); pad(b, 'sports', 84, 2)
    b.path('M-70,-30 v30 a70,26 0 0 0 140,0 v-30 z', TL, 4.5); b.ell(0, -30, 70, 26, CR, 4.5); b.ell(0, -30, 54, 19, GRN, 2.6)
    for x in (-36, -12, 12, 36): b.line(x, -46, x, -14, GRN2, 1.2)
    b.ell(0, -30, 12, 5, 'none', 1.2); b.line(0, -49, 0, -11, '#fff', 1.2)
    for sx in (-1, 1):
        b.rect(sx * 74 - 3, -112, 6, 106, ST2, 4.5, 2); b.rect(sx * 74 - 15, -124, 30, 18, CR, 2.6, 3)
        for k in (-8, 0, 8): b.circ(sx * 74 + k, -115, 2.6, '#fff', 0)
        b.window(sx * 74 - 12, -121, 24, 12, 2)
    b.rect(-6, -2, 12, 6, DV, 2.6, 2)
    return b.svg((200, 190), 100, 150, 84, 28, (-96, -126, 96, 6))
def n04():
    b = B('node_04'); pad(b, 'space', 58, 8)
    b.rect(-6, -92, 12, 90, ST, 4.5, 3); b.rect(-24, -8, 48, 10, ST2, 2.6, 3)
    b.rect(-56, -100, 112, 9, TL, 4.5, 4); b.circ(0, -96, 8, VI, 2.6)
    for sx in (-1, 1):
        x = sx * 46; b.line(x, -92, x - 14, -56, 'var(--l-line,#241a5e)', 2.6); b.line(x, -92, x + 14, -56, 'var(--l-line,#241a5e)', 2.6)
        b.path('M%s,-56 a16,6 0 0 0 32,0 z' % f(x - 16), PK, 2.6)
    b.rect(-58, -76, 24, 20, WD, 2.6, 2); ball(b, 46, -66, 10)
    return b.svg((200, 190), 100, 150, 56, 19, (-60, -110, 60, 12))
def n05():
    b = B('node_05'); pad(b, 'space', 60, 9)
    b.poly([(-8, 0), (8, 0), (5, -52), (-5, -52)], WD, 4.5)
    b.path('M-6,-30 Q-26,-38 -30,-48', 'none', 3, clip=False); b.path('M5,-34 Q22,-42 26,-52', 'none', 3, clip=False)
    b.path('M-50,-70 Q-58,-96 -34,-102 Q-26,-120 0,-114 Q24,-122 36,-104 Q58,-98 50,-72 Q52,-50 28,-52 Q0,-44 -26,-52 Q-48,-50 -50,-70Z', GRN, 4.5)
    b.path('M-34,-90 Q-22,-104 -6,-100', 'none', 1.2, clip=False); b.path('M10,-104 Q24,-102 28,-90', 'none', 1.2, clip=False)
    for x, y in ((-26, -76), (4, -88), (30, -72)): b.circ(x, y, 6, PK, 2.6)
    b.circ(50, -34, 6, PK, 2.6); b.line(46, -52, 46, -42, '#fff', 1.2); b.line(52, -56, 52, -46, '#fff', 1.2)
    return b.svg((200, 190), 100, 150, 58, 20, (-58, -122, 58, 12))
def n06():
    b = B('node_06'); pad(b, 'space', 80, 10)
    b.rect(-72, -34, 28, 28, ST, 4.5, 8); b.rect(-76, -40, 36, 8, VI, 2.6, 3); b.window(-66, -26, 16, 10)
    b.rect(-46, -20, 22, 8, ST2, 2.6, 2)
    b.path('M-44,-6 a42,46 0 0 1 84,0 z', ST, 4.5); b.path('M-44,-6 a42,10 0 0 1 84,0 a42,10 0 0 0 -84,0 z', VI, 2.6) if False else None
    b.rect(-42, -28, 80, 8, VI, 2.6, 2); b.rect(-10, -22, 20, 16, TL, 2.6, 8)
    for x in (-24, 0, 22): b.wcirc(x, -48, 6); b.circ(x, -48, 6, '#9fdcf2', 2.6)
    b.line(60, -4, 60, -64, 'var(--l-line,#241a5e)', 4.5)
    b.path('M42,-82 a28,14 -30 0 0 38,16 z', ST, 4.5); b.line(66, -88, 66, -74, 'var(--l-line,#241a5e)', 2.6); b.circ(66, -90, 3.6, PK, 2.6)
    b.rect(44, -10, 32, 8, ST2, 2.6, 2)
    return b.svg((200, 190), 100, 150, 76, 26, (-78, -94, 82, 8))
def n07():
    b = B('node_07'); pad(b, 'city', 66, 11)
    b.poly([(-18, -3), (18, -3), (0, -36)], VI, 4.5)
    b.rect(-62, -8, 124, 11, WD, 4.5, 3, rot=(-14, 0, -32))
    b.line(-44, -26, -44, -40, 'var(--l-line,#241a5e)', 2.6); b.line(-52, -40, -36, -40, 'var(--l-line,#241a5e)', 2.6)
    b.rect(36, -22, 22, 20, BL, 2.6, 3, rot=(-14, 47, -12)); ball(b, -50, -62, 11)
    b.circ(0, -32, 6, ST, 2.6)
    return b.svg((200, 190), 100, 150, 64, 22, (-66, -78, 66, 4))
def n08():
    b = B('node_08'); pad(b, 'farm', 66, 4)
    b.poly([(-28, -4), (28, -4), (17, -76), (-17, -76)], CR, 4.5)
    for y in (-26, -48): b.line(-24 + (y + 4) * -.1, y, 24 - (y + 4) * -.1, y, '#aba16e', 1.2)
    b.path('M-22,-76 L22,-76 L0,-98Z', VI, 4.5); b.path('M-9,-4 v-16 a9,9 0 0 1 18,0 v16z', TL, 2.6); b.window(-5, -64, 10, 10, 2); b.window(-5, -42, 10, 10, 2)
    for a in (20, 110, 200, 290):
        b.rect(-5, -60, 10, 60, CR, 2.6, 2, rot=(a, 0, -80), clip=True) if False else None
    for a in (20, 110, 200, 290):
        b.raw('<g transform="rotate(%s 0 -80)"><rect x="-8" y="-136" width="16" height="48" rx="2" fill="%s" class="eo" stroke-width="2.6"/><path d="M0,-134V-90M-8,-122H8M-8,-108H8" fill="none" style="stroke:#aba16e" stroke-width="1.2"/></g>' % (a, CR))
        b.clip.append('<rect transform="rotate(%s 0 -80)" x="-8" y="-136" width="16" height="48"/>' % a)
    b.circ(0, -80, 8, WD, 4.5)
    return b.svg((200, 190), 100, 150, 66, 23, (-60, -142, 60, 0))
def n09():
    b = B('node_09'); pad(b, 'dirt', 52, 5)
    b.rect(-30, -34, 60, 34, WD, 4.5, 4); b.ell(0, -34, 30, 11, '#e0b070', 4.5); b.ell(0, -34, 18, 6, 'none', 1.2); b.ell(0, -34, 8, 3, 'none', 1.2)
    b.line(-26, -22, -26, -6, WD2, 1.2); b.line(20, -24, 20, -6, WD2, 1.2)
    b.poly([(2, -34), (10, -34), (26, -100), (18, -102)], WD2, 4.5)
    b.poly([(-16, -38), (6, -30), (8, -52), (-6, -60)], ST2, 4.5); b.line(-12, -42, 2, -36, TL, 2.6)
    b.poly([(34, -6), (42, -2), (38, -10)], WD, 1.2); b.poly([(-40, -4), (-33, 0), (-36, -8)], WD, 1.2)
    return b.svg((200, 190), 100, 150, 52, 18, (-48, -104, 48, 4))
# ---- ۳ جزیرهٔ شهر صنعتی = پورت مستقیم v4 (gen_head: s_pulley، b_factory، b_harbor) با پایهٔ سنگی/بتنی v4 (slab + سایهٔ قرصی)؛ مقیاس بزرگ‌تر، خط 4.5/2.6 ----
class Sc:
    """پوشش B که مختصات را ضرب می‌کند (ضخامت خط ثابت می‌ماند)"""
    def __init__(s, b, k): s.b = b; s.k = k
    def poly(s, pts, fill, w=4.5, **kw): s.b.poly([(x * s.k, y * s.k) for x, y in pts], fill, w, **kw)
    def rect(s, x, y, wd, h, fill, w=4.5, r=3, **kw): s.b.rect(x * s.k, y * s.k, wd * s.k, h * s.k, fill, w, r, **kw)
    def circ(s, x, y, r, fill, w=4.5, **kw): s.b.circ(x * s.k, y * s.k, r * s.k, fill, w, **kw)
    def ell(s, x, y, rx, ry, fill, w=4.5, **kw): s.b.ell(x * s.k, y * s.k, rx * s.k, ry * s.k, fill, w, **kw)
    def line(s, x1, y1, x2, y2, col='var(--l-line,#241a5e)', w=2.6): s.b.line(x1 * s.k, y1 * s.k, x2 * s.k, y2 * s.k, col, w)
    def path(s, d, fill='none', w=4.5, **kw): s.b.path(d, fill, w, **kw)
    def smoke(s, x, y, r, op=.85): s.b.raw('<circle cx="%s" cy="%s" r="%s" fill="#fff" opacity="%s"/>' % (f(x * s.k), f(y * s.k), f(r * s.k), op))
def v4slab(b, rx, ry, top, side, h, tick='#a46f36'):
    """slab v4: سایهٔ قرصی + دیوارهٔ ضخیم + رویهٔ بیضی؛ خط دور 5.5"""
    b.raw('<ellipse cx="8" cy="%s" rx="%s" ry="%s" fill="#10083a" opacity=".3"/>' % (f(h + 10), f(rx + 8), f(ry + 3)))
    b.path('M%s,0 v%s a%s,%s 0 0 0 %s,0 v-%s z' % (f(-rx), f(h), f(rx), f(ry), f(2 * rx), f(h)), side, 5.5)
    b.ell(0, 0, rx, ry, top, 5.5)
    for k in range(-4, 5): b.line(k * rx / 4.6, -ry * .5 + abs(k) * 1.5, k * rx / 4.6 + 6, ry * .55, tick, 1.2)
def n10():       # جزیرهٔ تیر چراغ/قرقره (v4 s_pulley، گره ۱۰)؛ مقیاس 1.5
    b = B('node_10'); k = 1.5; s = Sc(b, k); v4slab(b, 36 * k, 36 * k * .36, '#f6dba0', '#a8672f', 12)
    s.rect(-4, -56, 8, 56, '#2f9a55', 4.5); s.rect(-4, -58, 30, 8, '#2f9a55', 4.5)
    s.circ(22, -40, 8, '#fff6dc', 4.5); b.window(22 * k - 9, -40 * k - 9, 18, 18, 9)
    s.line(14, -40, 14, -24, '#6b4a22', 2.6); s.line(30, -40, 30, -34, '#6b4a22', 2.6)
    s.rect(8, -24, 14, 14, '#c98a45', 4.5, 2)
    return b.svg((200, 190), 100, 150, 56, 20, (-54, -90, 54, 12), True)
def n11(prefix='node_11', smoke=True):    # کارخانهٔ بزرگ آجری-چوبی (v4 b_factory، گره ۱۱)؛ مقیاس 1.5، دودکش بیرون‌زده از جزیره
    b = B(prefix); k = 1.5; s = Sc(b, k); v4slab(b, 80 * k, 80 * k * .36, '#cfd3e2', '#6e72a8', 17, '#9a9fc6')
    s.rect(-56, -46, 112, 46, '#c4502f', 4.5, 2)
    for x in range(-40, 50, 20): s.line(x, -46, x, 0, '#8e2c1a', 1.2)
    for y in (-30, -15): s.line(-56, y, 56, y, '#a8401f', 1.2)
    s.poly([(-56, -46), (-56, -66), (-30, -46), (-30, -66), (-4, -46), (-4, -66), (22, -46), (22, -66), (48, -46), (56, -46)], '#8a90c0', 4.5)
    s.rect(36, -100, 16, 54, '#7d4a2a', 4.5, 2); s.rect(-50, -86, 14, 42, '#7d4a2a', 4.5, 2)
    s.rect(33, -104, 22, 8, '#5a3418', 2.6, 2); s.rect(-53, -90, 20, 8, '#5a3418', 2.6, 2)
    if smoke:
        for x, y, r, op in ((44, -110, 8, .85), (52, -122, 10, .75), (-42, -96, 8, .8), (-36, -108, 6, .7)): s.smoke(x, y, r, op)
    cog(b, 0, -24 * k, 20 * k, '#ffd23f', 4.5, 8); s.rect(30, -22, 18, 22, '#241a5e', 2.6, 6)
    for x in (-44, -26, 14): s.rect(x, -40, 10, 8, '#9fdcf2', 2.6, 2); b.window(x * k, -40 * k, 10 * k, 8 * k)
    return b.svg((200, 190), 100, 150, 122, 44, (-124, -190, 124, 20), True)
def n12(prefix='node_12'):    # جزیرهٔ جرثقیل با قایق (v4 b_harbor، گره ۱۲)؛ مقیاس 1.25
    b = B(prefix); k = 1.25; s = Sc(b, k)
    s.poly([(-112, -34), (-30, -34), (-44, -12), (-98, -12)], '#1f7a45', 4.5); s.line(-108, -29, -34, -29, '#fff3c4', 3)
    s.rect(-92, -62, 42, 28, '#fff6dc', 4.5, 3); s.rect(-86, -55, 8, 9, '#8fe3f0', 2.6, 2); s.rect(-72, -55, 8, 9, '#8fe3f0', 2.6, 2)
    s.rect(-52, -52, 14, 18, '#1f7a45', 4.5, 2); s.smoke(-47, -62, 5, .9); s.smoke(-42, -72, 7, .8)
    s.line(-70, -62, -70, -88, 'var(--l-line,#241a5e)', 2.6); s.circ(-70, -90, 3.5, '#ffd23f', 2.6)
    v4slab(b, 78 * k, 78 * k * .36, '#f6dba0', '#a8672f', 14)
    s.rect(-60, -8, 12, 16, '#7a5026', 2.6, 2); s.path('M-54,-1 Q-70,-30 -92,-24', 'none', 2.6, clip=False)
    s.rect(42, -112, 13, 112, '#2f9a55', 4.5, 2); s.rect(-16, -118, 76, 10, '#2f9a55', 4.5, 2); s.poly([(42, -92), (42, -108), (4, -108)], '#2f9a55', 2.6)
    s.line(-8, -108, -8, -66, '#6b4a22', 2.6); s.rect(-21, -66, 26, 22, '#c98a45', 4.5, 3); s.line(-21, -66, 5, -44, '#6b4a22', 1.2); s.line(5, -66, -21, -44, '#6b4a22', 1.2)
    b.raw('<ellipse cx="%s" cy="%s" rx="9" ry="6" fill="#fff" class="eo" stroke-width="2.6"/><circle cx="%s" cy="%s" r="4.4" fill="#fff" class="eo" stroke-width="2.6"/><path d="M%s,%sl6,1 -6,2z" fill="#ff9d1c"/>' % (f(22 * k), f(-12 * k), f(28 * k), f(-17 * k), f(31 * k + 3), f(-17 * k)))
    return b.svg((200, 190), 100, 150, 98, 35, (-142, -150, 90, 22), True)
# پروپ‌ها (مرکز پایه (۰،۰)؛ viewBox ۱۲۰×۱۰۰ لنگر (۶۰،۷۸))
def prop(n, fn, rx=36):
    b = B('prop_%02d' % n); fn(b); return b.svg((120, 100), 60, 78, rx, 12, (-rx, -fn.h, rx, 4), True)
def p01(b): ball(b, 0, -20, 18, 4.5)
def p02(b):
    b.rect(-24, -42, 48, 42, WD, 4.5, 3); b.line(-24, -21, 24, -21, WD2, 2.6); b.line(0, -42, 0, 0, WD2, 2.6); b.rect(-10, -32, 20, 8, CR, 2.6, 2)
def p03(b):
    b.rect(-30, -22, 60, 22, WD, 4.5, 11); b.ell(-30, -11, 6, 11, '#e0b070', 2.6); b.rect(-24, -40, 52, 20, WD, 4.5, 10); b.ell(-24, -30, 5, 10, '#e0b070', 2.6)
def p04(b):
    b.rect(-24, -24, 48, 24, ST2, 4.5, 6); b.rect(-30, -34, 60, 12, ST, 4.5, 4); b.poly([(-8, -34), (8, -34), (6, -48), (-6, -48)], VI, 2.6); b.circ(0, -52, 6, VI, 4.5)
def p05(b):
    b.circ(0, -26, 26, WD, 4.5); b.circ(0, -26, 8, CR, 2.6)
    for a in range(0, 180, 45): b.line(26 * math.cos(math.radians(a)), -26 + 26 * math.sin(math.radians(a)), -26 * math.cos(math.radians(a)), -26 - 26 * math.sin(math.radians(a)), WD2, 2.6)
def p06(b):
    b.ell(0, -8, 30, 10, WD, 4.5); b.ell(0, -18, 24, 9, WD2, 4.5); b.ell(0, -27, 17, 7, WD, 4.5); b.path('M10,-28 Q34,-34 38, -12', 'none', 2.6, clip=False)
def p07(b):
    b.rect(-34, -12, 68, 12, WD, 4.5, 3); b.rect(-26, -24, 52, 12, WD2, 4.5, 3); b.line(-16, -24, -16, -12, '#e0b070', 1.2); b.line(14, -24, 14, -12, '#e0b070', 1.2)
def p08(b):
    b.rect(-3, -60, 6, 60, ST, 2.6, 2); b.poly([(3, -62), (30, -52), (3, -42)], BL, 4.5); b.poly([(3, -62), (16, -57), (3, -52)], CR, 0)
def p09(b):
    b.rect(-3, -48, 6, 48, ST2, 4.5, 2); b.rect(-16, -62, 32, 22, CR, 4.5, 3); b.rect(-8, -56, 16, 10, 'none', 2.6, 2); b.path('M-13,-40 q13,16 26,0', 'none', 4.5, clip=False)
def p10(b):
    b.line(-16, 0, -4, -26, WD2, 4.5); b.line(16, 0, 4, -26, WD2, 4.5)
    b.circ(0, -46, 20, CR, 4.5); b.circ(0, -46, 13, BL, 2.6); b.circ(0, -46, 6, PK, 2.6); b.circ(0, -46, 2, CR, 0)
def p11(b):
    b.rect(-22, -22, 44, 22, ST2, 4.5, 8); b.ell(0, -22, 22, 7, '#1f87b8', 4.5); b.line(-20, -22, -20, -52, WD2, 4.5); b.line(20, -22, 20, -52, WD2, 4.5)
    b.poly([(-28, -52), (28, -52), (0, -66)], VI, 4.5); b.line(0, -52, 0, -38, WD2, 2.6); b.rect(-5, -40, 10, 8, WD, 2.6, 2)
def p12(b):
    b.path('M-24,0 v-26 a24,24 0 0 1 48,0 v26 h-14 v-26 a10,10 0 0 0 -20,0 v26z', PK, 4.5); b.rect(-24, -8, 14, 8, ST, 2.6, 1); b.rect(10, -8, 14, 8, ST, 2.6, 1)
def p13(b):
    b.line(-20, -4, 16, -40, 'var(--l-line,#241a5e)', 12); b.line(-20, -4, 16, -40, TL, 6)
    b.circ(-22, -2, 10, TL, 4.5); b.circ(-22, -2, 4, CR, 2.6); b.circ(22, -44, 12, TL, 4.5); b.circ(22, -44, 5, CR, 2.6)
def p14(b):
    b.poly([(-14, -34), (14, -34), (10, -48), (-10, -48)], ST2, 4.5); b.rect(-7, -34, 14, 34, ST, 4.5, 2)
    for y in (-26, -16, -6): b.line(-7, y, 7, y + 4, ST2, 1.2)
def p15(b):
    b.rect(-14, -80, 28, 80, '#a8b4d8', 4.5, 3); b.rect(-18, -88, 36, 12, VI, 4.5, 3); b.poly([(-18, -88), (18, -88), (0, -108)], VI, 4.5)
    b.circ(0, -58, 11, CR, 4.5); b.line(0, -58, 0, -66, 'var(--l-line,#241a5e)', 2.6); b.line(0, -58, 6, -56, 'var(--l-line,#241a5e)', 2.6); b.window(-4, -26, 8, 12)
    b.window(-10, -76, 6, 6)
def p16(b):
    b.rect(-40, -40, 14, 40, ST, 4.5, 2); b.rect(26, -40, 14, 40, ST, 4.5, 2); b.path('M-40,-38 a40,36 0 0 1 80,0 v8 h-14 v-8 a26,22 0 0 0 -52,0 v8 h-14z', CR, 4.5)
    b.rect(-6, -72, 12, 8, VI, 2.6, 2)
for n, fn, h in ((1, p01, 40), (2, p02, 44), (3, p03, 40), (4, p04, 58), (5, p05, 52), (6, p06, 38), (7, p07, 36), (8, p08, 64), (9, p09, 64), (10, p10, 66), (11, p11, 66), (12, p12, 50), (13, p13, 58), (14, p14, 48), (15, p15, 108), (16, p16, 72)): fn.h = h
PROPS = {n: globals()['p%02d' % n] for n in range(1, 17)}
LAND = {1: n01, 2: n02, 3: n03, 4: n04, 5: n05, 6: n06, 7: n07, 8: n08, 9: n09, 10: n10, 11: n11, 12: n12}
