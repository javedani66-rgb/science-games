#!/usr/bin/env python3
"""env_sheet.html (r2): نقشهٔ کامل ۳۴ گره با ظاهر v4 (مسیر کرم-بنفش، wob، عنوان بزرگ زمین، حلقهٔ زرد). پس از gen_env.py اجرا شود.
فقط برای بازبینی است؛ متن‌ها از strings.fa.json (+ نام گره‌ها از node_map)."""
import math, random, json, re
import layout as L, terrain as T, decor as DC
OUT = L.OUT; H = L.H
sprite = (OUT / 'sprite_env.svg').read_text(encoding='utf-8')
tokens = (L.HERE.parent / 'assets' / 'light' / 'tokens.css').read_text(encoding='utf-8')
STR = json.load(open(OUT / 'strings.fa.json', encoding='utf-8'))
NM = {n['id']: n for n in json.load(open(OUT / 'node_map.json', encoding='utf-8'))['nodes']}
S = L.path_samples(); NPI = L.NODE_PI
HERE_P = 20
LOCK = {'E06', 'E04'}
idx = {n['id']: i for i, n in enumerate(L.NODES)}
OUTC = '#241a5e'; CREAM = '#fff3c4'
def dmin(x, y): return min(math.hypot(x - a, y - b) for a, b in S)
def f1(v): return ('%.1f' % v).rstrip('0').rstrip('.')
def use(sid, x, y, w, h, extra=''): return '<use href="#%s" x="%s" y="%s" width="%s" height="%s" %s/>' % (sid, f1(x), f1(y), w, h, extra)
WOB = 'filter="url(#env_wob)"'
o = ['<g id="env_zones">']
for z in ('city', 'farm', 'space', 'sports'):
    ys = (L.ZB[z][0] - (90 if z != 'city' else 0)); h = L.ZB[z][1] - ys
    o.append(use('zb_strip_' + z, 0, ys, 390, h))
o.append('</g>')
# رود
RY0 = L.NODES[idx['E07']]['cy'] - 157; o.append('<g %s>%s</g>' % (WOB, use('env_river', 0, RY0, 390, 260)))
# یخ دور پیست (F06)
ICEX, ICEY = 12, L.NODES[idx['F06']]['cy'] - 118; o.append('<g %s>%s</g>' % (WOB, use('env_ice', ICEX, ICEY, 300, 156)))
# پل: جای تقاطع مسیر و رود
best = None
for i in range(len(S) - 1):
    x, y = S[i]
    if RY0 + 10 < y < RY0 + 230 and 30 < x < 360:
        cy = RY0 + T.river_center(x)
        if best is None or abs(y - cy) < best[0]: best = (abs(y - cy), i)
bi = best[1]; bx, by = S[bi]; ang = math.degrees(math.atan2(S[bi + 1][1] - S[bi - 1][1], S[bi + 1][0] - S[bi - 1][0]))
TUN = json.load(open(OUT / 'node_map.json', encoding='utf-8'))['tunnel']
# ---------- جای‌گذاری آزاد ----------
random.seed(21); placed = []
slots = L.slots()
def node_blocked(x, y, r, lab=62):
    for n in L.NODES:
        if n['id'] == 'M12': continue
        if abs(x - n['cx']) < n['rx'] + r and n['cy'] - n['h'] - r < y < n['cy'] + n['ry'] + lab + r: return True
    return False
def free(x, y, r=0, pd=44, top=0):
    if dmin(x, y) < pd + r: return False
    if top and dmin(x, y - top) < 30: return False
    if math.hypot(x - L.START[0], y - L.START[1] + 40) < 130: return False
    if node_blocked(x, y, 12 + r): return False
    if any(math.hypot(x - a, y - b) < 58 + r for a, b, _ in placed): return False
    if abs(y - (RY0 + T.river_center(x))) < 52 and RY0 - 20 < y < RY0 + 260: return False
    if ICEY - 22 < y < ICEY + 176 and x < 330: return False
    if TUN['y'] - 20 < y < TUN['y'] + TUN['h'] + 40: return False
    if y < 80 or y > H - 120: return False
    return True
# ---------- عنوان‌های بزرگ زمین (v4: لالهزار 34، سفید، خط 9) ----------
def title_spot(z, target, size):
    t = STR['env.zone_title.%s' % z]['text']; w = .44 * size * len(t) + 24; best = None
    y0, y1 = L.ZB[z]; up = size * .8; dn = size * .3
    for y in range(int(y0 + 40), int(y1 - 30), 6):
        for x0 in range(12, int(390 - w - 8), 14):
            ok = True
            for xx in range(x0, int(x0 + w) + 1, 16):
                for yy in (y - up, y - up / 2, y + dn):
                    if dmin(xx, yy) < 30 or node_blocked(xx, yy, 0, 50): ok = False; break
                if not ok: break
            if not ok: continue
            if z == 'city' and T.COAST_Y - 60 < y < T.COAST_Y + 40: continue
            hn = L.NODES[HERE_P]
            if abs(x0 + w / 2 - hn['cx']) < 150 and hn['cy'] - hn['h'] - 130 < y < hn['cy'] + 60: continue
            if z == 'farm' and RY0 - 30 < y < RY0 + 240: continue
            if z == 'space' and TUN['y'] - 10 < y < TUN['y'] + TUN['h'] + 20: continue
            if z == 'sports' and ICEY - 20 < y < ICEY + 170 and x0 < 330: continue
            d = abs(y - target) + abs(x0 + w / 2 - 195) * .05
            if best is None or d < best[0]: best = (d, x0 + w / 2, y)
    return best
ZT = []
for z, tgt in (('sports', L.ZB['sports'][0] + 520), ('space', L.ZB['space'][0] + 380), ('farm', L.ZB['farm'][0] + 250), ('city', 2350)):
    r = None
    for size in (34, 30, 27):
        r = title_spot(z, tgt, size)
        if r: ZT.append((z, r[1], r[2], size)); break
for z, x, y, size in ZT:
    t = STR['env.zone_title.%s' % z]['text']; ww = .44 * size * len(t)
    for xx in range(int(x - ww / 2), int(x + ww / 2) + 1, 30): placed.append((xx, y - 10, 'title'))
cnt = [('sports', 'land', 14), ('space', 'land', 11), ('farm', 'land', 8), ('city', 'yard', 12), ('city', 'sea', 9)]
decos = []
LAND_CITY = [n for n, _, _ in DC.SET['city']]
for z, kind, k in cnt:
    if kind == 'sea': names = ['buoy', 'sail', 'islet', 'crate', 'lighthouse', 'buoy', 'sail', 'islet']; y0, y1 = 60, T.COAST_Y - 60
    elif kind == 'yard': names = LAND_CITY; y0, y1 = T.COAST_Y + 60, L.ZB['city'][1] - 20
    else: names = [n for n, _, _ in DC.SET[z]]; y0, y1 = L.ZB[z]; y0 += 60; y1 -= 40
    if kind != 'sea': random.shuffle(names)
    made = 0; tries = 0
    while made < k and tries < 6000:
        tries += 1; x = random.randint(26, 364); y = random.randint(int(y0), int(y1))
        if z == 'sports' and y > L.H - 330: continue
        if free(x, y): placed.append((x, y, z)); decos.append((y, 'env_dec_%s_%s' % (z, names[made % len(names)]), x, y)); made += 1
# درخت‌ها: گونه‌های متفاوت، پراکنده (نه تکراری)
TS = T.TREE_SZ
TREE_PICK = {'sports': (['tree_pine', 'tree_round', 'tree_pop', 'tree_oak', 'tree_birch', 'tree_bush'], 10), 'farm': (['tree_autumn', 'tree_oak', 'tree_round', 'tree_birch', 'tree_bush'], 7), 'yard': (['tree_palm', 'tree_bush', 'tree_round', 'tree_pop'], 6)}
trees = []
for zk, (kinds, k) in TREE_PICK.items():
    if zk == 'yard': y0, y1 = T.COAST_Y + 60, L.ZB['city'][1] - 20
    else: y0, y1 = L.ZB[zk]; y0 += 60; y1 -= 40
    made = 0; tries = 0; last = None
    while made < k and tries < 6000:
        tries += 1; x = random.randint(24, 366); y = random.randint(int(y0), int(y1))
        if zk == 'sports' and y > L.H - 330: continue
        if free(x, y, 4, 34, top=70):
            choices = [t for t in kinds if t != last]; t = random.choice(choices); last = t
            sc = random.choice([.9, 1.0, 1.15]); placed.append((x, y, zk)); trees.append((y, t, x, y, sc)); made += 1
o.append('<g id="env_decor">')
dsz = TS
for y, sid, x, yy in sorted(decos):
    o.append(use(sid, x - 60, yy - 100, 120, 120))
for y, t, x, yy, sc in sorted(trees):
    w, h, ox, oy = TS[t]; o.append(use('env_' + t, x - ox * sc, yy - oy * sc, w * sc, h * sc))
o.append('</g>')
# ---------- مسیر v4 ----------
Dall = L.path_d(); ip = NPI[HERE_P]
Ddone = L.path_seg_d(None, 0, ip); Drest = L.path_seg_d(None, ip, len(L.SEGS))
o.append('<g id="env_path" %s>' % WOB)
o.append('<path d="%s" fill="none" stroke="%s" stroke-width="33" stroke-linecap="round" stroke-linejoin="round"/>' % (Dall, OUTC))
o.append('<path d="%s" fill="none" stroke="%s" stroke-width="22" stroke-linecap="round" opacity=".34"/><path d="%s" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round" stroke-dasharray="3 14" opacity=".95"/>' % (Drest, CREAM, Drest, CREAM))
o.append('<path d="%s" fill="none" stroke="%s" stroke-width="22" stroke-linecap="round"/><path d="%s" fill="none" stroke="#f0b429" stroke-width="3.2" stroke-dasharray="10 12"/></g>' % (Ddone, CREAM, Ddone))
o.append('<g transform="translate(%s %s) rotate(%s)" %s>%s</g>' % (f1(bx), f1(by), f1(ang), WOB, use('env_bridge', -60, -35, 120, 70)))
# تونل (رشته‌کوه) روی مسیر، زیر گره‌ها
o.append('<g %s>%s</g>' % (WOB, use('env_tunnel', TUN['x'], TUN['y'], TUN['w'], TUN['h'])))
sx, sy = L.START
o.append('<g %s>%s</g>' % (WOB, use('env_start_gate', sx - 85, sy - 120 + 6, 170, 130)))
o.append('<text x="%s" y="%s" text-anchor="middle" font-family="Lalezar" font-size="24" fill="%s">%s</text>' % (f1(sx), f1(sy - 81), OUTC, STR['env.start.label']['text']))
# ---------- گره‌ها ----------
SH_OK = {'sports': ['disc', 'plate', 'hex', 'mound', 'rock', 'tier', 'deck', 'pond'], 'space': ['disc', 'plate', 'hex', 'rock', 'tier', 'deck'], 'farm': ['disc', 'plate', 'hex', 'mound', 'rock', 'deck', 'tier', 'pond'],
         'sea': ['deck', 'plate', 'rock', 'hex', 'tier', 'disc'], 'yard': ['plate', 'hex', 'deck', 'disc', 'tier', 'rock']}
used = {}; LBL = []
def label(x, y, t):
    return '<text x="%s" y="%s" text-anchor="middle" font-family="Lalezar" font-size="20" fill="%s" stroke="%s" stroke-width="6" paint-order="stroke" stroke-linejoin="round">%s</text>' % (f1(x), f1(y), CREAM, OUTC, t)
for n in sorted(L.NODES, key=lambda n: n['cy']):
    if n['id'] == 'M12': continue
    s = slots[n['id']]; px, py = s['place_at']; i = idx[n['id']]
    g = '<g class="node" data-id="%s" %s>' % (n['id'], WOB)
    if n['kind'] == 'landmark': g += use(n['asset'], px, py, 200, 190)
    else:
        key = 'sea' if (n['zone'] == 'city' and n['cy'] < T.COAST_Y) else 'yard' if n['zone'] == 'city' else n['zone']; lst = SH_OK[key]
        shp = lst[(i * 3 + (1 if i % 2 else 0)) % len(lst)]
        g += use('env_pad_%s_%s' % (n['zone'], shp), px, py, 120, 100) + use(n['asset'], px, py, 120, 100)
    g += '</g>'; o.append(g)
    lx, ly = s['lock_done_center']
    if i < HERE_P: o.append('<g transform="translate(%s %s)"><circle r="10" fill="%s" stroke="%s" stroke-width="3"/><polyline points="-5,0 -1.5,4 5.5,-4" fill="none" stroke="%s" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></g>' % (f1(lx), f1(ly), CREAM, OUTC, OUTC))
    if n['id'] in LOCK: o.append('<g transform="translate(%s %s)"><circle r="10" fill="%s" stroke="%s" stroke-width="3"/><path d="M-3.6,-1 v-2.4 a3.6,3.6 0 0 1 7.2,0 v2.4" fill="none" stroke="%s" stroke-width="2.4"/><rect x="-5.6" y="-1" width="11.2" height="8" rx="2" fill="%s"/></g>' % (f1(lx), f1(ly), CREAM, OUTC, OUTC, OUTC))
    if i != HERE_P:
        cx, cy = n['cx'], n['cy']; LBL.append(label(cx, cy + n['ry'] + 12 + 26 + (0 if n['kind'] == 'landmark' else 2), NM[n['id']]['env_title'] or '.'))
o.append('<g id="env_labels">%s</g>' % ''.join(LBL))
# ---------- عنوان‌ها
TOUT = []
for z, x, y, size in ZT:
    t = STR['env.zone_title.%s' % z]['text']
    TOUT.append('<text x="%s" y="%s" text-anchor="middle" font-family="Lalezar" font-size="%d" fill="#fff" stroke="%s" stroke-width="9" paint-order="stroke" stroke-linejoin="round" transform="rotate(-3 %s %s)">%s</text>' % (f1(x), f1(y), size, OUTC, f1(x), f1(y), t))
o.append('<g id="env_zone_titles">%s</g>' % ''.join(TOUT))
# ---------- اینجایی: حلقه + b1 (همان v4، دست نخورده) ----------
h = L.NODES[HERE_P]; hx, hy = h['cx'], h['cy']; hr = h['rx'] + 22; hry = h['ry'] + 14
o.append('<g class="hero"><ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width="10"/><ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="#ffd23f" stroke-width="5.5" stroke-dasharray="16 10"/>' % (hx, hy + 6, hr, hry, OUTC, hx, hy + 6, hr, hry))
fx, fy = slots[h['id']]['b1_foot']
o.append('<ellipse cx="%s" cy="%s" rx="26" ry="7" fill="#10083a" opacity=".35"/><image href="../../../../v4/style/b1.png" x="%s" y="%s" width="82" height="82"/>' % (fx, fy + 6, fx - 41, fy - 62))
here_t = STR['env.here.label']['text']
bx_, by_ = hx, hy - h['h'] - 54
o.append('<path d="M%s,%s h80 a12,12 0 0 1 12,12 v26 a12,12 0 0 1 -12,12 h-18 l-22,14 l-22,-14 h-18 a12,12 0 0 1 -12,-12 v-26 a12,12 0 0 1 12,-12z" fill="#ffd23f" stroke="%s" stroke-width="4" stroke-linejoin="round" transform="translate(%s %s)"/>' % (-40, 0, OUTC, bx_, by_))
o.append('<text x="%s" y="%s" text-anchor="middle" font-family="Lalezar" font-size="23" fill="%s">%s</text></g>' % (bx_, by_ + 31, OUTC, here_t))
# ---------- ابرهای گرد (روی همه، کم و خالی از مسیر) ----------
cl = []; random.seed(3)
cand = [(332, 120), (50, 330), (330, 760), (60, 1050), (320, 1500), (50, 2000), (330, 2480), (60, 2900), (320, 3300), (50, 3640), (320, 4180), (60, 4600), (330, 5000), (70, 5480)]
for k, (x, y) in enumerate(cand):
    if dmin(x, y) > 46 and not node_blocked(x, y, 24) and math.hypot(x - L.START[0], y - L.START[1]) > 150: cl.append(use('env_cloud_' + 'abc'[k % 3], x - 55 * 1.05, y - 28 * 1.05, 110 * 1.05, 56 * 1.05, 'opacity=".96"'))
o.append('<g id="env_clouds">%s</g>' % ''.join(cl))
# نوار تیره بالا/پایین (v4 vig)
FONT = '/home/claude/science-games/assets/fonts/'
fonts = "@font-face{font-family:Lalezar;src:url('file://%sLalezar-Regular.woff2')}" % FONT
page = ('<!doctype html><html lang="fa" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>env_sheet r2</title><style>%s%s'
        'html,body{margin:0;background:#10083a}#sc{width:100vw;height:100vh;overflow-y:auto;overflow-x:hidden;scrollbar-width:none}#sc::-webkit-scrollbar{display:none}svg.map{display:block;width:100%%;height:auto}body.gray #sc{filter:grayscale(1)}</style></head><body data-light="day">'
        '<div style="position:absolute;width:0;height:0;overflow:hidden">%s</div><div id="sc"><svg class="map" xmlns="http://www.w3.org/2000/svg" width="390" height="%d" viewBox="0 0 390 %d">%s</svg></div>'
        '<script>const q=new URLSearchParams(location.search);document.getElementById("sc").scrollTop=+(q.get("y")||0);if(q.has("gray"))document.body.classList.add("gray");if(q.get("light"))document.body.setAttribute("data-light",q.get("light"))</script></body></html>') % (fonts, tokens, sprite, H, H, ''.join(o))
(OUT / 'env_sheet.html').write_text(page, encoding='utf-8'); print(len(page), 'bridge', bx, by, ang, 'decor', len(decos), 'trees', len(trees), 'titles', ZT)
# عنوان‌های زمین → slots.json
sj = json.load(open(OUT / 'slots.json', encoding='utf-8')); sj['zone_titles'] = {z: dict(string_key='env.zone_title.%s' % z, x=round(x), y=round(y), font='Lalezar', size=size, rotate=-3, fill='#ffffff', stroke='#241a5e', stroke_w=9) for z, x, y, size in ZT}
sj['here_label_key'] = 'env.here.label'; json.dump(sj, open(OUT / 'slots.json', 'w'), ensure_ascii=False, indent=1)
