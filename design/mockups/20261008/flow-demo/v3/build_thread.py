#!/usr/bin/env python3
"""Builds thread.json (lesson thread) and verifies B51 (no node before its prerequisites).
Run: python3 -I build_thread.py   (from this folder). Writes thread.json + verify_output.txt"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../../../..'))
nd = json.load(open(f'{ROOT}/docs/research/world/nodes_v2_draft.json'))
tt = json.load(open(f'{ROOT}/docs/research/world/titles_fa.json'))
N = {n['id']: n for n in nd['nodes']}
T = tt['nodes']

# id, name, child sentence (draft), colour need (NOT difficulty colours green/orange/red, D3/D11),
# symbol need, path_stages indices (1-based) it spans, nodes in teaching order
CH = [
 ('C01','نیرو','هل می‌دهیم، می‌کشیم؛ نیرو چیزها را به حرکت درمی‌آورد.','آبی','دست در حال هل‌دادن با پیکان',[1],['F01','F02','F03','F04']),
 ('C02','اصطکاک','چیزهای زبر و صاف حرکت را کم و زیاد می‌کنند.','قهوه‌ای خاکی','کف‌دست روی سطح زبر',[2],['F06','F07']),
 ('C03','چند نیرو','وقتی چند نیرو با هم کار می‌کنند چه می‌شود؟','بنفش','دو پیکان مخالف روی یک جعبه',[2],['F08','F09']),
 ('C04','وزن و جرم','سنگین و سبک چیست و زمین چطور چیزها را می‌کشد؟','فیروزه‌ای','ترازو و سیب',[3],['W01','W02','F05','W03','W04']),
 ('C05','کار و انرژی','برای کار کردن انرژی لازم است.','زرد','آسیاب بادی یا جرقه',[4],['E01','E02','E07']),
 ('C06','ماشین و تعادل','ماشین کارِ ما را راحت‌تر می‌کند؛ تعادل یعنی دو طرف برابر.','صورتی','ترازوی دوکفه',[5],['M01','B01','B02']),
 ('C07','اهرم','یک میله و یک تکیه‌گاه، بار سنگین را بلند می‌کند.','نیلی','اهرم روی تکیه‌گاه',[6],['M04','M05','M06','E05']),
 ('C08','شیب و گوه','راه شیب‌دار، گوه و پیچ نیرو را کمتر می‌کنند.','عنابی','رمپ با گوه',[7],['M03','M09','M10','E03']),
 ('C09','چرخ و قرقره','چرخ و طناب و دنده بار را راحت‌تر می‌برند.','خاکستری‌آبی','قرقره و چرخ‌دنده',[8],['M02','M07','M08','M11']),
 ('C10','جمع‌بندی','نیروی کمتر یعنی راه بیشتر؛ و کنجکاوی برای بیشتر دانستن.','سرمه‌ای با نقش ستاره‌نما (نه ستارهٔ پاداش)','در گشوده به اتاق مه‌آلود',[8],['E06','E04','M12']),
]
order = [n for c in CH for n in c[6]]
out = []
P = out.append
P('== راستی‌آزمایی ریسمان درس (B51) ==')
ok = True
# 1 coverage
miss = set(N) - set(order); dup = {x for x in order if order.count(x) > 1}; extra = set(order) - set(N)
P(f'گره‌ها در nodes: {len(N)} | در ریسمان: {len(order)} | گم‌شده: {sorted(miss)} | تکراری: {sorted(dup)} | ناشناس: {sorted(extra)}')
ok &= not (miss or dup or extra) and len(order) == 34
pos = {n: i for i, n in enumerate(order)}
chap = {n: c[0] for c in CH for n in c[6]}
# 2 prereq edges
bad = []
cnt = {}
for e in nd['edges']:
    cnt[e['kind']] = cnt.get(e['kind'], 0) + 1
    if e['kind'] == 'soft_prereq' and not pos[e['from']] < pos[e['to']]:
        bad.append(e)
P(f"یال‌ها: {cnt}")
P(f"پیش‌نیازهای نقض‌شده (soft_prereq با from بعد از to): {len(bad)} {[(b['from'],b['to']) for b in bad]}")
ok &= not bad
# 3 prereq_soft field consistent with edges
inc = {}
for e in nd['edges']:
    if e['kind'] == 'soft_prereq': inc.setdefault(e['to'], set()).add(e['from'])
mism = [(n, sorted(set(N[n].get('prereq_soft') or []) ^ inc.get(n, set()))) for n in N if set(N[n].get('prereq_soft') or []) != inc.get(n, set())]
P(f'ناهمخوانی فیلد prereq_soft با یال‌ها: {mism}')
bad2 = [(n, p) for n in N for p in (N[n].get('prereq_soft') or []) if pos[p] >= pos[n]]
P(f'نقض بر پایهٔ prereq_soft: {bad2}'); ok &= not bad2
# 4 detour entrances (E04) should precede it (visible entrance)
de = [e for e in nd['edges'] if e['kind'] == 'detour_entrance']
bad3 = [(e['from'], e['to']) for e in de if pos[e['from']] >= pos[e['to']]]
P(f'ورودی‌های مسیر مخفی که بعد از مقصد آمده‌اند: {bad3}'); ok &= not bad3
# 5 chapter-level monotonic (a chapter never needs a later chapter)
cidx = {c[0]: i for i, c in enumerate(CH)}
bad4 = [(a, b) for a, b in [(e['from'], e['to']) for e in nd['edges'] if e['kind'] == 'soft_prereq'] if cidx[chap[a]] > cidx[chap[b]]]
P(f'پیش‌نیاز در فصل دیرتر: {bad4}'); ok &= not bad4
# 6 info: related edges order
for e in nd['edges']:
    if e['kind'] == 'related':
        P(f"اطلاع (related، پیش‌نیاز نیست): {e['from']}->{e['to']} {'به‌ترتیب' if pos[e['from']]<pos[e['to']] else 'برعکس'}")
# 7 topological sanity with Kahn: a valid topo order exists
ind = {n: len(inc.get(n, ())) for n in N}; q = [n for n in N if ind[n] == 0]; seen = 0
adj = {}
for e in nd['edges']:
    if e['kind'] == 'soft_prereq': adj.setdefault(e['from'], []).append(e['to'])
while q:
    x = q.pop(); seen += 1
    for y in adj.get(x, []):
        ind[y] -= 1
        if ind[y] == 0: q.append(y)
P(f'گراف بدون دور است (Kahn): {seen == len(N)}'); ok &= seen == len(N)
P('نتیجه: ' + ('درست ✔ همهٔ شرط‌ها برقرارند' if ok else 'ناموفق ✘'))
P('')
P('ترتیب نهایی: ' + ' > '.join(order))

def flags(n):
    d = N[n]; f = []
    if d.get('band_entry') == 'to_test': f.append('to_test')
    if d.get('hidden_detour'): f.append('hidden_detour')
    if d.get('optional'): f.append('optional')
    if n == 'M12': f.append('deferred')
    if d.get('experimental'): f.append('experimental')
    return f
js = {
 '_readme_fa': 'ریسمان درس: ترتیب منطقی تدریس همهٔ ۳۴ گره. تنها منبع ترتیب کارت‌دان. تولید و راستی‌آزمایی: build_thread.py. نام فصل‌ها و جمله‌ها draft هستند و باید به strings.fa.json بروند (کلیدها: thread.<id>.name / thread.<id>.line). این فایل ادعایی دربارهٔ فهم کودک نیست (B9).',
 'status': 'draft', 'verified_b51': ok,
 'state_rules': {'locked': 'گرهٔ هنوز نرسیده (پیش‌نیاز دیده نشده)', 'unseen': 'باز شده ولی کودک کارت را باز نکرده', 'seen': 'کودک کارت را خوانده/ورق زده', 'collected': 'کودک خودش «بذار تو جعبه» زده؛ وارد تمرین می‌شود', 'fog': 'فقط hidden_detour تا کشف نشده'},
 'chapters': [], 'order': order}
for c in CH:
    js['chapters'].append({'id': c[0], 'name_fa': c[1], 'line_fa': c[2], 'color_need': c[3], 'symbol_need': c[4], 'path_stages': c[5],
      'nodes': [{'id': n, 'pos': pos[n] + 1, 'label_fa': N[n]['label_fa'], 'env_title_fa': T[n]['title'], 'flags': flags(n),
                 'prereq': sorted(inc.get(n, [])), 'band_entry': N[n].get('band_entry')} for n in c[6]]})
json.dump(js, open(f'{HERE}/thread.json', 'w'), ensure_ascii=False, indent=1)
open(f'{HERE}/verify_output.txt', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out)); sys.exit(0 if ok else 1)
