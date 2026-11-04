#!/usr/bin/env python3
"""D195: در node_loading_ramp.svg (ساخت کیت قدیمی) قهرمان داخل گروه سکو بود و روکش نور/سایهٔ سکو روی پایه‌های رمپ می‌افتاد (نوار کم‌رنگ روی ستون).
گروه سکو بعد از خط روشن سکو بسته می‌شود؛ نور و سایه بعد از آن و قهرمان در گروه _hero بعد از نور و سایه می‌آید (مثل بقیهٔ نمادها)."""
import pathlib, xml.etree.ElementTree as ET
NS = 'http://www.w3.org/2000/svg'; ET.register_namespace('', NS)
f = pathlib.Path(__file__).parent / 'out' / 'node_loading_ramp.svg'; s = f.read_text(encoding='utf-8')
if 'node_loading_ramp_hero' in s: raise SystemExit('already split')
root = ET.fromstring(s.replace('<symbol', '<symbol xmlns="%s"' % NS, 1))
q = lambda t: '{%s}%s' % (NS, t)
kids = list(root); byid = {k.get('id'): k for k in kids}
base = byid['node_loading_ramp_base']; ch = list(base)
k = next(i for i, e in enumerate(ch) if e.get('stroke') == '#8aa0bb') + 1   # تا خط روشن سکو
hero = ET.Element(q('g'), {'id': 'node_loading_ramp_hero', 'transform': base.get('transform')})
for e in ch[k:]: base.remove(e); hero.append(e)
shade = byid['node_loading_ramp_shade']; root.insert(list(root).index(shade) + 1, hero)
out = ET.tostring(root, encoding='unicode').replace(' xmlns="%s"' % NS, '', 1)
f.write_text(out, encoding='utf-8'); print('ok', [e.get('id') for e in root])
