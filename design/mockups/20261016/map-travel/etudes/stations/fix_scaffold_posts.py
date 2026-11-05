#!/usr/bin/env python3
"""D211 (مالک ۵ نوامبر): «ستون‌ها از وسط تخته رد نشده‌اند؛ تختهٔ طبقهٔ پایین از پایه‌ها بیرون زده و با بالایی همراستا نیست».
تخته‌ها روی ستون‌ها کشیده شده بودند و ستون زیرشان گم می‌شد. حالا یک کپی از ستون‌ها (خط دور نازک + رنگ + روشنایی) فقط در نوار هر تخته
(clipPath) بعد از تخته‌ها کشیده می‌شود، پس ستون از جلوی تخته رد می‌شود. علامت data-postfix؛ دوباره اجرا نمی‌شود."""
import re, pathlib
F = pathlib.Path(__file__).resolve().parent / 'out/node_scaffold.svg'
s = F.read_text(encoding='utf-8')
if 'data-postfix' in s: raise SystemExit('done before')
a = s.index('id="node_scaffold_hero"'); head, h = s[:a], s[a:]
def geo(t):
    g = re.search(r'(?:points|d)="([^"]*)"', t)
    if not g: return None
    n = [(float(x), float(y)) for x, y in re.findall(r'(-?\d+\.?\d*),(-?\d+\.?\d*)', g.group(1))]
    return (min(p[0] for p in n), max(p[0] for p in n), min(p[1] for p in n), max(p[1] for p in n)) if n else None
navy, color = [], []
for m in re.finditer(r'<(polygon|path)\b[^>]*/>', h):
    t = m.group(0); b = geo(t)
    if not b: continue
    x0, x1, y0, y1 = b
    post = (-40 <= x0 and x1 <= -25) or (19 <= x0 and x1 <= 33)
    if not post or x1 - x0 > 16 or y1 - y0 < 80: continue
    if 'fill="#241a5e"' in t and 'stroke-width="7.60"' in t:
        navy.append(t.replace('stroke-width="7.60"', 'stroke-width="5.2"'))
    elif 'class="eo"' in t or 'stroke-linejoin="round"/>' in t:
        color.append(t)
print('navy', len(navy), 'color', len(color))
# آخرین جزء تختهٔ بالایی و پایینی: درج پیش از بازو (گروه نردبان/بازو بعد از تخته‌ها)
anchor = h.index('<g id="node_scaffold_bucket"')
clip = '<clipPath id="scf_pk"><rect x="-60" y="-140" width="60" height="160"/><rect x="0" y="-75" width="60" height="95"/></clipPath>'   # ستون چپ کامل از جلوی هر دو تخته؛ ستون راست از زیر تختهٔ بالا (سرِ آن زیر تختهٔ بالا می‌ماند)
grp = '<g clip-path="url(#scf_pk)">' + ''.join(navy) + ''.join(color) + '</g>'
h = h[:anchor] + clip + grp + h[anchor:]
h = h.replace('id="node_scaffold_hero"', 'id="node_scaffold_hero" data-postfix="1"', 1)
F.write_text(head + h, encoding='utf-8')
