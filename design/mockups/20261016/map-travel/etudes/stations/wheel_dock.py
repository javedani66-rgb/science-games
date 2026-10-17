#!/usr/bin/env python3
"""ایستگاه «بارانداز» (M02) با station_kit: چرخ‌دندهٔ بزرگ روی سکوی آبی-سنگی (پالت دریایی). چرخ‌دنده = لایهٔ متحرک node_wheel_dock_gear."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent     # station_kit.HERE (etudes/) را نپوشاند

BR_T = '#ffd84d'; BR_L = '#f2b92c'; BR_R = '#d9961c'; BR_H = '#8a5f0c'


def gear_pts(cx, cy, R, n=8, depth=13):
    """چرخ‌دندهٔ n دندانه (ذوزنقه): شعاع بیرون R، ته دندانه R-depth. دندانه‌ها درشت تا لای دندانه زیر خط دور گم نشود."""
    pts = []; a = 360 / n
    for i in range(n):
        c = i * a
        for off, r in ((-a * .26, R - depth), (-a * .15, R), (a * .15, R), (a * .26, R - depth)):
            t = math.radians(c + off - 90); pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return pts


def gear(pen, cx, cy, R):
    """چرخ‌دندهٔ ایستادهٔ روبه‌رو: بدنه + حلقهٔ داخلی + چهار پرهٔ راست + توپی + یک خط درخشش."""
    pen.shape(gear_pts(cx, cy, R), BR_T, OUT, j=.4, step=99)
    pen.shape(ell(cx, cy, R * .62, R * .62, 0, 360, 36), BR_L, INNER, j=.3, clip=False)
    for k, a in enumerate((0, 90, 180, 270)):
        t = math.radians(a); c, sn = math.cos(t), math.sin(t)
        pen.ln((cx + 14 * c, cy + 14 * sn), (cx + R * .55 * c, cy + R * .55 * sn), PART, BR_H, j=.1, probe='پرهٔ چرخ‌دنده (جزء)' if a == 0 else None)
    pen.shape(ell(cx, cy, 13, 13, 0, 360, 24), BR_H, INNER, j=.3, clip=False)
    pts = [(cx + R * .47 * math.cos(math.radians(t)), cy + R * .47 * math.sin(math.radians(t))) for t in (205, 245)]
    pen.ln(pts[0], pts[1], INNER, CREAM, j=.1, probe='خط داخلی (درخشش)')


def build(out=HERE, legacy_shadow=False):
    p = Pen('wheel_dock', 'sea'); pad(p, line=((-60, 13), (-42, 18)), tri=((-58, -8), (61, 12)), dot=(56, -14))
    R = 46; cx, cy = -6, -42
    p.tipshadow(cx, cy + R - 1, 14); p.foot_tip(cx, cy + R - 1, 10)
    with layer(p, 'gear'): gear(p, cx, cy, R)
    return p, symbol(p, 'wheel_dock', ['gear'], out=out), (cx, cy)


STAND = (40, 6)     # px نقشه از مرکز سکو
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit'


if __name__ == '__main__':
    p, sym, c = build()
    r = finish(p, 'wheel_dock', STAND, motion={'gear': dict(rotate=c)}, out=HERE, shots=SHOTS)
    print(json.dumps(r, ensure_ascii=False, indent=1))
