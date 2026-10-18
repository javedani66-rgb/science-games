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

XF = (1.0, 4.0, -4.0)
C_T = '#ff9a6c'; C_L = '#e0553a'; C_D = '#9c2f1c'; C_H = '#ffc7a6'
GL = '#cfeaff'; GL_D = '#6fa8dc'
CNT = '#4fae4a'; CNT_L = '#8fd46f'; CNT_D = '#1f6b2e'
OR = '#ff9b2f'; OR_L = '#ffc56b'; OR_D = '#b4620f'
YEL = '#ffd84d'
G = 12                          # خط زمین
HX0, HX1, HT = -58, -26, -34    # ماشین‌خانه
MX0, MX1 = -54, -38             # دکل
PIV = (-46, -100)               # لولای بازو
TIP = (34, -112)
BX = -6                         # محور طناب
CT, CH, CWD = -40, 22, 28


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
    """بخش متحرک: طناب، قلاب، بندها و کانتینر آویزان."""
    p.ln((BX, TIP[1] + 4), (BX, CT - 12), PART, '#8a5f0c', j=0)
    p.probes.append(('طناب (جزء)', PART, p.X((BX, -70)), (1, 0), '#8a5f0c'))
    p.ln((BX, CT - 12), (BX - CWD / 2 + 3, CT), INNER, '#8a5f0c', j=0)
    p.ln((BX, CT - 12), (BX + CWD / 2 - 3, CT), INNER, '#8a5f0c', j=0)
    p.shape([(BX - 6, CT - 18), (BX + 6, CT - 18), (BX + 6, CT - 9), (BX - 6, CT - 9)], C_D, PART, j=.1, step=5, clip=False)     # بلوک قلاب
    disc(p, BX, CT - 13.5, 2, YEL)
    container(p, BX - CWD / 2, CT, BX + CWD / 2, CT + CH, CNT, CNT_L, CNT_D, 5, clip=False)
    p.ln((BX - 10, CT + CH - 4), (BX + 10, CT + CH - 4), INNER, CNT_D, j=0, probe='تختهٔ کانتینر (داخلی)')


def jib(p):
    """بازوی خرپایی: بال بالا و پایین، ضلعی‌های قطری و وزنهٔ تعادل؛ پشت لایهٔ متحرک ثابت می‌ماند."""
    (x0, y0), (x1, y1) = PIV, TIP
    L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L; nx, ny = -uy, ux
    HW = 10
    top = lambda t, s: (x0 + ux * t + nx * s * HW, y0 + uy * t + ny * s * HW)
    p.shape([top(-16, 1), top(L, 1), top(L, -1), top(-16, -1)], C_T, PART, j=.3, step=7)
    rect  # (حفظ نام)
    flat(p, [top(-12, -.55), top(L - 4, -.55), top(L - 4, -.15), top(-12, -.15)], C_H)         # نور بال بالا
    n = 9
    for i in range(n):                                                          # ضلعی‌های خرپا (راست و موازی)
        a, b = -4 + (L + 2) * i / n, -4 + (L + 2) * (i + 1) / n
        p.ln(top(a, .8), top(b, -.8) if i % 2 == 0 else top(b, .8), INNER, C_D, j=0)
        if i % 2 == 0: p.ln(top(b, -.8), top(b, .8), INNER, C_D, j=0)
    p.shape([(x0 - 16, y0 - 8), (x0 - 4, y0 - 8), (x0 - 4, y0 + 14), (x0 - 16, y0 + 14)], C_D, PART, j=.2, step=6)       # وزنهٔ تعادل
    rect(p, x0 - 13, y0 - 5, x0 - 7, y0 - 2, '#d2563a')
    p.shape(ell(x0, y0, 8, 8, 0, 360, 20), C_D, PART, j=.1, step=99, clip=False)               # لولا
    disc(p, x0, y0, 3, YEL)
    p.shape([(TIP[0] - 4, TIP[1] - 5), (TIP[0] + 5, TIP[1] - 3), (TIP[0] + 5, TIP[1] + 8), (TIP[0] - 4, TIP[1] + 8)], C_D, PART, j=.1, step=99, clip=False)  # سر بازو


def machine(p):
    # دکل
    p.shape([(MX0, PIV[1]), (MX1, PIV[1]), (MX1, HT + 4), (MX0, HT + 4)], C_T, PART, j=.3, step=7)
    rect(p, MX0 + 3, PIV[1] + 8, MX0 + 6.5, HT, C_H)                               # نور چپ دکل
    for y in range(-92, -36, 14):                                                # پلکان/نردبان
        p.ln((MX0 + 4, y), (MX1 - 4, y), INNER, C_D, j=0)
    # ماشین‌خانه
    p.shape([(HX0, HT), (HX1, HT), (HX1, G - 4), (HX0, G - 4)], C_L, PART, j=.3, step=5)
    rect(p, HX0 + 3, HT + 3, HX0 + 7, G - 8, '#f27a5c')                           # نور چپ
    rect(p, HX1 - 7, HT + 3, HX1 - 3, G - 8, '#b83f27')                           # سایهٔ راست
    for wx in (HX0 + 8, HX0 + 21):                                               # دو پنجره با قاب و نور
        rect(p, wx - 1.5, HT + 5.5, wx + 12.5, HT + 21.5, C_D)
        rect(p, wx, HT + 7, wx + 11, HT + 20, GL); rect(p, wx, HT + 7, wx + 5, HT + 20, '#eaf6ff'); rect(p, wx, HT + 17, wx + 11, HT + 20, GL_D)
    rect(p, HX0 + 9, HT + 26, HX1 - 9, G - 8, C_D)                                # در
    rect(p, HX0 + 11, HT + 28, HX1 - 11, G - 10, '#c9411f')
    # پایهٔ تیره با چرخ‌ها
    p.shape([(HX0 - 2, G - 8), (HX1 + 2, G - 8), (HX1 + 2, G), (HX0 - 2, G)], C_D, PART, j=.15, step=6)
    for wx in (HX0 + 6, HX1 - 6):
        p.shape(ell(wx, G + 1, 6, 6, 0, 360, 16), '#5c6bb0', INNER, j=.2, step=99, clip=False); disc(p, wx, G + 1, 2, YEL)


def build(out=None):
    p = Pen('harbor_crane', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-40, G + 6, 34); p.foot_tip(-56, G + 4, 6); p.foot_tip(-32, G + 4, 6)
    p.tipshadow(-5, G, 20); p.foot_tip(-5, G - 2, 8)
    machine(p)
    container(p, -20, -6, 8, G, OR, OR_L, OR_D, 4)                              # کانتینر روی زمین
    with layer(p, 'hook'): hook(p)
    jib(p)
    return p


STAND = None     # خودکار: find_stand
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/v2/harbor_crane'

if __name__ == '__main__':
    p = build()
    offs = [p.V(o) for o in [(0, 0), (0, 2), (0, 4), (0, 6)]]
    r = finish(p, 'harbor_crane', STAND, motion={'hook': dict(offsets=offs)}, out=HERE / 'out', shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(offsets=offs, note='طناب+قلاب+بندها+کانتینر بالا/پایین ۰ تا +۶؛ بالای طناب پشت بازوی ثابت')
    (HERE / 'out' / 'harbor_crane.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'inside': r['inside'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
