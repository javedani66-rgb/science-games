#!/usr/bin/env python3
"""ایستگاه B01 «داربست» (شهر). طرح قطعه‌به‌قطعه (واحد symbol، مرکز سکو (0,0)):
 (بازنگری: شاقول داخل چارچوب زیر تیرک کوتاه، X کامل پایین) ۱) دو پایهٔ عمودی لوله‌ای نقره‌ای (x=-46 و -6، پهنا ۱۴، از y=-100 تا ۷)، سه پله: #d5dde6 / روشن #f4f7fa / تیره #9aa8ba.
 ۲) دو کفشک (بلوک پایه) خاکستری تیره زیر هر پایه.
 ۳) ضربدر قرمز مرجانی (#e2553d) در دو طاق بین پایه‌ها (پشت پایه‌ها؛ سرها زیر پایه پنهان = اتصال تمیز).
 ۴) دو تختهٔ چوبی روشن (#f0cf86) در y=-44..-34 و y=-84..-74، همپوشان با پایه‌ها.
 ۵) تیرک افقی بالا (نقره‌ای) از x=-53 تا 30 که شاقول را نگه می‌دارد.
 ۶) شاقول (لایهٔ متحرک node_scaffold_plumb): ریسمان قهوه‌ای x=20 و وزنهٔ زرد لوزی؛ محور تاب = (20,-94).
 پالت: city. حرکت: ±۶° هنگام رسیدن، پایان = قائم؛ بدون حلقهٔ بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/scaffold'
S_B, S_L, S_D = '#c3cfdc', '#f6f9fc', '#8a98ac'
W_B, W_L, W_D = '#f0cf86', '#fbe8b8', '#c99a4a'
R_B, R_L, R_D = '#e2553d', '#ff9b84', '#a83420'
FT = '#7d8794'; STR = '#7a4a1f'; YEL = '#ffd84d'; YEL_L = '#fff2a8'
PX = (-48, 0); PW = 15; TOPY = -118; BASE = 7
DK = ((-57, -40, 12, -26), (-57, -78, 12, -64))
BAR = (-56, -126, 8, -110)
PV = (-24, -112)


def rect(p, x0, y0, x1, y1, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])), col))


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def box(p, x0, y0, x1, y1, col):
    p.shape([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col, PART, j=.2, step=6)


def _bp(a, b, w):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); nx, ny = -dy / L * w / 2, dx / L * w / 2
    return [(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny), (b[0] - nx, b[1] - ny), (a[0] - nx, a[1] - ny)]


def braces(p, lst):
    """همهٔ مورب‌ها اول با خط دور، بعد رنگ تخت درون‌نشین روی همه: ضربدر تمیز بدون تکه‌تکه شدن."""
    for a, b, w in lst: p.shape(_bp(a, b, w), R_B, PART, j=.2, step=6)
    for a, b, w in lst:
        p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(_bp(a, b, w - PART))), R_B))


def build(out=OUTD):
    p = Pen('scaffold', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((62, -24), (66, 10)), dot=(74, -8)); p.xf = (0.92, -12, 5)
    p.tipshadow(-24, BASE + 3, 36); p.foot_tip(-24, BASE + 2, 24)
    # ۱) مهاربندها (پشت پایه‌ها): X کامل در طبقهٔ پایین، یک مورب در طبقهٔ میانی
    braces(p, [((-48, 1), (0, -24), 14), ((0, 1), (-48, -24), 14)])
    braces(p, [((0, -42), (-48, -62), 16)])
    # ۲) پایه‌ها
    for x in PX:
        box(p, x - PW / 2, TOPY, x + PW / 2, BASE, S_B)
        rect(p, x - PW / 2 + 3, TOPY + 5, x - PW / 2 + 6.5, BASE - 6, S_L)
        rect(p, x + 1.5, TOPY + 5, x + PW / 2 - 2.5, BASE - 6, S_D)
    # ۳) تخته‌ها
    for x0, y0, x1, y1 in DK:
        box(p, x0, y0, x1, y1, W_B)
        rect(p, x0 + 4, y0 + 3, x1 - 4, y0 + 6, W_L); rect(p, x0 + 4, y1 - 5, x1 - 4, y1 - 3, W_D)
    # ۵) سایهٔ تماس شاقول روی تختهٔ بالا
    p.raw('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#10083a" opacity=".22"/>' % (p.X((PV[0], -73))[0], p.X((PV[0], -73))[1], 6, 1.8))
    # ۶) شاقول داخل چارچوب
    with layer(p, 'plumb'):
        p.ln((PV[0], -112), (PV[0], -95), INNER, STR, j=0, probe='ریسمان شاقول')
        p.shape([(PV[0] - 7.5, -97), (PV[0] + 7.5, -97), (PV[0], -85)], YEL, INNER, j=.1, step=99, clip=False)
    # ۴) تیرک بالا (کوتاه، تا کنار لولهٔ راست)
    x0, y0, x1, y1 = BAR
    box(p, x0, y0, x1, y1, S_B)
    rect(p, x0 + 4, y0 + 3, x1 - 4, y0 + 6, S_L); rect(p, x0 + 4, y1 - 5, x1 - 4, y1 - 3, S_D)
    return p


if __name__ == '__main__':
    p = build()
    hm = p.X(PV)
    r = finish(p, 'scaffold', None, motion={'plumb': dict(offsets=[(0, 0), (-3, 0), (3, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_scaffold_plumb': dict(center=[round(v, 1) for v in hm], angles_deg=[0, 6, -6, 3, -1.5, 0], duration_s=2.8, repeat='یک‌بار',
        note='فقط شاقول از نقطهٔ تیرک تاب می‌خورد و قائم می‌ایستد؛ داربست و تخته ثابت؛ حالت ایستا=قائم.'), 'reduced_motion': 'شاقول قائم'}
    (OUTD / 'scaffold.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
