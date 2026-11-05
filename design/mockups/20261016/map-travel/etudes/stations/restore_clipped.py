#!/usr/bin/env python3
"""اصلاح line_pass (مالک ۵ نوامبر: «خط دور بدنهٔ پیچ با اینکه خارجیه نازک شده»): جزءهای داخل گروه بریده (clip/mask) یا نیمه‌شفاف
لایهٔ پشتی نمی‌گیرند، پس خط خودشان همان خط دور بیرونی است و نباید نازک شود؛ پهنای خط اصلی‌شان (از نسخهٔ پیش از line_pass) برمی‌گردد."""
import subprocess, pathlib, sys
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
REF = sys.argv[1] if len(sys.argv) > 1 else '66d3796'
JS = r"""([a,b])=>{const P=new DOMParser();const load=t=>P.parseFromString('<svg xmlns="http://www.w3.org/2000/svg">'+t+'</svg>','image/svg+xml');
const A=load(a),B=load(b);const sel='path,polygon,polyline,rect,circle,ellipse,line';
const hero=d=>d.querySelector('[id$="_hero"]');const la=[...hero(A).querySelectorAll(sel)],lb=[...hero(B).querySelectorAll(sel)].filter(e=>!e.closest('.bk'));
if(la.length!==lb.length)return {err:la.length+'/'+lb.length};let n=0;
const clipped=e=>{for(let x=e.parentNode;x&&x.id!==hero(B).id;x=x.parentNode){if(x.getAttribute&&(x.getAttribute('clip-path')||x.getAttribute('mask')))return true}return false};
const opq=e=>{let o=1;for(let x=e;x&&x.getAttribute;x=x.parentNode){const v=x.getAttribute('opacity');if(v!=null)o*=+v}return o};
lb.forEach((e,i)=>{const f=(e.getAttribute('fill')||'').toLowerCase();if(f==='none'||f==='')return;
 if((clipped(e)||opq(e)<.95)&&e.getAttribute('stroke-width')!==la[i].getAttribute('stroke-width')){e.setAttribute('stroke-width',la[i].getAttribute('stroke-width'));n++}});
const s=new XMLSerializer().serializeToString(B.documentElement.firstElementChild);return {n,s}}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for f in sorted((HERE / 'out').glob('node_*.svg')):
        cur = f.read_text(encoding='utf-8')
        if 'data-linepass' not in cur: continue
        try: old = subprocess.run(['git', 'show', '%s:./out/%s' % (REF, f.name)], cwd=HERE, capture_output=True, text=True, check=True).stdout
        except subprocess.CalledProcessError: continue
        r = pg.evaluate(JS, [old, cur])
        if 'err' in r: print(f.name, 'mismatch', r['err']); continue
        if r['n']:
            f.write_text(r['s'].replace(' xmlns="http://www.w3.org/2000/svg"', '', 1), encoding='utf-8'); print(f.stem, 'restored', r['n'])
    b.close()
