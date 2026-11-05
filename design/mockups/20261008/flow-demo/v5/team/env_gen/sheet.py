#!/usr/bin/env python3
"""env_sheet.html: نقشهٔ کامل ۳۴ گره (۳۳ دیدنی)، با sprite واقعی؛ پس از gen_env.py اجرا شود."""
import math, random, json, re
import layout as L, terrain as T, decor as DC
OUT = L.OUT; H = L.H
sprite = (OUT / 'sprite_env.svg').read_text(encoding='utf-8')
tokens = (L.HERE.parent / 'assets' / 'light' / 'tokens.css').read_text(encoding='utf-8')
pts = L.path_pts(); D_ALL = L.path_d(pts); S = L.path_samples(pts)
HERE_P = 20                      # M05
LOCK = {'E06', 'E04'}
idx = {n['id']: i for i, n in enumerate(L.NODES)}
def dmin(x, y): return min(math.hypot(x - a, y - b) for a, b in S)
def use(sid, x, y, w, h, extra=''): return '<use href="#%s" x="%s" y="%s" width="%s" height="%s" %s/>' % (sid, f1(x), f1(y), w, h, extra)
def f1(v): return ('%.1f' % v).rstrip('0').rstrip('.')
o = ['<g id="env_zones">']
for z in ('city', 'farm', 'space', 'sports'):
    ys = (L.ZB[z][0] - (90 if z != 'city' else 0)); h = L.ZB[z][1] - ys
    o.append(use('zb_strip_' + z, 0, ys, 390, h))
o.append('</g>')
# دریا و خلیج و افق شهر
o.append(use('env_sea_edge', 0, 0, 390, 210) + use('env_bay_left', 0, 170, 110, 1340) + use('env_skyline', 0, 168, 390, 180))
# رود
RY0 = L.NODES[idx['E07']]['cy'] - 157; o.append(use('env_river', 0, RY0, 390, 260))
# یخ
ICEX, ICEY = 10, L.NODES[idx['F06']]['cy'] - 150; o.append(use('env_ice', ICEX, ICEY, 300, 150))
# پل: محل تقاطع مسیر و رود
best = None
for i in range(len(S) - 1):
    x, y = S[i]
    if RY0 + 10 < y < RY0 + 230:
        cy = RY0 + T.river_center(x)
        if best is None or abs(y - cy) < best[0]: best = (abs(y - cy), i)
bi = best[1]; bx, by = S[bi]; ang = math.degrees(math.atan2(S[bi + 1][1] - S[bi - 1][1], S[bi + 1][0] - S[bi - 1][0]))
# تزئین
random.seed(21); placed = []
def free(x, y, r=0):
    if dmin(x, y) < 66 + r: return False
    for n in L.NODES:
        if math.hypot(x - n['cx'], y - n['cy'] + 30) < n['rx'] + 58 + r: return False
    if any(math.hypot(x - a, y - b) < 92 for a, b, _ in placed): return False
    if abs(y - (RY0 + T.river_center(x))) < 60 and RY0 - 20 < y < RY0 + 260: return False
    if ICEY - 20 < y < ICEY + 170 and x < 330: return False
    if 160 < y < 1520 and x < 100: return False
    if y < 350: return False
    return True
cnt = {'sports': 13, 'space': 10, 'farm': 7, 'city': 16}
decos = []
for z, k in cnt.items():
    names = [n for n, _, _ in DC.SET[z]]; random.shuffle(names); y0, y1 = L.ZB[z]; made = 0; tries = 0
    while made < k and tries < 4000:
        tries += 1; x = random.randint(26, 364); y = random.randint(y0 + 60, y1 - 40)
        if z == 'sports' and y > L.H - 400: continue
        if free(x, y): placed.append((x, y, z)); decos.append((y, 'env_dec_%s_%s' % (z, names[made % len(names)]), x, y)); made += 1
# درخت‌ها: ۲ خوشهٔ ۳تایی (۶ کل)
trees = []
for z, k in (('sports', 1), ('farm', 1), ('city', 1)):
    if len(trees) >= 6: break
    y0, y1 = L.ZB[z]; tries = 0; got = 0
    while got < k and tries < 3000:
        tries += 1; x = random.randint(30, 360); y = random.randint(y0 + 80, y1 - 140)
        if free(x, y, 20): placed.append((x, y, z)); got += 1; trees += [(y, 'env_tree_pine', x - 26, y), (y + 6, 'env_tree_pop', x + 4, y + 6), (y + 12, 'env_tree_bush', x + 28, y + 14)]
dsz = {'env_tree_pine': (80, 100, -40, -90), 'env_tree_pop': (60, 100, -30, -90), 'env_tree_bush': (70, 60, -35, -52)}
o.append('<g id="env_decor">')
for y, sid, x, yy in sorted(decos + trees):
    if sid in dsz: w, h, dx, dy = dsz[sid]
    else: w, h, dx, dy = 120, 120, -60, -100
    o.append(use(sid, x + dx, yy + dy, w, h))
o.append('</g>')
# مسیر دو‌لایه
o.append('<g id="env_path"><path d="%s" fill="none" stroke="#241a5e" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"/>' % D_ALL)
o.append('<path d="%s" fill="none" stroke="#fff4d2" stroke-width="22" stroke-linecap="round" opacity=".55"/><path d="%s" fill="none" stroke="#fff4d2" stroke-width="5" stroke-dasharray="3 14" stroke-linecap="round"/>' % (D_ALL, D_ALL))
Dd = L.path_seg_d(pts, 0, HERE_P + 1)
o.append('<path d="%s" fill="none" stroke="#fff4d2" stroke-width="22" stroke-linecap="round"/><path d="%s" fill="none" stroke="#ffd23f" stroke-width="3.2" stroke-dasharray="10 12"/></g>' % (Dd, Dd))
fy0, fy1 = L.ZB['farm'][0] - 20, L.ZB['farm'][1] + 20
o.append('<clipPath id="env_farmclip"><rect x="0" y="%d" width="390" height="%d"/></clipPath><g clip-path="url(#env_farmclip)"><path d="%s" fill="none" stroke="#241a5e" stroke-width="38" stroke-linecap="round"/><path d="%s" fill="none" stroke="#fff4d2" stroke-width="22" stroke-linecap="round"/><path d="%s" fill="none" stroke="#6b4a22" stroke-width="3.2" stroke-dasharray="10 12"/></g>' % (fy0, fy1 - fy0, D_ALL, D_ALL, D_ALL))
# پلهٔ چوبی روی یخ (فقط درون چندضلعی یخ)
ip = ' '.join('%s,%s' % (a + ICEX, b + ICEY) for a, b in T.ice_poly())
o.append('<clipPath id="env_icemap"><polygon points="%s"/></clipPath><g clip-path="url(#env_icemap)"><path d="%s" fill="none" stroke="#241a5e" stroke-width="34" stroke-linecap="round"/><path d="%s" fill="none" stroke="#c98a45" stroke-width="22" stroke-linecap="round"/><path d="%s" fill="none" stroke="#8f5a2e" stroke-width="22" stroke-dasharray="1.6 11"/></g>' % (ip, D_ALL, D_ALL, D_ALL))
o.append('<g transform="translate(%s %s) rotate(%s)">%s</g>' % (f1(bx), f1(by), f1(ang), use('env_bridge', -60, -35, 120, 70)))
sx, sy = L.START
o.append(use('env_start_gate', sx - 85, sy - 120 + 6, 170, 130))
# گره‌ها (از بالا به پایین؛ جلوتر روی بالاتر)
slots = L.slots()
for n in sorted(L.NODES, key=lambda n: n['cy']):
    s = slots[n['id']]; px, py = s['place_at']
    pad = 'env_pad_%s_%s' % (n['zone'], 'abc'[n['p'] % 3])
    if n['kind'] == 'landmark': o.append(use(n['asset'], px, py, 200, 190))
    else: o.append(use(pad, px, py, 120, 100) + use(n['asset'], px, py, 120, 100))
    i = idx[n['id']]; lx, ly = s['lock_done_center']
    if n['id'] == 'M12': continue
    if i < HERE_P: o.append('<g transform="translate(%s %s)"><circle r="14" fill="#fff4d2" stroke="#241a5e" stroke-width="2.6"/><path d="M-6,0 l4,5 l8,-10" fill="none" stroke="#3a2a7a" stroke-width="3" stroke-linecap="round"/></g>' % (lx, ly))
    if n['id'] in LOCK: o.append('<g transform="translate(%s %s)"><circle r="16" fill="#3a2a7a" stroke="#241a5e" stroke-width="2.6"/><rect x="-7" y="-2" width="14" height="10" rx="2" fill="#fff4d2"/><path d="M-4,-2 v-4 a4,4 0 0 1 8,0 v4" fill="none" stroke="#fff4d2" stroke-width="2.6"/></g>' % (lx, ly))
# اینجایی: حلقه + جاگذار b1
h = L.NODES[HERE_P]; hx, hy = h['cx'], h['cy']
o.append('<g><ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="#241a5e" stroke-width="17"/><ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="#ffd23f" stroke-width="8"/></g>' % (hx, hy + 6, h['rx'] + 22, h['ry'] + 14, hx, hy + 6, h['rx'] + 22, h['ry'] + 14))
fx, fy = slots[h['id']]['b1_foot']
o.append('<g transform="translate(%s %s)"><ellipse cx="0" cy="0" rx="20" ry="6" fill="#10083a" opacity=".3"/><rect x="-14" y="-34" width="28" height="30" rx="10" fill="#2fb8a8" stroke="#241a5e" stroke-width="4.5"/><circle cx="0" cy="-46" r="18" fill="#e8b48a" stroke="#241a5e" stroke-width="4.5"/><path d="M-18,-48 a18,16 0 0 1 36,0z" fill="#fff4d2" stroke="#241a5e" stroke-width="4.5" stroke-linejoin="round"/></g>' % (fx, fy))
o.append('<g opacity=".85"><g transform="translate(0 70) scale(1 -1)">%s</g><g transform="translate(0 %d)">%s</g></g>' % (use('env_cloud_edge', 0, 0, 390, 70), H - 70, use('env_cloud_edge', 0, 0, 390, 70)))
page = ('<!doctype html><html lang="fa" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>env_sheet</title><style>%s'
        'html,body{margin:0;background:#1b79a6}#sc{width:100vw;height:100vh;overflow-y:auto;overflow-x:hidden;scrollbar-width:none}#sc::-webkit-scrollbar{display:none}svg.map{display:block;width:100%%;height:auto}body.gray #sc{filter:grayscale(1)}</style></head><body data-light="day">'
        '<div style="position:absolute;width:0;height:0;overflow:hidden">%s</div><div id="sc"><svg class="map" xmlns="http://www.w3.org/2000/svg" width="390" height="%d" viewBox="0 0 390 %d">%s</svg></div>'
        '<script>const q=new URLSearchParams(location.search);document.getElementById("sc").scrollTop=+(q.get("y")||0);if(q.has("gray"))document.body.classList.add("gray");if(q.get("light"))document.body.setAttribute("data-light",q.get("light"))</script></body></html>') % (tokens, sprite, H, H, ''.join(o))
(OUT / 'env_sheet.html').write_text(page, encoding='utf-8'); print(len(page), 'bridge', bx, by, ang, 'decor', len(decos), len(trees))
