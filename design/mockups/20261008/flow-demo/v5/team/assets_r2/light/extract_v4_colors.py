#!/usr/bin/env python3
"""استخراج رنگ‌های واقعی v4 (فقط خواندن v4) -> zone_tokens_v4.json
هر مقدار: hex + منبع (عکس+روش یا فایل کد+خط). روش عکس: میانهٔ پیکسل‌هایی از عکس که به hex کد نزدیک‌اند (ΔRGB<45)
تا شیء/خط روی زمین (بنا، مسیر، درخت) وارد نشود؛ دانه/ویگنت v4 همان‌طور که دیده می‌شود در عدد می‌ماند."""
import json, os, re
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.abspath(os.path.join(H, '../../../../v4/style'))
SH = os.path.join(V4, 'shots'); GEN = os.path.join(V4, 'gen')
def hx(a): return '#%02x%02x%02x' % tuple(int(round(v)) for v in a)
def rgb(h): h = h.lstrip('#'); return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)])
def img(f): return np.array(Image.open(os.path.join(SH, f)).convert('RGB')).reshape(-1, 3)
def near(f, code, tol=45, rows=None):
    a = np.array(Image.open(os.path.join(SH, f)).convert('RGB'))
    if rows: a = a[rows[0]:rows[1]]
    a = a.reshape(-1, 3); d = np.abs(a - rgb(code)).max(1); m = a[d < tol]
    return hx(np.median(m, 0)), int(len(m))
def box(f, b):
    a = np.array(Image.open(os.path.join(SH, f)).convert('RGB'))[b[1]:b[3], b[0]:b[2]].reshape(-1, 3)
    return hx(np.median(a, 0))
src = {}
def put(k, hexv, how): src[k] = {'hex': hexv, 'src': how}
# ---- کد: ثابت‌ها
head = open(os.path.join(GEN, 'gen_head.py')).read()
zline = re.search(r"Z = dict\((.*?)\)", head).group(1)
Zc = dict(re.findall(r"(\w+)='(#[0-9a-fA-F]{6})'", zline))
mp = open(os.path.join(GEN, 'gen_map.py')).read(); cd = open(os.path.join(GEN, 'gen_card.py')).read(); tr = open(os.path.join(GEN, 'gen_transition.py')).read()
# ---- زمین‌ها: عکس (دیده‌شده) + کد (تعریف)
maps = {'sports': ('grass', 'r10_map_y1900.png'), 'space': ('space', 'r10_map_y1450.png'), 'farm': ('farm', 'r11_map_y0.png'), 'city': ('sea', 'r11_map_y0.png')}
for z, (ck, f) in maps.items():
    v, n = near(f, Zc[ck], 45)
    put(f'ground.{z}', v, f'عکس v4/style/shots/{f}: میانهٔ {n} پیکسل نزدیک به کد Z[{ck}]={Zc[ck]} در gen_head.py')
    put(f'ground.{z}.code', Zc[ck], f'gen_head.py خط Z = dict(...) کلید {ck}')
v, n = near('r10_map_y1450.png', '#d4efff', 30); put('ground.ice', v, f'عکس r10_map_y1450: پیکسل‌های نزدیک Z[ice]={Zc["ice"]} (لکهٔ یخ پیست)')
v, n = near('r11_map_y0.png', '#f0cf7a', 40); put('ground.sand', v, 'عکس r11_map_y0: ساحل شنی نزدیک #f0cf7a (gen_map.py: wavy_top 700 fill #f0cf7a)')
put('ground.sand.code', '#f0cf7a', 'gen_map.py خط ساحل شنی')
# ---- مسیر
put('path.cream', '#fff3c4', 'gen_head.py CREAM')
put('path.outline', '#241a5e', 'common.py OUT')
put('path.river_fill', '#58d8ee', 'gen_map.py رود pth(...,\'#58d8ee\',31)')
put('path.river_foam', '#d4f6ff', 'gen_map.py خط‌چین رود')
put('path.done_dash', '#f0b429', 'gen_map.py D_DONE خط‌چین طلایی')
put('path.boardwalk', '#c98a45', 'gen_map.py تابلو/اسکله #c98a45')
# مسیر دیده‌شده در نقشه: کرم کامل (انجام‌شده) و کرم .۳۴ روی خط دور (باقی‌مانده)
v, n = near('r10_map_y1900.png', '#fff3c4', 25); put('path.done_seen', v, f'عکس r10_map_y1900: پیکسل‌های نزدیک کرم ({n})')
rest = 0.34 * rgb('#fff3c4') + 0.66 * rgb('#241a5e'); put('path.rest_calc', hx(rest), 'محاسبه: کرم با opacity .34 روی خط دور (gen_map.py D_REST)')
v, n = near('r11_map_y0.png', hx(rest), 30, rows=(380, 600)); put('path.rest_seen', v, f'عکس r11_map_y0: پیکسل‌های نزدیک رنگ محاسبه‌ای ({n})')
# ---- UI
put('ui.bar', '#241a5e', 'gen_map.py #bar path fill'); put('ui.bar_seen', box('r11_map_y0.png', (0, 0, 6, 10)), 'عکس r11_map_y0 گوشهٔ بالا-چپ (ویگنت v4)')
put('ui.chip', '#4b3b9e', 'gen_map.py css .chip background'); put('ui.chip_seen', box('r11_map_y0.png', (15, 40, 35, 50)), 'عکس r11_map_y0 چیپ غیرفعال')
put('ui.chip_text', '#fff3c4', 'gen_map.py css .chip color')
put('ui.chip_on', '#ffd23f', 'gen_map.py .chip.on'); put('ui.chip_on_seen', box('r11_map_y0.png', (125, 14, 140, 22)), 'عکس r11_map_y0 چیپ فعال')
put('ui.chip_shadow', '#120c3a', 'gen_map.py box-shadow چیپ'); put('ui.menu', '#fff3c4', 'gen_map.py .menu')
put('ui.label_fill', '#fff3c4', 'gen_map.py برچسب گره'); put('ui.zone_title_fill', '#ffffff', 'gen_map.py ZS عنوان زمین؛ stroke #241a5e 9')
put('ui.here_ring', '#ffd23f', 'gen_map.py حلقهٔ اینجایی'); put('ui.here_bubble', '#ffd23f', 'gen_map.py حباب اینجایی')
put('ui.start_sign', '#ffd23f', 'gen_map.py تابلوی شروع')
# ---- کارت شب
put('card.bg', '#190539', 'gen_card.py BG'); put('card.bg_seen', box('r10_card-night_vfront.png', (5, 5, 30, 30)), 'عکس r10_card-night_vfront گوشه (گرادیان n1 رویش)')
put('card.front_top', '#25cdc0', 'gen_card.py front card_svg c1'); put('card.front_bottom', '#0a86a4', 'gen_card.py c2')
put('card.front_top_seen', box('r10_card-night_vfront.png', (60, 70, 80, 80)), 'عکس r10_card-night_vfront بالای کارت')
put('card.glow', '#46f0d8', 'gen_card.py glow'); put('card.plate', '#07203a', 'gen_card.py plate')
put('card.plate_seen', box('r10_card-night_vfront.png', (60, 540, 330, 560)), 'عکس r10_card-night_vfront صفحهٔ متن')
put('card.frame_gold', '#ffd23f', 'gen_card.py قاب طلایی'); put('card.frame_cream', '#fff3c4', 'gen_card.py قاب نقطه‌چین')
put('card.edge', '#190539', 'gen_card.py لبهٔ کارت stroke BG')
put('card.pill_cyan', '#46f0d8', 'gen_card.py .pill.cyan'); put('card.pill_pink', '#ff7be5', 'gen_card.py .pill.pink'); put('card.pill_gold', '#ffd23f', 'gen_card.py .pill.gold')
put('card.pill_text', '#190539', 'gen_card.py .pill color')
put('card.title_fill', '#ffffff', 'gen_card.py .title؛ stroke #190539'); put('card.title_glow', '#ff5ad6', 'gen_card.py text-shadow عنوان')
put('card.body_text', '#ffffff', 'gen_card.py .body')
put('card.kept_top', '#7a6af5', 'gen_card.py slot kept'); put('card.kept_bottom', '#4a2fb8', 'gen_card.py slot kept'); put('card.kept_glow', '#a99dff', 'gen_card.py slot kept')
put('card.empty_fill', '#2a0b60', 'gen_card.py slot empty'); put('card.empty_dash', '#9a78e0', 'gen_card.py ico_plus/dash')
put('card.locked', '#34145f', 'gen_card.py slot locked'); put('card.locked_icon', '#cdb8ff', 'gen_card.py ico_lock')
put('card.plank_top', '#d9a05a', 'gen_card.py plank'); put('card.plank_side', '#8a5a2e', 'gen_card.py plank')
put('card.nebula1', '#5a14a8', 'gen_card.py n1'); put('card.nebula2', '#a0197a', 'gen_card.py n2'); put('card.star', '#e9dcff', 'gen_card.py ستاره')
# ---- زمین: جزئیات (از کد)
for k, v, s in [('tree', '#2f8a2b', 'gen_head.py tree()'), ('tree_hi', '#6fcf5e', 'gen_head.py tree()'), ('pine', '#2a8a58', 'gen_head.py pinet()'),
                ('crater', '#8e2c1a', 'gen_head.py crater()'), ('crater_rim', '#ffb08a', 'gen_head.py crater()'),
                ('hay', '#e9c24a', 'gen_map.py کاه‌بسته'), ('wave', '#aef0f4', 'gen_map.py wave'), ('cloud', '#ffffff', 'gen_head.py cloud()')]:
    put('detail.' + k, v, s)
# ---- سختی (v4 نشان سختی نداشت؛ رنگ از پالت v4 کد گرفته شده)
put('hard.easy', '#2fa44a', 'gen_head.py s_grav ساقهٔ سیب سبز #2fa44a (سبز روشن‌ترِ v4)')
put('hard.mid', '#ff9d1c', 'gen_head.py b_harbor منقار #ff9d1c')
put('hard.hard', '#ff4b4b', 'gen_head.py موشک/سیب #ff4b4b')
# ---- انتقال v4 (برای بازسازی بدون multiply)
put('night.overlay_top', '#6a55d8', 'gen_transition.py .night gradient'); put('night.overlay_bottom', '#3a1c90', 'gen_transition.py .night gradient')
put('night.overlay_opacity', '0.8', 'gen_transition.py .night opacity'); put('night.moon', '#fff6c8', 'gen_transition.py .moon'); put('night.window', '#fff3a8', 'gen_transition.py .lights')
put('dusk_v4.overlay', '#ff7a3d>#c2379a>#5a2a9a', 'gen_transition.py .dusk (multiply .72) - رد‌شده'); 
json.dump(src, open(os.path.join(H, 'zone_tokens_v4.json'), 'w'), ensure_ascii=False, indent=1)
for k, v in src.items():
    if k.startswith(('ground', 'path', 'ui.chip', 'ui.bar')): print(k, v['hex'])
