#!/usr/bin/env python3
"""ایستگاه F08 «میدان طناب‌کشی» (سرزمین ورزشگاه، پالت sports، رنگ‌مایهٔ سکو ۹۳°) — دور ۲ (اصلاح پس از ردّ ناظر).
طرح قطعه‌به‌قطعه (واحد symbol، y منفی = بالا):
 ۱) دو میلهٔ چوبی کوتاه (۴۵ واحد، پهنای ۱۴) با فاصلهٔ ۹۰ (x=-66 و +24 و XF جابه‌جا می‌کند)؛ چوب #b77a3a/#d9a463/#7a4a1f.
    بلوک پایه ۲۶×۱۲ از ماده‌ای دیگر: سنگ آبی-خاکستری #8fa3bf/#b9c9de/#5e7194 (رنگ‌مایه ≈۲۱۵ در برابر چوب ≈۳۰).
    میله‌ها clip=False: نوار نور/سایهٔ سکو هیچ‌کدام را نمی‌پوشاند ⇒ یکسان. نور و سایهٔ خود میله تخت و داخل میله.
 ۲) طناب کلفت (۱۰) ماسه‌ای #f6e7b4/#fffaf0/#cfae62، کمی شُل (خمیدگی ۸ واحد به پایین)، از گرهٔ چپ تا گرهٔ راست؛
    گرهٔ درشت هشت‌ضلعی r=9 روی هر میله با نقطهٔ نور؛ دو برش مورب تخت روی هر نیمهٔ طناب.
 ۳) لایهٔ متحرک node_tug_field_flag: نوار پرچم بنفش بزرگ (۲۶×۴۰، دم دوشاخه) آویزان از وسط طناب، مرکز روی x=CX؛
    #7b4fd0/#a98bf0/#4a2c94؛ حالت ایستا = وسط.
 ۴) زرد کوچک: دایرهٔ تخت r2.4 روی نقطهٔ نور هر گره.
رنگ قهرمان: چوب ≈۳۰°، ماسه ≈۴۵°، بنفش ≈۲۶۰°، پایه ≈۲۱۵° — همه ≥۳۵° از ۹۳°."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
_k.margin_check = functools.partial(_k.margin_check, min_margin=8.5); _k.motion_check = functools.partial(_k.motion_check, min_margin=8.5)
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/tug_field'

WOOD = '#b77a3a'; WOOD_L = '#d9a463'; WOOD_D = '#7a4a1f'
SAND = '#f6e7b4'; SAND_L = '#fffaf0'; SAND_D = '#cfae62'
PUR = '#7b4fd0'; PUR_L = '#a98bf0'; PUR_D = '#4a2c94'; YEL = '#ffd84d'

STONE = '#8fa3bf'; STONE_L = '#b9c9de'; STONE_D = '#5e7194'
XF = (1.2, 5.6, 0.0)
PX = (-45, 9)                    # مراکز میله‌ها
CX = sum(PX) / 2                 # -21 محور تقارن
PW = 13; PT = -44                # میله: بالا (ارتفاع ۴۵ تا بالای پایه)
BW, BT, BB = 20, -2, 10           # بلوک پایه ۲۶×۱۲
RY0, RH, SAG = -24, 15, 1         # طناب: مرکز در میله‌ها، ضخامت، شُلی وسط
BAND_W = 17; BAND_B = 0
SH = 7                           # حرکت: ±5px ≈ 7 واحد


def rope_y(x):
    t = (x - PX[0]) / (PX[1] - PX[0]); return RY0 + SAG * 4 * t * (1 - t)


def flat(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def rect(p, x0, y0, x1, y1, col, op=1): flat(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col, op)


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def mpoly(p, pts, fill, sw):
    q = p.X(pts); d = 'M' + 'L'.join('%.1f,%.1f' % z for z in q) + 'Z'
    p.raw('<path d="%s" fill="%s" class="eo" stroke-width="%s" stroke-linejoin="round"/>' % (d, fill, sw))


def post(p, x):
    p.tipshadow(x + 1, BB, 17); p.foot_tip(x, BB, 10)
    # بلوک پایه (سنگ)
    q = [(x - BW / 2, BT), (x + BW / 2, BT), (x + BW / 2, BB), (x - BW / 2, BB)]
    p.shape(q, STONE, PART, j=.1, step=6, clip=False)
    rect(p, x - BW / 2 + 4, BT + 4, x - BW / 2 + 8, BB - 4, STONE_L)
    rect(p, x + 3, BT + 4, x + BW / 2 - 3, BB - 3, STONE_D, .6)
    p.stroke(q, PART, j=.1, step=6)
    # میله (چوب)
    q = [(x - PW / 2, PT), (x + PW / 2, PT), (x + PW / 2, BT + 3), (x - PW / 2, BT + 3)]
    p.shape(q, WOOD, PART, j=.1, step=6, clip=False)
    rect(p, x - PW / 2 + 3.5, PT + 4, x - PW / 2 + 6.5, BT - 2, WOOD_L)
    rect(p, x + 1.5, PT + 4, x + PW / 2 - 2.9, BT - 2, WOOD_D, .55)
    p.stroke(q, PART, j=.1, step=6)


def build():
    p = Pen('tug_field', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((36, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    for x in PX: post(p, x)
    # طناب شُل: نوار منحنی کلفت ۱۰ (خط INNER)
    n = 24; xs = [PX[0] + (PX[1] - PX[0]) * i / n for i in range(n + 1)]
    up = [(x, rope_y(x) - RH / 2) for x in xs]; dn = [(x, rope_y(x) + RH / 2) for x in reversed(xs)]
    mpoly(p, up + dn, SAND, INNER)
    for sgn in (-1, 1):                                   # برش‌های مورب منظم، متقارن حول CX
        for dx in (20, 30):
            x = CX + sgn * dx; y = rope_y(x); h = RH / 2 - 1.9
            flat(p, [(x - 3.2, y + h), (x + .6, y + h), (x + 3.2, y - h), (x - .6, y - h)], SAND_D)
    for x in PX:                                          # گرهٔ درشت: بند دور میله ۲۰×۱۴ + نقطهٔ نور و زرد
        y = rope_y(x)
        mpoly(p, [(x - 10, y - 7), (x + 10, y - 7), (x + 10, y + 7), (x - 10, y + 7)], '#7a4a1f', INNER)
        flat(p, [(x - 6.5, y - 3.5), (x - 3, y - 3.5), (x - 3, y + 3.5), (x - 6.5, y + 3.5)], SAND_L)
        disc(p, x + 3, y, 2.4, YEL)
    with layer(p, 'flag'):
        w = BAND_W / 2; top = rope_y(CX) - 3
        pts = [(CX - w, top), (CX + w, top), (CX + w, BAND_B), (CX, BAND_B - 9), (CX - w, BAND_B)]
        mpoly(p, pts, PUR, PART)
        rect(p, CX - w + 4.5, top + 5, CX - w + 8.5, BAND_B - 5, PUR_L)
        flat(p, [(CX + 4, top + 5), (CX + w - 3, top + 5), (CX + w - 3, BAND_B - 4), (CX + 4, BAND_B - 11)], PUR_D, .6)
        mpoly(p, pts, 'none', PART)
    return p


if __name__ == '__main__':
    p = build()
    offs = [(0, 0), p.V((-SH, 0)), p.V((SH, 0)), (0, 0)]
    r = finish(p, 'tug_field', None, motion={'flag': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_tug_field_flag': dict(
        kind='نوار بنفش روی طناب؛ فقط translateX؛ حالت ایستا = وسط (پایان)',
        keyframes_px=[0, -5, 5, 0], keyframes_symbol_units=[0, -SH, SH, 0], average_px=0,
        duration_s=2.4, easing='ease-in-out', loop=False, trigger='رسیدن کودک (یک‌بار)',
        concept='نیروی برآیند: وسط ایستاده = نیروهای برابر و مخالف؛ بدون برنده، بدون پیکان',
        constraint='نوار بین دو میله می‌ماند و از سکو بیرون نمی‌زند؛ کاهش حرکت: وسط', fixed='میله‌ها، بلوک‌ها، طناب')}
    (OUTD / 'tug_field.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
