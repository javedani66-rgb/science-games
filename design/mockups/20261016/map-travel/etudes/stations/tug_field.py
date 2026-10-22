#!/usr/bin/env python3
"""ایستگاه F08 «میدان طناب‌کشی» (سکوی sports، رنگ‌مایهٔ سکو ۹۳°) — دور ۵ (بازطراحی: بزرگ، وسط، طناب کلفت و کشیده).
طرح قطعه‌به‌قطعه (واحد symbol، محور CX=0 = مرکز سکو؛ y منفی = بالا؛ کف 7):
 ۱) دو میلهٔ فولادی آبی (پهنای ۱۴، y -58..+3) در x=±50 با بلوک پایهٔ روشن (۲۶×۱۲)؛ آبی ≈۲۲۰°.
 ۲) طناب کلفت قهوه‌ای-کرم (۱۸ ضخامت) کاملاً صاف و افقی در y=-30 از میلهٔ چپ تا راست؛ هفت برش مورب روشن/تیره با فاصلهٔ ۱۲ مثل تابِ طناب.
 ۳) دو بند تیره دور میله‌ها (۲۴×۲۲) با نقطهٔ نور روشن؛ طناب زیر بندها می‌رود (هم‌پوشانی).
 ۴) لایهٔ متحرک node_tug_field_flag: روبان قرمز (۲۲×۴۴، دم دوشاخه) بسته‌شده روی طناب، مرکز x=CX؛ حالت ایستا = وسط.
رنگ قهرمان: آبی ≈۲۲۰°، قهوه‌ای ≈۳۰°، قرمز ≈۵° — همه ≥۳۵° از ۹۳°. بدون پیکان، بدون قرقره."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
_k.margin_check = functools.partial(_k.margin_check, min_margin=8.5); _k.motion_check = functools.partial(_k.motion_check, min_margin=8.5)
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/tug_field'

P_B, P_L, P_D = '#5f86d0', '#9fbdf0', '#3d5c9e'          # میله (فولاد آبی)
K_B, K_L, K_D = '#dfe6f0', '#f7faff', '#aab6c8'          # بلوک پایه (سنگ روشن)
T_B, T_L, T_D = '#c98a45', '#f0b774', '#8a5524'          # طناب
B_B, B_D = '#5a3a1c', '#3c2410'                          # بند
F_B, F_L, F_D = '#e0443a', '#ff8a73', '#a82a24'          # روبان قرمز
YEL = '#ffd84d'

CX = 0
PX = (-42, 42)
PW = 18; PT = -62
BW, BT, BB = 26, -4, 8
RY, RH = -16, 30
BAND_W, BAND_H = 18, 28
SH = 7                     # حرکت ±۷ واحد ≈ ۵px
FW, FT, FB = 11, -42, 0    # روبان: نیم‌پهنا، بالا، پایین


def flat(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def rect(p, x0, y0, x1, y1, col, op=1): flat(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col, op)


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def post(p, x):
    p.foot_tip(x, BB - 1, 10)
    q = [(x - PW / 2, PT), (x + PW / 2, PT), (x + PW / 2, BB), (x - PW / 2, BB)]
    p.shape(q, P_B, PART, j=.1, step=6, clip=False)
    rect(p, x - PW / 2 + 3.5, PT + 4, x - PW / 2 + 6.5, BB - 4, P_L)
    rect(p, x + 1.5, PT + 4, x + PW / 2 - 2.9, BB - 3, P_D, .8)
    p.stroke(q, PART, j=.1, step=6)


def build():
    p = Pen('tug_field', 'sports'); pad(p, line=((50, 30), (70, 27)), tri=((36, -22), (74, 6)), dot=(68, -14)); p.xf = (1.0, 0, 0)
    p.tipshadow(CX + 2, BB + 2, 50)
    for x in PX: post(p, x)
    # طناب صاف و کلفت با دو سر گرد، از روی میله‌ها رد می‌شود
    EX, r = 60, RH / 2
    rope = [(-EX + r, RY - r), (EX - r, RY - r)] + ell(EX - r, RY, r, r, -90, 90, 8)[1:-1] + [(EX - r, RY + r), (-EX + r, RY + r)] + ell(-EX + r, RY, r, r, 90, 270, 8)[1:-1]
    p.shape(rope, T_B, PART, j=.1, step=6, clip=False)
    rect(p, -EX + r, RY - r + 4, EX - r, RY - r + 7.5, T_L)                                    # نور بالا
    for x in (-27, -17, 17, 27):                                                       # تاب طناب: برش‌های مورب هم‌فاصله
        flat(p, [(x - 6, RY + r - 3.5), (x - 1.5, RY + r - 3.5), (x + 6, RY - r + 9), (x + 1.5, RY - r + 9)], T_D, .85)
    rect(p, -EX + r, RY + r - 3.5 - 3.5, EX - r, RY + r - 3.5, T_D, .5)
    p.stroke(rope, PART, j=.1, step=6)
    for x in PX:                                                                                 # بند دور میله
        q = [(x - 5.5, RY - RH / 2 - 2), (x + 5.5, RY - RH / 2 - 2), (x + 5.5, RY + RH / 2 + 2), (x - 5.5, RY + RH / 2 + 2)]
        p.shape(q, B_B, INNER, j=.08, step=6, clip=False)
    with layer(p, 'flag'):
        # نشانگر وسط: پرچم قرمز روی تیرک کوتاه، با بند قرمز دور طناب (مرکز x=CX)
        p.ln((CX, RY - RH / 2 + 2), (CX, -68), PART, T_D, j=0)
        fl = [(CX - 1, -70), (CX + 30, -57), (CX - 1, -44)]
        p.shape(fl, F_B, INNER, j=.05, step=99, clip=False)
        flat(p, [(CX + 5, -63), (CX + 16, -58), (CX + 5, -58)], F_L)
        q = [(CX - 9, RY - RH / 2 - 2), (CX + 9, RY - RH / 2 - 2), (CX + 9, RY + RH / 2 + 2), (CX - 9, RY + RH / 2 + 2)]
        p.shape(q, F_B, PART, j=.08, step=6, clip=False)
        rect(p, CX - 5, RY - RH / 2 + 2, CX - 2, RY + RH / 2 - 2, F_L)
        flat(p, [(CX + 3, RY - RH / 2 + 2), (CX + 6, RY - RH / 2 + 2), (CX + 6, RY + RH / 2 - 2), (CX + 3, RY + RH / 2 - 2)], F_D, .8)
        p.stroke(q, PART, j=.08, step=6)
    return p


if __name__ == '__main__':
    p = build()
    offs = [(0, 0), p.V((-SH, 0)), p.V((SH, 0)), (0, 0)]
    r = finish(p, 'tug_field', None, motion={'flag': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_tug_field_flag': dict(
        kind='روبان قرمز روی طناب؛ فقط translateX؛ حالت ایستا = وسط (پایان)',
        keyframes_px=[0, -5, 5, 0], keyframes_symbol_units=[0, -SH, SH, 0], average_px=0,
        duration_s=2.4, easing='ease-in-out', loop=False, trigger='رسیدن کودک (یک‌بار)',
        concept='نیروی برآیند: وسط ایستاده = نیروهای برابر و مخالف؛ بدون برنده، بدون پیکان',
        constraint='روبان بین دو میله می‌ماند و از سکو بیرون نمی‌زند؛ کاهش حرکت: وسط', fixed='میله‌ها، بلوک‌ها، طناب')}
    (OUTD / 'tug_field.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
