#!/usr/bin/env python3
"""ایستگاه F07 «استخر» (سرزمین ورزشگاه، پالت sports). مقطع استخر کوتاه و عریض + نردبان.
طرح قطعه‌به‌قطعه (واحد symbol؛ مرکز سکو = (0,0)؛ همه چیز سمت چپ تا جای فیگور سمت راست بماند):
 ۱) پوستهٔ کاشی U شکل: x -80..14، بالا y -40، پایین y 8؛ سه پله: سفید-آبی #eef4fb، روشن #ffffff، تیره #bccbdc؛ خط OUT.
    دیوارهٔ چپ و راست ۱۲ پهن، کف ۸ (پنجره x -68..2، پایین y 0). لبهٔ روشن بالای دیواره و درز کاشی ریز تخت.
 ۲) درون پنجره: هوای روشن #e6f6ff (تخت)، آب آبی (۲۰۰°) از y -22 تا 0 با خط INNER؛ پله‌ها: #43b0ec، #8fd8ff، #2b86c8.
 ۳) نردبان فولاد روشن (#d6dde8، روشن #fff، تیره #8b9ab2) روی محور x -15 (مرکز دو ریل): ریل‌ها ۱۱ پهن، U وارونه بالای لبه
    (y -56)، دو پله افقی؛ از y -56 تا -6؛ با PART. روی آب و دیواره راست.
 ۴) لایهٔ متحرک node_pool_wave: دو خط موج (سفید روی آب و آبی تیره پایین‌تر) به‌صورت تخت، ±۴ واحد افقی.
 هیچ لایهٔ دیگر متحرک نیست؛ حالت ایستا = جابه‌جایی صفر."""
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
L, R_, TOP, BOT = -80, 22, -48, 8
WL, WR, WT, WB = -64, 6, -48, -6       # پنجره
WATER = -30
LAD = (-6, -62, -12)                    # محور ریل، بالای نردبان، پایین


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def wave(x0, x1, y, amp=2.6, per=14, n=40):
    return [(x0 + (x1 - x0) * i / n, y + amp * math.sin(2 * math.pi * (x0 + (x1 - x0) * i / n) / per)) for i in range(n + 1)]


def build():
    p = Pen('pool', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.0, 8, 0)
    p.tipshadow(-33, BOT + 3, 46); p.foot_tip(-33, BOT + 1, 34)
    # ۱) پوستهٔ U
    shell = [(L, TOP), (WL, TOP), (WL, WB), (WR, WB), (WR, TOP), (R_, TOP), (R_, BOT), (L, BOT)]
    p.shape(shell, W_B, OUT, j=.15, step=8)
    poly(p, [(L + 4, TOP + 4), (WL - 4, TOP + 4), (WL - 4, TOP + 10), (L + 4, TOP + 10)], W_L)           # لبهٔ روشن چپ
    poly(p, [(WR + 4, TOP + 4), (R_ - 4, TOP + 4), (R_ - 4, TOP + 10), (WR + 4, TOP + 10)], W_L)         # لبهٔ روشن راست
    poly(p, [(L + 4, BOT - 10), (R_ - 4, BOT - 10), (R_ - 4, BOT - 4), (L + 4, BOT - 4)], W_D)             # کف تیره
    poly(p, [(WR + 8, WB), (R_ - 4, WB), (R_ - 4, BOT - 10), (WR + 8, BOT - 10), (WR + 8, TOP + 14)], W_D)  # سایهٔ راست
    for y in (-28, -12):                                                                                # درز کاشی
        p.ln((L + 4, y), (WL - 4, y), 2, '#9fb4cc', j=0)
    p.ln((WR + 4, -28), (R_ - 4, -28), 2, '#9fb4cc', j=0); p.ln((WR + 4, -12), (R_ - 4, -12), 2, '#9fb4cc', j=0)
    p.stroke(shell, OUT, j=.15, step=8)
    # ۲) آب
    poly(p, [(WL + 2, WT + 3), (WR - 2, WT + 3), (WR - 2, WATER), (WL + 2, WATER)], AIR)
    water = [(WL, WATER), (WR, WATER), (WR, WB), (WL, WB)]
    poly(p, water, A_B)
    poly(p, [(WL + 4, WATER + 5), (WR - 4, WATER + 5), (WR - 4, WATER + 9), (WL + 4, WATER + 9)], A_L)
    poly(p, [(WL + 4, WB - 6), (WR - 4, WB - 6), (WR - 4, WB - 3), (WL + 4, WB - 3)], A_D)
    # ۴) موج (لایهٔ متحرک)
    with layer(p, 'wave'):
        pts = wave(-56, -28, WATER + 1, 2.2, 14)
        p.raw('<polyline points="%s" fill="none" stroke="#ffffff" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), INNER))
        pts = wave(-54, -34, WATER + 14, 2.2, 14)
        p.raw('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), A_D, INNER))
    # ۳) نردبان: U وارونه
    cx, top, bot = LAD[0], LAD[1], LAD[2]; hw_, gap = 17, 5
    u = [(cx - hw_, bot), (cx - hw_, top), (cx + hw_, top), (cx + hw_, bot), (cx + hw_ - 11, bot), (cx + hw_ - 11, top + 11), (cx - hw_ + 11, top + 11), (cx - hw_ + 11, bot)]
    p.shape(u, S_B, PART, j=.1, step=8, clip=False)
    poly(p, [(cx - hw_ + 3, top + 3), (cx + hw_ - 3, top + 3), (cx + hw_ - 3, top + 6), (cx - hw_ + 3, top + 6)], S_L)
    for y in (-40, -24):
        poly(p, [(cx - hw_ + 9, y), (cx + hw_ - 9, y), (cx + hw_ - 9, y + 5), (cx - hw_ + 9, y + 5)], S_D)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'pool', STAND, motion={'wave': dict(offsets=[(-4, 0), (0, 0), (4, 0), (0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_pool_wave': dict(translate_x=[0, 4, -4, 0], unit='symbol', repeats=3, duration_s=3.2, trigger='هنگام رسیدن/بیدارشدن',
                                               note='دو خط موج ±۴ واحد افقی، یکنواخت؛ حالت ایستا = جابه‌جایی صفر؛ تزئینی'),
                         'idle_loop': 'ندارد (بخش ۰ فهرست: حلقهٔ بیکار نداریم؛ ردیف F07 «بیکار آهسته» نوشته بود، با بخش ۰ تناقض دارد و تصمیم با مالک است)',
                         'reduced_motion': 'موج ثابت (جابه‌جایی صفر)'}
    (OUTD / 'pool.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
