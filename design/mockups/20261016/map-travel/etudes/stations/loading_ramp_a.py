#!/usr/bin/env python3
"""M03 «رمپ بارگیری» نسخهٔ A، دور ۳ (ساده، یک‌تکه): ۴ جزء.
۱) پایهٔ پهن و کوتاه #b8743a با رویهٔ روشن (۳۶×۳۶)  ۲) تختهٔ نازک ۱۲ واحدی، بلند (طول روی شیب ≈۷۰)، #f7d894، زاویه ۲۰°؛
لبهٔ بالای تخته در y بالای پایه شروع می‌شود (بدون بیرون‌زدگی) و ۶ واحد زیر پایه می‌رود (هم‌پوشانی)؛ زیر تخته خالی (بدون مثلث پر)
۳) جعبهٔ چوبی ۱۴×۱۴ هم‌شیب، ۴ واحد در تخته فرو رفته، با سایهٔ تماس کوچک (لایهٔ متحرک node_loading_ramp_a_crate)
۴) یک سایهٔ تماس واحد زیر پایه و پای رمپ. خط براق سکو دورتر از پای رمپ. بدون طناب. ΔE تخته/پایه ≥۳۰."""
import sys, pathlib, json, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit7/loading_ramp_a'
import functools, station_kit as _k
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8); _k.inside_check = functools.partial(_k.inside_check, min_margin=8)


W_B = '#f7d894'; BLK = '#b8743a'; BLK_L = '#e0a468'
CR = '#f2a63e'; CR_D = '#cf7e26'
GY = 18; XR = 14
HB, BW, TH, CS, SINK = 38, 36, 13, 17, 4
ANG = math.radians(24); TAN = math.tan(ANG)
U = (-math.cos(ANG), -math.sin(ANG)); NUP = (math.sin(ANG), -math.cos(ANG))
T_END, RISE = 26, 18


def A(p, v, k=1): return (p[0] + v[0] * k, p[1] + v[1] * k)
def flat(p, pts, col, op=1): p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def build():
    p = Pen('loading_ramp_a', 'city'); pad(p, line=((42, 28), (58, 25)), tri=((-24, -30), (66, 6)), dot=(60, -16)); p.xf = XF
    TYR = GY - TH; by0 = GY - HB
    XL = XR - (TYR - by0) / TAN              # بالای تخته در XL دقیقاً y=by0
    bx1 = XL + 6; bx0 = bx1 - BW
    p.tipshadow((bx0 + XR) / 2, GY + 1, (XR - bx0) / 2 - 8)
    p.foot_tip((bx0 + XR) / 2, GY, 12)
    lx = XL + (XR - XL) * .55; ty = lambda x: TYR - (XR - x) * TAN
    flat(p, [(lx, ty(lx) + 3), (lx + 7, ty(lx + 7) + 3), (lx + 7, GY - 1), (lx, GY - 1)], '#8f5a2c')   # پایهٔ نازک
    p.shape([(XL, by0), (XR, TYR), (XR, GY), (XL, by0 + TH)], W_B, PART, j=.1, step=10)
    p.shape([(bx0, by0), (bx1, by0), (bx1, GY), (bx0, GY)], BLK, PART, j=.1, step=12)
    flat(p, [(bx0 + 3, by0 + 3), (bx1 - 3, by0 + 3), (bx1 - 3, by0 + 10), (bx0 + 3, by0 + 10)], BLK_L)
    with layer(p, 'crate'):
        P = (XR + U[0] * T_END, TYR + U[1] * T_END)
        a = A(P, NUP, -SINK); b = A(a, U, CS); c = A(b, NUP, CS); e = A(a, NUP, CS)
        flat(p, [A(P, U, -2), A(P, U, CS + 2), A(A(P, U, CS + 2), NUP, -3), A(A(P, U, -2), NUP, -3)], '#10083a', .3)   # سایهٔ تماس
        p.shape([a, b, c, e], CR, PART, j=.1, step=8, clip=False)
        q = A(a, NUP, 3)
        flat(p, [A(q, U, 3), A(q, U, CS - 3), A(A(q, U, CS - 3), NUP, 3), A(A(q, U, 3), NUP, 3)], CR_D)
    return p


XF = (0.88, 20.0, 8.0)
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
