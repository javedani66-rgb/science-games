#!/usr/bin/env python3
"""Owner rule (2026-10-08): no topic may come before its prerequisite.
Play order = order of `nodes` in docs/research/world/nodes_v2_draft.json
(lands in path order, zones in order). Every prereq_soft / soft_prereq edge
must point from an earlier node to a later one; lands/zones must list nodes in
that same order. Exit 1 on any problem."""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, 'docs/research/world/nodes_v2_draft.json'), encoding='utf-8'))
deferred = {x for l in d.get('deferred_lands', []) for x in l['nodes']}
order = [n['id'] for n in d['nodes']]
pos = {i: k for k, i in enumerate(order)}
N = {n['id']: n for n in d['nodes']}
bad = []
flat = []
for l in d['lands']:
    if l.get('zones'):
        flat += ([x for x in l['nodes'] if x not in {y for z in l['zones'] for y in z['nodes']}][:0])
    for x in l['nodes']:
        if N[x]['land'] != l['id']: bad.append(f"{x}: land={N[x]['land']} but listed in {l['id']}")
# play order implied by lands/zones
implied = []
for l in d['lands']:
    zs = {y for z in l.get('zones', []) for y in z['nodes']}
    entry = [x for x in l['nodes'] if x not in zs and x not in ('E06', 'E04')]
    implied += entry
    for z in l.get('zones', []): implied += z['nodes']
    implied += [x for x in l['nodes'] if x in ('E06', 'E04')]
if [x for x in implied] != [x for x in order if x not in deferred]:
    bad.append('nodes order differs from lands/zones order: ' + ' '.join(implied))
for n in d['nodes']:
    if n['id'] in deferred: continue
    for p in n['prereq_soft']:
        if pos[p] >= pos[n['id']]: bad.append(f"prerequisite {p} comes AFTER {n['id']}")
for e in d['edges']:
    if e['kind'] == 'soft_prereq' and e['to'] not in deferred and pos[e['from']] >= pos[e['to']]:
        bad.append(f"edge {e['from']}->{e['to']} goes backwards")
E = {(e['from'], e['to']) for e in d['edges'] if e['kind'] == 'soft_prereq'}
for n in d['nodes']:
    if n['id'] in deferred: continue
    for p in n['prereq_soft']:
        if (p, n['id']) not in E: bad.append(f"{p}->{n['id']} in prereq_soft but not in edges")
for a, b in E:
    if a not in N[b]['prereq_soft']: bad.append(f"edge {a}->{b} missing from prereq_soft")
for b in bad: print('FAIL', b)
print(f"prereq order: {len(order)} nodes, {len(bad)} problems")
sys.exit(1 if bad else 0)
