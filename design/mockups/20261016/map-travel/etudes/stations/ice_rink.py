#!/usr/bin/env python3
"""ایستگاه F06 «پیست اسکی روی یخ» (سرزمین ورزشگاه، سکوی sports #7fbf4a، رنگ‌مایهٔ ۹۳°) — بازطراحی سوم (ساده).
طرح (مختصات symbol، مرکز سکو (0,0)؛ ۱ واحد ≈ ۰٫۷۲px):
 ۱) تختهٔ یخ نازک و تخت (نمای سه‌چهارم): رویه #e3f6fc، جلو #9dd2ea، راست #6aa9cf (رنگ‌مایهٔ ≈۱۹۵°)؛ خط دور PART؛ بدون ترک و بدون هیچ شکل اضافه.
 ۲) node_ice_rink_glint: همان دو نوار سفید مایل قبلی؛ حالت ایستا = پایان (راست).
 ۳) دو اسکی خوابیدهٔ موازی، ۱۱ پهن، ۵۸ بلند، قرمز یکدست #e0553a (روشن #ff9a6c، تیره #9c2f1c)، نوک چپ گرد و بالاآمده (منحنی)،
    بست زرد روشن تخت روی هر کدام؛ سایهٔ تیز زیر نوک و زیر بدنه. بدون چوب‌دستی."""
"""ایستگاه F06 «پیست اسکیت روی یخ» (سرزمین ورزشگاه، سکوی sports #7fbf4a، رنگ‌مایهٔ ۹۳°) — بازطراحی چهارم (دستور مدیر هنری R5).
طرح (واحد symbol؛ مرکز سکو (0,0)):
 ۱) یخ‌پیست بیضی روشن: بیضی ۶۲×۲۷ (≈۶۷٪ پهنای سکو)، مرکز (0,-4)؛ دیوارهٔ نقره‌ای تیره ۷ واحد (#a9bccd)، لبهٔ سفید-نقره‌ای (#eef3f8)، رویهٔ یخ آبی روشن (#c9efff) با خط INNER.
 ۲) لایهٔ glint: دو نوار سفید مایل کوتاه روی یخ (بالا-راست)، فقط محو‌شدن/لغزش ۱۰ واحدی؛ حالت ایستا = پایان.
 ۳) دو اسکیت یکسان (کفش نارنجی #f0782a + ساق/کفی کرم + تیغهٔ نقره‌ای با دو پایه و دماغهٔ خمیده) رو به راست، یکی عقب‌تر و یکی جلوتر؛ سایهٔ تیز آبی روی یخ.
 رنگ‌مایه: کفش ≈۲۴°، یخ ≈۱۹۵°، سکو ≈۹۳° (≥۳۵° فاصله)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
from shapely.geometry import Polygon, box as sbox
from shapely.ops import unary_union
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/ice_rink'

RIM, WALL, ICE, ICE_S = '#ffffff', '#a9bccd', '#d4f1ff', '#9fd0ea'
O_B, O_L, O_D = '#f0782a', '#ffae6a', '#b4501a'
CRM = '#fff3d0'
M_B, M_L, M_D = '#dfe6ee', '#ffffff', '#8c9bb0'
CX, CY, RX, RY, WH = 0, -8, 62, 29, 8
GL = 10


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def rect(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def skate(p, ox, oy, k=1.0):
    """اسکیت رو به راست؛ (ox,oy) = پاشنهٔ کف تیغه روی یخ؛ k مقیاس."""
    T = lambda pts: [(ox + x * k, oy + y * k) for x, y in pts]
    poly(p, T([(2, 5), (46, 5), (48, 11), (4, 11)]), ICE_S, .9)                  # سایهٔ تیز روی یخ
    blade = unary_union([Polygon([(-5, 0), (40, 0), (50, -7), (54, -3), (46, 7), (-5, 7)]), Polygon(rect(5, -13, 13, 2)), Polygon(rect(32, -13, 40, 2))])
    bl = T(list(blade.exterior.coords)[:-1])
    p.shape(bl, M_B, INNER, j=0, step=5, clip=False)
    poly(p, T(rect(-2, 1.6, 36, 3.6)), M_L)
    boot = T([(0, -10), (0, -50), (19, -50), (21, -30), (38, -28), (47, -21), (46, -10)])
    p.shape(boot, O_B, PART, j=0, step=5, clip=False)
    poly(p, T(rect(3.5, -45, 8, -14)), O_L)
    poly(p, T([(14, -31), (17, -31), (17, -14), (14, -14)]), O_D)
    poly(p, T([(24, -17), (42, -17), (42, -14), (24, -14)]), O_D)
    poly(p, T(rect(2.5, -50 + 3, 16.5, -50 + 9)), CRM)             # کاف کرم
    poly(p, T([(2.5, -15.2), (43.5, -15.2), (43.5, -12.4), (2.5, -12.4)]), CRM)
    p.stroke(boot, PART, j=0, step=5)


def build(out=OUTD):
    p = Pen('ice_rink', 'sports'); pad(p, line=((-52, 40), (-36, 43)), tri=((74, -20), (70, 18)), dot=(-70, -14))
    top = ell(CX, CY, RX, RY, 180, 360, 24); bot = ell(CX, CY + WH, RX, RY, 0, 180, 24)
    p.tipshadow(CX, CY + WH + 2, 58)
    p.foot_tip(CX, CY + WH, 52)
    p.shape(top + bot, WALL, PART, j=.1, step=10)
    p.shape(ell(CX, CY, RX, RY, 0, 360, 48), ICE, PART, j=.1, step=10, clip=False)
    poly(p, ell(CX, CY, RX - 6, RY - 5, 195, 285, 14) + ell(CX, CY, RX - 13, RY - 11, 285, 195, 14), RIM)
    poly(p, ell(CX, CY, RX - 6, RY - 5, 20, 100, 14) + ell(CX, CY, RX - 13, RY - 11, 100, 20, 14), ICE_S, .7)
    with layer(p, 'glint'):
        poly(p, [(34, -22), (41, -22), (32, -13), (25, -13)], '#ffffff', .85)
        poly(p, [(44, -22), (48, -22), (39, -13), (35, -13)], '#ffffff', .85)
    skate(p, -42, -8, 0.82)
    skate(p, 2, 6, 0.82)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    mo = {'glint': dict(offsets=[(-GL, 0), (0, 0)])}
    r = finish(p, 'ice_rink', STAND, motion=mo, out=OUTD, shots=SHOTS)
    sp_ = r['spec']
    sp_['motion_spec'] = {'node_ice_rink_glint': dict(
        kind='دو نوار سفید مایل کوتاه روی یخ؛ حالت ایستا = پایان حرکت',
        translate_x_symbol_units=[-GL, 0], translate_x_map_px=[round(-GL * K, 1), 0],
        opacity='از ۰ تا ۰٫۷۵ در ۲۰٪ اول؛ بعد ثابت', duration_s=1.4, easing='ease-out', loop=False, trigger='رسیدن کودک (یک‌بار)',
        how='گروه glint را از translateX(%d) و شفافیت ۰ به 0 و ۱ ببر. تزئینی است. بدون حلقهٔ بیکار.', note='با reduced-motion ثابت در وضع پایان.')}
    (OUTD / 'ice_rink.json').write_text(json.dumps(sp_, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
