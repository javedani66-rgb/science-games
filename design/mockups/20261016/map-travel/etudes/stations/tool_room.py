#!/usr/bin/env python3
"""ایستگاه M06 «اتاق ابزار» (شهر، پالت city)، دور ۶: میز کار چوبی ¾ با رویهٔ ضخیم و عمق (16,-14)، چکش درشت ایستاده، انبردست زرد روی میز و گیرهٔ فولادی با دستهٔ زرد.
۴ جزء درشت: ۱) میز: رویه (جلو #e8b866، بالا #fbd990، پهلو #b8843a)، دو پایه، پیشانی/کشو #cf9a4a با دستگیرهٔ زرد.
 ۲) چکش (لایهٔ node_tool_room_hammer): دستهٔ قرمز #e2553d (سه پله)، سر فولادی #d4dce8/#f6f9fd/#8c9ab8 با چنگک؛ حرکت: کج‌شدن ±۸° حول پای دسته.
 ۳) انبردست: دو دستهٔ زرد #ffd84d و فک فولادی، پیچ وسط. ۴) گیره: بدنهٔ فولادی، فک جلو، دستهٔ زرد با گوی.
 سایهٔ تماس زیر پایه‌ها؛ فلز روشن/چوب گرم روی سکوی تیرهٔ شهر."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from r6lib import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/tool_room'
W_F, W_T, W_S = '#e8b866', '#fbd990', '#b8843a'
A_F = '#cf9a4a'
S_F, S_T, S_S = '#d4dce8', '#f6f9fd', '#8c9ab8'
H_F, H_T, H_S = '#e2553d', '#ff9b84', '#9c2a1a'
Y_F, Y_T, Y_S = '#ffd84d', '#ffe98f', '#c9891a'
DB = (16, -13)
TY0, TY1 = -40, -20          # بالا و پایین رویهٔ میز (جلو)
BX = 56
HB = (-26, TY0 - 4)          # پای دستهٔ چکش


def bar(a, b, w0, w1=None):
    w1 = w1 or w0
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    return [(a[0] + nx * w0 / 2, a[1] + ny * w0 / 2), (b[0] + nx * w1 / 2, b[1] + ny * w1 / 2), (b[0] - nx * w1 / 2, b[1] - ny * w1 / 2), (a[0] - nx * w0 / 2, a[1] - ny * w0 / 2)]


def build():
    p = Pen('tool_room', 'city'); pad(p, line=((60, 24), (76, 20)), tri=((-74, 4), (-66, 20)), dot=(72, -10)); p.xf = (1.0, -4, 4)
    p.tipshadow(2, 10, 62); p.foot_tip(2, 10, 44)
    for x in (-BX + 4, BX - 20):
        box3(p, x, TY1, x + 16, 12, (8, -5), W_F, W_T, W_S, sw=PART)
        rect(p, x + 3.5, TY1 + 6, x + 6.5, 4, W_T, .7)
    # پیشانی/کشو
    p.shape([(-BX + 20, TY1), (BX - 20, TY1), (BX - 20, TY1 + 16), (-BX + 20, TY1 + 16)], A_F, PART, j=.05, step=6, clip=False)
    p.shape([(-6, TY1 + 4), (6, TY1 + 4), (6, TY1 + 10), (-6, TY1 + 10)], Y_F, INNER, j=.05, step=99, clip=False)
    # رویهٔ ضخیم
    box3(p, -BX, TY0, BX, TY1, DB, W_F, W_T, W_S, sw=PART)
    rect(p, -BX + 6, TY0 + 4, BX - 30, TY0 + 7.5, '#fff3c4', .8)
    # گیره (راست)
    vx0, vx1 = 22, 50
    p.tipshadow(vx0 + 18, TY0 - 4, 20)
    box3(p, vx0 - 2, TY0 - 8, vx1 + 4, TY0 - 1, (8, -6), S_F, S_T, S_S, sw=PART)
    box3(p, vx0 + 2, TY0 - 42, vx1, TY0 - 8, (9, -7), S_F, S_T, S_S, sw=PART)
    box3(p, vx0 - 10, TY0 - 34, vx0 + 2, TY0 - 12, (7, -5), S_S, S_F, '#5e6c8c', sw=PART)
    p.shape(bar((vx1 - 2, TY0 - 22), (vx1 + 14, TY0 - 36), 9), Y_F, PART, j=.05, step=6, clip=False)
    p.shape(ell(vx1 + 17, TY0 - 39, 7.5, 7.5, 0, 360, 14), Y_F, PART, j=.05, step=99, clip=False)
    # چکش (لایهٔ متحرک)
    with layer(p, 'hammer'):
        p.tipshadow(HB[0] + 4, TY0 + 1, 10)
        extrude(p, [(HB[0] - 7, HB[1]), (HB[0] + 7, HB[1]), (HB[0] + 7, -108), (HB[0] - 7, -108)], (6, -4), H_F, H_T, H_S, sw=PART)
        rect(p, HB[0] - 3, HB[1] - 6, HB[0] - 0.5, -100, '#ffffff', .6)
        head = [(HB[0] - 30, -124), (HB[0] + 30, -124), (HB[0] + 30, -98), (HB[0] - 30, -98)]
        extrude(p, head, (10, -7), S_F, S_T, S_S, sw=OUT, sw_in=PART)
        for xa, xb in ((-30, -20), (20, 30)):
            rect(p, HB[0] + xa, -122, HB[0] + xb, -100, S_S, .9)
        rect(p, HB[0] - 14, -119, HB[0] + 14, -115, '#ffffff', .85)
    return p


if __name__ == '__main__':
    p = build(); hm = p.X(HB)
    r = finish(p, 'tool_room', None, motion={'hammer': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_tool_room_hammer': dict(pivot=[round(v, 1) for v in hm], rotate_deg='0 → +8 → -8 → 0 (حالت ایستا 0)', dur_s=1.2, once=True,
        note='چکش یک‌بار کمی کج می‌شود و برمی‌گردد؛ بقیه ثابت؛ بدون حلقهٔ بیکار.'), 'reduced_motion': 'چکش ایستا'}
    (OUTD / 'tool_room.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
