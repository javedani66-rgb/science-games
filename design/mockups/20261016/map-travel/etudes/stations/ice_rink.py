#!/usr/bin/env python3
"""ایستگاه F06 «پیست اسکی روی یخ» (سرزمین ورزشگاه، سکوی sports #7fbf4a، رنگ‌مایهٔ ۹۳°) — بازطراحی سوم (ساده).
طرح (مختصات symbol، مرکز سکو (0,0)؛ ۱ واحد ≈ ۰٫۷۲px):
 ۱) تختهٔ یخ نازک و تخت (نمای سه‌چهارم): رویه #e3f6fc، جلو #9dd2ea، راست #6aa9cf (رنگ‌مایهٔ ≈۱۹۵°)؛ خط دور PART؛ بدون ترک و بدون هیچ شکل اضافه.
 ۲) node_ice_rink_glint: همان دو نوار سفید مایل قبلی؛ حالت ایستا = پایان (راست).
 ۳) دو اسکی خوابیدهٔ موازی، ۱۱ پهن، ۵۸ بلند، قرمز یکدست #e0553a (روشن #ff9a6c، تیره #9c2f1c)، نوک چپ گرد و بالاآمده (منحنی)،
    بست زرد روشن تخت روی هر کدام؛ سایهٔ تیز زیر نوک و زیر بدنه. بدون چوب‌دستی."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
_k.margin_check = functools.partial(_k.margin_check, min_margin=8.5); _k.motion_check = functools.partial(_k.motion_check, min_margin=8.5)
_k.inside_check = functools.partial(_k.inside_check, min_margin=8.5)
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/ice_rink'

ICE, ICE_D, ICE_S = '#e3f6fc', '#9dd2ea', '#6aa9cf'
RED, RED_L, RED_D = '#e0553a', '#ff9a6c', '#9c2f1c'
YEL, YEL_L, YEL_D = '#ffd84d', '#fff0a0', '#d9961c'
XF = (0.84, 3.0, -12.0)

XL, XR, YT, YB, TH, SKW = -58, 26, -38, 28, 8, 8
def sh(y): return SKW * (YB - y) / (YB - YT)
TOPF = [(XL + SKW, YT), (XR + SKW, YT), (XR, YB), (XL, YB)]
FRONT = [(XL, YB), (XR, YB), (XR, YB + TH), (XL, YB + TH)]
SIDE = [(XR + SKW, YT), (XR + SKW, YT + TH), (XR, YB + TH), (XR, YB)]
SKIS = (-11, 11)
SX0, SX1, SW = -42, 16, 11


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def sp(p, pts, fill, sw, clip=True):
    q = p.X(pts); d = 'M' + 'L'.join('%.1f,%.1f' % z for z in q) + 'Z'
    p.o.append('<path d="%s" fill="%s" class="eo" stroke-width="%s"/>' % (d, fill, sw))
    if clip: p.clip.append(d)


def ski_pts(c):
    h = SW / 2; x0, x1 = SX0, SX1
    top = [(x0, c - h - 9), (x0 + 4, c - h - 5), (x0 + 10, c - h - 1.5), (x0 + 18, c - h), (x1 - 3, c - h), (x1, c - h + 3)]
    bot = [(x1, c + h - 3), (x1 - 3, c + h), (x0 + 24, c + h), (x0 + 16, c + h - 1.5), (x0 + 10, c + h - 5), (x0 + 6, c + h - 9.5), (x0 + 3, c - h - 4.5)]
    return top + bot


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
    sp(p, SIDE, ICE_S, PART); sp(p, FRONT, ICE_D, PART); sp(p, TOPF, ICE, PART)
    with layer(p, 'glint'):
        for s_ in strips(GL_REST):
            poly(p, s_, '#ffffff', .62)
    q = p.X(TOPF); p.o.append('<path d="M%s" fill="none" class="eo" stroke-width="%s"/>' % ('L'.join('%.1f,%.1f' % z for z in q) + 'Z', PART))
    for c in SKIS:
        h = SW / 2
        poly(p, [(SX0 + 6, c + h - 3), (SX0 + 24, c + h + 4), (SX1, c + h + 4), (SX1, c + h - 1), (SX0 + 24, c + h - 1)], ICE_S, .9)   # سایهٔ زیر اسکی و نوک
        sp(p, ski_pts(c), RED, INNER)
        poly(p, [(SX0 + 26, c - 2.9), (SX1 - 5, c - 2.9), (SX1 - 5, c - 1.5), (SX0 + 26, c - 1.5)], RED_L)
        poly(p, [(SX0 + 26, c + 1.6), (SX1 - 5, c + 1.6), (SX1 - 5, c + 2.9), (SX0 + 26, c + 2.9)], RED_D)
        poly(p, [(-26, c - 2.4), (-12, c - 2.4), (-12, c + 2.4), (-26, c + 2.4)], YEL)            # بست روشن تخت
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
        how='گروه glint را از translateX(%d)' % (GL_START - GL_REST) + ' به 0 ببر؛ نوارها از چپ به راست روی یخ می‌گذرند. تزئینی است. بدون حلقهٔ بیکار.',
        note='با reduced-motion ثابت در وضع پایان.')}
    (OUTD / 'ice_rink.json').write_text(json.dumps(sp_, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
