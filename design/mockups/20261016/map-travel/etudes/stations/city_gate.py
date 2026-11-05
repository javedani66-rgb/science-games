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
    from shapely.geometry import box as sbox
    p = Pen('city_gate', 'city'); pad(p, line=((50, 30), (70, 27)), tri=((36, -22), (74, 6)), dot=(68, -14)); p.xf = (.9, 0, 4)
    p.tipshadow(0, BASE + 4, 56)
    # جادهٔ سنگ‌فرش از دروازه تا جلوی سکو (جای ایستادن بچه آزاد)
    road = [(-18, -12), (18, -12), (36, 27), (-36, 27)]
    poly(p, road, ROAD)
    for a, b in (((-6, 0), (-10, 25)), ((6, 0), (10, 25)), ((-30, 14), (30, 14))):
        p.ln(a, b, 1.6, ROAD_J, j=.1)
    # بدنهٔ دروازه: یک قطعه با کنگره
    u = sbox(-50, -84, 50, BASE)
    for x0, x1 in ((-50, -34), (-8, 8), (34, 50)):
        u = u.union(sbox(x0, -100, x1, -84))
    from shapely.geometry import Polygon as SP
    arch_p = [(-25, BASE + 2), (-25, -44)] + [(25 * math.cos(math.radians(a)), -44 - 25 * math.sin(math.radians(a))) for a in range(180, -1, -15)] + [(25, -44), (25, BASE + 2)]
    u = u.difference(SP(arch_p))
    pts = list(u.exterior.coords)[:-1]
    extrude(p, pts, DD, S_B, S_L, S_D, sw=OUT, sw_in=0)
    for y in (-70, -44, -18):
        for x0, x1 in ((-47, -24), (24, 47)):
            p.ln((x0, y), (x1, y), 1.4, '#b8975a', j=.05)
    # دهانهٔ طاقی تیره
    arch = [(-19, BASE)] + [(-19 * math.cos(math.radians(a)), -44 - 19 * math.sin(math.radians(a))) for a in range(0, 181, 15)][::-1] + [(19, BASE)]
    arch = [(-19, BASE), (-19, -44)] + [(19 * math.cos(math.radians(a)), -44 - 19 * math.sin(math.radians(a))) for a in range(180, -1, -15)] + [(19, -44), (19, BASE)]
    # لنگه‌های چوبی باز، رو به جلو
    for sg in (-1, 1):
        q = [(sg * 25, -56), (sg * 25, BASE), (sg * 36, BASE + 8), (sg * 36, -48)]
        if sg > 0:
            with layer(p, 'door'):
                p.shape(q, W_B, PART, j=.1, step=8, clip=False)
                poly(p, [(sg * 27, -50), (sg * 27, 0), (sg * 30, 2), (sg * 30, -48)], W_L)
                disc(p, 33, -22, 2.2, YEL)
        else:
            p.shape(q, W_B, PART, j=.1, step=8, clip=False)
            poly(p, [(sg * 27, -50), (sg * 27, 0), (sg * 30, 2), (sg * 30, -48)], W_L)
            disc(p, -33, -22, 2.2, YEL)
    # تابلوی گرد زرد روی طاق
    p.shape(ell(0, -79, 11, 7, 0, 360, 20), YEL, PART, j=.05, step=99, clip=False)
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
