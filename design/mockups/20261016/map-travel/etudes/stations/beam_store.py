#!/usr/bin/env python3
"""ایستگاه M05 «انبار تیرآهن» (شهر، پالت city)، دور ۶: سه تیرآهن I درشت و سه‌بعدی (¾) روی هم، دو تا پایین و یکی بالا.
هر تیر: مقطع I (بال ۱۶، جان ۱۸، پهنا ۵۲، ارتفاع ۴۸) بیرون‌کشیده با عمق (17,-12) به پشت-راست؛ رخ جلو #b9cdf0 (میانی)، رویهٔ بال‌ها #f6f9ff (روشن)،
 پهلو #7f86c8 (تیره)؛ نوار برق باریک روی بال بالایی. بست زرد (#ffd84d) روی رویهٔ تیر بالا (لایهٔ node_beam_store_prop همراه تیر بالا).
 مرکز دو تیر پایین x=∓27؛ تیر بالا مرکز x=0. فلز روشن روی سکوی تیرهٔ شهر. سایهٔ تماس زیر دو تیر پایین. حرکت: تیر بالا از ۸ واحد بالاتر می‌نشیند (یک‌بار)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from r6lib import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/beam_store'
FR, TP_, SD, MD = '#b9cdf0', '#f6f9ff', '#7f86c8', '#9aa8dc'
YEL, YEL_D = '#ffd84d', '#c9891a'
W, H, TF, TW = 52, 48, 16, 18
D = (17, -12)
G = 12; OX = -8; DROP = 8


def I0(cx, base):
    x0, x1 = cx - W / 2 + OX, cx + W / 2 + OX; w0, w1 = cx - TW / 2 + OX, cx + TW / 2 + OX; t, b = base - H, base
    return [(x0, t), (x1, t), (x1, t + TF), (w1, t + TF), (w1, b - TF), (x1, b - TF), (x1, b), (x0, b), (x0, b - TF), (w0, b - TF), (w0, t + TF), (x0, t + TF)]


def beam(p, cx, base, strap=False):
    f = I0(cx, base)
    extrude(p, f, D, FR, TP_, SD, mid=MD, sw=PART, sw_in=INNER)
    t = base - H
    rect(p, cx - W / 2 + OX + 5, t + 4, cx + W / 2 + OX - 12, t + 7.5, '#ffffff', .9)
    if strap:
        x0 = cx + OX - 11; x1 = cx + OX + 11
        poly(p, [(x0, t), (x1, t), (x1 + D[0], t + D[1]), (x0 + D[0], t + D[1])], YEL)
        poly(p, [(x0, t), (x1, t), (x1, t + TF), (x0, t + TF)], YEL)
        rect(p, x1 - 4, t + 2, x1, t + TF, YEL_D, .9)
        p.stroke([(x0, t), (x1, t), (x1, t + TF), (x0, t + TF)], INNER, j=0, step=6)


def build(out=OUTD):
    p = Pen('beam_store', 'city'); pad(p, line=((-52, 40), (-36, 43)), tri=((72, -22), (-74, 14)), dot=(78, 6))
    p.xf = (1.06, 4, 0)
    p.tipshadow(OX + 4, G + 1, 60); p.foot_tip(OX + 4, G, 48)
    beam(p, -27, G)
    beam(p, 27, G)
    with layer(p, 'prop'):
        beam(p, 0, G - H, strap=True)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'beam_store', STAND, motion={'prop': dict(offsets=[p.V((0, -DROP)), (0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_beam_store_prop': dict(translate_from=[0, -DROP], translate_to=[0, 0], dur_s=1.2, repeat=1, easing='ease-in',
                         note='تیر بالایی (با بست زرد) از %d واحد بالاتر آرام می‌نشیند و می‌ماند؛ دو تیر پایین ثابت؛ حالت ایستا = نشسته؛ بدون حلقهٔ بیکار.' % DROP),
                         'reduced_motion': 'تیر بالا در جای نشسته'}
    (OUTD / 'beam_store.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
