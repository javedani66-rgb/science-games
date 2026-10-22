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
from r6lib import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/skate_park'
C_F, C_T, C_R, C_I = '#b9c0cc', '#e3e8ef', '#7e8799', '#9aa3b4'
D_T, D_L, D_S = '#ff8a2b', '#ffc27a', '#2a5fc4'
W_Y, W_C = '#ffd84d', '#d9961c'
RD = (16, -10)                         # عمق رمپ
RB, RT = -2, -62                       # کف و لبهٔ بالای رمپ
BCX, BCY = 16, 6                        # مرکز تخته
TILT = -5                              # بالاآمدن دماغهٔ تخته (درجه)


def tf(pts, a=TILT, c=(BCX, BCY)):
    r = math.radians(a); ca, sa = math.cos(r), math.sin(r)
    return [(c[0] + x * ca - y * sa + 0, c[1] + x * sa + y * ca) for x, y in pts]


def ramp(p):
    R = 38
    arc = [(R * math.cos(math.radians(a)), RT + R * math.sin(math.radians(a))) for a in range(0, 181, 10)]
    pts = [(-46, RT), (-46, RB), (46, RB), (46, RT), (R, RT)] + arc + [(-R, RT)]
    pts = [(x * .8 - 26, y * .8 - 4) for x, y in pts]
    p.tipshadow(-30, RB + 3, 46)
    extrude(p, pts, RD, C_F, C_T, C_R, mid=C_I, sw=OUT, sw_in=PART)
    poly(p, [(-43, RT + 5), (-39, RT + 5), (-39, RB - 8), (-43, RB - 8)], C_T, .85)


def wheel(p, x, y, r=12, core=True):
    pts = tf(ell(x, y, r, r, 0, 360, 36))
    p.shape(pts, W_Y, PART, j=.05, step=99, clip=False)
    if core:
        cx, cy = tf([(x, y)])[0]
        circ(p, cx, cy, 4.5, W_C)


def board(p):
    deck = [(-46, -13), (-38, -3), (38, -3), (46, -13), (46, -6), (38, 5), (-38, 5), (-46, -6)]
    D = (16, -13)
    for sx in (-27, 27):
        wheel(p, sx + D[0] * .9, 12 + D[1] * .9, 12, core=False)               # چرخ‌های دور
    for sx in (-27, 27):
        p.tipshadow(BCX + sx, 27, 17)
    extrude(p, tf(deck), D, D_S, D_T, D_S, mid=D_L, sw=PART, sw_in=PART)
    st = [(-34, -3), (34, -3), (34 + D[0] * .22, -3 + D[1] * .22), (-34 + D[0] * .22, -3 + D[1] * .22)]
    poly(p, tf([(x + D[0] * .4, y + D[1] * .4) for x, y in st]), D_S, .0001)
    for sx in (-27, 27): wheel(p, sx, 13, 14)                                    # چرخ‌های نزدیک


def build():
    p = Pen('skate_park', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.0, -1, -3)
    ramp(p)
    with layer(p, 'skateboard'): board(p)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    mo = {'skateboard': dict(offsets=[p.V((-12, 3)), p.V((0, 0))])}
    r = finish(p, 'skate_park', STAND, motion=mo, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {
        'node_skate_park_skateboard': dict(from_offset_symbol=[-12, 3], to_offset=[0, 0], duration_s=0.9, repeat=1, easing='ease-out', note='تخته یک‌بار از چپ روی کف رمپ می‌لغزد و می‌ایستد؛ حالت ایستا = پایان؛ چرخ‌ها جزو همان لایه'),
        'idle_loop': False, 'reduced_motion': 'تخته ایستا'}
    (OUTD / 'skate_park.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')}, ensure_ascii=False))
