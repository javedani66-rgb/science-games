#!/usr/bin/env python3
"""دور دوم عامل‌ها (۵ نوامبر): در همهٔ سکوها جایی که کمان پشتی رویه (خط دور بیرونی، polyline data-seam) به خط دور دیواره می‌رسد
یک دندانه/پلهٔ کوچک بود. سر کمان تا نزدیک‌ترین نقطهٔ خط دور دیواره ادامه داده می‌شود تا خط بیرونی یکسره شود."""
import pathlib, re
OUT = pathlib.Path(__file__).resolve().parent / 'out'
num = lambda t: [tuple(map(float, q.split(','))) for q in t.split()]
for f in sorted(OUT.glob('node_*.svg')):
    s = f.read_text(encoding='utf-8')
    if 'data-joined' in s: continue
    i = s.index('_base'); j = s.index('_lit')
    seg = s[i:j]
    m = re.search(r'<polyline data-seam="[^"]*" points="([^"]+)"', seg)
    w = re.search(r'<path d="(M[^"]+)" fill="#[0-9a-f]+" class="eo" stroke-width="7\.6"', seg)
    if not m or not w: print(f.stem, 'skip'); continue
    P = num(m.group(1)); W = [tuple(map(float, q)) for q in re.findall(r'(-?\d+\.?\d*),(-?\d+\.?\d*)', w.group(1))]
    def near(p):
        c = [q for q in W if q[0] * p[0] > 0 and abs(q[0]) >= abs(p[0]) - .6 and q[1] > p[1] + 2]
        return min(c, key=lambda q: (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)
    a, b = near(P[0]), near(P[-1])
    P = [a] + P + [b]
    pts = ' '.join('%.1f,%.1f' % q for q in P)
    seg = seg[:m.start(1)] + pts + '" data-joined="1' + seg[m.end(1):]
    s = s[:i] + seg + s[j:]
    f.write_text(s, encoding='utf-8'); print(f.stem, P[0], P[1], P[-2], P[-1])

# نوار رنگ دیواره زیر کمان رویه (D199) ۱٫۶ واحد پهن‌تر به پایین تا باریکه‌های سرمه‌ای خط دور دیواره زیرش دیده نشود
for f in sorted(OUT.glob('node_*.svg')):
    s = f.read_text(encoding='utf-8')
    if 'data-bandfix' in s: continue
    i = s.index('_base'); j = s.index('_lit'); seg = s[i:j]
    m = re.search(r'<polygon points="([^"]+)" fill="(#[0-9a-f]{6})"', seg)
    if not m: print(f.stem, 'no band'); continue
    P = num(m.group(1)); h = len(P) // 2
    P = P[:h] + [(x, y + 1.6) for x, y in P[h:]]
    seg = seg[:m.start()] + '<polygon data-bandfix="1" points="%s" fill="%s"' % (' '.join('%.1f,%.1f' % q for q in P), m.group(2)) + seg[m.end():]
    f.write_text(s[:i] + seg + s[j:], encoding='utf-8')
