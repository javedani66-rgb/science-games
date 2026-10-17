#!/usr/bin/env python3
"""ایستگاه «بازارچهٔ شناور» (E06): قهرمان = یک غرفهٔ بازار روی یک قایق (سایبان راه‌راه، پیشخوان، میوه، پرچم)، سکوی دریایی.
لایهٔ متحرک node_floating_market_boat = کل قایق و غرفه که روی موج بالا و پایین می‌رود (dy در -3..+3)؛ زیرش سکوی دریایی (ثابت و کامل) است.
طراحی دوباره برای خط ضخیم‌تر (D113، D110): یک قایق، یک غرفه با سایبان سه‌نواری؛ نوارها و میوه‌ها فقط رنگ تخت (بدون خط دور)."""
import sys, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit2/after/floating_market'
XF = (1.0, 4.0, -3.0)            # قاب قهرمان: (مقیاس هندسه، dx، dy) در واحد symbol؛ ضخامت خط ثابت می‌ماند
HULL = '#c98a4a'; HULL_D = '#8a5a2a'; RED = '#ef6a4a'; WH = '#fff8e0'; WOOD = '#ffd84d'
ORG = '#ff9b2f'; GRN = '#8bd45a'
BOB = 3
X0, X1 = -58, -2                 # عرض غرفه


def boat(p):
    p.shape([(X0 - 2, 8), (X1 + 4, 8), (X1 - 6, 26), (X0 + 8, 26)], HULL, OUT, j=.25, step=4)
    p.ln((X0 + 14, 17), (X1 - 8, 17), INNER, HULL_D, j=.1, probe='خط داخلی (تختهٔ قایق)')
    # غرفه: جعبهٔ کرم با پیشخوان میوه
    p.shape([(X0 + 2, -22), (X1 - 2, -22), (X1 - 2, 8), (X0 + 2, 8)], WH, PART, j=.2, step=4)
    for x, c in ((X0 + 14, ORG), (X0 + 28, GRN), (X0 + 42, ORG)):
        mx, my = p.X((x, -3)); p.raw('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (mx, my, 5.5 * p.xf[0], c))
    # سایبان راه‌راه: سه نوار (رنگ تخت) با یک خط دور
    xs0 = [X0 - 4 + i * (X1 - X0 + 8) / 3 for i in range(4)]
    for i in range(3):
        p.fill([(xs0[i], -22), (xs0[i + 1], -22), (xs0[i + 1] - 2, -42), (xs0[i] + 2, -42)], RED if i != 1 else WH)
    p.stroke([(X0 - 4, -22), (X1 + 4, -22), (X1 + 2, -42), (X0 + 0, -42)], PART, j=.2, step=4)
    # پرچم
    p.ln(((X0 + X1) / 2, -42), ((X0 + X1) / 2, -62), PART, NAVY, j=.1)
    c = (X0 + X1) / 2
    p.fill([(c, -62), (c + 15, -56), (c, -50)], ORG)


def build(out=OUTD):
    p = Pen('floating_market', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-30, 22, 30); p.foot_tip(-30, 20, 12)
    with layer(p, 'boat'): boat(p)
    return p


STAND = None     # خودکار: find_stand

if __name__ == '__main__':
    p = build()
    offs = [p.V(o) for o in [(0, -BOB), (0, 0), (0, BOB)]]
    r = finish(p, 'floating_market', STAND, motion={'boat': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(offsets=offs, note='کل قایق و غرفه روی موج بالا و پایین؛ سکو ثابت؛ سایهٔ تماس ثابت')
    (OUTD / 'floating_market.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
