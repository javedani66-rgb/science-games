#!/usr/bin/env python3
"""سازندهٔ دارایی‌های env (r2: بازگشت به ظاهر v4). اجرا: python3 gen_env.py  → v5/team/assets_r2/env/*
سپس sheet.py (env_sheet.html) و shots.py / cmp.py."""
import math, random, re, json, pathlib
import layout as L
from shapes import *
import buildings as X, terrain as T, decor as DC
OUT = L.OUT; OUT.mkdir(parents=True, exist_ok=True)
for old in OUT.glob('*.svg'): old.unlink()
files = {}
def put(name, svg): files[name] = svg; (OUT / name).write_text(svg, encoding='utf-8')
SYM = {}
def symbol(sid, svg, drop_style=True):
    m = re.match(r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*)</svg>$', svg, re.S); vb, inner = m.group(1), m.group(2)
    if drop_style: inner = re.sub(r'<style>.*?</style>', '', inner, flags=re.S)
    SYM[sid] = '<symbol id="%s" viewBox="%s">%s</symbol>' % (sid, vb, inner)
# --- ۱۲ بنا ---
for n, fn in X.LAND.items():
    s = fn(); put('node_%02d.svg' % n, s); symbol('node_%02d' % n, s)
# --- پایه‌ها: ۴ زمین × ۸ شکل (هر گره پایهٔ متفاوت می‌گیرد؛ ایراد ۱ v4) ---
for z in ('sports', 'space', 'farm', 'city'):
    for v, shp in enumerate(SHAPES):
        rx = (38, 42, 40, 44, 42, 40, 40, 38)[v]; pre = 'env_pad_%s_%s' % (z, shp)
        b = B(pre); pad(b, z, rx, v + 1, shape=shp); s = b.svg((120, 100), 60, 78, rx, 12, (-rx, -14, rx, 14)); symbol(pre, s)
for n, fn in X.PROPS.items():
    s = X.prop(n, fn); put('prop_%02d.svg' % n, s); symbol('prop_%02d' % n, s)
# --- زمین ---
ZB = L.ZB; order = ['city', 'farm', 'space', 'sports']; STRIP_Y = {}
for z in order:
    y0, y1 = ZB[z]; soft = z != 'city'; ys = y0 - (90 if soft else 0); STRIP_Y[z] = ys
    s = T.strip(z, y0, y1, soft); put('zone_strip_%s.svg' % z, s); symbol('zb_strip_' + z, s)
bg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 390 %d">' % L.H]
for z in order:
    s = files['zone_strip_%s.svg' % z]; inner = re.match(r'<svg[^>]*>(.*)</svg>$', s, re.S).group(1)
    bg.append('<g transform="translate(0 %d)">%s</g>' % (STRIP_Y[z], inner))
put('zones_bg.svg', ''.join(bg) + '</svg>')
for name, fn, sid in (('river.svg', T.river, 'env_river'), ('bridge.svg', T.bridge, 'env_bridge'), ('ice_patch.svg', T.ice, 'env_ice')):
    s = fn(); put(name, s); symbol(sid, s)
# ابرها
for k in T.CLOUDS:
    s = T.cloud_sym(k); symbol('env_cloud_' + k, s)
put('clouds.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 330 56">%s</svg>' % ''.join('<svg x="%d" width="110" height="56" viewBox="0 0 110 56">%s</svg>' % (i * 110, re.match(r'<svg[^>]*>(.*)</svg>$', T.cloud_sym(k), re.S).group(1)) for i, k in enumerate(T.CLOUDS)))
# درخت‌ها
trees = T.tree_syms()
for k, s in trees.items(): symbol('env_' + k, s)
tl = list(trees); cell = 100
put('trees.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d 110">%s</svg>' % (cell * len(tl), ''.join(
    '<svg x="%d" width="%d" height="%d" viewBox="%s">%s</svg>' % (i * cell, cell, 110, re.search(r'viewBox="([^"]+)"', trees[k]).group(1), re.match(r'<svg[^>]*>(.*)</svg>$', trees[k], re.S).group(1)) for i, k in enumerate(tl))))
# --- تزئین ---
dec = DC.decor_svgs(); dec.update(T.sea_decor())
SEA = [('buoy', 18), ('sail', 28), ('islet', 28), ('lighthouse', 28), ('crate', 24)]
for k, s in dec.items(): symbol('env_' + k, s)
DEC_SET = {z: [(n, rx) for n, _, rx in items] for z, items in DC.SET.items()}
DEC_SET['sea'] = SEA
for z, items in list(DC.SET.items()) + [('sea', [(n, None, rx) for n, rx in SEA])]:
    zz = 'city' if z == 'sea' else z
    cells = ''.join('<svg x="%d" width="120" height="120" viewBox="0 0 120 120">%s</svg>' % (i * 124, re.match(r'<svg[^>]*>(.*)</svg>$', dec['dec_%s_%s' % (zz, n)], re.S).group(1)) for i, (n, _, _) in enumerate(items))
    put('props_%s.svg' % z, '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d 120">%s</svg>' % (124 * len(items), cells))
sg = DC.start_gate(); put('start_gate.svg', sg); symbol('env_start_gate', sg)
for nm, fn in (('map', DC.tile_map), ('cards', DC.tile_cards), ('practice', DC.tile_practice), ('guide', DC.tile_guide)):
    s = fn(); put('tile_bldg_%s.svg' % nm, s); symbol('env_tile_' + nm, s)
# --- تونل (رشته‌کوه بین ردیف‌های TI و TI+1؛ دهانه روی لبهٔ چپ) ---
TI = L.TUNNEL_ROW
cyb, cyt = L.NODES[TI]['cy'], L.NODES[TI + 1]['cy']; hb_abs = cyb - 40; ht_abs = cyt + 22
S = L.path_samples(); cand = [(abs(y - hb_abs), x, y) for x, y in S if x < 100 and cyt < y < cyb]
xm = min(cand)[1]; TOPY = ht_abs - 26
svg_t, TH = T.tunnel(hb_abs - TOPY, 26, xm)
put('tunnel.svg', svg_t); symbol('env_tunnel', svg_t)
TUN = dict(row_low=TI, row_high=TI + 1, x=0, y=TOPY, w=390, h=TH, portal_x=round(xm, 1), portal_y=round(hb_abs, 1))
# --- بنر اسکله (دریای v4) ---
nest = X.n12('env_dock'); inner = re.match(r'<svg[^>]*>(.*)</svg>$', nest, re.S).group(1)
banner = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 390 200"><rect width="390" height="200" fill="#075a73"/><rect width="390" height="70" fill="#0a6e8a" opacity=".5"/>'
          '<path d="M10,40 q8,-5 16,0 q8,5 16,0 M250,30 q8,-5 16,0 M330,64 q8,-5 16,0" fill="none" stroke="#aef0f4" stroke-width="2.6" stroke-linecap="round" opacity=".4"/>'
          '<rect x="-4" y="150" width="398" height="52" fill="#c6c1b6"/><rect x="-4" y="150" width="398" height="10" fill="#e9e4d6"/><path d="M-4,150H394" stroke="#241a5e" stroke-width="4.5"/>'
          '<svg x="40" y="-52" width="300" height="285" viewBox="0 0 200 190">%s</svg></svg>' % inner)
put('dock_env_banner.svg', banner); symbol('env_dock_banner', banner)
sil = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 760">']
for k, n in enumerate(range(1, 13)):
    reg = X.REG['node_%02d' % n]; cx, cy = (k % 6) * 200 + 100, (k // 6) * 190 + 150
    for row, col in ((0, '#241a5e'), (2, '#8a8a8a')):
        sil.append('<g transform="translate(%d %d)" fill="%s">%s</g>' % (cx, cy + row * 190, col, ''.join(re.sub(r'<(\w+) ', r'<\1 ', g) for g in reg)))
put('silhouette_test.svg', ''.join(sil) + '</svg>')
# --- sprite (با فیلتر دست‌لرزی env_wob: فقط برای خط ≥4.5؛ صفحهٔ بازبینی/نقشه به‌کار می‌برد) ---
FILT = '<filter id="env_wob" filterUnits="userSpaceOnUse" x="-30" y="-30" width="450" height="%d"><feTurbulence type="fractalNoise" baseFrequency=".045" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.4"/></filter>' % (L.H + 60)
put('sprite_env.svg', '<svg xmlns="http://www.w3.org/2000/svg"><defs>%s%s</defs>%s</svg>' % (CSS, FILT, ''.join(SYM.values())))
print('symbols', len(SYM), 'files', len(files))
# --- strings.fa.json (عنوان بزرگ زمین‌ها؛ از titles_fa.json، پیش‌نویس) ---
Tt = json.load(open('/home/claude/science-games/docs/research/world/titles_fa.json', encoding='utf-8'))
LT = Tt['lands']
def short(t): return t.split(':')[0].replace('سرزمین ', '').strip()
ZT = {'sports': short(LT['L1']['title']), 'space': short(LT['L2']['title']), 'farm': short(LT['LW']['title']), 'city': 'شهر صنعتی'}
STR = {'_doc': 'متن‌های بوم نقشهٔ env. فقط این فایل؛ پیش‌نویس (draft). عنوان کامل زمین‌ها در titles_fa.json است و اینجا فقط نام کوتاه روی زمین آمده.'}
for z, t in ZT.items(): STR['env.zone_title.%s' % z] = dict(text=t, status='draft')
STR['env.start.label'] = dict(text='شروع', status='draft', note='جاگذار بازبینی روی تابلوی شروع؛ متن نهایی کار UI')
STR['env.here.label'] = dict(text='تو اینجایی', status='draft', note='از flow-demo/strings.fa.json (جاگذار بازبینی؛ نشانهٔ اصلی کار UI است)')
json.dump(STR, open(OUT / 'strings.fa.json', 'w'), ensure_ascii=False, indent=1)
# --- node_map.json + slots.json ---
Nd = Tt['nodes']
nm = [dict(id=n['id'], order=n['p'] + 1, zone=n['zone'], kind=n['kind'], asset=n['asset'], env_title=Nd.get(n['id'], {}).get('title', ''), concept=Nd.get(n['id'], {}).get('subtitle', ''), visible=n['id'] != 'M12', note=('پنهان: همان کارخانه' if n['id'] == 'M12' else '')) for n in L.NODES]
json.dump(dict(_doc='جدول نگاشت ۳۴ گره (۳۳ دیدنی) ← بنای شاخص node_NN یا پروپ prop_NN (روی پایهٔ env_pad_<زمین>_<شکل>). r2: همان نگاشت v5؛ ساخته از team/env_gen_r2/gen_env.py', canvas=dict(width=L.W, height=L.H), zones={z: dict(y0=a, y1=b) for z, (a, b) in L.ZB.items()}, start=dict(x=L.START[0], y=L.START[1]), coast_y=T.COAST_Y, tunnel=TUN, landmarks=12, props=sorted({n['asset'] for n in L.NODES if n['kind'] == 'prop'}), nodes=nm), open(OUT / 'node_map.json', 'w'), ensure_ascii=False, indent=1)
sl = L.slots()
json.dump(dict(_doc='جای هر گره، بوم 390×%d (بدون تغییر نسبت به v5). base_center = لنگر؛ place_at = گوشهٔ بالا-چپ symbol (بنا 200×190، پروپ 120×100). نشان سختی بالا-ابتدا، قفل/انجام پایین-ابتدا، پای b1 لبهٔ جلوی پایه، برچسب زیر پایه. مسیر r2: ردیف افقی از مرکز هر گره (path_d). عنوان‌های زمین: zone_titles با کلید strings.' % L.H, canvas=[L.W, L.H], path_d=L.path_d(), slots=sl), open(OUT / 'slots.json', 'w'), ensure_ascii=False, indent=1)
