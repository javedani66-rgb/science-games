#!/usr/bin/env python3
"""ایستگاه «کارخانهٔ کشتی‌سازی» (M11): قهرمان = بدنهٔ نیمه‌ساختهٔ قایق روی لغزگاه (سطح شیب‌دار)، سکوی دریایی.
لغزگاه (گوهٔ چوبی) ثابت و پیوسته؛ لایهٔ متحرک node_shipyard_hull = بدنه + دکل/پرچم که روی شیب به پایین می‌لغزد.
طراحی دوباره برای خط ضخیم‌تر (D113، D110): لغزگاه گوهٔ بزرگ و ساده، بدنه یک تکه با یک دکل، پرچم بدون خط دور."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit2/after/shipyard'
XF = (1.0, 4.0, -2.0)            # قاب قهرمان: (مقیاس هندسه، dx، dy) در واحد symbol؛ ضخامت خط ثابت می‌ماند
WOOD = '#ffd84d'; WOOD_D = '#d9961c'; HULL = '#ef6a4a'; FLAG = '#7bd35a'; MAST = '#8a5f0c'
A = (-62, -12); B = (4, 12); FLOORY = 22
ANG = math.degrees(math.atan2(B[1] - A[1], B[0] - A[0]))
UX, UY = math.cos(math.radians(ANG)), math.sin(math.radians(ANG))
SLIDE = 6
S0 = 2                       # آغاز بدنه روی شیب (فاصله از A)


def ramp(p):
    p.tipshadow(-30, FLOORY - 2, 30); p.foot_tip(-30, FLOORY - 2, 14)
    p.shape([A, B, (B[0], FLOORY), (A[0], FLOORY)], WOOD, OUT, j=.2, step=8)
    p.ln((A[0] + 12, FLOORY - 8), (-24, FLOORY - 8), INNER, WOOD_D, j=.1, probe='خط داخلی (تختهٔ لغزگاه)')


def hull(p):
    f = rot(A[0] + S0 * UX, A[1] + S0 * UY, ANG)
    T = lambda pts: [f(q) for q in pts]
    p.shape(T([(0, -26), (0, -8), (10, 0), (44, 0), (56, -12), (62, -26)]), HULL, OUT, j=.2, step=8)
    p.ln(f((24, -26)), f((24, -64)), PART, MAST, j=.1, probe='دکل (جزء)')
    p.fill(T([(24, -64), (42, -58), (24, -52)]), FLAG)


def build(out=OUTD):
    p = Pen('shipyard', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    ramp(p)
    with layer(p, 'hull'): hull(p)
    return p


STAND = None     # خودکار: find_stand
if __name__ == '__main__':
    p = build()
    offs = [p.V((SLIDE * k / 3 * UX, SLIDE * k / 3 * UY)) for k in range(4)]
    r = finish(p, 'shipyard', STAND, motion={'hull': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(layer='node_shipyard_hull', translate_along_slope=[round(UX * SLIDE * p.xf[0], 1), round(UY * SLIDE * p.xf[0], 1)], note='بدنه روی لغزگاه تا %d واحد به پایین می‌لغزد و برمی‌گردد؛ لغزگاه ثابت و پیوسته' % SLIDE)
    (OUTD / 'shipyard.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
