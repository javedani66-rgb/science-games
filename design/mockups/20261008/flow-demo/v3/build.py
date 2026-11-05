#!/usr/bin/env python3
"""ماکت جریان کامل v3: index.html خودبسته از template.html + kit + داده‌ها.
متن‌ها فقط از strings.fa.json (بانک متن، B50) و titles_fa.json؛ یادداشت بازبینی: review.fa.json (در بانک نیست).
فقط SVGهای مورد استفاده از kit/svg، فونت‌ها base64."""
import json, base64, pathlib, io, re
from PIL import Image, ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
FLOW = HERE.parent                      # flow-demo (strings.fa.json، review.fa.json)
ROOT = HERE.parents[4]
J = lambda p: json.load(open(p, encoding='utf-8'))
TITLES = J(ROOT / 'docs/research/world/titles_fa.json')
NODES = J(ROOT / 'docs/research/world/nodes_v2_draft.json')
THREAD = J(HERE / 'thread.json')
BANK = J(ROOT / 'docs/texts/TEXT_BANK_FA.json')['entries']
STR = J(FLOW / 'strings.fa.json')
REV = J(FLOW / 'review.fa.json')
KIT = HERE / 'kit'

SYM = dict(C01='force', C02='friction', C03='multi', C04='weight', C05='energy', C06='machine', C07='lever', C08='slope', C09='wheel', C10='summary')
FRAMES = [  # (پوست زمین، کلید عنوان لوحه، گره‌ها)
 ('stadium', 'L1', ['F01', 'F02', 'F03', 'F04']),
 ('stadium', 'L1', ['F06', 'F07', 'F08', 'F09']),
 ('space', 'L2', ['W01', 'W02', 'F05', 'W03', 'W04']),
 ('farm', 'LW', ['E01', 'E02', 'E07']),
 ('city', 'LM', ['M01', 'B01', 'B02']),
 ('city', 'Z1', ['M04', 'M05', 'M06', 'E05']),
 ('city', 'Z2', ['M03', 'M09', 'M10', 'E03']),
 ('city', 'Z3', ['M02', 'M07', 'M08', 'M11']),
 ('city', 'LM', ['E06', 'E04']),
]
ORDER = [n['id'] for c in THREAD['chapters'] for n in c['nodes']]          # ریسمان (۳۴)
assert [i for f in FRAMES for i in f[2]] == [i for i in ORDER if i != 'M12'], 'frames != thread'
# نمونهٔ وضعیت (نه دادهٔ واقعی)
pre = ORDER[:ORDER.index('M07')]
mid_v = [i for i in pre if i != 'E05']
mid_c = ['F01', 'F02', 'F03', 'F06', 'F08', 'W01', 'W02', 'F05', 'E01', 'M01', 'B01', 'M04', 'M05']
mid_s = [i for i in mid_v if i not in mid_c and i not in ('F04', 'E07', 'M02')]
end_v = [i for i in ORDER if i not in ('E06', 'E04', 'M12')]
end_c = [i for i in end_v if i not in ('F04', 'F07', 'E07', 'M06', 'M10', 'M11', 'E05')]
end_s = [i for i in end_v if i not in end_c and i not in ('M11', 'E07')]
STATES = {'start': dict(visited=[], here='F01', seen=[], coll=[]),
          'mid': dict(visited=mid_v, here='M07', seen=mid_s, coll=mid_c),
          'end': dict(visited=end_v, here='E06', seen=end_s, coll=end_c)}

def split(t):
    i = t.find(':'); return (t[:i].strip(), t[i+1:].strip()) if i >= 0 else (t, '')
plates = {k: split(v['title'])[0] for k, v in {**TITLES['lands'], **TITLES['zones']}.items()}
tn = {n['id']: n for n in NODES['nodes']}
nodes = []
for c in THREAD['chapters']:
    for n in c['nodes']:
        i = n['id']; t = TITLES['nodes'][i]
        nodes.append(dict(id=i, env=t['title'], concept=t.get('subtitle', ''), ch=c['id'], pre=n['prereq'], hidden=bool(tn[i].get('hidden_detour')),
                          trial=bool(tn[i].get('experimental')), deferred=bool(tn[i].get('deferred')), fog=(i == 'E04')))
ENTR = sorted({e['from'] for e in NODES['edges'] if e.get('kind') == 'detour_entrance' and e['to'] == 'E04'})
chapters = [dict(id=c['id'], sym=SYM[c['id']], ids=[n['id'] for n in c['nodes']]) for c in THREAD['chapters']]
frames = [dict(skin=s, plate=plates[p], ids=ids) for s, p, ids in FRAMES]
edges = [e for e in NODES['edges'] if e['from'] in tn and e['to'] in tn and not tn[e['from']].get('deferred') and not tn[e['to']].get('deferred')]
S = {k: v['text'] for k, v in STR.items()}
card = {b: {k: BANK[f'card.pulley.b{b}.{k}']['text'] for k in ('band', 'say', 'sub') if f'card.pulley.b{b}.{k}' in BANK} for b in (1, 2, 3)}
V = [("SciShow Kids: Need a Lift? Try a Pulley!", "یوتیوب · انگلیسی"), ("SciShow Kids: Solving Problems with Simple Machines", "یوتیوب · انگلیسی")]

def b64(b): return base64.b64encode(b).decode()
def slices(path):
    s = open(path, encoding='utf-8').read()
    return [base64.b64decode(m.group(2)) for m in re.finditer(r'data:(image/[a-z+]+);base64,([A-Za-z0-9+/=]{100,})', s)]
def webp(raw, w, alpha=False, q=78):
    im = Image.open(io.BytesIO(raw)).convert('RGBA' if alpha else 'RGB')
    if alpha:
        seeds = [(x, y) for x in range(0, im.width, 16) for y in (0, im.height - 1)] + [(x, y) for y in range(0, im.height, 16) for x in (0, im.width - 1)]
        for p in seeds:
            px = im.getpixel(p)
            if px[3] and min(px[:3]) > 225: ImageDraw.floodfill(im, p, (255, 255, 255, 0), thresh=30)
    im = im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'WEBP', quality=q); return 'data:image/webp;base64,' + b64(buf.getvalue())
FL = slices(ROOT / 'design/cards/approved/card-space-full-flow-v1/fragment.html')
IN = slices(ROOT / 'design/cards/approved/harbor-interaction-v1/fragment.html')
img = dict(head=webp(FL[0], 420, True), c0=webp(FL[3], 520, True), c1=webp(FL[2], 520, True), c2=webp(FL[1], 520, True),
           a0=webp(IN[0], 395), a1=webp(IN[1], 395), a2=webp(IN[2], 395),
           scene='data:image/webp;base64,' + b64((ROOT / 'design/mockups/20261007/mobile-layout-options/scene-v8-crop.webp').read_bytes()))

fonts = ''.join(f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{b64((ROOT / 'assets/fonts' / f).read_bytes())}) format('woff2')}}"
                for fam, w, f in (('Vazirmatn', 400, 'Vazirmatn-Regular.woff2'), ('Vazirmatn', 700, 'Vazirmatn-Bold.woff2'), ('Lalezar', 400, 'Lalezar-Regular.woff2')))

tpl = (HERE / 'template.html').read_text(encoding='utf-8')
css = (KIT / 'kit.css').read_text(encoding='utf-8')
css = re.sub(r'@font-face\{[^}]*\}\n?', '', css)
used = set()
def inline_svg(m):
    name = m.group(2)
    p = KIT / 'svg' / name
    used.add(name)
    return 'url("data:image/svg+xml;base64,' + b64(p.read_bytes()) + '")'
# فقط SVGهایی که در CSS کیت یا الگو به آن‌ها اشاره شده
def inline_all(text): return re.sub(r'url\((["\']?)svg/([A-Za-z0-9_.-]+\.svg)\1\)', inline_svg, text)
css = inline_all(css)
tpl = inline_all(tpl)

data = dict(S=S, R=REV, nodes=nodes, chapters=chapters, frames=frames, edges=edges, entr=ENTR, states=STATES, order=ORDER, card=card, videos=V, img=img)
out = tpl.replace('/*__FONTS__*/', fonts).replace('/*__KIT__*/', css).replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False))
(HERE / 'index.html').write_text(out, encoding='utf-8')
print('ok', len(out) // 1024, 'KB؛ SVG داخل‌شده:', len(used))
