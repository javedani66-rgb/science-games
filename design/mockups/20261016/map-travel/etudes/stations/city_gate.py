#!/usr/bin/env python3
"""ایستگاه M01 «دروازهٔ شهر» (سکوی city) — دور ۵ (بازطراحی طبق دستور مدیر هنری: بزرگ، وسط، سیلوئت روشن).
طرح قطعه‌به‌قطعه (واحد symbol، محور CX=0 = مرکز سکو، کف BASE=7):
 ۱ بدنهٔ سنگی یک‌تکه: دو برج (CX±29..54) تا y=-72 و دیوار میانی تا y=-50؛ سنگ کرم (پایه/روشن/تیره)، OUT؛ نور چپ، سایهٔ تیز راست، کرسی.
 ۲ سه دندانهٔ درشت روی دیوار (۱۴ پهنا، y -50..-62)، هر دندانه PART.
 ۳ دهانهٔ طاقی بزرگ (CX±19، قوس تا y=-35)، داخل بنفش تیره؛ لنگهٔ چپ چوبی بسته؛ دو میخ زرد.
 ۴ لنگهٔ راست (لایهٔ node_city_gate_leaf): چوب، لولا روی CX+18؛ حالت ایستا = نیمه‌باز.
 ۵ دو سقف مخروطی قرمز-نارنجی (پهنا ۳۸، ارتفاع ۳۶) روی دو برج؛ ۶ پرچم کوچک زرد روی برج راست.
 ۷ دو شکاف پنجرهٔ برج (تخت تیره).
سه خانواده: سنگ کرم، سقف قرمز-نارنجی، چوب قهوه‌ای (+پرچم زرد). بدون چرخ‌دنده/موتور.
حرکت: لنگهٔ راست یک‌بار هنگام رسیدن از بسته تا حالت ایستا (نیمه‌باز)، بدون بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/city_gate'

S_B, S_L, S_D = '#f3dfb0', '#fff7de', '#cfb078'       # سنگ
W_B, W_L, W_D = '#a8672f', '#d9a463', '#6e3f18'       # چوب
R_B, R_L, R_D = '#e0502e', '#ff9a6a', '#a8301a'       # سقف
HOLE = '#3a2a5a'
YEL = '#ffd84d'; FLAG = '#ffd84d'

CX, BASE = 0, 7
TO, TI = 54, 29            # بیرون/درون برج
TT, WT, MT = -76, -50, -67  # بالای برج، دیوار، دندانه
OR, OY = 22, -14           # نیم‌پهنای دهانه، مرکز قوس
ROOF_B, ROOF_T, ROOF_W = -72, -108, 19


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def R(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def build():
    p = Pen('city_gate', 'city'); pad(p, line=((50, 30), (70, 27)), tri=((36, -22), (74, 6)), dot=(68, -14)); p.xf = (1.0, 0, 0)
    p.tipshadow(CX + 3, BASE + 3, 50); p.foot_tip(CX - 42, BASE + 2, 12); p.foot_tip(CX + 42, BASE + 2, 12)
    # ۲) دندانه‌ها (پشت دیوار)
    for a, b in ((-TI, -TI + 14), (-7, 7), (TI - 14, TI)):
        t = R(a, MT, b, WT + 3)
        p.shape(t, S_B, PART, j=.1, step=6, clip=False)
        poly(p, R(a + 3.5, MT + 3.5, a + 6.5, WT - 1), S_L)
        poly(p, R(b - 5.5, MT + 4, b - 2.5, WT - 1), S_D, .9)
    # ۱) بدنه: دو برج + دیوار
    body = [(CX - TO, BASE), (CX + TO, BASE), (CX + TO, TT), (CX + TI, TT), (CX + TI, WT), (CX - TI, WT), (CX - TI, TT), (CX - TO, TT)]
    p.shape(body, S_B, OUT, j=.1, step=6)
    poly(p, R(-TO + 4, TT + 6, -TO + 7.5, BASE - 8), S_L)                       # نور برج چپ
    poly(p, R(TI + 4, WT + 6, TI + 7.5, BASE - 8), S_L)                          # نور برج راست
    poly(p, R(TO - 7.5, TT + 6, TO - 1, BASE - 1), S_D)                          # سایهٔ تیز راست
    poly(p, R(-TI - 7.5, TT + 6, -TI - 1, BASE - 1), S_D)                       # سایهٔ سمت راست برج چپ
    poly(p, R(-TI + 1, WT + 1, TI - 1, WT + 6), S_D)                              # لبهٔ بالای دیوار
    poly(p, R(-TO + 1, BASE - 5, TO - 1, BASE - 1), S_D)                          # کرسی
    p.stroke(body, OUT, j=.1, step=6)
    # ۷) شکاف پنجرهٔ برج‌ها
    for c in (-(TO + TI) / 2, (TO + TI) / 2):
        poly(p, R(c - 2.5, TT + 12, c + 2.5, TT + 32), HOLE)
    # ۳) دهانهٔ طاقی بزرگ
    hole = [(CX - OR, BASE - 1), (CX + OR, BASE - 1), (CX + OR, OY)] + ell(CX, OY, OR, OR, 0, -180, 16) + [(CX - OR, OY)]
    p.shape(hole, HOLE, INNER, j=.08, step=6, clip=False)
    # لنگهٔ چپ (بسته)
    L = [(CX - OR + 1, BASE - 1), (CX - 1, BASE - 1), (CX - 1, OY - OR + 1)] + ell(CX, OY, OR - 1, OR - 1, -90, -180, 8)[1:] + [(CX - OR + 1, OY)]
    p.shape(L, W_B, INNER, j=.08, step=6, clip=False)
    poly(p, R(-OR + 5, -16, -OR + 8.5, BASE - 5), W_L)
    disc(p, CX - 6, -4, 2.3, YEL)
    # ۴) لنگهٔ راست (نیمه‌باز)، لولا روی CX+OR-1
    with layer(p, 'leaf'):
        p.shape([(CX + 8, BASE - 1), (CX + OR - 1, BASE - 1), (CX + OR - 1, OY)] + ell(CX, OY, OR - 1, OR - 1, 0, -64, 8)[1:], W_B, INNER, j=.08, step=6, clip=False)
        poly(p, R(CX + 13, -16, CX + 16, BASE - 5), W_L)
        disc(p, CX + 12.5, -4, 2.1, YEL)
    # ۶) پرچم روی برج راست
    c = (TO + TI) / 2
    p.ln((c, ROOF_T + 3), (c, ROOF_T - 24), PART, W_D, j=0)
    fl = [(c - 1, ROOF_T - 25), (c + 24, ROOF_T - 17), (c - 1, ROOF_T - 9)]
    p.shape(fl, FLAG, INNER, j=.05, step=99, clip=False)
    # ۵) سقف‌های مخروطی
    for c in (-(TO + TI) / 2, (TO + TI) / 2):
        cone = [(c - ROOF_W, ROOF_B), (c + ROOF_W, ROOF_B), (c, ROOF_T)]
        p.shape(cone, R_B, PART, j=.1, step=6)
        poly(p, [(c + 1, ROOF_T + 6), (c + ROOF_W - 4, ROOF_B - 3), (c + 1, ROOF_B - 3)], R_D)
        poly(p, [(c - 3.5, ROOF_T + 14), (c - 1, ROOF_T + 14), (c - 9, ROOF_B - 7), (c - 11.5, ROOF_B - 7)], R_L)
        poly(p, R(c - ROOF_W + 3, ROOF_B - 5, c + ROOF_W - 3, ROOF_B - 1), R_D)
        p.stroke(cone, PART, j=.1, step=6)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'city_gate', STAND, motion={'leaf': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_city_gate_leaf': dict(
        type='scaleX افقی حول لولا (لبهٔ راست لنگه)', hinge_x_symbol=round(p.X((CX + OR - 1, 0))[0], 1), scale_from=1.5, scale_to=1.0,
        duration_s=1.4, easing='ease-out', loop=False,
        start='لنگهٔ راست بسته (پهنای ۱۸ واحد، تمام نیمهٔ راست دهانه)', end='حالت ایستا (پایان): نیمه‌باز؛ پهنای ظاهری ۱۲ واحد (فشردگی افقی ≈ ۰٫۶۷)',
        note='فقط هنگام رسیدن، یک‌بار؛ لنگهٔ چپ و برج‌ها ثابت؛ لنگه فیگور را نمی‌پوشاند؛ بدون حلقهٔ بیکار.'),
        'reduced_motion': 'نیمه‌باز (حالت ایستا)'}
    (OUTD / 'city_gate.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
