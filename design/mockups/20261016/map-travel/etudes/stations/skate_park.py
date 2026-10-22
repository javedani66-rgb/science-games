#!/usr/bin/env python3
"""F09 «زمین اسکیت» (سکوی sports، رنگ‌مایهٔ ۹۳°) — دور ۶ بازطراحی (هم‌سطح پیچ‌کاری).
قهرمان: اسکیت‌بردِ درشت ¾ جلو-راست + رمپ U بتنی خاکستری پشت-چپ. ≈۹۰٪ عرض سکو، ۵ جزء درشت.
طرح قطعه‌به‌قطعه (واحد symbol، عمق ¾ D):
 ۱) رمپ U (۱۰۰×۵۸، دیواره ۱۶، کف ۱۲، شعاع داخلی ۳۴): نوار جلویی U (بتن #b9c0cc)، رویهٔ دیواره‌ها (روشن #e3e8ef)، وجه راست (تیره #7e8799)،
    سطح داخلی کشیده‌شده (#9aa3b4، نوار روشن‌تر #cfd5df روی کف).
 ۲) تختهٔ اسکیت: رویهٔ نارنجی #ff8a2b با نوار آبی #2f6fd8 و نوار روشن، کنارهٔ آبی تیره، دو سر بالاآمده.
 ۳) چهار چرخ زرد #ffd84d (r13، دور PART) با هستهٔ کهربایی و نقطهٔ نشانهٔ چرخش؛ دو چرخ دور (کمی کوچک‌تر، ثابت)، دو چرخ نزدیک متحرک.
لایه‌های متحرک: node_skate_park_wheel (نزدیک راست) و node_skate_park_wheel_back (نزدیک چپ)؛ حالت ایستا = پایان؛ بدون حلقهٔ بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from station_kit import *
from r6_helpers import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/skate_park'
C_F, C_T, C_R, C_I, C_FL = '#b9c0cc', '#e3e8ef', '#7e8799', '#9aa3b4', '#cfd5df'
D_T, D_L, D_S = '#ff8a2b', '#ffc27a', '#2a5fc4'
W_Y, W_C = '#ffd84d', '#d9961c'
RD = (20, -12)                        # عمق رمپ
RCX, RB = -32, -6                     # مرکز و کف رمپ
BD = (11, -9)                         # عمق تخته
BX, BY = 20, 22                       # مرکز و کف تخته
WR = 13


def ramp(p):
    cx, b = RCX, RB; top = b - 58; ac = (cx, b - 12 - 34)
    arc = [(ac[0] + 34 * math.cos(math.radians(a)), ac[1] + 34 * math.sin(math.radians(a))) for a in range(0, 181, 10)]
    inner = [(cx + 34, top)] + arc + [(cx - 34, top)]          # منحنی داخلی U از لبهٔ راست تا لبهٔ چپ
    add = lambda q: (q[0] + RD[0], q[1] + RD[1])
    outer = [(cx - 50, top), (cx - 50, b), (cx + 50, b), (cx + 50, top)]
    band = outer + inner
    p.tipshadow(cx, b + 4, 52)
    right = [(cx + 50, top), add((cx + 50, top)), add((cx + 50, b)), (cx + 50, b)]
    p.shape(right, C_R, PART, j=.1, step=6)
    rib = inner + [add(q) for q in inner[::-1]]
    p.shape(rib, C_I, PART, j=.1, step=6)
    mid = [(q[0] + RD[0] * .25, q[1] + RD[1] * .25) for q in arc[2:-2]] + [(q[0] + RD[0] * .7, q[1] + RD[1] * .7) for q in arc[2:-2][::-1]]
    p.fill(mid, C_FL)
    for x0, x1 in ((cx - 50, cx - 34), (cx + 34, cx + 50)):                                  # رویهٔ دیواره‌ها
        p.shape([(x0, top), (x1, top), (x1 + RD[0], top + RD[1]), (x0 + RD[0], top + RD[1])], C_T, PART, j=.1, step=6)
    p.shape(band, C_F, OUT, j=.15, step=7)
    p.fill([(cx - 46, top + 5), (cx - 40, top + 5), (cx - 40, b - 8), (cx - 46, b - 8)], C_T, .9)    # نور چپ
    p.fill([(cx + 40, top + 18), (cx + 46, top + 18), (cx + 46, b - 5), (cx + 40, b - 5)], C_R, .75)  # سایهٔ راست


def wheel(p, cx, cy, r, near=True):
    p.shape(ell(cx, cy, r, r, 0, 360, 36), W_Y, PART, j=.1, step=99, clip=False)
    if near:
        disc(p, cx, cy, 6, W_C)
        disc(p, cx + 8.4, cy - 3, 2.6, '#fff6c8')


def board(p):
    ox, oy = BX, BY
    P = lambda pts: [(ox + x, oy + y) for x, y in pts]
    fy, th = -37, 9
    FRONT = P([(-60, -50), (-56, -42), (-50, fy), (50, fy), (56, -42), (60, -50)])
    BACK = [(x + BD[0], y + BD[1]) for x, y in FRONT]
    SIDE = FRONT[:-1] + [(x, y + th) for x, y in FRONT[::-1]][1:]
    TOP = FRONT + BACK[::-1]
    for sx in (-34, 34):
        p.tipshadow(ox + sx, oy - 1, 17); p.foot_tip(ox + sx, oy - 2, 9)
    for sx in (-34, 34):                                              # چرخ‌های دور
        wheel(p, ox + sx + BD[0], oy - 13 + BD[1], 12, near=False)
    p.shape(SIDE, D_S, PART, j=0, step=6, clip=False)
    p.shape(TOP, D_T, PART, j=0, step=6)
    p.fill(P([(-44, fy - 3), (46, fy - 3), (50, fy - 6.5), (-40, fy - 6.5)]), D_L)                           # نور لبهٔ جلو
    m0, m1 = .38, .64
    p.fill(P([(-50 + BD[0] * m0, fy + BD[1] * m0), (50 + BD[0] * m0, fy + BD[1] * m0), (50 + BD[0] * m1, fy + BD[1] * m1), (-50 + BD[0] * m1, fy + BD[1] * m1)]), D_S)  # نوار آبی
    p.stroke(SIDE, PART, j=0, step=6)
    with layer(p, 'wheel_back'): wheel(p, ox - 34, oy - 13, WR)
    with layer(p, 'wheel'): wheel(p, ox + 34, oy - 13, WR)


def build():
    p = Pen('skate_park', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.0, 0, 0)
    ramp(p); board(p)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    mo = {'wheel': dict(rotate=p.X((BX + 34, BY - 13))), 'wheel_back': dict(rotate=p.X((BX - 34, BY - 13)))}
    r = finish(p, 'skate_park', STAND, motion=mo, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {
        'node_skate_park_wheel': dict(center=[round(v, 1) for v in p.X((BX + 34, BY - 13))], dir='cw', turns=1, duration_s=1.2, repeat=1, easing='ease-out', note='چرخ نزدیک راست؛ یک دور کامل هنگام رسیدن؛ حالت ایستا = پایان'),
        'node_skate_park_wheel_back': dict(center=[round(v, 1) for v in p.X((BX - 34, BY - 13))], dir='cw', turns=1, duration_s=1.2, repeat=1, easing='ease-out', note='چرخ نزدیک چپ؛ هم‌زمان؛ چرخ‌های دور ثابت'),
        'idle_loop': False, 'reduced_motion': 'چرخ‌ها ثابت'}
    (OUTD / 'skate_park.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')}, ensure_ascii=False))
