# زمین/آب/یخ/آسمان و تزئین‌ها
import math, random, json
from shapes import *
import layout as L
Z = json.load(open(L.HERE.parent / 'assets' / 'light' / 'zone_tokens.json'))
ZC, WA, IC = Z['zones'], Z['water'], Z['ice']
SVGH = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s">'
LINE = 'var(--l-line,#241a5e)'
def wavy(y, w=390, amp=10, step=30, seed=0, x0=-10):
    r = random.Random(seed); pts = []; x = x0
    while x <= w + step: pts.append((x, y + r.uniform(-amp, amp))); x += step
    d = 'M%s,%s' % (f(pts[0][0]), f(pts[0][1]))
    for i in range(1, len(pts)):
        m = ((pts[i-1][0] + pts[i][0]) / 2, (pts[i-1][1] + pts[i][1]) / 2); d += ' Q%s,%s %s,%s' % (f(pts[i-1][0]), f(pts[i-1][1]), f(m[0]), f(m[1]))
    return d, pts[-1]
def soft_blob(cx, cy, rx, ry, fill, op, seed):
    return '<path transform="translate(%s %s)" d="%s" fill="%s" opacity="%s"/>' % (f(cx), f(cy), blob(rx, ry, 10, .22, seed), fill, op)
def strip(zone, y0, y1, top_soft):
    """نوار زمین: [y0,y1] ناحیهٔ زمین؛ اگر top_soft، ۹۰px بالاتر شروع و با نوارهای نیم‌شفاف محو می‌شود."""
    z = ZC[zone]; ext = 90 if top_soft else 0; h = y1 - y0 + ext; r = random.Random(hash(zone) % 999 + 5)
    o = [SVGH % (390, h)]
    soft = ''
    if top_soft:
        for j in range(5):
            d, _ = wavy(ext - 14 - j * 16 + 10, seed=j + 7 + len(zone))
            soft += '<path d="%s L400,%s L-10,%s Z" fill="%s" opacity=".3"/>' % (d, h + 5, h + 5, z['base'])
        body_top = ext - 4
    else: body_top = 0
    o.append(soft + '<rect x="-2" y="%s" width="394" height="%s" fill="%s"/>' % (body_top, h - body_top + 1, z['base']))
    # لکه‌های بزرگ کم‌کنتراست: سایه و روشن
    n = int(h / 230) + 2
    for i in range(n):
        cy = ext + (i + .5) * (h - ext) / n + r.uniform(-30, 30)
        o.append(soft_blob(r.choice([50, 330, 190, 90, 300]), cy, r.uniform(70, 130), r.uniform(26, 50), z['shade'], .5, i * 3 + 1))
        o.append(soft_blob(r.choice([300, 80, 210, 340]), cy + r.uniform(40, 100), r.uniform(50, 110), r.uniform(18, 36), z['patch'], .45, i * 3 + 2))
    if zone == 'sports':     # خط‌کشی چمن
        for k in range(int(h / 76)):
            y = ext + 20 + k * 76 + (0 if k % 2 == 0 else 0)
            d, _ = wavy(y, amp=5, seed=k); o.append('<path d="%s L400,%s L-10,%s Z" fill="%s" opacity=".22"/>' % (d, y + 38, y + 38, z['patch']))
    if zone == 'farm':
        for k in range(int((h - ext) / 24)):
            y = ext + 12 + k * 24
            o.append('<path d="M-10,%s Q100,%s 200,%s T400,%s" fill="none" stroke="%s" stroke-width="5" opacity=".55"/>' % (y, y - 8, y + 4, y - 3, z['patch']))
    if zone == 'city':       # خیابان‌ها، بلوک‌ها، میدانک‌ها؛ فقط lit/shade/لکه، پایه عوض نمی‌شود
        ys = []
        for k in range(14):
            y = 520 + k * 190 + r.uniform(-20, 20)
            if y < h - 40:
                ys.append(y); o.append('<rect x="-4" y="%s" width="398" height="12" fill="%s" opacity=".3"/><path d="M-4,%s H394" stroke="#fff4d2" stroke-width="1.2" stroke-dasharray="10 12" opacity=".35"/>' % (f(y), z['shade'], f(y + 6)))
        for x in (36, 354, 195):
            y0v, hv = (300, h - 380) if x != 195 else (700, h - 900)
            o.append('<rect x="%s" y="%s" width="12" height="%s" fill="%s" opacity=".22"/><path d="M%s,%s V%s" stroke="#fff4d2" stroke-width="1.2" stroke-dasharray="10 12" opacity=".3"/>' % (x - 6, y0v, hv, z['shade'], x, y0v, y0v + hv))
        tints = ['#6a7fa2', '#5f8aa0', '#7a93ae', '#6d7f9a', '#8aa0b8']
        for k in range(int(h / 150)):          # بلوک‌های شهری: لکهٔ مستطیلی گرد با رنگ‌مایهٔ نزدیک
            bx = r.choice([62, 150, 250, 320]); by = r.uniform(380, h - 120)
            o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="10" fill="%s" opacity=".45" stroke="%s" stroke-width="1.2" stroke-opacity=".4"/>' % (f(bx - 38), f(by), r.randint(56, 90), r.randint(40, 70), r.choice(tints), z['shade']))
        for k in range(int(h / 420)):          # میدانک گرد با سنگ‌فرش نقطه‌ای
            cx, cy = r.choice([70, 320, 200]), r.uniform(420, h - 160)
            o.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity=".5"/>' % (f(cx), f(cy), r.randint(28, 44), z['patch']))
            for q in range(14): o.append('<circle cx="%s" cy="%s" r="1.6" fill="%s" opacity=".6"/>' % (f(cx + r.uniform(-30, 30)), f(cy + r.uniform(-24, 24)), z['shade']))
    if zone == 'space':
        for k in range(18): o.append('<circle cx="%s" cy="%s" r="%s" fill="#fff" opacity=".55"/>' % (r.randint(8, 382), ext + r.randint(8, h - ext - 8), r.choice([1, 1.3, 1.8])))
    o.append('</svg>'); return ''.join(o)
# ---------- رود: عرض متغیر ۱۸ تا ۴۶، بدون خط وسط ----------
def river_center(x): return 40 + .345 * max(0, 390 - x) + 9 * math.sin(x / 45 + .5)
def river_dy(x): return -.345 * (1 if x < 390 else 0) + 9 / 45 * math.cos(x / 45 + .5)
def river_w(x): return 18 + 28 * (max(0, 390 - x) / 390) ** 1.4
def river():
    xs = list(range(-10, 401, 10)); up, dn = [], []
    for x in xs:
        y = river_center(x); w = river_w(x) / 2; dy = river_dy(x); n = math.hypot(1, dy); nx, ny = -dy / n, 1 / n
        up.append((x + nx * w * -1, y - ny * w)); dn.append((x + nx * w, y + ny * w))
    def d(pts, close=False): return 'M' + ' L'.join('%s,%s' % (f(a), f(b)) for a, b in pts)
    body = d(up) + ' L' + ' L'.join('%s,%s' % (f(a), f(b)) for a, b in reversed(dn)) + 'Z'
    # حوض در سر چپ
    px, py = 40, river_center(40)
    pond = blob(50, 38, 12, .1, 4)
    shade = d([(a + 0, b + 6) for a, b in dn]) 
    o = [SVGH % (390, 260), '<g id="env_river_g">',
         '<path transform="translate(%s %s)" d="%s" fill="%s" stroke="%s" stroke-width="2.6" stroke-linejoin="round"/>' % (px, py, pond, WA['river'], WA['river_lip']),
         '<path d="%s" fill="%s" stroke="%s" stroke-width="2.6" stroke-linejoin="round"/>' % (body, WA['river'], WA['river_lip']),
         '<path d="%s" fill="none" stroke="%s" stroke-width="7" opacity=".55" stroke-linecap="round" transform="translate(2 1)"/>' % (d(dn[2:-2]), WA['river_lip'])]
    r = random.Random(9)
    for k in range(9):
        x = 40 + k * 38 + r.uniform(-8, 8); y = river_center(x) + r.uniform(-4, 4)
        o.append('<path d="M%s,%s q6,-3 12,0" fill="none" stroke="#fff" stroke-width="1.2" stroke-linecap="round" opacity=".85"/>' % (f(x), f(y)))
    o.append('<path d="M20,%s q8,-4 16,0 M50,%s q8,-4 16,0" fill="none" stroke="#fff" stroke-width="1.2" opacity=".8"/>' % (f(py + 6), f(py - 8)))
    o.append('</g></svg>'); return ''.join(o)
def bridge():
    o = [SVGH % (120, 70), CSS]
    o.append('<rect x="8" y="12" width="104" height="46" rx="3" fill="#a06a30" opacity=".35"/>')
    o.append('<rect x="6" y="20" width="108" height="30" rx="3" fill="#c98a45" class="eo" stroke-width="2.6"/>')
    for x in range(16, 108, 14): o.append('<path d="M%s,21V49" stroke="#a06a30" stroke-width="1.2"/>' % x)
    for y in (16, 54):
        o.append('<path d="M10,%s H110" class="eo" fill="none" stroke-width="2.6"/>' % y)
        for x in (12, 60, 108): o.append('<rect x="%s" y="%s" width="6" height="8" rx="1.5" fill="#e0b070" class="eo" stroke-width="2.6"/>' % (x - 3, y - 4))
    o.append('</svg>'); return ''.join(o)
# ---------- یخ: چندضلعی تیز، نه ابر ----------
def ice_poly():
    pts = [(10, 80), (34, 40), (84, 22), (128, 36), (176, 14), (232, 30), (276, 62), (290, 104), (254, 132), (190, 140), (130, 128), (70, 140), (24, 118)]
    return pts
def ice():
    P = ice_poly(); pts = lambda q: ' '.join('%s,%s' % (f(a), f(b)) for a, b in q)
    o = [SVGH % (300, 150), CSS, '<defs><clipPath id="env_ice_clip"><polygon points="%s"/></clipPath></defs>' % pts(P)]
    o.append('<polygon points="%s" fill="%s" transform="translate(6 7)" opacity=".5"/>' % (pts(P), '#6ab7d8'))
    o.append('<polygon points="%s" fill="%s" class="eo" stroke-width="2.6"/>' % (pts(P), IC['body']))
    # لبهٔ روشن بالا-چپ + سطوح (facet) تیز
    o.append('<g clip-path="url(#env_ice_clip)"><polygon points="0,0 300,0 232,30 176,14 128,36 84,22 34,40 10,80 0,100" fill="%s" opacity=".9"/><polygon points="40,70 120,50 150,90 80,110" fill="%s" opacity=".5"/><polygon points="190,60 250,80 220,120 170,100" fill="#fff" opacity=".35"/></g>' % (IC['rim'], IC['rim']))
    o.append('<polygon points="%s" fill="none" class="eo" stroke-width="2.6"/>' % pts(P))
    for d in ('M60,60 L100,84 L96,112', 'M150,40 L168,76 L206,86 L220,116', 'M236,70 L214,92', 'M110,84 L140,100'):
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.2" stroke-linejoin="miter"/>' % (d, IC['crack']))
    o.append('</svg>'); return ''.join(o)
def boardwalk_sample():
    d = 'M10,50 C80,10 150,90 290,40'
    return (SVGH % (300, 100)) + '<path d="%s" fill="none" stroke="#241a5e" stroke-width="34" stroke-linecap="round"/><path d="%s" fill="none" stroke="#c98a45" stroke-width="22" stroke-linecap="round"/><path d="%s" fill="none" stroke="#8f5a2e" stroke-width="22" stroke-dasharray="1.6 11"/></svg>' % (d, d, d)
# ---------- دریا و اسکله ----------
def sea_edge():
    o = [SVGH % (390, 210), CSS]
    d, _ = wavy(176, amp=0, step=390)
    o.append('<rect x="-2" y="0" width="394" height="196" fill="%s"/>' % WA['sea'])
    o.append('<rect x="-2" y="0" width="394" height="60" fill="#1b79a6" opacity=".6"/><rect x="-2" y="60" width="394" height="60" fill="#1b79a6" opacity=".3"/>')
    r = random.Random(3)
    for k in range(14):
        x, y = r.randint(10, 360), r.randint(10, 150); o.append('<path d="M%s,%s q8,-5 16,0 q8,5 16,0" fill="none" stroke="#fff" stroke-width="1.2" stroke-linecap="round" opacity=".55"/>' % (x, y))
    # اسکلهٔ بتنی
    o.append('<rect x="-4" y="176" width="398" height="30" fill="#c6c1b6" class="eo" stroke-width="2.6"/><rect x="-4" y="176" width="398" height="14" fill="#e9e4d6" class="eo" stroke-width="2.6"/>')
    for x in range(30, 390, 70): o.append('<rect x="%s" y="166" width="12" height="14" rx="3" fill="#3a2a7a" class="eo" stroke-width="2.6"/>' % x)
    for x in range(10, 390, 46): o.append('<path d="M%s,196 v8" stroke="#9b968c" stroke-width="1.2"/>' % x)
    o.append('</svg>'); return ''.join(o)
def bay_left(h=1340):
    # خلیج باریک سمت چپ، متصل به دریای بالا؛ لب راست = دیوار اسکله
    o = [SVGH % (110, h), CSS]
    pts = []; r = random.Random(2); y = 0
    while y <= h:
        k = min(1, max(0, (h - y) / 200)) ** .6; pts.append((52 * k + r.uniform(-3, 3) * k, y)); y += 40
    edge = ' L'.join('%s,%s' % (f(a), f(b)) for a, b in pts)
    o.append('<path d="M0,0 L%s L0,%s Z" fill="%s"/>' % (edge, h, WA['sea']))
    o.append('<path d="M0,0 L%s L0,%s Z" fill="#1b79a6" opacity=".35" transform="translate(-20 0)"/>' % (' L'.join('%s,%s' % (f(a), f(b)) for a, b in pts), h))
    o.append('<path d="M%s" fill="none" stroke="#c6c1b6" stroke-width="14"/><path d="M%s" fill="none" class="eo" stroke-width="2.6" transform="translate(7 0)"/><path d="M%s" fill="none" class="eo" stroke-width="2.6" transform="translate(-7 0)"/>' % (edge, edge, edge))
    for k in range(10):
        o.append('<path d="M%s,%s q6,-4 12,0" fill="none" stroke="#fff" stroke-width="1.2" stroke-linecap="round" opacity=".6"/>' % (r.randint(6, 36), r.randint(60, h - 30)))
    for y in range(120, h, 220): o.append('<rect x="56" y="%s" width="12" height="14" rx="3" fill="#3a2a7a" class="eo" stroke-width="2.6"/>' % y)
    o.append('</svg>'); return ''.join(o)
def skyline():
    o = [SVGH % (390, 180), CSS]; r = random.Random(11)
    cols = ['#6c82a0', '#7a93ae', '#5f7694', '#8aa0b8', '#6a7fa2']
    x = -6; kinds = ['flat', 'slant', 'step', 'dome', 'tank', 'spire', 'flat']
    for i in range(7):
        w = r.randint(44, 66); hgt = r.randint(64, 140); c = cols[i % 5]; k = kinds[i]; top = 176 - hgt
        body = {'flat': 'M%s,176 V%s H%s V176Z', 'slant': 'M%s,176 V%s L%s,%s V176Z'}
        if k == 'slant': o.append('<path d="M%s,176 V%s L%s,%s V176Z" fill="%s" class="eo" stroke-width="2.6"/>' % (x, top + 18, x + w, top, c))
        elif k == 'step': o.append('<path d="M%s,176 V%s H%s V%s H%s V176Z" fill="%s" class="eo" stroke-width="2.6"/>' % (x, top + 24, x + w * .45, top, x + w, c))
        elif k == 'dome':
            o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" class="eo" stroke-width="2.6"/><path d="M%s,%s a%s,%s 0 0 1 %s,0z" fill="#a8bdd2" class="eo" stroke-width="2.6"/>' % (x, top, w, hgt, c, x + 4, top, w / 2 - 4, 18, w - 8))
        elif k == 'tank':
            o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" class="eo" stroke-width="2.6"/><rect x="%s" y="%s" width="20" height="16" rx="4" fill="#a8bdd2" class="eo" stroke-width="2.6"/><path d="M%s,%s v10 M%s,%s v10" class="eo" stroke-width="1.2"/>' % (x, top, w, hgt, c, x + w / 2 - 10, top - 18, x + w / 2 - 6, top, x + w / 2 + 6, top))
        elif k == 'spire':
            o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" class="eo" stroke-width="2.6"/><path d="M%s,%s L%s,%s L%s,%s z" fill="#a8bdd2" class="eo" stroke-width="2.6"/>' % (x, top, w, hgt, c, x + 4, top, x + w / 2, top - 30, x + w - 4, top))
        else: o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" class="eo" stroke-width="2.6"/>' % (x, top, w, hgt, c))
        for yy in range(top + 24, 160, 18):
            for xx in range(x + 8, x + w - 10, 14): o.append('<rect x="%s" y="%s" width="6" height="8" fill="#a8bdd2" opacity=".7"/>' % (xx, yy))
        x += w + r.randint(4, 12)
    o.append('<rect x="-4" y="170" width="398" height="14" fill="#44566c"/></svg>'); return ''.join(o)
def cloud_edge():
    o = [SVGH % (390, 120), '<defs><linearGradient id="env_cl_g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".9"/></linearGradient></defs>']
    r = random.Random(5)
    for x in range(-20, 400, 56):
        y = 92 + r.randint(-10, 8); rr = r.randint(22, 34)
        o.append('<g fill="#fff"><circle cx="%s" cy="%s" r="%s"/><circle cx="%s" cy="%s" r="%s"/><circle cx="%s" cy="%s" r="%s"/></g>' % (x, y, rr, x + 24, y + 6, rr - 6, x - 22, y + 8, rr - 8))
    o.append('</svg>'); return ''.join(o)
# ---------- درخت‌ها ----------
def tree_syms():
    pine = B('env_tree_pine'); pine.rect(-4, -10, 8, 12, '#a06a30', 2.6, 1)
    for i, (w, y) in enumerate(((26, -8), (20, -30), (14, -50))): pine.poly([(-w, y), (w, y), (0, y - 34)], ['#5f9e3a', '#6fb040', '#7fbf4a'][i], 2.6)
    pop = B('env_tree_pop'); pop.rect(-3, -10, 6, 12, '#a06a30', 2.6, 1); pop.path('M0,-12 C-14,-20 -16,-60 0,-86 C16,-60 14,-20 0,-12Z', '#66993b', 2.6); pop.line(0, -20, 0, -74, '#a6d86a', 1.2)
    bush = B('env_tree_bush'); bush.path('M-22,0 Q-30,-14 -16,-20 Q-14,-34 2,-30 Q18,-38 22,-20 Q34,-14 24,0Z', '#7fbf4a', 2.6); bush.line(-10, -12, -4, -22, '#a6d86a', 1.2); bush.line(8, -10, 14, -18, '#a6d86a', 1.2)
    return {'tree_pine': pine.svg((80, 100), 40, 90, 22, 8, (-26, -92, 26, 4), False), 'tree_pop': pop.svg((60, 100), 30, 90, 16, 6, (-16, -90, 16, 4), False), 'tree_bush': bush.svg((70, 60), 35, 52, 24, 7, (-26, -40, 26, 4), False)}
