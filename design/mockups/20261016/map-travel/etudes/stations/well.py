#!/usr/bin/env python3
"""ایستگاه E07 «چاه آب» (سرزمین مزرعه، سکوی farm ۵۰°) — دور ۶ (R6): بزرگ‌تر، دلوِ درشت و آشکار.
طرح (واحد symbol؛ مرکز چاه x=0؛ کف y=8؛ دهانه y=-26):
 ۱) بدنهٔ سنگی استوانه‌ای rx=42، y -26..8، سه پله (#b4c3d6 / #d6e1ee / #8798b3) با سه ردیف آجر منحنی؛ لبهٔ روشن و دهانهٔ تیره rx=31.
 ۲) دو ستون چوبی قهوه‌ای تیره x ±36 (۱۴ پهن) از لبه تا y=-100؛ قرقرهٔ کرم افقی y=-82 (۷۴ پهن، ۲۰ بلند).
 ۳) سقف دوشیبهٔ قرمز: مثلث ±60 از y=-96 تا -124، لبهٔ پیش‌آمده تیره، سایهٔ تیز راست.
 ۴) دستهٔ چرخان طلایی راست: میلهٔ محور + بازو + دستگیرهٔ گرد.
 ۵) دلوی چوبی نارنجی درشت (لایهٔ bucket): دهانهٔ بیضی ۳۰ پهن، ۲۴ بلند، دو بند فلزی، دستهٔ فلزی کمانی و طناب از قرقره، وسط قاب روی محور x=0.
حرکت: node_well_bucket ۱۰ واحد بالا؛ پایان = پایین (ایستا)؛ یک‌بار؛ بدون حلقهٔ بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from station_kit import *
from g4_helpers import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/well'

S_B, S_L, S_D = '#b4c3d6', '#d6e1ee', '#8798b3'
R_B, R_L, R_D = '#c23a2c', '#e8604c', '#7a1f19'
W_B, W_L, W_D = '#8a5a2a', '#b88048', '#5e3a18'
C_B, C_L, C_D = '#f6e6b8', '#fff8dc', '#c99a58'
B_B, B_L, B_D = '#f08a2e', '#ffb866', '#b85a14'
M_B, M_L = '#aab8cc', '#e6eef8'
ROPE = '#6b4a2a'; HOLE = '#1f3560'; WATER = '#4f86c6'; YEL = '#ffd84d'
HW, RIM_Y, BASE = 42, -26, 8
SPY, PX = -82, 36
BUCKET_DY = -10


def bucket(p):
    p.ln((0, SPY), (0, -68), 2.6, ROPE, j=0)
    ty, by = -54, -30
    body = [(-15, ty), (15, ty)] + ell(0, by, 12, 4.4, 0, 180, 14)[::-1][::-1]
    body = [(-15, ty), (15, ty), (12, by)] + [q for q in ell(0, by, 12, 4.4, 0, 180, 14)] + [(-12, by)]
    # بدنه: ذوزنقه با کف بیضی
    body = [(-15, ty), (15, ty)] + ell(0, by, 12, 4.4, 0, 180, 14)
    # دستهٔ فلزی (پشت دلو)
    arcline(p, ell(0, ty, 14, 14, 180, 360, 16), '#241a5e', 6.2)
    arcline(p, ell(0, ty, 14, 14, 180, 360, 16), M_B, 2.6)
    sharp(p, body, B_B, 2.6)
    poly(p, [(-12, ty + 3), (-8, ty + 3), (-6.5, by - 1), (-9.5, by - 1)], B_L)
    poly(p, [(7.5, ty + 3), (13.8, ty + 3), (11.2, by - .5), (7, by - .5)], B_D)
    for y in (-47, -36):
        w = 15 - (y - ty) * 3 / 24
        poly(p, [(-w, y), (w, y), (w - .4, y + 4), (-w + .4, y + 4)], M_B)
        poly(p, [(-w + 1.5, y + .6), (-w + 5, y + .6), (-w + 5, y + 2), (-w + 1.5, y + 2)], M_L)
    p.shape(ell(0, ty, 15, 4.8, 0, 360, 24), B_D, 2.6, j=.05, step=99, clip=False)
    p.fill(ell(0, ty + .6, 11, 2.8, 0, 360, 20), '#3a1c08')
    disc(p, 0, -68, 3.2, M_B)


def build(out=OUTD):
    p = Pen('well', 'farm'); pad(p, line=((16, 27), (34, 24)), tri=((62, -26), (76, 8)), dot=(70, -14)); p.xf = (1.0, 0, 6)
    p.tipshadow(0, BASE + 3, 44); p.foot_tip(0, BASE + 2, 36)
    body = [(-HW, RIM_Y), (HW, RIM_Y)] + ell(0, BASE - 10, HW, 10, 0, 180, 20)
    p.shape(body, S_B, 3.6, j=.15, step=8)
    poly(p, rect(-HW + 5, -22, -HW + 10.5, -3), S_L)
    k = math.acos(18 / HW)
    arc = [(HW * math.cos(a * k / 10), BASE - 10 + 10 * math.sin(a * k / 10)) for a in range(11)]
    poly(p, [(18, RIM_Y + 2), (HW, RIM_Y + 2)] + arc, S_D)
    for y in (-18, -10): poly(p, band(0, y, HW - 1, 10, 3.2), S_D)
    for y0, y1, xs in ((-15, -10, (-26, -6, 16)), (-7, -4, (-34, -14, 8, 28))):
        for x in xs:
            r_ = 10 * math.sqrt(max(0, 1 - (x / (HW - 1)) ** 2))
            poly(p, rect(x - 1.6, y0 + r_, x + 1.6, y1 + r_), S_D)
    p.stroke(body, 3.6, j=.15, step=8)
    p.shape(ell(0, RIM_Y, HW, 13, 0, 360, 40), S_L, 3.6, j=.05, step=99, clip=False)
    p.fill(ell(0, RIM_Y + 2.5, 32, 9.5, 0, 360, 32), HOLE)
    p.fill(ell(0, RIM_Y + 1.2, 33, 10.5, 200, 340, 20) + ell(0, RIM_Y + 3.6, 31.5, 8.6, 340, 200, 20), '#f2f6fb')
    poly(p, [(-9, RIM_Y + 6), (9, RIM_Y + 6), (7, RIM_Y + 8), (-7, RIM_Y + 8)], WATER)
    with layer(p, 'bucket'):
        bucket(p)
    sp = rect(-PX - 3, SPY - 10, PX + 3, SPY + 10)
    sharp(p, sp, C_B, 2.6)
    poly(p, rect(-PX + 2, SPY - 7, PX - 2, SPY - 3.5), C_L)
    for x in (-18, 0, 18): poly(p, rect(x - 2, SPY + 1, x + 2, SPY + 6.5), C_D)
    for s in (-1, 1):
        c = s * PX
        pts = rect(c - 7, -100, c + 7, RIM_Y + 3)
        sharp(p, pts, W_B, 2.6)
        poly(p, rect(c - 4.5, -95, c - 2, RIM_Y - 1), W_L)
        poly(p, rect(c + 1.8, -95, c + 4.8, RIM_Y - 1), W_D)
    roof = [(-60, -96), (60, -96), (0, -124)]
    sharp(p, roof, R_B, 3.6)
    poly(p, [(-9, -118), (-5, -118), (-33, -101), (-37, -101)], R_L)
    poly(p, [(7, -118), (50, -100.5), (50, -96), (7, -96)], R_D)
    poly(p, [(-52, -100), (52, -100), (60, -96), (-60, -96)], R_D)
    # دستهٔ چرخان
    sharp(p, rect(PX + 6, SPY - 3.5, PX + 16, SPY + 3.5), W_D, 2.6)
    sharp(p, [(PX + 11, SPY - 4), (PX + 19, SPY - 1), (PX + 31, SPY + 15), (PX + 24, SPY + 20)], YEL, 2.6)
    p.shape(ell(PX + 29, SPY + 19, 7.5, 7.5, 0, 360, 16), '#f0b020', 2.6, j=.05, step=99, clip=False)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'well', STAND, motion={'bucket': dict(offsets=[(0, BUCKET_DY), (0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_well_bucket': dict(offsets=[[0, BUCKET_DY], [0, 0]], dy_units=BUCKET_DY, dy_px=round(BUCKET_DY * K, 1), duration_s=2, repeat=1, ease='ease-in-out',
                                                  note='دلو با طناب ۱۰ واحد از بالا آهسته پایین می‌آید و در حالت ایستا (پایین) می‌ماند؛ سر طناب پشت قرقره؛ بدون حلقهٔ بیکار.'),
                         'reduced_motion': 'دلو ثابت در حالت پایین'}
    (OUTD / 'well.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
