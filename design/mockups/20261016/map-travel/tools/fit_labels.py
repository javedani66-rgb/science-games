#!/usr/bin/env python3
"""یک دور تنظیم خودکار LABEL_DY در build.py از روی خروجی measure_map.py --json (حداقل فاصله ۷٫۵)."""
import json, re, sys, math, pathlib
H = pathlib.Path(__file__).resolve().parent.parent
rep = json.load(open(sys.argv[1])); b = (H / 'build.py').read_text(encoding='utf-8')
cur = eval(re.search(r'^LABEL_DY = (\{.*?\})', b, re.M).group(1))
for L in rep['labels']:
    g = min(L['gap_own'], L['gap_any'], L['gap_ring'] if L['gap_ring'] is not None else 99)
    if g < 7.5: cur[L['id']] = cur.get(L['id'], 0) + math.ceil((7.5 - g) * 2) / 2
b = re.sub(r'^LABEL_DY = \{.*?\}', 'LABEL_DY = ' + repr(cur), b, count=1, flags=re.M)
(H / 'build.py').write_text(b, encoding='utf-8'); print(cur)
