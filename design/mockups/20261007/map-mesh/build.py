#!/usr/bin/env python3
"""Builds the map-mesh sketch (index.html) from docs/research/world/nodes_v2_draft.json.
Sketch only (proposal B30-B32): layout positions are hand-placed here; data comes from the JSON."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[4]
D = json.load(open(ROOT / 'docs/research/world/nodes_v2_draft.json', encoding='utf-8'))
ROWS = {  # land -> rows of (node id, x); y is computed so the land label never touches a node
 'L1':[[('F01',780),('F02',560),('F03',340)],[('F04',670),('F08',450),('F09',230)],[('F06',700),('F07',480)]],
 'L2':[[('F05',780),('W01',560),('W02',340)],[('W03',450),('W04',230)]],
 'L4':[[('B01',780),('B02',560),('M04',340),('M05',120)],[('M06',450),('E05',230)]],
 'L5':[[('M03',700),('M09',480),('M10',260)]],
 'L6':[[('M02',780),('M07',560),('M08',340),('M11',120)]],
 'L7':[[('M01',780),('E03',560),('E02',340),('E01',120)],[('M12',700),('E06',480)],[('E04',600),('E07',300)]],
}
POS, LAND_BOX = {}, {}
y = 30
for lid in ['L1','L2','L4','L5','L6','L7']:
    top = y
    ry = top + 130
    for row in ROWS[lid]:
        for nid, x in row:
            POS[nid] = (x, ry)
        ry += 170
    bottom = ry - 170 + 105
    LAND_BOX[lid] = (top, bottom)
    y = bottom + 28
HEIGHT = y
nodes = [{k: n.get(k) for k in ('id','land','label_fa','plain_fa','d1_idea_fa','depths','band_entry','band_entry_note_fa','optional','hidden_detour','main_map_max_depth','textbook_grades','evidence_refs','experimental','experimental_note_fa')} for n in D['nodes']]
for n in nodes:
    n['x'], n['y'] = POS[n['id']]
lands = [{'id': l['id'], 'label_fa': l['label_fa'], 'summary_fa': l['summary_fa'], 'y0': LAND_BOX[l['id']][0], 'y1': LAND_BOX[l['id']][1]} for l in D['lands']]
data = {'lands': lands, 'nodes': nodes, 'edges': D['edges'], 'height': HEIGHT, 'policy': D['depth_policy_proposal']['table']}
tpl = (pathlib.Path(__file__).parent / 'template.html').read_text(encoding='utf-8')
out = tpl.replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False)).replace('__H__', str(HEIGHT))
(pathlib.Path(__file__).parent / 'index.html').write_text(out, encoding='utf-8')
print('ok', len(out))
