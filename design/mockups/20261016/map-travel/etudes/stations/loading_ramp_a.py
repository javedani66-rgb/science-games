#!/usr/bin/env python3
"""M03 «رمپ بارگیری» نسخهٔ A، دور ۶: رمپ چوبی ¾ سه‌بعدی (نیم‌رخ بیرون‌کشیده با عمق (-20,-12) به پشت-چپ) + جعبهٔ نارنجی روی شیب + چرخ‌دستی فیروزه‌ای.
اجزای درشت (۳): ۱) رمپ: بدنهٔ گوه‌ای چوبی (جلو #d9a05a، رویه #fbe6b4، پهلو #b8843a) با سکوی بالا و شیب ≈۳۲°؛ درز تخته‌های بدنه؛ ۲) نرده/ریل دو طرف شیب (جلو و پشت) چوب روشن؛
 ۳) جعبهٔ نارنجی (#f28c28 / #ffc070 / #b5560e) هم‌جهت شیب با تسمهٔ روشن (لایهٔ node_loading_ramp_a_crate)؛ (چرخ‌دستی در این دور حذف شد تا شلوغ نشود).
 حرکت: جعبه در امتداد شیب از ۲۰ واحد پایین‌تر بالا می‌آید؛ حالت ایستا = پایان؛ بدون حلقهٔ بیکار. سایهٔ تماس زیر رمپ و چرخ‌دستی."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from r6lib import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/loading_ramp_a'
W_F, W_T, W_S = '#ffc94a', '#fff0a8', '#d98a1c'
RL, RL_T = '#f0c27a', '#fff0c8'
C_F, C_T, C_S = '#e8431f', '#ff9a70', '#9a2410'
T_F, T_T, T_S = '#2fb5a8', '#7fe0d4', '#1d7a70'
GY = 14
D = (-20, -8)
XT, XP, XE = -56, 24, 48
HP = 84; HT = 6
T = (XT, GY - HT); H = (XP, GY - HP)
_l = math.hypot(H[0] - T[0], H[1] - T[1])
U = ((H[0] - T[0]) / _l, (H[1] - T[1]) / _l)    # بالاشیب
N = (U[1], -U[0])                               # عمود بالا (بالا-چپ)
S0, S1 = 52, 24                                 # فاصلهٔ پای جعبه از پنجه (ایستا / شروع)
CS = 40


def pt(P, v, k): return (P[0] + v[0] * k, P[1] + v[1] * k)


def build():
    p = Pen('loading_ramp_a', 'city'); pad(p, line=((62, 30), (76, 26)), tri=((-76, -4), (-70, 18)), dot=(76, -8)); p.xf = (1.05, 12, -2)
    p.tipshadow(-4, GY + 2, 60); p.foot_tip(-4, GY, 40)
    prof = [(XE, GY), (XE, GY - HP), H, T, (XT, GY)]
    extrude(p, prof, D, W_F, W_T, W_S, mid=W_T, sw=OUT, sw_in=PART)
    for yy in (GY - 20, GY - 40):
        xs = XT + 8 + (GY - 6 - yy) * (XP - XT) / (HP - HT) if yy > H[1] else XT
        rect(p, xs + 4, yy - 1.5, XE - 7, yy + 1.5, W_S, .85)
    for s_ in (30, 62, 94):
        a = pt(T, U, s_); b = (a[0] + D[0] * .92, a[1] + D[1] * .92)
        p.ln(a, b, INNER, W_S, op=.9, j=0)
    bk = lambda q: (q[0] + D[0], q[1] + D[1])
    a2, b2 = bk(T), bk(H)
    p.shape([a2, b2, (b2[0], b2[1] - 6), (a2[0], a2[1] - 6)], RL, INNER, j=.05, step=8, clip=False)
    with layer(p, 'crate'):
        P = pt(T, U, S0); P = (P[0] + D[0] * .16, P[1] + D[1] * .16)
        c = [P, pt(P, U, CS), pt(pt(P, U, CS), N, CS), pt(P, N, CS)]
        p.tipshadow(P[0] + 2, P[1] + 1, 8)
        extrude(p, c, (D[0] * .66, D[1] * .66), C_F, C_T, C_S, mid=C_F, sw=PART)
        q = lambda s, h: pt(pt(P, U, s), N, h)
        poly(p, [q(15, 3), q(24, 3), q(24, CS - 3), q(15, CS - 3)], '#ffd9a0', .9)
        poly(p, [q(CS - 6, 3), q(CS - 2, 3), q(CS - 2, CS - 3), q(CS - 6, CS - 3)], C_S, .5)
    p.shape([T, H, (H[0], H[1] - 6), (T[0], T[1] - 6)], RL, INNER, j=.05, step=8, clip=False)
    return p, None


if __name__ == '__main__':
    p, off = build()
    offs = [p.V((-U[0] * S1 * f, -U[1] * S1 * f)) for f in (1, .75, .5, .25, 0)]
    r = finish(p, 'loading_ramp_a', None, motion={'crate': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']; so = [round(v, 1) for v in offs[0]]
    sp['motion_spec'] = {'node_loading_ramp_a_crate': dict(translate_xy=[so, [0, 0]], unit='واحد symbol', dir_deg=round(math.degrees(math.atan2(U[1], U[0])), 1), easing='ease-in-out', loop=False,
        start='جعبه %d واحد پایین‌تر روی شیب' % S1, end='حالت ایستا = پایان (بالاتر)', note='فقط جعبه، در امتداد شیب؛ بدون چرخش، بدون طناب/دست/پیکان.'), 'reduced_motion': 'جعبه در حالت ایستا'}
    (OUTD / 'loading_ramp_a.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
