#!/usr/bin/env python3
"""M01 «دروازهٔ شهر» (سکوی city) — دور ۶ (R6): دروازهٔ طاقی سنگی ¾، نه قلعه.
طرح (واحد symbol، مرکز سکو x=0، کف y=6):
 ۱ بدنهٔ سنگی ¾: رو x=±54 تا y=-88، عمق D=16/E=9 (رویهٔ بالا روشن، رو میانی، وجه راست تیره)؛ سنگ کرم؛ ۳ درز سنگ روی هر ستون.
 ۲ حلقهٔ طاق روشن (r=33) و دهانهٔ تیرهٔ بنفش (r=25) با مرکز (0,-20).
 ۳ دو لنگهٔ چوبی باز و نیم‌طاق (چپ ثابت؛ راست = لایهٔ node_city_gate_leaf).
 ۴ تابلوی چوبی سردر (x ±26، y -81..-63) با نشان زرد.
 ۵ پرچم زرد کوچک روی گوشهٔ راست.  ۶ سنگ‌فرش جلوی دروازه.
حرکت: لنگهٔ راست یک‌بار از بسته (scaleX 1.6) تا حالت ایستا (باز)، بدون بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from station_kit import *
from g6h import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/city_gate'
S_B, S_L, S_D = '#f1dba8', '#fff6dc', '#c9a96c'
W_B, W_L, W_D = '#a8672f', '#e0a96a', '#6e3f18'
HOLE = '#3a2a5a'; YEL = '#ffd84d'; ROAD = '#d9cfb0'; ROAD_J = '#a89870'
BASE, TW, TOP, D, E = 6, 52, -80, 16, 9
OY, OR_, RR = -20, 24, 31


def build():
    p = Pen('city_gate', 'city'); pad(p, line=((50, 30), (70, 27)), tri=((36, -22), (74, 6)), dot=(68, -14)); p.xf = (1.0, 0, 3)
    p.tipshadow(4, BASE + 4, 58)
    p.foot_tip(-44, BASE + 2, 12); p.foot_tip(52, BASE + 2, 12)
    # ۶ سنگ‌فرش
    road = [(-34, BASE - 1), (34, BASE - 1), (50, 30), (-50, 30)]
    p.shape(road, ROAD, PART, j=.15, step=8, clip=False)
    for a, b in (((-12, BASE + 2), (-17, 28)), ((12, BASE + 2), (17, 28)), ((-44, 18), (44, 18))):
        p.ln(a, b, INNER, ROAD_J, j=.1)
    # ۱ بدنه
    sil = [(-TW, BASE), (TW, BASE), (TW + D, BASE - E), (TW + D, TOP - E), (-TW + D, TOP - E), (-TW, TOP)]
    p.shape(sil, S_B, OUT, j=.1, step=7)
    poly(p, [(-TW, TOP), (TW, TOP), (TW + D, TOP - E), (-TW + D, TOP - E)], S_L)                 # رویه
    poly(p, [(TW, TOP), (TW + D, TOP - E), (TW + D, BASE - E), (TW, BASE)], S_D)                  # وجه راست
    poly(p, R(-TW + 4, TOP + 6, -TW + 8, BASE - 10), S_L)                                         # نوار برق
    poly(p, R(TW - 9, TOP + 6, TW - 1, BASE - 1), S_D, .85)                                       # سایهٔ تیز راست رو
    poly(p, R(-TW + 1, BASE - 8, TW - 1, BASE - 1), S_D)                                          # کرسی
    p.ln((-TW, TOP), (TW, TOP), INNER, NAVY, j=.1); p.ln((TW, TOP), (TW, BASE), INNER, NAVY, j=.1)
    for x0, x1, y in ((-49, -36, -66), (-42, -30, -50), (-48, -38, -2), (36, 46, -66), (33, 44, -50), (38, 47, -2)):
        pass
    for y, xs in ((-62, ((-50, -40), (38, 48))), (-40, ((-47, -36), (36, 46))), (-6, ((-50, -41), (40, 49)))):
        for a, b in xs: p.ln((a, y), (b, y), INNER, '#b8975a', j=.1)
    # ۲ حلقهٔ طاق و دهانه
    ring = [(-RR, BASE - 1), (RR, BASE - 1), (RR, OY)] + ell(0, OY, RR, RR, 0, -180, 22)[1:] + [(-RR, OY)]
    p.shape(ring, S_L, INNER, j=.08, step=7, clip=False)
    hole = [(-OR_, BASE - 1), (OR_, BASE - 1), (OR_, OY)] + ell(0, OY, OR_, OR_, 0, -180, 22)[1:] + [(-OR_, OY)]
    p.shape(hole, HOLE, INNER, j=.08, step=7, clip=False)
    poly(p, R(-OR_ + 1, BASE - 5, OR_ - 1, BASE - 1), '#5a4690')
    # ۳ لنگه‌ها
    th = math.degrees(math.acos(9 / OR_))
    leafL = [(-OR_, BASE - 1), (-9, 3)] + [(-x, y) for x, y in ell(0, OY, OR_, OR_, -th, 0, 8)][::-1][:0] + [(-x, y) for x, y in ell(0, OY, OR_, OR_, -th, 0, 8)]
    leafR = [(OR_, BASE - 1), (9, 3)] + ell(0, OY, OR_, OR_, -th, 0, 8)
    p.shape(leafL, W_B, INNER, j=.08, step=7, clip=False)
    poly(p, R(-OR_ + 3, -14, -OR_ + 6, BASE - 6), W_L); disc(p, -13, -6, 2.4, YEL)
    with layer(p, 'leaf'):
        p.shape(leafR, W_B, INNER, j=.08, step=7, clip=False)
        poly(p, R(OR_ - 6, -14, OR_ - 3, BASE - 6), W_L); disc(p, 13, -6, 2.4, YEL)
    # ۴ تابلو
    p.shape(R(-27, -75, 27, -60), W_B, INNER, j=.1, step=7, clip=False)
    poly(p, R(-25, -73, 25, -70.5), W_L); poly(p, R(-25, -63, 25, -61.5), W_D)
    disc(p, 0, -67.5, 4.4, YEL); disc(p, -20, -67.5, 2, YEL); disc(p, 20, -67.5, 2, YEL)

    # کتیبهٔ بالا (cornice) پهن‌تر از بدنه
    CT, CB, CW = -94, -80, 57
    cs = [(-CW, CB), (CW, CB), (CW + D, CB - E), (CW + D, CT - E), (-CW + D, CT - E), (-CW, CT)]
    p.shape(cs, S_B, OUT, j=.1, step=7)
    poly(p, [(-CW, CT), (CW, CT), (CW + D, CT - E), (-CW + D, CT - E)], S_L)
    poly(p, [(CW, CT), (CW + D, CT - E), (CW + D, CB - E), (CW, CB)], S_D)
    poly(p, R(-CW + 4, CT + 4, -CW + 8, CB - 3), S_L)
    poly(p, R(CW - 9, CT + 3, CW - 1, CB - 1), S_D, .85)
    p.ln((-CW, CT), (CW, CT), INNER, NAVY, j=.1); p.ln((CW, CT), (CW, CB), INNER, NAVY, j=.1)
    p.ln((-CW, CB), (CW, CB), INNER, NAVY, j=.1)
    TOP2 = CT
    # ۵ پرچم
    p.ln((48, TOP2 - 7), (48, TOP2 - 27), PART, W_D, j=0)
    p.shape([(47, TOP2 - 27), (72, TOP2 - 20), (47, TOP2 - 13)], YEL, INNER, j=.05, step=99, clip=False)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'city_gate', STAND, motion={'leaf': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_city_gate_leaf': dict(
        type='scaleX افقی حول لولا (لبهٔ راست لنگه)', hinge_x_symbol=round(p.X((OR_, 0))[0], 1), scale_from=1.6, scale_to=1.0,
        duration_s=1.4, easing='ease-out', loop=False, start='لنگهٔ راست نیمه‌بسته (پهن‌تر)', end='حالت ایستا: باز؛ پهنای ظاهری ۱۶ واحد',
        note='فقط هنگام رسیدن، یک‌بار؛ لنگهٔ چپ و بدنه ثابت؛ بدون حلقهٔ بیکار.'), 'reduced_motion': 'باز (حالت ایستا)'}
    (OUTD / 'city_gate.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
