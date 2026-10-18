#!/usr/bin/env python3
"""ایستگاه «انبار الوار» (بازطراحی ۱۸ اکتبر شب، D123): پشتهٔ هرمی شش کنده از سر (سه + دو + یک) که کنار هم چیده شده‌اند؛
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
XF = (1.0, -4.0, -2.0)
BARK = '#a8672f'; BARK_L = '#d29255'; BARK_D = '#7a4a1f'; FACE = '#f2cf8e'; FACE_L = '#fbe3b0'; RING = '#c98f4a'; PITH = '#8a4f1f'; ROPE = '#fff3c4'
WOOD = '#7a4a1c'; WOOD_L = '#a8703c'
R = 13; SP = 24.5
ROWS = [(-3, [-47, -22.5, 2]), (-24.2, [-34.7, -10.2]), (-45.4, [-22.5])]       # (y مرکز، x مرکزها)
TOPC = (-22.5, -45.4)
ARM_Y = -126; LOGX = 26


def flat(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def rect(p, x0, y0, x1, y1, col): flat(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col)


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def ringline(p, x, y, r, col, w=3.5):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="%s"/>' % (a, b, r, col, w))


def endlog(p, cx, cy):
    """کندهٔ از سر: پوست (با خط دور)، سرِ بریدهٔ روشن، حلقهٔ سالیانه، مغز و نور."""
    p.shape(ell(cx, cy, R, R, 0, 360, 44), BARK, INNER, j=.3, step=99)
    disc(p, cx, cy, R - 5.4, FACE)
    p.raw('<path d="M%.1f,%.1f A%s,%s 0 0 1 %.1f,%.1f" fill="none" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>' % (
        *p.X((cx - 6.4, cy - 3.2)), 7.2, 7.2, *p.X((cx + 1, cy - 7.2)), FACE_L))                    # نور روی سر
    ringline(p, cx + .8, cy + .6, 4.6, RING)
    disc(p, cx + .8, cy + .6, 1.6, PITH)


def hull(pts):
    pts = sorted(set(pts))
    cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo = []; up = []
    for q in pts:
        while len(lo) > 1 and cr(lo[-2], lo[-1], q) <= 0: lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(up) > 1 and cr(up[-2], up[-1], q) <= 0: up.pop()
        up.append(q)
    return lo[:-1] + up[:-1]


def logs(p):
    for y, xs in ROWS:
        for x in xs: p.tipshadow(x, y + R - 1, 12) if y == -3 else None
    pts = [(x + (R - 1) * math.cos(a * math.pi / 8), y + (R - 1) * math.sin(a * math.pi / 8)) for y, xs in ROWS for x in xs for a in range(16)]
    p.shape(hull(pts), BARK_D, PART, j=.2, step=99)                         # پشتیبان تیره: درز میان کنده‌ها تیره‌چوبی می‌شود نه سرمه‌ای
    for y, xs in ROWS:
        for x in xs: endlog(p, x, y)
    for y in (-13, -33):                                                    # طناب‌های دور پشته (دو ردیف)
        pass
    p.ln((-58, -14), (14, -14), INNER, ROPE, j=0)
    p.ln((-46, -35), (2, -35), INNER, ROPE, j=0)
    disc(p, -8, -14, 3, ROPE)


def hoist(p):
    rect(p, -53, ARM_Y - 6, -46, 6, WOOD); rect(p, -53, ARM_Y - 6, -51, 6, WOOD_L)         # دکل
    rect(p, -58, ARM_Y, 42, ARM_Y + 7, WOOD); rect(p, -58, ARM_Y, 42, ARM_Y + 2, WOOD_L)       # بازو
    p.ln((-49, ARM_Y + 30), (-26, ARM_Y + 8), INNER, WOOD, j=0)                                 # تکیه‌گاه مورب
    p.ln((LOGX - 10, ARM_Y + 7), (LOGX - 10, ARM_Y + 22), INNER, ROPE, j=0)
    p.ln((LOGX + 10, ARM_Y + 7), (LOGX + 10, ARM_Y + 22), INNER, ROPE, j=0)
    # کندهٔ آویزان (از کنار، سر بریده سمت چپ)
    x0, x1, cy, rr = LOGX - 20, LOGX + 20, ARM_Y + 31, 8.5
    pts = ell(x1, cy, 3, rr, -90, 90, 8) + ell(x0, cy, 5, rr, 90, 270, 10)
    p.shape(pts, BARK, PART, j=.25, step=99, clip=False)
    rect(p, x0 + 6, cy - rr + 3.5, x1 - 2, cy - rr + 6, BARK_L)
    p.raw('<ellipse cx="%.1f" cy="%.1f" rx="3" ry="%.1f" fill="%s"/>' % (*p.X((x0, cy)), rr - 3.4, FACE))


def build(out=OUTD):
    p = Pen('lumber', 'land'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    for x in (-47, 2): p.foot_tip(x, 10, 6)
    hoist(p)
    logs(p)
    with layer(p, 'marks'):                                                  # کمان حلقهٔ سالیانهٔ کندهٔ بالا (می‌چرخد)
        x, y = p.X((TOPC[0] + .8, TOPC[1] + .6)); r = 4.6; a0, a1 = math.radians(50), math.radians(320)
        d = 'M%.1f,%.1f A%s,%s 0 1 1 %.1f,%.1f' % (x + r * math.cos(a0), y + r * math.sin(a0), r, r, x + r * math.cos(a1), y + r * math.sin(a1))
        p.raw('<path d="%s" fill="none" stroke="%s" stroke-width="3.5" stroke-linecap="round"/>' % (d, '#e6b46a'))
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    cen = p.X((TOPC[0] + .8, TOPC[1] + .6))
    r = finish(p, 'lumber', STAND, motion={'marks': dict(rotate=cen)}, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(marks=dict(layer='node_lumber_marks', rotate_about=[round(v, 1) for v in cen],
                                                         note='کمان حلقهٔ سالیانهٔ سرِ کندهٔ بالای پشته می‌چرخد؛ id قدیمی حفظ شد'))
    (OUTD / 'lumber.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'inside': r['inside'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
