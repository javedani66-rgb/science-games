#!/usr/bin/env python3
"""ایستگاه «فانوس دریایی» (E04): قهرمان = برج راه‌راه با اتاقک چراغ، سکوی دریایی.
لایهٔ متحرک node_lighthouse_light = دو پرتو چپ و راست (چشمک: روشن/خاموش، بدون خروج از سکو).
برج و اتاقک چراغ ثابت و کامل زیر پرتو."""
import sys, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit3/lighthouse'
import functools, station_kit as _k   # D122/D123: حاشیهٔ چپ/راست ≥۴px (بدون دست‌زدن به کیت)
_k.margin_check = functools.partial(_k.margin_check, min_margin=4); _k.motion_check = functools.partial(_k.motion_check, min_margin=4)
XF = (1.0, -18.0, 0.0)             # قاب قهرمان: (مقیاس هندسه، dx، dy) در واحد symbol؛ ضخامت خط ثابت می‌ماند
RED = '#ef6a4a'; RED_D = '#c9452c'; WHITE = '#fffaf0'; WHITE_D = '#e6dcf0'; GLASS = '#ffd84d'; GLASS_D = '#d9961c'; ROOF = '#ef6a4a'
BEAM = '#ffe45c'; ROCK = '#c9c2e6'; ROCK_D = '#8f88c4'; ROCK_L = '#ece8ff'; DOOR = '#7a3a12'; SEA_W = '#d6e8ff'
YB, YT = -8, -58           # پای برج، بالای برج
WB, WT = 26, 17            # نیم‌پهنای پایین/بالا
LY = -80                   # ارتفاع مرکز اتاقک چراغ
BX = 47                    # دورترین نقطهٔ پرتوها از محور


def hw(y): return WB + (WT - WB) * (y - YB) / (YT - YB)


def poly(p, pts, col, op=1):
    """چندضلعی تیز (بدون گردشدن گوشه‌ها) در قاب قهرمان."""
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def build(out=OUTD):
    p = Pen('lighthouse', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(0, 15, 38); p.foot_tip(0, 15, 18)
    # پرتوها (لایهٔ متحرک): هر طرف یک پرتوی کوتاه افقی و یک پرتوی بلند رو به بالا؛ متقارن حول محور برج
    with layer(p, 'light'):
        for s_ in (-1, 1):
            poly(p, [(s_ * 11, LY - 2), (s_ * 30, LY - 8), (s_ * 30, LY + 5), (s_ * 11, LY + 2)], BEAM, .95)
            poly(p, [(s_ * 11, LY - 8), (s_ * BX, LY - 38), (s_ * (BX + 2), LY - 20)], BEAM, .95)
    # صخرهٔ پایه: سنگ اصلی + دو سنگ کوچک
    p.shape([(-35, 16), (-33, 2), (-22, -8), (22, -8), (33, 2), (35, 16)], ROCK, PART, j=.3, step=99)
    p.ln((-22, 8), (-6, 3), INNER, ROCK_D, j=.1); p.ln((10, 4), (26, 10), INNER, ROCK_D, j=.1); p.ln((-26, -1), (-16, -4), INNER, ROCK_L, j=.1)
    p.shape([(30, 14), (30, 8), (36, 6), (42, 14)], ROCK_L, PART, j=.3, step=99) if False else None
    # برج
    body = [(-WB, YB), (WB, YB), (WT, YT), (-WT, YT)]
    p.shape(body, WHITE, OUT, j=.2, step=5)
    for a_, b_ in ((-18, -31), (-43, -58)):                           # نوارهای قرمز، به‌اندازهٔ دیوارهٔ برج
        poly(p, [(-hw(a_), a_), (hw(a_), a_), (hw(b_), b_), (-hw(b_), b_)], RED)
    poly(p, [(hw(YB) * .35, YB), (hw(YB), YB), (hw(YT), YT), (hw(YT) * .35, YT)], '#241a5e', .13)    # سایهٔ سمت راست
    p.stroke(body, OUT, j=.2, step=5)
    p.shape([(-6, YB), (6, YB), (6, -20), (0, -25), (-6, -20)], DOOR, INNER, j=.1, step=99, clip=False)   # در
    for wy in (-37,):                                                       # پنجرهٔ برج (نوار سفید میانی)
        p.shape([(-4, wy - 6), (4, wy - 6), (4, wy + 6), (-4, wy + 6)], GLASS, INNER, j=.1, step=99, clip=False)
    # اتاقک چراغ + بالکن + سقف
    p.shape([(-11, YT - 7), (11, YT - 7), (11, LY - 12), (-11, LY - 12)], GLASS, PART, j=.2, step=5)
    p.ln((0, YT - 20), (0, LY - 9), INNER, GLASS_D, j=.1, probe='خط داخلی (قاب چراغ)')
    p.shape([(-30, YT), (30, YT), (30, YT - 7), (-30, YT - 7)], GLASS_D, PART, j=.2, step=5)             # کف بالکن
    for x_ in (-26, -13, 13, 26):
        p.ln((x_, YT - 7), (x_, YT - 17), INNER, '#241a5e', j=.05)                                        # تیرک نرده
    p.ln((-28, YT - 17), (28, YT - 17), INNER, '#241a5e', j=.05)                                          # دستهٔ نرده
    p.shape([(-15, LY - 12), (15, LY - 12), (0, LY - 31)], ROOF, PART, j=.2, step=5)
    p.shape(ell(0, LY - 36, 4.5, 4.5, 0, 360, 14), GLASS, INNER, j=.1, step=99, clip=False)               # گوی نوک سقف
    return p


STAND = None     # خودکار: find_stand

if __name__ == '__main__':
    p = build()
    r = finish(p, 'lighthouse', STAND, motion={'light': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    ax = p.X((0, 0))[0]; xl = p.X((-BX, 0))[0]; xr = p.X((BX, 0))[0]       # تقارن پرتوها حول محور برج
    sym_err = round(abs((ax - xl) - (xr - ax)), 3)
    sp = r['spec']; sp['motion_spec'] = dict(kind='blink', note='پرتوها با opacity روشن/خاموش؛ بدنه و اتاقک ثابت', beams_symmetry_error=sym_err)
    assert sym_err < .01
    (OUTD / 'lighthouse.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(r, ensure_ascii=False, indent=1))
