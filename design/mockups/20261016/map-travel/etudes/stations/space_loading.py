#!/usr/bin/env python3
"""W01 «ایستگاه بارگیری فضایی» (سکوی space، رنگ‌مایهٔ ۲۵۶°) — دور ۶ بازطراحی (هم‌سطح پیچ‌کاری).
قهرمان: کانتینر فلزی بزرگ ¾ با در باز (آبی فولادی ۲۰۵°، سه پله) + جرثقیل کوچک زرد با بازو و قلاب که جعبهٔ نارنجی را بالا می‌برد. ≈۸۰٪ عرض سکو، ۵ جزء درشت.
طرح قطعه‌به‌قطعه (واحد symbol، کف y=18):
 ۱) کانتینر: جلو ۷۶×۵۲ (آبی #3a8fd8)، رویهٔ روشن #8cc8f5، وجه راست تیره #245f9c، در باز = چارچوب تیره #142a5c با کف روشن؛ دو دنده؛ نوار هشدار زرد-سیاه پایین.
 ۲) جرثقیل: پایه + دکل ۱۴ + بازوی افقی ۱۰۰×۱۲ (زرد #ffd23f، روشن #fff0a8، تیره #d9961c) + چراغ قرمز روی دکل.
 ۳) لایهٔ متحرک node_space_loading_crate: کابل (INNER) + قلاب خاکستری + جعبهٔ نارنجی #ff8a2b (۲۶×۲۶).
حالت ایستا = پایان = جعبه بالا. بدون ترازو/عدد/متن/پیکان."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from station_kit import *
from r6_helpers import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/space_loading'
CB = ('#3a8fd8', '#8cc8f5', '#245f9c')
YB = ('#ffd23f', '#fff0a8', '#d9961c')
OR = ('#ff8a2b', '#ffc27a', '#c85f12')
GY = 18
RANGE = 14


def container(p):
    x0, y0, w, h, D = -78, -34, 72, 52, (24, -15)
    p.tipshadow(x0 + w / 2 + 8, GY + 2, 54); p.foot_tip(x0 + w / 2, GY, 30)
    box(p, x0, y0, w, h, D, CB, sw=OUT)
    for rx in (x0 + 8, x0 + w - 8):                                  # دنده‌های روشن
        p.fill([(rx - 1.5, y0 + 5), (rx + 1.5, y0 + 5), (rx + 1.5, y0 + h - 14), (rx - 1.5, y0 + h - 14)], '#6db0ea')
    dx0, dx1, dy0, dy1 = x0 + 16, x0 + w - 16, y0 + 8, y0 + h - 13   # در باز
    p.shape([(dx0, dy0), (dx1, dy0), (dx1, dy1), (dx0, dy1)], '#142a5c', PART, j=.05, step=6, clip=False)
    p.fill([(dx0 + 4, dy1 - 7), (dx1 - 4, dy1 - 7), (dx1 - 4, dy1 - 2.5), (dx0 + 4, dy1 - 2.5)], '#9db4d6')
    p.fill([(dx0 + 4, dy0 + 4), (dx0 + 9, dy0 + 4), (dx0 + 9, dy1 - 8), (dx0 + 4, dy1 - 8)], '#27428a')
    sy0, sy1 = y0 + h - 10, y0 + h - 1                                # نوار هشدار زرد-سیاه
    p.fill([(x0 + 3, sy0), (x0 + w - 3, sy0), (x0 + w - 3, sy1), (x0 + 3, sy1)], '#ffd23f')
    for i in range(7):
        a = x0 + 6 + i * 9.8
        p.fill([(a, sy0), (a + 5, sy0), (a + 1, sy1), (a - 4, sy1)], '#241a5e')
    p.stroke([(x0, sy0), (x0 + w, sy0)], INNER, j=0, step=99)


def crane(p):
    bx, by = 28, GY - 20
    p.foot_tip(bx + 14, GY, 12)
    box(p, bx, by, 30, 20, (13, -9), YB, sw=PART)                            # پایه
    for i in range(3):
        a = bx + 5 + i * 8.5
        p.fill([(a, by + 12), (a + 4, by + 12), (a + 1, by + 19), (a - 3, by + 19)], '#241a5e')
    box(p, bx + 8, -100, 14, by + 100, (8, -5), YB, sw=PART)                  # دکل
    p.tipshadow(bx + 20, GY + 2, 26)
    box(p, -26, -112, 72, 14, (9, -6), YB, sw=PART)                          # بازو
    cyl(p, bx + 18, -116, 7.5, 11, ('#e0443a', '#ff9a86', '#a82a24', '#ffb4a0'), sw=PART)   # چراغ


def load(p):
    cx = -4
    with layer(p, 'crate'):
        p.ln((cx, -107), (cx, -88), INNER, NAVY, j=.05)
        p.shape(ell(cx, -85, 6.5, 6.5, 0, 360, 16), '#aab8cf', PART, j=.1, step=99, clip=False)
        box(p, cx - 13, -80, 26, 26, (10, -7), OR, sw=PART)
        p.fill([(cx - 13, -68), (cx + 13, -68), (cx + 13, -63), (cx - 13, -63)], '#a8470a', .85)


def build():
    p = Pen('space_loading', 'space'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.0, -2, 0)
    container(p); load(p); crane(p)
    return p


if __name__ == '__main__':
    p = build()
    offs = [(0, 0), p.V((0, RANGE)), (0, 0)]
    r = finish(p, 'space_loading', None, motion={'crate': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_space_loading_crate': dict(
        kind='کابل + قلاب + جعبهٔ نارنجی؛ translateY؛ از پایین‌تر (+%s واحد) به بالا (۰)؛ حالت ایستا = بالا (پایان)' % RANGE,
        keyframes_symbol_units=[[0, RANGE], [0, 0]], duration_s=1.8, easing='ease-out', loop=False,
        trigger='رسیدن کودک (یک‌بار)', note='کابل در همان لایه می‌ماند و بالای آن پشت بازو پنهان است؛ جعبه از سکو بیرون نمی‌زند', reduced_motion='بالا')}
    (OUTD / 'space_loading.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')}, ensure_ascii=False))
