#!/usr/bin/env python3
"""ایستگاه «کارخانهٔ کشتی‌سازی» (بازطراحی ۱۷ اکتبر): قایق چوبی کوچک روی دو پایهٔ چوبی (قایق در حال ساخت)، سکوی دریایی.
بدنهٔ منحنی (هلال)، دکل مستقیم، یک بادبان مثلثی ساده. پایه‌ها ثابت‌اند و تا زیر بدنه بالا آمده‌اند.
لایهٔ متحرک node_shipyard_hull = بدنه + دکل + بادبان؛ فقط کمی بالا و پایین می‌رود (پایه‌ها همیشه زیر بدنه کامل‌اند)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit3/shipyard'
HULL = '#e8803a'; HULL_D = '#b85a1c'; HULL_L = '#ffc46b'; SAIL = '#fff3c4'; SAIL_B = '#ef6a4a'; MAST = '#8a5f0c'; WOOD = '#ffd84d'; WOOD_D = '#d9961c'
BOB = 3


def bez(p0, c, p1, n=14):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1])
            for t in [i / n for i in range(n + 1)]]


DY = -10


def cradle(p):
    """دو پایهٔ چوبی مستطیلی (نه گوه): از کف تا زیر بدنه."""
    for x in (-46, -14):
        p.tipshadow(x, 13, 12); p.foot_tip(x, 11, 5)
        p.shape([(x - 10, -4), (x + 10, -4), (x + 10, 13), (x - 10, 13)], WOOD, INNER, j=.2, step=6)
        p.ln((x - 4, 6), (x + 4, 6), INNER, WOOD_D, j=.1)


def boat(p):
    """قایق بادبانی با بدنهٔ کشیده: بدنهٔ نیم‌تخت با دماغهٔ تیز و پاشنهٔ بلند (نه کاسه)، یک دکل راست، یک بادبان بزرگ مثلثی و پرچم کوچک."""
    Y = lambda pts: [(x, y + DY) for x, y in pts]
    # بادبان بزرگ، بعد دکل روی لبهٔ چپ آن، بعد بدنه؛ پایهٔ دکل زیر بدنه پنهان است
    p.shape(Y([(-27, -90), (-27, -34), (8, -36)]), SAIL, INNER, j=.1, step=4, clip=False)
    p.shape(Y([(-52, -62), (-52, -34), (-33, -36)]), SAIL_B, INNER, j=.1, step=4, clip=False)      # بادبان کوچک جلو (کنار دکل)
    p.ln((-27, -94 + DY), (-27, -14 + DY), PART, MAST, j=.1, probe='دکل (جزء)')
    p.shape(Y([(-66, -28), (-36, -25), (-8, -26), (12, -33), (2, -2), (-10, 10), (-56, 10), (-62, -6)]), HULL, PART, j=.15, step=99)   # بدنهٔ کشیده با دماغهٔ بالا
    p.ln((-52, -14), (-10, -14), INNER, HULL_L, j=.05)                                  # یک خط روشن موازی لبهٔ بدنه


def build(out=OUTD):
    p = Pen('shipyard', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = (1.0, 5.0, 0.0)
    cradle(p)
    with layer(p, 'hull'): boat(p)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    offs = [(0, 0), p.V((0, -BOB))]
    r = finish(p, 'shipyard', STAND, motion={'hull': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(layer='node_shipyard_hull', translate=[0, -BOB], note='بدنه+دکل+بادبان کمی بالا و پایین می‌رود؛ دو پایهٔ چوبی ثابت و تا زیر بدنه کامل‌اند')
    (OUTD / 'shipyard.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
