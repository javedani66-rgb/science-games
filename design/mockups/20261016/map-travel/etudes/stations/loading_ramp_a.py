#!/usr/bin/env python3
"""M03 «رمپ بارگیری» نسخهٔ A (آزمون): نمای جانبی ساده، فقط چهار جزء درشت:
تختهٔ بلند و نازک (شیب حدود ۲۶ درجه، بالا-چپ)، بلوک چوبی زیر سر بالا، سر پایین روی زمین با سایهٔ تماس، و جعبهٔ نارنجی-قرمز
هم‌شیب با تخته که کفش مماس بر لبهٔ بالای تخته است (یک خط دور، نوار تسمهٔ روشن بدون خط دور).
بدون ستون/پرچم/تیرک/طناب/درز. لایهٔ متحرک node_loading_ramp_a_crate = فقط جعبه (ایستا = پایان، بالاترین جا)."""
import sys, pathlib, json, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit7/loading_ramp_a'
import functools, station_kit as _k
_k.margin_check = functools.partial(_k.margin_check, min_margin=4); _k.motion_check = functools.partial(_k.motion_check, min_margin=4)

W_B = '#e9a65b'; W_L = '#fbe0a8'; W_D = '#b8682a'; BLK = '#c9772a'; BLK_L = '#e29a52'; BLK_D = '#9a5420'
CR = '#f2552c'; CR_S = '#ffd98a'
GY = 18                       # زمین
XR, XL = 14, -52
HB, BW, OVER = 30, 34, 12              # لبهٔ راست (پایین) و چپ (بالا) تخته
ANG = math.radians(27)
TH = 19                       # ضخامت عمودی تخته
SL = -math.tan(ANG)           # dy/dx: سمت راست پایین‌تر (y بزرگ‌تر) ⇒ شیب منفی در x
def top_y(x): return (GY - TH) + (x - XR) * SL * -1 * -1 if False else (GY - TH) - (XR - x) * math.tan(ANG)
U = (-math.cos(ANG), -math.sin(ANG))        # بالا رفتن (چپ و بالا)
N = (-math.sin(ANG), math.cos(ANG))         # عمود به سمت پایین-راست؟ (پایین تخته)
NUP = (math.sin(ANG), -math.cos(ANG))       # عمود رو به بالا
CS = 24                                     # ضلع جعبه
T_END = 36                                  # فاصلهٔ لبهٔ پایین جعبه (مرکز کف) از سر پایین تخته در پایان
RISE = 26


def A(p, v, k=1): return (p[0] + v[0] * k, p[1] + v[1] * k)
def flat(p, pts, col): p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def build():
    p = Pen('loading_ramp_a', 'city'); pad(p, line=((34, 28), (52, 25)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    TYR = top_y(XR)
    p.tipshadow(-62, GY + 1, 22); p.tipshadow(6, GY + 1, 9)
    p.foot_tip(-62, GY, 10); p.foot_tip(12, GY - 1, 5)
    # بلوک (پایهٔ پهن و کوتاه، وجه بالا + جلو) اول کشیده می‌شود. گوشهٔ راست-بالای بلوک زیر تخته را می‌گیرد؛
    # سر بالای تخته کمی روی وجه بالای بلوک می‌نشیند (کف تخته روی لبهٔ بالا).
    by0 = GY - HB; bx1 = XR - HB / math.tan(ANG); bx0 = bx1 - BW; XL = bx1 - OVER
    TYL = top_y(XL)
    p.shape([(bx0, by0), (bx1, by0), (bx1, GY), (bx0, GY)], BLK, PART, j=.1, step=12)
    flat(p, [(bx0 + 3, by0 + 3), (bx1 - 3, by0 + 3), (bx1 - 3, by0 + 9), (bx0 + 3, by0 + 9)], BLK_L)            # وجه بالا (روشن)
    flat(p, [(bx0 + 3, GY - 8), (bx1 - 3, GY - 8), (bx1 - 3, GY - 3), (bx0 + 3, GY - 3)], BLK_D)
    B = [(XL, TYL), (XR, TYR), (XR, TYR + TH), (XL, TYL + TH)]
    p.shape(B, W_B, OUT, j=.15, step=10)
    flat(p, [(XL + 3, TYL + 3), (XR - 3, TYR + 3), (XR - 3, TYR + 3 + 3.6), (XL + 3, TYL + 3 + 3.6)], W_L)       # نوار روشن لبهٔ بالا
    flat(p, [(XL + 3, TYL + TH - 5.5), (XR - 3, TYR + TH - 5.5), (XR - 3, TYR + TH - 3), (XL + 3, TYL + TH - 3)], W_D)  # نوار تیرهٔ کف
    # جعبه
    with layer(p, 'crate'):
        base = (XR - T_END * math.cos(ANG) * 1, 0); base = (XR + U[0] * T_END, TYR + U[1] * T_END)   # روی لبهٔ بالا
        a = base; b = A(a, U, CS); c = A(b, NUP, CS); e = A(a, NUP, CS)
        a = A(a, NUP, .0)
        p.shape([a, b, c, e], CR, PART, j=.15, step=8, clip=False)
        s0, s1 = .40, .62                                                  # تسمهٔ روشن (بدون خط دور)
        q0 = A(a, NUP, 3); H = CS - 6
        flat(p, [A(q0, U, CS * s0), A(q0, U, CS * s1), A(A(q0, U, CS * s1), NUP, H), A(A(q0, U, CS * s0), NUP, H)], CR_S)
    return p


XF = (0.9, 14.0, 9.0)
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
