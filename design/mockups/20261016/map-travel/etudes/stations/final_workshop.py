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
BRICK = '#e0674c'; BRICK_D = '#b8432f'; SMOKE = '#f3eefc'; GEAR = '#ffd84d'; GEAR_D = '#e0a020'
CX, BASE, HW, HH = -24, 16, 32, 60       # مرکز تپه، خط کف، نیم‌پهنا، ارتفاع
DX, DY = -24, 2                         # مرکز در
XF = (1.0, 0.0, -9.0)
GX, GY = -33, -27                        # مرکز چرخ‌دنده


def hill():
    pts = []
    n = 72
    for i in range(n + 1):                       # گنبد پشمالو: برآمدگی‌های گرد با شکاف تیز (پشم)
        t = math.pi * i / n
        r = 1 + .075 * abs(math.sin(t * 4.5)) - .04
        c, sn = math.cos(t), math.sin(t); e = .78
        pts.append((CX + HW * math.copysign(abs(c) ** e, c) * r, BASE - HH * abs(sn) ** e * r))
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
    p.xf = XF
    p.tipshadow(CX + 2, BASE + 6, 38)
    # دودکش (راست بالا) و دود
    p.shape([(-6, -20), (10, -20), (10, -46), (-6, -46)], BRICK, PART, j=.3, step=99)
    p.shape([(-9, -52), (13, -52), (13, -44), (-9, -44)], BRICK_D, PART, j=.3, step=99)
    p.fill(ell(3, -63, 6, 5, 0, 360, 16), SMOKE); p.fill(ell(9, -74, 7, 6, 0, 360, 16), SMOKE); p.fill(ell(3, -87, 8.5, 6.5, 0, 360, 16), SMOKE)
    p.shape(hill(), FUR, OUT, j=.4, step=99)
    for (x, y) in ((-6, -10), (-4, 8), (-48, 4)):      # نشانهٔ پشم: v کوچک تخت
        p.ln((x - 4, y - 4), (x, y), INNER, FUR_D, j=.05); p.ln((x, y), (x + 4, y - 4), INNER, FUR_D, j=.05)
    # در: دهانهٔ تیره + درون گرم + لنگهٔ چوبی نیمه‌باز
    p.shape(ell(DX, DY, 15, 15, 0, 360, 28), HOLE, PART, j=.2, step=99)
    p.fill(ell(DX - 5, DY + 2, 8, 9, 0, 360, 20), GLOW)
    p.shape(ell(DX + 9, DY, 8, 15, 0, 360, 20), WOOD, PART, j=.2, step=99)
    p.ln((DX + 9, DY - 5), (DX + 9, DY + 5), INNER, WOOD_D, j=.05)
    # لامپ: هدلایت روی تپه (مثل هیولا)
    p.shape(ell(CX, BASE - HH - 2, 6.5, 6.5, 0, 360, 20), GLOW, PART, j=.2, step=99)
    # تابلو: چرخ‌دندهٔ کوچک (لایهٔ متحرک)
    with layer(p, 'gear'):
        p.fill(gear_poly(GX, GY, 8.5, 12.5), GEAR)
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
