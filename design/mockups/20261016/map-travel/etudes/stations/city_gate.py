#!/usr/bin/env python3
"""ایستگاه M01 «دروازهٔ شهر» (سکوی city).
طرح قطعه‌به‌قطعه (واحد symbol، محور دروازه CX=-30، کف BASE=7):
 ۱ سایهٔ تماس: بیضی rx 40 زیر کف.
 ۲ دیوار (سنگ): مستطیل CX±24 از y=7 تا -50، OUT؛ سایه تیز راست، نور چپ، کرسی تیره پایین.
 ۳ دهانهٔ طاقی: مستطیل CX±18 از کف تا y=-20 + نیم‌دایرهٔ r=18 (بالای طاق y=-38)؛ داخل بنفش-قهوه‌ای تیره، INNER.
 ۴ لنگهٔ چپ (ثابت، بسته): چوب قهوه‌ای CX-17..CX، با قوس؛ INNER؛ یک نوار روشن، دستگیره زرد.
 ۵ لنگهٔ راست (لایهٔ node_city_gate_leaf): نیمه‌باز، ذوزنقهٔ باریک چوب CX+8..CX+17 (لولا روی CX+17).
 ۶ دو برجک (سنگ): CX-36..CX-18 و CX+18..CX+36 تا y=-70؛ سایه/نور؛ بالای هرکدام سربند تیره 6 بلند؛ شکاف پنجرهٔ تخت تیره.
 ۷ سنگ کلید: مستطیل تخت روشن بالای طاق.
سه خانواده: سنگ کرم (پایه/روشن/تیره)، چوب قهوه‌ای (پایه/روشن/تیره)، داخل دهانه تیره. بدون چرخ‌دنده/موتور/دودکش.
حرکت: لنگهٔ راست یک‌بار هنگام رسیدن از بسته تا حالت ایستا (نیمه‌باز)، بدون بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/city_gate'

S_B, S_L, S_D = '#f3dfb0', '#fff7de', '#cfb078'       # سنگ
W_B, W_L, W_D = '#a8672f', '#d9a463', '#6e3f18'       # چوب
HOLE = '#5a3d6e'                                      # داخل دهانه
YEL = '#ffd84d'

CX, BASE = -30, 7
TT = -72           # بالای برجک
WT = -50           # بالای دیوار میانی
OR = 18            # نیم‌پهنای دهانه
OY = -16           # مرکز قوس
TW = 34            # نیم‌پهنای کل


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def R(x0, y0, x1, y1): return [(CX + x0, y0), (CX + x1, y0), (CX + x1, y1), (CX + x0, y1)]


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def build():
    p = Pen('city_gate', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.0, 4, 0)
    p.tipshadow(CX + 4, BASE + 3, 38); p.foot_tip(CX - 22, BASE + 2, 10); p.foot_tip(CX + 22, BASE + 2, 10)
    # بدنهٔ سنگی یک‌تکه: دو برجک + دیوار میانی
    body = [(CX - TW, BASE), (CX + TW, BASE), (CX + TW, TT), (CX + OR, TT), (CX + OR, WT), (CX - OR, WT), (CX - OR, TT), (CX - TW, TT)]
    p.shape(body, S_B, OUT, j=.1, step=6)
    poly(p, R(-TW + 4, TT + 10, -TW + 7.5, BASE - 7), S_L)                    # نور برج چپ
    poly(p, R(OR + 4, TT + 10, OR + 7.5, BASE - 7), S_L)                      # نور برج راست
    poly(p, R(TW - 6.5, TT + 8, TW - 1, BASE - 1), S_D)                       # سایهٔ تیز راست
    poly(p, R(-OR, WT + 8, OR, WT + 4), S_D)                                  # زیر لبهٔ دیوار (نوار تیره)
    poly(p, R(-TW + 1, TT + 1, -OR - 1, TT + 7), S_D)                         # سربند برج چپ
    poly(p, R(OR + 1, TT + 1, TW - 1, TT + 7), S_D)                           # سربند برج راست
    poly(p, R(-TW + 1, BASE - 5, TW - 1, BASE - 1), S_D)                      # کرسی
    p.stroke(body, OUT, j=.1, step=6)
    # شکاف پنجرهٔ برجک‌ها (تخت)
    for cx in (-(TW + OR) / 2, (TW + OR) / 2):
        poly(p, R(cx - 2, TT + 22, cx + 2, TT + 40), HOLE)
    # دهانهٔ طاقی
    hole = [(CX - OR, BASE - 1), (CX + OR, BASE - 1), (CX + OR, OY)] + ell(CX, OY, OR, OR, 0, -180, 14) + [(CX - OR, OY)]
    p.shape(hole, HOLE, INNER, j=.08, step=6, clip=False)
    # لنگهٔ چپ (ثابت، بسته)
    L = [(CX - OR + 1, BASE - 1), (CX - 1, BASE - 1), (CX - 1, OY - OR + 1)] + ell(CX, OY, OR - 1, OR - 1, -90, -180, 8)[1:] + [(CX - OR + 1, OY)]
    p.shape(L, W_B, INNER, j=.08, step=6, clip=False)
    poly(p, R(-13, BASE - 4, -10, -22), W_L)
    disc(p, CX - 4.5, -3, 2, YEL)
    # لنگهٔ راست (نیمه‌باز)
    with layer(p, 'leaf'):
        p.shape([(CX + 6, BASE - 1), (CX + OR - 1, BASE - 1), (CX + OR - 1, -22), (CX + 6, -29)], W_B, INNER, j=.08, step=6, clip=False)
        poly(p, [(CX + 12.5, BASE - 4), (CX + 15, BASE - 4), (CX + 15, -22), (CX + 12.5, -24)], W_L)
        disc(p, CX + 9.5, -3, 1.8, YEL)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'city_gate', STAND, motion={'leaf': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_city_gate_leaf': dict(
        type='scaleX افقی حول لولا (لبهٔ راست لنگه)', hinge_x_symbol=round(p.X((CX + OR - 1, 0))[0], 1), scale_from=1.5, scale_to=1.0,
        duration_s=1.4, easing='ease-out', loop=False,
        start='لنگهٔ راست بسته (پهنای ۱۷ واحد، تمام نیمهٔ راست دهانه)', end='حالت ایستا (پایان): نیمه‌باز؛ پهنای ظاهری ۱۱ واحد (فشردگی افقی ≈ ۰٫۶۵؛ در نمای رو‌به‌رو باز شدنی بیش از ۲۵° دیده می‌شود تا خوانا باشد)',
        note='فقط هنگام رسیدن، یک‌بار؛ لنگهٔ چپ و برجک‌ها ثابت؛ لنگه فیگور را نمی‌پوشاند؛ بدون حلقهٔ بیکار.'),
        'reduced_motion': 'نیمه‌باز (حالت ایستا)'}
    (OUTD / 'city_gate.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
