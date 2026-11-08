#!/usr/bin/env python3
"""D218 (مالک ۸ نوامبر): «سایهٔ زیر توپ همراه توپ بالا و پایین می‌رود؛ توپ و دروازه می‌تواند کوچک‌تر باشد با همان مقیاس فانتزی».
۱) دروازه + تور + توپ (گروه hero) ۲۰٪ کوچک می‌شوند: مختصات مسیرها/چندضلعی‌ها/بیضی‌ها ضرب می‌شود، نه خود گروه؛ ضخامت خط‌ها دست نمی‌خورد
   (قاعدهٔ خط: لبهٔ بیرونی کلفت، مرز داخلی نازک؛ مقیاس‌کردن گروه خط را نازک‌تر می‌کرد).
۲) بیضی سایهٔ توپ از گروه توپ بیرون می‌آید (node_football_bshadow) تا فقط افقی همراه توپ برود و با چرخش توپ بالا و پایین نرود.
ورودی: out/node_football.svg اصلاح‌نشده؛ نشانگر data-fbs؛ دوباره اجرا نمی‌شود. خروجی football.json هم هماهنگ می‌شود."""
import re, json, pathlib
H = pathlib.Path(__file__).resolve().parent
F = H / 'out/node_football.svg'
s = F.read_text(encoding='utf-8')
if 'data-fbs' in s: raise SystemExit('done before')
S = 0.8
a = s.index('<g id="node_football_hero"')
# پایان گروه hero: شمارش g های تودرتو
i, depth = a, 0
for m in re.finditer(r'<g\b|</g>', s[a:]):
    depth += 1 if m.group(0) == '<g' else -1
    if depth == 0: b = a + m.end(); break
hero = s[a:b]
num = lambda m: ('%.1f' % (float(m.group(0)) * S)).rstrip('0').rstrip('.')
sc = lambda txt: re.sub(r'-?\d+\.?\d*', num, txt)
def fix_attr(mm):
    return mm.group(1) + '="' + sc(mm.group(2)) + '"'
hero = re.sub(r'\b(d|points)="([^"]*)"', fix_attr, hero)
hero = re.sub(r'\b(cx|cy|rx|ry)="(-?[\d.]+)"', lambda m: '%s="%s"' % (m.group(1), num(re.match(r'-?[\d.]+', m.group(2)))), hero)
# سایهٔ توپ را از گروه توپ بیرون بیاور
sh = re.search(r'<ellipse cx="[^"]*" cy="[^"]*" rx="[^"]*" ry="[^"]*" fill="#10083a" opacity="\.2"/>', hero)
assert sh, 'سایهٔ توپ پیدا نشد'
hero = hero.replace(sh.group(0), '', 1)
k = hero.index('<g id="node_football_ball">')
hero = hero[:k] + '<g id="node_football_bshadow">' + sh.group(0) + '</g>' + hero[k:]
s = s[:a] + hero + s[b:]
s = s.replace('data-linepass="1"', 'data-linepass="1" data-fbs="1"', 1)
F.write_text(s, encoding='utf-8')
J = H / 'out/football.json'; d = json.loads(J.read_text(encoding='utf-8'))
d['pad'][3] = round(d['pad'][3] * S, 1)
d['motion'] = ['node_football_ball', 'node_football_bshadow']
ms = d['motion_spec']['node_football_ball']
ms['pivot_symbol'] = [round(-14 * S, 1), round(-29 * S, 1)]; ms['translate_x_symbol_units'] = [round(-17 * S, 1), 0]
ms['note'] = 'دروازه و توپ ۰٫۸ اندازهٔ قبلی (D218)؛ سایهٔ توپ گروه جدا (node_football_bshadow) و فقط افقی همراه توپ می‌رود، نمی‌چرخد.'
d['motion_spec']['node_football_bshadow'] = {'kind': 'سایهٔ توپ؛ فقط جابه‌جایی افقی هم‌زمان با توپ', 'translate_x_symbol_units': [round(-36 * S, 1), 0], 'duration_s': 1.6, 'easing': 'ease-out', 'loop': False}
J.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
print('ok', len(hero))
