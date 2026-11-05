#!/usr/bin/env python3
"""D210 (مالک ۵ نوامبر): «طبقهٔ پایین داربست از داربست زده بیرون». دو تختهٔ داربست (و لایهٔ پشتی‌شان) از ستون‌ها بیرون‌تر بودند:
چپ ۴٫۵ و راست ۱۰ واحد. حالا چپ ≈ ۲ و راست ≈ ۵ واحد بیرون از ستون است (فقط x فشرده می‌شود). علامت data-plankfix؛ دوباره اجرا نمی‌شود."""
import re, pathlib
F = pathlib.Path(__file__).resolve().parent / 'out/node_scaffold.svg'
s = F.read_text(encoding='utf-8')
if 'data-plankfix' in s: raise SystemExit('done before')
X0, X1, NX0, NX1 = -43.8, 42.6, -41.5, 37.0
f = lambda x: NX0 + (x - X0) * (NX1 - NX0) / (X1 - X0)
n = 0
def fix(m):
    global n
    t = m.group(0); attr = 'points' if m.group(1) == 'polygon' else 'd'
    a = re.search(r'\b' + attr + r'="([^"]*)"', t)
    if not a: return t
    nums = [(float(x), float(y)) for x, y in re.findall(r'(-?\d+\.?\d*),(-?\d+\.?\d*)', a.group(1))]
    if not nums: return t
    xs = [p[0] for p in nums]; ys = [p[1] for p in nums]
    side = min(xs) >= 29 and max(xs) <= 44 and max(ys) - min(ys) < 22 and -100 <= min(ys) and max(ys) <= -24   # وجه کناری تخته
    if not side and (max(xs) - min(xs) < 70 or min(xs) < -50 or max(xs) > 46 or min(ys) < -100 or max(ys) > -24): return t
    n += 1
    val = re.sub(r'(-?\d+\.?\d*),(-?\d+\.?\d*)', lambda q: '%.1f,%s' % (f(float(q.group(1))), q.group(2)), a.group(1))
    return t.replace(a.group(0), '%s="%s"' % (attr, val))
a = s.index('id="node_scaffold_hero"')
head, body = s[:a], s[a:]
body = re.sub(r'<(polygon|path)\b[^>]*>', fix, body)
body = body.replace('id="node_scaffold_hero"', 'id="node_scaffold_hero" data-plankfix="1"', 1)
F.write_text(head + body, encoding='utf-8'); print('shifted', n)
