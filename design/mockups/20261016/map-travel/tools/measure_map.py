#!/usr/bin/env python3
"""اندازه‌گیری دقیق نقشهٔ سفر (پیکسلی، از روی رندر واقعی با Playwright).
اجرا:  python3 tools/measure_map.py [--json out.json] [--png dir]
  ۱) فاصلهٔ برچسب (با هالهٔ دیده‌شده) تا سکو/بنا و تا حلقهٔ «اینجایی»   حداقل ۷px
  ۲) فاصلهٔ هر ردپا تا سکو و ساختمان (همهٔ ایستگاه‌ها)                   حداقل ۱۵px
  ۳) ردپا کاملاً داخل پر راه (حاشیه تا لبهٔ راه؛ در انتهای منحنی‌ها هم)   حداقل ۰٫۵px
  ۴) قفل‌ها: جای نسبی نسبت به مرکز سکو، رنگ، کاملاً روی سکو بودن؛ رنگ سکوهای قفل
واحد: پیکسل CSS در دستگاه ۳۹۰ واحدی نقشه. خروجی: جدول + کد خروج ۱ اگر تخطی باشد."""
import sys, json, io, pathlib, argparse
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent.parent
SC = 2                       # scale
LAB_MIN, PRINT_NODE_MIN, ROAD_MIN = 7.0, 15.0, 0.5
LOCKED = ['M11', 'E04', 'E06', 'M12']

SETUP = r"""
() => {
 const st=document.createElement('style');st.id='pass';
 st.textContent='html,body,#sc,#page,#root{background:transparent!important}#rv,#bar{display:none!important}#sc{overflow:visible!important}#world{position:absolute!important;left:0;top:0;transform:none!important;margin:0!important}'
  +'svg.map{visibility:hidden}#world > div,#world > button,#fig,#boat{visibility:hidden}';
 document.head.appendChild(st);
 window.__vis=[];
 window.__show=(els,hid)=>{window.__vis.forEach(e=>e.style.visibility='');window.__vis=[];els.forEach(e=>{e.style.visibility='visible';window.__vis.push(e)});(hid||[]).forEach(e=>{e.style.visibility='hidden';window.__vis.push(e)})};
 window.__layer=(id,mode)=>{ // کپی بنای ایستگاه بدون سایه/نور (مثل EXC در template)
  const svg=document.querySelector('svg.map'),g=svg.querySelector('g.node[data-id="'+id+'"]'),u=g.querySelector('use');
  const sym=document.querySelector(u.getAttribute('href')),vb=(sym.getAttribute('viewBox')||'0 0 200 190').split(/\s+/).map(Number);
  const tg=document.createElementNS('http://www.w3.org/2000/svg','g');
  tg.setAttribute('transform','translate('+u.x.baseVal.value+' '+u.y.baseVal.value+') scale('+(u.width.baseVal.value/vb[2])+' '+(u.height.baseVal.value/vb[3])+')');
  if(g.getAttribute('filter'))tg.setAttribute('filter',g.getAttribute('filter'));
  tg.dataset.m='tmp';
  [...sym.children].forEach(c=>{if(c.tagName==='defs'||/_(shadow|lit|shade)$/.test(c.id))return;const cl=c.cloneNode(true);cl.removeAttribute('id');
    cl.querySelectorAll('.under,.esd').forEach(x=>x.remove());
    if(mode==='pad'){if(!/_base$/.test(c.id))return;const eo=[...cl.querySelectorAll(':scope > path.eo')].slice(0,2);cl.innerHTML='';eo.forEach(p=>cl.appendChild(p))}
    tg.appendChild(cl)});
  svg.appendChild(tg);return tg};
 window.__clean=()=>document.querySelectorAll('[data-m=tmp]').forEach(x=>x.remove());
}
"""

def png(pg, clip=None):
    im = Image.open(io.BytesIO(pg.screenshot(omit_background=True, clip=clip or {'x': 0, 'y': 0, 'width': 390, 'height': pg.evaluate('H_')})))
    return np.array(im)[:, :, 3] > 60

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--json'); ap.add_argument('--png'); ap.add_argument('--html', default=str(HERE / 'index.html'))
    a = ap.parse_args()
    rep = {'labels': [], 'prints': {}, 'locks': [], 'viol': []}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 700}, device_scale_factor=SC)
        pg.goto('file://' + a.html); pg.wait_for_timeout(700)
        H = pg.evaluate('document.getElementById("world").offsetHeight'); pg.add_script_tag(content='window.H_=%d' % H)
        pg.set_viewport_size({'width': 390, 'height': H}); pg.evaluate(SETUP); pg.wait_for_timeout(300)
        ids = pg.evaluate('Object.keys(NODES).filter(i=>document.querySelector(\'svg.map g.node[data-id="\'+i+\'"]\')&&NODES[i].y<H_-40)')
        titles = pg.evaluate('Object.fromEntries(Object.keys(NODES).map(i=>[i,NODES[i].title]))')
        # ---- لایهٔ بناها (سکو + بنا)
        mask_nodes = {}
        for i in ids:
            pg.evaluate('(i)=>{__clean();__show([__layer(i,"all")])}', i); mask_nodes[i] = png(pg)
        allnode = np.zeros_like(next(iter(mask_nodes.values())))
        for m in mask_nodes.values(): allnode |= m
        dn = ndi.distance_transform_edt(~allnode) / SC       # فاصله تا نزدیک‌ترین بنا/سکو
        dn_i = {i: ndi.distance_transform_edt(~m) / SC for i, m in mask_nodes.items()}
        # ---- برچسب‌ها
        pg.evaluate('__clean()')
        lab = pg.evaluate('''()=>{const o=[];document.querySelectorAll('svg.map text').forEach(t=>{const s=t.textContent.trim();
          for(const i in NODES){if(NODES[i].title===s){const r=t.getBoundingClientRect();o.push({id:i,t:s,r:[r.left,r.top,r.right,r.bottom],el:null});}}});return o}''')
        pg.evaluate('''()=>{const els=[];document.querySelectorAll('svg.map text').forEach(t=>{for(const i in NODES)if(NODES[i].title===t.textContent.trim())els.push(t)});__show(els)}''')
        ml = png(pg)
        for L in lab:
            x0, y0, x1, y1 = [int(v * SC) for v in L['r']]; x0 -= 20; y0 -= 20; x1 += 20; y1 += 20
            sub = np.zeros_like(ml); sub[max(0, y0):y1, max(0, x0):x1] = ml[max(0, y0):y1, max(0, x0):x1]
            ys, xs = np.nonzero(sub)
            L['ink'] = [xs.min() / SC, ys.min() / SC, xs.max() / SC, ys.max() / SC]
            L['gap_own'] = float(dn_i[L['id']][sub].min()); L['gap_any'] = float(dn[sub].min())
            # حلقه (وقتی «اینجایی» است)
            pg.evaluate('(i)=>{__clean();here=i;refreshRing()}', L['id'])
            pg.evaluate('()=>{__show([])}')
            pg.evaluate('(()=>{const r=[...document.querySelectorAll("#world > div")].find(d=>d.style.borderRadius==="50%");r.style.visibility="visible"})')
            mr = png(pg)
            pg.evaluate('(()=>{const r=[...document.querySelectorAll("#world > div")].find(d=>d.style.borderRadius==="50%");r.style.visibility=""})')
            L['gap_ring'] = float((ndi.distance_transform_edt(~mr) / SC)[sub].min()) if mr.any() else None
            L.pop('r')
            rep['labels'].append(L)
            if min(L['gap_own'], L['gap_any'], L['gap_ring'] if L['gap_ring'] is not None else 99) < LAB_MIN: rep['viol'].append('label %s gap<%g' % (L['id'], LAB_MIN))
        # ---- ردپاها
        pg.evaluate('()=>{__clean();const pr=document.getElementById("prints");[...pr.childNodes].forEach(g=>{g.style.display="";g.dataset.on="1";const e=g.firstChild;if(e)e.style.animation="none"})}')
        pg.evaluate('()=>__show([document.getElementById("prints")])'); mp = png(pg)
        # راه: فقط پر راه (چهارمین مسیر env_path)  + اسکله
        pg.evaluate('()=>{const g=document.getElementById("env_path"),p=[...g.children];__show([g],p.filter((x,i)=>i!==3))}'); road = png(pg)
        pg.evaluate('()=>{const jt=document.getElementById("jetty");__show([jt])}'); jet = png(pg)
        walk = road | jet
        dedge = ndi.distance_transform_edt(walk) / SC        # فاصلهٔ هر پیکسل راه تا نزدیک‌ترین پیکسل غیرراه
        lab_p, n = ndi.label(ndi.binary_dilation(mp, iterations=1))
        res = []
        for k in range(1, n + 1):
            m = (lab_p == k) & mp
            ys, xs = np.nonzero(m)
            if len(ys) < 12: continue
            cx, cy = xs.mean() / SC, ys.mean() / SC
            ev = dedge[m]
            res.append({'x': round(cx, 1), 'y': round(cy, 1), 'node_gap': round(float(dn[m].min()), 1), 'in_road': round(float(ev.min()), 1), 'outside_px': int((ev == 0).sum()), 'nearest': None})
        near = pg.evaluate('(pts)=>pts.map(p=>{let b=null,bd=1e9;for(const i in NODES){const d=Math.hypot(NODES[i].x-p[0],NODES[i].y-p[1]);if(d<bd){bd=d;b=i}}return b})', [[r['x'], r['y']] for r in res])
        for r, nr in zip(res, near): r['nearest'] = nr
        rep['prints'] = {'count': len(res), 'min_node_gap': min(r['node_gap'] for r in res), 'min_in_road': min(r['in_road'] for r in res),
                         'bad_node': [r for r in res if r['node_gap'] < PRINT_NODE_MIN], 'bad_road': [r for r in res if r['in_road'] < ROAD_MIN]}
        if rep['prints']['bad_node']: rep['viol'].append('prints near node: %d' % len(rep['prints']['bad_node']))
        if rep['prints']['bad_road']: rep['viol'].append('prints outside road: %d' % len(rep['prints']['bad_road']))
        # ---- قفل‌ها
        locks = pg.evaluate('''()=>[...document.querySelectorAll('svg.map g[transform]')].filter(g=>g.firstElementChild&&g.firstElementChild.tagName==='circle'&&g.firstElementChild.getAttribute('r')==='10').map(g=>{
          const m=/translate\\(([-\\d.]+) ([-\\d.]+)\\)/.exec(g.getAttribute('transform'));const c=g.firstElementChild;return {x:+m[1],y:+m[2],fill:c.getAttribute('fill'),stroke:c.getAttribute('stroke'),sw:c.getAttribute('stroke-width'),filter:!!g.closest('[style*=filter]')}})''')
        locks = [l for l in locks if l['y'] < H and any(abs(l['x']-pg.evaluate('NODES["%s"].x' % i))<60 and abs(l['y']-pg.evaluate('NODES["%s"].y' % i))<60 for i in LOCKED)]
        for lk in locks:
            nid = min(ids, key=lambda i: np.hypot(lk['x'] - pg.evaluate('NODES["%s"].x' % i), lk['y'] - pg.evaluate('NODES["%s"].y' % i)))
            n = pg.evaluate('NODES["%s"]' % nid)
            pg.evaluate('(i)=>{__clean();__show([__layer(i,"pad")])}', nid); pad = png(pg)
            pg.evaluate('()=>{__clean();const g=[...document.querySelectorAll("svg.map g[transform]")].filter(g=>g.firstElementChild&&g.firstElementChild.tagName==="circle"&&g.firstElementChild.getAttribute("r")==="10");window.__lk=g}')
            lk['node'] = nid; lk['dx'] = round(lk['x'] - n['x'], 1); lk['dy'] = round(lk['y'] - n['y'], 1)
            pg.evaluate('(xy)=>{const g=__lk.find(g=>g.getAttribute("transform").includes("translate("+xy[0]+" "+xy[1]+")"));__show([g,...g.querySelectorAll("*")])}', [lk['x'], lk['y']]); lm = png(pg)
            lk['off_pad_px'] = int((lm & ~ndi.binary_dilation(pad, iterations=0)).sum()); lk['edge_margin'] = round(float((ndi.distance_transform_edt(pad) / SC)[lm].min()), 1) if lm.any() else None
            lk['pad_colors'] = pg.evaluate('(i)=>{const g=document.querySelector(\'g.node[data-id="\'+i+\'"]\');const u=g.querySelector("use");const s=document.querySelector(u.getAttribute("href"));const b=s.querySelector("[id$=_base]");return [...b.querySelectorAll(":scope > path.eo")].slice(0,2).map(p=>p.getAttribute("fill"))}', nid)
            rep['locks'].append(lk)
        if a.png:
            d = pathlib.Path(a.png); d.mkdir(exist_ok=True, parents=True)
            Image.fromarray((np.stack([allnode, mp, road], -1) * 255).astype('uint8')).save(d / 'masks.png')
        b.close()
    # ---- چاپ
    print('== برچسب‌ها (px؛ حداقل %g)' % LAB_MIN); 
    for L in rep['labels']:
        print('  %-4s %-16s سکو/بنای خودش %5.1f | هر شکلی %5.1f | حلقه %s %s' % (L['id'], L['t'], L['gap_own'], L['gap_any'], ('%5.1f' % L['gap_ring']) if L['gap_ring'] is not None else ' -', '' if min(L['gap_own'], L['gap_any'], L['gap_ring'] or 99) >= LAB_MIN else '  <-- تخطی'))
    P = rep['prints']; print('== ردپاها: %d؛ کمترین فاصله تا سکو/بنا %.1f (حداقل %g)؛ کمترین حاشیهٔ داخل راه %.1f (حداقل %g)' % (P['count'], P['min_node_gap'], PRINT_NODE_MIN, P['min_in_road'], ROAD_MIN))
    for r in P['bad_node']: print('  نزدیک بنا  (%.0f,%.0f) نزدیک %s: %.1f' % (r['x'], r['y'], r['nearest'], r['node_gap']))
    for r in P['bad_road']: print('  بیرون راه  (%.0f,%.0f) نزدیک %s: حاشیه %.1f، پیکسل بیرون %d' % (r['x'], r['y'], r['nearest'], r['in_road'], r['outside_px']))
    print('== قفل‌ها'); 
    for lk in rep['locks']: print('  %-4s dx=%5.1f dy=%5.1f پر=%s خط=%s ض=%s بیرون از سکو %dpx حاشیه تا لبهٔ سکو %s رنگ سکو %s' % (lk['node'], lk['dx'], lk['dy'], lk['fill'], lk['stroke'], lk['sw'], lk['off_pad_px'], lk['edge_margin'], lk['pad_colors']))
    if a.json: json.dump(rep, open(a.json, 'w'), ensure_ascii=False, indent=1)
    print('== تخطی‌ها: %d' % len(rep['viol'])); [print('  -', v) for v in rep['viol']]
    sys.exit(1 if rep['viol'] else 0)

if __name__ == '__main__': main()
