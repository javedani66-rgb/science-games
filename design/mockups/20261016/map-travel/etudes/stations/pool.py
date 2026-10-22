#!/usr/bin/env python3
"""ایستگاه F07 «استخر» — بازطراحی دور ۶ (همسطح پیچ‌کاری).
ایده: استخر مستطیلی ¾ (قاب مایل: وجه جلو + روی لبه + وجه راست)، آب فیروزه‌ای با دیوارهٔ درونی تیره‌تر، نردبان فلزی گوشهٔ پشت-راست، توپ ساحلی راه‌راه شناور.
واحد symbol؛ xf=(1.12,0,0). وجه جلو x -54..44، y 2..26؛ عمق (+14,-40). لبه ۸ (جلو/کنار) و ۶ (پشت).
 اجزای درشت: ۱) بدنهٔ سفید سه‌پله (جلو/راست/رو) ۲) آب با ریزموج ۳) نردبان ۴) توپ ساحلی (لایهٔ متحرک ball؛ از سمت چپ-پایین‌ترِ آب تا جای پایان می‌لغزد؛ ایستا=پایان؛ بدون بیکار)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8)
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/pool'
W_T, W_F, W_S = '#ffffff', '#dfe8f4', '#a9bcd6'       # لبه: رو، جلو، راست
A_B, A_L, A_D = '#3fb4f0', '#9be0ff', '#1f7fc4'
RAIL, RAIL_L, RAIL_D = '#aebfd8', '#f2f7ff', '#6f86ab'
FX0, FX1, FY0, FY1 = -52, 40, 4, 22
DX, DY = 12, -40
BR = 12; BALL_C = (-24, -18)
DRIFT = (-12, 3)
def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))
def pos(u, w): return (FX0 + u * (FX1 - FX0) + w * DX, FY0 + w * DY)
def pline(p, pts, col, w, cap='round'):
    p.raw('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, w, cap))
def wave(x0, x1, y, amp=1.8, n=20):
    return [(x0 + (x1 - x0) * i / n, y + amp * math.sin(2 * math.pi * i / n * 1.5)) for i in range(n + 1)]
def build():
    p = Pen('pool', 'sports'); pad(p, line=((-80, 12), (-66, 20)), tri=((74, -20), (80, 6)), dot=(-76, -14)); p.xf = (1.1, 0, 4)
    p.tipshadow(8, FY1 + 4, 56); p.foot_tip(-30, FY1 - 2, 18); p.foot_tip(24, FY1 - 2, 18)
    # ۱) بدنه
    p.shape([(FX1, FY0), (FX1 + DX, FY0 + DY), (FX1 + DX, FY1 + DY), (FX1, FY1)], W_S, PART, j=.05, step=8)
    p.shape([(FX0, FY0), (FX1, FY0), (FX1, FY1), (FX0, FY1)], W_F, PART, j=.05, step=8)
    p.shape([(FX0, FY0), (FX1, FY0), (FX1 + DX, FY0 + DY), (FX0 + DX, FY0 + DY)], W_T, PART, j=.05, step=8)
    p.ln((FX0 + 8, FY0 + 10), (FX1 - 8, FY0 + 10), INNER, '#b9c9de', j=.1)      # نوار کاشی جلو
    # دهانه و آب
    u0, u1, w0, w1, ww = .09, .91, .21, .84, .66
    hole = [pos(u0, w0), pos(u1, w0), pos(u1, w1), pos(u0, w1)]
    poly(p, hole, A_D)
    water = [pos(u0, w0), pos(u1, w0), pos(u1, ww), pos(u0, ww)]
    poly(p, water, A_B)
    poly(p, [pos(u0, w0 + .02), pos(u0 + .18, w0 + .02), pos(u0 + .18 + .03, w0 + .09), pos(u0 + .03, w0 + .09)], A_L)
    p.stroke(hole, INNER, j=.05, step=8)
    p.ln(pos(.12, .48), pos(.26, .48), INNER, '#ffffff', j=0); p.ln(pos(.42, .30), pos(.58, .30), INNER, '#ffffff', j=0)
    # ۳) نردبان بلند فلزی (دو ریل ضخیم سه‌پله + ۳ پله + دستگیرهٔ خمیده)
    xs, ys = pos(.72, .62)
    LH = 66; XG = 24
    def rail(x):
        pts = [(x, ys), (x, ys - LH)]
        for k in range(1, 8):
            t = math.radians(180 - 160 * k / 7); pts.append((x + 7 + 7 * math.cos(t), ys - LH - 7 * math.sin(t)))
        return pts
    rungs = (ys - 20, ys - 40, ys - 58)
    for x in (xs, xs + XG): pline(p, rail(x), NAVY, 15)
    for y in rungs: pline(p, [(xs, y), (xs + XG, y)], NAVY, 12, 'butt')
    for x in (xs, xs + XG): pline(p, rail(x), RAIL, 8)
    for y in rungs: pline(p, [(xs, y), (xs + XG, y)], RAIL, 6, 'butt')
    # ۴) توپ ساحلی درشت
    with layer(p, 'ball'):
        cx, cy = BALL_C
        ring = ell(cx, cy + BR - 1, BR * 1.5, BR * .3, 0, 360, 28)
        poly(p, ring, A_D, .85)
        poly(p, ell(cx, cy + BR - 3, BR * 1.15, BR * .2, 0, 360, 24), '#ffffff', .75)
        cols = ['#ee4b3c', '#ffc93c', '#ffffff']
        circ = ell(cx, cy, BR, BR, 0, 360, 40)
        poly(p, circ, '#ffffff')
        lam = [-90, -32, 32, 90]
        def mer(l): return [(cx + BR * math.cos(math.radians(t)) * math.sin(math.radians(l)), cy - BR * math.sin(math.radians(t))) for t in range(-90, 91, 15)]
        for i in range(2):
            a = mer(lam[i]); b = mer(lam[i + 1])[::-1]
            poly(p, a + b, cols[i])
        a = mer(lam[2]); b = mer(lam[3])[::-1]; poly(p, a + b, '#ff8a2a')
        for l in lam[1:-1]: pline(p, mer(l), NAVY, 1.3)
        poly(p, [(cx + BR * .98 * math.cos(math.radians(t)), cy + BR * .98 * math.sin(math.radians(t))) for t in range(-60, 61, 12)] + [(cx + BR * .45 * math.cos(math.radians(t)), cy + BR * .45 * math.sin(math.radians(t))) for t in range(60, -61, -12)], '#10083a', .2)
        poly(p, ell(cx - BR * .35, cy - BR * .45, BR * .22, BR * .14, 0, 360, 14), '#ffffff', .8)
        pline(p, circ + [circ[0]], NAVY, 2.0)
    return p
STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'pool', STAND, motion={'ball': dict(offsets=[p.V(DRIFT), p.V((DRIFT[0] / 2, DRIFT[1] / 2)), (0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_pool_ball': dict(
        kind='توپ ساحلی روی آب می‌لغزد؛ حالت ایستا = پایان', translate_symbol_units=[list(DRIFT), [0, 0]],
        duration_s=1.6, easing='ease-out', loop=False, trigger='رسیدن کودک (یک‌بار)', reduced_motion='ایستا',
        note='بدنه، آب و نردبان ثابت؛ بدون حلقهٔ بیکار (بخش ۰ فهرست).')}
    (OUTD / 'pool.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
