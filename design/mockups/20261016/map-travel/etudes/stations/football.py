#!/usr/bin/env python3
"""ایستگاه F01 «زمین فوتبال» (سرزمین ورزشگاه، سکوی sports #7fbf4a) — بازطراحی دور ۵.
ایدهٔ یک‌نگاه: توپ فوتبال بزرگ و وسط، جلوی یک دروازهٔ پهن با تور. همه متقارن حول x=0 (مرکز سکو).
طرح قطعه‌به‌قطعه (واحد symbol؛ کف توپ y=+2، کف دروازه y=-12):
 ۱) تور: مستطیل پهن 112x92 (x ±56، y -104..-12) آبی-خاکستری روشن (#c4d6f2)، خط‌های لوزی تخت و نازک (#7f9bc8)، خط دور PART.
 ۲) دو تیرک سفید (۱۴ پهن، مرکز x=±56، y -108..-8) و تیرک افقی سفید (۱۴ بلند، y -111..-97، از x=-63 تا 63)، سه‌پله (سفید/آبی روشن/آبی-خاکستری)،
    در هم‌پوشانی با تیرک افقی هم‌رنگ؛ خط PART دور هر جزء.
 ۳) توپ (لایهٔ متحرک ball): دایرهٔ سفید r=44 مرکز (0,-42)، سایهٔ تیز هلالی پایین-راست (#c9d6ee)، پنج‌ضلعی مرکزی تیره (r=15، رأس بالا)،
    پنج خط درز از رأس‌ها، پنج لکهٔ نیمه‌پنهان کنار لبه (قرمز-بنفش تیره نه؛ همان تیرهٔ مرکزی)، خط دور PART؛ سایهٔ تماس زیر توپ.
قهرمان: سفید/آبی روشن + تیره روی سبز ⇒ کنتراست ارزشی؛ توپ ≈۴۸٪ عرض سکو، کل مجموعه ≈۶۸٪.
حرکت: فقط ball؛ از ۱۷ واحد (≈۱۲px) چپ می‌غلتد با چرخش و می‌ایستد؛ حالت ایستا = پایان؛ بدون بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8)
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/football'

POST_B, POST_L, POST_D = '#ffffff', '#e6efff', '#aebfdc'
NET_B, NET_L = '#b9cdee', '#7f9bc8'
BALL_B, BALL_D = '#ffffff', '#c9d6ee'
PATCH = '#34306e'
BR = 42; BCX, BCY = 0, -40
GX = 54; GT, GB = -104, -14
ROLL = 17


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def rect(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def pent(cx, cy, r, a0):
    return [(cx + r * math.cos(math.radians(a0 + 72 * i)), cy + r * math.sin(math.radians(a0 + 72 * i))) for i in range(5)]


def clipc(pts, R):
    out = []; dense = []
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        for k in range(10): dense.append((a[0] + (b[0] - a[0]) * k / 10, a[1] + (b[1] - a[1]) * k / 10))
    for x, y in dense:
        d = math.hypot(x - BCX, y - BCY)
        if d > R: x, y = BCX + (x - BCX) * R / d, BCY + (y - BCY) * R / d
        out.append((x, y))
    return out


def post(p, x0, y0, x1, y1):
    q = rect(x0, y0, x1, y1)
    p.shape(q, POST_B, PART, j=.1, step=8)
    w = x1 - x0
    poly(p, rect(x0 + 2.5, y0 + 4, x0 + 2.5 + w * .22, y1 - 4), POST_L)
    poly(p, rect(x1 - 2.5 - w * .26, y0 + 4, x1 - 2.5, y1 - 4), POST_D)
    p.stroke(q, PART, j=.1, step=8)


def build():
    p = Pen('football', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((-70, 14), (66, 8)), dot=(62, -22))
    p.xf = (1.0, 0.0, -1.0)
    p.tipshadow(0, GB + 2, 64); p.foot_tip(-GX, GB + 2, 10); p.foot_tip(GX, GB + 2, 10); p.foot_tip(0, 4, 20)
    # ۱) تور
    net = rect(-GX, GT + 4, GX, GB)
    p.shape(net, NET_B, PART, j=.1, step=8)
    for i in range(-5, 6):   # لوزی: دو دستهٔ مورب تخت
        x = i * 22.4
        for sg in (1, -1):
            a = (x - sg * 46, GB - 1); b = (x + sg * 46, GT + 5)
            # برش به مستطیل تور
            ts = []
            for xe in (-GX + 3, GX - 3):
                t = (xe - a[0]) / (b[0] - a[0]); y = a[1] + t * (b[1] - a[1])
                if GT + 5 <= y <= GB - 1: ts.append((xe, y))
            for ye in (GT + 5, GB - 1):
                t = (ye - a[1]) / (b[1] - a[1]); xx = a[0] + t * (b[0] - a[0])
                if -GX + 3 <= xx <= GX - 3: ts.append((xx, ye))
            ts = sorted(set((round(u, 2), round(v, 2)) for u, v in ts))
            if len(ts) >= 2: p.ln(ts[0], ts[-1], 2.0, NET_L, j=0)
    p.stroke(net, PART, j=.1, step=8)
    # ۲) تیرک‌ها
    post(p, -GX - 7, GT, -GX + 7, GB + 2)
    post(p, GX - 7, GT, GX + 7, GB + 2)
    post(p, -GX - 7, GT - 3, GX + 7, GT + 11)
    # ۳) توپ
    with layer(p, 'ball'):
        p.tipshadow(2, 3, 36)
        circ = ell(BCX, BCY, BR, BR, 0, 360, 48)
        p.shape(circ, BALL_B, PART, j=.06, step=99)
        phi = math.radians(40.6); dd = 18.4; h = math.degrees(math.acos(dd / (2 * BR)))
        S = (BCX - 14, BCY - 12)
        cres = [(BCX + BR * math.cos(math.radians(a)), BCY + BR * math.sin(math.radians(a))) for a in [math.degrees(phi) - h + 2 * h * i / 20 for i in range(21)]]
        cres += [(S[0] + BR * math.cos(math.radians(a)), S[1] + BR * math.sin(math.radians(a))) for a in [math.degrees(phi) + h - 2 * h * i / 20 for i in range(21)]]
        poly(p, cres, BALL_D)
        # لکه‌ها: پنج‌ضلعی مرکزی + پنج لکهٔ لبه
        C0 = pent(BCX, BCY, 15.5, -90)
        for i in range(5):
            a = math.radians(-90 + 72 * i); b = math.radians(-90 + 72 * i + 36)
            v = (BCX + 15.5 * math.cos(a), BCY + 15.5 * math.sin(a))
            e = (BCX + 33 * math.cos(a), BCY + 33 * math.sin(a))
            p.ln(v, e, INNER, NAVY, j=0)
            # لکهٔ لبه در زاویهٔ میانی
            oc = (BCX + 47 * math.cos(a), BCY + 47 * math.sin(a))
            q = clipc(pent(oc[0], oc[1], 16, math.degrees(a) + 180), BR - 1.2)
            poly(p, q, PATCH)
            # خط از انتهای درز تا لکهٔ لبه
            tip = (BCX + 30 * math.cos(a), BCY + 30 * math.sin(a))
            side = (BCX + 36 * math.cos(math.radians(math.degrees(a) + 36 * (1 if i % 2 else 1))), BCY + 36 * math.sin(math.radians(math.degrees(a) + 36)))
        poly(p, C0, PATCH)
        p.stroke(circ, PART, j=.06, step=99)
    return p


if __name__ == '__main__':
    p = build()
    r = finish(p, 'football', None, motion={'ball': dict(rotate=(BCX, BCY), offsets=[p.V((-ROLL, 0)), (0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_football_ball': dict(
        kind='توپ؛ حالت ایستا = پایان (کنار دروازه، وسط سکو)', translate_x_symbol_units=[-ROLL, 0], translate_x_map_px=[round(-ROLL * K, 1), 0],
        rotate_deg=[-(ROLL / (2 * math.pi * BR) * 360), 0], pivot_symbol=[BCX, BCY], duration_s=1.6, easing='ease-out (کندشونده)', loop=False,
        trigger='رسیدن کودک (یک‌بار)', reduced_motion='ایستا', note='دروازه و تور ثابت؛ سایهٔ تماس با توپ می‌رود؛ بدون عامل هل و بدون خط حرکت؛ بدون حلقهٔ بیکار.')}
    (OUTD / 'football.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
