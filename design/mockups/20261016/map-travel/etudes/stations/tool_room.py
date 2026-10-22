#!/usr/bin/env python3
"""M06 «اتاق ابزار» (شهر) — دور ۸ (تصمیم D155): تختهٔ چوبی ضخیم + چکش بزرگ ایستاده + آچار خوابیده. بدون میز و ابزار ریز.
لایهٔ متحرک node_tool_room_hammer: کج‌شدن ±۸° حول پای دسته؛ ایستا = پایان. خط داخلی نازک، بدون خط بین وجه‌ها."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from station_kit import *
from g4_helpers import *
from r6lib import extrude
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/tool_room'
W_F, W_T, W_S = '#e8b866', '#fbd990', '#b8843a'
S_F, S_T, S_S = '#c9d3e4', '#f6f9fd', '#7d8cab'
H_F, H_T, H_S = '#e2553d', '#ff9b84', '#9c2a1a'
Y_F, Y_T, Y_S = '#ffd84d', '#fff0a0', '#c9891a'
BY = -8                           # روی تخته (جلو)
HBASE = (-18, BY)                 # پای دستهٔ چکش
LEAN = -6


def rot(pts, a, c):
    r = math.radians(a); ca, sa = math.cos(r), math.sin(r)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


def build():
    p = Pen('tool_room', 'city'); pad(p, line=((60, 24), (76, 20)), tri=((-74, 4), (-66, 20)), dot=(72, -10)); p.xf = (1.0, 2, 8)
    p.tipshadow(0, 12, 58); p.foot_tip(-34, 8, 14); p.foot_tip(34, 8, 14)
    # ۱) تختهٔ ضخیم چوبی (دو تخته روی هم) با دو پایهٔ کوتاه
    for x0, x1 in ((-46, -28), (28, 46)):
        extrude(p, rect(x0, BY + 2, x1, 10), (10, -7), W_F, W_T, W_S, sw=OUT, sw_in=0)
    extrude(p, rect(-58, BY - 14, 58, BY + 4), (22, -15), W_F, W_T, W_S, sw=OUT, sw_in=0)
    p.ln((-50, BY - 6), (50, BY - 6), 1.4, '#c48f3e', j=.05)                           # درز دو تخته (مرز دو جزء)
    # ۲) آچار خوابیده روی تخته (راست)
    ox, oy = 14, BY - 17
    handle = [(0, 0), (52, 0), (52, -9), (0, -9)]
    jaw = [(-14, 5), (-14, -14), (-4, -19), (6, -14), (6, -9), (0, -9), (0, 0), (6, 0), (6, 5)]
    shape = rot(handle, -4, (0, 0))
    wr = [(x + ox, y + oy) for x, y in rot(handle + [(52, -4.5)], -4, (0, 0))][:4]
    extrude(p, [(x + ox, y + oy) for x, y in rot([(-14, 4), (-14, -8), (-3, -8), (-3, -14), (-14, -14), (-14, -24), (9, -24), (11, -10), (58, -10), (58, 0), (11, 0), (9, 4)], -4, (0, 0))], (8, -6), S_F, S_T, S_S, sw=PART, sw_in=0)
    disc(p, ox + 50, oy - 6, 2.4, S_S)
    # ۳) چکش درشت ایستاده (لایهٔ متحرک): دستهٔ قرمز + سر فولادی با چنگک
    with layer(p, 'hammer'):
        hx, hy = HBASE
        a = LEAN
        handle = rot(rect(hx - 6, hy - 70, hx + 6, hy), a, (hx, hy))
        extrude(p, handle, (6, -4), H_F, H_T, H_S, sw=OUT, sw_in=0)
        head = rot([(hx - 32, hy - 98), (hx + 26, hy - 98), (hx + 26, hy - 70), (hx - 20, hy - 70), (hx - 36, hy - 78), (hx - 44, hy - 92)], a, (hx, hy))
        extrude(p, head, (9, -6), S_F, S_T, S_S, sw=OUT, sw_in=0)
        band = rot(rect(hx - 6, hy - 70, hx + 6, hy - 60), a, (hx, hy))
        poly(p, band, Y_F)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'tool_room', STAND, motion={'hammer': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_tool_room_hammer': dict(pivot=[round(v, 1) for v in p.X(HBASE)], rotate_deg='کج‌شدن ایستا -6 → +2 → -6 (یک‌بار)', dur_s=1.2, once=True,
        note='چکش یک‌بار کمی کج می‌شود و برمی‌گردد؛ تخته و آچار ثابت؛ بدون حلقهٔ بیکار.'), 'reduced_motion': 'چکش ایستا'}
    (OUTD / 'tool_room.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')}, ensure_ascii=False)[:300])
