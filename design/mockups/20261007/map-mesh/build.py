#!/usr/bin/env python3
"""Builds the map-mesh sketch (index.html) from docs/research/world/nodes_v2_draft.json.
Sketch only (proposal B30-B32): layout positions are hand-placed here; data comes from the JSON."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[4]
TITLES = json.load(open(ROOT / 'docs/research/world/titles_fa.json', encoding='utf-8'))  # the one place to rename (nodes, lands, zones, path stages)
D = json.load(open(ROOT / 'docs/research/world/nodes_v2_draft.json', encoding='utf-8'))
N = lambda *a: list(a)
LAYOUT = [
 ('L1', [[('F01',780),('F02',560),('F03',340)],[('F04',670),('F06',450),('F07',230)],[('F08',700),('F09',480)]]),
 ('L2', [[('F05',780),('W01',560),('W02',340)],[('W03',450),('W04',230)]]),
 ('LW', [[('E02',700),('E01',480)],[('E07',700)]]),
 ('LM', {'pre':[[('M01',780)]],
         'zones':[('Z1',[[('B01',780),('B02',560),('M04',340),('M05',120)],[('M06',450),('E05',230)]]),
                  ('Z2',[[('M03',700),('M09',480),('M10',260)],[('E03',700)]]),
                  ('Z3',[[('M02',780),('M07',560),('M08',340),('M11',120)]])],
         'post':[[('E06',780),('E04',420)]]}),
]
POS, LAND_BOX, ZONE_BOX = {}, {}, {}
y = 30
def place(rows, ry):
    for row in rows:
        for nid, x in row: POS[nid] = (x, ry)
        ry += 170
    return ry - 170  # y of last row
for lid, spec in LAYOUT:
    top = y
    if isinstance(spec, list):
        last = place(spec, top + 130)
        bottom = last + 105
    else:
        last = place(spec['pre'], top + 130)
        zb = last + 105 + 14
        for zid, rows in spec['zones']:
            zt = zb
            last = place(rows, zt + 135)
            zb = last + 105
            ZONE_BOX[zid] = (zt, zb)
            zb += 14
        last = place(spec['post'], zb + 60)
        bottom = last + 105
    LAND_BOX[lid] = (top, bottom)
    y = bottom + 28
HEIGHT = y
nodes = [{k: n.get(k) for k in ('id','land','label_fa','plain_fa','d1_idea_fa','depths','band_entry','band_entry_note_fa','optional','hidden_detour','main_map_max_depth','textbook_grades','evidence_refs','experimental','experimental_note_fa','zone')} for n in D['nodes'] if not n.get('deferred')]
for n in nodes:
    n['x'], n['y'] = POS[n['id']]
THEMES = json.load(open(ROOT / 'design/themes/map-themes-proposal.json', encoding='utf-8'))  # temporary colour themes (owner-approved 2026-10-08, B52)
lands = [{'id': l['id'], 'theme': THEMES['lands'][l['id']], 'label_fa': l['label_fa'], 'summary_fa': l['summary_fa'], 'y0': LAND_BOX[l['id']][0], 'y1': LAND_BOX[l['id']][1], 'zones': [{'id': z['id'], 'theme': THEMES['zones'][z['id']], 'label_fa': z['label_fa'], 'y0': ZONE_BOX[z['id']][0], 'y1': ZONE_BOX[z['id']][1]} for z in l.get('zones', [])]} for l in D['lands']]
PATHS = {  # proposal B37/B42: main path from force to simple machines (numbers = stages; shortcut = machines only)
 'main': {'label_fa':'مسیر بزرگ: از نیرو تا ماشین‌های ساده', 'stages':[
  {'t':'نیرو','n':['F01','F02','F03','F04']},
  {'t':'نیرو و حرکت (کار خیلی ساده معرفی می‌شود)','n':['F06','F07','F08','F09','E02']},
  {'t':'جرم، وزن و گرانش','n':['F05','W01','W02','W03','W04']},
  {'t':'کار و انرژی','n':['E02','E01']},
  {'t':'ماشین چیست و تعادل','n':['M01','B01','B02']},
  {'t':'اهرم','n':['M04','M05','M06']},
  {'t':'سطح شیب‌دار، گوه و پیچ','n':['M03','M09','M10','E03']},
  {'t':'چرخ، قرقره و چرخ‌دنده (پایان: ماشین کار نمی‌سازد)','n':['M02','M07','M08','M11','E06']}]},
 'machines': {'label_fa':'میانبر: فقط ماشین‌ها (مراحل ۵ تا ۸)', 'from_stage':5},
}
data = {'paths': PATHS, 'lands': lands, 'nodes': nodes, 'edges': [e for e in D['edges'] if e['from'] in POS and e['to'] in POS], 'height': HEIGHT, 'policy': D['depth_policy_proposal']['table']}
for n in nodes:
    t = TITLES['nodes'].get(n['id'])
    if t: n['label_fa'] = t['title']; n['concept_fa'] = t.get('subtitle', t['title']); n['title_status'] = t['status']
for l in lands:
    t = TITLES['lands'].get(l['id'])
    if t: l['label_fa'] = t['title']
    for z in l['zones']:
        tz = TITLES['zones'].get(z['id'])
        if tz: z['label_fa'] = tz['title']
for k, v in TITLES['path_names'].items(): PATHS[k]['label_fa'] = v['title']
for i, s in enumerate(PATHS['main']['stages']): s['t'] = TITLES['path_stages'][i]['title']
data['paths'] = PATHS
tpl = (pathlib.Path(__file__).parent / 'template.html').read_text(encoding='utf-8')
out = tpl.replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False)).replace('__H__', str(HEIGHT))
(pathlib.Path(__file__).parent / 'index.html').write_text(out, encoding='utf-8')
print('ok', len(out))
