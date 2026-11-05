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
  <g fill="{v['hdr']}" opacity=".3"><rect x="20" y="70" width="40" height="70"/><rect x="66" y="50" width="34" height="90"/><rect x="106" y="84" width="50" height="56"/><rect x="250" y="62" width="44" height="78"/><rect x="300" y="86" width="60" height="54"/><rect x="128" y="40" width="10" height="46"/><rect x="334" y="48" width="10" height="40"/></g>
  <g fill="none" stroke="{v['hdr']}" stroke-width="5" opacity=".3"><circle cx="205" cy="84" r="34" stroke-dasharray="10 6"/><circle cx="205" cy="84" r="12"/></g>
  <rect y="138" width="400" height="32" fill="{v['gnd']}"/><g fill="#8F7A66" stroke="{v['edge']}" stroke-width="2"><rect x="170" y="116" width="10" height="26"/><rect x="230" y="116" width="10" height="26"/><rect x="166" y="108" width="78" height="9" rx="3"/></g>''',
 'Z1': lambda v: f'''<rect width="400" height="170" fill="{v['sky']}"/><rect y="136" width="400" height="34" fill="{v['gnd']}"/>
  <g stroke="{v['edge']}" stroke-width="4" fill="none"><path d="M40 136 V62 M110 136 V62 M40 62 H110 M40 100 H110"/><path d="M110 62 H250 M200 62 V30 H320 M300 30 V80" /></g>
  <rect x="294" y="80" width="16" height="12" fill="#B98A45" stroke="{v['edge']}" stroke-width="2"/>
  <path d="M150 128 L270 112" stroke="#7A5A3A" stroke-width="8" stroke-linecap="round"/><path d="M210 120 l-14 22 h28z" fill="#8B6B4A"/><rect x="146" y="106" width="22" height="18" fill="#C3CED8" stroke="{v['edge']}" stroke-width="2"/>
  <path d="M330 136 l30 -20 h16 l-8 20z" fill="#6C7C8A" stroke="{v['edge']}" stroke-width="2"/><circle cx="352" cy="142" r="9" fill="#2B3640"/>''',
 'Z2': lambda v: f'''<rect width="400" height="170" fill="{v['sky']}"/><rect y="130" width="400" height="40" fill="{v['gnd']}"/>
  <g fill="#C79A6B" stroke="{v['edge']}" stroke-width="2"><rect x="30" y="98" width="130" height="32" rx="16"/><path d="M170 130 L240 130 L240 118z"/></g><circle cx="46" cy="114" r="8" fill="#E4CDB4"/><path d="M40 114 h12" stroke="{v['edge']}" stroke-width="2"/>
  <path d="M96 98 l10 -34 l10 34z" fill="#8F8F95" stroke="{v['edge']}" stroke-width="2"/>
  <g stroke="{v['edge']}" stroke-width="3" fill="#B7B7BD"><path d="M250 70 h70 v12 h-70z"/><path d="M250 70 l-10 6 l10 6" fill="none"/></g><g stroke="{v['edge']}" stroke-width="2"><path d="M262 70 v-6 M274 70 v-6 M286 70 v-6 M298 70 v-6 M310 70 v-6"/></g>
  <g fill="#E4CDB4" stroke="{v['edge']}" stroke-width="2"><rect x="270" y="112" width="100" height="8"/><rect x="278" y="122" width="100" height="8"/></g>
  <path d="M190 40 v26 M182 58 l8 8 l8 -8 M174 34 l32 0" stroke="{v['edge']}" stroke-width="3" fill="none"/><path d="M180 150 q20 -9 40 0" stroke="{v['edge']}" stroke-width="3" fill="none" opacity=".5"/>''',
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
