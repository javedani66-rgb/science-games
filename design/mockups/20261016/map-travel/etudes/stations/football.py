#!/usr/bin/env python3
"""ایستگاه F01 «زمین فوتبال» — بازطراحی دور ۶ (همسطح پیچ‌کاری).
ایده: دروازهٔ ¾ (چارچوب جلو + چارچوب پشتِ بالا-راست‌تر، تور سقف/کنار/پشت در سه پلهٔ آبی) و توپ بزرگ جلوی آن.
واحد symbol؛ کف دروازه y=-6، سقف جلو y=-98؛ عمق (+20,-16).
 اجزای درشت: ۱) تور سه‌وجهی ۲) دو تیرک جلو + تیرافقی (سفید/آبی روشن/آبی-خاکستری) ۳) چارچوب پشت (باریک‌تر) ۴) توپ r=44 (سفید/خاکستری/تیره) + سایهٔ تماس.
 عرض کل ≈۷۰٪ سکو؛ توپ نیمی از ارتفاع. حرکت: فقط ball؛ ایستا=پایان؛ بدون بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8)
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/football'
POST_B, POST_L, POST_D = '#ffffff', '#e6efff', '#a9bbdc'
NET_BK, NET_SD, NET_RF, NET_L = '#9fb9e2', '#bcd0ee', '#dce8fa', '#6f8dc0'
BALL_B, BALL_D, BALL_DD = '#ffffff', '#d3ddf0', '#a7b5d6'
PATCH = '#2b2766'
BR = 37; BCX, BCY = -14, -29
FX0, FX1 = -62, 46; FT, FB = -104, -8      # چارچوب جلو
DX, DY = 18, -17                          # عمق
ROLL = 17
def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, (' stroke="%s" stroke-width=".6" stroke-linejoin="round"' % col) if op == 1 else ' opacity="%s"' % op))   # حاشیهٔ هم‌رنگ: درز مویی بین چندضلعی‌ها نماند


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


def post(p, x0, y0, x1, y1):  # سه‌پله
    q = rect(x0, y0, x1, y1)
    p.shape(q, POST_B, PART, j=.1, step=8)
    w = x1 - x0
    poly(p, rect(x0 + 2.5, y0 + 4, x0 + 2.5 + w * .22, y1 - 4), POST_L)
    poly(p, rect(x1 - 2.5 - w * .26, y0 + 4, x1 - 2.5, y1 - 4), POST_D)
    p.stroke(q, PART, j=.1, step=8)


def build():
    p = Pen('football', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((-74, 14), (70, 8)), dot=(64, -22))
    p.xf = (1.0, 0.0, 0.0)
    p.tipshadow(0, FB + 8, 62); p.foot_tip(FX0, FB + 2, 10);  p.foot_tip(0, 8, 20)
    bx0, bx1, bt, bb = FX0 + DX, FX1 + DX, FT + DY, FB + DY
    # ۱) تور: پشت، کنار راست، سقف
    lside = [(FX0, FT), (bx0, bt), (bx0, bb), (FX0, FB)]
    p.shape(lside, NET_BK, INNER, j=.1, step=8)
    back = rect(bx0, bt, bx1, bb)
    p.shape(back, NET_BK, INNER, j=.1, step=8)
    for x in range(bx0 + 20, bx1, 20): p.ln((x, bt + 3), (x, bb - 3), 2.2, NET_L, j=0)
    for y in (bt + 30, bt + 60): p.ln((bx0 + 3, y), (bx1 - 3, y), 2.2, NET_L, j=0)
    # پایهٔ پشت چپ (باریک)
    side = [(FX1, FT), (bx1, bt), (bx1, bb), (FX1, FB)]
    p.shape(side, NET_SD, PART, j=.1, step=8)
    for k in (1,): 
        t = k / 2; p.ln((FX1 + DX * t, FT + DY * t + 3), (FX1 + DX * t, FB + DY * t - 3), 2.2, NET_L, j=0)
    for y in (-80, -50): p.ln((FX1 + 3, y), (bx1 - 3, y + DY), 2.2, NET_L, j=0)
    roof = [(FX0, FT), (FX1, FT), (bx1, bt), (bx0, bt)]
    p.shape(roof, NET_RF, PART, j=.1, step=8)
    for k in (1, 2, 3):
        t = k / 4; p.ln((FX0 + (FX1 - FX0) * t, FT - 2), (bx0 + (bx1 - bx0) * t, bt + 2), 2.2, NET_L, j=0)
    # پایهٔ پشت راست
    # ۲) تیرک‌های جلو و تیرافقی
    post(p, FX0 - 7, FT, FX0 + 7, FB + 2)
    post(p, FX1 - 7, FT, FX1 + 7, FB + 2)
    post(p, FX0 - 7, FT - 7, FX1 + 7, FT + 7)
    # ۳) توپ
    with layer(p, 'ball'):
        p.tipshadow(2, 7, 34)
        circ = ell(BCX, BCY, BR, BR, 0, 360, 48)
        p.shape(circ, BALL_B, OUT, j=.06, step=99)
        for dd, off, col in ((17, 0, BALL_D), (8, 0, BALL_DD)):
            phi = math.radians(40.6); h = math.degrees(math.acos(dd / (2 * BR)))
            S = (BCX - 14 - off, BCY - 12)
            cres = [(BCX + BR * math.cos(math.radians(a)), BCY + BR * math.sin(math.radians(a))) for a in [math.degrees(phi) - h + 2 * h * i / 20 for i in range(21)]]
            cres += [(S[0] + BR * math.cos(math.radians(a)), S[1] + BR * math.sin(math.radians(a))) for a in [math.degrees(phi) + h - 2 * h * i / 20 for i in range(21)]]
            poly(p, cres, col)
        for i in range(5):
            a = math.radians(-90 + 72 * i)
            v = (BCX + 14 * math.cos(a), BCY + 14 * math.sin(a)); e = (BCX + 28 * math.cos(a), BCY + 28 * math.sin(a))
            p.ln(v, e, INNER, NAVY, j=0)
            oc = (BCX + 42 * math.cos(a), BCY + 42 * math.sin(a))
            poly(p, clipc(pent(oc[0], oc[1], 15, math.degrees(a) + 180), BR - 1.5), PATCH)
        poly(p, pent(BCX, BCY, 14, -90), PATCH)
        p.stroke(circ, OUT, j=.06, step=99)
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
