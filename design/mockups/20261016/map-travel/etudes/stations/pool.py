#!/usr/bin/env python3
"""ایستگاه F07 «استخر» (سرزمین ورزشگاه، پالت sports). مقطع استخر کوتاه و عریض + نردبان (بازطراحی پس از FAIL ناظر).
طرح قطعه‌به‌قطعه (واحد symbol؛ مرکز سکو = (0,0)؛ همه چیز سمت چپ تا جای فیگور سمت راست بماند):
 ۱) پوستهٔ کاشی U: x -64..22، بالا y -58، پایین y 8؛ سه پله سفید-آبی #eef4fb، #ffffff، #bccbdc؛ دیواره ۱۲، کف ۱۴؛
    پنجرهٔ حوض x -52..10 (پهنا ۶۲)، عمق تا y -6. لبهٔ روشن بالای دیواره‌ها، سایهٔ راست 18,-34 22,-34 22,-2 18,-2. بدون درز کاشی.
 ۲) درون پنجره: هوای #e6f6ff؛ آب تخت #43b0ec (y -35..-10) با ۴ واحد فاصله از خط دور دیواره (خط دور را نمی‌پوشاند).
 ۳) خط شنا: طناب سفید ۳٫۹ روی آب (y -24) با دو توپک تخت (قرمز و زرد) در دو لبه.
 ۴) نردبان فولاد میان‌رنگ #8b9ab2: دو ریل ۵٫۸، هر کدام از روی دیواره راست (x ۱۲ و ۲۰) بالا می‌رود، روی لبه خم می‌شود (کمان تو‌در‌تو)
    و در آب پایین می‌رود (x -5 و -19؛ ۸ از دیواره فاصله) تا y -14؛ سه پلهٔ ۳٫۹. آب ۶۸٪ آزاد.
 ۵) لایهٔ متحرک node_pool_wave: یک موج سفید ۳٫۹ روی آب، ±۲٫۵ افقی؛ حالت ایستا = جابه‌جایی صفر؛ بدون حلقهٔ بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/pool'

W_B, W_L, W_D = '#eef4fb', '#ffffff', '#bccbdc'
A_B, A_L, A_D = '#43b0ec', '#8fd8ff', '#2b86c8'
S_B, S_L, S_D = '#d6dde8', '#ffffff', '#8b9ab2'
AIR = '#e6f6ff'
L, R_, TOP, BOT = -64, 22, -58, 8
WL, WR, WT, WB = -52, 10, -58, -6       # پنجره
WATER = -35
RAIL = '#8b9ab2'
RED, YEL = '#e8554e', '#ffc93c'


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def pline(p, pts, col, w, cap='round'):
    p.raw('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, w, cap))


def wave(x0, x1, y, amp=2.0, n=40):
    return [(x0 + (x1 - x0) * i / n, y + amp * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]


def build():
    p = Pen('pool', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((38, -20), (62, 6)), dot=(58, -16)); p.xf = (1.0, 4, 0)
    p.tipshadow(-21, BOT + 3, 50); p.foot_tip(-21, BOT + 1, 36)
    shell = [(L, TOP), (WL, TOP), (WL, WB), (WR, WB), (WR, TOP), (R_, TOP), (R_, BOT), (L, BOT)]
    p.shape(shell, W_B, OUT, j=.15, step=8)
    poly(p, [(L + 4, TOP + 4), (WL - 4, TOP + 4), (WL - 4, TOP + 10), (L + 4, TOP + 10)], W_L)
    poly(p, [(WR + 4, TOP + 4), (R_ - 4, TOP + 4), (R_ - 4, TOP + 10), (WR + 4, TOP + 10)], W_L)
    poly(p, [(L + 4, BOT - 10), (R_ - 4, BOT - 10), (R_ - 4, BOT - 4), (L + 4, BOT - 4)], W_D)
    poly(p, [(18, -34), (22, -34), (22, -2), (18, -2)], W_D)
    # آب (زیر خط دور؛ خط دور را نمی‌پوشاند)
    poly(p, [(WL, WT + 4), (WR, WT + 4), (WR, WATER), (WL, WATER)], AIR)
    poly(p, [(WL, WATER), (WR, WATER), (WR, WB), (WL, WB)], A_B)
    p.stroke(shell, OUT, j=.15, step=8)
    # خط شنا
    ry = -17
    pline(p, [(WL + 10, ry), (WR - 7.6, ry)], '#ffffff', INNER)
    p.raw('<circle cx="%.1f" cy="%.1f" r="3.4" fill="%s"/>' % (*p.X((WL + 10, ry)), RED))
    p.raw('<circle cx="%.1f" cy="%.1f" r="3.4" fill="%s"/>' % (*p.X((WR - 7.6, ry)), YEL))
    with layer(p, 'wave'):
        pline(p, wave(WL + 10, WR - 10, WATER + 5), '#ffffff', INNER)
    # نردبان: دو ریل تو‌در‌تو، از روی دیواره، روی لبه، به آب
    for sx, hy, xv in ((12, WT - 5, -5), (20, WT - 10, -19)):
        r = 4.5; X = p.X
        a, b, c, d = X((sx, WT + 6)), X((sx, hy)), X((xv, hy)), X((xv, -12))
        p.raw('<path d="M%.1f,%.1f L%.1f,%.1f Q%.1f,%.1f %.1f,%.1f L%.1f,%.1f Q%.1f,%.1f %.1f,%.1f L%.1f,%.1f" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"/>' % (
            a[0], a[1], b[0], b[1] + r, b[0], b[1], b[0] - r, b[1], c[0] + r, c[1], c[0], c[1], c[0], c[1] + r, d[0], d[1], RAIL, PART))
    for y in (-50, -40, -24):
        pline(p, [(-19, y), (-5, y)], RAIL, INNER, 'butt')
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
