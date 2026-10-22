#!/usr/bin/env python3
"""ایستگاه F02 «سالن بسکتبال» (سرزمین ورزشگاه، سکوی sports #7fbf4a). شناسه basketball_hall.
طرح قطعه‌به‌قطعه (واحد symbol، مرکز هندسی hero روی x=0 و سپس xf او را چپ می‌برد؛ کف y=4):
 1) پایه (بلوک): مستطیل 56x16، y -12..4، آبی-فولادی؛ سه پله STEEL B/L/D؛ خط PART.
 2) ستون: مستطیل 14 پهن، y -90..-12 روی محور x=0، همان آبی-فولادی (خط PART، رنگ دیدنی ~8).
 3) تخته: مستطیل 70x46، x -35..35، y -138..-92، سفید-آبی خیلی روشن (B/L/D)؛ خط PART؛ ستون زیر آن با هم‌پوشانی 2 واحد داخل تخته.
 4) مربع هدف: 24x16 روی محور، y -121..-105، قرمز تخت با خط INNER (قرمز-مرجان، نه نارنجی).
 5) تور (لایهٔ متحرک node_basketball_hall_net): ذوزنقه بالا ±19 (زیر رینگ)، پایین ±11، y -92..-50، سفید با خط INNER و دو قطر تخت آبی روشن.
 6) رینگ: بیضی تخت rx22 ry7 مرکز (0,-92) قرمز-مرجان با خط INNER + سوراخ بیضی تیره rx14 ry3.2؛ جلوی تور.
قهرمان: خاکستری-آبی (~215°) + سفید + قرمز کوچک؛ سکو 100° ⇒ اختلاف >100°. بدون توپ.
حرکت: فقط تور؛ حالت ایستا = پایان؛ بدون بیکار."""
import sys, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/basketball_hall'

S_B, S_L, S_D = '#7f9bc8', '#b4c8e8', '#566f9c'
W_B, W_L, W_D = '#e6edfb', '#ffffff', '#c9d6ee'
RED, RED_D, HOLE = '#e0553a', '#9c2f1c', '#4a1f4a'
NETL = '#5f7fb8'
XF = (1.0, -22.0, -4.0)
GY = 4
PX = 18                     # محور ستون؛ لبهٔ راستش ۶ داخل لبهٔ راست تخته (29 در برابر 35)
PW = 7                      # نیم‌پهنای ستون
BX0, BX1, BY0, BY1 = -45, 31, -140, -86   # تخته 84x60، مرکز x=-7 = محور رینگ و مربع
RIMY = -86
RX = -7                     # محور رینگ/تور/مربع (چپ ستون)
SWAY = 3


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def mpoly(p, pts, fill, sw):
    d = 'M' + 'L'.join('%.1f,%.1f' % z for z in p.X(pts)) + 'Z'
    p.raw('<path d="%s" fill="%s" class="eo" stroke-width="%s" stroke-linejoin="miter" stroke-miterlimit="6"/>' % (d, fill, sw))


def build():
    p = Pen('basketball_hall', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((-56, 12), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(PX + 1, GY + 3, 34); p.foot_tip(PX, GY + 2, 24)
    # 2) ستون (زیر پایه و زیر تخته؛ ۶ واحد هم‌پوشانی با پایه، بالا داخل تخته)
    pole = [(PX - PW, -100), (PX + PW, -100), (PX + PW, -6), (PX - PW, -6)]
    p.shape(pole, S_B, PART, j=.1, step=8)
    poly(p, [(PX - 4, -96), (PX - 1.5, -96), (PX - 1.5, -14), (PX - 4, -14)], S_L)
    poly(p, [(PX + 2, -96), (PX + 4.2, -96), (PX + 4.2, -14), (PX + 2, -14)], S_D)
    p.stroke(pole, PART, j=.1, step=8)
    # 1) پایه
    base = [(PX - 22, -12), (PX + 22, -12), (PX + 23, GY), (PX - 23, GY)]
    p.shape(base, S_B, PART, j=.1, step=8)
    poly(p, [(PX - 18, -7), (PX - 14, -7), (PX - 14, GY - 4), (PX - 18, GY - 4)], S_L)
    poly(p, [(PX + 8, -9), (PX + 19, -9), (PX + 19, GY - 2), (PX + 8, GY - 2)], S_D)
    p.stroke(base, PART, j=.1, step=8)
    # 3) تخته
    bd = [(BX0, BY0), (BX1, BY0), (BX1, BY1), (BX0, BY1)]
    p.shape(bd, W_B, PART, j=.1, step=8)
    poly(p, [(BX0 + 5, BY0 + 6), (BX0 + 9, BY0 + 6), (BX0 + 9, BY1 - 6), (BX0 + 5, BY1 - 6)], W_L)
    poly(p, [(BX1 - 16, BY0 + 4), (BX1 - 3, BY0 + 4), (BX1 - 3, BY1 - 3), (BX1 - 16, BY1 - 3)], W_D)
    p.stroke(bd, PART, j=.1, step=8)
    # 4) مربع هدف
    mpoly(p, [(RX - 9, -124), (RX + 9, -124), (RX + 9, -112), (RX - 9, -112)], RED, INNER)
    # 5) تور
    with layer(p, 'net'):
        net = [(RX - 12, RIMY), (RX + 12, RIMY), (RX + 8, -44), (RX - 8, -44)]
        mpoly(p, net, W_B, INNER)
        for a, b in (((-6, -78), (0, -56)), ((6, -78), (0, -56))):   # زیگزاگ ساده V؛ سرها ۱۲ از هم
            p.ln((RX + a[0], a[1]), (RX + b[0], b[1]), INNER, NETL, j=0)
        mpoly(p, net, 'none', INNER)
    # 6) رینگ
    p.shape(ell(RX, RIMY, 16, 7, 0, 360, 24), RED, INNER, j=.05, step=99, clip=False)
    p.fill(ell(RX, RIMY, 10.5, 3.2, 0, 360, 20), HOLE)
    return p


if __name__ == '__main__':
    p = build()
    offs = [p.V((-SWAY, 0)), p.V((SWAY, 0)), (0, 0)]
    r = finish(p, 'basketball_hall', None, motion={'net': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    top = p.X((RX, RIMY))
    sp['motion_spec'] = {'node_basketball_hall_net': dict(
        kind='تور آویزان زیر رینگ؛ حالت ایستا = حالت پایان (راست‌ایستاده)',
        pivot_map_symbol=[round(v, 1) for v in top], transform='rotate حول لبهٔ بالای تور؛ پایین تور ±%d واحد (≈±%.1fpx)' % (SWAY, SWAY * K),
        keyframes_deg=[0, -4, 4, -2.5, 1.5, 0], duration_s=1.4, easing='ease-in-out (میرا)', loop=False,
        trigger='رسیدن کودک (یک‌بار)', reduced_motion='ایستا',
        note='رینگ، تخته، ستون و پایه ثابت؛ بدون توپ؛ بدون حلقهٔ بیکار.')}
    (OUTD / 'basketball_hall.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
