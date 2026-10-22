#!/usr/bin/env python3
"""ایستگاه E01 «آسیاب بادی» (سرزمین مزرعه)، بازسازی کامل طبق docs/STATION_SYMBOL_CRAFT_FA.md بخش ۵.
سه خانوادهٔ رنگ جدا: برج کرم روشن، سقف قهوه‌ای تیره، چهار پرهٔ پارچه‌ای قرمز (ضربدر ×) حول محور.
لایهٔ دوّار: node_windmill_blades (مرکز = محور). بدون حلقهٔ بیکار، بدون عامل نیرو."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/windmill'

# برج (سنگ): پایه/روشن/تیره
T_B, T_L, T_D = '#f7ecd0', '#fffaf0', '#dcc896'
# سقف (چوب تیره)
R_B, R_L, R_D = '#7a4220', '#9c5c2c', '#55290f'
# پره (پارچه)
C_B, C_L, C_D = '#ef6a4a', '#ffb59c', '#c9452c'
SPAR = '#7a4a1f'; DOOR = '#b77a3a'; DOOR_D = '#7a4a1f'; GLASS = '#cfeaff'; YEL = '#ffd84d'

CX, BASE = -30, 7
TOP = -78                      # بالای برج
ROOF_B, ROOF_T = -73, -109      # کف و بالای سقف
HUB = (CX, -88)
R = 46                         # طول پارچه از محور
CW = 19                        # پهنای پارچه
STATIC = (-135, -45, 45, 135)  # ضربدر ×


def hw(y): return 26 - 9 * (BASE - y) / (BASE - TOP)       # نیم‌پهنای برج


def rw(y): return 38 - 22 * (ROOF_B - y) / (ROOF_B - ROOF_T)   # نیم‌پهنای سقف


def poly(p, pts, col, op=1):
    """چندضلعی تیز و تخت (بدون گردشدن گوشه‌ها)."""
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, (' stroke="%s" stroke-width=".6" stroke-linejoin="round"' % col) if op == 1 else ' opacity="%s"' % op))   # حاشیهٔ هم‌رنگ: درز مویی بین چندضلعی‌ها نماند


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def build(out=OUTD):
    p = Pen('windmill', 'farm'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.0, 8, 0)
    p.tipshadow(CX + 4, BASE + 3, 28); p.foot_tip(CX + 2, BASE + 2, 20)
    # ۱) برج
    body = [(CX - hw(BASE), BASE), (CX + hw(BASE), BASE), (CX + hw(TOP), TOP), (CX - hw(TOP), TOP)]
    p.shape(body, T_B, OUT, j=.15, step=8)
    poly(p, [(CX - hw(-70) + 5, -70), (CX - hw(-70) + 8.5, -70), (CX - hw(-2) + 8.5, -2), (CX - hw(-2) + 5, -2)], T_L)          # نور
    poly(p, [(CX + 5, TOP + 3), (CX + hw(TOP), TOP + 3), (CX + hw(BASE) - 1, BASE), (CX + 5, BASE)], T_D)                         # سایهٔ تیز راست
    poly(p, [(CX - hw(2), 2), (CX + hw(2), 2), (CX + hw(BASE), BASE), (CX - hw(BASE), BASE)], T_D)                                # کرسی سنگی
    p.stroke(body, OUT, j=.15, step=8)
    # ۲) در (یک در بزرگ با قوس)
    p.shape([(CX - 8, BASE - 1), (CX + 8, BASE - 1), (CX + 8, -3)] + ell(CX, -3, 8, 8, 0, -180, 12) + [(CX - 8, -3)], DOOR, INNER, j=.08, step=99, clip=False)
    poly(p, [(CX - 5, BASE - 3), (CX - 2.5, BASE - 3), (CX - 2.5, -4), (CX - 5, -4)], '#d9a463')
    disc(p, CX + 4, 0, 1.9, YEL)
    # ۳) پنجرهٔ گرد کوچک
    p.shape(ell(CX, -27, 5.5, 5.5, 0, 360, 16), GLASS, INNER, j=.05, step=99, clip=False)
    poly(p, [(CX - 2.5, -29.5), (CX - 0.5, -29.5), (CX - 0.5, -27.5), (CX - 2.5, -27.5)], '#ffffff')
    # ۴) سقف
    roof = [(CX - 38, ROOF_B), (CX + 38, ROOF_B), (CX + 16, ROOF_T), (CX - 16, ROOF_T)]
    p.shape(roof, R_B, PART, j=.15, step=8)
    poly(p, [(CX - rw(-104) + 4, -104), (CX - rw(-104) + 7.5, -104), (CX - rw(-77) + 7.5, -77), (CX - rw(-77) + 4, -77)], R_L)      # نور
    poly(p, [(CX + 6, ROOF_T), (CX + 16, ROOF_T), (CX + 38, ROOF_B), (CX + 22, ROOF_B)], R_D)                                         # سایهٔ تیز راست
    poly(p, [(CX - 38, ROOF_B - 4), (CX + 38, ROOF_B - 4), (CX + 38, ROOF_B), (CX - 38, ROOF_B)], R_D)                              # لبهٔ پیش‌آمده
    p.stroke(roof, PART, j=.15, step=8)
    # ۵) پره‌ها (لایهٔ دوّار): اول همهٔ پارچه‌ها، سپس تیرک‌ها
    with layer(p, 'blades'):
        for a in STATIC:
            f = rot(HUB[0], HUB[1], a)
            cloth = TP(f, [(8, 0), (R, 0), (R, -CW), (8, -CW)])
            p.raw('<polygon points="%s" fill="%s" class="eo" stroke-width="%s" stroke-linejoin="miter" stroke-miterlimit="6"/>' % (
                ' '.join('%.1f,%.1f' % q for q in p.X(cloth)), C_B, INNER))
            poly(p, TP(f, [(16, -11), (R - 9, -11), (R - 9, -14), (16, -14)]), C_L)             # نوار روشن
            poly(p, TP(f, [(R - 7, -CW + 3), (R - 4, -CW + 3), (R - 4, -9), (R - 7, -9)]), C_D)   # لبهٔ تیره
        for a in STATIC:
            f = rot(HUB[0], HUB[1], a)
            p.ln(f((4, -5.5)), f((R - 5, -5.5)), PART, SPAR, j=0)                                        # تیرک (یک‌بار)
    p.shape(ell(HUB[0], HUB[1], 6.5, 6.5, 0, 360, 16), SPAR, PART, j=.05, step=99, clip=False)     # کلاهک محور
    disc(p, HUB[0], HUB[1], 2, YEL)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    hm = p.X(HUB)
    r = finish(p, 'windmill', STAND, motion={'blades': dict(rotate=hm)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_windmill_blades': dict(center=[round(v, 1) for v in hm], dir='cw (جهت عقربه‌های ساعت)', turns=3,
                                                     note='چهار پرهٔ پارچه‌ای حول کلاهک محور؛ حالت ایستا = ضربدر ×؛ چرخش آهسته فقط هنگام رسیدن؛ بدون حلقهٔ بیکار.'),
                         'reduced_motion': 'پره‌ها ثابت در حالت ضربدر ×'}
    (OUTD / 'windmill.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
