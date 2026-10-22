#!/usr/bin/env python3
"""ایستگاه F09 «زمین اسکیت» (سکوی 'sports' سبز، رنگ‌مایه ۹۳°) — دور ۵ (فرمان مدیر هنری).
قهرمان: اسکیت‌برد بزرگ، نمای سه‌چهارم (عمق D=(18,-11))، وسط سکو، ≈۶۰٪ عرض سکو.
طرح قطعه‌به‌قطعه (واحد symbol، زمین y=6، مرکز سکو (0,0)، xf=(1,dx,0) برای وسط‌کردن):
 ۱) سایهٔ تماس زیر چهار چرخ.
 ۲) دو چرخ دور (کمی کوچک‌تر، کرم تیره #d9c27a، PART) = پشت تخته؛ چرخ نزدیک آن‌ها را نیمه می‌پوشاند.
 ۳) کنارهٔ تخته (ضخامت ۹، فیروزه‌ای تیره #1a8696، OUT) با دو سر بالاآمده (دماغه راست بلندتر).
 ۴) روی تخته: متوازی‌الاضلاع فیروزه‌ای #2cb5c6 (OUT)، نوار روشن #8fe8ee، نوار مرجانی #ff6f61 وسط (رنگ تخت).
 ۵) دو محور فلزی (#dbe9f8/#a3bbd9، INNER) زیر کنارهٔ تخته به مرکز چرخ نزدیک.
 ۶) دو چرخ نزدیک r=11 کرم #fff1c0 با دور PART، هستهٔ تیره + نقطهٔ زرد (نشانهٔ چرخش).
لایه‌های متحرک: node_skate_park_wheel (چرخ نزدیک راست)، node_skate_park_wheel_back (چرخ نزدیک چپ)؛ چرخ‌های دور ثابت.
حالت ایستا = پایان. بدون حلقهٔ بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/skate_park'

D_B, D_L, D_D = '#2cb5c6', '#8fe8ee', '#1a8696'
M_B, M_D = '#dbe9f8', '#a3bbd9'
W_B, W_FAR = '#fff1c0', '#d9c27a'
HUBC = '#7a4a1f'; YEL = '#ffd84d'; COR = '#ff6f61'
GY = 6
DX = (13, -8)
R, RF = 12, 11
WYC = -8
NEAR = (-34, 26)
DXC = 0
FY, TH, DD = -32, 9, (10, -12)
FRONT = [(-51, -44), (-48, -37), (-42, FY), (34, FY), (40, FY - 5), (45, FY - 10)]
BACK = [(x + DD[0], y + DD[1]) for x, y in FRONT]
TOP = FRONT + BACK[::-1]
SIDE = FRONT[:-1] + [(x, y + TH) for x, y in FRONT[::-1]][1:]
DECK = TOP


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def wheel(p, cx, cy, r, base, hub=True):
    p.shape(ell(cx, cy, r, r, 0, 360, 40), base, PART, j=.1, step=99, clip=False)
    if hub:
        poly(p, [(cx - 4, cy - 2), (cx + 4, cy - 2), (cx + 4, cy + 2), (cx - 4, cy + 2)], HUBC)
        a, b = p.X((cx, cy)); p.raw('<circle cx="%.1f" cy="%.1f" r="2.2" fill="%s"/>' % (a, b, YEL))


def build(out=None):
    p = Pen('skate_park', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.0, DXC, 0)
    for cx in NEAR:
        p.tipshadow(cx, GY - 1, 15); p.foot_tip(cx, GY - 2, 8)
        p.tipshadow(cx + DX[0], GY - 9, 12)
    for cx in NEAR: wheel(p, cx + DX[0], WYC + DX[1], RF, W_FAR, hub=False)
    for cx in NEAR:
        t = [(cx - 8, FY + 6), (cx + 8, FY + 6), (cx + 6, WYC), (cx - 6, WYC)]
        p.shape(t, M_B, INNER, j=0, step=99, clip=False)
        poly(p, [(cx + 1.5, FY + 7), (cx + 7, FY + 7), (cx + 5.2, WYC), (cx + 1.5, WYC)], M_D)
    p.shape(SIDE, D_D, PART, j=0, step=8, clip=False)
    p.shape(TOP, D_B, PART, j=0, step=8)
    poly(p, [(-36, FY - 3), (30, FY - 3), (34, FY - 6.5), (-34, FY - 6.5)], D_L)
    m0, m1 = .4, .62
    poly(p, [(-34 + DD[0] * m0, FY + DD[1] * m0), (30 + DD[0] * m0, FY + DD[1] * m0), (30 + DD[0] * m1, FY + DD[1] * m1), (-34 + DD[0] * m1, FY + DD[1] * m1)], COR)
    poly(p, [(14, FY + 1.5), (34, FY + 1.5), (40, FY - 3), (40, FY + 4), (34, FY + TH - 2), (14, FY + TH - 2)], D_D)
    p.stroke(SIDE, PART, j=0, step=8)
    with layer(p, 'wheel_back'): wheel(p, NEAR[0], WYC, R, W_B)
    with layer(p, 'wheel'): wheel(p, NEAR[1], WYC, R, W_B)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    mo = {'wheel': dict(rotate=p.X((NEAR[1], WYC))), 'wheel_back': dict(rotate=p.X((NEAR[0], WYC)))}
    r = finish(p, 'skate_park', STAND, motion=mo, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {
        'node_skate_park_wheel': dict(center=[round(v, 1) for v in p.X((NEAR[1], WYC))], dir='cw', turns=1, duration_s=1.2, repeat=1, easing='ease-out', note='چرخ نزدیک راست؛ یک دور کامل هنگام رسیدن؛ حالت ایستا = پایان'),
        'node_skate_park_wheel_back': dict(center=[round(v, 1) for v in p.X((NEAR[0], WYC))], dir='cw', turns=1, duration_s=1.2, repeat=1, easing='ease-out', note='چرخ نزدیک چپ؛ هم‌زمان؛ چرخ‌های دور ثابت‌اند'),
        'idle_loop': False, 'reduced_motion': 'چرخ‌ها ثابت'}
    (OUTD / 'skate_park.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
