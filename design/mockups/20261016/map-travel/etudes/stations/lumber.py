#!/usr/bin/env python3
"""ایستگاه «انبار الوار» (بازطراحی ۱۸ اکتبر شب، D123): سه کندهٔ بلند و استوانه‌ای خوابیده از کنار (روی هم)، 
هر کنده پوست قهوه‌ای با نور، سرِ بریدهٔ روشن، حلقهٔ سالیانه و مغز دارد؛ دو طناب دور پشته؛ زیر پشته دو تخته‌پایه.
کنار پشته دکل با بازوی چوبی (جرثقیل کوچک الوار) و یک کندهٔ آویزان با دو طناب است؛ بازو از بالای فیگور رد می‌شود (آزاد از بالا)؛
پایهٔ پشته سمت چپ می‌ماند. سکوی زمینی.
لایهٔ متحرک node_lumber_marks = حلقهٔ سالیانهٔ سرِ کندهٔ بالا (کمان باز که حول مرکز سر می‌چرخد). حلقه‌های بقیه ثابت‌اند."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import station_kit
from station_kit import *
from functools import partial
station_kit.margin_check = partial(station_kit.margin_check, min_margin=4)   # D123: حاشیهٔ چپ/راست ≥۴px
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/v2/lumber'
XF = (1.0, -5.0, 3.0)
BARK = '#a8672f'; BARK_L = '#d29255'; BARK_D = '#7a4a1f'; FACE = '#f2cf8e'; FACE_L = '#fbe3b0'; RING = '#c98f4a'; PITH = '#8a4f1f'; ROPE = '#fff3c4'
WOOD = '#7a4a1c'; WOOD_L = '#a8703c'

SHOTS = SHOTS.replace('/v2/lumber', '/v3/lumber')
LEN = 58; R = 9.5
LOGS = [(-52, -6.5), (-47, -25.5), (-50, -44.5)]          # (x سرِ چپ، y مرکز) پایین تا بالا؛ سر بریده فقط سمت چپ
POSTX = 17
ARM_Y = -112; HX = -8; HCY = -90; HLEN = 40; HR = 7.5


def flat(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def rect(p, x0, y0, x1, y1, col): flat(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col)


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def log(p, xl, cy, ln_, r, part=PART, bands=(), face=True):
    """کندهٔ خوابیده از کنار: بدنهٔ استوانه؛ سرِ چپ = بیضی روشن با حلقهٔ سالیانه؛ سمت راست پوست گرد (بدون حلقه)."""
    xr = xl + ln_
    pts = ell(xr, cy, 5, r, -90, 90, 8) + ell(xl, cy, 6.5, r, 90, 270, 12)
    p.shape(pts, BARK, part, j=.2, step=99, clip=False)
    rect(p, xl + 12, cy - r + 3, xr - 3, cy - r + 5.8, BARK_L)                                        # نور بالا
    for (a, b, dy) in ((12, 30, -1), (40, 54, 3.5), (18, 34, 6.5)):                                        # خط‌های پوست
        if xl + b < xr - 4: p.ln((xl + a, cy + dy), (xl + b, cy + dy), INNER * .8, BARK_D, j=.05)
    for bx in bands:                                                                                     # طناب بسته (نوار تخت روی کنده)
        rect(p, xl + bx, cy - r + 2.4, xl + bx + 4, cy + r - 2.4, ROPE)
    if face:
        p.raw('<ellipse cx="%.1f" cy="%.1f" rx="4.8" ry="%.1f" fill="%s"/>' % (*p.X((xl, cy)), r - 2.6, FACE))                    # سرِ بریده
        p.raw('<ellipse cx="%.1f" cy="%.1f" rx="1.9" ry="%.1f" fill="none" stroke="%s" stroke-width="2.4"/>' % (*p.X((xl + .4, cy + .4)), r * .36, RING))   # حلقهٔ سالیانه
        p.raw('<ellipse cx="%.1f" cy="%.1f" rx=".9" ry="1.4" fill="%s"/>' % (*p.X((xl + .5, cy + .5)), PITH))


def stack(p):
    for x in (-42, -8): p.tipshadow(x + 11, 14, 12)
    for x in (-42, -8):                                                   # دو تیرک زیر پشته
        p.shape([(x, 1), (x + 22, 1), (x + 22, 13), (x, 13)], WOOD, INNER, j=.2, step=8, clip=False)
        p.ln((x + 5, 8), (x + 17, 8), INNER, WOOD_L, j=.05)
    for xl, cy in LOGS: log(p, xl, cy, LEN, R, bands=(18, 38))


def crane(p):
    """جرثقیل چوبی آویز: ستون راست (تیر نگه‌دارنده)، بازوی افقی، تکیه‌گاه مورب، یک کندهٔ آویزان با دو طناب."""
    rect(p, POSTX - 4, ARM_Y - 6, POSTX + 4, 12, WOOD); rect(p, POSTX - 4, ARM_Y - 6, POSTX - 1.6, 12, WOOD_L)
    rect(p, -26, ARM_Y, POSTX + 4, ARM_Y + 8, WOOD); rect(p, -26, ARM_Y, POSTX + 4, ARM_Y + 2.6, WOOD_L)
    p.ln((POSTX - 2, ARM_Y + 28), (POSTX - 22, ARM_Y + 8), PART, WOOD, j=0)
    for dx in (-12, 12):
        p.ln((HX + dx, ARM_Y + 8), (HX + dx, HCY - HR + 2), INNER, ROPE, j=0)
    log(p, HX - HLEN / 2, HCY, HLEN, HR, INNER)


def build(out=OUTD):
    p = Pen('lumber', 'land'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.foot_tip(POSTX, 12, 6)
    crane(p)
    stack(p)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'lumber', STAND, motion={}, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(note='بدون لایهٔ متحرک الزامی؛ نمادِ ایستا. اگر خواستند: کندهٔ آویز با جرثقیل (لایهٔ پیشنهادی بعدی) ثابت می‌ماند تا طراحی موشن بیاید.')
    (OUTD / 'lumber.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'inside': r['inside'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
