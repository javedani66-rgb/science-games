#!/usr/bin/env python3
"""اصلاح دوم line_pass (مالک ۵ نوامبر، بدنهٔ پیچ): بعضی جزءها خودشان خط ندارند و خط دورشان یک «دورگیری» جداست (مسیر بی‌رنگ هم‌شکل).
line_pass آن دورگیری را نازک کرد ولی لایهٔ پشتی نساخت، پس لبهٔ بیرونی هم نازک شد. اینجا برای چنین جزئی لایهٔ پشتی با پهنای خط اصلی ساخته می‌شود."""
import subprocess, pathlib, sys
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
REF = '66d3796'
JS = r"""([a,b,OUT,NEST])=>{const P=new DOMParser();const load=t=>P.parseFromString('<svg xmlns="http://www.w3.org/2000/svg">'+t+'</svg>','image/svg+xml');
const A=load(a),B=load(b);const sel='path,polygon,polyline,rect,circle,ellipse,line';const NS='http://www.w3.org/2000/svg';
const hero=B.querySelector('[id$="_hero"]');const la=[...A.querySelector('[id$="_hero"]').querySelectorAll(sel)],lb=[...hero.querySelectorAll(sel)].filter(e=>!e.closest('.bk'));
if(la.length!==lb.length)return {err:la.length+'/'+lb.length};
const geo=e=>e.getAttribute('d')||e.getAttribute('points');
const bkd=new Set([...hero.querySelectorAll('.bk *')].map(geo));
function host(e){let tr=[],n=e.parentNode;while(n&&n!==hero&&!(n.id&&n.tagName==='g')){if(n.getAttribute('clip-path')||n.getAttribute('mask')||(n.getAttribute('class')||'').includes('under'))return null;const t=n.getAttribute('transform');if(t)tr.unshift(t);n=n.parentNode}return n?{c:n,tr:tr.join(' ')}:null}
let n=0;
lb.forEach((s,i)=>{const f=(s.getAttribute('fill')||'').toLowerCase();if(f!=='none')return;const st=(s.getAttribute('stroke')||((s.getAttribute('class')||'').includes('eo')?'#241a5e':'')).toLowerCase();if(st!=='#241a5e')return;
 const w0=parseFloat(la[i].getAttribute('stroke-width')||0);if(w0<=3)return;if(bkd.has(geo(s)))return;
 let F=lb.find(x=>x!==s&&geo(x)===geo(s)&&(x.getAttribute('fill')||'none')!=='none');if(!F){const d=(s.getAttribute('d')||'').trim();if(/[zZ]$/.test(d)||s.tagName==='polygon')F=s;else return}const h=host(F);if(!h)return;
 let g=[...h.c.children].find(x=>(x.getAttribute('class')||'')==='bk');if(!g){g=B.createElementNS(NS,'g');g.setAttribute('class','bk');h.c.insertBefore(g,h.c.firstElementChild)}
 const c=B.createElementNS(NS,F.tagName);for(const at of F.attributes)if(['d','points','x','y','width','height','rx','ry','cx','cy','r'].includes(at.name))c.setAttribute(at.name,at.value);
 const t=[h.tr,F.getAttribute('transform')].filter(Boolean).join(' ');if(t)c.setAttribute('transform',t);
 c.setAttribute('fill','#241a5e');c.setAttribute('stroke','#241a5e');c.setAttribute('stroke-width',Math.min(w0,h.c===hero?OUT:NEST).toFixed(2));c.setAttribute('stroke-linejoin','round');g.appendChild(c);bkd.add(geo(s));n++});
return {n,s:new XMLSerializer().serializeToString(B.documentElement.firstElementChild)}}"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    for f in sorted((HERE / 'out').glob('node_*.svg')):
        cur = f.read_text(encoding='utf-8')
        if 'data-linepass' not in cur: continue
        try: old = subprocess.run(['git', 'show', '%s:./out/%s' % (REF, f.name)], cwd=HERE, capture_output=True, text=True, check=True).stdout
        except subprocess.CalledProcessError: continue
        r = pg.evaluate(JS, [old, cur, 7.6, 4.6])
        if 'err' in r: print(f.name, 'mismatch', r['err']); continue
        if r['n']:
            f.write_text(r['s'].replace(' xmlns="http://www.w3.org/2000/svg"', '', 1), encoding='utf-8'); print(f.stem, 'backing added', r['n'])
    b.close()
