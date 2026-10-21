#!/usr/bin/env python3
"""ایستگاه M03 «رمپ بارگیری» (سرزمین شهر؛ بازسازی ۲۲ اکتبر طبق docs/STATION_SYMBOL_CRAFT_FA.md بخش ۶، راه‌حل الف):
نمای جانبی. تختهٔ بلند ~۲۴ درجه از زمین تا یک سکوی چوبی بالا؛ لبهٔ روشن و درز تخته‌ها؛ دو پایهٔ باز زیر تخته؛
بالای سکو یک تیرک طناب (بولارد) و پرچمک؛ جعبهٔ بنفش روی سطح تخته (هم‌جهت شیب) با طنابی که به تیرک بسته است.
لایهٔ متحرک: node_loading_ramp_crate (جعبه + طناب هم‌لایه). سر دور طناب با برشِ ثابتِ بیرونِ لایه و پشت تیرک پنهان است."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit5/loading_ramp'

import functools, station_kit as _k   # حاشیهٔ چپ/راست ≥۴px مثل نمونه‌های دیگر (کیت دست‌نخورده)
_k.margin_check = functools.partial(_k.margin_check, min_margin=4); _k.motion_check = functools.partial(_k.motion_check, min_margin=4)

# چوب: سه پله (پایه، روشن، تیره) برای تخته و برای سکو/پایه
PL_B = '#e9a65b'; PL_L = '#fff0c4'; PL_D = '#b8682a'
WD_B = '#c9772a'; WD_L = '#e29a52'; WD_D = '#8a4a1c'
CR_B = '#a678ff'; CR_L = '#d3bcff'; CR_D = '#6c42c9'; YEL = '#ffd84d'; ROPE = '#7a4418'; FLAG = '#e0553a'

GY = 14                                    # زمین
XA, YA = -36, -40                          # سر بالای سطح تخته = لبهٔ سکو
XB, YB = 38, -8                            # سر پایین سطح تخته
TH = 22                                    # ضخامت (عمودی) تخته
PX0 = -58                                  # لبهٔ چپ سکو
SLOPE = (YB - YA) / (XB - XA)
TH_ANG = math.atan(SLOPE)
U = (math.cos(TH_ANG), math.sin(TH_ANG))   # جهت سرازیری
N = (U[1], -U[0])                           # عمود بالا بر سطح
POST = (-50, -38)                           # تیرک طناب روی سکو
CW, CH = 28, 26                            # جعبه (در امتداد شیب، عمود شیب)
QX = -17                                   # x گوشهٔ بالا-پایینِ جعبه در حالت ایستا
DRISE = 16                                 # جابه‌جایی جعبه در امتداد شیب (از پایین تا حالت ایستا)
LEGS = (-22, 6)


def ys(x): return YA + (x - XA) * SLOPE            # سطح تخته
def yb(x): return ys(x) + TH                       # زیر تخته
def A(p, v, k=1): return (p[0] + v[0] * k, p[1] + v[1] * k)


def flat(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def rect(p, x0, y0, x1, y1, col, op=1): flat(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col, op)


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def leg(p, x, w=16):
    top = yb(x) - 4
    pts = [(x - w / 2, top), (x + w / 2, top), (x + w / 2, GY), (x - w / 2, GY)]
    p.shape(pts, WD_B, PART, j=.2, step=8)
    rect(p, x - w / 2 + 3.5, yb(x) + 4, x - w / 2 + 7, GY - 4, WD_L)
    flat(p, [(x + w / 2 - 6, top + 3), (x + w / 2 - 2, top + 3), (x + w / 2 - 2, GY - 1), (x + w / 2 - 6, GY - 1)], WD_D, .55)
    p.stroke(pts, PART, j=.2, step=8)


def build():
    p = Pen('loading_ramp', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    for x, r in ((-49, 20), (LEGS[0], 10), (LEGS[1], 10), (32, 12)): p.tipshadow(x, GY + 1, r)
    p.foot_tip(-52, GY - 1, 8); p.foot_tip(-42, GY - 1, 8); p.foot_tip(LEGS[0], GY, 7); p.foot_tip(LEGS[1], GY, 7); p.foot_tip(34, GY - 2, 9)
    for x in LEGS: leg(p, x)                                                    # پایه‌های باز زیر تخته
    # --- تخته: متوازی‌الاضلاع بلند (ضخامت عمودی TH) که زیر سکو ادامه دارد و پایینش روی زمین است
    PLK = [(XA - 8, ys(XA - 8)), (XB, YB), (XB, YB + TH), (XA - 8, ys(XA - 8) + TH)]
    p.shape(PLK, PL_B, OUT, j=.2, step=10)
    flat(p, [(XA, ys(XA) + TH - 4.5), (XB - 3, YB + TH - 4.5), (XB - 3, YB + TH - 2), (XA, ys(XA) + TH - 2)], PL_D, .6)     # سایهٔ زیر تخته
    flat(p, [(XA, ys(XA) + 4.2), (XB - 4, YB + 4.2), (XB - 4, YB + 7.8), (XA, ys(XA) + 7.8)], PL_L)                       # نوار روشن لبه
    for s in range(-24, 38, 13):                                                  # درز تخته‌های عرضی (عمود بر شیب، رنگ تخت)
        a = (s, ys(s)); b = A(a, N, -(TH * U[0] - 6)); a2 = A(a, N, -5.5)
        flat(p, [(a2[0] - 1.6 * U[0], a2[1] - 1.6 * U[1]), (a2[0] + 1.6 * U[0], a2[1] + 1.6 * U[1]),
                 (b[0] + 1.6 * U[0], b[1] + 1.6 * U[1]), (b[0] - 1.6 * U[0], b[1] - 1.6 * U[1])], PL_D)
    p.stroke(PLK, OUT, j=.2, step=10)
    # --- سکو: بلوک چوبی با دو درز افقی؛ روی سر تخته
    PF = [(PX0, YA), (XA, YA), (XA, GY), (PX0, GY)]
    p.shape(PF, WD_B, OUT, j=.2, step=10)
    rect(p, PX0 + 5, YA + 4, XA - 5, YA + 8, WD_L)
    for y in (-22, -8): rect(p, PX0 + 6, y - 1.9, XA - 6, y + 1.9, WD_D)
    flat(p, [(XA - 9, YA + 4), (XA - 4, YA + 4), (XA - 4, GY - 4), (XA - 9, GY - 4)], WD_D, .5)
    p.stroke(PF, OUT, j=.2, step=10)
    # --- تیرک طناب روی سکو (کنار لبه) + پین زرد
    pst = [(POST[0], YA - 17), (POST[1], YA - 17), (POST[1], YA + 3), (POST[0], YA + 3)]
    p.shape(pst, WD_B, PART, j=.15, step=8, clip=False)
    rect(p, POST[0] + 3.5, YA - 13, POST[0] + 7, YA - 2, WD_L)
    flat(p, [(POST[1] - 6, YA - 14), (POST[1] - 2, YA - 14), (POST[1] - 2, YA + 1), (POST[1] - 6, YA + 1)], WD_D, .55)
    p.stroke(pst, PART, j=.15, step=8)
    # --- پرچمک: میلهٔ تخت و پارچهٔ قرمز
    p.ln((-54, YA + 2), (-54, YA - 42), PART, ROPE, j=0)
    p.shape([(-54, YA - 42), (-32, YA - 42), (-39, YA - 34), (-35, YA - 26), (-54, YA - 26)], FLAG, INNER, j=.1, step=99, clip=False)
    disc(p, -54, YA - 43, 3, YEL)
    # --- جعبه و طناب (لایهٔ متحرک)؛ برش ثابت بیرونی: سر اضافی طناب چپ لبهٔ تیرک پنهان می‌ماند
    cx0 = p.X((POST[1], 0))[0]
    p.raw('<defs><clipPath id="loading_ramp_rope_clip"><rect x="%.1f" y="-400" width="500" height="800"/></clipPath></defs><g clip-path="url(#loading_ramp_rope_clip)">' % cx0)
    with layer(p, 'crate'):
        Q = (QX, ys(QX))
        hk = A(Q, N, 7)
        p.ln(A(hk, U, -60), A(hk, U, 3), INNER, ROPE, j=0)
        F = [Q, A(Q, U, CW), A(A(Q, U, CW), N, CH), A(Q, N, CH)]
        p.shape(F, CR_B, PART, j=.15, step=8, clip=False)
        flat(p, [A(A(Q, N, CH - 3.5), U, 3), A(A(Q, N, CH - 3.5), U, CW - 3), A(A(Q, N, CH - 7), U, CW - 3), A(A(Q, N, CH - 7), U, 3)], CR_L)
        for k in (CW * .38, CW * .62):                                            # دو تسمهٔ تیره (تخت)
            flat(p, [A(A(Q, N, 3), U, k - 1.8), A(A(Q, N, 3), U, k + 1.8), A(A(Q, N, CH - 9), U, k + 1.8), A(A(Q, N, CH - 9), U, k - 1.8)], CR_D)
        flat(p, [A(A(Q, N, 3), U, CW - 8), A(A(Q, N, 3), U, CW - 3.5), A(A(Q, N, CH - 9), U, CW - 3.5), A(A(Q, N, CH - 9), U, CW - 8)], CR_D, .55)
        p.stroke(F, PART, j=.15, step=8)
        c = A(Q, N, 6); disc(p, c[0] + U[0] * 1.5, c[1] + U[1] * 1.5, 2.4, YEL)
    p.raw('</g>')
    return p


XF = (1.0, -9.0, -3.0)
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
        translate_xy=[[sym_off[0], sym_off[1]], [0, 0]], unit='واحد symbol', dir_deg=round(math.degrees(TH_ANG), 1), easing='ease-in-out', loop=False,
        start='جعبه پایین‌تر روی شیب (جابه‌جایی +%.1f,+%.1f)' % tuple(sym_off), end='حالت ایستا (پایان): جعبه نزدیک سکو، چند واحد مانده به تیرک',
        note='جعبه و طناب (یک لایه) فقط در امتداد شیب و مماس بر سطح تخته به سمت سکو می‌روند؛ بدون چرخش. سر دور طناب با برش ثابتِ گروه بیرونیِ لایه و تیرک روی سکو پنهان می‌ماند و طناب همیشه به تیرک می‌رسد. تخته، سکو، پایه‌ها، تیرک و پرچمک ثابت‌اند. بدون دست و پیکان، بدون حلقهٔ بیکار؛ فقط هنگام رسیدن، یک‌بار، حدود ۲ ثانیه.'),
        'reduced_motion': 'جعبه در حالت ایستا (پایان)'}
    (OUTD / 'loading_ramp.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
