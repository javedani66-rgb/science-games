#!/usr/bin/env python3
"""ایستگاه «بارانداز» (بازطراحی ۱۸ اکتبر شب، D123): قهرمان = چرخ‌دستیِ بارکش، درشت و پرجزئیات، روی سکوی دریایی:
چرخ‌های بزرگ پره‌دار، کف تخته‌ای با لبهٔ روشن، دسته، سه جعبهٔ رنگی با تخته‌های ضربدری، بشکه با کمربند آهنی، طناب،
و چوب‌پرچم بلند با پرچم راه‌راه که از بالای فیگور رد می‌شود (آزاد از بالا)؛ پایهٔ چرخ‌دستی سمت چپ می‌ماند.
لایه‌های متحرک (هرکدام چرخش حول مرکز خودش): node_wheel_dock_wheel = چرخ راست (id قدیمی)، node_wheel_dock_wheel_back = چرخ چپ.
بدنه، جعبه‌ها و دسته ثابت‌اند؛ چرخ‌ها دایره‌اند و در هر زاویه از سکو بیرون نمی‌زنند."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import station_kit
from station_kit import *
from functools import partial
station_kit.margin_check = partial(station_kit.margin_check, min_margin=4)   # D123: حاشیهٔ چپ/راست ≥۴px
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/wheel_dock'
XF = (1.23, 12.4, -13.2)
BED = '#c98a3a'; BED_L = '#e8b25a'; BED_D = '#8a5f0c'; WOOD_H = '#ffd84d'
CR_A = '#ffd84d'; CR_A_D = '#d9961c'; CR_B = '#f59a3a'; CR_B_D = '#b4620f'; CR_C = '#52c7c0'; CR_C_D = '#2a8f8a'
BAR = '#a8672f'; BAR_L = '#d29255'; IRON = '#c9d3ea'
WH = '#7b8fe0'; WH_L = '#a9b8f2'; WH_D = '#241a5e'
R = 12; WY = 4; WX = (-44, -8)


def flat(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def rect(p, x0, y0, x1, y1, col): flat(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col)


def crate(p, x0, y0, x1, y1, col, dk):
    p.shape([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col, PART, j=.2, step=6)
    rect(p, x0 + 3, y0 + 3, x1 - 3, y0 + 5.5, '#fff3b0')                           # نور بالا
    p.ln((x0 + 5, y0 + 6), (x1 - 5, y1 - 5), INNER, dk, j=0)                       # تختهٔ ضربدری
    p.ln((x1 - 5, y0 + 6), (x0 + 5, y1 - 5), INNER, dk, j=0)


def cart(p):
    # دسته (پشت بدنه)
    p.ln((-52, -8), (-62, -28), PART + 2 * INNER, NAVY, j=.05); p.ln((-52, -8), (-62, -28), PART, WOOD_H, j=.05)
    p.ln((-66, -30), (-58, -30), PART + 2 * INNER, NAVY, j=.05); p.ln((-66, -30), (-58, -30), PART, WOOD_H, j=.05)
    # چوب‌پرچم و پرچم راه‌راه (پشت جعبه‌ها)
    rect(p, -41, -108, -37, -59, '#7a4a1c'); rect(p, -41, -108, -39.5, -59, '#a8703c')
    flat(p, [(-37, -108), (-22, -106), (-8, -100), (-22, -98), (-37, -92)], '#ef6a4a')
    flat(p, [(-37, -103), (-22, -102), (-14, -100), (-22, -99), (-37, -98)], '#fff8e0')
    flat(p, [(-37, -108), (-26, -107), (-37, -105)], '#ff9b6a')
    # بدنه
    p.shape([(-58, -17), (6, -17), (6, 4), (-58, 4)], BED, PART, j=.2, step=6)
    rect(p, -54, -14, 2, -11.5, BED_L)
    for x in (-26, -14): p.ln((x, -7), (x, 1), INNER, BED_D, j=0)
    p.ln((-54, -7.5), (2, -7.5), INNER, BED_D, j=0)
    # بار
    crate(p, -50, -43, -26, -17, CR_A, CR_A_D)
    crate(p, -50, -69, -26, -43, CR_B, CR_B_D)
    crate(p, -24, -39, -2, -17, CR_C, CR_C_D)
    # بشکه
    p.shape([(-24, -63), (-4, -63), (-1, -53), (-4, -39), (-24, -39), (-27, -53)], BAR, PART, j=.25, step=5)
    rect(p, -24, -59, -4, -57, IRON); rect(p, -24, -46, -4, -44, IRON); rect(p, -23, -62, -17, -41, BAR_L)
    # طناب دور بار
    p.ln((-48, -52), (-28, -52), INNER, '#fff3c4', j=0)


def wheel(p, cx):
    p.shape(ell(cx, WY, R, R, 0, 360, 40), WH, PART, j=.3, step=99, clip=False)
    for a in (0, 60, 120):
        t = math.radians(a + 25)
        p.ln((cx - (R - 4) * math.cos(t), WY - (R - 4) * math.sin(t)), (cx + (R - 4) * math.cos(t), WY + (R - 4) * math.sin(t)), INNER, '#fff3c4', j=0)   # پره‌ها
    p.raw('<circle cx="%.1f" cy="%.1f" r="3.6" fill="%s"/>' % (*p.X((cx, WY)), WH_D))
    p.raw('<circle cx="%.1f" cy="%.1f" r="1.4" fill="%s"/>' % (*p.X((cx, WY)), '#ffd84d'))


def build(out=None):
    p = Pen('wheel_dock', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    for cx in WX:
        p.tipshadow(cx, WY + R - 1, 14); p.foot_tip(cx, WY + R - 2, 6)
    cart(p)
    with layer(p, 'wheel_back'): wheel(p, WX[0])
    with layer(p, 'wheel'): wheel(p, WX[1])
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    mo = {'wheel': dict(rotate=p.X((WX[1], WY))), 'wheel_back': dict(rotate=p.X((WX[0], WY)))}
    r = finish(p, 'wheel_dock', STAND, motion=mo, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(wheel=dict(layer='node_wheel_dock_wheel', rotate_about=[round(v, 1) for v in p.X((WX[1], WY))], note='چرخ راست؛ id قدیمی حفظ شد'),
                                             wheel_back=dict(layer='node_wheel_dock_wheel_back', rotate_about=[round(v, 1) for v in p.X((WX[0], WY))], note='چرخ چپ، لایهٔ جدید'))
    (OUTD / 'wheel_dock.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'inside': r['inside'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
