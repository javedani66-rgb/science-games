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
CREAM = ('#f6e6b8', '#fffaea', '#d2b06a')
GREY = ('#d9dbe0', '#f7f8fa', '#989daa')
W_B, W_L, W_D = '#c98a4b', '#e6b27a', '#8f5a2c'
RED, RED_D = '#e0402e', '#a82a1c'
XF = (1.3, 0, -3)
PX = (-25, 25)
DECK0, DECK1, GROUND, DROP = 0, 8, 15, 11


def rrect(x0, y0, x1, y1, r, n=5):
    pts = []
    for (ox, oy, a0) in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n); pts.append((ox + r * math.cos(a), oy + r * math.sin(a)))
    return pts


def pallet(p, c):
    x0, x1, D = c - 23, c + 23, 6
    for dx in (-15, 15):
        p.shape(R(c + dx - 5, DECK1 - 1, c + dx + 5, GROUND), W_D, PART, j=.05, step=99, clip=False)
    sil = [(x0, DECK0), (x1, DECK0), (x1 + D, DECK0 - 4), (x1 + D, DECK1 - 4), (x1, DECK1), (x0, DECK1)]
    p.shape(sil, W_B, PART, j=.05, step=99)
    poly(p, [(x1, DECK0), (x1 + D, DECK0 - 4), (x1 + D, DECK1 - 4), (x1, DECK1)], W_D)
    poly(p, R(x0 + 3, DECK0 + 2.2, x1 - 3, DECK0 + 4.6), W_L)
    p.ln((x1, DECK0), (x1, DECK1), INNER, NAVY, j=.05)


def sack(p, cx, yb, w, h, col, tail=0):
    """گونی خوابیده؛ tail=-1 دُم چپ، +1 دُم راست."""
    B, L, D = col
    x0, x1, y0 = cx - w / 2, cx + w / 2, yb - h
    if tail:
        t = tail; xe = cx + t * (w / 2 + 7)
        ear = [(cx + t * (w / 2 - 5), yb - h * .68), (xe, yb - h * .78), (xe + t * 1, yb - h * .22), (cx + t * (w / 2 - 5), yb - h * .32)]
        p.shape(ear, B, PART, j=.05, step=99, clip=False)
        poly(p, R(min(cx + t * (w / 2 - 1), cx + t * (w / 2 + 3.5)), yb - h * .66, max(cx + t * (w / 2 - 1), cx + t * (w / 2 + 3.5)), yb - h * .34), RED)
    body = rrect(x0, y0, x1, yb, 9)
    p.shape(body, B, PART, j=.05, step=99)
    poly(p, R(x1 - 8, y0 + 5, x1 - 2.5, yb - 5), D, .9)
    poly(p, R(x0 + 3, y0 + 5, x0 + 6.5, yb - 7), L)
    p.ln((cx - 7, yb - h * .55), (cx + 3, yb - h * .47), INNER, D, j=.05)


def top_sack(p, cx, yb, col, w=32, h=25):
    B, L, D = col
    x0, x1, y0 = cx - w / 2, cx + w / 2, yb - h
    neck = [(cx - 6, y0 + 3), (cx + 6, y0 + 3), (cx + 14, y0 - 6), (cx + 9, y0 - 9), (cx + 4, y0 - 15), (cx, y0 - 10), (cx - 4, y0 - 15), (cx - 9, y0 - 9), (cx - 14, y0 - 6)]
    p.shape(neck, B, PART, j=.05, step=99, clip=False)
    poly(p, R(cx - 7.5, y0 - 3.5, cx + 7.5, y0 + 0.5), RED)
    body = rrect(x0, y0, x1, yb, 10)
    p.shape(body, B, PART, j=.05, step=99)
    poly(p, R(x1 - 9, y0 + 7, x1 - 3, yb - 5), D, .9)
    poly(p, R(x0 + 4, y0 + 7, x0 + 8, yb - 8), L)
    p.ln((cx - 6, yb - h * .5), (cx + 4, yb - h * .42), INNER, D, j=.05)


def build():
    p = Pen('materials_store', 'city'); pad(p, line=((-80, 12), (-66, 20)), tri=((72, -22), (80, 8)), dot=(-74, -14)); p.xf = XF
    for cx in PX:
        p.tipshadow(cx + 3, GROUND + 1.5, 32); p.foot_tip(cx, GROUND, 20)
    for cx, col in zip(PX, (CREAM, GREY)):
        pallet(p, cx)
        sack(p, cx - 1, DECK0, 38, 22, col, -1)
        sack(p, cx + 2, DECK0 - 21, 36, 22, col, 1)
    top_sack(p, PX[0], DECK0 - 42, CREAM, 30, 23)
    with layer(p, 'bag'):
        top_sack(p, PX[1], DECK0 - 42, GREY, 30, 23)
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
