#!/usr/bin/env python3
"""B01 «داربست» (سکوی city) — دور ۶ (R6): داربست لوله‌ای ¾، دو طبقه، دو سکوی تخته‌ای، نردبان، سطل آویزان با قرقره.
طرح (واحد symbol، مرکز سکو x=0، کف y=6):
 ۱ دو پایهٔ لوله‌ای (x=-40 و +24، پهنا ۱۴، y 6..-114): سه پله کرم/سفید/خاکستری-آبی (#e9edf3 / #ffffff / #a9b4c8)، کفشک تیره.
 ۲ دو ضربدر لوله‌ای (پهنا ۹، #b6c2d6) در دو طبقه، پشت پایه‌ها.
 ۳ دو سکوی تخته‌ای ¾ نارنجی (#f09a3a / #ffc983 / #b5621c): رو + رویه + وجه راست؛ طبقهٔ پایین y=-48 و بالا y=-102.
 ۴ نردبان چوبی روشن سمت راست (x=42..60) با ۴ پله.
 ۵ بازوی بالا + قرقره (چرخ خاکستری) بالای راست؛ سطل قرمز (لایهٔ node_scaffold_bucket: ریسمان+سطل+دسته) آویزان زیر قرقره، چپ داربست.
حرکت: سطل حول قرقره ±۶° تاب می‌خورد و قائم می‌ایستد (یک‌بار)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from station_kit import *
from g6h import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/scaffold'
T_B, T_L, T_D = '#e9edf3', '#ffffff', '#a9b4c8'
BR = '#b6c2d6'
P_B, P_L, P_D = '#f09a3a', '#ffc983', '#b5621c'
L_B = '#f3cf86'; STR = '#6e3f18'; RED, RED_L, RED_D = '#e2402e', '#ff8f7a', '#a42418'
FT = '#6f7c93'
BASE = 6; PXs = (-40, 24); PW = 14; TOPY = -100
PV = (-68, -127)


def plank(p, x0, x1, y, h=11, D=12, E=7):
    sil = [(x0, y + h), (x1, y + h), (x1 + D, y + h - E), (x1 + D, y - E), (x0 + D, y - E), (x0, y)]
    p.shape(sil, P_B, PART, j=.1, step=7)
    poly(p, [(x0, y), (x1, y), (x1 + D, y - E), (x0 + D, y - E)], P_L)
    poly(p, [(x1, y), (x1 + D, y - E), (x1 + D, y + h - E), (x1, y + h)], P_D)
    poly(p, R(x0 + 3, y + h - 4, x1 - 2, y + h - 1.5), P_D, .9)


def build():
    p = Pen('scaffold', 'city'); pad(p, line=((-14, 36), (8, 36)), tri=((72, -14), (68, 14)), dot=(-74, -6)); p.xf = (0.92, 4, 6)
    p.tipshadow(-4, BASE + 3, 62); p.foot_tip(-40, BASE + 1, 14); p.foot_tip(24, BASE + 1, 14); p.foot_tip(52, BASE + 1, 12)
    # ۲ ضربدرها (پشت)
    for y0, y1 in ((BASE - 2, -48), (-56, -100)):
        for a, b in (((-40, y0), (24, y1)), ((24, y0), (-40, y1))):
            p.shape(bar(a, b, 10), BR, 3.2, j=.15, step=7, clip=False)
        for a, b in (((-40, y0), (24, y1)), ((24, y0), (-40, y1))):
            poly(p, bar(a, b, 4.2), '#d8e0ee', .9)
    # ۱ پایه‌ها
    for x in PXs:
        p.shape(R(x - 12, BASE - 6, x + 12, BASE + 1), FT, PART, j=.12, step=6)
        p.shape(R(x - PW / 2, TOPY, x + PW / 2, BASE - 4), T_B, PART, j=.12, step=7)
        poly(p, R(x - PW / 2 + 2.5, TOPY + 6, x - PW / 2 + 5.5, BASE - 8), T_L)
        poly(p, R(x + 1.5, TOPY + 4, x + PW / 2 - 2, BASE - 8), T_D)
    # ۴ نردبان
    for y in (-72, -52, -32, -12): p.ln((45, y), (63, y), 3.4, STR, j=.1)
    for x in (45, 63): p.shape(R(x - 2.8, -86, x + 2.8, BASE), L_B, 3, j=.1, step=7, clip=False)
    # ۳ تخته‌ها
    plank(p, -52, 30, -48); plank(p, -52, 30, -102)
    # ۵ بازو + قرقره + سطل
    p.shape(R(-70, -132, -30, -121), T_B, PART, j=.1, step=7, clip=False)
    poly(p, R(-66, -130, -33, -127.5), T_L)
    with layer(p, 'bucket'):
        p.ln((PV[0], PV[1] + 4), (PV[0], -70), 3, STR, j=0)
        p.ln((PV[0] - 10, -62), (PV[0], -70), 3, STR, j=0); p.ln((PV[0] + 10, -62), (PV[0], -70), 3, STR, j=0)
        b = [(PV[0] - 12, -62), (PV[0] + 12, -62), (PV[0] + 9, -34), (PV[0] - 9, -34)]
        p.shape(b, RED, PART, j=.1, step=6, clip=False)
        poly(p, [(PV[0] + 3, -60), (PV[0] + 11, -60), (PV[0] + 8, -36), (PV[0] + 3, -36)], RED_D)
        poly(p, R(PV[0] - 9, -59, PV[0] - 6, -39), RED_L)
        p.shape(R(PV[0] - 15, -66, PV[0] + 15, -60), RED_L, 3, j=.1, step=6, clip=False)
    p.shape(ell(PV[0], PV[1], 9, 9, 0, 360, 18), '#d8e0ee', PART, j=.1, step=6, clip=False); disc(p, PV[0], PV[1], 2.6, NAVY)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    hm = p.X(PV)
    r = finish(p, 'scaffold', STAND, motion={'bucket': dict(offsets=[(-3, 0), (3, 0), (0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_scaffold_bucket': dict(center=[round(v, 1) for v in hm], angles_deg=[0, 6, -6, 3, -1.5, 0], duration_s=2.8, repeat='یک‌بار',
        note='فقط سطل با ریسمان حول قرقره تاب می‌خورد و قائم می‌ایستد؛ داربست ثابت؛ حالت ایستا=قائم.'), 'reduced_motion': 'سطل قائم'}
    (OUTD / 'scaffold.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
