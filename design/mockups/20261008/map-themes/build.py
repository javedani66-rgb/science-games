#!/usr/bin/env python3
"""Preview of the proposed land/zone themes. Names come from titles_fa.json, colours from design/themes/map-themes-proposal.json.
Run: python3 design/mockups/20261008/map-themes/build.py -> index.html"""
import json, pathlib
R = pathlib.Path(__file__).resolve().parents[4]
T = json.load(open(R/'design/themes/map-themes-proposal.json', encoding='utf-8'))
TT = json.load(open(R/'docs/research/world/titles_fa.json', encoding='utf-8'))
D = json.load(open(R/'docs/research/world/nodes_v2_draft.json', encoding='utf-8'))
NT = {k: v['title'] for k, v in TT['nodes'].items()}
def star(x, y, r=2): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".85"/>'
SC = {
 'L1': lambda v: f'''<rect width="400" height="170" fill="{v['sky']}"/>
  <path d="M0 96 H400 V170 H0Z" fill="{v['gnd']}"/>
  <ellipse cx="200" cy="130" rx="190" ry="34" fill="{v['gnd']}" stroke="#fff" stroke-width="3" opacity=".95"/>
  <ellipse cx="200" cy="130" rx="150" ry="22" fill="{v['hill']}" stroke="#fff" stroke-width="2"/>
  <path d="M0 96 q40 -26 80 0 t80 0 t80 0 t80 0 t80 0" fill="#E8D7B2" opacity=".9"/>
  <path d="M174 120 h52" stroke="#fff" stroke-width="3"/><circle cx="200" cy="130" r="9" fill="none" stroke="#fff" stroke-width="2"/>
  <path d="M60 126 V104 H92 V126" stroke="#fff" stroke-width="4" fill="none"/><circle cx="130" cy="124" r="6" fill="#fff" stroke="#5B3A29" stroke-width="1.5"/>
  <path d="M255 118 h110" stroke="#8B6B4A" stroke-width="4"/><rect x="305" y="108" width="6" height="20" fill="#C93B22"/>
  <path d="M370 60 v-30 l22 8 l-22 8" fill="#fff" stroke="#5B3A29" stroke-width="2"/>''',
 'L2': lambda v: f'''<rect width="400" height="170" fill="{v['sky']}"/>
  {''.join(star(x,y,r) for x,y,r in [(30,24,2),(80,60,1.5),(140,20,2),(210,50,1.5),(300,26,2),(350,70,1.5),(260,90,1.5),(40,95,1.5)])}
  <circle cx="330" cy="40" r="22" fill="#F7F1F4"/><circle cx="338" cy="35" r="20" fill="{v['sky']}"/>
  <circle cx="120" cy="70" r="16" fill="#8E6FA3"/><ellipse cx="120" cy="70" rx="26" ry="5" fill="none" stroke="#C9B6D6" stroke-width="3"/>
  <path d="M0 140 Q120 112 240 138 T400 130 V170 H0Z" fill="{v['hill']}"/><rect y="150" width="400" height="20" fill="{v['gnd']}"/>
  <path d="M200 40 v50 m-8 -10 l8 10 l8 -10" stroke="#fff" stroke-width="3" fill="none" opacity=".7"/>
  <path d="M230 150 a42 42 0 0 1 84 0z" fill="#EDEAF5" stroke="#8E6FA3" stroke-width="3"/><rect x="262" y="132" width="20" height="18" fill="#8E6FA3"/><path d="M300 108 v-26" stroke="#EDEAF5" stroke-width="3"/><circle cx="300" cy="80" r="4" fill="#6BD2C6"/>''',
 'LW': lambda v: f'''<rect width="400" height="170" fill="{v['sky']}"/>
  <circle cx="70" cy="46" r="26" fill="#FFD36B"/><g stroke="#F6A23A" stroke-width="4" stroke-linecap="round" opacity=".8"><line x1="70" y1="8" x2="70" y2="0"/><line x1="108" y1="46" x2="118" y2="46"/><line x1="32" y1="46" x2="22" y2="46"/><line x1="97" y1="19" x2="104" y2="12"/><line x1="43" y1="19" x2="36" y2="12"/></g>
  <path d="M0 118 Q110 90 220 118 T400 112 V170 H0Z" fill="{v['hill']}"/><path d="M0 140 Q120 124 240 144 T400 136 V170 H0Z" fill="{v['gnd']}"/>
  <path d="M240 120 L252 62 L264 120Z" fill="#D8B48A" stroke="{v['edge']}" stroke-width="2"/>
  <g stroke="{v['edge']}" stroke-width="4" stroke-linecap="round"><line x1="252" y1="62" x2="222" y2="34"/><line x1="252" y1="62" x2="282" y2="34"/><line x1="252" y1="62" x2="224" y2="90"/><line x1="252" y1="62" x2="280" y2="90"/></g><circle cx="252" cy="62" r="5" fill="{v['edge']}"/>
  <circle cx="340" cy="118" r="20" fill="none" stroke="#6C8FA6" stroke-width="5"/><path d="M340 98 v40 M320 118 h40 M326 104 l28 28 M354 104 l-28 28" stroke="#6C8FA6" stroke-width="3"/>
  <path d="M0 150 h400" stroke="#6C8FA6" stroke-width="4" opacity=".0"/><rect x="120" y="124" width="34" height="14" rx="3" fill="#B98A45" stroke="{v['edge']}" stroke-width="2"/><circle cx="130" cy="140" r="5" fill="{v['edge']}"/><circle cx="146" cy="140" r="5" fill="{v['edge']}"/>
  <path d="M330 24 l-14 28 h12 l-8 26 l24 -34 h-14 l10 -20z" fill="#FFD36B" stroke="{v['edge']}" stroke-width="2" transform="translate(-70 -8) scale(.7)"/>''',
 'LM': lambda v: f'''<rect width="400" height="170" fill="{v['sky']}"/>
  {''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="{v["edge"]}" opacity=".35"/>' for x in range(30,400,52) for y in (28,60))}
  <g fill="none" stroke="{v['hdr']}" stroke-width="5" opacity=".28"><circle cx="80" cy="95" r="38" stroke-dasharray="10 6"/><circle cx="80" cy="95" r="14"/><circle cx="165" cy="70" r="26" stroke-dasharray="8 5"/><circle cx="165" cy="70" r="9"/></g>
  <path d="M250 110 h110" stroke="{v['hdr']}" stroke-width="7" opacity=".28" stroke-linecap="round"/><path d="M285 110 l12 -14 l12 14z" fill="{v['hdr']}" opacity=".28"/>
  <rect y="135" width="400" height="35" fill="{v['gnd']}"/>''',
 'Z1': lambda v: f'''<rect width="400" height="170" fill="{v['sky']}"/><path d="M0 115 Q120 85 230 112 T400 104 V170 H0Z" fill="{v['hill']}"/><rect y="135" width="400" height="35" fill="{v['gnd']}"/>
  <path d="M120 122 L280 106" stroke="#7A5A3A" stroke-width="8" stroke-linecap="round"/><path d="M200 114 l-18 26 h36z" fill="#8B6B4A"/>
  <circle cx="125" cy="108" r="9" fill="#E9A93B"/><circle cx="278" cy="92" r="14" fill="#E9A93B"/>''',
 'Z2': lambda v: f'''<rect width="400" height="170" fill="{v['sky']}"/><rect y="132" width="400" height="38" fill="{v['gnd']}"/>
  <path d="M0 132 V96 h30 v-16 h28 v16 h24 v36z" fill="{v['hill']}"/>
  <g fill="#E4CDB4" stroke="{v['edge']}" stroke-width="2"><rect x="110" y="62" width="14" height="72"/><rect x="170" y="62" width="14" height="72"/><rect x="104" y="54" width="26" height="9"/><rect x="164" y="54" width="26" height="9"/><path d="M124 62 Q147 30 170 62z"/></g>
  <path d="M215 134 h20 v-9 h20 v-9 h20 v-9 h20 v-9 h20 v-9" stroke="{v['edge']}" stroke-width="3" fill="none" opacity=".6"/>
  <path d="M350 134 l22 -52 l12 52z" fill="#8F7A66" stroke="{v['edge']}" stroke-width="2"/><path d="M40 150 q22 -9 44 0 q-22 -10 -44 -20" stroke="{v['edge']}" stroke-width="3" fill="none" opacity=".6"/>''',
 'Z3': lambda v: f'''<rect width="400" height="170" fill="{v['sky']}"/><rect y="110" width="400" height="60" fill="{v['hill']}"/>
  <path d="M0 125 q25 -9 50 0 t50 0 t50 0 t50 0 t50 0 t50 0 t50 0 t50 0" stroke="#fff" stroke-width="3" fill="none" opacity=".7"/><rect x="250" y="102" width="150" height="14" fill="#8F7A66"/>
  <rect x="335" y="30" width="7" height="74" fill="#5C6B78"/><path d="M338 34 H240" stroke="#5C6B78" stroke-width="6"/><circle cx="262" cy="46" r="9" fill="none" stroke="#12405F" stroke-width="3"/><path d="M262 55 v32" stroke="#12405F" stroke-width="2"/><rect x="252" y="86" width="20" height="14" fill="#E9A93B"/>
  <g fill="none" stroke="#12405F" stroke-width="4" opacity=".4"><circle cx="70" cy="62" r="24" stroke-dasharray="7 5"/><circle cx="108" cy="82" r="16" stroke-dasharray="6 4"/></g>''',
}
def box(kind, key, name, extra=''):
    v = T[kind][key]
    return f'''<section class="box" style="--hdr:{v['hdr']};--hink:{v['hink']};--paper:{v['paper']};--edge:{v['edge']};--btn:{v['btn']}">
 <svg viewBox="0 0 400 170" preserveAspectRatio="xMidYMid slice" aria-hidden="true">{SC[key](v)}</svg>
 <header><b>{name}</b><small>{key}</small></header>
 <div class="body"><p>{v['scene']}</p>{extra}<div class="sw">{''.join(f'<i style="background:{v[c]}" title="{c}"></i>' for c in ('hdr','paper','sky','hill','gnd','edge','btn'))}</div></div></section>'''
lands = ''.join(box('lands', k, TT['lands'][k]['title']) for k in ('L1','L2','LW','LM'))
zones = ''.join(box('zones', k, TT['zones'][k]['title']) for k in ('Z1','Z2','Z3'))
html = f'''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>پیشنهاد تم سرزمین‌ها</title>
<style>@font-face{{font-family:V;src:local("Vazirmatn")}}body{{margin:0;padding:16px;background:#EDF4F7;color:#1B2A41;font:16px/1.7 Vazirmatn,Tahoma,sans-serif}}
h1{{font-size:22px;margin:0 0 4px}}h2{{font-size:18px;margin:28px 0 10px}}.note{{max-width:60ch;color:#56677F;margin:0 0 8px}}
.grid{{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(280px,1fr))}}
.box{{background:var(--paper);border:3px solid var(--edge);border-radius:18px;overflow:hidden}}.box svg{{display:block;width:100%;height:150px}}
.box header{{background:var(--hdr);color:var(--hink);padding:10px 14px;display:flex;justify-content:space-between;align-items:center;gap:8px}}
.box header b{{font-size:18px}}.box header small{{opacity:.7;font-family:monospace}}.body{{padding:10px 14px 14px;color:#1B2A41}}.body p{{margin:0 0 10px;font-size:15px}}
.sw{{display:flex;gap:6px}}.sw i{{width:26px;height:26px;border-radius:7px;border:1px solid #0003}}
.btn{{display:inline-block;background:var(--btn);color:#fff;padding:4px 14px;border-radius:12px;margin-bottom:8px}}
.dif{{display:flex;gap:8px;margin:16px 0}}.dif span{{padding:4px 12px;border-radius:10px;border:3px solid #211D19;color:#211D19}}</style></head><body>
<h1>تم موقت سرزمین‌ها و منطقه‌ها (تأیید مالک؛ بعداً با تصویر طراحی‌شده جایگزین می‌شود)</h1>
<p class="note">رنگ‌ها و محیط‌ها را مالک به‌عنوان موقت تأیید کرد (۸ اکتبر). رنگ‌ها از تم‌های بازی اولیه گرفته شد (شنی، آبی‌سبز، بنفش). نام‌ها همان نام‌های موقت‌اند و با عوض‌شدنشان فقط تصویر پس‌زمینه باید با نام جدید جور شود. متن همیشه روی سطح روشن است.</p>
<h2>چهار سرزمین (به ترتیب مسیر)</h2><div class="grid">{lands}</div>
<h2>سه منطقهٔ سرزمین ماشین‌های ساده (رنگ سرزمین ماشین‌ها را ادامه می‌دهند)</h2><div class="grid">{zones}</div>
<h2>نشان سختی ثابت می‌ماند (تم روی آن اثر نمی‌گذارد)</h2><div class="dif"><span style="background:#B9DB66">ساده</span><span style="background:#F4BE4F">چالشی</span><span style="background:#EF7464">خیلی سخت</span></div>
</body></html>'''
open(pathlib.Path(__file__).with_name('index.html'), 'w', encoding='utf-8').write(html)
print('ok', len(html))
