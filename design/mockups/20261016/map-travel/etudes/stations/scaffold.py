#!/usr/bin/env python3
"""ایستگاه B01 «داربست» (شهر). طرح قطعه‌به‌قطعه (واحد symbol، مرکز سکو (0,0)):
 ۱) دو پایهٔ عمودی لوله‌ای نقره‌ای (x=-46 و -6، پهنا ۱۴، از y=-100 تا ۷)، سه پله: #d5dde6 / روشن #f4f7fa / تیره #9aa8ba.
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
S_B, S_L, S_D = '#d5dde6', '#f4f7fa', '#9aa8ba'
W_B, W_L, W_D = '#f0cf86', '#fbe8b8', '#c99a4a'
R_B, R_L, R_D = '#e2553d', '#ff9b84', '#a83420'
FT = '#7d8794'; STR = '#7a4a1f'; YEL = '#ffd84d'; YEL_L = '#fff2a8'
PX = (-46, -6); PW = 14; TOPY = -100; BASE = 7
DK = ((-58, -44, 4, -34), (-58, -84, 4, -74))
BAR = (-53, -106, 30, -94)
PV = (20, -94); BOB_Y = (-20, 4)


def rect(p, x0, y0, x1, y1, col):
    p.fill([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col)


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def box(p, x0, y0, x1, y1, col):
    p.shape([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col, PART, j=.2, step=6)


def brace(p, a, b, w=14):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); nx, ny = -dy / L * w / 2, dx / L * w / 2
    p.shape([(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny), (b[0] - nx, b[1] - ny), (a[0] - nx, a[1] - ny)], R_B, PART, j=.2, step=6)


def build(out=OUTD):
    p = Pen('scaffold', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.0, 0, 0)
    for x in PX + (20,): pass
    p.tipshadow(-26, BASE + 3, 40); p.foot_tip(-26, BASE + 2, 26)
    # ۱) کفشک‌ها
    for x in PX: box(p, x - 12, -1, x + 12, BASE, FT)
    # ۲) ضربدرها (پشت پایه‌ها)
    for ya, yb in ((-2, -34), (-44, -74)):
        brace(p, (-43, ya - 2 if ya == -2 else ya), (-9, yb), 12)
        brace(p, (-9, ya if ya != -2 else ya - 2), (-43, yb), 12)
    # ۳) پایه‌ها
    for x in PX:
        box(p, x - PW / 2, TOPY, x + PW / 2, BASE - 5, S_B)
        rect(p, x - PW / 2 + 3, TOPY + 5, x - PW / 2 + 6.5, BASE - 9, S_L)
        rect(p, x + 1.5, TOPY + 5, x + PW / 2 - 2.5, BASE - 9, S_D)
    # ۴) تخته‌ها
    for x0, y0, x1, y1 in DK:
        box(p, x0, y0, x1, y1, W_B)
        rect(p, x0 + 4, y0 + 3, x1 - 4, y0 + 5.5, W_L); rect(p, x0 + 4, y1 - 4.5, x1 - 4, y1 - 2.5, W_D)
    # ۵) تیرک بالا
    x0, y0, x1, y1 = BAR
    box(p, x0, y0, x1, y1, S_B)
    rect(p, x0 + 4, y0 + 3, x1 - 4, y0 + 5.5, S_L); rect(p, x0 + 4, y1 - 4.5, x1 - 4, y1 - 2.5, S_D)
    # ۶) شاقول
    with layer(p, 'plumb'):
        p.ln((PV[0], PV[1]), (PV[0], BOB_Y[0] + 1), INNER, STR, j=0, probe='ریسمان شاقول')
        p.shape([(PV[0], BOB_Y[0]), (PV[0] + 8, -8), (PV[0], BOB_Y[1]), (PV[0] - 8, -8)], YEL, PART, j=.1, step=6, clip=False)
        p.fill([(PV[0] - 3.5, -9), (PV[0] - 1, -13), (PV[0] - 1, -8)], YEL_L)
    disc(p, PV[0], PV[1] + 6, 2.2, STR)   # بست ریسمان زیر تیرک (ثابت)
    return p


if __name__ == '__main__':
    p = build()
    hm = p.X(PV)
    r = finish(p, 'scaffold', None, motion={'plumb': dict(rotate=hm)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_scaffold_plumb': dict(center=[round(v, 1) for v in hm], angles_deg=[0, 6, -6, 3, -1.5, 0], duration_s=2.8, repeat='یک‌بار',
        note='فقط شاقول از نقطهٔ تیرک تاب می‌خورد و قائم می‌ایستد؛ داربست و تخته ثابت؛ حالت ایستا=قائم.'), 'reduced_motion': 'شاقول قائم'}
    (OUTD / 'scaffold.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
