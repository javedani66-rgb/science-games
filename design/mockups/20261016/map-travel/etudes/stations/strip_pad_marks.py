#!/usr/bin/env python3
"""D194: مثلث‌های ریز لبهٔ سکو و نقطهٔ تیرهٔ روی رویه از همهٔ نمادهای خروجی (out/node_*.svg) برداشته می‌شوند.
مالک ۴ نوامبر: روی نقشه مثل لکه و آثار اصلاح دیده می‌شوند. کیت (station_kit.pad) هم دیگر آن‌ها را نمی‌کشد؛ این اسکریپت خروجی‌های موجود را بی‌بازسازی پاک می‌کند."""
import re, pathlib, sys
OUT = pathlib.Path(__file__).parent / 'out'
TRI = re.compile(r'<path d="M[-\d.]+,[-\d.]+(?:Q[-\d.]+,[-\d.]+ [-\d.]+,[-\d.]+){3}Z" fill="#(?:8f8bd6|b9b4f0|7b8fe0|a9c4e0)" class="eo" stroke-width="3\.9"/>')
DOT = re.compile(r'<circle cx="[-\d.]+" cy="[-\d.]+" r="3\.5" fill="#[0-9a-f]{6}"/>')
tot = 0
for f in sorted(OUT.glob('node_*.svg')):
    s = f.read_text(encoding='utf-8')
    a = s.index('_base"'); b = s.index('<g id=', a + 10)          # فقط داخل گروه سکو (_base)
    seg = s[a:b]; n1 = len(TRI.findall(seg)); n2 = len(DOT.findall(seg))
    seg = DOT.sub('', TRI.sub('', seg))
    if n1 or n2: f.write_text(s[:a] + seg + s[b:], encoding='utf-8')
    tot += n1 + n2; print(f.name, n1, n2)
print('removed', tot)
