#!/usr/bin/env python3
"""ایستگاه M03 «رمپ بارگیری» (سرزمین شهر): تختهٔ بلند با شیب ملایم (~۲۶ درجه) و دو ریل کناری، بالای آن روی سکوی چوبی،
یک ستون چوبی با سوراخ برای طناب، و یک جعبهٔ قرمز روی شیب. لایهٔ متحرک: node_loading_ramp_crate (جعبه + طناب هم‌لایه)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit4/loading_ramp'

import functools, station_kit as _k   # D122/D123: حاشیهٔ چپ/راست ≥۴px (مثل نمونه‌های دیگر؛ کیت دست‌نخورده)
_k.margin_check = functools.partial(_k.margin_check, min_margin=4); _k.motion_check = functools.partial(_k.motion_check, min_margin=4)

W_L = '#fbdc9c'; W_M = '#eea94c'; W_D = '#c9782f'; W_DD = '#9a5a22'      # چوب گرم: روشن، میانه، تیره، تیره‌تر
CR_F = '#e5533d'; CR_T = '#f98a6c'; CR_S = '#b43a2c'; CR_B = '#ffe3a8'   # جعبهٔ قرمز زنده + تختهٔ کرم
ROPE = '#7a4418'; HOLE = '#3a2410'

ANG = 26
U = (math.cos(math.radians(ANG)), math.sin(math.radians(ANG)))      # جهت سرازیری (راست و پایین)
N = (U[1], -U[0])                                                   # عمود بالا بر شیب
DV = (9, -7)                                                        # عمق (پهنای تخته) در دید مایل
GY = 10                                                             # خط کف جلو
LR = 52                                                             # طول رمپ در امتداد شیب
TH = 6                                                              # ضخامت تخته
RAIL = 6
P0 = (-4, GY - 4)                                                   # گوشهٔ پایین-جلوی سطح رمپ
CW, CH = 22, 22                                                     # جعبه (در امتداد شیب، عمود شیب)
SQ = 40                                                             # فاصلهٔ لبهٔ بالایی جعبه از پایین رمپ (حالت ایستا)
LROPE = 24                                                          # طول طناب تا ستون
DRISE = 17                                                          # جابه‌جایی جعبه در امتداد شیب (از پایین تا حالت ایستا)


def A(p, v, k=1): return (p[0] + v[0] * k, p[1] + v[1] * k)
def on_slope(s, off=0): return A(A(P0, U, -s), DV, off)                # نقطه‌ای روی سطح رمپ: s از پایین، off کسری از عمق


P1 = on_slope(LR)
Q = on_slope(SQ, .18)                                                # گوشهٔ بالا-جلوی کف جعبه
QC = A(Q, N, CH / 2)                                                 # مرکز وجه بالادست جعبه (جای گره طناب)
C = A(QC, U, -LROPE)                                                 # مرکز سوراخ ستون
PX1 = P1[0] - 1                                                      # لبهٔ راست سکو
PX0 = C[0] - 13                                                      # لبهٔ چپ سکو (ستون ۲۶ واحد)
PTOP = P1[1]                                                         # بالای جلوی سکو = سطح رمپ در سر آن


def build():
    p = Pen('loading_ramp', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-30, GY + 1, 46); p.foot_tip(-24, GY - 1, 24)
    # --- سکوی چوبی (پشت): رویه، وجه راست، جلو
    pt = [(PX0, PTOP), (PX1, PTOP)]
    p.shape([(PX0, PTOP), (PX1, PTOP), A((PX1, PTOP), DV), A((PX0, PTOP), DV)], W_L, PART, j=.3, step=8)
    p.shape([(PX1, PTOP), A((PX1, PTOP), DV), A((PX1, GY), DV), (PX1, GY)], W_D, PART, j=.3, step=8)
    p.shape([(PX0, PTOP), (PX1, PTOP), (PX1, GY), (PX0, GY)], W_M, OUT, j=.4, step=8)
    for t in (.33, .66):
        x = PX0 + (PX1 - PX0) * t; p.ln((x, PTOP + 4), (x, GY - 3), INNER, W_DD, j=.1)
    p.ln((PX0 + 3, GY - 8), (PX1 - 3, GY - 8), INNER, W_DD, j=.1)
    # --- رمپ: وجه جلوی تخته (ضخامت)، سر پایین، سطح
    p.shape([P0, P1, A(P1, N, -TH), A(P0, N, -TH)], W_D, OUT, j=.3, step=9)
    p.shape([P0, A(P0, DV), A(A(P0, DV), N, -TH), A(P0, N, -TH)], W_DD, PART, j=.2, step=9)
    p.shape([P0, P1, A(P1, DV), A(P0, DV)], W_L, PART, j=.3, step=9)
    for s in (9, 20, 31, 42):                                                            # تخته‌های عرضی (موازی عمق)
        a = on_slope(s); p.ln(A(a, DV, .06), A(a, DV, .94), INNER, W_D, j=.1)
    # ریز پشتی
    b0, b1 = A(P0, DV), A(P1, DV)
    p.shape([b0, b1, A(b1, N, RAIL), A(b0, N, RAIL)], W_M, PART, j=.2, step=9)
    # --- طناب و جعبه (لایهٔ متحرک)
    with layer(p, 'crate'):
        a = A(QC, U, 0); b = C
        p.ln(b, a, PART, ROPE, j=.1)
        p.ln(A(b, N, 1.3), A(a, N, 1.3), INNER, '#c98a46', j=.1)
        # جعبه: جلو، بالا، وجه راست (دید مایل)
        d2 = (DV[0] * .55, DV[1] * .55)
        F = [Q, A(Q, U, CW), A(A(Q, U, CW), N, CH), A(Q, N, CH)]
        p.shape([F[1], A(F[1], d2), A(F[2], d2), F[2]], CR_S, PART, j=.2, step=9)
        p.shape([F[3], F[2], A(F[2], d2), A(F[3], d2)], CR_T, PART, j=.2, step=9)
        p.shape(F, CR_F, OUT, j=.3, step=9)
        p.ln(A(A(Q, U, 3), N, 3), A(A(Q, U, CW - 3), N, CH - 3), INNER, CR_B, j=.1)
        p.ln(A(A(Q, U, CW - 3), N, 3), A(A(Q, U, 3), N, CH - 3), INNER, CR_B, j=.1)
        k = A(QC, U, 1.5); p.raw('<circle cx="%.1f" cy="%.1f" r="3.4" fill="%s"/>' % (*p.X(k), HOLE))
    # --- ریل جلو (روی جعبه)
    p.shape([P0, P1, A(P1, N, RAIL), A(P0, N, RAIL)], W_M, PART, j=.2, step=9)
    p.ln(A(P0, N, RAIL - 1.5), A(P1, N, RAIL - 1.5), INNER, W_L, j=.1)
    # --- ستون با سوراخ طناب (روی سکو)
    pw = 26; ptop = C[1] - 17
    p.shape([(C[0] - pw / 2, PTOP + 3), (C[0] + pw / 2, PTOP + 3), (C[0] + pw / 2, ptop), (C[0] - pw / 2, ptop)], W_M, OUT, j=.3, step=8)
    p.shape([(C[0] + pw / 2, PTOP + 3), A((C[0] + pw / 2, PTOP + 3), DV, .6), A((C[0] + pw / 2, ptop), DV, .6), (C[0] + pw / 2, ptop)], W_D, PART, j=.2, step=8)
    p.shape([(C[0] - pw / 2, ptop), (C[0] + pw / 2, ptop), A((C[0] + pw / 2, ptop), DV, .6), A((C[0] - pw / 2, ptop), DV, .6)], W_L, PART, j=.2, step=8)
    p.shape(ell(C[0], C[1], 6.5, 6.5, 0, 360, 20), HOLE, INNER, j=.1, step=99)
    p.ln((C[0] - 9, PTOP - 4), (C[0] + 9, PTOP - 4), INNER, W_DD, j=.1)
    return p


def XFcalc():
    return (1.0, 0.0, 0.0)


XF = (1.0, 0.0, 0.0)
STAND = None
if __name__ == '__main__':
    import sys as _s
    if len(_s.argv) > 3: XF = tuple(float(v) for v in _s.argv[1:4])
    p = build()
    D = DRISE
    offs = [p.V((U[0] * D * f, U[1] * D * f)) for f in (1, .75, .5, .25, 0)]
    r = finish(p, 'loading_ramp', STAND, motion={'crate': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sym_off = [round(v, 1) for v in p.V((U[0] * D, U[1] * D))]
    sp['motion_spec'] = {'node_loading_ramp_crate': dict(
        translate_xy=[[sym_off[0], sym_off[1]], [0, 0]], unit='واحد symbol', dir_deg=ANG, easing='ease-in-out', loop=False,
        start='جعبه پایین رمپ (جابه‌جایی +%.1f,+%.1f)' % tuple(sym_off), end='حالت ایستا: نیمهٔ شیب',
        note='جعبه و طناب با هم در امتداد شیب (مماس بر تخته) بالا می‌روند؛ سر طناب پشت ستون ثابت پنهان می‌ماند. بدون دست و پیکان، بدون حلقهٔ بیکار؛ فقط هنگام رسیدن.'),
        'reduced_motion': 'جعبه در حالت ایستا (نیمهٔ شیب)'}
    (OUTD / 'loading_ramp.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
