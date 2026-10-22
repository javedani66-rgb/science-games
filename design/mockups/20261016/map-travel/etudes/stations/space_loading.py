#!/usr/bin/env python3
"""ایستگاه W01 «ایستگاه بارگیری فضایی» (سکوی space، رنگ‌مایهٔ سکو ۲۵۶°) — دور ۵ (بازطراحی: کپسول بارگیری + رمپ + جعبه).
طرح قطعه‌به‌قطعه (واحد symbol؛ مختصات پایه، سپس xf مجموعه را وسط می‌آورد؛ کف 7):
 ۱) پایهٔ فولادی: تختهٔ پهن (۶۸×۹، آبی-خاکستری ۲۰۵°) زیر کپسول.
 ۲) کپسول: بیضی ایستاده کرم-سفید (rx32, ry38، مرکز (-22,-44)) با نور چپ و سایهٔ هلالی راست؛ OUT.
 ۳) دریچهٔ باز: دهانهٔ طاقی تیره (۲۴×۲۴) روی بدنه، پایین دریچه به رمپ می‌رسد؛ یک پنجرهٔ گرد آبی بالای دریچه.
 ۴) رمپ فلزی زرد: نوار شیب‌دار از کف دریچه تا زمین (کف x=32)؛ سه پلهٔ تخت نارنجی.
 ۵) جعبهٔ بار (قهوه‌ای، ۲۶×۲۸) انتهای رمپ؛ تختهٔ چوبی روشن و ضربدر تیره.
 ۶) چراغ: پایهٔ فولادی + گنبد خاموش (ثابت) بالای کپسول؛ ۷) لایهٔ node_space_loading_light: گنبد روشن قرمز-نارنجی.
رنگ‌مایه: کرم ≈۴۵°، زرد ≈۴۸°، قهوه‌ای ≈۳۰°، فولاد ≈۲۰۵°، چراغ ≈۱۰° — همه ≥۳۵° از ۲۵۶°. بدون ترازو/عدد/متن/پیکان."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/space_loading'

C_B, C_L, C_D = '#f7efd9', '#ffffff', '#d2c5a6'      # کپسول
Y_B, Y_L, Y_D = '#ffd23f', '#fff0a8', '#d9961c'      # رمپ
H_B, H_L, H_D = '#8fa6b8', '#c4d3df', '#667f94'      # فولاد
X_B, X_L, X_D = '#b9733a', '#e0a468', '#7a4520'      # جعبه
L_B, L_L, L_OFF = '#ef5a3a', '#ffb59c', '#8c2a1a'    # چراغ
HOLE = '#26365f'; GLASS = '#9fd0ff'

CX0, CY0, RX, RY = -20, -34, 36, 30
BASE = 7
XF = (1.0, -4.0, 0.0)


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def rect(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def arc(sx, sy, a0, a1, n=12): return ell(CX0, CY0, RX * sx, RY * sy, a0, a1, n)


def dome(r=9): return [(CX0 + r * math.cos(math.radians(a)), -88 + r * math.sin(math.radians(a))) for a in range(180, 361, 15)]


def build(out=OUTD):
    p = Pen('space_loading', 'space'); pad(p, line=((50, 30), (70, 27)), tri=((78, -6),), dot=(32, -34)); p.xf = XF
    p.tipshadow(2, BASE + 3, 52); p.foot_tip(CX0 - 14, BASE + 2, 14); p.foot_tip(50, BASE + 2, 10)
    # ۲) کپسول
    cap = arc(1, 1, 0, 360, 36)
    p.shape(cap, C_B, OUT, j=.1, step=8)
    outer = [(CX0 + RX * .94 * math.cos(math.radians(t)), CY0 + RY * .94 * math.sin(math.radians(t))) for t in range(-60, 61, 10)]
    inner = [(x - 15 + 4 * (1 - math.cos(math.radians(t))) , y) for (x, y), t in zip(outer[::-1], range(60, -61, -10))]
    poly(p, outer + inner, C_D)                                                                                  # سایهٔ هلالی راست
    poly(p, arc(.88, .88, 205, 250, 8) + arc(.76, .76, 250, 205, 8), C_L)                                       # نور چپ
    # کمربند فولادی دور کپسول
    hw = lambda y: RX * math.sqrt(1 - ((y - CY0) / RY) ** 2)
    poly(p, [(CX0 - hw(-51), -51), (CX0 + hw(-51), -51), (CX0 + hw(-45), -45), (CX0 - hw(-45), -45)], H_B)
    poly(p, [(CX0 - hw(-51), -51), (CX0 - 8, -51), (CX0 - 8, -48.5), (CX0 - hw(-48.5), -48.5)], H_L)
    p.stroke(cap, OUT, j=.1, step=8)
    sl = rect(CX0 - 30, -9, CX0 + 30, BASE)
    p.shape(sl, H_B, PART, j=.1, step=6, clip=False)
    poly(p, rect(CX0 - 25, -5, CX0 - 20, BASE - 4), H_L)
    poly(p, rect(CX0 + 18, -5, CX0 + 26, BASE - 3), H_D, .85)
    p.stroke(sl, PART, j=.1, step=6)
    # ۳) دریچهٔ باز و پنجرهٔ گرد
    hole = [(CX0 - 13, -12)] + ell(CX0, -25, 13, 13, 180, 360, 10) + [(CX0 + 13, -12)]
    p.shape(hole, HOLE, INNER, j=.06, step=6, clip=False)
    # ۴) رمپ فلزی زرد (از کف دریچه تا زمین)
    ramp = [(CX0 - 8, -24), (34, -10), (34, BASE), (CX0 - 8, -8)]
    p.shape(ramp, Y_B, PART, j=.08, step=6, clip=False)
    for x in (-4, 8, 20):
        y0 = -24 + (x - (CX0 - 8)) * 14 / 62
        poly(p, [(x - 2, y0 + 5), (x + 2, y0 + 5), (x + 2, y0 + 15), (x - 2, y0 + 15)], Y_D)
    poly(p, [(CX0 - 5, -21), (31, -8), (31, -4.5), (CX0 - 5, -17.5)], Y_L)
    p.stroke(ramp, PART, j=.08, step=6)
    # ۵) جعبهٔ بار
    box = rect(37, -22, 63, BASE)
    p.shape(box, X_B, PART, j=.08, step=6)
    poly(p, rect(41, -18, 44.5, BASE - 4), X_L)
    poly(p, rect(57, -18, 60, BASE - 3), X_D, .8)
    poly(p, [(40, -19), (44, -19), (60, 3), (56, 3)], X_D)                                                       # ضربدر
    poly(p, [(56, -19), (60, -19), (44, 3), (40, 3)], X_D)
    p.stroke(box, PART, j=.08, step=6)
    # ۶) آنتن و چراغ (خاموش) و ۷) لایهٔ متحرک: چراغ روشن
    p.ln((CX0, CY0 - RY + 4), (CX0, -78), PART, H_D, j=0)
    lc = (CX0, -84)
    lamp = ell(lc[0], lc[1], 8, 8, 0, 360, 16)
    p.shape(lamp, L_OFF, INNER, j=.05, step=99, clip=False)
    with layer(p, 'light'):
        p.shape(lamp, L_B, INNER, j=.05, step=99, clip=False)
        ax, ay = p.X((lc[0] - 2.5, lc[1] - 2.5)); p.raw('<circle cx="%.1f" cy="%.1f" r="2" fill="%s"/>' % (ax, ay, L_L))
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'space_loading', STAND, motion={'light': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_space_loading_light': dict(kind='opacity-blink', blinks=3, duration_s=1.8, trigger='هنگام رسیدن', iterations=1,
                                                         note='لایهٔ گنبد روشن ۳ بار محو و دوباره پدیدار می‌شود (زیرش گنبد خاموش ثابت است)؛ حالت ایستا و پایان = روشن؛ تزئینی؛ بدون حلقهٔ بیکار.'),
                         'reduced_motion': 'چراغ روشن ثابت'}
    (OUTD / 'space_loading.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
