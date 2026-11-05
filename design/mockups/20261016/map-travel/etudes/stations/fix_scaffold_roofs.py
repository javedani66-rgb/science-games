#!/usr/bin/env python3
"""D212 (مالک ۵ نوامبر): داربست دو طبقه با دو بادبند؛ «سقف اول و دوم منطقاً باید روی سر ستون‌ها بنشینند، هر دو هم‌اندازه و متقارن نسبت
به ستون‌ها، نه بیرون‌زده». تخته‌های (سقف‌های) هر دو طبقه از نو ساخته می‌شوند: روی ستون‌ها، ۳ واحد بیرون‌زدگی برابر چپ و راست، عمق کم
(۴٫۵ × ۲٫۸) تا از ستون راست بیرون نزند. ستون‌ها پشت سقف‌اند (سقف روی سرشان). خط: لبهٔ بیرونی کلفت (لایهٔ پشتی)، مرز با ستون نازک.
ورودی: out/node_scaffold.svg بدون اصلاح قبلی (data-roofs). فقط هندسه عوض می‌شود؛ دوباره اجرا نمی‌شود."""
import re, pathlib
F = pathlib.Path(__file__).resolve().parent / 'out/node_scaffold.svg'
s = F.read_text(encoding='utf-8')
if 'data-roofs' in s: raise SystemExit('done before')
XL, XR, D, E, H = -42.4, 35.6, 4.5, 5.0, 10.2
YT = {'low': -38.2, 'up': -87.8}
fmt = lambda pts: ' '.join('%.1f,%.1f' % p for p in pts)
def sil(yt): return [(XL, yt + H), (XR, yt + H), (XR + D, yt + H - E), (XR + D, yt - E), (XL + D, yt - E), (XL, yt)]
def path(pts): return 'M' + 'L'.join('%.1f,%.1f' % p for p in pts) + 'Z'
a = s.index('id="node_scaffold_hero"'); head, h = s[:a], s[a:]
n = 0
def fix(m):
    global n
    t = m.group(0); g = re.search(r'(points|d)="([^"]*)"', t)
    if not g: return t
    pts = [(float(x), float(y)) for x, y in re.findall(r'(-?\d+\.?\d*),(-?\d+\.?\d*)', g.group(2))]
    if not pts: return t
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    if not (min(ys) >= -100 and max(ys) <= -22): return t
    fill = re.search(r'fill="([^"]*)"', t); fill = fill.group(1).lower() if fill else ''
    w = max(xs) - min(xs); ht = max(ys) - min(ys)
    which = 'low' if max(ys) > -50 else 'up'; yt = YT[which]
    new = None
    if fill == '#241a5e' and w >= 80: new = ('d', path(sil(yt)))
    elif fill == '#f09a3a' and w >= 80: new = ('d', path(sil(yt)))
    elif fill == '#ffc983' and w >= 80: new = ('points', fmt([(XL, yt), (XR, yt), (XR + D, yt - E), (XL + D, yt - E)]))
    elif fill == '#b5621c' and 8 <= w <= 14 and ht > 12: new = ('points', fmt([(XR, yt), (XR + D, yt - E), (XR + D, yt + H - E), (XR, yt + H)]))
    elif fill == '#b5621c' and w > 50 and ht < 4: new = ('points', fmt([(XL + 2.7, yt + H - 3.7), (XR - 1.8, yt + H - 3.7), (XR - 1.8, yt + H - 1.4), (XL + 2.7, yt + H - 1.4)]))
    if not new: return t
    n += 1
    out = t.replace(g.group(0), '%s="%s"' % new)
    if t.startswith('<path') and new[0] == 'points': out = out.replace('<path', '<polygon', 1)
    if t.startswith('<polygon') and new[0] == 'd': out = out.replace('<polygon', '<path', 1)
    return out
h = re.sub(r'<(polygon|path)\b[^>]*/>', fix, h)
h = h.replace('id="node_scaffold_hero"', 'id="node_scaffold_hero" data-roofs="1"', 1)
F.write_text(head + h, encoding='utf-8'); print('rewritten', n, '(باید ۱۰ باشد)')
