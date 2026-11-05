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

XF = (0.92, 6.0, 2.0)
C_T = '#ff9a6c'; C_L = '#e0553a'; C_D = '#9c2f1c'; C_H = '#ffc7a6'
GL = '#cfeaff'; GL_D = '#6fa8dc'
CNT = '#4fae4a'; CNT_L = '#8fd46f'; CNT_D = '#1f6b2e'
OR = '#ff9b2f'; OR_L = '#ffc56b'; OR_D = '#b4620f'
YEL = '#ffd84d'
G = 12                          # خط زمین
HX0, HX1, HT = -58, -28, -30    # ماشین‌خانه
MX0, MX1 = -52, -38             # برج
JX0, JX1, JT, JB = -62, 30, -108, -92   # بازوی ضخیم
BX = 4                         # محور کابل
HB0 = -74                       # بالای بلوک قلاب
CT, CH, CWD = -50, 20, 26       # کانتینر آویزان


from r6lib import extrude, poly, rect, circ        # حجم ¾ با سه پلهٔ رنگ؛ بین وجه‌ها خط نیست (قاعده ۱۴)
from shapely.geometry import Polygon
from shapely.ops import unary_union
HERO_W, HERO_T = 3.6, 2.8                            # خط دور قهرمان / قطعهٔ فرعی (قاعده ۲۴)
D_B = (14, -9)                                       # عمق بدنهٔ جرثقیل
B_F, B_T, B_S = '#ff8f5c', '#ffd2ae', '#b4401f'      # بدنه: جلو / رو / پهلو
CNT_F, CNT_T, CNT_S = '#4fae4a', '#a8e28a', '#1f6b2e'
OR_F, OR_T, OR_S = '#ff9b2f', '#ffd08a', '#b4620f'
WHEEL = '#5c6bb0'; CWT = '#8f9ad6'; CWT_T = '#c6cdf2'; CWT_S = '#5560a8'


def box(x0, y0, x1, y1): return Polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def crane_body(p):
    """ماشین‌خانه + برج + بازو = یک شکل (اجتماع)؛ یک‌بار بیرون‌کشیده می‌شود، بدون خط بین اجزا (قاعده ۱۸)."""
    u = unary_union([box(HX0, HT, HX1, G - 2), box(MX0, JT, MX1, HT + 6), box(JX0, JT, JX1, JB)]).buffer(0)
    prof = list(u.exterior.coords)[:-1]
    extrude(p, prof, D_B, B_F, B_T, B_S, mid=B_F, sw=HERO_W, sw_in=0)
    rect(p, JX0 + 4, JT + 3.5, JX1 - 6, JT + 7, '#ffe6cc', .95)                      # نوار برق بازو
    rect(p, MX0 + 3, JB + 5, MX0 + 6, HT - 2, '#ffb48a')                              # نوار برق برج
    # پنجرهٔ بزرگ ماشین‌خانه (قطعهٔ جدا: خط نازک)
    p.shape([(HX0 + 6, HT + 7), (HX1 - 6, HT + 7), (HX1 - 6, HT + 24), (HX0 + 6, HT + 24)], GL, 2.4, j=.05, step=99, clip=False)
    rect(p, HX0 + 8.5, HT + 9.5, HX0 + 13, HT + 21.5, '#eaf6ff')
    # وزنهٔ تعادل زیر سر عقبی بازو (قطعهٔ جدا)
    extrude(p, [(JX0 + 2, JB + 1), (JX0 + 18, JB + 1), (JX0 + 18, JB + 17), (JX0 + 2, JB + 17)], (6, -4), CWT, CWT_T, CWT_S, sw=HERO_T, sw_in=0)


def wheels(p):
    """D185: دو چرخ هم‌اندازه و هم‌تراز، روی خط زمین، زیر پایهٔ جلوی ماشین‌خانه (یکی نزدیک هر سر)."""
    r_ = 6.2
    for wx in (HX0 + 6.5, HX1 - 6.5):
        wy = G - r_
        p.shape(ell(wx, wy, r_, r_, 0, 360, 24), WHEEL, HERO_T, j=.05, step=99, clip=False)
        circ(p, wx, wy, r_ * .55, '#c6cdf2'); circ(p, wx, wy, 2.2, YEL)


def hook(p):
    """بخش متحرک: کابل، بلوک قلاب، دو بند و کانتینر آویزان."""
    p.ln((BX, JB), (BX, HB0), 2.6, '#5c3a10', j=0)
    p.probes.append(('کابل (جزء)', 2.6, p.X((BX, (JB + HB0) / 2)), (1, 0), '#5c3a10'))
    p.ln((BX - 4, HB0 + 11), (BX - 10, CT), 1.8, '#5c3a10', j=0)
    p.ln((BX + 4, HB0 + 11), (BX + 10, CT), 1.8, '#5c3a10', j=0)
    p.shape([(BX - 7, HB0), (BX + 7, HB0), (BX + 7, HB0 + 11), (BX - 7, HB0 + 11)], C_D, HERO_T, j=.05, step=99, clip=False)
    circ(p, BX, HB0 + 5.5, 2.2, YEL)
    extrude(p, [(BX - CWD / 2, CT), (BX + CWD / 2, CT), (BX + CWD / 2, CT + CH), (BX - CWD / 2, CT + CH)], (8, -5), CNT_F, CNT_T, CNT_S, sw=HERO_T, sw_in=0)
    for i in (-1, 1): rect(p, BX + i * 6 - 1.2, CT + 4, BX + i * 6 + 1.2, CT + CH - 3, '#2f7f36')     # آج‌های کانتینر (پلهٔ رنگ)


def ground_container(p):
    p.tipshadow(22, G + 2, 18)
    extrude(p, [(6, -8), (30, -8), (30, G), (6, G)], (9, -6), OR_F, OR_T, OR_S, sw=HERO_T, sw_in=0)
    for i in (1, 2): rect(p, 6 + i * 8 - 1.2, -4, 6 + i * 8 + 1.2, G - 3, '#d9780f')


def build(out=None):
    p = Pen('harbor_crane', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-44, G + 6, 30); p.foot_tip(-44, G + 4, 6)
    with layer(p, 'hook'): hook(p)
    crane_body(p); ground_container(p)   # D185: بدون چرخ (دستور مالک)
    return p


STAND = None     # خودکار: find_stand
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/harbor_crane'

if __name__ == '__main__':
    p = build()
    offs = [p.V(o) for o in [(0, 0), (0, 2), (0, 4), (0, 6)]]
    r = finish(p, 'harbor_crane', STAND, motion={'hook': dict(offsets=offs)}, out=HERE / 'out', shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(offsets=offs, note='کابل+قلاب+بندها+کانتینر بالا/پایین ۰ تا +۶؛ بالای کابل پشت بازوی ثابت')
    (HERE / 'out' / 'harbor_crane.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'inside': r['inside'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
