#!/usr/bin/env python3
"""دور دوم عامل‌ها (۵ نوامبر): (۱) نور شیشه‌ای سکو (_lit) روی خط دور بیرونی سکو می‌افتاد و آن را دوتایی/روشن نشان می‌داد:
خط دور بیرونی سکو یک بار دیگر بالای لایه‌های نور و سایه کشیده می‌شود. (۲) درز رویه و دیواره (D199) از ۳٫۹ به ۲٫۶، هم‌اندازهٔ بقیهٔ خط‌های داخلی."""
import pathlib, re
OUT = pathlib.Path(__file__).resolve().parent / 'out'
for f in sorted(OUT.glob('node_*.svg')):
    s = f.read_text(encoding='utf-8')
    if 'data-padtop' in s: continue
    i = s.index('_base'); j = s.index('_lit'); seg = s[i:j]
    w = re.search(r'<path d="(M[^"]+)" fill="#[0-9a-f]+" class="eo" stroke-width="7\.6"', seg)
    sm = re.search(r'<polyline data-seam="[^"]*" points="([^"]+)"', seg)
    t = re.search(r'(<path d="M[^"]+" fill="#[0-9a-f]+" class="eo" stroke-width=")3\.9(")', seg)
    if not (w and sm): print(f.stem, 'skip'); continue
    if t: seg = seg[:t.start()] + t.group(1) + '2.6' + t.group(2) + seg[t.end():]
    s = s[:i] + seg + s[j:]
    k = s.index('_shade'); k = s.index('</g>', k) + 4
    sym = re.search(r'<symbol id="(node_\w+)"', s).group(1)
    d = w.group(1); mm = re.search(r'(-9[0-3]\.\d),(-?\d+\.?\d*)', d)
    if not mm: print(f.stem, 'no left end'); continue
    outer = 'M' + d[mm.start():].rstrip('Z')
    add = ('<g data-padtop="1" transform="translate(100 150)" fill="none" stroke="#241a5e" stroke-linejoin="round" stroke-linecap="round">'
           '<path d="%s" stroke-width="7.6" fill="none"/><polyline points="%s" stroke-width="7.6"/></g>') % (outer, sm.group(1))
    # فقط بخش بیرونی: خط دور دیواره + کمان پشتی؛ کمان جلویی رویه (درز) دست نمی‌خورد
    s = s[:k] + add + s[k:]
    f.write_text(s, encoding='utf-8'); print(f.stem, 'ok')
