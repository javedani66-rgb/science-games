#!/usr/bin/env python3
"""ایستگاه «جرثقیل بندر» (M08): قهرمان = جرثقیل بندری ساده (پایه، دکل، بازوی افقی، طناب و جعبه)، سکوی دریایی.
لایهٔ متحرک node_harbor_crane_hook = طناب+قلاب+جعبه، فقط بالا/پایین (۰ تا +12). بالای طناب پشت بازوی ثابت پنهان است
و بازو جلوی آن کشیده می‌شود، پس بدنهٔ ثابت (پایه، دکل، بازو) همیشه کامل و پیوسته است."""
import sys, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent

C_T = '#ff8a5c'; C_L = '#e0553a'; C_D = '#9c2f1c'      # جرثقیل: مرجانی روشن/تیره
B_T = '#ffd84d'; B_H = '#8a5f0c'                        # جعبه
CW = '#8f8bd6'
MX = -22            # محور دکل
J = -80             # خط وسط بازو
FOOT = 18
BX = 18             # محور طناب/جعبه


def flat(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in pts), col))


def base_and_mast(p):
    # پایهٔ چهارگوش
    p.shape([(MX - 20, FOOT - 14), (MX + 20, FOOT - 14), (MX + 20, FOOT), (MX - 20, FOOT)], C_L, OUT, j=.3, step=5)
    flat(p, [(MX + 3, FOOT - 11), (MX + 17, FOOT - 11), (MX + 17, FOOT - 3), (MX + 3, FOOT - 3)], C_D)
    # دکل پیوسته، دو رنگ
    p.shape([(MX - 8, J), (MX + 8, J), (MX + 8, FOOT - 14), (MX - 8, FOOT - 14)], C_T, OUT, j=.3, step=5)
    flat(p, [(MX + 1, J + 4), (MX + 6, J + 4), (MX + 6, FOOT - 17), (MX + 1, FOOT - 17)], C_L)
    for y in (-8, -34, -58):
        p.ln((MX - 8, y), (MX + 8, y), INNER, C_D, j=.1, probe='بند دکل (داخلی)' if y == -8 else None)


def hook(p):
    """بخش متحرک: طناب (از داخل بازو)، قلاب، جعبه."""
    top = J - 6; bt = -14
    p.ln((BX, top), (BX, bt - 6), PART, B_H, j=0, probe='طناب (جزء)')
    p.shape(ell(BX, bt - 4, 4.5, 4.5, 0, 360, 14), B_T, INNER, j=.1, step=5, clip=False)
    p.shape([(BX - 14, bt), (BX + 14, bt), (BX + 14, bt + 22), (BX - 14, bt + 22)], B_T, PART, j=.3, step=5, clip=False)
    p.ln((BX - 14, bt + 11), (BX + 14, bt + 11), INNER, B_H, j=0, probe='تختهٔ جعبه (داخلی)')


def jib(p):
    # بازوی افقی (جلوی طناب) با دم کوتاه و وزنه
    p.shape([(MX - 30, J - 7), (BX + 22, J - 7), (BX + 22, J + 7), (MX - 30, J + 7)], C_T, OUT, j=.3, step=5)
    flat(p, [(MX - 26, J + 1), (BX + 18, J + 1), (BX + 18, J + 4), (MX - 26, J + 4)], C_L)
    p.shape([(MX - 34, J - 4), (MX - 22, J - 4), (MX - 22, J + 18), (MX - 34, J + 18)], CW, PART, j=.3, step=5, clip=False)
    # کابین/تکیه‌گاه: مثلث راست بالای دکل
    p.shape([(MX - 8, J - 7), (MX + 8, J - 7), (MX, J - 24)], C_L, PART, j=.3, step=5, clip=False)


def build(out=HERE):
    p = Pen('harbor_crane', 'sea'); pad(p, line=((34, 22), (54, 18)), tri=((54, -14), (-58, -14)), dot=(-56, 12))
    p.tipshadow(MX, FOOT, 24); p.foot_tip(MX, FOOT - 2, 18)
    p.tipshadow(BX, FOOT + 1, 20)
    base_and_mast(p)
    with layer(p, 'hook'): hook(p)
    jib(p)
    return p


STAND = (40, -2)
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/batch2/harbor_crane'

if __name__ == '__main__':
    p = build()
    r = finish(p, 'harbor_crane', STAND, motion={'hook': dict(offsets=[(0, 0), (0, 4), (0, 8), (0, 12)])}, out=HERE / 'out', shots=SHOTS)
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
