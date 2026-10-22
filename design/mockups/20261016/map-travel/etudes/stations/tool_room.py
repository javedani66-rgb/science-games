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
DB = (20, -17)
TY0, TY1 = -34, -18          # بالا و پایین رویهٔ میز (جلو)
BL, BR = -50, 44             # چپ و راست میز
HB = (-22, TY0 - 8)          # پای دستهٔ چکش (روی رویه)
LEAN = -8                   # کج‌شدن ایستای چکش (درجه)
Y_D = '#e0a21c'


def rp(pts, ang=LEAN, c=HB):
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


def bar(a, b, w0, w1=None):
    w1 = w1 or w0
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    return [(a[0] + nx * w0 / 2, a[1] + ny * w0 / 2), (b[0] + nx * w1 / 2, b[1] + ny * w1 / 2), (b[0] - nx * w1 / 2, b[1] - ny * w1 / 2), (a[0] - nx * w0 / 2, a[1] - ny * w0 / 2)]


def build():
    p = Pen('tool_room', 'city'); pad(p, line=((60, 24), (76, 20)), tri=((-74, 4), (-66, 20)), dot=(72, -10)); p.xf = (1.0, 4, 6)
    p.tipshadow(0, 12, 62); p.foot_tip(0, 12, 44)
    # پایه‌های ضخیم + قفسهٔ پایین (میز کار، نه میز ساده)
    for x in (BL + 2, BR - 18):
        box3(p, x, TY1, x + 16, 14, (7, -5), W_F, W_T, W_S, sw=PART)
        rect(p, x + 3.5, TY1 + 6, x + 6.5, 4, W_T, .7)
    p.shape([(BL + 18, TY1), (BR - 18, TY1), (BR - 18, TY1 + 12), (BL + 18, TY1 + 12)], A_F, PART, j=.05, step=6, clip=False)
    p.shape([(-6, TY1 + 3), (6, TY1 + 3), (6, TY1 + 9), (-6, TY1 + 9)], Y_F, INNER, j=.05, step=99, clip=False)
    # رویهٔ ضخیم
    box3(p, BL, TY0, BR, TY1, DB, W_F, W_T, W_S, sw=PART)
    rect(p, BL + 6, TY0 + 4, BR - 36, TY0 + 7.5, '#fff3c4', .8)
    # انبردست (زرد) روی رویهٔ میز، افتاده
    cx, cy = 6, TY0 - 9
    for sg in (-1, 1):
        p.shape(bar((cx - 24, cy + sg * 6), (cx + 2, cy + sg * 1.5), 10, 8), Y_F, PART, j=.05, step=6, clip=False)
    p.shape([(cx + 2, cy - 7), (cx + 22, cy - 3), (cx + 26, cy), (cx + 22, cy + 3), (cx + 2, cy + 7)], S_F, PART, j=.05, step=6, clip=False)
    circ(p, cx + 3, cy, 3.2, Y_D)
    # گیره (راست)
    vx0, vx1 = 32, 50
    box3(p, vx0, TY0 - 26, vx1, TY0 - 4, (9, -7), S_F, S_T, S_S, sw=PART)
    box3(p, vx0 - 10, TY0 - 22, vx0 + 2, TY0 - 8, (7, -5), S_S, S_F, '#5e6c8c', sw=PART)
    p.shape(bar((vx1 - 2, TY0 - 14), (vx1 + 12, TY0 - 26), 8), Y_F, PART, j=.05, step=6, clip=False)
    p.shape(ell(vx1 + 14, TY0 - 28, 7, 7, 0, 360, 14), Y_F, PART, j=.05, step=99, clip=False)
    # چکش چنگکی (لایهٔ متحرک)
    with layer(p, 'hammer'):
        p.tipshadow(HB[0] + 2, TY0 - 2, 10)
        X, Y = HB
        extrude(p, rp([(X - 8, Y), (X + 8, Y), (X + 8, Y - 62), (X - 8, Y - 62)]), (6, -4), H_F, H_T, H_S, sw=PART)
        poly(p, rp([(X - 8, Y - 22), (X + 8, Y - 22), (X + 8, Y - 2), (X - 8, Y - 2)]), Y_F)            # گریپ زرد
        poly(p, rp([(X - 4, Y - 58), (X - 1.5, Y - 58), (X - 1.5, Y - 26), (X - 4, Y - 26)]), '#ffffff', .6)
        hy = Y - 62
        head = rp([(X - 14, hy - 4), (X - 30, hy - 7), (X - 42, hy + 2), (X - 44, hy + 14), (X - 36, hy + 8), (X - 26, hy + 4), (X - 14, hy + 14),
                   (X + 24, hy + 14), (X + 24, hy - 4)])
        extrude(p, head, (9, -6), S_F, S_T, S_S, sw=OUT, sw_in=PART)
        poly(p, rp([(X + 14, hy - 2), (X + 24, hy - 2), (X + 24, hy + 12), (X + 14, hy + 12)]), S_S, .9)
        poly(p, rp([(X - 12, hy), (X + 10, hy), (X + 10, hy + 3.5), (X - 12, hy + 3.5)]), '#ffffff', .85)
    return p


if __name__ == '__main__':
    p = build(); hm = p.X(HB)
    r = finish(p, 'tool_room', None, motion={'hammer': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_tool_room_hammer': dict(pivot=[round(v, 1) for v in hm], rotate_deg='کج‌شدن ایستا -8 → 0 → -8 (حالت ایستا = -8؛ یک‌بار)', dur_s=1.2, once=True,
        note='چکش یک‌بار کمی کج می‌شود و برمی‌گردد؛ بقیه ثابت؛ بدون حلقهٔ بیکار.'), 'reduced_motion': 'چکش ایستا'}
    (OUTD / 'tool_room.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
