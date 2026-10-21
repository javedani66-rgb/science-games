#!/usr/bin/env python3
"""ایستگاه E01 «آسیاب بادی» (سرزمین مزرعه): برج مخروطی گچی-گرم با در و یک پنجره، سقف کلاهی قرمز-قهوه‌ای،
چهار پرهٔ پارچه‌ای پهن (قرمز، ضربدر ×) حول محور. لایهٔ دوّار: node_windmill_blades. بدون حلقهٔ بیکار، بدون عامل نیرو."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit3/windmill'

TOWER = '#f1e9da'; TOWER_D = '#cdbfa6'; ROOF = '#b8432f'; ROOF_D = '#8a2f20'
CLOTH = '#e8503a'; CLOTH_D = '#b8392a'; SPAR = '#7a4a22'; DOOR = '#8a5a26'; WIN = '#8cc6ea'; STONE = '#d7c9ae'
CX, BASE = -28, 7              # محور برج، خط کف
HW_B, HW_T, TOP = 31, 19, -50   # نیم‌پهنای کف/بالا، y بالای برج
HUB = (CX, -72)
R = 36                           # طول پره از محور
STATIC = (-135, -45, 45, 135)    # ضربدر (×)؛ مرکز برج برای پنجره باز می‌ماند


def blade(a):
    """یک پره: تیرک چوبی + پارچهٔ پهن کنار آن (نقاط در قاب محلی، چرخیده حول محور)."""
    f = rot(HUB[0], HUB[1], a)
    cloth = [(13, 0), (R, 0), (R, -19), (13, -19)]
    return f, cloth


def build(out=OUTD):
    p = Pen('windmill', 'farm'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.tipshadow(CX + 2, BASE + 8, 40)
    # برج مخروطی
    p.shape([(CX - HW_B, BASE), (CX + HW_B, BASE), (CX + HW_T, TOP), (CX - HW_T, TOP)], TOWER, OUT, j=.3, step=8)
    p.fill([(CX + 10, TOP + 2), (CX + HW_T, TOP), (CX + HW_B, BASE), (CX + 12, BASE)], TOWER_D)   # نیم‌سایهٔ راست
    for y in (-36,):                                      # دو درز افقی منظم
        k = (BASE - y) / (BASE - TOP); w = HW_B + (HW_T - HW_B) * k
        p.ln((CX - w + 3, y), (CX + w - 3, y), INNER, STONE, j=.1)
    # در و پنجره
    p.shape([(CX - 7, BASE - 1), (CX + 7, BASE - 1), (CX + 7, BASE - 18), (CX - 7, BASE - 18)], DOOR, PART, j=.2, step=99)
    p.shape(ell(CX, BASE - 18, 7, 5, 180, 360, 10) + [(CX + 7, BASE - 18), (CX - 7, BASE - 18)], DOOR, PART, j=.2, step=99)
    p.shape([(CX - 7, -26), (CX + 7, -26), (CX + 7, -14), (CX - 7, -14)], WIN, PART, j=.2, step=99)
    # سقف کلاهی
    p.shape([(CX - 25, TOP + 3), (CX + 25, TOP + 3), (CX + 7, -82), (CX - 7, -82)], ROOF, OUT, j=.3, step=8)
    p.fill([(CX + 6, TOP + 2), (CX + 25, TOP + 3), (CX + 7, -82), (CX + 2, -82)], ROOF_D)
    # پره‌ها (لایهٔ دوّار)
    with layer(p, 'blades'):
        for a in STATIC:
            f, cl = blade(a)
            p.ln(f((8, 0)), f((R, 0)), PART, SPAR, j=.05)
            p.raw('<polygon points="%s" fill="%s" stroke="%s" stroke-width="5.8" stroke-linejoin="miter" stroke-miterlimit="6"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(TP(f, cl))), CLOTH, NAVY))
            p.ln(f((12, 0)), f((R, 0)), PART, SPAR, j=.05)
    p.shape(ell(HUB[0], HUB[1], 6.5, 6.5, 0, 360, 16), SPAR, PART, j=.1, step=99)   # کلاهک محور (ثابت)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    hm = p.X(HUB)
    r = finish(p, 'windmill', STAND, motion={'blades': dict(rotate=hm)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_windmill_blades': dict(center=[round(v, 1) for v in hm], dir='cw', note='چهار پرهٔ پارچه‌ای حول محور برج؛ وضعیت ایستا = ضربدر ×؛ چرخش آهسته هنگام رسیدن؛ بدون حلقهٔ بیکار.'),
                         'reduced_motion': 'پره‌ها ثابت در حالت ضربدر ×'}
    (OUTD / 'windmill.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
