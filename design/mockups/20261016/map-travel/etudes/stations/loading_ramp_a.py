#!/usr/bin/env python3
"""M03 «رمپ بارگیری» نسخهٔ A، دور ۴ (بازطراحی ساده، یک جسم): ۳ جزء.
۱) گوهٔ پُر مثلث قائم (یک چندضلعی، یک خط دور OUT=7.6): کف افقی ۱۰۰ واحد، دیوارهٔ عمودی چپ ۵۰، پنجهٔ راست ۸ (برای ضخامت دیدنی)،
   شیب ≈۲۰٫۶°. بدنه (دیوارهٔ جانبی، تیره‌تر) #d7a762؛ سطح شیب‌دار = نوار روشن #fbe6b4 داخل دور؛ سایهٔ تیز راست #b8864a. بدون اتصال جدا.
۲) جعبهٔ مربع ۲۰×۲۰ بنفش #8b5fd0 (روشن #b690ec، تیره #5f3a9e) هم‌شیب، ۴ واحد در شیب فرو رفته (لایهٔ node_loading_ramp_a_crate).
۳) سایهٔ تماس زیر کف + foot_tip. رنگ‌مایه: سکو ≈۲۱۰°، گوه ≈۳۸°، جعبه ≈۲۶۵°. بدون طناب، بدون خال."""
import sys, pathlib, json, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/loading_ramp_a'
import functools, station_kit as _k
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8); _k.inside_check = functools.partial(_k.inside_check, min_margin=8)

W_BODY = '#d7a762'; W_LIGHT = '#fbe6b4'; W_DARK = '#b8864a'
CR = '#8b5fd0'; CR_L = '#b690ec'; CR_D = '#5f3a9e'
GY = 18; X0, X1 = -58, 42; HW, HT = 50, 8
CS, SINK = 20, 4
DX, DY = X1 - X0, HW - HT
ANG = math.atan2(DY, DX); L = math.hypot(DX, DY)
U = (-math.cos(ANG), -math.sin(ANG))          # بالا رفتن (به چپ و بالا)
NUP = (math.sin(ANG), -math.cos(ANG))         # بالا و کمی راست = بیرون از سطح
T0, RISE = 38, 18                             # فاصلهٔ کنج پایین جعبه از پنجه روی شیب؛ جابه‌جایی آغاز حرکت


def A(p, v, k=1): return (p[0] + v[0] * k, p[1] + v[1] * k)
def flat(p, pts, col, op=1): p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def build():
    p = Pen('loading_ramp_a', 'city'); pad(p, line=((42, 28), (58, 25)), tri=((-24, -30), (66, 6)), dot=(60, -16)); p.xf = XF
    cx = (X0 + X1) / 2
    p.tipshadow(cx, GY + 1, 46)
    p.foot_tip(cx, GY, 40)
    TOE = (X1, GY - HT); TOP = (X0, GY - HW)
    p.shape([TOP, TOE, (X1, GY), (X0, GY)], W_BODY, OUT, j=.1, step=12)
    d = ((TOE[0] - TOP[0]) / L, (TOE[1] - TOP[1]) / L); n = (-d[1], d[0])          # n = به درون (پایین)
    a = A(A(TOP, d, 9), n, 5.5); b = A(A(TOE, d, -9), n, 5.5)
    flat(p, [a, b, A(b, n, 7.5), A(a, n, 7.5)], W_LIGHT)                         # سطح شیب‌دار روشن
    flat(p, [(X0 + 6, GY - 10), (X1 - 6, GY - 10), (X1 - 6, GY - 4.5), (X0 + 6, GY - 4.5)], W_DARK)   # نوار تیرهٔ کف
    p.stroke([TOP, TOE, (X1, GY), (X0, GY)], OUT, j=.1, step=12)
    with layer(p, 'crate'):
        P = A(TOE, U, T0)                                                       # کنج پایین-راست جعبه روی شیب
        a_ = A(P, NUP, -SINK); b_ = A(a_, U, CS); c_ = A(b_, NUP, CS); e_ = A(a_, NUP, CS)
        flat(p, [A(P, U, -2), A(P, U, CS + 2), A(A(P, U, CS + 2), NUP, -3), A(A(P, U, -2), NUP, -3)], '#10083a', .3)
        p.shape([a_, b_, c_, e_], CR, PART, j=.1, step=8, clip=False)
        def Q(u, v): return A(A(a_, U, u), NUP, v)
        flat(p, [Q(9, CS - 9), Q(CS - 4.5, CS - 9), Q(CS - 4.5, CS - 4.5), Q(9, CS - 4.5)], CR_L)      # نور بالا
        flat(p, [Q(4.5, 4.5), Q(9, 4.5), Q(9, CS - 4.5), Q(4.5, CS - 4.5)], CR_D)                       # سایهٔ سمت پنجه
    return p


XF = (0.92, -6.0, -4.0)
if __name__ == '__main__':
    if len(sys.argv) > 3: XF = tuple(float(v) for v in sys.argv[1:4])
    p = build()
    offs = [p.V((-U[0] * RISE * f, -U[1] * RISE * f)) for f in (1, .75, .5, .25, 0)]
    r = finish(p, 'loading_ramp_a', None, motion={'crate': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']; so = [round(v, 1) for v in p.V((-U[0] * RISE, -U[1] * RISE))]
    sp['motion_spec'] = {'node_loading_ramp_a_crate': dict(translate_xy=[so, [0, 0]], unit='واحد symbol', dir_deg=round(math.degrees(ANG), 1),
        easing='ease-in-out', loop=False, start='جعبه پایین‌تر روی شیب (جابه‌جایی %.1f,%.1f)' % tuple(so), end='حالت ایستا = پایان (بالاتر)',
        note='فقط جعبه، در امتداد شیب؛ بدون چرخش، بدون طناب/دست/پیکان.'), 'reduced_motion': 'جعبه در حالت ایستا'}
    (OUTD / 'loading_ramp_a.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
