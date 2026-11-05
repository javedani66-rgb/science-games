#!/usr/bin/env python3
"""ماکت جریان کامل (گام ۲): index.html را از template.html و دادهٔ پروژه می‌سازد.
متن‌ها: فقط از strings.fa.json (بانک متن، B50)، titles_fa.json و بانک (کارت قرقره). یادداشت‌های بازبینی: review.fa.json (در بانک نیست)."""
import json, base64, pathlib, io
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
J = lambda p: json.load(open(p, encoding='utf-8'))
TITLES = J(ROOT / 'docs/research/world/titles_fa.json')
NODES = J(ROOT / 'docs/research/world/nodes_v2_draft.json')
THEMES = J(ROOT / 'design/themes/map-themes-proposal.json')
BANK = J(ROOT / 'docs/texts/TEXT_BANK_FA.json')['entries']
STR = J(HERE / 'strings.fa.json')
REV = J(HERE / 'review.fa.json')

def lum(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)
def theme(t):
    t = {k: v for k, v in t.items() if k not in ('scene', 'origin')}
    t['btnink'] = '#FFFFFF' if contrast(t['btn'], '#FFFFFF') >= contrast(t['btn'], '#211D19') else '#211D19'
    return t

EMOJI = dict(F01='⚽', F02='🏀', F03='🏹', F04='🧲', F06='⛸️', F07='🏊', F08='💪', F09='🛹', F05='🚀', W01='📦', W02='⚖️', W03='🌕', W04='🛰️',
             E01='🌬️', E02='🛒', E07='🚰', M01='🚪', B01='🏢', B02='🧱', M04='⛏️', M05='📏', M06='🧰', E05='🔧', M03='🚚', M09='🪓', M10='🔩',
             E03='🌲', M02='🚲', M07='⚓', M08='🏗️', M11='⚙️', E06='🏛️', E04='🕰️')
GROUPS = {
 'L1': [(None, ['F01','F02','F03','F04','F06','F07','F08','F09'])],
 'L2': [(None, ['F05','W01','W02','W03','W04'])],
 'LW': [(None, ['E02','E01','E07'])],
 'LM': [(None, ['M01']), ('Z1', ['B01','B02','M04','M05','M06','E05']), ('Z2', ['M03','M09','M10','E03']), ('Z3', ['M02','M07','M08','M11']), (None, ['E06','E04'])],
}
STAGES = [['F01','F02','F03','F04'], ['F06','F07','F08','F09','E02'], ['F05','W01','W02','W03','W04'], ['E02','E01'], ['M01','B01','B02'], ['M04','M05','M06'], ['M03','M09','M10','E03'], ['M02','M07','M08','M11','E06']]
VISITED = ['F01','F02','F03','F04','F06','F07','F08','F05','W01','W02','W03','E02','E01','M01','B01','B02','M04','M05','M03','M02']  # نمونه، نه دادهٔ واقعی

nodes = {}
for n in NODES['nodes']:
    if n.get('deferred'): continue
    t = TITLES['nodes'][n['id']]
    nodes[n['id']] = dict(id=n['id'], land=n['land'], zone=n.get('zone'), label_fa=t['title'], concept_fa=t.get('subtitle', ''), emoji=EMOJI[n['id']],
                          hidden_detour=bool(n.get('hidden_detour')), experimental=bool(n.get('experimental')), textbook_grades=n.get('textbook_grades') or {})
lands = []
for l in NODES['lands']:
    if l['id'] not in GROUPS: continue
    lands.append(dict(id=l['id'], label_fa=TITLES['lands'][l['id']]['title'], theme=theme(THEMES['lands'][l['id']]),
                      groups=[dict(zone=z, label_fa=TITLES['zones'][z]['title'] if z else None, theme=theme(THEMES['zones'][z]) if z else None, ids=ids) for z, ids in GROUPS[l['id']]]))
edges = [e for e in NODES['edges'] if e['from'] in nodes and e['to'] in nodes]
S = {k: v['text'] for k, v in STR.items()}
card = {b: {k: BANK[f'card.pulley.b{b}.{k}']['text'] for k in ('band', 'say', 'sub') if f'card.pulley.b{b}.{k}' in BANK} for b in (1, 2, 3)}
V = [("SciShow Kids: Need a Lift? Try a Pulley!", "یوتیوب · انگلیسی"), ("SciShow Kids: Solving Problems with Simple Machines", "یوتیوب · انگلیسی")]  # از بازی زنده (content.js)

def b64(b): return base64.b64encode(b).decode()
import re
from PIL import ImageDraw
def slices(path):
    s = open(path, encoding='utf-8').read()
    return [base64.b64decode(m.group(2)) for m in re.finditer(r'data:(image/[a-z+]+);base64,([A-Za-z0-9+/=]{100,})', s)]
def webp(raw, w, alpha=False, q=78):
    im = Image.open(io.BytesIO(raw)).convert('RGBA' if alpha else 'RGB')
    if alpha:  # سفیدی گوشه‌ها را شفاف کن (قاب کارت‌ها گرد است)
        seeds = [(x, y) for x in range(0, im.width, 16) for y in (0, im.height - 1)] + [(x, y) for y in range(0, im.height, 16) for x in (0, im.width - 1)]
        for p in seeds:
            px = im.getpixel(p)
            if px[3] and min(px[:3]) > 225: ImageDraw.floodfill(im, p, (255, 255, 255, 0), thresh=30)
    im = im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'WEBP', quality=q); return 'data:image/webp;base64,' + b64(buf.getvalue())
FLOW = slices(ROOT / 'design/cards/approved/card-space-full-flow-v1/fragment.html')   # 0 عنوان، 1 قرمز، 2 نارنجی، 3 سبز
INTER = slices(ROOT / 'design/cards/approved/harbor-interaction-v1/fragment.html')    # تصویر صحنهٔ سبز، نارنجی، قرمز
img = dict(head=webp(FLOW[0], 420, True), c0=webp(FLOW[3], 520, True), c1=webp(FLOW[2], 520, True), c2=webp(FLOW[1], 520, True),
           a0=webp(INTER[0], 395), a1=webp(INTER[1], 395), a2=webp(INTER[2], 395),
           scene='data:image/webp;base64,' + b64((ROOT / 'design/mockups/20261007/mobile-layout-options/scene-v8-crop.webp').read_bytes()))
fonts = ''.join(f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{b64((ROOT / 'assets/fonts' / f).read_bytes())}) format('woff2')}}"
                for fam, w, f in (('V', 400, 'Vazirmatn-Regular.woff2'), ('V', 700, 'Vazirmatn-Bold.woff2'), ('L', 400, 'Lalezar-Regular.woff2')))
stages = [dict(t=TITLES['path_stages'][i]['title'], n=ids) for i, ids in enumerate(STAGES)]
data = dict(S=S, R=REV, nodes=list(nodes.values()), lands=lands, edges=edges, stages=stages, card=card, videos=V, img=img, visited=VISITED)
out = (HERE / 'template.html').read_text(encoding='utf-8').replace('/*__FONTS__*/', fonts).replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False))
(HERE / 'index.html').write_text(out, encoding='utf-8')
print('ok', len(out) // 1024, 'KB')
