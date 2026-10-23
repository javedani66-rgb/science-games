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
from r6lib import extrude
import r6lib
from shapely.geometry import Polygon
from shapely.ops import unary_union
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/ice_rink'

RIM, W_B, W_L, W_D = '#ffffff', '#aebfd2', '#dfe8f2', '#7d93ad'
ICE, ICE_L, ICE_D = '#8fd3f4', '#c6ecfb', '#5fb0dc'
BT_B, BT_L, BT_D = '#ffffff', '#ffffff', '#c3d2ea'
RD_B, RD_D = '#e0402e', '#a82818'
M_B, M_L, M_D = '#cdd6e2', '#ffffff', '#7e8da6'
CX, CY, RX, RY, WH = 0, -2, 82, 38, 8
GLIDE = 10


def skate(p, ox, oy, k=1.0):
    """اسکیت ¾ (نوک به راست): پایه‌ها، تیغه، پوتین."""
    T = lambda pts: [(ox + x * k, oy + y * k) for x, y in pts]
    T0 = T
    D = (13 * k, -12 * k)
    poly(p, T(ell(54, 2, 64, 7, 0, 360, 24)), ICE_D, .9)                       # سایهٔ تیز روی یخ
    prof = [(-6, -11), (-6, 0), (92, 0), (104, -5), (109, -13), (101, -14), (97, -11)]
    u = unary_union([Polygon(prof)] + [Polygon(rect(x0, -34, x0 + 10, -11)) for x0 in (14, 70)]).buffer(0)
    runner = T(list(u.exterior.coords)[:-1])                                   # تیغه و دو پایه یک شکل یکپارچه
    extrude(p, runner, (5 * k, -3.5 * k), M_B, M_L, M_D, mid=M_B, sw=2.6, sw_in=0)
    T = lambda pts: [(ox + x * k, oy + (y - 10) * k) for x, y in pts]   # پوتین ۱۰ واحد بالاتر از تیغه
    boot_pts = [(0, -100), (38, -100), (40, -64), (62, -48), (88, -42), (101, -30), (101, -20), (0, -20)]
    boot = T(boot_pts)
    extrude(p, boot, D, BT_B, BT_L, BT_D, sw=3.6, sw_in=0)
    rx_ = lambda pts, c=(RD_B, '#f2705e', RD_D): extrude(p, T(pts), D, c[0], c[1], c[2], mid=c[0], sw=0, sw_in=0)
    rx_([(0, -100), (38, -100), (38.5, -86), (0, -86)])                                   # سرِ ساق (دور رویه و پهلو هم می‌پیچد)
    poly(p, T([(0, -50), (14, -50), (14, -20), (0, -20)]), RD_B)                          # پاشنه
    poly(p, T([(88, -42), (101, -30), (101, -20), (80, -20), (82, -36)]), RD_B)            # نوک
    Dx, Dy = D                                                                              # نوک دور رویه و پهلو هم می‌پیچد
    poly(p, [(ox + 88 * k, oy + (-42 - 10) * k), (ox + 101 * k, oy + (-30 - 10) * k), (ox + 101 * k + Dx, oy + (-40) * k + Dy), (ox + 88 * k + Dx, oy + (-52) * k + Dy)], '#f2705e')
    poly(p, [(ox + 101 * k, oy + (-40) * k), (ox + 101 * k, oy + (-30) * k), (ox + 101 * k + Dx, oy + (-30) * k + Dy), (ox + 101 * k + Dx, oy + (-40) * k + Dy)], RD_D)
    poly(p, T([(0, -26), (101, -26), (101, -20), (0, -20)]), RD_D)                        # کفی
    (ax, ay), (bx, by) = T([(5, -100), (33, -100)])                                          # دهانهٔ ساق: گود، نه پُر
    f = lambda q, u: (q[0] + D[0] * u, q[1] + D[1] * u)
    poly(p, [f((ax, ay), .16), f((bx, by), .16), f((bx, by), .88), f((ax, ay), .88)], '#2a3463')
    poly(p, [f((ax, ay), .16), f((bx, by), .16), f((bx, by), .28), f((ax, ay), .28)], '#6a78ad')
    pts_b = T(boot_pts)                                                                      # خط دور یکدست روی همهٔ رنگ‌ها
    pcs = [Polygon(pts_b).buffer(0), Polygon([(x + D[0], y + D[1]) for x, y in pts_b]).buffer(0)]
    for i_ in range(len(pts_b)):
        a_, b_ = pts_b[i_], pts_b[(i_ + 1) % len(pts_b)]
        pcs.append(Polygon([a_, b_, (b_[0] + D[0], b_[1] + D[1]), (a_[0] + D[0], a_[1] + D[1])]).buffer(0))
    sil = unary_union(pcs).buffer(0.01)
    if sil.geom_type != 'Polygon': sil = max(sil.geoms, key=lambda g: g.area)
    p.stroke(list(sil.exterior.coords)[:-1], 3.6, j=0, step=6)
    for y in (-76, -64, -52): poly(p, T(rect(18, y - 3, 37, y + 3)), RD_B)                # سه بند


def build(out=OUTD, glide=0):
    p = Pen('ice_rink', 'sports'); pad(p, line=((-52, 40), (-36, 43)), tri=((74, -20), (70, 18)), dot=(-70, -14))
    p.xf = (0.86, 0, 6)
    top = ell(CX, CY, RX, RY, 180, 360, 24); bot = ell(CX, CY + WH, RX, RY, 0, 180, 24)
    p.tipshadow(CX, CY + WH + 2, 62); p.foot_tip(CX, CY + WH, 56)
    p.shape(top + bot, W_B, PART, j=.1, step=10)
    poly(p, band(CX, CY + 2, RX - 1, RY, 3.5, 20, 160, 20), W_L)
    poly(p, [(x, y) for x, y in ell(CX, CY, RX, RY, 10, 80, 14)] + [(x, y + WH) for x, y in ell(CX, CY, RX, RY, 80, 10, 14)], W_D, .75)
    p.shape(ell(CX, CY, RX, RY, 0, 360, 48), RIM, PART, j=.1, step=10, clip=False)
    p.shape(ell(CX, CY, RX - 8, RY - 6, 0, 360, 48), ICE, INNER, j=.1, step=99, clip=False)
    poly(p, ell(CX, CY, RX - 11, RY - 9, 195, 270, 14) + ell(CX, CY, RX - 22, RY - 15, 270, 195, 14), ICE_L)
    arcline(p, ell(CX + 14, CY + 12, 40, 9, 20, 150, 12), ICE_L, 2.6)
    arcline(p, ell(CX - 10, CY - 4, 44, 12, 200, 330, 12), ICE_L, 2.4)
    arcline(p, ell(CX + 8, CY + 2, 26, 7, 190, 340, 12), ICE_L, 2.4)
    arcline(p, ell(CX + 30, CY - 6, 22, 8, 10, 120, 12), ICE_L, 2.2)
    with layer(p, 'skate_back'):                                               # اسکیت پشتی: ثابت، دورتر و بالاتر
        skate(p, CX + 3, CY - 7, .44)
    with layer(p, 'skate'):                                                    # اسکیت جلویی: می‌لغزد
        skate(p, CX - 56 - GLIDE + glide, CY + 12, .5)
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
