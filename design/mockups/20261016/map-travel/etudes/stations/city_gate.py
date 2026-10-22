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
BASE = 6; DD = (7, -5)
PX0, PX1, IX = 60, 38, 38     # ستون: x از ±58 تا ±36 (عرض ۲۲)


def build():
    p = Pen('city_gate', 'city'); pad(p, line=((50, 30), (70, 27)), tri=((36, -22), (74, 6)), dot=(68, -14)); p.xf = (.86, -4, 6)
    PX0_, PX1_ = 46, 22
    p.tipshadow(0, BASE + 4, 56)
    p.foot_tip(-34, BASE + 2, 12); p.foot_tip(34, BASE + 2, 12)
    # جادهٔ سنگ‌فرش از میان دو ستون
    road = [(-22, -30), (22, -30), (40, 27), (-40, 27)]
    p.shape(road, ROAD, PART, j=.15, step=8, clip=False)
    for a, b in (((-8, -24), (-14, 25)), ((8, -24), (14, 25)), ((-32, 13), (32, 13)), ((-27, 0), (27, 0))):
        p.ln(a, b, 1.6, ROAD_J, j=.1)
    # دو لنگهٔ چوبی باز: تختهٔ ضخیم کنار هر ستون، رو به عمق
    with layer(p, 'door'):
        extrude(p, R(PX0_ + 3, -64, PX0_ + 9, BASE - 1), (18, -12), W_D, W_L, W_B, sw=PART, sw_in=0)
        disc(p, PX0_ + 6, -30, 2.4, YEL)
    extrude(p, R(-PX0_ - 9, -64, -PX0_ - 3, BASE - 1), (-18, -12), W_D, W_L, W_B, sw=PART, sw_in=0)
    # دو ستون سنگی مکعبی (هر کدام یک مکعب بلند با کلاهک)
    for sgn in (-1, 1):
        x0, x1 = (-PX0_, -PX1_) if sgn < 0 else (PX1_, PX0_)
        extrude(p, R(x0, -88, x1, BASE), DD, S_B, S_L, S_D, sw=OUT, sw_in=0)
        for y in (-62, -36, -12):
            p.ln((x0 + 2, y), (x1 - 2, y), 1.2, '#b8975a', j=.05)
    # تیر افقی سنگی بین دو ستون (باریک؛ زیرش باز است)
    beam = R(-PX0_ - 4, -108, PX0_ + 4, -88)
    extrude(p, beam, DD, S_B, S_L, S_D, sw=OUT, sw_in=0)
    # تابلوی چوبی روی تیر
    sb = R(-24, -132, 24, -108)
    extrude(p, sb, (6, -4), W_B, W_L, W_D, sw=PART, sw_in=0)
    disc(p, 0, -120, 7, YEL)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'city_gate', STAND, motion={'door': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_city_gate_door': dict(
        type='scaleX افقی حول لولا (لبهٔ بیرونی لنگه، چسبیده به ستون راست)', hinge_x_symbol=round(p.X((IX - 5, 0))[0], 1), scale_from=2.2, scale_to=1.0,
        duration_s=1.4, easing='ease-out', loop=False, start='لنگهٔ راست نیمه‌بسته (پهن‌تر)', end='حالت ایستا: کاملاً باز (کنار ستون)',
        note='فقط هنگام رسیدن، یک‌بار؛ لنگهٔ چپ، ستون‌ها و جاده ثابت؛ بدون حلقهٔ بیکار.'), 'reduced_motion': 'باز (حالت ایستا)'}
    (OUTD / 'city_gate.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
