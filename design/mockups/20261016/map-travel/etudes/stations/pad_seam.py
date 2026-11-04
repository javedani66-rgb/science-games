#!/usr/bin/env python3
"""D199: مرز رویه و دیوارهٔ سکو خط داخلی است و نازک می‌شود (مالک ۴ نوامبر ۲۲:۱۷: «این خط هم خط داخلیه؛ پس می‌تونه نازک باشه»).
روی همهٔ out/node_*.svg بدون بازسازی: خط دور رویهٔ سکو از OUT (۷٫۶) به W (پیش‌فرض INNER=۳٫۹) می‌رسد؛ نیمهٔ زیرینِ خط دور دیواره
که زیر کمان مانده با رنگ دیواره پوشانده می‌شود؛ کمان بالای رویه (لبهٔ بیرونی نماد) با OUT دوباره کشیده می‌شود. کیت (station_kit.pad با PAD_SEAM_W) همین را می‌کند.
اجرا دوباره بی‌اثر است (نشانهٔ data-seam)."""
import re, sys, pathlib
OUT = 7.6; W = float(sys.argv[1]) if len(sys.argv) > 1 else 3.9
D = pathlib.Path(__file__).parent / 'out'
PATH = re.compile(r'<path (?=[^>]*class="eo")(?=[^>]*stroke-width="7\.6")[^>]*/>')
def attr(el, k): m = re.search(r'\b%s="([^"]*)"' % k, el); return m.group(1) if m else None
for f in sorted(D.glob('node_*.svg')):
    s = f.read_text(encoding='utf-8')
    if 'data-seam' in s: print(f.name, 'skip'); continue
    a = s.index('_base"'); ms = list(PATH.finditer(s, a)); wall, top = ms[0], ms[1]
    pts = [(float(x), float(y)) for x, y in re.findall(r'(-?[\d.]+),(-?[\d.]+)', attr(top.group(0), 'd'))]
    rx = max(abs(x) for x, _ in pts)
    lo = sorted([(x, y) for x, y in pts if y >= 0 and abs(x) < rx - 7], key=lambda q: q[0])
    up = sorted([(x, y) for x, y in pts if y <= 1], key=lambda q: q[0])
    band = [(x, y + W / 2 - .2) for x, y in lo] + [(x, y + OUT / 2 + .8) for x, y in reversed(lo)]
    new_top = top.group(0).replace('stroke-width="7.6"', 'stroke-width="%s"' % W)
    add = ('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in band), attr(wall.group(0), 'fill'))
           + '<polyline data-seam="%s" points="%s" fill="none" class="eo" stroke-width="%s"/>' % (W, ' '.join('%.1f,%.1f' % q for q in up), OUT))
    s = s[:top.start()] + new_top + add + s[top.end():]
    f.write_text(s, encoding='utf-8'); print(f.name, 'ok', len(lo), len(up))
