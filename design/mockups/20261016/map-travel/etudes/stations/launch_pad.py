#!/usr/bin/env python3
"""ایستگاه F05 «سکوی پرتاب» (سرزمین فضا، پالت space = #7a5cd0، رنگ‌مایهٔ ۲۵۶°). شناسه launch_pad.
طرح قطعه‌به‌قطعه (مختصات محلی، y منفی = بالا، محور موشک x=0، زمین GY=6؛ سپس XF):
  ۱ سایهٔ تماس + foot_tip؛ ۲ شعله (لایهٔ متحرک flame، پشت همه، رنگ تخت بدون خط مثل پرتوهای فانوس)؛
  ۳ دو پایهٔ فلزی (آبی-خاکستری سه‌پله، ۱۶×۱۸) در x=±[23..39]؛ ۴ دو بال مرجانی (ایستاده روی پایه‌ها، هم‌پوشانی ۴ با پایه)؛
  ۵ نازل فلزی؛ ۶ بدنهٔ سفید گرم ±۱۹ (سایهٔ تیز راست، نور چپ) + نوار خردلی؛ ۷ دریچهٔ گرد (حلقهٔ فلزی + شیشه)؛
  ۸ نوک نخودی (±۱۹ تا ±۶، گرد). همه روی یک محور x=0؛ فقط ۷٫۶/۵٫۸/۳٫۹.
رنگ‌ها: بدنه سفید-کرم، نوک نخودی (۴۵°)، خردلی (۴۰°)، بال مرجانی (۱۲°)، فلز (۲۱۵°)، شیشه، شعله (۲۵–۵۰°)؛ همه ≥۳۵° از ۲۵۶°.
حالت ایستا = پایان = شعلهٔ کوچک؛ بدون حلقهٔ بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/launch_pad'

W_B, W_L, W_D = '#fbf6ea', '#ffffff', '#d8cdb0'
N_B, N_D = '#ead59a', '#c3a762'
M_B, M_D = '#e3a82e', '#b07a12'
F_B, F_L, F_D = '#ef6a4a', '#ffb59c', '#c9452c'
S_B, S_L, S_D = '#dbe9f8', '#ffffff', '#a3bbd9'
NOZ = '#8aa3c8'; GLASS = '#cfeaff'
FL_O, FL_I = '#ff8a2a', '#ffe45c'

GY = 6
BW = 19
YB, YT = -22, -100
NT = -132
FX0, FX1 = 22, 35
FLAME_TOP = -10
XF = (1.0, -27, 8)


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def flame(p, s=1.0, sx=1.0):
    L = 19 * s
    o = [(-9 * sx, FLAME_TOP), (9 * sx, FLAME_TOP), (9 * sx, FLAME_TOP + .35 * L), (4.5 * sx, FLAME_TOP + .75 * L), (0, FLAME_TOP + L),
         (-4.5 * sx, FLAME_TOP + .75 * L), (-9 * sx, FLAME_TOP + .35 * L)]
    i = [(-4.5 * sx, FLAME_TOP), (4.5 * sx, FLAME_TOP), (4.5 * sx, FLAME_TOP + .3 * L), (0, FLAME_TOP + .62 * L), (-4.5 * sx, FLAME_TOP + .3 * L)]
    p.fill(o, FL_O); p.fill(i, FL_I)


def build(out=OUTD, fs=1.0, fsx=1.0):
    p = Pen('launch_pad', 'space'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    p.tipshadow(2, GY + 3, 34); p.foot_tip(-28, GY + 1, 10); p.foot_tip(28, GY + 1, 10)
    with layer(p, 'flame'):
        flame(p, fs, fsx)
    for sg in (-1, 1):
        a, b = sorted((sg * FX0, sg * FX1))
        blk = [(a, GY - 18), (b, GY - 18), (b, GY), (a, GY)]
        p.shape(blk, S_B, PART, j=.1, step=8)
        if sg < 0: poly(p, [(a + 4, GY - 14), (a + 7.5, GY - 14), (a + 7.5, GY - 3), (a + 4, GY - 3)], S_L)
        else: poly(p, [(b - 6, GY - 15), (b - 2, GY - 15), (b - 2, GY - 2), (b - 6, GY - 2)], S_D)
        p.stroke(blk, PART, j=.1, step=8)
    for sg in (-1, 1):
        fin = [(sg * 8, -64), (sg * 36, -26), (sg * 36, -8), (sg * 17, -8), (sg * 17, -18), (sg * 8, -18)]
        p.shape(fin, F_B, PART, j=.1, step=8)
        if sg < 0: poly(p, [(-33, -20), (-30, -20), (-30, -11), (-33, -11)], F_L)
        else: poly(p, [(36, -28), (36, -8), (26, -8)], F_D)
        p.stroke(fin, PART, j=.1, step=8)
    noz = [(-10, -24), (10, -24), (12, -8), (-12, -8)]
    p.shape(noz, NOZ, INNER, j=.05, step=99, clip=False)
    body = [(-BW, YB), (BW, YB), (BW, YT), (-BW, YT)]
    p.shape(body, W_B, OUT, j=.12, step=8)
    poly(p, [(-BW + 4, YT + 6), (-BW + 7.5, YT + 6), (-BW + 7.5, YB - 6), (-BW + 4, YB - 6)], W_L)
    poly(p, [(7, YT + 3), (BW, YT + 3), (BW, YB), (7, YB)], W_D)
    poly(p, [(-BW, -52), (7, -52), (7, -40), (-BW, -40)], M_B); poly(p, [(7, -52), (BW, -52), (BW, -40), (7, -40)], M_D)
    p.stroke(body, OUT, j=.12, step=8)
    p.shape(ell(0, -74, 10, 10, 0, 360, 18), S_D, INNER, j=.05, step=99, clip=False)
    disc(p, 0, -74, 6, GLASS); poly(p, [(-3.5, -78), (-1, -78), (-1, -75.5), (-3.5, -75.5)], '#ffffff')
    def edge(i): return (6 + (BW - 6) * (1 - (i / 12) ** 1.7), YT + (NT - YT) * i / 12)
    left = [(-edge(i)[0], edge(i)[1]) for i in range(13)]
    nose = left + [(-x, y) for x, y in left[::-1]]
    p.shape(nose, N_B, OUT, j=.12, step=8)
    poly(p, [(5, YT)] + [edge(i) for i in range(0, 11)] + [(5, edge(10)[1])], N_D)
    p.stroke(nose, OUT, j=.12, step=8)
    return p


if __name__ == '__main__':
    p = build()
    cx, cy = p.X((0, FLAME_TOP))
    r = finish(p, 'launch_pad', None, motion={'flame': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_launch_pad_flame': dict(transform_origin=[round(cx, 1), round(cy, 1)], from_state='شعلهٔ کوچک ایستا', scale_peak=[1.3, 1.5],
        flicker='سه بار بین ۱٫۵ و ۱٫۱ (scaleY) و scaleX هم‌جهت', end='برگشت به شعلهٔ کوچک ایستا', duration_s=1.5, repeat='یک‌بار هنگام رسیدن', purpose='تزئینی'),
        'reduced_motion': 'شعلهٔ کوچک ایستا', 'note': 'شعله رنگ تخت بدون خط (مثل پرتو فانوس)؛ موشک بلند نمی‌شود.'}
    (OUTD / 'launch_pad.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
