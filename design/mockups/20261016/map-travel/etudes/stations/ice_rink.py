#!/usr/bin/env python3
"""ایستگاه F06 «پیست اسکی روی یخ» (سرزمین ورزشگاه، سکوی sports #7fbf4a، رنگ‌مایهٔ ۹۳°).
طرح قطعه‌به‌قطعه (مختصات symbol، مرکز سکو (0,0)؛ ۱ واحد ≈ ۰٫۷۲px):
 ۱) تختهٔ یخ (بلوک، نمای جلو + رویهٔ باریک + دیوارهٔ راست): رویه #d6f1fb، جلو #a5dcf0، راست #7fc0dc؛ رنگ‌مایه ۱۹۰° (۹۷° از سکو).
    خط دور PART، نوار نور تخت، دو ترک راست (خط تخت) روی دیوارهٔ جلو.
 ۲) لایهٔ متحرک node_ice_rink_glint: دو نوار سفید مایل (۷ و ۳ واحد) روی دیوارهٔ جلوی یخ (تزئینی). حالت ایستا = پایان (نوارها در راست).
 ۳) اسکی بلند و باریک (۱۵ واحد ضخامت، خط PART): قرمز مرجانی #e0553a/#ff9a6c/#9c2f1c، نوک چپ خمیده به بالا؛ همان قرمز بدنهٔ جرثقیل؛ رنگ‌مایه ۱۰° (۸۳° از سکو).
 ۴) بستِ زرد: صفحهٔ باریک روی اسکی (خط INNER).
 ۵) پوتین اسکی: بنفش-آبی #6f63d9/#9a90f0/#4a3fa8 (رنگ‌مایه ۲۴۵°)، روی بست؛ ساق بلند برای نام‌پذیری «اسکی» (PART).
 فقط خط‌های ۷٫۶/۵٫۸/۳٫۹. بدون چرخ (فرق با F09)، شفاف نیست (فرق با E06)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8)
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/ice_rink'

ICE, ICE_L, ICE_D, ICE_S, CRACK = '#d6f1fb', '#ffffff', '#a5dcf0', '#7fc0dc', '#5f9fc0'
RED, RED_L, RED_D = '#e0553a', '#ff9a6c', '#9c2f1c'
YEL, YEL_L, YEL_D = '#ffd84d', '#fff0a0', '#d9961c'
BT, BT_L, BT_D = '#6f63d9', '#9a90f0', '#4a3fa8'
XF = (1.0, -2.0, 0.0)

# تختهٔ یخ: جلو x∈[XL,XR]، y∈[0,FH]؛ رویه عمق D (کج به بالا-راست)
XL, XR, FH, D = -56, 18, 18, 14
FRONT = [(XL, 0), (XR, 0), (XR, FH), (XL, FH)]
TOPF = [(XL, 0), (XR, 0), (XR + D, -D), (XL + D, -D)]
SIDE = [(XR, 0), (XR + D, -D), (XR + D, FH - D), (XR, FH)]

# اسکی ایستاده، فرو رفته در رویهٔ یخ؛ نوک بالا به چپ خمیده
XS, SB, ST_TOP, BEND = -8, -5, -108, -66
def cl(y):
    return XS if y >= BEND else XS - 20 * ((BEND - y) / (BEND - ST_TOP)) ** 2
def hw(y):
    return 7.5 if y >= BEND else 7.5 - 3.5 * (BEND - y) / (BEND - ST_TOP)
def ski_pts():
    ys = [SB - i * (SB - ST_TOP) / 30 for i in range(31)]
    return [(cl(y) - hw(y), y) for y in ys] + [(cl(y) + hw(y), y) for y in ys][::-1]


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def sp(p, pts, fill, sw, clip=True):
    """چندضلعی با گوشهٔ تیز، دور سرمه‌ای؛ clip=True ⇒ نور/سایهٔ سکو روی آن می‌افتد."""
    q = p.X(pts); d = 'M' + 'L'.join('%.1f,%.1f' % z for z in q) + 'Z'
    p.o.append('<path d="%s" fill="%s" class="eo" stroke-width="%s"/>' % (d, fill, sw))
    if clip: p.clip.append(d)


GL_REST = 46
def strips(dx):
    out = []
    for x, w in ((0, 7), (8, 3)):
        a = XL + 12 + x + dx; y0, y1 = 5, FH - 5
        out.append([(a + .5 * (FH - y0) / 2, y0), (a + w + .5 * (FH - y0) / 2, y0), (a + w, y1), (a, y1)])
    return out


def build():
    p = Pen('ice_rink', 'sports'); pad(p, line=((-58, 28), (-42, 31)), tri=((62, -22), (66, 12)), dot=(44, 24))
    p.xf = XF
    p.tipshadow(-8, FH + 2, 38); p.foot_tip(-8, FH, 26)
    # ۱) یخ
    sp(p, SIDE, ICE_S, PART); sp(p, FRONT, ICE_D, PART); sp(p, TOPF, ICE, PART)
    poly(p, [(XL + 6, 4.5), (XL + 6, 8), (XL + 20, 8), (XL + 20, 4.5)], ICE_L)                 # نور لبهٔ بالا-چپ
    for c0, c1 in (((-30, 3), (-35, 16)), ((-14, 3), (-17, 11))):                                  # ترک‌های راست (تک‌خط)
        p.ln(c0, c1, 3, CRACK, j=0)
    # ۲) درخشش (لایهٔ متحرک)
    with layer(p, 'glint'):
        for s in strips(GL_REST):
            poly(p, s, '#ffffff', .62)
    # ۳) اسکی
    poly(p, [(XS - 10, SB + .5), (XS + 12, SB + .5), (XS + 16, SB + 4), (XS - 6, SB + 4)], ICE_D, .9)          # سایهٔ تماس روی یخ
    body = ski_pts()
    sp(p, body, RED, PART)
    poly(p, [(cl(y) - 4.5, y) for y in (SB - 6, -40, -70, -90)] + [(cl(y) - 1.5, y) for y in (-90, -70, -40, SB - 6)], RED_L)   # نور چپ
    poly(p, [(XS + 3, SB - 6), (XS + 3, -66), (XS + 6, -66), (XS + 6, SB - 6)], RED_D)                                 # سایهٔ تیز راست
    p.stroke(body, PART, j=.04, step=99)
    # ۴) بست زرد: صفحهٔ عرضی روی اسکی
    sp(p, [(XS - 12, -30), (XS + 12, -30), (XS + 12, -43), (XS - 12, -43)], YEL, INNER, False)
    poly(p, [(XS - 8, -40), (XS + 3, -40), (XS + 3, -37.5), (XS - 8, -37.5)], YEL_L)
    poly(p, [(XS - 9, -34), (XS + 9, -34), (XS + 9, -32), (XS - 9, -32)], YEL_D)
    return p


if __name__ == '__main__':
    p = build()
    mo = {'glint': dict(offsets=[(-50 * XF[0], 0), (0, 0)])}
    r = finish(p, 'ice_rink', None, motion=mo, out=OUTD, shots=SHOTS)
    sp_ = r['spec']
    sp_['motion_spec'] = {'node_ice_rink_glint': dict(
        kind='دو نوار سفید مایل روی دیوارهٔ جلوی یخ؛ حالت ایستا = پایان حرکت (نوارها در راست)',
        translate_x_symbol_units=[-50, 0], translate_x_map_px=[round(-50 * K, 1), 0],
        opacity='از ۰ تا ۰٫۶۲ در ۱۵٪ اول؛ بعد ثابت',
        duration_s=1.8, easing='ease-in-out', loop=False, trigger='رسیدن کودک (یک‌بار)',
        how='گروه glint را از translateX(-50) به 0 ببر؛ نوارها از چپ به راست روی یخ می‌گذرند. تزئینی است (لغزش را F01/F09 نشان می‌دهند). بدون حلقهٔ بیکار.',
        note='با reduced-motion ثابت در وضع پایان.')}
    (OUTD / 'ice_rink.json').write_text(json.dumps(sp_, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
