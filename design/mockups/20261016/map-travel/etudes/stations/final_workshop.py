#!/usr/bin/env python3
"""ایستگاه M12 «مخفی‌گاه هیولای مخترع»: قهرمان = لانهٔ تپه‌ای پشمالوی بنفش با درِ گردِ چوبی نیمه‌باز و درون گرم،
لامپ بالای در، دودکش با دود، و یک چرخ‌دندهٔ کوچک (۸ دنده، رنگ تخت بدون خط دور) به‌عنوان تابلو. هیولا دیده نمی‌شود.
لایهٔ متحرک: node_final_workshop_gear (چرخش آهسته هنگام رسیدن). id نود: node_final_workshop (ثابت)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit3/final_workshop'

FUR = '#a477e8'; FUR_D = '#7c52c9'; FUR_L = '#c9a8f5'
HOLE = '#2b1d5e'; GLOW = '#ffd84d'; WOOD = '#c98f4a'; WOOD_D = '#8a5a26'
BRICK = '#e0674c'; SMOKE = '#f3eefc'; GEAR = '#ffd84d'; GEAR_D = '#e0a020'
CX, BASE, HW, HH = -26, 14, 33, 52       # مرکز تپه، خط کف، نیم‌پهنا، ارتفاع
DX, DY = -26, -1                         # مرکز در
GX, GY = -44, -20                        # مرکز چرخ‌دنده


def hill():
    pts = []
    n = 72
    for i in range(n + 1):                       # گنبد پشمالو: برآمدگی‌های گرد با شکاف تیز (پشم)
        t = math.pi * i / n
        r = 1 + .075 * abs(math.sin(t * 5.5)) - .03
        pts.append((CX + HW * math.cos(t) * r, BASE - HH * math.sin(t) * r))
    pts += [(CX - HW + 1, BASE + 3), (CX - 14, BASE + 5), (CX + 10, BASE + 5), (CX + HW - 1, BASE + 3)]
    return pts[::-1]


def gear_poly(cx, cy, ri, ro, n=8, w=.36):
    pt = 2 * math.pi / n; out = []
    for k in range(n):
        a = k * pt + math.radians(22.5)
        for da, r in ((-.5 * pt, ri), (-w * pt / 2 * 1.0 - .02, ri), (-w * pt / 2 * .8, ro), (w * pt / 2 * .8, ro), (w * pt / 2 + .02, ri)):
            out.append((cx + r * math.cos(a + da), cy + r * math.sin(a + da)))
    return out


def build(out=OUTD):
    p = Pen('final_workshop', 'land'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.tipshadow(CX + 2, BASE + 6, 38)
    p.shape(hill(), FUR, OUT, j=.5, step=99)
    # دودکش (راست بالا) و دود
    p.shape([(-1, -30), (13, -30), (12, -52), (0, -52)], BRICK, PART, j=.3, step=99)
    p.fill([(-3, -57), (15, -57), (15, -52), (-3, -52)], FUR_D)
    p.fill(ell(8, -66, 6, 5, 0, 360, 16), SMOKE); p.fill(ell(16, -77, 7, 6, 0, 360, 16), SMOKE); p.fill(ell(10, -90, 8.5, 6.5, 0, 360, 16), SMOKE)
    p.shape(hill(), FUR, OUT, j=.4, step=99)
    # در: دهانهٔ تیره + درون گرم + لنگهٔ چوبی نیمه‌باز
    p.shape(ell(DX, DY, 15, 14, 0, 360, 28), HOLE, PART, j=.2, step=99)
    p.fill(ell(DX - 3, DY + 3, 9, 8, 0, 360, 20), GLOW)
    p.shape(ell(DX + 13, DY, 6, 14, 0, 360, 20), WOOD, PART, j=.2, step=99)
    # لامپ: هدلایت روی تپه (مثل هیولا)
    p.shape(ell(CX, BASE - HH - 4, 7.5, 7.5, 0, 360, 20), GLOW, PART, j=.2, step=99)
    for a in (-70, -90, -110):
        t = math.radians(a)
        p.ln((CX + 13 * math.cos(t), BASE - HH - 4 + 13 * math.sin(t)), (CX + 19 * math.cos(t), BASE - HH - 4 + 19 * math.sin(t)), INNER, GLOW, j=.05)
    # تابلو: چرخ‌دندهٔ کوچک (لایهٔ متحرک)
    with layer(p, 'gear'):
        p.fill(gear_poly(GX, GY, 10, 15), GEAR)
        p.fill(ell(GX, GY, 4.2, 4.2, 0, 360, 16), FUR_D)
            return p


STAND = None
if __name__ == '__main__':
    p = build()
    gm = p.X((GX, GY))
    r = finish(p, 'final_workshop', STAND, motion={'gear': dict(rotate=gm)}, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = {'node_final_workshop_gear': dict(center=[round(v, 1) for v in gm], dir='cw', note='چرخ‌دندهٔ تابلو؛ ۸ دنده، چرخش آهسته. لامپ ثابت.')}
    (OUTD / 'final_workshop.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
