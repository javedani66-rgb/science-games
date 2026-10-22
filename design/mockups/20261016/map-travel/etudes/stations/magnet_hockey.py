#!/usr/bin/env python3
"""ایستگاه F04 «هاکی آهنربایی» (سرزمین ورزشگاه، سکوی سبز).
طرح قطعه‌به‌قطعه (واحد symbol؛ مرکز آهنربا CX=-30، کف BASE=7، قاب xf=(1,8,0) مثل آسیاب):
 ۱) بدنهٔ آهنربای نعلی ∩ ایستاده روی دو قطب: کمان بیرونی R=36 و درونی r=19 (پهنای ساق ۱۷)، یک بدنهٔ پیوسته با خط PART.
    نیمهٔ چپ آبی (#3f82e8 / روشن #8cbcff / تیره #2456b0)، نیمهٔ راست بنفش روشن (#a56fe0 / #d2adff / #6c3fae)، برش وسط روی محور x=CX.
 ۲) نور: نوار تخت روی لبهٔ بیرونی چپ (کمان + ساق)؛ سایهٔ تیز: نوار تخت لبهٔ راست هر ساق و کمان راست، همه داخل جزء.
 ۳) نوک نقره‌ای (۱۶ واحد پایین هر ساق): نقره‌ای سه‌پله (#dbe9f8 / سفید / #a3bbd9) با خط جداکنندهٔ INNER و شیار برش کوچک.
 ۴) گیرهٔ کاغذ فلزی نقره‌ای (لایهٔ متحرک node_magnet_hockey_clip) در فاصلهٔ بین دو قطب، روی زمین: قالب حلقهٔ دوبل
    (دو پوستهٔ تو در تو با خط INNER)، نه رنگی. پایان: چسبیده به لبهٔ درونی قطب راست؛ شروع: ۱۲ واحد (≈۸٫۶px) دورتر.
    (تغییر نسبت به ردیف فهرست: به‌جای «از زیر بالا بیاید»، چون آهنربا روی زمین ایستاده، گیره روی زمین می‌لغزد و می‌چسبد؛
     همچنان نیروی از دور و بی‌تماس در آغاز.) بدون حلقهٔ بیکار، بدون متن/پیکان."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8)
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/magnet_hockey'

B_B, B_L, B_D = '#3f82e8', '#8cbcff', '#2456b0'
P_B, P_L, P_D = '#a56fe0', '#d2adff', '#6c3fae'
S_B, S_L, S_D = '#dbe9f8', '#ffffff', '#a3bbd9'
CX, BASE = 0, 6
R, W = 56, 24
r = R - W
YC = -46                      # مرکز کمان
TIPY = -14                     # مرز نوک نقره‌ای
SHIFT = 5
CLIPW, CLIPH = 13, 22


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def body():
    return ([(CX - R, BASE), (CX - R, YC)] + ell(CX, YC, R, R, 180, 360, 28) + [(CX + R, YC), (CX + R, BASE), (CX + R - W, BASE), (CX + R - W, YC)]
            + ell(CX, YC, r, r, 360, 180, 28) + [(CX - r, YC), (CX - r, BASE)])


def right_half():
    return ([(CX, YC - R)] + ell(CX, YC, R, R, 270, 360, 14) + [(CX + R, BASE), (CX + R - W, BASE), (CX + R - W, YC)] + ell(CX, YC, r, r, 360, 270, 14))


def ribbon(rr0, rr1, a0, a1, n=12):
    return ell(CX, YC, rr1, rr1, a0, a1, n) + ell(CX, YC, rr0, rr0, a1, a0, n)


def build():
    p = Pen('magnet_hockey', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((-72, 12), (62, 8)), dot=(58, -16)); p.xf = (1.0, 0, -2)
    p.tipshadow(CX + 2, BASE + 3, 50); p.foot_tip(CX - R + W / 2, BASE + 2, 12); p.foot_tip(CX + R - W / 2, BASE + 2, 12)
    b = body()
    p.shape(b, B_B, PART, j=.04, step=99)
    p.fill(right_half(), P_B)
    # نور (چپ، لبهٔ بیرونی)
    poly(p, ribbon(R - 10, R - 5, 190, 255), B_L)
    poly(p, [(CX - R + 5, YC), (CX - R + 10, YC), (CX - R + 10, TIPY - 3), (CX - R + 5, TIPY - 3)], B_L)
    # سایهٔ تیز راست
    poly(p, ribbon(R - 9, R - 2, 290, 358), P_D)
    poly(p, [(CX + R - 9, YC), (CX + R - 2, YC), (CX + R - 2, TIPY - 3), (CX + R - 9, TIPY - 3)], P_D)
    poly(p, [(CX - r - 8, YC), (CX - r - 2, YC), (CX - r - 2, TIPY - 3), (CX - r - 8, TIPY - 3)], B_D)   # سایهٔ درونی ساق چپ
    # نور روی بنفش (درون ساق راست، لبهٔ چپ آن)
    poly(p, [(CX + r + 5, YC), (CX + r + 10, YC), (CX + r + 10, TIPY - 3), (CX + r + 5, TIPY - 3)], P_L)
    # برش وسط
    p.ln((CX, YC - R + 2), (CX, YC - r - 2), INNER, NAVY, j=0, probe='برش وسط')
    # نوک‌های نقره‌ای
    for x0, x1 in ((CX - R, CX - R + W), (CX + R - W, CX + R)):
        poly(p, [(x0 + 1, TIPY), (x1 - 1, TIPY), (x1 - 1, BASE - 7), (x1 - 4.5, BASE - 1.5), (x0 + 4.5, BASE - 1.5), (x0 + 1, BASE - 7)], S_B)
        poly(p, [(x0 + 3.5, TIPY + 3), (x0 + 6.5, TIPY + 3), (x0 + 6.5, BASE - 7), (x0 + 3.5, BASE - 7)], S_L)
        poly(p, [(x1 - 6, TIPY + 3), (x1 - 3, TIPY + 3), (x1 - 3, BASE - 7), (x1 - 6, BASE - 7)], S_D)
    p.stroke(b, PART, j=.04, step=99)
    for x0, x1 in ((CX - R, CX - R + W), (CX + R - W, CX + R)):
        p.ln((x0 + 2, TIPY), (x1 - 2, TIPY), INNER, NAVY, j=0)
    # گیرهٔ کاغذ (لایهٔ متحرک): موقعیت پایانی = چسبیده به لبهٔ درونی قطب راست
    # گیره: سه ران با فاصلهٔ ۱۰ (مرکز تا مرکز)، عرض مرکزها ۲۰ (+خط ≈۲۷٫۶)، ارتفاع کل ≈۴۰
    GAP = 10; NV, SV = 7.6, 3.9
    ce = CX + r - 3.8 - NV / 2 - 1.0
    xR, xM, xL = ce, ce - GAP, ce - 2 * GAP
    yb = BASE - 1; yt = yb - (46 - NV)
    wire = ([(xL, yb - 12), (xL, yt + GAP)] + ell((xL + xR) / 2, yt + GAP, GAP, GAP, -180, 0, 14)
            + [(xR, yb - GAP / 2)] + ell((xR + xM) / 2, yb - GAP / 2, GAP / 2, GAP / 2, 0, 180, 10)
            + [(xM, yt + GAP + 8)])
    with layer(p, 'clip'):
        p.tipshadow((xL + xR) / 2, BASE + 3, 20)
        q = p.X(wire); d = 'M' + 'L'.join('%.1f,%.1f' % z for z in q)
        p.raw('<path d="%s" fill="none" stroke="#241a5e" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"/>' % (d, NV))
        p.raw('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"/>' % (d, S_B, SV))
    return p, ce


if __name__ == '__main__':
    p, ce = build()
    offs = [p.V((-SHIFT, 0)), (0, 0)]
    r_ = finish(p, 'magnet_hockey', None, motion={'clip': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r_['spec']
    sp['motion_spec'] = {'node_magnet_hockey_clip': dict(
        kind='گیرهٔ کاغذ فلزی؛ حالت ایستا = چسبیده به قطب (پایان حرکت)',
        translate_x_symbol_units=[-SHIFT, 0], translate_x_map_px=[round(-SHIFT * K, 1), 0],
        duration_s=1.0, easing='ease-in (شتاب‌گرفتن به سمت قطب)', loop=False, trigger='رسیدن کودک (یک‌بار)',
        note='گیره از ≈%.1fpx دورتر (بی‌تماس) می‌لغزد و به قطب راست می‌چسبد؛ آهنربا ثابت. با reduced-motion چسبیده می‌ماند. بدون حلقهٔ بیکار.' % (SHIFT * K))}
    (OUTD / 'magnet_hockey.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r_[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r_['widths']]}, ensure_ascii=False))
