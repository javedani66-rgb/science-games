#!/usr/bin/env python3
"""M03 «رمپ بارگیری» نسخهٔ A، دور ۵: همان ایده (گوهٔ رمپ + جعبه روی شیب) ولی بزرگ‌تر، وسط و رمپ‌مانند، نه پنیر/میز.
طرح (واحد symbol، کف GY=22، مرکز x=0، عرض ≈۶۵٪ سکو):
 ۱) رمپ: یک چندضلعی چوبی #d7a762 (روشن #fbe6b4، تیره #b8864a): سکوی بالای تخت (طول ۲۲، ارتفاع ۵۸) در سمت چپ + شیب ≈۲۸° تا پنجهٔ راست (ارتفاع ۶).
 ۲) سطح تختهٔ رمپ: نوار روشن موازی سطح (سکو + شیب)، و ۵ پله‌چوب (کلیت) تیرهٔ عمود بر شیب (#8f5a2c)؛ نوار تیرهٔ کف.
 ۳) جعبهٔ بار ۳۶×۳۶ بنفش #8b5fd0 (روشن #b690ec، تیره #5f3a9e) هم‌شیب، ۳ واحد فرورفته؛ تسمهٔ روشن عمودی؛ لایهٔ node_loading_ramp_a_crate.
 ۴) سایهٔ تماس زیر کف + foot_tip. رنگ‌مایه: سکو ≈۲۱۰°، رمپ ≈۳۸°، جعبه ≈۲۶۵°."""
import sys, pathlib, json, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/loading_ramp_a'
W_BODY = '#d9a05a'; W_LIGHT = '#fbe6b4'; W_DARK = '#a8743a'; CLEAT = '#8f5a2c'
CR = '#8b5fd0'; CR_L = '#b690ec'; CR_D = '#5f3a9e'
GY = 18; X0, X1 = -57, 57; LAND = 20; HH, HT = 68, 6
CS, SINK = 38, 3
L2 = (X0 + LAND, GY - HH); TOE = (X1, GY - HT)
DX, DY = TOE[0] - L2[0], TOE[1] - L2[1]
SL = math.hypot(DX, DY); ANG = math.atan2(DY, DX)
D = (DX / SL, DY / SL)
N = (-D[1], D[0])
U = (-D[0], -D[1])
NUP = (-N[0], -N[1])
T0, RISE = 50, 18
XF = (1.0, 0, 0)


def A(p, v, k=1): return (p[0] + v[0] * k, p[1] + v[1] * k)
def flat(p, pts, col, op=1): p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def build():
    p = Pen('loading_ramp_a', 'city'); pad(p, line=((62, 30), (76, 26)), tri=((-76, -10), (-70, 12)), dot=(72, -14)); p.xf = XF
    p.tipshadow(0, GY + 1, 58); p.foot_tip(0, GY, 32)
    outline = [(X0, GY - HH), L2, TOE, (X1, GY), (X0, GY)]
    p.shape(outline, W_BODY, OUT, j=.1, step=12)
    # شیارهای تختهٔ بدنه (۳ خط افقی تیره، داخل بدنه)
    for yy in (GY - 16, GY - 32, GY - 48):
        xe = min(X1 - 14, L2[0] + (yy - L2[1]) * DX / DY - 16)
        flat(p, [(X0 + 7, yy - 1.5), (xe, yy - 1.5), (xe, yy + 1.5), (X0 + 7, yy + 1.5)], W_DARK)
    # سطح روشن: سکوی بالا + شیب
    flat(p, [(X0 + 6, GY - HH + 4.5), (L2[0] + 3, GY - HH + 4.5), (L2[0] + 3, GY - HH + 12.5), (X0 + 6, GY - HH + 12.5)], W_LIGHT)
    a = A(L2, N, 4.5); b = A(A(TOE, D, -9), N, 4.5)
    flat(p, [a, b, A(b, N, 8), A(a, N, 8)], W_LIGHT)
    for t in (24, 40, 56, 72, 88):
        c0 = A(A(L2, D, t), N, 3.5); c1 = A(c0, D, 4)
        flat(p, [c0, c1, A(c1, N, 10), A(c0, N, 10)], CLEAT)
    p.stroke(outline, OUT, j=.1, step=12)
    with layer(p, 'crate'):
        P = A(TOE, U, T0)
        a_ = A(P, NUP, -SINK); b_ = A(a_, U, CS); c_ = A(b_, NUP, CS); e_ = A(a_, NUP, CS)
        flat(p, [A(P, U, -2), A(P, U, CS + 2), A(A(P, U, CS + 2), NUP, -3), A(A(P, U, -2), NUP, -3)], '#10083a', .3)
        p.shape([a_, b_, c_, e_], CR, PART, j=.1, step=8, clip=False)
        Q = lambda u, v: A(A(a_, U, u), NUP, v)
        flat(p, [Q(9, CS - 9), Q(CS - 4.5, CS - 9), Q(CS - 4.5, CS - 4.5), Q(9, CS - 4.5)], CR_L)
        flat(p, [Q(4.5, 4.5), Q(9, 4.5), Q(9, CS - 4.5), Q(4.5, CS - 4.5)], CR_D)
    return p


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
