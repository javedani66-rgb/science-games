#!/usr/bin/env python3
"""ایستگاه F04 «هاکی آهنربایی» — بازطراحی دور ۶ (همسطح پیچ‌کاری).
ایده: آهنربای نعلی بزرگِ خوابیده روی سطح، نمای ¾ (رویهٔ U شکل فشرده با k=0.55 + ضخامت H=20 رو به بیننده)، نیمهٔ چپ آبی و راست قرمز،
نوک‌های سفید-نقره‌ای رو به بیننده، گیرهٔ کاغذ نقره‌ای ایستاده در شکاف کنار قطب راست.
اجزای درشت: ۱) نیمهٔ آبی ۲) نیمهٔ قرمز ۳) دو نوک نقره‌ای ۴) گیره. هر نیمه سه پله: رو روشن، دیواره تیره، نوار برق باریک.
ضخامت = پشتهٔ نسخه‌های جابه‌جاشدهٔ رو (بدون ترفند رستری). حرکت: فقط clip؛ ایستا=چسبیده به قطب (پایان)؛ بدون بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8)
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/magnet_hockey'
B_T, B_S, B_L = '#5aa3ff', '#2557b8', '#a9d0ff'      # آبی: رو، دیواره، برق
R_T, R_S, R_L = '#f2685c', '#a62f33', '#ffb3a8'      # قرمز
S_T, S_S = '#f4f8ff', '#a3bbd9'                      # نقره‌ای
R, r, L = 56, 29, 38          # شعاع بیرونی/درونی، طول ساق (در صفحه)
K3 = .6; Y0 = -34; H = 24    # فشردگی نما، مرکز کمان، ضخامت
TIP = 20                      # طول نوک نقره‌ای
CLIPSHIFT = 12
def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))
AY = math.radians(15); DX0 = 0
def P(u, v, t=0):
    return (u * math.cos(AY) - v * math.sin(AY) + DX0, Y0 + (u * math.sin(AY) + v * math.cos(AY)) * K3 + t)
def arc(rad, a0, a1, n=16): return [P(rad * math.cos(math.radians(a0 + (a1 - a0) * i / n)), rad * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
xs_ = [P(-R, L)[0], P(R, 0)[0], P(R, L)[0], P(-R, 0)[0], P(0, -R)[0]]; DX0 = -(min(xs_) + max(xs_)) / 2
def half(sg, v1=L):
    """نیمهٔ سمت sg (-1 چپ، +1 راست) از رویه تا v=v1 در ساق؛ نقطه‌ها در مختصات نما."""
    a0, a1 = (180, 270) if sg < 0 else (360, 270)
    out = [P(sg * R, v1), P(sg * R, 0)] + arc(R, a0, a1) + arc(r, a1, a0)[0:] + [P(sg * r, v1)]
    return out
def shift(pts, t): return [(x, y + t) for x, y in pts]
def build():
    p = Pen('magnet_hockey', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((-74, 14), (70, 8)), dot=(62, -22)); p.xf = (1.16, 0, -6)
    q1 = P(-R / 2 - r / 2, L, H); q2 = P(R / 2 + r / 2, L, H); p.tipshadow(0, (q1[1] + q2[1]) / 2 + 2, 56); p.foot_tip(q1[0], q1[1] - 3, 12); p.foot_tip(q2[0], q2[1] - 3, 12)
    full = [P(-R, L), P(-R, 0)] + arc(R, 180, 360, 30) + [P(R, 0), P(R, L), P(r, L), P(r, 0)] + arc(r, 360, 180, 30) + [P(-r, 0), P(-r, L)]
    # ضخامت: خط دور از اجتماع همهٔ نسخه‌ها، سپس رنگ دیواره
    ts = list(range(0, H + 1, 2))
    for t in ts[::-1]:
        p.raw('<polygon points="%s" fill="#241a5e" stroke="#241a5e" stroke-width="%s" stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(shift(full, t))), OUT))
    for sg, col in ((-1, B_S), (1, R_S)):
        for t in ts[::-1]: poly(p, shift(half(sg), t), col)
    # دیواره‌ها: خط تیرهٔ مرز رو-دیواره
    for sg, top, lit in ((-1, B_T, B_L), (1, R_T, R_L)):
        h0 = half(sg, L - TIP)
        p.shape(h0, top, PART, j=.04, step=8, clip=False)
        # برق باریک روی لبهٔ بیرونی کمان و ساق
        a0, a1 = (190, 262) if sg < 0 else (350, 278)
        rib = arc(R - 7, a0, a1, 12) + arc(R - 12, a1, a0, 12)
        poly(p, rib, lit)
        poly(p, [P(sg * (R - 7), 2), P(sg * (R - 12), 2), P(sg * (R - 12), L - TIP - 5), P(sg * (R - 7), L - TIP - 5)], lit)
    # برش میانی
    p.ln(P(0, -R + 4), P(0, -r - 3), INNER, NAVY, j=0, probe='برش وسط')
    # نوک‌های نقره‌ای (روی + دیوارهٔ جلو)
    for sg in (-1, 1):
        u0, u1 = sorted((sg * R, sg * r))
        front = [P(u0, L - TIP), P(u1, L - TIP), P(u1, L), P(u0, L)]
        p.shape(front, S_T, PART, j=.04, step=8, clip=False)
        wall = [P(u0, L), P(u1, L), P(u1, L, H), P(u0, L, H)]
        p.shape(wall, S_S, PART, j=.04, step=8, clip=False)
    # گیره: ایستاده روی زمین در شکاف کنار قطب راست
    NV, SV = 9.6, 5.4; GAP = 12
    bx_, yb = P(r - 4, L - 4, H * .5); xR = bx_ - 1 - NV / 2; xM = xR - GAP; xL = xM - GAP
    yt = yb - 46
    wire = ([(xL, yb - 14), (xL, yt + GAP)] + ell((xL + xR) / 2, yt + GAP, GAP, GAP, -180, 0, 14) + [(xR, yb - GAP / 2)]
            + ell((xR + xM) / 2, yb - GAP / 2, GAP / 2, GAP / 2, 0, 180, 10) + [(xM, yt + GAP + 10)])
    with layer(p, 'clip'):
        p.tipshadow((xL + xR) / 2, yb + 2, 22)
        q = p.X(wire); d = 'M' + 'L'.join('%.1f,%.1f' % z for z in q)
        p.raw('<path d="%s" fill="none" stroke="#241a5e" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"/>' % (d, NV))
        p.raw('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"/>' % (d, S_T, SV))
    return p, xR
if __name__ == '__main__':
    p, ce = build()
    offs = [p.V((-CLIPSHIFT, 0)), (0, 0)]
    r_ = finish(p, 'magnet_hockey', None, motion={'clip': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r_['spec']
    sp['motion_spec'] = {'node_magnet_hockey_clip': dict(
        kind='گیرهٔ کاغذ فلزی؛ حالت ایستا = چسبیده به قطب (پایان حرکت)',
        translate_x_symbol_units=[-CLIPSHIFT, 0], translate_x_map_px=[round(-CLIPSHIFT * K, 1), 0],
        duration_s=1.0, easing='ease-in (شتاب‌گرفتن به سمت قطب)', loop=False, trigger='رسیدن کودک (یک‌بار)',
        note='گیره از ≈%.1fpx دورتر (بی‌تماس) می‌لغزد و به قطب راست می‌چسبد؛ آهنربا ثابت. با reduced-motion چسبیده می‌ماند. بدون حلقهٔ بیکار.' % (CLIPSHIFT * K))}
    (OUTD / 'magnet_hockey.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r_[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r_['widths']]}, ensure_ascii=False))
