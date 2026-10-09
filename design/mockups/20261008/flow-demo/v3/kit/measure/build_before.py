#!/usr/bin/env python3
"""build_before.py: کیت قبلی (کامیت HEAD) را در پوشهٔ موقت بیرون می‌آورد و همان صفحهٔ نقشه را برای ۴ زمین می‌سازد
تا با همان اسکریپت measure.py «پیش از بازنگری» اندازه‌گیری شود (نمونه‌های مقایسه، نه محصول)."""
import subprocess,sys,os,re,shutil
out=sys.argv[1]
repo=subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip()
shutil.rmtree(out,ignore_errors=True); os.makedirs(out)
subprocess.check_call(f'git archive HEAD design/mockups/20261008/flow-demo/v3/kit | tar -x -C {out}',shell=True,cwd=repo)
K=f'{out}/design/mockups/20261008/flow-demo/v3/kit'
h=open(f'{K}/phone.html').read()
a=h.index('<div class="screen" id="s-map">'); b=h.index('<div class="screen" id="s-menu">')
blk=h[a:b]; head=h[:a]; 
pages=''.join(blk.replace('id="s-map"',f'id="b-{k}"').replace('data-land="stadium"',f'data-land="{k}"') for k in ('stadium','space','farm','city'))
open(f'{K}/before.html','w').write(head+'<div style="display:flex;flex-wrap:wrap">'+pages+'</div></body></html>')
print(f'file://{K}/before.html')
