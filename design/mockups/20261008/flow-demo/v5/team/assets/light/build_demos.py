#!/usr/bin/env python3
"""light_layers_demo.html و transition_demo.html را می‌سازد (SVGها inline تا var(--l-*) کار کند). پس از build_light.py اجرا شود."""
import re, os, json
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, '..')
T = json.load(open(os.path.join(H, 'zone_tokens.json'))); L = T['lights']
css = open(os.path.join(H, 'tokens.css')).read()
defs = open(os.path.join(H, 'common_defs.svg')).read()
sprite = open(os.path.join(A, 'character', 'sprite_char.svg')).read()
def node(n, tag):
    s = open(os.path.join(A, 'env', f'node_{n:02d}.svg')).read()
    s = re.sub(r'node_%02d_' % n, f'node_{n:02d}_{tag}_', s)
    return s
BASE = '''*{box-sizing:border-box;margin:0}body{background:#e8e4f4;color:#241a5e;font:16px/1.7 Vazirmatn,system-ui,sans-serif;direction:rtl;padding:12px 16px 40px;max-width:430px;margin:auto}
h1{font-size:22px}h2{font-size:18px;margin:14px 0 6px}p{font-size:14px}
.bar{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}button,label.chk{min-height:48px;min-width:48px;padding:0 16px;border:2.6px solid #241a5e;border-radius:14px 6px 14px 6px;background:#fff4d2;color:#241a5e;font:700 16px Vazirmatn,sans-serif;display:inline-flex;align-items:center;gap:6px}
button:focus-visible{outline:3px solid #2fb8a8;outline-offset:2px}'''
# ---------- لایه‌ها ----------
def panel(l):
    d = L[l]
    cells = ''.join(f'<div class="c">{node(n, l)}</div>' for n in range(1, 13))
    chars = ''.join(f'<svg class="cs-bust-82" width="82" height="82" viewBox="0 0 100 100"><use href="#ch-b{i}" class="ch-happy"/></svg>' for i in (2, 3, 4)) + \
        '<svg class="cs-full-110" width="73" height="110" viewBox="0 0 100 150"><use href="#ch-b1" class="ch-happy ch-pose-stand"/></svg>'
    return f'''<section data-light="{l}" style="background:linear-gradient({d["sky0"]},{d["sky2"]} 12%,{d["water"]} 12%)"><h2 style="color:#fff4d2;text-shadow:0 0 0 #000">{l}</h2><div class="g">{cells}</div><div class="ch">{chars}</div></section>'''
page = f'''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>light layers demo</title>
<style>{css}
{open(os.path.join(A,'character','char.css')).read()}
{BASE}
section{{border:4.5px solid #241a5e;border-radius:18px;padding:8px;margin:10px 0}}
.g{{display:grid;grid-template-columns:repeat(4,1fr);gap:2px}}.c svg{{width:100%;height:auto;display:block}}
.ch{{display:flex;justify-content:space-around;align-items:flex-end;margin-top:6px}}
.off-rim .elit,.off-rim [id$="-lit"]{{display:none}}.off-shade .esh,.off-shade [id$="-shade"]{{display:none}}.off-win .ew{{display:none}}
</style></head><body>
<h1>rim / shade / windows روی ۱۲ بنا و ۴ شخصیت</h1>
<p>سه نور؛ نور بالا-چپ، بدون blend. تیک‌ها لایه‌ها را خاموش می‌کنند. ابزار آزمایشی طراح نور، نه آزموده با کودک.</p>
<div class="bar"><label class="chk"><input type="checkbox" id="r" checked> rim</label><label class="chk"><input type="checkbox" id="s" checked> shade</label><label class="chk"><input type="checkbox" id="w" checked> windows</label></div>
<div id="all">{panel('day')}{panel('dusk')}{panel('night')}</div>
{sprite}
<script>var a=document.getElementById('all');[['r','off-rim'],['s','off-shade'],['w','off-win']].forEach(function(p){{document.getElementById(p[0]).onchange=function(e){{a.classList.toggle(p[1],!e.target.checked)}}}})</script>
</body></html>'''
open(os.path.join(H, 'light_layers_demo.html'), 'w').write(page)

# ---------- انتقال ----------
STARS = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff"/>' for x, y, r in [(120, 30, 1.6), (190, 70, 1.2), (250, 25, 1.8), (310, 80, 1.3), (350, 40, 1.6), (90, 110, 1.2), (330, 140, 1.2), (220, 120, 1.4)])
def scene(l, tag, extra='', win=False):
    d = L[l]
    return f'''<g data-light="{l}"><rect width="390" height="250" fill="url(#lt-sky-{l})"/>{extra}<rect y="250" width="390" height="190" fill="{d["water"]}"/>
<svg x="45" y="150" width="300" height="285" viewBox="0 0 200 190" overflow="visible">{node(12, tag).replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 190">','<g>').replace('</svg>','</g>')}</svg></g>'''
night_extra = f'<g id="tr-stars" fill="#fff">{STARS}</g><path id="tr-moon" d="M64 34A24 24 0 1 0 88 62A19 19 0 0 1 64 34Z" fill="{L["night"]["lit"]}"/>'
dusk_extra = '<rect y="190" width="390" height="60" fill="#f2a65a" fill-opacity=".35"/>'
sc = lambda inner, id_: f'<svg id="{id_}" viewBox="0 0 390 440" width="100%" role="img" aria-label="scene">{inner}</svg>'
dusk_water = '<use href="#lt-reflect-dusk" transform="translate(240 270)"/><use href="#lt-reflect-dusk" transform="translate(60 330) scale(.8)"/>'
tr = f'''<div id="scene" data-light="day"><svg viewBox="0 0 390 440" width="100%" role="img" aria-label="harbor day-night"><g class="lt-layer" data-for="day" id="tr-day">{scene('day','d')}</g>
<g class="lt-layer" data-for="night" id="tr-night">{scene('night','n', night_extra)}</g></svg></div>'''
dusk = f'<div data-light="dusk">' + sc(scene('dusk', 'k', dusk_extra).replace('</g>', dusk_water + '</g>', 1) if False else scene('dusk', 'k', dusk_extra) + dusk_water, 'tr-dusk') + '</div>'
page2 = f'''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>transition demo</title>
<style>{css}
{BASE}
.fr{{border:4.5px solid #241a5e;border-radius:18px;overflow:hidden;margin:8px 0;line-height:0}}
#scene svg,#tr-dusk{{display:block}}
</style></head><body>
<h1>انتقال روز ← شب (۱٫۲ ثانیه، فقط opacity)</h1>
<p>دو لایهٔ روز و شب هر دو در DOM می‌مانند؛ فقط شفافیتشان عوض می‌شود. با reduced-motion بدون انیمیشن. نه متغیر در حال میان‌یابی، نه blend.</p>
<div class="bar"><button id="b1" type="button">روز</button><button id="b2" type="button">شب</button></div>
<div class="fr">{tr}</div>
<h2>غروب ثابت (فقط صحنهٔ ماجرای ۲)</h2><p>گرمای لبه از بالا-چپ + سایهٔ بنفش داخل سیلوئت؛ بازتاب افقی؛ بدون multiply سراسری و بدون دایرهٔ خورشید.</p>
<div class="fr">{dusk}</div>
{defs}
<script>var s=document.getElementById('scene');function set(v){{s.setAttribute('data-light',v)}}document.getElementById('b1').onclick=function(){{set('day')}};document.getElementById('b2').onclick=function(){{set('night')}};var q=location.search.match(/light=(day|night)/);if(q)set(q[1])</script>
</body></html>'''
open(os.path.join(H, 'transition_demo.html'), 'w').write(page2)
print('demos built', os.path.getsize(os.path.join(H, 'light_layers_demo.html')) // 1024, os.path.getsize(os.path.join(H, 'transition_demo.html')) // 1024, 'KB')
