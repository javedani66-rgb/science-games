#!/usr/bin/env python3
"""ایستگاه B01 «داربست» (شهر، پالت city)، دور ۵ (فرمان مدیر: قاب پهن، ستون‌ها، تخته‌های افقی، ضربدر کامل، ۶۰٪، وسط).
طرح (واحد symbol، مرکز سکو x=0؛ کف y=8):
 ۱) دو پایهٔ عمودی کرم-سفید (x=±44، پهنا ۱۵، y=-112..8): پایه #f6f1e4 / روشن #ffffff / تیره #cfc4a8.
 ۲) دو کفشک (بلوک پایه) قهوه‌ای-خاکستری زیر پایه‌ها.
 ۳) ضربدر کامل قرمز مرجانی (#e2553d) در طبقهٔ پایین بین پایه‌ها، پشت پایه‌ها (سرها زیر پایه‌ها پنهان).
 ۴) تختهٔ میانی (سکوی کار) و تختهٔ بالایی، چوب قهوه‌ای #c98a4b / روشن #e8b27a / تیره #8f5a2c؛ x=±58 (≈۶۳٪ عرض سکو).
 ۵) شاقول (لایهٔ node_scaffold_plumb) در طبقهٔ بالا (بدون ضربدر) زیر تختهٔ بالا، محور x=0: ریسمان قهوه‌ای و وزنهٔ زرد؛ محور تاب = (0,-98).
 حرکت: شاقول ±۶° هنگام رسیدن، پایان = قائم؛ بدون حلقهٔ بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/scaffold'
S_B, S_L, S_D = '#f6f1e4', '#ffffff', '#cfc4a8'
W_B, W_L, W_D = '#c98a4b', '#e8b27a', '#8f5a2c'
R_B = '#e2553d'
FT = '#a08a70'; STR = '#5a3a1a'; YEL = '#ffd84d'
PX = (-44, 44); PW = 15; TOPY = -112; BASE = 8
PV = (0, -98)


def rect(p, x0, y0, x1, y1, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])), col))


def box(p, x0, y0, x1, y1, col, sw=PART):
    p.shape([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col, sw, j=.15, step=6)


def _bp(a, b, w):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); nx, ny = -dy / L * w / 2, dx / L * w / 2
    return [(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny), (b[0] - nx, b[1] - ny), (a[0] - nx, a[1] - ny)]


def braces(p, lst):
    for a, b, w in lst: p.shape(_bp(a, b, w), R_B, PART, j=.15, step=6, clip=False)
    for a, b, w in lst:
        p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(_bp(a, b, w - PART))), R_B))


def build(out=OUTD):
    p = Pen('scaffold', 'city'); pad(p, line=((-14, 36), (8, 36)), tri=((72, -14), (68, 14)), dot=(-74, -6)); p.xf = (1.0, 0, 0)
    p.tipshadow(0, BASE + 2, 56); p.foot_tip(0, BASE + 1, 44)
    # ۱) ضربدر کامل (پشت پایه‌ها)
    braces(p, [((-44, 0), (44, -52), 11), ((44, 0), (-44, -52), 11)])
    # ۲) کفشک‌ها + پایه‌ها
    for x in PX:
        box(p, x - 12, 1, x + 12, BASE + 1, FT)
        box(p, x - PW / 2, TOPY, x + PW / 2, 3, S_B)
        rect(p, x - PW / 2 + 3, TOPY + 10, x - PW / 2 + 6.5, -6, S_L)
        rect(p, x + 1.5, TOPY + 10, x + PW / 2 - 2.5, -6, S_D)
    # ۳) شاقول (زیر تختهٔ بالا)
    with layer(p, 'plumb'):
        p.ln((PV[0], -100), (PV[0], -84), INNER, STR, j=0, probe='ریسمان شاقول')
        p.shape([(PV[0] - 10, -86), (PV[0] + 10, -86), (PV[0], -64)], YEL, INNER, j=.1, step=99, clip=False)
    # ۴) تخته‌ها
    for y0, y1 in ((-60, -46), (-120, -106)):
        box(p, -58, y0, 58, y1, W_B)
        rect(p, -50, y0 + 3.5, 50, y0 + 7, W_L); rect(p, -50, y1 - 5.5, 50, y1 - 3, W_D)
    return p


if __name__ == '__main__':
    p = build()
    hm = p.X(PV)
    r = finish(p, 'scaffold', None, motion={'plumb': dict(offsets=[(0, 0), (-3, 0), (3, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_scaffold_plumb': dict(center=[round(v, 1) for v in hm], angles_deg=[0, 6, -6, 3, -1.5, 0], duration_s=2.8, repeat='یک‌بار',
        note='فقط شاقول از زیر تختهٔ بالا تاب می‌خورد و قائم می‌ایستد؛ داربست ثابت؛ حالت ایستا=قائم.'), 'reduced_motion': 'شاقول قائم'}
    (OUTD / 'scaffold.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
