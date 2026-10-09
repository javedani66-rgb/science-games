# gen_palette_css.py: توکن‌های پالت زمین‌ها را از palettes.py در kit.css می‌نویسد (بین دو نشانه).
import os,re
from palettes import PAL,FIG
CSS=os.path.join(os.path.dirname(__file__),'..','kit.css')
out=['/* PALETTES:BEGIN (خودکار از tools/palettes.py؛ دست نزن) */',
 ':root{',
 f'  /* لایهٔ «شکل»: مسیر، گره، برچسب؛ روشن‌ترین لایه با دورگیر تیره (Angstadt؛ WCAG 1.4.11) */',
 f'  --path-light:{FIG["path_light"]}; --path-done:{FIG["path_done"]}; --path-edge:{FIG["path_edge"]}; --path-foot:{FIG["foot"]};',
 '  --path-w:12px; --path-edge-w:18px;  /* رنگ روشن ≥۱۲px و دورگیر تیره ۳px هر طرف */',
 '}']
for k,P in PAL.items():
    out.append(f'.land[data-land="{k}"],.landbox[data-land="{k}"]{{')
    out.append(f'  /* {P["name"]} ({"نور گرم" if P["light"]=="warm" else "نور سرد"}) */')
    for n in ('sky0','sky1','sky2','glow','far','stand','pitch0','pitch1','track','front','deco','accent','accent_d','accent_l'):
        out.append(f'  --l-{n.replace("_","-")}:{P[n]};')
    out.append('}')
for k in PAL:
    for st in ('open','done','trial','locked'):
        out.append(f'.land[data-land="{k}"] .node[data-state="{st}"] .node__disc{{background-image:url("svg/node-{st}-{k}.svg")}}')
    out.append(f'.landbox[data-land="{k}"] .gate{{background-image:url("svg/gate-{k}.svg")}}')
    out.append(f'.land[data-land="{k}"] .mark--start{{background-image:url("svg/flag-start-{k}.svg")}}.land[data-land="{k}"] .mark--end{{background-image:url("svg/flag-end-{k}.svg")}}')
out.append('/* PALETTES:END */')
blk='\n'.join(out)
s=open(CSS).read()
if '/* PALETTES:BEGIN' in s:
    s=re.sub(r'/\* PALETTES:BEGIN.*?/\* PALETTES:END \*/',lambda m:blk,s,flags=re.S)
else:
    s=s.replace('/* ---------- 2) پایه و تایپ ---------- */', '/* ---------- 1b) پالت زمین‌ها ---------- */\n'+blk+'\n\n/* ---------- 2) پایه و تایپ ---------- */',1)
open(CSS,'w').write(s)
print('palette css ok')
