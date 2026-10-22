#!/usr/bin/env python3
"""ایستگاه F07 «استخر» (سرزمین ورزشگاه، سکوی سبز) — دور ۵ (دستور مدیر هنری: حوض روباز از بالا-کنار، ۶۵٪ وسط).
طرح قطعه‌به‌قطعه (واحد symbol؛ xf=1٫65؛ مرکز سکو = (0,0)):
 ۱) دیوارهٔ جلویی استخر: مستطیل گوشه‌گرد x -34..34، y -14..16، سفید-نقره‌ای تیره #bccbdc (عمق دیده شود).
 ۲) لبهٔ کاشی (رو): همان مستطیل y -14..10، سفید #eef4fb، نور #ffffff، دور OUT.
 ۳) آب: مستطیل گوشه‌گرد x -27..27، y -8..4، آبی روشن #43b0ec؛ سایهٔ تیز دیوارهٔ پشتی آبی تیره #2b86c8 (y -8..-3) داخل آب.
 ۴) خط‌کشی طناب: خط سفید ۳٫۹ افقی روی آب با پنج شناور رنگی (قرمز/زرد/قرمز/زرد/قرمز، دایرهٔ r=2٫6 تخت).
 ۵) نردبان فلزی: دو ریل کمانی #8b9ab2 (x 17 و 25) از آب بالا می‌آید، روی لبه خم می‌شود، دو پله.
 ۶) لایهٔ متحرک node_pool_wave: دو خط موج سفید روی آب، ±۲٫۵ افقی؛ حالت ایستا = صفر؛ بدون حلقهٔ بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/pool'

W_B, W_L, W_D = '#eef4fb', '#ffffff', '#b3c4d8'
A_B, A_L, A_D = '#43b0ec', '#8fd8ff', '#2b86c8'
RAIL = '#8b9ab2'
RED, YEL = '#e8554e', '#ffc93c'
XF = (1.55, 0, 8)


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def pline(p, pts, col, w, cap='round'):
    p.raw('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, w, cap))


def rrect(x0, y0, x1, y1, r, n=6):
    pts = []
    for (ox, oy, a0) in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n); pts.append((ox + r * math.cos(a), oy + r * math.sin(a)))
    return pts


def wave(x0, x1, y, amp=1.6, n=24):
    return [(x0 + (x1 - x0) * i / n, y + amp * math.sin(2 * math.pi * i / n * 1.5)) for i in range(n + 1)]


def build():
    p = Pen('pool', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((74, -20), (80, 6)), dot=(-76, -14)); p.xf = XF
    p.tipshadow(0, 18, 44); p.foot_tip(0, 16, 38)
    front = rrect(-34, -24, 34, 17, 9)
    p.shape(front, W_D, PART, j=.05, step=99)
    p.stroke(front, PART, j=.05, step=99)
    rim = rrect(-34, -24, 34, 10, 9)
    p.shape(rim, W_B, PART, j=.05, step=99)
    poly(p, [(-24, -22), (14, -22), (14, -20), (-24, -20)], W_L)
    p.stroke(rim, PART, j=.05, step=99)
    water = rrect(-27, -17, 27, 3, 5)
    p.shape(water, A_B, INNER, j=.05, step=99, clip=False)
    poly(p, [(-26, -16), (26, -16), (26, -10), (-26, -10)], A_D)
    # خط‌کشی طناب با شناور
    pline(p, [(-25, -3), (12, -3)], '#ffffff', INNER)
    for i, x in enumerate((-22, -13, -4, 5, 12)): disc(p, x, -3, 3.1, RED if i % 2 == 0 else YEL)
    with layer(p, 'wave'):
        pline(p, wave(-22, -8, 0.5), '#ffffff', INNER)
        pline(p, wave(-10, 6, -7.5), '#ffffff', INNER)
    # نردبان فلزی
    for xr in (19, 29):
        pline(p, [(xr, -6), (xr, -33)], NAVY, OUT)
    for y in (-14, -24): pline(p, [(19, y), (29, y)], NAVY, PART, 'butt')
    for xr in (19, 29):
        pline(p, [(xr, -6), (xr, -33)], RAIL, PART)
    for y in (-14, -24): pline(p, [(19, y), (29, y)], RAIL, INNER, 'butt')
    return pts


def wave(x0, x1, y, amp=1.6, n=24):
    return [(x0 + (x1 - x0) * i / n, y + amp * math.sin(2 * math.pi * i / n * 1.5)) for i in range(n + 1)]


def build():
    p = Pen('pool', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((74, -20), (80, 6)), dot=(-76, -14)); p.xf = XF
    p.tipshadow(0, 18, 44); p.foot_tip(0, 16, 38)
    front = rrect(-34, -14, 34, 16, 9)
    p.shape(front, W_D, PART, j=.05, step=99)
    p.stroke(front, PART, j=.05, step=99)
    rim = rrect(-34, -14, 34, 10, 9)
    p.shape(rim, W_B, PART, j=.05, step=99)
    poly(p, [(-22, -12), (22, -12), (22, -10), (-22, -10)], W_L)
    p.stroke(rim, PART, j=.05, step=99)
    water = rrect(-27, -8, 27, 4, 5)
    p.shape(water, A_B, INNER, j=.05, step=99, clip=False)
    poly(p, [(-26, -7), (26, -7), (26, -3), (-26, -3)], A_D)
    # خط‌کشی طناب با شناور
    pline(p, [(-25, -0.5), (25, -0.5)], '#ffffff', INNER)
    for i, x in enumerate((-22, -11, 0, 11, 22)): disc(p, x, -0.5, 3.1, RED if i % 2 == 0 else YEL)
    with layer(p, 'wave'):
        pline(p, wave(-20, -6, 2.2), '#ffffff', INNER)
        pline(p, wave(6, 18, -4.8), '#ffffff', INNER)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'pool', STAND, motion={'wave': dict(offsets=[(-2.5, 0), (0, 0), (2.5, 0), (0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_pool_wave': dict(translate_x=[0, 2.5, -2.5, 0], unit='symbol', repeats=3, duration_s=3.2, trigger='هنگام رسیدن/بیدارشدن',
                                               note='یک خط موج ±۲٫۵ واحد افقی، یکنواخت؛ حالت ایستا = جابه‌جایی صفر؛ تزئینی'),
                         'idle_loop': 'ندارد (بخش ۰ فهرست: حلقهٔ بیکار نداریم؛ ردیف F07 «بیکار آهسته» نوشته بود، با بخش ۰ تناقض دارد و تصمیم با مالک است)',
                         'reduced_motion': 'موج ثابت (جابه‌جایی صفر)'}
    (OUTD / 'pool.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
