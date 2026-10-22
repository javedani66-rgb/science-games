#!/usr/bin/env python3
"""B02 «انبار مصالح» (سکوی city) — دور ۶ (R6): دو پشتهٔ برابر، هرکدام ۳ گونی روی پالت چوبی؛ پشتهٔ چپ کرم، راست خاکستری.
طرح (واحد symbol، xf=(1.22،0،-2)، مرکز پشته‌ها x=±27، کف y=14):
 ۱ پالت چوبی ¾ (۵۰ پهن): عرشه y 0..8 با وجه راست تیره (عمق ۶) + سه پایه (y 8..14)؛ چوب #c98a4b/#e6b27a/#8f5a2c.
 ۲ دو گونی خوابیده (۴۴×۲۴ و ۴۰×۲۴، پایین‌تر آفست ۲) با دُم گره‌دار سمت چپ/راست متناوب، رشتهٔ قرمز، چین‌های کوتاه.
 ۳ گونی ایستادهٔ بالایی (۳۲×۲۵) با گردن چین‌دار و گره قرمز در بالا. هر گونی سه پله: پایه/روشن چپ/تیره راست (داخل جزء).
 رنگ: کرم #f6e6b8/#fffaea/#d2b06a، خاکستری #d0d4de/#f4f6fb/#8b92a8، سکو آبی-خاکستری ۲۱۳°.
حرکت: node_materials_store_bag = گونی بالایی پشتهٔ راست؛ هنگام رسیدن از ۱۴ واحد بالاتر می‌افتد و می‌نشیند؛ ایستا = روی پشته؛ بدون بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from station_kit import *
from g6h import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/materials_store'
CREAM = ('#fbecc0', '#ffffff', '#d9b76e')
YEL = ('#f5cf6a', '#fff0b0', '#c48a2a')
W_B, W_L, W_D = '#a9653a', '#cf8f5c', '#6d3d22'
RED, RED_D = '#e0402e', '#a82a1c'
XF = (1.45, 0, -2)
PX = (-31, 31)
DECK0, DECK1, GROUND, DROP = 0, 8, 15, 11


def rrect(x0, y0, x1, y1, r, n=5):
    pts = []
    for (ox, oy, a0) in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n); pts.append((ox + r * math.cos(a), oy + r * math.sin(a)))
    return pts


def pallet(p, c):
    x0, x1, D = c - 28, c + 28, 7
    for dx in (-18, 18):
        p.shape(R(c + dx - 6, DECK1 - 1, c + dx + 6, GROUND), W_D, PART, j=.05, step=99, clip=False)
    sil = [(x0, DECK0), (x1, DECK0), (x1 + D, DECK0 - 4), (x1 + D, DECK1 - 4), (x1, DECK1), (x0, DECK1)]
    p.shape(sil, W_B, PART, j=.05, step=99)
    poly(p, [(x1, DECK0), (x1 + D, DECK0 - 4), (x1 + D, DECK1 - 4), (x1, DECK1)], W_D)
    poly(p, R(x0 + 3, DECK0 + 2.4, x1 - 3, DECK0 + 5.2), W_L)
    p.ln((x1, DECK0), (x1, DECK1), INNER, NAVY, j=.05)


def pillow(cx, yc, w, h, n=28):
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n; c, s = math.cos(t), math.sin(t)
        px = c * (1 - .16 * abs(c) ** 3) * w / 2          # chin pinched ends
        py = math.copysign(abs(s) ** .62, s) * h / 2
        pts.append((cx + px, yc + py))
    return pts


def sack(p, cx, yb, w, h, col, tail=1):
    """گونی خوابیده با دو سر جمع‌شده؛ گرهٔ قرمز کنار tail (+1 راست، -1 چپ)."""
    B, L, D = col
    x0, x1, y0, yc = cx - w / 2, cx + w / 2, yb - h, yb - h / 2
    t = tail
    ear = [(cx + t * (w / 2 - 4), yc - 6), (cx + t * (w / 2 + 8), yc - 10), (cx + t * (w / 2 + 9), yc + 8), (cx + t * (w / 2 - 4), yc + 6)]
    p.shape(ear, B, PART, j=.05, step=99, clip=False)
    poly(p, R(min(cx + t * (w / 2 - 1), cx + t * (w / 2 + 4)), yc - 6.5, max(cx + t * (w / 2 - 1), cx + t * (w / 2 + 4)), yc + 6.5), RED)
    p.shape(pillow(cx, yc, w, h), B, PART, j=.05, step=99)
    poly(p, R(x0 + 12, y0 + 4.5, x1 - 14, y0 + 8.5), L)
    poly(p, R(x0 + 11, yb - 8, x1 - 11, yb - 4), D, .9)
    p.ln((cx - t * 4, y0 + 12), (cx + t * 8, yb - 12), INNER, D, j=.05)


def build():
    p = Pen('materials_store', 'city'); pad(p, line=((-80, 12), (-66, 20)), tri=((72, -22), (80, 8)), dot=(-74, -14)); p.xf = XF
    for cx in PX:
        p.tipshadow(cx + 3, GROUND + 1.5, 34); p.foot_tip(cx, GROUND, 22)
    for cx, col in zip(PX, (CREAM, YEL)):
        pallet(p, cx)
        sack(p, cx - 1, DECK0, 52, 30, col, -1)
    sack(p, PX[0] + 3, DECK0 - 29, 50, 30, CREAM, 1)
    with layer(p, 'bag'):
        sack(p, PX[1] + 3, DECK0 - 29, 50, 30, YEL, 1)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    offs = [p.V((0, -DROP)), p.V((0, -DROP / 2)), (0, 0)]
    r = finish(p, 'materials_store', STAND, motion={'bag': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_materials_store_bag': dict(
        layer='گونی بالایی پشتهٔ راست', dx=0, dy_from=-DROP, dy_to=0, dur_s=1.2,
        note='هنگام رسیدن: گونی از ۱۴ واحد بالاتر پایین می‌افتد و روی پشته می‌نشیند؛ حالت ایستا = روی پشته؛ بدون حلقهٔ بیکار.'),
        'reduced_motion': 'گونی روی پشته (ایستا)'}
    (OUTD / 'materials_store.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
