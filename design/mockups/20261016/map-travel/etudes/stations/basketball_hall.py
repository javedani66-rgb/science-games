#!/usr/bin/env python3
"""ایستگاه F02 «سالن بسکتبال» — بازطراحی دور ۶ (همسطح پیچ‌کاری).
ایده: تختهٔ ¾ (روی + ضخامت راست) با حلقهٔ نارنجی و تور، ستون و پایهٔ جعبه‌ای، و توپ نارنجی که از حلقه افتاده و کنار پایه نشسته.
اجزای درشت: ۱) تخته با کادر قرمز ۲) حلقه+تور ۳) ستون+پایه (سه‌پله فولادی) ۴) توپ r=26 با درزهای سیاه.
واحد symbol؛ بالاترین نقطه ≈ -144 (قاب دیده می‌شود). حرکت: فقط ball؛ از زیر حلقه (-38,-72) می‌افتد تا جای پایان؛ ایستا=پایان؛ بدون بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8)
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/basketball_hall'
S_B, S_L, S_D = '#7f9bc8', '#b4c8e8', '#4f6794'
W_B, W_L, W_D = '#f4f7fd', '#ffffff', '#c3d1e8'
RED = '#e0553a'
OR_B, OR_L, OR_D = '#ff9a2e', '#ffc27a', '#c4600c'
NETL = '#8aa6d2'
HOLE = '#4a1f4a'
BX0, BX1, BT, BB = -56, 56, -134, -72      # روی تخته
TX, TY = 8, -6                              # ضخامت
RIMY = -76
BR = 26; BALL = (38, 0)
SHIFT = (-38, -72)
def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, (' stroke="%s" stroke-width=".6" stroke-linejoin="round"' % col) if op == 1 else ' opacity="%s"' % op))   # حاشیهٔ هم‌رنگ: درز مویی بین چندضلعی‌ها نماند
def rect(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
def pline(p, pts, col, w):
    p.raw('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, w))
def box(p, x0, y0, x1, y1, dx, dy, cols):
    """جعبهٔ ¾: وجه جلو + رو + راست؛ cols=(جلو، رو، راست)."""
    p.shape([(x1, y0), (x1 + dx, y0 + dy), (x1 + dx, y1 + dy), (x1, y1)], cols[2], PART, j=.05, step=8)
    p.shape([(x0, y0), (x1, y0), (x1 + dx, y0 + dy), (x0 + dx, y0 + dy)], cols[1], PART, j=.05, step=8)
    p.shape(rect(x0, y0, x1, y1), cols[0], PART, j=.05, step=8)
def build():
    p = Pen('basketball_hall', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((-74, 14), (70, 8)), dot=(62, -22))
    p.xf = (1.0, 0.0, 0.0)
    p.tipshadow(0, 4, 36); p.foot_tip(0, 2, 26); p.foot_tip(BALL[0], BALL[1] + BR - 2, 14)
    # ۳) ستون و پایه
    pole = rect(-9, -80, 9, -10)
    p.shape(pole, S_B, PART, j=.05, step=8)
    poly(p, rect(-5, -76, -2, -14), S_L); poly(p, rect(3, -76, 6.5, -14), S_D)
    box(p, -26, -16, 26, 0, 10, -7, (S_B, S_L, S_D))
    poly(p, rect(-22, -12, -16, -3), S_L)
    # ۱) تخته
    p.shape([(BX1, BT), (BX1 + TX, BT + TY), (BX1 + TX, BB + TY), (BX1, BB)], W_D, PART, j=.05, step=8)
    p.shape([(BX0, BT), (BX1, BT), (BX1 + TX, BT + TY), (BX0 + TX, BT + TY)], W_L, PART, j=.05, step=8)
    p.shape(rect(BX0, BT, BX1, BB), W_B, PART, j=.05, step=8)
    poly(p, rect(BX0 + 6, BT + 6, BX0 + 14, BB - 6), W_L)
    poly(p, rect(BX1 - 20, BT + 5, BX1 - 5, BB - 5), '#e3ebf8')
    q = rect(-22, -118, 22, -88)
    p.shape(q, RED, INNER, j=.05, step=6, clip=False)
    poly(p, rect(-14, -111, 14, -95), W_B)
    # ۲) حلقه و تور
    ring = ell(0, RIMY, 32, 11, 0, 360, 36)
    p.shape(ring, OR_B, PART, j=.05, step=99, clip=False)
    p.fill(ell(0, RIMY - 1, 22, 5.5, 0, 360, 28), HOLE)
    net = [(-25, RIMY + 5), (25, RIMY + 5), (14, -44), (-14, -44)]
    p.shape(net, '#ffffff', INNER, j=.05, step=8)
    for a, b in (((-14, RIMY + 8), (0, -48)), ((0, RIMY + 8), (-8, -48)), ((0, RIMY + 8), (8, -48)), ((14, RIMY + 8), (0, -48)), ((-14, RIMY + 8), (-9, -48)), ((14, RIMY + 8), (9, -48))):
        p.ln(a, b, 2.4, NETL, j=0)
    p.stroke(net, INNER, j=.05, step=8)
    pline(p, [(x, RIMY + 2 + 10.5 * math.sin(math.radians(a))) for x, a in [(32 * math.cos(math.radians(t)), t) for t in range(10, 171, 10)]], OR_L, 3.2)
    # ۴) توپ
    with layer(p, 'ball'):
        cx, cy = BALL
        p.tipshadow(cx + 2, cy + BR - 1, 24)
        circ = ell(cx, cy, BR, BR, 0, 360, 40)
        p.shape(circ, OR_B, OUT, j=.05, step=99)
        h = math.degrees(math.acos(10 / (2 * BR))); phi = 40.6
        c1 = [(cx + BR * math.cos(math.radians(a)), cy + BR * math.sin(math.radians(a))) for a in [phi - h + 2 * h * i / 16 for i in range(17)]]
        c1 += [(cx - 10 + BR * math.cos(math.radians(a)), cy - 8 + BR * math.sin(math.radians(a))) for a in [phi + h - 2 * h * i / 16 for i in range(17)]]
        poly(p, c1, OR_D)
        poly(p, [(cx - 16 + 5 * math.cos(math.radians(t)), cy - 12 + 3 * math.sin(math.radians(t))) for t in range(0, 360, 30)], OR_L)
        for a, b in (((cx, cy - BR + 1), (cx, cy + BR - 1)), ((cx - BR + 1, cy), (cx + BR - 1, cy))): p.ln(a, b, INNER, NAVY, j=0)
        for sg in (-1, 1):
            pts = [(cx + sg * (1.45 * BR - 1.05 * BR * math.cos(math.radians(t))), cy + 1.05 * BR * math.sin(math.radians(t))) for t in range(-60, 61, 6)]
            pts = [q_ for q_ in pts if math.hypot(q_[0] - cx, q_[1] - cy) < BR - 1.5]
            pline(p, pts, NAVY, INNER)
        p.stroke(circ, OUT, j=.05, step=99)
    return p
if __name__ == '__main__':
    p = build()
    offs = [p.V(SHIFT), p.V((-30, -46)), p.V((-14, -18)), (0, 0)]
    r = finish(p, 'basketball_hall', None, motion={'ball': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_basketball_hall_ball': dict(
        kind='توپ از زیر حلقه می‌افتد؛ حالت ایستا = پایان (نشسته کنار پایه)',
        translate_symbol_units=[list(SHIFT), [-30, -46], [-14, -18], [0, 0]], translate_map_px_start=[round(SHIFT[0] * K, 1), round(SHIFT[1] * K, 1)],
        duration_s=1.1, easing='ease-in (شتاب‌گرفتن)', loop=False, trigger='رسیدن کودک (یک‌بار)', reduced_motion='ایستا',
        note='تخته، حلقه، تور و ستون ثابت؛ بدون حلقهٔ بیکار.')}
    (OUTD / 'basketball_hall.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
