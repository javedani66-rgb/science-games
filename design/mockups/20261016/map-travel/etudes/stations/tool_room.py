#!/usr/bin/env python3
"""M06 «اتاق ابزار» (شهر) — دور ۹ (D155): میز کار چوبی واضح (رویهٔ ضخیم + چهار پایه + زیرکش) با چکش و آچار خوابیده روی رویه، کاملاً داخل رویه.
اشیا روی رویه به‌صورت نقشهٔ بالا (u،v) رسم و با نگاشت ¾ روی رویه می‌نشینند. لایهٔ متحرک node_tool_room_hammer = چکش؛ ایستا = پایان.
خط: دور ۲٫۶ تا ۳٫۶، بدون خط بین وجه‌ها؛ جزئیات ظریف."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from station_kit import *
from g4_helpers import *
from r6lib import extrude
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/tool_room'
W_F, W_T, W_S = '#e8b866', '#fbd990', '#b8843a'
L_F, L_T, L_S = '#d9a550', '#f0c780', '#9c6c2a'
S_F, S_T, S_S = '#c9d3e4', '#f6f9fd', '#7d8cab'
H_F, H_T, H_S = '#e2553d', '#ff9b84', '#9c2a1a'
Y_F = '#ffd84d'
TY = -30                         # لبهٔ جلوی رویه
D = (36, -36)
X0, X1 = -64, 60


def M(u, v):                     # نقشهٔ بالا ← صفحه
    return (X0 + u + D[0] * v, TY + D[1] * v)


def flat(p, plan, col, sw=2.2, lift=3):
    p.fill([(x, y + lift) for x, y in [M(*q) for q in plan]], '#7a5420', .9)         # ضخامت (سایهٔ پایین)
    p.shape([M(*q) for q in plan], col, sw, j=.05, step=6, clip=False)


def build():
    p = Pen('tool_room', 'city'); pad(p, line=((60, 24), (76, 20)), tri=((-74, 4), (-66, 20)), dot=(72, -10)); p.xf = (0.82, -1, 17)
    p.tipshadow(8, 14, 62); p.foot_tip(-40, 8, 12); p.foot_tip(40, 8, 12)
    # پایه‌ها (دو عقبی کوتاه‌تر دیده می‌شوند) و زیرکش
    for x0, x1 in ((X0 + 36, X0 + 46), (X1 - 30 + 8, X1 - 30 + 18)):
        extrude(p, rect(x0 + D[0] * .75, TY - 6, x1 + D[0] * .75, 2), (4, -3), L_F, L_T, L_S, sw=PART, sw_in=0)
    for x0, x1 in ((X0 + 4, X0 + 16), (X1 - 16, X1 - 4)):
        extrude(p, rect(x0, TY + 12, x1, 14), (7, -5), L_F, L_T, L_S, sw=OUT, sw_in=0)
    extrude(p, rect(X0 + 16, TY + 12, X1 - 16, TY + 22), (7, -5), L_F, L_T, L_S, sw=PART, sw_in=0)     # زیرکش
    # رویهٔ ضخیم
    extrude(p, rect(X0, TY, X1, TY + 12), D, W_F, W_T, W_S, sw=OUT, sw_in=0)
    p.ln((X0 + 6, TY + 6), (X1 - 6, TY + 6), 1.3, '#c48f3e', j=.05)
    # ابزارها: نمای کنار، خوابیده روی رویه، هرکدام در نیمهٔ خودش (بدون همپوشانی)
    Y0 = TY - 18                                                           # خط میانی عمق رویه
    with layer(p, 'hammer'):
        h = 11
        p.fill([(-26 + h, Y0 + 9), (3 + h, Y0 + 9), (3 + h, Y0 + 12), (-26 + h, Y0 + 12)], '#7a5420', .8)
        p.shape([(-26 + h, Y0 - 3), (3 + h, Y0 - 3), (3 + h, Y0 + 5), (-26 + h, Y0 + 5)], H_F, 2.6, j=.05, step=6, clip=False)
        p.shape([(-38 + h, Y0 - 12), (-22 + h, Y0 - 12), (-22 + h, Y0 + 11), (-38 + h, Y0 + 11)], S_F, 3.0, j=.05, step=6, clip=False)
        p.fill([(-35 + h, Y0 - 9), (-30 + h, Y0 - 9), (-30 + h, Y0 + 8), (-35 + h, Y0 + 8)], '#ffffff', .7)
        p.fill([(-16 + h, Y0 - 3), (-10 + h, Y0 - 3), (-10 + h, Y0 + 5), (-16 + h, Y0 + 5)], Y_F)
    wr = [(26, Y0 - 3), (46, Y0 - 3), (46, Y0 - 10), (62, Y0 - 10), (62, Y0 - 3), (55, Y0 - 3), (55, Y0 + 5), (62, Y0 + 5), (62, Y0 + 11), (46, Y0 + 11), (46, Y0 + 5), (26, Y0 + 5)]
    p.fill([(x, y + 3) for x, y in wr], '#7a5420', .8)
    p.shape(wr, S_F, 2.6, j=.05, step=6, clip=False)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'tool_room', STAND, motion={'hammer': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_tool_room_hammer': dict(kind='چکش خوابیده روی میز؛ یک‌بار کمی می‌چرخد (±۶° حول مرکز دسته) و برمی‌گردد؛ ایستا = پایان',
        pivot=[round(v, 1) for v in p.X((0, TY - 18))], rotate_deg=[0, 6, 0], dur_s=1.2, once=True, note='میز و آچار ثابت؛ بدون حلقهٔ بیکار.'), 'reduced_motion': 'ایستا'}
    (OUTD / 'tool_room.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')}, ensure_ascii=False)[:300])
