#!/usr/bin/env python3
"""سنجش رنگ‌های ui_tokens.css و char_palette.json با ابزار light (فقط روشنایی/رنگ؛ آزموده‌نشده با کودک).
خروجی: ui_char_check.md / .json.  این ابزار فایل‌های ui و character را تغییر نمی‌دهد."""
import re, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, '..', 'assets')
sys.argv = ['x', os.path.join(A, 'light', 'zone_tokens.json')]
src = open(os.path.join(HERE, 'light_contrast.py')).read().split("U, P, Z, W, I")[0]
exec(src.replace("os.path.abspath(__file__)", "'%s'" % (HERE + '/x')))
U, Z, LI, H = T['ui'], T['zones'], T['lights'], T['hardness']
css = open(os.path.join(A, 'ui', 'ui_tokens.css')).read()
root = dict(re.findall(r'--(ui-[a-z0-9-]+):\s*(#[0-9a-fA-F]{6})', css.split('}')[0]))
def rule(sel):
    m = re.search(re.escape(sel) + r'\{([^}]*)\}', css); return m.group(1) if m else ''
def var(s, k, default=None):
    m = re.search(r'--' + k + r':\s*(#[0-9a-fA-F]{6}|var\(--([a-z0-9-]+)\))', s)
    if not m: return default
    return m.group(1) if m.group(1).startswith('#') else root.get(m.group(2))
line, cream, violet = root['ui-line'], root['ui-cream'], root['ui-violet']
rows = []
def chk(name, fg, bg, mn, note=''):
    v = cr(fg, bg); rows.append(dict(name=name, fg=fg, bg=bg, min=mn, val=round(v, 2), ok=v >= mn, note=note))
btn = rule('.ui-btn'); 
chk('دکمهٔ اصلی: متن ÷ فیروزه‌ای', var(btn, 'ink', line), var(btn, 'bg', root['ui-teal']) if var(btn, 'bg') else root['ui-teal'], 4.5)
chk('دکمهٔ ثانویه: متن ÷ کرم', line, var(rule('.ui-btn--sec'), 'bg', cream), 4.5)
hold = rule('.ui-btn--hold'); chk('نگه‌دار: سفید ÷ بنفش', '#ffffff', var(hold, 'bg', root['ui-danger']) or root['ui-danger'], 4.5)
vid = rule('.ui-btn--video'); vbg = re.search(r'--bg:(#[0-9a-fA-F]{6})', vid); vbg = vbg.group(1) if vbg else root['ui-pink']
chk(f'دکمهٔ فیلم: متن ÷ {vbg}', line, vbg, 4.5, 'این hex در ui_tokens.css هنوز ' + vbg + ' است؛ :root --ui-pink = ' + root['ui-pink'])
chk('دکمهٔ فیلم با --ui-pink: متن ÷ صورتی', line, root['ui-pink'], 4.5)
dis = rule('.ui-btn:disabled,.ui-btn[aria-disabled=true]'); chk('غیرفعال: متن ÷ پس‌زمینه', root['ui-ink-disabled'], root['ui-disabled-bg'], 3, 'مستثنا از 4.5 (WCAG)؛ حداقل 3')
chk('چیپ غیرفعال: سفید ÷ بنفش', '#ffffff', violet, 4.5, 'متن 14px کوچک')
chk('چیپ انتخاب‌شده: خط ÷ کرم', line, cream, 4.5)
chk('پلاک: خط ÷ کرم', line, cream, 4.5); chk('ورودی: خط ÷ سفید', line, '#ffffff', 4.5)
chk('کاشی: خط ÷ #d6ecf7', line, '#d6ecf7', 4.5); chk('برگهٔ روز: خط ÷ کرم', line, cream, 4.5)
chk('برگهٔ شب: سفید ÷ #190539', '#ffffff', root['ui-night-bg'], 4.5); chk('لبهٔ برگهٔ شب ÷ زمینه', root['ui-night-edge'], root['ui-night-bg'], 3)
chk('حلقهٔ فوکوس روز: بنفش ÷ کرم', violet, cream, 3); chk('حلقهٔ فوکوس شب: کرم ÷ #190539', cream, root['ui-night-bg'], 3)
chk('خط دور دکمه ÷ کرم', line, cream, 3)
chk('لبهٔ زیرین دکمهٔ اصلی (lip) ÷ فیروزه‌ای', '#1f8a7d', root['ui-teal'], 1.3, 'فقط حس ضخامت؛ نه معنا')
chk('نقطهٔ «تازه» فیروزه‌ای ÷ کرم', root['ui-teal'], cream, 1.0, 'فقط اطلاع؛ با خط دور 2.6 خوانده می‌شود')
chk('نقطهٔ «تازه»: خط ÷ فیروزه‌ای', line, root['ui-teal'], 3)
# رنگ‌مایهٔ رنگ‌های بزرگ رابط (فاصله از سختی)
hrows = []
for nm, hx in (('btn-video', vbg), ('ui-pink', root['ui-pink']), ('btn-hold', root['ui-danger']), ('teal', root['ui-teal']), ('tile-bg', '#d6ecf7')):
    for hk, h in H.items():
        d = hd(hx, h['hex']); dl = abs(lab(hx)[0] - lab(h['hex'])[0]); dc = abs(chroma(hx) - chroma(h['hex']))
        hrows.append(dict(name=nm, hex=hx, level=hk, dist=round(d), ok=d >= 35 or (dl >= 15 and dc >= 20)))
# ---- شخصیت‌ها
cp = json.load(open(os.path.join(A, 'character', 'char_palette.json')))
crow = []; BG = {'چمن': Z['sports']['base'], 'فضا': Z['space']['base'], 'شب': U['card_bg'], }
for k, c in cp.items():
    top = c['top']; hs = [hd(top, h['hex']) for h in H.values()]
    topok = min(hs) >= 35 or all(hd(top, h['hex']) >= 35 or (abs(lab(top)[0] - lab(h['hex'])[0]) >= 15 and abs(chroma(top) - chroma(h['hex'])) >= 20) for h in H.values())
    crow.append(dict(id=k, top=top, top_hue_min_dist=round(min(hs)), top_ok=topok,
                     top_vs_line=round(cr(top, line), 2), skin_vs_line=round(cr(c['skin'], line), 2), hair_vs_skin=round(cr(c['hair'], c['skin']), 2), top_vs_skin=round(cr(top, c['skin']), 2),
                     trim_vs_top=round(cr(c['trim'], top), 2), line_vs_bg={n: round(cr(line, b), 2) for n, b in BG.items()}, top_vs_bg={n: round(cr(top, b), 2) for n, b in BG.items()}))
json.dump(dict(ui=rows, ui_hue=hrows, chars=crow), open(os.path.join(HERE, 'ui_char_check.json'), 'w'), ensure_ascii=False, indent=1)
m = ['# سنجش رنگ رابط و شخصیت‌ها (light)\n', 'فقط روشنایی/رنگ. این ابزار فایل‌های ui و character را تغییر نمی‌دهد؛ اصلاح‌ها در گزارش.\n', '## رابط (ui_tokens.css)\n', '| جفت | پیش‌زمینه | زمینه | مقدار | حداقل | حکم | توضیح |', '|---|---|---|---|---|---|---|']
for r in rows: m.append(f"| {r['name']} | `{r['fg']}` | `{r['bg']}` | {r['val']} | {r['min']} | {'قبول' if r['ok'] else '**قرمز**'} | {r['note']} |")
m += ['\n### فاصلهٔ رنگ‌مایه از سختی (پر بزرگ رابط)\n', '| رنگ | hex | سختی | فاصله° | حکم |', '|---|---|---|---|---|'] + [f"| {h['name']} | `{h['hex']}` | {h['level']} | {h['dist']} | {'قبول' if h['ok'] else '**قرمز**'} |" for h in hrows]
m += ['\n## شخصیت‌ها (char_palette.json)\n', 'top÷خط ≥3 (دو‌لایه با خط دور #241a5e)، skin÷خط (ویژگی‌های چهره: خط روی پوست) ≥3، hair÷skin و لباس÷پوست اطلاعی‌اند (مرز با خط دور 4.5 خوانده می‌شود؛ در خاکستری هم‌روشنایی ممکن است).\n',
      '| شخصیت | لباس | رنگ‌مایه تا سختی (min°) | لباس÷خط | پوست÷خط | مو÷پوست | لباس÷پوست | حاشیه÷لباس | خط÷(چمن/فضا/شب) | لباس÷(چمن/فضا/شب) |', '|---|---|---|---|---|---|---|---|---|---|']
for c in crow:
    m.append(f"| {c['id']} | `{c['top']}` | {c['top_hue_min_dist']}{'' if c['top_ok'] else ' **قرمز**'} | {c['top_vs_line']}{'' if c['top_vs_line']>=3 else ' **قرمز**'} | {c['skin_vs_line']}{'' if c['skin_vs_line']>=3 else ' **قرمز**'} | {c['hair_vs_skin']}{'' if c['hair_vs_skin']>=1.3 else ' (اطلاع)'} | {c['top_vs_skin']}{'' if c['top_vs_skin']>=1.3 else ' (اطلاع)'} | {c['trim_vs_top']}{'' if c['trim_vs_top']>=1.5 else ' **قرمز**'} | " + ' / '.join(str(v) for k, v in c['line_vs_bg'].items() if k != 'آب‌روز') + ' | ' + ' / '.join(str(v) for k, v in c['top_vs_bg'].items() if k != 'آب‌روز') + ' |')
open(os.path.join(HERE, 'ui_char_check.md'), 'w').write('\n'.join(m) + '\n')
print('\n'.join(m))
