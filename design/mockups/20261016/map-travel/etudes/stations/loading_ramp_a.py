#!/usr/bin/env python3
"""M03 «رمپ بارگیری» نسخهٔ A (اصلاح پس از رد ناظر: شبیه پتک بود). نمای جانبی ساده، ۶ جزء:
۱) شیب مثلثی روشن زیر تخته (قاعدهٔ رمپ، #e2a25e)  ۲) تختهٔ ضخیم ۱۹ واحد، رنگ #f7d894، شیب ۲۶ درجه، دور PART=5.8 (هم‌خط با سکو)
۳) دو تختهٔ عرضی تخت (بدون خط، بدون نوار ریز)  ۴) بلوک تیرهٔ #a24f1c که بالای آن دقیقاً هم‌تراز بالاترین نقطهٔ تخته است
(گوشهٔ بالا-راست بلوک = گوشهٔ بالای تخته؛ تخته زیر بلوک می‌رود و از پهلوی آن بیرون می‌آید)
۵) جعبهٔ چوبی-نارنجی ساده ۲۰ واحد بدون راه‌راه، کفش روی لبهٔ بالای تخته، هم‌شیب. لایهٔ متحرک node_loading_ramp_a_crate = فقط جعبه.
بدون طناب. حرکت: جعبه از پایین تخته (۱۸ واحد پایین‌تر روی شیب) تا حالت ایستا (بالاتر)."""
import sys, pathlib, json, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit7/loading_ramp_a'
import functools, station_kit as _k
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8); _k.inside_check = functools.partial(_k.inside_check, min_margin=8)


W_B = '#f7d894'; W_X = '#e6bd6e'; WG = '#e2a25e'; BLK = '#a24f1c'; BLK_L = '#c06a2c'
CR = '#f0a244'; CR_D = '#d27f2a'
GY = 18; XR = 14
HB, BW, TH, CS = 46, 30, 19, 23
ANG = math.radians(26)
TAN = math.tan(ANG)
U = (-math.cos(ANG), -math.sin(ANG)); NUP = (math.sin(ANG), -math.cos(ANG))
T_END, RISE = 28, 18


def A(p, v, k=1): return (p[0] + v[0] * k, p[1] + v[1] * k)
def flat(p, pts, col): p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def build():
    p = Pen('loading_ramp_a', 'city'); pad(p, line=((34, 28), (52, 25)), tri=((-24, -30), (62, 6)), dot=(58, -16)); p.xf = XF
    TYR = GY - TH; by0 = GY - HB
    XL = XR - (TYR - by0) / TAN              # سر بالای تخته: بالای تخته در y=by0
    bx1 = XL; bx0 = bx1 - BW; XS = XL - 8     # تخته ۸ واحد زیر بلوک ادامه دارد
    TYS = by0 - 8 * -0 + 0
    TYS = TYR - (XR - XS) * TAN
    p.tipshadow(-4, GY + 1, 26); p.tipshadow(10, GY + 1, 8)
    p.foot_tip(-4, GY, 12); p.foot_tip(11, GY - 1, 5)
    # ۱) شیب مثلثی روشن
    p.shape([(bx1 - 2, TYS + TH), (XR, GY), (bx1 - 2, GY)], WG, PART, j=.1, step=12)
    # ۲) تخته
    p.shape([(XS, TYS), (XR, TYR), (XR, TYR + TH), (XS, TYS + TH)], W_B, PART, j=.1, step=10)
    # ۳) تخته‌های عرضی تخت
    for x0 in (XR - 9, XR - 38):
        for k in (0, 5):
            pass
        flat(p, [(x0, TYR - (XR - x0) * TAN + 4), (x0 + 5, TYR - (XR - x0 - 5) * TAN + 4), (x0 + 5, TYR - (XR - x0 - 5) * TAN + TH - 4), (x0, TYR - (XR - x0) * TAN + TH - 4)], W_X)
    # ۴) بلوک (روی تخته)
    p.shape([(bx0, by0), (bx1, by0), (bx1, GY), (bx0, GY)], BLK, PART, j=.1, step=12)
    flat(p, [(bx0 + 3, by0 + 3), (bx1 - 3, by0 + 3), (bx1 - 3, by0 + 9), (bx0 + 3, by0 + 9)], BLK_L)
    # ۵) جعبه
    with layer(p, 'crate'):
        a = (XR + U[0] * T_END, TYR + U[1] * T_END); b = A(a, U, CS); c = A(b, NUP, CS); e = A(a, NUP, CS)
        p.shape([a, b, c, e], CR, PART, j=.1, step=8, clip=False)
        q = A(a, NUP, 3)
        flat(p, [A(q, U, 3), A(q, U, CS - 3), A(A(q, U, CS - 3), NUP, 4), A(A(q, U, 3), NUP, 4)], CR_D)
    return p


XF = (0.88, 21.0, 9.0)
if __name__ == '__main__':
    if len(sys.argv) > 3: XF = tuple(float(v) for v in sys.argv[1:4])
    p = build()
    offs = [p.V((-U[0] * RISE * f, -U[1] * RISE * f)) for f in (1, .75, .5, .25, 0)]
    r = finish(p, 'loading_ramp_a', None, motion={'crate': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']; so = [round(v, 1) for v in p.V((-U[0] * RISE, -U[1] * RISE))]
    sp['motion_spec'] = {'node_loading_ramp_a_crate': dict(translate_xy=[so, [0, 0]], unit='واحد symbol', dir_deg=round(math.degrees(ANG), 1),
        easing='ease-in-out', loop=False, start='جعبه پایین‌تر روی شیب (جابه‌جایی %.1f,%.1f)' % tuple(so), end='حالت ایستا = پایان (بالاتر)',
        note='فقط جعبه؛ بدون چرخش، بدون طناب/دست/پیکان.'), 'reduced_motion': 'جعبه در حالت ایستا'}
    (OUTD / 'loading_ramp_a.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
