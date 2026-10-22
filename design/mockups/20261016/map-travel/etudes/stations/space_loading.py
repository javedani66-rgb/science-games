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

CX0, CY0, RX, RY = -22, -44, 32, 38
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
    p = Pen('space_loading', 'space'); pad(p, line=((50, 30), (70, 27)), tri=((36, -22), (74, 6)), dot=(68, -14)); p.xf = XF
    p.tipshadow(2, BASE + 3, 52); p.foot_tip(CX0 - 14, BASE + 2, 14); p.foot_tip(50, BASE + 2, 10)
    # ۱) پایهٔ فولادی
    sl = rect(CX0 - 34, -3, CX0 + 34, BASE)
    p.shape(sl, H_B, PART, j=.1, step=6, clip=False)
    poly(p, rect(CX0 - 30, -0, CX0 - 12, 2.5), H_L)
    poly(p, rect(CX0 + 18, 0, CX0 + 30, BASE - 1.5), H_D, .85)
    p.stroke(sl, PART, j=.1, step=6)
    # ۲) کپسول
    cap = arc(1, 1, 0, 360, 36)
    p.shape(cap, C_B, OUT, j=.1, step=8)
    poly(p, arc(.93, .93, -62, 62, 12) + arc(.62, .93, 62, -62, 12)[:0] + [(CX0 + RX * .93 * math.cos(math.radians(a)) - 15, CY0 + RY * .93 * math.sin(math.radians(a))) for a in range(62, -63, -10)], C_D)   # سایهٔ هلالی راست
    poly(p, arc(.86, .86, 200, 258, 8) + arc(.74, .74, 258, 200, 8), C_L)                                       # نور چپ
    p.stroke(cap, OUT, j=.1, step=8)
    # ۳) دریچهٔ باز و پنجرهٔ گرد
    hole = [(CX0 - 13, -9)] + ell(CX0, -26, 13, 13, 180, 360, 10) + [(CX0 + 13, -9)]
    p.shape(hole, HOLE, INNER, j=.06, step=6, clip=False)
    p.shape(ell(CX0, -62, 8, 8, 0, 360, 16), GLASS, INNER, j=.05, step=99, clip=False)
    poly(p, rect(CX0 - 4.5, -66, CX0 - 1.5, -61), '#ffffff')
    # ۴) رمپ فلزی زرد (از کف دریچه تا زمین)
    ramp = [(CX0 - 6, -17), (32, -1), (32, BASE), (CX0 - 6, -9)]
    p.shape(ramp, Y_B, PART, j=.08, step=6, clip=False)
    for x in (4, 14, 24):
        y0 = -17 + (x - (CX0 - 6)) * 16 / 54
        poly(p, [(x - 1.8, y0 + 3), (x + 1.8, y0 + 3), (x + 1.8, y0 + 8.5), (x - 1.8, y0 + 8.5)], Y_D)
    poly(p, [(CX0 - 3, -15.5), (30, -1.5), (30, 1), (CX0 - 3, -12.5)], Y_L)
    p.stroke(ramp, PART, j=.08, step=6)
    # ۵) جعبهٔ بار
    box = rect(37, -22, 63, BASE)
    p.shape(box, X_B, PART, j=.08, step=6)
    poly(p, rect(41, -18, 44.5, BASE - 4), X_L)
    poly(p, rect(57, -18, 60, BASE - 3), X_D, .8)
    poly(p, [(40, -19), (44, -19), (60, 3), (56, 3)], X_D)                                                       # ضربدر
    poly(p, [(56, -19), (60, -19), (44, 3), (40, 3)], X_D)
    p.stroke(box, PART, j=.08, step=6)
    # ۶) پایهٔ چراغ و گنبد خاموش
    p.shape(rect(CX0 - 8, -88, CX0 + 8, -78), H_B, INNER, j=.05, step=6, clip=False)
    d = dome(9)
    p.shape(d, L_OFF, INNER, j=.05, step=99, clip=False)
    # ۷) لایهٔ متحرک: گنبد روشن
    with layer(p, 'light'):
        p.shape(d, L_B, INNER, j=.05, step=99, clip=False)
        ax, ay = p.X((CX0 - 3.5, -93)); p.raw('<circle cx="%.1f" cy="%.1f" r="2.2" fill="%s"/>' % (ax, ay, L_L))
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
