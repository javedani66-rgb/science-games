#!/usr/bin/env python3
"""ایستگاه F06 «پیست اسکی روی یخ» (سرزمین ورزشگاه، سکوی sports #7fbf4a، رنگ‌مایهٔ ۹۳°).
طرح قطعه‌به‌قطعه (مختصات symbol، مرکز سکو (0,0)؛ ۱ واحد ≈ ۰٫۷۲px):
 ۱) تختهٔ یخ (بلوک سه‌چهارم): رویه (متوازی‌الاضلاع) #bfe9f7، دیوارهٔ جلو #7fc0dc (تیره)، دیوارهٔ چپ #9fd3ea؛ رنگ‌مایه ۱۹۰° (۹۷° از سکو).
    خط دور PART، نوار نور تخت، دو ترک راست (خط تخت) روی دیوارهٔ جلو.
 ۲) لایهٔ متحرک node_ice_rink_glint: دو نوار سفید مایل (۷ و ۳ واحد) روی رویهٔ یخ، پشت اسکی و قطب (تزئینی). حالت ایستا = پایان (نوار در راست رویه).
 ۳) اسکی بلند و باریک (۱۵ واحد ضخامت، خط PART): قرمز مرجانی #e0553a/#ff9a6c/#9c2f1c، نوک چپ خمیده به بالا؛ همان قرمز بدنهٔ جرثقیل؛ رنگ‌مایه ۱۰° (۸۳° از سکو).
 ۴) بستِ زرد روی اسکی (بلوک ۲۴×۱۲، خط INNER) + نوار تیره.
 ۵) عصای اسکی: میلهٔ فلزی #dbe9f8/#a3bbd9 (۱۳ پهن، خط INNER)، دستگیرهٔ چوبی بالا، حلقهٔ قرمز نزدیک پایین؛ ایستاده روی یخ پشت اسکی (فقط برای نام‌پذیری «اسکی»).
 فقط خط‌های ۷٫۶/۵٫۸/۳٫۹. بدون چرخ (فرق با F09)، شفاف نیست (فرق با E06)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8)
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/ice_rink'

ICE, ICE_L, ICE_D, ICE_S, CRACK = '#bfe9f7', '#effbff', '#7fc0dc', '#9fd3ea', '#5f9fc0'
RED, RED_L, RED_D = '#e0553a', '#ff9a6c', '#9c2f1c'
YEL, YEL_L, YEL_D = '#ffd84d', '#fff0a0', '#d9961c'
ST, ST_S, ST_L = '#dbe9f8', '#a3bbd9', '#ffffff'
WOOD, WOOD_L, WOOD_D = '#b77a3a', '#d9a463', '#7a4a1f'
XF = (1.0, -6.0, 0.0)

# تختهٔ یخ
T0, T1, Y0, Y1, SK = -68, 22, -22, 10, 18   # لبهٔ چپ/راست رویه در بالا، y بالا/پایین رویه، کجی (۱۸ واحد روی ۳۲)
TH = 14                                      # ضخامت دیواره
def ex(x, y): return x + SK * (y - Y0) / (Y1 - Y0)   # x لبهٔ مایل در ارتفاع y (با مبدأ لبه)
TOPF = [(T0, Y0), (T1, Y0), (T1 + SK, Y1), (T0 + SK, Y1)]
FRONT = [(T0 + SK, Y1), (T1 + SK, Y1), (T1 + SK, Y1 + TH), (T0 + SK, Y1 + TH)]
SIDE = [(T0, Y0), (T0 + SK, Y1), (T0 + SK, Y1 + TH), (T0, Y0 + TH)]

# اسکی
SB = 2          # کف اسکی
ST_H = 15       # ضخامت
X_TAIL, X_BEND, X_TIP = 4, -30, -60
def sk_bot(x):
    if x >= X_BEND: return SB
    t = (X_BEND - x) / (X_BEND - X_TIP); return SB - 19 * t * t
def sk_th(x):
    if x >= X_BEND: return ST_H
    t = (X_BEND - x) / (X_BEND - X_TIP); return ST_H - 4 * t
def ski_pts():
    xs = [X_TAIL - i * (X_TAIL - X_TIP) / 24 for i in range(25)]
    bot = [(x, sk_bot(x)) for x in xs]; top = [(x, sk_bot(x) - sk_th(x)) for x in xs]
    return bot + top[::-1]

PX = 20      # محور عصا


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def mpoly(p, pts, fill, sw):
    q = p.X(pts); d = 'M' + 'L'.join('%.1f,%.1f' % z for z in q) + 'Z'
    p.o.append('<path d="%s" fill="%s" class="eo" stroke-width="%s" stroke-linejoin="miter" stroke-miterlimit="6"/>' % (d, fill or 'none', sw))


def sp(p, pts, fill, sw, clip=True):
    """چندضلعی با گوشهٔ تیز (بدون گردشدن مسیر)، دور سرمه‌ای با اتصال گرد؛ clip=True ⇒ نور/سایهٔ سکو روی آن می‌افتد."""
    q = p.X(pts); d = 'M' + 'L'.join('%.1f,%.1f' % z for z in q) + 'Z'
    p.o.append('<path d="%s" fill="%s" class="eo" stroke-width="%s"/>' % (d, fill, sw))
    if clip: p.clip.append(d)


def strips(dx):
    out = []
    for x, w in ((0, 7), (11, 3)):
        a = T0 + 12 + x + dx; y0, y1 = Y0 + 4, Y1 - 3
        k = SK / (Y1 - Y0)
        out.append([(a + k * (y0 - Y0), y0), (a + w + k * (y0 - Y0), y0), (a + w + k * (y1 - Y0), y1), (a + k * (y1 - Y0), y1)])
    return out


GL_REST = 60      # حالت پایان: نوارها نزدیک راست رویه
def build():
    p = Pen('ice_rink', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-14, Y1 + TH + 3, 46); p.foot_tip(-12, Y1 + TH + 2, 34)
    # ۱) یخ: دیواره‌ها
    sp(p, SIDE, ICE_S, PART)
    sp(p, FRONT, ICE_D, PART)
    sp(p, TOPF, ICE, PART)
    # نور لبهٔ بالا-چپ رویه و ترک‌های راست روی دیواره
    poly(p, [(T0 + 7, Y0 + 5), (T0 + 10.5, Y0 + 5), (T0 + SK - 1 + 7, Y1 - 5), (T0 + SK - 1 + 3.5, Y1 - 5)], ICE_L)
    for (a, b) in (((-34, Y1 + 1), (-26, Y1 + 11)), ((16, Y1 + 1), (9, Y1 + 12))):
        p.ln(a, b, 3, CRACK, j=0)
    # ۲) درخشش (لایهٔ متحرک): پشت اسکی و عصا
    with layer(p, 'glint'):
        for s in strips(GL_REST):
            poly(p, s, '#ffffff', .62)
    p.stroke(TOPF, PART, j=.1, step=99)
    # سایهٔ تماس اسکی روی یخ (چندضلعی تیز، داخل رویه)
    poly(p, [(-52, SB + 1), (X_TAIL + 2, SB + 1), (X_TAIL - 1, SB + 5), (-50, SB + 5)], ICE_D, .9)
    # ۳) عصا (پشت اسکی)
    sy0, sy1 = -2, -80
    p.ln((PX + 4, sy0 + 2), (PX + 14, sy0 + 2), 4, ICE_D, op=.9, j=0)
    sp(p, [(PX - 6.5, sy0), (PX + 6.5, sy0), (PX + 6.5, sy1), (PX - 6.5, sy1)], ST, INNER)
    poly(p, [(PX + 1.5, sy1 + 4), (PX + 5.5, sy1 + 4), (PX + 5.5, sy0 - 1.5), (PX + 1.5, sy0 - 1.5)], ST_S)
    poly(p, [(PX - 4.2, sy1 + 22), (PX - 2.2, sy1 + 22), (PX - 2.2, sy0 - 12), (PX - 4.2, sy0 - 12)], ST_L)
    sp(p, [(PX - 8, sy1 - 10), (PX + 8, sy1 - 10), (PX + 8, sy1 + 18), (PX - 8, sy1 + 18)], WOOD, PART)
    poly(p, [(PX + 2, sy1 - 8), (PX + 5.5, sy1 - 8), (PX + 5.5, sy1 + 16), (PX + 2, sy1 + 16)], WOOD_D)
    poly(p, [(PX - 5.5, sy1 - 7), (PX - 3, sy1 - 7), (PX - 3, sy1 + 15), (PX - 5.5, sy1 + 15)], WOOD_L)
    sp(p, ell(PX, -17, 13, 5, 0, 360, 20), RED, INNER)
    poly(p, [(PX - 8, -17.5), (PX - 3, -19), (PX - 3, -17), (PX - 8, -15.8)], RED_L)
    # ۴) اسکی
    body = ski_pts()
    sp(p, body, RED, PART)
    poly(p, [(x, sk_bot(x) - sk_th(x) + 3.5) for x in (X_TAIL - 6, -10, -30, -50)] + [(x, sk_bot(x) - sk_th(x) + 6.8) for x in (-50, -30, -10, X_TAIL - 6)], RED_L)
    poly(p, [(X_TAIL - 6, SB - 5), (-28, SB - 5), (-28, SB - 1.8), (X_TAIL - 6, SB - 1.8)], RED_D)
    p.stroke(body, PART, j=.04, step=99)
    # بست زرد روی اسکی
    BX0, BX1, BY = -26, -2, SB - ST_H
    mpoly(p, [(BX0, BY + 1), (BX1, BY + 1), (BX1 - 3, BY - 12), (BX0 + 3, BY - 12)], YEL, INNER)
    poly(p, [(BX0 + 7, BY - 8), (BX1 - 6, BY - 8), (BX1 - 6, BY - 5.5), (BX0 + 7, BY - 5.5)], YEL_D)
    poly(p, [(BX0 + 6, BY - 3), (BX0 + 10, BY - 3), (BX0 + 10, BY - 1), (BX0 + 6, BY - 1)], YEL_L)
    return p


if __name__ == '__main__':
    p = build()
    mo = {'glint': dict(offsets=[p.V((-GL_REST - 0, 0)) if False else (-76 * XF[0], 0), (0, 0)])}
    r = finish(p, 'ice_rink', None, motion=mo, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_ice_rink_glint': dict(
        kind='دو نوار سفید مایل روی رویهٔ یخ (پشت اسکی و عصا)؛ حالت ایستا = پایان حرکت (نوارها در راست رویه)',
        translate_x_symbol_units=[-76, 0], translate_x_map_px=[round(-76 * K, 1), 0],
        opacity='۰ تا ۰٫۶۲ در ۱۵٪ اول و ۰٫۶۲ تا ۰٫۶۲ ثابت؛ در پایان ثابت می‌ماند',
        duration_s=1.8, easing='ease-in-out', loop=False, trigger='رسیدن کودک (یک‌بار)',
        how='گروه glint را از translateX(-76) به 0 ببر؛ نوارها از چپ به راست روی یخ می‌گذرند. حرکت تزئینی است (حرکت لغزش را F01/F09 نشان می‌دهند). بدون حلقهٔ بیکار.',
        note='با reduced-motion ثابت در وضع پایان.')}
    (OUTD / 'ice_rink.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
