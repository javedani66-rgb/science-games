#!/usr/bin/env python3
"""سازندهٔ دارایی‌های env (v5). اجرا: python3 gen_env.py  → v5/team/assets/env/*"""
import math, random, re, json, pathlib
import layout as L
from shapes import *
import buildings as X, terrain as T, decor as DC
OUT = L.OUT; OUT.mkdir(parents=True, exist_ok=True)
files = {}
def put(name, svg): files[name] = svg; (OUT / name).write_text(svg, encoding='utf-8')
SYM = {}     # id نماد → (viewBox, محتوا)
def symbol(sid, svg, drop_style=True):
    m = re.match(r'<svg[^>]*viewBox="([^"]+)"[^>]*>(.*)</svg>$', svg, re.S); vb, inner = m.group(1), m.group(2)
    if drop_style: inner = re.sub(r'<style>.*?</style>', '', inner, flags=re.S)
    SYM[sid] = '<symbol id="%s" viewBox="%s">%s</symbol>' % (sid, vb, inner)
# --- ۱۲ بنا ---
for n, fn in X.LAND.items():
    s = fn(); put('node_%02d.svg' % n, s); symbol('node_%02d' % n, s)
# --- پایه‌ها + پروپ‌ها ---
for z in ('sports', 'space', 'farm', 'city'):
    for v, (rx, sd) in enumerate(((38, 1), (44, 5), (34, 9))):
        b = B('env_pad_%s_%s' % (z, 'abc'[v])); pad(b, z, rx, sd); s = b.svg((120, 100), 60, 78, rx, 12, (-rx, -14, rx, 14)); symbol('env_pad_%s_%s' % (z, 'abc'[v]), s)
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
for name, fn, sid in (('river.svg', T.river, 'env_river'), ('bridge.svg', T.bridge, 'env_bridge'), ('ice_patch.svg', T.ice, 'env_ice'), ('sea_edge.svg', T.sea_edge, 'env_sea_edge'),
                      ('bay_left.svg', T.bay_left, 'env_bay_left'), ('skyline_city.svg', T.skyline, 'env_skyline'), ('cloud_edge.svg', T.cloud_edge, 'env_cloud_edge'),
                      ('boardwalk_skin.svg', T.boardwalk_sample, 'env_boardwalk')):
    s = fn(); put(name, s); symbol(sid, s)
trees = T.tree_syms()
for k, s in trees.items(): symbol('env_' + k, s)
put('trees.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 110">%s%s%s</svg>' % tuple(
    '<svg x="%d" width="%d" height="%d" viewBox="%s">%s</svg>' % (x, w, h, re.search(r'viewBox="([^"]+)"', trees[k]).group(1), re.match(r'<svg[^>]*>(.*)</svg>$', trees[k], re.S).group(1)) for k, x, w, h in (('tree_pine', 0, 80, 100), ('tree_pop', 90, 60, 100), ('tree_bush', 160, 70, 60))))
# --- تزئین ---
dec = DC.decor_svgs()
for k, s in dec.items(): symbol('env_' + k, s)
for z, items in DC.SET.items():
    cells = ''.join('<svg x="%d" width="120" height="120" viewBox="0 0 120 120">%s</svg>' % (i * 124, re.match(r'<svg[^>]*>(.*)</svg>$', dec['dec_%s_%s' % (z, n)], re.S).group(1)) for i, (n, _, _) in enumerate(items))
    put('props_%s.svg' % z, '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d 120">%s</svg>' % (124 * len(items), cells))
sg = DC.start_gate(); put('start_gate.svg', sg); symbol('env_start_gate', sg)
for nm, fn in (('map', DC.tile_map), ('cards', DC.tile_cards), ('practice', DC.tile_practice), ('guide', DC.tile_guide)):
    s = fn(); put('tile_bldg_%s.svg' % nm, s); symbol('env_tile_' + nm, s)
# --- بنر اسکله ---
nest = X.n12('env_dock'); inner = re.match(r'<svg[^>]*>(.*)</svg>$', nest, re.S).group(1)
banner = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 390 200"><rect width="390" height="200" fill="#1f87b8"/><rect width="390" height="70" fill="#1b79a6" opacity=".5"/>'
          '<path d="M10,40 q8,-5 16,0 q8,5 16,0 M250,30 q8,-5 16,0 M330,64 q8,-5 16,0" fill="none" stroke="#fff" stroke-width="1.2" opacity=".6"/>'
          '<rect x="-4" y="150" width="398" height="52" fill="#c6c1b6"/><rect x="-4" y="150" width="398" height="10" fill="#e9e4d6"/><path d="M-4,150H394" stroke="#241a5e" stroke-width="4.5"/>'
          '<svg x="40" y="-52" width="300" height="285" viewBox="0 0 200 190">%s</svg></svg>' % inner)
put('dock_env_banner.svg', banner); symbol('env_dock_banner', banner)
# --- silhouette test ---
sil = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 760">']
for k, n in enumerate(range(1, 13)):
    reg = X.REG['node_%02d' % n]; cx, cy = (k % 6) * 200 + 100, (k // 6) * 190 + 150
    for row, col in ((0, '#241a5e'), (2, '#8a8a8a')):
        sil.append('<g transform="translate(%d %d)" fill="%s">%s</g>' % (cx, cy + row * 190, col, ''.join(re.sub(r'<(\w+) ', r'<\1 ', g) for g in reg)))
put('silhouette_test.svg', ''.join(sil) + '</svg>')
# --- sprite ---
put('sprite_env.svg', '<svg xmlns="http://www.w3.org/2000/svg"><defs>%s</defs>%s</svg>' % (CSS, ''.join(SYM.values())))
print('symbols', len(SYM), 'files', len(files))
# --- node_map.json + slots.json ---
Tt = json.load(open(L.HERE.parents[3] / '..' / '..' / '..' / 'docs' / 'research' / 'world' / 'titles_fa.json', encoding='utf-8')) if False else json.load(open('/home/claude/science-games/docs/research/world/titles_fa.json', encoding='utf-8'))['nodes']
nm = [dict(id=n['id'], order=n['p'] + 1, zone=n['zone'], kind=n['kind'], asset=n['asset'], env_title=Tt.get(n['id'], {}).get('title', ''), concept=Tt.get(n['id'], {}).get('subtitle', ''), visible=n['id'] != 'M12', note=('پنهان: همان کارخانه' if n['id'] == 'M12' else '')) for n in L.NODES]
json.dump(dict(_doc='جدول نگاشت ۳۴ گره (۳۳ دیدنی) ← بنای شاخص node_NN یا پروپ prop_NN (روی پایهٔ env_pad_<زمین>). ساخته از team/env_gen/gen_env.py', canvas=dict(width=L.W, height=L.H), zones={z: dict(y0=a, y1=b) for z, (a, b) in L.ZB.items()}, start=dict(x=L.START[0], y=L.START[1]), landmarks=12, props=sorted({n['asset'] for n in L.NODES if n['kind'] == 'prop'}), nodes=nm), open(OUT / 'node_map.json', 'w'), ensure_ascii=False, indent=1)
json.dump(dict(_doc='جای هر گره، بوم 390×%d. base_center = لنگر (پایین-وسط بنا)؛ place_at = گوشهٔ بالا-چپ symbol (بنا 200×190، پروپ 120×100). نشان سختی بالا-ابتدا، قفل/انجام پایین-ابتدا، پای b1 لبهٔ جلوی پایه، برچسب زیر پایه. نور: بالا-چپ.' % L.H, canvas=[L.W, L.H], slots=L.slots()), open(OUT / 'slots.json', 'w'), ensure_ascii=False, indent=1)
