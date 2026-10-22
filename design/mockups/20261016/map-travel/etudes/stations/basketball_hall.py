#!/usr/bin/env python3
"""ایستگاه F02 «سالن بسکتبال» (سرزمین ورزشگاه، سکوی sports #7fbf4a) — بازطراحی دور ۵.
ایدهٔ یک‌نگاه: تابلوی بسکتبال عمودی و وسط، رینگ نارنجی جلوی تخته، تور سفید زیر رینگ، پایه زیر آن؛ همه روی محور x=0 (مرکز سکو).
طرح قطعه‌به‌قطعه (واحد symbol؛ کف y=+4؛ بالاترین نقطه ≈ -138):
 ۱) پایه (بلوک): مستطیل 60x16 (x ±30، y -12..4)، آبی-فولادی (STEEL B/L/D)، خط PART.
 ۲) ستون: مستطیل 16 پهن (x ±8، y -92..-8) همان آبی-فولادی، پشت تور؛ بالا داخل تخته.
 ۳) تخته: مستطیل 96x56 (x ±48، y -138..-82) سفید-آبی خیلی روشن (B/L/D)، خط PART، سایهٔ تیز راست.
 ۴) مربع هدف: قرمز-مرجان 28x18 (x ±14، y -126..-108)، خط INNER، روی محور.
 ۵) تور (لایهٔ net): ذوزنقه بالا ±22 (y -88)، پایین ±12 (y -50)، سفید با خط INNER و شش خط مورب لوزی (آبی)؛ پشت رینگ، جلوی ستون.
 ۶) رینگ: بیضی تخت نارنجی (#ff8a1f) rx26 ry8 مرکز (0,-88)، خط INNER، سوراخ تیره؛ جلوی تور و تخته.
قهرمان: خاکستری-آبی/سفید/نارنجی روی سبز ⇒ کنتراست ارزشی؛ نارنجی ۳۰°، سکو ۱۰۰°. بدون توپ.
عرض ≈۵۰–۵۳٪ سکو. حرکت: فقط net (تاب میرا)؛ حالت ایستا = پایان؛ بدون بیکار."""
import sys, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8)
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/basketball_hall'

S_B, S_L, S_D = '#7f9bc8', '#b4c8e8', '#566f9c'
W_B, W_L, W_D = '#f1f5fc', '#ffffff', '#c9d6ee'
RED = '#e0553a'
OR_B, OR_L, OR_D = '#ff8a1f', '#ffc27a', '#b85a0a'
NET_B, NETL = '#ffffff', '#7f9bc8'
HOLE = '#4a1f4a'
GY = 4
BW, BT, BB = 48, -138, -82
RIMY = -88
SWAY = 3


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def rect(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def build():
    p = Pen('basketball_hall', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((-68, 14), (66, 8)), dot=(60, -18))
    p.xf = (1.0, 0.0, -4.0)
    p.tipshadow(0, GY + 3, 32); p.foot_tip(0, GY + 2, 28)
    # ۲) ستون
    pole = rect(-8, -92, 8, -6)
    p.shape(pole, S_B, PART, j=.1, step=8)
    poly(p, rect(-4.6, -86, -1.8, -14), S_L); poly(p, rect(2.2, -86, 4.8, -14), S_D)
    p.stroke(pole, PART, j=.1, step=8)
    # ۱) پایه
    base = rect(-26, -12, 26, GY)
    p.shape(base, S_B, PART, j=.1, step=8)
    poly(p, rect(-21, -7, -11, GY - 4), S_L); poly(p, rect(11, -8, 21, GY - 3), S_D)
    p.stroke(base, PART, j=.1, step=8)
    # ۳) تخته
    bd = rect(-BW, BT, BW, BB)
    p.shape(bd, W_B, PART, j=.1, step=8)
    poly(p, rect(-BW + 5, BT + 6, -BW + 10, BB - 6), W_L)
    poly(p, rect(BW - 17, BT + 5, BW - 4, BB - 4), W_D)
    p.stroke(bd, PART, j=.1, step=8)
    # ۴) مربع هدف
    q = rect(-14, -127, 14, -109)
    p.shape(q, RED, INNER, j=.05, step=99, clip=False)
    # ۵) تور
    with layer(p, 'net'):
        net = [(-22, RIMY), (22, RIMY), (12, -50), (-12, -50)]
        p.shape(net, NET_B, INNER, j=.05, step=99)
        tx = [-14, 0, 14]; bx = [-6.5, 0, 6.5]
        for i, j in ((0, 1), (1, 0), (1, 2), (2, 1)):
            p.ln((tx[i], RIMY + 8), (bx[j], -57), 2.6, NETL, j=0)
        p.stroke(net, INNER, j=.05, step=99)
    # ۶) رینگ
    ring = ell(0, RIMY, 26, 8, 0, 360, 32)
    p.shape(ring, OR_B, INNER, j=.05, step=99, clip=False)
    p.fill(ell(0, RIMY, 17, 4.2, 0, 360, 24), HOLE)
    p.fill(ell(0, RIMY + 7, 22, 1.2, 0, 180, 14), OR_L)
    return p


if __name__ == '__main__':
    p = build()
    offs = [p.V((-SWAY, 0)), p.V((SWAY, 0)), (0, 0)]
    r = finish(p, 'basketball_hall', None, motion={'net': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    top = p.X((0, RIMY))
    sp['motion_spec'] = {'node_basketball_hall_net': dict(
        kind='تور آویزان زیر رینگ؛ حالت ایستا = حالت پایان (راست‌ایستاده)',
        pivot_map_symbol=[round(v, 1) for v in top], transform='rotate حول لبهٔ بالای تور؛ پایین تور ±%d واحد (≈±%.1fpx)' % (SWAY, SWAY * K),
        keyframes_deg=[0, -4, 4, -2.5, 1.5, 0], duration_s=1.4, easing='ease-in-out (میرا)', loop=False,
        trigger='رسیدن کودک (یک‌بار)', reduced_motion='ایستا',
        note='رینگ، تخته، ستون و پایه ثابت؛ بدون توپ؛ بدون حلقهٔ بیکار.')}
    (OUTD / 'basketball_hall.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
