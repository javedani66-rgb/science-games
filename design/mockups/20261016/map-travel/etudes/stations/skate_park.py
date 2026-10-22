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
RCX, RB = -34, -12                     # مرکز و کف رمپ
BD = (17, -15)                         # عمق تخته
BX, BY = 16, 24                       # مرکز و کف تخته
WR = 14


def ramp(p):
    cx, b = RCX, RB; top = b - 66; ac = (cx, b - 14 - 30)
    arc = [(ac[0] + 30 * math.cos(math.radians(a)), ac[1] + 30 * math.sin(math.radians(a))) for a in range(0, 181, 10)]
    inner = [(cx + 30, top)] + arc + [(cx - 30, top)]          # منحنی داخلی U از لبهٔ راست تا لبهٔ چپ
    add = lambda q: (q[0] + RD[0], q[1] + RD[1])
    outer = [(cx - 46, top), (cx - 46, b), (cx + 46, b), (cx + 46, top)]
    band = outer + inner
    p.tipshadow(cx, b + 4, 52)
    right = [(cx + 46, top), add((cx + 46, top)), add((cx + 46, b)), (cx + 46, b)]
    p.shape(right, C_R, PART, j=.1, step=6)
    rib = inner + [add(q) for q in inner[::-1]]
    p.shape(rib, C_I, PART, j=.1, step=6)
    mid = [(q[0] + RD[0] * .25, q[1] + RD[1] * .25) for q in arc[2:-2]] + [(q[0] + RD[0] * .7, q[1] + RD[1] * .7) for q in arc[2:-2][::-1]]
    p.fill(mid, C_FL)
    for x0, x1 in ((cx - 46, cx - 34), (cx + 34, cx + 46)):                                  # رویهٔ دیواره‌ها
        p.shape([(x0, top), (x1, top), (x1 + RD[0], top + RD[1]), (x0 + RD[0], top + RD[1])], C_T, PART, j=.1, step=6)
    p.shape(band, C_F, OUT, j=.15, step=7)
    p.fill([(cx - 42, top + 5), (cx - 36, top + 5), (cx - 36, b - 8), (cx - 42, b - 8)], C_T, .9)    # نور چپ
    p.fill([(cx + 36, top + 18), (cx + 42, top + 18), (cx + 42, b - 5), (cx + 36, b - 5)], C_R, .75)  # سایهٔ راست


def wheel(p, cx, cy, r, near=True):
    p.shape(ell(cx, cy, r, r, 0, 360, 36), W_Y, PART, j=.1, step=99, clip=False)
    if near:
        disc(p, cx, cy, 6.5, W_C)
        disc(p, cx + 9, cy - 3, 2.8, '#fff6c8')


def board(p):
    ox, oy = BX, BY
    P = lambda pts: [(ox + x, oy + y) for x, y in pts]
    fy, th = -38, 10
    FRONT = P([(-49, -47), (-45, -42), (-40, fy), (40, fy), (45, -42), (49, -47)])
    BACK = [(x + BD[0], y + BD[1]) for x, y in FRONT]
    SIDE = FRONT[:-1] + [(x, y + th) for x, y in FRONT[::-1]][1:]
    TOP = FRONT + BACK[::-1]
    for sx in (-28, 28):
        p.tipshadow(ox + sx, oy - 1, 17); p.foot_tip(ox + sx, oy - 2, 9)
    for sx in (-28, 28):                                              # چرخ‌های دور
        wheel(p, ox + sx + BD[0], oy - 14 + BD[1], 13, near=False)
    p.shape(SIDE, D_S, PART, j=0, step=6, clip=False)
    p.shape(TOP, D_T, PART, j=0, step=6)
    p.fill(P([(-36, fy - 3), (38, fy - 3), (42, fy - 7), (-32, fy - 7)]), D_L)                           # نور لبهٔ جلو
    m0, m1 = .38, .64
    p.fill(P([(-40 + BD[0] * m0, fy + BD[1] * m0), (40 + BD[0] * m0, fy + BD[1] * m0), (40 + BD[0] * m1, fy + BD[1] * m1), (-40 + BD[0] * m1, fy + BD[1] * m1)]), D_S)  # نوار آبی
    p.stroke(SIDE, PART, j=0, step=6)
    with layer(p, 'wheel_back'): wheel(p, ox - 28, oy - 14, WR)
    with layer(p, 'wheel'): wheel(p, ox + 28, oy - 14, WR)


def build():
    p = Pen('skate_park', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.0, 0, 0)
    ramp(p); board(p)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    mo = {'wheel': dict(rotate=p.X((BX + 28, BY - 14))), 'wheel_back': dict(rotate=p.X((BX - 28, BY - 14)))}
    r = finish(p, 'skate_park', STAND, motion=mo, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {
        'node_skate_park_wheel': dict(center=[round(v, 1) for v in p.X((BX + 28, BY - 14))], dir='cw', turns=1, duration_s=1.2, repeat=1, easing='ease-out', note='چرخ نزدیک راست؛ یک دور کامل هنگام رسیدن؛ حالت ایستا = پایان'),
        'node_skate_park_wheel_back': dict(center=[round(v, 1) for v in p.X((BX - 28, BY - 14))], dir='cw', turns=1, duration_s=1.2, repeat=1, easing='ease-out', note='چرخ نزدیک چپ؛ هم‌زمان؛ چرخ‌های دور ثابت'),
        'idle_loop': False, 'reduced_motion': 'چرخ‌ها ثابت'}
    (OUTD / 'skate_park.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')}, ensure_ascii=False))
