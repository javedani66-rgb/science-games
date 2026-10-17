#!/usr/bin/env python3
"""ایستگاه «بازارچهٔ شناور» (E06): قهرمان = یک غرفهٔ بازار روی یک قایق (سایبان راه‌راه، پیشخوان، میوه، جعبه، پرچم)، سکوی دریایی.
لایهٔ متحرک node_floating_market_boat = کل قایق و غرفه که روی موج بالا و پایین می‌رود (dy در -3..+3)؛
زیرش سکوی دریایی (ثابت و کامل) است. اتود الف: دو قایق بسته به هم (رد شد: شلوغ‌تر و پهن‌تر)."""
import sys, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/batch2/floating_market'
HULL = '#c98a4a'; HULL_D = '#8a5a2a'; RED = '#ef6a4a'; WH = '#fff8e0'; WOOD = '#ffd84d'
ORG = '#ff9b2f'; GRN = '#8bd45a'; BLU = '#5fa8f0'
BOB = 3


def boat(p):
    # بدنهٔ قایق (ذوزنقه)، یک خط روشن
    p.shape([(-58, 8), (26, 8), (14, 26), (-46, 26)], HULL, OUT, j=.25, step=4)
    p.ln((-40, 18), (6, 18), INNER, HULL_D, j=.1, probe='خط داخلی (تختهٔ قایق)')
    # دو ستون غرفه
    for x in (-42, 10):
        p.shape([(x - 3, -34), (x + 3, -34), (x + 3, 8), (x - 3, 8)], WOOD, PART, j=.15, step=4)
    # پیشخوان
    p.shape([(-46, -4), (14, -4), (14, 8), (-46, 8)], WH, PART, j=.2, step=4)
    # میوه روی پیشخوان
    for x, c in ((-30, ORG), (-16, GRN), (-2, ORG)):
        p.shape(ell(x, -10, 6, 6, 0, 360, 16), c, INNER, j=.1, step=99, clip=False)
    # جعبهٔ میوه کنار غرفه
    p.shape([(16, -8), (36, -8), (36, 8), (16, 8)], BLU, PART, j=.15, step=4)
    p.shape(ell(26, -10, 5, 5, 0, 360, 14), RED, INNER, j=.1, step=99, clip=False)
    # سایبان راه‌راه: چهار نوار
    xs = [-52, -36, -20, -4, 12]; xt = [-46, -32, -18, -4, 10]
    for i in range(4):
        p.shape([(xt[i], -50), (xt[i + 1], -50), (xs[i + 1] + 4, -34), (xs[i] + 4, -34)], RED if i % 2 == 0 else WH, PART if i == 0 else INNER, j=.15, step=4, clip=False)
    p.shape([(-47, -50), (11, -50), (15, -34), (-52 + 4, -34)], 'none', PART, j=.15, step=4, clip=False) if False else None
    # پرچم
    p.ln((-18, -50), (-18, -68), INNER, NAVY, j=.1)
    p.shape([(-18, -68), (-4, -63), (-18, -57)], ORG, INNER, j=.1, step=4, clip=False)


def build(out=OUTD):
    p = Pen('floating_market', 'sea'); pad(p, line=((34, 24), (52, 19)), tri=((-62, -14), (62, 16)), dot=(42, -26))
    p.tipshadow(-16, 22, 30); p.foot_tip(-16, 20, 16)
    with layer(p, 'boat'): boat(p)
    return p

STAND = (40, -2)

if __name__ == '__main__':
    p = build()
    offs = [(0, -BOB), (0, 0), (0, BOB)]
    r = finish(p, 'floating_market', STAND, motion={'boat': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(offsets=offs, note='کل قایق و غرفه روی موج بالا و پایین؛ سکو ثابت؛ سایهٔ تماس ثابت')
    (OUTD / 'floating_market.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False, indent=1))
