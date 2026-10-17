#!/usr/bin/env python3
"""ایستگاه «بارانداز» (بازطراحی ۱۷ اکتبر): قهرمان = چرخ‌دستی (چهارچرخ بارکش، از کنار دو چرخ دیده می‌شود) با دو جعبهٔ بار، سکوی دریایی.
لایه‌های متحرک (هرکدام چرخش حول مرکز خودش): node_wheel_dock_wheel = چرخ راست (id قدیمی)، node_wheel_dock_wheel_back = چرخ چپ.
بدنه، جعبه‌ها و دستهٔ چرخ‌دستی ثابت‌اند؛ چرخ‌ها دایره‌اند و در هر زاویه از سکو بیرون نمی‌زنند."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit3/wheel_dock'
XF = (.95, 4.0, 3.0)
BED = '#c98a3a'; CRATE_A = '#ffd84d'; CRATE_B = '#f59a3a'; DARK = '#8a5f0c'; WH = '#7b8fe0'; WH_D = '#241a5e'
R = 14; WY = 8; WX = (-44, -14)


def cart(p):
    # دستهٔ ایستادهٔ چرخ‌دستی در انتهای چپ (عقب)، بعد بدنه و دو جعبه
    p.ln((-62, -6), (-62, -50), PART, DARK, j=.1, probe='دستهٔ چرخ‌دستی (جزء)')
    p.ln((-62, -50), (-50, -50), PART, DARK, j=.1)
    p.shape([(-66, -10), (4, -10), (4, 4), (-66, 4)], BED, PART, j=.2, step=6)
    p.shape([(-54, -42), (-29, -42), (-29, -7), (-54, -7)], CRATE_A, PART, j=.2, step=6)
    p.ln((-48, -26), (-35, -26), INNER, '#d9961c', j=.1)
    p.shape([(-26, -36), (0, -36), (0, -7), (-26, -7)], CRATE_B, PART, j=.2, step=6)
    p.ln((-20, -22), (-6, -22), INNER, '#c9701c', j=.1)


def wheel(p, cx):
    p.shape(ell(cx, WY, R, R, 0, 360, 40), WH, INNER, j=.3, step=99, clip=False)
    for k in range(2):
        t = math.radians(45 + 90 * k)
        p.ln((cx - 8 * math.cos(t), WY - 8 * math.sin(t)), (cx + 8 * math.cos(t), WY + 8 * math.sin(t)), INNER, '#fff3c4', j=.05)
    p.raw('<circle cx="%.1f" cy="%.1f" r="3.2" fill="%s"/>' % (*p.X((cx, WY)), WH_D))


def build(out=None):
    p = Pen('wheel_dock', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    for cx in WX:
        p.tipshadow(cx, WY + R - 1, 12); p.foot_tip(cx, WY + R - 2, 5)
    cart(p)
    with layer(p, 'wheel_back'): wheel(p, WX[0])
    with layer(p, 'wheel'): wheel(p, WX[1])
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    mo = {'wheel': dict(rotate=p.X((WX[1], WY))), 'wheel_back': dict(rotate=p.X((WX[0], WY)))}
    r = finish(p, 'wheel_dock', STAND, motion=mo, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(wheel=dict(layer='node_wheel_dock_wheel', rotate_about=[round(v, 1) for v in p.X((WX[1], WY))], note='چرخ راست؛ id قدیمی حفظ شد'),
                                             wheel_back=dict(layer='node_wheel_dock_wheel_back', rotate_about=[round(v, 1) for v in p.X((WX[0], WY))], note='چرخ چپ، لایهٔ جدید'))
    (OUTD / 'wheel_dock.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
