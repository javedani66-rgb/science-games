#!/usr/bin/env python3
"""Builds the map-mesh sketch (index.html) from docs/research/world/nodes_v2_draft.json.
Sketch only (proposal B30-B32): layout positions are hand-placed here; data comes from the JSON."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[4]
D = json.load(open(ROOT / 'docs/research/world/nodes_v2_draft.json', encoding='utf-8'))
N = lambda *a: list(a)
LAYOUT = [
 ('L1', [[('F01',780),('F02',560),('F03',340)],[('F04',670),('F08',450),('F09',230)],[('F06',700),('F07',480)]]),
 ('L2', [[('F05',780),('W01',560),('W02',340)],[('W03',450),('W04',230)]]),
 ('LW', [[('E02',700),('E01',480)],[('E03',700),('E07',480)]]),
 ('LM', {'pre':[[('M01',780)]],
         'zones':[('Z1',[[('B01',780),('B02',560),('M04',340),('M05',120)],[('M06',450),('E05',230)]]),
                  ('Z2',[[('M03',700),('M09',480),('M10',260)]]),
                  ('Z3',[[('M02',780),('M07',560),('M08',340),('M11',120)]])],
         'post':[[('E06',780)]]}),
 ('LC', [[('M12',700),('E04',420)]]),
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
            last = place(rows, zt + 100)
            zb = last + 105
            ZONE_BOX[zid] = (zt, zb)
            zb += 14
        last = place(spec['post'], zb + 60)
        bottom = last + 105
    LAND_BOX[lid] = (top, bottom)
    y = bottom + 28
HEIGHT = y
nodes = [{k: n.get(k) for k in ('id','land','label_fa','plain_fa','d1_idea_fa','depths','band_entry','band_entry_note_fa','optional','hidden_detour','main_map_max_depth','textbook_grades','evidence_refs','experimental','experimental_note_fa','zone')} for n in D['nodes']]
for n in nodes:
    n['x'], n['y'] = POS[n['id']]
lands = [{'id': l['id'], 'label_fa': l['label_fa'], 'summary_fa': l['summary_fa'], 'y0': LAND_BOX[l['id']][0], 'y1': LAND_BOX[l['id']][1], 'zones': [{'id': z['id'], 'label_fa': z['label_fa'], 'y0': ZONE_BOX[z['id']][0], 'y1': ZONE_BOX[z['id']][1]} for z in l.get('zones', [])]} for l in D['lands']]
data = {'lands': lands, 'nodes': nodes, 'edges': D['edges'], 'height': HEIGHT, 'policy': D['depth_policy_proposal']['table']}
tpl = (pathlib.Path(__file__).parent / 'template.html').read_text(encoding='utf-8')
out = tpl.replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False)).replace('__H__', str(HEIGHT))
(pathlib.Path(__file__).parent / 'index.html').write_text(out, encoding='utf-8')
print('ok', len(out))
