#!/usr/bin/env python3
"""M01 «دروازهٔ شهر» (سکوی city) — R6b: دروازهٔ ساده، نه قلعه. دو ستون سنگی ضخیم، سردر طاق تخت، تابلو، دو لنگهٔ چوبی باز، جادهٔ سنگ‌فرش. بدون برج و کنگره.
لایهٔ متحرک: node_city_gate_door (لنگهٔ راست؛ از نیمه‌بسته تا حالت ایستا=باز)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from station_kit import *
from g6h import *
from r6lib import extrude, box3
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/city_gate'
S_B, S_L, S_D = '#f1dba8', '#fff6dc', '#c9a96c'
S_M = '#dcc58c'
W_B, W_L, W_D = '#a8672f', '#e0a96a', '#6e3f18'
HOLE = '#5a4690'; YEL = '#ffd84d'; ROAD = '#e6dcc0'; ROAD_J = '#a89870'
BASE = 6; DD = (14, -9)
PX0, PX1, IX = 58, 36, 36     # ستون: x از ±58 تا ±36 (عرض ۲۲)


def build():
    p = Pen('city_gate', 'city'); pad(p, line=((50, 30), (70, 27)), tri=((36, -22), (74, 6)), dot=(68, -14)); p.xf = (.93, -5, 4)
    p.tipshadow(4, BASE + 4, 62)
    p.foot_tip(-44, BASE + 2, 12); p.foot_tip(52, BASE + 2, 12)
    # سنگ‌فرش جلو و داخل دهانه
    road = [(-30, -20), (30, -20), (52, 31), (-52, 31)]
    p.shape(road, ROAD, PART, j=.15, step=8, clip=False)
    for a, b in (((-10, -16), (-18, 28)), ((10, -16), (18, 28)), ((-40, 14), (40, 14)), ((-34, 2), (34, 2))):
        p.ln(a, b, INNER, ROAD_J, j=.1)
    # پس‌زمینهٔ دهانه (عمق تیره)
    poly(p, R(-IX, -58, IX, BASE - 8), HOLE)
    poly(p, [(-IX, -20), (IX, -20), (30, -20), (-30, -20)], HOLE)
    # لنگهٔ چپ (ثابت، باز): ذوزنقهٔ چوبی چسبیده به ستون
    lf = [(-IX + 2, BASE - 1), (-IX + 2, -54), (-24, -48), (-24, -2)]
    p.shape(lf, W_B, INNER, j=.05, step=7, clip=False)
    poly(p, [(-IX + 5, -48), (-IX + 9, -46), (-IX + 9, BASE - 8), (-IX + 5, BASE - 6)], W_L)
    p.ln((-IX + 14, -48), (-IX + 14, BASE - 6), INNER, W_D, j=.05); disc(p, -28, -22, 2.6, YEL)
    with layer(p, 'door'):
        rf = [(IX - 2, BASE - 1), (IX - 2, -54), (24, -48), (24, -2)]
        p.shape(rf, W_B, INNER, j=.05, step=7, clip=False)
        poly(p, [(IX - 5, -48), (IX - 9, -46), (IX - 9, BASE - 8), (IX - 5, BASE - 6)], W_L)
        p.ln((IX - 14, -48), (IX - 14, BASE - 6), INNER, W_D, j=.05); disc(p, 28, -22, 2.6, YEL)
    # ستون‌ها
    for sgn in (-1, 1):
        x0, x1 = (-PX0, -PX1) if sgn < 0 else (PX1, PX0)
        box3(p, x0, -72, x1, BASE, DD, S_B, S_L, S_D, sw=OUT)
        poly(p, R(x0 + 3, -66, x0 + 7, BASE - 10), S_L)
        for y in (-48, -26, -6):
            p.ln((x0 + 2, y), (x1 - 2, y), INNER, '#b8975a', j=.05)
    # سردر طاق تخت (روی ستون‌ها، هم‌پوشان ≥۱۴)
    arch = [(-PX0, -92), (PX0, -92), (PX0, -58), (IX, -58)] + [(IX - 72 * t / 12.0, -58 - 9 * math.sin(math.pi * t / 12.0)) for t in range(1, 12)] + [(-IX, -58), (-PX0, -58)]
    extrude(p, arch, DD, S_B, S_L, S_D, sw=OUT)
    poly(p, R(-PX0 + 4, -88, PX0 - 4, -85), S_L, .8)
    # تابلوی سردر روی سردر
    sb = R(-27, -116, 27, -86)
    p.shape(sb, W_B, OUT, j=.05, step=7, clip=False)
    poly(p, R(-24, -113, 24, -108), W_L); poly(p, R(-24, -93, 24, -89), W_D)
    disc(p, 0, -101, 8, YEL)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'city_gate', STAND, motion={'door': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_city_gate_door': dict(
        type='scaleX افقی حول لولا (لبهٔ بیرونی لنگه، چسبیده به ستون راست)', hinge_x_symbol=round(p.X((36, 0))[0], 1), scale_from=2.2, scale_to=1.0,
        duration_s=1.4, easing='ease-out', loop=False, start='لنگهٔ راست نیمه‌بسته (پهن‌تر)', end='حالت ایستا: کاملاً باز (کنار ستون)',
        note='فقط هنگام رسیدن، یک‌بار؛ لنگهٔ چپ، ستون‌ها و جاده ثابت؛ بدون حلقهٔ بیکار.'), 'reduced_motion': 'باز (حالت ایستا)'}
    (OUTD / 'city_gate.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
