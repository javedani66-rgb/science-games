#!/usr/bin/env python3
"""ایستگاه F06 «پیست اسکی روی یخ» (سرزمین ورزشگاه، سکوی sports #7fbf4a، رنگ‌مایهٔ ۹۳°) — بازطراحی دوم.
طرح (مختصات symbol، مرکز سکو (0,0)؛ ۱ واحد ≈ ۰٫۷۲px):
 ۱) سطح یخ صاف و عریض (متوازی‌الاضلاع کم‌عمق + لبهٔ جلوی نازک ۸ + لبهٔ راست): رویه #d9f2fb، جلو #a6d9ee، راست #82bcd8 (رنگ‌مایه ۱۹۰°، ΔE پله‌ها ≈ ۱۵–۲۰).
    خط دور PART؛ دو ترک راست و بلند (خط تخت ۳٫۹ = INNER) زیر اسکی‌ها.
 ۲) node_ice_rink_glint: دو نوار سفید مایل روی رویه (پشت ترک/اسکی)؛ حالت ایستا = پایان (راست).
 ۳) دو اسکی موازی خوابیده (عرض ۱۳، خط PART) قرمز #e0553a/#ff9a6c/#9c2f1c، نوک سمت چپ باریک و بالا‌آمده (سایهٔ زیر نوک + نور روشن)؛ بست زرد تخت روی هر کدام.
 ۴) دو چوب‌دستی ضربدری پشت اسکی‌ها، سمت راست: فلز #dbe9f8/#a3bbd9 (۹ پهن، INNER)، دستگیرهٔ چوبی، حلقهٔ قرمز.
 هیچ لوزی/نقطهٔ بی‌معنا؛ هیچ اسکی با لبهٔ یخ مماس نیست (فاصله ≥ ۸)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8)
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/ice_rink'

ICE, ICE_L, ICE_D, ICE_S, CRACK = '#d9f2fb', '#ffffff', '#a6d9ee', '#82bcd8', '#6aa6c6'
RED, RED_L, RED_D = '#e0553a', '#ff9a6c', '#9c2f1c'
YEL, YEL_L, YEL_D = '#ffd84d', '#fff0a0', '#d9961c'
ST, ST_S, ST_L = '#dbe9f8', '#a3bbd9', '#ffffff'
WOOD, WOOD_L, WOOD_D = '#b77a3a', '#d9a463', '#7a4a1f'
XF = (1.0, -8.0, -22.0)

# سطح یخ: رویه y∈[YT,YB]، لبهٔ بالا به راست کج (SKW)
XL, XR, YT, YB, TH, SKW = -62, 28, -34, 24, 8, 8
def sh(y): return SKW * (YB - y) / (YB - YT)
TOPF = [(XL + SKW, YT), (XR + SKW, YT), (XR, YB), (XL, YB)]
FRONT = [(XL, YB), (XR, YB), (XR, YB + TH), (XL, YB + TH)]
SIDE = [(XR + SKW, YT), (XR + SKW, YT + TH), (XR, YB + TH), (XR, YB)]
SKIS = (-13, 9)          # محور y دو اسکی
SX0, SX1, SW = -50, 16, 14   # نوک و دم اسکی، عرض


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def sp(p, pts, fill, sw, clip=True):
    """چندضلعی با گوشهٔ تیز، دور سرمه‌ای؛ clip=True ⇒ نور/سایهٔ سکو روی آن می‌افتد."""
    q = p.X(pts); d = 'M' + 'L'.join('%.1f,%.1f' % z for z in q) + 'Z'
    p.o.append('<path d="%s" fill="%s" class="eo" stroke-width="%s"/>' % (d, fill, sw))
    if clip: p.clip.append(d)


def ski_pts(c, x0=SX0, x1=SX1, w=SW):
    h = w / 2
    return [(x0, c - 1.5), (x0 + 5, c - 4.5), (x0 + 22, c - h), (x1 - 3, c - h), (x1, c - h + 3), (x1, c + h - 3), (x1 - 3, c + h), (x0 + 22, c + h), (x0 + 5, c + 4.5), (x0, c + 1.5)]


def pole(p, b, t, w=9):
    dx, dy = t[0] - b[0], t[1] - b[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux; h = w / 2
    P = lambda s, o: (b[0] + ux * s + nx * o, b[1] + uy * s + ny * o)
    sp(p, [P(0, -h), P(0, h), P(L, h), P(L, -h)], ST, INNER, False)
    poly(p, [P(6, h - 4.5), P(6, h - 1.5), P(L - 4, h - 1.5), P(L - 4, h - 4.5)], ST_S)
    poly(p, [P(6, -h + 1.5), P(6, -h + 3.2), P(L - 14, -h + 3.2), P(L - 14, -h + 1.5)], ST_L)
    # دستگیره (چوب)
    sp(p, [P(L - 24, -5.5), P(L - 24, 5.5), P(L + 4, 5.5), P(L + 4, -5.5)], WOOD, PART, False)
    poly(p, [P(L - 20, -3.5), P(L - 20, -1.2), P(L, -1.2), P(L, -3.5)], WOOD_L)
    poly(p, [P(L - 20, 2), P(L - 20, 3.6), P(L, 3.6), P(L, 2)], WOOD_D)
    # حلقهٔ قرمز نزدیک پایین
    sp(p, [P(13, -8), P(13, 8), P(20, 8), P(20, -8)], RED, INNER, False)


GL_REST = 8
GL_START = -60
def strips(dx):
    out = []
    for x, w in ((0, 7), (8, 3)):
        a = x + dx; y0, y1 = YT + 5, YB - 5
        out.append([(a + sh(y0), y0), (a + w + sh(y0), y0), (a + w + sh(y1), y1), (a + sh(y1), y1)])
    return out


def build():
    p = Pen('ice_rink', 'sports'); pad(p, line=((-52, 40), (-36, 43)), tri=((62, -22), (66, 12)), dot=(62, 26))
    p.xf = XF
    p.tipshadow(-10, YB + TH + 2, 44); p.foot_tip(-10, YB + TH - 1, 30)
    # ۱) یخ
    sp(p, SIDE, ICE_S, PART); sp(p, FRONT, ICE_D, PART); sp(p, TOPF, ICE, PART)
    # ترک‌های راست و بلند (INNER) زیر اسکی‌ها
    p.ln((-22, YT + 6), (12, YB - 5), INNER, CRACK, j=0)
    p.ln((24, YT + 6), (22, YB - 6), INNER, CRACK, j=0)
    # ۲) درخشش (لایهٔ متحرک)
    with layer(p, 'glint'):
        for s_ in strips(GL_REST):
            poly(p, s_, '#ffffff', .62)
    q = p.X(TOPF); p.o.append('<path d="M%s" fill="none" class="eo" stroke-width="%s"/>' % ('L'.join('%.1f,%.1f' % z for z in q) + 'Z', PART))
    # ۳) چوب‌دستی‌های ضربدری (پشت اسکی)
    for b, t in (((4, -27), (12, -92)), ((26, -27), (34, -92))):
        poly(p, [(b[0] - 7, b[1] + 1), (b[0] + 8, b[1] + 1), (b[0] + 8, b[1] + 4.5), (b[0] - 7, b[1] + 4.5)], ICE_D, .9)
        pole(p, b, t)
    # ۴) اسکی‌ها
    for c in SKIS:
        sx = sh(c)
        body = [(x + sx * 0, y) for x, y in ski_pts(c)]
        poly(p, [(SX0 + 2, c + 4), (SX0 + 24, c + SW / 2 + 3), (SX0 + 24, c + SW / 2 + .5), (SX0 + 8, c + 4)], ICE_D, .9)   # سایه زیر نوک بالا‌آمده
        sp(p, body, RED, INNER)
        poly(p, [(SX0 + 6, c - 2.5), (SX0 + 24, c - 4.2), (SX1 - 5, c - 4.2), (SX1 - 5, c - 2.4), (SX0 + 24, c - 2.4), (SX0 + 8, c - .5)], RED_L)
        poly(p, [(SX0 + 26, c + 2.2), (SX1 - 4, c + 2.2), (SX1 - 4, c + 4), (SX0 + 26, c + 4)], RED_D)
        poly(p, [(-30, c - 3.8), (-14, c - 3.8), (-14, c + 3.8), (-30, c + 3.8)], YEL)            # بست زرد (تخت)
        poly(p, [(-28, c - 2.8), (-16, c - 2.8), (-16, c - 1.5), (-28, c - 1.5)], YEL_L)
        poly(p, [(-28, c + 1.6), (-16, c + 1.6), (-16, c + 2.8), (-28, c + 2.8)], YEL_D)
    return p


if __name__ == '__main__':
    p = build()
    mo = {'glint': dict(offsets=[(GL_START - GL_REST, 0), (0, 0)])}
    r = finish(p, 'ice_rink', None, motion=mo, out=OUTD, shots=SHOTS)
    sp_ = r['spec']
    sp_['motion_spec'] = {'node_ice_rink_glint': dict(
        kind='دو نوار سفید مایل روی رویهٔ یخ؛ حالت ایستا = پایان حرکت (نوارها در راست)',
        translate_x_symbol_units=[GL_START - GL_REST, 0], translate_x_map_px=[round((GL_START - GL_REST) * K, 1), 0],
        opacity='از ۰ تا ۰٫۶۲ در ۱۵٪ اول؛ بعد ثابت',
        duration_s=1.8, easing='ease-in-out', loop=False, trigger='رسیدن کودک (یک‌بار)',
        how='گروه glint را از translateX(%d)' % (GL_START - GL_REST) + ' به 0 ببر؛ نوارها از چپ به راست روی یخ می‌گذرند. تزئینی است (لغزش را F01/F09 نشان می‌دهند). بدون حلقهٔ بیکار.',
        note='با reduced-motion ثابت در وضع پایان.')}
    (OUTD / 'ice_rink.json').write_text(json.dumps(sp_, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
