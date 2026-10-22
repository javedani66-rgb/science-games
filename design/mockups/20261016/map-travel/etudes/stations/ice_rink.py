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
XF = (0.9, 5.0, -3.0)

# تختهٔ یخ: جلو x∈[XL,XR]، y∈[0,FH]؛ رویه عمق D (کج به بالا-راست)
XL, XR, FH, D = -86, 36, 24, 14
FRONT = [(XL, 0), (XR, 0), (XR, FH), (XL, FH)]
TOPF = [(XL, 0), (XR, 0), (XR + D, -D), (XL + D, -D)]
SIDE = [(XR, 0), (XR + D, -D), (XR + D, FH - D), (XR, FH)]

# اسکی (روی رویه، کف y=SB)
SB = -4
ST_H = 14
X_TAIL, X_BEND, X_TIP = 28, -36, -78
def sk_bot(x):
    if x >= X_BEND: return SB
    t = (X_BEND - x) / (X_BEND - X_TIP); return SB - 19 * t * t
def sk_th(x):
    if x >= X_BEND: return ST_H
    t = (X_BEND - x) / (X_BEND - X_TIP); return ST_H - 4 * t
def ski_pts():
    xs = [X_TAIL - i * (X_TAIL - X_TIP) / 24 for i in range(25)]
    return [(x, sk_bot(x)) for x in xs] + [(x, sk_bot(x) - sk_th(x)) for x in xs][::-1]


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def sp(p, pts, fill, sw, clip=True):
    """چندضلعی با گوشهٔ تیز، دور سرمه‌ای؛ clip=True ⇒ نور/سایهٔ سکو روی آن می‌افتد."""
    q = p.X(pts); d = 'M' + 'L'.join('%.1f,%.1f' % z for z in q) + 'Z'
    p.o.append('<path d="%s" fill="%s" class="eo" stroke-width="%s"/>' % (d, fill, sw))
    if clip: p.clip.append(d)


GL_REST = 8
def strips(dx):
    out = []
    for x, w in ((0, 7), (12, 3)):
        a = XL + 12 + x + dx; y0, y1 = 5, FH - 5
        out.append([(a + .5 * (FH - y0) / 2, y0), (a + w + .5 * (FH - y0) / 2, y0), (a + w, y1), (a, y1)])
    return out


def build():
    p = Pen('ice_rink', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-12, FH + 2, 44); p.foot_tip(-12, FH, 30)
    # ۱) یخ
    sp(p, SIDE, ICE_S, PART); sp(p, FRONT, ICE_D, PART); sp(p, TOPF, ICE, PART)
    poly(p, [(XL + 6, 4.5), (XL + 6, 8), (XL + 30, 8), (XL + 30, 4.5)], ICE_L)                 # نور لبهٔ بالا-چپ
    for pts in (((-52, 5), (-45, 13), (-49, 20)), ((16, 5), (10, 12), (14, 19))):               # ترک‌های راست
        p.ln(pts[0], pts[1], 3, CRACK, j=0); p.ln(pts[1], pts[2], 3, CRACK, j=0)
    # ۲) درخشش (لایهٔ متحرک)
    with layer(p, 'glint'):
        for s in strips(GL_REST):
            poly(p, s, '#ffffff', .62)
    # ۳) پوتین (پشت اسکی)
    B = SB - ST_H - 5
    sp(p, [(-30, B), (2, B), (2, B - 38), (-14, B - 38), (-14, B - 22), (-22, B - 16), (-30, B - 12)], BT, PART, False)
    poly(p, [(-27, B - 3), (-27, B - 9), (-21, B - 13), (-17, B - 17), (-17, B - 3)], BT_L)
    poly(p, [(-3, B - 35), (0, B - 35), (0, B - 3), (-3, B - 3)], BT_D)
    poly(p, [(-11, B - 28), (-3, B - 28), (-3, B - 25), (-11, B - 25)], YEL)
    # ۴) اسکی + بست
    body = ski_pts()
    sp(p, body, RED, PART)
    poly(p, [(x, sk_bot(x) - sk_th(x) + 3.5) for x in (X_TAIL - 6, 0, -36, -58)] + [(x, sk_bot(x) - sk_th(x) + 6.8) for x in (-58, -36, 0, X_TAIL - 6)], RED_L)
    poly(p, [(X_TAIL - 6, SB - 5), (-30, SB - 5), (-30, SB - 1.8), (X_TAIL - 6, SB - 1.8)], RED_D)
    p.stroke(body, PART, j=.04, step=99)
    sp(p, [(-34, SB - ST_H - 1), (6, SB - ST_H - 1), (6, SB - ST_H - 6), (-34, SB - ST_H - 6)], YEL, INNER, False)
    poly(p, [(-30, SB - ST_H - 5), (2, SB - ST_H - 5), (2, SB - ST_H - 3), (-30, SB - ST_H - 3)], YEL_L)
    return p


if __name__ == '__main__':
    p = build()
    mo = {'glint': dict(offsets=[(-72 * XF[0], 0), (0, 0)])}
    r = finish(p, 'ice_rink', None, motion=mo, out=OUTD, shots=SHOTS)
    sp_ = r['spec']
    sp_['motion_spec'] = {'node_ice_rink_glint': dict(
        kind='دو نوار سفید مایل روی دیوارهٔ جلوی یخ؛ حالت ایستا = پایان حرکت (نوارها در راست)',
        translate_x_symbol_units=[-72, 0], translate_x_map_px=[round(-72 * K, 1), 0],
        opacity='از ۰ تا ۰٫۶۲ در ۱۵٪ اول؛ بعد ثابت',
        duration_s=1.8, easing='ease-in-out', loop=False, trigger='رسیدن کودک (یک‌بار)',
        how='گروه glint را از translateX(-72) به 0 ببر؛ نوارها از چپ به راست روی یخ می‌گذرند. تزئینی است (لغزش را F01/F09 نشان می‌دهند). بدون حلقهٔ بیکار.',
        note='با reduced-motion ثابت در وضع پایان.')}
    (OUTD / 'ice_rink.json').write_text(json.dumps(sp_, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
