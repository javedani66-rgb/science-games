#!/usr/bin/env python3
"""ایستگاه «جرثقیل بندر» (M08؛ بازطراحی ۱۸ اکتبر: کوتاه‌تر، کل نماد با حاشیهٔ ≥۴px درون رویهٔ سکو): قهرمان = جرثقیل بندری روی سکوی دریایی: ماشین‌خانه، بازوی مورب، قلاب با طناب و کانتینر کوچک.
لایهٔ متحرک node_harbor_crane_hook = طناب+قلاب+کانتینر (بالا/پایین ۰ تا +۶)؛ بالای طناب پشت بازوی ثابت است."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
from station_kit import _shot, _poly
HERE = pathlib.Path(__file__).resolve().parent

XF = (1.0, 7.0, 1.0)            # قاب قهرمان: (مقیاس هندسه، dx، dy) در واحد symbol؛ ضخامت خط ثابت می‌ماند
C_T = '#ff8a5c'; C_L = '#e0553a'; C_D = '#9c2f1c'      # جرثقیل: مرجانی روشن/تیره
B_T = '#ffd84d'; B_H = '#8a5f0c'                        # جعبه
CW = '#8f8bd6'
BX0, BX1, BT, BB = -58, -30, -10, 12       # بدنهٔ جرثقیل (ماشین‌خانه): چپ، راست، بالا، پایین (کوتاه‌تر تا همه‌چیز درون رویهٔ سکو بماند)
TIP = (-4, -25)                         # نوک بازو (پایین‌تر از لبهٔ بالای سکو)
PIV = (-40, -10)                           # لولای بازو
BX = -4
CT, CH, CWD = 2, 14, 20                 # کانتینر: بالا، ارتفاع، پهنا
CNT = '#4fae4a'; CNT_D = '#1f6b2e'
HW = 5.5                                   # نیم‌پهنای بازو


def flat(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def machine(p):
    p.shape([(BX0, BT), (BX1, BT), (BX1, BB), (BX0, BB)], C_L, PART, j=.3, step=5)
    flat(p, [(BX0 + 5, BB - 8), (BX1 - 5, BB - 8), (BX1 - 5, BB - 4), (BX0 + 5, BB - 4)], C_D)      # نوار تیره پایین
    flat(p, [(BX0 + 6, BT + 8), (BX0 + 16, BT + 8), (BX0 + 16, BT + 14), (BX0 + 6, BT + 14)], '#cfeaff')  # پنجرهٔ اتاقک


def hook(p):
    """بخش متحرک: طناب، قلاب و کانتینر (بالا/پایین)."""
    p.ln((BX, TIP[1]), (BX, CT - 5), PART, '#8a5f0c', j=0)
    p.probes.append(('طناب (جزء)', PART, p.X((BX, -11.5)), (1, 0), '#8a5f0c'))
    p.shape([(BX - 5, CT - 6), (BX + 5, CT - 6), (BX + 5, CT), (BX - 5, CT)], C_D, PART, j=.1, step=5, clip=False)     # قلاب
    p.shape([(BX - CWD / 2, CT), (BX + CWD / 2, CT), (BX + CWD / 2, CT + CH), (BX - CWD / 2, CT + CH)], CNT, PART, j=.3, step=5, clip=False)
    p.ln((BX, CT + 5), (BX, CT + CH - 4), INNER, CNT_D, j=0, probe='تختهٔ کانتینر (داخلی)')


def jib(p):
    dx, dy = TIP[0] - PIV[0], TIP[1] - PIV[1]; L = math.hypot(dx, dy); nx, ny = -dy / L * HW, dx / L * HW
    p.shape([(PIV[0] + nx, PIV[1] + ny), (TIP[0] + nx, TIP[1] + ny), (TIP[0] - nx, TIP[1] - ny), (PIV[0] - nx, PIV[1] - ny)], C_T, PART, j=.3, step=7)
    p.shape(ell(PIV[0], PIV[1], 6, 6, 0, 360, 16), C_D, PART, j=.1, step=99, clip=False)      # لولا


def build(out=None):
    p = Pen('harbor_crane', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-40, BB, 26); p.foot_tip(-40, 8, 12)
    machine(p)
    with layer(p, 'hook'): hook(p)
    jib(p)
    return p


STAND = None     # خودکار: find_stand
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit3/harbor_crane'

if __name__ == '__main__':
    p = build()
    r = finish(p, 'harbor_crane', STAND, motion={'hook': dict(offsets=[p.V(o) for o in [(0, 0), (0, 2), (0, 4), (0, 6)]])}, out=HERE / 'out', shots=SHOTS)
    offs = [p.V(o) for o in [(0, 0), (0, 2), (0, 4), (0, 6)]]
    sp = r['spec']; sp['motion_spec'] = dict(offsets=offs, note='طناب+قلاب+کانتینر بالا/پایین ۰ تا +۶؛ بالای طناب پشت بازوی ثابت')
    (HERE / 'out' / 'harbor_crane.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
