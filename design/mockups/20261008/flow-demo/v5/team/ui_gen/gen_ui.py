#!/usr/bin/env python3
"""مولد دارایی‌های رابط v5 (ui-artist، گام ۲). اجرا:  python3 gen_ui.py
خروجی در ../assets/ui/: sprite_ui.svg، assets.json، ui_tokens.css، ui_kit.html.
متن فقط با کلید از v5/strings.fa.json و ../strings.fa.json (flow). رنگ‌ها از light/zone_tokens.json."""
import json, math, pathlib, re
HERE = pathlib.Path(__file__).resolve().parent
V5 = HERE.parents[1]
OUT = HERE.parent / 'assets' / 'ui'
Z = json.load(open(HERE.parent / 'assets/light/zone_tokens.json', encoding='utf-8'))
S = {}
S.update(json.load(open(V5.parent / 'strings.fa.json', encoding='utf-8')))
S.update(json.load(open(V5 / 'strings.fa.json', encoding='utf-8')))
def t(k, **kw): return S[k]['text'].format(**kw)
U = Z['ui']; H = Z['hardness']
LINE = 'var(--ui-line,%s)' % U['line']
C1, C2, C3, C4, C5 = ('var(--ui-c1,%s)' % U['cream'], 'var(--ui-c2,%s)' % U['teal'], 'var(--ui-c3,%s)' % U['deep_violet'],
                      'var(--ui-c4,%s)' % U['pink'], 'var(--ui-c5,#ffffff)')
def P(d, fill, w=2.6, extra=''):
    return f'<path d="{d}" style="fill:{fill};stroke:{LINE};stroke-width:{w};stroke-linejoin:round;stroke-linecap:round"{extra}/>'
def R(x, y, w, h, r, fill, sw=2.6, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" style="fill:{fill};stroke:{LINE};stroke-width:{sw};stroke-linejoin:round"{extra}/>'
def Ci(cx, cy, r, fill, sw=2.6):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" style="fill:{fill};stroke:{LINE};stroke-width:{sw}"/>'
def L(d, w=2.6, col=None):
    return f'<path d="{d}" style="fill:none;stroke:{col or LINE};stroke-width:{w};stroke-linecap:round;stroke-linejoin:round"/>'
def gear(cx, cy, ro, ri, n, tw=6, vw=10):
    pts = []
    for i in range(n):
        a = 360 / n * i
        for da, r in ((-vw, ri), (-tw, ro), (tw, ro), (vw, ri)):
            ang = math.radians(a + da - 90)
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + 'Z'

# ---------- ۲۰ آیکون (شبکهٔ 48، خط 2.6) ----------
ICONS = {}
ICONS['menu'] = ''.join(R(8, y, 32, 7, 3.5, C1) for y in (10, 20.5, 31))
ICONS['next'] = P('M7 24 L21 10 L21 18 L41 18 L41 30 L21 30 L21 38Z', C2)      # رو به انتهای خط (فیزیکی: چپ)؛ «برگرد» = scaleX(-1)
ICONS['close'] = P('M11 17 L17 11 L24 18 L31 11 L37 17 L30 24 L37 31 L31 37 L24 30 L17 37 L11 31 L18 24Z', C4)
ICONS['map'] = P('M6 12 L17 8 L31 12 L42 8 L42 36 L31 40 L17 36 L6 40Z', C1) + L('M17 8 V36 M31 12 V40') + Ci(30, 21, 5, C2)
ICONS['cards'] = R(9, 10, 22, 30, 4, C3, extra=' transform="rotate(-12 20 25)"') + R(17, 8, 22, 30, 4, C1, extra=' transform="rotate(9 28 23)"') + P('M28 17 L33 24 L28 31 L23 24Z', C2, 2.2, ' transform="rotate(9 28 23)"')
ICONS['practice'] = R(5, 21, 38, 20, 3, C2) + R(4, 13, 40, 9, 3, C1) + R(17, 28, 14, 6, 2, C1, 2.2) + P('M13 13 L16 6 L28 6 L31 13', C5, 2.2)
ICONS['guide'] = P('M9 31 Q9 11 24 11 Q39 11 39 31Z', C1) + P('M5 31 H43 V36 H5Z', C3) + P('M20 11 V31 M28 11 V31', C1, 2.2).replace('fill:' + C1, 'fill:none') + R(19, 6, 10, 6, 2, C2, 2.2)
ICONS['search'] = Ci(20, 20, 12, C1) + f'<rect x="27.5" y="31.5" width="17" height="8" rx="4" transform="rotate(45 36 35.5)" style="fill:{C3};stroke:{LINE};stroke-width:2.6"/>' + L('M14 16 Q16 12 21 12', 2.2, C5)
ICONS['lock'] = f'<path d="M15 22 V16 a9 9 0 0 1 18 0 V22" style="fill:none;stroke:{LINE};stroke-width:8.2;stroke-linecap:round"/><path d="M15 22 V16 a9 9 0 0 1 18 0 V22" style="fill:none;stroke:{C1};stroke-width:3;stroke-linecap:round"/>' + R(9, 21, 30, 21, 5, C1) + Ci(24, 30, 3.4, C3, 2.2) + R(22.6, 31, 2.8, 6, 1.4, C3, 2)
ICONS['eye'] = P('M3 24 Q24 5 45 24 Q24 43 3 24Z', C5) + Ci(24, 24, 8.5, C2) + Ci(24, 24, 3.2, LINE, 1)
ICONS['box'] = P('M24 5 L42 13 L42 34 L24 43 L6 34 L6 13Z', C3) + P('M24 5 L42 13 L24 22 L6 13Z', C1) + L('M24 22 V43')
ICONS['mypos'] = P('M24 5 L39 41 L24 33 L9 41Z', C2)
ICONS['pin'] = P('M24 44 C14 31 9 25 9 18 a15 15 0 0 1 30 0 c0 7 -5 13 -15 26Z', C1) + Ci(24, 18, 6, C2)
ICONS['flag'] = R(9, 5, 5, 38, 2.5, C1) + P('M14 8 L40 14 L14 22Z', C5) + f'<path d="M20 9.5 L26 11 L24 15.5 L18 14Z M31 12.5 L37 14 L30 17.2Z" style="fill:{LINE}"/>'
ICONS['game'] = P(gear(24, 24, 21, 16.5, 8, 7, 11), C2) + Ci(24, 24, 6.5, C1)
ICONS['flip'] = '<path d="M37 24 a13 13 0 1 1 -4 -9.3" style="fill:none;stroke:%s;stroke-width:8.2;stroke-linecap:round"/><path d="M37 24 a13 13 0 1 1 -4 -9.3" style="fill:none;stroke:%s;stroke-width:3;stroke-linecap:round"/>' % (LINE, C2) + P('M31 5 L42 15 L28 19Z', C2)
ICONS['lesson'] = P('M24 12 Q14 7 5 10 V38 Q14 35 24 40Z', C1) + P('M24 12 Q34 7 43 10 V38 Q34 35 24 40Z', C1) + P('M32 8 V22 L35.5 19 L39 22 V9', C2, 2.2) + L('M10 17 Q16 16 20 18 M10 24 Q16 23 20 25', 2)
ICONS['hint'] = P('M24 5 a13 13 0 0 1 8 23 V32 H16 V28 A13 13 0 0 1 24 5Z', C1) + R(16, 32, 16, 9, 3, C3) + L('M20 36.5 H28', 2, C1) + L('M17 15 Q19 11 23 11', 2.2, C5)
ICONS['hold'] = Ci(24, 24, 19, C1) + '<path d="M24 11 A13 13 0 1 1 11 24" style="fill:none;stroke:%s;stroke-width:6;stroke-linecap:round"/>' % C2 + Ci(24, 24, 4.5, C3, 2.2)
ICONS['skip'] = P('M38 9 L16 24 L38 39Z', C1) + R(7, 9, 7, 30, 2.5, C1)

def sym(i, vb, body, extra=''):
    return f'<symbol id="{i}" viewBox="{vb}" style="stroke-linejoin:round;stroke-linecap:round{extra}">{body}</symbol>'
syms = [sym('ui-ic-' + k, '0 0 48 48', v) for k, v in ICONS.items()]

# ---------- قرص سختی 56×30 ----------
def badge(level):
    hx, n = H[level]['hex'], H[level]['peaks']
    w, g = 12, 3.2
    tot = n * w + (n - 1) * g
    x0 = (56 - tot) / 2
    peaks = ''.join(f'<path d="M{x0+i*(w+g):.1f} 22.5 L{x0+i*(w+g)+w/2:.1f} 8.5 L{x0+i*(w+g)+w:.1f} 22.5Z" '
                    f'style="fill:{C1};stroke:{LINE};stroke-width:1.2;stroke-linejoin:round"/>' for i in range(n))
    # حاشیهٔ کرم فقط وقتی --ui-rim>0 (کارت شب)؛ خط دور روز #0d0426 (توصیهٔ light)
    rim = f'<rect x="1.3" y="1.3" width="53.4" height="27.4" rx="13.7" style="fill:none;stroke:{C1};stroke-width:calc(2.6px + 2 * var(--ui-rim,0px))"/>'
    pill = f'<rect x="1.3" y="1.3" width="53.4" height="27.4" rx="13.7" style="fill:{hx};stroke:var(--ui-badge-line,{U["badge_line_day"]});stroke-width:2.6"/>'
    return sym(f'ui-badge-{level}', '0 0 56 30', rim + pill + peaks, ';overflow:visible')
syms += [badge(k) for k in ('easy', 'mid', 'hard')]
# قفل 32px
syms.append(sym('ui-lock', '0 0 32 32',
    f'<circle cx="16" cy="16" r="14.7" style="fill:{C3};stroke:{LINE};stroke-width:2.6"/>'
    f'<path d="M11.5 15 V12.5 a4.5 4.5 0 0 1 9 0 V15" style="fill:none;stroke:{C1};stroke-width:2.4;stroke-linecap:round"/>'
    f'<rect x="9.5" y="14.5" width="13" height="9.5" rx="2.6" style="fill:{C1}"/><circle cx="16" cy="19" r="1.7" style="fill:{C3}"/>'))
# حلقهٔ اینجایی: باند زرد ۸؛ خط دور بیرونی پیش‌فرض 4.5px (مزرعه 10px با --ui-ring-ol) به سمت بیرون ضخیم می‌شود؛ خط درونی ثابت 4.5
syms.append(sym('ui-ring', '0 0 100 100',
    f'<circle cx="50" cy="50" r="42" style="fill:none;stroke:var(--ui-ring,{U["accent_yellow"]});stroke-width:8"/>'
    f'<circle cx="50" cy="50" style="r:calc(43.75px + var(--ui-ring-ol,4.5px) / 2);fill:none;stroke:{LINE};stroke-width:var(--ui-ring-ol,4.5px)"/>'
    f'<circle cx="50" cy="50" r="38" style="fill:none;stroke:{LINE};stroke-width:4.5"/>', ';overflow:visible'))
# تیک چیپ
syms.append(sym('ui-check', '0 0 20 20',
    f'<circle cx="10" cy="10" r="8.7" style="fill:{C2};stroke:{LINE};stroke-width:2.6"/>'
    f'<path d="M5.8 10.3 L8.6 13 L14.2 7" style="fill:none;stroke:{LINE};stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round"/>'))
# پایهٔ دکمهٔ آیکونی (دایرهٔ ۱۲ دندانه، شعاع 22.5/20.5، خط 4.5)
GEAR = gear(24, 24, 21.4, 19.2, 12, 6.5, 10.5)
syms.append(sym('ui-gearbtn', '0 0 48 54',
    f'<path d="{GEAR}" transform="translate(0 var(--ui-lipy,6))" style="fill:var(--ui-lip,#6a5aa8);stroke:{LINE};stroke-width:4.5"/>'.replace('translate(0 var(--ui-lipy,6))', 'translate(0 6)') +
    f'<path d="{GEAR}" style="fill:var(--ui-gear,{U["cream"]});stroke:{LINE};stroke-width:4.5"/>'))
SPRITE = '<svg xmlns="http://www.w3.org/2000/svg">' + '\n'.join(syms) + '</svg>'
(OUT / 'sprite_ui.svg').write_text(SPRITE, encoding='utf-8')

# ---------- assets.json ----------
A = {f'ui-ic-{k}': {'viewBox': '0 0 48 48', 'grid': 48, 'stroke': 2.6, 'role': 'icon'} for k in ICONS}
A.update({'ui-badge-easy': {'viewBox': '0 0 56 30', 'peaks': 1, 'word_key': 'difficulty.easy', 'role': 'hardness'},
          'ui-badge-mid': {'viewBox': '0 0 56 30', 'peaks': 2, 'word_key': 'difficulty.mid', 'role': 'hardness'},
          'ui-badge-hard': {'viewBox': '0 0 56 30', 'peaks': 3, 'word_key': 'difficulty.hard', 'role': 'hardness'},
          'ui-lock': {'viewBox': '0 0 32 32', 'role': 'lock'}, 'ui-ring': {'viewBox': '0 0 100 100', 'vars': ['--ui-ring-ol', '--ui-ring'], 'role': 'here-ring'},
          'ui-check': {'viewBox': '0 0 20 20', 'role': 'chip-tick'}, 'ui-gearbtn': {'viewBox': '0 0 48 54', 'vars': ['--ui-gear', '--ui-lip'], 'role': 'icon-button-base'}})
json.dump({'sprite': 'sprite_ui.svg', 'arrow_convention': 'ui-ic-next رو به انتهای خط (فیزیکی چپ)؛ «برگرد» = همان با class ui-flip', 'assets': A},
          open(OUT / 'assets.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------- ui_tokens.css ----------
CSS = f'''/* ui_tokens.css (ui-artist v5). مشخصات CSS دکمه/چیپ/برگه/پلاک؛ رنگ‌ها از light/tokens.css (این فایل پس از آن بیاید).
   خط: L4.5 دکمه/چیپ/کاشی/برگه، L2.6 پلاک/ورودی/آیکون/قرص، L1.2 تزئین. نور بالا-چپ؛ فشردن = لبه 6←2 بدون جابه‌جایی. بدون filter/blend. */
:root{{
  --ui-line:{U['line']}; --ui-cream:{U['cream']}; --ui-violet:{U['deep_violet']}; --ui-teal:{U['teal']}; --ui-pink:{U['pink']}; --ui-danger:{U['danger_violet']};
  --ui-night-bg:{U['card_bg']}; --ui-night-edge:{U['teal']};
  --ui-ink-disabled:#4a4268; --ui-disabled-bg:#d9d3e8;
  --ui-r-big:18px; --ui-r-small:7px; --ui-l45:4.5px; --ui-l26:2.6px; --ui-l12:1.2px; --ui-lip:6px; --ui-lip-pressed:2px;
  --ui-touch:48px; --ui-gap:8px; --ui-gutter:16px;
  --ui-font-title:'Lalezar','Vazirmatn',sans-serif; --ui-font:'Vazirmatn',system-ui,sans-serif;
  --ui-fs-page:28px; --ui-fs-zone:24px; --ui-fs-sheet:22px; --ui-fs-tile:18px; --ui-fs-btn:16px; --ui-fs-body:16px; --ui-fs-small:14px; --ui-lh:1.7;
}}
.ui-svg{{display:inline-block;inline-size:48px;block-size:48px;flex:none}}
.ui-svg--40{{inline-size:40px;block-size:40px}} .ui-svg--32{{inline-size:32px;block-size:32px}}
.ui-flip{{transform:scaleX(-1)}}
.ui-badge{{display:inline-block;inline-size:56px;block-size:30px;overflow:visible;flex:none}}
.ui-lockbadge{{display:inline-block;inline-size:32px;block-size:32px;flex:none}}
.ui-ring{{overflow:visible}}
[data-world=night]{{--ui-rim:2px;--ui-badge-line:var(--ui-line)}}
/* دکمه («پلاک ماشینی»): گوشهٔ بزرگ بالا-ابتدای خط با ویژگی‌های منطقی */
.ui-btn{{--bg:var(--ui-teal);--lipc:#1f8a7d;--ink:var(--ui-line);position:relative;display:inline-flex;align-items:center;justify-content:center;gap:8px;
  min-block-size:var(--ui-touch);min-inline-size:var(--ui-touch);padding:0 20px;margin-block-end:var(--ui-lip);box-sizing:border-box;
  font:700 var(--ui-fs-btn)/1.2 var(--ui-font);color:var(--ink);background:var(--bg);border:var(--ui-l45) solid var(--ui-line);cursor:pointer;
  border-start-start-radius:var(--ui-r-big);border-end-end-radius:var(--ui-r-big);border-start-end-radius:var(--ui-r-small);border-end-start-radius:var(--ui-r-small);
  box-shadow:0 var(--lip,6px) 0 0 var(--lipc),0 var(--lip,6px) 0 var(--ui-l45) var(--ui-line);--lip:6px}}
.ui-btn:active,.ui-btn[data-state=pressed]{{--lip:2px}}
.ui-btn--sec{{--bg:var(--ui-cream);--lipc:#cdbf93;border-width:var(--ui-l26)}}
.ui-btn--hold{{--bg:var(--ui-danger);--lipc:#5f2f99;--ink:#fff}}
.ui-btn--video{{--bg:#d9608f;--lipc:#a43a64}}
.ui-btn--s{{min-block-size:40px;padding:0 14px}}
.ui-btn--s::after{{content:"";position:absolute;inset-block:-4px;inset-inline:-4px}}
.ui-btn:focus-visible,.ui-chip:focus-visible,.ui-tile:focus-visible{{outline:3px solid var(--ui-cream);outline-offset:2px;box-shadow:0 var(--lip,6px) 0 0 var(--lipc),0 var(--lip,6px) 0 var(--ui-l45) var(--ui-line),0 0 0 8px var(--ui-violet)}}
.ui-btn:disabled,.ui-btn[aria-disabled=true]{{--bg:var(--ui-disabled-bg);--ink:var(--ui-ink-disabled);--lip:0px;border-color:#6d6492;box-shadow:none;margin-block-end:0;cursor:default;
  background-image:repeating-linear-gradient(135deg,transparent 0 6px,rgba(74,66,104,.18) 6px 8px)}}
/* دکمهٔ آیکونی: پایهٔ دایرهٔ ۱۲ دندانه از sprite (ui-gearbtn)، آیکون ۴۰ روی آن؛ فشردن = تغییر رنگ، بدون جابه‌جایی */
.ui-btn--icon{{padding:0;border:0;background:none;box-shadow:none;inline-size:48px;block-size:54px;min-block-size:54px;margin:0;--ui-gear:var(--ui-cream)}}
.ui-btn--icon>.ui-gear{{position:absolute;inset:0;inline-size:48px;block-size:54px}}
.ui-btn--icon>.ui-ic{{position:relative;inline-size:32px;block-size:32px;margin-block-end:6px}}
.ui-btn--icon:active{{--ui-gear:#e6d9a8;--ui-lip:#6a5aa8}}
/* چیپ پایه: 96×48، دو سطر «پایه» 14 و «۱ تا ۲» 18 بولد */
.ui-chips{{display:flex;gap:var(--ui-gap);direction:rtl}}
.ui-chip{{--bg:var(--ui-violet);--ink:#fff;--lip:2px;--lipc:#2a1f5c;position:relative;flex:1 1 0;min-inline-size:76px;max-inline-size:96px;block-size:48px;margin-block-end:6px;box-sizing:border-box;display:flex;flex-direction:column;align-items:center;justify-content:center;
  font-family:var(--ui-font);font-weight:700;line-height:1;color:var(--ink);background:var(--bg);border:var(--ui-l26) solid var(--ui-line);cursor:pointer;padding:0;
  border-start-start-radius:var(--ui-r-big);border-end-end-radius:var(--ui-r-big);border-start-end-radius:var(--ui-r-small);border-end-start-radius:var(--ui-r-small);
  box-shadow:0 var(--lip) 0 0 var(--lipc),0 var(--lip) 0 var(--ui-l26) var(--ui-line)}}
.ui-chip small{{font-size:var(--ui-fs-small);font-weight:700;opacity:1}} .ui-chip b{{font-size:18px}}
.ui-chip[aria-pressed=true]{{--bg:var(--ui-cream);--ink:var(--ui-line);--lip:6px;--lipc:#cdbf93;border-width:var(--ui-l45)}}
.ui-chip .ui-tick{{display:none;position:absolute;inset-block-start:-9px;inset-inline-start:-8px;inline-size:20px;block-size:20px}}
.ui-chip[aria-pressed=true] .ui-tick{{display:block}}
/* برگه‌ها */
.ui-sheet{{box-sizing:border-box;padding:12px var(--ui-gutter) 20px;background:var(--ui-cream);border:var(--ui-l45) solid var(--ui-line);border-block-end:0;border-radius:28px 28px 0 0 / 22px 22px 0 0;color:var(--ui-line);font:400 var(--ui-fs-body)/var(--ui-lh) var(--ui-font)}}
.ui-sheet::before{{content:"";display:block;inline-size:44px;block-size:6px;margin:0 auto 10px;border-radius:3px;background:var(--ui-line);opacity:.35}}
.ui-sheet h2,.ui-sheet-night h2{{margin:0 0 6px;font:400 var(--ui-fs-sheet)/1.4 var(--ui-font-title)}}
.ui-sheet-night{{box-sizing:border-box;padding:12px var(--ui-gutter) 20px;background:var(--ui-night-bg);color:#fff;border:var(--ui-l26) solid var(--ui-night-edge);border-block-end:0;border-radius:28px 28px 0 0 / 22px 22px 0 0;box-shadow:0 0 14px rgba(47,184,168,.45);font:400 var(--ui-fs-body)/var(--ui-lh) var(--ui-font)}}
.ui-sheet-night::before{{content:"";display:block;inline-size:44px;block-size:6px;margin:0 auto 10px;border-radius:3px;background:var(--ui-night-edge);opacity:.7}}
/* پلاک برچسب، «تازه»، ورودی */
.ui-plate{{display:inline-block;padding:2px 12px;min-block-size:28px;box-sizing:border-box;background:var(--ui-cream);color:var(--ui-line);border:var(--ui-l26) solid var(--ui-line);border-radius:10px 4px 10px 4px;font:700 var(--ui-fs-small)/1.6 var(--ui-font)}}
.ui-plate--16{{font-size:16px}}
.ui-newdot{{display:inline-block;inline-size:16px;block-size:16px;border-radius:50%;background:var(--ui-teal);border:var(--ui-l26) solid var(--ui-line);box-shadow:0 0 0 2px var(--ui-cream)}}
.ui-input{{box-sizing:border-box;min-block-size:48px;padding:0 14px;inline-size:100%;background:#fff;color:var(--ui-line);border:var(--ui-l26) solid var(--ui-line);border-radius:12px 5px 12px 5px;font:400 var(--ui-fs-body) var(--ui-font)}}
/* کاشی منو: ≥132 بلند، 160 عرض؛ بنا را env می‌دهد (img/svg داخل .ui-tile-art) و ۱۲px از لبهٔ بالا بیرون می‌زند */
.ui-tile{{--lip:6px;--lipc:#8fb7d9;--bg:#d6ecf7;position:relative;box-sizing:border-box;inline-size:160px;min-block-size:132px;margin-block-end:6px;padding:0 8px 10px;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;
  background:var(--bg);border:var(--ui-l45) solid var(--ui-line);color:var(--ui-line);font:700 var(--ui-fs-tile)/1.3 var(--ui-font);cursor:pointer;
  border-start-start-radius:var(--ui-r-big);border-end-end-radius:var(--ui-r-big);border-start-end-radius:var(--ui-r-small);border-end-start-radius:var(--ui-r-small);
  box-shadow:0 var(--lip) 0 0 var(--lipc),0 var(--lip) 0 var(--ui-l45) var(--ui-line)}}
.ui-tile .ui-tile-art{{position:absolute;inset-block-start:-12px;inset-inline:0;margin:auto;inline-size:100px;block-size:84px}}
.ui-tile:active{{--lip:2px}}
.ui-sr{{position:absolute;inline-size:1px;block-size:1px;overflow:hidden;clip:rect(0 0 0 0)}}
@media (prefers-reduced-motion:reduce){{.ui-btn,.ui-chip,.ui-tile{{transition:none!important;animation:none!important}}}}
'''
(OUT / 'ui_tokens.css').write_text(CSS, encoding='utf-8')

# ---------- ui_kit.html ----------
def use(i, cls='ui-svg', label=None):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#{i}"/></svg>'
FONTS = '../../../../../../../../assets/fonts'
tokens_light = (HERE.parent / 'assets/light/tokens.css').read_text(encoding='utf-8')
zones = {'sports': 'zone_sports', 'space': 'zone_space', 'farm': 'zone_farm', 'city': 'zone_city'}
icon_cells = ''.join(f'<figure><div class="ic">{use("ui-ic-"+k)}</div><figcaption dir="ltr">{k}</figcaption></figure>' for k in ICONS)
small_cells = ''.join(f'<span class="ic">{use("ui-ic-"+k,"ui-svg ui-svg--32")}</span>' for k in ICONS)
def chip(k, on): return (f'<button class="ui-chip" aria-pressed="{str(on).lower()}"><svg class="ui-tick" aria-hidden="true"><use href="#ui-check"/></svg>'
                        f'<small>{t("v5.ui.base.label")}</small><b><bdi dir="rtl">{t("v5.ui.base."+k)}</bdi></b></button>')
badges_day = ''.join(f'<div class="bd">{use("ui-badge-"+k,"ui-badge")}<span>{t("difficulty."+k)}</span></div>' for k in ('easy', 'mid', 'hard'))
rings = ''.join(f'<div class="zn" style="background:var(--z-{z}-base);--ui-ring-ol:var(--z-{z}-ring-outline)"><svg class="ui-ring" width="96" height="96" viewBox="0 0 100 100"><use href="#ui-ring"/></svg></div>' for z in zones)
lockrow = f'<div class="row">{use("ui-lock","ui-lockbadge")}<span class="ui-plate ui-plate--16">{t("flow.lock.reason", name=t("flow.menu.map"))}</span></div>'
css_kit = '''
@font-face{font-family:Vazirmatn;font-weight:400;src:url(%s/Vazirmatn-Regular.woff2)}
@font-face{font-family:Vazirmatn;font-weight:700;src:url(%s/Vazirmatn-Bold.woff2)}
@font-face{font-family:Lalezar;src:url(%s/Lalezar-Regular.woff2)}
html{background:#e7f3f8}body{margin:0;font:400 16px/1.7 Vazirmatn,sans-serif;color:#241a5e;background:#e7f3f8}
main{max-width:430px;margin:0 auto;padding:0 16px 40px}
h1{font:400 28px/1.4 Lalezar,Vazirmatn;margin:14px 0 4px}h3{font:400 24px/1.4 Lalezar,Vazirmatn;margin:26px 0 8px;border-block-end:1.2px solid #241a5e}
.row{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:8px 0}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}figure{margin:0;text-align:center}.ic{display:inline-flex;background:#d6ecf7;border-radius:10px;padding:0}
figcaption{font-size:14px}.night{background:#190539;color:#fff;border-radius:12px;padding:12px;margin:8px 0}
.zn{display:flex;align-items:center;justify-content:center;inline-size:100px;block-size:100px;border-radius:12px}.bd{display:flex;align-items:center;gap:6px;font-weight:700;font-size:16px}
.bar{display:flex;align-items:center;justify-content:space-between;gap:8px;background:#9fdcf2;padding:8px;border-radius:0 0 16px 16px;margin:0 -16px}
.sheets{display:grid;gap:14px}.sz{font-size:14px;color:#241a5e}
''' % (FONTS, FONTS, FONTS)
def btnrow(label_key):
    lab = t(label_key)
    return (f'<div class="row"><button class="ui-btn">{lab}</button><button class="ui-btn ui-btn--sec">{lab}</button>'
            f'<button class="ui-btn ui-btn--hold">{lab}</button><button class="ui-btn" data-state="pressed">{t("v5.ui.state.pressed")}</button>'
            f'<button class="ui-btn" disabled>{t("v5.ui.state.disabled")}</button><button class="ui-btn ui-btn--sec" style="outline:3px solid #fff4d2;outline-offset:2px;box-shadow:0 6px 0 0 #cdbf93,0 6px 0 4.5px #241a5e,0 0 0 8px #3a2a7a">{t("v5.ui.state.focus")}</button>'
            f'<button class="ui-btn ui-btn--s ui-btn--sec">{t("v5.ui.state.compact")}</button></div>')
icon_btns = ''.join(f'<button class="ui-btn ui-btn--icon" aria-label="{t(lk)}"><svg class="ui-gear" aria-hidden="true"><use href="#ui-gearbtn"/></svg><svg class="ui-ic" aria-hidden="true"><use href="#ui-ic-{ic}"/></svg></button>'
                    for ic, lk in (('menu', 'flow.menu.open'), ('close', 'flow.menu.back'), ('search', 'v5.ui.state.search')))
back_btn = f'<button class="ui-btn ui-btn--sec">{use("ui-ic-next","ui-svg ui-svg--32 ui-flip")}{t("flow.menu.back")}</button>'
html = f'''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t("v5.ui.kit.title")}</title><style>{tokens_light}
{CSS}
{css_kit}</style></head><body><div style="position:absolute;width:0;height:0;overflow:hidden">{SPRITE}</div><main>
<div class="bar"><button class="ui-btn ui-btn--icon" aria-label="{t("flow.menu.open")}"><svg class="ui-gear" aria-hidden="true"><use href="#ui-gearbtn"/></svg><svg class="ui-ic" aria-hidden="true"><use href="#ui-ic-menu"/></svg></button>
<div class="ui-chips">{chip("b12", False)}{chip("b34", True)}{chip("b56", False)}</div></div>
<h1>{t("v5.ui.kit.title")}</h1>
<h3>{t("v5.ui.kit.s_buttons")}</h3>{btnrow("flow.menu.back")}<div class="row">{icon_btns}{back_btn}</div>
<h3>{t("v5.ui.kit.s_base")}</h3><div class="ui-chips" style="margin:8px 0">{chip("b12", True)}{chip("b34", False)}{chip("b56", False)}</div>
<h3>{t("v5.ui.kit.s_icons")}</h3><div class="grid">{icon_cells}</div><div class="row">{small_cells}</div>
<h3>{t("v5.ui.kit.s_badges")}</h3><div class="row">{badges_day}</div>
<div class="night" data-world="night"><div class="row">{''.join(f'<div class="bd">{use("ui-badge-"+k,"ui-badge")}<span>{t("difficulty."+k)}</span></div>' for k in ("easy","mid","hard"))}</div></div>
<h3>{t("v5.ui.kit.s_lock")}</h3>{lockrow}<div class="row"><span class="ui-newdot"></span><span class="ui-plate">{t("flow.map.here")}</span></div>
<h3>{t("v5.ui.kit.s_ring")}</h3><div class="row">{rings}</div>
<h3>{t("v5.ui.kit.s_sheets")}</h3><div class="sheets"><div class="ui-sheet"><h2>{t("flow.menu.adults")}</h2><p style="margin:0 0 10px">{t("flow.lock.reason", name=t("flow.menu.cards"))}</p><div class="row"><button class="ui-btn">{t("flow.lock.go")}</button><button class="ui-btn ui-btn--sec">{t("flow.menu.back")}</button></div></div>
<div class="ui-sheet-night" data-world="night"><h2>{t("flow.menu.cards")}</h2><p style="margin:0 0 10px">{t("flow.lock.reason", name=t("flow.menu.practice"))}</p><div class="row"><button class="ui-btn">{t("flow.lock.go")}</button><button class="ui-btn ui-btn--sec">{t("flow.menu.back")}</button></div></div></div>
<h3>{t("v5.ui.kit.s_type")}</h3><div class="sz" style="font:400 28px/1.4 Lalezar">{t("flow.menu.map")} 28</div><div class="sz" style="font:400 24px/1.4 Lalezar">{t("flow.menu.cards")} 24</div><div class="sz" style="font:400 22px/1.4 Lalezar">{t("flow.menu.practice")} 22</div>
<div class="sz" style="font:700 18px/1.7 Vazirmatn">{t("flow.menu.guide")} 18</div><div class="sz" style="font:700 16px/1.7 Vazirmatn">{t("flow.menu.back")} 16</div><div class="sz" style="font:400 16px/1.7 Vazirmatn">{t("flow.menu.adults")} 16</div><div class="sz" style="font:700 14px/1.7 Vazirmatn">{t("flow.map.here")} 14</div>
</main></body></html>'''
(OUT / 'ui_kit.html').write_text(html, encoding='utf-8')
print('ok', len(SPRITE), 'bytes sprite;', len(ICONS), 'icons')
