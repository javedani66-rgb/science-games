#!/usr/bin/env python3
"""ایستگاه M03 «رمپ بارگیری» (سرزمین شهر؛ نسخهٔ ۳: نمای سه‌چهارم ساده، تصمیم مالک ۲۲ اکتبر).
هم‌زبان سکوی بیضی از بالا: سطح بالای تختهٔ بلند = متوازی‌الاضلاع پهن و روشن با نوار لبه (بالا رفتن به چپ)،
لبهٔ جلویی ضخیم و وجه راست (سه رنگ چوب)، دو پایه، یک جعبهٔ بنفش روی شیب. بدون ستون، تیرک، پرچم، طناب و درز ریز.
لایهٔ متحرک node_loading_ramp_crate = فقط جعبه."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit6/loading_ramp'

import functools, station_kit as _k
_k.margin_check = functools.partial(_k.margin_check, min_margin=4); _k.motion_check = functools.partial(_k.motion_check, min_margin=4)

S_L = '#f7d894'; S_X = '#fff0c4'                    # سطح بالا و نوار لبه
F_B = '#e29a52'; F_D = '#b8682a'; F_E = '#9a5420'    # لبهٔ جلو: پایه، تیره (زیر)، وجه راست
LG = '#c9772a'
CR_B = '#a678ff'; CR_L = '#d3bcff'; CR_D = '#6c42c9'

GY = 14
BX0 = -44                                            # بلوک چوبی بالا (مکعب کوتاه سه‌وجهی)
P0 = (36, 2); P1 = (-24, -30)                        # لبهٔ بالای جلوی تخته: سر پایین (راست) تا سر بالا روی بلوک
TH = 12                                              # ضخامت عمودی لبهٔ جلو (باریک)
DV = (8, -16)                                       # عمق (پهنای تخته) به سمت بالا-راست
SL = (P1[1] - P0[1]) / (P1[0] - P0[0])
ANG = math.atan(SL)
U = (math.cos(ANG), math.sin(ANG))                   # سرازیری
CW, CH = 18, 16
QX = -10                                             # x گوشهٔ پایین-چپ جلوی جعبه در حالت ایستا
DRISE = 14


def A(p, v, k=1): return (p[0] + v[0] * k, p[1] + v[1] * k)
def yf(x): return P1[1] + (x - P1[0]) * SL                 # لبهٔ بالای جلو
def flat(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def build():
    p = Pen('loading_ramp', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    p.tipshadow(-34, GY + 1, 18); p.tipshadow(32, GY + 1, 9)
    p.foot_tip(-38, GY, 8); p.foot_tip(-28, GY, 8); p.foot_tip(34, GY - 2, 6)
    # بلوک چوبی: وجه بالا + وجه جلو (+ نوار تیره پایین)
    BT = [(BX0, P1[1]), (P1[0], P1[1]), A(P1, DV), A((BX0, P1[1]), DV)]
    p.shape(BT, S_L, PART, j=.2, step=9)
    flat(p, [A((BX0, P1[1]), DV, .1), A(P1, DV, .1), A(P1, DV, .26), A((BX0, P1[1]), DV, .26)], S_X)
    p.stroke(BT, PART, j=.2, step=9)
    BF = [(BX0, P1[1]), P1, (P1[0], GY), (BX0, GY)]
    p.shape(BF, F_B, OUT, j=.2, step=10)
    flat(p, [(BX0 + 4, GY - 9.5), (P1[0] - 4, GY - 9.5), (P1[0] - 4, GY - 4), (BX0 + 4, GY - 4)], F_D)
    p.stroke(BF, OUT, j=.2, step=10)
    # سطح تخته (متوازی‌الاضلاع پهن) + نوار لبه
    TOP = [P1, P0, A(P0, DV), A(P1, DV)]
    p.shape(TOP, S_L, PART, j=.2, step=10)
    flat(p, [A(P1, DV, .10), A(P0, DV, .10), A(P0, DV, .27), A(P1, DV, .27)], S_X)
    p.stroke(TOP, PART, j=.2, step=10)
    RF = [P0, A(P0, DV), A(A(P0, DV), (0, 1), TH), A(P0, (0, 1), TH)]
    p.shape(RF, F_E, PART, j=.2, step=10)
    with layer(p, 'crate'):
        Qf = A((QX, yf(QX)), DV, .24); dc = (DV[0] * .5, DV[1] * .5)
        Fr = [Qf, A(Qf, U, CW), A(A(Qf, U, CW), (0, -1), CH), A(Qf, (0, -1), CH)]
        p.shape([Fr[1], A(Fr[1], dc), A(Fr[2], dc), Fr[2]], CR_D, INNER, j=.1, step=7, clip=False)
        p.shape([Fr[3], Fr[2], A(Fr[2], dc), A(Fr[3], dc)], CR_L, INNER, j=.1, step=7, clip=False)
        p.shape(Fr, CR_B, PART, j=.15, step=8, clip=False)
    FF = [P1, P0, A(P0, (0, 1), TH), A(P1, (0, 1), TH)]          # لبهٔ جلوی باریک روی بلوک تا زمین
    p.shape(FF, F_B, PART, j=.2, step=10)
    return p


XF = (1.1, -18.0, 0.0)
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
        translate_xy=[[sym_off[0], sym_off[1]], [0, 0]], unit='واحد symbol', dir_deg=round(math.degrees(ANG), 1), easing='ease-in-out', loop=False,
        start='جعبه پایین‌تر روی شیب (جابه‌جایی +%.1f,+%.1f)' % tuple(sym_off), end='حالت ایستا (پایان): جعبه بالاتر روی سطح تخته',
        note='لایه فقط جعبه است (بدون طناب). جعبه در امتداد شیب سطح تخته (موازی لبهٔ جلو) بالا می‌رود؛ بدون چرخش. بقیه ثابت‌اند. بدون دست و پیکان، بدون حلقهٔ بیکار؛ فقط هنگام رسیدن، یک‌بار، حدود ۲ ثانیه.'),
        'reduced_motion': 'جعبه در حالت ایستا (پایان)'}
    (OUTD / 'loading_ramp.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
