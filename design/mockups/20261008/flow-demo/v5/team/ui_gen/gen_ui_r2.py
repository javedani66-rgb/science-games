#!/usr/bin/env python3
"""مولد رابط v5-r2 (بازگشت به رنگ و حس v4). اجرا:  python3 gen_ui_r2.py
خروجی در ../assets_r2/ui/: sprite_ui.svg، assets.json، ui_tokens.css، ui_kit.html.
متن فقط با کلید از v5/strings.fa.json و ../strings.fa.json (flow). رنگ‌ها از light/zone_tokens.json."""
import json, math, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
V5 = HERE.parents[1]
OUT = HERE.parent / 'assets_r2' / 'ui'; OUT.mkdir(parents=True, exist_ok=True)
Z = json.load(open(HERE.parent / 'assets/light/zone_tokens.json', encoding='utf-8'))
V4 = dict(line='#241a5e', edge='#120c3a', cream='#fff3c4', gold='#ffd23f', chip='#4b3b9e', cyan='#46f0d8', pink='#ff7be5', purple='#8a4fe0', night='#190539', night_violet='#7a6af5')
S = {}
S.update(json.load(open(V5.parent / 'strings.fa.json', encoding='utf-8')))
S.update(json.load(open(V5 / 'strings.fa.json', encoding='utf-8')))
def t(k, **kw): return S[k]['text'].format(**kw)
U = Z['ui']; H = Z['hardness']
LINE = 'var(--ui-line,%s)' % V4['line']
C1, C2, C3, C4, C5, C6 = ('var(--ui-c1,%s)' % V4['cream'], 'var(--ui-c2,%s)' % V4['cyan'], 'var(--ui-c3,%s)' % V4['chip'],
                      'var(--ui-c4,%s)' % V4['pink'], 'var(--ui-c5,#ffffff)', 'var(--ui-c6,%s)' % V4['gold'])
def P(d, fill, w=2.6, extra=''):
    return f'<path d="{d}" style="fill:{fill};stroke:{LINE};stroke-width:{w};stroke-linejoin:round;stroke-linecap:round"{extra}/>'
def R(x, y, w, h, r, fill, sw=2.6, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" style="fill:{fill};stroke:{LINE};stroke-width:{sw};stroke-linejoin:round"{extra}/>'
def Ci(cx, cy, r, fill, sw=2.6):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" style="fill:{fill};stroke:{LINE};stroke-width:{sw}"/>'
def L(d, w=2.6, col=None):
    return f'<path d="{d}" style="fill:none;stroke:{col or LINE};stroke-width:{w};stroke-linecap:round;stroke-linejoin:round"/>'
def CH(x, y, w, h, c, fill, sw=2.6):
    """مستطیل با دو گوشهٔ بُریده (بالا-راست و پایین-چپ) = «دست» ماشین‌ساز؛ گوشه‌های دیگر تیز"""
    d = f'M{x} {y} H{x+w-c} L{x+w} {y+c} V{y+h} H{x+c} L{x} {y+h-c}Z'
    return f'<path d="{d}" style="fill:{fill};stroke:{LINE};stroke-width:{sw};stroke-linejoin:miter;stroke-miterlimit:4"/>'
def gear(cx, cy, ro, ri, n, tw=6, vw=10):
    pts = []
    for i in range(n):
        a = 360 / n * i
        for da, r in ((-vw, ri), (-tw, ro), (tw, ro), (vw, ri)):
            ang = math.radians(a + da - 90)
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z'

# ---------- ۲۱ آیکون (شبکهٔ 48، خط 2.6) — رنگ‌ها از v4: کرم، فیروزه‌ای، بنفش چیپ، صورتی، زرد ----------
ICONS = {}
ICONS['menu'] = ''.join(CH(8, y, 32, 7, 3, LINE) for y in (10, 20.5, 31))          # v4: خط‌های تیره روی دکمهٔ کرم
ICONS['next'] = P('M7 24 L21 10 L21 18 L41 18 L41 30 L21 30 L21 38Z', C2)
ICONS['close'] = P('M11 17 L17 11 L24 18 L31 11 L37 17 L30 24 L37 31 L31 37 L24 30 L17 37 L11 31 L18 24Z', C4)
ICONS['map'] = P('M6 12 L17 8 L31 12 L42 8 L42 36 L31 40 L17 36 L6 40Z', C1) + L('M17 8 V36 M31 12 V40') + Ci(30, 21, 5, C6)
ICONS['cards'] = '<g transform="rotate(-12 20 25)">' + CH(9, 10, 22, 30, 6, C3) + '</g><g transform="rotate(9 28 23)">' + CH(17, 8, 22, 30, 6, C1) + '</g>' + P('M28 17 L33 24 L28 31 L23 24Z', C6, 2.2, ' transform="rotate(9 28 23)"')
ICONS['practice'] = CH(5, 21, 38, 20, 5, C2) + CH(4, 13, 40, 9, 3, C6) + CH(17, 28, 14, 6, 2, C1, 2.2) + P('M13 13 L16 6 L28 6 L31 13', C5, 2.2)
ICONS['guide'] = P('M9 31 Q9 11 24 11 Q39 11 39 31Z', C6) + P('M5 31 H43 V36 H5Z', C3) + P('M20 11 V31 M28 11 V31', C6, 2.2).replace('fill:' + C6, 'fill:none') + CH(19, 6, 10, 6, 2, C2, 2.2)
ICONS['search'] = Ci(20, 20, 12, C2) + f'<rect x="27.5" y="31.5" width="17" height="8" rx="4" transform="rotate(45 36 35.5)" style="fill:{C3};stroke:{LINE};stroke-width:2.6"/>' + L('M14 16 Q16 12 21 12', 2.2, C5)
ICONS['lock'] = f'<path d="M15 22 V16 a9 9 0 0 1 18 0 V22" style="fill:none;stroke:{LINE};stroke-width:8.2;stroke-linecap:round"/><path d="M15 22 V16 a9 9 0 0 1 18 0 V22" style="fill:none;stroke:{C1};stroke-width:3;stroke-linecap:round"/>' + CH(9, 21, 30, 21, 6, C6) + Ci(24, 30, 3.4, C3, 2.2) + CH(22.6, 31, 2.8, 6, 0.8, C3, 2)
ICONS['eye'] = P('M3 24 Q24 5 45 24 Q24 43 3 24Z', C5) + Ci(24, 24, 8.5, C2) + Ci(24, 24, 3.2, LINE, 1)
ICONS['box'] = P('M24 5 L42 13 L42 34 L24 43 L6 34 L6 13Z', C3) + P('M24 5 L42 13 L24 22 L6 13Z', C6) + L('M24 22 V43')
ICONS['mypos'] = P('M24 5 L39 41 L24 33 L9 41Z', C6)
ICONS['pin'] = P('M24 44 C14 31 9 25 9 18 a15 15 0 0 1 30 0 c0 7 -5 13 -15 26Z', C4) + Ci(24, 18, 6, C1)
ICONS['flag'] = CH(9, 5, 5, 38, 1.5, C1) + P('M14 8 L40 14 L14 22Z', C4) + f'<path d="M20 9.5 L26 11 L24 15.5 L18 14Z M31 12.5 L37 14 L30 17.2Z" style="fill:{LINE}"/>'
ICONS['game'] = P(gear(24, 24, 21, 16.5, 8, 7, 11), C2) + Ci(24, 24, 6.5, C6)
ICONS['flip'] = '<path d="M37 24 a13 13 0 1 1 -4 -9.3" style="fill:none;stroke:%s;stroke-width:8.2;stroke-linecap:round"/><path d="M37 24 a13 13 0 1 1 -4 -9.3" style="fill:none;stroke:%s;stroke-width:3;stroke-linecap:round"/>' % (LINE, C2) + P('M31 5 L42 15 L28 19Z', C2)
ICONS['lesson'] = P('M24 12 Q14 7 5 10 V38 Q14 35 24 40Z', C1) + P('M24 12 Q34 7 43 10 V38 Q34 35 24 40Z', C1) + P('M32 8 V22 L35.5 19 L39 22 V9', C4, 2.2) + L('M10 17 Q16 16 20 18 M10 24 Q16 23 20 25', 2)
ICONS['hint'] = P('M24 5 a13 13 0 0 1 8 23 V32 H16 V28 A13 13 0 0 1 24 5Z', C6) + CH(16, 32, 16, 9, 3, C3) + L('M20 36.5 H28', 2, C1) + L('M17 15 Q19 11 23 11', 2.2, C5)
ICONS['hold'] = Ci(24, 24, 19, C1) + '<path d="M24 11 A13 13 0 1 1 11 24" style="fill:none;stroke:%s;stroke-width:6;stroke-linecap:round"/>' % C4 + Ci(24, 24, 4.5, C3, 2.2)
ICONS['skip'] = P('M38 9 L16 24 L38 39Z', C6) + CH(7, 9, 7, 30, 2.5, C1)

ICONS['play'] = P('M14 8 L40 24 L14 40Z', LINE)
def sym(i, vb, body, extra=''):
    return f'<symbol id="{i}" viewBox="{vb}" style="stroke-linejoin:round;stroke-linecap:round{extra}">{body}</symbol>'
syms = [sym('ui-ic-' + k, '0 0 48 48', v) for k, v in ICONS.items()]

# ---------- قرص سختی 56×30: رنگ‌های ثابت سختی؛ دورِ تیره 2.6 + حاشیهٔ کرم بیرونی 2 (روی هر زمین جدا بماند) ----------
PEAK = {'easy': V4['cream'], 'mid': V4['line'], 'hard': V4['cream']}   # قلهٔ نارنجی تیره می‌شود (کرم روی نارنجی ۲٫۴۱:۱ بود)
def badge(level):
    hx, n = H[level]['hex'], H[level]['peaks']
    w, g = 12, 3.2
    tot = n * w + (n - 1) * g
    x0 = (56 - tot) / 2
    pk = PEAK[level]; pl = V4['line'] if pk != V4['line'] else V4['cream']
    peaks = ''.join(f'<path d="M{x0+i*(w+g):.1f} 22.5 L{x0+i*(w+g)+w/2:.1f} 8.5 L{x0+i*(w+g)+w:.1f} 22.5Z" '
                    f'style="fill:{pk};stroke:{pl};stroke-width:1.2;stroke-linejoin:round"/>' for i in range(n))
    pd = 'M10 1.3 H46 L54.7 10 V20 L46 28.7 H10 L1.3 20 V10Z'
    rim = f'<path d="{pd}" style="fill:none;stroke:{V4["cream"]};stroke-width:calc(2.6px + 4px)"/>'
    pill = f'<path d="{pd}" style="fill:{hx};stroke:{V4["line"]};stroke-width:2.6"/>'
    return sym(f'ui-badge-{level}', '0 0 56 30', rim + pill + peaks, ';overflow:visible')
syms += [badge(k) for k in ('easy', 'mid', 'hard')]
# قفل 32px: هشت‌ضلعی بنفش چیپ، قفل کرم، حاشیهٔ کرم بیرونی (مثل v4: دایرهٔ کرم + قفل)
syms.append(sym('ui-lock', '0 0 32 32',
    f'<path d="M10 1.3 H22 L30.7 10 V22 L22 30.7 H10 L1.3 22 V10Z" style="fill:none;stroke:{C1};stroke-width:5.6;stroke-linejoin:miter"/>'
    f'<path d="M10 1.3 H22 L30.7 10 V22 L22 30.7 H10 L1.3 22 V10Z" style="fill:{C3};stroke:{LINE};stroke-width:2.6;stroke-linejoin:miter"/>'
    f'<path d="M11.5 15 V12.5 a4.5 4.5 0 0 1 9 0 V15" style="fill:none;stroke:{C1};stroke-width:2.4;stroke-linecap:round"/>'
    f'<rect x="9.5" y="14.5" width="13" height="9.5" rx="2.6" style="fill:{C1}"/><circle cx="16" cy="19" r="1.7" style="fill:{C3}"/>', ';overflow:visible'))
# حلقهٔ «اینجایی» مثل v4: خط تیره ضخیم + خط‌چین زرد 5.5 (می‌چرخد؛ با reduced-motion ثابت)
syms.append(sym('ui-ring', '0 0 100 100',
    f'<circle cx="50" cy="50" r="42" style="fill:none;stroke:{LINE};stroke-width:var(--ui-ring-ol,10px)"/>'
    f'<circle class="ui-ring-dash" cx="50" cy="50" r="42" style="fill:none;stroke:var(--ui-ring,{V4["gold"]});stroke-width:5.5;stroke-dasharray:16 10"/>', ';overflow:visible'))
syms.append(sym('ui-check', '0 0 20 20',
    f'<circle cx="10" cy="10" r="8.7" style="fill:{C2};stroke:{LINE};stroke-width:2.6"/>'
    f'<path d="M5.8 10.3 L8.6 13 L14.2 7" style="fill:none;stroke:{LINE};stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round"/>'))
GEAR = gear(24, 24, 21.4, 19.2, 12, 6.5, 10.5)
syms.append(sym('ui-gearbtn', '0 0 48 54',
    f'<path d="{GEAR}" transform="translate(0 5)" style="fill:var(--ui-gear-lip,{V4["edge"]});stroke:{LINE};stroke-width:3.5"/>'
    f'<path d="{GEAR}" style="fill:var(--ui-gear,{V4["cream"]});stroke:{LINE};stroke-width:3.5"/>'))
SPRITE = '<svg xmlns="http://www.w3.org/2000/svg">' + '\n'.join(syms) + '</svg>'
(OUT / 'sprite_ui.svg').write_text(SPRITE, encoding='utf-8')

A = {f'ui-ic-{k}': {'viewBox': '0 0 48 48', 'grid': 48, 'stroke': 2.6, 'role': 'icon'} for k in ICONS}
A.update({'ui-badge-easy': {'viewBox': '0 0 56 30', 'peaks': 1, 'word_key': 'difficulty.easy', 'role': 'hardness'},
          'ui-badge-mid': {'viewBox': '0 0 56 30', 'peaks': 2, 'word_key': 'difficulty.mid', 'role': 'hardness'},
          'ui-badge-hard': {'viewBox': '0 0 56 30', 'peaks': 3, 'word_key': 'difficulty.hard', 'role': 'hardness'},
          'ui-lock': {'viewBox': '0 0 32 32', 'role': 'lock'}, 'ui-ring': {'viewBox': '0 0 100 100', 'vars': ['--ui-ring-ol', '--ui-ring'], 'role': 'here-ring'},
          'ui-check': {'viewBox': '0 0 20 20', 'role': 'chip-tick'}, 'ui-gearbtn': {'viewBox': '0 0 48 54', 'vars': ['--ui-gear', '--ui-gear-lip'], 'role': 'icon-button-base'}})
json.dump({'sprite': 'sprite_ui.svg', 'arrow_convention': 'ui-ic-next رو به انتهای خط (فیزیکی چپ)؛ «برگرد» = همان با class ui-flip', 'assets': A},
          open(OUT / 'assets.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------- ui_tokens.css ----------
WAVE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='10' viewBox='0 0 120 10'%3E%3Cpath d='M0 5 Q15 0 30 5 T60 5 T90 5 T120 5' fill='none' stroke='%23ffd23f' stroke-width='3' opacity='.55'/%3E%3C/svg%3E\")")
CSS = f'''/* ui_tokens.css r2 (ui-artist، بازگشت به v4). رنگ و حس از v4/style/map.html و card-night.html:
   دکمه/چیپ با خط 3.5px #241a5e و سایهٔ لبهٔ 4px #120c3a؛ چیپ فعال زرد #ffd23f با حلقهٔ کرم؛ بقیهٔ چیپ‌ها بنفش #4b3b9e؛ دکمهٔ منو کرم.
   اصلی فیروزه‌ای، ثانویه کرم (شکل بُریده)، فیلم صورتی، «نگه‌دار» بنفش، «بذارش…» زرد. شب: درخشش به‌جای لبه (مثل pill های کارت v4). بدون filter/blend. */
:root{{
  --ui-line:{V4['line']}; --ui-edge:{V4['edge']}; --ui-cream:{V4['cream']}; --ui-gold:{V4['gold']}; --ui-chip:{V4['chip']};
  --ui-cyan:{V4['cyan']}; --ui-pink:{V4['pink']}; --ui-purple:{V4['purple']}; --ui-violet:{V4['chip']};
  --ui-night-bg:{V4['night']}; --ui-night-line:{V4['night']};
  --ui-ink-disabled:#4a4268; --ui-disabled-bg:#d9d3e8;
  --ui-r-big:18px; --ui-r-small:8px; --ui-l35:3.5px; --ui-l26:2.6px; --ui-l12:1.2px; --ui-lip:4px; --ui-lip-pressed:2px;
  --ui-touch:48px; --ui-gap:7px; --ui-gutter:16px;
  --ui-font-title:'Lalezar','Vazirmatn',sans-serif; --ui-font:'Vazirmatn',system-ui,sans-serif;
  --ui-fs-page:28px; --ui-fs-zone:24px; --ui-fs-sheet:24px; --ui-fs-tile:22px; --ui-fs-btn:22px; --ui-fs-body:16px; --ui-fs-small:14px; --ui-lh:1.7;
}}
[data-world=night]{{--ui-line:{V4['night']}; --ui-c3:{V4['night_violet']}; --ui-edge:{V4['night']}}}
.ui-svg{{display:inline-block;inline-size:48px;block-size:48px;flex:none}}
.ui-svg--40{{inline-size:40px;block-size:40px}} .ui-svg--32{{inline-size:32px;block-size:32px}}
.ui-flip{{transform:scaleX(-1)}}
.ui-badge{{display:inline-block;inline-size:56px;block-size:30px;overflow:visible;flex:none}}
.ui-lockbadge{{display:inline-block;inline-size:32px;block-size:32px;flex:none;overflow:visible}}
.ui-ring{{overflow:visible}} .ui-ring-dash{{animation:uispin 14s linear infinite}} @keyframes uispin{{to{{stroke-dashoffset:-260}}}}
/* نشان سختی + واژه: پلاک کرم (واژه همیشه تیره روی کرم، ≥14px)؛ واژه از کلید difficulty.* */
.ui-hard{{display:inline-flex;align-items:center;gap:8px;min-block-size:36px;padding:3px 12px 3px 8px;background:var(--ui-cream);border:var(--ui-l26) solid #241a5e;color:#241a5e;font:700 16px/1.2 var(--ui-font);border-radius:4px 14px 4px 14px}}
/* دکمه («پلاک»): شکل v5، رنگ و لبهٔ v4 */
.ui-btn{{--bg:var(--ui-cyan);--glow:rgba(70,240,216,.6);--ink:#241a5e;position:relative;display:inline-flex;align-items:center;justify-content:center;gap:8px;
  min-block-size:52px;min-inline-size:var(--ui-touch);padding:0 22px;margin-block-end:var(--ui-lip);box-sizing:border-box;
  font:400 var(--ui-fs-btn)/1.2 var(--ui-font-title);color:var(--ink);background:var(--bg);border:var(--ui-l35) solid #241a5e;cursor:pointer;
  border-start-start-radius:var(--ui-r-big);border-end-end-radius:var(--ui-r-big);border-start-end-radius:var(--ui-r-small);border-end-start-radius:var(--ui-r-small);
  box-shadow:0 var(--lip,4px) 0 0 var(--ui-edge);--lip:4px}}
.ui-btn:active,.ui-btn[data-state=pressed]{{--lip:2px;transform:translateY(2px)}}
.ui-btn--gold{{--bg:var(--ui-gold);--glow:rgba(255,210,63,.6)}}
.ui-btn--hold{{--bg:var(--ui-purple);--glow:rgba(138,79,224,.6);--ink:#fff}}
.ui-btn--video{{--bg:var(--ui-pink);--glow:rgba(255,123,229,.6)}}
/* ثانویه: شکل دیگر (تخت، بُریده، بی‌لب)، رنگ کرم */
.ui-cut{{--cut:10px;--b:3.5px;--cutbg:var(--ui-cream);position:relative;isolation:isolate;border:0;background:#241a5e;box-shadow:none;margin-block-end:0;
  clip-path:polygon(0 0,calc(100% - var(--cut)) 0,100% var(--cut),100% 100%,var(--cut) 100%,0 calc(100% - var(--cut)))}}
.ui-cut::before{{content:"";position:absolute;inset:var(--b);z-index:-1;background:var(--cutbg);
  clip-path:polygon(0 0,calc(100% - var(--cut) + var(--b) * .414) 0,100% calc(var(--cut) - var(--b) * .414),100% 100%,calc(var(--cut) - var(--b) * .414) 100%,0 calc(100% - var(--cut) + var(--b) * .414))}}
.ui-btn--sec{{--cutbg:var(--ui-cream);border:0;margin-block-end:0;border-radius:0;padding:0 24px}}
.ui-btn--sec:active,.ui-btn--sec[data-state=pressed]{{--cutbg:#f0dc8c;transform:none}}
.ui-btn--sec:focus-visible,.ui-btn--sec[data-state=focus]{{outline:0}}
.ui-btn--sec:focus-visible::before,.ui-btn--sec[data-state=focus]::before{{box-shadow:inset 0 0 0 3px var(--ui-chip),inset 0 0 0 5px var(--ui-cream)}}
.ui-btn--s{{min-block-size:44px;padding:0 14px;font-size:18px}}
.ui-btn--s:not(.ui-btn--sec)::after{{content:"";position:absolute;inset-block:-4px;inset-inline:-4px}}
.ui-btn:focus-visible,.ui-chip:focus-visible,.ui-tile:focus-visible{{outline:3px solid var(--ui-cream);outline-offset:2px;box-shadow:0 var(--lip,4px) 0 0 var(--ui-edge),0 0 0 8px var(--ui-chip)}}
.ui-btn:disabled,.ui-btn[aria-disabled=true]{{--bg:var(--ui-disabled-bg);--cutbg:var(--ui-disabled-bg);--ink:var(--ui-ink-disabled);--lip:0px;border-color:#6d6492;box-shadow:none;margin-block-end:0;cursor:default;transform:none;
  background-image:repeating-linear-gradient(135deg,transparent 0 6px,rgba(74,66,104,.18) 6px 8px)}}
/* شب (برگهٔ شب/کارت): مثل pill های کارت v4، خط #190539 و درخشش همرنگ به‌جای لبه */
[data-world=night] .ui-btn:not(.ui-cut){{border-color:{V4['night']};box-shadow:0 0 22px var(--glow);margin-block-end:0;transform:none}}
[data-world=night] .ui-btn:not(.ui-cut):active{{filter:brightness(.92)}}
[data-world=night] .ui-btn.ui-cut{{background:{V4['night']}}}
[data-world=night] .ui-btn:disabled{{box-shadow:none}}
[data-world=night] .ui-btn .ui-svg{{--ui-line:#241a5e;--ui-c3:#4b3b9e}}
/* دکمهٔ آیکونی (v4: دکمهٔ منوی کرم): پایهٔ ۱۲ دندانه، لبهٔ تیره 4px */
.ui-btn--icon{{padding:0;border:0;background:none;box-shadow:none;inline-size:48px;block-size:54px;min-block-size:54px;margin:0;--ui-gear:var(--ui-cream);--ui-gear-lip:var(--ui-edge)}}
[data-world=night] .ui-btn--icon{{box-shadow:none}}
.ui-btn--icon>.ui-gear{{position:absolute;inset:0;inline-size:48px;block-size:54px}}
.ui-btn--icon>.ui-ic{{position:relative;inline-size:32px;block-size:32px;margin-block-end:5px}}
.ui-btn--icon:active,.ui-btn--icon[data-state=pressed]{{--ui-gear:#f0dc8c;transform:none}}
/* نوار بالا (v4): سرمه‌ای #241a5e با لبهٔ موج‌دار و خط زردِ کم‌رنگ؛ منو + سه چیپ */
.ui-topbar{{position:relative;display:flex;align-items:center;gap:var(--ui-gap);padding:8px 9px 18px;background:#241a5e;border-radius:0 0 22px 22px / 0 0 14px 14px;color:var(--ui-cream)}}
.ui-topbar::after{{content:"";position:absolute;inset-inline:0;inset-block-end:5px;block-size:10px;background:{WAVE} repeat-x center/120px 10px}}
.ui-topbar .ui-btn--icon{{flex:none;inline-size:58px;block-size:60px;min-block-size:60px;margin-block-end:4px}}
.ui-topbar .ui-btn--icon>.ui-gear{{inline-size:58px;block-size:60px}}
/* چیپ پایه (v4): 60px بلند؛ «پایه» Vazirmatn 15 بولد + عدد Lalezar 24؛ فعال = زرد با حلقهٔ کرم؛ بقیه = بنفش #4b3b9e */
.ui-chips{{display:flex;gap:var(--ui-gap);direction:rtl;flex:1}}
.ui-chip{{--bg:var(--ui-chip);--ink:var(--ui-cream);--lip:4px;position:relative;flex:1 1 0;min-inline-size:76px;max-inline-size:110px;block-size:60px;box-sizing:border-box;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;
  font-family:var(--ui-font);font-weight:700;line-height:1.1;color:var(--ink);background:var(--bg);border:var(--ui-l35) solid #241a5e;cursor:pointer;padding:0;
  border-radius:16px;box-shadow:0 var(--lip) 0 0 #120c3a}}
.ui-chip small{{font-size:15px;font-weight:700;opacity:1}} .ui-chip b{{font:400 24px/1 var(--ui-font-title);display:block}}
.ui-chip[aria-pressed=true]{{--bg:var(--ui-gold);--ink:#241a5e;--lip:2px;transform:translateY(2px);box-shadow:0 2px 0 #120c3a,0 0 0 3px var(--ui-cream)}}
.ui-chip .ui-tick{{display:none;position:absolute;inset-block-start:-11px;inset-inline-start:-9px;inline-size:22px;block-size:22px}}
.ui-chip[aria-pressed=true] .ui-tick{{display:block}}
.ui-chips-solo .ui-chip{{block-size:60px}}
/* برگه‌ها */
.ui-sheet{{box-sizing:border-box;padding:12px var(--ui-gutter) 20px;background:var(--ui-cream);border:var(--ui-l35) solid #241a5e;border-block-end:0;border-radius:28px 28px 0 0 / 22px 22px 0 0;color:#241a5e;font:400 var(--ui-fs-body)/var(--ui-lh) var(--ui-font)}}
.ui-sheet::before{{content:"";display:block;inline-size:44px;block-size:6px;margin:0 auto 10px;border-radius:3px;background:#241a5e;opacity:.35}}
.ui-sheet h2,.ui-sheet-night h2{{margin:0 0 6px;font:400 var(--ui-fs-sheet)/1.4 var(--ui-font-title)}}
.ui-sheet-night{{box-sizing:border-box;padding:12px var(--ui-gutter) 20px;background:var(--ui-night-bg);color:#fff;border:3px solid var(--ui-cyan);border-block-end:0;border-radius:28px 28px 0 0 / 22px 22px 0 0;box-shadow:0 0 22px rgba(70,240,216,.6);font:400 var(--ui-fs-body)/var(--ui-lh) var(--ui-font)}}
.ui-sheet-night h2{{text-shadow:0 0 14px #ff5ad6}}
.ui-sheet-night::before{{content:"";display:block;inline-size:44px;block-size:6px;margin:0 auto 10px;border-radius:3px;background:var(--ui-cyan);opacity:.8}}
/* پلاک برچسب/«تازه»/ورودی */
.ui-plate{{--cut:7px;--b:2.6px;--cutbg:var(--ui-cream);display:inline-block;padding:2px 14px;min-block-size:28px;box-sizing:border-box;color:#241a5e;font:700 var(--ui-fs-small)/1.6 var(--ui-font)}}
.ui-plate--16{{font-size:16px}}
.ui-newdot{{display:inline-block;inline-size:16px;block-size:16px;border-radius:50%;background:var(--ui-pink);border:var(--ui-l26) solid #241a5e;box-shadow:0 0 0 2px var(--ui-cream)}}
.ui-input{{box-sizing:border-box;min-block-size:48px;padding:0 14px;inline-size:100%;background:#fff;color:#241a5e;border:var(--ui-l26) solid #241a5e;border-radius:3px;font:400 var(--ui-fs-body) var(--ui-font)}}
/* برچسب‌های نقشه (v4): کرم با هالهٔ #241a5e؛ عنوان زمین سفید درشت */
.ui-maplabel{{font:400 20px/1.3 var(--ui-font-title);color:var(--ui-cream);-webkit-text-stroke:6px #241a5e;paint-order:stroke fill;stroke-linejoin:round}}
.ui-zonetitle{{font:400 34px/1.2 var(--ui-font-title);color:#fff;-webkit-text-stroke:9px #241a5e;paint-order:stroke fill;transform:rotate(-3deg);display:inline-block}}
/* برچسب «اینجایی» (v4): تگ زرد با نشانگر پایین */
.ui-heretag{{position:relative;display:inline-block;padding:6px 18px 8px;background:var(--ui-gold);border:4px solid #241a5e;border-radius:14px;color:#241a5e;font:400 23px/1.2 var(--ui-font-title);margin-block-end:14px}}
.ui-heretag::after{{content:"";position:absolute;inset-inline-start:50%;inset-block-end:-16px;margin-inline-start:-10px;inline-size:0;block-size:0;border-inline:10px solid transparent;border-block-start:14px solid #241a5e}}
.ui-heretag::before{{content:"";position:absolute;inset-inline-start:50%;inset-block-end:-9px;margin-inline-start:-6px;inline-size:0;block-size:0;border-inline:6px solid transparent;border-block-start:9px solid var(--ui-gold);z-index:1}}
/* کاشی منو: هر کاشی رنگ خودش (فیروزه‌ای، بنفش، زرد، صورتی)؛ بنا را env می‌دهد */
.ui-tile{{--lip:4px;--bg:var(--ui-cyan);--ink:#241a5e;position:relative;box-sizing:border-box;inline-size:160px;min-block-size:132px;margin-block-end:4px;padding:0 8px 10px;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;
  background:var(--bg);border:var(--ui-l35) solid #241a5e;color:var(--ink);font:400 var(--ui-fs-tile)/1.3 var(--ui-font-title);cursor:pointer;
  border-start-start-radius:var(--ui-r-big);border-end-end-radius:var(--ui-r-big);border-start-end-radius:var(--ui-r-small);border-end-start-radius:var(--ui-r-small);
  box-shadow:0 var(--lip) 0 0 #120c3a}}
.ui-tile--violet{{--bg:var(--ui-chip);--ink:var(--ui-cream)}} .ui-tile--gold{{--bg:var(--ui-gold)}} .ui-tile--pink{{--bg:var(--ui-pink)}}
.ui-tile .ui-tile-art{{position:absolute;inset-block-start:-12px;inset-inline:0;margin:auto;inline-size:100px;block-size:84px}}
.ui-tile:active{{--lip:2px}}
.ui-sr{{position:absolute;inline-size:1px;block-size:1px;overflow:hidden;clip:rect(0 0 0 0)}}
@media (prefers-reduced-motion:reduce){{.ui-btn,.ui-chip,.ui-tile{{transition:none!important;animation:none!important}}.ui-ring-dash{{animation:none}}}}
'''
(OUT / 'ui_tokens.css').write_text(CSS, encoding='utf-8')

# ---------- ui_kit.html ----------
def use(i, cls='ui-svg', label=None):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#{i}"/></svg>'
FONTS = '../../../../../../../../assets/fonts'
icon_cells = ''.join(f'<figure><div class="ic">{use("ui-ic-"+k)}</div><figcaption dir="ltr">{k}</figcaption></figure>' for k in ICONS)
small_cells = ''.join(f'<span class="ic">{use("ui-ic-"+k,"ui-svg ui-svg--32")}</span>' for k in ICONS)
def chip(k, on): return (f'<button class="ui-chip" aria-pressed="{str(on).lower()}"><svg class="ui-tick" aria-hidden="true"><use href="#ui-check"/></svg>'
                        f'<small>{t("v5.ui.base.label")}</small><b><bdi dir="rtl">{t("v5.ui.base."+k)}</bdi></b></button>')
def hard(k): return f'<span class="ui-hard">{use("ui-badge-"+k,"ui-badge")}<span>{t("difficulty."+k)}</span></span>'
badges_row = ''.join(hard(k) for k in ('easy', 'mid', 'hard'))
ZN = {'grass': '#3f9a2b', 'sea': '#075a73', 'farm': '#9a8a10', 'space': '#c4502f'}
badge_on_zone = ''.join(f'<div class="zn" style="background:{c}">' + ''.join(use('ui-badge-' + k, 'ui-badge') for k in ('easy', 'mid', 'hard')) + '</div>' for z, c in ZN.items())
rings = ''.join(f'<div class="zn" style="background:{c};{"--ui-ring-ol:14px;" if z=="farm" else ""}"><svg class="ui-ring" width="96" height="96" viewBox="0 0 100 100"><use href="#ui-ring"/></svg></div>' for z, c in ZN.items())
lockrow = f'<div class="row">{use("ui-lock","ui-lockbadge")}<span class="ui-plate ui-cut ui-plate--16">{t("flow.lock.reason", name=t("flow.menu.map"))}</span></div>'
css_kit = '''
@font-face{font-family:Vazirmatn;font-weight:400;src:url(%s/Vazirmatn-Regular.woff2)}
@font-face{font-family:Vazirmatn;font-weight:700;src:url(%s/Vazirmatn-Bold.woff2)}
@font-face{font-family:Lalezar;src:url(%s/Lalezar-Regular.woff2)}
html{background:#f1e2a0}body{margin:0;font:400 16px/1.7 Vazirmatn,sans-serif;color:#241a5e;background:#f1e2a0}
main{max-width:430px;margin:0 auto;padding:0 16px 40px}
h1{font:400 28px/1.4 Lalezar,Vazirmatn;margin:14px 0 4px}h3{font:400 24px/1.4 Lalezar,Vazirmatn;margin:26px 0 8px;border-block-end:3px solid #241a5e;display:inline-block;padding-inline-end:12px}
.row{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:8px 0}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}figure{margin:0;text-align:center}.ic{display:inline-flex;background:#fff8dc;border-radius:10px;padding:0;border:2px solid #241a5e}
figcaption{font-size:14px}.night{background:#190539;color:#fff;border-radius:12px;padding:12px;margin:8px 0}
.zn{display:flex;align-items:center;justify-content:center;gap:2px;inline-size:100px;min-inline-size:100px;block-size:100px;border-radius:12px;border:3px solid #241a5e;flex-direction:column}.zn .ui-badge{margin:2px 0;transform:scale(.8)}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:20px 10px;margin-block-start:22px}.tiles .ui-tile{inline-size:100%%}
.tiles .ui-svg{inline-size:64px;block-size:64px;margin-block-end:6px}
.sheets{display:grid;gap:14px}.sz{font-size:14px;color:#241a5e}
.topbar-wrap{margin:0 -16px}
''' % (FONTS, FONTS, FONTS)
def btnrow(label_key, night=False):
    lab = t(label_key)
    return (f'<div class="row"><button class="ui-btn">{lab}</button><button class="ui-btn ui-btn--sec ui-cut">{lab}</button>'
            f'<button class="ui-btn ui-btn--gold">{t("flow.box.put")}</button>'
            f'<button class="ui-btn ui-btn--hold">{lab}</button><button class="ui-btn ui-btn--video">{t("v5.ui.state.video")}</button><button class="ui-btn" data-state="pressed">{t("v5.ui.state.pressed")}</button>'
            f'<button class="ui-btn" disabled>{t("v5.ui.state.disabled")}</button><button class="ui-btn ui-btn--sec ui-cut" data-state="focus" style="outline:3px solid #fff3c4;outline-offset:2px;box-shadow:0 0 0 8px #4b3b9e">{t("v5.ui.state.focus")}</button>'
            f'<button class="ui-btn ui-btn--s">{t("v5.ui.state.compact")}</button></div>')
def iconbtn(ic, lk, st=''): return f'<button class="ui-btn ui-btn--icon" {st} aria-label="{t(lk)}"><svg class="ui-gear" aria-hidden="true"><use href="#ui-gearbtn"/></svg><svg class="ui-ic" aria-hidden="true"><use href="#ui-ic-{ic}"/></svg></button>'
icon_btns = ''.join(iconbtn(ic, lk) for ic, lk in (('menu', 'flow.menu.open'), ('close', 'flow.menu.back'), ('search', 'v5.ui.state.search')))
back_btn = f'<button class="ui-btn ui-btn--sec ui-cut">{use("ui-ic-next","ui-svg ui-svg--32 ui-flip")}{t("flow.menu.back")}</button>'
tiles = ''.join(f'<button class="ui-tile {c}"><span class="ui-tile-art">{use("ui-ic-"+ic,"ui-svg")}</span>{t(k)}</button>' for c, ic, k in
                (('', 'map', 'flow.menu.map'), ('ui-tile--violet', 'cards', 'flow.menu.cards'), ('ui-tile--gold', 'practice', 'flow.menu.practice'), ('ui-tile--pink', 'guide', 'flow.menu.guide')))
tiles = tiles.replace('<span class="ui-tile-art"><svg class="ui-svg">', '<span class="ui-tile-art" style="display:flex;justify-content:center;align-items:center"><svg class="ui-svg">')
html = f'''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t("v5.ui.kit.title")}</title><style>{CSS}
{css_kit}</style></head><body><div style="position:absolute;width:0;height:0;overflow:hidden">{SPRITE}</div><main>
<div class="topbar-wrap"><div class="ui-topbar">{iconbtn("menu", "flow.menu.open")}
<div class="ui-chips">{chip("b12", False)}{chip("b34", True)}{chip("b56", False)}</div></div></div>
<h1>{t("v5.ui.kit.title")}</h1>
<h3>{t("v5.ui.kit.s_buttons")}</h3>{btnrow("flow.menu.back")}<div class="row">{icon_btns}{back_btn}</div>
<div class="night" data-world="night"><div class="row"><button class="ui-btn">{t("flow.menu.practice")}</button><button class="ui-btn ui-btn--video">{t("v5.ui.state.video")}</button><button class="ui-btn ui-btn--gold">{t("flow.menu.cards")}</button><button class="ui-btn ui-btn--sec ui-cut">{t("flow.menu.back")}</button><button class="ui-btn ui-btn--hold">{t("flow.menu.adults")}</button></div></div>
<h3>{t("v5.ui.kit.s_base")}</h3><div class="ui-chips" style="margin:8px 0">{chip("b12", True)}{chip("b34", False)}{chip("b56", False)}</div>
<div class="tiles">{tiles}</div>
<h3>{t("v5.ui.kit.s_icons")}</h3><div class="grid">{icon_cells}</div><div class="row">{small_cells}</div>
<h3>{t("v5.ui.kit.s_badges")}</h3><div class="row">{badges_row}</div><div class="row">{badge_on_zone}</div>
<div class="night" data-world="night"><div class="row">{badges_row}</div></div>
<h3>{t("v5.ui.kit.s_lock")}</h3>{lockrow}<div class="row"><span class="ui-newdot"></span><span class="ui-plate ui-cut">{t("flow.map.here")}</span><span class="ui-heretag">{t("flow.map.here")}</span></div>
<div class="row" style="background:#3f9a2b;border-radius:12px;padding:10px;border:3px solid #241a5e"><span class="ui-maplabel">{t("flow.menu.map")}</span><span class="ui-zonetitle">{t("flow.menu.practice")}</span></div>
<h3>{t("v5.ui.kit.s_ring")}</h3><div class="row">{rings}</div>
<h3>{t("v5.ui.kit.s_sheets")}</h3><div class="sheets"><div class="ui-sheet"><h2>{t("flow.menu.adults")}</h2><p style="margin:0 0 10px">{t("flow.lock.reason", name=t("flow.menu.cards"))}</p><div class="row"><button class="ui-btn">{t("flow.lock.go")}</button><button class="ui-btn ui-btn--sec ui-cut">{t("flow.menu.back")}</button></div></div>
<div class="ui-sheet-night" data-world="night"><h2>{t("flow.menu.cards")}</h2><p style="margin:0 0 10px">{t("flow.lock.reason", name=t("flow.menu.practice"))}</p><div class="row"><button class="ui-btn">{t("flow.lock.go")}</button><button class="ui-btn ui-btn--sec ui-cut">{t("flow.menu.back")}</button></div></div></div>
<h3>{t("v5.ui.kit.s_type")}</h3><div class="sz" style="font:400 28px/1.4 Lalezar">{t("flow.menu.map")} 28</div><div class="sz" style="font:400 24px/1.4 Lalezar">{t("flow.menu.cards")} 24</div><div class="sz" style="font:400 22px/1.4 Lalezar">{t("flow.menu.practice")} 22</div>
<div class="sz" style="font:700 18px/1.7 Vazirmatn">{t("flow.menu.guide")} 18</div><div class="sz" style="font:700 16px/1.7 Vazirmatn">{t("flow.menu.back")} 16</div><div class="sz" style="font:400 16px/1.7 Vazirmatn">{t("flow.menu.adults")} 16</div><div class="sz" style="font:700 14px/1.7 Vazirmatn">{t("flow.map.here")} 14</div>
</main></body></html>'''
(OUT / 'ui_kit.html').write_text(html, encoding='utf-8')
print('ok', len(SPRITE), 'bytes sprite;', len(ICONS), 'icons')
