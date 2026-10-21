#!/usr/bin/env python3
"""ایستگاه M03 «رمپ بارگیری» (سرزمین شهر): تختهٔ بلند با شیب ملایم (~۲۶ درجه) و دو ریل کناری، بالای آن روی سکوی چوبی،
طناب تا سکو، و یک جعبهٔ قرمز روی شیب. لایهٔ متحرک: node_loading_ramp_crate (جعبه + طناب هم‌لایه)."""
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
DV = (9, -34) # عمق (پهنای تخته) در دید مایل
GY = 10                                                             # خط کف جلو
LR = 68 # طول رمپ در امتداد شیب
TH = 7 # ضخامت تخته
RAIL = 6
P0 = (2, GY - 6)                                                    # گوشهٔ پایین-جلوی سطح رمپ
CW, CH = 20, 20                                                     # جعبه (در امتداد شیب، عمود شیب)
SQ = 46 # فاصلهٔ لبهٔ بالایی جعبه از پایین رمپ (حالت ایستا)
DRISE = 18 # جابه‌جایی جعبه در امتداد شیب (از پایین تا حالت ایستا)
BW = 22 # پهنای سکوی چوبی بالای رمپ


def poly(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def A(p, v, k=1): return (p[0] + v[0] * k, p[1] + v[1] * k)
def on_slope(s, off=0): return A(A(P0, U, -s), DV, off)                # نقطه‌ای روی سطح رمپ: s از پایین، off کسری از عمق


P1 = on_slope(LR)
Q = on_slope(SQ, .3)                                                 # گوشهٔ بالا-جلوی کف جعبه
QC = A(on_slope(SQ, .5), N, 2)                                      # جای گره طناب (روی سطح، پشت جعبه)
PX1 = P1[0] + 1                                                      # لبهٔ راست سکو (رمپ به آن تکیه می‌دهد)
PX0 = PX1 - BW
PTOP = P1[1]                                                         # بالای جلوی سکو = سطح رمپ در سر آن
XC = PX1 + DV[0] * .5                                                         # برش ثابت طناب: سمت چپ آن (سر اضافی طناب) دیده نمی‌شود
ROPE_FAR = A(QC, U, -(QC[0] - XC) / U[0] - 40)                       # سر دور طناب (پشت سکو؛ با برش پنهان)
BTOP = PTOP                                                      # بالای سکو (کمی بالاتر از سر رمپ)


def build():
    p = Pen('loading_ramp', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-24, GY + 1, 34); p.foot_tip(-24, GY - 1, 20)
    d6 = DV
    # --- سکو: وجه راست و رویه (پشت)
    p.shape([(PX1, BTOP), A((PX1, BTOP), d6), A((PX1, GY), d6), (PX1, GY)], W_D, INNER, j=.2, step=8)
    p.shape([(PX0, BTOP), (PX1, BTOP), A((PX1, BTOP), d6), A((PX0, BTOP), d6)], W_L, INNER, j=.2, step=8)
    # --- رمپ: یک خط دور برای کل تخته؛ داخل: سطح روشن، ضخامت تیره‌تر، سر پایین
    PB = [A(P0, N, -TH), P0, A(P0, DV), A(P1, DV), P1, A(P1, N, -TH)]
    p.shape(PB, W_D, OUT, j=.3, step=9)
    poly(p, [P0, P1, A(P1, DV), A(P0, DV)], W_L)
    poly(p, [P0, A(P0, DV), A(A(P0, DV), N, -TH), A(P0, N, -TH)], W_DD)
    for s in (8, 20, 32, 44, 56):                                                            # تخته‌های عرضی (موازی عمق)
        a = on_slope(s); p.ln(A(a, DV, .1), A(a, DV, .9), INNER, W_D, j=.1)
    p.ln(A(A(P0, DV, .86), U, -2), A(A(P1, DV, .86), U, 1), PART, W_DD, j=.1)              # ریل پشتی (خط)
    p.ln(A(A(P0, DV, .14), U, -2), A(A(P1, DV, .14), U, 1), PART, W_M, j=.1)               # ریل جلو (خط)
    p.stroke(PB, OUT, j=.3, step=9)
    # --- طناب و جعبه (لایهٔ متحرک). گروه بیرونی برش ثابت دارد: هرچه چپ XC است (سر اضافی طناب) دیده نمی‌شود.
    cx0 = p.X((XC, 0))[0]
    p.raw('<defs><clipPath id="loading_ramp_rope_clip"><rect x="%.1f" y="-400" width="500" height="800"/></clipPath></defs><g clip-path="url(#loading_ramp_rope_clip)">' % cx0)
    with layer(p, 'crate'):
        p.ln(ROPE_FAR, QC, PART, ROPE, j=.05)
        d2 = (DV[0] * .32, DV[1] * .32)
        F = [Q, A(Q, U, CW), A(A(Q, U, CW), N, CH), A(Q, N, CH)]
        p.shape([F[1], A(F[1], d2), A(F[2], d2), F[2]], CR_S, INNER, j=.2, step=9)
        p.shape([F[3], F[2], A(F[2], d2), A(F[3], d2)], CR_T, INNER, j=.2, step=9)
        p.shape(F, CR_F, OUT, j=.3, step=9)
        p.ln(A(A(Q, U, 5), N, 5), A(A(Q, U, CW - 5), N, CH - 5), INNER, CR_B, j=.1)
    p.raw('</g>')
    # --- جلوی سکو (روی سر تختهٔ رمپ)
    p.shape([(PX0, BTOP), (PX1, BTOP), (PX1, GY), (PX0, GY)], W_M, OUT, j=.4, step=8)
    return p


XF = (1.0, 10.0, 0.0)                                              # قاب قهرمان: بدون تغییر مقیاس، ۱۰ واحد به راست
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
        note='جعبه و طناب با هم در امتداد شیب (مماس بر تخته) بالا می‌روند؛ سر دور طناب با برش ثابتِ بیرونیِ لایه (کنار سکو) پنهان می‌ماند؛ طناب همیشه به سکو می‌رسد. بدون دست و پیکان، بدون حلقهٔ بیکار؛ فقط هنگام رسیدن.'),
        'reduced_motion': 'جعبه در حالت ایستا (نیمهٔ شیب)'}
    (OUTD / 'loading_ramp.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
