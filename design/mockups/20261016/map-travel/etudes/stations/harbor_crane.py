#!/usr/bin/env python3
"""ایستگاه «جرثقیل بندر» (M08؛ بازطراحی ۱۸ اکتبر شب، D123): جرثقیل درشت و پرجزئیات روی سکوی دریایی:
ماشین‌خانهٔ مرجانی با پنجره‌ها و در، چرخ‌های پایه، دکل، بازوی خرپایی (دو بال + ضلعی‌ها)، وزنهٔ تعادل، قلاب با طناب و کانتینر سبز،
و یک کانتینر نارنجی روی زمین. بازو از بالای فیگور رد می‌شود (آزاد از بالا)؛ پایه کاملاً سمت چپ می‌ماند.
لایهٔ متحرک node_harbor_crane_hook = طناب+قلاب+بندها+کانتینر آویزان (بالا/پایین ۰ تا +۶)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import station_kit
from station_kit import *
from functools import partial
station_kit.margin_check = partial(station_kit.margin_check, min_margin=4)   # D123: حاشیهٔ چپ/راست ≥۴px
HERE = pathlib.Path(__file__).resolve().parent

XF = (1.0, -2.0, 2.0)
C_T = '#ff9a6c'; C_L = '#e0553a'; C_D = '#9c2f1c'; C_H = '#ffc7a6'
GL = '#cfeaff'; GL_D = '#6fa8dc'
CNT = '#4fae4a'; CNT_L = '#8fd46f'; CNT_D = '#1f6b2e'
OR = '#ff9b2f'; OR_L = '#ffc56b'; OR_D = '#b4620f'
YEL = '#ffd84d'
G = 12                          # خط زمین
HX0, HX1, HT = -58, -28, -30    # ماشین‌خانه
MX0, MX1 = -52, -38             # برج
JX0, JX1, JT, JB = -62, 30, -108, -92   # بازوی ضخیم
BX = -8                         # محور کابل
HB0 = -74                       # بالای بلوک قلاب
CT, CH, CWD = -50, 20, 26       # کانتینر آویزان


def flat(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def rect(p, x0, y0, x1, y1, col): flat(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col)


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def container(p, x0, y0, x1, y1, col, lt, dk, ribs=4, clip=True):
    p.shape([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col, PART, j=.25, step=6, clip=clip)
    rect(p, x0 + 3, y0 + 3, x1 - 3, y0 + 6, lt)                           # نور بالا
    w = (x1 - x0 - 6) / ribs
    for i in range(1, ribs):
        rect(p, x0 + 3 + i * w - 1.6, y0 + 8, x0 + 3 + i * w + 1.6, y1 - 3, dk)    # آج‌های عمودی


def hook(p):
    """بخش متحرک: کابل، بلوک قلاب، دو بند و یک کانتینر آویزان (جدا از هم، هم‌پوشان نیستند)."""
    p.ln((BX, JB), (BX, HB0), PART, '#8a5f0c', j=0)
    p.probes.append(('کابل (جزء)', PART, p.X((BX, (JB + HB0) / 2)), (1, 0), '#8a5f0c'))
    p.shape([(BX - 7, HB0), (BX + 7, HB0), (BX + 7, HB0 + 11), (BX - 7, HB0 + 11)], C_D, PART, j=.1, step=5, clip=False)    # بلوک قلاب
    disc(p, BX, HB0 + 5.5, 2.2, YEL)
    p.ln((BX - 4, HB0 + 11), (BX - 10, CT), INNER, '#8a5f0c', j=0)
    p.ln((BX + 4, HB0 + 11), (BX + 10, CT), INNER, '#8a5f0c', j=0)
    container(p, BX - CWD / 2, CT, BX + CWD / 2, CT + CH, CNT, CNT_L, CNT_D, 3, clip=False)


def jib(p):
    """بازوی ضخیم و ساده (بدون خرپا) + وزنهٔ تعادل؛ پشت لایهٔ متحرک ثابت می‌ماند."""
    p.shape([(JX0, JT), (JX1, JT), (JX1, JB), (JX0, JB)], C_T, PART, j=.3, step=7)
    rect(p, JX0 + 4, JT + 4, JX1 - 4, JT + 7.5, C_H)                              # نور بالای بازو
    p.shape([(JX0, JB - 2), (JX0 + 16, JB - 2), (JX0 + 16, JB + 14), (JX0, JB + 14)], C_D, PART, j=.2, step=6)         # وزنهٔ تعادل
    rect(p, JX0 + 3, JB + 1, JX0 + 6.5, JB + 8, '#c9411f')


def machine(p):
    # برج
    p.shape([(MX0, JT + 6), (MX1, JT + 6), (MX1, HT + 4), (MX0, HT + 4)], C_T, PART, j=.3, step=7)
    rect(p, MX0 + 3, JB + 4, MX0 + 6.5, HT, C_H)
    # ماشین‌خانه با پنجرهٔ بزرگ
    p.shape([(HX0, HT), (HX1, HT), (HX1, G - 4), (HX0, G - 4)], C_L, PART, j=.3, step=5)
    rect(p, HX0 + 4, HT + 4, HX0 + 8, G - 9, '#f27a5c')
    rect(p, HX0 + 9, HT + 6, HX1 - 5, HT + 22, C_D)
    rect(p, HX0 + 11, HT + 8, HX1 - 7, HT + 20, GL); rect(p, HX0 + 11, HT + 8, HX0 + 17, HT + 20, '#eaf6ff')
    # پایه با دو چرخ
    p.shape([(HX0 - 2, G - 8), (HX1 + 2, G - 8), (HX1 + 2, G), (HX0 - 2, G)], C_D, PART, j=.15, step=6)
    for wx in (HX0 + 7, HX1 - 7):
        p.shape(ell(wx, G + 1, 6, 6, 0, 360, 16), '#5c6bb0', INNER, j=.2, step=99, clip=False); disc(p, wx, G + 1, 2, YEL)


def build(out=None):
    p = Pen('harbor_crane', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-44, G + 6, 30); p.foot_tip(-56, G + 4, 6); p.foot_tip(-32, G + 4, 6)
    p.tipshadow(18, G, 20); p.foot_tip(18, G - 2, 8)
    machine(p)
    container(p, 6, -8, 30, G, OR, OR_L, OR_D, 3)                              # کانتینر روی زمین
    with layer(p, 'hook'): hook(p)
    jib(p)
    return p


STAND = None     # خودکار: find_stand
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/v2/harbor_crane'

if __name__ == '__main__':
    p = build()
    offs = [p.V(o) for o in [(0, 0), (0, 2), (0, 4), (0, 6)]]
    r = finish(p, 'harbor_crane', STAND, motion={'hook': dict(offsets=offs)}, out=HERE / 'out', shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(offsets=offs, note='کابل+قلاب+بندها+کانتینر بالا/پایین ۰ تا +۶؛ بالای کابل پشت بازوی ثابت')
    (HERE / 'out' / 'harbor_crane.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'inside': r['inside'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
