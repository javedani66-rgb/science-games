#!/usr/bin/env python3
"""ایستگاه F09 «زمین اسکیت» (سرزمین ورزشگاه، سکوی 'sports' رنگ‌مایه ۹۳°).
قهرمان: اسکیت‌برد، نمای کنار. طرح قطعه‌به‌قطعه (واحد symbol، مرکز سکو (0,0)، y منفی = بالا، کف GY=6):
 ۱) تخته (چوب رنگی فیروزه‌ای، رنگ‌مایه ≈۱۸۵°، ۴۰° ... ۹۰° دور از سکو): چندضلعی یک‌پارچه، قسمت میانی صاف و دو سر کج‌شدهٔ رو به بالا
    (kicktail)، ضخامت ۱۶، x از -70 تا -2؛ پایه #2cb5c6، نور #8fe8ee (نوار تخت بالا)، سایهٔ تیز راست #1a8696 (چندضلعی داخل تخته)؛ دور PART.
 ۲) (حذف شد: فقط نوار نور؛ ساده‌تر)
 ۳) دو محور (truck) فلزی: ذوزنقه #dbe9f8، سایه #a3bbd9، دور INNER؛ زیر تخته، هم‌پوشان ۴ واحد با تخته؛ مرکز هر محور دقیقاً روی مرکز چرخ.
 ۴) چهار چرخ → دو چرخ دیده‌شده (نمای کنار): دایرهٔ r=12، کرم #fff1c0 با سایهٔ تیز #e3c66e و دور PART؛ مرکز: تکهٔ تیرهٔ قهوه‌ای (#7a4a1f) میله‌ای + نقطهٔ زرد.
    چرخ‌ها لایه‌های متحرک: node_skate_park_wheel (راست)، node_skate_park_wheel_back (چپ).
 ۵) سایهٔ تماس زیر هر چرخ. بدون دسته/جعبه/بشکه/پرچم/پره (هم‌ریختی M02/E02)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/skate_park'

D_B, D_L, D_D = '#2cb5c6', '#8fe8ee', '#1a8696'
M_B, M_D = '#b8c9e6', '#7f95b8'
W_B, W_D = '#fff1c0', '#e3c66e'
HUBC = '#7a4a1f'; YEL = '#ffd84d'; ORG = '#ff9b4a'
GY = 6; R = 9; WYC = GY - R
WX = (-62, -14)          # چرخ چپ (back)، چرخ راست
XF = (1.0, 0, 0)

TOPF, BOT = -43, -27     # بالا و پایین بخش صاف تخته
DECK = [(-74, -50), (-67, TOPF), (-7, TOPF), (0, -50), (0, -38), (-7, BOT), (-67, BOT), (-74, -38)]


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def truck(p, cx):
    pts = [(cx - 8, BOT - 4), (cx + 8, BOT - 4), (cx + 6, WYC + 2), (cx - 6, WYC + 2)]
    p.shape(pts, M_B, INNER, j=0, step=99, clip=False)
    poly(p, [(cx + 2, BOT + 1), (cx + 8, BOT + 1), (cx + 6, WYC), (cx + 2, WYC)], M_D)
    p.stroke(pts, INNER, j=0, step=99)


def wheel(p, cx):
    p.shape(ell(cx, WYC, R, R, 0, 360, 40), W_B, PART, j=.1, step=99, clip=False)
    poly(p, [(cx - 4, WYC - 2), (cx + 4, WYC - 2), (cx + 4, WYC + 2), (cx - 4, WYC + 2)], HUBC)          # نوار کوتاه مرکزی ۸×۴ (نشانهٔ چرخش)
    p.raw('<circle cx="%.1f" cy="%.1f" r="2.2" fill="%s"/>' % (*p.X((cx, WYC)), YEL))


def build(out=None):
    p = Pen('skate_park', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    for cx in WX:
        p.tipshadow(cx, GY - 1, 14); p.foot_tip(cx, GY - 2, 8)
    for cx in WX: truck(p, cx)
    p.shape(DECK, D_B, PART, j=0, step=8)
    poly(p, [(-66, TOPF + 4), (-12, TOPF + 4), (-12, TOPF + 7.5), (-66, TOPF + 7.5)], D_L)                    # نور
    poly(p, [(-26, TOPF + 3), (-7, TOPF + 3), (-3, TOPF - 4), (-1.5, TOPF - 6), (-1.5, -39), (-7, BOT - 3), (-26, BOT - 3)], D_D)   # سایهٔ تیز راست
    p.stroke(DECK, PART, j=0, step=8)
    with layer(p, 'wheel_back'): wheel(p, WX[0])
    with layer(p, 'wheel'): wheel(p, WX[1])
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    mo = {'wheel': dict(rotate=p.X((WX[1], WYC))), 'wheel_back': dict(rotate=p.X((WX[0], WYC)))}
    r = finish(p, 'skate_park', STAND, motion=mo, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {
        'node_skate_park_wheel': dict(center=[round(v, 1) for v in p.X((WX[1], WYC))], dir='cw', turns=1, duration_s=1.2, repeat=1, easing='ease-out', note='چرخ راست؛ یک دور کامل هنگام رسیدن؛ حالت ایستا = پایان'),
        'node_skate_park_wheel_back': dict(center=[round(v, 1) for v in p.X((WX[0], WYC))], dir='cw', turns=1, duration_s=1.2, repeat=1, easing='ease-out', note='چرخ چپ؛ هم‌زمان با چرخ راست'),
        'idle_loop': False, 'reduced_motion': 'چرخ‌ها ثابت'}
    (OUTD / 'skate_park.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
