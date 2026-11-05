#!/usr/bin/env python3
"""tokens.css و palette_*.svg و common_defs.svg را از zone_tokens.json می‌سازد (دست‌نزن به خروجی‌ها)."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); T = json.load(open(os.path.join(H, 'zone_tokens.json')))
U, Z, L, HD, W, I, P = T['ui'], T['zones'], T['lights'], T['hardness'], T['water'], T['ice'], T['path']
c = ['/* خودکار از zone_tokens.json (build_light.py). فقط روشن/غروب/شب + رنگ‌ها. بدون blend و بدون filter زنده. نور: بالا-چپ، در هر سه نور ثابت. */', ':root{']
for k, v in U.items(): c.append(f'  --c-{k.replace("_","-")}: {v};')
for k, v in HD.items(): c.append(f'  --hard-{k}: {v["hex"]};')
for zk, z in Z.items():
    for k in ('base', 'shade', 'patch', 'night', 'ring'): c.append(f'  --z-{zk}-{k}: {z[k]};')
    c.append(f'  --z-{zk}-ring-outline: {z["ring_outline_px"]}px;')
for g, d in (('water', W), ('ice', I), ('path', P)):
    for k, v in d.items(): c.append(f'  --{g}-{k.replace("_","-")}: {v};')
c += ['  --line-6: 6px; --line-4-5: 4.5px; --line-2-6: 2.6px; --line-1-2: 1.2px;', '  --light-dir: top-left; --light-transition: 1.2s;']
def block(name, d):
    o = [f'[data-light="{name}"]{{']
    for k in ('sky0', 'sky1', 'sky2', 'water', 'lit', 'shade', 'line', 'build', 'pier'): o.append(f'  --l-{k}: {d[k]};')
    o.append(f'  --l-windows: {d["windows"] or "transparent"}; --l-windows-opacity: {1 if d["windows"] else 0};')
    s = d['shadow']; o.append(f'  --l-shadow-color: {s["color"]}; --l-shadow-opacity: {s["opacity"]}; --l-shadow-dx: {s["dx"]}px; --l-shadow-dy: {s["dy"]}px;')
    i = d['intensity']; o.append(f'  --l-lit-a: {i["lit_a"]}; --l-shade-a: {i["shade_a"]}; --l-nlit-a: {i["nlit_a"]}; --l-nshade-a: {i["nshade_a"]};')
    o.append('}'); return o
c.append('  /* پیش‌فرض = روز */')
for k in ('sky0', 'sky1', 'sky2', 'water', 'lit', 'shade', 'line', 'build', 'pier'): c.append(f'  --l-{k}: {L["day"][k]};')
i0 = L['day']['intensity']
c += [f'  --l-lit-a: {i0["lit_a"]}; --l-shade-a: {i0["shade_a"]}; --l-nlit-a: {i0["nlit_a"]}; --l-nshade-a: {i0["nshade_a"]};', '  --l-windows: transparent; --l-windows-opacity: 0;', f'  --l-shadow-color: {L["day"]["shadow"]["color"]}; --l-shadow-opacity: {L["day"]["shadow"]["opacity"]}; --l-shadow-dx: 8px; --l-shadow-dy: 6px;', '}']
for n in ('day', 'dusk', 'night'): c += block(n, L[n])
c += ['/* لایه‌های ثابت انتقال: هر لایه یک id (با پیشوند صفحه) و data-for؛ فقط opacity عوض می‌شود. روز←شب مستقیم 1.2ث. غروب میان‌یابی نیست. */',
      '.lt-layer{opacity:0;transition:opacity var(--light-transition) ease-in-out}',
      '[data-light="day"] .lt-layer[data-for~="day"],[data-light="dusk"] .lt-layer[data-for~="dusk"],[data-light="night"] .lt-layer[data-for~="night"]{opacity:1}',
      '.lt-layer[data-for="windows"]{opacity:0}[data-light="night"] .lt-layer[data-for="windows"]{opacity:1}',
      '@media (prefers-reduced-motion: reduce){.lt-layer{transition:none}}']
c += ['/* شدت rim/سایهٔ بناهای env (کلاس‌های .elit/.esh در node_*.svg مقدار ثابت دارند؛ این‌ها آن‌ها را به نور وصل می‌کنند). شخصیت‌ها خودشان var(--l-lit-a) و var(--l-shade-a) می‌خوانند. */', '[data-light] .elit{opacity:var(--l-nlit-a,.3)}', '[data-light] .esh{opacity:var(--l-nshade-a,.22)}']
open(os.path.join(H, 'tokens.css'), 'w').write('\n'.join(c) + '\n')

# common_defs.svg
d = ['<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true"><defs>',
     '<!-- فقط پشتیبان ابزار ماکت؛ در خروجی نهایی brush در هندسه پخته می‌شود -->',
     '<filter id="lt-brush" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3" xChannelSelector="R" yChannelSelector="G"/></filter>']
for n in ('day', 'dusk', 'night'):
    l = L[n]; d.append(f'<linearGradient id="lt-sky-{n}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{l["sky0"]}"/><stop offset=".55" stop-color="{l["sky1"]}"/><stop offset="1" stop-color="{l["sky2"]}"/></linearGradient>')
    d.append(f'<linearGradient id="lt-water-{n}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{l["water"]}"/><stop offset="1" stop-color="{l["water"]}"/></linearGradient>')
d += ['<clipPath id="lt-clip-card"><rect width="360" height="240" rx="12"/></clipPath>', '<clipPath id="lt-clip-node"><rect width="200" height="180"/></clipPath>',
      '<!-- رگهٔ بازتاب آب غروب: خط‌های افقی نه لکه -->', f'<g id="lt-reflect-dusk" fill="#ffb27a" fill-opacity=".4"><rect x="0" y="0" width="120" height="3" rx="1.5"/><rect x="20" y="9" width="90" height="3" rx="1.5"/><rect x="40" y="18" width="60" height="3" rx="1.5"/></g>', '</defs></svg>']
open(os.path.join(H, 'common_defs.svg'), 'w').write('\n'.join(d) + '\n')

# palette svgs
def pal(n):
    l = L[n]; items = [('sky0', l['sky0']), ('sky1', l['sky1']), ('sky2', l['sky2']), ('water', l['water']), ('pier', l['pier']), ('build', l['build']), ('lit (rim)', l['lit']), ('shade', l['shade']), ('shadow', l['shadow']['color']), ('line', l['line']), ('windows', l['windows'] or 'off'), ('accent', U['accent_yellow'])]
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 340" font-family="sans-serif" font-size="12">', f'<rect width="520" height="340" fill="{U["card_bg"] if n=="night" else "#ffffff"}"/>',
         f'<text x="12" y="22" font-size="16" font-weight="700" fill="{"#fff4d2" if n=="night" else U["line"]}">palette {n} (light from top-left)</text>']
    tc = '#fff4d2' if n == 'night' else U['line']
    for i, (k, v) in enumerate(items):
        x = 12 + (i % 4) * 126; y = 36 + (i // 4) * 70
        fill = v if v != 'off' else 'none'
        s.append(f'<rect x="{x}" y="{y}" width="116" height="36" rx="6" fill="{fill}" stroke="{U["line"] if n!="night" else "#fff4d2"}" stroke-width="1.2"/><text x="{x}" y="{y+50}" fill="{tc}">{k}</text><text x="{x+60}" y="{y+50}" fill="{tc}" font-family="monospace">{v}</text>')
    # نمونهٔ ایستا: آسمان/آب/اسکله/بنا با rim و سایه
    s += [f'<g transform="translate(12,250)"><rect width="496" height="80" fill="url(#g{n})"/>', f'<defs><linearGradient id="g{n}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{l["sky0"]}"/><stop offset="1" stop-color="{l["sky2"]}"/></linearGradient></defs>',
          f'<rect y="44" width="496" height="36" fill="{l["water"]}"/><rect x="40" y="52" width="170" height="28" fill="{l["pier"]}" stroke="{l["line"]}" stroke-width="2.6"/>',
          f'<rect x="90" y="14" width="60" height="38" fill="{l["build"]}" stroke="{l["line"]}" stroke-width="4.5"/><rect x="92" y="16" width="8" height="34" fill="{l["lit"]}"/><rect x="132" y="16" width="16" height="34" fill="{l["shade"]}" fill-opacity=".8"/>',
          (f'<rect x="108" y="24" width="8" height="8" fill="{l["windows"]}"/><rect x="120" y="24" width="8" height="8" fill="{l["windows"]}"/>' if l['windows'] else ''), '</g></svg>']
    open(os.path.join(H, f'palette_{n}.svg'), 'w').write('\n'.join(s) + '\n')
for n in ('day', 'dusk', 'night'): pal(n)
print('built')
