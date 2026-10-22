#!/usr/bin/env python3
"""ایستگاه F06 «پیست اسکیت روی یخ» (سرزمین ورزشگاه، سکوی سبز ۹۳°) — دور ۶ (R6).
طرح (واحد symbol؛ مرکز سکو (0,0)):
 ۱) پیست بیضی ¾: دیوارهٔ سفید-نقره‌ای ضخیم (WH=9، سه پله #aebfd2/#dfe8f2/سفید)، لبهٔ سفید پهن ۹ واحد، یخ آبی #8fd3f4 (رنگ‌مایه ≈۱۹۸°) با سه خراش اسکیت؛ بیضی ۶۸×۳۰ (≈۷۴٪ سکو).
 ۲) دو اسکیت درشت ۱٫۰ (ارتفاع ≈۶۳ واحد): پوتین سفید سه‌پله + قرمز (نوک، پاشنه، سرِ ساق، سه بند) + تیغهٔ نقره‌ای با دو پایه؛ یکی عقب‌تر.
 لایهٔ متحرک node_ice_rink_skate = اسکیت جلویی: ۱۲ واحد به راست می‌لغزد؛ حالت ایستا = پایان. بدون حلقهٔ بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from station_kit import *
from g4_helpers import *
from shapely.geometry import Polygon
from shapely.ops import unary_union
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/ice_rink'

RIM, W_B, W_L, W_D = '#ffffff', '#aebfd2', '#dfe8f2', '#7d93ad'
ICE, ICE_L, ICE_D = '#8fd3f4', '#c6ecfb', '#5fb0dc'
BT_B, BT_L, BT_D = '#ffffff', '#ffffff', '#c3d2ea'
RD_B, RD_D = '#e0402e', '#a82818'
M_B, M_L, M_D = '#cdd6e2', '#ffffff', '#7e8da6'
CX, CY, RX, RY, WH = 0, -6, 70, 31, 9
GLIDE = 12


def skate(p, ox, oy, k=1.0):
    T = lambda pts: [(ox + x * k, oy + y * k) for x, y in pts]
    poly(p, T(ell(26, 1, 34, 5, 0, 360, 20)), ICE_D, .85)                       # سایهٔ تیز روی یخ
    blade = unary_union([Polygon([(-6, 0), (42, 0), (52, -6), (57, -12), (50, -11), (44, -5), (-6, -5)]), Polygon(rect(4, -16, 13, -3)), Polygon(rect(33, -16, 42, -3))])
    bl = T(list(blade.exterior.coords)[:-1])
    p.shape(bl, M_B, INNER, j=0, step=5, clip=False)
    poly(p, T(rect(-3, -3.5, 40, -1.5)), M_L)
    boot = T([(-1, -13), (-1, -62), (23, -62), (25, -40), (41, -38), (52, -29), (51, -13)])
    p.shape(boot, BT_B, PART, j=0, step=5, clip=False)
    poly(p, T([(16, -60), (23, -60), (24.5, -41), (25, -39), (41, -37.5), (50, -30), (49.5, -15), (16, -15)]), BT_D)       # سایهٔ تیز سمت راست
    poly(p, T(rect(2, -58, 6, -18)), BT_L)
    poly(p, T([(-1, -62), (23, -62), (23, -55), (-1, -55)]), RD_B)                      # سرِ ساق
    poly(p, T([(-1, -34), (6, -34), (6, -13), (-1, -13)]), RD_B)                       # پاشنه
    poly(p, T([(41, -38), (52, -29), (51, -13), (42, -13)]), RD_B)           # نوک
    poly(p, T([(-1, -17), (51, -17), (51, -13), (-1, -13)]), RD_D)                      # کفی
    for y in (-44, -36, -28): poly(p, T(rect(10, y - 1.7, 23, y + 1.7)), RD_B)          # سه بند
    p.stroke(boot, PART, j=0, step=5)


def build(out=OUTD, glide=0):
    p = Pen('ice_rink', 'sports'); pad(p, line=((-52, 40), (-36, 43)), tri=((74, -20), (70, 18)), dot=(-70, -14))
    top = ell(CX, CY, RX, RY, 180, 360, 24); bot = ell(CX, CY + WH, RX, RY, 0, 180, 24)
    p.tipshadow(CX, CY + WH + 2, 62); p.foot_tip(CX, CY + WH, 56)
    p.shape(top + bot, W_B, PART, j=.1, step=10)
    poly(p, band(CX, CY + 2, RX - 1, RY, 3.5, 20, 160, 20), W_L)
    poly(p, [(x, y) for x, y in ell(CX, CY, RX, RY, 10, 80, 14)] + [(x, y + WH) for x, y in ell(CX, CY, RX, RY, 80, 10, 14)], W_D, .75)
    p.shape(ell(CX, CY, RX, RY, 0, 360, 48), RIM, PART, j=.1, step=10, clip=False)
    p.shape(ell(CX, CY, RX - 9, RY - 7, 0, 360, 48), ICE, INNER, j=.1, step=99, clip=False)
    poly(p, ell(CX, CY, RX - 12, RY - 10, 195, 270, 14) + ell(CX, CY, RX - 24, RY - 17, 270, 195, 14), ICE_L)
    arcline(p, ell(0, CY + 10, 44, 10, 190, 330, 14), ICE_L, 2.4); arcline(p, ell(8, CY + 2, 52, 14, 15, 75, 10), ICE_L, 2.4); arcline(p, ell(-4, CY + 4, 30, 6, 200, 300, 10), ICE_L, 2.4)
    skate(p, -48, -8, .8)
    with layer(p, 'skate'):
        skate(p, 2 - GLIDE + glide, 8, .8)
    return p


STAND = None
if __name__ == '__main__':
    p = build(glide=GLIDE)
    mo = {'skate': dict(offsets=[(-GLIDE, 0), (0, 0)])}
    r = finish(p, 'ice_rink', STAND, motion=mo, out=OUTD, shots=SHOTS)
    sp_ = r['spec']
    sp_['motion_spec'] = {'node_ice_rink_skate': dict(
        kind='اسکیت جلویی روی یخ به راست می‌لغزد؛ حالت ایستا = پایان', translate_x_symbol_units=[-GLIDE, 0], translate_x_map_px=[round(-GLIDE * K, 1), 0],
        duration_s=1.2, easing='ease-out', loop=False, trigger='رسیدن کودک (یک‌بار)', note='با reduced-motion ثابت در وضع پایان؛ بدون حلقهٔ بیکار.')}
    (OUTD / 'ice_rink.json').write_text(json.dumps(sp_, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
