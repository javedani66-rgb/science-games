#!/usr/bin/env python3
"""مالک ۵ نوامبر: «رنگ سبز سکوهای سرزمین اول رو یه چند درجه تغییر بده که عین خود بک‌گراوندشون نباشه.»
رنگ‌های سکوی سبز (فقط گروه _base) ۲۲ درجه به سوی زرد-لیمویی چرخانده می‌شوند. زمینهٔ ورزشگاه حدود (۷۲،۱۵۹،۵۳) است."""
import pathlib, re
OUT = pathlib.Path(__file__).resolve().parent / 'out'
MAP = {'#4f8a2c': '#718a2c', '#7fbf4a': '#aabf4a', '#a8d878': '#cbd878'}
for f in sorted(OUT.glob('node_*.svg')):
    s = f.read_text(encoding='utf-8')
    if '#7fbf4a' not in s: continue
    i = s.index('_base'); j = s.index('_lit')
    seg = s[i:j]
    for a, b in MAP.items(): seg = seg.replace(a, b)
    f.write_text(s[:i] + seg + s[j:], encoding='utf-8'); print(f.stem)
