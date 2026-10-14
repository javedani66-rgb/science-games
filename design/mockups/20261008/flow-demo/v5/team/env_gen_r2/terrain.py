# r2: زمین/آب/یخ/ابر/درخت/تونل با پالت و ظاهر v4 (قابل خواندن در V4_RESTORE_BRIEF_FA.md)
# فیلتر زنده نیست: لبهٔ نرم زمین‌ها با چند لایهٔ نیم‌شفاف موجی پخته شده؛ دست‌لرزی (wob) فقط در صفحهٔ بازبینی روی خط ≥4.5.
import math, random
from shapes import *
import layout as L
SVGH = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s">'
LINE = 'var(--l-line,#241a5e)'
OUTC = '#241a5e'
# ---- پالت v4 (gen_head.py: Z) + رنگ‌های کمکی هم‌خانواده ----
ZC = {
 'sports': dict(base='#3f9a2b', shade='#2f7f21', patch='#56b13e'),
 'space': dict(base='#c4502f', shade='#a63f22', patch='#d9683f'),
 'farm': dict(base='#9a8a10', shade='#7f730c', patch='#b3a31c'),
 'city': dict(base='#075a73', shade='#06506a', patch='#0a6e8a'),     # دریا (v4: sea)
}
SAND, YARD, YARD_D, YARD_L = '#f0cf7a', '#c9a35c', '#a98343', '#dbb872'
WA = dict(river='#58d8ee', river_hi='#d4f6ff', river_lip='#1f87b8', river_deep='#2aa6c8')
IC = dict(body='#9fd8f0', rim='#eaf8ff', facet='#c9ecfb', crack='#4a9cc8', shard='#ffffff')
COAST_Y = 1385        # ساحل: بالا = دریا، پایین = خشکی شهر
def wavy_pts(y, amp, step, seed, x0=-20, x1=410):
    r = random.Random(seed); pts = []; x = x0
    while x <= x1 + step: pts.append((x, y + r.uniform(-amp, amp))); x += step
    return pts
def smooth_d(pts):
    d = 'M%s,%s' % (f(pts[0][0]), f(pts[0][1]))
    for i in range(1, len(pts)):
        m = ((pts[i-1][0] + pts[i][0]) / 2, (pts[i-1][1] + pts[i][1]) / 2); d += ' Q%s,%s %s,%s' % (f(pts[i-1][0]), f(pts[i-1][1]), f(m[0]), f(m[1]))
    return d + ' L%s,%s' % (f(pts[-1][0]), f(pts[-1][1]))
def band(ytop, h, amp, step, seed, fill, op=1, extra=''):
    d = smooth_d(wavy_pts(ytop, amp, step, seed)); return '<path d="%s L420,%s L-30,%s Z" fill="%s" opacity="%s" %s/>' % (d, h + 6, h + 6, fill, op, extra)
def blobp(cx, cy, rx, ry, fill, op, seed):
    return '<path transform="translate(%s %s)" d="%s" fill="%s" opacity="%s"/>' % (f(cx), f(cy), blob(rx, ry, 11, .22, seed), fill, op)
def wave_glyph(x, y, s=1, col='#aef0f4', op=.32):
    return '<path d="M%s,%s q%s,-%s %s,0 t%s,0 t%s,0" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round" opacity="%s"/>' % (f(x), f(y), f(6 * s), f(7 * s), f(12 * s), f(12 * s), f(12 * s), col, op)
def crater(x, y, r):
    return ('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#8e2c1a" opacity=".35"/><ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="#ffb08a" stroke-width="2" opacity=".35"/>'
            % (f(x), f(y), f(r), f(r * .45), f(x), f(y - 1.5), f(r), f(r * .45)))
def strip(zone, y0, y1, top_soft):
    """نوار زمین [y0,y1]. soft: ۹۰px بالاتر شروع می‌شود و با ۷ لایهٔ نیم‌شفاف موجی در زمین قبلی محو می‌شود (لبهٔ نرم v4 بدون فیلتر)."""
    z = ZC[zone]; ext = 90 if top_soft else 0; h = y1 - y0 + ext; r = random.Random(hash(zone) % 999 + 5); o = [SVGH % (390, h)]
    s0 = sum(map(ord, zone))
    if top_soft:
        for j in range(7): o.append(band(ext - 6 - j * 13, h, 20, 56, j * 7 + s0, z['base'], .22))
        o.append(band(ext - 2, h, 10, 70, 99 + s0, z['base'], 1))
    else: o.append('<rect x="-2" y="0" width="394" height="%s" fill="%s"/>' % (h + 1, z['base']))
    g = []
    n = int(h / 210) + 2
    for i in range(n):
        cy = ext + (i + .5) * (h - ext) / n + r.uniform(-30, 30)
        g.append(blobp(r.choice([40, 330, 190, 90, 300]), cy, r.uniform(80, 150), r.uniform(26, 50), z['shade'], .45, i * 3 + 1))
        g.append(blobp(r.choice([300, 70, 210, 340]), cy + r.uniform(40, 100), r.uniform(60, 120), r.uniform(18, 36), z['patch'], .4, i * 3 + 2))
    if zone == 'sports':     # خط‌کشی چمن (v4: نوار سفید کم‌رنگ)
        for yy in range(ext + 20, h, 62): g.append('<path d="%s L420,%s L-30,%s Z" fill="#fff" opacity=".05"/>' % (smooth_d(wavy_pts(yy, 4, 80, yy)), yy + 30, yy + 30))
    if zone == 'space':
        for k in range(int((h - ext) / 90)): g.append(crater(r.uniform(20, 370), ext + 30 + r.uniform(0, h - ext - 60), 14 + r.random() * 18))
        for k in range(16): g.append('<circle cx="%s" cy="%s" r="%s" fill="#fff" opacity=".5"/>' % (r.randint(8, 382), ext + r.randint(8, h - ext - 8), f(r.random() * 1.5 + .8)))
    if zone == 'farm':        # شیار کشت (v4)
        for yy in range(ext + 14, h, 26): g.append('<path d="M-10,%s Q100,%s 200,%s T400,%s" fill="none" stroke="#fff" stroke-width="5" opacity=".08"/>' % (yy, yy - 8, yy + 4, yy - 3))
    if zone == 'city':
        sea_h = COAST_Y
        for k in range(int(sea_h / 95)): g.append(wave_glyph(r.uniform(10, 360), 20 + r.uniform(0, sea_h - 30), 1.1))
        # خشکی شهر: ساحل شنی + حیاط بندری (رنگ‌های شنی v4)
        coast = wavy_pts(COAST_Y, 16, 46, 41)
        d = smooth_d(coast)
        g.append('<path d="%s L420,%s L-30,%s Z" fill="#ffffff" opacity=".55" transform="translate(0 -9)"/>' % (d, h + 6, h + 6))              # کف دریا
        g.append('<path d="%s L420,%s L-30,%s Z" fill="%s" transform="translate(0 -3)"/>' % (d, h + 6, h + 6, SAND))
        g.append('<path d="%s L420,%s L-30,%s Z" fill="%s" transform="translate(0 16)"/>' % (d, h + 6, h + 6, YARD))
        # لکه‌های حیاط، خیابان‌ها، بلوک‌ها
        for i in range(int((h - COAST_Y) / 190)):
            cy = COAST_Y + 90 + i * 190 + r.uniform(-30, 30)
            g.append(blobp(r.choice([60, 330, 200, 120]), cy, r.uniform(80, 130), r.uniform(30, 52), YARD_D, .4, i * 5 + 3))
            g.append(blobp(r.choice([300, 80, 220]), cy + 80, r.uniform(60, 110), r.uniform(22, 40), YARD_L, .45, i * 5 + 4))
        for i in range(int((h - COAST_Y) / 150)):
            bx = r.choice([34, 140, 250, 330]); by = COAST_Y + 60 + r.uniform(0, h - COAST_Y - 160)
            g.append('<rect x="%s" y="%s" width="%s" height="%s" rx="8" fill="%s" opacity=".5"/>' % (f(bx - 30), f(by), r.randint(52, 84), r.randint(34, 58), YARD_D))
        for k in range(46): g.append('<circle cx="%s" cy="%s" r="1.6" fill="%s" opacity=".55"/>' % (r.randint(6, 384), r.randint(COAST_Y + 30, h - 20), YARD_D))
    o.append(''.join(g)); o.append('</svg>'); return ''.join(o)
def farm_beach(h):
    """نوار شنی روی لبهٔ بالای مزرعه (در نوار مزرعه ادغام نمی‌شود؛ جدا نیست: strip مزرعه نرم است)"""
    return ''
# ---------- رود: عرض متغیر، موج، بدون خط وسط (ایراد ۳ v4) ----------
def river_center(x): return 40 + .345 * max(0, 390 - x) + 9 * math.sin(x / 45 + .5)
def river_dy(x): return -.345 * (1 if x < 390 else 0) + 9 / 45 * math.cos(x / 45 + .5)
def river_w(x): return 20 + 30 * (max(0, 390 - x) / 390) ** 1.3 + 4 * math.sin(x / 31)
def river():
    xs = list(range(-10, 401, 8)); up, dn = [], []
    for x in xs:
        y = river_center(x); w = river_w(x) / 2; dy = river_dy(x); n = math.hypot(1, dy); nx, ny = -dy / n, 1 / n
        up.append((x - nx * w, y - ny * w)); dn.append((x + nx * w, y + ny * w))
    P = lambda pts: ' L'.join('%s,%s' % (f(a), f(b)) for a, b in pts)
    body = 'M' + P(up) + ' L' + P(list(reversed(dn))) + 'Z'
    pond = blob(52, 40, 12, .12, 4); px, py = 38, river_center(38) + 3
    o = [SVGH % (390, 260), '<g id="env_river_g">']
    # لبهٔ خاکی/ساحل تیره زیر آب (سایه)، سپس آب، سپس خط دور 4.5
    o.append('<path transform="translate(%s %s)" d="%s" fill="#6b4a22" opacity=".45" stroke="#6b4a22" stroke-width="9" stroke-linejoin="round"/>' % (px + 2, py + 4, pond))
    o.append('<path d="%s" fill="#6b4a22" opacity=".45" stroke="#6b4a22" stroke-width="9" stroke-linejoin="round" transform="translate(2 4)"/>' % body)
    o.append('<path transform="translate(%s %s)" d="%s" fill="%s" class="eo" stroke-width="4.5"/>' % (px, py, pond, WA['river']))
    o.append('<path d="%s" fill="%s" class="eo" stroke-width="4.5"/>' % (body, WA['river']))
    o.append('<path transform="translate(%s %s)" d="%s" fill="%s"/>' % (px, py, blob(34, 24, 12, .12, 5), WA['river_deep']))
    # کف تیره‌تر نزدیک ساحل پایین + رگه‌های روشن بالا (جریان)
    o.append('<path d="M%s L%s Z" fill="%s" opacity=".7"/>' % (P(dn[8:-6]), P(list(reversed([(a, b - river_w(a) * .28) for a, b in dn[8:-6]]))), WA['river_deep']))
    r = random.Random(9)
    for k in range(11):
        x = 36 + k * 33 + r.uniform(-8, 8); y = river_center(x) + r.uniform(-river_w(x) * .25, river_w(x) * .25); wv = r.choice([10, 14, 18])
        o.append('<path d="M%s,%s q%s,-4 %s,0 q%s,4 %s,0" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".9"/>' % (f(x), f(y), f(wv / 4), f(wv / 2), f(wv / 4), f(wv / 2)))
    o.append('<path d="M20,%s q8,-4 16,0 M52,%s q8,-4 16,0 M34,%s q8,-4 16,0" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"/>' % (f(py + 12), f(py - 10), f(py + 2)))
    # سنگ و نیلوفر
    for (x, dy) in ((120, 7), (250, -9)):
        yy = river_center(x) + dy; o.append('<ellipse cx="%s" cy="%s" rx="7" ry="4" fill="#9fdba8" class="eo" stroke-width="2.6"/><path d="M%s,%s l6,0" stroke="#241a5e" stroke-width="1.2"/>' % (x, f(yy), x - 1, f(yy)))
    o.append('</g></svg>'); return ''.join(o)
def bridge():
    o = [SVGH % (120, 70), CSS]
    o.append('<rect x="8" y="12" width="104" height="46" rx="3" fill="#10083a" opacity=".3"/>')
    o.append('<rect x="6" y="18" width="108" height="34" rx="3" fill="#c98a45" class="eo" stroke-width="4.5"/>')
    for x in range(16, 108, 12): o.append('<path d="M%s,19V51" stroke="#8f5a2e" stroke-width="1.8"/>' % x)
    for y in (14, 56):
        o.append('<path d="M8,%s H112" class="eo" fill="none" stroke-width="4.5"/>' % y)
        for x in (12, 60, 108): o.append('<rect x="%s" y="%s" width="7" height="9" rx="1.5" fill="#e2a95d" class="eo" stroke-width="2.6"/>' % (x - 3.5, y - 4.5))
    o.append('</svg>'); return ''.join(o)
# ---------- یخ: چندضلعی تیز و شکافدار آبی-سفید (ایراد ۲ v4)؛ ابر گرد جداست ----------
def ice_poly():
    return [(4, 84), (30, 46), (50, 56), (74, 14), (104, 40), (132, 8), (160, 38), (188, 10), (226, 44), (256, 24), (292, 70), (270, 96), (294, 124), (240, 132), (214, 150), (178, 124), (140, 148), (104, 120), (62, 142), (40, 112), (6, 118)]
def ice():
    P = ice_poly(); pts = lambda q: ' '.join('%s,%s' % (f(a), f(b)) for a, b in q)
    o = [SVGH % (300, 156), CSS, '<defs><clipPath id="env_ice_clip"><polygon points="%s"/></clipPath></defs>' % pts(P)]
    o.append('<polygon points="%s" fill="#10083a" transform="translate(5 7)" opacity=".3"/>' % pts(P))
    o.append('<polygon points="%s" fill="%s" class="eo" stroke-width="4.5"/>' % (pts(P), IC['body']))
    o.append('<g clip-path="url(#env_ice_clip)">'
             '<polygon points="0,0 300,0 256,24 226,44 188,10 160,38 132,8 104,40 74,14 50,56 30,46 4,84 0,100" fill="%s"/>'
             '<polygon points="30,70 110,52 150,92 84,112" fill="%s"/><polygon points="196,56 262,74 230,116 176,98" fill="%s"/>'
             '<polygon points="110,100 176,98 214,150 140,148" fill="#7fc0e6" opacity=".65"/></g>' % (IC['rim'], IC['facet'], IC['facet']))
    o.append('<polygon points="%s" fill="none" class="eo" stroke-width="4.5"/>' % pts(P))
    for d in ('M56,58 L100,84 L92,110 L112,126', 'M150,40 L170,78 L210,88 L226,122', 'M240,70 L214,94 L196,130', 'M110,84 L142,104 L140,140', 'M20,104 L58,92'):
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.2" stroke-linejoin="miter" stroke-linecap="round"/>' % (d, IC['crack']))
    for x, y in ((76, 36), (150, 28), (238, 58), (126, 70)): o.append('<path d="M%s,%s l6,-6 M%s,%s l-6,-6 M%s,%s v-9" stroke="#fff" stroke-width="2" stroke-linecap="round"/>' % (x, y, x, y, x, y))
    o.append('</svg>'); return ''.join(o)
# ---------- ابر گرد (v4: دایره‌های هم‌پوشان با خط دور) ----------
CLOUDS = {
 'a': [(-18, 2, 12), (-4, -6, 16), (14, -2, 13), (28, 4, 9), (4, 6, 14)],
 'b': [(-24, 4, 10), (-10, -4, 15), (8, -10, 18), (26, -2, 14), (38, 6, 9), (6, 8, 13), (-10, 8, 12)],
 'c': [(-12, 2, 11), (4, -6, 15), (20, 2, 11), (4, 6, 12)],
}
def cloud_sym(k):
    cs = CLOUDS[k]; o = [SVGH % (110, 56), '<g transform="translate(52 30)">']
    o.append(''.join('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (a, b, r + 2.6, OUTC) for a, b, r in cs))
    o.append(''.join('<circle cx="%s" cy="%s" r="%s" fill="#fff"/>' % (a, b, r) for a, b, r in cs))
    o.append('<path d="M-18,12 Q4,18 30,10" fill="none" stroke="#cfe6f6" stroke-width="3" stroke-linecap="round"/></g></svg>'); return ''.join(o)
# ---------- درخت‌های متنوع (ایراد ۷ v4)؛ خط 2.6 (تزئین) ----------
def tree_syms():
    T = {}
    def mk(name, vb, ox, oy, rx, bbox, fn):
        b = B('env_' + name); fn(b); T[name] = b.svg(vb, ox, oy, rx, 7, bbox, False)
    def pine(b):
        b.rect(-4, -10, 8, 12, '#8f5a2e', 2.6, 1)
        for i, (w, y, c) in enumerate(((28, -6, '#1f7a45'), (22, -28, '#2a8a58'), (15, -48, '#38a06a'))): b.poly([(-w, y), (w, y), (0, y - 34)], c, 2.6)
        b.poly([(-6, -76), (0, -88), (6, -76)], '#fff', 0, clip=False)
    def pop(b):
        b.rect(-3, -10, 6, 12, '#8f5a2e', 2.6, 1); b.path('M0,-10 C-16,-20 -18,-62 0,-92 C18,-62 16,-20 0,-10Z', '#4fa832', 2.6); b.path('M-2,-30 C-10,-44 -6,-68 0,-80 C-4,-60 -4,-44 -2,-30Z', '#8de06c', 0, clip=False)
    def round_(b):
        b.rect(-3, -4, 6, 14, '#8f5a2e', 2.6, 1); b.circ(0, -24, 20, '#2f8a2b', 2.6); b.circ(-8, -30, 9, '#6fcf5e', 0, clip=False); b.circ(9, -20, 5, '#4fa832', 0, clip=False)
    def oak(b):
        b.rect(-5, -18, 10, 22, '#7a5026', 2.6, 1); b.circ(-14, -30, 14, '#3f9a2b', 2.6); b.circ(14, -30, 14, '#3f9a2b', 2.6); b.circ(0, -42, 17, '#4fb33a', 2.6); b.circ(-4, -46, 6, '#8de06c', 0, clip=False)
    def birch(b):
        b.rect(-3, -50, 6, 54, '#f4f0e0', 2.6, 1); b.line(-2, -30, 2, -30, '#241a5e', 1.6); b.line(-2, -18, 2, -18, '#241a5e', 1.6); b.line(-2, -40, 2, -40, '#241a5e', 1.6)
        b.circ(0, -62, 15, '#9be08a', 2.6); b.circ(-9, -50, 9, '#b9eaa0', 2.6); b.circ(8, -48, 8, '#b9eaa0', 2.6)
    def autumn(b):
        b.rect(-3, -6, 6, 14, '#7a5026', 2.6, 1); b.circ(0, -24, 20, '#e9a23a', 2.6); b.circ(-8, -30, 8, '#ffd23f', 0, clip=False); b.circ(9, -18, 6, '#d9682f', 0, clip=False)
    def palm(b):
        b.path('M-2,4 C-6,-20 4,-38 2,-56 L7,-56 C9,-36 2,-20 6,4Z', '#c98a45', 2.6)
        for a in (-150, -110, -70, -30): b.path('M4,-56 q%s,%s %s,%s q-%s,2 -%s,-1Z' % (30 * math.cos(math.radians(a)), 20 * math.sin(math.radians(a)) - 16, 40 * math.cos(math.radians(a)), 26 * math.sin(math.radians(a)) + 6, 12, 36 * math.cos(math.radians(a)) * .4), '#2fa44a', 2.6)
        b.circ(2, -52, 4, '#8f5a2e', 2.6)
    def bush(b):
        b.path('M-22,0 Q-30,-14 -16,-20 Q-14,-34 2,-30 Q18,-38 22,-20 Q34,-14 24,0Z', '#4fa832', 2.6); b.circ(-8, -18, 5, '#8de06c', 0, clip=False); b.circ(10, -16, 3, '#e5496e', 0, clip=False)
    mk('tree_pine', (80, 100), 40, 92, 22, (-28, -90, 28, 4), pine); mk('tree_pop', (60, 100), 30, 94, 16, (-18, -92, 18, 4), pop)
    mk('tree_round', (70, 70), 35, 56, 20, (-22, -46, 22, 8), round_); mk('tree_oak', (80, 80), 40, 66, 28, (-30, -60, 30, 6), oak)
    mk('tree_birch', (60, 100), 30, 90, 14, (-18, -76, 18, 4), birch); mk('tree_autumn', (70, 70), 35, 56, 20, (-22, -46, 22, 8), autumn)
    mk('tree_palm', (90, 100), 45, 90, 18, (-34, -70, 38, 4), palm); mk('tree_bush', (70, 60), 35, 52, 24, (-26, -40, 26, 4), bush)
    return T
TREE_SZ = {'tree_pine': (80, 100, 40, 92), 'tree_pop': (60, 100, 30, 94), 'tree_round': (70, 70, 35, 56), 'tree_oak': (80, 80, 40, 66), 'tree_birch': (60, 100, 30, 90), 'tree_autumn': (70, 70, 35, 56), 'tree_palm': (90, 100, 45, 90), 'tree_bush': (70, 60, 35, 52)}
# ---------- تونل: رشته‌کوه بین دو ردیف مسیر، مسیر از دهانهٔ سنگی به داخل می‌رود (ایراد ۶ v4) ----------
def tunnel(hb, ht, xm, seed=4):
    """رشته‌کوه با ارتفاع ht..hb (نسبت به بالای نماد)، دهانهٔ تونل در پایین، مرکز دهانه xm؛ پیکره 390×(hb+34)."""
    b = B('env_tunnel'); r = random.Random(seed); Hh = hb + 34; base = hb
    # قله‌ها
    xs = [-20, 40, 100, 160, 215, 275, 330, 400]; tops = [ht + 36, ht + 10, ht + 40, ht, ht + 34, ht + 8, ht + 30, ht + 44]
    pts = [(-20, base)]
    for x, t in zip(xs, tops): pts.append((x, t + r.uniform(-4, 4)))
    pts.append((410, base))
    wob_bot = [(x, base - 2 + 3 * math.sin(x / 23.0)) for x in range(410, -30, -26)]
    poly = pts + wob_bot
    b.poly(poly, '#c98a45', 4.5)
    # روشن/سایه: هر قله دو رخ
    for i in range(1, len(xs) - 0):
        px, py = pts[i]
        if 1 <= i <= len(xs):
            b.poly([(px, py), (px + 34, base - 8), (px + 4, base - 8)], '#8f5a2e', 0, clip=False)
            b.poly([(px, py), (px - 30, base - 8), (px - 2, base - 8)], '#e2a95d', 0, clip=False)
    for i in (2, 4, 6):          # قلهٔ برفی
        px, py = pts[i]; b.poly([(px - 14, py + 16), (px, py), (px + 14, py + 16), (px + 6, py + 12), (px, py + 18), (px - 6, py + 12)], '#fff', 0, clip=False)
    b.poly(poly, 'none', 4.5)
    # لایه‌های سنگ
    for k in range(7):
        x = r.uniform(10, 380); y = r.uniform(ht + 60, base - 14); b.line(x, y, x + r.uniform(14, 28), y + r.uniform(-2, 4), '#8f5a2e', 1.2)
    # دهانهٔ سنگی: قاب کرم + دهان تیره + حلقهٔ عمق + کلید سنگ
    W2, Ht = 30, 62; yb = base + 6
    b.rect(xm - W2 - 8, yb - Ht - 10, 2 * W2 + 16, Ht + 22, '#e9e4d6', 4.5, 4)                     # دیوار سنگی پشت
    b.path('M%s,%s v-%s a%s,%s 0 0 1 %s,0 v%s z' % (f(xm - W2 - 8), f(yb + 12), f(Ht - 10), f(W2 + 8), f(W2 + 10), f(2 * W2 + 16), f(Ht - 10 + 12)), '#fff3c4', 4.5)
    b.path('M%s,%s v-%s a%s,%s 0 0 1 %s,0 v%s z' % (f(xm - W2 + 4), f(yb + 12), f(Ht - 16), f(W2 - 4), f(W2 + 2), f(2 * W2 - 8), f(Ht - 16 + 12)), '#1a0f40', 4.5)
    b.path('M%s,%s v-%s a%s,%s 0 0 1 %s,0 v%s z' % (f(xm - W2 + 14), f(yb + 12), f(Ht - 24), f(W2 - 14), f(W2 - 8), f(2 * W2 - 28), f(Ht - 24 + 12)), '#3a2a7a', 0, clip=False)
    for k in range(-3, 4):      # سنگ‌چین دور قوس
        a = math.radians(90 + k * 24); cx0, cy0 = xm, yb - Ht + 14 + 8
        b.line(cx0 + (W2 - 2) * math.cos(a), cy0 - (W2 + 4) * math.sin(a), cx0 + (W2 + 12) * math.cos(a), cy0 - (W2 + 20) * math.sin(a), OUTC, 1.8)
    b.rect(xm - 8, yb - Ht - 24, 16, 14, '#ffd23f', 2.6, 3)          # کلید سنگ زرد
    b.circ(xm - W2 - 14, yb - 14, 4, '#ffd23f', 2.6); b.circ(xm + W2 + 14, yb - 14, 4, '#ffd23f', 2.6)    # چراغ‌ها
    return b.svg((390, Hh), 0, 0, 120, 6, (0, ht, 390, hb), False), Hh
# ---------- دریا: تزئین دریایی (به‌جای تزئین شهری) ----------
def sea_decor():
    D = {}
    def mk(n, fn, vb=(120, 120), ox=60, oy=96, rx=24, bbox=(-30, -70, 30, 4), win=False):
        b = B('env_dec_city_' + n); fn(b); D['dec_city_' + n] = b.svg(vb, ox, oy, rx, 6, bbox, win)
    def buoy(b):
        b.line(0, -20, 0, -50, LINE, 2.6); b.circ(0, -52, 4, '#ffd23f', 2.6); b.ell(0, -12, 16, 16, '#fff', 2.6); b.path('M-16,-12 a16,16 0 0 1 32,0z', '#ff4b4b', 2.6); b.line(-16, -12, 16, -12, LINE, 1.2)
    def sail(b):
        b.poly([(-26, -8), (26, -8), (18, 6), (-18, 6)], '#e5496e', 2.6); b.line(0, -8, 0, -52, LINE, 2.6); b.poly([(2, -50), (22, -14), (2, -14)], '#fff', 2.6); b.poly([(-2, -44), (-20, -14), (-2, -14)], '#ffd23f', 2.6)
    def islet(b):
        b.poly([(-26, 2), (-20, -10), (-6, -18), (8, -12), (24, -4), (28, 2)], '#8a90c0', 2.6); b.poly([(-6, -18), (8, -12), (2, -2)], '#c9cfe6', 0, clip=False)
        b.ell(10, -16, 6, 4, '#fff', 2.6); b.circ(16, -20, 3, '#fff', 2.6)
    def lighthouse(b):
        b.poly([(-26, 2), (-16, -8), (20, -8), (28, 2)], '#8a90c0', 2.6); b.poly([(-10, -8), (10, -8), (6, -52), (-6, -52)], '#fff', 2.6); b.poly([(-8, -30), (8, -30), (7, -38), (-7, -38)], '#e5496e', 0, clip=False)
        b.rect(-8, -62, 16, 10, '#ffd23f', 2.6, 2); b.poly([(-10, -62), (10, -62), (0, -72)], '#e5496e', 2.6)
    def crate(b):
        b.rect(-14, -18, 28, 20, '#c98a45', 2.6, 2); b.line(-14, -18, 14, 2, '#8f5a2e', 1.2); b.line(14, -18, -14, 2, '#8f5a2e', 1.2); b.rect(-24, -8, 14, 10, '#a8672f', 2.6, 2)
    mk('buoy', buoy, rx=18); mk('sail', sail, rx=28); mk('islet', islet, rx=28); mk('lighthouse', lighthouse, rx=28); mk('crate', crate, rx=24)
    return D
