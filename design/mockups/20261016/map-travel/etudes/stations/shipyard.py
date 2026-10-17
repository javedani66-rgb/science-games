#!/usr/bin/env python3
"""ایستگاه «کارخانهٔ کشتی‌سازی» (M11): قهرمان = بدنهٔ نیمه‌ساختهٔ قایق روی لغزگاه (سطح شیب‌دار)، سکوی دریایی.
لغزگاه (گوهٔ چوبی) ثابت و پیوسته؛ لایهٔ متحرک node_shipyard_hull = بدنه + دکل/پرچم که ۰..۱۸ واحد روی شیب به پایین می‌لغزد."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit2/after/shipyard'
WOOD = '#ffd84d'; WOOD_D = '#d9961c'; HULL = '#ef6a4a'; BAND = '#ffd84d'; FLAG = '#7bd35a'; MAST = '#8a5f0c'
A = (-58, -6); B = (38, 22); FLOORY = 22
ANG = math.degrees(math.atan2(B[1] - A[1], B[0] - A[0]))
UX, UY = math.cos(math.radians(ANG)), math.sin(math.radians(ANG))
SLIDE = 18
S0 = 8                       # آغاز بدنه روی شیب (فاصله از A)


def ramp(p):
    p.tipshadow(-10, FLOORY - 2, 30); p.foot_tip(-10, FLOORY - 2, 14)
    p.shape([A, B, (B[0], FLOORY), (A[0], FLOORY)], WOOD, OUT, j=.2, step=8)
    # دو خط موازی با شیب (تختهٔ لغزگاه)
    p.ln((A[0] + 10, A[1] + 14), (-6, FLOORY - 6), INNER, WOOD_D, j=.1, probe='خط داخلی (تختهٔ لغزگاه)')


def hull(p):
    f = rot(A[0] + S0 * UX, A[1] + S0 * UY, ANG)
    T = lambda pts: [f(q) for q in pts]
    for x0 in (6, 34):
        p.shape(T([(x0, 0), (x0 + 15, 0), (x0 + 15, -14), (x0, -14)]), WOOD_D, PART, j=.1, step=99, clip=False)
    body = [(0, -11), (44, -11), (60, -24), (66, -40), (0, -40)]
    p.shape(T(body), HULL, OUT, j=.2, step=8)
    p.ln(f((7, -26)), f((54, -26)), INNER, CREAM, j=.1, probe='خط داخلی (کمربند بدنه)')
    p.ln(f((24, -40)), f((24, -70)), PART, MAST, j=.1, probe='دکل (جزء)')
    p.shape(T([(24, -70), (42, -65), (24, -60)]), FLAG, INNER, j=.1, step=99, clip=False)


def build(out=OUTD):
    p = Pen('shipyard', 'sea'); pad(p, line=((20, 29), (36, 27)), tri=((-54, -12), (54, 14)), dot=(56, -15))
    ramp(p)
    with layer(p, 'hull'): hull(p)
    return p


STAND = None     # خودکار: find_stand
if __name__ == '__main__':
    p = build()
    offs = [(SLIDE * k / 3 * UX, SLIDE * k / 3 * UY) for k in range(4)]
    r = finish(p, 'shipyard', STAND, motion={'hull': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(layer='node_shipyard_hull', translate_along_slope=[round(UX * SLIDE, 1), round(UY * SLIDE, 1)], note='بدنه روی لغزگاه تا ۱۸ واحد به پایین می‌لغزد و برمی‌گردد؛ لغزگاه ثابت و پیوسته')
    (OUTD / 'shipyard.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
