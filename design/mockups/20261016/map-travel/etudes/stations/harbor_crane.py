#!/usr/bin/env python3
"""ایستگاه «جرثقیل بندر» (M08): قهرمان = جرثقیل بندری ساده (پایه، دکل، بازوی افقی با وزنه، طناب و جعبه)، سکوی دریایی.
لایهٔ متحرک node_harbor_crane_hook = طناب+جعبه، فقط بالا/پایین (۰ تا +۱۲). بالای طناب پشت بازوی ثابت پنهان است
و بازو جلوی آن کشیده می‌شود، پس بدنهٔ ثابت (پایه، دکل، بازو) همیشه کامل و پیوسته است.
طراحی دوباره برای خط ضخیم‌تر (D113، D110): دکل و بازو پهن‌تر، بدون بندهای ریز؛ سایهٔ دکل رنگ تخت."""
import sys, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent

XF = (1.0, 0.0, 0.0)            # قاب قهرمان: (مقیاس هندسه، dx، dy) در واحد symbol؛ ضخامت خط ثابت می‌ماند
C_T = '#ff8a5c'; C_L = '#e0553a'; C_D = '#9c2f1c'      # جرثقیل: مرجانی روشن/تیره
B_T = '#ffd84d'; B_H = '#8a5f0c'                        # جعبه
CW = '#8f8bd6'
MX0, MX1 = -42, -24            # دکل
J0, J1 = -100, -84             # بازو (بالا، پایین)
JX0, JX1 = -58, 0              # بازو (چپ، راست)
FOOT = 16
BX = -9                        # محور طناب/جعبه


def flat(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def base_and_mast(p):
    p.shape([(MX0 - 12, 0), (MX1 + 12, 0), (MX1 + 12, FOOT), (MX0 - 12, FOOT)], C_L, OUT, j=.3, step=5)
    p.shape([(MX0, J1), (MX1, J1), (MX1, 0), (MX0, 0)], C_T, OUT, j=.3, step=5)
    flat(p, [(MX0 + 9, J1 + 5), (MX1 - 4, J1 + 5), (MX1 - 4, -4), (MX0 + 9, -4)], C_L)       # نیمهٔ سایهٔ دکل (تخت)


def hook(p):
    """بخش متحرک: طناب (از داخل بازو) و جعبه."""
    top = -44
    p.ln((BX, J1 - 4), (BX, top), PART, B_H, j=0)
    p.probes.append(('طناب (جزء)', PART, p.X((BX, (J1 + top) / 2)), (1, 0), B_H))
    p.shape([(BX - 12, top), (BX + 12, top), (BX + 12, top + 24), (BX - 12, top + 24)], B_T, PART, j=.3, step=5, clip=False)
    p.ln((BX - 12, top + 12), (BX + 12, top + 12), INNER, B_H, j=0, probe='تختهٔ جعبه (داخلی)')


def jib(p):
    p.shape([(JX0, J0), (JX1, J0), (JX1, J1), (JX0, J1)], C_T, OUT, j=.3, step=5)
    flat(p, [(JX0 + 5, J1 - 5), (JX1 - 4, J1 - 5), (JX1 - 4, J1 - 2), (JX0 + 5, J1 - 2)], C_L)
    p.shape([(JX0, J1), (JX0 + 14, J1), (JX0 + 14, J1 + 20), (JX0, J1 + 20)], CW, PART, j=.3, step=5, clip=False)   # وزنهٔ تعادل


def build(out=None):
    p = Pen('harbor_crane', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow((MX0 + MX1) / 2, FOOT, 30); p.foot_tip((MX0 + MX1) / 2, FOOT - 2, 14)
    base_and_mast(p)
    with layer(p, 'hook'): hook(p)
    jib(p)
    return p


STAND = None     # خودکار: find_stand
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit2/after/harbor_crane'

if __name__ == '__main__':
    p = build()
    r = finish(p, 'harbor_crane', STAND, motion={'hook': dict(offsets=[p.V(o) for o in [(0, 0), (0, 4), (0, 8), (0, 12)]])}, out=HERE / 'out', shots=SHOTS)
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
