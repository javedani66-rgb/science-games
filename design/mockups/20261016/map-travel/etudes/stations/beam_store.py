#!/usr/bin/env python3
"""ایستگاه M05 «انبار تیرآهن» (سکوی شهر، city #5b7390). id=beam_store؛ لایهٔ متحرک node_beam_store_prop. بازطراحی چهارم (دستور مدیر هنری R5).
سه تیرآهن I درشت روی هم (دو تا پایین کنار هم، یکی بالا روی آن‌ها)؛ مقطع I (H خوان) رو به بیننده؛ تیرها به پشت-چپ می‌روند (D=(-24,-12)).
اجزا (واحد symbol؛ زمین G=10):
 ۱) تیر پایین راست و ۲) تیر پایین چپ: مقطع ۴۲×۴۰، بال ۱۲٫۵، جان ۱۵؛ رخ جلو #e2ebf5، رویه #ffffff، پهلوی چپ #9db0c8، بدنه #b7c6da؛ خط دور PART، رخ جلو INNER.
 ۳) تیر بالا (لایهٔ prop): همان تیر، روی بال بالایی دو تیر زیرین؛ حرکت: از ۸ واحد بالاتر آرام می‌نشیند (یک‌بار)؛ حالت ایستا = نشسته.
 ۴) سایهٔ تماس زیر تیرهای پایین.
فلز خاکستری-آبی روشن روی سکوی تیره (کنتراست ارزشی)؛ بنفش و گوه حذف شد."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
from shapely.geometry import Polygon
from shapely.ops import unary_union
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/beam_store'

FRONT, TOPF, SIDEF, BODY, DEEP = '#e2ebf5', '#ffffff', '#9db0c8', '#b7c6da', '#7f93ae'
G = 10
W, H, TF, TW = 42, 40, 12.5, 15
D = (-24, -12)
OX = 12                                   # جابه‌جایی کل برای وسط‌چین کردن
DROP = 8
LX = (-21, 21)                            # مرکز دو تیر پایین


def I0(cx, base):
    """مقطع I با مرکز افقی cx و کف base (y منفی = بالا)."""
    x0, x1 = cx - W / 2, cx + W / 2; w0, w1 = cx - TW / 2, cx + TW / 2; t, b = base - H, base
    return [(x0, t), (x1, t), (x1, t + TF), (w1, t + TF), (w1, b - TF), (x1, b - TF), (x1, b), (x0, b), (x0, b - TF), (w0, b - TF), (w0, t + TF), (x0, t + TF)]


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def shift(pts, dx=0, dy=0): return [(x + dx + OX, y + dy) for x, y in pts]


def beam(p, cx, base, dy=0):
    f = I0(cx, base)
    n = len(f)
    pieces = [Polygon(f), Polygon([(x + D[0], y + D[1]) for x, y in f])]
    for i in range(n):
        a, b = f[i], f[(i + 1) % n]
        q = Polygon([a, b, (b[0] + D[0], b[1] + D[1]), (a[0] + D[0], a[1] + D[1])])
        if q.area > 0: pieces.append(q)
    sil = unary_union([q.buffer(0) for q in pieces]).buffer(0)
    ext = list(sil.exterior.coords)[:-1]
    p.shape(shift(ext, 0, dy), BODY, PART, j=0, step=6, clip=False)
    area = sum(f[i][0] * f[(i + 1) % n][1] - f[(i + 1) % n][0] * f[i][1] for i in range(n)) / 2
    for i in range(n):
        a, b = f[i], f[(i + 1) % n]
        ex, ey = b[0] - a[0], b[1] - a[1]
        nx, ny = (ey, -ex) if area > 0 else (-ey, ex)
        L = math.hypot(nx, ny); nx, ny = nx / L, ny / L
        vis = nx * D[0] + ny * D[1]
        if vis <= 0.5: continue
        col = TOPF if ny < -.7 else (SIDEF if nx < -.7 else (DEEP if ny > .7 else BODY))
        poly(p, shift([a, b, (b[0] + D[0], b[1] + D[1]), (a[0] + D[0], a[1] + D[1])], 0, dy), col)
    p.shape(shift(f, 0, dy), FRONT, INNER, j=0, step=6, clip=False)
    p.stroke(shift(ext, 0, dy), PART, j=0, step=6)


def build(out=OUTD):
    p = Pen('beam_store', 'city'); pad(p, line=((-52, 40), (-36, 43)), tri=((72, -22), (-74, 14)), dot=(78, 6))
    p.tipshadow(OX - 2, G + 1, 56); p.foot_tip(OX - 2, G, 44)
    beam(p, LX[1], G)
    beam(p, LX[0], G)
    with layer(p, 'prop'):
        beam(p, 0, G - H)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'beam_store', STAND, motion={'prop': dict(offsets=[(0, -DROP), (0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_beam_store_prop': dict(translate_from=[0, -DROP], translate_to=[0, 0], dur_s=1.2, repeat=1, easing='ease-in',
                         note='تیر بالایی از %d واحد (≈%dpx) بالاتر آرام می‌نشیند و می‌ماند؛ دو تیر پایین ثابت؛ حالت ایستا = نشسته؛ بدون حلقهٔ بیکار.' % (DROP, round(DROP * K))),
                         'reduced_motion': 'تیر بالا در جای نشسته'}
    (OUTD / 'beam_store.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
